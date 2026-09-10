# 08_covariates/ — ladder-height covariates

## Files

- `ladder_height_covariates.csv` — 40 rows: per-receptor `family_term_continuous`,
  `family_term_logit`, `delta_ref_npxxy`, `delta_ref_tilt`, `cognate_family`,
  `n_ga_families`, `deposition_count`, `saturation_frac_backbones`, `cluster_id`.
- `ladder_height_regressions.csv` — 80 rows: per (backbone × predictor ×
  outcome_scale) panel slope + cluster-boot CI, both `all` and `no_aa2ar`.

## SC-B claims supported

- **SC-B-11** (no ladder-height covariate has a slope excluding zero at 95 % CI
  on any of Δ_ref NPxxY / Δ_ref tilt / coupling promiscuity; deposition
  degenerate — every receptor has exactly 2 refs).

See `claim_answers.csv`.

## AA2AR sensitivity

Δ_ref tilt continuous slope drops +0.049 → −0.003 when AA2AR is excluded
(E-B-3). Other predictors stable. Report the AA2AR-excluded pair when Δ_ref
tilt is the panel-level headline (C-B-8).

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/`.
