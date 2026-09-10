# 11_bootstrap_draws/ — consolidated bootstrap-draw CSVs

Two files (duplicated from `05_decomposition/` and `07_donor_residuals/`
respectively) collected here for the figure agent that wants a single source
for all draw-level data.

- `ladder_decomposition_bootstrap_draws.csv` — 30,000 draws.
  Columns: `draw_id, backbone, frame, contrast, scale, term_estimate`.
- `donor_class_residuals_bootstrap_draws.csv` — 180,000 draws.

## Common convention

- Bootstrap seed: `20260909`.
- Cluster count: 26 paralog clusters (see
  `09_references/paralogy_clusters.csv`).
- Draws per statistic: 1,000.
- Method: paralog-cluster resample with replacement, then per-draw statistic
  computed on all rows belonging to any of the drawn clusters.

## Recomputing intervals

CI convention: 95 % percentile interval on the per-draw statistic values —
`ci_lo = 2.5th percentile, ci_hi = 97.5th percentile`. Both bootstrap files
carry the raw draws (not the intervals) so downstream can also compute
bias-corrected or BCa intervals if needed.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/`.
