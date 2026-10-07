# IDS-TS handoff

Revision update: scientific review produced a separately frozen sensitivity-v2 extension with 54 fits, 1,080 prediction files and 4,320 metric rows. Seven tests and the independent routing recount pass; 1,440 overlapping primary rows match. Protocol freeze bfafb56, initial run implementation 5200498. After execution, CLI output-path options were added without changing scientific computations. Existing main.tex is updated in place. The user authorized the portable PDF refresh. It succeeded after starting the stopped Docker engine. The current nine-page PDF includes the sensitivity section; six tables and two figures were visually checked. Source/PDF hashes match the current build receipt. Native compilation still fails before parsing. Exact next action: scientific author review and the full-method/venue review described below.

Project ID: IDS-TS (local workstream ID, not P01-P23 or legacy L01). Repository: https://github.com/ezekielologunde/ids-telemetry-shift . Branch: main. Ownership: this workstream's checkout only, C:/Users/WT8/Projects/ids-telemetry-shift. No P01/P02 files or central portfolio paths were edited. No other agent was messaged. Editing session closes with the manuscript/artifact handoff; no shared-path claim remains active elsewhere.

Task: bounded failure-boundary IDS study. Primary protocol freeze: 2fccc96; evaluation implementation: 7a09fe2; pandas compatibility fix: 1113e54. Full current release is identified by Git history. Commands and exact dependency versions are in REPRODUCIBILITY.md and requirements-lock.txt. Python 3.12.14, pandas 3.0.6 for experiments; initial audit pandas 3.0.1.

Evidence: analysis/*-schema-audit.json; analysis/sample-audit.json; analysis/primary-v1-r2/{metrics.csv,prediction-hashes.json,verification.json,manifest.json}; paper/build/receipt.json. Raw archives and prediction NPZs remain local outside Git. Artifact hashes are in the release manifest.

Findings: 362/432 designed cross-domain cells exceeded a nominal 5% source-calibrated review fraction. Achieved review ranged from 0.85% to 100%. Capacity caps meet their count constraint but have high residual errors in this representation. This is not an operational failure probability or new detector. Representation ambiguity and deduplication materially limit interpretation.

Tests: six pass; separate prediction recount passes all 648 files and 6,480 metric rows. First primary run failed on a read-only pandas array and is retained. Restart complete. Native LaTeX compiler fails before parsing; separate portable compiler succeeds, and rendered PDF inspection passes. No HPC job was used or claimed.

Exact next action: scientific author review of paper/main.pdf and paper/REVIEW_STATUS.md, followed by full-method comparison against the closest literature and a venue suitability decision. Further validation needs a separately frozen protocol; do not silently retune this test set. No external journal submission has occurred.
