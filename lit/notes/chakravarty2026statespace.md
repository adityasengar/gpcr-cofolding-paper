# chakravarty2026statespace

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` with a reason where the field presupposes a primary study this document is not.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–29), which for this preprint
coincide with the printed page numbers.** Layout: p1 title/affiliations, p2 abstract + Section I,
p3 Fig 1 + rest of Section I, p4–7 Section II (2.1–2.5), p7–9 Section III, p9–14 Section IV
(4.1 alternative-state sampling, 4.2 energetic refinement, 4.3 experiments), p14–18 Section V
(5.1 conditioning on context, 5.2 evaluation strategies) + Conclusion, p18 Code/Data +
Acknowledgements, p19–29 references (122 entries). Figures: Fig 1 p3, Fig 2 p5, Fig 3 p11,
Fig 4 p16. **No tables, no supplementary material, no appendix.**

**DOCUMENT TYPE — settled from the paper itself, not assumed.** This is a **perspective /
review**, not a primary study. Evidence, all internal:
- p2 abstract: "Here, we **argue** that structure prediction should be reformulated as a
  state-space inference problem… We **review** emerging strategies—deep learning ensemble
  generators, physics-based simulations, and experimental constraints—and **outline a roadmap**
  toward state-space prediction."
- p3: "In **this perspective**, we propose that the objective of protein structure prediction
  must shift…"
- p4 (roadmap of the document): "We first identify the biological and physical boundary
  conditions… (Section II), discuss the importance… (Section III), and **review** current
  approaches… (Section IV). Finally, we outline a roadmap… (Section V)".
- p18, section heading: "Conclusion and **Perspective**".
- There is **no Methods section, no Results section, no data table, and no statistical test
  anywhere in the 29 pages.** Every quantitative statement carries a citation to another paper.
- The only artefact of the authors' own making is a figure-generation repository, p18: "All code
  and data used to generate figures can be found at:
  https://github.com/DevlinaC/expanding-protein-structure-prediction-figures".

Consequently **Section C is almost entirely NOT APPLICABLE**, and is marked so with the reason
each time rather than being filled with a manufactured benchmark reading. What the paper does
supply in place of a benchmark — a set of *prescribed* evaluation criteria — is recorded in full
under `state_metric`, `anti_memorization_design` and section D, because those prescriptions are
the actionable content.

**Scope discipline note:** the corpus already holds `waymentsteele2024cluster`,
`schafer2025confounds` and `waymentsteele2025reply` as separate entries. This note extracts only
what *this* document says; it does not adjudicate that exchange. Where this paper cites its own
authors' prior work (refs [59], [85]), that is recorded as a citation made by this paper, nothing
more.

---

## A. Identity

- **citekey**: `chakravarty2026statespace`
- **doi**: **arXiv:2608.02866v1** — stamped in the left margin of p1: "arXiv:2608.02866v1
  [q-bio.BM] 3 Aug 2026". `refs.bib` records `doi = {10.48550/arXiv.2608.02866}`, which is the
  standard arXiv-minted DOI for that identifier. No journal DOI appears anywhere in the PDF.
- **year**: **2026** (posted 3 Aug 2026, p1).
- **venue**: **arXiv preprint, q-bio.BM, not peer reviewed.** p1 margin stamp is the only venue
  statement in the document; there is no journal name, no submission notice, no "under review"
  line. Tagged `preprint`. The manuscript is typeset in the Springer Nature `sn-jnl` style
  (numbered sections I–V, "Fig. 1" caption style, Nature-style reference formatting), which
  suggests an intended journal submission, but the PDF never names one — do not infer.
- **title**: Expanding Protein Structure Prediction into Conformational State Space — p1
- **authors**: Devlina Chakravarty, Justin J. Miller, Da Teng, Yousuf O. Ramahi, Patrick Bryant,
  Camila Neira-Mahuzier, César A. Ramírez-Sarmiento, Sarah Rauscher, Gregory R. Bowman,
  Pratyush Tiwary, **Lauren L. Porter** (corresponding, porterll@nih.gov) — p1. Eleven authors
  across twelve affiliations: NLM/NIH and NHLBI (Chakravarty, Porter), UPenn Biochemistry and
  Biophysics (Miller, Bowman), Maryland Institute for Health Computing / Chemistry and
  Biochemistry / IPST (Teng, Tiwary), Toronto Mississauga and Toronto Chemistry/Physics
  (Ramahi, Rauscher), Stockholm University Molecular Biosciences (Bryant), Pontificia
  Universidad Católica de Chile / Millennium Institute iBio (Neira-Mahuzier,
  Ramírez-Sarmiento). **This is a multi-lab consensus document, not a single-group position
  paper** — the author list spans the fold-switching group (Porter/Chakravarty), the
  cryptic-pocket/MD group (Bowman/Miller), the hybrid DL–MD group (Tiwary/Teng), and an
  AlphaFold-methods author (Bryant). Record that: it raises the weight the framing carries.

## B. Scope

- **system**: **general protein.** The argument is explicitly kingdom- and fold-agnostic; the
  paper enumerates worked examples spanning many system classes to demarcate *boundary
  conditions*, not to study any one of them. Examples named, with pages:
  - adenylate kinase (domain closure, rate-limiting step) — p4, Fig 2b p5
  - excitatory amino acid transporter, EAAT (rigid-body outward↔inward) — p4, Fig 2b p5
  - µ-opioid receptor (ligand-dependent side-chain rotamer populations, G protein vs
    β-arrestin priming) — p4 — **the only GPCR in the paper, one sentence**
  - Ebola viral protein 35 interferon inhibitory domain (cryptic pocket controlling RNA
    binding) — p6, Fig 2b p5
  - KRAS (cryptic pocket, first FDA-approved KRAS inhibitor) — p6
  - F7 pyocin central tail fibre, 163-residue coiled-coil → β-prism fold switch — p6, Fig 2b p5
  - S100 / S100β EF-hand calcium switch — p7, Fig 2b p5
  - influenza A M2 proton channel His37 tetrad; EmrE proton-coupled transporter — p7
  - anti-HIV antibody 10E8 proline cis–trans isomerisation (minutes–hours kinetic
    bottleneck) — p7
  - BCCIP isoforms; pro-interleukin-18; DZZB; MP20 — p8
  - XCL1, KaiB, Mad2, RfaH, prion protein (dual-basin structure-based models) — p12
  - kinases (DFG motif, type-II inhibitor selectivity, Potts models) — p13, p18
  - GlyT1 and plasmepsin-II as *failure* cases of BioEmu-seeded MSM — p13
- **n_targets**: **NOT APPLICABLE — no targets were studied.** The document runs no predictions.
  Counting the illustrative examples above gives roughly 20 named proteins across p4–p18, all
  cited to other publications. **Generality flag is inverted here relative to the usual case:**
  the paper claims full generality and studies nothing, so there is no single-system-claiming-
  generality defect to flag, but equally no evidence generated in support.
- **method_class**: **other — perspective / review + roadmap.** Not `benchmark-only`: no
  benchmark is run, no method is scored, no head-to-head comparison is performed by these
  authors. The document *surveys* co-folding, MSA-subsampling, clustering, MD, enhanced
  sampling and MD-emulator families (Section IV, p9–14) and *prescribes* a research programme
  (Section V, p14–18).
- **backbones**: **NOT APPLICABLE — none run.** Backbones *discussed*: AlphaFold2 and
  AlphaFold3 throughout; ESMFold (p8); and, named in the Fig 3 "Single structure prediction"
  column on p11 (visible only in the rendered figure, not in the caption text): AlphaFold2,3 /
  OpenFold2,3 / RoseTTAFold / ESMFold2. Downstream/derived systems discussed: AlphaFlow,
  AF-cluster, AFSample2, SPEACH-AF, CF-random, BioEmu, DiG, AF2-RAVE, NeuralPLexer,
  RoseTTAFold All-Atom, DEERFold, AlphaLink2. **Do not tag `multi-backbone`** — nothing was
  compared head to head by these authors.
- **templates**: **NOT APPLICABLE — no predictions run.** The word "template" does not appear in
  the paper in the structure-prediction sense.
- **msa_handling**: **NOT APPLICABLE for the authors' own work — none run.** MSA handling
  *reviewed*, and the paper keeps the distinctions the schema cares about reasonably clean:
  - *subsampled* (depth reduction): p9, del Alamo et al. — "stochastic MSA subsampling could
    expose conformations otherwise suppressed by the dominant MSA signal [75]".
  - *clustered*: p9, AF-cluster [76] named; separately, frustration-based clustering [78] —
    "methods based on local energetic frustration have identified alternative conformations by
    clustering sequences according to their average frustration".
  - *column masking / conservation-profile masking*: p9, "masking conservation profiles" —
    SPEACH-AF [80].
  - *targeted MSA editing* (closest thing in this paper to state-filtering): p10, Clore and
    colleagues — "targeted MSA editing enables both AlphaFold2 and AlphaFold3 to recover a
    pro-IL-18 conformation similar to experiment without prior structural knowledge [84]".
  - *full MSA as the failure mode*: p8, "Because current prediction models rely heavily on
    multiple sequence alignments (MSAs), similar sequences frequently produce similar structural
    priors even when they experimentally occupy different conformational basins [58]".

## C. Conformational core

**Blanket reason for this section:** this document generates no structures, runs no pipeline,
scores no prediction and holds out no set. Every field below whose meaning presupposes a run is
marked `NOT APPLICABLE` with that reason restated, rather than being filled by transcribing
results the paper cites from elsewhere. Where the paper *prescribes* something for this axis,
the prescription is recorded under the field it prescribes for and labelled **PRESCRIBED, not
performed**.

- **states_generated**: **NOT APPLICABLE — perspective; no structures generated, no predictor
  run.** The paper's *target* object is defined at p2–3 and is the thing it argues should be
  generated: "recovering not one conformation's coordinates but accessible states, their
  energetic and kinetic relationships, context dependence, and responses to perturbations" (p2).
  Fig 1's right inset (p3) explicitly declines to fix a single topology: "state spaces range
  from a single dominant basin, to a small number of discrete alternative basins, to a
  continuous ensemble of interconverting conformations, and a general framework must accommodate
  this full range of topologies."

- **structural_priors_used**: **Deposited experimental structures, used for illustration only —
  no methodological sin, and no pipeline for one to enter.**
  - Fig 2b (p5) is built from deposited experimental structures of five systems in two states
    each: adenylate kinase apo / +Ap5A; EAAT inward-facing / outward-facing; Ebola VP35 closed /
    open; S100β apo / +calcium; F7 pyocin pre-ejection / post-ejection. Specific PDB accessions
    are **NOT REPORTED** — no accession codes appear anywhere in the paper or in the Fig 2
    caption.
  - p4 reports TM-scores for the EAAT transport / scaffold / core partition (0.608 / 0.834 /
    0.897) citing [27, 28], which are the *structure* papers (Boudker 2007; Yernool 2004), not
    TM-score papers. **These three numbers may therefore have been computed by these authors from
    deposited coordinates for this perspective.** The text does not say. See `unresolved`.
  - The figure-generation repository (p18) is the only place the underlying inputs could be
    checked, and it is outside the corpus.
  - **Design-time prior at the level of the argument itself:** every boundary condition in
    Section II is instantiated by a system whose alternative states are *already deposited or
    already experimentally characterised*. That is appropriate for a review — the point is
    demarcation, not prediction — but it is worth recording that the paper's evidence base for
    "single structures are insufficient" is entirely the set of cases where the second state is
    already known.

- **oracle_leakage**: **NOT APPLICABLE — there is no pipeline into which deposited-structure
  knowledge could leak.** All seven routes answered separately, per schema, with the page where
  the absence is checkable:
  1. *Structures as input or template* — **NOT APPLICABLE.** No prediction is run. Deposited
     structures appear only as figure renders (Fig 2b, p5). Protocol section that would describe
     any such use: **there is none** — the document has no Methods; the closest thing is the
     Code and Data statement, p18.
  2. *State annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates or
     alignments* — **NOT APPLICABLE, and none of these databases is mentioned anywhere in the
     paper.** Verified across all 29 pages.
  3. *Cluster labels derived from known states* — **NOT APPLICABLE.** Clustering is discussed as
     other people's method (p9) and never performed here.
  4. *Hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states* —
     **NOT APPLICABLE.** No hyperparameter of any kind is set in this document. Note that the
     paper explicitly *warns* about the analogous defect in others' work, p17: benchmark splits
     must "separate alternative states across training and evaluation splits to ensure genuine
     generalization [119], rather than memorization of a training-set-dominant basin."
  5. *Success defined post hoc by RMSD or TM to a structure they had* — **NOT APPLICABLE for
     this paper's own work.** It is, however, the practice the paper condemns as an evaluation
     standard, p17: "Traditional metrics such as RMSD and TM-score reward recovery of a single
     dominant fold and are poorly suited to assessing multi-state behavior."
  6. *Best/worst model labels assigned against a held reference* — **NOT APPLICABLE.** No model
     selection performed. The paper attacks the confidence-based version of this practice at
     p10 and p14 (see `confidence_as_discriminator`).
  7. *Design-level oracle use — inputs or systems chosen because the expected answer is already
     known* — **PRESENT AT REVIEW LEVEL ONLY, and it is not a defect here, but record it.** Two
     distinct things:
     (a) The paper's own illustrative systems are all cases with known second states
     (`structural_priors_used` above). For a demarcation argument that is legitimate.
     (b) **The paper states design-level oracle dependence as a property of the entire
     alternative-state-sampling field**, p9, verbatim: "Overall, these methods are most effective
     when biochemical, biophysical, or evolutionary evidence already suggests the existence of
     alternative conformations and the goal is to recover a specific non-dominant state [81]."
     That sentence is the paper's compressed statement of route 7 applied to the whole field and
     is the single most consequential line in the document for anyone making a multi-state
     prediction claim.

- **prospective**: **NOT APPLICABLE — nothing was predicted, so nothing can be prospective or
  retrospective.** The paper does discuss prospectivity as a standard it wants met: p14,
  "Structures generated by DL are best seen as hypotheses about potential basins within a
  conformational landscape", i.e. it treats the entire current output class as hypothesis-
  generating rather than as established prediction.

- **state_metric**: **NOT APPLICABLE for measurement performed; PRESCRIBED in detail.** The
  paper's prescription is the single most actionable passage in the document and is quoted in
  full under `necessity_claims` (E1). In field terms, what it asks for:
  - **Rejects** RMSD-to-reference and TM-score as sufficient state metrics (p17).
  - **Requires** three things instead (p17): (i) "recovery of experimentally validated
    alternative conformations"; (ii) "discrimination between competing basins"; (iii)
    "sensitivity to perturbations such as mutation, ligand binding, or the contextual factors
    described above (experimental restraints, environmental condition, splice isoform)".
  - **Requires population/energetic quantities**, not just geometry — p10: current methods
    "generate candidate conformational states without explicitly estimating their thermodynamic
    populations or kinetic accessibility" (p9); the target quantities are named in Fig 4 (p16)
    as ΔG and ΔG‡.
  - **Explicit thresholds: NOT REPORTED.** The paper prescribes no numeric cut-off for any of
    these criteria — no RMSD threshold, no population-error tolerance, no TM-score bar. That is
    a real gap in the prescription and should be recorded as such.
  - It points at existing efforts as partial exemplars, p17: "Recent benchmarking efforts
    comparing simulation- and AI-based estimates of cryptic pocket probabilities to experimental
    measurements of these thermodynamic quantities are a good step in this direction [99, 120]"
    (refs = PocketMiner, Meller et al. Nat Commun 2023; and Zhang, Miller & Bowman, JCTC 2026 —
    the latter co-authored by two authors of this perspective).

- **metric_saturation**: **NOT APPLICABLE — no metric is computed in this document, so nothing
  can floor or ceiling.** The paper does make the adjacent *conceptual* point that coordinate
  similarity is insensitive where it matters, p10: "mutations that experimentally shift
  conformational equilibria often produce little visible structural change, indicating that
  coordinate similarity alone cannot be interpreted as evidence that the underlying
  conformational landscape is unchanged [86, 87]." That is an argument about metric
  insensitivity, not numeric saturation of a reported arm.

- **directional_control**: **NOT APPLICABLE for the authors' own work.** Handles *reviewed*, each
  with the page:
  - **Experimental distance restraints** — DEER via DEERFold (p9, p15); crosslinking MS via
    AlphaLink2 (p9, p15). p15: DEERFold "incorporates distance distributions from Double
    Electron–Electron Resonance (DEER) spectroscopy directly into the network, guiding sampling
    toward conformations consistent with experimentally observed ensembles [68]".
  - **Binding partners / ligands / ions / PTMs, via co-folding** (p13): NeuralPLexer,
    RoseTTAFold All-Atom, AlphaFold3.
  - **Targeted MSA editing** (p10, Clore et al. [84]).
  - **Splice isoform as an intrinsic sequence handle** (p15–17).
  - **An external potential in targeted MD** (p11) — the only genuinely *directed* handle in the
    review: "targeted MD simulations, apply an external potential to promote structural
    interconversion between two states."
  - **Missing from the review entirely: latent steering.** No inference-time intervention on a
    pair representation, trunk embedding, distogram head or conditioning embedding is mentioned
    anywhere in the 29 pages. See the method-family table under `stated_limits`.

- **anti_memorization_design**: **NONE — and NOT APPLICABLE, because no set is held out for a
  run that does not exist.** What the paper *prescribes* (p17, verbatim) is precisely an
  anti-memorization design and is the sentence our own held-out design will be measured against:
  "Benchmark datasets must therefore include proteins with known conformational heterogeneity and
  separate alternative states across training and evaluation splits to ensure genuine
  generalization [119], rather than memorization of a training-set-dominant basin."
  Note the specific form demanded: **the split is across alternative states of the same protein**,
  not merely across proteins or across a date cutoff. No n is specified, no cutoff date is
  specified, and no candidate protein list is supplied. **PRESCRIBED, not performed.**

- **anti_memorization_control**: **NONE RUN.** No control arm of any kind exists in this
  document. The paper cites others' memorization findings rather than running one — p8: "Likewise,
  large-scale analyses of fold-switching proteins demonstrate that current predictors frequently
  fail to identify alternative conformations outside their training distributions [59]" (ref [59]
  = Chakravarty et al., *AlphaFold predictions of fold-switched conformations are driven by
  structure memorization*, Nat Commun 15:7296 (2024) — this paper's own first author).

- **controls_run**: **NOT APPLICABLE — no experimental or computational arm was run, therefore
  no control arm exists.** Table left empty deliberately rather than populated with controls
  performed in cited papers, which would misattribute them.

  | control | what it rules out | page |
  |---|---|---|
  | — none run — | — | — |

- **confidence_as_discriminator**: **The paper argues explicitly AGAINST using pLDDT/pTM as a
  conformational discriminator, and this is one of its clearest prescriptive positions.** Two
  passages, both verbatim:
  - p10: "Metrics such as pLDDT and pTM quantify internal geometric consistency rather than
    thermodynamic stability or kinetic accessibility. Consequently, experimentally validated
    alternative conformations may receive low confidence, whereas highly confident predictions
    can simply reflect agreement with dominant evolutionary priors or training data rather than
    biologically populated states [85]."
  - p14: "One major opportunity is improvement of confidence metrics. Current metrics primarily
    assess structural self-consistency based on learned priors and training data, rather than
    thermodynamic stability or basin occupancy. Consequently, structures with high confidence may
    reflect dominant training-set conformations without indicating their energetic plausibility
    [61, 81]. Landscape-aware prediction, therefore, requires methods that estimate basin
    stability and distinguish metastable conformations from transient or artifactual states."
  - No validation of confidence-as-discriminator is performed here (none could be); the position
    is asserted with citations. Ref [85] is Schafer et al., *Sequence clustering confounds
    AlphaFold2*, Nature 638:E8–E12 (2025) — already a separate corpus entry.

## D. Claims

- **central_conclusion**: Structure prediction has largely solved the single-dominant-conformation
  problem and should now be reformulated as inference of a *conformational state space* —
  the set of accessible states, their populations, the energetic and kinetic relationships among
  them, their dependence on biological context, and their response to perturbation — conditioned
  on both sequence and context, p(X | S, C). Current multi-state methods recover complementary
  *fragments* of that object (candidate states, approximate energetics, context-conditioned
  structures) but none recovers the whole, and none should be read as delivering it; progress
  requires integrating generative DL, physics-based free-energy methods and ensemble-sensitive
  experiment, with evaluation standards and benchmarks rebuilt to match the new objective.

- **necessity_claims**: **Verbatim + page.** Grouped by what they do, because this is the field
  most likely to be quoted back at us. Bold added by the extractor for emphasis; wording is
  exactly as printed.

  **E1 — Evaluation standards and generalisation vs recall. This is the load-bearing passage
  for our manuscript.** p17, §5.2, in full and in order:
  > "Finally, evaluation strategies must align with this expanded objective. Traditional metrics
  > such as RMSD and TM-score reward recovery of a single dominant fold and are poorly suited to
  > assessing multi-state behavior. Landscape-aware evaluation should instead measure recovery
  > of experimentally validated alternative conformations, discrimination between competing
  > basins, and sensitivity to perturbations such as mutation, ligand binding, or the contextual
  > factors described above (experimental restraints, environmental condition, splice isoform).
  > **Benchmark datasets must therefore include proteins with known conformational heterogeneity
  > and separate alternative states across training and evaluation splits to ensure genuine
  > generalization [119], rather than memorization of a training-set-dominant basin.** Recent
  > benchmarking efforts comparing simulation- and AI-based estimates of cryptic pocket
  > probabilities to experimental measurements of these thermodynamic quantities are a good step
  > in this direction [99, 120]"

  **E2 — Recall of a state the field already knows about is what current methods do.** p9:
  > "Overall, these methods are most effective when biochemical, biophysical, or evolutionary
  > evidence already suggests the existence of alternative conformations and the goal is to
  > recover a specific non-dominant state [81]. While they produce valuable structural
  > hypotheses, they ultimately loosen the single-state objective rather than redefining it.
  > Collectively, these methods can sometimes recover accessible conformational states, but not
  > their energetic organization or biological relevance (Figure 3)."

  **E3 — What the class of methods IS, stated as a category limit.** p10:
  > "Consequently, these methods are best viewed as generators of candidate conformational
  > states rather than predictors of conformational state spaces. Recovering the energetic
  > organization of those states requires additional physical modeling, discussed next."

  **E4 — What the field HAS achieved.** p2 (abstract):
  > "Recent AI advances have enabled protein structure prediction at near-experimental accuracy,
  > largely solving the problem of identifying a dominant conformation from sequence."

  p18 (Conclusion):
  > "Protein structure prediction has achieved a major milestone: accurately identifying a single
  > dominant conformation is no longer the main obstacle. The real challenge now is conceptual."

  **E5 — What the field has NOT achieved.** p14:
  > "Despite these advances, no single computational strategy yet provides a complete description
  > of conformational state spaces."

  Fig 3 caption, p11:
  > "Current computational and experimental approaches provide progressively richer
  > representations of conformational state spaces, but no single method yet recovers the
  > complete biological landscape."

  Fig 3 caption, p11 (closing sentence):
  > "…but integrating these components into a unified state-space predictor remains the central
  > challenge."

  **E6 — Necessity of experiment for validation.** p14:
  > "Ensemble-sensitive experimental techniques—including NMR, HDX-MS, SAXS, cryo-EM
  > classification, single-molecule methods, and mutational analyses—remain essential for
  > validating computationally predicted landscapes and characterizing them independently.
  > Structures generated by DL are best seen as hypotheses about potential basins within a
  > conformational landscape."

  p14:
  > "Until predictors directly recover complete conformational landscapes, ensemble-aware
  > interpretation of computational predictions will remain essential (Figure 3)."

  p14 (the division of labour it prescribes):
  > "Ultimately, deep learning, molecular dynamics, and experiment should be viewed as
  > complementary components of a single iterative framework: deep learning proposes candidate
  > states, physics estimates their energetic organization, and experiments establish their
  > biological relevance."

  **E7 — Impossibility claims: what a single-structure objective cannot do even in principle.**
  p6:
  > "In such cases, the single-structure objective fails not because of prediction error, but
  > because the target itself requires at minimum two divergent answers."

  p17:
  > "Each context source acts on p(X | S, C ) in a way a single-structure objective cannot
  > represent even in principle… A predictor recovering only X has no mechanism for any of these
  > effects, whereas one built around p(X | S, C ) can absorb all three as conditioning inputs
  > rather than special cases."

  p17 (splicing):
  > "it can generate structural states entirely absent from training data, which models that
  > assume one canonical sequence per gene are structurally incapable of recovering."

  p6:
  > "In fold-switching or metamorphic proteins, the same or nearly identical sequence can adopt
  > multiple stable folds with different secondary structures, demonstrating that the
  > sequence-single structure mapping is inherently flawed."

  **E8 — Confidence metrics must not be used as conformational discriminators.** p10 and p14,
  quoted in full under `confidence_as_discriminator`. The necessity form, p14:
  > "Landscape-aware prediction, therefore, requires methods that estimate basin stability and
  > distinguish metastable conformations from transient or artifactual states."

  **E9 — Coordinate similarity is not evidence of an unchanged landscape.** p10:
  > "Likewise, mutations that experimentally shift conformational equilibria often produce little
  > visible structural change, indicating that coordinate similarity alone cannot be interpreted
  > as evidence that the underlying conformational landscape is unchanged [86, 87]."

  **E10 — Starting-structure dependence as a necessity constraint on sampling and MD.** p10:
  > "This example highlights an important limitation shared by many sampling-based methods: the
  > quality of the sampled ensemble depends fundamentally on the correctness of the starting
  > structure."

  p12:
  > "A major limitation of MD, however, is its dependence on the starting structure [101].
  > Simulations initiated from inaccurate structural models may require microseconds of sampling
  > simply to relax toward experimentally observed conformations. Consequently, the quality of
  > conformational landscape reconstruction depends critically on both the accuracy of the
  > initial model and the environmental conditions under which simulations are performed."

  **E11 — Context must be a first-class input, not a post hoc correction.** p15:
  > "But the landscape is not fixed: it is reshaped by the conditions C under which a protein
  > exists, and next-generation predictors must treat these conditions as first-class inputs
  > rather than post hoc corrections."

  p9:
  > "Biological context provides critical information that cannot be inferred from sequence
  > alone."

  **E12 — Kinetics, not only thermodynamics, must be a prediction target.** p7:
  > "Predictive models should also have dynamics, barrier heights and timescales of functionally
  > relevant motions as their targets, not only static structures or multi-state predictions."

  p7:
  > "Across these regimes, thermodynamic stability alone does not determine biological relevance."

  **E13 — Training data as the structural cause of the limitation.** p2:
  > "Although the Protein Data Bank (PDB) contains more than 250,000 structures, it is heavily
  > biased toward stabilized conformations, with relatively few experimentally characterized
  > alternative states [12, 13]."

  p15:
  > "This objective reflects the training data: stable, experimentally accessible conformations
  > deposited in the PDB, with only a few entries explicitly showing alternative states. Even
  > when multiple conformations are present for the same protein in the training set, they are
  > usually treated as separate training examples rather than as parts of a shared conformational
  > landscape."

  **E14 — The reframing itself, stated as an obligation.** p3:
  > "In this perspective, we propose that the objective of protein structure prediction must
  > shift from recovering the coordinates of a single conformation to inferring a conformational
  > state space."

  p3:
  > "The next breakthrough will come not from improving coordinate accuracy of a single
  > conformation, but from predicting how sequences encode the dynamic organization of accessible
  > states across biological contexts."

  p18:
  > "While single-structure prediction has largely solved the problem of coordinate accuracy, the
  > next breakthrough will be measured not in angstroms, but in our ability to infer
  > conformational state spaces and the biological mechanisms they encode."

  p2 (the reframed question, verbatim including the paper's own inconsistent quotation marks):
  > "The central question is thus no longer 'What is the structure? ” but “What structural
  > ensemble of states does this sequence encode, under what conditions, with what populations,
  > and how do they interconvert? ” (Figure 1)"

- **novelty_claims**: **NO FIRST/NOVEL/UNPRECEDENTED CLAIM IS MADE.** Searched all 29 pages. The
  paper never claims to be first at anything, and never claims priority. The strongest
  self-positioning statements are proposals, not priority claims, and are recorded under E14
  above ("we argue", p2; "we propose", p3; "we outline a roadmap", p2). The only occurrences of
  "first" in the document refer to other people's work — p6, "the first FDA approved KRAS
  inhibitor"; p13, "Current co-folding methods represent the first generation of context-aware
  predictors"; p9/p12, "a first boundary condition"/"the first step". **This is itself worth
  recording: a perspective that makes no novelty claim cannot be cited against us on priority,
  only on standards.**

- **stated_limits**: The paper states limits of *the field*, extensively, and one limit of
  itself. Recorded as a per-family table because that is the requested and most reusable form.

  **Self-limit (the only one):** p14, on the epistemic status of everything it surveys —
  "Structures generated by DL are best seen as hypotheses about potential basins within a
  conformational landscape." And, on the MD data it advocates as training material, p14:
  "one runs the risk of either having MD trajectories that are too short and unintentionally
  biased due to simulation setup, or having an explosion of perhaps petabytes or more of MD
  trajectories."
  **The document contains no "limitations of this perspective" paragraph.** No statement that
  the roadmap is speculative, no acknowledgement that the six-component cycle of Fig 4 is
  untested, and no discussion of whether state-space prediction is achievable. Record that
  absence.

  **How the paper characterises each existing method family, with its specific criticism:**

  | family | how characterised (page) | specific criticism, verbatim where it bites (page) |
  |---|---|---|
  | **MSA subsampling** (del Alamo [75]) | "Because AlphaFold2 behaves almost deterministically for a fixed multiple sequence alignment (MSA), del Alamo et al. demonstrated that stochastic MSA subsampling could expose conformations otherwise suppressed by the dominant MSA signal" (p9) | Not criticised individually. Falls under the class-wide criticisms E2/E3: "they ultimately loosen the single-state objective rather than redefining it" and "can sometimes recover accessible conformational states, but not their energetic organization or biological relevance" (p9). Also listed as a *current* (not future) capability in Fig 3 column 2 (p11) |
  | **Sequence clustering / AF-cluster** [76] | Named once, p9, only inside a ranking sentence: "Among AlphaFold2-based approaches, CF-random [77] outperformed AFSample2 [79], AF-cluster [76], and SPEACH-AF [80] in predicting domain reorientations, local conformational changes, and fold switching" | **No standalone criticism of AF-cluster is made in this document.** It is placed last-equal in a three-way loss to CF-random, and that is all. The clustering critique is present only by citation: ref [85], Schafer et al. *Sequence clustering confounds AlphaFold2*, is cited on p10 in support of the confidence-metric argument, not as an attack on clustering. Fig 3 (p11) lists "AFCluster" as a current method alongside CF-random and AFSample2,3, i.e. it is not excluded. **The paper does not re-litigate the AF-cluster dispute** |
  | **Column masking / conservation-profile masking** (SPEACH-AF [80]) | "perturbing AlphaFold-class predictors through strategies such as masking conservation profiles, MSA subsampling, or stochastic sampling [75–77]" (p9) | Same as AF-cluster: named only as outperformed by CF-random (p9). No mechanism-level criticism |
  | **Frustration-based sequence clustering** [78] | "methods based on local energetic frustration have identified alternative conformations by clustering sequences according to their average frustration, successfully recovering rigid-body domain motions and fold-switching transitions" (p9) | None stated. Described favourably |
  | **CF-random / sequence association** [77] | The paper's evident preferred sampler: "outperformed AFSample2 [79], AF-cluster [76], and SPEACH-AF [80]… and was subsequently applied to large-scale prediction of fold-switching proteins in the E. coli proteome, suggesting that up to 5% of proteins may undergo fold switching" (p9) | None stated. **Note for us: this is a favourable characterisation of a method by a paper several of whose authors are in the CF-random / AF-cluster-critique lineage; it is asserted, not re-benchmarked here** |
  | **AFSample2** [79] | Named only in the ranking sentence, p9; listed in Fig 3 as "AFSample2,3" (p11) | Outperformed by CF-random (p9). Nothing further |
  | **Backbone choice for alternative states** | "Early methods adapted AlphaFold2, which generally outperforms AlphaFold3 for alternative-state prediction[59]" (p9) | An explicit, citable claim that **AF2 > AF3 for alternative states**, sourced to the authors' own ref [59] |
  | **Architecture/objective modification — AlphaFlow** [82] | "modeling conformational fluctuations around an input structure. It successfully recovered experimentally observed minor states of human pro-interleukin-18 (pro-IL-18) when initialized from the experimentally determined structure" (p9–10) | Starting-structure dependence, E10 (p10). And the concrete failure: "AlphaFold2, AlphaFold3, and BioEmu… generated starting conformations that differed from the experimentally observed pro-IL-18 structure by more than 20 Å, preventing subsequent sampling from recovering the experimentally observed ensemble" (p10) |
  | **Targeted MSA editing** (Clore et al. [84]) | "targeted MSA editing enables both AlphaFold2 and AlphaFold3 to recover a pro-IL-18 conformation similar to experiment **without prior structural knowledge**" (p10) | None — cited approvingly, and the "without prior structural knowledge" clause is the paper's own emphasis. **Note this is the one method the paper singles out as oracle-free** |
  | **Latent steering** (pair-representation / trunk / distogram intervention) | **ABSENT.** No such method is mentioned anywhere in the 29 pages | No criticism, because no coverage. **This is a coverage gap in the review, and worth recording: the sceptical camp's current survey does not engage with latent-space intervention at all** |
  | **MD-emulators — BioEmu** [83] | Given the most generous treatment of any DL method: "a more substantial advance, combining AlphaFold Database predictions, molecular dynamics trajectories, and experimental stability measurements to generate approximate Boltzmann-weighted ensembles… explicitly trained to reproduce equilibrium observables and… benchmarked not only on near-native structure generation but also on folding free energies and systems with known alternative conformational states" (p12); trained on "almost 100 milliseconds of publicly available all-atom molecular dynamics simulations" (p14) | "its outputs remain learned approximations to equilibrium distributions rather than direct physical simulations—and, as with pro-IL-18, an incorrect starting structure can still propagate to an inaccurate predicted ensemble" (p12) |
  | **MD-emulators — Distributional Graphormer (DiG)** [102] | "attempted to learn equilibrium conformational distributions using energy-based training objectives" (p12) — note the past-tense "attempted" | "although independent benchmarking has questioned its ability to reproduce realistic ensemble behavior [103]" (p12). **The harshest verdict on any single method in the paper** |
  | **MD, unbiased** | "the principal physics-based approach for estimating free-energy landscapes and transition pathways" (p12) | Cost and starting-structure dependence, E10 (p12). Sampling: "Even the longest unbiased MD simulation trajectory from DESRES barely captures one or two relevant slow conformational events for proteins such as kinases [118]" (p14). Force fields: "careful consideration must be given to force-field dependence, sampling biases, and the enormous computational cost of generating sufficiently converged simulations" (p14) |
  | **Enhanced sampling** (REMD [88], FAST [89], targeted MD [90]) | Described as the response to intractable sampling: "Recognizing that exhaustive sampling is intractable, goal-oriented adaptive sampling strategies such as FAST seek to manage exploration-exploitation trade-offs" (p11) | No direct criticism; targeted MD is noted as requiring "an external potential to promote structural interconversion between two states" (p11), i.e. it presupposes both endpoints |
  | **Structure-based / dual-basin models** [91–93] | "dual-basin structure-based models merge the contact maps of multiple experimentally determined states, allowing efficient reconstruction of transition pathways and free-energy landscapes" (p11–12); successes cited for ADK, prion, XCL1, KaiB, Mad2, RfaH (p12) | Not criticised, but the description itself concedes the oracle: they **merge contact maps of experimentally determined states**, i.e. both states must already be known |
  | **Hybrid DL–MD — AF2-RAVE** [104,105] | "using AlphaFold-generated structures as initial seeds for short unbiased simulations, followed by enhanced sampling to estimate conformational free energies and state populations"; applications to kinase DFG, conformation-selective docking, and "accelerated conformational sampling with no prior knowledge" (p12–13) | None stated. Described as substantially improving sampling efficiency "while preserving the physical interpretation of conformational populations" (p13) |
  | **Hybrid — BioEmu-seeded MSM** [110] | "BioEmu-seeded short MD simulations coupled to Markov State models to explore conformational ensembles of serine-threonine kinases, showing good performance in reliably mapping metastable states" (p13) | **A named failure mode, unusual for this document:** "but failing in other cases such as glycine transporter 1 (GlyT1) and plasmepsin-II (PlmII), proteins in which side chain heterogeneity governs their dynamics" (p13) |
  | **Co-folding** (NeuralPLexer [111], RoseTTAFold All-Atom [112], AlphaFold3 [113]) | "the first generation of context-aware predictors… Because binding frequently shifts conformational equilibria, these models naturally recover context-dependent structural states inaccessible to sequence-only predictors" (p13) | "Adversarial studies have shown that co-folding models often predict nearly identical ligand poses even after mutations that eliminate or sterically occlude binding sites, suggesting that current models remain strongly influenced by training-set biases rather than accurately modeling how perturbations reshape conformational landscapes [86, 114]. Moreover, many biologically important variables—including pH, ionic composition, temperature, membrane composition, alternative splicing, and macromolecular interactions—remain absent or only indirectly represented. Consequently, current co-folding methods should be viewed as an important first step toward context-aware state-space prediction rather than a complete solution." (p13) |
  | **Experiment-restrained prediction** (DEERFold [68], AlphaLink2) | Endorsed: "a small number of distance or contact restraints meaningfully narrows the space of plausible basins, illustrating that context-conditioning need not require dense experimental data to be useful" (p15) | None stated |
  | **AF2/AF3 as single-structure predictors, on perturbation response** | — | "AlphaFold3 predictions often remain nearly unchanged despite extensive sequence perturbations, suggesting a form of nonphysical robustness that fails to capture experimentally observed responses [67]. Even deletion of nearly 40% of the MSA frequently fails to induce expected structural changes. Although ESMFold exhibits greater sensitivity, both models remain more strongly influenced by training-set similarity than by physical plausibility." (p8) |
  | **AF2/AF3 on homologs with divergent folds** | — | "In the human oncoprotein BCCIP, two functionally distinct isoforms sharing approximately 80% sequence identity adopt structures differing by more than 10 Å, yet AlphaFold2 and AlphaFold3 predict nearly identical models because of training-set bias [59, 60]. Similar behavior is observed for pro-interleukin-18, DZZB, and MP20, where models converge on known folds despite experimental evidence for alternative conformations" (p8) |
  | **AFDB / ESMAtlas scale** | — | "most predicted structures cluster within previously observed fold space, and only a small fraction (approximately 4%) appear to represent genuinely novel folds[66]. Likewise, large-scale analyses of fold-switching proteins demonstrate that current predictors frequently fail to identify alternative conformations outside their training distributions [59]." (p8) |

  **The six prescribed roadmap components** (Fig 4, p16) — recorded here because they are the
  paper's positive programme and the closest thing it offers to reporting standards, arranged as
  a cycle in which each component feeds the next: **(1) Training data** — multi-state structures
  collected under diverse contextual conditions; **(2) Landscape benchmarks** — "quantitative
  tests of basin and state recovery"; **(3) Prediction objective** — "reframing model outputs as
  ensembles with calibrated uncertainty rather than single coordinates"; **(4) Physics-based
  modeling** — "the energetics and transition rates (ΔG, ΔG‡) linking states"; **(5) Perturbation
  modeling** — "predicting how mutations, ligands, pH, or temperature reshape the landscape and
  generalize to new conditions"; **(6) Experimental feedback** — "supplying empirical populations
  and mechanistic ground truth that validate and inform the training data, closing the loop."
  The rendered figure's legend strip adds a one-line contribution for each: diverse states /
  contexts; state / population recovery; calibrated ensembles; energetic / kinetic plausibility;
  perturbation generalization; empirical populations + mechanisms.

  **Data-infrastructure prescriptions**, p14: "expanding FAIR repositories of molecular dynamics
  trajectories will provide increasingly valuable training data for future landscape-aware
  predictors [117]"; and, on how to bound the cost, "Careful use of enhanced sampling in
  generating such a database of MD trajectories might be a compromise, especially if different
  sampling schemes yield similar ensembles."

- **stance**: **`contrast` + `background`. Provisional — the user's call.**
  - **`contrast` on standards of evidence.** The paper sets out, in E1/E2/E3/E8, exactly the bar
    a multi-state prediction claim will be held to: RMSD/TM alone is insufficient; the second
    state must be experimentally validated; basins must be *discriminated*, not merely produced;
    perturbation sensitivity must be shown; benchmark splits must separate alternative states of
    the same protein; and confidence metrics may not stand in for conformational correctness.
    It also pre-labels the whole method class our work sits in as "generators of candidate
    conformational states rather than predictors of conformational state spaces" (p10).
  - **`background` on the survey.** Sections II–IV are a competent, citable map of the boundary
    conditions, the method families, and where each is currently thought to stand. It is a good
    single citation for "the field agrees a single structure is insufficient".
  - **`threat` is arguable and should be considered by the user**, on the grounds that E1 is a
    reviewer checklist and that this document is the sceptical camp's consensus statement with
    eleven authors across four relevant labs. I have not tagged `threat`, because the paper
    contains no result that could contradict ours — it contains a standard. Whether a standard
    counts as a threat is a judgement above the extractor's pay grade. Flagged in `unresolved`.

## E. Quantitative comparators

- **metrics_reported**: **All numbers in this document are cited from other papers, with the
  possible exception of the three EAAT TM-scores (see `structural_priors_used` and
  `unresolved`).** None is a result of this work. The table is provided for traceability, and
  every row's "measured against" column names the source rather than an arm of this paper.

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | TM-score, EAAT transport domain, outward vs inward | 0.608 | TM-score | deposited EAAT structures, cited [27, 28]; **possibly computed by these authors** | p4 |
  | TM-score, EAAT scaffold domain | 0.834 | TM-score | as above | p4 |
  | TM-score, EAAT core structure | 0.897 | TM-score | as above | p4 |
  | EAAT transport-domain rigid-body displacement on substrate binding | ~15 | Å | cited [27, 28] | p4 |
  | F7 pyocin fold-switching segment length | 163 | residues | cited [40] | p6 |
  | BCCIP isoform pair, sequence identity | ~80 | % | cited [59, 60] | p8 |
  | BCCIP isoform pair, structural difference | >10 | Å | cited [59, 60] | p8 |
  | Fraction of AFDB/ESMAtlas structures representing genuinely novel folds | ~4 | % | cited [66] | p8 |
  | MSA deletion that still fails to induce expected structural change (AF3) | ~40 | % of MSA | cited [67] | p8 |
  | E. coli proteome estimated to undergo fold switching (CF-random, large-scale) | up to 5 | % of proteins | cited [77] | p9 |
  | AF2 / AF3 / BioEmu starting-structure error vs experimental pro-IL-18 | >20 | Å | cited [9, 62] | p10 |
  | BioEmu training data volume | ~100 | ms of all-atom MD | cited [83] | p14 |
  | PDB size | >250,000 | structures | cited [12, 13] | p2 |
  | 10E8 proline cis–trans isomerisation timescale | minutes to hours | — | cited [47] | p7 |
  | Fold-switching transition timescales | milliseconds to hours | — | cited [48–51] | p7 |
  | Longest DESRES unbiased MD trajectory, slow events captured for kinases | "one or two" | conformational events | cited [118] | p14 |
  | Type-II inhibitor / kinome study scale referenced | 50 inhibitors × 348 kinases | — | cited [122] | p18, ref list p29 |

  **No metric of the authors' own is reported. No error bars, no n, no statistical test appears
  anywhere in the document.**

- **n_predictions**: **NOT APPLICABLE — no predictions were made.** Samples per target: none.
  Targets: none. Total: none.

- **comparable_to_ours**: *(left empty for the user)*

- **si_in_scope**: **NO SI EXISTS — and the PDF is complete.** All 29 pages are held: 18 pages of
  text and figures, 11 pages of references (122 entries, p19–29). There is no supplementary
  file, no extended data, and no appendix referenced anywhere in the document. The one external
  artefact is the figure-generation repository at
  https://github.com/DevlinaC/expanding-protein-structure-prediction-figures (p18), which is
  **NOT HELD** by the corpus; it would be the only place to check whether the three EAAT
  TM-scores were computed here or copied.

## F. Figures

Four figures, five panel-group rows. Split points: Fig 2 splits because (a) carries an idealised
energy-landscape schematic and (b) carries structure renders — different forms entirely. Figs 1,
3 and 4 are each a single schematic each and are not split, even though each has internal
sub-regions, because neither `mark` nor `measure` differs across them (there is no mark and no
measure in any of the three).

**Pages rendered to fill this table: 4 (p3, p5, p11, p16), at 100 dpi.** Renders were necessary
for Fig 3 and Fig 4, whose captions describe the *content* of each stage but not the method lists
or legend strip drawn inside them, and for Fig 2b, whose caption names five systems but not that
each is drawn in two states. Temporary PNGs written to /tmp and not retained.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 3 | Side-by-side contrast of the current single-structure paradigm (sequence → predictor → one structure → inferred function) against the proposed paradigm (sequence + biological context → state-space predictor → states A/B/C with populations, pathways, context dependence, perturbation response → emergent function), with an inset asserting that state-space topologies span single-basin, discrete multi-basin and continuous ensemble | schematic | `SCHEMATIC \| two-box paradigm flowchart with cartoon structure glyphs, plus an inset strip of three idealised 1-D landscape sketches (single basin / discrete multi-basin / continuous ensemble) \| no data` | 3 regions: "CURRENT OBJECTIVE" box, "PROPOSED OBJECTIVE" box, "Conformational state-space topologies" inset. Regions vary by paradigm, not by system or condition | *(blank)* | **NOT REPORTED** — no licence statement appears anywhere in the PDF; arXiv listing licence not visible in the document. Figure code at the GitHub repo cited p18, licence there **NOT REPORTED** |
| 2A | 5 | Idealised 1-D free-energy landscape shown before and after a perturbation (mutation / ligand / environment), with the minimum shifting from State A to State B — the paper's illustration that function often follows population shifts rather than the appearance of new conformations | schematic | `SCHEMATIC \| paired idealised 1-D energy-vs-conformation curves, native and perturbed, with State A/B labels and an arrow between \| no data` | 2 sub-panels within panel (a), varying by condition (native, perturbed). No axis values, no units | Axes are labelled only "High energy (low probability)" / "Low energy (high probability)" with **no numeric scale on either axis** — appropriate for a schematic, but it means the depicted population shift is illustrative and carries no magnitude | as row 1 |
| 2B | 5 | Five deposited-structure pairs illustrating five classes of multi-state behaviour: adenylate kinase apo vs +Ap5A (domain reorientation), EAAT inward- vs outward-facing (rigid-body motion), Ebola VP35 closed vs open (cryptic pocket), S100β apo vs +calcium (local rearrangement), F7 pyocin pre- vs post-ejection (fold switching) | structure render | `RENDER \| facet: multi-state class (5: domain reorientation, rigid-body motion, cryptic pocket, local rearrangement, fold switching) × system (5, one per class) \| views: 1 \| overlay: 0 predictions on 2 references (two experimental states shown side by side, not superposed) \| axis: none` | 5 boxed sub-panels within panel (b), each holding 2 structures = 10 renders. Facets vary by system/class; within a facet the two structures vary by state, not by camera angle. Colouring is per-panel (grey vs red/green highlighting the moving element) | *(blank — the figure is illustrative by design and does not claim a quantitative result)* | as row 1. **PDB accession codes NOT REPORTED** for any of the ten structures |
| 3 | 11 | Four-stage progression of what current approaches recover, drawn left to right under a "PARTIAL REPRESENTATION → MORE COMPLETE REPRESENTATION" gradient bar: (1) single structure prediction → coordinates; (2) alternative state sampling → accessible states; (3) energetic refinement → populations; (4) experiments → mechanisms. Each stage box lists exemplar methods | schematic | `SCHEMATIC \| four-stage left-to-right capability ladder with a CURRENT/FUTURE band beneath and per-stage method lists \| no data` | 4 stage boxes varying by capability tier, not by system or condition. Method lists inside each box (visible only in the render, absent from the caption): stage 1 AlphaFold2,3 / OpenFold2,3 / RoseTTAFold / ESMFold2; stage 2 CF-random / MSA subsampling / AFSample2,3 / AFCluster; stage 3 BioEmu / AF2-RAVE / Multi-Basin SBMs / REMD; stage 4 NMR / HDX-MS / Cryo-EM / DEER | The stage-3 box displays population labels "40%" and "60%" on a two-basin cartoon. **These are illustrative numbers with no source, no system and no citation**, drawn in the same visual register as the method lists beside them, which are real. A reader skimming the figure could take them for a reported result | as row 1 |
| 4 | 16 | The roadmap: six components arranged as a closed cycle (1 training data → 2 landscape benchmarks → 3 prediction objective → 4 physics-based modeling → 5 perturbation modeling → 6 experimental feedback → back to 1), surrounding a central "TARGET: Conformational State Space" box listing states, populations, transitions/pathways and context dependence, with a legend strip stating what each component contributes | schematic | `SCHEMATIC \| six-node closed cycle around a central target box, with labelled directed edges (state/context cases, recovery metrics, ensemble targets, energy/rate constraints, testable predictions, measured states + populations) and a six-cell contribution legend \| no data` | 6 cycle nodes + 1 central target box + 1 six-cell legend strip. Nodes vary by research component, not by system or condition. Central box shows four cartoon states A–D with symbolic populations pA–pD | *(blank)* | as row 1 |

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), session 2026-09-08
- **schema_version**: v3
- **confidence**: **high** on document type, identity, the verbatim claim set, the per-family
  characterisations, the evaluation prescriptions, and the absence of new data. **High** on
  figure panel structure, all four figure pages having been rendered. **Medium** on one point
  only: whether the three EAAT TM-scores on p4 were computed by these authors or copied from
  refs [27, 28] — the citation points at the structure papers, which is what one would do either
  way. The text layer is clean; Greek letters render correctly (α, β, µ, Δ), and the only
  typographic defect is a mismatched quotation mark in the reframed central question on p2,
  reproduced as printed.
- **unresolved**:
  1. **Provenance of the three EAAT TM-scores (p4: 0.608 / 0.834 / 0.897).** If computed here,
     this perspective contains a small amount of original analysis and is a different citation
     from one that contains none. The GitHub figure repository (p18) is not held and would settle
     it. Everything else in the document is unambiguously cited.
  2. **Tag needed but not in the v3 vocabulary: `review` / `perspective`.** There is no tag that
     marks a document as a non-primary survey. `benchmark-only` is the nearest and is plainly
     false — no benchmark is run. This matters more than the usual missing-tag complaint, because
     the corpus now holds a document whose section C is uniformly NOT APPLICABLE and nothing in
     its tag set says why; a reverse lookup for rigour properties will find it absent from every
     list with no way to distinguish "did not do it" from "is not that kind of paper". The
     `experimental` tag exists for exactly this purpose on the wet-lab side ("marks a paper with
     no structure prediction in it at all, whose section C will be mostly NOT APPLICABLE by
     design rather than by sloppiness") — a `perspective` tag is its missing counterpart.
  3. **Second tag needed but not available: something for "proposes evaluation criteria /
     reporting standards".** This document's most citable content is a prescription, and there
     is no tag for a paper that sets standards rather than reporting results. `comparator-numbers`
     is the closest utility tag and is false here.
  4. **Method-family tags deliberately withheld.** The paper *reviews* MSA subsampling,
     clustering, MD, enhanced sampling, MD-emulators and co-folding, but performs none of them.
     Tagging `msa-subsample`, `af-cluster`, `md`, `md-emulator`, `enhanced-sampling` or
     `cofolding` would return this paper for "which papers did X", which is false. Tagging
     nothing means "which papers discuss X" has no answer. The vocabulary cannot express the
     difference between doing and surveying. Flagged, not resolved.
  5. **State-handling tags deliberately withheld** for the same reason: the paper argues for
     `ensemble` and `continuum` as the prediction *target* but generates neither.
  6. **`stance` third value.** `threat` is arguable (see `stance`); not tagged, deferred to the
     user.
  7. **`cryptic-pocket` tag applied at discussion level.** §2.2 (p6), the VP35 and KRAS examples,
     and the PocketMiner/Zhang-Bowman benchmarking endorsement (p17) make this a substantive
     topic of the paper, but nothing was *studied*. Applied on the reading that site tags "mark
     what was studied" is best served by including a document that devotes a section to the
     site; flag for the user if the corpus convention is stricter.
  8. **Venue.** Typeset in Springer Nature journal style but posted only to arXiv, with no
     journal named and no submission statement. Whether a journal version exists is not
     determinable from this PDF.
  9. **No figure licence anywhere in the PDF.** Every `reuse` cell is NOT REPORTED. arXiv's
     per-submission licence is not printed in the document.
- **why_it_matters**: *(left empty for the user)*

## Tags

`general-protein` `fold-switching` `cryptic-pocket` `preprint` `contrast` `background`

Tags withheld with reasons in `unresolved`: all Method tags (surveys but does not perform),
all State-handling tags (argues for, does not generate), all Metric, Rigour, Protocol and Control
tags (Section C is NOT APPLICABLE throughout), `benchmark-only` (no benchmark is run),
`threat` (deferred to the user), `figure-exemplar` (the document is kept for its framing, not
its figures).
