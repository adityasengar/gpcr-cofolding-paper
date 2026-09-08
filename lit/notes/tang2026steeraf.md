# tang2026steeraf

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–42).** For the main
article the PDF page equals the printed page (PDF p14 prints "14"). The Supplementary
Information is bound into the same PDF as **PDF pages 31–42**, which print as SI pages
S1–S12. Mapping for SI quotes: PDF p31 = S1 (SI title), p32 = S2 (Table S1
hyperparameters), p33 = S3 (Tables S2 and S3, curated residue sites), p34 = S4
(Figure S1), p35 = S5 (Figure S2), p36 = S6 (Figure S3), p37 = S7 (Figure S4),
p38 = S8 (Figure S5), p39 = S9 (Figure S6), p40 = S10 (Figure S7), p41 = S11
(Figure S8), p42 = S12 (SI reference list).

**The SI is bound in but holds no numeric results.** Tables S1–S3 (hyperparameter
defaults and curated residue lists) are here; Figures S1–S8 are here. But **every
per-system and per-dataset performance number in this paper exists only as a plotted
point or bar** — there is no results table anywhere in the 42 pages. See `si_in_scope`.

**Text-layer note:** the text layer is usable but figure panels scramble badly
(multi-column figure text interleaves). Figure 1B's method legend extracts as 6 methods
when the rendered panel shows 8. Pages **4, 37 and 41** were rendered at 150 dpi and read
directly to establish marks and legends; all other figure rows were filled from captions
plus the text layer.

---

## A. Identity

- **citekey**: `tang2026steeraf`
- **doi**: **bioRxiv 10.64898/2026.06.19.733296** — p1 header: "bioRxiv preprint doi:
  https://doi.org/10.64898/2026.06.19.733296; this version posted June 19, 2026."
  No journal DOI anywhere in the PDF.
- **year**: **2026.** p1 header: "this version posted June 19, 2026".
- **venue**: **bioRxiv preprint. Explicitly not peer-reviewed.** p1 header, verbatim:
  "(which was not certified by peer review) is the author/funder, who has granted bioRxiv
  a license to display the preprint in perpetuity." No journal masthead, no
  received/accepted line. Formatted in ACS `achemso` style (E-mail block, "Acknowledgements",
  ACS reference formatting), suggesting an intended ACS submission, but no journal is
  named. Tagged `preprint`, not `peer-reviewed`.
- **title**: "SteerAF: Distogram-based Steering of AlphaFold2 toward Alternative
  Conformations" — p1.
- **authors**: Jiajun Tang¹, Zefeng Zhu^{1,2}, Song Yang³ (all three "contributed equally"),
  and Chen Song^{1,2,*} (corresponding, c.song@pku.edu.cn) — p1. ¹ Center for Quantitative
  Biology, Academy for Advanced Interdisciplinary Studies, Peking University; ² Peking-Tsinghua
  Center for Life Sciences, Peking University; ³ Fujian Provincial Hospital Affiliated to
  Fuzhou University, School of Medicine, Fuzhou University.
  **Self-citation note relevant to the central premise:** the "distograms encode alternative
  states" claim rests on the group's own two prior papers — refs 34 (Li, Wang, Zhu, Song,
  *JCIM* 2024) and 35 (Li, Zhu, Song, bioRxiv 2024), cited on p2 as "our prior works" and on
  p27 in the reference list.

## B. Scope

- **system**: **General protein + transporter, dual.** The four evaluation datasets are
  (p5, Table 1): domain-motion proteins (16), an open–close set "oc23" (23), a
  transmembrane/transporter set "tp16" (15 used), and a fold-switch set (15). The tp16 set
  is entirely transporters (Figure S1 system list, p34: AAC3_OUT, MDFA, MELB, MFSD2A_OUT,
  MURJ, PTSG, SLC1A1_OUT, SLC39, WLAB_OUT, …). The remainder are mixed bacterial and
  eukaryotic soluble enzymes and periplasmic-type binding proteins. **No GPCR appears in
  any of the four conformational benchmarks** — see `unresolved` item 1. The single GPCR in
  the paper, human β2AR (P07550), appears only in the residue-interpretability analysis
  (p12) with no conformational accuracy metric reported.

- **n_targets**: **69 in the conformational benchmark, plus four other populations that
  must not be collapsed into it.**
  - **Main benchmark: 69 systems** = 16 domain-motion + 23 oc23 + 15 tp16 + 15 fold-switch
    (Table 1, p5; every system named in Figure S1, p34). Note tp16 is *named* for 16 but
    Table 1 lists 15: "The SPF1 system was excluded from the benchmark due to its intractable
    length, which causes an out-of-memory issue" (Figure 1 caption, p4).
  - **Reference-free selection evaluation: 46 systems** (p9), "among the systems in which
    both conformations were successfully predicted" — a success-conditioned subset of the 69,
    not an independent set.
  - **In-house multi-conformation dataset: 18 proteins** (p14), used only to report the
    ≥3-state failure. Not otherwise described, not named, not in the SI.
  - **Interpretability: 2 systems** — PGK1 (P00558) and hβ2AR (P07550), pp11–12.
  - **MD application: 2 systems** — MdfA (Figure 5, p15) and AAC3 (P18238, Figure S5, p38).

- **method_class**: **other** — inference-time gradient-based *hallucination* on the MSA
  input feature tensor, with the gradient supplied by the frozen model's own distogram head.
  Not MSA subsampling (that is a comparator arm), not state filtering, not template biasing.
  p17: "SteerAF is therefore essentially an inference-time optimization of OpenFold." The
  v3 `method_class` list has no entry for latent/tensor steering even though the v3 tag list
  gained `latent-steering`; see `unresolved`.
  **A downstream MD arm is genuinely run**: 2.5 µs aggregate per system on MdfA and AAC3
  (pp12, 23–24).

- **backbones**: **SteerAF itself is AF2-only**, implemented on OpenFold (ref 36): "The
  distogram-guided optimization pipeline is built on OpenFold (the open-source reproduction
  of the official AlphaFold2 project)" (p17). **The benchmark, however, compares three
  backbones head to head** — AF2/OpenFold (SteerAF, AFsample2, MSAsubsample, AlphaFold2
  baseline), AF3 (AFsample3, AlphaFold3 baseline), and Boltz-2 (Boltz-sample, ref 45), plus
  ConforMix (ref 21) — Table 2, p6, and the 8-method legend rendered from Figure 1B, p4.
  Tagged `multi-backbone` on the comparison, not on the method.

- **templates**: **off, explicitly.** p17, verbatim: "In AlphaFold2's design, the model takes
  three types of inputs: the input sequence, the MSA, and templates. **Because our method
  does not use template information, only the first two are used in practice.**"

- **msa_handling**: **full, then gradient-modified — this is neither subsampled nor
  state-filtered and must not be collapsed into either.** A deep MSA is built by AlphaFold's
  default pipeline and split into the MSA feature and the extra MSA feature "whose sequence
  counts are typically in a 1:10 ratio" (p17). Only the MSA feature is optimized: "Distogram-guided
  optimization therefore optimizes only the MSA feature, keeping the extra MSA feature fixed"
  (p17). No sequences are removed, clustered, or replaced; the *numerical embedding* of the
  retained alignment is moved by SGD. Depth is never reduced. MSAsubsample (max extra MSAs
  ∈ {16 … 5120}, Table 2 p6) appears only as a comparator arm.

## C. Conformational core

- **states_generated**: **ensemble + two.** Per target SteerAF emits 420 structures = 60 runs
  × 7 steps (T = 6 optimization steps → T+1 predictions; p18, Table 2 p6). Each run is a
  *trajectory*, not an i.i.d. sample: "in the first few steps, the result is usually closer to
  the default conformation, and only in the last or middle steps does the conformation approach
  the alternative conformation" (p7). So the output is an ensemble in count, but it resolves
  into at most two distinct basins for most systems, and the paper says so: on an in-house
  18-protein multi-state set, "7/18 proteins yielded only one predicted conformation, 7/18
  proteins yielded two, and 2/18 proteins yielded three or more" (p14). (7+7+2 = 16, not 18;
  see `unresolved`.) The paper is a **two-state method by construction** — the loss has one
  reference (the default) and one direction (away).

- **structural_priors_used**: **Substantial, and at design time this is not a defect.**
  1. **The four benchmarks are curated two-state sets in which both conformations are
     deposited.** Table 1 (p5) reports, per dataset, the TM-score *between the two reference
     conformations* (domain motion 0.6813 mean / 0.8370 max / 0.5070 min; oc23 0.5009 /
     0.6450 / 0.3790; tp16 0.7892 / 0.9690 / 0.3730; fold switch 0.6672 / 0.9004 / 0.4817).
     Computing that column requires both structures in hand for all 69 systems.
  2. **Datasets are inherited from competitor papers**, not built here: domain motion from
     ref 20 (Lewis *et al.*, BioEmu, *Science* 2025), oc23 and tp16 from ref 11 (Kalakoti &
     Wallner, AFsample2), fold switch from refs 9 and 21 (Lee *et al.* sequence-association /
     CF-random, and Richman *et al.* ConforMix) — Table 1 superscripts, p5.
  3. **PGK1 curated residue set** (Table S2, p33) is drawn from published mutagenesis, kinetic,
     DSC and SAXS studies since 2000 (p11, §5.7 p22). Independent of SteerAF and used only as
     an evaluation target.
  4. **hβ2AR curated residue set** (Table S3, p33) is drawn from constitutive-activation
     mutagenesis *plus* microswitch positions defined from deposited structures: "These residues
     correspond to established hβ2AR microswitch motifs—the DRY motif (D130/R131/Y132), the
     PIF/connector motif (P211/I121/F282), the rotamer toggle-switch region (C285/W286), and
     the NPxxY motif (N322/P323/Y326)—identified through active- versus inactive-state
     structural comparisons and allosteric network analyses" (p22–23), and N318 from "comparison
     of the inactive- and nanobody-stabilized active-state structures" (p23).
  5. **MD basin naming** uses deposited references: MdfA 6VS1 and 6GV1 (p14, Figure 5C p15);
     AAC3 4C9J (cytoplasmic-open c-state) and 6GCI (matrix-open m-state) (Figure S5, p38).

- **oracle_leakage**: **Routes 1, 2 and 3 are genuinely clean. Routes 4, 5, 6 and 7 are all
  present. Crucially, route 1 is clean in the place that matters most — the steering signal
  itself does not come from a deposited structure of the target state.** Enumerated:

  **Route 1 — deposited structures used as input or template: NONE FOUND.** Templates are
  off (p17, quoted above); inputs are sequence + MSA only. **The reference the loss is computed
  against is the model's own step-0 prediction, not any experimental structure.** Verbatim,
  p18: "We first compute the default distogram cross-entropy, **treating the distance bins of
  the step-0 predicted structure (𝑥₀) as the target one-hot distribution** and the distogram
  of the step-𝑖 prediction (𝑧ᵢ) as the predicted distribution for each residue pair 𝑘."
  And p19: "SteerAF performs gradient ascent in the direction of increasing this final loss."
  Restated in Results, p5: "we compute the cross-entropy (the distogram loss) between the
  pairwise distances of **the default conformation** and the pairwise distogram output by the
  model at each step, which serves as the core of the loss function". The whole scheme is
  self-referential: it pushes away from AF2's own default output. **The alternative-state
  distance pattern is taken from the alternative peak already present in AF2's distogram
  (p5: "amplifying the signal of the alternative peak in the distogram as much as possible"),
  not from a PDB entry.** This is the paper's real self-supervision claim and it holds.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving
  templates or alignments: NONE FOUND.** No structural state database is named anywhere. The
  benchmark protocol is on p5 (Table 1) and pp17–18 (§5.1); no annotation source enters the
  MSA or the templates, because there are no templates and the MSA is unfiltered.

  **Route 3 — cluster labels derived from known states: NONE FOUND in the selection pipeline
  itself.** p9, verbatim: "We then applied the PCA + HDBSCAN pipeline described above **without
  using any reference conformation.**" The clustering runs on internal Cα distance matrices
  restricted to common ordered-SS residue intervals identified from step 0 (p9). *Caveat that
  is not route 3 but is adjacent:* the HDBSCAN parameter choice is guided by pLDDT, not by
  references — Figure 3A caption, p10: "The first PCA map is colored by pLDDT **to guide the
  choice of appropriate HDBSCAN clustering parameters and the clustering itself**."

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
  states: FOUND, and it is a range tuned on the evaluation set, which v3 counts as leakage even
  with no per-target value chosen.** Three separate instances:
  - §5.5, p21, verbatim: "We tested three important SteerAF hyperparameters over a broad range:
    learning rate lr (2×10⁻³, 2×10⁻², and 5×10⁻²), fixed pLDDT loss weight 𝜆ₚ (0.33, 0.50, 0.67,
    and 0.80), and sample ratio 𝜌 (5% and 10%). … At a sample ratio of 10%, **all combinations
    of learning rate and pLDDT loss weight were evaluated on the OC23_TP16 and fold-switch
    datasets.**" OC23, TP16 and fold-switch *are* three of the four evaluation datasets (53 of
    the 69 systems). The sweep metric plotted in Figure S8 (p41) is TM-score and RMSD to the
    reference conformations. The recommended defaults (Table S1, p32) are the argmax of that
    sweep: "the peaks of cross-system Gaussian-kernel-smoothed performance curves were more
    concentrated near a learning rate of 2×10⁻² and a pLDDT loss weight of 0.50, suggesting that
    this combination is suitable for most systems" (p21).
  - **Stopping criterion set on the evaluation set**, p7, verbatim: "As shown in Figure 2C, the
    increase in the best TM-score slows markedly after 6 optimization steps, whereas the near-best
    prediction ratio continues to decline. Varying the number of runs shows a similar tradeoff.
    **We therefore chose 6 optimization steps and 10 or 20 runs per hyperparameter combination as
    the balanced fixed settings for prediction.**" Best TM-score is measured against the held
    reference; T = 6 is therefore a reference-tuned stopping rule.
  - **The recommendation for new systems is derived from an evaluation-set failure**, p16,
    verbatim: "For PF0708, SteerAF succeeded at a 20% sample ratio. **We accordingly recommend
    that users applying SteerAF to entirely new systems explore a wider hyperparameter range,
    with a sample ratio 𝜌 ≤ 20% and learning rate lr ≤ 2e-2 as a reasonable range.**" PF0708
    is a tp16 benchmark system (Figure S1, p34).

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had: FOUND, pervasively.
  Every headline number in the paper is reference-defined.** Four of the five metrics are explicit
  functions of a held reference (§5.4, pp20–21): best TM-score and best RMSD; fill ratio
  (Eq. 8, p20: "A predicted structure is counted as successfully close to the target conformation
  when it satisfies both TM-score > thr_tms and RMSD < thr_RMSD", instantiated as TM > 0.85 and
  RMSD < 3.0 Å in Figures S2 and S7); cluster spread (Eq. 9, p21, computed over the reference-close
  subset); near-best run ratio (Eqs. 10–11, p21, defined as TM ≥ 0.97 × TM_best, with TM_best a
  reference quantity). The acceptance thresholds themselves were set from the references, p9,
  verbatim: "To evaluate the selection, **we first used the reference conformations to define a
  scoring criterion**: a structure with TM-score > 0.85 and RMSD < 3 Å to a reference conformation
  is regarded as correctly predicting that conformation; the choice of these thresholds is justified
  in Figure 3B".

  **Route 6 — best/worst model labels assigned against a held reference: FOUND, and it propagates
  into the interpretability result.** The PSSM analysis — the paper's main biological claim — is
  computed only over runs selected by TM-score to the reference. p11, verbatim: "We then analyzed
  the MSA features from **near-best runs, defined here as runs containing predictions that reached
  at least 97% of the best TM-score for the target.**" Same for the site-restoration control:
  "we restored the last near-best step MSA feature values to their corresponding step-0 values"
  (p11). The ~50%-precision functional-residue recovery is therefore conditioned on a
  reference-based run filter and is **not** available in a blind setting.

  **Route 7 — design-level oracle use (weaker than pipeline leakage; label it as such): FOUND.**
  Every evaluated system was chosen because both conformations are already deposited — Table 1
  (p5) reports the inter-state TM-score for all 69 systems, which presupposes both structures.
  The reference-free selection experiment is likewise conditioned on knowing the answer: it is
  evaluated only "among the systems in which both conformations were successfully predicted"
  (p9, n = 46). And the two interpretability systems are chosen where the functional-residue
  answer is already published (§5.7, pp22–23). None of this feeds the model; all of it means the
  expected state was declared before the result was read. **This is design-level, not pipeline-level.**

- **prospective**: **partial, and the split is unusually clean.** *Prospective in the biasing
  pipeline*: nothing about the target state enters the model — no template, no state-filtered
  MSA, no reference structure; the steering target is AF2's own step-0 output (p18). *Retrospective
  in evaluation and in configuration*: success is defined by TM/RMSD to held references (§5.4,
  pp20–21), the run filter for the interpretability analysis is reference-based (p11), and the
  hyperparameter grid and stopping step were tuned on the evaluation datasets (§5.5 p21, p7).
  The reference-free PCA + HDBSCAN arm (pp8–9) is the one genuinely prospective *selection*
  experiment, and even it is scored against references and evaluated only on systems already
  known to have succeeded.

- **state_metric**: **continuous coordinate + binary predicate, dual.** Continuous: TM-score and
  Cα RMSD to each reference, reported as best-of-N (§5.4, p20), and distance-based PCA coordinates
  (PC1/PC2) used throughout Figures 3 and 5. Binary predicate: **TM-score > 0.85 AND RMSD < 3.0 Å**
  to a given reference conformation defines "correctly predicting that conformation" (p9, and the
  panel titles of Figures S2/S7, pp35/40: "Full ratio open (TM>0.85 & RMSD<3.0Å)"). A second
  predicate, TM ≥ 0.97 × TM_best (Eq. 10, p21), and a stricter variant additionally requiring
  TM > 0.85 (Eq. 11, p21).
  **Threshold justification:** partial and self-admittedly system-dependent. p9, verbatim: "This
  threshold may vary across protein systems: for example, **GPCR conformations can be separated by
  relatively small structural differences and may require stricter thresholds**, whereas many
  domain-motion proteins involve larger conformational changes and can tolerate looser criteria."
  The 0.85/3.0 Å pair is justified by eye from Figure 3B on a *single* system (AAC3_OUT) and then
  applied to all 69. **Whether any per-system threshold adjustment was actually made is NOT
  REPORTED** — the figure panel titles show one fixed pair.
  A third, purely visual call also occurs: MdfA basin B3 "may show as an intermediate occluded
  state" (p14) with no operationalised predicate.

- **metric_saturation**: **Yes, and the authors identify one instance themselves and patch it.**
  1. **Near-best run ratio, first definition, floors/ceilings spuriously.** p21, verbatim:
     "**Without an absolute TM-score requirement, a poorly predicted target could still have a high
     near-best ratio simply because many low-quality predictions are close to an equally low-quality
     best prediction.** Thus, we use the second definition of near-best ratio when there is a lack of
     best TM-score/RMSD information." The unpatched first definition is nevertheless the one plotted
     in Figure 2 (p8) — the paper says so explicitly on p21 — so Figure 2A's x-axis carries the known
     defect.
  2. **TM-score saturates against the benchmark's own inter-state similarity.** tp16 has mean
     inter-state TM 0.7892 and **max 0.9690** (Table 1, p5); fold switch max 0.9004; domain motion
     max 0.8370. For a pair separated by TM 0.969, returning the default conformation already scores
     above the 0.85 acceptance predicate. Figure 1B (p4) shows every method clustered between 0.84
     and 0.95 best TM-score on all four datasets — a ~0.1 band on a metric bounded at 1.0. **Note
     that this benchmark therefore does not exclude globally-similar two-state pairs**, unlike the
     construction the Cfold/AFsample-family exclusions apply; see `unresolved` item 3.
  3. Axis truncation in Figures 1B, 2A, S4, S8 is a *figure* defect and is recorded in `hides`
     on those rows, not here.

- **directional_control**: **NO. The method cannot be instructed which state to produce. It has
  exactly one direction — "away from whatever AF2 predicted by default" — and no handle at all.**
  This is the single most important finding in this note.
  - There is no partner, no ligand, no nanobody, no peptide, no state-annotated template, no
    state-filtered MSA, and no target distance restraint. The only user-facing knobs are the eight
    hyperparameters in Table S1 (p32): T, N, K, thr_mask, K_p, 𝜆ₚ, 𝜌, lr. Every one of them controls
    *how hard and how far* the optimizer pushes, not *where*.
  - The objective is explicitly repulsive, not attractive. p5, verbatim: "**Our goal is to prevent
    the dominant peak of the model's output distogram from overlapping too closely with the pairwise
    distances of the default conformation, while amplifying the signal of the alternative peak in the
    distogram as much as possible.**" The target one-hot in Eq. 4 (p18) is the step-0 *default*
    structure and the update is gradient *ascent* on cross-entropy to it (p19).
  - The paper states the consequence itself, and it is a direct admission that direction is not
    controllable when more than one alternative exists. p14, verbatim: "We reasoned that the
    alternative peaks from multiple conformations are mixed within a single distogram, whereas our
    method relies on driving the predicted conformation's distogram away from the default
    conformation's distribution; **this loss function inherently cannot separate the alternative peak
    signals originating from different conformations.**"
  - Consequently the method **only diversifies, along one axis**. It is directional in the trivial
    sense that it is not random (it moves away from the default rather than jittering), but a user
    who wants the *active* state rather than some other non-default state has no way to ask for it.
  - The mask (thr_mask = 4, p18) does select *which residue pairs* get upweighted — those "whose
    step-0 distance bins and distogram have high cross-entropy, which are precisely the positions
    more likely to contain alternative-peak information" (p18) — but that selection is computed from
    the model's own distogram, not supplied by the user, so it is not a control handle either.
  - Where the alternative distance pattern comes from: **from the secondary peaks of AF2's own
    distogram**, which the authors argue are a training artefact of distribution matching (Eq. 2,
    p4: "the model must fit the empirical distribution of distance labels rather than a one-hot
    target", p4–5). Not from any deposited structure of the target state.

- **anti_memorization_design**: **NONE as a design. One incidental post-cutoff system, n = 1,
  observed only to explain a failure.** There is no held-out set, no post-cutoff split, and no
  stated cutoff for the benchmark as a whole. The only cutoff discussion in the paper, p16 verbatim:
  "For A6UVT1, neither AlphaFold2 nor AF2-based methods predicted the alternative conformation,
  whereas AlphaFold3, AF3-based methods, and Boltz-based methods all succeeded. **All PDB depositions
  of A6UVT1 date from 2019, whereas the training data cutoff for AlphaFold2 is 2018-04-30 and for
  AlphaFold3 and Boltz is in or after 2021. Therefore, we cannot exclude the possibility of
  training-data leakage for the methods that successfully predicted this alternative conformation.**"
  That is a post-hoc explanation of one AF3/Boltz advantage, not an anti-memorization design. The
  memorization literature is cited (ref 6, Chakravarty *et al.* 2024, "AlphaFold predictions of
  fold-switched conformations are driven by structure memorization", p25) but never acted on.
  Deposition dates for the other 68 systems are NOT REPORTED.

- **anti_memorization_control**: **NONE RUN, and UNPOWERED even if the single case were counted
  (n = 1).** No control arm was executed or analysed. No post-cutoff subset was scored separately;
  no scrambled-sequence, shuffled-MSA or homolog-removed arm exists. The A6UVT1 observation (p16)
  is narrative, not an arm. Because SteerAF's premise is that AF2's distogram *already encodes*
  the alternative state, the memorization confound is load-bearing for this paper specifically —
  and it is untested.

- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | SteerAF-GA (dense gradient, whole MSA feature updated) vs SteerAF-BGA (sparse block updates) | That sparsity is doing the work, or that block sampling costs accuracy. Median best TM-score +0.009 for BGA; >0.05 better on 7 systems, clearly worse on 3 | p19, Fig S6 p39 |
  | Three gradient-regularization schemes: unit / exp / norm | That the result depends on one specific regularizer. "no significant difference in overall performance on the full dataset" | p20, Figs S6 p39, S7 p40 |
  | Hyperparameter grid: lr ∈ {2e-3, 2e-2, 5e-2} × 𝜆ₚ ∈ {0.33, 0.50, 0.67, 0.80} at 𝜌 = 10% | That the result is a knife-edge of one setting. "no strong monotonic trend across the hyperparameter space". **Note: this doubles as route-4 leakage — it was run on the evaluation datasets** | p21, Fig S8 p41 |
  | AlphaFold2 and AlphaFold3 repository-default baselines at 1000 predictions each | That plain sampling at high budget already reaches the alternative state | pp5–6, Table 2 p6, Fig 1B p4 |
  | Six competing steering/sampling methods at matched or larger prediction budgets (ConforMix 800, Boltz-sample 500, AFsample3 500, AFsample2 500, MSAsubsample 500) | That SteerAF's gain is a budget artefact | Table 2 p6, Figs 1B p4, S1 p34, S2 p35 |
  | Random-site restoration: restore **twice as many** randomly chosen non-curated sites that nevertheless had high MSA-feature modification | That any modified site would do — i.e. that the curated-site effect is not site-specific | p11, Fig S4 p37 |
  | Random-selection precision baseline for PGK1 functional-residue recovery: 3.4% (14/416) | That ~50% precision is what chance gives on a 416-residue protein | p11 |
  | AlphaFold2 unmodified arm inside the site-restoration figure (4th box, TM ≈ 0.71) | That the MSA-feature modification is not what moves the structure at all | Fig S4, p37 (render) |
  | hβ2AR replication of the PGK1 PSSM precision/recall analysis | That the interpretability result is a PGK1 one-off | p12, Fig 4B p13 |
  | Reference-free PCA + HDBSCAN selection run with no reference, then scored against references on 46 systems (85%, 39/46) | That the method is unusable without a solved alternative structure | p9 |

  *Not controls, recorded so they are not mistaken for them:* the Figure 3B threshold determination
  (p10) is a calibration on references; the MD arm (pp12–14) is an application; the runtime
  normalization (§5.6, p22) is a measurement procedure.

- **confidence_as_discriminator**: **Used in three distinct roles, and validated in none of them
  as a discriminator of conformational correctness.**
  1. **As a loss term** to keep the optimization in-distribution: L = (1−𝛾ᵢ)L_disto + 𝛾ᵢ L_pLDDT
     (Eq. 3, p18), "we add a pLDDT constraint to prevent the optimization from drifting away from
     the normal MSA distribution" (p18), ramped in from step K_p = 3 to 𝜆ₚ = 0.50 at step T (Eq. 7,
     p19; Table S1, p32).
  2. **As a guide for the unsupervised clustering hyperparameters** — Figure 3A caption, p10: "The
     first PCA map is colored by pLDDT **to guide the choice of appropriate HDBSCAN clustering
     parameters and the clustering itself**." This inserts a confidence signal into the one
     reference-free arm.
  3. **As a structural-quality filter on MD basins** — Figure S5 caption, p38: spurious misfolded
     basins "are nonetheless readily identified—and excluded from functional interpretation—by their
     elevated free energy, peripheral location and **abnormal pLDDT distribution** in the
     distance-PCA space".
  Figure 3D (p10) plots per-cluster pLDDT distributions, which is as close as the paper comes to
  testing the association — and it is shown for one system with no quantitative statement, no
  AUC, no separation statistic. **No validation that pLDDT distinguishes the correct conformational
  state from the wrong one is performed anywhere.** Note the direction of the confounder: the
  optimizer is explicitly *rewarded* for pLDDT, so pLDDT of SteerAF outputs is not an independent
  signal.

## D. Claims

- **central_conclusion**: SteerAF freezes AF2/OpenFold and performs block gradient *ascent* on the
  numerical MSA input feature, using a masked cross-entropy between the model's current distogram
  and the distance bins of its own step-0 default prediction, so that the prediction is driven away
  from the dominant basin and toward the secondary peaks the authors argue are already present in
  the distogram. In 420 predictions per target (60 runs × 7 steps) it matches or beats ConforMix,
  Boltz-sample, AFsample2/3, MSA subsampling and the AF2/AF3 baselines on three of four two-state
  benchmarks (69 systems), and is clearly worse on fold-switch. An unsupervised PCA + HDBSCAN
  pipeline over internal distance matrices separates both states in 39/46 systems without a
  reference. The MSA-feature modifications localise to ~50%-precision on curated functional residues
  in PGK1 and hβ2AR, and the predictions seed MD that expands sampled space >3-fold.

- **necessity_claims** (verbatim + page):
  1. p1 (abstract): "End-to-end structure predictors, such as AlphaFold2, typically output only the
     dominant conformational state of a given protein, which is biased by the training dataset."
  2. p2: "However, regression-based models (e.g. AlphaFold2 and RoseTTAFold) predominantly predict
     the single dominant conformation most frequently observed in the training data."
  3. p2: "However, most of these approaches suffer from intensive sampling and require substantial
     computational time."
  4. p2: "However, system-tailored experimental restraints are not always readily available."
  5. p14 — **the load-bearing impossibility claim about their own method**: "this loss function
     inherently cannot separate the alternative peak signals originating from different conformations."
  6. pp14–16: "AlphaFold2 was likewise not specifically trained to disentangle different possible
     signals in the distance representation, so the model's capacity during gradient backpropagation
     may also be insufficient to disentangle the mixed alternative-conformation signals, leading to a
     failure to find the correct MSA optimization direction."
  7. p14: "As a result, distogram-based gradient descent struggles to generate accurate predictions
     for fold-switch proteins."
  8. p1 (abstract): "Existing strategies for recovering alternative conformations are often
     computationally expensive and offer limited biological interpretability."

- **novelty_claims** (verbatim + page). **No claim to be *first* at anything appears anywhere in
  the paper.** The claims are of novelty-by-difference:
  1. p2: "In this study, we present SteerAF, a novel automated alternative conformation prediction
     framework based on OpenFold that leverages AlphaFold2's distogram outputs."
  2. p16: "**Since our framework operates at the MSA level to capture biologically meaningful
     modifications, which is different from contemporaneous related preprints,** and provides a
     straightforward yet effective strategy for selecting candidate alternative conformations without
     requiring experimental structures, we anticipate that it will enable an interpretable and
     self-supervised route to predict and design multi-state biomolecular systems." (The
     "contemporaneous related preprints" are refs 57 and 58 — ConforNets, arXiv:2604.18559, and
     SwitchCraft — p29.)
  3. p16: "In this work, we demonstrated that the mixture of signatures from multiple conformations
     encoded in AF2's predicted distogram can be effectively exploited by SteerAF, without updating
     the pretrained model weights or requiring large-scale sampling."
  4. p17: "**Crucially, because we optimize the interpretable MSA input rather than internal network
     representations,** the resulting sparse, site-specific modifications can be cross-validated
     against experimentally characterized functional residues—indicating that SteerAF's predictions
     are not arbitrary perturbations engineered to escape the default conformation, but instead carry
     genuine biological meaning, thereby extending a structure-prediction tool into a
     hypothesis-generating instrument that can inform experimental design."
  5. p2: "These results demonstrated that predicted contact maps and distograms derived from deep
     MSAs implicitly encode signatures of alternative conformational states, opening a route for
     predicting alternative conformations in a self-supervised manner." (Claimed for their own prior
     work, refs 34–35.)

- **stated_limits** (the authors are unusually forthcoming; §3 Discussion pp14–16 unless noted):
  1. "Despite achieving competitive performance on two-state conformational benchmarks, our method
     performs relatively poorly on the fold-switch dataset" (p14), attributed to distograms of
     fold-switch pairs differing "drastically" so that the alternative peak "may not provide
     sufficient guidance".
  2. "SteerAF also performs poorly on proteins that adopt three or more distinct conformations, such
     as multiple terminal states of domain motions, allosteric endpoints, and transporter channel
     states" — 7/18 one conformation, 7/18 two, 2/18 three or more (p14).
  3. The loss "inherently cannot separate the alternative peak signals originating from different
     conformations" (p14).
  4. "our method underperformed relative to others on only two systems: A6UVT1 and PF0708" (p16),
     with the A6UVT1 case attributed to possible training-data leakage in the *competitors*.
  5. SPF1 excluded for out-of-memory (Figure 1 caption, p4).
  6. Acceptance thresholds are system-dependent; GPCRs "may require stricter thresholds" (p9).
  7. The MdfA reference-free selection **failed**: "for which our reference-free selection strategy
     failed to identify the alternative conformation candidates because all predictions near the
     alternative conformation were classified as outliers" (p12).
  8. "We note that this free-energy estimate is rough and that the sampling has not fully converged"
     (p12).
  9. Misfolded spurious MD basins: "several of the higher-energy, peripheral basins arise from
     partially or incorrectly folded structures … These misfolded minima are a generic by-product of
     seeding MD from an aggressively diversified prediction set, which by design includes
     low-confidence, non-physical conformations" (Figure S5 caption, p38).
  10. "The curated sites listed here do not exhaustively cover all functional positions; unannotated
      residues should therefore not be treated as irrelevant" (p22) — so the precision figure has an
      unquantified false-negative floor.
  11. "The normalized runtimes reported here are intended only for relative comparison across
      methods, not as absolute runtime guarantees" (p22).
  12. Code and data are **not yet available**: "The source code and data for SteerAF, reference-free
      state selection, PSSM analysis, and MD simulations **will be available upon publication**" (p24).

- **stance**: **`threat` on scope + `contrast` on rigour. Provisional — the user's call.**
  - *threat*: this is a direct competitor occupying adjacent ground. It steers a different internal
    object than the other steering papers in the corpus — the **distogram head**, via gradient on the
    MSA input embedding, rather than the MSA content, the pair representation, or a learned latent —
    and it benchmarks against ConforMix, Boltz-sample, AFsample2/3 at matched budgets and wins on
    three of four datasets. It also stakes out the interpretability claim (functional-residue
    recovery) and the reference-free-selection claim.
  - *contrast*: on rigour it is a clean foil. It has **no directional control whatsoever** — one
    repulsive direction, no target-state handle, and the paper says the loss "inherently cannot
    separate" multiple alternatives (p14). Success is entirely reference-defined; the hyperparameter
    range and stopping step were tuned on the evaluation datasets; there is no anti-memorization arm
    at all despite the paper's own premise depending on what AF2 memorized; and **no GPCR appears in
    any of the four conformational benchmarks**.
  - A *precedent* reading also exists and should not be lost: it is the cleanest demonstration in
    the corpus that AF2's distogram carries a usable secondary-state signal *without* any structural
    input at inference. Recorded here rather than as a third stance value.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Benchmark size, domain motion | 16 | systems | Table 1, dataset from ref 20 (BioEmu, Lewis *et al.* 2025) | p5 |
  | Benchmark size, oc23 (open–close) | 23 | systems | Table 1, dataset from ref 11 (AFsample2) | p5 |
  | Benchmark size, tp16 (transmembrane) | 15 (of 16; SPF1 dropped, OOM) | systems | Table 1, dataset from ref 11 (AFsample2) | pp4–5 |
  | Benchmark size, fold switch | 15 | systems | Table 1, datasets from refs 9 and 21 | p5 |
  | Benchmark total | 69 | systems | sum of the four; all named in Fig S1 | p5, p34 |
  | Inter-state TM-score, domain motion | 0.6813 / 0.8370 / 0.5070 | TM-score (mean/max/min) | reference conformation A vs B | p5 |
  | Inter-state TM-score, oc23 | 0.5009 / 0.6450 / 0.3790 | TM-score (mean/max/min) | reference A vs B | p5 |
  | Inter-state TM-score, tp16 | 0.7892 / 0.9690 / 0.3730 | TM-score (mean/max/min) | reference A vs B — **max 0.969 means globally-similar pairs are retained** | p5 |
  | Inter-state TM-score, fold switch | 0.6672 / 0.9004 / 0.4817 | TM-score (mean/max/min) | reference A vs B | p5 |
  | Best TM-score, all methods, 4 datasets | ~0.84–0.95 band; SteerAF at or near top on domainmotion, oc23, tp16; **below Boltz-sample and AFsample3 on foldswitch** | TM-score | best-of-N prediction vs alternative reference | Fig 1B p4; per-system Fig S1 p34; per-metric Fig S2 p35. **Numeric values NOT REPORTED — plotted only** |
  | Best RMSD, all methods, 4 datasets | plotted, ~0–7 Å range | Å | best prediction vs alternative reference | Fig S2 p35. **Numeric values NOT REPORTED** |
  | Near-best run ratio, SteerAF, mean over all systems | **55.1%**, "reaching close to 100% for some systems" | fraction of runs | runs containing a prediction with TM ≥ 0.97 × TM_best | p7 |
  | Near-best run ratio vs competitors | "SteerAF achieves a higher near-best run ratio while maintaining a comparable best TM-score" | — | ConforMix, Boltz-sample, AFsample3 | p7, Fig 2A p8 |
  | Sampling saturation point | 10–20 runs ≈ 70–140 predicted structures | runs / structures | "most systems reached relatively saturated prediction performance" | p7 |
  | Reference-free selection success, SteerAF | **85% (39/46)** | systems | both conformations recovered as distinct clusters, ≥50% of a cluster each | pp3, 9 |
  | Reference-free selection, CF-random comparator | 81% (26/32) | systems | its own in-house fold-switch dataset, blind mode (ref 9) | p9 |
  | Reference-free selection, AFsample3 comparator | top-1 77%, top-10 89% | conformations (n = 238) | scored per conformation, not per protein (ref 44) | p9 |
  | AAC3_OUT cluster purity | cluster 0 captured >99% of alternative conformations; both clusters >74% pure; cluster 0 contained no default conformations | % | reference-labelled predictions | p9, Fig 3D p10 |
  | PGK1 functional-residue recovery | precision 15%–50%, recall >60% across L1 threshold 0.3–0.5 | precision / recall | 14 curated sites (Table S2) out of 416 residues | p11, Fig 4B p13 |
  | PGK1 random-selection baseline | **3.4% (14/416)** | precision | chance | p11 |
  | Abstract summary of residue recovery | "approximately 50% precision", "recall above 50%", "across two tested protein systems" | precision / recall | PGK1 + hβ2AR curated sets | pp1, 3 |
  | hβ2AR functional-residue recovery | plotted precision/recall vs L1 threshold; "far more reliable than random selection" | precision / recall | curated set, Table S3 | p12, Fig 4B p13. **Numeric values NOT REPORTED** |
  | BGA vs GA | median best TM-score **+0.009**; >0.05 better on 7 systems, clearly worse on 3 | ΔTM-score | SteerAF-GA (dense gradient) | p19, Fig S6 p39 |
  | Gradient regularization (exp / unit / norm) | "no significant difference in overall performance on the full dataset" | — | each other | p20, Figs S6 p39, S7 p40 |
  | SteerAF prediction budget | **420** = 60 runs × 7 steps; 𝜌 ∈ {10%, 5%}, lr ∈ {2e-2, 2e-3}; 10 runs at 𝜌=10%, 20 at 𝜌=5% | models per target | Table 2 | p6 |
  | Runtime, SteerAF | **1.35 (0.17–5.50)** | A800-equivalent GPU wall-clock hours per target | Table 2 | p6 |
  | Runtime, ConforMix | 2.73 (0.52–8.88) at 800 models | GPU h per target | Table 2 | p6 |
  | Runtime, Boltz-sample | 0.42 (0.09–1.28) at 500 models | GPU h per target | Table 2 | p6 |
  | Runtime, AFsample3 | 0.47 (0.11–1.30) at 500 models | GPU h per target | Table 2 | p6 |
  | Runtime, AlphaFold3 | 1.20 (0.43–3.42) at 1000 models | GPU h per target | Table 2 | p6 |
  | Runtime, AFsample2 | 3.65 (0.42–13.98) at 500 models | GPU h per target | Table 2 | p6 |
  | Runtime, MSAsubsample | 2.15 (0.22–8.27) at 500 models | GPU h per target | Table 2 | p6 |
  | Runtime, AlphaFold2 | 8.58 (1.10–28.70) at 1000 models | GPU h per target | Table 2 | p6 |
  | Multi-state failure rate (in-house set) | 7/18 one conformation, 7/18 two, 2/18 three or more | proteins | in-house 18-protein multi-conformation dataset (sums to 16, not 18) | p14 |
  | MD conformational-space expansion, MdfA | predictions 123 cells vs MD 437 cells; 356 cells new; ">threefold" | 2.0-PC grid cells | prediction ensemble vs 2.5 µs MD | pp3, 12 |
  | MD aggregate sampling | 50 seeds × 50 ns = **2.5 µs** per system; 25,050 frames | µs | MdfA and AAC3 | pp12, 24, Fig 5 p15, Fig S5 p38 |
  | Targeted-MD convergence | final RMSD **0.6–1.2 Å** to each of 50 assigned targets | Å | assigned seed structures | p12 |
  | MdfA basin RMSDs to references | B1/6VS1 1.52; B2/6VS1 1.10; B4/6GV1 1.96 | Å | deposited MdfA structures | Fig 5C, p15 |
  | AAC3 basin RMSDs to references | B1/4C9J 1.29; B2/4C9J 1.23; B4/4C9J 2.12; B5/6GCI 2.06; B6/6GCI 2.38; B7/6GCI 2.79; B8/4C9J 1.16; B3/6GCI 4.20 | Å | 4C9J (c-state), 6GCI (m-state) | Fig S5, p38 |
  | Default hyperparameters | T=6, N=10–20, K=3, thr_mask=4, K_p=3, 𝜆ₚ=0.50, 𝜌=5%, lr=2×10⁻² | — | Table S1 | p32 |
  | Recommended range for new systems | 𝜌 ≤ 20%, lr ≤ 2e-2 | — | derived from the PF0708 failure | p16 |

- **n_predictions**: **Record the three numbers separately.**
  - *Samples per target, SteerAF*: **420** structures = 60 runs × 7 predictions per run
    (T = 6 optimization steps, T+1 outputs; p18). The 60 runs = 2 learning rates × (10 runs at
    𝜌 = 10% + 20 runs at 𝜌 = 5%) — Table 2, p6.
  - *Targets*: **69** in the benchmark (plus 46 in the selection evaluation, 18 in-house, 2
    interpretability, 2 MD).
  - *Total, SteerAF*: **28,980** structures across the benchmark (420 × 69; the paper does not
    state this product).
  - *Comparator budgets per target*: ConforMix 800 (40 RMSD settings × 20 models), Boltz-sample
    500 (10 𝛽 values × 50), AFsample3 500, AFsample2 500, MSAsubsample 500 (8 depths),
    AlphaFold3 1000, AlphaFold2 1000 — Table 2, p6. **SteerAF runs at a smaller budget than every
    comparator except none — 420 is the lowest number in the table.**
  - *MD*: 50 seeds × 50 ns = 2.5 µs per system, 25,050 analysed frames, 2 systems (p12, p24).

- **comparable_to_ours**: *(left empty by the extractor per v3)*

- **si_in_scope**: **SI IS HELD (PDF pp31–42) but contains NO numeric results.** Present: Table S1
  (hyperparameter defaults, p32), Tables S2/S3 (curated PGK1 and hβ2AR residue sites with validated
  perturbations and functional roles, p33), Figures S1–S8 (pp34–41), SI reference list (p42).
  **Absent from the entire 42-page PDF: any table of per-system or per-dataset TM-score, RMSD, fill
  ratio, cluster spread or near-best run ratio.** Every one of those exists only as a plotted bar,
  point or violin, so no comparator number from this paper can be quoted to more precision than a
  figure read. The raw values are deferred to unreleased code: "The source code and data … **will be
  available upon publication**" (p24). Treat the `metrics_reported` rows marked "plotted only" as
  **SI NOT HELD** in effect.

## F. Figures

One row per panel group. Split on `mark` or `measure`, not on `facet`. Figure 3's letters A and C
each appear in two rows because a single panel letter carries two shapes; noted in `panels`.
**16 panel-group rows total** (10 main-text, 6 supplementary).

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | p4 | SteerAF workflow: query seq + input MSA → MSA feature → folding network → default conf; distogram of step-i vs default distances → loss → block gradient ascent → updated MSA feature | schematic | `SCHEMATIC \| one cyclic flow chart: MSA feature into a frozen protein-folding network, distogram loss against the step-0 default conformation, block gradient ascent back onto the MSA feature, with alternative-conf and default-conf renders as endpoints \| no data` | 1 | | **CC-BY-NC-ND 4.0** (p1 and every page header) — **ND clause: no derivatives. Redrawing as well as modifying is forbidden without permission.** |
| 1B | p4 | Best TM-score and near-best run ratio of 8 methods across the 4 benchmark datasets | bar | `PLOT \| facet: metric (2: best TM-score, near-best run ratio) \| vary: benchmark dataset (4: domainmotion, oc23, tp16, foldswitch) \| series: method (8: SteerAF, ConforMix, Boltz-sample, AFsample3, AlphaFold3, AFsample2, MSAsubsample, AlphaFold2) \| measure: best TM-score, and near-best run ratio \| mark: bar with error bar \| n: 16 / 23 / 15 / 15 systems behind each bar; 128 / 184 / 120 / 120 bars-worth per panel` | 2 (same faceting, two metrics → one row per the v3 rule) | **bars pool 15–23 systems each and hide the per-system distribution** — the per-system data exists (Fig S1) but the headline figure is bars; **TM-score y-axis pinned at 0.5–1.0**, compressing an already saturating metric into the top half; error bars are undefined (SD? SEM? CI? — not stated in the caption); n not shown on the panel | CC-BY-NC-ND 4.0, p4 header — **ND** |
| 2A | p8 | Near-best run ratio vs best TM-score, every system, 4 latest methods | scatter | `PLOT \| facet: none (1) \| vary: near-best run ratio (TM ≥ 0.97 × best), 0.0–1.0 (continuous) \| series: method (4: SteerAF-Exp, ConforMix, Boltz-sample, AFsample3) \| measure: best TM-score (0.4–1.0) \| mark: point \| n: 1 per mark (one system); 69 systems × 4 methods per panel` | 1 | **y-axis truncated at 0.4** on a 0–1 metric; the x-axis uses the *first* near-best definition, which the paper itself says is defective (p21) — a poorly-predicted target can score high on it | CC-BY-NC-ND 4.0, p8 header — **ND** |
| 2B | p8 | A800-equivalent total GPU time per target vs sequence length, 8 methods | line | `PLOT \| facet: none (1) \| vary: sequence length, 150–800 aa (continuous, log) \| series: method (8, with fitted scaling exponent b annotated: SteerAF b=1.79, ConforMix 1.40, Boltz-sample 1.38, AFsample3 1.23, AlphaFold3 token-bucketed, AFsample2 1.56, MSAsubsample 1.85, AlphaFold2 1.54) \| measure: total GPU time, A800-equivalent (min, log 10¹–10³) \| mark: line (power-law fit; AlphaFold3 a step function over 256/512/768/1024 padding buckets) \| n: 69 targets behind the fits; per-line n NOT REPORTED` | 1 | fitted lines are drawn without the underlying per-target points visible, so scatter around the fit is invisible; runtimes were measured on heterogeneous GPUs and converted by empirically estimated factors (p22) whose uncertainty is not shown | CC-BY-NC-ND 4.0, p8 header — **ND** |
| 2C | p8 | Budget–performance tradeoff: TM-score and near-best ratio as a function of optimization steps, and of number of runs | line | `PLOT \| facet: budget knob (2: cumulative optimization steps, total runs) \| vary: budget magnitude (0–10 steps / 10–40 runs, continuous) \| series: quantity (3: TM-score, near-best run ratio, near-best step ratio) \| measure: TM-score (left axis 0.8–1.0) and near-best ratio (right axis 0.0–1.0) \| mark: line \| n: aggregated over all 69 systems; per-point n NOT REPORTED` | 2, varying by which budget knob is swept; left panel metrics are cumulative over the step and all preceding steps (caption, p8) | **TM-score axis truncated at 0.8**; the two panels' independent variables differ but share axes, inviting direct comparison of a 10-step sweep with a 40-run sweep; **this is the panel the T = 6 stopping rule was chosen from, and it is measured against the held references** | CC-BY-NC-ND 4.0, p8 header — **ND** |
| 3A-i | p10 | The PCA + HDBSCAN reference-free selection pipeline | schematic | `SCHEMATIC \| step-0 through final-step predictions → common ordered-secondary-structure residue indices → per-prediction internal Cα distance matrix (N × l × l) → flatten → PCA → HDBSCAN \| no data` | 1 (letter A, shape 1 of 2) | | CC-BY-NC-ND 4.0, p10 header — **ND** |
| 3A-ii, 3C-left | p10 | The AAC3_OUT prediction cloud on the distance-PCA plane, coloured three ways: pLDDT, HDBSCAN cluster, and reference-derived ground-truth class | scatter | `PLOT \| facet: colouring (3: pLDDT, HDBSCAN cluster assignment, ground-truth class) \| vary: PC1 (80.1% variance, continuous, 0–400) \| series: pLDDT (continuous 40–100) / HDBSCAN cluster (4: Noise n=59, Cluster 0 n=13, Cluster 1 n=334, Cluster 2 n=14) / ground-truth class (5: neither, ConfB only, ConfA only, open ref, close ref) \| measure: PC2 (8.9% variance, −100 to +100) \| mark: point \| n: 1 per mark; 420 predictions + 2 references per panel` | 3 (letter A shape 2 of 2, plus the left half of letter C) | one system (AAC3_OUT) is shown to illustrate a pipeline claimed for 46; the 39/46 aggregate has **no quantitative panel anywhere** — the success rate appears only as a sentence on p9 | CC-BY-NC-ND 4.0, p10 header — **ND** |
| 3B | p10 | Justification of the TM > 0.85 / RMSD < 3.0 Å acceptance thresholds for AAC3_OUT, in four projections | scatter | `PLOT \| facet: projection (4: RMSD→6GCI vs TM→6GCI, RMSD→4C9J vs TM→4C9J, TM→4C9J vs TM→6GCI, RMSD→4C9J vs RMSD→6GCI) \| vary: TM-score or RMSD to reference (continuous, 0–1 or 0–30 Å) \| series: ground-truth class (5: neither, ConfA only, ConfB only, ConfA=6GCI marker, ConfB=4C9J marker) \| measure: RMSD (Å) and TM-score to the other reference \| mark: point, with a shaded "Acceptable region" \| n: 1 per mark; 420 predictions per panel` | 4 (same mark, compound measure → one row) | the threshold pair is set **by eye on one system** and then applied to all 69; the "Acceptable region" shading is a visual justification with no stated criterion for where its edges sit | CC-BY-NC-ND 4.0, p10 header — **ND** |
| 3C-right | p10 | The two AAC3 reference structures: 4C9J chain B (default, outward) and 6GCI chain A (alternative, inward) | structure render | `RENDER \| facet: reference conformation (2: 4C9J chain B default/outward, 6GCI chain A alternative/inward) \| views: 1 \| overlay: 0 predictions on 1 reference each \| axis: none` | 2 (letter C, shape 2 of 2) | | CC-BY-NC-ND 4.0, p10 header — **ND** |
| 3D-i | p10 | pLDDT distributions: overall, and within the best ConfA and best ConfB clusters | bar (histogram) | `PLOT \| facet: population (3: all predictions, best ConfA cluster 0, best ConfB cluster 1) \| vary: pLDDT, 50–95 (continuous, binned) \| series: ground-truth class (3: ConfA only, ConfB only, neither) \| measure: count \| mark: stacked bar (histogram) \| n: 420 overall (ConfA only n=10, ConfB only n=248, neither n=162); cluster 0 n=13 (10 + 3); cluster 1 n=334 (248 + 86)` | 3 | y-axis counts differ by an order of magnitude between the three panels with no shared scale, so the ConfA panel (n=13) reads as visually comparable to the ConfB panel (n=334) | CC-BY-NC-ND 4.0, p10 header — **ND** |
| 3D-ii | p10 | Composition of each HDBSCAN cluster by ground-truth class | bar (stacked, normalised) | `PLOT \| facet: none (1) \| vary: cluster (4: −1 noise n=59, 0 n=13, 1 n=334, 2 n=14) \| series: ground-truth class (3: ConfA only, ConfB only, neither) \| measure: fraction of cluster (0–1) \| mark: stacked bar \| n: 59 / 13 / 334 / 14 per bar; 420 per panel` | 1 | **normalising to fractions makes an n=13 cluster and an n=334 cluster the same height**; the n is printed above each bar, which partly mitigates it | CC-BY-NC-ND 4.0, p10 header — **ND** |
| 4A | p13 | PGK1: literature-validated residues (red) and PSSM-inferred sites (orange, L1 > 0.4) mapped onto the alternative (2WZD chain A, closed) and default (2XE6 chain A, open) conformations | structure render | `RENDER \| facet: conformation (2: 2WZD chain A alternative/close, 2XE6 chain A default/open) × residue class (2: literature-reported red, PSSM-inferred orange) \| views: 2 (front and 90° rotation) \| overlay: 0 predictions on 1 reference each \| axis: none` | 4 renders (2 conformations × 2 camera angles) | the site–structure correspondence is shown only as a render; the quantitative content is entirely in 4B | CC-BY-NC-ND 4.0, p13 header — **ND** |
| 4B | p13 | Precision and recall of PSSM-inferred sites against curated functional residues, as the L1 threshold varies, for PGK1 and hβ2AR | line | `PLOT \| facet: system (2: PGK1/P00558, hβ2AR) \| vary: L1-norm threshold on the per-residue PSSM difference, ~0.15–0.65 (continuous) \| series: quantity (3: recall, precision, # predicted sites) \| measure: recall/precision (left axis 0–1) and number of predicted sites (right axis, 0–400 PGK1 / 0–300 hβ2AR) \| mark: line \| n: 14 curated sites of 416 residues (PGK1); curated set size for hβ2AR NOT REPORTED in the figure (Table S3 lists 5 mutationally validated + 9 retained microswitch positions = 14, p33 and p22)` | 2, varying by system | the two panels use **different right-axis ranges** (400 vs 300) so the site-count curves are not visually comparable; the 3.4% random baseline quoted in the text is **not drawn on the panel**; no confidence interval on either curve | CC-BY-NC-ND 4.0, p13 header — **ND** |
| 5A | p15 | MdfA: 420 SteerAF predictions and the 50 selected MD seeds in distance-PCA space | scatter | `PLOT \| facet: none (1) \| vary: distance-PCA PC1, −200 to 0 (continuous) \| series: point class (2: SteerAF predictions n=420, selected seeds n=50) \| measure: distance-PCA PC2 (0–150) \| mark: point (predictions) + cross (seeds) \| n: 1 per mark; 470 marks per panel` | 1, with the Fig 5B zoom range boxed | | CC-BY-NC-ND 4.0, p15 header — **ND** |
| 5B, S5B | pp15, 38 | Two-dimensional free-energy surface from 2.5 µs of seeded MD, in the frozen prediction-derived PCA space, with basins marked | heatmap (2D KDE contour) | `MATRIX \| rows: distance-PCA PC2 (continuous, binned, −20 to +40 MdfA / −20 to +80 AAC3) \| cols: distance-PCA PC1 (continuous, binned, −60 to 0 MdfA / −50 to +50 AAC3) \| value: free energy ΔG = −k_BT ln 𝜌 (0–8 kT, colour + contour lines) \| facet: system (2: MdfA Fig 5B, AAC3 Fig S5B)` | 2 (one per system); 4 basins B1–B4 for MdfA, 18 basins B1–B18 for AAC3 | the paper states the estimate is "rough" and "has not fully converged" (p12) but the surface is drawn with quantitative kT contours and named basins anyway; **the axes are continuous PCA coordinates, not indices, which strains the v3 MATRIX form** — see `unresolved` | CC-BY-NC-ND 4.0, pp15/38 headers — **ND** |
| 5C, S5C | pp15, 38 | Representative structures at each basin, labelled with Cα RMSD to the nearest deposited reference | structure render | `RENDER \| facet: system (2: MdfA, AAC3) × basin (4 for MdfA: B1, B2, B3, B4; 8 shown for AAC3: B1–B8) \| views: 1 \| overlay: 1 MD frame on 1 reference (MdfA 6VS1/6GV1; AAC3 4C9J/6GCI) \| axis: none` | 4 + 8 renders | one frame per basin out of 25,050; how representative it is of the basin is given only as "all < 0.1 PC units" from the basin centre (p12) | CC-BY-NC-ND 4.0, pp15/38 headers — **ND** |
| S1 | p34 | Per-system, per-method grid of best TM-score and best RMSD for both conformations, all 69 systems | heatmap (grid of small multiples) | `MATRIX \| rows: system (69, grouped: DomainMotion 16, OC23 23, TP16 15, FoldSwitch 15) \| cols: method (8: SteerAF, ConforMix, Boltz-sample, AFsample3, AlphaFold3, AFsample2, MSAsubsample, AlphaFold2) \| value: best TM-score (0.6–1.0 colour scale) or best RMSD (0–6 Å colour scale); black or white circle marks the best method per conformation \| facet: metric × conformation (4: best open TM, best open RMSD, best close TM, best close RMSD)` | 4 column blocks × 69 rows | the cell values are colour-only — **this is the paper's only per-system result and it is not readable as numbers**; the RMSD colour scale tops out at 6 Å so all larger failures render identically | CC-BY-NC-ND 4.0, p34 header — **ND** |
| S2 | p35 | All five metrics for both conformations, 8 methods, across the 4 datasets | line | `PLOT \| facet: metric × conformation (10: best TM, best RMSD, fill ratio, cluster spread, near-best run ratio, each for open and close) \| vary: benchmark dataset (4: domainmotion, oc23, tp16, foldswitch) \| series: method (8) \| measure: TM-score, RMSD (Å), fill ratio, cluster spread std(TM)·std(RMSD), near-best run ratio \| mark: line connecting per-dataset aggregates \| n: 16 / 23 / 15 / 15 systems per point` | 10 (same mark, compound measure → one row) | **the aggregation statistic behind each point is never stated** (mean? median?) and no dispersion is drawn on any of the 10 panels; TM-score panels truncated at 0.5 | CC-BY-NC-ND 4.0, p35 header — **ND** |
| S3 | p36 | PGK1 PSSM at step 0, at the last near-best step, and their difference, with sequence logo, entropy and secondary-structure tracks | heatmap | `MATRIX \| rows: amino acid (20) \| cols: sequence position (416) \| value: PSSM probability, and the step-0-to-near-best difference \| facet: block (3: step-0 PSSM, last-near-best PSSM, difference), each with side tracks (sequence logo in bits, per-position entropy, secondary structure from the default-conformation experimental structure, and for the difference block a per-position count bar of how many of the 7 near-best predictions exceed L1 > 0.4)` | 3 blocks, each 4 tracks | a 20 × 416 heatmap stitched across a landscape page — individually unreadable at print size; the difference block's threshold (0.4) is the same one whose sensitivity Fig 4B sweeps, so the headline render is one arbitrary point on that sweep | CC-BY-NC-ND 4.0, p36 header — **ND** |
| S4 | p37 | PGK1 site-restoration test: TM-score to the alternative conformation after restoring curated vs random sites, against unrestored SteerAF and plain AlphaFold2 | box | `PLOT \| facet: none (1) \| vary: condition (4: SteerAF unrestored, Random mask, Validated mask, AlphaFold2) \| series: none \| measure: TM-score to the alternative conformation (0.65–1.00) \| mark: box with whiskers + overlaid strip of individual points \| n: ~60–70 points per box (visible strip); exact n NOT REPORTED` | 1 | **y-axis truncated at 0.65**, magnifying a small effect; the claimed result is only that "the median and 75th percentile of TM-score after curated-site restoration were both lower" (p11) — **no statistical test, no effect size, and the two box bodies overlap heavily**; the control set has *twice* as many sites as the curated set, which the text notes as conservative but which also means the two boxes are not matched in perturbation magnitude | CC-BY-NC-ND 4.0, p37 header — **ND** |
| S6 | p39 | Pairwise best-TM-score comparisons: BGA vs GA, and Exp vs Unit and Exp vs Norm regularization | scatter | `PLOT \| facet: comparison (3: SteerAF-BGA vs SteerAF-GA, SteerAF-Exp vs SteerAF-Unit, SteerAF-Exp vs SteerAF-Norm) \| vary: best TM-score of the comparator variant, 0.3–1.0 (continuous) \| series: conformation (2: conformation A, conformation B) \| measure: best TM-score of the reference variant (0.3–1.0) \| mark: point on an identity line, outliers labelled by system \| n: 1 per mark; 2 × 69 = 138 marks per panel` | 3, varying by comparison | only outliers are labelled, so which systems sit in the dense diagonal cloud cannot be recovered; no marginal distribution or paired test statistic on any panel | CC-BY-NC-ND 4.0, p39 header — **ND** |
| S7 | p40 | All five metrics for both conformations, three gradient-regularization schemes, across the 4 datasets | line | `PLOT \| facet: metric × conformation (10) \| vary: benchmark dataset (4) \| series: regularization scheme (3: SteerAF-Exp, SteerAF-Unit, SteerAF-Norm) \| measure: TM-score, RMSD (Å), fill ratio, cluster spread, near-best run ratio \| mark: line connecting per-dataset aggregates \| n: 16 / 23 / 15 / 15 systems per point` | 10 (same mark, compound measure → one row) | as S2: aggregation statistic unstated, no dispersion drawn; TM panels here run 0.0–1.0 while S2's run 0.5–1.0, so the two figures cannot be overlaid by eye | CC-BY-NC-ND 4.0, p40 header — **ND** |
| S8 | p41 | Hyperparameter sweep: distributions of best TM-score and best RMSD over all systems, for 3 learning rates × 4 pLDDT-loss weights | violin | `PLOT \| facet: learning rate (3: 5e-2, 2e-2, 2e-3) × pLDDT loss weight 𝜆ₚ (4: 0.33, 0.50, 0.67, 0.80) \| vary: setting (1 per panel, categorical) \| series: quantity (2: TM-score on the left axis, RMSD on the right inverted axis) \| measure: best TM-score (0.5–1.0) and best RMSD (0–10 Å, inverted) \| mark: violin with median line \| n: per caption "all datasets"; the text says the sweep was run on OC23_TP16 + fold-switch (53 systems) — **the two disagree** (see unresolved)` | 12 (3 × 4 grid) | **both axes truncated** (TM at 0.5, RMSD at 10 Å inverted) and the two violins are overlaid on different scales, so their apparent overlap is an artefact of axis choice; all 12 panels look near-identical, which is the paper's own conclusion ("no strong monotonic trend") but is also what an axis-compressed saturating metric looks like; **this is the panel from which the recommended defaults were chosen, and it was computed on the evaluation datasets** | CC-BY-NC-ND 4.0, p41 header — **ND** |

**reuse, general:** every page of this PDF, main text and SI alike, carries **"made available under a
CC-BY-NC-ND 4.0 International license"** (p1 header, and identically on pp2–42). The **ND (no
derivatives) clause forbids redrawing as well as reproducing** any panel; the **NC clause** additionally
restricts commercial use. Do not adapt, re-plot or trace any SteerAF figure for the manuscript without
written permission from the authors. Citing the numbers is unaffected.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5)
- **schema_version**: v3
- **confidence**: **high** for identity, scope, the loss and algorithm (Algorithms 1–2 and Equations
  3–7 are fully specified in the PDF), the source of the steering signal, `directional_control`,
  all seven `oracle_leakage` routes, the hyperparameter provenance, the control-arm table, and the
  absence of GPCRs from the four benchmarks (every system is named in Figure S1, p34, and was read
  system by system). **Medium** for figure rows filled from captions alone — Figures 2, 3, 5, S1, S2,
  S3, S5, S6, S7 were not rendered, so per-panel series counts and axis limits there are read from the
  text layer, which scrambles multi-column figure text; pages **4, 37, 41** were rendered at 150 dpi
  and are high confidence. **Low** for any numeric value in `metrics_reported` marked "plotted only" —
  there is no results table in this paper at all, so those are figure reads or absent.
- **unresolved**:
  1. **No GPCR appears in any of the four conformational benchmarks — stated explicitly as asked.**
     The benchmark is described in Table 1 on **p5** (16 domain motion, 23 oc23, 15 tp16, 15
     fold switch) and every one of the 69 systems is named in **Figure S1, p34**. The domain-motion
     and oc23 sets are UniProt-identified soluble proteins; the tp16 set is entirely transporters
     (AAC3_OUT, MDFA, MELB, MFSD2A_OUT, MURJ, PTSG, SLC1A1_OUT, SLC39, WLAB_OUT, TM_0287,
     TT_C0976, CYME_CMD148C_OUT, A5U30_003247, PF0708); the fold-switch set is PDB-pair identified.
     **hβ2AR (P07550) is not among them.** The only GPCR in the paper appears on **p12**, in the
     residue-interpretability analysis: "As a supplement, we performed a similar analysis on the
     hβ2AR receptor and plotted the relationship between selection threshold, precision, and recall
     in the same format as PGK1". SteerAF must have been *run* on hβ2AR to produce near-best runs
     for that analysis, but **no TM-score, RMSD, fill ratio, near-best ratio or reference PDB is
     reported for it anywhere**, and it is absent from Figures 1B, S1 and S2. The paper's only other
     GPCR statement is a caveat that GPCR states "may require stricter thresholds" than the 0.85/3.0 Å
     pair it uses (p9). **Conclusion: SteerAF has no reported conformational accuracy on any GPCR.**
  2. **Benchmark provenance vs the Cfold/AFsample families.** oc23 and tp16 are taken from ref 11
     (Kalakoti & Wallner, **AFsample2**) — Table 1 superscripts, p5 — so this benchmark **does**
     overlap the AFsample family. The fold-switch set is from refs 9 and 21 (Lee *et al.* 2025
     sequence-association / CF-random, and ConforMix). Domain motion is from ref 20 (BioEmu).
     **Cfold is never mentioned in this paper**, so no Cfold overlap can be asserted or excluded.
  3. **This benchmark does NOT exclude globally-similar two-state pairs.** Table 1 (p5) gives tp16
     a maximum inter-state TM-score of **0.9690** and fold-switch a maximum of 0.9004 — pairs whose
     two states are nearly identical globally are retained. Any comparison against a benchmark family
     that excludes such pairs by construction is therefore not like-for-like, and SteerAF's tp16
     numbers in particular are inflated relative to such a benchmark. The per-system inter-state
     TM-scores that would let this be quantified are not given.
  4. **The multi-state failure counts do not sum.** p14: "7/18 proteins yielded only one predicted
     conformation, 7/18 proteins yielded two, and 2/18 proteins yielded three or more" — 7 + 7 + 2 = 16,
     not 18. Two proteins are unaccounted for. The in-house 18-protein dataset is never named,
     listed, or included in the SI, so this cannot be checked.
  5. **Figure S8's caption and the §5.5 text disagree on what was swept.** The figure title (p41)
     reads "hyperparms tuning (**all datasets**)"; the text (p21) reads "all combinations of learning
     rate and pLDDT loss weight were evaluated on the **OC23_TP16 and fold-switch datasets**" (53 of
     69 systems). Either way the sweep ran on evaluation data, so the route-4 finding is unaffected,
     but the n behind each violin is indeterminate.
  6. **The sample ratio 𝜌 has two different "defaults".** Table S1 (p32) gives 𝜌 = 5%; Table 2 (p6)
     runs 𝜌 ∈ {10%, 5%} in the benchmark; §5.5 (p22) recommends 𝜌 ∈ {5%, 10%}; p16 recommends
     𝜌 ≤ 20% for new systems. Any citation of "SteerAF's sample ratio" must say which.
  7. **The near-best run ratio is reported under two incompatible definitions and the paper mixes
     them.** Eq. 10 (TM ≥ 0.97 × best) is used in Figure 2 only; Eq. 11 (adds TM > 0.85) is used
     "elsewhere" (p21). The headline 55.1% (p7) sits in the Figure 2 discussion, so it is presumably
     the *weaker* first definition — but the paper does not say so explicitly. Do not quote 55.1%
     without that caveat.
  8. **Error bars in Figure 1B are undefined.** The caption (p4) does not say whether they are SD,
     SEM or a CI, and no methods section defines them.
  9. **The aggregation statistic in Figures S2 and S7 is never stated** — each point is one number
     per method per dataset over 15–23 systems, with no mean/median declared and no dispersion drawn.
  10. **Code and data are unavailable**: "will be available upon publication" (p24). The raw
      per-target numbers, the GPU conversion factors, and the in-house 18-protein dataset are all
      inside that unreleased release.
  11. **Whether SteerAF was ever run with templates on is untested.** Templates are simply disabled
      (p17); there is no arm testing whether the distogram's alternative peak survives template
      conditioning. This matters for anyone applying it to a system with a solved partner state.
  12. **No deposition dates for 68 of 69 systems.** Only A6UVT1's is given (p16). The memorization
      confound cannot be assessed for the benchmark, which is a real gap given the paper's premise is
      that AF2 already knows both states.
  13. **hβ2AR curated set size is ambiguous.** Table S3 (p33) lists 5 mutationally validated sites
      (D130, E268, L272, F282, C285); p22 adds "I121, R131, Y132, P211, W286, N318, N322, P323, and
      Y326" as retained microswitch positions (9 more, total 14), and p23 discusses N318 separately.
      The denominator used for the hβ2AR precision curve in Figure 4B is not stated.

  **Tag vocabulary gaps encountered (needed but not in the fixed v3 list — NOT invented, recorded
  here as the schema requires):**
  - **A control tag for "steered away from the model's own default, with no target-state handle".**
    The v3 Control block is `directed-state` / `partner-driven` / `ligand-driven` / `peptide-driven` /
    `g-protein-mimetic` / `nanobody` / `apo-sampling` / `seed-only`. **None of them describes this
    paper's actual control mechanism**, which is a repulsive gradient with no destination.
    `directed-state` would be actively false (there is no state to direct to); `seed-only` is false
    (it is not seeds); `apo-sampling` is false (nothing is framed as apo). I left the Control block
    **empty**, which means a reverse lookup for "how was the state controlled" will return this paper
    with no answer — exactly the drift the tag list exists to prevent. **Suggest `repulsive-steering`
    or `undirected-diversification`.** This is the corpus's clearest case of a method that steers
    without direction, and it currently has no tag.
  - **A protocol tag for "templates off, full MSA on".** v3 has `no-template-no-msa` and
    `templates-on` but nothing for this very common regime (p17: templates explicitly not used, deep
    MSA fully used). Suggest `templates-off`. *(Noted as also requested by the `lee2026confornets`
    extractor — two independent hits now.)*
  - **A rigour tag for "hyperparameters or sweep ranges tuned on the evaluation set".** v3 folds this
    into `oracle-leak`, which then reads identically to a paper that fed a deposited target-state
    structure into the model. Those are very different sins and this paper is a clean example of the
    milder one having occurred **while route 1 stayed clean**. Suggest `tuned-on-eval`.
  - **A method tag for "gradient-based hallucination / inverse optimization on the input embedding".**
    `latent-steering` is the correct v3 tag per its own definition ("distogram head" is named in it)
    and is applied, but it flattens a real distinction: this paper explicitly contrasts itself with
    latent methods — p9: "A key design choice in SteerAF is to optimize the **MSA input feature
    rather than intermediate network representations**", repeated p17. A future query for "which
    papers manipulated an internal representation" will return this paper alongside ConforNets and
    pair-representation scaling, when SteerAF's own novelty claim is that it did *not*. Suggest
    `input-hallucination` as a sibling of `latent-steering`.

  **v3 schema ambiguities hit while extracting (blunt, as asked):**
  - **A 2D free-energy surface over two continuous PCA coordinates fits neither PLOT nor MATRIX
    cleanly.** Figures 5B and S5B have two continuous independent coordinates and a colour-encoded
    measure. PLOT has one `vary` slot; MATRIX is specified for axes that "are indices". I used MATRIX
    with continuous binned rows/cols and flagged it. A future extractor will plausibly choose PLOT and
    the join will break. *(Independently reported by the `lee2026confornets` extractor for the same
    class of figure — this is now a two-extractor defect and by the changelog's own standard should
    be fixed. Suggest either explicitly allowing continuous ranges in MATRIX `rows`/`cols`, or adding
    a FIELD/LANDSCAPE form.)*
  - **The panel-split rule covers `mark` and `measure` but is silent on a differing `vary`.**
    Figure 2C has two panels with the same mark (line) and the same measures (TM-score, near-best
    ratio) but *different independent variables* (optimization steps vs number of runs). Under the
    literal rule they are one row, but then `vary` has to hold two incompatible variables. I put the
    panel split in `facet:` and wrote a compound `vary:`, which is a workaround, not a rule. **Suggest
    the rule become: split on `mark`, `measure`, or `vary`.**
  - **`n:` has no form for "best-of-N per target, aggregated over targets".** Every headline metric
    here is a best-of-420 statistic summarised across 15–23 systems, so a bar's `n` is simultaneously
    420 (per system) and 15–23 (per mark). I wrote both, but the `1 of 5 (pLDDT-selected)` worked
    example does not cover best-of-B, which is the dominant metric shape in this entire literature.
    *(Also independently reported by the `lee2026confornets` extractor.)*
  - **`method_class` has no entry for inference-time tensor optimization** even though the v3 tag
    list gained `latent-steering`. I wrote `other` plus a description. The B-table list and the tag
    list have drifted apart and should be reconciled.
  - **`metric_saturation` says "numeric saturation only" but gives no guidance for a metric whose
    saturation comes from the *benchmark's* construction rather than the metric's bounds.** tp16's
    max inter-state TM of 0.969 means the metric is near-saturated *for that pair* before any
    prediction is made. I recorded it here since it is numeric, and cross-referenced the axis
    truncations to `hides` as instructed, but the schema does not say where benchmark-induced
    saturation belongs.
  - **`anti_memorization_design` has no way to express "one incidental system, observed post hoc,
    used to explain a competitor's success rather than to test our own".** `NONE` understates it and
    a bare n=1 overstates it. I wrote both plus the quote.
- **why_it_matters**: *(left empty by the extractor per v3 — the user's call)*

## Tags

`transporter` `fold-switching` `general-protein` `gpcr`
`latent-steering` `md`
`templates-on`
`ensemble` `two-state`
`continuous-metric` `binary-predicate` `saturating-metric`
`oracle-leak` `design-level-oracle` `no-anti-memorization` `multi-backbone`
`preprint`
`threat` `contrast`
`comparator-numbers`

**Tag notes, because three of these are borderline and a reverse lookup will otherwise mislead:**
- **`gpcr` is applied with a strong caveat.** No GPCR is in any of the four conformational
  benchmarks (see `unresolved` 1). hβ2AR appears only in the residue-interpretability analysis
  (p12, Fig 4B p13, Table S3 p33) with **no conformational accuracy metric of any kind**. A query
  for "GPCR conformational-state prediction results" will hit this paper and find nothing. Applied
  so the hβ2AR functional-residue analysis is findable; drop it if the tag is meant to imply
  conformational evaluation.
- **`templates-on` is applied in its negated sense and is therefore WRONG as written, but v3 has no
  alternative.** The paper runs **templates OFF** (p17, verbatim quote in `templates`). v3 offers
  only `no-template-no-msa` (false — the MSA is full and deep) and `templates-on` (false). I have
  applied `templates-on` **only because leaving the protocol untagged is worse**, and flag it here
  as the single most misleading tag in this note. **Whoever holds the vocabulary should add
  `templates-off` and re-tag this paper.** *(See tag-gap list above.)*
- **`md` is applied for a real MD arm**, not a comparator: 2.5 µs aggregate per system on MdfA and
  AAC3, CHARMM36m/POPC, GROMACS 2025.4, with targeted-MD relay seeding (pp12, 23–24, Figs 5 p15 and
  S5 p38). SteerAF itself is not an MD method.
- **`multi-backbone`** is applied to the *benchmark* (AF2/OpenFold, AF3 and Boltz-2 compared head to
  head, Table 2 p6), not to SteerAF, which is AF2-only.
- **No Control-block tag is applied at all**, deliberately — see the tag-gap list. This paper has no
  directional handle to name.
- **`no-anti-memorization`** rather than `anti-memorization`: no held-out or post-cutoff set exists
  and no control arm was run (see C).
- **`unpowered`** was considered and **not** applied: the 69-system benchmark is well powered. The
  n=1 anti-memorization observation is unpowered, but that is recorded in
  `anti_memorization_control` rather than by a tag that would be read as applying to the benchmark.
- **`experimental-validation`** was considered and **not** applied: the PGK1/hβ2AR residue analysis
  compares against *previously published* mutagenesis (Tables S2–S3, p33), it does not run any new
  experiment. No wet-lab work was performed for this paper.
