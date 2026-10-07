"""Independent routing recount and bridge to preserved primary metrics."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',default=str(root/'analysis/sensitivity-v2'))
out=Path(parser.parse_args().output)
df=pd.read_csv(out/'metrics.csv')
manifest=json.loads((out/'prediction-manifest.json').read_text())
keys=['source','target','seed','variant','model','population','condition']
indexed=df.set_index(keys).sort_index()
checked=0
for name,meta in manifest.items():
    path=root/'data/processed'/('predictions-'+out.name)/name
    assert hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256']
    with np.load(path,allow_pickle=False) as a:
        y=a['y'];pred=a['p']>=.5;err=y!=pred;uncertainty=1-np.abs(2*a['p']-1)
        rows=indexed.loc[tuple(meta[k] for k in keys)]
        assert len(rows)==4
        for _,r in rows.iterrows():
            actual=a['review_'+r.policy]
            if r.policy=='forced': expected=np.zeros(len(y),bool)
            elif r.policy=='frozen': expected=uncertainty>float(a['threshold'])
            else:
                priority=np.random.default_rng(int(meta['seed'])).random(len(y)) if r.policy=='random' else uncertainty
                expected=np.zeros(len(y),bool)
                for h in np.unique(a['hours']):
                    ids=np.flatnonzero(a['hours']==h)
                    order=np.lexsort((a['rows'][ids],-priority[ids]))
                    expected[ids[order[:int(np.floor(.05*len(ids)))]]]=True
            assert np.array_equal(actual,expected),(name,r.policy)
            assert r.n==len(y) and r.errors==err.sum()
            assert r.reviewed==actual.sum() and r.reviewed_errors==err[actual].sum()
            assert r.unreviewed_fn==((y==1)&~pred&~actual).sum()
            assert r.unreviewed_fp==((y==0)&pred&~actual).sum()
            assert r.accepted==len(y)-actual.sum()
            checked+=1
assert checked==4320 and len(manifest)==1080
primary=pd.read_csv(root/'analysis/primary-v1-r2/metrics.csv')
primary=primary[(primary.source!=primary.target)&(primary.condition!='random10')&((primary.budget==.05)|(primary.policy=='forced'))].copy()
primary['variant']=primary.augmented.map({False:'clean',True:'mask'})
bridge=df[(df.population=='unique')&df.variant.isin(['clean','mask'])]
join=['source','target','seed','variant','model','condition','policy']
merged=bridge.merge(primary,on=join,suffixes=('_v2','_v1'),validate='one_to_one')
assert len(merged)==1440
fields=['n','attacks','reviewed','errors','reviewed_errors','unreviewed_fn','unreviewed_fp','fn','fp','accepted']
for c in fields: assert (merged[c+'_v2']==merged[c+'_v1']).all(),c
for c in ['review_fraction','accepted_risk','threshold']:
    assert np.allclose(merged[c+'_v2'],merged[c+'_v1'],rtol=0,atol=1e-12,equal_nan=True),c
report={'prediction_files':len(manifest),'metric_rows':checked,'primary_bridge_rows':len(merged),'passed':True,'scope':'Routing recomputed independently from saved probabilities; metric counts and original-metric bridge verified. Labels and model fitting are not independently validated.'}
(out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
