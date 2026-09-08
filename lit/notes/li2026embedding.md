# li2026embedding

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NONE` / `NONE RUN` / `NONE FOUND` where the thing is genuinely absent.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–29), which for this preprint
coincide with the printed page numbers.** Layout: p1 title + abstract + §1 Introduction, p2 Fig 1
+ rest of §1, p3 contributions + §2 Background, p3–5 §3 Method (Algorithm 1 p4, Proposition 1 p4,
DPS comparison p5), p5 §4 Related Works, p5–9 §5 Experiments (§5.1 distance constraints p6–7,
§5.2 synthetic cryo-EM p7–8, §5.3 real cryo-EM p8–9), p9–10 §6 Discussion + Limitations,
p10–12 references, p13–29 appendices A–E. Figures: Fig 1 p2, Fig 2 p6, Fig 3 p7, Fig 4 p8,
Fig 5 p21, Fig 6 p22, Fig 7 p23, Fig 8 p23, Fig 9 p24, Fig 10 p24, Fig 11 p27, Fig 12 p28,
Fig 13 p29. Tables: Table 1 and Table 2 p19, Table 3 p25, Table 4 p26. **All appendices are inside
this 29-page PDF; there is no external supplementary file.**

**DOCUMENT TYPE.** Machine-learning methods paper with a formal proposition and proof
(Appendix A.2, p13–15) plus three empirical benchmarks. Per instruction, the theoretical claim is
recorded separately from the empirical ones — see `necessity_claims`, the `theoretical_claim`
sub-entry in section D, and `unresolved` item 6. The proposition is about a **surrogate** reward
and is **local**; it is not a claim that EmbedOpt finds better structures.

**MECHANISM IN ONE LINE (established from the method section, not the abstract).** EmbedOpt takes
the *conditioning embedding* `c = {s, z}` — the single embedding `s ∈ R^(Nres × Cs)` and the pair
embedding `z ∈ R^(Nres × Nres × Cz)` emitted by the PairFormer trunk of an AlphaFold-3-style model
(here Protenix) — and performs **one RMS-normalised gradient-ascent step on it at every diffusion
step**, ascending a differentiable experimental reward `R(x̂₀)` evaluated at the current denoised
prediction. **Network weights, MSA, sequence and the diffusion sampler are all unchanged**; only
the conditioning tensor moves. This is the corpus's `latent-steering` definition exactly
("conditioning embedding").

---

## A. Identity

- **citekey**: `li2026embedding`
- **doi**: **arXiv:2602.05285v2** — stamped in the left margin of p1: "arXiv:2602.05285v2 [cs.LG]
  14 May 2026". `refs.bib` records `doi = {10.48550/arXiv.2602.05285}`, the arXiv-minted DOI. **No
  journal or conference DOI appears anywhere in the PDF.**
- **year**: **2026** (v2 posted 14 May 2026, p1 margin).
- **venue**: **arXiv preprint, cs.LG. The only venue statement in the document is the single word
  "Preprint." at the foot of p1.** No journal, no conference, no "under review" line, no
  camera-ready notice. The manuscript is typeset in NeurIPS style (numbered contributions,
  "Acknowledgments and Disclosure of Funding" section p10) and the task brief calls it a
  machine-learning venue paper, which is consistent with the typesetting, but **the PDF never
  names a venue — do not infer one.** Tagged `preprint`.
- **title**: Robust Inference-Time Steering of Protein Diffusion Models via Embedding
  Optimization — p1
- **authors**: Minhuan Li, Jiequn Han, Pilar Cossio, Luhuan Wu — all Flatiron Institute (p1).
  Correspondence: Minhuan Li and Luhuan Wu (p1 footnote). Code:
  `https://github.com/rs-station/embedopt` (p1 abstract).

## B. Scope

- **system**: **General protein.** No protein family is the subject; the benchmarks are
  family-agnostic collections chosen for inter-domain flexibility and for map-fitting difficulty.
  The only named biological system in the paper is **8GMG_A, "P-glycoprotein / ABCB1"** (p24),
  used as the largest system in the compute profiling — a transporter, but studied as a size
  stress-test, not as a transporter. `transporter` is **not** tagged.
- **n_targets**: **Three disjoint benchmarks, 107 systems in total, plus reused subsets.**
  - 24 multi-domain protein systems, distance-constraint benchmark, taken from Zhang et al. 2025
    (p6). One is named: 6V7W chain B (Fig 2a, p6).
  - 77 protein systems, synthetic cryo-EM benchmark, assembled from the PDB (p7). Named in
    figures: 8H1I (p7–8), 8CAW_A, 8W2Q_A, 8F2R_E, 8K23_B (p21), 8ANE_A, 8AU1_A, 8B3Y_A, 8BBQ_A
    (p22), 8AHU_A, 8GXU_A, 8K9Z_A (p25–27), 8P4K_A (p24).
  - 6 real experimental cryo-EM targets from the CryoBoltz benchmark: 9UGC, 9UGB, 8GMG, 8SA1,
    8SA0, 8GMJ (p9), with maps EMD-64136, EMD-64135, EMD-40026, EMD-40027, EMD-40258, EMD-40259
    (p28–29) at resolutions 3.52, 3.25, 4.3, 4.4, 4.1, 4.4 Å (Fig 9 panel headers, p24).
  - Sub-studies reuse members of the 77: MSA-depth ablation on 3 (8AHU_A, 8GXU_A, 8K9Z_A, p25);
    runtime profiling on 3 (8K23_B, 8P4K_A, 8GMG_A, p24).
  **Generality claim vs. scope:** the paper claims a general inference-time framework and does test
  three modalities, but every biological conclusion rests on map-fitting and synthetic distance
  restraints; no protein family, no functional state, and no conformational-equilibrium question is
  studied.
- **method_class**: **other — inference-time optimisation of the conditioning embedding of a
  pretrained sequence-to-structure diffusion model (latent steering).** Explicitly *not*
  fine-tuning and *not* coordinate guidance: "EmbedOpt is a flexible, inference-time method that
  exploits the rich generative capacity of state-of-the-art AlphaFold 3-style diffusion models
  without the computational cost of model fine-tuning" (p18). Secondary class: benchmark of
  DPS-style coordinate guidance, which is run as the matched baseline.
- **backbones**: **Protenix** (open-source AF3 reproduction, Chen et al. 2025) is the diffusion
  prior for the prior arm, DPS arm and EmbedOpt arm — "Our experiments use the Protenix model Chen
  et al. [2025] as the diffusion prior" (p6). **Boltz-1** enters only underneath the published
  CryoBoltz baseline (p6, p9). **AlphaFold 3 is discussed as the architecture family but is never
  run.** Two backbones appear, they are not compared head to head as backbones, and the paper says
  so itself: "We note that this comparison conflates the base model choice (Protenix vs. Boltz-1)
  with inference-time schemes, while the previous experiment disentangles these factors" (p9).
  `multi-backbone` is therefore **not** tagged (see `unresolved` item 4).
- **templates**: **NOT REPORTED.** The word "template" does not occur anywhere in the 29 pages.
  Protenix's default template behaviour is never stated.
- **msa_handling**: **full (default), with a random-subsampling ablation on 3 systems.** MSAs are
  the source of the signal the method steers: "conditional embeddings are computed from the
  sequence and MSA information, which encodes coevolutionary signals" (p3). Ablation: "we sweep MSA
  depth ∈ {0%, 25%, 50%, 75%, 100%} (random MSA subsampling with 3 subsampling seeds × 3 diffusion
  seeds; at 0% and 100% MSA only 3 diffusion seeds since no subsampling is required)" (p25). This is
  depth reduction, **not** state filtering. For the CryoBoltz comparison, both methods get "the
  identical cleaned density maps ..., protein sequences, and multiple sequence alignments" (p20).

## C. Conformational core

- **states_generated**: **one.** Single-structure determination, stated as the scope boundary
  against the concurrent embedding-optimisation paper: "we develop embedding-space steering as a
  general inference-time framework that updates the embedding within a single diffusion trajectory,
  with a trust-region analysis and empirical comparison against coordinate-space methods on
  **single-structure determination** ...; Maddipatla et al. [2026] focus on empirical application to
  ensemble generation" (p5). Multiple seeds are run (3 by default, 5 on the real targets) but they
  are scored individually against one reference and summarised by median or by best; they are never
  treated as an ensemble, and no population, weight or free-energy quantity is ever reported. Not
  dual: there is no arm in which an ensemble is the product.
- **structural_priors_used**: **Substantial, and largely legitimate as benchmark construction —
  recorded here rather than in `oracle_leakage` where it would read as a defect.**
  1. **Deposited PDB structures define every synthetic measurement.** Synthetic cryo-EM: "We
     generate synthetic target cryo-EM maps V_obs at 5.0 Å resolution using SFC_Torch" (p7–8) from
     the deposited structures of 77 PDB entries selected as "high-resolution structures (<4.5 Å) and
     low sequence similarity (<25%)" (p7). Distance restraints: target distances `d_target_i` are
     read off "the ground truth PDB structure" (p20).
  2. **Benchmark systems chosen for a known structural property**: the 24 multi-domain proteins
     were taken "from Zhang et al. [2025], as they exhibit flexible inter-domain orientations that
     challenge existing generative models" (p6).
  3. **Deposited references define the agreement metrics**: RMSD Cα, RMSD all-atom and TM-score are
     computed "relative to the deposited structure" / "to the deposited reference ... using Biotite
     after Kabsch superposition" (p9, p20).
  4. **The pretrained priors themselves (Protenix, Boltz-1) are PDB-trained**, acknowledged only
     implicitly through the manifold-coverage discussion (p9, p20).
  5. Real cryo-EM maps (EMD-64135/64136/40026/40027/40258/40259) are genuine experimental
     measurements, not derived from a model — this is the one input channel that is not a
     structural prior.
- **oracle_leakage**: **PRESENT AND STRUCTURAL in the two synthetic arms, disclosed by the authors
  in one of the two cases; substantially reduced but not eliminated in the real-map arm.** Routes
  enumerated separately.

  **Route 1 — deposited structure of the target state used as input.** **PRESENT (synthetic arms).**
  The measurement `y` that the method is steered toward *is computed from the answer*.
  - Distance constraints, and the authors flag it themselves: "we derive constraints by selecting
    the top K = 20 residue pairs (a sparsity level typical of cross-linking experiments) with the
    largest structural discrepancies between the ground truth and the prior model's predictions,
    with a δ = 2.0 Å tolerance. **We note that this constraint-selection procedure uses oracle access
    to the target and is therefore an idealized stress-test rather than a model of a specific
    experimental protocol**; in practice, constraint pairs would be specified by the experimental
    modality (e.g., cross-linker reactivity profiles)." (p6) Repeated in the appendix: "We define
    the constraint set by identifying the atomic indices of the top K = 20 residue pairs that
    exhibit the largest distance deviation between the unguided prior predictions and the ground
    truth PDB structure." (p20)
  - Synthetic cryo-EM, **not** flagged as oracle use, though structurally identical: "We generate
    synthetic target cryo-EM maps V_obs at 5.0 Å resolution using SFC_Torch Li et al. [2025]." (p7–8)
    The rendered map is a function of the deposited coordinates, and the same differentiable
    forward model is then used to render the prediction: "We use the same differentiable forward
    model to render a map V(x0) from a generated structure x0" (p8) — i.e. the forward operator is
    exactly invertible in principle and carries no experimental noise, resolution anisotropy or
    missing density.
  - **Real cryo-EM arm (§5.3): NONE FOUND on this route.** The measurement is an experimental map:
    "we benchmark EmbedOpt on 6 real cryo-EM targets of varying resolutions used to evaluate
    CryoBoltz" (p8–9), with "the identical cleaned density maps (cropping out background regions of
    the map under a threshold), protein sequences, and multiple sequence alignments" given to both
    methods (p20). The deposited structure enters this arm only at evaluation (route 5).

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates
  or alignments.** **NONE FOUND.** No state-annotated database is used anywhere; no conformational
  state label of any kind is assigned to any structure in the paper. Protocols where such a thing
  would have to appear: p6 (distance benchmark construction), p7–8 (synthetic map benchmark
  construction and forward model), p20 (Appendix E.2/E.3 forward models), p20 (Appendix E.4 real-map
  protocol). None mentions a database beyond the PDB and EMDB.

  **Route 3 — cluster labels derived from known states.** **NONE FOUND.** No clustering step exists
  in the pipeline (Algorithms 1–4, p4, p13, p17; protocols p6–9, p20).

  **Route 4 — hyperparameters, sweeps, seeds or stopping criteria tuned against known states.**
  **PRESENT in both synthetic arms, and the sweep range itself is set on the evaluation set.**
  - "we compare best-achieved performance (**after sweeping learning rates**) across the full
    dataset (Figure 3b)" (p8) — the headline synthetic-cryo-EM comparison is a
    best-over-sweep number, and the sweep is scored by map correlation to the map that was rendered
    from the answer.
  - "Structures display the best samples from each method **following hyperparameter sweeping**"
    (Fig 5 caption, p21).
  - "Starting from a 200-step baseline (with α = 0.1, **optimal for both methods per Figure 8b**)"
    (p7) — the step-efficiency experiment inherits a learning rate chosen on the same benchmark.
  - Learning-rate ranges are themselves reported as evaluation-set findings: "In practice we found
    a range of α from 0.05 to 5 to work well" (p18, for the synthetic 1-D illustration); sweeps span
    0.0025–1.00 on the synthetic maps (Fig 3c, Fig 7, p7, p23) and 0.0025–0.5 on the real targets
    (p9). Under the v3 clarification, tuning a *range* on the evaluation set is leakage even where
    no per-target value is picked.
  - **Per-target hyperparameter selection is applied to the DPS baseline in the visual galleries**:
    "DPS uses the **best learning rate per system** from Figure 9; CryoBoltz uses default published
    settings" (Fig 12 caption, p28; same protocol for Fig 13, p29). This particular selection
    favours the baseline, not EmbedOpt, but it is still per-system tuning against the reference.
  - **Partially mitigated in the headline real-map comparison**: "For EmbedOpt, we use 100 diffusion
    steps and the **same learning rate α = 0.1 across all six systems**" (p9), and the same fixed
    α = 0.1 for DPS in Fig 10. A single global constant, not per-target tuning — but the constant
    was picked from sweeps on the same evaluation data.

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.** **PRESENT
  throughout, including in the real-map arm.** "We evaluate three metrics (Figure 4): data fitting
  (CC mask), physical plausibility (MolProbity score) and **reference agreement (RMSD Cα relative to
  the deposited structure)**" (p9); "Structural similarity to the deposited reference (TM-score,
  RMSD Cα, RMSD all-atom) was computed using Biotite after Kabsch superposition" (p20); on the
  synthetic side the reward-defining map and the scoring map are the same object rendered from the
  deposited coordinates (p7–8). Note this is unavoidable for a structure-determination benchmark
  and is not, on its own, the damaging form of leakage — but it does mean no arm of this paper
  reports a success criterion that could be evaluated without the answer.

  **Route 6 — best/worst model labels assigned against a held reference.** **PRESENT.**
  "**Best-sampled structures** across 77 systems (dots), binned by task difficulty" (Fig 3b caption,
  p7); "Structures display the **best samples** from each method following hyperparameter sweeping"
  (p21); "we display the experimental cryo-EM density together with the predicted model from the
  **median-CC seed** of four methods" (p28). Best-of-seeds and best-of-sweep are both assigned by a
  score computed against the reference. **Mitigation**: Fig 4 (p8), Fig 9 (p24) and Fig 10 (p24)
  show every seed as a dot with medians marked, so the median statistic is also available and the
  selection is visible rather than hidden.

  **Route 7 — design-level oracle use (weaker than pipeline leakage; label kept distinct).**
  **PRESENT.** The task difficulty axis is itself computed from the answer: "We define task
  'difficulty' as 1− prior map correlation, a proxy for the misalignment between the prior's
  dominant mode and the experimental target" (p8), and the headline claim is conditioned on it
  ("Both methods perform comparably on 'easy' targets (difficulty < 0.4), but EmbedOpt consistently
  outperforms DPS on 'hard' targets", p8) with the 0.4 split never justified. Systems were also
  selected because the expected difficulty was known in advance — the 24 multi-domain proteins
  "exhibit flexible inter-domain orientations that challenge existing generative models" (p6).

  **VERDICT.** Routes 1, 4, 5, 6 and 7 all fire on the two synthetic benchmarks; the paper
  self-declares route 1 for the distance task (p6) and not for the synthetic maps. The **real
  experimental cryo-EM arm (§5.3, 6 targets) is clean on routes 1, 2 and 3, uses one global
  hyperparameter rather than per-target tuning for EmbedOpt, and leaks only through evaluation
  (route 5) and best-seed labelling (route 6)** — that arm is the honest one, and it is also the
  smallest (n = 6).

- **prospective**: **partial.** Prospective in the real-map arm: genuine experimental maps
  (EMD-64135/64136/40026/40027/40258/40259), inputs matched to the baseline, one fixed learning rate
  α = 0.1 across all six systems, deposited structure used only to score (p9, p20). Retrospective in
  both synthetic arms, where the measurement steering the model is manufactured from the deposited
  answer (p6, p7–8, p20) and headline numbers are best-over-sweep (p8). The paper is therefore
  prospective in one arm of six targets and retrospective in the two arms of 101 targets that carry
  its scaling claims. `prospective` is **not** tagged; see `unresolved` item 3.
- **state_metric**: **binary predicate + continuous coordinate + RMSD-to-reference — three
  co-existing metrics, recorded together because no one of them carries the paper.**
  - *Binary predicate, with an explicit threshold:* a restraint counts as satisfied within a
    tolerance, "with a δ = 2.0 Å tolerance" (p6), and the reported metric is the count:
    "Performance is measured by the number of satisfied constraints" (p6). The δ = 2.0 Å tolerance
    is asserted, never justified against any cross-linker or FRET error model. A second binary
    predicate is drawn on the geometry axis: "Good geometry (MolProbity ≤ 2.0)" (Fig 4 legend p8,
    Fig 10 legend p24), also unjustified in the text.
  - *Continuous coordinate:* map correlation `cc` / `CC mask` from
    `phenix.validation_cryoem` (p8, p20), total distance violation in Å (Fig 8b, p23), MolProbity
    score (p8), surrogate reward value (Fig 2a, p6).
  - *RMSD-to-reference:* RMSD Cα, RMSD all-atom and TM-score against the deposited structure (p9,
    p20, Fig 4 p8, Fig 10 p24).
  - **Conformational state is never operationalised as a predicate at all.** No paper-defined
    state, no state-assignment rule, no two-state comparison. What is judged is agreement with a
    measurement and stereochemical validity. The one qualitative structural call — "DPS remains
    trapped in a local optimum (cc = 0.58), while EmbedOpt successfully reorients the domains
    (cc = 0.93)" (Fig 3 caption p7) — is backed by cc, not by eye, so `visual-metric` is **not**
    tagged.
  - Difficulty threshold used to partition results: "easy" vs "hard" at 0.4 on the 1−prior-cc axis
    (p8), stated without justification.
- **metric_saturation**: **YES, numerically, on the distance-constraint benchmark — and the paper
  says so.** The metric ceilings at K = 20 of 20 restraints: "it maintains near-optimal constraint
  satisfaction (**median constraints passed ≈ 20**) down to 50 diffusion steps" (p7) and "With
  sufficient steps and tuned hyperparameters, **both methods achieve comparable peak performance**
  (Figure 8a), as the flexibility of sparse distance targets **allows both to saturate the reward**"
  (p7); Fig 8a caption: "sparse constraints allow both methods to achieve comparable peak
  performance, with **both satisfying all constraints for the majority of targets**" (p23). The
  ceiling is why the distance benchmark can only support the *efficiency* and *robustness* claims,
  not a performance claim.
  Secondary saturation: map correlation approaches its ceiling for EmbedOpt at high learning rate
  before relaxation, 0.98 [0.93, 0.99] (Table 1, p19). **Floor**: DPS at LR ≥ 0.5 collapses to
  0.01 [−0.01, 0.05] after relaxation (Table 1, p19), i.e. the metric bottoms out — and 61.3% of
  those DPS structures "cannot be validated by Phenix" at all before relaxation (p19), so the
  MolProbity axis is undefined rather than merely bad for a majority of that arm.
  Axis defects (Fig 2a has no numeric reward scale; Fig 4 uses a different y-range per panel) are
  recorded in `hides` on the figure rows, per v3 rule 9, not here.
- **directional_control**: **YES — genuine, and this is the paper's core capability. The target is
  specified as an EXPERIMENTAL MEASUREMENT plus a differentiable forward model, not as a state
  label, not as a scalar property, and not as a classifier score.**
  - The handle is the reward: "we can prescribe an experimental likelihood p(y | x0) given some
    measurement y of the underlying structure x0. We define a reward function R(x0) ∝ log p(y | x0)
    ... We assume R is differentiable, as is the case in many applications." (p3)
  - What a user must supply is therefore (i) a measurement `y` and (ii) a differentiable operator
    mapping coordinates to that measurement. Two instantiations are demonstrated: a set of target
    residue-pair distances with a flat-bottom loss,
    `R(x0) = −Σ min(|d_i(x0) − d_target_i|, δ)²` (p6), and a rendered density map with an MSE loss,
    `R(x0) = −(1/NxNyNz) Σ (V(x0) − V_obs)²` (p8).
  - **The instruction is executed on the conditioning embedding, not on the coordinates**: "Update
    embedding c_{t−1} ← c_t + α_t ∇_{c_t} R(x̂0)" (Algorithm 1 line 6, p4), with the normalised form
    `s_{t−1} = s_t + α ḡ_{s_t}, z_{t−1} = z_t + α ḡ_{z_t}` (Eq. 3, p4). The claim about *why* this
    works: "In AlphaFold 3-style architectures, conditional embedding encodes rich coevolutionary
    signal derived from multiple sequence alignments (MSAs), so modifying it reshapes the model's
    structural preferences **without altering its parameters**" (p2).
  - **What is held fixed**: model weights, sequence, MSA, the trunk/PairFormer forward pass (run
    once, `N_cycle = 10`, p26), and the AF3-style stochastic sampler with its published constants
    (γ = 0.8, ρ = 1.003, step scale η = 1.5, Algorithm 2 p13). Only `c = {s, z}` is updated, once
    per diffusion step, initialised at the pretrained value `c_T ← c` (Algorithm 1 line 3, p4).
  - **Direction is toward a measurement, not toward a named conformational state.** There is **no**
    mechanism to request "the active state" or "the inward-facing state" without already holding
    data that distinguishes it. In the synthetic arms that data is manufactured from the deposited
    target, which is `oracle_leakage` route 1; in the real arm it is an experimental map, which is
    not. So directional control is real and demonstrated, but its currency is experimental data,
    which is a different (and stronger, but more demanding) handle than a state label, a partner, a
    ligand or an MSA manipulation.
  - Control is also shown to be *bounded* by the prior, which limits how far the instruction can be
    followed: "EmbedOpt only navigates the structural manifold induced by the pretrained model: when
    the target conformation is poorly represented, neither EmbedOpt nor DPS recovers it" (p9).
  - Tagged `directed-state`. Not `partner-driven` / `ligand-driven` / `peptide-driven` /
    `g-protein-mimetic` / `nanobody` / `apo-sampling` / `seed-only` — none of those handles is used.
- **anti_memorization_design**: **NONE.** There is **no held-out set, no post-cutoff set, and no
  training-cutoff date anywhere in the 29 pages** — the words "training set", "held-out", "cutoff"
  (in the temporal sense) and "memorisation" do not occur. The only selection filter is a
  *within-benchmark* redundancy filter with no reference to model training data: "we assemble a
  diverse benchmark of 77 protein systems from the PDB with high-resolution structures (<4.5 Å) and
  low sequence similarity (<25%)" (p7). Whether any benchmark entry — including 9UGB/9UGC, whose
  accession codes are conspicuously recent — postdates the Protenix or Boltz-1 training cutoff is
  never asked. The relation of the 24 distance systems and 6 CryoBoltz targets to training data is
  likewise never mentioned (p6, p8–9).
- **anti_memorization_control**: **NONE RUN.** No arm addresses memorisation. Two arms are
  adjacent but answer different questions and must not be mistaken for it: (i) the **unguided prior
  arm**, present throughout, which shows what the model produces without steering but says nothing
  about whether it has seen the target; (ii) the **MSA-depth ablation** (p25–27), which removes
  evolutionary signal rather than structural memory, and whose result — "all methods collapse at 0%
  MSA" (Fig 11 caption p27) — shows dependence on MSA, not independence from memorised structures.
  Not marked `UNPOWERED` because there is no control set to be underpowered; it simply does not
  exist. Tagged `no-anti-memorization`.
- **controls_run**: **A genuinely thorough control set — the strongest rigour feature of the paper.**

  | control | what it rules out | page |
  |---|---|---|
  | Unguided Protenix prior arm, run on every benchmark and shown in every results figure | That the improvement is the base model rather than the steering; supplies the "difficulty" baseline | p6, p7, p8, p19, p24, p27 |
  | DPS baseline **inside the same model** (Protenix), with the gradient-normalisation schedule adopted verbatim from Maddipatla et al. 2025 and a single shared base learning rate | That the EmbedOpt-vs-DPS gap is a base-model or implementation-tuning artefact; "This places the two methods in a relatively comparable optimization regime parameterized by a single base learning rate α" | p6, p9, p17 (Algorithm 4), p24 |
  | Matched learning rate α = 0.1 and matched 100 diffusion steps for EmbedOpt and DPS on real maps | That the real-map advantage comes from a more favourable hyperparameter for one method | p9, p24 |
  | Full learning-rate sweep for **both** methods (0.0025–1.00 synthetic, 0.0025–0.5 real) rather than one operating point | That either method was shown at a cherry-picked setting; this is what converts "better" into "robust" | p7 (Fig 8b), p8 (Fig 3c), p9 (Fig 9), p23 (Fig 7) |
  | CryoBoltz baseline run by the authors from "their official codebase under default settings", with identical maps, sequences and MSAs, identical energy relaxation, and the identical Phenix metric pipeline applied to both | That the cross-model comparison reflects input preparation, post-processing or metric differences rather than the methods | p20 |
  | CryoBoltz evaluated **both unrelaxed and relaxed** | That CryoBoltz was disadvantaged by omitting the post-processing step; "ensure the comparison reflects CryoBoltz at its best" | p20, p24 |
  | Energy-relaxation ablation over all methods × 3 learning-rate regimes, with paired per-sample differences (Tables 1–2) | That EmbedOpt's geometry advantage is created by the relaxation step rather than by the sampler | p18–19 |
  | MSA-depth ablation, 0/25/50/75/100%, 3 systems × 3 MSA seeds × 3 diffusion seeds | That the steering works independently of evolutionary signal — it does not | p25–27 |
  | Diffusion-step scaling with total guidance magnitude held constant (α × #steps = const) | That the step-count advantage is really a total-guidance-budget difference | p7, p6 (Fig 2b) |
  | Runtime and peak-GPU-memory profiling across three system sizes plus an analytic FLOP prediction, 3 seeds | That the robustness is bought with undisclosed compute; quantifies the 1.4–1.8× cost honestly | p23–26 (Tables 3–4) |
  | 3 random seeds by default, 5 seeds on the real cryo-EM targets, all shown as individual dots | Single-run luck | p6, p8, p24 |
  | 1-D Gaussian synthetic illustration with an analytically known posterior (prior N(5, 0.5²), likelihood N(y=20, 1)) | That the prior–likelihood-mismatch failure picture is an artefact of the protein setting | p2 (Fig 1a), p17–18 (Appendix C) |
  | Fixed occupancy 1.0 and uniform B-factor 50 Å² in the synthetic forward model | That map differences reflect B-factor or occupancy modelling rather than coordinates | p8, p20 |

- **confidence_as_discriminator**: **NOT REPORTED — and, unusually, not used at all.** pLDDT, pTM
  and ipTM do not appear anywhere in the 29 pages. Model selection within a method is done by
  reward/map correlation against the target (routes 5–6 above), and geometry is judged by
  MolProbity. `confidence-as-discriminator` is **not** tagged.

## D. Claims

- **central_conclusion**: Steering a pretrained AF3-style protein diffusion model by
  gradient-ascending its *conditioning embedding* (single + pair representations), one step per
  diffusion step, is an axis orthogonal to DPS-style guidance on the noisy coordinates: it matches
  DPS where the task is easy or the reward saturates, beats it where the target sits far from the
  prior's dominant mode, and — the actual headline — is far less sensitive to the guidance strength,
  holding performance and valid stereochemistry across a 100× learning-rate range and down to 4×
  fewer diffusion steps, where coordinate guidance destroys the structure. Cost is ~1.4–1.8× DPS per
  step. The gain is bounded by the pretrained model's manifold: where the conformation is not in the
  prior, no inference-time steering recovers it.

- **THE CLAIMED FAILURE MODE OF GRADIENT GUIDANCE, AND ITS EVIDENCE** *(recorded in full because a
  documented failure mode of the standard approach is independently useful)*:

  **The claim, stated as a mechanism (p2, p5):**
  - "their performance depends **sensitively on the likelihood weighting** ... This balance is
    delicate, especially under prior–likelihood mismatch: as illustrated in Figure 1(a), when the
    prior assigns little mass to high-likelihood regions, **DPS fails to generate
    measurement-consistent samples without aggressive likelihood upweighting**." (p2)
  - "when the target lies in a low-density region of the prior, these methods **require aggressive
    upweighting of the likelihood that can destabilize sampling and be sensitive to
    hyperparameters**." (p1, abstract)
  - The proposed mechanism, from the two updates written in a common form (Eqs. 5–6, p5): "DPS pulls
    this gradient back to the noisy-coordinate space via J_{x_t}^⊤, **coupling the update direction
    to the local sensitivity of the denoiser with respect to x_t**. EmbedOpt instead applies a
    J_{c_t} J_{c_t}^⊤ preconditioner: the coordinate update direction **stays within the span of the
    reward gradient**, while its magnitude and anisotropy are modulated by the embedding-space
    geometry." (p5)
  - Third-party corroboration they cite rather than claim: "Raghu et al. [2025] observe that models
    like AlphaFold 3 and Boltz-1 produce samples concentrated around a dominant conformation and
    **report limited optimization stability for their DPS-based method**" (p2).

  **The evidence, and what each piece actually measured:**
  1. *Optimisation-trace volatility* (Fig 2a, p6): reward vs diffusion step for one representative
     system (6V7W chain B), one trace per method — "while DPS's reward trace fluctuates frequently,
     EmbedOpt exhibits a smooth, monotonic improvement of the surrogate reward" (p7). Measured: the
     **surrogate reward**, on **one system**, with **no numeric y-axis**. Weakest piece of evidence
     in the set; "We observe this stability across test systems" (p7) is asserted, not shown.
  2. *Step-count collapse* (Fig 2b, p6): constraints passed and MolProbity vs number of diffusion
     steps (25–200), 24 systems, with α scaled so that α × #steps is constant — "**DPS, in contrast,
     collapses below 100 steps as high learning rates destabilize coordinate updates**" (p7). This
     is the cleanest controlled demonstration: the total guidance budget is held constant, so the
     difference is the per-step step size.
  3. *Local-optimum trapping on a hard target* (Fig 3a, p7–8): 8H1I, "As the target lies far from
     the prior's dominant mode, **DPS fails to correct this topology and stagnates at a local
     optimum (cc = 0.58) even under the best hyperparameters tested**. EmbedOpt, in contrast,
     successfully resolves the global domain rearrangement (cc = 0.93)" (p8; prior cc = 0.42).
     n = 1 system, best-hyperparameter, illustrative.
  4. *Hyperparameter window width* (Fig 3c p7, Fig 7 p23, Fig 9 p24, Fig 8b p23): the central
     evidence, across the whole 77-system benchmark and all 6 real targets — "**DPS requires
     delicate hyperparameter tuning to find a narrow efficacy window of learning rates**, as low
     learning rates provide insufficient guidance while high values produce unphysical structures.
     EmbedOpt exhibits a stable performance plateau across learning rates spanning from 0.01 to 1.0"
     (p8); "EmbedOpt preserves structural validity even at high learning rates, whereas **DPS
     suffers from severe geometric degradation when α > 0.1**" (Fig 7 caption, p23); on real maps
     "**DPS only matches EmbedOpt within a narrow window around α ∼ 0.1 before degrading sharply at
     higher rates**" (p9). **What was measured: the distribution of map correlation and MolProbity
     over systems as a function of a single shared base learning rate, both methods normalised the
     same way.**
  5. *Quantified geometry collapse* (Tables 1–2, p19), the hardest number in the paper: at LR ≥ 0.5,
     DPS map correlation falls to 0.30 [0.00, 0.49] unrelaxed and 0.01 [−0.01, 0.05] relaxed —
     "**DPS collapses (0.30 → 0.01), performing worse than the unguided prior even before
     relaxation**" (p19) — and "**DPS with large LR produce 61.3% degenerate structures that cannot
     be validated by Phenix before relaxation, and 5.6% after. In comparison, EmbedOpt produces only
     1 (0.2%) degenerate sample at large LR.**" (p19)
  6. *Reward-fitting artefacts survive relaxation* (Fig 10, p9, p24): "**coordinate-based steering is
     substantially more susceptible to reward-fitting artifacts than embedding-space optimization.**
     Before energy relaxation, CryoBoltz predictions achieve high map correlation but exhibit
     severely degraded geometry (MolProbity ≫ 2.0); the energy relaxation improves its geometry but
     remains suboptimal compared to EmbedOpt, as **severe stereochemical violations cannot be fully
     repaired by local optimization**" (p9).
  7. *Visual failure mode* (Fig 6, p22): at α = 1.0, "**DPS (bottom) that directly steers noisy
     coordinates can push trajectories off the data manifold, resulting in unphysical, unraveled
     structures that defy energy relaxation.** In contrast, EmbedOpt (middle) remains structurally
     coherent even in this aggressive regime."

  **What the robustness comparison did NOT measure, stated by the authors:**
  - The comparison is **within one base model** only when it is DPS-vs-EmbedOpt; the CryoBoltz
    comparison changes the base model too: "We note that this comparison conflates the base model
    choice (Protenix vs. Boltz-1) with inference-time schemes, while the previous experiment
    disentangles these factors." (p9)
  - The advantage is **not qualitative**: "**EmbedOpt also degrades at extreme learning rates
    (Figure 3c, Figure 7), so the difference is quantitative rather than qualitative; however, the
    degradation onset is delayed and milder.**" (p9)
  - The failure modes are **complementary, not ordered**: "We observe this inverse failure on a small
    subset of targets (e.g., 8F2R, Figure 5), where **DPS's noisy coordinate updates escape an
    embedding-space local mode that EmbedOpt does not. The two methods thus have complementary
    failure modes in different parameter spaces**" (p10); mechanism offered on p21: "DPS's
    stochastic, noise-amplified coordinate updates act as a thermal perturbation that occasionally
    escapes narrow basins, while EmbedOpt's preconditioned, deterministic ascent commits decisively
    to the basin it enters. **The same property that delivers EmbedOpt's headline robustness ... is
    also what penalizes it in this regime.**"
  - DPS in the galleries is given a **per-system best learning rate** (p28–29) while EmbedOpt uses a
    fixed one — a handicap on EmbedOpt, worth noting when reading those panels.

- **necessity_claims** *(verbatim, with pages)*:
  1. p2: "This **necessitates** the incorporation of additional constraints—e.g., derived from
     experimental measurements—that were not present during training."
  2. p2: "when the prior assigns little mass to high-likelihood regions, DPS **fails to generate
     measurement-consistent samples without aggressive likelihood upweighting**."
  3. p9: "EmbedOpt only navigates the structural manifold induced by the pretrained model: when the
     target conformation is poorly represented, **neither EmbedOpt nor DPS recovers it**."
  4. p9: "**Closing this gap requires expanded pretraining or model fine-tuning rather than
     inference-time methods alone.**"
  5. p20: "Embedding optimization is **fundamentally bounded by the support of the pretrained
     model**: gradient ascent on the conditional embedding c **cannot place mass on conformations
     the model has never associated with sequences resembling the target**."
  6. p26: "This result indicates that **evolutionary information is essential for the prior to
     provide a usable starting point**: steering can rescue a degraded prior, but **cannot
     compensate for one that is entirely uninformed**."
  7. p27 (Fig 11 caption): "all methods collapse at 0% MSA, signaling that **evolutionary
     information is essential for the prior to provide a usable starting point**."
  8. p9: "**severe stereochemical violations cannot be fully repaired by local optimization**."
  9. p22: "The energy-relaxation step we apply uniformly to all methods (Appendix E.1) repairs mild
     violations but **cannot fix coarse stereochemical errors once they accumulate**."
  10. p20: "This electron-specific parameterization **is essential for accurately modeling Cryo-EM
      density** and is the standard adopted by gold-standard validation suites such as
      phenix.validation_cryoem."
  11. p3–4 (on why the naive objective is not used): "Directly optimizing this objective via
      gradient-based methods **would require backpropagating through the entire sampling
      trajectory, which can be memory-intensive or numerically unstable**."

- **novelty_claims** *(verbatim, with pages)*:
  1. p2: "This **opens embedding-space optimization as a new algorithmic axis** for inference-time
     steering of protein diffusion models, complementary to the predominant coordinate-space axis."
  2. p3 (Contributions): "(i) **A new algorithmic axis** for inference-time steering of protein
     diffusion models, optimizing the conditional sequence embedding."
  3. p5: "Our work is **orthogonal to coordinate-based methods, unlocking a new axis** for
     biophysical inverse problems."
  4. p3 (Contributions): "(ii) **Theoretical analysis: a trust-region characterization that
     establishes monotonic optimization behavior of EmbedOpt** under small-step updates."
  5. p3 (Contributions): "(iv) **Real-world validation: EmbedOpt matches or outperforms the
     published CryoBoltz baseline on 5/6 experimental cryo-EM targets** while producing
     substantially better stereochemical geometry."
  6. p9 (Discussion): "we introduce EmbedOpt, an inference-time method that steers biomolecular
     sequence-to-structure diffusion models by optimizing conditional embeddings."

  **Priority is explicitly qualified by the authors — both qualifications matter and are recorded
  verbatim:**
  - Concurrent work, p5: "**A concurrent study, Maddipatla et al. [2026], also explores
    inference-time embedding-space optimization**, applying it to ensemble structure generation
    through a multi-round procedure that repeatedly optimizes embeddings across diffusion runs. Our
    work is complementary in scope: we develop embedding-space steering as a general inference-time
    framework that updates the embedding within a single diffusion trajectory, with a trust-region
    analysis and empirical comparison against coordinate-space methods on single-structure
    determination, showing improved robustness."
  - Prior art in the AF2 era, p18: "**Parallel efforts in the deterministic AlphaFold 2 era, such as
    Fadini et al. [2025], explored optimizing latent coevolutionary embeddings to align predictions
    with experimental measurements.**"
  - Prior art outside biology, p18: "A distinct line of work is prompt-tuning in text-to-image
    diffusion models, which steers generation by optimizing the conditioning prompt to maximize
    image-level rewards [Hao et al., 2023, Chung et al., 2023]. **While conceptually similar to
    EmbedOpt — both optimize a conditional embedding** — these approaches typically rely on
    iterative embedding refinement or reinforcement learning loops, incurring substantially higher
    computational cost."
  So the "new axis" claim is **new for protein diffusion, single-trajectory, with a trust-region
  analysis**; embedding/latent optimisation against experimental data is not claimed as new in
  itself.

- **theoretical_claim** *(kept separate from every empirical claim above, per instruction)*:
  **Proposition 1 (informal, p4) / Proposition 2 (formal, p14), with proof p14–15.** Statement:
  under four local regularity assumptions — local `c`-smoothness of the surrogate reward
  (Assumption 1, p13), local `c`-boundedness of the denoiser (Assumption 2, p14), local
  `x`-Lipschitz continuity (Assumption 3, p14) and local `σ`-Lipschitz continuity (Assumption 4,
  p14) — and for a learning rate `0 < α_t ≤ α_max` and a noise step `Δσ_t ≤ Δ_max` with both
  constants depending on the current `(x_t, c_t, σ_t)`, the **surrogate** reward is non-decreasing
  across one EmbedOpt step: `F(x_{t−1}, c_{t−1}, σ_{t−1}) ≥ F(x_t, c_t, σ_t)` (Eq. 15, p14).
  Interpretation given: "This proposition shows that **EmbedOpt acts as a local trust-region
  method**: within a sufficiently small trust region, the gradient-ascent gain (α_t/2)‖g_{c_t}‖² in
  Eq. (4) dominates the deviation from coordinate and noise-level updates, yielding a non-decreasing
  surrogate reward." (p5)
  **Four limits on what it proves, three of them stated by the authors:**
  - It concerns the **surrogate** reward `F(x,c,σ) = R(x̂_θ(x,c,σ))`, not the true reward at `x_0`,
    and not structural accuracy. Nothing is proven about RMSD, cc or geometry.
  - It is **vacuous at a stationary point**: "if c_t is a local optimum with ∇_{c_t}F = 0, this
    assumption is vacuous and there is no reward ascent guarantee against the shift caused by
    coordinate and noise level updates" (p14); "When g_{c_t} = 0, both the first-order improvement
    and the trust-region condition vanish and EmbedOpt remains at a local optimum" (p5). This is
    exactly the observed 8F2R failure (p10, p21).
  - The constants `α_max`, `Δ_max`, `L_c`, `G_x`, `G_σ` are **local and unknown**; the analysis does
    not tell a user what learning rate to pick, and the practical α = 0.1 is chosen empirically.
  - The assumptions are asserted to be plausible, not verified: "Assumptions 1 to 4 ... **hold for
    sufficiently regular denoiser network** x̂_θ(·,·,·) and the reward function R(·)" (p14) — no
    property of Protenix is checked against them.
  - Eq. (6), the DPS-vs-EmbedOpt comparison that carries the mechanistic story, is a **first-order
    Taylor approximation** (Appendix A.3, p16: "We apply a first-order Taylor approximation of
    x̂_θ(x_t, c_{t−1}, σ_t) around c_t ... where the remainder is o(‖c_{t−1} − c_t‖)"), i.e. the
    `J_c J_c^⊤` preconditioner picture is exact only to first order.

- **stated_limits** *(the authors' own, and they are unusually forthcoming)*:
  1. **Three bounding regimes**, given their own subsection (p9–10, expanded p20–23): *manifold
     coverage* — "when the target conformation is poorly represented, neither EmbedOpt nor DPS
     recovers it ... e.g. ... 8K23" (p9, p20); *manifold deviation* — "At aggressive learning rates
     or with reward signals far from the training distribution, EmbedOpt can deviate from the
     structural manifold, producing stereochemical degradation that energy relaxation cannot fully
     repair" (p10); *local optima* — "the trust-region guarantee (Proposition 2) is itself local:
     when the embedding-space gradient vanishes at a non-global optimum, EmbedOpt can be stuck"
     (p10).
  2. Robustness is relative, not absolute: "**Its robustness is quantitative rather than absolute**"
     (p9); "EmbedOpt also degrades at extreme learning rates ..., so the difference is quantitative
     rather than qualitative" (p9).
  3. **Oracle constraint selection admitted** (p6, quoted in full under `oracle_leakage` route 1).
  4. **Base-model confound in the CryoBoltz comparison admitted** (p9, quoted under route 4).
  5. Compute overhead admitted and measured: "EmbedOpt requires roughly 1.4–1.8× the
     per-diffusion-step compute of DPS, reflecting one extra forward pass through the denoiser"
     (p6); memory grows faster with system size because of the `O(N_res²)` pair-embedding gradient
     (p23–25).
  6. DPS is not dismissed: hybrid schemes are proposed as the most promising extension (p9, p22).
  7. MSA dependence is presented as a limit of the whole approach (p26–27).
  8. The synthetic forward model is idealised: uniform B-factor 50 Å², occupancy fixed at 1.0,
     5.0 Å resolution cutoff, no experimental noise model (p8, p20).

- **stance**: **`precedent` on mechanism + `contrast` on evaluation regime — PROVISIONAL, the
  user's call.**
  - *precedent*: it is a direct methodological neighbour — an inference-time intervention on the
    AF3-family conditioning embedding, with a formal statement of why that space is better behaved
    than coordinate space, plus a quantified failure map of the coordinate-guidance alternative
    that is reusable independent of the method.
  - *contrast*: the steering currency is an experimental measurement with a differentiable forward
    model, not a conformational-state instruction; two of three benchmarks manufacture that
    measurement from the deposited answer; there is no held-out or post-cutoff arm at all; and no
    conformational state is ever operationalised as a predicate.

## E. Quantitative comparators

- **metrics_reported**: one row per metric. **Almost every per-system number in this paper exists
  only as a point in a figure; the table below holds what is stated numerically in text, captions or
  Tables 1–4.**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Real-target win rate, EmbedOpt vs CryoBoltz, median over 5 seeds, all three metrics | 5 of 6 | systems | published CryoBoltz baseline (Boltz-1), matched inputs + relaxation + Phenix pipeline | p3, p9, p8 (Fig 4) |
  | Real-target win rate, EmbedOpt vs DPS, CC mask at matched α = 0.1, 100 steps | 6 of 6 | systems | DPS inside the same Protenix prior | p9 |
  | Diffusion-step reduction at preserved constraint satisfaction | 4× (200 → 50 steps) | — | EmbedOpt's own 200-step baseline; DPS "collapses below 100 steps" | p3, p7 |
  | Median constraints passed at 50 steps, EmbedOpt | ≈ 20 of 20 | restraints | K = 20 target restraints, δ = 2.0 Å, 24 systems (**ceiling**) | p7 |
  | Median constraint satisfaction rate maintained, EmbedOpt | > 75 | % | as above | p6 (Fig 2 caption) |
  | MolProbity maintained by EmbedOpt in the step-reduction regime | < 2.0 | MolProbity score | phenix.molprobity | p7 |
  | Learning-rate plateau width, EmbedOpt, synthetic maps | 0.01 – 1.0 (100×, "two orders of magnitude") | base learning rate α | map correlation over 77 systems | p1, p8 |
  | Learning rate above which DPS geometry degrades severely | α > 0.1 | base learning rate α | MolProbity over 77 systems | p23 (Fig 7 caption) |
  | 8H1I map correlation — unguided prior | 0.42 | cc | synthetic 5.0 Å map rendered from deposited 8H1I | p7, p8 |
  | 8H1I map correlation — DPS, best hyperparameters | 0.58 | cc | as above (stagnates at local optimum) | p7, p8 |
  | 8H1I map correlation — EmbedOpt | 0.93 | cc | as above | p7, p8 |
  | Gallery cc, 8CAW_A (easy): prior / DPS / EmbedOpt | 0.81 / 0.92 / 0.95 | cc | synthetic map, best sample after sweep | p21 |
  | Gallery cc, 8W2Q_A (large rearrangement): prior / DPS / EmbedOpt | 0.46 / 0.68 / 0.82 | cc | as above | p21 |
  | Gallery cc, 8F2R_E (**EmbedOpt loses**): prior / DPS / EmbedOpt | 0.43 / 0.86 / 0.66 | cc | as above | p21 |
  | Gallery cc, 8K23_B (**both fail**): prior / DPS / EmbedOpt | 0.08 / 0.28 / 0.33 | cc | as above | p21 |
  | Synthetic map cc, unrelaxed → relaxed, unguided prior | 0.68 [0.47, 0.82] → 0.64 [0.44, 0.79]; paired −0.03 [−0.04, −0.02] | cc, median [IQR] | 77 synthetic maps | p19 (Table 1) |
  | Synthetic map cc, DPS at 0.01 ≤ LR < 0.5 | 0.84 [0.69, 0.92] → 0.80 [0.66, 0.89] | cc, median [IQR] | as above | p19 (Table 1) |
  | Synthetic map cc, EmbedOpt at 0.01 ≤ LR < 0.5 | 0.95 [0.86, 0.98] → 0.89 [0.79, 0.94] | cc, median [IQR] | as above | p19 (Table 1) |
  | Synthetic map cc, DPS at LR ≥ 0.5 (**collapse**) | 0.30 [0.00, 0.49] → 0.01 [−0.01, 0.05]; paired −0.20 | cc, median [IQR] | as above; worse than the unguided prior even unrelaxed | p19 (Table 1) |
  | Synthetic map cc, EmbedOpt at LR ≥ 0.5 | 0.98 [0.93, 0.99] → 0.89 [0.73, 0.94]; paired −0.09 | cc, median [IQR] | as above (**near ceiling unrelaxed**) | p19 (Table 1) |
  | MolProbity, DPS at LR ≥ 0.5 | 4.48 [4.34, 4.66] → 3.27 [2.72, 3.97] | MolProbity, median [IQR] | 77 synthetic maps | p19 (Table 2) |
  | MolProbity, EmbedOpt at LR ≥ 0.5 | 3.60 [2.77, 4.35] → 1.37 [0.89, 2.26] | MolProbity, median [IQR] | as above | p19 (Table 2) |
  | MolProbity, EmbedOpt at 0.01 ≤ LR < 0.5 | 1.92 [1.60, 2.43] → 0.77 [0.64, 0.90] | MolProbity, median [IQR] | as above | p19 (Table 2) |
  | Degenerate structures unvalidatable by Phenix, DPS at high LR | 61.3 before relaxation, 5.6 after | % of samples | 77 synthetic maps | p19 |
  | Degenerate structures unvalidatable by Phenix, EmbedOpt at high LR | 0.2 (1 sample) | % of samples | as above | p19 |
  | Real-map cc, median-CC seed, 9UGC_A: prior / EmbedOpt / DPS / CryoBoltz | 0.04 / 0.64 / 0.62 / 0.60 | cc | EMD-64136, experimental | p28 |
  | Real-map cc, 9UGB_A: prior / EmbedOpt / DPS / CryoBoltz | 0.38 / 0.66 / 0.65 / 0.42 | cc | EMD-64135 | p28 |
  | Real-map cc, 8GMG_A: prior / EmbedOpt / DPS / CryoBoltz | 0.43 / 0.62 / 0.60 / 0.59 | cc | EMD-40026 | p28 |
  | Real-map cc, 8GMJ_A: prior / EmbedOpt / DPS / CryoBoltz | 0.07 / 0.54 / 0.53 / 0.54 | cc | EMD-40027 | p29 |
  | Real-map cc, 8SA0_A (**the one loss**): prior / EmbedOpt / DPS / CryoBoltz | 0.18 / 0.49 / 0.47 / 0.50 | cc | EMD-40258 | p29 |
  | Real-map cc, 8SA1_A: prior / EmbedOpt / DPS / CryoBoltz | 0.43 / 0.57 / 0.55 / 0.56 | cc | EMD-40259 | p29 |
  | Real-target map resolutions (9UGC / 9UGB / 8GMG / 8SA1 / 8SA0 / 8GMJ) | 3.52 / 3.25 / 4.3 / 4.4 / 4.1 / 4.4 | Å | experimental EMDB maps | p24 (Fig 9 headers) |
  | Compute overhead, EmbedOpt vs DPS, per diffusion step | 1.4–1.8× (predicted 1.33×) | relative runtime | matched Protenix runs, H100 PCIe | p6, p25 |
  | Compute overhead, EmbedOpt vs unguided prior | 4.0–4.4× on large targets (6.0× at 177 res) | relative runtime | as above | p25 |
  | Diffusion-loop runtime, 8GMG_A (1280 res): prior / DPS / EmbedOpt / CryoBoltz | 22.1 ± 0.0 / 53.2 ± 0.4 / 97.1 ± 0.2 / 98.7 ± 0.5 | s per trajectory | H100 PCIe, 100 steps (CryoBoltz 200) | p25 (Table 3) |
  | Peak GPU memory, 8GMG_A: prior / DPS / EmbedOpt / CryoBoltz | 10.10 / 23.90 / 30.16 / 27.12 | GB | as above | p25 (Table 3) |
  | End-to-end wall-clock, 8GMG_A: prior / DPS / EmbedOpt / CryoBoltz | 188 ± 4 / 205 ± 7 / 244 ± 1 / 649 ± 84 | s per job | as above; CryoBoltz ~2.7× EmbedOpt | p26 (Table 4) |
  | Fixed per-job overhead, largest system | ≈ 150 (≈ 60–88% of wall-clock) | s | as above | p26 |
  | MSA-depth ablation: prior cc of the three ablation targets (8AHU_A / 8GXU_A / 8K9Z_A) | ≈ 0.87 / ≈ 0.65 / ≈ 0.37 | cc | synthetic maps at 100% MSA | p25 |
  | MSA depth below which all methods collapse | 0 (25% still works) | % of full MSA | 3 targets × 9 runs per depth | p26, p27 |
  | Synthetic map generation resolution | 5.0 | Å | SFC_Torch electron-scattering forward model | p7–8, p20 |
  | Uniform atomic B-factor in the synthetic forward model | 50 | Å² | as above | p8, p20 |
  | Benchmark inclusion filters, synthetic cryo-EM | < 4.5 Å resolution, < 25% sequence similarity | — | PDB | p7 |
  | Restraint sparsity and tolerance | K = 20 pairs, δ = 2.0 | pairs, Å | 24 multi-domain systems | p6 |
  | Sampler constants held fixed (Protenix/AF3 default) | γ = 0.8, γ₀ = 1.0, ρ = 1.003, η = 1.5, N_cycle = 10 | — | Algorithm 2 / Algorithm 4 | p13, p17, p26 |

- **n_predictions**: **stated per arm; no total is ever given, and sweeps make the true total much
  larger than any headline number.**
  - *Samples per target*: "All runs use **3 random seeds** unless otherwise specified" (p6);
    **5 seeds** for the real cryo-EM targets ("Each of the 5 seed predictions are dots", Fig 4
    caption p8; "five independent guided structure predictions were generated" for CryoBoltz, p20);
    **9 runs per MSA depth** in the ablation (3 MSA seeds × 3 diffusion seeds), 3 at 0% and 100%
    (p25); **1 sample per run** in the compute profiling, 3 seeds (p24–25).
  - *Targets*: 24 (distance) + 77 (synthetic maps) + 6 (real maps) = 107, plus 3 reused for the MSA
    ablation and 3 for profiling.
  - *Totals*: **NOT REPORTED.** Not derivable either, because the number of learning-rate values in
    each sweep is given only as an axis in figures (8 values for the synthetic sweep: 0.0025, 0.0050,
    0.010, 0.020, 0.10, 0.20, 0.50, 1.00 — Fig 7, p23; 7 step counts 25/50/80/100/125/160/200 —
    Fig 2b, p6) and the arms are not always crossed. A lower bound on the synthetic-map sweep alone
    is 77 systems × 8 learning rates × 3 seeds × 2 methods ≈ 3,700 structures, plus the prior arm.
  - *Diffusion steps per prediction*: 200 (distance benchmark), 100 (real maps, and the profiling
    runs), CryoBoltz at its native 200 (p7, p9, p20, p25).

- **comparable_to_ours**: *(left empty for the user)*

- **si_in_scope**: **ALL SUPPLEMENTARY MATERIAL IS HELD — appendices A–E occupy p13–29 of this same
  PDF and there is no external supplementary file, no extended data and no separate SI referenced
  anywhere.** The gap is of a different kind and should be recorded as such: **the paper's
  per-system results are almost entirely un-tabulated.** Only four numeric tables exist (Tables 1–2,
  p19, aggregated medians over the whole 77; Tables 3–4, p25–26, compute). Everything else — the
  77-system difficulty scatter, all six real-target metric panels, every learning-rate sweep, every
  MSA-depth curve — exists only as plotted points, so per-system CC, MolProbity, TM-score and RMSD
  values cannot be extracted from the PDF beyond the handful printed on the gallery renders (p21,
  p28–29). The code repository (`github.com/rs-station/embedopt`, p1) is **NOT HELD** by the corpus
  and would be the only route to those numbers.

## F. Figures

**13 figures, 17 panel-group rows, 4 numeric tables (Tables 1–4, not figures; their contents are in
`metrics_reported`).** Split points applied per the v3 rule (split on `mark` or `measure`, never on
`facet` alone): Fig 2 splits because 2a is a line trace of reward against diffusion step while 2b is
a box distribution against step count (different mark and measure). Fig 3 splits three ways: 3a is a
structure render, 3b-left is a scatter of map correlation, 3b-right is a scatter of a *difference* in
map correlation (different measure — a per-system delta, not a level), 3c is a box distribution over
learning rates. Fig 8 splits because 8a is a scatter against a continuous difficulty axis and 8b is a
box distribution over learning rates. Figs 4, 9, 10 and 11 are each **one** row despite carrying
2–5 metric panels, because within each figure the mark is constant and only the facet changes;
their compound measures are written out in the `measure` slot. Figs 5, 6, 12, 13 are galleries of
structure renders and take the RENDER form.

**Pages rendered to fill this table: 8 (p2, p6, p7, p8, p21, p22, p23, p24), at 100–110 dpi.**
Renders were necessary because the captions name panels ("left", "right", "Top", "Bottom") without
ever stating the mark, the number of levels on the independent axis, or the legend dimension; the
learning-rate axis levels, step-count levels, series counts and per-panel metric identities in
Figs 2, 3, 4, 7, 8, 9 and 10 are readable only from the artwork. Temporary PNGs were written under
`ocr/pages/` inside the project directory (`/tmp` is not writable by the image tools here) and
deleted after reading.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 2 | The paper's core intuition on a 1-D toy problem: prior N(5, 0.5²) vs measurement y = 20. Four stacked strips show, in order, the diffusion prior against the measurement; DPS at likelihood weight 1 (samples stay near the prior, as does the exact posterior); DPS at weight 100 (samples move but the landscape is ill-conditioned); EmbedOpt (the prior itself shifts and samples concentrate on the measurement) | line | `PLOT \| facet: sampling scheme (4: prior, DPS w=1, DPS w=100, EmbedOpt) \| vary: x₀, 1-D coordinate, prior mean 5 to measurement 20 (continuous) \| series: curve identity (3: prior/DPS/EmbedOpt density, measurement likelihood, exact posterior) plus a sample-marker series (2: final sample, intermediate trajectory) \| measure: probability density (unitless, unlabelled) \| mark: line \| n: T = 1,000 timesteps; number of sampled trajectories NOT REPORTED` | 4 stacked strips, varying by sampling scheme/likelihood weight, not by system | **No numeric scale on either axis** in any strip — no density tick values, no x tick values beyond the annotated points. Legitimate for an illustration, but the "ill-conditioned sampling landscape" claim it is cited for (p1, p2) has no quantitative panel anywhere in the paper | **NOT REPORTED** — no licence statement appears anywhere in the PDF; the arXiv per-submission licence is not printed in the document |
| 1B | 2 | Schematic of the method: the diffusion trajectory x_T → x_0 running alongside an embedding trajectory c_T → c_0, with the reward R(x̂θ(x_t,c_t,σ_t)) computed from the denoised structure and fed back as a gradient update to the embedding, once per diffusion step; below, the Conditioning Module showing sequence + MSA → Feature Embedder → PairFormer (×N_cycle) → single embedding s and pair embedding z = c_T | schematic | `SCHEMATIC \| two-track flow diagram (coordinate track and embedding track) with a per-step reward-gradient feedback arrow, over an inset of the AF3-style conditioning stack producing s and z \| no data` | 2 regions: (top) per-step update loop ×T_diffusion, (bottom) Conditioning Module. Regions vary by pipeline stage, not by condition | *(blank)* | as row 1 |
| 2A | 6 | Surrogate reward against diffusion step for one representative system (6V7W chain B), DPS vs EmbedOpt: DPS oscillates with high-frequency spikes throughout, EmbedOpt rises smoothly and monotonically to a plateau | line | `PLOT \| facet: none (1) \| vary: diffusion step, t: T → 0, T = 200 (continuous) \| series: method (2: DPS, EmbedOpt) \| measure: surrogate reward value (arbitrary units) \| mark: line \| n: 1 trace per method, 1 system of 24; seeds per trace NOT REPORTED` | 1 panel, single system named in-panel ("system: 6V7W, chain B") | **y-axis carries no numeric scale and no tick values**, so the amplitude of DPS's oscillation relative to the total reward range cannot be read. **n = 1 system of 24** and the caption says only "Representative"; the generalisation "We observe this stability across test systems" (p7) has no panel. No seed variation shown | as row 1 |
| 2B | 6 | Step-efficiency scaling on the 24-system distance benchmark: constraints passed (left) and MolProbity (right) against the number of diffusion steps, with α scaled so α × #steps is constant. EmbedOpt holds ≈20/20 down to 50 steps; DPS falls away below 100 | box | `PLOT \| facet: metric (2: # constraints passed ↑, MolProbity score ↓) \| vary: number of diffusion steps (7: 25, 50, 80, 100, 125, 160, 200) \| series: method (2: DPS, EmbedOpt) \| measure: constraints passed (count, of 20) and MolProbity score \| mark: box with overlaid median line and jittered points \| n: 24 systems × 3 seeds = 72 per box (stated as "3 random seeds" p6, 24 systems p6); per-panel n not printed on the figure` | 2 panels varying by metric; both share the step axis and the 2-method series | **n is not printed anywhere on the figure**; it has to be reconstructed from "3 random seeds" (p6) and the benchmark size (p6). The left panel's measure **ceilings at 20** (see `metric_saturation`), which the box rendering makes look like a tight distribution rather than a saturated one | as row 1 |
| 3A | 7 | Target 8H1I: ground-truth structure in its map, then unguided prior (cc = 0.42, wrong domain orientation), DPS (cc = 0.58, trapped), EmbedOpt (cc = 0.93, domains reoriented), each inside the same grey synthetic density volume | structure render | `RENDER \| facet: method (4: ground truth, prior, DPS, EmbedOpt) \| views: 1 (one camera angle, shared across the four) \| overlay: 1 prediction on 1 reference volume (cartoon inside a transparent map surface; no superposed reference chain) \| axis: none` | 4 panels varying by method, one system | *(blank — cc is printed on every panel, so the render is quantified)* | as row 1 |
| 3B (left) | 7 | Best-achieved steered map correlation against task difficulty (1 − prior map correlation) for all 77 synthetic systems, DPS vs EmbedOpt, with binned-mean lines and a dashed "no improvement" diagonal | scatter | `PLOT \| facet: none (1) \| vary: difficulty = 1 − prior map correlation, 0.0–1.0 (continuous) \| series: method (2: DPS, EmbedOpt) × representation (2: per-system dot, binned mean with band) \| measure: steered map correlation (cc) \| mark: point plus binned-mean line \| n: 1 system per dot, 77 per series per panel; each dot is the best sample over the learning-rate sweep and 3 seeds` | 1 panel; a letter shared with the row below (Fig 3b holds two shapes) | Every dot is a **best-over-sweep** value (p8), so the panel shows an upper envelope, not typical behaviour; the sweep width is not indicated per point. Bin membership counts are not shown | as row 1 |
| 3B (right) | 7 | The same 77 systems replotted as the per-system difference DPS − EmbedOpt against difficulty, with a binned mean difference line, shaded green above zero ("DPS Better") and red below ("EmbedOpt Better") | scatter | `PLOT \| facet: none (1) \| vary: difficulty = 1 − prior map correlation, 0.0–1.0 (continuous) \| series: representation (2: per-system difference dot, binned mean difference) \| measure: Δ map correlation, DPS − EmbedOpt (−0.4 to +0.2) \| mark: point plus binned-mean line \| n: 1 system per dot, 77 per panel` | 1 panel; shares the letter b with the row above, different measure so split per the v3 rule | **The y-axis is asymmetric (−0.4 to +0.2)**, which enlarges the region favouring EmbedOpt relative to the region favouring DPS; the zero line is therefore not centred. No count of systems on each side of zero is given, though "the majority of systems" is claimed in the caption | as row 1 |
| 3C | 7 | Distribution of steered map correlation over all 77 systems at each of eight learning rates, DPS vs EmbedOpt: EmbedOpt holds a plateau from 0.01 to 1.0 while DPS peaks narrowly and collapses at the top of the range | box | `PLOT \| facet: none (1) \| vary: base learning rate α (8: 0.0025, 0.0050, 0.010, 0.020, 0.10, 0.20, 0.50, 1.00) \| series: method (2: DPS, EmbedOpt) \| measure: steered map correlation (cc) \| mark: box (IQR, median highlighted) with overlaid median-connecting line and jittered points \| n: 77 systems × 3 seeds per box; per-panel n not printed` | 1 panel, log-spaced learning-rate axis | n not printed on the figure. The α axis is log-spaced but the eight levels are unevenly sampled (a gap between 0.020 and 0.10), which flattens the shape of DPS's efficacy window | as row 1 |
| 4 | 8 | The headline real-data result: unguided prior, EmbedOpt and CryoBoltz on the six experimental targets, scored on data fitting (CC mask ↑), physical plausibility (MolProbity ↓) and reference agreement (RMSD Cα ↓); five seeds as dots, medians as filled diamonds, x-tick labels coloured by the better method | scatter (strip/dot) | `PLOT \| facet: metric (3: CC mask ↑, MolProbity score ↓, RMSD Cα (Å) ↓) \| vary: target (6: 9UGC_A, 9UGB_A, 8GMG_A, 8SA1_A, 8SA0_A, 8GMJ_A) \| series: method (3: Prior, EmbedOpt, CryoBoltz relaxed) \| measure: CC mask, MolProbity score, RMSD Cα (Å) \| mark: point with median diamond \| n: 5 seeds per method per target; 6 targets per panel` | 3 panels varying by metric; the same six targets and three methods in each | **DPS is absent from the main-text figure** despite being the paper's primary conceptual comparator — it appears only in Fig 10 (p24), i.e. the panel that carries the headline "5/6" claim omits the same-model baseline. Each panel uses its own y-range and none starts at a shared origin (CC mask starts near 0.05, RMSD near 1), so cross-panel magnitudes are not comparable. The dashed "MolProbity ≤ 2.0" guide encodes an unjustified threshold | as row 1 |
| 5 | 21 | Gallery of representative synthetic-map results after hyperparameter sweeping: four systems (8CAW_A easy, 8W2Q_A large rearrangement, 8F2R_E where DPS wins, 8K23_B where both fail) × four columns (ground truth, prior, DPS, EmbedOpt), each cartoon inside the target density, cc printed on every panel | structure render | `RENDER \| facet: system (4: 8CAW_A, 8W2Q_A, 8F2R_E, 8K23_B) × method (4: ground truth, prior, DPS, EmbedOpt) \| views: 1 (one camera angle per system, shared across methods) \| overlay: 1 prediction on 1 reference volume per panel \| axis: none` | 16 panels in a 4 × 4 grid; rows vary by system, columns by method | *(blank — cc printed on all 12 prediction panels, and the gallery deliberately includes the two adverse cases)* | as row 1 |
| 6 | 22 | Failure-mode gallery at α = 1.0 across four systems (8ANE_A, 8AU1_A, 8B3Y_A, 8BBQ_A): ground truth, EmbedOpt (still folded and map-shaped), DPS (unravelled filaments bearing no resemblance to a protein) | structure render | `RENDER \| facet: system (4: 8ANE_A, 8AU1_A, 8B3Y_A, 8BBQ_A) × method (3: ground truth, EmbedOpt α=1.0, DPS α=1.0) \| views: 1 \| overlay: 1 prediction on 1 reference volume per panel \| axis: none` | 12 panels in a 3 × 4 grid; rows vary by method, columns by system | **No cc or MolProbity value is printed on any panel**, so the most visually decisive figure in the paper about DPS's failure carries no number; the quantitative version lives in Tables 1–2 (p19) and Fig 7 (p23) | as row 1 |
| 7 | 23 | MolProbity distribution over the 77 synthetic systems at each of eight learning rates, DPS vs EmbedOpt: both flat and good up to α = 0.1, then DPS rises steeply while EmbedOpt lags behind it | box | `PLOT \| facet: none (1) \| vary: base learning rate α (8: 0.0025, 0.0050, 0.010, 0.020, 0.10, 0.20, 0.50, 1.00) \| series: method (2: DPS, EmbedOpt) \| measure: MolProbity score \| mark: box with median-connecting line and jittered points \| n: 77 systems × 3 seeds per box; per-panel n not printed` | 1 panel | Structures that Phenix **cannot validate at all** are necessarily absent from the boxes — 61.3% of the DPS high-LR arm before relaxation (p19) — so the DPS boxes at α ≥ 0.5 are computed on the surviving minority and **understate** the failure. That exclusion is stated in the appendix text but not on the figure. n not printed | as row 1 |
| 8A | 23 | Best-achieved constraints passed for each of the 24 distance-benchmark systems, ordered along a continuous difficulty axis (initial prior-vs-target distance deviation per constraint), DPS and EmbedOpt in separate stacked panels; most systems sit at 20/20 for both | scatter | `PLOT \| facet: method (2: DPS, EmbedOpt) \| vary: prior distance difference, ~3–100 Å (continuous, log axis) \| series: none (1) \| measure: # constraints passed (count, of 20) \| mark: point \| n: 1 system per dot, 24 per panel; each dot is the best over the learning-rate sweep and 3 seeds` | 2 stacked panels varying by method | The measure is **at its ceiling of 20 for most points in both panels** (the paper says so, p23), so the panel cannot separate the methods — it exists to show that it cannot. Both panels' y-axes are truncated to the top of the range (~17–20 visible), which magnifies the few sub-ceiling points | as row 1 |
| 8B | 23 | Hyperparameter sensitivity on the distance benchmark at fixed 200 steps: constraints passed, total distance violation and MolProbity, each against six learning rates, DPS vs EmbedOpt | box | `PLOT \| facet: metric (3: # constraints passed ↑, total distance violation (Å) ↓, MolProbity score ↓) \| vary: base learning rate α (6 levels, log-spaced) \| series: method (2: DPS, EmbedOpt) \| measure: constraints passed (count of 20), total distance violation (Å), MolProbity score \| mark: box (IQR, 1.5× IQR whiskers, median bar) with median-connecting line and jittered points \| n: 24 systems × 3 seeds per box; per-panel n not printed` | 3 panels varying by metric, shared learning-rate axis and 2-method series | n not printed. The constraints-passed panel is again **ceiling-limited at 20**; the total-distance-violation panel is the only unsaturated view of the same data and is the middle panel rather than the lead | as row 1 |
| 9 | 24 | Learning-rate sweep on the six **real** cryo-EM targets, one column per target with its resolution in the header: CC mask (top row) and MolProbity (bottom row) against α from 0.0025 to 0.5, median lines with IQR bands, individual seeds as dots, and the unguided prior drawn as a flat reference line | line | `PLOT \| facet: target (6: 9UGC_A 3.52 Å, 9UGB_B 3.25 Å, 8GMG_A 4.3 Å, 8SA1_A 4.4 Å, 8SA0_A 4.1 Å, 8GMJ_A 4.4 Å) × metric (2: CC mask ↑, MolProbity ↓) \| vary: base learning rate α, 0.0025–0.5 (continuous, log axis) \| series: method (3: Prior median, EmbedOpt median + IQR band, DPS median + IQR band) \| measure: CC mask and MolProbity score \| mark: line with shaded IQR band and jittered seed points \| n: 3 seeds per point (per p6 default); seeds shown as dots` | 12 panels in a 2 × 6 grid; columns vary by target, rows by metric | **Each panel sets its own y-range** (CC mask tops out at 0.8, 0.6, 0.6, 0.5, 0.5 and 0.5 across the six columns; MolProbity at 5, 5, 4, 3, 5, 5), so the six targets cannot be compared by eye and the apparent size of each method's advantage varies with the column. The prior is a flat line with no band, so its seed variation is not shown | as row 1 |
| 10 | 24 | The full real-target comparison the main text summarises: unguided prior, EmbedOpt, DPS, CryoBoltz unrelaxed and CryoBoltz relaxed on all six targets, across five metrics (CC mask, MolProbity, TM-score, RMSD Cα, RMSD all-atom); EmbedOpt and DPS at a matched α = 0.1 | scatter (strip/dot) | `PLOT \| facet: metric (5: CC mask ↑, MolProbity ↓, TM-score ↑, RMSD_CA (Å) ↓, RMSD_all (Å) ↓) \| vary: target (6: 9UGC_A, 9UGB_B, 8GMG_A, 8SA1_A, 8SA0_A, 8GMJ_A) \| series: method (5: Unconditional prior, EmbedOpt, DPS, CryoBoltz unrelaxed, CryoBoltz relaxed) \| measure: CC mask, MolProbity, TM-score, RMSD Cα (Å), RMSD all-atom (Å) \| mark: point with median diamond \| n: 5 seeds per method per target; 6 targets per panel` | 5 panels varying by metric, same six targets and five methods in each | This is the complete version of Fig 4 and is relegated to the appendix, so the **main-text figure is the one missing the same-model DPS baseline**, not this one. Panels again use independent y-ranges. Five overlapping series in one x-slot makes per-method medians hard to separate at this size | as row 1 |
| 11 | 27 | MSA-depth ablation: map correlation and MolProbity against MSA depth fraction (100% → 0%) for three systems of increasing difficulty (8AHU_A easy, 8GXU_A moderate, 8K9Z_A hard), for the prior and for DPS and EmbedOpt at α = 0.1 and 0.2. Both steering methods beat the prior from 25% to 100% MSA; all three collapse at 0% | line | `PLOT \| facet: system (3: 8AHU_A, 8GXU_A, 8K9Z_A) × metric (2: map correlation ↑, MolProbity ↓) \| vary: MSA depth fraction (5: 100%, 75%, 50%, 25%, 0%; axis drawn descending) \| series: method × learning rate (5: Prior, DPS lr=0.1, DPS lr=0.2, EmbedOpt lr=0.1, EmbedOpt lr=0.2) \| measure: map correlation (cc) and MolProbity score \| mark: line through medians with individual runs as semi-transparent points \| n: 9 runs per point (3 MSA seeds × 3 diffusion seeds), 3 at 0% and 100%` | 6 panels in a 3 × 2 grid; rows vary by system, columns by metric | **The x-axis runs from 1.0 down to 0.0**, i.e. reversed relative to the usual reading, so the collapse appears on the right where a reader expects the full-information end. Per-panel y-ranges differ (MolProbity tops at 3.0, 4.5 and 3.5 across the three rows). n = 3 at the two endpoint depths vs 9 elsewhere, so the collapse point is the least-sampled point on every curve | as row 1 |
| 12 | 28 | Per-system gallery for the first three real cryo-EM targets (9UGC/EMD-64136, 9UGB/EMD-64135, 8GMG/EMD-40026): the median-CC seed of prior, EmbedOpt, DPS and CryoBoltz inside the experimental density, cc printed under every panel | structure render | `RENDER \| facet: target (3: 9UGC_A, 9UGB_A, 8GMG_A) × method (4: Prior, EmbedOpt, DPS, CryoBoltz) \| views: 1 (one camera angle per target, shared across methods) \| overlay: 1 prediction on 1 experimental map per panel \| axis: none` | 12 panels in a 3 × 4 grid; rows vary by target, columns by method | The displayed model is the **median-CC seed** of 5 (a selection rule, stated in the caption), and **DPS is shown at its best per-system learning rate while EmbedOpt is fixed at α = 0.1** (caption, p28) — a defensible handicap on the authors' own method, but it makes the panels non-matched | as row 1 |
| 13 | 29 | Continuation of the gallery for the remaining three real targets (8GMJ/EMD-40027, 8SA0/EMD-40258, 8SA1/EMD-40259) under the identical protocol | structure render | `RENDER \| facet: target (3: 8GMJ_A, 8SA0_A, 8SA1_A) × method (4: Prior, EmbedOpt, DPS, CryoBoltz) \| views: 1 \| overlay: 1 prediction on 1 experimental map per panel \| axis: none` | 12 panels in a 3 × 4 grid, same layout as Fig 12 | as Fig 12 (median-CC seed selection; DPS at per-system best α, EmbedOpt fixed) | as row 1 |

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), session 2026-09-08
- **schema_version**: v3
- **confidence**: **high** on identity, the mechanism (which tensor is optimised, against what, when,
  and what is held fixed — Algorithms 1 and 2 are explicit, p4 and p13), the verbatim claim set, the
  failure-mode analysis of DPS, the control table, the numeric tables, and the figure panel
  structure (eight pages rendered). **High** on `oracle_leakage`, because the authors state the
  decisive route themselves (p6) and the appendix protocols (p20) are unusually complete.
  **Medium** on two points only: (i) the exact number of structures generated in total, which is not
  derivable from the text (see `n_predictions`); (ii) whether the synthetic-map arm's headline
  numbers are best-over-sweep in every panel or only in Fig 3b — the phrase "after sweeping learning
  rates" is attached to Fig 3b (p8) and to Fig 5 (p21), and Fig 3c is explicitly per-learning-rate,
  but Fig 8a's "best achieved" is not qualified. The text layer is clean throughout; mathematical
  symbols (σ, α, ∇, J, η, γ, ρ) extract correctly and the algorithm boxes are legible.
- **unresolved**:
  1. **Total structure count is not recoverable.** Sweep widths appear only as figure axes, and the
     arms are not fully crossed. Reported per-arm in `n_predictions` with a lower bound; the
     repository would settle it.
  2. **No per-system numbers outside the galleries.** Fifteen of the seventeen figure rows carry
     data that exists nowhere in tabular form (see `si_in_scope`). Anything the corpus wants to cite
     per-target — beyond the cc values printed on Figs 5, 12, 13 — would have to be re-derived from
     the code.
  3. **`prospective` deliberately not tagged.** The verdict is `partial`: one arm of 6 real targets
     is prospective in its inputs, two arms of 101 targets are not, and every arm scores against a
     deposited reference. Tagging `prospective` would return this paper for "which papers were
     prospective" on the strength of its smallest arm. Flagged for the user rather than decided.
  4. **`multi-backbone` deliberately not tagged.** Protenix and Boltz-1 both appear, but the schema
     sets the bar at "more than two are compared head to head", and the authors themselves say the
     two-backbone comparison is confounded with the method comparison (p9).
  5. **Tag needed but not in the v3 vocabulary: something for experiment-guided / inverse-problem
     structure determination.** This paper's task is "fit a structure to a measurement" — cryo-EM
     map fitting, cross-link/FRET-style distance restraints — which is neither conformational-state
     sampling nor docking, and no Method or Control tag names it. `latent-steering` correctly names
     the *mechanism* and is applied, but a reverse lookup for "which papers fit structures to
     experimental data" has no tag to return. Two other corpus-relevant papers are cited here in
     exactly this category (Maddipatla et al. 2025; CryoBoltz / Raghu et al. 2025), so the gap will
     recur. Not invented.
  6. **Second tag needed but not available: something marking a paper that proves a formal result.**
     This one carries a proposition with four assumptions and a four-step proof (p13–15), and that
     theoretical content is a distinguishing feature no tag expresses. `benchmark-only` is its
     opposite; nothing else is close. The theoretical claim is recorded separately in section D as
     instructed, but it is invisible to tag-based retrieval.
  7. **Third tag needed but not available: something for a documented failure mode of a *baseline*
     method.** `negative-result` exists under "Relation to us" and would misfile this as a negative
     result about the paper's own method, which it is not — the paper's DPS collapse data (p19,
     p22, p23) is a positive result about the fragility of the standard approach. Not applied.
  8. **`experimental-validation` deliberately not tagged.** The real cryo-EM arm uses experimental
     *data* as an input, which is not the same as testing a prediction in the lab; the tag's gloss
     ("tested a prediction in the lab (NMR, cryo-EM, an assay)") could be read either way. Read
     strictly here: nothing was measured for this paper.
  9. **`templates` is NOT REPORTED, not "off".** The word never occurs; Protenix's default template
     handling is not stated and must not be assumed.
  10. **No licence anywhere in the PDF**, so every `reuse` cell is NOT REPORTED. The arXiv
      per-submission licence is not printed in the document. The code repository
      (`github.com/rs-station/embedopt`, p1) is not held and its licence is unknown.
  11. **Venue.** NeurIPS-style typesetting, but the document says only "Preprint." (p1). Whether a
      conference version exists is not determinable from this PDF.
  12. **Relationship to `Fadini et al. 2025` and to the concurrent `Maddipatla et al. 2026`** is
      stated by these authors (p5, p18) and taken at face value here; neither is held by the corpus
      as far as this extraction can tell, and both are direct methodological neighbours of the
      "optimise the embedding" idea. Worth acquiring.
- **why_it_matters**: *(left empty for the user)*

## Tags

`general-protein` `latent-steering` `single-state` `binary-predicate` `continuous-metric`
`saturating-metric` `oracle-leak` `design-level-oracle` `no-anti-memorization` `directed-state`
`preprint` `precedent` `contrast` `comparator-numbers`

Tags withheld, with reasons above: `prospective` (item 3), `multi-backbone` (item 4),
`experimental-validation` (item 8), `confidence-as-discriminator` (no confidence metric is used at
all), `visual-metric` (every structural call is backed by cc), `rmsd-only` (RMSD is one of five
metrics, not the only one), `templates-on` / `no-template-no-msa` / `state-annotated-input` (template
handling never stated; MSAs are used at full depth), `msa-subsample` (subsampling appears only as an
ablation probing MSA dependence, not as the method's state handle), all other Method tags (no
co-folding, clustering, MD, emulator or enhanced sampling is performed), all State-handling tags
except `single-state`, all Site tags (no site is studied), `unpowered` (no control arm exists to be
underpowered), `negative-result` (item 7), `figure-exemplar` (the paper is kept for its method and
its numbers, not as a figure model).
