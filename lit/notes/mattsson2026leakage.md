# mattsson2026leakage

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` where the field presupposes a conformational-prediction paper and this is not one.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–15) and coincide with the
printed folios.** Layout: p1 title/abstract + §1 Introduction, p2 §2 Co-folding and sequence
similarity cutoffs, p3–4 §3 muscarinic case study, p4–5 §4 ChEMBL meta-analysis (Tables 1–2),
p4–6 §5 deconstructing FEP+ 4 / OpenFE (Fig 2, Table 3), p6–7 §6 ligand-only baselines (Fig 3),
p7–9 §7 proposed splitting (Figs 4–5), p9 §8 Conclusions and §9 data/code, p10 Appendix A
(split reproduction) + Appendix B Fig 6, p11 Fig 7 + Appendix C ligand-only model,
p12 Tables 4–5, p12–13 Appendix D benchmark construction + Fig 8, p14–15 References.

**This is an affinity-benchmark critique paper, not a conformational-state paper.** Section C of the
schema is therefore mostly `NOT APPLICABLE` by design (cf. the `experimental` tag rationale in
SCHEMA.md), except `oracle_leakage`, `anti_memorization_*` and `controls_run`, which are the
paper's actual subject matter. Note that this paper's own word "data leakage" means **affinity-value
leakage across a train/test split** (the same compound measured against a homologous target in the
training set), which is a *different* object from the corpus's `oracle_leakage` (deposited-structure
knowledge entering a prediction pipeline). Both are recorded, separately and explicitly labelled.

**Figure-value caveat:** bar labels in Fig 3 and bin counts (n_a, n_m) in Figs 4, 7, 8 are printed
in the panels and are exact. Curve values in Figs 4 and 8 marked *(read from rendered panel)* were
read off marks rendered with `pdftoppm` at 150 dpi (pages 3, 6, 7, 8, 10, 11, 13) and are
approximate to ±0.02. All renders were deleted after reading.

---

## A. Identity

- **citekey**: `mattsson2026leakage`
- **doi**: **10.64898/2026.06.29.735309** (bioRxiv, this version posted **30 June 2026**) — banner
  on every page, p1: "bioRxiv preprint doi: https://doi.org/10.64898/2026.06.29.735309; this
  version posted June 30, 2026."
- **year**: **2026** (p1).
- **venue**: **bioRxiv preprint, not certified by peer review** — p1: "The copyright holder for this
  preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a
  license to display the preprint in perpetuity. It is made available under a CC-BY 4.0
  International license." Tagged `preprint`.
- **title**: **"Identifying and Addressing Systematic Data Leakage in Protein-Ligand Affinity
  Benchmarks"** (p1).
- **authors**: **Björn Mattsson** (Enlace Bio, bjorn@enlacebio.com) and **W. Patrick Walters**
  (OpenADMET, pat.walters@omsf.io) — p1. Two authors only.
- **benchmark name**: **Novelty-Tiered Affinity Benchmark (NTAB)** — data at
  `https://doi.org/10.5281/zenodo.19665374` under **CC BY-SA 3.0**; evaluation code at
  `https://github.com/bamattsson/ntab` under **MIT**; figure-reproduction code at
  `https://github.com/bamattsson/paper-identifying_and_addressing_data_leakage` under **MIT**
  (all p9).

## B. Scope

- **system**: **general protein**, with three named sub-populations. The ChEMBL 36 meta-analysis is
  family-unrestricted and "cover[s] a wide variety of targets, including kinases, GPCRs, and
  metalloenzymes" (p4). The §3 case study is **GPCR** (five human muscarinic acetylcholine
  receptors M1–M5, p3). The FEP+ 4 benchmark is entirely **protein kinase** (TYK2, CDK2, JNK1,
  p38α, p4); the OpenFE leakage examples are kinase (BTK/LCK, p5) and tankyrase (TNKS2/TNKS1, p5,
  not a kinase). Table 2's sample (p5) spans kinases, GPCRs, HDACs, carbonic anhydrases,
  phosphodiesterases, collagenases, desaturases, prolyl hydroxylases and acetylcholinesterase.
- **n_targets**: **dual, and must not be collapsed.** (i) FEP+ 4 = **4** targets (p4). (ii) OpenFE
  subset of Ross et al. 2023 = **39** targets (p4). (iii) §3 case study = **5** muscarinic receptors
  (p3). (iv) ChEMBL 36 meta-analysis = **6,115 assay pairs** across **2,689 papers**, from a pool of
  **59,552 assay pairs / 8,454 papers** (Table 1, p4); the number of distinct *targets* behind those
  pairs is **NOT REPORTED**. (v) Novelty-Tiered Affinity Benchmark: reported as assays and
  measurements per novelty bin (n_a 24 / 235 / 340 / 112 / 111; n_m 1108 / 6106 / 7383 / 2114 /
  4396, Fig 4, p8), **total distinct targets NOT REPORTED**.
- **method_class**: **benchmark-only** (critique of two existing benchmarks + construction of a new
  one), **plus** the training of a ligand-only ML baseline used as a leakage probe (§6 p6,
  Appendix C p11–12). No structure-prediction method is developed. The only co-folding *run* the
  authors perform is the two illustrative Boltz-2 poses in Fig 2 left (p6).
- **backbones**: **Boltz-2** — used by the authors only to co-fold `lig_18633-1` with JNK1 and JNK2
  for the Fig 2 left panel (p6). All other Boltz-2 and IsoDDE performance numbers in Fig 3 were
  **not rerun**: "Results for methods other than the baselines were taken from the IsoDDE report"
  (Fig 3 caption, p7). Boltz-2 [15], IsoDDE [16] and AQAffinity [17] are discussed as the targets of
  the critique (p2). No AF2/AF3/Chai/OF3/Protenix arm. **Not tagged `multi-backbone`**: at most two
  co-folding backbones appear, and they are not run head to head by these authors.
- **templates**: **NOT REPORTED.** The Boltz-2 co-folding settings for Fig 2 are not stated anywhere
  in the paper or appendices. Everything else in the paper is sequence- and ligand-based.
- **msa_handling**: **NOT REPORTED** for the Fig 2 Boltz-2 run. Note that MMseqs2 *is* used
  (p10, Appendix A) but for **sequence clustering to reproduce the train/test split**, not for MSA
  construction: `mmseqs easy-cluster fasta_seqs_for_clustering.fasta cluster_res cluster_tmp
  --min-seq-id 0.9 --cov-mode 0 -c 0.01`. Do not read that as MSA handling.

## C. Conformational core

- **states_generated**: **NOT APPLICABLE — no conformational states generated or scored.** The only
  structures produced anywhere are two Boltz-2 co-folded poses of one ligand shown for illustration
  (Fig 2 left, p6): "Predicted binding poses of lig_18633-1 co-folded with JNK1 (test set, orange,
  pIC50 = 6.75) and JNK2 (train set, gray, pIC50 = 6.56) using Boltz-2, with residues within 3.5 Å
  shown." The paper's output is a benchmark and a set of correlation statistics.
- **structural_priors_used**:
  1. **PDB reference entries used to map the OpenFE benchmark to targets** — p10: "Mapping the
     system group and system name columns to targets can be achieved via the
     `industry_benchmarks/input_structures/original_structures/*/subset_metadata.csv` files in the
     same repository and the `Reference PDB` entries." Deposited structures are used at
     *dataset-assembly* time, to identify which protein each measurement belongs to.
  2. **Boltz-2 co-folding of the two JNK poses** in Fig 2 (p6) — a structure prediction used as
     visual evidence that two targets present the same binding environment.
  3. **Binding-pocket similarity knowledge underpinning Table 3** (p6): "Targets with similar
     binding pockets to each FEP+ 4 test target, grouped by data split." The procedure by which
     "similar binding pockets" was determined is **NOT REPORTED** — see `unresolved`.
  4. **Explicit refusal of a structural prior in the probe model**, which is the point of the probe
     — p11: "The baselines are ligand-only models trained to predict pIC50, pKi and pKd values from
     ligand features and a learned target representation, **with no structural information about
     the protein target**"; p6: "the protein target represented by a one-hot encoding that contains
     no protein structural information."
  5. **Sequence, not structure, priors** for the split reproduction: ChEMBL 36 sequences plus
     UniProt for two missing test targets (p10).
  None of the above is a defect; it is recorded here rather than in `oracle_leakage` per the v3 rule.
- **oracle_leakage**: **the corpus sense of the field — knowledge of deposited structures of a
  target state entering the pipeline — is essentially absent here, because there is no
  conformational pipeline.** Route by route:
  1. **Structures used as input or template** — **NONE FOUND for the paper's own quantitative
     results.** The probe model takes no protein structure at all (p11, quoted above); the split is
     built from sequence clustering (p10). **NOT REPORTED for the Fig 2 Boltz-2 run** (p6), whose
     template/MSA configuration is never stated; that run produces no number, only a picture.
  2. **State annotations from a curated database (GPCRdb / KLIFS / Kincore) driving templates or
     alignments** — **NONE FOUND.** The databases used are ChEMBL 36 [22], UniProt [30] and the
     OpenFE/protein-ligand-benchmark repositories (p10); none carries conformational-state
     annotation, and no alignment is state-filtered. Protocol described p10 (Appendix A) and p12–13
     (Appendix D).
  3. **Cluster labels derived from known states** — **NONE FOUND.** Clusters are MMseqs2 sequence
     clusters at `--min-seq-id 0.9` (p10); the novelty tiers are Morgan-fingerprint Tanimoto bins
     over *ligands* (p8, p13). No cluster carries a state label.
  4. **Hyperparameters, sweep ranges, seeds or stopping criteria tuned against the evaluation set** —
     **NONE FOUND for the proposed benchmark, PARTIAL for the FEP+ 4 / OpenFE arms.** For NTAB the
     validation set is a disjoint year band and the authors state why: "Since the validation set
     influences model development through early stopping and hyperparameter optimization, leakage
     across the test/val boundary would inflate reported performance in the same way as leakage
     across test/train" (p12), with "the best checkpoint selected by validation Pearson r" (p11).
     For the FEP+ 4 / OpenFE arms the baselines were "trained on ChEMBL 36 [22], which had been
     split following the FEP+ 4 and OpenFE benchmark methodology" (p6) and no separate validation
     protocol for those runs is stated — **NOT REPORTED**. One design choice touches the test set
     directly: "For targets absent from the training set, the embedding and bias of the nearest
     training target by protein sequence similarity were used" (p11), i.e. the test target's
     sequence identity selects which learned embedding is applied. That is the mechanism under
     study, deliberately, not a concealed leak. **No sweep range is reported at all** (Table 5, p12,
     fixes d = 2048, d_target = 256, n_hidden = 4 with no sweep description) — see `unresolved`.
  5. **Success defined post hoc by RMSD or TM to a structure they had** — **NONE FOUND / NOT
     APPLICABLE.** Success is Pearson r (and MAE) against experimental affinity (Figs 3, 4, 7, 8).
     The single structural claim is qualitative and by eye: "The poses are virtually
     indistinguishable" (Fig 2 caption, p6) — no RMSD is computed or reported.
  6. **Best/worst model labels assigned against a held reference** — **PRESENT, in the weak
     reporting sense.** The headline ligand-only numbers are "the best ligand-only model" selected
     *by its score on the benchmark being criticised*: p6, "On the FEP+ 4 test set, the best
     ligand-only model matched Boltz-2 and the physics-based OpenFE model at r = 0.66... On the
     OpenFE benchmark, the best ligand-only model achieved r = 0.36". Reading Fig 3 (p7), the
     best model differs between the two benchmarks — FP + mol desc (0.66) on FEP+ 4, Chemprop
     (0.36) on OpenFE, where FP + mol desc scores only 0.27. Same on the new benchmark: "the best
     ligand-only performance drops considerably from r = 0.61 to r = 0.14" (p8). All three baselines
     are always shown, so the selection is visible rather than hidden, but the abstract quotes only
     the maximum.
  7. **Design-level oracle use — systems or inputs chosen because the expected answer is already
     known** — **PRESENT, and labelled design-level, not pipeline leakage.** Both demonstrative case
     studies were selected because the correlation was known in advance. p3: "This data was
     extracted from a single 1998 paper [21] in which the authors were optimizing a chemical series
     of antagonists specifically to be selective for the M4 receptor over the M1 receptor" — a
     series chosen for a family known to mirror. p5: "The JNK1/JNK2 case is the clearest example of
     leakage: the entire compound series appears on both sides of the split." p5 likewise selects
     "two specific subsets, 'merck' and 'miscellaneous'" out of a collection they say they
     investigated in full. This is standard demonstrative practice for an existence proof, and the
     authors back it with the unselected 6,115-pair census (Table 1, p4) and the full-sweep Fig 5
     (p8); but the anecdotes themselves are chosen on the outcome.
  - **Separately: the paper's OWN definition of leakage**, which is what it measures, is
    affinity-value leakage across a protein-sequence-identity split — recorded in full under
    `central_conclusion` and `necessity_claims` below. Do not conflate the two vocabularies when
    querying this note.
- **prospective**: **no.** Every number is retrospective: a re-analysis of two published benchmarks,
  a census of an existing database (ChEMBL 36), and a temporally split benchmark whose "prospective"
  character is simulated by a publication-year cutoff (train < 2022, val 2022, test ≥ 2023, p12).
  No compound was made or measured. The authors frame prospectivity as the *goal* the field is
  failing, not as something they achieved (p9).
- **state_metric**: **NOT APPLICABLE** — no conformational state is called. The paper's metrics are
  continuous: Pearson r and MAE (Figs 3, 4, 7, 8). Two thresholds used as binary predicates are
  stated and justified: **R² ≥ 0.6** for "correlated" assay pairs (p4, criterion 4; justified as the
  same thing as r ≥ 0.77, p3) and **< 90% sequence similarity** for "dissimilar" targets (p4,
  criterion 3; justified as the value the criticised benchmarks use, p4).
- **metric_saturation**: **YES, numerically, in one arm.** Per-assay Pearson r is bounded on
  [−1, 1] and in Fig 7 (p11) individual grey assay points sit exactly at **r = 1.00** (several) and
  at **r = −1.00** (one), i.e. the per-assay metric floors and ceilings on small assays. The authors
  recognise this and filter against it in the proposed benchmark: assays are retained only with
  "at least 10 unique compounds, a −log10 standard deviation of at least 0.5 across those
  compounds" because "Correlation coefficients against assays with insufficient compounds or
  low-affinity variations would be dominated by measurement noise" (p13). The *aggregate* means
  never approach the ceiling (maximum reported value 0.85, Fig 3 p7), so the headline numbers are
  not saturated. No axis break or truncation anywhere — see `hides` (Fig 3) for the figure-level
  defects, which are pooling, not saturation.
- **directional_control**: **NOT APPLICABLE** — nothing is instructed to produce a state. The
  nearest analogue is the *handle on leakage*, which is the Tanimoto-similarity tier: the
  experimenter can dial ligand novelty from ≥ 1.00 down to < 0.35 and watch the ligand-only score
  fall (Fig 4, p8). That is a control on the benchmark, not on a model's output state.
- **anti_memorization_design**: **YES — this is the paper's contribution.** The **Novelty-Tiered
  Affinity Benchmark**, built on ChEMBL 36, with two stacked barriers (p7–8, detailed p12–13):
  1. **Temporal split by ChEMBL source-document publication year**: "assays from ≥ 2023 in test,
     2022 in val, and < 2022 in train" (p7). The val band is separate precisely so early stopping
     cannot leak (p12).
  2. **Ligand-novelty tiers by maximum Tanimoto similarity** (2048-bit Morgan fingerprints,
     radius 2) between each test compound and **all compounds whose earliest ChEMBL publication
     predates the cutoff** (p13). Exact-match compounds are broken out into their own bin (= 1.00).
     Bins and n (Fig 4, p8): **[0.00, 0.35)** n_a = 24, n_m = 1108; **[0.35, 0.50)** n_a = 235,
     n_m = 6106; **[0.50, 0.70)** n_a = 340, n_m = 7383; **[0.70, 1.00)** n_a = 112, n_m = 2114;
     **= 1.00** n_a = 111, n_m = 4396.
  3. **Assay predictability filter** (p13): test/val assays kept only with ≥ 10 unique compounds,
     −log10 standard deviation ≥ 0.5, equality-relation measurements only, and **at most one assay
     per document**, keeping the largest — "to avoid biasing the benchmark with multiple
     near-identical series from the same experimental campaign".
  4. **Source filters** (p12): ChEMBL max confidence score 9, binding assay type, single protein
     target, direct or homologous target mapping, Ki/Kd/IC50 only, mutant-sequence assays and
     flagged measurements excluded, all values on the −log10 scale.
  The cutoff is defined by **publication year of the ChEMBL source document**, not by a structure
  deposition date; the authors note this lets a two-step co-folding + affinity pipeline align both
  models' cutoffs (p12).
- **anti_memorization_control**: **RUN, and analysed — but on the baseline only, never on the
  models under criticism.** The ligand-only baselines are run across all five novelty tiers
  (Fig 4, p8), against a temporal-split-only benchmark ("our best ligand-only method achieved
  r = 0.32, indicating that a temporal split alone is insufficient to prevent data leakage", p9),
  and against the assay-average binning variant (Fig 8, p13). **Not `UNPOWERED` in the main tiers**
  (n_a 24–340, n_m 1108–7383; the authors contrast this with 10–21 per bin in the Boltz-2 analysis,
  p11). Two qualifications: (a) the **[0.00, 0.33) bin of Fig 8 has n_a = 5** and a confidence band
  spanning roughly 0.0–0.4 — that arm alone is unpowered; (b) **Boltz-2 and IsoDDE were never
  evaluated on the leakage-controlled benchmark** — the paper reports no co-folding number on NTAB
  at all, which is the single largest gap in it (see `unresolved`).
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | **Ligand-only baseline (Chemprop D-MPNN + FP + descriptors, one-hot target, no protein structure) on FEP+ 4** | Rules out that r ≈ 0.66 on FEP+ 4 requires protein structural information at all: a model that cannot see the protein matches Boltz-2 and the physics-based OpenFE result exactly. | p6, Fig 3 p7 |
  | **Twelve-molecular-descriptor-only model (MW, CLogP, TPSA, HBD, HBA, rotatable bonds, formal charge, molar refractivity, Fsp3, ring count, aromatic ring count, heavy atoms)** | Rules out that even a *learned ligand representation* is needed: 12 RDKit numbers reach r = 0.49 on FEP+ 4. Bounds how little signal the benchmark demands. | p6, Table 4 p12 |
  | **Same ligand-only baseline on OpenFE** | Rules out that the FEP+ 4 result is benchmark-specific; also establishes the size of the residual structure-based margin (0.36 vs 0.62–0.73), i.e. the leakage is worse on FEP+ 4 than on OpenFE. | p6, Fig 3 p7 |
  | **Exact reproduction of the ≥ 90% MMseqs2 split used by Boltz-2** (`--min-seq-id 0.9 --cov-mode 0 -c 0.01`) | Rules out that the leakage is an artefact of a different splitting protocol: the split is regenerated with the criticised paper's own command. | p10 Appendix A |
  | **JNK1/JNK2 whole-series check (assay CHEMBL860181 vs CHEMBL860184, same 2006 source paper)** | Rules out that the observed leakage is partial or incidental: the *entire* test compound series has a train-set twin, r = 0.95 at 81% sequence identity. | p4, Fig 2 p6 |
  | **Co-folded pose comparison of one shared ligand in JNK1 vs JNK2 (Boltz-2)** | Rules out that the two homologs present different binding environments, i.e. that the correlation could be coincidental rather than pocket-driven. Qualitative only, no RMSD. | Fig 2 left, p6 |
  | **Enumeration of related targets on both sides of the split for all four FEP+ 4 targets (Table 3)** | Rules out that JNK1/JNK2 is a lone bad case: every FEP+ 4 test target has close relatives in the train split. | Table 3, p6 |
  | **Two OpenFE subset checks — merck TNKS2 vs TNKS1 (19/27 ligands shared, s = 71.4%, r = 0.98) and miscellaneous BTK vs LCK (6/6 shared, s = 22.5%, r = 0.94)** | Rules out that leakage needs high sequence identity: BTK/LCK mirror at 22.5% identity, far below any usable cutoff. | p5, Fig 6 p10 |
  | **ChEMBL 36 census of all documents with ≥ 2 assays and ≥ 10 shared compounds (59,552 pairs → 59,085 below 90% identity → 6,115 with R² ≥ 0.6)** | Rules out that target mirroring is anecdotal: it is a population-level property of the medicinal-chemistry literature. | Table 1, p4 |
  | **Sequence-similarity cutoff sweep 0.1 → 0.9 on that census (Fig 5)** | Rules out that any *choice of threshold* solves the problem: > 4,000 correlated pairs survive at 0.5, and pairs persist down to 0.2. Directly refutes the Leakproof PDBBind recommendation. | p7, Fig 5 p8 |
  | **Temporal-split-only benchmark arm (no novelty tiers)** | Rules out that a date cutoff alone is sufficient: ligand-only still reaches r = 0.32. | p9 |
  | **Novelty-tier sweep of the ligand-only baselines on NTAB (five tiers, Fig 4)** | Rules out that the new benchmark is merely harder rather than *less leaky*: performance falls monotonically with ligand novelty and reaches r = 0.14 in the strictest tier, which is the intended leakage-free floor. | p8, Fig 4 p8 |
  | **Reproduction of the Boltz-2 compound-similarity diagnostic using a model known to memorise (Fig 7, Tukey-HSD)** | Rules out that the Boltz-2 similarity analysis has the power to detect ligand memorisation: it fails to reject the null even for a model that by construction interpolates between seen ligands. A power control on someone else's control. | p11, Fig 7 p11 |
  | **Assay-average vs per-compound similarity binning (Fig 8, Tukey-HSD)** | Rules out that per-compound binning is an arbitrary choice: averaging per assay lets high-similarity compounds hide inside low-similarity assays and flattens the gradient. | p9, p13, Fig 8 p13 |
  | **Molecular-property correlation check (pIC50 vs MW r = 0.19; vs CLogP r = 0.082)** | Rules out that the residual r = 0.14 in the strictest tier is itself leakage: it is attributed to general property–affinity trends within published series. | p9 |

  No shuffle/permutation control is run by these authors; the protein-permutation result is cited
  from the Isayev group's PCM study [20] (p3), not reproduced.
- **confidence_as_discriminator**: **NONE — no pLDDT, pTM or ipTM appears anywhere in the paper.**
  Model selection uses validation Pearson r (p11), and the two Boltz-2 poses in Fig 2 carry no
  confidence annotation (p6). Boltz-2's own affinity-confidence head is not discussed.

## D. Claims

- **central_conclusion**: Protein-sequence-identity splitting cannot prevent affinity-benchmark
  leakage, because homologous targets with low overall sequence identity still have highly
  correlated binding profiles ("target mirroring") — a ChEMBL 36 census finds 6,115 such assay pairs
  and they persist down to 0.2 identity. As a result the FEP+ 4 and OpenFE benchmarks are
  contaminated: a ligand-only model that cannot see the protein reaches r = 0.66 on FEP+ 4 (equal to
  Boltz-2) and r = 0.36 on OpenFE, so claims that co-folding models match or exceed FEP on these
  benchmarks are not supported by them. The remedy proposed is the Novelty-Tiered Affinity
  Benchmark: a publication-year split plus per-compound Tanimoto-similarity tiers, on which the
  ligand-only floor falls to r = 0.14.

- **necessity_claims** (verbatim, with page):
  - p1 (abstract): "We demonstrate that splitting by protein-sequence identity is **inherently
    insufficient** to prevent data leakage due to “target mirroring,” in which homologous proteins
    with low overall sequence identity still exhibit highly correlated binding profiles."
  - p1 (abstract): "We argue that the field **must** move beyond sequence-based splits to ensure
    that AI-driven discovery translates into successful prospective laboratory research."
  - p2: "Consequently, it is often **not possible** to assess, from published results alone, whether
    models would be useful in prospective drug discovery research."
  - p2: "the field **needs** robust benchmarking methods that control for data leakage."
  - p3: "their splitting criteria often prove **insufficient** for preventing the various forms of
    leakage discussed herein."
  - p7: "Unless one is extremely careful, any machine learning model trained to predict binding
    affinity is highly vulnerable to data leakage. **Merely adjusting the overall sequence
    similarity threshold is insufficient.**"
  - p7: "To ensure rigor in our train-test splits, **we need to go beyond overall sequence
    similarity and consider both binding-site and ligand similarity.**"
  - p7: "Since we often lack information about where compounds bind, assessing binding-site
    similarity can be challenging or **even impossible**."
  - p9: "Due to these limitations, this benchmark is **not suitable** for comparing different
    protein-ligand binding affinity methods."
  - p9: "This systemic “target mirroring” in the medicinal chemistry literature **renders overall
    protein-similarity methods, at any common threshold, unreliable** for constructing
    binding-affinity benchmarks."
  - p9: "Leakage-contaminated benchmarks **make it impossible** to separate memorization from
    genuine insight."
  - p9: "Building trust in these methods **requires** benchmarks that reflect the prospective task:
    predicting the affinity of genuinely novel compounds against targets of interest."
  - p11 (Appendix C, on the probe model's target embedding): "allowing the model to learn which
    compounds bind to which targets from historical data, but, **by design, preventing it from
    generalizing to genuinely novel binding environments** (such as unexplored regions of existing
    pockets, new pockets, or compounds without analogs)."
  - p11 (Appendix B): "Hence, this analysis is **not powerful enough** to identify methods that work
    through ligand memorization."

- **novelty_claims** (verbatim, with page). **No claim to be first, and no use of the words "novel",
  "unprecedented" or "first" about their own contribution.** The contribution claims are:
  - p1 (abstract): "This paper provides a critical assessment of these claims, revealing that
    current benchmarks are heavily influenced by data leakage, and **proposes a new benchmark that
    explicitly controls for data leakage**."
  - p1 (abstract): "To address this issue, **we propose the Novelty-Tiered Affinity Benchmark**, in
    which the test data is partitioned into ligand novelty tiers."
  - p2: "In this paper, we critically analyze benchmarks based on protein-identity splits, which
    have recently been used to claim that ML methods surpass physics-based methods, and **we
    contribute a more robust benchmarking suite.**"
  - p2: "In Sections 3 and 4, we present a case study and a meta-analysis that explain why
    protein-sequence-identity-based splits lead to data leakage."
  - p7: "**Inspired by the Runs N' Poses benchmark [14]** and based on ChEMBL 36 [22], we
    constructed the Novelty-Tiered Affinity Benchmark, which we make publicly available."
  - p9: "To help the field in this direction, **we propose and open-source the Novelty-Tiered
    Affinity Benchmark**, which bins compounds by maximum Tanimoto similarity to the training or
    validation sets into high- and low-novelty tiers."
  Priority is explicitly shared: the tiering idea is credited to Runs N' Poses [14] (p7, p9), and
  the prior structure-aware splits PDBBind CleanSplit [5], PLINDER [18] and Leakproof PDBBind [4]
  are credited before being criticised (p2, p7).

- **disputed published claims** — *extra block; SCHEMA v3 has no field for this, see `unresolved`.*
  The dispute is explicitly scoped **to the benchmarks and to the comparisons made with them, and
  explicitly NOT to the models**: p2, "This criticism targets flawed benchmarks and the claims made
  with them, **not the models themselves**"; p9, "This critique targets flawed benchmarks, not the
  models themselves."

  | # | Claim disputed (verbatim where quoted) | Whose | Grounds, with page | Dispute is about |
  |---|---|---|---|---|
  | 1 | Boltz-2 "reported an average Pearson correlation coefficient (r) of 0.66 over the FEP+ 4 targets and 0.62 on the OpenFE targets, **claiming to approach the performance of FEP methods (r = 0.78 and 0.72, respectively)**" (p4) | Boltz-2, Passaro et al. [15] | The 90% sequence-identity split leaves whole compound series on both sides (JNK1/JNK2, r = 0.95 at 81% identity, p4); a ligand-only model with no protein information reaches the same r = 0.66 on FEP+ 4 (p6). "This shows that any ML method exploiting this leakage would achieve inflated results, **invalidating comparisons with physics-based methods that operate without training data**" (p6). | **The benchmark and the comparison.** Not the model. |
  | 2 | "The Isomorphic Labs team later reported average correlations of 0.85 and 0.73 on the same benchmarks, **asserting that IsoDDE's affinity predictions surpass those of gold-standard physics-based methods**" (p4) | IsoDDE, Isomorphic Labs [16] | Same benchmark contamination (p4–6); and their supporting analyses do not close the gap: on the ChEMBL 35 novel-assay validation, "The use of recently deposited data is not in itself sufficient; newer assays often report on compounds and targets that were already extensively characterized in earlier versions of the database... **this analysis on a different dataset does not preclude the possibility that the model exploited data leakage to achieve the inflated results on which its central conclusions were based**" (p2). | **The benchmark and the comparison.** |
  | 3 | IsoDDE's and Boltz-2's use of **average assay-ligand similarity** to define similarity bins | [16], [15] | "The challenge with average assay-ligand similarity is that it **can allow partial leakage from high-similarity compounds into low-similarity assays**" (p9); demonstrated in Fig 8 (p13), where the same models' gradient is "less stark than in Figure 4, reflecting the fact that this method yields low-similarity assays that still might contain high-similarity compounds" (p13). Their own reproduction of the IsoDDE binning gives r = 0.40 → 0.27 between "high" and "medium", "with the most stringent bin containing only 5 assays and exhibiting substantial variability" (p9). | **The benchmark's diagnostic.** |
  | 4 | Boltz-2's compound-similarity-vs-performance analysis, whose logic is "that failing to show a relationship between compound similarity and performance would indicate that the model is not reliant on similar compounds in the training data" (p11) | Boltz-2 [15] | Reproduced with a ligand-only model that memorises by construction; "A Tukey-HSD test failed to reject the null hypothesis that there is no difference among the bins. **Hence, this analysis is not powerful enough to identify methods that work through ligand memorization.**" Cause given: 10–21 data points per bin vs 24–340 in NTAB, smallest bin only 3 (p11). | **The diagnostic's statistical power** — a null-result-is-not-evidence objection, not a claim that Boltz-2 memorises. |
  | 5 | IsoDDE's plot "suggesting equivalent performance across “high,” “medium,” and “low” similarity bins" (p2) | IsoDDE [16] | As #2 and #3. The authors also flag that their own reproduction differs: "they use ChEMBL 35, they use data from 2023 and onwards both for val and test, they use more activity types, they filter to assays with at least 20 ligands" (p13). | **The benchmark's diagnostic.** |
  | 6 | Leakproof PDBBind's recommended thresholds — "The team that created Leakproof PDBBind recommends a sequence similarity cutoff of 0.5 and a ligand similarity cutoff of 0.99 [4]" (p7) | Leakproof PDBBind, Li et al. [4] | "Even with a sequence similarity cutoff of 0.5, we find more than 4,000 assay pairs reporting correlated activity across different targets. This result, along with a similarity cutoff that captures only identical molecules, **calls the Leakproof PDBBind criteria into question**" (p7, Fig 5 p8). | **The splitting criteria.** |
  | 7 | AQAffinity's headline result at a 90% sequence-similarity cutoff (p2) | AQAffinity, SandboxAQ [17] | Same 90%-cutoff objection. Partially withdrawn in the same paragraph: "AQAffinity reported two assays filtered to 70% sequence similarity and 70% ligand similarity, where neither the AQAffinity nor the Boltz-2 method was able to rank the compounds by binding affinity" (p2). | **The headline benchmark only.** |
  | 8 | Structure-aware split families PDBBind CleanSplit [5] and PLINDER [18] | [5], [18] | Not disputed on correctness; disputed on applicability — "The primary disadvantage of these structure-aware approaches is their reliance on available crystallographic or docked data. In many practical scenarios, researchers seek to train on large-scale databases like ChEMBL or BindingDB, where 3D structural information or exact binding modes are often unknown" (p2). | **Scope of applicability.** |

  Concession recorded verbatim, p7: "Even though we conclude that the performance of machine
  learning methods can be significantly inflated on this benchmark by exploiting the substantial
  data leakage, **the evidence presented here is insufficient to conclude that Boltz-2 and IsoDDE
  derive the majority of their performance from memorizing ligand structures.**"
  Boltz-2 is also credited, p2: "It should be noted that both Boltz-2 and AQAffinity presented more
  nuanced results as well: Boltz-2 reported challenges reaching as promising results on internal
  Recursion targets."

- **proposed splitting procedure, in full** — *this is the most actionable content; recorded here
  because §7 + Appendix D span it.* To construct the **Novelty-Tiered Affinity Benchmark**:
  1. **Source and filters** (p12): ChEMBL 36. Keep only high-confidence binding assays against
     single protein targets — max confidence score 9, binding assay type, direct or homologous
     target mapping, and the three standard readouts Ki, Kd, IC50. Exclude flagged/unreliable
     measurements and assays against mutant sequences. Convert all values to the −log10 scale.
     Activities with both equality- and inequality-relation measurements are kept **in the training
     set**. Potential-duplicate-flagged activities are kept ("some of this data is genuinely
     novel"), with an optional user filter.
  2. **Time split by source-document publication year** (p7, p12): train < 2022; val = 2022;
     test ≥ 2023. Rationale for a separate val band, p12: early stopping and hyperparameter choice
     make test/val leakage as inflating as test/train leakage. Rationale for a date cutoff at all:
     a two-step co-folding + affinity pipeline can align both models' cutoffs.
  3. **Novelty tiers by per-compound similarity** (p8, p13): for each test compound compute the
     **maximum Tanimoto similarity (2048-bit Morgan fingerprint, radius 2) to all compounds whose
     earliest ChEMBL publication predates the cutoff**. Filter each bin to compounds inside that
     similarity interval. Bins used: [0.00, 0.35), [0.35, 0.50), [0.50, 0.70), [0.70, 1.00), and
     **= 1.00 broken out separately** (exact match to a train/val compound). Interpretation given,
     p8: "different use cases in drug discovery operate at different levels of compound novelty,
     from interpolation within a congeneric series (above 0.5 Tanimoto similarity) to the discovery
     of completely novel binders (below 0.35 Tanimoto similarity)."
  4. **Bin by individual compound, not by assay average** (p9): "We filter the similarity bins by
     individual-compound similarity rather than by average assay-ligand similarity, as employed by
     IsoDDE [16] and Boltz-2 [15]."
  5. **Assay predictability filter** on test and val (p8, p13): keep assays with ≥ 10 unique
     compounds, −log10 standard deviation ≥ 0.5 across those compounds, equality-relation
     measurements only; and **at most one assay per document**, keeping the largest qualifying one.
  6. **Scoring** (Fig 4 caption, p8): mean Pearson r and mean absolute error per bin, computed as an
     **unweighted average across all assays in that bin**, with bootstrapped 95% confidence
     intervals. Report n_a (assays) and n_m (measurements) per bin.
  7. **Reference floor**: the ligand-only baseline of Appendix C (p11–12) run through the same tiers,
     giving the leakage-attributable performance a structure-aware model must beat. In the strictest
     tier that floor is **r = 0.14** (p1, p8).

- **stated_limits**:
  - p7: "the evidence presented here is insufficient to conclude that Boltz-2 and IsoDDE derive the
    majority of their performance from memorizing ligand structures."
  - p9: "Large neural networks are known to memorize data, which does not preclude them from
    learning generalizable representations. However, these benchmarks provide no way to separate
    these contributions."
  - p9: on the binding-site-clustering alternative they cannot use — "guessing the binding site for
    every interaction in the data set could introduce significant errors that invalidate the
    resulting comparisons."
  - p11: their probe is a floor, not a ceiling — "This model represents a lower bound on what is
    achievable via ligand interpolation alone; more advanced ligand-only models with better
    representations of the ligand pharmacophore could achieve higher performance."
  - p9: the residual r = 0.14 is not claimed to be zero leakage — "The residual performance of the
    ligand-only models in Figure 4 likely stems from their learning general relationships between
    binding affinity and molecular properties within published series."
  - p11: dataset mismatch with Boltz-2 — "this dataset is not exactly the same as the one used in
    the Boltz-2 report; they report using 867 measurements, whereas we have used 873."
  - p13: reproduction mismatch with IsoDDE — "they use ChEMBL 35, they use data from 2023 and
    onwards both for val and test, they use more activity types, they filter to assays with at least
    20 ligands."
  - p13: their own alternative binning is weaker — "The difference is less stark than in Figure 4."
  - p2: the structure-aware alternatives are better but often inapplicable (quoted at dispute #8).
  - **Not stated by the authors, but a limit of the work:** no co-folding model is evaluated on the
    proposed benchmark. Recorded in `unresolved`, not attributed to them.
- **stance**: **`threat` on standards + `precedent` on methodology** — provisional, the user's call.
  *Threat*: the paper's operative standard is that a generalisation claim is worth nothing unless a
  leakage-free floor is reported alongside it, and it demonstrates that both temporal splits alone
  (r = 0.32, p9) and sequence-identity splits at any threshold (Fig 5, p8) fail to establish one.
  Any generalisation claim we make on a sequence-identity-split or date-split benchmark is exposed
  to exactly this argument. *Precedent*: the novelty-tier construction (p7–8, p12–13) and the
  ligand-only-baseline-as-floor device (p6, p11) are directly adoptable, and the paper open-sources
  both data and code (p9). It is **not** `contrast`: the paper is not about conformational states
  and does not compete with our subject matter.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Boltz-2 mean Pearson r, FEP+ 4 (90% seq-id split) | 0.66 | r | experimental affinity, 4 targets; as reported by [15] | p4, Fig 3 p7 |
  | Boltz-2 mean Pearson r, OpenFE (90% seq-id split) | 0.62 | r | experimental affinity, 39 targets; as reported by [15] | p4, Fig 3 p7 |
  | IsoDDE mean Pearson r, FEP+ 4 | 0.85 | r | as reported by [16] | p4, Fig 3 p7 |
  | IsoDDE mean Pearson r, OpenFE | 0.73 | r | as reported by [16] | p4, Fig 3 p7 |
  | FEP+ (physics) mean Pearson r, FEP+ 4 | 0.78 | r | quoted from [15]/[16] | p4, Fig 3 p7 |
  | FEP+ (physics) mean Pearson r, OpenFE | 0.72 | r | quoted from [15]/[16] | p4, Fig 3 p7 |
  | OpenFE (physics) mean Pearson r, FEP+ 4 | 0.66 | r | Fig 3 bar label | Fig 3 p7 |
  | OpenFE (physics) mean Pearson r, OpenFE | 0.63 | r | Fig 3 bar label | Fig 3 p7 |
  | **Ligand-only "FP + mol desc" mean r, FEP+ 4** — *best ligand-only, BEFORE leakage control* | **0.66** | r | same split, no protein structural information | p6, Fig 3 p7 |
  | Ligand-only Chemprop mean r, FEP+ 4 | 0.62 | r | same split | Fig 3 p7 |
  | Ligand-only "mol desc only" (12 RDKit descriptors) mean r, FEP+ 4 | 0.49 | r | same split | p6, Fig 3 p7 |
  | **Ligand-only Chemprop mean r, OpenFE** — *best ligand-only, BEFORE leakage control* | **0.36** | r | same split | p6, Fig 3 p7 |
  | Ligand-only "mol desc only" mean r, OpenFE | 0.29 | r | same split | Fig 3 p7 |
  | Ligand-only "FP + mol desc" mean r, OpenFE | 0.27 | r | same split | Fig 3 p7 |
  | **Best ligand-only mean r, NTAB tier = 1.00 (exact train match)** — *AFTER leakage control, most leaky tier* | **0.61** | r | NTAB, n_a = 111, n_m = 4396 | p8, Fig 4 p8 |
  | Best ligand-only mean r, NTAB tier [0.70, 1.00) | ≈ 0.30 *(read from rendered panel)* | r | NTAB, n_a = 112, n_m = 2114 | Fig 4 p8 |
  | Best ligand-only mean r, NTAB tier [0.50, 0.70) | ≈ 0.21 *(read from rendered panel)* | r | NTAB, n_a = 340, n_m = 7383 | Fig 4 p8 |
  | Best ligand-only mean r, NTAB tier [0.35, 0.50) | ≈ 0.18 *(read from rendered panel)* | r | NTAB, n_a = 235, n_m = 6106 | Fig 4 p8 |
  | **Best ligand-only mean r, NTAB tier [0.00, 0.35)** — *AFTER leakage control, strictest tier* | **0.14** | r | NTAB, n_a = 24, n_m = 1108 | p1, p8, Fig 4 p8 |
  | Ligand-only Chemprop mean r, NTAB tier [0.00, 0.35) | ≈ 0.08 *(read from rendered panel)* | r | NTAB, n_a = 24 | Fig 4 p8 |
  | Best ligand-only mean r, temporal-split-only benchmark (no novelty tiers) | 0.32 | r | ChEMBL 36 date split alone | p9 |
  | Expected ligand-only performance in "true de novo situations" | < 0.20 | r | authors' framing of the leakage-free regime | p6 |
  | Ligand-only mean absolute error, NTAB tier [0.00, 0.35) | ≈ 1.02–1.13 *(read from rendered panel)* | log10 units | NTAB, three baselines | Fig 4 p8 |
  | Ligand-only mean absolute error, NTAB tier = 1.00 | ≈ 0.65 (Chemprop/FP) to ≈ 0.92 (mol desc) *(read from rendered panel)* | log10 units | NTAB | Fig 4 p8 |
  | Assay pairs, ≥ 2 assays with ≥ 10 compounds in common | 59,552 pairs / 8,454 papers | count | ChEMBL 36 census | Table 1, p4 |
  | …of which sequence similarity < 0.9 | 59,085 pairs / 8,218 papers (**99% of cases**) | count | ChEMBL 36 census | Table 1, p4 |
  | …of which R² ≥ 0.6 | **6,115 pairs / 2,689 papers** | count | ChEMBL 36 census | p1, Table 1, p4 |
  | Correlated assay pairs surviving a 0.5 sequence-similarity cutoff | > 4,000 | count | Fig 5 sweep, cutoffs 0.1–0.9 | p7, Fig 5 p8 |
  | Lowest sequence-identity threshold at which leakage still persists | 0.2 | fraction identity | Fig 5 sweep / Table 2 | p1, Fig 5 p8 |
  | Muscarinic pairwise correlations ≥ 0.77 (= R² ≥ 0.6) | 5 of 10 pairs | count | Augelli-Szafran 1998 series, M1–M5 | p3, Fig 1 p3 |
  | Muscarinic M1 vs M3 Pearson r | 0.90 | r | same series | p3, Fig 1 p3 |
  | Muscarinic M1 vs M5 Pearson r | 0.96 | r | same series | p3, Fig 1 p3 |
  | Muscarinic inter-subtype overall sequence similarity | 40–65 | % | UniProt/ChEMBL sequences | p4 |
  | JNK1 (test) vs JNK2 (train) series Pearson r | 0.95 | r | CHEMBL860181 vs CHEMBL860184, same 2006 paper | p4, Fig 2 p6 |
  | JNK1/JNK2 sequence identity | 81 | % | MMseqs2 / sequence alignment | p4, Fig 2 p6 |
  | TNKS2 (test) vs TNKS1 (train, CHEMBL4322251) Pearson r | 0.98 | r | merck subset, coverage 19/27 ligands | p5, Fig 6 p10 |
  | TNKS2/TNKS1 sequence identity | 71.4 | % | Fig 6 annotation | p5, Fig 6 p10 |
  | BTK (test) vs LCK (train, CHEMBL3588238) Pearson r | 0.94 | r | miscellaneous subset, coverage 6/6 ligands | p5, Fig 6 p10 |
  | BTK/LCK sequence identity | 22.5 | % | Fig 6 annotation | p5, Fig 6 p10 |
  | Ligand-only r under IsoDDE-style assay-average binning, "high" bin | 0.40 | r | reproduction of IsoDDE binning | p9, Fig 8 p13 |
  | Ligand-only r under IsoDDE-style assay-average binning, "medium" bin | 0.27 | r | reproduction; strictest bin has only 5 assays | p9, Fig 8 p13 |
  | Boltz-2 similarity-diagnostic reproduction, Tukey-HSD | fails to reject H0 (no difference between buckets) | — | chemprop ligand-only on OpenFE, 4 buckets, n_a 10–21 | p11, Fig 7 p11 |
  | Fig 8 Tukey-HSD, [0.33, 0.66) vs [0.66, 1.00) | significant for all three models | — | NTAB assay-average binning | Fig 8 p13 |
  | pIC50 vs molecular weight Pearson r | 0.19 | r | across the NTAB dataset | p9 |
  | pIC50 vs CLogP Pearson r | 0.082 | r | across the NTAB dataset | p9 |

  **Before → after leakage control, stated compactly:** best ligand-only baseline **r = 0.66**
  (FEP+ 4) and **r = 0.36** (OpenFE) under the 90% sequence-identity split (p6, Fig 3 p7) →
  **r = 0.32** under a temporal split alone (p9) → **r = 0.61 → 0.14** across the NTAB novelty tiers
  from exact-match to < 0.35 Tanimoto (p8, Fig 4 p8). The co-folding models' own numbers **before**
  control are Boltz-2 0.66 / 0.62 and IsoDDE 0.85 / 0.73 (p4); their numbers **after** control are
  **NOT REPORTED — never measured** (see `unresolved`).

- **n_predictions**: no sampling in the generative sense; the analogous quantities are:
  - **Targets**: FEP+ 4 → 4; OpenFE → 39 (p4). Muscarinic case study → 5 (p3).
  - **Measurements**: OpenFE → **873** in the version the authors used (the IsoDDE-cited release),
    vs **867** in the Boltz-2 release (p10, p11). FEP+ 4 measurement count **NOT REPORTED**
    (extracted from `00_data/ligands.yml` per target, p10).
  - **NTAB per-bin measurements**: 1108 / 6106 / 7383 / 2114 / 4396 across the five tiers, over
    24 / 235 / 340 / 112 / 111 assays (Fig 4, p8). Assay-average variant: 747 / 16,753 / 11,437 over
    5 / 546 / 374 assays (Fig 8, p13). Fig 7 reproduction buckets: 304 / 330 / 128 / 111
    measurements over 16 / 21 / 11 / 10 assays (p11).
  - **Census**: 59,552 candidate assay pairs → 6,115 correlated pairs (Table 1, p4).
  - **Models trained**: three ligand-only baselines (Chemprop, FP + mol desc, mol desc only), each
    100 epochs, best checkpoint by validation Pearson r (p11). Number of seeds or replicate training
    runs **NOT REPORTED**; uncertainty is bootstrapped over assays, not over training runs.
- **comparable_to_ours**: *(left empty by the extractor per SCHEMA v3)*
- **si_in_scope**: **PARTIAL — SI NOT HELD for the census table.** The 6,115-pair table is
  represented in the PDF only by a 20-row sample (Table 2, p5): "The full table, as well as the
  scripts used to perform the analysis, are available in the supporting materials for this paper"
  (p4). Those supporting materials are not in the corpus. Everything else that carries a number —
  Tables 1, 3, 4, 5 and Figures 1–8 — **is in the PDF**, including all four appendices; the paper
  has no separate SI document beyond the census table, the Zenodo dataset
  (`10.5281/zenodo.19665374`) and the two GitHub repositories (p9). Per-target breakdowns of the
  Fig 3 bars (per-target r for the 4 FEP+ 4 and 39 OpenFE targets) are **not printed anywhere** —
  only size-weighted means.

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 3 | Lower-triangle pairwise scatters of pIC50 across the five muscarinic receptors for one 1998 antagonist series | scatter (pairs-plot lower triangle) | `PLOT \| facet: receptor pair (10 lower-triangle cells) \| vary: pIC50 of receptor j, ~4.5–9 (continuous) \| series: none (1) \| measure: pIC50 of receptor i \| mark: point \| n: 1 per mark, ~20 compounds per panel (exact n NOT REPORTED)` | 10 scatter cells of a 5×5 grid; panels vary by receptor pair (condition), not by view | n never stated — the caption and text give r values but never the number of compounds in the series | CC-BY 4.0, **no ND clause**; license banner on every page, stated p1 |
| 1B | 3 | Diagonal histograms of the pIC50 distribution for each receptor | histogram | `PLOT \| facet: receptor (5) \| vary: pIC50, ~4.5–9 (continuous) \| series: none (1) \| measure: compound count \| mark: bar \| n: NOT REPORTED` | 5 diagonal cells of the same 5×5 grid; same figure letter region as 1A, split here because mark and measure both differ | y-axis of the top-left histogram is labelled "M1" and scaled 0–1.00 rather than as a count, so the histogram measure is ambiguous | CC-BY 4.0, no ND, p1 |
| 1C | 3 | Upper-triangle Pearson r values between receptor pairs, colour-coded at the 0.77 threshold | heatmap-style annotated matrix (text in cells, colour-encoded) | `MATRIX \| rows: muscarinic receptor (5) \| cols: muscarinic receptor (5) \| value: Pearson r between the two receptors' pIC50 series, printed and colour-coded (blue ≥ 0.77, red < 0.77) \| facet: none (1)` | 10 upper-triangle cells; a two-colour binary encoding on a continuous quantity | binary blue/red colouring discards the magnitude it encodes — 0.51 and 0.76 render identically; only the printed number recovers it | CC-BY 4.0, no ND, p1 |
| 2A | 6 | Boltz-2 co-folded poses of the same ligand in JNK1 (test) and JNK2 (train), superposed, with 3.5 Å residues | structure render | `RENDER \| facet: none (1) \| views: 1 (single camera angle into the ATP site) \| overlay: 2 predictions (JNK1 orange, JNK2 gray) on 0 references \| axis: none` | 1 panel; the two entries vary by data-split membership, colour-legended "Train data point" / "Test data point" | the claim "virtually indistinguishable" is supported by no quantitative panel — no RMSD between the two poses is given, and no experimental structure is overlaid | CC-BY 4.0, no ND, p1 |
| 2B | 6 | Test-set JNK1 pIC50 against train-set JNK2 pIC50 for the whole shared compound series, r = 0.95 | scatter with regression band | `PLOT \| facet: none (1) \| vary: test-set JNK1 pIC50, 5.3–8.0 (continuous) \| series: none (1) \| measure: train-set JNK2 pIC50, 4.9–7.6 \| mark: point (with OLS line and 95% band) \| n: 1 per mark, ~20 compounds in the panel (exact n NOT REPORTED)` | 1 panel | n of the series is not printed; the regression band implies a fit whose parameters are not given | CC-BY 4.0, no ND, p1 |
| 3 | 7 | Mean Pearson r on FEP+ 4 and OpenFE for four published methods and three ligand-only baselines | bar | `PLOT \| facet: benchmark (2: FEP+ 4, OpenFE) \| vary: method (7: IsoDDE, FEP+, OpenFE, Boltz-2, Chemprop, FP + mol desc, mol desc only) \| series: method class (3: physics-based, structure-based ML, ligand-only ML baseline) \| measure: size-weighted mean Pearson r \| mark: bar \| n: 4 targets per bar (FEP+ 4 facet), 39 targets per bar (OpenFE facet); bootstrapped 95% CI on the three ligand-only bars only` | 2 panels varying by benchmark; bar order differs between panels (ranked by value), so the same method sits in different positions left and right | **bars hide the per-target distributions** they average — no per-target points are shown for any method; **error bars are present only on the ligand-only bars**, so the published methods appear as point estimates with no uncertainty, which is exactly the comparison at issue; n per bar is not printed in the figure; the four published values are re-used from [16] rather than rerun and the panel does not mark them as such | CC-BY 4.0, no ND, p1 |
| 4A | 8 | Mean Pearson r of the three ligand-only baselines across the five NTAB ligand-novelty tiers | line with CI band | `PLOT \| facet: none (1) \| vary: max Tanimoto similarity to train/val, 5 bins ([0.00,0.35), [0.35,0.50), [0.50,0.70), [0.70,1.00), =1.00) \| series: baseline model (3: Chemprop, FP + mol desc, mol desc) \| measure: mean Pearson r (unweighted across assays) \| mark: line + point, shaded bootstrapped 95% CI \| n: per bin n_a = 24 / 235 / 340 / 112 / 111 assays, n_m = 1108 / 6106 / 7383 / 2114 / 4396 measurements` | 1 panel; n_a and n_m printed under every bin — the paper's best-labelled figure | | CC-BY 4.0, no ND, p1 |
| 4B | 8 | Mean absolute error of the same three baselines across the same five tiers | line with CI band | `PLOT \| facet: none (1) \| vary: max Tanimoto similarity to train/val, 5 bins (as 4A) \| series: baseline model (3) \| measure: mean absolute error (log10 units) \| mark: line + point, shaded bootstrapped 95% CI \| n: as 4A` | 1 panel, sharing the x-axis and legend of 4A; split from 4A because the measure differs | MAE axis starts at ~0.55 rather than 0 — a truncation, though it does not cross a meaningful zero for an error metric | CC-BY 4.0, no ND, p1 |
| 5 | 8 | Number of correlated ChEMBL assay pairs surviving each sequence-similarity cutoff from 0.1 to 0.9 | scatter | `PLOT \| facet: none (1) \| vary: sequence similarity cutoff, 0.1–0.9 in steps of 0.1 (9 levels) \| series: none (1) \| measure: number of assay pairs with R² ≥ 0.6 \| mark: point \| n: 1 per mark, each derived from the 59,552-pair census` | 1 panel | no uncertainty shown on a count derived from a filtering cascade; the cumulative-vs-binned reading of "cutoff" is not stated in the panel | CC-BY 4.0, no ND, p1 |
| 6 | 10 | Two OpenFE leakage cases: test-set experimental −ΔG against the same compounds' train-set pIC50 for a related target | scatter with regression band | `PLOT \| facet: target pair (2: miscellaneous BTK vs train LCK CHEMBL3588238; merck TNKS2 vs train TNKS CHEMBL4322251) \| vary: test-set experimental −ΔG (continuous, ~8–11 and ~9–13 kcal/mol) \| series: none (1) \| measure: train-set pIC50 of the same compounds \| mark: point (with OLS line and 95% band) \| n: 6 of 6 ligands (BTK panel), 19 of 27 ligands (TNKS2 panel), printed as c in each panel` | 2 panels varying by target pair; each annotated with r, s (sequence identity) and c (coverage) | axis units differ between the two panels' x-axes (−ΔG scales differ) with no shared scale, so the two cases are not visually comparable | CC-BY 4.0, no ND, p1 |
| 7 | 11 | Reproduction of the Boltz-2 similarity-vs-performance diagnostic with a ligand-only model; Tukey-HSD non-significant | scatter with mean and CI | `PLOT \| facet: none (1) \| vary: mean maximum Tanimoto similarity to the training set, 4 buckets ([0.3,0.5), [0.5,0.65), [0.65,0.8), [0.8,1.0]) \| series: none (1) \| measure: per-assay Pearson r (grey points) and bucket mean (blue point) \| mark: point + 95% CI error bar over jittered per-assay points \| n: per bucket n_a = 16 / 21 / 11 / 10 assays, n_m = 304 / 330 / 128 / 111 measurements` | 1 panel; both the individual assays and their mean are drawn, which is what makes the null result readable | | CC-BY 4.0, no ND, p1 |
| 8A | 13 | Mean Pearson r of the three baselines when bins are formed by *assay-average* rather than per-compound similarity | line with CI band | `PLOT \| facet: none (1) \| vary: assay-average max Tanimoto similarity, 3 bins ([0.00,0.33), [0.33,0.66), [0.66,1.00)) \| series: baseline model (3: Chemprop, FP + mol desc, mol desc) \| measure: mean Pearson r (unweighted across assays) \| mark: line + point, shaded bootstrapped 95% CI \| n: per bin n_a = 5 / 546 / 374 assays, n_m = 747 / 16,753 / 11,437 measurements` | 1 panel | the leftmost bin rests on **n_a = 5 assays** and its CI band spans roughly 0.0–0.4; the line is drawn through it at equal visual weight to bins with 546 and 374 assays | CC-BY 4.0, no ND, p1 |
| 8B | 13 | Mean absolute error of the same three baselines under assay-average binning | line with CI band | `PLOT \| facet: none (1) \| vary: assay-average max Tanimoto similarity, 3 bins (as 8A) \| series: baseline model (3) \| measure: mean absolute error (log10 units) \| mark: line + point, shaded bootstrapped 95% CI \| n: as 8A` | 1 panel sharing 8A's x-axis; split because the measure differs | same n_a = 5 leftmost bin, here with a CI band spanning ~1.0–2.1; MAE axis starts at ~0.6 | CC-BY 4.0, no ND, p1 |

Tables (not figure rows, listed for retrieval): Table 1 census cascade (p4); Table 2 20-row sample
of correlated assay pairs with R² and sequence similarity (p5); Table 3 related targets per FEP+ 4
test target by split (p6); Table 4 the twelve RDKit descriptors (p12); Table 5 baseline architecture
(p12).

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), session of 2026-09-08
- **schema_version**: **v3**
- **confidence**: **high** for A, B, D, E and the benchmark construction in C; **medium** for the
  approximate curve values in Fig 4 and Fig 8 marked *(read from rendered panel)*, and for the
  Fig 1B histogram measure, whose y-axis label is ambiguous in the rendered panel. The text layer
  extracted cleanly and every headline number is printed in running text or as a panel label; the
  only values I had to read off marks are the intermediate NTAB tiers, and the two anchors of that
  curve (0.61 and 0.14) are printed on p8.
- **unresolved**:
  1. **How "similar binding pockets" was determined for Table 3 (p6) is never stated.** The table is
     the paper's evidence that leakage is not confined to JNK1/JNK2, and the grouping criterion —
     pocket-residue identity? a structural alignment? expert judgement? — is absent from both the
     caption and Appendix A. This is the weakest-supported claim in the paper.
  2. **Boltz-2 and IsoDDE are never evaluated on the Novelty-Tiered Affinity Benchmark.** The paper
     establishes a leakage floor (r = 0.14) but reports no co-folding number above it, so the
     question its own title implies — how much of Boltz-2's 0.66 survives leakage control — is left
     open. The authors say as much for memorisation specifically (p7) but do not flag the missing
     arm.
  3. **No hyperparameter search is described** for the ligand-only baselines. Table 5 (p12) fixes
     d = 2048, d_target = 256, n_hidden = 4 and the schedule (p11) with no sweep, no seed count and
     no replicate runs. Whether a range was tuned against the FEP+ 4 / OpenFE test sets — the v3
     route-4 concern — therefore cannot be checked either way.
  4. **The Fig 2 Boltz-2 run has no reported configuration** — templates on/off, MSA depth, seeds,
     number of samples, which of several poses is shown. It carries no number, but it is the only
     structural evidence for the "same binding environment" claim.
  5. **The Fig 5 sweep's semantics are ambiguous**: whether each x value is a cutoff applied
     cumulatively (all pairs below that identity) or a bin is never said. The 0.9 point (≈ 6,100)
     matches the cumulative reading against Table 1's 6,115, so cumulative is almost certainly
     right, but it is inferred.
  6. **Distinct target counts are never given** — for the 6,115 correlated pairs, and for the NTAB
     tiers. Only assay and measurement counts are reported, so the census cannot be read as a
     statement about how many *proteins* mirror.
  7. **Schema gap: v3 has no field for "published claims this paper disputes."** The parent task
     required it and it does not fit `necessity_claims` (those are the extracted paper's own
     load-bearing sentences), `stated_limits`, or `stance`. I added an explicitly labelled
     `disputed published claims` block inside section D rather than distort an existing field. A
     `disputed_claims` field with columns `claim` | `whose` | `grounds` | `about
     (benchmark/model/comparison)` | `page` would belong in section D — this is the second paper in
     the corpus (after `skrinjar2026generalization`) whose whole point is a dispute with a named
     prior result.
  8. **Schema gap: v3 has no field for a proposed protocol or standard.** The splitting procedure is
     the most reusable content in this paper and had no home; I recorded it as a labelled block in
     section D alongside `anti_memorization_design`, which is the closest existing field but is
     scoped to what the paper *ran*, not what it *proposes others adopt*.
  9. **Tags I needed and could not use** (recorded, not invented): there is no method tag for
     **affinity/potency prediction** — `benchmark-only` is the only fit and it loses the fact that
     this paper is about ΔG/pIC50 rather than structure; no tag for **data leakage** or
     **leakage-controlled split** as a subject, which is this paper's entire contribution and the
     property a future query would most plausibly search on; no tag for a **ligand-only / no-protein
     baseline**, the paper's central instrument; no tag for a **temporal / date-cutoff split**
     (`anti-memorization` covers the intent but not the mechanism, and cannot distinguish a date
     split from a similarity split — a distinction this paper shows matters, r = 0.32 vs 0.14). I
     also considered `cofolding` (the authors run Boltz-2 once, for a picture) and
     `no-template-no-msa` (their probe uses neither, but it is not a structure predictor) and
     declined both as false positives.
  10. **`multi-backbone` judgement call**: Figure 3 puts Boltz-2 and IsoDDE side by side, but the
      values are quoted from [16] rather than rerun, and two backbones is not "more than two". Not
      tagged. Flagging in case the corpus wants the tag to cover literature-sourced comparisons.
  11. **`saturating-metric` judgement call**: tagged on the strength of per-assay Pearson r reaching
      exactly ±1.00 in Fig 7 (p11). The paper's *headline* means never approach the ceiling. If the
      tag is meant only for a paper's primary reported metric, remove it.
- **why_it_matters**: *(left empty by the extractor — the user's call)*

## Tags

`general-protein` `kinase` `gpcr` `benchmark-only` `continuous-metric` `saturating-metric`
`anti-memorization` `design-level-oracle` `preprint` `threat` `precedent` `negative-result`
`comparator-numbers`

Tag notes: `gpcr` and `kinase` are tagged alongside `general-protein` because the muscarinic case
study (§3, p3–4) and the all-kinase FEP+ 4 benchmark (p4) are substantive named arms, not
incidental examples; a reverse lookup for either should return this paper.
`design-level-oracle` is route 7 only — the demonstrative case studies were chosen because the
correlation was known in advance (p3, p5) — and is **not** `oracle-leak`, which is genuinely absent
here. `anti-memorization` is tagged on the Novelty-Tiered Affinity Benchmark, which is both designed
and run (five tiers, plus a temporal-split-only arm). `negative-result` covers two negatives: the
benchmarks are contaminated, and the Boltz-2 similarity diagnostic lacks the power to detect
memorisation (p11). No state-handling, control-handle or site tag applies — the paper contains no
conformational content.
