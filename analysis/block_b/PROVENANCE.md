# Block B — provenance of the drop

Landed 2026-09-10 by the orchestrator session. Two bundles, both verified
against the SHA-256 values stated in the dispatch **before** extraction.

| bundle | SHA-256 | stated | files | landed at |
|---|---|---|---|---|
| `block_b_figure_data.zip` | `cadf3467c6b0841220a2221c15f9778a1f9fce6c1a547303337bdc8f6aa92d38` | matches | 104 files + 15 dirs = the "119" of the dispatch | `data/block_b/` |
| `block_b_structures.zip` | `dff8613502a6c1a75fca4889d7844748fbb951bbb854d8f766049539a19e431c` | matches | 20 (13 CIF + 7 text/CSV) | `data/block_b_structures/` |

The dispatch says the figure-data bundle is "119 files". The archive holds
**104 regular files and 15 directories**; `unzip -l` counts both, which is where
119 comes from. Nothing is missing. Recorded here so nobody re-derives it.

Both trees are `chmod a-w`. **Never edit the drop.** Defects are recorded in
`DISCREPANCY_REPORT.md`, never repaired in place.

## Upstream identifiers, copied from the drop's own README

- repo `paper_af3` @ `04531b8328ea4a71714a1b9ed7629736ec16f55a`
- freeze tag `block_b_freeze` — **PENDING** at the time of writing
- row source `rows.csv` SHA-256 `c65b93c2…d511d705`
- reference set of record `refs/reference_set.blockb_pinned.csv` SHA-256
  `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`
- single `scorer_git_sha = 04243c45…` across all 32,000 rows
  (`rows.pocket.csv` scored under later commit `fd87133`)
- bootstrap: 26 paralog clusters, 1,000 resamples, seed `20260909`

## The superseded r2 bundle

The dispatch instructs that a bundle with SHA-256 prefix `5129f07c…` is
superseded and must be deleted if present. **It is not present** on this
laptop — checked every zip under `~/Downloads` and the repo.

`~/Downloads/block_b_handover_2026_09_02.zip` (SHA `e8a1ddaa…`) is a *different*
older Block B artefact, from 2026-09-02. It is not the r2 bundle and it has not
been ingested. It is outside the repo and cannot reach a number here. Left in
place — deleting a file in Aditya's Downloads is his call, not mine.

## What is committed and what is not

Tabular data is committed, so every number in the paper traces to a shipped
file. Not committed: the two zips (kept at the repo root for re-extraction) and
`data/block_b_structures/**/*.cif`. Same rule as Block A.

## Two files are shipped twice, byte-identical

`11_bootstrap_draws/` is a convenience mirror, not a second source:

- `ladder_decomposition_bootstrap_draws.csv` — also at `05_decomposition/`, identical
- `donor_class_residuals_bootstrap_draws.csv` — also at `07_donor_residuals/`, identical

12.6 MB of the drop's 83 MB is this duplication. Harmless, but a checker that
counts rows across the tree will double-count the bootstrap draws.
