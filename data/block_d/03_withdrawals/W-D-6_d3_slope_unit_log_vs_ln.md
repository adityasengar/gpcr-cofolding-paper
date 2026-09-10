# W-D-6 — D3 slope unit label "%/log(depth)"

## Claim as previously stated

The D3 headline table (`experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md`)
labelled the four slopes as **%/log(depth)** (Protenix −2.96, OF3
−2.73, Boltz −1.68, Chai −0.82).

## Retraction

**Withdrawn as-labeled**. GATE-2 recompute shows the numbers reproduce
exactly **only under natural log** (`ln`, base *e*), NOT base-10 log
(`log10`). Off by factor ln(10) ≈ 2.303 otherwise.

**Correct unit label**: `%/ln(depth)` (percent-active per e-fold
change in MSA depth).

The magnitude of the fix is exactly ~2.3× — small on the number itself
(Boltz −0.73 under log10 vs −1.68 under ln — an editable difference
but a load-bearing one for anyone recomputing).

## Basis

- `dossiers/BLOCK_D/gates/GATE_2_D3_SLOPES.md` — verified against all three log bases (log2, ln, log10) and all `full=X` nominal choices. Only ln with full=4096 reproduces the headline table exactly.
- `analysis/block_d/scripts/derive_d3_slopes.py` — authoritative reproduction script uses `ln` explicitly.

## What the manuscript should say instead

Cite slopes as `%/ln(depth)` or equivalently "per e-fold change in
MSA depth". Do NOT report `%/log(depth)` — off by factor ~2.3.
