# stein2022speachaf

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.
`comparable_to_ours` and `why_it_matters` left EMPTY per v3.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–16), and for this
paper the PDF page equals the printed page** (PDF p8 prints "8 / 16"). No offset.

**The Supporting Information is NOT held.** The PDF is the 16-page article only. `S1
Text` (p14–15) contains Table A (the membrane-protein PDB IDs) and Figs A–K. Crucially
it contains **the entire targeted / directional-control arm** (Fig H = PfMATE, Fig I =
LmrP), **the entire negative control** (Fig K = ubiquitin), **the window-size
sensitivity analysis** (Fig J), and the per-target best-model plots (Figs D, F). See
`si_in_scope` — the directional-control evidence this note records exists only as prose
in the main text.

**Text-layer note:** the text layer is clean and complete, including the Fig 2 caption
which is split across p5 and p6. Figure axis labels, colourbar ranges and panel grids
are **not** in the text layer and were read from 150 dpi renders of **pages 5 and 8**
(two pages rendered; all other captions carried their own panel structure).

**Terminology warning for downstream use.** This paper does **not** mask, delete or
drop MSA columns. It **substitutes alanine** into selected columns across every
non-gap sequence in the alignment. Depth is unchanged; the alignment keeps the same
number of rows and columns. Any later paper that characterises SPEACH_AF as "masking"
is using the word loosely; the verbatim mechanism is in `oracle_leakage` route 1 and
`directional_control` below.

---

## A. Identity

- **citekey**: `stein2022speachaf`
- **doi**: `10.1371/journal.pcbi.1010483` — p1 citation block: "PLoS Comput Biol 18(8):
  e1010483. https://doi.org/10.1371/journal.pcbi.1010483". Matches `refs.bib`.
- **year**: **2022.** p1: "Received: March 8, 2022 / Accepted: August 11, 2022 /
  Published: August 22, 2022".
- **venue**: **PLOS Computational Biology 18(8): e1010483. Peer-reviewed research
  article, NOT a preprint.** p1 carries the journal masthead, the "RESEARCH ARTICLE"
  label, an academic editor ("Editor: Charlotte M. Deane, University of Oxford, UNITED
  KINGDOM") and received/accepted/published dates. Tagged `peer-reviewed`, not
  `preprint`.
- **title**: "SPEACH_AF: Sampling protein ensembles and conformational heterogeneity
  with Alphafold2" — p1.
- **authors**: Richard A. Stein (corresponding, richard.a.stein@vanderbilt.edu) and
  Hassane S. Mchaourab, Department of Molecular Physiology and Biophysics, Vanderbilt
  University — p1. Two authors, single institution. **Note for corpus cross-linking:**
  Mchaourab is also an author on ref [7], del Alamo et al. *eLife* 2022, the
  MSA-subsampling paper this work uses as its benchmark set and its comparator. This is
  an overlapping-author comparison, not an independent reproduction.

## B. Scope

- **system**: **Mixed — transporter-dominated, with GPCRs, one periplasmic binding
  protein, one nucleoside monophosphate kinase and one small globular control.** The
  paper is explicitly framed as a general method (p3: "Protein targets were selected to
  illustrate the general applicability of this method and to investigate its
  limitations"), and the target list bears that out:
  - **Canonical flexibility (2):** adenylate kinase (AK, *E. coli*) p4; ribose binding
    protein (RBP, Enterobacteriaceae) p6.
  - **Membrane proteins, both conformations outside the AF2 training set (8):** MCT1
    (MFS), STP10 (MFS), Lat1 (LeuT-fold), ZnT8 (CDF), ASCT2, CGRPR (GPCR), PTH1R (GPCR),
    FZD7 (GPCR) — named on p6.
  - **Membrane proteins with one conformation inside the AF2 training set (4):** MurJ
    (lipid II flippase, MOP superfamily), PfMATE (MATE/MOP), SERT (LeuT-fold), CCR5
    (GPCR) — named on p9.
  - **Targeted / directed arm (2, one repeated):** PfMATE again, and LmrP (multidrug
    transporter, CASP XIV target T1024) — p11.
  - **Negative control (1):** ubiquitin — p12.
- **GPCRs are present, four of them: CGRPR, PTH1R, FZD7 (no structure in training set,
  p6) and CCR5 (one structure in training set, p9).** The paper states the family
  membership explicitly on p6: "The set includes members of diverse protein families
  (Table A in S1 Text) such as the major facilitator superfamily (MFS), LeuT-fold,
  cation diffusion facilitator (CDF), and G-protein coupled receptor (GPCR) family."
  **The GPCR treatment is truncated:** p6, "In addition, only the transmembrane spanning
  region is modeled for the GPCRs." Extracellular domains — which for CGRPR, PTH1R and
  FZD7 are large and functionally central — are excluded from both modelling and
  scoring.
- **n_targets**: **16 distinct proteins** (PfMATE counted once across its systematic and
  targeted appearances): AK, RBP, MCT1, STP10, Lat1, ZnT8, ASCT2, CGRPR, PTH1R, FZD7,
  MurJ, PfMATE, SERT, CCR5, LmrP, ubiquitin. The paper's own arithmetic on p3: "two
  classical examples of protein flexibility... four membrane proteins where only one
  conformation was in the AF2 training set; and eight membrane proteins where both
  conformations were not in the AF2 training set", i.e. 2 + 12, plus LmrP (p11) and
  ubiquitin (p12) introduced later. **Generality claim from 16 targets:** the abstract
  (p1) claims "a general approach"; the discussion (p13) claims "the general utility of
  our methodology". Flagged.
- **method_class**: **other — MSA in-silico alanine mutagenesis (column-wise residue
  substitution across the whole alignment).** This is neither co-folding, nor
  MSA-subsampling (depth is untouched), nor MSA-state-filtering (no state-specific
  alignment is substituted), nor template-biasing (templates are off), nor MD, enhanced
  sampling, clustering or benchmark-only. It is a fifth thing the v3 `method_class`
  enumeration does not name. See `unresolved` item 1.
- **backbones**: **AF2 only, via ColabFold, model parameters v2.1.** p13 Methods: "These
  sequences were used as input for colabfold_batch that is part of ColabFold [27].
  ColabFold implements folding of the protein with the models for Alphafold2 using
  MMseqs2 to generate the MSA." p11 gives the parameter version: "The difference is most
  likely due to the update (v 2.1) of the model parameters for Alphafold used here." No
  AF3, Boltz, Chai, OF3 or Protenix — none existed in 2022. **`multi-backbone` NOT
  applied**; there is exactly one backbone.
- **templates**: **OFF, everywhere, deliberately, and this is load-bearing for the
  paper's argument.** p13 Methods: "The models were generated with the default
  parameters, which includes no template [3,27–30]. The rationale for not including any
  templates is to allow Alphafold2 to generate structural intermediates that may not be
  achieved by the bias of including structural templates." Restated as a contrast with
  DeepMind's CASP XIV LmrP protocol on p11: "In contrast, the approach here does not use
  structural templates."
- **msa_handling**: **full-depth, unsubsampled, sequence-modified.** The MMseqs2 a3m
  alignment is used at full depth; selected columns are overwritten with alanine in every
  sequence that is not a gap at that column. p14: "The alanine substitutions were made in
  the equivalent amino acid position across all sequences. This substitution was not made
  if the equivalent position was a gap." **This is explicitly NOT subsampling**, and the
  paper draws the distinction itself against ref [7] on p13 ("the alternate methodology of
  subsampling the MSA"). Per the v3 rule that subsampled and state-filtered must not be
  collapsed: this is a **third** category and neither word fits. Recorded as
  `sequence-modified (in-silico alanine mutagenesis, full depth retained)`.

## C. Conformational core

- **states_generated**: **`ensemble + two`.**
  - **`ensemble`** is what the systematic protocol produces and is the paper's own word:
    p1 abstract, "generating multiple protein conformations"; p13, "generating ensembles
    of multiple conformations". Per target the output is 300–420 models spread along a
    path between the two experimental endpoints, read off the TM-score plots (Figs 2C/E,
    3C/E, 4C, 5C) and the PCA plots (Figs 2F/H, 3F, 4D, 5D). For several targets the
    filling of that path is dense enough that the authors describe it as continuous —
    p8, "Lat1 on the other hand appears to adopt conformations along the whole pathway
    between the two experimental structures"; p9, "Four of the transporters exhibit a
    V-shaped plot, supporting isomerization of the transporter between inward and
    outward facing conformations". I stop short of writing `continuum` because the paper
    never operationalises a reaction coordinate; PC1 is an unlabelled, un-normalised
    axis whose variance fraction is never reported (see Figures `hides`).
  - **`two`** is what the *targeted* arm produces, and it produces it cleanly. p11,
    PfMATE: "These residues lead to a complete reversal of conformation from the
    outward-open for all of the initial models to inward-open for all of the models
    generated from the mutated MSA (Fig H in S1 Text)." That is a two-state switch, not
    an ensemble.
  - **Failure case within the ensemble arm:** CGRPR. p9, "CGRPR exhibits only an
    intermediate state between the two experimental conformations"; p13, "capable of
    generating both conformations for all of the targets, except CGRPR".

- **structural_priors_used**: **Substantial, and mostly at design time rather than in
  the default pipeline. Four distinct priors, and they must not be conflated with
  `oracle_leakage`.**
  1. **Both endpoint structures are deposited for every scored target, and the target
     set was chosen on that basis.** p3: "To enable direct comparison, the twelve
     membrane proteins were the same as those used in a previous study exploring
     conformational sampling with AF2 [7]." p4 for AK: "apo AK adopts an open
     conformation (PDB: 4ake) [8] whereas the inhibitor bound structure adopts a closed
     conformation (PDB: 1ake) [9]". p6 for RBP: "the closed structure (PDB 2dri) [13] and
     an open structure (1ba2B)".
  2. **Mechanistic prior on which interface mediates the transition, used in the targeted
     arm.** p11: "Based on the two-fold symmetry for PfMATE we hypothesized that the
     interface between the two halves would mediate the change in conformation."
  3. **Prior structural knowledge of which region is functionally interesting**, used to
     interpret MurJ. p9: "This is particularly notable as transmembrane helices 13–14 are
     thought to be the site of binding for the lipid II isoprenoid tail [18]."
  4. **Prior knowledge that PfMATE's low-pH experimental TM1 is a crystal artefact,
     used to exclude TM1 from scoring.** p9: "the analysis for PfMATE does not include
     TM1 as it is unraveled in the low pH experimental structure... as a result of crystal
     contacts and does not appear to represent the native conformation [17]." This is a
     defensible curation decision made against a deposited structure, recorded here
     rather than as leakage because it changes the *scoring region*, not the input.

- **oracle_leakage**: **PRESENT — routes 4, 5, 6 and 7 all fire; routes 1, 2 and 3 are
  clean. The default pipeline's INPUT is genuinely oracle-free; the filtering,
  adjudication and target selection are not.** Enumerated separately below.

  **Route 1 — structures used as input or template: NONE FOUND (default protocol), and
  this is the paper's strongest and best-supported claim.** The protocol is described on
  p3, p12 and p13–14. The only structural object entering the mutagenesis step is AF2's
  own initial model of the target, not a deposited structure. Verbatim, p3:

  > "the choice of residues to alter in the MSA entails determining sites of interactions
  > within the target using an 11 amino acid sliding window along the best pLDDT (the
  > predicted local-distance difference test which is Alphafold's metric for ranking the
  > confidence in the structure at every residue) scoring model from an initial AF2 run
  > without templates. The sites of interaction are then modified in the MSA to alanines
  > across all sequences where there is a non-gap residue. This modified MSA alignment is
  > then used 3 times, varying the random seed, to generate 15 models from AF2." (p3)

  The Methods give the same procedure at residue resolution, p14:

  > "The total length of the protein to be alanine-scanned was determined from the pLDDT
  > results for the top AF2 model... Both the N- and C- terminal ends were truncated where
  > the pLDDT values were less than the mean of all the pLDDT values. An 11 amino acid
  > window was scanned from these starting and ending points. Within this window, all
  > interacting residue pairs of this region and the rest of the protein that lie within
  > 4 Å of each other are tabulated. To keep from destabilizing secondary structure, any
  > of the interacting partners that were within 4 amino acids in the primary sequence
  > relative to the region of interest were omitted. Four angstroms was chosen as the
  > cutoff to encompass polar and ionic interactions including those mediated by water."
  > (p14)

  And the substitution itself, p14: "The alanine substitutions were made in the
  equivalent amino acid position across all sequences. This substitution was not made if
  the equivalent position was a gap. The choice of alanine is to minimize any negative
  consequences of the mutation on secondary structure."

  The authors state the no-prior-knowledge property flatly, p12:

  > "Our mutagenesis method requires no prior structural knowledge about the protein of
  > interest or its conformational landscape." (p12)

  **How the modified columns are chosen, and whether that needs prior structural
  knowledge of the target — the question this extraction was commissioned to settle.**
  The chosen column set is **not** a random draw and **not** a single contiguous block.
  It is the union of two things: (a) an 11-residue **sequence-contiguous sliding window**,
  stepped along the pLDDT-truncated chain, and (b) that window's **3D contact partners**
  anywhere else in the chain, defined as any residue within 4 Å, excluding partners
  within 4 residues in primary sequence. So the mutated set is *sequence-contiguous plus
  spatially-selected*, and the spatial selection is made **on AF2's own initial
  prediction of the target, produced without templates** — not on any deposited
  structure. **Answer: no, the default protocol does NOT require prior structural
  knowledge of the target.** Route 1 is clean. This is the real methodological
  distinction from later random-column-masking methods, and it is a distinction in *how
  columns are picked* (structure-aware, from the model's own prediction), not in the
  presence of an oracle.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving
  templates or alignments: NONE FOUND.** GPCRdb, KLIFS and Kincore are not mentioned
  anywhere in the paper. The alignment source is stated on p13 ("using MMseqs2 to
  generate the MSA") with database references [28–30] to Uniclust and MGnify, which are
  sequence resources carrying no state annotation. Templates are off (p13).

  **Route 3 — cluster labels derived from known states: NONE FOUND.** The clustering is
  unsupervised PCA on the model coordinates with ProDy (p14: "The parsed set of models
  underwent principal component analysis (PCA) with ProDy [31]"), and the experimental
  structures are projected onto the same axes as reference points rather than used to
  label clusters. The paper is explicit that PCA is meant to work without them, p6: "PCA
  can then be used as an additional screen for sets of models that do not fit the overall
  structural heterogeneity", and p11: "These results further support the utility of the
  PCA as a tool for classifying models in the absence of multiple experimental
  structures." **Caveat, not leakage but adjacent:** the outlier removal step feeding
  the PCA is manual and iterative — p14, "This plot was then used for manual inspection
  for outliers relative to the rest of the data. These outliers were removed from the set
  and the PCA was repeated until there were no apparent outliers." No criterion, no
  count, no per-target record.

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against
  known states: PRESENT.** Two instances.
  - **The MolProbity filter threshold was developed on, and validated against, targets
    whose two structures were both in hand.** The threshold (discard sets whose mean
    MolProbity is more than one SDM above the median) is introduced on AK, and its
    validity is argued by checking that the discarded models are the ones that fell on
    the wrong side of a line drawn from the two crystal structures. Verbatim, p4:

    > "The resultant plot of TM scores for the remaining models indicate that the majority
    > of models that were below the dashed line correspond to the sets with higher
    > molprobity scores (Fig 2E). This suggests that this method can be used to
    > systematically filter out sets with misfolded models." (p4)

    The dashed line is defined in the Fig 2 caption (p5) as "the TM score between the two
    experimental structures". The filter is then applied unchanged to all twelve membrane
    proteins. The same validation is repeated on RBP, p6: "The TM score plot supports this
    initial criteria for filtering as most of the models that lie outside of the
    progression of the closed to open states are eliminated (Fig 3E)."
  - **The 11-residue window size was chosen partly by justification and partly by a
    sweep run on adenylate kinase, a target with both endpoint structures deposited.**
    p12: "The choice of 11 amino acid presented here was selected based of the expected
    size of the structural elements to be probed... To explore the effect of window size
    on the ensemble of models, we tested the effect of smaller windows of 8 and 5 amino
    acid on adenylate kinase. The PCA of the resulting models from the three window sizes
    show good overlap of the conformational space explored (Fig J in S1 Text). These
    results support the use of the 11 amino acid window". Per the v3 note that tuning a
    *range* on the evaluation set is leakage even without a per-target value, this
    qualifies — the sweep is on an evaluation target, though the conclusion drawn is a
    null (window size does not matter much) rather than a selection.

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had: PRESENT,
  and this is the paper's primary success criterion.** Every headline claim is
  adjudicated by TM-score to the two deposited endpoint structures. Verbatim, p13:

  > "Plots of the TM-score for the AF2 models generated by making in silico mutations in
  > the MSA suggest that the approach described here is capable of generating both
  > conformations for all of the targets, except CGRPR, including those where the MSA
  > subsampling method failed (Fig 4–5)." (p13)

  Also p4: "we assessed the quality of the AF2 models for this test target by the TM score
  relative to the two crystal structures (Fig 2C)". **No numerical threshold for "both
  conformations" is stated anywhere**; the call is made by looking at the TM-score
  scatter plots. See `state_metric`.

  **Route 6 — best/worst model labels assigned against a held reference: PRESENT.** Fig 4
  caption, p8: "In Fig D in S1 Text are plots of the experimental structures and the best
  model based on TM score." Identically in the Fig 5 caption, p10: "In Fig F in S1 Text
  are plots of the experimental structures and the best model based on TM score." The
  "best model" is defined by TM to the held structure, and those panels live in the
  unheld SI.

  **Route 7 — design-level oracle use (input conditions or systems chosen because the
  expected answer is already known): PRESENT, and it is design-level, weaker than
  pipeline leakage.** Two instances.
  - **Target selection.** Every scored target was picked because two conformations are
    deposited for it — p3, "To enable direct comparison, the twelve membrane proteins
    were the same as those used in a previous study exploring conformational sampling
    with AF2 [7]". The expected answer for each target is on the axis labels of Fig 4B–C
    and Fig 5B–C before any model is read.
  - **The targeted-mutagenesis arm declares the expected state before reading the
    result.** p11, opening the section: "Whereas the protocol above makes no assumption
    regarding the surfaces to be mutated, prior knowledge of the underlying model of
    conformational changes may restrict the search to the hypothesized areas of
    contacts." And closing it: "The ability to generate the opposite conformations with
    fewer modified MSAs supports the use of directly targeting residues to mutate in the
    MSA based on prior knowledge of conformational changes." The authors label this arm
    as prior-knowledge-driven themselves; it is not concealed.

  **Verdict in one line: the default SPEACH_AF *input* is oracle-free (routes 1–3 clean,
  no templates, no state database, no state-derived labels), but the *filter*, the
  *adjudication*, the *best-model label* and the *target list* are all defined against
  deposited structures the authors held (routes 4, 5, 6, 7).** Tagged both `oracle-leak`
  and `design-level-oracle`.

- **prospective**: **partial.** Prospective in its inputs and in a real temporal sense
  for the 8-protein arm — those experimental structures postdate AF2's training set (p6:
  "Experimental structures of these targets were determined subsequent to the training of
  AF2"), and nothing about the target's structure enters the pipeline. Retrospective in
  its adjudication and its target selection — success is scored by TM to structures the
  authors already had (route 5), the model quality filter was calibrated against two
  targets whose endpoints were known (route 4), and the targeted arm names the expected
  state up front (route 7). The paper never uses the word "prospective".

- **state_metric**: **`RMSD-to-reference + continuous coordinate + visual only` — all
  three, and the third is the one that decides the headline result.**
  - **RMSD-to-reference (as TM-score, and once as RMSD):** TM-score computed with TM_align
    (p14: "The TM score was obtained with TM_align [32]") against each of the two
    deposited endpoints, plotted as a 2D scatter (TM-to-state-1 on one axis, TM-to-state-2
    on the other). One literal RMSD is given: p4, AK 4ake vs 1ake "an RMSD of 7.2 Å or TM
    score of 0.68 between the two crystal structures".
  - **Continuous coordinate:** PCA (PC1 vs PC2) on model coordinates via ProDy, p14. Used
    as the reference-free alternative — p6: "PCA provides a description of structural
    variance without multiple known protein structures."
  - **Visual only, and this is a rigour defect:** **no threshold is ever stated for
    calling a state.** The claim "capable of generating both conformations for all of the
    targets, except CGRPR" (p13) is read off the scatter plots by eye. The only numeric
    landmark on those plots is the dashed line at the inter-structure TM score, which is a
    reference marker, not a pass criterion. The PCA state calls are shape descriptions:
    p9, "Four of the transporters exhibit a V-shaped plot"; p11, "The MurJ plot of the
    first two principal components yields a square shape". The outlier removal is
    likewise by eye (p14). **`NOT REPORTED` for the threshold, where a threshold is
    plainly being used implicitly.**
  - **Thresholds that ARE stated, all for filtering rather than state-calling:** 4 Å
    contact cutoff for defining interacting pairs, justified as encompassing "polar and
    ionic interactions including those mediated by water" (p14); 4-residue primary-sequence
    exclusion, justified "To keep from destabilizing secondary structure" (p14); pLDDT
    below the mean of all pLDDT values for terminal truncation, unjustified (p14); mean
    MolProbity more than one SDM above the median for set rejection, unjustified beyond
    the post-hoc TM check (p4, p14).

- **metric_saturation**: **No numeric saturation is demonstrated, but TM-score is a
  bounded [0,1] metric and several arms sit near the ceiling on one axis.** From the p8
  render, MCT1's fifteen initial models cluster at TM(7da5) ≈ 0.97 and FZD7's at
  TM(7evw) ≈ 0.95, i.e. within a few hundredths of the ceiling on the state they already
  match; discrimination therefore has to come entirely from the other axis. The paper
  reports no summary statistics, so whether any comparison is actually floored or
  ceilinged **cannot be determined — NOT REPORTED**. **Axis truncation is NOT recorded
  here** per the v3 rule; every TM-score panel starts at 0.70/0.58 (Fig 2, p5) or 0.5
  (Figs 4–5), and that is logged in the Figures table under `hides` for rows 2C-E,
  3C-E, 4B-C and 5B-C.

- **directional_control**: **YES — partial, demonstrated, and claimed by the authors, but
  only in a secondary arm whose evidence is in the unheld SI. The handle is the CHOICE OF
  WHICH CONTACT INTERFACE TO ALANINE-SUBSTITUTE, and aiming it requires a mechanistic
  hypothesis about the transition, not a structure of the target state.**
  - **The default systematic arm has NO directional control.** It scans all windows and
    returns an ensemble; nothing selects a state. p11 states the contrast: "the protocol
    above makes no assumption regarding the surfaces to be mutated".
  - **The targeted arm does, and the authors claim it.** p11 verbatim: "prior knowledge
    of the underlying model of conformational changes may restrict the search to the
    hypothesized areas of contacts. We have carried this out for the MOP family
    transporter PfMATE and the multidrug transporter LmrP."
  - **PfMATE, complete switch:** "Based on the two-fold symmetry for PfMATE we
    hypothesized that the interface between the two halves would mediate the change in
    conformation. Therefore, the residues that were within 4 Å between the N- and
    C-terminal halves of the protein were mutated to alanine in the MSA as before and new
    AF2 models were generated. These residues lead to a complete reversal of conformation
    from the outward-open for all of the initial models to inward-open for all of the
    models generated from the mutated MSA (Fig H in S1 Text)." (p11)
  - **LmrP, mostly-switch, and note the interface came from AF2's own model, not from a
    deposited structure:** "In contrast, the approach here does not use structural
    templates. Rather, the residues that mediate the interface between the two halves of
    the protein in the inward facing AF2 model were explored. The mutations targeted
    residues in both the N- and C-terminal half, residues in either the N- or C-terminal
    half, and a set of 3 residues at the center of the transmembrane region. These
    mutations prompted AF2 to generate mostly outward-open conformations that match the
    experimental structure (Fig I1 in S1 Text)." (p11)
  - **The authors' own summary claim:** "The ability to generate the opposite
    conformations with fewer modified MSAs supports the use of directly targeting residues
    to mutate in the MSA based on prior knowledge of conformational changes." (p11)
  - **Precise characterisation of the handle:** you aim the method at *an interface you
    believe mediates the transition*, and the model then goes to the other side of that
    transition. You do not name a target state and you do not supply a structure of it.
    In both demonstrated cases the interface is the N-/C-terminal-half interface of a
    pseudo-two-fold-symmetric transporter, which is a mechanistic prior available without
    the answer structure. **The paper never demonstrates aiming at a specific named state
    on a system where the transition mechanism is unknown**, and never attempts directed
    control on any GPCR.
  - **A weaker, non-directional handle also exists:** the random seed. p13, "the first
    step in obtaining alternate conformations are multiple runs of AF2 with different
    random seeds". That samples; it does not aim.

- **anti_memorization_design**: **YES — a real, explicit, two-stratum training-set design.
  This is NOT `NONE`, and it is the paper's organising principle for the membrane-protein
  half.**
  - **Stratum 1, n = 8: both conformations outside the AF2 training set.** p3: "eight
    membrane proteins where both conformations were not in the AF2 training set". p6: "We
    selected a set of membrane protein targets on the basis of a previous report examining
    the ability of AF2 to predict multiple conformations [7]. Experimental structures of
    these targets were determined subsequent to the training of AF2."
  - **Stratum 2, n = 4: one conformation inside the AF2 training set.** p3 and p9: "we
    selected the same set of targets for analysis by our method: the lipid II flippase
    MurJ... PfMATE... SERT... and CCR5".
  - **How the cutoff was defined: inherited, not independently established.** The
    criterion is "determined subsequent to the training of AF2" (p6), with the target
    partition taken over wholesale from ref [7] (p6, p9). **No cutoff date, no PDB release
    dates, and no independent verification appear anywhere in the article**; the per-target
    PDB IDs live in Table A of the unheld S1 Text. So the design exists and is genuine,
    but it is **not independently auditable from this PDF**.
  - **Additional, separate memorization-adjacent design element:** PfMATE's TM1 is excluded
    from analysis because the deposited low-pH structure's TM1 is a crystal artefact (p9).

- **anti_memorization_control**: **RUN, and analysed as the paper's central negative-result
  test — but UNPOWERED (n = 4, and the comparison stratum is n = 8; both below the v3
  n ≈ 10 bar).**
  - **The control arm is the 4-protein one-structure-in-training-set stratum, and it was
    run to test a specific memorization hypothesis raised by the comparator paper.** p9:
    "The previous report by Del Alamo et al. noted that their approach of using a shallow
    MSA was unable to generate more than one conformation for targets where one structure
    existed in the AF2 training set suggesting an intrinsic bias within AF2 [7]. Having
    established the applicability of our method to targets with no conformations in the
    training set, we examined whether this bias would be present here."
  - **Result, stated as a rebuttal:** p11, "The generation of alternate conformations for
    these four proteins argues against a general bias as the origin of the observation that
    decreasing the number of sequences in the MSA did not lead to the alternate
    conformations for these proteins." And p13: "This demonstrates the general utility of
    our methodology in generating ensembles of multiple conformations regardless of whether
    the protein is in the training set."
  - **Marked UNPOWERED.** Four proteins, one of which (PfMATE) yields "hardly any
    additional conformations" (p9) and another (SERT) yields conformations that move "not
    completely in the direction of the second experimental conformation" (p9). The claim
    that training-set membership does not matter rests on 4 targets with two partial
    successes among them, and no statistical treatment of any kind.
  - **Second control arm, also run: the ubiquitin negative control** (a protein expected
    not to undergo a large conformational change). p12–13: "A question with this method is
    the effect of mutating residues to alanine on a protein that does not undergo a
    conformational change. We tested this question by using a 3 amino acid window on the
    protein ubiquitin... the strong overlap in the PCA indicates that structural
    flexibility is highly similar (Fig K4 in S1 Text) and examination of the structures on
    the periphery do not indicate any additional conformations. The similarity in the
    explored conformational space and lack of any new conformations generated by AF2
    further supports the overall conclusion that the method presented here, when filtered
    for misfolded models, does not lead to gross deviations from experimentally sampled
    conformations." n = 1, and all four supporting panels are in the unheld SI.

- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Unmodified-MSA arm, 15 models per target (3 seeds × 5 AF2 models), run for every target | That the alternate conformations are an artefact of nothing — establishes the baseline AF2 answer each target defaults to, and shows AF2 alone already gives >1 conformation for ZnT8, ASCT2, Lat1 | p3–4 (protocol), p7–8 (Fig 4A–B), p9–10 (Fig 5A–B) |
| Templates off in every run, including the LmrP arm where the CASP XIV comparator used curated outward-open templates | That the alternate state was supplied by a template rather than produced from the MSA | p13 (Methods); p11 (LmrP contrast) |
| Random-seed variation alone (3 seeds per MSA), reported as a distinct contributor | That MSA modification is doing all the work; the paper concedes seeds alone reach some alternate states | p8, p13 |
| MolProbity scoring of all models, with set-level rejection at >1 SDM above the median | That alanine substitution at interaction surfaces is simply producing misfolded models scored as "alternate conformations" | p4, p6, p14 |
| PCA screen with iterative manual outlier removal, on top of MolProbity | That MolProbity-passing but non-ensemble models (e.g. AK's differently-folded ATP lid, Fig 2G) are counted as conformations | p4, p6, p14 |
| Ubiquitin, 3-residue window, compared against NMR ensembles | That the method invents conformational heterogeneity in a protein that has none; n = 1 | p12–13 (Fig K in S1 Text, not held) |
| Window-size sweep 11 vs 8 vs 5 residues on adenylate kinase | That the 11-residue window is a tuned, load-bearing parameter | p12 (Fig J in S1 Text, not held) |
| 4-protein stratum with one conformation inside the AF2 training set, run head-to-head against the 8-protein post-cutoff stratum | That the method works only because the target's structures were absent from training — the memorization control | p9, p11 |
| MurJ re-analysed with TM13–14 excluded | That the bifurcated MurJ TM-score profile reflects a real global two-state split rather than one hypervariable helix pair | p9, p11 (Fig G in S1 Text, not held) |
| PfMATE analysed with TM1 excluded | That the score is dominated by a crystal-contact artefact in the reference structure | p9 |
| Same 12 targets as the MSA-subsampling comparator [7] | Nothing on its own — this is a shared-target literature comparison, not a re-run of the comparator. **The comparator method was NOT re-executed here**; its outcomes are quoted from the published paper | p3, p9, p13 |

- **confidence_as_discriminator**: **NO — pLDDT is used for model *selection* and for
  chain *truncation*, never to judge conformational correctness, and the paper does not
  validate it for that purpose.**
  - Selection: Fig 1 caption, p3, "the model with the highest pLDDT, AF2's ranking of
    model confidence, is shown in red"; p12, "Typically, the top ranked model is probed to
    identify contact points within the structure, though any of the five models can be
    used" — note the explicit statement that the choice does not matter much.
  - Truncation: p14, "Both the N- and C- terminal ends were truncated where the pLDDT
    values were less than the mean of all the pLDDT values."
  - **Structural quality is judged by MolProbity, not by pLDDT**, and conformational
    correctness by TM-score to the references (p4, p14). The only pLDDT-accuracy claim is
    a citation to someone else's work, p13: "This is supported by results that showed that
    AF2's pLDDT score is highly correlated to model accuracy [24]". pTM and PAE are never
    mentioned. **`confidence-as-discriminator` NOT tagged.**

## D. Claims

- **central_conclusion**: Alanine-substituting the residues that form 3D contacts with a
  sliding 11-residue sequence window — the contacts read off AF2's own template-free
  initial model, the substitution applied to every non-gap sequence in the full-depth
  MSA — makes AF2 return conformations it does not otherwise produce, yielding per-target
  ensembles that span the deposited endpoint states for 11 of 12 membrane proteins (all
  but CGRPR) plus adenylate kinase and ribose binding protein. Because the intervention is
  on the alignment rather than on templates or MSA depth, it works whether or not one of
  the target's conformations was in AF2's training set, which the authors present as a
  rebuttal to the training-set-bias explanation offered for the MSA-subsampling method's
  failures. MolProbity plus PCA are offered as reference-free filters so the pipeline can
  in principle run on a target with no known structures.

- **necessity_claims** (verbatim + page):
  - **On the method's own requirements — the key negative necessity claim:** "Our
    mutagenesis method requires no prior structural knowledge about the protein of
    interest or its conformational landscape." (p12)
  - **On what the reference-based metric requires:** "While the relative TM scores
    highlight the conformational flexibility, this comparison requires the availability of
    more than one experimental structure." (p4)
  - **On the prevailing view they are attacking:** "The implication is that the distance
    matrix, which AF2 derives from the MSA, contains information on this heterogeneity
    although at present, the general consensus is that AF2 is only able to predict a single
    conformation." (p2)
  - **On the comparator's limits (a necessity claim about ref [7], not about this
    method):** "In the previous report using these targets, the authors were able to
    increase the number of apo-like structures for all of the GPCRs, but were unable to
    obtain alternate conformations of MCT1 without using a structural template [7]." (p9)
  - **On the comparator's failure mode, from the Introduction:** "In contrast, this
    approach failed for 4 targets where one of the structures was present in AF2's training
    set, suggesting that in these cases AF2 may default to learned structures." (p2)
  - **On what remains undone:** "Further experiments would be needed to ascertain whether
    these models have a role in RBP function." (p6) — and — "How the makeup of the MSA,
    such as generated via MMseq2 or through the AF2 pipeline, affects the alternate
    conformations obtained by AF2 requires further examination." (p13)

- **novelty_claims** (verbatim + page):
  - "Here we present a general approach to drive Alphafold2 to model alternate protein
    conformations through simple manipulation of the multiple sequence alignment via in
    silico mutagenesis." (p1, Abstract)
  - "We have devised a method of in silico mutagenesis of the multiple sequence alignments
    (MSA) that are central to Alphafold2's prediction capabilities. The approach
    consistently unveils conformations not seen with the unmodified default MSA." (p1,
    Author summary)
  - "Here, we develop a general approach to transcend this apparent limitation of AF2 and
    consequently predict ensembles of conformations." (p2)
  - "This study introduces an alternative method for biasing the models generated by AF2
    that transcends the apparent bias of AF2 to conformations in its training set." (p2)
  - "Our methodology goes a step further than testing the validity of AF2 models by
    interrogating the conformational landscape of the protein in the context of the
    underlying biochemical function." (p2–3)
  - "The broad range of TM scores spanning the range between the two structures is a
    remarkable demonstration that this method unlocks AF2's ability to predict alternate
    conformations." (p4)
  - "This demonstrates the general utility of our methodology in generating ensembles of
    multiple conformations regardless of whether the protein is in the training set."
    (p13)
  - **No claim to be "first" or "unprecedented" is made about the method itself.** The
    word "unprecedented" appears once on p1 and refers to AlphaFold2's CASP XIV
    performance, not to this work. The paper positions itself as "an alternative method"
    (p2) to ref [7], which it cites as prior art throughout.

- **stated_limits**:
  - **One outright failure, named:** "the approach described here is capable of generating
    both conformations for all of the targets, except CGRPR" (p13); and p8, "We observed
    for the GPCRs, PTH1R and FZD7 but not CGRPR, an increase in the breadth of
    conformations that lie between the two experimental structures."
  - **Two partial failures, conceded:** PfMATE — "Conversely, there are hardly any
    additional conformations for PfMATE" (p9); SERT — "SERT does adopt alternate
    conformations, though the structural changes are not completely in the direction of the
    second experimental conformation." (p9)
  - **The method's central failure mode is misfolding:** "Because targeting interaction
    surfaces with alanine substitutions could lead AF2 to generate models that are
    misfolded" (p4), with examples where "beta sheets being replaced by alpha helices"
    (p4).
  - **Window size is a free parameter with a scope caveat:** "a smaller window might be
    more appropriate when the structural elements of the protein of interest are smaller or
    similar in size to the length of this window." (p12)
  - **Compute cost scales inversely with window size:** "As the length of the window gets
    smaller, more models need to be generated and the compute time of the AF2 calculations
    increases." (p12)
  - **Results are conditional on the models being right, stated twice as an explicit
    hypothetical:** "If the AF2 models generated here for the transmembrane helices 13–14
    region are correct, this would suggest that there is coupling between ion gradients and
    movement of transmembrane helices 13–14" (p11); "If the AF2 models for SERT are
    correct, then there are more conformations at the extrema for the transport cycle of
    serotonin." (p11)
  - **Deposited structures may not bound the sampled range:** "Positions of the
    experimental structures relative to the AF2 models would suggest that not all of the
    experimental structures are at the extremes of the range of conformational
    heterogeneity." (p9)
  - **Unexplained models remain after filtering:** "The models within the scattered region
    with higher PC2 values are spread across several sets of mutations and do not appear to
    be misfolded (Fig C in S1 Text). Further experiments would be needed to ascertain
    whether these models have a role in RBP function." (p6)
  - **The MSA source is an uncontrolled variable:** "How the makeup of the MSA, such as
    generated via MMseq2 or through the AF2 pipeline, affects the alternate conformations
    obtained by AF2 requires further examination." (p13)
  - **The physics claim is hedged with a contrary citation:** "though the learned physical
    principles do not describe protein folding pathways [25]." (p13)
  - **Fold-switching is proposed, not tested:** "would support this methodology in
    examining fold-switch proteins where the standard AF2 pipeline was generally unable to
    model both conformations [20]." (p12) — no fold-switching protein is in the target set.
  - **Nothing was validated experimentally:** the models are offered as hypotheses —
    "These in silico structures can guide experimental design and be tested using
    spectroscopic approaches" (p13).

- **stance**: **`precedent` + `contrast`. PROVISIONAL — the user's call, not settled
  here.**
  - **`precedent` on findings.** This is the earliest MSA-manipulation method in the
    corpus and it establishes the family's core empirical claim with a genuinely
    template-free, full-depth, no-deposited-structure input pipeline: that intervening on
    the alignment alone moves AF2 off its default basin, on 16 proteins across
    transporters, GPCRs, a periplasmic binding protein and a small kinase. It also
    establishes the two structure-agnostic filters (MolProbity, PCA) that the field then
    largely ignored, and it runs a real training-set stratification and a real negative
    control.
  - **`contrast` on rigour.** Success is called by eye off TM-score scatter plots with no
    stated threshold; the quality filter was calibrated on two targets whose endpoints were
    known; the PCA outlier removal is manual, uncounted and iterated "until there were no
    apparent outliers" (p14); the PCA panels never report variance explained; per-panel n
    is never given after filtering; the directional-control arm, the negative control and
    the parameter sweep are all in an SI the corpus does not hold; and the memorization
    control that carries the paper's boldest claim has n = 4.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Targets on which both conformations were generated | 11 of 12 (all except CGRPR) | count | TM-score plots vs two deposited endpoint structures per target; **no threshold stated** | p13 |
| Targets in the post-cutoff stratum (both states outside AF2 training) | 8 | count | Training-set membership inherited from ref [7] | p3, p6 |
| Transporters in that stratum whose breadth and endpoint correspondence increased | 5 of 5 (MCT1, STP10, Lat1, ZnT8, ASCT2) | count | "the breadth of variability and correspondence to the two experimental structures increased in all cases" | p8 |
| GPCRs in that stratum whose inter-state breadth increased | 2 of 3 (PTH1R, FZD7 yes; CGRPR no) | count | Visual comparison of TM-score plot breadth | p8 |
| Targets in the training-set-overlap stratum (one state inside AF2 training) | 4 (MurJ, PfMATE, SERT, CCR5) | count | Training-set membership inherited from ref [7] | p3, p9 |
| Targets in that stratum generating alternate conformations | 4 of 4, but two only weakly (PfMATE "hardly any"; SERT "not completely in the direction") | count | TM-score plots vs deposited structures | p9, p11 |
| AK: RMSD between the two reference crystal structures | 7.2 | Å | 4ake (open) vs 1ake (closed) | p4 |
| AK: TM-score between the two reference crystal structures | 0.68 | TM-score (dimensionless, 0–1) | 4ake vs 1ake; drawn as the dashed line in Figs 2C and 2E | p4, p5 |
| AK: sliding-window sets of interacting residues identified | 21 | count of mutated-MSA variants | 11-residue window over pLDDT-truncated chain | p4 |
| AK: models generated from mutated MSAs | 315 | models | 21 sets × 15 models | p4 |
| AK: total models scored (mutated + unmodified) | 330 | models | 22 sets × 15 | p4 |
| AK: modal MolProbity score range | 1.6–1.9 | MolProbity score | Histogram of all 330 models, Fig 2D | p4 |
| RBP: sliding-window sets | 27 | count | 11-residue window | p6 |
| RBP: total models scored | 420 | models | 28 sets × 15 | p6 |
| RBP: models surviving the MolProbity filter | 315 of 420 (75%) | models | Set-level rejection at >1 SDM above the median | p6 |
| Models generated per MSA variant | 15 | models | 3 ColabFold runs × 5 AF2 model parameter sets, seed varied per run | p3–4, p14 |
| Alanine-scanning window length | 11 (also tested at 8 and 5 on AK; 3 on ubiquitin) | residues | Justified by expected size of transmembrane helices and by model count | p12 |
| Contact cutoff defining residues to mutate | 4 | Å | Justified to "encompass polar and ionic interactions including those mediated by water" | p14 |
| Primary-sequence exclusion window for contact partners | 4 | residues | Justified "To keep from destabilizing secondary structure" | p14 |
| MolProbity set-rejection threshold | mean of set > median of all + 1 SDM | MolProbity score | All models for that target | p4, p14 |
| PfMATE, directed arm: conversion of outward-open to inward-open | 100% of models ("all of the models generated from the mutated MSA") | proportion | Visual conformational call; supporting panel in unheld SI (Fig H) | p11 |
| LmrP, directed arm: outcome | "mostly outward-open conformations that match the experimental structure" — **no count given** | qualitative | Single experimental outward-open structure; panels in unheld SI (Fig I) | p11 |
| LmrP, unmodified MSA: models not inward-open | 4 (judged misfolded, "partially open on both sides") | models | PCA + visual inspection; panels in unheld SI | p11 |
| ColabFold / AF2 parameter version | v2.1 | version | — | p11 |
| Ubiquitin control: additional conformations found | 0 ("lack of any new conformations") | count | PCA overlap with NMR ensembles; all panels in unheld SI (Fig K) | p12–13 |
| PCA variance explained by PC1 / PC2 | **NOT REPORTED** — never given for any target | % | — | Figs 2F/H, 3F, 4D, 5D |
| Models surviving filtering, per membrane-protein target | **NOT REPORTED** — given only for AK and RBP | models | — | Figs 4C, 5C |
| Total models generated across the study | **NOT REPORTED** — only AK (330) and RBP (420) are stated | models | — | — |
| Any per-target TM-score value for the membrane proteins | **NOT REPORTED** in the main text — readable only from the scatter plots; "best model based on TM score" panels are in the unheld SI | TM-score | — | p8, p10 |
| Runtime, GPU-hours or compute cost | **NOT REPORTED** — only the qualitative statement that smaller windows increase compute time | — | — | p12 |
| Head-to-head numbers vs the MSA-subsampling comparator | **NOT REPORTED** — the comparator was not re-run; its outcomes are quoted from ref [7] as prose | — | — | p9, p13 |

- **n_predictions**: recorded at three levels, per the v3 instruction not to collapse them.
  - **Per MSA variant: 15 models** = 3 `colabfold_batch` runs × 5 AF2 model parameter
    sets, with the random seed changed per run. p3–4: "This modified MSA alignment is then
    used 3 times, varying the random seed, to generate 15 models from AF2. The unmodified
    MSA is also run additional times to obtain 15 initial models." p14: "The subsequent
    runs using the modified sequence and MSA were again carried out with colabfold_batch, 3
    times for each MSA for a total of 15 models for each 11 aa window examined. A
    modification was made to batch.py within ColabFold to allow for a different random seed
    for each run".
  - **Per target: (number of windows + 1) × 15**, and the number of windows scales with
    chain length after pLDDT truncation. Stated only twice: **AK = 330** (21 mutated sets +
    1 unmodified, p4) and **RBP = 420** (27 mutated sets + 1, p6). For the twelve membrane
    proteins — all longer than AK and RBP — the per-target count is **NOT REPORTED**, but
    on the same formula each is plainly in the high hundreds.
  - **Targets: 16 distinct proteins** (see `n_targets`), of which 14 are scored against
    two deposited endpoint structures, LmrP against one, and ubiquitin against NMR
    ensembles.
  - **Total across the study: NOT REPORTED.**

- **comparable_to_ours**: *(left empty per schema v3 — the extractor cannot see our
  numbers.)*

- **si_in_scope**: **SI NOT HELD — and for this paper the gap is material, not
  cosmetic.** `S1 Text` is listed on p14–15 as "Contains all supplemental Tables and
  Figures. Table A: Membrane Protein Structures. Fig A: Examples of Misfolded Adenylate
  Kinase. Fig B: Structural intermediates of Ribose Binding Protein. Fig C: Structures
  outside the transition from 2dri to 1ba2 are not misfolded. Fig D: Plots matching models
  to experimental structures. Fig E: Conformation diversity of the models. Fig F: Plots
  matching models to experimental structures. Fig G: Analysis of MurJ without
  transmembrane helices 13 and 14. Fig H: PfMATE conformational flexibility. Fig I: LmrP
  conformational flexibility. Fig J: PCA of Adenylate Kinase. Fig K: SPEACH_AF on
  ubiquitin." Not present in `pdfs/`. **What this removes from the corpus:** the entire
  evidence base for `directional_control` (Figs H and I), the entire negative control
  (Fig K), the window-size sensitivity analysis (Fig J), the per-target PDB accessions and
  therefore any independent audit of the training-set cutoff (Table A), and the
  best-model-vs-experiment comparisons (Figs D and F). Every directional and control claim
  in this note is therefore quoted from main-text prose with its figure evidence unseen.
  Code and data are available (p1, "https://github.com/RSvan/SPEACH_AF") but are not held
  either.

## F. Figures

Fifteen panel-group rows across five figures. Split on `mark` or `measure` per the v3
rule; RENDER panels within a figure are merged where only `facet` differs.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 3 | The SPEACH_AF workflow: MMseqs2 MSA → 5 AF2 models → pick highest-pLDDT model → identify a contact point (3 residues, red) → alanine-substitute those columns across the whole MSA → re-fold → new conformation built on different contacts (blue) | schematic | `SCHEMATIC \| MSA→AF2→contact identification→whole-column alanine substitution→re-fold, with before/after cartoon structures \| no data` | 1 unlettered composite; no panel letters | The single illustrated example uses **3** mutated residues, whereas the actual protocol mutates an 11-residue window's full 4 Å contact set (p14) — the figure understates the size of the intervention. No target is named. | CC BY 4.0, no ND clause — p1: "This is an open access article distributed under the terms of the Creative Commons Attribution License, which permits unrestricted use, distribution, and reproduction in any medium, provided the original author and source are credited." Redrawing permitted. |
| 2A-B, 2G | 5 | AK reference structures (1ake closed / 4ake open superposed), the unmodified-MSA model with chain thickness encoding per-residue rmsf, and a highlight of the mis-built ATP-binding lid found in the PCA outlier group | structure render | `RENDER \| facet: purpose (3: two-crystal superposition, rmsf-weighted model, outlier-lid highlight) \| views: 1 \| overlay: 2 references in A; 1 outlier model on 2 references in G \| axis: none` | 3 of 8 letters (A, B, G); one system (AK); differ by purpose, not camera angle | 2B encodes rmsf 0–3 Å as chain thickness with a legend but **no quantitative rmsf panel** — a continuous per-residue measure shown only as line width, unreadable to a number. 2G shows one hand-picked representative of an unstated number of outliers. | CC BY 4.0, no ND — p1 |
| 2C, 2E | 5 | Every AK model placed by its TM-score to each of the two crystal structures, before (C) and after (E) MolProbity set rejection; colour = relative MolProbity | scatter | `PLOT \| facet: filtering stage (2: all models, MolProbity-parsed) \| vary: TM-score to 1ake (closed), 0.70–1.00 (continuous) \| series: relative MolProbity score (MP−MPmin)/MPmin, 0.0–0.8 (continuous colourbar) \| measure: TM-score to 4ake (open), 0.58–0.92 \| n: 1 model per mark; 330 per panel in C, parsed subset NOT REPORTED in E` | 2 of 8 letters; facet is filtering stage, same system | **Both axes truncated** — x starts at 0.70, y at ~0.58; neither reaches 0, so the visual spread is exaggerated relative to the true metric range. Parsed-panel n is not given, so the reader cannot tell how many models the filter removed. | CC BY 4.0, no ND — p1 |
| 2D | 5 | Distribution of MolProbity scores over all AK models, with the retained subset overlaid | bar (histogram) | `PLOT \| facet: none (1) \| vary: MolProbity score, ~1.4–2.7 (continuous, binned) \| series: model set (2: all models blue, MolProbity-parsed red hatched) \| measure: count \| n: 330 models in the blue series; parsed count NOT REPORTED` | 1 of 8 letters | Bin width not stated. The rejection threshold (median + 1 SDM) is **not drawn on the axis**, so the reader cannot see where the cut fell. Parsed-series n not given. | CC BY 4.0, no ND — p1 |
| 2F, 2H | 5 | PCA of the MolProbity-parsed AK models with the two crystal structures projected on, before (F) and after (H) removal of the mis-built-lid outlier cluster | scatter | `PLOT \| facet: outlier-removal stage (2: parsed, outliers removed) \| vary: PC1, −2 to 5.5 (continuous) \| series: none (models and the two named crystal structures share one mark style, distinguished only by colour and text label) \| measure: PC2, −4.5 to 3.5 \| n: 1 structure per mark; per-panel n NOT REPORTED` | 2 of 8 letters | **Variance explained by PC1 and PC2 is never reported**, for this or any other PCA panel in the paper — a reader cannot tell whether PC1 carries the transition or noise. Units are arbitrary and unstated. The number of models removed between F and H is not given, and the removal was by eye (p14). | CC BY 4.0, no ND — p1 |
| 3A-B | 7 | RBP reference structures (1ba2B open / 2dri closed superposed) and the unmodified-MSA model with chain thickness encoding rmsf | structure render | `RENDER \| facet: purpose (2: two-crystal superposition, rmsf-weighted model) \| views: 1 \| overlay: 2 references in A; 15 models summarised as rmsf in B \| axis: none` | 2 of 6 letters; one system (RBP) | 3B collapses 15 models into a thickness scale with no quantitative panel, same defect as 2B. | CC BY 4.0, no ND — p1 |
| 3C, 3E | 7 | Every RBP model placed by TM-score to the open and closed crystal structures, before (C) and after (E) MolProbity set rejection; colour = relative MolProbity | scatter | `PLOT \| facet: filtering stage (2: all models, MolProbity-parsed) \| vary: TM-score to one reference (continuous) \| series: relative MolProbity score (continuous colourbar) \| measure: TM-score to the other reference (continuous) \| n: 1 model per mark; 420 per panel in C, 315 in E (p6)` | 2 of 6 letters | Axes truncated as in Fig 2 (neither reaches 0). This is the one figure where the parsed n **is** recoverable, from the text on p6 rather than the caption. | CC BY 4.0, no ND — p1 |
| 3D | 7 | Distribution of MolProbity scores over all RBP models, with the retained subset overlaid | bar (histogram) | `PLOT \| facet: none (1) \| vary: MolProbity score (continuous, binned) \| series: model set (2: all models, parsed) \| measure: count \| n: 420 all; 315 parsed` | 1 of 6 letters | Rejection threshold not drawn on the axis; bin width not stated. **Caption inconsistency with Fig 2D:** here the criterion is worded "one standard deviation from the median" (p7) where Fig 2D says "one standard deviation above the median" (p6) — the Methods (p14) say "greater than one SDM from the median". The direction of the cut is stated three ways. | CC BY 4.0, no ND — p1 |
| 3F | 7 | PCA of the MolProbity-parsed RBP models with the two crystal structures projected on | scatter | `PLOT \| facet: none (1) \| vary: PC1 (continuous) \| series: none \| measure: PC2 (continuous) \| n: 1 structure per mark; 315 models + 2 crystal structures per panel` | 1 of 6 letters | Variance explained not reported. The "scattered region with higher PC2 values" the text discusses (p6) is not marked or delimited on the plot. | CC BY 4.0, no ND — p1 |
| 4A | 8 | Unmodified-MSA models for the eight membrane proteins whose structures both postdate AF2 training, chain thickness encoding rmsf across the 15 initial models | structure render | `RENDER \| facet: protein (8: MCT1, STP10, LAT1, ZnT8, ASCT2, CGRPR, PTH1R, FZD7) \| views: 1 (membrane-normal, all in the same orientation) \| overlay: 15 models summarised as rmsf per panel \| axis: none` | 8 panels in one lettered row, faceted by protein | rmsf shown only as chain thickness against a 0–3 Å legend; no quantitative rmsf panel anywhere in the paper. GPCR panels show **only the transmembrane region** (p6), which is not stated in the caption. | CC BY 4.0, no ND — p1 |
| 4B-C | 8 | TM-score placement of models against each protein's two deposited structures — B the 15 unmodified-MSA models, C all mutated-MSA models after MolProbity parsing; the two rows are the paper's central before/after result | scatter | `PLOT \| facet: protein (8) × model set (2: unmodified-MSA initial, mutated-MSA parsed) \| vary: TM-score to reference 1, 0.5–1.0 (continuous; the PDB ID differs per panel) \| series: none (single mark colour) \| measure: TM-score to reference 2, 0.5–1.0 \| n: 1 model per mark; 15 per panel in B, NOT REPORTED per panel in C` | 16 panels across two lettered rows (8 proteins × 2 model sets); B and C share `mark` and `measure` and differ only by facet, so they are one row | **Per-panel n is absent throughout row C** — the number of models surviving filtering is never given for any membrane protein, so the reader cannot compare density between panels or between proteins. **Both axes truncated at 0.5**, not 0. **The headline claim ("both conformations for all targets except CGRPR", p13) has no quantitative panel** — no threshold line, no per-target summary, no count; the pass/fail call is made by eye from these scatters. Colour carries no information here although it did in Figs 2C/3C, so the MolProbity dimension is silently dropped. | CC BY 4.0, no ND — p1 |
| 4D | 8 | PCA of the parsed model sets for the same eight proteins, with the experimental structures projected on and labelled by PDB ID | scatter | `PLOT \| facet: protein (8) \| vary: PC1 (continuous, per-panel arbitrary units) \| series: none (models and named experimental structures share a mark style) \| measure: PC2 (continuous) \| n: 1 structure per mark; per-panel n NOT REPORTED` | 8 panels in one lettered row | Variance explained never reported for any panel. **Additional models were removed by hand before these plots and neither the criterion nor the count is given** — p9: "In some cases, additional sets or individual models were removed from the initial PCA", p14: "manual inspection for outliers... repeated until there were no apparent outliers". The V-shape / gap / scatter readings in the text (p9) are pure shape description with no statistic. Axis ranges differ per panel, so apparent spread is not comparable across proteins. | CC BY 4.0, no ND — p1 |
| 5A | 10 | Unmodified-MSA models for the four membrane proteins with one conformation inside the AF2 training set, chain thickness encoding rmsf | structure render | `RENDER \| facet: protein (4: MurJ, PfMATE, SERT, CCR5) \| views: 1 \| overlay: 15 models summarised as rmsf per panel \| axis: none` | 4 panels in one lettered row | Same rmsf-as-thickness defect as 4A. PfMATE's TM1 is excluded from analysis (p9) but the exclusion is not marked on the render. | CC BY 4.0, no ND — p1 |
| 5B-C | 10 | TM-score placement for the training-set-overlap stratum — B the 15 unmodified-MSA models, C all mutated-MSA models after parsing. This is the arm carrying the paper's memorization rebuttal | scatter | `PLOT \| facet: protein (4) × model set (2: unmodified-MSA initial, mutated-MSA parsed) \| vary: TM-score to reference 1 (continuous) \| series: none \| measure: TM-score to reference 2 (continuous) \| n: 1 model per mark; 15 per panel in B, NOT REPORTED per panel in C` | 8 panels across two lettered rows | Per-panel n absent in row C. Axes truncated. **n = 4 proteins carries the claim that training-set membership does not matter (p11, p13), and the figure offers no summary statistic, no aggregate and no comparison panel against the n = 8 stratum in Fig 4** — the two strata are never plotted together, so the comparison the paper's argument rests on has to be made by flipping between pages 8 and 10. | CC BY 4.0, no ND — p1 |
| 5D | 10 | PCA of the parsed model sets for the four training-set-overlap proteins, experimental structures projected on | scatter | `PLOT \| facet: protein (4) \| vary: PC1 (continuous, per-panel arbitrary units) \| series: none \| measure: PC2 (continuous) \| n: 1 structure per mark; per-panel n NOT REPORTED` | 4 panels in one lettered row | Variance explained never reported. Manual outlier removal uncounted (p9, p14). The MurJ panel's "square shape" and its V-shaped TM13–14-excluded counterpart are discussed together in the text (p11) but the counterpart is in the unheld SI (Fig G), so the comparison cannot be checked. | CC BY 4.0, no ND — p1 |

**Licence, once, for all rows:** CC BY (Creative Commons Attribution License), stated on
**p1** in the copyright block: "Copyright: © 2022 Stein, Mchaourab. This is an open
access article distributed under the terms of the Creative Commons Attribution License,
which permits unrestricted use, distribution, and reproduction in any medium, provided
the original author and source are credited." **No ND clause and no NC clause** — the
figures may be reproduced, redrawn and modified with attribution. Individual figure DOIs
are printed under each caption (e.g. `.g001` on p3, `.g004` on p8).

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5, single-paper extraction session)
- **schema_version**: v3
- **confidence**: **medium-high.**
  - **High** for the mechanism, the protocol, the target list, the licence, the claims and
    the tags: the text layer is clean and the Methods (p13–14) describe the algorithm at
    residue resolution.
  - **Medium** for anything touching the directional-control arm, the negative control,
    the window-size sweep and the per-target PDB accessions: **all of that evidence is in
    `S1 Text`, which the corpus does not hold**, and this note quotes main-text prose about
    figures it has not seen.
  - **Medium** for figure `n` and for `metric_saturation`: post-filter model counts are
    given only for AK and RBP, and no summary statistic appears anywhere in the paper.
  - Two pages (5 and 8) were rendered at 150 dpi to read axis ranges, colourbar ranges and
    panel grids, none of which are in the text layer. Fig 2's caption is split across p5
    and p6 in the text layer; both halves were used.
- **unresolved**:
  1. **`method_class` has no value for this paper, and neither does the Method tag
     vocabulary.** SPEACH_AF modifies the *content* of MSA columns (alanine substitution
     across all sequences) while leaving depth and column count intact. That is neither
     `msa-subsample` (no depth reduction — the paper itself distinguishes the two on p13),
     nor `msa-state-filter` (no state-specific alignment is substituted), nor
     `template-state-bias` (templates off), nor `af-cluster`, nor `latent-steering` (the
     v3 note explicitly excludes MSA manipulation from that tag). **A tag such as
     `msa-mutagenesis` or `msa-column-perturbation` is needed and I have not invented it.**
     Consequence: **no Method tag is applied to this paper at all**, so a reverse lookup
     for MSA-manipulation methods will miss the earliest member of that family. This is the
     single most consequential gap in the note.
  2. **No Protocol tag fits a no-template, full-MSA regime.** `templates-on` is false,
     `no-template-no-msa` requires *both* to be absent and the MSA here is full-depth, and
     `state-annotated-input` is false. A `templates-off` tag is needed. No Protocol tag
     applied.
  3. **Whether `continuum` should join `ensemble` and `two-state`.** Several targets are
     described as filling the whole path between endpoints (Lat1, p8; the V-shaped
     transporter PCAs, p9), which is continuum behaviour in the output. I did not apply
     `continuum` because no continuous reaction coordinate is ever operationalised — PC1
     is unlabelled, un-normalised, and its variance fraction is unreported. A reader
     applying the tag differently would not be wrong. Flagged rather than decided.
  4. **The training-set cutoff is not auditable from this PDF.** The 8/4 partition is
     inherited verbatim from ref [7] (p6, p9). No cutoff date, no PDB release dates, and no
     accessions appear in the article; Table A is in the unheld SI. `anti_memorization_design`
     is recorded as present and genuine, but it is present *on the authors' say-so*.
  5. **The MolProbity rejection direction is stated three inconsistent ways**: "one standard
     deviation above the median" (p4/p6 caption), "one standard deviation from the median"
     (p7 caption), "greater than one SDM from the median" (p14 Methods). "Greater than
     median + 1 SDM" is the only reading consistent with discarding poor structures, and is
     what this note records, but the paper does not say it unambiguously.
  6. **How many models the manual PCA outlier step removed is unknown for every target.**
     p9: "In some cases, additional sets or individual models were removed from the initial
     PCA." p14: "repeated until there were no apparent outliers." No counts, no criterion.
     This sits between route 3 (clean — no state labels used) and a plain reproducibility
     defect; I have recorded it under route 3 as a caveat rather than as leakage.
  7. **LmrP's directed result is quantified only as "mostly".** p11: "These mutations
     prompted AF2 to generate mostly outward-open conformations that match the experimental
     structure". No count, no fraction; Fig I is in the unheld SI. The directional-control
     claim for LmrP therefore has no number attached to it anywhere in the held material.
  8. **v3 ambiguity — RENDER rows where panels differ in *purpose* rather than camera
     angle or system.** Fig 2's A, B and G are all renders of adenylate kinase but show,
     respectively, two crystal structures, an rmsf-weighted model, and a highlighted
     mis-built region. Under "split on `mark` or `measure`, never on `facet` alone" these
     merge, since RENDER has neither slot. I merged them and put "purpose" in `facet`,
     which the grammar permits ("`facet` is new in v3... Markers and systems are facets")
     but does not clearly anticipate. **The deeper problem: RENDER has no `mark`/`measure`
     slots, so the v3 splitting rule is undefined for renders** — every render in a figure
     merges into one row by construction, however unrelated. Worth a rule.
  9. **v3 ambiguity — a render that encodes a continuous measure (rmsf as chain
     thickness).** Figs 2B, 3B, 4A, 5A carry a real per-residue quantity with a numeric
     legend (0–3 Å) but no axes. RENDER says "with no data axes"; PLOT needs a `vary` and a
     `measure` that do not exist. I used RENDER and logged the missing quantitative panel
     under `hides`, but a "render with an encoded measure" is a genuine sixth shape and it
     recurs (it is how this whole subfield draws flexibility).
  10. **v3 ambiguity — `series:` when the legend dimension is *identity*, not condition.**
      In Figs 2F/H, 3F, 4D, 5D the experimental structures are drawn in a different colour
      from the models and labelled with PDB IDs. That is a two-level legend dimension
      (model vs reference) but it is identity rather than a condition, and writing
      `series: mark identity (2)` felt like it would pollute the join key. I wrote
      `series: none` with a note in `panels`. A rule for reference-point overlays in PLOT
      would help; they are ubiquitous in this corpus.
  11. **`metric_saturation` for a bounded metric with no reported values.** TM-score is
      bounded [0,1] and several arms visibly sit at ~0.95–0.97 on one axis, but the paper
      reports no numbers, so I cannot say whether any *comparison* saturates. v3 says
      "numeric saturation only", which I read as requiring reported numbers; the field
      therefore reads NOT REPORTED even though the render shows near-ceiling clustering.
      If the intent is "the metric is bounded and an arm approaches the bound", the answer
      would flip. Worth one clarifying sentence in the schema.
  12. **`n_targets` for a paper with several partly-overlapping target sets.** 16 distinct
      proteins, but 12 in the benchmark, 14 scored against two references, 2 in the
      directed arm (one of them a repeat), 1 negative control. A single integer loses the
      structure; I gave the integer plus the breakdown.
- **why_it_matters**: *(left empty per schema v3 — the user's call.)*

---

## Tags

`transporter` `gpcr` `periplasmic-binding` `general-protein`
`ensemble` `two-state`
`continuous-metric` `visual-metric`
`oracle-leak` `design-level-oracle` `anti-memorization` `unpowered`
`directed-state` `apo-sampling` `seed-only`
`peer-reviewed`
`precedent` `contrast`
`comparator-numbers`

**Tag rationale, including deliberate omissions:**

- **`transporter`** — nine of sixteen targets: MCT1, STP10, Lat1, ZnT8, ASCT2 (p6), MurJ,
  PfMATE, SERT (p9), LmrP (p11). This is the paper's dominant system.
- **`gpcr`** — four targets: CGRPR, PTH1R, FZD7 (p6) and CCR5 (p9). Applied, with the
  caveat recorded in `system` that **only the transmembrane region was modelled** (p6) and
  that CGRPR is the paper's single outright failure (p13). A GPCR query should return this
  paper.
- **`periplasmic-binding`** — ribose binding protein, "a bacterial periplasmic protein
  involved in the chemotactic response to ribose" (p6).
- **`general-protein`** — adenylate kinase and ubiquitin.
- **`kinase` is deliberately NOT applied**, and this is the schema's own instruction:
  "`kinase` means protein kinase; adenylate kinase and other small-molecule kinases are
  `general-protein`". Adenylate kinase is "a nucleoside monophosphate kinase" (p4), not a
  protein kinase. Tagging it would false-positive every kinase-conformation query.
- **`fold-switching` is NOT applied** — the paper only *proposes* the method for
  fold-switch proteins (p12) and tests none.
- **`atpase` is NOT applied** — no ATPase is studied; adenylate kinase is a phosphotransferase.
- **`ensemble`** — the systematic arm's product and the paper's own framing (p1, p13).
- **`two-state`** — the targeted arm's product; PfMATE flips 100% of models from
  outward-open to inward-open (p11).
- **`continuum` is NOT applied** — see `unresolved` item 3; the behaviour is arguably
  continuous but no reaction coordinate is operationalised.
- **`single-state` is NOT applied** — the method does not collapse onto one basin; that is
  the baseline it is designed to escape.
- **`continuous-metric`** — TM-score (continuous, TM_align, p14) and PCA coordinates.
- **`visual-metric`** — applied deliberately and it is the paper's main rigour defect:
  **no threshold is stated for calling a conformation**, and the headline "both
  conformations for all of the targets, except CGRPR" (p13) is read by eye off the
  scatter plots. Outlier removal is likewise "manual inspection" (p14) and the PCA state
  calls are shape descriptions ("V-shaped", "square shape", p9/p11).
- **`rmsd-only` is NOT applied** — the reference metric is TM-score, not RMSD (only one
  RMSD value appears in the whole paper, p4), and it is not the only metric since PCA runs
  alongside it. Applying `rmsd-only` would misdescribe both halves.
- **`saturating-metric` is NOT applied** — see `metric_saturation` and `unresolved` item 11;
  TM-score is bounded and some arms sit near the ceiling, but no numbers are reported.
- **`oracle-leak`** — routes 4, 5 and 6: the MolProbity filter was validated against the
  two known AK/RBP structures (p4, p6), success is adjudicated by TM to deposited
  structures with no threshold (p13), and "best model" is defined by TM to a held
  reference (p8, p10).
- **`design-level-oracle`** — route 7, kept distinct from the above per v3: every scored
  target was chosen because both states are deposited (p3), and the targeted arm declares
  the expected state before reading the result (p11). Weaker than pipeline leakage, and
  the authors are open about it.
- **`prospective` is NOT applied** — `prospective` is `partial` (see field), and the
  adjudication, filter calibration and target list are all retrospective. Applying the tag
  would overstate it.
- **`anti-memorization`** — a genuine, explicit two-stratum training-set design (8
  post-cutoff, 4 with one state in training) with the control arm actually run and
  analysed (p6, p9, p11). Note that the task brief anticipated `NONE` / `NONE RUN` here;
  that is **not** what the paper does, and this is one of the earliest papers in the corpus
  to run a training-set-membership control at all.
- **`no-anti-memorization` is NOT applied** — it would be flatly wrong.
- **`unpowered`** — per the v3 rule (n < ~10): the memorization control stratum is n = 4
  and the post-cutoff stratum is n = 8, with no statistics of any kind and two partial
  failures inside the n = 4 arm (PfMATE, SERT — p9).
- **`multi-backbone` is NOT applied** — one backbone (AF2 v2.1 via ColabFold, p11, p13).
- **`confidence-as-discriminator` is NOT applied** — pLDDT selects the model to scan and
  truncates termini (p12, p14); MolProbity and TM-score do the discriminating. pTM and PAE
  are never mentioned.
- **`experimental-validation` is NOT applied** — no wet-lab work. The models are offered as
  hypotheses to be "tested using spectroscopic approaches" (p13), i.e. future work. The
  ubiquitin control compares against *published* NMR ensembles, which is not the authors
  running an experiment.
- **`directed-state`** — the targeted-mutagenesis arm (p11): choosing which interface to
  alanine-substitute flips PfMATE completely and LmrP mostly, and the authors claim this
  as a usable directional handle.
- **`apo-sampling`** — every prediction is a bare single chain. p6: "The modeling excluded
  accessary or interacting proteins. In addition, only the transmembrane spanning region is
  modeled for the GPCRs." No ligand, no partner, no nanobody, no G protein anywhere in the
  paper.
- **`seed-only`** — a genuine arm, not just a nuisance parameter: the unmodified-MSA runs
  vary the random seed across 3 runs (p14) and this alone yields multiple conformations for
  ZnT8, ASCT2 and Lat1 (p8), which the paper credits explicitly (p13: "the first step in
  obtaining alternate conformations are multiple runs of AF2 with different random seeds").
- **`partner-driven`, `ligand-driven`, `peptide-driven`, `g-protein-mimetic`, `nanobody`
  are NOT applied** — none of these handles exists in the paper; see `apo-sampling`.
- **No Site tag.** MurJ's TM13–14 lipid II isoprenoid-tail site is discussed (p9, p11) and
  PfMATE's central cavity is implied, but no binding site is the object of study, and the
  method targets *inter-domain interfaces*, which the vocabulary's `orthosteric` /
  `allosteric-site` / `cryptic-pocket` triple does not cover. `allosteric-failure`
  describes a sampling outcome this paper does not report.
- **No Method tag and no Protocol tag** — see `unresolved` items 1 and 2. Both omissions
  are positive statements that the v3 vocabulary lacks the needed term, not oversights.
- **`peer-reviewed`** — PLOS Computational Biology research article with a named academic
  editor and received/accepted/published dates (p1). Not a preprint.
- **`precedent` + `contrast`** — see `stance`; provisional.
- **`negative-result` is NOT applied** — CGRPR's failure (p13) and PfMATE's weak response
  (p9) are conceded limits inside a positive paper, not the paper's substance.
- **`comparator-numbers`** — applied, but read the caveat in `metrics_reported`: the
  durable numbers are the counts (11/12, 8, 4, 5/5, 2/3), the model counts (330, 420, 15
  per MSA), the AK reference separation (7.2 Å / TM 0.68) and the parameter values (11-residue
  window, 4 Å cutoff). **There is no per-target TM-score table anywhere**, so any numeric
  comparison against this paper's per-target performance has to be read off scatter plots
  or taken from the unheld SI.
- **`figure-exemplar` is NOT applied** — the figures carry real defects (axes truncated at
  0.5/0.70, PCA variance never reported, post-filter n never given, the headline claim with
  no quantitative panel) and should not be recommended as design templates. They are useful
  as *negative* examples, which is what the `hides` column records.
