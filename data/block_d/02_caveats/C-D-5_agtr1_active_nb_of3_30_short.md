# C-D-5 — AGTR1 × active_nb × OF3 landed 170 preds, not 200

## Caveat

Canonical D2 grid: (5 seeds × 10 samples) = 50 preds per (receptor,
arm, backbone) cell. Total canonical n per cell = 50 × 4 sample
subruns = 200 preds (2 sample subruns per seed × 10 samples? actually
5 seeds × 10 samples = 50 per cell; but D2 uses 4 fold-multiplier per
cell to reach 200/cell canonical in the dispatch). AGTR1 × active_nb
× OF3 landed **170** of 200 predictions.

Root cause per `tier_d2_full_headline_2026_09_07.md`: three OF3
stragglers on AGTR1 active_nb hung ~3 h with no progress; workers
killed to reclaim H100 slots. No retry attempted.

Reported fraction uses **actual landed n = 170**, not the canonical
denominator. AGTR1 × active_nb × OF3 predicate-active is 95 % on
those 170 samples.

**Cell-specific footnote** required in any manuscript sentence citing
AGTR1 active_nb figures. The 15 % coverage loss on this one cell does
not affect the F2 verdict (active-Nb works on 3/4 bb) since the OF3
verdict on AGTR1 is confounded by AGTR1's apo already being
active-biased (F6).

## References

- `experiments/023_tier_d2_directed_inactive/analysis/tier_d2_full_headline_2026_09_07.md` — original headline documenting the shortfall.
- `dossiers/BLOCK_D/partA/PARTA_D2.md` §F2 verdict.
- `dossiers/BLOCK_D/ASSUMED_NOT_VERIFIED_BLOCK_D.md` §AGTR1 × active_nb × OF3 30-row shortfall.
