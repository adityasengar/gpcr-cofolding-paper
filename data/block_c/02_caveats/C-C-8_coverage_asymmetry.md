# C-C-8 — Coverage asymmetry: agonist ~50% NaN, antagonist ~93% covered

**Applies to**: any corpus-wide pose-accuracy or ligand-side statistic.

**The finding**: on `rescore_t7c_full/rows.csv` (post-fix scorer),
`ligand_rmsd_to_ref` NaN rate by (backbone × ligand_role):

| backbone | full_agonist NaN | neutral_antag NaN | decoy_lig NaN |
|---|---:|---:|---:|
| boltz | 51.4 % | 6.9 % | 54.6 % |
| chai | 54.1 % | 6.9 % | 57.6 % |
| of3 | 48.5 % | 3.4 % | 52.2 % |
| protenix | 48.6 % | 3.4 % | 52.0 % |

**Antagonist rows: ~93–97 % covered** (NaN 3–7 %).
**Agonist and decoy rows: ~46–52 % covered** (NaN ~50 %).

**Mechanism**: `ligand_rmsd_to_ref` needs a matcher path
(MCS or fast-path atom_name_element) that succeeds. On Boltz + Chai
(SMILES-derived ligand names in prediction CIFs), the matcher relies
on MCS almost entirely; MCS succeeds on ~50 % of agonist rows because
the reference-side ligand (from the active PDB) is chemically different
from the input agonist for many receptors. On OF3 + Protenix (CCD-based
ligand names), the fast-path succeeds when the reference PDB's CCD
resname matches the prediction's CCD resname.

**Missingness is NOT random** — it correlates with (a) backbone (SMILES
vs CCD naming) and (b) ligand class (antagonist references are more
often the "primary" reference in `refs/reference_set.csv`, giving them
a same-class chemistry match).

**Consequence for the pose section**: the scoped 6.93 % pose-accuracy
statement (SC-C-7) is defensible AS SCOPED to
OF3 + Protenix × neutral-antagonist × ref-matched (n = 4,500) — that
scope explicitly restricts to the coverage-rich subset. Corpus-wide
pose statements need this coverage table alongside them, otherwise a
"three-backbone 40 % dock rate" reading conflates matcher-coverage with
pose accuracy.

**Do NOT**: quote a corpus-wide `ligand_rmsd_to_ref` mean without
naming per-cell coverage.

**Source**: this table derived from `rescore_t7c_full/rows.csv` in this
closeout pass; see `docs/BLOCK_C_GATING_REPORT.md §G6d`.
