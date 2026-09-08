# sun2026kinconfbench

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–18)**, which coincide with
the printed page numbers of this preprint. Layout: p1 title/abstract, p2–3 Introduction, p3–11
Results (Figure 1 on p5, Figure 2 on p7, Figure 3 on p8, Figure 4 on p9, Figure 5 on p11),
p11–12 Discussion, p12–13 Materials and Methods, p13 SI pointer / data availability, p14–18
references.

**Supplementary Information is NOT in the held PDF.** The PDF ends at the reference list on
p18. Supplementary Figures S1–S4 and Supplementary Tables S1–S4 are cited throughout and hold
the paper's exact per-model Top-K numbers (Table S3), the 110-system joint-failure list
(Table S4), the label-validity check (Table S2) and the geometric distributions (Figure S2).
See `si_in_scope`.

**Version caveat, recorded up front because it affects `A. Identity`:** the held PDF is the
bioRxiv preprint posted 10 April 2026. The task brief states this work has since appeared in
*npj Drug Discovery* (`10.1038/s44386-026-00068-z`). Nothing inside this PDF says so; the
published version was not read. See `unresolved`.

---

## A. Identity

- **citekey**: `sun2026kinconfbench`
- **doi**: **10.64898/2026.04.07.716788** (bioRxiv) — p1 banner: "bioRxiv preprint doi:
  https://doi.org/10.64898/2026.04.07.716788; this version posted April 10, 2026". `refs.bib`
  and `MANIFEST.csv` carry the same DOI. Note the `10.64898` prefix rather than bioRxiv's
  usual `10.1101`; recorded as printed, see `unresolved`.
- **year**: **2026** — posted 10 April 2026 (p1).
- **venue**: **bioRxiv preprint, not peer reviewed.** p1: "The copyright holder for this
  preprint (which was not certified by peer review) is the author/funder, who has granted
  bioRxiv a license to display the preprint in perpetuity." Tagged `preprint` on the evidence
  of this PDF. A peer-reviewed *npj Drug Discovery* version is reported to exist but was not
  read — see `unresolved`; do **not** tag `peer-reviewed` on the basis of this PDF.
- **title**: KinConfBench: A Curated Benchmark for Cofolding Models on Kinase Conformational
  States — p1
- **authors**: Kunyang Sun and Teresa Head-Gordon (both corresponding: kysun@berkeley.edu;
  thg@berkeley.edu) — p1. Pitzer Theory Center and Dept. of Chemistry / Bioengineering /
  Chemical and Biomolecular Engineering, UC Berkeley. Two authors only. Contributions (p13):
  "KS conceived the project and wrote the code and performed all computational experiments.
  KS and THG did all analysis and wrote the paper."

## B. Scope

- **system**: **protein kinase** — human protein kinase catalytic domains exclusively.
  p3: "we introduce KinConfBench, a curated benchmark of 2,225 high-quality human kinase
  chains". Only catalytically competent kinase domains; pseudokinase domains are explicitly
  removed (p4: "we use the reference sequences of the active kinase domains extracted from
  UniProt to selectively retain only the catalytic units while excluding pseudokinase
  domains"). No GPCRs, transporters or non-kinase systems anywhere.
- **n_targets**: multi-level; record all four, because a single number misrepresents the scale:
  - **437** catalytically active human kinase domains seed the query (p3, following Faezov &
    Dunbrack [34]).
  - **2,225** structurally unique kinase chains in the final benchmark (p4–p5): 236 unique apo
    chains + 1,989 unique holo chains.
  - **1,420** unique kinase *systems* actually run through inference (p3, p13): "43 unique apo
    targets and 1,377 unique holo complexes".
  - **Analysis subsets are much smaller and are conditioned on model success:** 950 systems
    pass the geometric filter for the KinCoRe-correctness analysis (p6); 509 systems form the
    ensemble-diversity subset (p9); **234** holo/apo pairs enter the apo-drift analysis, split
    per model into train/test as 212/22 (Boltz-2), 182/52 (Chai-1), 194/40 (Protenix) (p11
    Figure 5 caption).
  - **Generality flag:** the paper's conclusions are framed for cofolding models and SBDD in
    general ("critical for next-generation structure-based drug discovery", p1) but rest
    entirely on one protein family. The authors state this scoping themselves (p12).
- **method_class**: **benchmark-only.** The paper builds and curates a benchmark dataset and
  evaluates three existing cofolding models; it proposes no new predictor and modifies no
  inference pipeline. p12–13: "we adhere to the official inference pipelines for each method
  to represent standard usage scenarios."
- **backbones**: **Boltz-2 [15], Chai-1 [13], Protenix [16]** — three open-source cofolding
  models compared head to head on identical inputs (p3, p6, p13). **Tag `multi-backbone`.**
  No AF2, AF3, Chai-2, OpenFold or NeuralPLexer inference is run; AF3 and NeuralPLexer appear
  only as citations, and AF2 only via Faezov & Dunbrack's precomputed 437-domain set used for
  *target selection*, not for prediction.
- **templates**: **NOT REPORTED.** The word "template" appears in the paper only in the
  biological sense ("common templates of the global fold", p3). Methods (p12–13) state MSA
  handling and sample count but never say whether each model's structural template channel was
  on, off, or left at repository default. Since the stated protocol is "we adhere to the
  official inference pipelines for each method", the setting is whatever each repository
  defaults to, which is not stated. Do not infer. Consequence: no protocol tag is applied.
- **msa_handling**: **full, default per model.** p12–13: "Multiple Sequence Alignments (MSAs)
  are generated and cached with each tool's default databases and pairing strategies. For
  Boltz-2, Chai-1, and Protenix, the ColabFold server [3] is used for MSA generation, while
  sequence pairing follows the defaults of the respective model repositories." **No
  subsampling and no state-filtering** — this is the unmodified default-depth regime, which is
  what makes it a clean benchmark of stock model behaviour rather than a biasing study.
  Input sequences are trimmed: "Input sequences are restricted to the canonical kinase domain
  boundaries defined by UniProt, so that the benchmark stresses domain-level cofolding
  behavior" (p12–13).

## C. Conformational core

- **states_generated**: **ensemble + single-state.** This is the dual case the v3 field exists
  for, and the collapse is the paper's actual result.
  - *Ensemble* by construction: "To ensure robust sampling of the conformational landscape, we
    generate N = 20 cofolding samples per target for each inference run" (p13).
  - *Single-state* in outcome, on two independent measurements:
    - **Mode collapse across the ensemble** (p7): "Figure 2(c) shows that, despite the increase
      in accuracy, the co-folding model predictions are largely bimodal. This mostly all-right
      or all-wrong pattern suggests ensemble mode collapse rather than graded uncertainty
      within the twenty samples." Figure 2c shows >500 of 950 systems in the 20/20 bin and
      ~175 in the 0/20 bin for Boltz-2 and Protenix (p7).
    - **Negligible intra-basin diversity** (p9): "all models produce very small structural
      deviations of ∼0.1 Å for the distance metrics and less than 5° average angle exploration
      except for Chai-1's performance on Asp χ2", against a stated reference scale of "root
      mean square fluctuations of ∼1-2 Å and backbone or side chain dihedral angle ranges of 5°
      to 30°" for ordinary thermal fluctuation (p9–10).
  - Note the structures are generated by the three evaluated models, not by a method of the
    authors' own; the authors ran the inferences (p13).
- **structural_priors_used**: **Heavy, and entirely legitimate for a benchmark — this is where
  the deposited-structure dependence belongs, not in `oracle_leakage`.**
  1. **The Modi–Dunbrack kinase nomenclature** as the state ontology: p3, "we employ the
     structural nomenclature developed by Modi and Dunbrack [31], labeling kinase chains with
     categorical structural features to capture specific active and inactive conformations."
     Eight categorical labels (spatial/DFG, dihedral/X-DFG, helix/αC, salt bridge, N- and
     C-terminal activation loop, spine, activity), enumerated p3–4.
  2. **The KinCoRe / Kincore software suite** [35, 36] as the classifier: p3, "we process all
     chains from the identified entries using the KinCoRe software suite [35, 36]."
  3. **Faezov & Dunbrack's 437 catalytically competent human kinase domains** [34] as the
     target list: p3, "we first identify 437 catalytically active human kinase domains and
     their corresponding UniProt [33] identifiers, following the classification established by
     Faezov and Dunbrack [34]."
  4. **The PDB itself** as the entire universe of systems: p3, RCSB "(snapshot 2025-08-01)",
     7,763 raw entries.
  5. **UniProt canonical kinase domain boundaries** define the input sequence (p12–13).
  6. **The 12 experimentally observed KinCoRe label combinations** as the space of allowed
     answers: p6, "KinCoRe assigns each kinase protein structure to valid spatial and dihedral
     label combinations (36 theoretical, 12 observed in the PDB; Supplementary Table S1)".
- **oracle_leakage**: **Present, but entirely on the EVALUATION and SELECTION side, not on the
  input side.** No knowledge of the target state reaches the models: their input is the kinase
  domain sequence plus the ligand SMILES, with a default full MSA and no state-annotated
  template (p12–13). Route-by-route:

  - **Route 1 — structures used as input or template: NONE FOUND at the benchmark level, with
    one gap.** The protocol is described p12–13; input is sequence + ligand only, per the
    abstract (p1): "cofolding models can generate global folds directly from kinase sequences
    and ligand SMILES strings". No experimental structure is fed to any model. *Gap:* whether
    each repository's default enables a PDB template search is never stated (see `templates`),
    so route 1 cannot be closed with full confidence from this PDF. Also note every reference
    structure is in the PDB and the models were trained on the PDB — training-set memorization
    is the paper's own subject matter, not a protocol leak (p10).
  - **Route 2 — state annotations from a curated database (Kincore) driving templates or
    alignments: NONE FOUND as a pipeline driver; PRESENT as the ground-truth definition.**
    KinCoRe is run on the *outputs*, never on the inputs. p6: "By applying the KinCoRe labels
    to every prediction, we establish a 'ground truth' based on the categorical orientation of
    the DFG motif and the αC-helix, providing a more functionally relevant metric than standard
    backbone RMSD." p13: "Post-inference, structures are passed through the Dunbrack KinCoRe
    annotation pipeline". The reference labels come from running the same classifier over the
    **deposited** chains (p3: "To assign conformational labels to the selected kinase PDB
    entries, we process all chains from the identified entries using the KinCoRe software
    suite"). So the database supplies the scoring function, symmetrically applied to prediction
    and to deposited reference, and never conditions the model. This is the single most
    important distinction in the note.
  - **Route 3 — cluster labels derived from known states: PRESENT, at dataset construction.**
    The benchmark's de-duplication and its retention of "meaningful structural diversity" are
    driven by the KinCoRe labels of deposited structures. p4: "we remove trivial redundancies,
    defined as entries sharing identical sequences (and ligand SMILES, where applicable)
    alongside identical KinCoRe conformational labels. Nevertheless, we preserve meaningful
    structural diversity by retaining any entry that exhibited at least one unique KinCoRe
    label relative to others of the same condition." The evaluation set is therefore shaped by
    the answer key; the model is not.
  - **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
    states: PARTIALLY PRESENT.**
    - *Not tuned:* the geometric thresholds are borrowed, not fitted. p6: "We define a
      geometrically successful prediction as one with global fold lDDT-Cα ≥ 0.7, binding pocket
      lDDT-PLI ≥ 0.8, and ligand RMSD < 2.0Å following the definition of previous works
      [2, 17]." N = 20 is fixed for all targets and all models (p13).
    - *Tuned on the evaluation outcome:* the diversity-subset cut is chosen so the models come
      out comparable. p9: "we focus on the 509 systems where Boltz-2, Chai-1, and Protenix each
      have at least ten all-correct structures according to KinCoRe in the top-20, so every
      cofolding method contributes a comparably populated success set based on classification."
      The "at least ten" threshold is set against results already computed on the evaluation
      set. Under the v3 clarification (tuning a *range* on the evaluation set is leakage even
      with no per-target value), this counts.
  - **Route 5 — success defined post hoc by RMSD/lDDT to a structure they had: PRESENT and
    load-bearing.** Both success definitions are defined against the held deposited structure,
    and the analysis set itself is conditioned on model success. p6: "Out of 1420 protein-
    ligand kinase systems, geometric filtering resulted in only 950 kinase where all cofolding
    models produce at least one geometrically valid pose out of 20 samples for downstream
    analysis." And p6: "a prediction is only considered 'correct' if all eight KinCoRe labels
    match those of the experimental structures." A softening clause is applied in the same
    direction (p7 caption): "we consider a prediction successful if it matches any valid set of
    ground truth labels associated with that protein-ligand complex." This is inherent to any
    retrospective benchmark and is not concealed, but it is route 5 and must be recorded.
  - **Route 6 — best/worst model labels assigned against a held reference: PRESENT.** The hard
    case and the failure list are both defined by disagreement with the reference. p8:
    "Supplementary Table 4 contains the 110 kinases where all three cofolding models fail to
    generate the correct conformation" and "Figure 3 highlights MAP4K1/YK1 (PDB ID: 7M0M) [42]
    as a representative hard case where all cofolding model predictions fail to obtain an
    induced-fit to the correct conformational state." Which of the 20 samples per model is the
    "representative" one rendered in Figure 3 is **NOT REPORTED** (p8 caption says only
    "representative Boltz-2 (green), Chai-1 (orange), and Protenix (blue) predictions").
  - **Route 7 — design-level oracle use (systems or conditions chosen because the answer is
    already known): PRESENT and explicit, and this is the strongest design-level statement in
    the paper.** p10: "We extract kinase systems from KinConfBench that possess resolved
    structures for both states, restricting our analysis to systems where the ligand induces a
    distinct structural change defined as a different set of KinCoRe functional labels compared
    to ligand-free structures." Every apo-drift system is one where the correct holo answer and
    the wrong apo answer are both already deposited and already labelled. Weaker than pipeline
    leakage, and correct practice for a benchmark, but it must be labelled as design-level.

  **Verdict in one line:** model inputs are clean (sequence + SMILES, default full MSA, no
  state-annotated template, no state-filtered alignment), and every oracle route that fires —
  3, 4 (partly), 5, 6, 7 — fires on the evaluation, selection or presentation side, which is
  what a retrospective benchmark is; route 2's Kincore dependence is a *scoring function*
  symmetrically applied to prediction and deposited reference, not a pipeline driver.

- **prospective**: **no.** Fully retrospective. Every target is a deposited PDB entry from a
  2025-08-01 snapshot (p3); every reference state, apo and holo, was solved before the
  analysis; success is defined by match to the deposited answer (p6). The apo-drift test set is
  *post-training-cutoff for the models* but not prospective for the authors — the structures
  already existed when the benchmark was built (see `anti_memorization_design`). No prediction
  is made about an unsolved system and no experiment is run.
- **state_metric**: **binary predicate + continuous coordinate** (with RMSD-to-reference used
  as a pre-filter, not as the state call).
  - *Binary predicate (primary):* exact 8-of-8 categorical label match. p6: "a prediction is
    only considered 'correct' if all eight KinCoRe labels match those of the experimental
    structures." Relaxed to any-of-set where an entry carries multiple valid label sets (p7
    caption). No threshold to state — it is a categorical identity test.
  - *Continuous coordinate (secondary, diversity only):* p8–9, "we extend our analysis beyond
    discrete accuracy to measure the structural dispersion within ensembles ... on a continuous
    scale for distances and dihedral angles as described in Supplementary Information."
    Twelve descriptors: Lys–Glu distance, salt bridge distance, spine distance, DFG–HRD
    distance, and Asp/Phe φ, ψ, χ1, χ2 (Figure 4, p9). Measured as within-ensemble standard
    deviation. Interpretive reference scale is stated but not used as a threshold: "root mean
    square fluctuations of ∼1-2 Å and backbone or side chain dihedral angle ranges of 5° to 30°
    define the statistical fluctuations of stable protein conformations [43, 44]" (p10).
  - *RMSD/lDDT-to-reference (pre-filter):* lDDT-Cα ≥ 0.7, lDDT-PLI ≥ 0.8, ligand heavy-atom
    RMSD < 2.0 Å, justification "following the definition of previous works [2, 17]" (p6).
    **The paper's central negative claim is precisely that this metric family does not
    determine the state call** — p1: "geometric success metrics of a ligand pose in the active
    site does not correlate strongly with the correct kinase conformational state".
  - *Not visual:* Figure 3 is a superposition, but the failure it illustrates is called by the
    KinCoRe predicate, not by eye. Do not tag `visual-metric`.
- **metric_saturation**: **YES — numeric, in three arms.**
  1. **All three geometric metrics are censored at their filter thresholds by construction.**
     Only predictions passing lDDT-Cα ≥ 0.7, lDDT-PLI ≥ 0.8 and ligand RMSD < 2.0 Å enter
     Figure 2a (p6), so the plotted distributions floor at 0.7 and 0.8 and ceiling at 2.0 Å.
     In Figure 2a (p7) the ligand-RMSD outlier mass piles into an unresolvable band against the
     2.0 Å boundary in all nine sub-panels, and the lDDT-PLI boxes sit against 0.8. The metric
     cannot separate correct from incorrect below/above the cut because that region was
     removed. Cross-reference the `hides` entry for figure row 2A, which is the axis-pinning
     half of the same problem.
  2. **The top-20 correctness count ceilings at 20** (Figure 2c, p7). >500 of 950 systems fall
     in the 20/20 bin for Boltz-2 and ~475 for Protenix; the metric cannot express "more
     reliably correct than 20 out of 20", so between-model differences at the top are
     compressed. The paper reads this saturation as the *result* (mode collapse), which is a
     defensible use, but the ceiling is real.
  3. **The Top-K success curve is near-plateau within the sampled range** (Figure 2b, p7): all
     three curves are visually flat from K ≈ 10 to K = 20, so the K = 20 endpoint approximates
     the asymptote for these models rather than a still-rising value.
- **directional_control**: **NONE — sampling only.** No handle exists in this study by which a
  model can be instructed which kinase state to produce. The only conditioning input is the
  **ligand SMILES** (p1: "directly from kinase sequences and ligand SMILES strings"), and the
  paper's finding is that this handle largely fails to steer the state: p10, models
  "effectively 'drift[] back' to the unperturbed, default apo state." The only ensemble handle
  exercised is repeated sampling, N = 20 per target (p13). No seed sweep, no MSA depth sweep,
  no state-annotated template, no partner, nanobody, peptide or G-protein mimetic. Ranking
  within the ensemble uses pLDDT (p7 caption), which is a selection handle, not a directional
  one.
- **anti_memorization_design**: **YES — a per-model, deposition-date time split, with the
  cutoff stated explicitly for each model.** p10: "For each cofolding model, we define training
  and test sets based on a time split relevant to each model: a holo ligand combination counts
  as part of the test set if it first appears in the PDB only after that method's training-data
  deposition cutoff: Boltz-2 (2023-06-01); Chai-1 (2021-01-12); Protenix (2021-09-30))."
  - **n (test / train systems), from the Figure 5 caption, p11:** Boltz-2 **22** test / 212
    train; Chai-1 **52** / 182; Protenix **40** / 194. Each model sees the same 234 holo/apo
    pairs, split differently because the cutoffs differ.
  - **Eligibility rule for the pair set** (p10): only systems with resolved apo *and* holo
    structures whose KinCoRe labels differ — i.e. only systems where a real induced-fit shift
    is documented.
  - **Critical asymmetry, stated by the authors** (p10): "All apo-state structures are found in
    the training data for all cofolding models." Only the holo half of each pair is ever
    held out.
  - Note there is **no held-out split anywhere else in the paper** — the 950-system correctness
    analysis (p6) and the 509-system diversity analysis (p9) use all deposited data with no
    date filter, so all Figure 2 and Figure 4 numbers are in-distribution for at least some of
    the models.
- **anti_memorization_control**: **CONTROL ARM ACTUALLY RUN AND ANALYSED — one of the few
  papers in the corpus where this is true — but mark `UNPOWERED` on the overlap clause.**
  - *Run:* Figure 5 (p11) reports the four-way outcome distribution separately for the train
    split and the test split, per model, and the text compares them: p11, "when comparing to
    the test set distribution in Figure 5b against the training set, the stacked profiles
    further shift toward Apo-only and Dual-Match segments relative to the training
    systems—most clearly for Boltz-2 and Protenix—consistent with apo-drift when confronted
    with new holo states unsupported in the training statistics." Restated in the Discussion,
    p12: "After the training cutoff (specific to each model), we find that the holo state
    prediction rates fall and apo drift rises for each architecture." This is a genuine control
    arm, not a held-out set left unused.
  - *`UNPOWERED`, on the v3 overlap clause:* the held-out set overlaps training by explicit
    statement — "All apo-state structures are found in the training data for all cofolding
    models" (p10) — so each test pair is half in-training. On the n clause the arm passes
    (22 / 52 / 40 all exceed ~10), though Boltz-2's n = 22 means one system moves a stacked bar
    by ~4.5 percentage points, and the model on which the effect is called "most clearly"
    visible is the one with the smallest test n.
  - *No inferential statistic:* no test, confidence interval or error bar accompanies the
    train-vs-test comparison anywhere in the text or in Figure 5. The claim is read off the
    stack heights.
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Label-validity check: every prediction from every model falls inside the 12 KinCoRe label combinations observed in the PDB (Supplementary Table S2) | Rules out gross geometric nonsense or "forbidden" kinase geometries as the cause of mislabelling — the models are producing plausible states, just the wrong ones | p6 |
  | Geometric pre-filter: only the 950 of 1,420 systems where **all three** models produce ≥1 pose at lDDT-Cα ≥ 0.7, lDDT-PLI ≥ 0.8, ligand RMSD < 2.0 Å | Rules out bad ligand placement / failed docking as the explanation for wrong conformational state; also equalises the three models' input sets | p6 |
  | Correct-vs-incorrect geometric comparison (Figure 2a) | Rules out the hypothesis that geometric scores discriminate state correctness — "mislabeled states can still achieve strong ligand-centric structural scores around the binding pocket" | p6–7 |
  | Top-K sweep, K = 1…20 by pLDDT rank (Figure 2b) | Rules out "one unlucky top-1 sample" and quantifies how much of the failure is a ranking failure vs a generation failure (+11.4 / +12.6 / +12.1 pp) | p7 |
  | Per-system histogram of correct-count out of 20 (Figure 2c) | Rules out graded/calibrated uncertainty as the alternative to mode collapse — the distribution is bimodal at 0 and 20 | p7 |
  | Equal-success-set diversity subset: 509 systems where **each** model has ≥10 all-correct structures in the top-20 | Rules out the artefact that a model with fewer correct poses would trivially show less measured dispersion | p9 |
  | Supplementary Figure S4: all models recover the correct **average** distances and angles | Rules out a systematic geometric offset, isolating *variance* (not accuracy) as the diversity defect | p9 |
  | External reference scale: literature RMSF ∼1–2 Å and dihedral ranges 5°–30° for stable proteins [43, 44] | Rules out the reading that ∼0.1 Å / <5° dispersion is normal thermal breadth | p9–10 |
  | Three architectures run head to head on identical inputs | Rules out an architecture-specific artefact; "Memorization of apo kinase states is shared across Boltz-2, Chai-1, and Protenix rather than unique to one model" | p3, p12 |
  | Per-model deposition-date train/test split (Figure 5) | Rules out the reading that apo-drift is a general modelling limitation rather than a memorization effect — the drift worsens specifically past each model's own cutoff | p10–11 |
  | Dataset-composition check against the PDB at large (Figure 1b) | Rules out an idiosyncratic benchmark composition — "This composition closely mirrors the broader distribution of kinases in the PDB, reflecting the data landscape encountered by co-folding models during training" | p4 |
  | Exclusion arms during curation: mutants (1,915), covalent complexes (428), phosphorylated chains, pseudokinase domains, NMR structures, resolution > 4.5 Å | Rules out confounds from sequence perturbation, covalent tethering, PTM-driven state change, non-catalytic domains and low-quality coordinates | p4 |

  **Not run, and worth naming:** no apo-input control arm is analysed in the apo-drift section
  (all 20 samples come from the **holo** sequence-ligand input, p10) — there is no arm showing
  what these models predict when given the apo sequence alone, which would establish the "apo
  baseline" the drift argument assumes. No decoy or scrambled-ligand arm. No seed or MSA-depth
  sensitivity arm.
- **confidence_as_discriminator**: **YES, used — and explicitly found wanting; the negative
  result is one of the paper's headline findings.**
  - *Used:* pLDDT ranks the ensemble for every Top-K number. p7 caption: "For each target, we
    evaluate an ensemble of N = 20 generated structures, ranked by their pLDDT confidence
    scores."
  - *Found wanting:* p3, "The resulting metrics show that high confidence in the active site
    geometry does not ensure high confidence in predicting the kinase conformational states,
    especially when ligands perturb the kinase away from common templates of the global fold."
    p11: "Framing success purely through the highest-confidence structure therefore obscures a
    clinically relevant failure mode: models can 'look' bound while adopting the wrong
    regulatory layout for the ligand at hand." The 11–13 pp Top-1→Top-20 gain (p7) is the
    quantitative form: the confidence ranking puts a wrong-state structure first in >11% of
    systems where a right-state structure exists in the ensemble.
  - *Validated as a use?* Yes, in the negative sense that matters: the ranking's discriminative
    power is measured against the KinCoRe ground truth rather than assumed. The prescription
    follows, p12: "Closing this gap likely demands both better generative breadth for rare
    induced-fit basins and confidence objectives that reward state discrimination, not only
    ligand-protein pocket aligned metrics."

## D. Claims

- **central_conclusion**: Three state-of-the-art cofolding models (Boltz-2, Chai-1, Protenix)
  reach only ~65–75% accuracy at reproducing the experimentally observed KinCoRe conformational
  state of a human kinase from sequence plus ligand SMILES, and their geometric success metrics
  (lDDT-Cα, lDDT-PLI, ligand RMSD) do not predict whether the state is right. Beyond that
  accuracy ceiling, the ensembles are pathological in two ways: they are bimodally all-right or
  all-wrong across 20 samples (mode collapse), and even the all-correct ensembles show
  within-basin dispersion an order of magnitude below ordinary thermal fluctuation. On holo/apo
  pairs whose holo structure post-dates each model's training cutoff, all three increasingly
  predict the ligand-free apo state despite the ligand being present — "apo-drift" — which the
  authors read as memorization of apo baselines rather than learned induced-fit physics.
- **necessity_claims** (verbatim + page):
  - p1: "Our results highlight that capturing ligand-induced protein conformational diversity,
    not just geometric fit, is critical for next-generation structure-based drug discovery."
  - p2: "In practical drug discovery, identifying the correct global fold is necessary but not
    sufficient; successful lead optimization requires capturing the specific induced-fit
    conformational states dictated by ligand binding."
  - p2: "Without a focused assessment of this conformational response, there remains a critical
    gap in understanding whether cofolding models can truly drive rational drug design."
  - p3: "Consequently, it is imperative and timely to evaluate the capacity of cofolding models
    to provide biophysically valid structural hypotheses, specifically by quantifying how well
    they capture the kinase conformational landscape and generalize across unseen
    ligand-induced states for drug discovery."
  - p5: "as the DFG-in/BLAminus configuration is a structural prerequisite for kinase activity"
  - p6: "we evaluate not only the ligand-centric geometric performance of the cofolding models,
    but establish the necessity of providing conformational selection metrics to enable drug
    selectivity for kinase targets."
  - p6: "Valid and conformationally diverse protein folded states is a fundamental prerequisite
    for the meaningful use of cofolding models."
  - p6: "indicating that geometry alone is an incomplete proxy for robust cofolding
    prediction."
  - p10: "while significantly higher values would be needed to indicate transitions between
    distinct conformational states."
  - p11: "None of the three cofolding models eliminates the need for external checks when
    structure-activity-relationships involving induced fit critical motions are required"
  - p12: "Closing this gap likely demands both better generative breadth for rare induced-fit
    basins and confidence objectives that reward state discrimination, not only ligand-protein
    pocket aligned metrics."
  - p12: "At its core, drug discovery requires conformational state correctness rather than
    solely fold correctness or memorization of training instances. Predicting the general
    architecture of a kinase is biologically insufficient if the specific, ligand-induced
    functional conformation is wrong."
  - p12: "Moving beyond static snapshots to dynamic, competitive scenarios will be essential
    for evolving these tools from structural prediction engines into true computational assays
    for drug discovery."
  - p13: "To ensure robust sampling of the conformational landscape, we generate N = 20
    cofolding samples per target for each inference run."
- **novelty_claims** (verbatim + page):
  - p1: "While cofolding models can generate global folds directly from kinase sequences and
    ligand SMILES strings, these models have not yet been tested on their ability to recover
    ligand induced-fit conformational states of the kinase proteins." *(priority claim — the
    "not yet been tested" formulation is the load-bearing one)*
  - p1: "Here, we introduce KinConfBench, a curated benchmark of 2,225 high-quality human
    kinase chains to evaluate the ability of three state-of-the-art cofolding models—Boltz-2,
    Chai-1, and Protenix—to recover both canonical and rare conformational states."
  - p1: "We show that geometric success metrics of a ligand pose in the active site does not
    correlate strongly with the correct kinase conformational state, motivating a new set of
    dynamical benchmarks for assessing cofolding models."
  - p2–3: "However, while these benchmarks successfully identify domain-specific challenges,
    they largely overlook a more fundamental requirement of modern SBDD: the capacity for
    ligand-modulated conformational reasoning."
  - p3: "In this work, we introduce KinConfBench, a curated benchmark of 2,225 high-quality
    human kinase chains representing a total of 1,420 unique kinase systems (43 unique apo
    targets and 1,377 unique holo complexes), designed to shift the evaluation focus from
    ligand RMSD to protein-ligand conformational fidelity."
  - p3: "We further document a critical generalization gap on kinase holo-apo pairs."
  - p8: "Supplementary Table 4 contains the 110 kinases where all three cofolding models fail
    to generate the correct conformation, providing an important benchmark for future cofolding
    model improvements."
  - p12: "KinConfBench is meant to keep that standard explicit as cofolding models continue to
    mature."
- **stated_limits**:
  - **Scope restricted to WT, non-covalent, unphosphorylated domains** — p12: "Our current work
    focuses on the interaction between wild-type domains and non-covalent inhibitors, yet
    kinase signaling is tightly modulated by post-translational modifications (PTMs) and
    somatic mutations." Mutants (1,915 chains) and covalent complexes (428 chains) were
    explicitly excluded (p4), and phosphorylated chains removed (p4).
  - **PTM and drug-resistance mutation effects untested** — p12: "Future benchmarks should
    rigorously assess whether cofolding models can predict how phosphorylation at specific
    regulatory sites or drug-resistant mutations alter the conformational ensemble."
  - **Covalent inhibitors untested** — p12: "the rise of covalent inhibitors in oncology
    necessitates a focused evaluation of how cofolding models handle the shift in protein
    context when a covalent bond is formed".
  - **Single-ligand, non-competitive setting only** — p12: "In a physiological environment,
    kinases are rarely isolated with just a single ligand... Future generations of benchmarks
    should evaluate the ability of models to handle multi-ligand scenarios".
  - **Systems with malformed outputs are dropped** — p13: "targets that failed annotation
    because of malformed outputs or missing motifs are excluded." The count dropped is
    NOT REPORTED.
  - **Class imbalance in the source data acknowledged** — p5: "This observation indicates a
    persistent bias in the PDB toward holo complexes where the ligands occupy the ATP-binding
    pocket in catalytically active states". Also p4: "while there appears to be a balanced
    global distribution between active and inactive states across the entire dataset, it is
    worth noting that this ratio can vary quite significantly at an individual gene level."
  - **Not stated by the authors, and worth recording as an unacknowledged limit:** the small
    post-cutoff test n (22 / 52 / 40); the fact that all apo references are in training; the
    conditioning of the main analysis on the 950 systems where all three models already
    succeeded geometrically; and the unstated template setting.
- **stance**: **`precedent` on findings + `background` on framing.** Provisional — the user's
  call, not settled here.
  - *Precedent on findings:* this paper independently documents, on 2,225 kinase chains and
    three backbones, the exact failure triad a conformational-control method exists to fix —
    mode collapse across a 20-member ensemble, within-basin dispersion an order of magnitude
    below thermal, and memorization-driven reversion to the apo state on post-cutoff holo
    complexes. It supplies the negative baseline rather than competing for the same result.
  - *Background on framing:* it is benchmark-only. It proposes no method, exercises no
    directional handle, and offers no state-control mechanism, so it cannot be a `threat`;
    it defines the problem statement and hands over a public dataset and a 110-system
    joint-failure list.
  - *Not `contrast`:* the paper's rigour is not the weak point one would argue against — its
    inputs are clean, its control arms are numerous and its limits are stated. The arguable
    rigour gaps (test n, apo-in-training, success-conditioned analysis set) are recorded above
    but are not the axis on which one would set a contrast.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Kinase conformational classification accuracy, all models | ∼65–75 | % | 8-of-8 KinCoRe label match to deposited reference | p1 |
  | Top-1 → Top-20 accuracy gain, Boltz-2 | +11.4 | percentage points | same, top-K by pLDDT rank, K = 1 vs 20 | p7 |
  | Top-1 → Top-20 accuracy gain, Chai-1 | +12.6 | percentage points | same | p7 |
  | Top-1 → Top-20 accuracy gain, Protenix | +12.1 | percentage points | same | p7 |
  | Top-20 system success rate, Boltz-2 / Protenix / Chai-1 | ≈82 / ≈81 / ≈76 (read off Figure 2b; exact values are in Supplementary Table S3, **not held**) | % of 950 systems | same | p7 |
  | Top-1 system success rate | **NOT REPORTED numerically** in the main text; ≈70.6 / ≈69 / ≈63.4 by subtracting the stated gains from the Figure 2b endpoints — derived, not printed | % of 950 systems | same | p7 |
  | Sampling-count effect (accuracy vs K) | monotone rise from K = 1, visually plateauing by K ≈ 10–15, all three models | % vs K (1–20) | Figure 2b curve | p7 |
  | Ensemble bimodality | >500 of 950 systems at 20/20 correct and ≈175 at 0/20 (Boltz-2); ≈475 and ≈180 (Protenix); ≈400 and ≈225 (Chai-1) — read off Figure 2c | number of systems per bin | count of top-20 samples matching all 8 labels | p7 |
  | Within-ensemble distance dispersion, all models | ∼0.1 | Å (std. dev. across 20-member ensemble) | 509-system diversity subset, all-label-correct poses only | p9 |
  | Within-ensemble angle dispersion, all models | < 5 (exception: Chai-1 Asp χ2, median ≈7, upper quartile ≈12 from Figure 4) | ° (std. dev.) | same | p9 |
  | Reference scale for "normal" fluctuation (literature, refs 43–44) | RMSF ∼1–2 Å; dihedral ranges 5–30 | Å; ° | stable protein conformations | p10 |
  | Apo-drift, training split: Holo-State fraction | ≈40 (Boltz-2, Protenix); ≈30 (Chai-1) | % of systems | KinCoRe match to deposited holo, 0 matches to apo | p11 |
  | Apo-drift, training split: Apo-Drift fraction | ≈40, all three models | % of systems | KinCoRe match to deposited apo, 0 matches to holo | p11 |
  | Apo-drift, test split (post-cutoff): Holo-State fraction | ≈9 (Boltz-2); ≈25 (Chai-1); ≈22 (Protenix) — read off Figure 5 test panel | % of systems | same | p11 |
  | Training-data deposition cutoffs | Boltz-2 2023-06-01; Chai-1 2021-01-12; Protenix 2021-09-30 | date | first PDB appearance of the holo ligand combination | p10 |
  | Apo-drift split sizes (train / test systems) | Boltz-2 212 / 22; Chai-1 182 / 52; Protenix 194 / 40 | systems | holo/apo pairs with differing KinCoRe labels | p11 |
  | Geometric success thresholds | lDDT-Cα ≥ 0.7; lDDT-PLI ≥ 0.8; ligand RMSD < 2.0 | unitless; unitless; Å | deposited complex, following refs [2, 17] | p6 |
  | Geometric filter yield | 950 of 1,420 (66.9%) | systems where all three models give ≥1 valid pose in 20 | geometric thresholds above | p6 |
  | Joint-failure set | 110 | kinases where all three models fail on state | 8-of-8 KinCoRe match; list in Supplementary Table S4, **not held** | p8 |
  | Diversity subset | 509 | systems with ≥10 all-correct in top-20 for every model | KinCoRe label match | p9 |
  | Benchmark size | 2,225 unique chains; 1,420 unique systems; 236 apo chains / 43 apo gene targets; 1,989 holo chains / 1,377 unique protein–ligand pairs | chains, systems | — | p3, p5 |
  | Curation attrition | 7,763 PDB entries → 7,638 chains → 6,703 high-quality → 4,564 WT noncovalent → 2,900 unphosphorylated → 2,225 unique | chains | curation pipeline, Figure 1a | p3–5, p5 |
  | Dataset composition | 1 ligand 1,781; no ligand 236; 2+ ligands 208; Active 1,020; Inactive 1,205 | chains | Figure 1b bar labels | p5 |
  | Valid-label check | all predictions from all models fall in the 12 PDB-observed label combinations (of 36 theoretical); zero "forbidden" geometries | — | Supplementary Table S2, **not held** | p6 |

- **n_predictions**: record the three levels separately.
  - **Samples per target:** 20. p13: "we generate N = 20 cofolding samples per target for each
    inference run." Fixed for all targets and all models; no per-target adaptation.
  - **Targets per model:** 1,420. p13: "Inferences are performed on NVIDIA A100 GPUs across the
    1,420 unique configuration pairs (43 apo + 1,377 holo) defined during curation."
  - **Models:** 3 (Boltz-2, Chai-1, Protenix).
  - **Total:** **NOT REPORTED by the paper.** 20 × 1,420 × 3 = **85,200** predicted structures
    by arithmetic from the numbers on p13; this product is derived here, not a figure the
    authors print.
  - **Analysed rather than generated:** 950 systems × 20 × 3 = 57,000 structures reach the
    Figure 2 analysis (derived); 509 systems × ≥10 correct × 3 reach Figure 4; 234 holo/apo
    pairs × 20 × 3 reach Figure 5.
  - **Discarded, count NOT REPORTED:** p13, "targets that failed annotation because of
    malformed outputs or missing motifs are excluded."
- **comparable_to_ours**: *(left empty by the extractor, per schema v3)*
- **si_in_scope**: **SI NOT HELD.** The held PDF is main text only (18 pages, ending at the
  reference list). The paper cites Supplementary Information for: the KinCoRe label format
  (p4), acronym definitions (p5 caption), the continuous distance/dihedral descriptor
  definitions (p9), and the KinCoRe pipeline details (p13). It cites **Supplementary Figures
  S1–S4** — S1 ligand and KinCoRe label frequencies (p5), S2 geometric distributions of
  successful predictions per model (p6), S3 how the 509 diversity targets distribute across the
  Top-K benchmark (p9), S4 that all models capture correct *average* distances and angles (p9)
  — and **Supplementary Tables S1–S4** — S1 the 36-theoretical/12-observed label combinations
  and Type-I ligand prevalence (p5, p6), S2 the label-validity check (p6), **S3 the exact Top-K
  success numbers (p7)**, **S4 the 110 joint-failure kinases (p8)**. The most-cited comparator
  numbers in this note (exact Top-1 and Top-20 accuracies) live in Table S3 and are therefore
  approximate here, read off Figure 2b. Code and data are stated to be public:
  https://github.com/THGLab/KinConfBench (p13).

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 5 | Curation workflow from 437 catalytically active human kinase domains down to the 2,225-chain benchmark, with the excluded branches (mutant, covalent) drawn off to the side | schematic | `SCHEMATIC \| curation flowchart: node = dataset state with chain count, edge = filtering operation; two side branches marked (Excluded) \| no data` | 1 panel, 8 nodes, 5 sequential filter edges plus 2 exclusion branches | | CC-BY 4.0 International, **no ND clause** — redrawing and modification both permitted. Stated in the banner on every page, including p5. |
| 1B-D | 5 | Composition of the benchmark: ligand count per chain, active/inactive balance, Manning-group taxonomy, and the top-10 genes | bar | `PLOT \| facet: composition view (4: ligand count, activity, Manning group, top-10 gene) \| vary: category within panel (3, 2, 8 and 10 levels respectively) \| series: none (1) \| measure: number of structures (chain count) \| mark: bar \| n: 2,225 chains partitioned within each panel; the count is printed on every bar` | 4 sub-panels (b splits into two adjacent bar charts; c and d are horizontal bars). Panels vary by partitioning variable, not by condition or system. One row rather than four because `mark` (bar) and `measure` (chain count) are identical throughout — see `unresolved` on the split rule | | as above |
| 2A | 7 | The three geometric quality metrics, split by whether the prediction's 8 KinCoRe labels match the reference — the paper's "geometry does not predict state" result | box | `PLOT \| facet: cofolding model (3) × geometric metric (3: ligand RMSD, lDDT-Cα, lDDT-PLI) \| vary: KinCoRe 8-label correctness (2: correct, incorrect) \| series: cofolding model (3, colour redundant with facet) \| measure: metric value (Å for ligand RMSD; unitless lDDT) \| mark: box \| n: NOT REPORTED per box; the pool is 950 systems × 20 samples × 3 models` | 3×3 grid; rows are metrics, columns are models. Panels vary by model and by metric | **Every axis is pinned at the geometric filter threshold** (ligand RMSD top at 2.0 Å, lDDT-Cα bottom at 0.7, lDDT-PLI bottom at 0.8), which is the same cut that selected the data, so the plotted distribution is the censored one and the outlier mass piles into an unresolvable solid band against the 2.0 Å boundary in all nine RMSD panels. **n is not shown on any box.** No indication of how many of the 950 systems contribute to "correct" vs "incorrect". The overlap the text describes ("the overlap with incorrect functional assignment remains large") is asserted rather than quantified — no effect size, AUC or separation statistic | as above |
| 2B | 7 | Success rate against K for top-K-by-pLDDT selection — the sampling-count effect | line | `PLOT \| facet: none (1) \| vary: K (top-K predictions), 1–20 (continuous integer range) \| series: cofolding model (3: Boltz-2, Chai-1, Protenix) \| measure: system success rate (%) \| mark: line \| n: 950 systems behind every point` | 1 panel, 3 lines | **y-axis truncated**, starting near 63% rather than 0, which visually magnifies the 11–13 pp Top-1→Top-20 gain the text reports. No error bars or confidence bands on any curve; n = 950 appears only in the Figure 2c caption text, not on this panel | as above |
| 2C | 7 | How many of each system's 20 ranked samples match all 8 labels — the mode-collapse result | bar (histogram) | `PLOT \| facet: cofolding model (3) \| vary: number of correct predictions out of top-20, 0–20 (21 bins) \| series: none (1) \| measure: number of systems \| mark: bar \| n: 950 systems per panel, summed across bins` | 3 panels, one per model, sharing a common vertical scale (stated in the caption) | | as above |
| 3 | 8 | MAP4K1/HPK1 with a Type-I diaminopyrimidine carboxamide (PDB 7M0M): experimental structure superposed with one prediction from each model, showing correct ligand pose but wrong DFG and activation-loop geometry | structure render | `RENDER \| facet: none (1) — a single system, MAP4K1 / 7M0M \| views: 3 (whole-complex superposition at left; DFG-motif close-up top right; activation-loop close-up bottom right) \| overlay: 3 predictions (one per model; which of that model's 20 samples was chosen is NOT REPORTED) on 1 experimental reference \| axis: none` | 3 views of one system; views vary by structural feature, not by condition | **A claimed failure mode with no quantitative panel.** The joint-failure claim covers 110 systems (Supplementary Table S4, not held) but only one is shown, chosen as "a representative hard case" after the failures were known. The selection rule for the single "representative" prediction out of 20 per model is not stated, so this could be the top-1-by-pLDDT structure or a hand-picked one. No RMSD, no label listing for the three predictions — the caption asserts they are "conformationally mislabeled relative to 7M0M" without saying which of the 8 labels differ | as above |
| 4 | 9 | Within-ensemble standard deviation of 4 distance and 8 dihedral descriptors across all-label-correct predictions — the low-diversity result | box | `PLOT \| facet: geometric descriptor (12: Lys–Glu, salt bridge, spine and DFG–HRD distances; Asp φ/ψ/χ1/χ2; Phe φ/ψ/χ1/χ2) \| vary: cofolding model (3) \| series: cofolding model (3, colour redundant with vary) \| measure: within-ensemble standard deviation (Å in the 4 distance panels, ° in the 8 dihedral panels) \| mark: box \| n: 509 systems per box; each system contributes ≥10 all-correct structures out of its top-20` | 12 panels in a 3×4 grid; rows are descriptor class (distance, Asp dihedral, Phe dihedral), columns are the individual descriptor. Panels vary by descriptor; the three models are the within-panel comparison | **Every panel carries its own free y-axis range** (0.04–0.16 Å, 0–0.3 Å, 0–18°, 0–4.5° and so on), so panels showing ∼0.1 Å dispersion look as tall as panels showing 18°, and the reader cannot see across panels that the values are uniformly tiny — which is the figure's whole claim. **No reference band is drawn** for the ∼1–2 Å RMSF / 5–30° thermal-fluctuation scale the text on p10 uses to interpret these numbers, so the "little structural diversity" conclusion is invisible in the figure and stated only in prose. n is not shown on any of the 36 boxes | as above |
| 5 | 11 | Four-way holo/apo outcome distribution per model, training split vs post-cutoff test split — the apo-drift result | bar (stacked) | `PLOT \| facet: data split (2: training set, test set) \| vary: cofolding model (3) \| series: holo/apo outcome category (4: Holo State, Dual Match, Apo Drift, None) \| measure: percentage of systems (%) \| mark: bar (stacked to 100%) \| n: per bar — train 212 / 182 / 194 and test 22 / 52 / 40 for Boltz-2 / Chai-1 / Protenix` | 2 panels × 3 bars; panels vary by split, bars by model, stack segments by outcome | **Percentages plotted over very unequal and, in the test panel, very small n** — Boltz-2's test bar rests on 22 systems, so a single system moves a segment by ~4.5 pp, and that is the model on which the text calls the shift "most clearly" visible. The n values appear only in the caption, never on the axis or the bars. **No error bars, confidence intervals or statistical test** accompany the train-vs-test comparison the whole section rests on. Stacking to 100% also means the four segments are not independently readable — only the bottom (Holo State) and top (None) segments have a common baseline | as above |

**Panel-group rows: 8** (1A, 1B-D, 2A, 2B, 2C, 3, 4, 5), covering all 5 numbered main-text
figures. Supplementary Figures S1–S4 are cited but not held and are not catalogued.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), single-paper extraction session
- **schema_version**: v3
- **confidence**: **high** on protocol, dataset construction, oracle routes, control arms and
  figure structure — the Methods and the curation section are unusually explicit, and the
  cutoff dates and split sizes are printed in the text and the Figure 5 caption. **Medium** on
  the headline accuracy numbers: the abstract gives only a "∼65-75%" range, the text gives only
  the Top-1→Top-20 *deltas*, and the exact per-model Top-1 and Top-20 values live in
  Supplementary Table S3, which is not in the held PDF, so the absolute rates in
  `metrics_reported` are read off Figure 2b and flagged as approximate. What was hard: (i) four
  figure pages had to be rendered because the captions do not carry panel structure — Figure 1
  (b/c/d described in one clause each), Figure 2 (panel a's 3×3 grid and mark type unstated),
  Figure 4 (12 panels, no panel letters, descriptors named nowhere in the caption) and Figure 5
  (the text refers to "Figure 5a" and "Figure 5b" but neither the caption nor the figure prints
  panel letters); (ii) the text-layer renders Greek letters correctly but glues some reference
  numerals to the preceding word.
- **unresolved**:
  1. **Published version.** The task brief states this preprint has since appeared in
     *npj Drug Discovery*, `10.1038/s44386-026-00068-z`. Nothing in the held PDF says so, the
     published version was not read, and no field in this note reflects it. Section A records
     the bioRxiv preprint as what was actually read, and the note is tagged `preprint` on that
     basis. **If the corpus is to cite the journal version, the note needs a re-pass against
     it** — venue, year, page numbers for every quote, the figure page numbers, and possibly
     the numbers themselves may all differ, and any SI table that is open-access there would
     close the `si_in_scope` gap.
  2. **Supplementary Information is not held.** Tables S1–S4 and Figures S1–S4 carry the exact
     Top-K accuracies (S3), the 110-system joint-failure list (S4), the label-validity check
     (S2) and the per-model geometric distributions (S2 figure). Retrieving the SI, or the
     GitHub repository (https://github.com/THGLab/KinConfBench, p13), would materially improve
     `metrics_reported`.
  3. **Template setting never stated.** The protocol is "official inference pipelines" with
     "default databases and pairing strategies" (p12–13), but whether Boltz-2, Chai-1 and
     Protenix ran with their structural template channels enabled is not said. This leaves
     `oracle_leakage` route 1 not fully closable and blocks any protocol tag
     (`templates-on` / `no-template-no-msa` are both unsupportable from this PDF).
  4. **Exact Top-1 accuracies.** Only the three deltas (+11.4 / +12.6 / +12.1) are printed
     (p7); the abstract's "∼65-75%" range is the only absolute figure in the main text. The
     Top-1 values in `metrics_reported` are derived by subtraction from Figure 2b endpoints
     and are explicitly labelled as such.
  5. **The 43 apo targets.** Inference is run on them (p13, "1,420 unique configuration pairs
     (43 apo + 1,377 holo)") but no main-text result is reported for apo-input predictions.
     Whether they feed Figure 2 at all, or exist only to supply the apo references for the
     Figure 5 pairing, is not stated. Note that this means the apo-drift argument has no
     apo-input control arm: the "default apo landscape" the models are said to revert to is
     never measured directly.
  6. **Figure 3's "representative" prediction.** Which of each model's 20 samples is rendered,
     and by what rule, is not stated (p8).
  7. **DOI prefix.** The banner reads `10.64898/2026.04.07.716788` rather than bioRxiv's
     customary `10.1101/...`. Recorded as printed and matching `refs.bib`; not verified.
  8. **Dropped-target count.** p13 excludes "targets that failed annotation because of
     malformed outputs or missing motifs" without giving n, so the denominator behind the 1,420
     → 950 attrition is partly unaccounted.
  9. **`UNPOWERED` judgement call in `anti_memorization_control`.** The v3 rule fires on
     "n < ~10 **or** the held-out set overlaps training". The test n values (22 / 52 / 40) all
     clear the n clause, but the apo reference of every test pair is in training by the
     authors' own statement (p10), which triggers the overlap clause literally. `UNPOWERED` is
     applied on that literal reading and the `unpowered` tag set; a reader who thinks the
     overlap clause was meant for accidental contamination rather than a deliberate one-sided
     design should downgrade it. Flagging rather than deciding silently.
  10. **Tags I needed and could not use** (not invented, per the rules):
      - A **result** tag for mode collapse / apo-drift / detected memorization, analogous to
        `allosteric-failure`. This is the paper's headline finding and `negative-result` is too
        generic to retrieve it. Suggest `mode-collapse` and/or `memorization-detected`.
      - A tag distinguishing **evaluation-side oracle** (a benchmark scoring against deposited
        references — unavoidable and not a defect) from **input-side oracle leakage**.
        `oracle-leak` is applied here, but it will retrieve this paper alongside papers that
        fed a state-annotated template into the model, which is a different thing entirely.
        Suggest `evaluation-oracle` or a qualifier on `oracle-leak`.
      - A protocol tag for **state classifier used as the metric** (Kincore/KLIFS/GPCRdb run on
        the outputs). `state-annotated-input` is the opposite of what happens here and would be
        wrong.
      - A tag for **success-conditioned analysis set** (the 950-of-1,420 and 509-system
        subsets, both selected on model performance). This is a recurring benchmark pattern
        with no vocabulary.
  11. **v3 ambiguities encountered** (blunt, since the schema is still being tuned):
      - **The panel-splitting rule does not cover a differing `vary`.** The rule is "split when
        `mark` or `measure` differs; do not split when only `facet` differs." Figure 1b/c/d all
        have `mark: bar` and `measure: number of structures` but four *different independent
        variables* (ligand count, activity, Manning group, gene). The literal rule forces one
        row, whose `vary` slot then has to hold a four-way compound — the exact unjoinable
        compound string the split rule exists to prevent. One row (`1B-D`) was written, per the
        rule, but the rule should probably read "split when `mark`, `measure` **or `vary`**
        differs", or `facet` should be defined to absorb this case.
      - **`vary` and `series` collide when the same variable does both jobs.** In Figures 2a
        and 4 the cofolding model is simultaneously the categorical position on the independent
        axis *and* the colour. Writing it in both slots (as done here, with a "colour redundant"
        annotation) is honest but will double-count on a join; leaving `series: none` would
        discard a real legend dimension. The grammar needs a rule for redundant encoding.
      - **`metric_saturation` vs `hides` for a *filter-induced* censor.** The v3 fix says
        numeric saturation goes in `metric_saturation` and axis truncation in `hides`. Figure
        2a is one phenomenon expressed both ways: the geometric pre-filter censors the data
        numerically *and* the axes are pinned at exactly those cut values. It is recorded in
        both fields with an explicit cross-reference, which is what v3 asks for, but this is
        the case where the "record it once" intent is hardest to honour.
      - **`states_generated` for a benchmark-only paper.** The paper generates nothing of its
        own design; it runs three other people's models. `ensemble + single-state` is recorded
        because the authors ran the inferences and the collapse is their result, but the field
        wording ("What did they actually produce") assumes the authors own the generator.
      - **`anti_memorization_design` assumes one cutoff.** Here there are three, one per
        backbone, with three different n. The field took it, but any index that stores a single
        cutoff date or a single n will be wrong for this paper.
- **why_it_matters**: *(left empty by the extractor — the user's call)*

## Tags

`kinase` `cofolding` `benchmark-only` `multi-backbone` `ensemble` `single-state`
`binary-predicate` `continuous-metric` `saturating-metric` `oracle-leak` `design-level-oracle`
`anti-memorization` `unpowered` `confidence-as-discriminator` `ligand-driven` `seed-only`
`apo-sampling` `orthosteric` `preprint` `precedent` `background` `negative-result`
`comparator-numbers`

Tag notes, so the reverse lookups are not misread:

- `ensemble` + `single-state` is the deliberate v3 pair: N = 20 samples per target (p13) that
  collapse bimodally onto one basin (p7, p9).
- `oracle-leak` is applied for routes 3, 4 (partly), 5 and 6, **all of which fire on the
  evaluation and selection side**. The models' inputs are clean. See item 10 in `unresolved` —
  this tag will co-retrieve this paper with input-side leakers, which is a vocabulary defect,
  not a property of the paper.
- `design-level-oracle` is route 7: the apo-drift systems were chosen because both the correct
  holo answer and the wrong apo answer are already deposited and already labelled (p10).
- `anti-memorization` **and** `unpowered` are both correct here: the post-cutoff control arm was
  genuinely run and analysed (Figure 5), and it trips the overlap clause because all apo
  references are in training (p10). Not `no-anti-memorization`.
- `ligand-driven` and `seed-only` describe the *absence* of any directional handle: the ligand
  SMILES is the only conditioning input and repeated sampling the only ensemble mechanism.
- `apo-sampling`: inference is run on 43 apo targets as well as 1,377 holo (p13), and apo
  reversion is the central failure mode.
- **Not tagged**, deliberately: `prospective` (fully retrospective); `no-anti-memorization`
  (a control was run); `rmsd-only` (RMSD is a pre-filter, the state call is categorical);
  `visual-metric` (Figure 3 illustrates a predicate-called failure, it does not call it);
  `templates-on` / `no-template-no-msa` / `state-annotated-input` (template setting is
  NOT REPORTED and MSAs are full, so no protocol tag is supportable); `allosteric-site` and
  `allosteric-failure` (Type-II/allosteric binding is discussed as motivation on p5–6 and the
  allosteric failure is cited to Nittinger et al. [22] on p2, but no allosteric arm is run
  here); `peer-reviewed` (the held PDF is the preprint — see `unresolved` item 1);
  `figure-exemplar` (that tag mandates exclusion from gap analysis, and this paper is squarely
  inside the gap analysis); `md` / `md-emulator` / `enhanced-sampling` / `msa-subsample` /
  `msa-state-filter` / `template-state-bias` / `latent-steering` / `af-cluster` / `experimental`
  / `experimental-validation` (none performed).
