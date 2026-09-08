# swapna2025memorization

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–19), which coincide with
the printed PLOS pagination (1/19 … 19/19).** Layout: p1 title/abstract, p2 author summary +
Introduction start, p3–4 Introduction, p4–5 Methods, p5–13 Results, p13–15 Discussion and
Conclusions, p15–16 Supporting Information list, p16–17 acknowledgments/contributions,
p17–19 references. Fig 1 on p7, Fig 2 on p8, Fig 3 on p9, Fig 4 on p10, Fig 5 on p12.

**Load-bearing caveat, recorded up front:** the paper's central quantitative evidence — the
per-target stratification by training-set availability (S1 Table), the ESMfold-vs-AF2 template
test (S2 Table), the per-protocol success matrix (S3 Table) and the AF2-vs-AF3 template-flip
test (S4 Table) — lives entirely in **DOCX supporting files that the corpus does not hold**.
The main text narrates those tables in prose but tabulates nothing. See `si_in_scope`.

---

## A. Identity

- **citekey**: `swapna2025memorization`
- **doi**: **10.1371/journal.pcbi.1013590** — p1. Matches `refs.bib`. Data/scripts at Zenodo
  **10.5281/zenodo.17386602** (p2, Data availability statement).
- **year**: **2025**. Received 1 May 2025, accepted 6 October 2025, published 17 October 2025 (p1).
- **venue**: **PLOS Computational Biology 21(10): e1013590** (p1). **Peer-reviewed, not a
  preprint** — p1: "PLOS recognizes the benefits of transparency in the peer review process;
  therefore, we enable the publication of all of the content of peer review and author responses
  alongside final, published articles." Editor: Alex Peralvarez-Marin (p1). Tag `peer-reviewed`.
- **title**: Memorization bias impacts modeling of alternative conformational states of solute
  carrier membrane proteins with methods from deep learning — p1
- **authors**: G.V.T. Swapna, Namita Dube, Monica J. Roth, Gaetano T. Montelione (co-corresponding
  Roth and Montelione) — p1. Rensselaer Polytechnic Institute and Rutgers RWJMS.
  Competing interest declared: "GTM is a founder of Nexomics Biosciences, Inc." (p2).

## B. Scope

- **system**: **transporter** — the Solute Carrier (SLC) superfamily of integral membrane
  transporters, both MFS-fold and LeuT-fold, plus non-SLC-numbered bacterial/parasite
  transporters (DgoT, YddG, PfCRT) treated as members of the same structural class.
  p3: "many SLC transporters have a characteristic structural architecture with pseudo two-fold
  symmetry, where the two halves of the protein structure are related by a two-fold symmetry
  axis in the plane of the membrane bilayer". Tag `transporter`. **Not** `periplasmic-binding`,
  **not** `atpase` — no soluble binding protein and no ATPase in the paper.
- **n_targets**: **10 proteins in the assessment table (S1 Table), 9 of which have a main-text or
  SI figure.** Enumerated from the text:
  - *Both states in the PDB at training (n = 2)*: DgoT (E. coli D-galactonate:proton symporter,
    S1 Fig) and human ZnT8/SLC30A8 (Fig 2) — p6, p7.
  - *One state in the PDB at training (n = 5)*: Zea mays CMP-sialic acid transporter 1 SLC35A1
    (Fig 3), S. cerevisiae GDP-mannose transporter Vrg4 / SLC35D (Fig 4), reduced folate
    transporter SLC19A1 (S5 Fig), aromatic amino acid exporter YddG (S4 Fig), chloroquine
    resistance transporter I (S6 Fig) — p6, p9, p11. Assignment of the individual five to this
    bin is inferred from the group membership stated on p6 and the protein list on p11; the
    table itself is not held.
  - *No homologous structure in the PDB at training (n = 3)*: SLC19A2 (thiamine transporter 1,
    S3 Fig), SLC35F2 (Fig 5), SLC35F3 — p6. **SLC35F3 appears in no figure**; it is named only
    in the S1 Table narration.
  - Chain-level detail: ZnT8 is a "2 x 320-residue homodimeric" protein and both states come
    from the two chains of one cryoEM entry, 6xpf-A (inward) and 6xpf-B (outward) — p7.
  - **Generality flag:** the paper generalises to "pseudo-symmetric SLC proteins" as a class
    (p15) and to the memorization claim across deep-learning structure prediction, from 10
    proteins, of which the never-in-training arm is n = 3.
- **method_class**: **dual — template-biasing + benchmark-only.**
  - *Template-biasing* is the proposed method: an ESMfold model built from a virtual
    sequence-permuted ("flipped") sequence is used as the structural template for the alternative
    state. p6: "In the ESM-AF/MODELLER process, the N-terminal (blue) and C-terminal (purple)
    segments of protein sequences are first swapped to create a virtual flipped sequence… The
    resulting virtual structure serves as a structural template for modeling the original protein
    sequence using template-based modeling with AF2/3 (if no state-specific bias is observed) or
    with MODELLER."
  - *Benchmark-only* is the memorization assessment arm: conventional AF2/AF3, shallow MSAs,
    dropouts, AF-alt, AFsample, AFsample2 run purely to characterise bias (p6, p10–11).
  - Comparator arms additionally exercise **MSA-subsampling** (shallow MSAs) and **enhanced
    sampling** (dropout, MSA masking); neither is the paper's own method.
- **backbones**: **AF2, AF3, ESMFold, and MODELLER, compared head to head → tag `multi-backbone`.**
  - AF2: ColabFold v1.5.5 server with AlphaFold2.ipynb; AF-Multimer weights v2.1.2, v2.2.0 and
    v2.3.2 for the AFsample/AFsample2 runs (p4–5).
  - AF3: the DeepMind/Isomorphic Labs server (no templates) **and** a locally installed instance
    (templates supported) — p5, p11.
  - ESMFold: `ESMFold_advanced.ipynb`, masking_rate = 0.15, stochastic_mode = "LM" (no dropout),
    recycle 12, highest-pTM model selected (p5).
  - MODELLER 10.4 (p5); SwissModel named as an interchangeable alternative, not run as a reported
    arm (p11: "Template-based modeling could also be done using SwissModel [60] or other
    template-based modeling methods").
  - Enhanced-sampling wrappers over AF2: AlphaFold-alt (Del Alamo/Meiler scripts), AF_Sample,
    AF_Sample2 (p5).
  - No Boltz, Chai, OpenFold3 or Protenix anywhere.
- **templates**: **dual — off for the assessment arm, on for the proposed method.**
  - Off: "The standard AF2 modeling in this study used no templates (unless specified)" (p5);
    AF3 server runs "(with no structural templates)" (p5); AFsample and AFsample2 "with no
    templates" (p5).
  - On: the whole ESM-AF/ESM-MODELLER protocol is template-based, the template being a *de novo*
    ESMfold model of a permuted sequence, **not a deposited structure** (p6).
  - Also on, as a side arm for one target: "with var-ious other protocols using templates of
    distant homologues and multiple seeds" for SLC35F2 (p10) — deposited homologue structures,
    result not separately reported.
  - **Not state-annotated in the database sense**: no GPCRdb/KLIFS-style curated state label is
    used anywhere. The template's state is defined by the sequence permutation, not by a lookup.
  - Tags: both `templates-on` and `state-annotated-input` apply to the proposed method
    (the input template is deliberately state-directed), plus `no-template-no-msa` for the
    ESMfold step, which runs on a single sequence with no homologs.
- **msa_handling**: **full + subsampled + masked, and one arm with no MSA possible.** These are
  distinct and are not collapsed:
  - *Full*: "default multiple sequence alignments (MSAs), recycle of 12, and random dropouts"
    (p5); local AF3 with "full MSAs generated with jackHMMR" and, as a check, MMseqs (p11).
  - *Subsampled (depth reduction)*: AF-alt "480 models … using randomly-sampled shallow MSAs
    (typically ranging from 16 - 32 sequences, though in some cases described in Supplementary
    Material runs were made using 4 - 8, 8 - 16, and even with a single sequence), with 30 models
    created per MSA depth" (p5); and in the ESM-AF template step "AF2 modeling was done using
    single-sequence inference, and also with shallow MSAs (8, 16, or 32), recycle of 12, and with
    dropout" (p11).
  - *Masked*: AF_Sample2, which the Introduction classifies as MSA masking (p2), run with 3
    max_recycles and no templates (p5).
  - *No MSA available by construction*: the flipped virtual sequence — p6: "Note that this
    flipped sequence has no homologs with which to generate a multiple-sequence alignment."
    This is the mechanistic core of why the trick works and is **not** MSA subsampling.
  - **No state-filtered MSA anywhere.** Do not tag `msa-state-filter`.

## C. Conformational core

- **states_generated**: **two + single-state.**
  - *Two* for the proposed protocol: inward-open and outward-open for every target it succeeded
    on, e.g. p7–8 for ZnT8 and p11 for the four additional proteins ("the ESM-MODELLER protocol …
    provided models of both inward-open and outward-open states").
  - *Single-state* for every AF2/AF3 arm without the ESM template, and for every enhanced-sampling
    arm on SLC35F2 despite ~6,480 models: p11: "all three of these methods generated exclusively
    outward-open states (S2A–C Fig)."
  - Occluded/intermediate states are explicitly **not** produced or analysed: p13: "Although the
    ESM-AF2/MODELLER protocols sometimes also generate such occluded states, these states were
    not explored in this study." So this is two-state, not ensemble or continuum, by design.
  - Tag both `two-state` and `single-state`.
- **structural_priors_used**: substantial, and mostly legitimate at design time rather than
  leaking into the pipeline:
  1. **Prior structural knowledge that SLC transporters have internal pseudo-two-fold symmetry
     and that the transport cycle is a swap of the two halves' conformations.** This is the entire
     basis of the method. p4: "their unique pseudo-symmetrical transport mechanisms, which
     provides the basis for an elegant method of modeling the inward-open (or outward-open)
     conformations of some SLC proteins from knowledge of their outward (or inward) open
     conformations by swapping the pseudo-symmetric structures of the N- and C-terminal halves".
     Credited to Forrest and others, refs [31,44–50].
  2. **Target selection driven by what is deposited.** p8–9: "In the two cases above, we chose SLC
     proteins for which experimental structures of both outward- and inward-open conformations
     are available, and validated the ESM-AF2 modeling protocol against both the experimental
     atomic coordinates (using Cα RMSD metrics) and against EC based contact maps".
  3. **Deposited coordinates as the reference for RMSD scoring**: 6xpf-A/B (ZnT8, cryoEM 3.9/4.1/
     5.1 Å, p7), 6i1r-A (SLC35A1, X-ray 3.22 Å, p9), 5oge (Vrg4, X-ray 2.80 Å, p9).
  4. **AF2-predicted secondary structure/topology used to locate the symmetry split point.**
     p13: "Protein secondary structure and AF2 predictions indicate 10 helices connected by short
     loops. Chopping the sequence at the exact center of the loop between symmetric halves and
     swapping the coordinates of the two halves orients the helices with inverted conformation".
  5. **Sequence-derived, not structure-derived, validation signal**: EC contact predictions from
     NeBcon (probability threshold 0.7) confirmed with EVcouplings (p4). The authors are explicit
     that this is an experimental-sequence-derived quantity: p14: "ECs are an interpretation of
     experimental protein sequence data, and hence this validation is effectively against
     experimental data."
  None of items 1–5 is by itself a methodological defect; items 2, 3 and 4 nevertheless feed
  `oracle_leakage` routes 5, 6 and 7 below.
- **oracle_leakage**: **present, but concentrated in evaluation and design rather than in the
  generative step.** Seven routes, each answered separately:
  1. **Deposited structure as input or template — PARTIAL / mostly NONE FOUND.** The proposed
     method's template is *generated*, not deposited: p6, "The 3D structure of this virtual
     sequence is then modeled using ESMfold, a large-language model-based method that requires no
     templates and only a single input sequence." The baseline AF2/AF3/AFsample arms ran with no
     templates (p5). **The exception**, for one target: p10, "Conventional AF2 modeling was
     carried out using the AF2-multimer colab server [55] executed both with the standard protocol
     without structural templates described in the Methods section and also with var-ious other
     protocols using templates of distant homologues and multiple seeds." Deposited homologue
     structures entered that arm; its per-model result is not separately reported.
  2. **State annotations from a curated database driving templates or alignments — NONE FOUND.**
     No GPCRdb / KLIFS / Kincore analogue is used. The one candidate database is named only as
     future work: p14, "It may also be possible to identify correct symmetry using repeat
     definitions identified by symmetry analyses available in the Encompass database [65]."
     Protocol described p4–5 and p6.
  3. **Cluster labels derived from known states — NONE FOUND.** No AF-Cluster-style clustering is
     run; sequence clustering appears only as a cited prior method in the Introduction (p2).
     Protocol p4–5.
  4. **Hyperparameters / sweep ranges / stopping criteria tuned against known states — PRESENT,
     as an iterative stopping criterion.** p14: "The contact maps generated for the flipped
     conformers are always compared with the EC-contact map. In cases where the match is not
     reflecting the contacts of the flipped state accurately, a few trials were made in the
     elimination of residues of the loop regions." The number of trials, the acceptance criterion
     and which targets required it are all NOT REPORTED. Also p13–14: "In these cases, the long
     loop was replaced by an 8 to 12 residue polyglycine linker, and the split was made at the
     center of this linker" — the 8–12 residue range is a swept range with no per-target value
     given. Selection scores themselves (highest pTM for ESMfold, lowest DOPE of 20 for MODELLER,
     p5) are internal and not oracle-derived.
  5. **Success defined post hoc by RMSD/TM to a structure they had — PRESENT, wherever a
     reference exists.** p7: "matching the cryoEM inward-open structure 6xpf-A (Cα RMSD = 2.00 Å)"
     and "excellent agreement with the experimental 6xpf-B (Cα RMSD = 1.09 Å)". p11: "with
     excel-lent agreement (< 1 - 2 Å rmsd) to experimental models where available". No threshold
     for what counts as success is stated.
  6. **Best/worst model labels assigned against a held reference — PRESENT.** The reported model
     is chosen from the top-scoring set *by its state*, not by score: p11, "For EMS-AF2, the
     top-ranked model was outward-open, but other top-scoring models were inward-open." And
     p11: "All 5 top-scoring models were assessed for representatives of the alternative
     conformational state." Likewise the enhanced-sampling arms are scored by whether any model
     in 480/3,000 matched the expected state (p10–11).
  7. **Design-level oracle use — PRESENT AND PERVASIVE; this is the dominant route, and it is
     weaker than pipeline leakage.** The expected answer is declared before the result is read in
     three ways: (a) targets are chosen because both states are deposited (p8–9, quoted under
     `structural_priors_used`); (b) the direction of the flip is asserted a priori from the
     pseudo-symmetry model, so "the alternative conformational state" is named before modelling
     (p6, p13); (c) for SLC35F2, where neither state is deposited, the outward-open assignment of
     the AF2 model and the inward-open assignment of the ESM model are made against the
     symmetry-derived expectation, with EC maps as the only external check (p10–12).
     Tag `design-level-oracle` **and** `oracle-leak` (routes 4–6 are pipeline-side).
- **prospective**: **partial.** Prospective in targets for SLC35F2 and SLC35F3, for which no
  experimental structure of either state exists (p10: "Of particular interest are SLC proteins
  for which no experimental structures are available for either the inward- or outward-open
  states"), and the SLC35F2 models are validated only against EC contacts. Retrospective in
  everything else: the eight remaining targets are scored against deposited coordinates, and the
  expected state is fixed by design in all ten (route 7). No target is prospective in both its
  reference and its expected answer. Do **not** tag `prospective`.
- **state_metric**: **dual — RMSD-to-reference + visual only.**
  - *RMSD-to-reference*, where a reference exists: backbone Cα RMSD and GDT "performed using the
    methods of Zemla implemented on their public server" (p5). Values: 2.00 Å and 1.09 Å for
    ZnT8 (p7), "< 1 - 2 Å rmsd" for the four additional proteins (p11).
  - *Visual*, for the actual inward-vs-outward call: **the criterion is never operationalised.**
    Nothing in the paper defines a numeric predicate separating inward-open from outward-open —
    no cavity-volume threshold, no distance between gating helices, no RMSD-to-each-of-two-
    references decision rule. The call is made by looking at which side of the membrane the
    surface cavity opens onto, rendered as space-filled voids with the KVFinder web server
    (Fig 2E–F, Fig 3A–B, Fig 4A–B, Fig 5A–C captions, p8–12), and by cylinder/topology diagrams.
    **Threshold for the state call: NOT REPORTED** — used on every target and never stated.
  - *Contact-map agreement*, the third de facto criterion, is also visual: agreement is asserted
    from circled regions, with no overlap statistic. Its two numeric thresholds are stated and
    are the only quantitative thresholds in the paper: **NeBcon probability threshold 0.7** and
    **contacts defined at interresidue Cα distance < 10.0 Å** via CMview (p4).
  - Tags `rmsd-only` is *not* right on its own; use `continuous-metric` (RMSD/GDT) plus
    `visual-metric` (the state call).
- **metric_saturation**: **yes, numerically, in the enhanced-sampling arms.** The reported measure
  there is a count of alternative-state models, and it **floors at zero** for all three methods on
  SLC35F2: 0 of 480 (AF-alt), 0 of 3,000 (AFsample), 0 of 3,000 (AFsample2) — p10–11, "all three
  of these methods generated exclusively outward-open states". At the floor the three methods are
  mutually indistinguishable, so the arm cannot rank them. The AF2-with-full-MSA arm across all
  ten proteins is similarly a floored binary (p6). The Cα RMSD values reported (1.09–2.00 Å) are
  far from any ceiling and do not saturate. The S1/S3/S4 Table success counts are 0/1-style
  binaries per target (p6, p11) and are ceiling-prone by construction but are not held.
  Figure-level defects are recorded in `hides`, not here.
- **directional_control**: **yes — the handle is a sequence permutation that produces a structural
  template.** Specifically: split the sequence at the pseudo-symmetry axis, swap the N- and
  C-terminal halves, fold the permuted sequence with ESMfold, and hand the result to the
  downstream engine as a template (p6). Two further handles: (i) **choice of downstream engine**,
  since MODELLER honours the template's state and AF2/AF3 often do not — p11, "the ESM-AF2
  protocols described here fail to generate the alternative conformational state when one
  conformational state was available in the PDB at the time of AF2 training"; (ii) **the permuted
  sequence itself as direct input to a sampler**, which is the cleanest demonstration in the paper
  — p11: "Interestingly, when AF-Sample was run on virtual flipped sequence of SLC35F2,
  exclusively inward-open conformational states for the flipped sequence were generated."
  The control is **unreliable through AF2/AF3**: the engine overrides the supplied template and
  flips back to the memorized state in 4 of 6 tested cases for AF3 (p11–12). Not partner-, ligand-,
  nanobody-, peptide- or seed-driven; tag `directed-state` only.
- **anti_memorization_design**: **PRESENT but weak — a three-way stratification of the 10 targets
  by training-set availability, with no date cutoff given.**
  - Cutoff definition: **qualitative, not a date.** The phrase used throughout is "available in
    the PDB at the time of AF2 training" (p6, and repeated p11, p13). **No training cutoff date,
    no PDB release-date filter, and no procedure for checking membership are reported anywhere.**
    Record as NOT REPORTED on the mechanism.
  - Counts (p6): **n = 2** with both states available; **n = 5** with exactly one state available;
    **n = 3** with "no homologous structures … available in the PDB at the time of training".
  - The only substantiation offered for the n = 3 arm is a homology argument on one member —
    p10: "SLC35F2 has < 12% sequence identity with any SLC35 subfamily members of known
    structure; in particular there is no good experimental structure that can be used as a
    template for comparative modeling of its inward- or outward-open conformations."
  - This is a stratification of a small convenience set, not a temporal held-out benchmark.
    Tag `anti-memorization` (a design exists) and `unpowered`.
- **anti_memorization_control**: **RUN AS AN ANALYSED ARM, and UNPOWERED (n = 3 in the never-in-
  training bin).** It is not merely a set that exists: the three bins are compared directly and
  the comparison is the paper's headline. p6, in full, is the analysis:
  > "In the first two systems (DgoT and ZnT8), both inward- and outward-open states were available
  > in the PDB at the time of AF2 training. AF2 with full MSAs (with or without dropouts) is biased
  > towards predicting only the inward-open state. … For the next 5 systems listed in S1 Table,
  > only one state (inward- or outward-open) was available in the PDB at the time of AF2 training.
  > For this set, AF2 with full MSAs (with or without dropouts) is biased towards predicting only
  > the state available for training (in 4 cases the outward-open state, in 1 case the inward-open
  > state). … Using shallow MSAs the alternative state is delivered as one or more of the generated
  > models in only one of the 5 cases; i.e., for SLC19A1. For the last 3 cases summarized in S1
  > Table, no homologous structures were available in the PDB at the time of training. AF2 with
  > full MSAs (with or without dropouts) again delivers a single dominant state. … Using shallow
  > MSAs (4 - 16 sequences) the alternative state is delivered as at least one of the generated
  > models for SLC19A2, but only the outward-open state is generated for SLC35F2 or SLC35F3."
  - **Effect size across the two comparable bins: 1 of 5 vs 1 of 3** alternative states recovered
    with shallow MSAs. That is not a separation, and the paper does not claim one statistically.
  - **The arm partially disconfirms a pure-memorization reading, and the paper says so.** p10:
    "Hence, even without a state-specific structure in their training sets, AF2 (and AF3) are
    biased towards the outward-open state of SLC35F2." The bias survives removal of the putative
    cause. This is the single most important qualification on the generality argument.
  - Mark `UNPOWERED`: n = 3, no statistics, no per-target numbers in the held PDF.
- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Conventional AF2, full MSA, no templates, ± dropout, on all 10 targets | That the second state is obtainable by default; establishes the single-state baseline the whole paper is measured against | 5, 6 |
| AF2 single-sequence inference, all targets | That simply removing the MSA is the fix — "AF2 inference with a single sequence consistently fails to generate a reasonable model" | 6 |
| Shallow-MSA depth sweep (4–8, 8–16, 16–32 sequences), all targets | That MSA subsampling is a sufficient remedy; alternative state recovered in 1 of 5 (one-state bin) and 1 of 3 (no-structure bin) | 5, 6 |
| AF-alt, 480 models on SLC35F2, 30 per MSA depth | That the failure is under-sampling of shallow-MSA space — 0 of 480 alternative-state models | 5, 10–11 |
| AF_Sample, 3,000 models on SLC35F2, weights v2.1.2/v2.2.0/v2.3.2, 21/3/9 max_recycles | That the failure is insufficient dropout-driven diversity, or a single-weight-version artifact — 0 of 3,000 | 5, 10–11 |
| AF_Sample2, 3,000 models on SLC35F2 (MSA masking) | That MSA masking, the other published state-diversification route, would succeed — 0 of 3,000 | 5, 10–11 |
| **AF_Sample run on the *virtual flipped sequence* of SLC35F2** | That the inward-open basin is physically unreachable by the network, or is an ESMfold-specific artifact; the same AF2 machinery yields "exclusively inward-open conformational states" once the sequence anchor is permuted. Isolates the sequence/MSA anchor, not the energy function, as the cause | 11 |
| ESMfold vs AF2 as the virtual-template generator (S2 Table) | That ESMfold is interchangeable with AF2 in the template step — ESMfold succeeded in all cases from single sequences, AF2 in none | 6 |
| **Template-flip test: hand AF2 the correct alternative-state template (S3 Table)** | That the model was never shown the answer. AF2 flips a supplied correct template back to the memorized state whenever that state was in training | 11 |
| Same template-flip test on locally installed AF3, 8 proteins (S4 Table) | That flip-back is an AF2-version or AF2-implementation artifact — AF3 also flipped back in 4 of the 6 tested (held only for SLC19A1 and SLC19A2) | 11–12 |
| jackHMMER vs MMseqs2 MSA generation for local AF3 | That the MSA-construction pipeline explains the flip-back — "The same results were obtained using MSAs generated by MMseqs" | 11 |
| AF3 server, no templates, on SLC35F2 | That the outward-open preference is AF2-specific — "Only the outward-open conformational state of SLC35 was returned by AF3" | 10 |
| EC contact-map validation (NeBcon p ≥ 0.7, cross-checked on EVcouplings) | That the flipped model is a geometric artifact with no independent support; ECs unique to each state are matched by the corresponding model. Structure-independent, sequence-derived | 4, 7–8 |
| Two targets with both states experimentally solved (ZnT8, DgoT) as positive controls | That the protocol produces plausible-but-wrong geometry — Cα RMSD 2.00 Å (inward) and 1.09 Å (outward) against 6xpf-A/B | 7–8, S1 Fig |
| Removal of physically unreasonable enhanced-sampling models (wrong chirality, non-native cis peptides) before analysis | That the 0-of-N counts are inflated by junk models being scored; also a possible source of bias, since the removal criterion is not quantified | 5 |

  Sixteen rows. The two bolded rows are the strongest: the flipped-sequence AF_Sample control and
  the template-flip test together rule out under-sampling *and* ignorance of the target state,
  which are the two standard benign explanations for single-state output.
- **confidence_as_discriminator**: **used for model selection, never validated for state, and
  shown to fail at it.** Confidence scores appear three times: average pLDDT over trimmed termini
  ranks AF-alt models (p5); highest pTM selects the ESMfold model (p5); lowest DOPE selects 1 of
  20 MODELLER models (p5). None is tested against conformational correctness. The paper reports
  direct evidence that ranking does **not** discriminate state — p11: "For EMS-AF2, the top-ranked
  model was outward-open, but other top-scoring models were inward-open", which is why "All 5
  top-scoring models were assessed for representatives of the alternative conformational state"
  (p11). Tag `confidence-as-discriminator` on the fact that scores gate which model is reported.

## D. Claims

- **central_conclusion**: For pseudo-symmetric SLC transporters, AF2 and AF3 return only one
  conformational state, and which state they return tracks what was deposited in the PDB at
  training time; the bias is not relieved by single-sequence input, shallow MSAs, dropout, MSA
  masking, or ~6,480 enhanced-sampling models, and it is strong enough that AF2/AF3 will flip a
  correct alternative-state template *back* to the memorized state. The authors' remedy is a
  hybrid: fold a sequence-permuted "flipped" virtual sequence with ESMfold to obtain a template,
  then build the alternative state from it with AF2/AF3 where no bias is present and with
  MODELLER where it is — validated against EC contact maps, and against deposited coordinates
  where those exist. **Two qualifications the paper itself supplies:** the outward-open bias
  persists for targets with no structure in training (p10), so memorization is not the whole
  story; and the AI half of the remedy is the part that fails, forcing a fallback to
  1990s-era comparative modelling. Also worth recording as a failure-to-replicate:
  p6, "Overall it was much harder to generate alternative conformational states (i.e., both
  inward- and o­utward-open states) for these SLC proteins using shallow MSAs than we expected
  from published studies."
- **necessity_claims** (verbatim + page):
  - p3: "To the degree that memorization biases the successful prediction of alternative
    conformational states, more robust methods leveraging the tools of AI-based modeling are
    required."
  - p3: "These observations suggest the need for more robust methods for modeling the multiple
    conformational states of this important class of membrane protein transporters."
  - p5: "These observations motivate the need for robust and consistent methods for modeling
    alternative conformational states (outward-open vs inward-open) of SLC proteins, at the very
    least for use as reference states for assessing the evolving deep learning methods for
    generating alternative conformational states of proteins."
  - p6: "AF2 inference with a single sequence consistently fails to generate a reasonable model."
  - p6: "In all cases, when using single sequences as input ESMfold provided a structural template
    with backbone structure matching the expected alternative conformational state, while AF2 was
    not able to generate reasonable structures for any of the virtual flipped sequence."
  - p11: "the ESM-AF2 protocols described here fail to generate the alternative conformational
    state when one conformational state was available in the PDB at the time of AF2 training."
  - p13: "This traditional approach requires an accurate sequence alignment between the two
    symmetric halves of SLC protein to generate a structural template for the alternative state,
    which can be quite difficult to generate."
  - p13: "Another shortcoming is that neither protocol can be applied directly to homodimeric
    pseudo-symmetric SLC proteins, such as YiiP or EmrE [27,63]."
  - p13: "Coordinates of SLC proteins with large loops and other structural decorations require
    manual editing to eliminate these loops/ decorations prior to applying the protocol."
  - p13–14: "For SLC proteins that have a long loop between their symmetric halves, chopping the
    sequence in the exact center fails to provide a flipped sequence that can be used to
    successfully generate a proper flipped conformer."
  - p14: "However, this validation is not as robust as validation against protein-specific
    experimental data such as X-ray crystallography, NMR, or cryoEM data."
  - p13 (on the class of methods being displaced): "molecular dynamics simula-tions are quite
    challenging, requiring powerful computing resources, accurate potential energy functions, and
    appropriate simulation of membrane-mimicking environments." (p3)
- **novelty_claims** (verbatim + page):
  - p4: "Although it is logical to combine the two concepts of validation with EC-based contact
    information and swapping of pseudo-symmetric structures, it has not yet been implemented as a
    general strategy for modeling SLC proteins."
  - p2 (Author summary): "Using either AlphaFold2 or AlphaFold3 in this process reveals bias due
    to "memorization" that challenges the view that modeling of the multiple conformational states
    of this important class of integral membrane proteins is a largely solved problem."
  - p15: "In this work we document bias in modeling multiple conformational states of SLC proteins
    that challenges the view that modeling of the multiple conformational states of this important
    class of integral membrane proteins is a largely solved problem."
  - p15: "We describe, validate, and compare hybrid ESM-AF2, ESM-AF3, and ESM-MODELLER protocols
    for modeling alternative conformational states of pseudo-symmetric SLC proteins."
  - p1 (Abstract) / p2: "This simple, rapid, and robust approach for modeling conformational
    landscapes of pseudo-symmetric SLC proteins is demonstrated for several integral membrane
    protein transporters, including SLC35F2 the receptor of a feline leukemia virus envelope
    protein required for viral entry into eukaryotic cells."
  - p4: "Here we describe a simple and robust approach for modeling alternative conformational
    states of pseudo-­symmetric SLC proteins using a combined ESM – template-based-modeling
    process inspired by the methods of Forrest and others [31,44–50]."
  - Priority is explicitly shared, not claimed outright, for the pseudo-symmetry swap itself
    (p4, refs [31,44–50]); the novelty claimed is the ESMfold-generated virtual template plus
    EC validation as a general strategy.
- **stated_limits** (all authors' own, Discussion p13–15):
  - The AI half of the method fails exactly where it is most needed: "In particular, where
    structures of only one of the alternative states was available in the PDB at the time of
    training, a significant bias towards this state was observed when AF2/3 were used either
    directly or as part of the ESM-AF modeling process. Although this bias is overcome using the
    ESM-MODELLER protocol, it is somewhat disappointing to have to sometimes resort to older
    template-based modeling methods in place of AI-based methods like AF2/3." (p13)
  - Not applicable to homodimeric pseudo-symmetric transporters such as YiiP or EmrE (p13).
  - Large loops and structural decorations require manual editing before the protocol runs (p13).
  - Validation quality is bounded by contact-prediction quality: "may not work well for SLC
    sequence families for which only shallow MSAs are available" (p13).
  - Occluded/intermediate states not explored (p13).
  - EC validation is weaker than target-specific experimental data (p14).
  - The AF3 server does not support user-supplied templates, so ESM-AF3 needs a local install
    (p13, p11).
  - Long-loop targets need a polyglycine linker substitution and, in some cases, iterative loop
    trimming judged against the EC map (p13–14).
  - Bias is variable and multi-factorial: "the impact of training memorization on both the ESM-AF2
    and ESM-AF3 protocols is highly variable and depends on multiple factors including the
    inference engine used and the nature and depth of the input MSA." (p13)
  - The authors concede memorization is not the only mechanism, citing Cfold: "in some cases, the
    network has learned enough to model alternative conformational states not included in the
    training data [70], in other cases success may in fact rely on some kind of memorization;
    i.e., both factors can be at play." (p14)
- **stance**: **`precedent` + `contrast`. Provisional — the user's call.**
  - *Precedent on findings*: it is the clearest published demonstration that memorization bias
    extends beyond fold-switchers and GPCRs to a large, structurally homogeneous membrane
    transporter family, and it adds a control (supplied-correct-template flip-back) that most
    memorization papers do not run. p14 makes the family-generality point explicitly: "The SLC
    proteins studied here have very similar overall structures and contact maps for the two
    states, yet the bias from conformational states available for the training process still
    strongly impacts the reliability of alternative conformational modeling by AF2/3."
  - *Contrast on rigour*: n = 10 with an n = 3 never-in-training bin; no training-cutoff date or
    membership test; no operationalised inward-vs-outward predicate; no quantitative
    contact-map agreement statistic; success judged by eye against a state declared in advance;
    an iterative loop-trimming step tuned against the validation criterion; and every per-target
    result in unsupplied DOCX tables.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Cα RMSD, ZnT8 inward-open, conventional AF2 | 2.00 | Å | cryoEM 6xpf chain A | 7, 8 |
| Cα RMSD, ZnT8 outward-open, ESM-AF2 | 1.09 | Å | cryoEM 6xpf chain B | 7, 8 |
| RMSD, 4 additional SLC proteins, ESM-MODELLER | "< 1 - 2" | Å | "experimental models where available" | 11 |
| Alternative state recovered with shallow MSAs, one-state-in-training bin | 1 of 5 (SLC19A1) | proteins | expected alternative state | 6 |
| Alternative state recovered with shallow MSAs, no-structure-in-training bin | 1 of 3 (SLC19A2) | proteins | expected alternative state | 6 |
| AF2 full-MSA bias direction, one-state bin | 4 outward-open, 1 inward-open | proteins | state available for training | 6 |
| Alternative-state models, AF-alt on SLC35F2 | 0 of 480 | models | inward-open call | 10–11 |
| Alternative-state models, AF_Sample on SLC35F2 | 0 of 3,000 | models | inward-open call | 10–11 |
| Alternative-state models, AF_Sample2 on SLC35F2 | 0 of 3,000 | models | inward-open call | 10–11 |
| AF_Sample on flipped SLC35F2 sequence | "exclusively inward-open" (count NOT REPORTED) | models | inward-open call | 11 |
| ESM-AF3 template flip-back, of the 6 where ESM-AF2 flipped | 4 of 6 flipped back; 2 of 6 held (SLC19A1, SLC19A2) | proteins | supplied ESM template state | 11–12 |
| Additional proteins where both ESM-AF2 and ESM-AF3 honoured the template | 2 | proteins | supplied template state | 12 |
| ESM-MODELLER success on the 4 additional proteins | 4 of 4 (both states) | proteins | EC map + experimental where available | 11 |
| SLC35F2 sequence identity to SLC35 members of known structure | < 12 | % | SLC35 subfamily | 10 |
| cryoEM resolution, ZnT8 6xpd / 6xpde / 6xpf | 3.9 / 4.1 / 5.1 | Å | — | 7 |
| X-ray resolution, SLC35A1 6i1r / Vrg4 5oge | 3.22 / 2.80 | Å | — | 9 |
| Contact definition | < 10.0 | Å, Cα–Cα | CMview | 4 |
| NeBcon EC probability threshold | 0.7 | probability | — | 4 |
| ESMfold masking rate | 0.15 | fraction | — | 5 |
| AF-alt runtime per run | < 3 | hours | 4× A100 HGX | 5 |
| *(cited, not measured here)* AF2+AF3 success on fold-switch alternative states, Porter and co-workers | 35 | % | >280,000 models | 14 |
| *(cited, not measured here)* Lazou et al. open+closed both recovered | 6 of 16 | proteins | — | 14 |
| *(cited, not measured here)* Cfold alternative conformations at TM-score > 0.8 | > 50 | % | nonredundant alternative pairs | 14 |

- **n_predictions**: recorded separately, as the schema requires.
  - *Per target, SLC35F2 (the deep arm)*: 480 AF-alt models (30 per MSA depth), 3,000 AF_Sample,
    3,000 AF_Sample2 → **≈ 6,480 models on one protein**, plus conventional AF2 and AF3 runs whose
    model counts are not given (p5, p10–11).
  - *Per target, routine arms*: AF2 top-5 scoring models assessed (p11); MODELLER 20 models per
    run with the lowest-DOPE one reported (p5); ESMfold — several models, count NOT REPORTED,
    highest-pTM one reported (p5).
  - *Targets*: 10 in the S1 Table assessment; 9 with a figure; 5 developed in the main text.
  - *Total models across all targets*: **NOT REPORTED.** Only SLC35F2 has a stated model budget.
- **comparable_to_ours**: *(left empty by the extractor, per schema v3)*
- **si_in_scope**: **SI NOT HELD — and this is the paper's core evidence, not an appendix.**
  The held PDF contains only the list of supporting files (p15–16). Missing and load-bearing:
  - **S1 Table** — "Assessment of modeling alternative states of SLC proteins with AF2": the
    per-target training-availability stratification on which the memorization claim rests. The
    main text narrates it (p6) but tabulates nothing.
  - **S2 Table** — ESMfold vs AF2 as virtual-template generator.
  - **S3 Table** — "Modeling of both outward-open and inward-open states of pseudo-symmetric SLC
    proteins": the per-protocol success matrix.
  - **S4 Table** — "Comparing bias of ESF-AF2, ESM-AF3, and ESM-MODELLER protocols in flipping the
    conformational state of SLC proteins": the template-flip test.
  - **S2 Fig** — the only quantitative panel for the 0-of-6,480 enhanced-sampling result.
  - **S1, S3–S6 Figs** — DgoT and the four additional proteins.
  - S7–S14 Figs are colour-blind-adjusted duplicates of Figs 2–5 and S3–S6 and carry no new data.
  Scripts and "key data" are at Zenodo 10.5281/zenodo.17386602 (p2), not retrieved here.
  Consequence: **no per-target number in this note can be checked against a table**, and the
  effect sizes above are reconstructed from the p6 and p11–12 prose.

## F. Figures

Five main-text figures, eleven panel-group rows. All are renders, schematics or contact maps —
**the paper contains no bar, box, violin, scatter or line plot of any measured quantity**, which
is itself the largest figure-level defect and is recorded per row in `hides`.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A–C | 7 | The ESM-AF/MODELLER protocol: abstract blue/purple two-half cartoon of the inward/outward flip (A), the workflow from wt sequence → chop → swap → ESMfold → template-based modeling → contact-map check (B), and 10-helix topology diagrams of SLC35F2 in outward-open, ESMfold-virtual and inward-open states (C) | schematic | `SCHEMATIC \| protocol workflow plus abstract two-half conformer cartoons and helix-topology diagrams for one representative protein \| no data` | 3 lettered panels; C is a vertical triple varying by state (outward / virtual flipped / inward). Panel B embeds a miniature contact map (residue number 0–400 on both axes) as an illustrative inset — a second shape inside one letter, not split out because it carries no readable data at that size | Panel A's blue/purple blocks are hand-drawn abstractions, not structures, so the "flip" is asserted graphically rather than shown; the inset contact map in B has no legend, no n and no scale | CC BY 4.0 (Attribution), no ND clause — p1–2 |
| 2A–B | 8 | Superposition of predicted on experimental ZnT8: AF2 inward-open (red) on 6xpf-A, ESM-AF2 outward-open (green) on 6xpf-B | structure render | `RENDER \| facet: conformational state (2: inward-open, outward-open) \| views: 1 (side view, membrane normal vertical) \| overlay: 1 prediction on 1 reference \| axis: none` | 2 panels varying by state; one model per panel | Shows **1 of 5** top-scoring models (p11 states all 5 were assessed) with no indication of which, and no spread across the 5; the RMSD lives only in the caption | CC BY 4.0, no ND — p1–2 |
| 2C–D | 8 | ZnT8 contact maps: EC-predicted contacts (black) against experimental (grey) and predicted (red inward / green outward) model contacts, with state-unique EC regions circled | heatmap (contact map, drawn as an overlaid point matrix) | `MATRIX \| rows: residue number (1–~250) \| cols: residue number (1–~250) \| value: contact present (Cα–Cα < 10 Å), by source: EC prediction / experimental structure / predicted model \| facet: conformational state (2: inward-open, outward-open)` | 2 panels varying by state; helix positions H1–H6 annotated on both axes | **The two triangles carry different data** — predicted model above the diagonal, experimental below — so prediction and experiment are never superimposed and a per-contact difference cannot be read off. Agreement is asserted from hand-drawn circles with **no overlap statistic, no contact count, no n**. The 0.7 EC threshold is in Methods, not the caption | CC BY 4.0, no ND — p1–2 |
| 2E–F | 8 | Space-filled surface-cavity renders of the inward-open (red) and outward-open (green) ZnT8 states, from KVFinder-web | structure render | `RENDER \| facet: conformational state (2: inward-open, outward-open) \| views: 1 \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 2 panels varying by state, no overlay | This is the *de facto* state-calling evidence and it is purely visual: **no cavity volume, no aperture measure, no threshold** — the criterion behind every inward/outward assignment in the paper appears only as a picture | CC BY 4.0, no ND — p1–2 |
| 3A–B | 9 | Zea mays SLC35A1: experimental outward-open (6i1r-A) vs ESM-MODELLER inward-open, each as a ribbon with the surface cavity coloured (green outward / red inward) above a numbered-cylinder helix diagram, membrane boundaries dashed | structure render | `RENDER \| facet: state × provenance (2: experimental outward-open, ESM-MODELLER inward-open) \| views: 2 (cavity-coloured ribbon; numbered helix-cylinder representation, helices 1–10) \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 2 lettered panels, each with 2 stacked sub-views | No superposition and no RMSD, because no inward-open reference exists; the state call rests entirely on the cavity colour. n of models behind the shown structure NOT REPORTED | CC BY 4.0, no ND — p1–2 |
| 3C | 9 | Combined outward-open (green) + inward-open (red) model contacts against the EC contact map (black) for SLC35A1 | heatmap (contact map) | `MATRIX \| rows: residue number (1–322) \| cols: residue number (1–322) \| value: contact present (Cα–Cα < 10 Å), by source: EC prediction / outward-open model / inward-open model \| facet: none (1)` | 1 panel, three overlaid contact sets, state-unique ECs circled in green and red | Unexplained ECs are conceded in words but never counted — caption: "At the thresholds chosen for ECs several predicted contacts are not explained by the combination of the two conformational states." No fraction-explained statistic, no n | CC BY 4.0, no ND — p1–2 |
| 4A–B | 10 | S. cerevisiae Vrg4 (SLC35D): experimental outward-open (5oge) vs modelled inward-open, same ribbon-plus-cylinder layout as Fig 3 | structure render | `RENDER \| facet: state × provenance (2: experimental outward-open, modelled inward-open) \| views: 2 (cavity-coloured ribbon; numbered helix-cylinder, helices 1–10) \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 2 lettered panels, each with 2 stacked sub-views | **Caption contradicts the text on provenance**: the figure title says ESM-MODELLER, but panel B is captioned "The inward-open structure modeled using ESM-AF2", while p9 states ESM-AF2 failed for this protein and ESM-MODELLER was used. See `unresolved`. Same visual-only state call as Fig 3 | CC BY 4.0, no ND — p1–2 |
| 4C | 10 | Combined outward-open (green) + inward-open (red) model contacts against the EC contact map (black) for Vrg4 | heatmap (contact map) | `MATRIX \| rows: residue number (1–337) \| cols: residue number (1–337) \| value: contact present (Cα–Cα < 10 Å), by source: EC prediction / outward-open model / inward-open model \| facet: none (1)` | 1 panel, three overlaid contact sets, state-unique ECs circled | Same as 3C: "several predicted contacts are not explained by the combination of two conformational states", unquantified; no n | CC BY 4.0, no ND — p1–2 |
| 5A–C | 12 | Human SLC35F2, no experimental structure for either state: AF2 outward-open (A), ESM-MODELLER inward-open (B), ESM-AF2 inward-open (C), each ribbon-with-cavity above numbered helix cylinders | structure render | `RENDER \| facet: protocol × state (3: AF2 outward-open, ESM-MODELLER inward-open, ESM-AF2 inward-open) \| views: 2 (cavity-coloured ribbon; numbered helix-cylinder, helices 1–10) \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 3 lettered panels, each with 2 stacked sub-views; panels vary by protocol, not by system | The paper's only fully prospective target and there is **no reference and no quantitative panel at all** — the two inward-open models (B, C) are never superposed on each other or given a mutual RMSD. Caption omits panel C from the membrane-boundary note. The 0-of-6,480 enhanced-sampling result for this same protein has its only panel in S2 Fig, which is not held | CC BY 4.0, no ND — p1–2 |
| 5D–E | 12 | SLC35F2 contact maps: outward-open (green) + ESM-MODELLER inward-open (red) against ECs (D), and outward-open + ESM-AF2 inward-open against ECs (E) | heatmap (contact map) | `MATRIX \| rows: residue number (1–~360) \| cols: residue number (1–~360) \| value: contact present (Cα–Cα < 10 Å), by source: EC prediction / outward-open model / inward-open model \| facet: inward-open protocol (2: ESM-MODELLER, ESM-AF2)` | 2 panels varying by which inward-open protocol supplied the red contacts | The comparison the paper draws from these two panels — "The ESM-AF2 inward-open structure explains a few more EC-based contacts than the ESM-Modeller protocol, particularly for predicted contacts between helices H6 and H9" (p11) — is a **counting claim with no count**; "a few more" is the entire effect size | CC BY 4.0, no ND — p1–2 |

**Licence, once, for all figures:** p1–2, "Copyright: © 2025 Swapna et al. This is an open access
article distributed under the terms of the Creative Commons Attribution License, which permits
unrestricted use, distribution, and reproduction in any medium, provided the original author and
source are credited." **CC BY, no NC and no ND clause — redrawing and modification are permitted
with attribution.**

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5)
- **schema_version**: v3
- **confidence**: **medium.** High for the protocol description, the claim quotations, the licence
  and the figure structure, all of which are unambiguous in the text layer and the two rendered
  pages. **Medium-to-low for every quantitative result**, because S1–S4 Tables and S1–S6 Figs are
  DOCX supporting files the corpus does not hold: the counts 2 / 5 / 3, 1-of-5, 1-of-3, 4-of-6 and
  2-of-6 are all reconstructed from prose on p6 and p11–12, and the assignment of individual named
  proteins to the three training-availability bins is partly inferred from the p11 protein list
  rather than read off the table. Text layer is clean; only soft-hyphen artifacts ("var-ious",
  "excel-lent", "o­utward-open") required repair, and quotes above reproduce the text layer.
  Two pages rendered (p7, p8) to settle whether Fig 1A is a molecular render or an abstract cartoon
  (it is an abstract cartoon → SCHEMATIC) and whether Fig 2C–D are matrices or plots (matrices,
  with the two triangles carrying different sources).
- **unresolved**:
  1. **No training-data cutoff is ever defined.** "Available in the PDB at the time of AF2
     training" (p6, p11, p13) is used as the paper's independent variable with no date, no PDB
     release-date filter and no stated membership test. Whether AF3's different cutoff was
     accounted for when AF3 results are pooled with AF2's is likewise unaddressed.
  2. **Which five proteins occupy the one-state bin of S1 Table** is inferred, not read. The p6
     narration gives only counts and one name (SLC19A1); the five names above come from combining
     p9 and p11 with the group sizes.
  3. **Fig 4 caption contradicts the Results text.** Figure title says ESM-MODELLER; panel B
     caption says "modeled using ESM-AF2" (p10); p9 says ESM-AF2 failed for Vrg4 and
     ESM-MODELLER succeeded. One of the three is wrong and the PDF does not resolve it.
  4. **SLC35F3 is named once (p6) and never shown.** It contributes to the n = 3 never-in-training
     bin but has no figure and no supporting panel in the listed SI.
  5. **No operationalised inward-vs-outward predicate.** Used on all 10 targets, stated nowhere.
     Recorded as NOT REPORTED in `state_metric`.
  6. **Iterative loop trimming has no stopping rule.** p14: "a few trials were made in the
     elimination of residues of the loop regions" — how many trials, on which targets, and what
     counted as an acceptable EC match are all unstated. This is the one place where the
     evaluation criterion could have shaped the model.
  7. **The distant-homologue-template arm for SLC35F2 (p10) has no reported result** beyond the
     blanket statement that only outward-open was returned; the number of templates, their PDB
     ids and the seeds used are not given.
  8. **AF_Sample on the flipped sequence has no model count** (p11) — "exclusively inward-open"
     out of an unstated N. This is the paper's most striking control and its n is missing.
  9. **Tags I wanted and could not use, per the fixed v3 vocabulary**: (a) a *sequence-permutation*
     or *virtual-sequence* method tag — the ESMfold-on-flipped-sequence trick is neither
     `template-state-bias` (the template is generated, not deposited or state-annotated) nor
     `msa-subsample` nor `latent-steering`; `template-state-bias` is the closest available and is
     used above with this caveat. (b) a *classical-comparative-modelling* backbone tag — MODELLER
     is the component that actually rescues the result and there is no method tag for it. (c) a
     *contact-map-validation* / *evolutionary-coupling* tag — EC validation is the paper's only
     external check and reverse lookup for it is impossible. (d) a *memorization-bias* rigour tag
     distinct from `oracle-leak`: this paper studies memorization in the *model's training set*
     rather than leaking an oracle into its own pipeline, and `oracle-leak` reads as an accusation
     against the authors when the finding is about AF2/AF3. None invented.
  10. **v3 ambiguities encountered, bluntly:**
      - **MATRIX has no `series` slot.** An overlaid contact map has a genuine legend dimension
        (EC / experimental / predicted) that PLOT would put in `series` and MATRIX has nowhere to
        put. I folded it into `value:` as "by source: …", which is a workable convention but is a
        convention I chose, so it will not join against another extractor who parks it in `facet`.
        This is exactly the drift the `series` slot was added to PLOT to prevent.
      - **The panel-splitting rule ("split on `mark` or `measure`") does not cover RENDER, MATRIX,
        TREE or SCHEMATIC**, none of which has a `mark` or a `measure`. Fig 2 has two render panel
        groups that differ only in `overlay` (superposition vs bare cavity render); I split them
        because the shapes are materially different for figure-design reuse, but the stated rule
        neither licenses nor forbids it.
      - **`metric_saturation` is defined for "any arm they report", but a floor at zero across
        three sampling methods is a *result*, not a measurement defect.** I recorded it because it
        is numerically a floor, but the field's phrasing invites recording every negative result
        as saturation. Worth a clarifying sentence.
      - **A figure that is *absent* has no home.** The central memorization evidence has no
        main-text panel at all; `hides` is per-figure-row, so "the claim's only quantitative panel
        is in unsupplied SI" had to go in `si_in_scope` and be cross-referenced from the 5A–C row.
      - **`templates` cannot express "the template is generated de novo by another network".**
        The on/off/state-annotated vocabulary makes an ESMfold-generated template look identical
        to a deposited one, which erases the paper's central cleanliness argument. I wrote it as
        dual prose.
- **why_it_matters**: *(left empty by the extractor, per schema v3)*

## Tags

`transporter` `template-state-bias` `msa-subsample` `enhanced-sampling` `benchmark-only`
`templates-on` `state-annotated-input` `no-template-no-msa` `two-state` `single-state`
`continuous-metric` `visual-metric` `saturating-metric` `oracle-leak` `design-level-oracle`
`anti-memorization` `unpowered` `confidence-as-discriminator` `multi-backbone` `directed-state`
`peer-reviewed` `precedent` `contrast` `negative-result` `comparator-numbers`

All from the fixed v3 vocabulary. Notes on the borderline choices:
- `template-state-bias` over `msa-state-filter`: the state handle is a supplied template, and no
  MSA is ever state-filtered. See `unresolved` item 9(a) for why the fit is imperfect.
- `msa-subsample` and `enhanced-sampling` are tagged for the **comparator arms** (shallow MSAs,
  AF-alt, AFsample, AFsample2), which were run and reported, not because they are the method.
- `no-template-no-msa` is tagged because the ESMfold step is single-sequence with no homologs by
  construction (p6) — the de novo input regime, applied to a virtual sequence.
- `saturating-metric` for the 0-of-480 / 0-of-3,000 / 0-of-3,000 floor (p10–11).
- `negative-result` for the failure to reproduce published shallow-MSA success rates (p6) and the
  0-of-6,480 enhanced-sampling result (p10–11).
- **Not** `prospective` (only partial, and the expected state is declared by design), **not**
  `gpcr` / `kinase` / `fold-switching` / `general-protein`, **not** `md` or `md-emulator`,
  **not** `af-cluster` or `latent-steering`, **not** `experimental` or `experimental-validation`
  (no wet-lab work; EC validation is computational inference from sequence data), **not**
  `orthosteric` / `allosteric-site` / `cryptic-pocket` / `allosteric-failure` (no binding-site
  analysis), **not** `rmsd-only` (RMSD is used but is not the state criterion), **not**
  `preprint`, **not** `figure-exemplar`.
