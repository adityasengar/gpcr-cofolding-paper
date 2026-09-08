# ku2026promise

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–21)** and coincide with the
printed page numbers. Layout: p1 title/abstract/Introduction, p2–5 Methods (Table 1 on p2,
Figure 1 on p3), p5–9 Results & Discussion (Figure 2 on p6, Figure 3 on p8), p9 Limitations +
Conclusion + Acknowledgments, p9–11 references, p12–21 Appendix A (Related work p12, dataset
curation p12–13, Algorithm 1 p13, Algorithm 2 p14, Figures S1–S9 and Table S1 on p14–21).

**Supplementary material IS held**: Appendix A with Figures S1–S9 and Table S1 is inside this
PDF (p12–21). Several per-model numbers exist only as in-figure annotations, not in prose; where
I read a number off a rendered figure page I say so. Pages 6, 8, 14 and 17 were rendered at
150 dpi and read as images, then deleted; all other figures were filled from their captions.

**A caveat recorded up front because it affects `A. Identity`:** the held PDF is a bioRxiv
preprint ("not certified by peer review", p1 banner) whose own footer simultaneously declares
it "Proceedings of the 43rd International Conference on Machine Learning, Seoul, South Korea.
PMLR 306, 2026" (p1). Both statements are on page 1. Tagged `preprint` on the evidence of the
banner; see `unresolved`.

---

## A. Identity

- **citekey**: `ku2026promise`
- **doi**: **10.64898/2026.06.11.731790** (bioRxiv) — p1 banner: "bioRxiv preprint doi:
  https://doi.org/10.64898/2026.06.11.731790; this version posted June 12, 2026". Matches
  `MANIFEST.csv` and `refs.bib`. Note the `10.64898` prefix rather than bioRxiv's usual
  `10.1101`; recorded as printed.
- **year**: **2026** — posted 12 June 2026 (p1).
- **venue**: **DUAL, as printed on p1.** (i) bioRxiv preprint, explicitly "not certified by peer
  review" (p1 banner); (ii) "Proceedings of the 43 rd International Conference on Machine
  Learning, Seoul, South Korea. PMLR 306, 2026. Copyright 2026 by the author(s)." (p1 footer).
  **Tagged `preprint`** per the held artefact; `peer-reviewed` NOT tagged because nothing in the
  PDF states an acceptance decision, only a proceedings template line. See `unresolved`.
- **title**: ProMiSE: Protein Multi-State Evaluation Benchmark in Biological Contexts — p1
- **authors**: Bonjae Ku\*, Seeun Kim\*, Yubeen Kim\* (equal contribution), Hahnbeom Park,
  Chaok Seok — p1. Affiliations: Department of Chemistry, Seoul National University (Ku, S.
  Kim, Y. Kim, Seok); Korea Institute of Science and Technology, KIST (Park). Correspondence:
  Hahnbeom Park <hahnbeom@kist.re.kr>, Chaok Seok <chaok@snu.ac.kr>. Five authors.

## B. Scope

- **system**: **general protein** — a PDB-wide, family-agnostic benchmark built from RCSB
  sequence clusters, not from any one protein family. p2 §2.1.1: "we retrieved sequences from
  the RCSB PDB grouped into clusters with ≥ 95% sequence identity." Functional composition is
  reported only as Gene-Ontology donut charts (Figure S1, p14), whose wedge labels are: for
  intrinsic — Other, Structural, Transport, Hydrolase, Regulatory, Biosynthesis, Transferase,
  Isomerase, Viral; for ligand-induced — Transport, Transferase, Biosynthesis, Other, Hydrolase,
  Ligase, Lyase; for protein-induced — Other, Regulatory, Hydrolase, Transport, Structural,
  Immune, Transferase (read from the rendered p14 image). **No receptor / signalling / GPCR
  category appears in any of the three panels.** Caption claim, p14: "The resulting distribution
  indicates that the dataset spans a broad range of functional categories without
  over-representation of redundant protein groups."
  **GPCR content: see `structural_priors_used` and `stated_limits` — there is no GPCR in the
  benchmark, and the construction rule excludes them by design.**
- **n_targets**: multi-level; a single number misrepresents it. All from Table 1, p2:

  | level | intrinsic | ligand-induced | protein-induced | total |
  |---|---|---|---|---|
  | sequence clusters (non-redundant families at 40% seq id) | 72 | 87 | 75 | **234** |
  | entries (unique PDB structures) | 162 (162 apo / — holo) | 435 (92 apo / 343 holo) | 189 (81 apo / 108 holo) | **786** |
  | pairs (entry combinations, TM-score < 0.8) | 109 | 350 | 118 | **577** |

  Before filtering: "In total, 1,333,459 multi-state pairs were retrieved" (p12; also p2).
  Within the intrinsic category, "the dataset contains 72 clusters, with 58 two-state systems
  and 14 systems with three or more states" (p2). BioEmu was in practice evaluated on **71** of
  the 72 intrinsic clusters, not 72 (Figure 2B annotation "N=50/71", read from rendered p6);
  the text does not explain the missing cluster.
- **method_class**: **benchmark-only.** The paper contributes a curated dataset plus an
  evaluation scheme and runs five existing predictors on it; it proposes no new predictor and
  modifies no inference pipeline. p1 abstract: "We introduce ProMiSE, the first benchmark that
  provides both a dataset and an evaluation scheme". p5 §2.5: dataset and code at
  https://github.com/seoklab/promise-bench.
- **backbones**: **AlphaFold3, Boltz-1, Boltz-2, Chai-1, BioEmu** — p2 §2.2: "Structures were
  predicted for all three dataset categories using AlphaFold3 (AF3), Boltz-1, Boltz-2, Chai-1,
  and BioEmu. BioEmu was applied only to the intrinsic multi-state set." Chai-1 is further
  "excluded from the conformational bias analysis" because it "does not provide pair
  representations" (p3 §2.4). **Tag `multi-backbone`** (five backbones, four on all categories).
  No AF2 inference of its own, though BioEmu carries "the same AlphaFold2 pairformer (frozen)"
  (p7 §3.4).
- **templates**: **NOT REPORTED.** The inference protocol (p2 §2.2) states seeds, sample counts,
  MSA source and MSA pairing, but never says whether any model's structural-template channel was
  on, off, or at repository default. The word "template" does not appear in the methods.
- **msa_handling**: **full, unmodified, single alignment per target — with one MSA-free arm.**
  p2 §2.2: "MSAs were retrieved from the ColabFold server (Mirdita et al., 2022) using MMseqs2
  (Steinegger & Söding, 2017). For multimeric inputs, MSA pairing was performed using the
  internal pairing algorithm of Boltz-2. Chai-1 predictions were run without MSA input."
  **No subsampling, no clustering and no state-filtering of MSAs anywhere.** MSAs are used a
  second time, analytically, to compute an MSA holo-preference score (`MSA_holo`, p4–5 §2.4.4)
  from MSA-Transformer attention over state-unique contacts; that is a diagnostic, not an
  intervention on the input.

## C. Conformational core

- **states_generated**: **ensemble + single-state.** Ensemble by protocol — p2 §2.2: "Each
  structure was predicted with 10 independent random seeds, generating 10 samples per seed,
  yielding 100 structural predictions per entry" (BioEmu instead "uses a single seed with 100
  samples", Figure 3B caption, p8). Single-state in result — that collapse *is* the paper's
  finding: "both intrinsic multi-state and ligand-induced sets exhibit systematic bias toward a
  single state—a phenomenon we term *conformational collapse*" (p6); "For AF3, Boltz-1, and
  Boltz-2, a given distogram maps to a narrow range of structural outputs" (p8).
- **structural_priors_used**: extensive, and legitimate for a benchmark — this is where the
  "both states are deposited" design belongs.
  1. **Both states of every system are deposited PDB structures, by construction.** p2 §2.1.1:
     "we retrieved sequences from the RCSB PDB grouped into clusters with ≥ 95% sequence
     identity. For each sequence cluster, we performed all-against-all pairwise TM-score
     calculations and grouped entries into conformational clusters via agglomerative
     clustering."
  2. **Pair selection uses a global-similarity cut on the two deposited states.** p2 §2.1.1:
     "For sequence clusters with multiple conformational clusters, we selected pairs of
     assemblies from different conformational clusters with TM-score < 0.8, yielding 1,333,459
     initial pairs." Restated p2 §2.1.3: "we collected conformations for each protein and then
     selected conformational pairs exhibiting structural transitions (TM-score < 0.8)."
  3. **Mechanism labels are read off the deposited assemblies** (ligand present/absent, chain
     count) — see the taxonomy below, p2 §2.1.3.
  4. **Deposited assembly composition sets the model input.** Apo-conditioned and
     holo-conditioned inputs reproduce the ligand/partner composition of the deposited apo and
     holo assemblies respectively (p3 §2.3.1, p12 A.2.1: "Lists of chains and ligands per
     assembly were maintained throughout the filtering process and used for classifying induced
     changes"). Ligands were curated by distance: "Ligands located beyond a 5 Å distance cutoff
     from the protein were removed. Metal ions were retained only if they coordinated with two
     or more residues within 5 Å" (p12).
  5. **A single representative sequence per cluster** was chosen using binding-site residues
     defined from the deposited complex: "we defined the binding site as residues within 5 Å of
     the binding partner and identified binding-site mismatches across entries in the same
     cluster" (p13).
  6. **Training-set exposure is estimated from deposited structures** by MMseqs2 + Foldseek
     search: "similar training entries were defined as chain- or interface-level entries with
     sequence identity >0.8 and TM-score >0.9 to the query state" (p4 §2.4.3).
- **oracle_leakage** — seven routes, each answered separately. Summary: **no coordinate leakage
  into the predictors; heavy, and openly declared, design-level and post-hoc-scoring oracle
  use.**
  1. **Structures used as input or template — NONE FOUND (with one qualification).** The stated
     inference protocol is sequence + MSA + assembly composition only (p2 §2.2, quoted under
     `msa_handling`); no experimental coordinates are fed to any model, and no template channel
     is mentioned. Qualification: the *composition* of the holo assembly (which ligand, how many
     partner chains) is taken from the deposited holo entry, so the model is told that a ligand
     or a partner is present even though it is never told where anything sits. Protocol page:
     p2 §2.2; composition source p12 A.2.1.
  2. **State annotations from a curated state database (GPCRdb / KLIFS / Kincore) driving
     templates or alignments — NONE FOUND.** No such database is used or cited anywhere. State
     labels are generated de novo by agglomerative clustering on all-against-all TM-scores
     (p2 §2.1.1; p12 A.2.1). Protocol described p2 §2.1.1 and p12–13 A.2.
  3. **Cluster labels derived from known states — PRESENT, in dataset definition (not in the
     prediction pipeline).** The conformational-cluster labels come from clustering deposited
     structures and then govern which systems enter the benchmark: "Sequence clusters containing
     only a single conformational cluster were excluded, as they do not represent multi-state
     proteins" (p12) and "we discarded sequence clusters in which apo and holo entries were
     assigned to the same conformation cluster, as this indicates that the two states are
     structurally similar and lack a detectable induction effect" (p13). These labels never
     reach a predictor; they select the evaluation set.
  4. **Hyperparameters / sweep ranges / thresholds tuned against known states — PARTIALLY
     PRESENT, and no threshold is justified.** Every operative threshold is set against the
     deposited pair and none is derived or validated: pair inclusion TM-score < 0.8 (p2, p12);
     success TM-score > 0.8 (p3 §2.3.2); dynamic-region definition |d_apo − d_holo| > 3 Å (p4
     Eq. 3); training-similarity thresholds seq id > 0.8 and TM > 0.9 (p4 §2.4.3); neutrality
     windows |Train_holo| < 0.3 and |MSA_holo| < 0.3 (p7 §3.3.2); "spans both states" defined as
     "at least one Struct_holo < −0.5 and one > +0.5" (Figure 3C caption, p8); AF3 training
     weights β_chain = 0.5, β_interface = 1, α_prot = 3, α_ligand = 1 taken from AF3's reported
     regime (p4). **A cutoff *range* was explicitly explored against the evaluation data**, p9:
     "A complementary criterion of 0.8 < TM-score < 0.9 with RMSD > 3 Å captured GPCR
     multi-state cases (e.g., ligand-induced: PDB IDs 7UL5 and 7WIG; protein-induced: 7UL5 and
     7T10)" — i.e. the authors checked what a different cutoff would have captured, then
     retained the stricter one. By the v3 rule this counts even though no per-target value is
     picked.
  5. **Success defined post hoc by RMSD/TM to a structure they held — PRESENT and central.**
     p3 §2.3.2: "state-level success is defined as: a prediction with a TM-score > 0.8 to the
     target state and higher than to all other states"; "Apo success: TM_apo(P_apo) > 0.8 ∧
     TM_apo(P_apo) > TM_holo(P_apo)". Also every bias score (Struct_holo, Eq. 1) is an RMSD ratio
     against both held references (p4 §2.4.1). Unavoidable for a benchmark of this design, but
     recorded because it means no result here is independent of the deposited answer.
  6. **Best/worst model labels assigned against a held reference — PRESENT, in the figure
     exemplars and in the induced-set scoring.** Figure 2D caption, p6: "PDB 6YED, gray; PDB
     6YEB, tan) with Boltz-2 predictions (blue), **where the prediction closest to state 1 was
     selected**" and "AF3 apo-conditioned prediction (pink), **where the prediction closest to
     the apo state was selected**". Also p3 §2.3.2: "TM_apo(P) = max_{a∈A} TM(P, a) … using the
     best-matching apo reference for each prediction."
  7. **Design-level oracle use — PRESENT (weaker than pipeline leakage; label it as
     design-level).** Systems are in the benchmark *because* two states are already deposited
     (route 3 above), and the expected answer is declared before the prediction is read: an
     apo-conditioned input is scored as a failure unless it reproduces the deposited apo state,
     and a holo-conditioned input unless it reproduces the deposited holo state (p3 §2.3.2).
     For the intrinsic set the labels are admitted to be arbitrary: "For intrinsic multi-state
     pairs, we therefore assign apo and holo labels arbitrarily to maintain a unified evaluation
     framework, without implying any biological asymmetry" (p2).
- **prospective**: **no.** Every target is a pair of already-deposited structures selected for
  the benchmark on the basis of those deposits (p2 §2.1.1, p12 A.2.1); there is no post-cutoff
  set, no blind arm, and no experimental follow-up. The pipeline fed to the predictors is
  nevertheless clean of coordinates (route 1 NONE FOUND), so the failure it reports is a real
  prediction failure — it is the *target selection*, not the inference, that is retrospective.
- **state_metric**: **binary predicate + RMSD-to-reference (continuous).** Both are used, and
  the whole benchmark is built on **global similarity to a reference structure**; no
  local/site-level or feature-based predicate exists anywhere in it.
  - *Binary predicate, state level* (p3 §2.3.2, verbatim): "state-level success is defined as: a
    prediction with a TM-score > 0.8 to the target state and higher than to all other states."
  - *Binary predicate, cluster level* (p3): "Cluster-level success is defined as: among 100
    sampled predictions, at least one state-level success for each known conformational state in
    the cluster." This is the headline metric in Figure 2A.
  - *Binary predicate, induced sets, pair level* (p3): "success is evaluated at the pair level
    and requires both apo and holo success", with Apo success = TM_apo(P_apo) > 0.8 ∧
    TM_apo(P_apo) > TM_holo(P_apo) and Holo success = TM_holo(P_holo) > 0.8 ∧ TM_holo(P_holo) >
    TM_apo(P_holo).
  - *Continuous, RMSD-based*: Struct_holo = (d_apo − d_holo) / sqrt(0.5(d²_apo + d²_holo +
    d²_ref)) with d = Cα-RMSD, "we adopt the ConfBench score from NeuralPLexer3 (Qiao et al.,
    2025)" (p4 Eq. 1). Threshold used for "spans both states": Struct_holo < −0.5 and > +0.5
    (Figure 3C caption, p8). Companion continuous scores: DynDisto_holo (p4 Eqs. 2–6, dynamic
    region = residue pairs with |d_apo − d_holo| > 3 Å), Train_holo (p4 Eqs. 7–8), MSA_holo (p5
    Eq. 9, contacts = heavy-atom distance < 8 Å excluding |i−j| ≤ 3).
  - *Complex-level auxiliaries* (Figure S3 caption, p16): "Success is defined as DockQ ≥ 0.23
    for the protein-induced set and ligand RMSD ≤ 2 Å for the ligand-induced set."
  - *Alignment protocol* (p3 §2.3.1): UCSF Chimera MatchMaker, default options; "Cα-RMSD and
    TM-score were calculated over aligned regions, excluding disordered or unresolved segments."
  - **No threshold in the list above is justified in the paper.** TM > 0.8 for success and
    TM < 0.8 for inclusion are asserted, never derived.
- **metric_saturation**: **YES, stated by the authors, in the ligand-induced holo-conditioned
  arm.** p7 §3.3.2 verbatim: "In the ligand-induced holo-conditioned setting, both the distogram
  and final structure predictions were already strongly biased toward the holo state, which
  likely saturated the signal and made the corresponding correlation estimates noisy." That
  saturation shows up as near-zero / sign-flipping correlations for holo-conditioned
  ligand-induced panels (Figure S8, p20: AF3 r = 0.117, Boltz-1 r = −0.057, Boltz-2 r = −0.100).
  A second, structural saturation: holo-conditioned failure in the ligand-induced set is already
  down at 4–17% of entries (Figure S5B, p17), leaving little room for a model to differ.
  Floor effect on the intrinsic set: Boltz-1 reaches 0.08 cluster-level success (Figure 2A, p6),
  close to the metric's floor. No axis break or truncation was observed anywhere — see `hides`
  in section F for figure-level defects, which are recorded there and not here.
- **directional_control**: **the only handle is biological context supplied as input
  composition — ligand present/absent, protein partner present/absent.** That handle is what the
  benchmark tests, and it is reported not to work in the ligand-induced set: "apo-conditioned
  predictions (blue boxes) systematically shift toward positive values, indicating collapse to
  holo-like conformations even in the absence of ligands" (p5). There is **no** state-annotated
  template, **no** state-filtered or subsampled MSA, and **no** seed or depth knob used to steer
  state; seeds are used only for replication (10 seeds × 10 samples, p2). The one architectural
  handle identified is not an inference-time control at all but a training-time one: BioEmu
  "uses the same AlphaFold2 pairformer (frozen) but fine-tunes only the structure decoding
  module on MD trajectory data" (p7 §3.4).
- **anti_memorization_design**: **NONE.** There is no held-out set, no post-cutoff set and no
  training-date cutoff defined anywhere in the paper; the benchmark is drawn from the PDB with
  no temporal filter (p2 §2.1.1, p12–13 A.2). What exists instead is an *estimate of training
  exposure per system*: "we estimated model-specific training exposure for the apo and holo
  states. Effective training hits were computed within the model-accessible training search
  space, incorporating the curation filters and weighted sampling scheme used during training"
  (p4 §2.4.3), with similarity defined as "sequence identity >0.8 and TM-score >0.9 to the query
  state" searched by MMseqs2 and Foldseek. Tag `no-anti-memorization`.
- **anti_memorization_control**: **NO HELD-OUT ARM RUN; a correlational memorization analysis
  WAS run.** No arm partitions the benchmark by training-set membership and re-reports success.
  What was run: (i) Train_holo vs the post-distogram shift, with MSA held neutral — "we
  restricted the analysis to pairs with minimal training set skewedness (|Train_holo| < 0.3) …
  Conversely, we selected pairs with weak MSA signal (|MSA_holo| < 0.3) and colored the
  corresponding points according to Train_holo" (p7 §3.3.2), result: "Across models, MSA_holo
  showed little to no correlation with this shift, whereas Train_holo exhibited a consistent
  positive correlation" (p7); (ii) a single outlier case study at domain rather than chain
  resolution (6crf / 7xhq, "Train^domain_holo = −0.1148", p7); (iii) the BioEmu comparison as a
  positive control for the structure-module hypothesis (p8). **Mark the outlier case study
  `UNPOWERED` (n = 1 cluster, p7).** The correlational analyses are adequately powered
  (350 ligand-induced pairs, 118 protein-induced pairs) but are association, not ablation:
  nothing here separates a memorized system from an unmemorized one and re-measures success.
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Apo-conditioned vs holo-conditioned input on the same target, all induced pairs | Rules out that models are simply inaccurate rather than context-insensitive; isolates *directional* failure | p3 §2.3.1, p5 §3.2, Fig 2C p6 |
  | Chai-1 run with no MSA at all | Rules out that competitive multi-state performance requires MSA depth ("Chai-1 shows balanced performance across categories despite its MSA-free setting", p5) | p2 §2.2, p5 |
  | Distogram stage (DynDisto_holo) vs structure stage (Struct_holo) on identical predictions | Localizes where bias is introduced; rules out "the pair representation already decided it" | p3 §2.4, p6–7 §3.3.1, Fig S4 p16, Fig S6 p18 |
  | Restrict to \|MSA_holo\| < 0.3, colour by Train_holo (Fig S8) | Rules out MSA coevolutionary signal as the driver of the post-distogram holo shift | p7 §3.3.2, p20 |
  | Restrict to \|Train_holo\| < 0.3, colour by MSA_holo (Fig S9) | Rules out training-set skew as the driver, in the complementary regime | p7 §3.3.2, p21 |
  | BioEmu (frozen AF2 pairformer, structure module fine-tuned on MD) vs AF3/Boltz-1/Boltz-2, paired Wilcoxon | Positive control: rules out "diverse output needs diverse pair representations" — diversity rises with the trunk frozen | p8 §3.4, Fig 3B |
  | Confidence-ranked top-k vs uniform-random top-k at matched budget k ∈ {10, 50} | Rules out confidence scores as a selector for alternative states | p5 §3.2, Fig S2 p15 |
  | Hit rate within *already-successful* clusters (Table S1) | Rules out "the model found the state but rarely" — i.e. distinguishes discovery failure from sampling sparsity | p5 §3.2, p15 |
  | Domain-level vs chain-level training-set search on the outlier cluster (6crf/7xhq) | Rules out that memorization operates only at chain resolution; n = 1, unpowered | p7, Fig S7 p19 |
  | Crystal-artifact removal via PRODIGY-cryst (Algorithm 1) | Rules out crystal-packing contacts masquerading as biological protein-induced partners | p2 §2.1.2, p13 |
  | Discard sequence clusters where apo and holo land in the same conformational cluster | Rules out pairs with no detectable induction effect — **also excludes small-amplitude real transitions**, see `stated_limits` | p13 |
  | Monomer accuracy vs complex accuracy correlation (DockQ / ligand RMSD) | Rules out that monomer conformational error is irrelevant to complex prediction | p6, Fig S3 p16 |

- **confidence_as_discriminator**: **Tested explicitly and REJECTED — a rare and valuable
  negative result.** p5 §3.2 verbatim: "model confidence scores do not provide a reliable
  solution to this discovery problem: confidence-based selection fails to outperform uniform
  random sampling in cluster-level success rate (Figure S2), indicating that current confidence
  estimates are poorly calibrated for identifying alternative experimentally observed states."
  Figure S2 caption, p15: "Selecting predictions based on the model's top confidence scores
  (Confidence Top-10) yields cluster-level success rates that are nearly identical to, or
  occasionally outperformed by, uniform random sampling from the generated ensemble … making
  self-reported confidence a poor metric for evaluating multi-state sampling quality."
  Confidence was therefore *not* used as a discriminator in any reported result; it was audited
  as an object of study. Tag `confidence-as-discriminator` on that audit.

### C-supplement. The mechanism taxonomy (the reason this note exists)

Three categories, defined in §2.1.3 on **p2**, verbatim, with the number of sequence clusters /
entries / pairs from Table 1 (p2) and the assignment rule as stated:

| category | verbatim definition (p2) | clusters | entries (apo/holo) | pairs | how systems were assigned |
|---|---|---|---|---|---|
| **Intrinsic Multi-State** | "Both structures are monomeric and ligand-free, capturing conformational changes inherent to the protein sequence itself." | 72 | 162 (162 / —) | 109 | Both members of the pair monomeric and ligand-free, read from the deposited assembly's chain and ligand lists (p12 A.2.1) |
| **Ligand-induced** | "In this study, we refer to ligands as small-molecule ligands only. One structure in these pairs is monomeric and ligand-free (apo), while the other is ligand-bound (holo), capturing conformational changes triggered by small-molecule binding." | 87 | 435 (92 / 343) | 350 | One member monomeric+ligand-free, the other monomeric+ligand-bound; **small molecules only** — peptides, nanobodies, G proteins and every other protein partner are excluded from this category by definition |
| **Protein-induced** | "One structure is monomeric and ligand-free (apo), while the other is a multimeric assembly (holo, ≥2 protein chains). To isolate the effect of protein–protein interactions, we required that the small-molecule ligand profile of the target chain remain identical between the two structures." | 75 | 189 (81 / 108) | 118 | One member monomeric+ligand-free, the other ≥2 protein chains, **with the small-molecule ligand profile of the target chain held identical across the pair** — this is the explicit de-confounding rule that keeps ligand effects out of the protein-induced arm |

Cross-cutting rules that apply to all three:

- Every pair must satisfy **TM-score < 0.8** between the two deposited states (p2 §2.1.1 and
  §2.1.3; p12 A.2.1).
- Naming convention, p2: "For consistency, we refer to the binding-partner–free structure as
  apo, and the bound structure (ligand-bound or multimeric) as holo."
- Intrinsic labels are arbitrary, p2: "In the case of intrinsic multi-state, both structures are
  ligand-free monomers, and thus a biologically meaningful apo/holo distinction does not exist.
  … we therefore assign apo and holo labels arbitrarily … without implying any biological
  asymmetry."
- The categories are **mutually exclusive by construction and deliberately conservative**, p9:
  "The biological contexts of conformational change often overlap, and some entries do not fit
  cleanly into a single category under our current annotation scheme. This is particularly
  challenging for multimeric assemblies with bound ligands, where protein-induced and
  ligand-induced effects can be coupled. We therefore used conservative category definitions in
  this work and leave the incorporation of multimeric assemblies with ligand contexts to future
  benchmark extensions." **So a system with both a ligand and a protein partner is in neither
  arm.**
- Entry-selection differs by category, p13: "for the intrinsic multi-state set, we retained only
  one entry per conformation label; for the ligand-induced and protein-induced sets, we allowed
  multiple entries with the same conformation label if they differ in their binding partners."

### C-supplement. Ligand-induced vs protein-induced: the two result sets side by side

**They differ, sharply, in three independent ways.**

*(1) Cluster-level success is lower for protein-induced in every model* (Figure 2A, p6; bar
labels read from the rendered page; the same numbers reappear as the "Success" segment of
Figure S5C, p17):

| model | intrinsic (n = 72 clusters) | ligand-induced (n = 87) | protein-induced (n = 75) | ligand − protein |
|---|---|---|---|---|
| AF3 | 0.18 | **0.50** | **0.27** | +0.23 |
| Boltz-1 | 0.08 | **0.35** | **0.19** | +0.16 |
| Boltz-2 | 0.18 | **0.42** | **0.34** | +0.08 |
| Chai-1 | 0.24 | **0.40** | **0.17** | +0.23 |
| BioEmu | 0.29 | not run | not run | — |

*(2) The failure is asymmetric for ligands and symmetric for partners.* p5–6 verbatim, ligand:
"apo-conditioned predictions (blue boxes) systematically shift toward positive values,
indicating collapse to holo-like conformations even in the absence of ligands. In contrast,
holo-conditioned predictions (red boxes) appropriately favor holo conformations. This asymmetry
demonstrates that the majority of failures of the ligand-induced set in Figure 2A arise from the
inability to predict apo conformations". p5–6 verbatim, protein: "In the protein-induced set,
the directional bias observed in ligand-induced pairs is substantially reduced (Figure 2C, right
panel). Both apo-conditioned and holo-conditioned predictions display relatively balanced
Struct_holo distributions … However, despite this apparent balance, the overall success rate
remains low (Figure 2A). This discrepancy arises because many predictions cluster near
Struct_holo ≈ 0, which by definition indicates structures that are equally distant from both apo
and holo references—neither successfully recovering the apo conformation nor the holo
conformation. Thus, unlike the systematic holo collapse in ligand-induced pairs, models in the
protein-induced set fail to sample either state, producing structures that match neither
functional state." And p7: "we focus on the ligand-induced set, where conformational collapse is
most severe and overwhelmingly directional (≥80% of apo-conditioned failures correspond to
Apo→Holo collapse across models; Figure S5)."

*(3) The failure-mode breakdown quantifies that difference* (Figure S5, p17; percentages read
from the rendered page; denominators are pairs, 350 ligand / 118 protein):

| | AF3 lig | AF3 pro | Boltz-1 lig | Boltz-1 pro | Boltz-2 lig | Boltz-2 pro | Chai-1 lig | Chai-1 pro |
|---|---|---|---|---|---|---|---|---|
| apo-task failures (S5A) | 165/350 (47%) | 51/118 (43%) | 287/350 (82%) | 57/118 (48%) | 232/350 (66%) | 57/118 (48%) | 235/350 (67%) | 55/118 (47%) |
| …of which directional Apo→Holo | **96%** | **61%** | **80%** | **44%** | **98%** | **53%** | **98%** | **47%** |
| holo-task failures (S5B) | 18/350 (5%) | 50/118 (42%) | 61/350 (17%) | 59/118 (50%) | 17/350 (5%) | 40/118 (34%) | 15/350 (4%) | 67/118 (57%) |
| …of which directional Holo→Apo | 50% | 66% | 90% | 63% | 59% | 60% | 40% | 49% |
| cluster outcome: HOLO-only fail (S5C) | 7% | 32% | 7% | 37% | 7% | 24% | 6% | 35% |
| cluster outcome: APO-only fail (S5C) | 38% | 32% | 54% | 28% | 47% | 31% | 49% | 22% |
| cluster outcome: both fail (S5C) | ~5% | 10% | ~4% | 16% | ~4% | 12% | 6% | 26% |

The cleanest single contrast: **holo-conditioned prediction almost never fails when the partner
is a small molecule (4–17% of pairs) but fails 34–57% of the time when the partner is a protein
chain.** Authors' own summary, Figure S5 caption p17: "these breakdowns support the distinction
that ligand-induced failures are *asymmetric* (collapse in a single direction, Apo→Holo),
whereas protein-induced failures are *symmetric*, with substantial collapse in both directions."

### C-supplement. GPCRs and the global-similarity exclusion rule

**Answer: the benchmark contains no GPCR, and the construction rule excludes proteins whose two
states are globally similar — twice over, by two independent criteria. The authors say so
themselves.**

1. **Global-similarity exclusion, criterion 1 — the TM-score cut.** p2 §2.1.1 verbatim: "For
   sequence clusters with multiple conformational clusters, we selected pairs of assemblies from
   different conformational clusters with **TM-score < 0.8**, yielding 1,333,459 initial pairs."
   Restated p12 A.2.1: "we selected pairs of protein assemblies that (1) belong to the same
   sequence cluster but different conformational clusters and (2) exhibit a **TM-score < 0.8**."
   Table 1 defines the released dataset as "pairs (entry combinations with TM-score < 0.8)" (p2).
2. **Global-similarity exclusion, criterion 2 — the same-conformational-cluster discard.** p13
   verbatim: "we discarded sequence clusters in which apo and holo entries were assigned to the
   same conformation cluster, **as this indicates that the two states are structurally similar
   and lack a detectable induction effect**." Also p12: "Sequence clusters containing only a
   single conformational cluster were excluded, as they do not represent multi-state proteins."
3. **The authors state, verbatim, that this removes GPCR activation** (p9, Limitations): "Our
   pair-extraction criterion, TM-score < 0.8, is also stringent and preferentially captures large
   conformational changes. Consequently, localized but biologically important motions, **such as
   GPCR TM6 displacement or transporter pocket rearrangements, may be excluded**. A complementary
   criterion of 0.8 < TM-score < 0.9 with RMSD > 3 Å captured GPCR multi-state cases (e.g.,
   ligand-induced: PDB IDs 7UL5 and 7WIG; protein-induced: 7UL5 and 7T10), suggesting a practical
   route for future expansion. We retained the stricter TM-score cutoff here due to computational
   and curation resource constraints."
4. **Consequently: the only GPCR PDB IDs named anywhere in the paper — 7UL5, 7WIG, 7T10 — are
   named as cases the released benchmark does NOT contain.** No GPCR, receptor or
   seven-transmembrane system is reported as a member of any category; the GO composition charts
   (Figure S1, p14) carry no receptor or signalling wedge in any of the three panels; the word
   "GPCR" appears in the paper only in the Limitations paragraph on p9.
5. **So the same exclusion applies here as in the two other corpus benchmarks that cut on
   TM-score.** The difference is one of framing rather than of effect: ProMiSE's cut is
   `TM < 0.8` between the two *states* (keep only large-amplitude pairs), it is stated as an
   inclusion criterion rather than a filter, and — unlike a silent threshold — the authors both
   name the class of motion it removes and demonstrate the alternative window that would recover
   it. Receptor activation is nevertheless absent by construction.

## D. Claims

- **central_conclusion**: ProMiSE is a PDB-derived, mechanism-stratified multi-state benchmark
  (intrinsic / ligand-induced / protein-induced) built from whole biological assemblies rather
  than isolated monomers. Evaluated on it, AF3, Boltz-1, Boltz-2, Chai-1 and BioEmu recover all
  known intrinsic states in only ~8–29% of clusters, collapse onto holo-like structures in the
  ligand-induced set even when given no ligand, and in the protein-induced set produce structures
  matching neither state. Tracing the pipeline, the authors place the bottleneck in the structure
  module rather than in pair-representation diversity, attribute it to training-set memorization
  rather than MSA signal, and support that with BioEmu, whose fine-tuned decoder yields more
  diverse structures from the same frozen AF2 pairformer.
- **necessity_claims** (verbatim + page):
  - p1: "It is essential to consider biological context to understand protein conformational
    changes."
  - p6: "Accurate conformational sampling of individual monomers is critical for overall complex
    structure prediction accuracy, as demonstrated by the correlation between monomer
    conformational accuracy and full complex accuracy in induced sets (Figure S3)."
  - p5 (impossibility / scope-limit): "estimating the true Boltzmann distribution of protein
    conformations remains beyond the scope of this benchmark."
  - p12 (exclusion asserted as definitional): "Sequence clusters containing only a single
    conformational cluster were excluded, as they do not represent multi-state proteins."
  - p8 (mechanistic necessity claim about the fix): "the limitation lies in the structure
    module's inability to preserve conformational diversity during decoding, constrained by
    training set memorization."
- **novelty_claims** (verbatim + page):
  - p1 (abstract): "no systematic benchmark exists to demonstrate how well current models capture
    functionally relevant dynamics. We introduce ProMiSE, **the first benchmark** that provides
    both a dataset and an evaluation scheme, based on native biological assemblies and
    integrating major conformational change mechanisms—intrinsic, ligand-induced, and
    protein-induced—within a single curated dataset."
  - p2: "Beyond providing a curated dataset, ProMiSE establishes **the first unified evaluation
    framework** that defines explicit success criteria for multi-state sampling and introduces
    quantitative metrics for assessing conformational bias across distinct biological contexts."
  - p1: "However, existing evaluations rarely consider these mechanisms within a unified
    framework and often rely on monomeric-only context rather than biologically relevant complex
    context, limiting insight into how models behave across different classes of state
    transitions."
  - p12 (A.1.3): "recent efforts have introduced benchmark sets for intrinsic multi-state (Lewis
    et al., 2025) and ligand-induced changes (Qiao et al., 2024). However, these resources
    typically focus on isolated conformational mechanisms and decompose biological assemblies
    into monomeric units. **A unified benchmark integrating multiple conformational mechanisms in
    biologically realistic assemblies remains absent.**"
- **stated_limits** (all from §3.5 Limitations, p9, unless noted):
  - Category overlap: "The biological contexts of conformational change often overlap, and some
    entries do not fit cleanly into a single category under our current annotation scheme. This
    is particularly challenging for multimeric assemblies with bound ligands, where
    protein-induced and ligand-induced effects can be coupled." Multimeric-with-ligand systems
    are deferred to future work.
  - The TM-score < 0.8 cutoff is "stringent and preferentially captures large conformational
    changes", excluding "GPCR TM6 displacement or transporter pocket rearrangements"; retained
    "due to computational and curation resource constraints".
  - Existence-based scoring only, p5: "Because our evaluation is existence-based, it is designed
    to test whether a model can recover each experimentally observed conformational state at
    least once, rather than whether it reproduces the full conformational ensemble or relative
    state populations. This distinction is important because estimating the true Boltzmann
    distribution of protein conformations remains beyond the scope of this benchmark."
  - Arbitrary apo/holo labelling in the intrinsic set (p2) and the consequence that "directional
    bias such as *holo collapse* cannot be meaningfully defined" there (p8).
  - Chai-1 is excluded from the entire conformational-bias analysis: "Chai-1 handles MSA
    differently from other models and does not provide pair representations. It was therefore run
    without MSA input and excluded from the conformational bias analysis" (p3).
  - Saturation makes the holo-conditioned ligand-induced correlations "noisy" (p7, quoted under
    `metric_saturation`).
  - Chain-level training statistics can mis-measure domain-level memorization, demonstrated on
    one outlier (p7).
- **stance**: **`precedent` + `threat` — PROVISIONAL, the user's call.**
  - *precedent (on findings)*: it is the first corpus paper to separate ligand-induced from
    protein-induced conformational change as distinct evaluation arms and to report per-mechanism
    numbers, and those numbers say the two mechanisms fail differently (asymmetric Apo→Holo
    collapse for ligands; symmetric both-state failure for partners). That is direct external
    support for treating partner-induced and ligand-induced effects as different problems.
  - *threat (on priority)*: the same taxonomy, with the same three names, is published here with
    a dataset, an evaluation scheme and a code release — so any claim to have first distinguished
    partner-induced from ligand-induced conformational change must now be positioned against it.
  - *(A third, weaker reading worth flagging for the user, not asserted as a stance: `contrast`
    on construction — the TM < 0.8 rule removes GPCRs and every other globally-similar state pair
    by construction (p9), success is a global TM predicate only, and there is no anti-memorization
    arm, so the benchmark cannot see the receptor-activation regime at all.)*

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Cluster-level success, intrinsic — AF3 | 0.18 | fraction of 72 clusters | ≥1 state-level success (TM > 0.8, nearest) for *every* known state, among 100 samples | p6 Fig 2A |
  | Cluster-level success, intrinsic — Boltz-1 | 0.08 | fraction of 72 | same | p6 Fig 2A |
  | Cluster-level success, intrinsic — Boltz-2 | 0.18 | fraction of 72 | same | p6 Fig 2A |
  | Cluster-level success, intrinsic — Chai-1 | 0.24 | fraction of 72 | same | p6 Fig 2A |
  | Cluster-level success, intrinsic — BioEmu | 0.29 | fraction of 71 | same | p6 Fig 2A/2B |
  | Cluster-level success, ligand-induced — AF3 / Boltz-1 / Boltz-2 / Chai-1 | 0.50 / 0.35 / 0.42 / 0.40 | fraction of 87 clusters | pair-level success = apo success ∧ holo success | p6 Fig 2A, p17 Fig S5C |
  | Cluster-level success, protein-induced — AF3 / Boltz-1 / Boltz-2 / Chai-1 | 0.27 / 0.19 / 0.34 / 0.17 | fraction of 75 clusters | same | p6 Fig 2A, p17 Fig S5C |
  | Headline summary of intrinsic performance | "∼20% cluster-level success" | % of clusters | all models pooled | p1, p9 |
  | Intrinsic failure decomposition (one-state collapse / complete failure), AF3 → BioEmu | 66%,27% / 64%,33% / 59%,34% / 55%,40% / 64%,28% | % of failed clusters | failed clusters N = 59/72, 66/72, 59/72, 55/72, 50/71 | p6 Fig 2B |
  | Apo-task failure rate, ligand-induced (AF3/B1/B2/Chai) | 47% / 82% / 66% / 67% | % of 350 pairs | apo-conditioned prediction fails apo success | p17 Fig S5A |
  | Apo-task failure rate, protein-induced | 43% / 48% / 48% / 47% | % of 118 pairs | same | p17 Fig S5A |
  | Directional Apo→Holo share of apo failures, ligand | 96% / 80% / 98% / 98% | % of failures | TM_holo ≥ 0.8 and TM_holo > TM_apo | p7, p17 Fig S5A |
  | Directional Apo→Holo share of apo failures, protein | 61% / 44% / 53% / 47% | % of failures | same | p17 Fig S5A |
  | Holo-task failure rate, ligand-induced | 5% / 17% / 5% / 4% | % of 350 pairs | holo-conditioned prediction fails holo success | p17 Fig S5B |
  | Holo-task failure rate, protein-induced | 42% / 50% / 34% / 57% | % of 118 pairs | same | p17 Fig S5B |
  | Hit rate within successful intrinsic clusters (mean fraction) | AF3 0.818, Boltz-1 0.840, Boltz-2 0.617, Chai-1 0.804, BioEmu 0.767 | fraction of 100 samples | TM ≥ 0.8 to ≥1 ground-truth state, over clusters with ≥1 state recovered | p15 Table S1 |
  | …its SD / #clusters | 0.320/19, 0.302/13, 0.371/16, 0.290/19, 0.234/24 | — / clusters | across clusters | p15 Table S1 |
  | Fraction of entries spanning both states | "below ∼30% across all DynDisto_holo bins" for AF3/Boltz-1/Boltz-2; BioEmu peaks ≈48% and ≈59% | % of entries | ≥1 sample with Struct_holo < −0.5 and ≥1 with > +0.5 | p8 Fig 3C |
  | σ(Struct_holo) within distogram, BioEmu vs others | p = 1.3e-08 (vs AF3), 1.4e-12, 4.2e-13; text reports p < 1e-4 for all | paired Wilcoxon p | BioEmu vs AF3 / Boltz-1 / Boltz-2 | p8 Fig 3B |
  | Struct_holo − DynDisto_holo positive shift, ligand-induced | AF3 57.0%, Boltz-1 71.7%, Boltz-2 86.0% of points above y = x | % of points | one-sided paired t-test / Wilcoxon: AF3 p = 3.24e-2 / 1.32e-3; Boltz-1 p = 1.28e-24 / 1.87e-33; Boltz-2 p = 7.30e-74 / 1.08e-80 | p18 Fig S6 |
  | Struct_holo vs DynDisto_holo Pearson r, ligand-induced | AF3 0.93, Boltz-1 0.90, Boltz-2 0.50 | Pearson r | per-model scatter | p18 Fig S6 |
  | Correlation of (Struct_holo − DynDisto_holo) with Train_holo, \|MSA_holo\| < 0.3 | intrinsic: 0.211/0.160/0.312 (Pearson, AF3/B1/B2); ligand apo-cond: 0.209/0.190/0.237; ligand holo-cond: 0.117/−0.057/−0.100; protein apo-cond: 0.269/0.291/0.356; protein holo-cond: 0.354/0.350/0.329 | Pearson r | Train_holo | p20 Fig S8 |
  | Correlation of (Struct_holo − DynDisto_holo) with MSA_holo, \|Train_holo\| < 0.3 | intrinsic: −0.185/−0.103/−0.141; ligand apo-cond: −0.201/0.059/−0.028; ligand holo-cond: −0.154/−0.137/−0.205; protein apo-cond: −0.155/0.031/0.022; protein holo-cond: −0.319/0.137/0.112 | Pearson r | MSA_holo | p21 Fig S9 |
  | Complex-accuracy coupling, AF3, protein-induced | Pearson r = −0.425, Spearman ρ = −0.426, p ≈ 0 | correlation | monomer Cα-RMSD vs DockQ | p16 Fig S3 |
  | Complex-accuracy coupling, AF3, ligand-induced | Pearson r = 0.342, Spearman ρ = 0.435, p ≈ 0 | correlation | monomer Cα-RMSD vs ligand RMSD | p16 Fig S3 |
  | Complex success vs monomer error, protein-induced | 70.5% (<1 Å) → 32.1% (>10 Å) | % success (DockQ ≥ 0.23) | binned by monomer Cα-RMSD | p16 Fig S3 |
  | Complex success vs monomer error, ligand-induced | 80.4% (<1 Å) → 10.7% (>10 Å) | % success (ligand RMSD ≤ 2 Å) | binned by monomer Cα-RMSD | p16 Fig S3 |
  | Confidence Top-10 vs Random Top-10 cluster-avg success | e.g. AF3 0.15 vs 0.17 (intrinsic), 0.49 vs 0.48 (ligand), 0.23 vs — (protein); BioEmu 0.18 vs 0.18 (intrinsic) | success rate | matched-budget confidence ranking vs uniform random | p15 Fig S2 |
  | Domain-level training skew, outlier cluster 6crf/7xhq | Train^domain_holo = −0.1148 | dimensionless (−1…1) | domain-restricted Foldseek/MMseqs2 search (N-SH2, PTP) | p7 |

  *Figure-read caveat*: values attributed to Figures 2A, 2B, S2 and S5 are in-figure annotations
  read from 150-dpi renders of pages 6, 15 and 17, not from prose. The S5C "both fail" entries
  marked ~ are inferred by subtraction from the labelled segments.
- **n_predictions**: recorded at all three levels, per the field's instruction.
  - *Samples per entry*: **100** — p2 §2.2: "Each structure was predicted with 10 independent
    random seeds, generating 10 samples per seed, yielding 100 structural predictions per entry."
    BioEmu differs in how it gets there: "BioEmu, which uses a single seed with 100 samples"
    (Figure 3B caption, p8).
  - *Targets*: **786 entries** across 234 sequence clusters, forming 577 pairs (Table 1, p2).
    Per category, entries = 162 / 435 / 189.
  - *Totals*: **NOT REPORTED as a number by the paper.** Extractor arithmetic, flagged as such:
    786 entries × 100 = 78,600 predictions per model for AF3, Boltz-1, Boltz-2 and Chai-1;
    BioEmu ran the intrinsic set only, 162 entries × 100 = 16,200 (Figure 2B implies 71 of 72
    clusters, so the true BioEmu entry count may be slightly below 162). Grand total ≈ 330,600
    predicted structures. Do not quote this as the paper's own figure.
- **comparable_to_ours**: *(left empty by the extractor, per schema v3)*
- **si_in_scope**: **SI HELD.** Appendix A (p12–21) is inside the PDF and contains the related
  work, the full curation protocol, Algorithms 1–2, Table S1 and Figures S1–S9. Two gaps
  nonetheless: (i) several per-model numbers exist only as annotations inside figure images and
  had to be read from renders — there is no numeric table for Figure 2A, Figure S2 or Figure S5;
  (ii) no per-target result list is given anywhere in the PDF; that presumably lives in the
  GitHub release (https://github.com/seoklab/promise-bench, p5), which is not held.

## F. Figures

22 panel-group rows. License for every one: **CC-BY 4.0 International**, declared in the banner
on **every page p1–p21** ("It is made available under a CC-BY 4.0 International license") —
**no ND clause; redrawing and modification are permitted with attribution.**

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 3 | Curation pipeline: RCSB → 95% seq clusters → pairwise TM → agglomerative conformational clusters → pairs with TM < 0.8 → three mechanism categories | schematic | `SCHEMATIC \| dataset curation flow from PDB to three mechanism categories, with cluster counts 72/87/75 \| no data` | 1 panel, left-to-right flow with a 3×3 TM matrix cartoon | The TM matrix shown is illustrative, not real data; no counts for how many pairs survive each filter step (1,333,459 → 577 is given only in text) | CC-BY 4.0, p3 banner |
| 2A | 6 | Cluster-level success rate for 5 models across the 3 mechanism categories | bar | `PLOT \| facet: none (1) \| vary: model (5: AF3, Boltz-1, Boltz-2, Chai-1, BioEmu) \| series: dataset category (3: intrinsic N=72, ligand-induced N=87, protein-induced N=75) \| measure: cluster-level success rate (fraction) \| n: 72/87/75 clusters per bar; 13 bars in the panel (BioEmu has only the intrinsic bar)` | 1 panel, 13 bars | Bars with no error bars, no CI and no per-cluster distribution behind them; BioEmu's two absent bars are not marked "not run" and read as zero; the y-axis is 0–1 while all values sit below 0.51 | CC-BY 4.0, p6 banner |
| 2B | 6 | Failure-mode decomposition of intrinsic-set failures | bar (stacked, 100%) | `PLOT \| facet: none (1) \| vary: model (5) \| series: failure mode (3: complete failure, one-state collapse, partial collapse) \| measure: proportion of failed clusters \| n: failed clusters per bar = 59, 66, 59, 55, 50 (of 72, 72, 72, 72, 71)` | 1 panel, 5 stacked bars | Denominator differs per bar (only failed clusters), so bar heights are not comparable to 2A; BioEmu's 71-cluster denominator is unexplained | CC-BY 4.0, p6 banner |
| 2C | 6 | Struct_holo distributions, apo- vs holo-conditioned, in the two induced sets | box | `PLOT \| facet: dataset category (2: ligand-induced, protein-induced) \| vary: model (4: AF3, Boltz-1, Boltz-2, Chai-1) \| series: input condition (2: apo-conditioned, holo-conditioned) \| measure: Struct_holo (dimensionless, −1…1) \| n: 350 pairs per ligand box, 118 per protein box; 8 boxes per panel` | 2 panels × 4 model positions × 2 boxes | n not printed on the figure; the intrinsic set is absent from this panel with no placeholder (its labels are arbitrary, explained only in text) | CC-BY 4.0, p6 banner |
| 2D | 6 | Two hand-picked structural examples of conformational collapse | structure render | `RENDER \| facet: example (2: intrinsic 6YED/6YEB with Boltz-2; ligand-induced 3C6Q/2H3H with AF3) × view pair (2: reference overlay, prediction overlay) \| views: 1 \| overlay: 1 of 100 predictions on 2 references \| axis: none` | 4 renders in 2 groups of 2 | **The displayed prediction is chosen against the answer**: "the prediction closest to state 1 was selected" / "the prediction closest to the apo state was selected" — a best-of-100 render standing in for a distribution | CC-BY 4.0, p6 banner |
| 3A | 8 | Distogram-stage vs structure-stage state preference, coloured by training exposure | scatter | `PLOT \| facet: model × set (4: AF3 ligand apo-cond, Boltz-2 ligand apo-cond, AF3 intrinsic, Boltz-2 intrinsic) \| vary: DynDisto_holo, −1…1 (continuous) \| series: Train_holo (continuous colour, −1…1) + point size = number of structure-based search hits \| measure: Struct_holo (−1…1) \| n: 1 per mark; per panel NOT REPORTED (≤350 ligand pairs / ≤109 intrinsic pairs)` | 4 panels, y = x dashed reference, one cluster ringed as an outlier | Per-panel n never given; two aesthetics (colour and size) encode two further variables with the size legend absent | CC-BY 4.0, p8 banner |
| 3B | 8 | Within-distogram spread of Struct_holo, BioEmu vs the three others | box (with overlaid strip) | `PLOT \| facet: none (1) \| vary: model (4: AF3, Boltz-1, Boltz-2, BioEmu) \| series: none (1) \| measure: σ(Struct_holo) within one distogram \| n: 1 dot = 1 distogram (~10 seeds per target for AF3/Boltz; for BioEmu 1 dot per target from 50 subsampled trials of 10 of 100); per panel NOT REPORTED` | 1 panel, 4 model columns with significance brackets | The BioEmu dot is constructed differently from the others (subsampled and averaged over 50 trials vs raw per-seed SD), so the compared quantities are not identically defined — stated in the caption, invisible in the plot | CC-BY 4.0, p8 banner |
| 3C | 8 | Fraction of entries whose samples span both states, by distogram-preference bin | line | `PLOT \| facet: none (1) \| vary: DynDisto_holo bin (7: [-1.0,-0.7] … [0.7,1.0]) \| series: model (4: AF3, Boltz-1, Boltz-2, BioEmu) \| measure: % of entries with ≥1 sample Struct_holo < −0.5 and ≥1 > +0.5 \| n: per-bin entry counts NOT REPORTED` | 1 panel, 4 lines over 7 bins | No per-bin n, so the BioEmu peaks at the extreme bins rest on unknown denominators; the extreme bins fall to 0 for all models with no indication whether that is emptiness or failure | CC-BY 4.0, p8 banner |
| S1 | 14 | GO functional-group composition of each dataset category | donut / pie (see `unresolved` — not in the v3 `plot_type` list) | `PLOT \| facet: dataset category (3: intrinsic 72 clusters, ligand-induced 87, protein-induced 75) \| vary: GO functional group (9 / 7 / 7 wedges) \| series: none (1) \| measure: % of clusters \| n: 72 / 87 / 75 clusters per panel; per-wedge count not printed (percentages only)` | 3 donuts | Percentages only, no counts, so a 3.81% wedge could be 3 clusters; the "Other" wedge is the largest or second largest in all three panels (20.3%, 19%, 31.4%), which undercuts the caption's breadth claim | CC-BY 4.0, p14 banner |
| S2 | 15 | Confidence-ranked vs uniform-random selection at matched budget | bar | `PLOT \| facet: none (1) \| vary: model (5) \| series: selection scheme × category (12: {Conf, Rand} × {Top-10, Top-50} × {intrinsic N=72, ligand N=87, protein N=75}) \| measure: cluster-avg success rate \| n: 72/87/75 clusters per bar; random arms averaged over n = 50 draws` | 1 panel, up to 12 bars per model | 12 series in one panel with no faceting makes the confidence-vs-random comparison hard to read pairwise; no error bars on the random arms despite n = 50 draws being available | CC-BY 4.0, p15 banner |
| S3A | 16 | Complex-structure prediction success in the induced sets | bar | `PLOT \| facet: none (1) \| vary: model (4) \| series: dataset category (2: protein-induced DockQ ≥ 0.23, ligand-induced ligand RMSD ≤ 2 Å) \| measure: complex success rate \| n: 118 / 350 pairs per bar` | 1 panel | Two different success criteria (DockQ and ligand RMSD) plotted on one axis as if commensurable | CC-BY 4.0, p16 banner |
| S3B | 16 | Monomer conformational error vs complex accuracy, AF3 | scatter | `PLOT \| facet: dataset category (2: protein-induced, ligand-induced) \| vary: monomer Cα-RMSD (Å, continuous) \| series: none (1) \| measure: DockQ (left) / ligand RMSD Å (right) \| n: 1 per mark; per panel NOT REPORTED` | 2 panels with shaded success regions | Two different measures share a row; per-panel n not given | CC-BY 4.0, p16 banner |
| S3C | 16 | Complex success rate binned by monomer error | bar | `PLOT \| facet: dataset category (2) \| vary: monomer Cα-RMSD bin (<1 Å … >10 Å) \| series: none (1) \| measure: complex success rate \| n: per-bin NOT REPORTED` | 2 panels | Per-bin n absent, so the <1 Å and >10 Å extremes could rest on very few pairs | CC-BY 4.0, p16 banner |
| S4 | 16 | Distogram vs structure holo-preference, both conditionings, both induced sets | box | `PLOT \| facet: dataset category (2: ligand-induced, protein-induced) × model (3: AF3, Boltz-1, Boltz-2) \| vary: pipeline stage (2: DynDisto_holo, Struct_holo) \| series: input condition (2: apo-conditioned, holo-conditioned) \| measure: holo preference score (−1…1) \| n: 350 / 118 pairs per box` | 2 panels × 3 model blocks × 2 stages × 2 conditions = 24 boxes | Chai-1 and BioEmu absent (no pair representations / not run) without an in-figure note; n not printed | CC-BY 4.0, p16 banner |
| S5A-B | 17 | Failure decomposition into directional collapse vs both-low-TM, for the apo task (A) and holo task (B) | bar (stacked, 100%) | `PLOT \| facet: task (2: apo-conditioned failures, holo-conditioned failures) \| vary: model (4) × dataset category (2: ligand-induced, protein-induced) \| series: failure mode (2: directional collapse, both low TM) \| measure: mean failure ratio (proportion of failed entries) \| n: failed entries annotated per bar, e.g. 165/350 and 51/118` | 2 panels, 8 stacked bars each | Denominator is failed entries only and varies enormously across bars (15 to 287), so segment percentages compare unlike samples; annotated as counts above the bars, which mitigates it | CC-BY 4.0, p17 banner |
| S5C | 17 | Cluster-level outcome breakdown summing to 100% | bar (stacked, 100%) | `PLOT \| facet: none (1) \| vary: model (4) × dataset category (2) \| series: outcome (4: success, APO-only fail, HOLO-only fail, both fail) \| measure: cluster-avg proportion \| n: 87 (lig) / 75 (pro) clusters per bar` | 1 panel, 8 stacked bars | Smallest segments are unlabelled, so "both fail" must be recovered by subtraction | CC-BY 4.0, p17 banner |
| S6A | 18 | Struct_holo vs DynDisto_holo with y = x, ligand-induced | scatter | `PLOT \| facet: model (3: AF3, Boltz-1, Boltz-2) \| vary: DynDisto_holo (−1…1, continuous) \| series: none (1) \| measure: Struct_holo (−1…1) \| n: 1 per mark; ≤350 per panel` | 3 panels with r and p annotated | Per-panel n not printed | CC-BY 4.0, p18 banner |
| S6B | 18 | Mean paired holo shift binned by distogram-preference magnitude | point (with 95% CI error bars) | `PLOT \| facet: model (3) \| vary: \|DynDisto_holo\| bin (continuous binned) \| series: none (1) \| measure: mean(Struct_holo − DynDisto_holo) with 95% CI \| n: per-bin sample sizes annotated on the figure` | 3 panels | *(none — per-bin n is annotated and CIs are shown)* | CC-BY 4.0, p18 banner |
| S7A | 19 | Structures of the outlier cluster with domains annotated (6crf, 7xhq) | structure render | `RENDER \| facet: state (2: 6crf, 7xhq) \| views: 1 \| overlay: NOT REPORTED predictions on 2 references \| axis: none` | 1 panel group | Whether any prediction is shown at all is not stated in the caption | CC-BY 4.0, p19 banner |
| S7B | 19 | Foldseek hit counts for two-domain query permutations | bar | `PLOT \| facet: none (1) \| vary: two-domain permutation query (n NOT REPORTED) \| series: state (2: apo-like, holo-like) \| measure: number of structure-based search hits \| n: 1 cluster (6crf/7xhq) behind the whole panel` | 1 panel | The entire memorization-resolution argument rests on one cluster; the panel does not show that n = 1 | CC-BY 4.0, p19 banner |
| S8 | 20 | Full grid of DynDisto vs Struct coloured by Train_holo, MSA held neutral | scatter (grid of small multiples) | `PLOT \| facet: dataset arm (5: intrinsic, ligand apo-cond, ligand holo-cond, protein apo-cond, protein holo-cond) × model (3) \| vary: DynDisto_holo (−1…1, continuous) \| series: Train_holo (continuous colour) + point size = number of searched training entries \| measure: Struct_holo (−1…1) \| n: 1 per mark; per panel NOT REPORTED (restricted to \|MSA_holo\| < 0.3)` | 15 panels (5 rows × 3 columns) | The neutrality restriction \|MSA_holo\| < 0.3 removes an unreported fraction of the data from every panel; no panel states how many points survive it | CC-BY 4.0, p20 banner |
| S9 | 21 | The same grid coloured by MSA_holo, training exposure held neutral | scatter (grid of small multiples) | `PLOT \| facet: dataset arm (5) × model (3) \| vary: DynDisto_holo (−1…1, continuous) \| series: MSA_holo (continuous colour) + point size = number of searched training entries \| measure: Struct_holo (−1…1) \| n: 1 per mark; per panel NOT REPORTED (restricted to \|Train_holo\| < 0.3)` | 15 panels (5 rows × 3 columns) | As S8: the \|Train_holo\| < 0.3 restriction silently changes n per panel; correlations near zero are reported without n | CC-BY 4.0, p21 banner |

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), session of 2026-09-08
- **schema_version**: v3
- **confidence**: **high** on the taxonomy, the inclusion criteria, the GPCR question, the metric
  definitions and every quoted claim — all of those are in prose and unambiguous. **Medium** on
  the per-model numeric values that exist only as annotations inside figure images (Figures 2A,
  2B, S2, S5): pages 6, 8, 14 and 17 were rendered at 150 dpi and read, and small-print
  percentages, especially the unlabelled "both fail" segments in Figure S5C, carry a real risk of
  misreading; Figure S2's bar values are dense and were transcribed only in part. **Low** on
  nothing. The mathematical notation in §2.4 (Eqs. 1–10) extracted cleanly enough to reproduce
  definitions, but subscripts in the flowed text are lossy, so equations were read against the
  layout output rather than retyped from a render.
- **unresolved**:
  1. **Preprint or proceedings?** p1 carries both the bioRxiv "not certified by peer review"
     banner and a PMLR/ICML 2026 proceedings footer. Tagged `preprint` only. If the ICML
     acceptance is real, this note's publication tag needs revisiting.
  2. **BioEmu's 71 vs 72 intrinsic clusters.** Figure 2B annotates "N=50/71" for BioEmu while
     every other model shows /72. The text never mentions a dropped cluster.
  3. **Templates**: the paper never states whether any predictor's structural-template channel
     was enabled. This matters for a memorization argument and is simply absent.
  4. **Whether any GPCR survives in the released dataset.** The paper reports none and explains
     why none would (p9), and the GO panels show no receptor wedge, but no per-target list is in
     the PDF; only the GitHub release could settle it definitively.
  5. **Tag I needed and could not use**: none, strictly — but see the plot-type gap below, and
     note that no tag in the v3 vocabulary expresses "benchmark stratified by conformational-change
     mechanism", which is this paper's single distinguishing feature. `ligand-driven` and
     `partner-driven` are both applied, which is the closest the vocabulary gets, but they read
     as *control handles the method uses* rather than *categories the benchmark separates*. I did
     not invent a tag.
  6. **Schema gap — `plot_type` and `mark` have no pie/donut.** Figure S1 is three donut charts.
     `plot_type`'s enumeration (violin / box / scatter / line / bar / heatmap / structure render /
     grid of small multiples / schematic) and PLOT's `mark` (bar|violin|box|point|line) both lack
     a wedge/part-of-whole form. I wrote `donut / pie` in `plot_type` and left `mark` out of the
     `data_shape` string for that row rather than mislabelling it a bar; that makes the S1 row
     partially unjoinable. Recorded rather than fudged.
  7. **Schema gap — the panel-splitting rule is silent on `vary`.** v3 says "Split when `mark` or
     `measure` differs. Do not split when only `facet` differs." Figures S3A and S3C share both
     `mark` (bar) and `measure` (complex success rate) but differ in `vary` (model vs Cα-RMSD
     bin), which is neither of the two named cases. I split them, on the grounds that merging
     produces exactly the compound `vary` string the grammar exists to prevent — but the rule as
     written arguably says merge. The rule needs a third clause covering `vary`.
  8. **Schema ambiguity — `series` when the colour dimension is continuous.** Figures 3A, S8 and
     S9 encode a continuous variable in colour *and* a second continuous variable in point size.
     `series: <var> (<n>)` presupposes discrete levels. I wrote `series: Train_holo (continuous
     colour) + point size = …`, which is a two-aesthetic compound and will not join cleanly. A
     `size:` slot, or an explicit continuous form for `series`, would fix it.
  9. **Schema ambiguity — where a saturating *binary* metric goes.** v3 says `metric_saturation`
     is numeric only. A TM > 0.8 pass/fail predicate saturates *categorically* (holo-conditioned
     ligand failures are already at 4–5%, so no model can distinguish itself downward), which is
     neither the numeric ceiling the field describes nor a figure defect for `hides`. I recorded
     it in `metric_saturation` alongside the authors' own saturation statement, flagged as a
     floor effect on a binary rate.
  10. **`states_generated` for a benchmark paper.** The benchmark generates nothing; the models
      it evaluates do. I recorded the models' behaviour (`ensemble + single-state`), which is
      what the paper measures, but the field's wording ("What did they actually produce")
      assumes a method paper. A `NOT APPLICABLE — benchmark, states generated by evaluated
      models` convention would be cleaner for the four benchmark-only papers in this corpus.
- **why_it_matters**: *(left empty by the extractor — the user's call)*

## Tags

`general-protein` `benchmark-only` `multi-backbone` `md-emulator` `ensemble` `single-state`
`binary-predicate` `continuous-metric` `rmsd-only` `saturating-metric` `design-level-oracle`
`no-anti-memorization` `unpowered` `confidence-as-discriminator` `ligand-driven`
`partner-driven` `apo-sampling` `orthosteric` `preprint` `precedent` `threat`
`negative-result` `comparator-numbers`

Tag notes, so the reverse lookups stay honest:

- **`general-protein`** and NOT `gpcr`, `kinase`, `transporter` or `fold-switching`: the dataset
  is family-agnostic and, per p9, its TM < 0.8 rule excludes GPCR and transporter-pocket motions
  by construction. Fold-switching is cited as motivation (p1, p12) but no fold-switching subset
  exists in ProMiSE.
- **`md-emulator`** applies to BioEmu, one of the five evaluated backbones (p7 §3.4: fine-tunes
  the structure decoder on MD trajectory data), not to the benchmark itself.
- **`ensemble` + `single-state`**: 100 samples per entry, collapsing onto one basin — the exact
  pair the schema describes.
- **`rmsd-only`** alongside `binary-predicate` / `continuous-metric`: every state call in the
  paper reduces to global TM-score or Cα-RMSD against a deposited reference. There is no
  site-level, feature-level or geometric predicate anywhere.
- **`design-level-oracle`** and NOT `oracle-leak`: nothing leaks into the predictors' inputs
  (route 1 NONE FOUND), but systems are selected because both states are deposited and the
  expected state is declared before the prediction is read (routes 3, 5, 6, 7).
- **`unpowered`** attaches specifically to the domain-vs-chain memorization case study, n = 1
  cluster (p7). The main correlational analyses are adequately powered.
- **`ligand-driven`** + **`partner-driven`**: both, because the benchmark's whole point is that
  these are separate arms with separate results.
- **`orthosteric`**: the ligand-induced arm is defined by small molecules bound to the target
  chain with ligands beyond 5 Å discarded (p12); no allosteric-site or cryptic-pocket analysis
  is performed, so neither of those tags applies, and `allosteric-failure` is not claimed.
- **`negative-result`**: the paper's headline findings are failures — ~20% intrinsic cluster
  success, holo collapse under apo conditioning, and confidence scores no better than random.
- **NOT tagged**: `peer-reviewed` (see `unresolved` 1), `prospective`, `anti-memorization`,
  `experimental-validation`, `msa-subsample`, `msa-state-filter`, `template-state-bias`,
  `templates-on`, `no-template-no-msa` (template state never stated — see `templates`),
  `state-annotated-input`, `latent-steering`, `af-cluster`, `md`, `enhanced-sampling`,
  `cofolding` (AF3/Boltz/Chai are co-folding models, but this paper is `benchmark-only` and
  proposes no co-folding method), `directed-state`, `seed-only`, `figure-exemplar`.
