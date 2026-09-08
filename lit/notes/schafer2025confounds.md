# schafer2025confounds

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–6).** The document is a
6-page bioRxiv preprint with no journal pagination: p1 abstract, p2–5 Introduction / Results /
Discussion / Methods / Data, p6 references. Figure 1 sits on p3, Figure 2 on p4.

**Text-layer caveat:** the PDF text layer renders Greek letters as Latin, so α appears as "a"
and β as "b" (e.g. "a-helical", "b-sheet"), and superscript reference numerals are glued to the
preceding word (e.g. "the two9", "AF25"). Verbatim quotes below reproduce the text layer as
extracted. The rendered page confirms these are α/β and superscript citations.

**Version caveat, recorded up front because it affects `A. Identity`:** the held PDF is the
bioRxiv preprint posted 6 January 2024. `refs.bib` records a 2025 *Nature* version with a
longer author list. See `unresolved`.

---

## A. Identity

- **citekey**: `schafer2025confounds`
- **doi**: **10.1101/2024.01.05.574434** (bioRxiv) — p1: "bioRxiv preprint doi:
  https://doi.org/10.1101/2024.01.05.574434; this version posted January 6, 2024".
  `refs.bib` instead records `10.1038/s41586-024-08267-2` (Nature). The PDF held by the corpus
  is the preprint, not that Nature version — see `unresolved`.
- **year**: **2024** as posted (p1). The citekey says 2025 and `refs.bib` says 2025; neither is
  supported by anything inside this PDF.
- **venue**: **bioRxiv preprint, not peer reviewed.** p1: "The copyright holder for this preprint
  (which was not certified by peer review) is the author/funder." Tagged `preprint` on the
  evidence of this PDF. (`refs.bib` claims *Nature*; not checkable here.)
- **title**: Sequence clustering confounds AlphaFold2 — p1
- **authors**: Joseph W. Schafer, Devlina Chakravarty, Ethan A. Chen, and Lauren L. Porter
  (corresponding, porterll@nih.gov) — p1. NCBI/NLM/NIH and NHLBI Biochemistry and Biophysics
  Center, Bethesda MD. **Four authors in this PDF**; `refs.bib` lists six (adds Lee and Thole).

## B. Scope

- **system**: **general protein — fold-switching / metamorphic soluble proteins.** No membrane
  proteins, GPCRs, kinases or transporters. p1: "some globular proteins remodel their secondary
  and/or tertiary structures in response to cellular stimuli."
- **n_targets**: **three protein families** (p2: "three naturally evolved fold-switching protein
  families characterized previously8"): KaiB, Mad2, RfaH. Resolved to individual proteins the
  count is larger and arm-dependent:
  - Figure 1b: **8 proteins** — six KaiB (R. sphaeroides, R. sphaeroides-3M, S. elongatus,
    T. elongatus, L. pneumophilia, T. elongatus vestitus TV4), plus H. sapiens Mad2 and
    E. coli RfaH (p3).
  - Figure 1c: **2 single-folding negative controls** — KaiB-TV4 and KaiB-TE 5M (p3–p4).
  - Ensemble/performance comparison (Figure 2b): **3** — KaiB, Mad2, RfaH (p4).
  - Deep RfaH re-analysis arm: 1 protein, 250 + 250 + 21 models (p2).
  - Out-of-training-set arm borrowed from ref. 4: "sequence-diverse RfaH homologs and two
    fold-switching proteins outside of AF2's training set" (p5), n for the RfaH homologs
    NOT REPORTED.
  - **Generality flag:** the recommendation in the abstract ("we suggest using ColabFold6-based
    random sequence sampling7 ... as a more accurate and less computationally intense
    alternative to AF-cluster", p1) is general, but rests on three families, all of them the
    families already chosen by the paper being rebutted.
- **method_class**: **dual — MSA-subsampling + benchmark-only.** The paper is primarily a
  re-analysis/rebuttal of a published method (AF-cluster) using the original authors' own
  deposited outputs, and secondarily proposes a comparator (CF-random) that is random shallow
  MSA subsampling. p3: "we ran ColabFold6–an efficient-yet-accurate implementation of AF2–with
  randomly sampled shallow input MSAs". p2: "Further inspection of results from the Repo
  revealed that AF2 predictions of RfaH from uniformly sampled MSAs predicted accurate,
  high-confidence structures more successfully than sequence clusters".
- **backbones**: **AF2 only.** Run two ways: ColabFold 1.5.3 as the CF-random implementation
  (p5, Methods) and AF2 directly, including "the version of AF2 reported in the Repo" (p3).
  ColabFold is an implementation of AF2, not a distinct backbone — p3 calls it "an
  efficient-yet-accurate implementation of AF2". **Do not tag `multi-backbone`.** No AF3, Boltz,
  Chai, OF3 or Protenix anywhere. MSA Transformer appears once but only for contact/coupling
  analysis, not structure prediction (p2, Supplementary Figure 1b).
- **templates**: **NOT REPORTED.** The word "template" does not appear in the paper. Methods
  (p5) state only: "CF-random was run with ColabFold1.5.3 with depths max-seq = 1, 8, 64 for
  KaiB, Mad2, and RfaH, respectively, and max-extra-seq = 2*max-seq in all 3 cases. All other
  parameters were kept constant." Whether ColabFold's default template setting applied is never
  stated. Do not infer.
- **msa_handling**: **subsampled + full**, with a **clustered** arm re-analysed rather than run.
  - *Subsampled* is CF-random's method: random shallow MSAs at max-seq = 1 (KaiB), 8 (Mad2),
    64 (RfaH), max-extra-seq = 2×max-seq (p5).
  - *Full* MSA is their control arm: "we generated 250 models by running AF2 on the full RfaH
    MSA from Wayment-Steele et al.'s GitHub repository (the Repo)" (p2).
  - *Clustered* is AF-cluster's handling, examined via the Repo's deposited outputs, not
    re-clustered by these authors.
  - **No state-filtered MSA anywhere.** Nothing substitutes a state-specific alignment;
    `msa-state-filter` does not apply. Subsampling here reduces depth only.

## C. Conformational core

- **states_generated**: **ensemble + two.** CF-random emits an ensemble per target — 330
  predictions for KaiB (Figure 2 caption, p4) — and what is scored and claimed is capture of the
  two experimentally determined conformations of each family. Figure 2a plots the ensemble as a
  cloud in a two-reference RMSD plane, with the two states as dashed boxes: "Both CF-random and
  AF-cluster predict both the fold-switched (lower right dashed boxes) and ground state (upper
  left dashed boxes) conformations of KaiB" (p4). The interesting half of the duality is that
  the ensemble is what carries the false positives: "AF-cluster predicts high-confidence false
  positives (dots outside of dashed boxes with confidences ≥70). CF-random does not." (p4)

- **structural_priors_used**: **Substantial, at design time, and not a defect.**
  1. **Both experimentally determined conformations of all three families are held and used as
     RMSD references.** p2: "we calculated the RMSDs of their fold-switching CTDs referenced
     against both experimentally determined conformations (Figure 1a): a-helical hairpin
     (autoinhibited) and b-sheet (active)." Figure 1a displays six of them: KaiB ground, KaiB
     fold-switched, Mad2 closed, Mad2 open, RfaH autoinhibited, RfaH active (p3).
  2. **Target set inherited from the rebutted paper**, which selected systems with both states
     solved. p2: "The Paper reported successful predictions from three naturally evolved
     fold-switching protein families characterized previously8".
  3. **Prior NMR characterisation defines ground truth for the two negative controls.** p4:
     "nuclear magnetic resonance (NMR) experiments from the Paper provide no evidence for it.
     Instead, these experiments indicate that KaiB-TV4 assumes the fold-switched conformation
     and a minor unfolded state5." and "NMR experiments indicate that the variant assumes the
     fold-switched state only12."
  4. **Prior sequence-identity knowledge to experimentally characterised homologs** is used to
     grade difficulty (p5, quoted under `stated_limits`).
  - **PDB accession codes: NOT REPORTED.** No accession is given anywhere in the PDF for any
    reference structure.

- **oracle_leakage**: **PRESENT. Routes 4, 5 and 6 are pipeline leakage; route 7 is
  design-level.** All seven routes enumerated separately below.

  **Route 1 — structures used as input or template: NONE FOUND.**
  The only stated inputs are MSAs. Protocol page for checkability is p5 (Methods), quoted in
  full: "CF-random was run with ColabFold1.5.3 with depths max-seq = 1, 8, 64 for KaiB, Mad2,
  and RfaH, respectively, and max-extra-seq = 2*max-seq in all 3 cases. All other parameters
  were kept constant." No structure is fed to the predictor at any point; the deposited
  structures appear only downstream as RMSD references (route 5). Caveat: templates are
  never mentioned, so a silent ColabFold default cannot be excluded from this PDF — recorded
  as a gap in `templates`, not as leakage.

  **Route 2 — state annotations from a curated database driving templates or alignments:
  NONE FOUND.**
  No GPCRdb / KLIFS / Kincore analogue is used, and no state-annotated alignment is built. MSAs
  are taken unmodified from the rebutted paper's repository: "the full RfaH MSA from
  Wayment-Steele et al.'s GitHub repository (the Repo)" (p2). Protocol pages: p2 and p5.

  **Route 3 — cluster labels derived from known states: NONE FOUND in their own method.**
  CF-random performs no clustering at all — it samples uniformly at random. p3: "we ran
  ColabFold6 ... with randomly sampled shallow input MSAs". The clustering under discussion is
  AF-cluster's, which these authors re-analyse rather than re-run, and their entire argument is
  that clustering carries no state information beyond what random sampling gives: "randomly
  sampling diverse MSAs–a method proposed previously7–enables more accurate, higher-confidence
  predictions than clustering by sequence similarity." (p3)

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
  states: PRESENT, and this is the paper's own sharpest rigour defect.**
  The MSA depth is set **per target**, to three different values, on the three evaluation
  systems whose both states they hold:
  *"CF-random was run with ColabFold1.5.3 with depths max-seq = 1, 8, 64 for KaiB, Mad2, and
  RfaH, respectively, and max-extra-seq = 2*max-seq in all 3 cases."* (p5)
  No a priori selection rule for 1, 8 and 64 is given anywhere in the PDF; the justification, if
  any, is in Supplementary Methods, which the corpus does not hold ("More details about
  predictions and other calculations can be found in Supplementary Methods.", p5).
  The **range** was itself chosen by looking at accuracy against the known references. The
  sentence that motivates leaving the rebutted paper's depths reads:
  *"Nevertheless, these results suggested that better predictions may be achieved by randomly
  sampling MSAs with depths other than 10 or 100, the only two depths randomly sampled in the
  Paper."* (p2–p3, sentence spans the page break)
  The "these results" being referred to are RMSD-to-reference success rates computed two
  sentences earlier (route 5). Per the v3 rule, tuning a sweep range on the evaluation set is
  leakage even where no single per-target value is picked — and here per-target values *are*
  picked as well. Seeds and recycles: **NOT REPORTED.**

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had: PRESENT, and it
  is the primary success criterion.**
  *"To assess their accuracies, we calculated the RMSDs of their fold-switching CTDs referenced
  against both experimentally determined conformations (Figure 1a): a-helical hairpin
  (autoinhibited) and b-sheet (active). Out of the 250 predictions, the CTDs of 10 were
  predicted accurately (defined as being within 3Å of either experimentally determined
  conformation and with an average confidence ≥ 55), a 4% success rate."* (p2)
  Same route elsewhere, with **three mutually inconsistent thresholds and no justification for
  any of them**:
  - 3 Å and plDDT ≥ 55 in the RfaH text (p2, above);
  - 5 Å and plDDT < 70 for figure colouring: "Red labels indicate RMSD > 5Å relative to
    experiment and/or plDDT scores <70." (Figure 1 caption, p3);
  - plDDT ≥ 70 for false-positive calling: "AF-cluster predicts high-confidence false positives
    (dots outside of dashed boxes with confidences ≥70)." (Figure 2 caption, p4).
  Figure 2a's entire coordinate system is RMSD to both held references (p4). The %Success and
  Matthews Correlation Coefficient bars in Figure 2b (p4) are computed against these
  reference-defined labels.

  **Route 6 — best/worst model labels assigned against a held reference: PRESENT.**
  *"After identifying AF-cluster predictions from the Repo with helical bundle folds like the
  autoinhibited structure, we calculated an average plDDT of 63.8 (Supplementary Figure 1a)."*
  (p2) — the subset averaged is selected by resemblance to the known autoinhibited structure,
  and the resemblance call is made by fold appearance.
  Figure 1b/1c likewise display **one selected model per protein**, labelled by its
  reference-derived status: "bold labels indicate dominant fold prediction; others are
  alternative. Red labels indicate RMSD > 5Å relative to experiment and/or plDDT scores <70."
  (p3). How that one model was selected out of the several hundred in each ensemble is
  **NOT REPORTED** — see the `hides` entry on Figure 1B-C.

  **Route 7 — design-level oracle use (input conditions or systems chosen because the expected
  answer is already known): PRESENT. Label design-level; weaker than the pipeline leakage
  above, and do not conflate.**
  The two negative controls are chosen precisely because the answer was settled by NMR before
  any prediction was read:
  *"It does the same for two experimentally confirmed single-folding KaiBs (Figure 1c)."* (p3–p4)
  *"Only five mutations distinguish this variant from its experimentally characterized
  ground-state homolog, but NMR experiments indicate that the variant assumes the fold-switched
  state only12."* (p4)
  The three evaluation families are inherited wholesale from the rebutted paper, which had
  chosen them for having both states solved (p2). This is legitimate and unavoidable for a
  rebuttal — a controls paper must test on systems with known answers — but it is design-level
  oracle use and must be labelled as such.

  **Summary verdict:** the predictor is fed nothing leaky (routes 1–3 clean), but the depth
  hyperparameter was set per target on the evaluation systems (route 4), success is defined by
  RMSD to held references with three unjustified and mutually inconsistent thresholds
  (route 5), displayed and averaged model subsets are selected against those references
  (route 6), and the target set is design-level oracle (route 7).

- **prospective**: **no.** Every arm is retrospective by construction. The predictions are
  scored against structures already in hand (route 5), the depth hyperparameter was chosen after
  seeing reference-scored results (route 4), and a large fraction of the analysis re-scores
  models the rebutted authors had already deposited: "Further inspection of results from the
  Repo revealed that AF2 predictions of RfaH from uniformly sampled MSAs predicted accurate,
  high-confidence structures more successfully than sequence clusters" (p2). No new prediction
  is made and then tested. Note this is not a criticism of the paper's genre — a controls
  rebuttal has no prospective mode available — but the field records what happened.

- **state_metric**: **RMSD-to-reference + binary predicate**, with a **third, visual** component
  that the dual form cannot hold and that is recorded here rather than dropped.
  - *RMSD-to-reference, continuous:* all-atom RMSD to both experimental conformations, plotted
    as the two axes of Figure 2a and printed per protein in Figure 1b as "All atom root-mean-
    square deviations (RMSDs) and AF2 prediction confidences (plDDTs) reported below the source
    organisms of each protein" (p3).
  - *Binary predicate:* "defined as being within 3Å of either experimentally determined
    conformation and with an average confidence ≥ 55" (p2). **Threshold justification:
    NOT REPORTED** — neither 3 Å nor 55 is defended. The competing 5 Å / plDDT 70 (p3) and
    plDDT ≥ 70 (p4) cuts are likewise unjustified, and the paper never reconciles them.
  - *Visual:* fold identity is called by eye in at least one load-bearing step — "identifying
    AF-cluster predictions from the Repo with helical bundle folds like the autoinhibited
    structure" (p2) — with no operationalised predicate. Tagged `visual-metric`.

- **metric_saturation**: **YES, numerically, in one arm.** The Matthews Correlation Coefficient
  ceilings: CF-random on KaiB is plotted and labelled at **1** (Figure 2b, p4), the maximum
  attainable MCC. No headroom remains in that cell, so the KaiB comparison cannot distinguish
  CF-random from a hypothetical better method. %Success does not saturate (max plotted 68 of a
  possible 100). Cross-reference the figure row `2B` rather than duplicating; the plDDT colour
  scale clipping in Figure 2a is a *figure* defect and is recorded in `hides` on row `2A`, not
  here.

- **directional_control**: **NONE. The method only samples.** CF-random has no handle that
  instructs which conformation to produce — no partner, ligand, nanobody, peptide,
  state-annotated template or state-filtered MSA is used anywhere. The single available knob is
  **MSA subsample depth** (max-seq 1 / 8 / 64, p5), and that is a sampling-breadth parameter, not
  a state selector: both states emerge from the same run and are separated only afterwards, by
  RMSD to the two references (Figure 2a, p4). Seeds are not used as a handle and are
  NOT REPORTED. The whole argument of the paper is that the competing method's apparent handle
  (sequence clustering) is not one either: "the Paper's claim that 'clustering resulted in
  deconvolving conflicting sets of couplings' is called into question." (p2)

- **anti_memorization_design**: **Present but borrowed and thin.** There is no held-out or
  post-cutoff set constructed by these authors. They import one from ref. 4: "a recent
  benchmarking study showed that both AF2 and AF-cluster failed to predict the correct
  conformations of sequence-diverse RfaH homologs and two fold-switching proteins outside of
  AF2's training set4." (p5). **n = 2 named proteins outside the training set, plus an
  unspecified number of sequence-diverse RfaH homologs (n NOT REPORTED).** **How the cutoff was
  defined: NOT REPORTED** — no date, no PDB release criterion, no training-set list. A separate
  sequence-distance criterion is stated and is the closest thing to a memorization design in the
  paper: "These RfaH homologs were a more difficult test: all fold-switching sequences were <35%
  identical to their closest experimentally characterized homolog. For comparison, the sequences
  of all KaiB variants in the Paper were ≥ 47% identical to their experimentally characterized
  homologs." (p5)

- **anti_memorization_control**: **RUN, but UNPOWERED and unreported.** The arm exists — CF-random
  was evaluated on that out-of-training-set set — but the entire result is delivered in three
  words: *"So does CF-random."* (p5, following the sentence quoted above). No n, no RMSDs, no
  confidences, no per-target breakdown, no figure or supplementary pointer for this arm.
  **Mark UNPOWERED**: n = 2 named proteins plus an unspecified homolog count, well under ~10, and
  the result is a bare assertion. This is the paper's own most consequential negative finding
  about its own proposed method and it carries less quantitative support than any other claim in
  the paper.

- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Full-MSA AF2 baseline for RfaH, 250 models generated by these authors | Rules out that AF-cluster's reported plDDT advantage over full-MSA prediction is real; full-MSA average (74.7) exceeds the reported AF-cluster value (73.9) | p2 |
| Software-matched control (AF2 vs ColabFold), raised as a defect in the rebutted work and then corrected by re-running with "the version of AF2 reported in the Repo" | Rules out that CF-random's advantage is a ColabFold-vs-AF2 implementation artifact; also rules out the rebutted paper's cross-software comparison | p2, p3 (result in Supplementary Table 1, not held) |
| Random/uniformly sampled MSA arm from the Repo, 21 models, scored against AF-cluster's 250 | Rules out that sequence clustering beats depth-matched random sampling: 24% vs 4% success | p2 |
| Matched ensemble sizes, CF-random 330 vs AF-cluster 329 for KaiB | Rules out that the false-positive difference is an artifact of unequal numbers of predictions | p4 (Figure 2 caption) |
| Two experimentally confirmed single-folding proteins run as negative controls: KaiB-TV4 and KaiB-TE 5M | Rules out that a high-confidence alternative-state prediction implies real fold switching; establishes a false-positive rate for AF-cluster, and catches CF-random failing the same way on KaiB-TE 5M | p3 (Figure 1c), p4 |
| MSA Transformer coupling analysis of the highest-confidence autoinhibited-RfaH cluster | Rules out the proposed mechanism ("deconvolving conflicting sets of couplings"): no contacts unique to the autoinhibited form were found, only weak contacts unique to the other form | p2 (Supplementary Figure 1b, not held) |
| Out-of-training-set / low-identity fold switchers, CF-random arm | Would rule out memorization as the source of CF-random's success — but reported only as "So does CF-random", so it rules nothing out quantitatively. UNPOWERED | p5 |
| JPred4 secondary-structure predictor as an orthogonal, non-AF2 route | Rules out that an AF2-based method is needed at all for these cases; JPred4 succeeds on the harder RfaHs and reproduces the KaiB predictions including the triple mutant | p5 (Supplementary Figure 3, not held) |
| Single-sequence prediction of all KaiB variants — **cited to ref. 11, not run here** | Rules out that coevolutionary signal is required for the KaiB result: "All KaiB predictions can be reproduced from single sequences also11." | p3 |

- **confidence_as_discriminator**: **YES, used — and the paper's central result is that it fails.**
  plDDT enters the success predicate directly ("with an average confidence ≥ 55", p2) and is the
  colour dimension of Figure 2a and the false-positive criterion in Figure 2 ("dots outside of
  dashed boxes with confidences ≥70", p4). The paper then validates that use **negatively**, in
  both directions:
  - correct structures with low confidence: "we identified several predictions from the Repo
    with low plDDT scores (Figure 1b)" (p3), and the abstract: "AF-cluster predicts many correct
    structures with low confidence" (p1);
  - wrong structures with high confidence: "Another concerning observation: AF-cluster predicts
    incorrect structures with relatively high confidence (Figure 1c)." (p3), and "the confidence
    of this ground-state prediction is higher than 4/6 correct AF-cluster KaiB predictions"
    (p4), with the mispredicted KaiB-TE 5M ground state at plDDT 90.4 (Figure 1c, p3) — the
    single highest confidence value printed anywhere in Figure 1.
  This is a validated *rejection* of confidence as a conformational discriminator for
  AF-cluster, not a validated use of it. CF-random's own use of the same criterion is not
  independently validated.

## D. Claims

- **central_conclusion**: Re-running the controls the rebutted paper omitted shows that AF-cluster
  is a poor predictor of metamorphic proteins: plain random shallow MSA sampling through
  ColabFold (CF-random) matches or beats it on accuracy and confidence across KaiB, Mad2 and
  RfaH at 1–2 runs instead of 95–329, AF-cluster's proposed coupling-deconvolution mechanism is
  not supported by contact analysis, and AF-cluster calls two experimentally confirmed single
  folders metamorphic with high confidence. The authors then concede that neither method
  predicts fold switching reliably on harder, low-identity cases, and recommend pairing AF2 with
  orthogonal evidence such as JPred4 or coevolutionary signatures.

- **necessity_claims** (verbatim + page):
  - p1: "However, their Paper lacks some essential controls needed to assess AF-cluster's
    reliability."
  - p1: "Further, we observe that AF-cluster mistakes some single-folding KaiB homologs for fold
    switchers, a critical flaw bound to mislead users."
  - p2: "This would seem to be an inappropriate control because the AF-cluster predictions of
    RfaH were generated using AF25. Controls should be performed with the same software."
  - p3: "Fold-switching proteins, including KaiB and RfaH, often have single-folding homologs.
    Thus, a good predictor must distinguish between the two9."
  - p4: "These predictive errors indicate that AF2-based predictions of mutational effects
    should be interpreted with caution."
  - p5 (impossibility / cannot-do form): "However, neither CF-random nor AF-cluster predicts fold
    switching reliably, especially in more difficult cases."
  - p5 (impossibility / cannot-do form): "In short, AF2 is an outstanding tool for generating
    three-dimensional models of protein structure, but its current ability to accurately predict
    alternative conformations is limited."
  - p5 (borderline — a recommendation carrying necessity force, recorded but flagged as such):
    "We suggest pairing its predictions with orthogonal validation–such as JPred4 predictions
    and/or coevolutionary signatures–to enhance predictive accuracy."

- **novelty_claims**: **NONE FOUND.** The paper makes no claim to be first, novel or
  unprecedented anywhere in its six pages. It does the opposite twice, explicitly disclaiming
  priority for the method it advocates:
  - p3: "Thus, randomly sampling diverse MSAs–a method proposed previously7–enables more
    accurate, higher-confidence predictions than clustering by sequence similarity."
  - p5: "These analyses indicate that CF-random, based on a method proposed previously7,
    outperforms AF-cluster, which requires more compute time and produces more false positives."
  Recording these as *anti*-novelty statements, because in a priority dispute they are what this
  paper would be held to: CF-random is asserted to be ref. 7's method, not theirs.

- **stated_limits**:
  - p5: "However, neither CF-random nor AF-cluster predicts fold switching reliably, especially
    in more difficult cases."
  - p5: "For instance, a recent benchmarking study showed that both AF2 and AF-cluster failed to
    predict the correct conformations of sequence-diverse RfaH homologs and two fold-switching
    proteins outside of AF2's training set4. So does CF-random."
  - p5: "These RfaH homologs were a more difficult test: all fold-switching sequences were <35%
    identical to their closest experimentally characterized homolog. For comparison, the
    sequences of all KaiB variants in the Paper were ≥ 47% identical to their experimentally
    characterized homologs." — i.e. their own successes are on high-identity cases.
  - p4: "CF-random also incorrectly predicts that KaiB-TE 5M is metamorphic." — their method
    fails one of their own two negative controls.
  - p4: "These predictive errors indicate that AF2-based predictions of mutational effects
    should be interpreted with caution."
  - p5: "but its current ability to accurately predict alternative conformations is limited."
  - Not stated as a limit but adjacent, p2: "Despite our previous experience generating AF2-based
    predictions of RfaH2,4,9, we had not seen AF2 generate correct models of the autoinhibited
    state from full MSAs with plDDTs so low."

- **stance**: **precedent + contrast** (provisional; the user confirms).
  - *precedent* on findings — this is the corpus's clearest demonstration that (i) depth-reduced
    random MSA sampling matches or beats a structured clustering method, (ii) plDDT does not
    discriminate conformational correctness in either direction, and (iii) a method that
    generates alternative states will call single folders metamorphic unless negative controls
    are run. The negative-control design (Figure 1c) is directly reusable.
  - *contrast* on rigour — the paper prosecutes a missing-controls case while itself setting the
    MSA depth per target on the evaluation systems (route 4), defining success by RMSD to held
    references with three mutually inconsistent and unjustified thresholds (route 5), calling one
    fold by eye (route 6), and disposing of its only anti-memorization arm in three words (p5).

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| plDDT, RfaH autoinhibited, full MSA, this work | 74.7 | plDDT (mean) | 250 AF2 models on the full RfaH MSA from the Repo | p2 |
| plDDT, RfaH, AF-cluster, as reported by the rebutted paper | 73.9 | plDDT (mean) | AF-cluster predictions | p2 |
| plDDT, RfaH, full MSA, as reported by the rebutted paper (ColabFold) | 68.6 | plDDT (mean) | full-MSA predictions | p2 |
| plDDT, Repo AF-cluster models with helical-bundle folds, recomputed | 63.8 | plDDT (mean) | AF-cluster predictions selected by fold appearance | p2 |
| Fraction of 250 full-MSA models near the reported AF-cluster value | 2 | % | 250 models | p2 |
| RfaH success rate, AF-cluster | 4 (10 of 250) | % | within 3 Å of either experimental conformation and plDDT ≥ 55 | p2 |
| RfaH success rate, randomly sampled MSAs | 24 (5 of 21) | % | same predicate | p2 |
| Matthews Correlation Coefficient, KaiB | CF-random 1; AF-cluster 0.6 | dimensionless | reference-defined state labels | p4 (Fig 2b) |
| Matthews Correlation Coefficient, Mad2 | CF-random 0.87; AF-cluster 0.7 | dimensionless | same | p4 (Fig 2b) |
| Matthews Correlation Coefficient, RfaH | CF-random 0.62; AF-cluster 0.4 | dimensionless | same | p4 (Fig 2b) |
| %Success, KaiB | CF-random 68; AF-cluster 29 | % | same | p4 (Fig 2b) |
| %Success, Mad2 | CF-random 24; AF-cluster 2 | % | same | p4 (Fig 2b) |
| %Success, RfaH | CF-random 64; AF-cluster 4 | % | same | p4 (Fig 2b) |
| Runs per ensemble, KaiB | CF-random 2; AF-cluster 329 | AF2 or ColabFold runs | compute cost | p4 (Fig 2b) |
| Runs per ensemble, Mad2 | CF-random 1; AF-cluster 95 | runs | compute cost | p4 (Fig 2b) |
| Runs per ensemble, RfaH | CF-random 2; AF-cluster 250 | runs | compute cost | p4 (Fig 2b) |
| Runs per ensemble, summary range | CF-random 1–2; AF-cluster 95–329 | runs | compute cost | p5 |
| Ensemble size compared, KaiB | CF-random 330; AF-cluster 329 | predictions | matched-n comparison | p4 (Fig 2 caption) |
| RMSD / plDDT, KaiB R. sphaeroides | CF-random 2.3 Å / 78.8; AF-cluster 3.0 Å / 63.8 | Å / plDDT | experiment | p3 (Fig 1b) |
| RMSD / plDDT, KaiB R. sphaeroides-3M | CF-random 3.0 Å / 70.6; AF-cluster 3.0 Å / 70.8 | Å / plDDT | experiment | p3 (Fig 1b) |
| RMSD / plDDT, KaiB S. elongatus | CF-random 3.9 Å / 81.7; AF-cluster 5.5 Å / 55.0 | Å / plDDT | experiment | p3 (Fig 1b) |
| RMSD / plDDT, KaiB T. elongatus | CF-random 1.6 Å / 75.2; AF-cluster 5.2 Å / 58.8 | Å / plDDT | experiment | p3 (Fig 1b) |
| RMSD / plDDT, KaiB L. pneumophilia | CF-random 3.2 Å / 82.4; AF-cluster 1.7 Å / 89.2 | Å / plDDT | experiment | p3 (Fig 1b) |
| RMSD / plDDT, KaiB T. elongatus vestitus (TV4) | CF-random 2.9 Å / 72.0; AF-cluster 2.8 Å / 85.9 | Å / plDDT | experiment | p3 (Fig 1b) |
| RMSD / plDDT, Mad2 H. sapiens | CF-random 3.3 Å / 71.8; AF-cluster 11.8 Å / 63.7 | Å / plDDT | experiment | p3 (Fig 1b) |
| RMSD / plDDT, RfaH E. coli | CF-random 3.9 Å / 76.3; AF-cluster 4.5 Å / 73.4 | Å / plDDT | experiment | p3 (Fig 1b) |
| False-positive AF-cluster predictions, KaiB-TV4 ground state | 2.1 Å / 71.0 | Å / plDDT | a fold never experimentally observed for this protein | p3 (Fig 1c) |
| AF-cluster, KaiB-TE 5M fold-switched (correct) | 2.8 Å / 90.4 | Å / plDDT | experiment | p3 (Fig 1c) |
| False-positive AF-cluster prediction, KaiB-TE 5M ground state | 2.4 Å / 82.5 | Å / plDDT | a fold never experimentally observed for this variant | p3 (Fig 1c) |
| plDDT of the rebutted paper's untested KaiB double-mutant fold switch | 68.1 | plDDT | quoted from the rebutted paper; no experimental test exists | p4 |
| Sequence identity, hard RfaH homolog set | < 35 | % identity to closest experimentally characterized homolog | difficulty stratification | p5 |
| Sequence identity, KaiB variants in the rebutted paper | ≥ 47 | % identity to experimentally characterized homologs | difficulty stratification | p5 |
| CF-random MSA depth used | max-seq 1 (KaiB), 8 (Mad2), 64 (RfaH); max-extra-seq = 2×max-seq | sequences | — | p5 |

  Figure 2b values are read from the printed bar labels on the rendered page; the text layer does
  not carry them.

- **n_predictions**:
  - *Samples per target:* KaiB — CF-random **330**, AF-cluster **329** (p4). RfaH — AF-cluster
    **250** (from the Repo), full-MSA AF2 **250** (generated by these authors), randomly sampled
    MSAs **21** (from the Repo) (p2). Mad2 — **NOT REPORTED** as a prediction count; only the run
    count is given (CF-random 1, AF-cluster 95; p4). CF-random per-target prediction counts for
    Mad2 and RfaH are **NOT REPORTED**.
  - *Runs per target (a different unit, and the one the efficiency claim uses):* CF-random 1–2
    runs, AF-cluster 95–329 runs (p5, Figure 2b p4).
  - *Targets:* 3 families; 8 proteins with per-protein numbers in Figure 1b; 2 single-folding
    negative controls; plus an out-of-training-set arm of 2 named proteins and an unspecified
    number of RfaH homologs (p5).
  - *Total:* **NOT REPORTED.** No total across all arms is stated, and it cannot be summed
    because Mad2 and RfaH CF-random ensemble sizes are missing.

- **comparable_to_ours**:

- **si_in_scope**: **SI NOT HELD.** Substantial results live outside the 6-page PDF and are not
  in the corpus. Referenced but absent: **Supplementary Figure 1a–d** (the RfaH plDDT
  distributions, MSA Transformer contacts, and the clustering-vs-random comparison — pp2–3),
  **Supplementary Figure 2** (RfaH and Mad2 true/false positives — p5), **Supplementary Figure 3**
  (JPred4 reproduction of the KaiB predictions including the triple mutant — p5),
  **Supplementary Table 1** (the AF2-version-matched re-run — p3), and **Supplementary Methods**
  ("More details about predictions and other calculations can be found in Supplementary
  Methods.", p5). The Supplementary Methods absence is the consequential one: it is where any
  justification for the per-target max-seq values 1, 8 and 64 would be, and that is the crux of
  the route-4 leakage assessment. Code and results are stated to be at
  https://github.com/porterll/CF-random (p5), also not held.

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 3 | The six experimentally determined conformations the whole paper is scored against: KaiB ground and fold-switched, Mad2 closed and open, RfaH autoinhibited and active | structure render | `RENDER \| facet: protein (3: KaiB, Mad2, RfaH) × conformation (2: dominant, alternative) \| views: 1 (single orientation per structure) \| overlay: 0 predictions on 1 reference (experiment only, no prediction shown) \| axis: none` | 6 panels in one row, varying by protein and by conformation. Fold-switching regions rainbow N→C, non-switching regions gray | RfaH is shown truncated relative to the others: "the C-terminal b-sheet domain of RfaH is shown without its gray N-terminal domain to fit in the figure" (p3). Oligomeric state is dropped without a panel: "Though monomeric units are shown, KaiB ground often folds into a tetramer and Mad2 forms a dimer with one of each conformer" (p3) — relevant because Mad2's biological conformer pair is a dimer | CC0, plus US Government work not subject to copyright under 17 USC 105. **No ND clause; redrawing permitted.** License statement on p1 (repeated in the p2 and p3 headers) |
| 1B-C | 3 | One selected prediction per protein superposed on experiment, annotated with RMSD and plDDT for both methods (B); and three AF-cluster predictions on two experimentally confirmed single folders, two of which are folds those proteins never populate (C) | structure render | `RENDER \| facet: protein (8 in B: 6 KaiB organisms, Mad2, RfaH) × method-outcome (3 in C: KaiB-TV4 ground state, KaiB-TE 5M fold-switched, KaiB-TE 5M ground state) \| views: 1 (single orientation per superposition) \| overlay: 1 prediction (navy) on 1 reference (light gray) \| axis: none` | B: 8 panels varying by protein/organism, each carrying two numeric annotations (CF-random in parentheses, AF-cluster in square brackets). C: 3 panels over 2 proteins — KaiB-TE 5M appears twice, once for the correct fold-switched prediction (bold black) and once for the false ground-state prediction (red italic); the caption names only the two proteins and does not state the three-panel split, which was resolved from the rendered page. Both letters are one row because both are single-overlay renders with no mark or measure to split on | **One model of hundreds is shown per panel with no stated selection rule** — the ensembles behind these panels are 250–330 predictions (p2, p4), and how the displayed representative was chosen is never said. This is the bar-hiding-a-distribution case in render form. Also: RMSD/plDDT for CF-random and AF-cluster are printed as bare numbers with no spread, no n, and no indication of whether they describe the displayed model or an average | as above (CC0, no ND) |
| 2A | 4 | The KaiB prediction landscape for each method in the plane of RMSD to both experimental conformations, coloured by confidence; the two dashed boxes are the two real states and everything outside them at high confidence is a false positive | scatter | `PLOT \| facet: method (2: CF-random, AF-cluster) \| vary: RMSD to ground state, 0–12 Å (continuous) \| series: confidence plDDT, 50–90 (continuous colour scale) \| measure: RMSD to fold-switched state, 0–12 Å \| mark: point \| n: 1 per mark; 330 per CF-random panel, 329 per AF-cluster panel` | 2 panels, varying by method. Dashed rectangles overlay each panel marking the ground-state (upper left) and fold-switched (lower right) basins | **The plDDT colour scale is clipped at 50 and 90** on a 0–100 metric, so every prediction below 50 and above 90 renders identically to the endpoint and confidence differences in exactly the two tails that matter are invisible. The dashed state boxes are drawn without stated coordinates, so the success region is defined graphically rather than by a printed threshold — and it corresponds to neither the 3 Å nor the 5 Å cut used in the text | as above (CC0, no ND) |
| 2B | 4 | Three head-to-head performance bars per protein: correlation with the reference labels, success rate, and compute cost | bar | `PLOT \| facet: metric (3: Matthews Correlation Coefficient, %Success, number of AF2 or CF runs) \| vary: protein (3: KaiB, Mad2, RfaH) \| series: method (2: CF-random, AF-cluster) \| measure: MCC (dimensionless) + success (%) + runs (count) \| mark: bar \| n: NOT REPORTED per bar except KaiB (330 CF-random, 329 AF-cluster); 6 bars per panel` | 3 panels, varying by metric; one row because all three share the bar mark and the same faceting, with a compound measure | **Bars with no distribution and no error bars**, over ensembles of hundreds of predictions — MCC and %Success are point estimates from binary labels whose n is given only for KaiB. **MCC ceilings at 1 for CF-random on KaiB** (cross-reference `metric_saturation`), so that comparison has no headroom. The runs panel puts a count of 1–2 against a count of 329 on one linear axis, which renders the CF-random bars as invisible stubs and forces the numbers to be printed as labels | as above (CC0, no ND) |

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude -p unattended batch smoketest
- **schema_version**: v3
- **confidence**: **medium-high.**
  - *High* on all body text: the paper is six pages, the text layer is clean, and every claim in
    sections C, D and E is quoted directly.
  - *Medium* on Figure 2b numeric values (MCC, %Success, runs). These exist only as printed bar
    labels in the image, not in the text layer, and were read from a 300 dpi render of the panel.
    The values 1 / 0.6, 0.87 / 0.7, 0.62 / 0.4, 68 / 29, 24 / 2, 64 / 4 and 2 / 329, 1 / 95,
    2 / 250 were legible, but a reader relying on these for a manuscript table should confirm
    against the source figure.
  - *Medium* on identity, because the held PDF and `refs.bib` disagree about venue, year and
    author list.
  - What was hard to read: the Figure 1c panel structure — the caption names two proteins but
    the figure has three panels — resolved by rendering p3. Greek letters are lost in the text
    layer throughout.
- **unresolved**:
  1. **Version and venue conflict.** The held PDF is the bioRxiv preprint (10.1101/2024.01.05.574434,
     posted 6 Jan 2024, four authors). `refs.bib` records `year = 2025`, `journal = Nature`,
     `doi = 10.1038/s41586-024-08267-2`, six authors (adding Lee and Thole). This note describes
     the preprint only, per the read-only-this-paper rule. If the Nature version is the one being
     cited, section E numbers and the figure table may not transfer and the note needs
     re-extraction against that PDF. The corpus also holds `waymentsteele2025reply` (JMB 2025,
     "Does Sequence Clustering Confound AlphaFold2?"), which is a reply to this paper — the
     exchange should be read as a pair.
  2. **Justification for max-seq = 1, 8, 64 is not in this PDF.** It is the single most important
     missing item: it determines whether route 4 is per-target tuning on the evaluation set or a
     principled a priori rule. It would be in Supplementary Methods, which is not held.
  3. **CF-random ensemble sizes for Mad2 and RfaH are not reported** — only run counts (1 and 2).
     The %Success and MCC bars for those two proteins therefore have no stated n.
  4. **Templates are never mentioned.** Whether ColabFold 1.5.3 ran with its default template
     search on is undeterminable from this PDF.
  5. **How the single model displayed in each Figure 1b/1c panel was selected** out of hundreds
     is not stated — by plDDT, by RMSD, or by eye.
  6. **No PDB accession codes** are given for any reference structure, so the reference set
     cannot be reproduced from the PDF alone.
  7. **The out-of-training-set result is asserted, not shown.** "So does CF-random." (p5) has no
     supporting number, figure or supplementary pointer anywhere.
  8. **Three inconsistent success thresholds** (3 Å / plDDT 55; 5 Å / plDDT 70; plDDT ≥ 70) are
     used in the text, Figure 1 and Figure 2 respectively, and the paper never reconciles them or
     says which governs the headline %Success and MCC numbers.
  9. **Tags wanted but not in the v3 vocabulary, not invented:** (a) a tag for a
     rebuttal / Matters-Arising / reanalysis-of-another-corpus-paper, which is this paper's whole
     genre and which `benchmark-only` does not capture; (b) a tag for per-target hyperparameter
     tuning, currently expressible only through the broad `oracle-leak`; (c) a tag for the
     single-folder false-positive failure mode, which is the paper's most reusable finding and
     has no reverse-lookup handle. See the Tags section note.
- **why_it_matters**:

## Tags

`general-protein` `fold-switching` `msa-subsample` `af-cluster` `benchmark-only` `ensemble`
`two-state` `binary-predicate` `continuous-metric` `visual-metric` `saturating-metric`
`oracle-leak` `design-level-oracle` `confidence-as-discriminator` `anti-memorization` `unpowered`
`preprint` `precedent` `contrast` `negative-result` `comparator-numbers`

Notes on tags applied and withheld, all from the fixed v3 vocabulary:
- `af-cluster` marks the method under examination; `msa-subsample` marks CF-random. Both are
  present and they are different arms.
- `multi-backbone` **withheld**: ColabFold and AF2 are the same backbone, and the paper says so
  (p3). MSA Transformer is used only for contacts.
- `msa-state-filter`, `template-state-bias`, `state-annotated-input`, `templates-on`,
  `no-template-no-msa` **all withheld**: no template or state-annotated input is used, and
  templates are NOT REPORTED so the de-novo regime cannot be asserted either.
- `prospective` **withheld**; see the `prospective` field.
- `anti-memorization` with `unpowered` rather than `no-anti-memorization`: an out-of-training-set
  arm was run, but reported in three words on n ≈ 2. A reverse lookup for real anti-memorization
  evidence should treat `unpowered` as disqualifying here.
- `experimental-validation` **withheld**: no experiment was performed by these authors. The NMR
  evidence is cited from the rebutted paper and from ref. 12.
- Control tags (`directed-state`, `partner-driven`, `ligand-driven`, `peptide-driven`,
  `g-protein-mimetic`, `nanobody`, `apo-sampling`, `seed-only`) **all withheld**: the method has
  no directional handle, and subsample depth is not one of the listed handles.
- Site tags **all withheld**: no binding site or pocket is studied.
- `figure-exemplar` **withheld**: the paper is worth keeping for its argument and its
  negative-control design, not for the figures themselves.
- **Tags needed but not available, recorded and not invented:** a `rebuttal` / `reanalysis` tag
  for the Matters-Arising genre; a `per-target-tuning` tag for route-4 leakage of this specific
  shape; and a `single-folder-false-positive` tag for the failure mode demonstrated in Figure 1c.
  All three are logged in `unresolved` item 9.
