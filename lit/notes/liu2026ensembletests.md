# liu2026ensembletests

Schema v3 extraction. Every field present; `NOT REPORTED` / `NOT APPLICABLE` where the paper
does not say or the field does not apply.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–31)**, which are the only
page numbers the preprint carries. Layout: p1 title/abstract/Introduction start, p1–2
Introduction, p3 Fig. 1, p4–11 Results (Fig. 2 p5, Table 1 p6, Fig. 3 p7, Fig. 4 p10, Fig. 5
p11), p12–13 Discussion, p13–22 Methods, p23–29 Extended Data (Figs. 1–7, Table 1), p30–31
References, p31 Statements (data/code availability, CRediT, funding).

**This is a methodological critique + a benchmark, not a structure-prediction paper.** Section C
is therefore partly `NOT APPLICABLE` by design (tag `benchmark-only`), not by sloppiness. The
authors run no co-folding model and predict no structure; they run MD, construct control
ensembles, and score nine public conformational generators.

**Supplementary Information is NOT in the held PDF.** Supplementary Notes 1–12 and Supplementary
Table S7 are cited throughout (Notes 2, 3, 6, 9, 10, 12 carry load-bearing claims) and are
absent. Extended Data Figs. 1–7 and Extended Data Table 1 ARE in the PDF (pp. 23–29). See
`si_in_scope`.

---

## A. Identity

- **citekey**: `liu2026ensembletests`
- **doi**: **10.64898/2026.09.02.748111** (bioRxiv) — p1 banner: "bioRxiv preprint doi:
  https://doi.org/10.64898/2026.09.02.748111; this version posted September 4, 2026." Matches
  `MANIFEST.csv` and `refs.bib`. Note the `10.64898` prefix rather than bioRxiv's usual `10.1101`;
  recorded as printed.
- **year**: **2026** — posted 4 September 2026 (p1).
- **venue**: **bioRxiv preprint, NOT peer reviewed.** p1: "The copyright holder for this preprint
  (which was not certified by peer review) is the author/funder…". Tagged `preprint`. No journal
  named anywhere in the PDF. Data availability (p31) says Dynbench 1.0.0 "will be made public at
  publication", so a journal submission is implied but not identified.
- **title**: "Ensemble tests mask missing dynamics in protein conformational generators" (p1).
- **authors**: Kaining Liu, Qiuting Qian, Ying Chi (corresponding, yingchi@intl.zju.edu.cn) — p1.
  Affiliations: Second Affiliated Hospital of Zhejiang University School of Medicine and
  Zhejiang University–University of Edinburgh Institute (ZJE), Zhejiang University; Edinburgh
  Medical School, University of Edinburgh (p1).
- **software artefact**: **Dynbench** v1.0.0, MIT licence, https://github.com/kkkniengLiu/dynbench
  (p31); data archive under reserved DOI 10.5281/zenodo.22146996, public at publication (p31).

## B. Scope

- **system**: **general protein.** No receptor/kinase/transporter focus. Main set is 82 ATLAS
  protein chains (p13); external sets are 82 mdCATH CATH domains at 320 K (p13–14) and PTM-85, 85
  phosphorylated (phospho-serine) proteins (p14); Lockbox-36 is 36 "soluble monomeric proteins of
  60–300 residues" (p14). Peptide positive controls: alanine dipeptide (two sources) and the
  WLALL pentapeptide (p14). Fig. 1 illustrates on ATLAS `5ftw_A`, 256 residues (p3).
- **n_targets**: **82** ATLAS chains (frozen evaluation set, p13) is the headline n. Additionally:
  **36** Lockbox proteins (Broad) of which **8** are the Deep subset extended to 1 µs (p14); **82**
  mdCATH domains (p13); **85** PTM-85 proteins (p14); **3** peptide systems (2 alanine-dipeptide
  sources + WLALL, p14). Model coverage on ATLAS-82 is partial for four models: ConfRover 73,
  ProTDyn 74, P2DFlow 65, BioKinema 81 (p13; Table 1 p6). The five ordered deep models and four
  kinetic anchors share a **72**-protein intersection (p19). Generality claim is broad and IS
  backed by four independent protein datasets plus three peptide systems.
- **method_class**: **benchmark-only + MD** (dual). Benchmark-only: Dynbench is a scoring
  protocol for external submissions (p15, "Submission contract and adapters"). MD: the authors
  ran their own reference simulations for Lockbox-36 — "three independent 200-ns CHARMM36m
  simulations in modified TIP3P water with 150 mM NaCl, saved every 10 ps; the three replicas of
  each preselected Deep protein were extended to 1 μs" (p14). ATLAS/mdCATH/PTM-85/peptide
  trajectories are pre-existing public data (pp. 13–14, 31).
- **backbones**: **NOT APPLICABLE** — no structure-prediction backbone (no AF2/AF3/Boltz/Chai/
  OF3/Protenix) appears anywhere in the paper. What is compared head-to-head is **nine public
  conformational/trajectory generators**, all scored on ATLAS-82 (Table 1, p6):
  - *ordered, temporal contract resolved*: **ConfRover** (1 ns, n=73), **MDGen** (1 ns, n=82)
  - *ordered, temporal contract unresolved (NR)*: **BioKinema** (10 ns, n=81), **ProTDyn** (10 ns,
    n=74), **MarS-FM** (~50 ns, n=82)
  - *unordered ensemble*: **AlphaFlow** (n=82), **P2DFlow** (n=65), **BioEmu** (n=82), **Str2Str**
    (n=82)
  - *not scored*: **ATMOS** — "not independently scored because public code and weights were
    unavailable at the evaluation cutoff; its reported 1-ns results are included in the literature
    comparison" (p8). **GLDP** and **Timewarp** appear only in the Extended Data Table 1 capability
    matrix (p29).
  Plus four internal baselines/anchors (p19): `classical_md` (held-out real MD replicate, the
  oracle), `msm_generative` (Markov-state generator), `tica_ou` (per-mode Ornstein–Uhlenbeck /
  Koopman near-harmonic surrogate), `iid_equilibrium` (i.i.d. resample of reference frames, the
  no-dynamics floor).
  See `unresolved` for why I did **not** apply the `multi-backbone` tag.
- **templates**: **NOT APPLICABLE** — no template channel exists; submissions are Cα coordinate
  arrays, not predictions from sequence. Protocol described p15 ("Submission contract and
  adapters": "a per-protein NumPy archive with Cα coordinates (T, L, 3) in reference residue
  order, an ordered flag and, for an ordered trajectory, a physical frame interval").
- **msa_handling**: **NOT APPLICABLE to the benchmark itself.** The single MSA mention is a
  property of an evaluated model: "BioKinema uses intended-MSA mode and has 29 of 82 evaluation
  chains overlapping its training corpus under the model-specific screen (Supplementary Note 3)"
  (Table 1 footnote †, p6). Neither subsampling nor state-filtering is performed by the authors.

## C. Conformational core

- **states_generated**: **ensemble + continuum.** What the *authors* produce is (i) time-ordered
  MD trajectories — Lockbox-36 CHARMM36m, 3 × 200 ns per protein saved every 10 ps, Deep-8
  extended to 1 µs (p14) — which are continua, and (ii) deliberately constructed *ensembles with
  the time axis removed*: exact-frame permutations of authentic MD (p3, p19), i.i.d. equilibrium
  resamples of reference frames (p19), and stationary-matched MSM re-orderings of an identical
  coordinate multiset (p19). No single-state or two-state prediction anywhere in the paper. The
  *evaluated* outputs are ensembles (four unordered generators) or trajectories (five ordered
  generators) supplied by their authors, not generated here.
- **structural_priors_used**: The design-time structural knowledge is **MD ensembles, not
  deposited experimental structures**:
  - ATLAS all-atom MD ensembles: "Each protein provides three independent 100-ns replicas saved
    every 10 ps" (p13). The evaluation split, anchors and verdict rules were frozen against these.
  - mdCATH multi-temperature all-atom MD for CATH domains, "~440-ns replicas saved every 1 ns",
    scored at 320 K under a 4-ns contract (p13–14).
  - PTM-85: 85 phosphoproteins, "three independent 10 ns MD replicates each", drawn from
    "DynaMo-PTM, an in-house database being prepared for separate publication" (p14, p31).
  - Public peptide MD: Timewarp alanine dipeptide (two trajectories, 0.25 ps saving), MDshare
    heavy-atom AD set from PyEMMA (three 250-ns trajectories, 1 ps saving), MDshare WLALL
    pentapeptide (25 × 500 ns implicit solvent, stride 25) (p14).
  - Lockbox-36 selection criterion: "36 soluble monomeric proteins of 60–300 residues selected
    prospectively after the evaluated model checkpoints were fixed" (p14). The **starting
    structures** for these 36 simulations are NOT REPORTED — the paper never says where the
    initial coordinates came from (PDB entries, models, or otherwise).
  - Reference-derived analysis objects: TICA basis fitted on the reference trajectory (p14, p19);
    a reversible microstate Markov model fitted to replicas A and B on four reference-fit TICA
    modes with PCA fallback (p19); a per-mode Ornstein–Uhlenbeck operational reference fitted on
    the reference trajectory (p17).
  None of this is a defect; it is the reference data a kinetic benchmark requires. The
  defect-shaped items are in `oracle_leakage` route 4.

- **oracle_leakage**: enumerated route by route. Summary: **no pipeline leakage of a target-state
  structure (routes 1, 2, 3, 5, 6 are clean), but real route-4 leakage — several verdict constants
  and reportability thresholds were calibrated or fixed on the evaluation data — and a self-
  declared route-7 design-level oracle in the control arms, which for a control is legitimate.**

  1. **Structures used as input or template — NONE FOUND (as leakage).** The scoring target *is*
     reference MD by construction, which is the benchmark's definition, not a leak. Protocol
     described p15: "A submission is a per-protein NumPy archive with Cα coordinates (T, L, 3) in
     reference residue order, an ordered flag and, for an ordered trajectory, a physical frame
     interval." The evaluation replicate is always held out from calibration: p20, "Each protein
     supplies three replicates: the last is the evaluation target, one is the N1 reference
     stand-in and the remaining replicate supplies calibration statistics. The evaluation target
     never enters calibration or the N2 pool." An explicit anti-leak check is run: p18, "Direct
     coordinate comparison verified that every seed used the same selected frames and changed only
     their order; no selected model frame matched the held-out reference coordinate fingerprint."
     **Model-side** leakage is acknowledged rather than committed: p13, "Because the ATLAS
     trajectories are public, this evaluation is not a strict hidden test." And p13: "complete
     model-specific training-corpus disjointness remains unverified."
  2. **State annotations from a curated database (GPCRdb / KLIFS / Kincore) — NONE FOUND.** No
     state-annotation database is used or cited anywhere. There is no discrete "active/inactive"
     labelling in the protocol; states are microstates in a reference-fit TICA/MSM basis (p19).
     Protocol pages 13–19.
  3. **Cluster labels derived from known states — NONE FOUND as leakage, with one caveat.** The
     microstate clustering and TICA basis are fitted on **fit replicas A and B**, with replica C
     held out for evaluation: p19, "we fitted a reversible microstate Markov model to replicas A
     and B on four reference-fit TICA modes, with a PCA fallback, and retained replica C for
     evaluation." No deposited-state labels enter. The caveat is *selection coupling*, which the
     authors state and then measure: p17, "The informative set is selected once per protein and
     shared by the trivial floor, surrogates and deep models. Selection requires real-replicate
     agreement to exceed the trivial surrogate **and can favour the oracle's absolute score**,
     while every row remains evaluated on the same selected metrics." Quantified by a decoupled
     control: 0.963 decoupled vs 0.951 coupled, Δ +0.012 (p17, ED Fig. 4d p26).
  4. **Hyperparameters / sweep ranges / seeds / stopping criteria tuned against the evaluation
     set — PRESENT, self-declared, and the only genuine leakage route.** Multiple constants were
     calibrated on, or fixed after seeing, the evaluation data:
     - p13: "The study uses a version-frozen protocol rather than prospective preregistration;
       **exploratory scoring preceded the split freeze**, and later analyses are identified as
       post hoc."
     - p15, the steric-clash ceiling calibrated on the evaluation set's own reference replicates:
       "Its absolute ceiling, 0.000758, was calibrated before rescoring as twice the maximum
       across 246 reference replicates; each protein also retains its reference-replicate maximum
       inflated by 50%, and the larger bound is used." (246 = 82 proteins × 3 replicas.)
     - p18, the reportability thresholds: "the oracle-minus-floor separation must be at least 0.30
       with a 95% bootstrap interval excluding zero, and the median number of informative temporal
       metrics must be at least three. **These post hoc operational criteria were fixed before the
       leak-free 105-cell audit.**"
     - p14, metric families: "The family definitions were formalised after scoring and no metric
       combinations were searched."
     - p22: "The split, anchors and verdict rules were frozen before model promotion, but **the
       alignment audit and pair-normalised clash analysis are explicitly post hoc.**"
     - p15, the pair-normalised clash statistic itself replaced an earlier frame-level statistic
       after rescoring: "This pair-normalised rate removes the strong chain-length dependence of
       the former frame-level 'any clash' fraction."
     Mitigation, also on the record: a 5×3 grid over gap 0.20–0.40 × median support 2–4 leaves all
     five contract statuses unchanged in all 15 settings (p18); a 27-combination verdict-constant
     sweep keeps oracle-to-floor separation at 0.80–1.00 and the floor at 0.00 (p21); a clash-
     ceiling rescale from 0.25× to 4× does not reorder the five ordered rows (p21). One constant
     is load-bearing and admitted: p21, "One constant is genuinely load-bearing: as the RMSF
     too-cold fraction rises from 0.3 to 0.7, ConfRover falls from 0.849 to 0.452, so its majority
     Layer-4 validity survives a fraction of 0.6 but not 0.7."
  5. **Success defined post hoc by RMSD/TM to a structure they had — NONE FOUND.** No RMSD-to-
     reference-structure or TM-score criterion appears anywhere. Success is the MODEL-OK verdict,
     defined by a model's position between a time-shuffled trivial floor T and a class-specific
     operational reference O, both derived from MD, with fixed algebraic thresholds (pp. 16–17).
     Note the *ladder* is post hoc in ordering-check only: p17, "Reversing the MODEL-OK and
     MODEL-FAILS checks changed no metric cell or kinetic-pass row."
  6. **Best/worst model labels assigned against a held reference — NONE FOUND as a *selection*
     device.** Every submission, including the held-out MD replicate, is "scored as an ordinary
     submission" (p17, p19). No per-target best-of-k selection is performed; there is no k. Partial
     coverage is not imputed and technical NA is kept distinct from failure (p14, p22: "Missing
     model outputs are treated as technical NA rather than failures").
  7. **Design-level oracle use — PRESENT and, in this paper, legitimate by construction; label it
     design-level, not pipeline leakage.** The three control arms are built so the expected answer
     is known before scoring: exact-frame shuffling *must* leave an order-invariant ensemble score
     unchanged (p2, "Ensemble tests must return the same answer; a test of dynamics must not"); an
     i.i.d. resample of reference frames *must* have no transition process; a held-out MD
     replicate *must* contain one. That is what a positive and a negative control are for, and the
     paper says so. The reading a critic could press: because Layer-2 metrics are functions of the
     frame marginal only, **the ensemble-invariance half of the central result is analytic rather
     than empirical** — the paper's own Fig. 1d reports "maximum within-protein change, 0" (p3),
     i.e. exact invariance, not an estimate. The empirical content is the *other* half: that the
     temporal tests collapse (0.963 → 0.004) while an independent replicate reaches 0.95, and that
     Layer-4 admissibility also survives shuffling (0.992–1.000). A second design-level item: the
     Lockbox-36 protein set was chosen *after* checkpoints were frozen (p14), which is anti-leak,
     but 9 of 36 subsequently flagged against disclosed ATLAS/mdCATH corpora (p14) means the
     prospectivity is of the reference data, not of the models' training exposure.

- **prospective**: **partial.**
  - *Prospective*: Lockbox-36 — "36 soluble monomeric proteins of 60–300 residues selected
    prospectively after the evaluated model checkpoints were fixed. Protein identities, three
    replicate roles, the eight-protein Deep subset, model contracts, endpoints, exclusions,
    bootstrap rules and gate thresholds were frozen before model scoring" (p14). The reference
    MD for it was run by the authors, so it is genuinely new data.
  - *Retrospective*: the ATLAS-82 headline scorecard — "Because the ATLAS trajectories are public,
    this evaluation is not a strict hidden test" (p13), and "The study uses a version-frozen
    protocol rather than prospective preregistration; exploratory scoring preceded the split
    freeze" (p13). Several verdict constants and reportability thresholds are post hoc (route 4).
  So: prospective in its validation set and in the protein selection, retrospective in the
  protocol's own calibration.

- **state_metric**: **continuous coordinate + binary predicate** (dual, and the duality is the
  design). Four layers, then a gate (pp. 15–18). Full metric inventory:

  | Layer | What it computes | How | Page |
  |---|---|---|---|
  | **Layer 1** — frame realism | single-frame sanity check | saturated on equilibrium MD frames by construction; "not expected to rank plausible generators" | p15 |
  | **Layer 2** — ensemble | free-energy-surface divergence; contact-distribution divergence; per-mode displacement Wasserstein distance | compared against the reference ensemble | p15 |
  | **Layer 3** — kinetics (ordered submissions only) | time-lagged autocorrelation; VAMP-2 score; implied timescales; transition-matrix statistics; mean-first-passage; directional predictability | **seven time-ordered metrics** used by the gate, + an eighth order-invariant per-mode displacement Wasserstein kept only as a legacy diagnostic; evaluated only where the model's declared physical frame interval supports the requested lag, else NA | p15, p18 |
  | **Layer 4** — geometric/fluctuation admissibility | steric clashes (non-adjacent Cα pairs < 4 Å ÷ eligible frame-pairs; absolute ceiling **0.000758**, or the protein's reference-replicate max +50%, whichever larger); virtual Cα–Cα bond-length violations; Ramachandran outliers (MolProbity) when backbone atoms supplied; late-vs-early drift; RMSF spread (two-sided, fails below **0.5×** min or above **2.0×** max reference). Radius of gyration is a QC diagnostic only and "never enters the verdict" | p15 |

  **Per-metric verdict (continuous → categorical), p16.** With T = trivial surrogate (time-shuffled
  or i.i.d.), M = model, O = class-specific operational reference, S = replicate noise floor, all
  expressed as errors so lower is better; A = max(|T|,|S|,|O|,10⁻⁹), Δ = T − S, c_X = (T − X)/Δ:
  ```
  SATURATED     if Δ ≤ 0.1 A
  DATA-LIMITED  if c_O < 0.15
  MODEL-OK      if c_M ≥ 0.6 c_O
  MODEL-FAILS   if c_M < 0.15
  MODEL-LIMITED otherwise
  ```
  Evaluated in that fixed order. "MODEL-OK is the only pass: SATURATED instances leave the
  denominator, whereas DATA-LIMITED and MODEL-LIMITED remain and count against the model" (p17).
  Choice of T and O is **per metric class** (p16–17): equilibrium metrics take T = a static
  structure and O = an i.i.d. equilibrium resample; kinetic metrics take T = time-shuffled
  surrogate and O = a per-mode OU fit; transition and mean-first-passage metrics take T =
  time-shuffled surrogate and O = a held-out real replicate ("because a single-basin OU process
  structurally cannot represent multi-state transitions"). Two of seven time-ordered metrics use
  the replicate reference, five use OU (p17). "The unqualified word oracle in this paper always
  denotes the held-out real-MD replicate (`classical_md`), never O" (p16).

  **Binary predicate — post-gate kinetic pass (`realdyn`), pp. 17–18.** Per protein p, with ℐ_p the
  non-SATURATED, non-NA temporal metrics, q_p their MODEL-OK fraction, g_p = 1[L4 = VALID]:
  ```
  realdyn = (1/|𝒫*|) Σ_{p∈𝒫*} 1[q_p ≥ 0.5] · g_p ,   𝒫* = {p : |ℐ_p| > 0}
  ```
  i.e. a protein counts "only if the model passes at least half of its informative temporal
  Layer-3 metrics **and** is Layer-4 valid" (p17). Threshold **0.5**, justified only as a majority
  and swept over {0.3, 0.4, 0.5, 0.6, 0.7} (p20). Explicitly disclaimed as a physical fraction:
  "It measures success under the audited contract rather than a fraction of physical dynamics
  learned" (p17).

  **Contract-level gate (reportability), p18.** Before any post-gate pass is reported: oracle-minus-
  floor separation ≥ **0.30** with a 95% bootstrap CI excluding zero, AND median informative
  temporal metrics ≥ **3**. Failing either gives **NR**, not a model failure. ConfRover and MDGen
  pass at 1 ns (median support 4; separations 0.956 [0.903–0.996] and 0.921 [0.859–0.971]);
  BioKinema and ProTDyn are range-limited at 10 ns (separations 0.053 [0.032–0.076] and 0.058
  [0.036–0.085]); MarS-FM is support-limited at ~50 ns (three reference frames, median support
  one, separation 0.034 [0.018–0.056]).

  **Graded companion** (p19): "The post-gate kinetic pass is a stringent per-protein binary rate,
  and its graded companion is the temporal Layer-3 informative-pass rate."

  **Attainment** (p21): "the corrected model rate minus the corrected N2 rate divided by the
  corrected N1-minus-N2 range" — the fraction of the reference-to-floor gap closed.

- **metric_saturation**: **YES, extensively, numerically, and it is one of the paper's two central
  findings.** Numeric only; axis issues are in the `hides` column of section F.
  - **Layer 1 is saturated by construction on every row.** p15: "Layer 1 (frame realism) is a
    single-frame sanity check, saturated on equilibrium MD frames and not expected to rank
    plausible generators." ED Fig. 6 (p28) shows Layer 1 = 100% saturated for all twelve rows.
  - **Layer 2 is exactly invariant to destruction of temporal order.** p3 (Fig. 1d legend):
    "Layer-2 ensemble fidelity is invariant at 0.888 (**maximum within-protein change, 0**)". p4:
    "As progressively larger blocks are permuted, ensemble fidelity remains fixed at 0.888 because
    the conformations and their frequencies are identical."
  - **Layer 2 ceilings on, and is *maximised by*, a construction with zero dynamics.** Table 1
    (p6): `Independent equilibrium samples` score **L2 = 0.99 (0.98–1.00)** — the highest L2 of any
    row, above the held-out MD replicate's **0.88 (0.85–0.91)** — while their post-gate kinetic
    pass is **0.00 (0.00–0.00)**. p4: "Frames drawn independently from the reference ensemble pass
    99% of informative ensemble tests, **exceeding the ensemble score of a held-out MD
    trajectory**, yet their post-gate kinetic pass rate is 0.00."
  - **Layer 2 is invariant under graded transition-rate perturbation.** p5: "Layer 2 remained fixed
    at 0.990 and Layer 4 within 0.003" across five nominal dynamical-speed factors (0.25× to 4×).
    ED Fig. 7b (p29): "Layer-2 ensemble fidelity remains 0.990 throughout and Layer-4 validity
    remains 0.998–1.000."
  - **Layer 2 is exactly invariant under arbitrary re-ordering of a learned ensemble.** p4: "Their
    ensemble scores were **exactly invariant**, whereas their temporal scores remained low across
    every ordering (0.065–0.158)" for BioEmu, P2DFlow and Str2Str under ten seeded permutations.
  - **Layer 4 also survives shuffling** — so geometric admissibility saturates as evidence of
    dynamics too. p3: "Layer-4 geometric and fluctuation admissibility remains 0.992–1.000" across
    the full corruption sweep.
  - **Census of saturation across all cells.** p17: "SATURATED accounts for **3,762 of the 12,760
    scored cells outside the Layer-1 sanity check (29.5%)**. On these cells the trivial surrogate
    already reaches the replicate noise floor, so the metric cannot discriminate submissions on
    that protein." Also: DATA-LIMITED = 267 scored cells (1.9%; 3.0% of the 8,998 non-saturated
    cells); MODEL-LIMITED = 1,227 of 13,791 (8.9%). The full grid is 14,319 cells (13,791 scored +
    528 NA-by-task).
  - **Saturation on small systems.** p14, WLALL pentapeptide: "**7 of its 8 Layer-3 metrics saturate
    on this simple system and are excluded**; the surviving one is time-ordered, so it is the
    kinetic gate that it carries."
  - **Not saturating**: the seven time-ordered Layer-3 metrics and the post-gate kinetic pass. They
    span 0.841 → 0.068 and 0.963 → 0.004 under the same intervention (p3–4) and recover to 0.82 /
    0.95 on an independent replicate (Table 1, p6).

- **directional_control**: **NOT APPLICABLE.** The authors instruct no generator to produce any
  state; no partner, ligand, nanobody, peptide, state-annotated template, state-filtered MSA, seed
  or subsample-depth handle is used. The only "handles" are on the *controls*: the temporal-order
  corruption fraction (0 → 1 of native adjacent frame pairs broken, p3), and the nominal
  dynamical-speed factor implemented as reversible transition operators 0.75I+0.25P, 0.5I+0.5P,
  P, P², P⁴ labelled 0.25×, 0.5×, 1×, 2×, 4× (p19). These *are* directional handles on the
  dynamics, and the paper shows Layer 3 responds monotonically to them (p5, ED Fig. 7c p29).

- **anti_memorization_design**: **PRESENT, two screens on ATLAS-82 plus one on Lockbox-36** (p20,
  p14). No time-based cutoff is used; the cutoffs are sequence-identity based.
  - Frozen protocol screen: "exact sequence matching and k-mer-Jaccard overlap (k = 3, Jaccard
    ≥ 0.3) against a combined ATLAS training profile, **flagging 4 of 82 proteins**" (p20).
  - Post hoc alignment screen: "MMseqs2 at sensitivity 7.5 searched the 82 evaluation chains
    against 1,266 ATLAS training chains. A protein is flagged when a hit reaches at least 30%
    sequence identity and at least 50% query coverage. The audit **flags 10 proteins, leaving 72
    unflagged**" (p20). Of the 72-protein shared intersection, **62 are unflagged** (p20).
  - Lockbox-36: "A post-result MMseqs2 sensitivity at 30% identity and 50% query coverage **flags 9
    of 36 proteins** against the disclosed ATLAS or mdCATH corpora" (p14).
  - Model-specific: "BioKinema … has **29 of 82** evaluation chains overlapping its training corpus
    under the model-specific screen (Supplementary Note 3)" (Table 1 footnote, p6).
  - Honest scope limit, p13: "A post hoc MMseqs2 audit … tests robustness to sequence overlap **in
    the auditable shared corpus; complete model-specific training-corpus disjointness remains
    unverified.**" p20: "An unflagged protein has no above-threshold match in the auditable
    corpus."

- **anti_memorization_control**: **RUN AND ANALYSED — not `NONE RUN`, and not `UNPOWERED`.**
  - ATLAS-82: p20, "On these same proteins the screened-minus-unscreened paired differences are
    small and **every 95% bootstrap interval includes zero**; the oracle-to-floor separation
    changes by **−0.004 (95% CI, −0.013 to 0.000)**." Restated p11 and shown as ED Fig. 4c (p26).
    n = 72 shared, 62 unflagged — powered.
  - Lockbox-36: p9, "The direction and reference separation persist **after removing nine proteins
    flagged against disclosed training corpora** and after removing each temporal metric family in
    turn." Fig. 4a (p10) shows both "All proteins (n = 36)" and "Unflagged (n = 27)" arms; MDGen
    0.59, ConfRover 0.15 on the unflagged subset. n = 27 — borderline but above ~10.
  - Caveat that keeps this short of a full control: the screens can only cover the **auditable**
    corpus (p13, p20), and BioKinema's own 29/82 overlap is reported but its scores are NR anyway.

- **controls_run**: this is the paper's most reusable content. Twenty-seven arms.

  | control | what it rules out | page |
  |---|---|---|
  | **Exact-frame temporal shuffle** of authentic MD, graded over corruption fraction 0→1, 3 fixed permutation seeds, 82 proteins | Rules out that ensemble agreement carries *any* information about temporal order. L2 invariant at 0.888 (max within-protein change 0); L3 0.841 (0.804–0.876) → 0.068 (0.049–0.088); post-gate 0.963 (0.927–1.000) → 0.004 (0.000–0.012); L4 0.992–1.000 | p3 (Fig. 1d), p4 |
  | **i.i.d. equilibrium resample** of reference frames (`iid_equilibrium`, the no-dynamics floor) | Rules out that a high ensemble score implies any temporal signal — and shows the ensemble metric *rewards* a dynamics-free construction: L2 0.99 (highest in Table 1) with post-gate 0.00 | p4, p6, p19 |
  | **Held-out real MD replicate** (`classical_md`, the oracle anchor), scored as an ordinary submission | Rules out that the temporal test is impossible to pass / that the collapse is an artefact of the metric: post-gate 0.95 (0.89–0.99), L3 0.82, L4 1.00 | p4, p6, p19 |
  | **Leave-one-replicate-out rotation** of the held-out reference (R1/R2/R3) | Rules out dependence on which replicate is the oracle: post-gate 0.951–0.976, floor stays 0.00; only 1.9% of metric-by-protein cells lack a resolvable target | p4, p17, p21, p26 (ED Fig. 4d) |
  | **Fully decoupled selection control** — distinct replicates for metric selection, reference prediction and evaluation | Rules out that informative-metric selection inflates the oracle: 0.963 decoupled vs 0.951 coupled, Δ +0.012; floor 0.00 | p17, p26 |
  | **Stationary-matched transition-rate perturbation** — reversible MSM operators 0.75I+0.25P, 0.5I+0.5P, P, P², P⁴ on an identical coordinate multiset, 5 fixed seeds, 82 proteins | Rules out that the temporal test only detects total order destruction and is blind to graded rate changes: 0.25× arm L3 +0.067 (0.046–0.090), 4× arm −0.136 (0.107–0.164); post-gate +0.085 / −0.183; L2 fixed 0.990, L4 within 0.003 | p5, p19, p29 (ED Fig. 7) |
  | **Synthetic-order stress test on unordered learned generators** — BioEmu, P2DFlow, Str2Str, first 50 frames, 10 independently seeded permutations, coordinate identity verified | Rules out that a *learned* ensemble implicitly encodes an order: ensemble scores exactly invariant, temporal 0.065–0.158 across every ordering | p4, p18, p27 (ED Fig. 5a) |
  | **Near-harmonic OU / Koopman surrogate** (`tica_ou`) | Rules out that passing relaxation statistics implies a usable trajectory: post-gate 0.38 (0.28–0.49) with L3 0.85 but L4 only 0.38 — "often leaves the region of admissible protein motion" | p6, p19 |
  | **Markov-state generator surrogate** (`msm_generative`) | Rules out that recovering coarse transitions implies ensemble quality: L2 0.81, L3 0.29, post-gate 0.32 (0.22–0.43) — "similar final scores can therefore encode different scientific outcomes" | p6, p19 |
  | **Peptide positive controls** — Timewarp AD, MDshare AD, WLALL pentapeptide (25 trajectories), CPU-only, no generative model in the loop | Rules out that the protocol simply cannot detect kinetics: replicate oracle post-gate 1.00 while shuffled floors 0.00; on WLALL the MSM and OU surrogates also reach 1.00 | p10, p14, p11 (Fig. 5a) |
  | **mdCATH-82 external replication** (320 K, 4-ns contract, held-out temperature-matched replicate) | Rules out ATLAS-specificity of the ensemble–temporal separation: held-out MD 1.00, floor 0.00, ConfRover 0.07 (exceeds floor by 0.07 [0.02–0.13], remains 0.93 below reference) | p10, p13–14, p11 (Fig. 5b) |
  | **PTM-85 external replication** (85 phosphoproteins, 3 × 10 ns) | Same, on a chemically distinct set: replicate temporal 0.87, floor 0.00 | p10, p14, p11 |
  | **Prospective Lockbox-36** — 36 proteins selected after checkpoints frozen; 3 × 200-ns CHARMM36m references; all protocol constants frozen before scoring | Rules out that the measurement was tuned to ATLAS: held-out MD 1.00, order-destroyed floor 0.00. Does **not** rule out ATLAS-specific *model ranking*: MDGen 0.58 vs ConfRover 0.11, paired difference −0.47 (95% CI −0.67 to −0.25) — a rank reversal | p9–10, p14 |
  | **Lockbox Deep-8 at 1 µs** (10 non-overlapping 100-frame windows per protein) | Rules out that short references cause the model deficit: MDGen recovers 48% of the reference-to-floor gap, ConfRover 8%; BioKinema becomes measurable (support 2.0 → 5.5 metrics, 5/15 → 15/15 reportability settings) yet passes on only 1 of 7 proteins | p9, p10 (Fig. 4b,d), p14 |
  | **Sequence-overlap screen A** — exact match + k-mer Jaccard (k=3, ≥0.3) on the frozen protocol | Rules out gross memorization under the frozen screen: flags 4 of 82 | p20 |
  | **Sequence-overlap screen B** — post hoc MMseqs2 (≥30% id, ≥50% query coverage, sensitivity 7.5, vs 1,266 ATLAS training chains) | Rules out that the separation is driven by memorized proteins: flags 10 of 82; on the 72 shared / 62 unflagged, every paired 95% interval includes zero and oracle-to-floor separation shifts by −0.004 (−0.013 to 0.000) | p11, p20, p26 (ED Fig. 4c) |
  | **Lockbox overlap screen** — post-result MMseqs2 vs disclosed ATLAS/mdCATH corpora | Rules out memorization driving the lockbox reversal: flags 9 of 36; removing them does not change the paired model direction (unflagged n = 27) | p9, p14, p10 (Fig. 4a) |
  | **Leave-one-protein-out jackknife**, all rows | Rules out a single protein driving any result: "no jackknife row moves by more than 0.014" (oracle 0.012, ConfRover 0.014, MDGen 0.012; floor and MarS-FM 0.000) | p11, p20, p26 (ED Fig. 4b) |
  | **Temporal-majority threshold sweep** {0.3, 0.4, 0.5, 0.6, 0.7} | Rules out threshold choice for the *anchors* (oracle 0.79–0.99, floor 0.00) but explicitly **fails to** rule it out for the deep models: ConfRover 0.40 → 0.03, MDGen 0.13 → 0.06, BioKinema raw 0.24 → 0.00 | p20, p26 (ED Fig. 4a) |
  | **Verdict-constant sweep**, 27 combinations of saturation tolerance × learnability tolerance × MODEL-OK ratio | Rules out constant choice for the anchor bracket (separation 0.80–1.00, floor 0.00); does **not** for model order — "at the strictest MODEL-OK ratio ConfRover and MDGen can exchange order, and BioKinema reaches the floor under the strictest kinetic-majority threshold" | p21 |
  | **Layer-4 guardrail sweep** including clash-ceiling rescale 0.25×–4× | Rules out clash-envelope choice: absolute values shift (MDGen 0.000–0.171, ConfRover 0.658–0.836) "without reordering the five ordered rows"; anchor separation invariant. Identifies the one load-bearing constant: RMSF too-cold fraction 0.3 → 0.7 drops ConfRover 0.849 → 0.452 | p21 |
  | **Reference-support / contract sensitivity grid** — 5×3 over gap 0.20–0.40 × median support 2–4, 20 i.i.d. seeds, 2,000 hierarchical bootstrap draws | Rules out that the NR classifications are threshold artefacts: ConfRover and MDGen resolved, the other three unresolved, in **all 15 settings** | p8, p18 |
  | **Reference-only temporal-resolution curve** — 12 conditions, fixed 100-ns horizon at 1/2/4/5/10/20/50 ns plus a fixed 11-frame arm, no model in the loop | Rules out that NR verdicts are model failures rather than reference limits: only the 1- and 2-ns fixed-horizon conditions meet the gap-0.30 + median-support-3 criteria; "increasing the interval without extending the trajectory eventually removes the evidence needed to distinguish intact from order-destroyed dynamics" | p8, p19, p27 (ED Fig. 5b) |
  | **Subset-bias recomputation on the 72-protein shared ID intersection** | Rules out coverage differences driving the ranking: oracle 0.972, MSM 0.361, OU 0.319, ConfRover 0.250, MDGen 0.083, floor 0.000 | p19, p21 |
  | **Metric-family leave-one-out** — remove timescale, autocorrelation, transition/MFPT or directional/VAMP as a complete group, recompute from stored verdicts | Rules out one metric family driving the lockbox direction | p9, p14 |
  | **Operational-reference sensitivity** — reroute all seven temporal metrics to the held-out replicate instead of the OU comparator | Rules out that the OU choice creates the separation: reference and floor stay 1.00 and 0.00. Does **not** stabilise intermediate models: ConfRover moves 0.25 → 0.40, MDGen stays ~0.13 — "the absolute position of an intermediate model depends on the chosen scientific ruler" | p7, p20 |
  | **S1c reference-assisted calibration diagnostic** — rescale fluctuations to an independent same-protein replicate, project virtual Cα–Cα bonds to reference length, applied symmetrically to model, N1 and N2 | Rules out attributing a geometry-gate rejection to missing temporal signal: attainment +0.093 (0.031–0.166) ConfRover, +0.244 (0.148–0.347) MDGen, interaction +0.181 (0.062–0.303) on 73 shared. 4/5 ConfRover and 17/19 MDGen rescues are Layer-4-only. Shifting the N1 arm by −0.041 is why all arms are corrected | p8, p20–21, p25 (ED Fig. 3) |
  | **DATA-LIMITED denominator sensitivity** — exclude DATA-LIMITED cells | Rules out that unresolved cells drive the model deficit: oracle 0.951 → 0.976, ConfRover 0.247 → 0.288, MSM 0.317 → 0.341, MDGen unchanged 0.134, floor 0.00. Table 1 keeps the full (stricter) denominator | p18 |
  | **Verdict-ladder order reversal** — swap the MODEL-OK and MODEL-FAILS checks | Rules out ladder ordering as an artefact: "changed no metric cell or kinetic-pass row" | p17 |
  | **Rg collapse/blow-up QC + extraction sanity check** (median Cα–Cα must sit near 3.8 Å) | Rules out adapter/unit/checkpoint errors being scored as model geometry failures; Rg is kept as a diagnostic and "never enters the verdict", so genuine collapse stays visible as a model outcome | p15, p21, p23 (ED Fig. 1b,d) |

- **confidence_as_discriminator**: **NOT USED — no pLDDT, pTM, ipTM or any model-emitted confidence
  appears anywhere in the paper.** Submissions carry only coordinates, an ordered flag and a
  physical frame interval (p15). The discriminators are all reference-calibrated: every metric is
  bracketed between a trivial floor T and an operational reference O, with the held-out MD
  replicate as the oracle (pp. 16–17). Explicit statement that a reference is not a ceiling, p16:
  "O is not a theoretical performance bound. For most kinetic metrics it is a per-mode
  near-harmonic fit …, which a richer model can in principle exceed, so a MODEL-OK verdict means
  the model matches or beats this reference, not that it has reached an upper limit."

## D. Claims

- **central_conclusion**: Agreement with an equilibrium conformational ensemble is invariant to the
  destruction of temporal order, so no ensemble-level metric can evidence that a generator learned
  dynamics; the missing signal is nevertheless measurable, because an independent MD replicate
  recovers it (post-gate kinetic pass 0.95) while shuffled frames and i.i.d. equilibrium samples do
  not (0.004 and 0.00). The authors propose Dynbench, a four-layer protocol that separates
  conformational coverage (Layer 2), time-dependent behaviour (Layer 3, seven time-ordered metrics
  bracketed by an order-destroyed floor and an MD-replicate/OU reference) and geometric and
  fluctuation admissibility (Layer 4), gated by a contract-level audit that returns NR when the
  reference itself cannot resolve the model's declared interval. Under it, generators that look
  similar on ensemble tests separate sharply — and on a prospective 36-protein lockbox the
  reference/floor bracket transfers while the model ranking reverses.

- **necessity_claims** (verbatim + page):
  - **[CENTRAL CLAIM, quoted verbatim as requested]** p1 (Abstract): *"We show that ensemble
    evidence can survive even when temporal dynamics are destroyed. Randomly reordering authentic
    MD frames leaves ensemble fidelity unchanged but reduces the post-gate kinetic pass rate from
    0.963 to 0.004; an independent MD replicate reaches 0.95 under the same test."*
  - p1 (Abstract): *"Ensemble-centred evaluation therefore systematically overstates evidence of
    learned dynamics. Claims about protein dynamics require direct temporal validation at a
    resolvable physical interval."*
  - p2: *"Ensemble tests must return the same answer; a test of dynamics must not."*
  - p2: *"Evidence from the conformational ensemble therefore survives after the detectable
    dynamics have been destroyed."*
  - p4: *"High ensemble fidelity can therefore provide strong evidence for state coverage while
    providing no evidence for dynamics."*
  - p4: *"Ensemble tests locate generated structures and estimate their populations; they do not
    identify the process that moves probability between them."*
  - p4: *"Their separation shows that the target is measurable and that equilibrium agreement is
    insufficient to reach it."*
  - p4: *"A learned state distribution can therefore retain its apparent quality under many
    incompatible temporal stories."*
  - p5: *"A post-gate kinetic pass requires both temporal evidence and an admissible trajectory."*
  - p8: *"A promising temporal statistic can therefore occur in a geometrically inadmissible
    trajectory."*
  - p12: *"Protein generators can now produce convincing collections of conformations, but a
    collection of states is not yet a model of motion."*
  - p12: *"Ensemble agreement can therefore certify the states present in an output without testing
    the process that connects them."*
  - p12 (the identifiability argument): *"The gap is a problem of identifiability: an equilibrium
    distribution does not determine the transition operator that generated it, and distinct
    pathways and rate scales can preserve the same state populations."*
  - p12 (**the scope boundary — the sentence that limits the critique**): *"Ensemble benchmarks and
    experiment-anchored population measurements remain essential because they test whether the
    relevant conformations are sampled and weighted correctly. Dynbench addresses the complementary
    question of whether generated trajectories connect those conformations with measurable temporal
    behaviour. A model must satisfy both requirements before its output can support a claim about
    protein dynamics."*
  - p12: *"Unordered generators can therefore be strong ensemble models without making a temporal
    claim. Ordered generators require a declared physical interval, reference data that resolve
    that interval and trajectories that remain admissible as they evolve."*
  - p12: *"Ensemble generators can be reported through state coverage and population agreement.
    Ordered generators additionally require a physical frame interval, reference data that retain
    temporal information and a complete trajectory that remains admissible."*
  - p13 (closing): *"Claims that a generator has learned protein dynamics should therefore require
    independent temporal evidence at a resolvable physical interval, not ensemble realism alone."*
  - p8 (impossibility, of the reference not the model): *"Some output clocks cannot support a
    kinetic claim."* / p8: *"NR identifies reference sampling that cannot support a kinetic
    estimate because intact and independently sampled references have become nearly
    indistinguishable."*
  - p17 (impossibility, of a saturated metric): *"On these cells the trivial surrogate already
    reaches the replicate noise floor, so the metric cannot discriminate submissions on that
    protein."*
  - p17 (why the OU reference is not used for transition metrics): *"a single-basin OU process
    structurally cannot represent multi-state transitions and would read DATA-LIMITED on precisely
    the proteins whose kinetics are most interesting."*

- **novelty_claims** (verbatim + page):
  - p2: *"Protein generators still lack a shared test of whether their ordered outputs reproduce a
    measurable transition process."*
  - p2: *"Together, these results establish time-resolved validation as a separate requirement for
    claims of learned protein dynamics."*
  - p22 (the explicit priority claim, against the Extended Data Table 1 capability matrix):
    *"Several methods populate the first two axes, and individual studies implement parts of the
    remaining protocol. **None combines all five protocol-level axes added by Dynbench.**"*
  - p22 (scope of the claim, same paragraph): *"The geometric-gate column records whether geometry
    gates the dynamical verdict, not whether geometry is merely reported. Str2Str defines a validity
    metric class and ConfRover reports MolProbity geometry, but neither uses geometry as a gate."*
  - p14: *"This set furnishes the strongest cross-replicate peptide oracle in the study."*
  - p15 (novelty of the clash statistic): *"This pair-normalised rate removes the strong
    chain-length dependence of the former frame-level 'any clash' fraction."*
  - p15 (framing the operationalisation as the contribution): *"Markov-state modelling distinguishes
    equilibrium agreement from kinetic validity through Chapman–Kolmogorov tests, implied-timescale
    convergence and related diagnostics. Dynbench operationalises this principle for heterogeneous
    external generators through three submission-level controls."*
  - Extended Data Table 1 (p29) is the machine-readable form of the priority claim: Dynbench is the
    only row with Yes across all seven axes; AlphaFlow, BioEmu, P2DFlow, Str2Str, MDGen, ConfRover,
    MarS-FM, ProTDyn, BioKinema, GLDP and Timewarp each score No on metric-specific calibration,
    task contract, screened shared set and public frozen board.

- **stated_limits** (authors' own):
  - p13: *"Dynbench resolves Cα-level geometry and fluctuations, primarily at 1-ns sampling over
    approximately 100 ns, with longer prospective references on a smaller set. Energetic validity,
    slower biological rates and broader model ordering require matched experimental or simulation
    support."*
  - p13: *"Because the ATLAS trajectories are public, this evaluation is not a strict hidden test."*
    and *"complete model-specific training-corpus disjointness remains unverified."*
  - p13: *"The study uses a version-frozen protocol rather than prospective preregistration;
    exploratory scoring preceded the split freeze, and later analyses are identified as post hoc."*
  - p22: *"The split, anchors and verdict rules were frozen before model promotion, but the
    alignment audit and pair-normalised clash analysis are explicitly post hoc."*
  - p9/p12: model **ranking** does not transfer — *"ConfRover's advantage is specific to ATLAS…
    Relative model performance thus depends on the protein distribution even when the temporal
    signal remains measurable."* (p9)
  - p20: *"The anchor bracket is stable, while deep-model ordering remains threshold-dependent."*
  - p21: *"Intermediate deep-model values and ordering are not invariant: at the strictest MODEL-OK
    ratio ConfRover and MDGen can exchange order."* and *"One constant is genuinely load-bearing: as
    the RMSF too-cold fraction rises from 0.3 to 0.7, ConfRover falls from 0.849 to 0.452."*
  - p17: *"It measures success under the audited contract rather than a fraction of physical
    dynamics learned."*
  - p16: *"O is not a theoretical performance bound. … a MODEL-OK verdict means the model matches or
    beats this reference, not that it has reached an upper limit."*
  - p7 (Fig. 3 legend): *"distances in this plane are descriptive and do not define a composite
    performance metric."*
  - p10: *"The mdCATH arm is a qualitative external replication under a replicate-based ruler; its
    absolute score is on a different scale from the ATLAS scorecard."*
  - p13–14: the mdCATH arm evaluates only one ConfRover contract and its training disjointness is
    unverified; PTM-85 comes from an unreleased in-house database (p31).
  - p8: ATMOS could not be scored (code/weights unavailable); Table 1 footnote §: AlphaFlow Layer 4
    not evaluated because the complete coordinate batch was unavailable (p6).
  - p19: the speed-factor labels *"index transition-operator perturbations rather than exact scaling
    of a continuous-time physical generator."*
  - p22: *"Generative AI tools (OpenAI Codex and Anthropic Claude) assisted code review, manuscript
    editing and consistency checks."*
  - p22: *"No statistical test predetermined sample size; the evaluation set is the full 82-protein
    split."*

- **stance**: **threat + background** (provisional; the user's call).
  - *threat*: the paper's argument directly constrains what may be claimed from any ensemble-level
    agreement metric. If our manuscript reports ensemble-level results and infers anything about
    interconversion, pathways or rates, this paper supplies the counter-control (p1, p4, p12–13).
    Note precisely what it threatens and what it does not — see the scope note below.
  - *background*: it also supplies the vocabulary and the boundary that *protects* an ensemble-only
    claim — p12, "Ensemble benchmarks and experiment-anchored population measurements remain
    essential because they test whether the relevant conformations are sampled and weighted
    correctly", and p18, unordered submissions "do not enter 𝒫* and the post-gate kinetic pass is
    NA by task rather than zero." A paper that reports ensemble results and claims only state
    coverage and populations is explicitly *not* attacked.

  **SCOPE NOTE — what the shuffling argument defeats and what survives it** (this is the boundary
  the extraction was asked to establish):
  - **Defeated** — anything that is a functional of the frame marginal alone, i.e. every Layer-2
    metric: free-energy-surface divergence, contact-distribution divergence, per-mode displacement
    Wasserstein distance (p15), plus the eighth order-invariant displacement Wasserstein diagnostic
    (p18). Empirically also **Layer 4** geometric/fluctuation admissibility (0.992–1.000 under full
    permutation, p3) — so "our structures are physically clean" is likewise no evidence of dynamics.
    Defeated *as evidence of learned dynamics only*.
  - **Also defeated, more strongly, by the i.i.d. arm**: the ensemble metric is not merely blind but
    anti-correlated at the top — an i.i.d. resample with zero dynamics scores L2 0.99, above real
    held-out MD's 0.88 (p6, p4). So a *higher* ensemble score is not even weak evidence of dynamics.
  - **Not defeated** — the seven time-ordered Layer-3 metrics (time-lagged autocorrelation, VAMP-2,
    implied timescales, transition matrix, mean-first-passage, directional predictability; p15,
    p18) and the post-gate kinetic pass built on them. These fall 0.841 → 0.068 and 0.963 → 0.004
    under shuffling and recover to 0.82 / 0.95 on an independent replicate (p3–4, p6). They also
    respond monotonically to graded rate perturbation at fixed ensemble (p5, ED Fig. 7).
  - **Not addressed at all** — single-structure and two-state metrics. No RMSD-to-reference,
    TM-score, lDDT or binary state-recovery predicate is tested anywhere in this paper. The
    argument formally covers *distributional ensemble* metrics; it says nothing directly about
    RMSD-to-a-deposited-state scoring of a conformational generator.
  - **Explicitly preserved** — claims about which conformations occur and at what population.
    p12: "Ensemble benchmarks and experiment-anchored population measurements remain essential."
    p4: "High ensemble fidelity can therefore provide strong evidence for state coverage while
    providing no evidence for dynamics."
  - **Generator-specificity**: the shuffling result itself is *not* generator-specific — it is
    demonstrated on authentic MD frames over 82 ATLAS proteins (Fig. 1 legend, p3: "the frozen
    cohort establishes that it is not protein-specific"), replicated on mdCATH-82, PTM-85 and three
    peptide systems (p10), and reproduced on three *learned* unordered generators under synthetic
    order (p4). What **is** generator-specific: the model ranking. ConfRover 0.25 > MDGen 0.13 on
    ATLAS-82 reverses to MDGen 0.58 > ConfRover 0.11 on Lockbox-36 (paired difference −0.47, 95% CI
    −0.67 to −0.25, p9); it also flips under the operational-reference change (ConfRover 0.25 →
    0.40, p7) and at the strictest MODEL-OK ratio (p21). The paper says so: p9, "The measurement
    therefore transfers more reliably than the ranking."

  **POSITIVE ALTERNATIVE PROPOSED — yes, and it is the most actionable content.** Dynbench, with
  four concrete, transferable components:
  1. **The bracket.** Every metric on every protein is scored against a *time-shuffled trivial
     floor* T and a *class-specific operational reference* O, with a *held-out real MD replicate*
     as the oracle and a *replicate noise floor* S; a metric is used only when the trivial
     surrogate is meaningfully worse than S (else SATURATED and dropped from the denominator).
     pp. 16–17. This is the reusable idea even outside a temporal setting: **report your metric
     next to what a destroyed-signal control scores on it.**
  2. **The seven time-ordered metrics** that survive shuffling: time-lagged autocorrelation, VAMP-2
     score, implied timescales, transition-matrix statistics, mean-first-passage, directional
     predictability (p15, p18).
  3. **The post-gate kinetic pass (`realdyn`)** — a per-protein binary requiring MODEL-OK on ≥ 0.5
     of a protein's informative temporal metrics **and** Layer-4 geometric validity; formula on
     pp. 17–18. Its graded companion is the Layer-3 informative-pass rate (p19), and its
     interpretable form is *attainment*, the fraction of the reference-to-floor gap closed (p21).
  4. **The reportability contract** — before any kinetic verdict, the reference must resolve the
     model's declared interval: oracle-minus-floor separation ≥ 0.30 with a 95% CI excluding zero,
     and median informative temporal metrics ≥ 3, else **NR** rather than a model failure (p18,
     p5). This is what converts "the model failed" into "the measurement could not be made", and
     it is what the paper uses to decline to rank BioKinema, ProTDyn and MarS-FM.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Layer-2 ensemble fidelity, intact vs fully permuted MD | 0.888 → 0.888 (max within-protein change 0) | pass fraction | reference ATLAS ensemble; 82 proteins | p3, p4 |
  | Temporal Layer 3, intact vs fully permuted MD | 0.841 (0.804–0.876) → 0.068 (0.049–0.088) | pooled informative-pass fraction | reference; 82 proteins, 3 permutation seeds | p3, p4 |
  | Post-gate kinetic pass, intact vs fully permuted MD | 0.963 (0.927–1.000) → 0.004 (0.000–0.012) | per-protein binary rate | reference; 82 proteins | p3, p4 |
  | Layer-4 admissibility under permutation | 0.992–1.000 | per-protein fraction | reference; 82 proteins | p3 |
  | Held-out MD replicate (oracle), ATLAS-82 | L2 0.88 (0.85–0.91); L3 0.82 (0.78–0.86); L4 1.00 (1.00–1.00); post-gate 0.95 (0.89–0.99) | pass fractions | reference MD, n = 82 | p6 (Table 1) |
  | Near-harmonic OU temporal surrogate | L2 0.85 (0.81–0.88); L3 0.85 (0.81–0.88); L4 0.38 (0.28–0.49); post-gate 0.38 (0.28–0.49) | pass fractions | reference MD, n = 82 | p6 |
  | Markov-state generator | L2 0.81 (0.76–0.86); L3 0.29 (0.23–0.36); L4 1.00; post-gate 0.32 (0.22–0.43) | pass fractions | reference MD, n = 82 | p6 |
  | Independent equilibrium samples (i.i.d. floor) | L2 0.99 (0.98–1.00); L3 0.00; L4 1.00; post-gate 0.00 (0.00–0.00) | pass fractions | reference MD, n = 82 | p6 |
  | ConfRover, ATLAS-82 (1 ns, resolved) | L2 0.49 (0.45–0.54); L3 0.30 (0.26–0.35); L4 0.78 (0.67–0.88); post-gate 0.25 (0.15–0.36) | pass fractions | reference MD, n = 73 | p6, p8 |
  | MDGen, ATLAS-82 (1 ns, resolved) | L2 0.21 (0.17–0.24); L3 0.64 (0.60–0.69); L4 0.15 (0.07–0.22); post-gate 0.13 (0.06–0.21) | pass fractions | reference MD, n = 82 | p6, p8 |
  | BioKinema, ATLAS-82 (10 ns, range-limited) | L2 0.64 (0.60–0.68); L3 0.13 (0.08–0.18)‡; L4 1.00; post-gate **NR** (raw 0.06) | pass fractions | reference MD, n = 81; 29/82 training overlap | p6, p24 |
  | ProTDyn, ATLAS-82 (10 ns, range-limited) | L2 0.15 (0.12–0.18); L3 0.24 (0.17–0.31)‡; L4 0.04 (0.00–0.10); post-gate **NR** (raw 0.01) | pass fractions | reference MD, n = 74 | p6, p16, p24 |
  | MarS-FM, ATLAS-82 (~50 ns, support-limited) | L2 0.09 (0.07–0.11); L3 0.29 (0.22–0.37)‡; L4 0.00 (0.00–0.00); post-gate **NR** (raw 0.00) | pass fractions | reference MD, n = 82 | p6, p24 |
  | AlphaFlow (unordered) | L2 0.64 (0.57–0.69); L3 NA; L4 NR; post-gate NA | pass fraction | reference MD, n = 82 | p6 |
  | P2DFlow (unordered) | L2 0.68 (0.61–0.75); L4 0.92 (0.85–0.99); post-gate NA | pass fractions | reference MD, n = 65 | p6, p7 |
  | BioEmu (unordered) | L2 0.48 (0.42–0.54); L4 0.71 (0.61–0.82); post-gate NA | pass fractions | reference MD, n = 82 | p6 |
  | Str2Str (unordered) | L2 0.22 (0.19–0.25); L4 0.16 (0.09–0.24); post-gate NA | pass fractions | reference MD, n = 82 | p6 |
  | Learned ensembles under 10 synthetic orders | L2 exactly invariant; L3 0.065–0.158 | pass fractions | BioEmu n=81, P2DFlow n=65, Str2Str n=82; 50 frames each | p4, p27 |
  | Transition-rate perturbation, 0.25× arm | L3 +0.067 (0.046–0.090); post-gate +0.085 (0.046–0.129) | change in pass fraction | fitted 1× chain; 82 proteins, 5 seeds | p5, p29 |
  | Transition-rate perturbation, 4× arm | L3 −0.136 (0.107–0.164); post-gate −0.183 (0.239–0.124) | change in pass fraction | fitted 1× chain; 82 proteins, 5 seeds | p5, p29 |
  | Ensemble/geometry stability under rate perturbation | L2 fixed 0.990; L4 0.998–1.000 | pass fractions | same coordinate multiset | p5, p29 |
  | Lockbox-36 (Broad, 200 ns) | held-out MD 1.00; i.i.d. floor 0.00; MDGen 0.58; ConfRover 0.11; paired difference −0.47 (−0.67 to −0.25) | post-gate kinetic pass rate | own CHARMM36m references, n = 36 | p9, p10 |
  | Lockbox-36, unflagged subset | MDGen 0.59; ConfRover 0.15 | post-gate kinetic pass rate | n = 27 | p10 (Fig. 4a) |
  | Lockbox-36 component split | temporal majority: MDGen 0.78, ConfRover 0.31; geometric valid: 0.69 / 0.36; post-gate 0.58 / 0.11 | fraction of proteins | n = 36 | p10 (Fig. 4c) |
  | Lockbox Deep-8 (1 µs references) | MDGen 48%, ConfRover 8% | fraction of reference-to-floor gap closed | n = 8, 10 windows each | p9, p10 |
  | BioEmu on Lockbox-36 | 0.813, no temporal result | ensemble fidelity | n = 36 | p9 |
  | BioKinema with 1-µs references | reference frames 21 → 101; informative metrics 2.0 → 5.5; resolved grid 5/15 → 15/15; passes 1 of 7 proteins | mixed | Deep-8 | p9, p10 |
  | mdCATH-82 external arm | held-out MD 1.00; ConfRover 0.07 (exceeds floor by 0.07 [0.02–0.13]); floor 0.00 | post-gate kinetic pass rate | 82 CATH domains, 320 K, 4-ns contract | p10 |
  | PTM-85 external arm | replicate 0.87; floor 0.00 | temporal Layer-3 pass fraction | 85 phosphoproteins | p10, p11 |
  | Peptide positive controls | Timewarp AD replicate oracle 0.67; MDshare AD 1.00; WLALL 1.00; all i.i.d. floors 0.00 | Layer-3 pass fraction / post-gate 1.00 | held-out peptide trajectories | p10, p11, p14 |
  | Alternative-ruler sensitivity (all 7 temporal metrics → held-out replicate) | reference 1.00, floor 0.00; ConfRover 0.25 → 0.40; MDGen ≈ 0.13 | post-gate kinetic pass rate | n = 73 / 82 | p7 |
  | Oracle replicate rotation | 0.951 / 0.976 / 0.976; floor 0.00 | post-gate kinetic pass rate | 82 proteins | p4, p21, p26 |
  | Selection decoupling | 0.963 decoupled vs 0.951 coupled (Δ +0.012) | post-gate kinetic pass rate | 82 proteins | p17, p26 |
  | 72-protein shared-ID recomputation | oracle 0.972; MSM 0.361; OU 0.319; ConfRover 0.250; MDGen 0.083; floor 0.000 | post-gate kinetic pass rate | n = 72 | p19 |
  | Threshold sweep {0.3–0.7} | oracle 0.79–0.99; floor 0.00; ConfRover 0.40 → 0.03; MDGen 0.13 → 0.06 | post-gate kinetic pass rate | 82 proteins | p20, p26 |
  | Leave-one-protein-out jackknife | max swing 0.014 (oracle 0.012, ConfRover 0.014, MDGen 0.012) | post-gate kinetic pass rate | 82 proteins | p20, p26 |
  | Alignment-screen effect | oracle-to-floor separation change −0.004 (−0.013 to 0.000); all paired CIs include zero | post-gate kinetic pass rate | 72 shared, 62 unflagged | p11, p20 |
  | S1c calibration attainment gain | ConfRover +0.093 (0.031–0.166); MDGen +0.244 (0.148–0.347); interaction +0.181 (0.062–0.303) | fraction of N1–N2 gap closed | n = 73 shared | p8, p25 |
  | S1c rescue mechanism | 4/5 ConfRover and 17/19 MDGen rescues are Layer-4-only | count | n = 73 / 82 | p8, p25 |
  | DATA-LIMITED exclusion sensitivity | oracle 0.951 → 0.976; ConfRover 0.247 → 0.288; MSM 0.317 → 0.341; MDGen 0.134 unchanged; floor 0.00 | post-gate kinetic pass rate | 82 proteins | p18 |
  | Verdict census | 13,791 scored cells (+528 NA = 14,319 grid); SATURATED 3,762 of 12,760 (29.5%); DATA-LIMITED 267 (1.9% scored, 3.0% non-saturated); MODEL-LIMITED 1,227 (8.9%) | metric-by-protein cells | whole scorecard | p17 |
  | Contract-audit separations | ConfRover 0.956 (0.903–0.996), MDGen 0.921 (0.859–0.971) at 1 ns; BioKinema 0.053 (0.032–0.076), ProTDyn 0.058 (0.036–0.085) at 10 ns; MarS-FM 0.034 (0.018–0.056) at ~50 ns | oracle-minus-floor separation | criterion ≥ 0.30 | p18 |
  | Layer-4 validity by model | ConfRover 78%; BioKinema 100%; MDGen 15%; MarS-FM 0%; ProTDyn 4% (3 of 74) | fraction of scored proteins | reference envelope + absolute ceiling | p9, p16, p23 |
  | MarS-FM global expansion | expands on 74 of 82 proteins; median Rg ratio 5.42 | ratio | reference MD | p9 |
  | Clash-ceiling calibration | absolute ceiling 0.000758 = 2 × max over 246 reference replicates; per-protein reference max +50%, larger bound used | non-adjacent Cα pairs < 4 Å per eligible frame-pair | ATLAS reference replicates | p15 |
  | RMSF guardrail | fails below 0.5× min or above 2.0× max reference | ratio | reference replicates | p15 |
  | Load-bearing constant | RMSF too-cold fraction 0.3 → 0.7 drops ConfRover Layer-4 validity 0.849 → 0.452; BioKinema stays > 0.92 | fraction | guardrail sweep | p21 |
  | Clash-ceiling rescale 0.25×–4× | MDGen 0.000–0.171; ConfRover 0.658–0.836; no reordering of the five ordered rows | post-gate kinetic pass rate | 82 proteins | p21 |
  | Verdict-constant sweep (27 combos) | oracle-to-floor separation 0.80–1.00; floor 0.00 | post-gate kinetic pass rate | 82 proteins | p21 |

- **n_predictions**:
  - *Targets*: 82 ATLAS chains (frozen split), with model coverage 73 (ConfRover), 74 (ProTDyn), 65
    (P2DFlow), 81 (BioKinema), 82 (others); 72-protein shared intersection for cross-model
    comparison (p13, p19). Plus 36 Lockbox (8 Deep), 82 mdCATH, 85 PTM, 3 peptide systems.
  - *Samples per target*: reference ATLAS = 3 independent 100-ns replicas saved every 10 ps,
    subsampled to 1-ns spacing → **101 frames** per replica in the anchor ladder (p13, p19). Deep
    models keep their native interval and rollout length (p13). The synthetic-order stress test
    uses **50 frames** per protein × **10 permutation seeds** (p18). Fig. 1d averages **3 fixed
    permutation seeds** per protein per corruption level (p3). The rate-perturbation control uses
    **5 fixed seeds** × 5 arms (p19). i.i.d. floors use **20 seeds** (p14, p18, p21). Lockbox
    Broad uses the first **100 aligned frames**; Deep averages **10 non-overlapping 100-frame
    windows** per protein (p14). mdCATH: ConfRover submits **110 frames** at 4 ns; references
    110–113 frames (p14).
  - *Total scale*: **13,791 scored metric-by-protein cells**, 528 NA-by-task, **14,319-cell grid**
    (p17). Bootstrap: 1,000 protein-cluster resamples for the scorecard (seed 0), 2,000 for the
    Fig. 1d ablation, sequence-overlap sensitivity, Lockbox and the reference audits (p18, p21).
  - No generator is run by the authors, so there is no per-target sampling budget in the usual
    sense; the only "samples" the authors generate are MD frames and control permutations/seeds.

- **comparable_to_ours**: *(left empty by the extractor per v3)*

- **si_in_scope**: **SI NOT HELD — partially.** Extended Data Figs. 1–7 and Extended Data Table 1
  are inside the PDF (pp. 23–29) and are fully extracted below. **Supplementary Notes 1–12 and
  Supplementary Table S7 are cited but absent.** Load-bearing content that is therefore not
  checkable from the held PDF: Note 1 (the per-axis justification behind the Extended Data Table 1
  capability matrix, i.e. the entire priority claim, p22, p29); Note 2 (ProTDyn's NR
  classification, p16); Note 3 (BioKinema's 29/82 training-corpus overlap, p6); Note 6 (Layer-4
  guardrail sweep, p21); Note 9 (the synthetic-order stress test's effect on production labels,
  p18); Note 10 (the reference-only temporal-resolution grid, p19); Note 12 (the stationary-matched
  perturbation control, p19); Table S7 ("Later methods are catalogued in Supplementary Table S7",
  p29). Source data are stated to be provided with the paper and in the Zenodo archive (p10, p27,
  p28, p31), neither of which is held.

## F. Figures

**Reuse licence for every row**: **CC-BY 4.0 International**, stated on the bioRxiv banner of every
page including p1 — "It is made available under a CC-BY 4.0 International license." **No ND
clause**; redrawing and modification are permitted with attribution. Code is MIT (p31). Where a
figure says "Source data are provided with this paper" (Figs. 4, ED 5, ED 6), the source data are
in the Zenodo archive under reserved DOI 10.5281/zenodo.22146996, public at publication (p31) —
not held.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 3 | One ATLAS protein (5ftw_A, 256 res) as a Cα backbone coloured by per-residue RMSF, mobile region fanning into overlaid frames | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: NOT REPORTED predictions on 1 reference \| axis: none` (a continuous RMSF colour ramp 2–8 Å is annotated but carries no data axis) | 1 panel, single system, single view | | CC-BY 4.0, p1 banner; no ND |
| 1B-C | 3 | The same trajectory on its TICA free-energy landscape, threading basins in time order (b), and the identical frames with order shuffled (c) | scatter on density | `PLOT \| facet: frame ordering (2: time-ordered, shuffled) \| vary: TICA 1 (continuous) \| series: trajectory time, 0–100 frames (continuous colour, panel b only) \| measure: TICA 2 \| mark: point on free-energy density \| n: 1 per mark; ~100 frames per panel, 1 protein` | 2 panels sharing one landscape and one frame set; differ only by ordering | Panel c has no colour series (order destroyed), so the two panels are not colour-comparable; density scale unlabelled | CC-BY 4.0, p1; no ND |
| 1D | 3 | Controlled temporal-order corruption across all 82 frozen proteins: L2 flat, L3 and post-gate kinetic pass collapse | line | `PLOT \| facet: none (1) \| vary: temporal-order corruption, fraction of native adjacent frame pairs broken, 0–1 (continuous) \| series: score type (3: Layer-2 ensemble, Layer-3 temporal, post-gate kinetic pass) \| measure: fraction passing \| mark: line with 95% bootstrap shading \| n: 82 proteins per point, 3 fixed permutation seeds averaged within protein, 2,000 bootstrap resamples` | 1 panel, 3 series; L4 (0.992–1.000) is stated in the legend but **not plotted** | The fourth layer's invariance — arguably as important as L2's, since it shows geometric admissibility is also order-blind — is given only as legend text with no line | CC-BY 4.0, p1; no ND |
| 2 | 5 | Dynbench decision flow: output claim → temporal measurability → the evidence each supports | schematic | `SCHEMATIC \| three-stage decision flow from output contract (unordered vs ordered with declared interval) through reference-vs-floor resolvability to the four-layer verdict and the post-gate gate \| no data` | 3 panels (a, b, c); caption itself states "Schematic; no data" | | CC-BY 4.0, p1; no ND |
| T1 | 6 | The ATLAS-82 scorecard: 12 rows (4 anchors/comparators, 5 ordered models, 4 unordered models — AlphaFlow appears among unordered) × 4 score columns with 95% bootstrap CIs | table | `MATRIX \| rows: model/anchor (12) \| cols: score (4: L2 ensemble, L3 temporal, L4 valid, post-gate kinetic pass) + n \| value: pass fraction with 95% bootstrap CI, or NA/NR \| facet: contract class (4: reference controls, resolved ordered, insufficient-support ordered, unordered)` | single table, 4 grouped row-blocks | | CC-BY 4.0, p1; no ND |
| 3A | 7 | Ensemble fidelity vs post-gate kinetic pass for anchors, comparators and the two resolved ordered models; the i.i.d. floor sits at (0.99, 0.00) and the replicate oracle at (0.88, 0.95) | scatter | `PLOT \| facet: none (1) \| vary: ensemble fidelity L2, 0–1 (continuous) \| series: model class (2: kinetically scored (6 points), ensemble-only rail (4 points)) \| measure: post-gate kinetic pass rate \| mark: point with 95% protein-bootstrap error bars \| n: 65–82 proteins per point (labelled per model); 1 point per model` | 1 panel plus a separate "ensemble-only" rail below the axes for AlphaFlow, P2DFlow, BioEmu, Str2Str | The four unordered models are placed on a rail *outside* the plotting plane with no vertical position, which is honest (their post-gate is NA) but makes them visually incomparable; the legend has to state "distances in this plane are descriptive and do not define a composite performance metric" | CC-BY 4.0, p1; no ND |
| 3B | 7 | Per-model temporal, geometric and post-gate results for five ordered contracts at their stated intervals | bar | `PLOT \| facet: model (5: ConfRover, MDGen, BioKinema, ProTDyn, MarS-FM) \| vary: quantity (3: native-task L3 pre-gate, L4 valid, post-gate pass if resolved) \| series: none (1) \| measure: fraction \| mark: bar with printed value \| n: 73, 82, 81, 74, 82 proteins respectively` | 5 stacked sub-panels, each annotated with its interval and resolution status | Three of five models show "NR" in place of a bar, so the panel is 40% populated; y-axis is truncated at 0.6 in each sub-panel, cutting off nothing observed but making the printed values do the work | CC-BY 4.0, p1; no ND |
| 4A | 10 | Lockbox-36 post-gate pass for ConfRover and MDGen on all 36 and on the 27 unflagged proteins, with held-out MD and i.i.d. anchors as dashed lines | line + point | `PLOT \| facet: none (1) \| vary: protein subset (2: all n=36, unflagged n=27) \| series: row (4: held-out MD, MDGen, ConfRover, i.i.d. floor) \| measure: post-gate kinetic pass rate \| mark: point with 95% protein-bootstrap error bars joined by line \| n: 36 and 27 proteins per point, 2,000 bootstrap draws` | 1 panel, 2 x-positions, 4 series (2 as dashed reference lines) | Only two x-positions, so the connecting lines imply a trend across a nominal 2-level variable; the two anchors are dashed lines without error bars | CC-BY 4.0, p1; no ND (source data in Zenodo, not held) |
| 4B | 10 | Fraction of the reference-to-floor gap closed on the Deep-8 subset after extending all three replicates to 1 µs | dot plot with range | `PLOT \| facet: none (1) \| vary: model (2: ConfRover, MDGen) \| series: none (1) \| measure: fraction of reference-to-floor gap closed, 0–1 \| mark: point with horizontal range \| n: 8 proteins × 10 non-overlapping 100-frame windows per point` | 1 panel, 2 rows, transposed (measure runs horizontally) | | CC-BY 4.0, p1; no ND |
| 4C | 10 | The lockbox reversal decomposed into temporal majority, geometric validity and post-gate pass | slope plot | `PLOT \| facet: none (1) \| vary: scorecard component (3: temporal majority, geometric valid, post-gate pass) \| series: model (2) \| measure: fraction of proteins \| mark: point joined by line, values printed \| n: 36 proteins per point` | 1 panel, 3 x-positions, 2 series | Lines join three non-ordinal categories, implying a progression that does not exist | CC-BY 4.0, p1; no ND |
| 4D | 10 | BioKinema's reportability under 200-ns vs 1-µs references: reference frames, informative metrics, resolved grid, verdict | paired dot / dumbbell | `PLOT \| facet: reported quantity (4: reference frames, informative metrics, resolved grid, verdict) \| vary: reference depth (2: Broad 200 ns, Deep 1 µs) \| series: none (1) \| measure: quantity-specific value (21→101 frames; 2.0→5.5 metrics; 5/15→15/15 settings; NR→reportable) \| mark: point pair joined by connector \| n: 36 evaluable → 32/36, and 8 → 7/8` | 1 panel, 4 rows of mixed units | Four different units share one horizontal layout with no axis at all; the "verdict" row is categorical (NR → reportable) plotted in the same visual grammar as counts | CC-BY 4.0, p1; no ND |
| 5A-B | 11 | Temporal Layer-3 pass fraction for four anchor rows on three peptide systems (a) and three protein datasets (b), with L4 validity printed at right in b | bar | `PLOT \| facet: dataset (6: Timewarp AD, MDshare AD, WLALL, ATLAS-82, mdCATH-82, PTM-85) \| vary: anchor row (4: replicate oracle, OU surrogate, MSM surrogate, i.i.d. floor) \| series: none (1) \| measure: temporal Layer-3 pass fraction \| mark: horizontal bar with printed value \| n: 82 / 82 / 85 proteins; 2 or 25 trajectories for peptides` | 6 facets in 2 groups (a peptides, b proteins); panel b additionally prints an L4-valid column as text, not as a mark | Panel b's L4 column is text beside the bars rather than a second encoded measure, so the reader cannot compare it visually; peptide and protein panels use different observables (heavy-atom distances vs Cα) on a shared axis label | CC-BY 4.0, p1; no ND |
| 5C | 11 | Specificity control: the same i.i.d. samples pass ensemble tests on every dataset but fail the temporal test, whereas the oracle retains both | bar | `PLOT \| facet: dataset (3: ATLAS-82, mdCATH-82, PTM-85) \| vary: none (1) \| series: score (3: i.i.d. ensemble, i.i.d. temporal, oracle temporal) \| measure: pass rate \| mark: horizontal bar with printed value \| n: 82 / 82 / 85 proteins` | 3 facets, 3 series each; the i.i.d.-temporal series is annotated "fails diagnostic" rather than drawn at 0 | The i.i.d.-temporal bars are replaced by the words "fails diagnostic", so the single most important comparison in the paper's specificity control has no drawn quantity — the zero is a label, not a mark | CC-BY 4.0, p1; no ND |
| ED1A+D | 23 | Layer-4 status composition per ordered model (a) and the fraction of proteins with global Rg failure (d) | stacked bar / bar | `PLOT \| facet: analysis (2: L4 status composition, global size failure) \| vary: model (5) \| series: status (a: 4 levels VALID, INVALID_GEOMETRY, TOO_COLD, TOO_HOT/DIVERGED; d: 2 failure modes Rg>2×, Rg<0.5×) \| measure: fraction of scored proteins \| mark: bar \| n: 73, 81, 82, 82, 74 proteins per row` | 2 panels (a and d), 5 model rows each; BioKinema marked "not recorded" in d | BioKinema's auxiliary distributions were never recorded, leaving a hole labelled "not recorded" in b–d | CC-BY 4.0, p1; no ND |
| ED1B | 23 | Per-protein radius-of-gyration ratio relative to reference MD, with collapse/blow-up bands shaded | strip + summary | `PLOT \| facet: none (1) \| vary: model (5) \| series: none (1) \| measure: model / reference Rg (log axis 0.1–10) \| mark: point per protein plus an open median marker with range \| n: 1 per point; 73, 81, 82, 82, 74 proteins per row (BioKinema not recorded)` | 1 panel, 5 rows, transposed | Log x-axis without gridlines; BioKinema row empty | CC-BY 4.0, p1; no ND |
| ED1C | 23 | Per-protein fraction of virtual Cα–Cα bonds within the accepted band | strip + summary | `PLOT \| facet: none (1) \| vary: model (5) \| series: none (1) \| measure: fraction of Cα–Cα bonds in band, 0–1 \| mark: point per protein plus an open median marker with range \| n: 1 per point; 73, 82, 82, 74 proteins per row (BioKinema not recorded)` | 1 panel, 5 rows, transposed | BioKinema row empty | CC-BY 4.0, p1; no ND |
| ED2 | 24 | Per-protein Layer-3 pass fraction for all nine kinetically scored rows, filled where Layer-4 valid and hollow where gated out, with the 0.5 majority cut drawn | strip / point cloud | `PLOT \| facet: none (1) \| vary: model/anchor (9) \| series: Layer-4 status (2: valid filled, invalid hollow) \| measure: per-protein Layer-3 informative-pass fraction, 0–1 \| mark: point, one per protein, with a 0.5 reference line \| n: 1 per mark; 65–82 proteins per column` | 1 panel, 9 columns, with post-gate values (or NR + raw) printed beneath each | Native output intervals differ between columns, so the columns are not on a common temporal resolution — stated in the legend but not encoded | CC-BY 4.0, p1; no ND |
| ED3A | 25 | Attainment before and after S1c reference-assisted calibration for ConfRover and MDGen | slope plot | `PLOT \| facet: none (1) \| vary: calibration state (2: uncorrected, S1c) \| series: model (2) \| measure: attainment, fraction of anchor gap closed \| mark: point joined by line \| n: 73 (ConfRover) and 82 (MDGen) proteins, 20 N2 seeds, 2,000 bootstrap draws` | 1 panel, 2 x-positions, 2 series | Paired CIs are printed as text next to the lines rather than drawn | CC-BY 4.0, p1; no ND |
| ED3B | 25 | How calibration shifts each arm (model, N1 oracle, N2 floor) separately | dot plot with CI | `PLOT \| facet: none (1) \| vary: arm (3: model, N1 oracle, N2 floor) \| series: none (1) \| measure: change in post-gate pass rate, −0.1 to +0.3 \| mark: point with 95% CI \| n: 73 shared proteins, 20 seeds, 2,000 draws` | 1 panel, 3 rows, transposed | | CC-BY 4.0, p1; no ND |
| ED3C | 25 | Source of each post-gate verdict change: Layer-4-only, Layer-3-only, both, or lost | stacked bar | `PLOT \| facet: none (1) \| vary: model (2) \| series: rescue source (4: Layer 4 only, Layer 3 only, both layers, lost) \| measure: count of proteins whose post-gate verdict changed, 0–30 \| mark: stacked bar \| n: 73 (ConfRover) and 82 (MDGen) proteins` | 1 panel, 2 rows, transposed | | CC-BY 4.0, p1; no ND |
| ED4A | 26 | Raw post-gate pass rate as the temporal-majority threshold sweeps 0.3–0.7, for nine rows | line | `PLOT \| facet: none (1) \| vary: majority threshold, 0.3–0.7 (continuous, 5 levels) \| series: model/anchor (9) \| measure: raw post-gate pass rate \| mark: line \| n: 82 proteins per point` | 1 panel, 9 lines, only 5 labelled in the legend | Nine overplotted lines with five legend entries; individual model traces are not separable in the middle of the range | CC-BY 4.0, p1; no ND |
| ED4B+D | 26 | Leave-one-protein-out jackknife rates with max swing per row (b), and the oracle-choice / selection-coupling comparison (d) | bar | `PLOT \| facet: analysis (2: jackknife, oracle choice & selection coupling) \| vary: row (b: 9 models/anchors; d: 5 conditions — replicates R1/R2/R3, coupled, decoupled) \| series: none (1) \| measure: raw post-gate kinetic pass rate (with a paired deviation strip in b, −0.02 to +0.02) \| mark: bar with printed value \| n: 82 proteins; 1,000–2,000 bootstrap draws` | 2 panels; panel b pairs each bar with a deviation strip, so letter b contributes two shapes and is recorded here under its bar shape | Panel d's axis is zoomed to 0.94–1.00, which magnifies a Δ of 0.012 into a visually large difference — the truncation is labelled "zoomed" but not broken-axis marked | CC-BY 4.0, p1; no ND |
| ED4C | 26 | Paired difference in raw pass rate from the alignment-based sequence-overlap screen, for nine rows | dot plot with CI | `PLOT \| facet: none (1) \| vary: model/anchor (9) \| series: none (1) \| measure: change in raw pass rate (screened − full), −0.08 to +0.08 \| mark: point with 95% CI \| n: 72 shared proteins, 62 unflagged` | 1 panel, 9 rows, transposed | | CC-BY 4.0, p1; no ND |
| ED5A | 27 | Fixed 50-frame outputs from three unordered generators under 10 seeded synthetic orders: Layer 2 invariant, Layer 3 low across every order | dot plot with range | `PLOT \| facet: generator (3: BioEmu, P2DFlow, Str2Str) \| vary: informative-pass fraction, 0–0.75 (continuous) \| series: layer (2: Layer 2 as square (invariant), temporal Layer 3 as circle with range) \| measure: informative-pass fraction \| mark: point (square/circle) with horizontal range \| n: 81, 65, 82 proteins; 50 frames × 10 seeds each` | 3 facets, 2 series each; transposed (measure horizontal) | Layer 2 is drawn as a single square because it is exactly invariant — correct, but a reader cannot tell an exact invariance from an unreported range | CC-BY 4.0, p1; no ND (source data in Zenodo, not held) |
| ED5B | 27 | Reference-only temporal-support audit: reference-minus-floor gap vs sampling interval, under a fixed 100-ns horizon and a fixed 11-frame support | scatter with error bars | `PLOT \| facet: none (1) \| vary: sampling interval, 1–50 ns (continuous, log-spaced, 7 levels) \| series: audit arm (2: fixed 100-ns horizon, fixed 11-frame support) \| measure: reference minus shuffled-floor gap, 0–1 \| mark: point with 95% interval, filled when it meets gap 0.30 and median support 3, labelled with retained frame count \| n: 82 proteins, 20 floor seeds, 2,000 hierarchical bootstrap draws` | 1 panel, 2 series, 12 conditions | | CC-BY 4.0, p1; no ND (source data in Zenodo, not held) |
| ED6 | 28 | Verdict composition (MODEL-OK / MODEL-LIMITED / MODEL-FAILS / DATA-LIMITED / SATURATED) within Layers 1, 2 and 3 for all twelve rows | stacked bar | `PLOT \| facet: layer (3: L1 frame, L2 ensemble, L3 temporal) \| vary: model/anchor (12) \| series: verdict (5) \| measure: percentage of classified cells in that model and layer \| mark: stacked bar with printed percentages \| n: 13,791 scored cells in total; per-row n not printed` | 3 facets × 12 rows, grouped into anchors / ordered deep / ensemble deep | Per-cell n behind each bar is not shown, so a 36% SATURATED share on one row and another are not weight-comparable; percentages "rounded and may sum to 100 ± 1" | CC-BY 4.0, p1; no ND (source data in Zenodo, not held) |
| ED7A | 29 | The transition-rate intervention actually changes transitions: fraction of adjacent frames changing microstate rises across the five operator arms | line | `PLOT \| facet: none (1) \| vary: nominal dynamical-speed factor (5: 0.25×, 0.5×, 1×, 2×, 4×) \| series: none (1) \| measure: fraction of adjacent frames changing state, 0.2–0.61 \| mark: line with 95% protein-bootstrap shading \| n: 82 proteins × 5 fixed seeds, 2,000 resamples` | 1 panel | | CC-BY 4.0, p1; no ND |
| ED7B-C | 29 | Ensemble and geometry stay fixed across all five arms (b) while temporal Layer 3 and post-gate pass respond monotonically (c) | line | `PLOT \| facet: score family (2: invariant (L2, L4), responsive (temporal L3, post-gate)) \| vary: nominal dynamical-speed factor (5: 0.25×–4×) \| series: score (b: 2, c: 2) \| measure: fraction passing \| mark: line with 95% protein-bootstrap shading \| n: 82 proteins × 5 fixed seeds, 2,000 resamples` | 2 panels; b and c differ only in which scores are drawn | **Panel b's y-axis runs 0.96–1.00 while panel c's runs 0.4–0.9** — the invariance and the response are shown on incomparable, truncated scales, which visually equalises a flat 0.990 line with a 0.2-wide swing | CC-BY 4.0, p1; no ND |
| EDT1 | 29 | Capability matrix: what each prior method's own paper evaluated across the seven axes Dynbench formalises | table | `MATRIX \| rows: method (12: AlphaFlow, BioEmu, P2DFlow, GLDP, Str2Str, MDGen, ConfRover, MarS-FM, ProTDyn, BioKinema, Timewarp, Dynbench) \| cols: capability axis (7: ensemble, temporal, metric-specific calibration, geometry gate, task contract, shared set screened for overlap, public frozen board) \| value: Yes / Partial / No \| facet: none (1)` | single table | Every cell is the authors' own reading of someone else's paper, justified only in Supplementary Note 1, which is not in the held PDF — the priority claim rests on an unverifiable table | CC-BY 4.0, p1; no ND |

## G. Provenance

- **extracted_on**: 2026-09-07 (per `BATCH_PROMPT.md`; the session date is 2026-09-08 — flagged in
  `unresolved`).
- **extractor**: claude subagent (Opus 5), single-paper extraction against SCHEMA.md v3.
- **schema_version**: **v3**
- **confidence**: **high** for text, claims, controls, methods constants and Table 1 (all read from
  `pdftotext -layout` with page markers, cross-checked against the Results prose). **Medium** for a
  few figure-panel details: numeric values inside Figs. 3b, 4a–d, 5a–c and ED Figs. 1–7 were read
  from the `-layout` text stream, which preserves the printed data labels but not always their
  panel assignment; I rendered **two pages (10 and 23)** at 110 dpi to confirm mark types and
  panel structure for Fig. 4 and ED Fig. 1, and took the rest from captions plus the layout stream.
  Hardest to read: ED Fig. 6's per-row percentages (the layout stream gives the numbers but not
  reliably which segment each belongs to) and Fig. 3b's sub-panel axis ranges.
- **unresolved**:
  1. **Tag I wanted and did not use: `multi-backbone`.** Nine conformational generators are
     compared head to head, which literally satisfies the v3 rule ("If more than two are compared
     head to head, tag `multi-backbone`"). But the `backbones` field enumerates structure-prediction
     backbones (AF2, AF3, Boltz, Chai, OF3, Protenix) and **none** appears here. Applying the tag
     would return this paper for every "which papers compare co-folding backbones" query, so I
     declined. **v3 needs either a separate tag for multi-generator benchmarks or an explicit note
     that `multi-backbone` covers any head-to-head model comparison.**
  2. `extracted_on` — `BATCH_PROMPT.md` and the task both specify 2026-09-07, but today is
     2026-09-08. I used 2026-09-07 as instructed.
  3. **Starting structures for the 36 Lockbox simulations are never stated** (p14 gives the force
     field, water model, salt and length, but not the source of the initial coordinates). This
     matters for `structural_priors_used` and I could not resolve it.
  4. **Supplementary Notes 1–12 and Table S7 are not held.** Note 1 carries the entire
     justification for the Extended Data Table 1 capability matrix, i.e. the paper's priority
     claim (p22, p29); Notes 2, 3, 6, 9, 10 and 12 carry the ProTDyn NR classification, BioKinema's
     29/82 training overlap, the Layer-4 guardrail sweep, the synthetic-order test's label
     handling, the resolution grid and the perturbation control. None is checkable here.
  5. **`state_metric` is a poor fit for this paper and I recorded it as dual.** The paper's
     discriminator is neither an RMSD-to-reference nor a state predicate: it is a *bracketed verdict
     ladder* — a continuous per-metric closure c_M relative to a floor and an operational
     reference, then thresholded into five categories, then majority-voted into a per-protein
     binary. v3 has no vocabulary for "metric scored relative to a destroyed-signal control", which
     is exactly the construct our manuscript would need to borrow. Suggest v4 add a
     `floor_referenced` value or a `control_referenced_metric` tag.
  6. **`states_generated` had no honest single value for a benchmark paper.** I wrote
     `ensemble + continuum` on the grounds that the authors do generate MD trajectories and control
     ensembles, but the field is really asking about a generator's output and this paper is not a
     generator. v3's `NOT APPLICABLE — equilibrium displaced` escape hatch exists for wet-lab
     papers; there is no equivalent for benchmark-only papers.
  7. **`metric_saturation` vs `hides` boundary was easy here but the `hides` column got crowded.**
     ED Fig. 7b/c use two different truncated y-axes (0.96–1.00 vs 0.4–0.9) to show an invariance
     next to a response — a figure defect, recorded in `hides` per v3 rule 9. The *numeric*
     invariance is in `metric_saturation`. This paper is a clean test case that the v3 split works.
  8. **Whether route 4 warrants the `oracle-leak` tag is a judgement call I made and should be
     reviewed.** The evaluation-set-calibrated constants (clash ceiling from 246 reference
     replicates, post hoc reportability thresholds, post hoc metric families, exploratory scoring
     before the split freeze) meet the v3 route-4 definition literally, and the authors declare all
     of them. But `oracle-leak` was written for structure-prediction pipelines seeing a target
     state, and applying it to a benchmark's threshold calibration may over-trigger the reverse
     lookup. Recorded here rather than silently dropped.
  9. **Fig. 3a's "ensemble-only rail"** places four models outside the plotting plane. I recorded
     it under `hides`, but it is arguably the correct design given post-gate is NA by task — v3 has
     no way to mark a figure choice as *defensible but potentially misleading*.
- **why_it_matters**: *(left empty by the extractor per v3 — the user's call)*

---

## Tags

`general-protein` `benchmark-only` `md` `md-emulator` `ensemble` `continuum` `binary-predicate`
`continuous-metric` `saturating-metric` `oracle-leak` `prospective` `anti-memorization` `preprint`
`threat` `background` `negative-result` `comparator-numbers`

All seventeen are from the fixed v3 vocabulary. Rationale for the non-obvious ones:
- `md` — the authors ran their own CHARMM36m simulations for Lockbox-36 (3 × 200 ns × 36, plus
  8 × 3 × 1 µs), p14. This is not only re-analysis of public data.
- `md-emulator` — the objects under test are generative models trained on MD trajectories
  (ConfRover, MDGen, BioEmu, AlphaFlow, P2DFlow, Str2Str, MarS-FM, ProTDyn, BioKinema); a reverse
  lookup for MD-emulator evaluation must return this paper.
- `saturating-metric` — the defining finding: Layer 1 saturated on every row, Layer 2 exactly
  invariant to order destruction and *maximised* by a dynamics-free i.i.d. construction (0.99 vs
  real MD's 0.88), 29.5% of scored cells SATURATED (pp. 3–6, 15, 17).
- `oracle-leak` — v3 route 4 only, self-declared; see `unresolved` item 8 for the caveat.
- `prospective` — Lockbox-36 only; the ATLAS-82 headline is retrospective (p13). `prospective` in
  the field is recorded as **partial**.
- `negative-result` — the central experiment is a negative result about a whole class of metrics.
- No `Control` or `Site` tag applies: the paper directs no generator to any state and studies no
  binding site.
- Deliberately **not** applied: `multi-backbone` (see `unresolved` 1), `design-level-oracle` (route
  7 here is control construction, which is legitimate, not a defect), `figure-exemplar` (the paper
  is kept for its argument, not its figures, and must not be excluded from gap analysis),
  `experimental-validation` (no wet-lab work; the "positive controls" are MD, not experiment).
