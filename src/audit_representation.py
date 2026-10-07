"""Exploratory ambiguity diagnostic, not a representation-selection procedure."""
import json
from pathlib import Path
import pandas as pd
from evaluate import EXCLUDE

root=Path(__file__).resolve().parents[1]
result={}
for name in ['unsw','ton','cic']:
    df=pd.read_pickle(root/'data/processed'/f'{name}.pkl')
    result[name]={}
    for mode,drop in [('primary',EXCLUDE),('extended',{'IPV4_SRC_ADDR','IPV4_DST_ADDR','FLOW_START_MILLISECONDS','FLOW_END_MILLISECONDS','Label','Attack','_row'})]:
        keys=pd.util.hash_pandas_object(df[[c for c in df if c not in drop]].astype('float64'),index=False)
        groups=pd.DataFrame({'h':keys,'y':df.Label}).groupby(['h','y']).size().unstack(fill_value=0)
        result[name][mode]={'conflicting_patterns':int(((groups[0]>0)&(groups[1]>0)).sum()),'minimum_errors_on_full_sample':int(groups.min(axis=1).sum()),'sample_n':len(df)}
(root/'analysis/representation-ambiguity.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result))
