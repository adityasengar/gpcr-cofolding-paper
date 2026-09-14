# class_b_kink — Class B active vs inactive pair, kink-angle demonstration

## Files
- `6X18.cif` — Class B active reference (with G-protein/ECD).
- `5VEW.cif` — Class B inactive/apo reference.

## Superpose on
Chain A (receptor) TM1–TM7 Cα. Exclude ECD residues (Class B receptors
typically resolve an extracellular domain — verify chain / residue range
against the structure's PDB header). Exclude Gα/Gβ/Gγ if present in active.

## Purpose
Illustrate the TM6 kink discriminator: Class B active-vs-inactive is
identified by kink angle rather than by 3.50–6.30 tilt (C-2). The kink
measurement's three anchor residues are documented in the `refs/reference_set.csv`
`anchor_class_b_kink_ref` column set — 6.39, 6.50, 6.54 in Wootten numbering
(receptor-specific uniprot positions vary).

## Measured values
- kink angle (from reference_set.csv `angle_class_b_kink_ref`):
  active reference ≈ 154 deg, inactive reference ≈ 161 deg.
- Threshold `threshold_kink_used` = 159.95° (active if < threshold).
