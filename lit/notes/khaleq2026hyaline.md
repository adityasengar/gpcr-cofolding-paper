# khaleq2026hyaline

> Extraction note, SCHEMA.md v3. Quotes are verbatim; the PDF text layer renders
> em-dashes as a stray comma-space (` ,`), and those have been restored to ` — `
> where they occur inside a quote. No other alteration.
>
> **This is a classifier, not a structure generator.** Several section C fields
> presuppose a generative method and are marked `NOT APPLICABLE` with a reason
> rather than forced into a generative reading.

---

## A. Identity

| Field | Value |
|---|---|
| `citekey` | `khaleq2026hyaline` |
| `doi` | https://doi.org/10.64898/2026.01.05.697778 (bioRxiv) (p1) |
| `year` | 2026 — "this version posted January 5, 2026" (p1). Journal-template header on p1 reads "(2025), 1–15", which is a template artifact, not a publication year. |
| `venue` | bioRxiv preprint, "not certified by peer review" (p1). Tagged `preprint`. |
| `title` | HYALINE: Geometric Deep Learning for Accurate Prediction of G Protein-Coupled Receptor Activation States from Structure |
| `authors` | A. Khaleq, H. Kabodha (Varosync). Corresponding address is a company partnerships mailbox: "Author for correspondence: Varosync, Email: partnerships@varosync.com" (p1). Competing interests: "The research presented here was conducted as part of Varosync's research and development activities" (p13). |

## B. Scope

| Field | Value |
|---|---|
| `system` | GPCR. Classes A, B1, C, F represented (Table 2, p7). |
| `n_targets` | 1,590 experimental structures total; 1,312 train / 278 temporal test (p4, p12). Per class: A 1,263; B1 145; C 94; F 34 (Table 2, p7). **Number of distinct receptors is NOT REPORTED** — the paper counts structures, never receptors, which is the number that would bear on memorization. Note Table 2's class rows sum to 1,536, not the stated 1,590 overall (54 unaccounted; Fig. 9a legend carries an "Other (n=54)" group, p10). |
| `method_class` | `other` — supervised binary structure classifier / state-assessment metric. None of the schema's listed classes (co-folding, MSA-subsampling, MSA-state-filtering, template-biasing, MD, enhanced sampling, clustering, benchmark-only) applies. The method consumes a 3D structure and emits a state probability; it predicts no coordinates. |
| `backbones` | NOT APPLICABLE — no structure-prediction backbone. The only pretrained model used is **ESM3-Open (`esm3-open-2024-03`)**, a 15-billion-parameter sequence transformer, used purely as a per-residue embedding source: "per-residue representations by computing the mean of hidden representations across all 48 transformer layers, yielding a 1,536-dimensional embedding per residue" (p12). AlphaFold 3, Boltz-1, Chai-1, Protenix and HelixFold3 are named only as the *targets* of a proposed downstream application (p10), never run. |
| `templates` | NOT APPLICABLE — no template machinery; the experimental structure is the input. |
| `msa_handling` | **None — explicitly MSA-free.** "Unlike AlphaFold and related structure prediction methods, this approach does not require multiple sequence alignments (MSAs), eliminating the computationally expensive and time-consuming MSA generation step" (p12). |

## C. Conformational core

### `states_generated`

**NOT APPLICABLE — nothing is generated; the model classifies.**

The output is a single scalar. "Global attention pooling aggregates per-residue features into a graph-level representation for final binary classification" (Fig. 2 caption, p3); the readout head is "Linear 160 → 1 / Sigmoid σ / logits → probability / Activation Probability p ∈ [0,1]" (Fig. 11, p14). The EGNN layers do update coordinates internally — `x'_i = x_i + C Σ (x_i − x_j) φ_x(m_ij)` (Eq. 3, p12) — but those refined coordinates are never emitted; only the scalar features reach the classifier, and the paper deposits no predicted structure anywhere.

The model does implicitly hold **two** state classes (active / inactive), and structures are excluded from the corpus when they do not fall cleanly into one: "Structures with partial agonists or ambiguous annotations were excluded to ensure clean training labels" (p12).

### `structural_priors_used`

Substantial, and all at design time. None of the following is a defect; each is recorded so that anyone reusing HYALINE as a scoring function inherits them knowingly.

1. **GPCRdb activation-state annotations are the ground truth.** "We retrieved all GPCR structures from the Protein Data Bank (PDB) as of December 2024, cross-referenced with the GPCRdb database (Kooistra et al. 2021) for receptor identification and activation state annotations" (p12); "Activation state labels were assigned based on GPCRdb annotations, structural criteria, and ligand binding status" (p12). A structure was only retained if it "had unambiguous activation state annotation in GPCRdb" (p12). **A classifier trained on GPCRdb state labels reproduces GPCRdb's operational definition of "active"; using it to score predicted structures inherits that definition and its exclusions.** This is a design-time prior, not a methodological fault — but it is the prior that matters most for our use.
2. **The label rule is itself partly pharmacological, not geometric.** "Active structures included: (1) G protein-coupled or G protein-mimetic nanobody-bound structures; (2) arrestin-coupled structures; (3) full agonist-bound structures with conformational criteria indicating activation. Inactive structures included: (1) apo structures; (2) antagonist-bound structures; (3) inverse agonist-bound structures" (p12). So "active" is defined largely by bound partner/ligand identity, and the model is asked to recover that from geometry alone. The authors observe the resulting mismatch in their own error analysis (see route 6 below).
3. **Three literature-derived microswitch motifs are hard-encoded as attention-bias targets.** "Based on extensive structural studies of GPCR activation (Weis and Kobilka 2018; Hauser et al. 2021), we identified three conserved motifs that undergo characteristic conformational changes upon activation: the DRY motif (Asp-Arg-Tyr, Ballesteros-Weinstein positions 3.49–3.51) at the cytoplasmic end of TM3, the NPxxY motif (Asn-Pro-x-x-Tyr, positions 7.49–7.53) in TM7, and the CWxP motif (Cys-Trp-x-Pro, positions 6.47–6.50) in TM6" (p3). Motif membership is assigned by sequence pattern matching against Ballesteros-Weinstein numbering (p12).
4. **42 hand-crafted inter-residue distances** "based on prior structural studies of activation" (p5) — used only to build the random-forest comparison baseline, not in HYALINE itself.
5. **β2AR 2RH1 (inactive) / 3SN6 (active)** used as the canonical reference pair for illustration and for the ionic-lock narrative (Fig. 1 p1, Fig. 8 p9).
6. **Quality/coverage filters presupposing a canonical GPCR fold:** "(1) contained at least 80% of the canonical transmembrane domain resolved; (2) had resolution ≤ 4.0 Å for X-ray structures or FSC ≤ 4.5 Å for cryo-EM structures" (p12).

### `oracle_leakage`

Seven routes, each answered separately. For a supervised classifier the framing shifts: labelled reference structures are the *task*, not a contaminant. What is recorded here is where knowledge of the answer entered anywhere other than as legitimate supervision.

1. **Structures used as input or template.** Present *by construction* — the deposited experimental structure is the model input: "predict GPCR activation states directly from 3D coordinates" (p1); "For each structure, we extracted Cα coordinates and amino acid sequences using BioPython" (p12). This is the intended interface, not leakage. Consequence worth flagging for reuse: every training and test structure is an experimental one, so nothing in this paper establishes behaviour on predicted coordinates (the authors say so themselves, p11).
2. **State annotations from a curated database (GPCRdb).** **PRESENT, as the supervision target.** "Activation state labels were assigned based on GPCRdb annotations" (p12). No template or alignment is biased by these annotations — there are no templates and no alignments. The dependency is on the label semantics, recorded fully under `structural_priors_used`. Recording it as an honest dependency rather than as pipeline leakage.
3. **Cluster labels derived from known states.** **NONE FOUND.** The only clustering in the pipeline is sequence-identity clustering for fold construction, which is state-agnostic: "Cross-validation used 30% sequence identity clustering via MMseqs2 to prevent data leakage from homologous receptors" (p13). t-SNE (Fig. 6, p8) and UMAP (Fig. 9a p10, Fig. 10a p11) are used for post-hoc visualisation only, coloured by known state, and no label is derived from them.
4. **Hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.** **PARTIAL, but confined to the training set's CV folds.** All ablations and the depth choice were evaluated on training-set cross-validation, not on the temporal test set: "All ablations evaluated via 5-fold cross-validation with cluster-based splitting at 30% sequence identity to prevent data leakage from homologous receptors" (Fig. 7 caption, p8). Early stopping is on a validation loss: "Training proceeded for 30 epochs with early stopping based on validation loss (patience 5 epochs)" (p13). The depth was selected by comparing against evaluation outcomes: "Increasing to 7 layers provided no additional benefit and slightly increased overfitting, suggesting that 5 layers represent an optimal trade-off for this application" (p8) — a range tuned on evaluation data, though on CV folds rather than on the held-out temporal set. The authors assert the temporal set was untouched: "This temporal split ensures that the test set contains structures that were not only unseen during training but were also unavailable during model development and hyperparameter tuning" (p4). Full hyperparameter list is given (Table 3, p14), which is more than most.
5. **Success defined post hoc by RMSD or TM to a structure they had.** **NONE FOUND.** Success is label agreement, scored by AuROC / accuracy / sensitivity / specificity / precision / F1 / MCC (p13). No RMSD or TM-score is used as a success criterion anywhere.
6. **Best/worst labels assigned against a held reference.** **PRESENT in the error analysis.** All 39 misclassifications are re-adjudicated post hoc against reference geometry, and the errors are reassigned to the ground truth rather than to the model: "Systematic examination of the 39 misclassified structures revealed that errors predominantly reflect genuine biological ambiguity or limitations in ground-truth annotations rather than model failures" (p9). The adjudication uses reference-relative measurements — Table 4 (p14) reports, per misclassified structure, an "Ionic lock distance: R3.50–E6.30 (or K3.46–TM6 for Class C)" and a "TM6 displacement measured relative to inactive reference". The strongest instance: "HYALINE correctly identifies these as geometrically closer to the inactive state, even though they are annotated as active based on ligand pharmacology" (p9), i.e. 15 of 39 errors (38%) are relabelled as correct against a geometric criterion the training labels did not use. Also: "may represent annotation errors in GPCRdb" for a further 5 (p9). This does not contaminate training, but it means the reported accuracy is a floor the authors argue is pessimistic — using an argument that would not survive if applied symmetrically to the successes.
7. **Design-level oracle use.** **PRESENT, and weaker than pipeline leakage — label it as design-level.** The evaluation corpus was constructed to contain only structures whose state was already confidently known, with the hard cases removed before either training or testing: "Structures with partial agonists or ambiguous annotations were excluded to ensure clean training labels" (p12), and retention required "unambiguous activation state annotation in GPCRdb" (p12). The headline AuROC is therefore measured on the subset of structural space where the answer was never in doubt — which is precisely the subset that does not include an AlphaFold 3 model of unknown state. Separately, the stated flagship application is asserted, not tested: "By applying HYALINE to AlphaFold 3-generated GPCR models, researchers can obtain rapid, quantitative estimates of whether the predicted structure represents an active, inactive, or intermediate conformation" (p11) — no such experiment is run.

### `prospective`

**no.** Every structure in the study was already deposited (PDB as of December 2024) and already state-annotated in GPCRdb before the model saw it. The temporal split is a retrospective simulation of prospectivity: the split is by deposition date, but both halves were in hand at analysis time (paper posted January 2026, cutoff December 2024). The one genuinely prospective use — scoring predicted structures — is proposed and explicitly deferred (p11).

### `state_metric`

**binary predicate.** (Single-valued; not dual — nothing here is called by eye and no RMSD is used as a success criterion.)

**What the model outputs.** A single scalar activation probability per structure. Readout: five EGNN layers → Jumping Knowledge concatenation of all six representations ("Concatenates representations from all 6 layers (init + 5 EGNN layers) ... [h(0)‖h(1)‖···‖h(5)] = 320 × 6 = 1920 dims", Fig. 11 p14) → concatenated with the mean-pooled final-layer 320-d global state → 2240 → MLP `2240 → 320 → 160 → 1` → "Sigmoid σ / logits → probability / Activation Probability p ∈ [0,1]" (Fig. 11 p14; also Fig. 2 p3). Trained with "binary cross-entropy loss with class weighting to address class imbalance (weights: active 0.38, inactive 1.0)" (p13).

**Decision boundary.** **Never stated explicitly — the threshold is NOT REPORTED.** It is recoverable as 0.5 only by inference: the headline metric is AuROC, which is threshold-free, but accuracy/sensitivity/specificity in Table 1 require a threshold, and the error analysis places borderline cases around 0.5 — "The majority of Class C misclassifications involved structures near the decision boundary (mean confidence: 0.58)" (p9), with Table 4's misclassified structures carrying confidences 0.52–0.71 (p14). The "high certainty" band is defined as "confidence scores above 0.9 or below 0.1" (p8). **Record this as a real gap: a paper offered as a state-assessment metric never writes down its operating point.**

**Geometric features used.** Cα-only, distance-based, rotation/translation invariant by construction.
- Graph: "vertices correspond to residues and edges connect residue pairs with Cα–Cα distance ≤ 10 Å ... typical GPCR graphs contain 15–20 edges per node" (p12).
- Edge features: 96 Gaussian radial basis functions, `φ_k(d) = exp(−(d − µ_k)²/2σ²)`, "where d is the Cα–Cα distance, µ_k are 96 uniformly spaced centers from 2 to 20 Å, and σ = 0.3 Å" (p12).
- Node features: ESM3 1,536-d embedding + 64-d sinusoidal positional encoding = 1,600-d (p12), projected 1536→320 (Fig. 2, p3).
- Five E(n)-equivariant message-passing layers, hidden dim 320, SiLU: "each message-passing layer propagates information approximately 10 Å through the structure; five layers thus provide a receptive field of roughly 50 Å, comfortably spanning the entire transmembrane bundle (∼40 Å)" (p3).
- Coordinates "centered at the geometric centroid of Cα atoms but not otherwise normalized, as the equivariant architecture is invariant to rotations and translations" (p12).
- **No side-chain atoms.** The classifier sees Cα only, which is worth noting against the paper's own ionic-lock narrative (Fig. 8, p9, discusses the Arg3.50 guanidinium–Glu6.30 salt bridge, a side-chain contact the model cannot observe directly).

**Motif-specific attention: YES, explicit.** "Residues belonging to these motifs receive enhanced attention through a learned bias term (b_motif = 0.5), implemented as an additive term in the pre-softmax attention logits" (p4); "Residues identified as belonging to motifs received an additive attention bias b_motif = 0.5 in the first attention layer" (p12). Motifs detected by regex on sequence: "The DRY motif was detected as D[R/K]Y in TM3 (Ballesteros-Weinstein positions 3.49–3.51). The NPxxY motif was detected as NP[A-Z][A-Z]Y in TM7 (positions 7.49–7.53). The CWxP motif was detected as C[W/F]xP in TM6 (positions 6.47–6.50)" (p12). Fig. 10b (p11) shows *trained* per-motif bias weights of DRY 0.80, NPxxY 0.59, CWxP 0.40, None 0.00, and a fifth category **PIF 0.99** that is described nowhere in the Methods motif-detection section — recorded under `unresolved`.

**Explicit structural descriptor as the decision rule: NO.** The classification is entirely learned; no interpretable geometric quantity (ionic-lock distance, TM6 displacement) is computed or thresholded to make the call. Such quantities appear only as post-hoc interpretation: the ionic lock "R3.50–E6.30 salt bridge distance: ∼3–4 Å in inactive states, >10 Å in active states" (p7) and "a strong correlation between attention weights and the magnitude of TM6 outward displacement across all structures (r = 0.78, p < 0.001)" (p6). The biasing "is deliberately 'soft' — the model remains free to discover additional relevant features from data" (p4), and ablating it costs almost nothing (Fig. 7, p8).

### `metric_saturation`

**YES — numeric ceiling, in every arm.**
- AuROC is at 0.995 (CV) and 0.991 (temporal test) out of a maximum of 1.000 (Table 1, p5), i.e. the reported headline sits 0.005–0.009 from the ceiling.
- Every per-class AuROC is ≥ 0.956 (Table 2, p7).
- Every ablation except the ESM3 removal lands between 0.971 and 0.987 (Fig. 7, p8) — a 0.016 spread compressed against the ceiling, so the four architectural ablations are separated by differences smaller than the CV standard error on the full model (±0.003 × several folds) and no significance test is given for three of the four.
- The model's own confidence output is bimodal against its bounds: "The vast majority of predictions (94.3%) had confidence scores above 0.9 or below 0.1, indicating high certainty. Intermediate confidence scores (0.3–0.7) were rare (2.8% of predictions)" (p8). Visible directly in Fig. 4b (p5), where the correct-prediction cloud is pinned along confidence = 1.0.
- Consequence for reuse: a metric this saturated on curated experimental structures carries no information about its dynamic range on ambiguous or predicted structures — which is the regime we would need it in.

Axis-truncation issues (Fig. 4a y-axis begins at 40%) are recorded in the figure table's `hides`, per the v3 rule, not here.

### `directional_control`

**NOT APPLICABLE — no generative handle exists.** The method has no mechanism to be instructed toward a state because it produces no structure. The only "handle" in the architecture is the motif attention bias (b_motif = 0.5), which steers *where the classifier looks*, not what conformation is produced.

The paper does gesture at a future control-like use — "The attention mechanism thus provides a learned 'activation sensor' that could be applied to analyze molecular dynamics trajectories, identify activation events in simulations, or assess the conformational state of computationally predicted structures" (p6) — but that is scoring, not direction, and is not implemented.

### `anti_memorization_design`

**Two mechanisms, of unequal strength.**

1. **Temporal split (the headline arm).** "HYALINE was trained exclusively on structures deposited in the Protein Data Bank before January 2023 (n = 1,312) and evaluated on structures deposited between January 2023 and December 2024 (n = 278)" (p4); restated in Methods: "structures were divided based on PDB deposition date: training set (deposited before January 1, 2023; n = 1,312) and temporal test set (deposited January 2023 – December 2024; n = 278). This split ensures that test structures were unavailable during model development" (p12). **Cutoff definition: PDB deposition date, 1 January 2023.**
2. **Sequence-identity clustering — but only inside cross-validation.** "Cross-validation used 30% sequence identity clustering via MMseqs2 to prevent data leakage from homologous receptors" (p13); Fig. 7 caption confirms the scope: "All ablations evaluated via 5-fold cross-validation with cluster-based splitting at 30% sequence identity to prevent data leakage from homologous receptors" (p8).

**The critical gap: the two are never combined.** No sequence- or family-level holdout is applied to the temporal test set, and no receptor-level holdout is reported anywhere. The paper never states that any receptor appears in only one of train/test, and its own framing concedes the split does not guarantee it: "it includes structures of receptors that **may have been** poorly represented or entirely absent from the training set" (p4, emphasis added) — a hedge, not a claim. Given the paper's own observation that "the structural database is dominated by a relatively small number of well-studied receptors (e.g., β2-adrenergic receptor, adenosine A2A receptor, muscarinic M2 receptor)" (p4), a 2023–2024 deposition slice of GPCR structures will overwhelmingly re-sample receptors already in the pre-2023 training set. **For reuse this is the single most important caveat: the 0.991 is a same-receptor, later-deposition number, not a held-out-receptor number.**

### `anti_memorization_control`

**RUN — for the temporal arm; NONE RUN for a sequence- or family-held-out arm.**

- The temporal arm was actually executed and analysed, not merely constructed: AuROC 0.991 (95% CI 0.984–0.997), accuracy 96.4%, sensitivity 97.8%, specificity 92.1% (p4–p5, Table 1). It was also stratified by class (Table 2, p7) and by resolution (Fig. 4b, p5), and baselines were re-scored on the same set (p5). n = 278 — **not `UNPOWERED`.**
- The 30% sequence-identity cluster split was run, but only as the CV protocol behind the ablation table (p8, p13) — no AuROC for the *temporal test set under a sequence-identity holdout* is reported, and no arm anywhere holds out a receptor or a family.
- **No arm establishes whether any receptor appears in both train and test.** The count of distinct receptors is not given, the overlap is not quantified, and there is no per-receptor or leave-one-receptor-out breakdown. Class F, at n = 34, would be the natural family-holdout test and is instead reported as a within-corpus stratum (Table 2, p7), with the authors attributing its wider CI to sample size: "The wider confidence interval reflects the limited structural data rather than fundamental model limitations" (p7).

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| Temporal test arm, structures deposited 2023–2024 (n = 278), model trained pre-2023 only | Memorization of the *specific deposited structures* seen in training (does **not** rule out receptor-level memorization) | p4, p12 |
| 5-fold CV with MMseqs2 cluster-based split at 30% sequence identity | Homolog leakage between CV folds (applied to CV / ablations only, not to the temporal arm) | p8 (Fig. 7 caption), p13 |
| ESM3 embeddings + linear classifier (sequence-only), AuROC 0.852 | That evolutionary sequence information alone accounts for the result | p5 |
| ESM3 + MLP (sequence-only), AuROC 0.867 (caption p5) / 0.807 (Fig. 7 p8) — figures disagree | Same, with a nonlinear head; rules out that the gap is head capacity | p5, p8 |
| Random forest on 42 hand-crafted inter-residue distances, AuROC 0.891 | That expert-chosen distance features already suffice; anchors the learned representation against a hand-crafted geometric baseline | p5 |
| Random baseline, AuROC 0.500 | Chance floor | p8 (Fig. 7) |
| One-hot amino-acid encoding replacing ESM3, AuROC 0.823 | That ESM3 pretraining is decorative | p7 |
| Motif attention bias removed, AuROC 0.987 | That the injected motif prior is doing the classification (it is not — Δ ≈ 0.008) | p8 (Fig. 7) |
| RBF edge features removed, AuROC 0.982 | That explicit pairwise distance encoding is redundant with message passing | p8 (Fig. 7), p7 |
| Attention pooling removed, AuROC 0.978 | That the pooling choice is inert | p8 (Fig. 7) |
| Multi-scale edges removed, AuROC 0.971 | That the multi-scale edge construction is inert | p8 (Fig. 7) |
| Message-passing depth 3 vs 5 layers, AuROC 0.981 vs 0.995; 7 layers tested and rejected | That receptive field is unrelated to performance; also the depth-selection sweep | p8 |
| Attention analysis on the **unbiased** (no motif-bias) model — DRY enrichment 2.4× vs 3.2× | That the observed motif attention enrichment is an artifact of the injected bias | p7 |
| Permutation test on attention enrichment, 10,000 permutations, p < 0.001 | Chance-level attention enrichment at DRY/NPxxY/CWxP | p6, p13 |
| Resolution stratification: r = −0.119 across 1.5–4.0 Å; <2.5 Å 97.7% vs ≥3.0 Å 97.2% | That performance is an artifact of high-resolution structural detail | p5 (Fig. 4b) |
| Per-class stratification (A / B1 / C / F, Table 2) | That performance is carried entirely by over-represented Class A | p7 |
| Calibration analysis on the temporal test set (asserted, no plot shown) | That the probability output is uninterpretable as a confidence | p5 |
| DeLong's test for AuROC comparison between methods | That the method-vs-baseline gaps are within noise | p13 |
| Coordinate-noise augmentation, Gaussian σ = 0.1 Å; **no rotational augmentation used** | That equivariance is being learned from augmentation rather than built in | p13 |

**Not run:** no decoy arm, no shuffled-label arm, no arm on computationally predicted (AlphaFold 3 / Boltz / Chai) structures, no receptor-held-out arm, no arm on the excluded ambiguous / partial-agonist structures.

### `confidence_as_discriminator`

**Not in the pLDDT/pTM sense — no structure-prediction confidence is used anywhere.** The relevant confidence is the model's *own* sigmoid output, which is simultaneously the prediction and the confidence, and which is used to triage cases: "The vast majority of predictions (94.3%) had confidence scores above 0.9 or below 0.1 ... Intermediate confidence scores (0.3–0.7) were rare (2.8% of predictions) and were associated with structures representing transitional or ambiguous conformational states" (p8), and low-confidence cases are read as biology: "HYALINE's intermediate confidence scores for these structures are arguably more informative than binary annotations, as they reflect the underlying conformational heterogeneity" (p10).

**Was that use validated?** Asserted, not shown: "calibration analysis confirmed that predicted probabilities remained well-calibrated on the temporal test set, enabling reliable confidence assessment for downstream applications where prediction uncertainty matters" (p5). **No calibration curve, no Brier score, no expected-calibration-error figure appears in the paper.** The claim that intermediate confidence marks genuine intermediates is supported only by the eight hand-picked structures of Table 4 (p14), which is an illustration rather than a test.

## D. Claims

### `central_conclusion`

A Cα-graph E(n)-equivariant GNN with ESM3 per-residue embeddings, five message-passing layers and a soft motif-attention prior classifies deposited GPCR structures as active or inactive at AuROC 0.995 (5-fold CV on 1,312 pre-2023 structures) and 0.991 on a temporally held-out set of 278 structures deposited 2023–2024, substantially above sequence-only baselines (0.852–0.867) and a hand-crafted-distance random forest (0.891), and holds up across classes A, B1, C and F. The authors read this as evidence that geometry, not sequence, carries the activation signal, and propose the classifier as a fast orthogonal check on AI-predicted GPCR structures — an application they do not test.

### `necessity_claims` (verbatim, with pages)

- p5 — "This substantial gap demonstrates that sequence-derived features alone, despite their considerable richness, are fundamentally insufficient for activation state prediction. The geometric information encoded through equivariant message passing is essential for capturing the conformational differences that distinguish active from inactive states."
- p7 — "These ablations reveal that both evolutionary embeddings and geometric message passing are essential, with neither alone approaching the performance of the full model."
- p2 — "This sequence-structure gap — the disconnect between methods that understand evolution and methods that understand geometry — has prevented accurate, generalizable activation state prediction across the GPCR superfamily."
- p2 — "However, these models operate on sequence alone; they cannot distinguish active from inactive conformations when the amino acid sequence is identical."
- p2 — "Hand-crafted structural features such as inter-residue distances, helix orientations, or cavity volumes capture some activation signatures but require class-specific parameterization, expert knowledge for feature selection, and fail to generalize across the mechanistically diverse GPCR superfamily (Caniceiro et al. 2025)."
- p2 — "Critically, standard neural network architectures lack the geometric inductive biases necessary to respect molecular symmetries."
- p1 — "However, current computational approaches often rely on static sequence analysis or lose critical geometric context, failing to resolve the fine-grained structural switches that drive allosteric signaling."
- p1 — "determining the functional activation state of each structure remains a critical bottleneck in the field."
- p1 — "This annotation bottleneck directly impedes structure-based drug discovery, where distinguishing activation states is essential for designing state-selective modulators and understanding the molecular basis of biased signaling (Wootten et al. 2018; Kolb et al. 2022)."
- p2 (on the target of our own interest) — "Recent benchmarks have demonstrated that AlphaFold-predicted GPCR structures often fail to capture the characteristic TM6 displacement that defines the active state, instead producing conformations that lie somewhere between canonical active and inactive structures (Xu et al. 2025)."
- p10 — "This ambiguity is particularly problematic for structure-based drug design, where the activation state of the receptor directly affects the predicted binding mode and affinity of candidate ligands."
- p3 — "The DRY motif in TM3 and the NPxxY motif in TM7 are separated by approximately 15–20 Å, and their coordinated rearrangement upon activation cannot be captured by local features alone." (p2 in the Introduction; same sentence)

### `novelty_claims` (verbatim, with pages)

- p1 (abstract) — "Here we introduce Hyaline, a geometric deep learning framework that leverages E(n)-equivariant graph neural networks and ESM3 evolutionary embeddings to predict GPCR activation states directly from 3D coordinates."
- p2 — "Here we introduce HYALINE, a geometric deep learning framework that unifies evolutionary and structural representations for GPCR activation state prediction."
- p3 — "The core innovation enabling HYALINE to learn activation-discriminative features is the use of E(n)-equivariant message passing (Satorras, Hoogeboom, and Welling 2021; Mao et al. 2025) (Fig. 3)."
- p9 — "By unifying evolutionary embeddings from protein language models with E(n)-equivariant graph neural networks, HYALINE bridges the sequence-structure gap that has limited previous computational approaches."
- p12 — "HYALINE demonstrates that geometric deep learning can provide accurate, interpretable, and generalizable conformational state prediction, establishing a foundation for computational characterization of protein functional states at scale."
- p1 (abstract) — "Hyaline provides a rapid, interpretable framework for annotating receptor conformational states, establishing a scalable foundation for the high-throughput discovery of allosteric modulators in complex signaling landscapes."

**No claim of priority.** The paper never uses "first", "unprecedented" or an equivalent; its novelty claims are framed as unification and bridging, not as being first to the problem. Worth noting for any priority comparison.

Claims bearing directly on the state-metric use case (not novelty claims, recorded here because they are the sentences that would be cited):
- p6 — "The attention mechanism thus provides a learned 'activation sensor' that could be applied to analyze molecular dynamics trajectories, identify activation events in simulations, or assess the conformational state of computationally predicted structures."
- p11 — "HYALINE provides an orthogonal assessment of predicted conformational states that does not rely on the same underlying methodology as the structure prediction itself. By applying HYALINE to AlphaFold 3-generated GPCR models, researchers can obtain rapid, quantitative estimates of whether the predicted structure represents an active, inactive, or intermediate conformation."

### `stated_limits`

- Class imbalance and class skew: "The class imbalance toward active structures (72.7%) and the predominance of Class A receptors (79.4%) may limit performance on underrepresented categories. While performance on Class C and Class F receptors remained strong, the confidence intervals were wider due to smaller sample sizes" (p11).
- Binary only, no continuum, no transducer specificity: "The model is trained for binary classification and does not address the continuum of activation states or the distinction between G protein-biased and arrestin-biased conformations" (p11).
- **The limit that matters most to us, stated by the authors:** "Additionally, HYALINE is trained on experimental structures and may not perform optimally on computationally predicted structures that contain systematic errors or represent non-physiological conformations. Evaluating HYALINE on a benchmark of AlphaFold 3-predicted GPCR structures with known experimental states would clarify the model's applicability to this important use case. Domain adaptation techniques could potentially improve performance on predicted structures while maintaining accuracy on experimental structures" (p11).
- Label noise in the ground truth, acknowledged: "A small number of misclassifications could not be attributed to the above categories and may represent annotation errors in GPCRdb, genuinely ambiguous conformations, or edge cases where the model's learned features fail to generalize" (p9).
- Class F data scarcity: "despite having only 34 structures in the dataset ... The wider confidence interval reflects the limited structural data rather than fundamental model limitations, and suggests that performance would likely improve as more Class F structures are deposited" (p7).

**Not stated as a limit anywhere:** that the temporal split does not hold out receptors; that the decision threshold is unreported; that the reported metrics are ceilinged; that the model sees Cα only while the interpretation narrative is about side-chain salt bridges.

### `stance`

`precedent` + `contrast`. **Provisional — the user's call.**

- **`precedent` on the finding.** This is the closest thing in the corpus to an operationalised, structure-only, class-general GPCR activation-state predicate — exactly the function global TM-score cannot serve. It reports a concrete decision procedure (probability from geometry, no reference structure required), a per-class breakdown, and a stated intent to be applied to AI-predicted structures. That is a direct precedent for the metric we would use.
- **`contrast` on the rigour.** The number that would justify reuse is not the one reported: the headline is a same-receptor temporal split with no family-level holdout, on a corpus deliberately purged of ambiguous cases, with an unstated decision threshold, a metric ceilinged at ~0.99, ablation figures that disagree between text and figure (see `unresolved`), and no evaluation on any predicted structure whatsoever — the sole use case that would matter to us, and one the authors themselves flag as future work.

## E. Quantitative comparators

### `metrics_reported`

| metric | value | units | measured against | page |
|---|---|---|---|---|
| AuROC, HYALINE full | 0.995 ± 0.003 | AuROC | 5-fold CV, pre-2023 training set (n = 1,312), 30% seq-id cluster split | p5 (Table 1) |
| AuROC, HYALINE full | 0.991 (95% CI 0.984–0.997) | AuROC | Temporal test set, 2023–2024 deposits (n = 278) | p4, p5 (Table 1) |
| Accuracy | 0.976 ± 0.011 / 0.964 | fraction | CV / temporal test | p5 (Table 1) |
| Sensitivity (recall, active) | 0.990 ± 0.008 / 0.978 | fraction | CV / temporal test | p5 (Table 1) |
| Specificity (inactive) | 0.938 ± 0.021 / 0.921 | fraction | CV / temporal test | p5 (Table 1) |
| Precision | 0.977 ± 0.010 / 0.962 | fraction | CV / temporal test | p5 (Table 1) |
| F1 | 0.983 ± 0.007 / 0.970 | score | CV / temporal test | p5 (Table 1) |
| Matthews Correlation Coefficient | 0.936 ± 0.018 / 0.912 | MCC | CV / temporal test | p5 (Table 1) |
| **AuROC, Class A** | **0.997 (95% CI 0.995–0.999)** | AuROC | n = 1,263 Class A structures (79.4% of corpus) | p7 (Table 2) |
| **AuROC, Class B1 (Secretin)** | **0.988 (95% CI 0.971–0.998)** | AuROC | n = 145 | p7 (Table 2) |
| **AuROC, Class C (Glutamate)** | **0.971 (95% CI 0.943–0.991)** | AuROC | n = 94 | p7 (Table 2) |
| **AuROC, Class F (Frizzled)** | **0.956 (95% CI 0.901–0.989)** | AuROC | n = 34 | p7 (Table 2) |
| AuROC, Overall (Table 2 row) | 0.995 | AuROC | n = 1,590 | p7 (Table 2) |
| Accuracy by class | A 98.3% / B1 95.9% / C 91.5% / F 88.2% / Overall 97.6% | % | as above | p7 (Table 2) |
| Sensitivity by class | A 99.2% / B1 97.1% / C 93.2% / F 90.0% / Overall 98.9% | % | as above | p7 (Table 2) |
| F1 by class | A 0.988 / B1 0.968 / C 0.938 / F 0.900 / Overall 0.983 | score | as above | p7 (Table 2) |
| Accuracy, Class C, Fig. 4a bar | 87.2% (HYALINE) vs 63.5% (ESM3 seq-only) vs 50.0% (random) | % | Class C subset, n = 94 | p5 (Fig. 4a) — **conflicts with Table 2's 91.5% Class C accuracy** |
| AuROC, ESM3 + linear classifier (sequence-only) | 0.852 | AuROC | Temporal test set | p2, p5 |
| AuROC, ESM3 + MLP (sequence-only) | 0.867 (text/caption, p5) vs 0.807 (Fig. 7, p8) | AuROC | Temporal test / CV — **figures conflict** | p5, p8 |
| AuROC, random forest on 42 hand-crafted inter-residue distances | 0.891 | AuROC | Temporal test set | p5 |
| AuROC, random baseline | 0.500 | AuROC | — | p8 (Fig. 7) |
| Δ AuROC, HYALINE − ESM3-only | 13.9 percentage points | pp | Temporal test set | p2, p5 |
| Ablation: ESM3 → one-hot AA | 0.823 (text, p7) / 0.807 (Fig. 7, p8); Δ = −17.2 pp (text) / −0.188 (Fig. 7) | AuROC | 5-fold CV, 30% seq-id cluster split — **text and figure conflict** | p7, p8 |
| Ablation: − motif attention bias | 0.987, Δ = −0.008 (Fig. 7) vs "Δ = −2.7%, p < 0.01" (text) — **conflict** | AuROC | 5-fold CV | p7, p8 |
| Ablation: − RBF edge features | 0.982, Δ = −0.013 (Fig. 7) vs "reduced AuROC to 0.971 (Δ = −2.4%)" (text) — **conflict** | AuROC | 5-fold CV | p7, p8 |
| Ablation: − attention pooling | 0.978, Δ = −0.017 | AuROC | 5-fold CV | p8 (Fig. 7) |
| Ablation: − multi-scale edges | 0.971, Δ = −0.024 | AuROC | 5-fold CV | p8 (Fig. 7) |
| Ablation: 3 vs 5 message-passing layers | 0.981, Δ = −1.4% | AuROC | 5-fold CV | p8 |
| Attention fold-enrichment at biased motifs | DRY 3.2×, NPxxY 2.8×, CWxP 2.4×; all p < 0.001 (10,000-permutation test) | fold enrichment vs non-motif residues | Correctly classified temporal-test structures | p6 |
| Attention fold-enrichment at *unbiased* regions (autonomous discovery) | TM5 intracellular end 2.1×, helix 8 1.9× | fold enrichment | as above | p6 |
| Attention enrichment in the *no-bias* ablated model | DRY 2.4× (vs 3.2× with bias) | fold enrichment | 5-fold CV | p7 |
| Correlation, attention weight vs TM6 outward displacement | r = 0.78, p < 0.001 | Pearson r | All structures | p6 |
| Correlation, prediction confidence vs resolution | r = −0.119 | Pearson r | Temporal test set | p5 (Fig. 4b) |
| Accuracy by resolution band | <2.5 Å: 97.7%; ≥3.0 Å: 97.2% | % | Temporal test set | p5 (Fig. 4b) |
| Confidence distribution | 94.3% of predictions >0.9 or <0.1; 2.8% in 0.3–0.7 | % of predictions | Test predictions | p8 |
| Misclassifications, total and by cause | 39 total: 15 partially activated intermediates (38%), 11 Class C (28%), 8 experimental artifacts (21%), 5 unexplained (13%) | count / % of errors | Misclassified structures | p9 |
| Ionic-lock distance in misclassified intermediates | mean 6.2 Å (vs <4 Å fully inactive, >10 Å fully active) | Å, R3.50–E6.30 | 15 intermediate-category errors | p9 |
| Mean confidence, Class C errors | 0.58 | probability | 11 Class C errors | p9 |
| Inference runtime | 16.9 ms/structure mean; throughput 59/sec; "Full GPCRome: 7.6 s"; linear fit r² = 0.887 | ms, structures/s | Sequence length 150–500 residues, single GPU | p10 (Fig. 9b) |
| Inference runtime (Methods, conflicting) | "0.5 seconds per structure ... throughput of approximately 7,200 structures per hour" | s, structures/h | Single A100 40 GB, ~8 GB inference memory | p13 — **conflicts with Fig. 9b's 16.9 ms / 59 per second** |
| Training cost | ~4 hours for full 5-fold CV | hours | Single NVIDIA A100 (40 GB) | p13 |
| Corpus composition | 72.7% active; Class A 79.4% | % of structures | Full dataset (n = 1,590) | p11 |

### `n_predictions`

Not a sampling method — the classifier is deterministic and emits exactly one probability per input structure. Recorded in the schema's three parts:

- **Samples per target:** 1. No seeds, no ensembles, no repeated sampling. The only stochasticity at training time is dropout (0.1 features / 0.2 classifier) and Gaussian coordinate noise σ = 0.1 Å (p13, Table 3 p14); none of it is applied at inference, and no test-time averaging is reported.
- **Targets:** 1,590 structures (1,312 train / 278 temporal test), spanning classes A (1,263), B1 (145), C (94), F (34) (p4, p7, p12).
- **Total predictions:** 278 in the headline temporal-test arm; 1,590 across the pooled dataset reported in Table 2. Uncertainty on the temporal test comes from 1,000 bootstrap resamples of those 278 predictions, not from repeated model runs (p5, p13); CV uncertainty is mean ± 1.96 SE across 5 folds (p5).

### `comparable_to_ours`

*(left empty — populated by whoever holds STATUS.md and the manuscript)*

### `si_in_scope`

**SI HELD.** The Extended Data is inside the 15-page PDF: Table 3 (hyperparameters, p14), Table 4 (representative misclassified structures with PDB IDs, confidences, ionic-lock distances and TM6 displacements, p14), and Fig. 11 (Jumping Knowledge readout architecture, p14). Nothing material is deferred to an external supplement. Code, curated dataset and trained models are stated to be at https://github.com/Varosync/Hyaline under the MIT License (p13) — not verified here.

## F. Figures

One row per panel group. Split on `mark` or `measure`, not on `facet`.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 1 | β2AR inactive (2RH1, blue) superposed on active (3SN6, tan), illustrating the 14 Å TM6 outward displacement the classifier must detect | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 1 structure on 1 reference \| axis: none` | 1; single superposition, no view variation | — | CC-BY-NC-**ND** 4.0 (p1 footer, every page). **ND forbids redrawing as well as modifying.** |
| 2 | 3 | Full HYALINE pipeline: PDB Cα → ESM3 encoder + radius graph + RBF + motif IDs → 5× enhanced EGNN → JK concat → MLP classifier → activation probability | schematic | `SCHEMATIC \| end-to-end architecture and tensor-shape flow diagram \| no data` | Caption labels (a)(b)(c) but the rendered figure is one continuous three-column flow diagram, not three separate panels | Caption promises three lettered panels the figure does not visually separate | CC-BY-NC-ND 4.0 (p3) |
| 3 | 4 | Detail of a single enhanced EGNN layer: edge update, message MLP, motif bias, attention, node update, coordinate refine | schematic | `SCHEMATIC \| single equivariant message-passing layer with motif-bias injection \| no data` | 1 | — | CC-BY-NC-ND 4.0 (p4) |
| 4A | 5 | Accuracy of HYALINE vs sequence-only ESM3 vs random, for the Class C subset and overall | bar | `PLOT \| facet: none (1) \| vary: method (3: HYALINE full, ESM3 seq-only, random) \| series: subset (2: Class C n=94, Overall) \| measure: accuracy (%) \| mark: bar \| n: 94 per Class C bar, 278 or 1,590 per Overall bar (which is NOT REPORTED); 6 bars per panel` | 1 panel, 6 grouped bars | **y-axis truncated at 40%**, inflating the HYALINE/ESM3 gap. Only the Class C bars are value-labelled (87.2 / 63.5 / 50.0); the Overall bars carry no numbers. Caption claims "Error bars denote 95% confidence intervals computed via bootstrap resampling (n = 1,000)" but **no error bars are drawn**. Class C accuracy 87.2% here contradicts Table 2's 91.5% (p7). Caption discusses AuROC values (0.991, 0.852, 0.867, 0.891) that the panel does not plot — the panel plots accuracy. | CC-BY-NC-ND 4.0 (p5) |
| 4B | 5 | Prediction confidence against experimental resolution, correct vs error, with a shaded cryo-EM band and a fitted trend | scatter | `PLOT \| facet: none (1) \| vary: resolution, 1.0–5.0 Å (continuous) \| series: outcome (2: correct, error) + cryo-EM range band \| measure: prediction confidence (0.5–1.0) \| mark: point \| n: 1 per mark, 278 per panel` | 1 panel, two point series plus a dashed linear fit | y-axis truncated at 0.5; the correct-prediction cloud is pinned along confidence = 1.0, so the bulk of the data is an unresolvable line at the ceiling (the numeric saturation recorded in `metric_saturation`). The r = −0.119 in the panel title has no p-value or CI. | CC-BY-NC-ND 4.0 (p5) |
| 5A | 6 | Mean learned attention weight at each of the three biased motifs, split by activation state | bar | `PLOT \| facet: none (1) \| vary: motif (3: DRY, NPxxY, CWxP) \| series: activation state (2: active, inactive) \| measure: mean attention weight \| mark: bar \| n: NOT REPORTED per mark; correctly classified temporal-test structures per panel (≤278, exact n NOT REPORTED)` | 1 panel, 6 grouped bars with error bars | Bars over distributions — mitigated only because 5B shows the same data as violins. Caption says weights are "mapped to Ballesteros-Weinstein residue positions", but the panel's axis is three motif categories, not positions. Caption reports "Additional peaks at the intracellular end of TM5 (2.1×) and helix 8 (1.9×)" — **a claimed result with no panel showing it.** Error-bar definition not given. | CC-BY-NC-ND 4.0 (p6) |
| 5B | 6 | Full distribution of attention scores at the same three motifs, split by activation state | violin | `PLOT \| facet: none (1) \| vary: motif (3: DRY, NPxxY, CWxP) \| series: activation state (2: active, inactive) \| measure: attention distribution \| mark: violin \| n: NOT REPORTED per violin and per panel` | 1 panel, 6 violins with median bars | Caption claims a comparison "at conserved motifs compared to variable regions (p < 0.001, permutation test with n = 10,000 resamples)" — **the variable-region reference distribution is not plotted**, so the stated comparison cannot be read off the figure. n behind each violin never given. | CC-BY-NC-ND 4.0 (p6) |
| 6A-B | 8 | t-SNE of the 320-d pooled graph embeddings for the temporal test set, coloured first by activation state, then by receptor class | scatter | `PLOT \| facet: none (1) \| vary: t-SNE dimension 1 (continuous, arbitrary units) \| series: activation state (2) in panel a; receptor class (4: A, B1, C, F) in panel b \| measure: t-SNE dimension 2 (continuous, arbitrary units) \| mark: point \| n: 1 per mark, 278 per panel` | 2 panels; same mark and same measure, differing only in the `series` colouring — one row per the v3 split rule | Axes unlabelled beyond "t-SNE Dimension 1/2" with no tick values; t-SNE inter-cluster distances are not interpretable yet the caption reads separation as evidence ("The clear separation between clusters explains the high classification performance"). Perplexity 30, 1,000 iterations given; random seed and repeat runs NOT REPORTED. | CC-BY-NC-ND 4.0 (p8) |
| 7 | 8 | Ablation ladder: AuROC of the full model and six reduced variants including the random floor | bar (horizontal) | `PLOT \| facet: none (1) \| vary: model variant (7: full, −motif bias, −RBF edges, −attention pooling, −multi-scale edges, ESM3+MLP, random) \| series: none (1) \| measure: AuROC (0.4–1.0) \| mark: bar \| n: 5 CV folds per bar, 1,312 training structures per panel` | 1 panel, 7 horizontal bars, each value-labelled with its Δ | **x-axis truncated at 0.4**, compressing the four architectural ablations (0.971–0.987) into visually indistinguishable bars. No error bars or CIs on any bar despite 5-fold CV being available. **Figure values contradict the body text** for three of the ablations (motif bias −0.008 vs "−2.7%"; RBF −0.013 vs "−2.4%"; ESM3 0.807 vs 0.823/"−17.2%"). The caption misdescribes the ESM3 ablation as "Removal of the geometric structure encoding (replacing ESM3 embeddings with one-hot amino acid encodings)" — that ablation removes the *sequence* encoding, not the geometric one. | CC-BY-NC-ND 4.0 (p8) |
| 8A-B | 9 | Ionic-lock geometry in β2AR inactive (2RH1, R3.50–E6.30 = 3.4 Å) and active (3SN6, 11.2 Å), the mechanism the model is said to detect | structure render | `RENDER \| facet: activation state (2: inactive 2RH1, active 3SN6) \| views: 1 \| overlay: 0 predictions on 2 reference structures \| axis: none` | 2 panels, one per state, same camera framing | **The body text cites Fig. 8 for a result the figure does not contain**: "We analyzed the distribution of prediction confidence scores to identify patterns in model certainty and characterize the sources of misclassification (Fig. 8)" (p8) — there is no confidence-distribution panel anywhere in the paper. Also: the panels turn on side-chain salt-bridge geometry, but the model consumes Cα coordinates only, so the figure illustrates a mechanism the classifier cannot observe directly. | CC-BY-NC-ND 4.0 (p9) |
| 9A | 10 | UMAP of learned graph representations coloured by transducer coupling group | scatter | `PLOT \| facet: none (1) \| vary: UMAP 1 (continuous, arbitrary units) \| series: transducer group (4: Gs n=179, Gi/Gq n=94, Mixed n=1263, Other n=54) \| measure: UMAP 2 (continuous, arbitrary units) \| mark: point \| n: 1 per mark, 1,590 per panel` | 1 panel | Legend n values (179 / 94 / 1263 / 54, sum 1,590) are the **full dataset**, while the parallel t-SNE in Fig. 6 uses only the 278-structure test set — the two embedding figures are on different populations without saying so. The group sizes 1263 and 94 are exactly Table 2's Class A and Class C counts, so "Mixed"/"Gi/Gq" appear to be re-labelled class strata rather than genuine transducer groups. Caption claims "clear separation of activation states" but the panel is coloured by transducer, not by state. Axes unlabelled and unticked. | CC-BY-NC-ND 4.0 (p10) |
| 9B | 10 | Inference time against sequence length, with a linear fit, demonstrating O(N) scaling | scatter + fitted line | `PLOT \| facet: none (1) \| vary: sequence length, 150–500 residues (continuous) \| series: none (1) \| measure: inference time (ms) \| mark: point + line \| n: 1 per mark, NOT REPORTED per panel` | 1 panel | The panel's headline numbers ("Mean: 16.9 ms/structure", "Throughput: 59/sec") are internally inconsistent — 16.9 ms/structure implies ~59 **per second only if** the two are read together, yet Methods p13 states "0.5 seconds per structure" and "approximately 7,200 structures per hour" (≈2/sec), a ~30× disagreement. r² = 0.887 is reported without n or hardware for the timing runs. | CC-BY-NC-ND 4.0 (p10) |
| 10A | 11 | UMAP of the 96-d RBF edge-feature encoding at the DRY motif, coloured by activation state | scatter | `PLOT \| facet: none (1) \| vary: UMAP 1 (continuous, arbitrary units) \| series: activation state (2: active, inactive) \| measure: UMAP 2 (continuous, arbitrary units) \| mark: point \| n: 1 per mark, NOT REPORTED per panel` | 1 panel | Axes unlabelled and unticked; n behind the cloud never stated; no quantification of the separation the caption implies. | CC-BY-NC-ND 4.0 (p11) |
| 10B | 11 | Trained per-motif attention bias weights after learning | bar | `PLOT \| facet: none (1) \| vary: motif category (5: None, DRY, NPxxY, CWxP, PIF) \| series: none (1) \| measure: learned weight (0–1.2) \| mark: bar \| n: 1 trained model per bar` | 1 panel, 5 value-labelled bars (0.00, 0.80, 0.59, 0.40, 0.99) | Bars come from a single trained model with no error bars or seed replicates. **A fifth category, PIF (0.99, the largest learned weight of all), appears here and nowhere else** — the Methods motif-detection section (p12) describes only DRY, NPxxY and CWxP, and no text discusses PIF. Caption text describes only the three-motif scheme, contradicting its own panel. | CC-BY-NC-ND 4.0 (p11) |
| 11 | 14 | Jumping Knowledge aggregation and readout head: concatenation of all six layer representations, pooling, MLP classifier, sigmoid to activation probability | schematic | `SCHEMATIC \| readout architecture and tensor-shape flow from EGNN stack to activation probability \| no data` | 1 | — | CC-BY-NC-ND 4.0 (p14) |

**Panel-group rows: 15.** Pages rendered to resolve panel structure: 2 (pages 5 and 6 — Fig. 4 and Fig. 5 marks and series were not recoverable from captions). All other rows were filled from captions plus the text layer.

**License, stated once for the whole paper:** "It is made available under a CC-BY-NC-ND 4.0 International license" — appears in the footer of every page, first on p1. **The ND clause forbids derivatives, so no figure here may be redrawn, adapted or re-plotted; only whole-figure reproduction with attribution, and even that is non-commercial.** The code and models are separately MIT-licensed (p13), which does not extend to the figures.

## G. Provenance

| Field | Value |
|---|---|
| `extracted_on` | 2026-09-07 |
| `extractor` | claude subagent (Claude Opus 5) |
| `schema_version` | v3 |
| `confidence` | **medium.** The text layer is clean and every number in Tables 1–4 and the body was legible. Confidence is held below high for two reasons: (1) the paper contradicts itself numerically in at least four places (ablation deltas text-vs-Fig. 7; ESM3+MLP AuROC 0.867 vs 0.807; Class C accuracy 87.2% Fig. 4a vs 91.5% Table 2; runtime 16.9 ms Fig. 9b vs 0.5 s Methods), so several `metrics_reported` rows carry two values rather than one and I could not determine which is authoritative; (2) Table 2's class rows sum to 1,536 against a stated overall n of 1,590, and Fig. 9a's legend sums to 1,590 while the parallel Fig. 6 t-SNE uses n = 278, so the population behind several analyses is ambiguous. Figure rows for pages I did not render (7, 9, 10, 11) rest on captions plus body text, which for the ablation and UMAP panels were adequate. |
| `unresolved` | See list below. |
| `why_it_matters` | *(left empty — the user's call)* |

### `unresolved`

1. **Which ablation numbers are correct.** Text (p7) and Fig. 7 (p8) disagree on three of six ablations. Text: motif bias Δ = −2.7%, RBF → 0.971 (Δ = −2.4%), ESM3 → 0.823 (Δ = −17.2 pp). Figure: motif bias 0.987 (−0.008), RBF 0.982 (−0.013), multi-scale edges 0.971 (−0.024), ESM3+MLP 0.807 (−0.188). The figure additionally lists an "attention pooling" ablation the text never mentions, and the text's "0.971 for RBF" collides with the figure's "0.971 for multi-scale edges". Cannot resolve from the PDF.
2. **The decision threshold is never stated.** Accuracy, sensitivity, specificity, precision, F1 and MCC all require an operating point; only AuROC is threshold-free. 0.5 is inferable from "structures near the decision boundary (mean confidence: 0.58)" (p9) but is nowhere written. For a paper offered as a state-assessment metric this is the field most needed for reuse.
3. **Number of distinct receptors, and train/test receptor overlap.** Never reported. The temporal split is by deposition date only; no sequence- or family-level holdout is applied to the temporal test set (the 30% MMseqs2 clustering is confined to CV folds, p8 caption / p13). Whether any receptor appears in both halves — and how many — cannot be determined, and given the corpus's known concentration on β2AR / A2A / M2 (p4) it is likely that most do.
4. **The "PIF" motif in Fig. 10b (p11).** It carries the largest learned bias weight (0.99) yet appears in no Methods description, no motif-detection rule, and no body text. Whether a fourth motif was in the trained model but omitted from the write-up is undeterminable.
5. **Which population Table 2 describes.** Class rows sum to 1,536 against a stated overall of 1,590 (54 missing; Fig. 9a shows an "Other (n=54)" group). The per-class breakdown also spans the full 1,590-structure corpus, not the 278-structure temporal test set, yet the section framing it (§2.4, p6–p7) presents it as a generalization assessment. So the per-class AuROCs are **not** held-out numbers in the way the temporal 0.991 is.
6. **Inference speed.** 16.9 ms/structure and 59/sec (Fig. 9b, p10) versus 0.5 s/structure and ~7,200/hour (p13) — roughly 30× apart, with no reconciliation.
7. **Whether the classifier works on predicted structures at all.** The paper's headline motivation (§3.3, p10–p11) and its own stated limitation (p11) both point at scoring AlphaFold 3 / Boltz / Chai models; **no such evaluation exists in the paper.** Every number reported is on experimental coordinates.
8. **Calibration evidence.** Asserted at p5 ("calibration analysis confirmed that predicted probabilities remained well-calibrated"); no calibration plot, Brier score or ECE appears anywhere.
9. **Tags needed that the v3 vocabulary does not contain** — none invented, all recorded here:
   - **A method tag for a supervised state classifier / scoring function.** The Method family (`cofolding`, `msa-subsample`, `msa-state-filter`, `template-state-bias`, `af-cluster`, `latent-steering`, `md`, `md-emulator`, `enhanced-sampling`, `benchmark-only`, `experimental`) has no entry for a model that consumes a structure and emits a state label. `benchmark-only` is wrong (this is a method, not a benchmark) and `experimental` is wrong (no wet lab). Something like `state-classifier` or `structure-scoring` is missing. **This paper currently carries no method tag at all**, which means a method-family reverse lookup will not find it.
   - **A tag for "the intended application was proposed but never run".** Route 7 in `oracle_leakage` and `stated_limits` both land on it; `design-level-oracle` covers the corpus-curation half but not the untested-application half.
   - Deliberately **not** used, to avoid false positives on reverse lookups: `two-state` (nothing is generated, so a "which papers produced two states" query must not return this); `state-annotated-input` (GPCRdb annotations are the supervision target, not a state-annotated template or alignment fed to a predictor); `confidence-as-discriminator` (the tag is defined for pLDDT/pTM repurposed as a state judge — here the sigmoid output *is* the prediction, and tagging it would pollute the pLDDT query); `no-template-no-msa` (defined for a de-novo prediction input regime; HYALINE is MSA-free but takes a solved structure as input, so the tag would mean something different here); `oracle-leak` (the GPCRdb labels are legitimate supervision, not pipeline contamination — `design-level-oracle` is the honest weaker call).

---

## Tags

`gpcr` `binary-predicate` `saturating-metric` `anti-memorization` `design-level-oracle` `preprint` `precedent` `contrast` `comparator-numbers`

*(No Method-family tag applies — see `unresolved` item 9. No State-handling tag applies: the method generates nothing. No Control-family tag applies: there is no generative handle. No Site tag applies: no binding site was studied, allosteric application is discussion-only.)*
