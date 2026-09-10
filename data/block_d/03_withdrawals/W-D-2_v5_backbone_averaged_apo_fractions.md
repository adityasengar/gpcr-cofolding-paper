# W-D-2 — "v5 (Block C Tier 3) apo-active-fraction point estimates as backbone-averaged claims"

## Claim as previously stated

Block C Tier 3 v5 analysis reported per-receptor apo-active-fraction
point estimates (CNR2 0.27, OPSD 0.38, ADRB2 0.26, LPAR1 0.22, CXCR4
0.04, GHSR 0.02, NPY1R 0.02) at n=100 or lower. These were carried
as receptor-level bimodality signals.

## Retraction

**Withdrawn as receptor-level claims.** D1 at n=500 per (receptor,
backbone) shows the v5 aggregate is a backbone-averaged number that
happens to average across a bimodal per-backbone distribution:

- CNR2 v5=0.27 vs D1 per-bb: Chai 0.998, Boltz 0.022, OF3 0.018,
  Protenix 0.016 (mean 0.263 — coincidence on the mean).
- OPSD v5=0.38 vs D1 per-bb: Boltz 0.388, Chai 0.986, OF3 0.094,
  Protenix 0.000 (Boltz alone hits 0.388).
- ADRB2 v5=0.26 vs D1 per-bb: Chai 1.00, others 0.000. Mean 0.260 —
  coincidence again.

Backbone-averaged reporting hides the CNR2/ADRB2/OPSD Chai
active-outlier pattern (F1 → SC-D-1) that D1 surfaces as receptor-specific.

## Basis

- `experiments/022_tier_d1_deep_apo/analysis/tier_d1_full_headline_2026_09_06.md` §"v5 comparison — falsification results".
- `dossiers/BLOCK_D/partA/PARTA_D1.md` §1.
- Block C Tier 3 v5 headline (superseded).

## What the manuscript should say instead

> Any per-receptor apo-active-fraction number is a per-backbone
> quantity; cross-backbone averages conceal the receptor-specific
> backbone-outlier pattern. Report per-backbone fractions with
> per-cell CIs; use panel-mean receptor-boot CIs only with the
> n-limitation named (SC-D-1, C-D-1).
