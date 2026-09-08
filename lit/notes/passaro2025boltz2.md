# passaro2025boltz2

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.
`comparable_to_ours` and `why_it_matters` deliberately left EMPTY per v3.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–55) and coincide with the
printed page numbers.** Layout: p1 title/abstract, p1–2 §1 Introduction (+ Fig 1 p2), p3–4 §2 Data
(+ Fig 2 architecture p4, Table 1 affinity training data p4), p4–5 §3 Architecture, p5–6 §4
Training, p6–11 §5 Evaluation (Fig 3 p7, Fig 4 + Fig 5 p8, Fig 6 p9, Fig 7 p10, Fig 8 p11),
p11–12 §6 Limitations, p12 §7 Conclusion, p13 Acknowledgements, p14–15 SI contents,
p16–22 App. A Data (A.1 structural p16–19, A.2 affinity p19–22), p23–27 App. B Model
(B.3 controllability/steering p24–25, B.4 confidence p25, B.5 affinity module p25–27),
p28–34 App. C Training (C.1.4 hyperparameters p29, C.2 affinity training p30–33,
C.3 SynFlowNet p33–34 + Fig 9 p34), p35–39 App. D Benchmarks and Baselines,
p40–50 App. E Extended Results (Tables 9–10 p40, Fig 11 p41, Tables 11–13 p42,
Tables 14–16 p43, Fig 12 p44, Figs 13–14 p45, Table 17 + Fig 15 p46, Fig 16 p47,
Figs 17–19 p48, Figs 20–21 p49, Figs 22–23 p50), p51–55 references.

**DOCUMENT TYPE.** Primary technical report describing a released foundation model
(weights, inference and training code released, p1 footnote 1, GitHub jwohlwend/boltz).
Self-declared as incomplete: p40 — "Note that this paper is still a preprint in preparation.
In the coming weeks, we will integrate even more results to the paper including evaluations of
the template, contact and pocket conditioning as well as more challenging prospective evaluations
of our small-molecule design pipelines." Also p40 — "Due to the scale of Boltz-2, comprehensive
ablation studies isolating the impact of each architectural or training component on final
performance are not computationally feasible." **Both facts bound what this note can say: the
controllability features (template / contact / pocket steering) are described in full but are
NOT evaluated anywhere in this version.**

**Scope discipline note.** The corpus holds other papers that benchmark against or dispute Boltz-2.
This note records only what THIS paper claims. Where this paper's own FEP-comparison claims appear
below, they are recorded verbatim as claims, with the n and benchmark identity attached, and no
external dispute is imported.

---

## A. Identity

- **citekey**: `passaro2025boltz2`
- **doi**: **bioRxiv 10.1101/2025.06.14.659707**, version posted **June 18, 2025** (page header,
  every page p1–55).
- **year**: **2025**
- **venue**: **bioRxiv preprint. Explicitly not peer reviewed** — page header, p1: "this version
  posted June 18, 2025 … (which was not certified by peer review)". Tagged `preprint`.
- **title**: Boltz-2: Towards Accurate and Efficient Binding Affinity Prediction — p1
- **authors**: Saro Passaro\*, Gabriele Corso\*, Jeremy Wohlwend\*, Mateo Reveiz\*, Stephan Thaler\*,
  Vignesh Ram Somnath, Noah Getz, Tally Portnoi, Julien Roy, Hannes Stark, David Kwabi-Addo,
  Dominique Beaini, Tommi Jaakkola, Regina Barzilay (\* = core contributors). Affiliations p1:
  MIT CSAIL, MIT Jameel Clinic, Valence Labs, Recursion, ETH Zurich.

---

## B. Scope

- **system**: **general protein** (and beyond protein: DNA, RNA, ligands, MHC-peptide, TCR-pMHC,
  antibody–antigen). Evaluation reaches into **protein kinases** specifically for affinity
  (FEP+ 4-target subset = CDK2, TYK2, JNK1, P38, p36; TYK2 prospective screen, p10–11;
  validation assays include ABL1/P00519, Q9Y5S2, O96013, p44) and into **GPCRs** as validation
  assay targets (P21453, P51686, P41146, P43115, Fig 12 p44) — but no conformational-state work
  on either family. p1 self-description: "a new structural biology foundation model".
- **n_targets**:
  - Structure benchmark: **2315 unique targets** from PDB 01/01/24–12/31/2024 (p35).
  - MD benchmark: **40 complexes per dataset** for mdCATH and ATLAS test sets (p19).
  - Antibody benchmark: n **NOT REPORTED** (Fig 4 left, p8 — no n in caption or text).
  - Polaris-ASAP: n **NOT REPORTED** (top-10 competition entries shown, p8).
  - Affinity: OpenFE subset **876 protein–ligand complexes** (p36); focused subset **4 targets /
    87 neutral compounds** (p36); CASP16 **140 protein–ligand pairs across two targets** (p9);
    MF-PCBA **10 HTS assays**, each downsampled to 50,000 complexes (p36); private Recursion
    **8 blinded hit-to-lead assays** (p10, p43); hit-to-lead validation set **16 assays** (p36).
  - Prospective screen: **1 target (TYK2)**, p10.
  - Training targets: ~**2k** protein clusters at 90% identity for ChEMBL/BindingDB affinity data,
    plus 300 (PubChem HTS), 1.3k (CeMM), 60 (MIDAS), 250 (PubChem small assays) — Table 1, p4.
- **method_class**: **co-folding** (diffusion-based all-atom structure prediction) **+ affinity
  prediction head + inference-time physics steering**. Also trained on MD trajectories and
  benchmarked against MD emulators. Not MSA-subsampling, not clustering, not enhanced sampling.
- **backbones**: **Boltz-2** (this work), compared head to head against **AlphaFold3, Chai-1,
  ProteinX, Boltz-1, Boltz-1x, Boltz-2x** on the PDB benchmark (Fig 3, p7; baselines p35: "For
  all tools, we use the same inference parameters (5 recycling rounds, 5 samples, single seed) and
  the same MSA"). MD baselines: **Boltz-1, AlphaFlow-MD base, BioEmu** (p36). Five distinct
  backbones compared → tagged `multi-backbone`.
- **templates**: **supported but OFF in every evaluation reported.** p35, PDB baselines: "We do
  not use templates during evaluation." Template conditioning and template steering are described
  (p24) but p40 states their evaluation is not yet in the paper. During *training* templates are
  used: "We produce template hits for protein chains as described in AlphaFold3, using hmmbuild
  and hmmsearch on PDB sequences deposited at least 60 days prior to any given query's deposition
  date" (p16); sampling: 60% of the time no templates, otherwise 1–4 from the top-20 hits (p28).
- **msa_handling**: **full, with randomised sampling and 5% full dropout at training time.**
  p28: "at training time, we do not select MSA sequences greedily, but we rather sample them
  randomly among the top 16k hits… we aim at improving the model performance in this setting by
  randomly dropping all of the MSA of a complex in 5% of training iterations." Max 8192 MSA
  sequences during training (Table 6, p29). MSAs computed with ColabFold search, taxonomy-paired
  via Uniref100 (p16). At inference, all baselines "were run with the same MSA and sequence
  inputs" (p36). **This is not subsampling as a state handle and not state-filtering** — it is
  training-time regularisation.

---

## C. Conformational core

- **states_generated**: **ensemble + single-state.**
  - *Ensemble* arm: with MD method conditioning the model produces diverse ensembles —
    p7: "(1) MD conditioning has a clear effect on the predicted ensembles, leading to more
    diverse structures that better capture the conformational diversity of the simulations".
    MD evaluation used **100 samples** per target against 200 reference frames (p35). Trained on
    ensembles: p3 — "Unlike Boltz-1, which trained on a single structure per system, we supervise
    Boltz-2 using ensembles coming from both experimental techniques, such as NMR, as well as
    computational ones, such as molecular dynamics."
  - *Single-state* arm and default: the reported structure is top-1 of 5 — p35: "For each result,
    we provide the top-1 prediction across 5 samples according to the confidence model ranking."
    The affinity module consumes "the top-ranked structure from five samples generated over 200
    diffusion steps each, ranked according to their protein-ligand ipTM-score" (p26).
  - **No conformational-state capability is claimed, and the opposite is stated.** p12,
    Limitations: "the model still often fails to capture large conformational changes, such as
    those that can be induced by binding." The diversity achieved is *local* fluctuation /
    RMSF-scale, and even there is bettered by the specialists — p8: "This diversity increase is,
    however, outperformed by BioEmu and AlphaFlow, which more closely align with the reference
    diversity from the simulation."
- **structural_priors_used** (design-time deposited knowledge; not a defect):
  1. **The entire PDB up to 2023-06-01** as structural training data (p16), plus B-factors
     extracted from PDB entries (p16).
  2. **AFDB / AlphaFold2 predictions** — ~5 million monomers, filtered at global lDDT ≥ 0.5
     (p18); 0.380 sampling weight, the second largest single source (Table 2, p18).
  3. **Boltz-1 self-distillation** across RNA, protein-DNA, RNA-ligand, protein-ligand, TCR-pMHC,
     MHC-I, MHC-II (p17–18).
  4. **MD trajectories** from MISATO (11,235 systems), ATLAS (1,284 proteins), mdCATH
     (5,270 systems) — p16–17. All three are seeded from deposited PDB entries: p19 — "all entries
     from the MD datasets correspond to PDB structures released before the validation cutoff date
     of 2023-06-01".
  5. **TYK2 protein-ligand complexes from the PDB were in the structure-module training data** —
     p49, stated by the authors: "The Boltz-2 structure module was trained using TYK2
     protein-ligand complexes from the PDB."
  6. **KLIFS** used post hoc only, to assess novelty of generated ligands — p49: "we collected the
     47 public TYK2 inhibitors from the KLIFS database … that correspond to the co-crystalized
     TYK2 inhibitors from the PDB." Not used to bias any prediction.
  7. **Deliberate upsampling of SARS-CoV-2 Mpro-like proteins in training** — p18: "we upsample
     interfaces containing antibodies and TCR, as these are specific modalities that we wanted the
     model to improve on, as well as proteins similar to SARS-CoV2-Mpro **as we had planned to
     participate in the Polaris-ASAP competition**" (weight 0.015, Table 2 p18). Recorded here as
     a design-time choice; its consequence for the reported Polaris-ASAP result is in
     `oracle_leakage` routes 4 and 7.

- **oracle_leakage** — seven routes, each answered separately.

  **Route 1 — deposited structures used as input or template.**
  **NONE FOUND for the reported evaluations.** p35 (protocol page): "For all tools, we use the same
  inference parameters (5 recycling rounds, 5 samples, single seed) and the same MSA. **We do not
  use templates during evaluation.**" The affinity module takes *predicted* structures, not
  deposited ones: p31 — "For each protein–ligand complex, we run Boltz-2 structure model with 5
  recycling iterations, 200 diffusion steps, and generate 5 candidate structures." One partial
  exception, in a *baseline*, not in Boltz-2: p39 — "In the absense of experimental crystal
  structures in MF-PCBA, we co-fold the median-weight active compound of each assay with Boltz-2
  to obtain the receptor structure for Docking."

  **Route 2 — state annotations from a curated database (GPCRdb / KLIFS / Kincore) driving
  templates or alignments.** **NONE FOUND.** KLIFS appears exactly once and only post hoc, p49
  (quoted under `structural_priors_used` item 6); it drives a Tanimoto novelty analysis of
  generated ligands, not any prediction. No GPCRdb, no Kincore, no state annotation anywhere.

  **Route 3 — cluster labels derived from known states.** **NONE FOUND.** All clustering in the
  paper is by *sequence identity*, never by state: p18 — "mmseqs easy-cluster … –min-seq-id 0.4"
  for structural splits; p37 — "clustering all protein sequences in the affinity datasets using
  'mmseqs easy-cluster … –min-seq-id 0.9 –cov-mode 0 -c 0.01'". Ligand clustering is by Tanimoto
  similarity (p19, p22).

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against the
  evaluation set.** **THREE FINDINGS, all admitted by the authors.**
  (a) *Calibration constants fitted on a validation set drawn from the training corpus.* p27:
  "we apply a calibrated ensembling strategy. We first compute the mean predicted affinity between
  models and then apply a molecular weight correction of the form ŷ = C0·(y1+y2) + C1·MW_binder +
  C2, where … C0, C1, and C2 are **fitted in the holdout validation set**". And that validation set
  is itself drawn from training data: p36 — "we curate a validation set by **selecting a diverse
  collection of hit-to-lead assays from our training corpus**." This is validation-set tuning, not
  test-set tuning, and the test sets are separately protected (see `anti_memorization_design`) —
  but it is a fitted post-hoc correction applied to every reported affinity number.
  (b) *Steering hyperparameters tuned; tuning set never stated.* p23: "Boltz-2 adopts the steering
  potentials we proposed in Boltz-1x **with tuned hyperparameters** and a normalization of each
  potential by the number of elements on which they are applied." What they were tuned against is
  not given anywhere in the paper.
  (c) *Training-data composition chosen with a benchmark in view.* p18: "…as well as proteins
  similar to SARS-CoV2-Mpro **as we had planned to participate in the Polaris-ASAP competition**",
  and the Polaris-ASAP result is then reported retrospectively as a headline (p7, Fig 4 right).
  No sweep or per-target tuning is involved, so this is training-set enrichment against a named
  evaluation rather than pipeline leakage; it is labelled design-level (route 7) below.
  For completeness, the paper flags the same class of problem in a *baseline*: p39 — "the results
  of the ABFE protocol [Wu et al., 2025] on the 4 target subset **may also represent an optimistic
  estimate of its prospective performance given that the protocol was optimized based this
  dataset**", and p39 on FEP+ — "The results of FEP+ are intended to show the maximum attainable
  accuracy of current (commercial) FEP simulations **by manually adjusting the protocol (input
  preparation, perturbation map, force field) to the system at hand after observing the error with
  respect to the experiment**."

  **Route 5 — success defined post hoc by RMSD/TM to a structure they held.**
  **PRESENT, and standard for a retrospective structure benchmark; absent for the prospective
  screen, where a different oracle substitutes.** Structure benchmarks score lDDT and DockQ against
  deposited references (p35, "The lDDT … DockQ which we use to score antibody interfaces"), which
  is retrospective scoring against a held reference by construction. For the prospective TYK2
  screen there is **no experimental readout at all**; success is defined by a simulation the
  authors also wrote — p10: "in the absence of experimental data, we validate the compounds
  selected by Boltz-2 with a single repeat of Boltz-ABFE, our recently developed absolute FEP
  pipeline". The authors flag the resulting circularity themselves, p11: "We note that these
  results might be optimistic given that Boltz-2 performs well on this target based on the
  protein-ligand benchmark data [Hahn et al., 2022], achieving Pearson R = 0.83."

  **Route 6 — best/worst model labels assigned against a held reference.**
  **NONE FOUND.** Ranking among samples is by the model's own confidence, never by the reference.
  p35: "For each result, we provide the top-1 prediction across 5 samples **according to the
  confidence model ranking**." p26: "the top-ranked structure from five samples … **ranked
  according to their protein-ligand ipTM-score**." p30: "We select the most confident structure
  according to the inter-chain predicted TM-score (ipTM)."

  **Route 7 — design-level oracle use (weaker than pipeline leakage; label kept distinct).**
  **PRESENT, twice, both stated openly by the authors.**
  (a) *The prospective target was chosen because the validator is known to work on it.* p10: "We
  selected TYK2 for two main reasons: First, TYK2 is in the test set of the Boltz-2 affinity model,
  avoiding data leakage from known binders. Second, in the absence of experimental data, we
  validate the compounds selected by Boltz-2 with a single repeat of Boltz-ABFE … **and Boltz-ABFE
  performs very well on this target**. Indeed, based on the protein-ligand benchmark, Boltz-ABFE
  achieves a Pearson R = 0.95, centered MAE = 0.42 kcal/mol … supporting our confidence of this
  procedure as a validation step for TYK2-targeting virtual screens." The first reason is a
  genuine anti-leakage measure; the second is target selection conditioned on the oracle's known
  performance.
  (b) *Training data enriched for a benchmark family before entering that benchmark* — the
  SARS-CoV-2 Mpro upsampling quoted at route 4(c), p18, with the Polaris-ASAP result reported at
  p7 and Fig 4 right, p8.

  **Summary line:** pipeline routes 1, 2, 3 and 6 are clean and the protocol pages that establish
  that are p35–p37; the real findings are route 4 (a fitted molecular-weight calibration on a
  validation set carved out of the training corpus, and untraceable steering-hyperparameter
  tuning) and route 7 (target and training composition chosen with the answer's difficulty
  already known). Route 5 is retrospective-by-design for structures and is replaced by a
  self-authored simulation oracle for the one prospective experiment.

- **prospective**: **partial.**
  - *Prospective:* the TYK2 virtual screen (460,160 HLL + 64,960 Kinase library + 117,199
    SynFlowNet-generated compounds scored, p11, p46 Table 17) selects compounds with no known
    answer, and CASP16 is a genuine blind challenge run out of the box — p9: "we ran Boltz-2
    out-of-the-box with no fine-tuning or input curation", and p37: "CASP16 data was released
    after our training data cutoff". The 8 Recursion assays are described as "blinded" (p10, p43).
  - *Retrospective:* everything else. The PDB, antibody, MD, FEP+, OpenFE, MF-PCBA benchmarks are
    all retrospective; Polaris-ASAP is explicitly "Retrospective results for the Polaris-ASAP
    competition" (Fig 4 caption, p8).
  - *Why not fully prospective:* the one prospective arm has no experimental readout (route 5) and
    its target was chosen for oracle convenience (route 7a).
- **state_metric**: **continuous coordinate + binary predicate.** Dual, and both halves are used
  for headline claims.
  - Continuous: lDDT per modality and per interface (p35); Pearson r / Spearman ρ / RMSE on RMSF
    (p35); Pearson R, Kendall τ, PMAE, MAE for affinity (p37); AP, AUROC, global AUROC (p38).
  - Binary predicates with **explicit but unjustified thresholds**: **DockQ > 0.23** and
    **DockQ > 0.49** for antibody interfaces (Fig 3 p7, Fig 4 p8) — thresholds shown on the axis,
    never justified in text; **< 2 Å** ligand-pose success for Polaris-ASAP (Fig 4 right, p8) —
    threshold in the axis label only; **Perc. within 1 and 2 kcal/mol** (p38, defined but the
    choice of 1 and 2 kcal/mol is not justified); **Enrichment Factor at 0.5/1/2/5%** (p38);
    **ABFE binding region < −5.45 kcal/mol** (Fig 8 legend, p11) — the threshold that converts
    every "predicted to bind" statement on p11 into a count, and **its derivation is NOT REPORTED
    anywhere in the paper**.
  - **No conformational-state predicate of any kind exists in this paper.** No active/inactive
    call, no RMSD-to-alternate-state, no state label.
- **metric_saturation**: **YES, numerically, in the affinity tables.** "Perc. within 2 kcal/mol"
  ceilings at 1.00 for two methods on the 4-target FEP subset — FEP+ non-centered/centered = 1.00,
  and BACPI centered = 1.00, with Boltz-2 at 0.97/0.98 and OpenFE at 0.98 (Table 12, p42): the
  metric cannot separate the best from the worst method there. Per-assay panels hit the same
  ceiling: Fig 12 p44 shows "|Δ| < 2 : 100.0%" for P21453, P43115, P56817 and O43570 (centered).
  The OpenFE-subset "Perc. within 2, cent." column is 0.91–0.97 across all five methods
  (Table 11, p42), i.e. compressed into the top 6 points of its range.
  *(Axis truncations in Figs 1 and 5 are figure defects and are recorded in `hides`, per v3 rule 9,
  not duplicated here.)*
- **directional_control**: **YES for geometry and experimental modality; NO for conformational
  state.** Handles named by the paper, all inference-time:
  1. **Experimental-method conditioning** — a one-hot method token: p24, "at training time, we
     condition the model to the experimental method … At inference time, users can decide on which
     experimental method to use to condition the model's prediction." Methods listed p24: "X-ray
     diffraction, electron microscopy, solution NMR, solid-state NMR, molecular dynamics,
     distillation from AlphaFold2 and distillation from Boltz-1." This is the **only handle with a
     demonstrated effect on the output distribution** (Fig 5 p8; Tables 9–10 p40: Boltz-2-MD vs
     Boltz-2-Xray, global RMSF r 0.67 vs 0.48 on mdCATH, 0.65 vs 0.57 on ATLAS). It selects
     *ensemble breadth and B-factor character*, not a named conformational state.
  2. **Multimeric template conditioning + template steering** — p24: "we allow for multimeric
     templates and we allow the user to strictly enforce that templates are respected via a
     Boltz-steering potential", pushing template atoms "to have a structure within α_cutoff Å of
     the given template". **Not evaluated in this version (p40).**
  3. **Contact and pocket conditioning + steering** — p25, distance constraints "constrained to be
     4Å ≤ d ≤ 20Å", fed as pairwise features and additionally enforced by a steering potential.
     **Not evaluated in this version (p40).**
  4. **Seeds** — "single seed" at evaluation (p35); diffusion multiplicity 32 at training
     (Table 6, p29). Not offered as a control handle.
  - **No state-annotated template, no state-filtered MSA, no state label input exists.** In
    principle a user could supply a state-specific template and enforce it via template steering,
    but the paper never frames, tests or claims this.
- **anti_memorization_design**: **PRESENT and multi-layered. This is the authoritative record of
  the Boltz-2 cutoff.**

  **THE TRAINING CUTOFF, VERBATIM:**
  > "We use every PDB structure up to the **training date cutoff of 06/01/2023**." — **p16**
  (Appendix A.1.1, first bullet).

  Restated twice more, in ISO form:
  > "The experimental data used for training comprises structures in the Protein Data Bank (PDB)
  > [Berman et al., 2000] **released before 2023-06-01**." — **p3** (§2, Structural Data).

  > "Given that all entries from the MD datasets correspond to PDB structures released before the
  > **validation cutoff date of 2023-06-01** …" — **p19** (A.1.5).

  Held-out sets built against it:
  - **Validation set, n = 398 PDB structures** — p19: "Initial release date is before 2023-06-01
    (exclusive) and 2024-01-01 (inclusive)", resolution < 4.5 Å, all protein sequences absent from
    every training cluster (mmseqs at 0.4 identity), plus a ligand-novelty condition ("At least one
    of the small-molecules exhibits a Tanimoto similarity of 0.85 or less to any small-molecule in
    the training set"). "This results in a total of 398 structures from PDB in our validation set."
  - **Structure test set, n = 2315 unique targets** — p35: "recently released structures from the
    PDB, specifically from **01/01/24 to 12/31/2024**. We filter the structures such that a target
    is kept if it has at least one monomer that is **more than 40% sequence dissimilar** to chains
    in the training data … This yields a final set of 2315 unique targets." Framed at p6 as "a wide
    variety of complexes submitted to the Protein Data Bank in 2024 and 2025 that were
    significantly different from any structure that **any of the models** had seen in their
    training set."
  - **MD test sets, n = 40 complexes per dataset** (mdCATH, ATLAS) — p19: clusters chosen greedily
    by smallest membership, then "Trajectories from the selected clusters **and all of their
    cluster members are then removed from the training set across all 3 MD datasets**", repeated
    "until we achieve a desired test set of 40 complexes per dataset."
  - **Affinity leakage control, sequence level** — p37: "we exclude from the training set any
    proteins with **sequence similarity ≥ 90%** to proteins in the validation or test sets…
    **This filtering is applied to all benchmark datasets except for CASP16 and the Recursion
    internal assays: CASP16 data was released after our training data cutoff, and the Recursion
    benchmarks consist of proprietary internal targets not accessible to external sources.**"
    Restated at p9: "The training sets are filtered to exclude proteins with ≥ 90% sequence
    identity to any protein in the FEP+ benchmark, ensuring that we benchmark on unseen proteins."
  - **Compound-level (not just protein-level) leakage check** — p37: "for the FEP+ benchmark, we
    assess the impact of compound similarity … We observe no significant dependence between
    prediction performance and compound similarity. We perform the same analysis on the CASP16
    benchmark, obtaining **maximum Tanimoto similarities of 0.41 for the L1000's compounds and
    0.59 for the L3000's compounds**."
  - **Structural quality filter that is itself model-derived** — p20: assays kept only if the mean
    ipTM over 10 random binders exceeds **0.75**; Table 1 (p4) gives before/after counts.

  **Caveat that belongs with the cutoff:** the affinity data has **no date cutoff of its own**
  stated anywhere. ChEMBL v34, PubChem 1.8.1, BindingDB versions are given (p19) but no cutoff
  date; affinity leakage is controlled by 90% sequence identity, not by time.

- **anti_memorization_control**: **RUN, and analysed — three arms.** This is not merely a held-out
  set existing.
  1. **Compound-similarity stratification on FEP+** — Fig 10, p38: per-assay Pearson R plotted in
     four maximum-Tanimoto bins with n printed, **N = 289 / 288 / 108 / 182**. Conclusion, p38
     caption: "We observe no strong dependence between compound similarity and predictive
     performance." Adequately powered.
  2. **Scaffold-novelty check on the generated TYK2 ligands against the structure-module training
     set** — p49–50, Fig 22: "none of the SynFlowNet–KLIFS ligand pairs exhibited high similarity,
     with a **maximum Tanimoto score of just 0.396** between the most similar scaffold pairs"
     (10 generated × 47 KLIFS binders). Small on the generated side (n = 10) — treat as
     **UNPOWERED on the generated axis**.
  3. **Cluster-level removal for MD test sets** (p19, quoted above) — the whole cluster is deleted
     from training, not just the test member. Run and reflected in Tables 9–10, p40.
  Additionally, a leakage control applied to a *baseline* rather than to Boltz-2, p36:
  "AlphaFlow is excluded from the ATLAS evaluation given that its training set largely overlaps
  with the test set constructed for Boltz-2."
  **NOT run:** no post-cutoff conformational-state arm, because no state task exists here; no
  ablation isolating the contribution of any data source, and the paper says why (p40, quoted in
  the Document Type header).

- **controls_run**

| control | what it rules out | page |
|---|---|---|
| **Boltz-2 ipTM** as an affinity predictor (all four affinity benchmarks) | That the affinity signal is just the confidence head / structural plausibility. It is not: R = −0.07 (OpenFE), 0.04 (4-target), 0.12 (CASP16); AP 0.0046 on MF-PCBA | p42 (T11–13), p43 (T14) |
| **GAT** = BACPI with the protein-sequence CNN deactivated ("we train ligand-only models to estimate the ligand bias in the data") | Ligand-only shortcut: that the benchmark is solvable from the SMILES alone | p39; p42–43 |
| **BACPI** sequence-based ML baseline | Isolates the gain attributable to predicted 3D structure over sequence-only learning | p39; p42–43 |
| **Chemgauss4 / OpenEye FRED docking** baseline on MF-PCBA | That a conventional docking score would do as well for hit discovery (AP 0.0051 vs 0.0248) | p39, p42 |
| **MM/PBSA, FMO, Chemgauss4** on the 4-target FEP subset | That cheap physics already reaches the same accuracy (0.18 / 0.55 / 0.26 vs 0.66) | p42 |
| **Random-molecule arm, N = 10**, in the TYK2 screen | That any molecule scores well / that ABFE calls everything a binder — "all 10 random compounds are predicted to be non-binders" | p11; p46 (Fig 15), Table 17 |
| **Public TYK2 binders arm, N = 10** (positive control from the protein-ligand benchmark) | That the screen score has no relation to known actives | p46 (Table 17, Fig 15) |
| **Synthetic decoys, Tanimoto < 0.3 to any binder of a 90%-identity-clustered target** (training-time) | Trivial distributional shortcuts between actives and decoys; also caps false-negative decoys | p4; p22 |
| **Second, differently-hyperparameterised affinity model used as an independent filter for the generative screen** | Reward hacking of a single scorer by SynFlowNet | p26 |
| **Method-conditioning arm: Boltz-2-Xray vs Boltz-2-MD, same weights** | That the MD gains come from the weights rather than the conditioning token | p40 (T9–10), p8 (Fig 5) |
| **Steering on/off: Boltz-1 vs Boltz-1x, Boltz-2 vs Boltz-2x** | That the physicality gain is not attributable to Boltz-steering; also that steering costs accuracy (it does not) | p6–7 (Fig 3) |
| **Compound-similarity binning on FEP+ (N = 289/288/108/182)** | Memorisation of near-duplicate compounds | p38 (Fig 10) |
| **AlphaFlow excluded from ATLAS for train/test overlap** | A baseline advantaged by leakage | p36 |
| **Two blinded arms: CASP16 out-of-the-box, 8 proprietary Recursion assays** | Input curation / benchmark-specific tuning | p9, p10, p43 |
| **ABFE protocol pre-validated on protein-ligand-benchmark (R = 0.95, cMAE 0.42 kcal/mol)** before being used as the TYK2 oracle | That the validating simulation is itself unreliable on this target — but see `oracle_leakage` route 7a: this is also how the target was chosen | p10 |

- **confidence_as_discriminator**: **Used heavily as a ranking and filtering device; validated
  only in the negative, and never validated for conformational correctness.**
  - *What the confidence module is and what it predicts.* p25: "The confidence module of Boltz-2
    has an architecture that resembles that of AlphaFold3's confidence model … we opted for a
    faster architecture, using **eight PairFormer layers** (versus the four of AlphaFold3) on top
    of the final pair token representation of the structure trunk and the encoding of the predicted
    coordinates. Unlike previous models, we found it beneficial to **divide the final heads
    predicting the PDE and PAE logits into two separate layers, one making the prediction for pairs
    of tokens within the same chain/molecule and one … across different chains/molecules.**"
    Confidence training is a single stage, crop 512, "**only trained on PDB data**" (p29).
    **The paper never states what pLDDT or pTM are trained to predict — those two terms do not
    appear as trained heads anywhere in the text. Only PDE, PAE, and the derived ipTM/PDE/iPDE
    scores are named. So: PDE/PAE = NAMED AND TRAINED (as logits over pairwise distance error and
    aligned error); pLDDT and pTM = NOT REPORTED in this paper.**
  - *Trained for robustness to inference settings* — p29: "In order to make the confidence model
    more robust to different inference hyperparameters, at every training iteration, we randomly
    sampled the number of inference steps between [20, 50, 200] and the diffusion step scale
    between [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]."
  - *A separate, additional local-flexibility head.* p5: "The trunk's final representation was also
    supervised to predict the B-factor of each token", with MD B-factors derived from RMSF via
    B = (8π²/3)·RMSF² (p28), loss weight 1×10⁻³ (Table 6, p29). p8 offers this as a partial
    explanation for the RMSF results: "Boltz-2's performance may also benefit from supervision on
    both experimental and computational B-factor estimates, which are specifically designed to
    capture local structural dynamics."
  - *Uses as a discriminator, all of them non-conformational:*
    (i) sample ranking — top-1 of 5 by confidence (p35), by protein–ligand ipTM for the affinity
    input (p26, p30, p31);
    (ii) training-data admission — assays kept only if mean ipTM over 10 binders > 0.75 (p20),
    and Table 1 (p4) reports the counts lost: 1.45M → 1.2M binders, 3.5M → 1.8M HTS decoys;
    (iii) distillation-set admission at explicit thresholds — RNA "maximum average predicted
    distance error (PDE) ≤ 2.0"; protein-DNA "PDE ≤ 2.0, iPDE ≤ 1.0 and ipTM ≥ 0.7";
    RNA-ligand "iPDE ≤ 1.0 or ipTM ≥ 0.7"; protein-ligand "iPDE ≤ 1.0 and ipTM ≥ 0.9";
    TCR-pMHC "iPDE ≤ 1.0, PDE ≤ 1.0, ipTM ≥ 0.8"; pMHC "ipTM ≥ 0.85"; AFDB "minimum global lDDT
    of 0.5" (p17–18).
  - **The one place the paper validates a confidence score as a discriminator, it fails.** ipTM is
    run as an explicit baseline for binding affinity and is near-useless: Pearson R **−0.07**
    (OpenFE, Table 11 p42), **0.04** (4-target subset, Table 12 p42), **0.12** (CASP16, Table 14
    p43); on MF-PCBA it gives **AP 0.0046, EF@0.5% = 2.42, AUROC 0.5657** against Boltz-2's
    0.0248 / 18.39 / 0.8122 (Table 13, p42). Stated in the text, p10: Boltz-2 "substantially
    outperforms prior machine learning approaches, **the widely used ipTM** and docking".
  - **Never used or validated as a discriminator of conformational correctness.** No experiment in
    the paper asks whether confidence tracks which conformational state was produced. Since the
    affinity module *consumes* the ipTM-selected structure, any conformational error in that
    selection propagates — which the authors say explicitly at p12: "If the model fails to identify
    the correct pocket or inaccurately reconstructs the binding interface or **conformational state
    of the protein**, downstream affinity predictions are unlikely to be reliable."

---

## D. Claims

- **central_conclusion**: Boltz-2 is a co-folding foundation model that adds a two-headed affinity
  module (binding likelihood + continuous affinity value) on top of a Boltz-1-lineage trunk, trained
  on a PDB-to-2023-06-01 structural corpus extended with NMR/MD ensembles, AF2 and Boltz-1
  distillation, and millions of curated ChEMBL/BindingDB/PubChem assay measurements. Its headline
  claim is that it approaches FEP-level affinity correlation at >1000× lower cost. Structure
  accuracy is only modestly better than Boltz-1 and still behind AlphaFold3; the physics-based
  inference-time steering (Boltz-steering) buys physical validity rather than accuracy; MD
  conditioning improves RMSF correlation to roughly the level of dedicated MD emulators. The model
  does not attempt, and explicitly does not achieve, large conformational-change prediction.

- **necessity_claims** — verbatim, with page:
  1. p2: "In fact, **no AI-based model has yet matched the accuracy of FEP methods or laboratory
     assays for binding affinity prediction.**"
  2. p1: "Despite its importance in drug design, in-silico affinity prediction remains an open
     challenge. To date, the most accurate techniques are atomistic simulations like free-energy
     perturbations (FEP). However, **they are far too slow and expensive to be used at scale.
     Faster methods, such as docking, are not precise enough to give a reliable signal.**"
     (sentence spans p1–p2)
  3. p20: "Since our model leverages protein–ligand complex structures as input, **it is essential
     to ensure the structural quality of the training data.**"
  4. p12: "Boltz-2 relies on predicted 3D protein–ligand structures and reliable trunk features as
     input to the affinity module. **If the model fails to identify the correct pocket or
     inaccurately reconstructs the binding interface or conformational state of the protein,
     downstream affinity predictions are unlikely to be reliable.**"
  5. p3: "While large amounts of binding data are publicly available, in their raw form **they are
     not suitable for training due to experimental differences and noise.**" (also p2, near-identical)
  6. p33 (on generative design): "generative models would often adversarially exploit the scoring
     function and generate non-sensical molecules, for example, by simply concatenating high-reward
     functional groups together."
  7. p12 (limitation stated as a persisting impossibility): "**the model still often fails to
     capture large conformational changes, such as those that can be induced by binding.**"

- **novelty_claims** — verbatim, with page:
  1. p1 (abstract): "Boltz-2 … **is, to our knowledge, the first AI model to approach the
     performance of free-energy perturbation (FEP) methods in estimating small molecule–protein
     binding affinity.** Crucially, it achieves strong correlation with experimental readouts on
     many benchmarks, **while being at least 1000× more computationally efficient than FEP**."
  2. p12 (conclusion): "Crucially, Boltz-2 **is, to our knowledge, the first AI model to approach
     the accuracy of FEP methods for predicting binding affinities on the FEP+ benchmark**, while
     offering orders-of-magnitude gains in computational efficiency."
  3. p1 (introduction): "Boltz-2 improves structural accuracy across modalities, extends
     predictions from static complexes to dynamic ensembles and **sets a new standard in physical
     grounding.**"
  4. p2: "**Boltz-2 overcomes this long-standing performance/compute time trade-off.**"
  5. p9: "Yet, **Boltz-2 outperforms all top-ranking participants by a clear margin**" (CASP16),
     and p2: "On the CASP16 affinity track, retrospective evaluation shows that **Boltz-2
     outperforms all submitted competition entries out of the box.**"
  6. p24 (templates): "**As a departure from previous work, our templating approach also natively
     supports the use of multimeric templates.**" And "**Unlike previous approaches, we allow users
     to either enforce strict observance of the templates via steering** or just use the
     soft-conditioning like previous methods."
  7. p23 (tokenization): "**Unlike AlphaFold3, Chai-1, and Boltz-1**, where non-canonical amino
     acids and nucleotides are tokenized at the atomic level, we keep them as a single token as
     well."
  8. p25 (confidence): "**Unlike previous models, we found it beneficial to divide the final heads
     predicting the PDE and PAE logits into two separate layers.**"
  9. p11: "**Together, these results demonstrate how Boltz-2 enables structure-based prioritization
     at a large scale.**"

  **Note on the FEP claim's scope, recorded because it is what the claim rests on and not as
  dispute:** the headline "approaches FEP" number is **Pearson R = 0.66 averaged over 4 targets**
  (CDK2, TYK2, JNK1, P38; 87 neutral compounds), against FEP+ at 0.78 and OpenFE at 0.66
  (Table 12, p42; p9). On the larger 876-complex OpenFE subset Boltz-2 is 0.62 vs OpenFE 0.63 and
  FEP+ 0.72 (Table 11, p42). The FEP+ baseline is described by these authors as protocol-tuned
  after seeing the experimental error (p39, quoted at `oracle_leakage` route 4).

- **stated_limits** (§6, p11–12, plus scattered admissions):
  1. **MD** — p11: "the model does not significantly deviate from other baselines such as AlphaFlow
     or BioEmu. The current model used a relatively small MD dataset at the later stages of
     training, with minor architectural changes to account for multiple conformations." And p29:
     "The molecular dynamics data was not included in the first stage of training due to project
     timing, we would expect bigger gains in the model's ability to model dynamics had this data
     been integrated in the model earlier."
  2. **Structure** — p12: "the model does not significantly deviate from the structure prediction
     performance of its predecessors. This similarity is primarily due to the use of largely
     identical structural training data, a similar architectural design, and withstanding
     limitations in predicting complex interactions, particularly within large complexes. In
     addition, the model still often fails to capture large conformational changes."
  3. **Affinity depends on structure** — p12, quoted in full under `necessity_claims` item 4;
     plus "the affinity module does not explicitly handle such cofactors, including ions, water, or
     multimeric binding partners" and "an insufficiently large affinity crop size could be limiting
     … e.g., in the case of both orthosteric and allosteric modulators."
  4. **Range of applicability unknown** — p12: "we notice in Figures 12-14 that the performance
     varies strongly between assays. Further work is needed to determine the source of this
     variance."
  5. **Public benchmarks overstate real-world performance** — p10: "We include these results as a
     reminder that strong performance on public benchmarks does not always immediately translate to
     all complexities of real-world drug discovery." Backed by numbers at p43: private assays
     R = 0.39 vs validation 0.42, but "the centered MAE = 1.36 kcal/mol is significantly worse
     compared to the validation set (MAE = 0.86 kcal/mol)", per-target R from 0.165 to 0.634.
  6. **Data curation admittedly shallow** — p20: "our affinity value curation only scratches the
     surface of what is possible"; p22 on binary labels: "Our current strategy … provides an initial
     filter but does not fully ensure reliability or biological relevance."
  7. **HTS labels are ~40% false positive** — p21: "we estimate that approximately 40% of the
     compounds labeled as actives in high-throughput primary screens may be false positives."
  8. **The affinity value is not a well-defined physical quantity** — p5: "the predicted value
     should be viewed as a general measure of binding strength that supports ranking and can be
     approximately interpreted as an IC50-like value."
  9. **No ablations; paper incomplete** — p40, both sentences quoted in the Document Type header.
  10. **Benchmarks themselves are flawed** — p37: "Many widely used benchmarks employ subselection
      strategies that introduce artificial biases and obscure the challenges inherent in real-world
      campaigns."
  11. **Generated molecules are single-objective** — p47 and p49 figure notes: "We remind the reader
      that the molecules were solely optimized for their Boltz-2 score. Other properties, such as
      toxicity, solubility, metabolism, etc. are ignored."

- **stance**: **`background` + `precedent`** — provisional, the user's call.
  - *background*: this is the specification sheet for a model used as a backbone elsewhere; its
    cutoff, sampling defaults, confidence semantics and training composition are inputs to other
    work rather than claims to be argued with.
  - *precedent*: it establishes an inference-time steering mechanism operating on the reverse
    diffusion trajectory via differentiable potentials, plus conditioning handles (method, template,
    contact, pocket) — the machinery a conformational-steering method would extend. It is precedent
    for the mechanism and explicitly *not* precedent for the conformational application, since the
    potentials target physical validity and restraint satisfaction only and the controllability
    features are unevaluated (p40).
  - *A case for `contrast` exists* (n = 4 targets behind the headline FEP claim; a protocol-tuned
    FEP+ baseline; a self-authored simulation oracle standing in for experiment on the one
    prospective arm) but the paper states each of these itself, so it is not a strawman-attack
    target; flagged rather than asserted.

---

## E. Quantitative comparators

- **metrics_reported**

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Intra-protein lDDT | 0.86 (Boltz-2), 0.86 (Boltz-2x); AF3 0.87, Chai-1 0.84, ProteinX 0.85, Boltz-1 0.86 | lDDT | PDB 2024 held-out set, 2315 targets, ≥40% seq-dissimilar; top-1 of 5 | p7 (Fig 3) |
| Intra-DNA lDDT | 0.78 (Boltz-2 and Boltz-2x); AF3 0.81, Chai-1 0.75, ProteinX 0.77, Boltz-1 0.78 | lDDT | same | p7 |
| Intra-RNA lDDT | 0.62 (Boltz-2), 0.62 (Boltz-2x); AF3 0.66, Chai-1 0.58, ProteinX 0.62, Boltz-1 0.60 | lDDT | same | p7 |
| Intra-ligand lDDT | 0.92 (Boltz-2/2x); AF3 0.94, Boltz-1 0.93 | lDDT | same | p7 |
| Ligand–protein lDDT | 0.68 (Boltz-2 and Boltz-2x); AF3 0.73, Boltz-1 0.69 | lDDT | same | p7 |
| Physical validity | **0.97 (Boltz-1x), 0.94 (Boltz-2x)** vs 0.38 (Boltz-2), 0.33 (Boltz-1), AF3 0.49 | fraction | same — the single largest effect of Boltz-steering in the paper | p7 |
| Protein–protein DockQ > 0.23 | 0.73 (Boltz-2/2x); AF3 0.76, Boltz-1 0.73 | fraction | same | p7 |
| Protein–protein DockQ > 0.49 | 0.64 (Boltz-2), 0.63 (Boltz-2x); AF3 0.68, Boltz-1 0.65 | fraction | same | p7 |
| Protein–RNA DockQ > 0.49 | 0.14 (Boltz-2), 0.11 (Boltz-2x); AF3 0.07 | fraction | same — floor region, all methods ≤ 0.14 | p7 |
| Antibody DockQ > 0.23 | 0.40 (Boltz-2x), 0.38 (Boltz-2); **AF3 0.49**, Chai-1 0.37, ProteinX 0.33, Boltz-1 0.32, Boltz-1x 0.32 | fraction | antibody benchmark, n NOT REPORTED | p8 (Fig 4 left) |
| Antibody DockQ > 0.49 | 0.27 (Boltz-2), 0.26 (Boltz-2x); Boltz-1 0.22, ProteinX 0.19, AF3 0.13 (as plotted) | fraction | same | p8 |
| Polaris-ASAP ligand pose success (<2 Å) | **Boltz-2 84.8%**, Boltz-1 79.4%; top competition entries 48.1–86.4% | % | Polaris-ASAP retrospective, SARS-CoV-2/MERS-CoV Mpro; no fine-tuning, no relaxation | p7, p8 (Fig 4 right) |
| Global RMSF Pearson r, mdCATH | **Boltz-2-MD 0.67**; Boltz-2-Xray 0.48, Boltz-1 0.46, BioEmu 0.53, AlphaFlow 0.24 | r | mdCATH held-out, 40 complexes, 100 samples vs 200 frames | p40 (T9) |
| Per-target RMSF Pearson r, mdCATH | Boltz-2-MD 0.79; Boltz-1 0.70, AlphaFlow 0.77, BioEmu 0.77 | r | same | p40 |
| Global RMSF Pearson r, ATLAS | **Boltz-2-MD 0.65**; Boltz-2-Xray 0.57, Boltz-1 0.38, BioEmu 0.56 | r | ATLAS held-out, 40 complexes (AlphaFlow excluded for train/test overlap) | p40 (T10) |
| Per-target RMSF Pearson r, ATLAS | Boltz-2-MD 0.85; Boltz-1 0.77, BioEmu 0.83 | r | same | p40 |
| Per-target RMSF RMSE, ATLAS | Boltz-2-MD 12.35; Boltz-1 19.62, BioEmu 15.04 | RMSE | same | p40 |
| Ensemble diversity lDDT | Boltz-2-MD 0.32; reference 0.23, Boltz-1 0.12 (mdCATH panel) | 1 − lDDT | Fig 5 — MD conditioning over-diversifies relative to reference | p8 |
| **FEP+ 4-target Pearson R** | **Boltz-2 0.66**; FEP+ 0.78, ABFE 0.75, OpenFE 0.66, FMO 0.55, GAT 0.40, Chemgauss4 0.26, MM/PBSA 0.18, BACPI 0.14, Boltz-2 ipTM 0.04 | Pearson R, per-assay avg | 4 targets (CDK2, TYK2, JNK1, P38), 87 neutral compounds; train filtered at ≥90% seq id | p9, p42 (T12) |
| FEP+ 4-target Kendall τ | Boltz-2 0.48; FEP+ 0.63, ABFE 0.54, OpenFE 0.51 | τ | same | p42 |
| FEP+ 4-target inference time | **Boltz-2 20 GPU sec** vs OpenFE 6–12 GPU hours, ABFE >20 GPU hours | time/ligand | basis of the ">1000× faster" claim | p42 (T12), p1, p9 |
| FEP+ 4-target Perc. within 2 kcal/mol (cent.) | Boltz-2 0.98; **FEP+ 1.00, BACPI 1.00**, OpenFE 0.98 | fraction | same — metric ceiling, see `metric_saturation` | p42 |
| **OpenFE-subset Pearson R** | **Boltz-2 0.62**; FEP+ 0.72, OpenFE 0.63, BACPI 0.29, GAT 0.28, Boltz-2 ipTM −0.07 | Pearson R, per-assay avg | OpenFE subset of FEP+, 876 protein–ligand complexes | p42 (T11), p9 |
| OpenFE-subset centered MAE | Boltz-2 0.64; FEP+ 0.64, OpenFE 0.94 | kcal/mol | same | p42 |
| **CASP16 Pearson R** | **Boltz-2 0.65**; best entrant LG016 0.54, LG055 0.47, LG082/LG207/LG008 0.38, GAT 0.50, BACPI 0.41, Boltz-2 ipTM 0.12 | Pearson R, target avg | CASP16 affinity challenge, 140 protein–ligand pairs / 2 targets, blind, out of the box | p9, p43 (T14) |
| CASP16 Kendall τ | Boltz-2 0.45; best entrant 0.42 | τ | same | p43 |
| **MF-PCBA average precision** | **Boltz-2 0.0248**; GAT 0.0133, BACPI 0.0131, Chemgauss4 0.0051, Boltz-2 ipTM 0.0046 | AP | MF-PCBA test set, 10 HTS assays × 50k complexes | p42 (T13), p10 |
| **MF-PCBA enrichment factor @0.5%** | **Boltz-2 18.39**; GAT 11.12, BACPI 9.48, ipTM 2.42, Chemgauss4 2.00 | EF | same | p42, p10 |
| MF-PCBA EF @1% / @2% / @5% | 13.95 / 10.57 / 7.04 | EF | same | p42 |
| MF-PCBA AUROC (target avg / global) | Boltz-2 0.8122 / 0.8056; GAT 0.7928, BACPI 0.7575, ipTM 0.5657, Chemgauss4 0.5450 | AUROC | same | p42 |
| Per-assay AUROC spread, MF-PCBA | 0.64 – 0.92 across the 10 assays | AUROC | Fig 13, per-assay ROC | p45 |
| Hit-to-lead validation-set Pearson R | Boltz-2 0.4246; GAT 0.2512, BACPI 0.1997 | Pearson R | 16 assays selected from the training corpus | p43 (T15), p36 |
| Per-assay Pearson R spread, validation set | **0.732 (P56817-adjacent max) down to 0.056** — stated in text as "ranging from 0.732 to 0.056" | Pearson R | 16 assays, per-assay; Fig 12 gives all panels | p42, p44 |
| **Private (Recursion) Pearson R** | **Boltz-2 0.39**; GAT 0.16, BACPI 0.11 | Pearson R, target avg | 8 blinded internal hit-to-lead assays | p43 (T16), p10 |
| Private centered MAE | Boltz-2 1.36 (vs 0.86 on validation set) | kcal/mol | same | p43 |
| Per-assay spread, private | Pearson R 0.165–0.634; centered MAE 0.855–1.734 kcal/mol; ">0.55 on 3 out of 8 assays, but limited performance on the other 5" | — | same | p10, p43 |
| TYK2 screen score vs ABFE correlation | **&#124;R&#124; = 0.74** | Pearson &#124;R&#124; | 50 compounds (5 streams × N = 10) | p11 (Fig 8) |
| TYK2 prospective hit rate | 8/10 (Enamine HLL), 10/10 (Enamine Kinase), 10/10 (SynFlowNet), 0/10 (random) predicted to bind | count | ABFE estimate, binding region < −5.45 kcal/mol | p11; p46 |
| Boltz-ABFE on protein-ligand-benchmark | Pearson R = 0.95, centered MAE = 0.42 kcal/mol, offset 0.92 kcal/mol | — | validation of the oracle used for the TYK2 screen | p10 |
| Boltz-2 on TYK2 (protein-ligand benchmark) | Pearson R = 0.83 | Pearson R | flagged by the authors as making the TYK2 result "optimistic" | p11 |
| Max scaffold Tanimoto, generated vs KLIFS TYK2 binders | 0.396 | Tanimoto | 10 SynFlowNet compounds × 47 KLIFS binders, Murcko scaffolds | p49–50 (Fig 22) |
| CASP16 max compound Tanimoto to affinity training set | 0.41 (L1000), 0.59 (L3000) | Tanimoto | leakage check | p37 |
| Inference cost | ~20 s per ligand; "hundreds of thousands of compounds per day" on parallel HPC; 60 H100 workers; ~1,000 GPU-hours for the generative screen (~400k molecules, ~16 h) | — | TYK2 generative screen | p33–34 |
| Affinity training compute | 128 A100 GPUs, AdamW, lr 1e-4, weight decay 0.001; ensemble members trained on 55M and 12.5M samples | — | Tables 3 and text | p27 |

- **n_predictions**:
  - **Samples per target — the defaults, gathered in one place:**
    - Structure evaluation (all models, all backbones): **5 recycling rounds, 5 diffusion samples,
      single seed**, top-1 by confidence (p35).
    - Affinity module input: **5 recycling iterations, 200 diffusion steps, 5 candidate
      structures**, best by protein–ligand ipTM (p26, p31).
    - Pocket pre-processing: **10 recycling steps, 200 diffusion iterations, 5 structural samples**,
      over 10 randomly sampled binders per target, consensus vote (p30).
    - MD evaluation: **100 samples** per target against **200 reference frames** (p35).
    - Boltz-1 distillation generation: **3 recycling steps, 3 diffusion samples** (p17).
    - Confidence training randomised over inference steps **[20, 50, 200]** and step scale
      **[1.0–1.5]** (p29).
    - Diffusion process hyperparameters (Table 7, p29): sigma_min 1e-4, rho 7, gamma_0 0.8,
      gamma_min 1.0, noise scale 1.003, **step scale 1.5**. Training diffusion multiplicity 32
      (Table 6, p29).
  - **Targets:** 2315 structure targets; 40 + 40 MD complexes; 876 + 87 + 140 + (10 × 50,000)
    affinity data points; 16 validation assays; 8 private assays; 1 prospective target.
  - **Totals for the screen:** 460,160 (HLL) + 64,960 (Kinase) + 117,199 unique SynFlowNet
    compounds scored out of ~400,000 sampled; 50 compounds carried to ABFE (5 streams × 10)
    (p11; Table 17, p46).
  - **Training scale (Table 1, p4):** 1.2M binders / 1.2M synthetic decoys (ChEMBL+BindingDB,
    2k targets, 600k compounds); 200k binders / 1.8M decoys (PubChem HTS); 25k / 115k (CeMM);
    10k / 50k (PubChem small assays); 2k / 20k (MIDAS). Structure training steps 88k + 4k + 4k + 1k
    across four crop-size stages (Table 5, p29).
- **comparable_to_ours**: *(left empty — v3)*
- **si_in_scope**: **SI HELD.** Appendices A–E are inside this same PDF (pp. 14–50) and carry
  Tables 1–17 and Figures 9–23, including every per-benchmark table. Three genuine gaps, all
  internal to the paper rather than to the corpus:
  1. **Per-compound data for the 8 Recursion assays is proprietary** — p37: "the Recursion
     benchmarks consist of proprietary internal targets not accessible to external sources." Only
     aggregate R/τ/MAE (Table 16, p43) and unlabelled scatters (Fig 14, p45) are given; the assays
     are identified only as "Assay id 1–8".
  2. **No evaluation of template, contact or pocket conditioning exists** — p40: "In the coming
     weeks, we will integrate even more results to the paper including evaluations of the template,
     contact and pocket conditioning."
  3. **No ablations** — p40: "comprehensive ablation studies isolating the impact of each
     architectural or training component on final performance are not computationally feasible."
  Code, weights and data are released (p1, footnote 1: https://github.com/jwohlwend/boltz), so the
  hyperparameters not printed are recoverable — p29: "For a full list of the hyperparameters and
  their precise impact on the model, we recommend the reader to refer directly to the code
  repository."

---

## F. Figures

One row per panel group. Split on `mark` or `measure`; not on `facet` alone (v3 rule 8).

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 2 | Accuracy/speed Pareto front for affinity prediction; Boltz-2 sits above every method faster than an hour | scatter | `PLOT \| facet: none (1) \| vary: wall-clock time per ligand, 0.001–~50,000 s log (continuous) \| series: method type (3: ML, physics, Boltz-2) × hardware (2: GPU, CPU) \| measure: Pearson R correlation \| mark: point \| n: 1 per mark (each point = mean over 4 assays), 10 methods per panel` | 1 panel, 10 labelled methods, an annotated "Pareto front" curve and three vertical guides (1 min / 1 hour / 1 day) | **Y axis broken** — `//` break glyphs top and bottom of the y axis, so 0.0 and 0.8 are not true endpoints; **x axis broken** at the low end; a shaded "Low performance" band clips BACPI and Boltz-2-iptm out of readable range; **n = 4 targets is not shown on the figure** and appears only in the caption as "a 4-target subset"; no error bars although Fig 6 shows the same numbers do have bootstrap SE | CC-BY 4.0 International (header, p2 and every page). **No ND clause — redrawing permitted with attribution.** |
| 2 | 4 | Boltz-2 architecture: trunk → denoising with Boltz-steering → confidence module → affinity module | schematic | `SCHEMATIC \| model architecture block diagram: input sequence + user conditioning → atom attention encoder, template and MSA modules, PairFormer trunk with recycling → distogram & B-factor heads, reverse diffusion with conditioning & physics potentials → confidence output and affinity module producing binding likelihood + affinity value \| no data` | 1 | | CC-BY 4.0, p4 |
| 3 | 7 | Seven co-folding models across 12 structural metrics on the unseen-PDB set; Boltz-2 ≈ Boltz-1, behind AF3; Boltz-1x/2x dominate physical validity | bar | `PLOT \| facet: metric (12: intra-protein/DNA/RNA/ligand lDDT, ligand-protein lDDT, physical validity, protein-protein/DNA/RNA DockQ at >0.23 and >0.49) \| vary: model (7) \| series: model (7: AF3, Chai-1, Protenix, Boltz-1, Boltz-1x, Boltz-2, Boltz-2x) \| measure: mean lDDT, mean DockQ-threshold pass fraction, and physical-validity fraction \| mark: bar \| n: NOT REPORTED per mark; ≤2315 targets per panel, subsetted per modality` | 12 panels in 2 rows of 6; panels vary by metric and by modality; the same 7 models recur as bars in each | **n per bar is nowhere given** — the caption states only "Error bars indicate 95% confidence intervals", and the per-modality subset sizes of the 2315-target set are never printed; bars conceal the per-target distribution; y axes differ between the two rows (0–1.0 top, 0–0.8 bottom) making cross-row height comparison misleading | CC-BY 4.0, p7 |
| 4A | 8 | Antibody–antigen benchmark: Boltz-2 improves on Boltz-1 but still trails AlphaFold3 | bar | `PLOT \| facet: DockQ threshold (2: >0.23, >0.49) \| vary: model (7) \| series: model (7: AF3, Chai-1, ProteinX, Boltz-1, Boltz-1x, Boltz-2, Boltz-2x) \| measure: mean fraction of interfaces above DockQ threshold \| mark: bar \| n: NOT REPORTED per mark and per panel` | 2 threshold groups in one axes | **The benchmark size is never stated anywhere in the paper**; bars over an unstated n with 95% CI only | CC-BY 4.0, p8 |
| 4B | 8 | Polaris-ASAP ligand-pose competition, retrospective: Boltz-2 at 84.8% vs the top-10 entrants | bar | `PLOT \| facet: none (1) \| vary: competition entry (12: 10 entrants + Boltz-1 + Boltz-2) \| series: entry class (3: top-10 entries, Boltz-1, Boltz-2) \| measure: success rate, pose RMSD < 2 Å (%) \| mark: bar \| n: NOT REPORTED per mark and per panel` | 1 panel, 12 bars | **y axis truncated, starting at 30% not 0**, which roughly triples the apparent gap between Boltz-2 (84.8) and the weakest entrant (48.1); **n of the pose set is not given**; two entrants exceed Boltz-2 (86.4, 85.4) yet the text says Boltz-2 "shows a clear improvement over … the top performers in the challenge" | CC-BY 4.0, p8 |
| 5 | 8 | MD conditioning raises RMSF correlation and sample diversity on held-out mdCATH/ATLAS clusters | bar | `PLOT \| facet: metric (5: per-target RMSF Pearson, per-target RMSF Spearman, precision lDDT, recall lDDT, diversity lDDT) × dataset (2: mdCATH, ATLAS) \| vary: method (6) \| series: method (6: Boltz-2-Xray, Boltz-2-MD, Boltz-1, BioEmu, AlphaFlow, Reference) \| measure: correlation coefficient and lDDT-derived scores \| mark: bar \| n: 40 complexes per dataset per mark; 100 predicted samples vs 200 reference frames behind each bar` | 10 groups (5 metrics × 2 datasets) on shared axes | **Bars hide the per-target distribution** for a metric the paper elsewhere reports per target; **y axis starts at 0.50 for the four left metric groups and at 0.00 for the diversity group** on one shared plot, so heights are not comparable across the figure; AlphaFlow is silently absent from the ATLAS bars (the reason is on p36, not in the caption) | CC-BY 4.0, p8 |
| 6 | 9 | Boltz-2 approaches FEP on three affinity benchmarks | bar | `PLOT \| facet: benchmark (3: FEP+ 4 targets, FEP+ OpenFE 8 internal targets, CASP16) \| vary: method (10, 8 and 9 respectively) \| series: method class (5: Boltz-2 ours, Physics<1h, Physics>1h, ML, Unknown) \| measure: Pearson R correlation averaged over assays \| mark: bar \| n: 4 assays / 876 complexes / 140 pairs per panel; per-mark n = the same assay set` | 3 panels, one per benchmark; bar order differs per panel | **Bars over 4 assays** in the leftmost panel — the panel carrying the headline "approaches FEP" claim — with the per-assay spread (0.732 to 0.056 in the validation set, 0.165–0.634 in private assays) visible only in Figs 12/14; the middle panel is labelled "FEP+ OpenFE 8 internal targets" whereas the text and Table 11 describe 876 complexes, an unexplained inconsistency | CC-BY 4.0, p9 |
| 7A | 10 | Average precision on MF-PCBA: Boltz-2 nearly doubles the best ML baseline | bar | `PLOT \| facet: none (1) \| vary: method (5: Boltz-2, GAT, BACPI, Chemgauss4, Boltz-2 ipTM) \| series: method (5) \| measure: average precision (area under PR curve), assay-averaged \| mark: bar \| n: 10 assays per mark, each downsampled to 50,000 complexes` | 1 panel | Bars over 10 assays whose individual AP ranges 0.0018–0.0781 (Fig 13, p45) — the spread is 40× and is not visible here | CC-BY 4.0, p10 |
| 7B | 10 | Enrichment factor at four top-K cutoffs | bar | `PLOT \| facet: none (1) \| vary: top-K threshold (4: 0.5%, 1%, 2%, 5%) \| series: method (5: Boltz-2, GAT, BACPI, Chemgauss4, Boltz-2 ipTM) \| measure: enrichment factor at K% \| mark: bar \| n: 10 assays per mark` | 1 panel, 4 threshold groups | No error bars on the right panel although the left panel carries them; per-assay spread again pooled | CC-BY 4.0, p10 |
| 8A | 11 | Boltz-2 screen score correlates with ABFE ΔG across five compound streams | scatter | `PLOT \| facet: none (1) \| vary: Boltz-2 screen score, 0.0–1.1 (continuous) \| series: compound stream (5: random, public binders, Enamine HLL, Enamine Kinase, SynFlowNet) \| measure: ABFE readout (kcal/mol) \| mark: point (+ dashed OLS line) \| n: 1 per mark, 50 per panel (10 per stream)` | 1 panel, 5 colour-coded streams, regression line, &#124;R&#124; = 0.74 annotated | **&#124;R&#124; = 0.74 is computed across streams that were selected to differ**, so between-group separation inflates a within-stream correlation claim; n = 10 per stream; a single ABFE repeat per compound (p10, "a single repeat") with no simulation error bars | CC-BY 4.0, p11 |
| 8B | 11 | ABFE ΔG distributions per screening stream | violin | `PLOT \| facet: none (1) \| vary: screen group (5: random, public binders, HLL, Kinase, SynFlowNet) \| series: screen group (5) \| measure: ABFE-predicted ΔG (kcal/mol) \| mark: violin with overlaid points and median bar \| n: 10 per violin, 50 per panel` | 1 panel, 5 violins, shaded "binding region < −5.45 kcal/mol" band | **Violins over n = 10** — kernel density on ten points; the −5.45 kcal/mol binding threshold that defines every "predicted to bind" count on p11 is given only in the legend and **its derivation is not reported anywhere** | CC-BY 4.0, p11 |
| 9 | 34 | Fixed-library vs generative virtual-screening workflows | schematic | `SCHEMATIC \| two screening topologies: (A) fixed molecular library fanned out to parallel Boltz-2 workers producing an annotated library; (B) SynFlowNet sampling into Boltz-2 workers, annotated samples feeding back into model training \| no data` | 2 (A, B) | | CC-BY 4.0, p34 |
| 10 | 38 | Prediction accuracy vs compound novelty on FEP+ — the memorisation control | violin | `PLOT \| facet: none (1) \| vary: max Tanimoto similarity to affinity training set, 4 bins (0.3–0.5, 0.5–0.65, 0.65–0.8, 0.8–1.0) \| series: none (1) \| measure: per-assay Pearson R \| mark: violin \| n: N = 289 / 288 / 108 / 182 compounds per bin, aggregated to per-assay values` | 1 panel, 4 similarity bins, dashed weighted-average line | Bin n is printed (good), but the **number of assays per violin — the actual unit of the plotted distribution — is not**; violins reach below −0.5 R, so some assays are anti-correlated, a fact the "no strong dependence" caption does not engage | CC-BY 4.0, p38 |
| 11 | 41 | Per-residue predicted vs reference RMSF, all methods, both MD holdout sets | scatter | `PLOT \| facet: method (5 top: Boltz-2-Xray, Boltz-2-MD, Boltz-1, BioEmu, AlphaFlow; 4 bottom: same minus AlphaFlow) × dataset (2: mdCATH top, ATLAS bottom) \| vary: predicted RMSF (continuous, per-panel range) \| series: none (1) \| measure: ground-truth RMSF \| mark: point \| n: 1 per mark; per panel = all residues across 40 complexes, count NOT REPORTED` | 9 panels (5 + 4); each carries ρ, R and MSE in its title | **Free x-axis ranges across panels** (0–17.5, 0–20, 0–14, 0–50, 0–30 …), so identical point clouds look differently shaped and the visual comparison the figure invites is not valid; overplotting with no density encoding; the number of residues behind each panel is never stated | CC-BY 4.0, p41 |
| 12 | 44 | Per-assay predicted vs measured affinity for the 16 validation assays, annotated by protein class | scatter | `PLOT \| facet: assay (16, labelled by UniProt ID and protein class: 4 GPCR, 3 kinase, 3 protease, transcription factor, intracellular receptor, transporter, ion channel, lipid-associated, lyase) \| vary: measured affinity, −15 to −4 kcal/mol (continuous) \| series: none (1) \| measure: predicted affinity (kcal/mol) \| mark: point (+ y=x and ±1, ±2 kcal/mol guide lines) \| n: 1 per mark; per panel NOT REPORTED (only percentages within 1 and 2 kcal/mol are given)` | 16 panels, 4 × 4, one per assay | **Per-panel n is never given** — only percentages, so the 0.056-R panel cannot be weighted against the 0.732-R panel; shared axes are stated only on the bottom row | CC-BY 4.0, p44 |
| 13A | 45 | ROC curves for the 10 MF-PCBA test assays | line | `PLOT \| facet: assay (10 PubChem AIDs) \| vary: false positive rate, 0–1 (continuous) \| series: none (1) \| measure: true positive rate \| mark: line \| n: 50,000 complexes per panel (downsampled), actives count NOT REPORTED` | 10 panels in 2 rows; AUROC and AP annotated per panel | Active/inactive counts per assay not given, though AP values (0.0018–0.0781) imply a 40× swing in prevalence | CC-BY 4.0, p45 |
| 13B | 45 | Predicted-probability distributions for binders vs decoys, same 10 assays | density | `PLOT \| facet: assay (10 PubChem AIDs) \| vary: predicted probability, 0–1 (continuous) \| series: label (2: Active, Inactive) \| measure: density \| mark: filled density curve \| n: 50,000 complexes per panel, class sizes NOT REPORTED` | 10 panels, paired below the ROC row (letter shared with 13A; the same panel column carries both shapes) | **Densities are normalised per class**, so the ~1:1000 class imbalance the AP values imply is invisible — the actives curve looks comparable in mass to the inactives curve | CC-BY 4.0, p45 |
| 14 | 45 | Per-assay predicted vs measured affinity on the 8 blinded Recursion assays | scatter | `PLOT \| facet: assay (8, labelled "Assay id 1"–"Assay id 8", targets undisclosed) \| vary: measured affinity, −15 to −4 kcal/mol (continuous) \| series: none (1) \| measure: predicted affinity (kcal/mol) \| mark: point (+ ±1, ±2 kcal/mol guides) \| n: 1 per mark; "hundreds of compounds" per assay (p43), exact n NOT REPORTED` | 8 panels, 2 × 4 | **Targets are not identified at all** and per-panel n is not given, so the R = 0.165–0.634 spread cannot be attributed to protein class or to assay size — which is precisely the open question the authors raise at p12 | CC-BY 4.0, p45 |
| 15 | 46 | Boltz-2 score distributions for the five TYK2 compound streams, before ABFE | violin | `PLOT \| facet: score type (2: predicted binding probability, predicted binding affinity kcal/mol) \| vary: compound stream (5: random, public binders, HLL, Kinase, SynFlowNet) \| series: compound stream (5) \| measure: Boltz-2 predicted binding probability and predicted affinity \| mark: violin with overlaid points and median/whisker bars \| n: 10 per violin, 50 per panel` | 2 panels | **Violins over n = 10**; the streams were filtered to a score threshold of 0.5 and an ensemble-MPO threshold of 0.9 before plotting (Table 17, p46), so three of the five distributions are truncated by construction and the figure shows selection, not discrimination | CC-BY 4.0, p46 |
| 16 | 47 | Binding poses of the top-2 ABFE-ranked ligands from each stream in TYK2 | structure render | `RENDER \| facet: stream (5: random, HLL, Kinase, SynFlowNet, known ligands) × rank (2: top-2 by ABFE) \| views: 2 (global view, zoom on pocket) \| overlay: NOT REPORTED predictions on NOT REPORTED reference(s) \| axis: none` | 20 renders (5 rows × 2 ligands × 2 views) | **No reference structure is overlaid and no pose-quality number is attached to any render** — the poses are Boltz-2's own co-folds, so the figure shows what the model believes, not what is true; the caption's own warning is about optimisation objective, not pose validity | CC-BY 4.0, p47 |
| 17-21 | 48-49 | 2D chemical structures of the 10 compounds in each of the five ABFE-tested streams | schematic | `SCHEMATIC \| 2D molecular structure grids, one per screening stream (random, HLL, Kinase, SynFlowNet, public TYK2 binders) \| no data` | 5 figures × 10 molecules | No score or ABFE value is printed on any structure, so the panels cannot be read against Figs 8 and 15 | CC-BY 4.0, p48–49 |
| 22 | 50 | Scaffold-similarity matrix, generated compounds vs known TYK2 binders | heatmap | `MATRIX \| rows: SynFlowNet sample (10) \| cols: TYK2 binder from KLIFS (47) \| value: Murcko-scaffold Morgan-fingerprint Tanimoto similarity, 0.0–1.0 \| facet: none (1)` | 1 matrix, 470 cells | Colour scale runs 0.0–1.0 while the observed maximum is 0.396, so the entire matrix renders as low-similarity blue — visually persuasive but it compresses all the real variation into the bottom 40% of the scale | CC-BY 4.0, p50 |
| 23 | 50 | Each generated ligand beside its nearest KLIFS TYK2 binder | schematic | `SCHEMATIC \| paired 2D molecular structures: 10 SynFlowNet compounds each next to their most similar KLIFS TYK2 binder \| no data` | 10 pairs | Per-pair Tanimoto values are not printed on the pairs, so the reader cannot tell which pair is the 0.396 maximum | CC-BY 4.0, p50 |

**License, once, for the whole document:** page header on **every page, p1–55**: "It is made
available under a **CC-BY 4.0 International license**." **No ND clause** — redrawing and
modification are permitted with attribution. Code and weights are separately released "under a
permissive open license" (p1, p12); the specific licence name is **NOT REPORTED** in the PDF.

---

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), single-paper extraction
- **schema_version**: v3
- **confidence**: **high** for sections A, B, D, E and for the cutoff, training composition,
  steering and sampling-default questions — all of these are stated in plain prose with page
  anchors, and the appendices are unusually explicit. **Medium** for parts of section F: eleven of
  the twenty-three figures have captions too thin to fill `data_shape` (they state only "error bars
  indicate 95% confidence intervals" or similar), and four pages were rendered to recover panel
  structure. **Medium** for `states_generated`, because the paper's own framing ("extends
  predictions from static complexes to dynamic ensembles", p1) is broader than what it demonstrates
  (RMSF-scale local fluctuation on 40+40 held-out MD complexes), and the honest answer needed both
  halves of the dual value.
  What was hard to read: the `pdftotext` layout output shatters every bar chart into free-floating
  numeric labels, so Figures 1, 3, 4, 5, 7, 11 and 15 could not be characterised from text alone.
  Pages **2, 7, 11, 41 and 46** were rendered at 150 dpi and read as images, then deleted.

- **unresolved**:
  1. **Tags I needed and could not use, in the order they hurt most:**
     - **A tag for inference-time steering of a diffusion trajectory by a differentiable
       potential.** `latent-steering` is defined as "any inference-time intervention on an internal
       tensor — pair representation, trunk embedding, distogram head, conditioning embedding",
       which covers Boltz-2's method conditioning and its contact/pocket pairwise-feature
       conditioning, so I applied it. But it does **not** cover Boltz-steering proper, which adds a
       potential gradient to the *coordinates* during reverse diffusion. That is the single most
       corpus-relevant mechanism in this paper and the vocabulary has no name for it. Suggested:
       `diffusion-steering` or `potential-steering`.
     - **A protocol tag for "templates available but switched off, MSA on".** The Protocol group
       offers only `no-template-no-msa` and `templates-on`. Boltz-2's evaluations use full MSAs and
       **no** templates (p35), which is neither. I applied neither tag. Suggested:
       `templates-off-msa-on`, or make `templates-on` a three-valued protocol field.
     - **`md-emulator` is defined so that it excludes this paper, and I think that is a defect.**
       The definition says it is "a generative model trained on MD trajectories, which is neither
       `md` nor `cofolding`". Boltz-2 *is* a cofolding model *and* is trained on MD trajectories
       (MISATO, ATLAS, mdCATH; MISATO carries a 0.230 sampling weight, the third-largest source)
       *and* is benchmarked head-to-head against AlphaFlow and BioEmu on RMSF. A reverse lookup for
       "which papers trained on MD trajectories" will miss it. I did not tag it, per the "never
       invent, never stretch" rule. Recommend the definition be relaxed to "trained on MD
       trajectories" with the cofolding exclusion dropped.
     - **No Control-group tag fits.** The Control vocabulary (`directed-state`, `partner-driven`,
       `ligand-driven`, `peptide-driven`, `g-protein-mimetic`, `nanobody`, `apo-sampling`,
       `seed-only`) is entirely about *state* handles. Boltz-2's handles direct **geometry and
       experimental modality**, not state: a method one-hot, a distance restraint, a template
       enforcement radius. I left the Control group empty rather than mislabel. Suggested:
       `restraint-driven` and `method-conditioned`.
  2. **`kinase` tag applied with a caveat.** The paper studies protein kinases heavily (TYK2, CDK2,
     JNK1, P38, ABL1) but studies them as **affinity** targets, never as conformational-state
     systems. A reverse lookup for "kinase conformational states" will return this paper as a false
     positive. The v3 note scoping `kinase` to protein kinases addresses a different failure mode
     (adenylate kinase) and does not help here. Flagging rather than silently dropping the tag.
  3. **`prospective` tagged although the field says "partial".** The tag vocabulary is binary and
     the field is not. I tagged it because one genuinely forward-looking arm exists (the TYK2
     screen), but the tag alone overstates: that arm has no experimental readout and its target was
     chosen for oracle convenience. Consider a `partially-prospective` tag or dropping the tag in
     favour of the field.
  4. **What pLDDT and pTM are trained to predict is genuinely absent from this paper.** The
     confidence section (p25) names only PDE and PAE logit heads; ipTM, iPDE and PDE are used
     throughout as scores. pLDDT is never mentioned; pTM is never mentioned. "Global lDDT" appears
     once, as an AFDB filter (p18), which is AlphaFold's confidence, not Boltz's. I recorded
     `NOT REPORTED` rather than importing the AlphaFold3 definitions the architecture is said to
     resemble. **If a downstream claim in the manuscript needs Boltz-2's pLDDT semantics, this PDF
     is not the source for it.**
  5. **Affinity training data has no stated date cutoff.** Only database versions (ChEMBL v34,
     PubChem 1.8.1, BindingDB unversioned; p19). Affinity leakage is controlled by 90% sequence
     identity, not by time. Anyone constructing a post-cutoff affinity set against Boltz-2 has no
     date to work from and must use the 2023-06-01 *structural* cutoff, which does not govern the
     affinity heads.
  6. **The Boltz-steering hyperparameter tuning set is not identified.** p23 says the Boltz-1x
     potentials were adopted "with tuned hyperparameters" and never says what they were tuned
     against. Under v3 route 4 this is potentially leakage; it is unfalsifiable from this PDF.
  7. **Figure 6's middle panel is labelled "FEP+ OpenFE 8 internal targets"** while the text (p9)
     and Table 11 (p42) describe the OpenFE subset as 876 hit-to-lead measurements. Either the
     panel label or the text is wrong; I recorded both and did not reconcile them.
  8. **The "1000× faster" claim's denominator shifts.** p1 abstract says "at least 1000× more
     computationally efficient than FEP"; Table 12 (p42) gives Boltz-2 at 20 GPU sec vs OpenFE at
     6–12 GPU hours (≈1000–2000×) and ABFE at >20 GPU hours (≈3600×), while FEP+ has no time entry
     at all ("-"), so the comparison against the *strongest* baseline is unquantified.
  9. **v3 ambiguity, reported bluntly.** The panel-splitting rule reads "Split when `mark` or
     `measure` differs. Do not split when only `facet` differs", but the very next sentence says
     "four box panels showing four metrics under the same faceting are one row with a compound
     measure". Those contradict: four metrics *are* four measures. I resolved it by treating
     *metric-as-facet under one mark* as a single row with a compound measure (so Figs 3 and 5 are
     one row each), and splitting only where the independent axis or the mark also changes (4A/4B,
     7A/7B, 8A/8B, 13A/13B). The rule should say so explicitly, because the opposite reading would
     turn Figure 3 into twelve rows.
  10. **v3 ambiguity: `hides` vs `metric_saturation` for a *shared* axis at different scales.**
      Figure 5 puts five metric groups on one axes where four are scaled 0.50–0.90 and one 0.00–0.35.
      That is neither a break (rule 9's case) nor numeric saturation. I put it in `hides`. A rule
      for "shared axis, incomparable scales" would help.
  11. **v3 ambiguity: `n:` for a filtered distribution.** The `1 of 5 (pLDDT-selected)` form covers
      a representative drawn from many. Figure 15's violins show all 10 members of a set that was
      *itself* selected by a score threshold — the distribution is truncated by construction, not
      subsampled. I recorded `n: 10 per violin` and put the truncation in `hides`, but a form like
      `10 of 117,199 (score-threshold-selected)` would be more joinable.
  12. **`si_in_scope` has no vocabulary for "SI present but the paper self-declares incomplete".**
      p40 states outright that template/contact/pocket evaluations are missing and will be added
      later. That is a different gap from "SI NOT HELD" and I described it in prose.

- **why_it_matters**: *(left empty — the user's call)*

---

## Tags

`general-protein` `kinase` `cofolding` `latent-steering` `ensemble` `single-state`
`binary-predicate` `continuous-metric` `saturating-metric` `anti-memorization`
`design-level-oracle` `prospective` `confidence-as-discriminator` `multi-backbone` `unpowered`
`orthosteric` `preprint` `background` `precedent` `comparator-numbers`

Justifications for the non-obvious ones:
- **`latent-steering`** — applied for **method conditioning** (an experimental-method one-hot fed
  into the single token representation at inference, p24) and **contact/pocket conditioning**
  (one-hot contact type + Fourier-embedded distance fed as *pairwise* features, p25). Both are
  inference-time interventions on conditioning/pair representations, which is exactly the
  definition. It is **not** applied for Boltz-steering itself — see `unresolved` item 1.
- **`ensemble` + `single-state`** — the paired form the v3 vocabulary explicitly sanctions.
  MD-conditioned sampling produces 100-member ensembles; the shipped default collapses to top-1
  of 5 by ipTM.
- **`saturating-metric`** — "Perc. within 2 kcal/mol" reaches 1.00 for two methods on the 4-target
  subset (Table 12, p42); numeric, not an axis artefact.
- **`design-level-oracle`, not `oracle-leak`** — routes 1, 2, 3 and 6 are clean. The findings are
  target selection conditioned on the validator's known performance (p10) and training-set
  upsampling toward a benchmark family the paper then reports on (p18 → p7). Nothing was fed to
  the model that contained the answer, so the weaker label is the correct one.
- **`unpowered`** — attaches specifically to the headline FEP-comparison claim, which is a mean
  over **4 assays** (Fig 6 left, Table 12, p42), and to the prospective screen, whose arms are
  N = 10 each. The anti-memorization control (Fig 10, N = 289/288/108/182) is *not* unpowered and
  the tag should not be read as covering it.
- **`confidence-as-discriminator`** — ipTM is used to rank samples, to admit training assays
  (>0.75) and to admit distillation examples (≥0.7/0.8/0.85/0.9); it is also run as an explicit
  affinity baseline where it fails (R = −0.07 to 0.12). Tagged for the usage; the validation is
  negative and is recorded as such.
- **`orthosteric`** — the TYK2 campaign targets the ATP site ("a well-established motif in
  orthosteric kinase inhibitor design", p49) and the limitations distinguish orthosteric from
  allosteric modulators (p12). No allosteric-site work; `allosteric-site` and `allosteric-failure`
  do not apply.
- **Not tagged, deliberately:** `experimental-validation` (ABFE is simulation, not a lab assay —
  the paper is explicit that it validates "in the absence of experimental data", p10);
  `md` (Boltz-2 runs no simulations; it consumes trajectories others ran); `md-emulator` (excluded
  by its own definition, see `unresolved` item 3); `templates-on` / `no-template-no-msa` (neither
  is true, see `unresolved` item 1); `oracle-leak` (see above); `rmsd-only` and `visual-metric`
  (the metric suite is broad and quantitative); `threat` and `negative-result`;
  `figure-exemplar` (the figures are workmanlike and several actively obscure their own results).
