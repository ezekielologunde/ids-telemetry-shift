# Sensitivity extension v2, frozen before extension outcomes

7 October 2026. This extension follows inspection of primary-v1-r2 results. It is exploratory, not independent confirmation. Preserve the original protocol, code, outputs and release hashes. No selection of favorable cells or retuning is permitted.

Questions: Does the 5% capacity-mismatch finding persist when repeated occurrences of the same eligible patterns receive their natural sampled weights? Does mask augmentation differ from duplicating clean training rows with the same row count?

Keep all three samples, original chronological boundaries, source training/calibration unique-pattern partitions, feature exclusions, preprocessing, classifiers, seeds 17/29/43, and source-only clean calibration unchanged. Add a repeated-clean training variant by concatenating each training matrix and label vector with itself. Compare original clean, repeated-clean and masked-copy variants. This matches row count, not stochastic optimizer operations, information content or actual training time. No optimal augmentation claim.

Evaluate six ordered cross-domain pairs only, at nominal 5%, under clean, temporal, size, TCP and temporal+TCP outages. Omit random cell masking from this extension so changing row multiplicity does not change the mask assigned to a pattern.

Two test populations: (1) the exact original eligible unique-pattern rows, after source overlap removal; (2) every sampled test-period occurrence whose complete uncorrupted predictor pattern is in population (1). The second keeps the same eligible pattern set and time boundary but restores sampled multiplicity and all recorded occurrence labels, including conflicting labels. It is conditional sampled-flow weighting, not full traffic-volume or operational prevalence. Preserve original row ordering for ties. Hourly cap, random cap and frozen threshold use the original definitions. Save forced errors, realized review, unreviewed FN/FP and prediction evidence.

Report 54 fits, 1,080 prediction conditions and 4,320 metric rows if all fits succeed. Check source classes and test nonemptiness. Main descriptive endpoints are frozen-budget exceedance counts by population and variant, realized review ranges, and paired augmentation-minus-repeated-clean differences in forced and unreviewed error. Do not pool cells as independent observations. Use exact counts and per-pair summaries, no significance testing based on flow independence.

Reproduce original unique clean/masked metrics as an implementation bridge; any discrepancy beyond 1e-12 must be investigated before interpreting the new extension. Failure logs, hashes and conditions are retained. Update the existing manuscript in place only after accounting checks. This extension cannot settle literature novelty, independent label validity, prospective deployment or operational analyst costs.
