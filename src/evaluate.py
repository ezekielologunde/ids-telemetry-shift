"""Frozen primary evaluation. Reads only locally generated sample pickles."""
import argparse
import hashlib
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

EXCLUDE = {'IPV4_SRC_ADDR','IPV4_DST_ADDR','FLOW_START_MILLISECONDS','FLOW_END_MILLISECONDS','Label','Attack','_row','DNS_QUERY_ID','DURATION_IN','DURATION_OUT','L4_SRC_PORT','L4_DST_PORT','L7_PROTO'}

def partitions(df, features):
    df = df.sort_values(['FLOW_START_MILLISECONDS','_row']).copy()
    t = df.FLOW_START_MILLISECONDS.to_numpy()
    a, b = t[int(.6*len(t))], t[int(.8*len(t))]
    x = df[features].astype('float64').replace([np.inf,-np.inf],np.nan)
    df['_hash'] = pd.util.hash_pandas_object(x, index=False).to_numpy()
    masks = [(df.FLOW_END_MILLISECONDS<a), (df.FLOW_START_MILLISECONDS>=a)&(df.FLOW_END_MILLISECONDS<b), df.FLOW_START_MILLISECONDS>=b]
    out, seen, receipt = {}, set(), {'boundaries_ms':[int(a),int(b)],'input_n':len(df),'purged_n':int((~(masks[0]|masks[1]|masks[2])).sum())}
    for name, mask in zip(['train','cal','test'],masks):
        part=df.loc[mask].copy()
        before=len(part)
        part=part.drop_duplicates('_hash')
        part=part.loc[~part._hash.isin(seen)].copy()
        seen.update(part._hash.tolist())
        receipt[name]={'before':before,'after':len(part),'attacks':int(part.Label.sum())}
        out[name]=part
    return out,receipt

def families(features):
    groups={
        'temporal':[i for i,c in enumerate(features) if 'IAT' in c or 'FLOW_DURATION' in c],
        'size':[i for i,c in enumerate(features) if any(s in c for s in ['BYTES','PKTS','PKT_LEN','FLOW_PKT','THROUGHPUT'])],
        'tcp':[i for i,c in enumerate(features) if 'TCP' in c]}
    flat=sum(groups.values(),[])
    assert len(set(flat))==len(flat)
    return groups

def corrupt(x, condition, groups, seed):
    x=x.copy()
    if condition=='random10':
        x[np.random.default_rng(seed).random(x.shape)<.1]=np.nan
    elif condition!='clean':
        for group in condition.split('+'):
            x[:,groups[group]]=np.nan
    return x

def review_mask(scores, hours, budget, random=False, seed=17):
    scores=np.random.default_rng(seed).random(len(scores)) if random else scores
    mask=np.zeros(len(scores),bool)
    for hour in np.unique(hours):
        ids=np.flatnonzero(hours==hour)
        count=int(np.floor(budget*len(ids)))
        chosen=ids[np.argsort(-scores[ids],kind='stable')[:count]]
        mask[chosen]=True
    return mask

def counts(y, pred, review):
    wrong=y!=pred
    accepted=~review
    n=len(y)
    return {'n':n,'attacks':int(y.sum()),'reviewed':int(review.sum()),'errors':int(wrong.sum()),'reviewed_errors':int((wrong&review).sum()),'unreviewed_fn':int(((y==1)&(pred==0)&accepted).sum()),'unreviewed_fp':int(((y==0)&(pred==1)&accepted).sum()),'fn':int(((y==1)&(pred==0)).sum()),'fp':int(((y==0)&(pred==1)).sum()),'accepted':int(accepted.sum()),'accepted_risk':float(wrong[accepted].mean()) if accepted.any() else None,'review_fraction':float(review.mean()) if n else None}

def run(data_dir, output):
    out=Path(output);out.mkdir(parents=True,exist_ok=False)
    predictions=Path(data_dir)/('predictions-'+out.name)
    predictions.mkdir(parents=True,exist_ok=False)
    prediction_hashes={}
    datasets={name:pd.read_pickle(Path(data_dir)/f'{name}.pkl') for name in ['unsw','ton','cic']}
    features=[c for c in datasets['unsw'].columns if c not in EXCLUDE]
    assert all(set(features)<=set(df.columns) for df in datasets.values())
    parts={};receipts={};groups=families(features)
    for name,df in datasets.items():
        parts[name],receipts[name]=partitions(df,features)
    (out/'split-receipts.json').write_text(json.dumps({'features':features,'groups':{k:[features[i] for i in v] for k,v in groups.items()},'domains':receipts},indent=2)+'\n')
    results=[]; hour_rows=[]; family_rows=[]; fits=[]
    with threadpool_limits(limits=2):
      for source in parts:
        train,cal=parts[source]['train'],parts[source]['cal']
        if len(train.Label.unique())!=2 or len(cal.Label.unique())!=2:
            raise ValueError(f'{source} lacks both classes in training/calibration')
        seen=set(train._hash)|set(cal._hash)
        raw=train[features].to_numpy(dtype=float,copy=True);raw[~np.isfinite(raw)]=np.nan
        med=np.nanmedian(raw,axis=0);med=np.nan_to_num(med)
        def prep(x):
            missing=~np.isfinite(x)
            x=np.where(missing,med,x)
            return np.column_stack([np.sign(x)*np.log1p(np.abs(x)),missing.astype(float)])
        for seed in [17,29,43]:
          for augmented in [False,True]:
            x=raw.copy(); y=train.Label.to_numpy(int)
            if augmented:
                masked=x.copy(); choices=np.random.default_rng(seed).integers(0,3,len(x))
                for gi,group in enumerate(groups.values()):
                    masked[np.ix_(choices==gi,group)]=np.nan
                x=np.concatenate([x,masked]);y=np.tile(y,2)
            scaler=StandardScaler().fit(prep(x))
            xx=scaler.transform(prep(x))
            for modelname in ['logistic','forest']:
                model=LogisticRegression(C=1,max_iter=500,random_state=seed) if modelname=='logistic' else RandomForestClassifier(n_estimators=100,max_depth=16,min_samples_leaf=5,n_jobs=2,random_state=seed)
                started=time.perf_counter();model.fit(xx,y)
                fits.append({'source':source,'seed':seed,'augmented':augmented,'model':modelname,'rows':len(y),'seconds':time.perf_counter()-started})
                calp=model.predict_proba(scaler.transform(prep(cal[features].to_numpy(float))))[:,1]
                cs=1-np.abs(2*calp-1)
                thresholds={b:float(np.quantile(cs,1-b,method='higher')) for b in [.01,.05,.1]}
                for target in parts:
                    test=parts[target]['test'];before=len(test)
                    test=test.loc[~test._hash.isin(seen)].sort_values('_row')
                    if not len(test): raise ValueError('Empty test after overlap purge')
                    ty=test.Label.to_numpy(int);hours=test.FLOW_START_MILLISECONDS.to_numpy(np.int64)//3600000
                    for condition in ['clean','temporal','size','tcp','temporal+tcp','random10']:
                        tx=corrupt(test[features].to_numpy(float),condition,groups,seed)
                        p=model.predict_proba(scaler.transform(prep(tx)))[:,1];pred=(p>=.5).astype(int);score=1-np.abs(2*p-1)
                        artifact=predictions/f'{source}-{target}-{seed}-{int(augmented)}-{modelname}-{condition}.npz'
                        np.savez_compressed(artifact,p=p,y=ty,hours=hours,rows=test._row.to_numpy(),attack=test.Attack.to_numpy(str),cal_thresholds=np.array([thresholds[b] for b in [.01,.05,.1]]))
                        prediction_hashes[artifact.name]=hashlib.sha256(artifact.read_bytes()).hexdigest()
                        base={'source':source,'target':target,'seed':seed,'augmented':augmented,'model':modelname,'condition':condition,'overlap_removed':before-len(test)}
                        results.append({**base,'policy':'forced','budget':0,**counts(ty,pred,np.zeros(len(ty),bool))})
                        for b in [.01,.05,.1]:
                          for policy in ['frozen','cap','random']:
                            mask=(score>thresholds[b]) if policy=='frozen' else review_mask(score,hours,b,policy=='random',seed)
                            row={**base,'policy':policy,'budget':b,'threshold':thresholds[b] if policy=='frozen' else None,**counts(ty,pred,mask)}
                            results.append(row)
                            if b==.05:
                              for h in np.unique(hours):
                                ix=hours==h
                                hour_rows.append({**base,'policy':policy,'hour':int(h),**counts(ty[ix],pred[ix],mask[ix])})
                              for attack in test.Attack.unique():
                                ix=test.Attack.to_numpy()==attack
                                family_rows.append({**base,'policy':policy,'attack':attack,**counts(ty[ix],pred[ix],mask[ix])})
                print(json.dumps(fits[-1]),flush=True)
                pd.DataFrame(results).to_csv(out/'metrics.csv',index=False)
                pd.DataFrame(fits).to_csv(out/'fits.csv',index=False)
                pd.DataFrame(hour_rows).to_csv(out/'hourly.csv',index=False)
                pd.DataFrame(family_rows).to_csv(out/'families.csv',index=False)
                (out/'prediction-hashes.json').write_text(json.dumps(prediction_hashes,indent=2)+'\n')
    manifest={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.iterdir() if p.is_file()}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data-dir',required=True);p.add_argument('--output',required=True);a=p.parse_args();run(a.data_dir,a.output)
