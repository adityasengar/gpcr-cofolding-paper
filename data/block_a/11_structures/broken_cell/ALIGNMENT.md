# broken_cell — ACM1/cognate/Protenix median-pLDDT row vs healthy comparator

## Files
- `ACM1__cognate__protenix__seed1340440218__row967__BROKEN.cif` — copied via rsync
- `ACM1__cognate__chai__seed966761149__row948__HEALTHY.cif` — copied via rsync
- `MISSING_ACM1_active.cif` — ACM1 active reference.

## Selection rule
- Broken row: median plddt_mean within ACM1/cognate/protenix (25 rows, all with mean cell pLDDT < 50).
  Row index 12 of 25.
  plddt_mean = 38.38, d_gpcrdb_tm6_tilt = 21.55 Å,
  d_npxxy_oh = 26.63 Å.
- Healthy row: ACM1/cognate/chai best plddt_mean row.
  plddt_mean = 69.23

## Superpose on
Chain A receptor Cα TM1–TM7 (both prediction files). Exclude Gα/Gβ/Gγ.
The broken row is expected to show severely distorted TM6 packing —
alignment across TM bundle may fail for the broken structure; consider
a partial-atom alignment on TM3/5/7 if the RMSD blows up.

## ACM1 numbering (uniprot P11229)
- Y5.58 ≈ Y213
- Y7.53 ≈ Y418
- Full anchor positions from `rows.csv:anchor_*_uniprot_pos` for these rows.

## Purpose
Illustrate the C-12 caveat: A1–A6 scorer gates have no pLDDT floor.
Structures with mean pLDDT < 50 pass A1–A6 (passed=True), so the corpus
retains 25 rows that are locally correct in sequence but structurally
unreliable. E1 is defined precisely to strip these.
