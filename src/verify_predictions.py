"""Recount saved prediction evidence without importing evaluator code."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

def verify(folder,predictions):
    folder=Path(folder);predictions=Path(predictions)
    hashes=json.loads((folder/'prediction-hashes.json').read_text())
    table=pd.read_csv(folder/'metrics.csv')
    checks=0
    for name,digest in hashes.items():
        p=predictions/name
        assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
        source,target,seed,aug,model,condition=p.stem.split('-')
        d=np.load(p,allow_pickle=False);truth=d['y'];guess=d['p']>=.5;error=truth!=guess
        rows=table[(table.source==source)&(table.target==target)&(table.seed==int(seed))&(table.augmented==bool(int(aug)))&(table.model==model)&(table.condition==condition)]
        assert len(rows)==10,(name,len(rows))
        for _,r in rows.iterrows():
            assert r.n==len(truth) and r.errors==error.sum()
            assert r.fn==((truth==1)&~guess).sum()
            assert r.fp==((truth==0)&guess).sum()
            assert r.reviewed_errors+r.unreviewed_fn+r.unreviewed_fp==r.errors
            assert r.accepted+r.reviewed==r.n
            if r.policy=='frozen':
                threshold=d['cal_thresholds'][[.01,.05,.1].index(r.budget)]
                mask=(1-np.abs(2*d['p']-1))>threshold
                assert mask.sum()==r.reviewed
                assert error[mask].sum()==r.reviewed_errors
            elif r.policy in ['cap','random']:
                expected=sum(int(np.floor(r.budget*(d['hours']==h).sum())) for h in np.unique(d['hours']))
                assert r.reviewed==expected
            checks+=1
    assert checks==len(table)
    report={'prediction_files_checked':len(hashes),'metric_rows_recounted':checks,'passed':True,'scope':'Hashes, forced errors, conservation identities, frozen routing and hourly budget counts; does not independently validate labels, sampling or model fitting.'}
    (folder/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('predictions');a=p.parse_args();verify(a.folder,a.predictions)
