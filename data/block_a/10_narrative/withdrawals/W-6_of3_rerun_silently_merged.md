# W-6 — "OF3 rerun 2,375 rows silently merged into Block A with `no-git`"

## Claim as previously stated

The paper's release-readiness recon (see `_internal/RECON/SUSPECTED_DEFECTS.md::D-03`
and `BLOCKERS.md::DEC-05`) framed the A_of3_rerun cohort as "2,375 rows
carrying `scorer_git_sha=no-git` on 100% of rows, silently merged into
the primary Block A analysis by `scripts/merge_of3_rerun_rows.py`".

## Retraction

**Withdrawn.** The merge script has NOT been executed to disk. There is
no `rows.merged.csv`. The primary Block A rows.csv points at the same
CIFs as the OF3 rerun tree (100% `input_path` overlap on 2,375 CIFs),
but carries the properly-stamped `scorer_git_sha=04243c45…` on those
rows. The rerun `rows.csv` is a separate rescore under a `setup.py`-
unstamped venv (the CLAUDE.md-named `no-git` regression detector); it is
a stale intermediate, not merged into the corpus.

**Running the merge script today would REGRESS the corpus** — replace
2,375 properly-stamped rows with `no-git` duplicates that carry
bit-identical scoring numbers.

## Evidence

- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md` §Phase 1g + §Phase 2c
- `scripts/merge_of3_rerun_rows.py` (the driver; dry-run analysis at Phase 2c)
- On-disk state: `experiments/018_block_a_switch_test/analysis/rows.csv` carries `04243c45` on 100% of 9,490 rows, 0 `no-git`

## Recommendation (adjudication-adjacent, not adjudicated here)

Retire `scripts/merge_of3_rerun_rows.py` or gate it behind a "this will
regress provenance" prompt. Fix the two doc references (see W-7).
