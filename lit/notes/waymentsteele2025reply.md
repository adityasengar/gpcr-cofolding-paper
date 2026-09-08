# waymentsteele2025reply

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–28).** The held document is
a 28-page bioRxiv preprint with no journal pagination: p1 title/abstract/intro, p2 intro
continued, p3–4 response to ref [2], p4 response to ref [3]/[4], p5–8 response to ref [5],
p8–10 response to the Nature Matters Arising [6] and the new column-shuffling analysis,
p11 Conclusion + Methods, p12 Methods continued + data/code, p13 Acknowledgments + Appendix A,
p13–16 Appendix B, p16–18 Appendix C, p18–21 Appendix D, p21–27 Table 1 (designed sequences),
p27–28 references. Main figures: Fig 1 image p3 (caption spans p3–4), Fig 2 image p5 (caption
p6), Fig 3 p7, Figs 4 and 5 both on p10 (Fig 4 caption p10, referenced from text on p8–9).

**Framing caveat, recorded up front:** this document is one side of a three-way exchange
(original AF-Cluster paper `waymentsteele2024cluster`; Matters Arising `schafer2025confounds`;
this reply). **Everything below is what THIS document argues and reports.** Where the reply
restates a finding of the original paper it is marked as reproduced/quoted from ref [7], not as
new evidence. Nothing here is imported from the other two notes and no adjudication of the
dispute is offered.

**Reference-numbering key used throughout the paper, needed to read the quotes:**
[1] AlphaFold2 (Jumper 2021); [2] Porter et al. bioRxiv 2023.11.21.567977; [3] Chakravarty et al.
bioRxiv 2023.12.12.571380; [4] its published form, Nat Commun 15:7296 (2024); [5] Schafer et al.
bioRxiv 2024.01.05.574434; **[6] Schafer et al., Nature 2025, 638(8051):E8–E12 — the Matters
Arising**; **[7] Wayment-Steele et al., Nature 2024, 625(7996):832–839 — the original AF-Cluster
paper being defended** (p27).

**Text-layer caveat:** Greek letters render as Latin in the extracted text (α → "a", β → "b", so
"a-helical", "b-sheet"), and the degree sign in "20˚C" is a modifier letter. Verbatim quotes
reproduce the text layer as extracted; rendered pages confirm the intended glyphs.

---

## A. Identity

- **citekey**: `waymentsteele2025reply`
- **doi**: **dual, and the two do not point at the same object.**
  - In the held PDF: **10.1101/2024.07.29.605333** (bioRxiv) — p1 header: "bioRxiv preprint doi:
    https://doi.org/10.1101/2024.07.29.605333; this version posted July 15, 2025."
  - In `refs.bib` / `MANIFEST.csv`: **10.1016/j.jmb.2025.169376** (*Journal of Molecular
    Biology*). Not verifiable from inside this PDF; the PDF contains no journal DOI, no
    received/accepted dates and no JMB branding.
- **year**: **2025.** The held version was posted **15 July 2025** (p1 header, every page). The
  bioRxiv accession itself is a 2024 accession (`2024.07.29.605333`), i.e. this is a later
  version of a preprint first posted in July 2024. `refs.bib` also says 2025.
- **venue**: **DUAL, AND THE SPLIT IS THE POINT — flagged in `unresolved`.**
  - Held PDF: **bioRxiv preprint, not peer reviewed** — p1 (and every page header): "The
    copyright holder for this preprint (which was not certified by peer review) is the
    author/funder". Tagged `preprint` on the evidence of this PDF.
  - Corpus record (`refs.bib`, `MANIFEST.csv`): ***Journal of Molecular Biology*, 2025**.
  - **The document this paper replies to appeared in *Nature*, not JMB.** The paper states this
    itself: reference [6] is "Schafer, J.W., et al., Sequence clustering confounds AlphaFold2.
    **Nature**, 2025. 638(8051): p. E8-E12" (p27), and the original AF-Cluster paper [7] is also
    *Nature* (p27). The reply says explicitly that it was denied a *Nature* reply slot: "we were
    not given a chance to see the final version of the Matters Arising or submit of a final
    response" (p8), and, on the preprint version of the comment, "These false claims of 'missing
    controls' were consequently taken out during the review process with Nature for the Matter
    Arising [6] in response to our formal written response and the reviewers evaluation" (p5).
  - **Consequence for citation: a *Nature* Matters Arising (E8–E12) and a *JMB* reply are not a
    comment/reply pair in one venue.** Any sentence in our manuscript that describes this as "the
    authors' reply in *Nature*" would be wrong. See `unresolved`.
- **title**: **Recorded in both forms because the corpus needs the pair.**
  - Title on the held PDF (p1): **"Does sequence clustering confound AlphaFold2?"**
  - Title in `refs.bib` for the JMB version of record: **"Does Sequence Clustering Confound
    AlphaFold2?"** — same words, journal capitalisation only.
  - **On the reported retitling across preprint versions: NOT REPORTED inside this PDF.** The
    held version (posted 15 July 2025) carries no version history, no "formerly titled" note and
    no change log. The bioRxiv accession `2024.07.29.605333` predates this version by ~12 months,
    so at least one earlier version exists and may have carried a different title, but **nothing
    in this document states what it was.** Do not assert a former title from this note. See
    `unresolved`.
  - Note the title is a near-mirror of the comment's title, which the paper points out: "The
    Matters Arising publication is titled the same as [5] on bioRxiv" (p8). The reply's title
    turns the comment's declarative ("Sequence clustering confounds AlphaFold2") into a question.
- **authors**: **Hannah K. Wayment-Steele, Sergey Ovchinnikov, Lucy Colwell, Dorothee Kern**
  (corresponding: dkern@scripps.edu) — p1. Affiliations: Scripps Research & HHMI (Wayment-Steele,
  Kern), MIT Biology (Ovchinnikov), Google Research and Cambridge University (Colwell). Four
  authors, matching `refs.bib`.

## B. Scope

- **system**: **general protein — naturally evolved fold-switching / metamorphic soluble
  proteins.** Three families carry the whole paper: **KaiB** (circadian clock, incl. variants
  KaiB<sup>TV-4</sup>, KaiB<sup>RS</sup>, KaiB<sup>TE</sup>), **RfaH** (transcription factor), and
  **Mad2**. No membrane proteins, GPCRs, kinases or transporters anywhere. Two further systems
  appear only as *scope-limiting* discussions, not as evaluation targets: **BCCIP-α/β** (an
  alternatively spliced isoform pair, Appendix A, p4/p13) and **SA1** (an engineered fold
  switcher, p4) — both are argued to lie outside AF-Cluster's premise rather than tested.
- **n_targets**: **3 protein families**, resolved differently per arm:
  - *Column-shuffling ablation (the paper's new headline analysis):* **2 families, 81 MSA
    clusters** — "This resulted in 49 MSA clusters in total for RfaH and 32 in total for Mad2"
    (p12), plus a single-protein arm on KaiB<sup>TV-4</sup> (p8, Fig 4B).
  - *Figure 5 (the summary panel):* **13 clusters** — those returning >50% of samples in one
    state: RfaH autoinhibited 6 (000, 014, 021, 049, 056, 093), RfaH active 4 (001, 005, 015,
    024), Mad2 closed 2 (000, 046), Mad2 open 1 (042), read from the rendered p10.
  - *Single-sequence vs shallow-MSA arm:* **1 protein** (KaiB<sup>TV-4</sup>) for the new
    calculation (p4, Fig 1B–E); the reproduced panel Fig 1A covers **487 KaiB variants** from
    ref [7] (p3).
  - *CF-Random decomposition:* **1 protein** (KaiB<sup>TE</sup>, sequence in 2QKE), 2 settings
    (p11).
  - *Sampling-matched pLDDT arm:* **1 protein** (KaiB<sup>RS</sup>) (p11, Fig 3).
  - *AF2 parameter-version and masking controls:* **1 protein** (RfaH) (p11, p14–16).
  - *MSA Transformer contact arm:* **1 protein** (RfaH), all its clusters from ref [7] (p17).
  - *De novo / anti-memorization arm:* **5 deposited structures** across the 3 families —
    2QKE:E, 5JYT:A, 6C6S:D, 1S2H:A, 1DUJ:A, with the RfaH autoinhibited state substituted by an
    AF-Cluster cluster-049 model because "the autoinhibited state of RfaH (5ONDA) has
    experimentally-unresolved residues" (p12).
  - **Generality flag:** the paper's central claim about evolutionary couplings is general
    ("Our results demonstrate that evolutionary information embedded in MSA clusters is indeed
    used by AF2 to predict multiple conformational states", p2) but rests on the same three
    families as the original paper and the comment. The paper is explicit that its premise is
    scoped: it applies to "natural protein families [that] have evolved to contain more than one
    structure preference" (p4) and not to spliced isoforms or engineered switchers (p4).
- **method_class**: **DUAL — clustering + benchmark-only.** It defends the clustering method
  (AF-Cluster: ColabFold MSA → DBSCAN → AF2 per cluster) and runs no new predictive method; every
  new calculation is a control, an ablation, or a re-run of an existing protocol. A third
  component, **MSA-subsampling**, appears only as the *comparator being rebutted* (CF-Random's
  `max_msa`/single-sequence settings) and as a reproduced arm, not as this paper's method.
- **backbones**: **AF2 only**, in two implementations that the paper deliberately compares —
  DeepMind AlphaFold notebook and **ColabFold** [19] (Figure B1, p14: "AlphaFold and ColabFold
  return the same result when given the same MSA and same settings"). Two non-structure-predictor
  models are used as instruments: **MSA Transformer** [23] for contact prediction (Appendix C,
  pp16–18) and **ProteinMPNN** [26] for inverse-folding sequence design (p12). **No AF3, Boltz,
  Chai, OF3 or Protenix anywhere. NOT tagged `multi-backbone`** — comparing two implementations
  of the same network and two parameter *versions* of it is not a head-to-head of two backbones.
  The parameter-version comparison is nevertheless central: `model_[1-5]` (older) vs
  `model_[1-5]_ptm` (current, used in AF-Cluster) — p14.
- **templates**: **NOT REPORTED.** The word "template" does not appear in the Methods (pp11–12)
  or anywhere in the paper. Every run is described by its MSA input, model number, seed, dropout
  and recycle count; whether ColabFold/`run_af2.py` ran with templates on or off is never stated.
  This blocks a clean `no-template-no-msa` tag for the single-sequence arms — see `unresolved`.
- **msa_handling**: **Four regimes are run in this paper, and they must not be collapsed:**
  1. **clustered** — DBSCAN clusters of a ColabFold MSA, the AF-Cluster method under defence; the
     paper restates its own definition: "From here on we refer to this entire pipeline as
     'AF-Cluster' – generating a MSA with ColabFold, clustering MSA sequences with DBSCAN, and
     running AF2 predictions for each cluster." (p3);
  2. **subsampled** — "shallow" MSAs of the 10 closest sequences by edit distance from the
     phylogenetic tree ("we refer to MSAs constructed of the 10 closest sequences from the
     phylogenetic tree as 'shallow' MSAs", p4), plus single-sequence mode and
     `max_msa:extra_msa=1:2` reproduced from the comment (p6, p11);
  3. **full MSA** — the unclustered ColabFold alignment, used as the comparison arm (p6, p14);
  4. **shuffled (new, and the paper's key ablation)** — "We kept the first sequence of the MSA
     (the query sequence) the same, and shuffled residues within each column of the input MSA
     clusters, which ablates any potential evolutionary relationships beyond single-site
     conservation" (p8). This is a *column-wise permutation within an existing cluster*; it is
     neither subsampling nor state-filtering, and the corpus has no field value for it — recorded
     here and in `controls_run`.
  A fifth, non-natural regime appears in the anti-memorization arm: **de novo designed sequence
  sets used as the MSA** (14–15 ProteinMPNN sequences per fold, p12).

## C. Conformational core

- **states_generated**: **two + ensemble.** *Two* because every arm is scored against exactly two
  deposited conformations per family (RfaH autoinhibited 5OND / active 2LCL — 6C6S in Appendix C;
  Mad2 closed 1S2H / open 1DUJ; KaiB ground 2QKE / fold-switched 5JYT), and cluster outputs are
  binarised into one or the other (p12). *Ensemble* because the new sampling protocol produces a
  distribution per cluster and the paper reads the distribution, not a single model: "we ran these
  in all 5 models, with dropout, for 3 different seeds, and for 3 recycles" (p12), and the
  distribution is what Figures 4D–E, 5, D1 and D2 plot. The paper insists the *family-level*
  distribution is the object of interest, not a two-state output: "AF-Cluster was developed as a
  method to detect the distribution of structure preferences across an entire protein family"
  (p5).
- **structural_priors_used**: **Extensive, and legitimate for a rebuttal — this is design-time
  structural knowledge, not pipeline leakage. Kept separate from `oracle_leakage` by design.**
  - *Target selection:* all three families were chosen (in ref [7], and inherited here) because
    **both** conformations are experimentally determined. Every deposited structure used as a
    reference frame is named: 8UBH (the authors' own NMR structure of KaiB<sup>TV-4</sup>, p4),
    2QKE and 5JYT (KaiB, p12), 5OND / 5ONDA and 2LCL / 6C6S / 6C6SD (RfaH, p10, p12, p16, p18),
    1S2H and 1DUJ (Mad2, p10, p12).
  - *Design of the anti-memorization control:* the de novo sequences are **inverse-folded from
    deposited coordinates** — "We used the ProteinMPNN [26] implementation on HuggingFace ... to
    design sequences corresponding to the structures 2QKEE, 5JYTA, 6C6SD, 1S2HA, 1DUJA" (p12).
    Using solved structures to *design an input* is a structural prior; it is what the control
    requires and is not a methodological sin.
  - *Evolutionary/structural rationale for the method itself:* the introduction builds the
    premise from known metamorphic biology — KaiB from a thioredoxin-like ancestor, RfaH from
    NusG by gene duplication, Lymphotactin by ancestral sequence reconstruction (p2). This is
    prior knowledge shaping the hypothesis, recorded here rather than as leakage.
  - *Scope exclusions decided from structure:* BCCIP-α/β is excluded after inspecting MSA
    coverage against the two deposited isoform structures 8EXE:B and 7KYS:A (p13).
- **oracle_leakage**: **All seven routes worked separately. Where the reply merely re-runs the
  original AF-Cluster protocol rather than devising a new one, that is said and the page cited
  rather than the protocol re-derived from scratch — the original protocol belongs to
  `waymentsteele2024cluster`, not to this note.**

  **Route 1 — deposited structures used as input or template.**
  **NONE FOUND for the structure-prediction arms**, on the protocol as described on pp11–12: every
  AF2 run in this paper is specified by an MSA input (`run_af2.py <a3m>`, `--model_num`,
  `--recycles`), a seed, dropout and a model number, with no structure argument. The commands are
  printed literally, e.g. "python run_af2.py data_sep2022/06_kaibtv4_followup/msas/scrambled/
  scramble_<REP>.a3m --model_num <NUM> --recycles <N_RECYCLES> --output_dir ." (p12), and the
  MSA-cluster runs use "`coevolutionary_ablation_2025/run_all.py` available in the Github
  repository corresponding to [7]" (p12). **The clustering itself is stated to be
  structure-blind**: "AF-Cluster is an automated method using the statistical method DBSCAN, and
  is not dependent on current information on known structures." (p6).
  **PRESENT, indirectly, in one arm:** the anti-memorization control feeds AF2 an MSA whose
  sequences were **generated from deposited coordinates** — "we used the ProteinMPNN [26]
  implementation ... to design sequences corresponding to the structures 2QKEE, 5JYTA, 6C6SD,
  1S2HA, 1DUJA. Because the autoinhibited state of RfaH (5ONDA) has experimentally-unresolved
  residues, we used the structure from cluster 049 from the AF-Cluster data respository [7]."
  (p12). The AF2 input is a sequence file, not a template, but the sequences are a lossy encoding
  of the target coordinates. This is inherent to the control's logic and is why it is also logged
  under `structural_priors_used`; it is nonetheless a structure-derived input and is recorded
  here so the claim is checkable.
  **Templates: unverifiable — NOT REPORTED** (see `templates`, section B). Route 1 cannot be
  closed on the template sub-question from this PDF.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving
  templates or alignments.**
  **NONE FOUND.** No state-annotated database is used or named anywhere. The only databases
  invoked are **SwissProt and the PDB, and they are used as *exclusion* filters for the
  anti-memorization control, not as state annotations**: "We used BLAST[27] to compare each of
  these sequence sets to both the PDB and SwissProt on June 15, 2025 and removed any sequences
  that resulted in hits to either database." (p12). Alignments come from ColabFold's own search
  (p3, p13). Protocol described on pp11–12.

  **Route 3 — cluster labels derived from known states.**
  **Cluster *membership*: NONE FOUND** — DBSCAN is unsupervised and structure-blind (p6, quoted
  under route 1); the clusters analysed here are the clusters from ref [7], not relabelled.
  **Cluster *selection for analysis*: PRESENT.** Which clusters entered the new headline analysis
  was decided partly by their previously observed agreement with known states: "we ran all MSA
  clusters from ref. [7] that either were the MSA clusters that generated the structure models
  for RfaH and Mad2 originally depicted in ref. [7], as well as any MSA cluster with 10 or more
  sequences." (p12). The size criterion (≥10 sequences) is state-blind; the first criterion is
  not. The displayed representatives are chosen by outcome against the references: "Figure 4C
  depicts all structures from two representative MSA clusters that predicted the RfaH
  autoinhibited and active state." (p9). And Figure 5 restricts to the subset that already agreed
  with a known state: "for the 13 clusters across RfaH or Mad2 that returned more than 50% of
  their samples as the same state after adding more stochasticity, all but one suffered when
  coevolution was ablated" (Fig 5 caption, p10). This is analysis-level, not input-level: the
  labels do not reach the predictor.

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
  states.**
  **PRESENT, in the state-calling thresholds, and the paper states the tuning openly:**
  *"We categorized RfaH structure outputs as autoinhibited or active states based on TMscore of
  the C-terminal domain, using a TMscore cutoff of 0.65 for both states. This was based on
  inspecting returned models. We categorized Mad2 structure outputs as open or closed state using
  a TMscore cutoff of 0.72. These TMscore cutoffs were based on inspecting resulting models."*
  (p12). Both cutoffs are set by eye on the evaluation outputs, against the held references, with
  no independent justification — the v3 rule that tuning a *range* or threshold on the evaluation
  set is leakage applies directly, and here it is a per-family value (0.65 vs 0.72).
  **A second, softer instance:** the ">50% of samples in the same state" criterion that defines
  Figure 5's 13-cluster set (p9, Fig 5 caption p10). The paper does show the alternative cutoffs
  it could have used — "Figure D3 depicts the number of clusters that returned either state,
  either original MSA cluster or shuffled cluster, at different fraction cutoffs of all samples
  generated from the MSA" (p12) — which makes the choice inspectable, but 0.5 is still the value
  chosen for the headline claim.
  **Sampling settings (5 models, 3 seeds, dropout, 3 recycles, p12; 10 shuffle replicates, p12;
  33 seeds, p11; 50 seeds, p14) are stated flat, with no evidence of tuning against outcomes —
  NONE FOUND for those.**

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.**
  **PRESENT, and it is the primary success criterion of every new analysis.**
  - RMSD to the authors' own NMR structure: "We find that with the shallow MSA, all models
    converge within 1 recycle to 2 Å of the NMR structure with high confidence (Figure 1B,D upper
    row). In contrast, with a single sequence, 4 models result in wrong structures even after
    many recycles, and only model 5 obtains the lowest RMSD to 8UBH (2.28 Å) in 7 recycles"
    (p4).
  - TM-score to both deposited states as the coordinate system: "models from the same sequence
    cluster tended to go to the same part of structure space, as characterized by TM-score to two
    known structures of the fold-switching families (Figure 4D,E)" (p9); the TM-score cutoffs of
    route 4 then binarise it (p12).
  - The shuffling result itself is stated as a distance-to-reference result: "Performing this test
    using KaiB<sup>TV-4</sup>, first questioned in [2], shows that the MSA cluster resulted in
    substantially lower RMSD after zero recycles, whereas with shuffled MSAs, AF2 struggled to
    find the correct structure even after 12 recycles (Figure 4B)." (p8).
  - One deliberate *exception* the paper flags: Figure 5's metric is reference-free with respect
    to confidence, though not with respect to structure — "Figure 5 depicts TM-score to the final
    state predicted from the original MSA cluster ... Note this is not dependent on pLDDT or
    other model quality metrics." (p9). The anchor there is the original cluster's own output,
    which is a genuine methodological improvement over anchoring on a PDB entry, but the state
    labels on the panels still come from the deposited pair.

  **Route 6 — best/worst model labels assigned against a held reference.**
  **PRESENT, and stated in a figure caption:**
  *"Models were selected at the recycle at which any model from single-sequence mode obtains the
  lowest RMSD to our solved NMR structure."* (Figure 1D caption, p4). The display frame of the
  head-to-head comparison in Figure 1D is chosen by the oracle — the recycle number shown is the
  one most favourable to the arm being criticised, which is a *conservative* use, but it is
  reference-driven selection and must be recorded.
  Also reference-driven: Figure 1E labels a specific model from the opposing paper as wrong by
  comparison with 8UBH — "Picked structure of KaiB<sup>TV-4</sup> from Fig. 1 in [2] from single
  sequence mode, which was used by Porter et al. to claim that single sequence predicts correct
  structures, rotated to the same orientation, is the incorrect structure, compared to our solved
  NMR structure of KaiB<sup>TV-4</sup> [7]" (p4).
  A **pLDDT-based** (not reference-based) selection is used in the de novo arm: "The structures
  depicted in Appendix D4 are the top-ranked structure predictions from ColabFold by pLDDT."
  (p12) — recorded under `confidence_as_discriminator`, not here.

  **Route 7 — design-level oracle use (systems or input conditions chosen because the expected
  answer is already known). PRESENT. Label design-level; weaker than pipeline leakage, do not
  conflate with routes 4–6.**
  - The three families are chosen precisely because both conformations were solved before any
    prediction was read; the whole TM-score coordinate system in Figures 4D–E and 5 presupposes
    it (p9, p12). For a rebuttal this is unavoidable — the disputed claims are about these
    systems — but it is design-level oracle use.
  - The **direction of the expected result is declared before the experiment**: the shuffling test
    is introduced as "a new direct test for the role of evolutionary couplings" whose expected
    outcome is stated in the same paragraph — "Our results demonstrate that evolutionary
    information embedded in MSA clusters is indeed used by AF2" (p2, abstract-adjacent framing
    repeated at p1).
  - The anti-memorization control is designed *for* structures whose answer is known, and its
    expected answer is stated before the result: "If AF2 required memorized natural sequences, one
    would not expect these predictions to succeed." (p9).
  - The **BCCIP and SA1 exclusions are decided in advance on principle**, not on measurement:
    "However, this is not an example where we would expect AF-Cluster to be applicable." (p4) and
    "Since it is engineered, we do not expect the principle underlying AF-Cluster to apply" (p4).
    Excluding negative test cases by prior expectation is a design-level move and is the single
    most consequential route-7 instance in this paper.

  **Summary verdict:** the predictor is fed nothing state-annotated (routes 1–2 clean on the
  prediction arms; route 1 present only in the de novo control, by construction), cluster
  membership is unsupervised but the clusters *analysed and displayed* are picked by prior
  agreement with known states (route 3), the state-calling TM-score thresholds are set by eye on
  the evaluation outputs (route 4), success is RMSD/TM to held references throughout (route 5),
  the Figure 1D display frame is chosen by lowest RMSD to the reference (route 6), and both the
  system set and the excluded counter-examples are design-level oracle (route 7).

- **prospective**: **no.** Every new calculation in this document is retrospective by
  construction: it re-runs an existing pipeline on systems whose two conformations were already
  deposited, and scores against them (routes 5–6 above). No new prediction is made and then
  tested. **Partial nuance, recorded so the note is not unfair:** the paper's strongest
  prospective evidence is *prior* work, not new here — the NMR structure 8UBH of the
  KaiB<sup>TV-4</sup> prediction and the triple-mutant design, both from ref [7], which it
  restates on p11: "we made one single protein, and our NMR experiments fully verified our
  computational predictions. We note that such one to one agreement between prediction and
  experiment is rare". That prospective test belongs to `waymentsteele2024cluster`; nothing
  prospective is added by this document.
- **state_metric**: **DUAL — continuous coordinate + binary predicate**, with an explicitly
  admitted **visual** component in how the predicate was set.
  - *Continuous:* RMSD to a single reference in Å (Figures 1B–C, 4B: "RMSD to 8UBH (Å)",
    axes 0–10 Å, p3/p10); RMSD to *both* references as a 2-D plane (Figure 2A/2C/2D, p5); TM-score
    to *both* references as a 2-D plane (Figures 4D–E, D1, D2, p10/p19/p20); TM-score to the
    original cluster's own predicted state (Figure 5, p10).
  - *Binary predicate, thresholds stated:* **TM-score ≥ 0.65 for RfaH (C-terminal domain, both
    states) and ≥ 0.72 for Mad2** (p12), plus a **>50% of samples** aggregation rule (p9).
  - *Threshold justification:* **stated but not principled** — "These TMscore cutoffs were based
    on inspecting resulting models." (p12). Tagged `visual-metric` for this reason and for the
    purely visual reading of Figure 4C: "The AF-cluster predictions return the known structures,
    after shuffling no meaningful structures are obtained." (Fig 4 caption, p10) — "no meaningful
    structures" has no operationalised definition.
- **metric_saturation**: **NONE FOUND numerically.** TM-score is bounded [0, 1] and no arm sits at
  either bound: the highest boxes in Figure 5 (RfaH cluster 000, recycles 1–3) sit near 0.8 and
  the lowest near 0.05, with visible spread throughout (p10). RMSD has no ceiling and the plotted
  0–10 Å window is not hit at the top by the local-10 arm. pLDDT in Appendix B is plotted as a
  fraction over ~0.57–0.85 (Figures B2, B3, p15–16), nowhere near 0 or 1. The one *bounded*
  quantity that could ceiling — "fraction of total samples in the same state" — is deliberately
  swept across its full range rather than reported at one point (Figure D3, p20–21). **Axis-range
  problems do exist in this paper and are recorded in `hides` on rows `2A,2C-D` and `3`, not
  here.**
- **directional_control**: **NO instructable handle. The method samples; the state is read off
  afterwards.** The only handle is **which DBSCAN MSA cluster you feed AF2** — and by the paper's
  own argument that handle is discovered, not commanded: clusters must be run and their outputs
  classified before you know which state a cluster favours (p9, p12). No partner, ligand,
  nanobody, peptide, state-annotated template or state-filtered MSA is used anywhere.
  Two near-handles are discussed and both are attributed to the *opposing* method rather than
  claimed: (i) **MSA depth**, where the paper's point is precisely that the two CF-Random settings
  each deterministically select a state — "the two settings selected uniquely predict only one or
  the other state, as we had already reported in [7]" (Fig 2 caption, p6) — i.e. depth *is* a
  directional handle, but one whose direction was chosen with knowledge of the answer; and
  (ii) **comparison to the PDB**, which the paper rejects as non-generalising: "CF-Random as
  published in [6] includes comparing to known structures in the PDB to pick an alternate
  conformation, which again would not generalize for proteins with uncharacterized alternate
  states." (p6). **Seeds and dropout are used to broaden sampling, not to steer** (p12).
- **anti_memorization_design**: **PRESENT, NEW IN THIS DOCUMENT, and unusual in kind.** Not a
  post-cutoff held-out set but a **de novo sequence set constructed to be absent from the
  databases**:
  - *Construction:* ProteinMPNN at temperature 1.0, 15 sequences per structure, over 5 deposited
    structures (2QKE:E, 5JYT:A, 6C6S:D, 1S2H:A, 1DUJ:A, plus a cluster-049 model standing in for
    5OND) — p12.
  - *Cutoff definition:* **not a date-based training cutoff but a similarity screen with a date
    stamp** — "We used BLAST[27] to compare each of these sequence sets to both the PDB and
    SwissProt on June 15, 2025 and removed any sequences that resulted in hits to either database.
    This removed 1 sequence each for 2QKEE, 5JYTA, and 5ONDA. No further statistically significant
    hits at BLAST's default settings were identified." (p12).
  - **n = 14–15 sequences per fold across 5 folds** (p9: "14-15 de novo sequences for KaiB, RfaH,
    and Mad2 folds that are dissimilar to any sequences in SwissProt as of June 2025"). The full
    sequence set is printed as Table 1 (pp21–27), so it is auditable.
  - **Caveat the paper does not state:** BLAST at default settings against SwissProt and the PDB
    is not the same as absence from AF2's training set, and no training-set list or model cutoff
    date is invoked.
- **anti_memorization_control**: **RUN — but UNPOWERED and reported without a single number.**
  The arm exists and was executed: the de novo sequence sets "were then used as MSA inputs to
  ColabFold[19]" (p12) and the outcome is Appendix D4 (p21). The entire quantitative content of
  the result is a qualitative sentence and a set of renders:
  *"We found that with these MSAs of de novo proteins, AF2 was able to robustly predict the
  structures (Appendix D), indicating that MSAs of natural proteins are not a requirement for AF2
  to predict the metamorphic protein structures it is capable of predicting."* (p9).
  **Mark UNPOWERED:** n = 5 folds (well under ~10); the readout is one top-pLDDT model per fold
  overlaid on its experimental structure (Fig D4B, p21) with **no RMSD, no TM-score, no pLDDT
  value, no distribution and no failure count reported**. The state-calling machinery built for
  the rest of the paper (TM ≥ 0.65 / 0.72, p12) is not applied to this arm. This is the paper's
  answer to the memorization hypothesis, and it carries less quantitative support than any other
  analysis in the document.
- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| **MSA column shuffling within each cluster, query sequence retained** — the paper's new headline ablation, "shuffled residues within each column of the input MSA clusters, which ablates any potential evolutionary relationships beyond single-site conservation" | Rules out that single-site conservation (residue frequencies per column) alone explains a cluster's state preference; isolates pairwise/higher-order coevolutionary signal as the operative variable | p8 (design), p11–12 (commands), p10 (Figs 4, 5), p19–20 (Figs D1, D2) |
| Shuffling replicates: **10 independent shuffles** for KaiB<sup>TV-4</sup>, each run over 5 AF2 models × 0–12 recycles | Rules out that a single unlucky permutation produced the shuffled-arm failure | p12 (`scramble_<REP>`, REP 0–9), p10 (Fig 4B) |
| **Increased-stochasticity re-run of every reported cluster**: 5 AF2 models × 3 seeds × dropout × 3 recycles, over 49 RfaH and 32 Mad2 clusters ("20 times more sampling than in [7]") | Rules out that the original one-model/one-seed cluster→state assignments in ref [7] were stochastic flukes; establishes which clusters return a state in >50% of samples before the ablation is applied | p8–9, p12, p10 (Fig 5 caption) |
| **Shallow (local-10) MSA vs single sequence**, all 5 AF2 models, 0–12 recycles, KaiB<sup>TV-4</sup> | Rules out the claim that single-sequence input is equivalent to a shallow MSA: 5/5 models converge to ~2 Å with the MSA; 4/5 are wrong without it | p4, p11, p3 (Fig 1B–D) |
| **Decomposition of CF-Random into its two constituent settings** — default ColabFold (full MSA) and `max_msa:extra_msa=1:2`, 33 random seeds each, KaiB<sup>TE</sup> | Rules out that CF-Random is a single random-sampling procedure: each setting deterministically returns one state, so the two-state result is a union of two hand-picked settings | p6, p11, p5 (Fig 2D) |
| **Sampling-budget-matched re-run of AF-Cluster**: KaiB<sup>RS</sup> cluster with 5 models × 5 seeds × 3 recycles, i.e. CF-Random's own budget | Rules out that CF-Random's pLDDT advantage is a method difference rather than a sampling-budget artifact: max pLDDT rises 63.8 → 70.8 at the same RMSD | p6, p11, p7 (Fig 3) |
| **AF2 parameter-version control**: `model_[1-5]` (older) vs `model_[1-5]_ptm` (current), 50 random seeds each, RfaH | Rules out that the opposing preprint's pLDDT values are comparable to AF-Cluster's: the two parameter sets give significantly different values, and only the older set reproduces [5] | p14, p11, p15 (Fig B2) |
| **Random-masking on/off control** for the RfaH full-MSA arm, across all 5 AF2 models | Rules out that a masking discrepancy the authors found in their own paper explains the cluster-49-vs-full-MSA pLDDT gap: cluster 49 is higher in 4 of 5 models with masking matched | p15, p11, p16 (Fig B3) |
| **Implementation control**: DeepMind AlphaFold notebook vs ColabFold on the same MSA and settings (`use_bfloat16=False`) | Rules out that AF2-vs-ColabFold implementation differences drive any comparison in the exchange — outputs superimpose without alignment | p14 (Fig B1) |
| **MSA Transformer across all RfaH clusters with a bootstrap baseline** (average of 5 randomly selected clusters, 100 iterations), rather than the single cluster used in the comment | Rules out that a contact analysis of one cluster generalises; shows state-specific contact enrichment relative to a within-paper baseline | p17–18 (Figs C1, C2) |
| **ProteinMPNN de novo sequence MSAs** (14–15 sequences per fold, BLAST-screened against PDB and SwissProt, 15 June 2025) fed to AF2 for 5 deposited structures | Would rule out the memorization alternative hypothesis for the shuffling result — but reported qualitatively with no metric, so it rules it out only visually. **UNPOWERED** | p9, p12, p21 (Fig D4) |
| **Sweep of the aggregation threshold** — cluster counts at every "fraction of total samples" cutoff, not just 0.5, for original and shuffled MSAs | Rules out that the headline 13-cluster result is an artifact of the 0.5 cutoff | p12, p20–21 (Fig D3) |
| **MSA coverage check on BCCIP-α/β** (ColabFold coverage over the alternatively spliced region) | Rules out that AF-Cluster should have been expected to distinguish the isoforms at all: no coevolutionary information exists in the region where they differ | p4, p13 (Appendix A) |

- **confidence_as_discriminator**: **Used in places, but explicitly and repeatedly rejected as a
  conformational or thermodynamic discriminator — and the new headline analysis is deliberately
  built to avoid it.**
  - *Rejected:* the paper re-quotes its own original text — "Firstly, the pLDDT metric itself
    cannot be used as a measure of free energy. This was immediately evident in our investigation
    of KaiB, where in our models generated with AF-Cluster, the thermodynamically-disfavored FS
    state, still had higher pLDDT than the ground state" (p7) — and adds "we do not view obtaining
    high pLDDT as a main parameter to optimize" (p6) and "we do not expect that every cluster
    should return a high-pLDDT structure, making high-pLDDT return rate an inappropriate measure
    of success for AF-Cluster" (p8). It points to alternatives without endorsing one: "Metrics
    based on other outputs from AF2 such as ipTM or PAE ... may already provide better insight
    [22]" (p7).
  - *Designed out of the key analysis:* "Figure 5 depicts TM-score to the final state predicted
    from the original MSA cluster for both the original and shuffled MSAs, from 0 to 3 recycles.
    Note this is not dependent on pLDDT or other model quality metrics." (p9).
  - *Still used, in three places:* pLDDT is the colour dimension of Figures 2A/2B, 4D–E, D1 and D2
    (p5, p10, p19–20); it is the whole y-axis of the sampling-budget and parameter-version
    arguments (Figures 3, B2, B3 — p7, p15, p16); and it selects the single model shown in the
    anti-memorization control, "the top-ranked structure predictions from ColabFold by pLDDT"
    (p12).
  - *A confidence-based failure is used as evidence against the opposing paper:* "Without prior
    knowledge, from the output of the single sequence predictions, one might pick the incorrect
    structural prediction, model 3, as it has the highest confidence." (p4) — i.e. confidence is
    shown to mis-rank, which is itself a validation-by-refutation of confidence as a
    discriminator.
  - **No positive validation of pLDDT as a state discriminator is offered anywhere.**

## D. Claims

- **central_conclusion**: The comment's core critique — that AF-Cluster's MSA clusters carry no
  usable local evolutionary coupling information, so clustering does no work that depth-matched
  random subsampling could not do — is wrong. A direct ablation (shuffling residues within MSA
  columns, which destroys coevolution while preserving per-column conservation) degrades or
  destroys the state-specific predictions of 12 of 13 clusters across RfaH and Mad2 and of the
  KaiB<sup>TV-4</sup> cluster, and a de novo sequence control argues the degradation is not a
  memorization artifact. Secondarily, the reply argues that CF-Random is not a random-sampling
  control at all but a union of two hand-chosen settings that each return one state, and that the
  comment's reproduction failures stem from using an older AF2 parameter set.
- **necessity_claims** — **verbatim, with pages. These are the load-bearing rebuttal sentences.**
  - **The central rebuttal, p1 (abstract):** *"However, Porter et al.'s primary critique, that
    AF-Cluster does not use local evolutionary couplings in its MSA clusters, is incorrect. We
    report here further analysis that underscores our original finding that local evolutionary
    couplings do indeed play an important role in AF-Cluster predictions, and refute all false
    claims made against [7]."*
  - p2: *"We conclude with a new direct test for the role of evolutionary couplings by comparing
    predictions from MSA clusters to those from MSAs with shuffled columns, which ablates
    coevolutionary signals while preserving single-site conservation. Our results demonstrate that
    evolutionary information embedded in MSA clusters is indeed used by AF2 to predict multiple
    conformational states, thereby clarifying this important question of the role of
    coevolutionary signal in modern structure prediction for the field."*
  - p2: *"We next describe why the constructed CF-Random method in refs. [5,6] is not random
    sampling: it combines multiple AF2 settings that still must be individually (subjectively)
    selected and is not a direct test for evolutionary couplings in AF-Cluster."*
  - p8, rejecting the comment's inference: *"Schafer et al. argue that because no evolutionary
    couplings can be detected in the shallow MSAs used as part of CF-Random, it cannot be the case
    that AF2 [1] is using evolutionary coupling information from sequence clusters in AF-Cluster.
    This logic does not hold."*
  - p8, the explicit "not a valid control" claim: *"Constructing the 'CF-Random' method to query
    AF-Cluster has confounding factors: for instance, the 'max_msa' random sampling that it relies
    on also performs clustering internally at the AF2 MSA processing step, so it is not a valid
    control for AF-Cluster."*
  - p9, the conclusion drawn from the new ablation: *"This test reinforces that AF-Cluster is
    leveraging local co-evolutionary signals and sequence preferences to make its predictions."*
  - p9, the memorization rebuttal: *"indicating that MSAs of natural proteins are not a
    requirement for AF2 to predict the metamorphic protein structures it is capable of predicting.
    If AF2 required memorized natural sequences, one would not expect these predictions to
    succeed."*
  - p6, on generalisation: *"Critically, CF-Random as published in [6] includes comparing to known
    structures in the PDB to pick an alternate conformation, which again would not generalize for
    proteins with uncharacterized alternate states. In contrast, AF-Cluster is an automated method
    using the statistical method DBSCAN, and is not dependent on current information on known
    structures."*
  - p6, on sampling: *"Schafer et al. did not compare the two methods with equivalent sampling."*
  - p8, on efficiency: *"Finally, [5]'s claim that CF-Random is more efficient is also incorrect:
    when wall time is correctly tallied, CF-Random as reported and AF-Cluster as reported use
    equivalent sampling."*
  - p4, scope limit stated as an impossibility: *"Therefore, no coevolutionary information exists
    from the outset in the MSA for AF2 or AF-Cluster to use to distinguish differing sequence
    preferences."* (BCCIP-α/β)
  - p4, second scope limit: *"Since it is engineered, we do not expect the principle underlying
    AF-Cluster to apply – namely, the principle that natural protein families have evolved to
    contain more than one structure preference."* (SA1)
  - p14, on the necessity of matched settings: *"The pLDDT values for both the full-MSA and the
    clustered sequences depend on the specific AF2 model, so it is essential that controls are
    performed with the same AF2 implementation and models. With proper controls in place, our
    benchmarking supports our original finding, that clustering the input MSA and using these
    clusters as input achieves higher pLDDT for the RfaH autoinhibited state than the full MSA,
    and that the claim made by [5] is false."*
  - p14, the incomparability claim: *"Therefore, [5]'s calculations cannot be compared to what we
    reported in the paper."*
  - p15: *"Therefore, controls varying other aspects must be performed using the same parameter
    set, as we did in our paper, but was not done in [5]."*
  - p16, on the contact-map claim: *"The claim of 'weak contacts unique to active b-sheet' (red
    box) cannot be validated since this region is not resolved in the crystal structure of the
    RfaH autoinhibited state (PDB: 5OND)."*
  - p7, on the metric (a quotation of their own ref [7], reasserted here): *"Firstly, the pLDDT
    metric itself cannot be used as a measure of free energy."*
  - p11, on the internal contradiction alleged in the opposing work: *"Comparing the main claims
    of [2] and [5], we want to highlight an intrinsic contradiction by the Porter lab in their own
    claims: the claim in [2] (single sequence is sufficient) to the second claim that CF-Random
    (which would be using a collection of sequences) is the way to predict the correct
    conformations [5]."*
- **novelty_claims** — **verbatim, with pages. Sparse, as expected for a reply, and one of them is
  an explicit *anti*-novelty statement.**
  - p2, the one clear novelty claim: *"We conclude with **a new direct test** for the role of
    evolutionary couplings by comparing predictions from MSA clusters to those from MSAs with
    shuffled columns"* (emphasis added to mark the claim word; the sentence is quoted in full
    under `necessity_claims`).
  - p8, explicitly disclaiming novelty for that same test: *"To directly probe the role of
    evolutionary couplings in AF-Cluster, we performed **a common control test that can be applied
    to any computational method where an MSA is used as input** [23, 24]."*
  - p11, a rarity rather than a priority claim: *"We note that such one to one agreement between
    prediction and experiment is rare, often in protein design and prediction many constructs are
    tested and only a few show such agreement."*
  - p11: *"One of [7]'s most impactful results was our experimental testing of computational
    predictions."*
  - p8, a field-level need rather than a first: *"As it is increasingly clear that there are many
    factors influencing AlphaFold predictions, to directly make claims about the influence of any
    given factor such as evolutionary couplings, the field needs interpretability tests that
    directly query specific factors of interest."*
  - **No claim to be first at anything is made anywhere in the paper.**
- **stated_limits**: The paper is unusually forthcoming, partly because conceding scope is part of
  its rebuttal strategy.
  - On the method not being final: "Deep learning methods development moves quickly, and by no
    means did we think that the implementation of AF-Cluster in [7] would be the final word on how
    to sample multiple conformations." (p1).
  - On the problem being open: "The topic of how to predict multiple conformations from sequence
    is clearly far from solved. Experimental tests are critical, and are the major rate-limiter of
    methodological advancement." (p11).
  - On MSA construction being unsolved: "We want to emphasize here that how subsampled MSAs should
    optimally be constructed is an interesting question." (p3).
  - On expected per-cluster failure — stated twice: "we do not expect that every cluster should
    return a high-pLDDT structure, making high-pLDDT return rate an inappropriate measure of
    success for AF-Cluster" (p8); "we want to emphasize we do not expect all clusters to have
    higher pLDDT" (p14).
  - **A conceded counter-example:** "We note that only one of all these clusters showed equivalent
    ability to predict the RfaH autoinhibited state: cluster 049, which is the single cluster that
    was the subject of the majority of Schafer et al.'s investigations in Supplemental Figure 1 of
    [6]." (p9) — i.e. the one cluster where shuffling did *not* hurt is the cluster the comment
    concentrated on.
  - **A conceded reproducibility failure of their own:** "We also could not exactly reproduce the
    top model reported in CF-Random data repository with CF-Random's reported settings in [6]."
    (p6).
  - **A conceded inconsistency in the original paper:** "One discrepancy we realized in our paper
    is that the RfaH full MSA predictions (Extended Data Figure 6a in ref. [7]), run with
    ColabFold, included random masking, whereas the models generated with `run_af2.py` in the rest
    of the paper did not include random masking." (p15).
  - On the interpretability problem in principle: "Because AF2 was trained with both sequence and
    structure information, we expect that sequence and structure information are convolved, and
    disentangling the effect of either is difficult." (p1).
  - Scope limits: not applicable to alternatively spliced isoforms (p4) or engineered fold
    switchers (p4).
- **stance**: **`contrast` + `background`. PROVISIONAL — the user's call, not settled here.**
  - *`contrast`, on rigour and on what an MSA-subsampling control can prove:* the paper's argument
    that a depth-matched random-subsampling arm is **not a valid control** for a clustering method
    because "the 'max_msa' random sampling that it relies on also performs clustering internally
    at the AF2 MSA processing step" (p8) is a direct constraint on how any of our own
    subsampling-vs-structured-MSA comparisons may be worded. Its TM-cutoff-by-inspection (p12) and
    its qualitative anti-memorization arm (p9) are contrast material on rigour.
  - *`background`:* as one side of a three-way exchange it is primarily context for the AF-Cluster
    dispute rather than a precedent our method builds on; the corpus holds all three documents so
    the exchange can be cited as a whole.
  - *Not `precedent`:* the paper introduces no method we would build on. *Not `threat`:* it does
    not pre-empt a claim of ours.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| KaiB variants whose single-sequence prediction matches the shallow-MSA prediction (**reproduced from ref [7]**, not new) | 71 | % of 487 variants | shallow (local-10) MSA prediction | p3 (Fig 1A) |
| KaiB variants predicted FS by shallow MSA that differ under single sequence (**reproduced from ref [7]**) | ~50 | % | shallow-MSA prediction | p3 (Fig 1A) |
| KaiB variants examined in that reproduced panel | 487 | variants | — | p3 |
| KaiB<sup>TV-4</sup>, local-10 MSA: convergence of all 5 AF2 models | ≤2 Å within 1 recycle | Å RMSD | NMR structure 8UBH | p4 (Fig 1B, D) |
| KaiB<sup>TV-4</sup>, single sequence: best model (model 5) | 2.28 Å at 7 recycles | Å RMSD | 8UBH | p4 (Fig 1C, D) |
| KaiB<sup>TV-4</sup>, single sequence: models giving wrong structures | 4 of 5 | models | 8UBH | p4 |
| Population of the KaiB<sup>RS</sup> "Enigma" state (**cited to ref [13]**, not measured here) | ~6 at 20 °C | % population | NMR | p4 |
| KaiB<sup>RS</sup> cluster, max pLDDT at original sampling (1 model, 1 seed) | 63.8 (at 3.0 Å) | pLDDT (Å RMSD) | reported by the comment from the AF-Cluster repo | p6, p7 (Fig 3) |
| KaiB<sup>RS</sup> cluster, max pLDDT at CF-Random's sampling budget (5 models × 5 seeds) | 70.8 (at 3.0 Å) | pLDDT (Å RMSD) | same cluster, matched budget | p6, p7 (Fig 3) |
| CF-Random model reported by the comment for KaiB<sup>RS</sup> | 73.9 (at 3.2 Å) | pLDDT (Å RMSD) | quoted from ref [6] | p7 (Fig 3) |
| Clusters across RfaH + Mad2 returning >50% of samples in one state under increased stochasticity | 13 | clusters | TM-score cutoffs 0.65 / 0.72 | p10 (Fig 5) |
| Of those, clusters degraded by column shuffling | 12 of 13 ("all but one") | clusters | TM-score to the state the original cluster predicted | p9, p10 (Fig 5) |
| RfaH breakdown printed on Figure 5 | 9/10 use coevolution; 1/10 single-site residue frequencies sufficient | clusters | as above | p10 (Fig 5, read from render) |
| Mad2 breakdown printed on Figure 5 | 3/3 use coevolution | clusters | as above | p10 (Fig 5, read from render) |
| The single exception | RfaH cluster 049 | — | the cluster the comment concentrated on | p9, p10 |
| MSA clusters entering the shuffling analysis | 49 (RfaH) + 32 (Mad2) = 81 | clusters | ≥10 sequences, or previously depicted in ref [7] | p12 |
| Sampling increase over the original paper | 20× | fold | ref [7]'s sampling | p10 (Fig 5 caption) |
| State-calling threshold, RfaH (C-terminal domain, both states) | 0.65 | TM-score | 5OND / 2LCL | p12 |
| State-calling threshold, Mad2 (open vs closed) | 0.72 | TM-score | 1S2H / 1DUJ | p12 |
| Aggregation rule for "returns a state" | >50 | % of samples | — | p9, p10 |
| Cluster-49 vs full-MSA pLDDT with matched masking and current parameters | cluster 49 higher in 4 of 5 AF2 models | AF2 models | full RfaH MSA | p15, p16 (Fig B3) |
| pLDDT range across AF2 parameter versions, RfaH (50 seeds × 5 models × 2 versions) | ~0.69–0.85 (old `model_X`); ~0.65–0.78 (`model_X_ptm`) | pLDDT (plotted as fraction) | — | p15 (Fig B2, read from render) |
| ProteinMPNN design temperature | 1.0 | — | — | p12 |
| Sequences designed per structure, before screening | 15 | sequences | — | p12 |
| Sequences removed by BLAST screen | 1 each for 2QKE:E, 5JYT:A, 5OND:A; 0 otherwise | sequences | PDB + SwissProt, 15 June 2025 | p12 |
| De novo sequences used as MSA input per fold | 14–15 | sequences | — | p9, p12 |
| Anti-memorization outcome | "AF2 was able to robustly predict the structures" | **no numeric value reported** | 5 experimental structures | p9, p21 (Fig D4) |
| MSA Transformer baseline construction | 5 clusters averaged, 100 bootstrap iterations | clusters / iterations | all RfaH clusters | p17, p18 (Fig C2) |
| Contact-map difference scale | −0.5 to +0.5 | contact probability difference | baseline across all clusters | p18 (Fig C2, read from render) |

  Values marked "read from render" appear only as printed labels or axis ticks in the figure
  images, not in the PDF text layer.

- **n_predictions**: **The paper never states a total, and it cannot be summed because two arms
  omit their counts. Recorded per arm; derived products are marked as derived.**
  - *Shuffling ablation (Figs 5, D1, D2 — the largest arm):* **per cluster, 15 predictions**
    (5 AF2 models × 3 seeds, with dropout), recorded at recycles 0–3 (p12). **Per condition,
    81 clusters × 15 = 1,215 predictions (derived); across original + shuffled, 2,430 (derived);
    up to 9,720 recorded structure snapshots if each of the 4 recycle points is counted
    (derived).** The paper's own statement of scale is relative: "20 times more sampling than in
    [7]" (p10).
  - *KaiB<sup>TV-4</sup> shuffling (Fig 4B):* original 5 models × 13 recycle points; shuffled
    **10 replicates** × 5 models × 13 recycle points = 650 snapshots (derived from p12).
  - *Figure 4C–E renders and scatters:* Figure 4A states **5 models, 4 seeds + dropout** = 20 per
    cluster — **which contradicts the 5 models × 3 seeds in the Methods for Figure 5** (p12). See
    `unresolved`.
  - *Single-sequence vs local-10 (Fig 1B–D):* 5 models × 13 recycle points × 2 inputs = 130
    snapshots for one protein (derived from p11).
  - *CF-Random decomposition (Fig 2D):* **33 random seeds** per setting × 2 settings = 66, one
    protein (p11).
  - *Sampling-matched pLDDT (Fig 3):* **5 seeds × 5 models × 3 recycles** per condition, 2
    conditions (p11) = 25 predictions per condition (derived).
  - *Parameter-version control (Fig B2):* **50 random seeds** × 5 parameter sets × 2 versions =
    500 RfaH structures (derived from p14).
  - *Masking control (Fig B3):* 5 AF2 models × 2 MSA conditions; **seed count NOT REPORTED**
    (p15–16).
  - *MSA Transformer (Fig C2):* all RfaH clusters, 5 models per cluster for the AF2 side (p17);
    baseline = 100 bootstrap draws of 5 clusters (p17).
  - *Anti-memorization (Fig D4):* 5 folds × 1 de novo MSA each; **number of ColabFold models per
    input NOT REPORTED**, only that the top-ranked by pLDDT is shown (p12).
  - *Targets:* 3 families / 81 MSA clusters / 5 deposited structures, per arm as in `n_targets`.
  - *Total:* **NOT REPORTED**, and not derivable — the B3 seed count and the D4 model count are
    missing.
- **comparable_to_ours**:

- **si_in_scope**: **Mostly IN SCOPE — an unusual and useful case.** This paper's four appendices
  (A–D) and its full designed-sequence table are *inside* the held PDF: Appendix A p13,
  Appendix B pp13–16 (Figs B1–B3), Appendix C pp16–18 (Figs C1–C2), Appendix D pp18–21
  (Figs D1–D4), Table 1 pp21–27. No separate supplementary file is referenced for this document's
  own results. **Not held:**
  - the two data/code repositories, https://github.com/HWaymentSteele/controls_04feb2024 and
    https://github.com/HWaymentSteele/AFCluster/coevolutionary_ablation_2025 (p12) — note the
    second URL is malformed relative to the repository named elsewhere as `AF_Cluster`;
  - the reproduction manifest https://github.com/HWaymentSteele/AF_Cluster/blob/main/
    complete_methods.md, which is where "exact commands to reproduce every model prediction in our
    original paper [7], as well as models presented here" now live (p11) — i.e. the *complete*
    methods for this paper are deliberately outside it;
  - the ColabDesign implementation notebook (p12);
  - all supplementary material of refs [5], [6] and [7] (e.g. "Supplemental Figure 1 of [6]", p9;
    "Extended Data Fig. 3 in [7]", p8; "Extended data Figure 6 in [7]", p11), which belong to the
    other two documents and are not imported here.
  - A dangling internal pointer: the text twice says "see Appendix 1" (p13, p14) where the figures
    referred to are **Appendix B**'s Figures B1–B3; there is no "Appendix 1" in the document.

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 3 | Reproduced from ref [7]: how the shallow-MSA state call of 487 KaiB variants changes when the MSA is replaced by the single query sequence | bar | `PLOT \| facet: none (1) \| vary: state from shallow MSA (3: FS, Ground, Other) \| series: single-sequence prediction (3: FS, Ground, Other) \| measure: number of KaiB variants \| mark: bar (stacked) \| n: 487 variants across 3 stacked bars; per-bar n not printed` | 1 panel, 3 stacked bars, 3 colour segments each | **Stacked bar with no printed n or percentage**: the load-bearing "roughly only 50% are predicted in the FS state using single sequences" (caption, p3) must be eyeballed as a segment ratio. No uncertainty shown | CC-BY 4.0 (p1 and every page header). **No ND clause; redrawing permitted for this document.** **But this panel is reproduced from ref [7] (*Nature* 2024)** — the preprint's CC-BY does not relicense a panel originating in a subscription journal. Check the source before redrawing |
| 1B-C | 3 | RMSD to the authors' NMR structure as a function of recycle count, for all 5 AF2 models, with a 10-sequence MSA vs a single sequence | line | `PLOT \| facet: MSA input (2: local 10 sequences, single sequence) \| vary: number of recycles, 0–12 (continuous, integer-valued) \| series: AF2 model (5: 1–5) \| measure: RMSD to 8UBH (Å) \| mark: line \| n: 1 trajectory per line, 5 lines per panel` | 2 panels differing by input; shared y-axis 0–10 Å | A black leader line from panel C to the boxed Model-3 render crosses the plotting area and obscures the model-3 and model-4 traces between recycles 4 and 7 | as above (this panel is new work, not reproduced) |
| 1D-E | 3 | The five models from each input overlaid on the NMR structure, coloured by pLDDT, plus the single structure the opposing preprint had picked, re-oriented | structure render | `RENDER \| facet: MSA input (2: local 10, single sequence) × AF2 model (5) \| views: 1 (one orientation, shared) \| overlay: 1 prediction per panel on 0 references shown separately (8UBH shown once, in grey, at left; E shows 1 picked model from ref [2]) \| axis: none` | 11 renders: 1 reference (8UBH), 10 predictions in a 2 × 5 grid, plus panel E's single re-oriented structure from ref [2]. Model 3 of the single-sequence row is boxed as the highest-pLDDT (and wrong) pick | **The displayed recycle is chosen by the oracle**: "Models were selected at the recycle at which any model from single-sequence mode obtains the lowest RMSD to our solved NMR structure" (caption, p4) — the frame most favourable to the arm being criticised, but reference-selected all the same. **No RMSD number is printed on any panel**, so the visual comparison carries the argument | as above; panel E reproduces a figure from ref [2] (a bioRxiv preprint) |
| 2A,2C-D | 5 | The KaiB prediction landscape in the plane of RMSD to both deposited states, for AF-Cluster clustered sampling (A, from ref [7]), CF-Random as published (C, from ref [5]), and CF-Random decomposed into its two settings (D, new) | scatter | `PLOT \| facet: sampling method (4: AF-Cluster clustered sampling; CF-random as published; CF-random default ColabFold; CF-random max_msa=1) \| vary: RMSD to ground state, 0–15 Å (continuous) \| series: pLDDT, 50–90 (continuous colour scale) \| measure: RMSD to FS state (Å) \| mark: point \| n: 1 per mark; 33 seeds per panel in D; per-panel n NOT REPORTED for A and C` | 4 scatter panels across three sources. Panel A additionally carries **two structure-render insets** (the two KaiB states, connected to the point cloud by leader lines) — described here rather than split into a row, since they are insets without their own panel letters | **The three panels the argument compares are on different axis ranges** — A runs 0–15 Å on both axes, C runs 0–12, D runs 0–10 — so the eye cannot compare cloud positions across the comparison the figure exists to make. **pLDDT colour scale clipped at 50 and 90** on a 0–100 metric, hiding the tails. Panel C is a reduced-size reproduction whose own axis labels are near-illegible at print size | CC-BY 4.0 for this document (p1). **Panel A is reproduced from ref [7] (*Nature*) and panel C from ref [5] (bioRxiv)** — third-party panels the preprint's licence does not cover. Panel D is new |
| 2B | 5 | Reproduced from ref [7]: the KaiB phylogeny with each leaf annotated by AF2's predicted state, and again by prediction confidence | tree | `TREE \| leaves: NOT REPORTED (the family analysed in ref [7] contains 487 variants, p3) \| annotation: predicted state (2: ground state, FS state) in the left tree; pLDDT (continuous, 50–90) in the right tree \| layout: radial` | 2 radial dendrograms differing only in leaf annotation, so one row; four sequence regions are marked i.–iv. on both | Leaf count never stated; the two trees are drawn at a size where individual leaves are unresolvable, so the "clusters across the family" claim (p5) rests on colour texture rather than countable leaves | as above; **reproduced from ref [7] (*Nature*)** |
| 3 | 7 | pLDDT of the KaiB<sup>RS</sup> models at issue, showing that the comment compared a max-of-many model against a single AF-Cluster model | box + point | `PLOT \| facet: none (1) \| vary: sampling condition (4: comment's AF-Cluster model from the KaiB-RS cluster; comment's CF-Random model; KaiB-RS cluster resampled at CF-Random's budget; CF-Random repeated) \| series: none \| measure: pLDDT \| mark: point for conditions 1–2, box + overlaid points for conditions 3–4 \| n: 1 for each of the first two conditions; 25 (5 models × 5 seeds) per box` | 1 panel, 4 x-positions, plus a structure-render inset (KaiB<sup>RS</sup> prediction on experiment) and a text block carrying the three RMSD/pLDDT pairs | **n = 1 points plotted on the same axis as n = 25 distributions**, which is the very asymmetry the figure is criticising — the figure reproduces the defect in order to name it, and does not mark the single points as n = 1 in the axis labels. **The y-axis is truncated to ~53–75 pLDDT**, expanding differences of a few pLDDT units to the full panel height | CC-BY 4.0 (p1); new work |
| 4A | 10 | The column-shuffling ablation scheme: query row preserved, each column permuted, both MSAs to AF2 | schematic | `SCHEMATIC \| MSA cluster vs column-shuffled MSA fed to AF2 under 5 models, 4 seeds and dropout, asking whether evolutionary couplings survive \| no data` | 1 schematic, 2 branches (Original, Shuffle MSA) | — | CC-BY 4.0 (p1); new work |
| 4B | 10 | RMSD to the NMR structure vs recycle for the KaiB<sup>TV-4</sup> cluster and its shuffled counterpart | line | `PLOT \| facet: MSA treatment (2: MSA cluster, shuffled) \| vary: number of recycles, 0–12 (continuous, integer-valued) \| series: AF2 model (5: 1–5) \| measure: RMSD to 8UBH (Å) \| mark: line \| n: 5 trajectories in the original panel; 50 in the shuffled panel (5 models × 10 shuffle replicates)` | 2 panels differing by treatment, shared 0–10 Å y-axis | **The two panels carry 5 and 50 lines respectively with no per-panel n stated in the caption**, so the shuffled panel looks noisier partly because it is ten times more densely drawn. The replicate count is recoverable only from the Methods command line on p12 | CC-BY 4.0 (p1); new work |
| 4C | 10 | Every sampled model from two RfaH clusters, before and after shuffling, superimposed | structure render | `RENDER \| facet: cluster (2: RfaH cluster 000 autoinhibited, cluster 001 active) × treatment (2: original, shuffled) \| views: 1 \| overlay: 20 predictions per panel (5 models × 4 seeds with dropout, per the Fig 4A scheme) on 0 references \| axis: none` | 4 render panels | **A qualitative claim with no quantitative panel of its own**: "after shuffling no meaningful structures are obtained" (caption, p10) is a visual judgement; the quantitative version of this comparison lives in D–E and is restricted to the same 2 of 49 clusters. The overlay count is not stated in the caption and must be inferred from the panel-A scheme | CC-BY 4.0 (p1); new work |
| 4D-E | 10 | The same comparison in the plane of TM-score to both deposited states, for two RfaH and two Mad2 clusters, original vs shuffled, over a grey background of all cluster samples | scatter | `PLOT \| facet: system × cluster × treatment (8: RfaH clusters 000/001 and Mad2 clusters 000/020, each original and shuffled) \| vary: TM-score to state 1 (RfaH 5OND autoinhibited; Mad2 1S2H closed), 0–1 (continuous) \| series: pLDDT, 50–90 (continuous colour) plus a grey "all AF-Cluster samples" background layer \| measure: TM-score to state 2 (RfaH 2LCL active; Mad2 1DUJ open) \| mark: point \| n: ~20 coloured points per panel; grey background n NOT REPORTED` | 8 panels in two rows (D: RfaH, E: Mad2), varying by cluster and treatment | **2 of 49 RfaH and 2 of 32 Mad2 clusters are shown**, chosen as clusters that had already predicted a known state (p9); the other 77 are relegated to Figs D1–D2 at unreadable size. **The grey background layer's n is never given** anywhere in the paper, and it is the denominator that makes the coloured points look localised | CC-BY 4.0 (p1); new work |
| 5 | 10 | The headline result: per-cluster TM-score to the state the unshuffled cluster predicted, original vs shuffled, across recycles, for the 13 clusters that return one state in >50% of samples | box + point | `PLOT \| facet: cluster (13: RfaH autoinhibited 000/014/021/049/056/093, RfaH active 001/005/015/024, Mad2 closed 000/046, Mad2 open 042) \| vary: recycle (4: 0, 1, 2, 3) \| series: MSA treatment (2: original, shuffle MSA) \| measure: TM-score to the state predicted by the original MSA cluster \| mark: box with overlaid points \| n: 15 per box (5 AF2 models × 3 seeds, with dropout); 8 boxes per panel` | 13 panels in two blocks, varying by system, state and cluster; cluster 049 is outlined as "Main cluster investigated by Schafer et al."; a legend block prints the summary counts (RfaH 9/10 and 1/10; Mad2 3/3) | **13 of 81 clusters are plotted, selected by having already returned one state in >50% of samples** — the 68 clusters that did not meet that criterion are absent, so the "all but one suffered" headline is conditional on a selection made after the sampling. The selection is inspectable only via Figs D1–D3. The legend counts (9/10, 1/10, 3/3) do not sum to 13 in an obvious way without reading the panel titles | CC-BY 4.0 (p1); new work |
| A1-A | 13 | The two BCCIP isoforms, with the alternatively spliced region highlighted | structure render | `RENDER \| facet: isoform (2: BCCIP-alpha 8EXE:B, BCCIP-beta 7KYS:A) \| views: 1 \| overlay: 0 predictions on 1 experimental structure each \| axis: none` | 2 panels | — | CC-BY 4.0 (p1); new work |
| A1-B | 13 | ColabFold sequence-coverage maps for both isoforms, showing the spliced region has essentially no alignment depth | heatmap | `MATRIX \| rows: aligned sequences, ordered by identity (~2,500 for alpha, ~2,100 for beta) \| cols: residue position (0–~310) \| value: sequence identity to query (0–1) \| facet: isoform (2)` | 2 panels; each carries an overlaid black line (per-position coverage count) on the same axes, i.e. a PLOT element inside a MATRIX panel — noted here rather than split, since the line is an annotation of the same matrix | The overlaid coverage line has no axis of its own, so its values cannot be read; the argument ("Sequence coverage of the alternatively spliced sequence in BCCIP-alpha is minimal", caption p13) rests on the visual sparsity of the right-hand region rather than a printed depth | CC-BY 4.0 (p1); new work |
| B1 | 14 | DeepMind AlphaFold and ColabFold outputs on the same MSA and settings, superimposed | structure render | `RENDER \| facet: none (1) \| views: 1 \| overlay: 2 predictions (AlphaFold notebook, ColabFold) on 0 references \| axis: none` | 1 panel, 2 superimposed models | Identity is asserted visually — "The outputs are identical and superimpose, without need to align" (caption, p14) — with **no RMSD or pLDDT number**, and the protein is unnamed ("a random protein with low MSA coverage", p14), so the check cannot be repeated | CC-BY 4.0 (p1); new work |
| B2 | 15 | pLDDT of RfaH structures across the five AF2 parameter sets, for the older and current parameter versions | box + point | `PLOT \| facet: none (1) \| vary: AF2 model number (5: 1–5) \| series: parameter version (2: model_X older, used in ref [5]; model_X_ptm current, used in ref [7]) \| measure: pLDDT (plotted as a fraction, ~0.65–0.85) \| mark: box with overlaid points \| n: 50 random seeds per box` | 1 panel, 10 boxes | y-axis truncated to ~0.645–0.855, which magnifies a ~0.05 pLDDT-fraction difference into most of the panel height. Seed count is in the Methods (p14), not the caption | CC-BY 4.0 (p1); new work |
| B3 | 16 | pLDDT of RfaH from MSA cluster 49 vs the full MSA, with masking and parameter version matched, across the five AF2 models | box + point | `PLOT \| facet: none (1) \| vary: AF2 model number (5: 1–5) \| series: MSA input (2: full MSA + mask, cluster 49 + mask) \| measure: pLDDT (fraction, ~0.57–0.82) \| mark: box with overlaid points \| n: NOT REPORTED per box (visibly unequal between the two series — the orange full-MSA boxes carry far fewer points than the green cluster-49 boxes)` | 1 panel, 10 boxes | **Unequal and unstated n between the two compared series**, which is the same sampling-asymmetry objection this paper raises against the comment. y-axis truncated to ~0.57–0.82 | CC-BY 4.0 (p1); new work |
| C1A-B,E-F | 17 | Binary contact maps of the two RfaH experimental structures (A, B) and of the AF-Cluster models from clusters 49 and 24 (E, F), with the disputed region boxed | heatmap | `MATRIX \| rows: residue index (0–160) \| cols: residue index (0–160) \| value: contact present/absent (binary) \| facet: source (4: 5OND autoinhibited, 6C6S active, AF-Cluster model from cluster 49, AF-Cluster model from cluster 24)` | 4 matrix panels | Panel A carries **grey bands marking residues unresolved in 5OND** — which is the paper's actual argument (p16), and is correctly annotated; noted here as a *good* practice, not a defect. No contact-definition distance cutoff is stated anywhere for these maps | CC-BY 4.0 (p1); new work |
| C1C-D | 17 | MSA Transformer contact predictions from RfaH clusters 49 and 24, with the contacts the comment called state-unique arrowed | heatmap | `MATRIX \| rows: residue index (0–160) \| cols: residue index (0–160) \| value: MSA Transformer contact probability (greyscale, scale unlabelled) \| facet: MSA cluster (2: cluster 49, cluster 24)` | 2 matrix panels, each with 3 coloured boxes (red, green, blue) marking the disputed regions and a single arrow | **No colourbar and no numeric scale** on either panel, so "weak contacts" (the disputed phrase, p16) cannot be quantified from the figure; the rebuttal is made by pointing at boxes | CC-BY 4.0 (p1); new work |
| C1G-H | 17 | The AF-Cluster models of the two RfaH states with the boxed contact regions rendered as secondary-structure elements | structure render | `RENDER \| facet: state (2: autoinhibited from cluster 49, active from cluster 24) \| views: 1 \| overlay: 1 AF-Cluster model per panel on 0 references \| axis: none` | 2 renders on black backgrounds, colour-keyed (red/green/blue) to the boxes in the matrix panels | — | CC-BY 4.0 (p1); new work |
| C2A | 18 | Contacts in the two RfaH experimental structures, with the state-unique regions boxed and the unresolved region left white | heatmap | `MATRIX \| rows: residue index (0–160) \| cols: residue index (0–160) \| value: contact present/absent (binary) \| facet: state (2: 5ONDA autoinhibited, 6C6SD active)` | 2 matrix panels | White = unresolved is stated in the caption but is visually identical to white = no contact, so absence of data and absence of contact are indistinguishable within a panel | CC-BY 4.0 (p1); new work |
| C2B | 18 | The systematic version of the coupling argument: mean MSA Transformer contacts over all clusters that predicted each state, minus a bootstrap baseline | heatmap | `MATRIX \| rows: residue index (0–160) \| cols: residue index (0–160) \| value: contact probability difference from baseline (−0.5 to +0.5, diverging red–blue) \| facet: predicted state (2: autoinhibited clusters − baseline, active clusters − baseline)` | 2 matrix panels, each with the state-unique regions boxed | **No n on either panel**: the number of clusters averaged into each state group is never stated (only that the baseline is 5 clusters × 100 bootstrap draws, p17). This is the panel that carries the paper's systematic coevolution claim, and its group sizes are missing | CC-BY 4.0 (p1); new work |
| C2C | 18 | The unsubtracted inputs to C2B: mean raw MSA Transformer output per state group, and the baseline | heatmap | `MATRIX \| rows: residue index (0–160) \| cols: residue index (0–160) \| value: mean MSA Transformer contact probability (sequential blue, scale unlabelled) \| facet: group (3: clusters predicting autoinhibited, clusters predicting active, bootstrap baseline)` | 3 matrix panels | No colourbar for the raw panels (the ±0.5 bar belongs to C2B), so the three raw maps cannot be compared numerically | CC-BY 4.0 (p1); new work |
| D1 | 19 | Every RfaH cluster, original and shuffled, in the TM-score plane | scatter | `PLOT \| facet: RfaH MSA cluster (49) × treatment (2: original, shuffled) = 98 \| vary: TM-score to 5OND autoinhibited, 0–0.75 (continuous) \| series: pLDDT, 50–90 (continuous colour) plus a grey all-samples background layer \| measure: TM-score to 2LCL active \| mark: point \| n: ~15 coloured points per panel; grey background n NOT REPORTED` | 98 panels, 10 per row (last row 8); panel titles are the cluster id and "<id> shuffled" | At 98 panels on one page each panel is ~2 cm wide with 4 axis ticks; the individual clusters are not readable as data, only as texture. No summary statistic accompanies the grid — the quantitative summary is Fig D3 | CC-BY 4.0 (p1); new work |
| D2 | 20 | Every Mad2 cluster, original and shuffled, in the TM-score plane | scatter | `PLOT \| facet: Mad2 MSA cluster (32) × treatment (2: original, shuffled) = 64 \| vary: TM-score to 1S2H closed, 0.2–0.8 (continuous) \| series: pLDDT, 50–90 (continuous colour) plus a grey all-samples background layer \| measure: TM-score to 1DUJ open \| mark: point \| n: ~15 coloured points per panel; grey background n NOT REPORTED` | 64 panels, 8 per row × 8 rows | as D1: unreadable at printed size; grey-layer n unstated | CC-BY 4.0 (p1); new work |
| D3 | 20 | The threshold sweep: how many clusters return a given state at each "fraction of samples" cutoff, original vs shuffled | bar | `PLOT \| facet: system × state (4: RfaH autoinhibited, RfaH active, Mad2 closed, Mad2 open) \| vary: fraction of total samples, 0.1–1.0 (continuous, binned) \| series: MSA treatment (2: original, shuffle MSA) \| measure: number of MSA clusters \| mark: bar \| n: 49 RfaH clusters and 32 Mad2 clusters behind the respective panels` | 4 panels, shared 0–10 y-axis | Bars only, no distribution or interval; the shuffled series is absent from two panels (Mad2 closed shows no orange bars at all), which reads as zero but is not labelled as such | CC-BY 4.0 (p1); new work |
| D4A | 21 | The de novo design workflow used to test the memorization hypothesis | schematic | `SCHEMATIC \| experimental structure → ProteinMPNN (T=1.0) → 15 sequences → BLAST removal of SwissProt hits → 14–15 sequences used as the MSA input to AF2 \| no data` | 1 flow diagram, 5 steps | — | CC-BY 4.0 (p1); new work |
| D4B | 21 | The anti-memorization result: the top-pLDDT ColabFold model from each de novo sequence set, on its experimental structure | structure render | `RENDER \| facet: system × state (6: KaiB ground 2QKE, KaiB fold-switched 5JYT, RfaH autoinhibited 5OND, RfaH active 6C6S, Mad2 closed 1S2H, Mad2 open 1DUJ) \| views: 1 \| overlay: 1 prediction (coloured by pLDDT 50–90) on 1 experimental reference (grey) \| axis: none` | 6 render panels in one row | **The paper's entire answer to the memorization hypothesis, with no quantitative panel at all**: no RMSD, no TM-score, no pLDDT value, no distribution, and 1 of an unstated number of models shown per fold ("top-ranked ... by pLDDT", p12). The TM-score predicates built for the rest of the paper are not applied here. This is the clearest instance in the document of a claimed result with no quantitative panel | CC-BY 4.0 (p1); new work |

  **27 panel-group rows across 5 main figures and 9 appendix figures.** Rows were split on `mark`
  or `value`/`measure` and never on `facet` alone: hence 2A, 2C and 2D are one row (identical
  scatter shape, differing only in method facet), C1's binary contact maps are split from its
  probability maps, and C2's three panels are split because A is binary contacts, B is a signed
  difference and C is a mean probability. Structure insets without their own panel letters
  (Fig 2A, Fig 3) are described inside the `panels` cell of the row they belong to rather than
  given rows of their own.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5)
- **schema_version**: v3
- **confidence**: **medium-high.**
  - *High* on the argumentative content, the Methods and all of sections C and D: the paper's
    prose is unambiguous and every claim above is quoted directly from the text layer.
  - *High* on the shuffling analysis parameters (49 + 32 clusters, 5 models, 3 seeds, dropout,
    3 recycles, TM cutoffs 0.65 / 0.72), which are stated explicitly on p12.
  - *Medium* on figure-panel counts and on values that exist only as printed labels or axis ticks
    — the Fig 5 legend counts (RfaH 9/10 and 1/10, Mad2 3/3), the Fig 3 pLDDT axis range, the
    Fig B2/B3 pLDDT ranges, and the Fig C2B ±0.5 scale. These were read from 100–110 dpi renders
    of pp3, 5, 7, 9, 10, 13, 15, 16, 17, 18, 19, 20 and 21 (13 pages rendered). A reader putting
    any of these in a manuscript table should confirm against the source figure.
  - *Medium* on identity, because the held PDF (bioRxiv, July 2025) and the corpus records
    (*JMB*, DOI 10.1016/j.jmb.2025.169376) describe different objects.
  - *Low* on nothing.
  - What was hard: Fig 2's panel provenance (three of its four panels are reproductions from two
    different papers, and the caption states this only in passing); Fig 4C's overlay count, which
    must be inferred from the panel-A schematic rather than the caption; and the D1 panel count,
    which had to be counted off a render (98 = 49 × 2, consistent with p12).
- **unresolved**:
  1. **VENUE SPLIT — flag this for any future citation.** The held PDF is a bioRxiv preprint
     (10.1101/2024.07.29.605333, posted 15 July 2025). `refs.bib` and `MANIFEST.csv` record
     *Journal of Molecular Biology* (10.1016/j.jmb.2025.169376). **The Matters Arising being
     answered was published in *Nature* (638(8051):E8–E12, p27), and the original AF-Cluster paper
     was also *Nature*.** So this is *not* a Nature comment/reply pair: the reply ran in a
     different journal. The paper's own explanation is on p8 — "we were not given a chance to see
     the final version of the Matters Arising or submit of a final response." **Never describe
     this document as a *Nature* reply.** Whether the JMB version differs in content from this
     preprint is not determinable here.
  2. **RETITLING ACROSS PREPRINT VERSIONS — not resolvable from this PDF.** The held version is
     titled "Does sequence clustering confound AlphaFold2?", matching the JMB title in `refs.bib`.
     The bioRxiv accession is `2024.07.29.605333` (a July 2024 accession) while this version was
     posted July 2025, so at least one earlier version exists — but **the PDF carries no version
     history and no former title.** Do not assert a previous title from this note; resolve it
     against the bioRxiv version history if the corpus needs it.
  3. **Seed-count contradiction.** The Figure 4A schematic states "5 models, 4 seeds + dropout"
     (p10), while the Methods for Figure 5 state "we ran these in all 5 models, with dropout, for
     3 different seeds, and for 3 recycles" (p12). Whether Figs 4C–E used 4 seeds and Fig 5 used
     3, or one is a typo, is not stated. All derived prediction counts above are marked as
     derived for this reason.
  4. **Templates are never mentioned** anywhere in the paper (see `templates`). This blocks the
     `no-template-no-msa` tag for the single-sequence arms, which otherwise fit it.
  5. **Grey "all cluster samples" background layer** in Figs 4D–E, D1 and D2 has no n anywhere in
     the paper, yet it is the denominator against which the coloured points look localised.
  6. **Dangling pointer**: "see Appendix 1" (p13, p14) has no referent; the figures meant are
     Appendix B's B1–B3.
  7. **Typo in a figure cross-reference**: "To generate the data in Figure 1c [6],d of this
     preprint" (p11) appears to mean Figure 1c,d of this preprint, with the "[6]" misplaced.
  8. **Malformed data URL**: `https://github.com/HWaymentSteele/AFCluster/coevolutionary_
     ablation_2025` (p12) is missing the underscore used in the repository named elsewhere as
     `AF_Cluster`; neither repository is held by the corpus.
  9. **Figure B3's per-box n is not stated** and is visibly unequal between the two compared
     series (see the `hides` cell on row B3).
  10. **TAGS I NEEDED AND COULD NOT USE — not invented, recorded here as v3 requests:**
      - **A tag for MSA column shuffling / coevolution ablation.** This is the paper's central new
        method and the corpus has no vocabulary for it: `msa-subsample` is wrong (depth is
        unchanged), `msa-state-filter` is wrong (no state-specific alignment is substituted), and
        `benchmark-only` describes the paper's genre, not the intervention. Suggested:
        `msa-shuffle` or `coevolution-ablation`. Without it, a reverse lookup for "who ablated
        coevolution directly" returns nothing.
      - **A tag for rebuttal / comment-reply documents.** Three documents in this corpus
        (`waymentsteele2024cluster`, `schafer2025confounds`, this) form one exchange, and there is
        no way to mark the exchange or to mark a document as one side of it. Suggested:
        `rebuttal` or `comment-reply`. `background` and `contrast` are stance tags and do not
        carry this.
      - **A control-handle tag for cluster identity.** Under **Control**, the paper's only
        directional handle is *which MSA cluster is used*, and none of `directed-state`,
        `partner-driven`, `ligand-driven`, `peptide-driven`, `g-protein-mimetic`, `nanobody`,
        `apo-sampling` or `seed-only` fits. Suggested: `cluster-driven`.
      - **A tag for de-novo / designed-sequence input.** The ProteinMPNN anti-memorization arm
        feeds AF2 sequences that exist nowhere in nature; `anti-memorization` covers the intent
        but nothing covers the input regime.
  11. **Publication tag is dual and only one was applied.** `preprint` is tagged on the evidence of
      this PDF; the corpus's own records say this text also exists as a peer-reviewed JMB article,
      which would warrant `peer-reviewed`. Following the `schafer2025confounds` precedent, only
      the tag supported by the held document is applied. Whoever reconciles item 1 should
      re-tag.
- **why_it_matters**:

## Tags

`fold-switching` `general-protein` `af-cluster` `msa-subsample` `benchmark-only` `two-state`
`ensemble` `continuous-metric` `binary-predicate` `visual-metric` `oracle-leak`
`design-level-oracle` `anti-memorization` `unpowered` `preprint` `contrast` `background`

Justification for the less obvious ones:
- `general-protein` **and** `fold-switching`: the three families are soluble globular proteins with
  no organ-system tag that fits, and metamorphic behaviour is the property under study.
- `af-cluster`: the method under defence, and the paper is its authors'.
- `msa-subsample`: shallow local-10 MSAs, single-sequence mode and `max_msa:extra_msa=1:2` are all
  run here (pp4, 6, 11) — as reproduced comparator arms rather than as this paper's method, but
  they are run.
- `benchmark-only`: the paper introduces no new predictive method; every new calculation is a
  control, an ablation or a re-run.
- `two-state` + `ensemble`: two deposited references per family define the state calls; the new
  protocol reads distributions rather than single models.
- `visual-metric`: the TM-score cutoffs were set "based on inspecting resulting models" (p12) and
  Fig 4C's conclusion ("no meaningful structures are obtained", p10) has no operationalised
  predicate.
- `oracle-leak`: routes 3 (analysis-level), 4, 5 and 6 are present — see `oracle_leakage`.
- `design-level-oracle`: route 7 — the system set, the declared expected direction, and the
  exclusion of BCCIP and SA1 by prior expectation (p4).
- `anti-memorization` + `unpowered`: the ProteinMPNN de novo arm exists and was run, on 5 folds,
  with no metric reported.
- **Not applied and why:** `multi-backbone` (only AF2, in two implementations and two parameter
  versions); `no-template-no-msa` (single-sequence arms exist but templates are never stated —
  `unresolved` item 4); `experimental-validation` (the NMR validation belongs to ref [7]; no new
  experiment here); `rmsd-only` (TM-score and binary predicates are also used); `saturating-metric`
  (no numeric floor or ceiling — see `metric_saturation`); `precedent` and `threat` (no method we
  build on, no claim of ours pre-empted); `comparator-numbers` (the numbers are internal to the
  dispute rather than reusable benchmarks); all Site and Control tags (none applicable — see
  `unresolved` item 10).
