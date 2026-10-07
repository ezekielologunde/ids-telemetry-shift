# Reproduction

Revision note: primary and sensitivity outputs are separate. The current source includes sensitivity-v2; the existing PDF/build receipt remain the earlier revision until a new authorized build succeeds. Native editor compilation remains blocked before source parsing.

Python 3.12.14 on Windows. requirements-lock.txt records the project environment. Initial archive audits used bundled pandas 3.0.1; sampling, fitting and analysis used project pandas 3.0.6. No paid APIs, live targets or HPC allocation were used. CPU fitting was limited to two threads. Fit times exclude preparation and inference.

Download official ZIPs using data/sources.json. Keep raw archives outside Git and inspect their commercial-use restrictions. Compare archive SHA-256 and payload SHA-1 values against analysis/*-schema-audit.json. Sample hashes are in analysis/sample-audit.json. Load only locally generated samples, never arbitrary untrusted pickle files.

Create and activate an isolated environment, then execute:

```text
python -m pip install -r requirements-lock.txt
python -m unittest discover -s tests -v
python src/audit_archive.py PATH_TO_UNSW_ZIP --output LOCAL_UNSW_AUDIT.json
python src/audit_archive.py PATH_TO_TON_ZIP --output LOCAL_TON_AUDIT.json
python src/audit_archive.py PATH_TO_CIC_ZIP --output LOCAL_CIC_AUDIT.json
python src/prepare_sample.py PATH_TO_UNSW_ZIP data/processed/unsw.pkl
python src/prepare_sample.py PATH_TO_TON_ZIP data/processed/ton.pkl
python src/prepare_sample.py PATH_TO_CIC_ZIP data/processed/cic.pkl
python src/evaluate.py --data-dir data/processed --output analysis/replication-v1
python src/verify_predictions.py analysis/replication-v1 data/processed/predictions-replication-v1
python src/summarize.py analysis/replication-v1
```

Use a new output directory; existing runs are not overwritten. Expect 36 fits, 648 prediction files and 6,480 metric rows. Compare metrics and split receipts to primary-v1-r2, not runtime or pickle bytes across arbitrary dependency versions. Preserve failures and warnings. The representation audit is exploratory and uses all sample labels. It is not a label-free preprocessing operation.

The manuscript generator reads the checked primary results. main.tex and conditions.pdf are the Overleaf inputs. Native compiler failed before source diagnostics: Unable to find standard directories for platform. The separate offline Docker build uses verified portable Tectonic 0.17.0 and an existing cached bundle. No local TeX installation is needed. Actual build status and hashes are in paper/build/receipt.json.

```text
python src/generate_manuscript.py
python src/build_manuscript.py --compiler-dir PATH_TO_VERIFIED_TECTONIC_AND_CACHE
```

Official compiler archive: https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.17.0/tectonic-0.17.0-x86_64-unknown-linux-musl.tar.gz . Archive SHA-256: 8533d07f9ccbd7a65824b9e0459041bca34af1eb33daba48f59215593753a3b7. Binary SHA-256: a98aa59ad5c1df39a6c9e56cbfc5088f2b11d6c179c0130b97998e4bd46a46da.

The second prediction implementation verifies hashes, forced errors, conservation identities, frozen routing and capacity counts. It is not an independent researcher review and does not authenticate labels, sampling or model fitting. Original work is unlicensed; third-party terms remain in force.

## Post-primary sensitivity extension

With the same local samples, use a new output directory:

```text
python src/sensitivity_v2.py --output analysis/sensitivity-replication
python src/check_sensitivity_v2.py --output analysis/sensitivity-replication
python src/summarize_sensitivity_v2.py --output analysis/sensitivity-replication
```

The runner refuses to overwrite analysis/sensitivity-v2 or its local prediction directory. Expected: 54 fits, 1,080 prediction files, 4,320 rows, and an exact/tolerance-bounded bridge for 1,440 original metric rows. The source-update script is a one-time patch and intentionally refuses to add a second copy of the manuscript section. Rerun summary/verification independently rather than rerun that patch. The primary script and result bytes remain unchanged.

## Verified manuscript refresh

On 7 October 2026, the authorized offline portable build produced the current nine-page sensitivity-v2 PDF. The initial attempt failed because Docker was stopped; after starting Docker, the build succeeded. All pages were rendered and inspected. Source and PDF hashes are recorded in paper/build/receipt.json and paper/revision-status.json. The native editor platform-directory failure remains unresolved. The Overleaf package contains the matching source, figure and review-status note.
