# protenix2025

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` **with a reason** where the field's axis does not exist in this paper.

**Framing.** This is a **MODEL paper**, and specifically an **open reproduction of AlphaFold 3**
by the ByteDance AML AI4Science Team. It is not a conformational-state paper: it predicts one
ranked structure per target and scores it against a deposited reference. Section C is therefore
largely `NOT APPLICABLE` **by design**, not by sloppy extraction — the paper contains no state
predicate, no two-state target, no directional handle, and no discussion of alternative protein
conformations anywhere. The two things the corpus wants from it are (1) the **exact training
cutoff**, and (2) **every stated deviation from AF3**, because a benchmark that treats Protenix
and AF3 as independent architectures would be over-claiming. Both are recorded in full below,
the deviations in a dedicated sub-table under `structural_priors_used` /
`### Deviations from AlphaFold 3`.

**Page numbers** are PDF page numbers from `./pagetext.sh` markers (1–21) and coincide with the
printed folios ("Page 4 of 21" on PDF p4). Layout: p1 title, p2 ToC, p3 Introduction, p3–10
Results (2.1 Overview p3–4, 2.2 Ligands p4–6, 2.3 Proteins p7–8, 2.4 Nucleic Acids p8–9,
2.5 Discussion p10), p11–14 Methods (3.1 Data Pipeline p11–12, 3.2 Model and Training p13–14),
p14–15 Accessibility, p15 Future Plan + Acknowledgements, p16–17 References, p18–19 Appendix A
Dataset, p19 Appendix B Evaluation Workflow, p20–21 Appendix C Chain and Atom Permutation.

**Figure-value caveat.** The paper prints almost **no numeric result in running text** — the
narrative says "slightly higher", "similar to", "higher accuracy than" and points at a panel.
Every value in `metrics_reported` marked *(read from rendered panel)* was read off panels
rendered with `pdftoppm -r 150` (pages 4, 5, 9) and is approximate to roughly ±0.01–0.02.
The only exact printed numbers in the whole paper are the correlation coefficients in Figure 8
(p10), the bin/cluster counts printed under the axes, the parameter count of AF3 (p13), the
training step counts (p14) and the dataset sampling weights (Table 3, p18).

---

## A. Identity

- **citekey**: `protenix2025`
- **doi**: **10.1101/2025.01.08.631967** (bioRxiv). Banner on every page, p1: "bioRxiv preprint
  doi: https://doi.org/10.1101/2025.01.08.631967; this version posted January 11, 2025."
- **year**: **2025** as posted (11 January 2025, p1). Note the **document itself is dated
  "November 9, 2024"** on the title page (p1) — the manuscript predates the bioRxiv posting by
  two months. `refs.bib` records 2025, matching the posting.
- **venue**: **bioRxiv preprint, not certified by peer review.** p1: "The copyright holder for
  this preprint (which was not certified by peer review) is the author/funder, who has granted
  bioRxiv a license to display the preprint in perpetuity. It is made available under a CC-BY 4.0
  International license." Tagged `preprint`. No journal version is referenced in the PDF.
- **title**: **"Protenix — Advancing Structure Prediction Through a Comprehensive AlphaFold3
  Reproduction"** (p1).
- **authors**: **ByteDance AML AI4Science Team** — Xinshi Chen\*, Yuxuan Zhang\*, Chan Lu,
  Wenzhi Ma, Jiaqi Guan, Chengyue Gong, Jincai Yang, Hanyu Zhang, Ke Zhang, Shenghao Wu,
  Kuangqi Zhou, Yanping Yang, Zhenyu Liu, Lan Wang, Bo Shi, Shaochen Shi, Wenzhi Xiao§ (p1).
  \* equal contribution; § contact, xiaowenzhi@bytedance.com. 17 authors. Corporate authorship
  is given as the team, not a university.
- **code / weights**: `https://github.com/bytedance/Protenix` (footnote, p14). Model weights,
  inference code **and trainable code** released "for research purposes" (p3, p14–15). Processed
  data including precomputed MSAs "covering all instances in the wwPDB" and a PDB-ID → processed
  data mapping are also released (p14).

## B. Scope

- **system**: **general — all biomolecular complex types AF3 covers.** Protein–ligand
  (PoseBusters V2), protein–protein and protein–antibody interfaces, protein–RNA, protein–dsDNA,
  and RNA monomers (CASP15). No family-specific arm, no GPCR/kinase/transporter arm, no
  fold-switching arm. Tagged `general-protein`.
- **n_targets**: Reported per benchmark, and the units differ between benchmarks — this must not
  be collapsed to one number.
  - **PoseBusters V2: 308 structures** (Fig 1A, p4; Appendix A.2.1, p18: "This dataset contains
    308 structures").
  - **Low Homology (LowH) Recent PDB Set, protein interfaces: N = 993 interface *clusters*** for
    all protein–protein and **N = 64 clusters** for protein–antibody (Fig 1B, p4). Fig 1 caption,
    p4: "Metrics are averaged within and across interface clusters; N represents the number of
    clusters." The number of underlying *structures* is never stated.
  - **Protein–nucleic acid: 25 RNA–protein structures and 38 dsDNA–protein structures**
    (Fig 1C, p4; Appendix A.2.3, p19).
  - **CASP15 RNA: 8 targets** (Fig 1D, p4), named individually on p19: R1116/8S95, R1117/8FZA,
    R1126, R1128/8BTZ, R1136/7ZJ4, R1138/[7PTK/7PTL], R1189/7YR7, R1190/7YR6.
  - **Confidence-calibration set (Fig 8, p10): 24,650 interfaces** binned across five chain-pair
    ipTM bins (3503 + 10969 + 4540 + 3419 + 2219), of which 16,595 protein–protein and 8,055
    protein–nucleic acid.
  - **Case studies: 7 individual PDB entries rendered** — 7WUX, 7URD (Fig 3, p6), 7LOE, 5SAK/5SAN
    (Fig 4, p7), 7XVA, 7XV8 (Fig 5, p8), 7R6R (Fig 7, p9), 7PZB/3MZH, 7XFA/5OAX (Fig 9, p10).
  - **Generality claim flag**: not a single-system paper, so the usual flag does not apply. The
    generality claim it *does* make and does not test is architectural, not biological — see
    `stated_limits`.
- **method_class**: **co-folding.** An all-atom joint structure predictor of protein + ligand +
  nucleic acid, diffusion-based, reproducing AF3's architecture (p3, p13). Secondarily a
  **benchmark** paper, since Section 2 is entirely head-to-head evaluation, but the deliverable
  is the model.
- **backbones**: **Protenix (own, the subject), AF3, AF2.3 (AlphaFold-Multimer 2.3), RF2NA
  (RoseTTAFold2NA), and AIchemy_RNA2** (p3, p4 Fig 1, p8–9). Five predictors appear in the
  comparison and four are compared head to head on at least one benchmark → tagged
  `multi-backbone`. Note that **AF3 numbers are not all recomputed**: PoseBusters AF3 metrics are
  computed by the authors from AF3's *released predictions* (Fig 2 caption, p5); the protein- and
  nucleic-interface AF3 numbers are **transcribed from the AF3 paper** and labelled "AF3 in AF3"
  (Fig 1 caption, p4); the CASP15 RNA AF3 numbers are **taken from a third preprint**, Bernard
  et al. (p8). Protenix never runs AF3 itself.
- **templates**: **OFF — categorically.** p11, one sentence in full: "**Templates. We do not use
  templates.**" This is a **deviation from AF3**, which uses templates, and is recorded again in
  the deviations table.
- **msa_handling**: **full, but from a different pipeline than AF3, and absent for nucleic
  chains.** p11: "We search MSAs using MMSEQS2 [25] and ColabFold [7] MSA pipeline, and use MSAs
  from the Uniref100 [26] database for pairing (species are identified with taxonomy IDs). We do
  not use MSA for nucleic chains." Confirmed p8: "Protenix does not use MSA for nucleic chains."
  **Not subsampled, not clustered, not state-filtered** — no MSA manipulation of any kind is
  performed. Precomputed MSAs for all wwPDB instances are part of the data release (p14).

## C. Conformational core

- **states_generated**: **one** — a single ranked structure per target is what is reported and
  scored, everywhere in the paper. The sampler does produce a pool (`one` reported out of 25
  generated; see `n_predictions`), and the paper reports an "all sample" and an "oracle" curve
  over that pool in Fig 2B (p5), but **the pool is never treated as a conformational ensemble**:
  it is a candidate list to be ranked, and the paper's own framing of it is "room for improvement
  with a better sample ranker" (p6). The one place an alternative conformation is acknowledged is
  a *ligand* conformer, not a protein state — p7: "Protenix predicts an alternative ligand
  conformation with the fluorine atom oriented oppositely (7LOE), though both conformations share
  similar occupancies (42% vs. 58%)."
  So: **one** (single-state), with a 25-sample pool that is collapsed by confidence ranking and
  never analysed as states. Dual value not warranted — `ensemble` would misdescribe a candidate
  list the paper itself never calls an ensemble.
- **structural_priors_used**: **Substantial, and entirely at training time. This is the field
  that matters for this paper.** Full training composition, Table 3 (p18) plus p3, p14, p18:

  | Dataset | Description (verbatim from Table 3, p18) | Sampling strategy | Weight |
  |---|---|---|---|
  | Weighted PDB | "Ground truth PDB structures" | weighted | **0.60** |
  | Protein monomer distillation (Set1) | "Protein monomer predictions from MGnify using 1 model" | uniform | **0.35** |
  | Protein monomer distillation (Set2) | "Protein monomer predictions from MGnify using 5 models" | uniform | **0.03** |
  | OpenProteinSet subset | "Protein monomer predictions from Uniclust30" | uniform | **0.02** |

  - **Experimental structural prior:** the PDB itself, cut at **September 30, 2021** — p3:
    "Protenix is trained using experimental structures curated from the Protein Data Bank (PDB)
    [17] with a cutoff date of September 30, 2021". Weight 0.60.
  - **Distillation prior (40% of training weight combined):** p18: "In addition to WeightedPDB,
    we also use AlphaFold 2 predictions to train our model. We use representative sequences from
    MGnify [38] with greater than 200 residues as the distillation data source. Due to resource
    limitations, we run 5 models on a small part of the data and only 1 model (model-3) on the
    rest. As a supplement, we also use a subset of the OpenProteinSet [39]. All distillation
    datasets are filtered based on pLDDT to obtain high-quality training data." p3 attributes the
    predicted structures to "AlphaFold2 [2] and OpenFold [10]". **Note the pLDDT filter: the
    distillation set is selected by model confidence, so the model is trained on the subset of
    AF2/OpenFold output AF2/OpenFold was most confident about.**
  - **Chemistry prior:** CCD (Chemical Component Dictionary) snapshot **downloaded 2024-06-08**,
    RDKit conformers via `pdbeccdutils` v0.8.5 (p11). When RDKit conformer generation fails they
    fall back to **CCD *ideal* coordinates and explicitly refuse the representative coordinates**
    — p11: "we use the CCD ideal coordinates and do not use the representative coordinates **to
    avoid potential data leakage**." This is a deliberate, correctly-reasoned anti-leakage choice
    and belongs here rather than in `oracle_leakage`.
  - **Architectural prior:** the whole model is AF3's published architecture, re-implemented from
    the AF3 paper and its supplementary materials (p3, p11, p13). This is the prior that matters
    most for how the corpus should treat Protenix — see the deviations table.
  - **Not a defect.** Nothing above is oracle use; it is the design-time knowledge the model was
    built from.

### Deviations from AlphaFold 3

**This is the second main deliverable.** The paper is explicit that its value is "sharing our
reproduction experience" (p3) and it enumerates its own departures. Everything below is stated by
the authors; nothing is inferred. Grouped by kind, each with a page. **Bearing on
architecture-independence** is flagged in the last column: `SAME` means the deviation does not
make Protenix a different architecture; `DIFFERENT` means it is a genuine architectural or
data-regime difference; `TRAINING` means the architecture is unchanged but the trained weights
cannot be assumed to behave like AF3's.

| # | Deviation from AF3 | Verbatim / near-verbatim | Page | Bearing |
|---|---|---|---|---|
| **Data regime** | | | | |
| D1 | **One model, one cutoff, instead of AF3's two models with two cutoffs** | "In contrast to AF3, which trains two separate models with different data cutoffs (September 30, 2019, for Posebusters, and September 30, 2021, for other datasets), we opt to train a single model due to resource limitations." | p3–4 | TRAINING |
| D2 | PoseBusters V2 targets removed from training | "Targets from PoseBusters Benchmark Set Verison 2 (PoseBusters V2) are excluded to avoid data leakage." / "To avoid potential data leakage issue, we remove identical PDB IDs from our training set." | p4, p6 | TRAINING |
| D3 | **Only the protein-monomer distillation set is used; AF3's other distillation sets are dropped** | "We also simplified the hyperparameters considerably, as our training utilizes the Protein Monomer Distillation dataset only, excluding other distillation sets." | p14 | TRAINING |
| D4 | Distillation source and depth differ: MGnify representative sequences >200 residues, 5 AF2 models on only part of the data and **1 model (model-3) on the rest**, plus an OpenProteinSet/Uniclust30 subset; all pLDDT-filtered | "Due to resource limitations, we run 5 models on a small part of the data and only 1 model (model-3) on the rest." | p18, Table 3 p18 | TRAINING |
| D5 | **No templates at all** | "Templates. We do not use templates." | p11 | DIFFERENT |
| D6 | **Different MSA pipeline**: MMseqs2 + ColabFold, Uniref100 for pairing by taxonomy ID | "We search MSAs using MMSEQS2 [25] and ColabFold [7] MSA pipeline, and use MSAs from the Uniref100 [26] database for pairing (species are identified with taxonomy IDs)." | p11 | DIFFERENT |
| D7 | **No MSA for nucleic acid chains** | "We do not use MSA for nucleic chains." / "Protenix does not use MSA for nucleic chains." | p11, p8 | DIFFERENT |
| D8 | Parser: first occupancy, not largest, for alternative locations | "In selecting alternative locations, we use the first occupancy rather than the largest one. This is because we found that using the largest occupancy may result in some adjacent residues adopting different conformations, preventing the formation of covalent bonds and leading to chain breaks." | p11 | SAME |
| D9 | Reference features: CCD snapshot 2024-06-08, pdbeccdutils v0.8.5; CCD **ideal** coords on RDKit failure, never representative coords | "When RDKit conformer generation fails, we use the CCD ideal coordinates and do not use the representative coordinates to avoid potential data leakage." | p11 | SAME |
| D10 | Bond features restricted | "Bond features between tokens only include bonds within ligands, bonds between ligands and polymers, and bonds within non-standard residues." | p11 | SAME |
| D11 | Cropping: metals/ions excluded from **contiguous** cropping (retained in spatial); ligands and non-standard amino acids kept intact and never fragmented | "we discard metals and ions, as this approach cannot guarantee that cropped atoms remain close to each other" / "we ensure that ligands and non-standard amino acids remain intact and are not split into incomplete segments during cropping" | p11 | SAME |
| D12 | Chain permutation adapted to cropping: spatial cropping restricts the GT anchor to chains inside the crop, contiguous cropping does not; only entities with ≥4 resolved tokens are anchor candidates; polymer chains prioritised | "we only consider entities with at least four resolved tokens for anchor chains and prioritize polymer chains to reduce permutation complexity" | p11, p20 | SAME |
| **Algorithm corrections (Table 1, p12) — algorithm numbers refer to the AF3 Supplementary Materials** | | | | |
| D13 | **Algorithm 1, Line 10**: `{z_ij} = MsaModule` replaces `{z_ij} += MsaModule` | "The MsaModule itself contains residual connections for updating z, hence adding an additional residual update would be redundant." | p12 | DIFFERENT (residual path) |
| D14 | **Algorithm 3, Line 8**: condition on `b_ij^same_entity` replaces `b_ij^same_chain` | "Comparing the symmetry IDs (sym_id) only makes sense for chains that share the same entity ID… the original comparison would be logically flawed." | p12 | DIFFERENT (featurisation) |
| D15 | **Algorithm 18, Line 9**: `δ_l = (x_l^noisy − x_l^denoised)/t̂` replaces `δ_l = (x_l − x_l^denoised)/t̂` | "The original form in Line 9 does not align with Line 11… which follows an Euler method for solving ODEs. The correction ensures mathematical consistency." | p12 | DIFFERENT (sampler) |
| D16 | **Algorithm 23, Line 2**: `{b_i} += AttentionPairBias` replaces `{b_i} = AttentionPairBias` — a *restored* residual connection in the DiffusionTransformer | "Empirically we find the model does not converge well if residual connection is missing in the DiffusionTransformer block." | p12 | DIFFERENT (architecture) |
| D17 | **Algorithm 28, Line 11**: `x_l^align = R·x_l + µ_GT` replaces `R·x_l + µ` | "We believe this is a typo. Otherwise, this is mathematically inconsistent." | p12 | SAME (typo fix) |
| D18 | **Algorithm 31, Line 3**: distance bin edges `[3⅜ Å, 4⅝ Å, …, 21⅜ Å]` replace `[3⅜ Å, 5⅝ Å, …, 21⅜ Å]` | "We believe this is a typo. After fixing it, the distances can be discretized into 15 bins of equal width 1.25 Å." | p12 | DIFFERENT (distogram binning) |
| D19 | **Supp. 3.7.1, Equation (6)**: diffusion-loss weighting `(t̂² + σ_data²)/(t̂ × σ_data)²` replaces `(t̂² + σ_data²)/(t̂ + σ_data)²` | "We believe this is a typo because the per-sample weighting of the diffusion loss… is carefully designed in a principled way by the authors of EDM [29]." | p12 | DIFFERENT (loss) |
| **Architecture** | | | | |
| D20 | **Confidence head modified: LayerNorm added plus additional linear layers** | "we make slight modifications to the confidence head by incorporating LayerNorm and adding a few linear layers (see our released code). We find that the confidence loss does not converge as effectively when implemented exactly as described in the original paper." (also flagged p10: "We make slight modifications to the confidence head architecture in contrast to AF3") | p13, p10 | **DIFFERENT — and this is the head every confidence-based comparison runs through** |
| D21 | Zero-initialisation applied where AF3 does not specify it: identity-at-init residual layers, both linear layers in AdaptiveLayerNorm, and the N-cycle loop connection blocks in the Pairformer (AF3 Algorithm 1, line 8) | "we find that these zero-initializations help prevent dimensional collapse in the network weights and mitigate the explosion of hidden values." | p13 | TRAINING |
| **Training / engineering** | | | | |
| D22 | **BF16 mixed precision** instead of FP32 | "Compared to FP32 training, BF16 training significantly reduces peak memory usage and nearly doubles the actual training speed." | p13 | TRAINING (numerics) |
| D23 | Custom CUDA LayerNorm kernel (from FastFold / OneFlow), 30–50% end-to-end speedup | p13 | p13 | SAME |
| D24 | `DS4Sci_EvoformerAttention` kernels from DeepSpeed4Science, 10–20% speedup | p13 | p13 | SAME |
| D25 | Alternative update-step implementations to avoid large intermediate tensors; gradient checkpointing, in-place ops, tensor offloading, chunking (OpenFold-style) | "A direct implementation of the model update steps, as outlined in the AF3 paper, leads to the creation of unnecessarily large tensors." | p13 | SAME |
| D26 | **Far fewer training steps than AF3**: 75K initial + 15K fine-tune stage 1 + **only 4K** fine-tune stage 2; 192 GPUs over ~2 weeks | "Although we implement a multi-stage training setup similar to AF3, our model is trained with significantly fewer steps… We run only 4K steps for fine-tuning stage 2, which may be insufficient for adequately training the confidence head." | p14 | **TRAINING — and it directly caps the confidence head** |
| D27 | Hyperparameters simplified; stage configs are crop 384/640/640, diffusion batch 48/32/–, bond loss weight 0/1/–, distillation used in stages 1–2 only, PAE head trained only in stage 3 | Table 2, p14 | p14 | TRAINING |
| **Inference / ranking** | | | | |
| D28 | Recycles: 10 by default, and AF3's value had to be **inferred** | "we generally use 10 recycles unless otherwise noted. AF3 specifies its configuration for recycles only in Appendix 5.10… Therefore, we infer that AF3 likely used at least 10 recycles in their report." | p19 | SAME (matched by inference, not by statement) |
| D29 | Task-specific rankers: chain-pair ipTM for protein interfaces; `0.8·ipTM + 0.2·pTM − 100·has_clash` for dsDNA–protein (because three chains make chain-pair scores awkward); pLDDT for CASP15 RNA | p7, p9, p8 | p7–9 | DIFFERENT (selection rule) |
| D30 | *(Followed, not deviated)* stereochemistry penalty in the ranking score | "we follow AF3 and incorporate a penalty term to mitigate such stereochemistry violations in our score function when we perform sample ranking." | p6 | SAME |

  **Summary for the corpus.** Protenix is a **faithful re-implementation of the AF3 architecture**
  with a **materially different data regime** (no templates, a different MSA pipeline, no nucleic
  MSAs, one distillation set, one cutoff, far fewer steps) and **six algorithm-level departures
  the authors judged to be AF3's errors or ambiguities** (D13–D19), of which two are substantive
  rather than typographic: the restored residual in the DiffusionTransformer (D16) and the
  removed double residual on the MSA module (D13). The **confidence head is explicitly not AF3's**
  (D20) and was trained for only 4K steps (D26). **Protenix and AF3 should not be treated as
  independent architectures** — they are the same architecture with different weights, different
  input features and a handful of corrected lines. Any architecture-independence argument that
  rests on Protenix-vs-AF3 agreement is arguing from a shared design, and the paper says so
  itself: "We implement Protenix based on the descriptions provided in AF3 as part of our
  reproduction effort" (p3).

- **oracle_leakage**: **All seven routes considered separately.** Net: **no pipeline leakage of
  target-state knowledge; two routes are present and are evaluation-side (routes 5 and 6), and
  both are explicitly labelled by the authors rather than hidden.**

  1. **Structures used as input or template — NONE FOUND.** p11: "Templates. We do not use
     templates." Inputs are sequence + MSA + CCD chemistry only; the featurisation is described
     in full on p11 and contains no coordinate input. Additionally the one place deposited
     coordinates could have entered through chemistry is closed deliberately, p11: "we use the
     CCD ideal coordinates and do not use the representative coordinates to avoid potential data
     leakage." Protocol described p11 and p19 (Appendix B).
  2. **State annotations from a curated database (GPCRdb / KLIFS / Kincore) — NONE FOUND.** No
     state-annotated database appears anywhere in the paper. The only databases used are PDB,
     MGnify, Uniref100, Uniclust30/OpenProteinSet, and the CCD (p11, p18). Protocol described
     p11, p18.
  3. **Cluster labels derived from known states — NONE FOUND.** Clustering appears twice and
     neither is a state label: (a) **interface clusters** used only to average metrics, Fig 1
     caption p4 — "Metrics are averaged within and across interface clusters; N represents the
     number of clusters"; (b) **sequence-homology groups** (0–30 / 30–95 / 95–100) used for the
     stratified analysis in Fig 2D, p5. Both are sequence/interface similarity, not conformation.
     Protocol described p4, p5, p18.
  4. **Hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states —
     NONE FOUND for *states*. One evaluation-set-facing tuning choice is present and is recorded
     here because the schema asks for it, not because it concerns conformational state.** p6:
     "Similar to AF3, the model cannot consistently generate samples with correct chirality and
     without steric clashes, hence we follow AF3 and incorporate a penalty term to mitigate such
     stereochemistry violations in our score function when we perform sample ranking. **This
     penalty term has successfully improved the PB-valid success rate by over 10%**, though there
     still exists a roughly 5% chance that we fail to predict the correct chirality." The penalty
     is a *ranking-score component whose benefit is quantified on the very PoseBusters V2 set it
     is then scored on*. It is inherited from AF3 rather than invented, and it is a physical-
     plausibility penalty rather than a target-specific one, so this is weak — but a reader
     should know the headline PB-Valid number is the post-penalty number. Related but not
     leakage: the "new natural common ligands" category in Fig 2C is defined by intersecting
     PoseBusters V2 with the *training* set (Fig 2 caption, p5: "we select other 75 NCL… in
     PoseBusters V2 that meet the same criteria within our training set") — that is a post-hoc
     analysis stratification, disclosed, and is the point of the analysis rather than a defect.
     No seed sweep, no per-target tuning, no stopping criterion tuned on the test set is
     described anywhere. Protocol described p13–14, p19.
  5. **Success defined post hoc by RMSD/TM to a structure they had — PRESENT, by construction,
     and this is what a structure-prediction benchmark is.** Every metric in the paper is a
     distance to a deposited reference: ligand pocket-aligned RMSD ≤ 2 Å (p4), DockQ > 0.23
     (Fig 1 caption, p4), interface LDDT (p4, p9), LDDT and TM-score against the CASP15 reference
     (p8–9). Verbatim, p4: "The success rate is defined as the percentage of predictions for which
     the pocket aligned ligand root-mean-square deviation (RMSD), as defined in [4], between the
     ground truth and the prediction is no greater than 2 Å." Neither threshold is independently
     justified — both are inherited from AF3. **Additionally, the evaluation-time chain and atom
     permutation is chosen to minimise RMSD to the ground truth** (p20–21: "selecting the
     permutation which minimizes the global RMSD"; for ligand complexes, "we generate all
     possible combinations of pockets and ligands, and then select the permutation resulted in
     the lowest ligand-specific RMSD"). That is standard practice and is applied to the baselines
     too (p9: "we apply the same evaluation approach to both Protenix and RF2NA"), but it is
     reference-facing and is recorded.
  6. **Best/worst model labels assigned against a held reference — PRESENT and explicitly
     labelled "oracle".** p5, Fig 2 caption: "'Oracle' refers to the samples with the lowest
     RMSD". p7: "including separate scores for best (oracle), median, and top-1 ranked
     predictions." The oracle arm appears in the **headline** Figure 1B alongside median and
     selected, and as the top curve in Figure 2B. **Assessment: this is a disclosed upper-bound
     arm, not disguised leakage.** The paper's own headline claim rests on the *confidence-ranked*
     arm, and it explicitly says the gap between them is a defect of its ranker, p6: "the selected
     results still lag behind the best candidates among all samples, suggesting room for
     improvement with a better sample ranker." One caution for reuse: in Fig 1B the oracle bars
     for Protenix and AF2.3 sit next to each other in the same panel as the selected bars, so a
     careless read of that figure can pick up an oracle number as if it were a deployable one.
  7. **Design-level oracle use (route 7, weaker than pipeline leakage) — PRESENT, confined to the
     case-study figures.** All five render figures show cases chosen *after* the reference was
     known, in both directions: successes (p6: "We inspect some challenging cases to assess
     Protenix's ability…"; Fig 3, Fig 5, Fig 7) and failures (p7: "We also inspect the cases where
     the RMSD of predicted ligands exceeds 2 Å and find that, in some instances, the predictions
     are reasonable"; Fig 4). The memorisation analysis in Fig 9 is likewise selected against
     known references (p10: "We review the showcase examples presented in the AF3 paper to
     evaluate how our model performs on these cases… we further investigated the training set and
     noted that some of these complexes share significant similarities with certain training
     samples"). **This is design-level only** — the model was given nothing, and the selection is
     post-hoc illustration, not conditioning. The quantitative benchmarks (Figs 1, 2, 6, 8) are
     whole-set and unselected. Note the Fig 9 case is design-level oracle use turned *against*
     the paper's own result, which is to its credit.

- **prospective**: **no.** Every evaluation is retrospective against structures deposited before
  the paper was written: PoseBusters V2 is a fixed 2023 benchmark (p18), the LowH Recent PDB set
  is "PDB targets released between 2022-05-01 and 2023-01-12" (p18), and the CASP15 RNA targets
  were "publicly available as of December 1, 2023" (p8, p19). No prediction is made before its
  answer existed. The set is *post-training-cutoff*, which is a real and well-executed
  anti-memorisation design (see below) but is not prospectivity. The pipeline is clean of state
  bias, so the paper is retrospective in evaluation and unbiased in pipeline — the reverse of the
  usual failure mode in this corpus.
- **state_metric**: **NOT APPLICABLE — the paper defines no conformational-state predicate of any
  kind.** There is no active/inactive call, no state coordinate, no state-classification arm, and
  no discussion of alternative protein conformations anywhere in 21 pages. What it does define,
  recorded here so the row is not empty for the reader, are **accuracy** metrics, all of them
  continuous distances to a reference with an inherited threshold:
  - **pocket-aligned ligand RMSD, threshold 2 Å**, "as defined in [4]" (p4) — threshold taken
    from AF3, not independently justified.
  - **DockQ, threshold 0.23** for interface success (Fig 1 caption, p4) — threshold stated, not
    justified in this paper.
  - **interface LDDT** for protein–nucleotide interfaces (p4, p9) — no threshold, reported as a
    continuous value.
  - **LDDT and TM-score** for CASP15 RNA, recomputed with OpenStructure (p8–9) — no threshold.
  - **PB-Valid**: all 18 PoseBusters validity criteria satisfied (p4, p6) — a binary predicate,
    but on physical plausibility, not on conformational state.
- **metric_saturation**: **YES, numerically, in two places.**
  1. **Figure 2E (p5), the 18 PoseBusters validity checks: most criteria sit at or within a
     hair's breadth of 1.0 for both models.** File loaded, sanitization, molecular formula,
     molecular bonds, double bond stereochemistry, bond lengths, bond angles, internal energy,
     aromatic ring flatness, double bond flatness, min distance to inorganic cofactors, and the
     three volume-overlap checks are all effectively at ceiling; only tetrahedral chirality
     (~0.95 Protenix / ~0.93 AF3), internal steric clash and min-distance-to-protein separate the
     two models at all. The panel therefore carries almost no discriminating information, and the
     ~5% chirality failure the authors quote (p6) is the entire signal.
  2. **Figure 2B (p5): all four RMSD-threshold curves plateau above ~0.93 by 6–8 Å** and become
     indistinguishable; the curves only separate below ~2.5 Å. The oracle curve is at ceiling
     across most of the plotted range.
  *(Axis truncation in Figs 1, 2A/C/D/E and 6 is a figure defect and is recorded in `hides` on
  the corresponding F rows, not here, per v3 rule 9.)*
- **directional_control**: **NONE — NOT APPLICABLE as a state handle.** The method cannot be
  instructed which conformation to produce; there is no partner-conditioning experiment, no
  ligand-conditioning experiment, no template handle (templates are off, p11), no state-filtered
  MSA, no latent intervention. The **only** sampling handles are: **model seed** (5) and
  **diffusion sample index** (5 per seed), plus **recycle count** (10 default, p19). Cofolding
  partners are supplied as part of the input complex definition, but no experiment varies them to
  steer a state — p7 is explicit that the effect of extra chains was not even measured: "Our
  model predicts the complete complex, though we do not assess whether including additional
  chains in the input influences performance." Directional control is listed only as **future
  work**, p15: "Certain features may be particularly useful for specific applications, such as
  predicting structures with incorporated priors on partial structures or interactions, or making
  predictions without utilizing the MSA feature." Tagged `seed-only`.

- **anti_memorization_design**: **YES — a stated cutoff and a post-cutoff, homology-filtered
  held-out set. This is the authoritative value for the corpus.**

  **THE TRAINING CUTOFF, VERBATIM (p3):**
  > "Protenix is trained using experimental structures curated from the Protein Data Bank (PDB)
  > [17] with a **cutoff date of September 30, 2021** and predicted structures of protein monomers
  > with AlphaFold2 [2] and OpenFold [10] (See details in Table 3 and Appendix A.1)."
  > — p3, Section 2.1 Overview, first sentence.

  Restated twice more, and each restatement is worth quoting because they carry the contrast with
  AF3 and the ISO-format spelling:
  > "In contrast to AF3, which trains two separate models with different data cutoffs (September
  > 30, 2019, for Posebusters, and September 30, 2021, for other datasets), we opt to train a
  > single model due to resource limitations."
  > — p3–4 (sentence begins on p3, completes on p4).

  > "We note that Protenix is trained with **PDB cut-off 2021-09-30**, hence the improvement of
  > performance may be attributed to additional training data."
  > — p6, Section 2.2, "Similarity analysis".

  So: **September 30, 2021 (2021-09-30) is the single training cutoff for Protenix v1.** There is
  exactly one model and one cutoff. Any corpus paper defining a held-out set against Protenix
  should use 2021-09-30. Note the two traps: (a) AF3's PoseBusters model uses **2019**-09-30, and
  Protenix's PoseBusters comparison is therefore against a *differently-cut* AF3 — the paper
  flags this itself, p4: "We acknowledge the differences in the cutoff dates and present an
  analysis in Section 2.2 to distinguish genuine improvements on Posebusters from potential data
  overlap"; (b) the **CCD chemistry snapshot is dated 2024-06-08** (p11), well after the
  structure cutoff, so the cutoff bounds deposited *coordinates*, not ligand *chemistry
  definitions*.

  **Held-out set, n, and how the cutoff was defined:**
  - **Low Homology Recent PDB Set** — p18: "This set consists of PDB targets released between
    **2022-05-01 and 2023-01-12**, filtered for **sequence similarity below 40%** to better assess
    model generalization. We apply the same token cutoff to evaluate models on structures with
    fewer than 2560 tokens." Both bounds are strictly after 2021-09-30, so the whole set is
    post-cutoff. n: **993 protein–protein interface clusters, 64 protein–antibody clusters**
    (Fig 1B, p4), **25 protein–RNA and 38 protein–dsDNA structures** (Fig 1C, p4; p19). Curated
    by following AF3's Supplementary Information; the nucleic subset is screened from "Table 14
    of the AF3 supplementary materials" (p19).
  - **PoseBusters V2 (n = 308)** is **not** post-cutoff for Protenix and the authors know it.
    Their mitigation is exclusion by identity rather than by date — p4: "Targets from PoseBusters
    Benchmark Set Verison 2 (PoseBusters V2) are excluded to avoid data leakage"; p6: "To avoid
    potential data leakage issue, we remove identical PDB IDs from our training set." **Identical
    PDB IDs only — homologues and near-duplicates of PoseBusters targets remain in training**,
    which is precisely why the homology-stratified control in Fig 2D exists.
  - **CASP15 RNA (n = 8)**: targets "publicly available as of December 1, 2023" (p8, p19), also
    post-cutoff, but n = 8 is unpowered.
  Tagged `anti-memorization`.

- **anti_memorization_control**: **RUN AND ANALYSED — this paper is unusual in the corpus for
  actually running the arm, and for reporting a result that cuts against itself.** Three distinct
  control analyses:
  1. **Homology-stratified success rate, both cutoffs (Figure 2D, p5).** PoseBusters V2 targets
     binned by protein sequence homology to the training set at 0–30 / 30–95 / 95–100, computed
     **twice** — once against the 2019-cutoff training set (n = 30 / 90 / 188) and once against
     the 2021-cutoff training set (n = 15 / 52 / 241). This directly isolates whether Protenix's
     PoseBusters advantage comes from the extra two years of data. Verdict, p6: "On the target
     side, Protenix outperforms AF3-2019 on high homology group but performs slightly worse on
     other targets." **UNPOWERED in the cell that matters most**: the low-homology (0–30) bin
     under the 2021 cutoff has **n = 15**, and the error bar on it spans roughly 0.67–0.99.
  2. **Common vs non-common ligand stratification (Figure 2C, p5).** Ligands split into
     "not common" / "new natural common ligands" (75, defined against the Protenix training set)
     / "old natural common ligands" (50, AF3's definition). Verdict, p6: "compared to AF3-2019,
     Protenix performs better on common ligands, likely benefiting from the additional training
     data. However, since they exhibit the same performance on non-common ligands, we can
     conclude that our model generalizes as well as AF3-2019."
  3. **Training-set nearest-neighbour inspection of the showcase cases (Figure 9, p10, and the
     Limitations paragraph).** Verbatim and load-bearing, p10: "Upon observing similar results, we
     further investigated the training set and noted that some of these complexes share
     significant similarities with certain training samples. For instance, as shown in Figure 9,
     the protein-DNA complex 7PZB has a close counterpart in the training set (3MZH), as does the
     protein-ligand complex 7XFA, which is similar to 5OAX. **This suggests that the accuracy of
     both Protenix and AF3 may partially result from memorization, indicating the need for more
     out-of-distribution (OOD) test sets to better assess its generalizability.**"
  **Assessment**: arms 1 and 2 are real quantitative control arms, run and reported, with the
  low-homology cell unpowered (n = 15). Arm 3 is a qualitative two-example demonstration with no
  quantitative panel — the strongest claim in the paper's Limitations rests on two hand-picked
  pairs and no distribution. That is a `hides` entry on Figure 9. Mark: **RUN, partially
  UNPOWERED.**

- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Homology stratification of PoseBusters V2 against the **2019** training set (n = 30 / 90 / 188) | That Protenix's PoseBusters edge is just recall of pre-2019 neighbours; makes the comparison with AF3-2019 interpretable | p5 (Fig 2D left), p6 |
  | Homology stratification against the **2021** training set (n = 15 / 52 / 241) | That the extra 2019→2021 training data is what produced the edge; this is the arm that isolates the cutoff difference | p5 (Fig 2D right), p6 |
  | Common vs non-common ligand split (not common / 75 new NCL / 50 old NCL) | That the gain is confined to ligands seen often in training; the non-common bin is where generalisation is read | p5 (Fig 2C), p6 |
  | Removal of identical PDB IDs of PoseBusters V2 targets from the training set | Exact-structure memorisation of the ligand benchmark. Does **not** rule out homologue memorisation | p4, p6 |
  | Post-cutoff, ≤40%-identity Low Homology Recent PDB set (2022-05-01 → 2023-01-12) | Both temporal leakage and sequence-similarity leakage for the protein and nucleic-acid interface benchmarks | p18 |
  | **Oracle vs median vs confidence-ranked** arms, run for both Protenix and the baseline | That the reported accuracy is a ranker artefact; separates generative capability from selection capability. It is an oracle arm, so it is an upper bound, not a deployable number | p5 (Fig 2B), p7 (Fig 1B) |
  | "All sample" arm over all 25 samples (Fig 2B) | That a favourable single sample was cherry-picked | p5 |
  | Stereochemistry-penalty ablation, reported as a delta only ("improved the PB-valid success rate by over 10%") | Nothing is *ruled out*; recorded here because it is the one ablation number the paper gives, and it is quoted without a figure | p6 |
  | Same evaluation pipeline applied to Protenix and RF2NA ("we apply the same evaluation approach to both Protenix and RF2NA") | That the nucleic-acid margin over RF2NA is a metric-implementation artefact. Note it does **not** cover AF3, whose numbers are transcribed | p9 |
  | Recomputation of LDDT/TM-score with OpenStructure for RF2NA, AIchemy_RNA2 and Protenix | Tool-to-tool metric drift on CASP15 RNA. AF3's values are taken from Bernard et al. and are *not* recomputed | p8–9 |
  | Single-seed evaluation of Protenix on CASP15 RNA, to match AF3's single-seed evaluation | That Protenix's RNA parity with AF3 comes from a 5× larger sampling budget | p8 |
  | Training-set nearest-neighbour lookup for the AF3 showcase cases (7PZB→3MZH, 7XFA→5OAX) | Nothing quantitatively; it *establishes* the memorisation concern rather than excluding it. n = 2, no distribution | p10 (Fig 9) |
  | **NOT RUN**: any ablation of the algorithm corrections D13–D19 individually | Whether each correction actually matters. Only D16 gets a qualitative justification ("does not converge well"); the rest are asserted | p12 |
  | **NOT RUN**: any templates-on arm | Whether the absence of templates costs accuracy relative to AF3 | p11 |
  | **NOT RUN**: any ablation of the distillation sets or their weights | Whether the 40% distillation weight helps or hurts | p14, p18 |

- **confidence_as_discriminator**: **Used as an accuracy discriminator and validated as such;
  never used as a conformational-state discriminator, because no state axis exists.**
  - **What is predicted**: **pLDDT**, a **PAE head**, **pTM**, **ipTM**, and **chain-pair ipTM**;
    plus a composite **complex ranking score = 0.8·ipTM + 0.2·pTM − 100·has_clash** (p9), and a
    stereochemistry-violation penalty folded into the ranking score (p6). Which score ranks which
    task: **chain-pair ipTM** for protein interfaces (p7: "the ranker used for protein interfaces
    is the 'chain pair ipTM' confidence"); the **complex ranking score** for dsDNA–protein, "This
    is because, for dsDNA-protein interfaces, three chains are involved, making it difficult to
    use chain pair scores directly" (p9); **pLDDT** for CASP15 RNA (p8: "The top-ranked sample of
    each structure, selected based on pLDDT, is used for evaluation"); the confidence head for
    PoseBusters ("confidence ranked", p5).
  - **What is claimed, verbatim (p10)**: "After training the confidence head, we observe that
    predicted scores can be used to select interfaces on low homology recentPDB dataset. As
    illustrated in Figure 8, a positive Pearson correlation (ρ>0.5) is observed between predicted
    scores and interface DockQ scores for diverse interface types, including protein-protein and
    protein-nucleic acid interactions. Given that our PAE head has been trained for only 4K steps,
    there is still huge potential for further improvement."
  - **Validation actually performed**: Figure 8 (p10), chain-pair ipTM binned into five bins
    against DockQ over 24,650 interfaces. **Pearson ρ = 0.5774 (all interfaces), 0.6007
    (protein–protein), 0.5300 (protein–nucleic acid)** — printed inside the panels. So the claim
    is validated *for interface accuracy ranking*, on a post-cutoff low-homology set, at
    modest correlation (ρ² ≈ 0.28–0.36; roughly a third of DockQ variance).
  - **Where it demonstrably fails**: the confidence-ranked arm sits well below the oracle arm at
    every RMSD threshold (Fig 2B, p5) and the authors concede it, p6: "the selected results still
    lag behind the best candidates among all samples, suggesting room for improvement with a
    better sample ranker"; and p8: protein-antibody "top-ranked predictions are on par with those
    of AF2.3, indicating potential for improvement in the sample ranker" — i.e. Protenix's oracle
    advantage on antibodies is not realisable through its confidence score.
  - **Caveat for the corpus**: the confidence head is **not AF3's** (D20) and was trained for only
    **4K steps** (D26, p14: "which may be insufficient for adequately training the confidence
    head"). Protenix confidence values are therefore not a proxy for AF3 confidence values.
  Tagged `confidence-as-discriminator`.

## D. Claims

- **central_conclusion**: Protenix is a from-scratch open reproduction of AlphaFold 3 — weights,
  inference code, trainable code and preprocessed data all released — that matches or slightly
  exceeds AF3 on PoseBusters V2 ligand docking, beats AF2.3 on protein interfaces, matches AF3
  and beats RF2NA on nucleic acids, and reaches this with one model, one 2021-09-30 cutoff, no
  templates, one distillation set and far fewer training steps than AF3. Along the way the authors
  document six algorithm-level errors or ambiguities they found in the AF3 paper and correct them.
  The paper's own closing caveat is that some of the accuracy of both Protenix and AF3 may be
  memorisation, and that better out-of-distribution test sets are needed.

- **necessity_claims** (verbatim + page; claims that something is required, impossible, or
  cannot be done):
  - p3: "However, the lack of comprehensive training code and preprocessed data **remains a
    barrier** for researchers aiming to fully reconstruct and utilize these models."
  - p3: "The absence of code and certain ambiguities and typographical errors in the AF3 paper
    present additional challenges for machine learning and computational biology researchers
    seeking to reproduce or improve the model."
  - p12 (Table 1, Algorithm 23): "Empirically we find the model **does not converge well if
    residual connection is missing** in the DiffusionTransformer block."
  - p13: "We find that the confidence loss **does not converge as effectively** when implemented
    exactly as described in the original paper."
  - p13: "Despite having only about 386 million parameters, AF3 **requires an enormous amount of
    computation**."
  - p13: "A naive implementation of LayerNorm in PyTorch [34] **often encounters memory
    limitations**."
  - p6: "Similar to AF3, the model **cannot consistently generate** samples with correct chirality
    and without steric clashes"
  - p10: "This suggests that the accuracy of both Protenix and AF3 may partially result from
    memorization, indicating the **need for more out-of-distribution (OOD) test sets** to better
    assess its generalizability."
  - p9: "This is because, for dsDNA-protein interfaces, three chains are involved, **making it
    difficult to use chain pair scores directly**."
  - p19: "RoseTTAFold2NA **can only input up to 1000 residues**, hence the dataset does not include
    systems with a total residue count exceeding 1000."
  - p11: "In our contiguous cropping method, we discard metals and ions, as this approach **cannot
    guarantee** that cropped atoms remain close to each other."
  - p14: "We run only 4K steps for fine-tuning stage 2, **which may be insufficient** for
    adequately training the confidence head."

- **novelty_claims** (verbatim + page):
  - p1 (title): "Protenix — **Advancing** Structure Prediction Through a **Comprehensive**
    AlphaFold3 Reproduction"
  - p4: "This suggests that Protenix **represents the current state-of-the-art (SOTA) model for
    the protein-ligand cofolding task**."
  - p3: "**As a fully open-source model**, it empowers researchers to generate novel predictions
    and fine-tune the model for specialized applications."
  - p3: "We have **open-sourced Protenix, providing model weights, inference code, and trainable
    code** for research purposes, as detailed in Section 4."
  - p3: "Open-source initiatives like HelixFold3 [14] and Chai-1 [15] have made significant
    strides in democratizing access to these advanced models. However, the lack of comprehensive
    training code and preprocessed data remains a barrier…" — the differentiation claim against
    the other open AF3 reproductions.
  - p3 (about AF3, not itself, recorded because it is the framing the paper argues from): "Among
    these, AlphaFold 3 (AF3) [4] has **set a new milestone**, representing a **significant leap
    forward** in this domain."
  - p8: "It highlights the **potential applicability of Protenix as a tool for biology and
    pharmacology research**, helping with hypothesis testing and uncovering novel mechanisms which
    can serve as the starting point for the development of new therapeutics."
  - p14: "The processed data includes time-consuming MSA (multiple sequence alignment) search
    results, **covering all instances in the wwPDB**."
  - No "first" claim is made anywhere. The paper is careful to position itself as a reproduction.

- **stated_limits** (the authors' own):
  - **Memorisation, p10, the strongest self-limit in the paper**: "This suggests that the accuracy
    of both Protenix and AF3 may partially result from memorization, indicating the need for more
    out-of-distribution (OOD) test sets to better assess its generalizability."
  - **Confidence head under-trained**: p10 "Given that our PAE head has been trained for only 4K
    steps, there is still huge potential for further improvement"; p14 "We run only 4K steps for
    fine-tuning stage 2, which may be insufficient for adequately training the confidence head."
  - **Ranker is the bottleneck**: p6 "the selected results still lag behind the best candidates
    among all samples, suggesting room for improvement with a better sample ranker"; p8 "our
    top-ranked predictions are on par with those of AF2.3, indicating potential for improvement in
    the sample ranker."
  - **Chirality/clash failures persist**: p6 "there still exists a roughly 5% chance that we fail
    to predict the correct chirality."
  - **Single model / single cutoff is a resource compromise**: p3–4 "we opt to train a single
    model due to resource limitations"; and the cutoff mismatch with AF3-2019 is acknowledged,
    p4: "We acknowledge the differences in the cutoff dates."
  - **Undertrained relative to AF3**: p14 "our model is trained with significantly fewer steps";
    "we also simplified the hyperparameters considerably, as our training utilizes the Protein
    Monomer Distillation dataset only, excluding other distillation sets."
  - **Input-composition effect unmeasured**: p7 "Our model predicts the complete complex, though
    we do not assess whether including additional chains in the input influences performance."
  - **The evaluation sets are not provably AF3's**: p18 "our dataset still differs in PDB and
    cluster numbers compared to the AF3 paper, despite our efforts with different tools and
    settings"; p9 "The number of structures in our curated dataset matches the count reported in
    AF3's Figure 1.c, although we cannot guarantee the datasets are identical"; p19 "Although the
    number here matches that in AF3, it does not necessarily mean the evaluation was conducted on
    an identical evaluation set, which may lead to discrepancies in the metrics."
  - **A baseline discrepancy they cannot explain**: p9 "Notably, the performance of RF2NA differs
    from that reported in AF3, which may be attributed to discrepancies in the dataset or the
    evaluation tools used."
  - **AF3's recycle count had to be guessed**: p19 "Therefore, we infer that AF3 likely used at
    least 10 recycles in their report."
  - **The metrics themselves are questioned**: p7 "These cases reveal areas for improvement in the
    evaluation metrics."
  - **Evaluation is hard and not yet standardised**: p15 "we observe that the evaluation procedure
    is highly complex, demanding close attention to numerous details… We plan to continue
    enhancing our evaluation tools and may eventually open-source a general-purpose evaluation
    platform to support fair model comparisons."
  - **Initialisation not studied**: p13 "We do not conduct an extensive analysis of the impact of
    different initialization strategies."

- **stance**: **`background` on the tool + `precedent` on the memorisation finding.**
  *Provisional — the user's call.*
  - **background**: this is the origin paper for one of the backbones the corpus and the
    manuscript use. Its job in the corpus is to fix what Protenix v1 *is* — its cutoff, its
    training data, its sampling defaults, its distance from AF3 — so that any claim about Protenix
    elsewhere is anchored.
  - **precedent**: the Limitations paragraph on p10 is a **model-authors' own admission** that
    accuracy "may partially result from memorization" and that OOD test sets are needed. A
    memorisation argument that can cite the model's own authors is stronger than one that cites
    only external critics.
  - A third reading is available and should be flagged rather than adopted: this paper is mild
    **`contrast` on rigour**, in that the memorisation claim rests on two hand-picked pairs with
    no distribution (Fig 9), and that almost no number in the paper is printed in text. Not
    recorded as a stance because the paper is not making a conformational claim we are contesting.

## E. Quantitative comparators

- **metrics_reported**: One row per metric. `(panel)` = read from a rendered panel and approximate
  to ±0.01–0.02; unmarked values are printed in the paper.

| metric | value | units | measured against | page |
|---|---|---|---|---|
| PoseBusters V2 RMSD ≤2 Å success rate, confidence-ranked | **≈0.815** *(panel)* | fraction of 308 structures | Protenix, top-1 by confidence, vs deposited ligand pose | p5 (Fig 2A), p4 (Fig 1A) |
| PoseBusters V2 RMSD ≤2 Å success rate, confidence-ranked | **≈0.803** *(panel)* | fraction of 308 | **AF3-2019**, from AF3's released predictions rescored by the authors | p5 (Fig 2A), p4 (Fig 1A) |
| PoseBusters V2 PB-Valid success rate (all 18 criteria) | **≈0.752** *(panel)* | fraction of 308 | Protenix | p5 (Fig 2A) |
| PoseBusters V2 PB-Valid success rate | **≈0.730** *(panel)* | fraction of 308 | AF3-2019 | p5 (Fig 2A) |
| Effect of the stereochemistry penalty term on PB-Valid | **"improved… by over 10%"** | relative improvement in PB-valid success rate | Protenix ranking with vs without the penalty | p6 |
| Residual chirality failure rate | **"roughly 5%"** | fraction of predictions | Protenix on PoseBusters V2 | p6 |
| RMSD success rate at 2 Å, **oracle** (lowest-RMSD of 25) | **≈0.86** *(panel)*, highest curve at every threshold | fraction of 308 | Protenix oracle vs AF3 confidence-ranked | p5 (Fig 2B) |
| RMSD success rate at 2 Å, **all 25 samples pooled** | **≈0.79** *(panel)* | fraction | Protenix, all samples | p5 (Fig 2B) |
| RMSD success rate plateau at 8 Å threshold | **≈0.93–0.96** *(panel)*, all four curves converged | fraction | all arms — saturation region | p5 (Fig 2B) |
| PoseBusters success rate, **not-common** ligands | **≈0.72 Protenix vs ≈0.72 AF3** *(panel)* — equal | fraction | the generalisation bin; basis for "our model generalizes as well as AF3-2019" (p6) | p5 (Fig 2C), p6 |
| PoseBusters success rate, **new** natural common ligands (75) | **≈0.79 Protenix vs ≈0.755 AF3** *(panel)* | fraction | ligands common in the 2021 training set | p5 (Fig 2C) |
| PoseBusters success rate, **old** natural common ligands (50) | **≈0.83 Protenix vs ≈0.815 AF3** *(panel)* | fraction | AF3's own NCL definition | p5 (Fig 2C) |
| PoseBusters success rate by homology, **2019 cutoff**: 0–30 / 30–95 / 95–100 | **≈0.89/0.795/0.82 Protenix vs ≈0.89/0.82/0.78 AF3** *(panel)* | fraction | n = 30 / 90 / 188 | p5 (Fig 2D left) |
| PoseBusters success rate by homology, **2021 cutoff**: 0–30 / 30–95 / 95–100 | **≈0.86/0.745/0.83 Protenix vs ≈1.00/0.82/0.78 AF3** *(panel)* | fraction | n = **15** / 52 / 241 — the 0–30 cell is unpowered | p5 (Fig 2D right) |
| PoseBusters tetrahedral chirality check | **≈0.95 Protenix vs ≈0.93 AF3** *(panel)* — the only clearly separating validity criterion | fraction passing | 18-criterion breakdown | p5 (Fig 2E) |
| All protein–protein interfaces, DockQ >0.23 success rate — **oracle** | **≈0.775 Protenix vs ≈0.75 AF2.3** *(panel)* | fraction of 993 interface clusters | LowH Recent PDB; AF2.3(5×5), 20 recycles vs Protenix 10 recycles | p4 (Fig 1B), p7 |
| All protein–protein interfaces — **median** | **≈0.685 Protenix vs ≈0.65 AF2.3** *(panel)* | fraction of 993 clusters | as above | p4 (Fig 1B) |
| All protein–protein interfaces — **selected (top-1 by chain-pair ipTM)** | **≈0.71 Protenix vs ≈0.695 AF2.3** *(panel)* | fraction of 993 clusters | the deployable number | p4 (Fig 1B), p7 |
| Protein–antibody interfaces — **oracle** | **≈0.405 Protenix vs ≈0.375 AF2.3** *(panel)* | fraction of 64 clusters | LowH Recent PDB | p4 (Fig 1B) |
| Protein–antibody interfaces — **median** | **≈0.17 Protenix vs ≈0.135 AF2.3** *(panel)* | fraction of 64 clusters | | p4 (Fig 1B) |
| Protein–antibody interfaces — **selected** | **≈0.27 Protenix vs ≈0.27 AF2.3** *(panel)* — **parity, the paper's one stated loss** | fraction of 64 clusters | p8: "our top-ranked predictions are on par with those of AF2.3" | p4 (Fig 1B), p8 |
| Protein–RNA interface LDDT | **≈0.355 Protenix, ≈0.19 RF2NA (rerun), ≈0.40 "AF3 in AF3", ≈0.185 "RF2NA in AF3"** *(panel)* | interface LDDT | 25 structures; AF3 value transcribed from the AF3 paper, not rerun | p4 (Fig 1C) |
| Protein–dsDNA interface LDDT | **≈0.73 Protenix, ≈0.235 RF2NA (rerun), ≈0.66 "AF3 in AF3", ≈0.29 "RF2NA in AF3"** *(panel)* | interface LDDT | 38 structures; note RF2NA rerun ≠ RF2NA-in-AF3, unexplained (p9) | p4 (Fig 1C) |
| CASP15 RNA mean LDDT | **≈0.575 Protenix, ≈0.57 AF3, ≈0.42 RF2NA, ≈0.655 AIchemy_RNA2** *(panel)* | LDDT (OpenStructure) | 8 targets, single seed for both Protenix and AF3 | p4 (Fig 1D), p9 (Fig 6A) |
| CASP15 RNA per-target TM-score | 8 grouped bars per method, range ≈0.15–0.80 *(panel)*; no mean printed | TM-score (OpenStructure) | 8 targets, 4 methods | p9 (Fig 6B) |
| Confidence↔accuracy correlation, **all interfaces** | **ρ = 0.5774** | Pearson r, chain-pair ipTM vs DockQ | 24,650 interfaces, LowH Recent PDB | p10 (Fig 8A) |
| Confidence↔accuracy correlation, **protein–protein** | **ρ = 0.6007** | Pearson r | 16,595 interfaces | p10 (Fig 8B) |
| Confidence↔accuracy correlation, **protein–nucleic acid** | **ρ = 0.5300** | Pearson r | 8,055 interfaces | p10 (Fig 8C) |
| AF3 parameter count (stated of AF3; Protenix's own count never given) | **≈386 million** | parameters | AF3 | p13 |
| Training compute | **192 GPUs, ~2 weeks** | — | Protenix full training | p14 |
| Training steps | **75K initial + 15K FT-1 + 4K FT-2** | optimiser steps | Protenix; AF3's count not stated for comparison | p14 |
| Custom LayerNorm kernel speedup | **30–50%** | end-to-end training speed improvement | vs PyTorch native LayerNorm | p13 |
| DS4Sci_EvoformerAttention speedup | **10–20%** | end-to-end training speed improvement | vs baseline attention | p13 |
| Alternative-conformation case, 7LOE | **42% vs 58%** | crystallographic occupancy of the two ligand conformers | the "failure" Protenix predicted the minor conformer of | p7 |

- **n_predictions**: recorded per the schema as **samples per target / targets / total, separately**.
  - **Samples per target: 25** — p4: "For each PDB entry, we follow AF3's inference setup,
    generating 25 predictions using 5 model seeds, with each seed producing 5 diffusion samples.
    The predictions are ranked using confidence scores." Restated p19: "Unless specified, we
    generate 25 samples using 5 model seeds."
  - **Exception — CASP15 RNA: 5 samples per target (single seed)**, to match AF3's evaluation
    protocol. p8: "Since the authors evaluted AF3's performance based on a single seed, we also
    report the performance of Protenix using a single seed instead of five seeds."
  - **Other inference defaults**: **10 recycles** by default (p19); no cropping at inference
    (p19); **asymmetric unit** predicted for PoseBusters V2, **first bioassembly** for all other
    datasets (p19, p7); AF2.3 baseline run as 5×5 with **20** recycles (p7).
  - **Targets**: 308 (PoseBusters V2); LowH Recent PDB reported as **993 + 64 interface clusters**,
    underlying structure count never stated; 25 + 38 nucleic-acid structures; 8 CASP15 RNA.
  - **Totals**: PoseBusters V2 = 308 × 25 = **7,700 predicted structures**. CASP15 RNA = 8 × 5 =
    **40**. Protein and nucleic interface totals **cannot be computed** because the paper reports
    clusters, not structures — this is a real gap, not an omission by the extractor.
- **comparable_to_ours**: *(left empty by the extractor per v3 — populated by whoever holds
  `STATUS.md` and the manuscript.)*
- **si_in_scope**: **No external supplementary material exists or is referenced for this paper —
  Appendices A (Dataset), B (Evaluation Workflow) and C (Chain and Atom Permutation) are inside
  the 21-page PDF (pp 18–21) and the corpus holds them.** However the practical effect is close to
  `SI NOT HELD` and should be flagged as such for anyone quoting numbers: **the paper contains no
  results table at all.** Every accuracy number in Section 2 lives in a figure panel and almost
  none is printed in text, and there is no per-target table for any benchmark. The one thing that
  is genuinely elsewhere is the **AF3 supplementary material**, which the paper repeatedly leans
  on and does not reproduce — its algorithm numbering (Table 1, p12), its Table 14 of RecentPDB
  IDs (p19), and its Section 5.10 recycle configuration (p19). Reproducing Protenix's data or
  evaluation setup requires the AF3 SI in hand, and the corpus does not hold Protenix numbers in
  tabular form from any source.

## F. Figures

One row per panel group. Split on `mark` or `measure`; not on `facet` alone. 11 panel-group rows
across 9 figures.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| **1A-B** | 4 | Headline success rates: Protenix vs AF3 on PoseBusters V2, and Protenix vs AF2.3 on protein/antibody interfaces | bar | `PLOT \| facet: benchmark (3: PoseBusters V2, all protein-protein, protein-antibody) \| vary: metric or selection mode (2 in A: RMSD, PB-Valid; 3 in B: Oracle, Median, Selected) \| series: predictor (2 per panel: Protenix + AF3 in A, Protenix + AF2.3 in B) \| measure: success rate (RMSD ≤2 Å, PB-Valid, or DockQ >0.23) \| mark: bar \| n: A 308 structures per bar; B 993 clusters (all protein-protein) and 64 clusters (protein-antibody) per bar` | 3 sub-panels under labels A and B; panels vary by benchmark and by interface type | **Y-axes truncated in every panel** — A starts at 0.60, B-left at 0.55, B-right at 0.10, so bar-length ratios badly overstate differences that are 1–3 points. **No error bars anywhere in Figure 1**, although Figure 2A shows the same PoseBusters comparison *with* CIs that overlap heavily — so Fig 1A presents as a clean win what Fig 2A shows is within noise. **Oracle bars sit beside deployable bars in the same panel** with no visual distinction. | CC-BY 4.0 International, **no ND clause** — redrawing and modification permitted with attribution. License banner on every page including p4 (and p1) |
| **1C-D** | 4 | Nucleic-acid accuracy: protein–RNA and protein–dsDNA interface LDDT, and CASP15 RNA LDDT | bar | `PLOT \| facet: benchmark (2: LowH Recent PDB nucleic interfaces, CASP15 RNA) \| vary: interface or target type (2 in C: PDB Prot-RNA, PDB Prot-dsDNA; 1 in D: CASP15 RNA) \| series: predictor (4 in C: Protenix, RF2NA, "AF3 in AF3", "RF2NA in AF3"; 4 in D: RF2NA, Protenix, AF3, Alchemy_RNA2) \| measure: (interface) LDDT \| mark: bar \| n: C 25 structures (Prot-RNA) and 38 (Prot-dsDNA) per bar; D 8 structures per bar` | 2 sub-panels, C and D; vary by molecule type | **Y-axes truncated** — C starts at 0.10, D at 0.40. **No error bars, and n = 8 in D**, where a mean over eight targets is presented as a bar without a spread. **Two different RF2NA values are plotted side by side** ("RF2NA" rerun ≈0.235 vs "RF2NA in AF3" ≈0.29 on dsDNA) with the discrepancy acknowledged only in the p9 text, not the figure. **AF3's bars are transcribed, not rerun**, which the caption discloses but the visual encoding does not distinguish. | CC-BY 4.0, no ND (p4) |
| **2A** | 5 | PoseBusters V2 overall: Protenix vs AF3 on RMSD and PB-Valid, **with confidence intervals** | bar | `PLOT \| facet: none (1) \| vary: metric (2: RMSD, PB-Valid) \| series: predictor (2: Protenix, AF3) \| measure: success rate \| mark: bar + error bar \| n: 308 structures per bar` | 1 panel | **Y-axis truncated, starts at 0.65.** The error bars are the honest content here — they **overlap substantially** between Protenix and AF3 on both metrics, which is not reflected in the p4 text's "Protenix outperforms AF3-2019" or in Fig 1A. Error-bar definition (CI? bootstrap? level?) is **never stated** in caption or text. | CC-BY 4.0, no ND (p5) |
| **2B** | 5 | Cumulative RMSD success rate vs threshold, four selection arms | line | `PLOT \| facet: none (1) \| vary: RMSD threshold, 0–8 Å (continuous) \| series: arm (4: AF3 confidence-ranked, Protenix oracle, Protenix all-sample, Protenix confidence-ranked) \| measure: cumulative success rate \| mark: line \| n: 308 structures per curve; 25 samples per target behind the oracle and all-sample curves` | 1 panel | The most informative panel in the paper and it hides little. Note only that **the four curves are indistinguishable above ~5 Å** (see `metric_saturation`) so the right two-thirds of the x-range carries no signal, and that the **oracle curve is an upper bound plotted in the same style as deployable curves**. | CC-BY 4.0, no ND (p5) |
| **2C** | 5 | Success rate split by ligand commonality — the generalisation control | bar | `PLOT \| facet: none (1) \| vary: ligand category (3: not common, new common ligs, old common ligs) \| series: predictor (2: Protenix, AF3) \| measure: RMSD ≤2 Å success rate \| mark: bar + error bar \| n: NOT REPORTED per bar — the caption gives 50 old NCL and 75 new NCL as ligand-type counts, not as per-bar structure counts, and the "not common" bin has no n at all` | 1 panel | **Y-axis truncated, starts at 0.40. n is not shown for any bar** — the panel carrying the paper's generalisation conclusion ("our model generalizes as well as AF3-2019", p6) does not say how many structures that conclusion rests on. Error bars overlap in all three bins, so the conclusion of *equality* is safe but the two *differences* are not. | CC-BY 4.0, no ND (p5) |
| **2D** | 5 | Success rate by protein sequence homology to the training set, computed under both cutoffs — the anti-memorisation control | bar | `PLOT \| facet: training-set cutoff (2: 2019-09-30, 2021-09-30) \| vary: homology group (3: 0–30, 30~95, 95~100) \| series: predictor (2: Protenix, AF3) \| measure: RMSD ≤2 Å success rate \| mark: bar + error bar \| n: 2019 panel 30/90/188; 2021 panel 15/52/241 structures per group (printed under the axis)` | 2 sub-panels, both under label D, varying by which training set homology is computed against | **Y-axes truncated, start at 0.40.** **The 0–30 bin under the 2021 cutoff has n = 15** and its error bar spans roughly 0.67–0.99 — the single most important cell for the memorisation question is unpowered, and the AF3 bar in it reads ≈1.00 with a barely visible interval. n is printed, to the figure's credit. | CC-BY 4.0, no ND (p5) |
| **2E** | 5 | Per-criterion pass rate across all 18 PoseBusters validity checks | bar | `PLOT \| facet: none (1) \| vary: validity criterion (18: file loaded → volume overlap with inorganic cofs) \| series: predictor (2: Protenix, AF3) \| measure: pass rate \| mark: bar \| n: 308 structures per bar` | 1 wide panel, 36 bars | **Y-axis truncated to 0.80–1.00, and even so most bars are pinned at the 1.0 ceiling** — see `metric_saturation`. **No error bars.** Criterion labels are printed *inside* the bars vertically, so the panel is near-unreadable at print size. Only 3 of 18 criteria carry any signal. | CC-BY 4.0, no ND (p5) |
| **3, 4, 5, 7** | 6, 7, 8, 9 | Case-study overlays: two accurate novel protein–ligand predictions (3), two "sensible failures" (4), a novel protein–protein and protein–DNA prediction (5), a novel protein–dsDNA prediction (7) | structure render | `RENDER \| facet: case (7: 7WUX, 7URD, 7LOE, 5SAK/5SAN, 7XVA, 7XV8, 7R6R) \| views: 1 \| overlay: 1 prediction on 1 reference (2 references for the 5SAK/5SAN case) \| axis: none` | 7 renders across 4 figures; panels vary by system, one camera angle each | **Every case is selected post hoc with the reference in hand** (route 7, see `oracle_leakage`). **No quantitative panel accompanies any of them** — no RMSD, LDDT or DockQ value is given for a single case study, including the Fig 4 "failure" cases whose whole point is that the RMSD exceeds 2 Å but the pose is reasonable. Fig 4B compares against a *different* PDB entry (5SAN) than the target (5SAK) to argue the prediction is defensible, with no number attached. | CC-BY 4.0, no ND (pp 6–9) |
| **6A-B** | 9 | Per-target CASP15 RNA accuracy for four methods, LDDT and TM-score | bar | `PLOT \| facet: metric (2: LDDT, TM-score) \| vary: CASP15 target (8) \| series: method (4: RoseTTAFold2NA, AlphaFold3, Alchemy_RNA2, Protenix) \| measure: LDDT + TM-score \| mark: bar \| n: 1 structure per bar (single top-ranked sample, pLDDT-selected, from 5 single-seed samples)` | 2 sub-panels, A and B, differing only by metric — one row with a compound measure per the v3 splitting rule | **The x-axis has no target labels at all** — eight groups of four bars and the reader cannot tell which CASP15 target any group is. **Y-axes truncated** (A starts at 0.2, B at 0.2). **No mean, no error bars, no summary statistic** in the panel, although the text's claim ("the average LDDT and TM-score of Protenix are similar to those of AF3", p9) is about the mean. **Alchemy_RNA2 uses human input** and is plotted identically to the automated methods; the legend says so, the bars do not. | CC-BY 4.0, no ND (p9) |
| **8A-C** | 10 | Confidence calibration: DockQ distribution against binned chain-pair ipTM, split by interface type | box | `MATRIX-adjacent but genuinely a PLOT: PLOT \| facet: interface type (3: all, protein-protein, protein-nucleic acid) \| vary: chain pair ipTM bin (5: 0~0.4, 0.4~0.8, 0.8~0.9, 0.9~0.95, 0.95~1) \| series: none (1) \| measure: DockQ \| mark: box \| n: per box, A 3503/10969/4540/3419/2219, B 2580/6708/3640/2370/1297, C 923/4261/900/1049/922; per panel A 24,650, B 16,595, C 8,055 interfaces` | 3 panels, varying by interface type | Nothing serious. Minor: the Pearson ρ printed in each panel is computed on the **unbinned** data while the boxes are binned, so the reader cannot recover ρ from what is drawn; and the bins are unequal in width (0.4, 0.4, 0.1, 0.05, 0.05), which compresses the high-confidence region where selection actually happens. n is printed under every box, which is exemplary and rare in this paper. | CC-BY 4.0, no ND (p10) |
| **9A-B** | 10 | Memorisation demonstration: two good predictions shown beside their close training-set neighbours | structure render | `RENDER \| facet: case (2: 7PZB/3MZH protein–DNA, 7XFA/5OAX protein–ligand) \| views: 1 \| overlay: 1 prediction on 1 reference, shown next to 1 training-set structure \| axis: none` | 2 figure parts, each with a left (prediction vs crystal) and right (training-set neighbour) render | **The paper's most consequential claim — "the accuracy of both Protenix and AF3 may partially result from memorization" (p10) — is supported by exactly two hand-picked pairs and no quantitative panel.** No similarity score, no TM/RMSD between target and training neighbour, no distribution over the benchmark, no n. The claim is correct in direction and the corpus can cite the authors' own words, but the *evidence* in this figure is anecdotal and should be cited as an admission, not as a measurement. | CC-BY 4.0, no ND (p10) |

- **Figure 1 vs Figure 2A note for reuse**: the same PoseBusters comparison is drawn twice, once
  without error bars (Fig 1A) and once with them (Fig 2A). If a panel from this paper is reused,
  **use Fig 2A, not Fig 1A.**
- **Table inventory** (not figures, but the only tabular content in the paper): Table 1
  "Corrections" (p12, the 7 AF3 algorithm corrections — the most reusable content in the paper);
  Table 2 "Training Stages Configurations" (p14); Table 3 "Datasets used to train Protenix"
  (p18). All three are transcribed above.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), session of 2026-09-08
- **schema_version**: v3
- **confidence**: **high** on everything that is printed in text — the cutoff, the deviations from
  AF3, the training composition, the sampling defaults, the confidence-score definitions, the
  correlation coefficients, the release contents. All of these are stated plainly and I quote them
  directly. **Medium-low on the accuracy values in `metrics_reported` marked *(panel)***: this
  paper prints essentially no result numbers in running text, so almost every comparator had to be
  read off a rendered bar at 150 dpi against a truncated axis, and values should be treated as
  ±0.01–0.02 with the *ordering* reliable and the *magnitude of each gap* not. Three pages were
  rendered (4, 5, 9); Figure 8's values are printed in-panel and needed no render. **Low** on any
  interface *structure* count for the LowH Recent PDB set, which the paper reports only as cluster
  counts. What was hard to read: nothing in the OCR — the text layer is clean throughout; the
  difficulty is entirely that the paper's results are pictures.
- **unresolved**:
  1. **A Protenix-v2 preprint exists and is a separate corpus entry.** `MANIFEST.csv` and
     `refs.bib` hold `protenix2026v2` — "Protenix-v2: Broadening the Reach of Structure Prediction
     and Biomolecular Design", 2026, DOI `10.64898/2026.04.10.717613`, 17 pages, overlapping
     author list (Yuxuan Zhang, Chengyue Gong, Jiaqi Guan, Hanyu Zhang, Wenzhi Ma, Zhenyu Liu,
     Xinshi Chen, Wenzhi Xiao). **Everything in this note — the 2021-09-30 cutoff, the "no
     templates" statement, the 25-sample default, the confidence-head modification, the 75K/15K/4K
     step budget, the single-distillation-set training, and every accuracy value — is a property
     of Protenix v1 only, and must not be attributed to Protenix-v2 or to "Protenix" unqualified.**
     Citations must not be conflated: cite `protenix2025` for v1 and `protenix2026v2` for v2, and
     any manuscript sentence saying "Protenix was trained to 2021-09-30" needs the v1
     qualification. I have not read the v2 preprint and cannot say whether its cutoff, template
     policy or architecture differ; a corpus consumer must check `notes/protenix2026v2.md`.
  2. **Two tags were needed and do not exist in the v3 vocabulary; neither was invented.**
     (a) **`templates-off`** — the Protocol group has `no-template-no-msa` (no templates *and* no
     MSA) and `templates-on`, but no tag for the very common regime this paper occupies: **MSA on,
     templates off**. `no-template-no-msa` would be false (MSAs are used for protein chains);
     `templates-on` would be false. So Protenix carries **no Protocol tag at all**, and a reverse
     lookup for "which papers ran without templates" will miss it. This is a real hole, not a
     taste objection: templates-off-with-MSA is the default regime for most cofolding work.
     Ironically Protenix *is* `no-template-no-msa` for **nucleic acid chains** specifically (p8,
     p11), so the paper straddles two Protocol tags depending on chain type — which is itself
     something the fixed vocabulary cannot express.
     (b) **`reported-oracle-arm`** — the Rigour group has `oracle-leak` and `design-level-oracle`,
     but nothing for a **disclosed, symmetric oracle upper-bound arm reported alongside the
     deployable number**, which is what Fig 1B and Fig 2B contain (`oracle_leakage` route 6). I
     did **not** tag `oracle-leak`, because tagging it would put this paper in the same bucket as
     papers that select best-of-N against a reference and report it as the result — a materially
     different and much worse practice. But the consequence is that a reverse lookup for oracle
     selection will not return Protenix, and Protenix does contain a prominent oracle arm. Someone
     re-reading Fig 1B carelessly *could* lift an oracle bar as a headline number.
  3. **Where `states_generated` should sit for a single-structure predictor that samples 25 times
     is genuinely underdetermined by v3.** I wrote `one`. But the field's own guidance —
     "'ensemble + single-state' is the correct answer for a method that samples broadly and
     collapses onto one basin" — could be read as applying, since Protenix does generate 25
     samples and collapse them by confidence. I judged `ensemble` inappropriate because the paper
     never treats the pool as conformationally meaningful; it is a candidate list for a ranker. A
     future extractor reading the same field could reasonably write `ensemble + single-state`, and
     the index would then disagree with itself across two model papers that behave identically.
     **The schema should say explicitly whether a diffusion sampler's N-sample pool counts as an
     ensemble when the paper never analyses it as one.**
  4. **The number of *structures* behind the 993 and 64 protein-interface cluster counts is never
     stated**, so `n_predictions` cannot be totalled for the largest benchmark in the paper, and
     no power comparison against a per-structure benchmark is possible without recuration.
  5. **Protenix's own parameter count is never given.** 386M is stated of AF3 (p13). Whether
     Protenix has the same count is not confirmed, though the reproduction framing implies it.
     Do not quote 386M as Protenix's size on the strength of this paper.
  6. **The error bars in Figures 2A, 2C and 2D are never defined** — no caption or text says
     whether they are 95% CIs, bootstrap intervals, or standard errors, and no bootstrap procedure
     is described. Any statement about statistical significance drawn from those panels is
     unsupported by the paper.
  7. **AF3 is never rerun by the authors.** PoseBusters AF3 metrics are recomputed *from AF3's
     released prediction files*; interface AF3 metrics are transcribed from the AF3 paper
     ("AF3 in AF3"); CASP15 RNA AF3 metrics are taken from Bernard et al. (p8). So every
     "Protenix vs AF3" comparison in this paper is against a number produced by someone else's
     run, and the authors flag two places where that produced a discrepancy they cannot explain
     (RF2NA differing from RF2NA-in-AF3, p9; cluster counts differing from AF3's, p18).
  8. **The v3 panel-splitting rule remains ambiguous, and I hit the ambiguity three times.** The
     bolded rule is "Split when `mark` or `measure` differs", but the sentence immediately
     following says "four box panels showing four metrics under the same faceting are **one row**
     with a compound measure" — which is a case where `measure` differs and the schema says *do
     not* split. I resolved it as: **split on differing `measure` when the panels also differ in
     `vary` or benchmark; merge into a compound measure when the panels differ only by which
     metric is plotted over identical data.** That is why Fig 6A-B is one row (same 8 targets,
     same 4 methods, LDDT vs TM-score → compound measure) but Fig 1A-B is separate from Fig 1C-D
     (different benchmarks, different `vary`, different n). It is also why 2A / 2C / 2D / 2E are
     four rows despite sharing `mark: bar` and `measure: success rate` — they differ in `vary`,
     and the rule says nothing about `vary`. **The rule should be restated as a precedence order
     over `measure`, `mark` and `vary`, with the compound-measure exception stated as an exception
     rather than as an example.** As written, two extractors will split Figure 2 differently.
  9. **Figure 8 sits between PLOT and MATRIX.** It is a binned box plot: `vary` is a binned
     continuous variable, and the boxes carry a distribution rather than a single value. PLOT with
     `mark: box` is the right form, but the v3 PLOT `n:` slot ("per mark, and per panel") is what
     makes it work, and the MATRIX form's existence made me check twice. No change needed; noting
     it because the next extractor will pause in the same place.
 10. **The `hides` field has no way to record "the axis is truncated in five separate figures".**
     I repeated the observation on each row as v3 requires (`metric_saturation` is numeric only),
     which is correct but means the note carries the same defect five times. A figure-level
     `hides` summary line, or a convention for cross-referencing, would compress this.
- **why_it_matters**: *(left empty by the extractor — the user's call.)*

## Tags

`general-protein` `cofolding` `single-state` `continuous-metric` `saturating-metric`
`anti-memorization` `confidence-as-discriminator` `multi-backbone` `seed-only` `preprint`
`background` `precedent` `comparator-numbers`

**Tag notes (why some obvious tags are absent):**
- **No Protocol tag.** Templates are off but MSAs are on; `no-template-no-msa` would be false and
  `templates-on` would be false. See `unresolved` item 2(a). This is a vocabulary gap, not an
  oversight.
- **No `oracle-leak`, no `design-level-oracle`.** Route 6 is present but confined to explicitly
  labelled oracle arms reported beside the deployable number; route 7 is present but confined to
  post-hoc case-study selection with no quantitative claim attached. Tagging either would put
  Protenix in a bucket with papers whose *headline result* depends on the oracle, which would
  misrepresent it. See `unresolved` item 2(b).
- **No `prospective`** — every benchmark is retrospective (see `prospective`). `anti-memorization`
  is tagged instead, which is the accurate claim: post-cutoff held-out sets and a homology-
  stratified control arm actually run.
- **No `rmsd-only`** — RMSD is one of four accuracy metrics (RMSD, DockQ, LDDT, TM-score), so
  `continuous-metric` is the correct tag and `rmsd-only` would be false.
- **No state, site, or directional-control tags** beyond `seed-only` — there is no conformational
  state axis, no site analysis, and no state handle anywhere in the paper.
- **No `negative-result`** — the memorisation finding on p10 is a self-reported caveat inside an
  otherwise positive paper, not a negative-result paper.
