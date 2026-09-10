# Reference survey — Bug #2 prevalence + candidate inventory
Generated: 2026-09-07 from `refs/reference_set.csv` (168 refs).
CSV: `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/reference_survey.csv` — one row per reference, all HETATM candidates per row.

## Headline
- 10/126 references (of those with at least one candidate) fire Bug #2 by centroid-distance criterion.
- 0 references have no local PDB (download failed).
- 42 references have zero HETATM candidates after buffer/AA filter.

## Bug #2 firing rate by role

| role | fires | total | pct |
|---|---:|---:|---:|
| active | 5 | 95 | 5.3% |
| inactive | 5 | 73 | 6.8% |

## Interpretation

`bug2_fires=YES` means the scorer's largest-HETATM pick != the candidate closest to the receptor Cα centroid. The centroid proxy is imperfect (assumes pocket ligand sits near geometric center of protein) but should be conservative — real disagreements will show large distance gaps.

Inspect the CSV — the `all_candidates` column has the full HETATM list for each reference. Any row where `picked_dist_to_receptor_centroid` > 25 Å but a candidate at < 15 Å exists is a Bug #2 event.
