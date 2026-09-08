# wohlwend2024boltz1

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` with a reason where the field presupposes a conformational-state study this
paper is not.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–24), which coincide with the
printed page numbers.** Layout: p1 title + abstract + Fig 1; p2 contents + §1 Overview; p3–5 §2
Data pipeline (2.1 sources p3–4, 2.2 validation/test curation p4, 2.3 MSA pairing p5, 2.4
cropping p5, 2.5 pocket conditioning p5); p5–11 §3 Modeling (3.1 architecture p6, 3.2 training
and inference p6–7, 3.3 confidence model p7–9, 3.4 optimizations p9–11); p11–14 §4 Boltz steering
(4.1 intro p11, 4.2 method p11–12, 4.3 constraint potentials p12–14); p14–17 §5 Results; p18
§6 Conclusion + Table 1 + §7 Acknowledgments; p20–22 Algorithms 3–5; p23–24 references (23
entries). Figures: Fig 1 p1, Fig 2 p7, Fig 3 p8, Fig 4 p10, Fig 5 p15, Fig 6 p16, Fig 7 p17.
Algorithms 1–2 are inline at p9 and p13. **One table (Table 1, p18). No supplementary file, no
appendix beyond the algorithm listings.**

**DOCUMENT TYPE — a MODEL / SYSTEM paper.** It introduces a co-folding structure predictor
(Boltz-1), an inference-time steering procedure (Boltz-steering) and the model that results from
applying it (Boltz-1x), plus a released PDB train/validation/test split. It is not a
conformational-state study: **the words "conformation", "state", "ensemble", "apo", "holo",
"allosteric", "cryptic" never appear in a conformational-heterogeneity sense anywhere in the 24
pages.** "Conformer" appears only as (a) the RDKit/CCD input conformer of a ligand and (b) the
denoised sample inside the steering derivation. Consequently the conformational fields of
Section C are marked **NOT APPLICABLE with the reason restated**, not filled with a manufactured
reading. What the paper *does* supply that the corpus needs — an exact training cutoff, a
documented held-out split, a confidence-model specification, and the Boltz-1x/steering definition
— is recorded in full.

**PREPRINT VERSION.** The PDF footer on every page reads, verbatim: "bioRxiv preprint doi:
https://doi.org/10.1101/2024.11.19.624167; **this version posted May 6, 2025**". The DOI encodes
the original posting date 2024-11-19. **The version number ("v4") is nowhere printed inside the
PDF** — only the posting date is. The task metadata identifies this file as v4; that is recorded
here as external metadata, not as something the document states. Anyone citing "Boltz-1" against
a different bioRxiv version may be citing different numbers: the paper itself warns at p3 that
"this manuscript and its linked GitHub repository will be regularly updated". See `unresolved`.

---

## A. Identity

- **citekey**: `wohlwend2024boltz1`
- **doi**: **10.1101/2024.11.19.624167** (bioRxiv), printed in the footer of every page. Matches
  `refs.bib`. No journal DOI appears anywhere in the document.
- **year**: **2024 by the DOI / original posting; this file is the version posted 6 May 2025**
  (p1 footer). Both dates matter — record both, since the citekey says 2024 and the content is
  2025.
- **venue**: **bioRxiv preprint, not peer reviewed.** p1 footer, verbatim: "The copyright holder
  for this preprint (**which was not certified by peer review**) is the author/funder, who has
  granted bioRxiv a license to display the preprint in perpetuity. It is made available under a
  **CC-BY 4.0 International license**." Tagged `preprint`. No journal is named and no submission
  statement appears.
- **title**: Boltz-1 — Democratizing Biomolecular Interaction Modeling (p1)
- **authors**: Jeremy Wohlwend\*, Gabriele Corso\*, Saro Passaro\*, Noah Getz\* (equal
  contribution), Mateo Reveiz, Ken Leidal, Wojtek Swiderski, Liam Atkinson, Tally Portnoi, Itamar
  Chinn, Jacob Silterra, Tommi Jaakkola, **Regina Barzilay** — p1. Affiliations: MIT CSAIL, MIT
  Jameel Clinic, Genesis Research (part of Genesis Therapeutics), CHARM Therapeutics.
  Correspondence {jwohlwend,gcorso,saro00}@csail.mit.edu.
  **Note a corpus defect, not a paper defect: `refs.bib` omits Regina Barzilay from the author
  list.** She is the last listed author on p1.

## B. Scope

- **system**: **general protein — and beyond protein.** The model is all-atom and multi-modal by
  design: p3, "Boltz-1 operates on proteins represented by their amino acid sequence, ligands
  represented by their smiles strings (and covalent bonds), and nucleic acids represented by
  their genomic sequence." Evaluation sets deliberately span protein monomers, protein–protein
  complexes, protein–ligand complexes, RNA and DNA (p4, p14). **No protein family is singled out
  anywhere; there is no GPCR, kinase or transporter analysis in the paper.**
- **n_targets**: recorded separately because the paper reports four different counts and they are
  routinely conflated when this paper is cited.
  - **Validation set: 553 structures** (p4) — from 1728 date/resolution/cluster-filtered
    candidates → 744 after the four-step iterative refinement → 553 after a ≤1024-residue filter.
  - **Test set as curated and released: 593 structures** (p4).
  - **Test set as actually evaluated: 541 structures** (p15) — after removing covalently bound
    ligands (because "the current version of the Chai-1 public repository does not provide a way
    to set these") and any structure that OOM'd or failed for any method on A100 80GB GPUs.
  - **CASP15 as curated: 76 targets; as actually evaluated: 66** (p15), same removal rule.
  - Training: "all PDB structures released before 2021-09-30 … with a resolution of at least 9Å"
    (p3), count not stated, plus ~270K OpenFold distillation structures (p4).
- **method_class**: **co-folding** (all-atom diffusion co-folding predictor of arbitrary
  biomolecular complexes), **plus an inference-time guidance/resampling method** (Boltz-steering,
  §4) that has no clean slot in the schema's method_class list. Also releases a benchmark split,
  but it is not `benchmark-only`: a model is trained and is the subject.
- **backbones**: **Boltz-1 and Boltz-1x (this work), compared head to head against AlphaFold3
  [Abramson et al., 2024] and Chai-1 [Chai et al., 2024]** (p15). Chai-1 was run locally,
  `chai_lab` package version 0.2.1 (p15); how AlphaFold3 predictions were obtained is **NOT
  REPORTED** — the paper says only that AF3 and Chai-1 "were released under an exclusive
  commercial license and do not have training code and pipelines available" (p15). Four arms
  compared → tagged `multi-backbone`.
- **templates**: **OFF, and deliberately so, for Boltz-1.** p3, verbatim: "**Unlike AlphaFold3,
  we do not include input templates, due to their limited impact on the performance of large
  models.**" This is one of the most citable single sentences in the paper. No evidence for the
  "limited impact" claim is presented anywhere in the document. Whether the AlphaFold3 baseline
  was run with or without templates is **NOT REPORTED**, which makes the head-to-head comparison
  on p15–17 not fully specified.
- **msa_handling**: **full MSA, with a new dense taxonomy-based pairing algorithm; no
  subsampling, no clustering, no state filtering.**
  - Construction (p3): "colabfold search tool [Mirdita et al., 2022] (which leverages MMseqs2),
    using default parameters (versions: uniref30 2302, colabfold envdb 202108)". Taxonomy labels
    from UniProt for all UniRef sequences.
  - Pairing (p5, Algorithm 3 p20): a taxonomy-based pairing algorithm "that preserves MSA density
    (a critical factor, as model complexity scales linearly with the number of MSA rows) while
    balancing the trade-off between the signal derived from paired sequences and the sequence
    redundancy within each chain."
  - Depth at benchmark time (p15): "We also used the same pre-computed MSA's **up to 16384
    sequences**", identical across all four model arms.
  - Depth in the Table 1 ablation (p18 caption): "All models used pre-computed MSAs with **up to
    4,096 sequences**" — different from the headline runs, which the caption itself flags as one
    reason Table 1 and Figures 5/6 do not agree exactly.
  - Distillation MSAs: for the OpenFold distillation set they use "the MSAs they provided" (p4).

## C. Conformational core

**Blanket reason for the NOT APPLICABLE entries below:** this paper predicts one structure per
complex and scores it against one deposited reference. It never defines a conformational state,
never compares two states of the same molecule, and never reports a state-resolved metric. Fields
whose meaning presupposes a conformational-state study are marked NOT APPLICABLE with that reason
restated. Fields that are genuinely answerable for a model paper — training cutoff, held-out
design, confidence semantics, controls — are answered in full, because they are what the corpus
holds this paper for.

- **states_generated**: **one per prediction, by design.** Five diffusion samples are drawn per
  target (p16: "we run all methods to generate 5 samples and evaluate both the best (oracle) and
  highest confidence prediction (top-1) out of the 5 for every metric"), but the five samples are
  **never analysed as distinct conformational states** — they are treated as repeated attempts at
  one answer and collapsed to a single reported structure by oracle or confidence ranking. There
  is no clustering of samples, no inter-sample diversity metric, and no discussion of what the
  five samples differ by. **`ensemble` would be a false reading of the ` + `-dual form:** the
  paper does not claim to sample a landscape, so this is `one`, not "ensemble + single-state".
- **structural_priors_used**: **substantial and fully disclosed. This is the training-data
  composition field and is the second most reusable content in this note after the cutoff.**
  1. **Deposited PDB, pre-cutoff.** p3, verbatim: "For training we use all PDB structures [Berman
     et al., 2000] released before **2021-09-30** (same training cut-off date as AlphaFold3) and
     with a resolution of **at least 9Å**." (On the odd wording of "at least 9Å", see
     `unresolved`.) "We parse the **Biological Assembly 1** from these structures from their
     mmCIF file."
  2. **AlphaFold3's data-cleaning conventions, adopted wholesale.** p3: "we follow the same
     process as AlphaFold3 for data cleaning, which includes the ligand exclusion list, the
     minimum number of resolved residues, and the removal of clashing chains."
  3. **Predicted structures — distillation.** p4, verbatim: "During the first 53k iterations, we
     use a crop size of 384 tokens and 3456 atoms and **draw structures equally from the PDB
     dataset and the OpenFold distillation dataset (approximately 270K structures, using the MSAs
     they provided)** [Ahdritz et al., 2024]. For the last 15k iterations, **we only sampled from
     the PDB structures** and had a crop size of 512 tokens and 4608 atoms." So: 53k of 68k steps
     at a 50/50 PDB : predicted-structure mix, then a 15k-step PDB-only tail. **This is a
     predicted-structure prior on a par with the deposited-structure prior for most of training.**
  4. **No distillation for nucleic acids**, and the paper attributes its own deficit to that —
     p17: AlphaFold3's "slight edge over the other models on the mean LDDT metric … likely derives
     from better handling complexes containing RNA and DNA **thanks to its extra distillation
     datasets**."
  5. **Cheminformatic priors, not structural.** p4: "we pre-compute a single conformer for all CCD
     codes using the RDKit's ETKDGv3"; the steering potentials additionally use "the bounds matrix
     which is generated by the RDKit package" (p14) and CIP priority assignments (p13).
  6. **No templates** (p3) — the one deposited-structure route explicitly closed.
  7. **Training scale**, for the record (p4): "68k steps with a batch size of 128… As a comparison
     AlphaFol3 [sic] trained a similar architecture for nearly 150k steps with a batch size of
     256, which required approximately four times the computing time."

- **oracle_leakage**: **NO conformational-state oracle leakage exists to find, because no
  conformational state is the target.** All seven routes answered separately, with the page where
  the protocol is described so each absence is checkable. Route 4 carries the one real finding.
  1. *Structures used as input or template* — **NONE FOUND.** Templates are switched off by
     design; the input is sequence + SMILES + MSA + an RDKit conformer only. Protocol: p3
     ("Unlike AlphaFold3, we do not include input templates…"), p3–4 (§2.1 input list). Note the
     ligand *conformer* is an RDKit-generated input, not a deposited pose (p4).
  2. *State annotations from a curated database (GPCRdb, KLIFS, Kincore)* — **NONE FOUND, and
     none of these databases is mentioned anywhere in the 24 pages.** Verified by full-text
     search. The only databases used are PDB, CCD, UniProt/UniRef and ColabFold envDB (p3–4).
  3. *Cluster labels derived from known states* — **NONE FOUND.** Clustering appears exactly
     once, and it is sequence-identity clustering for the split, not state clustering: p4,
     "We first cluster the protein sequences in PDB by sequence identity with the command
     `mmseqs easy-cluster ... --min-seq-id 0.4`."
  4. *Hyperparameters, sweep ranges, seeds or stopping criteria tuned against the evaluation set*
     — **PRESENT IN TWO FORMS, neither involving conformational states. Both should be recorded
     as they are the only rigour findings in this paper.**
     (a) **The inference-hyperparameter sweep was run on the test set, not the validation set.**
     Table 1 caption, p18, verbatim: "Ablation on the number of recycling rounds and sampling
     steps for Boltz-1 **on the test set**." Eleven configurations (recycling ∈ {0,1,2,3,6,8,10},
     diffusion steps ∈ {20,50,200}) are evaluated on the same 541-structure set used for the
     headline comparison, and the conclusion drawn — p17, "relatively plateaued beyond 3 recycling
     and 50 diffusion steps" — is a statement about the evaluation set. Per the v3 rule, tuning a
     *range* on the evaluation set is leakage even where no per-target value is chosen. It is mild
     here (the headline runs use 10 recycles / 200 steps, at the generous end, for every method
     equally) but it is the schema's route 4 exactly.
     (b) **The steering potentials are defined against the evaluation criterion.** The "Physical
     Validity" metric is the PoseBusters check set (p16), and the seven Boltz-steering constraint
     potentials (p12–14) are one-to-one against those checks — chirality, bond stereochemistry,
     planarity, RDKit bounds-matrix internal geometry, and inter-chain clash. The numeric
     constants nearly coincide: the steering clash potential penalises distances below **0.725**×
     the VdW radius sum (p14) while the PoseBusters clash check passes above **0.75**× the VdW
     radius sum (p16). **Boltz-1x is therefore optimised at inference time against the metric it
     is then scored on**, and its 97% physical-validity result must be read in that light. The
     paper does not flag this. It is not deposited-structure leakage; it is metric-targeted
     design, and should be labelled as such rather than conflated with an oracle leak.
  5. *Success defined post hoc by RMSD or TM to a structure they had* — **NONE FOUND in the leaky
     sense.** Every metric is defined a priori against the deposited reference and applied
     uniformly to all four model arms with published thresholds (p15–16: DockQ > 0.23; ligand
     pocket-aligned RMSD < 2Å; OpenStructure 2.8.0). The TM-scores of 0.95 quoted in Fig 1 (p1)
     are for two hand-picked showcase targets — "two examples of hard targets from the test set
     where Boltz-1 performed remarkably well" (p17) — which is cherry-picking for illustration,
     not post hoc metric definition. Record it as such.
  6. *Best/worst model labels assigned against a held reference* — **PRESENT AND EXPLICIT, but
     correctly labelled by the paper and applied symmetrically to all arms.** This is the "oracle"
     arm: p16, "we run all methods to generate 5 samples and evaluate both the **best (oracle)**
     and highest confidence prediction (top-1) out of the 5 for every metric." Selecting the best
     of 5 against the ground truth is reference-informed selection by construction; the paper is
     transparent about it, reports top-1 alongside every oracle number, and applies the same rule
     to AF3, Chai-1, Boltz-1 and Boltz-1x. **The oracle–top-1 gap is the paper's only measurement
     of how much its confidence model is worth** (see `confidence_as_discriminator`).
  7. *Design-level oracle — inputs or systems chosen because the expected answer is known* —
     **NONE FOUND at the level that matters.** Targets are date-and-cluster-filtered en bloc, not
     chosen individually (p4). The one design-level judgement call is negative rather than
     favourable: structures were removed from evaluation because a *baseline* could not handle
     them — p15, "we remove structures with covalently bounded ligands because the current version
     of the Chai-1 public repository does not provide a way to set these" and "we remove
     structures that go out of memory or fail for other reasons **for any of the methods**". This
     removes 52 of 593 test structures and 10 of 76 CASP15 targets; whether the removed structures
     were systematically harder is **NOT REPORTED**.

- **prospective**: **no.** The test set is *post-training-cutoff* but wholly *retrospective*: all
  targets were already deposited in the PDB when the evaluation was run (structures "released
  after 2023-01-13", p4), and CASP15 (2022) was complete before the model existed. No prediction
  was registered before the answer was available to the authors. The date discipline is real and
  is recorded under `anti_memorization_design`; it is temporal holdout, not prospectivity, and the
  two must not be collapsed.

- **state_metric**: **NOT APPLICABLE — no conformational state is scored, so there is no state
  metric of any kind (binary, continuous, RMSD-to-reference or visual).** The paper's metrics are
  accuracy-to-a-single-reference metrics. Recorded here for completeness because the corpus will
  want their exact definitions and thresholds (all p15–16):
  - **Mean all-atom LDDT** — "measuring accuracy of local structures across all biomolecules";
    continuous, unthresholded.
  - **DockQ success rate** — "the proportion of predictions with **DockQ > 0.23**, which measures
    the number of good protein-protein interactions predicted." Threshold stated; **its
    justification is not** — 0.23 is the standard CAPRI "acceptable" floor but the paper never
    says so or cites it.
  - **Mean LDDT-PLI** — "measuring the quality of the ligand and pocket predicted interactions,
    official CASP15 metric to evaluate the ligand category"; continuous.
  - **Ligand pocket-aligned RMSD success rate** — "the proportion of ligands with a pocket-aligned
    **RMSD below 2Å**: a widely adopted measure of molecular docking accuracy." Threshold stated,
    justification asserted rather than cited.
  - **Physical Validity** — the proportion of poses passing **all six** PoseBusters checks
    [Buttenschoen et al., 2024] listed a–f at p16: ligand bond strain, ligand angle strain, ligand
    internal clash (all against RDKit ranges), tetrahedral chirality preserved, bond
    stereochemistry preserved, and inter-chain clash (distances "greater than **0.75** times the
    sum of their Van der Waals radii"). A conjunctive pass/fail predicate.
  - Aggregation, p16: "LDDT-PLI, DockQ and ligand RMSD success rates are computed over all the
    different protein-protein and protein-ligand interfaces, these proportions are averaged over
    interfaces within individual complexes and then averaged across complexes containing
    interfaces." All computed with **OpenStructure version 2.8.0** [Biasini et al., 2013].

- **metric_saturation**: **YES, in one arm, numerically. Physical Validity ceilings for Boltz-1x.**
  Test set, p17: "**Boltz-1x gets 97% of the poses passing the checks**" — a bounded [0,1]
  proportion 3 points from its ceiling, leaving almost no headroom to distinguish Boltz-1x from
  any future method on this metric. On CASP15 (Fig 6, p16) the Boltz-1x physical-validity bars sit
  at ~0.92 with the **upper 95% bootstrap CI reaching 1.0**, i.e. the estimate is
  ceiling-censored at n=66. No other metric saturates: mean LDDT tops out around 0.83 (test) and
  0.43 (CASP15), and the two success-rate metrics sit near 0.6–0.7 (test). *Figure-level
  criticisms of Figures 5 and 6 are recorded in the `hides` column of Section F, not here.*

- **directional_control**: **NOT APPLICABLE for conformational state — the model cannot be
  instructed which conformation to produce, and the paper never claims it can.** Two genuine
  input-side handles exist, both about *what* is predicted rather than *which state*:
  1. **Pocket conditioning** (§2.5 p5, Algorithm 5 p22) — the user names binding-site residues and
     a binder chain. Designed for partial specification: "designed to (1) retain a single unified
     model, (2) ensure robustness to a partial specification of interacting residues, and (3)
     enable interaction site specification for polymer binders such as proteins or nucleic acids."
     Training: "we incorporate pocket information for a randomly selected binder in **30%** of
     iterations… we draw the (maximum) number of pocket residues to reveal from a **geometric
     distribution** (p = 0.3, Algorithm 5) and randomly select residues from those with at least
     one heavy atom within **6Å** of the binder", encoded as a one-hot token feature with values
     BINDER / POCKET / UNSELECTED / UNSPECIFIED.
  2. **Co-folded partners and ligands** — a ligand, nucleic acid or partner chain is an input, so
     the prediction is conditioned on it by construction (p3). **No experiment in this paper
     varies the partner or ligand and measures the structural response**, so this is a capability
     of the architecture, not a demonstrated handle.
  3. **Boltz-steering itself is a directional handle over *physical validity*, not over
     conformation** — it drives samples toward a low-energy region defined by seven physics
     potentials (p12–14). Nothing in the potential set encodes a target conformation.
  - **Seeds**: seed handling is **NOT REPORTED** anywhere; the five samples per target are drawn
    from the diffusion process but the paper never states how randomness is controlled or whether
    seeds are fixed.

- **anti_memorization_design**: **PRESENT, dated, and the reason this note exists. Quoted in full
  with pages.**

  **The training cutoff, verbatim, p3:**
  > "For training we use all PDB structures [Berman et al., 2000] released before **2021-09-30**
  > (same training cut-off date as AlphaFold3) and with a resolution of at least 9Å."

  **The split procedure, p4, verbatim and in order.** Preamble:
  > "To address the absence of a standardized benchmark for all-atom structures, we are releasing
  > a new PDB split designed to help the community converge on reliable and consistent benchmarks
  > for all-atom structure prediction tasks. Our training, validation and test splitting strategy
  > largely follows Abramson et al. [2024]. We first cluster the protein sequences in PDB by
  > sequence identity with the command `mmseqs easy-cluster ... --min-seq-id 0.4` [Hauser et al.,
  > 2016]."

  **VALIDATION SET — four inclusion filters, then a four-step iterative refinement, then a size
  filter. All p4.**
  Filters (all four must hold):
  > "1. Initial release date is before **2021-09-30 (exclusive)** and **2023-01-13 (inclusive)**.
  > 2. Resolution is below **4.5Å**.
  > 3. All the protein sequences of the chains are **not present in any training set clusters**
  > (i.e. before 2021-09-30).
  > 4. Either no small-molecule is present, or at least one of the small-molecules exhibits a
  > **Tanimoto similarity of 0.8 or less** to any small-molecule in the training set. Here, a
  > small-molecule is defined as any non-polymer entity containing more than one heavy atom and
  > not included in the ligand exclusion list."

  This yields **1728 structures**, refined by:
  > "1. Retaining all the structures containing RNA or DNA entities. (**126 structures**)
  > 2. Iteratively adding structures containing small-molecules or ions under the condition that
  > all their protein chains belong to new unseen clusters (**330 additional structures**)
  > 3. Iteratively adding multimeric structures under the condition that all the protein chains
  > belong to new unseen clusters. These are further filtered by **randomly keeping only 50%** of
  > the passing structures. (**231 additional structures**)
  > 4. Iteratively adding monomers under the condition that their chain belongs to a new unseen
  > cluster. These are further randomly filtered out by **keeping only 30%** of the passing
  > structures. (**57 additional structures**)"

  > "This results in a total of **744 structures**. Finally, we retain the structures with **at
  > most 1024 residues** in the valid protein/RNA/DNA chains, finishing with a total of **553
  > validation set structures**."

  **TEST SET — same procedure, three stated differences. p4, verbatim:**
  > "The test set is created using the same procedure described above with the following
  > differences: for protein and ligand similarity exclusion we consider **all structures released
  > before 2023-01-13 (which include all training and validation sets)**, we filter to structures
  > **released after 2023-01-13** and the final size filter to structures **between 100 and 2000
  > total residues**. The resulting final test set size is **593**."

  **Reading of the above, stated plainly because this is what the corpus will be asked:** the test
  set is held out on **three independent axes at once** — (i) **date**, released after 2023-01-13,
  i.e. ~15.5 months after the 2021-09-30 training cutoff; (ii) **protein sequence**, every protein
  chain must fall in an MMseqs2 40%-identity cluster containing nothing released before
  2023-01-13; (iii) **ligand chemistry**, at least one small molecule must have Tanimoto ≤ 0.8 to
  every training small molecule. The composition is deliberately reweighted toward the hard
  classes: all nucleic-acid structures kept, all qualifying ligand structures kept, multimers
  subsampled to 50% and monomers to 30%. **This is a stronger anti-memorization design than a
  date cutoff alone**, and stronger than most papers in this corpus; it is also the split other
  Boltz-family papers inherit.
  **What it does not do:** it never separates *alternative conformational states of the same
  protein* across the split — a protein whose other state is in training is excluded entirely by
  the 40%-identity cluster rule rather than retained as a state-generalisation test. Nothing in
  the design targets conformational novelty, only sequence and chemistry novelty.
  **CASP15**, the second benchmark, is a natural post-cutoff set (2022 competition, p14) but its
  targets fall inside the *validation* date window (2021-09-30 → 2023-01-13); the paper never says
  whether any CASP15 target is also in the 553-structure validation set used for model selection.
  See `unresolved`.

- **anti_memorization_control**: **NONE RUN as a control *arm*, though the held-out set is real
  and well powered (n=541).** The distinction the schema exists to preserve applies squarely
  here: every headline number in this paper is computed on post-cutoff, cluster-excluded data, so
  the whole evaluation sits inside the anti-memorization design — but **no arm contrasts memorised
  against novel targets**. Specifically, the paper reports:
  - no pre-cutoff vs post-cutoff comparison,
  - no stratification of the test set by sequence identity to training, by cluster size, or by
    ligand Tanimoto to training,
  - no per-target or per-class breakdown of any metric (results are pooled across all 541
    structures and all 66 CASP15 targets),
  - no held-out set of *conformationally* novel targets.
  Not `UNPOWERED`: n = 541 test and 66 CASP15, both far above the ~10 threshold, with 95%
  bootstrap CIs reported on every bar (Figs 5–6). The CASP15 CIs are nonetheless very wide (see
  Section F `hides`).

- **controls_run**: every arm the paper actually ran. Ablations of the *architecture* changes were
  **not** run at full scale and the paper says so (p6, quoted in `stated_limits`).

  | control | what it rules out | page |
  |---|---|---|
  | Recycling-round sweep: 0, 1, 2, 3, 6, 8, 10 rounds at 200 diffusion steps, oracle and top-1, 4 metrics | That the reported accuracy depends on recycling depth; shows monotonic-ish gain to ~3 then plateau (0 → 3 recycles moves mean LDDT top-1 0.681 → 0.716) | Table 1, p18; text p17 |
  | Diffusion-step sweep: 20, 50, 200 steps at 3 recycles | That accuracy depends on sampling budget beyond ~50 steps; 20 → 50 → 200 moves mean LDDT top-1 0.693 → 0.710 → 0.716 | Table 1, p18; text p17 |
  | Oracle (best of 5 vs ground truth) reported alongside top-1 (confidence-ranked) for every metric and every model | Isolates how much of the reported accuracy is delivered by the confidence model rather than by the generator; the only quantification of confidence-model value in the paper | p16, Figs 5–6, Table 1 |
  | Boltz-1 vs Boltz-1x — same generator, steering on/off | Isolates the effect of Boltz-steering on both physical validity (0.43 → 0.97 top-1, test) and geometric accuracy (unchanged within CI), i.e. rules out that the physics gain is bought with accuracy | p17, Figs 5–6 |
  | Identical pre-computed MSAs (≤16384 sequences) supplied to all four model arms | Rules out MSA construction as the source of cross-model differences | p15 |
  | Identical sampling budget for all arms: 200 sampling steps, 10 recycling rounds, 5 outputs | Rules out inference budget as the source of cross-model differences | p15 |
  | Chai-1 sequence-source labelling variants (uniref90 / bfd_uniclust) | Rules out that the Chai-1 baseline was crippled by mis-annotated MSA provenance — but the check is informal: "We briefly experimented with alternative labelings but did not find these to impact the model substantially", with no numbers | p15 |
  | Two benchmarks with different construction (own post-2023-01-13 PDB split; CASP15 community targets) | Rules out that the result is an artefact of the authors' own split | p14–15 |
  | 95% bootstrap confidence intervals on every bar in Figs 5 and 6 | Quantifies sampling error; the basis for the paper's repeated "within the confidence intervals" claims | Figs 5–6, p15–16 |
  | — **NOT run**: full-scale ablation of the architectural changes (MSA-module reordering, transformer residual order, Kabsch interpolation, EDM loss weighting, confidence-model redesign, unified cropping, dense MSA pairing, pocket conditioning) — | Nothing. Each change is adopted on small-scale evidence that is not shown | p6, admitted |
  | — **NOT run**: decoys, shuffled/scrambled inputs, apo arms, per-class or per-difficulty stratification, sensitivity to seed | Nothing | — |

- **confidence_as_discriminator**: **The confidence model is used for model *ranking* (top-1
  selection among 5 samples), never for conformational discrimination — the latter is NOT
  APPLICABLE here. What it is trained to predict is stated precisely and is recorded in full,
  because that is what the corpus needs.**
  - **What the heads predict.** p8, describing the AlphaFold3 design Boltz-1 inherits: the
    confidence layers "are followed by linear projections trained to predict **whether each atom
    is resolved in the crystal structure, per-atom LDDT and per-token pair PAE and PDE**."
    Algorithm 1 (p9) makes the four outputs explicit: `plddt`, `pde`, `resolved`, `pae`, each a
    softmax over bins — pLDDT and `resolved` from the single representation, PDE from the
    symmetrised pair representation (`z + zᵀ`), PAE from the pair representation.
  - **What they therefore measure, on the paper's own account:** agreement with the **deposited
    crystal structure** — local distance accuracy (LDDT), pairwise alignment error (PAE/PDE) and
    experimental resolvedness. **The paper makes no claim that confidence measures physical
    plausibility, thermodynamic stability, or that a state is correct**; indeed Boltz-steering
    exists precisely because high-scoring poses can be physically invalid (p11: hallucinated
    overlapping chains, steric clashes, wrong chirality, non-planar aromatics — "these issues are
    not strongly penalized in geometric measures of accuracy of the poses"). **That sentence is
    the paper's own statement that its accuracy metrics, and by extension its confidence model,
    do not see physical validity.**
  - **What is architecturally new here** (§3.3, p7–9), and the reason this paper is worth citing
    on confidence at all — three changes from AlphaFold3:
    1. **Separate training.** "AlphaFold3 trains the confidence model alongside the trunk and
       denoising models while, however, cutting all the gradients going from the confidence task
       to the rest of the model. Instead, training structure prediction and confidence models
       separately allowed us to disentangle experiments on each component" (p7–8).
    2. **The confidence model is a fine-tuned copy of the trunk, not four PairFormer layers.**
       p8: "inspired by the way that researchers in the large language model community have been
       training reward models by fine-tuning the 'trunk' of their pretrained generative models
       [Touvron et al., 2023], we define the architecture of our confidence model to contain all
       the components of the trunk and initialize its representation to the trained trunk weights.
       Hence, our confidence model presents an AtomAttentionEncoder, an MSAModule, and a
       **PairFormerModule with 48 layers**." Initialised from the trunk EMA weights, with all
       other components randomly initialised but with **zeroed final layers** (p8). **The paper
       frames confidence explicitly as a reward model.**
    3. **It sees the diffusion trajectory, not just the final pose.** p8: "We feed to the
       confidence model not only the representations coming from the trunk but also a learned
       aggregation of the final token representation at each reverse diffusion step… aggregated
       through the reverse diffusion trajectory with a time-conditioned recurrent block."
  - **Validation of the confidence model: only indirect, via the oracle–top-1 gap.** No
    calibration curve, no reliability diagram, no correlation of pLDDT against true LDDT appears
    anywhere in the paper. The gap on the test set (Table 1, p18, 3 recycles / 200 steps) is:
    mean LDDT 0.729 oracle vs 0.716 top-1; DockQ>0.23 0.654 vs 0.625; LDDT-PLI 0.621 vs 0.580;
    L-RMSD<2Å 0.581 vs 0.545. **A perfect ranker would close these gaps; the confidence model
    recovers most but not all of the oracle's advantage.** No tag `confidence-as-discriminator`
    is applied, because that tag is about judging *conformational* correctness — see
    `unresolved`.

## D. Claims

- **central_conclusion**: Boltz-1 reproduces and modestly extends the AlphaFold3 recipe as a fully
  open-source, MIT-licensed all-atom co-folding model, and reaches accuracy statistically
  indistinguishable from AlphaFold3 and Chai-1 on a post-cutoff 541-structure PDB test set and on
  66 CASP15 targets, at roughly a quarter of AlphaFold3's reported training compute. Separately,
  the physical validity of diffusion-model outputs is a distinct failure mode that geometric
  accuracy metrics do not capture, and it can be fixed almost entirely at inference time —
  Boltz-steering, a Feynman-Kac / Sequential-Monte-Carlo resampling scheme with flat-bottomed
  physics potentials plus gradient guidance, raises the PoseBusters pass rate from 43% to 97% on
  the test set without measurable loss of geometric accuracy; the steered model is named Boltz-1x.

- **necessity_claims**: **Verbatim + page.** This paper is an engineering report and makes few
  necessity claims; those it makes are about tractability and about the inadequacy of
  filtering, not about biology.

  **N1 — Filtering/importance sampling cannot reach rare constraint-satisfying conformers. This is
  the load-bearing justification for Boltz-steering over AlphaFold3's post-hoc filtering.** p11:
  > "To sample from this tilted distribution, one approach would be to sample k particles from our
  > diffusion process … and subsequently resample them based on their corresponding importance
  > weights … This approach would function similarly to the approach employed by Abramson et al.
  > [2024] in AlphaFold3 where multiple samples of the diffusion model are then filtered based on
  > physical-realism heuristics. However, as noted by Singhal et al. [2025], this approach has
  > drawbacks. **First, for constraints that are rarely satisfied by the model, importance sampling
  > or filtering will be unable to bias the model towards the rare conformer that satisfies the
  > constraint.**"

  **N2 — Physical invalidity blocks downstream use, and accuracy metrics do not see it.** p11:
  > "**While these issues are not strongly penalized in geometric measures of accuracy of the
  > poses, they can prevent the predictions from being used in many downstream applications**,
  > both for expert and computational analyses (e.g. running molecular dynamics calculations)."

  **N3 — The AlphaFold3 aligned-MSE training objective is theoretically unsound on its own.** p7:
  > "However, **we argue that on its own this procedure is theoretically problematic.** One can
  > define simple functions that would achieve zero rigid aligned MSE loss during training, but
  > completely fail to sample realistic poses at inference time."
  and, p7:
  > "This model will have a loss approaching zero during training … However, when used at inference
  > time, **this model will consistently go out of distribution** (and therefore predict a zero
  > vector)."

  **N4 — Impossibility/tractability claims.** p10:
  > "Because the number of possible perturbations grows exponentially with the size of the complex,
  > **considering all of them is computationally unfeasible.**"
  p12:
  > "**Directly sampling from the tilted transition kernel is intractable**, therefore, the FK
  > steering framework uses Sequential Monte Carlo (SMC) to propose multiple particles at each
  > timeste,p [sic] which are then resampled based on their importance weights."
  p6:
  > "This trunk is computationally expensive due to its use of token pairs as fundamental
  > 'computational token' and its axial attention operations on these pair representations which
  > results in a complexity that scales cubically with the number of input tokens. **To make such
  > encoding computationally tractable, the trunk is set to be independent of the specific
  > diffusion time or input structure** such that it can be run only once per complex."

  **N5 — A requirement on the evaluation procedure.** p10:
  > "During validation and confidence model training, **the optimal alignment between the ground
  > truth and predicted structure must be determined**, accounting for permutations in the order
  > of identical chains or symmetric atoms within those chains."

  **N6 — Templates are dispensable. Stated as a design decision with no supporting evidence, but
  it is a claim about what is *not* needed and will be quoted as one.** p3:
  > "**Unlike AlphaFold3, we do not include input templates, due to their limited impact on the
  > performance of large models.**"

- **novelty_claims**: **Verbatim + page.**

  **V1 — Priority claim, made twice in identical form.** p2 (§1 Overview):
  > "In this manuscript, we present Boltz-1, **the first fully commercially accessible open-source
  > model reaching AlphaFold3 reported levels of accuracy.**"
  p18 (§6 Conclusion):
  > "We introduced Boltz-1, **the first fully commercially accessible open-source model to achieve
  > AlphaFold3-level accuracy** in predicting the 3D structures of biomolecular complexes."
  **Note the careful hedging in the first form — "AlphaFold3 *reported* levels of accuracy" — and
  the qualifier "fully commercially accessible open-source", which is what makes the priority
  claim survivable given Chai-1's prior release under a non-commercial licence.**

  **V2 — Abstract-level novelty, p1:**
  > "In this paper, we introduce Boltz-1, an open-source deep learning model incorporating
  > innovations in model architecture, speed optimization, and data processing **achieving
  > AlphaFold3-level accuracy** in predicting the 3D structures of biomolecular complexes. Boltz-1
  > demonstrates a performance on-par with state-of-the-art commercial models on a range of diverse
  > benchmarks, **setting a new benchmark for commercially accessible tools in structural
  > biology**. Further, **we push the boundary of capabilities of these models with Boltz-steering,
  > a new inference time steering technique that is able to fix hallucinations and non-physical
  > predictions from the models.**"

  **V3 — Boltz-steering as a new technique, p11:**
  > "To tackle these issues, **we introduce a new inference time steering technique that we refer
  > to as Boltz-steering.**"
  and its differentiation from prior inference-time potentials, p11:
  > "**By contrast, we use a flat-bottom potential based on the distance bounds, to enforce that
  > the potential is within the range of realistic conformers without forcing it to match the
  > RDKit conformer, expand to other physical properties and not only use gradient updates but
  > also resampling.**"

  **V4 — The released split as a new community artefact, p4:**
  > "To address the absence of a standardized benchmark for all-atom structures, **we are releasing
  > a new PDB split** designed to help the community converge on reliable and consistent benchmarks
  > for all-atom structure prediction tasks."

  **V5 — Component-level novelty claims, p3 (the three-item list), p5 and p5:**
  > "it also presents several innovations which include: 1. **New algorithms** to more efficiently
  > and robustly pair MSAs, crop structure at training time, and condition predictions on
  > user-defined binding pockets; 2. Changes to the flow of the representations in the architecture
  > and the diffusion training and inference procedures; 3. Revision of the confidence model both
  > in terms of architectural components as well as the framing of the task as a fine-tuning of the
  > model's trunk layers."
  p5: "To this end, **we define a new cropping algorithm** which directly interpolates between
  spatial and contiguous strategies."
  p11: "**We implement a Triton kernel** that performs the calculation via a chunked online
  softmax… **This is an extension of FlashAttention that allows for the inner bias term.**"

  **V6 — Boltz-1x, p18:**
  > "Further, **we introduced Boltz-1x** an updated model that leverages Boltz-steering, a new
  > inference time technique, to significantly improve the physical quality of the poses generated
  > while maintaining their geometric accuracy of Boltz-1."

- **stated_limits**: unusually candid for a model paper on two points, silent on others.
  - **No full-scale ablations exist for any architectural change. Verbatim, p6:**
    > "Because of the significant computational budget required to train a full-sized model, we
    > tested these changes on a smaller-sized architecture at different points of our development
    > process. **We expect our observations to hold for the final full-size model, but cannot
    > present direct ablation studies.**"
    The small-scale results themselves are **not shown anywhere**, so every architectural claim in
    §3.1–3.2 is unevidenced in this document.
  - **The reported metrics are noisy and the ablation should not be over-read. Table 1 caption,
    p18, verbatim:**
    > "**It is worth noting that the metrics are noisy, so minor inconsistencies (e.g., lack of
    > improvement with increased recycling rounds or diffusion steps) should not be
    > overinterpreted.** Moreover, there is a slight difference with the results in Figures 5 and 7
    > due to differences in MSA parameters as well as the set of structures passing all ablations."
  - **One of its own innovations is conceded to be near-inert at full scale.** p7, on the Kabsch
    diffusion interpolation:
    > "Empirically, we note that this change to the reverse diffusion has a bigger effect when
    > training models on subsets of the full data where the model is more likely to overfit, on the
    > other hand, **the final Boltz-1 seems to largely denoising [sic] close to the projection
    > making the Kapsch alignment not critical.**"
  - **Its architecture may partly be an artefact of errors in the AlphaFold3 report.** Footnote 2,
    p6: "**Some of these differences may simply be the result of reporting mistakes in the current
    version of the original manuscript from Abramson et al. [2024]**, as reported ." (the sentence
    is truncated in the PDF — the citation is missing).
  - **Concession on nucleic acids.** p17: AlphaFold3's edge on mean LDDT "likely derives from
    better handling complexes containing RNA and DNA thanks to its extra distillation datasets."
  - **The document is explicitly a moving target.** p3: "Given the dynamic nature of this
    open-source project, **this manuscript and its linked GitHub repository will be regularly
    updated** with improvements from our core team and the community."
  - **Symmetry correction is approximate, with stated caps.** p10: "an **approximate**, yet
    effective, atom matching… In practice, we limit the number of perturbations of the chain
    assignment we consider to 100 and the perturbations of the atoms of each ligand to 1000."
  - **Limits NOT stated anywhere, and worth recording as absences:** no statement that the model
    predicts a single conformation and cannot be asked for another; no discussion of what the 5
    samples represent; no discussion of memorization or of what the post-cutoff test set does and
    does not control for; no statement of the steering hyperparameter values (λ, the seven α
    weights, t_clash, the number of particles k, or the number of gradient steps m are all left
    unspecified in the text); no runtime or cost comparison against the baselines; **no limitations
    section of any kind.**

- **stance**: **`background` + `precedent`. Provisional — the user's call.**
  - **`background`, primarily.** This is the origin document for a backbone the corpus and the
    manuscript both use, and the definitional source for Boltz-1x. It reports no conformational
    result that can support or contradict a state-prediction claim.
  - **`precedent` on the split design.** The three-axis held-out construction (date + 40%-identity
    protein cluster exclusion + Tanimoto ≤ 0.8 ligand exclusion), quoted in full above, is a
    concrete, citable standard our own held-out design can be measured against or built on, and it
    is stricter than a date cutoff alone.
  - **Not `contrast`, not `threat`**: the paper makes no claim about conformational states, so it
    cannot conflict with a conformational finding. The only rigour findings against it (route 4a
    test-set sweep, route 4b metric-targeted steering) are ordinary engineering-paper defects, not
    a challenge to anyone's result.

## E. Quantitative comparators

**Value provenance convention, because it matters here.** The headline four-way comparison exists
**only as bar charts** (Figs 5–6); the paper prints no numeric table for it. Values below are
tagged:
- **[text]** = stated numerically in the running text (exact).
- **[Table 1]** = from Table 1, p18 (exact, but Boltz-1 only, and run at MSA depth ≤4,096 rather
  than the ≤16,384 used for Figs 5–6 — the caption warns the two "differ slightly").
- **[fig ~]** = **read off the rendered bar chart by the extractor; approximate to about ±0.01**,
  because no data labels are printed. Do not quote these to three decimals in the manuscript;
  quote them as approximate or fetch the released evaluation files from the GitHub repo (p16).

- **metrics_reported**:

  **PDB test set (n = 541 evaluated; Fig 5, p15). Values are "oracle / top-1" of 5 samples.**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Mean all-atom LDDT — AlphaFold3 | ~0.83 / ~0.82 [fig ~] | LDDT (0–1) | deposited reference, OpenStructure 2.8.0 | p15 |
  | Mean all-atom LDDT — Chai-1 | ~0.81 / ~0.79 [fig ~] | LDDT | as above | p15 |
  | Mean all-atom LDDT — Boltz-1 | ~0.80 / ~0.79 [fig ~] | LDDT | as above | p15 |
  | Mean all-atom LDDT — Boltz-1x | ~0.81 / ~0.80 [fig ~] | LDDT | as above | p15 |
  | DockQ > 0.23 success rate — AlphaFold3 | ~0.72 / ~0.70 [fig ~] | proportion of interfaces | protein–protein interfaces vs reference | p15 |
  | DockQ > 0.23 success rate — Chai-1 | ~0.71 / ~0.69 [fig ~] | proportion | as above | p15 |
  | DockQ > 0.23 success rate — Boltz-1 | ~0.71 / ~0.69 [fig ~] | proportion | as above | p15 |
  | DockQ > 0.23 success rate — Boltz-1x | ~0.69 / ~0.68 [fig ~] | proportion | as above | p15 |
  | Mean LDDT-PLI — AlphaFold3 | ~0.645 / ~0.605 [fig ~] | LDDT-PLI | protein–ligand interfaces vs reference | p15 |
  | Mean LDDT-PLI — Chai-1 | ~0.60 / ~0.578 [fig ~] | LDDT-PLI | as above | p15 |
  | Mean LDDT-PLI — Boltz-1 | ~0.625 / ~0.60 [fig ~] | LDDT-PLI | as above | p15 |
  | Mean LDDT-PLI — Boltz-1x | ~0.64 / ~0.60 [fig ~] | LDDT-PLI | as above | p15 |
  | Ligand pocket-aligned RMSD < 2Å — AlphaFold3 | ~0.60 / ~0.565 [fig ~] | proportion of ligands | pocket-aligned RMSD to reference ligand | p15 |
  | Ligand pocket-aligned RMSD < 2Å — Chai-1 | ~0.565 / ~0.542 [fig ~] | proportion | as above | p15 |
  | Ligand pocket-aligned RMSD < 2Å — Boltz-1 | ~0.595 / ~0.57 [fig ~] | proportion | as above | p15 |
  | Ligand pocket-aligned RMSD < 2Å — Boltz-1x | ~0.595 / ~0.555 [fig ~] | proportion | as above | p15 |
  | **Physical Validity (all 6 PoseBusters checks) — AlphaFold3** | ~0.715 / **0.58** [text] | proportion of complexes | PoseBusters rule set, no reference structure needed | p17 |
  | **Physical Validity — Chai-1** | ~0.34 / **0.27** [text] | proportion | as above | p17 |
  | **Physical Validity — Boltz-1** | ~0.47 / **0.43** [text, stated as "57% of top-1 poses do not pass"] | proportion | as above | p17 |
  | **Physical Validity — Boltz-1x** | ~0.978 / **0.97** [text] | proportion | as above | p17 |

  **CASP15 (n = 66 evaluated; Fig 6, p16). Values are "oracle / top-1". All [fig ~]; the paper
  states no CASP15 number in text. Confidence intervals here are very wide — see Section F.**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Mean all-atom LDDT — AlphaFold3 | ~0.43 / ~0.42 | LDDT | CASP15 reference structures | p16 |
  | Mean all-atom LDDT — Chai-1 | ~0.41 / ~0.40 | LDDT | as above | p16 |
  | Mean all-atom LDDT — Boltz-1 | ~0.38 / ~0.36 | LDDT | as above | p16 |
  | Mean all-atom LDDT — Boltz-1x | ~0.41 / ~0.39 | LDDT | as above | p16 |
  | DockQ > 0.23 — AlphaFold3 | ~0.60 / ~0.60 | proportion | as above | p16 |
  | DockQ > 0.23 — Chai-1 | ~0.50 / ~0.50 | proportion | as above | p16 |
  | DockQ > 0.23 — Boltz-1 | ~0.70 / ~0.70 | proportion | as above | p16 |
  | DockQ > 0.23 — Boltz-1x | ~0.70 / ~0.70 | proportion | as above | p16 |
  | Mean LDDT-PLI — AlphaFold3 | ~0.47 / ~0.40 | LDDT-PLI | as above | p16 |
  | Mean LDDT-PLI — Chai-1 | ~0.31 / ~0.27 | LDDT-PLI | as above | p16 |
  | Mean LDDT-PLI — Boltz-1 | ~0.49 / ~0.46 | LDDT-PLI | as above | p16 |
  | Mean LDDT-PLI — Boltz-1x | ~0.46 / ~0.445 | LDDT-PLI | as above | p16 |
  | Ligand RMSD < 2Å — AlphaFold3 | ~0.475 / ~0.38 | proportion | as above | p16 |
  | Ligand RMSD < 2Å — Chai-1 | ~0.16 / ~0.145 | proportion | as above | p16 |
  | Ligand RMSD < 2Å — Boltz-1 | ~0.425 / ~0.24 | proportion | as above | p16 |
  | Ligand RMSD < 2Å — Boltz-1x | ~0.325 / ~0.31 | proportion | as above | p16 |
  | Physical Validity — AlphaFold3 | ~0.72 / ~0.64 | proportion | PoseBusters rule set | p16 |
  | Physical Validity — Chai-1 | ~0.555 / ~0.50 | proportion | as above | p16 |
  | Physical Validity — Boltz-1 | ~0.47 / ~0.47 | proportion | as above | p16 |
  | Physical Validity — Boltz-1x | ~0.915 / ~0.915 (upper CI touches 1.0) | proportion | as above | p16 |

  **Table 1 (p18) — exact values, Boltz-1 only, PDB test set, 5 samples, MSA ≤4,096. Reproduced
  because it is the only exact numeric table in the paper and it is the source for the sampling
  defaults.**

  | # rec. | # steps | LDDT oracle | LDDT top-1 | DockQ>0.23 oracle | top-1 | LDDT-PLI oracle | top-1 | L-RMSD<2Å oracle | top-1 |
  |---|---|---|---|---|---|---|---|---|---|
  | 3 | 200 | 0.729 | 0.716 | 0.654 | 0.625 | 0.621 | 0.580 | 0.581 | 0.545 |
  | 0 | 200 | 0.698 | 0.681 | 0.579 | 0.544 | 0.573 | 0.530 | 0.582 | 0.541 |
  | 1 | 200 | 0.718 | 0.702 | 0.656 | 0.635 | 0.623 | 0.573 | 0.588 | 0.535 |
  | 2 | 200 | 0.726 | 0.710 | 0.651 | 0.632 | 0.616 | 0.581 | 0.587 | 0.546 |
  | 6 | 200 | 0.732 | 0.714 | 0.644 | 0.635 | 0.630 | 0.593 | 0.595 | 0.555 |
  | 8 | 200 | 0.733 | 0.717 | 0.644 | 0.633 | 0.630 | 0.584 | 0.588 | 0.545 |
  | 10 | 200 | 0.735 | 0.720 | 0.644 | 0.631 | 0.619 | 0.577 | 0.575 | 0.541 |
  | 3 | 20 | 0.720 | 0.693 | 0.615 | 0.592 | 0.577 | 0.547 | 0.550 | 0.532 |
  | 3 | 50 | 0.727 | 0.710 | 0.645 | 0.627 | 0.621 | 0.579 | 0.586 | 0.540 |

  **Non-accuracy numbers, with pages:**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Boltz-1 training length | 68,000 steps, batch size 128 | steps | own training run | p4 |
  | AlphaFold3 training length, as cited by this paper | ~150,000 steps, batch size 256, "approximately four times the computing time" | steps | Abramson et al. 2024 | p4 |
  | OpenFold distillation set size | ~270,000 | predicted structures | Ahdritz et al. 2024 | p4 |
  | Showcase TM-score, PDB 8SVA and 8IG1 | 0.95 each ("around 95%") | TM-score | deposited reference; 2 hand-picked test-set targets | p1, p17 |
  | Trifast Triangle-Attention forward runtime at n≈2000 | ~220 (Trifast) vs ~450 (DeepSpeed) | ms, RTX 3090, float32 | own kernel benchmark; compiled PyTorch OOM/stops at n≈780 | Fig 4, p10 |

- **n_predictions**: recorded separately as the schema requires.
  - **Samples per target: 5** for every model arm, on both benchmarks (p15: "producing 5 outputs";
    p16: "we run all methods to generate 5 samples").
  - **Targets: 541** (PDB test, evaluated) **+ 66** (CASP15, evaluated) = 607 per model arm.
  - **Model arms: 4** (AlphaFold3, Chai-1, Boltz-1, Boltz-1x).
  - **Total headline predictions: 5 × 607 × 4 = 12,140 structures.**
  - **Plus the ablation: 9 distinct configurations × 5 samples × 541 structures ≈ 24,345
    additional Boltz-1 predictions** (Table 1 lists 11 rows, of which the "3 recycles / 200 steps"
    row is repeated three times — 9 distinct configurations).
  - Validation-set predictions during training: **NOT REPORTED** (n=553 set exists; how often it
    was scored is not stated).

- **comparable_to_ours**: *(left empty for the user)*

- **si_in_scope**: **No supplementary file exists and the 24-page PDF is complete** — Algorithms
  1–5 are inline (p9, p13, p20, p21, p22) and the 23-entry reference list closes it (p23–24).
  **But the headline numbers are effectively out of scope anyway:** the four-way comparison in
  Figures 5 and 6 is published *only as bar charts with no data labels and no companion table*, so
  every cross-model number in `metrics_reported` above is either read off a chart or stated
  loosely in prose. The exact values exist, but only in the released artefacts: p16, "we publicly
  release all the inputs, outputs, and evaluations of all the models in our benchmarks as well as
  the scripts we used to aggregate them", at https://github.com/jwohlwend/boltz — **NOT HELD by
  the corpus.** Record this as **NUMBERS NOT TABULATED IN PDF; RELEASED DATA NOT HELD**. Likewise
  the released train/validation/test split itself (553 / 593 structure IDs) is on GitHub and not
  in the PDF.

## F. Figures

Seven figures, **seven panel-group rows**. No figure needed splitting: each has a single `mark`
and a single `measure` (Figs 5 and 6 each show four metrics plus one physical-validity rate under
one mark and one shared value axis — a compound measure under common faceting, which the v3 rule
says is one row, not four).

**Pages rendered to fill this table: 3 (p10, p15, p16), at 150 dpi, deleted after reading.**
Renders were required for Fig 4 (the caption gives neither axes nor series), Fig 5 and Fig 6 (the
captions say only "visual summary" and carry no panel, series, metric or value information at all;
the metric names and the 8-way legend exist only in the rendered image). Figures 1, 2, 3 and 7 were
read from the text layer, whose captions and in-figure labels are complete for the purpose.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 1 | Two Boltz-1 predictions on test-set targets (PDB 8SVA and 8IG1), each annotated "TM-score: 0.95" — the cover showcase | structure render | `RENDER \| facet: target (2: PDB 8SVA, PDB 8IG1) \| views: 1 \| overlay: NOT REPORTED predictions on 1 reference (superposition implied by the TM-score but not stated) \| axis: none` | 2 side-by-side renders, varying by system. No panel letters | **Selection is not disclosed in the caption.** The caption reads only "Example predictions of Boltz-1 on targets from the test set"; only at p17, sixteen pages later, is it admitted these are "two examples of hard targets from the test set where Boltz-1 performed remarkably well". Two best-case targets out of 541, on the front page, with no distribution shown | **CC-BY 4.0** (stated in the footer of every page, p1–24). **No ND clause — redrawing and modification are both permitted with attribution** |
| 2 | 7 | 2-D cartoon contrasting AlphaFold3's reverse-diffusion interpolation with Boltz-1's Kabsch-aligned interpolation, showing how an unaligned interpolation can carry a "perfect" denoised prediction to a poor next-step structure | schematic | `SCHEMATIC \| paired 2-D point-and-arrow cartoons (model predictions → interpolation → next step) for AF3 vs Boltz-1 reverse diffusion, with colour marking point correspondence \| no data` | 2 cartoon columns varying by method (AlphaFold3, Boltz-1), sharing a left-hand column of model predictions | *(blank — declared as an explanatory cartoon; "Colors indicate correspondence between different points")* | as row 1 |
| 3 | 8 | Architecture block diagram of Boltz-1: input → atom attention encoder → MSA module → PairFormer trunk (with recycling) → denoising model chain under reverse diffusion → structure output; and, in a second block, the confidence model built from a full trunk composition fed by a stop-gradient plus the denoising model's recursive updates | schematic | `SCHEMATIC \| two-block network architecture diagram (trunk + reverse diffusion; confidence model) with labelled modules, recycling loop and a stop-gradient edge \| no data` | 2 blocks (trunk/diffusion, confidence model), varying by component, not by condition or system | *(blank)* | as row 1 |
| 4 | 10 | Forward-pass runtime of the authors' Trifast Triton kernel for Triangle Self-Attention against compiled PyTorch and the DeepSpeed kernel, as input size grows | line | `PLOT \| facet: none (1) \| vary: input size n, 0–2050 tokens (continuous) \| series: kernel implementation (3: Simple PyTorch compiled TF32-enabled, DeepSpeed, Trifast) \| measure: forward runtime (ms), RTX 3090, float32 \| n: 1 timing per point, repeats NOT REPORTED` | 1 panel, 3 lines. Title strip in-figure: "Triangle Attention, Forward Runtime (RTX 3090, float32)" | **No error bars and no repeat count** — every point is a single unreplicated timing. **The PyTorch line simply stops at n≈780 with no explanation** (presumably OOM), which is the most consequential fact in the plot and is not annotated. Backward-pass runtime and peak memory — the quantity the surrounding text argues about ("The memory complexity is often the limiting factor") — are **not plotted at all**; only forward runtime is | as row 1 |
| 5 | 15 | Four-way head-to-head on the 541-structure post-cutoff PDB test set: AlphaFold3, Chai-1, Boltz-1 and Boltz-1x, each in oracle and top-1 form, across five metrics, with 95% bootstrap CIs | bar | `PLOT \| facet: none (1) \| vary: metric (5: Mean LDDT, DockQ > 0.23, Mean LDDT-PLI, L-RMSD < 2A, Physical Validity) \| series: model × selection rule (8: AF3/Chai-1/Boltz-1/Boltz-1x × oracle/top-1) \| measure: metric value, shared 0–1 axis \| n: 541 structures per bar (subset for interface metrics: interfaces averaged within then across complexes containing them, per-metric counts NOT REPORTED)` | 1 panel, 5 metric groups × 8 bars = 40 bars. Series vary by model and by selection rule; nothing varies by system or view | **Bars hide distributions.** Every bar is a mean or a pass-rate over 541 structures with only a bootstrap CI; no violin, box, per-complex scatter or paired comparison is shown anywhere in the paper, so nothing reveals whether the models fail on the *same* targets. **No numeric labels**, and no companion table — the paper's central comparison is unreadable to more than ~±0.01 without downloading the released files. **Per-metric n is not shown**: the interface metrics are computed only over complexes that have such interfaces, a subset of 541 whose size is never stated. **Five metrics on different scales share one 0–1 axis**, so an LDDT and a pass-rate are given equal visual weight | as row 1 |
| 6 | 16 | The same four-way, eight-series comparison on the 66 evaluated CASP15 targets | bar | `PLOT \| facet: none (1) \| vary: metric (5: Mean LDDT, DockQ > 0.23, Mean LDDT-PLI, L-RMSD < 2A, Physical Validity) \| series: model × selection rule (8: AF3/Chai-1/Boltz-1/Boltz-1x × oracle/top-1) \| measure: metric value, shared 0–1 axis \| n: 66 targets per bar (fewer per interface metric, counts NOT REPORTED)` | 1 panel, 5 metric groups × 8 bars = 40 bars. Same structure as Fig 5, different benchmark | All of Fig 5's defects, plus one specific to n=66: **the confidence intervals are enormous and overlap almost everything** — DockQ CIs span roughly 0.17–0.82, so the apparent Boltz-1 advantage over AlphaFold3 on DockQ (~0.70 vs ~0.60) is not separable from noise, and the Boltz-1x physical-validity CI is **ceiling-censored at 1.0**. The paper draws no CASP15-specific conclusion in the text and states no CASP15 number, so the figure is the sole record of an under-powered comparison | as row 1 |
| 7 | 17 | Two paired failure/fix examples: PDB 8GH8 with overlapping DNA chains under Boltz-1 vs physical chain placement under Boltz-1x; PDB 8SUT with wrong small-molecule chirality under Boltz-1 vs correct chirality under Boltz-1x | structure render | `RENDER \| facet: target (2: 8GH8, 8SUT) × failure mode (2: overlapping chains, chirality) \| views: 1 \| overlay: NOT REPORTED predictions on 0 references (the model outputs are shown against each other, not against a deposited structure) \| axis: none` | 2×2 grid: rows vary by target/failure mode, columns vary by model (Boltz-1, Boltz-1x). In-figure labels carry the verdicts ("Overlapping DNA chains" / "Physical DNA chain placement"; "Wrong small molecule chirality" / "Correct small molecule chirality") | **The verdicts are visual, with no quantitative panel.** Two hand-picked cases stand in for the 43% → 97% physical-validity claim, and the figure shows no reference structure, so the reader cannot see whether the fixed pose is also the *correct* pose — only that it is physical. Selection criteria for the two examples are not stated | as row 1 |

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), session 2026-09-08
- **schema_version**: v3
- **confidence**: **high** on identity, the training cutoff, the split construction, the sampling
  defaults, the Boltz-1x/steering description, the confidence-model specification, the verbatim
  claim sets, and the absence of any conformational-state content (verified by full-text search
  for "conformation", "state", "ensemble", "apo", "allosteric", "cryptic"). **High** on figure
  structure for Figs 4–6, which were rendered. **Medium-low on the numeric values of the four-way
  comparison**, which exist only as unlabelled bars — every `[fig ~]` value should be treated as
  ±0.01 and should be replaced from the released evaluation files before any of them is quoted in
  the manuscript. The text layer is clean apart from mathematical notation (the diffusion
  equations on p7 and p12 are partially mangled by extraction, though the algorithm listings are
  legible) and several author typos noted below.
- **unresolved**:
  1. **The preprint version number is not printed in the PDF.** Only "this version posted May 6,
     2025" appears (p1 footer, every page). The task metadata says v4; the document does not.
     Since the paper itself announces that it "will be regularly updated" (p3), any corpus paper
     citing "Boltz-1" may be citing a different version with different numbers — in particular,
     the original 2024-11-19 posting predates the Boltz-1x/Boltz-steering material by roughly six
     months, so **a citation of Boltz-1 dated 2024 may well be to a version that does not contain
     §4 or Boltz-1x at all.** Flagged as the single most important provenance caveat in this note.
  2. **"resolution of at least 9Å" (p3) is almost certainly inverted.** Read literally it admits
     only structures worse than 9Å, which would exclude essentially the whole PDB. The intended
     meaning must be "no worse than 9Å" (a very permissive floor, consistent with AlphaFold3).
     Recorded verbatim as printed; the corpus should not silently repair it.
  3. **Steering hyperparameters are entirely unspecified.** λ, the seven potential weights
     (α_chiral, α_stereo, α_planar, α_geom, α_clash, α_overlap, α_covalent), the clash cutoff time
     t_clash, the number of SMC particles k, and the number of gradient-descent steps m all appear
     as symbols in §4.2–4.3 (p11–14) and **no numeric value is given for any of them**. Only the
     resampling cadence ("resampling every 3 timesteps", p12) and the flat-bottom geometric
     tolerances (π/6, 5π/6, π/12, 1.2U / 0.8L, 0.725×VdW, b_t interpolating 5.0 Å → 1.0 Å, 2 Å
     covalent) are stated. **Boltz-1x as described in this PDF is not reproducible from the PDF.**
  4. **Whether Boltz-1x has different weights from Boltz-1 is ambiguous.** p3 and p18 describe it
     purely as inference-time — "We refer to the Boltz-1 model with the steering as Boltz-1x"
     (p3) — but p18 also calls it "an updated model", and §4 never states that the weights are
     identical. On this document's own account it is the same generator plus a steered sampler,
     and this note records it that way. If another corpus paper reports Boltz-1x results that
     imply retrained weights, that difference did not come from this PDF.
  5. **CASP15 may intersect the validation set.** CASP15 targets (2022) fall inside the validation
     date window 2021-09-30 → 2023-01-13 (p4), and the paper never states whether any CASP15
     target was in the 553-structure validation set used during development. Not determinable from
     the PDF.
  6. **How the AlphaFold3 baseline was run is not stated** — server, weights, template usage, MSA
     substitution — beyond "we also used the same pre-computed MSA's up to 16384 sequences"
     (p15). Since Boltz-1 runs template-free by design and AlphaFold3 normally uses templates,
     the template configuration of the AF3 arm is a real gap in a head-to-head comparison.
  7. **The 52 test structures and 10 CASP15 targets dropped for OOM/failure/covalent ligands
     (p15) are not characterised.** If they are systematically the large or hard ones, every
     reported number is conditioned on an easier set.
  8. **Tag needed but not available: something for inference-time guidance on a diffusion
     trajectory.** `latent-steering` is defined in v3 as "any inference-time intervention on an
     internal tensor — pair representation, trunk embedding, distogram head, conditioning
     embedding", and Boltz-steering intervenes on **the sampled atom coordinates** during reverse
     diffusion (gradient guidance on x̂_t plus SMC resampling of particles), not on any learned
     internal representation. Applying `latent-steering` would return this paper for queries about
     trunk/pair-representation intervention, which is false; withholding it means the corpus's
     canonical inference-time-steering paper carries no method tag for its headline contribution.
     **Recommend a `diffusion-guidance` or `inference-time-potential` tag.** Not invented here.
  9. **Tag needed but not available: `templates-off`.** v3 has `templates-on` and
     `no-template-no-msa` but no tag for the very common regime this paper occupies — full MSA,
     no templates. `no-template-no-msa` is plainly false here (MSAs are central and deep). So the
     paper's explicit, quotable "we do not include input templates" (p3) is unfindable by reverse
     lookup.
  10. **Tag deliberately withheld: `confidence-as-discriminator`.** The paper uses pLDDT-family
      confidence to pick top-1 among 5 samples, but the tag's definition is about judging
      *conformational* correctness, which this paper never attempts. Tagging it would false-
      positive every query about confidence-as-a-state-discriminator. The confidence-model
      specification is recorded in full in Section C instead.
  11. **Control tags withheld** (`ligand-driven`, `partner-driven`, `directed-state`): the
      architecture conditions on ligands and partners and offers explicit pocket conditioning, but
      **no experiment in the paper varies an input condition and measures the structural
      response**, so tagging a control handle would record a capability as a demonstration.
  12. **Metric tags: both `continuous-metric` and `binary-predicate` applied**, since the five
      metrics split cleanly into two continuous (LDDT, LDDT-PLI) and three thresholded rates
      (DockQ > 0.23, RMSD < 2Å, PoseBusters all-pass). `rmsd-only` deliberately withheld: RMSD is
      one metric of five, not the sole criterion.
  13. **Author-list defect in `refs.bib`:** Regina Barzilay (p1) is missing.
  14. **Typos recorded for text fidelity, not corrected:** "AlphaFol3" (p4); "Kapsch" for Kabsch
      (Fig 2 caption p7, and p7 body, alongside correct "Kabsch"); "timeste,p" (p12);
      "largely denoising close to the projection" (p7, missing a word); footnote 2 on p6 ends
      "as reported ." with the citation missing; p16 says results are reported "in Figures 5 and
      7" where Figure **6** is meant (Figure 7 is the failure-mode render), and Table 1's caption
      on p18 repeats the same wrong cross-reference.
- **why_it_matters**: *(left empty for the user)*

## Tags

`general-protein` `cofolding` `single-state` `continuous-metric` `binary-predicate`
`saturating-metric` `anti-memorization` `multi-backbone` `preprint` `background` `precedent`
`comparator-numbers`

Tags withheld, with reasons in `unresolved`: `latent-steering` (Boltz-steering acts on sampled
coordinates, not an internal tensor — item 8); `templates-on` / `no-template-no-msa` (the paper is
full-MSA-with-templates-off, a regime the vocabulary cannot express — item 9);
`confidence-as-discriminator` (confidence ranks samples, never judges conformation — item 10); all
Control tags (capability, not demonstration — item 11); `rmsd-only` (item 12); all Site tags (no
site is studied); `prospective` (post-cutoff but retrospective); `oracle-leak` and
`design-level-oracle` (no target state exists to leak — the two route-4 findings are test-set
hyperparameter sweeping and metric-targeted potential design, neither of which is deposited-
structure leakage); `no-anti-memorization` (false — the design is strong); `unpowered` (n=541 and
n=66, both above threshold, though CASP15 CIs are very wide); `benchmark-only` (a model is trained
and is the subject); `contrast` / `threat` (the paper makes no conformational claim to conflict
with); `figure-exemplar` (the figures are held for their content, and Figs 5–6 are negative
examples of bar-chart reporting rather than models to copy).
