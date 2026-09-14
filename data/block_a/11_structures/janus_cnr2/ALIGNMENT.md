# janus_cnr2 — inactive vs active CB2 pair with engineered residues flagged

## Files
- `5ZTY.cif` — inactive CB2 with T4L insertion + 7 engineered mutations (incl. R242E, G304E).
- `8GUR.cif` — active CB2–Gi–CP55940 (cryo-EM ternary).

## Superpose on
Chain A (receptor) TM1–TM7 Cα only. In 5ZTY exclude T4L insertion range
(check chain header for insertion boundaries). In 8GUR exclude Gα/Gβ/Gγ
chains + any nanobody.

## CNR2 numbering (uniprot P34972)
- R242 (BW 6.30) → engineered R242E in 5ZTY (destabilises TM6 outward
  motion; anchors DRY lock)
- G304 → engineered G304E in 5ZTY (further stabilises inactive conformation)
- Y5.58 ≈ Y223
- Y7.53 ≈ Y293

## Purpose
Illustrates why CNR2 references drive the "5ZTY heavily engineered inactive"
observation in the reference-side audit — the very positions the predicate
depends on (6.30 near tilt anchor 6.37) carry engineered mutations.
