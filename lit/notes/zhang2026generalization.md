# zhang2026generalization

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–7), and they coincide with
the journal's own printed page numbers (the footer reads "npj Drug Discovery | (2026) 3:30" and
1–7).** Layout: p1 abstract + introduction; p2 Fig. 1 + Results start; p3 Fig. 2 + confidence
and rescue sections; p4 FEP+ sections + Methods start; p5 Fig. 3 + Methods; p6 Methods end,
Data/Code availability, references; p7 references, author contributions, competing interests,
license.

**Scope caveat recorded up front, because it governs how this note should be read:** this is a
*pose-accuracy and usability* benchmark, not a conformational-state paper. It never applies an
active/inactive predicate to anything. Section C is therefore filled honestly rather than
generously: several conformational fields are `NOT APPLICABLE` or `NOT REPORTED` by the paper's
design, and the one arm that touches state (co-folding with the cognate G protein) is scored by
RMSD to the deposited structure like everything else.

**SI caveat, stated here because it empties several rows below:** every per-target and
per-series number lives in Table S1, Table S2 and Figs. S1–S6, none of which are in this
7-page PDF. See `si_in_scope`.

---

## A. Identity

- **citekey**: `zhang2026generalization`
- **doi**: **10.1038/s44386-026-00066-1** — p1 header, repeated in the running head on p2–p7.
  Matches `refs.bib` and `MANIFEST.csv`. Supplementary information is at the same DOI (p7).
  Data: Zenodo **10.5281/zenodo.18343531** (p6). Code:
  `https://github.com/schrodinger/Co-Folded-GPCR-Evaluation` (p6).
- **year**: **2026.** p6: "Received: 23 January 2026; Accepted: 17 July 2026". Footer on every
  page: "(2026) 3:30".
- **venue**: **npj Drug Discovery**, volume 3, article 30 — peer-reviewed journal article
  (p1 masthead "npj | drug discovery — Article"; explicit Received/Accepted dates on p6).
  **Not a preprint.** Tag `peer-reviewed`, not `preprint`.
- **title**: On the generalization and usability of cofolding models for GPCR drug discovery — p1
- **authors**: Lichirui Zhang¹, Richard A. Friesner², Edward B. Miller¹ & João P. GLM Rodrigues¹
  (corresponding, joao.rodrigues@schrodinger.com) — p1. ¹Schrödinger, Inc., New York;
  ²Department of Chemistry, Columbia University.
  **Competing interests are load-bearing for how the physics arm is read and are declared on
  p7:** "R.A.F. has a significant financial stake in Schrödinger, Inc., is a consultant to
  Schrödinger, Inc., and is on the Scientific Advisory Board of Schrödinger, Inc. L.Z., E.B.M.
  and J.P.G.L.M.R. are employees of Schrödinger, Inc, and have a stake in the company." Every
  physics-based tool benchmarked as the *rescue* (Glide, IFD-MD, FEP+, PrepWizard, LigPrep,
  Epik, OPLS4, Force Field Builder) is a Schrödinger product; Friesner (author 2) is the first
  author of the Glide reference (ref. 31, p7) and Miller (author 3) of the IFD-MD reference
  (ref. 32, p7).

## B. Scope

- **system**: **GPCR — human, ligand-bound, small-molecule ligands only.** p4: "This yielded 253
  ligand-bound human GPCRs across 74 families as our GPCR benchmark (see Table S2 for a complete
  list)." Peptide- and protein-ligand entries are explicitly excluded (p4: "We further required
  that the selected GPCRs had a small-molecule ligand bound, thereby excluding entries with
  protein and peptide ligands").
- **n_targets**: **253 ligand-bound human GPCR complexes across 74 GPCRdb families** (p4), all
  post-dating the Boltz/AF3 training cutoff at family level. Sub-arms have their own n and they
  differ; recording each separately because the headline 253 is not the n behind most claims:
  - RMSD evaluation (Fig. 1): **253** top-scored models.
  - G-protein co-folding arm: **201 paired complexes** (p2).
  - Boltz-2 comparison: 253 re-run; the statistical test is on the **180** cases *not* in the
    Boltz-2 training set (73 of 253 are) — p3.
  - Rescue arm (Fig. 2a): 253 → **84** Boltz failures redocked (114 successes and 55
    wrong-pocket cases removed first) — p3.
  - FEP+ curation: **27 congeneric series across 14 GPCR structures** (p5); of these **14 series
    targeting 8 GPCRs** had a clear retrospective FEP+ signal and form the FEP+ arm (p4).
  - IFD-MD + FEP+ arm: 5 Boltz models × **8 FEP+-validated receptors** (p4).
  - **Generality flag:** the abstract's claim is about "co-folding models" in general but the
    evidence is one model family (Boltz-1x, with a Boltz-2 check) on one receptor class. The
    authors are explicit that Boltz is used "as a representative co-folding method" (p1), and
    they themselves offer the GPCR-only restriction as the explanation for the pLDDT null
    result (p3).
- **method_class**: **benchmark-only + co-folding evaluation, coupled to physics-based
  refinement (docking / induced-fit MD / alchemical free energy).** They train nothing and
  modify no model; they run an off-the-shelf co-folding model and then a Schrödinger physics
  stack on its outputs. p2: "Our major goal in this study was to evaluate how co-folding methods
  perform on tasks and metrics relevant to drug discovery". The physics half (Glide rigid-receptor
  docking, IFD-MD induced-fit docking, FEP+ alchemical free-energy perturbation with 50 ns per
  leg) has no clean `method_class` label in the v3 list; recorded here and flagged under
  `unresolved`.
- **backbones**: **Boltz only — Boltz-1x (v1.0.0) as the primary model, Boltz-2 as a
  version-comparison arm.** p5: "Boltz-1x (v1.0.0) was obtained from GitHub." p1: "using
  Boltz-1x (hereafter 'Boltz'), an open-source state-of-the-art model, as a representative
  co-folding method." p3: "we re-ran the entire benchmark dataset with Boltz-2, an improved
  model that was released during the course of this work". **No AF3, Chai, OF3, Protenix or
  RoseTTAFold All-Atom was run** — they appear only as citations on p1. Two versions of one
  model are not two backbones: **do not tag `multi-backbone`.**
- **templates**: **NOT REPORTED.** The Methods section "Boltz predictions and FEP+" (p5) names
  the sequence source, the ligand SMILES source, the MSA server and the recycling count, and
  says nothing about structural templates. Boltz's default template setting is never stated and
  must not be inferred. (Note the word "template" *does* appear on p5–p6, but only in the
  docking sense — "the centroid of the template ligand", "maximum-common-substructure
  (GlideMCS) constraint to the native ligand" — which is a different and separate issue,
  recorded under `oracle_leakage` route 1.)
- **msa_handling**: **full (default server), not subsampled, not clustered, not state-filtered.**
  p5: "Multiple sequence alignments (MSAs) were generated using the Boltz default MSA server,
  with 10 recycling iterations per the recommendation in the Boltz technical report." No depth
  is stated, no subsampling, no per-state alignment. Nothing in this paper manipulates the MSA.

## C. Conformational core

- **states_generated**: **ensemble + single-state.** Boltz emits five diffusion samples per
  complex (p5: "For each GPCR-ligand complex, we generated five diffusion samples"), so an
  ensemble exists; but the primary evaluation collapses it to one — p2: "We evaluated the
  accuracy of the top-scored Boltz model". The collapse is also the paper's own diagnosis of a
  failure mode: p2, "Co-folding methods tend to predict inactive receptor structures, while most
  of our dataset comprises agonists (228 out of 253 cases)." Note this single-basin claim is
  *asserted with a citation* (refs 33, 36) and **is never measured in this paper** — no
  active/inactive assignment is made anywhere. The five-sample ensemble is used as a pose pool
  only in the rescue and FEP+ arms (p6: "each of the five Boltz diffusion samples for the GPCRs
  was redocked with Glide and IFD-MD").
- **structural_priors_used**: **Extensive, at design time, and not in itself a defect — this is
  a retrospective benchmark and every reference is a deposited structure.** Enumerated:
  1. **The full set of deposited post-cutoff human GPCR structures, enumerated from GPCRdb**, is
     the target set. p4: "We enumerated all human GPCR structures in GPCRdb41 that were initially
     released in the RCSB Protein Data Bank (PDB)42 after 2021-09-30 (the training cutoff for
     Boltz and AlphaFold3) and up to December 2024."
  2. **GPCRdb family assignments** define what counts as unseen. p4: "We retained only receptors
     whose GPCR family, as defined by GPCRdb, had no structures released before that date,
     ensuring that the benchmark excludes families seen during training. It is worth noting that
     the definition of a 'family' in GPCRdb accounts for the pharmacological classification of
     its endogenous ligands, rather than being purely based on sequence similarity43."
  3. **The native co-crystal ligand of each deposited structure is the ligand fed to Boltz**
     (p5, "the native ligand SMILES from ChEMBL"), and congeneric series were required to
     contain it (p5, filter 3: "the series must include the native ligand").
  4. **Sequence and chemical similarity to the training set was computed against pre-cutoff
     deposited structures** using BLAST and Tanimoto fingerprints (p4).
  5. **The OPM database** supplies the membrane orientation for FEP+ setup (p5).
  6. **The experimental structure's reported pH and prepared protonation/tautomer states** are
     carried into the model preparation (p5) — see route 1 below; this one crosses from prior
     into pipeline.
  7. **Prior literature knowledge of a specific deposited map's quality** is used to excuse a
     failure: p4, "previous publications reported that the PDB structure 8 × 16 has poor map
     density in the extracellular loop region".
  - PDB IDs named in the main text: 8IJB, 8WC7 (Fig. 2, p3), 8IJD, 8×17, 8×16, 8K2W, 8XVK
    (p4). The full 253-entry list is Table S2, **not held**.

- **oracle_leakage**: **PRESENT and structurally two-tiered. The Boltz prediction step itself is
  clean (routes 1–3 NONE FOUND for the co-folding input); every step downstream of it — pose
  triage, docking box placement, model preparation, best-model reporting — is oracle-informed,
  and route 5 is the definition of the benchmark.** The authors partially acknowledge this
  themselves (p3: "This analysis, while limited by its retrospective character, highlights the
  robustness of physics-based methods..."). All seven routes enumerated separately.

  **Route 1 — structures used as input or template: NONE FOUND for the co-folding prediction;
  PRESENT downstream.**
  - *Clean for Boltz.* Protocol page for checkability is p5: "Boltz-1x (v1.0.0) was obtained
    from GitHub. For each GPCR-ligand complex, we generated five diffusion samples using the
    full-length receptor sequence obtained from the UniProt database and the native ligand
    SMILES from ChEMBL." Sequence + SMILES + MSA only. No deposited coordinates enter Boltz.
  - *Leaky downstream, route 1a — the docking box is centred on the experimental ligand.*
    p6, verbatim: "For Glide docking grid generation, the box center was placed at the centroid
    of the template ligand." The entire Glide/IFD-MD rescue arm therefore knows the experimental
    binding-site location. The authors state the dependency openly as a reason for excluding the
    wrong-pocket cases — p3: "we then removed 55 'wrong pocket' cases where the predicted ligand
    center of mass was > 5 Å from that of the experimental ligand, since those cases fall outside
    the scope of refinement with most physics-based docking methods where knowledge of the
    binding site is a prerequisite."
  - *Leaky downstream, route 1b — protonation and tautomer states are copied from the prepared
    experimental structure into the Boltz model.* p5, verbatim: "To ensure consistency, the
    protonation/tautomer states of the ligand and protein titratable residues were forced to
    match the states in the prepared experimental structures."
  - *Leaky downstream, route 1c — FEP+ starting poses on the experimental arm are built under an
    MCS constraint to the native ligand.* p5: "Initial poses for each series were generated with
    Glide31 using a maximum-common-substructure (GlideMCS) constraint to the native ligand."
    (On the Boltz arm the MCS constraint is instead to the Boltz-predicted pose, p5–p6, which is
    the non-leaky choice and should be credited.)
  - *Leaky downstream, route 1d — the severe-clash diagnostic is computed against the native
    pose.* p3: "we quantified clashes between the native pose and the Boltz receptor models,
    defining a severe clash as any pair of heavy atoms closer than 0.75 times the sum of their
    van der Waals radii."

  **Route 2 — state annotations from a curated database driving templates or alignments:
  NONE FOUND.** GPCRdb *is* used, heavily, but for enumeration and family-novelty filtering, not
  for state annotation, templating or alignment — p4, quoted in full under
  `structural_priors_used` item 1–2. UniProt is used for sequences and for the "Transmembrane"
  annotation used in RMSD superposition (p6: "Transmembrane (TM) residues were identified using
  the 'Transmembrane' annotation in the UniProt database"), which is a topology annotation, not
  a state annotation. **No GPCRdb active/inactive state label is used anywhere.** Protocol pages
  for checkability: p4 (benchmark construction) and p5–p6 (all Methods).

  **Route 3 — cluster labels derived from known states: NONE FOUND.** No clustering of any kind
  is performed. Protocol pages p4–p6.

  **Route 4 — hyperparameters, sweeps, seeds or stopping criteria tuned against known answers:
  PRESENT, twice, both on the FEP+ arm.**
  - *4a, the reported metric is the minimum over an analysis-time sweep.* p5, verbatim: "To
    minimize the FEP+ errors related to simulation time, we reanalyzed the FEP+ maps to 5 ns,
    10 ns, and 25 ns, and picked the lowest RMSE result as the final result." RMSE here is
    against the experimental affinities, i.e. against the evaluation target. Under the v3 rule
    ("tuning a *range* on the evaluation set is leakage even when no single value is picked per
    target") this is leakage, and it is applied to the experimental, Boltz and IFD-MD arms
    alike, so it inflates all three rather than the comparison between them.
  - *4b, the evaluation subset is chosen by how well the reference performs on it.* p4: "we
    first needed to identify ligand series for which FEP+ could reliably recapitulate
    experimental structure–activity relationships using the experimental structures" — 14 of 27
    series survive this filter (p4). The authors give an explicit and defensible reason (p4:
    "Otherwise, if both the experimental and Boltz-predicted structures fail to produce a clear
    FEP+ signal, we cannot attribute the failure specifically to errors in the Boltz models"),
    but the arithmetic consequence is that the headline FEP+ comparison runs only on the half of
    the series where the oracle structure already worked.
  - *Boltz itself was not tuned:* p5 gives one fixed setting (5 samples, 10 recycles, default MSA
    server) applied to every target, and p6 states "All other settings were kept at their default
    values for both methods" for Glide and IFD-MD. No per-target tuning anywhere.

  **Route 5 — success defined post hoc by RMSD to a structure they had: PRESENT, and it is the
  benchmark's definition.** Verbatim, p3: "we first filtered out the 114 cases where Boltz
  already produced a native-like ligand pose, defined as a ligand heavy-atom RMSD < 2.5 Å
  relative to the experimental pose." And p2: "If we defined the top N success rate as the
  top-N-ranked pose within 2.5 Å of the native ligand, which is a widely used threshold in the
  docking field". And Fig. 1 caption, p2: "Horizontal red dashed lines mark 'success' thresholds
  at 2.0 Å for Cα RMSD and 2.5 Å for ligand RMSD, respectively." This is not a criticism of the
  paper — a retrospective benchmark can define success no other way — but it must be recorded,
  because none of the reported success rates are obtainable prospectively.

  **Route 6 — best/worst model labels assigned against a held reference: PRESENT on the FEP+ and
  rescue arms; ABSENT on the primary RMSD arm.**
  - *Clean on the primary arm:* the reported model is chosen by Boltz's own confidence ranking,
    not by RMSD. p2: "We evaluated the accuracy of the top-scored Boltz model".
  - *Leaky on the rescue arm:* success is "within the top 5 predictions" (p3) out of 5 Boltz
    models × 5 (or 10) docked poses, with the hit identified by RMSD to native. Relaxing the
    budget to top 10 moves the rescue rate from 45/84 to 52/84 (p3), which quantifies how much
    the selection-by-oracle is worth.
  - *Leakiest on the FEP+ arm:* Fig. 3's title is "FEP+ performance of experimental structures,
    the **best** Boltz model, and the **best** IFD-MD models" (p5, emphasis added), and the
    selection criterion is stated on p4, verbatim: "we performed full IFD-MD refinement on all
    five Boltz models for each of the eight FEP + -validated receptors, then ran FEP+ validation
    on the top 5 IFD-MD poses from each model. As summarized in Table S1 and Fig. S6, except for
    Series 3, all thirteen remaining series contained **at least one pose** with ligand
    RMSD < 2.5 Å that also passed FEP+ validation". So the headline IFD-MD result is a best-of-25
    per series, selected jointly on RMSD to the native pose *and* on the FEP+ outcome being
    reported. The Boltz baseline it is compared against is a best-of-5.

  **Route 7 — design-level oracle use (weaker than pipeline leakage; label kept distinct):
  PRESENT, and inherent to the design.** Systems were selected because a deposited answer exists
  (p4, benchmark construction, quoted above); series were selected to contain the native ligand
  (p5, filter 3); and the paper states the outcome of the site question before evaluating it —
  p5: "All native ligands are bound in the orthosteric binding site of the receptors." The
  expected-answer-known condition also drives the interpretive framing on p4 ("In a prospective
  drug discovery setting, using the unrefined Boltz structures would not have enabled any of
  these targets, in contrast to IFD-MD refinement, which enabled all three") — a prospective
  claim made entirely from retrospective, oracle-selected evidence. **This is design-level, not
  pipeline-level, and should not be conflated with routes 1, 4, 5 and 6 above.**

- **prospective**: **NO — retrospective in every arm, and the authors half-say so.** The
  *targets* are prospective-flavoured (post-cutoff, family-novel — p1: "To better mirror
  prospective use in drug discovery, we restricted the benchmark to GPCR structures whose
  families were not included in the reported training set of Boltz"), but every scoring step
  requires the deposited structure and the deposited affinity data. Their own hedge, p3
  verbatim: "This analysis, while limited by its retrospective character, highlights the
  robustness of physics-based methods in correctly predicting ligand poses given sufficiently
  accurate receptors." They also describe FEP+ as the prospective substitute for the oracle
  (p2: "we demonstrate how free-energy perturbation can be used as a rigorous validation method
  for co-folding models in prospective scenarios, provided high-quality affinity data is
  available"), which is the paper's honest answer to its own retrospectivity — but no
  prospective run is reported.
- **state_metric**: **RMSD-to-reference, with every claim binarised by a stated threshold. No
  conformational-state predicate exists in this paper at all.**
  - Receptor: in-place Cα RMSD after sequence-alignment superposition (p6, Methods "RMSD
    calculations"); success threshold **2.0 Å** (Fig. 1 caption, p2), justification NOT REPORTED.
  - Ligand (orthosteric): TM-Cα superposition then in-place heavy-atom RMSD (p6); success
    threshold **2.5 Å**, justified only as convention — p2: "which is a widely used threshold in
    the docking field".
  - Ligand (allosteric): superposition on binding-pocket Cα within 10 Å of the native ligand
    (p6) — a *different* superposition frame for allosteric than for orthosteric ligands, which
    means the two ligand-RMSD populations plotted together in Fig. 1b–d are not computed
    identically. The paper does not flag this.
  - Wrong pocket: predicted ligand centre of mass **> 5 Å** from experimental (p3), justification
    NOT REPORTED.
  - Severe clash: heavy-atom pair closer than **0.75 ×** the sum of vdW radii (p3), justification
    NOT REPORTED.
  - FEP+ signal: **R² > 0.3 and pairwise RMSE < 2.0 kcal/mol** (p4), justification NOT REPORTED.
  - **NOT APPLICABLE — active/inactive.** No state assignment, no state-specific reference, no
    activation coordinate. The G-protein arm's "improvement" is a TM Cα RMSD number (p2), not a
    state call.
  - One diagnosis is made by eye rather than by metric, and it inverts a metric result: p4,
    "Inspection of the FEP+ maps indicates that the high RMSD reflects a pose flipped by 180°
    around its long axis". Recorded here rather than tagged `visual-metric`, which would
    false-positive state queries.
- **metric_saturation**: **YES — receptor Cα RMSD floors on this dataset, and the authors invoke
  the floor themselves to explain their own null result.** p3, verbatim: "A possible explanation
  is that our dataset is restricted to GPCRs, for which most receptor Cα positions are
  well-predicted even when the confidence score is low." The numbers bear it out: mean Cα RMSD
  1.44 Å against a 2.0 Å success threshold, median 1.25 Å, SD 0.76 Å (p2) — the bulk of the
  distribution sits below the threshold, so the receptor metric has little dynamic range left
  and the pLDDT correlation (R² = 0.046) is measured against a near-floored quantity. Second,
  minor: R² in Fig. 3a is bounded at 1.0 and Series 10 IFD-MD reaches ≈1.00 (p5 render), so the
  top of that axis is attained. Ligand RMSD does **not** saturate (range to 35 Å, Fig. 1b–d).
  Figure-level concealment is recorded in `hides` on the Fig. 1f and Fig. 3 rows, not here.
- **directional_control**: **Tested with one handle — the cognate G-protein partner — and it
  worked on the receptor backbone and not on the ligand.** This is the field's cleanest result
  in the paper and it is recorded verbatim, p2:

  > "Co-folding methods tend to predict inactive receptor structures, while most of our dataset
  > comprises agonists (228 out of 253 cases). To test this hypothesis, we re-predicted the
  > complexes in our dataset and included the corresponding G-protein sequence (if present in
  > the experimental structure). Across 201 paired complexes, while we observe substantial
  > improvements to receptor model accuracy (Fig. S1a, median TM Cα improves from 1.01 Å to
  > 0.75 Å), we do not observe significant improvement of ligand prediction accuracy (Fig. S1b,
  > median improvement of 0.01 Å)."

  So: **partner co-folding buys 0.26 Å of median TM Cα accuracy and 0.01 Å of median ligand
  accuracy.** The supporting panels (S1a, S1b) are in supplementary material **not held**; the
  main text carries only these two medians, with no distribution, no n per bin and no test
  statistic. Other handles: the native ligand is always co-folded (an input, never varied, so
  not tested as a handle); no seed control, no MSA-depth control, no template bias, no nanobody
  or mimetic, no apo arm. Nothing in the paper can be *instructed* which receptor state to
  produce beyond adding the partner.
- **coinput_composition**: **New in v3.1. CONFOUNDED, and more tightly than it first appears.**
  - baseline arm: receptor + **native small-molecule ligand, always present and never varied** — 228 of the 253 ligands are agonists (p.2).
  - G-protein arm: receptor + the same ligand + cognate G-protein sequence, 201 paired complexes (p.2).
  - **There is no apo arm at all**, and the ligand is an input rather than a handle.
  **Consequence.** The reported 1.01 → 0.75 Å median TM Cα improvement is the *marginal* effect of adding the transducer to a receptor that already has its agonist bound. It is not a partner-versus-nothing comparison, and it cannot be read as the partner driving activation from rest. Tag `coinput-confounded`.

- **binding_order**: **ORDER-AGNOSTIC by construction.** All inputs supplied at once to Boltz; no sequence is represented. The paper does, however, motivate its partner arm with an order-flavoured hypothesis (p.2: co-folding "tend[s] to predict inactive receptor structures, while most of our dataset comprises agonists"), i.e. it treats the missing transducer as the reason the agonist alone did not produce an active receptor. That is a mechanistic reading the method itself cannot test.

- **input_factor_design**: **New in v3.2. HELD throughout — no factor is crossed with any other.** **MSA**: full default server, **never varied** (not subsampled, not clustered, not state-filtered). **templates**: NOT REPORTED. **ligand**: a small-molecule ligand is required of every one of the 253 entries and is **never removed**. **partner**: **VARIED** — the 201-pair G-protein co-folding arm against the main arm. <br>`crossings:` **partner x ligand HELD** (ligand present in every arm); **MSA x anything impossible** because the MSA is fixed by design. So its partner result cannot be separated from ligand occupancy, and the alignment plays no experimental role at all.
- **anti_memorization_design**: **YES, and it is the paper's design centrepiece — a
  family-level, date-based holdout, n = 253.** Cutoff definition, p4 verbatim: "We enumerated all
  human GPCR structures in GPCRdb41 that were initially released in the RCSB Protein Data Bank
  (PDB)42 after 2021-09-30 (the training cutoff for Boltz and AlphaFold3) and up to December
  2024. We retained only receptors whose GPCR family, as defined by GPCRdb, had no structures
  released before that date, ensuring that the benchmark excludes families seen during training."
  Note the cutoff is **family-level, not sequence-level**, and the authors quantify the residual
  overlap themselves — p4: "Due to the family definition in GPCRdb, 8% of GPCRs in our benchmark
  have > 50% sequence identity with structures in the training set." A second, independent
  holdout exists for the Boltz-2 arm: cutoff 2023-06-01, n = 180 out-of-training of 253 (p3).
- **anti_memorization_control**: **RUN, analysed, and reported as a null — this is a real
  control arm, not a held-out set that merely exists.** Three arms:
  1. *Similarity-vs-accuracy regressions* (Fig. 1a–c, p2): receptor sequence identity to
     training, ligand Tanimoto to training. Result, p2 verbatim: "we found no clear trend
     between the accuracy of receptor and ligand predictions and training set similarity
     (Fig. 1a–c). Boltz can produce very accurate models when both the receptor and ligand are
     dissimilar to the training data, while it can perform poorly when they are similar."
  2. *Boltz-1x vs Boltz-2, split by training-set membership* (p3). Verbatim: "Boltz-2 was
     trained on an expanded dataset comprising structures deposited in the wwPDB before
     2023-06-01, which includes 73 of our dataset cases. We show that while Boltz-2 produces
     more accurate ligand poses across the entire dataset (Fig. S2 and S3), the improvements are
     mostly concentrated among those structures that are part of the new model training set. For
     all other structures, there is no significant difference between Boltz-1x and Boltz-2
     performance (t = 1.51, n = 180, p = 0.13; Wilcoxon signed-rank test: W = 7329, p = 0.2957)."
     **This is the memorization control: "novel" here means deposited after 2023-06-01 and hence
     outside the Boltz-2 training set, n = 180 of 253; the apparent version improvement vanishes
     on it (t-test p = 0.13; Wilcoxon p = 0.2957).**
  3. *Ligand volume-overlap and allosteric annotation* (Fig. 1d, p2) — a mode-of-failure control
     rather than a memorization control; recorded in `controls_run`.
  - **Powered:** n = 180 for arm 2 and n = 253 for arm 1, both well above the `UNPOWERED`
    threshold. **Caveats to record:** the family-level cutoff leaves 8% of targets at > 50%
    sequence identity to training (p4), and the supporting distributions for arm 2 (Figs. S2,
    S3) are **not held**.

- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Training-set similarity regressed against accuracy: receptor sequence identity (Fig. 1a–b), ligand Tanimoto (Fig. 1c) | Rules out "the test set is just too dissimilar to training" as the explanation for poor ligand poses; also rules out similarity as a usable prospective quality proxy | p2 |
  | Boltz-2 re-run of the whole benchmark, split into 73 in-training vs 180 out-of-training cases, with t-test and Wilcoxon signed-rank | Rules out that a newer/bigger model closes the gap; isolates the improvement as memorization of newly-trained-on structures | p3 |
  | Co-folding with the cognate G-protein sequence, 201 paired complexes, scored separately on receptor TM Cα and on ligand RMSD | Rules out "the receptor is in the wrong (inactive) state" as the explanation for bad ligand poses — receptor accuracy improves, ligand accuracy does not | p2 |
  | FEP+ run on the *experimental* structures first, 27 series → 14 with a clear signal | Rules out the FEP+ protocol, the affinity data quality and the deposited structure quality as the cause of downstream FEP+ failures | p4 |
  | Staged rescue: rigid-receptor Glide first, then induced-fit IFD-MD only on Glide failures | Separates ligand-pose search error from receptor sidechain/backbone error as the cause of failure | p3 |
  | Severe-clash quantification on rescue failures (native pose vs Boltz receptor, 0.75 × vdW criterion) | Rules out docking-method weakness as the cause of unrescued cases; attributes them to receptor model error | p3 |
  | Pose-budget sensitivity: rescue rate at top-5 vs top-10 poses (45/84 vs 52/84) | Quantifies how much of the rescue rate is bought by selection budget rather than by method quality | p3 |
  | pLDDT and ipTM evaluated as the *same* kind of discriminator on the *same* dataset (Fig. 1e vs 1f) | Rules out "any confidence head works"; identifies which score carries the signal | p3 |
  | Wrong-pocket cases (COM > 5 Å, n = 55) segregated and excluded before refinement | Rules out contamination of the rescue statistics by cases physically outside the docking box | p3 |
  | Allosteric ligands flagged and plotted separately (red points, Fig. 1b–d) | Isolates the allosteric-into-orthosteric failure mode from generic pose error | p2 |
  | IFD-MD applied also to series where Boltz *already* produced an FEP+ signal | Rules out that refinement degrades already-good models — "IFD-MD refinement did not degrade FEP+ performance significantly" | p4 |
  | FEP+ maps reanalysed at 5, 10 and 25 ns | Controls for insufficient simulation length as a source of FEP+ error (but see `oracle_leakage` route 4a — the minimum is then reported) | p5 |
  | Protonation/tautomer states forced identical between experimental and Boltz structures; identical FEP+ protocol and perturbation graph across arms | Rules out preparation and protocol differences as the source of the experimental-vs-Boltz FEP+ gap (at the cost of route-1b leakage) | p5 |

- **confidence_as_discriminator**: **YES, and this is the field's decisive entry for this paper —
  they test two confidence heads on the same 253 cases and reach opposite conclusions, and the
  section heading generalises the positive half.** Section title, p3: "Confidence scores are
  useful markers of prediction quality".
  - **ipTM — validated as a discriminator of ligand-pose correctness.** p3 verbatim: "As shown
    in Fig. 1f, a higher interface predicted TM-score (ipTM) generally corresponds to a lower
    ligand RMSD (R2 = 0.49), making ipTM a useful decision metric. Indeed, in our dataset,
    ipTM > 0.95 indicates a correct ligand pose (RMSD < 2.5 Å) for more than 75% of cases,
    whereas lower ipTM values indicate a need for additional validation or refinement."
    **Statistics: R² = 0.49; ipTM > 0.95 → > 75% of cases correct at the 2.5 Å threshold (n = 71
    in that bin, from the Fig. 1f render, p2).**
  - **ipTM also flags wrong-pocket hallucinations.** p3 verbatim: "This confidence filtering is
    particularly valuable for detecting binding site errors. Cases where allosteric ligands were
    incorrectly placed into the orthosteric pocket consistently have ipTM scores below 0.80,
    suggesting that the model can potentially flag its own hallucinations regarding binding site
    location, preventing users from trusting these artifactual poses."
  - **pLDDT — tested and REJECTED for receptor accuracy.** p3 verbatim: "However, we note that
    this observation does not extend to the predicted receptor accuracy score (pLDDT) (Fig. 1e;
    R2 = 0.046). A possible explanation is that our dataset is restricted to GPCRs, for which
    most receptor Cα positions are well-predicted even when the confidence score is low."
    **Statistic: R² = 0.046 against Cα RMSD.**
  - **Was the use validated?** Partially and retrospectively. The validation is a correlation
    against RMSD to the deposited structure over the 253-case benchmark (routes 5 and 6 above);
    no prospective or held-out confirmation of the ipTM > 0.95 rule is run, no calibration curve,
    no per-family breakdown, and the two scores are compared on **different measures** — ipTM
    against ligand RMSD, pLDDT against receptor Cα RMSD — so the comparison is not like-for-like
    and the pLDDT null is confounded with the receptor-metric floor the authors themselves name.
    **A cross-comparison (pLDDT vs ligand RMSD, or ipTM vs Cα RMSD) is NOT REPORTED.**
  - **Confidence also drives model selection throughout:** "the top-scored Boltz model" (p2) is
    the confidence-ranked model, so the headline RMSD numbers are already conditioned on the
    confidence head being useful.

## D. Claims

- **central_conclusion**: On a family-level post-training-cutoff benchmark of 253 ligand-bound
  human GPCRs, Boltz predicts receptor backbones accurately (mean Cα RMSD 1.44 Å) but ligand
  poses poorly (mean 5.95 Å; 37.15% top-1 success at 2.5 Å), and this pose error is not explained
  by similarity to the training set, is not fixed by a newer model version, and is not fixed by
  supplying the cognate G protein. The pose errors are consequential downstream: half the
  congeneric series that work from experimental structures fail FEP+ from Boltz structures.
  Physics-based refinement (Glide, then IFD-MD) rescues 53.57% of the failures and restores FEP+
  performance to near-native, and ipTM — but not pLDDT — is a usable filter for deciding which
  predictions to trust.

- **necessity_claims** (verbatim + page):
  - p1: "concerns persist regarding training set leakage and generalization to novel targets,
    **an essential requirement in drug discovery**, where ligands and, at times, targets, are
    often novel."
  - p3: "those cases fall outside the scope of refinement with most physics-based docking
    methods **where knowledge of the binding site is a prerequisite**."
  - p4: "To gather benchmark data for validating Boltz structures with FEP + , **we first needed
    to identify ligand series for which FEP+ could reliably recapitulate experimental
    structure–activity relationships using the experimental structures.** Otherwise, if both the
    experimental and Boltz-predicted structures fail to produce a clear FEP+ signal, we cannot
    attribute the failure specifically to errors in the Boltz models, as it could also arise from
    limitations in the FEP+ protocol, uncertainties in the experimental affinities, or
    inaccuracies in the experimental structures themselves."
  - p4: "This also indicates that additional refinement, such as density-map-guided refinement,
    **is probably necessary** to obtain better FEP+ results40."
  - p4: "These cases highlight **the necessity of diverse chemical series targeting multiple
    sites on the molecule** when using methods such as FEP + , to avoid drawing erroneous
    conclusions28."
  - p2 (advocacy, conditional necessity): "In summary, for maximal confidence, we advocate a
    workflow in which predicted structures seed physics-based refinement and validation before
    committing to design choices."
  - p1 (abstract, same claim): "These results highlight the strengths and limitations of
    co-folding methods and motivate a workflow that pairs them with physics-based refinement and
    validation before high-stakes decisions in drug discovery."
  - **Impossibility / negative claims** (recorded here because they are the load-bearing
    contrast sentences):
    - p2: "structural or sequence similarity to the model's training set **does not reliably
      guarantee** prediction quality."
    - p2: "Thus, for the cases in our benchmark, training set similarity showed little predictive
      value for pose quality, consistent with previous studies15,37."
    - p2: "we **do not observe significant improvement of ligand prediction accuracy** (Fig. S1b,
      median improvement of 0.01 Å)."
    - p3: "For all other structures, **there is no significant difference between Boltz-1x and
      Boltz-2 performance** (t = 1.51, n = 180, p = 0.13; Wilcoxon signed-rank test: W = 7329,
      p = 0.2957)."
    - p4: "In a prospective drug discovery setting, **using the unrefined Boltz structures would
      not have enabled any of these targets**, in contrast to IFD-MD refinement, which enabled
      all three."
    - p1: "in line with previously published observations, cofolding models **struggle to produce
      accurate ligand poses that can effectively drive drug discovery**."
    - p3: "Such local yet consequential misplacements are **not well captured by the RMSD
      metric**, as well-predicted parts could average them out." (p4 restates this.)

- **novelty_claims**: **NONE FOUND.** The paper makes no claim to be first, novel or
  unprecedented anywhere in the text; a full scan for "first", "novel", "unprecedented", "to our
  knowledge" returns only the enumerative "First, do co-folding models generalize beyond their
  training sets?" (p1) and uses of "novel" meaning *unseen target* ("a benchmark of human GPCR
  complexes novel to Boltz", p2). The nearest thing to a gap claim is the opening sentence of
  the abstract, p1 verbatim: "The generalizability of co-folding models for protein–ligand
  structure prediction remains unclear." The paper repeatedly positions itself as *consistent
  with* prior work rather than ahead of it — p1: "in line with previously published
  observations"; p2: "consistent with previous studies15,37"; p2: "This result is expected and in
  line with other published reports33". **A paper that claims no priority is unusual in this
  corpus and is worth noting as such.**

- **stated_limits**:
  - Retrospective character of the clash analysis, p3: "This analysis, while limited by its
    retrospective character, highlights the robustness of physics-based methods in correctly
    predicting ligand poses given sufficiently accurate receptors."
  - The pLDDT null may be an artefact of a GPCR-only dataset, p3: "A possible explanation is that
    our dataset is restricted to GPCRs, for which most receptor Cα positions are well-predicted
    even when the confidence score is low."
  - Residual training overlap despite family-level filtering, p4: "Due to the family definition
    in GPCRdb, 8% of GPCRs in our benchmark have > 50% sequence identity with structures in the
    training set."
  - Unexplained FEP+ failures on experimental structures, p4: "The absence of a clear FEP+ signal
    in the remaining 13 cases could be attributed to various factors, including subtle
    inaccuracies in the experimental structures in the initial ligand binding poses or receptor
    sidechain placements... A comprehensive analysis of these specific cases, however, is beyond
    the scope of this study."
  - Long-timescale MD was ruled out on cost, not on principle, p3: "Although such cases could
    potentially be refined using long timescale simulations38, the computational cost and
    uncertainty in results led us to rule out such attempts."
  - The top-10 pose budget is conceded as generous, p3: "Although 10 poses per Boltz model is
    generous, as shown below, rigorous methods such as FEP+ can then be used to identify correct,
    high-quality predictions."
  - A strong FEP+ signal can arise for the wrong reason, p4: "experimental affinities correlate
    with the calculated octanol–water partition coefficient (AlogP; R² = 0.63), suggesting that
    hydrophobicity, rather than fine-grained receptor–ligand interactions, dominates affinity."
  - Series 3 is the one case IFD-MD did not fix (p4, "except for Series 3").
  - Ligand-series curation loses ligands, p5: "Ligands for which no acceptable pose could be
    found under the MCS constraint were excluded, potentially reducing series size from the
    original set."
  - The allosteric-bias hypothesis is explicitly untested, p2: "We hypothesize that this bias
    towards the orthosteric binding site arises from an imbalance in the model training set".
  - **Not stated as a limit, and it should have been:** the competing-interest overlap between
    the tools that fail (Boltz, third-party) and the tools that rescue (Glide, IFD-MD, FEP+, all
    Schrödinger, two of them co-authored by authors of this paper — p7).

- **stance**: **`precedent` on findings + `threat` on the confidence-score claim. Provisional —
  the user's call, not the extractor's.**
  - *Precedent, because:* it is an independent, well-powered, peer-reviewed demonstration that
    (i) co-folding partner supplementation improves receptor backbone but **not** ligand pose
    (p2), (ii) training-set similarity does not predict accuracy (p2), and (iii) a newer model
    version's apparent gain is memorization and vanishes on truly novel targets (p3, n = 180,
    p = 0.13 / 0.2957). Each of these is a result our work can cite rather than have to
    establish, and (i) bears directly on whether partners drive state.
  - *Threat, because:* the section headline "Confidence scores are useful markers of prediction
    quality" (p3) with ipTM R² = 0.49 and an ipTM > 0.95 → 75%-correct rule cuts against a
    confidence-does-not-discriminate position. The tension is narrower than the headline
    suggests — their positive result is ipTM against *ligand pose*, their negative result is
    pLDDT against *receptor Cα* (R² = 0.046), and neither is a conformational-state
    discrimination test — but the sentence as written is quotable against us and must be
    engaged rather than ignored.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Receptor Cα RMSD, TM bundle — mean | 1.44 | Å | deposited experimental structure, top-scored Boltz-1x model, n = 253 | 2 |
  | Receptor Cα RMSD, TM bundle — SD | 0.76 | Å | same | 2 |
  | Receptor Cα RMSD, TM bundle — median | 1.25 | Å | same | 2 |
  | Receptor Cα RMSD, loops + accessory domains — mean | 2.90 | Å | same | 2 |
  | Receptor Cα RMSD, loops + accessory domains — SD | 1.75 | Å | same | 2 |
  | Receptor Cα RMSD, loops + accessory domains — median | 2.63 | Å | same | 2 |
  | Ligand heavy-atom RMSD — mean | 5.95 | Å | deposited ligand pose, top-scored model, n = 253 | 2 |
  | Ligand heavy-atom RMSD — SD | 7.03 | Å | same | 2 |
  | Ligand heavy-atom RMSD — median | 3.45 | Å | same | 2 |
  | Top-1 pose success rate | 37.15 | % of 253 | top-1-ranked pose within 2.5 Å of native ligand | 2 |
  | Top-5 pose success rate | 44.66 | % of 253 | top-5-ranked pose within 2.5 Å of native ligand | 2 |
  | Boltz outcome — success | 114 / 253 (45.06) | count (%) | ligand RMSD < 2.5 Å | 3 (Fig. 2 caption) |
  | Boltz outcome — failure | 84 / 253 (33.20) | count (%) | ligand RMSD ≥ 2.5 Å, COM within 5 Å | 3 (Fig. 2 caption) |
  | Boltz outcome — wrong pocket | 55 / 253 (21.74) | count (%) | ligand COM > 5 Å from experimental | 3 (Fig. 2 caption) |
  | Glide rescue of Boltz failures, top 5 | 29 / 84 (34.52) | count (%) | native-like pose, RMSD < 2.5 Å | 3 |
  | IFD-MD additional rescue, top 5 | 16 / 84 (19.05) | count (%) | same | 3 |
  | **Total physics-based rescue, top 5** | **45 / 84 (53.57)** | count (%) | same | 3 |
  | Glide rescue, top 10 | 36 / 84 | count | same, relaxed pose budget | 3 |
  | Total physics-based rescue, top 10 | 52 / 84 (61.90) | count (%) | same, relaxed pose budget | 3 |
  | Cases left unrescued by either method, top 5 | 39 / 84 | count | same | 3 |
  | Severe clash present among Glide rescue failures | 94.90 | % of cases | native pose vs Boltz receptor, 0.75 × vdW criterion | 3 |
  | Severe backbone clash among IFD-MD rescue failures | 75.12 | % of cases | same | 3 |
  | ipTM vs ligand RMSD correlation | R² = 0.49 | dimensionless | ligand RMSD to native, n = 253 | 3 |
  | ipTM > 0.95 → correct pose | > 75 | % of cases in bin (n = 71) | ligand RMSD < 2.5 Å | 3 (bin n from Fig. 1f, p2) |
  | ipTM for allosteric-into-orthosteric errors | < 0.80 | ipTM | "consistently", no n given | 3 |
  | **pLDDT vs receptor Cα RMSD correlation** | **R² = 0.046** | dimensionless | Cα RMSD to native, n = 253 | 3 |
  | Boltz-1x vs Boltz-2, out-of-training subset — t-test | t = 1.51, n = 180, p = 0.13 | — | ligand pose accuracy | 3 |
  | Boltz-1x vs Boltz-2, out-of-training subset — Wilcoxon signed-rank | W = 7329, p = 0.2957 | — | ligand pose accuracy | 3 |
  | Boltz-2 training overlap with benchmark | 73 / 253 | count | wwPDB deposition before 2023-06-01 | 3 |
  | G-protein co-fold — receptor median TM Cα | 1.01 → 0.75 (Δ 0.26) | Å | deposited structure, 201 paired complexes | 2 |
  | **G-protein co-fold — ligand median improvement** | **0.01** | Å | deposited ligand pose, 201 paired complexes | 2 |
  | Benchmark composition — agonist complexes | 228 / 253 | count | dataset annotation | 2 |
  | Benchmark composition — families | 74 | GPCRdb families | dataset construction | 4 |
  | Residual training similarity despite family filter | 8 | % of benchmark GPCRs with > 50% seq. id. to training | BLAST vs pre-cutoff structures | 4 |
  | ChEMBL curation — raw | 16,236 measurements / 798 series | counts | receptor-ligand-document triads | 4 |
  | ChEMBL curation — after filters | 27 series / 14 GPCR structures | counts | six stated filters | 4, 5 |
  | **Series with a clear retrospective FEP+ signal from experimental structures** | **14 of 27** (targeting 8 GPCRs) | count | R² > 0.3 and pairwise RMSE < 2.0 kcal/mol | 4 |
  | **Series that FAILED FEP+ from experimental structures** | **13 of 27** | count | same criterion | 4 |
  | **Series that FAILED FEP+ from Boltz structures** | **7 of 14** ("ligand was incorrectly modeled") | count | same criterion, Boltz models as starting structures | 4 |
  | Series that recapitulated affinities from Boltz structures | 7 of 14 | count | same | 4 |
  | Of those 7, series with poor starting ligand RMSD (> 2.5 Å) | 2 | count | ligand RMSD to native | 4 |
  | Series meeting both RMSD < 2.5 Å and FEP+ pass, before IFD-MD | 5 | count | joint criterion | 4 |
  | Series meeting both criteria, after IFD-MD | 13 of 14 (all but Series 3) | count | joint criterion, best of 5 models × top-5 poses | 4 |
  | Series 2 (8IJD) initial pose RMSD despite strong FEP+ signal | 9.74 | Å | native ligand; pose flipped 180° | 4 |
  | Series 10 (8×17) initial pose RMSD despite strong FEP+ signal | 3.05 | Å | native ligand; AlogP correlation R² = 0.63 | 4 |
  | 8K2W Boltz ligand RMSDs / IFD-MD rescue | > 5 → 2.14 | Å | native ligand; restored FEP+ signal in Series 4–6 | 4 |
  | 8×17 Boltz ligand RMSDs | > 3 | Å | native ligand; no FEP+ signal Series 11, 12 | 4 |
  | 8XVK Boltz ligand RMSDs | > 2.5 (all) | Å | native ligand; 3 IFD-MD structures recovered signal | 4 |
  | Fig. 2 case study 8IJB — Boltz → Glide | 4.70 → 0.94 | Å | native ligand pose | 3 |
  | Fig. 2 case study 8WC7 — IFD-MD | 1.21 | Å | native ligand pose; Tyr287 clash resolved | 3 |
  | IFD-MD vs Boltz — median ΔR² | +0.095 | dimensionless | FEP+ R², paired over series | 5 (Fig. 3 caption) |
  | IFD-MD vs Boltz — median ΔRMSE | −0.150 | kcal/mol | FEP+ RMSE, paired over series | 5 (Fig. 3 caption) |
  | Wilcoxon signed-rank p-values for ΔR² and ΔRMSE | 0.066 and 0.029 | — | printed as "i-values" in the text layer; from context these are p-values | 5 (Fig. 3 caption) |
  | Cliff's δ for ΔR² | 0.39 (95% CI −0.12 to 0.89, n_eff = 13) | dimensionless | IFD-MD vs Boltz | 5 (Fig. 3 caption) |
  | Cliff's δ for ΔRMSE | 0.57 (95% CI 0.14 to 1.00, n_eff = 14) | dimensionless | IFD-MD vs Boltz | 5 (Fig. 3 caption) |
  | IFD-MD refinement cost | ~400 CPU-hours + 60 GPU-hours (average) | compute | per refinement job | 4 |
  | FEP+ simulation time per leg | 50 | ns | protocol | 5 |
  | FEP+ lambda windows | 24 (charge-changing), 16 (core-hopping), 16 (other) | windows | protocol | 5 |
  | FEP+ re-analysis time points | 5, 10, 25 | ns | lowest RMSE picked as final | 5 |

  Two numbers worth flagging as internally awkward. First, **top-1 = 37.15% (p2) and "Boltz
  succeeded in 114/253 (45.06%)" (p3)** are both "success at 2.5 Å" but differ by ~8 points; the
  paper never reconciles them, and the most likely reading is that 37.15% is the top-1-ranked
  pose of the five samples while 114/253 counts the top-*scored model* used for the rescue
  triage — but that reading is not stated. Recorded rather than resolved; see `unresolved`.
  Second, **top-1 37.15% → top-5 44.66% is only a 7.5-point gain for a 5× pose budget**, which
  is a small number the paper does not comment on.

- **n_predictions**:
  - **Sampling setting (stated, p5):** "we generated **five diffusion samples**" per GPCR–ligand
    complex, with "**10 recycling iterations** per the recommendation in the Boltz technical
    report", using Boltz-1x v1.0.0, full-length UniProt receptor sequence and ChEMBL native
    ligand SMILES, default Boltz MSA server. **No seed count, no random-seed policy, and no
    diffusion-step count are reported.**
  - **Targets:** 253 complexes (main), 201 complexes (G-protein arm), 253 complexes (Boltz-2
    arm), 84 complexes (rescue arm), 8 receptors / 14 series (FEP+ arm).
  - **Totals — DERIVED, not stated by the paper:** 253 × 5 = **1,265** Boltz-1x samples for the
    main benchmark; 201 × 5 = **1,005** for the G-protein arm. The Boltz-2 arm re-ran "the
    entire benchmark dataset" (p3) but **samples per complex on that arm are NOT REPORTED**, so
    no total is derivable. The paper never states a total prediction count anywhere.
  - **Models evaluated vs models generated:** Fig. 1 evaluates **1 of 5 per target** (the
    top-scored model, p2) — the other four are invisible in the primary result and reappear only
    in the rescue and FEP+ arms.
  - **Downstream pose counts:** all 5 Boltz samples redocked per rescue case with both Glide and
    IFD-MD (p6); top-5 poses per method assessed, top-10 in the relaxed arm (p3); FEP+ on the
    top-5 IFD-MD poses from each of 5 models = **up to 25 refined poses per receptor–series**
    (p4). Number of Glide/IFD-MD poses actually generated per model before truncation to top-5 /
    top-10 is **NOT REPORTED**.

- **comparable_to_ours**: *(left empty by the extractor per schema v3)*

- **si_in_scope**: **HELD as of 2026-09-10** — the SI DOCX was obtained
  (`../source/si/zhang2026generalization_SI.docx`). **Table S2, the complete list of the 253
  benchmark GPCRs, is extracted** to `../panels/si_tables/zhang2026generalization_tableS2.csv`
  with PDB ID, resolution, GPCR class, GPCR state, ligand CCD, ligand pharmacology, max ligand
  similarity and max sequence similarity per entry; all 253 join to GPCRdb, giving 68 distinct
  receptors. The FEP+ series table is extracted alongside it (15 series with PDB and ChEMBL
  ids). What the table shows that the main text does not: **225 active / 28 inactive, 203 of
  253 G-protein-bound, 215 of 253 agonists** — a benchmark built to test generalisation to
  unseen families is overwhelmingly agonist-bound, active-state and transducer-coupled.
  The per-series FEP+ numbers (their Table S1) are in the file but **not extracted**.

  The paragraph below was written before the SI was obtained and is kept because its
  reasoning about what a missing SI costs is still correct:

  **[superseded] SI NOT HELD — and the gap is material, not cosmetic.** This is a 7-page
  article whose supplementary information is a separate file at the same DOI (p7:
  "Supplementary information The online version contains supplementary material available at
  https://doi.org/10.1038/s44386-026-00066-1") and is not in the corpus. What is missing:
  - **Table S1** — the per-series FEP+ results (R², RMSE, ligand RMSD, pass/fail) for
    experimental, Boltz and IFD-MD structures across all 27 series. Referenced four times (p4).
    Fig. 3 renders 14 series as bars but prints no values.
  - **Table S2** — "a complete list" of the 253 benchmark GPCRs (p4). **Without it none of the
    per-target numbers, PDB IDs, families or similarity values are recoverable**, and only seven
    PDB IDs appear anywhere in the main text.
  - **Fig. S1a / S1b** — the G-protein co-folding arm. The main text carries two medians (1.01 →
    0.75 Å; 0.01 Å) and nothing else: no distributions, no test statistic, no n per bin. **The
    "partners do not fix ligand pose" result, which is the most reusable finding in the paper,
    is a supplementary figure.**
  - **Figs. S2, S3** — the Boltz-2 vs Boltz-1x comparison. Only the test statistics survive into
    the main text.
  - **Fig. S4** — the severe-clash analysis (94.90% / 75.12%).
  - **Fig. S5** — the Series 2 flipped-pose FEP+ map analysis.
  - **Fig. S6** — the post-IFD-MD FEP+ summary.
  - Raw data and prepared MAE files are on Zenodo (10.5281/zenodo.18343531, p6) and code on
    GitHub (p6); neither is held.
  - **Net effect: of the paper's four control arms, two (G protein, Boltz-2) have their entire
    quantitative display in unheld SI.** The main text numbers recorded above are what exists.

## F. Figures

Three main-text figures, split into **seven panel-group rows** by the v3 rule (split on `mark`
or `measure`, not on `facet`). Fig. 1 is a six-panel figure containing three distinct shapes;
Fig. 2 mixes a flow diagram with structure renders; Fig. 3's two panels differ in measure.
All three figure pages were rendered (p2, p3, p5) because the captions are one-liners that do
not carry the panel structure — and the render was necessary: **the Fig. 1f caption is wrong**
(see the `1F` row).

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A+1E | 2 | Receptor Cα RMSD plotted against two candidate predictors of quality — training-set sequence identity (a) and model confidence (e); both are flat, which is the point | scatter | `PLOT \| facet: predictor variable (2: max receptor sequence identity, average per-residue pLDDT) \| vary: predictor value (continuous; 18–70% seq. id. in a, 0.65–0.90 pLDDT in e) \| series: none (1) \| measure: receptor Cα RMSD (Å), 0–17 \| mark: point \| n: 1 per mark; 253 per panel (caption states no n; 253 inferred from the benchmark size and from Fig. 1f bins summing to 253)` | 2 of 6 (a, e). Panels vary by predictor, not by system or view; every point is one benchmark target | Caption gives no n for any panel. R² is printed in the *text* for e (0.046) but not on the panel, and no trend line or fit is drawn on either panel, so the reader cannot see the fit that the R² summarises. Allosteric cases are **not** highlighted in a or e although they are in b–d, so the same points are colour-coded in one panel and not in another | CC BY 4.0, no ND clause — p7: "This article is licensed under a Creative Commons Attribution 4.0 International License, which permits use, sharing, adaptation, distribution and reproduction in any medium or format". Redrawing and modification are permitted with attribution. Third-party material carve-out stated on p7 |
| 1B-D | 2 | Ligand RMSD against three candidate predictors — receptor sequence identity (b), ligand Tanimoto to training (c), ligand volume-overlap with the native ligand (d); allosteric cases in red, and only (d) shows structure | scatter | `PLOT \| facet: predictor variable (3: max receptor sequence identity, max ligand Tanimoto similarity, ligand volume-overlap ratio) \| vary: predictor value (continuous; 18–70%, 0.2–1.0, 0.0–0.95) \| series: ligand site (2: orthosteric — panel-coloured; allosteric — red) \| measure: ligand heavy-atom RMSD (Å), 0–35 \| mark: point \| n: 1 per mark; 253 per panel (caption states no n)` | 3 of 6 (b, c, d) | No n, no fit line, no reported correlation coefficient for any of the three despite the text asserting "no clear trend" (p2) — the null is claimed from visual inspection of these panels with no statistic attached. Allosteric n is never stated, so the reader cannot tell how much of the top of the y-range is one small subgroup. Orthosteric and allosteric ligand RMSDs are computed with **different superposition frames** (p6) yet plotted on one axis, and the caption does not say so | as above (CC BY 4.0, p7) |
| 1F | 2 | Distribution of ligand-RMSD outcome across four ipTM bins — the panel behind the "ipTM is a useful decision metric" claim | bar (100% stacked) | `PLOT \| facet: none (1) \| vary: protein–ligand ipTM bin (4: 0.4–0.6, 0.6–0.8, 0.8–0.95, > 0.95) \| series: ligand RMSD bin (4: 0–0.5, 0.5–1.0, 1.0–2.5, > 2.5 Å) \| measure: ligand RMSD distribution (% of cases in bin), 0–100 \| mark: bar \| n: per bar printed on the axis — 10, 49, 123, 71 (sums to 253)` | 1 of 6 (f). This letter carries a shape found nowhere else in the figure | **The caption misdescribes this panel.** It reads "f Ligand RMSD vs. receptor–ligand ipTM", which describes a scatter; the rendered panel is a 100%-stacked bar of binned outcomes. Consequently **the R² = 0.49 asserted in the text (p3) has no panel showing the point cloud it was computed from** — the reader cannot check a correlation against a binned bar chart. Percentage normalisation also hides that the lowest-ipTM bin holds only 10 cases while the bar is drawn full height, and everything worse than 2.5 Å is compressed into one grey band, so the difference between a 3 Å and a 30 Å error is invisible in the panel that is being used to argue the score is trustworthy | as above (CC BY 4.0, p7) |
| 2A | 3 | Sankey of the triage-and-rescue pipeline with case counts: All Cases (253) → Boltz Success (114) / Boltz Failure (84) / Boltz Wrong Pocket (55); Failure → Glide Success (29) / Glide Failure (55) → IFD-MD Success (16) / IFD-MD Failure (39) | schematic (Sankey flow) | `SCHEMATIC \| Sankey flow of the hierarchical triage and rescue pipeline, nodes labelled with case counts (253 → 114 / 84 / 55; 84 → 29 / 55; 55 → 16 / 39) \| no data` | 1 of 5 (a) | Flow widths are the only encoding and no axis or scale is given, so the counts must be read from the node labels rather than seen. The Sankey shows the **top-5** numbers only; the top-10 variant (36, 52 of 84) is in the text on p3 with no visual counterpart | as above (CC BY 4.0, p7) |
| 2B-E | 3 | Two worked rescue cases: 8IJB Boltz failure → Glide rescue, and 8WC7 Boltz failure → IFD-MD rescue with the Tyr287 sidechain clash resolved | structure render | `RENDER \| facet: case (2: 8IJB, 8WC7) × stage (2: Boltz failure, physics-rescued) \| views: 1 (single close-up of the binding site per panel, camera angle unstated) \| overlay: 1 prediction on 1 reference per panel — native (white), Boltz (green), physics-refined (cyan) \| axis: none` | 4 of 5 (b, c, d, e) | Two hand-picked successes out of 45 rescues and 84 attempts, with **no render of any of the 39 unrescued cases** — the failure mode the paper diagnoses quantitatively (severe clashes, 94.90% / 75.12%) is never shown. No scale bar, no resolution or map context, no indication of how these two were chosen | as above (CC BY 4.0, p7) |
| 3A | 5 | Per-series FEP+ correlation, experimental vs best Boltz vs best IFD-MD structures | bar (grouped) | `PLOT \| facet: none (1) \| vary: series index (14) \| series: starting structure (3: Native, Boltz, IFD-MD; hatched where IFD-MD beats Boltz by > 0.05 R²) \| measure: FEP+ R², 0–1.0 \| mark: bar \| n: 1 FEP+ map per bar; 14 series per panel; ligands per series NOT REPORTED (filters require > 12, p5)` | 1 of 2 (a) | No error bars anywhere — FEP+ R² carries cycle-closure and statistical uncertainty that is not drawn, so bar-height differences of 0.05 (the hatching threshold) are shown as if exact. Ligand count per series is not shown, so each bar's weight is invisible. The 13 series that failed the retrospective screen are absent from the figure entirely, and series indices are unlabelled by receptor, so the reader cannot map a bar to a target without Table S1 (**not held**). "Best" model per arm is a maximum over 5 (Boltz) or 25 (IFD-MD) candidates and the figure gives no hint of the distribution it maximised over | as above (CC BY 4.0, p7) |
| 3B | 5 | Same comparison scored by FEP+ error rather than correlation | bar (grouped) | `PLOT \| facet: none (1) \| vary: series index (14) \| series: starting structure (3: Native, Boltz, IFD-MD; hatched where IFD-MD beats Boltz by > 0.2 kcal/mol) \| measure: FEP+ RMSE (kcal/mol), 0–2.3 \| mark: bar \| n: 1 FEP+ map per bar; 14 series per panel; ligands per series NOT REPORTED` | 1 of 2 (b) | Same defects as 3A: no error bars on a quantity whose statistical error is routinely ~0.2–0.3 kcal/mol — the same order as the hatching threshold — no per-series n, no receptor labels, best-of-N selection invisible. Additionally, the 2.0 kcal/mol pass criterion used to define an FEP+ signal (p4) is **not drawn as a reference line** on the RMSE axis, so pass and fail cannot be read off the panel | as above (CC BY 4.0, p7) |

Figure-page renders performed: **3** (p2, p3, p5). All three were necessary — the captions are
single-clause labels, and rendering p2 is what exposed the Fig. 1f caption error.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5)
- **schema_version**: v3
- **confidence**: **high** on identity, scope, metrics, controls, confidence-discriminator and
  oracle routes — the paper is unusually explicit in its Methods and every number above is a
  direct quote from the text layer. **Medium** on figure `n` values (no caption states n; the
  253-per-panel figure is inferred from the Fig. 1f bin counts summing to 253) and on section C's
  conformational fields, which are mostly not-applicable by the paper's design rather than by
  omission. Text-layer artefacts worth noting for anyone re-quoting: the PDF renders "FEP+" as
  "FEP + " with stray spaces, PDB ID **8X17** appears as "8 × 17" and **8X16** as "8 × 16"
  (a multiplication sign substituted for the letter X), superscript reference numerals are glued
  to the preceding word ("studies24–30", "Boltz11,12"), and the Fig. 3 caption's "i-values"
  is almost certainly "p-values" — quotes above reproduce the text layer as extracted.
- **unresolved**:
  1. **Top-1 success 37.15% (p2) vs "Boltz succeeded in 114/253 (45.06%)" (p3)** — both are
     success at 2.5 Å on the same 253 cases and they disagree by ~8 points. Probably top-1-ranked
     *pose* vs top-*scored model*, but the paper never says. Do not quote both in one sentence
     without resolving.
  2. **Templates** — whether Boltz was run with structural templates on or off is never stated
     (p5). This matters for the leakage argument and is unrecoverable from the PDF; the GitHub
     repo (p6) would settle it.
  3. **Boltz-2 sampling depth** — "we re-ran the entire benchmark dataset with Boltz-2" (p3)
     without stating samples per complex or whether the 5-sample / 10-recycle setting carried
     over. No total prediction count is derivable for that arm.
  4. **"Best Boltz model" and "best IFD-MD models"** (Fig. 3, p5) — the selection criterion is
     stated as "at least one pose with ligand RMSD < 2.5 Å that also passed FEP+ validation"
     (p4), but whether the *plotted* bar is the best-by-R², best-by-RMSE or best-by-RMSD model
     is not stated, and the three need not be the same model.
  5. **"i-values of 0.066 and 0.029"** (p5) — from context these are Wilcoxon p-values, but the
     text says "i-values". Recorded verbatim above; treat as p-values with a caveat.
  6. **Allosteric n** — the number of allosteric-ligand cases among the 253 is never stated,
     although they are highlighted in red in Fig. 1b–d and carry a headline failure claim (p2).
  7. **Which 55 cases are wrong-pocket, and how many of those are the allosteric ones** — not
     stated; needs Table S2 (not held).
  8. **The 27 → 14 series identities** and every per-series number are in Table S1 (not held).
  9. **Tag needed but not in the v3 vocabulary — flagged, not invented:** there is no method tag
     for **physics-based refinement / docking / alchemical free-energy** (Glide, IFD-MD, FEP+),
     which is half of this paper and the whole of its positive result. `md` is used below on the
     strength of IFD-MD and 50 ns/leg FEP+ simulations being genuine MD, but `md` in this corpus
     plainly means MD-for-conformational-sampling and is a poor fit; `enhanced-sampling` is
     arguably right for alchemical FEP but would false-positive metadynamics/REMD queries. A
     `physics-refinement` or `free-energy` tag would be the honest addition. Recorded here rather
     than invented.
  10. **Second tag gap:** there is no tag for **model-version comparison / memorization-by-version**
      (Boltz-1x vs Boltz-2 split by training-set membership). `multi-backbone` is wrong — it is
      one backbone, two versions — and `anti-memorization` covers the design but not the
      version-comparison design that makes this arm distinctive.
  11. **Schema ambiguity, `data_shape`, Sankey diagrams.** A Sankey carries real quantitative
      data (flow widths and node counts) but has no dependent measure, no matrix, no tree and no
      camera view. None of the five v3 forms fits. `SCHEMATIC | ... | no data` is a mild false
      statement — the same objection the v3 changelog raises for TREE at item 6 — and is what
      was used here for want of anything better. **A sixth form (FLOW: nodes / stages / edge
      value) would fix it**, and Sankeys are common in benchmark triage papers.
  12. **Schema ambiguity, panel splitting when `vary` differs.** The v3 rule splits on `mark` or
      `measure` and explicitly not on `facet`, but says nothing about `vary`. Fig. 1a and 1e
      share mark and measure and differ only in which predictor runs along the independent axis.
      They were merged into one row by treating "predictor variable" as the facet — which
      follows the schema's own worked example (`facet: predictor (4)`) — but the rule as written
      does not say to do that, and a different extractor could equally have produced two rows.
      **Recommend stating explicitly that a set of panels differing only in the independent
      variable is a facet over predictors, not a split.**
  13. **Schema ambiguity, `stance` vocabulary for a self-interested benchmark.** This paper is a
      rigorous third-party benchmark of a competitor's model published by the vendor of the
      tools that rescue it (p7 competing interests). None of `precedent` / `contrast` / `threat`
      / `background` captures "credible finding, interested party"; the competing-interest fact
      is recorded in `A. Identity` and `stated_limits` instead. Not a defect to fix urgently,
      but worth knowing the corpus cannot currently sort on it.
- **why_it_matters**: *(left empty by the extractor per schema v3)*

## Tags

`gpcr` `cofolding` `benchmark-only` `md` `ensemble` `single-state` `rmsd-only`
`saturating-metric` `oracle-leak` `design-level-oracle` `anti-memorization`
`confidence-as-discriminator` `partner-driven` `orthosteric` `allosteric-site`
`allosteric-failure` `peer-reviewed` `precedent` `threat` `negative-result`
`comparator-numbers`

Tag notes, so the reverse lookups behave:

- **`md`** is applied on the strength of IFD-MD and of FEP+ at 50 ns per leg (p5) being real
  molecular dynamics, **not** because MD was used for conformational sampling. See `unresolved`
  item 9 — the tag this paper actually needs does not exist.
- **`benchmark-only`** and **`cofolding`** are both applied: the paper runs a co-folding model
  but modifies nothing about it.
- **`multi-backbone` is deliberately NOT applied.** Boltz-1x and Boltz-2 are two versions of one
  model; no second backbone was run.
- **`prospective` is deliberately NOT applied** — see `prospective`, which is `no`.
- **`unpowered` is deliberately NOT applied**: the memorization control runs at n = 180 and the
  primary benchmark at n = 253. (The FEP+ arm at 14 series / 8 receptors is small and its Cliff's
  δ CI for ΔR² crosses zero, but that is an arm, not the anti-memorization control the tag
  governs.)
- **`experimental-validation` is deliberately NOT applied**: no new wet-lab experiment was run.
  Experimental *affinity data* from ChEMBL was used as a computational validation target, which
  is a different thing.
- **`ligand-driven` is deliberately NOT applied**: the native ligand is co-folded in every
  prediction but is never varied as a state handle. **`partner-driven`** is applied because the
  G-protein arm is exactly that experiment — and its result is that the handle moves the receptor
  backbone and not the ligand pose (p2).
- **`allosteric-failure`** is applied with a caveat: the strict v3 definition is "no model or
  setting ever sampled the allosteric site", and this paper's claim is the slightly weaker "Boltz
  performs poorly when predicting allosteric ligands, often forcing them into the orthosteric
  binding pocket" (p2), with some allosteric points falling below the 2.5 Å success line in
  Fig. 1d. Applied because the finding is genuine and a reverse lookup should return it; the
  caveat is here so nobody over-quotes it.
- **`visual-metric` is deliberately NOT applied**: one diagnosis is made by inspection (the 180°
  pose flip, p4) but no conformational state is ever called by eye, and the tag would
  false-positive state queries.
- **`saturating-metric`** refers to the receptor Cα RMSD floor that the authors themselves invoke
  to explain the pLDDT null (p3), not to any axis truncation — axis and display defects are in
  `hides`.
- **`threat`** is provisional and narrow: it attaches to the p3 section headline "Confidence
  scores are useful markers of prediction quality" and the ipTM R² = 0.49 result, not to the
  paper as a whole. The user decides.
