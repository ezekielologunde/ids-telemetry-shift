"""Descriptive extension summaries, no claims of independent confirmation."""
import argparse
import json
from pathlib import Path
import pandas as pd
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--output',default=str(root/'analysis/sensitivity-v2'))
out=Path(parser.parse_args().output)
assert json.loads((out/'verification.json').read_text())['passed']
d=pd.read_csv(out/'metrics.csv')
d['residual']=(d.unreviewed_fn+d.unreviewed_fp)/d.n
d['forced_error']=d.errors/d.n
f=d[d.policy=='frozen'].copy()
f['exceeds']=f.review_fraction>.05+1e-12
summ=f.groupby(['population','variant']).agg(cells=('n','size'),exceedances=('exceeds','sum'),mean_review=('review_fraction','mean'),min_review=('review_fraction','min'),max_review=('review_fraction','max')).reset_index()
summ.to_csv(out/'budget-summary.csv',index=False)
keys=['source','target','seed','model','population','condition','policy']
m=d[d.variant=='mask'].set_index(keys)
c=d[d.variant=='repeat'].set_index(keys)
delta=(m[['residual','forced_error']]-c[['residual','forced_error']]).reset_index()
delta.to_csv(out/'mask-minus-repeat.csv',index=False)
rows=[]
for (pop,policy),g in delta.groupby(['population','policy']):
    rows.append({'population':pop,'policy':policy,'cells':len(g),'mean_residual_delta':g.residual.mean(),'mask_lower':int((g.residual < -1e-12).sum()),'ties':int((g.residual.abs()<=1e-12).sum()),'mask_higher':int((g.residual > 1e-12).sum())})
pd.DataFrame(rows).to_csv(out/'mask-comparison-summary.csv',index=False)
print(summ.to_string(index=False))
print(pd.DataFrame(rows).to_string(index=False))
