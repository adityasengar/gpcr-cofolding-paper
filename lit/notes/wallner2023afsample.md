# wallner2023afsample

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**This is a 3-page Bioinformatics Applications Note. It is sparse by design and this note
is correspondingly short.** Many section C fields are genuinely absent because the paper
does not attempt conformational-state work at all. Nothing here is imported from the
later AFsample2 / AFsample3 papers held in this corpus, and nothing is inferred from
them.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–3), which equal the
printed page numbers (PDF p1 prints "1", the journal pagination is btad573).**

**SI is NOT held.** Supplementary Table S1 — the table that actually enumerates the six
sampling settings — is referenced on p2 and is not in the PDF. See `si_in_scope`.

**Text-layer note:** the text layer is clean except that `pdftotext` drops the multiplier
glyph "×" (p3 reads "it generates 240 models" and "the overall timing is 1000 more
costly"). A 150 dpi render of p3 confirms the true text is **"it generates 240× models"**
and **"the overall timing is ∼1000× more costly"**. Figure axis labels, panel marks and
the ~60 group tick labels in Fig 1a are not in the text layer and were read from a
150 dpi render of p2 (both renders deleted afterwards).

---

## A. Identity

- **citekey**: `wallner2023afsample`
- **doi**: **10.1093/bioinformatics/btad573** — p1 masthead: "https://doi.org/10.1093/
  bioinformatics/btad573". Matches `refs.bib`.
- **year**: **2023.** p1: "Advance Access Publication Date: 15 September 2023".
- **venue**: **Bioinformatics 39(9), btad573 — Applications Note, Structural
  bioinformatics section. Peer-reviewed, not a preprint.** p1 masthead: "Bioinformatics,
  2023, 39(9), btad573 ... Applications Note"; p1 footer: "Received: 13 March 2023;
  Revised: 29 May 2023; Editorial Decision: 8 September 2023; Accepted: 14 September
  2023"; "Associate Editor: Janet Kelso" (p1). Tagged `peer-reviewed`, not `preprint`.
- **title**: "AFsample: improving multimer prediction with AlphaFold using massive
  sampling" — p1.
- **authors**: **Björn Wallner, sole author.** Division of Bioinformatics, Department of
  Physics, Chemistry and Biology, Linköping University, Sweden (p1). Corresponding:
  bjorn.wallner@liu.se. Note that the two most load-bearing methodological antecedents
  (Johansson-Åkhe and Wallner 2022, on selective dropout and recycle tuning; Basu and
  Wallner 2016, the DockQ metric the whole result is scored in) are the author's own.

## B. Scope

- **system**: **general protein — protein assemblies (multimers) from CASP15.** No
  protein family is targeted. The two worked examples are a nanobody–antigen complex
  (H1144, p3: "Target H1144 is a nanobody interaction") and a homodimer (T1187o, p3:
  "Target T1187o is a dimer of the Uniprot ID Q94EW1"). No GPCR, kinase or transporter
  work appears anywhere.
- **n_targets**: **NOT REPORTED.** The benchmark is "common CASP15 multimer targets"
  (p2 Fig 1 caption, p2 Methods) but the number of common multimeric targets is never
  stated in the text or on any panel. Fig 1b (p2) plots one labelled point per target;
  ~39 labelled points are legible at 150 dpi, which is an eyeball count and not a paper
  statement. Two targets (H1144, T1187o) are shown individually. Recorded as NOT
  REPORTED rather than guessed.
- **method_class**: **other — inference-time dropout plus massive sampling.** Not any of
  the MSA classes and not template biasing. Concretely, six settings, all using dropout,
  differing in (i) dropout placement (full network vs Evoformer-only "selective
  dropout"), (ii) multimer weight version (v1 or v2), (iii) recycle count, (iv) templates
  on or off; ~1000 models per setting, 6000 per target; rank-1 chosen by
  `ranking_confidence`. p1 abstract, p2, p3.
  The closest v3 list entry is "enhanced sampling", which is the tag applied, but note
  it means *inference-time stochastic sampling of a fixed network*, not MD enhanced
  sampling.
- **backbones**: **AlphaFold2 / AlphaFold-Multimer only. Both the v1 and v2 multimer
  weight sets are used inside AFsample** — p1: "with v1 and v2 multimer network models";
  p2: "Both v1 and v2 of the multimer neural network weights and increased number of
  recycles were also utilized to increase the diversity further." AlphaFold-Multimer v3
  is added to the released code and run post hoc on the two showcase targets only (p3).
  **This is one architecture with three weight versions, not multiple backbones**;
  `multi-backbone` is deliberately NOT tagged (see Tag notes).
- **templates**: **BOTH, within the same 6000-model pool.** p1 abstract: "with v1 and v2
  multimer network models, **with and without templates**, and increased the number of
  recycles within the network." Templates come from "PDB from 2 May 2022" (p2), i.e. the
  same PDB snapshot as the baseline, and p2 states AFsample and the baseline "were run
  with exactly the same MSAs and templates." **Which of the six settings had templates on
  and which off is only in Supplementary Table S1, which is not held.**
- **msa_handling**: **full — and, critically, untouched.** p2 Methods: "AFsample
  (Wallner) and AlphaFold-Multimer baseline (NBIS-AF2-multimer) were run with exactly the
  same MSAs and templates. The alignments were created with the large database setting:
  --db_preset=full_dbs using the AlphaFold-Multimer baseline server (NBIS-AF2-multimer).
  They were made available by the CASP organizers". Reinforced on p3: "It is clear the
  sole reason for the improved performance of AFsample is improved sampling as AFsample
  was using identical MSAs as the AlphaFold-Multimer v2 baseline."
  **There is no MSA manipulation of any kind in this method — no subsampling, no column
  masking, no clustering, no state filtering, no depth reduction.** The author explicitly
  names MSA perturbation as *a different option that he did not take*, p1: "Another
  option is to randomly perturb or alter the input multiple sequence alignment (MSA),
  which has been shown to enable better sampling of the conformational landscape and
  prediction of multiple conformational states (Wayment-Steele et al. 2022). **An
  alternative way** to achieve more diversity among the generated models is to enable the
  dropout layers in the neural network". This sentence is the cleanest statement in the
  corpus of the dropout-vs-MSA-manipulation fork, and it is why this paper must not be
  filed with the MSA-masking methods that cite it.

## C. Conformational core

**Framing caveat that governs this whole section: the paper's stated target is multimer
prediction *quality* (DockQ), not conformational states.** No state is defined, no state
predicate exists, no alternative-conformation experiment is run, and no target is chosen
for having two deposited states. Alternative conformations appear only in passing — see
`states_generated` and `central_conclusion`. Fields below are answered against what the
paper actually did, and are `NOT APPLICABLE` / `NOT REPORTED` where a conformational
reading would have to be imposed.

- **states_generated**: **ensemble + single-state, in the model-quality sense, and
  NOT APPLICABLE in the conformational-state sense.**
  - *Ensemble*: 6000 models per target are generated (p1, p3: "For each setting, on the
    order of 1000 models were generated per setting for a total of 6000 models per
    target"), and Fig 1c/1e (p2) show the full 6000-point cloud for two targets.
  - *Single-state*: the deliverable is one rank-1 model per target, selected by
    `ranking_confidence` (p2), and every headline number is a rank-1 average DockQ
    ("The rank 1 models from each method were used to calculate the average DockQ", p2).
  - **The ensemble is never characterised as containing distinct conformational states.**
    Alternate conformations are mentioned exactly once as a hoped-for use, p1 abstract
    final sentence: "the method should be useful for anyone interested in modeling
    multimeric structures, **alternate conformations**, or flexible structures" — a
    forward-looking statement with no supporting experiment. The only other adjacent
    sentence is p3: "Dynamics, flexibility, or simply the sheer complexity of large
    molecular assemblies will all require more sampling." Neither is a result.
- **structural_priors_used**: **Two, both benign and both explicitly declared.**
  1. **PDB templates (snapshot 2 May 2022)** are available to some of the six settings
     (p1 abstract "with and without templates"; p2 database list "PDB from 2 May 2022").
     These are the ordinary AF2 template pipeline, identical to the baseline's, and are
     not state-annotated or hand-picked.
  2. **Recycle counts were carried over from the author's earlier peptide–protein docking
     study**, p2–p3: "The number of recycles for v1 and v2 were optimized in a previous
     study of peptide–protein predictions (Johansson-Åkhe and Wallner 2022)." Likewise
     the selective-dropout choice: p3, "In a previous study, we observed an improved
     correlation between ranking_confidence and actual DockQ using selective dropout with
     no dropout in the structural module (Johansson-Åkhe and Wallner 2022)."
     **This is a design-time prior tuned on a different dataset, imported wholesale, and
     it is the single most important thing to notice about this paper's rigour: the
     hyperparameters were frozen before the evaluation set existed.**
  No deposited structure of any CASP15 target informed the design. No state-annotated
  database (GPCRdb, KLIFS, Kincore) appears anywhere.
- **oracle_leakage**: **Essentially NONE for the primary result. This is a genuinely
  blind CASP15 submission and is among the cleanest papers in the corpus on this axis.**
  Enumerated by route:
  1. **Deposited structures as input or template — PRESENT BUT NOT A TARGET-STATE
     ORACLE.** Templates from the 2 May 2022 PDB snapshot are used in some settings
     (p1, p2), predating the CASP15 prediction season, and are *identical to the
     baseline's*: "run with exactly the same MSAs and templates" (p2). No CASP15 target's
     own structure could be in that snapshot; CASP15 targets are unreleased at prediction
     time by construction. No hand-selected or state-chosen template anywhere.
  2. **State annotations from a curated database driving templates or alignments —
     NONE FOUND.** The complete database list is on p2 §2.1 (Uniclust30/UniRef30_2021_03,
     Uniref90, Uniprot/TrEMBL/SwissProt, BFD, Mgnify 2018_12, PDB) — sequence databases
     and the raw PDB only. No GPCRdb, KLIFS, Kincore or any state annotation exists in
     this pipeline.
  3. **Cluster labels derived from known states — NONE FOUND.** No clustering step exists
     anywhere in the method. Selection is by a single scalar score: "The self-assessment
     ranking score (ranking_confidence) ... 0.8ipTM + 0.2pTM, is used for selection" (p2).
  4. **Hyperparameters / sweeps / seeds / stopping criteria tuned against known states —
     NONE FOUND on the evaluation set.** The two tuned quantities (recycle count,
     selective-dropout placement) were both fixed in a prior peptide–protein study, p2–p3:
     "The number of recycles for v1 and v2 were optimized in a previous study of
     peptide–protein predictions (Johansson-Åkhe and Wallner 2022)." No range, value or
     stopping criterion is tuned on CASP15 — the CASP15 predictions were submitted blind
     during the season. The `ranking_confidence > 0.8` stopping criterion recommended on
     p3 ("A good criterion for this is to use a ranking_confidence > 0.8 and require at
     least a couple of structures at this level of confidence") is proposed *after*
     looking at the CASP15 DockQ results and is therefore a post-hoc recommendation, but
     it did not enter the pipeline that produced the reported numbers.
  5. **Success defined post hoc by RMSD/TM to a structure they had — PRESENT AS
     EVALUATION ONLY, WHICH IS NORMAL AND NOT LEAKAGE HERE.** DockQ against the CASP15
     native is the sole metric (p2: "The DockQ (Basu and Wallner 2016) scores for all
     methods that participated in CASP15 were downloaded from the CASP15 website"). The
     natives were unavailable when the models were made, so this is retrospective scoring
     of prospective predictions, not a target defined by a held answer.
  6. **Best/worst model labels assigned against a held reference — NOT USED FOR
     SELECTION; USED FOR ILLUSTRATION.** Rank 1 is chosen by `ranking_confidence`, an
     internal score, never by DockQ (p2). But the two showcase narratives count models
     against the native after the fact: "only 3 of the 6000 models obtained a
     ranking_confidence > 0.8, of which all were of high quality with a DockQ > 0.8. In
     fact, only five high-quality models could be found in the whole set of 6000 models
     sampled" (p3), and "it is possible to generate several high-quality models
     (38/6000)" (p3). These are oracle *counts* used to argue that sampling depth was
     necessary; they do not feed selection and no headline number depends on them.
  7. **Design-level oracle use (route 7, weaker than pipeline leakage) — PRESENT ONLY IN
     TWO PLACES, both minor and both self-declared.**
     (a) The two illustrative targets, H1144 and T1187o, are chosen after the CASP15
     results were known, precisely because they are cases where sampling mattered (p3).
     That is anecdote selection in the discussion, not a design-time state declaration.
     (b) **The AlphaFold-Multimer v3 comparison is explicitly non-blind, and the author
     says so himself**, p3: "However, it is important to note that the v3 predictions are
     not blind since it was released after CASP15 and several targets were already
     available." This is a two-target, post-hoc arm and does not touch the 0.41 → 0.55
     headline.
  **Verdict: NO pipeline leakage into the primary CASP15 result. Design-level exposure is
  limited to post-hoc example selection and the author's own flagged non-blind v3 arm.**
- **prospective**: **YES — genuinely, for the headline result; partial only for the
  appended v3 comparison.** The 0.41 → 0.55 result is a CASP15 blind season submission
  scored against structures released afterwards, with databases frozen 22 April / 2 May
  2022 (p2) and identical inputs to the baseline (p2). This does not follow from the
  author's word for it — CASP15 blindness is structural. The single non-prospective
  element is the v3 arm on two targets, which the author labels non-blind himself (p3).
- **state_metric**: **NOT APPLICABLE — no conformational state predicate exists.** The
  quality metric is **DockQ, a continuous reference-dependent interface score** (Basu and
  Wallner 2016), averaged over interfaces where there are several: "In the case of
  multiple interfaces, DockQ is calculated for each interface and then averaged" (p2).
  **Thresholds are used but never defined in this paper.** "high quality" is used against
  DockQ > 0.8 (p3: "all were of high quality with a DockQ > 0.8") and improvements of
  ">0.4 DockQ units" are described as "essentially going from incorrect to high-quality
  predictions" (p2), but no threshold table, no justification and no citation of the
  standard DockQ bands appears. Recorded as: continuous coordinate, with an
  unstated 0.8 "high quality" cut used informally.
- **metric_saturation**: **Not discussed by the author; a numeric ceiling is nevertheless
  visible.** DockQ is bounded on [0, 1] and `ranking_confidence` on [0, 1]. In Fig 1b
  (p2) a dense cluster of easy targets sits at DockQ ≈ 0.8–0.9 for *both* methods, hard
  against the ceiling, so the comparison there is compressed and the reported average
  improvement is carried by the low-DockQ targets. The paper never mentions this. No arm
  is reported at a floor or ceiling by the author. (Figure-level complaints about Fig 1c/e
  axis truncation are in `hides`, per the v3 split, not here.)
- **directional_control**: **NONE. The method only samples; it cannot be instructed which
  structure or state to produce.** Every handle available is stochastic or
  configurational, and none is state-directed: dropout activation and placement
  (Evoformer-only vs full network), multimer weight version (v1/v2/v3), recycle count,
  templates on/off, and the sheer number of samples. There is no partner toggle, no
  ligand, no nanobody condition, no state-annotated template, no state-filtered MSA and
  no conditioning input of any kind — the MSA is byte-identical to the baseline's (p2,
  p3). The only steering that exists is *post-hoc selection* by `ranking_confidence`
  (p2), which ranks by predicted confidence, not by state. Recorded plainly: **no
  directional control; sampling only.**
- **anti_memorization_design**: **YES, by construction of CASP15, and the cutoff is
  explicitly dated — but n is never stated.** p2 §2.1: "Sequence databases were
  downloaded on 22 April 2022, and the PDB was updated 2 May 2022"; the CASP15 prediction
  season followed, and CASP15 targets are structures unreleased at prediction time. The
  cutoff is therefore defined by the database snapshot dates plus the CASP15 season, not
  by an author-defined hold-out rule. **n = the number of common CASP15 multimer targets,
  which the paper never gives** (see `n_targets`). The author additionally flags the one
  place where this protection lapses, p3: "the v3 predictions are not blind since it was
  released after CASP15 and several targets were already available."
- **anti_memorization_control**: **NONE RUN as a separate arm — and none is needed for
  the headline, because the entire benchmark is post-cutoff.** There is no seen-vs-unseen
  split, no memorisation probe, no pre-/post-cutoff comparison. The nearest thing is the
  v3 arm, which is the *reverse* control (a knowingly contaminated arm) on **2 targets —
  UNPOWERED**, and is presented as a code-update note, not as a control (p3).
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | AlphaFold-Multimer v2 baseline (NBIS-AF2-multimer) run with **byte-identical MSAs and templates** | That the gain comes from better alignments, deeper databases, or different template input rather than from sampling. This is the paper's central and best control: "run with exactly the same MSAs and templates" (p2); "the sole reason for the improved performance of AFsample is improved sampling as AFsample was using identical MSAs" (p3) | p2, p3 |
  | All other groups that participated in CASP15, ranked (Fig 1a) | That the improvement is trivially matched by the rest of the field; establishes the top ranking against ~60 independent pipelines | p1, p2 (Fig 1a) |
  | Per-target paired comparison against the baseline (Fig 1b) | That the average improvement is driven by a handful of targets while others regress — the paired scatter shows the direction target by target | p2 (Fig 1b) |
  | AlphaFold-Multimer **v3** on the two showcase targets (DockQ 0.44 and 0.09) | Partially: that AFsample's advantage is simply superseded by newer weights. **Author-flagged as non-blind and run on n = 2 — UNPOWERED and contaminated** | p3 |
  | Confidence-vs-accuracy scatter over all 6000 models for 2 targets (Fig 1c/e) | That `ranking_confidence` selection is reliable — and it partly *fails* this control: "one-third of the models with a ranking_confidence > 0.8 actually had a wrong domain orientation indicated by the low DockQ score" (p3) | p2, p3 |

  **The decisive control that is NOT run: there is no dropout-off arm at matched sample
  count.** Nothing in the paper separates the contribution of *dropout* from the
  contribution of *6000-vs-25 samples*, or from the v1+v2 weight mixture, or from the
  extra recycles. All six settings use dropout (p2: "Six different settings were used,
  and they all involved using dropout"), so the four levers are fully confounded. The
  causal claim on p3 is only that the gain is *sampling* rather than *inputs*; it is not,
  and cannot be, a claim that dropout specifically is responsible.
- **confidence_as_discriminator**: **YES, centrally — and it is the one place the author
  reports it failing.** `ranking_confidence` = 0.8·ipTM + 0.2·pTM is the *sole* selection
  criterion over the 6000-model pool (p2: "The self-assessment ranking score
  (ranking_confidence), which for multimer is a linear combination of the predicted
  interface TMscore (ipTM) and the predicted TMscore (pTM), 0.8ipTM + 0.2pTM, is used for
  selection"), and it is also proposed as the practical stopping rule (p3:
  "ranking_confidence > 0.8 and require at least a couple of structures at this level of
  confidence"). It is used to judge **model/interface quality, never conformational
  correctness** — there is no conformational question in this paper.
  *Validation*: partial, retrospective, and honest in both directions. Supporting: H1144,
  where all 3 models with `ranking_confidence` > 0.8 had DockQ > 0.8 (p3); and the cited
  prior finding that selective dropout improves the confidence/DockQ correlation
  (Johansson-Åkhe and Wallner 2022, p3). Against: T1187o, where "one-third of the models
  with a ranking_confidence > 0.8 actually had a wrong domain orientation indicated by
  the low DockQ score" (p3). The author's closing position is nonetheless strongly
  pro-confidence, p3: "The success of sampling relies heavily on the excellent internal
  scoring function in AlphaFold, which so far has proven to be exceptionally good."

## D. Claims

- **central_conclusion**: Enabling AlphaFold2's dropout layers at *inference* and
  generating 6000 models per target instead of the default 25 — across six settings that
  also vary the multimer weight version (v1/v2), the recycle count and templates on/off,
  with the MSAs left completely untouched — raises average rank-1 DockQ on common CASP15
  multimer targets from 0.41 to 0.55 and placed the method at the top of the CASP15
  protein-assembly category. **The stated target throughout is multimer prediction
  accuracy, not conformational states**; alternate conformations appear only as an
  unsupported forward-looking suggestion in the abstract's last sentence (p1).
- **necessity_claims** (verbatim, with page):
  1. p3: "Thus, without substantial sampling, most likely, no high-quality model would
     have been generated at all."
  2. p3: "It is clear the sole reason for the improved performance of AFsample is
     improved sampling as AFsample was using identical MSAs as the AlphaFold-Multimer v2
     baseline." *(causal-exclusivity claim; see `controls_run` on what it can and cannot
     support)*
  3. p3: "Dynamics, flexibility, or simply the sheer complexity of large molecular
     assemblies will all require more sampling."
  4. p1: "Furthermore, predicting transient interactions or interactions with flexible
     binding partners, such as short peptides or disordered regions, requires even more
     sampling to achieve optimal performance (Johansson-Åkhe and Wallner 2022)."
  5. p1 (an impossibility claim about plain sampling, and the closest the paper comes to
     a conformational-landscape argument): "For complex cases, simply increasing the
     number of sampled models might not be enough if the evolutionary constraints have
     trapped the prediction in a local minimum in the conformational landscape (Roney and
     Ovchinnikov 2022) or the if the evolutionary constraints are weak." *(sic — "or the
     if" is in the original)*
  6. p3 (superiority claim functioning as a necessity claim for practice): "The results
     from CASP15 demonstrate that the best way to model multimeric protein assemblies
     today is to use AFsample."
- **novelty_claims** (verbatim, with page):
  1. p1 abstract: "We demonstrate that by stochastically perturbing the neural network by
     enabling dropout at inference combined with massive sampling, it is possible to
     improve the quality of the generated models."
  2. p1 abstract: "The method was benchmarked in CASP15, and compared with
     AlphaFold-Multimer v2 it improved the average DockQ from 0.41 to 0.55 using
     identical input and was ranked at the very top in the protein assembly category when
     compared with all other groups participating in CASP15."
  3. p2: "Here, we present AFsample that significantly improves over AlphaFold-Multimer
     v2 baseline (NIBS-AF2-Multimer). The method was the most successful in CASP15 for
     multimer prediction (Wallner 2023)". *(sic — "NIBS" here, "NBIS" everywhere else)*
  **Notable absence, and it is to the paper's credit: there is no claim to be first,
  novel or unprecedented about the technique.** The word "unprecedented" appears twice on
  p1 and both times describes AlphaFold2, not this work ("unprecedented performance",
  "The unprecedented accuracy of AlphaFold version 2"). Inference-time dropout is
  explicitly credited to prior work, p1: "An alternative way to achieve more diversity
  among the generated models is to enable the dropout layers in the neural network
  (Johansson-Åkhe and Wallner 2022, Mirdita et al. 2022)." The novelty asserted is the
  *scale* (6000 models) and the *CASP15 result*, not the mechanism. Anyone using this
  paper as the origin point of the massive-sampling line should record that it claims
  priority on the scale and the benchmark, not on dropout itself.
- **stated_limits**:
  1. **Compute cost, stated bluntly.** p3: "AFsample requires more computational time
     than AF2, as it generates 240× models, and including the extra recycles, the overall
     timing is ∼1000× more costly than the baseline." Mitigated by a triage
     recommendation: "a good strategy is first to run the AF2 baseline prediction and
     only use more sampling if needed" (p3).
  2. **Selection is unreliable at the top of the confidence scale.** p3: "Still, selecting
     the best possible model was not straightforward as one-third of the models with a
     ranking_confidence > 0.8 actually had a wrong domain orientation indicated by the
     low DockQ score."
  3. **The v3 comparison is not blind.** p3: "it is important to note that the v3
     predictions are not blind since it was released after CASP15 and several targets
     were already available."
  4. **Dropout rate was not explored.** p2: "However, there may be instances where
     increasing the dropout rates could prove beneficial to increase the diversity and
     this is something we like to follow up on in future studies." The rates used are the
     training rates: "The dropout rate in the AlphaFold2 network is 10%–25%, depending on
     the network module" (p1).
  Limits the paper does **not** state: that dropout is never isolated from sample count
  (see `controls_run`); that the number of benchmark targets is never given; that the
  alternate-conformation claim in the abstract has no supporting experiment.
- **stance**: **`precedent` on mechanism + `contrast` on scope. Provisional — the user's
  call, not settled here.**
  - *precedent*: this is the origin point of the massive-sampling line and the direct
    antecedent that AFsample2/AFsample3 build on. It establishes, blind and at CASP
    scale, that inference-time stochastic perturbation plus a very large sample budget
    beats the default 25-model protocol on identical inputs (0.41 → 0.55, p1/p2).
  - *contrast*: it is a multimer *accuracy* paper. It defines no state, offers no
    directional control, never separates dropout from sample count, and mentions
    alternate conformations once as an aspiration. Any conformational-states claim
    attributed to AFsample is being read into it.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Average rank-1 DockQ, AFsample (Wallner) | **0.55** | DockQ, 0–1 | common CASP15 multimer targets, scored vs CASP15 natives | p1, p2 |
  | Average rank-1 DockQ, AlphaFold-Multimer v2 baseline (NBIS-AF2-multimer) | **0.41** | DockQ, 0–1 | same targets, identical MSAs and templates | p1, p2 |
  | Absolute improvement | **+0.14** | DockQ units | AFsample − baseline | p1, p2 |
  | Targets improving by more than 0.4 DockQ | **8** | targets | per-target paired comparison, Fig 1b | p2 |
  | CASP15 ranking, protein-assembly category | **top / most successful group** | rank | all groups participating in CASP15, Fig 1a | p1, p2 |
  | Models generated per target, AFsample | **6000** (~1000 per setting × 6 settings) | models | — | p1, p3 |
  | Models generated per target, AlphaFold-Multimer default | **25** | models | — | p1 |
  | Sampling ratio | **240×** | models | AFsample vs baseline | p3 |
  | Compute cost ratio | **∼1000×** | wall-clock, relative | AFsample (incl. extra recycles) vs baseline | p3 |
  | Inference speed | **≤1 minute per model**; "a couple of days on a single GPU" for a difficult target | time | — | p3 |
  | Selection score | **ranking_confidence = 0.8·ipTM + 0.2·pTM** | dimensionless, 0–1 | — | p2 |
  | Recommended triage threshold | **ranking_confidence > 0.8**, plus "at least a couple of structures at this level" | dimensionless | — | p3 |
  | H1144: models with ranking_confidence > 0.8 | **3 of 6000**, all with DockQ > 0.8 | count | scored vs native, post hoc | p3 |
  | H1144: high-quality models in the whole pool | **5 of 6000** | count | scored vs native, post hoc | p3 |
  | H1144: rank-1 DockQ | **0.88** | DockQ | vs native | p2 (Fig 1d caption) |
  | H1144: AlphaFold-Multimer v3 DockQ | **0.44** | DockQ | vs native, **non-blind** | p3 |
  | T1187o: high-quality models generated | **38 of 6000** | count | scored vs native, post hoc | p3 |
  | T1187o: rank-1 DockQ | **0.81** | DockQ | vs native | p2 (Fig 1f caption) |
  | T1187o: AlphaFold-Multimer v2 baseline DockQ | "completely wrong ... **very close to zero**" | DockQ | vs native | p3 |
  | T1187o: AlphaFold-Multimer v3 DockQ | **0.09** | DockQ | vs native, **non-blind** | p3 |
  | T1187o: fraction of ranking_confidence > 0.8 models with wrong domain orientation | **one-third** | fraction | scored vs native, post hoc | p3 |
  | AF2 dropout rate as used (training rates retained) | **10%–25%**, module-dependent | dropout probability | AlphaFold2 network, cited | p1 |
  | Number of settings / settings using selective (Evoformer-only) dropout | **6 total / 4 selective** | settings | — | p2, p3 |

  *(Cited-not-measured, recorded so it is not mistaken for this paper's own result: pLDDT
  and pTM correlations to their true values, 0.76 and 0.85, are quoted from Jumper et al.
  2021 on p1.)*

- **n_predictions**: **Samples per target: 6000** — "For each setting, on the order of
  1000 models were generated per setting for a total of 6000 models per target" (p3),
  matching p1's "We generated 6000 models per target compared with 25 default". Note
  "on the order of 1000", so the per-setting count is approximate and the six settings
  may not be exactly equal. **Targets: NOT REPORTED** (see `n_targets`). **Total models:
  NOT REPORTED** — cannot be computed, since the target count is never given; it is
  6000 × n for an unstated n.
- **comparable_to_ours**:
- **si_in_scope**: **SI NOT HELD, and the gap is material.** p2 refers the reader to
  Supplementary Table S1 for the settings — "AFsample generates a large pool of models
  using different settings (Supplementary Table S1)" — and p3 states only "Supplementary
  data are available at Bioinformatics online." **Supplementary Table S1 is the only
  place the six settings are enumerated**, so the exact protocol (which setting used
  which weight version, how many recycles, templates on or off, full vs selective
  dropout, and the exact model count per setting) **cannot be reconstructed from the held
  PDF**. The main text gives only the ingredient list, not the assignment. Everything in
  `metrics_reported` above is from the main text and figure captions; no headline number
  is lost to the SI.

## F. Figures

**Licence for all figures: CC-BY 4.0, no ND clause and no NC clause** — p1 footer: "This
is an Open Access article distributed under the terms of the Creative Commons Attribution
License (https://creativecommons.org/licenses/by/4.0/), which permits unrestricted reuse,
distribution, and reproduction in any medium, provided the original work is properly
cited." Panels may be reproduced, redrawn and adapted with attribution.

**The paper contains exactly one figure (Fig 1, p2) with six panels (a–f), and no
tables.** Four panel-group rows, split on `mark`/`measure` per the v3 rule: 1A is a line,
1B a labelled scatter, 1C+1E share a mark and a measure and differ only by target
(facet), and 1D+1F are renders. Panel marks and axis ranges are not in the caption and
were read from a 150 dpi render of p2.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 2 | Every CASP15 group's average DockQ on the common multimeric targets, sorted ascending as a rising curve; two stars mark the AF-Multimer v2 baseline (0.41) and AFsample (0.55) at the very top | line | `PLOT \| facet: none (1) \| vary: CASP15 group, rank-ordered ascending (n NOT REPORTED; ~60 tick labels legible at 150 dpi) \| series: none (1) \| measure: average DockQ on common multimeric targets, axis 0.0–0.55 \| mark: line, with 2 star point markers annotated 0.41 and 0.55 \| n: 1 per mark (one group); number of targets behind each group's average NOT REPORTED` | 1 | **Group tick labels are printed at a size that is illegible in the published figure**, so only the two starred groups can be identified and the reader cannot see who else is near the top or how close they are; **the number of targets behind each average is never given, on the panel or in the text**; no error bars, no spread, no per-target information — a sorted line of point estimates is presented as a ranking with no uncertainty; the y-axis stops at ~0.55, i.e. at the paper's own result | CC-BY 4.0, no ND, p1 |
| 1B | 2 | Paired per-target comparison: AFsample rank-1 DockQ (x) against AF-Multimer v2 baseline rank-1 DockQ (y), with the y = x diagonal drawn; points labelled with CASP target IDs | scatter | `PLOT \| facet: none (1) \| vary: AFsample (Wallner) average DockQ for rank 1, 0.0–1.0 (continuous) \| series: none (1) \| measure: NBIS-AF2-multimer average DockQ for rank 1, 0.0–1.0 \| mark: point, each labelled with its CASP target ID \| n: 1 per mark (one target); per panel = number of common CASP15 multimer targets, NOT REPORTED (~39 labelled points)` | 1 | **n is not stated anywhere**, so the reader must count labelled dots to learn the size of the benchmark; the "eight targets showing considerable improvements with >0.4 DockQ units" claimed on p2 is **not marked on the panel** — no threshold band, no highlighting, no count annotation; overlapping ID labels are unreadable in the 0.6–0.8 cluster; targets are unordered and undistinguished by type, so the nanobody/antibody cases that motivate the discussion cannot be located | CC-BY 4.0, no ND, p1 |
| 1C+1E | 2 | The paper's core evidence: all ~6000 sampled models for one target plotted as `ranking_confidence` against DockQ — H1144 (c), where only a handful of points reach the high-confidence/high-DockQ corner, and T1187o (e), where a high-confidence band contains both correct and wrong-orientation models | scatter | `PLOT \| facet: CASP target (2: H1144, T1187o) \| vary: ranking_confidence, ~0.2–0.9 (continuous) \| series: none (1) \| measure: DockQ, 0.0–1.0 \| mark: point \| n: 1 per mark (one sampled model); ~6000 models per panel` | 2, vary by target; one row because mark and measure are shared and only the facet differs | **Severe overplotting: ~6000 opaque points per panel in a panel roughly a quarter the area of 1B, with no transparency, no density encoding and no marginal distribution** — the 3 points (H1144) and 38 points (T1187o) that the entire "you need 6000 samples" argument rests on are visually indistinguishable from the cloud; **the `ranking_confidence` axis is truncated to ~0.2–0.9 rather than the full 0–1 score range**, with no break marks; n is printed on neither panel; the two panels carrying the paper's mechanism are given less than half the space of the summary scatter above them | CC-BY 4.0, no ND, p1 |
| 1D+1F | 2 | Rank-1 prediction (grey) superposed on the native complex — H1144 (d), native chain A green and chain B cyan, DockQ = 0.88; T1187o (f), same colouring, DockQ = 0.81 | structure render | `RENDER \| facet: CASP target (2: H1144, T1187o) \| views: 1 (single cartoon view per target) \| overlay: 1 prediction on 1 reference \| axis: none` | 2, vary by target | **One model of ~6000 shown per target, selected by `ranking_confidence`** — the ensemble spread that is the paper's subject is invisible; no scale bar, no per-interface DockQ breakdown for the multi-interface case, and the wrong-domain-orientation failure mode described in the text (p3) is never rendered, so the reader sees only the success | CC-BY 4.0, no ND, p1 |

*(There are no tables in the article. Supplementary Table S1, the settings table, is not
held — see `si_in_scope`.)*

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5)
- **schema_version**: `v3`
- **confidence**: **high** on the mechanism, the input regime, the claims, the licence and
  every headline number — the paper is short, blunt and unusually explicit that the MSAs
  were identical and that dropout plus sample count is the whole intervention. **Medium**
  on the figure rows: no panel carries an n, the marks and axis ranges are absent from the
  caption and were read from a 150 dpi render of p2, and the ~39 targets in Fig 1b and
  ~60 groups in Fig 1a are my counts off that render, not paper statements. **Low** on
  the protocol detail: the six settings exist only in Supplementary Table S1, which is not
  held, so the assignment of weight version / recycle count / template state / dropout
  placement across settings is unknown.
- **unresolved**:
  1. **The number of benchmark targets is never stated.** "Common CASP15 multimer
     targets" is the only description (p2). `n_targets`, the per-panel n for Fig 1b, and
     the total model count in `n_predictions` are all blocked by this single omission.
  2. **Supplementary Table S1 is not held**, so the six settings cannot be reconstructed.
     The main text says only that all six used dropout, four used selective (Evoformer-
     only) dropout, and that v1 and v2 weights, extra recycles and both template states
     appear somewhere in the set. Which combination is which, and how the ~1000 models per
     setting were distributed, is unrecoverable from the PDF.
  3. **Dropout is never isolated from sample count.** No arm runs 6000 models with dropout
     off, and no arm runs a single weight version or a single recycle setting. The p3
     claim that "the sole reason for the improved performance of AFsample is improved
     sampling" is supported against the *input* hypothesis (identical MSAs) but leaves
     dropout, sample count, weight mixing and recycle count mutually confounded. Anyone
     citing this paper for "dropout works" is citing something it did not measure
     separately.
  4. **The `ranking_confidence > 0.8` triage criterion (p3) is recommended after the
     CASP15 results were seen**, on the strength of two illustrative targets, one of which
     (T1187o) shows it failing a third of the time. It did not enter the reported
     pipeline, so it is not leakage, but it should not be read as a validated threshold.
  5. **Typos in the original that a quoting author should know about**: "NIBS-AF2-
     Multimer" on p2 versus "NBIS-AF2-multimer" everywhere else; "or the if the
     evolutionary constraints are weak" on p1. Both are quoted verbatim above.
  6. **Tag vocabulary gaps (none invented).**
     - **There is no Method tag for inference-time dropout / stochastic weight
       perturbation.** `enhanced-sampling` has been applied, following the corpus
       precedent already set in `kalakoti2025afsample2`, where it is used for exactly this
       family ("an inference-time noise injection that broadens the sampled ensemble at a
       fixed architecture"). It remains imprecise: it sits next to `md` in the vocabulary
       and will read as MD enhanced sampling to anyone who has not read this note.
       Requested: **`inference-dropout`** (and possibly **`massive-sampling`**, since the
       sample *budget* is half of this paper's actual claim and no tag expresses scale).
     - **No Protocol tag fits "templates on in some settings and off in others, full-depth
       untouched MSA throughout".** `templates-on` has been applied because templates are
       genuinely used in part of the pool, but it is half the truth; `no-template-no-msa`
       is flatly wrong (full_dbs MSA); `state-annotated-input` is wrong. Requested: a
       Protocol tag that can express a mixed template regime, or a
       **`no-template-msa-on`** counterpart as also requested by `mitjavila2026afsample2t`.
     - **No Metric tag expresses DockQ / interface quality.** DockQ is a bounded composite
       of Fnat, LRMSD and iRMSD against a reference — continuous, reference-dependent, but
       not a state predicate and not plain RMSD. `continuous-metric` has been applied;
       `rmsd-only` was declined as actively misleading. A reverse lookup for "papers
       evaluated by interface quality / docking accuracy" will find nothing.
  7. **`state_metric`, `states_generated` and `metric_saturation` all presuppose a
     conformational endpoint that this paper does not have.** v3 gave `states_generated`
     an explicit `NOT APPLICABLE` escape (worded for wet-lab papers), but `state_metric`
     has none, and a prediction-accuracy paper with no state question is a real category
     in this corpus. The fields were answered against what the paper measured, with the
     inapplicability stated, but the index row will mislead anyone reading it without the
     note. Suggested: extend the `NOT APPLICABLE` wording in `state_metric` to cover
     "paper has no conformational endpoint", not only "nothing generated".
  8. **`metric_saturation` is ambiguous between *observed* and *possible* saturation.**
     v3 fixed the double-recording problem with `hides` but does not say whether a bounded
     metric that visibly compresses a cluster of easy cases near its ceiling — with the
     authors never mentioning it — counts. It has been recorded here as a visible ceiling
     with an explicit note that the paper does not discuss it.
  9. **`controls_run` has no column for a control that was conspicuously *not* run.** The
     absent dropout-off arm is the most informative thing about this paper's causal claim,
     and it had to be written as prose beneath the table. A `controls NOT run` companion
     row-set, or an explicit instruction to note absences there, would make that
     retrievable.
- **why_it_matters**:

## Tags

`general-protein` `enhanced-sampling` `templates-on` `ensemble` `single-state` `continuous-metric` `prospective` `anti-memorization` `unpowered` `confidence-as-discriminator` `seed-only` `peer-reviewed` `precedent` `contrast` `comparator-numbers`

### Tag notes (not tags)

- **`enhanced-sampling` is the method tag, and it must be read as "inference-time
  stochastic sampling of a fixed AF2 network", not as MD enhanced sampling.** This
  follows the precedent already set in `kalakoti2025afsample2`. The missing
  `inference-dropout` tag is logged under `unresolved` 6 and was **not** invented.
- **NO MSA tag is applied, and this is the single most important tagging decision on this
  paper.** `msa-subsample` is wrong — depth is untouched. `msa-state-filter` is wrong —
  no state-specific alignment. Column masking is not done either. The MSAs are
  **byte-identical to the baseline's** (p2, p3), and the author explicitly names MSA
  perturbation as the *other* option he did not take (p1). AFsample is a **dropout +
  sample-budget** method; AFsample2/AFsample2T/AFsample3 add MSA manipulation on top.
  Tagging this paper with any MSA tag would collapse exactly the distinction the corpus
  needs to keep, and would make every "which papers manipulate the MSA" query return the
  one paper in the line that does not.
- **`templates-on` is applied at half strength.** Templates are on in some of the six
  settings and off in others ("with and without templates", p1); no Protocol tag can
  express a mixed regime. See `unresolved` 6.
- **`ensemble` + `single-state`** per the v3 dual rule: 6000 models are generated per
  target, and exactly one is selected and reported. Both halves are the paper.
  **`two-state` and `continuum` are NOT applied** — no state is defined and none is
  claimed.
- **`continuous-metric`** for DockQ. **`rmsd-only` deliberately NOT applied** — DockQ is a
  composite interface score, and the tag would false-positive RMSD-metric queries.
  **`binary-predicate` NOT applied** — the informal "high quality = DockQ > 0.8" (p3) is
  never operationalised as a success predicate for the headline result.
  **`saturating-metric` NOT applied** — the ceiling compression in Fig 1b is visible but
  the paper reports no arm at floor or ceiling, and applying it would overstate.
  **`visual-metric` NOT applied** — nothing is called by eye; every claim is a DockQ
  number.
- **`prospective` is applied and is genuinely earned**, which is rare in this corpus. The
  0.41 → 0.55 result is a CASP15 blind-season submission with databases frozen 22 April /
  2 May 2022 (p2). It follows from the protocol, not from the author's word for it.
- **`oracle-leak` is deliberately NOT applied.** All seven routes were checked separately
  and none is present in the pipeline that produced the reported numbers; see
  `oracle_leakage`.
- **`design-level-oracle` is deliberately NOT applied either**, which is a judgement call
  worth stating. Route 7 exposure is limited to (a) picking two illustrative targets after
  the results were known and (b) the author's own explicitly-flagged non-blind
  AlphaFold-Multimer v3 comparison on n = 2 (p3). Neither declares an expected answer
  before a reported result is read; both live in the discussion, not the design. Applying
  the tag would put this paper alongside benchmarks whose target *admission criterion* was
  a known answer, which would be a false equivalence.
- **`anti-memorization` is applied** — the post-cutoff condition is structural to CASP15
  and the snapshot dates are given (p2). **`no-anti-memorization` therefore NOT applied.**
  Note the distinction the schema draws: the *design* is sound, but no memorisation
  **control arm** was run (`anti_memorization_control` = NONE RUN), because none was
  needed.
- **`unpowered` is applied narrowly and only for the AlphaFold-Multimer v3 arm** (p3),
  which is n = 2 and non-blind. It does **not** apply to the CASP15 headline, whose
  target count is unstated but is on the order of 39 from Fig 1b. Read this tag on this
  paper as "one appended arm is unpowered", not "the paper is unpowered".
- **`confidence-as-discriminator` is applied.** `ranking_confidence` (0.8·ipTM + 0.2·pTM)
  is the sole selection handle over 6000 models (p2) and the proposed stopping criterion
  (p3). Applied even though it discriminates *quality*, not *conformational correctness* —
  the paper has no conformational question. The author reports it failing one-third of the
  time above threshold on T1187o (p3), which makes this paper useful evidence *against*
  naive confidence-based selection as well as for it.
- **`multi-backbone` is deliberately NOT applied.** v1, v2 and v3 are weight versions of
  one AlphaFold-Multimer architecture (p1, p2, p3), not distinct backbones. Applying it
  would false-positive every AF3-vs-Boltz-vs-Chai query.
- **`seed-only` is applied for the control axis, and is the correct answer to
  `directional_control`.** The only handles are stochastic (dropout draws, seeds) or
  configurational (weight version, recycles, templates); none can be pointed at a state.
  **`directed-state`, `partner-driven`, `ligand-driven`, `peptide-driven`,
  `g-protein-mimetic`, `nanobody` and `apo-sampling` are all NOT applied.** In particular
  **`nanobody` is NOT applied** even though H1144 is a nanobody complex (p3) — the
  nanobody is a *target*, not a control handle, and the tag means the latter.
- **No Site tag is applied** — no binding site, pocket or allosteric question appears.
- **`benchmark-only` is NOT applied** — a method is presented, benchmarked though the
  vehicle is.
- **`experimental-validation` and `experimental` are NOT applied** — no wet-lab work.
- **`precedent` + `contrast`** per `stance`, both provisional. Precedent on the mechanism
  and the blind CASP15 evidence; contrast because it is a multimer-accuracy paper with no
  state definition and no directional control, and is routinely read as more
  conformational than it is.
- **`comparator-numbers` is applied** — 0.41 vs 0.55 average DockQ, 25 vs 6000 models per
  target, 240× sampling and ∼1000× compute are all directly quotable comparators.
- **`figure-exemplar` is NOT applied** — one figure, and three of its four panel groups
  have recorded defects.
