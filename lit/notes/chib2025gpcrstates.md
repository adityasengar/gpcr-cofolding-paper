# chib2025gpcrstates

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–24).** For the main
article the PDF page equals the printed page (PDF p8 prints "8"). The Supporting
Information is bound into the same PDF as **PDF pages 20–24**, which print as SI pages
1–5. Mapping for SI quotes: PDF p20 = SI p1 (§1 Dataset Preparation), p21 = SI p2
(§1 cont., §2), p22 = SI p3 (Figure S1, §3 steps 1–3.1), p23 = SI p4 (§3 steps 3.2–5,
§4), p24 = SI p5 (Figure S2).

**The SI is held.** Unlike several papers in this corpus, the substantive methods detail
(the deformation algorithm, the overlap-ratio definition, the t-SNE subset size) is
inside this PDF. See `si_in_scope`.

**Text-layer note:** the text layer is clean. Greek and math render correctly
(`∆H3-H6`, `β1/β2`). Figure axis labels, legends and colourbar ranges are **not** in the
text layer and were read from 150 dpi renders of pages 8, 9, 22 and 24.

---

## A. Identity

- **citekey**: `chib2025gpcrstates`
- **doi**: **arXiv:2502.17628v1** — p1 and p20 sidebar: "arXiv:2502.17628v1 [q-bio.QM]
  24 Feb 2025". `refs.bib` records `doi = {10.48550/arXiv.2502.17628}`,
  `eprint = {2502.17628}`, `archivePrefix = {arXiv}`. No journal DOI appears anywhere in
  the PDF.
- **year**: **2025.** p1 sidebar: "24 Feb 2025".
- **venue**: **arXiv preprint, q-bio.QM, v1, not peer-reviewed.** p1 sidebar:
  "arXiv:2502.17628v1 [q-bio.QM] 24 Feb 2025". There is no journal masthead, no
  received/accepted line, no editor, and no peer-review statement anywhere in the 24
  pages. The manuscript is formatted in the ACS `achemso` style (ACS-style reference
  formatting, "Supporting Information" and "Acknowledgement" sections, `E-mail:` block),
  which suggests an intended ACS submission, but no journal is named. Tagged `preprint`,
  not `peer-reviewed`.
- **title**: "Characterizing the Conformational States of G Protein Coupled Receptors
  Generated with AlphaFold" — p1.
- **authors**: Garima Chib (Dept. of Chemical Engineering, Carnegie Mellon University),
  Parisa Mollaei (Dept. of Mechanical Engineering, CMU), Amir Barati Farimani
  (corresponding, barati@cmu.edu; Mechanical Engineering / Biomedical Engineering /
  Machine Learning Department, CMU) — p1. Three authors, single institution.
  **Self-citation note relevant to the metric:** the H3-H6 metric is imported from the
  group's own prior work — refs 47 (Mollaei & Barati Farimani, *JCIM* 2023, "Activity Map
  and Transition Pathways of G Protein-Coupled Receptor Revealed by Machine Learning",
  p16) and 64 (Mollaei & Barati Farimani, *JCTC* 2023, p18) — and the class analysis uses
  the group's own GPCR-BERT (ref 66, p19).

## B. Scope

- **system**: **GPCR, exclusively.** p6: "The ground truth GPCR structures consist of 75
  GPCRs with four unique receptor classes obtained from the Protein Data Bank (PDB)
  database." Classes A (Rhodopsin), B1 (Secretin), C (Glutamate) and F (Frizzled) are
  described on p5 and counted on p6. No non-GPCR system appears.

- **n_targets**: **75 GPCR reference structures, in four classes. Do not collapse the
  counts; two of them are different populations.**
  - **Main benchmark set: 75.** p6: "The ground truth GPCR structures consist of 75
    GPCRs... The dataset contains 63 receptors in Class A, six receptors in Class B1,
    four receptors in Class C, and two receptors in Class F." 63 + 6 + 4 + 2 = 75,
    consistent. SI p20 repeats: "The dataset contains 75 GPCRs along with their activity
    levels."
  - **t-SNE / class-analysis subset: 16 receptors, a different and much smaller set.**
    SI p23: "We should note that the dataset for this analysis (16 GPCRs) is
    significantly smaller than the dataset used for our study (75 GPCRs)." The Figure S2
    legend (p24 render) names all sixteen: aa2ar, adrb2, ox2r, cnr1, 5ht2b, ntr1, drd1,
    adrb1, opsd, gpr52, cnr2, mtr1a, 5ht2a, cxcr4, nk1r, cltr2. All sixteen are Class A,
    which the paper acknowledges obliquely on p10: "the t-SNE plots do not encompass all
    the receptor classes included in our dataset."
  - **Whether the 75 are 75 *unique receptors* or 75 *structures* is NOT REPORTED and
    matters.** p6 says "75 GPCRs" and "63 receptors in Class A", i.e. the paper uses
    "GPCR", "receptor" and "structure" interchangeably. But the analysis axis is a
    *per-structure* activity level from 0 to 100% (p5), and a single receptor can only
    occupy one point on that axis if only one of its deposited structures is used. The
    Figure S2 render shows ~90 points for 16 named receptors, so in the t-SNE arm points
    are plainly not one-per-receptor. Whether the same is true of the 75 is never stated.
    See `unresolved`.
  - **Generality claim from a single system:** the paper studies only GPCRs and does not
    claim generality beyond them. p10–11 conclusions are scoped to GPCRs throughout.

- **method_class**: **benchmark-only.** No method is proposed, trained or modified.
  Predictions are taken as given from two public sources (p6: AF2 from "the AlphaFold
  Protein Structure Database", AF3 from "the AF3 server") and scored against deposited
  references. The only computation the authors perform is the scoring itself (PyMOL
  superposition, Biopython deformation, MDTraj H3-H6) plus a t-SNE of pre-existing
  GPCR-BERT embeddings. Nothing in the paper intervenes in the prediction pipeline.

- **backbones**: **AF2 and AF3, exactly two, compared head to head.**
  - AF2: p6: "The AF2 generated structures are obtained from the AlphaFold Protein
    Structure Database." These are the **pre-computed AFDB models**, not runs the authors
    executed. Consequence: the model is a full-length UniProt-sequence model, not a model
    of the crystallised construct — which is why the overlap ratio is only ">96%" rather
    than 100% (p6, SI p20–21).
  - AF3: p6: "Additionally, AF3 generated structures were obtained from the AF3 server."
    Cited as ref 61 (Abramson et al., *Nature* 2024, p18). SI p21: "For structures
    generated by AlphaFold 3, the generated sequences are identical to the reference
    sequences."
  - No AF-Multimer, Boltz, Chai, OpenFold, Protenix or RoseTTAFold arm. GPCR-BERT (ref
    66) is used but is a **sequence language model for embedding**, not a structure
    predictor, and is not a backbone.
  - **`multi-backbone` is NOT tagged.** The schema rule is "If more than two are compared
    head to head, tag `multi-backbone`"; two is not more than two. Flagged under
    `unresolved` as a schema edge case, because AF2-vs-AF3 is exactly the head-to-head a
    reverse lookup would want.

- **templates**: **NOT REPORTED.** The word "template" does not appear anywhere in the
  24 pages (verified by full-text grep). The authors never state whether the AFDB models
  or the AF3 server runs used structural templates. This is not a neutral omission: the
  AFDB models were produced by the default AF2 pipeline, whose default template search
  over the PDB can, and for well-studied receptors like β2AR and A2A almost certainly
  does, retrieve the very deposited structures being used as references — and the AF3
  server's default template behaviour is likewise unstated. The paper's own explanation of
  its results appeals to training-data composition (p10) without ever examining templates.
  See `oracle_leakage` route 1.

- **msa_handling**: **NOT REPORTED for the authors' own predictions.** MSAs are mentioned
  once, and only as background description of the AF2 architecture — p3: "It constructs a
  multi-sequence alignment (MSA) that identifies sequences similar to the input
  sequence." Nothing is said about MSA depth, subsampling, clustering, state filtering or
  pinning for either the AFDB models or the AF3 server runs. Neither `subsampled` nor
  `state-filtered` applies; both are absent. Because the AF2 arm is the AFDB, the MSA is
  whatever DeepMind's pipeline built at AFDB build time and is not under the authors'
  control at all.

## C. Conformational core

- **states_generated**: **one (single-state).** One structure per receptor per predictor,
  taken as given. There is no sampling, no seed sweep, no ensemble and no continuum of
  outputs anywhere in the paper. The AF2 arm is a single pre-computed AFDB model per
  UniProt entry (p6); the AF3 arm is whatever the AF3 server returned, with no statement
  of how many models were produced or which was analysed (p6). The *evaluation* axis is
  continuous (activity level 0–100%, p5), but that continuum is a property of the
  reference set, not of anything the models generated. `ensemble` and `continuum` are
  both wrong here. The paper's own conclusion is about the single output collapsing
  toward the inactive end — p10: "AlphaFold demonstrates lower accuracy in predicting
  active GPCR conformations", and p10 on why: active receptors form "a heterogeneous
  ensemble of structures rather than a single well-defined state. This structural
  flexibility poses a challenge for AlphaFold, which is optimized for predicting static
  conformations."

- **structural_priors_used**: **Extensive, and entirely on the evaluation side. None of it
  is a defect; all of it is what a benchmark is made of.** Four distinct priors, kept
  separate because they enter at different points:
  1. **75 deposited PDB structures as ground truth.** p6: "The ground truth GPCR
     structures consist of 75 GPCRs with four unique receptor classes obtained from the
     Protein Data Bank (PDB) database." SI p20: "the reference structures obtained from
     the RCSB PDB server". These supply the target coordinates against which both metrics
     are computed.
  2. **The reference structure supplies the sequence that is modelled.** p6 (Methods
     opening, describing Figure 1): "The process involves extracting the GPCR sequence
     from a reference structure, generating a predicted structure using AlphaFold, and
     quantifying structural deviations". Figure 1 (p4) draws this explicitly: "Reference
     GPCR Structure → GPCR Sequence → AlphaFold". So which construct gets modelled is
     decided by which structure was deposited. This is design-level, and carries no
     conformational information — a sequence is state-agnostic. It is recorded here
     rather than in `oracle_leakage` for exactly that reason. (For AF2 this link is even
     weaker in practice, since the AFDB models are of the full UniProt sequence and match
     the reference construct only to ">96%", p6.)
  3. **GPCRdb activity annotations.** p6: "The activity level associated with each GPCR
     structure is obtained from the GPCRdb database. This database consists of
     experimental information about GPCRs, including ligand binding, sequence alignments,
     and mutation analysis." This is a curated state annotation of the *reference*, and
     it is the independent axis of every quantitative panel in the paper.
  4. **The seven-TM truncation, and the TM3/TM6 residue choice, are structure-derived
     priors from the GPCR activation literature.** p6: "we truncate these structures to
     retain only the seven transmembrane regions of the GPCRs as these domains are
     integral to the activation process." p5: "We also measured contact distances between
     two residues in the intracellular regions of the third and sixth transmembrane
     helices (TM3 and TM6) as this distance is highly correlated with the activity level
     of GPCRs" — justified by refs 46 (Rasmussen et al., β2AR–Gs crystal structure) and
     47 (the authors' own activity-map paper).
  Additionally, **GPCR-BERT (ref 66) is a pretrained sequence prior**, not a structural
  one; it supplies the embedding space for the t-SNE only (p7).

- **oracle_leakage**: **NO PIPELINE LEAKAGE. Routes 1, 2, 3 and 4 are clean; routes 5, 6
  and 7 fire, all on the evaluation/design side. This is the expected signature of an
  honest retrospective benchmark, and the note should not be read as accusing the paper
  of contamination.** All seven routes, separately:

  **Route 1 — structures used as input or template: NONE FOUND as coordinate input;
  templates NOT REPORTED and therefore not clearable.**
  No coordinates enter either predictor. The pipeline is stated in full on p6 and drawn in
  Figure 1 (p4): "The process involves extracting the GPCR sequence from a reference
  structure, generating a predicted structure using AlphaFold, and quantifying structural
  deviations through average deformation and ∆H3-H6 distances." The only thing extracted
  from the reference and passed forward is the **sequence**. For the AF2 arm not even
  that is passed by the authors — p6: "The AF2 generated structures are obtained from the
  AlphaFold Protein Structure Database", i.e. the models were already computed by a third
  party with no knowledge of this study's reference set. For AF3, SI p21: "For structures
  generated by AlphaFold 3, the generated sequences are identical to the reference
  sequences" — sequence identity, not coordinate identity.
  **The caveat that stops this being a clean `NONE FOUND`:** the word "template" never
  appears in the paper, so whether the AFDB models or the AF3 server runs saw the
  reference structures as templates is unstated and unexamined. Both default pipelines
  perform template search over the PDB. The authors cannot control the AFDB arm and did
  not report the AF3 arm. Recorded as **NOT REPORTED / uncontrolled**, not as leakage,
  because nothing in the paper says a template was used.

  **Route 2 — state annotations from a curated database driving templates or alignments:
  NONE FOUND for templates or alignments. GPCRdb annotations are used, but they drive the
  *evaluation axis*, not the prediction.**
  GPCRdb is used exactly once, p6: "The activity level associated with each GPCR structure
  is obtained from the GPCRdb database." That activity level is the x-axis of Figure 2a–d.
  No GPCRdb-derived template set, state-annotated template library, or state-filtered MSA
  appears anywhere; contrast with the state-annotated-database methods elsewhere in this
  corpus. The protocol that would have to contain such a step is fully described on
  p6–p7 and contains no alignment or template construction at all, only PyMOL
  superposition of a finished prediction onto a finished reference.

  **Route 3 — cluster labels derived from known states: NONE FOUND.**
  The only clustering in the paper is the t-SNE on GPCR-BERT `[CLS]` embeddings, p7: "By
  extracting the [CLS] token embeddings from the final hidden state of the GPCR-BERT
  model, we can perform a t-distributed stochastic neighbor embedding (t-SNE) analysis."
  The embeddings are **sequence**-derived, so the cluster geometry cannot carry state
  information; p9 confirms the clusters are receptor identities: "The resulting clusters
  correspond to distinct GPCR classes". State knowledge enters only as the *colour* on
  those clusters, which is deformation-to-reference — that is route 5, recorded there, not
  a cluster label. No cluster is defined by, or split on, a known state.

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against
  known states: NONE FOUND, because nothing is tuned at all.**
  Nothing in this paper is trained, fitted, swept or selected. There is no threshold to
  tune (see `state_metric`: neither metric has one), no seed choice reported, no
  hyperparameter, no stopping criterion, and no model-selection rule. The complete
  protocol is p6–p7 and SI §§1–3 (p20–23); it is a fixed, deterministic post-processing
  chain. The v3 warning that "tuning a *range* on the evaluation set is leakage even when
  no single value is picked per target" has nothing to attach to here: the only ranges in
  the paper are *reported* ranges of the results (p8: "the average deformation ranges from
  0.25Å to 2Å"), not swept ranges. The one place a hidden tunable does exist —
  PyMOL `align`'s default outlier-rejection cutoff — is not reported and so cannot have
  been reported as tuned; see `unresolved` item 4, which is a reproducibility gap rather
  than a leakage finding.

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had: PRESENT,
  and it is the entire result section.**
  Both metrics are deviation-from-reference quantities and neither exists without the
  deposited structure. p5, defining the first: "To assess AlphaFold's predictive accuracy,
  we define the deformation between ground truth and generated structures as the average
  distance between alpha carbon atoms in both structures." p7, defining the second: "We
  then calculate the absolute difference between the H3-H6 distance in the reference and
  predicted structures to assess the accuracy of AlphaFold predictions." Every number in
  Figure 2 and every colour in Figure 3 is one of these two. Because the predictions
  (AFDB, AF3 server) were fixed before the references were consulted, this is post-hoc
  *evaluation*, which is what a benchmark is for — it does not contaminate the
  predictions. It is recorded because it means **the paper has no reference-free notion of
  a conformational state**: there is no predicate that could be applied to a prediction
  whose true structure is unknown, which is precisely the property that would be needed to
  reuse this as a state predicate on novel targets.

  **Route 6 — best/worst model labels assigned against a held reference: PRESENT, at
  target level, post hoc.**
  p9: "Our findings reveal that the adenosine A2A receptor exhibited the lowest
  deformation values for both AF2 and AF3. In contrast, the dopamine D1 receptor showed
  the highest deformation with AF2, while the serotonin 2A receptor had the highest
  deformation with AF3." Repeated in the conclusion, p11: "The adenosine A2A receptor
  exhibited the lowest deformation values, while the dopamine D1 and serotonin 2A
  receptors showed higher deformation values." These best/worst labels are assigned purely
  by deviation from the held reference. They are *target*-level labels, not
  *model*-selection labels: no candidate model is chosen over another using the reference,
  because there is only ever one model per target per predictor. The model-selection form
  of route 6 is **NONE FOUND** — and the reason is worth stating, since it is also a gap:
  the AFDB deposits a single pLDDT-ranked model and the AF3 server returns several, and
  the paper never says which AF3 output was used (p6), so no selection rule of any kind is
  documented, reference-based or otherwise.

  **Route 7 — design-level oracle use (systems or conditions chosen because the expected
  answer is already known): PRESENT, and it is the weaker, design-level kind. Label it as
  such; do not conflate it with pipeline leakage.**
  Every target in the study was selected because a deposited structure *and* a GPCRdb
  activity annotation already existed for it. p6: "The ground truth GPCR structures consist
  of 75 GPCRs with four unique receptor classes obtained from the Protein Data Bank (PDB)
  database... The activity level associated with each GPCR structure is obtained from the
  GPCRdb database." The reference structure additionally determines which sequence is
  modelled (p6, Figure 1 on p4), so a matched reference exists for every prediction *by
  construction*. This is the ordinary and unavoidable design of a retrospective benchmark.
  **What the paper does not do, and this is to its credit, is declare a per-target expected
  state before reading the result** — there is no "we expect AF to return the inactive
  state of receptor X" anywhere; the inactive-bias conclusion (p8, p10) is drawn from the
  aggregate trend after the fact. So route 7 fires on **system selection only**, at its
  weakest setting.

  **Verdict in one line:** no knowledge of the deposited target structures entered the
  prediction pipeline (routes 1–4 clean, with template handling unreported rather than
  leaky); routes 5, 6 and 7 fire entirely post hoc on the evaluation and target-selection
  side, which is the normal and honest signature of a retrospective benchmark. Tag
  `design-level-oracle`, **not** `oracle-leak`.

- **prospective**: **no — retrospective throughout, in both halves.**
  The pipeline half is clean of leakage (routes 1–4), but that does not make the study
  prospective: every target was chosen because its answer was already deposited (route 7),
  and every reported quantity is a distance to that answer (route 5). No prediction is made
  about a receptor or a state whose structure was unknown at the time; no post-cutoff set
  exists (see `anti_memorization_design`); no experimental follow-up is performed. The
  paper does not itself claim to be prospective. The one forward-looking statement is a
  hope rather than a result — p11: "Continued refinement of these models can further
  improve their usefulness in drug discovery and development".

- **state_metric**: **RMSD-to-reference + continuous coordinate (dual). Two metrics, both
  deviation-from-reference, no threshold on either, and no binary state call anywhere in
  the paper.** This is the field this paper is in the corpus for, so both are given in
  full with their exact residue and atom scope.

  **Metric 1 — "average deformation", units Å.**
  *Definition, verbatim, p5:* "To assess AlphaFold's predictive accuracy, we define the
  deformation between ground truth and generated structures as the average distance
  between alpha carbon atoms in both structures."
  *Region scope, verbatim, p6:* "For our analysis, we truncate these structures to retain
  only the seven transmembrane regions of the GPCRs as these domains are integral to the
  activation process."
  *Superposition, verbatim, p6:* "To estimate AlphaFold's predictive accuracy, we align the
  ground truth and predicted structures using PyMOL, a molecular visualization software.
  This process involves sequence alignment and spatial superposition." And SI p20: "We
  aligned the reference structures obtained from the RCSB PDB server with their AlphaFold
  generated counterparts using the `align` tool in PyMOL. This allows us to calculate the
  average distance between corresponding alpha carbon atoms in both structures."
  *Procedure, verbatim, p6–p7:* "To calculate deformation, we utilize the Biopython
  package in Python... The workflow includes the following steps: 1. Parsing the PDB files
  for both ground truth (reference) and predicted structures to iterate through the entire
  amino acid sequence. 2. Extracting the seven transmembrane (TM) regions from the
  reference structures. 3. Identifying the corresponding TM regions in the predicted
  structures that consist of the same sequence of residues. 4. Calculating the Euclidean
  distance between alpha carbon atoms of matching residues in the reference and predicted
  structures... The average distance between these alpha carbons is used as a metric to
  evaluate AlphaFold's prediction accuracy."
  *How the seven TM regions are actually identified, verbatim, SI p22–23 (§3):* "2. **Extract
  Top 7 Subsequences**: Identify the 7 longest subsequences (TM regions) of alpha carbons
  from the reference structure. 3. **Find Corresponding Subsequences**: 1. For each
  reference subsequence, scan the generated structure to create sequences of alpha carbons
  with residue names and numbers. 2. For each potential subsequence in the generated
  structure: Compare it with the reference subsequence. Count how many residues match in
  terms of residue names. Track the subsequence with the highest number of matching
  residues as the best match. 4. **Compute Distances**: Calculate the Euclidean distances
  between corresponding CA atoms of matching residues for each matched subsequence pair.
  5. **Calculate Average Deformation**: Determine the average deformation distance for each
  protein and store the results."
  *Reduced to a specification:*
  - **Which residues:** the residues of the seven transmembrane segments only; loops,
    termini, ECD and ICL3 are excluded by the p6 truncation. The TM segments are defined
    **operationally, not from an annotation** — they are "the 7 longest subsequences...
    of alpha carbons" of the truncated reference (SI p22), i.e. the seven longest runs of
    consecutively resolved CA atoms. **The source of the original TM boundaries used for
    the p6 truncation is never stated** (not GPCRdb, not UniProt, not Ballesteros-Weinstein
    — none is named). Within each segment, only residues whose *residue names* match
    between reference and prediction contribute (SI p23).
  - **Which atoms:** **alpha carbons (CA) only**, stated four times (p5, p7 step 4, SI p20,
    SI p23 step 4). No sidechain, no backbone N/C/O, no all-atom variant.
  - **Which alignment tool:** **PyMOL, the `align` command** (SI p20; p6 describes it as
    "sequence alignment and spatial superposition"). Note that the residue correspondence
    used for the *superposition* (PyMOL's own sequence alignment) is a different
    correspondence from the one used for the *distances* (Biopython longest-subsequence +
    residue-name best match, SI p22–23); the paper does not reconcile them.
  - **Reduction:** arithmetic **mean** of the per-pair Euclidean CA–CA distances, pooled
    across all seven TM segments ("Determine the average deformation distance for each
    protein", SI p23). It is a mean absolute deviation, **not** an RMSD — there is no
    squaring and no square root, so it is systematically smaller than the RMSD of the same
    correspondence and is not numerically interchangeable with an RMSD from another paper.
  - **Thresholds:** **NONE.** No cutoff separates "correct" from "incorrect"; the value is
    reported as a continuous quantity on the y-axis of Figure 2a–b and as a colour in
    Figure 3. No success criterion is ever defined.

  **Metric 2 — "∆H3-H6", the TM3–TM6 intracellular contact distance difference, units nm.**
  *Motivation, verbatim, p5:* "We also measured contact distances between two residues in
  the intracellular regions of the third and sixth transmembrane helices (TM3 and TM6) as
  this distance is highly correlated with the activity level of GPCRs." (refs 46, 47.)
  *Definition, verbatim, p7:* "Additionally, we use the H3-H6 distance as a metric to
  evaluate the error in AlphaFold-generated GPCR structures. To determine this distance, we
  identify the third-to-last residue in the third and the sixth TM region of each GPCR,
  calculating the Euclidean distance between their alpha carbons. To achieve this, we use
  the MDTraj Python library, which offers tools for analyzing molecular dynamics
  trajectories. We then calculate the absolute difference between the H3-H6 distance in the
  reference and predicted structures to assess the accuracy of AlphaFold predictions."
  *Reduced to a specification:*
  - **Which residues:** exactly **two** — the **third-to-last residue of TM region 3** and
    the **third-to-last residue of TM region 6**, where "TM region" means the segment
    identified by the same 7-longest-subsequence rule as Metric 1 (SI p22). **No residue
    numbers, no residue names, no Ballesteros–Weinstein indices and no per-target list are
    given anywhere in the paper or SI.** The pair is therefore reproducible only by
    re-running the authors' segment-extraction code (GitHub link, p11), not from the text.
  - **Which atoms:** **alpha carbons**, stated once and unambiguously (p7: "the Euclidean
    distance between their alpha carbons").
  - **Which alignment tool:** **none, and this is a genuine strength.** The H3-H6 distance
    is an intramolecular distance computed within a single structure, so it is invariant to
    superposition; PyMOL `align` plays no part in it. Only **MDTraj** is used, to read the
    coordinates (p7).
  - **Reduction:** `∆H3-H6 = |d_H3-H6(reference) − d_H3-H6(prediction)|` — an **absolute**
    difference (p7). Reported in **nanometres** (Figure 2c–d y-axis "∆H3-H6 (nm)", read from
    the p8 render; Figure S1 on p22 labels raw distances "1.51 nm (Ref)", "1.48 nm (AF2)",
    "1.36 nm (AF3)"). Note the unit inconsistency with Metric 1, which is in Å.
  - **Thresholds:** **NONE.** No cutoff on the raw H3-H6 distance separates active from
    inactive, and no cutoff on ∆H3-H6 separates a correct from an incorrect prediction.
  - **Defect worth carrying forward:** taking the **absolute** value discards the sign, so
    a prediction whose TM6 is too far *out* (over-active) is scored identically to one
    whose TM6 is too far *in* (over-inactive). Since the paper's central claim is directional
    — that AF collapses toward the inactive state — the sign is exactly the quantity the
    claim needs, and the metric throws it away. The signed version is never reported.

  **Why the field is dual.** Metric 1 is an RMSD-to-reference in kind (a mean CA deviation
  after superposition). Metric 2 is built on a genuine **continuous state coordinate** —
  the TM3–TM6 intracellular distance is a standard activation coordinate, and the *raw*
  distance would be a reference-free state descriptor — but the paper reports only its
  absolute difference to the reference, converting a state coordinate into a second error
  measure. Both halves must be recorded: the coordinate is the reusable part, the
  difference-taking is what makes it reference-dependent.

  **`binary predicate`: absent.** The paper never classifies any prediction as active or
  inactive. Activity is a continuous 0–100% GPCRdb annotation of the *reference* (p5:
  "activity levels ranging from 0 to 100 percent"), and prose terms like "inactive
  conformations" (p8) refer to the low end of that axis, not to a call made on a
  prediction.
  **`visual only`: absent as a metric.** Figure S1 (p22) is an illustration of the two
  distances on one receptor, explicitly labelled "Demonstration"; no claim rests on it.

- **metric_saturation**: **Yes, one floor, in ∆H3-H6, and it sits under the headline
  claim.** ∆H3-H6 is an absolute difference and is therefore bounded below by exactly 0.
  In the p8 render of Figure 2c and 2d a substantial population of low-activity points is
  pressed against 0.0 nm — visibly the densest region of both panels. The headline claim
  that "the difference in H3-H6 distances is smaller for inactive conformations compared
  to active ones" (p9) is a claim about a population that is partly resting on the
  metric's own floor, and no statistic is reported that would separate a genuine
  concentration near zero from censoring at the bound. Average deformation does **not**
  saturate: its floor is also 0 but the observed minima are 0.25 Å (AF2) and ~0.8 Å (AF3)
  (p8), comfortably clear of it, and there is no upper bound. No metric ceilings anywhere.
  *Figure-level defects (the different y-scales in Figure 2a vs 2b, the non-zero y-origins,
  the mismatched colourbar ranges in Figure 3a vs 3b) are recorded in the `hides` column of
  the figure table, not here, per the v3 rule.*

- **directional_control**: **NONE. There is no handle of any kind.** The method offers no
  way to instruct either predictor which state to produce, and the paper does not attempt
  one. Enumerating the handles the schema names, against the protocol on p6–p7: no partner
  (predictions are of the receptor alone), no ligand, no nanobody, no G-protein mimetic, no
  state-annotated template (templates are never mentioned), no state-filtered or subsampled
  MSA (MSA handling is never mentioned), no seed (never mentioned), no subsample depth. For
  the AF2 arm a handle is structurally impossible, since the models are pre-computed AFDB
  entries (p6) rather than runs the authors performed. The paper only *observes* which state
  the predictors land in; it never steers. Its closing recommendation is directed at model
  builders rather than at users — p11: "Continued refinement of these models can further
  improve their usefulness in drug discovery and development."

- **anti_memorization_design**: **NONE.** There is no held-out set, no temporal cutoff, and
  no date filter of any kind. The dataset section (p6) states only the source and the class
  breakdown; no deposition-date criterion, no exclusion of structures released before the
  AF2 or AF3 training cutoffs, and no sequence-identity filter against the training set
  appears anywhere in the paper or SI (verified by full-text grep for "cutoff", "held-out",
  "training data" — the only hits are the discussion sentences below). The paper is
  additionally *aware* of the issue and reasons about it without testing it — p10: "the
  scarcity of experimentally resolved active GPCR structures in databases such as the
  Protein Data Bank (PDB) contributes to prediction inaccuracies. Inactive states are more
  frequently captured through techniques like X-ray crystallography and cryo-electron
  microscopy due to their higher stability, leading to an overrepresentation of these
  conformations in AlphaFold's training data." That is a training-composition explanation
  advanced with no training-composition analysis, no per-structure release dates, and no
  memorisation control. n = 0.

- **anti_memorization_control**: **NONE RUN.** Follows from the above: with no held-out or
  post-cutoff set defined, no control arm could be and none was. No arm splits the 75
  receptors by deposition date, by whether the reference postdates the AF2 training cutoff,
  by PDB coverage of the receptor, or by number of deposited structures per receptor — any
  of which would have tested the p10 explanation. `UNPOWERED` is not the right marker here,
  because the issue is not a small n but a wholly absent arm.

- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Sequence overlap ratio between each AF2 (AFDB) model and its reference, defined as `Length of Overlapping Sequence / Length of Reference Sequence` via Biopython global pairwise alignment, reported as ">96% for all samples" | That the deformation is inflated by residue mis-correspondence between a full-length AFDB model and a shorter crystallised construct. It is a data-quality check on the *matching* step, not on the prediction | p6; SI §1, p20–21 |
| AF3 sequence identity check — "For structures generated by AlphaFold 3, the generated sequences are identical to the reference sequences" | The same mis-correspondence risk for the AF3 arm, where it is eliminated by construction rather than bounded | SI §1, p21 |
| AF2 vs AF3 run head to head on the identical 75-receptor reference set, with identical metrics and identical processing | That the activity-level trend is an artefact of one predictor's idiosyncrasies. Both predictors show the same direction (p9: "A consistent trend was observed in both models"), which is the strongest internal evidence in the paper. It is a comparison arm rather than a control proper — neither arm is a negative control | p8–p9, Figure 2 |
| Best-match subsequence search by residue-name agreement, used instead of naive index alignment when AF2 and reference sequences differ | Residue-frame slippage in the deformation calculation for the non-identical AF2 sequences | SI §3, p22–23 |

  **What is absent, and it is most of the standard battery:** no decoy or scrambled
  reference arm; no shuffled-activity-label permutation test (which would cost nothing and
  would establish that the activity trend in Figure 2 is not noise); no apo-vs-holo arm; no
  random-pairing negative control for the metric; no repeat-prediction or seed-variance arm
  (impossible for AFDB, omitted for AF3); no per-class statistical comparison despite class
  being a headline variable; no comparison against a null predictor or a homology model.

- **confidence_as_discriminator**: **NOT USED, and not mentioned.** pLDDT, pTM, ipTM, PAE
  and the word "confidence" appear nowhere in the 24 pages (verified by full-text grep). No
  attempt is made to use a model-confidence score to judge conformational correctness, and
  none to validate such a use. Note the implicit dependence the paper does not discuss: the
  AFDB deposits the single top-ranked model **by pLDDT**, so the AF2 arm is a
  confidence-selected sample without the paper saying so; the AF3 server's ranking and
  which of its outputs was analysed are not reported at all (p6).

## D. Claims

- **central_conclusion**: Given only sequence, both AF2 and AF3 return GPCR structures that
  agree best with deposited references at the **low-activity (inactive) end** of the GPCRdb
  activity scale: both the mean CA deformation over the seven TM helices and the absolute
  error in the TM3–TM6 intracellular distance grow, and scatter more widely, as the
  reference's activity level rises toward 100%. AF3 is not an improvement on AF2 for this
  purpose — its deformation range is roughly three-fold wider (0.8–6 Å vs 0.25–2 Å) and its
  ∆H3-H6 values are consistently larger than AF2's for inactive references. Accuracy also
  varies by receptor, with A2A best under both predictors. The authors attribute the active-
  state weakness to the intrinsic flexibility of active states and to the
  overrepresentation of inactive structures in the training data, neither of which they
  test.

- **necessity_claims** (verbatim + page). The paper is written in a hedged register and
  makes no strong impossibility claim; these are the strongest statements present.
  1. p2 (abstract): "These findings demonstrate the potential of AlphaFold in advancing
     drug discovery efforts, while also highlighting the **necessity** for continued
     refinement to enhance predictive accuracy for active conformations."
  2. p4: "Consequently, a comprehensive evaluation of AlphaFold's predictions is **crucial**
     to assess its effectiveness in modeling GPCR structures."
  3. p5: "These structural and functional distinctions among GPCR classes are **essential**
     for evaluating AlphaFold's predictive accuracy across diverse receptor types."
  4. p6: "For our analysis, we truncate these structures to retain only the seven
     transmembrane regions of the GPCRs as these domains are **integral** to the activation
     process." (The stated justification for the TM-only scope of Metric 1.)
  5. p3, a limitation claim about the prior art rather than about their own method: "However,
     these methods fall short of experimental accuracy, which **limits** their utility for a
     broad range of biological applications."
  6. p10, the nearest thing to an impossibility statement, and it is about the model class
     rather than about any particular attempt: "Active GPCRs undergo significant
     conformational changes upon ligand binding and intracellular coupling, resulting in a
     heterogeneous ensemble of structures rather than a single well-defined state. This
     structural flexibility poses a challenge for AlphaFold, which is **optimized for
     predicting static conformations**."
  7. p5, background biology rather than method — recorded so a later reader does not mistake
     it for a methodological necessity claim: "Class B (Secretin) GPCRs possess an
     extracellular hormone-binding site and a conserved extracellular N-terminal domain
     (ECD) **essential** for their function".
  **No sentence in the paper asserts that any task is impossible, that any component is
  required for a method to work, or that a competing approach cannot succeed.**

- **novelty_claims** (verbatim + page): **NONE FOUND for the authors' own contribution.**
  The paper contains no "first", "novel", "unprecedented", "to our knowledge" or "for the
  first time" claim about its own work — verified by full-text grep across all 24 pages,
  which returns exactly one hit, and that hit is a claim about **AlphaFold**, not about this
  study:
  - p3: "It is **the first** computational approach to protein structure prediction that has
    achieved near experimental accuracy in the majority of cases." (Attributed to refs 26 and
    36; a restatement of the AlphaFold2/CASP14 result, not a priority claim by these
    authors.)
  The abstract's framing is deliberately modest — p1: "This study conducts **an evaluation**
  of AlphaFold's performance in predicting GPCR structures and their conformational states"
  — and the conclusion opens "In this study, we highlight the efficacy of AlphaFold..." (p10)
  rather than with any claim of priority. This paper is therefore **not a priority threat**.

- **stated_limits**: Thin — three, and none of them is the main one.
  1. **The class analysis runs on a different and much smaller dataset than the study.** p9:
     "It should be noted that the dataset used for the t-SNE analysis with GPCR-BERT is
     significantly smaller than the dataset used for our study (see Section 4 in Supporting
     Information)." p10: "Consequently, the t-SNE plots do not encompass all the receptor
     classes included in our dataset." SI p23 gives the numbers: "the dataset for this
     analysis (16 GPCRs) is significantly smaller than the dataset used for our study (75
     GPCRs)."
  2. **AF2 sequences do not exactly match the references, complicating the deformation
     calculation.** SI p23: "Since some of the AlphaFold 2 generated sequences do not exactly
     match the reference sequences, we face some additional challenges in calculating the
     deformation." Mitigated by the best-match procedure and bounded by the >96% overlap
     ratio (p6), but acknowledged as a difficulty.
  3. **AlphaFold needs further refinement for active conformations.** p2 (abstract) and p11:
     "While AlphaFold demonstrates significant potential in accurately predicting GPCR
     structures, its performance varies depending on the receptor's activity level, the
     availability of training data, and structural complexity."
  **Not acknowledged anywhere:** the absence of any memorisation control (§`anti_memorization_design`);
  the absence of any statistical test or summary statistic; the loss of sign in ∆H3-H6; the
  unreported template and MSA handling; the fact that only one model per target per predictor
  is examined; the unstated PyMOL `align` outlier-rejection behaviour; and the mismatch
  between "third-to-last residue" and "intracellular" for TM6 (see `unresolved`).

- **stance** (provisional; the user's call): **precedent on findings + contrast on rigour.**
  - *Precedent on findings:* it is independent, GPCR-specific evidence that vanilla AF2 and
    AF3 collapse toward the inactive basin, on n = 75 receptors across four classes, and it
    supplies the useful negative result that **AF3 is worse than AF2** on this axis (p8:
    AF3's deformation range "extending from approximately 0.8Å to 6Å"; p9: "the ∆H3-H6 values
    predicted by AF2 are consistently lower than those from AF3 for inactive GPCR
    conformations"). It makes no priority claim, so it competes with nothing.
  - *Contrast on rigour:* one prediction per target with no sampling; no threshold, no state
    predicate, and no statistical test of any kind — not a single correlation coefficient,
    p-value, mean or standard deviation appears in the paper; no memorisation control despite
    a training-data explanation being offered; ∆H3-H6 reported as an absolute value, discarding
    the direction the central claim depends on; template and MSA handling unreported; and the
    class-level conclusion drawn from a 16-receptor, all-Class-A subset while being stated as a
    result about "different GPCR classes" (p9).

## E. Quantitative comparators

- **metrics_reported**: The paper reports **ranges and orderings, never summary statistics**.
  No mean, median, standard deviation, correlation coefficient, p-value or per-target table
  appears anywhere in the 24 pages. Rows below marked "read from render" were measured off the
  150 dpi renders and should not be quoted to better than ±5% of the axis span.

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Average deformation, AF2, full range over the set | 0.25 – 2 | Å | 75 deposited PDB reference structures, 7-TM CA mean after PyMOL `align` | p8 (text), Fig 2a |
| Average deformation, AF3, full range over the set | ~0.8 – 6 | Å | same references, same metric | p8 (text: "extending from approximately 0.8Å to 6Å"), Fig 2b |
| ∆H3-H6, AF2, observed range | ~0.0 – 1.1 | nm | \|d_ref − d_pred\| of the TM3/TM6 third-to-last CA pair | Fig 2c, p8 (read from render; not stated in text) |
| ∆H3-H6, AF3, observed range | ~0.0 – 1.15 | nm | same | Fig 2d, p8 (read from render; not stated in text) |
| H3-H6 distance, A2A reference | 1.51 | nm | the deposited A2A structure itself (raw, not a difference) | Fig S1, p22 |
| H3-H6 distance, A2A, AF2 prediction | 1.48 | nm | ∆ = 0.03 nm vs reference | Fig S1, p22 |
| H3-H6 distance, A2A, AF3 prediction | 1.36 | nm | ∆ = 0.15 nm vs reference | Fig S1, p22 |
| Sequence overlap ratio, AF2 (AFDB) models vs references | > 96 | % | `Length of Overlapping Sequence / Length of Reference Sequence`, Biopython global alignment | p6; SI §1, p20–21 |
| Sequence identity, AF3 models vs references | 100 (identical) | — | stated, not measured | SI §1, p21 |
| Activity level axis span of the reference set | 0 – 100 | % | GPCRdb annotation of each reference | p5, p6; Fig 2 x-axis |
| Deformation colourbar span, AF2 t-SNE (16-receptor subset) | 0.50 – ~1.85 | Å | as Metric 1, on the 16-receptor GPCR-BERT subset | Fig 3a, p9 (read from render) |
| Deformation colourbar span, AF3 t-SNE (16-receptor subset) | ~1.4 – ~3.7 | Å | as above | Fig 3b, p9 (read from render) |
| Receptor set composition | 63 A / 6 B1 / 4 C / 2 F = 75 | receptors | PDB + GPCRdb | p6 |
| t-SNE subset size | 16 | receptors (~90 plotted points) | GPCR-BERT embedding set | SI §4, p23; Fig S2, p24 |
| Best / worst receptor, AF2 | best A2A / worst dopamine D1 | — | lowest / highest average deformation | p9, p11 |
| Best / worst receptor, AF3 | best A2A / worst serotonin 2A | — | lowest / highest average deformation | p9, p11 |

- **n_predictions**:
  - **Samples per target: 1, for both predictors.** AF2: one pre-computed AFDB model per
    receptor (p6: "The AF2 generated structures are obtained from the AlphaFold Protein
    Structure Database"). AF3: **NOT REPORTED** — p6 says only "AF3 generated structures were
    obtained from the AF3 server"; the number of seeds or models returned, and which one was
    analysed, are never stated. Every figure is consistent with one point per receptor per
    predictor.
  - **Targets: 75** (p6) for the deformation and ∆H3-H6 analyses; **16** (SI p23) for the
    t-SNE class analysis, plotted as ~90 points (Fig S2 render, p24).
  - **Total predictions analysed: 150** (75 AF2 + 75 AF3), of which the authors generated at
    most the 75 AF3 models; the 75 AF2 models were downloaded pre-computed.
  - **No repeated predictions, no seed variance, no ensemble** — so no error bar on any point
    in the paper is available even in principle.

- **comparable_to_ours**:

- **si_in_scope**: **SI HELD — it is bound into this PDF as pages 20–24** and contains
  §1 Dataset Preparation (the overlap-ratio definition, Eq. 1, and the PyMOL `align`
  statement), §2 with Figure S1 (the A2A H3-H6 illustration and its three numeric labels),
  §3 Calculation of Average Deformation (the five-step algorithm, which is the only place the
  seven TM regions are operationally defined), and §4 with Figure S2 (the t-SNE with the
  16-receptor legend). Nothing cited as SI is missing. **What *is* missing is not SI but
  data:** there is no per-target table anywhere — no PDB accession list, no per-receptor
  activity level, no per-receptor deformation or ∆H3-H6 value, and no residue numbers for the
  TM3/TM6 pair. p11 points to a repository instead: "The necessary information containing the
  codes and data used in this study is available here:
  https://github.com/garimachib01/GPCR_AlphaFold". That repository is not held by the corpus,
  so the identity of the 75 references and the exact H3/H6 residues are recoverable only from
  it. Record as **per-target data NOT IN PDF, deferred to GitHub**.

## F. Figures

Five figures (2 main-text data figures, 1 main-text schematic, 2 SI figures) split into
**6 panel-group rows**.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 4 | Workflow: reference PDB structure → extracted sequence → AlphaFold → superposition onto the reference → computation of average deformation and ∆H3-H6 | schematic | `SCHEMATIC \| pipeline from a deposited reference structure to its sequence, to an AlphaFold prediction, to PyMOL superposition, to the two metrics \| no data` | 1 unlettered panel, three stacked stages with a sequence excerpt and two structure cartoons as illustration | | NOT REPORTED — no licence statement anywhere in the PDF; arXiv v1 with no CC notice, so the arXiv default non-exclusive licence must be assumed and redistribution rights are not granted |
| 2A-B | 8 | Average CA deformation over the seven TM helices against GPCRdb activity level, for AF2 (a) and AF3 (b), coloured by receptor class | scatter | `PLOT \| facet: predictor (2: AF2, AF3) \| vary: activity level 0–100% (continuous) \| series: GPCR class (4: A, B1, F, C) \| measure: average deformation (Å) \| mark: point \| n: 1 per mark; ~75 per panel (75 stated on p6, never printed on the figure)` | 2 panels (a, b) varying by predictor; class encoded as a 4-entry colour+glyph legend inside each panel (blue circle A, orange square B1, green diamond F, red triangle C) | **y-axes are not shared and neither starts at zero** — panel a runs 0.25–2.00 Å, panel b runs ~1–6 Å, so the AF3 point cloud *looks* comparable to AF2's when its values are up to three-fold larger; the paper's central AF2-vs-AF3 comparison is exactly what this rescaling obscures. n is not printed on either panel. Class counts are extremely unbalanced (63/6/4/2, p6) but every class is drawn with equal visual weight, so a single Class C triangle at 6 Å reads as a class-level result. No trend line, no binned means, no correlation coefficient — the claimed activity-level trend has no quantitative summary anywhere | as above |
| 2C-D | 8 | Absolute difference in the TM3–TM6 intracellular CA–CA distance between reference and prediction, against activity level, for AF2 (c) and AF3 (d) | scatter | `PLOT \| facet: predictor (2: AF2, AF3) \| vary: activity level 0–100% (continuous) \| series: GPCR class (4: A, B1, F, C) \| measure: ∆H3-H6 (nm) \| mark: point \| n: 1 per mark; ~75 per panel (75 stated on p6, never printed on the figure)` | 2 panels (c, d) varying by predictor; same 4-entry class legend as 2A-B. Split from 2A-B because the measure differs (Å deformation vs nm distance difference), per the v3 rule | same absent-n and unbalanced-class problems as 2A-B; additionally the points pile up against the hard 0.0 nm floor of an absolute difference at low activity (see `metric_saturation`), and the sign of the H3-H6 error — the direction the inactive-collapse claim depends on — is discarded before plotting and appears nowhere. The x-axis is heavily clumped at 0% and 100% with a sparse middle, which the scatter does not communicate | as above |
| 3A-B | 9 | t-SNE of GPCR-BERT `[CLS]` embeddings for the 16-receptor subset, points coloured by average deformation, for AF2 (a) and AF3 (b) | scatter | `PLOT \| facet: predictor (2: AF2, AF3) \| vary: t-SNE dimension 1, −10 to ~13 (continuous) \| series: average deformation, continuous colourbar (AF2 0.50–~1.85 Å; AF3 ~1.4–~3.7 Å) \| measure: t-SNE dimension 2 \| mark: point \| n: 1 per mark; ~90 points per panel from 16 receptors (SI p23), per-panel n never printed` | 2 panels (a, b) varying by predictor; each carries its own vertical deformation colourbar and four hand-drawn red ellipses annotated "Rhodopsin", "A2A", "β1/β2 Adreno", "Dopamine D1" | **the two colourbars use different, non-overlapping ranges** (AF2 tops out near where AF3 begins), so the same colour means a different deformation in a vs b and the panels cannot be compared by eye — again on the paper's headline comparison. The caption says "Clusters represent distinct GPCR classes" but all four annotated clusters are individual **receptors**, and all four are Class A, so the figure does not show what it is captioned as showing; the class-level claim on p9 has no panel that supports it. The red ellipses are hand-drawn annotations, not a clustering result, and no clustering algorithm or cluster statistic is reported. Only 4 of ~16 receptor groups are labelled; the rest are unidentifiable. n per panel not shown, and the mismatch between "16 GPCRs" (SI p23) and ~90 plotted points is never explained | as above |
| S1 | 22 | Superposition of the reference (red), AF2 (green) and AF3 (yellow) A2A receptor at the intracellular TM3/TM6 region, with the three H3-H6 distances drawn as dashed lines | structure render | `RENDER \| facet: none (1) \| views: 1 (zoomed intracellular TM3/TM6 region of a single receptor) \| overlay: 2 predictions on 1 reference \| axis: none` | 1 unlettered panel; three superposed cartoon structures with three labelled dashed measurements (1.51 nm Ref, 1.48 nm AF2, 1.36 nm AF3) | a single hand-picked receptor, and it is the **best-performing** one in the whole study (p9: "the adenosine A2A receptor exhibited the lowest deformation values for both AF2 and AF3"), presented as the illustration of the metric with no statement that it is the best case. TM3 and TM6 are not labelled in the render and the measured residues are not identified, so the figure cannot be used to disambiguate the metric definition (see `unresolved` item 2). No scale bar | as above |
| S2 | 24 | The same t-SNE embedding as Figure 3, with points coloured by receptor identity instead of by deformation | scatter | `PLOT \| facet: none (1) \| vary: t-SNE dimension 1, −10 to ~13 (continuous) \| series: receptor identity (16: aa2ar, adrb2, ox2r, cnr1, 5ht2b, ntr1, drd1, adrb1, opsd, gpr52, cnr2, mtr1a, 5ht2a, cxcr4, nk1r, cltr2) \| measure: t-SNE dimension 2 \| mark: point \| n: 1 per mark; ~90 points per panel from 16 receptors (SI p23)` | 1 unlettered panel with a 16-entry colour legend and the same four red annotation ellipses as Figure 3 | caption again says "Clusters correspond to GPCR classes" while the legend is 16 individual receptors, all Class A. The 16-colour sequential-hue legend is not discriminable — several adjacent entries (drd1/adrb1/opsd/gpr52, cnr1/5ht2b/ntr1) are near-identical greens, so points cannot reliably be assigned to receptors. Points per receptor are not given, and the ~90-point count is not reconciled with the stated 16 GPCRs | as above |

**6 panel-group rows across 5 figures.** Renders taken of pages 8, 9, 22 and 24 — necessary
because none of the four captions carries axis identities, units, legend contents or colourbar
ranges (Figure 2's caption names only "average deformation" and "H3-H6 distances" with no
axes or class legend; Figure 3's caption gives neither the colourbar range nor the cluster
labels; Figure S2's caption gives neither the legend nor the point count). Figure 1's caption
on p4 fully describes the workflow and was not rendered.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), schema v3 batch
- **schema_version**: v3
- **confidence**: **high** for A, B, C and D — the paper is short, the methods are stated in
  one place, and the SI is held, so the two metric definitions could be quoted end to end
  rather than reconstructed. **High** for the figure table, with the caveat that all axis
  labels, legend contents and colourbar ranges come from renders rather than from the text
  layer. **Medium** for E, not because anything was hard to read but because the paper reports
  almost nothing quantitative: four of the fifteen rows are ranges eyeballed from a 150 dpi
  render, and no summary statistic of any kind exists in the paper to anchor them.
- **unresolved**:
  1. **Are the 75 "GPCRs" 75 unique receptors or 75 deposited structures?** p6 uses "GPCRs",
     "receptors" and "structures" for the same count. The activity axis is per-structure, and
     the t-SNE arm plainly has multiple points per receptor, so the two readings give
     materially different effective sample sizes. Cannot be settled from the PDF; the PDB
     accession list is only on GitHub (p11).
  2. **Which end of TM3 and TM6 the H3-H6 residues sit on — the definition is internally
     inconsistent, and this is the most important open item for reuse.** p5 says the two
     residues are "in the intracellular regions of the third and sixth transmembrane helices",
     but p7's operational rule is "the third-to-last residue in the third and the sixth TM
     region". Read literally, "third-to-last" selects the C-terminal end of each extracted
     segment. In a canonical 7TM topology the C-terminal end of TM3 is intracellular but the
     C-terminal end of TM6 is **extracellular**, so the literal rule contradicts the stated
     intent for TM6. Either "last" is meant with respect to some other ordering, or the
     segments are stored in a direction the paper does not describe. Figure S1 (p22) does not
     settle it: the view is cropped, the helices are unlabelled, and the dashed-line endpoints
     cannot be assigned to a terminus with confidence. **Anyone reusing this predicate must
     read the GitHub code rather than the paper.**
  3. **The source of the TM boundaries used for the p6 truncation is never stated.** The SI's
     "7 longest subsequences" rule (p22) operates on structures that are *already* truncated to
     the TM regions, so it inherits its boundaries from an earlier, undocumented step. No
     annotation source (GPCRdb, UniProt, OPM, Ballesteros–Weinstein) is named anywhere. Since
     both metrics are defined on these segments, the whole quantitative content of the paper
     rests on an undocumented boundary definition.
  4. **PyMOL `align` settings are not reported, and the default is not neutral.** SI p20 names
     the `align` tool but gives no parameters. PyMOL's `align` by default performs five cycles
     of outlier rejection at a 2.0 Å cutoff, which *removes* the worst-fitting residue pairs
     before converging the superposition. If defaults were used, the reported deformation is
     systematically lower than a straight all-TM-CA superposition would give, and the effect is
     larger for the worse-fitting active structures — i.e. it would flatten the very trend the
     paper reports. Whether `cycles=0` was set is unknowable from the PDF.
  5. **Two different residue correspondences are used and never reconciled.** The superposition
     uses PyMOL's own sequence alignment (p6, SI p20); the distances use a separate
     Biopython longest-subsequence + residue-name best-match correspondence (SI p22–23). They
     need not agree, and no check that they do is reported.
  6. **Which AF3 server output was analysed is not stated** (p6). The server returns multiple
     ranked models; no seed, count or selection rule is given. The AF2 arm has the mirror-image
     gap: AFDB models are pLDDT-top-ranked by DeepMind, which the paper does not mention.
  7. **Templates and MSA handling are entirely unreported for both arms** — the word "template"
     never appears, and "MSA" appears only as background on p3. For a paper whose conclusion is
     about training-data bias (p10), whether the reference structures were available as
     templates is a first-order question that is not addressed.
  8. **No statistical test, correlation coefficient, mean or standard deviation appears
     anywhere in the paper.** The activity-level trend, the AF2-vs-AF3 difference and the
     class differences are all asserted from the visual appearance of scatter plots. Nothing in
     the PDF permits an effect size to be quoted.
  9. **The ~90 points in Figures 3 and S2 are not reconciled with the stated 16 GPCRs**
     (SI p23). Presumably multiple deposited structures per receptor, but the paper never says,
     so the per-panel n is genuinely unknown.
  10. **No licence statement exists anywhere in the 24 pages** (verified by grep for "licen",
      "creative", "copyright", "CC BY"). This is an arXiv v1 with no CC notice, so the arXiv
      default non-exclusive distribution licence must be assumed: **no redistribution or
      derivative rights are granted**, and the figures should be treated as not redrawable
      without contacting the authors. Recorded in every `reuse` cell as NOT REPORTED rather
      than assumed permissive.
  11. **No tag was needed that does not exist in v3.** Nothing was invented. Two vocabulary
      *choices* were close calls and are documented under Tags below (`multi-backbone`,
      `apo-sampling`).
  12. **Schema ambiguity — the `multi-backbone` threshold excludes the commonest comparison.**
      The B-table rule is "If more than two are compared head to head, tag `multi-backbone`".
      This paper compares AF2 against AF3 head to head on an identical set with identical
      metrics, which is precisely what a reverse lookup for backbone comparisons wants to find,
      and it is excluded by one. Suggest v4 either lower the threshold to two or add a
      `backbone-comparison` tag; as written, the rule silently drops every two-way study.
  13. **Schema ambiguity — a t-SNE (or any embedding scatter) has no natural `measure`.** The
      dependent quantity of interest is the colour (deformation), while the two axes are
      arbitrary embedding coordinates carrying no units and no direction. Following the v3
      grammar literally puts t-SNE 2 in `measure:` and the scientifically meaningful variable
      in `series:`, which is defensible but inverts the usual reading of those slots and will
      not join sensibly against ordinary PLOT rows. Suggest v4 add an `EMBEDDING` form, or a
      rule that when both axes are unitless embedding coordinates the coloured variable takes
      `measure:` and the axes take `vary:`/`series:`.
  14. **Schema ambiguity — where a metric's *floor* belongs when the pile-up is only visible in
      a figure.** ∆H3-H6 is numerically bounded below at 0 (a `metric_saturation` matter under
      the v3 numeric-only rule), but the evidence that the population is actually resting on
      that bound is the density of points at 0.0 nm in Figure 2c–d, which is a figure
      observation. Both fields were written with a cross-reference rather than duplicating, per
      the v3 instruction, but the rule does not say which is canonical when the numeric fact and
      its only evidence live in different fields.
  15. **Schema ambiguity — `n_targets` has no slot for "the headline analysis and a secondary
      analysis use different sets".** 75 for the metrics, 16 for the class analysis, and the
      paper states class-level conclusions from the 16. Recorded as sub-bullets, which will not
      join against a single integer in `INDEX.md`.
- **why_it_matters**:

## Tags

`gpcr` `benchmark-only` `single-state` `rmsd-only` `continuous-metric` `saturating-metric`
`design-level-oracle` `no-anti-memorization` `apo-sampling` `preprint` `precedent` `contrast`
`negative-result` `comparator-numbers`

Tag notes, so the reverse lookups stay honest:
- **`oracle-leak` is deliberately NOT applied.** Routes 1–4 are clean: no coordinates, no
  state-annotated templates or alignments, no state-derived cluster labels, and nothing tuned
  at all. Only the post-hoc routes 5–7 fire, so `design-level-oracle` alone is correct. Applying
  `oracle-leak` here would false-positive a query intended to find pipeline contamination.
- **`rmsd-only` + `continuous-metric` together**, matching the dual `state_metric`. `rmsd-only`
  covers the average CA deformation (an RMSD-analogue against a held reference — though note it
  is a mean, not a root-mean-square). `continuous-metric` covers the TM3–TM6 distance, which is
  a genuine continuous activation coordinate even though the paper reports only its absolute
  difference to the reference. **`binary-predicate` is NOT applied** — the paper never calls a
  state on any prediction. **`visual-metric` is NOT applied** — Figure S1 is explicitly a
  "Demonstration" and no claim rests on visual state assignment.
- **`saturating-metric`** refers only to the 0 nm floor of ∆H3-H6 and the low-activity pile-up
  against it (Figure 2c–d, p8). Average deformation does not saturate.
- **`single-state`** — one AFDB model and one AF3 server model per receptor, no sampling, no
  seeds, no ensemble. `ensemble` and `continuum` are both wrong: the continuum in this paper is
  the reference set's activity axis, not the model output.
- **`no-anti-memorization`** — no held-out set, no date cutoff, no control arm, and a
  training-data explanation offered on p10 that is never tested. `unpowered` is not applied
  because there is no under-powered arm; there is no arm.
- **`apo-sampling`** — applied, but scoped. It is certain for the AF2 arm, which is by
  construction single-chain receptor-only AFDB models (p6). For the AF3 arm the input
  composition is **NOT REPORTED**: p6 says only that structures "were obtained from the AF3
  server", and SI p21 confirms only sequence identity, so whether any ligand or partner was
  co-folded is unstated. Applied on the strength of the AF2 arm and of the fact that no ligand,
  G protein, nanobody or mimetic is mentioned anywhere in the paper.
- **`multi-backbone` is NOT applied**, strictly following the v3 rule "more than two ... head to
  head". Exactly two (AF2, AF3) are compared. Flagged as a probable schema defect under
  `unresolved` item 12 — a reverse lookup for backbone comparisons will miss this paper.
- **Method tags other than `benchmark-only` are all absent by construction.** No `cofolding`,
  `msa-subsample`, `msa-state-filter`, `template-state-bias`, `af-cluster`, `latent-steering`,
  `md`, `md-emulator` or `enhanced-sampling` — the paper intervenes in nothing. `experimental`
  is also wrong: it marks a paper with no structure prediction in it, and this paper is
  entirely about structure prediction, just not about producing it.
- **No Protocol tag is applied.** `templates-on`, `no-template-no-msa` and
  `state-annotated-input` all require the paper to state its template/MSA regime, and it states
  none (see `templates`, `msa_handling`). Leaving these off is a positive statement that the
  regime is unknown, not an oversight.
- **No Control tag other than `apo-sampling`.** `directed-state`, `partner-driven`,
  `ligand-driven`, `peptide-driven`, `g-protein-mimetic`, `nanobody` and `seed-only` all require
  a handle on the prediction; there is none, not even a seed (see `directional_control`).
- **No Site tag.** The TM3–TM6 intracellular contact is the G-protein coupling interface, which
  is neither `orthosteric` nor an `allosteric-site` in the small-molecule sense the vocabulary
  uses, and no binding site is studied. `allosteric-failure` describes a sampling result that
  this paper does not report.
- **`negative-result`** — the paper's substantive finding is a failure mode of AF2 and AF3 on
  active conformations, and specifically that AF3 is *worse* than AF2 on both metrics (p8, p9).
- **`comparator-numbers`** — applied for the deformation and ∆H3-H6 ranges and the A2A H3-H6
  triplet, which are directly quotable, while noting that the paper offers no mean, no
  distribution and no per-target values, so the comparators are ranges only.
- **`figure-exemplar` is NOT applied** — the figures carry real defects (unshared and non-zero
  y-axes, mismatched colourbars, captions describing something other than what is plotted) and
  should not be recommended as design templates.
- **`experimental-validation` is NOT applied** — no wet-lab work of any kind.
- **`confidence-as-discriminator` is NOT applied** — pLDDT, pTM and PAE are never mentioned.
