# C-C-6 — Matcher path affects ligand RMSD, not pocket-Cα RMSD

**Applies to**: any manuscript statement that quotes a pocket-Cα-RMSD
number.

**The finding**: `pocket_ligand_atom_map_method` values in the Block C
corpus are `{mcs, atom_name_element (fast-path), mcs_too_small, NaN}`.
This column drives `ligand_rmsd_to_ref` and any ligand-side statistic.
It does NOT enter `pocket_ca_rmsd`, `pocket_ca_rmsd_active`, or
`pocket_ca_rmsd_inactive` — those are receptor-side quantities computed
on 12 FIXED BW pocket positions (3.32, 3.33, 3.36, 5.42, 5.43, 5.46,
6.48, 6.51, 6.52, 6.55, 7.39, 7.42) via
`scorer/pocket_metrics.py::pocket_ca_rmsd`, with 7TM Cα Kabsch
alignment on the receptor.

**Consequence**: the S1 classifier (SC-C-4), the 2×2 pocket-Cα
interaction (SC-C-1), the P4 ordinal recovery (SC-C-2), and the S3
consensus signal (SC-C-3) are ALL unaffected by matcher-path bugs. Only
the SC-C-7 pose-accuracy claim inherits the matcher-path uncertainty.

**Do NOT**: propagate matcher-path caveats to classifier claims.

**Source**: `scorer/pocket_metrics.py::pocket_ca_rmsd` (fixed BW anchor
set, receptor-Cα Kabsch); `scorer/pocket_metrics.py::_mcs_ligand_rmsd`
(the matcher-path code path).
