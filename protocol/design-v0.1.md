# Candidate design v0.1

Recorded before any model fitting or outcome inspection, 7 October 2026. This is a design draft, not a preregistration or a completed experiment.

## Question and hypotheses

RQ: Under held-out network domains and structured telemetry loss, how do calibrated uncertainty policies trade residual classification errors against limited review capacity?

H1: Joint shift and telemetry loss can make a source-calibrated abstention threshold exceed its intended review budget or fail to concentrate errors in the review set.

H2: Training with feature-family masking improves error concentration under some missingness patterns relative to complete-data training. This is a hypothesis, not an expected positive result.

H3: A hard batch review cap prevents budget overflow but may increase unreviewed errors relative to unconstrained thresholding. The operational distinction is part of the evaluation, not a new selective-learning algorithm.

## Data gate

Prefer NF-UNSW-NB15-v3, NF-ToN-IoT-v3 and NF-CSE-CIC-IDS2018-v3 from the University of Queensland. V3 includes temporal information. Inspect actual headers, units, timestamp coverage, class counts, duplicates, grouping feasibility and file hashes before selecting splits. Do not mix NetFlow versions or raw CICFlowMeter and UNSW schemas by matching similar column names. Do not use the pooled NF-UQ collection together with constituent datasets as independent domains.

Exclude addresses, labels, attack names and absolute timestamps from predictors. Use timestamps/group identifiers for partitioning and audit only. Specify ports and protocol treatment explicitly after schema inspection. Exclude invalid labels, record every exclusion, and retain natural evaluation prevalence. No target-test labels for model or threshold selection.

## Proposed experiment

Three source domains, evaluated on each other domain. Within-source evaluation is a diagnostic. Chronological train/calibration/test boundaries require timestamp and capture checks; purge flows crossing boundaries and audit duplicate feature vectors. If capture structure prevents meaningful temporal splits, document the limitation and choose group holdout before outcomes rather than silently use random rows.

Baselines: logistic regression, tree ensemble and compact MLP; source-only preprocessing; complete-data versus feature-family mask augmentation. Compare forced decisions, random review, confidence review and mask-aware error scoring trained on source calibration data. Model tuning and error-scorer fitting need disjoint development partitions or cross-fitting.

Missingness: clean, random cell loss, entire predeclared feature-family loss and unseen combinations of families. Preserve a missingness indicator. Treat these as simulated exporter-field outages, not packet-loss simulation. Packet loss would require recomputing flows from packets. Do not imply missing fields faithfully model every sensor failure.

Budgets: 1%, 5%, 10% of evaluated flows. Compare frozen calibration thresholds to top-k review within explicitly defined batches. Top-k uses test scores without labels and is a batch/transductive policy, not a latency-free online guarantee. Tie-breaking deterministic. Report actual review fraction, error capture, unreviewed false negatives/false positives per total flows, class-conditional performance and risk-coverage summaries. Report undefined quantities explicitly when denominators vanish. Human review is not assumed perfect unless clearly labeled an oracle upper bound; include imperfect-review sensitivity.

Inference: compare paired policies on identical flows and masks. Repeated random seeds measure algorithm variability, not independent networks. Bootstrap time or capture blocks where supported; three domains cannot establish broad population generalization. No flow-level confidence intervals that imply independent traffic records without justification.

Freeze exact feature groups, split boundaries, seeds, model settings and evaluation code in a versioned protocol before primary evaluation. Keep pilot outcomes separate. Report compute time, memory and data volume. Local work covers acquisition/schema/tests; ASA-X covers justified repeated training after a scheduler/resource smoke test.

## Completion gate

Read closest papers in full where accessible, document comparison limits, execute the frozen design, preserve negative findings and failed runs, independently reproduce tables, create diagrams and a full ACM-style manuscript with limitations and Overleaf package. Repository publication is not journal submission.
