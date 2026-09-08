# chitsazi2025gpcrdock4

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–31), and the PDF page
equals the printed page throughout** (PDF p15 prints "15"). Layout: p1 abstract, p2
introduction, p3–p12 Results, p12–p14 Discussion, p15–p19 figures and legends, p20 Tables
1–3, p21–p22 Methods, p22–p23 acknowledgements / author contributions / data availability,
p24–p31 references.

**THE SI IS NOT HELD.** This is a 31-page main text only. Supp. Data 1–4, Supp. Tables 1–4
and Supp. Figs 1–10 are all cited and none is present. That matters more than usual here:
the participant list, the per-model ranking table, every group's method description, and
**the entire AlphaFold3/Boltz-1/Chai-1/NeuralPLexer arm (Supp. Fig. 10)** live in the
missing SI. See `si_in_scope`.

**Why this note is long on `oracle_leakage` and `prospective`:** this is a genuinely blind,
genuinely prospective community assessment — the rarest property in this corpus. The
timeline is reconstructed field by field below with page-cited quotes so the blindness
claim is checkable rather than asserted.

**License warning, read before using any panel:** the paper is **CC-BY-ND 4.0**. The ND
clause forbids derivatives, which includes redrawing, recolouring, cropping and adapting.
See `reuse` in section F.

---

## A. Identity

- **citekey**: `chitsazi2025gpcrdock4`
- **doi**: **10.1101/2025.04.18.647407** (bioRxiv). p1 banner, repeated on every page:
  "bioRxiv preprint doi: https://doi.org/10.1101/2025.04.18.647407; this version posted
  April 20, 2025."
- **year**: **2025.** Posted 20 April 2025 (p1 banner).
- **venue**: **bioRxiv preprint — NOT peer-reviewed.** p1 banner: "The copyright holder for
  this preprint (which was not certified by peer review) is the author/funder, who has
  granted bioRxiv a license to display the preprint in perpetuity. It is made available
  under a CC-BY-ND 4.0 International license." No journal masthead, no
  received/accepted/editor line anywhere in 31 pages. Tagged `preprint`, not
  `peer-reviewed`. Note the license is **ND**, which is unusual for bioRxiv and is a
  practical constraint on figure reuse.
- **title**: "The 4th GPCR Dock: assessment of blind predictions for GPCR-ligand complexes
  in the era of AlphaFold" — p1.
- **authors**: Rezvan Chitsazi (Skaggs School of Pharmacy, UC San Diego), Yiran Wu (iHuman
  Institute, ShanghaiTech), **GPCR Dock 2021 participants** (a collective author; the roster
  is Supp. Table 1, not held), Raymond C. Stevens (corresponding, iHuman/ShanghaiTech),
  Suwen Zhao (corresponding, iHuman/ShanghaiTech), Irina Kufareva (corresponding,
  ikufareva@ucsd.edu, UC San Diego) — p1.
  **Continuity note:** Kufareva and Stevens are authors on the GPCR Dock 2010 [ref 16] and
  2013 [ref 17] assessments, and the scoring function used here is imported unchanged from
  ref 17 (p22). This is the same assessment team running the same metric a fourth time,
  which is what makes the cross-round comparison in Fig 5B/D legitimate.

## B. Scope

- **system**: **GPCR, exclusively.** Five receptor–ligand complexes (p3).

- **n_targets**: **5 complexes of 5 distinct receptors.** p3: "The GPCR modeling and docking
  assessment 2021 was performed for five separate GPCR-ligand complexes: Apelin receptor
  bound to a small-molecule agonist cmpd6 (APJ/cmpd6), orphan receptor GPR139 bound to a
  small-molecule agonist JNJ-63533054 (GPR139/JNJ-63533054), κ-Opioid receptor bound to
  agonist peptide dynorphin (OPRK/dynorphin), Neuropeptide Y Receptor Y1 bound to its
  endogenous agonist neuropeptide Y (NPY1R/NPY), and Neuromedin U Receptor 2 bound to
  agonist peptide neuromedin U-25 (NMUR2/NMU25)."
  - **Split by ligand modality: 2 small-molecule targets (APJ/Cmpd6, GPR139/JNJ-63533054),
    3 peptide targets (OPRK/dynorphin A(1-13), NPY1R/NPY, NMUR2/NMU25).** p12: "Only two of
    five 2021 targets were complexes with small molecules; three were with peptides (vs only
    1 peptide complex in prior assessments, that of CXCR4 with CVX15 in 2010 [16])."
  - **Split by prior structural coverage:** target-receptor structures existed in the PDB for
    APJ, OPRK, NPY1R; only distant homologues for GPR139 and NMUR2. p3: "Experimental
    structures with high sequence homology to the target (which can greatly aid the modeling
    efforts) were only available in the Protein Data Bank (PDB) for APJ, OPRK, and NPY1R; for
    GPR139 and NMUR2, only distant homologous structures existed (Fig. 1B)."
  - **Split by experimental method of the answer:** 1 X-ray (APJ/Cmpd6, 2.40 Å), 4 cryo-EM
    (Table 1–2, p20).
  - **All five complexes are active-state, G-protein-bound.** p3: "All five complexes featured
    active receptors and intracellularly bound heterotrimeric G proteins; however, predictions
    for receptor interactions with the G proteins were not evaluated as part of the
    assessment." **This single sentence is why no conformational-state question is ever
    asked** — every target is in the same state, so state is a constant, not a variable.
  - **Receptor CLASS is NOT REPORTED.** The paper never uses class A / class B / rhodopsin-like
    / family terminology for the targets. It names them only as "Apelin receptor", "orphan
    receptor GPR139", "κ-Opioid receptor", "Neuropeptide Y Receptor Y1", "Neuromedin U
    Receptor 2" (p3–p4), and elsewhere only says "GPCR superfamily" (p2). The closest thing to
    a classification statement is the homology bar chart Fig 1B (p15), which lists the closest
    structural templates as AGTR1/CXCR2/US28/OPRD for APJ, CCR5/GPR52/NTR1/OPRK/CCKAR for
    GPR139, OPRM/OPRD/OPRX/OX2R for OPRK, CCKAR/NPY2R/NK1R/AGTR1 for NPY1R, and
    GHSR/OPRK/OX1R/OX2R for NMUR2. **Do not write "all five are class A" into the manuscript
    on the strength of this paper — it does not say so.** All five are peptide-binding
    receptors by the ligands named, which is as far as the text goes.

- **method_class**: **benchmark-only** (a blind community assessment; the authors score other
  people's models and do not propose a modelling method) **+ a small co-folding arm run by the
  assessors themselves**. p12: "The release of the open-source code for AlphaFold3 [109,110]
  and other related diffusion-based models for protein co-folding with small molecules
  (NeuralPLexer [111], Chai-1 [112], Boltz-1 [113]) made it possible to assess this next
  generation methodology on the small-molecule complexes from GPCR Dock 2021." That arm is
  described in Methods p22 under "End-to-end modeling of APJ/Cmpd6 complexes" and is
  retrospective, unlike the assessment proper.

- **backbones**: **Two populations; keep them apart.**
  - **Participant-side (blind, 2021):** AlphaFold2 / AlphaFold Monomer v2.0 (p7, p11),
    **AlphaFold2-Multimer** for peptide co-folding (p9, p11, Fig 5C "AF cpx"), RoseTTAFold
    (p7, UW-DiMiao), RosettaCM / MODELLER conventional homology (p7, p9), Rosetta Ligand
    Docking / Rosetta GALigandDock (p7), AutoDock CrankPep (p9), GEnSeMBLE/SuperBiHelix (p11),
    docking into deposited PDB structures (p11), plus MD refinement in GROMACS/CHARMM36m
    (SIAT-Yuan, 200 ns) and Schrödinger/S-OPLS (ShanghaiTech-Bai, 100 ns) — p9.
  - **Assessor-side (retrospective, Nov 2024):** **AlphaFold3 v3.0.1, Boltz-1, Chai-1,
    NeuralPLexer v1.0** — p22.
  - Four next-generation backbones are compared head to head on the same two targets, and
    AF2 vs RoseTTAFold vs homology vs PDB-docking vs GEnSeMBLE are compared head to head across
    all five (Fig 5A/C, p19). Tagged `multi-backbone`.

- **templates**: **Dual, and mostly NOT REPORTED.**
  - Participant-side: **not controlled by the assessment.** Templates were whatever each group
    chose. The available templates are enumerated per target on p3–p4, and Fig 1B (p15) plots
    their TM sequence identity. UW-DiMiao "built partial threaded models using RosettaCM [103]
    based on predicted homologs from HHpred [104]" (p7); MSU-Feig used a **state-annotated
    template**: "the receptor was first modeled using the Multi-State GPCR modeling protocol
    [107] and then used as a template in AlphaFold Multimer, to bias the predictions towards
    the active state of the complex" (p9). Whether any group's AF2 run had templates on or off
    is **NOT REPORTED** anywhere in the main text.
  - Assessor-side AF3 arm: **NOT REPORTED explicitly.** p22 says only "For AlphaFold3, the
    published GitHub version 3.0.1 was used with default parameters; the database preset was
    configured to the full database mode". AF3's default is templates on, but the paper does
    not say so, and does not say whether the template search was date-restricted. This matters
    because the answer structures were in the PDB by Nov 2024 (Tables 1–2, p20).

- **msa_handling**: **Dual.**
  - Participant-side: **varied and mostly unreported.** SDU-Yang used "AlphaFold V2.0 [20] to
    predict the APJ model using a **customized MSA** and applying AlphaFold default settings"
    (p7) — the only MSA intervention named in the main text, and its nature is not described.
    A negative MSA result is reported for OPRK: co-folding "did not work well for OPRK
    (Fig. 5C), possibly because the peptide was too short for building a reliable multiple
    sequence alignment (MSA)" (p11), restated on p13 as "likely due to lack of co-evolution of
    this short and extremely conserved peptide with the receptor".
  - Assessor-side: **full.** AF3 — "the database preset was configured to the full database
    mode and multiple sequence alignments were constructed using Jackhmmer version 3.3";
    Boltz-1 — "`--use_msa_server` (MMSeqs2)" (p22). No subsampling, no clustering, no
    state-filtering anywhere in the paper.

## C. Conformational core

- **states_generated**: **one.** Every submitted model is a single static receptor–ligand
  complex, and every target is the same functional state (active, agonist-bound), so no
  method in this paper is asked to produce two states or an ensemble of states. Groups could
  submit **up to five models per target** (p21: "Groups were invited to submit up to five
  models per target"), but those five are alternative *poses/models* within one state, not
  distinct conformational states — the paper never once describes a submission as an inactive
  or intermediate state. Several participant *pipelines* sampled internally and collapsed
  (SIAT-Yuan "built 20,000 receptor models … selected the best one by DOPE … refined it with a
  200 ns restrained all-atom MD simulation … and selected representative conformation from the
  clustered simulation frames", p9; GEnSeMBLE is cited via ref 108, "SuperBiHelix method for
  predicting the pleiotropic ensemble of G-protein-coupled receptor conformations", p30), but
  what reaches the assessment is ≤5 single structures. **Not dual:** the ensemble half never
  enters the measured object.

- **structural_priors_used**: **Extensive, deliberate, documented, and not a defect** — this
  is the field that carries what participants were legitimately allowed to know, and the
  paper spends p3–p4 enumerating it precisely because prior knowledge is the confound the
  assessment is designed around.
  1. **Deposited structures of the target receptor in other complex compositions**, for three
     of five targets. APJ — p3: "There were two X-ray structures available for APJ, one bound
     to an unrelated agonist peptide (AMG3054, PDB 5VBL [23]) and another to a single domain
     antibody (JN241-9, PDB 6KNM [24])." OPRK — p3: "multiple structures bound with agonists
     (e.g. MP1104, PDB ID 6B73 [47]) and antagonists (e.g. JDTic, PDB ID 4DJH [48]) existed in
     the PDB at the time of the assessment, but peptide-bound structures were not available."
     NPY1R — p4: "two X-ray structures existed in the PDB at the time of the assessment, both
     solved with small molecule antagonists (PDB 5ZBQ, 5ZBH) [61]."
  2. **Deposited structures of close homologues with peptides.** p3 (OPRK): "structures with
     bound peptides were available for OPRD and OPRM, the two closest homologs of OPRK (PDB
     IDs 6PT2 [49], 6DD[EF] [50], 4RW[AD] [51])." p4 (NPY1R): "CCKAR complexes with CCKN (PDB
     IDs 7MBX, 7EZH) [62,63] provided a highly structurally similar template for both the
     receptor in an active agonist-bound conformation, and the agonist peptide with an amidated
     C-terminus in the receptor's pocket."
  3. **No structural prior at all for two targets.** GPR139 — p3: "At the time of the
     assessment, there were no available experimental structures for this receptor, and the
     closest homologous structure (CCR5) had only 27% sequence identity in the TM domain
     (Fig. 1B)." NMUR2 — p4: "There were no experimental structures for NMUR2 at the time of
     assessment and the closest structurally characterized homolog, the Neurotensin receptor 1
     (NTSR1) had only ~35% sequence identity in the TM domain (Fig. 1B)."
  4. **Public AlphaFold apo models of all five targets.** p4: "In addition to the listed
     experimental structure of target and homologous receptors, models of all five receptors,
     in apo form, have also been predicted by the AlphaFold Monomer V2.0 pipeline and were
     available publicly in AlphaFold Protein Structure Database [86] at the time of the
     competition."
  5. **Ligand SAR for all five targets, receptor mutagenesis for three of five.** p4 summary:
     "However, considerable ligand SAR information was available for all five targets, and
     receptor mutagenesis for three out of five targets, which could assist and guide model
     selection." Detail per target on p3–p4 (e.g. GPR139: "The agonist binding site on GPR139
     has been mapped through extensive mutagenesis [43,45,46], providing hints regarding the
     compound binding geometry for this receptor").
  6. **The scoring background set is itself a structural prior, frozen from 2013.** p22: "The
     background set (34,317 pairs of PDB complexes representing 1390 proteins) and the equation
     for this calculation were exactly taken from [17] to ensure that the results are directly
     comparable to prior assessments."

  Note the paper's own warning that priors can hurt: p12 — "On the one hand, homologous
  structures may provide critical templates for modeling. On the other, by biasing modeling
  efforts, the available structures can have a detrimental effect on modeling success when the
  target complex is sufficiently conformationally distinct." Borne out: the most
  structurally-characterised receptor (OPRK) was the hardest target (p9).

- **oracle_leakage**: **For the community assessment proper: essentially NONE, by
  construction — this is the cleanest prospective design in the corpus. For the assessors'
  post-2024 AF3-era arm: retrospective by construction, with the training-data question
  unanswerable from this PDF. Routes 5 and 6 are present by design and are the assessment's
  purpose, not a defect.** Enumerated route by route.

  **Route 1 — deposited structures of the target state as input or template.
  NONE FOUND for participants.** The target complex structures were withheld and had not been
  released.
  - p2 (design statement): "GPCR Dock capitalizes on **recently solved and yet-unpublished**
    experimental structures of receptor-ligand complex to challenge the community with **blind
    prediction of complex geometries from amino-acid sequences** (and a 2D structure for
    small-molecule ligands)."
  - p22 (acknowledgements — the mechanism by which the assessors, not the participants, held
    the answers): "The authors are grateful to … Drs. Fei Xu, Zhi-Jie Liu, Tian Hua, Beili Wu,
    and Qiang Zhao (iHuman institute at ShanghaiTech University, Shanghai, China) for
    **providing the coordinates of the target complex structures ahead of publication**".
  - p4→p5 (the answers arrived after the deadline): "An important aspect of the GPCR Dock 2021
    assessment was the availability, **after the model submission deadline**, of multiple
    experimental 'answers' for four out of five studied complexes (all except APJ/cmpd6,
    Supp. Data 1)".
  - p5 (GPR139): "In the case of GPR139, GPCR Dock 2021 capitalized on the structures from the
    cryo-EM study [89] that were **solved shortly prior but still unpublished at the time of
    the assessment**."
  - p5 (OPRK): "Another cryo-EM structure … was **released on 2022-12-14 (PDB 8F7W [91]),
    after the GPCR Dock 2021 model submission deadline** and while this paper was in
    progress."
  - p5 (NPY1R): "one cryo-EM structure (PDB 7X9A [92]) was solved by the Qiang Zhao/Beili Wu
    collaboration at ShanghaiTech, **before the assessment (but not released until later)**".
  - p6 and p23 (two answers were never released at all): p6 — "the **unpublished**
    ShanghaiTech X-ray structure for APJ-Cmpd6"; p4 — "For APJ, **no published structures still
    exist with cmpd6**"; p23 Data availability — "**Except for APJ21** (the X-ray structure of
    the APJ/Cmpd-6 complex, Table 1 and Supp. Data 1) **and pre-7XK8** (the preliminary
    refinement of the NMUR2/Neuromedin-U-25 complex structure, Table 1 and Supp. Data 2), the
    structures of the experimental 'answers' are available in the PDB under accession codes
    listed in Table 1)."
  - **What participants COULD legitimately see** is fully enumerated in
    `structural_priors_used` above and is *not* leakage: those are different complexes of the
    same or homologous receptors, publicly deposited before the competition, and the paper
    states so target by target on p3–p4. The nearest thing to a compromised target is APJ,
    where a peptide-bound structure (5VBL) shared pharmacophores with Cmpd6 — and the paper
    says this **misled** rather than helped: p3, "The crystalized constrained peptide AMG3054
    had features similar to Cmpd6 but their spatial arrangement in the pocket was quite
    different (Fig. 1F), which might have misguided attempts of 3D-pharmacophore-assisted
    ligand docking."
  - **Route 1 for the assessor-side AF3-era arm: UNVERIFIABLE, and the paper never asks.**
    The runs were made in late 2024 (Chai-1 "server implementation … accessed Nov 13, 2024",
    p22), by which date every answer except APJ21 and pre-7XK8 was in the PDB (Tables 1–2,
    p20; earliest release 2021-12-29, latest 2024-12-04). **The paper reports no training
    cutoff for AlphaFold3, Boltz-1, Chai-1 or NeuralPLexer, and runs no post-cutoff control.**
    So whether those four models had seen the answers cannot be settled from this PDF. Do not
    assert either way. Recorded again under `anti_memorization_control` and `unresolved`.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving
  templates or alignments. NONE FOUND at assessment level; PRESENT in one participant
  pipeline.** The assessment protocol (p21–p22) uses Ballesteros-Weinstein position ranges to
  define the TM superposition (p21: "residue positions 1.30-1.60, 2.39-2.64, 3.22-3.54,
  4.38-4.64, 5.35-5.64, 6.31-6.58, 7.32-7.55 in Ballesteros-Weinstein notation [123]") and
  hand-listed residue ranges for the loops — a generic GPCR numbering convention, not a
  state-annotated database, and applied identically to model and answer. No GPCRdb, KLIFS or
  Kincore query appears anywhere. **The one participant exception**, p9 (MSU-Feig, the winning
  NPY1R model): "the receptor was first modeled using the **Multi-State GPCR modeling protocol
  [107]** and then used as a **template in AlphaFold Multimer, to bias the predictions towards
  the active state of the complex**." That is a state-annotated template bias, applied by a
  participant, and it produced the best NPY1R model. It is not leakage — the target's state
  (active, agonist-bound) is inferable from the ligand being an agonist without seeing the
  answer — but it is the one place in the corpus where state-annotated templating appears
  *inside a blind competition* and it won its target.

  **Route 3 — cluster labels derived from known states. NONE FOUND.** Clustering appears twice
  and neither instance is labelled by state. p9 (SIAT-Yuan): MD frames were clustered and a
  "representative conformation from the clustered simulation frames" selected — an
  unsupervised structural clustering of that group's own trajectory. p9 (ShanghaiTech-Bai):
  "MD frames were clustered, the averaged conformations were further energetically refined and
  scored by MM-GBSA in Schrödinger." No state labels are attached to any cluster anywhere in
  the paper.

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
  states. NONE FOUND, and the paper takes an explicit step to prevent it.** The scoring
  function was frozen before this round: p22 — "The background set (34,317 pairs of PDB
  complexes representing 1390 proteins) and the equation for this calculation were **exactly
  taken from [17]** to ensure that the results are directly comparable to prior assessments";
  p13 — "we chose to rely on the distribution of assessment parameters among the
  high-resolution X-ray structures of identical complexes **as it existed in the PDB in 2013**;
  this allowed us to quantify the improvements in model accuracy relative to prior
  assessments." Contact-strength thresholds are likewise inherited, not fitted: p22 — "the
  'strength' was assigned to 1 for d < dmin = 3.23 Å, 0 for d > dmax = 4.63 Å … as previously
  described [16,17,126]". The assessor AF3-era arm uses stock settings: p22 — AF3 "with default
  parameters", Boltz-1 "with the default Boltz-1 model checkpoint, 3 recycling steps, 200
  sampling steps, default `--step_scale` (1.638)". Seeds are fixed counts, not swept (AF3 and
  Boltz-1 "3 seeds and 5 models per seed"; Chai-1 "2 seeds and 5 models per seed"). **No
  parameter, range, or threshold in this paper was chosen against the five answers.**

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had. PRESENT, BY
  DESIGN — this is the definition of the assessment, not a defect, but two sub-choices were
  made after the answers were in hand and should be recorded honestly.**
  - The metric itself: p6 — "The primary criteria for this assessment included ligand position,
    assessed as the RMSD on its non-hydrogen atoms following optimal superimposition of the
    receptors, and the shared atomic contacts between the ligand and the receptor (Supp.
    Fig. 3). These two criteria were converted into a single score representing the likelihood
    of observing similar deviations among experimentally solved high-resolution X-ray
    co-crystal structures (the so-called model ''correctness'' [16,17]) and used for final
    model ranking." This is exactly what a blind assessment is supposed to do — the reference
    was withheld from predictors and applied afterwards by assessors. Scored against a
    reference the *assessors* held, not one the *predictors* held.
  - **Sub-choice A, the 'gold standard' answer, chosen post hoc.** p5–p6: "we ran all model
    analyses against each. However, in the remaining parts of the manuscript below, we
    primarily focus on model comparisons to **the highest resolution structure of each
    complex**". p13 states the rule and its one exception: "For 4 out of 5 targets, this was
    the structure with a better resolution, even though for some targets, the differences were
    marginal (3.20 Å vs 3.22 Å for PDB 7VUG vs 7VUH for GPR139; 3.19 Å vs 3.20 Å for PDB 8F7W
    vs 7Y1F for OPRK). For NPY1R, the declared experimental resolution of the two structures,
    PDB 7X9A and 7VGX, was the same (3.20 Å) so we chose a more complete structure PDB 7X9A."
    The rule is stated, is resolution-based rather than result-based, and **all alternatives
    are also reported** (Supp. Figs 4, 6, 8; numbers repeated in text on p13), which defuses
    the concern. But the choice was made with all answers visible.
  - **Sub-choice B, the assessed peptide window, chosen post hoc — and it changes the
    headline number by 4×.** p6: "The OPRK structures were solved with Dynorphin A (1-13);
    however, its C-terminal part was completely unresolved in both structures … prompting us to
    focus on predictions for **aa 1-8 only**. We also ran a **secondary set of analyses for the
    distal N-terminal part, aa 1-5**, which effectively form another OPRK agonist,
    Leu-enkephalin." Similarly "we focused our attention on predictions for the peptide core
    (aa 21-36)" for NPY and "the core (18-25 aa)" for NMUR2. Restricting dynorphin to aa 1–5
    raises the best correctness from 0.7% to 2.88% (p9). The justification given is disorder in
    the answer — legitimate — but the window was necessarily selected after seeing which
    residues the answer resolved, and the aa 1–5 window in particular is described as the
    "well-constrained" part (p10). Both windows are reported, so nothing is hidden.

  **Route 6 — best/worst model labels assigned against a held reference. PRESENT, BY DESIGN.**
  Every "top-ranking", "winning" and "best" label in the paper is assigned by correctness
  against the withheld answer — e.g. p7, "The correctness for the best-ranking model of the
  APJ/Cmpd6 complex, SDU-Yang (model APJ-1912-0005) was 0.61%". This is the entire point of an
  assessment. **The participants' own self-ranking is separate and is not analysed:** groups
  submitted up to five models in their own order (p21) and the paper never asks whether a
  group's own model 1 was its best. That is a missed control, not leakage. Note also that the
  label is reference-dependent in a way the paper is upfront about: the best APJ model changes
  identity depending on which answer is used (SDU-Yang APJ-1912-0005 vs the X-ray, correctness
  0.61%; KIST-Park APJ-8824-0001 vs the CMF-019 MCS in 8XZI, correctness 5%) — p7.

  **Route 7 — design-level oracle use (systems or conditions chosen because the expected
  answer is known). NONE FOUND for the community assessment; PRESENT for the assessors'
  AF3-era arm, and this is design-level only, weaker than pipeline leakage.**
  - For the assessment: targets were chosen because their structures were *newly solved and
    unreleased*, i.e. precisely because the answer was **unknown to the field** — the inverse
    of route 7. p2: "capitalizes on recently solved and yet-unpublished experimental
    structures". The only expectation declared in advance is the receptor's functional state,
    and that follows from the ligand being an agonist rather than from any structure. Note also
    that the assessors' own institution solved four of the answers (ShanghaiTech, p5) and
    ShanghaiTech-Bai was a participating group that won NMUR2 (p9) — the paper does not discuss
    this potential conflict, and the model submission system was blind and online (p21), but it
    is worth flagging. See `unresolved`.
  - For the AF3-era arm (p12, Methods p22): the four next-generation models were run **in
    2024, on targets whose answers the assessors already held and had already scored**, and the
    result is reported as which method matched which known geometry — "none of the four methods
    predicted the CMF-019-like geometry (similar to PDB 8xzi) and only Boltz-1 predicted the
    geometry similar to our X-ray structure of APJ/Cmpd6 (Supp. Fig. 10)" (p12). The expected
    answers were fully in hand before the run. This is a retrospective comparator bolted onto a
    prospective paper. Label it design-level; there is no evidence of anything being fed to the
    models, only that the evaluation is retrospective.

- **prospective**: **YES for the community assessment (the paper's substance, 886 scored
  models across 5 targets); NO for the assessors' AlphaFold3/Boltz-1/Chai-1/NeuralPLexer arm
  (p12, Methods p22). Overall: `partial`, but the partiality is lopsided — the prospective
  half is the paper and the retrospective half is one paragraph plus a supplementary figure
  that is not held.**
  Why prospective, on the evidence rather than the authors' word: the answers were unpublished
  and unreleased at the submission deadline (p2, p4, p5), were transferred privately to the
  assessors ahead of publication (p22), two of them are *still* unreleased in 2025 (p23), and
  the release dates in Tables 1–2 (p20) — 2021-12-29 at the earliest, through 2024-12-04 —
  all postdate the deadline. Predictions were made from sequence plus a 2D ligand structure
  (p2). This is the strongest available answer to `oracle_leakage` route 5 and route 7 in the
  corpus: routes 5 and 6 are present but are applied by the assessors *after* the predictions
  were locked, which is the only configuration in which they are not a defect.
  **The one gap that keeps this from being airtight: the submission deadline date is never
  stated.** See `unresolved` item 1.

- **state_metric**: **`RMSD-to-reference` + `continuous coordinate` — and the object measured
  is LIGAND POSE and RECEPTOR FOLD, never conformational STATE.** Read this field together
  with `unresolved` item 3.
  - **Primary (both small-molecule and peptide targets):** ligand heavy-atom RMSD to the answer
    after optimal TM superposition, plus fraction of correctly predicted ligand–receptor
    contacts, combined into a single percentile score, "correctness". p6: "The primary criteria
    for this assessment included ligand position, assessed as the RMSD on its non-hydrogen
    atoms following optimal superimposition of the receptors, and the shared atomic contacts
    between the ligand and the receptor". p22 gives the contact definition with **explicit,
    justified-by-citation thresholds**: "the 'strength' was assigned to 1 for d < dmin =
    **3.23 Å**, 0 for d > dmax = **4.63 Å**, and continuously decreased from 1 to 0 as a linear
    function of d for dmin < d < dmax", with the justification being consistency with refs
    [16,17,126]. Contact accuracy is the mean of recall and precision computed on a continuous
    contact-strength matrix (p22).
  - **Correctness is a percentile, not a distance:** it is the model's rank within the
    distribution of RMSD/contact deviations observed **between pairs of high-resolution X-ray
    structures of identical composition**, 34,317 pairs over 1,390 proteins, frozen at the 2013
    PDB (p22, p13). Reported "in percent of the experimental pair distribution" (p7). A model
    at 3.91% correctness is therefore "closer to the answer than 96.09% of pairs of independent
    high-resolution crystal structures of the same complex are to each other" — this is the
    interpretation the paper leans on for its headline claim, and it is what makes
    "exceeds low-resolution experimental structures" a measurable rather than rhetorical
    statement.
  - **Secondary, peptide targets only:** DockQ. p6: "For peptide targets, DockQ score [96],
    which takes the CAPRI measures [97–99] and formulates them into a single score for the
    protein-docking quality assessment, was included in this round of GPCR Dock for a
    comparison". Result, p9: "As expected, DockQ scores correlated well with our 'correctness'
    scores (Supp.Fig. 7), as the core equation of the DockQ metric similarly relies on LRMS
    (ligand RMSD) and Fnat (fraction of correct contacts)."
  - **Receptor side:** backbone RMSD of the TM bundle and of ECL1/ECL2/ECL3 after TM
    superposition (p21, Fig 4 p18). Reported both as continuous radar traces and as the
    fraction of models under **1 Å, 2 Å or 3 Å** cutoffs (p10–p11). **Those cutoffs are used
    without any stated justification** — 1 Å, 2 Å and 3 Å appear in the results text with no
    definition, no citation and no threshold rationale anywhere in Methods.
  - **`binary predicate`: NOT USED for state.** No predicate of the form "active if X" or
    "inactive if Y" exists anywhere. No TM6 displacement, no DRY/NPxxY measure, no activation
    index, no state classifier.
  - **`visual only`: partially present, on the participant side, as a model-selection
    criterion.** KIST-Park "picked models 1-3 by visual inspection" (p7); ShanghaiTech-Bai —
    "Model selection for the submission was guided by both MM-GBSA binding energies and visual
    inspection" (p9). The assessors themselves never call anything by eye.

- **metric_saturation**: **Yes, in two arms, and both floor rather than ceiling.**
  1. **The receptor-loop cutoff arm floors at exactly zero.** p10 (APJ): "ECL3 was not
     predicted within that accuracy [1 Å] by **any** of the models"; "Relative to PDB 8XZI,
     21.4% of the models had ECL1 RMSD within 1Å, and **none** achieved this cutoff for ECL2 or
     ECL3". p10 (GPR139): "**none** had any of the three ECLs within this cutoff". p10 (OPRK):
     "**none** had ECL2/3 RMSD below 1Å". p10 (NPY1R): "**none** had ECL2 or ECL3 below not only
     1Å but also 2Å". p11 (NMUR2): "**No** models had ECL2 RMSD of < 2Å". With 0/206, 0/198,
     0/175, 0/155 and 0/152 the 1 Å ECL predicate cannot discriminate between methods at all
     for ECL2 and ECL3 — the arm is uninformative below the floor, and the paper has to fall
     back on the 2 Å and 3 Å cutoffs for NPY1R and OPRK to recover any signal.
  2. **The correctness scale is compressed against zero across its whole reported range.**
     Correctness is a 0–100% percentile; the maximum ever achieved by any of 886 models on any
     target against any reference is **5%** (p7), and the modal value sits near 0.05%. Fig 5
     (p19) is drawn on a log axis with a literal "0" tick at the bottom, so exactly-zero models
     cannot be placed. Some arms are essentially pinned to the floor: APJ conventional homology
     best = **0.04%** across 11 models (p11).
  Neither is an axis artefact; both are numeric. The related *figure* defects (the log axis
  with a 0 tick; the "N/A" cells in Fig 5A/C) are recorded in `hides`, per the v3 split.

- **directional_control**: **The assessment itself has no handle — it does not instruct
  anything, it scores. The handles that appear are participant-side, and the paper's central
  method finding is about which handle worked.**
  - **Peptide co-folding (the winning handle for two of three peptide targets).** p11: "For
    NPY1R and NMUR2, peptide docking to a homology model, to an apo AlphaFold2 model, or (in
    the case of NPY1R) to an experimental structure produced approximately the same levels of
    accuracy, well below 1% (Fig. 5C). **The real improvement in both cases was achieved when
    AlphaFold was used in the Multimer mode for co-folding the receptor with the peptide**
    (Fig. 5C)."
  - **A state-annotated template, used to steer AF-Multimer to the active state.** p9
    (MSU-Feig, winning NPY1R model): "the receptor was first modeled using the Multi-State GPCR
    modeling protocol [107] and then used as a template in AlphaFold Multimer, **to bias the
    predictions towards the active state of the complex**." This is the only explicit
    state-directing intervention in the paper.
  - **MD restraints used to open a pocket.** p9 (SIAT-Yuan, winning OPRK model): "refined it
    with a 200 ns restrained all-atom MD simulation in GROMACS using CHARMM36m force field,
    **to open up the binding pocket and thus enable peptide docking**."
  - **Apo prediction followed by docking** — the necessary route for small molecules, and a
    limitation the paper names: p11, "For small molecule targets (APJ and GPR139), the
    receptors **could only be predicted in the apo form** and required subsequent ligand
    docking."
  - **Seeds:** used only as replicate counts in the assessors' AF3-era arm (p22), never as a
    state handle.
  - **The handle that does NOT exist:** nothing in this paper can be instructed to produce an
    inactive receptor. Every target is active; the question is never posed. p13 names this as
    an AF2 limitation without testing it: "two limitations of AF2 affected prediction accuracy:
    (i) **inability to systematically and reproducibly predict receptor conformational
    ensembles and distinct functional states [107]**, and (ii) understandably lower prediction
    accuracy (and certainty) for receptor loops and flexible parts [22]."

- **anti_memorization_design**: **YES — and it is the strongest form of it available: not a
  date-filtered held-out set but genuinely unpublished reference structures.**
  - **n = 5 targets** (886 scored models). The held-out property is per target, not per model.
  - **How the cutoff was defined: by the model submission deadline, not by a training-data
    date.** p4: answers became available "after the model submission deadline". p5: PDB 8F7W
    was "released on 2022-12-14 … after the GPCR Dock 2021 model submission deadline". The
    deadline itself is never dated (see `unresolved` 1). Bounds that can be read off the paper:
    it is at or after the July-2021 AF2 release ("Released only a few months before the
    assessment, AlphaFold2 became a go-to approach", p12) and — since the four GPR139 answers
    were "still unpublished at the time of the assessment" (p5) while Table 1 gives their
    release date as 2021-12-29 — on or before roughly the end of 2021.
  - **Answer release dates, all post-deadline (Tables 1–2, p20):** GPR139 7VUG/7VUH/7VUI/7VUJ
    2021-12-29; NPY1R 7VGX 2022-02-23, 7X9A 2022-05-18; NMUR2 7W55 2022-04-20, 7XK8 2023-02-22;
    OPRK 8F7W 2022-12-14, 7Y1F 2023-05-24; APJ 8XZI 2024-03-20, 8S4D 2024-12-04. **APJ21 and
    pre-7XK8: release date "n/a" — never released** (p20, p23).
  - **A second, weaker anti-memorization observation the paper makes in passing:** p8 — "This
    limitation could have affected the AF2 prediction accuracy for GPR139 **since the model is
    trained on existing structures**", and p13 — "This is consistent with other studies that
    demonstrated that AF2 prediction accuracy for GPCRs is **only loosely related to the
    representation of homologous receptors in the training set** [12,118]." The paper's own
    data support the second: p9 — "The maximum prediction accuracy did not correlate with the
    availability of the homologous experimental structures (Fig. 1B) as the most structurally
    characterized receptor - OPRK - turned out to be the most challenging."

- **anti_memorization_control**: **Split answer — a control arm was genuinely run for the
  participant assessment, and NONE RUN for the AF3-era arm.**
  - **Participant assessment: RUN, and it is the whole experiment.** All 886 models were
    scored against references that did not exist in public form when they were built. This is
    not a held-out set merely existing; it is the measured arm. Model-level n is large
    (206/198/175/155/152 per target). **Target-level n = 5, which is below the schema's ~10
    threshold** — so any statement of the form "AF2-based methods beat physics-based methods"
    rests on five targets and should be marked **UNPOWERED at the target level** even though it
    is well powered at the model level. The paper's own per-target results are heterogeneous
    enough to make this real: co-folding won NPY1R and NMUR2 and lost OPRK (p11).
  - **AF3-era arm: NONE RUN.** No training cutoff is reported for AlphaFold3, Boltz-1, Chai-1
    or NeuralPLexer; no post-cutoff or decoy control accompanies that arm; and the arm's only
    quantitative panel (Supp. Fig. 10) is not in the held PDF. The four models were run in late
    2024 against structures released between 2021-12-29 and 2024-12-04. Whether the comparison
    is contaminated is **unanswerable from this paper**.
  - **Also not run:** no scrambled-sequence, decoy-ligand, wrong-receptor or random-pose null
    arm exists. The null the paper does use is the *experiment-versus-experiment* comparison
    (below), which is a better null than a decoy but answers a different question.

- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Every model scored against **all** available experimental answers, not just one (4 of 5 targets have ≥2) | That the ranking is an artefact of one arbitrarily chosen reference structure | p5–p6 ("we ran all model analyses against each"), p13, Supp. Figs 4/6/8 |
  | **Experiment-vs-experiment** RMSD/contact values projected onto the same axes as the models (yellow squares, Fig 2B; Fig 3A/C/E) | That "close to the answer" is being judged with no scale — supplies the experimental-error floor against which "approaches experimental accuracy" is defined | p7, p19 (Fig 2–3 legends p16–p17) |
  | Scoring background frozen at the **2013 PDB** (34,317 pairs, 1,390 proteins), imported unchanged from ref [17] | That the metric was tuned on this round's data; also makes the 2010/2013/2021 comparison legitimate | p22, p13 |
  | **DockQ** computed independently for all peptide targets and correlated against 'correctness' | That the headline ranking is an artefact of the bespoke GPCR Dock metric | p6, p9, Supp. Fig. 7 |
  | **Uninterpretable-model filter**: no ligand, no receptor, or steric-clash penalty sum > 3,000 → excluded (18 models) | That physically impossible complexes contribute to the distributions | p6, p21, p22 |
  | **Model standardisation**: fusion proteins/non-native helices deleted, ligand atoms renamed to topological identity with the target ligand, all non-receptor/non-ligand molecules removed | That scoring differences come from submission formatting rather than from geometry | p21 |
  | **Group de-duplication and random 5-model down-selection** (49 groups → 45; HUST-Huang-3983 + -8470 merged, Tsinghua-Peng-6760 + HeliXon-Luo-6867 merged, Galux-Won-4528 + Seoul-Seok-8669 merged; KIST-Park-8824's 9 effective OPRK models cut to 5 at random) | That one PI's multiple entries inflate a method's apparent success rate | p21 |
  | **Method-stratified correctness distributions** (AF apo / AF complex / conventional homology / docking to a PDB structure / GEnSeMBLE / unknown) | That success is method-independent; this is the arm that supports the AF2-vs-physics conclusion | p11, Fig 5A/C p19 |
  | **Cross-round comparison** to GPCR Dock 2010 and 2013 on the same metric | That 2021 accuracy cannot be placed on a historical scale | p12, Fig 5B/D p19 |
  | **Receptor-side TM/ECL RMSD analysis** run separately from ligand scoring | That a good ligand pose is being credited to a bad receptor model, or vice versa | p10–p11, Fig 4 p18 |
  | **Secondary evaluation window** for dynorphin (aa 1–5, "which effectively forms another OPRK agonist, Leu-enkephalin") alongside the primary aa 1–8 | That the OPRK failure is an artefact of scoring a poorly-constrained peptide tail | p6, p9 |
  | **Post-hoc AF3/Boltz-1/Chai-1/NeuralPLexer end-to-end run** on the two small-molecule targets | Comparator, not a control — and itself uncontrolled (no training cutoff reported) | p12, p22, Supp. Fig. 10 (not held) |
  | **NOT RUN — participants' own model ranking (their submitted order 1–5) is never analysed** | Would have ruled out that "best model" success depends on the assessors' oracle ranking; the field's practical question, "could the group have picked it?", is left open | p21 (five models per group), never revisited |

- **confidence_as_discriminator**: **Yes — used by participants, for model selection, and never
  validated by the assessors.**
  - p7 (KIST-Park): "built the apo receptor model using AlphaFold2 and **selected the
    prediction with the highest pLDDT** for subsequent docking with Rosetta GALigandDock."
  - p9 (MSU-Feig, the best NPY1R model): "The **AlphaFold models with high confidence scores**
    were then submitted by the group without any further refinements."
  - Also used indirectly: KIST-Park picked "models 4-5 based on the rank predicted by
    **DeepAccNet-ligand score** [101]" (p7), a learned accuracy estimator rather than a native
    confidence head; SIAT-Yuan "trained a Convolutional Neural Network (CNN) on all the existing
    GPCR-ligand structures … used as the final step to select the final models" (p9).
  - **No validation.** The assessors never plot correctness against pLDDT/pTM/ipTM, never report
    a confidence value for any model, and never test whether confidence predicts correctness.
    The nearest statement is a bare assertion that selection matters, p8: "only one of the two
    AF2-based models, GPR139-2717-0003, had considerable accuracy; the remaining models were not
    successful (correctness between 0.2% and 0.03%), **highlighting the importance of strategic
    selection of diverse conformations**"; and p11: "not all AF2 models had comparable accuracy.
    This emphasizes that even when the best tools are available, one often needs expert
    knowledge about (i) how to apply them and (ii) how to rank and score/rank the resulting
    models." **Confidence-as-discriminator is asserted to matter and never measured.**

## D. Claims

- **central_conclusion**: In the only genuinely blind, post-AlphaFold community assessment of
  GPCR–ligand complex prediction, 45 groups' 886 scored models showed that AlphaFold2 —
  especially AF2-Multimer co-folding of receptor with peptide — drove the successes, that the
  best peptide-complex models (NMUR2 3.91%, NPY1R 1.32% correctness) match or beat the
  agreement between independent low-resolution experimental structures of the same complex,
  and that small-molecule complexes still lag: the best APJ model reached only 0.61%
  correctness against the target X-ray and no small-molecule prediction matched the best 2010
  result. Prediction success did not track the availability of homologous structures — the
  most structurally characterised receptor (OPRK) was the hardest target and the least
  characterised (NMUR2) the easiest. The authors conclude that expert-guided, physics-based
  modelling and high-resolution experimental structure determination remain necessary.

- **necessity_claims** (verbatim, with page):
  1. p1 (abstract): "However, our results highlight **the unwavering need for high-resolution
     GPCR structure determination, especially with small molecule chemicals, and for the
     concurrent application of physics-based and expert-guided modeling methods**."
  2. p14 (closing sentence — the same claim, sharpened): "However, all the recent successes in
     AI structural modeling **have not eliminated the need for experimental high-resolution
     GPCR structure determination** [122], especially with small molecule chemicals - a much
     needed prerequisite for structure-based drug discovery, - and for conventional,
     physics-based and expert-guided computational modeling and refinement."
  3. p14: "Therefore, **expert knowledge, incorporating information from compound SAR, and
     conventional model refinement remain important** for generating accurate predictions even
     in the era of AlphaFold2/3."
  4. p11: "This emphasizes that even when the best tools are available, **one often needs
     expert knowledge** about (i) how to apply them and (ii) how to rank and score/rank the
     resulting models."
  5. p11: "This said, **the use of best practices in subsequent compound docking / pose
     generation and pose scoring / selection was just as important as having the correct
     conformation of the receptor**, and so was an expert assessment of the complexes, for
     example to evaluate the pose consistency with SAR or to exclude poses with buried polar
     atoms that do not make hydrogen bonds (Supp. Data 4)."
  6. p10 (necessity of induced-fit modelling): "**Because accurate modeling of ligand
     geometries and interactions required the prediction of induced conformational
     rearrangements in the receptors**, we next assessed how well these rearrangements were
     predicted in the submitted models."
  7. p11 (a conditional necessity, stated with its own limit): "**Precise ligand placement
     generally required generally accurate prediction for the loops; however, this relationship
     was not strict and the reverse was not true** (not all accurate receptor models featured
     precise ligand placement)."
  8. p12 (a "not possible / intractable" claim about the prior state of the field): "**Peptide
     complexes have traditionally been considered most challenging and often intractable
     prediction targets**, due to a large number of rotatable bonds that had to be sampled in
     docking, as well as the uncertainties of induced fit."
  9. p13 (an inability claim about AF2, cited not measured): "For small-molecule complexes,
     which required compound docking, two limitations of AF2 affected prediction accuracy: (i)
     **inability to systematically and reproducibly predict receptor conformational ensembles
     and distinct functional states** [107], and (ii) understandably lower prediction accuracy
     (and certainty) for receptor loops and flexible parts [22]."
  10. p3 (a necessity about what a correct answer even is — the paper's most quotable framing
      of reference uncertainty): "This made us consider the following questions: Why are the
      ligand poses in these experimental structures so different? Are any of the experimental
      structures 'better' or more 'correct' than others? **And what is the ultimately 'correct'
      geometry of the complexes that the computational community should strive to predict?**"
      (p4).

- **novelty_claims** (verbatim, with page):
  1. p1 (abstract — the headline, and the one to quote): "**We demonstrate that thanks to the
     breakthroughs in AI-powered modeling, the accuracy of modern computational models of GPCR
     complexes with peptides can not only approach but also exceed that of low-resolution
     experimental structures.**"
  2. p14 (restated in the summary): "In summary, **our work demonstrated that the accuracy of
     computationally generated models of GPCR complexes with peptides can exceed that of
     low-resolution experimental structures.**"
  3. p13 (the supporting statement, with its small-molecule qualifier attached — quote both
     halves together or the qualifier is lost): "Altogether, these observations suggest that
     **for peptide complexes, predicted models can be as accurate as (or even more accurate
     than) low-resolution experimental structures. Similarly, for small-molecule complexes,
     best computationally generated models appear to be within the expected experimental error
     from at least one of the alternative complex geometries.**"
  4. p7 (the specific measured version): "Notably, we found that **a few best-ranking models of
     the GPR139/JNJ complex (orange circles in Fig. 2B) were closer to the experimental answer
     in PDB ID 7VUG than other, lower resolution experimental structures of the same complex
     (yellow squares in Fig. 2B) were to the same PDB.** Therefore, we concluded that **the
     precision of the top-ranking models was well within the experimental error observed in
     modern cryo-EM GPCR-ligand complex structures.**"
  5. p12 (first-ness of scale in the series): "The 4th, 2021 GPCR Dock assessment was different
     from prior assessments in the series (2008 [15], 2010 [16], 2013 [17]) in several ways.
     **First, it featured a larger number of targets: 5 target complexes of 5 receptors in GPCR
     Dock 2021 vs 1, 3, and 4 complexes of 1, 2, and 3 receptors, respectively, in GPCR Dock
     2008, 2010, and 2013.**"
  6. p6 (first use of DockQ in the series): "For peptide targets, DockQ score [96] … **was
     included in this round of GPCR Dock for a comparison**".
  7. p12 (a surprise finding stated as new): "**As a result, the challenges of predicting
     accurate receptor structures and complexes with larger peptides were largely solved.
     However, challenges for shorter peptides and small molecules remained, and induced fit was
     still a critical issue for these complexes.**"
  8. p13 (satisfaction claim about resolution tracking): "**It was surprising - and satisfying,
     - to see that best computational models generally more closely recapitulated higher
     resolution structures than their lower resolution alternatives.**"

  **Where small-molecule lags peptide, verbatim** (the paper's own comparative statements, all
  worth quoting):
  - p12: "Surprisingly, **none of the small-molecule predictions reached the best accuracy
    observed in 2010 for the DRD3/eticlopride complex** (Fig. 5B). The most CMF-019-like APJ
    prediction and the best GPR139/JNJ predictions had the level of similarity with the answer
    approaching that of best 2013 5HT1B/ergotamine and 5HT2B/ergotamine models in GPCR Dock
    2013 (Fig. 5B)." — i.e. **small-molecule accuracy did not improve in 11 years.**
  - p12: "In any case, **the prediction accuracy for all three peptide targets greatly exceeded
    that for the only peptide target in prior assessment: CXCR5/CVX15 in GPCR Dock 2010**
    (Fig. 5D)." (The receptor is CXCR4 elsewhere in the same paper, p12 — see `unresolved` 7.)
  - p6 (the section heading, which is itself a claim): "Small-molecule targets: ligand
    predictions for GPR139 but not APJ approach experimental accuracy."
  - p8 (peptide section heading): "Peptide targets: near-experimental accuracy for the core
    parts of neuropeptide Y (NPY1R) and neuromedin-25 (NMUR2), but not for dynorphin (OPRK)."
  - p14 (the AF3-era caveat): "Although the reported accuracy for these methods is excellent,
    **they may still have limitations when it comes to predictions for complexes without
    homology and chemical similarity to the training set structures [121] or with multiple
    'correct' complex geometries** (Supp. Fig. 10 and [12])."
  - p11 (AF2's own limits on peptides): "However, this approach did not work well for OPRK
    (Fig. 5C), possibly because the peptide was too short for building a reliable multiple
    sequence alignment (MSA). … **These examples thus illustrate the limitations of AlphaFold2
    in application to not only small-molecule but also to peptide complexes.**"

- **stated_limits** (the authors' own, and there are many — the paper is candid):
  1. **The answer itself is uncertain.** p6: "In conclusion, the dynamic nature of the target
     GPCR-ligand complexes, and possibly the limited resolution of the available experimental
     structures, **created substantial uncertainties in what would otherwise be considered the
     'correct' structure of each complex, and confounded the assessment of the computational
     models**."
  2. **Two independent structures of the same complex disagree by more than the models do.**
     p5 (APJ): "the root mean square deviation for the maximum common substructure (MCS) of the
     two compounds after optimal superimposition of the receptor TM domains is as high 9.9Å …
     the complete flip in the compound bindings pose (Supp. Fig. 1B) was still unexpected and
     hardly rationalizable." p13: "the multitude and diversity of structural forms of GPCR
     complexes of the same composition is increasingly being appreciated [114–116] and
     **affects the definition of 'success' in structural modeling [117]**."
  3. **The gold standard was chosen by resolution, and the margins are marginal.** p13: "For 4
     out of 5 targets, this was the structure with a better resolution, even though for some
     targets, **the differences were marginal (3.20 Å vs 3.22 Å for PDB 7VUG vs 7VUH for
     GPR139; 3.19 Å vs 3.20 Å for PDB 8F7W vs 7Y1F for OPRK)**."
  4. **APJ cannot be resolved at all.** p13: "For APJ, due to the profound differences in the
     binding pose of congeners Cmpd6 and CMF-019 … **it is hard to conclusively relate the model
     success to structure resolution**".
  5. **G-protein interactions were not evaluated**, despite being present in all five answers.
     p3: "predictions for receptor interactions with the G proteins were not evaluated as part
     of the assessment."
  6. **Method information is incomplete for a quarter of models.** p11: "methods were provided
     for 150 of 201 APJ/Cmpd6 models, 155 of 198 GPR139/JNJ models, 128 of 170 OPRK/dynorphin
     models, 119 of 155 NPY1R/NPY models, and 115 of 152 NMUR2/NMU25 models". Every
     method-stratified conclusion (Fig 5A/C) therefore rests on 74–84% of the models, and
     Table 3 carries an explicit "Other/unknown" column.
  7. **The strongest possible entrant declined.** p11: "it would have been interesting to see
     the predictions of DeepMind scientists who were invited to participate but unfortunately
     declined." (So no reference implementation of AF2 by its authors is in the set.)
  8. **Peptide tails were unresolved and had to be excluded from scoring.** p6, and its
     consequence at p9: OPRK correctness 0.7% on aa 1–8 vs 2.88% on aa 1–5.
  9. **Prior structures may hurt as well as help.** p12: "by biasing modeling efforts, the
     available structures can have a detrimental effect on modeling success when the target
     complex is sufficiently conformationally distinct."
  10. **AF2 has two named limitations for small molecules** — no reliable conformational
      ensembles/states, and poor loops (p13, quoted in full under `necessity_claims` 9).
  11. **AF3-generation models are not exempt** (p14, quoted above under lag statements).

- **stance**: **`precedent` + `background`** — provisional, the user's call.
  - **`precedent`, and the strongest kind:** this is a genuinely prospective, genuinely blind,
    community-scale assessment of GPCR–ligand complex prediction in the AlphaFold era. Nothing
    else in this corpus has answers that were unpublished at prediction time, and two of these
    answers are unreleased to this day. Any claim we make that a retrospective benchmark
    overstates performance can be anchored to this paper's numbers. It is also precedent for
    the *framing* that a prediction can beat a low-resolution experiment, and for using
    experiment-vs-experiment agreement as the accuracy floor.
  - **`background` on the conformational-state question:** the paper never scores state. All
    five targets are active; the metric is pose plus fold. So it cannot corroborate or
    contradict a state-prediction claim, and its "AF2 cannot predict distinct functional
    states" line (p13) is a citation to ref [107], not a measurement made here.
  - **Not `contrast`:** the design is more rigorous than most of the corpus, not less. The only
    rigour defects are the un-analysed participant self-ranking, the unreported submission
    deadline, and the uncontrolled AF3-era arm — none of which is a strawman we would argue
    against.
  - **Not `threat`:** it predates and does not attempt the state problem.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Participating groups | 45 (49 registered; 1 withdrew, 3 pairs merged) | groups | — | p6, p21 |
  | Countries represented | 14 | countries | Supp. Fig. 2A (not held) | p6 |
  | Models submitted | 904 | models | — | p6 |
  | Models uninterpretable and removed | 18 | models | no ligand / no receptor / clash penalty sum > 3,000 | p6, p21–p22 |
  | Models assessed, per target | 206 / 198 / 175 / 155 / 152 (APJ / GPR139 / OPRK / NPY1R / NMUR2); total 886 | models | — | p6, p21 |
  | **Best correctness, APJ/Cmpd6** | **0.61%** (SDU-Yang, APJ-1912-0005) | percentile of high-res X-ray pair distribution | unpublished ShanghaiTech APJ/Cmpd6 X-ray, 2.40 Å | p7 |
  | Best APJ ligand RMSD / contacts | 3.47 Å / 31.3% | Å / % correct contacts | same | p7 |
  | Best correctness, APJ vs CMF-019 MCS | **5%** (KIST-Park, APJ-8824-0001); ≥5 more models above 1% | percentile | PDB 8XZI (CMF-019, 2.70 Å cryo-EM) | p7 |
  | Best APJ MCS RMSD / contacts vs 8XZI | 1.18 Å / 51.2% | Å / % | PDB 8XZI | p7 |
  | **Best correctness, GPR139/JNJ-63533054** | **2.50%** (UW-DiMiao, GPR139-2717-0003) | percentile | PDB 7VUG, 3.20 Å | p7 |
  | Best GPR139 ligand RMSD / contacts | 2.05 Å / 47.80% | Å / % | PDB 7VUG | p7 |
  | Best correctness, GPR139 vs alternative | 1.45% (1.41% for GPR139-8824-0005, KIST-Park, 2.08 Å / 34.74%) | percentile | PDB 7VUH, 3.22 Å | p13, p7 |
  | **Best correctness, OPRK/dynorphin (aa 1–8)** | **0.7%** (SIAT-Yuan, OPRK-8407-0003); 0.59% (Uppsala-Carlsson, OPRK-2736-0004) | percentile | PDB 8F7W, 3.19 Å | p8 |
  | Best OPRK RMSD / contacts (aa 1–8) | 2.96 Å / 28.55%; second 3.40 Å / 29.45% | Å / % | PDB 8F7W | p8 |
  | Best correctness, OPRK vs 7Y1F | 0.24% (model 8321-0003), 4.03 Å, 14.4% | percentile / Å / % | PDB 7Y1F, 3.20 Å | p8 |
  | **Best correctness, OPRK restricted to aa 1–5 (Leu-enkephalin)** | **2.88%** (OPRK-8407-0003, 1.79 Å, 47.3%) vs 8F7W; 1.06% (OPRK-8669-0003, 2.08 Å, 28.34%) vs 7Y1F | percentile | PDB 8F7W / 7Y1F | p8 |
  | **Best correctness, NPY1R/NPY (aa 21–36)** | **1.32%** (MSU-Feig, NPY1R-3601-0005) | percentile | PDB 7X9A, 3.20 Å | p8 |
  | Best NPY1R RMSD / contacts | 1.99 Å / 32.12% | Å / % | PDB 7X9A | p8 |
  | Best correctness, NPY1R vs 7VGX | 1.44%; **11 models ≥1%** | percentile | PDB 7VGX, 3.20 Å | p13, p8 |
  | Distribution, NPY1R models | ~half of submitted models at 2–4 Å ligand-core RMSD; bimodal correctness distribution | Å | PDB 7X9A | p8, p10 |
  | **Best correctness, NMUR2/NMU25 (aa 18–25)** | **3.91%** (ShanghaiTech-Bai, NMUR2-7750-0004) — the highest of any target | percentile | PDB 7W55, 2.80 Å | p9 |
  | Best NMUR2 RMSD / contacts | 1.5 Å / 50.21% | Å / % | PDB 7W55 | p9 |
  | Best correctness, NMUR2 vs 7XK8 / pre-7XK8 | 0.42%–0.48% only | percentile | PDB 7XK8, 3.30 Å | p9, p13 |
  | **AF2 use, % of models with methods** | 40.7 / 68.4 / 54.7 / 82.4 / 84.3 (APJ / GPR139 / OPRK / NPY1R / NMUR2) | % | Table 3 | p11, p20 |
  | **AF2 use, % of all submitted models** | 30.3 / 53.5 / 41.2 / 63.2 / 63.8 | % | Table 3 | p20 |
  | AF apo vs AF complex (co-folding) split | APJ 61/0, GPR139 106/0, OPRK 61/9, NPY1R 36/62, NMUR2 31/66 | models | Table 3 | p20 |
  | Models with methods reported | 150/201, 155/198, 128/170, 119/155, 115/152 | models | Table 3 | p11, p20 |
  | **APJ by method — docking into an existing PDB structure** | best correctness **0.22%** (86 models) vs X-ray; 1.3% vs 8XZI | percentile | Fig 5A / Supp. Fig. 9 | p11 |
  | **APJ by method — GEnSeMBLE (physics/systematic conformational search)** | best **0.35%** vs X-ray; **0.02%** vs 8XZI | percentile | Fig 5A / Supp. Fig. 9 | p11 |
  | **APJ by method — conventional homology** | best **0.04%** (11 models) vs X-ray; 0.2% vs 8XZI | percentile | Fig 5A / Supp. Fig. 9 | p11 |
  | **GPR139 by method — conventional homology** | best **0.82%** (44 models) | percentile | Fig 5A | p11 |
  | **Head-to-head verdict, small molecules** | "AlphaFold2-generated models seem to have performed best for both small-molecule targets (Fig. 5A)" | — | Fig 5A | p11 |
  | **Head-to-head verdict, peptides** | docking to homology model / apo AF2 model / experimental structure all "well below 1%"; co-folding with AF-Multimer is "the real improvement" for NPY1R and NMUR2, but failed for OPRK | percentile | Fig 5C | p11 |
  | TM domain backbone RMSD < 1 Å | APJ 70%; GPR139 ~3%; OPRK ~33%; NPY1R 17.42%; NMUR2 12.5% | % of models | gold-standard answers | p10–p11 |
  | ECL1 backbone RMSD < 1 Å | APJ 16.5% (21.4% vs 8XZI); GPR139 0%; OPRK 2 models; NPY1R 26.45%; NMUR2 4.6% | % of models | gold-standard answers | p10–p11 |
  | ECL2 backbone RMSD < 1 Å | APJ 4.85%; GPR139 0%; OPRK 0%; NPY1R 0% (also 0% at <2 Å); NMUR2 0% at <2 Å | % of models | gold-standard answers | p10–p11 |
  | ECL3 backbone RMSD < 1 Å | APJ **0% of 206**; GPR139 0%; OPRK 0%; NPY1R 0% (also 0% at <2 Å); NMUR2 15.79% at <2 Å | % of models | gold-standard answers | p10–p11 |
  | ECL RMSD < 2 Å, OPRK | ECL1 56.57%, ECL2 38.29%, ECL3 47.43% | % of models | PDB 8F7W | p10 |
  | ECL RMSD < 3 Å, NPY1R | ECL2 46.45%, ECL3 59.35% | % of models | PDB 7X9A | p10 |
  | Overall ECL2 spread across models | 0.5–16 Å | Å backbone RMSD | all targets | p10 |
  | **Experimental-vs-experimental disagreement, APJ** | **9.9 Å** MCS RMSD between Cmpd6 (X-ray 2.40 Å) and CMF-019 (8XZI 2.70 Å) after TM superposition; complete pose flip | Å | structure vs structure | p4–p5 |
  | Experimental disagreement, GPR139 | pairwise ligand RMSD 0.4–2.8 Å across 4 structures + 2 alternate conformers; W170(ECL2) lowered >3 Å in 7VUG; vertical shifts up to 1.8 Å | Å | structure vs structure | p5 |
  | Experimental disagreement, OPRK | 2.87 Å backbone RMSD between dynorphin N-termini in 7Y1F and 8F7W | Å | structure vs structure | p5 |
  | Experimental disagreement, NPY1R | 2.0 Å heavy-atom peptide RMSD; TM helices systematically 1–1.5 Å shorter in 7X9A (44.08 vs 45.58 Å R254(6.26)–T284(6.56)) | Å | structure vs structure | p5 |
  | Experimental disagreement, NMUR2 | 2.65 Å backbone / **4.03 Å** all-heavy-atom peptide RMSD; Phe19 and Leu20 point in opposite directions | Å | structure vs structure | p5 |
  | Scoring background set | 34,317 pairs of PDB complexes representing 1,390 proteins, frozen at the 2013 PDB | pairs / proteins | — | p22, p13 |
  | Contact-strength thresholds | dmin = 3.23 Å (strength 1), dmax = 4.63 Å (strength 0), linear between; clash penalty Σ(dmin/d − 1) > 3,000 ⇒ sterically impossible | Å / unitless | — | p22 |
  | AF3-era arm, APJ/Cmpd6 | "none of the four methods predicted the CMF-019-like geometry (similar to PDB 8xzi) and **only Boltz-1** predicted the geometry similar to our X-ray structure of APJ/Cmpd6" | qualitative | APJ21 X-ray and PDB 8XZI | p12 |
  | AF3-era arm, GPR139 | "only Boltz-1 predictions reached the accuracy of the best models in this assessment" | qualitative | PDB 7VUG | p12 |
  | Cross-round, small molecules | no 2021 small-molecule prediction reached the best 2010 DRD3/eticlopride accuracy; best 2021 approaches best 2013 5HT1B/5HT2B-ergotamine | percentile | GPCR Dock 2010 / 2013 | p12, Fig 5B |
  | Cross-round, peptides | all three 2021 peptide targets "greatly exceeded" the 2010 CXCR4/CVX15 result | percentile | GPCR Dock 2010 | p12, Fig 5D |
  | Prior rounds' scale | 1, 3 and 4 complexes of 1, 2 and 3 receptors in 2008, 2010, 2013 | complexes / receptors | — | p12 |

  **No error bars, confidence intervals, or significance tests appear anywhere in the paper.**
  Every comparison between methods, targets or rounds is made on point estimates and
  distribution shapes.

- **n_predictions**: **Record the three levels separately.**
  - **Samples per target per group:** up to 5. p21: "Groups were invited to submit up to five
    models per target." (KIST-Park's OPRK submission effectively contained 9 and was cut to 5
    at random, p21.)
  - **Targets:** 5 complexes / 5 receptors (p3).
  - **Total submitted:** 904 models from 45 groups (p6). **Total assessed: 886**
    (206+198+175+155+152, p6/p21) after removing 18 uninterpretable models. Per-target n is the
    number that matters for every distribution in Figs 2–5.
  - **Assessors' AF3-era arm (separate, retrospective):** NeuralPLexer 16 predictions
    (`--chunk-size=2 --num-steps=40 --sampler=langevin_simulated_annealing`); Chai-1 10 (2 seeds
    × 5 models); Boltz-1 15 (3 seeds × 5); AlphaFold3 v3.0.1 15 (3 seeds × 5) — p22. The
    Methods heading says "End-to-end modeling of **APJ/Cmpd6** complexes" only, while the
    Results (p12) also report GPR139 numbers, so **whether these counts also apply to GPR139 is
    NOT REPORTED**.
  - **Power note:** 886 models is a large model-level n but the target-level n is 5, and the
    method-stratified arms are small (11 APJ conventional-homology models; 44 GPR139
    conventional-homology models; 86 APJ PDB-docking models — p11).

- **comparable_to_ours**: *(left empty by the extractor — per schema v3)*

- **si_in_scope**: **SI NOT HELD — and the gap is material, not cosmetic.** The held PDF is
  31 pages of main text ending at reference 130 (p31). Cited and absent:
  - **Supp. Data 1** — coordinates of the APJ21 X-ray answer (never deposited in the PDB, p23).
  - **Supp. Data 2** — coordinates of 'pre-7XK8', the preliminary NMUR2 refinement used as an
    answer (never deposited, p23).
  - **Supp. Data 3** — the 886 cleaned, standardised model PDB files (p21).
  - **Supp. Data 4** — every participating group's modelling method description. **All the
    method attributions quoted in this note (SDU-Yang, KIST-Park, UW-DiMiao, SIAT-Yuan,
    MSU-Feig, ShanghaiTech-Bai) are the main text's summary of Supp. Data 4** and cannot be
    checked against the source.
  - **Supp. Table 1** — the participant roster (i.e. the collective author list).
  - **Supp. Table 2** — the 18 uninterpretable models.
  - **Supp. Table 3** — **the full per-model ranking. This is the paper's actual result table
    and none of it is held.** Only per-target best models appear in the main text.
  - **Supp. Table 4** — the AF2-usage tabulation behind Table 3.
  - **Supp. Figs 1–10** — including Supp. Fig. 1 (all pairwise experimental-structure
    disagreements), Supp. Fig. 2 (country and per-target model counts), Supp. Fig. 3 (the
    contact-matrix scoring schematic), Supp. Figs 4/6/8/9 (every alternative-reference
    analysis), Supp. Fig. 5 (per-target correctness distributions), Supp. Fig. 7 (DockQ vs
    correctness), and **Supp. Fig. 10 — the only quantitative panel for the entire
    AlphaFold3 / Boltz-1 / Chai-1 / NeuralPLexer comparison**.
  - Consequence: the AF3-era result is available to us **only as the two qualitative sentences
    on p12**; there is no number, no RMSD, no correctness value for AF3, Chai-1 or NeuralPLexer
    anywhere in the held text. Anything we write comparing AF3-generation co-folders on these
    targets must either quote those sentences or be sourced from the SI, which we do not have.

## F. Figures

**11 panel-group rows** (5 main-text figures; no supplementary figures are held). Pages 15,
18 and 19 were rendered at 150 dpi because the captions do not carry the panel structure
(Fig 4's caption never says there are five panels or what the three series are; Fig 5's never
says the mark is a violin with overlaid points; Fig 1's caption does not say panel B is a
faceted horizontal bar chart or that panel J is a matrix). Three pages rendered.

**License — applies to every row below, stated once here.** Banner on every page, e.g. p1:
"It is made available under a **CC-BY-ND 4.0 International license**." **The ND clause forbids
derivatives.** Verbatim reproduction with attribution is permitted; **redrawing, recolouring,
cropping, re-faceting or adapting any panel is not.** If we want a figure in this style we
must build it from our own data, not adapt theirs. This is the only ND-licensed paper flagged
so far in this corpus and it is the one whose figure designs (the correctness scatter with an
experimental-error background, and the TM/ECL radar) are most tempting to borrow.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A | 15 | The five answer structures, one render each, with method and resolution labelled | structure render | `RENDER \| facet: target complex (5: APJ/Cmpd6 X-ray 2.4 Å, GPR139/JNJ cryo-EM 3.2–3.8 Å, OPRK/Dynorphin cryo-EM 3.2 Å, NPY1R/NPY cryo-EM 3.2 Å, NMUR2/NMU25 cryo-EM 3.3 Å) \| views: 1 (membrane-plane, extracellular up) \| overlay: 0 predictions on 1 reference \| axis: none` | 5 sub-renders in one lettered panel, varying by target | | CC-BY-**ND** 4.0 — p1 banner; no derivatives |
| 1B | 15 | How much homology each target had in the PDB at competition time — the confound the whole assessment is organised around | bar | `PLOT \| facet: target receptor (5: APJ, GPR139, OPRK, NPY1R, NMUR2) \| vary: template receptor (6 per facet: the target itself plus its 5 closest structurally characterised homologues — APJ/AGTR1/CXCR2/US28/OPRD; CCR5/GPR52/NTR1/OPRK/CCKAR; OPRK/OPRM/OPRD/OPRX/OX2R; NPY1R/CCKAR/NPY2R/NK1R/AGTR1; NTR1/GHSR/OPRK/OX1R/OX2R) \| series: none (1; filled bar = target self-identity, open bar = template) \| measure: TM domain sequence identity (%), 0–100 \| mark: bar (horizontal) \| n: 1 per mark; ~6 per facet` | 1 lettered panel containing 5 stacked facet groups | The GPR139 and NMUR2 facets have **no filled self-identity bar** because no structure existed — the absence is the panel's key information but is encoded only as a missing bar with no annotation; no n, and the identity values quoted in text (27%, ~35%, ~31%) are readable only approximately off the axis | CC-BY-**ND** 4.0 — p1; no derivatives |
| 1C-I | 15 | Induced fit and ligand-pose divergence: each answer superposed on the pre-existing structure of the same receptor (C–E) and each answer ligand overlaid on the pre-existing ligand (F–I) | structure render | `RENDER \| facet: comparison (7: C APJ21 vs 6KNM, D 7Y1F vs 6B73, E 7X9A vs 5ZBQ, F Cmpd6 vs AMG3054(14-17), G Dynorphin vs MP1104, H Dynorphin vs KGCHM07 + DAMGO, I NPY vs UR-MK299) \| views: 1 (pocket close-up) \| overlay: 0 predictions on 1 reference; answer (coloured/yellow) on 1–2 prior experimental structures (gray) \| axis: none` | 7 sub-panels C–I; C–E receptor-level, F–I ligand-level; both are answer-on-prior overlays so one row | No quantitative panel accompanies the induced-fit claim — the magnitude of the rearrangement is asserted visually and never given as an RMSD anywhere in the paper | CC-BY-**ND** 4.0 — p1; no derivatives |
| 1J | 15 | Which pocket positions each answer ligand touches, projected onto a common receptor alignment | heatmap | `MATRIX \| rows: answer structure (7: APJ, GPR139 7vuh, GPR139 7vug, OPRK, NPY1R 7vgx, NPY1R, NMUR2) \| cols: aligned receptor residue position (continuous along N-term/TM1/TM2/ECL1/TM3/TM4/ECL2/TM5/TM6/ECL3/TM7, individual positions labelled only at 3.32/3.33, 6.48/6.51/6.54/6.55/6.58, 7.35/7.39/7.43) \| value: contact presence, encoded as dot size, with dot fill = side-chain vs backbone contact \| facet: none (1)` | 1 panel, 7 rows | Dot area encodes contact strength on an unlabelled scale — no legend maps dot size to a value, and the underlying continuous strengths (p22) are discretised invisibly; total column count is not stated | CC-BY-**ND** 4.0 — p1; no derivatives |
| 2A-B | 16 | Every small-molecule model placed in RMSD × contact-accuracy space against the shaded distribution of real X-ray structure pairs — the panel that defines "approaches experimental accuracy" | scatter | `PLOT \| facet: target (2: APJ/Cmpd6 vs the ShanghaiTech X-ray; GPR139/JNJ vs PDB 7VUG) \| vary: ligand heavy-atom RMSD after TM superposition (continuous, ~0–10+ Å) \| series: entity class (3: submitted models; best-ranking models highlighted; other experimental structures of the same complex) \| measure: fraction of correctly predicted ligand–receptor contacts (%) \| mark: point, over a shaded 2-D density background and solid correctness isolines \| n: 1 per mark; 206 (A) and 198 (B) models per panel, plus 1–3 experimental points` | 2 panels, varying by target | The shaded "experimental" background is the **2013** high-resolution X-ray pair distribution (p13/p22) plotted behind **2021–2024 cryo-EM** answers, and nothing in the panel says so; the isolines are labelled only in the caption; per-point group identity is not encoded, so a group's five models cannot be traced | CC-BY-**ND** 4.0 — p1; no derivatives |
| 2C-D | 16 | The single best small-molecule model per target, contacts and pose, against the answer | structure render | `RENDER \| facet: target (2: APJ, GPR139) × view type (3: target contacts captured/missed, pose overlay, model contacts) \| views: 3 (left/middle/right as named in the caption) \| overlay: 1 prediction on 1 reference \| axis: none` | 2 lettered panels, 3 sub-renders each | **1 of 206 and 1 of 198 models shown**, selected by the assessors' own correctness ranking; no second-best or median model is rendered, so the reader sees the ceiling and not the distribution the scatter above actually reports | CC-BY-**ND** 4.0 — p1; no derivatives |
| 3A/C/E | 17 | The same RMSD × contact-accuracy space for the three peptide targets | scatter | `PLOT \| facet: target (3: OPRK/Dynorphin vs PDB 8F7W aa 1–8; NPY1R/NPY vs PDB 7X9A aa 21–36; NMUR2/NMU25 vs PDB 7W55 aa 18–25) \| vary: peptide heavy-atom RMSD after TM superposition (continuous, Å) \| series: entity class (3: submitted models; best-ranking models; the alternative experimental structure of the same complex) \| measure: fraction of correctly predicted contacts (%) \| mark: point over shaded background with correctness isolines \| n: 1 per mark; 175 (A), 155 (C), 152 (E) models per panel, plus 1 experimental point` | 3 panels, varying by target | Each panel scores a **different, post-hoc-chosen residue window** (aa 1–8, 21–36, 18–25) yet the three are drawn on visually identical axes and compared directly in the text; the aa 1–5 dynorphin re-analysis that quadruples the OPRK result has no main-text panel at all (Supp. Fig. 6B-C, not held) | CC-BY-**ND** 4.0 — p1; no derivatives |
| 3B/D/F | 17 | The single best peptide model per target, contacts and pose, against the answer | structure render | `RENDER \| facet: target (3: OPRK, NPY1R, NMUR2) × view type (3: target contacts captured/missed, pose overlay, model contacts) \| views: 3 \| overlay: 1 prediction on 1 reference \| axis: none` | 3 lettered panels, 3 sub-renders each | 1 of 175, 1 of 155 and 1 of 152 shown, oracle-selected as in 2C-D | CC-BY-**ND** 4.0 — p1; no derivatives |
| 4A-E | 18 | Receptor-side accuracy: every model drawn as a quadrilateral over TM/ECL1/ECL2/ECL3 RMSD axes, with experimental structures and top-ranked models overdrawn | line (radar / polar polygon) | `PLOT \| facet: target (5: APJ, GPR139 vs 7vug, OPRK vs 8f7w, NPY1R vs 7x9a, NMUR2 vs 7w55) \| vary: receptor region (4 radial axes: TMs, ECL1, ECL2, ECL3) \| series: entity class (3: experimental structures, top-ranked models, other models) \| measure: backbone RMSD to the gold-standard answer (Å; radial rings at 1, 4, 9, 16 Å) \| mark: line (one closed quadrilateral per structure) \| n: 1 per quadrilateral; 206 / 198 / 175 / 155 / 152 model quadrilaterals per panel plus 1–4 experimental ones` | 5 panels A–E, varying by target; one shared legend in panel A | **Radial rings at 1, 4, 9, 16 Å are a quadratic (r ∝ √RMSD) scale**, unstated anywhere, which visually compresses large loop errors — the 16 Å ECL2 outliers mentioned on p10 sit only ~4× further from centre than the 1 Å ring; ~200 overlaid translucent polygons per panel make the density unreadable and no per-region distribution or count is shown, so every percentage quoted on p10–p11 has to be taken from the text; **the running text cites "Fig. 4D" for both NPY1R and NMUR2** (p10, p11) although NMUR2 is panel E | CC-BY-**ND** 4.0 — p1; no derivatives |
| 5A,C | 19 | Correctness by modelling approach, per target — the panel behind "AlphaFold2 played a vital role" | violin | `PLOT \| facet: target (5: APJ, GPR139 in A; OPRK, NPY1R, NMUR2 in C) \| vary: prediction method (5–6: AF apo, AF cpx [peptide targets only], GEnSeMBLE [small-molecule targets only], homology, PDB, unk) \| series: none (1; one violin + overlaid points per method) \| measure: model "correctness" (%), log axis 0–10 with a literal 0 tick \| mark: violin with overlaid points (sina) \| n: 1 point per model; 150 / 155 / 128 / 119 / 115 models with reported methods per panel, per-method n NOT REPORTED in the figure` | 5 panels across two lettered groups (A: 2 small-molecule targets; C: 3 peptide targets); method levels differ between the two groups | Per-method n is not printed anywhere on the figure although it varies by more than an order of magnitude (11 APJ homology models vs 106 GPR139 AF-apo models, p11), so a violin built on 11 points is drawn the same width as one built on 106; **"N/A" text is placed in the PDB column for GPR139 and NMUR2** where no structure existed — correct, but visually reads as a missing measurement rather than an impossible one; the log measure axis carries a literal "0" tick, which no log scale can hold | CC-BY-**ND** 4.0 — p1; no derivatives |
| 5B,D | 19 | 2021 correctness placed against the 2010 and 2013 rounds, small molecules and peptides separately | violin | `PLOT \| facet: ligand modality (2: small-molecule targets in B; peptide targets in D) \| vary: target complex × competition round (8 in B: D3/eticlopride and CXCR4/IT1t [2010], 5HT1B/ergotamine, 5HT2B/ergotamine, SMO/LY-680, SMO/SANT-1 [2013], APJ/cmpd6, GPR139/JNJ-054 [2021]; 4 in D: CXCR4/CVX-15 [2010], OPRK/dynorphin, NPY1R/NPY, NMUR2/NMU-25 [2021]) \| series: none (1; violin coloured by round/target) \| measure: model "correctness" (%), log axis 0–10 with a literal 0 tick \| mark: violin with overlaid points \| n: 1 point per model; 2021 panels 206/198 and 175/155/152; **n for the 2010 and 2013 rounds NOT REPORTED**` | 2 panels, varying by ligand modality; 8 and 4 violins respectively | The 2010/2013 model counts are never given, so the historical violins cannot be weighted against the 2021 ones; the rounds used different targets and different numbers of groups, and the only thing held constant is the metric (p22) — the panel invites a like-for-like reading it cannot support; same literal-0-on-a-log-axis problem | CC-BY-**ND** 4.0 — p1; no derivatives |

**Tables, recorded here so they are not lost.** **Table 1 (p20)** — the small-molecule answers
and their alternatives: PDB, receptor, ligand, fusion/IC effector, method, resolution,
**release date**, reference (APJ21 2.40 Å X-ray release "n/a"; 8XZI 2.70 Å 2024-03-20; 8S4D
2.58 Å 2024-12-04; 7VUG 3.20 Å, 7VUH 3.22 Å, 7VUI 3.30 Å, 7VUJ 3.80 Å all 2021-12-29).
**Table 2 (p20)** — the peptide answers, adding the **ordered part of the ligand** column that
justifies every scoring window (7Y1F aa 1-9 3.20 Å 2023-05-24; 8F7W aa 1-8 3.19 Å 2022-12-14;
7X9A aa 1-36 3.20 Å 2022-05-18; 7VGX aa 1-5,20-36 3.20 Å 2022-02-23; pre-7XK8 aa 1-25 3.30 Å
release "n/a"; 7XK8 aa 1-25 3.30 Å 2023-02-22; 7W55 aa 18-25 2.80 Å 2022-04-20). **Table 3
(p20)** — AF2 usage per target. **Tables 1–2 are the load-bearing evidence for the
prospectivity claim** and are the two objects to cite for the timeline.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), session
  `b4b527b3-7dd9-48b6-8b5d-c95a41ac3967`
- **schema_version**: v3
- **confidence**: **High** on identity, scope, the blindness timeline, claims, controls and
  figure structure — the text layer is clean, every quoted sentence is legible, and the
  timeline is corroborated in four independent places (p2 design statement, p4/p5 deadline
  statements, p22 acknowledgement of pre-publication coordinate transfer, p20 Tables 1–2
  release dates). **Medium** on `metrics_reported`: all values are from running text and
  Table 3, which is fine, but they are best-model values only — the full per-model result table
  (Supp. Table 3) is not held, so no distribution statistic other than the percentages quoted
  on p10–p11 can be verified, and Fig 5's violins were read visually, not numerically.
  **Medium-low** on anything concerning the AlphaFold3-generation arm: its only quantitative
  panel (Supp. Fig. 10) is absent and the entire result reaches us as two sentences on p12.
  What was hard to read: Ballesteros-Weinstein superscripts collapse in the text layer
  ("N271 7.39" for N271^7.39, "W170ECL2"); Table 1–3 columns are badly shredded by pdftotext
  and were cross-checked against the p20 layout; Figs 1, 4 and 5 required rendering because
  their captions omit panel counts, series identities and mark types.
- **unresolved**:
  1. **The model submission deadline is never dated.** This is the single most important missing
     fact in the paper, because it is the cutoff that makes the whole assessment prospective.
     The paper refers to it three times without a date (p4 "after the model submission
     deadline"; p5 "after the GPCR Dock 2021 model submission deadline"; p5 "at the time of the
     assessment"). It can be bracketed but not fixed: after the July 2021 AF2 release (p12,
     "Released only a few months before the assessment"), and on or before roughly end-2021
     since the four GPR139 answers were "still unpublished at the time of the assessment" (p5)
     but were released 2021-12-29 (Table 1, p20). **If we quote a date in the manuscript we must
     source it elsewhere; this PDF does not supply one.** Also undated: when targets were
     announced, and how long the prediction window was.
  2. **Whether AlphaFold3, Boltz-1, Chai-1 and NeuralPLexer had the answer structures in their
     training data.** No training cutoff is reported for any of the four (p12, p22), and the
     answers were released between 2021-12-29 and 2024-12-04 while the runs were made around
     Nov 2024. The arm has no post-cutoff control and no held-out comparison. **Do not describe
     that arm as either contaminated or clean — the paper does not say, and neither should we.**
     Related and also unstated: whether the AF3 run's templates (implied by "default
     parameters", p22) were date-restricted, and whether NeuralPLexer's checkpoints [128]
     postdate the releases.
  3. **RECEPTOR CONFORMATIONAL STATE IS NEVER ASSESSED — and this absence is directly useful to
     us.** The paper scores three things and only three: (i) ligand pose, as heavy-atom RMSD
     plus contact accuracy folded into 'correctness' (p6, p22); (ii) global receptor fold, as
     TM-bundle backbone RMSD (p21, Fig 4 p18); (iii) local extracellular loop geometry, as
     ECL1/2/3 backbone RMSD (p21, Fig 4). **There is no state predicate anywhere in the paper**
     — no active/inactive call, no TM6 outward displacement, no DRY or NPxxY microswitch
     measure, no activation index, no state classifier, no comparison of any model against an
     inactive reference. The reason is structural to the design and is stated in one sentence
     on p3: "All five complexes featured **active** receptors and intracellularly bound
     heterotrimeric G proteins; however, predictions for receptor interactions with the G
     proteins were not evaluated as part of the assessment." Every target is in the same state,
     so state is a constant and cannot be scored. The consequence is that **the largest blind
     community assessment of GPCR complex prediction in the AlphaFold era never once tested
     whether a method can get the conformational state right** — it tested whether, given that
     everyone knows the state is active, methods can place a ligand and reproduce a fold. The
     paper is nevertheless aware of the gap and names it as an AF2 limitation without measuring
     it, p13: "two limitations of AF2 affected prediction accuracy: (i) inability to
     systematically and reproducibly predict receptor conformational ensembles and distinct
     functional states [107]" — a citation to Heo & Feig, not a result of this assessment.
     A blind assessment of state prediction has, on this evidence, never been run.
  4. **The organisers' institution solved four of the five answers and one of its groups won a
     target.** The answers came from iHuman/ShanghaiTech (p5, p22 acknowledgements naming Fei
     Xu, Zhi-Jie Liu, Tian Hua, Beili Wu, Qiang Zhao), two of the three corresponding authors
     are at ShanghaiTech (p1), and the winning NMUR2 model was submitted by
     **ShanghaiTech-Bai** (p9). The paper does not discuss this, does not say whether
     ShanghaiTech-Bai was firewalled from the structural biologists, and does not report any
     conflict-of-interest procedure for participants at the answer-holding institution — the
     conflict statement (p23) says only "The authors declare no conflict of interest." The
     submission system was an online blind SmartSheets system (p21) and model analysis was done
     at UC San Diego (p22, author contributions), which are mitigating, but the question is not
     addressed. **This is the one crack in an otherwise exemplary blind design and should be
     stated if we lean hard on the blindness.**
  5. **Two internally inconsistent model counts.** The Methods and Results give the assessed set
     as **206 / 198 / 175 / 155 / 152** (p6, p21; total 886 = 904 − 18). **Table 3 (p20)** gives
     "Submitted models*" as **201 / 198 / 170 / 155 / 152** (total 876), with the footnote
     "* Submitted models after removing group ID 8067", and p11 repeats the Table 3 numbers
     ("150 of 201 APJ/Cmpd6 models", "128 of 170 OPRK/dynorphin models"). APJ and OPRK differ by
     exactly 5 each — one group's full submission — but group 8067 is stated on p21 to have
     withdrawn *before* the 904 figure was reached. **The AF2-usage percentages in Table 3 are
     computed on the smaller denominators**, so 40.7% and 54.7% would be 39.6% and 53.1% on the
     Methods counts. Small, but it means the two count systems in this paper are not
     reconcilable from the text.
  6. **Whether the assessors' AF3-era arm covered GPR139.** The Methods section is headed
     "End-to-end modeling of **APJ/Cmpd6** complexes" and describes runs for that complex only
     (p22), but the Results report a GPR139 finding from the same four methods (p12). Sample
     counts, seeds and settings for any GPR139 run are not given.
  7. **A receptor-name error in the peptide cross-round comparison.** p12 says "the only peptide
     target in prior assessment: **CXCR5**/CVX15 in GPCR Dock 2010", while the same page earlier
     says "only 1 peptide complex in prior assessments, that of **CXCR4** with CVX15 in 2010
     [16]" and Fig 5D (p19) labels it "CXCR4 CVX-15". CXCR4 is correct; CXCR5 is a typo.
     Flagged so we do not propagate it in a quote.
  8. **The 1 Å / 2 Å / 3 Å receptor-accuracy cutoffs are never justified.** They appear only in
     the Results prose (p10–p11) and in no Methods definition, with no citation and no
     rationale. Every "70% of models had TM RMSD < 1 Å"-style statement depends on an
     unjustified threshold. (The *ligand-side* thresholds, by contrast, are fully specified and
     cited — p22.)
  9. **Participants' own model ranking is never analysed.** Groups submitted up to five models
     in their own priority order (p21), so the paper could have reported "was the group's model
     1 its best?" — the question that decides whether these accuracies are achievable
     prospectively by the modeller, not just findable retrospectively by the assessor. It does
     not. Given how much weight the Discussion puts on selection and expert judgement (p8, p11),
     this is the most valuable analysis the paper could have run and did not.
  10. **`si_in_scope` is the practical ceiling on this note.** No per-model score, no per-group
      method text, no country breakdown, no alternative-reference figure and no AF3-era panel is
      held. If we need any of those, the SI must be obtained from bioRxiv.
  11. **Tags wanted but not available in the v3 vocabulary** (none invented, per rule 9). Three
      genuine gaps, all of which this paper exposes precisely because it is unlike the rest of
      the corpus:
      - **No tag for a blind community assessment / competition.** `benchmark-only` covers a
        retrospective benchmark and a blind competition identically, which erases the single
        most valuable property this paper has. `prospective` marks the rigour property but not
        the *object* — a query for "community assessments" or "CASP-like competitions" cannot be
        expressed. Suggested: `community-assessment` or `blind-competition`.
      - **No tag for pose/docking accuracy as the scored quantity.** The metric tags
        (`binary-predicate`, `continuous-metric`, `rmsd-only`, `visual-metric`,
        `saturating-metric`) all describe metric *form*, not metric *object*. This corpus is
        otherwise full of papers scoring conformational state; there is no way to mark that a
        paper scored **ligand pose and never scored state**, which is exactly the distinction
        `unresolved` 3 makes and the reason this paper is `background` rather than `precedent`
        on the state question. Suggested: `pose-accuracy` and/or `state-not-assessed`.
      - **No tag for reference-structure uncertainty / disagreement between experimental
        answers.** A third of this paper (p4–p6, p13) is about two independent structures of the
        same complex disagreeing by up to 9.9 Å, and about what "correct" then means. Nothing in
        the vocabulary can mark it, and it is a theme our manuscript is likely to need.
        Suggested: `reference-uncertainty`.
      Also noted but not a gap: `experimental-validation` was considered and rejected (see Tags).
  12. **Points where schema v3 was still ambiguous** (blunt, as requested):
      - **The figure-splitting rule does not cover `vary`.** The rule is "split when `mark` or
        `measure` differs; do not split when only `facet` differs." Figure 5 has four lettered
        panels with **identical mark (violin + points) and identical measure (correctness %)**
        but two different independent variables: A/C vary by *modelling method*, B/D vary by
        *target × competition round*. Under a literal reading that is one row, which would
        produce a `vary` slot holding two incompatible variables — the exact unjoinable
        compound string the rule exists to prevent. I split it into `5A,C` and `5B,D`. **v3
        should say: split on `mark`, `measure`, or `vary`.**
      - **RENDER rows have neither `mark` nor `measure`, so the splitting rule cannot be applied
        to them at all.** Figure 1 contains renders of single structures (1A, `overlay: 0`) and
        renders of superpositions (1C-I, answer overlaid on prior structures). Under the literal
        rule these differ "only by facet" and are one row, which would join a
        no-overlay row against overlay queries. I used `overlay` as RENDER's analogue of
        `measure` and split. **v3 should name the RENDER discriminator explicitly — `overlay`
        and/or `views`.**
      - **`plot_type` has no vocabulary entry for a radar / polar plot.** Figure 4 is five radar
        plots; the permitted list is violin / box / scatter / line / bar / heatmap / structure
        render / grid of small multiples / schematic. I wrote "line (radar / polar polygon)"
        because a radar trace is a closed line in polar coordinates, and put the polar geometry
        in `data_shape` (`4 radial axes`, rings at 1/4/9/16 Å). A future query for "line plots"
        will now return a radar chart. **v3 should add `radar` (and probably `sina`/`strip`,
        which Fig 5 also needs alongside `violin`).**
      - **`metric_saturation` says "numeric saturation only" but does not say whether a
        *derived* floor counts.** Here the raw quantity (ECL RMSD) does not saturate at all —
        it spans 0.5–16 Å — but the *reported statistic*, "fraction of models under 1 Å", is
        0/206 for several targets, which is a hard floor that destroys all discrimination. I
        recorded it as saturation because the discriminating power is genuinely gone. **v3
        should say whether saturation of a thresholded summary of an unsaturated measure counts;
        two extractors will otherwise answer differently.**
      - **`anti_memorization_control` has no clean answer for a paper where the held-out design
        IS the experiment.** The field's `NONE RUN` / `UNPOWERED` vocabulary assumes a control
        arm sitting beside a main arm. Here the blind arm *is* the main arm, model-level n is
        886, and target-level n is 5. I wrote both. **v3 should allow, or name, the case where
        the anti-memorization arm and the primary arm are the same thing, and should say which
        n the `UNPOWERED` threshold applies to when a paper has two nested levels of n.**
      - **`prospective` and `oracle_leakage` routes 5 and 6 are structurally in tension.** In
        any blind assessment, success *is* defined by RMSD to a held reference (route 5) and
        best/worst labels *are* assigned against it (route 6) — but by the assessor, after the
        predictions are locked, which is the opposite of a defect. v3's route list has no way to
        mark "present, but applied after the prediction was sealed". I labelled both routes
        `PRESENT, BY DESIGN` and explained. **v3 should distinguish leakage-into-the-pipeline
        from evaluation-after-the-fact for routes 5 and 6, or every honest blind assessment will
        be scored as having two leakage routes.**
- **why_it_matters**: *(left empty by the extractor — the user's call)*

## Tags

`gpcr` `benchmark-only` `cofolding` `multi-backbone` `state-annotated-input` `single-state`
`continuous-metric` `saturating-metric` `prospective` `anti-memorization` `unpowered`
`confidence-as-discriminator` `peptide-driven` `apo-sampling` `orthosteric` `preprint`
`precedent` `background` `comparator-numbers`

**Scoping notes on four tags that are true but narrower than they look:**
- `cofolding` — justified twice over: participants used AF2-Multimer to co-fold receptor with
  peptide, and that was the winning approach for NPY1R and NMUR2 (p11); and the assessors
  themselves ran AlphaFold3, Boltz-1, Chai-1 and NeuralPLexer end-to-end (p12, p22). The paper
  proposes no co-folding method of its own.
- `state-annotated-input` — present in **one participant pipeline only**: MSU-Feig's winning
  NPY1R model used the Multi-State GPCR modeling protocol [107] to build a template and biased
  AF-Multimer "towards the active state of the complex" (p9). The assessment itself uses no
  state-annotated input. Tagged because it is the only instance in the corpus of
  state-annotated templating inside a *blind* competition, and it won its target.
- `saturating-metric` — applies to the receptor-loop cutoff arm, where 0/206, 0/198, 0/175,
  0/155 models clear the 1 Å ECL2/ECL3 bar (p10–p11), and to the compression of correctness
  against zero (max 5% on a 0–100% scale). The primary correctness metric discriminates fine in
  log space; do not read this tag as "the assessment metric was useless".
- `unpowered` — at the **target** level only: n = 5 targets. Model-level n is 886. Both numbers
  are in `n_predictions`; use the right one.
- `confidence-as-discriminator` — **participant-side model selection, never validated by the
  assessors.** Two winning models were pLDDT-selected (p7 KIST-Park, p9 MSU-Feig); no
  confidence value is reported or correlated with correctness anywhere.

**Tags considered and rejected, with reasons, so the decision is auditable:**
- `oracle-leak` — **rejected**, and the rejection is the point of this note. No deposited
  structure of the target state entered any participant pipeline; the answers were unpublished
  at the deadline (p2, p4, p5), transferred privately to the assessors (p22), and two remain
  unreleased in 2025 (p23). Routes 5 and 6 are present but applied by assessors after
  predictions were sealed, which is what a blind assessment is. For the AF3-era arm, leakage is
  **unverifiable, not established** — no training cutoff is reported (see `unresolved` 2) — and
  tagging on a suspicion would corrupt the reverse lookup.
- `design-level-oracle` — **rejected for the assessment** (targets were chosen because the
  answer was *unknown*, the inverse of route 7). Arguable for the retrospective AF3-era
  paragraph, where the assessors already held and had scored the answers, but that is one
  paragraph plus an unheld supplementary figure, and tagging the paper would mislabel 30 pages
  of prospective work. Recorded in `oracle_leakage` route 7 instead.
- `no-anti-memorization` — rejected; the anti-memorization design here is the strongest form
  available (unpublished, partly never-released references), not merely a date filter.
- `md`, `enhanced-sampling`, `md-emulator` — rejected. MD appears only inside two participants'
  method summaries (SIAT-Yuan 200 ns restrained GROMACS/CHARMM36m, ShanghaiTech-Bai 100 ns
  Schrödinger/S-OPLS, p9). The paper runs no simulation of its own. `cofolding` survives only
  because the *assessors* ran co-folding models themselves (p22); `md` has no such warrant.
- `msa-subsample`, `msa-state-filter`, `af-cluster`, `latent-steering` — rejected; none occurs.
  The only MSA intervention named is SDU-Yang's unspecified "customized MSA" (p7), which is
  neither subsampling nor state-filtering as far as the text goes.
- `template-state-bias` — rejected in favour of `state-annotated-input`, which is the more
  precise description of the single MSU-Feig instance (p9); tagging both would double-count one
  submission.
- `templates-on`, `no-template-no-msa` — rejected; the assessment does not control templates,
  participants' template settings are unreported, and the assessors' AF3 run says only "default
  parameters" (p22). Neither input regime can be asserted.
- `two-state`, `ensemble`, `continuum` — rejected; every target is the same active state and
  every submission is a single static complex. Ensemble generation happens inside two
  participant pipelines (SIAT-Yuan's 20,000 models, GEnSeMBLE's "pleiotropic ensemble" per ref
  108) but never reaches the assessed object, so `ensemble` would false-positive a query for
  methods that *deliver* ensembles.
- `binary-predicate` — rejected as misleading. The 1 Å / 2 Å / 3 Å ECL cutoffs (p10–p11) are
  thresholded summaries of a continuous measure, not an operationalised state predicate, and no
  predicate of the form "correct if X" governs the primary ranking, which is a continuous
  percentile.
- `rmsd-only` — rejected; RMSD is combined with contact accuracy into 'correctness' (p6, p22)
  and cross-checked with DockQ for peptides (p9). Calling it RMSD-only would understate the
  metric.
- `visual-metric` — rejected for the assessment, which never calls anything by eye. Visual
  inspection appears only as a participant *model-selection* step (KIST-Park p7,
  ShanghaiTech-Bai p9), not as the accuracy metric.
- `experimental` — rejected; that tag marks a paper with no structure prediction in it, and this
  one scores 886 predictions.
- `experimental-validation` — rejected, and the near-miss is worth stating: the paper contains
  two previously unpublished experimental structures (APJ21, pre-7XK8, p20/p23) contributed by
  collaborators, but they are the *reference answers*, not a lab test of a computational
  prediction. Nothing predicted here was validated experimentally afterwards.
- `partner-driven`, `g-protein-mimetic`, `nanobody` — rejected; scFv16, Nb35 and the
  heterotrimeric G proteins appear only in the experimental answer constructs (Tables 1–2, p20)
  and G-protein interactions were explicitly excluded from scoring (p3). No model was steered by
  a partner.
- `ligand-driven` — rejected; docking a small molecule into an already-built apo receptor is
  pose generation, not state direction. `peptide-driven` is kept because AF-Multimer co-folding
  with the peptide demonstrably changed the receptor prediction and was the winning handle
  (p11).
- `directed-state`, `seed-only` — rejected; no method is instructed which state to produce
  (the closest is MSU-Feig's active-state template, tagged `state-annotated-input`), and seeds
  are used only as replicate counts in the assessors' AF3-era arm (p22).
- `allosteric-site`, `cryptic-pocket`, `allosteric-failure` — rejected; all five ligands are
  orthosteric agonists and no allosteric site is modelled or discussed.
- `kinase`, `transporter`, `periplasmic-binding`, `atpase`, `fold-switching`,
  `general-protein` — rejected; GPCRs only.
- `peer-reviewed` — rejected; bioRxiv, explicitly "not certified by peer review" (p1).
- `threat`, `contrast` — rejected; see `stance`. The paper's design is more rigorous than most
  of the corpus and it does not attempt the conformational-state problem we work on.
- `negative-result` — rejected as the overall stance, though the paper reports several honest
  internal negatives worth citing: no 2021 small-molecule prediction beat the best 2010 result
  (p12); co-folding failed on OPRK (p11); the most structurally characterised receptor was the
  hardest target (p9); no model predicted ECL3 within 1 Å for four of five targets (p10–p11).
- `figure-exemplar` — rejected; the tag is for papers kept *mainly* for figures and excluded
  from gap analysis, and this paper is kept for its content. Note separately that its two most
  reusable designs — the correctness scatter with an experimental-error background (Fig 2A-B,
  Fig 3A/C/E) and the TM/ECL radar (Fig 4) — are **CC-BY-ND and therefore may not be redrawn**.
