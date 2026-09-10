# 10_exclusions/ — exclusion sets: definitions, membership, counts

## Files

- `exclusion_definitions.csv` — 5 rows (four E-B flags + `excl_any`), with
  members, receptor counts, rationale, and claim-sheet reference.
- `exclusion_membership.csv` — 40 rows, one per receptor, with boolean
  membership in each set + reason string.
- `exclusion_counts.csv` — 5 rows, row-count effect if each flag is applied
  singly.

## Load-bearing hygiene rule

Exclusion flags are **present on every row of `01_rows/rows_tidy.csv` and
NEVER pre-applied to any downstream table.** The figure agent applies each
set at panel-generation time and shows before / after where warranted.

## The four sets

- **E-B-1** (`EDNRA, EDNRB, GRPR, HRH3` — 4 receptors, 3,200 rows) — all-NaN
  NPxxY-OH under the current axis definition (7.53 = L not Y). Frame_36 =
  whole panel − E-B-1.
- **E-B-2** (`OPRD, CNR1` — 2 receptors, 1,600 rows) — agonist-only active
  reference; cognate arm cannot reach the two-instrument ceiling by
  construction.
- **E-B-3** (`AA2AR` — 1 receptor, 800 rows) — recurrent anomaly; excluded
  from pooled inference where AA2AR alone drives a slope (C-B-8).
- **E-B-4** (15 receptors, 12,000 rows) — non-native-anchored active reference
  (chimera / mini-G / nanobody / scFv / agonist-only / DVL-DEP). Applied on
  Phase 6b native-only re-run to answer Phase 5's reference-bias caveat
  (C-B-10).

## Overlap

- 5 receptors appear in two sets (AA2AR ∈ E-B-3 ∩ E-B-4; CNR1 / OPRD ∈ E-B-2 ∩
  E-B-4; EDNRA ∈ E-B-1 ∩ E-B-4; EDNRB / GRPR / HRH3 ∈ E-B-1 only).
- `excl_any` covers 22 distinct receptors → 14,400 rows.
