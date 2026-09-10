# lee2026confornets

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–26)**, which coincide with the
printed page numbers of the arXiv preprint. Structure: p1–p9 main text (Abstract, Intro, Related
Work, Method, Unsupervised Prediction, Supervised Transfer, Discussion, Conclusion), p10–p12
references, p13–p26 appendices A–H. Figures 1–6 on p4, p6, p7, p7, p8, p8. Tables 1–3 on p6, p8, p9.
Appendix figures A1–A11 and Tables A1–A11 on p14–p26.

**Text-layer caveat:** footnote markers are glued to the preceding token. `k = 21` on p4 is
`k = 2` plus footnote 1; `flip3` on p8 is `flip` plus footnote 3; `TM1-H8` and `4-5Å` are en-dashes.
Verbatim quotes below reproduce the text layer, with `[sic]` or a bracketed note where the glue
changes the meaning.

**Two-task caveat, recorded up front because it governs sections C and E.** This paper contains
**two separate methods evaluated on two separate benchmark suites**, and almost every field below is
dual as a result:

| | Task 1 — unsupervised diverse prediction | Task 2 — supervised conformation transfer |
|---|---|---|
| what is optimised | k=2 ConforNets jointly, per input protein, at inference | 1 ConforNet on **one source protein**, then reused |
| objective | maximise pairwise distance between the k samples | MSE to a **deposited reference structure** of the desired state |
| training label | none (unsupervised) | a solved structure of the target state |
| directional? | **no** — diversity only | **yes** |
| benchmark suite | 104 proteins / 208 structures, 6 groups | 86 proteins, 3 families |
| section / tables | Sec. 4, Table 1 (p6) | Sec. 5, Table 2 (p8) |

Conflating these two is the single easiest way to mis-cite this paper.

---

## A. Identity

- **citekey**: `lee2026confornets`
- **doi**: **arXiv:2604.18559v1 [q-bio.BM]** — p1, stamped in the left margin: "arXiv:2604.18559v1
  [q-bio.BM] 20 Apr 2026". `refs.bib` records `doi = {10.48550/arXiv.2604.18559}`, the arXiv DOI.
  No journal DOI exists in the PDF.
- **year**: **2026.** p1: "Preprint. April 21, 2026." arXiv stamp date 20 Apr 2026.
- **venue**: **arXiv preprint, not peer reviewed.** p1: "Preprint. April 21, 2026." Formatted in the
  ICML/JMLR two-column style (it carries an "Impact Statement" section, p10, which is an ICML
  requirement), but **no conference or journal is named anywhere in the PDF**. Tagged `preprint`.
- **title**: ConforNets: Latents-Based Conformational Control in OpenFold3 — p1
- **authors**: Minji Lee, Colin Kalicki, Minkyu Jeon, Aymen Qabel, Alisia Fadini, Mohammed
  AlQuraishi — p1. Affiliations: Dept. of Computer Science, Columbia (1); Dept. of Systems Biology,
  Columbia (2); Dept. of Computer Science, Princeton (3). Correspondence: Alisia Fadini
  (af3659@cumc.columbia.edu) and Mohammed AlQuraishi (m.alquraishi@columbia.edu). This is the
  AlQuraishi lab, i.e. **the group that produces OpenFold/OpenFold3**, which is the chassis used
  (p2: "OpenFold3-preview (OF3p) (The OpenFold3 Team, 2025), an open-source reproduction of
  AlphaFold3").

## B. Scope

- **system**: **multi-system.** GPCR + kinase + transporter + fold-switching + general protein, in
  two distinct suites. Sec. 4 (unsupervised) covers domain motions, membrane transporters, cryptic
  pockets, fold switchers and a general post-cutoff set (p5). Sec. 5 (transfer) covers exactly the
  three families this corpus cares about: GPCR active, kinase DFG-out, transporter outward-open
  (p7). Motivation, p2: "Many proteins undergo conformational changes that are conserved across
  their families, such as activation of GPCRs or the DFG-in/out transition of kinases, both common
  drug targets."

- **n_targets**: **175 unique proteins across the two suites** (104 + 51 + 20; the 15 transporters
  in the transfer suite are the *same* 15 as in the multi-state suite and are not double-counted).
  The counts below are the ones prior corpus notes have confused, so they are given in full with
  the distinction between **proteins** and **reference states** made explicit.

  **Benchmark inventory — the definitive table.**

  | Suite | Benchmark | n proteins (Sec. text) | N in the tables | what the table N counts | page |
  |---|---|---|---|---|---|
  | Multi-state (Sec. 4) | Domain motions | 21 | 42 | reference states (2 per protein) | p5, p6 |
  | Multi-state | Membrane transporters | 15 | 30 | reference states | p5, p6 |
  | Multi-state | Cryptic pockets | 34 | 34 (apo) **and** 34 (holo), reported as two rows | proteins, one row per state | p5, p6 |
  | Multi-state | Fold switchers | 15 | 30 | reference states | p5, p6 |
  | Multi-state | OOD60 | 19 | 38 | reference states | p5, p6 |
  | Multi-state | **suite total** | **104 proteins / 208 structures** | — | — | p5 |
  | Transfer (Sec. 5) | GPCR active | 51 pairs | 51 | proteins (pairs); 50 scored as targets | p7, p15 |
  | Transfer | Kinase DFG-out | 20 pairs | 20 | proteins (pairs); 19 scored as targets | p7, p15 |
  | Transfer | Transporter outward-open | 15 | 15 | proteins; 14 scored as targets — **reused from Sec. 4.1** | p7 |
  | Transfer | **suite total** | **86 proteins, 83 scored targets** | — | — | p7 |

  The `N` column of Tables 1, A2, A3, A4, A6 is **not** a protein count except for cryptic pockets.
  21×2=42, 15×2=30, 19×2=38, 15×2=30; cryptic pockets are split into two 34-row entries instead.
  Sec. 4.1 states the protein counts directly (p5): "Domain motions (N=21)", "Membrane transporters
  (N=15)", "Cryptic pockets (N=34)", "Fold switchers (N=15)", "OOD60 (N=19)", against the suite
  header "comprising 104 proteins with two distinct and experimentally determined conformations
  (208 structures in total)" (p5). 21+15+34+15+19 = 104. ✓

  Sub-counts inside the kinase set, p8 footnote 3 and p15: "Of the 20 kinases in the benchmark, only
  11 have experimentally resolved A-loop flips between the pairs (App. D.2)." The 11 are named on
  p15: ABL1, AKT1, AKT2, CDK2, CDK4, CDK7, ERBB2_ErbB2, MAP4K1_HPK1, MET, TNIK, ULK3. The kinase set
  was filtered down from 42: p15, "yielding 42 candidate kinase pairs... yielding 20 pairs."

  Transfer targets exclude the source, p7: "The benchmark transfer success rate is the average
  across all target proteins in the benchmark (excludes the source protein used in training the
  ConforNet)." Fig. 6 (p8) confirms 19 named kinase bars plus an "Avg" bar.

  **Generality flag:** the paper does *not* over-claim from one system — it runs six multi-state
  groups and three transfer families. But the transfer claim rests on **three ConforNets, one per
  family**, each trained on a **single** source protein (p7: "we choose as the source protein the
  family centroid"). The generality of *transfer itself* rests on n=3 source proteins.

- **method_class**: **other — inference-time latent steering.** A learned channel-wise affine
  transform of the pre-Pairformer pair representation of an AF3-architecture model. It is not
  co-folding, not MSA manipulation, not template biasing, not MD, not clustering. p1 abstract: "We
  distill our findings in ConforNets: channel-wise affine transforms of the pre-Pairformer pair
  latents." p4: "We formulate a ConforNet φ that adapts a latent h with channel dimension c (e.g.,
  c_z = 128 for pair latents) as an affine transform φ(h) = hW^T + b, with trainable parameters
  W ∈ R^{c×c} and b ∈ R^c. ConforNets are initialized to the identity (W = I, b = 0)."
  Self-positioned against MSA and template methods, p2: "Unlike existing perturbational methods,
  which operate residue-wise and are thus protein-specific, ConforNets are channel-wise affine
  transforms. They modulate AF3's latents globally and permit reuse across different proteins."
  Also positioned against diffusion guidance, p3: "ConforMix operates on AF3's diffusion module
  while ConforNets intervene upstream, in the Pairformer, via channel-wise transforms."
  **Re-implemented baseline arms belong to other classes** and are run inside this paper: shallow
  MSA subsampling, AFsample3 MSA column masking, ConforMix diffusion guidance, entropy guidance, and
  a state-annotated template arm.

- **backbones**: **OpenFold3-preview (OF3p) as the sole working chassis**, plus a single-seed
  **AF3 server** sanity check and **BioEmu** as an external comparator model.
  - p2: "ConforNets are broadly applicable to all AF3-based models, and we use OpenFold3-preview
    (OF3p) (The OpenFold3 Team, 2025), an open-source reproduction of AlphaFold3 and its associated
    pretrained weights, as our implementation chassis."
  - All competing methods were re-implemented on OF3p, p5: "We (re)implement shallow MSA subsampling
    (Lee et al., 2025), ConforMix (Richman et al., 2025), AFsample3 (Kalakoti & Wallner, 2026), and
    entropy guidance (Wu & Feng, 2025) under a common OF3p framework for fair comparison."
  - AF3 server, p16 (App. E.1): "we ran one AF3 seed (5 diffusion rollouts) using the AF3 server and
    report success@5 for both models. Because of the limited API quota, we cannot compute
    bootstrapped standard deviations for AF3. Accordingly, Table A2 and Fig. A1 should be
    interpreted only as a sanity check that OF3p performs similarly to AF3, rather than as evidence
    that OF3p outperforms AF3."
  - BioEmu v1.2 (p5) is an MD-trained generative model, not an AF backbone.
  - **`multi-backbone` NOT tagged.** Only OF3p carries the method; AF3 was one unbootstrapped
    server run explicitly disclaimed as a sanity check; BioEmu is not an AF3-family backbone. This
    is not "more than two compared head to head".

- **templates**: **OFF for every main experiment; ON for exactly one baseline arm.**
  - Off, p13 (App. B, Inputs): "**We did not provide the templates, as they would bias structure
    prediction.**"
  - On for one comparator, p7: "As baselines, we ran default OF3p, **OF3p with the centroid
    protein's desired conformation provided as a template**, and AFsample3, each with 20 random
    seeds, as well as ConforMix with 1 seed."
  - Result of that arm, p8 (Table 2, "Template" row): 14.9±3.0% GPCR, 6.4±2.6% kinase, 15.7±6.6%
    transporter at success@5 — i.e. **worse than plain OF3p on GPCRs (24.3%)**. p8: "Supplying the
    desired conformation of the centroid protein as a template does not improve performance."
  - This is a rare and directly citable negative result on template state-biasing, run under a
    controlled comparison against a latent method.

- **msa_handling**: **full-ish (subsampled to 1,024 rows, OF3p default) for the method; explicitly
  shallow-subsampled (8 rows) only for the re-implemented baseline.** The two are kept apart by the
  paper itself.
  - p5: "We provide as input MSAs generated from the ColabFold (Mirdita et al., 2022) server without
    templates or ligands (App. B). Following standard OF3p inference, we subsample MSAs to a maximum
    of 1,024 rows per recycle, **except for shallow MSA subsampling, when we subsample to 8 rows**."
  - MSA resampling is used as a *regulariser during ConforNet optimisation*, p5: "At each step,
    s_pre and z_pre are recomputed from different MSA subsamples, preserving the stochasticity of
    OF3p inference and promoting robustness in the learned ConforNets."
  - Not clustered, not state-filtered. There is no MSA-state-filtering anywhere. The paper's whole
    argument is that MSA-space perturbation is the wrong place to intervene, p3: "these methods must
    contend with a vast combinatorial space of MSA perturbations—**without a mechanism to specify
    the type or magnitude of induced conformational change**—and with their effectiveness being
    contingent on the depth and diversity of the starting MSA."
  - Sequence handling where the two reference structures differ, p13: "Following BioEmu, when the
    sequences of two reference structures differ, we sample both sequences in equal proportion.
    However, for OOD60 we observed that the mismatch was primarily due to His-tags and therefore
    sampled only the de-tagged sequence."

## C. Conformational core

- **states_generated**: **`ensemble + one` — genuinely dual, and the split is exactly the two tasks.**
  - *Task 1 (unsupervised)* produces an **ensemble**: 800 samples per target, from which an empirical
    free-energy landscape is estimated (Fig. 2b, 3b, 4). But the ensemble is deliberately shaped to
    **two** modes: p4 footnote 1, "We focus on k = 2 because all benchmarks considered in this work
    contain only two reference conformational states." So it is an ensemble whose k is set to the
    number of states the evaluation set is known to have.
  - *Task 2 (transfer)* produces effectively **one** state — it collapses the distribution onto the
    induced state. Fig. 4 caption, p7: "ConforNets shift the sampling probabilities of the active
    states of both GPCRs to over 80% and **rarely sample their inactive states**." For AA1R the
    inactive fraction goes 100% → 1%, and the active 0% → 88%; for CNR1 inactive 27% → 0%, active
    35% → 80% (Fig. 4, p7).
  - The ensemble is **not calibrated** and the authors say so, p6: "While we do not expect ConforNets
    to be energetically calibrated..." and "Nonetheless, the sampled empirical free energy landscape
    is clearly not calibrated."

- **structural_priors_used**: **Extensive, at design time, and largely legitimate — but it is the
  same knowledge that route 1/2/3 of `oracle_leakage` then re-uses at pipeline time.** Recorded here
  separately as the schema requires.
  1. **Both states of every benchmark protein are deposited by construction.** p5: "a broad suite of
     multi-state benchmarks... comprising 104 proteins with **two distinct and experimentally
     determined conformations** (208 structures in total)."
  2. **The transfer benchmarks were built from state-annotated structural databases.** p15 (App.
     D.1): "The GPCR benchmark was constructed from the GPCRdb structure database (Munk et al.,
     2016). We selected GPCRs with both **fully active (100% activation degree) and inactive
     structures available**. We selected pairs with the fewest engineered mutations and highest
     crystallographic resolution, retaining 51 pairs where both structures contained at most one
     mutation." p15 (App. D.2): "The kinase benchmark dataset was constructed from the KLIFS database
     (Kanev et al., 2021). We selected kinase families with **matching active or inactive state
     annotations at both the DFG site and the AC-helix**."
  3. **The scored region is defined from prior structural knowledge of the conformational change.**
     p7: "compute RMSD of TM6 to its undersampled active state"; "compute RMSD of the activation loop
     and DFG motif"; p15: "Per-residue segment annotations (TM1-H8) were retrieved from the GPCRdb
     API"; "All metrics for kinases were scored over the DFG site and A-loop."
  4. **Reference structures shape the input preprocessing.** p15: "Inactive structures were further
     post-processed to remove ICL3 and any fusion proteins inserted, as well as helix 8."
  5. **The k of the diversity objective is set from prior knowledge of the number of states.** p4
     footnote 1 (quoted above).
  6. The interpretability case study was chosen for its known, localised change, p25 (App. H): "We
     selected this example because the conformational difference is localized and easily structurally
     interpretable."
  None of 1–6 is a methodological sin on its own. They become one where the same structure is fed
  back into the pipeline, which is what the next field records.

- **oracle_leakage**: **PRESENT AND SUBSTANTIAL — and, uniquely in this corpus so far, it enters
  through a supervised training label, not only through evaluation.** All seven routes below.

  > **Headline.** In the transfer task the ConforNet is trained by **regressing directly onto a
  > deposited structure of the desired conformational state** of a source protein in the same
  > family. p5, Sec. 3.2.2, verbatim: "**Given a source protein x with a desired reference
  > conformation X_ref, we optimize a ConforNet φ so that the one-step deterministic diffusion
  > sample X̂_φ from adapted representation φ(z_pre) reconstructs the reference by minimizing
  > L_transfer = MSE(Align(X̂_φ), X_ref)**". The control handle *is* an oracle structure. This is not
  > a defect the authors hide — it is the stated design — but it is the fact that makes ConforNets a
  > different kind of claim from any sampling-only method.

  **Route 1 — deposited structures used as input or template.** **PRESENT, in two forms; and
  explicitly ABSENT in a third.**
  - *As a supervised training target (transfer):* the L_transfer quote above, p5. The source
    protein's solved structure in the desired state is the optimisation target. The PDB IDs are
    shown: source 8YN2;R (GPCR active), source 6QV1;B (transporter outward), Fig. 5 (p8).
  - *As a supervised training target in the perturbation-location study:* p9, "For each latent, we
    optimized 4 ConforNets for the ground truth entries of OOD60 (N = 19×2) using L_transfer and
    R = 1"; Table 3 caption, p9: "**ConforNets are trained directly to ground truths** using K = 1
    mini rollouts." The entire architecture-siting decision (z_pre vs z_post vs s_pre vs s_post) was
    made by fitting to the ground truths of an evaluation benchmark. See also route 4.
  - *As a template:* **NONE for the main pipeline** — p13: "We did not provide the templates, as they
    would bias structure prediction." **PRESENT for one comparator arm** — p7: "OF3p with the centroid
    protein's desired conformation provided as a template". That arm is labelled and reported
    separately, so it is disclosed, not leaked.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates
  or alignments.** **PRESENT.** GPCRdb and KLIFS annotations do not drive an MSA or a template here,
  but they drive something with more leverage: **which deposited structure becomes the ConforNet's
  training label, and which region is scored.**
  - p7: "We curate 51 receptors (App. D.1) with experimental inactive and active structures from
    **GPCRdb** (Kooistra et al., 2021) and compute RMSD of TM6 to its undersampled active state."
  - p7: "We curate 20 kinase DFG-in/out pairs (App. D.2) from **KLIFS** (Kanev et al., 2021) and
    compute RMSD of the activation loop and DFG motif to their undersampled inactive state."
  - p15: "We selected GPCRs with both fully active (**100% activation degree**) and inactive
    structures available" — the GPCRdb activation-degree annotation is the selection criterion.
  - Kincore is not used. Alignment to the GPCRdb canonical 7TM sequence is used for trimming, p15:
    "the canonical 7TM subsequence—spanning TM1 through TM7 including intracellular and extracellular
    loops—was used as the query sequence for each receptor... each chain was trimmed to the 7TM
    domain by global pairwise sequence alignment to the canonical sequence."

  **Route 3 — cluster labels derived from known states.** **NONE FOUND** in the MSA-clustering
  sense — there is no MSA clustering anywhere in this paper (contrast AF-cluster, which is only
  cited as related work, p3). Protocol described on p5 (Sec. 4.2, Experimental design) and p13
  (App. B).
  *However*, the nearest analogue **is present**: the k=2 ConforNets in the diversity task are
  post-hoc **assigned** to states by RMSD to each reference, and the number of them is set to the
  known number of states (p4 footnote 1). In App. H the two learned ConforNets are named after the
  states they happen to induce, p25: "We denote the two learned ConforNets φ_H and φ_C, **as they
  induce predictions close to the H and C conformations**, respectively." That labelling is done
  against the reference structures. It is a labelling-after-the-fact, i.e. route 6, not route 3.

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.**
  **PRESENT, in four distinct places. This is the most under-flagged leakage in the paper.**
  1. **The perturbation location — the paper's central architectural claim — was selected by fitting
     to benchmark ground truths.** p9: "For each latent, we optimized 4 ConforNets for the ground
     truth entries of OOD60 (N = 19×2) using L_transfer... We used this setup **not to transfer
     states, but to determine whether a given latent provides sufficient conformational control to
     induce a state that is directly optimized for**." OOD60 is then reported as an evaluation
     benchmark in Table 1 (p6) and Table A6 (p19). The set used to pick where to intervene is a set
     the method is later scored on.
  2. **Recycle count selected per benchmark, post hoc, from the results.** p5: "We consider two
     recycling settings: R = 11 passes (10 recycles) and R = 1 passes (no recycles). **In Table 1,
     we report the better of R = 11 or R = 1 for all methods**, as some tasks benefit from fewer
     recycles (we consider this part of the fixed sampling budget)." Applied to every method
     symmetrically, and Tables A3/A4 (p17, p18) give the fixed-R numbers so the effect is checkable
     — but the headline Table 1 is a per-benchmark best-of-two. The effect is not small: ConforNets
     membrane transporters go 51.1% (R=1) → 42.7% (R=11) for Ours-dist, and AFsample3 goes 32.4%
     (R=1) → 46.9% (R=11); Table 1 takes 51.1% and 46.9% from different rows.
  3. **The optimisation-step sweep is a range tuned to the evaluation set — the exact case the v3
     schema calls out.** p5: "For ConforNets, we retain the 5 diffusion rollouts but use 20 seeds
     with k = 2 and take structures **after 5, 10, 15, and 20 ConforNet optimization steps**...
     **As benchmark targets span a wide range of conformational changes and we do not know a priori
     at which step the desired conformation emerges, we sweep a range of steps to maximize
     diversity.**" The sample budget is equalised at 800 across methods, which is the right control,
     but the *sweep range itself* was chosen because the benchmark spans a range of changes.
     (Symmetrically, ConforMix's target-RMSD sweep 0.5–19.5 is also a range, p13.)
  4. **The success thresholds τ are set per benchmark from the measured separation of the reference
     pairs.** p14 (App. C.1): "For cryptic pockets, where conformational changes are **localized and
     apo/holo pairs differ by as little as 1.02Å**, we use a stricter cutoff of τ = 1Å"; "we use
     fixed RMSD thresholds for the remaining benchmarks: τ = 3Å for fold switchers and **τ = 2Å for
     membrane transporters, where the reference states typically differ by only 4-5Å**." Also the
     stopping criterion for transfer training is defined on the loss to the reference, p7:
     "ConforNets were trained for at most 300 steps with early stopping if the loss fell below 0.1
     for three consecutive steps; **the checkpoint with the minimum loss was used**."

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.** **PRESENT, and it is
  the definition of every headline number.** p5: "we define **success@B as having a sample whose
  backbone RMSD ≤ τ to the reference state after B predictions**. For each state, we estimate success
  probability using 100 bootstrap trials." p7 for the transfer task: "To declare a sample successful
  we use an RMSD cutoff of τ = 2Å. For GPCRs and kinases, we first align the full structures (using
  US-align (Zhang et al., 2022)) and then compute RMSD over the regions involved in the
  conformational change." Thresholds are fully stated in Table A1 (p14), which is better practice
  than most of this corpus. The relaxed kinase criterion is likewise defined against both references,
  p8: "It asserts that a prediction is **closer to the DFG-out than the DFG-in state**, and its RMSD
  to the DFG-out state is less than max[2, ½RMSD(DFG-in, DFG-out)]."

  **Route 6 — best/worst model labels assigned against a held reference.** **PRESENT.**
  - success@B is by construction a best-of-B statistic against the reference: any one of 100 samples
    matching counts as success (p5, and the metric name itself).
  - Figure 2c caption, p6: "**Best predictions** and ground truth conformations superposed" — the
    displayed structure was chosen by RMSD to the reference (1.54Å outward, 0.91Å inward, p6).
  - Fig. 5 (p8) likewise shows the successful transfer (TM6 RMSD 0.9Å; global RMSD 0.8Å), and Fig. 6
    (p8) shows two labelled failures and one labelled success chosen against the DFG-out reference.
  - App. H, p25: the two ConforNets are named φ_H and φ_C after which reference they land near.
  - There is **no confidence-based selection anywhere** — see `confidence_as_discriminator`.

  **Route 7 — design-level oracle use (weaker than the above; label it as design-level).**
  **PRESENT, and unusually explicit.** The transfer benchmarks were *selected* on a property of the
  base model's behaviour, measured on the evaluation set before the experiment:
  - p7: "we construct three conformation transfer benchmarks that satisfy two criteria: (i) the
    conformational change is biologically meaningful and conserved across the protein family, and
    (ii) **the source state being transferred is rarely sampled by the base model (in this case,
    default OF3p inference); this ensures that success is attributable to controlled induction
    rather than default sampling**."
    This is defensible — it is stated as a design decision and it makes the comparison *harder*, not
    easier — but the expected answer (the state to be produced) is declared before any result is
    read, and the benchmark composition is a function of measurements on the evaluation targets.
  - The three families were chosen because their conserved conformational change is already known
    and catalogued, p2: "such as activation of GPCRs or the DFG-in/out transition of kinases".
  - The scored regions (TM6; A-loop + DFG) were declared from the literature, and other regions were
    explicitly not scored, p15: "We do not score other canonical conformational changes, such as TM5
    and TM7"; "We did not score other canonical conformational changes, such as AC-helices."

  **Training-set leakage, assessed separately because a learned method can leak this way and a
  sampling method cannot.**
  - *ConforNet parameters (128×128 W + 128 b) are trained on ONE structure.* For transfer, that
    structure is the **source protein's** deposited target-state structure. The **targets'** own
    deposited structures are **not** in any training loss — they are used only for scoring. So the
    train/test split at the ConforNet level is a genuine leave-the-source-out split (p7: "excludes
    the source protein used in training the ConforNet").
  - *But the split is neither structure-aware nor sequence-similarity-thresholded.* Source and
    targets are by construction members of the same family, and the source is chosen to be the one
    **most** similar to the rest: p7, "we choose as the source protein the family centroid, defined
    as **the protein with the highest mean sequence similarity to all other family members**." No
    identity cutoff, no fold-based holdout, no time-based split is applied to the transfer suite.
  - *The nearest thing to a leakage control is Fig. A5b (p20), and it is a real one.* p20: "Across
    all source-target pairs, we observe at most a weak negative correlation. When the analysis is
    restricted to the centroid source, this trend disappears (ρ_C is not significant in all
    benchmarks)... successful transfers with sub-2Å RMSD are achieved even at low similarity."
    Fig. 5 (p8) makes the same point on one pair with TM-score 0.28. This argues the effect is not
    a similarity artefact. It does **not** address whether OF3p memorised the target structures.
  - *The decisive gap: the backbone's training set is never characterised.* OF3p-preview's PDB cutoff
    and training composition are **NOT REPORTED anywhere in this paper**. The word appears only about
    a competitor, p6: "direct comparison is difficult as it [BioEmu] was trained on an **earlier PDB
    cutoff** (less data) and fine-tuned on MD trajectories (additional synthetic data)." So the
    possibility that OF3p has seen the deposited active/DFG-out/outward-open structures of the 86
    transfer targets — all of which are, by construction, in the PDB — is nowhere excluded. See
    `anti_memorization_control`.

- **prospective**: **no.** Retrospective at every level: both states of every target are deposited
  and were used to build the benchmark (p5, p15); the training label for transfer is itself a
  deposited structure (p5); success is RMSD to a held reference (p5, p7); the perturbation site was
  chosen by fitting to benchmark ground truths (p9); the recycle setting is a per-benchmark best-of-
  two (p5). No prediction was made and then tested against a structure the authors did not hold, and
  no experiment was performed. The authors do not call it prospective. The one forward-looking
  statement is aspirational, p9: "Clear opportunities lie in exploring its use in biological
  applications."

- **state_metric**: **`RMSD-to-reference + binary predicate` — genuinely dual.**
  - *Continuous / RMSD-to-reference*: backbone RMSD to each deposited reference; also reported as
    coverage curves across a continuous τ (Fig. 2a, 3a, A1–A4), and as "expected minimum RMSD over 5
    samples" in App. F.1 (p20).
  - *Binary predicate*: success@B is a thresholded indicator, and the relaxed kinase criterion is an
    explicit comparative predicate (closer to DFG-out than DFG-in **and** RMSD < max[2, ½ΔRMSD]),
    p8.
  - **Exact thresholds, all stated (Table A1, p14):**

    | Benchmark | τ (Å) | RMSD region | justification given | page |
    |---|---|---|---|---|
    | Cryptic pockets | 1.0 | pocket region (BioEmu-curated) | "apo/holo pairs differ by as little as 1.02Å" | p14 |
    | Domain motions | 3.0 | full structure | "adopt τ = 3Å following BioEmu" | p14 |
    | OOD60 | 3.0 | curated local regions (BioEmu) | "following BioEmu" | p14 |
    | Membrane transporters | 2.0 | full structure | "reference states typically differ by only 4-5Å" | p14 |
    | Fold switchers | 3.0 | full structure | fixed threshold, no per-benchmark justification | p14 |
    | Transfer, all three families | 2.0 | TM6 (GPCR); A-loop + DFG (kinase); global (transporter) | not justified numerically | p7, p15 |
    | Transfer, kinase relaxed | max[2, ½·RMSD(DFG-in, DFG-out)] | A-loop + DFG | "Given the scale of change" (up to 20Å) | p8 |

  - They also state why they rejected ConforMix's adaptive criterion, p14: "ConforMix instead defines
    success relative to the inter-conformation distance: a prediction is considered successful if its
    RMSD to one reference state is less than half the RMSD between the two reference conformations.
    While adaptive, this criterion can be **overly permissive** for benchmarks with large
    conformational changes (e.g., when the two states differ by >20Å)." — then adopt exactly that
    form for the relaxed kinase criterion on p8. Worth noting as an internal inconsistency.
  - No visual-only state calls: every render in the paper carries an RMSD or TM number.

- **metric_saturation**: **YES — numeric ceiling, in two places.**
  1. **success@B is monotone in B and bounded at 100%, and per-target values reach the ceiling.**
     In Fig. 6 (p8), per-kinase success@5 under the relaxed criterion reaches 1.0 for several targets
     in **both** the OF3p panel (CDK2, MAP4K1_HPK1 region, NTRK1_TRKA) and the ConforNet panel
     (ERBB2_ErbB2, MET, NTRK1_TRKA), so those targets cannot separate the arms.
  2. **The coverage curves saturate at 100% by construction as τ grows** (Fig. 2a, 3a, A1–A4): all
     methods converge at large RMSD, so the curves only discriminate in a narrow τ window around the
     benchmark cutoff.
  Not saturating: the aggregate success@100 values, which sit at 22–86% and have headroom
  everywhere (max reported is 86.0%, GPCR reachability, Table 2, p8).
  Axis-truncation issues are recorded in `hides` on the figure rows, not here.

- **directional_control**: **YES, in the transfer mode — this is a genuinely directional, learned
  control, and it is the strongest such claim in the corpus so far. NO in the unsupervised mode.**
  - **What the user specifies:** not a target state label, and not a text or category token, but **a
    solved structure of the desired state for one source protein of the family**. That is the entire
    conditioning signal. p5, Sec. 3.2.2: "**Given a source protein x with a desired reference
    conformation X_ref, we optimize a ConforNet φ so that the one-step deterministic diffusion sample
    X̂_φ from adapted representation φ(z_pre) reconstructs the reference by minimizing
    L_transfer = MSE(Align(X̂_φ), X_ref)**".
  - **How it is supplied at inference:** as a 128×128 matrix plus a 128-vector, multiplied into the
    pre-Pairformer pair latent. p5: "The learned ConforNet φ encodes a state bias towards X_ref in
    the Pairformer latents. **To effect conformational transfer at inference time, we apply φ to the
    pre-Pairformer pair latents of any target protein (typically of the same family as x), propagate
    the transformed latents through the Pairformer, then perform full diffusion rollout.**" There is
    no per-target retraining: p4 Fig. 1 caption, "**Train once (300 steps), Apply to many**".
  - **Cost of instructing it:** one ConforNet training run per family per state, ≤300 steps (p7);
    thereafter "Applying a trained ConforNet at inference time adds negligible overhead, since it is
    just an affine transformation" (p22).
  - **The claim in the authors' words**, p2: "We introduce the concept of supervised transfer of
    conformational state, where we **train a ConforNet on a (single) source protein that encodes a
    specific state, then use this ConforNet to induce the same state in other proteins of the same
    structural family**." And the contrast they draw, p2: "**Standard AF3 inference typically
    produces a single state, and, when it does not, provides no control over what state is
    produced** (Fig. 4)." And p3, against MSA methods: "these methods must contend with a vast
    combinatorial space of MSA perturbations—**without a mechanism to specify the type or magnitude
    of induced conformational change**".
  - **Does it work?** Yes, at the distribution level. Table 2 (p8): success@5 (at-will induction)
    goes OF3p → ConforNets: GPCR active 24.3% → **79.1%**; kinase DFG-out 5.9% → **22.8%**;
    transporter outward 16.1% → **56.7%**. Fig. 4 (p7): AA1R active-state sampling 0% → 88%; CNR1
    35% → 80%.
  - **The named handle:** a *learned channel-wise affine transform of the pre-Pairformer pair
    representation*, conditioned on a deposited reference structure. It is **not** a partner, ligand,
    nanobody, peptide, template, state-filtered MSA, seed or subsample depth. All of the alternative
    handles this corpus tracks were also *run as baselines here and were worse*: template 14.9%,
    ConforMix diffusion guidance 16.9%, AFsample3 MSA masking 27.4%, plain OF3p seeds 24.3% (GPCR
    success@5, Table 2, p8).
  - **Limits on the direction achieved:** kinases work poorly in absolute terms (22.8%), and the
    failure mode is precision rather than direction, p9: "In contrast, ConforNets often produce
    structures **closer to the inactive state, but with limited precision or angular deviations**."
    Fig. 6 (p8) labels two such failures at 3.8Å and 6.0Å.
  - **Unsupervised mode has no direction at all**: the objective is pure pairwise dissimilarity
    (L_dist, L_coord, p4) with no target. Which of the k=2 ConforNets lands in which state is
    discovered afterwards (p25, "as they induce predictions close to the H and C conformations").

- **anti_memorization_design**: **ONE set exists — OOD60, n=19 proteins / 38 reference states — and
  its cutoff is defined against the WRONG model.** p5: "**OOD60 (N=19): proteins deposited after AF2
  training date cutoff and out-of-distribution for BioEmu (but not necessarily for other methods);
  we treat this as a general-purpose benchmark.**"
  - The cutoff is *AF2's* training date and BioEmu's distribution. The model actually being tested is
    **OF3p**, whose training cutoff is never stated anywhere in the paper.
  - The authors' own framing — "we treat this as a general-purpose benchmark" — says outright that
    they are not using it as a memorization control.
  - The transfer suite (GPCR/kinase/transporter, 86 proteins) has **no** post-cutoff or held-out
    design of any kind. Every one of its structures is in the PDB by construction (p15: "All entries
    were downloaded from the PDB").
  - No other holdout: no sequence-identity cutoff, no fold-based split, no time split.

- **anti_memorization_control**: **RUN BUT INVALID FOR THIS METHOD — and mark `UNPOWERED`.**
  - *Run*: OOD60 was executed and analysed as a full arm across all seven methods (Table 1, p6;
    Tables A3, A4, A6; Figs. A1–A3). ConforNets 60.7±2.8% vs OF3p 45.3±1.9% (Table 1, p6). So this
    is **not** the common "held-out set exists but was never used" case.
  - *Invalid as a memorization control for the method under test*, because the set's
    out-of-distribution status is claimed only relative to AF2/BioEmu and is explicitly disclaimed
    for everything else: "**but not necessarily for other methods**" (p5). OF3p's cutoff is
    NOT REPORTED, so overlap between OOD60 and OF3p's training data is neither excluded nor
    quantified.
  - *Worse*, OOD60 is also the set on which the paper's central architectural decision was fitted
    (p9, "we optimized 4 ConforNets for the ground truth entries of OOD60... using L_transfer"), so
    for the purpose of an anti-memorization argument it is contaminated twice over: unknown overlap
    with backbone training, and known use for method selection.
  - **`UNPOWERED`** under the schema's rule: n = 19 proteins is above the ~10 floor, but the held-out
    set's overlap with the backbone's training data is unestablished, which is the second trigger.
  - There is **no anti-memorization arm at all** for the GPCR / kinase / transporter transfer
    results, which are the paper's novelty claim.

- **controls_run**: a real strength of this paper — it runs an unusual number of control arms. Every
  arm actually executed and analysed:

  | control | what it rules out | page |
  |---|---|---|
  | **Equal sample budget across methods (800 samples/target: 160 seeds × 5 rollouts for OF3p/Shallow/AFsample3; 20 seeds × k=2 × 4 checkpoints × 5 for ConforNets; 8 seeds × 20 target-RMSDs × 5 for ConforMix)** | that ConforNets simply sample more | p5, p13 |
  | **Plain OF3p with 160 seeds** | that any gain is seed diversity alone; "simply generating 2× more OF3p samples does not [change the conformational distribution]" | p5, p6, p22 |
  | **Shallow MSA subsampling (8 rows), re-implemented on OF3p** | that MSA-depth perturbation is sufficient | p5, p6 |
  | **AFsample3 MSA column masking (0.2 and 0.4), re-implemented on OF3p** | that MSA-column perturbation is sufficient | p5, p13 |
  | **ConforMix diffusion guidance (twist 15, RMSD sweep 0.5–19.5, 8 seeds), re-implemented on OF3p** | that coordinate-space guidance is equivalent to latent steering | p5, p13 |
  | **Entropy-maximisation objective (Wu & Feng reformulated in the ConforNet framework)** | that any latent perturbation works — it does not: entropy loses to all three diversity objectives on all 6 benchmarks | p5, p19 (Table A6) |
  | **Pair-representation-MSE objective (baseline diversity loss)** | that the choice of diversity space matters — it barely does; all three are comparable | p4, p19 (Table A6) |
  | **State-annotated template arm: OF3p given the centroid's desired conformation as a template** | that a template of the desired state achieves the same thing — it does not (14.9% vs 79.1% GPCR success@5) | p7, p8 |
  | **Perturbation-location sweep: z_pre vs z_post vs s_pre vs s_post, × K ∈ {1,2,5,10} mini-rollouts, 38 entries × 4 replicates** | that the site of intervention is arbitrary; identifies z_post/s_post as shortcut solutions that fail under full rollout | p9 (Table 3), p22 (Table A8) |
  | **Affine ablations: disable b, disable W, diagonal-W only (transporters)** | that channel *mixing* is doing nothing; disabling W costs 47.5→41.2%, diagonal-only 43.3% | p9, p23 (Table A11) |
  | **Recycling ablation R=1 vs R=11, for both tasks** | that gains are a recycling artefact; also shows baselines get *worse* with more recycles in transfer (4 of 6 combinations) | p17, p18, p21 (Tables A3, A4, A7) |
  | **AF3-server sanity check (1 seed, 5 rollouts), all 6 benchmarks** | that OF3p is an unrepresentative stand-in for AF3 | p16 (Table A2, Fig. A1) |
  | **Ligand-input arm on cryptic pockets** | that the ligand-free protocol is not silently crippling holo prediction — it partly is: holo 47.9% → 63.7% with ligand | p19 (Table A5) |
  | **Geometric-validity filter (BioEmu chain-continuity and clash checks, Cα-Cα < 4.5Å, C-N < 2.0Å, clash > 1.0Å) applied to all methods** | that diversity is bought with unphysical structures — "Applying our diversity objective did not increase the proportion of unphysical samples compared to OF3p" | p14 |
  | **Source-selection sweep: 8 GPCR sources, all 20 kinase sources, all 15 transporter sources** | that the centroid heuristic was picked post hoc — the centroid is best in all three | p20 (Fig. A5a) |
  | **Source–target similarity correlation analysis (sequence identity and TM-score, ρ and ρ_C)** | that transfer success is just source–target similarity — "at most a weak negative correlation... ρ_C is not significant in all benchmarks" | p20 (Fig. A5b) |
  | **Wall-clock and memory accounting vs OF3p and ConforMix** | that the comparison hides a compute advantage — ConforNets cost 2–3× OF3p, comparable to ConforMix | p22 (Tables A9, A10) |

  **Controls NOT run**, and their absence matters: no scrambled/decoy ConforNet (a random or
  shuffled W as a null), no held-out-by-time arm for the transfer benchmarks, no cross-family
  transfer arm (does a GPCR ConforNet do anything to a kinase?), no arm testing whether a ConforNet
  trained on the *wrong* state of the same family induces that wrong state, and no test of whether
  OF3p had seen the target structures.

- **confidence_as_discriminator**: **NO — pLDDT/pTM/ipTM are never used to judge conformational
  correctness, and this is unusually clean.**
  - Sample selection is by RMSD to the reference (success@B) and by geometric validity filters, not
    by confidence: p14, "we discard any samples failing the BioEmu geometric validity checks for
    chain continuity and steric clashes (Cα-Cα < 4.5Å, C-N < 2.0Å, clash distance > 1.0Å)."
  - Confidence appears exactly once, describing someone else's method, p3: "Bryant & Noé (2024)
    optimize MSA profiles in AF-Multimer (Evans et al., 2021) to maximize the model's predicted
    confidence (pLDDT), yielding improved multimeric complexes."
  - No validation of confidence as a state discriminator is attempted, and none is needed, because
    no such use is made. The flip side: because success@B takes the best of B against a held
    reference, the paper offers **no way to pick the right structure without the answer** — a
    limitation the authors do not state.

## D. Claims

- **central_conclusion**: A small learned affine transform (W ∈ R^{128×128}, b ∈ R^{128}) applied to
  AF3's pair representation *immediately before* the Pairformer is the right place and form for
  conformational control: it beats MSA-perturbation and diffusion-guidance methods on all six
  multi-state benchmarks, and — because it acts on channels rather than residues — a single such
  transform trained on one source protein's deposited structure can be transferred to induce the same
  functional state in other members of the family, roughly tripling at-will induction of the GPCR
  active state, quadrupling kinase DFG-out and tripling transporter outward-open relative to default
  OF3p inference.

- **necessity_claims** (verbatim + page):
  - p2: "Standard AF3 inference typically produces a single state, and, when it does not, provides
    no control over what state is produced (Fig. 4)."
  - p3: "While they provide partially effective heuristics, these methods must contend with a vast
    combinatorial space of MSA perturbations—without a mechanism to specify the type or magnitude of
    induced conformational change—and with their effectiveness being contingent on the depth and
    diversity of the starting MSA."
  - p1 (Abstract): "Several efforts have focused on eliciting greater conformational variability
    through ad hoc inference-time perturbations of AF models or their inputs. Despite their progress,
    these approaches remain inefficient and fail to consistently recover major conformational modes."
  - p1 (Intro): "These models continue to, however, struggle to capture the conformational
    heterogeneity and context-dependent changes that underlie many protein functions."
  - p1 (Intro): "Existing approaches seldom operate optimally, leading to inefficient sampling,
    missing conformational modes, and implausible structures with physical violations."
  - p2 (Intro): "Perturbing latents, where implicit conformational knowledge may be encoded, is
    natural but not guaranteed to yield energetically accessible and physically plausible states.
    The same is arguably truer when directly perturbing predictions in coordinate space, for instance
    in AF3's diffusion module (Richman et al., 2025), which can be brittle (Li et al., 2026) due to
    bypassing the extensive structural reasoning performed prior to diffusion."
  - p2 (Related work, on MD-trained ensemble models): "By virtue of requiring explicit ensembles as
    training data, these models are highly dependent on the quality and quantity of said data, which
    remains exceedingly rare for experimental sources, and short in timescales for MD trajectories."
  - p1 (Intro): "it is constrained by the limited lengths of available MD trajectories, which
    typically do not sample slow but biologically relevant conformational changes."
  - p2 (Related work): "In both cases, the models capture variation that is limited in spatial scale,
    as they are not trained, tuned, or steered to recover large transitions."
  - p3 (on why upstream beats diffusion guidance): "because ConforNets are learned transforms, once
    trained they are reusable across proteins in a way that is inherently inaccessible to diffusion
    guidance."
  - p8 (on the template arm): "Supplying the desired conformation of the centroid protein as a
    template does not improve performance."
  - p8: "Low reachability, even when using competitive diversity-maximizing baselines such as
    ConforMix and AFsample3, highlights that supervised transfer enables a new capability."
  - p8 (Table 2 caption): "Current methods do not provide an interface for inducing a conformation
    embodied by a different protein and are therefore shown in gray".
  - p3 (on prior latents work): "All of the above approaches directly optimize AF2/3 representations
    (across the sequence dimension) during inference and are therefore inherently per-protein
    procedures."

- **novelty_claims** (verbatim + page):
  - p1 (Abstract): "Unlike previous methods, ConforNets globally modulate AF3 representations, making
    them reusable across proteins."
  - p1 (Abstract): "On unsupervised generation of alternate states, ConforNets achieve
    state-of-the-art success rates on all existing multi-state benchmarks."
  - p1 (Abstract): "On the novel supervised task of conformational transfer, ConforNets trained on
    one source protein can induce a conserved conformational change across a protein family."
  - p1 (Abstract): "Collectively, these results introduce a mechanism for conformational control in
    AF3-based models."
  - p2: "In this work, we introduce ConforNets, a new inference-time, perturbational approach that
    optimizes the placement and method-of-operation on the AF3 architecture."
  - p2: "Unlike existing perturbational methods, which operate residue-wise and are thus
    protein-specific, ConforNets are channel-wise affine transforms."
  - p2: "We introduce the concept of supervised transfer of conformational state, where we train a
    ConforNet on a (single) source protein that encodes a specific state, then use this ConforNet to
    induce the same state in other proteins of the same structural family."
  - p6/p7: "As this is a novel task, we construct three conformation transfer benchmarks..."
  - p3: "While widely explored in domains such as language and image generation, these strategies
    have seen limited use in the molecular sciences. Our work suggests that pretrained protein
    structure predictors implicitly encode rich physical priors, permitting lightweight adaptations
    that unlock new generative capabilities without additional training."
  - p6: "ConforNets consistently achieve state-of-the-art success rates across benchmarks in both the
    coordinate and distogram formulations (Table 1), with the latter showing the best overall
    results."
  - p9 (Conclusion): "In this work, we introduce ConforNets, a lightweight perturbational approach
    that enables a new form of conformation control in AF3-based models."

- **stated_limits**:
  - Ensembles are not Boltzmann-calibrated, p6: "While we do not expect ConforNets to be energetically
    calibrated..."; and "Nonetheless, the sampled empirical free energy landscape is clearly not
    calibrated."
  - Kinases are the weakest case, p8: "In absolute terms, kinases are the most challenging, possibly
    due to the difficulty of modeling flexible loops compared to the well-ordered secondary structures
    of GPCRs and transporters."
  - Failure mode is precision, not direction, p9: "ConforNets often produce structures closer to the
    inactive state, but with limited precision or angular deviations."
  - Resolution limit of the transfer claim, p9: "We evaluated transfer primarily at the level of
    global fold and medium- to large-scale conformational changes, rather than detailed residue-level
    interactions. Understanding the drivers of transferability, and whether it can be extended to
    finer structural features, is an important future direction."
  - Mechanism unexplained, p9: "Our study also raises questions regarding the mechanism and limits of
    conformational transfer."
  - BioEmu comparison is not apples-to-apples, p6: "direct comparison is difficult as it was trained
    on an earlier PDB cutoff (less data) and fine-tuned on MD trajectories (additional synthetic
    data)."
  - AF3 comparison is a sanity check only, p16: "Table A2 and Fig. A1 should be interpreted only as a
    sanity check that OF3p performs similarly to AF3, rather than as evidence that OF3p outperforms
    AF3."
  - Compute overhead is real, p9: "Training ConforNets does have a one-time cost"; p22: "training
    requires additional memory relative to inference-time methods."
  - Compute comparison is not straightforward, p22: "Comparing compute across methods is not
    straightforward, since the cost depends on several implementation choices."
  - R=11 transfer untested for their own method, p21: "It would still be interesting in future work
    to test ConforNets transfer with R = 11".
  - Scored regions are incomplete, p15: "We do not score other canonical conformational changes, such
    as TM5 and TM7"; "We did not score other canonical conformational changes, such as AC-helices."
  - Only the last recycle is perturbed, p5: "In our experiments, we apply ConforNets only in the final
    pass, consistent with OF3p training where gradients are enabled only in the last pass."
  - Only two-state problems are addressed, p4 footnote 1: "We focus on k = 2 because all benchmarks
    considered in this work contain only two reference conformational states."
  - The deposition bias is acknowledged, p13: "Most methods achieve lower success on apo than on holo
    conformations, likely due to a PDB deposition bias toward holo complexes."
  - **Not stated as a limit anywhere:** that transfer requires a solved structure of the desired
    state; that OF3p's training cutoff is unknown relative to the benchmarks; that success@B needs
    the answer to pick the right sample.

- **stance**: **`precedent` + `contrast`. PROVISIONAL — the user's call, not the extractor's.**
  - *precedent on findings*: it is the closest methodological competitor in the corpus — a learned
    latent perturbation delivering explicit, reusable directional control over GPCR active, kinase
    DFG-out and transporter outward-open states, with head-to-head numbers against MSA subsampling,
    MSA column masking, diffusion guidance and state-annotated templates, all re-implemented on one
    chassis. Its Table 2 template row is a directly citable negative result on template biasing.
  - *contrast on rigour*: directional control is bought with a deposited structure of the desired
    state as the training label; the perturbation site was selected by fitting to a benchmark it then
    reports on; Table 1 takes the better of two recycling settings per benchmark; the only
    post-cutoff set is defined against AF2's cutoff and explicitly disclaimed for OF3p, whose own
    training cutoff is never stated; and the transfer benchmarks — the novelty claim — have no
    anti-memorization arm at all.

## E. Quantitative comparators

- **metrics_reported**:

  **E.1 — Unsupervised multi-state task, success@100 (Table 1, p6; best of R=1 / R=11 per benchmark).**
  τ per Table A1. `N` is reference states except cryptic pockets (proteins, one row per state).

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | success@100, Cryptic pockets (apo), N=34, τ=1Å on pocket | BioEmu 30.5±2.8; OF3p 30.8±1.7; Shallow 34.6±2.8; AFsample3 44.7±1.7; ConforMix 37.0±1.5; **Ours-coord 48.2±1.8; Ours-dist 48.8±2.9** | % | backbone RMSD ≤ τ to deposited apo reference, 100 bootstrap trials | p6 |
  | success@100, Cryptic pockets (holo), N=34, τ=1Å on pocket | BioEmu 60.6±3.2; OF3p 63.7±2.6; Shallow 53.4±2.6; AFsample3 73.6±2.3; ConforMix 62.7±2.0; **Ours-coord 83.0±2.5; Ours-dist 78.9±2.8** | % | deposited holo reference | p6 |
  | success@100, Domain motions, N=42 states (21 proteins), τ=3Å full | BioEmu 73.1±3.1; OF3p 69.5±2.5; Shallow 72.8±2.6; AFsample3 80.6±2.4; ConforMix 80.3±1.6; **Ours-coord 81.7±1.3; Ours-dist 81.9±1.4** | % | deposited references | p6 |
  | success@100, OOD60, N=38 states (19 proteins), τ=3Å local | BioEmu 43.1±2.5; OF3p 45.3±1.9; Shallow 44.9±3.6; AFsample3 54.0±3.0; ConforMix 57.7±3.3; Ours-coord 53.7±3.2; **Ours-dist 60.7±2.8** | % | deposited references | p6 |
  | success@100, Membrane transporters, N=30 states (15 proteins), τ=2Å full | BioEmu 34.3±3.2; OF3p 24.3±2.1; Shallow 28.7±2.8; AFsample3 46.9±3.4; ConforMix 34.9±2.5; Ours-coord 47.2±3.3; **Ours-dist 51.1±3.7** | % | deposited inward/outward references | p6 |
  | success@100, Fold switchers, N=30 states (15 proteins), τ=3Å full | BioEmu 43.1±0.8; OF3p 52.7±2.6; Shallow 47.3±2.6; AFsample3 48.7±1.8; **ConforMix 54.3±2.6**; Ours-coord 52.5±2.2; **Ours-dist 54.4±2.4** | % | deposited references | p6 |

  **E.2 — Supervised transfer task (Table 2, p8; R=1; 100 samples per target).** Targets exclude the
  source: 50 GPCR, 19 kinase, 14 transporter.

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | success@5 "at-will induction", GPCR active (N=51 pairs), τ=2Å on TM6 | OF3p 24.3±2.6; ConforMix 16.9±3.7; AFsample3 27.4±4.1; Template 14.9±3.0; **ConforNets 79.1±2.3** | % | RMSD of TM6 to deposited fully-active (GPCRdb 100% activation) reference | p8 |
  | success@5, Kinase DFG-out (N=20 pairs), τ=2Å on A-loop+DFG | OF3p 5.9±2.3; ConforMix 3.7±3.6; AFsample3 4.4±3.7; Template 6.4±2.6; **ConforNets 22.8±3.8** | % | RMSD of A-loop + DFG motif to deposited DFG-out (KLIFS) reference | p8 |
  | success@5, Transporter outward-open (N=15), τ=2Å global | OF3p 16.1±5.8; ConforMix 23.1±7.0; AFsample3 20.2±5.7; Template 15.7±6.6; **ConforNets 56.7±6.5** | % | global backbone RMSD to deposited outward-open reference | p8 |
  | success@100 "reachability", GPCR active | OF3p 37.3; ConforMix 43.1; AFsample3 60.8; Template 32; **ConforNets 86.0** | % (no bootstrap SD; only 100 samples generated) | as above | p8 |
  | success@100, Kinase DFG-out | OF3p 10.0; ConforMix 15.1; AFsample3 20.0; Template 10.5; **ConforNets 26.3** | % | as above | p8 |
  | success@100, Transporter outward-open | OF3p 33.3; ConforMix 40.0; AFsample3 33.3; Template 35.7; **ConforNets 73.3** | % | as above | p8 |
  | success@5, Kinase DFG-out under **relaxed** A-loop-flip criterion | OF3p 30 → **ConforNets 58** | % | "closer to the DFG-out than the DFG-in state, and its RMSD to the DFG-out state is less than max[2, ½RMSD(DFG-in, DFG-out)]" | p9 |
  | success@5, Kinase DFG-out, strict, quoted in text | OF3p 6 → **ConforNets 23** | % | rounded restatement of the 5.9 → 22.8 Table 2 row | p9, p2 |

  **E.3 — Headline improvements as the abstract/intro state them (p2):** "24→79% for GPCR active,
  6→23% for kinases DFG-out, and 16→57% for transporters outward-open" — these are the success@5
  Table 2 numbers rounded, **not** the reachability numbers. Do not mix them up.

  **E.4 — Per-target state-probability shifts (Fig. 4, p7).**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Adenosine receptor A1 (AA1R), active-state sampling frequency | OF3p 0% → **ConforNets 88%** | % of samples | empirical landscape, RMSD to active vs inactive reference | p7 |
  | AA1R, inactive-state sampling frequency | OF3p 100% → ConforNets 1% | % of samples | as above | p7 |
  | Cannabinoid receptor 1 (CNR1), active | OF3p 35% → **ConforNets 80%** | % of samples | as above | p7 |
  | CNR1, inactive | OF3p 27% → ConforNets 0% | % of samples | as above | p7 |

  **E.5 — Individual-case RMSD/TM numbers (for figure legends and single-example claims).**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Best transporter prediction, outward (3VVS;A) | 1.54 | Å RMSD | deposited outward reference | p6 |
  | Best transporter prediction, inward (6FHZ;A) | 0.91 | Å RMSD | deposited inward reference | p6 |
  | Separation of the two transporter references | 4.7 | Å RMSD | inward vs outward ground truths | p6 |
  | GPCR transfer example, source 8YN2;R → target 8HCQ;R | TM6 RMSD **0.9**; source–target TM-score 0.75 | Å / TM | target GT active state | p8 |
  | Transporter transfer example, source 6QV1;B → target 6GV1;A | global RMSD **0.8**; source–target TM-score **0.28** | Å / TM | target GT outward state | p8 |
  | Same transporter target, fraction of successful predictions | OF3p 7% → **ConforNets 35%** ("quintuple") | % | 2Å global cutoff | p8 |
  | Same GPCR target, OF3p best sample | minimum TM6 RMSD **3.34** (no sample close to active) | Å | active reference | p8 |
  | PaaI thioesterase, ConforNet φ_H | 1.38 | Å RMSD | 4ZRB;H (N-terminal helix) | p25 |
  | PaaI thioesterase, ConforNet φ_C | 1.29 | Å RMSD | 4ZRB;C (N-terminal coil) | p25 |
  | Kinase failure modes shown | 3.8 ("A-loop flipped but low atomistic precision"), 6.0 ("A-loop flipped but has wrong angle"); success 0.7 | Å RMSD | DFG-out reference | p8 |
  | Smallest apo/holo separation in cryptic-pocket set | 1.02 | Å | apo vs holo references | p14 |
  | Typical transporter inter-state separation | 4–5 | Å | inward vs outward references | p14 |

  **E.6 — Ablations and design-choice numbers.**

  | metric | value | units | measured against | page |
  |---|---|---|---|---|
  | Perturbation location, RMSD after direct optimisation to GT, K=1 (Table 3) | z_post 1.79±1.19 mini / **3.40±2.37 full**; **z_pre 1.90±2.05 mini / 1.93±1.55 full**; s_post 2.31±2.99 / **9.84±26.33**; s_pre 4.14±3.78 / 4.41±3.85 | Å RMSD | OOD60 ground truths, 38 entries × 4 replicates | p9 |
  | Same, full K sweep (Table A8), best z_pre setting | K=2: 1.72±1.13 mini, **1.81±1.11 full** | Å RMSD | as above | p22 |
  | Diversity-objective ablation, membrane transporters, success@100, R=1 (Table A6) | Distogram CDF MSE 50.4±3.9; Coordinate MSE 47.0±3.4; Pair-rep MSE 48.0±4.1; **Entropy max 38.3±3.5** | % | deposited references | p19 |
  | Diversity-objective ablation, all six benchmarks (Table A6) | entropy loses on all 6; the three diversity objectives within ~3 pts of each other on all 6 | % | deposited references | p19 |
  | Affine ablation, membrane transporters, success@100 (Table A11) | Default (rerun) 47.5±3.7; Disable **b** 48.5±3.7; **Disable W 41.2±1.8**; Scaling channels only 43.3±3.2 | % | deposited references | p23 |
  | Ligand input on cryptic pockets, OF3p R=1, success@100 (Table A5) | Holo: with ligand 63.7±3.1 vs without **47.9±2.5**; Apo: 25.4±2.0 vs 26.0±1.1 | % | deposited references | p19 |
  | AF3-server sanity check, success@5 (Table A2) | AF3 vs OF3p — cryptic apo 29.4 / 30.8±1.7; cryptic holo 52.9 / 63.7±2.6; domain 56.8 / 69.5±2.5; OOD60 36.8 / 45.3±1.9; transporters 30.0 / 24.3±2.1; fold switchers 40.0 / 52.7±2.6 | % | deposited references; AF3 is one seed, no SD | p16 |
  | Transfer baselines at R=11 vs R=1 (Table A7), success@5 GPCR | OF3p R=1 24.2±2.4 vs **R=11 9.1±2.1**; AFsample3 R=1 27.7±4.2 vs R=11 26.1±4.5 | % | as above | p21 |
  | Source-selection correlation (Fig. A5a), success@5 vs mean sequence similarity | Spearman ρ = 0.62 (GPCR), 0.19 (kinase), 0.51 (transporter); vs mean TM-score ρ = 0.57, 0.29, 0.49 | Spearman ρ | all-source sweep | p20 |
  | Source–target similarity vs min RMSD (Fig. A5b) | ρ = −0.21 / −0.19 / n.s. (sequence) and −0.20 / −0.34 / n.s. (TM); **ρ_C = n.s. in all six** | Spearman ρ | centroid vs other sources | p20 |
  | Wall-clock, 5 diffusion samples, 40GB A100, R=11 (Table A9) | length 300: ConforNets **37** s, OF3p 19 s, ConforMix 42 s; length 400: 64 / 26 / 54 s | s | includes amortized ConforNet training | p22 |
  | Wall-clock, R=1 (Table A9) | length 300: 31 / 13 / 35 s; length 400: 51 / 16 / 40 s | s | as above | p22 |
  | ConforNet training cost, 20 Pairformer backprop steps, 80GB A100 (Table A10) | 100 res 25.89 s / 2.66 GB; 200 res 38.63 s / 5.21 GB; 300 res 90.04 s / 9.84 GB; 400 res 190.01 s / 17.04 GB; 500 res 366.11 s / 26.85 GB | s / GB | — | p23 |
  | Headline speed claim | "**less than 40 GPU seconds for a 200-residue protein**" | GPU s | ConforNets optimisation | p2 |
  | Relative overhead | "ConforNets cost roughly 2–3× default OF3p sampling, comparable to ConforMix" | × | OF3p | p9, p22 |

  **E.7 — Method hyperparameters (needed to reproduce or to compare budgets).** Diversity: k=2,
  20 optimisation steps, Adam lr 0.001 halved every 5 steps, gradient clip norm 10, ConforNets
  initialised to identity plus Gaussian noise to break symmetry (p4–p5). Transfer: 10 ConforNets per
  source, ≤300 steps, early stop if loss < 0.1 for three consecutive steps, minimum-loss checkpoint
  (p7). Latent dimension c_z = 128, so a ConforNet is 128×128 + 128 = 16,512 parameters (p4;
  Fig. A7 caption on p24 confirms "one 128-dimensional ConforNet (W, b)").

- **n_predictions**: recorded per the schema as samples-per-target, targets, and totals **separately**.

  | task | samples per target | how composed | targets | total |
  |---|---|---|---|---|
  | Multi-state, OF3p / Shallow / AFsample3 | 800 | 160 seeds × 5 diffusion rollouts | 104 proteins | 83,200 per method |
  | Multi-state, ConforNets | 800 | 20 seeds × k=2 × 4 checkpoints (5/10/15/20 steps) × 5 rollouts | 104 | 83,200 |
  | Multi-state, ConforMix | 800 | 8 seeds × 20 target RMSDs × 5 rollouts | 104 | 83,200 |
  | Multi-state, BioEmu | 4,000 | "We generated 4,000 structures per test case without any generation-time filtering" (p13) | 104 | 416,000 |
  | Transfer, ConforNets | 100 | 10 ConforNets × 10 diffusion samples | 83 scored targets (50+19+14) | 8,300 |
  | Transfer, OF3p / Template / AFsample3 | 100 | 20 random seeds × 5 rollouts | 83 | 8,300 each |
  | Transfer, ConforMix | 100 | 1 seed | 83 | 8,300 |
  | Source-selection sweep (App. F.1) | 10 per transfer | N ConforNets per source × 10 samples; N=10 GPCR, N=8 transporter, N=4 kinase; sources = 8 GPCR, all 20 kinase, all 15 transporter | all pairs | NOT REPORTED as a total |
  | Perturbation-location study | — | 4 ConforNets per latent, 4 latents, K ∈ {1,2,5,10} | 38 OOD60 entries × 4 replicates | NOT REPORTED as a total |

  Bootstrap resampling: 100 trials for every success rate except the transfer success@100 column,
  p8 (Table 2 caption): "We only generate 100 samples per benchmark/model combination and therefore
  do not report standard deviation from bootstrap trials for success@100."

- **comparable_to_ours**: *(left empty by the extractor — populated by whoever holds STATUS.md)*

- **si_in_scope**: **ALL IN PDF** for the appendix — but the appendix contains **no target
  list**; Tables A1–A11 are performance summaries only, checked directly. The benchmark
  itself is in the **authors' repository**, `github.com/aqlaboratory/confornets`, obtained
  2026-09-10: `assets/gpcr/references.csv` gives all **51 GPCR pairs / 102 structures**,
  extracted to `../panels/si_tables/lee2026confornets_gpcr_references.csv`. Column
  `pdbidchain_i` is the **active** member, `pdbidchain_j` the **inactive** member, in all 51
  rows (cross-checked against GPCRdb); no structure is reused across pairs. The repo also
  carries `references.csv` for the other six benchmarks (crypticpocket, domainmotion,
  foldswitching, kinases, membrane, ood60), not yet extracted.

  **Two of the 51 pairs are cross-species and the paper does not say so:** ACM3 pairs human
  `8E9Z` (active) with rat `4U15` (inactive); NTR1 pairs rat `8FN1` (active) with human
  `7UL2` (inactive). Both are presented as within-receptor two-state pairs. This is why 51
  test cases yield 53 distinct GPCRdb proteins, and it qualifies any use of this benchmark
  as a clean within-receptor conformational contrast.

## F. Figures

One row per panel group. Split on `mark` or `measure`, not on `facet`. Figures 3, 4, 6 and A7 each
have a letter appearing in two rows because a single panel letter carries two shapes; noted in
`panels`.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | p4 | Method overview: ConforNets as channel-wise affine on z_pre, and the two training regimes (diversity vs transfer) | schematic | `SCHEMATIC \| three side-by-side pipeline diagrams: standard OF3p inference with a ConforNet inserted pre-Pairformer; k parallel ConforNets trained to maximise pairwise sample distance; one ConforNet trained by MSE to a source reference then applied to a target \| no data` | 3 columns, varying by regime; carries the "Train once (300 steps), Apply to many" annotation | | NOT REPORTED — no license statement anywhere in the PDF |
| 2A | p6 | Coverage curve: success@100 vs RMSD cutoff, membrane transporters, 5 methods | line | `PLOT \| facet: none (1) \| vary: RMSD cutoff τ, 0–4 Å (continuous) \| series: method (5: Ours-dist, OF3p, ConforMix, BioEmu, AFsample3) \| measure: success rate (%) \| mark: line + bootstrap SD band \| n: 800 samples per target per method per mark, 30 reference states (15 proteins) per panel` | 1 | x-axis truncated at 4 Å, so the curves are cut before they converge; only Ours-**dist** is drawn, Ours-coord is omitted without saying so | NOT REPORTED |
| 2B | p6 | Empirical free-energy landscape of ConforNet samples for a MATE transporter | heatmap (2D density) | `MATRIX \| rows: RMSD to 6FHZ;A inward-open, 0–8 Å (continuous, binned) \| cols: RMSD to 3VVS;A outward-open, 0–8 Å (continuous, binned) \| value: empirical free energy (0–10, colour) \| facet: none (1)` | 1, with dashed guides at the 2 Å success cutoffs | landscape is explicitly not calibrated (stated p6) yet is drawn with free-energy units and a colourbar; n of samples behind the density not shown on the panel | NOT REPORTED |
| 2C | p6 | Best predictions superposed on inward and outward ground truths | structure render | `RENDER \| facet: comparison (3: GT inward vs GT outward, prediction vs outward GT, prediction vs inward GT) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 3 | shows only the **best** of 800 samples per state (RMSD 1.54 Å, 0.91 Å), against a benchmark success rate of ~51% | NOT REPORTED |
| 3A | p7 | Coverage curves for cryptic pockets, holo and apo | line | `PLOT \| facet: pocket state (2: holo, apo) \| vary: RMSD cutoff τ, 0–2 Å (continuous) \| series: method (5: Ours-coord, OF3p, ConforMix, BioEmu, AFsample3) \| measure: success rate (%) \| mark: line + bootstrap SD band \| n: 800 samples per target per method, 34 proteins per panel` | 2, varying by state | only Ours-**coord** shown here while 2A shows only Ours-dist — the better arm is silently selected per figure | NOT REPORTED |
| 3B | p7 | Empirical free-energy landscape, apo vs holo pocket RMSD, Elongation Factor Tu | heatmap (2D density) | `MATRIX \| rows: RMSD to 1HA3;B holo pocket, 0–5.5 Å (continuous, binned) \| cols: RMSD to 1EXM;A apo pocket, 0–5 Å (continuous, binned) \| value: empirical free energy (0–10, colour) \| facet: none (1)` | 1 (panel letter b, shape 1 of 2) | uncalibrated landscape drawn in energy units; sample n not shown | NOT REPORTED |
| 3B-render | p7 | Cryptic pocket surface with N-methyl kirromycin, experimental vs predicted | structure render | `RENDER \| facet: source (2: holo reference, holo prediction) \| views: 1 \| overlay: NOT REPORTED predictions on 1 reference \| axis: none` | 2 (panel letter b, shape 2 of 2) | the ligand is drawn into both panels although **no ligand was given to the model** in the main protocol (p13) — the reader can mistake this for ligand-conditioned prediction | NOT REPORTED |
| 4A-B | p7 | Empirical landscapes of two GPCRs, default OF3p vs transfer ConforNets, with active/inactive sampling percentages annotated | heatmap (2D density) | `MATRIX \| rows: RMSD to active state, 0–8 Å (continuous, binned) \| cols: RMSD to inactive state, 0–10 Å (continuous, binned) \| value: empirical free energy (0–10, colour) \| facet: receptor (2: AA1R, CNR1) × method (2: OF3p, ConforNets)` | 4 landscape panels (letters a and b, shape 1 of 2), varying by receptor and method | n = 2 receptors chosen to illustrate two narratives ("never samples" and "arbitrary probability"); no aggregate landscape over the 51-receptor benchmark is shown, so the reader cannot tell how typical these are | NOT REPORTED |
| 4A-B-render | p7 | GPCR structures: GT active/inactive vs prediction, before and after transfer | structure render | `RENDER \| facet: receptor (1: AA1R shown) × method (2: OF3p, ConforNets) \| views: 1 \| overlay: NOT REPORTED predictions on 2 references (GT active, GT inactive) \| axis: none` | 2 (letters a and b, shape 2 of 2); only AA1R is rendered | | NOT REPORTED |
| 5A-B | p8 | Transfer across low structural similarity: source, target GT, OF3p prediction, ConforNet-induced prediction | structure render | `RENDER \| facet: family (2: GPCR active 8YN2;R→8HCQ;R, transporter outward 6QV1;B→6GV1;A) \| views: 1 \| overlay: 1 prediction on 1 reference (plus separate source and OF3p panels) \| axis: none` | 2 rows × 4 sub-renders each, varying by family | two hand-picked successes (TM6 RMSD 0.9 Å, global 0.8 Å) illustrating a claim whose benchmark values are 79% and 57% success@5; no quantitative panel accompanies the "generalizes to structurally dissimilar proteins" title claim — that evidence is in Fig. A5b, p20 | NOT REPORTED |
| 6A-B | p8 | Per-kinase and average success@5, OF3p vs DFG-out ConforNet, strict and relaxed cutoffs | bar | `PLOT \| facet: method (2: OF3p, DFG-out ConforNet) \| vary: kinase target (20: 19 named targets + Avg) \| series: cutoff (2: relaxed, 2 Å) \| measure: success@5 (0–1) \| mark: bar (overlaid, relaxed behind strict) \| n: 100 samples per target per method per bar; 19 targets per panel` | 2 panels (letters a implied by layout; the two bar rows), varying by method | bars carry no error bars although success@5 is bootstrapped elsewhere; several bars sit at the 1.0 ceiling in both panels; the "Avg" bar pools 19 heterogeneous targets into one bar with no distribution shown; the 9 kinases without resolved A-loop flips are not distinguished from the 11 that have them | NOT REPORTED |
| 6-render | p8 | Three illustrative kinase transfer outcomes overlaid on DFG-in and DFG-out ground truths | structure render | `RENDER \| facet: outcome (3: failure 3.8 Å ABL1, failure 6.0 Å AKT1, success 0.7 Å CDK2) \| views: 1 \| overlay: 1 prediction on 2 references (DFG-in GT, DFG-out GT) \| axis: none` | 3 | | NOT REPORTED |
| A1 | p16 | Coverage curves, AF3 server vs OF3p, all six benchmarks | line | `PLOT \| facet: benchmark (6: cryptic apo, cryptic holo, domain motion, OOD60, membrane transporter, fold switching) \| vary: RMSD cutoff (continuous) \| series: model (2: AF3 server, OF3p) \| measure: success@5 (%) \| mark: line + bootstrap SD band (OF3p only) \| n: AF3 = 5 samples per target (1 seed), OF3p = 800; per-panel n as Table 1` | 6, varying by benchmark | AF3 curve carries no uncertainty band at all (single seed) while OF3p does — the two are visually comparable but statistically are not; the caption discloses this, the panels do not | NOT REPORTED |
| A2 | p17 | Coverage curves, all methods at fixed R=1 | line | `PLOT \| facet: benchmark (6) \| vary: RMSD cutoff (continuous) \| series: method (5: OF3p, AFsample3, ConforMix, Ours-coord, Ours-dist) \| measure: success@100 (%) \| mark: line + bootstrap SD band \| n: 800 per target per method; per-panel n as Table 1` | 6, varying by benchmark | | NOT REPORTED |
| A3 | p18 | Coverage curves, all methods at fixed R=11 | line | `PLOT \| facet: benchmark (6) \| vary: RMSD cutoff (continuous) \| series: method (6: OF3p, AFsample3, ConforMix, Ours-coord, Ours-dist, BioEmu) \| measure: success@100 (%) \| mark: line + bootstrap SD band \| n: 800 per target per method (BioEmu 4,000); per-panel n as Table 1` | 6, varying by benchmark | | NOT REPORTED |
| A4 | p19 | Cryptic pocket coverage with and without ligand input to OF3p | line | `PLOT \| facet: pocket state (2: apo, holo) \| vary: RMSD cutoff (continuous) \| series: ligand input (2: with, without) \| measure: success@100 (%) \| mark: line + bootstrap SD band \| n: 800 per target, 34 proteins per panel` | 2, varying by state | | NOT REPORTED |
| A5A | p20 | Transfer success vs how central the source protein is in its family | scatter | `PLOT \| facet: benchmark (3: GPCR active, kinase DFG-out, transporter outward) × similarity measure (2: mean sequence similarity, mean TM-score) \| vary: mean similarity to all targets (continuous) \| series: none \| measure: success@5 (0–1) \| mark: point, Spearman ρ annotated \| n: 1 point per candidate source; 8 GPCR, 20 kinase, 15 transporter sources per panel` | 6, varying by benchmark and similarity measure | ρ = 0.19 for kinases is reported without a p-value while the companion panel marks non-significance explicitly — significance is stated inconsistently between A5a and A5b | NOT REPORTED |
| A5B | p20 | Whether transfer success is explained by source–target similarity | scatter | `PLOT \| facet: benchmark (3) × similarity measure (2: sequence similarity, TM-score) \| vary: source–target similarity (continuous, 0–1) \| series: source type (2: other, centroid) \| measure: expected minimum RMSD at 5 samples (Å) \| mark: point, ρ and ρ_C annotated \| n: 1 point per source–target pair; 10 diffusion samples behind each point` | 6, varying by benchmark and similarity measure | | NOT REPORTED |
| A6A | p23 | Distributions of learned ConforNet parameter norms, diversity vs transfer | box | `PLOT \| facet: none (1) \| vary: parameter block (3: diag(W−I), off-diagonals of W, bias b) \| series: training regime (2: diversity, transfer) \| measure: L2 norm / number of entries \| mark: box \| n: one value per ConforNet; number of ConforNets per box NOT REPORTED` | 1 (letter a) | n behind each box is never stated | NOT REPORTED |
| A6B | p23 | Joint spread of ‖W−I‖ and ‖b‖ across ablations and regimes | scatter | `PLOT \| facet: none (1) \| vary: ‖W−I‖/c_z (continuous, 0–0.05) \| series: run type (4: Diversity (Disable W), Diversity (Disable b), Diversity, Transfer) \| measure: ‖b‖₂/√c_z \| mark: point \| n: 1 point per ConforNet; count NOT REPORTED` | 1 (letter b) | | NOT REPORTED |
| A7A-B | p24 | Learned W and its deviation from identity, for two diversity and two transfer ConforNets | heatmap | `MATRIX \| rows: pair-latent channel (128) \| cols: pair-latent channel (128) \| value: W entry, and W−I entry, on separate colour scales \| facet: regime (2: diversity, transfer) × example (2) × quantity (2: W, W−I)` | 8 matrix panels (rows 1–2 of the figure) | the W and W−I rows use different colour ranges per regime (±1.0 / ±0.04 vs ±1.0 / ±0.1), so diversity and transfer panels cannot be compared by eye | NOT REPORTED |
| A7C | p24 | Learned bias vector b for the same four ConforNets | line | `PLOT \| facet: regime (2: diversity, transfer) × example (2) \| vary: channel index, 0–127 (continuous) \| series: none \| measure: bias value b \| mark: line \| n: 1 ConforNet per panel` | 4 (bottom row of the figure) | y-scales differ between the diversity (±0.025) and transfer (±0.05) panels | NOT REPORTED |
| A8 | p24 | Growth of ConforNet parameter magnitude over the 20 diversity training steps, against the transfer level | line | `PLOT \| facet: parameter (2: ‖W−I‖/c_z, ‖b‖₂/√c_z) \| vary: training step, 5–20 (continuous) \| series: run type (3: Diversity, Diversity (Disable b) or (Disable W), Transfer as a dashed horizontal reference band) \| measure: normalised L2 norm \| mark: line + SD band \| n: mean over all diversity ConforNets; count NOT REPORTED` | 2, varying by parameter | transfer is drawn as a flat dashed line with no step axis of its own — a 300-step run compared to a 20-step run on a 20-step axis | NOT REPORTED |
| A9 | p25 | PaaI thioesterase fold switch: ground truth pair and the two ConforNet-induced structures | structure render | `RENDER \| facet: structure (3: GT helix vs GT coil superposed, φ_H-induced vs 4ZRB;H, φ_C-induced vs 4ZRB;C) \| views: 1 \| overlay: 1 prediction on 1 reference \| axis: none` | 3 | single hand-picked interpretable example, selected because it is easy to interpret (stated p25) | NOT REPORTED |
| A10 | p26 | Evolution of an 8×137 pair-representation slice (channel 0) through Pairformer depth under φ_H and φ_C, and their difference, against the ground-truth distogram slice | heatmap | `MATRIX \| rows: N-terminal helix residue (8) \| cols: all residues (137) \| value: pair-representation activation, channel 0 (and the ground-truth distogram slice in the last column) \| facet: ConforNet (3: φ_H, φ_C, difference) × pipeline stage (z_pre, φ(z_pre), selected Pairformer blocks, ground truth)` | 3 panel groups, each a strip of stages | no colour scale shared across stages is stated; the "pattern... gradually emerges and sharpens with depth" claim (p25) is made by eye with no quantitative panel | NOT REPORTED |
| A11 | p26 | Same as A10 for channel 1 | heatmap | `MATRIX \| rows: N-terminal helix residue (8) \| cols: all residues (137) \| value: pair-representation activation, channel 1 \| facet: ConforNet (3: φ_H, φ_C, difference) × pipeline stage` | 3 panel groups | as A10; 2 of 128 channels are shown with no statement of how they were chosen | NOT REPORTED |

**reuse, general:** the PDF carries **no license statement, no copyright line and no CC notice** on any
page — checked p1 (title block), p10 (Acknowledgements / Impact Statement) and p26 (last page).
Default arXiv terms therefore apply and are not visible here; **assume all rights reserved and do not
redraw or reproduce any panel without checking the arXiv abstract page for the submitter's chosen
license.** No ND clause is confirmed or excluded from the PDF alone.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5)
- **schema_version**: v3
- **confidence**: **high** for identity, scope, the two benchmark inventories, all tabulated numbers,
  oracle-leakage routes, directional control and the control-arm table — the paper is unusually
  explicit about its protocol and puts every appendix in the same PDF. **Medium** for the figure
  rows: captions are terse about panel counts, so pages 6, 7, 8 and 23 were rendered at 150 dpi and
  read directly; A1–A5 and A7–A11 were filled from captions plus the text layer without rendering,
  so per-panel series counts there are inferred from the caption wording and could be off by a
  series. **Medium** for `metric_saturation` on Fig. 6, where bar heights at 1.0 were read off a
  rendered page rather than from a table.
- **unresolved**:
  1. **OF3p-preview's training cutoff and training set are never stated.** This is the single most
     consequential gap in the paper: without it, no claim about memorization of the 86 transfer
     targets (all deposited, all PDB-sourced) can be evaluated, and OOD60's "out-of-distribution"
     label demonstrably does not transfer to OF3p (p5 says so).
  2. **Benchmark membership is not enumerated.** The 51 GPCR pairs, 20 kinase pairs, 34 cryptic
     pockets, 21 domain-motion, 15 fold-switch and 19 OOD60 proteins are described procedurally but
     not listed; only the 11 A-loop-flipping kinases are named (p15). The benchmarks are therefore
     not reproducible from the PDF and cannot be intersected against our own target list.
  3. **No code or data availability statement.** Whether ConforNets will be released is not stated.
  4. **The relaxed kinase criterion contradicts the paper's own critique.** On p14 they reject
     ConforMix's "RMSD < half the inter-state distance" rule as "overly permissive for benchmarks
     with large conformational changes"; on p8 they adopt max[2, ½RMSD(DFG-in, DFG-out)] for exactly
     the benchmark with the largest changes (up to 20 Å). The 30%→58% relaxed numbers should be
     cited with that noted.
  5. **Table 1 mixes recycling settings across rows** ("we report the better of R = 11 or R = 1 for
     all methods", p5). Any citation of a Table 1 value should say which R it came from; Tables A3
     (R=1, p17) and A4 (R=11, p18) are the fixed-setting sources.
  6. **Fig. 2a shows only Ours-dist and Fig. 3a only Ours-coord**, with no statement that the other
     arm was omitted. Whether the omitted arm would change the visual conclusion is undeterminable
     from the PDF.
  7. **Whether the diversity-mode k=2 ConforNets can be steered at all is untested.** The paper never
     asks whether a diversity ConforNet, once trained, transfers — only transfer-trained ones are
     reused. So "reusable across proteins" (abstract, p1) is demonstrated only for the supervised
     variant.
  8. **No cross-family transfer test.** Whether a GPCR ConforNet does anything to a kinase — the
     obvious null — is never run.
  9. **The number of ConforNets behind each box/point in Figs. A6 and A8 is never given.**
  10. **Venue is ambiguous.** ICML-style formatting with an Impact Statement, but no conference is
      named; recorded as arXiv preprint.

  **Tag vocabulary gaps encountered (needed but not in the fixed v3 list — NOT invented, recorded
  here as the schema requires):**
  - **A protocol tag for "templates off, MSA on".** v3 has `no-template-no-msa` and `templates-on`
    but nothing for the very common regime this paper uses in every main experiment: full MSAs from
    ColabFold, templates explicitly withheld (p13). I could not tag the paper's actual protocol.
    Suggest `templates-off`.
  - **A method tag for diffusion/coordinate-space guidance.** `latent-steering` is defined as
    intervention on "pair representation, trunk embedding, distogram head, conditioning embedding" —
    ConforMix, run here as a full baseline arm, guides the *diffusion score* in coordinate space and
    fits no v3 method tag. Suggest `diffusion-guidance`.
  - **A tag for cross-protein transfer of a learned control.** `directed-state` covers "a state was
    directed", but the reusable-across-proteins property is this paper's distinguishing claim and has
    no tag. Suggest `transferable-control`.
  - **A rigour tag for "the training label is a deposited structure of the target state".** This is a
    different animal from `oracle-leak` (evaluation-time) and from `design-level-oracle` (route 7),
    and it is exactly what separates a learned control method from a sampling one. Suggest
    `supervised-on-target-state`.
  - Not needed but noted: `md-emulator` correctly describes BioEmu, which appears here only as a
    comparator, so the paper is not tagged with it.

  **v3 schema ambiguities hit while extracting (blunt, as asked):**
  - **A 2D free-energy landscape fits neither PLOT nor MATRIX cleanly.** Figs. 2b, 3b and 4 have
    *two continuous independent coordinates* and a colour-encoded measure. PLOT has one `vary` slot
    and no second axis role; MATRIX is specified for axes that "are indices". I used MATRIX with
    binned continuous rows/cols and flagged it here, but a future extractor will plausibly choose
    PLOT and the join will break. This is the same class of defect that produced the v2→v3
    `series:` fix. Suggest either allowing `rows`/`cols` to be continuous ranges explicitly, or
    adding a FIELD form for landscape/density plots.
  - **`n:` has no clean form for "800 samples per target, best of which is scored".** A success@B
    coverage curve's mark is a *rate over targets* whose underlying unit is a best-of-800 statistic.
    I wrote both numbers into `n:`, but the "1 of 5 (pLDDT-selected)" worked example does not cover
    the best-of-B case, which is the dominant metric in this whole literature. Suggest a
    `best-of-B` form.
  - **`method_class` has no entry for latent steering**, although the tag vocabulary gained
    `latent-steering` in v3. I wrote `other` plus a description. The B-table list and the tag list
    should be reconciled.
  - **`states_generated` dual form is under-specified for a paper with two modes.** "ensemble + one"
    is right but reads as one method that does both; here it is two methods. The schema's example
    ("ensemble + single-state") is a collapse *within* one method. A future reader of INDEX.md will
    not see the difference. Suggest allowing a per-mode annotation.
  - **`anti_memorization_control` has no verdict for "arm was run, but its holdout is defined against
    a different model than the one tested".** `NONE RUN` is false, plain `RUN` is misleading, and
    `UNPOWERED` is the closest but its stated triggers are small n or overlap-with-training rather
    than wrong-model-cutoff. I used `UNPOWERED` and wrote the reason out. Suggest an explicit
    `INVALID` verdict.
  - **`metric_saturation` says "numeric saturation only", but a success@B metric saturates
    *structurally* (monotone in B, bounded at 1) as well as numerically in specific panels.** I
    recorded both and cross-referenced Fig. 6. Worth a sentence in the schema on max-over-samples
    metrics, which are now the norm in this field.
- **why_it_matters**: *(left empty by the extractor — the user's call)*

## Tags

`gpcr` `kinase` `transporter` `fold-switching` `general-protein`
`latent-steering`
`state-annotated-input`
`ensemble` `two-state` `single-state`
`rmsd-only` `binary-predicate` `continuous-metric` `saturating-metric`
`oracle-leak` `design-level-oracle` `anti-memorization` `unpowered`
`directed-state` `apo-sampling`
`cryptic-pocket`
`preprint`
`precedent` `contrast`
`comparator-numbers`

**Justification for each non-obvious tag** (so a future reverse lookup can be trusted):

- `gpcr` / `kinase` / `transporter` — the three transfer benchmarks (p7). `kinase` is correct in the
  v3 protein-kinase sense: ABL1, AKT1/2, BRAF, BTK, CDK2/4/7, CSK, ERBB2, HCK, INSR, MAP4K1, MAP4K4,
  MET, NTRK1, TNIK, ULK3 (p8, p15) are all protein kinases.
- `fold-switching` — the 15-protein fold-switcher benchmark (p5, curated by Porter & Looger 2018) and
  the PaaI thioesterase case study (p25).
- `general-protein` — domain motions (21), cryptic pockets (34), OOD60 (19).
- `latent-steering` — the defining method: an inference-time affine transform of the pre-Pairformer
  pair representation (p4). Exactly the v3 definition.
- `state-annotated-input` — the transfer ConforNet's training input is a **state-annotated deposited
  structure** (GPCRdb 100%-activation-degree active structures, p15; KLIFS DFG-out annotations, p15),
  and one baseline arm supplies the centroid's desired conformation as a template (p7).
- `ensemble` + `two-state` + `single-state` — all three are literally true and the vocabulary permits
  combination: the diversity mode produces an 800-sample ensemble (p5), that ensemble is deliberately
  shaped to **k=2** modes because the benchmarks are two-state (p4 fn 1), and the transfer mode
  collapses onto one induced state at >80% (p7, Fig. 4).
- `rmsd-only` — every physical measure in the paper is a backbone RMSD to a deposited reference.
- `binary-predicate` — success@B is a thresholded indicator, and the relaxed kinase criterion is an
  explicit comparative predicate (p8).
- `continuous-metric` — coverage curves across a continuous τ (Figs. 2a, 3a, A1–A4) and "expected
  minimum RMSD over 5 samples" (p20).
- `saturating-metric` — per-target success@5 hits the 1.0 ceiling for several kinases in both arms of
  Fig. 6 (p8), and every coverage curve saturates at 100% by construction.
- **NOT** `visual-metric` — every render in the paper carries a numeric RMSD or TM value.
- `oracle-leak` — routes 1, 2, 4, 5, 6 all present; decisively, the transfer control signal *is* a
  deposited structure of the desired state (p5), and the perturbation site was chosen by fitting to
  OOD60 ground truths (p9).
- `design-level-oracle` — route 7: benchmark states were selected *because* the base model rarely
  samples them (p7), and the scored regions were declared in advance from the literature (p15).
- `anti-memorization` — a post-cutoff set (OOD60, 19 proteins / 38 states) **exists and was actually
  run** across all methods (p5, p6). Tagged so the reverse lookup finds it, but read
  `anti_memorization_control` before citing: the cutoff is AF2's, not OF3p's.
- `unpowered` — the same arm's overlap with OF3p's training data is unestablished (OF3p's cutoff is
  NOT REPORTED), and the transfer suite has no holdout at all.
- `directed-state` — the paper's central novel capability, p2: "induce the same state in other
  proteins of the same structural family."
- `apo-sampling` — the main protocol supplies no ligands to any method (p13), and apo cryptic-pocket
  prediction is a headline benchmark row. **NOT** `ligand-driven`: a ligand-input arm exists (Table
  A5, p19, holo 47.9%→63.7%) but ligands are not this paper's control handle; the number is in
  `metrics_reported` so it remains findable.
- `cryptic-pocket` — the 34-protein benchmark (p5).
- **NOT** `multi-backbone` — one chassis (OF3p) plus one disclaimed single-seed AF3 sanity check
  (p16). BioEmu is not an AF-family backbone.
- **NOT** `msa-subsample` / `template-state-bias` — these appear only as re-implemented *baseline
  arms*, not as the paper's method. Tagging them would return this paper on queries for MSA and
  template methods, which would be a false positive. Their numbers are in `controls_run` and
  `metrics_reported`.
- **NOT** `confidence-as-discriminator` — pLDDT/pTM are never used to select or score (p14).
- **NOT** `prospective`, **NOT** `experimental-validation`, **NOT** `experimental`,
  **NOT** `negative-result`, **NOT** `allosteric-failure`, **NOT** `md` / `md-emulator`
  (BioEmu is a comparator, not this paper's method), **NOT** `af-cluster`, **NOT** `seed-only`,
  **NOT** `no-template-no-msa` (MSAs are used at 1,024 rows).
- `precedent` + `contrast` — provisional, see `stance`.
- `comparator-numbers` — Tables 1 and 2 are directly placeable next to our numbers, with matched
  sample budgets and stated thresholds.
</content>
</invoke>
