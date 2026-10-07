# Data feasibility findings

7 October 2026. These are data-quality observations, not model evaluation results.

The official NF-UNSW-NB15-v3 ZIP passed every supplied payload SHA-1 check. Our additional archive SHA-256 is recorded in `analysis/unsw-schema-audit.json`. The CSV contains 2,365,424 flows: 2,237,731 benign and 127,693 attack. The catalogue states 127,639 attacks, a 54-record discrepancy; the downloaded labels are the analysis source of truth. This does not establish incorrect row labels.

Capture days are 22 January 2015 (1,078,112 benign, 17,462 attack), 23 January 2015 (39,778 benign, zero attack), and 18 February 2015 (1,119,841 benign, 110,231 attack). A naive three-day train/calibration/test partition would calibrate on a benign-only day. Temporal partitions need a finer-resolution audit before being frozen. No reversed or missing start/end intervals were found by the initial audit.

The supplied feature dictionary contains apparent copy-edit errors: several destination-to-source IAT descriptions repeat minimum IAT despite distinct MAX/AVG/STDDEV headers, and both DURATION_IN and DURATION_OUT descriptions say client-to-server. Do not silently assert semantic equivalence based on these descriptions. Verify against extractor documentation and the dataset paper or omit ambiguous features from the primary analysis.

Three official ZIP archives downloaded successfully to the local Downloads directory; raw archives are excluded from Git. ToN-IoT full audit is running. CICIDS2018 audit is pending. Landing pages for all three identify open access with a commercial-use restriction. Public access does not waive those restrictions.

The scientific contribution remains under discussion because current literature overlaps both the original budgeted detection idea and feature-mask training. No model has been fit and no test outcomes inspected.
