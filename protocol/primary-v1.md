# Frozen bounded evaluation, version 1

7 October 2026. User selected continuation of IDS and the failure-boundary study. No claim of a new masking algorithm, new selective classifier, or first-ever joint-shift study is intended. Original candidate design is retained as history; this document specifies the bounded primary evaluation. Primary outcomes have not been observed at this freeze.

## Scope and sampling

Three official NetFlow v3 domains. Select a uniform priority sample of 100,000 flows per domain using NumPy default_rng seed 20261007, one independent stream reset per archive. Select smallest priorities across the entire archive, without using labels. This is a reproducible bounded study, not a full-dataset training claim. Sort samples by start time then original row index. Split at time boundaries associated with 60% and 80% sample quantiles. Training flows must end before the first boundary; calibration flows must start at/after the first and end before the second; test flows must start at/after the second. Keep equal-timestamp records on the same side. Report purged counts. No tuning on test labels. Abort any source fit lacking both training classes or calibration classes. Uniform sampling retains prevalence in expectation, not exactly.

Remove repeated complete predictor vectors within each partition, and remove calibration/test predictor vectors present in earlier source partitions. Report natural-sample and post-deduplication prevalence. Across-domain tests also remove predictor vectors appearing in the source training/calibration sets. This intentionally evaluates unique feature patterns; flow-volume performance is a separate future extension, not implied here.

## Features and models

Use numeric flow fields excluding addresses, timestamps, Label, Attack, row identifiers, DNS_QUERY_ID and ambiguous DURATION_IN/DURATION_OUT. Remove raw ports and L7_PROTO from primary models to reduce environment-specific service identifiers. PROTOCOL remains numeric; this is a pragmatic baseline limitation. Keep source-trained median imputation and missing indicators for every feature. Signed log1p transformation and source-only standard scaling precede logistic regression. Random forest uses median-imputed values and mask indicators. No hyperparameter search.

Logistic regression: C=1, max_iter=500. Random forest: 100 trees, max_depth=16, min_samples_leaf=5, n_jobs=2. Seeds 17, 29, 43. Complete-data training versus one additional masked copy of each training row. For that copy choose uniformly among temporal, size, and TCP families. Identical source samples for paired methods. No class reweighting or resampling.

Feature families: temporal = names containing IAT or FLOW_DURATION; size = names containing BYTES, PKTS, PKT_LEN, FLOW_PKT or THROUGHPUT; TCP = names containing TCP. Families may not overlap; assert this. Remaining features remain observed. Test clean, temporal outage, size outage, TCP outage, temporal+TCP outage, and 10% independent random cell masking. An outage removes a family from every flow. This models absent exporter fields, not missing packets or physical sensor behavior. Clean source calibration is used throughout, expressly testing frozen calibration failure. Use missingness indicators, not replacement zeros interpreted as observed measurements.

## Policies and outcomes

Prediction threshold 0.5. Review score = 1 - abs(2p-1). Budgets 1%, 5%, 10%. Frozen policy threshold is the upper empirical clean-source-calibration quantile, using strict greater-than to keep tied scores from exceeding the calibration budget. Hard-cap policy reviews floor(b*n) highest-uncertainty flows within each UTC hour represented in the sample; ties broken by original row order. Random review uses the same per-hour cap and deterministic random priorities. Hourly batches are an offline, retrospective policy with waiting-time implications, not immediate online triage.

Report actual review fraction, reviewed errors, total errors, unreviewed FN and FP, accepted count/risk, full confusion counts, attack-family error counts, and hourly aggregates. Report forced-classifier results once per condition. Review is routing only; no human correction benefit is claimed. Oracle perfect-review estimates, if added, must be separately labeled sensitivity analyses. Null for undefined denominators. Primary comparison: frozen-threshold versus hard-cap uncertainty review at 5%; 1% and 10% sensitivity. Augmentation and model comparisons are secondary. Random review is a nonlearned reference.

## Validity and inference

Six ordered cross-domain pairs and three within-domain diagnostics. Pair identical flows and masks. Seeds are algorithm variability, not additional independent domains. Report per-pair results and ranges, not pooled flow-level significance claims. Hourly aggregates support later block sensitivity, but no independent-block or population-generalization claim follows automatically. Three synthetic/testbed domains cannot establish real SOC effectiveness. Report training runtime and input counts; large HPC execution requires a fresh resource check. This bounded primary study can run locally if measured resource use is modest.

No learned error scorer or MLP in this first bounded evaluation. These remain possible separately frozen extensions. This narrower scope supersedes their tentative inclusion in v0.1. Closest papers unavailable in full remain explicitly unresolved; no exact reproduction claim for RiskGate-IDS or MaskAug.
