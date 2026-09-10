# C-B-16 — Block A vs Block B OF3 effective-n asymmetry (constant-seed bug)

## Caveat

Block A ran with the OF3 seed bug in place (all rows silently used
constant `seed_2746317213`). The fix landed 2026-09-02 (auto-memory
`of3_seed_bug_fixed_2026_09_02.md`). Phase 0 verified **zero sentinel
hits** in Block B rows: OF3 seed-level replication for Block B = 5
distinct seeds × 10 samples = 50 rows per cell; for Block A = effectively
5 samples only (single seed used regardless of what was passed).

| Block | OF3 seed-level replication | Effective n per cell |
|---|---|---:|
| Block A | constant seed regardless of what was passed | 5 (samples only) |
| Block B | 5 distinct seeds × 10 samples | 50 |

## Why it matters

Any statement of the form:

- "the same pattern appears in both blocks",
- pooled A+B statistic that treats Block A and Block B OF3 rows as
  exchangeable,
- bootstrap over OF3 rows that pools A+B,

must account for the ~10× asymmetry. **Block A OF3 has ~10× less
seed-level dispersion than Block B OF3 by construction.**

All prior OF3 seed-dispersion claims on Block A are void (per auto-memory
`of3_seed_bug_fixed_2026_09_02.md`).

## Affects

- Any cross-block pooling that includes OF3.
- Cross-block sentence framing ("Block A observed X; Block B replicates X").
- Not the Block-B-internal claims (Block B OF3 is post-fix, effective n=50
  per cell).

## Manuscript sentence

> Block A OF3 rows were produced under a constant internal seed
> (`seed_2746317213`); the fix landed 2026-09-02 before Block B was
> dispatched. Block B verified zero sentinel-seed hits across all 8,000
> OF3 rows (5 distinct seeds × 10 samples per cell). Cross-block
> pooling of OF3 rows must account for the ~10× effective-n asymmetry
> in seed-level replication.

## Related

- MANUSCRIPT_FLAGS.md Flag B-25.
- Phase 0 §0e (seed distinctness + sentinel sweep).
- Phase 0 addendum §"OF3 effective-n asymmetry (standing note)".
- Auto-memory `of3_seed_bug_fixed_2026_09_02.md`.
- Block A caveat C-5 (pre-freeze `no-git` subtrees) — related but distinct.
