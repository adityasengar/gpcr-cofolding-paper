# 11_structures/SELECTION.md — prediction picks and rules

| Panel | Type | Selection | Rule | Percentile within cell |
|---|---|---|---|---|
| instrument_schematic | reference-only | 3SN6 (active) + 2RH1 (inactive) | canonical β2AR published pair | N/A |
| confidently_wrong | prediction | AA2AR/Boltz/apo row_id=567 | SUBSTITUTED rule (no >8Å hit in Class A): top-quintile RMSD, highest pLDDT within | 100th percentile within cell |
| connector_orthogonality | reference-only | 4LDE (active β2AR) | clean canonical active reference | N/A |
| agonist_only_vs_ternary | reference-only | 6PT2 + 8FZQ | canonical agonist-only vs ternary contrast | N/A |
| janus_cnr2 | reference-only | 5ZTY (inactive) + 8GUR (active) | engineered mutations in predicate window | N/A |
| class_b_kink | reference-only | 6X18.cif + 5VEW.cif | canonical Class B pair; GLP1R preferred, else GCGR/CRHR1/PTH1R fallback | N/A |
| success_case | prediction | DRD2/cognate/of3 row_id=8285 | median RMSD within cell (excl_any filter applied) | 50th |
| broken_cell | prediction (broken) | ACM1/cognate/protenix row_id=967 | median plddt_mean within the broken cell | 50th |
| broken_cell | prediction (healthy) | ACM1/cognate/chai row_id=948 | highest plddt_mean row among non-protenix ACM1/cognate | 100th (top of cell) |

## Notes
- `confidently_wrong` uses a **substituted** rule because no Class A row in the 9,490-row corpus has `rmsd_to_active_ref > 8 Å`. The corpus max is documented in ALIGNMENT.md.
- No structure was chosen for appearance; every prediction pick is rule-driven.

## Reference PDBs fetched from RCSB
- **3SN6** → 3SN6.cif
- **8FZQ** → 8FZQ.cif
- **6X18** → 6X18.cif
- **5VEW** → 5VEW.cif
