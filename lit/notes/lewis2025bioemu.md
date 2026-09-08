# lewis2025bioemu

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–45)**, which coincide with the
printed page numbers of this preprint. Layout: p1 title/abstract/Introduction start, p2 Introduction,
p3 Model (Figure 1), p4–6 §3 Sampling conformational changes (Figure 2 on p5), p6–8 §4 Emulating MD
equilibrium distributions (Figure 3 on p7), p8–10 §5 Predicting protein stabilities (Figure 4 on p9),
p10–11 §6 Conclusion + code availability, p12–14 references, p15–16 SI contents, p17–32 Supplementary
Methods §S.1–S.6, p33–41 Supplementary Tables and Figures (Table S4 p33, Figs S1–S8 on p34–41),
p42–45 supplementary references.

**Supplementary Information IS held** (p15–41), which is unusual for this corpus and means
`metrics_reported` is not silently emptied. The one thing that is *not* held is the separate
"Supplementary Data" file carrying the full PDB/chain identifier lists and per-residue alignment
labels for every benchmark entry (cited p29: "Full lists containing PDB and chain identifiers
(label_asym_id), as well as residue labels for both alignment and metric computation regions, where
appropriate, are provided in the Supplementary Data of this manuscript"). See `si_in_scope`.

**Version caveat, recorded up front because it affects `A. Identity`:** the held PDF is the bioRxiv
preprint, version posted 25 February 2025. The task brief states this work has since appeared in
*Science* (2025), DOI `10.1126/science.adv9817`. Nothing inside this PDF says so; the journal version
was **not read**, and none of the numbers below can be assumed to survive peer review unchanged.
Tagged `preprint` on the evidence of this PDF only. See `unresolved`.

**Why this note is unusual for the corpus:** BioEmu is not a co-folding model, not an MSA-manipulation
method, and not an enhanced-sampling protocol. It is a sequence-conditioned diffusion model trained on
molecular dynamics trajectories and experimental stabilities that emits i.i.d. samples claimed to
approximate a Boltzmann equilibrium distribution. Section C fields that presuppose "which state did
you steer it to" therefore have no handle to name; that is a property of the method, not a gap in the
extraction. Tag `md-emulator`.

---

## A. Identity

- **citekey**: `lewis2025bioemu`
- **doi**: **10.1101/2024.12.05.626885** (bioRxiv) — p1 banner: "bioRxiv preprint doi:
  https://doi.org/10.1101/2024.12.05.626885; this version posted February 25, 2025". The journal DOI
  `10.1126/science.adv9817` (Science 2025) is supplied by the task brief and does **not** appear
  anywhere in this PDF; recorded in `unresolved`, not asserted here.
- **year**: **2025** — this version posted 25 February 2025 (p1). Original preprint posting date
  encoded in the DOI is 5 December 2024; this is a revised version.
- **venue**: **bioRxiv preprint, not certified by peer review.** p1: "The copyright holder for this
  preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a
  license to display the preprint in perpetuity. It is made available under a CC-BY-NC-ND 4.0
  International license." Tagged `preprint`; do **not** tag `peer-reviewed` on the evidence of this
  PDF, notwithstanding the known Science version.
- **title**: Scalable emulation of protein equilibrium ensembles with generative deep learning — p1
- **authors**: Sarah Lewis, Tim Hempel, José Jiménez-Luna, Michael Gastegger, Yu Xie, Andrew Y. K.
  Foong, Victor García Satorras, Osama Abdin, Bastiaan S. Veeling et al. — 25 authors, p1. The first
  nine are marked "† These authors contributed equally to this work" (p1). Correspondence: Frank Noé
  (franknoe@microsoft.com). Affiliations: 1 = AI for Science, Microsoft Research; 2 = Freie
  Universität Berlin, Department of Physics (Zaporozhets, Chen, Clementi, Noé) — p1.

## B. Scope

- **system**: **general protein — soluble single chains, small-to-medium, at 300 K.** The model is
  explicitly scoped: "our system was trained on large amounts of MD simulation of soluble proteins"
  (p10) and "it only emulates single protein chains at a fixed thermodynamic condition of 300K"
  (p10). Within that scope the benchmark and training systems span many families; three are worth
  naming because they are true positives for corpus reverse-lookup:
  - **Protein kinases** are present both in training and in the benchmarks: 6.8 ms of DDR1 kinase MD
    (Table S1, p18; "Simulations of 9 DDR1 kinases", p20), and CaM Kinase II (Fig. 2b,iii, p5), CaM
    Kinase I, DCLK1 Kinase and Titin Kinase in the local-unfolding benchmark (Fig. S3, p36).
  - **Periplasmic / solute binding proteins** dominate the domain-motion benchmark: LAO-binding
    protein (Fig. 2a,ii, p5), Glutamine Binding Protein, D-ribose binding protein, Dipeptide Binding
    Protein, Oligopeptide-binding protein A, L-cystine solute receptor, Lipoprotein CD0873 (Fig. S2,
    p35).
  - **Intrinsically disordered proteins**: Complexin II case study (p8) and the 65-protein CALVADOS /
    IDRome test set (p9, p31).
  Explicitly **out of scope**: membranes, small-molecule ligands, multi-chain complexes, temperatures
  other than 300 K (p10). Adenylate kinase (Fig. 2a,i) is a small-molecule kinase and per the v3
  scoping note does **not** justify the `kinase` tag; the protein kinases above do.
- **n_targets**: **no single number is meaningful; record every level, with pages.**
  - **Training MD**: 24,062 MD systems / 24,219 independent chains (Table S1 total, p18) — but 21,458
    of those are single-point mutants of 271 MEGAscale wildtypes, so distinct *protein folds* in
    training are on the order of 2,600.
  - **Training experimental**: ~776,000 ΔG / ΔΔG entries from MEGAscale (p21); main text says "over
    750,000 experimental measurements" (p8).
  - **Multi-conformation benchmarks**: OOD60 **19** proteins (p4, p29); domain motion **22** examples
    (p29); cryptic pocket **34** apo/holo pairs (p6, p29); local unfolding **21** examples (p29, main
    text says "20 protein examples" on p6 — see `unresolved`); OODVal **11** examples (p30, used for
    model selection, not reporting). Main text summarises these as "a set of around 100 proteins that
    engage in experimentally-validated domain motions, local unfolding transitions, or cryptic pocket
    formation" (p4). Table S4 (p33) counts **152 reference structures** across these benchmarks
    (121 pre-AF2-cutoff + 31 post).
  - **MD-emulation benchmarks**: **12** DESRES fast folders (p6, leave-one-out); **17** CATH domains
    with >100 µs MD designated as test set (p8); 2 large case studies — Complexin II (134 aa) and
    ACE2 (614 aa) (p8).
  - **Stability benchmarks**: MEGAscale train/test scatter (Fig. 4a, p9; exact n per split NOT
    REPORTED in the caption or text); **26** hyper-stable ProThermDB proteins from an initial 140
    (p31); **65** CALVADOS IDPs (p31).
  - **Generality flag:** the paper claims genome-scale ambition — "indicates a path forward for
    predicting biomolecular function at genomic scale" (p2) — while every quantitative equilibrium
    result rests on ≤17 CATH domains and 12 fast folders. The authors do not hide this; they attribute
    it to data limits (p10).
- **method_class**: **other — sequence-conditioned generative diffusion model trained on MD
  trajectories and experimental stabilities ("biomolecular emulator").** None of the schema's named
  classes fits. It is not MD (it runs no dynamics and has no potential energy function — see
  `stated_limits`), not enhanced sampling, not co-folding, not clustering, not benchmark-only. This is
  precisely the case the v3 tag `md-emulator` was added for. Architecturally: frozen AlphaFold2
  evoformer sequence encoder → SE(3) denoising diffusion model over backbone frames, sampled with a
  second-order (Heun) integrator in 100 denoising steps (p3, p21–23, p28). Note the paper *also*
  contributes ~172 ms of new MD (Table S1, p18) and five new benchmarks (p29–30), but neither is the
  method.
- **backbones**: **AlphaFold2 only, and only as a frozen sequence encoder.** p21: "we use pre-trained
  AlphaFold2 [27] sequence representations. We run the AlphaFold2 container with a few changes; we
  used only the Uniclust30 database [29] (as of August 2018) as reference for multiple sequence
  alignment construction via hhblits [30], completely excluded templates, and removed the AlphaFold2
  recycling iterations. During generation, we set the random seed to 0 and use the single and pair
  embeddings generated by AlphaFold2 model 3." p24: "We start with a pretrained sequence encoder from
  AlphaFold2 [27], freeze its weights, and train our own structure module from scratch." The structure
  module is BioEmu's own (Distributional Graphormer-like IPA transformer, 8 blocks — p3, p23).
  Baselines compared head to head are **AFCluster** and **AlphaFlow** (p4, p31, Fig. S5 p38) — both
  are themselves AF2-derived, so this is three *methods* over one backbone, not three backbones.
  **Do NOT tag `multi-backbone`**: no AF3, Boltz, Chai, OpenFold or Protenix appears anywhere.
- **templates**: **OFF, explicitly and completely.** p21: "completely excluded templates". No template
  channel exists in BioEmu's own structure module. Note the consequence for tagging: the corpus has
  `templates-on` and `no-template-no-msa` but **no tag for templates-off-with-MSA-on**, which is
  exactly this paper's regime. Recorded in `unresolved`; no protocol tag applied.
- **msa_handling**: **full, single alignment, fixed and frozen.** One hhblits/Uniclust30 (August 2018
  snapshot) MSA per sequence, fed once to the frozen AF2 evoformer with seed 0 and no recycling; the
  resulting single and pair embeddings "for all proteins used in training and inference are
  pre-computed once and stored for fast retrieval" (p21–22). **Not subsampled and not state-filtered**
  — these are different things and neither is done here. All conformational diversity comes from the
  diffusion sampler, not from the alignment. Baseline AFCluster does MSA subsampling/clustering with
  ColabFold defaults (p31), but that is the baseline's protocol, not BioEmu's.

## C. Conformational core

- **states_generated**: **ensemble + continuum.** This is genuinely dual and both halves matter.
  - *Ensemble*: the output is a set of i.i.d. coarse-grained backbone structures. "BioEmu receives as
    input a protein sequence and generates independent identically-distributed (i.i.d.) samples from
    the approximated equilibrium distribution over conformations of that protein" (p21). Sampling
    scale is fixed across the paper: "For all BioEmu results shown here, we draw 10k samples" (p6).
    Only backbone heavy atoms are modelled: "side-chains and hydrogen atoms are not explicitly modeled
    by BioEmu" (p22).
  - *Continuum*: the ensemble is used to build continuous free energy surfaces over TICA coordinates
    (Fig. 3a,b; Fig. S7, S8) and continuous free-energy profiles over RMSD or fraction-of-native-
    contacts (Fig. 2; Figs. S1–S4). The claim is not "two states" but a density.
  - **What it is claimed to approximate**: the Boltzmann equilibrium distribution of the protein at
    300 K. Abstract, p1: "BioEmu's protein ensembles represent equilibrium in a range of challenging
    and practically relevant metrics." Conclusion, p10: "a generative machine learning system to
    approximately sample the equilibrium distributions of proteins". The word "approximately" is the
    authors' own and is used consistently.
  - **Equilibrium free-energy accuracy claims, with numbers and pages** (also in `metrics_reported`):
    abstract "relative free energy errors around 1 kcal/mol" (p1); DESRES fast folders "the mean
    average error between the MD and model 2D free energy landscapes is only 0.74 kcal/mol, ranging
    from 0.30 kcal/mol for BBA to 1.63 kcal/mol for λ-repressor, which is on the order of differences
    expected from two different classical MD force fields" (p6); CATH test set "a free energy mean
    average error over the converged test set of 0.91 kcal/mol, again comparable to the differences
    expected between different MD force fields" (p8); folding free energies "a mean absolute error
    below 0.8 kcal/mol and a Spearman correlation coefficient above 0.65 for proteins in the MEGAscale
    dataset" (p9), with Fig. 4a reporting train 0.73 kcal/mol / correlation 0.67 and test 0.76
    kcal/mol / correlation 0.66 (p9, panel annotations).
- **structural_priors_used**: **extensive, layered, and the single most important field for judging
  whether a conformational success is emulation or recall.** Four distinct deposited-knowledge layers
  enter at design/training time. None of these is a methodological sin; all of them bound what
  "generalisation" can mean here.
  1. **Frozen AlphaFold2 evoformer weights** (p21, p24). AF2 was trained on the PDB to a 30 April 2018
     cutoff, so every BioEmu embedding carries PDB structural knowledge the authors did not control.
     The authors name this risk themselves and call it "potential Evoformer embedding leakage" (Fig.
     S5 caption, p38) and "embedding poisoning" (Table S4 caption, p33). It is the reason Table S4
     exists.
  2. **AlphaFold database pretraining — ~200 M predicted structures, reduced to a ~50 k
     structurally-diverse subset.** AFDB snapshot downloaded July 2024 (p17). Pipeline (p17, S.1.1):
     mmseqs cluster at 80% identity / 70% coverage → >93 M clusters; recluster centroids at 30%
     identity and keep one per 30%-cluster; discard clusters with <10 members → ~1.4 M sequence
     clusters; foldseek structure-cluster within each sequence cluster at 70% identity / 90% coverage;
     keep one representative per structure cluster; discard single-structure clusters and all-coil
     clusters; discard structure representatives with TM-score > 0.9 to another representative;
     require at least one structure with pLDDT > 80 and per-residue pLDDT std-dev ≥ 15. Result:
     "∼50k sequence clusters with structural diversity" (p17). The *deliberate design intent* is that
     a sequence maps to several structures: "This effectively creates a mapping from a sequence to
     multiple structures" (p24). This is the prior that teaches the model to be multi-modal at all —
     ablating it (training on PDB, or on high-pLDDT AFDB) "are significantly worse in [the model's]
     capacity to sample diverse conformations (Fig. S6)" (p25).
  3. **Protein Data Bank processing** (p17, S.1.2): PDB snapshot 23 November 2023, asymmetric units,
     ≤2500 residues, resolution ≤9.5 Å, nucleic acids discarded, non-biological heteroatoms filtered,
     ligand-binding chains preferentially kept "So as to better capture ligand-binding conformational
     effects". **Caveat:** the paper never states that this processed PDB set trains the released
     BioEmu; the only place it is used in the text is the pretraining ablation of Fig. S6 (p25). See
     `unresolved`.
  4. **Deposited structures inside the MD pipeline itself.** Every in-house MD dataset is seeded from
     a deposited or predicted structure: CATH1 "the first trajectory epoch was seeded from a reference
     PDB structure" (p18); MEGAsim "Folded structures were obtained from the AF2 predictions available
     on the Zenodo repository of Ref. [21]" (p19); Complexin "The simulations were seeded using the
     AlphaFold2 predicted structure deposited in Uniprot" (p20); ACE2 comparison MD "seeded from
     magenta PDB-ID 6LZG" (Fig. 3 caption, p7). And the fraction-of-native-contacts function — which
     drives both the reweighting and the PPFT loss — is defined against a deposited reference: "For
     each simulated MEGAscale system, we use its PDB structure as the reference conformation" (p27).
  5. **Benchmark construction from deposited pairs.** Every multi-conformation benchmark is a set of
     PDB pairs chosen because both endpoints are solved (p29–30). See `oracle_leakage` route 7.
- **oracle_leakage** — **seven routes, each answered separately.**

  **Route 1 — deposited structures used as input or template.**
  **NONE FOUND at inference for the target's own structure; PRESENT upstream, and the authors say so.**
  At inference BioEmu is conditioned on sequence alone: "BioEmu receives as input a protein sequence
  and generates independent identically-distributed (i.i.d.) samples" (p21); templates are
  "completely excluded" (p21). Protocol is described on p21–23 and p24, so the negative is checkable.
  But three upstream channels carry deposited structural knowledge into the model, and the third is
  quantified rather than denied:
  - Frozen AF2 evoformer trained on the pre-2018 PDB (p21, p24).
  - AFDB pretraining and 200 ms of MD seeded from deposited/predicted structures (p17–20; see
    `structural_priors_used`).
  - **Verbatim, the authors' own framing (Fig. S5 caption, p38):** *"Note that all comparisons apart
    from those in the OOD60 benchmark test how well different models fit the data but it is not fair
    in terms of generalization. Apart from potential Evoformer embedding leakage, for our method, all
    cases are in the test set, whereas for other methods cases before the AF cutoff date were present
    in the training set."*
  - **Verbatim (Table S4 caption, p33):** *"Success rates of multi-conformation benchmark split by
    whether the reference was present in the AlphaFold2 monomer model training set, or whether it is a
    new reference not explicitly leaked via embedding poisoning."*

  **Route 2 — state annotations from a curated state database driving templates or alignments.**
  **NONE FOUND.** No GPCRdb, KLIFS, Kincore or equivalent appears anywhere in the paper. Benchmark
  curation is manual from the PDB plus the CryptoSite benchmark and two literature sources: "Many of
  these examples were further curated from the CryptoSite benchmark [45] or other related works [46]"
  (p29), and local-unfolding examples come partly from Chakravarty & Porter's fold-switching set
  ("including some examples from the benchmark proposed in [47]", p29). The CATH database (v4.3.0) is
  used to *select training domains* (p19) — that is a fold-classification database, not a state
  annotation, and it drives neither templates nor alignments. Protocol described p19, p29–30.

  **Route 3 — cluster labels derived from known states.**
  **PRESENT in three distinct places, none of them at inference.**
  - AFDB pretraining: foldseek structure clustering *within* sequence clusters supplies the multi-
    structure augmentation signal (p17, steps 4–7; p24). The labels come from *predicted* structural
    heterogeneity, not from experimentally known states, which is materially weaker.
  - Benchmark definition: OOD pairs are chosen by clustering deposited structures — "Within each
    sequence cluster, we perform a structure clustering procedure on the associated PDB entities...
    This included TM-score as the main comparison metric per sequence cluster followed by an
    agglomerative clustering procedure as implemented in scikit-learn, with a maximum allowed TM-score
    between clusters of 0.7" (p30). Cluster labels from deposited structures define what counts as
    "two states" — design-level, see route 7.
  - MD reweighting: MSM/k-means clustering of octapeptide trajectories (p26) and HMM macrostate
    clustering in TICA space for the free-energy MAE (p31–32). These are clusters of *simulation*
    data, not of known deposited states.

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.**
  **PRESENT, and this is the sharpest pipeline-level finding in the paper.**
  - **Model checkpoint selected on a conformational benchmark of deposited pairs. Verbatim (p24):**
    *"The final model checkpoint was chosen based on the performance obtained on our curated OODVal
    benchmark (see S.4.1)."* OODVal is "A manually-curated set of 11 examples picked after the
    AlphaFold 2 monomer model cutoff date but that is disjoint from the OOD60 set detailed above,
    which we use for pre-trained model selection purposes. Only global RMSD is used as a metric in
    this benchmark" (p30). Disjointness from OOD60 is a real mitigation; it does not make the stopping
    criterion state-blind. Under the v3 clarification (tuning a *range* on the evaluation set is
    leakage even without a per-target value), selecting the checkpoint against RMSD-to-deposited-pairs
    is leakage into the released model.
  - **Fixed thresholds chosen a priori but never justified against anything but the reference set:**
    FNC folding threshold found as the KDE minimum "within the range of 0.45-0.9" — the *range* is
    fixed by hand (p27); PPFT constants "We choose k = −24, dRMSDthreshold = 0.4 for all protein
    systems" (p28); loss weight "w = 2" (p28); success thresholds RMSD ≤ 3 Å, FNC ≤0.3/≥0.7, cryptic
    RMSD ≤ 1.5 Å (Table S4 caption, p33); ProThermDB foldedness threshold 0.65 (p9).
  - **Visual curation of training data against reference structures. Verbatim (p19):** *"In difficult
    cases, we checked several sample structures as well as the FNC and RMSD time series and made a
    decision based on visual inspection."* And of the benchmarks (p30): "Both sets underwent
    significant manual curation to ensure unphysical or unrealistic examples were excluded."
  - The AF2 encoder seed is pinned, not swept: "we set the random seed to 0" (p21).

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.**
  **PRESENT by construction; this is the entire multi-conformation evaluation.** Every success rate in
  §3 is a distance-to-held-reference predicate. Table S4 caption, p33: "success is defined for each
  type of conformational change as described in the main text — domain motion: RMSD ≤ 3Å, local
  unfolding: fraction of native contacts ≤ 0.3 and ≥ 0.7, cryptic pockets RMSD ≤ 1.5Å." Fig. 2
  caption, p5: "coverage, defined as the percentage of reference structures that are sampled by at
  least 0.1% of samples (4 kcal/mol) within a given distance of the respective metric... Our defined
  success threshold is marked by dashed lines." The 1.5 Å cryptic threshold is justified in words
  ("To ensure capturing subtle changes, we define success by a very strict 1.5Å RMSD threshold to the
  apo and holo reference structures", p6); the 3 Å domain-motion and 0.3/0.7 FNC thresholds are
  stated but **not justified** anywhere I could find. This is not concealed — it is the standard for
  this benchmark family — but it means "85% success" is a statement about a held reference set, not
  about the world.

  **Route 6 — best/worst model labels assigned against a held reference.**
  **PRESENT, explicitly, as a named metric. Verbatim (p30):** *"k-recall: defined as the average of a
  metric for the closest 0.1% samples per reference."* This selects the best 0.1% of 10,000 samples
  (i.e. the best ~10) by distance to the structure being predicted, and reports their mean. It is the
  headline metric in the middle and right columns of Fig. S5 (p38) and Fig. S6 (p39), where it is
  labelled "Recall RMSD" / "Recall FNC". The coverage metric has the same character in a softer form:
  a reference counts as covered if *any* 0.1% of samples land within threshold. No calibrated,
  reference-free selection rule is offered; BioEmu emits no confidence score (see
  `confidence_as_discriminator`).

  **Route 7 — design-level oracle use: systems or input conditions chosen because the expected answer
  is already known.**
  **PRESENT throughout, and it is design-level, not pipeline-level — keep the two distinct.** Every
  multi-conformation benchmark is a set of PDB *pairs* selected because both endpoints are deposited
  and the transition is already documented: "we have also curated a set of around 100 proteins that
  engage in experimentally-validated domain motions, local unfolding transitions, or cryptic pocket
  formation" (p4); "34 example pairs featuring a conformational change characterized by the formation
  of a binding site that is induced in a holo (bound) structure, but not on its apo (unbound) version"
  (p29); OOD pair selection requires "a minimum shared sequence identity between resolved sequences of
  0.8, and a maximum resolved sequence length difference of 50 residues" between the two deposited
  members (p30). Input-condition choice is also driven by known labels: "For the cryptic pocket
  benchmark, however, only the experimental sequence of the apo conformation was sampled, as it is the
  more biologically challenging case" (p30), and where the two references disagree in sequence "both
  were sampled in equal proportion" (p30). The expected answer is declared before any sample is read.
  This is weaker than pipeline leakage and must not be conflated with it. Tag `design-level-oracle`
  alongside `oracle-leak`.

- **prospective**: **no — retrospective throughout, in both the conformational and the thermodynamic
  arms.** Targets are chosen because deposited reference pairs exist (route 7); success is scored
  against those references (route 5); the reported best samples are picked against them (route 6);
  and the released checkpoint was selected on a conformational benchmark (route 4). The
  post-AF2-cutoff arm (Table S4, p33) is a *temporal* control on the encoder's training set, not a
  prospective prediction: those structures were already deposited when BioEmu was built. The nearest
  thing to a prospective claim in the paper is the general statement that BioEmu "can efficiently
  provide experimentally-testable hypotheses" (p1) — a hypothesis about future work, not a test.
  No wet-lab validation of any BioEmu prediction is reported; every experimental comparison is against
  pre-existing measurements (MEGAscale, ProThermDB, IDRome). Do **not** tag `prospective` or
  `experimental-validation`.
- **state_metric**: **triple — RMSD-to-reference + binary predicate + continuous coordinate.** Forcing
  one loses two-thirds of the paper. (The schema licenses dual values; this paper needs three, and the
  discarded ones would each be the interesting half for a different query.)
  - **RMSD-to-reference**, with stated thresholds: global backbone Cα RMSD for domain motions,
    **success at ≤ 3 Å** (p5 caption, p33; **threshold not justified**); local Cα RMSD over
    manually-defined pocket regions for cryptic pockets, **success at ≤ 1.5 Å**, justified as "very
    strict... to ensure capturing subtle changes" (p6). "For most benchmarks we used RMSD on the
    backbone atoms as our main metric" (p30). Global pairwise sequence alignment (BioPython
    PairwiseAligner, open-gap penalty manually set to 0.5) reconciles sampled and resolved sequences
    (p30).
  - **Binary predicate** on fraction of native contacts, used where no single reference exists: "For
    the local unfolding benchmark, however, we used a Cα-only version of a contact map between the
    unfolding region and the entire protein because the unfolded state has no single reference" (p30);
    thresholds **FNC > 0.7 folded, < 0.3 unfolded** (Fig. S3 caption, p36; Table S4 caption, p33);
    for stability, foldedness is a Heaviside step on FNC with a **system-dependent** threshold taken
    as the KDE minimum in 0.45–0.9 (Eq. 6, p27), and **0.65** for the ProThermDB check (p9). The
    FNC definition is the Best–Hummer–Eaton switching function with β = 5, λ = 1.2, δ = 0 over residue
    pairs ≥3 apart in sequence and within 10 Å in the reference fold (Eq. 7, p27).
  - **Continuous coordinate**, which is where the paper's real novelty sits: the **macrostate mean
    absolute error (mMAE)** of free energies. Procedure (S.6, p31–32): linear TICA projection of the
    MD data → 2-D TICA space → HMM clustering at 1 ns lag time with **3 hidden states** ("a
    numerically stable choice") → per-macrostate free energy by sample counting Gi = −kBT ln(pi) →
    offset so min Gi = 0 → mMAE = mean |G_ML − G_MD| over macrostates (Eqs. 13–14, p32).
  - Two ensemble-level statistics summarise the above: **coverage** ("measures the fraction of sampled
    reference conformations, according to a chosen metric, and as a function of different metric
    thresholds. We consider a conformation as covered if at least 0.1% of samples are within a
    specific threshold the corresponding reference structure", p30) and **k-recall** (route 6, p30).
  - **Unphysical samples are filtered before any metric is computed** (p30): Cα–Cα ≤ 4.5 Å and C–N
    ≤ 2.0 Å between sequence-adjacent residues, and no two backbone atoms of different residues within
    1.0 Å. The residual clash fraction is itself reported (Fig. 3a,iii and 3b,ii, p7).
  - Additional non-structural observables: helix/sheet propensity per residue, radius of gyration
    against Flory scaling (Fig. 4c, p9), and secondary-structure content over the ensemble (Fig. 3).
- **metric_saturation**: **YES — two genuine numeric floors/ceilings, both acknowledged by the
  authors.** (Numeric only; the log axis on Fig. 3a,ii and the truncated free-energy colour scales are
  figure defects and live in `hides` on the relevant rows.)
  1. **Explicit clamp on the free-energy metric. Verbatim (p32):** *"As not all macrostates were
     sampled by our model for the systems considered, a prior count of 1 was assigned to each
     macrostate. For a model with 10k samples that corresponds to clamping pi = max(pi, 10⁻⁴), which
     can be regarded as the model resolution boundary."* At 300 K this floors any unsampled
     macrostate's free energy at ≈ 5.5 kcal/mol above the most populated state, so the reported mMAE
     of 0.74 / 0.91 kcal/mol cannot exceed a bounded value however badly a state is missed. The
     authors label it a resolution boundary rather than concealing it, but it is a floor on the
     headline number.
  2. **Coverage ceilings at 100% within the plotted range** for domain motions, cryptic holo and both
     local-unfolding states, for *every* method including the pretrained baseline (Fig. 2 left column,
     p5; Fig. S5 left column, p38). Method separation therefore exists only in the low-threshold
     region; at the right edge of each panel all curves are indistinguishable at 1.0. The 0.1%-of-
     samples coverage criterion is itself a floor, and the authors state its energetic equivalent:
     "sampled by at least 0.1% of samples (4 kcal/mol)" (Fig. 2 caption, p5).
- **directional_control**: **NONE. BioEmu cannot be instructed which state to produce; it can only be
  sampled.** There is no partner, no ligand, no nanobody, no state-annotated template, no
  state-filtered MSA and no subsample-depth knob. The conditioning variable is the amino acid sequence
  and nothing else: `x ~ p_θ(x|S)` (Eq. 1, p22). The only levers a user actually has are (i) which
  sequence to submit — used deliberately in the cryptic-pocket benchmark, where "only the experimental
  sequence of the apo conformation was sampled" (p30), and in the mutant analyses of Fig. 4d — and
  (ii) how many i.i.d. samples to draw (10k throughout). The authors name the absence as a limitation:
  "A proper emulator for proteins requires conditioning on experimentally and biologically relevant
  parameters such as temperature and pH, and needs to be able to model multiple interacting molecules"
  (p10). No `directed-state`, `partner-driven`, `ligand-driven`, `peptide-driven`, `g-protein-mimetic`
  or `nanobody` tag applies. `seed-only` is a poor fit and is **not** applied — see `unresolved`.
- **anti_memorization_design**: **YES, and unusually thorough for this corpus — three independent
  mechanisms, all with stated cutoffs.**
  1. **Sequence-similarity filter on the training set, 40%.** Main text, p4: "Finally, to evaluate
     generalization, we filter our training set such that no protein has more than 40% sequence
     similarity to any of the reported test proteins of at least 20 residues or longer." Method, p24
     (S.3.1): "Having defined a list of test proteins, we removed from our training and validation
     data any protein whose sequence was similar to any test protein's sequence. Specifically, we used
     the mmseqs2 software [1] (version 15.6f452) and removed proteins if they have 40% or higher
     sequence similarity with any test protein of at least 20 residues in size, using the highest
     sensitivity parameter supported by the software (8.0)." **This is a sequence hold-out, not a fold
     hold-out.** No TM-score, CATH-class, foldseek or any structural criterion is applied to the
     train/test split. Nothing prevents a test protein sharing a fold — or a domain-motion mechanism —
     with a training protein at <40% identity. That is the honest answer to "held out by sequence, by
     fold, or not at all": **by sequence, at 40%, and by nothing else.**
  2. **Temporal cutoff against the frozen AF2 encoder — 30 April 2018.** p29: "OOD60: A collection of
     19 examples collected from the PDB after the AlphaFold 2 monomer model cutoff date (Apr. 30th
     2018). A 60% sequence similarity cutoff is used to remove anything from this benchmark that is
     similar to any chain in the PDB prior to the specified cutoff date." p4 restates the double
     constraint: "we defined a challenging test set of conformational changes, called OOD60, with a
     maximum of 60% and 40% sequence similarity to the AlphaFold2 monomer model and our training sets,
     respectively." Curation detail p30: PDB chains after the cutoff → Uniprot segments via SIFTS →
     mmseqs2 at 0.99 identity → TM-score agglomerative clustering at 0.7 → pairs filtered to ≥50
     resolved residues, ≤0.4 coil, ≥0.8 mutual sequence identity, ≤50-residue length difference. **n =
     19.** Cause of the small n is stated: "Due to the strict sequence similarity constraints, OOD60
     only contains 19 proteins" (p4).
  3. **Leave-one-out over the 12 DESRES fast folders** (p6, p25): "We train 12 'DESRES-finetuned
     models', each of which is tested on one fast folder and fine-tuned on the others"; split 10:1:1
     per protein, with PRB as validation in every split except its own, where UVF substitutes (p25).
  Also: a fixed CATH test set of 17 domains with >100 µs MD each (p8, p32); a MEGAscale train/test
  split (Fig. 4a, p9, sizes NOT REPORTED); and OODVal held separate from OOD60 for model selection
  (p30). Two stability checks are effectively held-out by construction: the 26 ProThermDB
  hyper-stable proteins are "not included in the MEGAscale experimental dataset" (Fig. 4 caption, p9),
  and for the 65 CALVADOS IDPs "Sequence similarity search indicated that there was only one protein
  with a similarity above 40% with respect to the training set of BioEmu" (p31).
- **anti_memorization_control**: **RUN — a control arm was actually executed and analysed, which is
  the rarer answer in this corpus — but PARTIALLY UNPOWERED per benchmark cell.**
  The arm is **Table S4 (p33)**, which splits every multi-conformation success rate by whether the
  reference structure predates or postdates the AF2 monomer cutoff. Result, verbatim from the main
  text (p4): *"We confirmed that the model's performance is similar for proteins that overlap with the
  AlphaFold2 training set and those that do not, indicating that the benchmark does not test
  capabilities that the model trivially extracted from evoformer embeddings (Table S4)."*
  The numbers (Table S4, p33; n_success is a bootstrap expectation):

  | Benchmark | pre-AF2 n_success / N | post-AF2 n_success / N |
  |---|---|---|
  | Domain motion | 23.89 / 26 | 13.64 / 18 |
  | Local folded | 13.16 / 18 | 1.00 / **2** |
  | Local unfolded | 9.00 / 11 | 6.30 / 9 |
  | Cryptic apo | 17.00 / 34 | 0.00 / **0** |
  | Cryptic holo | 26.96 / 32 | 2.00 / **2** |
  | **Total** | **90.01 / 121** | **22.94 / 31** |
  | **Success rate** | **0.744** | **0.740** |

  **Mark UNPOWERED at the cell level.** The pooled post-cutoff n = 31 is adequate; three of the five
  cells are not. Cryptic apo — the one benchmark where BioEmu is beaten by AFCluster and where the
  main text concedes "further room for improvement" (p6) — has **N = 0** post-cutoff, so the
  memorisation question is simply unanswered for the paper's weakest arm. Local folded (N = 2) and
  cryptic holo (N = 2) carry no statistical weight either. The headline 0.744 vs 0.740 agreement is
  therefore carried almost entirely by domain motion (N = 18) and local unfolded (N = 9). A second,
  independent control is the OOD60 arm (n = 19, Fig. S1 p34, Fig. S5a p38), where BioEmu's advantage
  over both baselines is largest; the authors themselves flag it as the only fair comparison ("all
  comparisons apart from those in the OOD60 benchmark test how well different models fit the data but
  it is not fair in terms of generalization", p38). Note also what the control does **not** cover: it
  tests the *AF2 encoder's* training set, not BioEmu's own MD training set, which is guarded only by
  the 40% sequence filter of route 1 above.
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Pretrained (AFDB-only) vs fine-tuned model, reported side by side on every multi-conformation benchmark | That the MD + ΔG fine-tuning is doing nothing; isolates the AFDB structural prior's contribution from the MD contribution | p5 (Fig. 2), p34–37 (Figs. S1–S4), p40 (Fig. S7) |
  | Pretraining-dataset ablation: augmented AFDB vs PDB vs high-pLDDT AFDB (~250 k sequences), scored on OODVal | That the AFDB augmentation strategy is incidental — "models trained on the PDB and the high pLDDT subset of AFDB are significantly worse in its capacity to sample diverse conformations" | p24–25, p39 (Fig. S6) |
  | Baselines AFCluster and AlphaFlow run on identical benchmarks with ColabFold MSAs and matched sample counts | That any generative method would score the same; establishes where BioEmu loses (cryptic apo) as well as wins | p31 (S.4.4), p38 (Fig. S5) |
  | Pre- vs post-AF2-cutoff split of all 152 benchmark references (Table S4) | That success is evoformer-embedding recall of structures AF2 already saw | p4, p33 |
  | OOD60: post-cutoff PDB pairs, ≤60% similar to AF2 training data and ≤40% to BioEmu training data | Sequence-level memorisation from both training corpora at once; the authors' own "fair" arm | p4, p29–30, p34, p38 |
  | Leave-one-out over 12 DESRES fast folders (fine-tune on 11, test on the 12th) | That the free-energy surfaces are reproduced because the test protein's own trajectory was in training | p6, p25, p40 |
  | CATH data-scaling: three from-scratch CATH-only models at 1%, 10%, 100% of training domains | That accuracy is saturated / that errors are model-capacity rather than data limited — "We observed decreased free energy errors and an increased coverage... as the amount of training proteins increased" | p8, p7 (Fig. 3b,iii) |
  | MEGAscale train vs test split of the ΔG scatter | Overfitting to the stability training set — "the errors are similar for both training and test set" (train 0.73 / test 0.76 kcal/mol) | p9 (Fig. 4a) |
  | 26 hyper-stable ProThermDB proteins, none in MEGAscale, ΔG < −8 kcal/mol | That the ΔG head only interpolates within MEGAscale's dynamic range; checks the stable extreme | p9, p31 |
  | 65 CALVADOS/IDRome IDPs, only one >40% similar to training data | That folded-state bias makes the model call everything folded; checks the disordered extreme, zero-shot | p9, p31 |
  | Two-force-field MD comparison for Complexin II (ff14sb vs ff99sb-disp, ~5 µs each) | That disagreement with any single MD force field is BioEmu's error rather than force-field spread — the two force fields disagree with each other | p8, p7 (Fig. 3c) |
  | ACE2 against 890 µs of published MD plus homologous PDB structures | That the ACE2 gate distribution is unconstrained; two independent references instead of one | p8, p7 (Fig. 3d) |
  | Unphysical-sample filter (chain breaks, clashes) applied before every metric, with residual clash fraction reported | That success rates are inflated by counting broken backbones as conformations | p30, p7 (Fig. 3a,iii / 3b,ii) |
  | Reported free-energy MAE restricted to "converged" test systems inside MSM-connected sets | Nothing — this is a *filter*, not a control, and it removes the hardest systems; recorded here so the restriction is visible | p8, p26, p31–32 |

- **confidence_as_discriminator**: **NO — and BioEmu emits no confidence score at all.** No pLDDT,
  pTM or ipTM is produced by the model, and none is used to judge conformational correctness anywhere
  in the evaluation. pLDDT appears only twice, both times in *training-data curation* of AFDB: as a
  filter ("we removed sequence clusters lacking at least one structure with pLDDT greater than 80, and
  with a pLDDT standard deviation lower than 15 across residues", p17) and as an input-sequence
  selection rule ("we always use the sequence associated with the highest pLDDT structure in the
  cluster as input to the model", p24). The discriminators BioEmu actually uses are the physical-
  plausibility filter (p30) and the free-energy weight of a sample, i.e. how often the state recurs
  across 10k draws. Do not tag `confidence-as-discriminator`.

## D. Claims

- **central_conclusion**: A sequence-conditioned diffusion model, pretrained on a
  structural-diversity-augmented subset of the AlphaFold database and fine-tuned on ~208 ms of
  reweighted all-atom MD plus ~776 k experimental folding stabilities, can emit 10,000 i.i.d. backbone
  structures per protein in minutes-to-hours on one GPU whose distribution approximates the 300 K
  equilibrium ensemble to within roughly 1 kcal/mol in relative free energy — four to five orders of
  magnitude cheaper than the MD it emulates. Qualitatively it recovers domain motions (85% of
  references at ≤3 Å), local unfolding (72%/74%) and cryptic pockets (85% holo, 49% apo), and its
  accuracy improves monotonically with training-data volume, which the authors read as evidence that
  the bottleneck is data rather than architecture.
- **necessity_claims** — **verbatim, with pages.**
  - The scope limitation, which is the most quotable sentence in the paper for any argument about what
    an MD emulator can be asked to do (p10): *"BioEmu and MD simulation are complementary: our system
    was trained on large amounts of MD simulation of soluble proteins, and within this scope, it has
    shown to be able to approximate MD distributions at a tiny fraction of the MD simulation costs.
    However, BioEmu cannot be expected to generalize beyond this scope — for example membrane
    environments and small molecule ligands are neither represented in the model nor in the training,
    and BioEmu can therefore not be expected to make reliable predictions when membranes or ligands
    play a key role in the process. For MD, generalizing to such conditions is straightforward,
    although obtaining results will be limited by the sampling problem."*
  - (p10): *"A proper emulator for proteins requires conditioning on experimentally and biologically
    relevant parameters such as temperature and pH, and needs to be able to model multiple interacting
    molecules, as proteins rarely have a function on their own."*
  - (p2): *"A demonstration that generative ML can quantitatively match equilibrium ensembles and
    predict experimental observables is critical going forward [19]."*
  - (p2): *"Available technologies that probe such conformational and binding states and their
    probabilities at high accuracy are currently not scalable."*
  - (p2): *"biomolecular forcefields are far from perfect and the sampling problem renders the study of
    protein folding or association via MD a feat of epic computational costs for small-sized proteins,
    even if special-purpose supercomputers or enhanced sampling methods are employed [8, 9]."*
  - (p6): *"the millisecond timescales often involved in the spontaneous opening of such pockets make
    MD on commercial hardware rarely viable for in-silico drug discovery pipelines."*
  - (p6–8): *"we also note that for most proteins shown here, performing sufficiently long MD
    simulations to directly observe folding and unfolding in single trajectories is still not possible
    on consumer-grade hardware but instead requires a much more complex methodological framework
    [28, 31]."*
  - (p8): *"Achieving convergence of IDPs of this size with all-atom MD is unpractical."*
  - (p10): *"MD forcefields... can also be tuned to fit experimental data [47], but the processes that
    give rise to the experimental observables must be sampled during the training process — a task
    that is tedious or even unfeasible for observables that involve complex rare events, such as
    folding free energies."*
  - (p27): *"Even more importantly, experimental observables such as ∆G can only be used in a standard
    diffusion model training approach if folded and unfolded structures are available, e.g. obtained
    via MD simulation, whose computational costs would limit us to rather few training systems."*
  - (p10): *"An important limitation of BioEmu is that it generates distributions entirely
    empirically, while MD simulation uses potential energy functions which are connected to
    equilibrium distributions and expectation values by statistical mechanics."*
  - (p9–10): *"These analyses highlight BioEmu's ability to correlate predictions of thermodynamics
    with structural causes, which is not possible with black-box prediction models."*
- **novelty_claims** — **verbatim, with pages.**
  - (p2): *"Here we set out to develop a first version of an ML system that can approximately sample
    from the equilibrium distribution of protein conformations within a few GPU-hours per experiment —
    a biomolecular emulator (BioEmu)."*
  - (p2), the implicit priority claim the paper is built against: *"As yet, generative ML systems have
    mainly demonstrated an ability to qualitatively sample distinct protein conformational states."*
  - (p4): *"As the MEGAscale dataset does not contain structures, we developed an new algorithm called
    property-prediction fine-tuning (PPFT) to efficiently incorporate experimental measurements into
    diffusion model training (Fig. 1f, Sec. S.3.6)."*
  - (p27): *"To avoid these limitations and take advantage of high-throughput experiments such as the
    ones in [21], we have developed a novel and efficient method that trains diffusion models to
    generated distributions that respect a given set of properties of these distributions, e.g.
    experimental expectation values."*
  - (p25): *"At this stage, in addition to the standard denoising diffusion loss, for those proteins
    where this information was available, we also use a novel loss to match experimental folding free
    energies by backpropagating through the sampling procedure (see S.3.6)."*
  - (p3): *"For model training and testing we have developed several new benchmarks and training
    methods to integrate the heterogeneous data modalities (Sec. S.1, S.3)."*
  - (p25): *"indicating that our curated subset of AFDB is an important contribution to facilitate
    multi-conformational learning."*
  - (p9): *"This accuracy outperforms other existing black box methods that predict ∆G values directly
    from sequences [38–41]."*
  - (p2): *"Importantly, our demonstration that the large upfront costs of MD simulation and
    experimental data generation can be amortized and the prediction error decreases with an
    increasing amount of diverse training data indicates a path forward for predicting biomolecular
    function at genomic scale."*
  - **Generalisation-beyond-training claims, quoted verbatim because they are the load-bearing
    sentences for any "emulation vs recall" argument:**
    - (p4): *"Due to the strict sequence similarity constraints, OOD60 only contains 19 proteins, but
      it features various challenging cases like large-scale conformational changes caused by binding
      to other biomolecules (Fig. S1). While it is uncertain if all of these conformational changes
      can be predicted by a single-domain model, the benchmark tests for strong generalization and we
      find that our model significantly outperforms the two considered baseline approaches (Fig.
      S5a)."*
    - (p4): *"We confirmed that the model's performance is similar for proteins that overlap with the
      AlphaFold2 training set and those that do not, indicating that the benchmark does not test
      capabilities that the model trivially extracted from evoformer embeddings (Table S4)."*
    - (p4): *"Furthermore, BioEmu outperforms other methods except for the apo states in the cryptic
      pocket benchmark, and the difference is especially large for the proteins outside the AlphaFold2
      training set (Fig. S5, b-d)."*
    - (p6): *"However, fine-tuning on only 11 sequences results in a surprisingly good match in the
      free energy surfaces of test proteins (Fig. 3a,i, Fig. S7)."*
    - (p9): *"In contrast to other works [44, 45], our model has not been directly trained on IDPs;
      nonetheless, it provides zero-shot predictions of Rg that correlate well with experimental
      measurements, albeit with overestimation of Rg values for longer sequences (Fig. 4c)."*
    - (p9): *"Interestingly, the errors are similar for both training and test set, indicating that
      the model generalizes well but cannot perfectly fit the training data, perhaps due to
      inconsistencies between the folded/unfolded state definitions between this work and what the
      experiment is sensitive to."*
    - (p38, Fig. S5 caption, and the honest counterweight to all of the above): *"Note that all
      comparisons apart from those in the OOD60 benchmark test how well different models fit the data
      but it is not fair in terms of generalization. Apart from potential Evoformer embedding leakage,
      for our method, all cases are in the test set, whereas for other methods cases before the AF
      cutoff date were present in the training set."*
- **stated_limits** — the authors are notably forthcoming; these are their words, condensed with
  pages, and the verbatim forms of the sharpest ones are in `necessity_claims`.
  1. **No generalisation beyond soluble single chains** — membranes and small-molecule ligands are in
     neither model nor training data, so predictions where they matter are unreliable (p10).
  2. **Single chains only, 300 K only** — no temperature, pH or partner conditioning (p10).
  3. **No potential energy function** — the distribution is empirical, so no reweighting and no
     rigorous enhanced sampling on top of the emulator (p10).
  4. **Backbone only** — side chains and hydrogens are not modelled (p22), which is why FNC and
     backbone RMSD are the only structural metrics available.
  5. **Cryptic apo states are a known weakness** — "Surprisingly the model has a strong preference for
     holo states and successfully predicts the cryptic pocket in 85% of cases, while it only succeeds
     in predicting 49% of the apo structures, indicating further room for improvement" (p6); AFCluster
     beats BioEmu there (p38).
  6. **Rg is overestimated for longer IDP sequences**, with two IDPs mis-called as folded (p9).
  7. **Data-limited, not capacity-limited** — accuracy still climbing with training-set size (p8),
     and "a key obstacle to extending the emulator to other scopes different from proteins, as well as
     further improving it for the current scope, is the lack of training data" (p10).
  8. **MD training data itself is imperfect and inconsistent** — mixed force fields chosen
     deliberately because "each of these MD models is inherently imperfect, and we regarded
     experimental data as being more reliable for weighing between conformations" (p8).
  9. **MD training data is not converged** and had to be reweighted by MSMs or experimental ΔG (p4,
     p26): "Since the MD simulations are too short to represent a converged sample of folding and
     unfolding events, the folding free energy estimated from histogramming the raw simulation data do
     not match their corresponding experimental measurements" (p26).
  10. **Free-energy MAE is only reported on systems with enough MD to build a TICA/HMM model**
      ("we have limited this analysis to a subset of test systems with sufficient MD data", p31).
  11. **Mutant MD rests on two stated assumptions** — that point mutations perturb only local
      interactions in the folded state and leave the unfolded ensemble unchanged, so unfolded samples
      were reused from wildtypes (p20).
  12. **ACE2 gate distribution is "similar albeit less flexible"** than 890 µs of MD (p8) — an
      under-dispersion the authors name rather than smooth over.
  13. **OOD60 may be unfair to the model itself** — several of its transitions are caused by binding
      partners a single-chain model cannot see: "While it is uncertain if all of these conformational
      changes can be predicted by a single-domain model" (p4).
- **stance**: **`precedent` on findings + `contrast` on rigour — PROVISIONAL, the user's call.**
  - *Precedent*, and the strongest in the corpus on this axis: this is the reference demonstration
    that a generative model can produce a *quantitative* equilibrium ensemble rather than a menu of
    distinct conformers, with free-energy errors benchmarked against millisecond MD and against
    experiment. It also does something most corpus papers do not: it defines a sequence-similarity
    hold-out (40%), builds a post-cutoff set (OOD60, n=19), and **actually runs** the pre/post-cutoff
    control arm (Table S4). Its self-stated scope limits (p10) are a ready-made citation for why an
    MD emulator is not a substitute for a state-directed structure predictor.
  - *Contrast* on rigour: success is defined post hoc by RMSD to references the authors held
    throughout (route 5); the headline per-reference metric is k-recall, the mean of the best 0.1% of
    samples chosen against that reference (route 6); the released checkpoint was selected on a
    conformational benchmark of deposited pairs (route 4); the anti-memorisation control's weakest
    cell has N = 0 (Table S4); the hold-out is by sequence only, with no fold-level criterion; and the
    free-energy metric carries an explicit numeric floor at pi = 10⁻⁴ (p32). None of these is
    concealed — the paper's own captions flag the encoder-leakage risk — but every one of them is a
    difference in evaluation standard that a comparison would have to state.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Relative free energy error (headline abstract claim) | ~1 (stated as "around 1") | kcal/mol | millisecond-timescale MD and experimental protein stabilities | p1 |
  | Macrostate free-energy MAE, DESRES fast folders (leave-one-out) | 0.74 mean; 0.30 (BBA) – 1.63 (λ-repressor) range | kcal/mol | DESRES Anton MD 2-D TICA free energy surfaces | p6 |
  | Macrostate free-energy MAE, CATH test set (17 domains >100 µs) | 0.91 | kcal/mol | in-house Amber MD free energy surfaces | p8 |
  | Folding ΔG MAE, MEGAscale (headline) | < 0.8 | kcal/mol | MEGAscale cDNA-display-proteolysis ΔG | p9 |
  | Folding ΔG MAE, MEGAscale train split | 0.73 | kcal/mol | MEGAscale experimental ΔG | p9 (Fig. 4a annotation) |
  | Folding ΔG MAE, MEGAscale test split | 0.76 | kcal/mol | MEGAscale experimental ΔG | p9 (Fig. 4a annotation) |
  | Spearman correlation, ΔG (headline) | > 0.65 | — | MEGAscale experimental ΔG | p9 |
  | Correlation, ΔG train / test split | 0.67 / 0.66 | — | MEGAscale experimental ΔG | p9 (Fig. 4a annotation) |
  | Domain-motion coverage at ≤3 Å global backbone RMSD | 85 | % of reference structures | 22 curated domain-motion PDB pairs | p4 |
  | Local unfolding coverage, folded state (FNC ≥ 0.7) | 72 | % of references | 20–21 local-unfolding examples | p6 |
  | Local unfolding coverage, unfolded state (FNC ≤ 0.3) | 74 | % of references | 20–21 local-unfolding examples | p6 |
  | Cryptic pocket coverage, holo, at ≤1.5 Å local RMSD | 85 | % of references | 34 curated apo/holo pairs | p6 |
  | Cryptic pocket coverage, apo, at ≤1.5 Å local RMSD | 49 | % of references | 34 curated apo/holo pairs | p6 |
  | Multi-conformation success rate, references **pre**-AF2 cutoff | 0.744 (90.01 successes / 121 refs) | fraction | pooled domain motion + local unfolding + cryptic | p33 (Table S4) |
  | Multi-conformation success rate, references **post**-AF2 cutoff | 0.740 (22.94 / 31) | fraction | pooled; cryptic-apo cell is N=0 | p33 (Table S4) |
  | ACE2 HEXXH+E active-site backbone RMSD | < 1.5, for all samples | Å | crystal structure of the HEXXH+E motif | p8 |
  | ΔΔG, HHH_rd1_0335 I7P (predicted vs experimental) | 1.3 vs 2.1 | kcal/mol | MEGAscale experiment | p10 |
  | ΔΔG, 2JWS I24D (predicted vs experimental) | 1.5 vs 2.9 | kcal/mol | MEGAscale experiment | p10 |
  | ΔΔG, 2ZW1_Y34A → E57H (predicted vs experimental) | 1.9 vs 1.2 | kcal/mol | MEGAscale experiment | p10 |
  | Inference cost, 10k samples | < 1 GPU-minute (Chignolin) to ~1 GPU-hour (λ-repressor); "on the order of one GPU-hour per computational experiment" | GPU-hours (NVIDIA Titan V) | — | p6, p10 |
  | MD cost for the equivalent DESRES trajectories | 2,000 (Chignolin) to > 100,000 (NTL9) | GPU-hours | DESRES Anton datasets sized for ~10 folding-unfolding round trips | p6 |
  | Speed advantage of emulator over MD | 4–5 | orders of magnitude | as above | p6 |
  | Denoising steps at inference | 100 (second-order/Heun sampler) | steps | — | p3, p23 |
  | Denoising steps inside PPFT training | 35 total, foldedness read after 8 | steps | — | p9, p28 |
  | ProThermDB hyper-stable check | FNC always > 0.65 threshold; 26 proteins | — | ProThermDB ΔG < −8 kcal/mol proteins | p9, p31 |
  | CALVADOS IDP check | 63 of 65 predicted unfolded (2 exceptions); Rg correlates with experiment, overestimated at long length | — | IDRome/CALVADOS experimental Rg and Flory scaling | p9, p31 |
  | Total MD training data | 172.2 raw / 216.0 effective (chains counted separately); 207.8 effective excluding DESRES | ms | — | p18 (Table S1), p20 |
  | CATH share of MD training data | 46 (41.0 CATH2 + 5.2 CATH1), over ~1100 domains | ms | — | p8, p18 |
  | Experimental stability measurements used | ~776,000 (main text: "over 750,000") | ΔG/ΔΔG entries | MEGAscale Dataset2+Dataset3 | p8, p21 |
  | Training compute | ~5 days × 32 A100 (pretrain); ~5 days × 4 A100 (fine-tune); ~3 days × 4 A100 (DESRES) | — | — | p24 (Table S2) |
  | Data-scaling trend, CATH-only models at 1/10/100% | free-energy MAE decreases and state coverage increases monotonically (exact values only in figure) | kcal/mol, fraction | CATH test set | p8, p7 (Fig. 3b,iii) |

- **n_predictions**: record the three levels separately; a single total is not what a power comparison
  needs.
  - **Samples per target: 10,000, uniformly.** p6: "For all BioEmu results shown here, we draw 10k
    samples". This fixes the resolution floor at 1/10,000 = 10⁻⁴ in probability, i.e. ≈5.5 kcal/mol at
    300 K, and defines the 0.1% coverage criterion as "at least 10 of 10,000 samples".
  - **Targets per benchmark**: OOD60 19; domain motion 22; local unfolding 21; cryptic pocket 34
    pairs; OODVal 11 (model selection); DESRES 12 (each with its own leave-one-out model); CATH test
    17; ProThermDB 26; CALVADOS IDPs 65; MEGAscale train + test (n per split **NOT REPORTED**);
    Complexin II and ACE2 as single case studies. Reference *structures* scored: 152 (Table S4, p33).
  - **Total samples**: never stated as one number. Lower bound from the enumerated benchmarks alone
    is on the order of 2 × 10⁶ structures (≈200 distinct targets × 10⁴), before the MEGAscale scatter
    of Fig. 4a, which is the largest arm and whose n is not given.
  - **Baseline sampling**: "In the case of AlphaFlow, the same number of samples were drawn as for our
    model, whereas for AFCluster, the number of samples was limited to the number of clustered MSAs
    generated by the method" (p31). AFCluster is therefore sampled at a *much* lower and
    target-dependent depth than BioEmu's 10k — a matched-budget comparison this is not, and it is the
    one place a baseline comparison in this paper is structurally unfair in BioEmu's favour.
- **comparable_to_ours**: *(left empty by the extractor per schema v3)*
- **si_in_scope**: **SI HELD — pages 15–41 of the PDF.** Supplementary Methods S.1–S.6, Table S1
  (MD dataset composition), Table S2 (training hyperparameters), Table S3 (MD dataset mixture
  weights), Table S4 (pre/post-AF2-cutoff success rates) and Figures S1–S8 are all present and were
  read. Consequently `metrics_reported` is not hollowed out, which is the failure mode `si_in_scope`
  exists to flag.
  **What is NOT held:** (i) the separate "Supplementary Data" file with per-benchmark PDB/chain
  identifiers and residue-level alignment labels (p29) — so the exact composition of every benchmark
  cannot be audited from the PDF; (ii) per-system numeric values behind Figs. S1–S8 and Fig. 3b,iii,
  which exist only as plotted curves — the data-scaling MAE values, the per-protein MAE and clash
  fractions, and the per-entry recall scatter points are all figure-only; (iii) the n per split of the
  MEGAscale train/test scatter (Fig. 4a). Code and benchmarks are open — MIT licence, at
  `https://github.com/microsoft/bioemu` and `https://github.com/microsoft/bioemu-benchmarks` (p11) —
  so those gaps are recoverable outside the PDF.

## F. Figures

One row per panel group; split on `mark` or `measure`, not on `facet`.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A-F | 3 | Actin functional cycle, BioEmu architecture, score-model block diagram, three-stage training pipeline, AFDB preprocessing funnel, PPFT loop | schematic | `SCHEMATIC \| model architecture, data-integration pipeline and AFDB/PPFT preprocessing flows \| no data` | 6 lettered panels (a–f); vary by subject, not by condition | — | CC-BY-NC-**ND** 4.0 (p1 banner, every page). **ND forbids derivatives: redrawing is prohibited, not only copying.** NC also bars commercial use. |
| 2A-C(cov) | 5 | Cumulative coverage of reference conformations vs metric threshold, pretrained vs fine-tuned, for all three conformational-change classes | line | `PLOT \| facet: benchmark arm (5: domain motion, local unfolding-unfolded, local unfolding-folded, cryptic apo, cryptic holo) \| vary: metric threshold (RMSD 0–10 Å; RMSD 0–4.5 Å; FNC 0–1) (continuous) \| series: training stage (2: pretrained, finetuned) \| measure: fraction of references covered at 0.1% of samples \| mark: line \| n: 10,000 samples per protein; 22 / 21 / 21 / 34 / 34 references per panel` | 5 sub-panels in the left column of a/b/c; vary by benchmark arm | **Curves ceiling at 1.0 within every panel's plotted range** for domain motion, cryptic holo and both local-unfolding arms, so pretrained and fine-tuned are indistinguishable over the right half of each axis — cross-reference `metric_saturation`. No confidence band and no n printed on the panels. | as above (ND) |
| 2A,C(fes) | 5 | Per-example 2-D empirical free-energy density over RMSD to reference 1 vs RMSD to reference 2, for six domain-motion and cryptic-pocket cases | heatmap | `MATRIX \| rows: RMSD to reference 1 (binned, Å) \| cols: RMSD to reference 2 (binned, Å) \| value: empirical free energy from sample density (kcal/mol) \| facet: example system (6: 3 domain motion, 3 cryptic pocket)` | 6 density panels with dashed success thresholds | Colour scale is truncated at the top (contour outline marks the 4 kcal/mol = 0.1% boundary), so the tail beyond the resolution floor is not shown; no colourbar units on several panels | as above (ND) |
| 2B(fes) | 5 | 1-D free-energy profile along fraction of native contacts for three local-unfolding examples | line | `PLOT \| facet: example system (3: Ras p21, Rhomboid protease, CaM Kinase II) \| vary: fraction of native contacts, 0–1 (continuous) \| series: none (1) \| measure: free energy (kcal/mol) \| mark: line \| n: 10,000 samples per panel` | 3 panels with shaded regions above the 4 kcal/mol cut and dashed state boundaries | Free energy is visually clipped at the shaded 4 kcal/mol ceiling (the 0.1%-of-10k resolution floor), which hides how badly an unsampled state is missed | as above (ND) |
| 2A-C(rend) | 5 | BioEmu samples (green) overlaid on experimental reference structures (grey) for nine examples, plus surface close-ups of three cryptic pockets | structure render | `RENDER \| facet: conformational class (3) × example system (9 total) × reference state (2: reference 1, reference 2) \| views: 1 (plus 2 zoomed surface insets per cryptic-pocket example) \| overlay: NOT REPORTED predictions on 1 reference per sub-panel \| axis: none` | ~24 render sub-panels; vary by system and by reference state | **Number of overlaid samples is never given** — the caption says only that examples are "using BioEmu", so a render showing a close match could be 1 of 10,000. This is the classic best-sample-render case; the quantitative answer is in the coverage panels, not here | as above (ND) |
| 3A-B(rend) | 7 | Model (green) and MD (grey) structures for three fast folders and three CATH domains, in folded and partially/unfolded states, with flexible motifs colour-coded | structure render | `RENDER \| facet: protein (6: BBA, Protein G, Homeodomain, 2wg5F02, 3udcA02, 4o96A01) × state (3–4: folded plus numbered partially/unfolded states) \| views: 1 \| overlay: NOT REPORTED model samples on 1 MD representative per state \| axis: none` | ~22 render sub-panels; vary by protein and by macrostate | Representative-structure selection rule is not stated (which of 10,000 samples is drawn) | as above (ND) |
| 3A-B(fes) | 7 | Free energy surfaces in the space of the two slowest TICA components, MD vs model, for three fast folders and three CATH domains | heatmap | `MATRIX \| rows: TIC 1 (binned) \| cols: TIC 2 (binned) \| value: free energy (kcal/mol) \| facet: protein (6) × source (2: ground-truth MD, fine-tuned model)` | 12 surface panels, numbered macrostate labels overlaid | Colour scale is capped at 6.0 kcal/mol on every panel, and the clamp at pi = 10⁻⁴ (p32) means an entirely unsampled macrostate renders identically to a merely rare one | as above (ND) |
| 3A-B(ss) | 7 | Per-residue secondary-structure propensity, MD vs BioEmu, for the same six proteins | line | `PLOT \| facet: protein (6) × source (2: MD, BioEmu) \| vary: residue index (continuous, 1–N) \| series: secondary structure type (2: helix, sheet) \| measure: propensity, 0–1 \| mark: line \| n: 10,000 samples (model) vs full trajectory (MD) per panel` | 12 strip panels down the right of a,i and b,i | No error band on either the MD or model propensity, so agreement cannot be judged against sampling noise | as above (ND) |
| 3A(ii) | 7 | GPU-hours for BioEmu vs DESRES MD as a function of protein length, log scale | scatter | `PLOT \| facet: none (1) \| vary: protein length, ~10–80 amino acids (continuous) \| series: cost source (3: full DESRES MD, single folding-unfolding round trip, BioEmu 10k samples) \| measure: compute cost (GPU-hours, log axis) \| mark: point \| n: 1 per mark, 12 proteins per series` | 1 panel, 12 proteins × 3 series with drop lines to labels | Log axis spans ~5 decades, which is the honest scale for the claim but visually compresses the 30× spread *within* the BioEmu series | as above (ND) |
| 3A(iii)+3B(ii) | 7 | Per-protein macrostate free-energy MAE and clash fraction, fine-tuned vs pretrained, for the 12 fast folders and the CATH test set | scatter (Cleveland-style) | `PLOT \| facet: benchmark (2: DESRES fast folders, CATH test) × metric (2: free-energy MAE, fraction of unphysical samples) \| vary: protein (12 and ~17, categorical) \| series: training stage (2: finetuned, pretrained) \| measure: macrostate MAE (kcal/mol) and clash fraction \| mark: point \| n: 1 per mark; 10,000 samples behind each` | 4 strip panels, one point per protein per stage, with a "mean" column | The per-protein numeric values exist only as plotted points — the SI carries no table for them (see `si_in_scope`); the "mean" column pools proteins of very different difficulty | as above (ND) |
| 3B(iii) | 7 | Free-energy MAE and state coverage of CATH-only models as a function of the fraction of CATH training domains used | line | `PLOT \| facet: metric (2: macrostate free-energy MAE, state coverage) \| vary: percentage of CATH training data, 1–100% (continuous, log axis) \| series: none (1) \| measure: MAE (kcal/mol) and coverage (fraction) \| mark: line \| n: 3 trained models per panel, plus BioEmu shown as a single star` | 2 small panels | **Three points define each trend line** and no uncertainty is shown, yet the monotonic-improvement claim on p8 and the "path forward at genomic scale" claim on p2 both lean on it | as above (ND) |
| 3C | 7 | Complexin II: per-residue helicity and radius-of-gyration distribution, BioEmu vs two Amber force fields, with an ensemble render | line + structure render | `PLOT \| facet: model/force field (3: BioEmu, ff99sb-disp, ff14sb) \| vary: residue index, 1–134 (continuous) \| series: none (1) \| measure: helix content and radius of gyration \| mark: line \| n: 10,000 samples (BioEmu) vs ~5 µs MD (each force field)`; render companion: `RENDER \| facet: model/force field (3) \| views: 1 \| overlay: NOT REPORTED sampled structures superposed \| axis: none` | 3 helicity strips + 3 Rg traces + 3 ensemble renders | The MD arms are explicitly non-converged ("most likely not converged", p8) but are plotted with the same visual weight as the model, and no n or error band is shown for any arm | as above (ND) |
| 3D | 7 | ACE2 helix-gate opening as a joint distribution of two inter-helix distances, and HEXXH+E motif RMSD, BioEmu vs 890 µs MD | scatter + histogram + structure render | `PLOT \| facet: measurement (2: gate-distance joint distribution, HEXXH+E backbone RMSD) \| vary: gate distance d1, 3.0–4.5 nm (continuous) / backbone RMSD, 0–1.5 Å (continuous) \| series: source (3: extensive MD, homologous PDB structures, BioEmu samples) \| measure: gate distance d2 (nm) / sample density \| mark: point and filled density \| n: 10,000 BioEmu samples; 890 µs MD; homologous PDB count NOT REPORTED` | 1 render + 1 joint scatter + 1 paired density | The BioEmu cloud is visibly narrower than the MD cloud — the under-dispersion the text concedes ("similar albeit less flexible", p8) — but no dispersion statistic is given, so the gap can only be eyeballed | as above (ND) |
| 4A | 9 | Predicted vs experimental folding free energy, train and test splits | scatter | `PLOT \| facet: split (2: train, test) \| vary: predicted ΔG, −5 to +2 kcal/mol (continuous) \| series: none (1) \| measure: experimental ΔG (kcal/mol) \| mark: point with horizontal error bar \| n: 1 per mark; per panel NOT REPORTED (visually ~10³ points)` | 2 panels with a shaded ±1 kcal/mol band and in-panel error/correlation annotations | **n is not stated for either split** — the single most reusable comparator table in the paper rests on an unreported sample size; heavy overplotting in the dense central region | as above (ND) |
| 4B | 9 | Fraction of native contacts sampled for hyper-stable ProThermDB proteins, with a representative render | box/interval | `PLOT \| facet: none (1) \| vary: protein (9 labelled PDB IDs shown of 26 in the benchmark) \| series: none (1) \| measure: fraction of native contacts, 0–1 \| mark: box/interval \| n: 10,000 samples per protein; 26 proteins in the benchmark, 9 plotted` | 1 interval panel + 1 structure render (1A23) | **9 of 26 benchmark proteins are shown and the selection rule is not stated** — the claim "Our model consistently samples these proteins in their folded states with a fraction of native contacts always exceeding the 0.65 threshold" (p9) covers all 26, the figure evidences 9 | as above (ND) |
| 4C | 9 | Radius of gyration vs sequence length for 65 IDPs: model, experiment, folded-PDB reference and ideal-random-coil scaling | scatter | `PLOT \| facet: none (1) \| vary: sequence length, ~50–450 residues (continuous) \| series: source (4: folded PDB, ideal random coil, sampled Rg, reference Rg) \| measure: radius of gyration (nm) \| mark: point and line \| n: 65 IDPs; 10,000 samples behind each model point` | 1 panel | The two mis-called IDPs conceded in the text (p9) are not marked or identified in the panel | as above (ND) |
| 4D(rend) | 9 | Wild-type and mutant structures for three destabilising mutations, with the mutated site highlighted | structure render | `RENDER \| facet: system (3: HHH_rd1_0335 I7P, 2JWS I24D, 2ZW1_Y34A E57H) × variant (2: wild type, mutant) \| views: 1 \| overlay: NOT REPORTED sampled structures on 1 reference \| axis: none` | 6 render sub-panels | Number of samples behind each render not stated | as above (ND) |
| 4D(prop) | 9 | Per-residue helix or sheet propensity, wild type vs mutant, with the mutation site marked | line | `PLOT \| facet: system (3) \| vary: sequence position (continuous, sequence printed on axis) \| series: variant (2: wild type, mutant) \| measure: α-helix or β-sheet propensity, 0–1 \| mark: line \| n: 10,000 samples per variant per panel` | 3 panels, dashed vertical line at the mutation site | Shaded band shown without a stated definition (SD, SEM or percentile is not given in the caption) | as above (ND) |
| S1,S2,S4 | 34, 35, 37 | Per-example 2-D free-energy landscapes over RMSD to each of two references, pretrained and fine-tuned, for the full OOD60 (19), domain-motion (22) and cryptic-pocket (34) benchmarks, with reference renders | heatmap + structure render | `MATRIX \| rows: RMSD to reference 1 (binned, Å) \| cols: RMSD to reference 2 (binned, Å) \| value: empirical free energy from sample density (kcal/mol) \| facet: benchmark (3) × example (19 / 22 / 34) × training stage (2: pretrained, finetuned)`; render companion: `RENDER \| facet: example (75 total) \| views: 1 \| overlay: 2 reference structures (red = state 1 / apo, yellow = state 2 / holo, holo contact residues black in S4) \| axis: none` | ~150 landscape panels plus paired renders across three full-page figures; vary by example and training stage | Dashed success thresholds (3 Å in S1/S2, 1.5 Å in S4) are drawn but colour scales are per-panel and unlabelled, so panels are not comparable to each other by eye | as above (ND) |
| S3 | 36 | Per-example 1-D free-energy profile along fraction of native contacts for all 21 local-unfolding cases, pretrained vs fine-tuned | line | `PLOT \| facet: example (21) \| vary: fraction of native contacts, 0–1 (continuous) \| series: training stage (2: pretrained black, finetuned blue) \| measure: free energy (kcal/mol) \| mark: line \| n: 10,000 samples per curve` | 21 panels + a shared legend, paired with folded-state renders | Free energy clipped at the resolution ceiling as in Fig. 2B; the unfolded-state reference is by construction absent, so only the folded endpoint is anchored | as above (ND) |
| S5A,S6A | 38, 39 | Coverage vs threshold for BioEmu (pretrained and fine-tuned) against AlphaFlow and AFCluster, across six benchmark arms (S5) and on OODVal across three pretraining datasets (S6) | line | `PLOT \| facet: benchmark arm (6 in S5: OOD60, domain motion, cryptic holo, cryptic apo, local unfolding unfolded, local unfolding folded; 1 in S6) \| vary: metric threshold (RMSD 0–12 Å / 0–6 Å; FNC 0–1) (continuous) \| series: method (4 in S5: pretrained, fine-tuned, AlphaFlow, AFCluster; 3 in S6: augmented AFDB, PDB, high-pLDDT AFDB) \| measure: percentage of reference states covered \| mark: line \| n: 19 / 44 / 34 / 34 / 20 / 20 references per panel; 10,000 samples per protein for BioEmu and AlphaFlow, MSA-cluster-limited for AFCluster` | 7 coverage panels across two figures; vary by benchmark arm | **AFCluster is sampled at a different and much smaller budget than the other methods** (p31) while sharing an axis with them, and the panels carry no confidence bands; the caption, to its credit, states the generalisation caveat explicitly | as above (ND) |
| S5B-C,S6B-C | 38, 39 | Per-entry paired comparison of the recall metric: BioEmu pretrained on the independent axis, AlphaFlow or AFCluster on the dependent axis, coloured by AF2-training-set membership | scatter | `PLOT \| facet: benchmark arm (6 in S5, 1 in S6) × baseline (2: AlphaFlow, AFCluster) \| vary: recall RMSD or recall FNC of BioEmu pretrained (continuous) \| series: AF2 training-set membership (2: in AF2 training set red, NOT in AF2 training set blue) \| measure: recall RMSD or recall FNC of the baseline method \| mark: point with error bars \| n: 1 per mark; 19 / 44 / 34 / 34 / 20 / 20 points per panel` | 12 scatter panels in S5 + 2 in S6, each with a y=x diagonal | The independent axis is the **pretrained** model, not BioEmu proper, while the coverage column beside it plots both — so the head-to-head panels understate the released model; the measure itself is k-recall, the mean of the best 0.1% of samples chosen against the held reference (`oracle_leakage` route 6) | as above (ND) |
| S7,S8 | 40, 41 | Free-energy surfaces in TICA space (MD, fine-tuned, pretrained) plus secondary-structure profiles and macrostate renders, for all 12 DESRES fast folders (S7) and all CATH domains with >100 µs MD (S8) | heatmap + line + structure render | `MATRIX \| rows: TIC 1 (binned) \| cols: TIC 2 (binned) \| value: free energy (kcal/mol) \| facet: protein (12 in S7, 17 in S8) × source (3 in S7: MD, fine-tuned, pretrained; 2 in S8: MD, fine-tuned)`; secondary-structure companion has the same shape as row `3A-B(ss)` | ~70 surface panels plus per-protein structure columns and secondary-structure strips | Pretrained column is present in S7 but dropped in S8, so the ablation is not carried through both datasets; per-panel colour scales again differ | as above (ND) |

**Licence note, recorded once because it governs every row:** the whole preprint, figures included, is
**CC-BY-NC-ND 4.0** (p1 banner, repeated on all 45 pages). The **ND clause forbids derivative works**,
which means these figures may not be redrawn, recoloured, cropped or adapted — only reproduced whole
with attribution, and not for commercial purposes. The *code and benchmark* repositories are separately
MIT-licensed (p11), so regenerating equivalent figures from re-run code is the clean route.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), session of 2026-09-08
- **schema_version**: `v3`
- **confidence**: **high** for identity, scope, training composition, oracle-leakage routes,
  anti-memorisation design and control, claims and metrics — all of these are stated explicitly, most
  of them twice (main text and SI), and the SI is held. **Medium** for the figure table: four pages
  (5, 7, 9, 38) were rendered at 110 dpi and read directly, so those rows are solid, but Figs. S1–S4
  and S6–S8 were catalogued from captions plus the shape established by their rendered siblings, and
  the exact per-panel counts for S1–S4 and S8 are inferred from the stated benchmark sizes rather than
  counted panel by panel. **Medium** on two specific numbers flagged in `unresolved` below. What was
  hard to read: Fig. 1 is a dense six-panel schematic whose text layer extracts as scattered fragments
  and whose arrows carry meaning that neither the caption nor the text layer preserves; and the
  `data_shape` form for a 2-D free-energy density was a genuine judgement call (see below).
- **unresolved**:
  1. **Venue split.** The held PDF is the bioRxiv preprint (v. 25 Feb 2025, DOI
     10.1101/2024.12.05.626885). The task brief states a *Science* 2025 version exists at DOI
     **10.1126/science.adv9817**. That version was **not read**. Any number in this note may have
     changed in peer review — in particular the benchmark sizes, the pre/post-cutoff control table and
     the free-energy MAEs. Tagged `preprint`, not `peer-reviewed`. Someone should re-extract §E and
     Table S4 against the Science version before quoting figures in a manuscript.
  2. **Local-unfolding benchmark size: 20 or 21?** Main text p6 says "72% of locally folded and 74% of
     locally unfolded states across 20 protein examples"; SI p29 says "Local unfolding: A set of 21
     examples"; Table S4 (p33) sums to 20 folded references and 20 unfolded. Fig. S3 (p36) shows 20
     labelled panels. The discrepancy is not explained.
  3. **Does the processed PDB set train the released model?** S.1.2 (p17) describes a full PDB
     preprocessing pipeline under the "Data" heading, but the only use of PDB training data anywhere in
     the text is the pretraining *ablation* of Fig. S6 (p25), which found PDB pretraining worse. It is
     not stated whether the processed PDB set contributes to the released BioEmu. Recorded in
     `structural_priors_used` as a caveat rather than resolved either way.
  4. **MEGAscale train/test split sizes are never given** (Fig. 4a, p9), so the headline ΔG MAE of
     0.76 kcal/mol on test carries no n.
  5. **Mutant MD count mismatch**: p27 says "we conducted a large number of MD simulations for 22,389
     protein sequences from the MEGAscale dataset", p19 says "1 µs simulations for each of the 22,118
     point mutants", and the surviving dataset after filtering is 21,458 mutants (p20, Table S1 p18).
     The three numbers are reconcilable in principle (22,118 + 271 = 22,389) but the paper does not
     reconcile them.
  6. **Success threshold justification.** The 1.5 Å cryptic-pocket threshold is justified in words
     (p6); the 3 Å domain-motion threshold and the 0.3/0.7 FNC state boundaries are stated (p33, p36)
     but never justified. Recorded in `state_metric` as thresholds-without-justification.
  7. **Tags I needed and could not use — none invented.**
     - **`templates-off`** (or `msa-on-templates-off`). The Protocol vocabulary offers only
       `no-template-no-msa`, `templates-on` and `state-annotated-input`. BioEmu uses a full MSA with
       templates *completely excluded* (p21), which is none of the three. **No protocol tag is applied
       to this note**, which means a protocol-based reverse lookup will not find BioEmu at all. This is
       a real hole in the vocabulary, not a property of this paper — any AF2-derived method that keeps
       MSAs and drops templates hits it.
     - **`no-directional-control`** (or `unconditional-sampler`). The Control vocabulary presupposes a
       state handle. BioEmu has none: it is conditioned on sequence alone. `seed-only` is the nearest
       but is wrong — it implies seed-varied AF2 inference, whereas BioEmu's samples are i.i.d. draws
       from a learned distribution, which is a different mechanism with different statistics. I applied
       `apo-sampling` (which is genuinely true of the cryptic-pocket arm) and left the absence of a
       handle recorded in `directional_control` prose only.
     - **`data-scaling`** or similar. Fig. 3b,iii is a training-set-size scaling curve, which is a
       distinctive and citable result type with no tag. Minor.
     - Tags I considered and deliberately **declined**: `fold-switching` (local unfolding is not fold
       switching, and although some examples come from Chakravarty & Porter's fold-switching benchmark
       (p29), the paper never studies metamorphic proteins as such); `md` (the v3 note explicitly says
       `md-emulator` is neither `md` nor `cofolding`); `multi-backbone` (three methods, one backbone);
       `visual-metric` (visual inspection appears in training-data curation, p19, and benchmark
       curation, p30, but not as a reported state metric); `experimental-validation` (no new wet-lab
       work — every experimental comparison is against pre-existing datasets); `allosteric-site`
       (mentioned as a use case on p2, never studied).
  8. **Schema ambiguity in v3, stated bluntly since the schema is still being tuned.**
     - **A 2-D free-energy density / contour plot has no clean home.** Fig. 2a/c, Fig. 3a/b, Figs.
       S1–S2, S4, S7–S8 are all of this type: both axes are *continuous physical measures* (RMSD to a
       reference, or a TICA component), and the colour encodes a *derived* quantity (free energy from
       binned sample density). PLOT is wrong because the dependent measure is neither axis; MATRIX
       says "rows and cols are indices", which continuous binned axes are only after discretisation.
       I chose MATRIX and wrote the binning into the slot values, because putting free energy in
       `measure:` and one RMSD axis in `vary:` would silently drop the other axis. But this is a
       judgement call, and since this figure family is the entire visual output of every MD-emulator
       and enhanced-sampling paper, **v4 should either add a DENSITY form or state explicitly that
       binned continuous axes are legal MATRIX rows/cols.** Two extractors will otherwise split.
     - **`state_metric` says "may be dual" and this paper needs three** (RMSD-to-reference, binary
       predicate, continuous coordinate), each genuinely load-bearing for a different arm. I wrote all
       three joined by ` + `. If dual is meant as a hard cap, the rule needs restating; if not, say
       "may be multiple".
     - **`n_targets` has no place for a benchmark's reference-structure count as distinct from its
       protein count.** A 34-pair cryptic benchmark is 34 proteins and 68 references, and Table S4
       scores references. I recorded both, but the field's grammar does not ask for it.
     - **`anti_memorization_control` has no way to record "the control was run and is adequately
       powered in aggregate but has an empty cell in the arm that matters most."** UNPOWERED is a
       single flag; here the pooled n is 31 (fine) while cryptic-apo post-cutoff is N = 0 (fatal for
       that arm). I wrote both into the field, but a per-cell qualifier would be the cleaner fix.
     - **`metric_saturation` vs `hides` boundary held up well** on the coverage ceilings, but the
       clamp at pi = max(pi, 10⁻⁴) (p32) is an interesting third case: it is numeric saturation
       *deliberately introduced by the authors as a stated resolution boundary*, not an accidental
       floor. The field has no way to mark "acknowledged" versus "unacknowledged" saturation, and the
       distinction matters for how harshly it reads.
- **why_it_matters**: *(left empty by the extractor per schema v3)*

## Tags

`general-protein` `kinase` `periplasmic-binding` `md-emulator` `ensemble` `continuum`
`continuous-metric` `binary-predicate` `rmsd-only` `saturating-metric` `oracle-leak`
`design-level-oracle` `anti-memorization` `unpowered` `apo-sampling` `cryptic-pocket` `preprint`
`precedent` `contrast` `comparator-numbers`

Justification for the non-obvious ones, so a later re-tagging pass can check the reasoning:

- **`md-emulator`** — the defining tag, and the reason this paper is in the corpus. A generative model
  trained on MD trajectories; explicitly neither `md` nor `cofolding` per the v3 vocabulary note.
- **`kinase`** — protein kinases only, per the v3 scoping note: 6.8 ms of DDR1 kinase MD in training
  (Table S1, p18, p20) and CaM Kinase II (Fig. 2b,iii, p5), CaM Kinase I, DCLK1 and Titin Kinase in
  the local-unfolding benchmark (Fig. S3, p36). **Adenylate kinase (Fig. 2a,i) does not count** and is
  not the basis for this tag.
- **`periplasmic-binding`** — six or more solute/periplasmic binding proteins are named benchmark
  systems in the domain-motion arm (LAO-binding protein, Glutamine Binding Protein, D-ribose binding
  protein, Dipeptide Binding Protein, Oligopeptide-binding protein A, L-cystine solute receptor;
  Fig. 2a,ii p5 and Fig. S2 p35). A judgement call — the paper is not *about* them — but a reverse
  lookup for periplasmic-binding conformational change would be right to surface this paper.
- **`ensemble` + `continuum`** — the output is 10k i.i.d. samples (ensemble) used to build continuous
  free energy surfaces over TICA and RMSD coordinates (continuum). Not `single-state` — there is no
  collapse result here; the failure mode reported is under-dispersion (ACE2, p8), not collapse.
- **`rmsd-only`** — applied narrowly: RMSD to a held reference is the *sole* metric for the OOD60,
  domain-motion, cryptic-pocket and OODVal benchmarks (p29–30). It is **not** the whole paper (FNC and
  free-energy MAE carry §4–§5), which is why `continuous-metric` and `binary-predicate` are tagged
  alongside it. A reverse lookup for RMSD-only conformational scoring should find this paper's §3.
- **`saturating-metric`** — coverage curves ceiling at 1.0 within every panel's range (Fig. 2, Fig.
  S5), and the free-energy metric is explicitly clamped at pi = 10⁻⁴ (p32).
- **`oracle-leak` + `design-level-oracle` together** — both are present and they are distinct. Pipeline
  level: the released checkpoint was selected on the OODVal conformational benchmark of deposited
  pairs (p24, route 4), success is a post-hoc distance predicate (route 5), and k-recall picks the
  best 0.1% of samples against the held reference (route 6). Design level: every benchmark is a set of
  deposited pairs chosen because both endpoints are solved, and the apo sequence is chosen knowing
  which is apo (routes 3 and 7).
- **`anti-memorization` + `unpowered` together** — a control arm was genuinely run and analysed
  (Table S4, p33), which earns the first tag; three of its five cells have N ≤ 2 and the
  cryptic-apo cell is N = 0, which earns the second. Do **not** read `unpowered` as "no control was
  run"; that would be `no-anti-memorization`, which is wrong here.
- **`apo-sampling`** — the cryptic-pocket arm samples the apo sequence explicitly and reports apo
  success separately (49%, p6, p30). Not a directional handle; a benchmark arm.
- **`precedent` + `contrast`** — both, provisional; see `stance` for the reasoning on each half.
- **No protocol tag** — templates are off and MSAs are on, and v3 has no tag for that combination.
  See `unresolved` item 7.
