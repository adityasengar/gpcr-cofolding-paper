# C-C-4 — AGTR1's active reference is a β-arrestin-biased-agonist state, not Gα-coupled

**Applies to**: every AGTR1 numeric result in Block C.

**The finding**: AGTR1's active reference is 6OS2, deposited as
*"synthetic nanobody-stabilized angiotensin II type 1 receptor bound
to TRV026"*. Entity list:
1. AT1R–BRIL chimera polymer.
2. **Nanobody Nb.AT110i1_le** — an intracellular nanobody selected to
   stabilise the β-arrestin-biased state of AT1R.
3. **TRV026 peptide** — a β-arrestin-biased-agonist peptide (not a
   G-protein-active agonist like angiotensin II).

**No Gα, no Gβγ, no G-protein-mimetic (Nb35-class) present.** This is
category (d) in the G2 reference-homogeneity table
(`docs/G2_REFERENCE_HOMOGENEITY.md`), uniquely in the S1 15-set (count
1/15 — every other receptor's active reference has a native heterotrimer,
mini-G, or chimera on the Gα-pathway).

**`refs/reference_set.csv` label vs actual**:
- `resolved_state = Ga-coupled-active` (imprecise; 6OS2 is not Gα-coupled).
- `stabilising_elements = nanobody_beta_arrestin_biased_agonist` (accurate).
- `active_stabilization_source = nanobody` (accurate coarse category).

The `resolved_state` label is imprecise but not a mechanical defect
in the scorer — see `docs/AGTR1_REFASSIGN_REPORT.md` §Section 2, all
three checks (swap, predicate, mapping) pass.

**Consequence for the manuscript**: AGTR1 warrants its OWN Methods
footnote about the biased-agonist active reference — separate from
whatever CXCR2's OF3-only inversion footnote says (parity with Block B's
five-independent-footnote treatment of AA2AR, per
`docs/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md`).

**Consequence for G2**: excluding AGTR1 for scope-consistency
("Gα-pathway-only active references") flattens the pooled slope from
−0.325 to −0.060 with CI [−0.246, +0.087]; the reference-separation
hypothesis is not supported on the remaining 14 receptors either
(SC-C-5).

**Do NOT**: treat AGTR1 as if its inversion is a stochastic outlier;
name the biased-agonist reference-curation reason.

**Sources**: `docs/AGTR1_REFASSIGN_REPORT.md`, `docs/G2_REFERENCE_HOMOGENEITY.md`,
`../paper_af3_release/panel/refs/pdb/6os2.cif`.
