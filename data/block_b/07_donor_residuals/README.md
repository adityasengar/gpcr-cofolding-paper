# 07_donor_residuals/ — Phase 5 donor-class residuals + Phase 6b native-only power

## Files

- `donor_class_residuals.csv` — 32,000 rows: per-row residuals on tilt / NPxxY /
  delta_to_active against each receptor's active + inactive references.
- `donor_class_residuals_summary.csv` — 270 rows: cluster-boot summary per
  (backbone × donor_class × cognate_class × axis).
- `donor_class_residuals_bootstrap_draws.csv` — 180,000 draws (seed `20260909`,
  26 clusters, 1,000 draws).
- `donor_class_residuals.provenance.json` — bootstrap provenance (parent
  rows.csv SHA, cluster list, seed, draw counts).
- `phase5_power_analysis.csv` — 45 rows: native-only re-run per cell, both
  "all references" and "native only" median + CI.
- `donor_class_covariate_regression.csv` — 30 rows: absolute-residual
  regression against `alpha5_donor_class` controlled for cognate family.

## SC-B claims supported

- **SC-B-6** (Gs → Gi residual ≈ 0; Outcome A signed and firmed by native-only
  power).

See `claim_answers.csv`.

## Reading rule (C-B-10)

The Phase 5 §5.6 reference-bias caveat (37.5 % non-native panel-wide) does
NOT localise to the manuscript-load-bearing Gs → Gi cell — that cell is 83.3 %
native-anchored (20 of 24 receptors). The native-only re-run moves the
residual median from +0.024 to −0.062 Å; CI still spans zero, CI width
unchanged.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/`.
