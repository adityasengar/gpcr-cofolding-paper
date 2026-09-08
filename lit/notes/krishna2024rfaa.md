# krishna2024rfaa

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say and
`NOT APPLICABLE` (with a reason) where the field asks something this paper never sets out to do.

**Page numbers below are PDF page numbers from `./pagetext.sh` markers (1–40)**, which for this
preprint are also the only page numbers the document carries. Layout: p1–p2 title/abstract,
p2–p4 architecture and training, p5–p7 protein–small molecule prediction, p7 covalent
modifications, p7–p9 RFdiffusionAA design, p9–p11 experimental characterisation, p11 Discussion,
p12 acknowledgements/contributions, p13 "Figures" divider, p14–p22 Figures 1–5 (image page then
caption page), p23–p35 Supplementary Figures S1–S11 (image and caption on the same page),
p36–p40 references 1–59.

**FRAMING. This is a MODEL paper**, not a conformational-states study and not a benchmark-only
paper. It introduces one architecture (RFAA) plus one fine-tuned generative derivative
(RFdiffusionAA) and reports accuracy across biomolecular categories. Section C fields that
presuppose a states study are answered as `NOT APPLICABLE` with a reason rather than forced;
the one genuine conformational-state result in the paper is the apo-vs-holo panel Fig S3E–G
(p25–p26) and it is recorded where it belongs rather than inflated.

**The three things this note exists for in the corpus:**

1. **The training cutoff is NEVER STATED AS A DATE.** The paper refers to "the cutoff date for
   our training set" (p6) without giving it. The *only* date anywhere in the paper that anchors
   a train/test boundary is a parenthetical describing the covalent-modification test set:
   **"931 recent entries in the PDB (post-May, 2020)" (p7).** Full treatment in
   `anti_memorization_design`. **Any corpus paper reporting a specific RFAA training-cutoff date
   is taking it from the released code, the Science version, or the Supplemental Methods — not
   from this preprint.**
2. **The architecture** is recorded in detail in `structural_priors_used` and in the
   `## Architecture` block below. **AlphaFold3 is never mentioned in this paper** (it postdates
   this October 2023 preprint); comparisons are to AF2, RF2, RFNA, DiffDock, Uni-Mol, DeepDock,
   TankBind, EquiBind, AutoDock Vina and Gold. Everything recorded about architecture is what
   *this* paper states about *itself*; no AF3 fact is imported.
3. **Confidence metrics**: `confidence_as_discriminator`.

**THE SUPPLEMENTARY METHODS ARE NOT HELD.** Supplementary Figure *captions* S1–S11 are held
(p23–p35), but the Supplemental Methods text, Table S4 (validation sets), Table S6 (46 element
tokens), and the separately numbered "Supplementary Information Figures 9-11" cited at p10 for
heme thermostability are all cited and none is present. See `si_in_scope` and `unresolved`.

**LICENSE WARNING, up front: CC-BY-ND 4.0** — printed on the header of every one of the 40
pages. The **ND (no-derivatives) clause forbids redrawing as well as modifying** any figure from
this preprint. See `reuse`.

---

## A. Identity

- **citekey**: `krishna2024rfaa`
- **doi**: **Preprint held: bioRxiv 10.1101/2023.10.09.561603** (page header, all 40 pages,
  e.g. p1: "bioRxiv preprint doi: https://doi.org/10.1101/2023.10.09.561603; this version posted
  October 9, 2023"). **Journal version (not held): Science, DOI 10.1126/science.adl2528**, per
  `refs.bib` and `MANIFEST.csv`. See `unresolved` for the venue split.
- **year**: **Preprint posted 9 October 2023** (p1 header). `refs.bib` records the journal year
  as **2024**. The citekey year (2024) is therefore the Science year, not the year of the PDF in
  hand.
- **venue**: **DUAL, and the corpus must not collapse it.** The PDF held is the **bioRxiv
  preprint, not peer reviewed** — stated explicitly on every page: "this version posted October
  9, 2023. The copyright holder for this preprint (which was not certified by peer review) is
  the author/funder" (p1). The version of record is **Science (2024), DOI
  10.1126/science.adl2528**, which is *not* in this PDF. Tagged `preprint`, **not**
  `peer-reviewed`. Every page number and every quote in this note is from the preprint.
- **title**: "Generalized Biomolecular Modeling and Design with RoseTTAFold All-Atom" (p1).
  (`refs.bib` uses sentence case; the PDF title-cases it.)
- **authors**: Rohith Krishna, Jue Wang, Woody Ahern (‡ equal contribution), Pascal Sturmfels,
  Preetham Venkatesh, Indrek Kalvet, Gyu Rie Lee (° equal contribution), Felix S. Morey-Burrows,
  Ivan Anishchenko, Ian R. Humphreys, Ryan McHugh, Dionne Vafeados, Xinting Li, George A.
  Sutherland, Andrew Hitchcock, C. Neil Hunter, Minkyung Baek, Frank DiMaio, David Baker*
  (p1). 19 authors. Institute for Protein Design / University of Washington, HHMI, with
  University of Sheffield (photosynthesis/bilin work) and Seoul National University (p1).
- **funding / competing interests** (p12, recorded because it bears on how the numbers read):
  "We thank Microsoft for generous donation of Azure Compute Credits"; "This work was supported
  by gifts from Microsoft (R.K., P.S., D.B.), the Howard Hughes Medical Institute (D.B),, the
  New Faculty Startup Fund from Seoul National University (M.B.), the Schmidt Futures program".
  **No competing-interests statement, no data-availability statement and no code-availability
  statement appears anywhere in this PDF.** See `unresolved`.

---

## Architecture (not a schema field; recorded because the corpus asked for it explicitly)

Everything here is a statement the paper makes about RFAA. **AF3 is not named in this paper**;
the "shares / differs" split below is expressed against the AF2/RF2 lineage the paper itself
compares to, and the reader must make the AF3 comparison from elsewhere.

**Lineage and trunk.** "We modeled the network architecture after the RoseTTAFold2 (RF2) protein
structure prediction network, which accepts 1D sequence information, 2D pairwise distance
information from homologous templates, and 3D coordinate information and iteratively improves
predicted structures through many hidden layers(11)." (p3). So: a **three-track (1D/2D/3D)
architecture with recycling**, not a two-track Evoformer-plus-diffusion stack.

**How non-protein components enter.** "We retain the representations of protein and nucleic acid
chains from RF2 and represent arbitrary small molecules as atom-bond graphs. To the 1D track, we
input the chemical element type of each non-polymer atom; to the 2D track, the chemical bonds
between atoms; and to the 3D track, information on chirality [whether chiral centers are (r) or
(s)]." (p3). Element vocabulary: "we supplement the 20 residue and eight nucleic acid base
representation in RFNA with 46 new element type tokens representing the most common element
types found in the Protein Data Bank (PDB) (Table S6)" (p3). Bond orders are explicit: "we
encode pairwise information about whether bonds between pairs of atoms are single, double,
triple, or aromatic bonds. These features are linearly embedded and summed with the initial pair
features at the beginning of every recycle of the network" (p3).

**Chirality is handled by an explicit geometric gradient feature, not learned implicitly.**
"Since the 1D and 2D representations in the network are invariant to reflections, we encode
stereochemistry information in the third track by specifying the sign of angles between the
atoms surrounding each chiral center (Fig S1); at each block in the 3D track the gradient of the
deviation of the actual angles from the ideal values (with respect to the current coordinates)
is computed and provided as an input feature to the subsequent block" (p3). Fig S1 (p23) names
the module: "pass the gradients of the error in predicted angles with respect to the predicted
coordinates into the subsequent blocks as vector input features in the **SE(3)-Transformer**
which breaks the symmetry over reflections present in the rest of the network".

**Coordinate updates.** "in AF2 and RF, protein residues are represented by the coordinates of
the Cα and the orientation of the N-Cα-C rigid frame (or the P coordinate and the OP1-P-OP2
frame orientation in RFNA) and along the 3D track the network generates rotational updates to
each frame orientation and translational updates to each coordinate. To generalize this in RFAA,
heavy atom coordinates are added to the 3D track and move independently based only on a
predicted translational update to their position. Thus, immediately after input, the full system
is represented as a disconnected gas of amino acid residues, nucleic acid bases, and freely
moving atoms, which is successively transformed through the many blocks of the network into
physically plausible assembly structures." (p3). **Frame-based, iteratively refined regression —
there is no denoising-diffusion module in the structure predictor.** (Diffusion appears only in
the *design* derivative, RFdiffusionAA, p8.)

**Loss.** "we develop an all-atom version of the Frame Aligned Point Error (FAPE) loss introduced
in AF2 by defining coordinate frames for each atom in an arbitrary molecule based on the
identities of its bonded neighbors and, as with residue based FAPE, successively aligning each
coordinate frame and computing the coordinate error on the surrounding atoms (Figure 2A; for
greater sensitivity to small molecule geometry, we upweight contributions involving atoms; see
Supplemental Methods)" (p3). Formula rendered in Fig 2A (p15).

**Atom-token permutation invariance.** "Unlike proteins and nucleic acid sequences, molecular
graphs are permutation invariant, and hence, the network should make the same prediction
irrespective of small molecule element token order. In AF2 and RF2, the sequence order of amino
acids and bases is represented by a relative position encoding; for atoms, we omit such an
encoding and leverage the permutation invariance of the network's attention mechanisms." (p3).

**Required input.** The model needs the ligand's **bonded geometry supplied by the user**:
"given the sequences of the polymers and the atomic bonded geometry of the small molecules and
covalent modifications" (p1, abstract); Fig 1A (p14) lists "small molecule bonded structure, and
covalent bonds between small molecules and proteins".

**Confidence heads.** "In addition to atomic coordinates, the network predicts atom and
residue-wise confidence (pLDDT) and pairwise confidence (PAE) metrics to enable users to identify
high-quality predictions." (p3–p4).

**MSAs and templates are used** — Fig 3A caption: "the rest of the protein is modeled as
residues (with MSA and template inputs)" (p18); templates named at p3 as "2D pairwise distance
information from homologous templates".

**Summary for the corpus, three lines:** (i) RFAA is a **three-track RF2 descendant** — 1D/2D/3D
tracks, MSA + homologous templates, recycling, SE(3)-Transformer 3D track — whereas the
AF3-family models are pair-representation trunks feeding a generative diffusion head; (ii) RFAA
is a **deterministic single-pass regressor trained on an all-atom FAPE loss**, with **no
diffusion module in the predictor** (diffusion appears only in the separate design arm) and with
ligand chemistry supplied as **explicit bond-order and chirality-gradient features** rather than
generic atom tokens; (iii) it therefore shares with the AF3 family only the **all-atom joint
prediction goal, the pLDDT/PAE confidence heads, and the AF2-derived FAPE loss and recycling
idea** — the sampling mechanism, the loss, and the ligand featurisation all differ.

---

## B. Scope

- **system**: **General biomolecular assemblies.** "a deep network capable of modeling full
  biological assemblies containing proteins, nucleic acids, small molecules, metals, and covalent
  modifications" (p1). Categories actually benchmarked: protein–small molecule complexes (p5–p6),
  covalent modifications including glycans, enzyme cofactors and covalent drugs (p7), protein
  monomers (Fig S11A, p35), protein–nucleic acid complexes (Fig S11B, p35), multi-component
  assemblies (Fig 2D, p16). **No GPCR, kinase or transporter framing anywhere; no conformational
  state family is studied.**
- **n_targets**: Large and multi-arm. Per benchmark: **261** protein–small molecule interfaces
  (CAMEO 05/20/23–7/29/23, Fig 2B caption p16); **149** interfaces (CAMEO 8/12/23–09/02/23, Fig
  2C caption p16); **5,421** recent-PDB complexes in **1,681** protein sequence clusters and
  **3,261** ligand clusters (p6); **931** covalent-modification entries (p7) — printed as
  **938** in the Fig 3B caption (p18), see `unresolved`; **940** cases scored by Rosetta ΔG
  (Fig 2G caption, p16); **126** CASP14 structures (Fig S11A caption, p35); **89** protein–nucleic
  acid structures (Fig S11B caption, p35); PoseBusters set size **NOT REPORTED** in this PDF
  (deferred to ref 30). Design arm: **4** in-silico ligands (FAD, SAM, IAI, OQO), **3**
  experimental targets (digoxigenin, heme, bilin/PEB).
  **The generality claim is not made from a single system**, so the usual single-system flag does
  not apply here.
- **method_class**: **co-folding** (joint all-atom prediction of protein + nucleic acid + small
  molecule + metal + covalent modification from sequence and bonded graph) **+ generative design**
  (RFdiffusionAA, a DDPM fine-tuned from the RFAA weights, p8). Not MSA-subsampling, not
  state-filtering, not template-biasing, not MD, not benchmark-only.
- **backbones**: **RFAA itself is the new backbone.** Compared head to head against, in this
  paper: **AF2** (Fig S11A, p35; p11 "median GDT of 85 vs. 86"), **RoseTTAFold2 / RF2** (Fig S3A,
  p25–p26; Fig S11A, p35), **RoseTTAFoldNA / RFNA** (Fig S11B, p35), **DiffDock**, **Uni-Mol**,
  **DeepDock**, **TankBind**, **EquiBind** (Fig 2E, p15–p16; Fig S4A, p27), **AutoDock Vina** and
  **Gold** (p5, p6; Fig S4A, p27), and **RFdiffusion** for the design arm (Fig 4C, p19–p20).
  **AF3, Boltz, Chai, OF3 and Protenix are not mentioned** — none existed publicly at the time of
  this preprint. More than two backbones compared head to head, so tagged `multi-backbone`.
- **templates**: **on.** "2D pairwise distance information from homologous templates" (p3); Fig
  3A caption "the rest of the protein is modeled as residues (with MSA and template inputs)"
  (p18). **NOT state-annotated** — no state-annotated template source anywhere. **Whether
  templates were date-filtered for the post-cutoff benchmarks is NOT REPORTED** in this PDF; the
  template search protocol lives in the Supplemental Methods, which are not held. This is a real
  gap and is carried into `oracle_leakage` route 1.
- **msa_handling**: **full / default.** MSAs are used (Fig 3A caption, p18) but the generation
  protocol, depth and any filtering are described only in "Supplemental Methods" (p4, not held).
  **No subsampling, no clustering, no state-filtering and no pinning is described or attempted
  anywhere in the paper.** For the design arm, self-consistency is checked with "AF2 predictions
  made from a single sequence" (p9) — single-sequence, no MSA, on the *evaluation* side only.

---

## C. Conformational core

- **states_generated**: **one.** RFAA is a deterministic single-structure predictor: one
  all-atom model per input specification, refined by recycling; no ensemble, no sampling over
  states, no seeds discussed anywhere in the paper. The only place two structures of one protein
  appear is Fig S3E–G (p25–p26), where **two different input specifications** (with and without
  the ligand) yield two single-state predictions: "Binding site RMSD of apo and holo predictions
  of protein chains relative to the holo state crystal structure of the protein" (Fig S3E
  caption, p26). That is a two-input arm, not a two-state generator, and the paper never claims
  otherwise.
- **structural_priors_used**: **Extensive, and this is not a defect — it is the training and
  design substrate.**
  - *Training composition (p4, verbatim):* "From the PDB, we curated a protein-biomolecule
    dataset including protein-small molecule, protein-metal, and covalently modified protein
    complexes, filtering out common solvents and crystallization additives. Following clustering
    (30% sequence identity) to avoid bias towards overrepresented structures, we obtained
    **121,800 protein-small molecule structures in 5,662 clusters, 112,546 protein-metal
    complexes in 5,662 clusters, and 12,689 structures with covalently modified amino acids in
    1,099 clusters** for training."
  - *Non-PDB structural prior:* "we supplemented the training set with small molecule crystal
    structures from the **Cambridge Structural Database**(12). Each training example is sampled
    uniformly from the set of organic non-polymeric molecules, and the network predicts the
    coordinates for the asymmetric unit given atomic graph information." (p4).
  - *Data augmentation by atomization:* "we augment the training data by inputting portions of
    proteins as atoms rather than residues (a process we term atomization). We atomize randomly
    selected subsets of three to five contiguous residues" (p4).
  - *Polymer training carried over from prior work:* "we train the network on protein monomer,
    protein complex, and protein-nucleic acid complex examples as previously described(10, 11)"
    (p4).
  - *Cropping:* "All examples were cropped to have 256 tokens during the initial stages of
    training and 375 tokens during fine-tuning." (p4).
  - *Cluster-count context (p11):* "whereas there are over 21,000 distinct protein-only structure
    clusters in the PDB, there are only **6,016 distinct sequence clusters with protein-small
    molecule complexes**."
  - *Inference-time priors:* MSAs and homologous templates for the protein chains (p3, p18); the
    user-supplied small-molecule bonded graph and chirality (p1, p3).
  - *Design-time priors (RFdiffusionAA arm, and the reason this field exists):* the ligand's
    3D conformation is always given — "In design settings, we typically know the conformation of
    the small molecules we want to bind, so **the ligand conformation is always included in the
    motif**" (p8); a known coordination geometry is given for heme — "We diffused proteins around
    heme with the central iron coordinated by a cysteine and placeholder molecule just above the
    porphyrin ring to keep the axial heme binding site open" (p9); a known natural sequence motif
    is given for bilin — "We utilized the **CARD motif** recognised by the CpcEF bilin lyase for
    covalent attachment of bilins to the native cyanobacterial CpcA phycobiliprotein" (p10). The
    three design cases are explicitly described as "one with no protein motif, one with a single
    residue protein motif, and one with a four residue protein motif" (p9). **All of these are
    legitimate design-time structural priors, not pipeline leakage.**
- **oracle_leakage**: **Seven routes, considered separately.**

  **Route 1 — deposited structures used as input or template.**
  *For RFAA itself: NONE FOUND for the target structure, PARTIAL AND UNSTATED for homologous
  templates.* The predictor is given only sequence plus ligand graph: "RFAA only receives the
  protein sequence and basic atomic graph information for the small molecule" (Fig S4A caption,
  p27); "For RFAA this means only having sequence and minimal atomic graph inputs" (Fig 2E
  caption, p16); design-motivating sentence at p2: "starting only from knowledge of the
  constituent molecules (and not their 3D structures)". **But** homologous templates *are* an
  input (p3: "2D pairwise distance information from homologous templates"), and **the paper never
  states whether templates were date-filtered or homology-filtered for the post-cutoff test
  sets**; the protocol is deferred to Supplemental Methods (p4), not held. On a strict reading
  this is an **unquantified route-1 exposure**, not a clean NONE FOUND. The protocol pages to
  check are p3–p4.
  *For the comparator methods: EXPLICIT AND DISCLOSED, in RFAA's favour.* "the other methods were
  not enrolled in CAMEO, so we could not carry out a blind test" and "RFAA predicts the protein
  backbone and side chains in addition to the small molecule dock, whereas **DiffDock receives
  the crystal structure of the protein from the bound complex as input**" (p6); "Vina and Gold
  receive the bound crystal structure and a bounding box for the pocket" (Fig S4A caption, p27).
  The authors label this correctly: "when they are provided with more privileged information"
  (p6), and "An often used but not very stringent test of protein-ligand docking methods is the
  ability of a method to dock a small molecule with a protein target given the crystal structure
  of the backbone and side chains of the protein in complex with the small molecule (in
  real-world problems, such a 'bound' crystal structure is never available)" (p5–p6).

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving
  templates or alignments.** **NONE FOUND.** No state-annotated database appears anywhere in the
  paper. Every database named is unannotated by conformational state: the PDB (p4), the Cambridge
  Structural Database (p4), the AlphaFold Protein Structure Database (ref 29 only), EMDB (Fig 3G
  caption, p18). Protocol described p3–p4; benchmark protocols p5–p7.

  **Route 3 — cluster labels derived from known states.** **NONE FOUND.** All clustering in the
  paper is by sequence identity or chemical similarity, never by conformational state:
  "clustering (30% sequence identity)" (p4); "1,681 protein sequence clusters at 30% sequence
  identity" and "3,261 ligand clusters" (p6); "agglomerative clustering at TM-score thresholds
  from 0 to 1" for design diversity (Fig S6 caption, p29). Protocol pages p4, p6, p29.

  **Route 4 — hyperparameters, sweeps, seeds or stopping criteria tuned against known states.**
  **PARTIAL, and the confidence thresholds are the exposure.** Training is monitored on a
  declared held-apart split: "The progress of training was monitored using independent validation
  sets consisting of 10% of the protein sequence clusters (see Supplementary Information Table
  4)" (p4) — Table S4 not held, so the split cannot be checked. **No sweep of any inference
  hyperparameter over the evaluation set is described**, and no seed or recycle count is tuned
  per target. **However**, the confidence cutoffs that carry the headline claims are asserted
  without justification and never stated to have been fixed in advance: "PAE Interaction < 10"
  (p5, p7), "PAE Interaction <10 and pLDDT>0.8 respectively" (p6), "filtered by PAE < 10 and
  PLDDT > 0.8" (Fig S3A caption, p26). Choosing those thresholds against the same recent-PDB sets
  on which the accuracy is then reported is a route-4 exposure of the "tuned range" kind the
  schema flags. **NOT REPORTED whether the thresholds were pre-registered.**

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.** **PRESENT BY
  CONSTRUCTION, disclosed.** Every success rate in the paper is an RMSD-to-deposited-structure
  predicate: "< 2Å ligand RMSD" (p5), "Modification RMSD<2.5Å ... where Modification RMSD is
  defined as RMSD of the modified residue and chemical modification when the rest of the protein
  is aligned" (p7), "Ligand RMSD was computed by CAMEO organizers" (Fig 2B/2C captions, p16),
  "Ligand RMSD was computed using PoseBusters suite" (Fig 2E caption, p16). This is standard
  retrospective benchmarking and the reference is a held crystal structure in every arm except
  the wet-lab design arm. The mitigating fact is that in the CAMEO arm the reference did not
  exist when the prediction was made (p5).

  **Route 6 — best/worst model labels assigned against a held reference.** **PRESENT AND
  EXPLICIT. This is the single most quotable leakage in the paper.** Fig 2F caption, p16,
  verbatim: **"Each set is clustered based on sequence/ligand similarity, and the lowest Ligand
  RMSD cluster representative is chosen for each (to answer the question of what is the best the
  network can do on these inputs)."** The 41%-vs-23% and 20%-vs-16% generalisation numbers on p6
  are therefore **best-of-cluster figures selected against the held reference**, not per-target
  success rates. A second, smaller instance in the design arm: "Top: GALigandDock evaluated
  binding ΔG (**minimum of eight LigandMPNN sequences**) ... Bottom: proportion of designs with
  RMSD to AF2 prediction less than the value specified by the x-axis (**minimum of eight
  LigandMPNN sequences**)" (Fig 4C caption, p20) — best-of-eight against an in-silico oracle
  rather than a crystal structure.

  **Route 7 — design-level oracle: inputs or systems chosen because the expected answer is
  already known. PRESENT, WEAK, and correctly disclosed by the authors — label it design-level,
  NOT pipeline leakage.** The clearest case is the conformational-shift illustration: Fig S3F
  caption, p26, verbatim: "Prediction of the FK1 domain of FKBP51 with (teal) and without (pink)
  the binding partner 35-(E) (PDB entry 7b9z). The model demonstrates an understanding of the
  conformational shift upon binding in the β3a loop, **represented in the PDB and our training
  set (e.g., see PDB entries 3o5e, 6saf)**." The authors themselves say the shift the model
  reproduces was in training, and the example was selected after the fact ("The pink points are
  depicted in panels F and G", Fig S3E caption, p26 — the illustrated cases are picked off the
  scatter). Two further, milder instances: the three multi-component successes in Fig 2D and the
  three low-similarity successes in Fig 2H are selected exemplars of successful predictions
  ("Three examples of successful predictions", Fig 2D and 2H captions, p16); and the three
  experimental design targets were chosen because their binding chemistry is known in advance
  (digoxigenin has prior designed binders, ref 49, p9; heme's "catalytic function enabled by
  pentacoordinate iron binding", p9; bilin's CARD lyase motif, p10). None of these feeds anything
  to the network — the network's inputs stay clean — so this is route 7, not route 1.

- **prospective**: **PARTIAL, and the split is arm-by-arm.**
  - **Genuinely prospective (2 arms).** (a) The **CAMEO ligand-docking arm**: "To enable blind
    testing of RFAA prediction performance, we enrolled an RFAA server in the blind CAMEO ligand
    docking evaluation, which carries out predictions using a series of servers on all structures
    submitted to the PDB each week and evaluates their performance(21–23)" (p5); scoring is
    third-party — "Ligand RMSD was computed by CAMEO organizers" and "AutoDock Vina server set up
    by CAMEO organizers" (Fig 2C caption, p16). Predictions precede deposition; there is no target
    selection by the authors. (b) The **wet-lab design arm**: designs were made, then expressed
    and assayed (p9–p10); no oracle existed at design time.
  - **Retrospective (all remaining arms).** The recent-PDB set (p6), the covalent-modification set
    (p7), the PoseBusters comparison (p6, Fig S4A p27), CASP14 (Fig S11A, p35), the protein–NA set
    (Fig S11B, p35) and the apo/holo panel (Fig S3E–G, p26) are all scored against structures the
    authors held at analysis time. These are post-cutoff (so not memorised) but not blind (so
    thresholds, exemplars and best-of-cluster representatives were chosen with the answers
    visible — see routes 4, 6, 7).
- **state_metric**: **DUAL — RMSD-to-reference + visual only.**
  - *RMSD-to-reference*, with stated thresholds: **< 2 Å ligand RMSD** for protein–small molecule
    success (p5, p6; "All boxplots cut off at 20Å for clarity", Fig 2 caption p16); **< 2.5 Å
    modification RMSD** for covalent modifications (p7; "Boxplot cut off at 15Å for clarity", Fig
    3B caption p18); **< 2 Å AF2 backbone RMSD** for design self-consistency (p9). **The
    justification for 2 Å and 2.5 Å is NOT REPORTED** — both are asserted as conventional. Also
    used: GDT (Fig S11A, p35), all-atom lDDT (p11, Fig S11B p35), "LDDT Interaction ... computed
    by measuring the all-atom LDDT between protein residues and the residue and modification
    atoms" (Fig S5C caption, p28), TM-score for design novelty and diversity (p11, Figs S6, S7,
    S10).
  - *Visual only*: every conformational claim in the paper is called by eye from a render with no
    operationalised predicate — "Some examples of shifts predicted by RFAA but not by RF2 include
    domain movements, subtle backbone movements, and flipping of side chain rotamers to
    accommodate the ligand in the pocket (Figure S3B-C)" (p6); "The model demonstrates an
    understanding of the conformational shift upon binding in the β3a loop" (Fig S3F caption,
    p26); "The model shifts residues in a neighboring helix to better form a binding pocket for
    the ligand" (Fig S3G caption, p26); "the RFAA predicted glycan model fits well in the
    density" (p7). None of these has a number attached.
- **metric_saturation**: **NONE REPORTED (numeric).** No metric floors or ceilings in any arm:
  success rates run 8%–52% and never approach 0% or 100%; median GDT 85 vs 86 and median lDDT
  0.74 vs 0.78 are comfortably off both bounds (p11). One structural remark that is *not*
  saturation but bears on it: the primary metric is a **thresholded binary predicate** (<2 Å,
  <2.5 Å) computed on an unbounded continuous quantity, so all magnitude information above the
  threshold is discarded by the headline numbers, and the underlying RMSD distributions are only
  shown in truncated boxplots. **The 20 Å and 15 Å boxplot cut-offs are axis truncations and are
  recorded in the figure table's `hides` column (Fig 2B, 2F-G, Fig 3B-D), not here**, per v3 rule
  9.
- **directional_control**: **LARGELY NOT APPLICABLE — RFAA is not a state-directable method and
  never claims to be.** It emits one structure per input and offers no state handle: no seed
  sweep, no subsample depth, no state-annotated template, no state-filtered MSA. **The one handle
  that exists is the ligand itself**, used only in a single SI panel group: adding or removing the
  small molecule from the input changes the predicted protein conformation — "Binding site RMSD
  of apo and holo predictions of protein chains relative to the holo state crystal structure"
  (Fig S3E caption, p26), with the FKBP51 β3a loop and the tRNA-ligase helix as the two
  illustrations (Fig S3F–G, p26). Related but weaker: co-folding with the ligand improves the
  protein prediction itself — "In cases where RFAA predicts ligand placement with high confidence
  and RF2 has high confidence (PAE Interaction <10 and pLDDT>0.8 respectively), RFAA makes higher
  accuracy protein structure predictions than RF2 (Fig S3A), indicating that training with ligand
  context can improve overall protein prediction accuracy" (p6). **For the design arm the control
  is far stronger and is a different thing entirely**: RFdiffusionAA is explicitly conditional —
  "we train an explicitly conditional model that learns the distribution of proteins conditioned
  on biomolecular substructure. During training, substructures of the native complexes, 'motifs',
  are provided to the model as context" (p8) — and the handles are the **ligand conformation, a
  protein motif (0, 1 or 4 residues, p9), and optional auxiliary potentials** ("we investigated
  the use of auxiliary potentials to influence trajectories to make more contacts between small
  molecules and binders. Generally, we found the use of such potentials unnecessary, though they
  can yield tighter interfaces for larger small molecules, as we demonstrate for FAD", p8). That
  is control over *what is built*, not over *which conformational state of an existing protein is
  produced*.
- **anti_memorization_design**: **YES — several post-cutoff held-out sets exist. But the CUTOFF
  DATE IS NEVER STATED, and that is the finding.**

  **The cutoff, exactly, quoted with its page.** The paper refers to its own cutoff exactly once,
  and without a date — p6, verbatim: **"To evaluate the ability of the model to generalize to new
  cases, we assembled a dataset of recent PDB entries with small molecules bound that were
  deposited **after the cutoff date for our training set**, and predicted full structure models
  for all 5,421 complexes (1,681 protein sequence clusters at 30% sequence identity)."**
  **No date is given there or anywhere else in the main text, and no Methods section in this PDF
  supplies one.**

  **The only date anywhere in the paper that anchors a train/test boundary** is a parenthetical
  in the covalent-modification section — p7, verbatim: **"We benchmarked the performance of the
  network in covalent modification structure prediction on 931 recent entries in the PDB
  (post-May, 2020), and found that the network made accurate predictions (Modification RMSD<2.5Å)
  in 46% of cases".** That sentence dates the **test set**, not the training set; it says
  "post-May, 2020" without a day, and the paper never says that May 2020 *is* the training
  cutoff. **Treat "May 2020" as an inference from a test-set selection date, not as a stated
  training cutoff.** The corresponding figure caption (Fig 3B, p18) gives the set size as **938**
  and drops the date entirely: "a set of 938 recently solved structures with covalent
  modifications".

  **Verdict for the corpus: the training cutoff is `NOT REPORTED` as a date in this preprint.**
  Downstream corpus papers that define held-out sets against an RFAA cutoff, and especially any
  that report a specific day, are taking that value from the Science version, the released
  code/weights, or the unheld Supplemental Methods — **not from this document**. Recorded here
  explicitly so the absence is visible rather than inferred.

  **The held-out sets that do exist, with n:**
  | set | n | how the boundary was defined | page |
  |---|---|---|---|
  | Recent-PDB protein–small molecule | 5,421 complexes; 1,681 seq clusters at 30% ID; 3,261 ligand clusters | "deposited after the cutoff date for our training set" — **date not given** | p6 |
  | Covalent modifications | 931 (text) / 938 (Fig 3B caption) | "recent entries in the PDB (post-May, 2020)" | p7; p18 |
  | CAMEO blind ligand docking, set 1 | 261 protein–small molecule interfaces | weekly PDB depositions, 05/20/23–7/29/23; prediction precedes deposition | Fig 2B caption, p16 |
  | CAMEO blind ligand docking, set 2 | 149 protein–small molecule interfaces | weekly PDB depositions, 8/12/23–09/02/23 | Fig 2C caption, p16 |
  | PoseBusters comparison set (from ref 30) | **n NOT REPORTED in this PDF** | "the test structures are outside of the training sets of all the methods" (p6); "a single example present in our training set was removed for all methods in comparison" (Fig 2E caption, p16) | p6; p16 |
  | Protein–nucleic acid | 89 structures | "recently solved structures that were **not in the training set of either method**" | Fig S11B caption, p35 |
  | CASP14 monomers | 126 structures (TBM-hard, FM/TBM, FM) | CASP14 targets; **no cutoff statement given** | Fig S11A caption, p35 |
  | Held-out ligand-binding proteins (RFAA vs RF2) | n NOT REPORTED | "a held-out set of ligand-binding proteins in the PDB" | Fig S3A caption, p25–p26 |
  | Training-monitoring validation split | 10% of protein sequence clusters | "independent validation sets consisting of 10% of the protein sequence clusters (see Supplementary Information Table 4)" — Table S4 **not held** | p4 |

- **anti_memorization_control**: **CONTROL ARMS WERE ACTUALLY RUN AND ANALYSED — this is not a
  `NONE RUN` paper, and the arms are well powered.** Four distinct memorisation controls:
  1. **Sequence-novelty split on the recent-PDB set** (p6, Fig 2F p15–p16): "The network performs
     better for clusters with overlap with the training set, but does generalize to novel clusters
     (**41% vs. 23% success rate**)". n = 1,681 sequence clusters. **Well powered.** Caveat: these
     are best-of-cluster figures (route 6 above).
  2. **Ligand-novelty split** (p6, Fig 2F): "while the network makes more accurate predictions for
     ligands seen in training, it also can make accurate predictions on ligands that are not
     similar to those in training (<0.5 Tanimoto similarity; **20% vs. 16% success rate**)". n =
     3,261 ligand clusters. **Well powered.**
  3. **Sequence-identity stratification for covalent modifications** (p7, Fig 3C p17–p18): "While
     the network makes slightly more accurate predictions on cases with sequence similarity (>25%
     identity) to proteins in the training set, there are still many cases (**27.5%**) that do not
     have sequence overlap to the training set that are predicted with high accuracy". Homolog
     presence is near-null for glycans specifically — "Having a homolog in the training set (>30%
     sequence similarity) does not seem to be a large indicator of successful predictions" (Fig
     S5C caption, p28).
  4. **Physics-correlate control** (p6, Fig 2G p15–p16), used as an orthogonal argument that the
     network learned chemistry rather than lookup: "predictions for protein-small molecule
     complexes with high predicted affinity (by Rosetta ΔG) were more accurate than predictions
     for complexes predicted to bind weakly (Figure 2G; **50%, 25%, and 22% success rates for
     <-30, -30-0, and >0 Rosetta Energy Units respectively**)"; n = 940.

  The design arm runs its own memorisation controls (Figs S6, S7, S10; see `controls_run`),
  including the honest negative result at Fig S6 (p29): "for ligands that appear frequently in the
  training set [FAD, SAM], the binders generated are **less diverse** than those designed against
  ligands with low similarity to any ligand in the training set [IAI, OQO] as the network has come
  to recognize some of the canonical binding modes of common ligands."

  **Not UNPOWERED.** The caveats are (i) the cutoff date is unstated, so the reader cannot verify
  the boundary; (ii) template date-filtering is unstated; (iii) the generalisation numbers are
  best-of-cluster.
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Blind CAMEO enrolment, weekly, scored by CAMEO organizers | Retrospective target selection and self-scoring; oracle existing at prediction time | p5; Fig 2B–C captions p16 |
  | CAMEO baseline "Vina" server (homology model + AutoDock + Vina scoring), same targets | That any automated classical pipeline would score the same on the same blind targets (32% vs 8%) | p5; Fig 2C p15–p16; Fig S2A p24 |
  | CAMEO baseline "AD4" server, same targets | Same, against a second classical baseline | Fig S2B caption, p24 |
  | Novel-vs-overlapping **sequence** cluster split (41% vs 23%) | Memorisation of protein families | p6; Fig 2F p15–p16 |
  | Novel-vs-seen **ligand** cluster split, Tanimoto <0.5 (20% vs 16%) | Memorisation of ligand binding modes | p6; Fig 2F p15–p16 |
  | Sequence-identity-to-training stratification for covalent modifications, 5 bins | Homology-driven success on the modification benchmark | p7; Fig 3C p17–p18 |
  | Homolog-in-training split for glycans | Homology-driven success on glycans specifically | Fig S5C caption, p28 |
  | Rosetta ΔG stratification of native complexes (50 / 25 / 22%) | Pure lookup: accuracy tracks physical binding strength, which a lookup table would not | p6; Fig 2G p15–p16 |
  | RF2 head-to-head on the same held-out ligand-binding proteins, both confidence-filtered, paired t-test | That ligand context adds nothing to protein prediction (p<0.05; 6.7e-10 pocket, 2.9e-5 global) | p6; Fig S3A p25–p26 |
  | **Apo vs holo prediction** of the same protein chains, scored against the holo crystal | That the ligand input has no effect on the predicted protein conformation | Fig S3E–G, p25–p26 |
  | AF2 and RF2 head-to-head on 126 CASP14 monomers (GDT) | That all-atom generalisation cost protein-only accuracy (85 vs 86 median GDT) | p11; Fig S11A p35 |
  | RFNA head-to-head on 89 held-out protein–NA complexes (all-atom lDDT) | That all-atom generalisation cost nucleic-acid accuracy (0.74 vs 0.78) | p11; Fig S11B p35 |
  | PoseBusters physical-validity filter battery (~20 checks) run on RFAA's own <2 Å poses | Physically invalid poses passing as successes; localises the residual failure to "minimum distance to protein" (0.39 of poses) | Fig S4B–C, p27 |
  | RFAA vs DiffDock split by presence of cofactors | That RFAA's advantage is not specifically multi-molecule modelling | Fig S4D caption, p27 |
  | Removal of the one PoseBusters case present in RFAA training, for **all** methods | An unfair single-case advantage in the head-to-head | Fig 2E caption, p16 |
  | Protein-only RFdiffusion + attractive/repulsive potential, same four ligands | That implicit-ligand diffusion would do as well as explicit all-atom conditioning (p<1.56E-12 in each case) | p8–p9; Fig 4C p19–p20 |
  | RFdiffusion unconditional vs motif-conditional diversity reference curves | That RFdiffusionAA's diversity is anomalously low for a conditional generator | Fig S6, p29 |
  | Max/mean TM-score of 400 designs to the training set, and to training proteins binding the same ligand | That designs are memorised training scaffolds | Fig S7A–B, p30 |
  | Same, restricted to AF2-self-consistent designs (RMSD<2 Å) | That the apparent novelty comes from non-foldable backbones | Fig S7C caption, p30 |
  | Closest training-set protein binding a *similar* ligand (Tanimoto>0.5) for each experimental hit | That the experimentally successful binders recapitulate a known binding mode (TM ≤0.62 in all cases) | p11; Fig S10, p34 |
  | AF2 single-sequence prediction of each design | That the design sequence does not encode the designed structure | p9; Fig 4B–C p19–p20 |
  | **Wet lab:** C114A cysteine→alanine mutant of the heme binder, UV/Vis | That heme binding is not via the designed Cys coordination — "Mutating the putative heme-coordinating cysteine residue to alanine led to a notable change in the Soret features upon in vitro heme-loading" | p10; Fig 5B p21–p22 |
  | **Wet lab:** thermal series (22/73/90 °C heme; 25/75/95 °C CD melt) | That the observed binding/fold is a marginal, non-thermostable artefact | p9–p10; Fig 5A–B p21–p22 |
  | **Wet lab:** SEC on 45 purified heme designs | Aggregate-associated pigment rather than genuine monomeric binding (38/45 monomeric and heme-retaining) | p10 |
  | **Wet lab:** native CpcA-PEB positive control, spectra and quantum yield set to 100% | That the designed biliproteins' spectral shifts and yields have no reference scale | p10; Fig S8B–C p31 |
  | **Wet lab:** prior expert-designed maquette proteins with the CARD motif (FΦ 2–3%) as a literature comparator | That the design route offers nothing over expert scaffold design | p10 |

- **confidence_as_discriminator**: **YES, centrally — and validated for *accuracy*, never for
  conformational correctness.**
  - *What is predicted*: "the network predicts atom and residue-wise confidence (pLDDT) and
    pairwise confidence (PAE) metrics to enable users to identify high-quality predictions" (p3–p4).
    The derived quantity used throughout is **PAE Interaction**, "the network's predicted pairwise
    error between protein chains and small molecule chains (PAE Interaction)" (p5).
  - *What is claimed, verbatim*: "While not all predictions are accurate, we use the network's
    predicted pairwise error between protein chains and small molecule chains (PAE Interaction) to
    identify accurate predictions; across CAMEO targets, **43% of cases are predicted with high
    confidence (PAE Interaction < 10), and 77% of those high-confidence structures are predicted
    with < 2Å ligand RMSD** (Figure 2B)." (p5). And for covalent modifications: "confident
    predictions tend to be more accurate: **60% of structures are predicted with high confidence
    (PAE Interaction <10), and 63% of those predictions are accurate (<2.5Å modification RMSD)**"
    (p7). And for glycans: "The model's error prediction accurately identifies high-accuracy
    predictions" (Fig S5C caption, p28).
  - *How the claim is validated*: by showing the accuracy distribution stratified by confidence
    bin — Fig 2B "Model accuracy correlates with error predictions" (p16), Fig 3B "Model accuracy
    correlates with predicted error" (p18), Fig S5C third panel (p28). This is a genuine
    validation of PAE-Interaction as an *accuracy* discriminator, on n=261 / n=938 / glycan sets.
    **Only median/quartile separation is shown; no AUROC, no precision–recall, no calibration
    curve is reported.**
  - *Where it is used as a gate rather than a report*: pLDDT and PAE select the analysis subset in
    the RFAA-vs-RF2 comparison — "filtered by PAE < 10 and PLDDT > 0.8" (Fig S3A caption, p26) —
    and pLDDT selects designs for experimental testing — "Of 168 designs selected based on AF2
    predicted confidence (pLDDT), backbone RMSD to design, and RMSD of the predicted cysteine
    rotamer to the design" (p10). Note that the design-arm pLDDT is **AF2's**, not RFAA's.
  - **NOT validated as a discriminator of conformational correctness.** No panel, sentence or
    metric anywhere asks whether pLDDT or PAE distinguishes a correct conformational state from an
    incorrect one; the apo/holo panel (Fig S3E, p26) is not stratified by confidence. **The
    threshold value 10 is never justified** (see `oracle_leakage` route 4).

---

## D. Claims

- **central_conclusion**: A single three-track network descended from RoseTTAFold2, given
  polymer sequences plus atom-bond graphs for everything non-polymeric, can predict full
  biological assemblies — protein, nucleic acid, small molecule, metal and covalent modification —
  in one forward pass, at protein-only accuracy comparable to AF2 and with usable accuracy on
  ligand docking and covalent modifications; and the same weights, fine-tuned as a conditional
  denoising diffusion model, generate de novo small-molecule-binding proteins that bind their
  targets experimentally.

- **necessity_claims** (verbatim + page):
  - p2: "Modeling such general biomolecular assemblies composed of polypeptide chains, covalently
    modified amino acids, nucleic acid chains, and arbitrary small molecules **remains an
    outstanding challenge**".
  - p2: "This graph representation **is not suitable** for proteins, as they contain many
    thousands of atoms, and hence, modeling whole proteins at the atomic level **is
    computationally intractable**."
  - p2: "but general biomolecular system modeling is a more challenging problem given the great
    diversity of possible small molecule components."
  - p5: "While these methods have shown promising accuracy, they **generally require a priori
    knowledge of the bound conformation of the protein** and are **also unable to model additional
    atomic contexts** such as cofactors, metal ions, or covalent modifications."
  - p5–p6: "An often used but not very stringent test of protein-ligand docking methods is the
    ability of a method to dock a small molecule with a protein target given the crystal structure
    of the backbone and side chains of the protein in complex with the small molecule (**in
    real-world problems, such a 'bound' crystal structure is never available**)."
  - p7: "It is difficult to compare to other methods because, **to our knowledge, previous deep
    learning based tools do not model covalent modifications to proteins**."
  - p8: "However, current deep learning based generative approaches **do not explicitly model
    protein-ligand interactions, so they are not directly applicable** to the small molecular
    binder design problem."
  - p8: "In RFdiffusion, a heuristic attractive-repulsive potential encouraged the formation of
    pockets with shape complementarity to a target molecule, but the approach **was unable to
    model the details of protein-small molecule interactions**, and **none of the designs were
    experimentally validated**(42)."
  - p9: "However, this approach **is not generally applicable** since ideal scaffolds and specific
    binding interactions may not be available or known for arbitrary small molecules."
  - p11: "**The primary factor limiting accuracy is the relatively small size of the training
    set**; whereas there are over 21,000 distinct protein-only structure clusters in the PDB,
    there are only 6,016 distinct sequence clusters with protein-small molecule complexes."
  - p6: "**Training on more extensive datasets will likely be necessary** to generate consistently
    accurate predictions for new protein-small molecule complexes on par with the accuracy deep
    networks can achieve on protein systems alone."
  - p3: "**Since the 1D and 2D representations in the network are invariant to reflections**, we
    encode stereochemistry information in the third track" — an architectural necessity claim.

- **novelty_claims** (verbatim + page):
  - p1 (abstract): "RFAA has comparable protein structure prediction accuracy to AF2, excellent
    performance in CAMEO for flexible backbone small molecule docking, and reasonable prediction
    accuracy for protein covalent modifications and assemblies of proteins with multiple nucleic
    acid chains and small molecules **which, to our knowledge, no existing method can model
    simultaneously**."
  - p5: "**To our knowledge, no other current methods can model arbitrary higher-order
    biomolecular complexes**, which can include multiple proteins, small molecules, metal ions,
    and nucleic acids."
  - p5: "One strength of RFAA compared to previous methods is that the network is able to
    **jointly predict interactions between proteins and multiple non-protein ligands in a single
    forward pass**."
  - p5 (parenthetical, and a strong zero-shot claim): "(**the network received no examples of
    higher order assemblies containing proteins, small molecules, and nucleic acids during
    training**)."
  - p11: "**RoseTTAFold All-Atom (RFAA) demonstrates that a single neural network can be trained
    to accurately model a wide range of general biomolecular assemblies** containing a wide
    diversity of non-protein components."
  - p11: "**RFAA goes beyond any previous method we are aware of** in generating accurate models
    for complexes of proteins with two or more non-protein molecules (small molecules, metals,
    nucleic acids, etc.)."
  - p11: "**Unlike prior methods which rely on redesigning existing scaffolds, RFdiffusionAA
    builds proteins from scratch around the target compound**, resulting in highly
    shape-complementary binding pockets and reducing the need for expert knowledge."
  - p11: "**In all cases there is no detectable sequence similarity to any known protein.**"
  - p10: "much higher than obtained previously with expert designed scaffolds (maquette proteins)
    with the CARD motif (FΦ values of 2-3%)".
  - p1 (abstract): "we design and experimentally validate proteins that bind the cardiac disease
    therapeutic digoxigenin, the enzymatic cofactor heme, and optically active bilin molecules
    with potential for expanding the range of wavelengths captured by photosynthesis."

- **stated_limits** (the authors' own, verbatim where load-bearing):
  - p4: "We adopted the philosophy that a single model trained on all available data over all
    modalities would have the greatest ability to generalize and be more accessible than a series
    of models specialized for specific problems–**it is possible that better performance could be
    obtained by problem specific fine-tuning**."
  - p5: "**While not all predictions are accurate**, we use the network's predicted pairwise error
    ... to identify accurate predictions".
  - p5: "**The most common failure mode is the placement of small molecules in the correct pockets
    but not in the correct orientation** (Figure S3; for further exploration of failure modes, see
    Supplemental Methods)."
  - p5 (an unusually fair concession about their own baseline): "(**the Vina performance by an
    expert would likely be considerably improved** because of the complexities of fully automatic
    multiple step modeling pipelines)".
  - p6: "**In cases where both the bound protein structure and the pocket residues are provided,
    physics-based methods such as AutoDock Vina outperform RFAA (52% vs 42%)**, which has the much
    harder task of predicting both the protein backbone and sidechain details and the dock from
    sequence alone."
  - p6: "During training, RFAA should be learning general features of protein-small molecule
    interactions, **but it could also be memorizing likely binding modes of molecules to different
    sequence families**."
  - p6: "**Training on more extensive datasets will likely be necessary** to generate consistently
    accurate predictions for new protein-small molecule complexes on par with the accuracy deep
    networks can achieve on protein systems alone."
  - p11: "**While immediately useful** for protein-small molecule binder design and for modeling
    complex biomolecular assemblies for which there are few or no alternative methods available,
    **the accuracy of RFAA will need to be further increased to have a big impact on drug
    discovery.**"
  - p11: "**The primary factor limiting accuracy is the relatively small size of the training
    set**".
  - Fig S6 caption, p29 (a stated negative result about the design arm): "We observe that for
    ligands that appear frequently in the training set [FAD, SAM], **the binders generated are
    less diverse** than those designed against ligands with low similarity to any ligand in the
    training set [IAI, OQO] as **the network has come to recognize some of the canonical binding
    modes of common ligands**."
  - Fig S4B–C, p27: physical-validity violations concentrate in one check — "**Most structures are
    physically plausible, with most violations occurring in the 'minimum distance to protein'
    metric**"; "Most 'violating' distances are between 2.0 and 2.5 Å."
  - Fig S3F, p26 (the memorisation caveat the authors volunteer about their own conformational
    example): the β3a shift is "**represented in the PDB and our training set** (e.g., see PDB
    entries 3o5e, 6saf)".
  - **Not stated as a limit anywhere**: that RFAA predicts a single conformation; that it cannot
    be directed to a chosen state; that no ensemble is produced. Conformational heterogeneity is
    never raised as a limitation.

- **stance**: **`precedent` + `background`. PROVISIONAL — the user's call, not settled here.**
  - *precedent*: it is the reference all-atom co-folding model of the non-DeepMind lineage, and
    the source of the headline accuracy numbers (32% CAMEO <2 Å, 46% covalent <2.5 Å, GDT 85 vs
    86 against AF2) that any later co-folding comparison is measured against; it also establishes
    the post-cutoff-generalisation control design (novel sequence cluster vs overlapping, novel
    ligand cluster vs seen) that later papers reuse.
  - *background*: it is not a conformational-states paper and makes no claim in that arena, so for
    a manuscript about conformational state it supplies architecture, training composition and
    comparator numbers rather than a competing or contradicting result.
  - *Not `contrast`, and not `threat`.* Its rigour is unusually good for a model paper — a blind
    third-party-scored arm, four memorisation controls, an honest negative diversity result, and a
    concession that a classical method beats it under privileged input. The two rigour defects
    worth carrying (unstated cutoff date; best-of-cluster selection in Fig 2F) are recorded in
    `oracle_leakage` and `anti_memorization_design` but do not amount to a contrast stance.

---

## E. Quantitative comparators

### `metrics_reported` — PREDICTION ARM (RFAA)

| metric | value | units | measured against | page |
|---|---|---|---|---|
| CAMEO high-confidence fraction | 43 | % of targets with PAE Interaction < 10 | CAMEO blind, 05/20/23–7/29/23, n=261 protein–small molecule interfaces | p5; Fig 2B caption p16 |
| CAMEO accuracy among high-confidence | 77 | % with < 2 Å ligand RMSD | same 43% subset of n=261 | p5; Fig 2B p15–p16 |
| CAMEO head-to-head success, RFAA | 32 | % with < 2 Å ligand RMSD | CAMEO blind, 8/12/23–09/02/23, n=149 interfaces, RMSD computed by CAMEO organizers | p5; Fig 2C caption p16 |
| CAMEO head-to-head success, AutoDock Vina server | 8 | % with < 2 Å ligand RMSD | same n=149, CAMEO-run Vina server (homology model + AutoDock + Vina scoring) | p5; Fig 2C p15–p16 |
| PoseBusters-set success, RFAA (sequence + ligand graph only) | 42 | % with < 2 Å ligand RMSD | recent-PDB set curated in ref 30; **n NOT REPORTED in this PDF** | p6; Fig 2E p15–p16; Fig S4A p27 |
| PoseBusters-set success, DiffDock (given the bound crystal structure) | 38 | % with < 2 Å ligand RMSD | same set, privileged input | p6; Fig 2E p15–p16 |
| PoseBusters-set success, AutoDock Vina (bound structure + pocket bounding box) | 52 | % with < 2 Å ligand RMSD | same set, privileged input | p6; Fig S4A p27 |
| PoseBusters-set success, Gold / Uni-Mol / DeepDock / TankBind / EquiBind | rank order only; Gold ≈ Vina, then RFAA ≈ DiffDock, then Uni-Mol, DeepDock, TankBind, EquiBind (**exact values not printed**) | fraction < 2 Å RMSD | same set | Fig S4A p27; Fig 2E p15 |
| Recent-PDB generalisation, clusters overlapping training | 41 | % success (< 2 Å ligand RMSD), **lowest-RMSD cluster representative** | 5,421 complexes / 1,681 sequence clusters at 30% ID, deposited after the (unstated) cutoff | p6; Fig 2F p15–p16 |
| Recent-PDB generalisation, novel clusters | 23 | % success, best-of-cluster | same | p6; Fig 2F p15–p16 |
| Ligand generalisation, ligands seen in training | 20 | % success, best-of-cluster | 3,261 ligand clusters | p6; Fig 2F p15–p16 |
| Ligand generalisation, ligands with < 0.5 Tanimoto to training | 16 | % success, best-of-cluster | same | p6; Fig 2F p15–p16 |
| Rosetta ΔG stratification of native complex (< −30 / −30–0 / > 0 REU) | 50 / 25 / 22 | % success (< 2 Å) | n=940 recent-PDB cases successfully processed by Rosetta | p6; Fig 2G caption p16 |
| Covalent modification accuracy | 46 | % with modification RMSD < 2.5 Å | 931 PDB entries post-May 2020 (938 in Fig 3B caption) | p7; Fig 3B p17–p18 |
| Covalent modification high-confidence fraction | 60 | % with PAE Interaction < 10 | same set | p7 |
| Covalent accuracy among high-confidence | 63 | % with < 2.5 Å modification RMSD | the 60% subset | p7 |
| Covalent accuracy, no sequence overlap with training | 27.5 | % predicted with high accuracy | subset of the same set with no >25% identity match | p7; Fig 3C p17–p18 |
| Enzyme-cofactor modification, median RMSD | 0.99 | Å | same covalent test set, cofactor subset | p7; Fig 3D p17–p18 |
| Covalent drug modification, median RMSD | 2.8 | Å | same set, covalent-drug subset | p7; Fig 3D p17–p18 |
| Glycosylation, median RMSD | 3.2 | Å | same set, glycan subset; chains up to seven monosaccharides | p7; Fig 3D p17–p18; Fig S5 p28 |
| Protein monomer accuracy, RFAA vs AF2 | median GDT 85 vs 86 | GDT | 126 CASP14 structures (TBM-hard, FM/TBM, FM) | p11; Fig S11A p35 |
| Protein–nucleic acid complex accuracy, RFAA vs RFNA | median all-atom lDDT 0.74 vs 0.78 | all-atom lDDT | 89 recently solved structures not in either training set | p11; Fig S11B p35 |
| RFAA vs RF2 on ligand-binding proteins, ligand-pocket RMSD | RFAA lower; p = 6.7e-10 | Å (paired t-test on medians ≈ 1.0 vs 0.9) | held-out ligand-binding proteins, both filtered PAE<10 / pLDDT>0.8; **n NOT REPORTED** | p6; Fig S3A p25–p26 |
| RFAA vs RF2, global protein RMSD | RFAA lower; p = 2.9e-5 | Å (medians ≈ 1.7 vs 1.5) | same | Fig S3A p25–p26 |
| PoseBusters validity, worst check | 0.39 | fraction of < 2 Å docks failing "minimum distance to protein" | RFAA's own < 2 Å poses | Fig S4B p27 |
| PoseBusters validity, other checks | ≥ 0.92 (violations 0.01–0.08) | fraction of < 2 Å docks passing | same | Fig S4B p27 |

### `metrics_reported` — DESIGN ARM (RFdiffusionAA). **Kept separate; do not blend with prediction.**

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Designs with negative Rosetta interface ΔG, protein-only RFdiffusion + attractive/repulsive potential | 0 ("produces no interfaces with negative Rosetta ΔG") | % | 4 ligands: FAD, SAM, IAI, OQO | p8–p9; Fig 4C p19–p20 |
| Same, RFdiffusionAA | 52 | % | same 4 ligands | p9; Fig 4C p19–p20 |
| Same, RFdiffusionAA + auxiliary contact potential | 72 | % | same 4 ligands | p9; Fig 4C p19–p20 |
| Significance of ΔG improvement over RFdiffusion | p < 1.56E-12 (text); per-ligand p < 1.6e-12 / 4.2e-22 / 1.8e-29 / 1.3e-28 (figure) | p-value | FAD / SAM / IAI / OQO | p8–p9; Fig 4C p19 |
| AF2 self-consistency (single sequence), RFdiffusionAA | ≥ 45 (per-ligand 0.46, 0.45, 0.52, 0.52) | % of designs with AF2 backbone RMSD < 2 Å, min of 8 LigandMPNN sequences | 4 ligands | p9; Fig 4C p19–p20 |
| AF2 self-consistency, RFdiffusion + potential | 0.34, 0.34, 0.32(?), 0.20 (per-ligand, figure labels) | same | 4 ligands | Fig 4C p19 |
| Design ligand novelty | IAI 0.50; OQO 0.46 | Tanimoto similarity to nearest training ligand | training set | p9 |
| Designs whose most structurally similar training protein does not bind the same ligand | 99 | % of cases | 400 designs | p9; Fig S7 p30 |
| **Digoxigenin, wet lab**: designs screened → hits → affinity | 4,416 designs cloned and FACS-screened → 3 characterised hits → tightest **Kd = 10 nM** | count; nM | yeast display + FACS, then FP on purified protein | p9; Fig 5A p21–p22 |
| Digoxigenin binder thermostability | stable to 95 | °C | CD melt at 220 nm | p9; Fig 5A p21–p22 |
| **Heme, wet lab**: cascade | 168 designs → 135 well expressed → 96 with Cys-bound-heme UV/Vis → 45 purified → **38 monomeric and heme-retaining by SEC** | count | E. coli expression, UV/Vis Soret maximum, SEC | p10; Fig 5B p21–p22 |
| Heme binder thermostability | heme binding retained > 85; no unfolding to 95 | °C | UV/Vis at 22/73/90 °C | p10; Fig 5B p21–p22 |
| **Bilin (PEB), wet lab**: hit rate | 9 hits from 94 designs = **9.6%** | % | whole-cell pigmentation/fluorescence screen | p10; Fig S8 p31 |
| Bilin designs, absorption maxima | C11 557, H4 605, F9 607 vs CpcA-PEB control 573 | nm | purified protein absorption spectra | p10; Fig 5C p21–p22; Fig S8B p31 |
| Bilin designs, relative fluorescence quantum yield | C11 57.6, H4 17.1, F9 38.4 (text gives 17 / 38 / 57) vs CpcA-PEB = 100 | % relative to CpcA-PEB | spectroscopy | p10; Fig S8C p31 |
| Prior art comparator: expert-designed maquette + CARD motif | 2–3 | % FΦ | literature (ref 58) | p10 |
| Spectral range covered in one design round | 50 absorption / 46 emission | nm | three designs, one chromophore | p10 |
| **Design novelty vs PDB**, digoxigenin | TM 0.59 (0.71 to nearest training protein overall) | TM-score to closest PDB protein binding a related ligand (Tanimoto > 0.5) | training set | p11; Fig 5A p21–p22; Fig S10 p34 |
| Design novelty, heme | < 0.62 (HEM_3.B10: 0.54 overall / 0.51 similar-ligand) | TM-score | same | p11; Fig 5B p21–p22; Fig S10 p34 |
| Design novelty, bilin | < 0.52 (C11 0.58/0.46; H4 0.67/0.53; F9 0.67/0.51) | TM-score | same | p11; Fig 5C p21–p22; Fig S10 p34 |
| Design sequence novelty | "no detectable sequence similarity to any known protein" | — | all characterised designs | p11 |

- **n_predictions**: **Recorded separately per axis, since a single total is not what a power
  comparison needs.**
  - *Samples per target*: **NOT REPORTED** for RFAA. No number of seeds, recycles, or models per
    input is given anywhere in the main text; the CAMEO server presumably submits one model per
    target but this is never stated. For the design arm, per-backbone sampling **is** given:
    "**minimum of eight LigandMPNN sequences**" per backbone for both ΔG and AF2 self-consistency
    (Fig 4C caption, p20).
  - *Targets, prediction arm*: 261 (CAMEO set 1) + 149 (CAMEO set 2) + 5,421 (recent-PDB complexes,
    within 1,681 sequence clusters and 3,261 ligand clusters) + 931/938 (covalent modifications) +
    940 (Rosetta ΔG subset, a subset of the 5,421) + 126 (CASP14) + 89 (protein–NA) + PoseBusters
    set (**n NOT REPORTED**) + held-out ligand-binding proteins for the RF2 comparison (**n NOT
    REPORTED**).
  - *Total, prediction arm*: not additive as printed (the 940 is a subset of the 5,421; the two
    CAMEO windows may overlap in method but not in targets). **A defensible headline is ~7,900
    distinct predicted complexes across the named sets**, but the paper never states a total.
  - *Design arm*: 100 unfiltered designs per ligand for the diversity analysis (Fig S6, p29); 400
    designs for the novelty analysis (Fig S7, p30); 4,416 digoxigenin designs cloned and screened;
    168 heme designs selected (135 / 96 / 45 / 38 through the funnel); 94 bilin designs screened
    (9 hits, 3 purified). **The number of raw backbones generated before filtering is NOT
    REPORTED** for the three experimental campaigns.
  - *Training scale, for context*: 121,800 protein–small molecule structures (5,662 clusters);
    112,546 protein–metal complexes (5,662 clusters); 12,689 covalently modified structures (1,099
    clusters) (p4).
- **comparable_to_ours**: *(left empty by the extractor, per v3 §13)*
- **si_in_scope**: **PARTIAL — Supplementary figure captions held, Supplemental Methods and
  Tables NOT HELD.** Present in this 40-page PDF: main text, Figures 1–5 with full captions
  (p14–p22), **Supplementary Figures S1–S11 with full captions (p23–p35)**, references 1–59
  (p36–p40). **Absent and cited:**
  - "**Supplemental Methods**", cited five times and carrying material the corpus needs — the full
    RFAA architecture description (p4: "A full description of the RFAA architecture is provided in
    the Supplemental Methods"), the FAPE atom-upweighting scheme (p3), the atom-to-residue
    positional encoding (p4), the failure-mode analysis (p5), the design filtering and yeast
    screening protocols (p9). **The training-set cutoff date, the MSA/template generation
    protocol, and any template date-filtering would live here.**
  - **Table S6** (the 46 element-type tokens), cited p3.
  - **"Supplementary Information Table 4"** (the validation-set definition), cited p4.
  - **"Supplementary Information Figures 9-11"**, cited p10 for heme thermostability — these are
    numbered differently from this PDF's Figures S9–S11 (bilin coulombic charge, design novelty,
    AF2/RFNA comparison) and are therefore a **separate, unheld supplementary figure series**. See
    `unresolved`.
  - **PoseBusters benchmark set size**, deferred entirely to ref 30.
  - **No data-availability or code-availability statement** appears in this PDF, so the released
    weights (whose metadata would carry the cutoff) cannot be located from this document.
  **Consequence: `metrics_reported` is NOT emptied** — all headline numbers are in the main text
  and held figure captions — but the training cutoff, the template protocol and several n's are
  unrecoverable from what is held.

---

## F. Figures

One row per panel group. `fig_no` carries letter suffixes. All page numbers are PDF pages; for
main figures the **image page precedes the caption page** (Fig 2 image p15, caption p16, etc.),
and both are given. `reuse` is identical for every row and is stated once at the foot of the
table rather than repeated 24 times.

| fig_no | page | gist | plot_type | data_shape | panels | hides |
|---|---|---|---|---|---|---|
| 1A-B | p14 (image + caption) | Inputs RFAA accepts, and the three-track flow from molecular input featurisation to all-atom coordinates + confidence | schematic | `SCHEMATIC \| input composition of a biomolecular assembly, then 1D element-type / 2D bond-type / 3D chirality featurisation feeding a three-track network \| no data` | 2 (A inputs, B processing); vary by stage of the pipeline | |
| 2A | p15 / p16 | Definition of the per-atom coordinate frame and the all-atom FAPE loss, with the loss equation printed | schematic | `SCHEMATIC \| per-atom local coordinate frames in predicted vs true structure, and the all-atom FAPE formula \| no data` | 1 (three sub-renders + one equation) | |
| 2B | p15 / p16 | Ligand RMSD falls monotonically with better predicted error — the confidence-as-accuracy-discriminator panel | box | `PLOT \| facet: none (1) \| vary: PAE Interaction bin (5: 0-5, 5-10, 10-15, 15-20, 20+) \| series: none (1) \| measure: ligand RMSD (Å) \| mark: box \| n: NOT REPORTED per box, 261 protein–small molecule interfaces per panel` | 1 | **y-axis truncated at 20 Å** — stated in the caption ("All boxplots cut off at 20Å for clarity"), so the upper tail and the true worst-case magnitude are invisible; **per-box n not shown**, and the bins are plainly unequal in size |
| 2C | p15 / p16 | Head-to-head per-target ligand RMSD, RFAA vs the CAMEO Vina server, with an identity diagonal | scatter | `PLOT \| facet: none (1) \| vary: RFAA ligand RMSD, 0–20 Å (continuous) \| series: none (1) \| measure: AutoDock Vina ligand RMSD (Å) \| mark: point \| n: 1 per mark, 149 protein–small molecule interfaces per panel` | 1 | **Both axes clipped at 20 Å** with no break marker, so any target where either method failed badly is either dropped or piled on the frame; the 32%/8% summary is stated only in the text, not on the panel |
| 2D | p15 / p16 | Three multi-component assemblies (heme+lipid decarboxylase 8d8p; methyltransferase dimer + SAH + Tyr 7ux6; DNA polymerase + DNA + GTP analogue + Mg 7u7w) predicted under 2 Å | structure render | `RENDER \| facet: example complex (3: 8d8p, 7ux6, 7u7w) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 3, varying by system | **Selected successes** — "Three examples of successful predictions"; no distribution, no n, and no failure counterpart for the multi-component claim, which is the paper's strongest novelty claim (p5, p11) and has **no quantitative panel anywhere** |
| 2E | p15 / p16 | Fraction of PoseBusters-set complexes under 2 Å, RFAA vs five deep-learning docking methods, each in its own input regime | bar | `PLOT \| facet: none (1) \| vary: method (6: RFAA, DiffDock, UniMol, DeepDock, TankBind, EquiBind) \| series: none (1) \| measure: % under 2 Å ligand RMSD \| mark: bar \| n: NOT REPORTED per bar and per panel` | 1 | **Bar over a distribution** — six single bars stand in for six full RMSD distributions; **n is never given** for this set in the whole PDF; **the input regimes differ across bars** (RFAA gets sequence only, DiffDock gets the bound crystal structure) and that is disclosed only in the caption, not on the axis |
| 2F-G | p15 / p16 | RFAA ligand RMSD split by novelty relative to training (sequence homolog −/+, similar ligand −/+) and by native-complex Rosetta ΔG bin | box | `PLOT \| facet: stratifying variable (2: training-set novelty, native-complex Rosetta ΔG) \| vary: stratum (F: 4 = seq-homolog −/+, similar-ligand −/+; G: 3 = <−30, −30–0, >0 REU) \| series: none (1) \| measure: RFAA ligand RMSD (Å) \| mark: box \| n: NOT REPORTED per box; F over 1,681 sequence clusters and 3,261 ligand clusters, G over 940 cases` | 2 panels, 7 boxes, varying by stratification variable | **y-axis truncated at 20 Å**; **per-box n not shown** and the strata are certainly unequal; and critically, **each point is the lowest-RMSD cluster representative**, not a target — "the lowest Ligand RMSD cluster representative is chosen for each (to answer the question of what is the best the network can do on these inputs)" — so the panel shows a best-of-cluster upper bound, which the axis label does not say |
| 2H | p15 / p16 | Three successful predictions with low training-set similarity (7eme, 8ous, 7xqr), annotated with closest training sequence identity, closest training ligand Tanimoto, and achieved ligand RMSD | structure render | `RENDER \| facet: example complex (3: 7eme, 8ous, 7xqr) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 3, varying by system; each annotated with three numbers | **Selected successes**, chosen after scoring against the reference |
| 3A | p17 / p18 | How a covalent modification is tokenised: modified residue + moiety as atoms, remainder as residues with MSA and templates | schematic | `SCHEMATIC \| atom/residue tokenisation of a covalent modification, with the "residue-to-atom" bond feature labelled \| no data` | 1 | |
| 3B-D | p17 / p18 | Modification RMSD stratified three ways: by predicted error, by closest training sequence identity, and by modification type | box | `PLOT \| facet: stratifying variable (3: PAE Interaction, most-similar training sequence identity, modification type) \| vary: stratum (B: 4 = 0-5, 5-10, 10-15, 15+; C: 5 = 0-25, 25-50, 50-75, 75-99, 100 %; D: 3 = glycosylation, enzyme cofactor, other) \| series: none (1) \| measure: modification RMSD (Å) \| mark: box \| n: NOT REPORTED per box, 938 structures per panel` | 3 panels, 12 boxes, varying by stratification variable | **B truncated at 15 Å** ("Boxplot cut off at 15Å for clarity"), C and D at 10 Å with no caption acknowledgement at all; **per-box n not shown** anywhere, which matters most in C where the 100%-identity bin is the memorisation control |
| 3E-G | p17 / p18 | Successful covalent-modification predictions: BCAT-1 cofactor (7ny2), SARS-CoV-2 3CL protease covalent inhibitor (7lkt), two glycoproteins (7s69, 7ux0), and an IL-27 glycan fitted into cryo-EM density (7u7n / EMDB 26382) with a hydrogen-bond zoom | structure render | `RENDER \| facet: modification class (4: cofactor, covalent drug, glycosylation ×2) × example \| views: 2 for G (density fit, then interaction zoom), 1 elsewhere \| overlay: 1 prediction on 1 reference (G additionally on 1 EM density map) \| axis: none` | 6 render panels across E, F, G; vary by system and, in G, by view | **Selected successes**; the cryo-EM density fit is asserted visually ("fits well in the density", p7) with **no correlation coefficient, no real-space R, no quantitative fit metric at all** |
| 4A | p19 / p20 | The RFdiffusionAA denoising trajectory: ligand → randomised residue gas → partially ordered → folded binder | schematic | `SCHEMATIC \| four-stage denoising cartoon from a small molecule and a random residue gas to a folded binder \| no data` | 1 (4 stages, one arrow chain) | |
| 4B (top row) | p19 / p20 | 2D chemical structures of the four in-silico design targets | schematic | `SCHEMATIC \| 2D chemical structures of FAD, SAM, IAI, OQO \| no data` | 4, varying by ligand; **this letter also appears in the next row of this table** (rows 2–3 of panel B are renders, not chemical structures) | |
| 4B (rows 2-3) | p19 / p20 | Two structurally distinct designs per ligand, each overlaid on the AF2 single-sequence prediction of its own sequence | structure render | `RENDER \| facet: ligand (4: FAD, SAM, IAI, OQO) × design replicate (2) \| views: 1 \| overlay: 1 design on 1 AF2 prediction (+ the ligand) \| axis: none` | 8, varying by ligand and by design; **shares panel letter B with the row above** | **2 of 100 shown**, chosen to "illustrate design diversity" — the diversity itself is only quantified in Fig S6 |
| 4C (top) | p19 / p20 | Rosetta GALigandDock interface ΔG for RFdiffusion+potential vs RFdiffusionAA vs RFdiffusionAA+potential, per ligand, with p-values | box | `PLOT \| facet: ligand (4: FAD, SAM, IAI, OQO) \| vary: method (3) \| series: method (3: RFdiffusion+attr/rep potential, RFdiffusionAA, RFdiffusionAA+attractive potential) \| measure: Rosetta interface ΔG (REU), minimum of 8 LigandMPNN sequences \| mark: box \| n: NOT REPORTED per box and per panel` | 4 panels × 3 boxes, varying by ligand | **The RFdiffusion box runs off the top of the frame in the FAD and SAM panels** — its median and upper quartile are outside the plotted range, so the size of the baseline's failure is unreadable; **per-box n never given**; each observation is already a **best-of-eight** over LigandMPNN sequences |
| 4C (bottom) | p19 / p20 | Cumulative proportion of designs with AF2 RMSD below x, per ligand, three methods, with the 2 Å crossing labelled | line | `PLOT \| facet: ligand (4: FAD, SAM, IAI, OQO) \| vary: AF2 backbone RMSD threshold, 0–8 Å (continuous) \| series: method (3, as above) \| measure: cumulative proportion of designs below threshold (0–1) \| mark: line \| n: NOT REPORTED per panel; each design scored as min of 8 LigandMPNN sequences` | 4 panels × 3 curves | **Per-panel n not shown**; again best-of-eight per design |
| 5A-C (renders) | p21 / p22 | Input motif → design → binding-site zoom, for the digoxigenin binder, the heme binder and three bilin binders, annotated with closest training TM-scores | structure render | `RENDER \| facet: design campaign (3: digoxigenin, heme, bilin) × design (1, 1, 3) \| views: 3 (input motif, whole design, binding-site zoom) \| overlay: 0 predictions on 0 references (designs, no experimental structure exists) \| axis: none` | 15 render panels; vary by campaign, by design, and by view | **No experimental structure of any design is reported** — every structural claim about the designed pockets is a model, and the paper says so implicitly by showing only designs |
| 5A (FP curve) | p21 / p22 | Fluorescence-polarization binding isotherm for the tightest digoxigenin binder, Kd = 10 nM | scatter + line | `PLOT \| facet: none (1) \| vary: digoxigenin concentration, ~1e-10–1e-5 M (continuous, log) \| series: none (1) \| measure: fluorescence polarization (a.u.) \| mark: point + fitted line \| n: NOT REPORTED (replicates not stated)` | 1 | **No error bars and no replicate count**; a single Kd is quoted from a single fitted curve, and **the other two characterised hits are not shown** |
| 5A (CD) | p21 / p22 | CD spectrum of the digoxigenin binder at three temperatures, with a CD-melt inset at 220 nm | line | `PLOT \| facet: none (1) \| vary: wavelength 200–260 nm (continuous) \| series: temperature (3: 25, 75, 95 °C) \| measure: MRE (×1000) \| mark: line \| n: 1 protein at 26 µM; replicates NOT REPORTED` | 1 + 1 inset (melt: intensity at 220 nm vs 25–100 °C) | **Inset y-axis is unlabelled** apart from a bare numeric scale, and the melt is a single trace with no replicate |
| 5B (UV/Vis) | p21 / p22 | Heme binder UV/Vis: designed protein vs C114A knockout vs free heme (Soret at 387 vs 397/399 nm), and the same design at three temperatures | line | `PLOT \| facet: experiment (2: design vs C114A vs free heme; thermal series) \| vary: wavelength ~250–700 nm (continuous) \| series: condition (left 3: design, C114A KO, heme; right 3: 22, 73, 90 °C) \| measure: absorbance (A.U.) \| mark: line \| n: 1 representative design (HEM_3.B10) of 38 heme-retaining; replicates NOT REPORTED` | 2 | **1 of 38 shown** — the panel shows one representative design out of 38 that passed SEC, and the distribution of Soret maxima across the 96 spectroscopically positive designs is never plotted |
| 5C (absorption) | p21 / p22 | Normalised absorption spectra of the three purified bilin binders (557 / 605 / 607 nm), with photographs of the coloured solutions inset | line | `PLOT \| facet: design (3: C11, H4, F9) \| vary: wavelength 400–700 nm (continuous) \| series: none (1) \| measure: normalised absorption (0–1) \| mark: line \| n: 1 spectrum per design; replicates NOT REPORTED` | 3 + 3 photographic insets | **Normalisation to 1 removes all information about extinction coefficient and about how much bilin each design actually incorporated**, which is the property the CpcA comparison turns on; the CpcA-PEB control trace (573 nm) is in Fig S8B, **not on this panel**, so the shift being claimed is not visible in the figure that claims it |
| S1 | p23 | How chirality is encoded: dihedral angles between planes at a chiral centre, for both handednesses | schematic | `SCHEMATIC \| tetrahedral chiral centre in two handednesses, and the plane-pair dihedral angles computed at each \| no data` | 2 rows × 2 chiralities | |
| S2A-B | p24 | Pointwise ligand RMSD, RFAA vs the CAMEO Vina server and vs the CAMEO AD4 server | scatter | `PLOT \| facet: baseline server (2: Vina, AD4) \| vary: RFAA ligand RMSD, 0–30 Å (continuous) \| series: none (1) \| measure: baseline-server ligand RMSD (Å) \| mark: point \| n: 1 per mark, per-panel n NOT REPORTED` | 2, varying by baseline | **Per-panel n not given**, and it is not stated whether these are the same 149 targets as Fig 2C; **both axes clipped at 30 Å** |
| S2C | p24 | Fraction of predicted molecules with all bond lengths / planar angles / chiral centres valid | bar | `PLOT \| facet: none (1) \| vary: structural property (3: bond lengths, planar angles, chiral centres) \| series: none (1) \| measure: fraction of molecules with all valid (0–1) \| mark: bar \| n: NOT REPORTED per bar and per panel` | 1 | **Bar over a distribution**, **no n**, and the x-axis runs 0–1 with all three bars near 0.9–1.0, which compresses exactly the differences the panel exists to show |
| S2D | p24 | Three CAMEO failure modes: right pocket wrong orientation (7xql), pocket formed by an unresolved region (8ii2), small ligand buried too deep (8hwp) | structure render | `RENDER \| facet: failure mode (3: 7xql, 8ii2, 8hwp) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 3, varying by failure mode | |
| S3A | p25 / p26 | RFAA vs RF2 ligand-pocket RMSD and global protein RMSD on held-out ligand-binding proteins, with paired-t p-values | box | `PLOT \| facet: measure (2: ligand-pocket RMSD, global protein RMSD) \| vary: model (2: RF2, RFAA) \| series: model (2: RF2, RFAA) \| measure: RMSD (Å) \| mark: box + outlier points \| n: NOT REPORTED per box and per panel` | 2 | **n never given for either box** in text or caption, despite a paired t-test being reported; **both panels clipped at 5 Å**; and both arms are **pre-filtered on confidence** (PAE<10, pLDDT>0.8), so the panel compares the two models only where both were already confident |
| S3B-D, S3F-G | p25 / p26 | Ligand-aware folding examples: domain placement (7kct), pocket side chains (7kg7), a training-set homolog and a similar-ligand training entry for 7rjj, and the apo-vs-holo conformational shifts in FKBP51 (7b9z) and a tRNA ligase (7ckg) | structure render | `RENDER \| facet: example (6: 7kct, 7kg7, 7rjj, 7b9z, 7ckg, + 7rjj comparators) × model shown (RFAA / RF2 / crystal / training entry) \| views: 1 \| overlay: 2–4 structures on 1 reference \| axis: none` | 8 render panels; vary by system and by which models are superimposed | **The paper's only conformational-change claims live here and are entirely visual** — β3a loop shift and helix repositioning are asserted from renders with **no RMSD, no per-residue metric, no n**; and the caption concedes the FKBP51 shift is "represented in the PDB and our training set" |
| S3E | p25 / p26 | Binding-site RMSD to the holo crystal for apo-input vs holo-input predictions of the same chains, with an identity diagonal | scatter | `PLOT \| facet: none (1) \| vary: holo-state prediction binding-site RMSD, 0–7 Å (continuous) \| series: highlighted example (2: highlighted pink points shown in F–G, all others) \| measure: apo-state prediction binding-site RMSD (Å) \| mark: point \| n: 1 per mark, per-panel n NOT REPORTED` | 1 | **Per-panel n not reported** for the one panel in the paper that measures a conformational effect; no summary statistic, no test, and no statement of how many points lie off the diagonal in each direction; the two illustrated cases are **selected off this scatter after the fact** |
| S4A | p27 | Fraction under 2 Å on the PoseBusters set for eight methods, each in its own input regime | bar | `PLOT \| facet: none (1) \| vary: method (8: RFAA, vina, gold, diffdock, unimol, deepdock, tankbind, equibind) \| series: none (1) \| measure: fraction under 2 Å RMSD \| mark: bar \| n: NOT REPORTED per bar and per panel` | 1 | **Bar over a distribution**; **no n anywhere in the PDF for this set**; and the decisive fact that Vina and Gold receive the bound crystal structure plus a pocket bounding box while RFAA receives only sequence is in the caption, not on the chart |
| S4B | p27 | Waterfall of PoseBusters validity checks: fraction of RFAA's <2 Å docks passing each of ~20 physical criteria | bar | `PLOT \| facet: none (1) \| vary: validity check (20, ordered by pass rate) \| series: none (1) \| measure: fraction of <2 Å docks passing (0–1) \| mark: bar \| n: NOT REPORTED per bar and per panel` | 1 | **No n**; the incremental deltas are annotated (−0.01 … −0.39) but the absolute base count is never stated |
| S4C | p27 | Distribution of the shortest protein–ligand distance among violating predictions, plus one 2.3 Å example | histogram + line | `PLOT \| facet: none (1) \| vary: smallest protein–ligand distance, ~0.75–2.75 Å (continuous) \| series: none (1) \| measure: count of violating predictions \| mark: bar (histogram) + KDE line \| n: ~100 violating predictions summed across bins (total NOT REPORTED)` | 1 + 1 adjoining render | |
| S4D | p27 | RFAA vs DiffDock ligand RMSD, split by whether the complex contains a cofactor | box | `PLOT \| facet: cofactor presence (2: no cofactor, has cofactor(s)) \| vary: method (2: DiffDock, RFAA) \| series: method (2) \| measure: ligand RMSD (Å) \| mark: box + outlier points \| n: NOT REPORTED per box and per panel` | 2 | **Truncated at 20 Å**; **per-box n not given**, which is the whole point of a split-by-subgroup panel — the "has cofactor(s)" subgroup could be small |
| S5A | p28 | Histogram of glycosylation RMSDs on recently solved glycoproteins | bar | `PLOT \| facet: none (1) \| vary: glycosylation RMSD bin (5: 0-2.5, 2.5-5, 5-8, 8-10, 10+ Å) \| series: none (1) \| measure: count of predictions \| mark: bar \| n: ~300 summed across bins (total NOT REPORTED)` | 1 | Binning is **uneven in width** (2.5, 2.5, 3, 2, open) which distorts the visual shape of the distribution; the open top bin hides how bad the failures are |
| S5B | p28 | Successfully predicted IL-27 quaternary signalling complex glycoprotein (7u7n) | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 1 | Selected success |
| S5C | p28 | Glycan lDDT-Interaction split three ways: homolog in training, number of resolved monosaccharides, and PAE Interaction bin | box | `PLOT \| facet: stratifying variable (3: homolog in training set, number of resolved monosaccharides, PAE Interaction) \| vary: stratum (2 / 8 / 6) \| series: none (1) \| measure: all-atom lDDT Interaction (0–1) \| mark: box + outlier points \| n: NOT REPORTED per box and per panel` | 3 panels, 16 boxes | **Per-box n not shown**, and the monosaccharide-count panel plainly has very unequal bins (chains of 7–8 monosaccharides must be rare), so the "longer glycans can still be successfully modeled" claim rests on invisible counts |
| S6 | p29 | Number of TM-score clusters vs clustering threshold, for RFdiffusionAA on four ligands and two RFdiffusion reference regimes — the design-diversity panel | line | `PLOT \| facet: none (1) \| vary: minimum intra-cluster TM-score threshold, 0–1 (continuous) \| series: model:motif (6: RFdiffusionAA FAD / SAM / IAI / OQO, RFdiffusion protein-motif 5TRV, RFdiffusion unconditional) \| measure: number of clusters (0–100) \| mark: line \| n: 100 unfiltered designs per curve` | 1, six curves | **The measure ceilings at 100 by construction** (100 designs), and four of six curves reach it before TM 0.8, so the right-hand third of the panel carries no information; this is a real numeric ceiling and is the one place in the paper where a metric saturates |
| S7A-C | p30 | Distributions of TM-score of 400 designs to the training set, versus to training proteins bearing the same ligand: mean, max, and max restricted to self-consistent designs | histogram | `PLOT \| facet: statistic (3: mean TM, max TM, max TM among AF2-self-consistent designs) × ligand (2: FAD, SAM) \| vary: TM-score, ~0.25–0.85 (continuous) \| series: reference set (2: training dataset, training dataset – same ligand) \| measure: count of designs (0–300) \| mark: bar (overlaid histograms) \| n: 400 designs per panel in A–B; subset in C (count NOT REPORTED)` | 6 panels, varying by statistic and ligand | **Panel C's n is never given** — it is the self-consistent subset of the 400, and the whole force of C is that filtering does not change the picture, which cannot be judged without the count; **A and C share no common y-scale with B** |
| S7D | p30 | The median-TM design overlaid on the closest PDB structure binding the same ligand, for two ligands | structure render | `RENDER \| facet: ligand (2: FAD, SAM) \| views: 1 \| overlay: 1 design on 1 native protein \| axis: none` | 2 | |
| S8A | p31 | Topology cartoons and electrostatic space-filling models for CpcA and the three bilin designs | structure render | `RENDER \| facet: protein (4: CpcA control, C11, F9, H4) × representation (2: topology, electrostatic surface) \| views: 1 \| overlay: 0 predictions on 0 references \| axis: none` | 8 | Electrostatic surfaces are shown on a **blue–red scale with no numeric legend or units**, yet a quantitative charge–wavelength correlation is claimed from them in Fig S9 |
| S8B | p31 | Normalised absorption spectra of CpcA and the three designs, with solution photographs inset | line | `PLOT \| facet: none (1) \| vary: wavelength (continuous) \| series: protein (4: CpcA, C11, F9, H4) \| measure: normalised absorption \| mark: line \| n: 1 spectrum per protein; replicates NOT REPORTED` | 1, four curves + insets | **Normalisation hides incorporation efficiency**, the property the CpcA comparison is about |
| S8C | p31 | Absorptance and emission profiles of CpcA and the three designs, with the excited region shaded | line | `PLOT \| facet: protein (4: CpcA, C11, H4, F9) \| vary: wavelength (continuous) \| series: quantity (2: absorptance, emission) \| measure: normalised absorptance / emission, with shaded area under each \| mark: line + shaded area \| n: 1 per protein; replicates NOT REPORTED` | 4 | The relative quantum yields (100 / 57.6 / 17.1 / 38.4%) are given as caption text, **not as a plotted quantity with error** |
| S9 | p32 | Maximal absorption wavelength against coulombic potential within 5 Å of the chromophore | scatter | `PLOT \| facet: none (1) \| vary: coulombic charge within 5 Å of the bilin (continuous) \| series: none (1) \| measure: maximal absorption wavelength (nm) \| mark: point \| n: 1 per mark; per-panel n NOT REPORTED (at most a handful of designs)` | 1 | **Almost certainly n ≈ 3–9** — the paper only ever characterises three purified and nine screened bilin binders — yet a correlation is asserted in the text ("The degree of red shifting largely correlates with the strength of negative coulombic potential within 5 Å of the chromophore", p10) with **no n, no r, and no p-value**. The one-line caption gives nothing |
| S10 | p33–p34 | For each design campaign, the design, the closest training entry binding a similar ligand, their superposition, and a binding-site comparison | structure render | `RENDER \| facet: design campaign (3: digoxigenin, heme, bilin) × comparison stage (4: design, closest hit, superposition, binding-site zoom) \| views: 1 \| overlay: 1 design on 1 training-set structure \| axis: none` | 12 | The claim being supported ("the closest entry with a similar ligand in the training set by TM score is below 0.62") is **quantitative but is shown only as renders**; the TM-score distribution behind "below 0.62" is not plotted here |
| S11A | p35 | Per-target GDT of RFAA against AF2 and against RF2 on 126 CASP14 monomers, coloured by difficulty | scatter | `PLOT \| facet: comparator (2: AF2, RF2) \| vary: RF All-Atom GDT, 0–1 (continuous) \| series: CASP14 difficulty class (3: TBM-hard, FM/TBM, FM) \| measure: comparator GDT (0–1) \| mark: point \| n: 1 per mark, 126 structures per panel` | 2, varying by comparator | The headline "median GDT of 85 vs. 86" (p11) is **not shown on the panel** and cannot be read off a scatter; per-difficulty-class counts are not given |
| S11B | p35 | Per-target all-atom lDDT of RFAA against RFNA on 89 held-out protein–nucleic acid complexes | scatter | `PLOT \| facet: none (1) \| vary: RF All-Atom all-atom lDDT, 0–1 (continuous) \| series: none (1) \| measure: RFNA all-atom lDDT (0–1) \| mark: point \| n: 1 per mark, 89 structures per panel` | 1 | The headline "median allatom-LDDT of 0.74 vs. 0.78" (p11) is **not marked on the panel**; the points sit visibly above the diagonal (RFNA better) and no summary or test quantifies the gap |

**`reuse` (identical for every row above).** **CC-BY-ND 4.0 International** — printed in the
header of **every one of the 40 pages**, e.g. p1: "It is made available under a **CC-BY-ND 4.0
International license**." **The ND (no-derivatives) clause forbids modifying a figure AND forbids
redrawing it** — a redrawn or restyled version is a derivative work. Reproduction of an unaltered
panel with attribution is permitted; **any adaptation, recolouring, cropping-for-effect,
re-plotting from the same data, or incorporation into a composite figure is not.** If a panel
from this paper is needed in the manuscript, either (a) reproduce it unaltered with full
attribution, (b) obtain the corresponding panel from the **Science version (10.1126/science.adl2528)
under whatever licence that carries — not held, see `unresolved`**, or (c) request permission.
**Do not redraw.** This is the strictest licence in the corpus so far and it applies to all 45
panel-group rows above.

---

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), single-paper extraction against SCHEMA.md v3.
- **schema_version**: v3
- **confidence**: **high** for the prediction-arm numbers, the architecture description, the
  training composition, the claims, and the licence — all are in running main text or held figure
  captions and were read directly. **High** for the central negative finding (no stated training
  cutoff date): the full text was grepped for "cutoff", "cut-off", "post-", "deposited",
  "held-out" and every four-digit year, and p6 and p7 are the only two hits that bear on the
  train/test boundary. **Medium** for figure `n` values, which are absent from most captions and
  had to be recorded as NOT REPORTED, and for the exact PoseBusters comparator percentages in
  Fig 2E / S4A, which are readable only as bar lengths. **Medium-low** for anything in the
  Supplemental Methods, which are not held.
  Eleven pages were rendered to PNG at 100–110 dpi to fill `data_shape` where captions did not carry
  panel structure — p15 (Fig 2), p17 (Fig 3), p19 (Fig 4), p21 (Fig 5), p24 (S2), p25 (S3), p27
  (S4), p28 (S5), p29 (S6), p30 (S7), p35 (S11) — and deleted afterwards.
- **unresolved**:
  1. **The training cutoff date.** Never stated. "the cutoff date for our training set" (p6) is
     the only reference to it and carries no date; "post-May, 2020" (p7) dates a *test* set. If a
     specific day is needed, it must come from the Science version, the released weights, or the
     Supplemental Methods — **none of which is held**. Flagged because two corpus papers define
     held-out sets against this value.
  2. **Venue split.** The PDF held is the bioRxiv preprint of 9 October 2023 (CC-BY-ND 4.0, not
     peer reviewed). The version of record is **Science (2024), DOI 10.1126/science.adl2528**,
     which is **not held**. The Science version may differ in: the stated cutoff date, the exact
     n's, the figure set, the supplementary organisation, and — critically for `reuse` — the
     licence. **Every page number in this note refers to the preprint and will not transfer to the
     Science pagination.** Tagged `preprint`, not `peer-reviewed`.
  3. **931 vs 938.** The covalent-modification test set is "931 recent entries" in the text (p7)
     and "938 recently solved structures" in the Fig 3B caption (p18). Neither is corrected. Seven
     structures unaccounted for; the 46% success rate is quoted against the 931 figure.
  4. **PoseBusters set size.** Never stated in this PDF; the 42% / 38% / 52% comparison in
     `metrics_reported` therefore has no denominator here.
  5. **Held-out ligand-binding-protein set size** for the RFAA-vs-RF2 comparison (Fig S3A, p26) is
     never given, although a paired t-test with p = 6.7e-10 is reported from it.
  6. **Two conflicting supplementary figure numbering schemes.** p10 cites "Supplementary
     Information Figures 9-11" for heme thermostability data, but this PDF's Figures S9, S10 and
     S11 are the bilin coulombic-charge correlation, the design-novelty renders, and the
     AF2/RFNA comparison respectively. There is therefore a **second, unheld supplementary figure
     series**, and the heme thermostability evidence beyond Fig 5B cannot be checked.
  7. **Template date-filtering for the post-cutoff benchmarks.** Templates are an input (p3, p18)
     but the paper never says whether template searches were restricted by deposition date for the
     recent-PDB, covalent-modification, CASP14 or protein–NA test sets. This is the one open route
     by which target-state structural information could reach the network on a "post-cutoff" test.
     Recorded as an unquantified route-1 exposure in `oracle_leakage`.
  8. **No data-availability, code-availability or competing-interests statement** anywhere in this
     PDF. Unusual for a Baker-lab release; presumably added in the Science version.
  9. **Samples per target is never stated** for RFAA. Whether the CAMEO server submitted one model
     or a ranked set, and how many recycles were used at inference, are both unrecoverable here.
  10. **No tag was needed that the v3 vocabulary lacks.** Every tag applied below is from the fixed
      list. Two near-misses are recorded for the schema owner rather than invented:
      (a) there is no tag for **all-atom / non-protein-component modelling** (small molecules,
      metals, covalent modifications, glycans) as a *capability class* — `cofolding` is the closest
      and is what was used, but it does not distinguish a ligand-docking co-folder from a model
      that also does glycans, metals and nucleic acids in one pass, which is this paper's entire
      novelty claim; (b) there is no tag for a **generative design / de-novo binder-design** arm.
      `experimental-validation` was used and correctly marks that wet-lab work happened, but the
      corpus cannot currently retrieve "papers with a de-novo design arm" as distinct from "papers
      that validated a prediction experimentally". Both are recorded here, **not invented**.
  11. **Ambiguity remaining in v3, reported bluntly** (see the report-back note at the end of
      `EXTRACT_PROMPT.md`):
      - **The panel-split rule under-determines `vary`.** The rule splits on `mark` or `measure`
        but says nothing about `vary`. Fig 2B, 2F and 2G are all box plots of ligand RMSD and
        differ only in the stratifying variable, so a literal reading merges all three into one
        row — losing the fact that 2B is 261 CAMEO targets while 2F–G are 1,681/3,261 clusters
        from a different benchmark. I split 2B from 2F-G and merged 2F with 2G, and did the same
        for Fig 3B-D, but the rule does not decide this and two extractors will not agree.
        **Suggest: also split when the underlying dataset or n differs, even at identical mark and
        measure.**
      - **`facet` and `vary` collide for stratified box panels.** In Fig 2F-G and Fig 3B-D the
        thing that splits sub-panels is *which stratifying variable is used*, and the thing that
        varies within a panel is *which stratum*. Writing `facet: stratifying variable (3)` and
        `vary: stratum (4/5/3)` is the only honest encoding but it is a meta-level facet, not a
        data variable, and it will not join against a normal `facet: system (3)`.
      - **`n` for a histogram has no home.** For Fig S5A and S7A-C the meaningful n is the total
        behind the histogram, not per bar; `n: <per mark, and per panel>` reads oddly and I wrote
        the total in the per-panel slot.
      - **`overlay` is wrong for design renders.** Fig 5A-C and S8A show *designed* proteins with
        no experimental reference at all. `overlay: 0 predictions on 0 reference(s)` is literally
        true but reads as missing data rather than as "no reference exists". **Suggest an explicit
        `overlay: none (no experimental reference exists)` form.**
      - **A figure that is a plot *of* another figure's selection has nowhere to be flagged.** The
        best-of-cluster selection in Fig 2F is recorded in `hides` and in `oracle_leakage` route 6,
        but a reader querying the figure table alone would have to read the whole `hides` cell to
        learn that the panel is an upper bound rather than a performance estimate.
      - **`metric_saturation` vs `hides` is now clean** (v3 change 9 works), but Fig S6's ceiling
        at 100 clusters is a *numeric* ceiling caused by the sample size, not by the metric's
        range. I recorded it in `hides` on the S6 row and noted it in `metric_saturation`; the
        schema does not say which is canonical for a sample-size-induced ceiling.
- **why_it_matters**: *(left empty by the extractor — the user's call)*

---

## Tags

`general-protein` `cofolding` `templates-on` `single-state` `binary-predicate`
`continuous-metric` `rmsd-only` `visual-metric` `oracle-leak` `design-level-oracle` `prospective`
`anti-memorization` `confidence-as-discriminator` `multi-backbone` `experimental-validation`
`ligand-driven` `preprint` `precedent` `background` `comparator-numbers`

**Tag justifications where the call is not obvious:**

- `general-protein` — no system family is studied; the paper spans arbitrary proteins, nucleic
  acids, metals and small molecules. No GPCR, kinase, transporter, periplasmic-binding, ATPase or
  fold-switching content anywhere.
- `cofolding` — joint prediction of protein plus non-protein components in a single forward pass
  from sequence and bonded graph (p1, p5). The nearest available tag; see `unresolved` item 10(a).
- `templates-on` — homologous templates are an input (p3; Fig 3A caption p18). **Not**
  `no-template-no-msa`, and **not** `state-annotated-input` (no state annotation is used).
- `single-state` — one deterministic structure per input; no ensemble, no sampling over states.
  Not `two-state`: the apo/holo panel uses two *inputs*, not two states from one input.
- `binary-predicate` + `continuous-metric` + `rmsd-only` — headline results are thresholded
  predicates (<2 Å, <2.5 Å) over continuous RMSD distributions, all measured against a deposited
  reference.
- `visual-metric` — every conformational claim in the paper (Fig S3B–C, S3F–G, the cryo-EM density
  fit) is called by eye from a render with no operationalised predicate. Applied deliberately: it
  is the paper's one clear rigour gap in the states dimension.
- `oracle-leak` — route 6, quoted verbatim: "the lowest Ligand RMSD cluster representative is
  chosen for each" (Fig 2F caption, p16). The generalisation numbers most likely to be cited
  (41/23%, 20/16%) are best-of-cluster selections against the held reference.
- `design-level-oracle` — route 7, weaker and correctly disclosed: the conformational-shift
  exemplar was selected off a scatter after scoring and its answer is conceded to be "represented
  in the PDB and our training set" (Fig S3F caption, p26). Kept distinct from `oracle-leak`.
- `prospective` — applies to the CAMEO arm and the wet-lab design arm only; the note records the
  arm-by-arm split rather than letting the tag imply the whole paper.
- `anti-memorization` — four post-cutoff control arms were actually run and analysed with large n.
  **Not** `no-anti-memorization`, and **not** `unpowered`.
- `confidence-as-discriminator` — PAE Interaction < 10 gates the headline claims (p5, p7) and
  selects analysis subsets (Fig S3A, p26).
- `multi-backbone` — AF2, RF2, RFNA, DiffDock, Uni-Mol, DeepDock, TankBind, EquiBind, AutoDock
  Vina and Gold are all compared head to head against RFAA; far more than two.
- `experimental-validation` — FP, CD, UV/Vis, SEC, whole-cell screening and fluorescence
  spectroscopy on designed proteins (p9–p10). **Not** `experimental`, which marks a paper with no
  structure prediction in it at all.
- `ligand-driven` — the only conformational handle in the paper is the presence or absence of the
  ligand in the input (Fig S3E–G, p26), and for the design arm the ligand conformation is the
  primary conditioning motif (p8). **Not** `directed-state`, `partner-driven`, `peptide-driven`,
  `g-protein-mimetic`, `nanobody`, `apo-sampling` or `seed-only` — the paper does no apo-ensemble
  sampling and never varies a seed.
- `preprint` — the PDF held is the bioRxiv preprint, "not certified by peer review" (p1). **Not**
  `peer-reviewed`, even though a Science version exists, because the Science version is not held.
- `precedent` + `background` — see `stance`. Provisional.
- `comparator-numbers` — 40+ extractable headline values across the two arms.
- **Deliberately NOT applied:** `msa-subsample`, `msa-state-filter`, `template-state-bias`,
  `af-cluster`, `latent-steering`, `md`, `md-emulator`, `enhanced-sampling`, `benchmark-only`
  (none of these methods is used); `two-state`, `ensemble`, `continuum` (nothing multi-state is
  generated); `saturating-metric` (no metric saturates numerically except the sample-size ceiling
  in Fig S6, which is not a property of the metric); `orthosteric`, `allosteric-site`,
  `cryptic-pocket`, `allosteric-failure` (no site framing anywhere); `no-anti-memorization`,
  `unpowered` (contradicted by four well-powered control arms); `threat`, `contrast`,
  `negative-result` (see `stance`); `figure-exemplar` (the figures are competent but the paper is
  kept for its content, not its charts, and the ND licence forbids redrawing them anyway).
