# Post-review annotation changes to reference_set.csv

Annotation-column edits made after `post-review-analysis-batch`; no coordinate
data or per-PDB axis values changed. Row-level `provenance_sha256`,
`ref_pdb_sha_active/inactive`, and every measurement column remain
byte-identical to the pre-review file. Only two annotation-column values in
two rows were updated. The parent working repo's `refs/reference_set.csv`
retains the pre-review annotations pending an explicit user decision on
propagating these edits back to the working repo.

## AGTR1 (active reference 6OS2)

**Column changed**: `stabilising_elements`
- Pre-review: `nanobody`
- Post-review: `nanobody_beta_arrestin_biased_agonist`

**Rationale**. 6OS2 is technically nanobody-stabilised (Wingler 2020 Science,
Nb.AT110i1_le + TRV026 β-arrestin-biased agonist). The pre-review annotation
was factually true but too coarse. The paper's "distinctive activation
mechanism" argument (F6.44/F6.45 ratcheting, N7.46 inward movement) refers to
**6DO1** (Wingler 2019 Cell, AngII partial agonist), not 6OS2. Methods must
cite 6DO1 wherever the distinctive-mechanism argument appears.

**Also documented (no CSV change)**: 6OS2's BRIL fusion insertion range (per
`fusion_partner_insertion_range = 227,228,229` column) falls within the rough
tilt-predicate residue-range window on AGTR1 (approx 220–265 by mixed
BW/PDB numbering; AGTR1's 6.30 anchor is at 235 per the row's
`anchor_positions` field). BRIL at 227–229 is just below the 6.30 anchor —
strictly, in ICL3 adjoining TM6. T4 flagged this as a "predicate-window
adjacent" fusion. Not previously in the caveat set. Flag 43 covers it.

**No PDB swap. No reference-axis rescore.** Reference cleanly discriminates
apo vs cognate at Δtilt = 12.5 Å (P1a).

## CNR2 (inactive reference 5ZTY)

**Column changed**: `construct`
- Pre-review: `wt`
- Post-review: `multi_mutation_incl_R242E_tilt_window`

**Rationale**. Per T4's widened O-4 audit, 5ZTY carries 7 receptor mutations
per RCSB `pdbx_mutation` metadata (G78L, T127A, T153L, R242E, G304E, and two
others). The pre-review `construct=wt` value was flatly wrong. Post-review
annotation names the load-bearing mutation R242E (charge reversal at BW 6.30
= sequence position 242 in this receptor's numbering — INSIDE the tilt
predicate window).

**The `construct` column is corpus-wide untrusted**. T4 found 52/127 (41%)
evaluable PDBs carry `construct=wt` while RCSB reports mutations. This CNR2
edit fixes one instance; the systemic issue is captured in Flag 42 and
caveat C-11. The corpus-wide repair is deferred as a stated limitation
(MANUSCRIPT_FLAGS.md).

**No PDB swap.** Per the dispatch: bistability is reported as a panel-level
property (25/29 apo bimodal cells per current dossier count), not anchored on
any single receptor's reference pair. CNR2 is retained as an illustrative
case: 5ZTY has a Janus property (agonist-like extracellular pocket, inactive-
like intracellular face per Li 2019 Cell), which explains both Block A's
clean pass (reads cytoplasmic face where 5ZTY is genuine inactive) AND Block
C's compromised pocket-shape claims involving CNR2 (reads pocket where 5ZTY
is agonist-like).

## OPRD (no annotation change)

The dispatch decision: OPRD 6PT2 is HELD; no swap. The 16.75 Å NPxxY-OH is
honest geometry (T6 independent recompute + OPRD artifact-check verified
bit-exactly). 6PT2 is agonist-only + BRIL, not Gα-engaged. The NPxxY H-bond
network does not form without Gα clamping — an agonist-only crystal fails
NPxxY by construction. OPRD is handled via exclusion set E5 (agonist-only
actives: OPRD, CNR1, FZD4) with headline recomputed with and without E5.
No PDB swap; no annotation change; the reference is limited but its numeric
values are correct as-recorded.

## Parent working repo state

The parent working repo `/Users/SENGAAD1/Documents/claude/paper_af3/refs/reference_set.csv`
still carries pre-review annotations (`AGTR1 stabilising_elements=nanobody`,
`CNR2 construct=wt`). Propagating these two edits back to the parent
requires an explicit user decision — the parent's refs/ is under the
CLAUDE.md standing rule "No edits to `refs/reference_set.csv` without
explicit user go". This release archive's copy holds the post-review-frozen
version and is the citable authority for the manuscript.
