# Execution deviations and diagnostic findings

## Primary v1 interrupted

The first run completed UNSW-source fits then failed on ToN-IoT with pandas 3.0.6: `ValueError: assignment destination is read-only`. `to_numpy` can return read-only views. The fix requests an explicit copy before replacing nonfinite values. The protocol, samples, masks, model settings and scoring are unchanged. Keep `analysis/primary-v1/`, its console log and predictions; the complete restart uses `primary-v1-r2`. These are repeated executions, not independent experiments.

## Representation ambiguity audit, exploratory

While primary evaluation was running, an additional full-sample audit counted identical numeric predictor patterns carrying both labels. It did not alter primary training, features or splits. Under primary features, minimum empirical errors for any deterministic feature-only classifier on the full 100,000-flow samples are UNSW 0, ToN-IoT 5,186 and CIC 388. These are within-sample information bounds, not operational error guarantees. Extending the features with omitted service identifiers and ambiguous duration fields reduces those counts to 0, 44 and 15 respectively. This diagnostic mixes all sample periods, uses labels, and must not be used to select a primary representation or infer held-out performance.

The primary unique-pattern evaluation keeps the earliest observed label for a duplicate pattern. That choice changes the estimand and can discard conflicting-label occurrences. Results are conditional on this protocol and cannot establish traffic-volume accuracy. A future study should separate service-identifier dependence from duplicate handling with new held-out data. No first-ever failure-boundary claim is made.
