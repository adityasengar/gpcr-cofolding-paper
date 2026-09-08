# skrinjar2026generalization

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–31), which coincide with the
printed page numbers** (PDF p4 carries the printed folio "4"). Layout: p1 title/abstract, p2–3
Introduction, p3–13 Results, p13–15 Discussion, p15 Data availability, p15–20 Methods, p21–26
Acknowledgements + References, p27–31 Supplementary Figures S1–S4 and Supplementary Table S1
(S-Table S1 on p28).

**Version caveat, recorded up front because it changes `A. Identity`:** the PDF held by the corpus
is the **bioRxiv preprint posted 4 August 2025**, DOI `10.1101/2025.02.03.636309`, titled *"Have
protein-ligand cofolding methods moved beyond memorisation?"* with **five** authors. `refs.bib`
records the **peer-reviewed journal version**: *"Evaluating generalization in protein–ligand
cofolding methods"*, **Nature Structural & Molecular Biology 2026**, DOI
`10.1038/s41594-026-01797-5`, with **six** authors (adds Gabriel Studer). Everything quoted below
was read from the preprint. The corpus should **cite the NSMB version**; page numbers, panel
letters and numeric values in this note are the preprint's and are not guaranteed to survive
into the journal version. See `unresolved`.

**Figure-value caveat:** the paper prints almost no success-rate numbers in running text. Values
in `metrics_reported` marked *(read from rendered panel)* were read off panels rendered with
`pdftoppm` at 150–450 dpi (pages 4, 6, 7, 9, 10, 12, 19). Bin counts and Fig 1E bar labels are
printed in the figure and are exact; curve values in Figs 1A/1B, 2A, 3, 6 are read from marks and
are approximate to ±1–2 points.

---

## A. Identity

- **citekey**: `skrinjar2026generalization`
- **doi**: **10.1101/2025.02.03.636309** (bioRxiv, this version posted **4 August 2025**) — banner
  on every page, e.g. p1: "bioRxiv preprint doi: https://doi.org/10.1101/2025.02.03.636309; this
  version posted August 4, 2025." `refs.bib` instead records **10.1038/s41594-026-01797-5**
  (Nature Structural & Molecular Biology). Both are real; the PDF held is the preprint.
- **year**: **2025** as posted (p1). The citekey and `refs.bib` say 2026, which is the journal
  version's year, not this PDF's.
- **venue**: **bioRxiv preprint, not certified by peer review** — p1: "The copyright holder for
  this preprint (which was not certified by peer review) is the author/funder." Tagged `preprint`
  on the evidence of this PDF. The journal version (NSMB 2026) is peer-reviewed but is not the
  document extracted here.
- **title**: **"Have protein-ligand cofolding methods moved beyond memorisation?"** — p1.
  (Journal title differs: "Evaluating generalization in protein–ligand cofolding methods".)
- **authors**: Peter Škrinjar, Jérôme Eberhardt, Gerardo Tauriello, Torsten Schwede, Janani
  Durairaj — p1. Biozentrum, University of Basel, and SIB Swiss Institute of Bioinformatics,
  Basel. Corresponding: janani.durairaj@unibas.ch. **Five authors in this PDF**; `refs.bib` lists
  six (adds Gabriel Studer).
- **benchmark name**: **Runs N' Poses** (p1, p3). Data at Zenodo
  `doi.org/10.5281/zenodo.14794785`; code at `github.com/plinder-org/runs-n-poses`; ML-ready
  version on Polaris Hub; models to be deposited in ModelArchive under `ma-rnp` (all p15).

## B. Scope

- **system**: **general protein — protein–small-molecule complexes, unrestricted by family.**
  The set is everything in the PDB after the cutoff that passes automated quality filters (p15–16),
  not a curated family. Families are visible only in the cluster table: cluster #1 is 171 SARS-CoV-2
  main protease structures, cluster #2 is 136 protein kinase complexes, #3 phosphodiesterase 10,
  #4 HCoV-NL63 main protease, #5 neuronal nitric oxide synthase, #6 cytochrome P450, #7 FABP1,
  #8 BRDT bromodomain, #9 PRMT5/MEP50, #10 glucose 1-dehydrogenase (Supplementary Table S1, p28).
  No GPCR, transporter or fold-switching arm. Tagged `general-protein` only, deliberately — kinases
  are present but are not the paper's system.
- **n_targets**: give n at every level, because the paper reports at least six different
  denominators (Table 1, p18; text p16–18; Fig 3C text p7):
  - **Post 30 Sep 2021 full set: 2,600 systems / 2,585 PDB IDs / 4,282 all ligands / 3,047 proper
    (non-ion, non-artifact) ligands / 401 multi-ligand systems / 790 multi-protein systems** (Table 1, p18).
  - **Common subset predicted by all four methods: 2,077 systems / 2,311 proper ligands (3,288
    including ions)**, from **229,887 predictions** (p18).
  - Per-method (Table 1, p18): AF3 2,409 systems / 2,710 proper ligands; Protenix 2,323 / 2,609;
    Chai-1 2,292 / 2,572; Boltz-1 2,139 / 2,400; AF3-NT 2,411 / 2,711; Boltz-1x 2,091 / 2,338;
    RFAA 1,769 / 1,946.
  - **Post 1 Jun 2023 subset (Boltz-2 arm): 1,028 systems / 1,025 PDB IDs / 1,187 proper ligands**;
    Boltz-1 ran 844 systems / 933 proper ligands, Boltz-2 871 / 961 (Table 1, p18).
  - **Redundancy clusters: 1,017 total, 789 in the common subset** (p7), from graph community
    clustering at SuCOS-pocket similarity > 50.
  - **Number of distinct proteins: NOT REPORTED.** Systems were clustered to 80% sequence identity
    for redundancy filtering (p16) but the resulting protein-cluster count is never given.
  - Dropped: **21 systems** with nucleic acid chains near the pocket; **72 system ligands from 63
    systems** in the common subset unreadable by RDKit, so no similarity score (p16–17);
    **128 systems** failed to produce output across all four methods (p17).
- **method_class**: **benchmark-only.** The paper introduces a dataset and evaluates existing
  methods; it proposes no predictor. The methods *benchmarked* are all co-folding. No new
  architecture, no MSA or template intervention is proposed.
- **backbones**: **six co-folding methods plus one non-co-folding baseline, seven arms total**
  (p17, Table 1 p18). Versions are pinned:
  | arm | version | role | stated training cutoff |
  |---|---|---|---|
  | AlphaFold3 | v3.0.0 | primary, templates **on** | 30 Sep 2021 (p3) |
  | Protenix | v0.3.4 | primary | 30 Sep 2021 (p3) |
  | Chai-1 | v0.5.1 | primary, ESM embeddings enabled | 30 Sep 2021 (p3) |
  | Boltz-1 | v0.4.1 | primary | 30 Sep 2021 (p3) |
  | AF3-NT | v3.0.0 | control, templates **off** | 30 Sep 2021 |
  | Boltz-1x | v1.0.0 | supplementary arm (S1) | NOT REPORTED separately |
  | Boltz-2 | v2.0.3 | later-cutoff arm | **1 Jun 2023** (p5, p18) |
  | RoseTTAFold-All-Atom | version NOT REPORTED | supplementary arm, 1 model not 25 | **NOT REPORTED** |
  More than two compared head to head → tagged `multi-backbone`. **Important caveat:** the paper
  asserts a *single shared* cutoff of 30 September 2021 for AF3, Chai-1, Protenix and Boltz-1
  (p3: "released after their training cutoff (30 September 2021)") and does not cite each method's
  own stated cutoff individually. See `unresolved`.
- **templates**: **dual — on and off, both run.** AF3 primary arm: "AlphaFold3 predictions were
  made with templates enabled. AlphaFold3 was also run without templates for comparison (AF3-NT)"
  (p17). Template settings for Protenix, Chai-1, Boltz-1, Boltz-1x, Boltz-2 and RFAA are
  **NOT REPORTED**. Whether the AF3 template search was date-restricted to the pre-cutoff PDB is
  **NOT REPORTED** — see `oracle_leakage` route 1.
- **msa_handling**: **full, and deliberately identical across methods.** p17: "To ensure that the
  prediction outcomes had no reliance on the depth or quality of the multiple sequence alignments
  (MSAs) generated by different pipelines, we used the same MSAs as input for all methods. The
  standard AlphaFold3 MSA generation pipeline was run to obtain the non paired and paired MSAs for
  each system." Converted per method: a3m + pairing_db=uniprot for Protenix; `a3m-to-pqt` with
  UniProt taxonomy IDs for Chai-1; custom MSA CSV with the same pairing keys (−1 for unpaired) for
  the Boltz methods (p17). No subsampling, no clustering, no state filtering.

## C. Conformational core

- **states_generated**: **ensemble + single-state.** Each method produced **25 models per system**
  (5 seeds × 5 diffusion samples, 10 recycling steps, 200 diffusion sampling steps; p17), so
  sampling is an ensemble; but the reported headline is the single **top-ranked** model per system,
  and the paper's own finding is that the ranking collapses that ensemble onto a model "usually not
  much better than random selection" (p11). The dual value is the paper's result, not a hedge.
  RFAA is the exception: "run with only 1 model output instead of 25" (p5) — single-state.
  Note this is **pose/complex sampling, not conformational-state generation**; the paper does not
  set out to produce alternative protein conformational states. The one state observation is
  anecdotal: p11, "the ground truth is a protein kinase in inactive DFG-out conformation [35],
  however the predicted structure adopts a DFG-in conformation" (Fig 5C).
- **structural_priors_used**: substantial, and none of it is a defect —
  1. **The entire PDB up to 2024-06-05** as the training-set proxy: "we perform a Foldseek [56]
     search against the entire PDB and calculate similarities between any pair of test and train
     systems where any protein chain has an alignment" (p20); a Parquet file of "all the
     similarities found to every system in the PDB up to 2024-06-05" is released (p15).
  2. **PLINDER** [28] system definitions, pocket definitions and X-ray validation criteria drive
     dataset construction (p15–16).
  3. **Deposited post-cutoff X-ray structures as ground truth** — receptor CIF and ligand SDF saved
     by PLINDER (p18).
  4. **Templates** from the PDB in the AF3 primary arm (p17).
  5. **Kincore** [35] cited once, on p11, only to name the DFG-out state of one ground-truth kinase
     in a figure caption discussion. It drives nothing.
  None of these were used to select systems by expected outcome — see `oracle_leakage` route 7.
- **oracle_leakage**: **the benchmark's prediction pipeline is clean; the analysis layer uses the
  reference structure in four separate places, three of them labelled as such by the authors and
  one (route 4) not.** Enumerated route by route, each with the page where the protocol is
  described so every negative is checkable.

  **Route 1 — structures used as input or template: PRESENT but bounded, and one detail is
  unstated.** AF3 was run with templates enabled (p17: "AlphaFold3 predictions were made with
  templates enabled"). The paper **never states that the template search was restricted to
  structures released before 30 September 2021**, so a post-cutoff homolog — in principle the
  ground-truth entry itself — could in principle be retrievable as a template. The authors bound
  this two ways: a full **AF3-NT (templates off) control arm** was run (p17, Table 1 p18,
  Supplementary Figure S1 p27), and p5 reports "AlphaFold3 with and without templates does not show
  any significant differences; this is expected since ligand information from the template is not
  utilised by the method." So any template effect is empirically ~zero for the ligand pose, which is
  the measured quantity. Recorded as present-but-controlled, with the date restriction unstated.
  MSAs are sequence, not structure, and are not date-restricted either (p17) — not a structural
  oracle route.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates
  or alignments: NONE FOUND.** The full input-preparation protocol is on p17 ("Running all-atom
  prediction methods") and the similarity protocol on p20 ("Similarity scoring"); neither invokes
  any state-annotated database. Kincore appears exactly once, on **p11**, as a citation describing
  the ground-truth DFG-out conformation of one example complex after the fact. No state annotation
  enters templates, alignments, inputs or scoring.

  **Route 3 — cluster labels derived from known states: NONE FOUND in the prediction pipeline;
  PRESENT in the analysis, by construction.** Clustering exists — "The dataset was clustered using
  community clustering on the graph connecting systems having SuCOS-pocket similarity scores above
  50. Cluster representatives are chosen as those with the lowest similarity to the training set"
  (p21) — but it is applied **downstream, to stratify results** (Fig 3C), never to condition a
  prediction. The load-bearing consequence, which the paper does not flag: **the SuCOS-pocket
  similarity that defines every x-axis in the paper is computed from the ground-truth ligand pose
  of the test system** (p20: SuCOS requires superposing "the ligand poses of a query and target
  system"). The stratification variable therefore *cannot be computed without the answer*, so the
  bins are a retrospective annotation of a prospective prediction. That is not leakage into the
  models, but it does mean the benchmark's central axis is not available at prediction time.
  Cross-referenced to route 7.

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
  states: PRESENT, and this is the one route the authors do not label.** Two instances:
  (a) **The iPTM decision threshold is fitted on the evaluation set against the references, with no
  held-out split, and the accuracy of that same threshold is then reported.** p11: "For each method,
  we independently determine the best threshold as the optimal operating point of the ROC-AUC curve
  across all predicted systems, where positives are predicted models with LDDT-PLI > 0.8 and RMSD
  < 2Å compared to the reference and negatives are predicted models that don't satisfy this
  criteria." The fitted thresholds (AF3 0.92, Protenix 0.99, Chai-1 0.75, Boltz-1 0.95; p11) are
  then used to produce the Fig 6E accuracy curves (p13). The reported classification accuracies are
  therefore **in-sample** and are optimistic upper bounds on what a threshold transferred to new
  data would achieve.
  (b) **The success criterion itself was chosen after inspecting the evaluation set.** The 2 Å /
  0.8 combination is justified on p19 by pointing at the joint RMSD–LDDT-PLI distribution of "all
  229,887 predictions" and the size of the two off-diagonal corners (1.6% and 8.3%), i.e. by
  looking at the results before fixing the predicate. The thresholds themselves are conventional
  and cited to prior work ([17], [19]), and the paper runs an **RMSD-only control** (Fig 1B, p3–4)
  showing the trend is unchanged — which is exactly the right control — but the *combination* was
  settled against this data.
  Genuinely **clean** by contrast: the inference hyperparameters were fixed by copying an external
  protocol, not tuned — p17: "Following the protocol of the PoseBusters benchmark conducted by the
  authors of AlphaFold3 [22], ... were run on one A100 40 GPU each with 10 recycling steps, 200
  diffusion sampling steps, 5 seeds and 5 diffusion samples per seed". No sweep, no range, no
  per-target choice.

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had: PRESENT by design and
  openly declared.** p3: "we define the success rate as a combination of LDDT-PLI (> 0.8) [17] and
  ligand pose RMSD (< 2 Å)"; p19: "we redefine the commonly used 'Success rate' measure as the
  fraction of systems with <2Å RMSD and >0.8 LDDT-PLI." All scores are computed against the
  deposited reference with OpenStructure 2.8.0 `compare-ligand-structures` (p18). This is what a
  benchmark *is*; it is recorded because the schema requires every route enumerated, not as a
  defect. The relevant question — whether the predicate drives the conclusion — is answered by the
  RMSD-only arm (Fig 1B) and the pli_qcov arm (S3L), both of which reproduce the trend.

  **Route 6 — best/worst model labels assigned against a held reference: PRESENT, deliberate, and
  labelled as oracle upper bounds.** p11: "the success rates of the best-scored (i.e closest to the
  ground truth), worst-scored (i.e furthest from the ground truth), a randomly picked model from the
  25, and the top-ranked model selected based on each method's ranking scores." Fig 6 caption, p12,
  makes it explicit: "best-scored model (blue diamonds, **best LDDT-PLI across 25**), worst-scored
  model (red crosses, worst LDDT-PLI across 25)". The gray "Best" line in Figs 1A/1B and 3A–C is
  the same device across methods: "selecting the best-scored model from the four top-ranked"
  (Fig 1 caption, p4). Every one of these is an oracle curve, and the paper's argument depends on
  the *gap* between them and the method's own top-ranked model — the oracle use is the measurement,
  not a contaminant. It does mean **the gray "Best" curve is not an achievable performance number**
  and must never be quoted as one.

  **Route 7 — design-level oracle (systems or conditions chosen because the expected answer is
  known): NONE FOUND.** The selection protocol is fully specified and automated on **p15–16**: the
  PLINDER ingestion pipeline was run "on all entries in the Protein Data Bank (PDB) [51] released
  after 30 September 2021 until 9 January 2025", then filtered on crystallographic quality
  (resolution ≤ 3.5 Å, R ≤ 0.4, R_free ≤ 0.45, R − R_free ≤ 0.05, all heavy atoms present in ligand
  and pocket, no alternates, no clash outliers, no crystal contacts), on interaction statistics
  (3–50 PLIP interactions, 5–100 pocket residues, largest ligand MW 200–800), and on composition
  (X-ray only, first bioassembly, ≤ 5 ligand chains, ≤ 5 protein chains, no covalent ligands, not
  all-cofactor/oligomer). Redundancy was broken by taking "**Only one system per redundancy
  cluster ... the one with the maximum number of PLIP [52] interactions detected**" (p16) — a
  criterion computed from the reference structure but blind to any prediction. **No system was
  selected, excluded or binned on the basis of an expected or observed prediction outcome.** The
  authors also state the residual risk honestly (p15): "As the dataset was constructed in an
  automated fashion, there may be a few complexes which do not qualify as biologically relevant."
  The one thing that comes close is the retrospective nature of the similarity bins (route 3), which
  is a property of the *analysis axis*, not of system selection, and is weaker still than
  design-level oracle use.

  **Net:** nothing that could hand a model the answer entered any prediction. The reference enters
  the analysis at four points; three are declared and load-bearing (routes 5, 6, and route 1's
  bounded template use), and one is not declared — **the in-sample iPTM threshold of route 4**,
  which inflates the Fig 6E confidence-classification accuracies only.
- **prospective**: **partial — prospective in the predictions, retrospective in the analysis.**
  Prospective side: every one of the 2,600 systems was deposited after the models' stated training
  cutoff, and the automated selection protocol (p15–16) is blind to prediction outcome, so no model
  could have seen these answers. Retrospective side: the similarity bins, the success predicate, the
  best/worst curves and the iPTM thresholds are all computed against the deposited references after
  the fact (p11, p19, p20). The paper is the right shape for a prospective claim about *models* and
  the wrong shape for a prospective claim about *its own metric*.
- **state_metric**: **continuous coordinate + binary predicate**, and both are used throughout, so
  the dual value is required.
  - Continuous: binding-site-superposed symmetry-corrected **ligand RMSD**; **LDDT-PLI** (with
    "added model contacts" flag enabled, "which further penalises protein-ligand contacts present
    in the model which are not in the reference"); **LDDT-LP**; **pocket-recovery F1**; all from
    OpenStructure 2.8.0 (p18).
  - Binary: **success = RMSD < 2 Å AND LDDT-PLI > 0.8** (p3, p19). Thresholds are stated and
    justified: 2 Å is the classical docking convention (p3), 0.8 LDDT-PLI is cited to CASP15 [17]
    (p3), and the combination is defended on p19 by the sizes of the two off-diagonal populations
    (1.6% high-LDDT-PLI/high-RMSD, 8.3% low-RMSD/low-LDDT-PLI). Secondary predicates: PB-Valid
    (all PoseBusters "dock" checks pass, p20); LDDT-LP > 0.8 (Fig 4 caption, p9); per-method iPTM
    thresholds (p11).
  - The *similarity* axis is its own continuous metric: **SuCOS-pocket = SuCOS × (pocket_qcov/100)**
    (p20), binned into eight ordinal bins (0–20, 20–30, 30–40, 40–50, 50–60, 60–70, 70–80, 80–100).
  - No visual-only state call anywhere. Fig 5 renders are illustrative and every panel carries the
    numeric RMSD / LDDT-PLI / LDDT-LP (p10).
- **metric_saturation**: **yes, at the high-similarity end, numerically.** In the 80–100 bin the
  oracle "Best" curve reaches ~97% success (Fig 1A, p4, read from panel) against a hard 100%
  ceiling, and the four individual methods sit at 89 / 86 / 85 / 81% (Fig 1E printed labels, p4) —
  the top bin has ~10–20 points of headroom left, so between-method differences compress there.
  **LDDT-LP ceilings across the whole range**: "the majority of predictions have an LDDT-LP > 0.8"
  in every bin (p8), quantified in the Fig 4 caption (p9) as 90–92% of all systems per method — a
  metric that is at ceiling in the lowest bin cannot resolve the paper's question, which the authors
  say themselves (p8: "these results do not guarantee that the predicted protein models could be
  used for downstream docking applications"). Pocket F1 is similarly near 1.0 from the mid bins on
  (Fig 4E, p9). The success-rate floor is not reached: the lowest bin is 8–25% depending on method,
  not 0. *Axis truncation in Fig 6E/F is a figure defect and is recorded in `hides`, not here.*
- **directional_control**: **NONE — no state handle exists in this study, by design.** Nothing
  instructs a method which pose or protein conformation to produce. The only inputs varied at all
  are: the **ligand SMILES** (which is the task, not a control), **templates on/off** for AF3 only
  (p17), and the **random seed** (5 seeds × 5 diffusion samples, p17). The seed handle is explicitly
  tested and found useless: "we observe that using multiple seeds is currently not useful at
  inference time for any of the methods" (p11). Tagged `seed-only`.
- **anti_memorization_design**: **this is the paper's entire construction, and it is the strongest
  in the corpus.** Two nested post-cutoff sets, with per-complex similarity annotation:
  - **Cutoff definition.** The primary cutoff is **30 September 2021**, taken as the stated
    structural training cutoff shared by AlphaFold3, Chai-1, Protenix and Boltz-1 (p3: "2,600
    high-resolution PLI systems released after their training cutoff (30 September 2021)"). The
    second cutoff is **1 June 2023**, Boltz-2's stated cutoff (p5: "Boltz-2 [31] has been released
    which was trained with a cutoff of 2023-06-01, thus using a full two years more PDB data than
    the other methods"; restated p18). The cutoff is a **release-date cutoff on the PDB**, not a
    sequence- or pocket-identity holdout, and the paper says so as a portability requirement:
    "the only requirement to apply the Runs N' Poses benchmark in its entirety on a new method is a
    structural training cutoff of 30 September 2021" (p15). Per-model cutoffs are **asserted as one
    shared date**, not sourced individually per method; RFAA's cutoff is **NOT REPORTED**.
  - **n at every level.** Ingestion window 30 Sep 2021 → **9 Jan 2025** (p15). After filtering:
    **2,600 systems / 2,585 PDB IDs / 3,047 proper ligands** (Table 1, p18). Common subset actually
    predicted by all four methods: **2,077 systems / 2,311 proper ligands / 229,887 predictions**
    (p18). Post-1-Jun-2023 subset: **1,028 systems / 1,187 proper ligands**, of which Boltz-1
    modelled 844 and Boltz-2 871 (Table 1, p18). Losses accounted for: 128 systems failed in all
    four methods, 21 dropped for nucleic-acid chains, 72 ligands from 63 systems unreadable by
    RDKit (p16–17).
  - **Per-complex similarity annotation.** Each test system is scored against **every** PLI system
    in the pre-cutoff PDB: a **Foldseek** search against the entire PDB finds any pair with a
    protein-chain alignment; for each pair, ligand poses are superposed with RDKit
    `rdShapeAlign.AlignMol`, **SuCOS** (volume + chemical-feature overlap) is computed, and
    multiplied by **pocket_qcov/100** (the fraction of the query's 6 Å pocket residues that align to
    the target's) to give **SuCOS-pocket** (p20). The maximum over all training systems defines the
    system's training-set similarity and identifies its "closest training system". p3 states the
    intent: "a training system is only considered similar if it has a similar ligand pose in a
    similar protein pocket to the test system."
  - **Strata.** Eight ordinal SuCOS-pocket bins with counts printed on the axis of Fig 1 (p4), for
    the common subset of proper ligands: **0–20 (n=64), 20–30 (n=91), 30–40 (n=149), 40–50 (n=258),
    50–60 (n=312), 60–70 (n=376), 70–80 (n=368), 80–100 (n=673)** — 2,291 annotated ligands. Fig 4
    prints n=674 for the top bin rather than 673 (p9); the one-ligand discrepancy is unexplained.
  - **Prevalence stratum**, orthogonal to similarity: for each test ligand, the number of pre-cutoff
    training systems containing an analogous ligand (**>0.9 RDKit topological fingerprint Tanimoto**)
    (p6, p17). Levels and n from Fig 3A (p7): **0–2 (n=1,364), 2–10 (n=186), 10–100 (n=193),
    100–500 (n=93), 500–2500 (n=84), 2500–60000 (n=372)**. Ligands with >100 analogous training
    systems are "prevalent"; the rest are "distinct".
  - **Redundancy stratum**: community clustering of the graph of systems with SuCOS-pocket > 50,
    giving **1,017 clusters, 789 in the common subset**, representative = lowest training similarity
    (p7, p21).
- **anti_memorization_control**: **RUN, analysed, and the analysis is the paper's result — not a
  held-out set that merely exists.** Six distinct control arms were executed on the post-cutoff set:
  1. **Similarity-stratified accuracy for all four methods** (Fig 1A–E, p4) — the primary arm.
     Success rate rises monotonically from ~8–25% in the 0–20 bin to 81–89% in the 80–100 bin.
  2. **Success-definition control** — the same stratification with success defined by RMSD < 2 Å
     alone (Fig 1B, p3–4), confirming "our success rate criteria do not influence the observed
     trend of limited generalisation" (p3).
  3. **Later-cutoff control** — Boltz-2 (cutoff 1 Jun 2023, ~25k additional PDB entries) evaluated
     on its *own* post-cutoff systems with similarity recomputed against its own cutoff, versus
     Boltz-1 on the same systems with 2021-cutoff similarity (Fig 2A, p5–6). Result: "the additional
     data used for training (over 25k PDB entries) increases the number of cases in the higher
     similarity bins but does not seem to help with generalisation to unseen data" (p5).
  4. **Prevalence control** — removing prevalent ligands (>100 analogous training systems) and
     re-running the stratification (Fig 3B, p6–7), showing "the successes in the lower similarity
     bins are primarily due to such cases".
  5. **Redundancy control** — cluster representatives only (Fig 3C, p7), verifying "the observed
     trend is not driven by an over-representation of certain protein families".
  6. **Alternative-similarity control** — pli_qcov instead of SuCOS-pocket (Supplementary Fig S3L,
     p20–21, p30), "gave similar results".
  **Power.** The primary arm is well powered at every stratum: the smallest bin is n=64 and all
  eight bins carry 1,000-sample bootstrap 95% CIs (Fig 1 caption, p4). **Not** marked `UNPOWERED`
  overall. Three sub-arms are thin in their lowest bins and their low-similarity conclusions should
  be treated as indicative only: the **Boltz-2 arm** (0–20 bin n=30 for Boltz-1, m=21 for Boltz-2;
  20–30 bin n=34/m=28 — Fig 2A axis, p6), the **cluster-representative arm** (0–20 bin n=37, 70–80
  bin n=50 — Fig 3C axis, p7), and the **distinct-ligand arm** (0–20 bin n=51 — Fig 3B axis, p7).
  None falls below n≈10, so the schema's `UNPOWERED` threshold is not tripped. The authors flag the
  same risk forward in time: "there is a significant decrease of cases in the more difficult bins,
  lowering the capability to perform granular and confident analysis of memorisation and
  generalisability" (p6).
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Success defined by RMSD < 2 Å alone (Fig 1B) | that the trend is an artefact of the dual RMSD + LDDT-PLI predicate | p3, p4 |
  | PoseBusters physical-validity overlay (Fig 1E) | that counted "successes" are physically invalid poses | p5, p4 |
  | AF3 with templates vs AF3-NT without (Supplementary Fig S1) | template-derived structural leakage or template-derived advantage | p5, p17, p27 |
  | Boltz-1x arm (Supplementary Fig S1) | that PoseBusters failures are intrinsic to the Boltz architecture (Boltz-1x passes all min-distance checks with no success-rate change) | p5, p27 |
  | RoseTTAFold-All-Atom arm (Supplementary Fig S1) | that the trend is specific to AF3-family architectures — caveated, 1 model not 25, "not directly comparable" | p5, p27 |
  | Boltz-2 (2023 cutoff) vs Boltz-1 on post-2023 systems (Fig 2A) | that two more years of PDB training data fixes generalisation | p5, p6 |
  | Systems-available-per-cutoff curve (Fig 2B) | that the benchmark is exhausted by later cutoffs; quantifies remaining difficult-bin counts | p5–6, p6 |
  | Prevalent-ligand removal, distinct ligands only (Fig 3B) | that low-bin successes are cofactor / amino-acid / nucleotide analogs | p6, p7 |
  | Cluster-representatives only (Fig 3C) | protein-family over-representation and congeneric-series redundancy driving the trend | p7 |
  | Rotatable-bond and molecular-weight stratification (S3A–B) | ligand-size bias | p7, p30 |
  | Binding-pocket-size stratification (S3C–H) | pocket-size bias | p7, p30 |
  | Single-ligand / multi-ligand / multi-protein subsets (S3I–K) | multi-chain or multi-ligand complexity as the driver | p7–8, p30 |
  | pli_qcov as the similarity metric instead of SuCOS-pocket (S3L) | that the trend is an artefact of the SuCOS-pocket definition | p20–21, p30 |
  | Pocket-recovery F1 across bins (Fig 4E) | "the model found the wrong pocket" as the failure mode | p8, p9 |
  | LDDT-LP across bins (Fig 4F) | protein/pocket mis-modelling as the failure mode | p8, p9 |
  | Sequence-identity and fingerprint similarity vs SuCOS-pocket (Fig 4A–B) | that a 40% sequence-identity or 85% Morgan-Tanimoto threshold suffices to detect leakage | p8, p9 |
  | Identical MSAs supplied to all four methods | MSA depth/quality differences as the source of between-method differences | p17 |
  | Best-scored / worst-scored / random / top-ranked across 25 models (Fig 6A–D) | conflation of *sampling* failure with *ranking* failure | p11, p12 |
  | 1 seed vs 5 seeds (Fig 6A–D) | that multi-seed sampling helps at inference | p11, p12 |
  | Balanced 250 positive / 250 negative per bin for iPTM classification (Fig 6E) | class imbalance across similarity bins inflating classification accuracy | p13, p12 |
  | Ligand-protein vs protein-ligand chain-pair iPTM (Fig 6F) | that the asymmetric iPTM matrix direction is immaterial for Boltz-1/Chai-1 | p13, p12 |
  | SuCOS-pocket audit of the PoseBusters benchmark (87% > 50) | that the incumbent benchmark is itself leakage-free | p14 |

- **confidence_as_discriminator**: **yes, used and explicitly validated — and found wanting.** Two
  separate uses, both audited:
  1. **Ranking.** The 25 models per system are ranked by the ligand-protein chain-pair iPTM score,
     "calculated as the average of chain pair iPTM scores across all protein chains to the
     considered ligand chain" (p11); "using the default ranking score showed very similar results"
     (p17). Validated against the best/worst/random oracle curves (Fig 6A–D): "While the top-ranked
     model is better than the worst-scored model generated (black vs. red), there is still a gap to
     the best possible model (in blue) and it is usually not much better than random selection (in
     green)" (p11).
  2. **Success classification.** Per-method iPTM thresholds fitted at the ROC-AUC optimal operating
     point (p11): AF3 **0.92**, Protenix **0.99**, Chai-1 **0.75**, Boltz-1 **0.95**; for the
     protein-ligand direction, Chai-1 **0.60**, Boltz-1 **0.53** (Fig 6F, p12). Accuracy by bin,
     class-balanced 250/250: Boltz-1 **70–90%**, the other three **below 75%** (p13). "Overall, the
     iPTM-based accuracy does not seem to correlate with the training set similarity" (p13) — i.e.
     confidence does not know when it is memorising.
  **Caveat carried from `oracle_leakage` route 4:** those thresholds are fitted on the same
  predictions whose classification accuracy is then reported, so the accuracies are in-sample.
  The paper's own verdict, p11: "previously established TM-score thresholds cannot be used for
  model selection, and the confidence scores are not comparable across the four methods."

## D. Claims

- **central_conclusion**: On 2,600 post-training-cutoff, high-resolution protein–ligand complexes,
  the accuracy of all four leading all-atom co-folding methods rises monotonically with how similar
  the complex is to their training data — from roughly 8–25% success in the least-similar stratum to
  81–89% in the most-similar — and the trend survives every stratification the authors could apply
  (success definition, ligand prevalence, cluster redundancy, ligand size, pocket size, system
  composition, similarity metric). Proteins and pockets are modelled well everywhere; it is the
  ligand pose in a familiar pocket that fails. Two more years of training data (Boltz-2) does not
  flatten the curve, confidence scores do not detect the failure, and the incumbent thresholds
  (40% sequence identity, 85% Morgan Tanimoto) and the incumbent benchmark (PoseBusters, 87% of it
  above SuCOS-pocket 50) are not sensitive enough to have revealed any of this.
- **necessity_claims** — verbatim, with pages:
  - p1 (Abstract): "We demonstrate that current cofolding approaches largely memorise ligand poses
    from their training data, hindering their use for de novo drug design."
  - p3: "We explore the impact of training data similarity on prediction accuracy, revealing a
    critical limitation: current cofolding methods struggle to generalise beyond ligand poses seen
    in their training data."
  - p13: "Overall, our benchmark shows that the current generation of deep learning cofolding
    methods still have a long way to go to accurately model unseen protein-ligand complexes."
  - p13: "We demonstrate that the performance of current approaches strongly correlates with the
    similarity to their training data, regardless of the metric used to define success or the
    subsets considered."
  - p13: "In cases where the prediction was not accurate, the correct pose is either not sampled at
    all or, when it is, the method fails to select it during ranking, further highlighting the need
    for improvement in both aspects."
  - p10: "Although Figure 5 provides some useful visual cues on when these current methods are
    likely to perform well, it also paints a clear picture of their inherent limitations in
    generating accurate predictions for drug-like molecules beyond the training data."
  - p8: "We conclude that previous similarity metrics and thresholds used for validating cofolding
    methods' performance are insufficient to detect data leakage for the PLI prediction task."
  - p8: "The commonly used 40% sequence identity threshold misses numerous cases of proteins from
    the same family sharing the same fold, pocket and binding mode, and 85% Morgan fingerprint
    similarity threshold (used for validation of AlphaFold3 [22]) misses cases of ligands binding
    with highly similar poses to highly similar proteins and pockets."
  - p11: "Nevertheless, sampling the correct pose continues to be the main bottleneck in improving
    the accuracy, since even the best-scored poses do not flatten the curve."
  - p11: "Additionally, we observe that using multiple seeds is currently not useful at inference
    time for any of the methods."
  - p11: "Thus, previously established TM-score thresholds cannot be used for model selection, and
    the confidence scores are not comparable across the four methods."
  - p14: "For example, the generalisability of Boltz-2 did not discernibly improve compared to
    Boltz-1, despite being trained on more data (Figure 2)."
  - p14: "Incorporating physics-based terms to more accurately model protein-ligand interactions,
    potentially from simulations, conformational ensembles, or other sources, are likely needed to
    achieve more exciting results in this field."
  - p14: "This highlights the need to integrate robust physical and chemical priors to enhance
    method generalisation."
  - p14: "We observed that most released high-quality complexes have a high similarity to the
    training set (Figure 1, 75% system ligands have >50 SuCOS-pocket similarity), demonstrating that
    difficult test systems consisting of novel molecules or binding pockets, both highly relevant to
    drug discovery and design, are underrepresented in general, and the commonly-used time split
    approaches would not capture these."
  - p14: "In fact, 87% of the complexes in the commonly used PoseBusters benchmark dataset [19] have
    a SuCOS-pocket similarity >50 to the training set, explaining the high performance scores
    typically obtained by these methods on this set."
  - p15: "We note that the only requirement to apply the Runs N' Poses benchmark in its entirety on
    a new method is a structural training cutoff of 30 September 2021."
  - p2: "Therefore, to achieve accurate predictions of how ligands bind and their binding affinity,
    a deep understanding of the fundamental principles governing PLIs is essential [4]."
  - **Important counter-nuance the authors state themselves, p8** — do not quote the memorisation
    claim without it: "Thus, the trend that we observe is not a case of lack of out-of-distribution
    (OOD) generalisation for lesser-studied proteins or novel pockets and more likely arises from
    other factors, such as the difficulty in generalising to unseen ligand poses within otherwise
    familiar pockets." Supported on the same page by: "already from the third bin (SuCOS-pocket
    similarity between 30 and 40) we see that the protein and pocket of a test system share more
    than 60% sequence identity and 80% pocket coverage to the closest training system on average"
    and "finding the correct pocket does not seem to be the limiting factor for the inaccurate
    complex predictions."
  - p8: "these results do not guarantee that the predicted protein models could be used for
    downstream docking applications, as previous studies showed that even LDDT-LP values higher
    than 0.9 do not detect atom-level conformational changes which lead to unsuccessful rigid
    docking [18]."
- **novelty_claims** — verbatim, with pages. **The paper makes no explicit "first" or
  "unprecedented" claim anywhere**; its novelty language is "newly introduced", "we present",
  "we provide", "we demonstrate the pitfalls":
  - p1 (Abstract): "Here we present a comprehensive evaluation of four leading all-atom cofolding
    methods using our newly introduced benchmark dataset Runs N' Poses, which comprises 2,600
    high-resolution protein-ligand systems released after the training cutoff used by these
    methods."
  - p3: "To address this, we present a comprehensive benchmark of four leading all-atom cofolding
    deep learning methods with highly similar architectures and training paradigms (AlphaFold3 [22],
    Chai-1 [23], Protenix [25], and Boltz-1 [24]) on 2,600 high-resolution PLI systems released
    after their training cutoff (30 September 2021)."
  - p3: "We provide a benchmark dataset (Runs N' Poses) with varying degrees of training set
    similarity, along with resources to analyse the relationship between data leakage and
    performance."
  - p3: "With this work, we aim to facilitate progress and enable identification of genuine
    breakthroughs in the critical field of protein-ligand complex prediction."
  - p1 (Abstract): "With this assessment and benchmark dataset, we aim to accelerate progress in the
    field by allowing for a more realistic assessment of the current state-of-the-art deep learning
    methods for predicting protein-ligand interactions."
  - p14: "In fact, out of the four benchmarked methods only the authors of Protenix list memorisation
    artifacts as an expected limitation, further underscoring the difficulty in uncovering such
    biases without extensive benchmarking combining measures of prediction performance with measures
    of data leakage."
  - p14: "We demonstrate the pitfalls of commonly used similarity thresholds such as 40% sequence
    identity, proving them to be insufficient to assess method generalisation."
  - p20 (methodological novelty of the metric): "In addition, the Combined Overlap Score (SuCOS),
    which measures the overlap of volume and chemical features between two ligand poses, has been
    shown to better differentiate binding pose similarity compared to RMSD and PLI-based scores
    [30]. Thus, we calculated three more metrics working in concert with the protein-based scores."
- **stated_limits** — the authors are unusually forthcoming:
  - p20: "Despite our best efforts, we cannot be sure that we are always able to accurately calculate
    similarity to the training set, as our methods rely on a combination of alignment and
    superposition which may fail in edge cases."
  - p20: "we only search for similarity against PLI systems, excluding only-artifact systems and
    those with oligopeptides, oligosaccharides or oligonucleotides over 10 in length, thus
    potentially missing cases of training set proteins complexed with oligo, protein or nucleotide
    chains which resemble small molecule binding." (i.e. leakage may be **under**-estimated; they
    add "However, this latter similarity would indicate transfer of binding modes from different
    modalities and perhaps may not be considered memorisation.")
  - p15: "As the dataset was constructed in an automated fashion, there may be a few complexes which
    do not qualify as biologically relevant."
  - p5: "RoseTTAFold-All-Atom has a different architecture and was run with only 1 model output
    instead of 25 and thus is not directly comparable."
  - p5: Boltz-2 "was trained with a cutoff of 2023-06-01, thus using a full two years more PDB data
    than the other methods. While this makes the new method not directly comparable to the others
    presented in this manuscript, it can still be assessed using the similarity to the training set."
  - p17: "For some systems, the SMILES for the ligand in the PDB does not contain chiral information
    while the ground truth has at least one chiral center, i.e the molecule given as input to each
    cofolding method may not be the molecule expected as the output. This is not a straightforward
    issue to fix in an automated fashion."
  - p17: "We did not manage to obtain prediction results from all methods across all 2,600 systems
    in the dataset. Some systems (128) failed to produce output across all four methods."
  - p16: 21 nucleic-acid-containing systems dropped "due to the scarce numbers"; p16–17: 72 system
    ligands from 63 systems dropped as unreadable by RDKit.
  - p6: "there is a significant decrease of cases in the more difficult bins, lowering the capability
    to perform granular and confident analysis of memorisation and generalisability."
  - p14 (missing baseline, acknowledged): "In future work, we aim to include template-based and
    physics-based docking baselines, using similar systems from before the training cutoff as
    templates for homology modelling."
  - p14 (analysis not done): "it would also be interesting to disentangle these two aspects and
    inspect how much these methods make use of simple volume overlap over chemical similarity."
  - p8: LDDT-LP > 0.9 does not guarantee usability for downstream rigid docking.
  - p20: combined protein-and-pocket superposition approaches "turned out to be too sensitive to the
    efficacy of rigid protein superposition" and were abandoned.
- **stance**: **provisional, the user's call** — `precedent` + `threat`.
  - **precedent on methodology.** This is the corpus's reference implementation of an
    anti-memorisation design: a genuine post-cutoff set with n given at every level, per-complex
    similarity annotation to the training set, ordinal strata with bootstrap CIs, and a dozen
    stratification controls. Any anti-memorisation claim we make should be measured against this
    construction, and its similarity metric (SuCOS-pocket) is the thing to adopt or explicitly
    reject.
  - **threat on findings.** The central result — that co-folding accuracy is a monotone function of
    training-set similarity and that confidence scores do not detect the difference — undercuts any
    claim that a co-folding backbone has learned generalisable physics rather than recall, and
    therefore undercuts downstream conformational or pose claims built on those backbones without a
    similarity-stratified control of their own. p14's audit of PoseBusters (87% above SuCOS-pocket
    50) is directly a threat to any number quoted from that benchmark.
  - Not `contrast`: the paper's own rigour is high and the one un-declared leakage route (in-sample
    iPTM threshold, route 4) affects a single supporting panel, not the central claim.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Success rate (RMSD < 2 Å & LDDT-PLI > 0.8), AlphaFold3, by SuCOS-pocket bin 0–20 / 20–30 / 30–40 / 40–50 / 50–60 / 60–70 / 70–80 / 80–100 | 25 / 25 / 28 / 43 / 55 / 67 / 75 / 89 | % of system ligands | deposited post-cutoff X-ray reference; common subset, top-ranked model | p4 (Fig 1E printed bar labels) |
  | Same, Protenix | 8 / 11 / 18 / 27 / 43 / 59 / 66 / 86 | % | as above | p4 (Fig 1E) |
  | Same, Chai-1 | 9 / 18 / 13 / 30 / 45 / 59 / 71 / 85 | % | as above | p4 (Fig 1E) |
  | Same, Boltz-1 | 14 / 8 / 24 / 36 / 45 / 55 / 68 / 81 | % | as above | p4 (Fig 1E) |
  | Same, additionally PB-Valid — AF3 / Protenix / Chai-1 / Boltz-1 in the 80–100 bin | 70 / 74 / 72 / 60 | % | as above + all PoseBusters "dock" checks | p4 (Fig 1E) |
  | Same, additionally PB-Valid, in the 0–20 bin | 12 / 6 / 9 / 6 | % | as above | p4 (Fig 1E) |
  | Oracle "Best of four top-ranked" success rate, 0–20 bin → 80–100 bin | ~30 → ~97 | % | reference; **oracle selection, not achievable** | p4 (Fig 1A, read from panel) |
  | Success rate, RMSD < 2 Å only, AF3, 0–20 bin → 80–100 bin | ~29 → ~92 | % | reference | p4 (Fig 1B, read from panel) |
  | n per similarity bin, common subset proper ligands (0–20 … 80–100) | 64 / 91 / 149 / 258 / 312 / 376 / 368 / 673 | ligands | — | p4 (Fig 1 axis) |
  | Share of post-cutoff system ligands with SuCOS-pocket similarity > 50 to training set | 75 | % | Runs N' Poses itself | p14 |
  | Share of PoseBusters benchmark complexes with SuCOS-pocket similarity > 50 to training set | 87 | % | PoseBusters benchmark [19] | p14 |
  | Predictions failing the PoseBusters minimum-distance-to-protein check | 22.6 | % of predicted models, across four methods | PoseBusters "dock" checks | p5 |
  | Predictions passing all remaining PoseBusters checks | > 95 | % of predicted models | as above | p5 |
  | Predictions with LDDT-PLI > 0.8 but RMSD > 2 Å ("top-right" outliers) | 1.6 | % of 229,887 predictions | reference | p19 |
  | Predictions with RMSD < 2 Å but LDDT-PLI < 0.8 ("bottom-left" outliers) | 8.3 | % of 229,887 predictions | reference | p19 |
  | Systems with LDDT-LP > 0.8, all systems: AF3 / Protenix / Chai-1 / Boltz-1 | 92 / 91 / 90 / 91 | % | reference pocket | p9 (Fig 4 caption) |
  | Systems with LDDT-LP > 0.8, cluster representatives only | 87 / 83 / 82 / 83 | % | reference pocket | p9 (Fig 4 caption) |
  | Mean sequence identity and pocket coverage to closest training system, from the 30–40 bin upward | > 60 seq. id., > 80 pocket coverage | % | closest training system | p8 |
  | ROC-optimal ligand-protein chain-pair iPTM threshold: AF3 / Protenix / Chai-1 / Boltz-1 | 0.92 / 0.99 / 0.75 / 0.95 | iPTM | fitted in-sample on the evaluation set | p11 |
  | ROC-optimal protein-ligand chain-pair iPTM threshold: Chai-1 / Boltz-1 | 0.60 / 0.53 | iPTM | fitted in-sample | p12 (Fig 6F legend) |
  | iPTM-based success-classification accuracy across bins: Boltz-1 vs the other three | 70–90 vs < 75 | % (class-balanced 250 pos / 250 neg per bin) | reference-derived labels; in-sample threshold | p13 |
  | Boltz-1 (2021 cutoff) success rate, 0–20 → 80–100 bin | ~17 → ~85 | % | reference | p6 (Fig 2A, read from panel) |
  | Boltz-2 (2023 cutoff) success rate, 0–20 → 80–100 bin | ~9 → ~90 | % | reference | p6 (Fig 2A, read from panel) |
  | n / m per bin in the Boltz-1 vs Boltz-2 arm (0–20 … 80–100) | n = 30/34/46/67/118/151/154/284; m = 21/28/41/60/95/159/160/320 | system ligands | — | p6 (Fig 2A axis) |
  | Runs N' Poses systems remaining as the cutoff advances Q1 2021 → Q4 2023 | 2,579 → 707 total; 707 → 129 with similarity < 50 | systems | PDB release date | p6 (Fig 2B labels) |
  | Success rate vs number of analogous training systems (0–2 … 2500–60000), AF3 | ~62 / ~55 / ~53 / ~74 / ~70 / ~81 | % | reference | p7 (Fig 3A, read from panel) |
  | n per prevalence level (0–2 / 2–10 / 10–100 / 100–500 / 500–2500 / 2500–60000) | 1,364 / 186 / 193 / 93 / 84 / 372 | system ligands | — | p7 (Fig 3A axis) |
  | n per similarity bin, distinct ligands only (Fig 3B) | 51 / 79 / 132 / 233 / 269 / 315 / 276 / 387 | system ligands | — | p7 (Fig 3B axis) |
  | n per similarity bin, clustered + distinct (Fig 3C) | 37 / 55 / 89 / 109 / 88 / 83 / 50 / 58 | cluster representatives | — | p7 (Fig 3C axis) |
  | Redundancy clusters | 789 in common subset out of 1,017 total | clusters | SuCOS-pocket > 50 community clustering | p7 |
  | Largest clusters (top 3) | 171 (SARS-CoV-2 3CLpro, rep. 7EN9), 136 (SIK3, rep. 8OKU), 100 (PDE10, rep. 5SH0) | systems | — | p28 (Table S1) |
  | Total predictions analysed, common subset | 229,887 | predicted models | — | p18 |

- **n_predictions**: recorded at each level, per the schema.
  - **Samples per target per method: 25** — "5 seeds and 5 diffusion samples per seed, which
    resulted in a total of 25 models per system for each method" (p17). Exception: **RFAA = 1**
    model per system (p5).
  - **Targets: 2,600 systems / 3,047 proper ligands** in the full post-2021 set; **2,077 systems /
    2,311 proper ligands** in the four-method common subset; **1,028 systems / 1,187 proper ligands**
    in the post-2023 set (Table 1, p18).
  - **Total: 229,887 predictions** across the four primary methods in the common-subset analysis
    (p18). Predictions from AF3-NT, Boltz-1x, Boltz-2 and RFAA are additional and not included in
    that figure.
  - Bootstrap resampling: **1,000 samples per bin per method** for all CIs (Fig 1, Fig 3 captions,
    p4, p7); **1,000 bootstrap estimates** for Fig 6E/F (p12).
- **comparable_to_ours**:
- **si_in_scope**: **Partially held.** Supplementary Figures S1–S4 and Supplementary Table S1 **are
  in this PDF** (pp. 27–31) with full captions and rendered panels, so the stratification controls
  (S1 all-predictions arms including AF3-NT/Boltz-1x/RFAA; S2 prevalent-ligand distribution; S3A–L
  the twelve robustness stratifications; S4 example molecules per bin; Table S1 the ten largest
  clusters) are all readable. **SI NOT HELD** for the underlying data: the per-system similarity CSV,
  the all-PDB-to-2024-06-05 similarity Parquet, all prediction CIFs, and the per-model accuracy and
  confidence CSVs live at Zenodo `10.5281/zenodo.14794785`, GitHub `plinder-org/runs-n-poses`,
  Polaris Hub and ModelArchive `ma-rnp` (p15) — none of which the corpus holds. Consequence: every
  per-bin curve value in `metrics_reported` that is not a printed bar label had to be read off a
  rendered panel; the exact numbers exist but are outside the PDF.

## F. Figures

22 panel-group rows (15 main-text, 7 supplementary). Pages 4, 6, 7, 9, 10, 12 and 19 were rendered
because the captions do not carry bin counts, series counts or axis ranges.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A-B | 4 | Success rate rises monotonically with training-set similarity for all four methods, under two different success definitions | line | `PLOT \| facet: success definition (2: RMSD<2Å & LDDT-PLI>0.8; RMSD<2Å only) \| vary: SuCOS-pocket similarity bin (8: 0-20…80-100) \| series: method (5: AlphaFold3, Protenix, Chai-1, Boltz-1, Best-of-four) \| measure: success rate (%), compound over the two definitions \| mark: line \| n: 64/91/149/258/312/376/368/673 system ligands per bin per series; 2,291 per panel` | 2 panels, varying by success definition | Per-method n is not shown — the printed bin n is the pooled common-subset count and each method's own count differs (Table 1, p18); the gray "Best" line is an oracle selection and is drawn identically to the four achievable curves with no visual marking | CC-BY 4.0 International, no ND clause — declared in the banner on every page, e.g. p1 |
| 1C-D | 4 | Distributions of LDDT-PLI and of RMSD shift with similarity bin | violin | `PLOT \| facet: metric (2: LDDT-PLI, RMSD) \| vary: SuCOS-pocket similarity bin (8) \| series: method (4) \| measure: LDDT-PLI (0-1) and RMSD (Å, log 0.1-100), compound \| mark: violin (pooled over methods) + point (per method) \| n: per-bin totals as 1A-B; per-mark 1 point per prediction, per-method n per bin NOT REPORTED` | 2 panels, varying by metric | The violin is pooled across all four methods while the scatter is coloured per method, so the shape shown is not any method's distribution; median/mean glyphs are drawn for the pooled violin only | CC-BY 4.0, no ND — p1 |
| 1E | 4 | The same success rate split into PB-Valid and not, per method per bin | bar | `PLOT \| facet: none (1) \| vary: SuCOS-pocket similarity bin (8) \| series: method (4) × validity (2: striped = RMSD/LDDT-PLI only, solid = also PB-Valid) \| measure: success rate (%) \| mark: bar \| n: 64/91/149/258/312/376/368/673 per bin; 32 bars per panel` | 1 panel, 8 bin groups × 4 methods × 2 nested bars | Bars carry **no confidence interval** although panel A of the same figure shows 1,000-sample bootstrap CIs for the identical quantity; nested striped/solid bars encode a subset relationship that reads as two independent series | CC-BY 4.0, no ND — p1 |
| 2A | 6 | Boltz-2's extra two years of training data shift the bin populations but not the slope | line | `PLOT \| facet: none (1) \| vary: SuCOS-pocket similarity bin (8) \| series: model × cutoff (2: Boltz-1 @2021, Boltz-2 @2023) \| measure: success rate (%) \| mark: line \| n: Boltz-1 30/34/46/67/118/151/154/284; Boltz-2 21/28/41/60/95/159/160/320 per bin` | 1 panel, 2 series | The two curves are computed against **different similarity annotations** (2021 cutoff for Boltz-1, 2023 for Boltz-2), so the shared x-axis is not the same variable for both series; the caption says so but the plot does not | CC-BY 4.0, no ND — p1 |
| 2B | 6 | How many benchmark systems, and how many hard ones, survive as the cutoff advances | stacked area | `PLOT \| facet: none (1) \| vary: training cutoff date, Q1 2021 – Q4 2023 (continuous, 12 quarters) \| series: SuCOS-pocket similarity bin (8) \| measure: number of systems \| mark: stacked area \| n: 1 stack per quarter; totals 2,579 → 707 per panel` | 1 panel | | CC-BY 4.0, no ND — p1 |
| 3A | 7 | Success rate against how many training systems contain an analogous ligand | line | `PLOT \| facet: none (1) \| vary: no. of training systems with analogous ligand (6: 0-2, 2-10, 10-100, 100-500, 500-2500, 2500-60000) \| series: method (5, incl. Best-of-four) \| measure: success rate (%) \| mark: line \| n: 1,364/186/193/93/84/372 system ligands per level` | 1 panel | The six levels are unequal, roughly logarithmic bins plotted at equal spacing, which linearises a log relationship; the 0–2 level holds 60% of the data and is drawn the same width as the 84-ligand level | CC-BY 4.0, no ND — p1 |
| 3B-C | 7 | The similarity trend survives removing prevalent ligands, and survives clustering away redundancy | line | `PLOT \| facet: subset (2: distinct ligands only; cluster representatives of distinct ligands) \| vary: SuCOS-pocket similarity bin (8) \| series: method (5, incl. Best-of-four) \| measure: success rate (%) \| mark: line \| n: B 51/79/132/233/269/315/276/387; C 37/55/89/109/88/83/50/58` | 2 panels, varying by subset | Panel C's lowest bins (n=37, and n=50 in 70–80) carry visibly wide bootstrap bands that overlap most of the y-range, so the monotone reading of C rests on the mid bins | CC-BY 4.0, no ND — p1 |
| 4A-B | 9 | How sequence identity, pocket coverage and three ligand-similarity metrics track the SuCOS-pocket bin, versus the thresholds AF3 used for validation | violin | `PLOT \| facet: similarity family (2: protein-side; ligand-side) \| vary: SuCOS-pocket similarity bin (8) \| series: similarity metric (2 in A: protein sequence identity, pocket coverage; 3 in B: topological fingerprint Tanimoto, Morgan fingerprint Tanimoto r=2 nbits=2048, ligand SuCOS) \| measure: metric value (%) \| mark: violin + point \| n: 64/91/149/258/312/376/368/674 per bin` | 2 panels, varying by similarity family | The top bin is labelled n=674 here and n=673 in Fig 1 for what should be the same set; the two AF3 validation thresholds are drawn as dashed lines with no count of how many systems fall on the wrong side of them, which is the panel's actual claim | CC-BY 4.0, no ND — p1 |
| 4C-D | 9 | Two worked counterexamples: high SuCOS-pocket similarity at low sequence identity (26%) and at low Morgan similarity (29%) | structure render | `RENDER \| facet: counterexample type (2: low seq. id.; low Morgan similarity) \| views: 1 \| overlay: 0 predictions on 1 reference — ground truth and closest training system shown side by side, not superposed \| axis: none` | 2 panels, each with 2 sub-renders (ground truth, training system) | Two hand-picked examples support a distributional claim; the selection criterion beyond "low X, high SuCOS-pocket" is not stated | CC-BY 4.0, no ND — p1 |
| 4E-F | 9 | Pocket recovery and pocket geometry are already good in the lowest bins, so neither is the failure mode | violin | `PLOT \| facet: pocket metric (2: pocket-recovery F1; LDDT-LP) \| vary: SuCOS-pocket similarity bin (8) \| series: method (4) \| measure: pocket F1 (0-1) and LDDT-LP (0-1), compound \| mark: violin (pooled) + point (per method) \| n: 64/91/149/258/312/376/368/674 per bin; per-method n per bin NOT REPORTED` | 2 panels, varying by pocket metric; the caption mislabels panel F as a second "D" | Same pooled-violin/per-method-scatter mismatch as 1C-D; both metrics sit at ceiling from the mid bins on, so the panels cannot discriminate there | CC-BY 4.0, no ND — p1 |
| 5 | 10 | One failed and one successful AF3 prediction from each of four similarity bins, each against ground truth and against the closest training system | structure render | `RENDER \| facet: similarity bin (4: 0-20, 30-40, 40-60, 80-90) × outcome (2: incorrect, correct) \| views: 3 (ground truth, AlphaFold3 prediction, closest training system) \| overlay: 0 predictions on 1 reference — the three structures are shown side by side, not superposed \| axis: none` | 8 panels A–H, 3 renders each; the caption lists them as "A-B, C-D, E-F and F-G", which is a typo — F appears twice and H is never named | One AF3 model out of 25 is shown per cell with the selection rule unstated — `1 of 25 (selection criterion NOT REPORTED)`; the other three methods are never rendered although the chirality claim on p10 is made for "all the methods" | CC-BY 4.0, no ND — p1 |
| 6A-D | 12 | Best-scored, worst-scored, random and top-ranked models across 25, and across 1 vs 5 seeds, per method | line | `PLOT \| facet: method (4: AlphaFold3, Protenix, Chai-1, Boltz-1) \| vary: SuCOS-pocket similarity bin (8) \| series: model-selection strategy (7: random/5 seeds, best-scored/5, worst-scored/5, top-ranked/5, top-ranked/1, random/1, best-scored/1) \| measure: success rate (%) \| mark: line \| n: AF3 90/118/163/289/342/419/417/791; Protenix 82/107/156/283/336/408/408/753; Chai-1 75/102/156/277/333/408/405/741; Boltz-1 65/94/149/261/314/378/374/675` | 4 panels, varying by method | The 1-seed series carry standard-deviation whiskers while the 5-seed series carry none, so the two cannot be compared for spread; four of the seven series overlap almost exactly, which is the panel's finding but is hard to read at this line density | CC-BY 4.0, no ND — p1 |
| 6E-F | 12 | iPTM-threshold classification accuracy does not track similarity, and Boltz-1's confidence is the only useful one | line | `PLOT \| facet: iPTM direction (2: ligand-protein chain pair; protein-ligand chain pair) \| vary: SuCOS-pocket similarity bin (8) \| series: method (4 in E; 2 in F: Chai-1, Boltz-1) \| measure: iPTM-based classification accuracy (%) \| mark: line \| n: 250 positive + 250 negative sampled per bin per method; 1,000 bootstrap estimates` | 2 panels, varying by iPTM direction | **Y-axis truncated at 50%, not 0** in both panels, which triples the apparent separation between Boltz-1 and the rest; 50% is also chance for a balanced two-class problem, so the truncation happens to hide how close three of the four methods sit to chance | CC-BY 4.0, no ND — p1 |
| 7A | 19 | Joint distribution of RMSD and LDDT-PLI over all 229,887 predictions, justifying the dual success predicate | scatter | `PLOT \| facet: none (1) \| vary: LDDT-PLI, 0-1 (continuous) \| series: method (4) \| measure: binding-site-superposed RMSD, 0.1-100 Å (log) \| mark: point \| n: 1 per mark; 229,887 per panel` | 1 panel | Massive overplotting with no density encoding or colour bar, so the 1.6% and 8.3% corner populations quoted in the text cannot be read off the plot; the four method colours are indistinguishable in the dense band | CC-BY 4.0, no ND — p1 |
| 7B-C | 19 | Two worked outliers: high RMSD with high LDDT-PLI (8W0J, 3.72 Å / 0.86) and low RMSD with low LDDT-PLI (8EBC, 1.63 Å / 0.43) | structure render | `RENDER \| facet: outlier type (2: high-RMSD/high-LDDT-PLI; low-RMSD/low-LDDT-PLI) \| views: 1 \| overlay: 1 prediction on 1 reference (prediction blue, ground truth gray) \| axis: none` | 2 panels, varying by outlier type | | CC-BY 4.0, no ND — p1 |
| S1A-B | 27 | Fig 1A-B repeated on all predictions rather than the common subset, adding AF3-NT, Boltz-1x and RFAA | line | `PLOT \| facet: success definition (2: RMSD<2Å & LDDT-PLI>0.8; RMSD<2Å only) \| vary: SuCOS-pocket similarity bin (8) \| series: method (8: AlphaFold3, AF3-NT, Protenix, Chai-1, Boltz-1, Boltz-1x, RFAA, Best) \| measure: success rate (%) \| mark: line \| n: per-method per-bin counts NOT REPORTED in caption; per-method totals in Table 1, p18` | 2 panels, varying by success definition | Per-bin n is not given for any of the eight series, so the arms with the fewest predictions (RFAA, 1,946 proper ligands) are indistinguishable in weight from AF3's 2,710 | CC-BY 4.0, no ND — p27 |
| S1C-D | 27 | LDDT-PLI and RMSD distributions on all predictions | violin | `PLOT \| facet: metric (2: LDDT-PLI, RMSD) \| vary: SuCOS-pocket similarity bin (8) \| series: method (8) \| measure: LDDT-PLI (0-1) and RMSD (Å, log), compound \| mark: violin (pooled) + point (per method) \| n: NOT REPORTED per bin` | 2 panels, varying by metric | Pooled violin over eight heterogeneous arms including RFAA, which produced 1 model not 25 | CC-BY 4.0, no ND — p27 |
| S1E | 27 | PB-Valid overlay on all predictions | bar | `PLOT \| facet: none (1) \| vary: SuCOS-pocket similarity bin (8) \| series: method (7) × validity (2: striped, solid) \| measure: success rate (%) \| mark: bar \| n: NOT REPORTED per bin` | 1 panel | No CIs, as in Fig 1E; no per-bin n | CC-BY 4.0, no ND — p27 |
| S2-plot | 29 | What fraction of test ligands have how many analogous training systems | bar | `PLOT \| facet: none (1) \| vary: number of training systems with analogous ligands (continuous, log scale) \| series: none (1) \| measure: percentage of system ligands (%) \| mark: bar \| n: 3,047 proper ligands per panel (2,291 with similarity scores)` | 1 panel | | CC-BY 4.0, no ND — p29 |
| S2-mols | 29 | The chemical structures of every ligand classified as prevalent (>100 analogous training systems) | schematic | `SCHEMATIC \| 2D chemical structures of all ligands in systems with >100 analogous ligand training systems \| no data` | 1 grid panel, count of molecules NOT REPORTED | | CC-BY 4.0, no ND — p29 |
| S3A-L | 30 | Twelve robustness stratifications: rotatable bonds, MW, pocket size, five pocket-size strata, single/multi-ligand/multi-protein subsets, and pli_qcov as the similarity metric | line | `PLOT \| facet: stratification (12: A rotatable bonds, B molecular weight, C pocket residue count, D-H pocket size 0-20/20-25/25-30/30-35/>35 residues, I single-ligand, J multi-proper-ligand, K multi-protein-chain, L pli_qcov bins) \| vary: SuCOS-pocket similarity bin (8) in D-L; ligand or pocket property level in A-C \| series: method (5, incl. Best-of-four) \| measure: success rate (%) \| mark: line \| n: NOT REPORTED per facet in the caption` | 12 panels, varying by stratification; A-C vary by a ligand/pocket property, D-L by similarity bin | Twelve panels share one caption with no per-panel n; panels A-C put a different variable on the independent axis from D-L without visual separation | CC-BY 4.0, no ND — p30 |
| S4 | 31 | Ten example small molecules drawn from each of the eight similarity bins | schematic | `SCHEMATIC \| grid of 2D chemical structures, ten example ligands per training-set similarity bin \| no data` | 1 grid, 8 bins × 10 molecules | Ten of 64–673 shown per bin with the sampling rule unstated | CC-BY 4.0, no ND — p31 |

Not a figure, recorded here so it is not lost: **Table 1 (p18)** gives per-method PDB IDs, systems,
all ligands, proper ligands, multi-ligand and multi-protein counts for both cutoffs; **Supplementary
Table S1 (p28)** gives the ten largest clusters with size, representative PDB ID, description, and
per-similarity-bin breakdown.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), session
  `b4b527b3-7dd9-48b6-8b5d-c95a41ac3967`
- **schema_version**: v3
- **confidence**: **high** on identity, scope, design, controls, claims and figure structure —
  the Methods are unusually complete and every protocol claim is checkable against a stated page.
  **Medium** on `metrics_reported`: only the Fig 1E bar labels, the bin counts, and the percentages
  quoted in running text are printed; every curve value (Figs 1A/1B, 2A, 3A–C, 6A–F) had to be read
  off a rendered panel and is approximate to ±1–2 percentage points. The underlying CSVs exist at
  Zenodo but the corpus does not hold them. Also medium on the per-model training cutoffs: the paper
  asserts one shared date for four methods rather than citing each method's own.
  What was hard to read: the text layer renders "pocket_qcov" as "pocket qcov" and "pli_qcov" as
  "pli qcov" (underscores lost), and the Fig 5 caption's panel lettering is internally inconsistent.
- **unresolved**:
  1. **Which version the corpus should cite.** The PDF held is the bioRxiv preprint (4 Aug 2025,
     DOI 10.1101/2025.02.03.636309, title "Have protein-ligand cofolding methods moved beyond
     memorisation?", five authors). The paper has since been published as **"Evaluating
     generalization in protein-ligand cofolding methods", Nature Structural & Molecular Biology
     2026, DOI 10.1038/s41594-026-01797-5**, six authors (adds Gabriel Studer), which is what
     `refs.bib` already records. **The corpus should cite the NSMB version; this note documents the
     preprint.** Not checkable from here: whether the journal version changed any n, any bin count,
     any figure panel lettering, or the memorisation framing that the retitle suggests was softened.
     Anything quoted verbatim from this note into the manuscript should be re-verified against the
     NSMB text, and the `year`/`venue`/`title` fields in section A re-extracted if the journal PDF
     is obtained. The `preprint` tag should become `peer-reviewed` at that point.
  2. **Whether the AlphaFold3 template search was date-restricted to the pre-cutoff PDB.** p17 says
     only "AlphaFold3 predictions were made with templates enabled". If it was not restricted, a
     post-cutoff structural template — conceivably the ground truth — was retrievable. The AF3-NT
     control and the p5 statement that ligand information is not carried by templates bound the
     consequence to approximately zero for the measured quantity, but the protocol detail itself is
     absent. Also unstated: whether MSA databases were date-restricted (they are sequence, not
     structure, so this is a lesser concern).
  3. **Per-method training cutoffs are asserted, not sourced.** A single date (30 September 2021) is
     attributed to AlphaFold3, Chai-1, Protenix and Boltz-1 (p3) with no per-method citation.
     Boltz-1x's cutoff is never given; RoseTTAFold-All-Atom's is never given. Only Boltz-2's
     (1 June 2023) is separately stated and sourced to [31]. If any of the four differs from
     30 September 2021 in reality, the bin annotations for that method are systematically wrong.
  4. **Whether the 2 Å / 0.8 success predicate was fixed before or after inspecting Fig 7A.** The
     justification on p19 is written retrospectively against the joint distribution of all 229,887
     predictions. Both thresholds are cited to prior work, and an RMSD-only arm is run, so the
     conclusion is robust either way — but the ordering is not stated.
  5. **The n=673 (Fig 1) vs n=674 (Fig 4) discrepancy** in the 80–100 bin, for what appears to be
     the same common-subset stratum. One ligand, unexplained.
  6. **RoseTTAFold-All-Atom's version number** is never given (p17 says only "we followed the
     standard procedure as described in its documentation").
  7. **Number of distinct proteins in the benchmark.** Systems were clustered to 80% sequence
     identity for redundancy filtering (p16) but the resulting count is never reported, so "n
     proteins" cannot be stated — only n systems, n PDB IDs, n proper ligands and n SuCOS-pocket
     clusters.
  8. **Tags wanted but not invented**, per rule 9 — none were fabricated, and two gaps are worth
     the schema's attention:
     - There is **no tag for a paper whose contribution is a training-set-similarity or
       data-leakage metric**. `anti-memorization` marks that a paper *has* a post-cutoff design;
       nothing marks that a paper *defines the leakage measure* other papers should adopt. Something
       like `leakage-metric` or `similarity-stratified` would make this paper findable for the
       query it is most likely to be asked ("what should we stratify our accuracy by?").
     - There is **no system tag for protein–small-molecule complex prediction as a task**. The
       system vocabulary is entirely protein-family-based (`gpcr`, `kinase`, `transporter`, …), so a
       2,600-system pan-PDB ligand-binding benchmark lands on `general-protein` alongside papers
       about single soluble proteins. A `protein-ligand` system tag, or a task axis, would separate
       them. I tagged `general-protein` and did not invent an alternative.
     - Minor: `md-emulator` and `latent-steering` exist, but there is no tag for
       **physics-based / docking baselines**, which this paper names as its own missing arm (p14).
  9. **`data_shape` grammar gaps hit while writing section F** (blunt, as asked):
     - **`mark:` has no value for a stacked area chart.** The enum is `bar|violin|box|point|line`.
       Fig 2B is a stacked area over a continuous time axis; I wrote `mark: stacked area`, which is
       outside the enum and will therefore not join. `area` and `step` should be added.
     - **The panel-splitting rule has no provision for a differing `vary`.** The rule is "split when
       `mark` or `measure` differs; do not split when only `facet` differs". Figure 3A varies by
       *number of analogous training systems* while 3B and 3C vary by *similarity bin* — same mark
       (line), same measure (success rate %). A literal reading of the rule makes Fig 3 a single row
       with an incoherent `vary` slot. I split it into `3A` and `3B-C` and am flagging the deviation.
       **`vary` should join `mark` and `measure` as a split trigger**, since it is the independent
       axis and a row whose `vary` is ambiguous cannot be matched against anything.
     - **A nested/subset series has no expression.** Fig 1E's bars are striped (success) with a
       solid sub-bar (success *and* PB-Valid) — the two are not parallel categories but a set and
       its subset. I wrote `series: method (4) × validity (2)`, which loses the nesting and implies
       eight independent bars where there are four bars with an inset.
     - **`n:` for a violin overlaid with per-method scatter.** Figures 1C-D, 4A-B and 4E-F pool all
       methods into one violin and overlay per-method points. The per-mark n is the pooled bin
       count for the violin and 1 for each scatter point; the per-panel n is a third number. The
       field takes two values and this shape needs three.
     - **RENDER's `overlay:` slot assumes superposition.** Figures 4C-D and 5 show ground truth,
       prediction and closest training system *side by side in separate boxes*, never superposed.
       `overlay: 0 predictions on 1 reference` is technically true and reads as though nothing was
       shown. A `layout: side-by-side | superposed` slot would fix it.
     - Minor: `metric_saturation` says "numeric only" and `hides` takes axis truncation, which is
       now unambiguous and worked well — Fig 6E/F's y-axis starting at 50% went cleanly into `hides`
       with no temptation to double-record. The v3 fix holds.
- **why_it_matters**:

---

## Tags

`general-protein` `cofolding` `benchmark-only` `templates-on` `single-state` `ensemble`
`continuous-metric` `binary-predicate` `saturating-metric` `anti-memorization` `multi-backbone`
`confidence-as-discriminator` `prospective` `oracle-leak` `seed-only` `preprint` `precedent`
`threat` `negative-result` `comparator-numbers`

Tag notes, because three of these need a caveat that a bare tag would misrepresent:

- **`oracle-leak`** is applied **narrowly and deliberately**, not because a benchmark scores against
  references. It marks `oracle_leakage` **route 4(a)**: the per-method iPTM decision thresholds are
  fitted at the ROC-optimal operating point on the full evaluation set against the references (p11),
  and the classification accuracies in Fig 6E (p13) are then reported using those same in-sample
  thresholds with no held-out split. **This affects one supporting panel, not the central
  memorisation result**, and it is the only undeclared reference use in the paper. Routes 5 and 6
  (success defined by RMSD/LDDT-PLI to the reference; best/worst oracle curves) are also present but
  are declared, load-bearing and correct for a benchmark. Anyone reverse-looking-up `oracle-leak`
  must read the field before treating this paper as compromised.
- **`prospective`** reflects that all 2,600 systems postdate the models' training cutoffs and were
  selected by an automated protocol blind to outcome (p15–16). The *analysis* — bins, predicate,
  oracle curves, thresholds — is retrospective. `prospective` here means prospective **with respect
  to the models**, which is the sense that matters for memorisation.
- **`single-state` + `ensemble`** describes pose sampling (25 models per system, collapsed by
  ranking to one), not protein conformational-state generation. This paper is not a
  conformational-states paper; the one state observation is a single anecdote on p11 (a DFG-out
  ground truth predicted DFG-in).
- **`design-level-oracle` deliberately NOT applied**: route 7 is `NONE FOUND` (p15–16). No system
  was chosen because its answer was known. The nearest thing — that the SuCOS-pocket bins can only
  be computed from the ground-truth ligand pose — is a property of the analysis axis, recorded under
  route 3, and is weaker than design-level oracle use.
- **`unpowered` deliberately NOT applied**: the primary arm's smallest stratum is n=64 with
  bootstrap CIs. Three sub-arms are thin in their lowest bins (Boltz-2 m=21, cluster representatives
  n=37, distinct ligands n=51) — all above the schema's n≈10 trigger, and all recorded in
  `anti_memorization_control`.
- **`figure-exemplar` deliberately NOT applied**: the definition carries "must be excluded from gap
  analysis", and this paper must not be excluded from gap analysis. Its figures are strong, but that
  is what the `F` table is for.
