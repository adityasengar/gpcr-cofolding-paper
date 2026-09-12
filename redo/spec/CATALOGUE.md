# REDO_EXPERIMENT_CATALOGUE.md

Input to designing the re-run that supersedes Blocks A–D. Compiled 2026-09-11 by a
research session with read access to the whole repo and write access to this file only.

**What this is.** A catalogue with costs and a ranking, not a programme. Aditya picks.
Where the framing I was given is wrong, it says so (§0.3).

**Revision state.** Second pass 2026-09-11 added Groups 8 (MSA depth) and 9 (the deep-apo
floor). Third pass 2026-09-11 applied the lit session's novelty audit
(`lit/analysis_review/REDO_CATALOGUE_NOVELTY_CHECK.md`), which checked every load-bearing
`Novelty.` line against `INDEX.md`. **Every OPEN call survives.** One row (E3.3) was wrong
as written, one (E1.2) contradicted itself, three had mischaracterised supports, and every
"of 81" denominator was unsound — all corrected below and each correction marked where it
sits. Claims imported from that audit were re-verified here against the notes themselves
before being written in; the counting bugs that turned up doing so are in §3.0.

**How to read a cost class.** The project's three classes are kept, plus one that the
existing documents do not have and now need:

| class | meaning | who pays |
|---|---|---|
| **free** | re-analysis of row data already in `data/block_*/` | us, hours |
| **free (them)** | already computed upstream, sitting in a file that was not zipped | them, minutes |
| **free\*** | new measurement on *deposited* structures — no inference, but real labour and a download | us, days |
| **cheap** | re-scoring existing predictions, no new inference | them, hours |
| **real** | new predictions | compute |

`free (them)` is introduced because it is the single largest category in the four ask
documents and the existing vocabulary hides it inside `free`, which reads as "we can do
it ourselves" — and for Blocks C and D we cannot.

**Prediction accounting unit.** Throughout, one *cell* = one (receptor × backbone × arm)
at 50 predictions (5 seeds × 10 samples), the Block B grid. So:

- one arm on the current 40-receptor Class A panel × 4 backbones = **8,000 predictions**
- one arm on the full 64-receptor Class A both-state census × 4 backbones = **12,800**
- one arm on 40 receptors × 1 backbone = **2,000**

---

# 0. Ground truth established for this document

Every number in §0 was computed here today from the files named, not read from a claim
sheet. Where it disagrees with a project document, the disagreement is stated.

## 0.1 What we actually hold, per block

| drop | files | row-level prediction table | predictions in hand |
|---|---:|---|---:|
| A | 80 | `data/block_a/01_rows/block_a_rows.csv`, 9,490 × 55 | **9,490** |
| B | 104 | `data/block_b/01_rows/rows_tidy.csv`, 32,000 × 76 | **32,000** |
| C | 70 | `data/block_c/12_g4_off_site_census/g4_full_census_v2.csv`, 40,000 × 16 — **off-site ligand geometry only; no state, no NPxxY, no tilt, no pLDDT, no RMSD** | **40,000 rows, 0 usable for state** |
| D | 61 | **none** | **0 of 42,180** |

Block D's 42,180 decomposes as D1 14,000 + D2 2,370 + D3 25,810, named by HPC path in
`data/block_d/10_structures/MANIFEST.json` and shipped in neither.

Block B ships **no boolean state column at all** — no `active`, no `npxxy_active`, no
`tilt_active`. Every Block B state call in the manuscript was recomputed here from the
two axis columns and the two threshold columns. That is free, and it is worth knowing
before anyone assumes a re-run will ship one.

Block C: 82 distinct data filenames are referenced inside the drop's own documents, 16
are present, **66 are absent**; netting the capitalisation variant, the deliberately
retracted v1 census, one renamed file and three held in other blocks leaves **~61
genuinely missing**. Exactly one of the 16 present is row-level, and it carries no state.

## 0.2 The structural universe the redo can draw on

From `lit/panels/cache/gpcrdb_structures.json`, 1,716 entries, recomputed here:

| quantity | value |
|---|---:|
| Class A entries | 1,358 |
| Class A entries annotated Active or Inactive | **1,336** (965 Active / 371 Inactive) |
| Class A entries annotated **Intermediate** | **21** |
| unique Class A receptors with an Active/Inactive entry | **199** |
| Class A receptors with **both** states (species-specific) | **66** |
| …collapsing species, as receptor slugs | **64** |
| …restricted to human | **61** |
| all-class both-state receptor slugs | **83** |

**Every one of our 40 Class A panel receptors is in the 66.** So the panel is 40 of 64
slugs — 63% of the Class A both-state census — and there are exactly **24 off-panel
Class A both-state receptors** available: `5ht2a ada1a c5ar1 ccr2 ccr6 ccr8 cxcr3 drd4
gpr52 gpr6 hrh2 mtr1a mtr1b nk1r ntr1 oprm oxyr pd2r2 pe2r4 s1pr1 s1pr5 ssr2 ta2r tshr`.

**The calibration population, sized.** Splitting the 1,336 Class A Active/Inactive
structures by whether the receptor is on our panel:

| | structures | Active | Inactive | receptor entries |
|---|---:|---:|---:|---:|
| **off-panel** | **726** | 611 | **115** | 155 |
| on-panel | 610 | 354 | 256 | 44 |

This is the single most consequential fact for the calibration decision, and it is not in
any project document: **an off-panel calibration set is 5.3:1 active-biased and contains
only 115 inactive structures.** A midpoint objective fitted on that population without
balancing will not behave like the current one, which was fitted on 80 rows drawn from a
set that is 354:256. The calibration design has to state its balancing rule up front.

Method and resolution are available for all 726 (584 cryo-EM, 142 X-ray; median 3.00 Å),
so a quality floor can be set in advance rather than discovered afterwards — which is
exactly what `reference_audit.csv` could not support, its `method` and `resolution`
columns being the same placeholder string on all 80 rows.

**Date-stratified holdout, sized.** Using `publication_date` (verified in
`lit/panels/README.md` to be the PDB initial release date, agreeing with RCSB on all
1,713 matched entries) against the Boltz-2 structural cutoff 2023-06-01:

- 486 Class A Active/Inactive structures released on or after the cutoff (432 Active, 54 Inactive)
- **12 both-state Class A receptors whose earliest *active* entry is post-cutoff**:
  `ada1a b1b1u5 ccr8 cxcr3 cxcr4 drd4 gpr6 hrh2 hrh3 mchr1 pd2r2 ta2r`
- **5 whose *both* states are entirely post-cutoff**: `ada1a ccr8 cxcr3 gpr6 mchr1` —
  four of them off our current panel

That is a buildable memorization control. It needs no new machinery, only panel choice.

## 0.3 Five places the brief I was given, or a sibling document, is imprecise

Recorded because each would propagate into a dispatch.

1. **"18,400 already-scored predictions"** (`CLAUDE.md:146`, `HANDOVER.md:64`) does not
   reproduce from the census. `g4_full_census_v2.csv` gives, for agonist + antagonist on
   the 28 receptors that have both roles, **22,400** predictions (28 × 2 roles × 2 arms ×
   4 backbones × 50). 18,400 is 23 × 800 and corresponds to the 23-receptor *common* set
   from `stage3_2x2_ligand_state_specificity.json`, which additionally requires both
   references. Both are defensible; they are different objects and must not be quoted
   interchangeably.
2. **"66 receptors with both states" is a Class A count, and "19 Class A receptors we
   lack" is a ConfoRNets count.** `rebuttals/PANEL_EXPANSION_CLASS_A.md` says 19; the gap
   against the whole GPCRdb snapshot is **24**. Both correct for their own universe.
   `rebuttals/PANEL_EXPANSION.md` §1 additionally says we hold "29" of ConfoRNets' 51;
   recomputed here it is **30 against our 48** and **27 against our 40 Class A** —
   `PANEL_EXPANSION_CLASS_A.md` §2 itself says 27. Three numbers for one overlap.
3. **`rebuttals/PANEL_EXPANSION.md` §4 lists `GLR` as a both-state receptor we lack. GLR
   is our GCGR.** `GCGR` resolves in GPCRdb as `glr_human` (18 entries, 13 Active / 5
   Inactive); `CRHR1` resolves as `crfr1_human`. Neither slug resolves by lowercasing, so
   any script that maps panel slugs to GPCRdb by `slug.lower()` silently drops them — the
   same class of defect as the `_human` default recorded in `lit/panels/README.md`. The
   §4 list also omits `PE2R4`, which has both states (6 Active / 2 Inactive) and is on no
   panel. Of our 48, exactly one receptor lacks a second state in GPCRdb: **FZD6**
   (Active only).
4. **The 21-mer arm specification is wrong as written.** `analysis/block_b/DATA_REQUESTS.md:221`
   and `rebuttals/BLOCK_B.md:479` both specify "Gα residues **334–354**". From
   `data/block_b/02_constructs/construct_build_report.md`, the five canonical partners are
   Gs/GNAS 394 aa, Gi/GNAI1 354, Gq/GNAQ 359, G12/GNA13 377, Gt/GNAT1 350. Residues
   334–354 are the C-terminal 21 **only for Gi1**. For Gs that range ends 40 residues
   short of the C terminus. The spec must read *"the last 21 residues of the cognate
   subunit"*, with the per-class ranges enumerated, or four of five classes will be built
   wrong. This is the kind of error that produces a campaign nobody can use.
5. **The headline apo/cognate rates are computed on 48 receptors inside a paragraph scoped
   to 40.** *(Added second pass.)* All eight rates at `results.tex:47–50` reproduce exactly
   from the shipped `active` column on **all 48 receptors with no exclusions applied** —
   16.0 / 32.7 / 24.2 / 14.5 apo and 83.4 / 75.0 / 79.9 / 87.1 cognate. Two consequences.
   (i) The sentence three lines above them scopes the result to "the 40 Class A receptors";
   on Class A alone the apo rates are **12.3 / 28.7 / 9.9 / 6.9**, so OpenFold3 more than
   halves and Protenix drops by more than half. The 8 class B and F receptors are scored by
   *different* predicates (a kink angle for B, tilt alone for F), so a pooled
   "predicate-active rate" over 48 mixes three instruments. (ii) `methods.tex:186–188` says
   E1 and E2 "are applied everywhere"; these rates do not have them applied, and applying
   them moves Protenix cognate from 87.1 to 89.0. Neither is fatal and both are the "scope
   asserted where it is most read" pattern. **My first attempt at this check was wrong** — I
   filtered on E1+E2 and failed to reproduce, and the drop was right.

## 0.4 Two assets nobody has costed, because they are not in any ask document

**(a) The bulk control and the α5 point mutants are already built.**
`data/block_b/03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md` §1a enumerates the pipeline's
`partners.fasta` — 29 entries — and records that **25 of them were consumed by zero Block
B rows**. Among the unconsumed:

| entry | len | why it matters |
|---|---:|---|
| `ubiquitin` | 76 | mass-matched non-Gα bulk control, self-declared as such |
| `KaiB_2QKEE` | 91 | second bulk control, unrelated fold |
| `gcn4_leucine_zipper_33` | 33 | **helix-length** bulk control — the right size for the peptide rungs |
| `random_helix_40mer` | 40 | designed helix, no evolutionary partner |
| `arrestin_FL` | 15 | a *different biological* active-directing co-input, at peptide length |
| `arrestin_Ctail` | 41 | |
| `alphas_F376A_L388A_mutant` | 394 | α5 uncoupling point mutant, full subunit |
| `alphas_F376A_L388A_R380A_triple_null` | 394 | triple null |
| `alpha13 alphagust alphao alphai2 alphaz alpha11` | 350–377 | six further Gα subunits, never used |

`rebuttals/BLOCK_B.md` S1 asks for a bulk control and proposes candidates as if none
existed. Two mass-matched non-Gα chains, a helix-length decoy, and two designed
α5-uncoupling Gα mutants are already in the pipeline's own sequence file, hashed and
MSA-depth-audited (`03_msa_audit/msa_depth_report.md` lines 353–376). **The bulk control
is a dispatch, not a construction job.** This materially lowers the cost and the risk of
several `real` entries below.

Two of those entries are mislabelled and the audit says so: `partners.fasta:GASR` is the
gastrin receptor, not a Gα, and `partners.fasta:Nb60` carries the **Nb80** CDR3. Any
re-use must key on sequence hash, not header.

**(b) The five α5 C-termini are nearly a designed mutagenesis series already.** From the
same construct report, the last 11 residues:

| class | α5-CT (last 11) |
|---|---|
| Gs | `QRMHLRQYELL` |
| Gi | `IKNNLKDCGLF` |
| Gt | `IKENLKDCGLF` |
| Gq | `LQLNLKEYNLV` |
| G12 | `LHDNLKQLMLQ` |

**Gi and Gt differ at exactly one position** (N→E at position 3). Gi↔Gs differ at all
eleven. `N4-L5-K6` is conserved across Gi, Gt, Gq and G12 and broken in Gs. A per-position
series between Gi and Gs is 11 single substitutions, and the Gi/Gt pair is a
single-residue natural minimal pair that already exists in the cognate arm (OPSD is the
one Gt receptor).

---

# 1. What each block established, and what it failed to

## 1.1 Block A — sound, narrow, and mostly recomputable

**Established.** On 48 receptors (40 A, 4 B, 4 F) × 4 backbones × 2 arms × 25 predictions
= 9,490 predictions in hand, a co-folded cognate Gα drives active-state geometry, on all
four backbones, with a five-fold spread in magnitude (median TM6 tilt shift +1.05 Å on
Chai-1 to +5.31 Å on Protenix2) and pooled predicate-active rates moving 14.5–32.7% apo to
75.0–87.1% cognate (`results.tex:38–66`). It behaves as a switch: 111 of 160 apo cells
never fire on any seed, 108 of 159 cognate cells fire on every seed. The instrument was
scored on the reference set first (159/168 as expected) and every deviation classified.

**The best result in the block is the negative.** Receptor-specific activation amplitude
is not reproduced: NPxxY-axis slopes 0.04/0.37/0.18/0.26 against unity, three of four
intervals spanning zero (`results.tex:153–188`). A model retrieving a memorised complex
should reproduce that complex's amplitude; it does not. That is the strongest indirect
anti-memorization argument the project has, and it is an argument rather than a control.

**Failed to establish, or could not have.**
- No peptide arm, no ligand column at all in the schema. The design could not have
  answered either open title clause.
- The tilt axis has a reference-separation SD of 1.17 Å against NPxxY's 5.22 Å and goes
  negative on two backbones under Class-A restriction. It cannot resolve a slope. Half
  the two-instrument predicate is, on this population, an instrument with no dynamic range.
- The confidence headline is arm-pooling. Scoring apo *and* cognate rows against the
  **active** reference produced a "two of four backbones" shape that dissolves on
  conditioning: within the cognate arm all four are negative (−0.30, −0.43, −0.42, −0.16).
  Direction survives, shape does not, and the manuscript carries a `[PI]` saying so
  (`results.tex:189–249`).
- 15 of 63 checks do not reproduce; 21 discrepancy groups recorded, 17 found here and not
  flagged upstream, including a shipped CIF that is CFTR and a "confidently wrong"
  structure that is confidently right (`analysis/block_a/DISCREPANCY_REPORT.md` D18, D12).
- `FZD4` has no cognate arm at all — 4 apo cells, 100 rows, and nothing in the drop says
  so. The whole pre-check audit block (`A1_amino_acid_identity` … `A6_receptor_identity`)
  is all-NaN on 9,490 rows.

## 1.2 Block B — the best-designed block, and the decomposition is the paper's real result

**Established.** 40 Class A receptors × 4 backbones × 4 arms × 50 = 32,000 predictions,
every one of 640 cells exactly full. Predicate-active fraction rises monotonically apo
0.158 → decoy 0.558 → shuffled 0.809 → cognate 0.891, on all four backbones
independently. The rise is not threshold reclassification: within ±0.5 Å of the tilt cut
the cognate arm carries *less* mass than shuffled on three of four backbones, and the
difference lives in the far-inactive tail.

The decomposition is the contribution. Supplying any partner, even one whose α5 tail is a
composition-preserving permutation, accounts for **+0.400 [0.334, 0.464] — 55%**. The
decoy→cognate step, **+0.333 [0.242, 0.432]**, is the only contrast in the whole project
that isolates the α5 C-terminus with everything else held byte-identical (verified 40/40:
`decoy[:-11] == cognate[:-11]`, tail Hamming 7–11, composition preserved). Getting the
*family* right adds only +0.082 [0.047, 0.127].

**Failed to establish.**
- **The manipulated segment is eleven residues, not twenty-one.** Minimum partner length
  on any non-apo row is 350 aa, maximum 394; there is no arm below 350 and none at 21
  (`06_interface/interface_continuous.csv`, `n_partner_aa` over all 640 cells).
  `ligand_type`, `ligand_sequence`, `ligand_smiles` are NaN on 32,000 of 32,000.
- **No bulk control.** The 55% occupancy term is the largest of the three and the least
  controlled; nothing distinguishes a G protein from a protein. `yu2026domainmotion`
  (82 enzymes, nonbinder ligands reproducing the domain motion, training prior 40.3 pp
  against a ligand effect of 9.1–17.5 pp) is the published version of this objection and
  it is not yet in the `CLAIMS.md` threats table.
- **The decoy arm is confounded at the MSA.** Scrambling the tail also disrupts
  inter-chain MSA pairing at the same columns, and on Chai-1 the edit does not reach the
  model as aligned upper-case columns at all (`03_msa_audit/PHASE_1D_EXTENSION.md`).
  The surviving fallback ladder is apo → shuffled → cognate.
- **One stratum carries the identity-blindness conclusion.** Gs→Gi is powered at 20
  native-referenced receptors; Gs→Gq collapses to 3 with an interval spanning zero;
  Gi→Gs has none.
- **SC-B-2's per-backbone family shares reproduce from nothing** and one of them reached
  the manuscript (`DISCREPANCY_REPORT.md` D-B-6). `frame_36` resamples 24 clusters and
  every interval on it says 26.
- β and γ subunits are outside the input schema. **No block has ever supplied a
  heterotrimer.**

## 1.3 Block C — the design is better than the delivery, and the delivery is the problem

**Established, with scope withdrawn.** 36 receptors × 4 backbones × 3 ligand roles × 2
arms × 50 = 40,000 scored predictions exist. Agonist- and antagonist-occupied pockets
separate in the predicted direction on all four backbones (−0.306 to −0.137 Å on the
active-minus-inactive pocket-Cα RMSD difference). A **pre-registered** ordinal test,
locked before the campaign ran, recovers the same ordering on 65–87% of receptors. That
test could have failed and did not, and it is the strongest evidential object in the
block.

**Why it is not convincing, precisely.**
1. **The 2×2's factors are ligand class × reference state, not ligand × partner.** The
   apo-only filter was designed and never applied: the artefact records 2,800 and 2,300
   rows per cell, while apo alone would give 1,400 and 1,150. So the headline interaction
   pools both partner arms and cannot be attributed to the ligand
   (`results.tex:415–432`, `DISCREPANCY_REPORT.md` D-C-9).
2. **The activation predicate does not function on this panel** — floor-pinned apo,
   ceiling-pinned cognate, ~65% of cells unresolvable — so every Block C number is
   continuous pocket geometry and none is commensurable with a Block A or B rate.
3. **Almost nothing is independently checkable.** `analysis/block_c/DATA_REQUESTS.md` ask 1
   splits the block's checks 23 RECOMPUTED / 30 CONSISTENCY — 30 of them are the same
   number read from two shipped files and compared. `rows.tier3.v2.csv` is pinned by SHA in
   twenty places and shipped nowhere. Block B's family shares passed their own
   `matches_claim_sheet_bool` column while reproducing from nothing; a consistency check
   cannot catch a computation that was wrong identically in every file.
4. **The block refuted its own pre-registered applicability domain** — the slope ran
   negative — so what survives is an after-the-fact failure list.
5. **The one pose number is scoped to the only cell where two problems vanish**, and the
   ligand placement asymmetry is severe: on the 2×2's own 23 receptors, 35.85% of apo-arm
   agonist ligands are off-site against 2.00% of antagonist rows.
6. `flag_low_confidence` is False on all 40,000 rows and can never fire; `ligand_resname`
   takes six slot labels and identifies no molecule; eight receptors are missing an entire
   ligand role with no caveat.

**The thing Block C got right that nobody has noticed loudly enough: the crossing exists
and is scored.** 22,400 predictions cross ligand class with partner presence on 28
receptors, four backbones, 50 per cell. The crossing that no paper in 81 performs (E2.2)
has already run here. Only the export is missing.

## 1.4 Block D — the most honest block and the least usable

**Established, in prose.** Unsteered at 500 samples per cell, the four backbones are not
bistable — they are four different systems (Chai-1 100% active on β2AR apo where Boltz-2
is 0%). Four cells clear +50 points over the best other backbone, **and all four reproduce
on Block A's independent apo rows** — the only result in the project that survives a
change of corpus. Steering works in the active direction (cognate Gα ≥96% on 14 of 16
cells) and not in the inactive direction. MSA depth moves the predicate on all four
backbones, and on a second axis two of those four are degradation rather than steering.

**Failed.**
- **Zero row-level data for 42,180 predictions.** Twelve of twelve claims are PROSE-ONLY
  in whole or part. Every headline fraction and every slope interval is unverifiable.
  What could be recomputed was and it held — panel sizes, cluster counts, all six exact
  binomials, fifteen NPxxY distances from the deposited coordinates.
- **Every nanobody anchor predates every datable cutoff (2013–2020)**, so the inactive
  negative is not separable from a memorization-availability effect, and OpenFold-3's
  cutoff could not be dated at all.
- **The D2 ADRB2 active-Nb and inactive-Nb arms fed the same 125-aa sequence.** Both
  YAMLs carry sha256 `1406ad7ea26451…`; the manifest annotates the active subarm
  `partner_perturbation=placeholder_nb80_from_nb60_5jqh` and the substitution never
  landed (`data/block_b/03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md` §1a, cross-block
  audit). Any sentence contrasting those two arms is contrasting one arm with itself.
- The directed tier rests on four receptors. `tier_d3_panel.csv` has an unquoted comma
  and will not parse with pandas defaults.

---

# 2. Four cross-cutting constraints the redo has to design around

**C1 — The instrument grades with the labelling it was calibrated on.** Thresholds derive
from 80 annotated reference rows (`methods.tex:67`, `methods.tex:95`), and whether those
rows were selected by crystallographic tier or by curated label is an open `[PI]`
(`methods.tex:117`). `paajanen2026activation` finds deposited entries "whose state of
activity was originally interpreted incorrectly", so the annotation is not a fixed point.
Recalibrating off-panel is decided; §0.2 sizes it and names the imbalance it will hit.

**C2 — The panel is a sample with an unstated frame.** No selection rule exists anywhere
in any drop (`rebuttals/BLOCK_A.md` Q-A1). We can now say what it *is*: 40 of the 64
Class A both-state slugs, and every one of the 40 qualifies. A census rule is available
and stronger than the current silence.

**C3 — Most of what we publish cannot be recomputed.** One block shipped nothing, one
shipped a state-free census, one ships no state column. A delivery contract has to be part
of the redo's design, not a request appended to it (E6.1).

**C4 — The corpus contains a wet-lab result that the naive peptide claim contradicts.**
`tran2026nanogs`: a **stapled 15-mer** Gαs α5 C-terminal peptide stabilises active-like
β2AR with efficacy comparable to Nb80 — **only with agonist present**, and the *unstapled
linear* peptide does nothing; the free peptide is a random coil by CD. Verbatim, p.8:
"In absence of agonist, both peptides 2 and 4, as well as Nb80 showed only minor responses
in the bimane assay suggesting they were unable to stabilize an active receptor
conformation alone." A co-folding model has no solution-phase equilibrium and is not
obliged to agree — but the length ladder must carry a **helicity readout on the supplied
peptide** (Block B already measures `partner_tail11_helicity_frac`) or the result cannot
be discussed against this paper. Do not design the ladder without it.

---

# 3. The experiment catalogue

Novelty grades are from a full sweep of `lit/INDEX.md` (81 papers) run for this document,
audited by the lit session on 2026-09-11
(`lit/analysis_review/REDO_CATALOGUE_NOVELTY_CHECK.md`) and corrected here. `DONE` means do
not claim it. Costs assume the conventions in the header.

## 3.0 How a novelty claim is counted here, and why the first version counted wrong

**"Zero of 81" was the wrong denominator and it is now banned in this document.** The field
that records factor crossing, `input_factor_design`, is populated on **11 of 81 notes** and
appears in `INDEX.md` **zero times**; `lit/SCHEMA.md` is explicit that its absence on the
other 70 means *not yet backfilled*, never `NOT ADDRESSED`. So "zero of 81" was really
"zero of the 11 where anyone looked" — a claim a referee can dismantle.

**The rule.** Every absence claim is stated as *"zero of the N papers that could hold it"*,
with N named and derived from a tag that is actually exercised. For the ligand × partner
crossing, N = **7** — the notes carrying both `ligand-driven` and `partner-driven`. The
claims survive on the real denominator, which is the point of restating them.

**The trap, in the corpus's own words.** `vo2026fiducials`'s note records that despite
carrying `msa-subsample`, `ligand-driven` and `partner-driven` together, the paper "crosses
none of them — it is the clearest demonstration that a tag combination in `INDEX.md` must
not be read as a crossing." Co-occurrence is a candidate list, not a finding.

**Three counting bugs of my own, recorded because they are the reason for the rule.**
Recounting the 7-paper denominator, my first pass grepped whole note bodies and returned
**39** (prose mentions, tag glossaries and negations all matched); my second parsed only
backticked tags inside `## Tags` and returned **6**, missing `chiesa2025templatebias`
because that note stores its tags in a fenced code block rather than backticks. Only the
third pass, handling both formats, returned **7** and matched the lit session name for
name. **Two of three attempts at a one-line count were wrong.** Two notes
(`cheng2026af3cluster`, `xing2025purified`) carry no `## Tags` section at all, so the true
statement is *7 of the 79 tagged notes* — and `xing2025purified` is untagged while being
the paper the depth rows in Group 8 lean on hardest, which is worth knowing before quoting
any tag-derived denominator about depth.

**One caution I was given that turned out to be void, recorded so it is not re-raised.**
The coordinator warned that the corpus might have moved during the day and that a
counterexample from a new note would outrank any row here. The lit session checked:
**nothing moved.** No note carries a 2026-09-11 mtime; the newest is `vo2026fiducials` at
2026-09-10 20:17. Every novelty line in this document was written against the corpus as it
stands.

**One pending candidate that could change a claim in Group 8.** `factors-crossed` is tagged
on exactly one paper in `INDEX.md` (`mitjavila2026afsample2t`, line 448). A second note,
`cheng2026af3cluster`, discusses the tag and explicitly withholds it — "**Do not tag
`factors-crossed` until the PDF is read**" — because it is an abstract-level note. It
combines MSA clustering with co-folded binders. **If that PDF is read and the tag lands,
E8.1's "exactly one" becomes "two", and the second one is on an AF3-lineage backbone.**
Worth reading before the depth rows are quoted in a paper.

## Group 0 — the instrument

### E0.1 — Recalibrate the predicate on the off-panel Class A population
- **Question.** Where do the two thresholds sit when they are fitted on structures the
  panel does not contain?
- **Closes.** The first methodological objection a referee makes: you built the ruler from
  the same annotations you grade with (`methods.tex:95`).
- **Design.** 726 off-panel Class A Active/Inactive structures across 155 receptor
  entries. Measure d(Y5.58 OH, Y7.53 OH) and d(2×46 Cα, 6×37 Cα) on every one. Report:
  ROC over the two axes jointly and separately, the midpoint threshold, a
  balanced-objective threshold, and the sensitivity of both to a resolution floor and to
  a 1:1 active/inactive reweighting. **The set is 611 active against 115 inactive; state
  the balancing rule before fitting.** Hold out the 610 on-panel structures as the
  application set.
- **Cost.** `free*` — no inference, but ~726 downloads, chain selection and generic-number
  mapping. Budget days, not hours.
- **Depends on.** Nothing. **Everything else that reports a rate depends on it.**
- **Novelty.** `paajanen2026activation` DONE at scale (1,351 Class A structures, learned
  PC1, GMM threshold −1.72 ± 0.44, 10,000 bootstrap resamples) — but it is **not
  reimplementable from the paper**: no weight vector, no residue list, no repository.
  `khaleq2026hyaline` DONE as a supervised classifier (1,590 structures, AuROC 0.99) — but
  its decision threshold is **not reported** and it has **never been run on a predicted
  structure**; its authors propose exactly our use case as future work. Nearest:
  `paajanen2026activation`. Our claim is a *reimplementable, per-axis, off-panel-calibrated*
  predicate, not a new idea.

### E0.2 — Concordance against an independent state index
- **Question.** Where does a two-distance geometric rule disagree with a learned
  coordinate, and on what kind of structure?
- **Closes.** Block B S4, reframed: turns the weakest methodological point into a result.
- **Design.** Score the off-panel calibration set and the reference set on (a) GPCRdb's
  own Active/Inactive annotation, (b) the PIF connector as a third geometric axis, and
  (c) `paajanen2026activation`'s coordinate *if* it can be reconstructed. Report the
  disagreement rate. **No study in the corpus reports such a rate** —
  `intro.tex:325–332` already says so.
- **Cost.** `free*`, rides on E0.1's measurement pass. (c) may be impossible; say so.
- **Depends on.** E0.1.
- **Scope limit on option (c), added after the lit audit.** **`paajanen2026activation`
  excluded arrestins** — "Arrestins have not been included in the analysis because there is
  not enough data to influence the graph" (p.2) — and excluded intermediates for the same
  reason. So (c) cannot check an arrestin arm (E7.6) and cannot check E0.3's intermediates.
  Its coverage is Class A active/inactive G-protein-relevant structures and nothing else.
  Say which arms have an independent check and which do not, rather than implying all do.
- **Novelty.** ADJACENT. The indices exist; the cross-validation does not.

### E0.3 — Admit a third state
- **Question.** Should the predicate be binary at all?
- **Closes.** `georgiou2025heterogeneity`'s rheostat objection, which the introduction
  already concedes (`intro.tex:315–323`): "a single hard cut-off imposed on a continuum
  can destroy the signal it is meant to detect."
- **Design.** The snapshot holds **21 Class A Intermediate structures**. Measure them on
  both axes; report where they fall relative to the two cuts. If they sit between, the
  predicate has an interpretable middle band and the paper can report three states. If
  they scatter, say that too — it bounds what the instrument can express.
- **Cost.** `free*`, 21 structures, rides on E0.1.
- **Commit to what n=21 can conclude, before measuring.** The one paper that faced this
  exact n **chose not to report**: `paajanen2026activation` dropped intermediate and other
  states because "their number is too low to be distinguished from the graph" (p.2). That
  is not a reason to skip the measurement — it is a reason to state in advance what a
  21-structure result licenses. A defensible pre-commitment: *if ≥15 of 21 fall strictly
  between the two cuts, report a middle band as an instrument property; otherwise report
  the scatter and make no three-state claim.* Without that written first, 21 points will be
  read whichever way the plot happens to look.
- **Novelty.** `georgiou2025heterogeneity` and `paajanen2026activation` both describe
  intermediates; **nobody scores them through a fixed predicate**, and paajanen declined to
  at this n. OPEN, small, and honestly underpowered.

### E0.4 — Report the axes continuously and the predicate as a derived call
- **Question.** How much of every result is threshold placement?
- **Design.** Every headline re-reported as (i) the continuous two-axis distribution,
  (ii) the call at the fitted threshold, (iii) the call swept across a threshold band.
  Block C already demonstrates the failure mode this prevents: the predicate saturates and
  the block had to abandon it mid-campaign.
- **Cost.** `free` on A and B today.
- **Novelty.** Not a novelty claim; a robustness one.

### E0.5 — Decide the class B and class F instrument
- **Question.** Is there a predicate for these, or are they scope decoration?
- **State.** For 4 class B receptors rule (2) is replaced by a TM6 kink angle below
  159.95°; for 4 class F both substitutions are unestablished and tilt is used alone
  (`methods.tex:53–63`). Neither is calibrated. FZD6 has no inactive structure in GPCRdb
  at all. Class B1 has 148 entries and class F 34 in the snapshot.
- **Options.** (a) drop B and F and say the work is Class A; (b) calibrate a class B
  predicate on the 148 B1 entries as a separate instrument with its own result; (c) keep
  them as declared instrument scope with no claim, which is the status quo.
- **Cost.** (a) free, (b) `free*`.
- **Novelty.** `hilger2020gcgr` supplies the biology — in class B, agonist alone produces
  no TM6 opening and the active state appears only on G-protein engagement. That makes
  class B the *sharpest* possible venue for a partner-length ladder (E7.2), which argues
  against simply dropping it.

## Group 1 — partner length: the centrepiece

### E1.1 — The α5-CT length ladder
- **Question.** How much of the transducer do the models need? Is the response to partner
  length graded or a step?
- **Closes.** Title clause 1 outright, and it is the only experiment that does.
- **Design.** Rungs, nested so each differs from its neighbour in one way:

  | rung | chain B | residues |
  |---|---|---:|
  | R0 `apo` | none | 0 |
  | R1 `ct11` | last 11 of cognate Gα | 11 |
  | R2 `ct21` | last 21 of cognate Gα | 21 |
  | R3 `a5helix` | the whole α5 helix | ~26 |
  | R4 `a5plus` | α5 helix + the preceding β6 strand | ~45 |
  | R5 `a5null` | full cognate Gα with the **entire α5** replaced, not just the tail | 350–394 |
  | R6 `cognate` | full cognate Gα | 350–394 |

  R0 and R6 already exist on 40 receptors (Block B). **R5 is the bulk control that S1
  asked for and the rung that separates "a Gα-shaped object" from "the α5 contact"** —
  `rebuttals/BLOCK_B.md` S1 names it as the third candidate and the one closest to what
  the pipeline already builds. `n_partner_aa` must be emitted per cell so every rung is
  verifiable from the data rather than from the dispatch note.
- **Specification warning.** Express every rung as *"the last N residues of the cognate
  subunit"*, never as a fixed residue range — see §0.3 item 4.
- **Cost.** `real`. Five new rungs (R1–R5) × 40 receptors × 4 backbones × 50 =
  **40,000 predictions**. On the 64-receptor census: **64,000**. Single-backbone pilot
  (Boltz-2, 40 receptors, 5 rungs): **10,000**.
- **Depends on.** E0.1 for the threshold; nothing else. Can be dispatched before
  calibration finishes if the axes are shipped continuously.
- **Novelty.** **OPEN, and it is the safest novelty claim available.** The corpus records
  the absence twice and independently: `ye2026multistatebias` `controls_run` — "ABSENT —
  reduced or partial partner construct … No truncated, decoy or scrambled partner is run"
  (p.18), and its `unresolved` field notes the words "nanobody", "mini-G", "α5" and
  "alpha5" do not occur in the paper at all; `chiesa2025templatebias` — "the co-input is
  the whole Gα subunit or heterotrimer, not a 21-residue α5 C-terminal peptide, so the
  paper cannot separate the α5 contact from the rest of the interface." **Two further
  recorded absences were added by the lit audit and verified here**, which makes four
  independent ones: `heo2022multistate` — "ligand, nanobody, G-protein and arrestin are
  never used as inputs"; and `miglionico2026atlas`, the largest partner-supplying study in
  the corpus (10,413 receptor–Gα pairs, 801 receptors), whose note states the absence so it
  is checkable — "No partial G-protein construct was used as a prediction input … No α5
  helix, no α5 C-terminal peptide, no mini-G, no nanobody, no scFv, no G-protein mimetic
  appears in the input protocol (pp19–20)". Nearest: `chiesa2025templatebias`. **Four
  independent recorded absences is as strong as this corpus gets.**
- **Must carry.** Per-rung helicity of the supplied chain (C4), per-rung engagement depth,
  and the pLDDT of the supplied chain — `tran2026nanogs` predicts a disordered, inactive
  free peptide and the model's own confidence on that chain is the closest in-silico
  analogue of the CD measurement.
- **A design threat to the ladder, which is a costing question and not a novelty one.**
  `junker2026peptidedesign` is the corpus's only **length-stratified** analysis of peptide
  co-inputs against co-folding predictors — 113 GPCR peptide/protein complexes, peptide
  lengths **3–137 aa**, 50 seeds, three predictors. It does not touch E1.1's novelty
  (length is an observational covariate there, the generative arm pins length to the
  native, and receptor state is never assessed), but it carries two warnings. (i) Stratified
  ≤50 vs >50 residues, "100% of AF2IG-predicted, 82.1% of RF3-predicted and 35.5% of
  Boltz-2-predicted GPCR–protein ligand complexes achieve a DockQ score below 0.23" (p5) —
  **our ladder crosses that boundary between R4 (~45 aa) and R5/R6 (350–394 aa)**, so the
  two ends sit in different placement-accuracy regimes and a graded response to length
  could be a placement artefact rather than a signal-content effect. The engagement-depth
  column is the mitigation and is hereby **required for interpretation, not merely
  carried**. (ii) Comparing an interface score across peptides of different lengths "is
  hindered" (Methods, p16), which is why they chose DockQ — **whatever interface measure
  the ladder reports must be defined consistently from 11 to 394 residues, or reported
  within-rung only.** The redesign this implies belongs to `redo/spec/RUN_MATRIX.md`;
  recorded here so it is not lost.

### E1.2 — Bulk control, crossed at two rungs
- **Question.** Is the 55% occupancy term specificity or literal occupancy?
- **Closes — RESTATED 2026-09-11; the first version contradicted its own Novelty line.** It
  said `yu2026domainmotion` "is the published form of it", which cannot stand beside a
  Novelty line reading OPEN. **The Novelty line is the correct one.** yu is 82 **enzymes**
  from DynDom, open↔closed **domain motion**, AF3 with **no templates and no MSA**, and its
  control is a **nonbinder small molecule** — a decoy of the same chemical class as the
  binder. E1.2's control is a mass- and shape-matched **non-Gα protein chain** on GPCRs read
  on receptor state. Different co-input class, different system, different state definition.
  **E1.2 therefore tests whether yu's finding extends to protein co-inputs**, which is a
  stronger and more interesting framing than confirming it.
- **Design.** At the peptide rung and at the subunit rung, a mass- and shape-comparable
  non-Gα chain: `gcn4_leucine_zipper_33` (33 aa, helix, peptide-scale) against R2/R3, and
  `ubiquitin` (76) or `KaiB_2QKEE` (91) against a truncated subunit; `random_helix_40mer`
  (40) as a designed-helix arm with no evolutionary partner. **All four sequences already
  exist in the pipeline's `partners.fasta` and were consumed by zero rows.**
- **Cost.** `real`. Two arms × 40 receptors × 4 backbones × 50 = **16,000**. One arm on
  one backbone as a pilot: **2,000**.
- **Depends on — CORRECTED.** This row previously said "Nothing." **It depends on E4.2, and
  on yu's own design.** yu's decisive covariate is not the ligand but the **apo:holo ratio
  in the PDB**: the trigger ligand moves the holo-like fraction by 11.9% and 9.1% in their
  Groups 1 and 2, against a **40.3-point gap attributable to training composition alone**,
  rising to 17.5% in Group 3 where the memorised prior is weak. Its recorded `crossings:`
  line is the point — the ligand axis is crossed with a training-set-composition
  stratification, *and that crossing is what produces the result*. **A bulk control run
  without stratifying each receptor by its deposited active:inactive ratio is
  uninterpretable**: a null could be the control working or the prior swamping it. Run and
  analyse E1.2 and E4.2 together. (The run-matrix agent has been asked to re-cost with that
  stratification; the stratum sizes are theirs to set, not this document's.)
- **Novelty.** **OPEN for protein partners.** No paper runs a scrambled or decoy *protein*
  partner. The ligand analogue is DONE and is the threat: `yu2026domainmotion` (nonbinder
  ligands reproduce the motion; pLDDT does not separate them), `masters2025physics` (pose
  survives a pocket made incapable of binding), `bret2025boltz2docking` (Boltz-2's
  classification insensitive to binding-site mutation and sometimes to target exchange).
  `bret2025boltz2docking`'s note anticipates our design explicitly. Nearest:
  `yu2026domainmotion`.

### E1.3 — Composition-matched and order-matched controls at peptide length
- **Question.** At peptide length, where nothing but the tail is left, does sequence
  identity finally matter?
- **Why it is sharper than Block B's decoy.** In Block B the scramble sits on the tail of
  a 354-residue subunit, so 97% of the partner is unchanged and bulk dominates. Strip the
  bulk and the scramble is the *entire* partner. **This is the experiment that converts
  the decoy arm from confounded to decisive.**
- **Design.** At R2 (21-mer): `wt`, `scrambled` (permutation, composition preserved),
  `reversed`, `poly-Ala of matched length`, `matched-composition random`. Five arms.
- **Cost.** `real`. Four new arms × 40 × 4 × 50 = **32,000**; on one backbone **8,000**.
- **Depends on.** E1.1 R2 existing (can be dispatched together).
- **Novelty.** OPEN. Nearest: `tran2026nanogs`, whose `controls_run` records "ABSENT —
  scrambled-sequence peptide | … Every negative control is structural … none scrambles the
  sequence while preserving length and charge."
- **Caveat that must be designed for.** At 21 residues the partner chain's MSA is
  essentially empty, so scramble and wild type differ in sequence but not in alignment
  depth — which *removes* the Block B confound rather than repeating it. Verify by
  auditing the partner MSA as `03_msa_audit/PHASE_1D_EXTENSION.md` did.

### E1.4 — Family swap at peptide length
- **Question.** Block B found the models nearly blind to partner family (+0.082 of a 0.733
  rise). Is that blindness real, or is it bulk drowning the signal?
- **Design.** Cross receptor coupling class × supplied α5-CT class at R2. Minimal version:
  Gi-coupled receptors given the Gs 21-mer and Gs-coupled receptors given the Gi 21-mer,
  against cognate. The panel supports it — cognate classes are Gi 24, Gq 10, Gs 5, Gt 1.
- **Cost.** `real`. One swap arm × 40 × 4 × 50 = **8,000**.
- **Depends on.** E1.1 R2.
- **Novelty.** ADJACENT to Block B's own shuffled arm (which changes family, scaffold,
  length and tail at once) and OPEN against the corpus as a *prediction* experiment.
- **It has a wet-lab twin, and citing it makes the arm much stronger.**
  `miglionico2026atlas` ran **11 Gαq chimeras with different Gα C-termini swapped in**, read
  by TGFα-shedding (Fig 4C, p32), **with a C-terminally truncated Gαq (ΔC) control** that
  rules out the signal coming from the Gαq scaffold; for QRFPR, predicted against measured
  gives **Pearson r = 0.66, P = 0.026** (p9). **That ΔC control is the wet-lab analogue of
  E1.1's R5 rung**, and the chimera series is the wet-lab analogue of this arm. Our
  experiment is the in-silico version of a published assay with a published effect size —
  which is a better position than claiming virgin ground.
- **The trap in citing it.** Those chimeras are **wet-lab TGFα-shedding reagents, not model
  inputs**; miglionico's own note flags them as a near-miss that "must not be mistaken for"
  a prediction input. Every one of its 10,413 predictions used the **full heterotrimer**
  and **no ligand of any kind**, deliberately. Cite the chimeras as biology, never as
  precedent for a truncated co-input.
- **Honest risk.** Gs-coupled receptors number 5. Powering the reverse direction needs
  panel extension (E7.5) — Block B S6 records that Gi→Gs currently has *zero*
  native-referenced receptors.

### E1.5 — Per-position scan inside the supplied α5-CT
- **Question.** Which residues carry the effect, and does the model's answer match the
  structural biology?
- **Closes.** The paper has **no residue-level account of anything** across all four
  blocks — Block C's `s4_bw_decomposition.json` is the only residue-level analysis named
  anywhere and it never shipped.
- **Design.** On a reduced receptor set (8–12 receptors, one backbone), alanine-substitute
  each of the 21 positions in turn, plus the 11 Gi→Gs substitutions as a second series.
  Report per-position Δ(active fraction). Anchor against `hilger2020gcgr`'s structure-guided
  alanine scan and against the two α5 point mutants already in `partners.fasta`.
- **Cost.** `real` but scalable. 21 arms × 10 receptors × 1 backbone × 20 samples =
  **4,200**. At 50 samples and 4 backbones it is 84,000 — do the cheap version first.
- **Depends on.** E1.1 (a length must be chosen first), and see the retrieval confound
  below, which constrains *which* length.
- **Novelty.** **OPEN**, and the sweeps behind it are worth quoting because they are
  unusually clean: `/deep mutational|saturation mutagenesis|mutational scan/` returns
  **0 of 81**; `/alanine scan|Ala scan/` returns 1 (`hilger2020gcgr`, wet lab);
  `/per-position|position-by-position|residue-by-residue/` returns 5, none on a partner.
  Nothing in the corpus scans a *supplied* partner residue-by-residue and reads receptor
  state.
- **Both supports the first version named are weaker than they looked, and the row now says
  why.** `masters2025physics` mutates the **receptor's own pocket**;
  `bret2025boltz2docking` alanine-mutates the **target's** binding site and reads an
  **affinity classifier**, not a structure and not a state. Both are receptor-side
  self-mutation, so neither is evidence about a supplied partner.
- **The paper whose protocol to copy, missing from the first version.**
  **`waymentsteele2024cluster` is the corpus's one per-position scan read on a
  conformational state**: the KaiB_RS mutation scan runs "all combinations of 8 … point
  mutations most enriched from FS state analysis" with **no MSA, 12 recycles, model 1**
  (p4, p17), and three mutations — I68R, V83D and N84R — flip the predicted state. It is a
  *self*-scan, not a supplied partner, so E1.5's novelty is untouched. It is the design
  precedent, and the "no MSA" choice was not incidental.
- **The confound this arm must be designed around, and it decides the length.**
  `masters2025physics` states its own null's mechanism: when small mutations are
  introduced, "the sequence alignment and template search will return exactly the same
  results as before" (p.9) — **the mutated sequence retrieves the wild-type MSA and
  template.** So a null from mutating positions inside a supplied partner whose alignment
  is unchanged is a **retrieval artefact, not model insensitivity**. The mitigation is
  already implicit in E1.3: at 21 residues the partner's MSA is essentially empty. **E1.5
  must therefore run at peptide length, or audit the partner MSA per arm** the way
  `data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md` did. `waymentsteele2024cluster` ran its
  scan with no MSA for exactly this reason.
- **Why this is still the most interesting entry in the catalogue.** It is the only
  experiment that produces a *mechanistic map* rather than another fraction. But the case
  is now narrower and more honest: the two published "models do not respond to mutation"
  results are receptor-side, so they are a weaker prior than the first version implied,
  and `waymentsteele2024cluster` is a counter-prior — a self-scan where three point
  mutations *did* flip the predicted state. The expected outcome is therefore genuinely
  uncertain, which is the best reason to run something.

### E1.6 — The Gi/Gt single-residue natural pair
- **Question.** Is the instrument sensitive to one residue?
- **Design.** Gi `IKNNLKDCGLF` and Gt `IKENLKDCGLF` differ at one position. Supply each to
  the same receptors at R2 and at R6. Free half: OPSD is the only Gt receptor on the
  panel, so the Gt→Gi direction on 24 Gi receptors is a one-arm add.
- **Cost.** `real`, one arm, **8,000**; or 2,000 on one backbone.
- **Novelty.** OPEN; a sensitivity floor for E1.5 rather than a headline.

### E1.7 — Gα alone versus heterotrimer
- **Question.** Every block supplies Gα alone. The deposited active references are
  heterotrimers. Does adding Gβγ change the receptor's predicted state, or only the
  interface?
- **Closes.** A referee comparing our input to our reference will ask. It also bears on
  reference-set curation: the Class A active reference set contains **no native
  heterotrimeric Gs complex** (Block B's own audit, `rebuttals/BLOCK_B.md` S5).
- **Design.** Add a `heterotrimer` rung (Gα + Gβ1 + Gγ2) at the top of the ladder. `Gg2`
  (71 aa) is already in `partners.fasta`.
- **Cost.** `real`, one arm, **8,000**. Requires a three-chain input schema — Block A's
  FASTA schema is single-partner, so this is a harness change, not only a dispatch.
- **Novelty.** ADJACENT. `ye2026multistatebias` and `mitjavila2026afsample2t` both supply
  heterotrimers; neither contrasts them against Gα alone. Nearest: `ye2026multistatebias`.

### E1.8 — Uncoupling point-mutant Gα arms
- **Question.** Does a full subunit that cannot couple still open TM6?
- **Design.** `alphas_F376A_L388A_mutant` and `alphas_F376A_L388A_R380A_triple_null`, both
  394 aa, both already in `partners.fasta`, both consumed by zero rows. Run against the 5
  Gs-coupled panel receptors, extended by E7.5.
- **Cost.** `real`, small: 2 arms × 5 receptors × 4 backbones × 50 = **2,000**; worth
  extending to more Gs receptors.
- **Novelty.** OPEN. This is the partner-side analogue of `masters2025physics` and
  `bret2025boltz2docking` and it is a sharper control than the scramble because the
  mutation is biologically motivated rather than combinatorial.

### E1.9 — Coevolution versus sterics: partner MSA on and off
- **Question.** Does the partner's effect survive when the model has no alignment for it?
- **Design.** At R6 (full Gα) and at R2 (21-mer), run with paired MSA enabled and with the
  partner chain supplied as a single sequence. Block B establishes that pairing is on by
  default and that the α5-CT columns are audited
  (`03_msa_audit/PHASE_1D_EXTENSION.md`). If the effect survives MSA-free, it is steric
  or structural; if it collapses, it is co-evolutionary.
- **Cost.** `real`, 2 arms, **16,000**; or 4,000 on one backbone.
- **Novelty.** ADJACENT. The MSA-mechanism debate is mature but entirely about the
  *receptor's* alignment: `waymentsteele2025reply` (column shuffling ⇒ local coevolution),
  `lee2025seqassoc` (sequence association, not coevolution), `xing2025purified` (purity,
  not depth), `feldman2026alphainterp` (the pair track is the causal substrate). **Nobody
  asks it of a protein partner.** Nearest: `feldman2026alphainterp`.
- **Bonus.** This retrospectively explains the Block B decoy confound rather than leaving
  it as a caveat.
- **Not to be confused with Group 8.** This entry varies **pairing** on the partner chain,
  binary, at two rungs. **Group 8 varies the depth of the receptor's own alignment**, which
  is a different factor with a different literature and a different open question. Both
  should be run; neither substitutes for the other, and a design document that lists only
  one of them has an MSA gap.

## Group 2 — the ligand axis

### E2.1 — Export the state call on Block C's existing predictions
- **Question.** What does the predicate say on 7,000 apo × agonist and 7,000 cognate ×
  agonist predictions?
- **Closes.** Title clause 2, at least partially, with **no new inference**.
- **Design.** A per-cell predicate table — `receptor_slug, backbone, arm, ligand_role, n,
  n_predicate_active, frac_predicate_active`, plus medians of both axes. At most 864 rows.
  Better: ship `rows.tier3.v2.csv` and we compute it.
- **Cost.** **`free (them)`.** The predictions are scored. The file is SHA-pinned in
  twenty places.
- **Depends on.** An instruction, not data: Block C's dispatch forbids connecting the
  block to two-state generation and Flag C-3 forbids quoting a binary rate for a
  *ligand-class discrimination* claim. Clause 2 is neither. Somebody upstream has to rule.
- **Novelty of the resulting claim.** ADJACENT, not open. `ye2026multistatebias` already
  reports that small-molecule ligands move predicted state weakly and inconsistently
  (β2AR, n=1); `vo2026fiducials` reports the opposite experimentally — agonist alone drives
  β2AR TM6 nearly fully out with the Gs α5 adding under 1 Å. **An "agonist alone does not"
  sentence is a confirmation at scale, not a discovery, and must cite both.**

### E2.2 — The real 2×2: ligand presence × partner presence
- **Question.** Do the two inputs compose? Additively, redundantly, or synergistically?
- **Closes.** The second half of title clause 2 and the strongest referee question after
  the bulk control.
- **Design.** Four cells — apo/no-ligand, apo/agonist, cognate/no-ligand, cognate/agonist —
  on one panel, one predicate, with the interaction term estimated and its interval
  reported. Three of the four already exist across blocks but **not on one panel with one
  scorer**: Block B has apo and cognate with no ligand; Block C has apo/agonist and
  cognate/agonist on 35 receptors. A unifying run is 1 arm if Block C's panel and scorer
  are reused, 4 arms if not.
- **Cost.** `real` if re-run: 4 cells × 28 receptors × 4 backbones × 50 = **22,400**.
  Potentially **`free (them)`** if Block C's existing 22,400 can be re-exported with state
  plus Block B's apo/cognate joined — but the two campaigns have different scorers,
  different panels and different reference sets, and `CLAIMS.md` forbids comparing a Block
  C number against a Block A/B predicate rate. **Re-running it clean is the honest option.**
- **Novelty — OPEN, restated on a real denominator (see §3.0 below).** A ligand × partner
  crossing can only exist in a paper that holds both handles. **Exactly 7 of 81 notes carry
  both `ligand-driven` and `partner-driven`** — recounted independently here — and **none
  of the seven crosses them**: `georgiou2025heterogeneity` (review),
  `tejero2024opsin` and `hilger2020gcgr` (no prediction pipeline),
  `chiesa2025templatebias` (**partner × ligand HELD** — the ligand is never removed),
  `ye2026multistatebias` (**CONFOUNDED** — β2AR receives agonist *and* Gαβγ together, with
  no agonist-free partner condition, p.18), `vo2026fiducials` (crosses none of them), and
  `ku2026promise` (below). **Zero of the seven that could hold it.**
- **`ku2026promise` is the strongest ADJACENT and the first version did not cite it.** It
  runs **both** co-input types against the same five models (AF3, Boltz-1, Boltz-2, Chai-1,
  BioEmu), each conditioned present/absent — but keeps them in **separate, non-overlapping
  sets**, a "ligand-induced set" and a "protein-induced set", scored with different success
  criteria. Its note draws the consequence: this is "support for treating partner-induced
  and ligand-induced effects as different problems". **That strengthens the OPEN call
  rather than weakening it** — a paper that held both handles and both model families still
  did not cross them. A referee who knows ku will ask; the row should answer first.
- **`suzuki2026conforflux` — citation corrected.** The p.21 sentence is verbatim: "With
  n=10 targets and across-target standard error ∼0.6 Å, we cannot resolve non-additivity
  between the two factors." But **"the two factors" are two internal scaling terms of the
  steering equation** — noise level and kernel saturation, Table 10 p22 — **not a ligand
  and a partner.** As the first version wrote it, a reader would take it for a failed
  co-input attempt. The honest and stronger sentence is: **no paper in the corpus even
  attempts an interaction estimate between two biological co-inputs, and the corpus's only
  non-additivity test is between two algorithmic hyperparameters and is underpowered.**
  A sweep for interaction language across all 81 notes returns 11, and the ANOVAs among
  them are on representation choice (`ferguson2026deorphann`) and wet-lab geometry
  (`matic2023gpcrome`).
- **Nearest.** `ku2026promise` (both handles, separate sets); `mitjavila2026afsample2t`
  (the corpus's only `factors-crossed` paper, and it crosses MSA masking × partner with no
  ligand channel).

### E2.3 — Efficacy ladder
- **Question.** Is the pocket response graded with pharmacological efficacy, or binary?
- **Design.** Inverse agonist → neutral antagonist → partial agonist → full agonist, at
  fixed partner condition. Block C has three roles (`full_agonist`, `neutral_antagonist`,
  `decoy_lig`) and no partial and no inverse agonist. `georgiou2025heterogeneity` supplies
  the expectation: inverse agonist → S1/S2, partial → I2, full agonist shifts toward
  active but does not reach it alone (p.21).
- **Cost.** `real`, 2 new roles × 28 receptors × 4 backbones × 50 = **11,200**; plus
  curation of inverse-agonist and partial-agonist ligands, which is the harder half.
- **Novelty.** OPEN. No paper varies pharmacological class across a GPCR panel and calls
  state with a fixed predicate. Nearest in kind: `kohlhoff2014gpcr` (MD, one receptor,
  agonist / inverse agonist / apo — and its apo arm does not reach active).

### E2.4 — The agonist-versus-decoy-ligand result
- **Question.** Does a ligand known not to bind reproduce the conformational change?
- **Design.** Block C ran **14,400 `decoy_lig` predictions** (7,200 per arm) and reports
  nothing on them; `task_A_v2_agonist_vs_decoy_apo_same_complex.json` is named and does
  not ship.
- **Cost.** **`free (them)`.**
- **Novelty.** The *question* is DONE and is the sharpest published challenge to this
  paper: `yu2026domainmotion`, 82 enzymes, 500 AF3 models per condition, no templates —
  nonbinders reproduce the motion, the training prior (40.3 pp) is 3–4× the ligand effect
  (9.1–17.5 pp), and pLDDT does not discriminate. **A referee who knows that paper will
  ask for exactly this arm, and we have run it and not looked at it.** The answer must be
  quantitative and must cite them by name. `yu2026domainmotion` is still not in
  `CLAIMS.md`'s threats table.

## Group 3 — confidence

### E3.1 — Restate the confidence result arm- and receptor-conditionally
- **Question.** Does confidence track *which structure is right*, or only *which receptor
  is easy*?
- **Design.** Recompute every pLDDT correlation within arm and within receptor. The
  recomputation exists (`analysis/block_a/DISCREPANCY_REPORT.md` D-A-25): pooled across
  seeds confidence separates correct from incorrect calls at AUC 0.60–0.96, **and that
  evaporates when receptor is controlled**. The manuscript sentence merges two claims.
- **Cost.** `free`, on 9,490 rows in hand.
- **Novelty.** The headline is **DONE many times over** — `bryant2024cfold`,
  `ye2026multistatebias`, `sun2026kinconfbench` (wrong-state structure ranked first in
  >11% of cases), `schafer2025confounds`, `junker2026peptidedesign` (PAE over-estimates
  for misplaced GPCR peptides in all three predictors), `yu2026domainmotion`,
  `ku2026promise`, `kalakoti2025afsample2`. **Frame clause 3 as confirmation on a new axis,
  not as discovery.** What is genuinely unreported is the *re-aggregation* finding — a
  confidence metric changing sign between whole-complex and anchor grain (Protenix2 +0.33
  → +0.07; OpenFold3 −0.26 → −0.63). That is Block A's A2 suggestion and it is free.

### E3.2 — The operational test
- **Question.** If you must pick one structure, does picking the highest-confidence seed
  beat picking at random?
- **Design.** Already computed: **+1.1 pp overall, sign flipping across backbones (−3.1 to
  +4.9), and — at SEED grain, which is the grain this question is about — **300 of 319
  cells unanimous**, i.e. only **19 of 319 (6.0%)** show any seed-to-seed disagreement at
  all.** Report it as the operational half, and note that the +1.1 pp is therefore being
  extracted from a 6% slice — a sharper statement of "the operational effect is small"
  than the percentage-point figure alone.
  *(This line previously read "256 of 319 cells unanimous anyway". **256 is the
  SAMPLE-grain count** — all 25 individual predictions agreeing — and using it for a
  question about seeds understates how redundant the seed axis is. Corrected 2026-09-11;
  both grains are derived in `redo/build/matrix_power.py`, which prints the
  distinction at runtime, and recorded at `RUN_MATRIX.md:547-548` and `HANDOVER.md:39`.)*
- **Cost.** `free`.
- **Novelty.** ADJACENT — `ku2026promise` runs confidence-ranked vs uniform-random top-k
  at matched budget and reaches the same verdict. **Cite its numbers, not just the paper**
  (note line 523, p15 Fig S2): Confidence Top-10 vs Random Top-10 — AF3 **0.15 vs 0.17**
  (intrinsic) and **0.49 vs 0.48** (ligand), BioEmu **0.18 vs 0.18**, across five models
  at 100 predictions per entry, with the paper stating confidence is *"occasionally
  outperformed by, uniform random sampling"*. Our +1.1 pp and ku's ≈0 agree, which makes
  our operational result a **replication** rather than an isolated observation.

### E3.3 — Confidence on the supplied partner chain
- **Question.** Does the model's confidence in the *peptide it was handed* predict whether
  the receptor opened?
- **Design.** `plddt_ga_alpha5` exists on Block A rows. At peptide length this becomes the
  in-silico analogue of `tran2026nanogs`'s CD measurement of a disordered free peptide.
  Report it at the α5 C-terminal positions specifically, not as a chain mean.
- **Cost.** `free` on Block A; a required column on any new peptide arm.
- **Novelty — CORRECTED 2026-09-11 after the lit session's audit; the first version of this
  row was wrong.** It said "nobody has asked it of a protein partner". That is false.
  **`miglionico2026atlas` asks exactly that, on a Gα partner, at an α5 position**, and
  reports **per-residue pLDDT at Gα position H5.11 with ROC AUC 0.762** (p5, Spearman
  ρ = 0.505 over 1,714 GProteinDb pairs), alongside ipTM (AUC 0.706; 0.735 for class A) and
  max contact probability (AUC 0.771). It further **hard-protects the 7 C-terminal Gα
  residues from its own pLDDT < 70 filter** "since they are known to be important for
  specificity" (p20) — i.e. it treats partner-chain confidence at the α5 tail as the most
  informative thing in the complex. Verified here in `lit/notes/miglionico2026atlas.md`
  lines 46, 102–106 and 181.
- **What survives, and it is sharper than the original claim.** Miglionico's confidence use
  is **for binding, not for conformational correctness**, and its own note records that
  "no relationship between any confidence score and DockQ is reported anywhere". So the
  correct clause is: **nobody has asked it of a protein partner against a receptor
  conformational-state outcome.** The row keeps its value and gains two things it did not
  have — a strong prior that partner-chain confidence at α5 positions carries real signal,
  and **a published number to beat: AUC 0.762 for coupling.** If our α5 pLDDT discriminates
  receptor *state* at anything approaching that, it is a result; if it discriminates
  binding but not state, that is the cleaner and more publishable finding, and it is
  directly comparable to theirs.
- **Why this was the likeliest miss.** `miglionico2026atlas` is tagged
  `confidence-as-discriminator` **and** `partner-driven` in `INDEX.md`. A referee reaching
  for a prior on partner-chain confidence lands on it first.
- **Nearest.** `miglionico2026atlas` for the partner-confidence question;
  `yu2026domainmotion` for the ligand analogue (pLDDT fails to separate binders from
  nonbinders).

## Group 4 — memorization and generalization

### E4.1 — A date-stratified holdout panel
- **Question.** Does the co-input effect hold on receptors whose active state the models
  could not have seen?
- **Closes.** The largest single threat to the whole paper, and the one the Methods already
  concedes: 35 of 43 dated panel active references (81%) predate Boltz-2's cutoff
  (`methods.tex:222–246`).
- **Design.** §0.2 gives the set: **12 both-state Class A receptors whose earliest active
  entry is post-2023-06-01**, of which **5 are entirely post-cutoff**. Run the full ladder
  on them as a stratum and report ladder height post-cutoff against pre-cutoff.
  `ada1a ccr8 cxcr3 gpr6` are post-cutoff *and* off our current panel, so they are clean.
- **Cost.** `real`, and cheap for what it buys: 12 receptors × 4 backbones × (however many
  rungs) × 50. At 3 rungs, **7,200**.
- **Depends on.** Per-backbone cutoffs. Boltz-2 2023-06-01, Protenix 2021-09-30, Chai-1
  2021-01-12 (**but Chai-1 also trains on AlphaFoldDB — do not write "saw nothing after
  January 2021"**), OpenFold3 **undated and still an open ask**.
- **Novelty.** The *design* is DONE and well established — `skrinjar2026generalization`
  (8–25% success in the least-similar stratum vs 81–89% in the most similar),
  `swapna2025memorization`, `kim2026mac1`, `chiesa2025templatebias` (94 of 145 structures
  with no template and no training presence). **Not doing it is what would be unusual.**
  Nearest: `chiesa2025templatebias`.

### E4.2 — Training exposure against effect size
- **Question.** Is per-receptor ladder height correlated with that receptor's training-set
  exposure?
- **Design.** A scatterplot: exposure (deposition count, apo:holo ratio, first release
  date) against ladder height. `yu2026domainmotion` quantifies the enzyme version at
  40.3 pp; `ye2026multistatebias` notes a 10:1 state ratio as a possible contributor.
- **Cost.** `free` — Block B rows plus the GPCRdb snapshot, both in hand. Note
  `deposition_count` in the Block B covariates is constant and its regression ships NaN
  (`analysis/block_b/DATA_REQUESTS.md` ask 7), so the exposure variable has to be rebuilt
  from the snapshot rather than read from the drop.
- **Novelty.** ADJACENT. Nearest: `yu2026domainmotion`.

### E4.3 — The wild-type 21-mer as an unseen input
- **Question.** Can the peptide arm be argued prospective by construction?
- **State.** Checked here and in `CLAIMS.md`: **4X1H is the only peptide-bound entry among
  the 80 references**, its chain C is an **11-mer** `VLEDLKSCGLF` differing from native
  bovine Gαt1 `IKENLKDCGLF` at **four of eleven** positions. It is an engineered
  high-affinity analogue.
- **Consequence.** **No wild-type 21-mer α5-CT appears with a receptor in any deposited
  structure.** That is a quantitative anti-memorization argument and it is ours to make —
  it is also the single best reason to run the 21-mer rather than the 11-mer first.
- **Cost.** `free` to establish (a search over the deposited set); rides on E1.1 to use.
- **Do not.** Cite 4X1H as precedent for a wild-type 21-mer, and do not score a 21-mer
  prediction against it — that is an interface mismatch of the class already recorded for
  6E67.

### E4.4 — A post-cutoff inactive-state binder
- **Question.** Is "no backbone steers inactive" a property of the models or of what they
  have memorised?
- **Design.** Block D S2: ~600 predictions on one receptor with one post-cutoff
  inactive-state nanobody. The earlier search disqualified four candidates, three because
  a 141-residue "nanobody" was an anti-BRIL cryo-EM fiducial; that filter rule is reusable.
- **Cost.** `real`, ~600–2,000.
- **Depends on.** Finding a candidate. The search was closed rather than answered.
- **Novelty.** **OPEN.** The `nanobody` tag fires on three corpus papers and **none of them
  runs a predictor** (`georgiou2025heterogeneity` review, `hilger2020gcgr` cryo-EM/DEER,
  `tran2026nanogs` wet lab). Nobody has supplied an inactive-directing binder to a
  structure predictor and measured the result.
- **Prerequisite.** The D2 ADRB2 arms fed the same sequence to both subarms (§1.4). Any
  re-run must verify chain B by SHA before dispatch, not after.

## Group 5 — mechanism

### E5.1 — Steric exclusion at panel scale
- **Question.** *Why* does the co-input work?
- **State.** The only mechanistic measurement in the whole project, at **n = 2 receptors**:
  α5 heavy atoms fall within 4 Å of where TM6 sits in the deposited **inactive** structure
  on 52% and 39% of contacts, against 11% for the active structure and 2–4% for the
  prediction's own TM6. The partner cannot be placed without displacing TM6.
- **Design.** Extend to the full panel. Needs one representative cognate structure per
  receptor — coordinates, not predictions.
- **Cost.** `cheap` (the predictions exist; the coordinates were not shipped). Item 7 of
  `analysis/block_a/DATA_REQUESTS.md`.
- **Novelty.** **OPEN.** No paper in the corpus offers a steric account from coordinates
  for a partner-induced state change.
- **Why it matters more than its size suggests.** Everything else in the paper is *what*
  the models do. This is the only measurement that says *why*, and at n=48 with the
  active-structure control quantified it becomes the mechanistic section the paper lacks.

### E5.2 — Per-Ballesteros–Weinstein decomposition
- **Question.** *Where* in the pocket, and at which residues, is the signal?
- **State.** `s4_bw_decomposition.json` and `s4_bw_position_decomposition.json` are named
  in two Block C narrative reports and neither ships. Block C's own claim sheet names this
  as what keeps Rung 3 at partial.
- **Cost.** **`free (them)`.**
- **Novelty.** Fills a hole rather than claiming ground: across all four blocks the paper
  has no residue-level account of anything.

### E5.3 — Report the ensemble, not its mean
- **Question.** Does the partner *shift* the ensemble or *narrow* it?
- **Design.** Every Block B cell holds 50 samples and is currently reported as a scalar.
  The bimodality is already visible in the binary result — 111 of 160 apo cells never fire,
  108 of 159 cognate cells always fire — and the introduction is built on a multi-state
  literature.
- **Cost.** `free`.
- **Novelty.** ADJACENT. `ku2026promise` recovers all known states in only ~8–29% of
  clusters and traces the collapse to the structure module; `jung2026boltzperturb` reports
  vanilla Boltz-2 ligand RMSF < 2.3 Å across 180 samples. Nearest: `ku2026promise`.

### E5.4 — Dose–response on engagement depth
- **Question.** Replace a threshold argument with a dose–response one.
- **Design.** The 20 Å α5-tip-to-R3.50 cutoff is ~4× the cognate median insertion depth of
  12.19 Å and the drop's own C-B-6 flags it as permissive. Report p(active) as a
  *function* of insertion depth. The distance is continuous and measured on every row.
- **Cost.** `free`.
- **Novelty.** ADJACENT. Dose ladders exist on MSA and steering knobs
  (`mitjavila2026afsample2t`, `kalakoti2025afsample2` with its non-monotonic optimum,
  `jedryszek2026probing`'s explicit k-sweep) but **nobody titrates a biological co-input
  and reads a graded state response.** Combined with E1.1 this becomes the first co-input
  dose–response in the literature.

### E5.5 — What the failures have in common
- **Question.** Is there a rule for when the co-input fails?
- **Design.** Pool every cell across A, B and D by outcome and regress failure against
  published correlates rather than inventing new ones: training similarity
  (`skrinjar2026generalization`), PDB apo:holo or active:inactive ratio
  (`yu2026domainmotion`, `ye2026multistatebias`), reference activity level
  (`chib2025gpcrstates` — agreement with inactive references worsens as activity rises),
  reference separation, ligand modality (peptide vs small molecule), and paralog cluster.
  Block C attempted the last of these as a *pre-registered* applicability domain and it was
  **refuted** — the slope ran negative — so this must be framed as post-hoc unless it is
  pre-registered afresh.
- **Cost.** `free` on A and B; needs Block D's rows for D.
- **Novelty.** DONE as a genre. Nearest: `skrinjar2026generalization`. Value is internal.

## Group 6 — the delivery contract

### E6.1 — A row-level delivery contract, agreed before the campaign runs
- **Question.** Will the redo be recomputable?
- **Why it is an experiment and not admin.** Block D shipped 0 of 42,180 predictions,
  Block C shipped a 16-column census with no state, and Block B ships no state column.
  Three of four campaigns are partly or wholly unverifiable, and the paper says so in the
  Methods. **A fifth campaign that repeats this is not worth running.**
- **The contract.** One tidy table per campaign, one row per prediction, carrying:
  `receptor_slug, backbone, arm, rung, partner_identity, partner_sha256, n_partner_aa,
  ligand_role, ligand_ccd_or_smiles, seed_outer, sample_idx, msa_depth_realised,
  msa_depth_rung, msa_paired,
  templates_used, d_npxxy_oh, d_tm6_tilt, pif_connector, pocket_ca_rmsd_active,
  pocket_ca_rmsd_inactive, plddt_mean, plddt_at_anchors, plddt_partner_chain,
  partner_helicity, n_interface_contacts, engagement_depth, ref_pdb_active,
  ref_pdb_inactive, scorer_sha, excl_*`. Plus the bootstrap draws behind every interval.
- **Specific defects to ban by contract:** self-certifying columns that can never fire
  (`flag_low_confidence` False on 40,000 rows; `passed` True on all of A, B and C);
  placeholder strings in place of nulls (`reference_audit.csv`'s `method` and `resolution`
  on all 80 rows, both non-null so a null check passes); all-NaN audit blocks
  (`A1`–`A6` on 9,490 and 32,000 rows); CSVs with unquoted commas (`tier_d3_panel.csv`);
  and **nominal levels standing in for measured quantities** — `msa_depth_realised` must be
  the row count the backbone actually consumed, because Block D's four headline depth slopes
  are fitted with `full` imputed as 4,096 and no realised depth was ever recorded (E8.3).
  A rung label is a design fact; a depth is a measurement, and a regression needs the
  second.
- **Cost.** free, and it is a precondition rather than an experiment.

### E6.2 / E6.3 — Ship the three Block D `rows.csv` and `rows.tier3.v2.csv`
- **Cost.** **`free (them)`.** Between them these two files close ~18 of the 62 open asks
  across the four request documents — Block D's own S1 puts it at "eleven of the twelve
  asks", and Block C's ask 1 says the one file closes asks 2, 6, 7, 8, 10 and 14 alongside
  itself. Block D's verifier goes from 40 recomputed checks to something near 120. Nothing
  in the catalogue has a better ratio of value to cost.

### E6.4 — Pair seeds across arms
- **Question.** Can within-seed differences be read?
- **State.** Block A's seeds are not paired between arms
  (`analysis/block_a/DATA_REQUESTS.md` open question C). A ladder whose rungs share seeds
  supports a matched-pair analysis at no extra compute and materially tightens every
  interval.
- **Cost.** free if specified before dispatch; impossible afterwards.

## Group 7 — new directions

### E7.1 — What would an inactive-directing co-input even be?
- **Question.** The active direction has a natural co-input. Does the inactive direction
  have one at all?
- **Why it is worth asking.** Block D found the inactive direction does not work, bounded
  by a memorization confound it could not close, and `rebuttals/BLOCK_D.md` S5 notes the
  deeper problem: *without an inactive-direction positive control, "no backbone steers
  inactive" and "nothing in this setup could have steered inactive" are
  indistinguishable.*
- **Candidates, honestly ranked.** (a) a post-cutoff inactive-state nanobody (E4.4) — the
  only clean one, and it may not exist; (b) an inverse agonist (E2.3) — biologically the
  right handle and weak in these models; (c) a Gα α5 mutant that binds without opening
  (E1.8) — speculative; (d) the *absence* of a partner, which is the apo arm and is not a
  control. **Being unable to name a good one is itself a result** and belongs in the
  Discussion rather than being hidden.
- **Cost.** free to write; `real` to test.
- **Novelty.** OPEN, per E4.4.

### E7.2 — Cross-class transfer: the class B ladder
- **Question.** Does partner length behave the same way where the biology says the partner
  matters *more*?
- **Why class B is the sharpest venue.** `hilger2020gcgr`, on GCGR: "TM6 activation is only
  triggered by the engagement of the α5 helix of Gαs", and agonist alone produces no TM6
  opening at all. In class A the agonist does part of the work; in class B it does none.
  **If the α5-CT length ladder means what we think, class B should show a larger step.**
- **Design.** The length ladder on 4–8 class B1 receptors. Requires E0.5 first — class B
  has no NPxxY and no validated predicate; the current substitute is an uncalibrated kink
  angle. 148 class B1 structures exist in the snapshot to calibrate one.
- **Cost.** `free*` for the predicate, then `real`: 8 receptors × 4 backbones × 4 rungs ×
  50 = **6,400**.
- **Novelty.** ADJACENT on coverage (`heo2022multistate` spans A/B1/B2/C/F,
  `chib2025gpcrstates` spans 75 receptors across four classes, `khaleq2026hyaline` reports
  per-class breakdowns) but **OPEN as transfer**: no paper tests class transfer *as*
  transfer with a held-out class, and `khaleq2026hyaline`'s temporal split does not hold
  out receptors at all. `lee2026confornets`' transfer is across domains, not GPCR classes.

### E7.3 — A prospective arm on receptors with no solved active state
- **Question.** The whole argument for an intrinsic predicate is that it runs where no
  reference exists. Have we ever run it there?
- **State.** No. Every receptor in every block has both references by construction.
- **Design.** Recomputed here at receptor-slug level, the snapshot holds **113 Class A
  receptors with active structures only** and **9 with inactive structures only and no
  active structure anywhere**: `acm5 ada1b ada2c ccr7 ccr9 gnrhr lgr4 ox1r q9wtk1`
  (species-level the counts are 120 and 13; the difference is paralog/species duplicates
  such as `acm3_rat`, `drd4_mouse`, `oprd_mouse` whose active state is solved under another
  entry). Take those 9, run the ladder, and report predicted active-state geometry that can
  be scored against nothing — a genuine prediction. Pre-register the calls.
- **Cost.** `real`, 9 × 4 × 3 rungs × 50 = **5,400**.
- **Novelty.** **This is the closest thing to prospectivity available.** The corpus survey
  found that of 78 papers **exactly three report an unqualified prospective result and none
  is of the relevant kind** — a wet-lab peptide study generating no structures
  (`tran2026nanogs`), a blind CASP submission defining no conformational state
  (`wallner2023afsample`), and a de novo design campaign (`ingraham2023chroma`).
  Even `richman2025conformix`, the cleanest reference-free method, scores coverage against
  deposited references.
- **Honest limit.** Nobody can grade it. Its value is that it is the only experiment whose
  design does not presuppose the answer, and it costs little. Pair it with a falsifiable
  pre-registration or it is decoration.

### E7.4 — Estimate the interaction, with power stated in advance
- **Question.** Not "do the inputs compose" but "could we have detected it if they did?"
- **Why.** `suzuki2026conforflux` is the only corpus paper to attempt an interaction term
  between two factors and it reports, p.21, that with n=10 targets and ~0.6 Å standard
  error it **cannot resolve non-additivity**. Block C's null on the applicability domain
  has the same shape: a null nobody can size. Both of Block A's and Block C's suggestion
  lists ask for a positive control for a null, twice, independently.
- **Design.** Before E2.2 runs, inject true interaction effects of known size into the
  existing 22,400-row design and report the fraction of cluster-bootstrap replicates whose
  interval excludes zero. One panel, one sentence, and it turns every null in the paper
  from unfalsifiable into bounded.
- **Cost.** `free` once one row-level ligand table exists.
- **Novelty.** Not novel; load-bearing. This is the cheapest way to stop the paper's
  negatives from being unanswerable.

### E7.5 — Extend the panel to the Class A both-state census
- **Question.** Is the panel a census or a sample?
- **Design.** Add the 24 off-panel Class A both-state receptors (§0.2) to reach **64 of 64
  slugs — a complete census of Class A receptors with both states in GPCRdb as of the
  snapshot date**. That is a sentence a referee can evaluate, and it is the strongest
  available answer to `rebuttals/BLOCK_A.md` Q-A1.
- **Secondary effect that may matter more.** It fixes three specific weaknesses at once:
  Gs-coupled receptors rise from 5, so E1.4 and E1.8 become powered; Block B's collapsed
  Gs→Gq (n=3) and Gi→Gs (n=0) strata get members; and four of the five entirely-post-cutoff
  receptors (E4.1) join the panel.
- **Cost.** `real` multiplier: every arm becomes 12,800 instead of 8,000, a 1.6× uplift on
  everything. **Adopt it only for the arms whose conclusions depend on power**, not
  uniformly.
- **Comparability.** Anchoring on ConfoRNets: their benchmark is 51 pairs; we share **27**
  with our 40 Class A (**30** with our 48). A 64-slug Class A census contains **45 of their
  51** test cases; the six it cannot contain are CALRL (B1), GLP1R (B1), AGRE5 (B2), FZD7
  (F), SMO (F) — out of Class A by construction — and **ACM3**, which qualifies as a
  both-state receptor only under the cross-species pairing (human 8E9Z active / rat 4U15
  inactive) that their paper does not disclose. Note this corrects a reading in
  `rebuttals/PANEL_EXPANSION_CLASS_A.md`, which describes the 51 as Class A plus CALRL and
  AGRE5: it also contains three receptors of classes B1 and F that happen to be on our
  panel already.
- **Two cautions from `lit/panels/README.md`.** A matching count is not a matching
  membership — a panel rebuilt from a published rule matched a count to 1.2% while sharing
  only 222 of 253 entries. And **no receptor appears in all four enumerated GPCR
  benchmarks** (union 175, 115 in exactly one), so no "X beats Y on GPCRs" claim has a
  shared basis, ours included.
- **Known panel defects to fix while extending.** `B1B1U5` is a jumping-spider opsin and
  `OPSD` is bovine — **no sentence may call this panel human**. AA2AR is recurrently
  anomalous and ConfoRNets picks a *worse-resolution* active reference for it (6GDG 4.11 Å
  over our 5G53 3.40 Å), which under their construct-quality-first rule implies 5G53 is
  more heavily engineered — a concrete, testable explanation for the anomaly at the cost of
  no new predictions.

### E7.6 — A second biological co-input at peptide length: the arrestin finger loop
- **Question.** Is the effect about the α5 specifically, or about *any* cognate
  intracellular partner element?
- **Design.** `arrestin_FL` (15 aa) and `arrestin_Ctail` (41 aa) are already in
  `partners.fasta` and were consumed by zero rows. The finger loop occupies the same cleft
  and stabilises an active-like state through a different evolutionary lineage — which
  makes it a *positive* control of a kind the project has never had: a non-Gα biological
  partner that should work, against a non-Gα non-biological partner (E1.2) that should not.
- **Cost.** `real`, 1–2 arms, **8,000–16,000**; 2,000 on one backbone.
- **Novelty — OPEN, but the supporting sentence is CORRECTED.** The first version said
  arrestin "appears in the corpus only as review content in `georgiou2025heterogeneity`".
  **That is false: it appears in 7 notes** — `paajanen2026activation`,
  `georgiou2025heterogeneity`, `khaleq2026hyaline`, `miglionico2026atlas`,
  `heo2022multistate`, `chakravarty2026statespace`, `bryant2024cfold`. **None supplies
  arrestin to a predictor**, so the OPEN verdict holds — but three of the seven are better
  evidence than the review, and one changes a design:
  - **`heo2022multistate`** records that "ligand, nanobody, G-protein and arrestin are never
    used as inputs" — a recorded absence, the same shape of evidence E1.1 rests on. **Cite
    this rather than the review.**
  - **`khaleq2026hyaline`** already counts "arrestin-coupled structures" as active in its
    own label rule, so the classifier literature treats an arrestin-coupled receptor as
    active-state — which supports this arm's premise. It also states its limit: the model
    "does not address … the distinction between G protein-biased and arrestin-biased
    conformations" (p11).
- **A circularity check this arm must pass before it runs.** If any arrestin-coupled
  structure defines "active" in **our own** reference set, an arrestin-FL arm is partly
  circular in exactly the way `khaleq2026hyaline`'s label rule is. That is a free check
  against `data/block_b/09_references/reference_audit.csv` and it should be done first, not
  discovered afterwards.
- **A cross-experiment dependency neither row recorded.** E0.2 names
  `paajanen2026activation`'s learned coordinate as independent index (c). **Paajanen
  excluded arrestins** — "Arrestins have not been included in the analysis because there is
  not enough data to influence the graph" (p.2). **So an arrestin arm cannot be
  concordance-checked against E0.2's index.** Either E7.6 states that it has no independent
  check, or E0.2 drops option (c) for this arm. Decide before dispatch.
- **The hypothesis, still the best reason to run it.** `georgiou2025heterogeneity` records
  that β-arrestin-biased agonists act on TM7 rather than TM6, so the prediction is that the
  finger loop **moves the NPxxY axis more than the tilt axis**. That is falsifiable, and it
  is an argument for reporting the two axes separately rather than only their conjunction.

## Group 8 — MSA depth as a crossed factor

*Added in a second pass, 2026-09-11. Depth was varied in Block D and appears nowhere in
the first draft of this catalogue except as a delivery column (E6.1). That was an
omission: E1.9 varies MSA **pairing** on the partner chain (binary) and E5.4 is physical
insertion depth, neither of which is alignment depth.*

**What Block D actually did.** D3: 26 Class A receptors × 4 backbones × **5 depths
(8, 32, 128, 512, full)** × 5 seeds × 10 samples = 26,000 dispatched, **25,810 landed**
(190 rows, 0.73%, non-uniform — worst case n=1,250 at OF3 × full and Chai × full).
**Apo only.** No partner at any depth, no ligand at any depth. The panel is the 40 Class A
panel of record minus 8 sealed receptors, quota-stratified to 26; FSHR and LSHR were
dropped as "compute-heavy glycoprotein-hormone big complexes — H100-only constraint",
which is a hardware decision, not a scientific one, and it matters for Group 9.

### E8.1 — Cross depth with partner, in the middle of the ladder
- **Question.** Does a physical co-input **rescue** what removing the alignment took away?
  Do depth and partner act on the same mechanism or on different ones?
- **Closes.** The axis Aditya named, and the limitation the manuscript already states in
  its own words (`results.tex:655–663`): "depth is varied in the apo arm only, so MSA depth
  and partner presence are never varied together inside one model here either."
- **Design, and the one non-obvious choice.** **Do not cross depth with apo and cognate.**
  Both endpoints are pinned — the apo arm sits at 0.158 and the cognate arm at 0.891, and
  Block C is the cautionary case of a campaign whose predicate saturated mid-flight. Cross
  depth with the **middle rungs** of the length ladder (E1.1 R1–R3, the peptide rungs),
  where the response has headroom in both directions. Keep apo and cognate as the two
  anchors at full depth only.
- **The prediction it tests.** If depth and partner act on one mechanism, a partner should
  flatten the depth slope. If on two, the slope should survive at every rung. Either result
  is publishable and they are distinguishable.
- **Cost, with the affordable projections spelled out** (the run-matrix agent owns the
  final subsetting; these are sizes, not a decision):

  | version | factors | cells | new predictions |
  |---|---|---:|---:|
  | full three-way | 5 depths × 2 partner × 2 ligand × 26 rec × 4 bb | 2,080 | **260,000** — unaffordable |
  | depth × partner, all depths | 5 depths × 2 partner × 26 × 4 | 1,040 | 130,000 gross, **~104,000 new** (D3's apo × 5 depths already exists) |
  | depth × partner, 3 depths (full/32/8) | 3 × 2 × 26 × 4 | 624 | **~31,200 new** |
  | **depth × partner, 2 depths (full/8), 1 backbone** | 2 × 2 × 26 × 1 | 104 | **~2,600 new** |
  | depth × 3 ladder rungs, 2 depths, 12 rec, 2 bb | 2 × 3 × 12 × 2 | 144 | **7,200** |

  **Run the 2,600-prediction version first.** Block D's own S3 proposes exactly this shape
  ("a 2 × 2 of depth (full, 8) by partner (apo, cognate Gα) on a subset of the D3 panel");
  what this entry adds is that the partner level should be a *peptide rung*, not cognate,
  and the reason.
- **Depends on.** **E8.3 first — the anchor must be fixed or the top rung is undefined.**
  Also on E1.1 if the middle rungs are used; the cognate-level version can run alone.
- **Novelty.** **OPEN.** Of 81 papers, exactly one crosses an MSA manipulation with a
  co-input inside a single model — `mitjavila2026afsample2t`, which crosses column masking
  (0/10/20/30%) with partner presence at 250 models per cell, and which **has no ligand
  channel at all** (AF2 docks ligands post hoc). `cheng2026af3cluster` combines MSA
  clustering with co-folded binders but does not cross them as factors.
  `xing2025purified` is the result to engage: "the successful sampling of alternative
  states depends not on MSA depth but on sequence purity" (p.3) — and it is AF3 + ligand
  SMILES + subsetted MSA + a state readout, on EGFR, not a GPCR. Nearest:
  `mitjavila2026afsample2t`.

### E8.2 — Cross depth with ligand, at fixed partner condition
- **Question.** Aditya's phrasing was "MSA subsampling with and without ligand". A ligand
  and a protein partner are not interchangeable co-inputs, and the corpus says so.
- **Design.** Depth × ligand presence (none / full agonist) at the apo partner level, on the
  subset of the D3 panel that also has a Block C agonist. **This is the half that is
  genuinely cheap:** D3 already holds depth × no-ligand × apo on 26 receptors, so only the
  ligand arm is new.
- **The hypothesis, which is falsifiable.** `ye2026multistatebias` (p.2) reports that "large
  protein partners drive clear conformational switching between states" where small
  molecules do not. So the prediction is that **a partner rescues depth loss and a ligand
  does not** — and running E8.1 and E8.2 as two 2×2s on one panel makes that a direct,
  matched comparison rather than a cross-paper inference. If the ligand *does* rescue,
  `ye2026multistatebias`'s asymmetry does not survive on an AF3-lineage panel at scale,
  which is a more interesting result than the expected one.
- **Cost.** `real`. 5 depths × 1 new ligand arm × 26 × 4 × 50 = **26,000**; at 2 depths on
  1 backbone, **2,600**.
- **Depends on.** E8.3; the Block C ligand curation (which receptors have a usable agonist —
  35 of 36 in Block C, with HRH3 missing the role entirely).
- **Novelty.** **OPEN**, same evidence as E8.1. `lazou2026cryptic` varies the ligand with the
  MSA held constant, and `jung2026boltzperturb` varies the representation with the ligand
  held constant. They bracket the question from opposite sides and neither crosses it.

### E8.3 — Fix the depth anchor before any depth work. **Blocking.**
- **The problem as stated upstream.** D1 and D3 share 7 receptors. On **OPSD × Boltz-2**,
  D1 reports 38.8% predicate-active at n=500 and D3's *full-depth rung* reports 10.0% at
  n=50 — a 28.8-point, ~3σ gap. Block D's caveat C-D-8 hypothesises that "D3's per-depth-cell
  MSA subsampling pipeline's `full` rung is NOT bit-identical to D1's upstream default
  MSA-mode — D3 sub-samples then re-inflates", and records it as "hypothesis only",
  "not verified this pass".
- **What I can add from data in hand, and it changes the reading.** Block B's apo arm is an
  **independent third measurement of all 28 D1 cells** — different campaign (019 vs 022),
  different panel, 50 predictions per cell, scorer `04243c45` against Block D's `d9c646af`.
  Recomputed here from `data/block_b/01_rows/rows_tidy.csv`:

  | cell | Block B, n=50 (95% Wilson) | D1, n=500 | D3 full, n=50 |
  |---|---|---:|---:|
  | **OPSD × boltz** | **30.0% [19.1, 43.8]** | **38.8%** | **10.0%** |
  | OPSD × chai | 94.0% [83.8, 97.9] | 98.6% | 88.0% |
  | OPSD × of3 | 4.0% [1.1, 13.5] | 9.4% | 4.0% |
  | CNR2 × chai | 100.0% [92.9, 100] | 99.8% | 100.0% |
  | LPAR1 × of3 | 92.0% [81.2, 96.8] | 91.8% | 98.0% |

  Across all 28 cells, **D1's point estimate falls inside Block B's 95% Wilson interval on
  26 of 28**, the two misses being OPSD × chai (98.6 against an upper bound of 97.9) and
  NPY1R × boltz (0.2 against a lower bound of 0.4) — both under a point. **Block B
  independently reproduces D1.**
- **And undersampling does not explain D3.** If the cell's true rate is D1's ~0.388, then
  observing 5 of 50 is a ~3.7σ draw (p ≈ 5 × 10⁻⁴), while Block B's 15 of 50 is an ordinary
  one. So the pipeline's own reading (a) — "real bimodality where (5, 10) undersamples the
  active mode" — is **not supported**; reading (b), an upstream difference between D3's
  `full` rung and the default apo condition, is the one that survives. That is worse for
  depth work than undersampling would have been.
- **One thing that cuts the other way, stated because it bounds the claim.** At *panel*
  level the D3 full rung does reproduce. On D3's own 26 receptors, Block B's apo arm gives
  Boltz 8.3%, Chai 21.6%, OF3 11.1%, Protenix 0.2% against D3-full's 5.1 / 19.4 / 12.4 /
  0.1 — within 3.2 points on all four. But that comparison is **insensitive to a per-cell
  defect**: a 29-point error on 1 of 26 receptors moves a pooled mean by about a point. So
  panel-level agreement bounds the *average* size of the drift and does not exclude it.
- **What closes it.** (i) Emit the **realised** MSA row count per prediction, not a rung
  label — free, and it settles the question directly; (ii) one sentence saying whether the
  `full` rung is the same input condition as an unmanipulated run — free; (iii) rerun
  **OPSD × Boltz-2 apo at n=500 through the D3 pipeline's full rung**, which C-D-8 itself
  proposes as "small compute, single cell" — **~500 predictions**; (iv) refit the slopes
  against realised depth.
- **Why (iv) is not cosmetic.** GATE-2 established that the four headline slopes reproduce
  only under `ln(depth)` with **`full` imputed as 4096**. That value is nominal — no
  realised depth was recorded — and Block B's own MSA audit shows Boltz consuming **13,678
  alignment rows** for one ADRB1 cell. If the true top rung is ~13,700 rather than 4,096,
  every slope in %/ln(depth) is fitted against an x-axis whose highest point is wrong by
  more than an e-fold.
- **Cost.** `free (them)` for (i), (ii), (iv); `real` but trivial for (iii).
- **Novelty.** None; it is a prerequisite. It also closes Block D's open Q8 and caveat
  C-D-8, and the Block B evidence above is new and free.

## Group 9 — the deep-apo floor

*Added in a second pass. Its omission was not deliberate and the coordinator is right that
it should not have been.*

**Why it is a designed experiment and not a summary statistic.** The four backbones do not
share a baseline. On β₂AR apo, Chai-1 calls 100% of 500 samples active and Boltz-2 calls
0%. **Every ladder rung is measured against a different floor per backbone, so a rung at
40% means opposite things on two of them** — and pooling across backbones is what produced
the withdrawn "spontaneous apo bistability" claim, which was a 50% average over two
backbones that disagreed completely. The four outlier cells are also the only project
result that survives a change of corpus.

### E9.1 — Characterise the floor from data already held. **free.**
- **Question.** Which receptor × backbone apo cells carry information, and which are pinned?
- **Recomputed here** from `data/block_b/01_rows/rows_tidy.csv`, 160 apo cells (40 Class A ×
  4 backbones), predicate applied at the shipped thresholds:

  | | cells |
  |---|---:|
  | NPxxY axis undefined (4 receptors × 4 backbones) | 16 |
  | **pinned at 0** — never fires on any of 50 | **91** |
  | **pinned at 1** — fires on all 50 | **9** |
  | **mixed** | **44** |

  Of the 44 mixed, **24 sit between 0.10 and 0.90** and **20 sit at ≤ 0.08**, i.e. 1–4
  samples of 50. **The information is in ~24 cells and the variance risk is in 20 more;
  the other 100 need no deeper sampling at all.**
- **The per-backbone floor, like for like.** Block A (Class A only, NPxxY-defined) gives
  Boltz 13.6%, Chai 31.9%, OF3 11.0%, Protenix 7.7%; Block B's apo arm on the same basis
  gives 12.7 / 32.3 / 11.0 / 7.2. **Two independent campaigns agree within 0.9 points on
  every backbone.** The floor is a stable, reproducible property and should be reported as a
  result, not as a baseline to be subtracted silently.
- **The receptor the existing panels miss.** **FSHR is mixed on all four backbones**
  (Protenix 0.92, Boltz 0.90, Chai 0.72, OF3 0.30) — the only receptor in the panel that is
  intermediate everywhere rather than backbone-split. It is in neither D1's 7 nor D3's 26,
  and D3's own panel file records why: dropped as a "compute-heavy glycoprotein-hormone big
  complex". **The single most informative receptor for a deep-apo arm was excluded for
  hardware reasons.** That is a decision worth revisiting explicitly rather than inheriting.
- **Cost.** `free`, and most of it is done above.
- **Dependency note.** This is a *selection* statistic, not a panel decision — the
  ConfoRNets-anchored panel is `redo/spec/PANEL.md`'s call and the sampling budget is
  `redo/spec/RUN_MATRIX.md`'s. **This entry supplies the input to both and decides
  neither.**

### E9.2 — Deep apo sampling, targeted rather than uniform
- **Question.** At what n is an apo cell's rate stable, and does the ladder's bottom rung
  need a different sampling budget from its other rungs?
- **Why n=50 is not enough at the bottom and is enough elsewhere.** The cognate rung is
  pinned near 1 and the apo rung is pinned near 0 for 91 of 160 cells; both are cheap. The
  ~24 intermediate cells are where a binomial at n=50 has a standard error of ~7 points,
  which is the width of an entire ladder step. D1 spent 500 per cell on 7 receptors and got
  intervals of ±2–4 points.
- **Design.** An asymmetric budget: 50 per cell at every rung, **plus** a deep apo arm at
  200–500 per cell restricted to the cells E9.1 identifies as unpinned. Selection is from
  data in hand and therefore free and auditable, which is what D1's panel note did by hand.
- **Cost.** `real`, and targeting is most of the value:

  | scope | cells | at n=500 | at n=200 |
  |---|---:|---:|---:|
  | all 160 apo cells | 160 | 80,000 | 32,000 |
  | the 44 mixed cells | 44 | **22,000** | **8,800** |
  | the 24 cells in [0.10, 0.90] | 24 | **12,000** | **4,800** |

  Uniform deep sampling costs 6.7× the targeted version and buys nothing on 100 pinned
  cells.
- **Depends on.** E9.1 for the selection; E0.1, because recalibrating the thresholds moves
  which cells are pinned — **run the selection after calibration, not before.**
- **Novelty.** ADJACENT. Sampling budgets in the corpus run from 5 (`wohlwend2024boltz1`,
  `zhang2026generalization`) to 6,000 (`wallner2023afsample`), with 500 per condition common
  (`yu2026domainmotion`, `lazou2026cryptic`, `suzuki2026conforflux`). What is unusual is
  spending them **asymmetrically by measured cell variance rather than uniformly**, and
  saying so. Nearest: `yu2026domainmotion`.

### E9.3 — Report every rung against its own backbone's floor. **free.**
- **Question.** An analysis convention, not an experiment, and it changes what the results
  mean.
- **Design.** Report each rung as a shift from that backbone's own apo floor as well as an
  absolute rate, and never pool a rate across backbones. Block D already established the
  rule — "**No figure or sentence in this work pools across backbones**, and this is why" —
  after pooling produced a finding that had to be withdrawn. The redo should carry it as a
  convention from the start rather than as a lesson.
- **Cost.** `free`.
- **What it also fixes.** It makes Chai-1 legible. Chai-1 is the "soft predictor" on every
  metric in Block A, and part of that is simply that its floor is 2–4× every other
  backbone's (31.9% against 7.2–13.6%), so it has the least headroom to rise. A shift-from-
  floor reading and a ceiling-aware one may show Chai-1 is not soft at all.

---

# 4. Ranked shortlist

Ranked on: does it close a title clause; is it the referee's first question; is it novel
against 81 papers; what does it cost; does it de-risk something that could invalidate the
paper. **Four of the top six cost no new inference.** That is deliberate.

*Extended from eight to ten in the second pass, when Groups 8 and 9 were added. The first
eight are unchanged in order relative to each other.*

### 1. E6.2 + E6.3 — ship `rows.tier3.v2.csv` and Block D's three `rows.csv`. `free (them)`.
Unglamorous and first. Forty-two thousand predictions currently cannot be checked at all
and thirty of Block C's fifty-three checks are consistency-only. Until these land, any new
campaign is being designed against numbers nobody has verified — and Block A's record (21
discrepancy groups, 17 found here, including an inverted claim and a CIF that is the wrong
protein) is the reason that is not a rhetorical worry. It also unblocks E2.1, E2.4, E5.2,
E5.5 and E7.4 at once. **Ranked above everything because it costs nothing and everything
downstream conditions on it.**

### 2. E9.1 — characterise the apo floor from data already held. `free`.
Free, mostly done in this document, and **time-critical**: three sibling agents are
selecting a panel and a run matrix right now, and the statistic they need is which apo cells
carry information. **91 of 160 Block B apo cells never fire on any of 50 samples and 9 fire
on all 50; the information is in about 24.** Uniform sampling spends 6.7× what targeted
sampling does and buys nothing on the pinned cells. It also shows the two campaigns agree
on the floor to within 0.9 points per backbone, which turns a baseline into a result.

### 3. E0.1 — recalibrate the predicate off-panel. `free*`.
The instrument grades with the labelling it was built from, the Methods admits it, and a
reviewer will open there. It is also the one thing that must happen before any new rate is
reported, so it sits on the critical path regardless of what else runs. §0.2's finding —
611 active against 115 inactive off-panel — means this is a real design problem, not a
formality, and finding that out now rather than after 40,000 predictions is most of its
value.

### 4. E8.3 — fix the depth anchor. `free (them)` plus ~500 predictions.
Blocking for everything in Group 8, and it resolves an open Block D question rather than
inheriting it. D1 and D3 disagree by 28.8 points on OPSD × Boltz-2; Block B's apo arm is an
independent third measurement and it reproduces D1 on **26 of 28 D1 cells**, siding with
D1 on the contested one. D3's value is a ~3.7σ draw from D1's estimate, so undersampling
does not explain it and the pipeline's unverified "depth-preparation drift" is the reading
that survives. Separately, the four published depth slopes are fitted with **`full` imputed
as 4,096** while Block B's own MSA audit shows Boltz consuming 13,678 rows for one cell —
so the regression's top x-point may be wrong by more than an e-fold. Emitting realised MSA
depth per row fixes both and costs nothing.

### 5. E1.1 — the α5-CT length ladder. `real`, 40,000 (10,000 for a single-backbone pilot).
The only experiment that closes a title clause. Novel against the whole corpus, with the
absence recorded verbatim in two independent notes. It absorbs the bulk control at rung R5
and it converts "how much partner do you need" from a caveat into a dose–response curve.
Ranked below the three no-inference items only because they are free and it is not. **Run the
single-backbone pilot before the full grid** — if the rungs do not separate on Boltz-2 at
n=2,000, the 40,000 buys a flat line.

### 6. E1.2 — the bulk control. `real`, 16,000 (2,000 for a pilot).
The first thing a referee writes, `yu2026domainmotion` is the published version of it, and
the occupancy term is 55% of the effect. Ranked sixth rather than higher only because
E1.1's R5 rung already supplies part of the answer and because the sequences are already
built, which makes it a dispatch rather than a design. **If only one of E1.1 and E1.2 can
run, run E1.1 with R5 included.**

### 7. E8.1 + E8.2 — cross depth with partner, and with ligand. `real`, ~2,600 to start.
The axis Aditya named, and the limitation the manuscript states about itself. **OPEN
against the corpus**: one paper carries the `factors-crossed` tag at all, and it crosses
MSA masking with partner presence and has no ligand channel. Ranked seventh rather than higher for two
reasons, both honest. First it is blocked on E8.3. Second, depth is an *operator* handle,
not a biological one, and this paper's whole argument is that the handle should be
biological — so a depth result is a mechanism probe and a robustness check, not a title
clause. Its real value is the matched comparison: if a protein partner rescues depth loss
and a small molecule does not, that is `ye2026multistatebias`'s asymmetry tested directly
rather than inferred across papers. **Start with the 2 × 2 at 2,600 predictions**, and
cross depth with the ladder's *middle* rungs rather than with apo and cognate, both of
which are pinned.

### 8. E2.1 + E2.2 — the ligand axis. `free (them)` then `real`, 22,400.
E2.1 is free and closes half of title clause 2 today. E2.2 is the cleanest *open* question
in the whole map: **zero of the seven papers that hold both handles cross ligand class
with partner presence in one model**, and the one paper that attempted an interaction term reported it could not resolve
one. Ranked eighth rather than higher because the resulting claim is confirmation, not
discovery — `ye2026multistatebias` and `vo2026fiducials` already bracket it — and because
E7.4 (free) should size the test before it runs.

### 9. E4.1 — the date-stratified holdout. `real`, ~7,200.
Cheap for what it de-risks. Eighty-one per cent of dated panel active references predate
Boltz-2's cutoff; `skrinjar2026generalization` reports 8–25% success in the least-similar
stratum against 81–89% in the most similar. If the effect is retrieval, this is where it
shows, and twelve receptors already exist for it. Ranked ninth only because Block A's
amplitude null is already a partial answer and because the OpenFold3 cutoff is still
undated.

### 10. E5.1 — steric exclusion at panel scale. `cheap`.
The only mechanism in the paper, currently at n=2, needing coordinates rather than
predictions. It converts a paper that reports *what* into one that reports *why*, and no
corpus paper offers a steric account of a partner-induced state change. Ranked last of the
ten because its cost sits with the pipeline and it does not close a title clause.

**Just below the line, and closest to being in it.**

- **`E1.5` — the per-position scan. `real`, 4,200 in its cheap form.** The
  highest-variance entry in the catalogue and the only one that produces a residue-level
  map, which the paper lacks across all four blocks. Both published point-mutation results
  (`masters2025physics`, `bret2025boltz2docking`) say these models do **not** respond to
  mutations that abolish function, so a positive result would be the most interesting
  finding in the project and a negative one is a clean extension of a published result to
  the partner side. It is informative either way, which is not true of most expensive
  experiments. It sat at eight before Groups 8 and 9 were added and it is displaced on
  cost, not on merit.
- **`E9.2` — targeted deep apo sampling. `real`, 4,800–12,000.** Follows E9.1 mechanically
  and is the cheapest way to stop a ladder step being narrower than the error bar on its
  own bottom rung. Below the line only because E9.1 must run first and the threshold
  recalibration will move which cells qualify.

**Deliberately not in the top ten, and why:**
`E7.5` (panel extension) is a multiplier on everything else rather than an experiment, and
applying it uniformly would raise every cost by 1.6× to fix power problems that only three
arms have. `E0.5` (class B/F) is a decision, not an experiment. `E2.3` (efficacy ladder) is
bottlenecked on ligand curation, not compute. `E7.3` (prospective arm) is cheap and
genuinely novel but ungradeable, so it belongs in the paper as a demonstration rather than
as evidence. `E3.x` (confidence) is free and should all be done, but the headline is DONE
eight times over in the corpus and is the weakest of the three title clauses as a
contribution.

---

# 5. New scientific directions, and what the corpus already covers

The ~36 suggestions in the four rebuttal documents are the floor. This section answers the
directions named in the brief one by one — with a verdict, not a hedge — and then lists the
ideas that came out of reading the data rather than the documents.

## 5.1 The named directions

| direction | catalogue entry | corpus verdict | nearest paper |
|---|---|---|---|
| **sequence determinants within the α5 tail** | E1.3, E1.5, E1.6 | **OPEN.** `/deep mutational\|saturation mutagenesis\|mutational scan/` returns **0 of 81**; the 5 per-position hits are all receptor-side self-mutation. Nothing scans a *supplied* partner and reads receptor state. | `waymentsteele2024cluster` (the protocol to copy: 8-point scan, no MSA, state flips); `masters2025physics` (receptor-side, and it names the retrieval confound) |
| **do partner and ligand compose additively** | E2.2, E7.4 | **OPEN, and the cleanest open question in the map.** **Zero of the 7 papers carrying both handles cross them.** No paper attempts an interaction between two *biological* co-inputs; the corpus's only non-additivity test is between two algorithmic hyperparameters and is underpowered. | `ku2026promise` (both handles, both model families, **separate sets**); `mitjavila2026afsample2t` |
| **what the failure cases have in common** | E5.5 | **DONE as a genre**, with several correlates already published — use them rather than rediscovering them. Value here is internal, not novel. | `skrinjar2026generalization`; `yu2026domainmotion`; `chib2025gpcrstates` |
| **co-evolutionary or steric** | E1.9, E5.1 | **ADJACENT.** The mechanism debate is mature and entirely about the *receptor's* alignment. Nobody asks it of a protein partner, and nobody offers a steric account from coordinates. | `feldman2026alphainterp`; `waymentsteele2025reply`; `lee2025seqassoc`; `xing2025purified` |
| **dose–response versus binary** | E1.1, E5.4 | **ADJACENT on method, OPEN on substrate.** Dose ladders exist on MSA masking and on steering strength, with a documented non-monotonic optimum. Nobody titrates a *biological co-input*. | `kalakoti2025afsample2`; `jedryszek2026probing`; `mitjavila2026afsample2t` |
| **cross-class transfer** | E7.2, E0.5 | **ADJACENT on coverage, OPEN as transfer.** Several papers span classes; none holds a class out and tests transfer. And class B is where the biology predicts the *largest* partner effect. | `heo2022multistate`; `khaleq2026hyaline`; `hilger2020gcgr` |
| **what an inactive-directing co-input would be** | E7.1, E4.4, E2.3 | **OPEN, and possibly unanswerable.** The `nanobody` tag fires on three papers and none of them runs a predictor. Being unable to name a good candidate is itself a reportable result. | `tran2026nanogs` (wet lab); `georgiou2025heterogeneity` (review) |
| **MSA subsampling with and without ligand** *(added second pass)* | E8.1, E8.2, E8.3 | **OPEN.** Exactly one paper carries `factors-crossed` — MSA masking × partner presence — and it has no ligand channel at all; a second candidate (`cheng2026af3cluster`) is unread and explicitly untagged pending its PDF. Our own Block D varied depth **apo-only** and the manuscript says so about itself. | `mitjavila2026afsample2t`; `xing2025purified`; `cheng2026af3cluster` |
| **the per-backbone apo floor** *(added second pass)* | E9.1, E9.2, E9.3 | **ADJACENT.** Deep sampling is routine (5 to 6,000 per target in the corpus); spending the budget *asymmetrically by measured cell variance* is not, and neither is reporting the floor as a result. | `yu2026domainmotion`; `ku2026promise` |

## 5.2 Directions that came out of the data, not the documents

Seven, ordered by how much I would want to run them.

1. **Strip the bulk and the decoy arm becomes decisive (E1.3).** Block B's scramble sits on
   the tail of a 354-residue subunit, so 97% of the partner is unchanged and occupancy
   drowns the signal — which is exactly why the decomposition puts 55% on presence. At
   21 residues the scramble *is* the entire partner. The same control, at a different
   length, changes from confounded to conclusive. This is the most under-appreciated
   consequence of the length ladder and it is not stated in any existing document.

2. **The panel already contains a single-residue natural experiment (E1.6).** Gi1's α5-CT
   is `IKNNLKDCGLF` and Gt's is `IKENLKDCGLF` — one substitution. Gs is `QRMHLRQYELL`, all
   eleven. The motif `N4-L5-K6` is conserved across Gi, Gt, Gq and G12 and broken in Gs.
   A sensitivity floor and a mechanistic hypothesis are both sitting in
   `data/block_b/02_constructs/construct_build_report.md` and neither has been used.

3. **Is it the α5, or is it the cleft? (E7.6)** The arrestin finger loop occupies the same
   cavity by a different evolutionary route and is 15 residues. It is already built and was
   never run. It is a *biological* positive control that the bulk control cannot substitute
   for, and `georgiou2025heterogeneity`'s note that β-arrestin-biased signalling acts on
   TM7 rather than TM6 makes a falsifiable prediction our two-axis predicate is uniquely
   able to test: the finger loop should move NPxxY more than tilt. If it works as well as
   the α5-CT, the paper's central claim narrows — and it should.

4. **Nobody has run the instrument where it is supposed to be useful (E7.3).** Every
   receptor in every block has both references. The selling point of an intrinsic predicate
   is that it works on a receptor whose active state has never been solved, and there are
   nine such Class A receptors in the snapshot. It is cheap, it is ungradeable, and it is
   the only design in the catalogue that does not presuppose its answer. The corpus makes
   this sharper than it looks: of 78 papers surveyed, **exactly three report an unqualified
   prospective result and none is of the relevant kind.**

5. **Does the model hallucinate the helix? (§6 item 5.)** `tran2026nanogs` reports that an
   unstapled linear α5 peptide is a random coil and does nothing, while the stapled one
   works only with agonist present. A co-folding model will build a helix from whatever it
   is handed. If it builds an ideal helix at every rung, the ladder is measuring *reach*,
   not *recognition*. Recording partner-chain helicity and partner-chain pLDDT per row is
   the difference between a result and an artefact, and neither is in any existing
   specification.

6. **The 21-mer is unseen by construction, and that is a quantitative argument (E4.3).** No
   wild-type 21-residue α5-CT appears with a receptor in any deposited structure; the only
   isolated-peptide precedents are short, engineered, pre-cutoff opsin entries. So the
   peptide arm is anti-memorization *by design*, not by a date filter — which is a stronger
   argument than a holdout and costs nothing. It is also the reason to run the 21-mer before
   the 11-mer.

7. **A third campaign already adjudicates a disagreement between two others (E8.3).** Block
   B's apo arm was never read as an independent replication of Block D's D1 tier, and it is
   one: 28 shared cells, a different campaign, a different scorer, and D1's point estimate
   inside Block B's 95% interval on 26 of 28. That is worth more than it costs — it
   converts Block D's most-flagged open question from a hypothesis into a narrowed one, and
   it establishes that the apo floor is reproducible across campaigns, which nothing in the
   project currently claims. **Cross-block replication of the apo arm should be a standing
   check, not something noticed once.**

8. **Predict the peptide's own state, not just the receptor's.** Every experiment in this
   project reads one chain. At peptide length the partner's predicted conformation, its
   insertion register and its confidence are all measurable and none has ever been reported.
   `junker2026peptidedesign` shows PAE over-estimates precisely where a GPCR peptide is
   misplaced, so a register error is the failure mode to expect — and the one metric we hold
   would not catch it, exactly as recorded for 6E67.

## 5.3 Three things that would be new and that I would not run

Stated so they are not proposed later as though nobody had considered them.

- **A fifth backbone.** Architecture independence is already the strongest structural
  argument in the paper at four; a fifth adds a bit of information and multiplies every cost.
- **Steering inside the model** (trunk scaling, pair-representation transforms, guidance).
  This is a crowded and fast-moving field — `lee2026confornets`, `suzuki2026pairscaling`,
  `suzuki2026conforflux`, `li2026embedding`, `tang2026steeraf`, `richman2025conformix`,
  `jung2026boltzperturb` — and it is a different paper. The whole point of this one is that
  the handle is *biological* and a user could supply it.
- **Scaling to the GPCRome.** `miglionico2026atlas` already co-folded 801 receptors × 13 Gα
  and `pandyszekeres2024gproteindb` released 5,595 complexes. Both verified no state. Going
  bigger without the instrument is what the introduction criticises; going bigger *with* it
  is a resource paper, not this one.

---

# 6. What I could not determine, and what would settle it

1. **Whether the redo should re-run Blocks A and B or build on them.** Both are internally
   sound and their row data is complete. But if E0.1 moves the thresholds, every rate in
   both changes, and if the panel extends to 64, the denominators change too. The axes are
   continuous and stored, so *re-scoring* A and B under a new threshold is free — but a
   64-receptor panel means 24 receptors have no apo or cognate arm at all. **Settled by:**
   deciding E7.5 first. If the panel extends, A and B need their two arms re-run on the 24
   new receptors (24 × 4 × 2 × 50 = 9,600 predictions) and everything else is free.

2. **Whether Block C's 22,400 crossed predictions can be joined to a new campaign, or
   whether E2.2 must re-run.** They were scored by a different scorer, on a different
   reference set, on a panel of 36 that overlaps ours partially, and `CLAIMS.md` forbids
   comparing a Block C number to a Block A/B rate because the predicate saturates there.
   **Settled by:** `rows.tier3.v2.csv` plus the scorer SHA. If the scorer matches Block B's
   `04243c45` the join may be legitimate; if not, E2.2 is `real` and costs 22,400.

3. **Whether OpenFold3 has a datable training cutoff.** Asked in Block D (ask 4) and
   unanswered. Without it, one of four backbones cannot enter E4.1's stratification.
   **Settled by:** one sentence from upstream, or by dropping OF3 from the memorization
   analysis and saying why.

4. **How the 80 threshold rows were selected** — by crystallographic tier, or by curated
   state label. This is `[PI]` at `methods.tex:117` and it determines whether the *current*
   instrument is circular. E0.1 makes the question moot going forward but not backward, and
   the Methods still has to say which. **Settled by:** the answer to Block A's D19, which
   costs no compute; somebody knows.

5. **Whether a linear 21-mer is a meaningful input to these models at all.**
   `tran2026nanogs` says the unstapled peptide is a random coil and inactive. A co-folding
   model will fold whatever it is handed and may well build a helix that does not exist in
   solution. **If it does, is that a result about receptor activation or about the model
   hallucinating helicity?** I cannot answer this from the repo. **Settled by:** running
   E1.1 with the partner-chain helicity and partner-chain pLDDT recorded per row (C4), and
   by reporting the peptide's own predicted secondary structure beside every state call. If
   the models build an ideal helix at every rung, the ladder measures reach and not
   recognition, and the paper must say so.

6. **Whether the effect is the α5 or the intracellular cleft.** E7.6 (arrestin finger loop)
   is designed to answer it and I do not know which way it will go. If the finger loop works
   as well as the α5-CT, the paper's claim narrows from "the α5 C-terminus drives the active
   state" to "an occupant of the cleft does", which is a materially weaker and more honest
   result — and one the bulk control alone would not distinguish, because the finger loop is
   a *biological* occupant.

7. **Whether the panel should be a census or a matched subset.** A census of 64 is the
   strongest sentence for Q-A1, but ConfoRNets' rule filters on construct quality (at most
   one engineered mutation per structure), and adopting theirs makes the instrument depend
   on GPCRdb's activation-degree annotation — the exact circularity E0.1 exists to escape.
   **Settled by:** deciding whether the panel rule may reference a curated state
   annotation at all. If it may not, the rule has to be "both states deposited" with a
   resolution and method floor, which is available for all 726 off-panel structures and was
   not available in any drop we received.

8. **The real cost ceiling.** Nothing in the repo records how long a prediction takes on
   which backbone, or what the compute budget is. Every `real` figure above is a count of
   predictions, not of hours, and the ranking would change if one backbone is ten times
   more expensive than another. **Settled by:** one line from the pipeline team, and it
   should be requested alongside the protocol.

9. **Whether D3's `full` MSA rung is the same input condition as an unmanipulated run.**
   *(Added second pass.)* Block D's own caveat calls this a hypothesis and says it was not
   verified; my work above narrows it — Block B independently reproduces D1 on 26 of 28
   shared cells and sides with D1 on the contested one, and D3's value is a ~3.7σ draw, so
   undersampling is ruled out — but narrowing is not settling. The panel-level agreement
   (within 3.2 points on all four backbones) bounds the average drift and cannot exclude a
   per-cell one. **Settled by:** the realised MSA row count per prediction, which costs
   nothing and answers it directly; failing that, the single-cell n=500 rerun the caveat
   itself proposes. **Until one of them lands, no depth slope should be quoted and no depth
   experiment should be dispatched** — an x-axis whose top point may be a different
   condition is not an axis.

10. **The right sampling budget for a mixed apo cell.** I can show that 50 is too few —
    a binomial standard error of ~7 points on a cell whose ladder step is ~0.33 — and that
    D1's 500 gives ±2–4. I cannot show where between them the curve flattens, because no
    campaign has run the same cell at two budgets under one pipeline. **Settled by:** a
    staircase on three or four of the mixed cells E9.1 names — 50 / 100 / 200 / 500 on one
    backbone, roughly 3,400 predictions — before the main grid is sized. This is the
    cheapest thing in the document that could change the cost of everything else in it, and
    it belongs to `redo/spec/RUN_MATRIX.md` to decide, not here.

11. **Whether `cheng2026af3cluster` is a second `factors-crossed` paper.** *(Third pass.)*
    Its note is abstract-level and explicitly withholds the tag — "Do not tag
    `factors-crossed` until the PDF is read" — while describing a method that combines MSA
    clustering with co-folded binders. That is the same shape as E8.1. If the tag lands,
    "exactly one paper crosses an MSA manipulation with a co-input" becomes "two", and the
    second is on an AF3-lineage backbone, which is closer to us than
    `mitjavila2026afsample2t`'s AF2. **Settled by:** reading one PDF. It is the cheapest
    open item in this document and it protects a sentence in the paper.

12. **Whether our own reference set defines "active" partly by arrestin coupling.**
    *(Third pass.)* `khaleq2026hyaline`'s active-state label rule counts arrestin-coupled
    structures as active. If ours does the same, E7.6's arrestin arm is partly circular and
    so is any sentence contrasting G-protein-directed against arrestin-directed states.
    **Settled by:** a free pass over `data/block_b/09_references/reference_audit.csv` and
    the 80 reference rows, checking the partner chain of every active reference — which is
    request 2 of `rebuttals/PANEL_EXPANSION.md` and has not been run. Note that nothing in
    this project currently checks the sequence of any non-receptor chain, which is how the
    4X1H mis-annotation survived two audits.
