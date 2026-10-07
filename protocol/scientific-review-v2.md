# Scientific review and corrective extension

Date: 7 October 2026. This is an internal methodological review, not external peer review.

## Material findings

1. The primary duplicate rule changes both prevalence and the contribution of conflicting-label occurrences. A result on unique feature patterns cannot be generalized to all traffic. Corrective extension restores every test-period occurrence of the same eligible patterns, including conflicting labels. It remains conditional sampled-flow weighting, not a full-volume operational test.
2. Mask augmentation doubles training rows. Clean-versus-mask differences are confounded by row count and effective fitting behavior. Corrective extension adds repeated-clean training with equal row count. It does not equalize information, exact optimizer work or runtime.
3. Budget compliance of the hard cap is mathematical by construction. The empirical contribution is the measured error/capacity tradeoff, not a discovery that a cap enforces capacity.
4. Closest literature is stronger than a generic rejection baseline. The publisher record for RiskGate-IDS identifies target-labeled calibration, BudgetBank allocation across micro-batches, and actual downstream detectors. Our source-only uncertainty policies are not a faithful reproduction or fair head-to-head comparison. Author and DOI verified through Crossref: Ha Thanh Dung, International Journal of Critical Infrastructure Protection 54 (2026), 100876, https://doi.org/10.1016/j.ijcip.2026.100876 . Full methods still not available in this review.
5. The same retained data are reused in this extension. Results are exploratory sensitivity evidence, not independent validation, new domains or an external review.

## Evidence

Protocol: sensitivity-v2.md, committed before extension execution. Code: src/sensitivity_v2.py. Seven boundary tests pass. Extension code is separate from the preserved primary evaluator. The primary metric bridge must pass before results are incorporated into the existing manuscript. Full routing and error accounting are recomputed from saved probabilities by src/check_sensitivity_v2.py.

## Remaining gate

This work may support a transparent benchmark/diagnostic manuscript. It does not yet support exclusive novelty, a new algorithm, operational SOC improvement, or superiority over RiskGate-IDS or MaskAug. Additional independent data, complete closest-method assessment, and venue suitability remain author-facing decisions. Do not automatically advance to a different project merely because the source draft is complete.
