# Intrusion detection under telemetry loss and domain shift

Author: Ezekiel Ologunde, Independent Researcher. Email: ologunde@bu.edu.

Status: bounded experiment completed, 7 October 2026; manuscript/artifact review in progress. No established exclusive novelty or journal submission. Original work remains unlicensed. Third-party dataset and paper terms remain in force.

The research asks whether uncertainty-based triage remains useful under simultaneous domain transfer and structured loss of flow telemetry. The initial broad proposal overlaps with RiskGate-IDS; budgeted cross-domain detection alone is not a new contribution. The candidate contribution is a controlled evaluation of joint shift, feature-family outages, and the distinction between a calibration-time review budget and a deployment-time hard budget.

See `protocol/design-v0.1.md` and `protocol/literature-audit.md`. Data must stay outside Git. Public downloads, exact hashes, schema audits, split rules, and execution receipts will support reproduction. Large training is gated on data and literature feasibility and a measured resource pilot.

## Measured scope

- Three official archives audited, 50,001,213 flows total. Models use 100,000 sampled flows per domain before chronological splitting and pattern deduplication.
- 36 fits, 648 prediction conditions, 6,480 metric rows; six boundary tests and a separate prediction recount pass.
- Frozen thresholds exceed nominal 5% review in 362/432 cross-domain cells. Actual review ranges from 0.85% to 100%.
- Hourly caps meet capacity but leave high residual errors. Uncertainty routing has no consistent aggregate advantage over random routing.
- Duplicate handling, conflicting labels and omitted service information materially constrain interpretation. No operational SOC benefit or new algorithm is claimed.

See paper/main.tex, protocol/primary-v1.md, protocol/deviations.md and REPRODUCIBILITY.md. Complete results: analysis/primary-v1-r2. The original primary-v1 directory is a retained failed partial execution.
