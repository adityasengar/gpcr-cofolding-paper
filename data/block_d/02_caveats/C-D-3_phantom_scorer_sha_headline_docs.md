# C-D-3 — Phantom scorer SHA `891041e858f3` cited in D2 + D3 headline docs

## Caveat

Two experiment-side headline documents cite a scorer SHA that does not
exist in git:

- `experiments/023_tier_d2_directed_inactive/analysis/tier_d2_full_headline_2026_09_07.md` line 6.
- `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md` line 6.
- Auto-memory `d3_full_confirmed_2026_09_08.md` also cited the same SHA.

The SHA `891041e858f3747b…` has no git ref, no orphan object, is not
in reflog. Verified per GATE-4. Row-level `scorer_git_sha` on all
42,180 D-tier rows (D1 14,000 + D2 2,370 + D3 25,810) is
`d9c646af5f89861c16062bf256de96a8389d9915` — this is the authoritative
scorer.

**Same shape as Block C's T7C headline drift** (documented in Block C
Q2). Documentation drift only; no data-integrity impact. Corrections
needed at dossier-authoring time:

- Replace `891041e858f3747b` → `d9c646af5f89861c16062bf256de96a8389d9915`
  in the D2 and D3 headline docs.
- Auto-memory `d3_full_confirmed_2026_09_08.md` was updated in this
  pass (§6.6 item 2).

The `891041e858f3` SHA does not correspond to any known scorer commit;
best hypothesis is that it was recalled from an intermediate scorer
branch that was rebased away before the D-tier rescore fired.

## References

- `gates/GATE_4_SCORER_DIFF.md` §Documentation drift.
- `BLOCK_D_STATE_CHECK.md` §Q2.
- Working-repo memory `d3_full_confirmed_2026_09_08.md` (updated 2026-09-10).
