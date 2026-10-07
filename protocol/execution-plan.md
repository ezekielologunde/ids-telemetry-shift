# Execution plan and resource gates

Completion update, 7 October 2026: all three archive audits and the frozen bounded experiment are complete. The separate recount verified 648 prediction files and 6,480 metric rows. An eight-page ACM-class manuscript with five tables and two figures compiled using the portable fallback; the native compiler remains unavailable. The plan below is retained as history. The scope was narrowed before fitting to two conventional CPU models; no MLP or HPC execution was performed. Remaining publication gates are scientific author review, closest-method full-text comparison, venue choice and submission approval.

## Completed

- Repository and candidate hypotheses created before model fitting.
- Closest literature screening identifies direct overlap with RiskGate-IDS and MaskAug.
- Three official NetFlow v3 ZIPs downloaded through UQ's public download controls.
- UNSW archive payload integrity, full row counts and day/label distribution checked.
- Audit tests check known counts, reversed intervals and rejection of altered payloads.

## Next, in dependency order

1. Complete ToN-IoT and CICIDS2018 checksum/schema/date audits; preserve archive and payload hashes.
2. Resolve the contribution choice: failure-boundary evaluation or new method development. Both require closest-paper comparison. A new method cannot be created by simply renaming standard masking, confidence rejection or top-k routing.
3. Inspect fine-grained time/class coverage and duplicate groups. Freeze training, calibration, tuning and test boundaries before examining predictive outcomes.
4. Resolve ambiguous feature definitions against extractor documentation. Freeze feature-family masks. Exclude identifiers and ambiguous variables from primary models.
5. Run a small development-only workload, record wall time and peak memory, then size the primary experiment. Pin package versions and record Python/platform details.
6. Verify current ASA-X account limits, modules, storage and an allocated GPU. Use CPU jobs for trees and streaming preprocessing, GPU jobs for a justified neural workload. Never train on a login node. Existing historical queue limits do not prove current GPU availability.
7. Commit the primary protocol and executable configuration before evaluation. Keep pilot results separate. No test-driven redesign without labeling subsequent work exploratory.
8. Execute paired conditions, preserve errors and exclusions, independently reconstruct metrics, and package manuscript, diagrams, tables, code and acquisition instructions.

## Compute rationale

HPC value comes from six ordered source-to-target pairs, repeated seeds, training ablations, missingness conditions and blockwise evaluation. Request resources based on the pilot. Trees generally use CPUs; a small MLP may not benefit from multiple GPUs. Do not inflate networks or repeat experiments merely to consume allocation. Three benchmark domains remain three domains regardless of the number of flows or seeds.

## Local files and reproduction

Download from the official landing pages linked in `data/sources.json`. The site's Download file control produces a BagIt ZIP. Keep ZIPs outside the repository. Audit with Python 3.11 or newer and pandas:

```text
python src/audit_archive.py PATH_TO_OFFICIAL_ZIP --output analysis/DATASET-schema-audit.json
python -m unittest discover -s tests -v
```

The initial audit ran with the bundled Python environment; the independent project virtual environment is for future work. Its locked packages are recorded separately. The audit streams data and does not require extracting multiple-gigabyte CSVs. It verifies the dataset's supplied SHA-1 payload manifest and independently records archive SHA-256. SHA-1 here checks the source's published payload receipt, not authenticity against an adversarial substitution.

Raw data and third-party PDFs are not uploaded to GitHub. Publication of original protocol, aggregate audit counts and code does not imply unrestricted rights to redistribute the underlying datasets. Original work remains unlicensed.
