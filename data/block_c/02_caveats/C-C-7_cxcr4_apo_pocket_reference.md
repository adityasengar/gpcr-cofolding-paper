# C-C-7 — CXCR4's active reference has an apo orthosteric pocket

**Applies to**: CXCR4-specific results in Block C.

**The finding**: CXCR4's active reference is 8U4N, whose deposition
title is *"Structure of Apo CXCR4/Gi complex"*. Chain composition:
native Gα-i + Gβ + Gγ + CXCR4 receptor. The complex has a canonical
Gα-coupled effector but the receptor's ORTHOSTERIC POCKET is APO — no
bound orthosteric ligand.

**Category on the effector axis**: (a) native heterotrimer, consistent
with the S1 15-set's dominant category (12/15). **No curation-scope
anomaly on the effector axis**, unlike AGTR1 (C-C-4).

**Category on the pocket axis**: apo pocket. This IS unusual — every
other active reference in the S1 15-set carries a bound orthosteric
ligand (agonist).

**Consequence**: predictions of CXCR4 with a bound agonist may end at a
slightly different pocket-side geometry than 8U4N's apo pocket (which
lacks the ligand-induced side-chain rearrangements). This could shift
`pocket_ca_rmsd_active` and `pocket_ca_rmsd_inactive` values for CXCR4
in either direction. It is NOT the mechanism behind Chai's marginal
CXCR4 AUROC (0.457) — CXCR4 clears on Boltz (0.993) and Protenix
(1.000), so backbone-specific variation dominates.

**Manuscript treatment**: name in Methods as a reference-curation
observation for CXCR4 alongside the AGTR1 biased-agonist reference.
Not a hard-stop, not a withdrawal — a scoped note.

**Sources**: `../paper_af3_release/panel/refs/pdb/8u4n.cif` header,
`docs/G2_REFERENCE_HOMOGENEITY.md` §1 table.
