# BB-6 — Panel F: Per-receptor ladder + ceiling-pinning flags

## Purpose

Show the per-receptor variation in the four-arm ladder and mark
ceiling-pinned cells (cognate rate ≥ 0.98) and floor-pinned cells
(apo rate ≤ 0.02). This is the load-bearing figure for the
ceiling-pinning caveat: three-quarters of the cells produce zero
family shift because they cannot go higher, one-quarter produce
large family shifts.

Load-bearing for **SC-B-2** (decomposition), **C-B-7** (ceiling
pinning), and Flag B-9.

## Data source

Primary CSV: `experiments/019_block_b_partner_selection/analysis/ladder_per_receptor.csv`.

- Rows: 160 (40 receptors × 4 backbones).
- Columns used: `receptor`, `backbone`, `apo_rate`, `decoy_rate`,
  `shuffled_rate`, `cognate_rate`, `apo_to_decoy`, `decoy_to_shuffled`,
  `shuffled_to_cognate`, `ceiling_pinned`, `floor_pinned`.

## Panels

**Panel F.i — parallel-coordinates plot of the 4 arms per (receptor,
backbone)**

- x-axis: arm ∈ {apo, decoy, shuffled, cognate}.
- y-axis: predicate rate 0 → 1.
- One line per (receptor × backbone) = 160 lines.
- Faded strokes for ceiling-pinned lines; bold strokes for the
  non-saturated subset (family term "lives here").
- Highlight AA2AR (see C-B-8 — non-saturated exemplar).

**Panel F.ii — bar chart of shuffled → cognate family term per
receptor (boltz only for illustration)**

- x-axis: 40 receptors, sorted by family term.
- y-axis: Δp shuffled → cognate.
- Colour by ceiling-pinning flag (grey if `cognate_rate ≥ 0.98`,
  emphasised otherwise).
- Value labels for the top 5 non-saturated: NPY2R (+0.68),
  NPY1R (+0.28), OX2R (+0.20), DRD3 (+0.20), ACM4 (+0.19).
- Note: AA2AR (+0.76 in Phase 6a, boltz; not from Phase 3f cite of
  +0.19 — see Flag B-11 for the discrepancy).

**Panel F.iii — saturation census (small side panel)**

Table or stacked bar:

| backbone | ceiling_pinned / 40 | floor_pinned / 40 |
|---|---:|---:|
| boltz | 29 | 31 |
| chai | 28 | 27 |
| of3 | 24 | 25 |
| protenix | 34 | 36 |

## Annotations

- Callout: "For 24–34 of 40 receptors, the cognate cell is at the
  ceiling (≥ 0.98) and the family term cannot read above zero on the
  probability scale. The logit-scale companion (BB-2) recovers the
  panel-consistent 17–21% family share across all four backbones."
- Note the four all-NaN NPxxY receptors (EDNRA, EDNRB, GRPR, HRH3)
  appear as always-zero lines under the two-instrument predicate on
  the probability panel — these are in the frame_40 view; frame_36
  excludes them (C-B-5).

## Exclusion flags to render as annotations

- Frame declared: default = frame_40 for the parallel-coordinates so
  the 4 excluded receptors are visible as the flat-zero lines and can
  be pointed at. Frame_36 sensitivity in the supplementary.

## Qualified by

C-B-5 (frame convention), C-B-7 (ceiling pinning), C-B-8 (AA2AR
anomaly), C-B-15 (Class A only), Flag B-1, Flag B-9, Flag B-11.
