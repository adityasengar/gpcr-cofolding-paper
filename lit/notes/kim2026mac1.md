# kim2026mac1

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–39).** The PDF carries no
printed folios. Layout: p1 title/abstract, p2–3 Introduction, p3–14 Results (figures on p5, p7,
p10, p11, p14), p15–16 Discussion, p17–19 Methods, p20 Acknowledgements/Competing
interests/Author contributions, p21 Supplementary Information index, p22–34 Supplementary Figures
S1–S13, p35–39 References.

**Read-through caveat:** all quotes below are from `pdftotext -layout`. Panels on p5, p7, p10, p11
and p14 were rendered at 150 dpi with `pdftoppm` and read, because the Fig 2a and Fig 2b summary
tables (which carry the headline success rates and the conformational-state counts) and the Fig 3a
and Fig 5 AUROC legends are **image-only and do not appear in the extracted text at all**. Every
success rate in `metrics_reported` marked *(Fig 2a table, read from render)* was read off that
rendered table; the digits are printed and are exact, not estimated. Supplementary Figures S1–S13
were **not** rendered; their rows in section F are caption-derived and are marked as such.

---

## A. Identity

- **citekey**: `kim2026mac1`
- **doi**: **10.64898/2025.12.25.696505** (bioRxiv) — banner on every page, e.g. p1: "bioRxiv
  preprint doi: https://doi.org/10.64898/2025.12.25.696505; this version posted March 18, 2026."
  Matches `refs.bib`.
- **year**: **2026** as posted (this version posted **18 March 2026**, p1). The DOI stem
  `2025.12.25` indicates the v1 posting date of 25 December 2025; the corpus PDF is **v3**.
  `refs.bib` records `year = {2025}`, which is the v1 year, not this document's.
- **venue**: **bioRxiv preprint, not certified by peer review** — p1: "The copyright holder for this
  preprint (which was not certified by peer review) is the author/funder." Tagged `preprint`.
- **title**: **"Large scale prospective evaluation of co-folding across 557 Mac1-ligand complexes
  and three virtual screens"** — p1.
- **authors**: Jongbin Kim, Galen J. Correy, Brendan W. Hall (these three contributed equally),
  Moira M. Rachman, Olivier Mailhot, Takaya Togo, Ryan L. Gonciarz, Priyadarshini Jaishankar,
  R. Jeffrey Neitz, Eric R. Hantz, Yagmur U. Doruk, Maisie G. V. Stevens, Morgan E. Diolaiti,
  Rashad Reid, Saumya Gopalkrishnan, Nevan J. Krogan, Adam R. Renslo, Alan Ashworth,
  **Brian K. Shoichet** and **James S. Fraser** (co-corresponding) — p1. All UCSF (+ Gladstone).
  Shoichet lab (docking) + Fraser lab (crystallography) joint paper.
- **code/data**: co-folding input/post-processing scripts at
  `https://github.com/jongbin99/Cofolding` (p18). Docked hit lists from `lsd.docking.org` (p18).
  **Supplementary Table 1 (X-ray data statistics) is deliberately embargoed** — p21: "X-ray data
  statistics will be released after a small delay to preserve the potential for blind predictions
  by any new methods."

## B. Scope

- **system**: **general protein — one enzyme for the pose arm, three unrelated targets for the
  virtual-screen arm.** Pose arm: SARS-CoV-2 NSP3 macrodomain 1 (**Mac1**), an ADP-ribosylhydrolase
  / viral antiviral target (p1, p3). Virtual-screen arm: **AmpC β-lactamase** (bacterial enzyme),
  the **σ₂ receptor** (TMEM97) and the **dopamine D4 receptor** (a GPCR) (p3, p12). All ligands are
  orthosteric/active-site binders — the 557 Mac1 ligands "all bind in the active site where they
  compete with the substrate, ADP-ribosylated (ADP-r) peptides" (p3).
- **n_targets**: **4 total, but the two arms must not be pooled. Pose-prediction arm: 1 protein
  (Mac1), 557 ligand complexes. Virtual-screen / hit-triage arm: 3 proteins (σ₂, D4, AmpC), 2,340
  experimentally tested molecules.** The paper's central pose result rests on a **single target**.
  Authors flag this themselves — see `stated_limits`.
- **method_class**: **benchmark-only** (prospective/temporal-holdout evaluation of existing
  co-folding models). No new method, no new architecture, no fine-tuning. Secondary arm is
  **rescoring** of published docking hit-lists. The crystallography is the authors' own (p17) but
  is the ground truth, not an experimental test of a prediction, so this is not
  `experimental-validation` in the schema's sense.
- **backbones**: **AlphaFold3, Chai-1, Boltz-2** head to head on the pose arm, plus **DOCK3.7** as a
  physics-based non-ML baseline (p4, p17–18). Virtual-screen arm uses **AF3 and Boltz-2 only** —
  "For further sets of analyses with docked hit lists... only AlphaFold3 and Boltz-2 were used"
  (p18). Three co-folding backbones compared → tagged `multi-backbone`. Sources: AF3
  `github.com/google-deepmind/alphafold3`, Chai-1 `github.com/chaidiscovery/chai-lab`, Boltz-2
  `github.com/jwohlwend/boltz` (p18). Run on NVIDIA A40 GPUs (p18). **Version/commit hashes and
  weight releases: NOT REPORTED.**
- **templates**: **NOT REPORTED.** The only statement of inputs is "Three co-folding methods
  (AlphaFold3, Chai-1, and Boltz-2) were given the SMILES strings of each ligand and the sequence of
  the enzyme as inputs" (p4) and "Ligand SMILES and amino acid sequences for the target protein were
  used to perform co-folding" (p18). Whether each tool's **default template search was left on** —
  which for Mac1 would retrieve dozens of pre-cutoff Mac1 structures — is never stated. This is the
  single largest protocol gap in the paper; see `oracle_leakage` route 1 and `unresolved`.
- **msa_handling**: **full** (not subsampled, not clustered, not state-filtered) — p18: "Multiple
  Sequence Alignment (MSA) was performed with the Jackhammer module." [sic: jackhmmer]. Depth,
  database and any depth cap: **NOT REPORTED**.

## C. Conformational core

- **states_generated**: **one.** One predicted protein–ligand complex per ligand per method; the
  number of diffusion samples, seeds or recycles behind each is **NOT REPORTED** (p18 describes no
  sampling settings). Across the 557 predictions the receptor does **not** move: "protein alignment
  gave generally low global C-alpha RMSDs (range 0.1 Å – 0.4 Å; STable 3)" (p6). This is a
  single-basin result, not an ensemble — the paper's own finding is that the models fail to leave
  the ground state (4/19 twisted, 0/20 open; Fig 2b table, p7). Tagged `single-state`.
- **structural_priors_used**: several, all legitimate and all at design/evaluation time, none in the
  co-folding input:
  1. **PDB 5SQW as the DOCK3.7 receptor** — p17: "The modelled orthosteric site of the Mac1 model
     was available from the PanDDA analysis group deposition in the Protein Data Bank (PDB), with
     PDB ID: 5SQW (Gahbauer et al. 2023). We used this structure because the inhibitor
     (Z5014193706) was the most potent molecule with a structure determined around the same time as
     the ligands in this dataset were tested." 45 matching spheres derived from it. This is a prior
     for the **docking baseline only**; co-folding received no structure.
  2. **5SQW again as the reference for defining alternate receptor conformations** — SFig 3a caption
     (p24): "The density distribution plot shows RMSD between residues in PDB ID: 5SQW, and 557
     complexes obtained from crystallography, a filter that was used to define alternate
     conformations." Also Fig 2b caption (p7): "residues in green are from PDB ID: 5SQW".
  3. **The authors' own ~1,000 Mac1 crystal structures**, of which ~326 were already public — p3:
     "we determined x-ray crystal structures for ~1000 small molecules bound to Mac1, typically at
     close to 1 Å resolution... only up to 326 of our molecules... were available in public
     databases prior to the training cutoffs". The benchmark exists because this prior exists.
  4. **Human MacroD1 open-state structures (PDB 2X47, 6LH4)** cited to argue the open state is a
     genuine macrodomain feature rather than a Mac1 artefact (p6).
  5. **Ground-truth reference poses**: "ultra-high-resolution (~1.0 Å) crystal structures" (p19),
     used only as the evaluation reference.
- **oracle_leakage**: enumerated route by route. Protocol is described on **p4, p17–19**.
  1. **Structures used as input or template — NONE FOUND for the co-folding arm, on the evidence
     given, but not closed.** p4: "Three co-folding methods (AlphaFold3, Chai-1, and Boltz-2) were
     given the SMILES strings of each ligand and the sequence of the enzyme as inputs." p18: "Ligand
     SMILES and amino acid sequences for the target protein were used to perform co-folding." No
     template flag, no `--no-templates`, no statement that templates were disabled. **PRESENT by
     construction for the DOCK3.7 baseline** (PDB 5SQW receptor, p17) — that is docking's normal
     operating mode, uses a pre-cutoff structure bound to a *different* ligand, and is recorded here
     for completeness rather than as a defect.
  2. **State annotations from a curated database driving templates or alignments — NONE FOUND.**
     Methods p17–19 name only the PDB, RDKit, PyMOL, AMBER/QNIFFT/Corina/Omega (docking) and
     jackhmmer. No GPCRdb, KLIFS, Kincore or equivalent appears anywhere in the paper.
  3. **Cluster labels derived from known states — NONE FOUND.** Clustering in this paper is
     **chemical, not conformational**: "Best-First Clustering (BFC) based on these similarity
     metrics was used to estimate the number of unique chemotypes represented in each dataset"
     (p17). No protein-state cluster labels enter any prediction.
  4. **Hyperparameters, thresholds or sweep ranges tuned against the evaluation set — PRESENT,
     three separate instances, none touching model weights but all touching reported numbers.**
     (a) The chemotype clustering threshold was fitted on the benchmark and then exported: "Within
     the Mac1 benchmark set, applying an MCS cutoff of 35% yielded four distinct scaffolds, in
     agreement with PCA-derived cluster separation. The same clustering threshold was subsequently
     applied to define scaffold families for the AmpC, σ₂ and D4 benchmark datasets" (p17).
     (b) The **activity threshold defining a "true hit" was loosened relative to the source papers**:
     "True hits among these docked molecules were previously defined as displacing greater than 50%
     of 3H ditolylguanidine ([3H]DTG) to σ₂ (Alon et al. 2021), but in our work, the cutoff is
     adjusted to 25% displacement, giving a less stringent threshold to include more molecules into
     the space of true hits" (p18); the same loosening is applied to D4 (p18). Every AUROC and KS
     statistic in Fig 5 is computed against these re-drawn labels.
     (c) The **Boltz-2 affinity calibration is fitted on the same data whose error is then
     reported**: "Empirically correcting with a linear fit reduced this error to ~0.7 kcals (0.54
     pIC units)" (p9); the same in-sample linear correction is applied to all three screens (p12–13,
     SFig 9–10). The abstract's headline — "after calibration, achieved lower mean absolute error
     than a baseline predictor" (p1) — is therefore an **in-sample calibrated number**. No held-out
     split for the calibration fit is described.
  5. **Success defined post hoc by RMSD to a structure they held — PRESENT, by design and openly
     stated.** p4: "we used a threshold of ligand center of mass < 2.5 Å after alignment of protein
     structures"; p4: "Using the field standard, 2 Å cutoff for correct predictions"; p19: "The
     heavy-atom root-mean-square deviation (RMSD) between the aligned co-folded ligand and its
     crystallographic counterpart was then calculated." The reference structures were **never
     public**, so this is not memorisation leakage — but it is the standard, disclosed form of route
     5 and is recorded as such. The 2 Å and 2.5 Å thresholds are field conventions with citations
     (Nittinger et al. 2025 for the 2.5 Å COM filter, p4/p19), not values fitted here.
  6. **Best/worst labels assigned against a held reference — PRESENT for illustrative examples
     only.** mac-x3927 is labelled "Successful ligand pose recovery with all methods" and mac-x4091
     "Ligand pose recovery failed with all methods" (Fig 3 panel labels, p10); the three exemplars
     in Fig 2c (Mac-x5015 L-RMSD 1.00 Å, Mac-x3538 0.37 Å, Mac-x4088 0.75 Å, p7) are chosen after
     the RMSDs are known and are explicitly the low-similarity/high-accuracy cases. Aggregate
     numbers are unaffected. **But the paper never states how the single reported pose per ligand
     was chosen from each model's samples** — see `metrics_reported` and `unresolved`; this is the
     one place where an oracle-selected number could hide and the paper does not close it.
  7. **Design-level oracle use — PRESENT, and conceded by the authors.** The target was chosen
     because the authors' own lab holds the structures, and the models had already trained on ~326
     Mac1 ligand complexes from the same campaign. p15, verbatim: "The Mac1 benchmark, while diverse
     by ECPP4 Tc, is nevertheless dominated by four groups when clustered by MCS and benefits from a
     large training set of fragment molecules bound to the protein in the training set (Schuller et
     al. 2021). This may inflate apparent pose recovery rates, although Boltz-2 predicted poses were
     poorly recapitulated even with its much later training cutoff dates." Second design-level
     point: **the 557-ligand pose set contains only true binders** ("Note that Mac1 dataset comprises
     only actives", SFig 13 caption, p34), so on the pose arm the models are never asked to reject a
     non-binder. Third: the three virtual screens are re-analyses of campaigns published by the same
     group (Lyu 2019, Alon 2021, Liu 2025), with hit/non-hit labels the authors then re-drew (route
     4b). Tagged `design-level-oracle` alongside `anti-memorization` — the two coexist here.
- **prospective**: **partial — and the two arms differ, so a single word would be a lie.**
  - **Pose arm (Mac1, 557 complexes): a genuine strict temporal holdout at the ligand level, but
    NOT a blind prospective prediction.** Evidence for the holdout: the structures were never
    public — "we identified 557 ligands where we determined X-ray structures that have not been
    disclosed previously" (p3); "only up to 326 of our molecules... were available in public
    databases prior to the training cutoffs (e.g. 2021-09-30 for AF3, 2023-06-30 for Boltz-2)" (p3);
    abstract, p1: "557 ligands bound to the SARS-CoV-2 NSP3 macrodomain (Mac1) that were determined
    after the training cut-off dates." Evidence against calling it blind: the structures were solved
    by the authors **before** the predictions were run, so the predictors held the answers
    throughout; the paper draws this distinction itself when it embargoes STable 1 "to preserve the
    potential for blind predictions by any new methods" (p21) — i.e. the authors regard a blind test
    as something still to come. The protein itself, and 326 chemically related ligand complexes from
    the same campaign, are inside the training data (p3, p15). So: **prospective with respect to the
    models (post-cutoff, never-deposited, un-memorisable at the ligand level); retrospective with
    respect to the experiment (a post-hoc temporal split on data the authors already held).**
  - **Virtual-screen arm (σ₂, D4, AmpC): retrospective.** The compounds and their measured
    activities come from three **already-published** campaigns — Lyu et al. 2019 (D4), Alon et al.
    2021 (σ₂), Liu et al. 2025 (AmpC) (p3, p12, p18). The word "prospective" in the paper's own
    sentences refers to the *original* campaigns' prospective synthesis-and-test, not to this
    paper's rescoring: "hit lists from recent large library, prospective docking against three
    well-behaved targets" (p3). The paper **never claims these three sets are post-cutoff** and
    never gives a cutoff comparison for them; two of the three source papers predate AF3's
    2021-09-30 cutoff. Tagged `prospective` on the strength of the Mac1 arm only.
- **state_metric**: **RMSD-to-reference + binary predicate. This paper's primary metric is LIGAND
  POSE, not protein conformational state**, and that must not be blurred.
  - *Ligand pose* (the headline): heavy-atom **L-RMSD < 2 Å** to the crystal pose after
    least-squares superposition of all Cα atoms in PyMOL, computed with
    `rdMolAlign.CalcRMS` after an RDKit sanitisation + substructure-match atom mapping (p4, p19).
    Threshold justified as "the field standard, 2 Å cutoff for correct predictions" (p4).
    Pre-filter: **ligand centre-of-mass distance < 2.5 Å**, a binary in-pocket predicate, "If the
    distance exceeds 2.5 Å, we would expect the RMSD to be large, indicating that ligand poses are
    not modelled accurately in an orthosteric pocket (Nittinger et al. 2025)" (p19).
  - *Receptor conformational state* (secondary, AF3 only): a **binary predicate on per-residue
    RMSD to PDB 5SQW** — "twisted backbone (Phe156 RMSD > 1.5 Å) and open structure (Gly130 RMSD,
    Ala129 RMSD > 3 Å)" (SFig 3a caption, p24). The 1.5 Å and 3 Å thresholds are stated but **not
    justified**. The open state is additionally described in the text as "a ~8 Å loop rearrangement
    including Gly130 and Ala129" (p6).
  - *Affinity*: Pearson r and MAE in pIC₅₀/kcal against HTRF IC₅₀ or radioligand-displacement
    apparent Kᵢ (p9, p12–13, p19).
  - **Receptor conformational variation WAS examined**, and this is one of the paper's real results:
    global Cα RMSD 0.1–0.4 Å across all 557 (p6, STable 3); 19 twisted and 20 open experimental
    alternate conformations identified; AF3 recovered 4/19 and 0/20 with 8/538 and 0/537 false
    positives (Fig 2b table, p7). **Only AF3 was assessed for conformational state** — Chai-1 and
    Boltz-2 were not (Fig 2b caption, p7: "ability of AF3 to capture these conformational changes").
- **metric_saturation**: **numeric floor in one arm, and a ceiling imposed by a pre-filter.**
  (i) **Floor:** open-state recovery is **0/20 = 0%** and its false-positive rate **0/537 = 0%**
  (Fig 2b table, p7) — the metric is pinned at zero at both ends with n = 20, so no effect size or
  direction can be estimated; this arm is unpowered rather than merely negative.
  (ii) **Ceiling:** the COM < 2.5 Å pre-filter passes 92–94% of co-folding poses (519/550, 509/551,
  511/548; p4), so the in-pocket predicate is near-saturated for all three co-folding methods and
  cannot separate them; only the continuous RMSD does. (iii) Boltz-2 pIC₅₀ as a *pose* discriminator
  sits at AUROC 54.52 and AF3 L-pLDDT on D4 at **46.42, below the 50 random floor** (Fig 3a, p10;
  Fig 5b, p14) — at or under chance, not saturated but uninformative. Figure-level defects (the
  duplicated Fig 4 panel) are recorded in `hides`, per the v3 rule, not here.
- **directional_control**: **NONE — the method cannot be instructed which receptor state to produce
  in this study.** The only handle exercised is the **ligand** (each of the 557 SMILES is a separate
  co-folding input), which is the whole premise: "we investigated the potential for co-folding
  methods to identify alternative conformations of the protein that are stabilized by ligand
  binding. This application is a potentially large differentiator relative to virtual screening,
  which generally uses a fixed structure" (p6). That handle **failed**: the ligand did not steer the
  receptor into the twisted or open state in the great majority of cases. No seed sweep, no MSA
  depth handle, no template bias, no partner/nanobody, no state-annotated input. Tagged
  `ligand-driven`.
- **anti_memorization_design**: **YES, and it is the paper's strongest feature. n = 557
  ligand–Mac1 complexes, none previously disclosed, all determined after the models' training
  cutoffs.** Cutoff definition, verbatim from Methods p17: "Tanimoto coefficients (TC) were used to
  identify, for each test ligand, the most similar compound present in the training corpus (Chai-1
  entries deposited before **1 December 2021** and AlphaFold3 entries before **30 September 2021**).
  The training date cutoff for Boltz-2 is **1 June 2023** (STable 6)." Results text p3 gives the
  same two anchors slightly differently: "prior to the training cutoffs for the co-folding methods
  (e.g. **2021-09-30** for AF3, **2023-06-30** for Boltz-2)" — the Boltz-2 date is quoted as 1 June
  2023 in Methods and 30 June 2023 in Results; see `unresolved`. The cutoffs are the **models'
  published PDB cutoffs**, not a split the authors chose. Per-model training PDB accession lists are
  in STable 6, "PDB accessions by cutoff date" (p21) — **not held by the corpus**.
  Second design layer: **per-ligand nearest-training-neighbour similarity** was computed for every
  one of the 557 by two metrics (ECFP4 Tanimoto and RDKit `rdFMCS` MCS%), against each model's own
  training corpus (p17, Fig 1d p5, SFig 8 p29). Result: trimodal Tc with "two larger distributions
  centered around 0.35 (indicating scaffold hops) and 0.2 (indicating low similarity to any ligand)"
  and MCS "centered around ~60%" (p3). **Caveat the authors state:** the *protein* is heavily
  represented in training and ~326 ligand complexes from the same campaign are public (p3, p15) — so
  this is a **ligand-level, not target-level** holdout.
- **anti_memorization_control**: **RUN AND ANALYSED — not merely a held-out set that exists.**
  Three distinct control analyses:
  (1) **Similarity–accuracy correlation, n = 550.** "We measured the correlation between AF3 ligand
  RMSD, and either the Tc (ECFP4) or %MCS of the most similar ligand within the training set,
  finding no meaningful signal (Fig. 2c)" (p6). Pearson **r = 0.065** (vs Tc) and **r = −0.078**
  (vs MCS%) (Fig 2c panels, p7).
  (2) **Binned stratification by similarity, all four methods and all scores** — SFig 5 (p26): RMSD
  and score compared across Tc bins (<0.2, 0.2–0.4, 0.4–0.6, >0.6) and MCS% bins (<40, 40–60,
  60–80, >80). "the performance of co-folding and docking scores did not show a strong dependence on
  novelty relative to the training set" (p8).
  (3) **Later-cutoff natural experiment.** Boltz-2's cutoff is ~20 months later than AF3's and it
  therefore saw *more* Mac1 material, yet it performed **worse** (52.1% vs 72.2%): "This result was
  surprising because the later training cut-off date for Boltz-2 meant that it could potentially
  benefit from additional Mac1 ligand-bound structures" (p4); re-used as a memorisation rebuttal on
  p15. This is the cleanest single piece of anti-memorisation evidence in the paper.
  **Powered**: n = 550–557, far above the ~10 threshold; not `unpowered`. **The one arm that IS
  unpowered is the conformational-state arm** (n = 19 twisted, n = 20 open, AF3 only).
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | DOCK3.7 physics-based docking, same 557 ligands, receptor PDB 5SQW | that the pose task is trivially easy / that any method would score 70%; gives a non-ML floor of 40.9% | p4, p7, p17 |
  | RDKit sanitisation + substructure atom-mapping gate before any RMSD | RMSD inflation from bad valences, wrong bond orders or mismatched atom correspondence | p4, p19 |
  | Ligand centre-of-mass < 2.5 Å in-pocket pre-filter | that a low RMSD is being reported for a ligand placed outside the orthosteric site | p4, p19 |
  | Success denominators fixed at 557 for all methods (not at the 544–551 that passed sanitisation) | a method being rewarded for failing to produce a parseable pose | Fig 2a table, p7 |
  | Similarity-to-training correlation, AF3 RMSD vs Tc and vs MCS% (r = 0.065, −0.078) | memorisation of chemically similar training ligands driving pose accuracy | p6, Fig 2c p7 |
  | Similarity-binned RMSD and score comparison, all four methods (SFig 5) | the same, non-parametrically and per method | p8, p26 |
  | Boltz-2 (cutoff 2023) vs AF3/Chai-1 (cutoff 2021) as a later-data arm | that more in-domain training data buys accuracy — it did not | p4, p15 |
  | False-positive rate for conformational-state calls among normal-conformation complexes (twisted 8/538 = 1.5%; open 0/537 = 0%) | a "correct" twisted-state call being an artefact of a high base rate of predicting twisted | Fig 2b table, p7 |
  | Hydrogen-bond confusion matrices with Matthews correlation coefficients at four hotspot residues (D22, I23, F156, D157) | a low ligand RMSD masking systematically wrong interactions | p6, SFig 3b p24 |
  | Cross-method error-correlation scatter, AF3-vs-other RMSD against AF3-vs-experiment RMSD (SFig 6, SFig 7) | co-folding and docking errors being independent (they are partly correlated: r = 0.72 AF3–Chai-1, 0.52 AF3–Boltz-2, 0.45 AF3–DOCK) | p8–9, p27–28 |
  | "Predict the dataset mean pIC₅₀ for every compound" baseline (MAE 0.93 kcal / 0.68 pIC on Mac1; 1.84, 1.07, 1.46 kcal on σ₂, AmpC, D4) | an affinity MAE looking good when the dynamic range is narrow | p9, p11, p12–13 |
  | Two explicit assumptions for scoring false positives in the MAE (optimistic 2× threshold; random Kᵢ between threshold and 100 mM) | an affinity MAE computed on true positives only, which is the flattering case | p12–13, SFig 10 p31 |
  | Kolmogorov–Smirnov test on active vs inactive score distributions, all three screens | eyeballing violin separation | p14, p19 |
  | Semi-logarithmic ROC (early enrichment) alongside linear ROC | a good global AUROC hiding no early enrichment | p10, p13, SFig 11 p32 |
  | pProp rolling-window hit-rate curves with 95% Wilson intervals (window 100 for AmpC/σ₂, 50 for D4) | rank-threshold cherry-picking in the hit-triage claim | p13, p19, SFig 12 p33 |
  | Friedman global test + Conover post-hoc with Bonferroni/Holm correction across the three scoring methods | claiming a method difference from a raw correlation gap | p9, p11, p19 |
  | Chemotype diversity quantification (pairwise Tc, MCS%, BFC cluster heads) for all four datasets | the 557 being one scaffold in disguise — it is four MCS clusters, which the authors concede | p3–4, p15, SFig 2 p23 |
  - **NOT run:** no apo arm; no decoy/non-binder arm on Mac1 (the pose set is all true ligands); no
    scrambled-sequence or adversarial-mutant arm; no per-seed or multi-sample variance arm; no
    template-off vs template-on ablation; no Chai-1 or Boltz-2 conformational-state arm.
- **confidence_as_discriminator**: **YES, and the use was validated against ground truth — this is a
  properly done instance of the pattern, not a bare assertion.** Metrics: AF3 **L-pLDDT** (arithmetic
  mean of pLDDT over ligand atoms), AF3 L-PAE and mPAE, Chai-1 **ipTM**, Boltz-2 **Ligand ipTM** and
  Boltz-2 **pIC₅₀** (p18 defines the ligand-centric aggregations). Validation: ROC against the
  RMSD < 2 Å ground-truth label, "True Positives (good score, RMSD < 2Å) versus False Positives
  (good score, RMSD > 2Å)" (p8), giving AUROC 75.72 (AF3 L-pLDDT), 73.49 (Boltz-2 Ligand ipTM),
  72.65 (Chai-1 ipTM), 67.07 (DOCK3.7 energy), 54.52 (Boltz-2 pIC₅₀) (Fig 3a, p10), plus direct
  score-vs-RMSD scatters (SFig 4, p25). Verdict quoted, p8: "This indicates that the internal model
  confidence has predictive power". **Explicit negative half:** confidence was **not** validated as
  a discriminator of *conformational* correctness, and it **fails** as a binder/non-binder
  discriminator — AF3 L-pLDDT AUROC 56.10 (σ₂), 46.42 (D4), 60.51 (AmpC) (Fig 5, p14), i.e. at or
  below chance on a GPCR. Abstract, p1: "AF3 ligand pose confidence values did not separate true
  ligands from high-scoring false-positives as effectively as docking scores or Boltz-2 affinity
  predictions did." Tagged `confidence-as-discriminator`.

## D. Claims

- **central_conclusion**: On a strict post-training-cutoff, never-deposited set of 557 Mac1–ligand
  crystal structures, all three co-folding methods placed the majority of ligands within 2 Å of the
  crystal pose (AF3 72.2%, Chai-1 66.6%, Boltz-2 52.1%) and beat DOCK3.7 (40.9%), with accuracy
  showing essentially no dependence on chemical similarity to the training set — so this is real
  generalisation on ligand placement, not memorisation. But the same predictions **failed** to
  reproduce the receptor's ligand-stabilised conformational changes (AF3: 4/19 twisted, 0/20 open),
  and on the different task of separating true binders from high-ranking docking false positives
  across three unrelated targets, co-folding was no better than, and often worse than, docking
  running four orders of magnitude faster. The authors read this as complementarity: docking for
  discovery, co-folding for pose and within-series ranking during optimisation.
- **necessity_claims**: The paper makes **almost no necessity claims of its own** — a deliberate and
  unusually careful piece of writing. The only "needed"-form sentence in the body is a
  characterisation of *other people's* results, p2, verbatim:
  > "These results highlight pervasive memorization and hallucination in current co-folding methods
  > and suggest that alternative computational approaches are needed to quantify the physical basis
  > of the protein-ligand interactions."

  Two further load-bearing "is required for the field" style statements, both verbatim:
  > "However, partly because of the lack of widely adopted community prospective tests, akin to CASP
  > (Gathiaka et al. 2016)... co-folding methods have not yet been subject to the rigorous,
  > large-scale testing that helped establish the utility, domain of applicability, and ultimately
  > optimization of the early protein structure-prediction methods." (p2)

  > "Where they have complementary strengths is in predicting the accurate geometries of ligands,
  > once known, and their ranking within a series, both of which are crucial for affinity maturation
  > once a series is discovered and with both of which docking has historically struggled." (p15)

  No statement of the form "X cannot be done" or "X is impossible" appears. `grep` over pp. 1–20 for
  *necessar/essential/require/cannot/not possible/must be/need* returns only the p2 sentence above
  and one incidental methodological use ("the RDkit-based sanitization pipeline necessary for RMSD
  comparisons", p4).
- **novelty_claims**: The paper's novelty claim is **scale and holdout cleanliness**, and the
  authors **explicitly decline a priority claim**. Verbatim:
  > Title, p1: "Large scale prospective evaluation of co-folding across 557 Mac1-ligand complexes
  > and three virtual screens"

  > p1 (abstract): "While deep learning co-folding methods can help address these challenges, their
  > evaluation has been hampered by the difficulties in assessing independence from training data
  > and insufficiently large test sets. Here we test the ability of co-folding methods to predict
  > the structures of 557 ligands bound to the SARS-CoV-2 NSP3 macrodomain (Mac1) that were
  > determined after the training cut-off dates."

  > p3: "From our internal dataset, we identified 557 ligands where we determined X-ray structures
  > that have not been disclosed previously (Fig. 1a, STable 1)."

  > p3: "This dataset represents the scale and depth typical of the early phase of industrial
  > structure-based drug design campaigns."

  > p15: "Against a benchmark of 557 topologically diverse Mac1 ligand-bound structures, determined
  > to true atomic resolution and largely dissimilar to structures already in the PDB, each of the
  > co-folding methods predicted ligand poses and interactions with high-fidelity to the
  > experimental structure."

  **Priority explicitly ceded**, p3 and p16, verbatim:
  > "Contemporaneous work has highlighted the importance of using AF3 in the same experimental
  > datasets from ultra-large library docking campaigns (Menon et al. 2025)." (p3)

  > "These observations are supported by a fascinating study on some of the same ligand sets as
  > investigated here, using AlphaFold3, reaching similar conclusions (Menon et al. 2025)." (p16)

  No "first", "novel" or "unprecedented" claim about the method or the analysis appears.
- **stated_limits**: The Discussion carries a dedicated caveats paragraph (p15, opening "Several
  caveats merit airing"), and there is a second concession mid-Results (p9). Verbatim, in order:
  1. **Single target — the authors flag it themselves, twice.** p9: "Still, the Mac1 set, as large
     as it is, represents only a single system with ligands that share a limited set of
     pharmacophores. We wanted to broaden testing to more targets and more diverse ligands, such as
     those encountered in virtual screening hit lists with their focus on new chemotype discovery."
     And p15, for the second arm: "Even though the prospective docking hit lists included thousands
     of diverse molecules, they still represent only three targets, and so offer a limited view of
     molecular recognition."
  2. **Chemical homogeneity + protein already in training, may inflate the headline.** p15: "The
     Mac1 benchmark, while diverse by ECPP4 Tc, is nevertheless dominated by four groups when
     clustered by MCS and benefits from a large training set of fragment molecules bound to the
     protein in the training set (Schuller et al. 2021). This may inflate apparent pose recovery
     rates, although Boltz-2 predicted poses were poorly recapitulated even with its much later
     training cutoff dates."
  3. **Right pose for the wrong reasons — non-physical.** p15: "Unexpectedly, even when the
     co-folding methods got important conformations of the enzyme binding site wrong, the ligands
     were still often posed correctly, speaking to a non-physical aspect of the ML methods that
     others have also described (Masters et al. 2025; Škrinjar et al. 2025)." Same point, p6: "This
     result suggests that co-folding reliably recapitulates dominant ligand-binding interactions
     even in the absence of accurate protein conformational modeling, providing further support to
     the idea that they are learning specific interaction patterns rather than a deeper
     physics-based representation".
  4. **The hit-list comparison is stacked in docking's favour.** p15: "Finally, comparing co-folding
     to docking based on hit-lists themselves selected by docking is arguably unfair to co-folding.
     Counter-balancing this is the inclusion, in each of the three hit lists, of molecules that had
     mediocre and poor docking scores intentionally selected to test the correlation between docking
     score and hit-rate." Same caveat p13: "An important caveat is that the hit-lists were composed
     of molecules prioritized by docking in the first place, giving it an advantage on these
     particular sets."
  5. **Crystal contacts may create the conformational changes being scored.** p6: "This result
     suggests that there is only a limited ability to predict conformational adaptations, which
     admittedly may be, at least in part, stabilized by crystal contacts." Also p8, for the
     mispredicted exemplar: "Although this group packs against a crystal contact".
  6. **The virtual-screen sets are structurally thinner than Mac1.** p12: "For validation, there are
     more measured IC50 values, but they are admittedly not as deeply supported by structural
     information as the Mac1 set."
  7. **Boltz-2's affinity MAE on true positives only is the flattering case.** p12: "however, it is
     restricted only to true positives and the performance could be much worse if the false
     positives were accounted for in the comparison."
  8. **Incomplete assay coverage of the 557.** p3: "Because these ligands were synthesized during an
     active campaign and many did not meet evolving thresholds for single point % inhibition, only
     202 have fully measured dose response IC50 estimations"; and the potency distribution "is
     skewed towards weaker affinities as more potent molecules were progressed and disclosed in
     papers describing in vivo-active lead molecules" — i.e. the affinity subset is **truncated at
     the potent end by design**.
- **stance**: **`precedent` on findings + `contrast` on scope — provisional, the user's call.**
  - *precedent*: the cleanest strict temporal holdout available for co-folding pose prediction (557
    never-deposited post-cutoff complexes on one target), with the anti-memorisation control
    actually run, the null result on receptor conformational change reported honestly, and a
    physics baseline throughout. If our manuscript concedes what co-folding gets right before
    arguing about what it misses, this is the paper to concede it with — and its conformational
    result (4/19, 0/20) is directly on our side of the argument.
  - *contrast*: one protein for the headline number; the receptor barely moves across 557 ligands so
    the benchmark cannot test conformational selection at all; sampling protocol (seeds, samples per
    ligand, template flag) undisclosed so top-1 vs best-of-N is unresolvable; the affinity headline
    is calibrated in-sample; the second arm's hit/non-hit labels were re-drawn by the authors.

## E. Quantitative comparators

- **metrics_reported**:

  **Arm 1 — Mac1 ligand pose prediction (1 target, 557 complexes).** Success = heavy-atom L-RMSD to
  the crystal pose < 2 Å after all-Cα superposition (p4, p19). **Denominator is 557 for every method
  in the Fig 2a table**, i.e. molecules that failed RDKit sanitisation are counted as failures — the
  conservative choice.

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | AF3 pose success, L-RMSD < 2 Å | **72.2% (402/557)** | % of ligands | crystal pose, n = 557 | Fig 2a table, p7 (read from render); text says "~70%", p4 |
  | Chai-1 pose success, L-RMSD < 2 Å | **66.6% (371/557)** | % of ligands | crystal pose, n = 557 | Fig 2a table, p7 (read from render); text "~70%", p4 |
  | Boltz-2 pose success, L-RMSD < 2 Å | **52.1% (290/557)** | % of ligands | crystal pose, n = 557 | Fig 2a table, p7; text "52%", p4 |
  | DOCK3.7 pose success, L-RMSD < 2 Å | **40.9% (228/557)** | % of ligands | crystal pose, n = 557 | Fig 2a table, p7; text "41%", p4 |
  | AF3 in-pocket, COM < 2.5 Å | 94% (519/550) | % of sanitised poses | crystal ligand COM, n = 550 | p4; Fig 2a table p7 |
  | Chai-1 in-pocket, COM < 2.5 Å | 92% (509/551) | % of sanitised poses | crystal ligand COM, n = 551 | p4; Fig 2a table p7 |
  | Boltz-2 in-pocket, COM < 2.5 Å | 93% (511/548) | % of sanitised poses | crystal ligand COM, n = 548 | p4; Fig 2a table p7 |
  | DOCK3.7 in-pocket, COM < 2.5 Å | 83% (450/544) | % of sanitised poses | crystal ligand COM, n = 544 | p4; Fig 2a table p7 |
  | Molecules failing RDKit sanitisation | ~1.5% of 557 | % | — | p4 |
  | RMSD distribution modes (AF3, Chai-1) | ~1, 2, 4 (trimodal) | Å | crystal pose | p4; Fig 2a density, p7 |
  | Global receptor Cα RMSD, prediction vs crystal | 0.1 – 0.4 (range) | Å | 557 crystal structures | p6 (STable 3, not held) |
  | AF3 twisted-state (F156 flip) recovery | **4/19 = 21%** | fraction | crystal alternate conformations | Fig 2b table, p7; text p6 |
  | AF3 open-state (A129/G130, ~8 Å loop) recovery | **0/20 = 0%** | fraction | crystal alternate conformations | Fig 2b table, p7; text p6 |
  | AF3 twisted-state false positives | 8/538 = 1.5% | fraction | ground-state complexes | Fig 2b table, p7; text p6 ("8 false positive twisted states") |
  | AF3 open-state false positives | 0/537 = 0% | fraction | ground-state complexes | Fig 2b table, p7 |
  | AF3 L-RMSD vs Tc to nearest training ligand | **r = 0.065** | Pearson r | n ≈ 550 | Fig 2c, p7; "no meaningful signal", p6 |
  | AF3 L-RMSD vs MCS% to nearest training ligand | **r = −0.078** | Pearson r | n ≈ 550 | Fig 2c, p7 |

  **Arm 1b — confidence/energy as a discriminator of pose accuracy** (ROC, positive class =
  L-RMSD < 2 Å):

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | AF3 L-pLDDT | AUROC **75.72**; norm_logAUC 15.52 | % | RMSD < 2 Å label, n ≈ 550 | Fig 3a, p10; text "AUC=75.7", p8 |
  | Boltz-2 Ligand ipTM | AUROC **73.49**; norm_logAUC **20.50** (best early enrichment, "20.5% above random") | % | RMSD < 2 Å label, n ≈ 548 | Fig 3a, p10; text p8 |
  | Chai-1 ipTM | AUROC **72.65**; norm_logAUC 14.91 | % | RMSD < 2 Å label, n ≈ 551 | Fig 3a, p10; text "AUC=72.7", p8 |
  | DOCK3.7 energy | AUROC **67.07**; norm_logAUC 13.94 | % | RMSD < 2 Å label, n ≈ 544 | Fig 3a, p10; text "AUC=67.1", p8 |
  | Boltz-2 pIC₅₀ | AUROC **54.52**; norm_logAUC 19.16 | % | RMSD < 2 Å label | Fig 3a, p10; text "AUC=54.5", p8 |
  | DOCK3.7 energy vs L-RMSD | r = 0.35, p < 0.001 | Pearson r | n ≈ 544 | p8 |
  | Boltz-2 pIC₅₀ vs L-RMSD | r = −0.03, p = 0.49 (null) | Pearson r | n ≈ 548 | p8 |
  | AF3 vs Chai-1 pose agreement | r = 0.72 | Pearson r | RMSD-to-experiment, n = 557 | p9, SFig 7 |
  | AF3 vs Boltz-2 pose agreement | r = 0.52 | Pearson r | same | p9 |
  | AF3 vs DOCK3.7 pose agreement | r = 0.45 | Pearson r | same | p9 |

  **Arm 1c — affinity, Mac1 subset with full dose–response (n = 202):**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Boltz-2 pIC₅₀ vs measured pIC₅₀ | **r = 0.600** | Pearson r | HTRF IC₅₀, n = 202 | Fig 4a, p11; text "r = 0.6", p9 |
  | Boltz-2 MAE, **uncalibrated** | 1.190 pIC (~1.6 kcal), "most affinities predicted as too potent" | pIC / kcal mol⁻¹ | measured pIC₅₀, n = 202 | Fig 4a p11; p9 |
  | Boltz-2 MAE, **after in-sample linear correction** | **0.538 pIC (~0.7 kcal)** — *calibration fitted on this same set; not held out* | pIC / kcal mol⁻¹ | measured pIC₅₀, n = 202 | Fig 4a p11; p9 |
  | Baseline: predict the dataset mean pIC₅₀ (4.95) for every compound | 0.68 pIC (0.93 kcal) | pIC / kcal mol⁻¹ | measured pIC₅₀, n = 202 | Fig 4 caption p11; p9 |
  | AF3 L-pLDDT vs measured pIC₅₀ | r = 0.314; MAE 0.639 pIC | Pearson r / pIC | HTRF IC₅₀, n = 202 | Fig 4a, p11; p9 |
  | DOCK3.7 energy vs measured pIC₅₀ | r = −0.225; MAE 0.680 pIC | Pearson r / pIC | HTRF IC₅₀, n = 202 | Fig 4a, p11; p9 |
  | Friedman global test across the three scores | χ² = 16.68, p = 2.39 × 10⁻⁴ | — | MAE, n = 202 | Fig 4a, p11 |
  | Conover post-hoc, Boltz-2 pIC₅₀ vs DOCK score | **p = 0.0057** (only significant pair) | Bonferroni-corrected p | MAE | Fig 4a p11; p9 |
  | Conover post-hoc, AF3 L-pLDDT vs Boltz-2 pIC₅₀ | p = 0.089 (n.s.) | Bonferroni-corrected p | MAE | Fig 4a, p11 |
  | Conover post-hoc, AF3 L-pLDDT vs DOCK score | p = 1.000 (n.s.) | Bonferroni-corrected p | MAE | Fig 4a, p11 |
  | AF3 L-RMSD vs measured potency | r = −0.297 | Pearson r | n = 202 | p9 (**cited as Fig 4b, which is not printed — see `hides`**) |
  | Boltz-2 pIC₅₀ vs pose accuracy | r = −0.387 | Pearson r | n = 202 | p9 (same missing panel) |
  | DOCK3.7 accuracy vs potency | "no correlation" | — | n = 202 | p9 (same missing panel) |

  **Arm 2 — virtual-screen hit triage (3 targets; SEPARATE ARM, do not pool with Arm 1).**
  AF3 and Boltz-2 only; Chai-1 not run. Positive class = experimentally confirmed active under the
  authors' **re-drawn** 25%-displacement threshold (p18).

  | target / library | n tested | n active | n inactive | metric | value | page |
  |---|---|---|---|---|---|---|
  | **σ₂ receptor**, 490 M docked (Alon 2021) | 506 | 201 (apparent Kᵢ 2.5 nM – 1.5 µM) | 305 | Boltz-2 pIC₅₀ AUROC | **83.78** (text 83.8) | Fig 5a p14; p12 |
  | σ₂ | — | — | — | DOCK3.7 AUROC | **78.77** (text 78.8) | Fig 5a p14; p12 |
  | σ₂ | — | — | — | AF3 L-pLDDT AUROC | **56.10** (text 56.1) | Fig 5a p14; p12 |
  | σ₂ | — | — | — | KS statistic: Boltz-2 0.55*, DOCK 0.49*, AF3 0.16 (p = 0.004) | — | Fig 5a, p14 |
  | σ₂ | — | — | — | median active vs inactive: DOCK −55.0 vs −42.5 kcal/mol; AF3 75.9 vs 74.1; Boltz-2 6.70 vs 5.38 | — | p12 |
  | σ₂, actives only | — | 201 | — | r vs pKᵢ: Boltz-2 **0.486**, AF3 0.183, DOCK −0.211 | Pearson r | p12 |
  | σ₂, actives only | — | 201 | — | Boltz-2 MAE 0.7 kcal → **0.54 after in-sample calibration** | kcal mol⁻¹ | p12, SFig 9 |
  | σ₂, actives + inactives, optimistic (FP assigned IC₅₀ = 4 µM) | 506 | — | — | MAE 0.92 kcal (0.56 calibrated) | kcal mol⁻¹ | p13 |
  | σ₂, actives + inactives, random FP assignment | 506 | — | — | MAE **1.66 kcal (1.55 calibrated)** vs dataset-mean baseline **1.84 kcal** | kcal mol⁻¹ | p13, SFig 10 |
  | **Dopamine D4**, 138 M docked (Lyu 2019) | 541 (Methods says 549 prioritised, p18) | 205 (apparent Kᵢ 3.1 nM – 7.8 µM) | 336 | DOCK3.7 AUROC | **70.54** (text "~71") | Fig 5b p14; p13 |
  | D4 | — | — | — | Boltz-2 pIC₅₀ AUROC | **71.34** (text "~71") | Fig 5b, p14 |
  | D4 | — | — | — | AF3 L-pLDDT AUROC | **46.42** — "slightly worse than random" | Fig 5b p14; p13 |
  | D4 | — | — | — | KS: Boltz-2 0.36*, DOCK 0.37*, AF3 0.11 (p = 0.07, n.s.) | — | Fig 5b, p14 |
  | D4 | — | — | — | median active vs inactive: DOCK −63.9 vs −52.0 kcal/mol; Boltz-2 6.15 vs 5.72; AF3 65.4 vs 66.2 (**inverted**) | — | p13 |
  | D4, actives only | — | 205 | — | r vs pKᵢ: DOCK −0.247, Boltz-2 0.284, AF3 **−0.109** ("notably a positive correlation is expected") | Pearson r | p13 |
  | D4, actives only | — | 205 | — | Boltz-2 MAE 0.89 kcal (0.55 calibrated); with FP optimistic 1.15 (0.57); random 1.97 (1.4); baseline **1.46** | kcal mol⁻¹ | p13, SFig 10 |
  | **AmpC β-lactamase**, 1.7 B docked, top 1% tested (Liu 2025) | 1,293 | 247 (apparent Kᵢ < 400 µM) | 1,046 | DOCK3.7 AUROC | **76.47** (text 76.5) | Fig 5c p14; p12 |
  | AmpC | — | — | — | Boltz-2 pIC₅₀ AUROC | **68.13** (text 68.1) | Fig 5c, p14 |
  | AmpC | — | — | — | AF3 L-pLDDT AUROC | **60.51** (text 60.5) | Fig 5c, p14 |
  | AmpC | — | — | — | KS: DOCK 0.41*, Boltz-2 0.28*, AF3 0.17* | — | Fig 5c, p14 |
  | AmpC | — | — | — | median active vs inactive: DOCK −85.6 vs −82.8 kcal/mol; Boltz-2 5.16 vs 4.87; AF3 76.6 vs 72.0 | — | p12 |
  | AmpC, actives only | — | 247 | — | Boltz-2 MAE 1.81 kcal → 0.42 calibrated; with FP optimistic 2.33 (0.32); random 3.29 (1.04); baseline **1.07** | kcal mol⁻¹ | p12–13, SFig 10 |
  | All three screens, early enrichment | — | — | — | "no clear evidence of early ligand enrichment with co-folding methods over docking methods from semi-logarithmic ROC plots" | — | p13, SFig 11 |
  | All three screens, hit-rate plateau | — | — | — | DOCK3.7 and Boltz-2 plateau at **40–50%** hit rate for top-ranked compounds; AF3 L-pLDDT enriches only on AmpC, "no enrichment signal for σ₂ and D4" | % hit rate | p13, SFig 12 |

  **Chemical-diversity comparators** (SFig 2 table, p23) — cluster heads by Tc > 0.35 / MCS > 35%:
  σ₂ 348 / 46 (n = 506); D4 410 / 47 (n = 541); AmpC 500 / 62 (n = 1,293); **Mac1 30 / 4 (n = 557)**.
  Mean pairwise ECFP4 Tc: Mac1 0.2–0.4 (p3); the three screens 0.12–0.15 (p12). Similarity to
  training set: Mac1 Tc ~0.36, MCS ~60.1%; the three screens Tc 0.11–0.19, MCS 33–42% (p12). The
  Mac1 set is **markedly more homogeneous and markedly closer to training data** than the screens —
  the numbers that carry the paper's own inflation caveat.

  **Top-1 vs best-of-N — stated explicitly:** the paper reports **exactly one pose per ligand per
  method** and one score per pose, and **never states how many samples/seeds/diffusion runs were
  generated or how the reported one was selected** (Methods, p18, gives no sampling settings).
  **No headline number is described as oracle-selected**, and there is no "best of N" or
  "top-ranked model" language anywhere in the paper. The most likely reading is each tool's default
  top-ranked output (top-1), but the paper does not say so, so it cannot be asserted. Consequence
  for our use: the 72.2% / 66.6% / 52.1% figures should be quoted as "one pose per ligand,
  selection protocol unstated" rather than as confirmed top-1. Recorded in `unresolved`.
- **n_predictions**:
  - **Targets:** 1 (Mac1, pose arm) + 3 (σ₂, D4, AmpC, hit-triage arm) = 4.
  - **Mac1 ligands attempted:** 557 per method × 3 co-folding methods + DOCK3.7. Poses surviving
    sanitisation: AF3 550, Chai-1 551, Boltz-2 548, DOCK3.7 544 (Fig 2a table, p7). Poses passing
    the COM filter: 519 / 509 / 511 / 450 (p4).
  - **Mac1 affinity subset:** 202 with full 8-point dose–response HTRF IC₅₀ (p3, Fig 1b p5).
  - **Samples per target per method (co-folding): NOT REPORTED.** No seeds, no diffusion sample
    count, no recycles anywhere in the paper.
  - **Samples per molecule (DOCK3.7): reported and large** — "each molecule was sampled in about
    2,719 orientations and, on average, 105 conformations... Overall, over 290 million complexes
    were sampled and scored" (p17), for the 557-molecule Mac1 campaign.
  - **Virtual-screen molecules scored:** σ₂ 506 + D4 541 + AmpC 1,293 = **2,340**, each by AF3 and
    Boltz-2 (and already by DOCK3.7 in the source papers) — the paper never states this total; it is
    arithmetic from p12/p18. Underlying docked libraries: 490 M (σ₂), 138 M (D4), 1.7 B (AmpC).
  - **Grand total co-folding runs (derived, not stated):** 557 × 3 + 2,340 × 2 = 6,351.
- **comparable_to_ours**: *(left empty for the user)*
- **si_in_scope**: **PARTIAL.** Supplementary **Figures S1–S13 are present in the PDF** (pp. 22–34)
  with full captions, and SFig 2 carries a numeric table (p23). Supplementary **Tables 1–6 are NOT
  held** — p21 lists only their titles. `SI TABLES NOT HELD`, and this matters: **STable 3** holds
  the per-ligand co-folded and docked poses and scores plus the per-structure Cα RMSDs, **STable 4**
  the per-residue hydrogen-bond comparison, **STable 6** the per-model PDB accession lists that
  define the training cutoffs, and **STable 1** (X-ray data statistics) is under a deliberate
  embargo (p21). Every per-ligand number and the exact composition of each model's Mac1 training
  exposure therefore sits outside the corpus.

## F. Figures

**License applies to every row: CC-BY 4.0, no ND clause — redrawing and modification are both
permitted with attribution.** Stated in the banner on every page, e.g. p1: "It is made available
under a CC-BY 4.0 International license."

Rows for Figures 1–5 were read from 150 dpi renders of pp. 5, 7, 10, 11 and 14. Rows for
Supplementary Figures S1–S13 are **caption-derived only** (pages not rendered) and are flagged.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 5 | All 557 ligands superposed in the Mac1 pocket, with a zoom onto the four hotspot residues (D22, I23, F156, D157) | structure render | `RENDER \| facet: none (1) \| views: 2 (whole-protein surface; zoomed active site) \| overlay: 557 crystal ligands on 1 reference receptor \| axis: none` | 2 views of one system; an arrow labelled "HTRF assay" links it to panel b | | CC-BY 4.0, no ND (p1) |
| 1B | 5 | Potency distribution of the 202 ligands with full dose–response | bar | `PLOT \| facet: none (1) \| vary: IC50 bin (5: 0–1, 1–10, 10–100, 100–500, >500 µM) \| series: none (1) \| measure: number of compounds \| mark: bar \| n: ~25/57/89/16/16 per bar (read from render), 202 per panel` | 1 | Bars over a distribution: the underlying IC₅₀ values are binned into 5 coarse bins, so the sub-µM tail is one bar. Also the 355 ligands **without** dose–response are simply absent, and the caption does not say the set is truncated at the potent end (that is only in the p3 text) | CC-BY 4.0, no ND (p1) |
| 1C | 5 | PCA of the 557 in chemical-similarity space, once by MCS% and once by Tc, with 4 MCS clusters circled | scatter | `PLOT \| facet: similarity metric (2: MCS%, ECFP4 Tc) \| vary: PC1 (continuous, 47.0% / 37.8% variance) \| series: exemplar compound (4 highlighted vs the rest) \| measure: PC2 (21.0% / 16.0% variance) \| mark: point \| n: 1 per mark, 557 per panel` | 2, varying by similarity metric | Cluster ellipses are drawn only on the MCS panel; the Tc panel shows visually more structure than 4 clusters and is left unannotated, which understates the disagreement between the two metrics | CC-BY 4.0, no ND (p1) |
| 1D | 5 | Each test ligand's nearest training-set neighbour: MCS% against Tc, with marginal histograms | scatter | `PLOT \| facet: none (1) \| vary: Tanimoto to nearest training ligand, ~0.15–0.95 (continuous) \| series: exemplar (3 highlighted: MCS 33.3%/Tc 0.19, MCS 70.0%/Tc 0.33, MCS 100%/Tc 0.92) \| measure: MCS% to nearest training ligand \| mark: point \| n: 1 per mark, 557 per panel` | 1, plus marginal histograms on both axes | The panel makes visible — but the text never says — that at least one of the 557 has an **MCS of 100% and Tc 0.92** to a training ligand, i.e. a near-identical compound was in training. The holdout is by *deposition*, not by chemistry | CC-BY 4.0, no ND (p1) |
| 1D-inset | 5 | 2D structures of three test molecules beside their nearest training molecule, by MCS and by Tc | schematic | `SCHEMATIC \| three test ligands paired with their nearest training-set ligand, annotated with MCS% and Tc \| no data` | 3 stacked pairs | | CC-BY 4.0, no ND (p1) |
| 2A | 7 | Ligand-RMSD distributions for AF3, Chai-1, Boltz-2 and DOCK3.7, with the success-rate table | line (kernel density) + tabulated counts | `PLOT \| facet: none (1) \| vary: ligand RMSD, 0–10 Å (continuous) \| series: prediction method (4: AF3, Chai-1, Boltz-2, DOCK3.7) \| measure: kernel density \| mark: line \| n: 550 / 551 / 548 / 511-548 poses per series; 557 ligands attempted per panel` | 1 density panel + 1 summary table (4 rows × 4 columns: method, # sanitised, # COM < 2.5 Å, success rate) | The **headline success rates live only in the table image** and are absent from the extracted text (the running text on p4 rounds them to "~70%", "52%", "41%"). The density curves carry no confidence band and no n annotation on the panel itself | CC-BY 4.0, no ND (p1) |
| 2B | 7 | The two experimentally observed alternate Mac1 conformations (twisted F156 backbone; open A129/G130 loop) with AF3's recovery counts | structure render + tabulated counts | `RENDER \| facet: alternate conformation (2: twisted backbone, open state) \| views: 1 \| overlay: 1 crystal alternate conformation (pink) on 1 reference PDB 5SQW (green) \| axis: none` | 2 renders + 1 summary table (3 rows: total alternate conformations, AF3 success rate, false positives among normal conformations) | **The AF3 prediction itself is not shown in either render** — the two colours are crystal-alternate vs 5SQW reference, so the figure that carries the conformational-failure claim contains no predicted structure. The quantitative result exists only as the table | CC-BY 4.0, no ND (p1) |
| 2C | 7 | AF3 pose error against similarity to the nearest training ligand, by Tc and by MCS% | scatter | `PLOT \| facet: similarity metric (2: ECFP4 Tc; MCS%) \| vary: similarity to nearest training ligand (continuous; Tc 0.15–0.95, MCS 30–100%) \| series: exemplar (3 highlighted: Mac-x5015, Mac-x3538, Mac-x4088) \| measure: AF3 L-RMSD (Å) \| mark: point \| n: 1 per mark, ~550 per panel` | 2, varying by similarity metric; marginal histograms on both axes | The y-axis is truncated at ~18 Å while the density plot in 2A runs to 10 Å — different ranges for the same quantity in one figure. Pearson r is printed but no CI and no p-value | CC-BY 4.0, no ND (p1) |
| 2C-inset | 7 | Three low-similarity test ligands, their nearest training molecule, and the co-folded pose overlaid on the crystal pose | structure render + schematic | `RENDER \| facet: exemplar ligand (3: Mac-x5015, Mac-x3538, Mac-x4088) \| views: 1 \| overlay: 1 AF3 pose on 1 crystal pose in the pocket surface \| axis: none` | 3 stacked rows, each 2D structures + 1 pocket render | Exemplars are chosen after the RMSDs are known and are all successes (1.00, 0.37, 0.75 Å); no low-similarity failure is shown alongside | CC-BY 4.0, no ND (p1) |
| 3A | 10 | ROC for five scores discriminating accurate (< 2 Å) from inaccurate poses, linear and semi-log | line | `PLOT \| facet: false-positive-rate scaling (2: linear 0–1; log₁₀ 10⁻³–1) \| vary: false positive rate (continuous) \| series: score (5: AF3 L-pLDDT, Chai-1 ipTM, Boltz-2 Ligand ipTM, DOCK3.7 energies, Boltz-2 pIC50) \| measure: true positive rate \| mark: line \| n: ~544–551 poses per curve, same per panel` | 2, varying by axis scaling; same 5 series in both | No confidence bands on any curve and no n printed on the panel; AUROC and norm_logAUC are given without CIs, so the 75.72 / 73.49 / 72.65 ordering is presented as a ranking without any evidence it is separable | CC-BY 4.0, no ND (p1) |
| 3B | 10 | 2D structures of the universally-failed (mac-x4091) and universally-solved (mac-x3927) exemplars with IC₅₀ and training similarity | schematic | `SCHEMATIC \| two exemplar ligands with IC50, MCS% and Tc to the training set \| no data` | 2 stacked | | CC-BY 4.0, no ND (p1) |
| 3C | 10 | Predicted vs crystal pose for those two ligands, under all four methods, with H-bonds | structure render | `RENDER \| facet: method (4: AF3, Chai-1, Boltz-2, DOCK3.7) × ligand (2: mac-x4091, mac-x3927) \| views: 1 \| overlay: 1 predicted pose on 1 crystal reference pose \| axis: none` | 8 (4 methods × 2 ligands), each annotated with L-RMSD and that method's score | | CC-BY 4.0, no ND (p1) |
| 4A | 11 | Measured pIC₅₀ against AF3 L-pLDDT, DOCK energy and Boltz-2 predicted pIC₅₀, for 202 ligands | scatter | `PLOT \| facet: score (3: AF3 L-pLDDT; DOCK3.7 energy kcal/mol; Boltz-2 predicted pIC50) \| vary: score value (continuous) \| series: regression fit (2 on the Boltz-2 panel: before correction, after linear correction) \| measure: measured pIC50 \| mark: point \| n: 1 per mark, 202 per panel` | 3, varying by score; marginal histograms on both axes; Friedman/Conover statistics printed above | **The panel labelled "a)" is printed TWICE and panel b) is missing entirely.** The caption and the p9 text both describe a panel b ("Lower co-folded ligand RMSDs associate with higher affinity, while docked pose RMSDs do not"; r = −0.297 AF3, r = −0.387 Boltz-2, no correlation for DOCK) and the two printed blocks are byte-identical duplicates of panel a. So three cited correlations have **no quantitative panel at all** in this version. Also: the "after correction" MAE of 0.538 is an **in-sample** fit shown as if it were a prediction | CC-BY 4.0, no ND (p1) |
| 5A-C-violin | 14 | Score distributions for confirmed actives vs docking false positives, three scores × three targets | violin (split) | `PLOT \| facet: target (3: σ₂, D4, AmpC) × score (3: Boltz-2 pIC50, AF3 L-pLDDT, \|DOCK3.7 energy\|) \| vary: none (single category per panel) \| series: hit class (2: active hits, inactive hits) \| measure: score value \| mark: violin \| n: σ₂ 201 active / 305 inactive; D4 205 / 336; AmpC 247 / 1,046` | 9 violin panels (3 targets × 3 scores), each with its KS statistic | Each violin's y-axis is scaled independently per panel, so the AF3 column (a 30-point pLDDT range) looks as separated as the DOCK column (a 60 kcal/mol range) until the AUROC is read. Medians are drawn as thin lines with no IQR box and no CI | CC-BY 4.0, no ND (p1) |
| 5A-C-roc | 14 | ROC for the same three scores on each target | line | `PLOT \| facet: target (3: σ₂, D4, AmpC) \| vary: % decoys found, 0–100 (continuous) \| series: score (3: AF3 L-pLDDT, DOCK3.7 energies, Boltz-2 pIC50) \| measure: % ligands found \| mark: line \| n: 506 / 541 / 1,293 molecules per panel` | 3, varying by target | No confidence bands; the AF3 D4 curve sits below the diagonal (AUROC 46.42) and this is not annotated on the panel | CC-BY 4.0, no ND (p1) |
| S1A-B | 22 | Pairwise similarity distributions within the Mac1 set, by Tc and by MCS% | histogram (bar) | `PLOT \| facet: similarity metric (2: ECFP4 Tc; MCS%) \| vary: similarity value (continuous) \| series: reference line (2 on the Tc panel: scaffold-hop 0.35, random 0.25) \| measure: count of ligand pairs \| mark: bar \| n: 557×556/2 = 154,846 pairs per panel (derived, not stated)` | 2, varying by metric — **caption-derived, panel not rendered** | | CC-BY 4.0, no ND (p22) |
| S1C-D | 22 | PCA of all PDB-deposited ligands with the Mac1 test compounds overlaid | scatter | `PLOT \| facet: similarity metric (2: ECFP4 Tc; MCS%) \| vary: PC1 (continuous) \| series: ligand source (2: all PDB ligands, Mac1 test compounds) \| measure: PC2 \| mark: point \| n: NOT REPORTED per panel (all PDB ligands); 557 Mac1` | 2 — **caption-derived, panel not rendered** | n for the "all ligands deposited in PDB" background is never given | CC-BY 4.0, no ND (p22) |
| S2 | 23 | PCA chemical-space maps of the three docking hit lists, actives vs false positives, by Tc and MCS%, with a cluster-head summary table | scatter + tabulated counts | `PLOT \| facet: target (3: σ₂, D4, AmpC) × similarity metric (2: Tc, MCS%) \| vary: PC1 (continuous) \| series: hit class (2: docked false positives red, known actives blue) \| measure: PC2 \| mark: point \| n: 506 / 541 / 1,293 per target panel` | 6 scatter panels + 1 summary table (4 targets × 4 columns) — **scatters caption-derived; the table was read from text extraction** | | CC-BY 4.0, no ND (p23) |
| S3A | 24 | Per-residue RMSD densities used to define the twisted and open states | line (density) | `PLOT \| facet: residue / state definition (F156 twisted; A129 + G130 open) \| vary: residue RMSD to PDB 5SQW (continuous) \| series: NOT REPORTED \| measure: density \| mark: line \| n: 557 crystal complexes per panel` | caption-derived, panel not rendered | The 1.5 Å and 3 Å state-defining thresholds are stated in the caption but never justified | CC-BY 4.0, no ND (p24) |
| S3B | 24 | Confusion matrices for AF3-predicted vs crystal hydrogen bonds at four hotspot residues, with MCC | heatmap (2×2 confusion matrices) | `MATRIX \| rows: crystal H-bond present (2: yes, no) \| cols: AF3-predicted H-bond present (2: yes, no) \| value: absolute count of complexes \| facet: residue (4: D22, I23, F156, D157)` | 4 matrices — caption-derived, panel not rendered | | CC-BY 4.0, no ND (p24) |
| S4 | 25 | Pose RMSD against each method's own score, six score/method combinations | scatter | `PLOT \| facet: method × score (6: DOCK energy, Chai-1 ipTM, Boltz-2 pIC50, AF3 L-pLDDT, AF3 L-PAE, AF3 mPAE) \| vary: score value (continuous) \| series: none (1) \| measure: pose RMSD (Å) \| mark: point \| n: 1 per mark, ~544–551 per panel` | 6 — caption-derived, panel not rendered | | CC-BY 4.0, no ND (p25) |
| S5A/S5C | 26 | Pose RMSD by similarity bin, for all four methods | box or violin (mark not stated in caption) | `PLOT \| facet: similarity metric (2: Tc bins <0.2 / 0.2–0.4 / 0.4–0.6 / >0.6; MCS% bins <40 / 40–60 / 60–80 / >80) \| vary: similarity bin (4) \| series: method (4: AF3, Chai-1, Boltz-2, DOCK3.7) \| measure: ligand RMSD (Å) \| mark: NOT REPORTED (caption does not say) \| n: NOT REPORTED per bin` | 2 — caption-derived, panel not rendered | Per-bin n is not given in the caption; the >0.6 Tc and >80 MCS bins are likely very small (Fig 1d shows few such ligands) and any bin-wise claim rests on them | CC-BY 4.0, no ND (p26) |
| S5B/S5D | 26 | Method scores by the same similarity bins | box or violin (mark not stated) | `PLOT \| facet: similarity metric (2: Tc bins; MCS% bins) \| vary: similarity bin (4) \| series: method (4) \| measure: method score (L-pLDDT / ipTM / pIC50 / kcal mol⁻¹, per series) \| mark: NOT REPORTED \| n: NOT REPORTED per bin` | 2 — caption-derived, panel not rendered | The four series have four incommensurate score units on one measure axis | CC-BY 4.0, no ND (p26) |
| S6 | 27 | AF3-vs-experiment error against AF3-vs-other-method disagreement | scatter | `PLOT \| facet: comparison method (3: Chai-1, Boltz-2, DOCK3.7) \| vary: AF3-to-other L-RMSD (continuous) \| series: ligand class (3: has affinity data n = 202 green, high COM distance red, no affinity data grey) \| measure: AF3-to-ground-truth L-RMSD \| mark: point \| n: 1 per mark, 557 per panel` | 3 — caption-derived, panel not rendered | | CC-BY 4.0, no ND (p27) |
| S7 | 28 | Pairwise method-vs-method pose accuracy against ground truth | scatter | `PLOT \| facet: method pair (6: AF3–Chai-1, AF3–DOCK, Boltz-2–Chai-1, Chai-1–DOCK, Boltz-2–AF3, Boltz-2–DOCK) \| vary: method-1 L-RMSD to ground truth (continuous) \| series: exemplar (2 labelled: Mac-x4091, Mac-x3927) \| measure: method-2 L-RMSD to ground truth \| mark: point \| n: 1 per mark, 557 per panel` | 6 — caption-derived, panel not rendered | | CC-BY 4.0, no ND (p28) |
| S8 | 29 | Similarity of each benchmark's actives to the corresponding training set | histogram or density (mark not stated) | `PLOT \| facet: similarity metric (2: Tanimoto; MCS%) \| vary: similarity to training set (continuous) \| series: dataset (5: AmpC n = 247, D4 n = 205, σ₂ n = 201, Mac1_af3 n = 557, Mac1_boltz n = 557) \| measure: count or density \| mark: NOT REPORTED \| n: per series as listed` | 2 — caption-derived, panel not rendered | This is the panel that would show whether the σ₂/D4/AmpC molecules are pre- or post-cutoff, and the caption discusses only chemical similarity, never deposition date | CC-BY 4.0, no ND (p29) |
| S9 | 30 | Boltz-2, AF3 and DOCK scores against measured pKᵢ for the actives of each screen | scatter | `PLOT \| facet: target (3: σ₂ n = 201, D4 n = 205, AmpC n = 247) × score (3: Boltz-2 pIC50, AF3 L-pLDDT, DOCK score) \| vary: score value (continuous) \| series: fit line (3: before correction black dotted, after correction blue, dataset-mean baseline green) \| measure: measured pKi \| mark: point \| n: 1 per mark; 201 / 205 / 247 per row` | 9 — caption-derived, panel not rendered | Actives only; the false positives that make the task hard are excluded from every panel, which is the flattering case the authors themselves flag on p12 | CC-BY 4.0, no ND (p30) |
| S10 | 31 | Boltz-2 affinity error when false positives are given an assumed pKᵢ, under two assumptions | scatter | `PLOT \| facet: target (3: σ₂, D4, AmpC) × FP assumption (2: pKi = 2 × threshold; random pKi between threshold and 1) \| vary: Boltz-2 predicted pIC50 (continuous) \| series: fit line (3: before correction grey dotted, after correction red, measured-mean baseline blue) \| measure: measured or assumed pKi \| mark: point \| n: 506 / 541 / 1,293 per target` | 6 — caption-derived, panel not rendered | Under the fixed-2× assumption the caption itself warns the baseline is uninterpretable ("Baseline MAE is only quoted for b), since the error could be misinterpreted when all non-binders' pKi values are fixed") — yet the 2× number is the one quoted first in the p12–13 text | CC-BY 4.0, no ND (p31) |
| S11 | 32 | Semi-log ROC (early enrichment) for the three screens | line | `PLOT \| facet: target (3: σ₂, D4, AmpC) \| vary: false positive rate, log scale (continuous) \| series: score (4: AF3 L-pLDDT, DOCK3.7 energies, Boltz-2 pIC50, Boltz-2 binary probability) \| measure: true positive rate \| mark: line \| n: 506 / 541 / 1,293 per panel` | 3 — caption-derived, panel not rendered | | CC-BY 4.0, no ND (p32) |
| S12 | 33 | Rolling-window hit-rate curves against normalised rank (pProp) | line with band | `PLOT \| facet: target (3: σ₂ 201/305, D4 205/336, AmpC 247/1,046) \| vary: pProp rank (continuous) \| series: score (3: DOCK3.7, AF3 L-pLDDT, Boltz-2 pIC50) \| measure: hit rate (fraction) with 95% Wilson CI \| mark: line \| n: rolling window of 100 (AmpC, σ₂) or 50 (D4) per point` | 3 — caption-derived, panel not rendered | | CC-BY 4.0, no ND (p33) |
| S13 | 34 | DOCK score against AF3 L-pLDDT and Boltz-2 pIC₅₀, all four datasets | scatter | `PLOT \| facet: target (4: σ₂, D4, AmpC, Mac1) × co-folding score (2: AF3 L-pLDDT, Boltz-2 pIC50) \| vary: DOCK score (continuous) \| series: hit class (2: known actives blue, non-binders red; Mac1 panel has actives only) \| measure: co-folding score \| mark: point \| n: 506 / 541 / 1,293 / 557 per target` | 8 — caption-derived, panel not rendered | The Mac1 panel has only one series ("Note that Mac1 dataset comprises only actives") and so is not comparable to the other three, but is drawn in the same grid | CC-BY 4.0, no ND (p34) |

**Panel-group rows: 28** (14 for main Figures 1–5, 14 for Supplementary Figures S1–S13).
**Pages rendered: 5** (pp. 5, 7, 10, 11, 14), all main-figure pages; PNGs deleted after reading.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5, Claude Code session)
- **schema_version**: v3
- **confidence**: **high** for the pose-arm and virtual-screen numbers, the holdout design, the
  oracle-leakage routes and the stated limits — these are printed in running text or in rendered
  figure tables and were read directly. **Medium** for the Supplementary Figure rows S1–S13, which
  are caption-derived without rendering, so `mark` and per-panel `n` are `NOT REPORTED` in several.
  **Medium-low** on two specific points: (i) whether templates were enabled in any of the three
  co-folding runs, and (ii) whether the reported pose is top-1 or otherwise selected — both are
  genuinely unstated and both change how the headline number should be quoted.
  What was hard to read: the Fig 2a and Fig 2b summary tables and the Fig 3a / Fig 5 AUROC legends
  are **images with no extractable text**, so the exact success rates (72.2/66.6/52.1/40.9) and the
  conformational counts exist nowhere in the PDF's text layer; they were recovered only by
  rendering. Anyone querying this paper from `pdftotext` alone would find only "~70%".
- **unresolved**:
  1. **Top-1 vs best-of-N is not resolvable from the paper.** Methods (p18) give no seed count, no
     number of diffusion samples, no recycle count and no model-selection rule for any of the three
     co-folding tools. One pose and one score per ligand are reported. No number is *described* as
     oracle-selected and no "best of N" language appears, so the most probable reading is each
     tool's default top-ranked output — but the paper does not say it, so 72.2% cannot be asserted
     as a confirmed top-1 rate.
  2. **Template usage is never stated.** "SMILES strings... and the sequence of the enzyme as
     inputs" (p4) is consistent with either templates on (defaults) or off. For a target with dozens
     of pre-cutoff deposited structures this is the difference between a sequence-only prediction
     and a template-guided one, and it is the single unclosed leakage route.
  3. **Boltz-2's training cutoff is given two different dates**: "1 June 2023" (Methods, p17) and
     "2023-06-30" (Results, p3). One month, immaterial to the argument, but the corpus should quote
     the Methods date.
  4. **The determination dates of the 557 structures are never given.** The abstract asserts they
     "were determined after the training cut-off dates" (p1) but no date range, deposition date or
     data-collection date appears anywhere in the text, and the table that would carry them
     (STable 1) is deliberately embargoed (p21). The holdout claim rests on the authors' assertion
     plus the fact of non-disclosure, not on a checkable date column.
  5. **Figure 4 panel b is missing from this version** — panel "a)" is printed twice on p11 while
     the caption and the p9 text both describe a panel b and cite three correlations from it
     (r = −0.297, −0.387, and a null). Likely a v3 layout error; recorded in `hides`.
  6. **Figure 5 panel lettering contradicts the running text.** The Fig 5 caption and the rendered
     panel labels read a) σ₂, b) D4, c) AmpC; the p12–13 text cites "For AmpC (Fig. 5b)" and Fig 5c
     for D4. The AUROC values disambiguate it, but a reader following panel letters from the text
     will land on the wrong target.
  7. **The virtual-screen arm's relationship to the training cutoffs is never analysed.** Two of the
     three source campaigns (Lyu 2019, Alon 2021) predate AF3's 2021-09-30 cutoff. The paper
     characterises those sets by *chemical* similarity to training (Tc 0.11–0.19) but never by
     deposition date, so the arm cannot be described as a temporal holdout and this note does not.
  8. **Chai-1 was dropped from the virtual-screen arm without explanation** — "only AlphaFold3 and
     Boltz-2 were used" (p18); no reason given.
  9. **Only AF3 was tested for receptor conformational recovery.** Chai-1 and Boltz-2 conformational
     performance is unmeasured, so "co-folding does not recover the conformational change" rests on
     one model with n = 19 and n = 20.
  10. **D4 n disagrees between sections**: Methods p18 says 549 molecules were prioritised, while
      p13 and SFig 12 give 205 actives + 336 inactives = 541, and p12 says 541 tested. Eight
      molecules unaccounted for.
  11. **Schema gap — there is no TABLE form in the `data_shape` grammar.** Figures 2a, 2b and S2
      each pair a plot or render with a **numeric summary table that carries the paper's headline
      result** (the success rates, the conformational recovery counts, the cluster-head counts).
      `SCHEMATIC | ... | no data` is a false statement about them, PLOT has no slot for a table, and
      MATRIX is for heatmaps where both axes are indices. I folded each table into the `panels` and
      `hides` cells of its sibling row and said so, but a `TABLE | rows: <var> (<n>) | cols: <var>
      (<n>) | value: <what the cell holds>` form would have been the honest answer. This is the same
      class of defect that produced MATRIX and TREE in v3.
  12. **Schema gap — `metric_saturation` has no vocabulary for a floor at zero with tiny n.** The
      0/20 open-state result is simultaneously a numeric floor and an unpowered arm; the field asked
      for numeric saturation and the `unpowered` tag applies to `anti_memorization_control`, not to
      an arm. I recorded it in both `metric_saturation` and `anti_memorization_control` and
      cross-referenced, but the note is duplicated in exactly the way changelog item 9 was trying to
      prevent.
  13. **Schema gap — `prospective` takes one value plus one line, but this paper has two arms with
      different answers.** `states_generated` and `state_metric` were made dual in v3 for precisely
      this reason; `prospective` was not, and a single "partial" here loses the fact that arm 1 is a
      strict temporal holdout and arm 2 is a plain retrospective re-analysis. I wrote both under one
      `partial` heading. Suggest allowing ` + ` here in v4.
  14. **No tag needed that does not exist.** Every tag used below is from the fixed v3 vocabulary.
      The one I reached for and correctly could not use was a marker for **"benchmark built from the
      authors' own unpublished experimental data"**, which is what makes this holdout unusually
      clean and is distinct from both `anti-memorization` and `experimental`. Recorded here rather
      than invented.
- **why_it_matters**: *(left empty for the user)*

## Tags

`general-protein` `gpcr` `cofolding` `benchmark-only` `multi-backbone` `single-state`
`rmsd-only` `binary-predicate` `prospective` `anti-memorization` `design-level-oracle`
`confidence-as-discriminator` `orthosteric` `ligand-driven` `preprint` `comparator-numbers`
`precedent` `contrast`

Tag notes, since several are contestable:
- **`general-protein`** for Mac1 (a viral macrodomain hydrolase — not a kinase, transporter or
  fold-switcher) and for AmpC and σ₂. **`gpcr`** is added only because the **dopamine D4 receptor**
  is one of the three virtual-screen targets and a reverse lookup for GPCR co-folding results should
  return this paper's D4 numbers (AF3 AUROC 46.42, below random). No GPCR appears in the pose arm.
- **`benchmark-only`** is the method class: no new method is introduced. **`cofolding`** marks what
  is being benchmarked.
- **`single-state`**, not `ensemble`: one complex per ligand per method, and the receptor collapses
  onto one basin across all 557 (Cα RMSD 0.1–0.4 Å). No sampling-breadth claim is made or tested.
- **`rmsd-only` + `binary-predicate`**: the headline metric is thresholded RMSD to a reference; the
  conformational-state calls are binary predicates on per-residue RMSD. `visual-metric` does **not**
  apply — nothing is called by eye.
- **`prospective` and `design-level-oracle` together, deliberately.** The Mac1 arm is a genuine
  post-cutoff, never-deposited holdout (`prospective`, `anti-memorization`); the target was
  nonetheless chosen because the authors held the structures and the models had already trained on
  ~326 related Mac1 complexes, which the authors concede "may inflate apparent pose recovery rates"
  (p15) — that is route 7, `design-level-oracle`. **`oracle-leak` is NOT applied**: no deposited
  structure of the target complex entered the co-folding pipeline on the evidence given.
- **`no-anti-memorization` is explicitly NOT applied** — the control arm was run and analysed
  (r = 0.065, r = −0.078, plus the binned and later-cutoff arms).
- **`unpowered` is NOT applied at the note level** — n = 557 is the paper's scale. The
  conformational sub-arm (n = 19, n = 20, AF3 only) is unpowered and that is recorded in the fields,
  not in a tag that would mislabel the whole paper.
- **`templates-on` / `no-template-no-msa` are both withheld** — the protocol says SMILES + sequence
  with a full jackhmmer MSA, so `no-template-no-msa` is factually wrong (there is an MSA) and
  `templates-on` is unevidenced (never stated). See `unresolved` item 2.
- **`experimental-validation` is NOT applied.** The crystallography and HTRF assays are extensive
  and are the authors' own, but they are the **ground truth against which predictions were scored**,
  not a lab test of a prediction the models made. Applying the tag would false-positive every
  benchmark that has a reference structure.
- **`allosteric-site` / `cryptic-pocket` / `allosteric-failure` do not apply** — all 557 ligands are
  orthosteric substrate-competitive binders (p3). The twisted and open states are local
  active-site-adjacent rearrangements, not an allosteric site.
- **`comparator-numbers`**: the Fig 2a success-rate table and the Fig 3a / Fig 5 AUROC sets are the
  most directly quotable numbers in the corpus for co-folding pose accuracy under a clean temporal
  holdout.
- **`precedent` + `contrast`** per `stance`; provisional, the user's call.
