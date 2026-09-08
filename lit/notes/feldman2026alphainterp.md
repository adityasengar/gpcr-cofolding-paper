# feldman2026alphainterp

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` + reason where the field presupposes a conformational generator this paper is not.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–45)** and coincide with the
printed page numbers. Structure: p1 title/abstract, p2 abstract cont. + §1 Introduction, p3 intro
cont. + §2.1 checkpoint design, p4 **Fig 1** (13 panels A–M), p5 §2.1 cont. + §2.2, p6 §2.2 PCA +
**activation patching results**, p7 §2.3 linear probes, p8 §2.4 MSA removal, p9 §2.4 cont. + §2.5
mutational invariance, p10 **Fig 2** (8 panels A–H), p11–12 §2.5–2.6, p13 **Fig 3** (6 panels A–F),
p14–15 §2.7 SABmark, p15–16 §2.8 fold-switching, p16 §2.9 MSA perturbation, p17 **Fig 4** (6 panels
A–F), p18–19 §2.10 phylogenetic subsampling + fake MSA, p20 **Fig 5** (4 panels A–D), p21–22 §2.11
residue-level n=1 analysis, p22–24 §3 Discussion, p24–37 §4 Methods (4.1 datasets … 4.11 statistics),
p38 acknowledgments + start of references, p38–45 references only.

---

## What this paper is, stated up front because it governs sections C and E

This is a **mechanistic-interpretability / representation-probing paper about AlphaFold 3**, plus a
large **MSA-ablation and MSA-perturbation study**. It is **not** a conformational-sampling method, not
a co-folding method, and proposes no predictor. It runs stock AlphaFold 3 (templates off, one
diffusion sample) tens of thousands of times, harvests internal tensors, and probes them.

**The single most important structural fact for anyone citing this note: the paper is overwhelmingly
correlational, with exactly one genuinely causal experiment, and that causal experiment's downstream
readout is the distogram head — never the diffusion module, never predicted coordinates.** See
`oracle_leakage`, `controls_run` and the dedicated section "REPRESENTED vs CAUSALLY USED" below.

### Exactly what was probed, where, and with what — the precision this note exists for

**Internal objects extracted** (p3–p5 §2.1; p25 §4.2):

| object | shape | where it lives in AF3 |
|---|---|---|
| single representation `s` | `L × 384` | residue-level track |
| pair representation `p` | `L × L × 128` | pairwise track |
| distogram | `L × L × 64` softmax bins (p29, "C is the number of distance bins, which is 64, as is the default") | output of the distogram head |
| distogram head weights `W`, `b` | linear, `128 → 64`, symmetrised | `z_ij = (p_ij W + b) + (p_ji W + b)` (p30) |

**The MSA representation itself was never extracted. No attention maps, no diffusion-module
internals, no per-head analysis, no sparse autoencoders.** The paper's object set is exactly: single
track, pair track, distogram, distogram head.

**Four checkpoints, not four layers** (p3–p5, §2.1; p25, §4.2). This matters and is easy to
misdescribe:

| checkpoint | position in forward pass | recycling step | verbatim |
|---|---|---|---|
| **A** | after sequence initialisation, **before the MSA module has been fully applied** — but *not* MSA-free | not stated (implicitly r=0) | "Checkpoint A is sampled immediately after sequence initialization but before the MSA module has been fully applied. It is not entirely MSA-free: per-position amino acid frequency distributions and deletion means are already concatenated into the initial single representation during input preparation, embedding a shallow statistical summary of co-evolutionary context before any deep pairwise interaction occurs." (p3) |
| **B** | after the MSA module, before the Pairformer | **r = 0 only** | "Checkpoint B is sampled after the MSA module and before the Pairformer, collected exclusively at the first recycling iteration (r = 0). This marks the first point at which deep co-evolutionary information enters the pair channel through the outer product mean and row-wise gated self-attention." (p3) |
| **C₁** | after the **final** Pairformer layer | **r = 0** | "Checkpoint C1 is sampled after the final Pairformer layer at r = 0, capturing the model's first complete bottom-up structural hypothesis from sequence and MSA alone, with no geometric prior carried in from previous recycling iterations." (p3–p5) |
| **C_N** | after the **final** Pairformer layer | **r = N − 1, N = 10** (AF3 default) | "Checkpoint C_N is sampled after the final Pairformer layer at the terminal recycling iteration r = N − 1. It is the representation that directly conditions the diffusion module and determines the predicted structure. For all analyses, N = 10, consistent with the AlphaFold 3 default." (p5) |

**Critical caveat on granularity, because the paper's own framing invites over-reading.** There is
**no per-Pairformer-layer resolution anywhere in this paper.** C₁ and C_N are both taken *after the
final Pairformer layer*; they differ only in recycling step (0 vs 9). The number of Pairformer layers
is never stated. So "layer by layer" is the wrong description of this study: it is **four checkpoints
across two axes — module position (3 positions: init / post-MSA-module / post-Pairformer) and
recycling step (2 values: r=0 and r=9)**. Every "the Pairformer does X" claim in this paper is
inferred from the A/B → C₁ contrast, i.e. from crossing the entire Pairformer stack in one step.

**Recycling coverage is likewise coarse:** only r = 0 and r = 9 are sampled. Intermediate recycles
(r = 1…8) are never examined, so "recycling continues to reshape the latent geometry" (p5) rests on a
two-point comparison.

**Probes and analyses applied** (p26–p35, §4.3–4.9):

| probe / analysis | applied to | target | where |
|---|---|---|---|
| Ridge regression, α = 1.0, standardised features | pooled pair (128-d), pooled single (384-d) | pTM, TM-score | p26 §4.3.1 |
| Ridge regression | per-residue single | secondary structure, SASA, burial depth, amino-acid identity | p7, p26–27 |
| Ridge regression | per-pair `p_ij` | Cα–Cα distance, 8 Å contact | p7, p30 §4.5.1 |
| Three-probe distance decodability: (i) `|i−j|` baseline, (ii) isolated `p_ij`, (iii) context-augmented (`p_ij` + row/col means + `|i−j|`) | pair | Cα–Cα distance | p30 §4.5.1 |
| Unique-information decomposition: single-only / pair-only / joint ridge → `U_S = R²_J − R²_P`, `U_P = R²_J − R²_S`, `S = (R²_S + R²_P) − R²_J` | single + one-side-pooled pair | pTM, TM-score, SASA, burial, secondary structure | p28 §4.3.4 |
| IncrementalPCA; effective dimensionality = #PCs for 95% variance | pooled reps | — | p28 §4.3.3 |
| Effective rank = `exp(−Σ p_k log p_k)` over normalised singular values | reps | — | p29 §4.5 |
| Spearman ρ between PC scores and biophysical labels | top-5 PCs | contact density, burial, SASA, pTM, seq. length, TM-score | p28, Fig 1F–G |
| Shannon entropy of distogram; ΔH; KL(p_MSA ‖ p_no-MSA), binned by sequence separation | distogram | — | p29 §4.4 |
| Cosine distance on **unpooled, fully flattened** tensors | pair (upper triangular), single | drift under mutation, SABmark alignment, fold-switch regions | p32 §4.7.2, p33 §4.8.1, p35 §4.9 |
| Mean resultant vector length `R̄` of PCA drift vectors | pooled C_N pair | directional coherence of collapse | p32–33 §4.7.3 |
| Leave-one-out nearest-neighbour cosine classifier | pooled pair | SABmark fold group | p34 §4.8.4 |
| **Activation patching** (the only intervention) | C_N pair, immediately before distogram head | distogram entropy | p30–31 §4.6 |
| MLPs and Gradient Boosting Trees (comparators to ridge) | as above | as above | p27 |

**What each probe achieved, in one line each** — numbers all in `metrics_reported`:
pTM self-prediction from the pair track rises 0.34 (A) → 0.86 (C_N); pairwise-distance decodability
rises 0.311 → 0.474 (0.504 with context) against a 0.239 sequence-separation floor; contact balanced
accuracy 0.642 → 0.703; secondary structure 0.43 → 0.57; SASA 0.02 → 0.09; burial 0.05 → 0.15;
amino-acid re-identification "near-perfect" at every checkpoint (no number given); pair beats single
on unique information for every target; effective dimensionality follows A(16) → B(32) → C₁(19) →
C_N(17); nearest-neighbour fold classification peaks at 0.670.

### REPRESENTED vs CAUSALLY USED — the distinction this note is written to preserve

**Shown to be REPRESENTED (correlational, read-out only).** Everything above. Every probe, every PCA,
every cosine distance, every entropy comparison, every SABmark and fold-switching analysis, every MSA
perturbation arm. These establish that information is *decodable from* the representations and that
the representations *change* when the input changes. **None of them establishes that the model uses
the decoded quantity.** The paper is candid about the direction of the question but not always about
which side of the line a given result falls on.

**Shown to be CAUSALLY USED — one experiment, in three variants, all at C_N, all read out through
the distogram head only** (p6–p7 results; p30–31 §4.6 methods):

1. **PC-direction shift.** `p'_ij = p_ij + σ √λ_k v_k` for `σ ∈ {−2, −1, +1, +2}`, `k ∈ {1..5}`;
   patched tensor pushed through the **frozen distogram head**; measured Δ mean distogram entropy.
   Result: PC1 at +1σ raises entropy by +0.0044 for accurate predictions vs +0.0133 for poor ones
   (average +0.0088), `ρ = −0.757` against original predicted confidence; PC2 shifts entropy the
   other way (Fig 1H: −0.0094 at +1σ, −0.0184 at +2σ).
2. **Cross-protein transplantation.** The C_N pair tensor of the single most accurate training-set
   protein (TM = 0.999) overwritten into low-accuracy test targets up to `L_min = min(L_T, L_S)`;
   mean distogram entropy drops by **−0.268**.
3. That is the entire causal content of the paper.

**What the causal experiment does NOT show, stated precisely.** No patched representation was ever
passed to the diffusion module. **No predicted coordinate, TM-score, RMSD, lDDT or pLDDT is reported
for any patched run.** The measured effect is a change in an *auxiliary output distribution*, and the
paper itself describes that output's head as a probe — verbatim, p30: "**Unlike other structural
modules, the AlphaFold 3 distogram head acts as a direct, transparent linear probe**… Because this
projection lacks intermediary non-linearities or layer normalization, targeted interventions on p_ij
map directly to changes in the output probability distribution and its corresponding Shannon entropy
H_ij." The transparency that makes the intervention interpretable is exactly what makes it weak
evidence of downstream structural causation: a linear head with no nonlinearity will move when you
move its input, whether or not the diffusion module cares.

The authors flag the unresolved half themselves, verbatim, p22: "This raises a question the framework
makes tractable but that this study does not resolve: whether direct intervention on internal
representations can induce structures the model would otherwise suppress due to evolutionary
precedent or data scarcity."

**Two-line summary for the caller.** *Representation:* the pair track at C_N linearly encodes
distances, contacts, secondary structure and the model's own confidence, and MSA removal destroys
that encoding — all measured by read-out probes with no intervention. *Causal use:* one intervention
family, activation patching on the C_N pair tensor, changes distogram entropy (PC1 +1σ → +0.0088
bits; cross-protein transplant → −0.268 bits) and nothing else was measured, so causal control is
demonstrated over the model's **geometric certainty as expressed in an auxiliary linear head**, not
over its predicted structure. The paper's own words for the gap, p22: "**whether direct intervention
on internal representations can induce structures the model would otherwise suppress … this study
does not resolve.**"

**Everything MSA-related is an INPUT ablation, not an internal intervention.** No-MSA, column
shuffling, row subsampling, phylogenetic tiering and fake-MSA injection are all changes to AF3's
*inputs*. They are strong, well-controlled causal evidence about the input→output map, and they are
the paper's best evidence — but they say nothing directly about which internal tensor carries the
effect. The localisation claims (p11, verbatim: "it emerges specifically within the Pairformer, where
residue-residue geometry is actively reconciled into a fold hypothesis") are
correlational overlays on those input ablations.

---

## A. Identity

- **citekey**: `feldman2026alphainterp`
- **doi**: **10.64898/2026.04.22.720175** (bioRxiv). Stamped in the header of every page: "bioRxiv
  preprint doi: https://doi.org/10.64898/2026.04.22.720175; this version posted April 23, 2026."
  Matches `refs.bib`.
- **year**: **2026** (posted 23 April 2026, p1 header; PDF CreationDate 22 Apr 2026).
- **venue**: **bioRxiv preprint, not peer reviewed.** Verbatim, p1 header: "which was not certified by
  peer review". Tagged `preprint`. **Licence: CC-BY-ND 4.0 — the ND clause matters, see `reuse`.**
- **title**: AlphaInterp: Probing AlphaFold 3's Internal Representations Reveals Evolutionary
  Determinants of Predicted Structure and Confidence — p1.
  **Note a discrepancy with `refs.bib`,** which records a different title: "AlphaInterp: Mechanistic
  Interpretability of AlphaFold 3 Reveals How Evolutionary Information Shapes Protein Structure
  Prediction". The PDF title above is authoritative; the bib entry appears to be from an earlier
  version or an abstract listing. Recorded in `unresolved`.
- **authors**: Jonathan Feldman (Georgia Tech College of Computing / Center for the Study of Systems
  Biology / School of Biological Sciences) and Jeffrey Skolnick (corresponding, same centre) — p1.
  Two authors, one lab. Funded by NIH GM-118039 (p38). Relevant self-citation: ref [5] is
  Feldman & Skolnick, *AF3Complex* (Bioinformatics 2025); ref [11] is Feldman et al. on
  biophysically grounded ΔG prediction; ref [18] is Feldman & Feldman on biosecurity.

## B. Scope

- **system**: **general protein** — monomers, with a deliberate `fold-switching` arm. Three datasets
  (p24 §4.1): (i) 400 monomeric proteins with no family restriction; (ii) SABmark, 100 proteins in 5
  SCOP fold groups; (iii) 46 experimentally validated fold-switching (metamorphic) protein pairs.
  **No GPCR, kinase, transporter or membrane-protein analysis. No complexes, no ligands, no nucleic
  acids** — despite AF3 being a co-folding model, every input in this paper is a single protein
  chain. The paper says the multimer case is untested and expects it to be worse (p23): "For
  multimeric complexes, which are far more structurally challenging and whose interactions govern
  much of biology, the situation is unlikely to improve".
- **n_targets**: several nested sets — record them separately, they are not interchangeable.

  | set | n | selection | page |
  |---|---|---|---|
  | Primary monomer benchmark | **400** = 200 **Novel** + 200 **Similar** | all deposited **after 30 Sep 2021** (AF3 training cutoff); Novel = <30% homology to any pre-Sep-2021 PDB entry, Similar = ≥30%; no two proteins in the set share ≥30% identity | p5, p24 |
  | SABmark | **100** proteins = 5 groups × 20; **950** within-group pairs, **560** retained (those with complete residue-level structural-overlap annotations) | same SCOP fold within group, ≤25% pairwise identity; each group from a distinct SCOP group, no PDB in two groups | p14, p24 |
  | Fold-switchers | **46 pairs** (= **92 domains**, from Fig 3D/F legend) | from ref [23]; excluded if chain length > 10× the fold-switching region; redundant PDBs removed; ≥60% local identity between annotated switching fragment and deposited sequence | p15, p25 |
  | MSA perturbation (shuffle + subsample) | **200** (the Novel subset only) | — | p16 |
  | Phylogenetic subsampling + fake-MSA injection | **61** of the 200 Novel | required ≥10 sequences in *each* of the similar / medium / dissimilar tiers | p18, p36 |
  | Fake-MSA donors | **139** non-qualifying proteins | the complement of the 61 | p19, p37 |
  | Nested 30–60%-identity subsampling | **183** of the 200 Novel | ≥10 sequences in the 30–60% identity band | p22 |

  **A generality flag worth carrying:** the paper's headline "phylogenetic diversity, not depth"
  result rests on **61 proteins** (30.5% of the Novel set, 15.25% of the full benchmark), selected
  *because* their MSAs happened to have coverage in all three tiers. The nested 183-protein analysis
  (p22) is the generalisation check and it only tests one tier band.
- **method_class**: **other** — mechanistic interpretability / linear probing of internal
  representations + activation patching, combined with a systematic input-ablation study of the MSA.
  It is not co-folding, not MSA-state-filtering, not template-biasing, not MD, not enhanced sampling,
  not clustering, not benchmark-only. It *contains* MSA subsampling, but as a perturbation instrument
  rather than as a conformational-sampling method — see the tag notes, this distinction is a genuine
  v3 vocabulary gap.
- **backbones**: **AlphaFold 3 only. Single backbone; no head-to-head comparison; `multi-backbone`
  does NOT apply.** AF2, Boltz, Chai, OpenFold3 and Protenix appear nowhere as run systems.
  Implementation detail: the paper interacts with "the AlphaFold 3 input JSON files" and names the
  `pairedMsa` and `unpairedMsa` fields (p31, p35), i.e. the official AF3 open-source interface, but
  **no version, commit, weights release or repository is ever named.** `N = 10` recycles, AF3 default
  (p5). Recorded in `unresolved`.
- **templates**: **OFF, everywhere, stated flatly.** Verbatim, p26: "**Critically, across all
  generated structures and the embeddings that precede them, no structural templates were used.** As
  is mentioned in further detail, some analyses included the MSA and some did not as inputs into
  AlphaFold 3, but **no analysis used template information as inputs to reduce potential confounds
  and structural invariance.**" This is unusually clean for this corpus and is the reason
  `no-template-no-msa` can be applied without inference.
- **msa_handling**: **six regimes in one paper — this is the paper's instrument set.** Keep them
  distinct; the schema's warning that subsampled ≠ state-filtered applies with extra force here
  because *none* of these is state-filtering.
  1. **full MSA** (control, standard AF3 operating regime) — p8.
  2. **no MSA** — both `pairedMsa` and `unpairedMsa` explicitly omitted (p31). Run on all 400
     monomers, all SABmark proteins, all fold-switch pairs, and all mutation levels.
  3. **column shuffling** — each selected alignment column independently permuted across rows;
     destroys pairwise coupling, **preserves per-position marginal amino-acid distribution and
     preserves depth**; A3M-aware (permutes only non-lowercase positions so alignment length is
     invariant). Rates 10, 20, 40, 70, 90, 95, 99% (p35–36, Algorithm 1).
  4. **row subsampling** — uniform random removal of homolog rows, query fixed; **preserves coupling,
     reduces depth**. Same seven rates (p36).
  5. **phylogenetic tiering** — 12 variants per protein: depths {1, 5, 10} × tiers {similar ≥80%
     identity, medium 50–70%, dissimilar ≤30%, random uniform}. Deterministic sort order so smaller
     depths are strict subsets of larger (p36–37).
  6. **fake-MSA injection** — donor sequences from *unrelated* proteins' MSAs, trimmed to the target's
     aligned length, A3M format preserved, depths {1, 10, 20, 50, 100} (p37). **This is the paper's
     single best-designed control.**
  Additionally: for all perturbation runs, "**All paired MSAs are replaced with the query sequence**,
  and all predictions are computed with identical hyperparameters and random seeds to the control"
  (p35). Under mutation, the MSA-conditioned pipeline **reuses the unmutated sequence's MSA**;
  regeneration is *not* run here, it is cited from ref [21] (p31).
  **State-filtering: absent entirely. No MSA in this paper is selected to favour a conformational
  state.**

## C. Conformational core

**Blanket note.** This paper is not a conformational-generation method and does not claim to be. It
generates one structure per input condition and studies representations. Fields that presuppose a
generator are marked `NOT APPLICABLE` **with a reason**, per the v3 rule; the fields that carry real
meaning for a probing paper (`structural_priors_used`, `oracle_leakage`, `anti_memorization_*`,
`controls_run`, `metric_saturation`, `confidence_as_discriminator`) are filled in full, because those
are the fields the paper's claims actually rest on.

- **states_generated**: **one.** AF3 is run at defaults with a single exception — verbatim, p26:
  "Instead of generating five diffusion samples, as is standard, for computational efficiency **only
  one diffusion sample was generated during structural inference.**" So every prediction in this
  paper is a single structure, and there is no per-target ensemble anywhere. This is *not*
  `NOT APPLICABLE`: structures are generated in bulk (see `n_predictions`), and the paper's
  fold-switching result is precisely that the one state produced is the same one for both members of
  a metamorphic pair — "AlphaFold 3 Collapses Metamorphic Sites to a Single Fold" (§2.8 heading,
  p15). Mean RMSD between the two predicted fold-switching regions is **2.02 Å** where experiment
  says they differ (p15). `one` is therefore the honest and load-bearing answer, not a shrug.
- **structural_priors_used**: **extensive, and none of it is a defect** — it is all evaluation-side
  and design-side knowledge, cleanly separated from AF3's inputs. Enumerated:
  1. **PDB coordinates as probe labels.** Secondary structure (mmCIF `struct_conf` /
     `struct_sheet_range`, falling back to DSSP on the Cα trace), SASA (Shrake–Rupley, 1.4 Å probe),
     burial score (9-nearest-neighbour packing density, normalised to [0,1]), Cα–Cα distance
     matrices, 8 Å binary contacts — all "derived directly from PDB coordinate files" (p27 §4.3.2).
     Analyses using these were restricted to structurally resolved residues (p27).
  2. **SABmark gold-standard residue-level structural alignments** used to index matched sub-tensors
     `P_A[I_A, I_A, :]` and `P_B[I_B, I_B, :]` (p33 §4.8). Verbatim, p33: "To solve this without
     relying on spatial pooling—which smears and destroys position-specific geometric data—we
     utilized the **gold-standard structural alignments from the SABmark benchmark**."
  3. **SCOP fold-group labels** as the ground truth for nearest-neighbour fold classification
     (p24, p34).
  4. **Experimentally annotated metamorphic regions** from ref [23], located in the predicted
     sequences by windowed alignment to give `I_FS` (p35 §4.9).
  5. **Deposition dates and pre-2021 PDB homology** used to construct the Novel/Similar split
     (p24 §4.1) — this is the anti-memorisation design, and it is a structural prior in the sense the
     v3 field intends.
  6. **Fold-switch pair curation used the deposited structures** (chain-length-to-switch-region ratio
     ≤10, ≥60% local identity to the deposited sequence, redundancy removal) — p25.
  7. **TM-score / Kabsch RMSD references** are deposited PDB structures throughout (OpenStructure,
     p37).
  **None of these ever enters AlphaFold 3's input.** The inputs are: sequence, and (sometimes) an
  MSA. That is all.
- **oracle_leakage**: **Route by route, per the v3 rule. Summary: AF3's INPUT pipeline is clean;
  the leakage that exists is ANALYSIS-LEVEL (routes 4, 5, 6) and DESIGN-LEVEL (route 7).**

  **Route 1 — structures used as input or template: `NONE FOUND`.** Templates are off in every run
  and the paper says so explicitly and for the right reason. Verbatim, p26: "Critically, across all
  generated structures and the embeddings that precede them, no structural templates were used… no
  analysis used template information as inputs **to reduce potential confounds and structural
  invariance.**" Protocol described p25–26 §4.2 and p35–37 §4.10. Checkable.

  **Route 2 — state annotations from a curated database driving templates or alignments:
  `NONE FOUND`.** SCOP (ref [50]), SABmark (ref [49]) and the fold-switch annotation set (ref [23])
  are all used, but only to *index residues for comparison* and to *label the evaluation*. No
  annotation is converted into a template, an alignment filter, or an input feature. The MSAs fed to
  AF3 are unmodified, uniformly perturbed, or absent — never state-selected. Protocol pages: p24–25
  §4.1, p33 §4.8, p35 §4.9.

  **Route 3 — cluster labels derived from known states: `NONE FOUND` as pipeline input, but present
  as an evaluation label.** The nearest-neighbour classifier is scored against SABmark fold-group
  membership (p34 §4.8.4): "the classification was scored correct if that neighbor belonged to the
  same SABmark fold group." The labels score the result; they do not shape the representation. No
  clustering is used to select or filter predictions anywhere.

  **Route 4 — hyperparameters, sweeps, seeds or stopping criteria tuned against known states:
  `PRESENT, MILD, ANALYSIS-LEVEL`.** Three instances, none of which touch AF3 itself:
  - **Model-family selection made on the test metric with no validation split described.** Verbatim,
    p27: "In addition to Ridge regression, we tested Multilayer Perceptrons (MLPs) and Gradient
    Boosting Trees (GBTs). **All methods performed comparably**, and, ultimately, the Ridge
    Regression method was chosen due to its simplicity, interpretability, and regularization
    penalties that minimize overfitting." Only an 80/20 train/test split is ever described (p26); no
    third validation split exists, so "performed comparably" was assessed on the reported test set.
  - **Pooling-strategy selection likewise.** Verbatim, p5: "We systematically evaluated multiple
    pooling strategies (see Methods) and found that **simple mean pooling was optimal for global
    prediction tasks.**" And p26: "these more complex schemes did not majorly or consistently
    outperform simpler representations."
  - **The train/test split is stratified by pTM** (p26) and the patching PCA split is **stratified by
    TM-score decile** (p30) — TM-score is measured against the deposited structure, so the split
    itself is conditioned on an oracle quantity. This is defensible practice (it prevents a skewed
    test set) and the paper says why, but it is conditioning on the reference and should be recorded.
  Mitigations that are real and should be stated alongside: the split is **protein-level, explicitly
  to prevent leakage** (p26: "To strictly prevent data leakage, this split is performed at the whole
  protein level"), the ridge α is **fixed at 1.0 with no sweep**, and pair subsampling uses "a
  deterministic seed for exact reproducibility" (p26). **No per-target tuning and no swept range
  chosen on the evaluation set.**

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had: `PRESENT AND
  PERVASIVE, BY DESIGN`.** Every accuracy claim is TM-score, lDDT or Kabsch RMSD against a deposited
  PDB structure (p33–34 §4.8.2, p37 §4.11 — all scoring via OpenStructure). Examples: SABmark aligned
  RMSD 3.13 Å (p14); fold-switch RMSD to experiment 7.35 Å with MSA vs 10.0 Å without (p16). **This
  is unavoidable for a retrospective evaluation and is not a methodological sin on its own** — but it
  is route 5 and the field asks for it. **A second, subtler variant that matters more:** in several
  arms success is defined against **the model's own control prediction**, not against experiment.
  Verbatim, p31: "all TM-scores were calculated **relative to the unmutated prediction from the
  corresponding condition**… mutated MSA-conditioned structures were compared to the unmutated
  MSA-conditioned baseline, and mutated no-MSA structures were compared to the unmutated no-MSA
  baseline." And p37: "Structural outputs were compared against the **full-MSA control prediction**
  for the same protein… Recall for contact prediction is computed as TP / (TP + FN) **with respect to
  the full-MSA control prediction**." So the phylogenetic-subsampling and MSA-perturbation headline
  numbers (Fig 4A, Fig 5A, Fig 5D) measure **agreement with AF3's own full-MSA output, not
  correctness against experiment.** A "TM-score of 0.92" there means "reproduces what AF3 does with a
  full MSA", which is the right measure for the paper's mechanistic question and the wrong one for
  anyone reading it as accuracy. This is the single most citation-hazardous fact in the paper and is
  repeated in `metrics_reported` and `unresolved`.

  **Route 6 — best/worst model labels assigned against a held reference: `PRESENT, AND IT IS INSIDE
  THE CAUSAL EXPERIMENT`.** The activation-patching source and targets are chosen by accuracy against
  the deposited structure. Verbatim, p30: "we mathematically modulated the representations of target
  proteins drawn strictly from the held-out test set (**comprising the 40 highest and 40 lowest
  TM-score predictions**)". And p31: "We extracted the pair representation from **the highest-accuracy
  protein in the training set** (the source, S) and transplanted it into **low-accuracy, high-entropy
  test proteins** (the targets, T)." The reported effect — that patching sensitivity is three-fold
  larger for poorly predicted targets, `ρ = −0.757` (p6) — is measured across a population whose two
  arms were *defined* by TM-to-PDB. That does not make the entropy change unreal, but it means the
  accurate/poor contrast is a contrast between groups selected on the outcome variable's close
  correlate. Mitigation, and it is a genuine one: **the PCA directions were fit on the training split
  only, stratified across TM deciles, and the patched proteins come strictly from the held-out test
  set** (p30) — so the *directions* are not fit on the patched proteins.

  **Route 7 — design-level oracle use (input conditions or systems chosen because the expected answer
  is already known): `PRESENT, AND CORRECTLY LABELLED AS DESIGN-LEVEL, NOT PIPELINE-LEVEL`.** Three
  instances:
  - SABmark groups were selected *because* fold-level similarity is experimentally validated and
    sequence identity is ≤25% (p24) — the expected answer ("these should look alike internally") is
    declared before the representations are read.
  - The 46 fold-switch pairs were selected *because* both alternative states are deposited, and the
    metamorphic residue ranges are known in advance (p25, p35) — the expected answer ("these regions
    should differ") is likewise declared first.
  - The Novel/Similar split is constructed from known homology to the presumed training set (p24).
  **This is normal, sound benchmark design and is not equivalent to feeding AF3 the answer.** It is
  recorded because v3 route 7 asks for it and because the fold-switching claim in particular is a
  claim about a set chosen for having the property being tested.

  **Net verdict, in one line:** *AlphaFold 3 received nothing but sequence and (sometimes) an MSA —
  no template, no state annotation, no structural hint of any kind — so the input pipeline is one of
  the cleanest in this corpus; the leakage that exists is entirely in the analysis layer (probe/model
  selection on the test split, and selection of the causal experiment's proteins by TM-to-PDB) and in
  ordinary benchmark design.*

- **prospective**: **partial.**
  - *Prospective in memorisation terms:* every one of the 400 primary proteins was deposited **after
    the AF3 training cutoff of 30 Sep 2021** (p5, p24), so the predictions are genuinely
    out-of-distribution in time. Verbatim, p5: "**Crucially, all proteins were deposited after
    September 30, 2021, the AlphaFold 3 training cutoff, ensuring that even the Similar set is
    temporally out-of-distribution.**"
  - *Retrospective in evaluation:* nothing is predicted before its structure exists; every claim is
    scored against a structure already in the PDB, and the two secondary datasets **predate the
    cutoff entirely** — the paper says so and turns it into an argument, p14: "This performance likely
    reflects a combination of MSA support and, **given that all SABmark proteins predate the
    AlphaFold 3 training cutoff, possible prior exposure to these folds.**"
  - *Retrospective in the causal arm:* patching targets selected by TM-to-PDB (route 6).
  Follows from `oracle_leakage`, not from the authors' own framing. `prospective` is **not** applied
  as a tag.
- **state_metric**: **`RMSD-to-reference` + `continuous coordinate` (dual, per the v3 rule).**
  - The conformational question ("did AF3 produce the right state at a metamorphic site?") is
    answered **only** by **Kabsch Cα RMSD at the annotated fold-switching indices**, against the
    experimental PDB structure and against the other predicted state (p35 §4.9, p33–34 §4.8.2).
  - The representational question is answered by **cosine similarity/distance** on flattened
    sub-tensors, and the uncertainty question by **distogram Shannon entropy** and **KL divergence** —
    all continuous coordinates.
  - **Thresholds: there is no binary state predicate anywhere in this paper.** No RMSD cutoff, no
    identity criterion, no "correct state" definition is ever stated. The claim that the model
    "collapses metamorphic sites to a single fold" is supported by a comparison of means (2.02 Å for
    predicted-vs-predicted fold-switch regions against 9.25 Å and 10.3 Å controls, p15) with **no
    threshold and no per-pair success rate**. The nearest thing to a per-domain predicate is Fig 3D/F's
    "MSA closer / no-MSA closer / tied" trichotomy (63 / 27 / 2 of 92 domains), which is a
    *comparison between two predictions*, not a correctness predicate.
  - The only stated numeric thresholds anywhere are structural-feature definitions, not state calls:
    8.0 Å for a Cα–Cα contact (p27), 10 Å neighbourhood for the burial count with k = 9 nearest
    neighbours (p27), 1.4 Å SASA probe radius (p27), sequence-separation bins 1–5 / 6–11 / 12–23 /
    ≥24 (p29), and 95% cumulative variance for effective dimensionality (p28). **Justification for
    any of these: NOT REPORTED** — each is asserted as standard.
- **metric_saturation**: **YES, in three places, and the authors name one of them themselves.**
  Numeric saturation only; figure-level axis problems are in `hides` on the relevant figure rows.
  1. **Explicit, author-acknowledged ceiling in the MSA-conditioned self-prediction arm.** Verbatim,
     p8: "By contrast, the MSA-conditioned embeddings show low self-predictive power for these same
     quantities—**not due to representational failure, but as an artifact of limited dynamic range.
     MSA-conditioned predictions are compressed into a narrow, high-confidence distribution whose low
     variance renders regression effectively uninformative, regardless of the underlying signal.**"
     This is a clean statement that R² is uninformative wherever AF3 is confident, and it cuts
     against the paper's own §2.2 headline (pair R² = 0.86 for pTM at C_N) unless the two arms are
     kept apart. Cross-reference: no figure shows the two dynamic ranges side by side.
  2. **Cosine similarity ceilings at checkpoints A and B in the SABmark arm** (Fig 3A, p13): within-
     fold, between-fold and null-baseline bars all sit at ≈0.95–1.00 at A and B under both
     conditions, so the metric cannot separate anything there. The paper reads this as "Checkpoints A
     and B remain comparatively invariant" (p14) — which is a statement about the representation, but
     is equally consistent with the metric being saturated. **The paper does not distinguish the two
     readings.** Cross-reference figure row 3A.
  3. **Cosine distance floors in the mutation arm** (Fig 2A–B, p10): every cell for checkpoints A and
     B, and every cell for all three single-representation checkpoints, reads 0.000–0.036 at every
     mutation level up to 80% under both MSA conditions. The conclusion "No meaningful drift is
     observed at Checkpoints A or B" (p11) rests on a metric pinned at its floor across seven rows.
     Cross-reference figure row 2A-B.
- **directional_control**: **NOT APPLICABLE — the paper contains no mechanism for instructing which
  conformational state to produce, and does not claim one.** No partner, ligand, nanobody, peptide,
  state-annotated template, state-filtered MSA or seed handle exists anywhere. Recorded here rather
  than left blank because the near-miss is important for this corpus: **the activation-patching
  experiment is a directional handle on *certainty*, not on *state*** — shifting PC1 raises distogram
  entropy, shifting PC2 lowers it, and transplantation lowers it hard (−0.268), but nothing in the
  paper steers the model toward one fold rather than another, and the readout never reaches
  coordinates. The authors put conformational steering explicitly in future work, verbatim, p22:
  "whether direct intervention on internal representations can induce structures the model would
  otherwise suppress due to evolutionary precedent or data scarcity" — "a question the framework
  makes tractable but that this study does not resolve."
- **anti_memorization_design**: **YES, and it is one of the stronger designs in this corpus.**
  n = 400, split 200 Novel / 200 Similar. Cutoff defined by the AF3 training date, **30 September
  2021**, with three simultaneous criteria (p24 §4.1): (i) *all* 400 deposited after that date; (ii)
  Novel = no ≥30% sequence homology to any PDB entry released on or before that date, Similar = ≥30%
  homology to at least one; (iii) **no two proteins in the 400 share ≥30% identity with each other**,
  so within-set redundancy is controlled too. Verbatim, p24: "Importantly, all proteins in the
  dataset were released after September 30, 2021, and no two proteins share 30% or more sequence
  similarity, ensuring minimal redundancy and that none were present in AlphaFold 3's training set."
  **Counterweight to record: the two secondary datasets have no such design.** SABmark and the
  fold-switchers predate the cutoff and are acknowledged as possibly seen in training (p14).
- **anti_memorization_control**: **RUN AND ANALYSED, and well powered (n = 200 per arm).** Not merely
  a held-out set that exists. Verbatim, p9: "Finally, we separated the Similar and Novel cohorts to
  test whether training-set membership modulates any of these effects. Across all biophysical
  probes—secondary structure, SASA, burial depth, contact prediction, and pairwise distance—
  **performance differences between the two groups were negligible at every checkpoint**, despite
  Similar proteins being supported by MSAs approximately twice as deep (mean depth 9,513 vs. 4,587).
  AlphaFold 3 therefore encodes biophysical information in a manner that is largely invariant to
  training-set familiarity." **Not `UNPOWERED`.** A second, different memorisation control is run as
  a by-product: the no-MSA collapse is demonstrated on SABmark and fold-switch proteins that
  *probably were* in training, and the paper uses that deliberately — p16: "That this degradation
  occurs **even for proteins likely familiar from training** indicates that the model's structural
  prior is organized around MSA-derived evolutionary context, not raw sequence."
  **Weaknesses to carry with the citation:** (i) "negligible differences" is asserted without a test
  statistic, effect size, CI or per-checkpoint table — there is **no figure panel and no number** for
  the Novel-vs-Similar comparison anywhere in the paper, only the sentence above; (ii) the depth
  confound runs the wrong way for a clean read (Similar proteins have ~2× deeper MSAs, so "no
  difference" pools a familiarity effect against a depth effect that could cancel); (iii) the ≥30%
  homology criterion is applied to the *deposited PDB* rather than to AF3's actual (undisclosed)
  training set, which the paper acknowledges by writing "**plausibly** present in the AlphaFold 3
  training set" (p5).
- **controls_run**: **21 rows. This is the most reusable content in the note; the paper's control
  design is genuinely good and its one gap is glaring.**

  | control | what it rules out | page |
  |---|---|---|
  | **No-MSA arm** run on all 400 monomers, all SABmark proteins, all 46 fold-switch pairs, and every mutation level | That the effects attributed to evolutionary context are actually properties of sequence alone; establishes the lower baseline for every other arm | p8, p14–16, p31 |
  | **Similar vs Novel cohorts** (200 / 200) compared across all five biophysical probes at all four checkpoints | Training-set familiarity as the driver of encoding quality | p9, p24 |
  | **Post-cutoff deposition (all 400 after 30 Sep 2021)** | Memorisation of the primary benchmark; makes even the "Similar" arm temporally OOD | p5, p24 |
  | **Sequence-separation-only probe** (`\|i−j\|` as sole feature, R² = 0.239) | That pair-representation distance decodability is just a restatement of chain topology | p7, p30, Fig 1L |
  | **Amino-acid identity re-identification probe** ("near-perfect accuracy at all checkpoints") | Broken extraction / degenerate representations; confirms "the probes are operating on a faithful encoding" | p7 |
  | **Isolated pair probe vs context-augmented probe** (`p_ij` alone vs + row/col means + `\|i−j\|`) | That decodability gains come from hand-built local context rather than the pair tensor | p7, p30 |
  | **Single-only / pair-only / joint ridge triplet** (unique-information decomposition) | That the pair track's advantage is duplicated information rather than unique content | p7, p28 |
  | **Matched-reference TM-scores under mutation** (mutated-no-MSA scored against unmutated-no-MSA, not against the MSA control) | Compounding the MSA-deprivation penalty into the measured mutational sensitivity | p31 |
  | **Protein-level (not residue-level) 80/20 split, stratified by pTM** | Residues of one protein appearing in both train and test; a test set skewed in structural quality | p26 |
  | **SABmark same-protein non-aligned-residue null** (K random unaligned residues from the same pair, averaged over **30** iterations) | That aligned-region similarity is a generic property of any two residue sets from the same proteins | p14, p33 |
  | **SABmark unrelated-monomer null** (random pairs from the 400-set, K random residues, averaged over **20** iterations) | Baseline similarity of structural noise; sets the floor for cosine and RMSD | p14, p33 |
  | **Fold-switching internal control region** `I_ctrl` (same length K, non-metamorphic, non-overlapping, same proteins) | That fold-switch-region behaviour is a generic property of any region of those proteins | p15, p35 |
  | **Fold-switching external null** (random length-K regions from unrelated 400-set proteins) | Stochastic representational and structural similarity at matched length | p15, p35 |
  | **Column shuffling** at 7 rates (destroys co-evolutionary coupling; **preserves per-column marginals and depth**) | That the MSA works through per-position composition or through sheer depth | p16, p35–36 |
  | **Row subsampling** at 7 rates (**preserves coupling**, reduces depth) | That the MSA works through depth; separates depth from integrity — run as the complement of the above | p16, p36 |
  | **Fake-MSA injection** — sequences from 139 *unrelated* proteins' MSAs, trimmed to the target's aligned length, A3M format preserved, depths 1/10/20/50/100 | **That the effect of an MSA is an artefact of alignment format, tensor shape or depth rather than of evolutionary relatedness.** The paper's strongest control; the result is a flat null at every depth and every metric | p19, p37, Fig 5C |
  | **Random tier at matched depth** (uniform sampling from all homolog rows, mean identity ≈0.42 ± 0.14) | That tier effects are depth effects; provides a matched-depth diversity control against which `similar` fails | p18, p37 |
  | **Full-MSA control prediction + no-MSA lower baseline attached to every subsampling arm** | Un-anchored perturbation results; every Fig 4/5 number is bracketed by both ends | p37 |
  | **PCA fit on the training split only, stratified across ten TM-score deciles; patched proteins drawn strictly from the held-out test set** | That the "causal" PC directions were fit on the very proteins they are then applied to | p30 |
  | **Alternative regressors (MLP, GBT) and alternative pooling (mean+std, context-augmented)** | That conclusions are an artefact of linear-probe capacity or of the pooling choice | p26, p27 |
  | **Nested 30–60%-identity subsampling on 183 of the 200 Novel proteins** | That the "diversity beats depth" principle is specific to the 61 qualifying proteins | p21–22 |
  | ⚠️ **Random-unit-vector patching baseline — DESIGNED, DESCRIBED IN METHODS, RESULT NEVER REPORTED** | *Would have ruled out* that any perturbation of matched magnitude moves distogram entropy, i.e. that the effect is about the PC directions at all | designed p31; **no result anywhere in text or figures** |

  **The most important missing control, stated plainly.** The last row is not a control the authors
  failed to think of — they specified it. Verbatim, p31: "To ensure these effects are uniquely tied
  to the learned PC axes, **identical shifts were performed using random unit vectors of matched
  magnitude √λ_k as a noise baseline.**" **No number, no panel, no sentence reports its outcome.**
  Fig 1H (p4) shows only the five PC rows. Without it, the entire causal claim — the paper's only
  causal claim — is unfalsified against the null that pushing a linear head's input in *any*
  direction of comparable magnitude moves its output entropy by a comparable amount. Given the
  effect sizes involved (|ΔH| ≤ 0.02 bits on a 64-bin distribution), this is not a pedantic
  objection.

  **Other controls that are absent rather than unreported, in rough order of importance:**
  1. **No structure-level readout of any intervention.** Patched representations go to the distogram
     head and stop (p31). No coordinates, no TM-score, no pLDDT after patching. The claim that "AlphaFold 3's latent
     geometry is not merely descriptive but manipulable" (p22) is demonstrated on an auxiliary head.
  2. **No probe control task / shuffled-label baseline.** Standard practice in the probing literature
     is to bound probe capacity by training the same probe on random labels or on random/untrained
     representations. Neither exists here, so absolute R² values (0.86 for pTM, 0.474 for distance,
     0.09 for SASA) have no capacity floor other than the single `|i−j|` baseline in Fig 1L. The
     amino-acid re-identification probe is a *faithfulness* check, not a capacity control.
  3. **No run-to-run variance anywhere.** One diffusion sample per prediction (p26), "identical
     hyperparameters and random seeds to the control" for perturbations (p35). No seed replicates, no
     error bars on any TM-score, no CI on any correlation. Every "significant at p < 0.05" is a
     blanket statement (p37: "Unless otherwise noted, all statistical tests, correlations, and
     regression analyses reported are significant at p < 0.05") with no per-claim test named.
  4. **No MSA-regeneration arm under mutation** — the paper cites ref [21] for it (p31, p23) rather
     than running it, then builds an argument on top of that borrowed result.
  5. **No second backbone.** Every conclusion about "the Pairformer" is a conclusion about one
     model's weights; AF2's Evoformer and the Boltz/Chai/Protenix trunks are never tested, so
     architectural generality is asserted by analogy in the Discussion only.
  6. **No multimer, ligand or nucleic-acid arm**, despite AF3 being a co-folding model and the
     Discussion extrapolating to complexes (p23).
  7. **No positive control for the fold-switching arm** — no case where AF3 is known to produce both
     states, so the "collapse" result has no upper reference.
- **confidence_as_discriminator**: **Used descriptively and as a probe target; NOT used to judge
  conformational correctness, and NOT validated for that use. The tag is therefore declined.** What
  is actually done:
  - pTM is a **probe target** for representational self-consistency (R² 0.34 → 0.86, p5) and a
    **stratification variable** for the train/test split (p26).
  - TM-score deciles stratify the patching PCA split (p30).
  - Distogram entropy is used throughout as a *representation-level* uncertainty measure, and its
    displacement (KL divergence) is shown to correlate with realised structural loss — the closest
    thing to a validated confidence claim in the paper. Verbatim, p9: "KL-divergence correlates
    strongly with the corresponding change in TM-score relative to the PDB ground truth (Pearson
    r ≈ 0.72 across all sequence-separation bins), directly linking the information-theoretic
    displacement of the model's internal distance distribution to realized structural collapse in 3D
    space. **KL-divergence thus serves as a mechanistic bridge between latent uncertainty and
    downstream structural failure.**"
  - At fold-switching sites, entropy (2.25 vs 1.39) and pLDDT (77.4 vs 82.3) are reported as evidence
    that "the model is aware that something is geometrically unusual at these sites, **even while
    failing to resolve the alternative conformation**" (p16) — i.e. confidence flags anomaly but is
    explicitly stated *not* to discriminate the correct state.
  - The Discussion proposes representational uncertainty as a *better* future alternative to scalar
    confidence, p22: "These representations may also provide richer uncertainty quantification than
    scalar metrics such as pLDDT or pTM, as their high-dimensional geometry encodes early signals of
    representational failure before it manifests in predicted coordinates." That is a proposal, not a
    validated result.
  - **The pLDDT gap of 4.9 points (77.4 vs 82.3) carries no dispersion, no n, and no test**, and is
    the only pLDDT number in the paper.

## D. Claims

- **central_conclusion**: AlphaFold 3's pair representation, not its single representation, is the
  geometric substrate of its structural reasoning: across four checkpoints the pair track compresses
  a diffuse co-evolutionary signal (effective dimensionality 16 → 32 → 19 → 17) into a compact latent
  space in which distances, contacts, secondary structure and the model's own confidence become
  progressively linearly decodable, and in which shifting the dominant principal directions causally
  changes the distogram's entropy. What drives all of it is the *presence* of evolutionary context
  rather than its quantity or integrity: AF3 tolerates 99% MSA removal and 40% column shuffling
  almost intact, but collapses when the MSA is removed entirely (TM 0.936 → 0.539) — even for
  proteins it has likely seen — and a handful of *sufficiently divergent* homologs restores most of
  the accuracy while near-identical ones restore almost none, and format-preserving but evolutionarily
  unrelated sequences restore nothing at all. The authors' conclusion is that AF3 is best understood
  as a very sensitive fold-recognition system that uses the MSA to locate structurally constrained
  positions and thereby activate structural priors stored in its weights, rather than as a model that
  reasons from sequence to structure by physics.
- **necessity_claims**: **Verbatim + page. Recorded in full because these are the load-bearing
  sentences.**

  *On evolutionary / co-evolutionary information being the dominant signal:*
  1. p1 (abstract): "we show that the model **relies predominantly on comparative evolutionary
     context rather than raw sequence**, and that a few divergent homologs contribute more to
     accurate prediction than many near-identical ones."
  2. p1 (abstract): "accuracy is preserved even under heavily degraded multiple sequence alignments
     (MSAs) but **collapses when MSAs are removed, regardless of sequence familiarity or training-set
     membership. The model depends on phylogenetic diversity, not MSA depth**: a few sufficiently
     divergent sequences largely restore accuracy and representational coherence, whereas
     near-identical sequences do not, and evolutionarily unrelated sequences fail entirely even when
     the alignment format is preserved."
  3. p2 (abstract cont.): "**AlphaFold 3 therefore uses the MSA to locate structurally constrained
     positions and activate structural priors stored in its weights. In other words, AlphaFold 3 is a
     very sensitive fold recognition algorithm.**"
  4. p12: "**The MSA is not merely buffering local sequence changes at the input stage. It is what
     allows the Pairformer to sustain a coherent geometric hypothesis at all. Without it, the sequence
     carries insufficient information to anchor structural reasoning, and even modest perturbations
     are enough to collapse the representational space entirely.**"
  5. p15: "**The failure to recover even canonical fold overlaps without an MSA, regardless of
     potential training familiarity, establishes co-evolutionary information as a dominant substrate
     of the model's structural reasoning.**"
  6. p16: "That this degradation occurs even for proteins likely familiar from training indicates
     that **the model's structural prior is organized around MSA-derived evolutionary context, not raw
     sequence**."
  7. p19: "**MSA existence alone is insufficient, and the signal AlphaFold 3 extracts from the MSA is
     genuinely evolutionary. The model is not reading alignment-shaped input.**"
  8. p19: "**Long-range contacts are precisely those that cannot be inferred from local sequence
     patterns alone and require comparative evolutionary information.** The model's ability to recover
     them with as few as one dissimilar or randomly selected sequence supports the view that
     AlphaFold 3 has internalized co-evolutionary constraints during training and **requires only a
     minimal evolutionary signal to activate them at inference time.**"
  9. p19: "The fake MSA condition produces negligible or negative delta recall, **confirming that
     evolutionary relevance—not alignment format or depth—is what drives contact recovery.**"
  10. p21: "**This failure is not a matter of insufficient depth or alignment format: it reflects a
      fundamental absence of the evolutionary contrast needed to distinguish structurally essential
      from permissive positions.**"
  11. p21: "**structural accuracy does not require deep alignments, but it does require sequences
      that have diverged sufficiently to expose which positions are truly constrained.**"
  12. p22: "the internal representation analysis developed here reveals that **MSA absence does not
      merely reduce structural accuracy: it destroys internal representational coherence entirely.**"
  13. p23: "**Sequence alone, regardless of similarity to training examples, is not sufficient.** The
      model appears to have learned a mapping from MSA-derived motifs—perhaps coupled with
      sequence—to structure, and that mapping dominates."
  14. p23: "**The model does not require deep or pristine alignments—only sufficient diversity to
      anchor the Pairformer's geometric reasoning. Indeed, as few as 5–10 evolutionarily divergent
      sequences relative to the query may suffice.**"

  *On where physics or geometry does — and does not — enter. These are the sentences to quote when
  contrasting an evolution-driven account with a physics-driven one:*
  15. p23: "**AlphaFold 3 is immensely powerful, but its power is bounded by our ability to construct
      informative MSAs. Whatever physical understanding the model has acquired is overwhelmingly
      mediated by evolutionary statistics and their encoded echo rather than autonomous biophysical
      reasoning.**"
  16. p23: "**This is a working solution to the protein structure prediction problem, but it does not
      reflect how proteins actually fold. When a protein folds in nature, it does not query an
      evolutionary database. It follows biophysical principles and minimizes free energy. The folding
      process is governed by the physics of the polypeptide chain in its environment, not by the
      statistical preferences of its homologs. A model that recovers structure primarily through
      evolutionary context and the implied similar fold is solving a related but distinct problem,
      and solving it brilliantly is not the same as understanding it.**"
  17. p24: "**a model that genuinely reasons from sequence to structure would not need evolutionary
      scaffolding to reach that geometry—it would reach it from first principles.**"
  18. p24: "The protein structure prediction problem, as historically defined, has been largely
      solved. **The deeper problem—a physically grounded, genuinely generalizable model of how
      sequence determines structure—remains open.**"
  19. p2 (intro): "models without genuine biophysical grounding are unlikely to generalize to novel
      protein families, engineered sequences, or proteins with substantial mutations relative to
      characterized homologs."

  *On where geometry is located inside the network — the mechanistic claims proper:*
  20. p8: "**The pair representation carries the burden of geometry**, as it encodes relational
      structure between residues and is progressively sculpted, through the MSA module and Pairformer,
      into a linearly accessible representation of three-dimensional protein structure. **It is this
      pair manifold, not the single channel, that constitutes the primary geometric substrate of
      AlphaFold 3's structural reasoning.**"
  21. p11: "The uncertainty introduced by mutation is not expressed during sequence initialization or
      during the immediate integration of MSA information—**it emerges specifically within the
      Pairformer, where residue-residue geometry is actively reconciled into a fold hypothesis.**"
  22. p14: "**It is only after residue-residue geometry is iteratively reconciled in the Pairformer
      that the latent space recovers the experimentally validated fold overlap—further evidence that
      the Pairformer is the primary structural conditioner within AlphaFold 3.**"
  23. p12: "**the model's robustness to deleterious sequence perturbation is embedded deeply within
      its pair-level geometric reasoning, not a surface property of the final predicted structure.**"
  24. p16: "**Removing the MSA does not make the model more conformationally flexible—it makes it
      less correct.**"
  25. p5–6: "**The Pairformer seems not to merely refine the MSA-derived representation—it reorganizes
      the entire embedding manifold around the notion of fold quality.**"

  *On the causal claim specifically — quoted here because its exact wording is what a citation must
  not exceed:*
  26. p1 (abstract): "the Pairformer compresses a diffuse co-evolutionary manifold into a compact
      latent space in which biophysical features are linearly encoded and **predicted confidence is
      causally manipulable in the representational geometry.**" *(Note the scope: "predicted
      confidence", not predicted structure.)*
  27. p6: "**The dominant principal components prove to be causally active.**"
  28. p6–7: "**The internal geometry encoding a successful fold can therefore be transferred between
      unrelated proteins and still impose structural certainty on the downstream distribution.**"
      *(Again: the downstream **distribution**, i.e. the distogram — not the structure.)*
  29. p22: "**we demonstrate that AlphaFold 3's latent geometry is not merely descriptive but
      manipulable.** This raises a question the framework makes tractable but that this study does not
      resolve: whether direct intervention on internal representations can induce structures the
      model would otherwise suppress due to evolutionary precedent or data scarcity."
  30. p30 (Methods, the sentence that bounds all of the above): "**Unlike other structural modules,
      the AlphaFold 3 distogram head acts as a direct, transparent linear probe.**"

- **novelty_claims**: **Verbatim + page.**
  1. p1 (abstract): "Here, **in the first systematic mechanistic interpretability analysis of
     AlphaFold 3**, we show that the model relies predominantly on comparative evolutionary context
     rather than raw sequence".
  2. p3: "Mechanistic interpretability— the systematic analysis of what information is encoded in a
     model's internal representations, how that information is organized, and whether it is causally
     upstream of model outputs—has proven powerful for understanding large language models and
     biological sequence models such as ESM, **but has not yet been applied systematically to
     structure prediction models like AlphaFold 3.**"
  3. p22: "**This work represents, to our knowledge, the first systematic mechanistic interpretability
     study of AlphaFold 3's internal representations. Prior examinations of AlphaFold-like systems
     have largely remained at the phenomenological level, characterizing outputs without probing the
     internal geometry that produces them.**"
  4. p2: "This phenomenon [mutational invariance] **has been documented at the level of predicted
     coordinates, but its representational origins—whether the invariance is embedded in the model's
     internal geometry or emerges only at the final structure module—have not been examined.**"
  5. p3: "The internal representations of AlphaFold 3—its single residue-level channels and its
     pairwise interaction channels—carry the information that determines the predicted fold, but
     **what exactly they encode, how they evolve through the network, and what role the multiple
     sequence alignment (MSA) plays in shaping them has remained opaque.**"
  6. p22: "**That this refinement follows a consistent, compressive trajectory into a lower-dimensional
     effective feature space suggests that substantial information remains to be extracted from these
     internal states.**"
  7. p14: "Because SABmark includes residue-level structural alignments, **we could ask a sharper
     question than simple structure-level agreement: do AlphaFold 3's internal representations
     recapitulate experimentally validated structural correspondence even when sequence similarity is
     absent?**"
  **Priority note for the corpus:** claim 1/3 is a first-in-kind claim about **AlphaFold 3**
  specifically. It does not claim priority over interpretability work on AF2, on Boltz, or on protein
  language models — ESM SAE work is cited at refs [27–29] and acknowledged as prior art.
- **stated_limits**: the authors' own, all with pages.
  - **Probe ceilings may be a probe artefact, not an absence of information.** p7: "The modest
    absolute values for some features, particularly SASA, are not unexpected. **There is no a priori
    reason to expect AlphaFold 3 to organize these properties into linearly separable axes—it is
    entirely plausible that they exist as non-linear superpositions within the representation that a
    linear probe cannot recover.** What is notable is not the ceiling of performance but its
    consistency".
  - **Low R² in the MSA arm is a dynamic-range artefact, not representational failure.** p8 (quoted
    in full under `metric_saturation`).
  - **The collapse interpretation is offered conservatively.** p11: "**While this pattern is
    consistent with a collapse-like behavior under mutation, it is more conservatively interpreted as
    indicating that the model's representations become progressively less discriminative as sequence
    perturbations increase, rather than definitively establishing a discrete failure mode.**"
  - **Pooling destroys geometric detail and is a compromise.** p25: "**While pooling inevitably
    discards fine grained pairwise geometric detail, it is necessary for length-invariant comparison
    across diverse datasets**; other alternatives, such as padding, truncation, or length-matching,
    introduce greater structural artifacts." (Mitigated: unpooled tensors are used wherever lengths
    match — mutation, SABmark, fold-switching.)
  - **SABmark performance is confounded by possible training exposure.** p14: "This performance
    likely reflects a combination of MSA support and, **given that all SABmark proteins predate the
    AlphaFold 3 training cutoff, possible prior exposure to these folds.**"
  - **The causal question is left open.** p22, quoted above as necessity claim 29.
  - **Biophysical labels exist only for resolved residues.** p27: "Biophysical labels were available
    only for structurally resolved residues, meaning that analyses involving PDB-derived features
    were restricted to this subset of residues in each protein."
  - **Only one diffusion sample per prediction, for compute.** p26.
  - **Training-set membership is inferred, not known.** p5: proteins with "less than 30% sequence
    homology to any protein **plausibly** present in the AlphaFold 3 training set".
  - Implicit but stated: multimers untested and expected worse (p23).
- **stance**: **`precedent` + `contrast` — both, joined, and PROVISIONAL (the user's call, per schema
  D).**
  - **`precedent` on findings.** This is the mechanistic account that sits underneath any
    trunk-level-intervention paper in this corpus. It establishes, on AF3 specifically, that (i) the
    **pair track at C_N** is where geometry lives and is what conditions the diffusion module, (ii)
    that manifold is low-dimensional (effective rank ~15–17 with MSA), (iii) its dominant principal
    directions move a downstream head's output when shifted, and (iv) a whole representation can be
    transplanted between unrelated proteins and still impose certainty. Anyone arguing that
    intervening on the AF3 trunk *should* work has here the closest thing to a mechanistic
    justification, plus a ready-made quantitative frame (checkpoints, effective rank, distogram
    entropy, cosine drift) for describing what an intervention does.
  - **`contrast` on rigour, and specifically on the causal claim.** The abstract says confidence is
    "causally manipulable in the representational geometry" and the Discussion says (p22) that "AlphaFold 3's latent
    geometry is not merely descriptive but manipulable" — but no patched representation ever reaches
    the diffusion module, no coordinate is ever measured after an intervention, and the
    random-direction noise baseline the Methods specify is never reported. A paper that *does* run
    trunk interventions through to structure has a clean and precise contrast to draw here, and it is
    a contrast about evidentiary reach, not about correctness. Secondary contrast points: no probe
    control task; TM-scores in the perturbation arms are computed against AF3's own control
    prediction rather than experiment; the headline diversity result rests on 61 proteins; no error
    bars anywhere.
  - `threat` considered and rejected: the paper competes with no method in this corpus and proposes
    none. `background` considered: too weak — the findings are directly load-bearing, not context.
    `negative-result` is applied as a *tag* (the fold-switch collapse and the fake-MSA null are real
    negative results) without displacing the two stances above.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | pTM self-prediction R², **pair** rep, ridge | 0.34 (A) → **0.86** (C_N) | R² | AF3's own pTM, 80/20 protein-level split, MSA condition | p5 |
  | pTM self-prediction R², **no-MSA** embeddings | 0.822 | R² | AF3's own pTM | p8 |
  | TM-score self-prediction R², **no-MSA** embeddings | 0.845 | R² | TM-score to PDB | p8 |
  | Mean TM-score, **full MSA**, 400 monomers | **0.9363** (std 0.0987) | TM-score | experimental PDB | p8 |
  | Mean TM-score, **no MSA**, 400 monomers | **0.5388** (std 0.2333) | TM-score | experimental PDB | p8 |
  | Effective dimensionality (PCs for 95% var), pair, **MSA** | A **16** → B **32** → C₁ **19** → C_N **17** | count | — | p6, Fig 1B |
  | Effective dimensionality, pair, **no MSA** | A **17** → B **18** → C₁ **26** → C_N **25** | count | — | Fig 1B, p4 |
  | Effective **rank** (entropy-based), C_N pair, SABmark | **15.2** (MSA) → **24.2** (no MSA) | rank | — | p15 |
  | PC1 vs sequence length, checkpoint A | Pearson **−0.917**, Spearman **−0.943** | r / ρ | — | p6, Fig 1F |
  | PC1 vs sequence length, checkpoint C_N | Pearson **−0.77**, Spearman **−0.80** | r / ρ | — | p6, Fig 1G |
  | PC1 vs pTM, checkpoint C_N | Spearman **−0.71** | ρ | — | p6, Fig 1G |
  | **Patching:** ΔH from +1σ shift along PC1, accurate targets | **+0.0044** | bits (distogram entropy) | unpatched same protein | p6 |
  | **Patching:** ΔH from +1σ shift along PC1, poor targets | **+0.0133** | bits | unpatched same protein | p6 |
  | **Patching:** ΔH from +1σ shift along PC1, overall mean | **+0.0088** | bits | unpatched | p6, Fig 1H |
  | **Patching:** ΔH vs original predicted confidence | Spearman **ρ = −0.757** | ρ | — | p6 |
  | **Patching:** PC1 full response row (Fig 1H) | −2σ **−0.0133**, −1σ **−0.0074**, +1σ **+0.0088**, +2σ **+0.0192** | bits | unpatched | Fig 1H, p4 |
  | **Patching:** PC2 response row (Fig 1H) | −2σ **+0.0198**, −1σ **+0.0097**, +1σ **−0.0094**, +2σ **−0.0184** | bits | unpatched | Fig 1H, p4 |
  | **Patching:** text's PC2 summary | "**uniformly reduces distogram entropy by −0.0198**" | bits | unpatched | p6 — **does not match Fig 1H; see `unresolved`** |
  | **Patching:** cross-protein transplant (source TM = 0.999) | mean ΔH̄ = **−0.268** | bits | unpatched low-accuracy targets | p6 |
  | Cα–Cα distance decodability R², **pair only** | 0.311 (A) → **0.474** (C_N) | R² | PDB Cα–Cα distance | p7, Fig 1L |
  | Cα–Cα distance decodability R², **pair + local context** | → **0.504** (C_N) | R² | PDB Cα–Cα distance | p7, Fig 1L |
  | Cα–Cα distance decodability R², **sequence-separation baseline** | **0.239** | R² | PDB Cα–Cα distance | Fig 1L, p4 |
  | Cα–Cα contact prediction, balanced accuracy | 0.642 → **0.703** | balanced accuracy | 8 Å PDB contacts | p7 |
  | Secondary structure probe accuracy | 0.43 (B) → **0.57** (C_N) | accuracy | mmCIF/DSSP labels | p7 |
  | SASA probe R² | 0.02 → **0.09** | R² | Shrake–Rupley SASA | p7 |
  | Burial depth probe R² | 0.05 → **0.15** | R² | 9-NN packing score | p7 |
  | Amino-acid re-identification, single rep | "near-perfect" at **all** checkpoints | accuracy | input sequence | p7 — **no number given** |
  | KL(MSA ‖ no-MSA) vs ΔTM-score | Pearson **r ≈ 0.72** across all separation bins | r | TM-score to PDB | p9 |
  | Distogram entropy gain from MSA, by separation bin (Fig 1E, difference bars) | seq-local(1–5) **0.93**, secondary(6–11) **1.32**, medium(12–23) **1.26**, long-range(≥24) **0.73** | bits | no-MSA − MSA | Fig 1E, p4 |
  | Mean MSA depth, **Similar** vs **Novel** | **9,513** vs **4,587** | sequences | — | p9 |
  | Novel-vs-Similar probe difference | "**negligible at every checkpoint**" | — | — | p9 — **no number, no test, no panel** |
  | Mutation: cosine distance at C_N pair, 70% load, MSA | ≈ **0.731** | cosine distance | unmutated same protein | p9 |
  | Mutation: cosine distance vs TM divergence, MSA | Pearson **−0.948**, Spearman **−0.899** | r / ρ | — | p11, Fig 2C |
  | Mutation: same correlation, **no MSA** | Pearson **−0.338** | r | — | Fig 2D, p10 |
  | Mutation: drift-vector directional coherence | mean resultant length **R̄ = 0.901** (max 1.0) | — | — | p11 |
  | Mutation: drift loading on PCs | PC1 **0.767**, PC2 **0.325**, PC3 **0.239** (mean abs component) | — | — | p11 |
  | Mutation: cosine shift at 80%, initial TM < 0.5 vs ≥ 0.9 | **0.548** vs **0.763** | cosine distance | unmutated | p11 |
  | Mutation resistance correlates | length ρ = **−0.516**; mean SASA ρ = **0.338**; contact density ρ = **0.501** | ρ | collapse onset | p12 |
  | Mutation, **no MSA**: cosine distance at C_N, 10% load | **0.271** | cosine distance | unmutated no-MSA | p12 |
  | Mutation, **MSA**: TM-score at 40% load | ≈ **0.70** | TM-score | unmutated MSA prediction | p12 |
  | SABmark RMSD, **MSA**: aligned / non-aligned / unrelated | **3.13** / **21.66** / **23.15** | Å (Kabsch Cα) | between the two predicted structures at matched indices | p14, Fig 3C |
  | SABmark RMSD, **no MSA**: aligned / non-aligned / unrelated | **12.80** / **23.18** / **24.45** | Å | as above | p15, Fig 3C |
  | SABmark nearest-neighbour fold classification, **MSA** | A **0.500**, B **0.670**, C₁ **0.600**, C_N **0.630** | accuracy | SCOP fold group | Fig 3B, p13 |
  | SABmark nearest-neighbour fold classification, **no MSA** | A **0.460**, B **0.530**, C₁ **0.590**, C_N **0.570** | accuracy | SCOP fold group | Fig 3B, p13 |
  | Fold-switch: RMSD between the two **predicted** switching regions, MSA | **2.02** | Å | prediction vs prediction | p15 |
  | Fold-switch: within-pair control / random-monomer control | **9.25** / **10.3** | Å | — | p15 |
  | Fold-switch: RMSD of prediction to **experimental** structure | **7.35** (MSA) → **10.0** (no MSA) | Å | experimental PDB | p16 |
  | Fold-switch: per-domain winner count | MSA closer **63**, no-MSA closer **27**, tied **2** (n = **92** domains); mean Δ = **+2.869 Å** | count / Å | experimental PDB | Fig 3D/F, p13 |
  | Fold-switch: distogram entropy, switching vs non-switching (MSA) | **2.245** vs **1.385** | bits | — | p16, Fig 3E |
  | Fold-switch: distogram entropy, switching vs non-switching (no MSA) | **3.242** vs **2.390** | bits | — | Fig 3E, p13 |
  | Fold-switch: pLDDT, switching vs non-switching | **77.4** vs **82.3** | pLDDT | — | p16 |
  | MSA perturbation: mean TM-score, **column shuffling** 10→99% | 0.955, 0.943, 0.910, 0.818, 0.756, 0.752, 0.758 | TM-score **vs full-MSA control prediction** | Fig 4A, p17 |
  | MSA perturbation: mean TM-score, **row subsampling** 10→99% | 0.982, 0.981, 0.976, 0.962, 0.947, ~0.93, ~0.92 (last two occluded by the legend box) | TM-score **vs control prediction** | Fig 4A, p17 |
  | MSA perturbation: **no-MSA baseline** on the 200 Novel | **0.564** | TM-score | Fig 4A dashed line | Fig 4A, p17 |
  | MSA perturbation: breakpoints | intact until **>99% removed** (≈ **47 sequences** left on average) and until **>40% of columns** shuffled; worst case still **>0.5** | — | — | p16 |
  | MSA perturbation: representational drift, C₁ | column shuffling up to **0.253**; row subsampling up to **0.099** | cosine distance from unperturbed | Fig 4C–D, p17 |
  | MSA perturbation: representational drift, C_N | column shuffling up to **0.121**; row subsampling up to **0.053** | cosine distance | Fig 4C–D, p17 |
  | Phylogenetic tiers: random-tier mean aligned identity | ≈ **0.42** (sd **0.14**) | fractional identity | query | p18 |
  | Phylogenetic tiers: qualifying proteins | **61** of 200 (tiers: similar ≥80%, medium 50–70%, dissimilar ≤30%, random) at depths 1, 5, 10 | count | — | p18, p36 |
  | **Fake MSA (Fig 5C), n = 1/10/20/50/100 vs no-MSA reference** — TM-score | 0.491 / 0.512 / 0.514 / 0.512 / 0.502 vs **no-MSA 0.517** | TM-score vs control prediction | Fig 5C, p20 |
  | Fake MSA — pTM | 0.384 / 0.434 / 0.433 / 0.430 / 0.418 vs **no-MSA 0.425** | pTM | Fig 5C, p20 |
  | Fake MSA — cosine distance | 0.537 / 0.520 / 0.519 / 0.524 / 0.542 vs **no-MSA 0.539** | cosine distance from full-MSA C_N | Fig 5C, p20 |
  | Fake MSA — entropy delta | 0.857 / 0.946 / 0.942 / 0.959 / 0.979 vs **no-MSA 0.817** | bits | Fig 5C, p20 |
  | n = 1 alignment composition: % variable residues | similar **27.6%**, dissimilar **86.2%**, random **73.3%** | % | — | p21 |
  | n = 1 long-range **CC** contact recall | similar **0.315**, dissimilar **0.675**, random **0.671** | recall | full-MSA control contact map | p21 |
  | n = 1 CC share of long-range control contacts | dissimilar **3.6%**, similar **65.4%** | % | — | p21 |
  | n = 1 recall ordering, dissimilar tier | CC **0.675** > CV **0.601** > VV **0.514** | recall | control contact map | p21 |
  | n = 1 recall ordering, random tier | CC **0.671** > CV **0.627** > VV **0.454** | recall | control contact map | p21 |
  | Nested 30–60% identity subsampling (183 proteins), n = 5 | mean TM **0.88**, median **0.94** | TM-score **vs full-MSA control prediction** | p22 |
  | Nested 30–60% identity subsampling, n = 10 | mean TM **0.92**, median **0.97** | TM-score **vs control prediction** | p22 |

  **Read the "measured against" column before reusing any TM-score from this table.** The 0.9363 /
  0.5388 pair and the fold-switch RMSDs are against **experiment**. The Fig 4A, Fig 5A/5C and nested-
  subsampling TM-scores are against **AF3's own full-MSA prediction**, and the mutation TM-scores are
  against **AF3's own unmutated prediction in the matching MSA condition**. Mixing them produces a
  false accuracy claim.

- **n_predictions**: **The paper never states a total. Reconstructed below from the protocol; every
  line is derived arithmetic and should be quoted as such.**
  - **Samples per target: 1.** Verbatim, p26: "Instead of generating five diffusion samples, as is
    standard, for computational efficiency **only one diffusion sample was generated during
    structural inference**." So structures ≈ AF3 runs throughout, and **there is no per-target
    ensemble anywhere in this paper**.
  - Baseline monomers: 400 × 2 (MSA, no-MSA) = **800**
  - Adversarial mutation: 400 × 5 loads × 2 regimes = **4,000**
  - SABmark: 100 × 2 = **200**
  - Fold-switchers: 46 pairs = 92 domains × 2 = **184**
  - MSA perturbation: 200 × (7 shuffle + 7 subsample) = **2,800**
  - Phylogenetic subsampling: 61 × 12 variants = **732**
  - Fake-MSA injection: 61 × 5 depths = **305**
  - Nested 30–60% subsampling: 183 × 2 depths = **366**
  - **Derived total ≈ 9,387 AF3 forward passes**, over **≈546 distinct proteins/domains**
    (400 + 100 + 46 pairs), at **1 sample per run**. Recycling N = 10 in every run.
  - **NOT REPORTED by the paper:** total compute, wall-clock, hardware, or any run count.
- **comparable_to_ours**: *(left EMPTY by the extractor, per v3 — populated by whoever holds
  `STATUS.md` and the manuscript)*
- **si_in_scope**: **NO SI — and none is needed for the numbers, but a real gap exists anyway.** The
  PDF is complete at 45 pages (37 pp of body + Methods, then references from p38). **No supplementary
  material, supplementary figure, supplementary table, appendix or extended data is referenced
  anywhere in the text.** There is also **no numbered table of any kind in the paper** — zero tables.
  Consequently every number in `metrics_reported` above is from main text or read off a figure panel,
  and a substantial fraction (all of Fig 1B/1E/1H, Fig 3B/3C/3E, Fig 4A/4C/4D, Fig 5C) exists **only**
  as a printed annotation inside a figure. **The real gap is different and worth flagging: there is no
  code, data, or weights availability statement anywhere in the PDF, and no repository URL** — I
  grepped the full text including the back matter. So the perturbed MSAs, the checkpoint-extraction
  hooks, the 400-protein list, the 61-protein subset and the 46 fold-switch pairs are all
  unobtainable from this document. Not `SI NOT HELD`; rather **NO SI EXISTS, AND NO ARTEFACTS ARE
  RELEASED.**

## F. Figures

One row per panel group. Split on `mark` or `measure`, not on `facet` (v3 rule 8).
**Five figures, 37 lettered panels, 28 panel-group rows** (19 `PLOT`, 9 `MATRIX`, and — unusually for
this corpus — **zero `RENDER`, `TREE` or `SCHEMATIC` rows: this paper contains no structure renders,
no workflow diagrams and no architecture schematic anywhere**).
Pages rendered to fill this table: **p4, p10, p13, p17, p20** at 150 dpi, plus two 400-dpi crops
(Fig 1H on p4; Fig 2D legend on p10; Fig 4A on p17) where printed values or in-panel statistics were
unreadable at 150 dpi. **The captions are unusually informative but never state marks, axis ranges,
n per panel, or the printed cell values, so the renders were necessary.**

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 4 | Cumulative explained variance vs number of PCs for the C_N pair representation, MSA vs no-MSA | line | `PLOT \| facet: none (1) \| vary: number of principal components, 1–70 (continuous) \| series: MSA condition (2: with MSA blue, without MSA red) + shaded "MSA advantage" band + dashed "convergence at PC 68" marker \| measure: cumulative variance explained (%) \| mark: line \| n: 400 proteins behind the PCA; per-mark n/a` | 1 | y-axis starts at ~20%, not 0, which visually exaggerates the early gap between the two curves; the two curves are within ~5 points of each other over most of the range yet the difference is called "saturates faster" without a number | **CC-BY-ND 4.0** — the **ND clause forbids derivatives, i.e. redrawing or modifying as well as copying**. Licence stated in the header of **every page**, incl. p1 and p4 |
| 1B | 4 | PCs required for 95% variance at all four checkpoints, MSA vs no-MSA | bar | `PLOT \| facet: none (1) \| vary: checkpoint (4: A, B, C1, CN) \| series: MSA condition (2) \| measure: effective rank (components for 95% variance) \| mark: bar \| n: 400 proteins per bar; 1 PCA fit per bar` | 1, 8 bars | No error bars and no resampling estimate for a quantity (a 95%-variance cutoff) that is highly sensitive to sample size and to the stratified split; n per bar not printed | as 1A |
| 1C-D | 4 | PC1 score vs sequence length at checkpoints A and C_N, coloured by pTM, with linear fit | scatter | `PLOT \| facet: checkpoint (2: A, CN) \| vary: total sequence length, ~50–580 residues (continuous) \| series: pTM (continuous colour scale, ~0.2–0.9) \| measure: PC1 score \| mark: point \| n: 1 per mark; 400 per panel` | 2, varying by checkpoint | Panels use **different y-ranges** (A ≈ −20…+20, C_N ≈ −20…+10), so the visual "weakening" of the trend is partly an axis effect on top of the real r change (−0.917 → −0.77); pTM colour scales are not shared between panels | as 1A |
| 1E | 4 | Mean distogram entropy by sequence-separation bin: MSA, no-MSA, and their difference | bar | `PLOT \| facet: none (1) \| vary: sequence separation bin (4: seq-local 1–5, secondary 6–11, medium 12–23, long-range ≥24) \| series: condition (3: MSA, no-MSA, difference no-MSA−MSA) \| measure: mean distogram entropy (bits) \| mark: bar \| n: 400 proteins per bar; per-pair entropies averaged within bin then across proteins` | 1, 12 bars | Plots a **derived difference as a third bar in the same series as the two quantities it is derived from**, which triples the apparent number of independent measurements; only the difference bars carry printed values (0.93 / 1.32 / 1.26 / 0.73), the MSA and no-MSA bars do not; no error bars, no n printed | as 1A |
| 1F-G | 4 | Spearman correlations between the top five pair-representation PCs and six biophysical features, at A and C_N | heatmap | `MATRIX \| rows: principal component (5: PC1–PC5) \| cols: feature (6: contact density, mean burial, mean SASA, pTM, sequence length, TM-score) \| value: Spearman ρ, printed, diverging −1…+1 \| facet: checkpoint (2: A, CN)` | 2, varying by checkpoint | **No significance marking or multiple-comparison correction on 60 printed correlations**; p-values are covered only by the blanket statement at p37, verbatim: "Unless otherwise noted, all statistical tests, correlations, and regression analyses reported are significant at p < 0.05". Sequence length and pTM sit in the same matrix as structural features with no distinction between confound and result | as 1A |
| 1H | 4 | Mean distogram entropy change when each of the top five PCs is shifted by ±1σ and ±2σ — **the causal panel** | heatmap | `MATRIX \| rows: principal component (5: PC1–PC5) \| cols: shift magnitude (4: −2.0σ, −1.0σ, +1.0σ, +2.0σ) \| value: mean Δ distogram entropy (bits), printed, range −0.0184…+0.0198 \| facet: none (1)` | 1 | **The paper's only causal result and it hides its own controls.** (i) **The random-unit-vector noise baseline specified in Methods (p31) appears nowhere in this panel or anywhere else** — there is no null row. (ii) The accurate-vs-poor stratification that carries the headline three-fold amplification (+0.0044 vs +0.0133) is **not shown**; only the pooled mean (+0.0088) is plotted. (iii) No dispersion, no n per cell (80 proteins total: 40 highest + 40 lowest TM). (iv) The diverging colour scale spans ±0.015 bits on a 64-bin distribution, making sub-1% entropy changes look categorical. (v) The text's PC2 figure (−0.0198) does not match any cell | as 1A |
| 1I-K | 4 | Shared, unique-pair and unique-single R² information across checkpoints B, C₁, C_N for six targets | heatmap | `MATRIX \| rows: checkpoint (3: B, C1, CN) \| cols: target property (6: helix fraction, mean burial, mean SASA, strand fraction, TM-score, pTM) \| value: R² decomposition component (printed) \| facet: decomposition component (3: shared I, unique-pair J, unique-single K)` | 3, varying by decomposition component (one row per v3 rule 8: same mark, same R² measure, only the facet differs) | **The three panels use wildly different colour scales** (shared ~0–0.9, unique-pair ~0–0.2, unique-single ~0–0.03) with no shared reference, so the visual impression that "pair carries more unique information" is delivered by the colour maps as much as by the numbers — the actual unique-pair values are ≤0.19 and unique-single ≤0.02, both small. Panel K is almost entirely 0.00 and is nonetheless given equal area. n per cell not printed. The decomposition can go negative by construction and no clipping rule is stated | as 1A |
| 1L | 4 | Cα–Cα distance decodability R² across all four checkpoints for three probes | line | `PLOT \| facet: none (1) \| vary: checkpoint (4: A, B, C1, CN) \| series: probe (3: pair representation only, pair + context features, sequence-separation baseline drawn as a horizontal dashed reference at R² = 0.239) \| measure: pairwise distance prediction R² \| mark: line + point \| n: ≤3,000 residue pairs per protein × 320 train / 80 test proteins per point` | 1 | The two live series are within ~0.03 R² of each other at every checkpoint and are plotted with markers large enough to overlap, so the "context adds little" conclusion (stated only in Methods, p26) is hard to read off the panel; no error bars; y-axis 0–1 makes all three lines sit in the lower half | as 1A |
| 1M | 4 | Per-residue-pair expected distance difference (no-MSA − MSA) for a single protein, 7QR2 | heatmap | `MATRIX \| rows: residue i (~330) \| cols: residue j (~330) \| value: expected pairwise distance difference no-MSA − MSA (Å), diverging ≈ −10…+15 \| facet: none (1)` | 1 | **A single hand-picked protein (7QR2, ΔTM = 0.76) with no statement of how representative it is** of the 400; the caption reports the ΔTM of this one case as if it were a result. No aggregate version of this panel exists anywhere in the paper | as 1A |
| 2A-B | 10 | Mean cosine distance from the unmutated control across mutation levels, all checkpoints and both tracks, MSA vs no-MSA | heatmap | `MATRIX \| rows: mutation level (6: control, 10, 20, 40, 70, 80%) \| cols: checkpoint × track (7: A_pair, B_pair, C1_pair, CN_pair, B_single, C1_single, CN_single) \| value: mean cosine distance from control (printed, 0.000–0.751) \| facet: MSA condition (2)` | 2, varying by MSA condition | **Floored metric presented as a finding:** 5 of the 7 columns (A_pair, B_pair and all three single columns) read 0.000–0.036 in every cell of both panels, which is the sole evidence for "No meaningful drift is observed at Checkpoints A or B" (p11) — a saturation floor and an absence of signal are not distinguished. The two panels use **different colour maxima** (~0.75 vs ~0.51), so the no-MSA panel looks more responsive than it is. n = 400 not printed; no dispersion | as 1A |
| 2C-D | 10 | C_N pair cosine distance from control vs TM-score, coloured by mutation level, with linear fit | scatter | `PLOT \| facet: MSA condition (2) \| vary: cosine distance from control, 0–0.9 (MSA) / 0–0.8 (no-MSA) (continuous) \| series: mutation level (5: 10, 20, 40, 70, 80%) \| measure: TM-score \| mark: point + dashed linear fit (r = −0.948 MSA; r = −0.338 no-MSA) \| n: 1 per mark; 400 × 5 = 2,000 per panel` | 2, varying by MSA condition | **x-ranges differ between the two panels** (0–0.9 vs 0–0.8) and **y-ranges differ** (~0.1–1.0 vs ~0.1–1.0 but with all no-MSA mass below 0.4), so the two fits are not visually comparable even though the panels are placed side by side to be compared. Heavy overplotting with no transparency or density estimate; the fit is a single global line through five clearly distinct clusters | as 1A |
| 2E-F | 10 | Dual-axis TM-score and cosine drift vs mutation level, ±1 SD shading | line | `PLOT \| facet: MSA condition (2) \| vary: mutation level, 0–80% (continuous, 6 sampled points) \| series: quantity (2: TM-score on left axis, C_N cosine drift on right axis) \| measure: TM-score (left) and cosine distance from unmutated control (right) \| mark: line + point with ±1 SD band \| n: 400 proteins per point` | 2, varying by MSA condition | **Dual axes with different scalings in each panel** (right axis 0–0.8 in E, ~−0.3–0.4 in F), which is exactly the construction that manufactures apparent "tracking" between two unrelated quantities — the crossing point of the two curves in E has no meaning. The no-MSA right axis extends **below zero** for a cosine distance. SD bands overlap heavily and are not distinguished where they cross | as 1A |
| 2G | 10 | Mean distogram entropy change from control vs mutation level, MSA vs no-MSA | line | `PLOT \| facet: none (1) \| vary: mutation level, 0–80% (continuous, 6 points) \| series: MSA condition (2) \| measure: entropy delta from control (bits) \| mark: line + point with ±1 SD band \| n: 400 proteins per point` | 1 | The MSA-condition SD band is ~±0.4 bits wide at 80% while the separation between the two means is ~0.6 bits, so the bands nearly overlap at every point and no test is reported | as 1A |
| 2H | 10 | PCA projection of pooled MSA-conditioned C_N pair representations, coloured by mutation level | scatter | `PLOT \| facet: none (1) \| vary: PC1 (53.8% variance), ~−25…+5 (continuous) \| series: mutation level (6: control, 10, 20, 40, 70, 80%) \| measure: PC2 score \| mark: point \| n: 1 per mark; ~2,400 points per panel (400 proteins × 6 levels)` | 1 | The headline quantity for this panel — the mean resultant drift-vector length R̄ = 0.901 (p11) — **is not shown**: no drift vectors, no arrows, no directional summary are drawn. The reader is shown a colour gradient and told it means directional convergence. Axis percentages are printed but no n | as 1A |
| 3A | 13 | Within-fold, between-fold and null cosine similarity at all four pair checkpoints, MSA vs no-MSA | bar | `PLOT \| facet: MSA condition (2) \| vary: checkpoint (4: A pair, B pair, C1 pair, CN pair) \| series: comparison type (3: within-fold, between-fold, null baseline) \| measure: cosine similarity \| mark: bar \| n: 560 SABmark pairs per within-fold bar; nulls averaged over 30 (same-protein) and 20 (unrelated-monomer) resamples per pair` | 2, varying by MSA condition, 12 bars each | **Ceiling-saturated over half the panel:** at checkpoints A and B all three bars sit at ≈0.95–1.00 in both conditions, so the "A and B remain comparatively invariant" reading (p14) is indistinguishable from the metric having no room to move. **y-axis 0–1.0 with all data above 0.7**, compressing every real difference into the top third. **No error bars on any bar despite 560 pairs and 30/20 resamples being available.** No n printed | as 1A |
| 3B | 13 | Nearest-neighbour fold classification accuracy per checkpoint and condition | heatmap | `MATRIX \| rows: MSA condition (2) \| cols: checkpoint (4: A pair, B pair, C1 pair, CN pair) \| value: leave-one-out nearest-neighbour accuracy (printed, 0.460–0.670) \| facet: none (1)` | 1 | **The chance level is never stated or drawn** — with 5 groups of 20 in a leave-one-out scheme, chance is ≈19/99 ≈ 0.19, which would make 0.46 (the worst cell) already well above chance and would substantially change how the MSA/no-MSA gap reads. Colour scale runs 0.40–0.70, i.e. **starts far above chance**, so every cell looks informative. n = 100 not printed; no CI on a proportion from 100 trials (±~0.09 at 95%), which is comparable to the entire MSA-vs-no-MSA gap | as 1A |
| 3C | 13 | Mean Kabsch RMSD by MSA condition and alignment status, SABmark | heatmap | `MATRIX \| rows: MSA condition (2) \| cols: alignment status (3: aligned SABmark, non-aligned same protein, unrelated protein) \| value: mean Kabsch Cα RMSD (Å), printed, 3.13–24.45 \| facet: none (1)` | 1 | Means only — **no distribution, no dispersion, no n behind any cell** (560 pairs, and the two null columns are themselves resample means), for the comparison that carries the paper's central SABmark claim. A 3.13 → 12.80 Å shift is reported without knowing whether it is a uniform shift or a bimodal split between recovered and destroyed pairs | as 1A |
| 3D | 13 | Per-domain no-MSA vs MSA RMSD to the experimental structure at the fold-switching region | scatter | `PLOT \| facet: none (1) \| vary: MSA-conditioned predicted RMSD to experiment, 0–30 Å (continuous) \| series: which condition is closer (3: MSA closer n=63, no-MSA closer n=27, tied n=2) \| measure: no-MSA predicted RMSD to experiment (Å) \| mark: point + y=x diagonal \| n: 1 per mark; 92 domains per panel` | 1 | Colouring points by **which side of the diagonal they fall on** is tautological — the legend categories are defined by the geometry being displayed, so the colour carries no independent information while looking like a classification result. Both axes truncate at 30 Å with no indication whether any domain exceeds it | as 1A |
| 3E | 13 | Mean distogram entropy at fold-switching vs non-switching residues, both MSA conditions | bar | `PLOT \| facet: none (1) \| vary: region type (2: fold-switching, non-FS) \| series: MSA condition (2) \| measure: mean distogram entropy (bits), printed (2.245, 3.242, 1.385, 2.390) \| mark: bar \| n: 92 domains per bar` | 1, 4 bars | Four bars, no error bars, no n printed, no test — the entire fold-switch "the model knows something is unusual" claim rests on this panel plus a single pLDDT pair (77.4 vs 82.3) that has **no panel at all** | as 1A |
| 3F | 13 | Per-domain waterfall of RMSD delta (no-MSA − MSA) at the fold-switching region, sorted | bar (horizontal waterfall) | `PLOT \| facet: none (1) \| vary: domain, sorted by delta (92) \| series: sign of delta (2: MSA closer blue, no-MSA closer red) \| measure: RMSD delta no-MSA − MSA (Å), −15…+20 \| mark: bar (horizontal) + dashed mean line at +2.869 Å \| n: 1 per bar; 92 per panel` | 1 | 92 domain labels are printed at a size that is illegible at any normal reproduction scale, so the identity of the 27 domains where removing the MSA *helped* — the most interesting subset in the panel — cannot be recovered. Same data as 3D in a second encoding, which double-counts one comparison across two panels | as 1A |
| 4A | 17 | Mean TM-score across all 14 MSA perturbation levels plus the no-MSA condition | bar | `PLOT \| facet: none (1) \| vary: perturbation condition (15: Shuf 10/20/40/70/90/95/99%, Sub 10/20/40/70/90/95/99%, No MSA) \| series: perturbation type (3: column shuffling, row subsampling, no MSA) \| measure: mean TM-score vs the full-MSA control prediction \| mark: bar + dashed no-MSA baseline at 0.564 \| n: 200 Novel proteins per bar` | 1, 15 bars | **The in-panel legend box physically occludes the tops of the Sub 95% and Sub 99% bars**, i.e. two of the fifteen values cannot be read off the figure at all. **No unperturbed full-MSA control bar is drawn**, so the reference the y-values are measured against is absent from its own panel. No error bars, no n printed, no per-protein distribution behind a mean over 200 proteins. The caption says TM-score is "relative to the no-MSA baseline" while the Methods say comparisons are against the full-MSA control prediction — see `unresolved` | as 1A |
| 4B | 17 | Mean distogram entropy across the same perturbation levels, plus control and no-MSA | bar | `PLOT \| facet: none (1) \| vary: perturbation condition (16: Control, Shuf 10–99% (7), Sub 10–99% (7), No MSA) \| series: perturbation type (4: control, column shuffling, row subsampling, no MSA) \| measure: mean distogram entropy (bits) \| mark: bar \| n: 200 proteins per bar` | 1, 16 bars | No error bars, no printed values, no n. Uses a **different condition set from 4A** (this panel has a Control bar, 4A does not), so the two panels immediately above and below one another cannot be read against a common x-axis | as 1A |
| 4C-D | 17 | Mean cosine distance from the unperturbed control across checkpoints, for row subsampling and column shuffling | heatmap | `MATRIX \| rows: perturbation level (7: 10, 20, 40, 70, 90, 95, 99%) \| cols: checkpoint (5: A, B, C1, CN, CN_single) \| value: mean cosine distance from unperturbed control (printed, 0.000–0.253) \| facet: perturbation type (2: row subsampling, column shuffling)` | 2, varying by perturbation type | **The two panels use different colour maxima (0.10 for subsampling, 0.25 for shuffling)** while being placed side by side for comparison, so the shuffling panel's larger drift is visually flattened relative to its true 2.5× advantage. Both panels are dominated by 0.000 cells (columns A, B and CN_single are entirely ~0.000–0.003 in both), another floored region presented as a result. **Negative-zero values are printed ("−0.000")** in the shuffling panel | as 1A |
| 4E-F | 17 | Entropy-based effective rank across checkpoints and perturbation levels | bar | `PLOT \| facet: perturbation type (2: row subsampling, column shuffling) \| vary: checkpoint (5: A, B, C1, CN, CN_single) \| series: perturbation level (9: control, 10, 20, 40, 70, 90, 95, 99%, no MSA) \| measure: entropy-based effective rank \| mark: bar \| n: 200 proteins per bar` | 2, varying by perturbation type; 45 bars each | 45 bars per panel in a 9-colour sequential ramp where adjacent levels are indistinguishable; **the only bar that matters (no-MSA, red) is legible but the other eight are not**, so the claimed invariance across perturbation levels is asserted by an unreadable ramp. No values printed, no error bars. The CN_single group (rank ~65–70) shares a y-axis with the pair groups (rank ~19–45), compressing the pair differences the panel exists to show | as 1A |
| 5A | 20 | TM-score-to-control and pTM vs MSA depth, stratified by phylogenetic tier | line | `PLOT \| facet: metric (2: TM-score vs control, pTM) \| vary: MSA depth (3: 1, 5, 10 sequences) \| series: phylogenetic tier (4: similar, medium, dissimilar, random) + 2 reference lines (full-MSA control dashed, no-MSA dotted) \| measure: TM-score to the full-MSA control prediction / pTM \| mark: line + point with shaded band \| n: 61 proteins per point` | 2, varying by metric | **Both y-axes are truncated** — the TM-score panel starts at ≈0.48 and the pTM panel at ≈0.35, neither at 0 — which magnifies the tier separation that is the panel's entire message. Only **three** depth points (1, 5, 10) are joined by straight lines that imply a continuous trend. The shaded bands are never defined in the caption (SD? SEM? CI?). n = 61 not printed | as 1A |
| 5B | 20 | Radar profiles across five metrics for each tier, at depths 1, 5 and 10 | radar / spider | `PLOT \| facet: MSA depth (3: n=1, n=5, n=10) \| vary: metric axis (5: lDDT, TM-score, Rep. Similarity, Model Certainty, pTM) \| series: phylogenetic tier (4: similar, medium, dissimilar, random) \| measure: normalised metric value (radial) \| mark: line (closed polygon) \| n: 61 proteins per vertex` | 3, varying by depth | **A radar chart of five metrics, two of which are monotone transforms of the others' inputs** (`1 − entropy increase` and `1 − C_N cosine distance` alongside pTM and TM-score), so the "larger enclosed area = better" heuristic the caption invites double-counts correlated axes. **Enclosed area depends on the arbitrary ordering of the five axes** and on the unstated radial normalisation. Radial tick values are printed but illegible at print size; no axis ranges given | as 1A |
| 5C | 20 | Model performance under fake-MSA injection at five depths, against the no-MSA reference | heatmap | `MATRIX \| rows: metric (4: TM-Score, pTM, Cosine Distance, Entropy Delta) \| cols: fake-MSA depth (5: n=1, 10, 20, 50, 100) + 1 separated no-MSA reference column \| value: metric value (printed, 0.384–0.979) \| facet: none (1)` | 1 | Four metrics with **incompatible directions and units share one colour scale** (0.4–0.9): higher is better for TM-score and pTM, lower is better for cosine distance, and "entropy delta" is a normalised uncertainty whose polarity is never stated — so the darkest row (entropy delta, 0.857–0.979) reads as the strongest result when it is the *worst*. **No full-MSA control column**, only a no-MSA one, so the reader cannot see how far below the ceiling everything sits. n = 61 not printed | as 1A |
| 5D | 20 | Delta Cα–Cα contact recall vs the no-MSA baseline, by tier × depth and sequence-separation bin | bar | `PLOT \| facet: none (1) \| vary: tier × depth condition (13: similar/medium/dissimilar/random × n=1/5/10, plus fake_n100) \| series: sequence separation bin (4: sequential 1–5, secondary 6–11, medium-range 12–23, long-range ≥24) \| measure: delta contact recall vs the no-MSA baseline \| mark: bar \| n: 61 proteins per bar (fake_n100 also 61)` | 1, 52 bars | **Recall is computed against the full-MSA control prediction, not against experiment** (p37), so every bar measures agreement with AF3's own output; the axis label "Delta Contact Recall vs No-MSA" does not say this. x-tick labels are printed at ~4 pt and are illegible at reproduction size. No error bars on 52 bars over 61 proteins. The `fake_n100` bar — the paper's key null — is squeezed to the far right at ~0 height where it is easiest to miss | as 1A |

**28 panel-group rows across 5 figures and 37 lettered panels** (9 + 5 + 6 + 4 + 4). Splits: Fig 1 → 9 rows
(1A, 1B, 1C-D, 1E, 1F-G, 1H, 1I-K, 1L, 1M); Fig 2 → 5 rows (2A-B, 2C-D, 2E-F, 2G, 2H); Fig 3 → 6 rows
(3A, 3B, 3C, 3D, 3E, 3F); Fig 4 → 4 rows (4A, 4B, 4C-D, 4E-F); Fig 5 → 4 rows (5A, 5B, 5C, 5D).
There are **no tables** in this paper, so no table rows exist.

**Licence warning, repeated because it governs every row.** The preprint is **CC-BY-ND 4.0**
(p1 and every subsequent page header). **The ND clause forbids derivative works, which means these
figures may not be redrawn, recoloured, cropped into a composite, or otherwise adapted — only
reproduced verbatim with attribution.** Several of these panels are otherwise attractive redraw
candidates (Fig 1B, Fig 3C, Fig 5C); they are not available for that. Note that most bioRxiv
preprints in this corpus are CC-BY or CC0; this one is not.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), session 2026-09-08
- **schema_version**: v3
- **confidence**: **high** for the experimental design, the checkpoint definitions, the probe
  inventory, the control inventory, the MSA-perturbation protocol, the licence, and — the point of
  this extraction — the boundary between what is shown to be represented and what is shown to be
  causally used. The Methods are unusually explicit (14 subsections, equations given) and the causal
  section (p30–31 §4.6) states its own scope plainly enough that no inference was needed.
  Reservations:
  - **Figure values were read from renders.** Pages 4, 10, 13, 17 and 20 were rendered at 150 dpi;
    Fig 1H, the Fig 2C-D legends and Fig 4A were re-cropped at 400 dpi because the printed cell
    values and in-panel fit statistics are unreadable at 150 dpi. All printed heatmap values quoted
    in this note (Fig 1H, 1I-K, 2A-B, 3B, 3C, 3E, 4C-D, 5C) were read at 150 dpi or better and are
    reliable to the digits shown. **Two values are explicitly uncertain and marked as such: the Sub
    95% and Sub 99% bars in Fig 4A, whose tops are occluded by the legend box (estimated ~0.93 and
    ~0.92 from bar position).**
  - **Effective-dimensionality no-MSA values (17 / 18 / 26 / 25) are read off Fig 1B only**; the body
    text (p6) gives the MSA series (16/32/19/17) in prose but never the no-MSA series.
  - **Fig 1E difference-bar values (0.93 / 1.32 / 1.26 / 0.73) are read off the panel**; the text
    gives only the qualitative claim that the gap peaks at 6–23 separation.
  - Panel counts and mark types were confirmed visually for all five figures; caption text alone
    would not have supported the `data_shape` rows.
- **unresolved**:
  1. **Fig 1H does not agree with the p6 text on PC2.** The text says "shifting representations along
     PC2 **uniformly reduces** distogram entropy by **−0.0198**". Fig 1H's PC2 row reads
     **+0.0198 at −2σ**, +0.0097 at −1σ, −0.0094 at +1σ, **−0.0184 at +2σ**. So (a) the response is
     **monotone and antisymmetric, not "uniform"**, and (b) the magnitude 0.0198 appears in the
     figure with the **opposite sign** to the text, at the −2σ cell. Most likely the text is quoting
     the −2σ cell with a sign error, or quoting the +2σ cell with a transposed magnitude. **Not
     resolvable from the PDF. A citation of the PC2 result must carry this caveat.**
  2. **The random-unit-vector noise baseline for activation patching is specified in Methods (p31)
     and its result is reported nowhere.** I searched the full text for "random unit", "noise
     baseline", "random direction" and "random vector"; the only hit is the Methods sentence itself.
     This is the paper's single most consequential gap and it is unresolvable from the document.
  3. **What Fig 4A's TM-scores are measured against.** The caption (p17) says "relative to the no-MSA
     baseline"; the Methods for phylogenetic subsampling (p37) say "Structural outputs were compared
     against the full-MSA control prediction". §4.10.1 and §4.10.2 (column shuffling, row
     subsampling) **never state a reference at all**. Given the no-MSA dashed line at 0.564 sits
     *inside* the panel as a reference rather than as the zero point, the values are almost certainly
     TM-score to the full-MSA control prediction — but this is inference, not statement.
  4. **How many Pairformer layers does AF3 have, in this study's setup?** Never stated. C₁ and C_N
     are both "after the final Pairformer layer", so **no intra-Pairformer depth resolution exists**
     and no claim in this paper can be attributed to a specific layer. Anyone citing this note for
     "layer-by-layer" analysis is citing it wrongly.
  5. **Which AlphaFold 3 implementation, version or weights?** Never named. The `pairedMsa` /
     `unpairedMsa` JSON fields (p31, p35) identify the official open-source interface, but no
     repository, commit, release date or weights identifier appears anywhere. There is likewise **no
     code or data availability statement and no URL** in the entire PDF.
  6. **The Novel-vs-Similar anti-memorisation control has no number, no test and no figure panel** —
     only the sentence "performance differences between the two groups were negligible at every
     checkpoint" (p9). The comparison that carries the memorisation argument is the only major
     analysis in the paper with no quantitative artefact.
  7. **"Near-perfect accuracy" for amino-acid re-identification (p7) is never quantified.** It is the
     paper's probe-faithfulness control and has no number.
  8. **Checkpoint A's recycling step is never stated.** B is explicitly r = 0, C₁ is r = 0, C_N is
     r = N−1; A is left unspecified, and since sequence initialisation is recomputed or carried
     across recycles depending on the module, this matters for interpreting the A → B contrast.
  9. **Fold-switch domain count vs pair count.** The text says 46 pairs (p15, p25); Fig 3D/F report
     n = 92 with a 63/27/2 split. 92 = 46 × 2 is the obvious reconciliation, but the paper never
     states it, and it means each *pair* contributes two non-independent points to the waterfall.
  10. **The p8 claim that MSAs "most bolster model confidence—though not structure (see MSA
      Perturbation section)—at local secondary-structure contacts rather than long-range tertiary
      interactions" sits awkwardly against the p19 claim that MSA inclusion "produces marked
      improvements in contact recall across all separation ranges, with long-range contacts
      consistently showing the largest gains."** The
      first is about *entropy* by separation bin (Fig 1E), the second about *contact recall* by
      separation bin (Fig 5D), so they are not formally contradictory — but they are stated three
      pages apart in opposite directions with no cross-reference, and a careless citation of either
      will misrepresent the paper.
  11. **`refs.bib` records a different title from the PDF** (see `title`). The bib entry should
      probably be updated; I have not changed it.
  12. **Blanket significance statement.** p37: "Unless otherwise noted, all statistical tests,
      correlations, and regression analyses reported are significant at p < 0.05." **No individual
      p-value appears anywhere in the paper**, and no multiple-comparison correction is mentioned
      despite ~60 printed correlations in Fig 1F-G alone.
  13. **Tags I needed and could not use — none invented.** Four vocabulary gaps, all recorded in the
      Tags section below rather than resolved: (a) no method tag for **interpretability / probing**
      as a read-out activity; (b) no way to distinguish an intervention **read out at an auxiliary
      head** from one read out in coordinates; (c) `msa-subsample` conflates a *conformational
      sampling method* with an *ablation instrument*; (d) no atomic tag for **MSA-off / MSA-ablation**.
      Gaps (a) and (d) were also reported by the `migliorini2026pairsae` extractor — that makes them
      two-extractor findings and, by the schema's own standard, structural.
- **why_it_matters**: *(left empty by the extractor — the user's call)*

---

## Tags

`general-protein` `fold-switching` `latent-steering` `msa-subsample` `no-template-no-msa`
`single-state` `rmsd-only` `continuous-metric` `saturating-metric` `oracle-leak`
`design-level-oracle` `anti-memorization` `preprint` `precedent` `contrast` `negative-result`
`comparator-numbers`

### Tag notes — every decision, especially the declines

**`latent-steering` — APPLIED, and this is the most consequential tag decision in the note.** The v3
definition is "any inference-time intervention on an internal tensor — pair representation, trunk
embedding, distogram head, conditioning embedding". The activation-patching experiments (p6–p7,
p30–31 §4.6) intervene at inference time on the **C_N pair representation**, which is named
explicitly in the definition: `p'_ij = p_ij + σ√λ_k v_k` for the PC shifts, and wholesale tensor
overwriting for the cross-protein transplant. This is unambiguously within scope. **But the tag must
not be read as "this paper steered a structure."** It did not. The intervention is read out through
the frozen distogram head as a change in entropy, and no patched representation ever reaches the
diffusion module or produces a coordinate. A reverse lookup on `latent-steering` will return this
paper alongside papers that steered structures, and the two are not the same claim — see the
"REPRESENTED vs CAUSALLY USED" section at the top of this note, which exists precisely so that
distinction survives the tag. **This is v3 gap (b): the vocabulary cannot express "intervened, but
measured only at an auxiliary head."**

**`msa-subsample` — APPLIED, with an explicit warning.** The paper performs genuine MSA row
subsampling at seven rates (p36 §4.10.2) and phylogenetic subsampling at three depths across four
tiers (p36–37 §4.10.3), which is textbook MSA subsampling. **But the purpose is diametrically
opposite to every other `msa-subsample` paper in this corpus.** Elsewhere the tag marks a method that
subsamples MSAs *to generate conformational diversity*; here subsampling is a **perturbation
instrument used to ablate information and measure what breaks**, and the paper's finding is that
subsampling changes essentially nothing until 99% (Fig 4A). A query for "AF-subsampling conformational
sampling methods" will get a false positive here. **This is v3 gap (c) and I could not avoid it
without either inventing a tag or dropping a genuinely accurate one.** Recorded, not resolved.

**`no-template-no-msa` — APPLIED, and this paper is arguably the strongest instance of the tag in the
corpus.** The tag "marks the de-novo input regime". Templates are off in **every single run**, stated
verbatim and with a stated rationale (p26: "no analysis used template information as inputs to reduce
potential confounds and structural invariance"), and the **no-MSA arm is run on every benchmark** —
400 monomers, 100 SABmark proteins, 46 fold-switch pairs, all five mutation levels, and as the lower
baseline for every perturbation. Both halves of the compound tag are asserted by the paper, so no
inference is required. **Caveat for the reverse lookup:** the paper is not *only* de-novo — the
full-MSA arm is equally central, and the paper's entire point is the contrast between the two. This
tag marks the presence of the regime, not its exclusivity.

**`single-state` — APPLIED.** One diffusion sample per prediction, by explicit choice (p26); no
ensemble anywhere; and the substantive fold-switching finding is that both members of a metamorphic
pair collapse onto the same fold (§2.8, 2.02 Å between predicted switching regions that experiment
says differ). `two-state`, `ensemble` and `continuum` all declined — none is produced or attempted.

**`fold-switching` — APPLIED.** 46 experimentally validated metamorphic pairs are a full section
(§2.8) with its own figure panels (3D, 3E, 3F) and its own curation protocol (p25 §4.1). The tag is a
system property covering metamorphic proteins, which is exactly what this arm studies.

**`general-protein` — APPLIED.** The 400-monomer primary benchmark and the SABmark SCOP groups carry
no family restriction. Explicitly **not** `gpcr` / `kinase` / `transporter` / `periplasmic-binding` /
`atpase` — none of these appears anywhere in the paper.

**`rmsd-only` + `continuous-metric` + `saturating-metric` — all three APPLIED, deliberately, and here
is why that is not self-contradictory.** `rmsd-only` is applied because **the conformational question
is answered by Kabsch RMSD alone, with no binary state predicate and no threshold anywhere** — the
fold-switch and SABmark state calls have no operationalised success criterion. `continuous-metric` is
applied because the *representational* half of the paper is entirely continuous (cosine distance,
distogram entropy, KL divergence, R², effective rank, Spearman ρ) and a query for papers with
continuous internal metrics should find this one. `saturating-metric` is applied for the three
documented saturation sites in `metric_saturation`, one of which the authors themselves name (p8,
"limited dynamic range… renders regression effectively uninformative"). **`binary-predicate`
declined** — there is no binary predicate in the paper. **`visual-metric` declined** — everything is
quantified; there is not a single by-eye structural call, and notably there are **no structure renders
at all** in any of the five figures, which is unusual for this corpus and worth knowing.

**`oracle-leak` — APPLIED, narrowly, and the scope must travel with the tag.** Applied on **route 6**:
the activation-patching source protein is "the highest-accuracy protein in the training set" and the
targets are "the 40 highest and 40 lowest TM-score predictions" (p30–31), i.e. **best/worst labels
assigned against a held reference — the exact wording of route 6** — and the resulting accurate-vs-poor
contrast is the paper's headline causal number. Secondarily on **route 4** (probe model family and
pooling strategy chosen on the reported test split, with no validation split described; splits
stratified by pTM and TM decile). **What this tag does NOT mean here, and the distinction is
important enough to state twice: nothing leaky ever entered AlphaFold 3. No template, no state
annotation, no structural input, no per-target tuning.** The input pipeline is among the cleanest in
this corpus. Applying `oracle-leak` without this note would badly misrepresent the paper; declining
it would suppress a real route-6 instance sitting inside the only causal claim. I have applied it and
attached the scope.

**`design-level-oracle` — APPLIED (route 7), and kept distinct from the above.** SABmark groups were
chosen because fold similarity is experimentally validated; the 46 fold-switch pairs were chosen
because both states are deposited and the metamorphic ranges are already annotated; the Novel/Similar
split is built from known homology to the presumed training set. The expected answer is declared
before the result is read, while the pipeline stays clean. This is the weaker of the two rigour tags,
per the schema, and is normal benchmark design.

**`anti-memorization` — APPLIED, and unusually well earned.** A held-out set exists **and** a control
arm was run and analysed: all 400 proteins post-date the 30 Sep 2021 AF3 cutoff, the 200/200
Novel/Similar contrast was actually compared across all five probes at all four checkpoints (p9), and
the no-MSA collapse is deliberately demonstrated on likely-trained proteins (p16). Well powered
(n = 200 per arm), so **not** `unpowered`. `no-anti-memorization` obviously declined. **Caveat: the
Novel-vs-Similar comparison is reported as a sentence with no number, no test and no panel**, and
"training set" is inferred from PDB deposition dates rather than known — see `unresolved` 6.

**`negative-result` — APPLIED.** Three of the paper's most solid findings are nulls or failures:
(i) fake MSAs, format-preserving and up to 100 sequences deep, do nothing at all (Fig 5C, all four
metrics flat against the no-MSA reference); (ii) near-identical homologs at n = 10 leave accuracy near
the no-MSA floor (Fig 5A, similar tier); (iii) AF3 collapses metamorphic sites to one fold with an
MSA, and removing the MSA makes it *less* correct rather than more flexible (§2.8, 7.35 → 10.0 Å).
These are results, not incidental nulls.

**`precedent` + `contrast` — APPLIED, both provisional (the user's call, per schema D).** Rationale in
`stance`. `threat` declined: the paper proposes no competing method and benchmarks nothing against
which another method would lose. `background` declined as too weak — the findings are load-bearing,
not context.

**`comparator-numbers` — APPLIED.** `metrics_reported` carries ~60 rows including full-MSA and no-MSA
TM-score distributions with standard deviations, probe R² trajectories, SABmark RMSD tables,
fold-switch RMSDs against experiment, and complete MSA-degradation curves. Several are directly
usable as reference values, provided the "measured against" column travels with them.

**Tags considered and DECLINED, with reasons — these are the decisions a future query depends on:**

- **`cofolding` — DECLINED, deliberately, and this is a close call worth stating.** AlphaFold 3 *is* a
  co-folding architecture, and the `migliorini2026pairsae` note in this corpus applied `cofolding` on
  exactly that reasoning for Boltz-2. But **every single input in this paper is a single protein
  chain**: 400 monomers (the word "monomer" is in the dataset name), 100 SABmark monomeric domains,
  46 fold-switch domains. There is not one complex, ligand, nucleic acid or interface anywhere, and
  the Discussion explicitly marks multimers as untested (p23). Applying `cofolding` would return this
  paper for "which papers folded things together", which it never did. **I am flagging the
  inconsistency with the pairsae note rather than hiding it: the corpus needs a rule on whether
  `cofolding` marks the architecture or the input regime.** Recorded for the schema owner.
- **`multi-backbone` — DECLINED.** One backbone (AF3). No AF2, Boltz, Chai, OF3 or Protenix is run;
  they are not even discussed comparatively.
- **`msa-state-filter` — DECLINED, firmly.** No MSA anywhere in this paper is selected to favour a
  conformational state. The phylogenetic tiers select on **sequence identity to the query**, which is
  a diversity axis, not a state axis. Confusing these is the exact error the schema's `msa_handling`
  note warns about.
- **`template-state-bias`, `af-cluster`, `md`, `md-emulator`, `enhanced-sampling`, `benchmark-only`,
  `experimental` — all DECLINED.** Templates are off entirely; no clustering of predictions; no
  molecular dynamics of any kind and no MD-trained generator; no enhanced sampling; the paper is not
  a benchmark (it proposes no leaderboard and ranks no methods); and `experimental` is wrong twice
  over — there is no wet lab, and structure prediction is the paper's entire substrate.
- **`templates-on` / `state-annotated-input` — DECLINED.** Templates are off (p26). Annotations
  (SCOP, SABmark alignments, metamorphic ranges) are used **only for evaluation and residue
  indexing**, never as model input, so `state-annotated-input` would be actively false.
- **`prospective` — DECLINED.** Post-cutoff targets make the paper memorisation-clean, not
  prospective: nothing is predicted before its structure exists, and the two secondary datasets
  predate the cutoff entirely. See `prospective` in section C for the partial reading.
- **`unpowered` — DECLINED.** n = 400 for the primary benchmark, 200 per anti-memorisation arm,
  560 SABmark pairs, 92 fold-switch domains. The only arm near the schema's n < ~10 threshold is the
  patching experiment's 40 + 40 test proteins, which is above it. (Statistical *reporting* is poor —
  no error bars, no per-claim tests — but that is a `hides` and `controls_run` problem, not an n
  problem.)
- **`confidence-as-discriminator` — DECLINED, after real consideration.** pTM and pLDDT are used as
  probe targets and as stratification variables, and entropy/pLDDT are reported as *flagging* fold-
  switch anomalies — but the paper never uses any confidence metric **to judge conformational
  correctness**, and explicitly says the model flags the anomaly "even while failing to resolve the
  alternative conformation" (p16). The nearest thing to a validation is the KL-vs-ΔTM correlation
  (r ≈ 0.72, p9), which validates an *internal* uncertainty measure against realised structural loss —
  and that is not what this tag means. Full reasoning in `confidence_as_discriminator`.
- **`experimental-validation` — DECLINED.** No NMR, no cryo-EM, no assay. Every "experimentally
  validated" phrase in this paper refers to *previously deposited* structures, not to work the
  authors did.
- **Control family (`directed-state`, `partner-driven`, `ligand-driven`, `peptide-driven`,
  `g-protein-mimetic`, `nanobody`, `apo-sampling`, `seed-only`) — NONE APPLIED.** There is no
  conformational control handle of any kind: no binding partner, no ligand, no apo/holo contrast, and
  seeds are held *fixed* to the control rather than varied ("identical hyperparameters and random
  seeds to the control", p35), which is the opposite of `seed-only`.
- **Site family (`orthosteric`, `allosteric-site`, `cryptic-pocket`, `allosteric-failure`) — NONE
  APPLIED.** No binding site of any kind is studied; there are no ligands in the paper.
- **`figure-exemplar` — DECLINED.** The figures are information-dense and the `hides` column above is
  long: occluded bars (4A), unshared colour scales presented for comparison (1I-K, 2A-B, 4C-D),
  truncated axes (5A), dual axes engineered to look like tracking (2E-F), illegible tick labels
  (3F, 5D), a radar chart with correlated axes (5B), and a causal panel with no null row (1H). These
  are instructive as **negative** examples and are recorded as such, but the tag means "kept mainly
  for its figures", which is not why this paper is in the corpus.

### Four v3 vocabulary gaps hit while tagging — recorded, not invented

1. **No method tag for interpretability / probing as a read-out activity.** `latent-steering` covers
   only the intervention. This paper's probing programme — four checkpoints, eight probe families,
   two representations — has no tag, so a query for "which papers probed model internals" finds
   nothing. **Second independent report: the `migliorini2026pairsae` extractor hit the same gap and
   also declined to invent a tag.** By the schema's own two-extractor standard this is structural.
2. **No way to distinguish an intervention read out at an auxiliary head from one read out in
   coordinates.** `latent-steering` puts "changed the distogram entropy by 0.0088 bits" and "produced
   a different fold" in the same bucket. For a corpus whose central question is whether trunk
   interventions do anything to structure, this is the distinction that matters most.
3. **`msa-subsample` conflates a conformational-sampling method with an ablation instrument.** See
   the tag note above.
4. **No atomic tag for MSA-off / MSA-ablation.** `no-template-no-msa` is a compound that asserts both
   halves, and works here only because templates genuinely are off. A paper that ran a no-MSA arm
   with templates on would have nowhere to record it. **Also a second independent report** — the
   pairsae extractor hit this from the other direction (MSA off, template status unknown, so the
   compound tag was unusable).
