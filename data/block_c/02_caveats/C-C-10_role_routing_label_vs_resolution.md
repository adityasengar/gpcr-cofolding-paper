# C-C-10 — Reference-role routing labels differ, resolved PDBs collapse

**Applies to**: the Methods sentence on reference-role routing; the
pose-section limitation.

**The finding** (per `docs/BLOCK_C_GATING_REPORT.md §G3`): the row-level
column `pocket_ref_role_inactive` DIFFERS across ligand_role subsets on
every receptor:
- `full_agonist` and `decoy_lig` rows → `generic_inactive_fallback`.
- `neutral_antagonist` rows → `inactive_neutral_antagonist`.

But the resolved PDB SHA is IDENTICAL across `ligand_role` for every
receptor: 28/28 receptors with a defined `pocket_ref_pdb_sha_inactive`
show 1 distinct SHA per receptor across the three ligand-role subsets.
**0/28 receptors differ**.

**Classifier consequence (positive, by construction)**: S1's Δ feature
= `pocket_ca_rmsd_active − pocket_ca_rmsd_inactive` is computed against
a per-receptor pair identical across ligand_role values. Reference-
identity leak is ruled out by construction — Check 1's SHA-identity
observation reports the collapsed state, and no leak was detectable
under a routing that could differentiate.

**Pose consequence (limitation)**: `ligand_rmsd_to_ref` for a given
input row is computed against the reference PDB whose ligand is
IDENTIFIED once per receptor (typically the antagonist bound in the
inactive PDB when the inactive side is used). For NEUTRAL_ANTAGONIST
input rows, this is chemistry-appropriate (predicted antagonist
compared against reference antagonist). For FULL_AGONIST or DECOY_LIG
input rows that end up scored on the inactive-side reference (per the
row's own `_pocket_metric_ref_used`), the comparison is
CHEMISTRY-MISMATCHED — an agonist pose against an antagonist-bound
reference — and the resulting RMSD carries a floor unrelated to
prediction quality.

**Manuscript sentences** (from Methods):
- *"Role-specific reference-routing labels were emitted for each row,
  but resolved to the same reference PDB per receptor in the current
  corpus. The classifier's active-vs-inactive pocket-Cα-RMSD delta is
  therefore computed against a per-receptor reference pair identical
  across ligand classes; reference-identity leak is ruled out by
  construction rather than by audit."*
- *"For at least one ligand class per row, ligand_rmsd_to_ref is
  computed against a chemically different bound ligand than the input;
  this contributes a floor to the pose-accuracy metric that is
  independent of prediction quality (see coverage-asymmetry note
  C-C-8)."*

**Sources**: `docs/BLOCK_C_GATING_REPORT.md §G3`, corpus-level SHA
identity check in this closeout pass.
