# C-D-8 — OPSD × Boltz cross-tier 3σ divergence (D1 vs D3-full)

## Caveat

D1 and D3 overlap on 7 receptors (CNR2, OPSD, ADRB2, LPAR1, CXCR4,
GHSR, NPY1R). Cross-tier consistency check on the predicate-active
fraction at "full" MSA depth (D1 always uses full-mode; D3 "full" is
one of the depth rungs). Broadly consistent except:

**OPSD × Boltz**:
- D1 (n=500, apo): 38.8 % predicate-active.
- D3 (n=50, apo, full-depth rung): 10.0 % predicate-active.
- Divergence: 28.8 points, ~3σ.

Both cells use scorer `d9c646af`. Same receptor, same predicate.
The likely mechanism is that D3's per-depth-cell MSA subsampling
pipeline's "full" rung is NOT bit-identical to D1's upstream default
MSA-mode — D3 sub-samples then re-inflates, and the identity-behaviour
at `full` is subtly different from Block A / D1's default. Not
verified this pass; hypothesis only.

**Do not retract**. The 3σ divergence is a genuine finding worth
flagging in the OPSD-specific section of any manuscript that cites
OPSD numbers. Preferred remediation (per joint-review §6.6 item 3):
a targeted follow-up methods note running the OPSD × Boltz cell at
n=500 under the D3 pipeline — small compute, single cell, deferred
as future work.

**Applies to OPSD only among the 7 overlap receptors**. Every other
apparent CI-miss between D1 and D3-full was either a rounding artifact
(both 0 % or both ≥ 99 %) or small-tail n=50 undersampling.

## References

- `dossiers/BLOCK_D/partA/PARTA_D3.md` §5 (cross-tier D1↔D3 check).
- `dossiers/BLOCK_D/EXPERIMENT_DOSSIER_BLOCK_D.md` §SC-D-10.
- `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` (D1 OPSD × Boltz).
- `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` (D3 OPSD × Boltz full).
