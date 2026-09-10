# BB-2 — Panel B: Ladder decomposition on both scales

## Purpose

Decompose the apo → cognate ladder into three telescoping terms
(occupancy = apo→decoy, α5-CT sequence = decoy→shuffled, correct
family = shuffled→cognate) and report each term's share on BOTH the
probability scale and the logit scale. Show the ceiling-artefact
signature: the family term expands from 11.1% (probability) to 17.4%
(logit) while occupancy and α5-CT sequence stay stable in share.

Load-bearing for **SC-B-2** and Flag B-1.

## Data source

Primary CSV: `experiments/019_block_b_partner_selection/analysis/ladder_decomposition.csv`.

- Rows: 60 (5 backbones × 2 frames × 2 scales × 3 contrasts).
- Columns used: `frame`, `backbone`, `scale`, `contrast`, `estimate`,
  `share`, `ci_lo`, `ci_hi`.

Filter to `frame == "reproduction_36"`, panel row only for the main
panel; per-backbone rows for a companion sub-panel or supplementary.

Bootstrap draws: `ladder_decomposition_bootstrap_draws.csv` — 30,000
rows (1000 draws × 2 scales × 3 contrasts × 5 backbone-strata). Useful
if the figure needs violin/beeswarm rather than point + CI.

## Panels

**Panel B.i — stacked or side-by-side bar of shares, panel row**

- x-axis: two ticks — "Probability scale" and "Logit scale".
- y-axis: share of the ladder (0–100%).
- Bars: three stacked segments (occupancy / α5-CT sequence / correct
  family), or side-by-side triplet.
- Value labels: prob 54.6% / 34.3% / 11.1%; logit 50.5% / 32.1% / 17.4%.

**Panel B.ii — per-backbone family term (companion sub-panel)**

- x-axis: backbone ∈ {boltz, chai, of3, protenix}.
- y-axis (twin): probability family term (Δp) on one axis, logit
  family estimate on the other. Or two separate small multiples.
- Error bars: 95% CI on each estimate (cluster-boot).
- Annotate protenix probability CI crossing zero as a **ceiling
  artefact** callout (magnitude labels: prob 0.024 / 0.089 / 0.148 /
  0.066; logit 0.35–1.05 for protenix, panel 0.39–1.09).

## Annotations

- Occupancy 54.6% [0.328, 0.464] prob | 50.5% [1.52, 2.40] logit
- α5-CT sequence 34.3% [0.188, 0.321] | 32.1% [0.97, 1.49]
- Correct family 11.1% [0.047, 0.125] | 17.4% [0.39, 1.09]
- Panel A logit-vs-probability family-share ratio: **1.57×**
- Note that all four backbones agree on the logit-scale family share
  (17–21%) even where their probability shares differ 3–5×.

## Exclusion flags to render as annotations

- E-B-1 (frame_36) applied.
- E-B-4 (ceiling-pinned cells) is the reason the probability-scale
  family term is smaller — annotate on Panel B.ii.

## Qualified by

C-B-7 (ceiling pinning), C-B-13 (cluster map), W-B-1 (bare 11% figure
retired), Flag B-1, Flag B-9.
