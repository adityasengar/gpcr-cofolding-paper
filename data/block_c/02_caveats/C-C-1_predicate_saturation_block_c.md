# C-C-1 — Two-instrument predicate is saturated on Block C

**Applies to**: every Block C claim that could otherwise be stated on the
binary two-instrument predicate.

**The finding**: the Class-A two-instrument predicate
(`d_npxxy_y558_y753_oh < 9.082 AND d_gpcrdb_tm6_tilt_246_637_ca > 14.932`)
is floor-pinned on apo-cognate-ligand rows and ceiling-pinned on
cognate-partner-cognate-ligand rows across a majority of the (receptor
× backbone × ligand-class) cells in the Tier-3 corpus. ~65 % of cells
sit on a saturated boundary of the binary predicate.

**Consequence**: any pocket-side ligand-identity discrimination signal
that shows up on continuous pocket-Cα-RMSD is invisible on the binary
predicate. This is the reason Block C reports continuous readouts, not
binary fractions, for the SC-C-1 2×2 interaction, the SC-C-4 S1
classifier, and the SC-C-2 P4 ordinal recovery.

**Manuscript wording**: *"The class-conditional two-instrument
activation predicate that resolves the four-arm partner ladder in
Block B is saturated on Block C's ligand-class panel: apo-arm rows
floor-pin at the low end, cognate-arm rows ceiling-pin at the high end,
and ~65 % of cells sit on one of the two boundaries. Ligand-identity
discrimination is therefore reported on continuous pocket-Cα-RMSD."*

**Do NOT**: quote a binary-predicate active fraction for a Block C
ligand-class discrimination claim.

**Source**: `experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3_2x2_ligand_state_specificity.json`;
`SIGNAL_RECOVERY_REPORT.md §Rung 0`.
