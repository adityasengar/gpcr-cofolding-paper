# W-D-10 — Scorer SHA `891041e858f3747b…` as authoritative

## Claim as previously stated

Two experiment-side headline documents cite scorer SHA
`891041e858f3747b…` in prose:

- `experiments/023_tier_d2_directed_inactive/analysis/tier_d2_full_headline_2026_09_07.md` line 6.
- `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md` line 6.

Auto-memory `d3_full_confirmed_2026_09_08.md` cited the same.

## Retraction

**Withdrawn as authoritative.** The SHA `891041e858f3747b…` does not
exist in git — verified per GATE-4:

- No git ref points to it.
- No orphan object exists at that hash.
- Not in git reflog.

**Phantom SHA.** Best hypothesis: recalled from an intermediate scorer
branch that was rebased away before the D-tier rescore fired.

**Authoritative scorer for all three D-tier corpora**:
`d9c646af5f89861c16062bf256de96a8389d9915` — verified as the uniform
row-level `scorer_git_sha` on all 42,180 D-tier rows (D1 14,000 + D2
2,370 + D3 25,810).

Same shape as Block C's T7C headline drift (documented as Block C's
Q2 δ). Documentation drift only; no data-integrity impact.

## Basis

- `dossiers/BLOCK_D/gates/GATE_4_SCORER_DIFF.md` — git-ancestry + reflog check.
- `dossiers/BLOCK_D/BLOCK_D_STATE_CHECK.md` §Q2 (uniform `d9c646af` on all D-tier rows).
- Auto-memory `d3_full_confirmed_2026_09_08.md` (updated 2026-09-10).

## What the manuscript should say instead

Cite scorer `d9c646af5f89861c16062bf256de96a8389d9915` for D1, D2, and
D3 corpora. Do NOT cite `891041e858f3` — that SHA does not exist in
git and cannot be recovered.
