# jung2026boltzperturb

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–28)**, which coincide with the
printed page numbers. Structure: p1–p9 main text (Abstract, 1. Introduction, 2. Related work,
3. Methods, 4. Experiments, 5. Results, 6. Discussion, 7. Acknowledgements, 8. Data and Code
Availability), p9–p11 references, p12–p28 Supplemental Information (A. Background, B. Methods,
C. Metric Definitions, D. Additional Results and Discussion). Main figures 1–5 on p2, p6, p7, p8,
p9. Main tables 1–2 on p6, p7. SI figures S1–S10 on p17, p18, p19, p20, p21, p24, p25, p26, p27,
p28. SI tables S1–S4 on p17, p18, p21, p22.

**Reading caveat, recorded up front because it governs sections C and E.** This paper has two
distinct evidential layers and conflating them is the easiest way to mis-cite it:

| | Layer 1 — the diagnostic argument | Layer 2 — the method result |
|---|---|---|
| what is done | the deposited ligand coordinates are **injected into the reverse-diffusion trajectory** once, then denoising continues | Gaussian noise is injected into the denoising module's conditioning tensors; no structural information enters |
| set | diagnostic five (n=5), post-cutoff | diagnostic five (n=5) + 57 RnP targets |
| uses the answer? | **yes, by construction** — this is the point of the experiment | **no** at inference; **yes** at configuration-selection and at scoring |
| what it is offered as | evidence that correct binding-mode basins pre-exist in the learned landscape | evidence that perturbation reaches them without the answer |
| section / figure | §4.1 p5, §B.4 p15, Figure S1 p17 | §5 pp.6–8, Tables 1–2, Figures 2–5 |

The manuscript-relevant claim ("failure is sampling, not knowledge") is carried by Layer 1. Layer 2
is the non-circular half of the argument and is scored entirely by oracle best-of-N against the same
deposited structures.

---

## A. Identity

- **citekey**: `jung2026boltzperturb`
- **doi**: **10.64898/2026.08.05.742877** (bioRxiv). p1 banner: "bioRxiv preprint doi:
  https://doi.org/10.64898/2026.08.05.742877; this version posted August 5, 2026." Matches
  `refs.bib`. No journal DOI exists in the PDF.
- **year**: **2026** — p1, posted August 5, 2026.
- **venue**: **bioRxiv preprint, not peer reviewed.** p1 banner: "this version posted August 5, 2026.
  The copyright holder for this preprint (which was not certified by peer review) is the
  author/funder". Typeset in the ICML/JMLR two-column style (numbered `Algorithm 1/2/S1` blocks,
  "Abstract" head, appendix lettering), but **no conference or journal is named anywhere in the
  PDF**. Tagged `preprint`.
- **title**: Boltz-Perturb: Improving Diversity and Accuracy in Protein-Ligand Co-Folding through
  Training-Free Conditioning Perturbation — p1
- **authors**: Hyeyun Jung, BoRam Lee, Alan C. Cheng — p1. Jung and Lee marked equal contribution.
  Single affiliation: Merck & Co., Inc., South San Francisco, CA, USA (p1). Funding, p9: "This
  research was fully funded by Merck Sharp & Dohme LLC, a subsidiary of Merck & Co., Inc., Rahway,
  NJ, USA." This is an **industry pharma methods paper**, not an academic benchmark group.

## B. Scope

- **system**: **general protein.** Protein–ligand complexes with no family restriction. Selection
  criteria are structural/technical, not biological: "(1) single protein chain and (2) single
  non-covalent ligand" (p15, §B.2) and "single-chain, single-ligand complexes deposited after the
  Boltz-2 training cutoff" (p5). No GPCR, kinase or transporter stratification anywhere. The
  stratification axis they do use is training-set similarity (SuCOS-pocket), not protein family
  (Figure 3, p7).

- **n_targets**: **62 protein–ligand complexes, in two disjoint sets.**

  | Set | n | how defined | page |
  |---|---|---|---|
  | Diagnostic five | 5 (9JF4, 9M4Q, 9PY4, 9RAY, 9Z1L) | PDB depositions after the RnP curation date **and** the Boltz-2 training cutoff; single chain, single non-covalent ligand | p5, p15 |
  | Curated Runs N' Poses (RnP) subset | 57 | RnP systems with a single protein chain and single ligand, released after the Boltz-2 training cutoff, **and** where "the RnP reported the best Boltz-2 predicted ligand RMSD exceeded 2Å" | p5, p15 |
  | **combined** | **62** | p7: "Across the combined 62-target evaluation" | p7 |

  The 57 are a **failure-conditioned** subset by construction (see `oracle_leakage` route 7). The
  RnP benchmark's own full size is never given in this PDF.

- **method_class**: **co-folding + other (inference-time conditioning perturbation / latent
  steering).** Training-free noise injection into the denoising module's single (`s_t`) and pairwise
  (`z_t` → attention bias `B`) conditioning tensors during reverse diffusion. p2: "we present
  Boltz-Perturb, a training-free perturbation framework that injects time-annealed noise into these
  conditioning signals during inference". Explicitly **not** MSA manipulation and **not**
  coordinate-level steering — p3: "unlike MSA perturbation methods, we intervene directly in the
  latent representation of the denoising module, leaving the input pipeline unchanged."

- **backbones**: **Boltz-2 only.** p5, p15. `Boltz-2x` (the steering-potential variant, `use
  potentials` flag) is the same backbone with a different inference flag, not a second model. The
  paper claims transferability without testing it — p12: "We evaluate on Boltz models, but the
  perturbation targets exist in all AF3-style architectures." **Not** tagged `multi-backbone`.

- **templates**: **NOT REPORTED.** Figure 1 (p2) draws a "Template Module" in the trunk and §A.1
  (p12) describes the AF3-style trunk generically, but **the protocol never states whether templates
  were supplied, enabled or disabled** in any arm. §B.3 (p15) says only "Boltz-2 with default
  parameters: 3 random seeds, 2 sampling temperatures, and 30 diffusion samples per
  seed-temperature combination". No template input is described for any run.

- **msa_handling**: **full (all method arms) + masked and subsampled (baseline arms only).** The
  Boltz-Perturb runs leave the input pipeline untouched (p3), so MSAs are whatever Boltz-2 default
  produces — depth and source never stated. Two baselines deliberately degrade the MSA (p15, §B.3):
  "MSA masking (V mask). 60 samples. Random masking of MSA columns at rate 0.1." and "MSA
  subsampling (V sub). 60 samples. MSA depth reduced to 4086 rows." Both are **depth/coverage
  reduction**, not state substitution: **no state-filtered or state-specific alignment is used
  anywhere in this paper.**

## C. Conformational core

- **states_generated**: **ensemble + single-state.** Dual, and the duality is the paper's actual
  finding.
  - *single-state*: default Boltz-2 collapses. p5: "Vanilla Boltz-2 sampling produced a low
    diversity of structures, with ligand RMSF remaining below 2.3 Å in all cases and below 0.5 Å in
    two cases (Figures S1 and S2)." Table 1 (p6) shows all five baseline variants on 9Z1L landing
    within 0.02 Å of each other (7.195–7.214 Å) — 180–270 samples across 3 seeds and multiple
    temperatures producing effectively one answer.
  - *ensemble*: perturbation produces a genuinely broader distribution. Ligand RMSF with protein
    context rises from 2.382 ± 2.613 Å (V) to 7.666 ± 4.241 Å (TCP-C11), Table 2 p7.
  These are **ligand binding modes within a pocket**, not protein conformational states. No protein
  backbone state is scored anywhere.

- **structural_priors_used**:
  1. **Deposited coordinates are the injected signal in the diagnostic experiment.** p15, §B.4: "We
     prepared a structure coordinate file from the PDB as a NumPy array." This is a design-time use
     of a solved structure to run a diagnostic, and is legitimate as such.
  2. **Both evaluation sets are defined by the existence of a deposited reference.** Diagnostic five
     and the RnP subset are chosen from the PDB precisely so that a ground-truth ligand pose exists
     to measure RMSD against (p5, p15).
  3. **The RnP subset is defined by prior knowledge of Boltz-2's failure against those references**
     — p15: "we retained only PDBs in which the RnP reported the best Boltz-2 predicted ligand RMSD
     exceeded 2Å, ensuring that our evaluation focused on cases where Boltz-2 did not already
     produce an accurate ligand pose." Stated openly and with a defensible reason.
  4. **SuCOS-pocket similarity to training-set structures** is used to stratify results (Figure 3,
     p7), which requires knowing the training-set pockets.
  5. **No** state-annotated database (GPCRdb / KLIFS / Kincore), **no** template, **no** structural
     restraint, and **no** fine-tuning on known binding modes are used. Fine-tuning is explicitly
     named as the alternative they did *not* take — p14, §A.4: fine-tuning "requires target-specific
     retraining and known reference structures."

- **oracle_leakage**: **PRESENT on routes 1 (diagnostic route only), 4, 5, 6 and 7; NONE FOUND on
  routes 2 and 3.** Route by route:

  **Route 1 — structures used as input or template.**
  **PRESENT, but confined to the diagnostic experiment; NONE FOUND in the headline TBP/TCP results.**
  The true-coordinate injection route feeds the answer directly into the sampler:
  > "At an intermediate denoising step, we replaced the predicted coordinates with the experimental
  > ground truth a single time, and then continued standard reverse diffusion to completion." — p5
  > "We prepared a structure coordinate file from the PDB as a NumPy array. During the denoising
  > process, if the noise variance was lower than a set threshold, we replaced the coordinates with
  > the prepared PDB coordinates once. Denoising then continued following the default noise
  > schedules." — p15, §B.4

  This is **by construction**, is labelled as a diagnostic, and its results (Figure S1, p17) are
  reported separately from every accuracy number in Tables 1 and 2. It is a legitimate diagnostic,
  not a defect — but the claim it supports is the one our manuscript must engage, so it must not be
  read as an unsupervised result.

  For the TBP/TCP arms themselves: **NONE FOUND.** The injected quantity is Gaussian noise scaled by
  the local std of the conditioning tensor — Algorithm 2, p4: "X̃ ← X + λ · σ_local · ϵ ⊙ M" with
  "ϵ ∼ N(0, I)". No structural information enters. Protocol: pp.3–5 (§3.1–3.3), p15 (§B.1, Algorithm
  S1). Confirmed by p14, §A.4: "our method does not optimize toward a specific objective function.
  Instead, it injects stochastic noise into the conditioning representations".

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates
  or alignments.** **NONE FOUND.** No annotation database of any kind is used. Data sources are
  exhaustively listed on p9, §8: "Runs N' Poses (RnP) is available from Zenodo ... and the five
  diagnostic structures (9JF4, 9M4Q, 9PY4, 9RAY, 9Z1L) are available from RCSB". Protocol described
  on p5 (§4.2 Benchmarks) and p15 (§B.2).

  **Route 3 — cluster labels derived from known states.** **NONE FOUND.** No clustering step exists
  in the pipeline. Algorithm S1 (p14) is the complete inference loop and contains no clustering;
  metric definitions (p16, §C) contain no cluster assignment. RMSF is computed over all samples
  without partitioning (p16).

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.**
  **PRESENT, and this is the most consequential pipeline leak.** Three separate mechanisms:
  - *Per-target selection of the noise scale against ground truth, on the diagnostic five.* Table S2
    caption, p18:
    > "Table S2. Minimum ligand RMSD (Å) per method across all 5 PDB targets (best over all noise
    > scales). TBP/TCP values shown as RMSD (ns)."

    The reported `ns` differs per target within the same method row (e.g. TBP-C4: ns=1.0 for 9JF4,
    9.0 for 9M4Q, 11.0 for 9PY4, 25.0 for 9RAY, 12.0 for 9Z1L). The noise scale is therefore chosen
    per target by minimising RMSD to the deposited structure. Table 1 (p6) is the same data.
  - *The sweep range itself was tuned on the evaluation sets.* Table S1 (p17) lists σ_max ∈
    {0.5, 1.0, 1.5, 2.0} for both methods, but the reported runs use σ up to 25.0 (Table 2, p7;
    Table S2, p18) and Figure S3 (p19) sweeps "TBP large-scale (σ ∈ [0, 25])". The grid was
    evidently extended after seeing results on the same targets that are then reported as the
    result. Under v3 this counts as leakage even though no single value is fixed per target.
  - *Configuration carried forward to RnP was selected on the diagnostic five, and the RnP table
    itself reports a grid over the evaluation set.* Table 2 (p7) reports 8 TBP configurations and 1
    TCP configuration across the same 57 targets, and the headline pair (TBP-C5 s=12.0; TCP-C11
    s=0.9) is the best of them. Figure 4 (p8) then presents that pair as "the perturbation methods".
  - Partial mitigation, recorded fairly: **TADS-Auto exists precisely to remove this**. p4: "We
    further introduce TADS-Auto for noise scheduling (Algorithm 1) to reduce reliance on manual
    hyperparameter tuning", calibrating from "ν_t, the standard deviation of the noise being added
    at step t" — the model's own quantity, not the reference. p9: "TADS-Auto showed promising
    results for TBP configurations ... While not always optimal, it provides a good starting point
    when the appropriate perturbation schedule is unknown." TADS-Auto still leaves σ_max free. The
    tail-end window [0.0, 0.25] was chosen from a model-internal observation, not from RMSD — p17:
    "The tail-end window was selected based on the empirical observation that, in the 200-step
    diffusion process, the stochastic noise variance effectively vanishes around step 154."

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.** **PRESENT, and it is
  the primary reported metric, openly labelled "oracle".**
  > "SR_O: oracle success rate (best-case over all poses per target)." — p7, Table 2 notation
  > "Success rate (SR) Fraction of unique test systems, where the minimum ligand RMSD from
  > openstructure is lower than 2Å" — p16, §C
  > "success rate (fraction of targets with ≥1 pose below 2 Å RMSD)" — p5

  The 2 Å threshold is never justified in the text. Mitigation, recorded fairly: they report a
  **non-oracle counterpart alongside it** — SR20, the confidence-ranked top-20 success rate (p7,
  p8, Figure 4, Figure S8) — and the headline abstract number is that non-oracle one ("TCP improves
  top-20 oracle success rates by 2.6 to 7.8 fold", p1). §D.7 (p23) is an explicit argument that the
  gain survives without ground truth.

  **Route 6 — best/worst model labels assigned against a held reference.** **PRESENT throughout.**
  > "Table 1. Minimum ligand RMSD (Å) per structure across baseline and perturbation methods." — p6
  > "W_<2 / W_all: win count — number of targets (out of 57) where this method achieves the lowest
  > min-RMSD across all methods" — p7
  > "Figure 2. Comparison of the lowest RMSD structures identified in Table1." — p6

  Every structure rendered in Figure 2 is the reference-selected best of 60–180 poses. The union
  arms in Figure 3 (TBP∪TCP = 21/57, TBP∪TCP∪V = 22/57, p7) are a further best-of-methods oracle on
  top of the best-of-poses oracle.

  **Route 7 — design-level oracle use (input conditions or systems chosen because the expected
  answer is already known).** **PRESENT — and this is design-level, weaker than pipeline leakage,
  and must be labelled as such.** Two instances:
  > "We then retained only PDBs in which the RnP reported the best Boltz-2 predicted ligand RMSD
  > exceeded 2Å, ensuring that our evaluation focused on cases where Boltz-2 did not already produce
  > an accurate ligand pose." — p15, §B.2

  The 57-target evaluation set is selected **by prior knowledge of the reference-measured failure of
  the very baseline it is compared against**, which floors the V baseline near its worst case. The
  authors state the reason plainly and it is a defensible design for a rescue method; it does mean
  the reported V oracle SR of 19.30% is not a general Boltz-2 success rate.

  Second instance: the true-coordinate injection experiment declares the expected answer before
  reading the result — the correct pose is both the injected input and the success criterion (p5,
  p15). Recorded here as design-level because the experiment is a diagnostic, not a prediction.

  **Summary verdict.** The **headline TBP/TCP predictions are clean of structural input** — noise
  only, no reference coordinates, no templates, no state-annotated alignments. Leakage enters at
  **configuration selection** (route 4), at **scoring** (routes 5, 6), and at **set construction**
  (route 7). The **diagnostic argument** (route 1) uses the answer by construction and is labelled
  as such by the authors. Tag both `oracle-leak` and `design-level-oracle`.

- **prospective**: **no.** Every target is a deposited PDB entry used as ground truth; the primary
  metric is oracle best-of-N RMSD to that entry (p7, p16); configuration and noise scale were chosen
  against it (p18); and the RnP set was constructed from known baseline failure (p15). It is
  **anti-memorization by design** (all targets post-date the Boltz-2 training cutoff, p5, p15), and
  it is **retrospective in evaluation and in tuning**. No blind or held-out prediction is made.

- **state_metric**: **RMSD-to-reference + binary predicate.** Dual.
  - *Continuous*: ligand RMSD to the deposited ligand after alignment, formula given p16, §C.1;
    reported as per-target minimum (Tables 1, 2, S2) and as a distribution (Figures S6–S10).
  - *Binary*: "success ⇔ at least one pose <2 Å per target" (p7). Also expressed as "Fraction of
    unique test systems, where the minimum ligand RMSD from openstructure is lower than 2Å" (p16).
  - **Threshold: 2 Å. Justification: NOT REPORTED** — the value is used on p5, p7, p8, p16, p23 and
    is never argued for anywhere in the paper.
  - Secondary metrics: ligand RMSF with and without protein context (diversity, formulas p16, §C.2),
    Boltz-2 confidence score and ligand ipTM (reliability), PoseBusters v0.6.5 + OpenStructure v2.7.0
    validity (p16). PoseBusters checks enumerated on p16: "bond lengths, bond angles, internal
    clashes, protein–ligand clashes, volume overlap."
  - Figure 2 (p6) is a visual overlay but the state/pose is **not** called by eye — every render
    carries its RMSD. Not `visual-metric`.

- **metric_saturation**: **YES — two numeric floors and one ceiling.**
  1. **The 2 Å binary success predicate floors at zero for the majority of the RnP set under every
     method.** p23, §D.7: "we ... kept only targets with at least one correct pose (ligand RMSD
     <2Å) when combining all predictions. This yielded 23 out of 57 targets." So 34/57 targets score
     0 under all 14 methods pooled; no method can be distinguished on them. Figure S8 caption, p26,
     states the consequence directly: "Since most targets have zero predictions below 2 Å, the mean
     flattens."
  2. **Mean per-target minimum ligand RMSD is insensitive across all arms.** Table 2, p7: every
     method lies between 9.32 and 10.17 Å with σ ≈ 7 Å, and the best oracle-SR method (TCP-C11,
     10.457 ± 6.575 Å) is *worse* on this metric than vanilla (9.604 ± 7.025 Å). The metric that
     moves and the metric that does not disagree in sign.
  3. **PoseBusters validity ceilings for all baselines** at 97.85–98.79% (Table 2, p7) and at
     99–100% on the diagnostic five (Figure S3a, p19), so validity cannot discriminate baselines.
  Axis truncations and irregular axes are recorded in `hides` on the figure rows (S4A, S5, S3B-D,
  S4B-D, S6, S7), not here.

- **directional_control**: **NO — the method broadens the distribution and cannot be aimed.** This is
  stated by the authors as a design property, twice, verbatim:
  > "while coordinate-level methods such as Boltz-steering and ConforMix optimize toward specific
  > physical objectives or bias away from reference structures, we apply stochastic perturbation for
  > broader conformational exploration without any predefined goal." — p3
  > "In contrast, our method does not optimize toward a specific objective function. Instead, it
  > injects stochastic noise into the conditioning representations—pair bias and single-token
  > modulation—within the DiffusionTransformer, encouraging exploration of alternative denoising
  > trajectories without requiring target-state supervision. This places our approach closer to
  > stochastic perturbation guidance than to directed optimization: rather than steering the model
  > toward a predefined state, we broaden the distribution of sampled conformations by perturbing
  > the conditioning signals." — p14, §A.4

  **Handles that exist, all non-directional**: noise scale σ_max; injection window (full trajectory
  t∈[0,1], mid-range t∈[0.2,0.6], tail-end t∈[0,0.25], or TADS-Auto); perturbation *region* mask —
  TBP ∈ {cross, cross+LL, LL, all}, TCP ∈ {L, P, all} (Algorithm 2, p4); interpolation weight ψ
  (fixed at 0.7 throughout, Table S1 p17); moment-matching rescale and norm-preserving projection
  toggles; plus the pre-existing seed and diffusion-temperature handles. The region mask is
  *spatial* selectivity (which tokens get noised), **not** state selectivity — it cannot name a
  target binding mode.

  **The one directional handle in the paper is the true-coordinate injection itself, and it requires
  the answer.** p2: "Boltz recovers correct binding modes when guided toward the correct
  conformational region". There is no aimable version of the method.

  Weak, unquantified aside on off-pocket exploration, p15: "We observed that higher perturbation
  noise can shift predicted ligand positions outside the conventional binding pocket, implying the
  potential to discover alternative binding sites." No alternative-site result is reported.

- **anti_memorization_design**: **YES, and it is the whole evaluation, n = 62.**
  - Diagnostic five: "five recent PDB complexes absent from the Boltz-2 training data set" (p5);
    "The 5 complexes were selected from PDB depositions after the RnP benchmark curation date and
    Boltz-2 training cutoff" (p15, §B.2).
  - RnP subset: "we selected test systems containing a single protein chain and a single ligand
    molecule released after the Boltz-2 training cutoff date" (p15, §B.2), n = 57.
  - **How the cutoff was defined: NOT REPORTED.** The phrase "Boltz-2 training cutoff" is used four
    times (p5 twice, p15 twice) and **the date is never given**, nor is the RnP curation date. The
    cutoff is inherited from the Boltz-2 and RnP papers by reference only.
  - There is no in-training / pre-cutoff comparison arm; every target is post-cutoff, so there is no
    contrast that isolates the memorization effect itself.

- **anti_memorization_control**: **RUN — but as a similarity stratification, not a held-out arm; and
  UNPOWERED where it matters most.**
  The analysis actually run is the SuCOS-pocket stratification, Figure 3 (p7): success counts binned
  by "ligand pocket shape similarity", "where lower scores indicate less similar pockets and ligands
  compared to training-set structures (Škrinjar et al., 2025)". Bin sizes are given: [0,20) N=9,
  [20,40) N=16, [40,60) N=19, [60,80) N=10, [80,100) N=3.

  The result, stated by the authors:
  > "Although the lowest similarity bin (0–20, N =9) in Figure 3 contains too few targets to draw
  > confident conclusions, we observed no improvement in this bin from TBP/TCP perturbations. This
  > may imply that perturbation offer the greatest benefits in the mid-low and mid-high SuCOS-pocket
  > similarity regimes. For targets with very low similarity to the training set, improving sampling
  > alone may not sufficient and additional training may be necessary." [sic] — p7

  **Mark UNPOWERED**: the lowest-similarity bin is N=9 (< ~10) and the authors say so themselves; the
  highest bin is N=3. The diagnostic set is n=5. This is the single most important limitation for
  anyone citing this paper against a memorization framing: **the arm where the sampling-vs-knowledge
  question is sharpest is the one arm that shows no gain, and it is underpowered.**

- **controls_run**: 16 arms actually run and analysed.

  | control | what it rules out | page |
  |---|---|---|
  | Vanilla Boltz-2 (V): 3 seeds × 2 temperatures × 30 samples = 180 poses/target | Rules out that seed and temperature variation alone give the diversity: ligand "RMSF remaining below 2.3 Å in all cases and below 0.5 Å in two cases"; all five baselines on 9Z1L land within 0.02 Å of each other | p5, p15, p6, p7 |
  | Elevated diffusion temperature (V_hT): T ∈ {1.2, 1.3, 1.4}, 270 poses/target | Rules out that the gain is just more stochasticity in the diffusion sampler — V_hT reaches SR_O 22.81% with 4.5× the poses of TCP-C11's 26.32% | p5, p15, p7, p8 |
  | Boltz-2x steering potentials (V_x), `use_potentials`, 180 poses | Rules out that physics-based coordinate-level guidance already solves it: SR_O falls to 15.79%, below vanilla | p5, p15, p7 |
  | MSA masking (V_mask): random masking of MSA columns at rate 0.1, 60 poses | Rules out that input-level MSA perturbation is equivalent to latent perturbation: SR_O 10.53%, worst arm | p15, p7 |
  | MSA subsampling (V_sub): MSA depth reduced to 4086 rows, 60 poses | Same; SR_O 12.28%, also below vanilla | p15, p7 |
  | Matched-or-reduced sampling budget: all TBP/TCP conditions use 60 poses vs 180 (V, V_x) and 270 (V_hT) | Rules out that the gain comes from drawing more samples — "a three-fold reduction relative to the vanilla budget of 180 samples and a 78% reduction relative to the vanilla high-temperature sampling budget of 270 samples" | p5, p8, p9 |
  | **Injection-timing sweep in the true-coordinate experiment** (x-axis "Variance (run condition)", ~12 threshold levels per target, Figure S1) | **The paper's own control on the central claim.** Rules out that injecting the answer at *any* point trivially yields the answer: "because of high noise in the early diffusion schedule, coordinate injection at earlier steps reverted to the default result" | p5, p17 |
  | Region-specific masking ablation: no masking (PP+PL+LP+LL), ligand self-attention only (LL), cross-attention only (PL+LP), all-but-protein-self (PL+LP+LL) | Isolates which conditioning region carries the effect; result: "High-error targets benefited most from perturbing protein–ligand cross-attention, while moderately accurate targets improved with additional ligand self-attention perturbation" | p17, p8 |
  | Noise-schedule ablation: three fixed windows (t∈[0,1], [0.2,0.6], [0,0.25]) + TADS-Auto | Rules out that any single schedule is doing the work; TADS-Auto removes manual window choice | p17, p4, p9 |
  | Regularization ablation: moment-matching rescale (R) and norm-preserving projection (N) ablated independently under a fixed full-trajectory schedule | Isolates whether gains come from the noise or from the re-standardisation | p17, p5 |
  | PoseBusters v0.6.5 + OpenStructure v2.7.0 validity filter on all poses, with a validity-vs-σ sweep (Figure S3) | Rules out that added diversity is just physically invalid poses — though it also exposes the cost: TBP-C1 drops to 90.80% validity, and "the experiments that include LL (ligand region), tend to drop in validity as the noise scale increases" | p16, p19, p7 |
  | Alternative intervention point: head-level attention-weight perturbation in the token transformer | Rules out that any attention-level noise works; "we did not get meaningful improvements on our diagnostic set" — a reported negative result | p13 |
  | Confidence-ranked selection control: SR20 (top-20 by confidence) reported alongside oracle SR_O, plus a top-k sweep k=1..120 (Figure S8) | Rules out that the oracle gain is unrecoverable without ground truth: "TCP-C11 consistently achieves more predictions with RMSD < 2 Å at every k compared to all baselines"; V needs ≈120 predictions (≈3×) and V_x ≈90 (≈2.5×) to match TCP at k=60 | p8, p23, p26 |
  | Confidence-level control: mean confidence compared across arms (Figure 5, S4, S5) | Rules out that perturbation buys accuracy by inflating confidence — "the overall mean confidence scores are similar across experiments and methods ... perturbation methods achieve higher success rates at comparable confidence levels" | p8, p9, p20, p21 |
  | GPU-hardware control: same seed, same CUDA version, same precision, across H100 / A100 / V100 with and without kernel flags (Tables S3, S4) | Rules out (for vanilla) that hardware explains results — "The differences are negligible across different GPUs for vanilla"; **fails to rule it out for perturbation**: 9PY4 under TBP gives 1.674 Å on V100 vs ~9.0 Å on A100/H100, and "the exact GPU type per run was not recorded" | p21, p22 |
  | Method-union arms: TBP∪TCP and TBP∪TCP∪V success counts (Figure 3) | Shows the two perturbation targets rescue **different** targets (21/57 and 22/57 vs 15/57 for TCP alone) — but this is a best-of-methods oracle with no matched-budget baseline | p7 |

- **confidence_as_discriminator**: **Used as a ranking discriminator, explicitly tested, and found
  insufficient.** §5.2 is titled "Confidence alone is not sufficient for pose selection" (p8).
  - *Used*: SR20 ranks the top-20 poses per target by the Boltz-2 confidence score (p8, Table 2 p7);
    Figures S6/S9 scatter confidence vs RMSD per target; Figures S7/S10 do the same for ligand ipTM;
    Figure S8 sweeps top-k.
  - *Validated, and the validation is negative*:
    > "However, the decoupling of confidence from structural accuracy highlights that improvement in
    > model confidence is needed for downstream analysis." — p8
    > "Moreover, model confidence scores did not reliably reflect coordinate-level improvements,
    > suggesting that complementary post-hoc methods such as physics-based re-scoring may be needed
    > for pose selection." — p8
    > "However, we caution that a high confidence metric value alone is not a reliable indicator of a
    > correct pose. For example, the accurate TCP-C11 structures are not always the 'single'
    > most-confident prediction." — p23
    > "The use of confidence scores was not meaningful, as the scores were not consistent across
    > runs." — p15, §B.4 (in the true-coordinate injection experiment specifically)
  - They decline to close the loop: "A thorough analysis of the correlation between confidence
    metrics and pose quality (e.g., ligand RMSD) would be needed to clarify when confidence-based
    selection is reliable, and we leave this for future work." (p23)
  - Note a self-inconsistency in the same passage: p23 says "This is why we report the top-30 ranked
    poses rather than trusting the top-1" while every table and figure in the paper reports top-20.

## D. Claims

- **central_conclusion**: Default Boltz-2 sampling produces near-degenerate ligand binding poses
  (RMSF < 2.3 Å across 180 samples on all five diagnostic targets), and a true-coordinate injection
  experiment shows the denoiser will refine to and hold the experimental pose once the trajectory is
  placed in its vicinity at a low-noise step — which the authors read as evidence that correct
  binding-mode basins already exist in the learned landscape and that the failure is one of sampling
  rather than of knowledge. Building on that reframing, two training-free inference-time
  perturbations of the denoising module's conditioning tensors — TCP on the single representation
  and TBP on the pairwise attention bias — raise oracle success from 19.30% to 26.32% and top-20
  confidence-ranked success from 5.26% to 14.04% on 57 post-cutoff RnP targets while using one third
  of the sampling budget; the gains do **not** appear in the lowest training-similarity bin, where
  the authors say additional training may be needed.

- **necessity_claims** (verbatim + page):
  - p7: "For targets with very low similarity to the training set, improving sampling alone may not
    sufficient and additional training may be necessary." [sic — "may not sufficient"]
  - p8: "However, for targets in the lowest similarity regime, inference-time perturbation alone may
    not overcome the model's limitation, suggesting that targeted fine-tuning or additional training
    data may be necessary."
  - p8: "However, the decoupling of confidence from structural accuracy highlights that improvement
    in model confidence is needed for downstream analysis."
  - p8: "Moreover, model confidence scores did not reliably reflect coordinate-level improvements,
    suggesting that complementary post-hoc methods such as physics-based re-scoring may be needed
    for pose selection."
  - p14, §A.4 (on the alternative they rejected): "Fine-tuning on known binding modes modifies the
    model parameters to bias predictions toward specific conformations of interest but requires
    target-specific retraining and known reference structures."
  - p23: "A thorough analysis of the correlation between confidence metrics and pose quality (e.g.,
    ligand RMSD) would be needed to clarify when confidence-based selection is reliable, and we
    leave this for future work."
  - p3: "Therefore, any additionally injected perturbation should be aware of the current denoising
    step."
  - **No claim of impossibility appears anywhere in the paper.** The strongest negative statements
    are the hedged "may not be sufficient" forms above.

- **novelty_claims** (verbatim + page):
  - p1, Abstract: **"To our knowledge, this is the first systematic perturbation analysis of a
    co-folding architecture for small-molecule binding mode diversity."**
  - p8, Discussion (the same claim, restated without "systematic" and scoped to AF3-style): **"To
    our knowledge, this is the first perturbation analysis of an AF3-style co-folding architecture
    for small-molecule binding mode diversity."**
  - p1, Abstract: "We demonstrate that inference-time perturbations can unlock latent structural
    diversity in generative co-folding models and improve protein-ligand predictions without costly
    retraining."
  - p2, contribution 1: "Diagnosing sampling deficiency. Through true-coordinate injection
    experiments, we demonstrate that Boltz-2 possesses the latent capacity to identify correct
    binding modes, suggesting that the problem can be reframed as a sampling problem amenable to
    inference-time solutions."
  - p2, contribution 3: "In addition, we introduce TADS-Auto, an adaptive schedule that uses the
    model's own noise variance to automatically calibrate perturbation timing and magnitude."
  - p3: "Our work extends this principle to the biomolecular co-folding setting, where the
    conditioning signals are high-dimensional structured tensors, pairwise representations, and
    token embeddings."

  **The central claim our manuscript must engage, verbatim, p1 (Abstract):**
  > "We first show with true-coordinate injection experiments that the model's learned energy
  > landscape contains correct binding-mode basins, allowing us to reframe the problem as one of
  > sampling deficiency."

  Its three restatements, each softer than the abstract, all verbatim:
  > "This result suggests that the learned energy landscape can contain correct basins corresponding
  > to experimentally observed binding modes, but default trajectories converge to suboptimal modes
  > before reaching them." — p2
  > "Therefore, experimentally correct binding modes may be encoded within the model but remain
  > underexplored by default sampling." — p5
  > "Our coordinate injection experiments reframed the core challenge from a model accuracy problem
  > to a sampling deficiency problem, amenable to inference-time solutions." — p8
  > "We have shown that correct binding modes are often encoded within co-folding models but are not
  > recovered at prediction time because of limited sampling diversity." — p9

  **The abstract asserts ("contains") what the body hedges ("can contain", "may be encoded").** The
  strong form appears only on p1 and p8.

- **stated_limits**: The authors state, on their own initiative:
  - Low training-similarity targets are not rescued and may need retraining — p7, p8 (quoted above).
  - Underpowered bins: "the lowest similarity bin (0–20, N =9) in Figure 3 contains too few targets
    to draw confident conclusions" (p7); "Evaluation on an even broader set of diverse targets
    remains a key area for future work" (p7).
  - Confidence scores do not track accuracy — p8, p23.
  - TBP memory overhead: "Since Token Bias Perturbation (TBP) operates on large internal tensors and
    requires tracking diffusion state throughout the sampling process, it incurs additional memory
    overhead ... a small number of targets could not be evaluated on NVIDIA Tesla V100 32GB GPUs due
    to memory constraints" — p9.
  - Hyperparameter space not exhausted: "additional exploration of hyperparameters to enable more
    complex noising schedules and possible application of non-gaussian noise" — p9.
  - Out of scope: "quantitative binding free energy prediction and improvement of confidence metrics
    are also beyond the scope of our current work" — p9.
  - **GPU-dependent non-determinism, reported unusually frankly** — p21: "Despite identical software
    conditions, NVIDIA Tesla V100 32GB GPUs produced substantially different RMSD values (1.674 Å)
    compared to NVIDIA A100 80GB or NVIDIA H100 80GB ( 9.0 Å) ... the exact cause remains unclear";
    p21–22: "Since each experiment was run on whichever GPU resources were available at the time of
    HPC cluster submission, the exact GPU type per run was not recorded. We report this transparently
    as a practical limitation".
  - The theoretical justification does not transfer cleanly: "Note that CADS derives a ridge
    regularization interpretation under a linear condition-to-data mapping assumption. In our
    setting, the conditioning pathway is non-linear, so this specific result does not formally hold."
    — p13.
  - TCP and TBP are not mechanistically separable: "their downstream effects are not fully separable:
    perturbations propagate across depth, and TCP's modulation of queries and keys indirectly affects
    routing. We therefore treat the choice between TCP, TBP, and their combination as an empirical
    question." — p13.
  - The true-coordinate experiment does not always work — p15, §B.4: "some runs successfully
    recovered the correct binding mode even when noise was added. However, some did not recover as
    well. For example, we observed flipped conformations."

  **What they do not state as a limit:** that the noise scale was chosen per target against ground
  truth (route 4), that the RnP subset is failure-conditioned (route 7, stated as a design choice
  rather than a limit), that the 2 Å threshold is unjustified, or that the injection experiment is
  partly circular.

- **stance**: **PROVISIONAL — the user's call.** `threat` on argument + `precedent` on findings.
  - *threat on argument*: this is the clearest published counterargument to a memorization framing —
    it asserts that correct basins pre-exist in the learned landscape and that failure is sampling,
    not knowledge (p1, p8), and it cites Škrinjar et al. 2025 ("Have protein-ligand cofolding methods
    moved beyond memorisation?", p11) as the source of its own benchmark while arriving at the
    opposite emphasis. It must be engaged directly.
  - *precedent on findings*: its diagnostic result — that 180 vanilla samples across 3 seeds and 2
    temperatures collapse to a single mode (RMSF < 2.3 Å, all five targets, p5) and that all five
    baseline variants agree within 0.02 Å on 9Z1L (Table 1, p6) — is a clean, reusable demonstration
    that seed/temperature diversity is illusory in a co-folding model. Its SuCOS stratification
    result (no gain in the lowest-similarity bin, p7) is precedent *for* a similarity-dependence
    argument, not against it.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Oracle success rate (SR_O), vanilla Boltz-2 (V), 180 poses/target | 19.30 | % of 57 targets with ≥1 pose <2 Å | deposited ligand pose, RnP subset n=57 | p7 (Table 2), p8 (Fig 4) |
  | SR_O, Boltz-2x steering (V_x), 180 poses | 15.79 | % of 57 | same | p7, p8 |
  | SR_O, high diffusion temperature (V_hT), 270 poses | 22.81 | % of 57 | same | p7, p8 |
  | SR_O, MSA masking (V_mask), 60 poses | 10.53 | % of 57 | same | p7, p8 |
  | SR_O, MSA subsampling (V_sub), 60 poses | 12.28 | % of 57 | same | p7, p8 |
  | SR_O, TBP-C5 (s=12.0), 60 poses | 22.81 | % of 57 | same — matches V_hT with 78% fewer poses | p7, p8 |
  | **SR_O, TCP-C11 (s=0.9), 60 poses** | **26.32** | % of 57 | same — best arm; +7.02 pp over V, +3.51 pp over V_hT | p7, p8 |
  | Top-20 confidence-ranked success (SR20), V | 5.26 | % of 57 | deposited pose, top-20 of 180 ranked by Boltz-2 confidence | p7, p8 |
  | SR20, V_x | 5.26 | % of 57 | same | p7, p8 |
  | SR20, V_hT | 3.51 | % of 57 | same | p7, p8 |
  | SR20, V_mask | 1.75 | % of 57 | same | p7, p8 |
  | SR20, V_sub | 3.51 | % of 57 | same | p7, p8 |
  | SR20, TBP-C1 (s=3.0) and TBP-C4 (s=3.0) | 10.53 | % of 57 | same | p7 |
  | SR20, TBP-C5 (s=12.0) | 7.02 | % of 57 | same | p7, p8 |
  | **SR20, TCP-C11 (s=0.9)** | **14.04** | % of 57 | same — "more than doubled the success rate of the best baselines (5.26% to 14.04%)" | p7, p8 |
  | Headline abstract fold-change, top-20 | **2.6 to 7.8** | fold | TCP-C11 SR20 vs the range of baselines; 14.0/5.3 = 2.6 (vs V) and 14.0/1.8 = 7.8 (vs V_mask), reading Figure 4's rounded values — **the paper never states which baselines bound the range** | p1, p8 (Fig 4) |
  | Combined-set oracle success, vanilla → TCP | **17.7 → 30.6** | % of 62 targets | "Across the combined 62-target evaluation, TCP nearly doubled the oracle success rate from 17.7% to 30.6%" (= 11/62 → 19/62); p2 calls the same pair "the fraction of predictions with ligand RMSD lower than 2Å", which is a mislabel | p7, p2 |
  | Success count, V → TBP-C5 (s=12) → TCP-C11 (s=0.9) → TBP∪TCP → TBP∪TCP∪V | 11 → 13 → 15 → 21 → 22 | targets out of 57 | deposited pose, <2 Å | p7 (Fig 3) |
  | Win count W_all, TCP-C11 vs V | 20 vs 3 | targets out of 57 with lowest min-RMSD across all 14 methods | deposited pose | p7 |
  | Mean per-target minimum ligand RMSD, V | 9.604 ± 7.025 | Å | deposited ligand pose, n=57 | p7 |
  | Mean per-target minimum ligand RMSD, TCP-C11 | 10.457 ± 6.575 | Å | same — **worse than vanilla on the mean while better on oracle SR** | p7 |
  | Ligand RMSF with protein context (F_p), V → TCP-C11 | 2.382 ± 2.613 → 7.666 ± 4.241 | Å | across the poses generated per target, n=57 targets | p7 |
  | Ligand RMSF without protein context (F_l), V → TCP-C11 | 0.825 ± 0.419 → 1.126 ± 0.485 | Å | same | p7 |
  | Vanilla ligand RMSF, diagnostic five | < 2.3 (all 5); < 0.5 (2 of 5) | Å | across 180 samples/target | p5 |
  | PoseBusters+OpenStructure validity, V → TCP-C11 → TBP-C1 | 98.79 → 97.16 → 90.80 | % of poses valid | all generated poses, n=57 | p7 |
  | Diagnostic-five min ligand RMSD, 9PY4: V → TBP-C2 | 8.958 → 1.674 | Å | deposited pose | p6 (Table 1), p18 |
  | Diagnostic-five min ligand RMSD, 9Z1L: V → TCP-C10 | 7.212 → 0.968 | Å | deposited pose | p6 (Table 1), p18 (0.97) |
  | Diagnostic-five min ligand RMSD, 9RAY: V → TBP-C4 | 2.089 → 1.055 | Å | deposited pose | p6, p18 |
  | Spread of all five baselines on 9Z1L (V, V_x, V_hT, V_mask, V_sub) | 7.195 – 7.214 | Å | deposited pose — 0.019 Å total spread across 180–270 poses and 5 sampling strategies | p6 (Table 1) |
  | Sampling-budget reduction, perturbation vs V / vs V_hT | 3-fold (60 vs 180) / 78% (60 vs 270) | — | pose count per target | p5, p8, p9 |
  | Relative oracle gain of TCP-C11 over V_hT at 78% less compute | 15 | % relative (26.32 vs 22.81) | "TCP achieves 15% higher oracle success compared to the best vanilla Boltz variant, V_hT, with 78% less sampling, which translates to approximately 78% less compute" | p8 |
  | Poses baselines need to match TCP-C11's k=60 count of correct poses | V ≈120 (≈3×); V_x ≈90 (≈2.5×) | poses per target | confidence-ranked top-k, n=23 oracle-successful targets only | p23 (Fig S8) |
  | Targets with ≥1 correct pose when all methods are pooled | 23 of 57 | targets | deposited pose, <2 Å | p23 |
  | GPU-dependent RMSD spread, 9PY4 under TBP, identical seed/CUDA/precision | 1.674 (V100) vs 9.007–9.167 (A100/H100) | Å | deposited pose | p21 (Table S3) |
  | Mean Boltz-2 confidence, diagnostic five, all baselines | 0.925 – 0.927 | confidence score (0–1) | model self-assessment | p20 (Fig S4a) |

- **n_predictions**: recorded separately, per the schema.
  - **Poses per target, by arm** (p7 Table 2 notation; p15 §B.3; p17 §D.1): V = 3 seeds × 2
    temperatures × 30 = **180**; V_x = **180**; V_hT = 3 seeds × 3 temperatures × 30 = **270**;
    V_mask = **60**; V_sub = **60**; **every TBP and TCP condition = 3 seeds × 2 temperatures × 10 =
    60**.
  - **Diagnostic five** (p5): "We generated 180 predictions per PDB complex using three random seeds
    and two temperatures", i.e. 180 vanilla poses × 5 targets = 900 vanilla poses, plus 15 method
    rows × a noise-scale sweep per row (Table S2, p18) whose per-row sample count is not totalled.
  - **Targets**: 5 (diagnostic) + 57 (RnP subset) = **62**, disjoint.
  - **Total poses**: **NOT REPORTED.** Table 2's 14 rows alone imply 1,290 poses/target × 57 =
    73,530 poses, and the full hyperparameter grid (Table S1, p17, plus the σ sweeps in Figures
    S3/S4 spanning σ ∈ [0.1, 25]) is far larger. No grand total, wall-clock time or GPU-hour figure
    appears anywhere.
  - **True-coordinate injection experiment**: number of runs, seeds and samples **NOT REPORTED**.
    Figure S1 (p17) plots ~12 variance-threshold conditions per target with error bars, so n > 1 per
    condition, but no count is given in the caption or in §B.4 (p15).

- **comparable_to_ours**: *(left empty by the extractor, per schema v3)*

- **si_in_scope**: **SI HELD — pp.12–28 of this PDF.** Sections A (Background), B (Methods),
  C (Metric Definitions) and D (Additional Results) are all present, including Tables S1–S4 and
  Figures S1–S10. The code is public (p9: https://github.com/MSDLLCpapers/boltz-perturb) and the
  benchmark is public (Zenodo record 18366081, p9).

  **Two gaps remain despite the SI being held:**
  1. **Per-target RnP results are not tabulated anywhere.** Table 2 (p7) is aggregate over 57
     targets. Per-target min-RMSD for the RnP set exists only as scatter points in Figures S6, S7,
     S9, S10 (pp.24–28) with autoscaled per-panel axes — not extractable as numbers.
  2. **The `Ret / R / D` columns of Table 2** (targets retained / rescued / degraded vs V) are the
     most informative per-method breakdown and are given only as counts, with no list of which
     targets.

## F. Figures

18 panel-group rows. License for all: **CC-BY 4.0 International, no ND clause — redrawing and
modification are permitted with attribution**, stated in the banner on every page including p1: "It
is made available under a CC-BY 4.0 International license."

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 2 | Boltz-2 architecture with the two perturbation injection points (TCP on `s_t`, TBP on `z_t`/pair-bias blocks PP/PL/LP/LL) marked inside the diffusion conditioning path | schematic | `SCHEMATIC \| Boltz-2 trunk → diffusion-conditioning → denoising module, annotating where TCP and TBP inject noise and which protein/ligand token blocks each can mask \| no data` | 1 (single composite) | | CC-BY 4.0, no ND — p1 banner |
| 2 | 6 | Best perturbed pose vs best vanilla pose vs experimental conformer, for each diagnostic target | structure render | `RENDER \| facet: PDB target (5) × method (2: TBP/TCP-perturbed, vanilla) \| views: 1 \| overlay: 1 prediction on 1 reference (ground truth in magenta) \| axis: none` | 10 (5 rows × 2 cols); panels vary by system and by method | **Shows only the single lowest-RMSD pose out of 60 (perturbed) or 180 (vanilla)** — a best-of-N oracle selection presented as the visual result, with no accompanying distribution panel. RMSD is printed per render, so the number is honest; the *selection* is not shown. | CC-BY 4.0, no ND — p1 banner |
| 3 | 7 | Success count (<2 Å) per method, stacked by training-set pocket similarity | bar (stacked) | `PLOT \| facet: none (1) \| vary: method (5: V, TBP-C5 s=12, TCP-C11 s=0.9, TBP∪TCP, TBP∪TCP∪V) \| series: SuCOS-pocket similarity bin (5: [0,20) N=9, [20,40) N=16, [40,60) N=19, [60,80) N=10, [80,100) N=3) \| measure: count of targets with ≥1 pose <2 Å, out of 57 \| mark: bar \| n: 57 targets per bar, per-bin n given in caption` | 1 panel, 5 stacked bars; series varies by training-similarity bin | The two rightmost bars pool separately-tuned methods (and vanilla) into a best-of-methods oracle with **no matched-budget baseline** — a 3-method union is compared against a 1-method column. No uncertainty on integer counts where one target = 1.75 pp. | CC-BY 4.0, no ND — p1 banner |
| 4 | 8 | Oracle vs top-20 success rate for 5 baselines and 2 perturbation methods | bar (grouped) | `PLOT \| facet: none (1) \| vary: method (7: V_mask, V_sub, V_x, V, V_hT, TBP-C5 s=12, TCP-C11 s=0.9) \| series: metric (2: SR_O oracle, SR20 top-20) \| measure: success rate (%) over 57 targets \| mark: bar \| n: 57 targets per bar; poses per target printed above each bar (20/60/180/270)` | 1 panel, 14 bars | **No error bars or CI on percentages computed over n=57**, where a single target moves a bar by 1.75 pp and the headline TBP-vs-V_hT tie (22.81 vs 22.81) is exactly zero targets apart. The differing sampling budgets are labelled, which is good practice, but bar heights are still read side by side across a 4.5× budget difference. | CC-BY 4.0, no ND — p1 banner |
| 5 | 9 | Per-target mean confidence of the top-20 confidence-ranked poses, four methods | box | `PLOT \| facet: none (1) \| vary: method (4: V, TBP-C5 s=12, TBP-C1 s=3, TCP-C11 s=0.9) \| series: none (1) \| measure: per-target mean confidence score of the top-20 poses \| mark: box \| n: 57 per box (one per-target mean each); 20 poses behind each per-target mean` | 1 panel, 4 boxes; varies by method | Boxes are of **means of means** — pose-level spread is collapsed twice, and the caption defers the real distribution to Figures S4/S5. y-axis truncated to 0.800–0.975. | CC-BY 4.0, no ND — p1 banner |
| S1 | 17 | **The paper's central diagnostic.** Ligand RMSD of vanilla vs true-coordinate-injected trajectories, as a function of the noise-variance threshold at which the injection is performed, per diagnostic target | line/point with error bars | `PLOT \| facet: PDB target (5) \| vary: noise-variance injection threshold ("Variance (run condition)", ~12 levels, var1.0 → var45) \| series: run type (4: default Boltz vanilla, true-coordinate injected (TC), min ligand RMSD from default, min ligand RMSD from TC) \| measure: ligand RMSD (Å) \| mark: point + line with error bars \| n: NOT REPORTED per mark, NOT REPORTED per panel` | 5 panels + a legend panel; panels vary by system | **The figure the central claim rests on, and it reports no n.** Caption is one line ("Diagnostic five set true coordinate injection outputs") and never defines "Variance (run condition)", never maps a variance threshold to a denoising step, and never states how many runs are behind each point or error bar. The y-axis carries no units. The recovery/non-recovery split described in §B.4 ("some runs successfully recovered ... some did not recover as well ... we observed flipped conformations", p15) is not visible as a success fraction anywhere. | CC-BY 4.0, no ND — p1 banner |
| S2A | 18 | Vanilla ligand-RMSD distribution per diagnostic target, all 180 poses vs top-10 by confidence | box | `PLOT \| facet: none (1) \| vary: PDB target (5) \| series: pose set (2: all predictions n=180, top-10 confidence) \| measure: ligand RMSD (Å), with a mean-RMSD diamond marker \| mark: box \| n: 180 per box (all predictions), 10 per box (top-10 confidence)` | 1 panel carrying two shapes (see S2B); this row is the box shape | | CC-BY 4.0, no ND — p1 banner |
| S2B | 18 | Mean ligand RMSF per diagnostic target, on a secondary axis over the same categories | line/point | `PLOT \| facet: none (1) \| vary: PDB target (5) \| series: none (1) \| measure: mean ligand RMSF (Å), secondary right-hand axis \| mark: point + line \| n: computed across 180 samples per point` | same single panel as S2A — a dual-y-axis overlay; the letter appears in two rows because one panel genuinely holds two shapes | Dual y-axis overlay of a **fluctuation** measure on an **accuracy** measure with no dispersion shown on the RMSF line; the two axes have different units and the red line reads as a trend across five unordered categorical targets. | CC-BY 4.0, no ND — p1 banner |
| S3A | 19 | PoseBusters validity per baseline method, diagnostic five | bar | `PLOT \| facet: none (1) \| vary: baseline method (5: V, V_x, V_hT, V_mask, V_sub) \| series: none (1) \| measure: valid pose (%) \| mark: bar \| n: 5 targets per bar (individual targets overlaid as dots, ±1 std)` | 1 panel (a) of a 4-panel figure | n=5 per bar, which the caption states; dots overlaid, which is good practice. | CC-BY 4.0, no ND — p1 banner |
| S3B-D | 19 | Validity as a function of noise scale, for each perturbation family | line | `PLOT \| facet: perturbation family (3: TBP small σ∈[0.1,8], TBP large σ∈[0,25], TCP σ∈[0.1,1.0]) \| vary: noise scale σ (continuous, range differs per panel) \| series: configuration (5 in (b): C1,C3,C5,C7,C8; 4 in (c): C2,C4,C6,C9; 3 in (d): C10,C11,C12) \| measure: valid pose (%) \| mark: line with ±1 std shading \| n: 5 targets per point` | 3 panels (b)–(d); panels vary by perturbation family and σ range | σ axis is drawn as **evenly spaced categorical ticks** (0.1…1.0 then 1…8 in (b); 0…10 then 15, 20, 25 in (c)), so a tenfold change in σ occupies the same width as a unit step and the shape of the validity fall-off is not readable. Three panels use three different σ ranges, so curves cannot be compared across them. | CC-BY 4.0, no ND — p1 banner |
| S4A | 20 | Mean confidence per baseline method, diagnostic five | bar | `PLOT \| facet: none (1) \| vary: baseline method (5) \| series: none (1) \| measure: mean confidence score \| mark: bar \| n: 5 targets per bar (dots overlaid, ±1 std)` | 1 panel (a) of a 4-panel figure | **y-axis spans 0.4–1.0 while all five bars sit at 0.925–0.927** — the axis range is chosen so five identical values render as five tall, indistinguishable bars. The genuine finding (confidence is flat across baselines) is legible only from the printed numbers, not the geometry. | CC-BY 4.0, no ND — p1 banner |
| S4B-D | 20 | Mean confidence as a function of noise scale, per perturbation family | line | `PLOT \| facet: perturbation family (3: TBP small, TBP large, TCP) \| vary: noise scale σ_max (continuous, range differs per panel) \| series: configuration (5 / 4 / 3) \| measure: mean confidence score, valid structures only \| mark: line with ±1 std shading \| n: 5 targets per point (mean over poses, then mean over targets)` | 3 panels (b)–(d) | y-axis is 0.7–1.0 in (b)–(d) but 0.4–1.0 in (a) of the same figure, so panel (a) and panels (b)–(d) cannot be read against each other. Same irregular σ tick spacing as S3B-D. Computed on valid structures only, so the arms that lose validity (TBP with LL) are silently conditioned. | CC-BY 4.0, no ND — p1 banner |
| S5 | 21 | Per-target mean confidence over **all** poses, 14 methods, RnP benchmark | box | `PLOT \| facet: none (1) \| vary: method (14: V, V_x, V_hT, V_mask, V_sub, TBP-C1 s=3, TBP-C4 s=3/12/25, TBP-C5 s=3/12/25, TBP-C6 s=3, TCP-C11 s=0.9) \| series: none (1) \| measure: per-target mean confidence score over all poses \| mark: box \| n: 57 per box (one per-target mean each); 60–270 poses behind each per-target mean` | 1 panel, 14 boxes, grouped by family (baselines / TBP / TCP) | y-axis truncated to 0.775–0.975. Box widths do not encode that some per-target means average 60 poses and others 270. | CC-BY 4.0, no ND — p1 banner |
| S6 | 24 | Does confidence track accuracy? Per-target confidence vs ligand RMSD, top-20 poses, 3 methods | scatter | `PLOT \| facet: PDB target (23) \| vary: confidence score (continuous, per-panel autoscaled) \| series: method (3: TCP-C11 s=0.9, V, V_x) \| measure: ligand RMSD (Å) \| mark: point \| n: 20 per method per panel, 60 per panel` | 23 panels; panels vary by system | Caption states **"Axes are autoscaled"** — every panel has a different x and y range (RMSD ceilings from 2.4 Å to 30 Å), so no cross-panel comparison of confidence or accuracy is possible and the 2 Å dashed line sits at a different height in every panel. Panel set is **conditioned on oracle success**: "Only targets with at least one pose below 2 Å ligand RMSD (oracle success) are included, giving n = 23 out of 57 targets." | CC-BY 4.0, no ND — p1 banner |
| S7 | 25 | Same as S6 but ranked and plotted against ligand ipTM | scatter | `PLOT \| facet: PDB target (23) \| vary: ligand ipTM (continuous, per-panel autoscaled) \| series: method (3: TCP-C11 s=0.9, V, V_x) \| measure: ligand RMSD (Å) \| mark: point \| n: 20 per method per panel, 60 per panel` | 23 panels | Same autoscaled-axis and oracle-success conditioning as S6 (n = 23 of 57, stated in caption). | CC-BY 4.0, no ND — p1 banner |
| S8 | 26 | Number of correct poses recovered as a function of confidence-ranked top-k, TCP-C11 vs each baseline | line | `PLOT \| facet: baseline comparator (5: V, V_x, V_hT, V_mask, V_sub) \| vary: top-k (continuous, 1–120 in (a)–(c), 1–60 in (d)–(e)) \| series: method (2: the baseline, TCP-C11 s=0.9) \| measure: number of predictions with ligand RMSD < 2 Å \| mark: line (thin per-target lines + bold mean) \| n: 23 targets per bold line, 1 per thin line` | 5 panels (a)–(e); panels vary by comparator | The mean is taken over **only the 23/57 targets that already have at least one oracle-successful pose** — the 34 excluded targets are precisely those where no method helps. The caption is explicit ("Since most targets have zero predictions below 2 Å, the mean flattens"), which makes it honest rather than hidden, but the plotted curve is not a benchmark-wide result. x-axis maxima differ between panels (120 vs 60), so slopes are not comparable across panels. | CC-BY 4.0, no ND — p1 banner |
| S9 | 27 | Full 57-target version of S6 | scatter | `PLOT \| facet: PDB target (57) \| vary: confidence score (continuous, per-panel autoscaled) \| series: method (3: TCP-C11 s=0.9, V, V_x) \| measure: ligand RMSD (Å) \| mark: point \| n: 20 per method per panel, 60 per panel` | 57 panels | Autoscaled per-panel axes again; at this panel density the axis labels are near-illegible at print size and no per-target numeric table backs it. This is the only place per-target RnP results appear. | CC-BY 4.0, no ND — p1 banner |
| S10 | 28 | Full 57-target version of S7 | scatter | `PLOT \| facet: PDB target (57) \| vary: ligand ipTM (continuous, per-panel autoscaled) \| series: method (3: TCP-C11 s=0.9, V, V_x) \| measure: ligand RMSD (Å) \| mark: point \| n: 20 per method per panel, 60 per panel` | 57 panels | As S9. | CC-BY 4.0, no ND — p1 banner |

**Panel-splitting notes.** Figures 3, 4, 5 are each one row: `mark` and `measure` are constant within
each. S2 is split into two rows because one panel carries a box (`measure:` ligand RMSD) and a line
(`measure:` mean RMSF) on a second axis — a single letter appearing in two rows, as the schema
permits. S3 and S4 are each split because panel (a) is a bar over methods and panels (b)–(d) are
lines over a continuous σ axis — different `mark` **and** different `vary`. S6/S7 and S9/S10 are
kept as four rows rather than two because they are four separately numbered figures, but S6 and S9
share a `data_shape` up to facet count, as do S7 and S10.

**Rendered pages**: 2 (p17 for Figure S1, p18 for Figure S2 — both captions are single lines that do
not carry panel structure). All other panel structures were recoverable from captions and text.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), single-paper extraction, full text read via
  `./pagetext.sh jung2026boltzperturb` (pp.1–28) plus two rendered pages.
- **schema_version**: v3
- **confidence**: **high** on sections A, B, D, E and on `oracle_leakage`, `directional_control`,
  `controls_run`, `confidence_as_discriminator` — the paper is unusually explicit about its protocol
  and its own limitations, and the SI is present in the PDF. **Medium** on section F's `n` slots
  (several figures never state how many observations sit behind a point, most importantly Figure S1)
  and on the exact provenance of the abstract's "2.6 to 7.8 fold" (reconstructed from Figure 4's
  rounded values; the paper never names the bounding baselines). **Medium** on `templates`, which is
  simply never addressed.
- **unresolved**:
  1. **Boltz-2 training cutoff date is never stated**, though the phrase "Boltz-2 training cutoff" is
     the sole basis for the anti-memorization design (p5 ×2, p15 ×2). The RnP benchmark curation date
     is likewise never given. Both are inherited by citation.
  2. **Table S1's hyperparameter grid contradicts the reported runs.** Table S1 (p17) gives σ_max ∈
     {0.5, 1.0, 1.5, 2.0} for both TBP and TCP, but Table 2 (p7) reports TBP at s = 3.0, 12.0 and
     25.0; Table S2 (p18) reports ns up to 25.0; and Figure S3c (p19) sweeps σ ∈ [0, 25]. The stated
     grid is either incomplete or superseded, and the paper never reconciles them. This matters
     directly for `oracle_leakage` route 4: **the actual searched range cannot be determined from the
     paper.**
  3. **Table S2's `V highT` row (p18) duplicates the `Vx` row exactly** (2.25 / 3.01 / 9.01 / 3.82 /
     7.21) and disagrees with Table 1's V_hT column (p6: 2.457 / 3.015 / 8.947 / 2.158 / 7.195).
     One of the two tables is wrong; the paper does not flag it.
  4. **Sample size of the true-coordinate injection experiment is never reported** — no n per
     variance condition, no seed count, no total runs. §B.4 (p15) reports a qualitative success/
     failure split ("some runs successfully recovered ... some did not") with no fraction attached.
  5. **"Variance (run condition)" — the x-axis of Figure S1 — is never defined**, and the mapping
     from a variance threshold to a denoising step index is never given, although the tail-end window
     discussion (p17) shows the authors know that step 154 of 200 corresponds to t ≈ 0.25.
  6. **p2 and p7 describe the same 17.7% → 30.6% pair differently**: p2 calls it "the fraction of
     predictions with ligand RMSD lower than 2Å", p7 calls it "the oracle success rate" over 62
     targets. The numbers reconcile as 11/62 and 19/62, i.e. p7 is correct and p2 is a mislabel.
  7. **The abstract's "2.6 to 7.8 fold" is not stated against named baselines anywhere.** It
     reconstructs from Figure 4's rounded SR20 values as 14.0/5.3 (vs vanilla) to 14.0/1.8 (vs MSA
     masking), so the upper end of the range is measured against the paper's weakest baseline.
  8. **p23 says "we report the top-30 ranked poses" while every table and figure reports top-20.**
  9. **GPU non-determinism is unresolved by the authors' own account** and could account for a
     headline diagnostic result: 9PY4's best TBP RMSD of 1.674 Å (Table 1, p6) is a V100 number that
     A100 and H100 reproduce as ~9.0 Å under identical software and seed (Table S3, p21), and "the
     exact GPU type per run was not recorded" (p21). Table 2 is stated to be all-H100 (p7 caption),
     so the RnP results are internally consistent, but **the diagnostic-five table mixes hardware**.
  10. **Templates**: never stated on or off for any arm.
  11. **Tag I needed and could not use** — see the Tags section: there is no Control-block tag for
      an intervention that is deliberately *undirected*, and no Method-block tag for a
      diagnostic that injects the ground-truth answer to probe the landscape.
- **why_it_matters**: *(left empty by the extractor, per schema v3 — the user's call)*

---

## What the coordinate-injection argument does and does not establish

Recorded here rather than in a schema field because it is the reason this paper was extracted, and
because the schema has no field for "how far does the paper's own evidence carry its own claim". No
editorialising: this is a statement of what is and is not shown, with the controls the paper ran.

**The claim, verbatim (p1, Abstract):**
> "We first show with true-coordinate injection experiments that the model's learned energy landscape
> contains correct binding-mode basins, allowing us to reframe the problem as one of sampling
> deficiency."

**What was injected, when, what was measured, what was concluded.** The deposited ligand+protein
coordinates, loaded from the PDB as a NumPy array (p15), replace the sampler's predicted coordinates
**once**, at the first denoising step whose noise variance falls below a set threshold; reverse
diffusion then continues under the default noise schedule to completion (p5, p15). The measurement
is the final ligand RMSD to the same deposited structure, plotted against the variance threshold
(Figure S1, p17). The conclusion drawn is that "the denoiser can refine to the correct binding mode
once the trajectory enters its basin" (p5).

**What this establishes.** That the injected pose is not destroyed by the remaining denoising steps:
the model's learned dynamics, from a low-noise state, refine toward and hold the experimental pose
rather than reverting to the pose the unperturbed trajectory would have produced. That is a real
finding about the denoiser's behaviour near the reference pose, and it is not trivially true — the
same paper shows that on 9Z1L every unperturbed sampling strategy lands 7.2 Å away and stays there.

**What this does not establish.** (i) That the correct pose is a *basin* — a region of attraction the
sampler could reach on its own — as opposed to a locally stable point in a regime where the denoiser
has almost stopped moving. The paper's own control is exactly the sweep that exposes this: injection
survives only at **low** variance thresholds and, at higher ones, "coordinate injection at earlier
steps reverted to the default result" (p5). The window in which the answer persists is the window in
which the model changes least. (ii) That the injection is reliable even in that window — §B.4 (p15)
reports that "some runs successfully recovered the correct binding mode even when noise was added.
However, some did not recover as well. For example, we observed flipped conformations", with no
success fraction and no n. (iii) That the recovered pose is preferred by the model, since "The use of
confidence scores was not meaningful, as the scores were not consistent across runs" (p15) — the
model cannot be shown to *score* the injected pose as better than the one it produces by default.

**Controls the paper ran on this specific experiment, and what they rule out** (also in
`controls_run`): the **injection-timing sweep** (Figure S1, ~12 variance thresholds per target,
p5/p17) rules out the trivial reading that injecting the answer at any point returns the answer.
**Controls the paper did not run**: no decoy injection (a plausible-but-wrong pose injected at the
same step, to test whether the denoiser holds *any* injected pose or specifically the correct one);
no random-pose injection; no injection of a near-native perturbed pose to map the basin's width; and
no confidence or energy comparison between the injected-and-refined pose and the default pose. The
first of these is the control that would separate "the correct basin exists" from "late-stage
denoising preserves whatever it is handed", and it is absent.

**The non-circular part of the argument is elsewhere.** The perturbation results are not circular in
the same way: TBP and TCP inject only Gaussian noise (Algorithm 2, p4), and they nevertheless produce
sub-2 Å poses on targets where every vanilla variant fails by 7–9 Å (9PY4 8.958 → 1.674 Å; 9Z1L 7.212
→ 0.968 Å, Table 1 p6). That is genuine evidence that reachable-without-the-answer poses exist near
the reference. It is qualified by three things the paper itself reports: the *configuration and noise
scale* were selected per target against ground truth (Table S2 caption, p18); the pose is the oracle
best of 60; and the gain vanishes exactly where the memorization question is sharpest — "we observed
no improvement in this bin from TBP/TCP perturbations" for the lowest training-similarity bin (p7,
N=9, which the authors call too small to conclude from).

---

## Tags

`general-protein` `cofolding` `latent-steering` `msa-subsample` `ensemble` `single-state`
`rmsd-only` `binary-predicate` `saturating-metric` `oracle-leak` `design-level-oracle`
`anti-memorization` `unpowered` `confidence-as-discriminator` `orthosteric` `preprint` `threat`
`precedent` `comparator-numbers`

Justification for the non-obvious ones, and the tags deliberately withheld:

- **`latent-steering`** — the schema's definition is exact: "any inference-time intervention on an
  internal tensor — pair representation, trunk embedding, distogram head, conditioning embedding."
  TCP perturbs the single conditioning tensor `s_t`; TBP perturbs the attention bias `B` derived from
  the pairwise representation `z_ij` (p3, p4). Note the tag name says "steering" but this method does
  not steer — see `directional_control`.
- **`msa-subsample`** — applied to the **baseline arms only** (V_sub: MSA depth reduced to 4086 rows;
  V_mask: random column masking at rate 0.1, p15). Tagged because those arms were run and their
  numbers are reported (Table 2, p7), and a reverse lookup for MSA-subsampling comparators should
  find this paper. **Not** `msa-state-filter`: no state-specific alignment is used anywhere.
- **`ensemble` + `single-state`** — the pair the schema explicitly sanctions: perturbation samples
  widely (RMSF 2.38 → 7.67 Å), default Boltz collapses (RMSF < 2.3 Å on all five diagnostic targets).
- **`saturating-metric`** — numeric floor, not an axis artefact: 34 of 57 targets score zero under
  all 14 methods pooled (p23), and Figure S8's caption states the consequence outright (p26).
- **`oracle-leak`** — routes 4 (per-target noise scale chosen by minimum RMSD to the deposited pose,
  Table S2 p18; sweep range extended on the evaluation set, Table S1 p17 vs Table 2 p7), 5 (oracle
  success rate is the primary metric, p7, p16), 6 (min-RMSD and win-count labels, p6, p7).
- **`design-level-oracle`** — route 7, and **weaker than the above, kept distinct as the schema
  requires**: the RnP subset is constructed from prior knowledge that Boltz-2 failed on those targets
  (p15), and the injection diagnostic declares its answer by construction (p5, p15).
- **`anti-memorization`** — all 62 targets post-date the Boltz-2 training cutoff (p5, p15), and a
  training-similarity stratification was actually run and analysed (Figure 3, p7).
- **`unpowered`** — the diagnostic set is n=5; the SuCOS bin that matters most is N=9, which the
  authors themselves call "too few targets to draw confident conclusions" (p7); the top bin is N=3.
- **`confidence-as-discriminator`** — used for SR20 ranking **and** explicitly tested against
  accuracy, with a negative result (§5.2 p8, §D.7 p23, Figures S6–S10).
- **`orthosteric`** — the benchmark is single non-covalent ligands in the conventional binding pocket
  (p15). The one off-pocket remark ("higher perturbation noise can shift predicted ligand positions
  outside the conventional binding pocket, implying the potential to discover alternative binding
  sites", p15) is unquantified and unevaluated, so **not** `allosteric-site` or `cryptic-pocket`.
- **`threat` + `precedent`** — provisional, per section D; the user decides.
- **`comparator-numbers`** — Tables 1 and 2 (pp.6–7) are directly reusable: 14 method arms, 57
  post-cutoff targets, oracle and non-oracle success rates, mean min-RMSD, RMSF and validity, with
  pose budgets stated per arm.

**Withheld deliberately:**
- **`multi-backbone`** — Boltz-2 only; Boltz-2x is a flag on the same model. The claim that the
  targets "exist in all AF3-style architectures" (p12) is untested.
- **`prospective`** — retrospective in evaluation, in tuning and in set construction.
- **`visual-metric`** — Figure 2 is a render but every pose carries its RMSD; no state is called by
  eye.
- **`no-template-no-msa` / `templates-on` / `state-annotated-input`** — none can be asserted:
  templates are never mentioned in any protocol statement, and the MSA regime for the method arms is
  Boltz-2 default with no depth reported.
- **`seed-only`** — would misdescribe the method. Seed-and-temperature variation is the *baseline*
  the paper argues against, not its control handle.
- **`experimental-validation`, `md`, `enhanced-sampling`, `benchmark-only`, `af-cluster`,
  `md-emulator`, `experimental`, `template-state-bias`, `msa-state-filter`** — none apply.
- **Every Control-block tag** (`directed-state`, `partner-driven`, `ligand-driven`,
  `peptide-driven`, `g-protein-mimetic`, `nanobody`, `apo-sampling`, `seed-only`) — none apply,
  because **the method has no directional handle by design** (p3, p14). See the tag gap below.

**Tags needed but not in the v3 vocabulary — recorded, not invented:**
1. A Control-block value for **deliberately undirected inference-time perturbation** — a method that
   broadens the distribution and cannot be aimed at a named state. Every existing Control tag names a
   directing handle, so a paper whose defining property is the *absence* of one has no way to be
   found by reverse lookup. Suggested: `undirected-sampling`.
2. A Method- or Rigour-block value for a **ground-truth-injection diagnostic** — an experiment that
   deliberately feeds the answer into the model to probe what the learned landscape supports. This is
   a recognisable and recurring experimental form (cf. the Bennett et al. 2023 citation on p2 and the
   Richman et al. 2025 framing on p5), it is the reason this paper matters to us, and `oracle-leak`
   is the wrong label because the use is diagnostic and disclosed. Suggested:
   `answer-injection-diagnostic`.
3. A Rigour-block value for **hardware/numerical non-determinism affecting reported results**. This
   paper reports a 7.3 Å swing on the same target with the same seed across GPU families (p21) and
   flags it honestly; there is no way to tag or later retrieve that.
