# C-D-6 — D3 Chai + OF3 short 190 preds (of 26,000 dispatched)

## Caveat

D3 canonical grid: 26 receptors × 4 backbones × 5 depths × 5 seeds ×
10 samples = 26,000 predictions dispatched.

**Landed**: 25,810 preds (99.27 %). 190 short across backbones:

- Boltz: 6,500 (canonical)
- Chai: 6,410 (90 short)
- OF3: 6,400 (100 short)
- Protenix: 6,500 (canonical)

The 190 gap is concentrated on shallow-depth cells (per the D3 headline
doc's "19 rows failed" note — where "rows" here refers to (receptor,
seed, depth) rescore rows carrying 10 samples each, so 19 rows × 10
samples = 190 predictions). Root cause not investigated in this pass;
likely per-cell Triton/CUDA transients on shallow-MSA cells where the
model has to work harder.

Reported per-cell fractions use **actual landed n**, not the canonical
6,500 / cell denominator. 0.73 % overall coverage loss, unevenly
distributed. Cell-specific footnote required in any sentence quoting
a shallow-depth cell's n.

Does not affect the D3 headline mechanism split (Boltz clean lever
vs OF3/Protenix degradation-leaning per SC-D-8) — the split relies on
cross-backbone comparison of populated cells, not on missing-data
imputation.

## References

- `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md` §Coverage caveats.
- `dossiers/BLOCK_D/gates/GATE_2_D3_SLOPES.md` (recompute on landed subset).
- `dossiers/BLOCK_D/ASSUMED_NOT_VERIFIED_BLOCK_D.md` §D3 Chai + OF3 190-pred shortfall.
