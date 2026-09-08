# singh2026moredata

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` **with a reason** where the field presupposes a study this paper did not run.

**THIS IS AN OPINION / PERSPECTIVE PIECE, NOT A PRIMARY STUDY.** That determination is made
from the document itself, not from the venue name, and the evidence is listed in full in
section A under `venue`. It has no Methods section, no Results section, no data-availability
statement, no supplementary material, and no protocol of any kind. It reports **no new
experiment, no new simulation, and no prediction run by these authors**. Its one quantitative
figure (Figure 4) re-presents an analysis attributed to reference [67] — a companion bioRxiv
preprint on which two of this piece's four authors (Castellanos, Chodera) are co-authors.
See `si_in_scope` and the Figure 4 rows in section F. **Consequence: almost all of section C
is NOT APPLICABLE by construction, not by sloppy reading.**

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–23), which here equal the
printed "Page N" in the running header** (PDF p7 prints "Page 7"). Layout: p1 PMC masthead +
title + abstract + disclosures; p2–p3 Introduction; p3–p5 "Structure-based drug discovery
relies heavily on the Protein Data Bank and blind challenges"; p5–p7 "Task-specific datasets,
models, and challenges will drive progress in structure-based modeling"; p7–p8 "Prospective
predictions of inhibitor binding modes and affinities remain limited"; p8–p10 "Conclusions and
Perspectives"; p10 acknowledgements; p10–p18 references **with annotated highlights** ("of
Special interest" ** / "of Outstanding interest" ***, the Current Opinion convention); p19
Figure 1; p20 Figure 2; p21 Figure 3; p22–p23 Figure 4.

**The annotated bibliography is a first-class part of this paper's content and is treated as
such below.** Twenty-odd references carry author-written annotations of one to two paragraphs
each. Those annotations are where this group states, in its own words, what it thinks is wrong
with named benchmarks, named datasets and named models. They are quoted with pages in
`central_conclusion`, `metrics_reported` and the evidence-base subsection of D.

**Quotation convention.** The PDF text layer carries soft-hyphen artifacts from the printed
line breaks ("pro-tein", "chal-lenges", "im-proved") and occasionally drops a hyphen entirely
("proteinligand"). All quotes below are **verbatim except that these layout artifacts have
been repaired** — hyphens introduced by line-wrapping removed, and a dropped hyphen restored
as `protein[-]ligand`. No word, order or emphasis has been changed. The `*and*` in the p5 quote
is the authors' own emphasis, present in the source.

**License: NO LICENCE STATEMENT IN THE PDF.** This is an NIH/HHS Public Access author
manuscript of an Elsevier journal article. Treat as all-rights-reserved for redrawing. See
`reuse` in section F.

**Left empty by instruction:** `comparable_to_ours` (section E) and `why_it_matters` (section
G).

---

## A. Identity

- **citekey**: `singh2026moredata`
- **doi**: **10.1016/j.sbi.2026.103257** — p1 masthead ("Curr Opin Struct Biol. 2026 June;
  98: 103257. doi:10.1016/j.sbi.2026.103257"), and matches `refs.bib`.
- **year**: **2026.** p1: "Published in final edited form as: Curr Opin Struct Biol. 2026 June;
  98: 103257." The PMC embargo line reads "available in PMC 2026 April 04" on every page footer.
  `refs.bib` records `year = {2026}`. No received / revised / accepted dates are printed in this
  author-manuscript PDF.
- **venue**: **Current Opinion in Structural Biology, volume 98 (Elsevier) — PEER-REVIEWED,
  and an INVITED OPINION / PERSPECTIVE piece, not a research article.** Not a preprint; tagged
  `peer-reviewed`, not `preprint`. The perspective determination rests on six independent
  signals inside the document:
  1. **The authors call it a "piece", twice.** p3: "In this piece, we assert that more
     protein[-]ligand binding and kinetics data is needed…"; p8: "In this piece, we highlight
     the key role the PDB has played in enabling PSPMs to exist."
  2. **The abstract is a discussion abstract, not a results abstract** (p1): "Here, we discuss
     recent efforts to benchmark existing PSPMs and identify their limitations. We offer a
     hierarchical framework… Finally, we emphasize the need for systematic dataset generation…"
     No result, no number, no comparison is claimed as the authors' own.
  3. **No Methods, no Results, no Data Availability, no supplementary material.** The section
     headings are the four listed in the layout note above plus "Conclusions and Perspectives".
  4. **The reference list carries the Current Opinion annotated-highlights apparatus** (p10):
     "Papers of particular interest, published within the period of review, have been
     highlighted as: ** of Special interest / *** of Outstanding interest." That apparatus is
     used only by Current Opinion review-family articles.
  5. **The argumentative register is declarative throughout** — "we assert" (p2, p5, p6 ×2,
     p9), "we argue" (p3, p8), "we emphasize" (p5, p8), "we hope" (p3) — the vocabulary of a
     position, not of a measurement.
  6. **The one data figure is sourced elsewhere.** Figure 4's caption cites "[67]" for the ROC
     analysis (p22) and the body attributes the work to "The authors" of [67] (p7), a third-party
     construction the piece then narrates.
  **Countervailing signal, recorded so this is not overstated:** Figure 4 *is* a quantitative
  figure with numbers in it, and its panel B (PDB entries before/after the Boltz-2 cutoff)
  carries **no citation at all**, so it may be a tabulation new to this piece. See `unresolved`
  item 2. A citing sentence should therefore say "a perspective that re-presents an analysis
  from a companion preprint", not "a perspective with no data".
- **title**: "More Protein-Ligand data is needed for AlphaFold-like Models to enable drug
  discovery" — **as printed on p1**. Note the discrepancy: `refs.bib` and the task assignment
  both record the title as "More protein-ligand data **are** needed for AlphaFold-like models
  to enable drug discovery". The PDF title block reads "**is** needed". Cite whichever the
  final typeset version carries; the p1 author-manuscript reads "is".
- **authors**: Sukrit Singh¹\*, Ariana Brenner Clerkin¹, Maria A. Castellanos¹, John D.
  Chodera¹\* — ¹Computational and Systems Biology Program, Memorial Sloan Kettering Cancer
  Center, New York, NY, USA (p1). Corresponding: sukrit.singh@choderalab.org,
  john.chodera@choderalab.org (p1).
  **Continuity notes that bear on how to read the paper, all from the reference list:**
  (i) **Reference [67], the source of Figure 4, is Castellanos, Payne, Scheen, MacDermott-Opeskin,
  Pulido, Balcomb, Griffen, Fearon, Barr, Lahav, Cousins, Stacey, Robinson, Lefker, Chodera,
  "A Structure-Based Computational Pipeline for Broad-Spectrum Antiviral Discovery", bioRxiv
  2025.07.29.667267 (p17)** — first-authored by this piece's third author and senior-authored by
  its last author. Figure 4 is therefore the authors reviewing their own preprint.
  (ii) **Reference [5], the "point of diminishing returns" result that carries the p6 argument,
  is Payne, Kaminow, MacDermott-Opeskin, Pulido, Scheen, Castellanos, Fearon, Chodera, Singh,
  "How many crystal structures do you need to trust your docking results?", bioRxiv
  2025.09.19.677428 (p10)** — first and last authors of this piece are co-authors.
  (iii) **Reference [11], the kinase variant-effect NanoBRET dataset used on p5 and p6, is
  Singh, Gapsys, Aldeghi, … Chodera, J. Phys. Chem. B 129:2882–2902 (2025) (p11)** — again this
  piece's first and last authors.
  (iv) **Reference [64]** (Lyczek et al., PNAS 2021) is also a Chodera-lab paper.
  So three of the four empirical props under the argument are the authors' own work, all
  declared openly by citation. This is normal for an invited perspective and is recorded here
  because a reviewer from this group will be arguing from these specific papers.
  **Declared conflicts, p1:** "John D. Chodera is a current member of the Scientific Advisory
  Board of OpenEye Scientific Software, and is co-Founder, President, and CEO and has equity
  interests in Achira Inc." Also: "Sukrit Singh reports financial support was provided by
  National Institutes of Health National Cancer Institute… Damon Runyon Cancer Research
  Foundation. John D. Chodera reports… National Institute of General Medical Sciences." Funding
  p10: Damon Runyon DRQ-14-22, NCI K99 CA286801 (SS); NIH R35GM152017 and P30CA008748 (JDC);
  Sloan Kettering Institute and Gordon MERIT Fellowship (MAC).

## B. Scope

- **`system`**: **general protein.** The piece is about small-molecule drug targets in general.
  The concrete systems that actually appear: **four viral protease families in Figure 4** —
  SARS-CoV-2 main protease (Mpro), MERS-CoV Mpro, Picornavirus 2APro, Flavivirus NS3-NS2BPro
  (p7, p22) — plus **Zika virus and West Nile virus NS3-NS2BPro** for the pose-prediction panel
  (p8, p22–23), and **Abl protein kinase** as the running example for variant effects and
  NanoBRET kinetics (p5, p11 ref [11], p17 ref [64]). Also mentioned in passing: pMHC-TCR
  complexes (p17 ref [62]), antibody–antigen ΔΔG (p13 ref [29]), HSP90 (p14 ref [33]).
  Do **not** tag `kinase` off the Abl mentions: no kinase result is presented here, only cited.
- **`n_targets`**: **NOT APPLICABLE — the piece studies no targets of its own.** The numbers
  that exist belong to the re-presented Figure 4 analysis: **4 viral-family targets** for the
  affinity arm (p22) and **2 targets** (ZIKV and WNV NS3-NS2BPro) for the pose arm, evaluated
  with **1 ligand**, ASAP-0016806–001 (p8, p23). Population-scale numbers the piece quotes about
  the field, not about itself: ≥200,000 experimental PDB structures (p3), >9,000 target proteins
  in BindingDB (p4). **Generality flag: the piece generalises from four viral proteases and one
  kinase to "drug discovery" as a whole.** That is the standard latitude of a perspective, but
  it is the single most attackable step in its argument and is recorded here for that reason.
- **`method_class`**: **other — perspective/opinion piece; no method of its own.** Nearest
  schema category for its *subject matter* is `benchmark-only` (it is about how PSPMs are
  benchmarked and where benchmarks are missing), and the models it discusses are `co-folding`
  models. It does not itself run a benchmark, so `benchmark-only` is **not** tagged; see the
  rejected-tags list under Tags.
- **`backbones`**: **None run.** Models named and discussed: **AlphaFold** (p2, p7 ref [7]),
  **AlphaFold2** (p4, p20 Fig 2 timeline), **AlphaFold3** (p4, p11 ref [8], p16 ref [50] where
  it "did particularly well at pose-prediction in CASP16"), **Boltz-2** (p3, p7, p8, p9, p12 ref
  [15]; the only model actually evaluated anywhere in the piece, and only in the re-presented
  Figure 4), **Boltz-1** (p20 Fig 2), **Boltz-1x** (p17 ref [66], used to generate the SAIR
  dataset), **Chai-1** (p3, p12 ref [16]), **AlphaFold-Multimer** (p17 ref [62]), **BioEmu**
  (p20 Fig 2), **AF3Score** (p16 ref [56]), **BANANA** (p15 ref [40]). Figure 2's timeline also
  lists PLINDER, PoseBusters, Runs N' Poses, ATLAS, MDCATH, BigBind, SAIR, BindingNet,
  ASAP-Polaris, Schrödinger, OpenFE, Merck KGaA (p20).
  **`multi-backbone` is NOT tagged**: no two backbones are compared head to head *by these
  authors*. Only Boltz-2 is evaluated, and that evaluation is [67]'s.
  Explicit exclusion stated by the authors, p4: "Other models that leverage normalizing flows
  are not freely available or openly sourced and will not be discussed here."
- **`templates`**: **NOT APPLICABLE — no prediction was run by these authors, so there is no
  template setting to report.** The only template statement in the document is a characterisation
  of someone else's result, in the annotation of ref [50] (CASP16), p16: "the authors highlight
  that template-base[d] pose-prediction approaches worked incredibly well, especially when
  relative to baseline and null models." The template configuration of the Boltz-2 runs behind
  Figure 4 is **NOT REPORTED** in this piece; it lives in ref [67], which the corpus does not
  hold.
- **`msa_handling`**: **NOT APPLICABLE — no prediction was run by these authors.** MSA handling
  appears once, as a characterisation of ref [54] (Riccabona et al., Structure 2024), p15: "MSA
  subsampling, an inherently gaussian and noisy process, can generate ensembles but it does not
  provide any functionally relevant predictions from them". Note this is a **subsampling**
  statement, not a state-filtering statement; the piece never discusses state-filtered or pinned
  MSAs at all. The MSA configuration behind Figure 4 is **NOT REPORTED**.

## C. Conformational core

**Read this section as: the piece has no conformational core.** It is not a conformational-states
paper, it runs no structure prediction, and it makes no claim about generating alternative
states. Every field below is `NOT APPLICABLE` with a reason, except where the re-presented
Figure 4 analysis supplies a genuine, checkable answer — in which case the answer is given **and
explicitly attributed to [67] / Figure 4, not to a pipeline of these authors'**. Three fields do
carry real content this way: `metric_saturation`, `anti_memorization_design` and
`anti_memorization_control`.

- **`states_generated`**: **NOT APPLICABLE — nothing generated; this is an opinion piece with
  no prediction pipeline.** The piece's only statement about state/ensemble generation is a
  criticism of others, p6: "Models have emerged that generate protein ensembles, but do not
  generate the complete set of atoms (only the backbone) nor provide populations." And, of
  ref [54], p15: "current AlphaFold-like models cannot predict useful ensembles of proteins…
  the authors highlight the limitations of AlphaFold-like models, while highlighting the need
  for ensemble level data to bridge structures to functional readouts." Also p17, ref [62]:
  "emphasize the need for multi-state predictions to tackle challenges of TCR promiscuity and
  MHC restriction." **These are the piece's only contact with the multi-state literature and
  they are all second-hand.**
- **`structural_priors_used`**: **YES, and they are the subject of the paper rather than a
  choice inside it.** Three concrete priors are identifiable:
  1. **The entire argument is built on the PDB as the accumulated structural prior of the
     field** — p3: "The protein data bank (PDB) was established in 1971 and has been a
     foundational resource for modern SBDD… Starting with seven deposited structures, the PDB
     has grown to ≥200,000 experimental structures (Figure 2)"; p8: "The role of the PDB is
     best exemplified by recognizing its ~50 years of data curation that was used to train
     current PSPMs."
  2. **Figure 4C uses a deposited crystal structure as the reference for the pose comparison** —
     p23: "Pose prediction of ASAP Discovery inhibitor ASAP-0016806–001 bound to Zika virus
     NS3-NS3B as predicted by Boltz-2 (orange) relative to the crystal structure (blue, PDB:
     7I9J)." This is a *reference*, i.e. a legitimate structural prior at design time for a
     retrospective pose comparison; it is recorded here rather than as leakage, per the v3 rule.
  3. **Figure 4B is a tabulation of the deposited structural record itself**, split at the
     Boltz-2 training cutoff (p22).
  **None of these is a defect.** No structure was fed to any model by these authors.
- **`oracle_leakage`**: **NOT APPLICABLE AT THE PIPELINE LEVEL — there is no pipeline.** The
  seven v3 routes are nonetheless enumerated separately, as the schema requires, with the page
  where the (absent) protocol would be described:
  - **Route 1 — structures used as input or template:** `NOT APPLICABLE`. These authors run no
    model. For the re-presented Figure 4 analysis the input protocol is not described anywhere
    in this document (Fig 4 caption, p22–23, gives only the outputs); it lives in ref [67].
    `NOT REPORTED` for the re-presented arm.
  - **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore):**
    `NONE FOUND`. No state-annotated database is mentioned anywhere in the piece. Databases
    discussed (p3–p4, p14–p15): PDB, PubChem, ChEMBL, BindingDB, PDBbind, BigBind, Pocketome,
    CrossDocked, PPB-Affinity, MF-PCBA, PLBD, SAIR, BindingNet, PLINDER. None is a
    conformational-state annotation resource.
  - **Route 3 — cluster labels derived from known states:** `NONE FOUND`. No clustering of any
    kind is performed or discussed.
  - **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
    states:** `NOT APPLICABLE` for this piece (nothing is tuned). `NOT REPORTED` for the
    re-presented Figure 4 arm — no Boltz-2 configuration, seed count or sampling setting appears
    in this document.
  - **Route 5 — success defined post hoc by RMSD or TM to a structure they had:** **PRESENT IN
    THE RE-PRESENTED ARM, BY DESIGN, AND NOT QUANTIFIED.** Figure 4C compares a Boltz-2 pose to
    a crystal structure the authors had (PDB 7I9J, p23), and the verdict is stated in prose:
    p8, "Boltz-2 predicts correct protein structures in both cases but fails to recover the
    ligand pose, altering key interactions in ZIKV and misidentifying the binding pocket entirely
    in WNV." This is a legitimate retrospective pose evaluation, but **no RMSD, no LDDT-PLI and
    no threshold is given** — the failure is asserted from a render. Recorded again under
    `state_metric` and under Figure 4C's `hides`.
  - **Route 6 — best/worst model labels assigned against a held reference:** `NONE FOUND` in
    this piece. Whether a best-of-N selection was applied in [67] is `NOT REPORTED` here;
    Figure 4C shows a single pose per target with no selection statement (p22–23).
  - **Route 7 — design-level oracle use (systems or conditions chosen because the expected
    answer is known):** **PRESENT, WEAKLY, AND WORTH STATING PLAINLY.** The four viral families
    in Figure 4 are chosen precisely because their data situations differ in a known way, and
    the piece says so before reading the result — p7: "Given the plethora of pre-cutoff-date
    structures available for well-studied systems like SARS-CoV-2 Mpro (Figure 4B), Boltz-2
    demonstrates **the expected ability** to evaluate new ligands in this target." The expected
    answer is declared, then confirmed. This is **design-level, not pipeline-level**: nothing
    leaky was fed to Boltz-2, and the interesting half of the result (Picornavirus and
    Flavivirus fail *despite* having an order of magnitude more structures than MERS-CoV) is
    the half that contradicts the expectation — p8: "Both have an order of magnitude more
    structural data than MERS-CoV MPro but perform worse." Tagged `design-level-oracle`, not
    `oracle-leak`.
  **The piece's own position on leakage is the sharpest thing in it and belongs in this field
  even though it is about others' work:** p7, "To prevent data leakage, training sets cannot
  contain this use-case data. Additionally, current benchmarks can be used to train subsequent
  models, suggesting a need for continually updated assessments."; p7, "Critically, compounds
  not present in training must be evaluated to minimize data leakage."; p3, "there is a large
  data gap driving our inability to evaluate the limitations of these methods (Figure 2),
  particularly if past benchmarks are part of the training data."; and, of ref [30], p13:
  "the authors… identify train-test data leakage between PDBbind and CASP benchmark datasets.
  This data leakage likely drives the inflated performance of currently available
  AlphaFold-like models, leading to overestimation of the generalization capability."
- **`prospective`**: **NOT APPLICABLE for the piece — it makes no predictions.** For the
  re-presented Figure 4 arm: **partial → effectively yes on the affinity panel, no on the pose
  panel.** The affinity arm is prospective by construction — the Figure 4A y-axis reads
  "Boltz-2 ROC AUC against **prospective** ligands" (p22) and Figure 4B splits the PDB record
  at "Boltz-2 data cutoff **2023-06-01**" into "Before cutoff (retrospective)" and "After cutoff
  (prospective)" (p22). The pose arm (4C) is retrospective: the ZIKV crystal structure 7I9J
  already existed and is used as the reference (p23), and no cutoff status is stated for it.
- **`state_metric`**: **NOT APPLICABLE — no conformational state is scored anywhere.** The
  metrics that do appear in the re-presented Figure 4 are ligand-level, not state-level, and
  they are **dual in character**: **continuous (ROC AUC on pIC50-labelled ligands, p7, p22)
  + visual only (the pose verdict in 4C, asserted from a render with no RMSD, p8, p23)**.
  No threshold is stated for either — no ROC AUC success threshold, no RMSD cutoff. The one
  numeric threshold anywhere in the piece is quoted from ref [5], p6: "Only a few structures
  are needed to pose 70% of candidate ligands within **2 Å** of the correct binding pose."
- **`metric_saturation`**: **YES, NUMERIC, IN FIGURE 4A: ROC AUC floors at 0.5, the
  random-classifier value, and one bar sits exactly on that floor.** p7: "This promising
  universality does not extend to more distant viral families, with Boltz-2 affinity predictions
  showing lower ROC AUC values (with high error bars) for Picornavirus 2APro and **dropping to
  0.5** for Flavivirus NS3-NS2BPro (Figure 4A)." The panel draws a dashed reference line at 0.5
  (p22 render). ROC AUC cannot report *how much worse than random* a predictor is, so the
  Flavivirus result is floored and the metric carries no further information there. This is
  numeric saturation and is recorded here; the figure-level defects (undefined error bars, the
  invisible MERS bar) are recorded in `hides` in section F, per the v3 rule, and are not
  duplicated here.
- **`directional_control`**: **NOT APPLICABLE — nothing is generated, so there is no handle to
  instruct.** No partner, ligand, nanobody, peptide, state-annotated template, state-filtered
  MSA, seed or subsample depth is used as a control anywhere in the piece.
- **`anti_memorization_design`**: **PRESENT IN THE RE-PRESENTED ARM.** The design is a
  **temporal split at the Boltz-2 training-data cutoff, 2023-06-01**, stated on the Figure 4B
  chart title (p22): "PDB Entries Before/After Boltz-2 data cutoff **2023-06-01**". n, read from
  the printed bar labels in Figure 4B (p22): SARS-CoV-2 Mpro **743 before / 1044 after**;
  MERS-CoV Mpro **40 before / 19 after**; Picornavirus 2APro **334 before / 594 after**;
  Flavivirus NS3-NS2B **423 before / 257 after**. The body restates the MERS figure, p7–p8:
  "≤100 MERS-CoV MPro structures are deposited, and only **40** are available by the
  cutoff-date". A second, independent temporal design is quoted from ref [5], p5: docking
  strategies "were assessed in a real-world program, using a **temporal split**".
  **For the piece itself: NONE — there is nothing to hold out.**
- **`anti_memorization_control`**: **RUN AND ANALYSED — in the re-presented arm only, and it is
  the piece's single strongest empirical point.** The before/after-cutoff structure counts
  (Fig 4B) are not merely tabulated; they are set against the Fig 4A performance and the
  comparison is what generates the conclusion, p8: "Picornavirus 2APro and Flavivirus
  NS3–NS2BPro have similar numbers of structures in the PDB prior to the cutoff-date (Figure 4B)
  yet perform differently. Both have an order of magnitude more structural data than MERS-CoV
  MPro but perform worse. This discrepancy highlights current limitations of PSPMs and
  underscores the need for more diverse datasets to improve generalization and reduce the risk
  of memorization." **UNPOWERED at the target level: n = 4 targets in the affinity comparison
  and n = 2 targets, 1 ligand, in the pose comparison.** The per-target ligand counts are large
  (176–1373 pIC50 values, Fig 4A) but the unit of the generalisation claim is the *viral family*,
  and there are four of them. Tagged `unpowered` on that basis, and the basis is stated so the
  tag is not misread as "the whole thing is underpowered".
  **For the piece itself: NONE RUN.**
- **`controls_run`**: **NONE RUN BY THESE AUTHORS.** The piece runs no arm of any kind. The
  table below records the control arms present **in the re-presented Figure 4 analysis**, which
  is what a reader will want; every row is attributed to Figure 4 / ref [67], not to this piece.

  | control | what it rules out | page |
  |---|---|---|
  | Random-classifier reference line drawn at ROC AUC = 0.5 in Fig 4A | Rules out reading a low AUC as weak-but-real signal; fixes the floor against which Flavivirus (0.50) is judged | p22 (dashed line, render); p7 (text) |
  | Data-cutoff temporal split, 2023-06-01, tabulated per target (Fig 4B) | Rules out the explanation that good performance is simple recall of post-cutoff deposited complexes; establishes which ligands are genuinely prospective | p22 |
  | MERS-CoV Mpro as a **low-structure, close-homolog** arm (40 pre-cutoff structures) | Rules out "performance requires many structures of the target itself" — MERS succeeds on borrowed SARS-CoV-2 signal | p7–p8, p22 |
  | Picornavirus 2APro and Flavivirus NS3-NS2B as **distant-family** arms with *more* structures than MERS | Rules out raw structure count as the explanatory variable; isolates family distance / diversity as the driver | p8, p22 |
  | Per-target pIC50 test-set sizes printed beneath the AUC bars (1323 / 1373 / 176 / 534) | Rules out small-test-set artifact as the explanation for the low AUCs — Flavivirus has 534 values and still floors at 0.5 | p22 |
  | WNV NS3-NS2BPro pose prediction alongside ZIKV, same ligand | Rules out "the ligand is simply hard" — the model gets the protein right in both and the pocket wrong in one | p8, p22–23 |
  | Protein-structure prediction reported alongside the pose failure ("Boltz-2 predicts correct protein structures in both cases") | Rules out a folding failure as the cause of the pose failure; isolates the protein–ligand step | p8 |

  **Controls conspicuously absent from the re-presented arm, since their absence is what a
  reviewer would press on:** no second model (Chai-1, AF3) run as a comparator, no docking or
  physics baseline, no null/random-ligand arm, no scrambled-sequence arm, and no repeat-seed
  arm. The error bars in Fig 4A are never defined (see `hides`).
- **`confidence_as_discriminator`**: **NOT APPLICABLE / NOT REPORTED.** pLDDT, pTM and ipTM are
  never mentioned in the piece. Confidence is never used to judge correctness, and the
  validity of doing so is never discussed. The nearest adjacent statement is about affinity
  *modules* rather than confidence heads, p3: "Some open-source PSPMs, such as Boltz-2 and
  Chai-1, predict ligand-binding affinity alongside structure."

## D. Claims

- **`central_conclusion`**: The bottleneck on AlphaFold-like protein structure prediction models
  (PSPMs) becoming useful for drug discovery is **data, not architecture**: there is now enough
  monomeric structural data to predict folds but far too little diverse, systematically measured
  protein–ligand binding, kinetics and variant-effect data to predict poses, affinities or the
  downstream properties a real Design-Make-Test-Analyze cycle needs. The authors argue for a
  hierarchical "task" framework that names, per drug-discovery task, which models are mature,
  which are promising and which are untapped for want of data; and they argue that progress
  requires large-scale systematic data generation, harmonised assay labelling, and continually
  refreshed blind challenges, because existing benchmarks leak into training sets and current
  models largely memorise.

- **`necessity_claims`** — **VERBATIM + page.** These are the load-bearing sentences and the
  ones a reviewer from this group would quote at us. Ordered by page.

  | # | verbatim | page |
  |---|---|---|
  | 1 | "However, it is critical to assess the limitations of these models using blind challenges, and to expand existing datasets to better reflect real-world drug design tasks." | p1 (abstract) |
  | 2 | "Finally, we emphasize the need for systematic dataset generation to support the development of frontier models and highlight recent efforts to generate experimental and physics-based datasets for challenging tasks in drug discovery." | p1 (abstract) |
  | 3 | "However, there has been no historical standard to assess AI/ML method performance, and many models quickly fail in prospective testing." | p3 |
  | 4 | "…there is a large data gap driving our inability to evaluate the limitations of these methods (Figure 2), particularly if past benchmarks are part of the training data." | p3 |
  | 5 | "In large part, these methods fail due to a lack of protein-ligand binding data hindering our ability to rigorously assess performance." | p3 |
  | 6 | **"In this piece, we assert that more protein[-]ligand binding and kinetics data is needed for modern AI/ML structural methods to enable prospective evaluation with SBDD."** | p3 |
  | 7 | "We argue that a "task hierarchy" must be crafted to better identify the types of data required to maximize success at each stage of the assay cascade." | p3 |
  | 8 | "It is crucial to curate usable data subsets for specific SBDD tasks from large publically-available repositories." | p4 |
  | 9 | "This reduces the effective diversity of protein-ligand structures available for training and limits the prospective predictive power of modern AI/ML models." | p4 |
  | 10 | **"We emphasize that for rigorously predictive models, training data must be both high in volume *and* in diversity; focused structural data describing a specific set of protein-compound interactions is not able to train a model on the generalized set of protein-ligand interactions, and so structural/biochemical data must represent as diverse a pharmacological space as possible."** | p5 |
  | 11 | "Therefore, there is a clear need for large-scale, efficient systematic assays." | p5 |
  | 12 | "Despite the availability of these biochemical datasets, no data-driven model has established itself as a prospective prediction engine for drug residence time properties, inhibitor binding affinities, or variant-effect classification." | p5 |
  | 13 | "More experimental data must be collected and shared to drive model building in SBDD." | p5 |
  | 14 | "It will be critical to note data type used at each stage using labeling and harmonizing schemes, as synthetic data cannot be weighted equally against biophysical measurements." | p5 |
  | 15 | "Not all model-specific tasks have established themselves as prospectively predictive, and not every task has an existing benchmark to appropriately compare models." | p6 |
  | 16 | "An increase in volume and diversity of assay data and biochemical readouts will be needed for frontier PSPMs and AI/ML models to infer mechanistic modalities." | p6 |
  | 17 | "We assert that frontier PSPMs will strike a balance between AI training and physics-based intuition to combine the best of both worlds. Addressing new challenges and failure modes will require new data types at trainable scales" | p6 |
  | 18 | "Critical tasks for precision medicine such as variant effects, induced-fit, folding-upon-binding, and kinetics remain drug-relevant properties where insufficient data exists." | p6 |
  | 19 | "Lastly, kinetics is gaining appreciation as a critical property for drug design, but little data exists to predict residence time." | p7 |
  | 20 | "The scarcity of protein-ligand structures and rigorous benchmarks has limited the success of protein-ligand binding predictors." | p7 |
  | 21 | **"To prevent data leakage, training sets cannot contain this use-case data. Additionally, current benchmarks can be used to train subsequent models, suggesting a need for continually updated assessments."** | p7 |
  | 22 | "Critically, compounds not present in training must be evaluated to minimize data leakage." | p7 |
  | 23 | "This discrepancy highlights current limitations of PSPMs and underscores the need for more diverse datasets to improve generalization and reduce the risk of memorization." | p8 |
  | 24 | **"We argue that the amount of systematically available protein[-]ligand data is the main bottleneck to improved PSPM training."** | p8 |
  | 25 | **"Across these studies, a consistent theme emerges: there is enough monomeric structural data to predict structures, but not enough ligand-binding and affinity data to extrapolate to predicting protein[-]ligand interactions."** | p8 |
  | 26 | "As more models are released, blind challenges will be critical to identify generalizable and performant models, consensus around training strategies, and useful datasets." | p9 |
  | 27 | "In outlining existing model limitations, and the importance of blind challenges, we assert that a hierarchical task structure must be used to identify and tackle key challenges in conducting SBDD with PSPMs." | p9 |
  | 28 | "For example, there are no established datasets or curated efforts to predict drug-residence times and kinetics." | p9 |
  | 29 | **"However, datasets at the scale and breadth needed for predictive models to exist requires large scale data generation and curation efforts."** | p9 |
  | 30 | **"Together, rigorous generation, curation, and evaluation of datasets and models is essential to drive model evolution towards the predictive power needed to accelerate real-world drug discovery."** | p10 |

  **The four sentences to quote if only four are wanted** — the central argument compressed:
  #6 (p3, the thesis), #10 (p5, volume *and* diversity), #24/#25 (p8, the bottleneck named and
  the fold/ligand asymmetry stated), #30 (p10, what would be required).

  **Impossibility-shaped statements, recorded separately because they are the strongest form:**
  #12 (p5, *no* data-driven model has established itself as a prospective engine for residence
  time, affinity or variant effects), #21 (p7, training sets **cannot** contain use-case data),
  #28 (p9, there are **no** established datasets for residence time and kinetics), and #10's
  "is not able to train a model on the generalized set of protein-ligand interactions" (p5).

- **`novelty_claims`** — **NO EXPLICIT PRIORITY CLAIM.** The piece never uses "first", "novel",
  "unprecedented" or "for the first time" about its own contribution. Searched: those words
  appear only about other people's results ("a novel CDK20 small molecule inhibitor", p12 ref
  [14]; "a novel mechanism of imatinib resistance", p17 ref [64]; "novel ligands", p2). The
  closest things to a contribution claim, quoted verbatim because they are what a priority
  dispute would turn on if one ever arose:
  - p1 (abstract): "We offer a hierarchical framework for parsing which tasks current models
    perform well, and which remain challenging or unexplored."
  - p3: "The task hierarchy we present (Figure 3) acknowledges the current success in
    protein-structure prediction, as well as the challenges and lacking benchmarks for
    functionally relevant biochemical properties, such as blood-brain barrier penetration and
    ligand-residence time."
  - p3: "We hope that our task hierarchy will serve as a descriptive blueprint for fine-tuning
    modern AI/ML models."
  - p2: "Rather than a single filter or funnel, we assert that SBDD is best viewed as a
    Design-Make-Test-Analyze cycle (Figure 1)…" — a reframing claim, explicitly positioned
    against the prevailing "filtration process" view.
  **The claimed contribution is a framework, offered as "descriptive", with the authors' own
  hedge attached (see `stated_limits`).**

- **`stated_limits`** — limits the authors state themselves:
  1. **The framework is admitted to be incomplete**, p6: "It is important to note that our task
     breakdown is not exhaustive, and new challenges will emerge as established models succeed
     at current tasks."
  2. **The framework is offered as descriptive, not prescriptive**, p3: "We hope that our task
     hierarchy will serve as a **descriptive** blueprint…"
  3. **Scope exclusion of a whole model class**, p4: "Other models that leverage normalizing
     flows are not freely available or openly sourced and will not be discussed here."
  4. **The core premise of SBDD is admitted to be hard to quantify**, p2: "This rapid
     acceleration, while difficult to measure, has enabled SBDD to become a popular approach to
     drug discovery…"
  5. **The DMTA picture is admitted to be a simplification**, p2: "It is worth noting that
     real-world pipelines have additional tiers, with both positive and negative readouts used
     in subsequent analyses."
  6. **The success criterion in their own cited diminishing-returns result is admitted to be
     narrow**, p10 (annotation of ref [5]): "While limiting the definition of "success" to
     pose-prediction in this case…"
  7. **The physics-based alternative they advocate is not exempted from criticism**, p13
     (annotation of ref [31]): "…although the sampling strategy used may be difficult to
     interpret for discovery-oriented questions about kinetic pathways or transition states."
  8. **Their own kinetics claim is bounded to order-of-magnitude accuracy**, p7: "Physics-based
     models now predict drug-residence time within an order of magnitude, and can fill this data
     gap."
  9. **Conflicts of interest declared in full**, p1 (Chodera: OpenEye SAB; Achira co-founder,
     President, CEO, equity). Relevant because the piece advocates for physics-based data
     generation and for open data consortia.
  **Not stated as a limit anywhere, and worth noting as such:** that three of the four empirical
  props are the authors' own preprints (see section A), and that the Figure 4 conclusion rests
  on four viral families.

- **`stance`**: **`background` on framing + `contrast` on rigour standards. PROVISIONAL — this
  is the user's call and is not presented as settled.**
  - **`background`, on framing:** this is the canonical citation for "the data are the
    bottleneck for AlphaFold-like models in drug discovery". It is a review-family piece that
    sets the scene; it does not compete with a methods result and it establishes no precedent
    for any technique.
  - **`contrast`, on rigour standards:** its operative content is a set of demands — prospective
    evaluation on post-cutoff data, benchmarks that are not in the training set, continually
    refreshed blind challenges, harmonised assay labelling, volume **and** diversity, and no
    equal weighting of synthetic against biophysical data (#10, #14, #21, #22, #26, p5–p9).
    Any claim of ours about model performance is measurable against that list, sentence by
    sentence. That is a contrast relationship, not a background one.
  - **Explicitly NOT `threat`:** the piece contains no result that could pre-empt or contradict
    a conformational-states methods contribution. It does not touch alternative-state
    generation except at second hand (see `states_generated`).
  - **`negative-result` is tagged separately**, because the piece's substantive empirical
    content is a failure: Boltz-2 at chance on Flavivirus affinity and wrong-pocket on WNV pose.

---

### Extra, non-schema: the piece's concrete recommendations, with pages

**v3 has no field for "recommendations the paper makes".** For a perspective that is the most
actionable content in the document and the thing our own work will be measured against, so it is
recorded here as a clearly-labelled extra block rather than smuggled into `stated_limits` (the
v2 failure mode the changelog names) or dissolved into `necessity_claims`. Flagged in
`unresolved` item 1. Each row is a recommendation the authors make in their own voice.

| # | recommendation | form / concreteness | page |
|---|---|---|---|
| R1 | **Three-part programme for improved models, numbered by the authors:** "Improved model generation will be achieved through **1. Better data harmonization, standardization, and labeling in datasets, 2. Systematic assay and protocol usage to ensure reproducible dataset-generation, and 3. The use of blind challenges and benchmarks to test when a point of diminishing returns has been reached for a certain assay type.**" | Explicit, numbered, verbatim. **This is the recommendation list of the paper.** | p8–p9 |
| R2 | **Build and use a task hierarchy** to decide what data to collect per task, with per-task "model maturity" labelled as established (solid) / promising (dashed) / untapped (dotted). "We connect these tasks hierarchically, with subsequent tasks and metrics building on prior tasks and data (Figure 3)." | Framework, operationalised only as Figure 3's schematic | p6, p9, p21 |
| R3 | **Run continually refreshed blind challenges**, because today's benchmark becomes tomorrow's training set: "current benchmarks can be used to train subsequent models, suggesting a need for continually updated assessments." Named as the model to build on: **CASP, SAMPL, CACHE**, and the new prospective challenges from **ASAP Discovery and OpenADMET**. | Concrete: names five challenge programmes | p7, p9 |
| R4 | **Evaluate on under-represented use cases with the use-case data excluded from training:** "Testing on under-represented use-cases best demonstrates a model's extrapolation ability by revealing which underlying principles the model has learned that transfer to new systems. To prevent data leakage, training sets cannot contain this use-case data." | A reporting/protocol standard, stated as a requirement | p7 |
| R5 | **Predict compound efficacy across protein families as the generalisability test:** "An ideal way to evaluate model generalizability is to predict compound efficacy across protein families. Critically, compounds not present in training must be evaluated to minimize data leakage." | A concrete evaluation design; instantiated by Figure 4 | p7 |
| R6 | **Large-scale systematic data-generation programmes, named:** "New efforts such as **OpenADMET** and **OpenBind** promise to expand the diversity and volume of training data"; "Existing efforts such as **OpenBind** seek to curate the large datasets needed in an open, scalable manner." Also named as exemplar data producers: the **ASAP Discovery Consortium**, and the **Protein Structure Initiative** as historical precedent. | Concrete: names the programmes it wants funded/used | p3, p9 |
| R7 | **Use large-scale in vitro and in cellulo biochemical infrastructure, specifically NanoBRET**, to generate systematic affinity, variant-effect and kinetics data: "Modern experimental biochemistry infrastructure can address this scaling issue by collecting large-scale biochemical measurements…"; "NanoBRET can also measure datasets of protein-ligand kinetic measurements". | Concrete assay named | p5 |
| R8 | **Label and down-weight synthetic data; do not pool it with measurement:** "It will be critical to note data type used at each stage using labeling and harmonizing schemes, as synthetic data cannot be weighted equally against biophysical measurements." | A reporting standard, stated as a requirement | p5 |
| R9 | **Do not pool IC50/Ki across assay contexts without annotation** — the piece's assay-provenance standard, carried by ref [34]: "combining literature IC50 data without annotation of the assays used, nor the assay dynamic ranges, into a single pooled set contributes significant noise into model training and leads to large unneeded inaccuracy"; and in the authors' own voice, "kinase-inhibitor IC50s can come from BaF3 viability, mobility shift, or qPCR measurements; each assay context with its own dynamic range and variance." | A reporting standard with a quantified cost (0.3 log units to >1 order of magnitude, p14) | p5, p14 |
| R10 | **Stop adding data of a single type past its point of diminishing returns; treat data generation as resource allocation:** ">5 crystal structures of a known scaffold already passes the point of diminishing returns; only a few structures are needed to pose 70% of candidate ligands within 2 Å". "identifying points of diminishing returns indicates when additional data sources are needed." | **The only quantified dataset-size recommendation in the piece** | p6, p10 |
| R11 | **Combine statistical and physics-based approaches rather than choosing:** "We assert that a balance between statistical inference and physics-based intuition is key… frontier PSPMs will strike a balance between AI training and physics-based intuition". Physics-based synthetic data is endorsed as augmentation (refs [29], [31]). | Direction, not a protocol | p6, p5 |
| R12 | **Retain and use negative data** from the assay cascade: "Our DMTA-cycle framework emphasizes the role negative data plays in model construction; effective models prospectively identify true binders and **discriminate away from ineffective candidate compounds** prior to expensive synthesis and testing"; "all the data from each of these tests, both positive and negative, are incorporated into the analysis and design of subsequent rounds" (Fig 1 caption). | Direction, with a figure | p8, p19 |
| R13 | **Test on targets, anti-targets and drug-like properties, not only on potency:** "Models built with these large datasets can be rigorously tested using a sustained set of blind challenges on targets, anti-targets, and other drug-like properties." Untapped tasks named: anti-target avoidance, ADMET, blood-brain-barrier penetration, drug-residence time. | Concrete scope for future challenges | p6, p9 |

**No target dataset size is ever specified.** The piece asks for "large scale", "trainable
scales", "volume *and* diversity" and never names a number of structures, measurements or
targets that would suffice. The only quantities it offers are the current shortfall (15K
paired structures vs 2.9M measurements vs "trillions of tokens needed for LLM training", p8)
and the *upper* bound of usefulness for one narrow task (>5 same-scaffold crystal structures,
p6). Recorded because "how much data would be enough" is the obvious question this piece
raises and does not answer.

---

### Extra, non-schema: how the piece characterises the current evidence base

Recorded exactly and neutrally, because a reviewer from this group will bring these specific
judgements. **Named benchmarks, datasets and models criticised, and on what grounds.**

| object | characterisation | grounds | page |
|---|---|---|---|
| **PDB (as a training corpus)** | "only a fraction of the structures in the PDB (<20%) are protein-ligand structures… Many of these structures may be duplicated complexes, non-drug-like ligands, or drug analogs binding to protein homologs. This reduces the effective diversity…" | Composition: low ligand fraction, redundancy, non-drug-like chemistry | p4 |
| **PDBbind + CASP benchmark sets** | "identify train-test data leakage between PDBbind and CASP benchmark datasets. This data leakage likely drives the inflated performance of currently available AlphaFold-like models, leading to overestimation of the generalization capability… Retraining top-performing models on CleanSplit caused benchmark performance to drop substantially" | Train–test leakage → inflated reported performance (via ref [30], Graber et al.) | p13 |
| **ChEMBL / pooled IC50 and Ki collections** | "The authors flag large collections like ChemBL as providing increased risk when pooling assays and estimate the degree of noise found in IC50 measurements across assays for the drug-target pair, ranging 0.3 log units to more than one order of magnitude." | Assay heterogeneity, unannotated provenance (via ref [34], Landrum & Riniker) | p14 |
| **BindingDB** | "it lacks easily parseable 3D protein structural data (which is not guaranteed to match the exact construct assayed), nor does it often label what ligand in the congeneric series is the crystallographic ligand… can often contain duplicate entries, but does not often annotate the assay from which an affinity was provided." | Missing structure pairing, missing assay annotation, duplication | p14 |
| **PLINDER / Runs N' Poses** | "the authors provide a clean benchmarking split that demonstrates where the PLINDER set provides useful training data or otherwise… only a few metrics such as RMSD and LDDT, when compared against the training set, are needed to predict the performance of any prediction accurately. Their results demonstrate that current cofolding approaches largely **memorise** ligand poses from their training data, hindering their use for de novo drug design." | Performance predictable from training-set similarity → memorisation (via ref [28], Škrinjar et al.) | p13 |
| **ML-based scoring functions in general** | "The authors propose a baseline model that can only learn dataset biases… The baseline models are competitive in accuracy to existing MLBSFs in many proposed benchmark tasks and evaluations, indicating that models are heavily learning biases in the dataset." | A bias-only baseline matches them (via ref [9], Durant et al.) | p10–p11 |
| **Co-folding models generally, on pose prediction** | "Many of these models fail to predict binding poses for new ligands… a variety of new benchmarks pioneered by **Charlotte Deane and others** highlight points of failure." | Failure on unseen ligands | p4 |
| **Affinity-prediction models generally** | "recent efforts highlight the inability of these models to correctly predict affinities in larger systematic screens… they often struggle to predict binding affinities or rank candidates, a critical ability…" | Fail at ranking in systematic screens | p4 |
| **AlphaFold3, in CASP16** | "AlphaFold3 did particularly well at pose-prediction in CASP16, but **all contestants showed only modest performance at best with affinity prediction**. In fact, most methods correlated poorly with experimental data even in the face of experimental error. The paper strikingly notes that **providing experimental structures did not improve affinity predictions**, suggesting that the scoring functions are a limiting factor." | Praised on pose, criticised (with the whole field) on affinity (via ref [50], Gilson et al.) | p16 |
| **Boltz-2** | "PSPMs like Boltz-2 are unable to generalize pose or affinity predictions across viral families" (Fig 4 title); ROC AUC "dropping to 0.5 for Flavivirus NS3-NS2BPro"; "fails to recover the ligand pose, altering key interactions in ZIKV and **misidentifying the binding pocket entirely** in WNV" | Chance-level affinity discrimination on a distant family; wrong pocket on pose | p7, p8, p22 |
| **AlphaFold-like models for ensembles** | "current AlphaFold-like models cannot predict useful ensembles of proteins. MSA subsampling, an inherently gaussian and noisy process, can generate ensembles but it does not provide any functionally relevant predictions from them" | Ensembles not functionally meaningful (via ref [54], Riccabona et al.) | p15 |
| **Ensemble generators generally** | "Models have emerged that generate protein ensembles, but do not generate the complete set of atoms (only the backbone) nor provide populations." | Backbone-only, no populations | p6 |
| **AlphaFold-Multimer for pMHC-TCR** | "these starting models fail to capture key geometric details that benefit evaluation" | Geometric detail (via ref [62], McMaster et al.) | p17 |
| **Models trained on deep-mutational-scanning data** | "many models remain trained on deep-mutational-scanning data which can convolve binding and fitness together… such measurements may miss variants that sensitize the target to ligands." | The label conflates binding with fitness | p6 |
| **ML models on variant effects** | "models cannot identify which variants sensitize a kinase to known inhibitors, and struggle with allosteric mutations"; "the ML-based model demonstrates evidence of data **memorization**, likely due to the small data volume" | Memorisation on small data; blind to sensitising and distal mutations (via ref [11]) | p5, p11 |
| **Models trained on experimental data, tested on synthetic (SAIR)** | "models trained on experimental data do not generalize well to synthetic data" | Distribution shift (via ref [66], Lemos et al.) | p17 |
| **Datasets and challenges generally** | "Many additional databases also have arisen to enable SBDD tasks but **only a few of these have been maintained and updated**"; Fig 2 marks unsupported ones with † | Abandonment / lack of maintenance | p4, p20 |

**Balancing statements, recorded so the characterisation is not read as uniformly negative:**
"AlphaFold emerged as a clear victor for protein fold prediction" (p4); "many established
models are capable of monomeric protein fold prediction" (p6); "Boltz-2 demonstrates the
expected ability to evaluate new ligands in this target" and generalises to MERS-CoV despite
sparse data (p7); "we emphasize the grand potential these models have to accelerate affinity
prediction, although more data is needed" (p8); "some efforts to discover small molecule
inhibitors using AlphaFold have identified novel ligands" (p2); template-based pose prediction
"worked incredibly well" in CASP16 (p16).

## E. Quantitative comparators

**Read the `measured against` column carefully: almost nothing here is this piece's own
measurement.** Rows are marked **[Fig 4 / ref 67]** where the number comes from the re-presented
analysis, **[quoted]** where the piece is quoting a third party, and **[piece]** where the
number is the piece's own tabulation of the public record.

- **`metrics_reported`**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Boltz-2 affinity ROC AUC, SARS-CoV-2 Mpro | ≈0.87 *(read from the p22 render; no numeric label printed)* | ROC AUC (0.5 = chance) | 1323 prospective pIC50-labelled ligands **[Fig 4 / ref 67]** | p22 |
  | Boltz-2 affinity ROC AUC, MERS-CoV Mpro | ≈0.88 *(read from render)* | ROC AUC | 1373 pIC50 values **[Fig 4 / ref 67]** | p22 |
  | Boltz-2 affinity ROC AUC, Picornavirus 2APro | ≈0.69, with the largest error bar in the panel (≈0.55–0.83) *(read from render)*; text: "lower ROC AUC values (with high error bars)" | ROC AUC | 176 pIC50 values **[Fig 4 / ref 67]** | p7, p22 |
  | **Boltz-2 affinity ROC AUC, Flavivirus NS3-NS2B** | **0.50** *(stated in text)* | ROC AUC | 534 pIC50 values **[Fig 4 / ref 67]** | p7, p22 |
  | pIC50 values in test set | 1323 / 1373 / 176 / 534 | count | SARS-CoV-2 Mpro / MERS-CoV Mpro / Picornavirus 2APro / Flavivirus NS3-NS2B **[Fig 4 / ref 67]** | p22 |
  | PDB entries **before** Boltz-2 cutoff (2023-06-01) | 743 / 40 / 334 / 423 | count | same four targets **[Fig 4]** | p22 |
  | PDB entries **after** cutoff | 1044 / 19 / 594 / 257 | count | same four targets **[Fig 4]** | p22 |
  | MERS-CoV Mpro structures deposited | ≤100 total; **40** by the cutoff date | count | PDB **[piece]** | p7–p8 |
  | Boltz-2 pose prediction, ZIKV NS3-NS2BPro, ligand ASAP-0016806–001 | protein correct, ligand pose **wrong** ("altering key interactions"); **no RMSD given** | qualitative | crystal structure **PDB 7I9J** **[Fig 4 / ref 67]** | p8, p23 |
  | Boltz-2 pose prediction, WNV NS3-NS2BPro, same ligand | protein correct, **binding pocket misidentified entirely**; **no RMSD given** | qualitative | no experimental reference shown **[Fig 4 / ref 67]** | p8, p23 |
  | Total experimental structures in the PDB | ≥200,000 (from 7 at founding, 1971) | count | PDB, plotted to ~2025 in Fig 2 **[piece]** | p3, p20 |
  | Protein–ligand fraction of the PDB | **<20%** | % of entries | PDB **[piece]** | p4 |
  | Paired structure–affinity data vs unpaired affinity data vs LLM training scale | **~15K structures vs 2.9 million measurements vs "trillions of tokens needed for LLM training"** | counts | the piece's own framing of the bottleneck **[piece]** | p8 |
  | BindingDB scale | 2.9 million protein–ligand affinity measurements; >9,000 target proteins; ≥1200 pre-defined congeneric series | counts | **[quoted, ref 38]** | p4, p14 |
  | PDBbind scale | subset of the PDB with affinities drawn from >50,000 publications | count | **[quoted, ref 39]** | p4 |
  | Crystal structures needed for docking pose success | **>5 same-scaffold structures passes the point of diminishing returns**; a few structures pose **70%** of candidate ligands within **2 Å** | % and Å | COVID Moonshot, temporal split **[quoted, ref 5]** | p6, p10 |
  | Noise from pooling IC50 across assays | **0.3 log units to more than one order of magnitude** | log units | drug–target pairs across assays **[quoted, ref 34]** | p14 |
  | Physics-based drug-residence-time accuracy | "within an order of magnitude" | orders of magnitude | **[quoted, refs 31–33, 68]** | p7 |
  | SBDD adoption | ≥65% of successful hit-to-clinic progressions (as of 2023); 33% of programs 2015–2022 used SBDD for hit-finding | % | **[quoted, refs 2,3]** | p2 |
  | DMTA attrition | ≤1% of initial designs nominated as preclinical candidates | % | **[quoted, ref 3]**; drawn in Fig 1 | p2, p19 |
  | Škrinjar benchmark scale | 2,600 protein–ligand systems after quality/diversity filters on PLINDER | count | **[quoted, ref 28]** | p13 |
  | Hummer synthetic-data scale | 1,000,000 FoldX + 20,000 Rosetta Flex-ddG synthetic ΔΔG values | count | **[quoted, ref 29]** | p13 |
  | SAIR scale | >5,000,000 co-folded 3D structures; >1,000,000 protein–ligand pairs; 5,149 unique protein sequences | count | **[quoted, ref 66]** | p17 |
  | BigBind scale | ~583,000 3D pocket structures with ligand activities; ~22M CrossDocked complexes aggregated | count | **[quoted, ref 40]** | p14–p15 |

- **`n_predictions`**: **NONE BY THESE AUTHORS.** For the re-presented Figure 4 arm, reported
  separately as the schema requires:
  - **Targets:** 4 (affinity arm: SARS-CoV-2 Mpro, MERS-CoV Mpro, Picornavirus 2APro, Flavivirus
    NS3-NS2B) + 2 (pose arm: ZIKV, WNV NS3-NS2BPro) (p7–p8, p22–23).
  - **Ligands scored per target (affinity arm):** 1323 / 1373 / 176 / 534 = **3406 total
    pIC50-labelled ligands** (Fig 4A, p22).
  - **Ligands in the pose arm:** **1** (ASAP-0016806–001), on 2 targets (p8, p23).
  - **Samples/seeds per prediction:** **NOT REPORTED** — no seed count, no best-of-N statement,
    no sampling configuration appears anywhere in this document.
- **`comparable_to_ours`**: *(left empty by instruction)*
- **`si_in_scope`**: **NO SUPPLEMENTARY MATERIAL EXISTS FOR THIS PIECE, AND NONE IS NEEDED — but
  the real numbers behind its one data figure are held elsewhere and the corpus does not hold
  them.** The 23-page PDF is the complete author manuscript: main text (p1–p10), references
  (p10–p18), four figures (p19–p23). No SI is cited anywhere. **However:** every number in
  Figure 4 originates in **ref [67], Castellanos et al., bioRxiv 2025.07.29.667267 (p17)**,
  which is **NOT HELD** by this corpus, and this piece reproduces no ROC curves, no per-ligand
  data, no error-bar definition, no Boltz-2 configuration and no RMSD. Record as
  **`SOURCE PREPRINT NOT HELD`** — the functional equivalent of `SI NOT HELD` for a perspective.
  Likewise the diminishing-returns numbers on p6 come from **ref [5], Payne et al., bioRxiv
  2025.09.19.677428**, also not held. If either number is to be used in our manuscript, cite
  the primary preprint, not this piece.

## F. Figures

Four figures. **Seven panel-group rows** below. Splitting follows the v3 rule — split on `mark`
or `measure`, never on `facet` alone — which forces Figure 4's panel A into **two rows** (its
top sub-panel measures ROC AUC, its bottom sub-panel measures a count; same bar mark, different
measure) and puts 4B in a third row (a different count, with a stacked series 4A-bottom does not
have). Panel letter **A therefore appears in two rows**, which v3 explicitly permits.

**Two pages were rendered to fill panel structure the captions do not carry: p20 (Figure 2 —
the caption names colours but not the mark, the axis or the annotation layer) and p22
(Figure 4 — the caption says "ROC Curve" where the panel in fact shows ROC *AUC* as bars, and
does not say that A is two stacked sub-panels).** Both renders were deleted after reading.
Figures 1 and 3 were not rendered: their captions are fully sufficient because both are
schematics with no data.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | p19 | The Design-Make-Test-Analyze cycle drawn as a loop with the four-tier assay cascade on the right; potency → ADMET/off-target → kinetics/tolerance → in vivo efficacy, funnelling to ~1% preclinical candidates, with both positive and negative readouts fed back into design | schematic | `SCHEMATIC \| DMTA loop (design → make → test → analyze) with a 4-tier assay cascade and a feedback arrow carrying positive and negative data back to design \| no data` | 1, unlettered | | No licence statement in PDF — see note below table |
| 2 | p20 | Timeline, 1970–~2025: cumulative PDB entries and cumulative protein–ligand complexes drawn as two curves, overlaid with dated vertical markers for every major dataset, blind challenge and model release | line (2 series) with a dated vertical-annotation layer | `PLOT \| facet: none (1) \| vary: year, 1970–~2025 (continuous) \| series: entry type (2: total PDB entries [green], total protein–ligand complexes [yellow]) \| measure: cumulative count of entries (0–250,000) \| mark: line \| n: 1 curve per series; per panel = the full PDB record, per-year values NOT REPORTED` | 1 panel. Carries a **second, non-measured layer**: ~40 dated vertical markers, colour-coded blue = dataset, orange/red = model, purple = dataset **and** model, `*` = blind challenge, `†` = no longer supported. Named on the plot: PDB, SWISS-Prot, SWISS-Model, ModBase†, CATH, SGC†, BindingDB, UniProt, PDBbind, BindingMOAD†, PubChem, SAMPL\*, CHEMBL, D3R†, CACHE\*, CASP\*, AlphaFold2, Merck KGaA, Schrödinger, OpenFE, AlphaFold3, Boltz-1, Chai-1, ATLAS, MDCATH, PLINDER, BioEmu, Boltz-2, BindingNet, ASAP-Polaris, Runs N' Poses, BigBind, SAIR, PoseBusters | The two curves share a linear 0–250,000 axis, so the protein–ligand curve (the paper's actual subject, <20% of entries) is compressed into the bottom fifth and its shape is unreadable; a second axis or a ratio panel would carry the claim the figure is drawn to support. The marker labels above the plot are dense and unreadable at print size in the 2018–2025 region, which is where the argument lives. No n, no source, no accession date for the PDB counts | No licence statement in PDF |
| 3 | p21 | The task hierarchy: drug-discovery tasks and example systems arranged left→right by increasing complexity, each annotated with a "Model Maturity" level | schematic | `SCHEMATIC \| hierarchical left-to-right task ladder with example systems, annotated by model maturity in three levels (solid = established prospective models; dashed = promising, datasets exist but no clear predictive approach; dotted = out of reach for want of data) \| no data` | 1, unlettered | **The paper's central framework is presented with no quantitative panel of any kind.** The three maturity levels are assigned by author judgement; no criterion, no benchmark score and no threshold separates solid from dashed from dotted, and no citation is attached to individual placements in the caption | No licence statement in PDF |
| 4A-top | p22 (caption continues p23) | Boltz-2 affinity-module discrimination against prospective ligands, one bar per viral family, with a dashed chance line at 0.5 | bar | `PLOT \| facet: none (1) \| vary: viral family target (4: SARS-CoV-2 Mpro, MERS-CoV Mpro, Picornavirus 2APro, Flavivirus NS3-NS2B) \| series: none (1; colour is redundant with vary) \| measure: Boltz-2 ROC AUC against prospective ligands (0.0–1.0, chance line at 0.5) \| mark: bar with error bars \| n: per bar = the target's prospective pIC50 ligand set (1323 / 1373 / 176 / 534, printed in the panel below); 4 bars` | 1 of the 2 stacked sub-panels inside lettered panel A (the other is the row below); shares an x-axis with 4A-bottom | **Error bars are drawn on every bar and never defined** — not in the caption (p22), not in the body (p7 says only "with high error bars"). Whether they are CIs, SD, or bootstrap replicates is unrecoverable from this document, so the Picornavirus-vs-Flavivirus distinction cannot be assessed. **No n printed on this sub-panel itself** (it is in the one below). **The metric floors at 0.5** and one bar sits on the floor, so "how much worse than chance" is unrecoverable — cross-reference `metric_saturation` in section C | No licence statement in PDF; data are ref [67]'s |
| 4A-bottom | p22 | Test-set size per target: how many pIC50 values back each AUC above | bar | `PLOT \| facet: none (1) \| vary: viral family target (4, same as 4A-top) \| series: none (1) \| measure: number of pIC50 values in test set (0–1500) \| mark: bar \| n: 1 aggregate count per bar (1323, 1373, 176, 534); 4 bars` | 1 of the 2 stacked sub-panels inside lettered panel A. **Split from 4A-top on `measure`, per the v3 rule** | The 1323 and 1373 labels are printed **inside** bars that are clipped by the sub-panel's 1500 ceiling, so the two largest values are read from text rather than from the bar length; the y-axis label overlaps the sub-panel above it in the rendered page | No licence statement in PDF |
| 4B | p22 | The memorisation control: PDB entries per target split at the Boltz-2 training cutoff 2023-06-01 | bar (stacked) | `PLOT \| facet: none (1) \| vary: viral family target (4, same as A) \| series: cutoff status (2: before cutoff [retrospective, blue], after cutoff [prospective, orange]) \| measure: total entries in the PDB (0–1750) \| mark: bar (stacked) \| n: 1 count per segment (743/1044, 40/19, 334/594, 423/257); 4 stacked bars` | 1 (lettered panel B). Split from 4A rows on `measure` and on the presence of a `series` | **The MERS-CoV bar (40 + 19 = 59) is visually nil against SARS-CoV-2 (1787) on a shared linear axis** — and MERS is precisely the target the argument turns on ("demonstrating the ability of Boltz-2 to generalize", p7). The comparison the text makes is legible only from the printed numbers, not from the bars. A log axis or a per-target panel would carry it. **No citation on this panel**, so whether the tabulation is new to this piece or taken from ref [67] cannot be told (see `unresolved` item 2); no PDB accession date is given for the counts | No licence statement in PDF |
| 4C | p22 (caption on p23) | The pose failure: Boltz-2's predicted binding modes for ASAP-0016806–001 in ZIKV and in WNV NS3-NS2BPro, overlaid on the ZIKV crystal structure | structure render | `RENDER \| facet: none (1) \| views: 1 (single orientation, surface + cartoon of one receptor) \| overlay: 2 predictions (ZIKV [orange], WNV [yellow]) on 1 reference (ZIKV crystal, PDB 7I9J [blue]) \| axis: none` | 1 (lettered panel C); 3 ligand copies drawn on one receptor surface | **The paper's sharpest empirical claim — "fails to recover the ligand pose, altering key interactions in ZIKV and misidentifying the binding pocket entirely in WNV" (p8) — is supported by a render alone: no RMSD, no LDDT-PLI, no threshold, no second pose, no confidence value.** Two different targets' predictions (ZIKV and WNV) are drawn on a **single** receptor surface, with no WNV experimental reference shown, so the WNV "wrong pocket" verdict is read against the ZIKV structure. The "key interactions" said to be altered are not annotated on the render | No licence statement in PDF; data are ref [67]'s |

**`reuse`, in full — read before reproducing or redrawing anything.** **No licence statement of
any kind appears in this PDF.** Checked: p1 (masthead, footnotes, disclosures), the per-page
footers on all 23 pages, and the figure pages p19–p23. What the document *does* say, p1:
"**HHS Public Access — Author manuscript — Curr Opin Struct Biol. Author manuscript; available
in PMC 2026 April 04**", and "Publisher's Disclaimer: This is a PDF file of an unedited
manuscript that has been accepted for publication… during the production process errors may be
discovered which could affect the content, and all legal disclaimers that apply to the journal
pertain." This is an **NIH Public Access author manuscript of an Elsevier journal article**.
No Creative Commons licence, no CC-BY, no CC-BY-ND, no open-access statement. **Practical
consequence: assume all rights reserved.** Do not reproduce any panel; if Figure 4's content is
wanted, **redraw it from the primary source, ref [67] (bioRxiv 2025.07.29.667267), and check
that preprint's own licence** — bioRxiv preprints usually carry a CC licence and this one is
where the data actually live. There is **no ND clause** to worry about, because there is no
licence at all. Also note the publisher's disclaimer: **this is the unedited accepted
manuscript**, so wording and figure numbering could differ from the final typeset article
(the title already differs between this PDF and `refs.bib`; see section A).

## G. Provenance

- **`extracted_on`**: 2026-09-07
- **`extractor`**: claude subagent (Opus 5), single-paper extraction, schema v3
- **`schema_version`**: **v3**
- **`confidence`**: **high on text, medium on Figure 4's numeric values.**
  - **High** on everything drawn from the body text and the annotated bibliography: the PDF text
    layer is clean apart from the soft-hyphen artifacts noted at the top, all 23 pages extracted,
    and every quote above was taken from the extracted text and page-checked against the
    `===== PAGE n =====` markers.
  - **Medium** on three ROC AUC values (SARS-CoV-2 ≈0.87, MERS ≈0.88, Picornavirus ≈0.69 with a
    ≈0.55–0.83 error bar): these are **read off the p22 render**, not printed as numbers
    anywhere. Only the Flavivirus value (0.50) is stated in text. They are marked as read-from-
    figure in section E and should not be quoted to two decimal places in our manuscript.
  - **Medium** on whether Figure 4B is new to this piece or reproduced from ref [67] — see
    `unresolved` item 2.
  - One `pagetext.sh` warning was emitted and ignored: "Syntax Error (635717): Can't revert non
    decrypt streams". It did not truncate the extraction; all 23 page markers and all four
    figure captions came through.
- **`unresolved`**:
  1. **v3 HAS NO TAG FOR A REVIEW OR PERSPECTIVE, AND NO FIELD FOR RECOMMENDATIONS.** Two
     separate gaps, both hit hard by this paper.
     (a) *Tag.* There is no `review` and no `perspective` tag in the fixed v3 vocabulary. Sibling
     extractors hit this and used **`experimental`** on its literal definition — "marks a paper
     with no structure prediction in it at all, whose section C will be mostly NOT APPLICABLE by
     design rather than by sloppiness" — while flagging the mismatch. **The same was done here**
     rather than inventing a tag. The mismatch is real and should be recorded: the tag's evident
     *intent* is a wet-lab paper (its neighbours in the Method list are all computational
     methods, and its sibling rigour tag is `experimental-validation`), whereas this paper is a
     desk piece that runs neither an experiment nor a prediction. A reverse lookup for
     "experimental papers" will return this perspective and that will be wrong. **Requested:
     add `review` (or `perspective`) to the Publication or Method group.** Until then, filter
     `experimental` + `peer-reviewed` + no `experimental-validation` to find these.
     (b) *Field.* v3 has no home for "recommendations the paper makes". For a perspective this
     is the single most reusable content — it is what our work will be measured against — and
     it is neither a necessity claim (some recommendations are permissive or directional, e.g.
     R11's "balance") nor a stated limit nor a metric. It has been recorded as a clearly-labelled
     **non-schema block in section D**, deliberately not smuggled into `stated_limits`, which is
     the exact v2 failure the changelog (item 12) names. **Requested: a `recommendations` field
     (verbatim + page) in section D, or an explicit instruction that they belong in
     `necessity_claims`.**
  2. **Provenance of Figure 4B is undeterminable from this document.** Panels 4A and 4C cite
     "[67]"; **panel 4B cites nothing**, and the body text introduces its numbers with no
     attribution ("≤100 MERS-CoV MPro structures are deposited, and only 40 are available by
     the cutoff-date", p7–8). It may be a fresh tabulation by these authors — which would make
     this a perspective carrying a small piece of original analysis — or it may be reproduced
     from ref [67]. **Resolving this requires ref [67], which the corpus does not hold.** The
     note is written to be correct either way.
  3. **Error bars in Figure 4A are never defined** — not in the caption, not in the body. CI,
     SD, SEM or bootstrap is unrecoverable. The Picornavirus-vs-Flavivirus contrast, on which
     the "does not extend to more distant viral families" claim partly rests (p7), cannot be
     assessed without it.
  4. **The pose failure in Figure 4C is never quantified.** No RMSD, no LDDT-PLI, no threshold.
     "Misidentifying the binding pocket entirely" (p8) is a strong claim carried by a render.
     This is recorded in `state_metric` as `visual only` and in `hides`, but note that the
     underlying number may well exist in ref [67].
  5. **No licence statement exists in the PDF at all** (checked p1 and every figure page).
     v3's `reuse` asks for "License and, critically, whether it carries an ND clause… Record the
     page the license appears on" — there is no such page. Recorded as "no licence statement;
     NIH/HHS Public Access author manuscript of an Elsevier article; assume all rights
     reserved". **v3 should say what to write when a licence is simply absent**, since that is
     the common case for PMC author manuscripts and it is materially different from an explicit
     restrictive licence.
  6. **Title discrepancy between the PDF and `refs.bib`**: "More Protein-Ligand data **is**
     needed…" (p1) vs "More protein-ligand data **are** needed…" (`refs.bib`, and the task
     assignment). This PDF is the unedited accepted manuscript per the p1 publisher's
     disclaimer, so the typeset version may differ. Not resolvable without the final article.
  7. **Section C has no idiom for "this is not a study".** Writing `NOT APPLICABLE` seven times
     is correct per the field rules but produces a section that reads as a defect list. This
     note handles it with a standing header at the top of C plus a reason on every field, and
     records the three fields (`metric_saturation`, `anti_memorization_design`,
     `anti_memorization_control`) that do carry real, attributed content so they are not lost in
     the NOT APPLICABLEs. **v3 might consider a `paper_type` field in section A** — it would let
     the index know in one token that section C is empty by construction, which is currently
     only recoverable by reading the prose.
  8. **Figure 2's annotation layer has no home in the `data_shape` grammar.** The figure is a
     two-series line PLOT *plus* ~40 dated categorical event markers with a four-way colour
     encoding and two symbol encodings (`*` blind challenge, `†` unsupported). The markers are
     not a `series` (they do not share the measure), not a `facet`, and not a separate panel
     group (they have no mark of their own and no measure). They are recorded in `panels` as
     prose, which is unjoinable. **A PLOT-level `annotation:` slot would fix this**, and
     timeline figures are common enough in review-family papers to warrant it.
  9. **`stance` for a framing citation from a plausible-reviewer group** is genuinely awkward in
     the four-value vocabulary. `background` understates the operational force of R1–R13;
     `contrast` overstates it, since the piece competes with nothing we do; `threat` is plainly
     wrong. Recorded as `background + contrast` and flagged provisional, but the honest answer
     is closer to "the standard we will be held to", which the vocabulary cannot say.
  10. **`n` in the PLOT grammar has no clean form for a bar whose height *is* the count.** For
      4A-bottom the mark is a count and the "n behind the mark" question is circular; written as
      "1 aggregate count per bar" with the values listed. Minor, but it will recur for every
      histogram-like bar panel.
- **`why_it_matters`**: *(left empty by instruction — the user's call)*

## Tags

`general-protein` `experimental` `continuous-metric` `visual-metric` `saturating-metric`
`prospective` `anti-memorization` `unpowered` `design-level-oracle` `peer-reviewed`
`background` `contrast` `negative-result` `comparator-numbers`

**Scoping notes on the tags that are true but narrower than they look. Read these before using
this note in a reverse lookup.**

- **`experimental` — APPLIED ON ITS LITERAL DEFINITION, WITH THE MISMATCH FLAGGED.** v3 defines
  it as marking "a paper with no structure prediction in it at all, whose section C will be
  mostly NOT APPLICABLE by design rather than by sloppiness". That is exactly true here: no
  structure prediction is run, and section C is NOT APPLICABLE by design. But the tag's evident
  intent is a **wet-lab** paper, and this is a desk perspective with no bench work either.
  **v3 has no `review` or `perspective` tag; one was not invented.** See `unresolved` item 1(a).
  Do not read this tag as "they did experiments" — they did not.
- **`continuous-metric`, `visual-metric`, `saturating-metric` — all three describe Figure 4,
  which is a re-presentation of ref [67], not a measurement by these authors.** `continuous-metric`
  = ROC AUC (p7, p22). `visual-metric` = the pose verdict in 4C, called from a render with no
  RMSD (p8, p23) — a genuine rigour defect as it appears *in this document*, whatever ref [67]
  reports. `saturating-metric` = ROC AUC floored at 0.5, with the Flavivirus bar exactly on the
  floor (p7). All three are tagged so a metric-rigour reverse lookup finds this figure; none is
  a statement about a pipeline these authors built.
- **`prospective`, `anti-memorization`, `unpowered` — the same caveat, and they travel
  together.** The Figure 4 affinity arm is prospective by construction (post-2023-06-01 ligands,
  axis label p22) and the temporal split is not just declared but *analysed* against performance
  (p8) — a real anti-memorization control, and a better one than most papers in this corpus
  manage. `unpowered` applies **at the target level only: n = 4 viral families, and n = 2
  targets / 1 ligand for the pose arm**. The per-target ligand counts (176–1373) are ample.
  Use the right number; all of them are in `n_predictions`.
- **`design-level-oracle` — route 7, weak form, and it partly *fails*.** The four families were
  chosen for their known data situations and the expected answer was stated before the result
  ("the expected ability", p7). But the headline finding contradicts the expectation
  (Picornavirus and Flavivirus have ~10× MERS's structures and do worse, p8). Tagged so a
  route-7 lookup finds it; a reader who takes this as "the result was rigged" has misread it.
  **`oracle-leak` is deliberately NOT tagged** — nothing leaky entered any pipeline here.
- **`background` + `contrast`** — both, provisionally; see `stance` in section D.
- **`comparator-numbers`** — tagged, but note that **almost every number in section E is
  somebody else's**, and the two most citable (Figure 4's AUCs and the >5-structures
  diminishing-returns result) live in preprints the corpus does not hold. Cite the primary
  source, not this piece. See `si_in_scope`.

**Tags considered and rejected, with reasons, so the decision is auditable:**

- **`benchmark-only`** — rejected. The piece is *about* benchmarking and criticises named
  benchmarks at length (p4, p7, p13), but it **runs no benchmark**. Tagging it would return this
  perspective in every "which papers benchmarked X" query alongside papers that actually did.
  If the corpus later wants "papers that argue about benchmarking", that needs its own tag.
- **`cofolding`** — rejected. Co-folding models (Boltz-2, Chai-1, AF3) are the *subject*, but
  none is run here. Same false-positive argument.
- **`multi-backbone`** — rejected. Many backbones are named; **none is compared head to head by
  these authors**. Only Boltz-2 is evaluated, in a re-presented figure.
- **`kinase`** — rejected despite Abl appearing repeatedly (p5, p6, p11, p17). Every kinase
  statement is a citation of refs [11] and [64]; no kinase result is presented here. Tagging it
  would false-positive a kinase reverse lookup.
- **`preprint`** — rejected; this is the peer-reviewed Current Opinion article (vol 98, 103257),
  distributed as a PMC author manuscript. The *author-manuscript* format is not preprint status.
- **`rmsd-only`** — rejected. No RMSD is computed anywhere in this document. The only Å figure
  is quoted from ref [5] (2 Å pose success, p6).
- **`msa-subsample`** — rejected. MSA subsampling appears once, as a characterisation of ref
  [54] (p15), and nothing is subsampled here.
- **`experimental-validation`** — rejected. Nothing is validated in a lab by these authors. The
  NanoBRET work advocated on p5 belongs to refs [11] and [64].
- **`single-state` / `two-state` / `ensemble` / `continuum`** — all rejected. No states are
  generated; see `states_generated`.
- **`orthosteric` / `allosteric-site` / `cryptic-pocket` / `allosteric-failure`** — rejected.
  Figure 4C concerns a protease active site but the piece studies no site; "allosteric
  mutations" appears once (p5) as a characterisation of ref [11]'s finding.
- **`no-template-no-msa` / `templates-on` / `state-annotated-input`** — rejected. No input
  regime is configured; see `templates` and `msa_handling`.
- **`precedent`** — rejected as a stance. The piece establishes no methodological precedent; its
  framework is offered as descriptive (p3) and it introduces no technique.
- **`threat`** — rejected. Nothing here pre-empts or contradicts a conformational-states methods
  contribution.
- **`figure-exemplar`** — rejected. Figure 2's timeline is an attractive object and Figure 3 is a
  clean hierarchy, but neither is a design worth copying for quantitative data (Fig 2's shared
  linear axis buries its own subject; Fig 3 carries no data at all), and the licence forbids
  reproduction anyway.
