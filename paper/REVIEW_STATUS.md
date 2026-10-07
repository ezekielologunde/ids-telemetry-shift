# Manuscript status

Revision update, 7 October 2026: the existing main.tex now includes the checked post-primary sensitivity extension and a corrected RiskGate-IDS reference. Native compilation again fails before parsing. Until a separately authorized PDF refresh succeeds, main.pdf and paper/build/receipt.json refer to the earlier eight-page version at commit b369956, not the revised source. The newer source contains six tables. Do not distribute the earlier PDF as this revision.

Eight-page ACM-class manuscript, five tables, two figures. Author: Ezekiel Ologunde, Independent Researcher, ologunde@bu.edu, no corresponding-author designation. Complete bounded study draft for scientific review, not a claim of journal acceptance or submission readiness.

## Verified

- Official archive integrity, dataset counts and sample hashes recorded.
- Protocol and code frozen before primary outcomes; pandas compatibility restart disclosed and partial run preserved.
- Six boundary tests pass. Second implementation verifies 648 saved prediction hashes and 6,480 metric rows within its stated scope.
- Portable offline compiler succeeds. PDF pages rendered and inspected, including full-size result tables and chart. No overfull-box or undefined-reference warnings in the final build. Fontconfig/default font warnings remain despite successful rendering.
- Native editor compilation fails before source diagnostics with its platform-directory error. It is not claimed to work.

## Material scientific limits before submission

- Resolve access to the closest papers' full methods and assess whether this bounded contribution suits a specific venue. No first-ever or state-of-the-art claim is supported.
- Unique-pattern deduplication changes the estimand and discards some conflicting-label occurrences. Do not present this as traffic-volume effectiveness.
- The original augmentation comparison had no repeated-clean control. The exploratory extension adds an equal-row control and finds mixed results; it does not match every optimization effect or establish a causal masking benefit.
- Three historical testbed domains, retrospective hourly batches and no human review experiment cannot establish SOC effectiveness.
- Independent researcher validation, additional held-out domains and operational calibration remain unperformed.

The author must review these limits and the selected venue's requirements before any journal submission. No venue, submission identifier, DOI or acceptance is invented. Original work remains unlicensed, and dataset restrictions are preserved through acquisition references rather than raw-data redistribution.
