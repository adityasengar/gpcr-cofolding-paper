# W-B-2 — Per-receptor midpoint ladder 0.130 / 0.500 / 0.801 / 0.887

## Claim as previously stated

Prior Block B campaign summaries cite a "per-receptor midpoint ladder"
of **0.130 / 0.500 / 0.801 / 0.887** on {apo, decoy, shuffled, cognate}
as a companion to the panel-binary-predicate ladder 0.158 / 0.552 /
0.810 / 0.892. The dispatch plan named these two ladders as a paired
report.

## Retraction

**Withdrawn as a reproducible figure.** Under Block B's uniform (5, 10)
× 40 design, per-receptor midpoint mean equals panel mean by arithmetic
identity — cells are uniform-sized, so weighting per-receptor first
gives the same result as pooling. The Phase 3 computation on today's
rows.csv gives 0.158 / 0.558 / 0.809 / 0.891 (matching panel-mean to
6 decimal places).

Phase 6 tried 7 candidate n=28 subsets by Euclidean distance to the
0.130 / 0.500 / 0.801 / 0.887 target:

| subset | n | apo | decoy | shuffled | cognate | Euclidean dist |
|---|---:|---:|---:|---:|---:|---:|
| native_active_only_no_nan_np | 22 | 0.104 | 0.477 | 0.788 | 0.892 | 0.038 |
| Gi_cognate_only | 24 | 0.104 | 0.478 | 0.766 | 0.861 | 0.056 |
| exclude_nan_np_and_sealed | 30 | 0.163 | 0.553 | 0.806 | 0.884 | 0.063 |
| exclude_nan_np_only_36 | 36 | 0.158 | 0.558 | 0.809 | 0.891 | 0.065 |
| exclude_nan_np_and_chim_and_agonist_only | 32 | 0.156 | 0.559 | 0.826 | 0.913 | 0.074 |
| **exclude_nan_np_and_heldout_28** | **28** | 0.165 | 0.579 | 0.831 | 0.910 | 0.094 |
| unsaturated_only | 16 | 0.132 | 0.608 | 0.815 | 0.878 | 0.110 |

**None of the tried subsets reproduces the target within 0.02 per arm.**
The four numbers likely come from either (a) a different corpus (Block
A rather than Block B — but Block A has no shuffled arm), (b) a different
weighting scheme not documented on disk, or (c) a per-receptor median
rather than mean.

## What supersedes it

Cite the reproduction_36 ladder (0.158 / 0.558 / 0.809 / 0.891) as the
per-receptor midpoint ladder on Block B. Under uniform (5, 10) × 40
design this IS the per-receptor midpoint. The manuscript sentence at
Flag B-10 records the discrepancy as documentation ambiguity.

## What the manuscript should say instead

*Nothing new to say; use the panel-mean ladder as the per-receptor
midpoint ladder.* If the manuscript needs a per-receptor-first computation
for narrative reasons:

> Under Block B's uniform (5 seeds × 10 samples) × 40-receptor design,
> per-receptor midpoint mean is arithmetically identical to panel mean
> (0.158 / 0.558 / 0.809 / 0.891 on the two-instrument predicate on
> frame_36). The distinct number cited in earlier dispatch drafts
> (0.130 / 0.500 / 0.801 / 0.887) does not reproduce on any tried n=28
> subset and lacks a documented source.

## Evidence

- `docs/BLOCK_B_DOSSIER_PHASE_3_LADDER.md §3d` (per-receptor midpoint = panel mean).
- `docs/BLOCK_B_DOSSIER_PHASE_6_COVARIATES_AND_REFERENCES.md §Smaller reconciliations → Midpoint ladder on 28-receptor subsets`.
- Source CSV: `midpoint_ladder_28.csv` (13 rows).

## Related

- MANUSCRIPT_FLAGS.md Flag B-10.
