"""Post-primary sensitivity study; original evaluator and outputs remain intact."""
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
from evaluate import EXCLUDE, partitions, families, corrupt, review_mask, counts

ROOT=Path(__file__).resolve().parents[1]

def weighted_test(full, unique, boundary, features):
    eligible=full.loc[full.FLOW_START_MILLISECONDS>=boundary].copy()
    x=eligible[features].astype('float64').replace([np.inf,-np.inf],np.nan)
    eligible['_hash']=pd.util.hash_pandas_object(x,index=False).to_numpy()
    return eligible.loc[eligible._hash.isin(unique._hash)].sort_values('_row')

def run():
    out=ROOT/'analysis/sensitivity-v2'
    out.mkdir(exist_ok=False)
    evidence=ROOT/'data/processed/predictions-sensitivity-v2'
    evidence.mkdir(exist_ok=False)
    data={n:pd.read_pickle(ROOT/'data/processed'/f'{n}.pkl') for n in ['unsw','ton','cic']}
    features=[c for c in data['unsw'] if c not in EXCLUDE]
    parts={};receipts={}
    for n,d in data.items(): parts[n],receipts[n]=partitions(d,features)
    groups=families(features)
    metrics=[];fits=[];manifest={}
    with threadpool_limits(limits=2):
      for source in data:
        train=parts[source]['train'];cal=parts[source]['cal']
        assert train.Label.nunique()==cal.Label.nunique()==2
        seen=set(train._hash)|set(cal._hash)
        raw=train[features].to_numpy(dtype=float,copy=True)
        raw[~np.isfinite(raw)]=np.nan
        med=np.nan_to_num(np.nanmedian(raw,axis=0))
        def prep(x):
            missing=~np.isfinite(x)
            x=np.where(missing,med,x)
            return np.column_stack([np.sign(x)*np.log1p(np.abs(x)),missing.astype(float)])
        populations={}
        for target in data:
            if target==source: continue
            unique=parts[target]['test']
            unique=unique.loc[~unique._hash.isin(seen)].sort_values('_row')
            weighted=weighted_test(data[target],unique,receipts[target]['boundaries_ms'][1],features)
            assert set(unique._hash)==set(weighted._hash)
            populations[target]={'unique':unique,'weighted':weighted}
        for seed in [17,29,43]:
          for variant in ['clean','repeat','mask']:
            x=raw.copy();y=train.Label.to_numpy(int)
            if variant!='clean':
                extra=x.copy()
                if variant=='mask':
                    choice=np.random.default_rng(seed).integers(0,3,len(x))
                    for i,ids in enumerate(groups.values()): extra[np.ix_(choice==i,ids)]=np.nan
                x=np.concatenate([x,extra]);y=np.tile(y,2)
            scaler=StandardScaler().fit(prep(x))
            xx=scaler.transform(prep(x))
            for modelname in ['logistic','forest']:
                model=LogisticRegression(C=1,max_iter=500,random_state=seed) if modelname=='logistic' else RandomForestClassifier(n_estimators=100,max_depth=16,min_samples_leaf=5,n_jobs=2,random_state=seed)
                start=time.perf_counter();model.fit(xx,y)
                fit={'source':source,'seed':seed,'variant':variant,'model':modelname,'rows':len(y),'seconds':time.perf_counter()-start}
                fits.append(fit)
                cp=model.predict_proba(scaler.transform(prep(cal[features].to_numpy(float))))[:,1]
                threshold=float(np.quantile(1-np.abs(2*cp-1),.95,method='higher'))
                for target,pops in populations.items():
                  for population,test in pops.items():
                    assert len(test)>0
                    ytest=test.Label.to_numpy(int)
                    hours=test.FLOW_START_MILLISECONDS.to_numpy(np.int64)//3600000
                    for condition in ['clean','temporal','size','tcp','temporal+tcp']:
                        x=corrupt(test[features].to_numpy(float),condition,groups,seed)
                        prob=model.predict_proba(scaler.transform(prep(x)))[:,1]
                        pred=(prob>=.5).astype(int);score=1-np.abs(2*prob-1)
                        base={'source':source,'target':target,'seed':seed,'variant':variant,'model':modelname,'population':population,'condition':condition}
                        name=f'{len(manifest):04d}.npz'
                        masks={'forced':np.zeros(len(test),bool),'frozen':score>threshold,'cap':review_mask(score,hours,.05),'random':review_mask(score,hours,.05,True,seed)}
                        np.savez_compressed(evidence/name,p=prob,y=ytest,hours=hours,rows=test._row.to_numpy(),threshold=np.array(threshold),**{'review_'+k:v for k,v in masks.items()})
                        manifest[name]={'sha256':hashlib.sha256((evidence/name).read_bytes()).hexdigest(),**base}
                        for policy,mask in masks.items():
                            metrics.append({**base,'policy':policy,'budget':0 if policy=='forced' else .05,'threshold':threshold if policy=='frozen' else None,**counts(ytest,pred,mask)})
                print(json.dumps(fit),flush=True)
                pd.DataFrame(metrics).to_csv(out/'metrics.csv',index=False)
                pd.DataFrame(fits).to_csv(out/'fits.csv',index=False)
                (out/'prediction-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (out/'split-receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    print('Complete',len(metrics),'metric rows',flush=True)

if __name__=='__main__':run()
