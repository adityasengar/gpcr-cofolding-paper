# heo2022multistate

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–13).** The journal
pagination runs 1873–1885, so PDF page n = journal page 1872+n. Mapping, because quotes
below use PDF pages: p1=1873 (abstract, intro), p2=1874, p3=1875, p4=1876 (Figure 1),
p5=1877 (Figure 2), p6=1878 (Figure 3), p7=1879, p8=1880 (Figure 4), p9=1881 (Figure 5,
Conclusions, Methods 4.1), p10=1882 (Methods 4.2–4.4), p11=1883 (Methods 4.5–4.6),
p12–13 = references.

**Text-layer caveat:** superscript GPCRdb residue numbering is flattened into the baseline
text, so the paper's `W6×48` appears as `W648`, `P5×50` as `P550`, `N7×49` as `N749`, and
`8.2 × 10⁻⁸` appears as `8.2  108`. Verbatim quotes reproduce the text layer; the rendered
pages 4, 6 and 8 confirm the intended superscripts. The rendered p4 confirms
`8.2 × 10⁻⁸` and the p8 render confirms `W358⁶ˣ⁴⁸`.

**Supplement caveat, recorded up front:** the substantive ablation, per-class and per-target
results live in Figures S1–S15, Tables S1–S3 and Algorithm S1, none of which are in the held
PDF. See `si_in_scope`.

---

## A. Identity

- **citekey**: `heo2022multistate`
- **doi**: **10.1002/prot.26382** — p1 masthead: "DOI: 10.1002/prot.26382". Matches `refs.bib`.
- **year**: **2022.** p1: "Received: 6 January 2022 | Revised: 7 April 2022 | Accepted:
  26 April 2022"; p13 citation block: "Proteins. 2022;90(11):1873‐1885".
- **venue**: **Proteins: Structure, Function, and Bioinformatics, Wiley — peer-reviewed
  research article, not a preprint.** p1: "RESEARCH ARTICLE"; p1 footer: "© 2022 The Authors.
  Proteins: Structure, Function, and Bioinformatics published by Wiley Periodicals LLC.";
  p12: "The peer review history for this article is available at
  https://publons.com/publon/10.1002/prot.26382." Tag `peer-reviewed`, not `preprint`.
- **title**: Multi-state modeling of G-protein coupled receptors at experimental accuracy — p1
- **authors**: Lim Heo and Michael Feig (corresponding, mfeiglab@gmail.com), Department of
  Biochemistry and Molecular Biology, Michigan State University — p1. Two authors only.

## B. Scope

- **system**: **GPCR**, exclusively. Class A, B1, B2, C and F human receptors (p4). p1:
  "The family of G-protein coupled receptors (GPCRs) is one of the largest protein families
  in the human genome." Generalisation to other families is asserted but not run — p9:
  "The multi-state modeling approach introduced here can be extended in principle to other
  protein families such as kinases as long as experimental structures in multiple states are
  available to form state-specific template databases."
- **n_targets**: several nested counts; do not collapse them.
  - **68** post-cutoff human GPCRs in the benchmark set — p10: "There were 68 GPCRs in the
    set, and they are summarized in Table S2."
  - **49 active / 30 inactive** reference states within that set — p10: "Among them, there
    were 49 and 30 GPCRs for the active and inactive states".
  - **15** GPCRs solved in *both* states — p10: "and 15 GPCRs were determined in both active
    and inactive states". This 15 is the multi-state discrimination denominator (10/15 correct).
  - **All human non-olfactory GPCRs** modelled in both states for the deposited database —
    p10: "All human non-olfactory GPCRs were modeled as active and inactive state structures.
    The list of the GPCRs was retrieved from GPCRdb." The structure-less subset is **289** per
    the Figure 3 percentages (p5: "209 out of 289"). The universe is 401 — p2: "Known
    structures comprise only 112 out of 401 human non-olfactory receptors."
  - **Docking subset**: **45 protein–ligand complexes across 19 receptors** (28 active, 17
    inactive) — **RESOLVED 2026-09-10** from the bioRxiv v2 SI, Table S3; extracted to
    `../panels/si_tables/heo2022multistate_tableS3_docking.csv` with PDB id and ligand CCD.
  - **1** target for intermediate-state sampling (AT1/AGTR1, p6); **5** GPCR Dock 2021
    targets of which 2 had structures released (p8).
- **method_class**: **template-biasing**, with a secondary MSA-ablation component that is not
  MSA-subsampling. The state handle is a state-annotated template database substituted for
  PDB70; the enabling condition is total removal of the MSA. p9 (Conclusions): "AF2 was used
  with activation state-annotated GPCR structure databases instead of a general PDB structure
  database and without MSA input features to avoid learned biases towards inactive GPCR
  states." A shallow-MSA arm (Del Alamo protocol) is reproduced as a *comparator*, not as the
  method (p7, p11).
- **backbones**: **AF2** as the method. **RoseTTAFold** re-run by the authors as a comparator
  (p5: "we ran RoseTTAFold according to its multi-state modeling protocol with the same
  templates that we used for our protocol"), **MODELLER** for template-based modelling (p10),
  **AlphaFold-Multimer** for the peptide-ligand stage of GPCR Dock (p11), and **GPCRdb**
  homology models retrieved from a 2018 archive (p5). No AF3, Boltz, Chai, OF3 or Protenix
  (2022 paper). AF2 vs RoseTTAFold is a head-to-head of two prediction backbones on the same
  templates — **tag `multi-backbone`** on that arm; MODELLER and GPCRdb are homology-modelling
  comparators, not learned backbones.
- **templates**: **state-annotated** (this is the whole method), with **on / off / PDB70**
  arms in the ablation. p9–10: "Protein structure prediction for a state was guided by the
  input database for the state, as a replacement of the PDB70 database." Database sizes,
  p10: "As of July 29, 2021, there were 224 and 309 experimentally determined structures for
  active and inactive state structures, respectively. And, they resulted in 161 and 206 unique
  entries for the activation state-annotated GPCR structure databases after removing proteins
  with identical sequences." Intermediate-state arm replaces templates with artificial
  interpolated models (p10).
- **msa_handling**: **dual — full, and removed entirely; plus a third, distinct
  state-directed gapping variant.** All three are in the paper and they are different things.
  1. **Full** MSA, in the original-AF2 baseline and in the "annotated DB + MSA" arm (p3).
  2. **Removed entirely** in the final protocol — p3: "when MSA input features were removed
     and state-annotated GPCR databases were used, it became possible to generate highly
     accurate models for both active and inactive state structures of GPCRs". p6: "None of
     the sequences in the MSA was used except for the target protein sequence."
  3. **State-filtered by template-guided gapping**, the second of two ways the annotated
     databases were used — p10: "In another approach, residues in the input MSAs were
     modified to gaps for sequence positions which were aligned to selected structure
     templates from the activation state-annotated databases. (Algorithm S1)" This is a
     state-directed edit of the alignment, not a depth reduction. Its standalone result is in
     Figures S2–S4/S6, not in the held PDF; which of variants 2 and 3 constitutes the released
     protocol is **not stated unambiguously in the text** — see `unresolved`.
  4. **Subsampled** appears only in the reproduced Del Alamo comparator — p11: "we used
     16, 32, 64, and 128 for max_extra_msa and set max_msa_cluster to half of the value."

## C. Conformational core

- **states_generated**: **two (one per operator-selected run) + ensemble in a side arm.**
  The protocol is run twice per receptor, once per state, and each run yields five AF2 models
  that are the same state; the two states come from two different template databases, not from
  one sampling process. p9: "A database was built for each active or inactive state."
  The intermediate arm produces a swept series — p6: "Input models at different points along
  the interpolation were used to sample various conformations between the active and inactive
  states" (21 input models, p10–11) — but p6–7 reports the output as **discontinuous**, not a
  continuum: "While the input models had continuous structures between the active and inactive
  models, the output models showed discontinuous structural transitions (Figure S11A,B)."
  Original AF2 alone is **single-state**: p3: "AF2 only modeled either the active or inactive
  state for a given GPCR sequence, though, not both."

- **structural_priors_used**: **Extensive, at design time, and largely legitimate as design
  rather than leakage.** Kept separate from `oracle_leakage` per v3.
  1. **The entire GPCRdb corpus of state-labelled deposited GPCR structures is the method's
     raw material.** p10: "Template structure databases for each active and inactive state
     GPCRs were built based on the GPCRdb activation state annotation." 224 active + 309
     inactive structures → 161 + 206 unique entries (p10).
  2. **Benchmark systems were chosen because both states are deposited.** p10: "15 GPCRs were
     determined in both active and inactive states." The paper's own framing of the field-wide
     scarcity, p2: "only 74 and 65 GPCRs were determined in active and inactive states,
     respectively, and only 36 GPCRs have experimental structures in both activation states."
  3. **The TM-helix definition used for every RMSD is taken from a curated structural
     database**, p10: "the Cα-RMSD was evaluated using transmembrane helices, whose definition
     was taken from the GPCRdb."
  4. **A prior MD free-energy surface is used as the reference landscape for the intermediate
     models**, p7: "The output models were further validated by mapping the structure onto a
     potential of mean force (PMF) map generated by a previous MD simulation study."
  5. **Known activation-mechanism motifs from the structural literature** (PIF, NPxxY, DRY,
     W6×48) are the assessment axes in Figure 2 (p4–5).
  6. **PDB accessions are given for the worked examples**: 6lfo_R / 6lfl_A (CXCR2, p4),
     7e2y / 7E2Y (5-HT1A serotonin complex, p7–8), 7vgx_R / 7vgx_L / 5zbh_A (NPY1R, p8).

- **oracle_leakage**: **PRESENT and structural to the method. Routes 1, 2, 4, 5 and 7 are all
  live; route 6 is partial; route 3 is absent.** This paper is the canonical template-biasing
  baseline, so each route is enumerated in full.

  **Route 1 — deposited structures used as input or template: PRESENT, and it is the
  mechanism.** Deposited GPCR structures of the *target state* are the sole informative input
  once the MSA is discarded.
  - p9–10 (Methods 4.1): "In addition, we intended to guide AF2 to model a specific activation
    state structure using activation state-annotated GPCR structure databases. A database was
    built for each active or inactive state. ... Protein structure prediction for a state was
    guided by the input database for the state, as a replacement of the PDB70 database."
  - p6: "The structural template dependence was introduced here because information from
    structural templates was one of the most important input features for our protocol as MSA
    information was discarded."
  - **Same-receptor templates WERE excluded; same-state templates of other receptors were
    not — that exclusion is the whole point of the method.** p10: "For the benchmark test,
    close homologous structures that have a sequence identity higher than a cutoff of 70% were
    excluded from the template lists." A 70% sequence-identity cutoff removes the target
    receptor's own deposited structures (100% identity) and its close orthologues/paralogues,
    so the model is not shown a structure of the receptor it is predicting. It does **not**
    remove structures of *other* receptors in the requested state — those remain and are the
    signal that carries the state. The residual accuracy is therefore homology-driven, which
    the authors state plainly, p3: "the activation state-annotated structural template
    databases could be used to guide the AF2 modeling network towards a specific activation
    state based on homology". Consistent with that, accuracy tracks template identity, p6:
    "We observed that modeling with an active state template that has a sequence identity
    higher than 20% usually resulted in a high quality model".
  - **Additional route-1 instances outside the benchmark:**
    (a) The intermediate-conformation arm feeds structures derived from its own predicted
    active/inactive endpoints as templates — p10: "Rather than searching structural templates
    against activation state-annotated GPCR databases, artificial input templates were
    generated and were fed to the AF2 network model."
    (b) The GPCR Dock peptide stage feeds a predicted receptor as a template into
    AlphaFold-Multimer — p11: "The modification enabled AlphaFold-Multimer model to take any
    structure as a template rather than performing template search so that we could feed the
    predicted GPCR structures as input."
    (c) **The docking evaluation places the search box using the experimental complex** —
    p11: "For an experimental protein structure, the center of the cubic search space of
    docking was located at the geometrical center of the ligand from its bound structure ...
    For predicted GPCR structures, the same search space was used after superimposition to the
    experimental structure." The flexible sidechains are likewise chosen from the experimental
    contact set — p11: "The binding site residues were defined as residues whose atoms were
    within 8 Å from the ligand in the experimental structure." The 70% template filter does not
    protect this arm; the docking numbers are oracle-boxed.
  - **The 70% cutoff is stated only "For the benchmark test."** Whether it was applied to the
    whole-proteome run or the GPCR Dock predictions is not stated — see `unresolved`.

  **Route 2 — state annotations from a curated database driving templates or alignments:
  PRESENT, and this is the second half of the mechanism.** The state labels are not inferred;
  they are read from GPCRdb.
  - p10 (Methods 4.2, "Building activation state-annotated GPCR structure databases"):
    "Template structure databases for each active and inactive state GPCRs were built based on
    the GPCRdb activation state annotation. ... A list of PDB IDs was collected from the GPCRdb
    for either active or inactive states."
  - GPCRdb also picks the chain: p10: "If there were multiple chains of GPCRs for a PDB entry,
    a preferred chain selected by the GPCRdb was used."
  - The abstract states the dependence outright, p1: "a multi-state prediction protocol is
    introduced that extends AlphaFold2 to predict either active or inactive states at very high
    accuracy using state-annotated templated GPCR databases."
  - The database *replaces* the generic one at search time, p3: "Activation state-annotated
    GPCR databases could be simply used instead of the standard template database, PDB70, to
    model GPCRs in a desired functional state."
  - The same curated annotation also feeds route 2 into the *alignment*, in variant 3 of
    `msa_handling`: p10: "residues in the input MSAs were modified to gaps for sequence
    positions which were aligned to selected structure templates from the activation
    state-annotated databases."
  - And into the *metric*: TM helix boundaries come from GPCRdb (p10).

  **Route 3 — cluster labels derived from known states: NONE FOUND.** The only clustering in
  the paper is redundancy removal at 100% identity, which carries no state information —
  p10: "To remove redundant sequences, the extracted sequences were clustered by MMseqs2 with
  a sequence identity cutoff of 100% and a sequence coverage of 100%." Protocol page for
  checkability: p10 (Methods 4.2). No AF-Cluster-style MSA clustering anywhere.

  **Route 4 — hyperparameters, sweeps or stopping criteria tuned against known states:
  PRESENT, twice.**
  (a) **The protocol configuration itself was chosen on the evaluation set.** Four input
  configurations were run against the benchmark of receptors with known structures, and the
  winning one — annotated DB with the MSA removed — was selected because it reproduced both
  known states. p10: "an ablation study was performed to better understand the role of each
  input feature. The original AF2 method was compared with three variants: one without MSAs,
  one without structure templates, and one without both MSAs and structure templates."
  p3: "when MSA input features were removed and state-annotated GPCR databases were used, it
  became possible to generate highly accurate models for both active and inactive state
  structures of GPCRs (Figure 1 and Figures S1–S3 and S6)." The negative half is stated with
  equal clarity, p3: "using such curated template databases was not sufficient to make
  meaningful changes."
  (b) **Two confidence/identity selection criteria were fitted on the benchmark's known
  structures and then applied to receptors with no structures.** p6 (Figure 3 caption):
  "A model that has a pLDDT higher than 90 or is predicted using a template with a sequence
  identity of more than 20% was likely to be accurate (TM-RMSD < 1.5 Å)." These thresholds are
  read off the same TM-RMSD-vs-predictor scatter they are then used to summarise (p5–p6), and
  the paper explicitly relaxes the literature identity threshold on the strength of its own
  benchmark: p6: "the sequence identity criteria may be lowered because the AF2 network can
  model accurately even with approximate information."
  (c) A weaker instance in the docking arm: the flexible-sidechain setting was adopted because
  the rigid setting scored worse on the same evaluation — p7: "Two sidechains at the binding
  site were set to be flexible ... Otherwise, the success ratios dropped significantly for them
  because misoriented sidechains prevented a ligand from docking (Figure S14)."

  **Route 5 — success defined post hoc by RMSD/TM to a structure they held: PRESENT, and it is
  the paper's only definition of success.** There is no prediction-time state predicate.
  - State correctness: p3–p4: "for 10 targets among the 15 multi-state GPCRs, our protocol
    successfully modeled the correct activation states based on the active state model being
    closer to the active state experimental structures than to the inactive experimental
    structure and vice versa for the inactive state model."
  - Multi-state capability of baseline AF2, same construction: p10: "The ability of being able
    to model multiple states was judged based on some of the five models being closer to active
    state than inactive state while others were closer to the other state."
  - "High accuracy" threshold: p3: "17 out of 30 models predicted at high-accuracy (i.e.,
    <1.5 Å TM-RMSD".
  - Docking success threshold: p10: "A docking simulation was considered successful if the
    ligand heavy-atom RMSD was lower than 3 Å."

  **Route 6 — best/worst model labels assigned against a held reference: PARTIAL.**
  Model *ranking* is by AF2's own confidence, not by the reference — p3 discusses "the
  top-ranked model" and "the fifth-ranked model" for PTH1R, and Figure 4/Table analyses use
  "top 1" and "top 3" (p8 caption). But the **reference itself is oracle-selected as the
  closest of several**: p10: "If there were multiple experimental structures for an activation
  state of a GPCR, the closest result was reported." That is a best-of-references choice made
  against the model, which biases every reported RMSD downward by an unstated amount.

  **Route 7 — design-level oracle use (input conditions or systems chosen because the expected
  answer is known): PRESENT. Label as design-level, weaker than the pipeline leakage above.**
  - The operator declares the state before the run, for every prediction in the paper; the
    benchmark is scored by whether the declared state came out. The systems are exactly those
    with both states deposited (p10, 15 GPCRs).
  - In the blind competition the state was **supplied by the organisers**, not predicted —
    p11: "The activation state of target GPCRs were determined based on the given information
    of G-protein binding." p8 confirms it was given: "Five GPCR-ligand complexes were given as
    targets with activation state information."
  - The docking arm docks each ligand to "multi-state models in the corresponding activation
    states that of the experimental structures" (p11) — i.e. the correct state is assigned from
    the answer before docking.

- **prospective**: **partial, and the two halves point opposite ways.**
  - *Prospective in target selection and in memorisation terms*: the whole benchmark
    post-dates AF2's training cutoff — p10: "The set was composed of human GPCRs that were
    experimentally first determined after May 01, 2018 and before January 05, 2022. Since AF2
    was trained protein structures determined by April 30, 2018, thus, none of the GPCR
    structures that were used for the training were included in the benchmark set."
  - *Prospective in one genuinely blind arm*: GPCR Dock 2021, p8: "As another blind test of
    application of our multi-state modeling, we participated in GPCR Dock 2021." Structures for
    two of five targets were released afterwards (p8).
  - *Retrospective in the biasing pipeline*: the template databases were assembled on
    2021-07-29 from all GPCRdb structures (p10), which is *inside* the benchmark's
    2018–2022 window. Contemporaneous structures of related receptors in the target state are
    therefore in the template set even though the target's own are filtered at 70% identity.
    The state is chosen by the operator, and success is defined by RMSD to a held structure.
  - **Net: not prospective as a state-prediction method; prospective only as an
    accuracy-under-a-given-state demonstration.**

- **state_metric**: **RMSD-to-reference + binary predicate derived from it. There is no
  geometric state criterion anywhere in this paper — no TM6 distance, no NPxxY/DRY ionic-lock
  measurement used as a decision rule.**
  - *Continuous measure*: Cα TM-RMSD to the state reference. p10: "the Cα-RMSD was evaluated
    using transmembrane helices, whose definition was taken from the GPCRdb."
  - *Binary predicate*: **relative**, not absolute — a model is "in" the state whose reference
    it is nearer to. p3–4: "based on the active state model being closer to the active state
    experimental structures than to the inactive experimental structure and vice versa for the
    inactive state model." **No numeric threshold is used for state assignment**; the predicate
    is `RMSD_active < RMSD_inactive`, which requires that both references exist, and this is
    why the state-discrimination denominator is 15, not 68.
  - *Separate accuracy threshold*, which is not a state call: **1.5 Å TM-RMSD**. It is used
    throughout (p3, p5, p6) and the paper gives **no justification for the value** —
    `NOT REPORTED` for its derivation. The only threshold that is justified is the template
    identity cutoff, by citation to prior GPCR homology-modelling practice, p6: "GPCR models
    predicted using templates with sequence identities higher than 20%–40% were assumed to be
    confident.24,33,34"
  - *Docking threshold*: 3 Å ligand heavy-atom RMSD (p10), unjustified in the text.
  - *Visual*: Figures 1B–C, 2 and 5 argue mechanistic correctness by superposition and red
    arrows with no operationalised predicate — e.g. p4: "structural changes of TM6 on the
    intracellular side, which enables G-protein binding, was described very accurately."
    TM6 is discussed qualitatively; it is never measured.

- **metric_saturation**: **Yes, in the docking arm, and it is acknowledged.** The docking
  success ratio is bounded by the experimental-structure control, which itself does not reach
  100%: p7: "ligand docking to active state conformations is intrinsically a difficult problem
  considering that self-docking to less than half of the experimental structures was
  successful"; p8: "with around 30% success, but overall, they were less than 80% success when
  docking to experimental structures." The models' ~1/3 active-state success must be read
  against a <50% ceiling, and the paper says so — p9: "reaching almost the same success rate as
  with experimental structures." **TM-RMSD does not saturate**; the <1.5 Å binary counts
  compress the top of the range but the continuous median is always reported alongside.
  Axis truncation in Figure 1A is a figure defect and is recorded in that row's `hides`, not
  here.

- **directional_control**: **YES — full operator-directed state selection. This is the field
  that makes the paper a baseline. The handle is the choice of which state-annotated template
  database to hand AF2, and it works only once the MSA is deleted.**
  - The handle, stated as a substitution: p9–10: "Protein structure prediction for a state was
    guided by the input database for the state, as a replacement of the PDB70 database."
  - The intent, stated as intent: p9: "we intended to guide AF2 to model a specific activation
    state structure using activation state-annotated GPCR structure databases."
  - The mechanism and its precondition, in one sentence, p3: "In this manner, the activation
    state-annotated structural template databases could be used to guide the AF2 modeling
    network towards a specific activation state based on homology, but without interference
    from MSA-based contacts that are still biased by conformational state preferences according
    to training."
  - **The template handle alone is not sufficient — this is the paper's most important
    negative result and the reason MSA deletion is part of the handle.** p3: "However, using
    such curated template databases was not sufficient to make meaningful changes.
    (Figures S2–S4) For all the multi-state GPCRs, there was little change from the result with
    the standard template database. This suggests that simply using templates according to a
    conformational state as input to AF2 has little impact when deep MSAs were provided as
    inputs."
  - Conclusions restate the two-part handle, p9: "A modified protocol is described here that
    can guide AF2-based high-accuracy modeling towards a specific activation state. In this
    multi-state modeling protocol, AF2 was used with activation state-annotated GPCR structure
    databases instead of a general PDB structure database and without MSA input features to
    avoid learned biases towards inactive GPCR states."
  - **Not a handle here:** ligand, nanobody, G-protein and arrestin are never used as inputs;
    the models are apo — p7: "computational model structures were predicted without
    consideration of binding ligands and resulted in apo structures." Seeds/network parameters
    vary the five outputs but do not select state (p3, Figure S5).
  - A **second, weaker handle** exists in the intermediate arm: the degree of activation `d`,
    swept 0–100% in 5% steps over interpolated input templates (p10–11, Equation 1). It is a
    directed coordinate but the outputs snap to basins (p6–7), so it does not deliver
    controllable intermediates.

- **input_factor_design**: **New in v3.2. CONFOUNDED by construction — the method IS two factors changed together.** **MSA**: total deletion. **templates**: state-annotated GPCRdb templates, on. **ligand**: not an input (AF2 lineage). **partner**: not an input. <br>`crossings:` **templates x MSA CONFOUNDED.** The protocol is state-annotated templates *plus* total MSA deletion applied together, so the paper cannot say whether the template or the alignment removal produced the state control. That is not a criticism of its result, which is strong, but it bounds what can be attributed. Note `chiesa2025templatebias` later beats this protocol with a partner co-input on the large rearrangements.
- **anti_memorization_design**: **PRESENT and explicit — a post-cutoff benchmark set, n = 68.**
  p10: "The set was composed of human GPCRs that were experimentally first determined after
  May 01, 2018 and before January 05, 2022. Since AF25 was trained protein structures
  determined by April 30, 2018, thus, none of the GPCR structures that were used for the
  training were included in the benchmark set. There were 68 GPCRs in the set". The cutoff is
  defined by AF2's published training-set date (30 April 2018) with a one-day margin, and the
  criterion is date of *first* experimental determination of that receptor, which is stricter
  than per-structure date. Note the deliberate use of the training set as an *explanation* for
  the baseline bias, p3: "This bias may originate from the larger number of experimental GPCR
  structures in inactive states (178) than active states (60) that were available for
  training."
- **anti_memorization_control**: **RUN, in the sense that every headline number is measured on
  the post-cutoff set — but no pre-cutoff-versus-post-cutoff contrast arm was ever run, and the
  template side is not held out.** Three qualifications, all load-bearing:
  1. There is **no paired arm** on pre-cutoff receptors, so the size of any memorisation effect
     is never estimated; the design removes the confound rather than measuring it.
  2. **The templates are not date-filtered.** The state-annotated databases were built
     "As of July 29, 2021" (p10) from all GPCRdb entries, i.e. from inside the benchmark
     window. Only sequence identity (>70%) excludes structures, not date. So the *model* never
     saw the target during training, but the *pipeline* is handed contemporaneous structures of
     related receptors in the target state — by design.
  3. The one incidental observation that a reference *was* in training is reported as a
     comparator's advantage, not analysed: p8: "AF2 predicted the inactive structure with a
     TM-RMSD of 0.93 Å with respect to an experimental structure in the inactive state (PDB ID:
     5zbh_A), which was included in the AF2 training set".
  Not `UNPOWERED`: n = 68 receptors, 49 active + 30 inactive states, well above the ~10 bar.

- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Original AF2 (full MSA + PDB70) on the same 68 receptors | that the multi-state gain is just AF2 being good | p3 |
| Template-based modelling with MODELLER using the **identical** templates and alignments | that the gain comes from the templates rather than from the AF2 network | p3, p10 ("template-based modeling using MODELLER with the identical structure templates and the sequence alignments used for the AF2 predictions") |
| Ablation: AF2 without MSAs (PDB70 templates only) | isolates the MSA's contribution — 1.84 Å vs 1.49 Å | p3 |
| Ablation: AF2 without templates (MSA only) | isolates the template contribution — 1.55 Å, "little loss in accuracy" | p3 |
| Ablation: AF2 without both MSAs and templates | floor arm for the input-feature study (result in Figures S1–S3, not held) | p10 |
| State-annotated DB **with** the MSA retained | the key negative control: shows the template handle alone does nothing | p3 |
| Post-cutoff benchmark (first determined after 2018-05-01) | memorisation of the target's own structure from AF2 training | p10 |
| >70% sequence-identity template exclusion | that the model is simply copying the target receptor's own deposited structure | p10 |
| RoseTTAFold multi-state protocol run **with the same templates** | that the result is specific to the template set rather than to AF2 | p5 |
| GPCRdb homology models from a 2018 archive | that AF2-based modelling beats existing GPCR-specific homology modelling | p5 |
| Docking to the **experimental** structures | establishes the achievable docking ceiling (<50% active, <80% inactive) | p7–p8 |
| Rigid- vs flexible-sidechain docking | that docking failure is a backbone/state error rather than a rotamer error | p7 (Figure S14) |
| Shallow-MSA subsampling (Del Alamo protocol) run on the same targets | that the interpolation protocol is merely reproducing MSA-depth sampling | p7, p11 |
| Intermediate models mapped onto a published MD PMF surface | that the interpolated intermediates are physically meaningless | p7 (Figure S11D) |
| Blind arm: GPCR Dock 2021, structures unavailable at prediction time | retrospective tuning on the two released targets | p8, p11 |
| Class-stratified analysis (A, B1, B2, C, F) | that the gain is driven by one over-represented class | p4 (Table S1, not held) |
| Loop-region (3 ICL + 3 ECL) accuracy analysis | that TM-only RMSD hides failure elsewhere in the fold | p4 (Figure S8, not held) |

- **confidence_as_discriminator**: **Used as an accuracy predictor, validated retrospectively;
  explicitly found NOT to work as a state discriminator for baseline AF2.** This distinction is
  unusually clean and worth quoting both halves.
  - *As accuracy predictor, validated*: p5: "There was a clear relationship between the
    accuracy and the pLDDT as presented in Jumper et al. For a model that had a pLDDT higher
    than 90, it was likely to be accurate; 83% (29 out of 35) and 74% (14 out of 19) of the
    active and inactive state models had less than 1.5 Å in TM-RMSD, respectively."
    Validation is against TM-RMSD on the benchmark, with Pearson r shown in Figure 3
    (r = −0.61 active / −0.29 inactive for pLDDT; r = −0.58 / −0.27 for template identity;
    read from the rendered p6, not stated in the text).
  - *As state discriminator, negative*: p6: "the pLDDT for models by original AF2 was less
    informative for the simultaneous assessment of multiple states. (Figure S10) Presumably
    this is because these models were similar to one of the states but not the other one."
  - It is then **used prospectively to triage the structure-less proteome**: p5: "72% (209 out
    of 289) and 64% (189 out of 289) of the active and inactive models are expected to be
    accurate as they had predicted pLDDTs higher than 90." That transfer rests on a threshold
    fitted on the benchmark (route 4b).
  - pTM and ipTM are never used. Model *ranking* uses AF2's default confidence ranking (p3).

## D. Claims

- **central_conclusion**: AlphaFold2 predicts only one conformational state per GPCR and is
  biased toward whichever state is over-represented in its training data for that class
  (inactive for A, C, F; active for B1). Replacing PDB70 with a GPCRdb-derived,
  activation-state-annotated template database *and simultaneously deleting the MSA* lets an
  operator direct AF2 to either state at near-experimental accuracy — median TM-RMSD 1.12 Å
  active and 1.41 Å inactive on 68 post-training-cutoff human GPCRs — with the correct state
  recovered for 10 of 15 receptors solved in both. The improved active-state models translate
  into better ligand docking and were validated in the blind GPCR Dock 2021 competition.

- **necessity_claims** (verbatim + page):
  - p3: "using such curated template databases was not sufficient to make meaningful changes."
  - p3: "This suggests that simply using templates according to a conformational state as input
    to AF2 has little impact when deep MSAs were provided as inputs."
  - p2: "the regular AF2 protocol can predict accurate GPCR models, more accurate than
    template-based modeling, but it was not possible to predict models in multiple states for
    most of the benchmarked GPCRs."
  - p1 (abstract): "However, AlphaFold2 only predicts one state and is biased toward either the
    active or inactive conformation depending on the GPCR class."
  - p7: "This requires the structure of the target protein for being able to dock potential
    ligands. Because protein-ligand docking is very sensitive to the structure of the binding
    pocket, high-accuracy models are essential for docking success."
  - p7: "Therefore, to design a ligand that targets a certain activation state of a GPCR, a
    high-accuracy protein model for that state is required."
  - p11: "We did not use our multi-state prediction protocol for peptide docking because that
    approach removes MSA information while coevolutionary information from MSA was essential
    for predicting inter-protein contacts."
  - p9: "The multi-state modeling approach introduced here can be extended in principle to
    other protein families such as kinases as long as experimental structures in multiple
    states are available to form state-specific template databases" (conditional necessity: the
    method requires deposited multi-state structures to exist).
  - p7: "In the case of such complex pathways, it was difficult to capture intermediate states
    with our protocol (e.g., PTH1R/Q03431)."
  - p2: "Proteins often possess multiple conformational states to perform their biological
    roles, whereas prediction methods are generally trained to predict a single, native state
    for a given sequence."

- **novelty_claims** (verbatim + page):
  - p1 (abstract): "Here, a multi-state prediction protocol is introduced that extends
    AlphaFold2 to predict either active or inactive states at very high accuracy using
    state-annotated templated GPCR databases."
  - p1 (abstract): "At the time, the new protocol paves the way towards capturing the dynamics
    of proteins at high-accuracy via machine-learning methods." (text-layer note: "At the time"
    appears to be a typo for "At the same time".)
  - p9 (Conclusions): "we expect that the approach described here is a first step towards
    capturing not just native structures but conformational dynamics at high-accuracy via
    machine learning-based approaches."
  - p2 (gap claim against prior GPCR model databases): "However, the accuracy of these GPCR
    models has not been rigorously benchmarked, especially with respect to reproducing
    differences between active and inactive states and in light of the recent advances in
    structure prediction accuracy."
  - p2 (gap claim against RoseTTAFold's state-specific templates, i.e. the closest prior art):
    "The method generated reasonable models for both states. However, generating very accurate
    active state models was less likely unless there were templates with high sequence
    identities, thus, there was still room for improvements."
  - p8: "As exemplified here, our high accuracy multi-state modeling of GPCRs offers important
    practical advantages for predicting ligand-bound structures over other methods."

- **stated_limits**:
  - **The method trades away MSA information and can therefore lose to plain AF2 on the state
    AF2 already favours.** p4: "Since we sacrificed information that can be inferred from the
    MSA for modeling both states, it was less likely that we could predict better models for
    these states, and thus we could obtain similar performance to AF2, at best." Concretely,
    p4: "models in the state by our multi-state protocol were comparable to the AF2 models
    (class A) or slightly worse than AF2 (class C and F)."
  - **Thin per-class evidence.** p4: "For class F GPCRs, it was satisfactory as well, however,
    there were only three targets in the benchmark set."; p4: "A poor model was generated for a
    class B2 GPCR, but based on only one example we cannot draw more general conclusions about
    modeling class B2 GPCRs."
  - **The template-identity relationship could not be established for inactive states.** p6:
    "For the inactive state models, we could not conclude that there is a clear template
    similarity dependence since there were not enough GPCRs that had low template homology."
  - **Loop failures are not rescued.** p4: "substantially incorrect loop structures in the
    input features could not be rescued and remained incorrect" — worst for "very long ECL2s".
  - **Intermediate sampling does not generalise.** p9: "However, the general applicability of
    this approach still needs further investigation." p7: "our protocol occasionally could not
    generate diverse conformations when active and inactive state models showed little
    structural difference (e.g., CASR/P41180)."
  - **Docking is bounded by an unfavourable ceiling and by ligand size.** p7: "ligand docking
    to active state conformations is intrinsically a difficult problem considering that
    self-docking to less than half of the experimental structures was successful"; p8: "The
    lower success rates with inactive state docking for models compared to experimental
    structures may be because antagonists in the benchmark set are bigger than agonists".
  - **Models are apo.** p7: "computational model structures were predicted without
    consideration of binding ligands and resulted in apo structures."
  - **Docking scope was restricted to easy ligands.** p11: "We selected ligands that have not
    too many rotatable torsion angles (<15) and heavy atoms (<25) because the docking procedure
    described below may not effectively handle such high degrees of freedom and lead to docking
    failures."

- **stance** (provisional; the user's call): **precedent on the method + contrast on rigour.**
  - *Precedent*: this is the original AlphaFold-Multistate protocol and the reference point
    every later GPCR state-biasing paper is measured against; the accuracy numbers (1.12 Å
    active / 1.41 Å inactive, 10/15 correct states) are the standing bar, and the paper's own
    negative result — that state-annotated templates do nothing while a deep MSA is present
    (p3) — is directly reusable.
  - *Contrast*: the state is not predicted, it is instructed. The operator declares it, the
    template database supplies it from GPCRdb annotations of deposited structures, success is
    defined by comparative RMSD to two references the authors already hold, and the state call
    is only possible for the 15 receptors solved in both states. Its accuracy is also bought by
    discarding coevolutionary information, which the authors themselves say costs them on
    AF2-favoured states (p4).

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Median TM-RMSD, multi-state protocol, **active** state | **1.12** | Å (Cα, TM helices) | closest active-state experimental structure, 49 post-cutoff GPCRs | p3 |
| Median TM-RMSD, multi-state protocol, **inactive** state | **1.41** | Å | closest inactive-state experimental structure, 30 GPCRs | p3 |
| High-accuracy fraction, multi-state active | 35/49 = **71%** | fraction <1.5 Å TM-RMSD | active references | p3 |
| High-accuracy fraction, multi-state inactive | 17/30 = 57% | fraction <1.5 Å | inactive references | p3 |
| Median TM-RMSD, original AF2 vs **any** state | 1.49 | Å | any experimental structure of the 68 | p3 |
| High-accuracy fraction, original AF2 vs any state | 34/68 = 50% | fraction <1.5 Å | any state | p3 |
| Median TM-RMSD, original AF2 vs **inactive** | 1.33 | Å | inactive references | p3 |
| High-accuracy fraction, original AF2 inactive | 19/30 = 63% | fraction <1.5 Å | inactive references | p3 |
| Median TM-RMSD, original AF2 vs **active** | 1.86 | Å | active references | p3 |
| Median TM-RMSD, TBM (MODELLER, same templates) | 2.71 | Å | any state | p3 |
| High-accuracy fraction, TBM | 3/68 = 4% | fraction <1.5 Å | any state | p3 |
| Median TM-RMSD, AF2 **without templates** (MSA only) | 1.55 | Å | any state | p3 |
| Median TM-RMSD, AF2 **without MSA** (PDB70 templates only) | 1.84 | Å | any state | p3 |
| Median TM-RMSD, RoseTTAFold multi-state, active | 2.16 | Å | active references, 49 targets | p5 |
| High-accuracy count, RoseTTAFold active | 2/49 | models <1.5 Å | active references | p5 |
| **Correct-state discrimination, multi-state protocol** | **10/15** | GPCRs | receptors solved in both states; predicate RMSD_own-state < RMSD_other-state | p3–p4 |
| Baseline AF2 state bias | 11/15 closer to inactive | GPCRs | both-state receptors | p3 |
| Median TM-RMSD **between** active and inactive experimental structures | 2.26 | Å | experiment vs experiment (the scale the 1.12/1.41 must be read against) | p3 |
| Paired t-test, multi-state vs AF2, active | p = 8.2 × 10⁻⁸ | — | null of identical performance | p3 |
| Paired t-test, multi-state vs AF2, inactive | p = 0.37 | — | null of identical performance | p3 |
| pLDDT > 90 → accurate, active | 29/35 = 83% | fraction <1.5 Å | benchmark GPCRs | p5 |
| pLDDT > 90 → accurate, inactive | 14/19 = 74% | fraction <1.5 Å | benchmark GPCRs | p5 |
| Template seq. identity > 20% → accurate, active | 30/36 = 83% | fraction <1.5 Å | benchmark GPCRs | p6 |
| Pearson r, TM-RMSD vs pLDDT (active / inactive) | −0.61 / −0.29 | — | benchmark GPCRs | p6 (Figure 3, read from render) |
| Pearson r, TM-RMSD vs max template identity (active / inactive) | −0.58 / −0.27 | — | benchmark GPCRs | p6 (Figure 3, read from render) |
| Proteome-wide expected accuracy, pLDDT > 90 | 209/289 = 72% active; 189/289 = 64% inactive | fraction | human GPCRs with no structure for that state | p5 |
| Docking success, multi-state active models | "around one third" ≈ 34% top-1 (read from Figure 4A) | % within 3 Å ligand heavy-atom RMSD | experimental ligand pose | p7, p8 |
| Docking success, other computational models, active | <10% | % within 3 Å | experimental ligand pose | p7 |
| Docking success ceiling, experimental active structures | "less than half" ≈ 45% top-1 / 69% top-3 (Figure 4A) | % within 3 Å | self-docking | p7, p8 |
| Docking success, inactive/antagonist, multi-state ≈ AF2 | ~30 | % within 3 Å | experimental ligand pose | p8 |
| Docking success ceiling, experimental inactive structures | <80 (≈80% top-1, 100% top-3 in Figure 4A) | % within 3 Å | self-docking | p8 |
| 5-HT1A worked example: ligand RMSD, multi-state vs AF2 model | 0.55 vs 4.38 | Å heavy-atom | experimental complex 7E2Y | p7–p8 |
| 5-HT1A binding-site accuracy, multi-state model | 1.05 | Å heavy-atom (site residues) | experimental complex | p7 |
| GPCR Dock 2021 T04 (NPY1R): multi-state active model | 1.14 | Å TM-RMSD | 7vgx_R (active) | p8 |
| GPCR Dock 2021 T04: AF2 model | 0.93 vs inactive 5zbh_A; 2.17 vs active | Å TM-RMSD | both references | p8 |
| GPCR Dock 2021 T04: bound NPY peptide placement | 2.00 | Å Cα-RMSD | 7vgx_L | p8 |
| GPCR Dock 2021 T04: NPY C-terminal residues 32–36 | 1.88 | Å heavy-atom RMSD | 7vgx_L | p8 |
| CXCR2 worked example (Figure 1 labels) | active 1.09; inactive 1.31; AF2 2.03 (A) / 1.44 (I) | Å TM-RMSD | 6lfo_R / 6lfl_A | p4 (figure labels, render) |
| State-annotated database size | 224 active / 309 inactive structures → 161 / 206 unique entries | structures | GPCRdb as of 2021-07-29 | p10 |

- **n_predictions**:
  - **Samples per target**: **5** AF2 models per run — p9: "as output five models are
    predicted." The protocol is run **once per state**, so a both-state receptor gets 5 + 5.
  - **Targets**: 68 benchmark GPCRs (49 active-state + 30 inactive-state evaluations,
    15 receptors in both) — p10. Plus all human non-olfactory GPCRs modelled in both states,
    of which 289 lack a structure for the state (p5, p10).
  - **Totals**: not stated as a single number anywhere. Implied benchmark total ≈ (49+30) × 5
    ≈ 395 scored models, plus the proteome-wide run.
  - **Intermediate arm**: 21 inputs → 21 outputs per target, 1 output model per input — p10–11:
    "we used equally spaced values from 0% to 100% with an incremental of 5%; it resulted in
    21 input models. For each input model with a different degree of activation, one output
    model was predicted."
  - **Del Alamo comparator arm**: 4 MSA depths × 20 models = 80 per target — p11: "For each
    depth of MSA, 20 models were generated for a target with different random seeds."
  - **Docking**: 5 independent runs per protein–ligand pair — p10: "Protein-ligand docking was
    performed five times independently for a given protein structure", AutoDock Vina
    exhaustiveness 32 (p11). Number of complexes docked: NOT REPORTED in the PDF (Table S3).
  - **GPCR Dock 2021**: 5 targets submitted, 2 assessable (p8).

- **comparable_to_ours**:

- **si_in_scope**: **HELD as of 2026-09-10, via the bioRxiv preprint rather than Wiley.**
  `10.1101/2021.11.26.470086` **version 2** (2022-04-08) is the revision that became
  Proteins 90:1873–1885, is CC-BY, and its SI is at `../source/si/heo2022multistate_SI_biorxiv_v2.pdf`.
  **Use v2, not v1**: v1's "recently determined" set has only 55 receptors, v2's has the
  published 68. The two versions' Table S3 are also different tables entirely.

  Extracted: **Table S2** → `../panels/si_tables/heo2022multistate_tableS2.csv`, 68 receptors
  with UniProt, gene, class and per-state structure counts — reproducing all four published
  numbers exactly (68 receptors, 49 with an active structure, 30 with an inactive, 15 with
  both). **Table S3** → `heo2022multistate_tableS3_docking.csv`, 45 complexes over 19
  receptors, which closes `unresolved` item 4. Table S1 (per-class TM-RMSD) not extracted.

  Note that Table S2 enumerates **receptors, not structures** — it gives per-state counts, not
  PDB ids. `panels.csv` marks these rows `panel_unit=receptor` for exactly that reason.

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 4 | TM-RMSD of four modelling protocols against active and against inactive references, for the receptors solved in both states | violin | `PLOT \| facet: reference state (2: active, inactive) \| vary: protocol (4: AlphaFold −annotatedDB +MSA; AlphaFold +annotatedDB +MSA; AlphaFold +annotatedDB −MSA; TBM +annotatedDB) \| series: none (1) \| measure: TM-RMSD (Å) \| mark: violin \| n: 15 both-state GPCRs per violin (from p10), 60 per panel; not stated in the caption` | 2 stacked panels, varying by reference state; protocol encoded as a ±annotated-DB / ±MSA table under the axis rather than as a legend | y-axis pinned to 0–4 Å; TBM and AF2-active distributions plainly extend past 4 Å (TBM median is 2.71 Å) and their upper tails are cut, so the worst arm is visually compressed. n is never shown on or under the panels. Medians quoted in the text are not printed on the figure | CC BY-NC-**ND** — p1: "This is an open access article under the terms of the Creative Commons Attribution-NonCommercial-NoDerivs License ... no modifications or adaptations are made." **ND forbids redrawing as well as modifying** |
| 1B-C | 4 | CXCR2 active and inactive models superposed on both experimental structures, extracellular and side views | structure render | `RENDER \| facet: model (3: active-state prediction, inactive-state prediction, AlphaFold prediction) \| views: 2 (extracellular, side) \| overlay: 1 prediction on 2 references per facet \| axis: none` | 6 renders in a 3×2 grid; B is the extracellular view row, C the side view row; per-model TM-RMSDs printed as labels (1.09 / 1.31 / 2.03 (A), 1.44 (I) Å) | | as above, p1 |
| 2 | 5 | Sidechain-level activation changes in CXCR2 at three motif sites, models vs experiment | structure render | `RENDER \| facet: motif site (3: W6×48, PIF motif, NPxxY+DRY) \| views: 1 \| overlay: 2 predictions (active, inactive) on 2 references \| axis: none` | 3 panels (A, B, C) varying by motif; no camera-angle variation | no quantitative panel at all — the claim "captured very accurately up to atomistic detail" (p4) is supported only by superposition and red arrows; no per-atom deviation is reported | as above, p1 |
| 3 (density row of each pair) | 6 | Distribution of pLDDT and of max template identity across human GPCRs that have **no** experimental structure for that state | bar (histogram) | `PLOT \| facet: state (2: active, inactive) × predictor (2: pLDDT, max template identity) \| vary: pLDDT 60–100 / max template identity 0–100% (continuous) \| series: none (1) \| measure: density \| mark: bar \| n: 289 GPCRs per panel (from p5), not stated in the caption` | 4 histogram panels, each sitting above its matching scatter panel; the yellow shaded region marks the selection criterion and carries the retained percentage (72 / 54 / 64 / 49%) | n per histogram not shown; the panels have no letters, so no caption-level way to reference them | as above, p1 |
| 3 (scatter row of each pair) | 6 | TM-RMSD of benchmark models against pLDDT and against max template identity, with moving average and Pearson r | scatter | `PLOT \| facet: state (2: active, inactive) × predictor (2: pLDDT 60–100, max template identity 0–100%) \| vary: predictor value (continuous) \| series: none (1) \| measure: TM-RMSD (Å) \| mark: point + moving-average line \| n: 1 per point; 35 active / 19 inactive points per panel (from p5)` | 4 scatter panels sharing x-axes with the histograms above them; blue dashed moving average (window 2.5 pLDDT / 5% identity), horizontal line at the 1.5 Å criterion | the criterion thresholds (pLDDT 90, identity 20%) are drawn on the same data they were chosen from, so the shaded success rate is not an out-of-sample estimate; n per panel not printed | as above, p1 |
| 4A | 8 | Ligand docking success ratio by protein-structure source, for agonist/active and antagonist/inactive complexes | bar | `PLOT \| facet: state (2: active, inactive) \| vary: structure source (4: experimental; AlphaFold +MSA −annotatedDB; AlphaFold −MSA +annotatedDB; TBM +annotatedDB) \| series: prediction rank cutoff (2: top-1 opaque, top-3 transparent) \| measure: docking success ratio (%) \| mark: bar with SE error bars \| n: 5 independent docking runs per structure–ligand pair (p10); number of complexes per bar NOT REPORTED (Table S3 not held)` | 2 stacked panels varying by activation state; source encoded as a ±annotated-DB / ±MSA table under the axis | bars over a per-complex distribution — the underlying per-target success/failure pattern is never shown; the number of complexes behind each bar is nowhere in the held PDF, so the SE bars cannot be interpreted; the top-3 segment is stacked on top-1 rather than plotted separately | as above, p1 |
| 4B-C | 8 | Docked serotonin pose in the AF2 model vs the multi-state model of 5-HT1A, against the experimental complex | structure render | `RENDER \| facet: protein model (2: original AlphaFold, multi-state) \| views: 1 (binding pocket) \| overlay: 1 docked pose on 1 experimental complex \| axis: none` | 2 panels varying by model source; each labelled with binding-site RMSD, TM lDDT and ligand RMSD (1.36, 0.78 / 4.38 Å vs 1.05, 0.84 / 0.55 Å) | single hand-picked example; the caption does not say how it was selected from the docking set | as above, p1 |
| 5A | 9 | GPCR Dock 2021 target T04 (NPY1R): multi-state active model and AF2 model against both experimental states | structure render | `RENDER \| facet: none (1) \| views: 2 (extracellular, side) \| overlay: 2 predictions on 2 references (7vgx_R active, 5zbh_A inactive) \| axis: none` | 2 stacked views of one system | | as above, p1 |
| 5B-C | 9 | Bound neuropeptide Y placement in the predicted complex vs experiment | structure render | `RENDER \| facet: none (1) \| views: 2 (overview, C-terminal residues 32–36) \| overlay: 1 prediction on 1 reference \| axis: none` | 2 panels, differing by zoom level on the same system | | as above, p1 |

**9 panel-group rows across 5 figures.** Renders taken of pages 4, 6 and 8, where the captions
do not carry the panel grid (Figure 1's four-protocol ±DB/±MSA axis table, Figure 3's 2×2×2
histogram/scatter arrangement and its r values, Figure 4A's top-1/top-3 series). Figures 2 and
5 captions carry their full panel structure; not rendered.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), schema v3 batch
- **schema_version**: v3
- **confidence**: **high** for A, B, C, D and the figure table; **medium** for E, purely because
  a substantial share of the paper's per-target and per-class numbers are in absent SI, and
  because several docking percentages exist only as bar heights in Figure 4A (read from the
  render and marked as such). Text extraction is clean apart from flattened superscripts, noted
  at the top.
- **unresolved**:
  1. **Which of the two uses of the annotated database is the released protocol.** Methods 4.1
     (p10) says "Databases were used in two ways" — straight PDB70 replacement, and MSA gapping
     at template-aligned positions (Algorithm S1). The Results text and Figure 1A's axis table
     describe the winning arm only as "annotated DB, no MSA input", which reads as the first
     use with the MSA deleted; but then the second use, the gapping variant, has no reported
     result in the held PDF at all. Algorithm S1 is not held. Cannot be settled from this PDF.
  2. **Scope of the 70% sequence-identity template exclusion.** p10 states it "For the benchmark
     test." Whether it also applied to the proteome-wide run or to the GPCR Dock submissions is
     not stated. If it did not, those arms could see the target's own homologues.
  3. **Whether the state-annotated databases were date-filtered.** They were built "As of
     July 29, 2021" (p10) from all GPCRdb entries, i.e. inside the 2018–2022 benchmark window.
     Nothing says post-2018 structures were removed from the template side; only the 70%
     identity filter is mentioned. This is the weak point of an otherwise clean post-cutoff
     design and the paper does not address it.
  4. ~~**Number of protein–ligand complexes in the docking benchmark** — Table S3, not held.~~
     **RESOLVED 2026-09-10: 45 complexes, 19 receptors** (bioRxiv v2 Table S3). Original note: The
     Figure 4A error bars are therefore uninterpretable from the PDF alone.
  5. **No justification is given for the 1.5 Å TM-RMSD "high accuracy" threshold** or the 3 Å
     docking success threshold. Both are used throughout as if standard.
  6. **Exact docking success percentages** for the model arms are given in prose as "around one
     third", "less than 10%", "around 30%", "less than 80%"; the numeric values exist only as
     bar heights. Values in `metrics_reported` marked "read from Figure 4A" are eyeballed from
     the 150 dpi render and should not be quoted to better than ±3 percentage points.
  7. **No tag was needed that does not exist in v3.** Nothing invented.
  8. **Schema ambiguity — RENDER rows have no splitting rule.** The v3 rule is "split when
     `mark` or `measure` differs", but the RENDER form has neither slot. Figure 5 was split into
     5A and 5B-C because `overlay` and the subject differ (2 predictions on 2 references vs
     1 on 1), while Figure 1B-C and Figure 2 were each kept as one row. That was a judgement
     call, and a different extractor could defensibly merge or split all three differently.
     Suggest: for RENDER, split on `overlay`, treating it as the measure analogue.
  9. **Schema ambiguity — panel-group suffixes assume the figure has panel letters.** Figure 3
     has eight panels and no letters at all, so `fig_no` had to carry a prose qualifier
     ("3 (density row of each pair)") which will not join cleanly against a `4A`-style key.
     Suggest allowing a positional suffix convention for unlettered figures.
  10. **Schema ambiguity — `facet` in PLOT with two crossed variables.** Figure 3 is faceted by
      state *and* by predictor. The grammar shows a single `<var> (<n>)`; the RENDER worked
      example uses `×` for crossed facets, so `×` was borrowed into PLOT here. Worth stating
      explicitly in v4 that crossing with `×` is legal in every form.
- **why_it_matters**:

## Tags

`gpcr` `template-state-bias` `msa-state-filter` `templates-on` `state-annotated-input`
`two-state` `single-state` `rmsd-only` `binary-predicate` `visual-metric` `saturating-metric`
`oracle-leak` `design-level-oracle` `anti-memorization` `multi-backbone`
`confidence-as-discriminator` `directed-state` `apo-sampling` `orthosteric` `peer-reviewed`
`precedent` `contrast` `comparator-numbers`

Tag notes, so the reverse lookups stay honest:
- `msa-state-filter` is applied for the template-guided MSA-gapping variant (p10, Algorithm S1),
  which substitutes a state-directed alignment rather than reducing depth. `msa-subsample` is
  **not** applied: subsampling appears only in the reproduced Del Alamo comparator, not in this
  paper's method.
- `two-state` + `single-state`: the protocol delivers one state per run and two states per
  receptor across two runs; baseline AF2 in the same paper is strictly single-state. `ensemble`
  and `continuum` are **not** applied — the intermediate arm is explicitly reported as
  discontinuous (p6–7).
- `visual-metric` is applied for Figures 2, 1B-C and 5, where mechanistic correctness is argued
  by superposition with no predicate; it coexists with `rmsd-only` and `binary-predicate`,
  which cover the quantitative half.
- `saturating-metric` refers to the docking success ratio ceiling (p7–p8), not to TM-RMSD.
- `anti-memorization` is applied on the strength of the explicit post-2018-05-01 benchmark
  (n = 68, p10); `no-anti-memorization` is **not** applied. The template side is not date
  filtered — see `unresolved` 3.
- `multi-backbone` is applied for the AF2 vs RoseTTAFold head-to-head on identical templates
  (p5). MODELLER and GPCRdb are homology-modelling comparators, not backbones.
- `orthosteric` is applied because all docking is at the orthosteric pocket (p11: "The center
  of the docking search space was manually set at the canonical class A GPCR binding pocket").
  No allosteric site is studied, so no `allosteric-*` tag.
- `experimental-validation` is **not** applied: GPCR Dock 2021 is a blind prediction contest
  scored against structures solved by others, not an experiment run by these authors.
- `negative-result` is **not** applied to the paper as a whole, though it contains a sharp
  internal negative result (state-annotated templates do nothing with a deep MSA, p3).
