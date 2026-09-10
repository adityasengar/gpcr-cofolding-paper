# 04_ladder/ — the four-scoring ladder

## Files

- `ladder_four_scorings.csv` — 40 rows: 2 frames × 5 backbone strata × 4 arms.
  The headline table.
- `ladder_continuous_distributions.csv` — 96 rows: (arm × backbone × axis)
  medians + percentiles + IQR on NPxxY-OH, TM6 tilt, `delta_to_active`,
  `delta_to_inactive`, `rmsd_to_active_ref`, `rmsd_to_inactive_ref`.
- `ladder_threshold_proximity.csv` — 32 rows: mass fraction inside ±0.5 Å of
  each axis threshold, per (arm × backbone).
- `ladder_adjacent_pair_separation.csv` — 24 rows: adjacent-pair median shift
  vs pooled IQR.
- `ladder_per_receptor.csv` — 160 rows: per (receptor × backbone) rates on
  every arm + `ceiling_pinned` / `floor_pinned` flags.
- `midpoint_ladder_28.csv` — 13 rows: enumerated 28-receptor subsets attempted
  for the retired dispatch-cite reproduction (W-B-2). NO subset reproduces
  0.130 / 0.500 / 0.801 / 0.887 within 0.02.

## SC-B claims supported

- **SC-B-1** (ladder monotonic + reproduces on frame_36).

See `claim_answers.csv`.

## Frame filter for headline figures

For BB-1 use `frame == "reproduction_36"` (frame_36). For sensitivity or
comparison, `frame == "all_40"` is present in the same file.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/`.
