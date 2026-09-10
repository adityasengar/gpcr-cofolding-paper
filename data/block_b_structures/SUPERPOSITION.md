# Superposition rule for visualising these CIFs

**Align on TM1–TM5 + TM7 Cα only. Exclude TM6.**

## Why

The instrument used to call activation is a two-instrument predicate on
- **NPxxY-OH** (Y5.58-OH ↔ Y7.53-OH distance) — a TM5/TM7 packing axis.
- **GPCRdb TM6 tilt** (2×46 Cα ↔ 6×37 Cα distance) — a TM6-outward-swing axis.

Aligning by full 7TM including TM6 lets the model's own TM6 outward swing
soak into the alignment residual, hiding the exact geometry the predicate
scores. **The scorer aligns on full 7TM** for numerical consistency across
40 receptors × 4 arms × 4 backbones (`scorer/pocket_metrics.py`); the
scorer's alignment is calibrated to be robust across receptors and is not
intended for figure making.

## BW ranges to include in the alignment

- **TM1**: 1×30 – 1×60 Cα
- **TM2**: 2×39 – 2×65 Cα
- **TM3**: 3×22 – 3×55 Cα
- **TM4**: 4×39 – 4×62 Cα
- **TM5**: 5×36 – 5×68 Cα
- **TM7**: 7×32 – 7×56 Cα

## BW range to EXCLUDE

- **TM6**: 6×25 – 6×60 Cα excluded entirely from the alignment so its
  outward swing is diagnostic in the residual.

## Notes

- Use Cα only, not full backbone; side-chain differences are irrelevant
  to the alignment target.
- Weight residues equally; do not down-weight by pLDDT (the goal is a
  geometric alignment, not a confidence-weighted one).
- Deviation from the scorer's own alignment is deliberate. State this
  explicitly in the figure caption to prevent readers from concluding
  the figure and the number tables use the same superposition — they
  don't.
