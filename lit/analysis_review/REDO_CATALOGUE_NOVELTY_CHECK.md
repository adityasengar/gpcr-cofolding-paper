# Novelty sanity read — `analysis/REDO_EXPERIMENT_CATALOGUE.md`

lit-3d, 2026-09-11. Checked against `INDEX.md` (81 blocks) and the notes named below.
Requested by paper-6f, which ranked the rows by prediction spend rather than by interest.

**Corpus state at check time.** 81 notes / 81 INDEX blocks / 85 bib. **No note has a
2026-09-11 mtime**; the newest is `vo2026fiducials` at 2026-09-10 20:17. paper-6f's
caution that "the corpus moved during the day" does not apply — every novelty line in
the catalogue was written against the corpus as it stands.

**Verdict in one line: every OPEN call I checked survives. Three rows have a wrong or
incomplete supporting sentence, one has an internal contradiction, and one novelty line
is wrong as written.**

---

## The denominator problem, which is the structural finding

Three of the catalogue's OPEN calls (E2.2/E7.4, E8.1, E8.2) rest on "zero of 81" or
"exactly one of 81" claims about **factor crossing**. The field that records factor
crossing, `input_factor_design`, is populated on **11 of 81 notes** and appears in
`INDEX.md` **zero times**. `SCHEMA.md` is explicit that its absence on the other 70
means *not yet backfilled*, never `NOT ADDRESSED`. So as written those are
"zero of the 11 notes where anyone looked."

**I closed it on a real denominator instead, and the claims hold.**
A ligand × partner crossing can only exist in a paper that has both handles. Exactly
**7 of 81** carry both `ligand-driven` and `partner-driven`:

| paper | can it hold the crossing? |
|---|---|
| `georgiou2025heterogeneity` | no — review |
| `tejero2024opsin` | no — cryo-EM + assay, `oracle: NOT APPLICABLE, no prediction pipeline` |
| `hilger2020gcgr` | no — cryo-EM/DEER wet lab |
| `chiesa2025templatebias` | **partner × ligand HELD** (recorded `crossings:`) — ligand never removed |
| `ye2026multistatebias` | **partner × ligand CONFOUNDED** (recorded) — β2AR gets agonist AND Gαβγ together, no agonist-free partner condition, p.18 |
| `vo2026fiducials` | **crosses none of them** (recorded) |
| `ku2026promise` | ligand-induced and protein-induced are **separate sets**, not crossed — see below |

`factors-crossed` fires on exactly one block in `INDEX.md` (`mitjavila2026afsample2t`,
line 448–449), and `coinput-confounded` on three. `controls_run` is populated on 79 of
81, so the control-side tagging is broadly exercised rather than backfill-only.

**`vo2026fiducials`'s own note states the trap the catalogue is at risk of**, and it
should be quoted in the spec:

> "Despite carrying `msa-subsample`, `ligand-driven` and `partner-driven` together, this
> paper crosses none of them — it is the clearest demonstration that a tag combination
> in `INDEX.md` must not be read as a crossing."

**Recommendation.** Phrase every such claim as *"of the N papers that could hold it"*
and name N, rather than "of 81". It is a stronger sentence and it is the one that
survives a referee who knows the field.

---

## Row 1 — E1.1, the α5-CT length ladder (44,800 predictions). **OPEN survives.**

Nobody in the corpus ladders partner length against a structure predictor. The
catalogue's two supports are correct and well chosen — `ye2026multistatebias`
`controls_run` "ABSENT — reduced or partial partner construct … No truncated, decoy or
scrambled partner is run" (p.18), and `chiesa2025templatebias`. I add a third:
**`heo2022multistate`** records that "ligand, nanobody, G-protein and arrestin are never
used as inputs". Three independent recorded absences is as strong as this corpus gets.

Sweeps run, with denominators: `/truncat/` 59 of 81 (too broad — it is almost entirely
MSA and receptor-segment truncation); the subset of those lines that also name a partner
term, 15 lines, none of which is a partner-length series against a predictor;
`/peptide length|length series|length ladder|varying length/` 4 of 81;
`/titrat/` 4 of 81; `/\d+-mer/` 1 of 81 (`tran2026nanogs`).

**But the row is missing a near-miss a referee will find, and it carries a measurement
warning the ladder needs.**

`junker2026peptidedesign` (PLOS One 21(8):e0355549) is the corpus's only
**length-stratified** analysis of peptide co-inputs against co-folding predictors: 113
GPCR peptide/protein complexes, **peptide lengths 3–137 aa** (p3, Fig 2B p5), 50 seeds,
three predictors. Peptide length there is an observational covariate, not a manipulated
factor — the generative arm *pins* length to the native ("restricted to exactly the
length of the respective reference peptide", p11) — and **receptor state is never
assessed**. So it does not touch E1.1's novelty. It matters for two other reasons:

1. **It is a placement-quality prior on our own rungs.** Stratified ≤50 vs >50 residues:
   "100% of AF2IG-predicted, 82.1% of RF3-predicted and 35.5% of Boltz-2-predicted
   GPCR-protein ligand complexes achieve a DockQ score below 0.23" (p5, S2 Fig). Our
   ladder crosses that boundary between **R4 (~45 aa) and R5/R6 (350–394 aa)**, so the
   two ends of the ladder sit in different placement-accuracy regimes. A graded response
   to length could be a placement artefact rather than a signal-content effect. The row's
   existing "engagement depth" column is the mitigation — it needs to be stated as
   *required for interpretation*, not merely carried.
2. **It warns that cross-length comparison of an interface score is itself unsound**:
   comparing "peptides of different lengths is hindered" (Methods, p16), which is why
   they chose DockQ. Whatever interface measure the ladder reports must be one that is
   defined consistently across 11 → 394 residues, or reported within-rung only.

**Answer to the second half of the question — does anything titrate a peptide length
against any predictor, GPCR or not?** No. `/deep mutational|saturation mutagenesis|
mutational scan/` returns 0 of 81, and the four `/titrat/` hits are a wet-lab
concentration series (`tran2026nanogs`, `hilger2020gcgr`), a ligand-encoding study
(`bugrova2026representation`) and `zhang2026generalization`. Dose ladders in the corpus
are on operator handles only, as the catalogue says.

## Row 2 — E1.2, the bulk control (16,000–38,400). **OPEN survives; the row contradicts itself.**

`yu2026domainmotion` is **a different claim, on a different system, with a different
co-input class**, and the row says so correctly in its `Novelty.` line ("OPEN for protein
partners… The ligand analogue is DONE and is the threat") while its `Closes.` line says
yu "is the published form of it". Those cannot both stand. The `Novelty.` line is right.

What yu actually is: 82 **enzymes** from DynDom, open↔closed **domain motion**, AF3
primary with **no templates and no MSA**, 500 models per protein per condition. Its
control is a **nonbinder small-molecule ligand** — a decoy of the same chemical class as
the binder. E1.2's control is a **mass- and shape-matched non-Gα protein chain**
(`gcn4_leucine_zipper_33`, `ubiquitin`, `KaiB_2QKEE`, `random_helix_40mer`) on GPCRs read
on receptor state. Different co-input class, different system, different state
definition. E1.2 tests **whether yu's finding extends to protein co-inputs** — which is
the correct and more interesting framing, and it is not confirmatory.

**The real dependency the row misses.** yu's decisive covariate is not the ligand, it is
the **apo:holo ratio in the PDB**: the trigger ligand moves the holo-like fraction by
11.9% and 9.1% in Groups 1 and 2 against a **40.3%** gap attributable to training
composition alone, rising to 17.5% in Group 3 where the memorised prior is weak. Its
recorded `crossings:` line is the point — *"the ligand axis is crossed with a
training-set-composition stratification, and that crossing is what produces the paper's
result."* The catalogue records **E1.2 "Depends on. Nothing."** On yu's own design, a
bulk control run without stratifying by each receptor's deposited **active:inactive**
ratio is uninterpretable: a null could be the control working or the prior swamping it.
**E1.2 should depend on E4.2's exposure covariate**, and the two should be analysed
together.

## Row 3 — E2.2, ligand class × partner presence (27,200). **OPEN survives, and it can be stated more strongly.**

Sweep for interaction language across all 81 notes —
`/interaction term|interaction effect|two-way interaction|factorial|ANOVA|synerg|additiv/`
— returns **11 of 81**, and **none estimates an interaction between a ligand and a
protein co-input in one model**. The ANOVAs are on representation choice
(`ferguson2026deorphann`, 2-way RM ANOVA on single-vs-pair tensors) and on wet-lab
geometry (`matic2023gpcrome` PERMANOVA/PERMDISP). No second attempt exists.

**Sharpen the `suzuki2026conforflux` citation — as written a reader will take it for a
co-input attempt.** The p.21 sentence is real and verbatim: *"With n=10 targets and
across-target standard error ∼0.6 Å, we cannot resolve non-additivity between the two
factors."* But **"the two factors" are two internal scaling terms of the steering
equation** — the noise-level factor and the kernel-saturation factor (Table 10, p22) —
not a ligand and a partner. The honest and stronger sentence is: *no paper in 81 even
attempts an interaction estimate between two biological co-inputs; the corpus's only
non-additivity test is between two algorithmic hyperparameters and is underpowered.*

**Add `ku2026promise` to this row — it is the strongest ADJACENT in the corpus and the
row does not cite it.** It runs **both** co-input types against the same five models
(AF3, Boltz-1, Boltz-2, Chai-1, BioEmu), each conditioned present/absent, and keeps them
in **separate, non-overlapping sets**: a "ligand-induced set" and a "protein-induced
set", scored with different success criteria (ligand RMSD ≤ 2 Å vs pair-level, p3).
Its own note draws the consequence — it is *"support for treating partner-induced and
ligand-induced effects as different problems"*, and *"partner-induced from ligand-induced
conformational change must now be positioned against it."* This **strengthens** the OPEN
call: a paper that held both handles and both model families still did not cross them.
A referee who knows ku will ask about it, and the row should answer first.

## Row 4 — E1.5, the per-position scan (4,200). **OPEN survives; both named supports are receptor-side, and the row is missing the one paper whose protocol it should copy.**

Nobody scans a **supplied partner** residue-by-residue and reads **receptor state**.
Sweeps: `/alanine scan|Ala scan/` 1 of 81 (`hilger2020gcgr`, wet lab);
`/point mutation|point mutant|single-residue mutat/` 2 of 81;
`/deep mutational|saturation mutagenesis|mutational scan/` **0 of 81**;
`/per-position|position-by-position|residue-by-residue/` 5 of 81, none on a partner.

The two cited supports are both **receptor-side self-mutation**, which is worth saying in
the row because it is what makes them weaker evidence than they look:
`masters2025physics` mutates the **receptor's own pocket**; `bret2025boltz2docking`
alanine-mutates the **target's** binding site and reads an **affinity classifier**, not a
structure or a state.

**Two things to add.**

1. **`waymentsteele2024cluster` is the corpus's one per-position scan read on a
   conformational state, and E1.5 should cite it and copy its protocol.** The KaiB_RS
   mutation scan runs "all combinations of 8 enriched point mutations, **no MSA**, 12
   recycles, model 1" (p4, p17), and three mutations (I68R, V83D, N84R) flip the
   predicted state. It is a *self*-scan, not a supplied partner, so E1.5's novelty is
   untouched — but it is the design precedent.
2. **`masters2025physics` hands E1.5 a confound it must design around.** Its null has a
   stated mechanism: "when we introduce small mutations… the sequence alignment and
   template search will return exactly the same results as before" (p.9) — *the mutated
   sequence retrieves the wild-type MSA and template*. If we mutate positions inside a
   **supplied partner chain** and the partner's alignment is unchanged, a null is an
   artefact of retrieval, not model insensitivity. **The mitigation is already implicit in
   E1.3's caveat** — at 21 residues the partner MSA is essentially empty — so **E1.5 must
   be run at peptide length, or the partner MSA audited per arm as
   `03_msa_audit/PHASE_1D_EXTENSION.md` did.** `waymentsteele2024cluster` ran its scan
   with no MSA for the same reason.

## E7.6 — the arrestin finger loop. **OPEN survives; the supporting sentence is wrong, and there is a cross-experiment dependency.**

"Arrestin appears in the corpus only as review content in `georgiou2025heterogeneity`" is
false. It appears in **7 notes**: `paajanen2026activation` (3), `georgiou2025heterogeneity`
(3), `khaleq2026hyaline` (2), `miglionico2026atlas`, `heo2022multistate`,
`chakravarty2026statespace`, `bryant2024cfold`. None supplies arrestin to a predictor, so
the verdict holds — but three of them are *better evidence than the review*, and one
changes a design:

- **`heo2022multistate`**: "ligand, nanobody, G-protein and arrestin are never used as
  inputs". A recorded absence, the same shape as the evidence E1.1 uses. Cite this.
- **`khaleq2026hyaline`**: its active-state label rule *already counts* "(2)
  arrestin-coupled structures" as active — so the classifier literature treats an
  arrestin-coupled receptor as active-state, which supports the arm's premise. It also
  states its own limit: the model "does not address… the distinction between G
  protein-biased and arrestin-biased conformations" (p11). Two citable facts.
  **Check before running:** if any arrestin-coupled structure defines "active" in our own
  reference set, an arrestin-FL arm is partly circular.
- **`paajanen2026activation` — the dependency.** E0.2 names paajanen's coordinate as
  independent index (c). Paajanen **excluded arrestins**: *"Arrestins have not been
  included in the analysis because there is not enough data to influence the graph."*
  (p.2). **So an E7.6 arrestin arm cannot be concordance-checked against E0.2's index.**
  Neither row records this. Either E7.6 states that it has no independent check, or E0.2
  drops option (c) for that arm.

*Related, smaller:* E0.3 proposes scoring **21 Class A Intermediate** structures.
Paajanen dropped intermediate/other for exactly that reason — *"their number is too low
to be distinguished from the graph"* (p.2). E0.3's design is fine, but it should say in
advance what it will conclude at n=21, since the one paper that faced the same n chose
not to report.

---

## One row that was not on the list, and is wrong as written

### E3.3 — "Confidence on the supplied partner chain"

> **Novelty.** ADJACENT — `yu2026domainmotion` reports ligand pLDDT fails to separate
> binders from nonbinders; **nobody has asked it of a protein partner.**

**That last clause is false.** `miglionico2026atlas` asks exactly it, on a Gα partner, at
an α5 position, and reports **`pLDDT H5.11 AUC 0.762` (p5)** — per-residue pLDDT at a
single Common-Gα-Numbering α5 C-terminal position, validated as a discriminator against
experimental coupling labels. It further uses ipTM (AUC 0.706; 0.735 class A), pDockQ and
max contact probability (AUC 0.771) the same way, and **hard-protects the 7 C-terminal Gα
residues from its own pLDDT<70 filter** "since they are known to be important for
specificity" (p20).

The correct clause is: *nobody has asked it of a protein partner **against a receptor
conformational-state outcome***. Miglionico's own note is explicit that its confidence
use is **"for *binding*, not for conformational correctness, and only the binding use is
validated"** — "no relationship between any confidence score and DockQ is reported
anywhere." So E3.3 keeps its value, gains a strong prior (partner-chain confidence at α5
positions carries real signal for coupling), and gains a directly comparable published
number to beat.

This is the row I would most expect a referee to catch, because `miglionico2026atlas` is
already tagged `confidence-as-discriminator` **and** `partner-driven` in `INDEX.md`.

---

## Two additional near-misses worth carrying

- **E1.4 (family swap at peptide length)** should cite `miglionico2026atlas`'s wet-lab
  arm: **11 Gαq chimeras** with different Gα C-termini swapped in, read by TGFα-shedding
  (Fig 4C, p32), with a **C-terminally truncated Gαq (ΔC)** control ruling out that the
  signal comes from the Gαq scaffold; QRFPR predicted vs measured Pearson **r = 0.66,
  P = 0.026** (p9). That is the experimental result our in-silico family swap is the
  prediction analogue of — and the ΔC control is the wet-lab twin of E1.1's R5 rung.
- **`pandyszekeres2024gproteindb`** truncates *receptor* segments as an input construct
  (class A ICL3 retained at 14 residues; a 10-residue GPCR C-terminus swap-in, p.3). Not
  a partner truncation, but it is the precedent for "truncation as a deliberate input
  construct" and it is where the convention for reporting it comes from.

## What I did not check

The remaining ~6 per-experiment `Novelty.` lines (E0.1, E0.4, E0.5, E1.6–E1.9, E2.1,
E2.3, E2.4, E3.1, E3.2, E4.x, E5.x, E6.x, E7.1–E7.5, E9.x) and 7 of the 13 rows in the
§5.1 map. paper-6f ranked by spend; these were below the line.

---

# Second pass, 2026-09-11 — the rows left over

Covers the novelty calls not reached in the first pass. **Every call I checked stands.
One row carries a number the project has already corrected elsewhere, and that is the
material finding of this pass.**

## MATERIAL — E3.2 quotes a superseded number, in the one context the correction warns about

E3.2 (`analysis/REDO_EXPERIMENT_CATALOGUE.md:903`) reads:

> "Already computed: **+1.1 pp overall, sign flipping across backbones (−3.1 to +4.9), and
> 256 of 319 cells unanimous anyway.**"

The row's question is *"does picking the highest-confidence **seed** beat picking at
random?"* — so 256 is being used as a **seed-grain** count. It is not one, and the project
established that in three places before the catalogue was last touched:

| file | what it says |
|---|---|
| `analysis/redo/RUN_MATRIX.md:547–548` | "**256 of 319 (80.3%)** are unanimous across all **25 predictions** — *sample* grain"; "**300 of 319 (94.0%)** are unanimous at **seed-majority** grain" |
| `analysis/redo/RUN_MATRIX.md:555` | warns in terms against writing "256 of 319 cells unanimous across seeds … **in that form**" |
| `HANDOVER.md:39–41` | carries the corrected line — 300 of 319, "only 19 cells (6.0%) show any seed-to-seed disagreement" — and says quoting 256 as seed-grain "understated how redundant the seed axis is" |
| `analysis/redo/matrix_power.py:87–88` | prints the same correction at runtime |
| `analysis/redo/g1_recording_spec.tsv:41` | records it as a recording-spec requirement |

`REDO_EXPERIMENT_CATALOGUE.md` was last modified **13:53**, `HANDOVER.md` **13:39** — so the
catalogue was touched after the correction landed and still carries the stale figure. **Fix
E3.2 to 300 of 319 (94.0%) at seed grain, or state the grain explicitly if 256 is wanted for
a different reason.** Five files agree; one disagrees.

This also *strengthens* E3.2's own argument: at seed grain only **19 of 319 cells (6.0%)**
show any seed-to-seed disagreement at all, so a +1.1 pp gain from confidence-ranked seed
selection is being extracted from a 6% slice — which is a sharper way to say the operational
effect is small than "+1.1 pp" alone.

## E3.2's ADJACENT understates its own support

The row cites `ku2026promise` for confidence-ranked vs uniform-random top-k. It has
**directly comparable numbers**, and they are better support than the row admits (note
`ku2026promise` line 523, p15 Fig S2): **Confidence Top-10 vs Random Top-10**, AF3 **0.15 vs
0.17** (intrinsic), **0.49 vs 0.48** (ligand), BioEmu **0.18 vs 0.18** (intrinsic) — i.e.
confidence ranking is matched or *beaten* by random at fixed budget, across five models at
100 predictions per entry. The paper says so: confidence is *"occasionally outperformed by,
uniform random sampling from the generated ensemble"* (p5 §3.2). **Our +1.1 pp and ku's
≈0 agree**, which turns our operational result from an isolated observation into a
replication. Cite the numbers, not just the paper.

## Rows checked and standing

### E2.3 — efficacy ladder. **OPEN survives; one near-miss to name.**
"No paper varies pharmacological class across a GPCR panel and calls state with a fixed
predicate." Checked on a real denominator: **13 of 83** papers carry both `gpcr` and
`ligand-driven`; of those, only four have a conformational state metric that is not
`NOT APPLICABLE`, and none varies pharmacological class across a panel.
`kohlhoff2014gpcr` is correctly named as nearest in kind (one receptor, agonist / inverse
agonist / apo, MD). **Add `obendorf2026statespecific`**: three GPCR systems spanning classes
— 5-HT2A + pimavanserin (inactive, 8ZMG), A2A + CGS21680 (active, 8UGW), δOR + ADL5859
G-protein-biased agonist (active, 8Y45) — but **one ligand per receptor**, so class is
confounded with receptor *and* with reference state, and its state calls are "visual marker
calls **by eye, no rule**", n = 7 overall. That is the shape our fixed predicate is designed
to fix, so the row is better with it than without.

### E1.8 — uncoupling point-mutant Gα arms. **OPEN survives; two wet-lab near-misses.**
No paper mutates a **supplied partner** and reads receptor state from a predictor. Two
papers mutate a Gα, both experimentally:
- `tejero2024opsin` — "Mutations were introduced to the human Gαi to match the sequence of
  the jumping spider" — the jsGiq chimera (A31R, D193S, L194I, residues 337–354 wholly
  replaced), read by cryo-EM. **No predictor is run** (`oracle: NOT APPLICABLE`).
- `bondar2017preassembly` — the **N269D non-dissociating Gαi1 mutant**, used as a *positive
  control* that the assay can detect a GPCR–G protein interaction at all. Linear dichroism,
  no predictor, and it is an association readout rather than a receptor-conformation one.
Neither touches the novelty. Both are worth citing as the biological motivation the row
already claims ("biologically motivated rather than combinatorial") — `tejero2024opsin`
especially, since it shows an interface-swapped Gα still forms a productive complex.

### E7.3 — prospectivity. **Confirmed, and it can now be stated with a denominator.**
Exactly **4 of 83** papers record `prospective: yes` — `bondar2017preassembly`,
`ingraham2023chroma`, `tran2026nanogs`, `wallner2023afsample`. Of those, **bondar and tran
are wet-lab with no predictor**; `ingraham2023chroma` is `v3-partial` and `lit/CLAUDE.md`
forbids using it for novelty or priority arguments; `wallner2023afsample` is a sampling
method, not a GPCR state study. The other 32 are `partial`. **So no paper in 83 runs a
prospective structure-prediction arm on GPCR conformational state.** "The closest thing to
prospectivity available" is an understatement — say 4 of 83, and why none of the four
counts.

### E0.1, E3.1, E4.1, E5.3 — DONE/ADJACENT calls. **Every number verified exact.**
This is worth recording as a clean pass; a reviewer that only ever reports defects is as
suspect as one that never does.

| claim in the catalogue | corpus | verdict |
|---|---|---|
| `paajanen2026activation` 1,351 Class A structures, GMM threshold −1.72 ± 0.44 | note `state_metric`, `n_targets` | **exact** |
| `khaleq2026hyaline` 1,590 structures, AuROC 0.99, threshold **not reported** | note lines 78, 162, 217 | **exact**, including the unreported threshold |
| `sun2026kinconfbench` wrong-state ranked first in **>11%** of cases | note line 334 | **exact** |
| `chiesa2025templatebias` **94 of 145** with no template and no training presence | note line 155, p6302 | **exact** |
| `skrinjar2026generalization` **8–25%** least-similar vs **81–89%** most-similar | note lines 325, 402–403 | **exact** |
| `ku2026promise` all known states in only **~8–29%** of clusters | note line 416 | **exact** |
| `junker2026peptidedesign` PAE over-estimates for misplaced GPCR peptides in all three predictors | INDEX `claim` | **exact** |

### E0.1's framing is the best in the document and should be copied
"Our claim is a *reimplementable, per-axis, off-panel-calibrated* predicate, **not a new
idea**" — with the two reasons stated (paajanen ships no weight vector, no residue list, no
repository; khaleq never reports its threshold and has never been run on a predicted
structure). That is exactly how a DONE-adjacent contribution should be written, and several
of the weaker rows would improve by imitating it.

## Rows not individually re-derived

E0.2, E0.3, E0.4, E0.5, E1.4, E1.6, E1.7, E1.9, E2.1, E2.4, E4.2, E4.3, E5.2, E5.4, E5.5,
E6.x, E7.1, E7.2, E7.4, E7.5, E9.1, E9.3. Their supports are either already checked in the
first pass, or are internal to our own blocks rather than corpus claims. **E2.4 and E5.5**
are DONE calls resting on `yu2026domainmotion` and `skrinjar2026generalization`, both of
which I verified for other rows and both of which carry the cited content.
