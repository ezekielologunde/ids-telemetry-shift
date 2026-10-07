"""Apply checked sensitivity results to the existing source and its template."""
import json
from pathlib import Path
import pandas as pd

root=Path(__file__).resolve().parents[1]
folder=root/'analysis/sensitivity-v2'
check=json.loads((folder/'verification.json').read_text())
assert check['passed'] and check['primary_bridge_rows']==1440
b=pd.read_csv(folder/'budget-summary.csv')
m=pd.read_csv(folder/'mask-comparison-summary.csv')
rows=[]
for _,r in b.iterrows():
    rows.append(f"{r.population} & {r.variant} & {int(r.exceedances)}/{int(r.cells)} & {100*r.mean_review:.2f}" + r" \\")
cap=m[(m.population=='weighted')&(m.policy=='cap')].iloc[0]
section=r"""
\section{Post-Primary Sensitivity Extension}
An internal methodological review motivated a separately frozen exploratory extension after the primary outcomes were known. It reuses the same samples and is not an independent confirmation. All original source partitions, representations, model settings, seeds, clean-source calibration and hourly routing rules remain fixed. The extension covers six cross-domain pairs, five deterministic observation conditions and the five-percent nominal budget; random cell masking is omitted so adding repeated occurrences does not alter a pattern's mask.

Two evaluation populations isolate a specific duplicate-handling choice. The unique population exactly reproduces the original eligible test rows. The weighted population includes every sampled test-period occurrence whose uncorrupted predictor pattern belongs to that eligible set, retaining each occurrence's recorded label. This restores sampled multiplicity, including conflicting labels, while holding pattern eligibility fixed. It is conditional sampled-flow weighting, not full-volume operational prevalence.

A repeated-clean variant concatenates the clean training data with itself, matching the masked-copy variant's row count. It does not match information content, stochastic optimizer work or runtime. The extension comprises 54 fits, 1,080 saved prediction conditions and 4,320 metric rows. An independently implemented routing recount verifies those rows from saved probabilities, including cap tie-breaking and random selection. All 1,440 overlapping unique-population clean/masked rows match the original metrics to an absolute floating-point tolerance of $10^{-12}$. Seven boundary tests pass.

\begin{table}[t]
\centering
\caption{Exploratory extension at nominal 5 percent. Exceedances count dependent designed cells. Mean review is a percentage; clean, repeat and mask denote training variants.}
\begin{tabular}{llll}
\toprule
Population & Variant & Exceedances & Mean review \\
\midrule
"""+"\n".join(rows)+r"""
\bottomrule
\end{tabular}
\end{table}

Frozen-threshold capacity mismatch persists in both populations and all training variants. Across the extension, 436 of 540 unique-population cells and 435 of 540 weighted-population cells exceed five-percent review. These counts cover a different condition set and an additional training control, so they must not be added to the primary 362/432 figure as independent evidence.

"""+f"The masked-copy variant increases mean unreviewed error under the hourly uncertainty cap by {100*cap.mean_residual_delta:.3f} percentage points relative to repeated-clean training in the weighted population. Of {int(cap.cells)} paired cells, masking has lower residual error in {int(cap.mask_lower)}, ties in {int(cap.ties)}, and higher error in {int(cap.mask_higher)}. "+r"""The mixed pattern and small aggregate differences do not establish that either variant is universally preferable. They do rule out a consistent masking benefit in this extension. The interpretation is narrower than a causal attribution to missingness augmentation, because other training dynamics remain unmatched.

This extension addresses two specific validity concerns but does not resolve target-label calibration, prospective deployment, additional independent domains, or exact reproduction of the closest methods.

"""
oldref=r"\bibitem{riskgate} Budget-aware two-stage NetFlow intrusion detection for high-traffic critical information infrastructure under domain shift. 2026. Publisher record, PII S187454822600048X. \url{https://www.sciencedirect.com/science/article/abs/pii/S187454822600048X}. Accessible indexed abstract and sections consulted; full methods unavailable."
newref=r"\bibitem{riskgate} Ha Thanh Dung. 2026. Budget-aware two-stage NetFlow intrusion detection for high-traffic critical information infrastructure under domain shift. \emph{International Journal of Critical Infrastructure Protection} 54, 100876. \url{https://doi.org/10.1016/j.ijcip.2026.100876}. Accessible publisher abstract and sections consulted; full methods unavailable."
replacements={
oldref:newref,
"Our simpler family-mask variant is an established-method baseline, not an exact MaskAug implementation. Because our variant adds training rows and changes effective forest leaf support, its comparison does not isolate masking from every training-budget effect.":"Our simpler family-mask variant is an established-method baseline, not an exact MaskAug implementation. The primary comparison changes training row count and effective forest leaf support. A post-primary extension adds a repeated-clean control, while retaining limitations on matched optimization effort.",
"The augmentation comparison is secondary and lacks a matched repeated-clean training control; it cannot establish a uniquely causal masking benefit.":"The primary augmentation comparison lacked a matched repeated-clean training control. The post-primary extension supplies equal training row counts, but does not establish a uniquely causal masking benefit or match every optimization effect.",
"A subsequent extension should use a separately frozen protocol with volume-weighted evaluation, a matched augmentation control, independent label assessment where possible, and a prospective or additional-domain test set.":"The post-primary extension adds conditional occurrence weighting and an equal-row augmentation control. Full-volume evaluation, independent label assessment where possible, and a prospective or additional-domain test set remain necessary for broader claims.",
"including target-domain calibration\\cite{riskgate}.":"including labeled target-domain calibration and adaptive allocation across micro-batches\\cite{riskgate}."
}
for name in ['main.tex','manuscript-template.tex']:
    path=root/'paper'/name
    text=path.read_text(encoding='utf-8-sig')
    assert r'\section{Post-Primary Sensitivity Extension}' not in text
    text=text.replace(r'\section{Discussion and Threats to Validity}',section+r'\section{Discussion and Threats to Validity}')
    for a,z in replacements.items():
        assert a in text,(name,a[:60])
        text=text.replace(a,z)
    path.write_text(text,encoding='utf-8')
print('Updated existing manuscript and template; no PDF rebuilt.')
