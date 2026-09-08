# gilson2025casp16

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–18).** The PDF page does
**not** equal the printed page: PDF p1 prints "249" and the mapping is `printed = 248 + PDF`,
so PDF p18 prints "266". All citations below are PDF pages. Layout: p1 masthead + abstract +
Introduction; p2 Table 1 + Introduction end + Methods 2.1; p3 Figure 1 + target descriptions;
p4 targets end + 2.2 Structure of the Challenge (the timeline) + 2.3 begins; p5 2.3 Evaluation
Metrics + 2.4 Baseline Predictors; p6 baselines end + 2.5 PDB-similarity assessment + Results
begin + 3.1.1 Submissions; p7 3.1.2 Assessments + Figure 2 legend; p8 Figure 3 (full page);
p9 Figure 4 + best-of-5 analysis; p10 Figure 5 + 3.1.3 correlates + 3.1.4 baseline poses;
p11 Figure 6 + Table 2 + 3.2 incidental ligands; p12 Figure 7 + 3.3 affinity + the disclosed-data
removal; p13 Figure 8 + expected-τ analysis; p14 Figures 9 and 10 + 3.3.2 + 3.4 + Discussion
begins; p15 Discussion end + Conclusions; p16–p18 acknowledgements, conflicts, data
availability, references, and the Supporting Information manifest.

**THE SI IS NOT HELD.** Table S1, Table S2 and Figures S1–S10 are all cited in the text and
none is present; the 18-page PDF is main text only. This matters in five specific places, all
listed under `si_in_scope`, the sharpest being **Table S2 (the per-supertarget LDDT-PLI table
for every group)** and **Figure S10 (the affinity assessment recomputed *with* the
previously-disclosed targets left in — the paper's own leakage control)**.

**Why this note is long on `oracle_leakage` and `prospective`:** this is a genuinely blind,
genuinely prospective community assessment — the same rare property that makes
`chitsazi2025gpcrdock4` valuable, and the two are the corpus's only true blind competitions.
The timeline is reconstructed date by date with page-cited quotes so the blindness claim is
checkable rather than asserted. It is also the corpus's only blind competition in which the
organisers **found leakage after the fact, quantified it, and removed the affected targets** —
5 pose targets and 18 affinity targets. See routes 1 and 7.

**Schema friction, stated up front because it changes how this note reads:** v3's routes 5 and
6 (success defined post hoc by RMSD to a held reference; best/worst labels assigned against a
held reference) are **structurally present in every blind assessment and are what a blind
assessment *is***. There is no v3 syntax for "applied by the assessor after the predictions
were sealed". Both routes are recorded below as `PRESENT BY DESIGN — ASSESSOR-SIDE,
POST-SEAL`, in prose, and the gap is flagged in `unresolved` item 1. Do not let this note be
read as leaky.

**License: CC-BY, no ND clause.** Redrawing and adapting the figures is permitted with
attribution. See `reuse` in section F.

---

## A. Identity

- **citekey**: `gilson2025casp16`
- **doi**: **10.1002/prot.70061** — p1 footer, and `refs.bib`.
- **year**: **Dual, and the citekey year is the submission year, not the issue year.**
  Received 25 April 2025 | Revised 10 September 2025 | Accepted 15 September 2025 (p1).
  The running footer on every page reads "Proteins: Structure, Function, and Bioinformatics,
  **2026**" and the p1 citation line reads "Proteins: Structure, Function, and Bioinformatics,
  **2026; 94:249–266**". So: accepted 2025, issued 2026, vol 94, pp 249–266. `refs.bib` records
  `year = {2025}`. Cite as 2026 if the journal issue is what matters; the citekey stays as is.
- **venue**: **Proteins: Structure, Function, and Bioinformatics (Wiley) — PEER-REVIEWED
  research article, open access.** p1: "RESEARCH ARTICLE   OPEN ACCESS", with received /
  revised / accepted dates, which is the peer-review record. Tagged `peer-reviewed`, not
  `preprint`. This is one of the CASP16 special-issue assessment papers (the companion
  experimental-datasets paper is cited as ref [19], "Proteins 94, no. 1 (2026): 79–85").
- **title**: "Assessment of Pharmaceutical Protein–Ligand Pose and Affinity Predictions in
  CASP16" — p1.
- **authors**: Michael K. Gilson (corresponding, mgilson@ucsd.edu, Skaggs School of Pharmacy
  and Pharmaceutical Sciences, UC San Diego), Jerome Eberhardt (SIB Swiss Institute of
  Bioinformatics / Biozentrum, University of Basel), Peter Škrinjar (SIB / Biozentrum), Janani
  Durairaj (SIB / Biozentrum), Xavier Robin (SIB / Biozentrum), Andriy Kryshtafovych (Genome
  Center, UC Davis) — p1.
  **Continuity notes that bear on how to read the paper:** (i) Xavier Robin is first author of
  the CASP15 protein–ligand assessment [ref 8] from which the BiSyRMSD and LDDT-PLI metrics are
  inherited (p5); (ii) Jerome Eberhardt is an author of AutoDock Vina 1.2.0 [ref 26], which is
  one of the baseline predictors he then runs (p5–p6) — the paper discloses the Vina protocol
  in full and explicitly says it was left untuned (p10, p14); (iii) Peter Škrinjar, Eberhardt
  and Durairaj are authors of ref [43], "Have Protein-Ligand Co-Folding Methods Moved Beyond
  Memorisation?", which supplies the template-search protocol used in Section 2.5 (p6) and is
  cited to support the claim that Boltz-1 is generally less accurate than AF3 (p10). That
  paper is `skrinjar2026generalization` in this corpus; the memorization framing here is
  inherited from it; (iv) Kryshtafovych is the CASP Prediction Center's data manager and is an
  author on the CASP new-categories paper [ref 7].
  **Conflict of interest declared, p16:** "M.K.G. has an equity interest in and is a cofounder
  and scientific advisor of VeraChem LLC. He is also on the scientific advisory boards of
  Denovicon Therapeutics, In Cerebro, Cold Start Therapeutics, and Beren Therapeutics." No
  VeraChem method is among the assessed groups or the baselines.

## B. Scope

- **system**: **General protein — five human/viral globular proteins, four of them enzymes,
  none a GPCR, none a protein kinase.** Table 1 (p2) and descriptions p3–p4:
  - **Chymase** — "a globular, 247-residue enzyme with a structural Zn outside the active
    site" (p3). Serine protease. Contributor F. Hoffmann-La Roche.
  - **Cathepsin G** — "a 255-residue globular enzyme, structurally similar to chymase" (p3).
    Serine protease. Roche.
  - **Autotaxin** — "a larger (846-residue), single-chain, globular enzyme, with one or two Zn
    ions in or near the active site … a posttranslational N-glycosylation far from the active
    site … The protein sequence is a hybrid construct, with most of the structure derived from
    rat, which is easier to crystallize, but with binding site residues from the human protein.
    The construct also includes a His tag" (p3). Roche. **This chimeric construct is worth
    noting: predictors were given a sequence that exists in no organism.**
  - **SARS-CoV-2 main protease (Mpro)** — "a medium-sized, homodimeric globular enzyme with 306
    residues per chain … there are two chemically equivalent binding sites" (p3–p4). Contributor
    Idorsia Pharmaceuticals. Four ligands are **covalently bound** to a Cys sulfur, with the
    attachment points given as SMARTS strings (p4).
  - **WDR55** — "a 383-residue WD repeat protein, which is not an enzyme and also is not so far
    considered a drug target … WDR55 did not have a known, well-characterized binding site"
    (p4). Contributor Structural Genomics Consortium. **This is the paper's only novel-fold /
    novel-site case and its n is 1.**
  - Crystallographic resolutions (Table 1, p2): chymase 1.1–2.2 Å (mean 1.7); cathepsin G 1.2,
    1.2 Å; autotaxin 1.3–2.7 Å (mean 1.9); Mpro 1.3–1.9 Å (mean 1.7); WDR55 1.2 Å. **These are
    high-resolution X-ray answers, not cryo-EM** — a material difference from
    `chitsazi2025gpcrdock4`, where four of five answers were cryo-EM at 3.2 Å.
  - **Prior structural coverage of the targets, quantified.** p4: "whereas the other
    ligand–protein complexes used in this challenge had maximum similarity scores (of range
    0–1) to an existing structure in the PDB ranging between 0.3 and 0.9, the similarity score
    for the WDR55 target was 0.0". The authors return to this in the Discussion, p14: "This
    outcome may, again, reflect the fact that the main protein targets here are already well
    represented in the PDB. In future challenges, we hope that some less well-characterized
    systems may be included among the targets in order to better probe the generalizability of
    pose-prediction methods to novel drug discovery targets."

- **n_targets**: **5 proteins. Two different target counts follow from them and must never be
  merged — the pose count and the affinity count differ by system, by n, and by conclusion.**
  - **POSE: 229 drug-like pose targets.** Table 1 (p2) `Npose` column: chymase 17
    (L1001–L1017), cathepsin G 2 (L2001, L2002), autotaxin 189 (IDs in L3001–L3231), Mpro 20
    (IDs in L4001–L4028), WDR55 1 (L5001). 17 + 2 + 189 + 20 + 1 = **229**, and p7 confirms:
    "Most groups included predictions for all or nearly all of the 229 pose prediction
    targets". **Autotaxin alone is 189/229 = 83% of the pose set** — Table 2's own footnote
    (p11) warns: "Autotaxin, with 189 targets, dominates the overall averages."
  - Mpro's pose count was reduced from 25 to 20 by the leakage discovery (p4, quoted under
    `oracle_leakage` route 1).
  - **AFFINITY: 140 posed, 122 assessed, 103 in Stage 2.** Abstract p1: "229 protein–ligand
    pose targets and 140 affinity targets". Table 1 (p2) `Naffinity`: chymase Stage 1 = 17,
    Stage 2 = 17; autotaxin Stage 1 = 123, Stage 2 = 93; cathepsin G, Mpro and WDR55 = 0.
    17 + 123 = **140 Stage-1 affinity targets**. After removing previously disclosed data
    (p12): 14 chymase + 108 autotaxin = **122 assessed**. Stage 2: "Structures were available
    for all 17 of the originally posed chymase targets, so 14 were used following the removal
    of three previously disclosed data points. Structures were available for 93 of the original
    autotaxin affinity targets, and 89 undisclosed affinities with associated cocrystal
    structures were available for Stage 2" (p14) → 14 + 89 = **103 Stage-2 affinity targets**.
  - **Autotaxin's internal split (p3):** "The autotaxin dataset comprises 93 protein–ligand
    pairs with both structures and affinities to predict; 96 with only structures to predict;
    and 30 with only affinities to predict." (93 + 96 = 189 poses; 93 + 30 = 123 affinities.)
  - **A third, separate target set: incidental ligands.** Sulfate, acetate, bromide, chloride,
    DMSO, ethylene glycol, tetraethylene glycol found within 4.5 Å of the drug-like ligand in
    some autotaxin and Mpro structures (p2). Predictions for these were invited, scored, and
    reported separately in Figure S8 (not held). Their count is **NOT REPORTED**.
  - **Affinity ranges (Table 1, p2):** chymase 1–400 nM; autotaxin 1 nM–10 μM. Restated as
    dynamic range on p13: chymase 400×, autotaxin 8700×. This 400× range is the direct cause of
    the chymase metric ceiling — see `metric_saturation`.

- **method_class**: **`benchmark-only`, plus an assessor-run baseline arm that is
  co-folding + docking.** The six authors are the CASP16 ligand-category assessors; they
  propose no prediction method of their own. The baseline arm (Section 2.4, p5–p6) is theirs
  and is explicitly retrospective: p10, "These calculations were not conducted in a blinded
  setting, so the outcomes cannot be viewed as true CASP results." Keep the two arms apart in
  every downstream use of this note.

- **backbones**: **Two populations; do not merge them.**
  - **Assessor-side baselines (retrospective, four methods head-to-head on all 229 targets
    except L5001):** **AlphaFold 3**, **Boltz-1 (v0.4.1)**, **RoseTTAFold All-Atom (RFAA)**,
    and **AutoDock Vina** used with SWISS-MODEL receptors (p5). Affinity baselines: molecular
    weight, cLogP, a Gaussian process regressor on ChEMBL, AD Vina scores (Stage 1), and
    GNINA v1.3 + AD Vina rescoring of the crystal poses (Stage 2) (p6). Four co-folding /
    docking backbones compared on identical inputs → tagged `multi-backbone`.
  - **Participant-side (blind, 2024):** not systematically catalogued in this PDF. Named
    method families, p6: "physics-based modeling (though none used the highly regarded approach
    of simulation-based free energy calculations [44, 45]), methods based on artificial
    intelligence with DNNs (AI), and template-based methods". Named tools: **NeuralPlexer** and
    **DiffDock** in combination (MULTICOM_ligand, p12); **graph neural networks trained on
    PDBbind** (Haiping group 16, p12); citizen-scientist **DockIt** (Drugit, p7). Group names
    visible in Figure 3 imply AF2-based pipelines (Zou_af2, 420) and established docking codes
    (HADDOCK 8, ClusPro 494, CoDock 262, KiharaLab 294, Koes 309, VnsDock 82, DIMAIO 432,
    McGuffin 164, Schneidman 191, SNU-CHEM-lig 408, OpenComplex 167/450, GPLAffinity 416,
    PocketTracer 464, GrominhaLab 272, Vinardo 363, UNRES 261, LCBio 189, Seamount 92,
    comppharmunibas 20, arosko 39, KUMC 227, Bryant 32, ShanghaiTech-human 298,
    ShanghaiTech-Ligand 386, Huang-HUST 91, CCB-AIGDock 474, Zou 204, Drugit 201). **The
    per-group method descriptions are not in this PDF** — they live in the CASP16 abstracts
    booklet, cited at p7: "https://predictioncenter.org/casp16/doc/CASP16_Abstracts.pdf". See
    `unresolved` item 3: this is why the paper's central template-based claim cannot be audited
    from the paper alone.
  - **A key negative:** p10, "during the challenge period, the publicly available version of
    AF3 was not able to run this challenge because it could not co-fold a protein with an
    arbitrary ligand, only one of a small set of ligands", and p5, "AlphaFold 3 and Boltz-1
    were not publicly available in a form suitable for protein–ligand pose predictions during
    the actual challenge, so these methods could not be used by CASP16 participants." **AF3 and
    Boltz-1 are therefore not in the blind arm at all.** The headline "AF3 beats the best CASP
    predictor" is a comparison between a blind arm and a non-blind arm.

- **templates**: **ON, uncontrolled on the participant side, and central to the paper's main
  finding.**
  - Participants were free to use any template. The paper's headline finding is that the ones
    who did so won (p14, quoted verbatim in `central_conclusion` and `necessity_claims`).
    Per-group template settings are **NOT REPORTED** in this PDF.
  - **Do not misread the "template PDB file" the organisers supplied.** p4: the website
    provided "for structure predictions, a template protein PDB file with the coordinate fields
    **filled with zeroes** as an unambiguous guide to what was to be predicted". That is a
    submission-format skeleton carrying **no coordinates**. It is not structural information
    and must not be recorded as a template hand-out.
  - Assessor-side: AD Vina docked into a **SWISS-MODEL homology model** built from a named PDB
    template per supertarget — "5yjp [29] for chymase (L1000), 1cgh [30] for cathepsin G
    (L2000), 5s9m [31] for autotaxin (L3000), and 7n8c [32] for Mpro (L4000)" (p5). Template
    selection criterion, p5: "The best template was selected based on the sequence identity to
    the reference sequence and **the presence of a ligand in the main known pocket**, regardless
    of its nature." AF3/Boltz-1/RFAA template usage is **NOT REPORTED** (only MSAs are
    described).
  - **Template cutoff dates are stated and differ by arm**, p6: "The template cutoff dates were
    set to the training cutoff dates used for each DNN method; **September 30, 2021**, was used
    for both AF3 and Boltz-1, whereas **March 31, 2020**, was used for RFAA. For CASP
    participants and the naïve docking protocol, we used **May 3, 2024**, which corresponds to
    the deposition date of the supertargets L1000, L2000, L3000, and L5000 datasets."

- **msa_handling**: **Full, and deliberately identical across the two co-folding baselines.**
  p5: "To ensure that the DNN methods were compared on an equal footing, we used the same MSAs
  as input for both AF3 and Boltz-1. The standard AF3 MSA generation pipeline was run to obtain
  the non-paired and paired MSAs for each system. The same pairing keys were used to generate
  the custom MSA CSV files for Boltz-1. For unpaired sequences, pairing keys were set to −1."
  No subsampling, no clustering, no state filtering anywhere in the paper. Participant-side MSA
  handling: **NOT REPORTED**.

## C. Conformational core

**Read this whole section against one sentence, p4: "We did not assess the accuracy of the
overall protein structures because multiple crystal structures of these target proteins were
already available in the PDB."** This paper has no conformational-state axis by construction.
Section C is therefore thin by design, not by sloppiness — but the fields below are still the
honest answers, and `state_metric` is where the important negative lives.

- **states_generated**: **one.** Each submitted model is a single static protein–ligand
  complex; each target has a single crystallographic answer. Participants could submit up to
  five models per target (p4: "participants were permitted to submit up to five different
  predictions, termed Model 1 to Model 5, with the understanding that Model 1 would be
  considered their best or most favored prediction"), and the assessors analyse both Model 1
  and best-of-five (p9), but **the five models are alternative poses of the same ligand in the
  same protein state, not alternative protein conformational states** — the paper never treats
  them as states and never reports the spread among them except as a best-of statistic. The
  baselines generate 25 models per system (5 seeds × 5 diffusion samples, p5) and **only one is
  used**: p10, "to generate a single pose prediction for each of the CASP16 protein–ligand
  targets". How that one was chosen from the 25 is **NOT REPORTED** — see `unresolved` item 4.
  Not `ensemble`: nothing ensemble-shaped survives into the assessed object.

- **structural_priors_used**: **Extensive, legitimate, and the paper's actual subject matter.**
  This is where the PDB-knowledge that this paper is *about* belongs; it is not a defect and
  must not be filed as leakage.
  1. **Target selection at design time.** The five systems are established, heavily-deposited
     pharma targets ("the protein targets are already well characterized, with many data
     available in the public domain", p14; maximum PDB similarity 0.3–0.9, p4). The organisers
     chose them for their pharmaceutical relevance and data availability, not for the answer.
  2. **Template-based participant methods are prior-driven by definition**, p14: "they seek to
     model the protein–ligand structure on existing similar co-crystal structures available in
     the PDB".
  3. **Every DNN in the paper is trained on the PDB** (p10: "the deep-learning methods are
     trained on structural data in the PDB"), and the best affinity method is "graph neural
     networks trained on PDBbind [59]" (p12).
  4. **The assessors' own baselines are prior-driven**: SWISS-MODEL homology receptors from
     named PDB templates, docking box "center … defined based on the ligand present in the
     template" with "search box dimensions … set to 25 × 25 × 25 Å" (p5–p6). The binding-site
     *location* for four of five supertargets therefore came from a related holo structure.
  5. **The affinity baseline GPR is trained on public assay data**, p6: "A separate GPR model
     was trained for each supertarget, chymase (L1000) and autotaxin (L3000), using the
     CHEMBL3691 and CHEMBL4068 datasets … These datasets contained 1110 IC50 values for human
     chymase, ranging from 0.3 nM to 570 μM, and 450 IC50 values for human autotaxin, ranging
     from 10 pM to 1.25 mM", ChEMBL "accessed on December 5, 2024".
  6. **Post hoc quantification of the prior**, Section 2.5 (p6): Foldseek fold search + SuCOS
     ligand-shape overlap × pocket coverage, giving a 0–1 similarity score per target. Used only
     to *analyse* results, never to make a prediction.

- **oracle_leakage**: **All seven routes below. Headline: the participant arm is CLEAN, with
  two documented leaks that the organisers found and excised; the assessor baseline arm is
  openly non-blind and says so. Routes 5 and 6 are present by design and assessor-side.**

  **Route 1 — deposited structures of the target used as input or template. TWO REAL LEAKS,
  BOTH FOUND BY THE ORGANISERS AND REMOVED, plus a general condition that is not leakage.**
  - *Leak 1a, pose targets, 5 of 25 Mpro structures.* p4, verbatim: "There were originally 25
    protein–ligand structures (but no affinities) to predict, but we report statistics only on
    20. This is because **we were informed on February 26, 2025, that the following five MPro
    structure targets had become available in the PDB well before the CASP16 submission
    deadline: L4006 (PDB ID 7gs2), 4007 (7grr), 4008 (7grw), 4009 (7grh), and 4010 (7gri). The
    statistics presented in this paper have been recomputed, relative to those presented at the
    CASP16 conference, with these targets omitted.**" This is a genuine route-1 leak: the
    answers were downloadable during the prediction window. It affects 5/229 = 2.2% of the pose
    set, all in one supertarget, and the reported statistics exclude them. **Note the timing:
    the leak was discovered in February 2025, after the CASP16 conference at which the original
    numbers were presented.** No per-target before/after comparison is given, so the size of
    the effect on the conference numbers is **NOT REPORTED**.
  - *Leak 1b, affinity targets, 18 of 140.* p12, verbatim: "during the assessment phase of this
    experiment, we rechecked the publication status of all of the protein–ligand data and
    discovered that **chymase affinity data for chymase affinity targets L1003 and L1010 had
    been previously disclosed in Roche patents [52–55] and that another group had published the
    chymase affinity associated with target L1013 [56]. In addition, the autotaxin affinity data
    for 15 CASP16 targets, L3009, L3047, L3196, L3197, L3211, L3213, L3214, L3216, L3217,
    L3219, L3222, L3224, L3225, L3226, and L3229, had been disclosed in the following Roche
    patents: US10647719, US2023/0312582 A1, US11098048, and US10800786.** Therefore, in
    preparing the assessment below, we omitted these three of the 17 chymase affinity targets
    and these 15 of the 123 autotaxin affinity targets, so the total number of affinity targets
    became 122." 18/140 = 13% of the affinity set. **This one has a control arm** (route 5,
    below).
  - *General condition, not leakage.* Related structures of all four main target proteins were
    in the PDB (similarity 0.3–0.9, p4) and every participant could and did use them. That is
    the challenge as designed, not a breach: **the specific complexes being predicted were not
    public** (deposition date May 3, 2024 with release after the deadline, p6), except for the
    five Mpro cases above.
  - *Baseline arm.* AD Vina's receptor and docking box came from a related holo PDB entry
    (p5–p6, quoted under `templates`), i.e. the binding-site location was supplied from prior
    structures — but not from the target's own structure. AF3/Boltz-1/RFAA received sequence +
    ligand + MSA only, as far as the Methods state.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving
  templates or alignments. NONE FOUND.** No conformational-state database of any kind appears
  in the paper. The only structural database operations are Foldseek fold search and SWISS-MODEL
  template selection (p5–p6), neither of which is state-annotated, and both of which are
  described in full in Sections 2.4 and 2.5 (p5–p6) so the absence is checkable. There is no
  conformational state to annotate: every answer is a holo crystal structure of an enzyme
  active site.

  **Route 3 — cluster labels derived from known states. NONE FOUND.** No clustering appears
  anywhere in the paper: not in the assessment (Sections 2.3, 2.5, p5–p6), not in the baselines
  (Section 2.4, p5–p6), not in the results. The 25 baseline models per system are not clustered;
  a single pose is used (p10).

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
  states or against the evaluation set. NONE FOUND, and the paper twice states the opposite
  explicitly. This is a positive rigour finding and should be quoted as such.**
  - p14, verbatim: "It should again be emphasized that **these calculations were run in a
    uniform manner with essentially no human intervention, and better results might be obtained
    with some tuning on, e.g., a subset of the ligands.**"
  - p10, verbatim: "Given the sensitivity of docking in general to methodological details, **we
    expect that AD Vina would perform better across the board if our procedure had been tuned
    (e.g., box size and location, exhaustiveness, treatment of protonation states) based on
    several targets for each supertarget.**"
  - Every baseline setting is a fixed default or a stated constant, not a swept range: AF3 and
    Boltz-1 "on one A100 40 GPU node each with 10 recycling steps, 200 diffusion sampling steps,
    5 seeds, and 5 diffusion samples per seed, which resulted in a total of 25 models per
    system for each method"; RFAA "with a number of MAXCYCLE set to 10"; AD Vina "using the
    default parameters; in particular, exhaustiveness was set to 8" with a 25 × 25 × 25 Å box
    (p5–p6). Same MSAs for AF3 and Boltz-1 "to ensure that the DNN methods were compared on an
    equal footing" (p5).
  - The one threshold in the paper, the 2.5 Å success cutoff, is **inherited from the prior
    literature, not fitted here**: p7, "we also defined a pose prediction as successful if
    RMSD ≤ 2.5 Å [46–50]", citing five external papers, and p15 restates it as a field norm:
    "the commonly used cutoff of 2.0–2.5 Å—values chosen because this quality of prediction is
    needed in CADD applications".
  - Metrics were inherited from CASP15 rather than designed against these results — BiSyRMSD
    and LDDT-PLI both cite ref [8], the CASP15 assessment, and the computation uses stock
    "OpenStructure [22] version 2.8" (p5). The one metric change from CASP15 is stated and is a
    tightening, not a loosening: "In contrast to CASP15, an additional penalty is applied to
    predicted ligand–protein contacts that are not present in the crystal structure [22]" (p5).

  **Route 5 — success defined post hoc by RMSD or a distance measure to a structure they had.
  PRESENT BY DESIGN — ASSESSOR-SIDE, POST-SEAL. This is what a blind assessment is, and v3 has
  no way to say so; see `unresolved` item 1.** The references were withheld from predictors and
  applied afterwards by the organisers. Three sub-choices were nonetheless made *after* the
  submissions were in hand and are recorded honestly:
  - *Sub-choice A: the skip penalty, chosen after inspecting the submissions.* p7: "Most groups
    included predictions for all or nearly all of the 229 pose prediction targets, but some
    included a more modest number of predictions (Figure S2A). **We thus had to consider whether
    and, if so, how to penalize omitted predictions.** As shown in Figure S2B, the distribution
    of mean accuracy across targets is about the same for groups that submitted few versus many
    predictions … **We therefore chose to favor groups that included predictions across most or
    all targets and penalize those that skipped targets.** To do this, we compute the
    skip-penalized mean LDDT-PLI of a given group as the mean of its LDDT-PLI values when
    skipped predictions are assigned an LDDT-PLI value of zero." The rule is stated, is
    coverage-based rather than result-based, and **both penalised and unpenalised versions are
    reported** (Figure 4 and Figure 5 use no penalty; Figures 3 and S8 do), which defuses the
    concern. But the decision was taken with all scores visible.
  - *Sub-choice B: the choice not to rank on binding-site accuracy, made after computing it.*
    p7: "We also computed a metric of the accuracy of predicted structures of the binding site
    itself, BB-RMSD (Section 2.4), but **ultimately chose not to rank participants on this
    metric**. This is because predictions with accurate ligand poses (i.e., low RMSD or high
    LDDT-PLI) also tend to have accurate binding site predictions (BB-RMSD). In particular, if
    ligand RMSD < X Å, then typically BB-RMSD < X also (Figure S1)." The justification is a
    measured redundancy, and the evidence (Figure S1) is in the unheld SI. **This is the single
    decision that erases receptor conformation from the assessment — see `state_metric`.**
  - *Sub-choice C: the best-scoring alternative is used wherever the answer is ambiguous.* p3:
    "Some crystal structures provided two alternate (hence partly occupied) ligand
    conformations … whereas others included two fully occupied ligand conformations … In such
    cases, we scored the agreement of the predicted ligand poses against all available
    conformations in the crystal structure and **used the best score** in computing performance
    statistics." Same for Mpro's two binding sites, p4: "We scored the agreement of all
    available predicted ligand poses against all available conformations in the crystal
    structure, accounting for symmetry, and **used the single best score**". And p5, for
    multi-chain/multi-copy cases: "all permutations were scored, and **we focused on the
    permutation with the best LDDT-PLI score**." Every one of these is a maximum over the
    answer's own degeneracy — a scoring convention, uniformly applied, favourable to all
    predictors equally.

  **Route 6 — best/worst model labels assigned against a held reference. PRESENT BY DESIGN —
  ASSESSOR-SIDE, POST-SEAL.** Two forms:
  - *Best-of-five.* p9: "we compare the mean skip-penalized LDDT-PLI statistic of each group's
    Model 1 submission with the corresponding mean of their best (highest LDDT-PLI) prediction
    for each target." The best-of-five label is assigned by the assessors against the answer,
    and the paper is careful to report Model 1 separately: "the mean skip-penalized LDDT-PLI
    across all groups rises from **0.30 to 0.37** on going from Model 1 to the best of Models
    1–5" (p9). Figure 3A (Model 1) and Figure 3C (best model) are both shown, and the ranking
    shuffles between them (p9).
  - *And critically, the participants' OWN reliability estimate is assessed separately and is
    the one place where the paper tests whether predictors can identify their own best model
    without the answer.* p4: "Participants were also invited to submit estimates of the
    reliability of each of their structural predictions. This is expressed as a number, called
    the LScore, in the range [0, 1]". Result, p14: "Participants were not particularly good at
    assessing the reliability of their pose predictions in advance, as evidenced by the
    generally low correlations between pose accuracy and LScore." **This is the anti-route-6
    control that `chitsazi2025gpcrdock4` was missing**, and CASP16 ran it (Figure 10, p14).

  **Route 7 — design-level oracle use (systems or conditions chosen because the expected answer
  is already known). NONE FOUND for the participant arm; PRESENT for the assessor baseline arm,
  and it is design-level only — weaker than pipeline leakage.**
  - *Participant arm: the inverse of route 7.* Targets were unpublished, unreleased pharma
    co-crystals contributed by Roche, Idorsia and the SGC (Table 1, p2), i.e. chosen because
    the answer was **unknown to the field**. The two known exceptions were removed (route 1).
    Nothing about the expected answer was declared in advance: the website gave "a brief
    description of the dataset; protein sequence; ligand SMILES string with any available
    stereochemical specifications; a statement of what was to be predicted … and, for structure
    predictions, a template protein PDB file with the coordinate fields filled with zeroes"
    (p4). Sequence + 2D ligand, nothing more.
  - *Assessor baseline arm: retrospective by the authors' own statement.* p10, verbatim: "**These
    calculations were not conducted in a blinded setting, so the outcomes cannot be viewed as
    true CASP results.** Nonetheless, we ascertained that the deep learning methods had not
    been trained on data unavailable to the CASP participants. In addition, the baseline methods
    were applied in an end-to-end, automated manner with minimal human input, so it is
    reasonable to compare them with the CASP group results." The answers were in hand when the
    baselines were run. Two concrete design-level items: (i) the AD Vina template had to contain
    "a ligand in the main known pocket" (p5) — the site location came from prior structure;
    (ii) the baselines were run on all targets **except L5001**, the one target with no known
    site (p10), and AF3 was then applied to L5001 as a deliberate probe *after* the main
    comparison — "We probed AF3 further by applying it to the solitary WDR55 target (L5001)"
    (p10). The probe is reported honestly and its result (LDDT-PLI 0.93) argues *against* the
    memorization hypothesis, but the run order is post hoc.
  - *One more design-level item, in the participant arm's favour and worth recording:*
    the organisers deliberately downgraded the incidental ligands rather than letting them
    inflate scores, p2: "we treated these predictions separately and regarded them as being of
    lower importance … such predictions are not representative of the main application of the
    prediction methods".

- **prospective**: **PARTIAL, and the partition is clean and lopsided — the participant
  assessment (34 groups, 229 pose targets, 122 affinity targets) is YES; the assessor baseline
  arm (AF3, Boltz-1, RFAA, AD Vina, and every affinity baseline) is NO, by the authors' own
  statement.**

  **Why YES for the participant arm, on the evidence rather than on the authors' word — the
  timeline, date by date, all from p4 unless marked:**
  | date | event | page |
  |---|---|---|
  | 2024-05-03 | PDB deposition date of the L1000, L2000, L3000 and L5000 datasets — used as the template cutoff for CASP participants | p6 |
  | 2024-05-05 | "The information needed for supertargets L1000–L4000 (chymase, cathepsin G, autotaxin, and Mpro) was posted May 5, 2024" | p4 |
  | 2024-07-21 | Stage 1 pose + affinity predictions due ("predictions were due by July 21, 2024") | p4 |
  | 2024-08-04 | deadline for resubmitting technically invalid files (format/SMILES checks only) | p4 |
  | 2024-08-07 → 08-21 | **Stage 2: experimental coordinates released**, affinities re-predicted with structures in hand. "we released experimental coordinates of protein–ligand complexes and asked modelers to predict binding affinities for each of them; note that in the first stage, the task was to predict affinities without the benefit of the experimental structures. Stage 2 ran from August 7 to August 21." | p4 |
  | 2024-08-09 | WDR55 (L5001) released to participants — "arrived at CASP later and was shared with participants on August 9, 2024" | p4 |
  | 2024-08-28 | L5001 predictions due | p4 |
  | 2024-08-30 | L5001 re-released as L5001v1 after a SMILES error was found | p4 |
  | 2024-09-18 | L5001v1 predictions due | p4 |
  | 2025-02-26 | organisers informed that five Mpro answers had been public before the deadline; statistics recomputed without them | p4 |
  | 2025-04-25 | manuscript received | p1 |

  **The blindness is therefore established by four independent facts, not by assertion:**
  (i) target information was posted 2024-05-05 and predictions closed 2024-07-21, a fixed
  77-day window; (ii) the experimental coordinates were withheld until 2024-08-07 and their
  release is itself an experimental variable — Stage 1 vs Stage 2 (p4); (iii) the PDB
  deposition date of the answers is 2024-05-03, two days before the challenge opened, with
  release after the deadline, and the organisers used that date as the participants' template
  cutoff (p6); (iv) when the organisers discovered that five answers had in fact been public,
  they removed them and recomputed (p4). Point (iv) is the strongest evidence of all, because
  it shows the blindness condition was audited rather than assumed.

  **Why NO for the baseline arm:** p10, "These calculations were not conducted in a blinded
  setting, so the outcomes cannot be viewed as true CASP results." The mitigation the authors
  offer is a training-cutoff argument, not a blindness argument: "we ascertained that the deep
  learning methods had not been trained on data unavailable to the CASP participants" (p10),
  backed by the cutoff dates on p6 (AF3/Boltz-1 2021-09-30; RFAA 2020-03-31 — all comfortably
  before the 2024-05-03 deposition).

  **The one gap.** The paper never states the *release* dates of the target structures, only
  the deposition date (2024-05-03) and the fact that five Mpro entries were public early. For
  the other 224 pose targets, "unreleased at prediction time" is inferred from the deposition
  date, the organisers' template cutoff, and the Stage-1/Stage-2 design — strong, but not a
  direct statement. See `unresolved` item 2.

- **state_metric**: **`RMSD-to-reference` + `continuous coordinate` — BUT THE OBJECT MEASURED
  IS THE LIGAND POSE, NEVER A PROTEIN CONFORMATIONAL STATE. Receptor conformation was
  DELIBERATELY NOT ASSESSED. This is the field to read if you came here for the state
  question.** See also `unresolved` item 5, where the negative is restated with its page.
  - **The explicit refusal, p4, verbatim:** "Our assessment of predicted protein–ligand
    structures focused on the accuracy of the ligand poses, that is, of their locations and
    conformations, and of the binding site structures. **We did not assess the accuracy of the
    overall protein structures because multiple crystal structures of these target proteins
    were already available in the PDB.**"
  - **What WAS measured about the receptor, and why it was then dropped.** Two receptor metrics
    exist and neither is used for ranking. p5: "The accuracy of each predicted binding site
    structure was evaluated in terms of the root-mean-square deviation of Cα atoms in the
    binding site (BB-RMSD [8]) and the differences in interatomic distances of all binding site
    atoms (LDDT-LP [8], for 'ligand pocket'). BB-RMSD and LDDT-LP are reported based on the
    best ligand RMSD." Then p7: "We also computed a metric of the accuracy of predicted
    structures of the binding site itself, BB-RMSD … but ultimately chose not to rank
    participants on this metric. This is because predictions with accurate ligand poses … also
    tend to have accurate binding site predictions (BB-RMSD). In particular, if ligand
    RMSD < X Å, then typically BB-RMSD < X also (Figure S1)." **No BB-RMSD or LDDT-LP number
    appears anywhere in the 18 pages** — the only evidence is Figure S1, which is not held.
  - **Primary pose metric 1 — BiSyRMSD**, p4–p5: "the binding-site superposed,
    symmetry-corrected, pose root-mean-square deviation (BiSyRMSD, here further abbreviated as
    RMSD) [8]. This is computed by defining binding site residues as any residue with heavy
    (non-hydrogen) atoms within **4 Å** of heavy atoms of the ligand, superimposing Cα atoms of
    those binding site residues of the predicted and crystallographic protein–ligand structures
    with the Kabsch algorithm [21], and then computing the root-mean-square distance between
    the predicted and crystallographic coordinates of corresponding ligand atoms. In case of
    symmetries, such as the 180° rotation of a phenyl group, we take the lowest root-mean-square
    distance achievable by the product of all symmetry operations. The best possible RMSD is 0,
    and there is no mathematical upper limit."
  - **Primary pose metric 2 — LDDT-PLI, the ligand-aware measure**, p5: "an enhanced version of
    the previously described local distance difference test for protein–ligand interactions
    (LDDT-PLI) score [8, 22]. The LDDT-PLI is obtained by computing the differences of
    interatomic distances between ligand atoms and binding site atoms in the crystal structure
    and the predicted complex. In contrast to CASP15, an additional penalty is applied to
    predicted ligand–protein contacts that are not present in the crystal structure [22]. The
    LDDT-PLI favorably scores the correct prediction of close ligand–protein contacts and ranges
    from **0** (no crystallographic contacts predicted correctly) to **1** (all crystallographic
    contacts predicted correctly)." LDDT-PLI is the primary ranking metric (Figure 3A).
  - **The one binary predicate, with a cited threshold**, p7: "we also defined a pose prediction
    as successful if **RMSD ≤ 2.5 Å** [46–50] (see sample structures with RMSD = 2.5 Å in Figure
    S3) and computed the skip-penalized success rate of a given submission by treating skipped
    targets as unsuccessful predictions." Justification is the CADD literature, restated on p15:
    "the commonly used cutoff of 2.0–2.5 Å—values chosen because this quality of prediction is
    needed in CADD applications." The two metrics agree: p7, "for all but the least accurate
    groups … the skip-penalized success rate and the LDDT-PLI score correlate extremely well",
    and "both metrics provide very similar rankings".
  - **Affinity metric**, p5: "ranking power, as measured by Kendall's τ statistic [23], because
    this allows all submissions—whether provided in terms of absolute, relative, or ranked
    affinities—to be compared against each other." Aggregated across the two affinity
    supertargets as the N-weighted κ_N = (N_A τ_A + N_C τ_C)/(N_A + N_C), with N_A = 108
    (autotaxin) and N_C = 14 (chymase) (p12).
  - **Nothing in this list is a state predicate.** There is no active/inactive, no
    open/closed, no DFG-in/out, no apo/holo comparison, and no second conformation of any target
    anywhere in the paper.

- **metric_saturation**: **YES for Kendall's τ, quantified by the authors themselves, and it is
  one of the paper's better contributions. NO for LDDT-PLI, which does not saturate at the
  observed values.**
  - **The τ ceiling is computed, not asserted**, p5: "even a computational method that yields
    perfect predictions will not give a perfect correlation with experiment because the
    experimental data are subject to error. We used a common estimate that the experimental
    IC50 data could be off by about a factor of 3, which corresponds to a binding free energy of
    DG = RT ln (3) = **0.66 kcal/mol** at room temperature … we converted the experimental IC50
    data into estimated binding free energies … and used resampling to generate **1000** new
    datasets with added experimental error drawn from a Gaussian distribution with a mean of 0
    and a standard deviation of 0.66 kcal/mol. We computed Kendall's τ for each resampled data
    set against the actual experimental data set and determined its mean and standard deviation.
    **The mean represents the highest value of Kendall's τ that even a perfectly accurate
    computational method is expected to achieve.**"
  - **The ceilings, p13:** chymase **0.54 (SD 0.11)**; autotaxin **0.76 (SD 0.02)**;
    N-weighted **0.73**. Observed maximum 0.39 (Figure 8A/9), so the *aggregate* metric has
    headroom: "This is well above the maximum achieved value of 0.39 (Figure 9A), so there is
    still considerable room for improvement in this challenge component."
  - **But chymase specifically is saturated, and the authors say so plainly, p13, verbatim:**
    "Note that the fact that CASP participants came close to the theoretical maximum value of
    Kendall's τ for chymase does not imply that these predictions were more successful, only
    that **the chymase challenge is less capable of resolving levels of accuracy**, due, again,
    to the small range of experimental data." Cause, p13: "the IC50s for chymase vary over a
    much smaller range (400×) than those for autotaxin (8700×), and a larger range makes the
    ranking more stable in the face of 3× experimental uncertainty." **This is a real ceiling on
    a real arm and must not be dropped when quoting the chymase numbers.**
  - **The ceiling is then inverted into an error estimate**, p13–p14: "if we assign an error of
    30× in IC50 (2 kcal/mol in binding free energy), we obtain a mean expected best Kendall's τ
    of **0.43** for autotaxin, which is similar to the best result in Figure 8A. This suggests
    that the best affinity prediction method has an effective uncertainty of **~2 kcal/mol** in
    binding free energy." Elegant, and reusable as a comparator.
  - **LDDT-PLI does not saturate** at the observed values: best group 0.69, best baseline 0.80,
    highest single per-supertarget value 0.88 (AF3 on chymase, Table 2 p11), highest single
    target 0.93 (AF3 on WDR55, p10), all short of 1.0. The upper part of the range is populated
    but not compressed.
  - **Figure axis truncations are recorded in `hides` (Figure 4 row), not here**, per v3 rule 9.

- **directional_control**: **NONE — there is no conformational-state handle in this paper, and
  the concept does not apply.** No partner, no nanobody, no state-annotated template, no
  state-filtered MSA, no seed-steering. The only inputs a predictor receives are the protein
  sequence, the ligand SMILES with stereochemistry where available, and a statement of what to
  predict (p4). The one deliberate information manipulation in the whole design is the
  **Stage 1 → Stage 2 transition**, in which the organisers hand over the experimental complex
  coordinates and ask for affinities again (p4) — a handle on *information available*, not on
  *state produced*, and its result is a null (see `controls_run`). Baseline-side, the only
  directional element is AD Vina's docking box, centred on the template's ligand (p6), which
  directs *where* to search but not *which state*.

- **anti_memorization_design**: **PRESENT and multi-layered — the strongest such design in the
  corpus after `chitsazi2025gpcrdock4`, and stronger in one respect (it caught its own leaks).
  Four layers, with n for each:**
  1. **The blind window itself.** 229 pose targets and 140 affinity targets whose answers were
     unreleased between 2024-05-05 and the deadlines (p4, timeline above). n = 229 / 140.
  2. **Post-hoc leakage audit and excision.** 5 pose targets removed after PDB release was
     discovered (p4); 18 affinity targets removed after patent/paper disclosure was discovered
     (p12). n removed = 5 pose, 18 affinity; n retained = 229 pose (already excluding the 5 from
     the original 25 Mpro), 122 affinity.
  3. **Training-cutoff verification for the DNN baselines.** p6: AF3 and Boltz-1 cutoff
     2021-09-30, RFAA cutoff 2020-03-31, all used as the template cutoff for the similarity
     analysis; p10: "we ascertained that the deep learning methods had not been trained on data
     unavailable to the CASP participants." n = 3 methods.
  4. **A quantified prior-similarity coordinate for every target.** Section 2.5 (p6): Foldseek
     fold search + SuCOS shape/pharmacophore overlap × pocket coverage → a 0–1 similarity score
     per target, computed against the PDB *as of each method's cutoff date*. This turns
     "memorization" from a suspicion into an axis that can be plotted, which is what Figures 6C
     and 7 then do. n = 229 targets.
  5. **One genuinely novel system**, WDR55: "did not have a known, well-characterized binding
     site" and similarity score 0.0 (p4). **n = 1.**

- **anti_memorization_control**: **RUN, and analysed, in four separate arms — and the headline
  result is a NULL that cuts against the memorization hypothesis. But the arm that matters most
  is UNPOWERED (n = 1).**
  - **Arm 1 — baseline accuracy vs PDB similarity, per target, four methods (Figure 7, p12).
    RUN. Result: no correlation.** p10, verbatim: "Because the deep-learning methods are trained
    on structural data in the PDB, we speculated that the accuracy of their predictions would
    correlate with the similarity of the individual target pose to that of the most similar
    co-crystal structure in the PDB. **However, this is not the case, as shown in Figure 7,
    which also demonstrates the same lack of correlation for AD Vina.**" n = ~220–224 targets
    per panel. **No R² or correlation coefficient is reported for this claim** — see the Figure
    7 `hides` entry and `unresolved` item 6.
  - **Arm 2 — participant accuracy vs PDB similarity (Figure 6C, p11). RUN. Result: weak
    positive.** p10: "we conjectured that ligands with higher similarity to those available to
    participants in the PDB would be easier to predict, and there is a correlation between the
    SuCOS similarity score (Section 2.5) and the mean best pose accuracy, but the correlation is
    not strong, as indicated by a **coefficient of determination of 0.25**". n = 229.
  - **Arm 3 — the zero-similarity target, WDR55. RUN. Result: a strong pass, on n = 1.** p10,
    verbatim: "We probed AF3 further by applying it to the solitary WDR55 target (L5001), for
    which there was no previously defined binding site and no structure in the PDB with a
    similarity score (Section 2.5) above 0. **Remarkably, AF3 not only placed the ligand in the
    correct general location but also accurately replicated the crystallographic pose, with
    LDDT-PLI of 0.93 and RMSD of 0.48 Å.**" Set against this: WDR55 was among the *worst*
    targets for the CASP participants — p10, "The average performance on WDR55 is among the
    worst, presumably because of the novelty of this system (Section 2.1)." **Mark UNPOWERED:
    n = 1 target, one method, and the two halves of the WDR55 result point in opposite
    directions.**
  - **Arm 4 — the leakage-removal sensitivity check. RUN, reported only in the unheld SI.**
    p12: "for completeness, Figure S10 in the SI provides an assessment based on all 17 chymase
    and 123 autotaxin targets, and **the results are much the same as those computed without the
    previously disclosed cases**." The corresponding check for the 5 removed Mpro pose targets
    is **NOT REPORTED** — the paper says only that statistics were recomputed (p4), not by how
    much they changed.

- **controls_run**: every control arm the paper actually ran.

  | control | what it rules out | page |
  |---|---|---|
  | AF3 / Boltz-1 / RFAA / AD Vina run end-to-end on all 229 targets except L5001, scored identically to participants | that the participants' accuracy is the field's ceiling; establishes an automated floor and ceiling for the same targets | p5, p10, Table 2 p11 |
  | Same MSAs given to AF3 and Boltz-1 | that the AF3 > Boltz-1 gap is an MSA artefact | p5 |
  | Training-cutoff dates checked for all three DNN baselines against the 2024-05-03 deposition | that the baselines were trained on the answers | p6, p10 |
  | Baseline accuracy vs max PDB structural similarity, per target, all four baselines (Figure 7) | that co-folding accuracy is explained by similarity to a memorised co-crystal | p10, p12 |
  | Participant accuracy vs SuCOS similarity (Figure 6C, R² 0.25) | same, on the blind arm | p10, p11 |
  | AF3 applied to WDR55, the zero-similarity, no-known-site target | that AF3 fails outside its training distribution — n = 1 | p10 |
  | Removal of 5 Mpro pose targets found to be public before the deadline; all statistics recomputed | that the pose result rests on non-blind targets | p4 |
  | Removal of 18 affinity targets disclosed in patents/papers; **Figure S10 repeats the analysis with them included** | that the affinity result rests on disclosed data | p12 |
  | Stage 1 (no structures) vs Stage 2 (experimental co-crystals given) affinity prediction, same groups, same ligands (Figure 8B,C) | that affinity error is driven by pose error rather than by the scoring function | p4, p14 |
  | AD Vina rescoring of the *crystallographic* poses in Stage 2 vs docking in Stage 1 | same, on the baseline side — and it came out worse: "scoring crystallographic poses with AD Vina in Stage 2 gave lower accuracy than docking and scoring with AD Vina in Stage 1" | p6, p14 |
  | Trivial affinity baselines: molecular weight and cLogP | that a nontrivial method is needed to reach the observed τ — MolW (τ 0.37) nearly matches the best CASP group (0.39) | p6, p14, Fig 9 p14 |
  | Classical ML affinity baseline: Gaussian process regressor + Tanimoto kernel on ChEMBL (1110 chymase, 450 autotaxin IC50s) | that structure-based scoring beats a ligand-only regression | p6, p14 |
  | GNINA v1.3 scoring of the true complexes (Stage 2) | that a modern DNN scoring function fixes affinity given a perfect pose | p6, Fig 9 p14 |
  | Resampling with 0.66 kcal/mol (3×) and 2 kcal/mol (30×) experimental error, 1000 replicates | that the observed τ gap is method error rather than experimental noise; sets the τ ceiling per dataset | p5, p13 |
  | Best-of-Models-1–5 vs Model 1 across all groups (0.30 → 0.37) | that groups are being penalised for a bad model-1 choice; also quantifies within-group spread | p9, Fig 3A vs 3C p8 |
  | Number-of-predictions vs mean accuracy per group (Figure S2B) | that the skip penalty is masking genuinely selective, accurate groups | p7 |
  | BB-RMSD vs ligand RMSD (Figure S1) | that ranking on ligand pose alone hides bad binding-site geometry | p5, p7 |
  | Cross-supertarget consistency of group accuracy (R² 0.46, 0.53, 0.61; Figure S5) | that a group's ranking is a single-target fluke | p7 |
  | Two independent pose metrics (LDDT-PLI and RMSD ≤ 2.5 Å success rate) ranked side by side (Figure 3A vs 3B; Figure S4) | that the ranking is a metric artefact | p7, p8 |
  | Incidental (non-drug-like) ligands scored and reported separately (Figure S8) | that easy cosolvent placements inflate the headline drug-like scores | p2, p11 |
  | LScore (participant self-confidence) vs LDDT-PLI, Kendall's τ, 10 groups + AF3 pLDDT (Figure 10) | that predictors can identify their own good models without the answer — they largely cannot | p4, p14 |
  | Ligand size, rotatable-bond count and affinity vs accuracy (Figure 6A,B,D; R² 0.1, ~0.1, 0.07) | that the accuracy spread is explained by ligand complexity or potency | p10, p11 |
  | Comparison of RMSD distributions against D3R Grand Challenges 2/3/4 in D3R's own plot format (Figure 4) | that CASP16's difficulty is incomparable to the prior challenge series — though the authors decline to draw a conclusion | p7–p8, p9 |

- **confidence_as_discriminator**: **YES — and this is one of only a handful of papers in the
  corpus that both uses a confidence score and validates it. The validation is a mostly
  negative result.**
  - **The participant-side score.** p4: "Participants were also invited to submit estimates of
    the reliability of each of their structural predictions. This is expressed as a number,
    called the LScore, in the range [0, 1], where 0 means low reliability, and 1 means high
    reliability." Uptake was poor and the data were partly unusable, p6: "**Only 13 groups
    provided LScores with their pose predictions. Of these, three groups submitted only LScore
    values of 1, and one group submitted negative (hence out of range) LScore values, so we
    analyzed only the remaining 10 submissions.**"
  - **The validation.** p5: "The reliability estimates (LScores, Section 3.3) were evaluated in
    terms of the correlation between the LScore and the LDDT-PLI of each structural prediction.
    Thus, we hope to see greater accuracy for predictions considered more reliable. The
    correlation between LScore and LDDT-PLI across structure predictions was summarized with
    Kendall's τ ranking statistic."
  - **The result, p14:** "few groups provided LScores, and of these, HADDOCK (8) performed
    relatively well, while the other correlations were rather modest. Interestingly,
    **AlphaFold 3 performed best, with a Kendall's τ of 0.53, when we interpreted pLDDT from
    AlphaFold 3 as LScore.**" Figure 10 values (read from the rendered figure, p14): AF3 0.53,
    HADDOCK (8) 0.43, McGuffin (164) 0.29, Bryant (32) 0.24, MULTICOM_ligand (207) 0.19,
    haiping (16) 0.11, Zou (204) 0.11, Zou_af2 (420) 0.11, Koes (309) 0.06, CoDock (262) 0.04,
    GrominhaLab (272) **−0.16**.
  - **pLDDT specifically as the discriminator**: p5, "For AlphaFold 3, we used the average
    per-atom pLDDT of the ligand, as provided by AlphaFold 3, as a proxy for LScore." So the
    best confidence-as-discriminator result in the paper is **ligand pLDDT, τ = 0.53** — a
    genuine but far-from-decisive ranking signal.
  - **Verdict sentence, p14:** "Participants were not particularly good at assessing the
    reliability of their pose predictions in advance, as evidenced by the generally low
    correlations between pose accuracy and LScore." And p15: "Users of pose- and
    affinity-prediction methods would presumably value some indication of the reliability of the
    predictions, so this would appear to be an important—if difficult—direction for future
    research."

## D. Claims

- **central_conclusion**: In the first CASP round to assess drug-like ligand poses *and*
  affinities, 30 labs (34 pose groups) submitted predictions for 229 pose targets and 140
  affinity targets across five pharma-derived protein systems; **the best pose predictions all
  came from at least partly template-based methods** (best skip-penalized mean LDDT-PLI 0.69),
  while an **assessor-run, non-blind AlphaFold 3 baseline scored higher still (0.80)** than any
  blind participant. Affinity prediction was **modest** (best N-weighted Kendall's τ 0.39
  against a noise-imposed ceiling of 0.73) and, as in the D3R challenges, **did not improve when
  the experimental structures were handed to participants in Stage 2**, which the authors read
  as evidence that the scoring functions, not the poses, are the binding constraint.

- **necessity_claims**: verbatim, with pages.
  - **On blindness being what makes an assessment valid (the paper's opening rationale), p1:**
    "By forcing 'blinded' predictions made without knowledge of the experimental results, CASP
    went beyond the prior practice, in which protein structure prediction methods were typically
    evaluated against protein structures that had already been published, **an approach that,
    even when done with care, risks tilting the predictions toward the known results.**"
  - **On the baseline arm not counting as a blind result, p10:** "**These calculations were not
    conducted in a blinded setting, so the outcomes cannot be viewed as true CASP results.**"
  - **On what limits affinity prediction — the paper's second headline, stated twice.** p1
    (abstract): "As seen in prior challenges, providing experimental structures did not improve
    affinity predictions in the second stage of the challenge, **suggesting that the scoring
    functions used here are a key limiting factor.**" p15 (Conclusions): "Access to experimental
    structures in Stage 2 did not improve affinity predictions, consistent with observations in
    the prior D3R challenges and **suggesting that current scoring models are a key limiting
    factor in affinity prediction accuracy.**"
  - **On an impossibility that shaped the challenge, p10:** "Note that, during the challenge
    period, **the publicly available version of AF3 was not able to run this challenge because
    it could not co-fold a protein with an arbitrary ligand, only one of a small set of
    ligands.**" And p5: "**AlphaFold 3 and Boltz-1 were not publicly available in a form
    suitable for protein–ligand pose predictions during the actual challenge, so these methods
    could not be used by CASP16 participants.**"
  - **On the impossibility of a perfect correlation, p5:** "**even a computational method that
    yields perfect predictions will not give a perfect correlation with experiment because the
    experimental data are subject to error.**"
  - **On what the chymase numbers cannot mean, p13:** "Note that the fact that CASP participants
    came close to the theoretical maximum value of Kendall's τ for chymase **does not imply that
    these predictions were more successful, only that the chymase challenge is less capable of
    resolving levels of accuracy**, due, again, to the small range of experimental data."
  - **On the accuracy the field actually needs, p15:** "there seems to be little ambiguity in
    defining this field's ultimate goal of achieving near 100% success in predicting poses to
    within the commonly used cutoff of 2.0–2.5 Å—**values chosen because this quality of
    prediction is needed in CADD applications.**"
  - **A refusal to conclude, twice — useful because it is the opposite of an overclaim.** p8:
    "Due to the large variation across protein targets, here and in D3R, as well as the modest
    number of targets, **we find it difficult to conclude that the present results are better or
    worse than the prior ones.**" p15: "**it is not clear that the CASP16 pose-prediction
    results reflect significant methodological improvement since D3R**, especially given that
    the protein–ligand targets were different and that there was considerable target-to-target
    variation even within a single challenge."
  - **A procedural requirement, p4:** "Structure predictions **were required to** include
    three-dimensional coordinates of the protein in PDB format and three-dimensional coordinates
    of the ligand in MDL molfile format **in order to avoid ambiguity regarding atom identities
    and connectivity.**"

- **novelty_claims**: verbatim, with pages. All four are "first within CASP" claims, carefully
  scoped, and none claims priority over the D3R/CSAR/SAMPL series — the paper explicitly places
  itself in that lineage (p2: "CASP's entry into this field is timely because these prior
  challenges are, at best, in abeyance").
  - **p2:** "In particular, **CASP 15 (2022) was the first cycle that challenged participants to
    predict the three-dimensional structures of protein–small molecule (also called
    protein–ligand) complexes [7, 8].**" (about the prior round, not this one)
  - **p2:** "In addition, **CASP 16 for the first time introduces a self-assessment aspect to
    ligand pose predictions.**"
  - **p14 (Discussion, opening sentence):** "**This first CASP challenge to include pose and
    affinity predictions for drug-like ligands** attracted a strong pool of participants (30
    labs) deploying a range of different methods (34 CASP groups)."
  - **p15 (Conclusions, opening sentence):** "**The CASP16 protein–ligand challenge summarized
    here represents the first assessment of pose and affinity predictions for drug-like
    compounds within the CASP framework.**"

- **stated_limits**: the authors' own, and they are unusually forthcoming.
  1. **Ranking is target-set dependent**, p14: "a challenge based on different targets would
     undoubtedly have led to a somewhat different ranking among the higher-performing methods,
     if only due to chance."
  2. **The targets are too well characterised to test generalization**, p14: "This outcome may,
     again, reflect the fact that the main protein targets here are already well represented in
     the PDB. In future challenges, we hope that some less well-characterized systems may be
     included among the targets in order to better probe the generalizability of pose-prediction
     methods to novel drug discovery targets." Repeated in Conclusions, p15.
  3. **The baselines are not blind results**, p10 (quoted above).
  4. **The baselines are untuned and would do better if tuned**, p10 and p14 (quoted under
     `oracle_leakage` route 4).
  5. **The most accurate class of affinity method never entered**, p6: "physics-based modeling
     (though none used the highly regarded approach of simulation-based free energy calculations
     [44, 45])", and p15: "As a number of computational methods currently used in industrial
     drug discovery did not appear in CASP 16, it would be helpful to the field if a wider set
     of methods could be applied by experienced users in future rounds. For example, although
     simulation-based free energy methods are time-consuming, they can be quite accurate and,
     indeed, did particularly well in the last D3R challenge [14]."
  6. **No progress claim against D3R**, p8 and p15 (quoted under `necessity_claims`).
  7. **The chymase affinity challenge cannot resolve accuracy**, p13 (quoted under
     `metric_saturation`).
  8. **The autotaxin supertarget dominates every aggregate**, Table 2 footnote p11: "Autotaxin,
     with 189 targets, dominates the overall averages."
  9. **The Boltz-1/autotaxin anomaly is unexplained**, p10: "It is not yet clear why Boltz-1
     yields results similar to AF3 for chymase, cathepsin G, and Mpro but underperforms for
     autotaxin, but we were able to confirm this result with the developers of Boltz-1 (data not
     shown)."
  10. **Descriptor baselines are unreliable rather than good**, p14: "Thus, although these
      descriptors sometimes do very well, they are unreliable."
  11. **Too few groups submitted usable confidence scores**, p6 (13 → 10) and p14.
  12. **No distinguishing feature was found for easy vs hard ligands**, p10: "we inspected the
      ligands that received the highest and lowest mean accuracy across submissions (Figure S7)
      but did not discern any obvious distinguishing characteristics of the two sets."

- **stance**: **`precedent` + `background`** — provisional, the user's call.
  - **`precedent`, on assessment design.** This is one of only two genuinely blind, prospective
    community assessments in the corpus (with `chitsazi2025gpcrdock4`), and it is the more
    rigorous of the two on four counts: it audited its own blindness and removed the targets
    that failed (p4, p12); it ran an anti-memorization control with a quantified similarity axis
    (Figures 6C, 7); it ran a confidence-calibration control (Figure 10); and it computed the
    noise-imposed ceiling on its own metric (p13). Any claim we make about what a blind
    evaluation should look like can cite this paper's protocol.
  - **`background`, on the conformational-state question.** The paper contains no conformational
    state axis at all: one state per target, receptor accuracy computed and then deliberately
    dropped from the ranking (p4, p7). It cannot support or contradict any state claim.
  - **Not `contrast` and not `threat`:** the paper's rigour exceeds, rather than challenges,
    the corpus norm, and its subject (ligand pose in enzyme active sites) does not overlap ours.
    The one place it could read as a threat is the template-based finding — a blind competition
    concluding that PDB-derived templates win is an argument about memorization versus de-novo
    prediction — but that argument is *supportive* of the corpus's memorization thread
    (`swapna2025memorization`, `skrinjar2026generalization`, `zhang2026generalization`), not
    opposed to it, and the paper's own control (Figure 7) declines to confirm the simplest
    memorization story. See `unresolved` item 7.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | LDDT-PLI, skip-penalized mean, Model 1 — **best CASP group (ClusPro, group 494)** | **0.69** | 0–1, 1 best | crystallographic ligand–binding-site contacts, 229 pose targets | p1 (abstract), Fig 3A p8, Table 2 p11 |
  | LDDT-PLI, skip-penalized mean, Model 1 — 2nd (kozakovvajda, 274) | 0.69 | 0–1 | same | Fig 3A p8 |
  | LDDT-PLI, skip-penalized mean, Model 1 — 3rd–10th (CoDock 262 / Huang-HUST 91 / MULTICOM_ligand 207 / DIMAIO 432 / Zou_af2 420 / LCDD-team 55 / Zou 204 / SNU-CHEM-lig 408) | 0.60 / 0.59 / 0.59 / 0.56 / 0.54 / 0.52 / 0.51 / 0.46 | 0–1 | same | Fig 3A p8 |
  | LDDT-PLI, skip-penalized mean, Model 1 — worst groups | 0.02 … 0.00 | 0–1 | same | Fig 3A p8 |
  | LDDT-PLI, mean across all groups — Model 1 → best of Models 1–5 | **0.30 → 0.37** | 0–1 | same | p9 |
  | LDDT-PLI, skip-penalized mean, best model — best group (kozakovvajda 274, then ClusPro 494) | 0.73 / 0.73 | 0–1 | same | Fig 3C p8 |
  | Skip-penalized RMSD success rate (RMSD ≤ 2.5 Å), Model 1 — best group (ClusPro 494) | **0.62** | fraction of 229 | BiSyRMSD to crystal ligand | Fig 3B p8 |
  | Skip-penalized RMSD success rate — 2nd–4th (kozakovvajda 274 / Huang-HUST 91 / CoDock 262) | 0.61 / 0.56 / 0.52 | fraction | same | Fig 3B p8 |
  | **AF3 baseline, skip-penalized mean LDDT-PLI, all supertargets** | **0.80** | 0–1 | same targets, non-blind | p1, p10, Table 2 p11 |
  | Boltz-1 baseline | **0.53** (Table 2) / **0.52** (text p10) — see `unresolved` 8 | 0–1 | same | p10, Table 2 p11 |
  | RFAA baseline | 0.37 | 0–1 | same | p10, Table 2 p11 |
  | AD Vina baseline | 0.38 | 0–1 | same | p10, Table 2 p11 |
  | AF3 per supertarget (chymase / cathepsin G / autotaxin / Mpro) | 0.88 / 0.87 / 0.81 / 0.63 | 0–1 | same | Table 2 p11 |
  | Boltz-1 per supertarget | 0.87 / 0.84 / 0.48 / 0.60 | 0–1 | same | Table 2 p11 |
  | RFAA per supertarget | 0.37 / 0.19 / 0.38 / 0.31 | 0–1 | same | Table 2 p11 |
  | AD Vina per supertarget | 0.57 / **0.85** / 0.36 / 0.38 | 0–1 | same; the cathepsin G value is the paper's docking outlier, n = 2 targets | p10, Table 2 p11 |
  | ClusPro (494) per supertarget | 0.72 / 0.76 / 0.68 / 0.72 | 0–1 | same; the most *consistent* profile in Table 2 | Table 2 p11 |
  | AF3 on WDR55 (L5001), the zero-PDB-similarity target | LDDT-PLI **0.93**, RMSD **0.48** | 0–1; Å | crystal structure; n = 1 target | p10 |
  | Baseline omitted/failed predictions (AF3 / Boltz-1 / RFAA / AD Vina) | 5 / 9 / 7 / 5 | targets, scored as LDDT-PLI 0 | of 228 (L5001 excluded); includes all 4 covalent Mpro ligands for every method | p10 |
  | Per-supertarget mean best LDDT-PLI across groups (chymase / cathepsin G / Mpro) | 0.62 / 0.49 / 0.57 | 0–1 | red bars of Fig 5; autotaxin and WDR55 values not given in text | p10 |
  | Covalent Mpro ligands, mean scores | 0.48, 0.51, 0.51, 0.58 | LDDT-PLI | "their mean scores are unremarkable" | p10 |
  | Targets where the *average* group exceeded LDDT-PLI 0.6 | **17% (28/229)** | fraction of targets | mean across groups | p10 |
  | Targets where the *best submitted* model exceeded LDDT-PLI 0.6 / 0.7 | **98% (224/229)** / 94% | fraction of targets | best of all models of all groups | p10 |
  | Incidental-ligand pose accuracy, best group (skip-penalized mean LDDT-PLI, Model 1) | **0.39** vs 0.69 for drug-like | 0–1 | 18 Model-1 submissions; Figure S8 not held | p11 |
  | **Affinity: best N-weighted Kendall's τ (κ_N), Stage 1 — Haiping (group 16)** | **0.39** | −1 to 1 | experimental IC50 ranking, 122 targets (108 autotaxin + 14 chymase) | p12, Fig 8A p13 |
  | Affinity: abstract's stated maximum Kendall's τ | **0.42** — does not match the 0.39 in text/Fig 8A; see `unresolved` 8 | −1 to 1 | — | p1 |
  | Affinity: groups with κ_N > 0.25 (LCDD-team 55 / MULTICOM_ligand 207 / VnsDock 82 / Zou 204 / HADDOCK 8) | 0.33 / 0.29 / 0.29 / 0.29 / 0.25 | −1 to 1 | same | p12, Fig 8A p13 |
  | Affinity: worst group (DIMAIO 432) | −0.23 | −1 to 1 | same | Fig 8A p13 |
  | **Theoretical maximum Kendall's τ given 3× IC50 error** — chymase / autotaxin / N-weighted | **0.54 (SD 0.11) / 0.76 (SD 0.02) / 0.73** | −1 to 1 | 1000 resamples at σ = 0.66 kcal/mol | p13 |
  | Theoretical maximum τ given 30× IC50 error (autotaxin) | 0.43 | −1 to 1 | 1000 resamples at σ = 2 kcal/mol | p13 |
  | Implied effective uncertainty of the best affinity method | **~2** | kcal/mol | inverting the resampling analysis | p14 |
  | Baseline affinity predictors, N-weighted Kendall's τ (MolWeight S1 / GPR S1 / GNINA score S2 / AD Vina S1 / AD Vina score S2 / cLogP S1) | 0.37 / 0.27 / 0.13 / 0.13 / 0.04 / **−0.07** | −1 to 1 | same experimental IC50 ranking | Fig 9 p14 |
  | D3R comparator: best Stage 1 result across Grand Challenges | mean 0.48 (min 0.21, max 0.71) | Kendall's τ | prior blinded challenges | p15 |
  | D3R comparator: participating labs in GC2 / GC3 / GC4 | 49 / 28 / 51 | labs | — | p15 |
  | LScore↔LDDT-PLI Kendall's τ: AF3 (ligand pLDDT) / HADDOCK 8 / McGuffin 164 / Bryant 32 / MULTICOM 207 / haiping 16 / Zou 204 / Zou_af2 420 / Koes 309 / CoDock 262 / GrominhaLab 272 | **0.53** / 0.43 / 0.29 / 0.24 / 0.19 / 0.11 / 0.11 / 0.11 / 0.06 / 0.04 / −0.16 | −1 to 1 | all models, no skip penalty | p14, Fig 10 p14 |
  | Correlates of pose accuracy, R²: ligand heavy-atom count / rotatable bonds / SuCOS PDB similarity / log IC50 | ~0.1 / ~0.1 / **0.25** / 0.07 | R² | mean best LDDT-PLI per target across groups | p10, Fig 6 p11 |
  | Cross-supertarget consistency of group accuracy, R² | 0.46, 0.53, 0.61 | R² | pairs of supertargets, Figure S5 | p7 |
  | Target prior-similarity to the PDB | 0.3–0.9 for the four main supertargets; **0.0** for WDR55 | 0–1 similarity | SuCOS × pocket coverage vs PDB at the relevant cutoff date | p4, p6 |
  | Crystallographic resolution of the answers | 1.1–2.7 | Å | X-ray; per-supertarget means 1.7 / 1.2 / 1.9 / 1.7 / 1.2 | Table 1 p2 |
  | Experimental affinity ranges | chymase 1–400 nM (400×); autotaxin 1 nM–10 μM (8700×) | IC50 | Table 1; dynamic range restated p13 | p2, p13 |
  | ChEMBL training data for the GPR affinity baseline | 1110 chymase IC50s (0.3 nM–570 μM); 450 autotaxin IC50s (10 pM–1.25 mM) | assay values | ChEMBL accessed 2024-12-05 | p6 |

- **n_predictions**: **record the three levels separately; a single total does not exist in this
  paper.**
  - **Targets.** Pose: **229** (chymase 17, cathepsin G 2, autotaxin 189, Mpro 20, WDR55 1) —
    Table 1 p2, confirmed p7. Affinity: **140** posed → **122** assessed (108 autotaxin + 14
    chymase) → **103** in Stage 2 (89 autotaxin + 14 chymase) — p2, p12, p14. Incidental-ligand
    targets: **NOT REPORTED**.
  - **Groups.** 30 research **labs** participated (p6, p14, p15). **34 CASP pose-prediction
    groups** for pharmaceutical ligands and **19** for incidental ligands (p6) — but only **18
    Model 1 submissions** for incidental ligands were received (p11); see `unresolved` 9.
    Affinity Stage 1: **28** groups for chymase, **21** for autotaxin; Stage 2: **27** and
    **24** (p6, and Figure 8 caption p13). "We received Stage 1 affinity predictions from 28
    groups" (p12) — **but Figure 8A shows only 26 bars** (read from the rendered figure); see
    `unresolved` 9. LScores: **13** groups submitted, **10** analysable (p6). Note p4: "sometimes
    a lab wishes to test more than one method, and CASP provides a mechanism for this through
    multiple group registrations from the same lab … it should be understood that more than one
    'group' may be associated with a given lab."
  - **Models per target.** Up to **5** per group per target (Model 1 … Model 5), "with the
    understanding that Model 1 would be considered their best or most favored prediction" (p4).
  - **Per-group prediction counts** are printed on the figure axes: Figure 3 labels run from 229
    (full coverage: ClusPro, kozakovvajda, MULTICOM_ligand, DIMAIO, LCDD-team, CoDock,
    PocketTracer) down to 2 (UNRES 261) — Fig 3 p8. Figure 10 labels give totals across all
    models, up to **1295** (McGuffin, MULTICOM_ligand, CoDock) and as few as 22 (GrominhaLab) —
    Fig 10 p14. Figure 8A labels give affinities ranked per group, mostly 108, with several
    groups at 0 — Fig 8A p13.
  - **Total number of submitted models across the whole challenge: NOT REPORTED.** The paper
    never states it. (Arithmetic note, flagged as the extractor's inference and not the paper's:
    1295 = 5 × 259, and 259 = 229 drug-like + 30 further targets, which would be the incidental
    set; do not cite this as the paper's number.)
  - **Baselines.** AF3 and Boltz-1: "10 recycling steps, 200 diffusion sampling steps, 5 seeds,
    and 5 diffusion samples per seed, which resulted in a total of **25 models per system** for
    each method", one A100 40 GB node each (p5). RFAA: MAXCYCLE 10 (p5). AD Vina: default
    parameters, exhaustiveness 8, 25 × 25 × 25 Å box, "The best pose was selected based on the
    docking score" (p6). All four run on **228** targets (all but L5001), with 5/9/7/5 failures
    respectively; AF3 additionally run on L5001 as a probe (p10). **How the single reported pose
    was selected from the 25 co-folding models is NOT REPORTED** — see `unresolved` 4.
  - **Resampling.** 1000 synthetic datasets per affinity supertarget for the τ-ceiling estimate
    (p5).

- **comparable_to_ours**: *(left empty by the extractor, per schema v3)*

- **si_in_scope**: **SI NOT HELD — and it holds five things this note would otherwise be able to
  quote.** The Supporting Information manifest is on p17–p18; none of the items is in the PDF.
  1. **Table S2 — "Skip-penalized mean LDDT-PLI results for Model 1 predictions of all groups
     and supertargets."** Referenced at p7. This is the per-group × per-supertarget matrix; the
     main text gives only the "All" column (Figure 3A) plus the five-row Table 2. **Without it,
     no per-supertarget participant number can be quoted except the three on p10.**
  2. **Figure S10 — the affinity assessment recomputed with the 18 previously-disclosed targets
     included.** Referenced at p12. This is the paper's own leakage control and its result is
     stated in one clause ("the results are much the same") with no numbers.
  3. **Figure S8 — incidental-ligand accuracy by group.** Referenced at p11; only the maximum
     (0.39) reaches the main text.
  4. **Figure S1 — ligand RMSD vs BB-RMSD.** Referenced at p7. This is the entire evidential
     basis for dropping receptor binding-site accuracy from the ranking (see `state_metric`);
     **not one BB-RMSD or LDDT-LP number appears in the main text.**
  5. **Figures S2, S4, S5, S6, S9 — the skip-penalty justification, the success-rate/LDDT-PLI
     agreement, the cross-supertarget consistency (R² 0.46/0.53/0.61), the Model-1-vs-best
     correlation, and the chymase-vs-autotaxin affinity scatter.** All the sensitivity analyses
     that make the ranking defensible live here; only their conclusions are in the text.
  6. **Table S1** (target FASTA sequences) and **Figures S3, S7** (example poses at RMSD 2.5 Å;
     the four highest- and lowest-accuracy ligands, 0.70–0.73 and 0.24–0.31 mean best LDDT-PLI,
     target IDs 1010/4028/4027/3192 and 3083/3058/5001/3109) — illustrative, lower priority.
  - **The raw data are public**, however: p16, "The data that support the findings of this study
    are openly available in CASP Prediction Center at
    https://predictioncenter.org/casp16/results.cgi?tr_type=ligand". Per-group method abstracts:
    https://predictioncenter.org/casp16/doc/CASP16_Abstracts.pdf (p7). Both would resolve most
    of `unresolved`.

## F. Figures

Ten figures and two tables. **Twelve panel-group rows** below (eleven from the figures, plus
one MATRIX row for Table 2, which is a genuine method × supertarget value matrix and is the most
reusable single object in the paper). Panel splitting follows the v3 rule — **split on `mark` or
`measure`, never on `facet` alone** — which is applied literally here; where panels differ only
in the `vary` variable (Figures 2 and 6), they are kept in one row and the difference is recorded
in `panels`. See `unresolved` item 10: v3 gives no splitting rule for a `vary` difference.

Four pages were rendered to fill panel structure the captions do not carry: p8 (Figure 3 bar
counts and values), p9 (Figure 4 box counts), p13 (Figure 8A bar count; and to discover that
8B–C are line plots, not bars), p14 (Figures 9 and 10 bar counts and values). All four renders
were deleted after reading.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | p3 | The five target systems: one representative crystal structure each, orange ribbon + purple Zn spheres + stick ligands, with a close-up of the autotaxin site showing double ligand occupancy | structure render | `RENDER \| facet: target system (5: chymase L1001, cathepsin G L2001, autotaxin L3053/L3018, Mpro L4020, WDR55 L5001) \| views: 1 per system, plus 1 binding-site close-up for autotaxin \| overlay: 0 predictions on 1 reference (crystal only) \| axis: none` | 6 lettered panels (A, B, C1, C2, D, E) varying by system; C1/C2 vary by zoom level within one system | | CC-BY 4.0, no ND — p1 |
| 2A-C | p7 (legend); figure on p7 | Bimodality of pose accuracy: histograms of LDDT-PLI and of RMSD over all submissions, plus per-group LDDT-PLI histograms for five arbitrarily chosen groups | bar (histogram) | `PLOT \| facet: submission population (3: all submissions, all submissions, 5 selected groups) \| vary: pose accuracy score (continuous, binned — LDDT-PLI 0–1 at bin width 0.1 in A and C; BiSyRMSD in Å at bin width 1.0 in B) \| series: none (1) \| measure: count of predictions per bin \| mark: bar \| n: NOT REPORTED per bin; per panel = all submissions across 34 groups × 229 targets, count not stated` | 3 (A, B, C). **A and B differ in the `vary` variable, not in facet, mark or measure** — kept in one row per the v3 rule; C differs from A by faceting on group only | n never printed; "five arbitrarily selected groups" in C are not named, so the per-group bimodality claim cannot be traced to a group | CC-BY 4.0 — p1 |
| 3A, 3C | p8 | The paper's primary ranking: skip-penalized mean LDDT-PLI per group, for Model 1 (A) and for each group's best model (C) | bar | `PLOT \| facet: model selection (2: Model 1, best of Models 1–5) \| vary: group (34, sorted descending by score) \| series: none (1) \| measure: skip-penalized mean LDDT-PLI \| mark: bar \| n: per bar = 229 targets with skips scored 0 (the group's actual submission count is printed in each label, 2–229); 34 bars per panel` | 2 of 3 (A and C share measure; B is the row below). A: 0.69 → 0.00; C: 0.73 → 0.00 | no error bars or bootstrap CIs on any bar, so the 0.69 vs 0.69 tie and the 0.69 vs 0.60 gap cannot be assessed for significance — and the paper's own caveat (p14, "a challenge based on different targets would undoubtedly have led to a somewhat different ranking") is not represented anywhere in the figure | CC-BY 4.0 — p1 |
| 3B | p8 | The same ranking under the CADD-familiar metric: skip-penalized fraction of predictions with RMSD ≤ 2.5 Å | bar | `PLOT \| facet: none (1) \| vary: group (34, sorted descending by score) \| series: none (1) \| measure: skip-penalized RMSD success rate (fraction ≤ 2.5 Å) \| mark: bar \| n: per bar = 229 targets with skips scored as failures; 34 bars` | 1 of 3 (B). 0.62 → 0.00, with **10 groups at exactly 0.00** | ten bars pinned at zero are visually indistinguishable, so the bottom third of the field carries no information in this panel; no CIs | CC-BY 4.0 — p1 |
| 4 | p9 | Per-group RMSD distributions within each of the three supertargets with more than two targets, drawn in the D3R house format for cross-challenge comparison | box | `PLOT \| facet: supertarget (3: chymase N=17, Mpro N=20, autotaxin N=189) \| vary: group (~30 per panel, sorted by median) \| series: none (1) \| measure: BiSyRMSD (Å), axis clipped at 14 \| mark: box (whiskers = min/max, box = Q1–Q3, orange dot = median) \| n: per box = that group's predictions within that supertarget (≤17, ≤20, ≤189), no skip penalty; ~30 boxes per panel` | 3, varying by supertarget; group order differs between panels | **axis truncation, stated in the caption:** "The vertical axis limit is set to 14 to focus on the lower-RMSD results and for comparison with prior challenges [14, 15] which used similar axis limits." RMSD has no upper bound (p5), so every gross failure is clipped and the upper whisker is uninterpretable — the metric's own failure mode is the part cropped out. Also: n behind each box is not printed (the axis label gives each group's total across all supertargets, not the per-panel n), and no skip penalty is applied here while Figure 3 applies one, so the two figures rank the same groups on different populations | CC-BY 4.0 — p1 |
| 5 | p10 | Per-target predictability: one stacked bar per pose target, sorted within supertarget, decomposing group-mean accuracy, best-Model-1 accuracy and best-across-all-models accuracy | bar (stacked) | `PLOT \| facet: supertarget (5) \| vary: target/ligand (229, sorted descending by mean best LDDT-PLI within each supertarget) \| series: statistic layer (3: red = per-target mean across groups of each group's best LDDT-PLI; blue = increment to the best Model 1 across groups; black = increment to the best across all models of all groups) \| measure: LDDT-PLI \| mark: bar (stacked) \| n: 1 target per bar, 34 groups × ≤5 models behind each; 229 bars total` | 5 facets in one strip, one bar per target | only the red segment is a central tendency; the blue and black segments are maxima across 34 groups, so total bar height is a best-case envelope and the two are read off the same axis. The across-group distribution behind each red bar — the quantity that would show whether a target is *reliably* predictable — is never shown. Individual target IDs are unreadable at 229 bars | CC-BY 4.0 — p1 |
| 6A-D | p11 | Four candidate explanations for why some targets are easier: ligand size, ligand flexibility, similarity to the PDB, and ligand potency, each against mean pose accuracy | scatter | `PLOT \| facet: candidate correlate (4: non-hydrogen atom count, rotatable-bond count, SuCOS-based PDB similarity 0–1, log IC50) \| vary: the correlate (continuous) \| series: none (1) \| measure: mean best LDDT-PLI across groups, no skip penalty \| mark: point \| n: 1 per mark; per panel 229 targets for A–C, autotaxin-only for D (93 by Table 1 arithmetic, not stated in the paper)` | 4 (A–D). **Panels differ in the `vary` variable only**; measure and mark are identical, so one row per the v3 rule | R² values (0.1, ~0.1, 0.25, 0.07) are given in the text (p10) but not on the panels; panel D silently changes population from all targets to autotaxin only, which the caption states but the axis does not | CC-BY 4.0 — p1 |
| 7A-D | p12 | The anti-memorization control: per-target accuracy of each automated baseline against how similar that target is to anything already in the PDB | scatter | `PLOT \| facet: baseline method (4: AlphaFold 3, Boltz-1, RoseTTAFold All-Atom, AutoDock Vina) \| vary: maximum SuCOS-based structural similarity to available PDB structures (continuous, 0–1) \| series: none (1) \| measure: LDDT-PLI \| mark: point \| n: 1 per mark; per panel = 228 targets minus that method's failures (5/9/7/5), i.e. ~223/219/221/223 — not stated on the figure` | 4, varying by method | **the figure carries the paper's most load-bearing negative — "this is not the case" (p10) — with no regression line, no R², and no correlation coefficient of any kind**, in a paper that reports R² for the four weaker correlations in Figure 6. A null asserted from a point cloud by eye. Also, the similarity cutoff date differs between panels (2021-09-30 for AF3/Boltz-1, 2020-03-31 for RFAA, 2024-05-03 for AD Vina, p6), so the x-axes are not the same quantity across panels | CC-BY 4.0 — p1 |
| 8A | p13 | Affinity ranking accuracy per group, Stage 1, Model 1 predictions | bar | `PLOT \| facet: none (1) \| vary: group (26, sorted descending) \| series: none (1) \| measure: N-weighted Kendall's τ (κ_N) \| mark: bar \| n: per bar = affinities ranked by that group, printed in the label (108 for most; 95, 99, 82 for three; **0 for five groups**); 26 bars` | 1 | five bars are labelled with **0 affinities ranked** yet still carry a plotted τ near zero, and what those bars represent is never explained; the bar count (26) does not match the 28 Stage-1 affinity groups stated on p6 and p12; no CIs, on a statistic whose noise floor the paper itself computes elsewhere (SD 0.11 for chymase, p13) | CC-BY 4.0 — p1 |
| 8B-C | p13 | The Stage 1 vs Stage 2 null: does handing predictors the experimental structure shift the distribution of affinity accuracy? | line (normalized histogram drawn as a polyline) | `PLOT \| facet: supertarget (2: autotaxin, chymase) \| vary: Kendall's τ ranking statistic, −0.5 to 0.7 (continuous, binned at 0.2) \| series: stage (2: Stage 1 blue, Stage 2 red) \| measure: probability (normalized histogram) \| mark: line \| n: per line = 21 (autotaxin S1), 24 (autotaxin S2), 28 (chymase S1), 27 (chymase S2) group submissions` | 2 (B autotaxin, C chymase). **Drawn as lines, not bars — the caption says "normalized histograms" but the marks are polylines**, which is why this is a separate row from 8A | ~6 bins holding 21–28 observations each, so the curve shape is strongly binning-dependent, and the two curves are compared **by eye with no test statistic** for what is one of the paper's two headline conclusions ("knowledge of the structures did not lead to a shift toward greater accuracy", p14). The chymase panel (C) in fact shows a visible leftward Stage-2 shift that the text does not discuss | CC-BY 4.0 — p1 |
| 9 | p14 | Baseline affinity predictors, including the trivial descriptor baselines, with the best CASP group shown for scale | bar | `PLOT \| facet: none (1) \| vary: predictor (7: Haiping group 16 S1 [the best CASP group, for reference], MolWeight S1, GPR S1, GNINA Score S2, AD Vina S1, AD Vina Score S2, cLogP S1) \| series: stage (2: S1 blue, S2 orange) \| measure: N-weighted Kendall's τ \| mark: bar \| n: per bar = 122 affinity targets for S1 and 103 for S2 — not printed on the figure` | 1 | mixes a CASP participant result with six assessor-run baselines on one axis without visual distinction, so the striking comparison (MolW 0.37 vs the best participant 0.39) reads as a like-for-like contest between a blind and a non-blind arm; no CIs | CC-BY 4.0 — p1 |
| 10 | p14 | Do predictors know when they are right? Correlation between each group's self-reported LScore and its actual pose accuracy | bar | `PLOT \| facet: none (1) \| vary: predictor (11: 10 CASP groups + AF3 with ligand pLDDT as LScore, sorted descending) \| series: none (1) \| measure: Kendall's τ between LScore and LDDT-PLI, no skip penalty \| mark: bar \| n: per bar = that group's predictions carrying an LScore, printed in the label (1295, 1292, 1225, 959 … 22); 11 bars` | 1 | the bar for GrominhaLab (272) rests on **22** predictions while the rest rest on ~1000–1300, and the axis gives them identical visual weight; the AF3 bar is a non-blind assessor computation placed on the same axis as ten blind participant submissions with no marking; no CIs | CC-BY 4.0 — p1 |
| Table 2 *(a table, not a figure — included because it is the paper's most reusable value matrix)* | p11 | Skip-penalized mean LDDT-PLI for each automated baseline and for the best CASP group, overall and per supertarget | heatmap-shaped table (rendered as plain text) | `MATRIX \| rows: method (5: AF3, Boltz-1, RFAA, AD Vina, ClusPro group 494) \| cols: supertarget (5: All, chymase, cathepsin G, autotaxin, Mpro) \| value: skip-penalized mean LDDT-PLI (0–1) \| facet: none (1)` | 25 cells, no panels | the "All" column is dominated by autotaxin (189/229), which the footnote states — "Autotaxin, with 189 targets, dominates the overall averages" — but the table gives every column equal width, so cathepsin G (n = 2) and autotaxin (n = 189) look equally weighty; **per-column n is not printed in the table** | CC-BY 4.0 — p1 |

**Table 1 (p2)** is not given a row: it is a target inventory (protein, Npose, resolution range,
Naffinity by stage, affinity range, contributor, supertarget ID, target ID range) with no
measured quantity and no panel structure. Its contents are transcribed in `n_targets`.

**`reuse`, in full:** p1 — "This is an open access article under the terms of the **Creative
Commons Attribution License**, which permits use, distribution and reproduction in any medium,
provided the original work is properly cited. © 2025 The Author(s). PROTEINS: Structure,
Function, and Bioinformatics published by Wiley Periodicals LLC." **CC-BY with no ND clause and
no NC clause**, so redrawing, recolouring, adapting and reusing any panel is permitted with
attribution. This is a materially freer licence than `chitsazi2025gpcrdock4` (CC-BY-ND), and it
means Table 2 and Figure 7 can be redrawn for our manuscript.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), single-paper extraction against SCHEMA.md v3
- **schema_version**: v3
- **confidence**: **high** for sections A, B, D, E and for `oracle_leakage`, `prospective`,
  `state_metric`, `controls_run` — the paper is unusually explicit about its own protocol, dates
  and caveats, the text layer of the PDF is clean, and every number quoted above is either in
  the running text, in Table 1/2, or was read directly off a rendered figure. **Medium** for
  three things: (i) the participant-side method descriptions, which are not in this PDF at all
  and live in an external abstracts booklet, so the paper's central template-based claim is
  recorded exactly as stated and cannot be audited from the paper; (ii) all per-group
  per-supertarget numbers, which are in the unheld Table S2; (iii) the Figure 2 panel structure,
  which was taken from the caption rather than a render (bin widths and panel roles are stated
  in the caption, so this is low risk). What was hard to read: the paper's two-column layout
  interleaves figure legends with body text in the extracted text stream, so legends for
  Figures 2, 4, 5, 7 and 8 appear a paragraph away from where they are cited — every legend
  above was matched back to its figure number explicitly.

- **unresolved**:
  1. **v3 GAP, and the one that matters for this paper: routes 5 and 6 have no way to record
     "applied by the assessor after the predictions were sealed."** Every blind competition
     scores predictions against a reference the assessors hold and assigns best/worst labels
     against it. Under a literal reading of v3, that is routes 5 and 6 "PRESENT", and an
     honest blind assessment — the rarest and most valuable design in this corpus — scores as
     leaky in exactly the same cells as a paper that tuned its RMSD threshold on the answer.
     This note records the distinction in prose (`PRESENT BY DESIGN — ASSESSOR-SIDE,
     POST-SEAL`) and refuses the `oracle-leak` tag. **Recommendation for v4:** routes 5 and 6
     should take a three-valued answer — `absent` / `present, predictor-side` / `present,
     assessor-side post-seal` — or the schema should carry a `blind_arm` boolean that the two
     routes are read against. `chitsazi2025gpcrdock4` hit the identical wall and solved it the
     identical way, independently; two extractors, two papers, same defect.
  2. **The release dates of the target structures are never stated.** The paper gives the
     deposition date (2024-05-03, p6) and the challenge dates (p4), and it names five Mpro
     entries that *were* public early (p4), but it never says "the remaining structures were
     released on date X". Blindness for the other 224 pose targets is therefore established by
     deposition date + template cutoff + the organisers' own audit, which is strong, but is not
     a direct statement. Resolvable from the PDB entries or the CASP16 results page (p16).
  3. **The paper's central claim — that template-based methods won — cannot be audited from the
     paper.** The evidence in the PDF is two sentences: p7, "All four groups include
     template-based steps", naming ClusPro (494), kozakovvajda (274), CoDock (262) and
     Huang-HUST (91); and p14, "All of the leading pose-prediction methods are at least partly
     template-based." **There is no table of which groups used templates, no count of
     template-based vs non-template-based groups, and no group-level statistic comparing the two
     classes.** The per-group method descriptions are in the external CASP16 abstracts booklet
     (p7 URL). The claim is also softened by "at least partly" and by the observation on p6
     that "Many groups combined several techniques … such as a workflow that uses a structural
     template if available but falls back on docking calculations if no template can be found",
     which makes "template-based" a property of a *step in a pipeline*, not of a method class.
     Quote the claim as the authors state it; do not convert it into a between-class comparison
     the paper never made.
  4. **How the single reported baseline pose was chosen from the 25 generated models is not
     stated.** p5 says AF3 and Boltz-1 produced "a total of 25 models per system"; p10 says the
     baselines generated "a single pose prediction for each of the CASP16 protein–ligand
     targets". The selection rule (ranking score? first seed? best pLDDT?) is nowhere in the
     Methods. If it were best-by-score it would be a legitimate model-1 analogue; if it were
     best-by-LDDT-PLI it would be a route-6 selection on the assessor side and would inflate the
     0.80. **Nothing in the text suggests the latter, and the AF3 pLDDT-as-LScore analysis (p5,
     p14) implies a confidence-based selection, but the paper does not say so.** This is the
     single most consequential unstated detail in the paper, because 0.80 vs 0.69 is its most
     quoted comparison.
  5. **Receptor conformational state was never assessed — stated here explicitly as instructed.**
     p4: "**We did not assess the accuracy of the overall protein structures because multiple
     crystal structures of these target proteins were already available in the PDB.**" Binding-
     site geometry *was* computed as BB-RMSD (Cα RMSD over binding-site residues) and LDDT-LP
     (p5) and then dropped from the ranking, p7: "we … ultimately chose not to rank participants
     on this metric … predictions with accurate ligand poses … also tend to have accurate
     binding site predictions". **No BB-RMSD or LDDT-LP value appears anywhere in the 18-page
     main text**; the supporting evidence is Figure S1, which is not held. There is no
     conformational state variable of any kind in the paper — no apo/holo pair, no
     active/inactive, no second conformation of any target. This paper cannot speak to any
     state question.
  6. **The anti-memorization null in Figure 7 is reported without a statistic.** p10 asserts
     "this is not the case" for the accuracy-vs-PDB-similarity correlation across all four
     baselines, but no R², no correlation coefficient and no regression line appears, in a paper
     that reports R² for the four weaker correlations in Figure 6 (p10). The null is plausible
     from the point cloud but is not quantified. Additionally the four panels use three
     different similarity cutoff dates (p6), so their x-axes are not strictly the same quantity.
  7. **Whether this paper is `precedent`, `background` or a memorization `threat` is genuinely
     the user's call, and the two halves of its evidence point opposite ways.** The winning
     participant methods are template-based, i.e. they explicitly reuse deposited co-crystals
     (p7, p14) — which reads as memorization winning a blind competition. But the paper's own
     control finds *no* correlation between baseline accuracy and PDB similarity (Figure 7,
     p10), only a weak one on the participant side (R² 0.25, Figure 6C), and the one
     zero-similarity target was solved almost perfectly by AF3 (LDDT-PLI 0.93, p10) while being
     among the worst for participants (p10). Recorded as `precedent` + `background`; flag for
     confirmation.
  8. **Three internal numeric inconsistencies, all small, all worth knowing before quoting:**
     (a) **Boltz-1's overall score is 0.52 in the text (p10) and 0.53 in Table 2 (p11).**
     (b) **The abstract (p1) says "maximum Kendall's τ = 0.42", while the text (p12) and Figure
     8A (p13) give the best group, Haiping, at κ_N = 0.39** and p12 says "the maximum value of
     Kendall's τ observed here, about 0.4". 0.42 may be a single-supertarget τ rather than the
     N-weighted κ_N, but the paper never says so. **Quote 0.39 as the N-weighted maximum and
     cite p12/p13; do not quote 0.42 without this caveat.**
     (c) p10 reads "the LDDT-PLI of the best submitted model exceeded 0.6 on 98% of targets
     (224/229 whole bars), **including 94% of targets where LDDT-PLI > 0.7**" — the sentence is
     ambiguous as to whether 94% is a fraction of all targets or of the 224.
  9. **Group counts do not reconcile in two places.** (a) p6 says "19" groups submitted
     incidental-ligand pose predictions; p11 says "We receive 18 Model 1 submissions with pose
     predictions for the incidental ligands". (b) p6 and p12 both give 28 Stage-1 affinity
     groups for chymase, but **Figure 8A (rendered) shows 26 bars**, five of which are labelled
     with 0 affinities ranked. Neither discrepancy is explained.
  10. **v3 ambiguity, reported as requested: there is no splitting rule for a `vary`
      difference.** The rule is "split on `mark` or `measure`, never on `facet` alone", which
      leaves the common case of panels that share mark and measure but plot a *different
      independent variable* undecided. This paper has it twice: Figure 2 (A/C bin LDDT-PLI, B
      bins RMSD) and Figure 6 (four different correlates against the same accuracy measure).
      Following the rule literally puts each in one row and forces a compound `vary` string —
      precisely the unjoinable-compound-string failure the split rule exists to prevent, only
      relocated from `measure` to `vary`. **Recommendation for v4: state whether a `vary`
      difference splits.** I have followed the rule literally and recorded the difference in
      `panels`; another extractor following the same v3 text could defensibly split these into
      four rows instead, which means the join key is not yet deterministic for this shape.
  11. **Minor, but it affects any n we quote from Figure 6D:** the caption says panel D is "only
      for autotaxin targets (L3000)" and the measure requires an affinity, so n should be the 93
      autotaxin pairs with both a structure and an affinity (Table 1 arithmetic, p2–p3). **The
      paper never states this n**, and it could equally be 123 if pose accuracy were averaged
      differently. Do not quote an n for Figure 6D.
  12. **No tag was needed that the v3 vocabulary lacks.** Every tag below is from the fixed list.
      The closest call was a tag for "assessment / community challenge" as distinct from
      "benchmark", but `benchmark-only` covers it without distortion. If v4 ever adds one,
      `blind-assessment` would separate this paper and `chitsazi2025gpcrdock4` from the
      retrospective benchmarks, which is currently only recoverable by combining
      `benchmark-only` + `prospective`.

- **why_it_matters**: *(left empty by the extractor — the user's call)*

---

## Tags

`general-protein` `benchmark-only` `cofolding` `multi-backbone` `templates-on` `single-state`
`continuous-metric` `binary-predicate` `saturating-metric` `prospective` `anti-memorization`
`unpowered` `confidence-as-discriminator` `design-level-oracle` `orthosteric` `peer-reviewed`
`precedent` `background` `comparator-numbers`

**Scoping notes on six tags that are true but narrower than they look:**
- `general-protein` — chymase and cathepsin G are serine proteases, autotaxin an
  ectonucleotide pyrophosphatase, Mpro a viral cysteine protease, WDR55 a WD-repeat scaffold
  (p3–p4). No GPCR, no protein kinase. Do not let a "drug target" query pull this into a GPCR or
  kinase reverse lookup.
- `cofolding` — warranted **only for the assessors' baseline arm** (AF3, Boltz-1, RFAA run
  end-to-end, p5, p10) and for two named participant pipelines (MULTICOM_ligand's NeuralPlexer +
  DiffDock combination, p12). AF3 and Boltz-1 were **not available to participants** during the
  challenge (p5, p10), so this paper is not evidence about blind co-folding performance.
- `templates-on` — the participant arm, where template use is uncontrolled but is the paper's
  headline finding (p7, p14), and the AD Vina baseline, which docks into a SWISS-MODEL receptor
  built from a named PDB template (p5). **Not** the coordinate-zeroed submission skeleton the
  organisers handed out (p4), which contains no structural information.
- `saturating-metric` — applies to **Kendall's τ on the chymase affinity set only**, where the
  400× IC50 range imposes a ceiling of 0.54 ± 0.11 and the authors state that the challenge "is
  less capable of resolving levels of accuracy" (p13). The autotaxin ceiling (0.76) and the
  N-weighted ceiling (0.73) leave ample headroom above the observed 0.39, and LDDT-PLI does not
  saturate at all. Do not read this tag as "the assessment metrics were useless".
- `unpowered` — at the **novel-system level only: n = 1** (WDR55, the sole zero-PDB-similarity
  target, p4, p10), and at the cathepsin G supertarget (n = 2 pose targets, on which AD Vina's
  0.85 outlier rests, Table 2 p11). **Pose-target n is 229 and affinity-target n is 122** — both
  are well powered. Use the right number; all three are in `n_predictions`.
- `design-level-oracle` — **route 7, assessor baseline arm only, and it is the weakest form.**
  The four baselines were run after the answers were known and the authors say so (p10, "These
  calculations were not conducted in a blinded setting"); AD Vina's receptor template was chosen
  for "the presence of a ligand in the main known pocket" (p5); and the WDR55 probe was run after
  the main comparison (p10). Nothing about any answer was fed to any model, no target was chosen
  because its answer was known (the opposite: they were chosen because it was not), and the
  participant arm — which is the paper — is untouched. **Tagged so a route-7 reverse lookup finds
  the retrospective baseline arm; a reader who takes this as a verdict on the challenge has
  misread it.**

**Tags considered and rejected, with reasons, so the decision is auditable:**
- **`oracle-leak` — REJECTED, and the rejection is the point of this note.** The participant arm
  is blind: targets posted 2024-05-05, deadline 2024-07-21, answers deposited 2024-05-03 and
  released after (p4, p6). Routes 5 and 6 are present but assessor-side and post-seal, which is
  what a blind assessment is (see `unresolved` 1). The two real leaks — 5 Mpro pose targets
  public before the deadline (p4) and 18 affinity values disclosed in patents and one paper
  (p12) — were **discovered by the organisers and the affected targets were removed**, with the
  affinity case additionally re-analysed with them left in (Figure S10, p12). Tagging a paper
  `oracle-leak` for leakage that it found and excised would invert the meaning of the tag and
  corrupt the reverse lookup.
- `no-anti-memorization` — rejected; the anti-memorization design here is four-layered
  (blind window, leak audit and excision, training-cutoff verification, a quantified
  per-target similarity axis) and two of the layers were run as analysed control arms.
- `rmsd-only` — rejected. BiSyRMSD is one of two pose metrics and is the *secondary* one; the
  primary ranking is on LDDT-PLI, a contact-based measure with an added false-contact penalty
  (p5). Tagging rmsd-only would understate the metric and false-positive a query for
  RMSD-only rigour defects.
- `visual-metric` — rejected as the assessment's metric; nothing is called by eye in the
  scoring. **Near-miss worth recording:** the Figure 7 null (no accuracy/similarity correlation,
  p10) and the Figure 8B–C null (no Stage-1/Stage-2 shift, p14) are both read off plots without
  a test statistic. That is a *reporting* defect, recorded in `hides`, not a visual state call.
- `two-state`, `ensemble`, `continuum` — rejected; one crystallographic state per target, one
  static complex per submitted model. The 25 baseline models per system (p5) and the up-to-five
  participant models (p4) are alternative poses collapsed to one before scoring, so `ensemble`
  would false-positive a query for methods that deliver ensembles.
- `md`, `enhanced-sampling`, `md-emulator` — rejected; no simulation is run by the authors, and
  the paper notes that the one physics-heavy class that would qualify never entered: "none used
  the highly regarded approach of simulation-based free energy calculations" (p6).
- `msa-subsample`, `msa-state-filter`, `af-cluster`, `latent-steering`, `template-state-bias`,
  `state-annotated-input`, `no-template-no-msa` — rejected; none occurs. MSAs were generated by
  the standard AF3 pipeline and shared unchanged between AF3 and Boltz-1 (p5); no MSA
  intervention, no internal-tensor intervention, and no state annotation exists anywhere in the
  paper.
- `directed-state`, `partner-driven`, `ligand-driven`, `peptide-driven`, `g-protein-mimetic`,
  `nanobody`, `apo-sampling`, `seed-only` — **all rejected; the entire Control block is
  inapplicable.** These tags mark handles on *conformational state*. The ligand here is the
  object being predicted, not a lever on a receptor state, and no apo arm, partner, or
  seed-steering experiment exists. Tagging `ligand-driven` because the paper is about ligands
  would be the exact false positive the vocabulary is designed to prevent.
- `allosteric-site`, `cryptic-pocket`, `allosteric-failure` — rejected. All assessed ligands sit
  in enzyme active sites ("small molecule ligands bound in the enzyme's active sites", Figure 1
  caption p3), hence `orthosteric`. WDR55 is the one site that was not previously characterised
  (p4) but the paper never calls it cryptic or allosteric, and one target is not a finding.
- `experimental` — rejected; that tag marks a paper with no structure prediction in it, and this
  one scores tens of thousands of predicted complexes.
- `experimental-validation` — rejected, and the near-miss is worth stating: the paper is built
  on previously unpublished experimental structures and affinities contributed by Roche, Idorsia
  and the SGC (Table 1 p2, refs [19, 20]), but those are the **reference answers**, not a
  laboratory test of a computational prediction made afterwards. Nothing predicted here was
  subsequently validated in a lab.
- `preprint` — rejected; this is a peer-reviewed Wiley research article with received / revised
  / accepted dates on p1.
- `contrast`, `threat`, `negative-result` — rejected as the overall stance. The paper's rigour
  exceeds the corpus norm rather than challenging it, and its subject does not overlap ours.
  `negative-result` was the closest call: the paper contains three clean nulls (Stage 2 does not
  help affinity, p14; accuracy does not track PDB similarity for the baselines, p10; ligand
  complexity does not predict difficulty, p10) and one soft null (no demonstrable progress since
  D3R, p15). But `negative-result` in this vocabulary marks a paper whose *headline* is a
  negative, and this paper's headline is a positive ranking result. Recorded in
  `central_conclusion` and `controls_run` instead.
- `figure-exemplar` — rejected. The figures are serviceable but three of them carry the defects
  listed in `hides` (a clipped unbounded axis, a null with no statistic, a stacked bar mixing
  means with maxima). **Table 2 is the exception and is genuinely reusable**, which is why it
  was given a MATRIX row; that alone does not warrant the tag.
