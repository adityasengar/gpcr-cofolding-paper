# CAMPAIGN.md — what the redo should now be

> **CORRECTION, 2026-09-12 — the D-C baseline figures below are WRONG and were
> corrected after this document was written.** The baseline is **9 receptors in 8
> clusters, interaction MDE 0.431**, and the worklist is **SEVEN receptors**, not
> six. The error came from intersecting the modality columns with the Block C g4
> census, which records that a `full_agonist` row was *dispatched* — not whether
> that ligand was a peptide. CCKAR moved. The reliable test is `is_peptide=false`
> AND a non-empty `smiles`, **on both roles**; a row is not a curation.
> Reproduced independently. Aditya's D-C decision stands and the gain is slightly
> larger than these numbers show. Authority: `DECISIONS.md` (D-C WORKLIST) and
> `LIGAND_CURATION_PROPOSAL.md`. Figures in this document are left as written
> rather than silently patched, so the correction is visible.


**Written 2026-09-11, after `spec/DECISIONS.md` F-1…F-9 landed.** This is a decision
document, not a plan to accept whole. Aditya picks; everything below is costed so that
picking is possible.

**What it supersedes.** Nothing. `CATALOGUE.md` stays as the menu, `RUN_MATRIX.md` stays
as the cost model, `PANEL.md` / `SEQUENCES.md` / `SEQ_RECEPTORS.md` / `COUPLING.md` /
`GROUP0_SYSTEMS.md` / `GROUP1_SYSTEMS.md` stay as the frozen specs. This document says
which parts of them survive contact with the nine findings, and what the campaign should
be instead.

**What is frozen and is not reopened here.** The 30-receptor primary panel in 29 paralogy
clusters; the sequence set; the cognate map; both preflight gates. They survive the
findings intact — I checked each against each finding and none is disturbed. The
statistical unit is the paralog **cluster**, n = 29.

---

# 0. The answer in one page

**The redo was designed against a belief about how the original campaign ran. Six of its
premises were wrong, and exactly one of them is expensive.**

The expensive one is **F-5**. The α5-CT ladder varies partner length, and on three of the
four backbones it silently varies the alignment regime at the same time: a short excised
Gα fragment retrieves one homolog, a full subunit retrieves fifteen thousand, and the
paired-MSA axis those three backbones switch on when a second chain appears is degenerate
at one end of the ladder and rich at the other. **A monotone ladder would be exactly what
a pairing artefact looks like.**

The good news is that three of the four mitigations are already in the frozen spec or are
free, and the fourth is a four-line harness fix:

1. `SEQUENCES.md` §6 already mandates **partner-MSA-free at every rung including
   `R7_full`** — that removes the confound by construction rather than by measurement.
   But **it is not implementable in the harness as delivered** (§3.3). This is the one
   blocking engineering item in the whole campaign.
2. **Chai-1 never pairs.** It is the built-in falsification: if the ladder has the same
   shape on Chai as on the three pairing backbones, pairing is not driving it. Free — Chai
   is already in the grid, and nobody has written this down.
3. **The ladder's zero should not be `R0_apo`.** It should be a length-matched non-Gα
   chain at each rung. That holds chain count and pairing mode constant along the
   informative contrast, and the sequences (`polyA`, `gcn4_window`) are already built.
4. **Measure the depths before spending anything** — 212 distinct partner sequences,
   hours of wall-clock, no GPU.

The other five findings are cheaper and mostly make the campaign *smaller*:

- **F-1/F-2 (the instrument).** Report one predicate, not two. NPxxY-OH, off-panel
  calibrated, with the TM6 tilt as a *reported second axis* and never a conjunct — its
  reference separation has no dynamic range and it is circular against GPCRdb's own
  inactive pole on the same atom pair. Drop the confidence early return; without that,
  **title clause 3 is not computable at all**, because the state call is a function of
  pLDDT by construction. **P7 — "pLDDT does not separate" — can be computed today on Block
  A's 9,490 rows for zero cost. It is a title clause with no result and it has been free
  the whole time.**
- **F-7 (the ligand axis).** Block C's "cognate" arm was apo-vs-arbitrary-Gα, so nothing
  from it transfers. The redo already resolves the partner per receptor and gates it
  (B16). What changes is scope, and it is worse than `RUN_MATRIX` assumes: on the frozen
  panel only **16 receptors in 15 clusters** carry a small-molecule agonist *and* a
  small-molecule antagonist, and only **10 receptors in 9 clusters** are both
  small-molecule-complete and already curated by Block C. At k = 9 the ligand × partner
  interaction is powered to **0.41** — larger than every Block B decomposition term except
  cognate−apo. **The ligand arm is unpowered as it stands, and the fix is curation, not
  compute.**
- **The decoy rule.** A defensible one is specified in §5.3. My recommendation is to
  **build it, put it behind a gate that can reject, and make the decoy arm conditional on
  that gate passing on ≥12 clusters** — not to run it unconditionally. It bears on no
  title clause.
- **F-8/F-9 (unit and guards).** On the frozen panel cluster ≈ receptor (one cluster of
  two, 28 singletons), so the unit question is nearly vacuous *here* and must still be
  gated, because the extension tiers reintroduce multi-member clusters. The three output-
  vs-input receipt assertions are the cheapest hardening available and they are
  pre-conditions, not extras.

**Costs.** Pre-flight **0 GPU** (plus a 40-prediction timing probe). Pilot **9,040**. Core
**128,800**, or **94,000** in the lean variant. Referee-proofing **+58,120**. Options
**+68,280**. Cumulative through the core is **137,840 predictions = 1.1× everything
delivered in Blocks A–D, 7.7% of the naive full factorial**, and 2.9–19.1 days wall on the
25-H100 pool depending on which end of the unclosed 13× two-chain cost bracket is true.
**Closing that bracket costs 40 predictions and should be the first GPU spent.**

**One thing got cheaper.** The date-stratified holdout, costed at 7,200 new predictions in
`RUN_MATRIX` G8, is **free**: on the frozen 30 the Protenix cutoff (2021-09-30) splits the
panel 16 / 14 receptors and 16 / 13 clusters, and Chai-1's splits it 21 / 9. It is a
stratification of the core ladder, not an arm.

---

# 1. The nine findings, and what each one does to the design

Plain first: **four findings change what we run, three change how we read it, and two
change what we must build before running anything.**

| finding | what it does to the design | cost of responding |
|---|---|---|
| **F-1** predicate is single-metric | Drop the two-instrument conjunction. Report NPxxY-OH as the predicate and tilt as a second reported axis. Class B/F instrument question dissolves — the frozen panel is 30 Class A receptors. | free |
| **F-2** state call is not confidence-independent | Drop the early return. **Precondition for title clause 3.** Carry `confidence_flag` as a reported column. | free (scorer change) |
| **F-3** 9.08 applied / 9.0815 derived | Record both, separately, in Methods. Re-derive on our own calibration population anyway (Group 0). | free |
| **F-4** no Gα-side numbering | Already answered: CGN convention frozen in `SEQUENCES.md` (G.H5 = 26 exactly, G.S6 → C-term = 36). Send it. | free |
| **F-5** ladder varies length and pairing regime together | **§3.** The single biggest design change. Four mitigations, one of which is a blocking harness fix. | 0 GPU pre-flight + a harness fix + ~1,200 predictions of pilot contrast |
| **F-6** no MSA metadata on any row | Already answered: `g1_recording_spec.tsv` carries `partner_msa_mode`, `partner_msa_depth`, `partner_msa_depth_uniref90`, `receptor_msa_depth`. Keep. Add an alignment **sha256** per chain. | free |
| **F-7** Block C cognate arm was blanket `alphas` | Nothing from Block C's partner axis transfers. Its **ligand curation** still does, for 14 of the frozen 30. Keep B16. | free (already gated) |
| **F-8** stated unit ≠ implemented unit; P7 never computed | Declare the unit once, implement once, gate it with a planted defect. **Compute P7.** | free |
| **F-9** nothing compares output to input | Three assertions in a post-run receipt, plus the delivery contract refusing a run that cannot answer them. | free |

## 1.1 The two findings that change what we must build first

**F-5 needs a harness change we do not yet have** (per-chain MSA control — §3.3), and
**F-9 needs a receipt the pipeline does not write** (§9). Both are cheap. Both are
impossible to add after dispatch. Neither is negotiable if the ladder is to mean anything.

## 1.2 What none of the findings touched

The panel, the cognate map, the sequence set, the rung definitions, both gates. I checked
each frozen object against each finding:

- F-5 threatens the *interpretation* of the rungs, not their construction.
- F-7 threatens the cognate assignment method, and ours is structure-read (Option A,
  Aditya 2026-09-11) with `g1_preflight` **B16** enforcing that every row carries both the
  supplied family and the reference tip. It is the fix for F-7, already in place.
- F-4 is answered by the CGN convention already frozen.
- F-8's unit is the paralog cluster, already the declared unit, and `B9` already enforces
  one-per-cluster on the primary panel.

---

# 2. Every catalogued experiment: survives, changes, dies

**Plain first: of the 46 catalogued experiments, 21 survive unchanged, 19 change, and 6
die.** Nothing dies because it is uninteresting; each death is a finding removing its
premise, its power, or its interpretability.

**A counting correction I owe you first.** The brief I was given, `CATALOGUE.md`'s own
header and `RUN_MATRIX.md:4` all say **"33 experiments in 9 groups."** The document
enumerates **45 `### E…` headings in 10 groups (Group 0 through Group 9)**, one of which
(`E6.2 / E6.3`) carries two experiments — so **46 experiments in 10 groups**. I treated
this as my own miscount first and re-derived it three ways; the count is 46. The "33 in 9"
line predates the second pass that added Groups 8 and 9 and was never updated. It is the
project's own `[[scope-is-asserted-where-it-is-most-read]]` pattern, in two headers. All
46 are assigned below.

## 2.1 Group 0 — the instrument

| id | verdict | why |
|---|---|---|
| **E0.1** recalibrate off-panel | **SURVIVES**, promoted to blocking | Unchanged by any finding, and F-1 makes it the *only* calibration that matters: the instrument that actually ran is the one axis it calibrates. |
| **E0.2** concordance vs an independent index | **SURVIVES** | Rides on E0.1's measurement pass. Note the scope limit already recorded: `paajanen2026activation` excluded arrestins, so option (c) cannot check an arrestin arm. |
| **E0.3** admit a third state | **SURVIVES** | 21 Intermediate structures, pre-committed reading rule. Unaffected. |
| **E0.4** report axes continuously | **SURVIVES**, promoted | F-1 makes this the *substitute* for the second instrument rather than a robustness extra. The tilt axis becomes a reported axis, not a conjunct. |
| **E0.5** decide the class B/F instrument | **DIES** as an experiment, **SURVIVES** as one Methods sentence | The frozen primary panel is 30 Class A receptors. There is no class B or F receptor in it, so there is nothing to instrument. `g0_preflight` **G0-10** additionally records that the class F tilt uses the wrong atom pair (2×46–6×37 instead of 2×44–6×31). Option (a) — say the work is Class A — is now the panel's decision, not a choice. Class B transfer survives separately as T4-optional. |

## 2.2 Group 1 — the ladder

| id | verdict | why |
|---|---|---|
| **E1.1** the length ladder | **CHANGES**, and this is the main change in the document | **F-5.** The rungs stay; the baseline, the alignment regime and the reading change. §3. |
| **E1.2** bulk control | **CHANGES** | The bulk control is no longer three loose candidates: `SEQUENCES.md` supplies `R6b_a5perm` (full subunit, α5 permuted in place — the true bulk control) and `R6c_a5polyA`. The non-Gα chains (`ubiquitin`, `KaiB`) become the *second* bulk control, not the first. Still exposure-stratified per `RUN_MATRIX` §10.5(a). |
| **E1.3** composition controls at peptide length | **CHANGES — its stated rationale was backwards** | The catalogue says "at 21 residues the partner's MSA is essentially empty, so scramble and wild type differ in sequence but not in alignment depth — which *removes* the Block B confound." `SEQUENCES.md` §6 shows the opposite: the Gα α5-CT is among the most conserved 21-mers in the proteome (a 21-mer endothelin retrieved 732 rows in this project's own cache) while a scramble retrieves ≈1. **With partner MSA on, WT-vs-scramble at ct21 is a pure depth contrast — a stronger confound than Block B's, not a weaker one.** The arm is only decisive MSA-free. |
| **E1.4** family swap at peptide length | **CHANGES** | Survives as a design; its power does not. The frozen panel is Gi/o 22, Gs 6, Gq/11 2, **G12/13 zero**. Gs→Gi is powered at 6; Gi→Gs at 22; Gq is n=2 and should be reported as a bound, not a test. |
| **E1.5** per-position scan | **CHANGES** | Must run at `ct21`, MSA-free, with the partner-MSA audit as a reportability gate (already in `RUN_MATRIX` §10.5(b)). `g1_preflight` additionally flags two declared no-op cells (Gq positions 4 and 5 are already Ala) — run them, label `is_noop=true`, count them as within-arm WT replicates. |
| **E1.6** Gi/Gt single-residue pair | **SURVIVES**, gains a sibling | `COUPLING.md` supplies a second natural minimal pair, GoA/GoB (1 substitution at ct11, 4 at ct21, both human, both bona fide primaries). Run both or neither. |
| **E1.7** Gα alone vs heterotrimer | **SURVIVES**, stays last | Still a harness change (three-chain schema). `SEQUENCES.md` freezes Gβ1 P62873 SV3 / Gγ2 P59768 SV2 and warns chain-order sensitivity is untested — run at least one order-swapped cell. |
| **E1.8** uncoupling point mutants | **CHANGES — it got much cheaper** | `SEQUENCES.md` verified F376/R380/L388 against the fetched Gs sequence: all three sit inside `ct21`, so the mutants can be made **at peptide length**, not only as full subunits. It becomes an arm of the ladder rather than a separate construction job. Restricted to the 6 Gs receptors. |
| **E1.9** partner MSA on/off | **CHANGES — promoted from optional to load-bearing** | **F-5.** This is no longer "coevolution vs sterics"; it is the measurement of how much the confound is worth. `SEQUENCES.md` §6.1(3) already promotes it. It belongs in the pilot. |

## 2.3 Group 2 — the ligand axis

| id | verdict | why |
|---|---|---|
| **E2.1** export state calls on Block C | **CHANGES — its value drops sharply** | **F-7.** The arm it would export is apo vs *arbitrary Gα* on 35 of 40 receptors. It is still worth having (the apo × ligand half is unaffected) but it no longer "closes half of clause 2". |
| **E2.2** the real 2×2 | **SURVIVES**, rescoped | **F-7** kills the cheap path (re-exporting Block C's 22,400 as the crossing). Re-running clean was already the honest option; it is now the only option. Panel is **16 receptors / 15 clusters** small-molecule-complete (9 clusters curated today), not 17 clusters of a 32-receptor core. |
| **E2.3** efficacy ladder | **DIES** for this campaign | Bottlenecked on inverse-agonist and partial-agonist curation that does not exist for the frozen panel, and it bears on no title clause. Revisit if T3's ligand axis returns a graded result. |
| **E2.4** agonist vs decoy ligand | **CHANGES — conditional on a new rule** | **The decoy rule is not what its module claims** (§5.3). The existing 14,400 `decoy_lig` predictions were scored against a decoy set that fails its own property window on 3–5 of 6 axes and is systematically uncharged where the real ligands are cationic. Exporting them answers `yu2026domainmotion` with a bad negative. Rebuild the rule, or do not run the arm. |

## 2.4 Group 3 — confidence

| id | verdict | why |
|---|---|---|
| **E3.1** restate arm- and receptor-conditionally | **SURVIVES**, promoted to blocking | **F-2.** It cannot be done at all under the inherited scorer: below pLDDT 50 the call *is* the confidence. Redo it with the early return removed. |
| **E3.2** the operational test | **SURVIVES** | Free, done, and the corrected seed-grain number (300/319, 6.0% of cells showing any seed disagreement) strengthens it. |
| **E3.3** confidence on the supplied partner chain | **SURVIVES**, promoted | **F-5** gives it a second job: `plddt_partner_chain_mean` at a depth-1 rung is the closest thing we have to a readout of whether the model is folding a peptide it has no information about. Benchmark to beat: `miglionico2026atlas` AUC 0.762 for *coupling*. |
| *(new)* **P7** | **NEW — must be added** | **F-8.** The pre-registered null that pLDDT does not separate was never computed; `analyse_block_c_tier1_headline.py:383-386` emits `"descriptive_placeholder"`. It is title clause 3 and it is free on Block A's 9,490 rows once F-2 is fixed. |

## 2.5 Group 4 — memorization

| id | verdict | why |
|---|---|---|
| **E4.1** date-stratified holdout | **CHANGES — it became free** | Costed at 7,200 in `RUN_MATRIX` G8. On the frozen 30 it is a *stratification of the core ladder*: Protenix 2021-09-30 splits 16/14 receptors and 16/13 clusters; Chai-1 2021-01-12 splits 21/9 and 21/8. Boltz-2 2023-06-01 splits 4/26 and is not usable. OpenFold3 is still undated. **Three of four backbones get a stratification for zero predictions.** |
| **E4.2** exposure vs effect size | **SURVIVES**, promoted to a hard predecessor of the bulk control | Per `RUN_MATRIX` §10.5(a): `yu2026domainmotion`'s decisive covariate is training composition (40.3 pp) not the co-input (9–12 pp). Median split declared before dispatch. |
| **E4.3** the WT 21-mer as unseen input | **CHANGES** | Still true and still free, with one correction from `COUPLING.md`: OPSD's 4X1H **does** contain a deposited 11-residue α5 analogue (`VLEDLKSCGLF`, 4 substitutions from WT Gt1). So the statement is "no **wild-type** α5-CT of any length appears with a receptor", and OPSD is both the best positive control available and the one receptor where the deposited tip is engineered. |
| **E4.4** post-cutoff inactive binder | **SURVIVES**, still blocked on a candidate | Unchanged. The D2 defect that motivated the caution is **corrected** in `SEQUENCES.md` §: the placeholder nanobody was written into the YAMLs but the arm was removed before dispatch — 0 rows. No contrast compared an arm with itself. The SHA-before-dispatch requirement stands anyway. |

## 2.6 Group 5 — mechanism

| id | verdict | why |
|---|---|---|
| **E5.1** steric exclusion at panel scale | **SURVIVES** | Needs coordinates, not predictions. It also now carries a second job: it supplies the fragment-restricted interface reference that `RUN_MATRIX` §3.5(3) needs for a placement covariate that works from 11 to 394 residues. |
| **E5.2** per-BW decomposition | **DIES** as an ask, **SURVIVES** as our own analysis | It was a `free (them)` ask for `s4_bw_decomposition.json`. F-7 means that file describes an arm we cannot use. Compute it on our own rows instead. |
| **E5.3** report the ensemble | **SURVIVES** | Free, unaffected. |
| **E5.4** dose–response on engagement depth | **SURVIVES**, promoted | **F-5.** Engagement depth is the placement covariate the ladder needs; `junker2026peptidedesign` shows a confidence metric will not catch a misplaced GPCR peptide. It stops being a nice extra. |
| **E5.5** what the failures have in common | **SURVIVES** at low priority | Post-hoc unless pre-registered afresh. |

## 2.7 Group 6 — the delivery contract

| id | verdict | why |
|---|---|---|
| **E6.1** row-level delivery contract | **CHANGES — it grows** | **F-6 and F-9.** Add per-chain alignment sha256 and row count, `n_chains`, `partner_chain_count`, `checkpoint_sha`, `wall_time_s`, `gpu_model`, per-structure `output_sha`, and an `attempt` counter. `MAP_LIFECYCLE` §7.3 and §8.5 name all of them. |
| **E6.2 / E6.3** ship `rows.tier3.v2.csv` and Block D's rows | **CHANGES — demoted from rank 1** | This was the catalogue's number-one item on the grounds that everything downstream conditions on it. **F-7 breaks that logic**: the highest-value thing those files unblocked was the ligand × partner crossing, and on a blanket-`alphas` cognate arm that crossing is apo vs arbitrary-Gα. They are still worth asking for — Block D's depth rows and Block C's apo × ligand half are unaffected — but the redo no longer waits on them. |
| **E6.4** pair seeds across arms | **SURVIVES**, blocking | Free before dispatch, impossible after. Blocks A and B both failed it (1,898 distinct `seed_outer` across 380 Block A cells). |

## 2.8 Group 7 — new directions

| id | verdict | why |
|---|---|---|
| **E7.1** what an inactive-directing co-input would be | **SURVIVES** as Discussion | Free to write. |
| **E7.2** class B ladder | **CHANGES — deferred** | It needs a class B instrument (E0.5) that the frozen panel gives us no reason to build. Keep as an option; it is the sharpest venue biologically (`hilger2020gcgr`: in class B the agonist alone produces no TM6 opening) and the cheapest way to buy a transfer claim later. |
| **E7.3** prospective arm | **SURVIVES**, corrected to 8 receptors | `PANEL.md` resolves the 9-vs-8 discrepancy: `q9wtk1_cavpo` is the same receptor as `lt4r1_human`. Eight. |
| **E7.4** size the interaction before running it | **SURVIVES**, and **changes method** | It was to be run by injecting effects into Block C's existing 22,400-row design. F-7 makes that design the wrong one. Run the injection on the **pilot's** own rows instead, or analytically from the cluster SDs in `RUN_MATRIX` §4.3. Either way it must precede the ligand arm. |
| **E7.5** extend the panel to the census | **DIES** as a uniform multiplier, **SURVIVES** as one replication arm | Already the `RUN_MATRIX` position and the frozen panel's. Census replication at three rungs, 2,880 predictions, Tier 4. |
| **E7.6** arrestin finger loop | **CHANGES — its reagent is mislabelled** | `SEQUENCES.md` establishes that `partners.fasta`'s `arrestin_FL` is **not** the finger loop: its 15 bytes are β-arrestin-1 P49407 residues 22–36, a β-strand of the N-domain sandwich; the receptor-interaction region is 45–86. And `arrestin_Ctail`'s bytes are not held at all. **The arm needs its sequences built from scratch before it can run**, and the circularity check against our own active references still has to pass first. |

## 2.9 Group 8 — MSA depth

| id | verdict | why |
|---|---|---|
| **E8.1** cross depth with partner | **SURVIVES**, and gains urgency | It is the novel cell and it is now also a direct probe of F-5's mechanism: if receptor-MSA depth and partner presence act on one mechanism, a partner flattens the depth slope. |
| **E8.2** cross depth with ligand | **SURVIVES** | Panel shrinks to 16 receptors / 15 clusters — 9 clusters with curation in hand. |
| **E8.3** fix the depth anchor | **SURVIVES**, blocking, and **it got worse** | `MAP_MSA` §6.2 adds a second mechanism nobody had: `subsample_msa.py:106-107` returns the input unchanged when `len(entries) <= depth`, while the manifest still records the nominal depth. A "512" arm on a 300-row alignment is a 300-row arm labelled 512. Combined with `PARTA_D3.md:128`'s **12 of 28 cells outside D1's Wilson interval**, the `full` rung is not a condition, it is a name. Emit realised depth. |

## 2.10 Group 9 — the apo floor

| id | verdict | why |
|---|---|---|
| **E9.1** characterise the floor | **SURVIVES**, mostly done | Free. |
| **E9.2** targeted deep apo sampling | **CHANGES — shrinks to the bistability bound** | `RUN_MATRIX` §6.2 already recommends 8,000 over 48,000, and F-2 sharpens the reason: a cell "pinned at 0" under the inherited scorer may be pinned by the pLDDT gate rather than by geometry. **Re-read the floor with the early return removed before deciding any cell is pinned.** That is free and it may move which cells qualify. |
| **E9.3** report every rung against its own floor | **SURVIVES**, adopt as a convention | Free. Never pool a rate across backbones. |

## 2.11 The six that die, and the one sentence each

- **E0.5** (class B/F instrument) — the frozen panel has no class B or F receptor.
- **E2.3** (efficacy ladder) — curation that does not exist, bearing on no title clause.
- **E5.2** (per-BW decomposition, as an *ask*) — F-7 makes the file describe an unusable arm.
- **E7.5** (panel extension as a multiplier) — it is a 1.6–2× uplift to fix power problems
  that three arms have.
- **E6.2/E6.3** are **not** in this list: they are demoted, not killed.
- **E2.4** is **not** in this list either: it is conditional on §5.3's gate passing.

That is four outright deaths plus two conditionals. The "6" in the plain-language opener
counts E0.5, E2.3, E5.2-as-ask, E7.5, and the two conditionals if their gates fail. Stated
this way so the number is not doing work the table does not support.

---

# 3. F-5 — the ladder confound, and what to do about it

## 3.1 The problem in plain words

We want to say: *the more α5 you give the model, the more active the receptor gets.* The
danger is that the models are not responding to the peptide at all — they are responding
to how much **alignment** came with it.

Three of the four backbones (Boltz-2, OpenFold-3, Protenix) run a *paired* alignment search
when the input has two protein chains. A paired alignment needs homologs on both sides. If
the partner chain retrieves one row — itself — the paired axis carries one row no matter
how deep the receptor's alignment is, and "paired" collapses into "unpaired". So on those
three backbones, as the partner gets longer, the paired axis goes from degenerate to rich.
**Length and alignment regime move together, and a monotone ladder is what both would
produce.**

The measurements that make this real are `paper_af3`'s own, from their Chai cache
(`msa_depth_report.md:351-376`, reproduced in `SEQUENCES.md` §6):

| sequence | aa | depth |
|---|---:|---:|
| `DAMGO` | 5 | **1** |
| `substanceP` | 11 | **1** |
| `arrestin_FL` | 15 | 84 |
| `endothelin1` | 21 | **732** |
| `gcn4_leucine_zipper_33` | 33 | 224 |
| `random_helix_40mer` | 40 | **1** |
| **`arrestin_Ctail`** | **41** | **1** |
| `Gg2` | 71 | 3,191 |
| cognate Gα | 350–394 | 11,904–14,986 |

**Depth is not monotone in length. The predictor is naturalness.** `arrestin_Ctail` is the
governing case: 41 residues, an excised fragment of a larger protein, depth 1 — exactly
our α5-CT rungs.

## 3.2 Two things I got wrong on the first reading, and the correction matters

**(a) I expected the short rungs to return depth 1. `SEQUENCES.md` §6 argues the opposite,
and it is more likely right.** The Gα α5 C-terminus is among the most conserved 21-residue
windows in the proteome; a 21-mer endothelin retrieved 732 rows. So the expected shape is
**WT rungs deep, control rungs at 1** — which is worse, not better, because it means the
*identity* contrast (WT vs scramble at ct21) is a pure depth contrast unless the partner
runs MSA-free. **It also means the catalogue's stated rationale for E1.3 is backwards.**

**(b) The Block B decoy confound is not a pairing confound.** `SEQUENCES.md` §6 establishes
that Boltz, Protenix and OpenFold-3 all read the decoy tail edit as aligned uppercase
(6/6 each); **Chai is the outlier at 0/40**, and Chai's `pairing_key` is empty on every row
of every file. So Block B's confound is *content and depth, per backbone* — not pairing.
I had been carrying it as a pairing story and it is not one.

Both of these are the project's standing rule in action: the first run is wrong before the
data is.

## 3.3 The four mitigations, evaluated and costed

### M1 — Measure first. **Blocking. 0 GPU.**

Submit every distinct partner sequence the campaign will dispatch to the servers the
campaign will use, and record the row count, unpaired **and** paired.

**Scope, computed here from the frozen inputs:** the five Gα subtypes the frozen panel
needs (Gi1 ×20, Gs ×6, Gq ×2, Gi3 ×1, Gt1 ×1) give **35 ladder-rung sequences + 25
mid-rung sequences + 168 distinct control sequences = 212 distinct partner sequences**,
plus 21 α5-null constructs. `g1_preflight` already carries this as a pending dependency
("~60 distinct peptide-rung sequences"); the real number, with the control set included,
is 212.

**Three servers, not one.** ColabFold (`mode=env` for unpaired, `mode=pairgreedy-env` for
paired — `MAP_MSA` §6.3 shows the prewarm only ever requested `env`, so the paired number
has never been measured by anyone), Protenix's own server, and the Chai cache builder.
`MAP_MSA` §12 Q6 is unresolved and matters here: `step7_dispatch_gate.py:1246-1248`
allowlists `substanceP` as "too short for MMseqs2 MSA search", yet it *has* a 1-row
`.aligned.pqt`. **We do not know whether a short rung errors out or silently returns
query-only.** The pre-flight settles it for our sequences directly.

**What would change the design.** If WT rungs come back deep and controls come back at 1,
the MSA-free condition (M2) is mandatory rather than preferred. If everything comes back at
1, the confound is smaller than feared and MSA-free becomes a cheap confirmation. Either
way we know before spending.

### M2 — Hold the alignment regime constant by construction. **Blocking, and it needs a harness fix.**

`SEQUENCES.md` §6.1 already mandates **partner-MSA-free at every rung including
`R7_full`**, and `g1_preflight` **B7/B8** already enforce that every row declares a
partner-MSA condition and that MSA-free is the primary one. That is the right call and I
endorse it without reservation: it converts the ladder from a length × depth surface into a
length axis.

**It is not implementable in the harness as delivered, on three of four backbones.**
From `MAP_MSA` §8.5 and `MAP_LIFECYCLE` §2.4:

- `scorer/propose.py:471-472` and `:599-600` assign **the same MSA path to every protein
  chain** when `msa_a3m_path` is a plain string. The per-chain dict form exists
  (`_boltz_msa_field`, `propose.py:358-360`) and is labelled *"D3 multi-chain support,
  currently unused"* — **no caller.**
- `_of3_apply_msa_paths` applies to every chain with `molecule_type == PROTEIN`
  (`propose.py:458`), which includes a peptide partner and a peptide ligand.
- **Chai has no `MSA_A3M_PATH` branch at all** (`MAP_LIFECYCLE` §9.1). Its partner MSA
  comes only from the content-addressed `.aligned.pqt` directory, so "partner MSA off" on
  Chai means writing a query-only `.aligned.pqt` for the partner sequence — which is
  feasible, and is in fact what ColabFold returns for a depth-1 sequence anyway.
- On OpenFold-3, `use_paired_msas` is set from the **protein chain count**
  (`propose.py:485`, `:524-525`), not from whether we supplied alignments. So even
  MSA-free, the flag differs between `R0_apo` (monomer, false) and every other rung (true).

**Consequence, and it is the sharpest statement in this section:** with M2 in place, the
pairing regime is **constant across R1…R7 and differs only at R0**. That is a step, not a
gradient — which is far better than the inherited design, because the step sits exactly at
the one contrast (partner absent vs present) where it is unavoidable. M3 then removes even
that.

**Cost of the fix:** three edits in `propose.py` (pass the dict form), one Chai cache
builder change, and one smoke test per backbone that reads back what the model consumed.
It is a day of engineering, and it must land before the pilot.

### M3 — The ladder's zero is not apo. **Free; the sequences already exist.**

Replace `R0_apo` as the reference level of the length axis with a **length-matched non-Gα
chain at each rung**. `seq_controls.tsv` already carries `polyA` and `gcn4_window` at ct11,
ct15, ct21 and a5helix (26); the set needs extending to a5plus (36) and the mid-rungs,
which is a generator change in `build/`, not a new design.

Why this is the strongest single move: at each rung the WT arm and its matched null differ
in **sequence identity alone** — same length, same chain count, same pairing mode, same
`use_paired_msas` flag, same number of tokens. The contrast that carries the title becomes
`ct21_WT − ct21_polyA` rather than `ct21_WT − apo`, and every mechanism that operates on
"a chain is present" is differenced out. `R0_apo` stays in the grid as the floor and as the
join to Blocks A/B; it stops being the baseline of the headline claim.

`gcn4_window` is the better of the two nulls for the helicity question (matched helical
propensity) and `polyA` the better for the "any helix will do" upper bound. Run both at
ct21; run `polyA` alone elsewhere.

**One caveat to carry:** GCN4 is a coiled-coil, helical *as a dimer*. Supplied as a monomer
it may not come back helical. That is why `partner_chain_helicity_frac` and
`partner_helix_span_len` are required columns, and it is why both nulls are run rather than
one.

### M4 — Let Chai falsify it. **Free; nobody has written this down.**

**Chai-1 does not pair.** Three independent lines of evidence in `MAP_MSA` §3: the cache
builder calls `generate_colabfold_msas(protein_seqs=[seq], …)` with a one-element list; the
cache is deduplicated by sequence hash across the whole project, so one file is shared by
every complex that sequence appears in; and a measured pass over all 120 cache files found
`pairing_key` empty on every row.

So on Chai, adding a partner adds a chain and nothing else about the alignment. **If the
ladder has the same shape on Chai as on the three pairing backbones, pairing is not driving
it.** That is a built-in falsification test at zero cost, and it is the reason the pilot
should run on **two** backbones rather than one (§6.2) — a change from `RUN_MATRIX` §3.2,
which nominates Boltz-2 alone.

Two caveats, both real. Chai's apo floor is 2–4× every other backbone's (0.287–0.323
against 0.069–0.127), so it has the least headroom and the comparison must be of *shape*,
read against its own floor (E9.3). And Chai is the backbone where the Block B tail edit did
not reach the model at all (0/40) — so M4 depends on M1 and on the pre-flight content
readback (§8, PF-3) passing on Chai specifically.

### M5 — Measure the residual. **E1.9, promoted into the pilot.**

Run the partner-MSA **ON** condition at `ct21` and at `R7_full`. If the ladder is the same
with and without a partner alignment, the confound is bounded empirically and the result is
reportable as such. If it is not, we have measured the size of the thing we were worried
about, which is a publishable result in its own right and is `E1.9`'s original question
answered on a real axis.

## 3.4 What I would not do

- **Run the ladder single-sequence on the receptor too.** It would hold the regime constant
  and destroy everything else the receptor's alignment does.
- **Rely on depth-as-covariate alone.** `g1_recording_spec.tsv` already carries
  `partner_msa_depth`, and it should — but a covariate that is near-perfectly collinear
  with the factor of interest cannot be adjusted for. Carry it; do not lean on it.
- **Drop the short rungs.** They are the paper's title. The answer is to control the
  regime, not to avoid the question.

---

# 4. The instrument — F-1, F-2 and title clause 3

## 4.1 One predicate, not two. Plainly.

**Recommendation: NPxxY-OH alone as the predicate; TM6 tilt reported as a second continuous
axis and never ANDed with it.** Three reasons, in order of weight:

1. **Their collapse was sound and is not in dispute** (`DECISIONS.md` F-1): NPxxY-OH alone
   reaches 94.3% self-classification (32/36 A→A, 34/34 I→I) on 70 of 80 tier-1 rows; the
   tilt is TM6 re-measured (r = +0.913 against DRY) and the pack metric self-classifies at
   only 71.1%.
2. **The tilt has no dynamic range on our population.** Block A: reference-separation SD
   1.17 Å against NPxxY's 5.22 Å, going negative on two backbones under Class-A
   restriction.
3. **The tilt is circular where NPxxY is not.** `MAP_REFERENCES` §7.3 shows a 2×2 of
   (axis × pole) in which **exactly one cell of four is clean, and it is NPxxY against the
   inactive pole** — because GPCRdb's own inactive-pole definition uses the same atom pair
   as the tilt. That is true of their calibration and of ours, for the same reason.

**What we lose by dropping the conjunction:** four Class A receptors (EDNRA, EDNRB, GRPR,
HRH3) have non-Tyr at 5.58 or 7.53 and are NPxxY-blind. Note that `PREREG.md:100` and
`switch_signal.py:100-104` both *promise* a fallback to midpoint-crossing on the TM6 axis
for exactly these receptors, and `MAP_REFERENCES` §5.3(e) establishes **there is no such
fallback anywhere in the code** — the string `metric_coverage_insufficient` does not occur
in any `.py` file in the bundle. So we inherit no fallback; we build one or we report those
receptors as unevaluable.

**On the frozen 30 this is a small problem: EDNRB and HRH3 are in the panel, GRPR and
EDNRA are not** (GRPR is one of the ten chimeric-reference exclusions, EDNRA likewise). Two
receptors, and `g0_preflight` **D1** (NPxxY OH vs Cα) is the open decision that may recover
them. Deciding D1 as Cα costs comparability with `paper_af3`'s 9.08; deciding it as OH
costs 42 of 199 Class A receptors in the calibration set. That is Aditya's call and it is
listed in §10.

## 4.2 Drop the early return, because clause 3 depends on it

`prediction_is_active_like` returns `"inactive"` **before any geometry is read** when
`confidence_flag == "low"`, and `confidence_flag` is a pure function of
`min_plddt_at_anchor` (`switch_signal.py:116-117`, `orchestrator.py:613-622`), verified
across all 32,000 Block B rows. `paper_af3` confirm it is intentional and call it "a real
circularity, not an artefact".

**The paper's third title clause is that confidence does not track state correctness. Under
that scorer, confidence *determines* the state call below pLDDT 50.** The clause is not
weakly supported; it is not computable.

Two consequences that go beyond "fix the scorer":

- **Every "pinned at 0" apo cell must be re-read.** `E9.1` counts 91 of 160 Block B apo
  cells as never firing on any of 50 samples. Some unknown fraction of those are pinned by
  the pLDDT gate, not by geometry. This is free to redo and it changes which cells E9.2
  would deep-sample.
- **Report `insufficient` as a bucket, not as a pole.** `orchestrator.py:604-607` and
  `schema.py:222` both describe the *intended* behaviour as a third bucket. The code
  returns a pole. Implement what the design note says.

## 4.3 P7, and the rest of clause 3

`analyse_block_c_tier1_headline.py:383-386` emits `"descriptive_placeholder"` for P7 — the
pre-registered null that pLDDT does not separate correct from incorrect state calls. It was
never computed, in any block.

**It is free on Block A's 9,490 rows** once the early return is removed, and it is free on
every row of the redo. Pre-register it: the statistic, the unit (paralog cluster), the
stratification (within arm, within receptor — because `DISCREPANCY_REPORT.md` D-A-25 shows
the pooled AUC of 0.60–0.96 evaporates when receptor is controlled), and the reading rule
for each outcome.

`E3.3` gives clause 3 a second, genuinely novel leg: partner-chain pLDDT at α5 positions,
against a published number to beat (`miglionico2026atlas` AUC 0.762 for coupling). If ours
discriminates *binding* but not *state*, that is the cleaner finding and it is directly
comparable to theirs.

---

# 5. The ligand axis and the decoy rule — F-7

## 5.1 What F-7 destroys, and what it leaves

**Destroyed:** any use of Block C's partner axis. `COGNATE_PARTNER_IDENTITY = "alphas"` is
hard-set in all three Block C manifest builders and assigned without consulting the coupling
table, so 35 of 40 receptors received a Gα they are not coupled to in the arm labelled
`cognate`. Block A's own code names this failure class — *"A blanket alphas would recreate
the W54 taxonomy failure"* — and ships `verify_cognate_identity.py` to catch it, which on
this evidence was never pointed at a Block C manifest.

**Left standing:** Block C's *ligand* curation, its apo-arm results, and its 40,000 scored
predictions' apo × ligand half. A ligand supplied to an apo receptor is unaffected by what
the (absent) partner would have been.

**Still unanswered by the pipeline team, and I design around it both ways:** was the blanket
`alphas` a decision, or a recurrence? **If a decision**, someone should tell us what it was
for, and the Block C partner arm becomes "receptor + Gαs" — a legitimate if oddly-named
experiment, and one we could in principle join to a Gαs-supplied arm of our own. **If a
recurrence**, the arm is simply void. The redo is identical either way: it resolves the
partner per receptor from `coupling_cognate_map.tsv` and `g1_preflight` **B16** refuses any
row that carries a supplied family without a reference tip. Nothing in our design depends
on the answer; only the disposal of 18,400 existing predictions does.

## 5.2 The ligand panel is much smaller than anyone has costed

**I got this wrong on the first pass and the correction is the most consequential number
in this section.** My first count required `n_agonist_smiles > 0`, which gave 17 receptors
/ 16 clusters. But `n_agonist_smiles` counts a SMILES string for a **peptide** — EDNRB
reports 9 agonist SMILES and its `agonist_modalities` is `peptide;protein`. Counting on
modality instead:

| set | receptors | clusters |
|---|---:|---:|
| frozen primary panel | 30 | 29 |
| …with **any** agonist and **any** antagonist curated by Block C | 14 | 13 |
| …with a **small-molecule** agonist **and** a small-molecule antagonist | **16** | **15** |
| …**both of the above** — small-molecule-complete *and* already curated | **10** | **9** |
| …with no antagonist of any kind | 3 (APJ, GPR52, MTR1A) | — |
| …whose only agonists are peptide or protein | 8 (AGTR1, C5AR1, CCR2, EDNRB, MCHR1, NK1R, NPY1R, NTR1) | — |

`RUN_MATRIX` costs the ligand and depth arms on **CORE-L17 = 17 clusters** drawn from a
32-receptor core. The real ligand-ready set on the frozen panel is **9 clusters today and
15 after curation.** The arithmetic barely moves; the power statement collapses:

| k clusters | interaction MDE (80% power, cluster SD 0.435) |
|---:|---:|
| **9** (small-molecule **and** Block-C-curated — what we have) | **0.406** ← *corrected: 8 clusters, MDE 0.431* |
| 13 (Block C curation as-is, peptide agonists included) | 0.338 |
| **15** (all small-molecule pairs, after curating 6 receptors) | **0.314** |
| 29 (whole panel, if the peptide-agonist receptors are solved) | **0.226** |

**At k = 9 the interaction MDE is 0.406.** *(Corrected 2026-09-12: the baseline is k = 8, MDE 0.431 — see the banner at the top.)* Block B's decomposition terms are +0.400,
+0.333 and +0.082. So as things stand the ligand × partner interaction is powered to
detect only an effect as large as the *entire* cognate−apo main effect. **That is not a
test; it is a decoration.**

**Stated in advance, and in the paper:** whatever k we run at, the interaction is powered
for effects ≥ the number in that table and no smaller. Anything below it is reported as
*unestimable at this n*, with the number, never as absent — `suzuki2026conforflux`'s
position and the honest one.

**The cheapest power upgrade in the campaign is curation, not compute, and it is now
necessary rather than nice.** Curating a small-molecule agonist and antagonist for the 6
frozen-panel receptors that have the modality but not the curation takes k from 9 to 15
and the MDE from 0.406 to 0.314, **for zero GPU hours**. Going beyond 15 means solving the
8 peptide-only-agonist receptors, and that is a different experiment: **a peptide agonist
is a third protein chain, and on OpenFold-3 it flips `use_paired_msas` exactly as a peptide
partner does.**

**One specific hazard, and it is live.** `partners.fasta:endothelin1` is **21 residues —
exactly `ct21`'s length** — and EDNRB is on the frozen panel. An EDNRB agonist arm crossed
with `R3_ct21` would put **two unlabelled 21-mers into one prediction**, either of which
the model may place in the intracellular crevice. `chain_role_json` is a required column
for this reason (`g1_recording_spec.tsv`), and no peptide-agonist receptor may be crossed
with a peptide partner rung without it.

## 5.3 A decoy rule we could defend — and my recommendation about whether to use it

**What theirs actually is** (`MAP_LIGANDS_AND_ANALYSIS` §2): a hand-picked FDA-approved
drug, one hard-coded per receptor in a Python dict, chosen on a "known other target, no
known activity here" prose argument. The only gate that can reject is Morgan Tanimoto
< 0.30. The ±20% property window across six axes is **computed and never enforced** —
`_build_small_mol_report:1576-1589` records `within_tolerance` per axis and no branch
raises. All 8 Tier-1 decoys miss the window on **three to five of six axes**; three Tier-3
`chosen_because` strings say in prose that the pick is outside the window and was taken
anyway. And "Decision A" makes every aminergic decoy neutral where the real ligands are
cationic, so the decoy arm differs from the ligand arms **systematically in net charge**.
The module's own docstring title says "property-matched decoy ligands".

That is not a controlled negative for pocket occupancy. It is a different experiment.

**A rule we could defend, stated so it can be pre-registered:**

> **D-RULE.** For each receptor, define the *reference ligand* as its curated **full
> agonist** (not the mean over all real ligands — a mean over mixed pharmacological roles
> is what produced their n=1 and n=2 windows). Build a candidate pool from ChEMBL
> restricted to compounds with (i) no measured activity at the receptor, (ii) no measured
> activity at any receptor in its **paralog cluster**, and (iii) ≥1 measured activity at
> some unrelated target. Compute eight axes on every candidate and on the reference:
> MW, cLogP, TPSA, HBD, HBA, rotatable bonds, ring count, and **formal charge at pH 7.4**
> (not `Chem.GetFormalCharge` on the SMILES as written — that is what produced the charge
> asymmetry). Accept a candidate iff every continuous axis is within ±20% of the
> reference's, every integer axis within ±1, **charge exactly equal**, and Morgan
> (r = 2, 1024 bit) Tanimoto < 0.30 against every curated real ligand of the receptor
> **and of every receptor in its paralog cluster**. From the accepted set draw **k = 3**
> decoys per receptor by a seeded draw recorded in the row.
>
> **The gate rejects.** A receptor with fewer than 3 accepted candidates is reported as
> *decoy-unavailable*, named in the paper, and excluded from the decoy arm. No candidate is
> ever taken "anyway".
>
> **The report is regenerated, never frozen into a CSV cell.** Tanimoto values, the
> `n parseable` count and the charge flag are recomputed at dispatch time from the current
> ligand table and hashed. (Theirs drifted: the ADRB2 decoy notes still reference
> `S-(-)-propranolol`, replaced by `(S)-alprenolol` on 2026-09-04, and nothing noticed.)

Three decoys per receptor rather than one is the single biggest improvement: it converts
"is this one molecule odd" into a within-receptor distribution, and it makes a null
interpretable.

**My recommendation is nevertheless to hold the decoy arm back.** The decoy answers "is the
pocket response ligand-specific?" — a referee's question, and one `yu2026domainmotion`
already answers in the negative for 82 enzymes. **Title clause 2 is "the agonist alone does
not drive the active state", and that is answered by agonist-vs-no-ligand at fixed partner
condition, not by agonist-vs-decoy.** So: build D-RULE, run it, see how many clusters
survive its gate, and run the arm **only if ≥12 clusters pass**. Below that it is a
2×2 nobody can read. Cost of finding out: curation time, zero GPU.

## 5.4 What the ligand axis should actually be

The minimum that bears on clause 2 is **ligand {none, agonist} × partner {absent,
present}**, one panel, one scorer, one predicate, interaction estimated with its interval
reported. That is T2.8 below. Antagonist as a third ligand level and `ct21` as a third
partner level are the extension (T3.1) — they add pharmacological direction and connect the
ligand axis to the ladder, but they are not what the title needs.

---

# 6. The recommended campaign

## 6.1 The shape, in plain words

**Nothing expensive runs until four cheap things have come back.** Then a two-backbone
pilot on the whole panel decides whether there is a ladder at all. Then the core campaign
runs the ladder, its matched nulls, its identity controls and the ligand 2×2. Then two
tiers of referee-proofing and options.

Conventions, all inherited and all measured rather than assumed:

- **Statistical unit: the paralog cluster, n = 29.** On the frozen panel there is exactly
  one two-member cluster (AA1R + AA2AR) and 28 singletons, so cluster and receptor nearly
  coincide *here*. That is not a reason to skip the gate — the extension tiers reintroduce
  multi-member clusters and F-8 is what happens when the unit drifts.
- **n = 10 per cell (2 seeds × 5 samples) for pooled claims; n = 50 (5 seeds × 10) for
  per-cell claims.** `RUN_MATRIX` §2.1: going 50 → 10 costs ≤0.002 of half-width on every
  pooled Block B contrast. Block C's variance decomposition says cut seeds before samples
  (σ²_seed / σ²_within-seed = 0.11).
- **Seeds paired across arms within a receptor.** Free now, impossible later.
- **Every rung reported against its own backbone's apo floor as well as absolutely; no rate
  is ever pooled across backbones.**
- **Both axes shipped continuously on every row; the state call is derived.**

## 6.2 Tier 1 — the pilot. 9,040 predictions.

Two backbones: **Boltz-2 and Chai-1**. This is a change from `RUN_MATRIX` §3.2, which
nominates Boltz-2 alone. The extra 4,520 predictions buy the F-5 falsification test (M4):
Chai never pairs, so a matching ladder shape on Chai is direct evidence that pairing is not
driving the result. At this price it is not a close call.

| id | what | panel × bb × cells × n | predictions |
|---|---|---|---:|
| **T1.1** | ladder, 7 rungs (R0, ct11, ct15, ct21, a5helix, a5plus, R7_full) | 30 × 2 × 7 × 10 | **4,200** |
| **T1.2** | length-matched nulls: `polyA` at ct11 / ct21 / a5plus | 30 × 2 × 3 × 10 | **1,800** |
| **T1.3** | gap-bridging rungs `M1_h4s6` (44–47), `M2_h4` (61–63), `M4_he` (204–221) | 30 × 2 × 3 × 10 | **1,800** |
| **T1.4** | partner-MSA **ON** contrast at ct21 and R7_full | 30 × 2 × 2 × 10 | **1,200** |
| **T1.5** | two-chain timing probe, 1 receptor × 4 backbones × {apo, R7_full} × 5 | 1 × 4 × 2 × 5 | **40** |
| | | | **9,040** |

**Question each answers, and what each result would mean:**

- **T1.1.** *Is there a ladder?* Positive (ordering holds, ct21 − matched-null CI excludes
  zero): proceed. Negative: the peptide rungs do not separate, and the core's 128,800 would
  buy a flat line — stop and report a bounded null with its MDE. **Clause 1.**
- **T1.2.** *Is the ladder about the α5 or about a chain being there?* This is the control
  that makes T1.1 readable at all. If WT and matched-null are indistinguishable at ct21,
  the peptide arm is occupancy and the paper's first clause does not survive in the form
  it is written. **Clause 1.**
- **T1.3.** *Does the curve bend at the 50-residue placement-regime boundary?*
  `junker2026peptidedesign` stratifies GPCR peptide complexes at ≤50 vs >50 because
  placement accuracy changes regime there, and our ladder's only gap is 36 → 350.
  `GROUP1_SYSTEMS.md` §7 brackets that boundary properly: `R5_a5plus` is 36, `M1_h4s6` is
  44–47 (below), `M2_h4` is 61–63 (just above) — **15 residues apart instead of a
  314-residue leap.** If the three mid-rungs lie on the curve, the ladder is one
  dose–response; if they break, it is two segments and must be analysed as two.
  **Clause 1, interpretation.**
- **T1.4.** *How much is the pairing regime worth?* This is F-5 measured rather than
  argued. A null (same ladder with and without a partner alignment) bounds the confound; a
  difference sizes it. Either is reportable. **Clause 1, validity.**
- **T1.5.** *What does a two-chain prediction actually cost?* The bracket is 13× wide
  (22.7 s measured apo vs a 5 min/pred planning estimate never validated). Everything in
  §7 has a 13× uncertainty until this returns. **Nothing scientific; it prices the rest.**

### The Stage 1 → Stage 2 gate, written before the pilot runs

> Tier 2 dispatches only if, on the pilot at cluster grain over 29 clusters:
> **(a)** `ct21_WT − ct21_matched_null` has a 95% cluster-bootstrap CI excluding zero on
> **both** backbones; **and** **(b)** the rung ordering
> R0 ≤ ct11 ≤ ct15 ≤ ct21 ≤ a5helix ≤ a5plus ≤ R7_full holds on at least 4 of the 6
> adjacent steps at cluster grain; **and** **(c)** the pilot's pre-flight MSA depths
> (PF-1) and the partner-MSA-ON contrast (T1.4) do not jointly indicate that the ladder's
> ordering is reproduced by depth alone.
>
> If (a) fails → stop; report the pilot as a bounded null with its MDE.
> If (a) holds and (b) fails → the ladder is a step, not a dose–response; run
> R0 / ct21 / R7_full only and drop ct11, ct15, a5helix, a5plus — saving ~24,000.
> If (c) fails → the ladder is not reportable as a length effect; escalate to Aditya
> before any Tier 2 spend.
>
> **The ligand 2×2 (T2.8) and the depth cube (T3.2) have no gate.** They are unoccupied
> ground and a null there is publishable, which is exactly when a gate is inappropriate.

## 6.3 Tier 2 — the core. 128,800 predictions (lean variant 94,000).

Four backbones, frozen panel, n = 50 where a per-cell claim is wanted and n = 10 where the
claim is pooled.

| id | what | grid | n | predictions | clause |
|---|---|---|---:|---:|---|
| **T2.1** | the ladder, 7 rungs | 30 × 4 × 7 | 50 | **42,000** | 1 |
| **T2.2** | matched nulls at ct21: `polyA` + `gcn4_window` | 30 × 4 × 2 | 50 | **12,000** | 1 |
| **T2.3** | matched nulls at ct11 / a5plus / `R6a_da5` | 30 × 4 × 3 | 10 | **3,600** | 1 |
| **T2.4** | gap-bridging rungs `M1_h4s6`, `M2_h4`, `M4_he`, `M5_dHD`, pooled | 30 × 4 × 4 | 10 | **4,800** | 1 |
| **T2.5** | identity controls at ct21: scramble ×5 + face_scramble ×3, pooled | 30 × 4 × 8 | 10 | **9,600** | 1 |
| **T2.6** | identity controls at ct21, per-cell: `reversed` + 1 scramble + 1 face_scramble | 30 × 4 × 3 | 50 | **18,000** | 1 |
| **T2.7** | bulk controls: `R6b_a5perm`, `ubiquitin`, `KaiB_2QKEE` | 30 × 4 × 3 | 50 | **18,000** | 1 |
| **T2.8** | ligand 2×2: {none, agonist} × {apo, R7_full} | 16 × 4 × 4 | 50 | **12,800** | 2 |
| **T2.9** | deep-apo bistability bound, 4 receptors | 4 × 4 × 1 | 500 | **8,000** | — |
| | | | | **128,800** | |

**A framing point that costs nothing.** T2.2 and T2.3 are not new arms.
`ct21@gcn4_window` is already one of `GROUP1_SYSTEMS.md`'s three non-Gα bulk arms in
G3a/G3b, and `polyA` at ct21 is already one of G4's composition-control cells. **What
changes is which contrast is the headline**, not what gets dispatched. The arms exist; the
paper's central number becomes `WT(L) − matched_null(L)` instead of `WT(L) − apo`. Two
mechanical notes: `gcn4_window` derives from P03069's 33-residue zipper, so it **cannot
reach `R5_a5plus` (36)** — `polyA` carries the matched-null role there alone; and
`gcn4_window` and `polyA` are **byte-identical across all five panel Gα families at every
rung**, so each is one construct per length, not five.

**Questions, arms and readings:**

- **T2.1 + T2.2 + T2.3 together are the headline.** The claim is
  `WT(L) − matched_null(L)` as a function of L, read at cluster grain, per backbone,
  against each backbone's own floor. Positive: an α5-CT peptide, supplied as a co-input,
  drives the active state, and the response is graded in length. Negative at every rung:
  the models respond to a chain, not to this chain — which contradicts clause 1 and is
  worth publishing as such. **Clause 1.**
- **T2.5 + T2.6.** *At peptide length, where nothing but the tail remains, does identity
  matter?* Five scrambles rather than one, so the permutation can be treated as a random
  effect ("is it this permutation, or permutations in general"). `face_scramble` is the
  sharp control — it preserves the amphipathic face and destroys residue identity, so
  `WT − face_scramble` is identity net of geometry, and `face_scramble − scramble` is
  geometry net of identity. This is the arm that converts Block B's confounded decoy into a
  decisive one, **and only MSA-free** (§3.2a). **Clause 1.**
- **T2.7.** *Is the 55% occupancy term specificity or literal occupancy?* `R6b_a5perm` is
  the true bulk control — full subunit, α5 permuted in place, bulk and composition and
  helical propensity preserved, identity destroyed. Analysed with the exposure median split
  declared in advance (PF-9), because `yu2026domainmotion`'s decisive covariate is training
  composition (40.3 pp) and not the co-input (9–12 pp). **Gate:** `R6a`/`R6b`/`R6c` may not
  fold as Gα — α5 packs against the Ras domain — so `ras_domain_ca_rmsd_to_R7` and Gα-chain
  pLDDT are checked on the pilot leg before the full arm dispatches. A bulk control that
  arrives as a molten globule is mass-matched to nothing. **Clause 1.**
- **T2.8.** *Does the agonist alone drive it, and do ligand and partner compose?* Four
  cells, one panel, one scorer, interaction estimated with its interval. Positive
  interaction: the two inputs are not additive and the paper has a mechanism story.
  Null: reported as *unestimable below 0.31 at k = 15* (or **0.41 at k = 9** if the six
  receptors are not curated — §5.2), never as absent. **Clause 2 — this is the only item in
  the campaign that bears on it, and it is the item whose power depends entirely on a
  curation decision rather than on compute.**
- **T2.9.** *Does any backbone have no second basin above 1%?* n = 50 gives a Wilson upper
  bound of 7.1% when 0 of 50 fire; n = 500 gives 0.8%. That difference is the bistability
  claim and nothing else in the plan can write it. Four receptors, per-cell CIs
  authoritative, **panel mean is not a claim** (4 receptors span 4 clusters, so
  cluster-boot ≡ receptor-boot). **Run it after F-2's early return is removed**, since
  which cells are "pinned" may change.

### The lean variant — 94,000, and exactly three levers

| lever | change | saving |
|---|---|---:|
| **T2.1-lean** | n = 50 on R0 / ct21 / R7_full only; n = 10 on ct11, ct15, a5helix, a5plus | −19,200 |
| **T2.6-lean** | 2 identity controls per-cell instead of 3 (`reversed` + 1 `face_scramble`) | −6,000 |
| **T2.7-lean** | `R6b_a5perm` at n = 50; `ubiquitin` and `KaiB` at n = 10 | −9,600 |

All three trade **per-cell** resolution for pooled resolution and none touches a pooled
interval (`RUN_MATRIX` §2.1). What they cost is per-receptor figure panels at the middle
rungs and at the second bulk control. **If per-receptor panels are wanted in the main
figure, do not take T2.1-lean.**

## 6.4 Tier 3 — referee-proofing. +58,120.

| id | what | grid | n | predictions | clause |
|---|---|---|---:|---:|---|
| **T3.1** | ligand axis extended: + antagonist, + `ct15`/`ct21` as partner levels | 16 × 4 × 5 | 50 | **16,000** | 2 |
| **T3.2** | depth cube: 3 depths × 3 rungs × 2 ligand levels | 16 × 4 × 18 | 10 | **11,520** | — |
| **T3.3** | partner-MSA ON at ct21 + R7_full, 4 backbones, per-cell | 30 × 4 × 2 | 50 | **12,000** | 1, validity |
| **T3.4** | family swap at ct21 (Gi↔Gs) | 30 × 4 × 1 | 50 | **6,000** | 1 |
| **T3.5** | per-position Ala scan at ct21, 1 backbone | 10 × 1 × 21 | 20 | **4,200** | 1 |
| **T3.6** | uncoupling mutants F376A/L388A(+R380A) at ct21 and a5helix, Gs receptors | 6 × 4 × 4 | 50 | **4,800** | 1 |
| **T3.7** | **wet-lab-matched rungs `ct13`, `ct17`, `ct19`, pooled** | 30 × 4 × 3 | 10 | **3,600** | 1 |
| | | | | **58,120** | |

- **T3.1** adds pharmacological direction and joins the ligand axis to the ladder.
- **T3.2** is the novel cell: depth × co-input crossed inside one model, which exactly one
  paper in 81 does (`mitjavila2026afsample2t`, AF2, no ligand channel). **Blocked on E8.3**
  — the `full` rung must be shown to be the same condition as an unmanipulated run, or the
  x-axis has a different condition at its top point. Two independent reasons to doubt it:
  12 of 28 D1/D3 cells disagree, and `subsample_msa.py:106-107` returns the input unchanged
  when the alignment is shallower than the target while the manifest still records the
  nominal depth.
- **T3.3** promotes the pilot's F-5 contrast to per-cell on all four backbones. Run it only
  if T1.4 showed a difference worth resolving; if T1.4 was null, this is 12,000 predictions
  confirming a null and belongs in Tier 4.
- **T3.4** is honest about its power: Gi→Gs is 22 receptors, Gs→Gi is 6, Gq is 2. Report
  the first as a test and the others as bounds.
- **T3.5** must run at ct21 and MSA-free, with the partner-MSA audit as a **reportability
  gate**: a null whose arms differ in sequence but not in alignment is a retrieval
  artefact, which `masters2025physics` states as the mechanism of its own null. Two Gq
  positions are already Ala — run them, label `is_noop=true`, count as WT replicates.
- **T3.6** is nearly free in construction: all three Gs mutation sites sit inside `ct21`,
  so E1.8 and E1.1 cross at zero construction cost. **Not at `ct11`** — F376 and R380 fall
  outside the 11-mer, so the double and triple mutants collapse to the same molecule there
  (`GROUP1_SYSTEMS.md` §8.3). Peptide-rung cells are `ct21` and `a5helix` only.
- **T3.7 is the item I would add that no existing document costs, and it is the best value
  in Tier 3.** There is a **wet-lab length titration at our exact rungs, on a receptor on
  our panel.** `mazzoni2000` tested Gαs C-terminal peptides on A2AR membranes and found
  the last 17, 19 and 21 residues most effective with "shorter peptides … not effective";
  `eddy2018extrinsictrp` used GαS **374–394** on human A2AR, which is byte-for-byte our
  `R3_ct21` (`RVFNDCRDIIQRMHLRQYELL`, sha `39355d83d34556e4`), derived independently from
  the "last N residues" rule. Adding `ct13`, `ct17` and `ct19` turns our ladder into a
  direct in-silico counterpart of a published dose series rather than a free-standing
  curve. Three warnings travel with it, all from `GROUP1_SYSTEMS.md` §12: `mazzoni2000` is
  **abstract-only** and the six-peptide enumeration reaches us through
  `dursi2011signalpeptides`, **a relay that contradicts the abstract** — nothing in the
  relay may be cited as `mazzoni2000`; the species differ (`mazzoni2000` rat,
  `eddy2018extrinsictrp` human); and **no per-rung sign may be pre-registered**, only
  monotonicity. The C379A constructs are a Gs-specific anchor arm, not rungs.

## 6.5 Tier 4 — options. +68,280.

| id | what | predictions | why it is here and not higher |
|---|---|---:|---|
| **T4.1** | gap-bridging rungs at n = 50 | 24,000 | The regime question is pooled; n = 10 answers it. |
| **T4.2** | arrestin finger loop / C-tail at matched length | 12,000 | **Its reagents do not exist.** `arrestin_FL` is mislabelled (it is β-arrestin-1 residues 22–36, a β-strand) and `arrestin_Ctail`'s bytes are not held. Build first, and pass the circularity check against our own active references. |
| **T4.3** | Gi/Gt **and** GoA/GoB single-residue pairs at ct11 + ct21 | 12,000 | A sensitivity floor for T3.5, not a headline. |
| **T4.4** | heterotrimer rung R8 | 6,000 | Harness change (three-chain schema); chain-order sensitivity untested; lipidation not modelled by any backbone. |
| **T4.5** | census replication on the 24 extension receptors, R0/ct21/R7 | 2,880 | Lets the paper say the result holds on the full 64-receptor census. Cheap; not a new arm. |
| **T4.6** | chimeric-reference tier: option A / option B / `DEPOSITED_TIP` at ct21 | 6,000 | The 10 receptors excluded from the primary panel, with the matched control that makes the exclusion defensible rather than merely declared. |
| **T4.7** | prospective arm, 8 receptors with no active reference | 4,800 | Ungradeable by construction; its value is that its design does not presuppose its answer. Pre-register the calls or it is decoration. |
| **T4.8** | post-cutoff inactive binder | 600 | Still blocked on finding a candidate. |

---

# 7. Costs

## 7.1 The model

The one measured throughput anywhere in four blocks: D3 drained 25,810 predictions on 25
H100 workers in ~6.5 h = **158.8 predictions per H100-hour = 22.67 s per prediction**
(`HEADLINE_D3_tier_d3_full_2026_09_08.md:3-6`). **D3 is apo only.** The only two-chain
figure on disk is an unvalidated planning estimate of ~5 min/pred, which is 13.2× the
measured apo rate. `matrix_cost.py` carries all three scenarios and I use it unchanged:
2.0× (linear in tokens), 4.2× (pairformer L², 774 vs 380 tokens), 13.2× (planning).

**The 13× bracket is still the largest unknown in the campaign, and T1.5 closes it for 40
predictions.**

## 7.2 The tiers

Cumulative cost through each tier, on the 25-H100 pool that actually ran D3:

| tier | predictions | cumulative | 2.0× | 4.2× | 13.2× |
|---|---:|---:|---:|---:|---:|
| **Tier 0** pre-flight | **0** (+40 in T1.5) | 0 | — | — | — |
| **Tier 1** pilot | 9,040 | 9,040 | 114 H100-h / 0.2 d | 236 / 0.4 d | 753 / 1.3 d |
| **Tier 2** core | 128,800 | 137,840 | 1,736 / 2.9 d | 3,600 / 6.0 d | 11,487 / 19.1 d |
| *Tier 2 lean* | *94,000* | *103,040* | *1,297 / 2.2 d* | *2,691 / 4.5 d* | *8,587 / 14.3 d* |
| **Tier 3** referee-proofing | 58,120 | 195,960 | 2,468 / 4.1 d | 5,119 / 8.5 d | 16,330 / 27.2 d |
| **Tier 4** options | 68,280 | 264,240 | 3,327 / 5.5 d | 6,902 / 11.5 d | 22,020 / 36.7 d |

## 7.3 In the units Aditya thinks in

| through | predictions | Block-B drops | × everything ever delivered (124,470) | % of the naive full factorial (1,792,000) |
|---|---:|---:|---:|---:|
| Tier 1 | 9,040 | 0.28 | 0.07× | 0.5% |
| Tier 2 | 137,840 | 4.31 | **1.11×** | 7.7% |
| Tier 2 lean | 103,040 | 3.22 | 0.83× | 5.8% |
| Tier 3 | 195,960 | 6.12 | 1.57× | 10.9% |
| Tier 4 | 264,240 | 8.26 | 2.12× | 14.7% |

**Comparison to the existing plan.** `RUN_MATRIX`'s MINIMAL / INTENDED / EXPANSIVE are
45,860 / 155,100 / 249,540. Mine are 9,040 / 137,840 / 195,960 / 264,240. The pilot is much
smaller (two backbones, one gate, no per-cell claims) and the core is slightly smaller
despite carrying more control arms, because the panel is 30 rather than 32, the ligand
panel is 16 rather than 17, and the date-stratified holdout became free. The difference is
not a saving to celebrate; it is what happens when the holdout stops being an arm.

## 7.4 Costs that are not predictions

| item | cost | who pays |
|---|---|---|
| Group 0 measurement pass (726 + 610 + 98 structures; ≤1,336 mmCIF downloads, ~4,000 API calls at a 0.15 s throttle) | days of labour, 1–3 GB cached, **no GPU** | us |
| PF-1 depth ladder: 212 sequences × 3 servers × 2 modes | hours of wall-clock, no GPU | us |
| Per-chain MSA harness fix (`propose.py` dict form, Chai cache path) | ~1 day engineering | them or us |
| Post-run receipt (three assertions) | ~1 day engineering | them |
| D-RULE decoy construction + gate | days of curation, no GPU | us |
| Small-molecule ligand curation for 6 frozen-panel receptors | days of curation, no GPU | us |
| `R8_hetero` three-chain input schema | harness change | them |
| `verify_partner_chains.py` multi-xref fix (it takes the **first** UniProt xref and breaks, so a Gs-scaffold/Gq-tip chimera is compared against canonical Gi2 and reports a confident wrong answer) | hours | us |
| `numpy` 1.24.4 / `scipy` 1.6.2 version conflict, and `gemmi` absent | hours | us — **before the Group 0 fitting stage** |

**The two best value-per-hour items in the whole document are both here and neither is
compute:** small-molecule ligand curation (interaction MDE 0.406 → 0.314) and the
per-chain MSA fix (without which the ladder's headline is uninterpretable).

---

# 8. The pre-flights that must run before any inference

Plain first: **these are the measurements that would change the design if they came back
wrong. None needs a GPU except a 40-prediction timing probe, and every one of them is
cheaper than discovering the same thing from 130,000 predictions.**

| id | what | cost | what a wrong answer changes |
|---|---|---|---|
| **PF-1** | **MSA depth ladder.** 212 distinct partner sequences (35 rungs + 25 mid-rungs + 168 controls, for the 5 Gα subtypes the frozen panel needs) + 21 α5-null constructs, submitted to ColabFold (`mode=env` **and** `mode=pairgreedy-env`), Protenix's server, and the Chai cache builder. Record row count per (sequence, server, mode). | hours, 0 GPU | **Everything.** If WT rungs are deep and controls are at 1, the identity controls are a depth contrast unless MSA-free; if short rungs error out rather than returning query-only, the pipeline needs a branch. |
| **PF-2** | **Per-chain MSA control, proved.** One two-chain smoke input per backbone with receptor-MSA on and partner-MSA off, then read back what the model actually consumed. | 4 predictions + 1 day engineering | If it cannot be done, M2 fails and the ladder's alignment regime is a gradient. This is the one blocking engineering item. |
| **PF-3** | **Perturbation-reached-the-model check.** For one edited arm per backbone, assert the edited residues appear **uppercase in row 0** of the alignment the model reads. | free, rides on PF-2 | Catches the Block B Chai defect (0 of 40 decoy query rows carried the scrambled tail). If it fails on Chai, M4's falsification test is void. |
| **PF-4** | **Post-run receipt, three assertions** (F-9): returned chain count == requested; each chain's returned sequence == dispatched; seed used == seed requested. Plus `n_produced == n_samples` exactly. | 1 day engineering | A monomer returned where a dimer was requested currently passes every check in the pipeline. |
| **PF-5** | **Group 0 measurement pass.** 726 calibration + 610 application + 98 pinned reference rows, both axes. | days, 0 GPU | Every rate in the redo is graded by this ruler. The set is 611 active : 115 inactive off-panel — the balancing rule must be fixed **before** fitting (open decision D4). |
| **PF-6** | **Threshold re-derivation + the instrument decision.** Reproduce 9.0815 / 9.082 / 9.08; decide one predicate or two (§4.1); decide D1 (OH vs Cα). | free | Decides which receptors are evaluable and whether our numbers are comparable to theirs. |
| **PF-7** | **P7, computed on Block A with F-2's early return removed.** Also re-read the apo floor: which cells are pinned by geometry vs by the pLDDT gate. | free | Title clause 3 has no result at all until this runs. It may also move E9.2's cell selection. |
| **PF-8** | **Ligand-completeness census** (done here: **16 receptors / 15 clusters** with a small-molecule agonist **and** a small-molecule antagonist; **10 / 9** also curated by Block C; 8 peptide-only agonists; 3 with no antagonist). | free | Sizes the entire ligand axis and its interaction MDE. At k = 9 the interaction MDE is 0.406 — the arm is a decoration until curation moves it. |
| **PF-9** | **Exposure covariate + median split, declared.** `active_frac`, `n_deposited_active`, `n_deposited_inactive` per receptor from the GPCRdb snapshot (Block B's own `deposition_count` is constant and its regression ships NaN). | free | The bulk control is uninterpretable without it on `yu2026domainmotion`'s design. Must be declared *before* dispatch. |
| **PF-10** | **α5-tip identity audit.** `ref_alpha5_tip_identity`, `ref_alpha5_is_canonical`, `ref_alpha5_pdb` per receptor. | free | On the frozen 30 the chimeric-tip receptors are already excluded, but **OPSD remains and its deposited tip is an engineered 11-mer 4 substitutions from WT Gt1**. If we supply WT and score against an engineered reference we are comparing a third thing to it. |
| **PF-11** | **Depth-anchor check (E8.3).** Realised MSA row count per prediction; one sentence on whether the `full` rung is the same condition as an unmanipulated run; the 6-receptor passthrough control. | free (them) + ~600 predictions | **Blocking for the depth cube.** 12 of 28 D1/D3 cells disagree; `subsample_msa.py:106-107` silently relabels a shallow alignment. |
| **PF-12** | **Two-chain timing probe** (T1.5). | 40 predictions | Closes the 13× cost bracket that every number in §7 carries. |
| **PF-13** | **Interaction power injection (E7.4).** Inject known effects and report the fraction of cluster-bootstrap replicates whose interval excludes zero, at k = 13, 16 and 29. | free | Turns the ligand null from unfalsifiable into bounded, and tells us whether curation is worth doing before we do it. |
| **PF-14** | **Delivery contract agreed**, with seed pairing and per-chain alignment hashing. | free | Impossible to add after dispatch. `runs/README.md` is drafted and unsent. |

**Dependency order.** PF-5, PF-6, PF-7, PF-8, PF-9, PF-10, PF-13, PF-14 are independent and
can run in parallel now. PF-1 → PF-2 → PF-3 is a chain and it gates the pilot. PF-4 and
PF-14 gate any dispatch. PF-11 gates only the depth cube. PF-12 should be the first GPU
spent.

---

# 9. The guards, each with the defect it must catch

Plain first: **this project's rule is that a check is not trusted until it has been shown
to fail.** Every guard below is listed with the specific defect to plant, because a silent
check looks exactly like a passing one — and `MAP_LIFECYCLE` §7.5(b) documents the pipeline
shipping exactly that: `sentinel_bug_seed_present: false`, evaluated on a file the chunked
run never reads.

## 9.1 Compute-layer guards — in the receipt the job itself writes

`step7_dispatch_gate.py:964-971` states the pattern in the pipeline's own words: audit
trail #9–#13 *"all shared one failure shape — configuration correct at repo layer, dropped
before the compute layer, all status signals green."* **A gate that runs on the login node
cannot see this class.** These five live in the job's own receipt.

| guard | what it asserts | plant this defect |
|---|---|---|
| **C1 — chain count** | `n_chains(output) == n_chains(requested)` | Dispatch a two-chain input and hand the receipt a monomer CIF. It must fail. |
| **C2 — chain sequence** | each returned chain's sequence == the dispatched sequence for that chain | Swap one residue in the returned chain B. It must fail. Run it specifically on a `scramble` arm, because that is the arm where the edit is the entire experiment. |
| **C3 — seed** | seed used == seed requested, **per chunk on OpenFold-3** | Point the OF3 probe at the top-level `_runner_seeds.yml` as the pipeline does. It must fail, because that file is written and never read by the chunked branch. This is the exact defect in the delivered code. |
| **C4 — sample count** | `ok` requires `n_produced == n_samples` **exactly**, every file non-zero-length and parseable | Delete 99 of 100 CIFs. Their `ok = exit_code == 0 and len(produced) > 0` returns true; ours must fail. |
| **C5 — alignment content** | the dispatched partner residues appear **uppercase in row 0** of the alignment the model read; `partner_msa_depth` and `partner_msa_sha256` are recorded | Feed a scrambled tail and a wild-type alignment. It must fail. This is the Block B Chai defect (0 of 40), and no gate in the delivered pipeline can see it. |

**C5 must be length-conditional.** Depth 1 is *correct* for a short peptide — `substanceP`
(11 aa) and `DAMGO` (5 aa) legitimately return query-only. A naive "depth > 1" guard would
false-positive on exactly the arms the campaign cares about. Gate on depth **relative to
what PF-1 measured for that sequence**, not on an absolute floor.

## 9.2 Analysis-layer guards

| guard | what it asserts | plant this defect |
|---|---|---|
| **A1 — the unit is the cluster** | every reported interval resamples `cluster_id`, and the emitted provenance field names the unit that the loop actually uses | Change the loop to resample receptors while leaving the provenance string saying `cluster`. It must fail. This is F-8 exactly: their provenance JSON declares `two_stage_cluster_resample_receptors_then_seeds` over a one-stage loop on receptor scalars. |
| **A2 — the denominator is the declared grain** | a pooled fraction over n = 10 per cell reports `n_cells`, not `n_rows`; a per-cell claim refuses a cell with n < 50 | Report a rate whose denominator is rows where the spec says cells. It must fail. Their scripts report 25 or 50 where the pre-registration says 5. |
| **A3 — no self-certifying column** | no column may vouch for its own row | Ship a `matches_claim_sheet = True` column on a row where the value disagrees. It must fail. Block A shipped exactly this. |
| **A4 — seeds are paired** | within a receptor, every arm draws the same seed set | Give one arm its own seeds. It must fail. Block A has 1,898 distinct `seed_outer` across 380 cells; Block B 3,200 across 640. |
| **A5 — no reproducible-CI defect** | `PYTHONHASHSEED` is set, and no RNG is seeded from `hash()` | Seed a bootstrap from `hash((bb, arm))`. It must fail. Eleven call sites in the delivered analysis do this, including the training-cutoff stratum CIs. |
| **A6 — the state call is confidence-independent** | the predicate reads geometry only; `confidence_flag` appears in no branch above the geometry | Reinstate the early return. It must fail. |
| **A7 — realised, not nominal** | any depth regression is fitted against `msa_depth_realised`, never a rung label | Fit against the label with `full` imputed as 4,096. It must fail. Every published depth slope in Block D is fitted this way, and Block B's own audit shows Boltz consuming 13,678 rows for one cell. |

## 9.3 Scope guards

| guard | what it asserts | plant this defect |
|---|---|---|
| **S1 — grep the short text** | section headings, caption titles, panel titles, ledger status lines and **module docstrings** carry no scope the body withdraws | Write a heading claiming a 21-residue peptide while the body says eleven. It must fail. Three module headers in the delivered bundle (`switch_signal.py`, `pocket_metrics.py`, `build_block_c_decoys.py`) assert scopes their code withdrew, and so did our own section heading on 2026-09-11. |
| **S2 — counts in headers** | any count asserted in a header (`33 experiments in 9 groups`) is recomputed from the body | Recount. It fails today: the body holds 46 in 10 groups. |
| **S3 — every path claimed absent is absent** | `analysis/audit_asks.py`, extended to `redo/` | Claim a file we hold is missing. It must fail. |

## 9.4 The three existing gates stay

`layout.py` (7 checks), `g0_preflight.py` (12 blocking + 8 dependencies), `g1_preflight.py`
(16 blocking + 7 dependencies). All pass today; I ran them. **B8** — "MSA-free on the
partner chain is the primary condition" — becomes the most load-bearing check in the tree
once §3 is adopted, and it needs a sibling: a check that the *harness* can honour it
(PF-2). A gate that enforces a declaration the pipeline cannot implement is a silent check.

---

# 10. Open decisions for Aditya

Each with options, cost, a recommendation, and the reason. Ordered by what blocks the most.

### D-A. The instrument: one predicate or two?

| option | cost | consequence |
|---|---|---|
| **(a) NPxxY-OH alone; tilt reported as a second axis** | free | Comparable to `paper_af3`'s applied predicate. Loses the conjunction the manuscript describes — which never ran anyway. 2 of the frozen 30 receptors (EDNRB, HRH3) become NPxxY-blind with no inherited fallback. |
| (b) Build a second instrument and justify it | days of Group 0 work | The only honest way to keep a conjunction. The tilt is the wrong candidate (no dynamic range; circular on the same atom pair as GPCRdb's inactive pole). A genuinely independent second axis would have to be new. |
| (c) Keep the two-instrument description | free | Not available. It describes a predicate that produced no data. |

> **SUPERSEDED 2026-09-12. This section's premise is false and the decision went the
> other way.** It was written while F-1 claimed the two-instrument conjunction never
> ran. **It ran** — Block A reproduces Class A as `npxxy AND tilt` at 100.0% on
> 7,995 rows. Option (c) above ("keep the two-instrument description — not
> available") was therefore wrong, and option (a) was chosen for a reason that no
> longer exists.
>
> **The decision taken is: keep the conjunction for Class A, calibrate NPxxY,
> inherit the tilt threshold with its provenance stated, and validate it on the
> apo/cognate contrast instead of calibrating it** — because every ground truth
> available to Group 0 for that axis is circular or retracted. Class A only: F-13
> shows the tilt fails on Class B (9 Å inter-backbone disagreement) and has no
> discriminating power on Class F.
>
> Authority: `DECISIONS.md` → **D-2026-09-12-c**.

**Recommendation: (a).** Report both axes continuously, call the state from NPxxY-OH, and
say in Methods why the tilt is reported and not conjoined. It is the defensible version of
what actually ran, and E0.4 already carries the robustness sweep.

### D-B. Does the partner chain run MSA-free? (F-5's M2)

| option | cost | consequence |
|---|---|---|
| **(a) MSA-free on the partner at every rung including `R7_full`** | 1 day engineering (per-chain MSA fix), already mandated by `SEQUENCES.md` §6.1 and `g1_preflight` B8 | The ladder becomes a length axis. The pairing regime is constant across R1…R7. Costs comparability with Blocks A/B's cognate arm, which ran partner-MSA on. |
| (b) MSA-on, depth carried as a covariate | free | The covariate is near-collinear with the factor. This is the design F-5 says is confounded. |
| (c) Both, at two rungs (E1.9) | +1,200 in the pilot, +12,000 per-cell in Tier 3 | Measures the residual. |

**Recommendation: (a) as primary and (c) in the pilot.** (a) alone leaves "how much did we
change by doing that?" unanswered, and that is the first question a referee asks. 1,200
predictions buys the answer.

### D-C. Ligand curation — and this is now a blocking decision, not a tuning one

| option | cost | interaction MDE |
|---|---|---|
| run on what is small-molecule-complete **and** already curated | free | k = 9 → **0.406** |
| accept Block C's 14, peptide agonists included | free | k = 13 → 0.338 |
| **curate small-molecule pairs for the 6 receptors that have the modality but not the curation** | days of curation, **0 GPU** | k = 15 → **0.314** |
| also solve the 8 peptide-only-agonist receptors | a different experiment | k = 29 → 0.226 |

**Recommendation: curate the 6, and scope the rest with PF-13 before deciding.** At k = 9
the interaction MDE (0.406) exceeds every Block B decomposition term but one, so the arm
cannot do its job as things stand. Six receptors of curation buys the difference between a
bounded test and a decoration, at zero compute. The 8 peptide-only receptors are a separate
question — a peptide agonist is a third protein chain and flips OpenFold-3's
`use_paired_msas` — and `endothelin1` is exactly 21 residues, the same length as `ct21`,
so one of them (EDNRB) cannot be crossed with a peptide rung without explicit chain
labelling. Run PF-13's injection at k = 9, 15 and 29 and let the answer price the rest.

### D-D. The decoy arm: run it, gate it, or drop it?

| option | cost | consequence |
|---|---|---|
| reuse their decoys | free | Indefensible: fails its own window on 3–5 of 6 axes, systematically uncharged against cationic real ligands, gate is stale relative to the ligand set it guards. |
| **build D-RULE, gate it, run only if ≥12 clusters pass** | curation, 0 GPU to find out | Answers `yu2026domainmotion` with a real negative, or tells us honestly that we cannot build one on this panel. |
| drop the arm | free | Loses a referee answer; loses no title clause. |

**Recommendation: the middle one.** It bears on no title clause, so it should not be
allowed to consume compute before its own gate has passed.

### D-E. Group 0's four open decisions — D1, D2, D3, D4

These are already `WAIT` items in `g0_preflight` and they are the PI's.
`GROUP0_SYSTEMS.md` owns them and carries a recommendation for each; **I do not override
its recommendations**, and I restate them here only with what each costs *this* campaign:

- **D1 — NPxxY OH vs Cα** *(deferred by Aditya 2026-09-11; does not block)*. OH leaves 42
  of 199 Class A receptors unevaluable and cuts the calibration set 726 → 514; Cα is
  defined on all 199 but every published number on this axis changes. **On the frozen 30
  it costs 2 receptors (EDNRB, HRH3).** GROUP0's recommendation — report both, headline
  OH, Cα as a coverage arm — is the right one and I endorse it.
- **D2 — panel expansion vs calibration reserve.** 41 of the 61 surviving calibration
  inactives, and *every* paired receptor, sit in the 32 expansion receptors. Expanding
  drops calibration inactives 61 → 20 and paired receptors to **zero**. GROUP0 recommends
  the **split** — expand onto actives-rich receptors, reserve the inactive-rich ones. I
  agree, and note it costs this campaign almost nothing: T4.5's census replication needs
  three rungs on 24 receptors and tolerates a smaller extension tier.
- **D3 — agonist-only admissibility.** Reopened, because the rule that briefly closed it
  (Q0c, activation degree = 100) was retracted the same day for encoding partner presence.
  **This is the decision that determines whether our active pole is partner-bound by
  construction** — the same limitation `paper_af3`'s set has (94% partner-bound; both
  transducer-free actives flagged for removal). GROUP0 recommends admit-flag-report-both.
  It may not be decided by appeal to our own thesis, and whatever is decided goes into
  Methods as a stated anchor choice.
- **D4 — balancing rule.** 611 active : 115 inactive off-panel, and **every resolution
  floor is also a class-balance rule** (Mann-Whitney on resolution, active vs inactive,
  p = 0.0095; a ≤2.5 Å cut gives 1.5:1 on 48 structures, no cut gives 5.3:1 on 726).
  GROUP0 recommends equal-weight headline with the others reported. *Must be fixed before
  fitting, not after.*

### D-F. Pilot on one backbone or two?

**Recommendation: two (Boltz-2 + Chai-1), +4,520 predictions.** Chai is the only
non-pairing backbone and is therefore the F-5 falsification. At 0.03% of the core's cost
this is not a budget question.

### D-H. B1B1U5 — does it stay on the panel?  **RESOLVED 2026-09-12: yes, option (c′).**

It is the jumping-spider opsin, sole member of cluster `001_009_001_inv`. Its cognate Gα
was contested: Block B assigned Gi and `COUPLING.md`'s structure-read rule gives **Gq via
9EPP**. `GROUP1_SYSTEMS.md` D6 stated it plainly: *resolve it, or the receptor leaves the
panel.*

| option | cost | consequence |
|---|---|---|
| **resolve the reference question** ← **TAKEN** | free, panel session | Keeps 30 receptors / 29 clusters. |
| drop B1B1U5 | −1 receptor, −1 cluster; pooled half-widths × √(29/28) = 1.018 | Also removes one of the two Gq receptors, leaving Gq at n = 1. |

**Recommendation: resolve it.** A 1.8% interval penalty is not the issue; halving the Gq
arm is. And the panel cannot be called a census with an unresolved member in it.

**Outcome, and two things this framing got wrong.** Aditya chose **(c′)**: reference
**9EPP**, `cognate_family` **Gq**, recorded as a spider-Gαq1-tipped chimera on a human
Gαi1 backbone, with **(e′)** — supply the spider α5 instead of the human one — offered as
an extension arm. Panel unchanged at 30 / 29. The two errors above, both corrected in
`D_H_RESOLUTION.md`: (1) ~~Rule R step 4 points at 9EPR~~ — step 4 requires a native
transducer to demote to, and **there is none**, so it never fires; (2) ~~invertebrate
visual opsins are canonically Gq~~ — that claim has **no locator** in our corpus and must
not be used as evidence. The Gq assignment rests on the deposited spider-Gq tip and the
depositors' stated design intent, not on a canon. {ref-history}

### D-G. Do we ask `paper_af3` for `rows.tier3.v2.csv` at all?

It was rank 1 in the catalogue. F-7 removes most of its value, because the crossing it
unblocks is apo vs arbitrary-Gα. **Recommendation: still ask, at lowered priority.** Block
D's depth rows and Block C's apo × ligand half are unaffected, and the four open questions
to the pipeline team (§11) should travel in one message rather than five.

---

# 11. Where I disagree with the existing design, and where I am uncertain

## 11.1 Disagreements, with the reason

1. **The pilot should be two backbones, not one.** `RUN_MATRIX` §3.2 nominates Boltz-2 as
   the sole reference backbone. That was right before F-5. Chai's non-pairing is the
   cheapest falsification of the confound and it only works if Chai is in the pilot.
2. **`R0_apo` should not be the ladder's baseline.** Every existing document reads the
   ladder as rungs against apo. Apo differs from every other rung in chain count and, on
   OpenFold-3, in the `use_paired_msas` flag. The matched-length null is the correct zero.
   No existing document says this.
3. **The date-stratified holdout is not an arm.** `RUN_MATRIX` G8 costs it at 7,200. On the
   frozen 30 it is a free stratification (Protenix 16/14 receptors, 16/13 clusters;
   Chai 21/9, 21/8). Spending 7,200 on it would be spending to recover something the core
   already contains.
4. **`E6.2/E6.3` should not be rank 1 any more.** The catalogue ranks shipping
   `rows.tier3.v2.csv` above everything because everything conditions on it. F-7 breaks
   that: the highest-value thing it unblocked is now known to be a different experiment.
5. **`E1.3`'s stated rationale is backwards** and the catalogue should be corrected in
   place. Its caveat says the peptide rungs *remove* the Block B confound; `SEQUENCES.md`
   §6 shows they sharpen it unless the partner runs MSA-free.
6. **The class B/F instrument decision (E0.5) is not a decision.** The frozen panel settles
   it. Carrying it as an open option invites someone to reinstate an uncalibrated kink
   angle and a wrong atom pair.
7. **I would not adopt `RUN_MATRIX`'s CORE-32 or CORE-L17 numbers unmodified.** It is
   costed against a 32-receptor / 32-cluster core with a 17-cluster ligand subset. The
   frozen panel is **30 / 29**, and its ligand-ready subset is **15 clusters after
   curation and 9 today** — not 17. Every ladder cost scales by 30/32; the ligand-arm
   interaction MDE moves from `RUN_MATRIX`'s quoted 0.295 to **0.314 (k = 15)** or
   **0.406 (k = 9)**. The paper has to quote the one that is true, and 0.406 is a
   different sentence from 0.295.
8. **`RUN_MATRIX` §7.1 has no line item for E1.8 or E1.9**, and `GROUP1_SYSTEMS.md`
   proposes both as G16 and G17. E1.9 (partner MSA on/off) is now load-bearing for F-5 and
   must be costed — it is T1.4 and T3.3 here.
9. **`RUN_MATRIX` G12 is anchored at `ct21`; it cannot be.** Gi1 and Gt1 differ at **one**
   position at `ct11` and at **two** at `ct21`, so the single-residue natural minimal pair
   exists at the 11-mer rung and nowhere else (`GROUP1_SYSTEMS.md` §8.1). The catalogue's
   own E1.6 text says ct21. It is ct11.

## 11.2 Where I am uncertain, stated rather than resolved

- **Whether the short rungs return depth 1 or depth 700.** `SEQUENCES.md` argues the α5-CT
  is conserved enough to retrieve deeply and that the *controls* will be at 1. The
  `arrestin_Ctail` datum (41 aa excised fragment, depth 1) argues the other way for excised
  fragments specifically. **I do not know which, and PF-1 is precisely the measurement that
  decides.** The mitigations in §3.3 are chosen so that the campaign is valid either way,
  which is why I recommend them all rather than picking.
- **Whether `gcn4_window` comes back helical as a monomer.** It is a coiled-coil. If it
  does not, `polyA` carries the matched-null role alone and the helicity-matched comparison
  is lost. The pilot's helicity columns answer it at no extra cost.
- **Whether a linear 21-mer is a meaningful input to these models at all.**
  `tran2026nanogs` reports the unstapled peptide is a random coil and does nothing, while
  the stapled one works only with agonist present. A co-folding model will build a helix
  from whatever it is handed. If it builds an ideal helix at every rung, the ladder
  measures **reach**, not **recognition**, and only recognition supports the title. The
  helicity and helix-span columns are what distinguish them, and I cannot predict the
  answer.
- **Whether the ligand axis can reach beyond 15 clusters.** Eight frozen-panel receptors
  have peptide-only agonists. I do not know how many of them have a usable small molecule
  that nobody has curated, and the answer is the difference between a bounded interaction
  test and a well-powered one.
- **Whether the depth cube should run at all.** It is the most novel cell in the plan and
  the least load-bearing for the title. It is also blocked on E8.3, which two independent
  mechanisms now say is unresolved. If the budget is tight, this is the first Tier 3 item I
  would cut — and I say that knowing it is the one a referee would find most interesting.
- **The two-chain cost.** 13× wide. Everything in §7 inherits it.

## 11.3 Still unanswered by the pipeline team — the branch both ways

| question | if yes | if no |
|---|---|---|
| **Is the MSA-depth pre-flight running?** (unanswered across three messages) | We may be able to read their numbers instead of measuring 212 sequences ourselves. Saves hours, not days. | PF-1 runs on our side. **Nothing in the design changes either way** — this was the right conclusion to reach, and it means the question is not blocking. |
| **Was a peptide ever dispatched as a partner?** (no manifest with a partner arm yet) | Their catalogue's 24 exploratory partner sequences become a prior on what to expect at peptide length, and one of them (`endothelin1`, 21 aa) is an exact length-match to `ct21`. | We are the first, which is the novelty claim four independent corpus absences already support. **The ladder is unchanged.** The only thing that moves is how confidently we can predict PF-1's answer. |
| **Was Block C's blanket `alphas` a decision or a recurrence?** | The Block C partner arm is "receptor + Gαs" and its 18,400 crossed predictions describe a real, if oddly-named, experiment. Worth exporting for the 2 of 30 Gs-coupled frozen-panel receptors it happens to be correct for. | The arm is void. **Our design is identical**: partner resolved per receptor from `coupling_cognate_map.tsv`, enforced by B16. Only the disposal of their existing data changes. |
| **`reference_panel_v2.csv`, and whether "transducer present" was a stated rule for actives** | We can attribute the limitation correctly — "their active pole is partner-bound by design" — and write the same sentence about ours honestly. | We say the rule is emergent, evidenced by the rejection log (`7EZC`, `5WF5`, `8UGW`, `3QAK` all rejected for "no Gα"), and flag it as unattributed. **Group 0's D3 is the decision either way**, and it is ours, not theirs. |

**In all four cases the campaign is the same.** That is the useful finding: no design choice
in this document hinges on an answer we are waiting for. What hinges is how much of their
existing data we can reuse, and the honest answer to that is "less than we hoped, and the
redo was already designed not to need it".

---

# 12. Anomalies found while writing this

Each was treated as my own error first, per the project's rule. Two of the four were.

1. **"33 experiments in 9 groups" is wrong in three places.** The brief, `CATALOGUE.md`'s
   header and `RUN_MATRIX.md:4`. The body holds **45 `### E…` headings in 10 groups
   (0–9)**, one carrying two ids, so **46 experiments**. I recounted three ways before
   calling it. It is documentation drift from before Groups 8 and 9 landed — and it is our
   own instance of the pattern F-1 records for `switch_signal.py`.
2. **`RUN_MATRIX`'s CORE-L17 is not the frozen panel's ligand set, and my own first
   recount of it was also wrong.** `RUN_MATRIX`'s 17 is 17 *clusters* of a 32-receptor
   core. My first pass counted `n_agonist_smiles > 0` and got 17 *receptors* / 16
   clusters — but that column counts a SMILES string for a **peptide**: EDNRB reports 9
   agonist SMILES and its modality is `peptide;protein`. Counting on modality gives
   **16 receptors / 15 clusters** small-molecule-complete, and **10 / 9** also curated by
   Block C. Three different "17"s and two of them were mine. The recount is in §5.2 and it
   changes the interaction MDE from 0.305 to 0.406.
3. **My first reading of F-5 predicted the wrong sign.** I expected short rungs at depth 1.
   `SEQUENCES.md` §6 argues WT rungs will be deep and *controls* will be at 1, which is a
   worse confound in a different place. I have kept both possibilities live because PF-1 is
   what decides, but the correction is mine and it changes which arm is at risk.
4. **I initially carried the Block B decoy confound as a pairing story.** It is not:
   Boltz, Protenix and OpenFold-3 all read the tail edit as aligned uppercase; Chai is the
   sole outlier at 0/40 and its `pairing_key` is empty on every row of every file. The
   confound is content and depth, **per backbone**. Correcting this is what made M4 (Chai
   as the falsification backbone) visible.
5. **The date-stratified holdout was costed as an arm and is not one.** Computed here on
   the frozen 30: Protenix 2021-09-30 splits 16/14 receptors and 16/13 clusters; Chai-1
   2021-01-12 splits 21/9 and 21/8; Boltz-2 2023-06-01 splits 4/26 and is unusable;
   OpenFold-3 is undated. Three of four backbones get a stratification for zero
   predictions.
6. **`g1_preflight` already enforces the F-5 mitigation that nobody had connected to F-5.**
   Checks **B7** and **B8** — every row declares a partner-MSA condition, and MSA-free is
   the primary one — were written from `SEQUENCES.md` §6 before `DECISIONS.md` F-5 existed.
   Two sessions reached the same conclusion independently from different evidence. That is
   the strongest reason to believe it.

## 12.1 Documentation discrepancies in the frozen specs — found, not resolved here

These belong to their owning documents. I record them so they are not quoted before they
are reconciled, and I have not touched any of the files.

| where | discrepancy |
|---|---|
| `GROUP0_SYSTEMS.md` prose vs `g0_preflight.py` | Prose says **11 blocking checks and 9 dependencies**; the script has **12 (G0-1…G0-12) and 8**. G0-12 was promoted from a `wait()` and has **no selftest plant**, so of the twelve blocking checks eleven are defect-proved and one is not. |
| `GROUP0_SYSTEMS.md` §2.2 vs the filter ladder | **155 off-panel receptor entries** against **147 receptors** at F0; §10's Class A census says 1,358 / 188 / 65 against §2.2's 1,336 / 199. Different grains (entries vs receptors, with vs without Intermediates) but they read as contradictory side by side. |
| `GROUP1_SYSTEMS.md` §5 vs §11.1 | partner registry is **588 constructs** in one place and **771** in the other. |
| `GROUP1_SYSTEMS.md` §4 vs §11.1 | system rows carrying a resolved sha256: **1,365** vs **1,451**. |
| `GROUP1_SYSTEMS.md` §4 vs §11.3 | G18a **3,840 / 19,200** vs **3,600 / 18,000**; G18b **150** vs **180**; G19 **440 / 2,200** vs **920 / 4,600**. |
| `CATALOGUE.md` header, `RUN_MATRIX.md:4`, and the brief | "33 experiments in 9 groups" against a body of 46 in 10 (§2). |

None of these changes a design decision in this document. Every number I quote from those
files, I recomputed from the `inputs/` artefacts rather than from the prose — the panel
(30 / 29), the class distribution (Gi/o 22, Gs 6, Gq/11 2), the ladder lengths, the control
counts and the date splits all come from the TSVs and CSVs, not from a table someone typed.
`COUPLING.md` records why that matters: a hand-typed 64-row table in that session had
**27 wrong cells in 66 lines**.

---

## One paragraph for the handoff

**The redo's frozen objects survive the nine findings. What changes is the ladder's
baseline, its alignment regime, and the instrument.** Run the fourteen pre-flights and a
9,040-prediction two-backbone pilot before anything else; the pilot's gate is written and
can stop the campaign for 7% of the core's cost. The core is 128,800 predictions — 1.1×
everything delivered in Blocks A–D — and it closes title clause 1, closes the half of
clause 2 that new inference can close, and makes clause 3 computable for the first time by
removing a confidence gate that currently decides the state call. Two of the best items in
the document cost no GPU at all: small-molecule ligand curation for six receptors, and a
per-chain MSA fix in `propose.py`. The first GPU spent should be 40 predictions on a timing
probe, because every cost here carries a 13× bracket that nobody has closed.

**And one thing to decide before anything else, because it is free and it is a title
clause: P7 has never been computed, and it can be computed this week on data we already
hold.**
