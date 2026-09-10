# BB-1 — Panel A: The ladder — 4-arm × 4-backbone binary predicate

## Purpose

Show the two-instrument active-call fraction across the four arms
{apo, decoy, shuffled, cognate} for each of the four backbones, with
cluster-boot 95% CI on 26 paralog clusters. Include the panel-level
row. State the "both scales" observation: probability-scale panel
rate ladder plus the logit-scale companion.

Load-bearing for **SC-B-1** (ladder is monotonic and reproduces
exactly).

## Data source

Primary CSV: `experiments/019_block_b_partner_selection/analysis/ladder_four_scorings.csv`.

- Rows: 40 (2 frames × 5 backbone-strata (4 backbones + panel) × 4 arms).
- Columns used: `frame`, `backbone`, `arm`, `binary_predicate_mean`,
  `binary_predicate_ci_lo`, `binary_predicate_ci_hi`, `logit`,
  `per_receptor_midpoint_mean`, `delta_to_active_median`.

Filter to `frame == "reproduction_36"` (frame_36) — every panel-level
number in the manuscript uses this frame per Flag B-7.

Bootstrap draws (for CI): `ladder_decomposition_bootstrap_draws.csv`
carries panel-level draws; per-arm CIs on `binary_predicate_mean`
are already stored in `ladder_four_scorings.csv`.

## Panels

**Panel A.i — probability scale**

- x-axis: arm ∈ {apo, decoy, shuffled, cognate}, ordered left-to-right.
- y-axis: binary predicate mean (two-instrument), 0 → 1.
- hue/series: backbone ∈ {boltz, chai, of3, protenix, panel}. Panel
  drawn as a distinct series (bold or different marker).
- Error bars: cluster-boot 95% CI (`binary_predicate_ci_lo`,
  `binary_predicate_ci_hi`).
- Annotate dispatch cite (0.158 / 0.552 / 0.810 / 0.892) at panel row
  as reference dashes.

**Panel A.ii — logit scale (small inset or twin panel)**

- Same x-axis.
- y-axis: logit(binary_predicate_mean), with ε = 1/8000 continuity
  correction (documented in Phase 3 §3d and in the emitting script).
- Same backbone hues + panel.
- No error bars in the inset (space); refer reader to `ladder_decomposition.csv`
  for logit-scale CIs.

## Annotations

- Frame declared explicitly on the plot title or a note ("Class A
  n=36, frame_36").
- 4 receptors excluded from n=36 named in a subtext note
  (EDNRA / EDNRB / GRPR / HRH3; C-B-5).
- Panel value labels above each error bar on panel row: 0.158, 0.558,
  0.809, 0.891.

## Exclusion flags to render as annotations

- E-B-1 (frame_36) applied.
- No other exclusions in the primary panel; frame_40 sensitivity in a
  supplementary panel.

## Notes for rendering

- No colour scheme prescribed; use the paper's palette.
- Chai should be visually distinguishable as the per-backbone outlier
  (see C-B-2, Flag B-2) but not styled as an error.
- Sensitivity supplementary: same plot in frame_40 for the "here is
  what the naïve denominator gives" comparison (C-B-5).

## Qualified by

C-B-5 (frame convention), C-B-7 (ceiling pinning — visible on the
logit-scale inset as the exaggerated cognate rung), C-B-13 (cluster
map reconstructed), Flag B-1, Flag B-7.
