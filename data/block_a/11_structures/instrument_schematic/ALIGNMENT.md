# instrument_schematic — β2AR active + inactive

## Files
- `3SN6.cif` — active β2AR–Gs–Nb35 complex (Rasmussen 2011). Chain **R** is the receptor.
- `2RH1.cif` — inactive β2AR–carazolol (Cherezov 2007). Chain **A** is the receptor.

## Superpose on
Chain R (3SN6) vs chain A (2RH1) — receptor Cα atoms TM1–TM7 only.
Exclude the fusion partners (T4L on 2RH1), the Gs heterotrimer (chains A/B/G in 3SN6),
and Nb35 (chain N in 3SN6) from the alignment atoms.

## ADRB2 numbering (uniprot P07550)
- Y5.58 (Y219 ADRB2) — NPxxY OH acceptor at TM5 end
- Y7.53 (Y326 ADRB2) — NPxxY-Y core
- 2×46 tilt anchor Cα (~L124 ADRB2)
- 6×37 tilt anchor Cα (~F282 ADRB2)
- P5.50 (P211 ADRB2), I3.40 (I121 ADRB2), F6.44 (F290 ADRB2) — PIF connector triad

## Measured values (from reference_predicates.csv)
- Δ tilt (2×46–6×37 Cα, active − inactive) ≈ 5.02 Å (published landmark)
- Δ NPxxY-OH (Y5.58 OH – Y7.53 OH) ≈ 5.4 Å

## Source
Both CIFs from `paper_af3_release/panel/refs/pdb/`.
