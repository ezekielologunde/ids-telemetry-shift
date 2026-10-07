"""Produce descriptive tables, no flow-independent significance assumptions."""
import argparse
import json
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def summarize(folder):
    folder=Path(folder)
    df=pd.read_csv(folder/'metrics.csv')
    cross=df[(df.source!=df.target)&(df.budget==.05)].copy()
    cross['residual_error_rate']=(cross.unreviewed_fn+cross.unreviewed_fp)/cross.n
    cross['error_capture']=cross.reviewed_errors/cross.errors.replace(0,float('nan'))
    table=cross.groupby(['condition','policy'],as_index=False)[['review_fraction','residual_error_rate','accepted_risk','error_capture']].mean()
    table.to_csv(folder/'condition-summary.csv',index=False)
    pair=cross.groupby(['source','target','policy'],as_index=False)[['review_fraction','residual_error_rate']].mean()
    pair.to_csv(folder/'pair-summary.csv',index=False)
    # Each row has equal descriptive weight; no claim of independent replication.
    keys=['source','target','seed','augmented','model','condition']
    f=cross[cross.policy=='frozen'].set_index(keys)
    cap=cross[cross.policy=='cap'].set_index(keys)
    diff=f.residual_error_rate-cap.residual_error_rate
    report={'metric_rows':len(df),'cross_5pct_rows':len(cross),'paired_conditions':len(diff),'frozen_budget_exceedances':int((f.review_fraction>.05+1e-12).sum()),'frozen_review_min':float(f.review_fraction.min()),'frozen_review_max':float(f.review_fraction.max()),'frozen_residual_lower_than_cap':int((diff<-1e-12).sum()),'frozen_residual_equal_cap':int((diff.abs()<=1e-12).sum()),'frozen_residual_higher_than_cap':int((diff>1e-12).sum()),'note':'Descriptive cells reuse domains and samples; not independent trials.'}
    (folder/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
    fig,axes=plt.subplots(1,2,figsize=(10,3.5),layout='constrained')
    for policy,g in table.groupby('policy'):
        axes[0].plot(g.condition,g.review_fraction,marker='o',label=policy)
        axes[1].plot(g.condition,g.residual_error_rate,marker='o',label=policy)
    axes[0].axhline(.05,color='gray',linestyle='--');axes[0].set_ylabel('Mean review fraction')
    axes[1].set_ylabel('Mean unreviewed errors / all flows')
    for ax in axes:
        ax.tick_params(axis='x',rotation=35);ax.legend();ax.grid(alpha=.2)
    fig.savefig(folder/'conditions.pdf');fig.savefig(folder/'conditions.png',dpi=160)
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');a=p.parse_args();summarize(a.folder)
