# chai2024chai1

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–18)**, which coincide with the
printed page numbers. Layout: p1 title/abstract/§1 Introduction, p2 Figure 1 + §2.1 Model
Architecture, p3 Figure 2 + §2.2 Protein-ligand, p4 Figure 3 + §2.3 Multimeric protein, p5 Figure 4,
p6 §2.4 Monomer / §2.5 Nucleic acid / §2.6 Confidence / §2.7 Lab server, p7 Figures 5 and 6, p8 §2.8
Limitations + §3 Discussion + §4 Contributors, p9 §5 Methods (Architecture, Constraints, Data and
Training, Genetic search), p10 (Genetic search cont., Inference, Baselines, Metrics), p11 (Metrics
cont., §5.6 Evaluation set), p12 §6 Supplementary Information — Tables 1 and 2, p13 Figure S1, p14
Figures S2 and S3, p15 §6.2 Supplementary data (external URL), p16–18 references.

**What this paper is.** A corporate technical report from Chai Discovery announcing Chai-1, an
AlphaFold3-style all-atom co-folding model. It is a MODEL paper, not a conformational-states paper.
It contains no conformational-state analysis of any kind: no alternative states, no apo/holo pairs
scored as states, no ensembles. Every Section C field that presupposes "which state did you steer it
to" is therefore `NOT APPLICABLE` by the nature of the work, not by extraction sloppiness. Methods
are thin by academic standards — architecture is delegated wholesale to Abramson et al. [11]
("largely follows", p2 and p9) and no architecture diagram beyond the schematic Figure 1, no
hyperparameters, no loss functions, no ablation of the language-model track are given. **Nothing in
this note is inferred from AlphaFold3 or from any other co-folding model.**

**Supplementary Information IS held** (p12–15): Tables 1–2 and Figures S1–S3. What is *not* held is
the externally hosted PoseBusters prediction archive
(`https://chaiassets.com/chai-1/paper/assets/posebusters_predictions.zip`, p15). No per-target result
table appears anywhere in the PDF. See `si_in_scope`.

---

## A. Identity

- **citekey**: `chai2024chai1`
- **doi**: **10.1101/2024.10.10.615955** (bioRxiv) — p1 banner: "bioRxiv preprint doi:
  https://doi.org/10.1101/2024.10.10.615955; this version posted October 15, 2024". No journal DOI
  appears in this PDF.
- **year**: **2024**. Two dates are given and they differ: the bioRxiv banner says "this version
  posted October 15, 2024" (p1, and repeated on every page), while the paper's own dateline reads
  "Date: September 9, 2024" (p1). Both recorded; neither is the "training cutoff" (see
  `anti_memorization_design`).
- **venue**: **bioRxiv preprint, not certified by peer review.** p1: "The copyright holder for this
  preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a
  license to display the preprint in perpetuity. It is made available under a CC-BY-NC 4.0
  International license." Tagged `preprint`; **not** `peer-reviewed`.
- **title**: Chai-1: Decoding the molecular interactions of life — p1
- **authors**: **Chai Discovery** is the sole byline on p1 — there is no author list on the title
  page. Individual names appear only under §4 Contributors on p8: "Jacques Boitreaud, Jack Dent,
  Matthew McPartlon, Joshua Meier, Vinicius Reis, Alex Rogozhnikov, Kevin Wu." For citation purposes:
  Chai Discovery (Boitreaud, Dent, McPartlon et al.). No corresponding author, no affiliations, no
  funding statement, no competing-interests statement, and no acknowledgements section anywhere in
  the PDF.

## B. Scope

- **system**: **general protein, plus nucleic acids, small-molecule ligands and antibodies** — a
  general biomolecular complex predictor. p1: "a multi-modal foundation model for molecular structure
  prediction that performs at the state-of-the-art across a variety of tasks relevant to drug
  discovery." Evaluated modalities: protein–ligand (PoseBusters), protein–protein multimers,
  antibody–protein and antibody–antigen interfaces, protein monomers, protein–DNA, protein–RNA, RNA
  monomers. No GPCR, kinase, transporter or fold-switching system is named or studied anywhere.
  Tag `general-protein` only.
- **n_targets**: **no single number; record every level, all pages given.**
  - **PoseBusters V1**: 427 structures evaluated (428 minus obsolete 7D6O), p3 and Table 1 p12.
  - **Protein–protein**: "n = 2362 protein-protein interfaces among n = 1054 PDB structures, which we
    then clustered to obtain n = 929 interface clusters" (p4). Figure 2 and Figure S2 report n = 929.
  - **Antibody–protein**: "This set includes 268 interfaces across 129 structures, forming 122
    redundancy reduced clusters" (p4). Figures 2 and S2 both label this axis group **n = 121**, not
    122 — a one-unit discrepancy the paper never explains. See `unresolved`.
  - **Antibody–antigen** (the Figure 4 constraint experiment, explicitly a *different* set from
    antibody–protein, p5): **n NOT REPORTED** — no count is given in text or caption.
  - **Protein monomers**: "447 protein monomers, belonging to 271 clusters" (p6); Figure 2 reports
    n = 271.
  - **CASP15 monomers**: 70 targets, 69 evaluated (T1169 excluded for inference time), p6.
  - **Nucleic acids** (Figure S3, p14): Protein–RNA n = 18, Protein–DNA n = 26, CASP15 RNA n = 9.
    Note the text on p6 says "9 CASP15 RNA targets" and AF3's cited number is on 8 of them.
  - **Training set size**: **NOT REPORTED.** The paper never states how many structures, chains or
    tokens Chai-1 was trained on.
- **method_class**: **co-folding.** An all-atom diffusion-based structure predictor taking sequence +
  chemical composition and emitting coordinates; p2 §2.1: "Our model architecture and training
  strategy largely follows that of Abramson et al. [11]". Tag `cofolding`. Not MSA-subsampling, not
  state-filtering, not template-biasing, not MD.
- **backbones**: **Chai-1 (this paper's own model)**, compared against — AlphaFold-Multimer 2.3 (run
  by the authors via ColabFold v1.5.5, p10); AlphaFold3 (**not run**; "Values are taken from
  AlphaFold3's publicly released PoseBusters predictions; we did not run AF3 ourselves", footnote 3,
  p3); RoseTTAFold All-Atom (published value, Table 1 p12); RoseTTAFold2NA (run via Tamarind Bio API,
  p10); ESMFold and ESM3 (cited numbers only, p1 and p6). More than two backbones compared →
  tag `multi-backbone`. **Boltz, Protenix and OpenFold3 do not appear** — they did not exist at
  submission.
- **templates**: **dual — on for the headline mode, off for single-sequence mode, plus one explicit
  template ablation.**
  - Training/inference templates from PDB70: "Templates are generated using PDB70 with the same
    cutoff date" (p9), i.e. 2021-01-12, so the template database cannot contain any evaluation
    structure.
  - Headline runs use them: "We run inference by giving Chai-1 the input sequence, MSAs, protein
    language model embeddings, and templates" (p10).
  - Ablation: "Without templates, Chai-1 achieves a slightly lower DockQ of 0.743; this reduction is
    not statistically significant" (p4), against 0.751 with templates.
  - Single-sequence mode omits them entirely: "MSAs and templates are omitted in this mode" (p10).
  - Chai-1 lab server runs without templates (p7). AF2.3 baseline was run *without* templates: "We do
    not search for or provide templates" (p10).
  - Tag both `templates-on` and `no-template-no-msa`.
- **msa_handling**: **full, or none. Never subsampled, never clustered, never state-filtered.**
  - Training MSAs: OpenProteinSet where available for UniRef90, UniProt, MGnify, UniClust30+BFD;
    otherwise jackhmmer v3.4 with `-N 1 -E 0.0001 --incE 0.0001 --F1 0.0005 --F2 0.00005 --F3
    0.0000005` and per-database `--seq_limit` (UniRef90 10000, UniProt 50000, Reduced BFD 5000,
    MGnify 5000) — p9–10.
  - Evaluation MSAs: "For inference over the datasets in our main analysis (CASP15, the low-homology
    evaluation sets, and PoseBusters), we additionally generated MSAs using jackhmmer with 3
    iterations (-N 3 flag) on the UniRef90, UniProt, and MGnify databases" (p10).
  - Web server MSAs differ from the paper's: jackhmmer in parallel over UniRef90, Uniprot and Mgnify,
    "the server does not query the Uniclust30+BFD database or use the -N 3 flag on jackhmmer" (p6),
    "the web interface only provides MSA with n=1 JackHMMer iteration" (p10).
  - **No nucleic-acid MSAs at all**, in training or inference: "Chai-1 is trained and performs
    inference without MSAs for nucleic acid sequences" (p6).
  - Single-sequence mode: no MSA. See `directional_control` and the dedicated MSA-free block below.
  - **MSA depth, cropping and subsampling parameters are NOT REPORTED.**

### B-supplement: the MSA-free / single-sequence mode (asked for explicitly)

**What the mode is** — Methods §5.3, p10, verbatim: *"In single sequence mode, we provide only the
input sequence and protein language model embeddings; MSAs and templates are omitted in this mode."*
Note that it is **not** a bare-sequence mode: the protein language model track stays on, and it is
the stated reason the mode works. §2.1.1, p2: *"To enable strong single-sequence capabilities in
Chai-1, we add an additional input track consisting of residue-level embeddings from a large protein
language model [13, 14, 8]."* The LM is a "3 billion parameter model [8]" (p9, citing ESM-2). Non-
protein tokens are masked and modified residues mapped to a canonical parent or "X" (p9). The mode is
not a separate model or a separate set of weights: "we use the same model for all evaluations" (p10).

**What it costs, with pages.** Headline claim, abstract p1: *"Chai-1 can also be run in
single-sequence mode without MSAs while preserving most of its performance."* The measured cost
(Table 2, p12; text p4 and p6):

| task | with MSA | single-sequence | delta | page |
|---|---|---|---|---|
| Protein–protein DockQ success (>0.23), n=929 clusters | 0.751 (0.723, 0.778) | 0.698 (0.668, 0.728) | −0.053 | p12, text p4 |
| Protein–antibody DockQ success (>0.23), n=121 | 0.529 (0.438, 0.620) | 0.479 (0.388, 0.570) | −0.050, CIs overlap heavily | p12, text p4 |
| Protein monomer Cα-LDDT, n=271 clusters | 0.915 (0.907, 0.922) | 0.852 (0.834, 0.867) | −0.063 | p12, text p6 |

The cost is **not uniform, and monomers are where it bites**: p6, verbatim — *"Without MSA
information, Chai-1 exhibits poorer performance on monomer folding than AF2.3 (two-sided Wilcoxon
test, p = 4.46 × 10−16)."* That is single-sequence Chai-1 (0.852) losing to AF2.3 *with* MSAs
(0.903). On interfaces the opposite holds: p4, verbatim — *"In single-sequence mode without MSAs,
Chai-1 also performs comparably to AF2.3 with MSAs (0.698 vs. 0.677; difference between means is not
statistically meaningful)"*, and on antibodies, p4 — *"Chai-1 without MSAs in single-sequence mode
performs similarly to Chai-1 when given full MSAs on these antibody-protein interfaces, and also
outperforms AF2.3 (which is still provided MSA information, two-sided Wilcoxon test, p = 4.04 ×
10−4)."* Their stated explanation, p4–5: *"We hypothesize that MSAs have little performance impact
for Chai-1 on this antibody set because there is less evolutionary signal available in the first
place for these more variable sequences."*

**Nucleic acids are always single-sequence** (p6): "running the model in single sequence mode (i.e.
no RNA MSAs) in all cases", and Chai-1 still matches RoseTTAFold2NA, which has full MSAs.

**The claim staked on it**, p4, verbatim: *"Chai-1 is the first model to offer high-accuracy multimer
folding without the need for MSAs, while also outperforming AF2.3 when using MSAs."*

**Speed is asserted but never measured.** p5: "Chai-1 in single-sequence mode appears to be a
particularly potent method for exploring design space of highly variable immunological protein
sequences as it is both fast and accurate." **No runtime, wall-clock or throughput number for either
mode appears anywhere in the paper — NOT REPORTED.**

## C. Conformational core

- **states_generated**: **one.** Chai-1 emits a single top-ranked static structure per target,
  selected by a confidence model from 25 samples: "We run Chai-1 with 4 recycles, 5 trunk samples and
  5 diffusion samples for a total of 25 predicted structures unless otherwise noted. A confidence
  model is then used for ranking" (p10). The 25 samples are seeds of one predictor, never analysed as
  an ensemble, never clustered, and never described as sampling distinct conformational states. The
  only place all 25 are used is the "Chai-1 oracle" curve in Figure S1B (p13), which is a
  best-of-25-vs-ground-truth accuracy ceiling, not a state analysis. **No alternative-conformation,
  apo/holo, or multi-state result appears in this paper.** Tag `single-state`.
- **structural_priors_used**: **substantial and fully disclosed at the dataset level; thin at the
  per-parameter level.** This is training data, not leakage.
  - **PDB, release date ≤ 2021-01-12**: "Chai-1 is trained on both PDB and AlphaFoldDB [27]
    structures. For PDB structures, we apply with a release date cutoff of 2021-01-12" (p9). No count
    of structures given.
  - **AlphaFold Protein Structure Database (AFDB)** as the only distillation set: "We do not train on
    any of the distillation datasets described in [11] other than AFDB" (p9). This is an explicit
    *negative* disclosure and is unusually informative — it says Chai-1 did **not** use AF3's other
    distillation corpora.
  - **PDB70 templates**, same cutoff (p9).
  - **OpenProteinSet [28] MSAs** for UniRef90, UniProt, MGnify, UniClust30+BFD (p9).
  - **ESM-family protein language model embeddings**, 3B parameters (p9) — a sequence prior trained
    on UniRef, itself indirectly shaped by structure only through sequence.
  - **Ground-truth structures shape the constraint features at training time**: pocket and contact
    constraints are sampled from the true structure, "we randomly sample θP ∈ (6, 20) and randomly
    sample satisfying pocket constraints from the ground truth structure … we randomly sample θD ∈
    (6Å, 30Å) and satisfying constraints ∥xi − xj∥ ≤ θD from the ground truth structure" (p9), and
    docking features come from "partitioning the chains of the ground truth complex into two groups"
    (p9). This is standard supervised conditioning and is not itself an evaluation leak; it becomes
    one only where the same construction is used at *evaluation* time, which it is — see route 1 of
    `oracle_leakage`.
  - **Preprocessing prior**: "In all cases we remove crystallization aids, mirroring how our model was
    trained" (p10). Figure 3 (p4) then turns on exactly this: a DMS crystallization aid in the
    reference structure of 7Q2B, which the model never sees.
  - **SAbDab [20] annotations** identify antibody vs antigen chains for the Figure 4 evaluation (p5).
    This is an annotation prior, not a state annotation.
  - **NOT REPORTED**: number of training structures, training/validation split sizes, crop size and
    sampling weights, number of training steps or epochs (only wall-clock: "128 Nvidia A100 GPUs with
    a batch size of 128 for 30 days", p9), model parameter count, diffusion schedule, loss weights,
    confidence-head training procedure.
- **oracle_leakage**: **the headline blind arms are clean; three named non-headline arms use the
  reference structure openly and are labelled as such by the authors themselves.** All seven routes
  answered separately.

  **Route 1 — deposited structures used as input or template.** *PRESENT IN NAMED NON-HEADLINE ARMS,
  NONE FOUND in the headline arms.*
  - Headline PoseBusters, protein–protein, antibody–protein and monomer arms take sequence and
    chemistry only: "Given only the sequence of the protein and the chemical composition of the
    ligand, Chai-1 achieves a ligand RMSD success rate of 77%" (p3). Templates come from PDB70 with
    the 2021-01-12 cutoff (p9) and so cannot contain a post-cutoff evaluation structure.
  - PoseBusters *docking* arm, verbatim p3: *"Namely, specifying the apo structure of the protein
    boosts success rate to 81%. We note that the holo structure of the protein could leak
    conformational information that makes the task easier, and we therefore primarily consider this
    task as a way to evaluate the prompt following abilities of the model."* The authors flag the
    leak themselves, use the apo rather than the holo form, and report the arm separately (Table 1,
    p12, "Chai-1 - Docking 81.20 %"). It is not the headline number.
  - Figure 4 constraint arms, verbatim p5: *"One Contact (15A)/One Contact (25A) we randomly sample a
    pair of residues, one in the antibody chain and one in the antigen chain with distance less than
    15Å/25Å respectively and provide the pair and distance threshold to our model as a contact
    feature. One Epitope (8 Å)/Four Epitope (8 Å) we sample one/four antigen residue(s) that have
    minimum Cα distance less than 8Å to some residue in the antigen chain and provide this residue
    and chain as a pocket feature."* These restraints are drawn from the solved complex. The paper's
    framing is explicit that this simulates wet-lab data: "We illustrate the impact of our pocket and
    contact features by simulating experimentally derived constraints" (p5). The `Blind` bar in the
    same figure is the un-leaked control, and it is shown alongside.
  - PoseBusters cropping, p3, verbatim: *"For 4/428 structures that have more than 2048 tokens, we
    crop the assembly to the 2048 tokens closest to the ligand binding site."* The binding site is
    known from the reference. 4 of 427 structures; small, but it is reference-derived input.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates or
  alignments.** *NONE FOUND.* No conformational-state database is used, mentioned or cited anywhere.
  The only curated annotation database is SAbDab, used to label which chain is the antibody and which
  the antigen (p5, "according to SAbDab annotation [20]"), which carries no state information. The
  full inference protocol is on p10 §5.3 and the evaluation-set construction on p11 §5.6.

  **Route 3 — cluster labels derived from known states.** *NONE FOUND.* Every clustering in the paper
  is by sequence identity, not by structure or state: "Individual polymer chains were clustered at
  40% sequence identity for proteins more than 9 residues, and 100% sequence identity for proteins
  with 9 or fewer residues and for all nucleic acids" (p11); interface cluster IDs are the tuple of
  the two participants' sequence clusters (p11).

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.**
  *NONE FOUND for state; NOT REPORTED more broadly, and two ranges deserve naming.*
  - No hyperparameter sweep, no validation-set tuning procedure and no model selection criterion is
    described anywhere. There is no statement that any setting was chosen on the evaluation sets, and
    equally no statement that it was not. Sampling settings are given as fixed defaults (p10).
  - The two sampled ranges in the paper — pocket θP ∈ (6, 20) and contact θD ∈ (6Å, 30Å), plus the
    geometric restraint-count distribution p = 1/3 (p9) — are **training-time** augmentation ranges,
    not ranges swept on the evaluation set. The Figure 4 evaluation thresholds (15 Å, 25 Å, 8 Å, p5)
    are fixed reporting conditions, each shown as its own bar rather than a per-target choice.
  - One ranking heuristic is unjustified and could in principle have been tuned on PoseBusters: "We
    rank samples by the interface pTM-score of the ligand and penalize ligands that do not respect
    the input chirality by dividing their interface pTM-score by 100" (p3). The factor 100 is stated
    without derivation and no ablation of it is shown. Recorded as a candidate, not an established
    leak.
  - Two exclusions are made on the evaluation sets: 7D6O ("marked as obsolete in PDB", p3) and CASP15
    T1169 ("could not complete inference on Chai-1 in a reasonable timeframe", p6). The second is an
    exclusion made *because of the model's own behaviour on that target*; it is one target out of 70,
    and the authors report the un-excluded AF2.3 number alongside for comparability (p10).

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.** *PRESENT, and
  unavoidable for a benchmark paper; the thresholds are pre-registered community standards, not
  chosen here.* Every success criterion is distance-to-reference: pocket-aligned ligand RMSD < 2 Å,
  DockQ > 0.23, Cα-LDDT (Figure 2 caption, p3), with the stricter DockQ ≥ 0.49 and ≥ 0.8 cutoffs in
  Figure S2 (p14). The 2 Å and DockQ thresholds are taken from Buttenschoen et al. [15] and the DockQ
  literature [35] rather than defined here — p3: "We follow the recommendations provided in
  Buttenschoen et al. [15] and Abramson et al. [11] to compute success rate". No conformational state
  is defined by RMSD, because none is defined at all.

  **Route 6 — best/worst model labels assigned against a held reference.** *PRESENT, and explicitly
  labelled as such in both places it occurs.*
  - Figure S1B, verbatim p13: *"Chai-1 oracle takes the best (lowest ligand RMSD) prediction after
    comparing all 25 examples to the ground truth."* Reported as a separate named curve alongside
    "Chai-1 - confidence ranked" and "Chai-1 - random"; the headline 77% is the confidence-ranked
    number, not the oracle one.
  - Figure 4B, verbatim p5: *"Cherry-picked example predictions for PDB ID 7SYV with and without
    epitope residues (pocket restraints, purple) provided."* The word is the authors'. Figure 3 (p4)
    is likewise a hand-selected failure case, chosen after comparison to the reference.

  **Route 7 — design-level oracle use (systems or input conditions chosen because the expected answer
  is known).** *PRESENT, weaker than pipeline leakage, and confined to the demonstration arms.*
  - The Figure 4 restraint settings declare where the interface is before the prediction is read;
    they are described as "simulating experimentally derived constraints" (p5), i.e. a stand-in for
    data the user would not have. The Blind arm is the honest baseline and is reported (35% acceptable
    vs 57% with one 15 Å restraint, p5).
  - Figure 6 (p7) examples are chosen for narrative: "These have been chosen to emphasize potentially
    therapeutically relevant structures" (p7).
  - The PoseBusters 2048-token crop is centred on the known binding site (p3).
  - Against this, the primary evaluation sets are *not* target-selected: they are whole temporal
    slices of the PDB with mechanical homology filters (p11), which is the opposite of design-level
    target picking.

- **prospective**: **no — retrospective throughout, but temporally held out and homology-filtered,
  which is the strong form of retrospective.** Every evaluated structure was already deposited in the
  PDB when the paper was written; nothing was predicted before its experimental structure existed.
  The mitigation is temporal, not prospective: PoseBusters structures "are released on or after
  2021-01-13 – after our training data cutoff" (p3) and the main evaluation set is "constructed from
  a temporal split of PDB entries released between 2022-05-01 and 2023-01-12" (p11). The constraint
  arms of Figure 4 are additionally retrospective in their *inputs*, since the restraints come from
  the answer (see route 1). No wet-lab validation of any prediction is performed.
- **state_metric**: **NOT APPLICABLE — no conformational state is assessed anywhere in this paper.**
  For completeness, the *accuracy* metrics (which are not state metrics) are, from §5.5 p10–11 and
  Figure 2 caption p3: pocket-aligned ligand RMSD with a 2 Å success threshold, where interface atoms
  are "any Cα atom within 10 Å of any ligand atom in the true structure" (p10); DockQ with success at
  > 0.23 and stricter cutoffs ≥ 0.49 and ≥ 0.8 (Figure S2, p14); Cα-LDDT at 15 Å inclusion radius;
  C1′-LDDT at 30 Å inclusion radius for nucleotides; interface LDDT over Cα and C1′ atoms (p11).
  Chain-mapping for DockQ is by exhaustive permutation below 8! and by an alignment-based greedy
  procedure above it, and the paper notes this "differs significantly from the simulated annealing
  approach described by Abramson et al. [11]" (p11) — a real comparability caveat for anyone placing
  Chai-1 DockQ numbers next to AF3's.
- **metric_saturation**: **yes, numerically, in one place.** Figure S1A (p13): the PoseBusters
  chemistry-validity checks sit at or fractionally below 1.0 for essentially all 18 criteria for both
  Chai-1 and AF3, so the panel has no headroom and the only criteria that discriminate are
  tetrahydral chirality (~0.96 vs ~0.94) and volume overlap with proteins (~0.97 vs ~0.89). The
  DockQ success rate and the ligand-RMSD success rate are binary threshold predicates and therefore
  saturate by construction at 1.0, but no reported arm approaches that (highest is 0.915 Cα-LDDT,
  Table 2 p12, which is a continuous metric). No arm floors at 0. Figure axis issues are recorded in
  the `hides` column of Section F, not here.
- **directional_control**: **yes — this is Chai-1's distinguishing feature, but it directs *interface
  geometry*, not conformational state.** The named handles, all from p2 §2.1.2 and p9 §5.1.2:
  - **pocket constraint** — a token ID i, chain ID C and distance threshold θP, asserting
    minj∈C ∥xi − xj∥ ≤ θP (p9). Used at evaluation as "One Epitope (8 Å)" / "Four Epitope (8 Å)"
    (p5).
  - **contact constraint** — a token pair (i, j) and threshold θ, asserting ∥xi − xj∥ ≤ θD (p9).
    Used as "One Contact (15A)" / "One Contact (25A)" (p5).
  - **docking constraint** — a one-hot encoding of pairwise inter-group distances in four bins
    [0–4Å, 4–8Å, 8–16Å, >16Å] between two partitions of the chains (p9). Explicitly distinguished
    from templates: "while templates contain intra-chain distance information, they do not contain
    inter-chain distances" (p9).
  - **templates** (intra-chain distances, PDB70) and **the apo receptor structure** in the docking
    task (p3).
  - **MSA on/off** and **template on/off** as coarse regime switches (p10).
  All constraint features are trained with dropout ("chain-wise and token-wise dropout … each of
  these features is included independently with probability 10% during training", p9) so the model
  does not require them. **There is no handle that names a conformational state**, and no seed or
  subsample-depth control is offered as a diversity knob — the 5 trunk × 5 diffusion samples are for
  ranking, not for state exploration.
- **anti_memorization_design**: **yes, and it is the paper's most carefully specified section
  (§5.6, p11).** Three separate held-out constructions:
  1. **PoseBusters V1**, n = 427: "All structures in this benchmark set are released on or after
     2021-01-13 – after our training data cutoff" (p3). Temporal only; PoseBusters carries its own
     novel-sequence design [15].
  2. **Low-homology temporal evaluation set**: "constructed from a temporal split of PDB entries
     released between 2022-05-01 and 2023-01-12; these structures were all released after any data in
     our training set (most recent cutoff date of 2021-01-12)" (p11), filtered to non-NMR, resolution
     better than 4.5 Å, ≤ 2048 tokens, then homology-filtered — "Monomers with 40% or greater
     sequence identity to the training set are removed"; polymer–polymer interfaces removed "where
     both polymers have greater than 40% sequence identity to two chains in the same complex in the
     training set"; polymer–peptide interfaces removed where the non-peptide entity has ≥ 40% identity
     (p11). Then clustered at 40% identity and reported per cluster: n = 929 protein–protein
     interface clusters, n = 121 antibody–protein, n = 271 monomer clusters.
  3. **CASP15**, 69 of 70 monomer targets and 9 RNA targets (p6) — a blind community assessment,
     though held here retrospectively.
  A caveat the paper states itself, p11: "in the case of complexes, the overall complex that we
  predict may contain chains that have significant homology to the training set, but we only evaluate
  on interfaces that are low-homology as defined above."
  The **cutoff is stated exactly and repeatedly** — see the block below.
- **anti_memorization_control**: **the held-out sets are the primary evaluation and are analysed, so
  this is not the common "held out but never used" failure — but no dedicated memorization *control
  arm* is run.** What exists: the low-homology filter is applied and the filtered set is what every
  headline number is computed on (p11); the AF2.3 baseline is run on the identical set (p10). What
  does **not** exist: no pre-cutoff vs post-cutoff comparison, no high-homology vs low-homology
  comparison, no training-set-recall probe, no ablation of the 40% identity threshold. So there is no
  measurement anywhere of *how much* the homology filter cost, which is exactly the number a
  memorization argument needs. **NO DEDICATED CONTROL ARM RUN.** Powered, not `UNPOWERED`: n = 929,
  427 and 271 are all comfortably above 10; the antibody–antigen constraint set of Figure 4 has **no
  reported n at all** and its high-quality bars are described by the authors as low (4–8%, p5).
  One internal contradiction worth flagging, Figure 5 caption p7, verbatim: *"Here we show results for
  all interfaces in our low homology subset, and do not restrict only to interfaces with low
  homology."* Those two clauses contradict each other; the confidence-calibration analysis may
  therefore include homologous interfaces. Recorded in `unresolved`.
- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | Temporal cutoff 2021-01-12 on training; all evaluation structures released after it | Direct memorization of the evaluation structures | p9, p11, p3 |
  | 40% sequence-identity homology filter against the training set (monomers, interfaces, peptides) | Memorization via a close homolog rather than the exact chain | p11 |
  | 40% sequence-identity clustering with per-cluster averaging | Over-representation of large redundant families inflating the mean | p4, p11 |
  | `Blind` arm in Figure 4 (no constraints supplied) | That the restraint gains are an artefact rather than a response to the prompt | p5 |
  | Template ablation on protein–protein (0.743 vs 0.751, n.s.) | That the headline multimer result depends on templates | p4 |
  | Single-sequence ablation (no MSA, no templates) on all three protein tasks | That the headline result depends on MSAs | p4, p6, Table 2 p12 |
  | "Chai-1 random" arm in Figure S1B (mean over all 25 samples) | That the reported accuracy is a lucky sample rather than the typical one | p13 |
  | "Chai-1 oracle" arm in Figure S1B (best of 25 vs ground truth) | Bounds how much confidence-ranking leaves on the table | p13 |
  | AF2.3 run in-house on the identical evaluation set via ColabFold, verified against a published number (0.842 vs Hayes et al. 0.826 on CASP15 n=70) | That the baseline was mis-run or under-tuned | p10 |
  | PoseBusters chemistry-validity checks (18 criteria) run on the predictions | That RMSD success is achieved with physically invalid poses | Fig S1A, p13 |
  | Server-vs-internal-pipeline spot check on PoseBusters examples (µ = 0.345 Å, σ = 0.150 Å, all < 1 Å) | That the public server reproduces the paper's pipeline | p6–7 |
  | Stricter DockQ cutoffs (≥ 0.49, ≥ 0.8) in Figure S2 | That the lead over AF2.3 exists only at the loosest threshold | p5, p14 |
  | Chirality penalty applied in ranking (interface pTM ÷ 100 for chirality violators) | Ranking a chirally invalid pose to the top | p3 |
  | Crystallization aids removed at inference, "mirroring how our model was trained" | Train/test input mismatch on solvent and cryoprotectant molecules | p10 |
  | **NOT RUN**: seed-variance / run-to-run reproducibility arm | — | — |
  | **NOT RUN**: ablation of the protein language model track | — | — |
  | **NOT RUN**: high-homology vs low-homology comparison | — | — |

- **confidence_as_discriminator**: **yes as a *quality* discriminator, and yes they validated that
  use against ground truth. NOT APPLICABLE as a conformational-state discriminator — no state is ever
  judged.** What is predicted: **ipTM** (interface predicted TM-score), reported per chain-pair
  ("Chain-pair ipTM is shown for each plot and refers to the ipTM score of the two chains defining the
  interface being evaluated", Figure 5 caption p7), and **ligand interface pTM** used for PoseBusters
  ranking (p3, and Figure S1B "ranked by ligand ipTM"). A separate "confidence model … used for
  ranking" produces these (p10); **its architecture, training and outputs are NOT REPORTED beyond the
  parenthetical "(details below)" on p10, and no such details in fact follow anywhere in the paper —
  this is the largest single methods gap.** pLDDT, PAE and pTM are never mentioned.
  The claim, §2.6 p6, verbatim: *"We find that model confidence estimates from Chai-1 are well
  calibrated with prediction quality. In Figure 5 we show that interface predicted TM score (ipTM) is
  a strong discriminator of model quality across all molecular interaction types."*
  The validation: Figure 5 (p7) plots DockQ against binned chain-pair ipTM for protein–protein (5A)
  and protein–nucleic-acid (5B) interfaces, and pocket RMSD against binned chain-pair ipTM for
  protein–ligand (5C); Figure S1C (p13) plots ligand RMSD against binned ligand ipTM on PoseBusters.
  Two honest scoping notes are given in the same breath (p6): "the set of interfaces evaluated in
  Figure 5 include all model predictions rather than only the top prediction for each interface,
  ranked by confidence", and "protein-ligand interactions are restricted to non-bonded ligands and
  exclude ions".
  **No numeric calibration statistic is given** — no Spearman ρ, no AUROC, no expected calibration
  error, no per-bin n. "Well calibrated" and "strong discriminator" are asserted from the shape of
  boxplots. Tag `confidence-as-discriminator`.

### C-supplement: the training data cutoff (asked for explicitly)

**The cutoff IS stated, exactly, and in four independent places.** It is **2021-01-12** for PDB
training structures and for the PDB70 template database. Verbatim:

- p2, §2.1 Model Architecture: *"Our model architecture and training strategy largely follows that of
  Abramson et al. [11] with the key difference that we train a single model with a training data date
  cutoff of 2021-01-12 as opposed to training separate models for separate evaluations."*
- p9, §5.2 Data and Training: *"Chai-1 is trained on both PDB and AlphaFoldDB [27] structures. For PDB
  structures, we apply with a release date cutoff of 2021-01-12. We do not train on any of the
  distillation datasets described in [11] other than AFDB. Templates are generated using PDB70 with
  the same cutoff date."*
- p11, §5.6 Evaluation set: *"these structures were all released after any data in our training set
  (most recent cutoff date of 2021-01-12)."*
- p3, §2.2, stated from the other side: *"All structures in this benchmark set are released on or
  after 2021-01-13 – after our training data cutoff."*

Two consequences that matter for anyone defining a held-out set against Chai-1:

1. **There is one model, not a per-evaluation family.** p10, §5.3, verbatim: *"Unlike Abramson et al.
   [11], we use the same model for all evaluations since our training data cutoff does not overlap
   with the data used in any of our evaluation sets."* So a single cutoff date is sufficient to
   characterise Chai-1 for every task in this paper — unlike AF3 as described here.
2. **The cutoff applies to PDB and PDB70 only.** The AFDB distillation set has **no stated cutoff**
   (p9), and the genetic databases are dated only by reference: "All databases use the same date
   cutoffs and versions described in [6]" (p10), i.e. deferred to the AlphaFold2 paper and **not
   given numerically here**. A held-out set defined purely against 2021-01-12 is therefore clean with
   respect to Chai-1's PDB training data and its templates, but the paper does not let you verify the
   AFDB or sequence-database vintages.

No other cutoff date appears in the paper. If a downstream benchmark cites a different date for
Chai-1, it is not sourced from this document.

## D. Claims

- **central_conclusion**: Chai-1, an AlphaFold3-architecture all-atom co-folding model trained to a
  2021-01-12 PDB cutoff, matches AF3 on PoseBusters ligand placement (77.05% vs 76.34%) and beats
  AlphaFold-Multimer 2.3 on protein–protein, antibody–protein and monomer accuracy on a post-cutoff
  low-homology set; a language-model track lets it run without MSAs or templates at a modest cost
  (and no cost at all on antibody interfaces), and optional pocket/contact/docking restraint features
  raise antibody–antigen DockQ success by double-digit percentage points when interface information
  is supplied. Weights and inference code are released for non-commercial use, and a free web server
  permits commercial use.
- **necessity_claims** (verbatim + page):
  - p4: *"Chai-1 is the first model to offer high-accuracy multimer folding without the need for
    MSAs, while also outperforming AF2.3 when using MSAs."* (This is simultaneously the paper's
    strongest novelty claim and its strongest necessity-*negation*: it asserts MSAs are not needed.)
  - p4: *"Notably, while previous work has studied single-sequence models for multimer folding [17],
    prior methods have fallen short of AF2.3 in terms of performance."*
  - p5: *"Unfortunately, AF3 restricts commercial use and so we cannot benchmark DeepMind's latest
    model on the above protein-protein and protein-antibody evaluations."*
  - p6: *"Due to commercial use restrictions, we are unable to directly compare to several recent
    methods – including AF3 and ESM3 – for protein structure prediction."*
  - p11: *"we are not able to match exactly the evaluation set used in AF3. As a result, values
    reported on protein-protein interactions, protein-antibody interactions, protein-DNA and
    protein-RNA interactions are not directly comparable to those reported in Abramson et al. [11]."*
  - p5: *"Unfortunately the fraction of high quality predictions still remains low (4-8%) which
    suggests that high quality antibody-antigen structure prediction remains a generally challenging
    task."*
  - p10: *"Inference is currently limited to a maximum of 2048 tokens."*
  - p8: *"We hypothesize that this is because Chai-1 has been trained explicitly on structures with
    modifications and relies on this information to accurately predict structures."*
- **novelty_claims** (verbatim + page):
  - p4: *"Chai-1 is the first model to offer high-accuracy multimer folding without the need for
    MSAs, while also outperforming AF2.3 when using MSAs."* — the sole explicit priority claim.
  - p5: *"More broadly, these above results suggest that Chai-1 sets a new benchmark for multimer
    protein folding in both its full performance mode with MSAs, and its single-sequence mode without
    MSAs and without structural templates."*
  - p1: *"Here we introduce Chai-1, a state-of-the-art and openly accessible foundation model for
    biomolecular structure prediction."*
  - p1 (abstract): *"We introduce Chai-1, a multi-modal foundation model for molecular structure
    prediction that performs at the state-of-the-art across a variety of tasks relevant to drug
    discovery."*
  - p1: *"In single sequence mode, Chai-1 outperforms ESMFold, and can even outperform AF-Multimer2.3
    [12] – which we evaluate with MSAs – under certain evaluations."*
  - Architectural novelty is claimed only modestly, p2: *"We also make a number of key additions to
    enable new functionality (Figure 1)"*, the additions being the language-model track and the
    constraint features. p2 also concedes the LM idea is prior art: *"a number of language models have
    been introduced and shown to enable accurate prediction of protein structure. However, these
    models have yet to demonstrate actionable performance on multimeric prediction or protein-ligand
    interactions."*
- **stated_limits**: an explicit §2.8 Limitations (p7–8) plus limits scattered through Results and
  Methods.
  - **Relative chain orientation**, p7–8: *"the model may sometimes predict the individual chains in a
    complex correctly, but fail to place them in the correct relative orientations."*
  - **Modified residues**, p8: *"Chai-1 can be highly sensitive to modified residues. Removing
    modified residues from a sequence that natively posses them or replacing modified amino acids with
    their standard amino acid analogs can cause large changes in predicted structures."*
  - **Single-sequence monomer folding is worse than AF2.3**, p6 (quoted in full above).
  - **High-quality antibody–antigen prediction remains poor**, 4–8% high-quality even with restraints
    (p5).
  - **RNA is behind AF3**, p6: *"AF3 reports a LDDT of 0.473 on 8 of the CASP15 RNA targets, which
    suggests improved performance on RNA structures."*
  - **Server ≠ paper pipeline**, p7: *"we note that these changes may still result in subtle
    discrepancies between the server results and those in the paper, and we therefore refer readers
    to the GitHub repository where all variables can be controlled."*
  - **AF3 comparison is second-hand**, footnote 3 p3: *"Values are taken from AlphaFold3's publicly
    released PoseBusters predictions; we did not run AF3 ourselves."*
  - **Cross-paper DockQ numbers are not comparable** (p11, quoted above), compounded by a different
    chain-mapping procedure from AF3's (p11).
  - **2048-token inference limit** (p10).
  - **PoseBusters manual inspection caveat**, p4: the 7Q2B "failure" may be an artefact of a DMS
    crystallization aid in the reference, "This highlights the importance of manually inspecting
    models".
  - **Nucleic-acid MSAs absent**, p6: *"Future work incorporating nucleic acid MSAs or nucleic acid
    language model embeddings [22, 23] could improve its accuracy when modeling these complexes."*
- **stance**: **`precedent` + `background`** (provisional; the user's call).
  - **precedent** — on two specific things this corpus will want to cite: (a) that a co-folding model
    can run MSA-free at near-parity on interfaces, with the exact accuracy cost quantified in Table 2
    (p12); (b) the exact training cutoff 2021-01-12 (p2, p9, p11), which is the datum other corpus
    papers define their held-out sets against, plus the single-model claim (p10) that makes one date
    sufficient. Also `comparator-numbers`: Tables 1 and 2 are directly reusable.
  - **background** — on everything conformational. This paper produces one structure per target,
    never mentions conformational states, ensembles, apo/holo pairs or alternative basins, and offers
    no state-directing handle. It is the substrate other corpus papers perturb, not a competitor to
    them.
  - **Not `contrast`**: the rigour is above the corpus average (temporal cutoff plus homology filter
    plus clustering plus a run-in-house baseline), and where oracle information is used the authors
    label it themselves. **Not `threat`**: it makes no claim about conformational sampling that would
    pre-empt anything.

## E. Quantitative comparators

- **metrics_reported**:

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Ligand RMSD success (pocket-aligned RMSD < 2 Å), Chai-1 blind | 77.05 | % of targets | PoseBusters V1, n = 427 structures | Table 1, p12; text 77%, p3 |
  | Ligand RMSD success, AF3 (published predictions, not re-run) | 76.34 | % of targets | PoseBusters V1, n = 427 | Table 1, p12; footnote 3, p3 |
  | Ligand RMSD success, RoseTTAFold All-Atom (published) | 42 | % of targets | PoseBusters V1, n = 427 | Table 1, p12 |
  | Ligand RMSD success, Chai-1 with apo receptor supplied (docking task) | 81.20 | % of targets | PoseBusters V1, n = 427 | Table 1, p12; text 81%, p3 |
  | DockQ success rate (> 0.23), Chai-1 with MSA | 0.751 (95% CI 0.723–0.778) | fraction of clusters | Low-homology protein–protein, n = 929 interface clusters (2362 interfaces, 1054 PDB structures) | Table 2, p12; text p4 |
  | DockQ success rate (> 0.23), Chai-1 single-sequence | 0.698 (0.668–0.728) | fraction of clusters | same, n = 929 | Table 2, p12 |
  | DockQ success rate (> 0.23), Chai-1 with MSA, no templates | 0.743 | fraction of clusters | same, n = 929; "reduction is not statistically significant" | p4 |
  | DockQ success rate (> 0.23), AlphaFold-Multimer 2.3 | 0.677 (0.646–0.706) | fraction of clusters | same, n = 929; Chai-1 vs AF2.3 two-sided Wilcoxon p = 6.24 × 10⁻¹⁰ | Table 2, p12; text p4 |
  | DockQ success rate (> 0.23), Chai-1 with MSA | 0.529 (0.438–0.620) | fraction of clusters | Antibody–protein subset, n = 121 clusters (268 interfaces, 129 structures) | Table 2, p12 |
  | DockQ success rate (> 0.23), Chai-1 single-sequence | 0.479 (0.388–0.570) | fraction of clusters | same, n = 121; beats AF2.3 at p = 4.04 × 10⁻⁴ | Table 2, p12; text p4 |
  | DockQ success rate (> 0.23), AlphaFold-Multimer 2.3 | 0.380 (0.298–0.463) | fraction of clusters | same, n = 121; Chai-1 vs AF2.3 p = 3.25 × 10⁻⁵ | Table 2, p12; text p4 |
  | Cα-LDDT, Chai-1 with MSA | 0.915 (0.907–0.922) | LDDT (0–1) | Low-homology protein monomers, n = 271 clusters (447 monomers) | Table 2, p12 |
  | Cα-LDDT, Chai-1 single-sequence | 0.852 (0.834–0.867) | LDDT (0–1) | same, n = 271; worse than AF2.3, p = 4.46 × 10⁻¹⁶ | Table 2, p12; text p6 |
  | Cα-LDDT, AlphaFold-Multimer 2.3 | 0.903 (0.895–0.911) | LDDT (0–1) | same, n = 271; Chai-1 > AF2.3, p = 7.21 × 10⁻¹⁰ | Table 2, p12; text p6 |
  | LDDT, Chai-1 | 0.849 | LDDT (0–1) | CASP15 monomers, n = 69 (T1169 excluded) | p6 |
  | LDDT, AF2.3 | 0.843 | LDDT (0–1) | CASP15 monomers, n = 69 | p6 |
  | LDDT, AF2.3 (all targets, authors' reproduction) | 0.842 | LDDT (0–1) | CASP15 monomers, n = 70; vs 0.826 reported by Hayes et al. [21] | p10 |
  | LDDT, ESM3 98B (cited, not run) | 0.801 | LDDT (0–1) | CASP15 monomers, n = 70 | p6 |
  | LDDT, Chai-1 on AF2.3-hard subset | 0.643 | LDDT (0–1) | CASP15 targets with AF2.3 LDDT < 0.75, n = 14; p = 3.66 × 10⁻⁴ | p6 |
  | LDDT, AF2.3 on the same hard subset | 0.552 | LDDT (0–1) | same, n = 14 | p6 |
  | LDDT, AF3 on CASP15 RNA (cited, not run) | 0.473 | LDDT (0–1) | 8 of the CASP15 RNA targets | p6 |
  | Antibody–antigen DockQ acceptable, Blind (no constraints) | 35 | % of interfaces | Antibody–antigen subset, **n NOT REPORTED** | p5, Figure 4A |
  | Antibody–antigen DockQ acceptable, one contact restraint θ ≤ 15 Å | 57 | % of interfaces | same, **n NOT REPORTED** | p5, Figure 4A |
  | Antibody–antigen DockQ high-quality, all constraint settings | 4–8 | % of interfaces | same, **n NOT REPORTED** | p5 |
  | Example: DockQ improvement from epitope conditioning, PDB 7SYV | 0.10 → 0.81 | DockQ | single cherry-picked example | Figure 4B caption, p5 |
  | Server-vs-internal-pipeline agreement | µ = 0.345, σ = 0.150, all < 1 | Å RMSD | spot check on PoseBusters examples; server run without templates | p6–7 |
  | Interface LDDT / C1′-LDDT, Chai-1 vs RoseTTAFold2NA | **values NOT REPORTED numerically** — box medians only, roughly 0.57 / 0.66 / 0.37 for Chai-1 | LDDT (0–1) | protein–RNA n = 18, protein–DNA n = 26, CASP15 RNA n = 9 | Figure S3, p14; text p6 |
  | Runtime / wall-clock inference cost, either mode | **NOT REPORTED** | — | — | — |
  | Confidence calibration statistic (ρ, AUROC, ECE) | **NOT REPORTED** | — | — | — |

- **n_predictions**: **recorded at each level, as three separate numbers.**
  - **Samples per target (Chai-1)**: 25 — "4 recycles, 5 trunk samples and 5 diffusion samples for a
    total of 25 predicted structures unless otherwise noted" (p10), reduced to 1 reported structure
    by confidence ranking. This is the sampling default asked for.
  - **Samples per target (AF2.3 baseline)**: 25 — "3 recycles across 5 models and 5 seeds, and
    without relaxation. We use the top-ranked output across these 25 examples" (p10).
  - **Targets**: 427 (PoseBusters) + 1054 PDB complexes yielding 2362 interfaces / 929 clusters +
    447 monomers / 271 clusters + 69 CASP15 monomers + 9 CASP15 RNA + 18 protein–RNA + 26
    protein–DNA + the unsized antibody–antigen set × 5 constraint settings.
  - **Total predictions**: **NOT REPORTED**, and not reconstructible because the antibody–antigen set
    size is never given and it is unclear whether the Figure 4 constraint settings were run with 25
    samples each.
  - Also relevant: inference cap of 2048 tokens (p10); "For inference over the datasets in our main
    analysis … we additionally generated MSAs using jackhmmer with 3 iterations" (p10).
- **comparable_to_ours**: *(left empty by the extractor per schema v3)*
- **si_in_scope**: **SI IS HELD.** §6 Supplementary Information occupies p12–15 of the PDF and
  contains everything the text cites: Table 1 (PoseBusters success rates, p12), Table 2 (protein
  evaluation with 95% CIs, p12), Figure S1 (PoseBusters extended data, p13), Figure S2 (stricter
  DockQ cutoffs, p14), Figure S3 (nucleic acids, p14). **What is NOT held**: (a) the external
  PoseBusters prediction archive, p15 — "Predicted structures for the posebusters set are available at
  https://chaiassets.com/chai-1/paper/assets/posebusters_predictions.zip"; (b) **no per-target result
  table exists anywhere**, in the PDF or as a described supplement — every number is an aggregate
  across a benchmark; (c) the nucleic-acid results (Figure S3) are given only as boxplots, so no
  numeric iLDDT/C1′-LDDT value for either method is recoverable from this paper; (d) the exact
  membership lists of the low-homology evaluation sets are never provided, so §5.6's construction is
  described but not reproducible from the paper alone.

## F. Figures

License for every row: **CC-BY-NC 4.0 International**, stated in the banner on every page (p1–18).
Attribution and non-commercial use required; **no ND clause, so redrawing and adaptation are
permitted** for non-commercial purposes.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 2 | Chai-1 architecture and the optional input tracks: LM embeddings, templates, genetic search, wet-lab contacts from XL-MS or epitope mapping | schematic | `SCHEMATIC \| model architecture block diagram with optional input feature tracks feeding a trunk and diffusion module \| no data` | 1 | Caption asserts a "wide variety of optional input features" but the figure is the only architecture description in the paper — no layer counts, no dimensions, no parameter count anywhere in text or figure | CC-BY-NC 4.0, no ND (p2) |
| 2 | 3 | Headline result: success rate of Chai-1 vs four comparators across six benchmark tasks | bar | `PLOT \| facet: modality (2: Ligand PoseBusters set, Proteins) \| vary: benchmark task (6: PoseBusters ×3 method-specific groups, All protein-protein, Antibody-protein, Protein monomers) \| series: method (5: Chai-1, Chai-1 single-seq, AF2.3, AF3, RoseTTAFold All-Atom) \| measure: success (percent) — pocket-aligned ligand RMSD < 2 Å, DockQ > 0.23, or Cα-LDDT depending on task \| mark: bar \| n: n = 427 per PoseBusters mark, 929 / 121 / 271 clusters per protein mark; per-panel n as labelled on the axis` | 2 panels sharing one y-axis and one legend; panels vary by modality, not by method | **Three different metrics are stacked on one "Success (percent)" axis** — RMSD < 2 Å, DockQ > 0.23 and Cα-LDDT are not the same quantity and are only comparable by being 0–100. The left panel's series are exclusive (each method appears once, so the "series" is really the x-axis there) while the right panel's series are shared; the two halves therefore encode method differently. Cα-LDDT is a continuous mean shown as a "success percent" bar. **Bars hide distributions** throughout: only a mean and an error bar are drawn, though per-target LDDT and DockQ distributions exist and are shown as boxplots elsewhere (Fig S3). Significance is shown only as unlabelled horizontal bars with no p-values in the figure | CC-BY-NC 4.0, no ND (p3) |
| 3 | 4 | Manual inspection of a PoseBusters "failure": Chai-1's 7Q2B ligand sits deeper than the reference, which contains a blocking DMS molecule; two related structures without DMS bind deep | structure render | `RENDER \| facet: PDB entry (3: 7Q2B, 7Q2C, 7Q2F) \| views: 1 \| overlay: 1 prediction on 1 reference (7Q2B only; 7Q2C and 7Q2F show reference only) \| axis: none` | 3, varying by system | The argument is that a benchmark failure is a benchmark artefact, and it is made entirely from three hand-picked renders with **no quantitative panel at all** — no count of how many PoseBusters targets contain crystallization aids, no re-scored success rate with such cases excluded. One RMSD (1.73 Å) is quoted in the caption | CC-BY-NC 4.0, no ND (p4) |
| 4A | 5 | DockQ success at three quality tiers for antibody–antigen interfaces under five restraint conditions | bar | `PLOT \| facet: none (1) \| vary: DockQ quality tier (3: acceptable, medium, high) \| series: restraint condition (5: Blind, One Contact 15 Å, One Contact 25 Å, One Epitope 8 Å, Four Epitope 8 Å) \| measure: DockQ success rate \| mark: bar \| n: NOT REPORTED per mark and per panel` | 1 | **n is never given** for the antibody–antigen set, in the caption or the text — the one evaluation set in the paper whose size is unstated. Bars hide distributions; error bars not described in the caption. The three tiers are nested subsets of the same predictions, so the three groups are not independent | CC-BY-NC 4.0, no ND (p5) |
| 4B | 5 | Two renders of PDB 7SYV predicted with and without epitope pocket restraints, against the reference | structure render | `RENDER \| facet: restraint condition (2: without epitope residues, with epitope residues) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 2, varying by condition | Caption states these are **"Cherry-picked example predictions"** — the authors' own word — and quotes a 0.10 → 0.81 DockQ jump that is by construction the most favourable case available | CC-BY-NC 4.0, no ND (p5) |
| 5A-B | 7 | DockQ against binned chain-pair ipTM, for protein–protein and for protein–nucleic-acid interfaces: the confidence-calibration evidence | box | `PLOT \| facet: interaction type (2: protein-protein, protein-nucleic acid) \| vary: chain-pair ipTM bin (binned, 0–1) \| series: none (1) \| measure: DockQ \| mark: box \| n: NOT REPORTED per box and per panel` | 2 panels, varying by interaction type; same mark and measure, so one row | **No n per bin**, so a bin containing three interfaces looks like one containing three hundred. **No calibration statistic** accompanies the "well calibrated" and "strong discriminator" claims (p6). The caption also contains a self-contradiction about homology filtering: "we show results for all interfaces in our low homology subset, and do not restrict only to interfaces with low homology" | CC-BY-NC 4.0, no ND (p7) |
| 5C | 7 | Pocket RMSD against binned chain-pair ipTM for protein–ligand interfaces | scatter (swarm) | `PLOT \| facet: none (1) \| vary: chain-pair ipTM bin (binned, 0–1) \| series: none (1) \| measure: pocket-aligned ligand RMSD (Å) \| mark: point \| n: 1 per mark, per panel NOT REPORTED and explicitly subsampled — "Dots show ligand RMSD, sampled down to 5% of the overall data"` | 1 | **The plotted cloud is a 5% subsample and the caption says so**, so visual density carries no information about how many points sit in each bin; combined with the absent per-bin n this makes the panel unquantified. Ions and bonded ligands are excluded without a count of how many that removed | CC-BY-NC 4.0, no ND (p7) |
| 6 | 7 | Three Chai-1 lab-server predictions of post-cutoff therapeutically relevant complexes (7VLH Zika NS2B-NS3 protease + inhibitor, 7MB4 SARS-CoV-2 protease + NSP fragment, 7WVM PD-1 + cemiplimab) overlaid on their references | structure render | `RENDER \| facet: complex (3: 7VLH, 7MB4, 7WVM) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 3, varying by system | Examples were "chosen to emphasize potentially therapeutically relevant structures" (p7) with no stated selection protocol; RMSD values are printed under each panel but there is no distribution, no n, and no comparator — a showcase, not a result | CC-BY-NC 4.0, no ND (p7) |
| S1A | 13 | PoseBusters chemical-validity checks: Chai-1 vs AF3 across 18 criteria | bar | `PLOT \| facet: none (1) \| vary: PoseBusters validity criterion (18: file loads, sanitization, molecular formula, bonds, tetrahedral chirality, double bond stereochemistry, bond lengths, bond angles, planar aromatic rings, planar double bonds, internal steric clash, energy ratio, minimum protein/ligand distance, minimum distance to organic cofactors, minimum distance to inorganic cofactors, volume overlap with proteins, volume overlap with organic cofactors, volume overlap with inorganic cofactors) \| series: method (2: Chai-1, AF3) \| measure: success rate (0–1) \| mark: bar \| n: 427 per mark; 427 per panel` | 1 | **The whole panel is at ceiling** — every criterion sits at or just below 1.0 for both methods, so 16 of 18 criteria carry no information and the two that do (tetrahedral chirality, volume overlap with proteins) are compressed into the top 12% of the axis. No error bars. Cross-reference `metric_saturation` | CC-BY-NC 4.0, no ND (p13) |
| S1B | 13 | Cumulative success rate as a function of the ligand-RMSD threshold, for four ranking regimes | line | `PLOT \| facet: none (1) \| vary: pocket-aligned ligand RMSD threshold, 0–10 Å (continuous) \| series: ranking regime (4: Chai-1 confidence ranked, AF3 confidence ranked, Chai-1 random, Chai-1 oracle) \| measure: cumulative success rate (0–1) \| mark: line \| n: 427 targets per line; "Chai-1 random takes the mean over the aforementioend 25 samples", "Chai-1 oracle takes the best (lowest ligand RMSD) prediction after comparing all 25 examples to the ground truth"` | 1 | Nothing hidden — this is the most honest panel in the paper: it shows the oracle ceiling and the random floor alongside the reported number, and makes the 2 Å threshold's arbitrariness visible. No confidence bands on the curves | CC-BY-NC 4.0, no ND (p13) |
| S1C | 13 | Ligand RMSD distribution against binned ligand ipTM on PoseBusters — the confidence-calibration evidence for ligands | box (with outlier points) | `PLOT \| facet: none (1) \| vary: ligand ipTM bin (5: (0.0,0.2], (0.2,0.4], (0.4,0.6], (0.6,0.8], (0.8,1.0]) \| series: none (1) \| measure: ligand RMSD (Å) \| mark: box \| n: NOT REPORTED per box; 427 per panel` | 1 | **No n per bin.** The y-axis is clipped at 20 Å, so any prediction worse than that is silently pulled to the edge or dropped — the caption does not say which | CC-BY-NC 4.0, no ND (p13) |
| S2 | 14 | DockQ success at three increasingly strict cutoffs, Chai-1 vs Chai-1 single-seq vs AF2.3, on two interface sets | bar | `PLOT \| facet: DockQ cutoff (3: ≥ 0.23 acceptable, ≥ 0.49 medium, ≥ 0.8 high) \| vary: evaluation set (2: All protein-protein n = 929, Antibody-protein n = 121) \| series: method (3: Chai-1, Chai-1 single-seq, AF2.3) \| measure: DockQ success rate \| mark: bar \| n: 929 and 121 clusters per mark; 1050 per panel` | 3, varying by cutoff; same mark and measure so one row | **Each panel has its own unlabelled y-scale** (the high-quality panel tops out near 0.35 while the acceptable panel reaches 0.8), so the visual impression of the lead is not comparable across panels. Bars hide distributions; significance shown as unlabelled horizontal bars with no p-values | CC-BY-NC 4.0, no ND (p14) |
| S3 | 14 | Chai-1 vs RoseTTAFold2NA on nucleic-acid complexes and RNA monomers | box | `PLOT \| facet: none (1) \| vary: evaluation set (3: Protein-RNA n = 18, Protein-DNA n = 26, CASP15 RNA n = 9) \| series: method (2: Chai-1, RoseTTAFold2NA) \| measure: success — interface LDDT for protein–nucleic-acid, C1′-LDDT for RNA \| mark: box \| n: 18 / 26 / 9 targets per mark, but the boxes are drawn over 10,000 bootstrap resamples, not over targets` | 1 | **The boxes are bootstrap distributions of the mean, not distributions over targets** ("Boxes indicate the inter-quartile range across 10,000 bootstrap samples"), so the visible spread is sampling error and looks far tighter than the per-target variation. Two different metrics (iLDDT and C1′-LDDT) share one "Success" axis. n = 9 for CASP15 RNA is **underpowered** and no p-value is given for any comparison in this figure | CC-BY-NC 4.0, no ND (p14) |

**13 panel-group rows across 9 figures** (Figures 1–6 and S1–S3). Two figures split: Figure 4 into
4A (bar) and 4B (render) on differing mark; Figure 5 into 5A-B (box, DockQ) and 5C (point, RMSD) on
differing mark and measure. Figure 5A and 5B are one row because only `facet` differs. Figure S2's
three panels are one row for the same reason. Three pages (3, 13, 14) were rendered as PNGs to
recover panel structure that the text layer had mangled into cipher-like glyphs; all three were
deleted after reading.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), single-paper extraction against SCHEMA.md v3
- **schema_version**: v3
- **confidence**: **high** for A, B, D, E, the training-cutoff block, the MSA-free block and the
  confidence-metric block — all of these are stated plainly in the text and quoted verbatim here.
  **Medium** for F, because the PDF's text layer renders every figure's in-panel labels as a
  substitution cipher (axis labels came out as strings like `< $ $ ' 9 9 l 6 ' 8 $ ' 2 ; m` for
  "Success (percent)"), so panel structure for Figures 2, S2 and S3 was recovered from page renders
  rather than from extractable text; Figures 4, 5 and 6 were filled from their captions alone.
  **Medium-low** for the training-detail portions of `structural_priors_used`, not because the
  reading was hard but because the paper genuinely does not report them.
- **unresolved**:
  1. **Antibody–protein n is 122 in the text and 121 in two figures.** p4 says "268 interfaces across
     129 structures, forming 122 redundancy reduced clusters"; Figures 2 (p3) and S2 (p14) both label
     the axis n = 121. Table 2 gives no n. Which is right is not determinable from the PDF.
  2. **Figure 5's caption contradicts itself on homology filtering** (p7): "we show results for all
     interfaces in our low homology subset, and do not restrict only to interfaces with low
     homology." If the second clause governs, the confidence-calibration analysis includes
     training-homologous interfaces and the calibration claim is weaker than it appears.
  3. **The antibody–antigen evaluation set (Figure 4) has no stated size.** It is described only as
     differing from the antibody–protein set and as counting each antibody/antigen copy in a PDB
     separately (p5). Every Figure 4 percentage is therefore unpowered as far as this PDF can tell.
  4. **The confidence model is never described.** p10 promises "A confidence model is then used for
     ranking (details below)" and no such details appear anywhere in the paper. Its architecture,
     training data, training objective and full output set are unknown; only ipTM and ligand
     interface pTM are named as outputs.
  5. **No parameter count, no training-set size, no training-step count** for Chai-1 (only 128 A100s
     × batch 128 × 30 days, p9). The 3B figure on p9 is the *language model's* size, not Chai-1's.
  6. **AFDB and genetic-database vintages are not dated.** The 2021-01-12 cutoff is stated for PDB and
     PDB70 only; AFDB has no stated cutoff and sequence databases are deferred to reference [6]
     (p9–10). This limits how cleanly the single cutoff date characterises the model.
  7. **Two dates on p1** — bioRxiv "this version posted October 15, 2024" versus the paper's own
     "Date: September 9, 2024". Both recorded in `year`; the citekey's 2024 is unaffected.
  8. **Nucleic-acid numbers exist only as boxplots** (Figure S3, p14). No iLDDT or C1′-LDDT value is
     printed anywhere for Chai-1 or RoseTTAFold2NA, so the "similar performance" claim on p6 cannot
     be quantified from this paper.
  9. **No version-2 changelog inside the PDF.** The task brief identifies this as bioRxiv v2; the
     document itself carries no revision note, so nothing here can be attributed to the revision.
  10. **Tag needed but unavailable (reported, not invented):** there is no Control-vocabulary tag for
      **restraint / constraint prompting** — Chai-1's pocket, contact and docking distance features,
      the paper's single most distinctive control handle and the mechanism behind its double-digit
      antibody–antigen gains. The nearest existing tags are wrong: `directed-state` means directing a
      *conformational state*, which these features do not do; `partner-driven`, `ligand-driven`,
      `peptide-driven` and `nanobody` all name a molecular partner rather than a geometric restraint;
      `state-annotated-input` is about state annotations. I have therefore applied **no Control tag**
      rather than mis-tagging. Suggested addition to the v3 vocabulary under **Control**:
      `restraint-prompted` (or `distance-restraint`), covering inference-time pocket/contact/distance
      conditioning as introduced by Chai-1 and now common in AF3-family models.
  11. **Second tag gap, lower priority:** there is no **Utility** or **Method** tag marking a model
      whose *weights are publicly released*, which is the single most consequential property of this
      paper for anyone building on it. `benchmark-only` is the opposite of what Chai-1 is, and no
      openness tag exists. Suggested: `open-weights`.
  12. **Schema ambiguity in v3, reported bluntly:**
      - **`states_generated` has no clean answer for a co-folding model that draws k samples and
        confidence-ranks them.** The field's dual form ("ensemble + single-state") was written for
        methods that *sample broadly and collapse*, and Chai-1's 25 samples are seed variation for
        ranking, not conformational exploration. I wrote `one`, but the schema gives no way to
        distinguish "produced 1 structure" from "produced 25 near-identical structures and reported
        the best-ranked", and that distinction matters for every co-folding paper the corpus will
        hold. Suggest a note that k-sample-then-rank is `one`, with k recorded in `n_predictions`.
      - **`oracle_leakage` has no way to mark a route as "present, but in a clearly labelled
        non-headline arm".** For this paper routes 1, 5, 6 and 7 are all technically present and all
        confined to arms the authors themselves flag as leaky (docking, constraints, oracle curve,
        cherry-picked renders), while the headline numbers are blind. Writing "PRESENT" without
        qualification would badly misrepresent the paper; writing "NONE FOUND" would be false. I
        qualified in prose, but a per-route `arm:` sub-slot (headline / ablation / demonstration)
        would make this machine-readable rather than dependent on the reader reading the paragraph.
      - **`metric_saturation` says "numeric only" but does not say whether a *threshold* metric that
        cannot exceed 1.0 counts as saturating when no arm approaches 1.0.** I recorded only the
        genuine ceiling (Figure S1A) and noted the threshold metrics separately.
      - **`si_in_scope` conflates two different absences**: SI that exists but is not held, and
        per-target data that was never published in any form. This paper is the second case, which is
        worse for reuse and currently indistinguishable in the field.
      - **The Figure-2 case where one panel's `series` is another panel's `vary`.** In Figure 2's left
        panel each method appears once so method *is* the x-axis; in the right panel method is the
        legend dimension. The grammar assumes one role assignment per row, and the panel-split rule
        forbids splitting on facet alone. I filled both slots and explained in `hides`, but the
        grammar has no clean way to say "role assignment differs between facets".
- **why_it_matters**: *(left empty by the extractor per schema v3)*

## Tags

`general-protein` `cofolding` `no-template-no-msa` `templates-on` `single-state` `binary-predicate`
`continuous-metric` `saturating-metric` `anti-memorization` `confidence-as-discriminator`
`multi-backbone` `oracle-leak` `design-level-oracle` `preprint` `precedent` `background`
`comparator-numbers`

Tag notes, so the reverse lookups are not misread:

- **`oracle-leak` is applied for the non-headline arms only** — the PoseBusters docking arm (apo
  receptor supplied, p3), the Figure 4 restraint arms (restraints sampled from the solved complex,
  p5), the "Chai-1 oracle" curve (best-of-25 against ground truth, p13) and the 2048-token crop
  centred on the known binding site (p3). **Every headline number in Table 1 and Table 2 is blind.**
  A query returning this paper for `oracle-leak` should read `oracle_leakage` before drawing a
  conclusion.
- **`design-level-oracle`** covers route 7: the restraint conditions and the hand-selected showcase
  structures declare the expected answer before the result is read.
- **`no-template-no-msa` and `templates-on` are both applied** because both regimes are run and
  reported head to head (Table 2, p12) — this is not a contradiction but the paper's central
  ablation.
- **`anti-memorization` is applied on the design** (2021-01-12 cutoff, 40% homology filter, temporal
  split 2022-05-01 to 2023-01-12); note in `anti_memorization_control` that **no dedicated control
  arm was run** to measure what the filter cost.
- **`saturating-metric`** refers specifically to Figure S1A's chemistry checks, which sit at ceiling
  for both methods.
- **No Control tag applied** — see `unresolved` item 10.
- **Not applied and why**: `msa-subsample` (depth is never reduced, only removed entirely — the
  schema explicitly warns these are different things), `msa-state-filter`, `template-state-bias`,
  `latent-steering`, `md`, `md-emulator`, `enhanced-sampling`, `af-cluster`, `benchmark-only`
  (Chai-1 is the paper's own model), `experimental`, `experimental-validation` (no wet-lab work),
  `prospective` (retrospective throughout), `rmsd-only` (LDDT and DockQ are also used),
  `visual-metric` (Figures 3, 4B and 6 are visual, but every reported *metric* is operationalised),
  `unpowered` (the main sets are large; the unsized antibody–antigen set is flagged in prose
  instead), `two-state` / `ensemble` / `continuum`, every Site tag, `gpcr` / `kinase` / `transporter`
  / `periplasmic-binding` / `atpase` / `fold-switching`, `peer-reviewed`, `contrast`, `threat`,
  `negative-result`, `figure-exemplar`.
