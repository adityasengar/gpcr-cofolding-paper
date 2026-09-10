# W-D-1 — "Chai has a systematic active bias" (D1 smoke story)

## Claim as previously stated

The D1 smoke result at n=1 receptor (CNR2, per auto-memory
`chai_cnr2_apo_model_bias_2026_09_06.md`) suggested Chai has a
receptor-agnostic systematic active bias — Chai predicts CNR2 apo
as active on 499/500 samples while Boltz/OF3/Protenix land at 0.6–2.2 %.

## Retraction

**Withdrawn.** Panel-scale D1 shows Chai is active-outlier on only
3 of 7 receptors (CNR2 99.8 %, OPSD 98.6 %, ADRB2 100.0 %) and
inactive-consistent on the other 4 (LPAR1 0.0 %, CXCR4 0.0 %, GHSR
0.0 %, NPY1R 0.0 %). Similarly, OF3 is active-outlier on LPAR1 (91.8 %)
but not on the other 6. The pattern is receptor-specific, not global.

Formalised in SC-D-1: backbone active-outlier = ≥+50-pt predicate-active
delta over max-of-others. All 4 outliers (Chai on CNR2/OPSD/ADRB2, OF3
on LPAR1) satisfy the rule. Reproduces on Block A independent data at
n=25/cell (SC-D-11).

## Basis

- `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` — 14,000 preds.
- `dossiers/BLOCK_D/partA/PARTA_D1.md` §5 (F1 formalisation).
- `dossiers/BLOCK_D/EXPERIMENT_DOSSIER_BLOCK_D.md` §SC-D-1, §SC-D-11.

## What the manuscript should say instead

> Backbone active-outlier behaviour on apo GPCRs is receptor-specific:
> Chai over-predicts active on CNR2, OPSD, and ADRB2 while landing
> inactive-consistent on LPAR1, CXCR4, GHSR, NPY1R. OF3 shows the
> mirror pattern on LPAR1. The pattern is not a global-backbone bias;
> it is receptor-conditioned and reproduces on Block A independent
> data.
