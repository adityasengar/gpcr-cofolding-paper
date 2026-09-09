# C-5 — Pre-freeze subtrees carry `scorer_git_sha=no-git`

## Caveat

Eight subtrees in the campaign carry `scorer_git_sha=no-git` at row
level. These are pre-scorer-freeze rescores — the venv was pip-installed
without `setup.py`'s `build_py` step running (the CLAUDE.md-named
regression detector). Some of them are cited by PREREG amendments as
motivating evidence for the frozen scorer's decisions.

**List**:

| Subtree | Rows | Purpose | Manuscript citation |
|---|---:|---|---|
| `smoke_tests/` | 45 | initial validation | none |
| `diversity_pilot/` | 100 | initial validation | none |
| `chai_msa_pilot_{aa2ar,adrb2,drd2}_5_5/` | 3 × 25 | Chai MSA discipline | PREREG §11d |
| `chai_msa_cache_verify_drd2_5_5/` | 25 | Chai cache verification | PREREG §11d |
| `timing_boltz_50_vs_200_ab_2026_09_01/` | 30 | Boltz sampling_steps | PREREG §11a |
| `018_block_a_switch_test_of3_rerun_2026_09_02/` | 2,375 | OF3 seed fix rerun | W-6, W-7 |

## Affects

- Only pre-freeze motivational subtrees. Not headline claims.
- PREREG §11a (Boltz sampling_steps=200) and §11d (Chai MSA correction)
  reference `timing_boltz_50_vs_200` and `chai_msa_pilots` as motivating
  evidence. Those references stand; the pre-freeze marker only affects
  the rows in those subtrees, not the PREREG lock derived from them.

## Evidence

- `_internal/RECON/SUSPECTED_DEFECTS.md::D-34`
- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md` §Phase 1g, §Phase 2d

## Manuscript sentence

> Six pre-freeze subtrees (smoke_tests, diversity_pilot, chai_msa
> pilots, chai_msa_cache_verify, timing_boltz_50_vs_200) carry
> pre-scorer-freeze provenance markers. These subtrees are motivational
> evidence for pre-registered decisions (PREREG §11a and §11d) and are
> not part of the block-level headline corpora.
