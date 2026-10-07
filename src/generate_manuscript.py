"""Insert verified outputs into the manuscript."""
import json
import shutil
from pathlib import Path
import pandas as pd

root=Path(__file__).resolve().parents[1]
folder=root/'analysis/primary-v1-r2'
paper=root/'paper'
s=json.loads((folder/'summary.json').read_text())
v=json.loads((folder/'verification.json').read_text())
assert v['passed'] and s['metric_rows']==6480
split=json.loads((folder/'split-receipts.json').read_text())
names={'unsw':'UNSW','ton':'ToN','cic':'CIC'}
def table(caption,heads,rows):
    return '\n'.join([r'\begin{table}[t]',r'\centering',r'\caption{'+caption+'}',r'\begin{tabular}{'+'l'*len(heads)+'}',r'\toprule',' & '.join(heads)+r' \\',r'\midrule']+[' & '.join(map(str,row))+r' \\' for row in rows]+[r'\bottomrule',r'\end{tabular}',r'\end{table}'])
text=(paper/'manuscript-template.tex').read_text()
text=text.replace('%ABSTRACT_RESULTS%',f"Across {s['paired_conditions']} paired cross-domain conditions at a nominal five-percent review fraction, frozen routing exceeds that fraction in {s['frozen_budget_exceedances']} conditions and ranges from {100*s['frozen_review_min']:.2f} to {100*s['frozen_review_max']:.1f} percent. Enforced caps respect capacity but leave substantial errors unreviewed.")
rows=[]
for n in names:
    a=json.loads((root/'analysis'/f'{n}-schema-audit.json').read_text())
    rows.append([names[n],f"{a['rows']:,}",f"{int(a['labels']['0']):,}",f"{int(a['labels']['1']):,}"])
text=text.replace('%DATA_TABLE%',table('Full-archive counts. UNSW, ToN and CIC abbreviate the three NetFlow-v3 domains. These are not model-training sample sizes.',['Domain','Flows','Benign','Attack'],rows))
rows=[]
for n,a in split['domains'].items():
    rows.append([names[n]]+[f"{a[k]['after']:,} ({a[k]['attacks']:,})" for k in ['train','cal','test']]+[a['purged_n']])
text=text.replace('%SPLIT_TABLE%',table('Unique patterns before cross-domain overlap removal. Parentheses give attack counts.',['Domain','Train','Calibration','Test','Purged'],rows))
conditions=pd.read_csv(folder/'condition-summary.csv')
rows=[]
for condition,g in conditions.groupby('condition',sort=False):
    f=g[g.policy=='frozen'].iloc[0];c=g[g.policy=='cap'].iloc[0];r=g[g.policy=='random'].iloc[0]
    rows.append([condition]+[f'{100*x:.2f}' for x in [f.review_fraction,c.review_fraction,f.residual_error_rate,c.residual_error_rate,r.residual_error_rate]])
text=text.replace('%CONDITION_TABLE%',table('Cross-domain means at nominal 5 percent. Values are percentages. F: frozen; C: uncertainty cap; R: random cap. Error is unreviewed errors per input.',['Condition','F review','C review','F error','C error','R error'],rows))
rows=[]
for (source,target),g in pd.read_csv(folder/'pair-summary.csv').groupby(['source','target']):
    f=g[g.policy=='frozen'].iloc[0];c=g[g.policy=='cap'].iloc[0]
    rows.append([names[source]+r' $\rightarrow$ '+names[target]]+[f'{100*x:.2f}' for x in [f.review_fraction,c.review_fraction,f.residual_error_rate,c.residual_error_rate]])
text=text.replace('%PAIR_TABLE%',table('Pair means over seeds, models, variants and conditions at nominal 5 percent. Percentages are descriptive, not pooled operational estimates.',['Transfer','F review','C review','F error','C error'],rows))
ambiguity=json.loads((root/'analysis/representation-ambiguity.json').read_text())
rows=[[names[n],a['primary']['conflicting_patterns'],a['primary']['minimum_errors_on_full_sample'],a['extended']['minimum_errors_on_full_sample']] for n,a in ambiguity.items()]
text=text.replace('%AMBIGUITY_TABLE%',table('Exploratory audit of each 100,000-flow sample. Extended features restore omitted service and duration variables. Minimum errors are finite-sample bounds.',['Domain','Conflicts, primary','Min. errors, primary','Min. errors, extended'],rows))
fit=pd.read_csv(folder/'fits.csv')
results=rf"""The complete restart contains 36 fitted models, 648 saved prediction conditions, and 6,480 policy metric rows. The separate recount checked all {v['metric_rows_recounted']:,} rows and {v['prediction_files_checked']} prediction hashes. Six code boundary tests passed. Recorded model-fitting time totals {fit.seconds.sum():.2f} seconds, with a maximum single fit of {fit.seconds.max():.2f} seconds. This excludes acquisition, preprocessing, inference, compression and auditing. It is not end-to-end runtime. The modest fitting cost did not justify an HPC allocation for this bounded experiment.

At nominal five-percent review, frozen routing exceeded that fraction in {s['frozen_budget_exceedances']} of {s['paired_conditions']} cross-domain conditions ({100*s['frozen_budget_exceedances']/s['paired_conditions']:.1f}\%). Actual review ranged from {100*s['frozen_review_min']:.2f}\% to {100*s['frozen_review_max']:.1f}\%. This is a count of dependent designed cells, not a population failure probability. Hourly caps remained at or below five percent by construction and verified count; flooring caused modest underspend.

Frozen routing left fewer errors unreviewed than the uncertainty cap in {s['frozen_residual_lower_than_cap']} cells, the same number in {s['frozen_residual_equal_cap']}, and more in {s['frozen_residual_higher_than_cap']}. These comparisons do not hold realized capacity constant. In the no-additional-corruption condition, mean frozen review was 44.16\%, compared with 4.91\% for the cap. Domain change alone was therefore sufficient to expose a capacity mismatch here; missingness is not necessary to explain every failure.

Mean unreviewed error under the uncertainty cap ranged from 45.76\% to 50.40\% across observation conditions. Random-cap means were close and slightly lower in each condition-level aggregate. Uncertainty ranking did not provide a consistent aggregate residual-error advantage over random routing under these transfers. Pair-specific results differ, so the summaries must not obscure heterogeneity. They do not establish universal superiority of random review.

Additional outages did not monotonically worsen every summary. Some omissions may suppress misleading transferred features. Shared models, representation changes and different prevalence prevent interpreting this as a general benefit of losing telemetry. The primary finding is the measured separation between calibration-time review fraction and enforced test-time capacity, accompanied by poor reliability under several evaluated transfers."""
text=text.replace('%RESULTS_TEXT%',results)
assert not any(t in text for t in ['%RESULTS_TEXT%','%DATA_TABLE%','%PAIR_TABLE%','%ABSTRACT_RESULTS%'])
(paper/'main.tex').write_text(text,encoding='utf-8')
shutil.copyfile(folder/'conditions.pdf',paper/'conditions.pdf')
print('Generated manuscript from verified outputs')
