# W-7 — "Merged via `merge_of3_rerun_rows.py`" claim in two docs

## Claim as previously stated

Two docs in the parent repo state that the OF3 rerun was merged into the
primary corpus via `scripts/merge_of3_rerun_rows.py`:

- `docs/campaign_completion_report.md` (~line 82): "Merged into the primary
  `rows.csv` via `scripts/merge_of3_rerun_rows.py`."
- `docs/framework/capability_evidence.md`: "Merged via
  `scripts/merge_of3_rerun_rows.py`."

## Retraction

**Withdrawn.** Neither claim reflects on-disk state (see W-6). Both docs
are preserved in `_internal/superseded_docs/` for archaeological
reference. They are not part of the release archive's `analysis/`
directory. **Do not cite them.** The dossier is the analysis record; see
release/README.md precedence rule.

## Evidence

- `_internal/superseded_docs/campaign_completion_report.md`
- `_internal/superseded_docs/capability_evidence.md`
- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md` §Phase 2c (dry-run showing the merge would REGRESS)

## Recommendation

Either delete the two doc claims from the parent repo (with a git note
pointing at this file), or amend them to state "the OF3 rerun was NOT
merged; the primary rows.csv already carries the properly-stamped
rescore of the OF3-seed-fixed CIFs". The dossier's precedence over the
docs is stated in release/README.md.
