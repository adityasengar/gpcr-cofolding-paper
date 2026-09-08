# protenix2026v2

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say,
`NOT APPLICABLE` **with a reason** where the field's axis does not exist in this paper.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–17)**, which coincide with the
printed folios. Layout: p1 title/authors/abstract + Figure 1; p2 §1 Introduction + §2 Methods
(**the training-cutoff sentence is here**); p3 §3 Antibody-Antigen Structure Prediction + Figures 2
and 3; p4 §4 Zero-shot Antibody Design + Figure 4; p5 design panel construction, GPCR results,
developability; p6 Figures 5 and 6 + VEGF-A ranking case study; p7 §5 Expanded Capabilities, §5.1
ligand plausibility + Table 1; p8 Figures 7 and 8; p9 §5.2 SC2RBD dual binding + Figure 9 + Table 2;
p10 §6 Summary + Acknowledgment; p11–13 References; p14 Appendix A Benchmark Details + Table 3 +
§A.2 Model Inference Setting; p15 Figure 10 + §B Wet-Lab Experimental Details (B.1, B.2); p16 §B.3
Binding Kinetics + Table 4 antigen catalogue; p17 §B.4 Developability + Table 5 thresholds.

**What this paper is.** A corporate technical report from ByteDance Seed announcing **Protenix-v2**,
a system with two modes: an AlphaFold3-style all-atom co-folding structure predictor, and a
target-conditioned generative binder-design stack (the successor to PXDesign). It is a MODEL /
CAPABILITY report with substantial wet-lab validation. **It contains no conformational-state analysis
of any kind** — no apo/holo pairs, no alternative states, no state-annotated inputs, no ensemble
scored as states. Every Section C field that presupposes "which state did you steer it to" is
therefore `NOT APPLICABLE` by the nature of the work, not by extraction sloppiness. See
`directional_control` for the controllability handles the paper *does* claim, which are
epitope/format/chemistry handles rather than conformational-state handles.

**Method detail is extremely thin.** There is no architecture description, no diagram, no
hyperparameters, no loss functions, no training-set size, no ablation of the "architectural
refinements", and no statement of Protenix-v2's own MSA or template settings. Page 2 delegates the
entire architectural delta to one sentence. **Nothing in this note is inferred from AlphaFold3, from
PXDesign, or from either earlier Protenix report.**

**Three distinct Protenix reports exist and this paper cites two of them.** See `unresolved` — this
is the single most citation-dangerous thing about this entry.

**No supplementary material exists outside this PDF** — but several headline numbers are readable
only as figure badges and bar labels, never as a table. See `si_in_scope`.

---

## What is new in v2 relative to v1 — everything this paper itself states, with pages

This block exists because the corpus holds an earlier Protenix entry and the two must stay
distinguishable. **Every line below is what THIS paper says; nothing is imported from the earlier
note.** Read `unresolved` item 1 first: the "Protenix-v1" baseline in this paper is reference **[33]**
(bioRxiv 2026-02), which is *not* the corpus's `protenix2025` entry (reference **[8]**).

**Architecture and training — stated in one sentence and never elaborated:**
- p2: "Relative to earlier Protenix iterations [8, 33], Protenix-v2 incorporates **architectural
  refinements and training optimizations** while **retaining the same input-output setting**." No
  refinement is named, no optimization is described, no ablation is run. This is the entire
  architectural delta as documented.

**Training data — the cutoff:**
- p2: "Protenix-v2 is trained without wwPDB [3] entries released on or after **2021-09-30**." The
  paper gives **no cutoff date for any earlier version**, only that this one "aligns with established
  conventions in recent models [8, 28, 34]". **Whether the date changed cannot be established here.**

**Capability and performance deltas, each with its page:**
1. **Antibody–antigen interface accuracy.** +9 to +13 percentage points over Protenix-v1 at
   DockQ > 0.23 across three collections (p3); 49.7 vs 40.2 (PXMeter-AB), 65.0 vs 52.3
   (FoldBench-AB), 53.5 vs 40.4 (AF3-AB) (Figure 2, p3). "gains at DockQ > 0.8 are comparably large"
   (p3) — asserted, never quantified.
2. **Sampling efficiency.** "Protenix-v2 at only 5 seeds already exceeds the performance of
   Protenix-v1 at 1000 seeds" (p4; abstract p1; Figure 3, p3). This is the sharpest v1→v2 claim in the
   paper.
3. **Position relative to AlphaFold3.** "Protenix-v2 moves from approximate parity with AlphaFold3 to
   a clear leading position in antibody-antigen modeling" (p4) — i.e. the *parity* is attributed to v1
   and the *lead* to v2.
4. **General benchmark suites — small gains, explicitly downgraded.** Protenix-v2 vs Protenix-v1
   (Table 3, p14): FoldBench monomer LDDT 89.1 vs 88.6; protein–ligand 64.0 vs 62.5; protein–protein
   73.0 vs 72.7; PXMeter monomer 88.0 vs 87.2; protein–ligand 49.2 vs 48.1; protein–protein 73.9 vs
   72.9. The authors call this "remains competitive" and steer the reader to the antibody and ligand
   analyses instead (p14).
5. **Ligand plausibility — a new evaluation criterion and a new inference-time variant, and the v1
   variant is not beaten.** PXMeter is extended to v1.1.0 with "additional checks on planarity around
   sp2 carbon centers, planarity of amide groups, and non-planarity at sp3 carbon and nitrogen
   centers" (p7). New TFG (training-free guidance) variants are introduced for **both** versions
   (p7). Revised-criterion joint success: Protenix-v2 49.22 vs Protenix-v1 48.14 — a gain of ~1 point;
   **Protenix-v2-TFG 60.46 vs Protenix-v1-TFG 61.11 — v1-TFG is marginally *higher*** (Table 1, p7).
   So the ligand improvement comes from the TFG guidance, not from the v2 base model, and the paper
   does not remark on the v1-TFG > v2-TFG inversion.
6. **Design scope broadened from protein binders to antibodies.** "The design results reported here
   move beyond the protein-binder focus of prior PXDesign work [32] to achieve robust zero-shot
   antibody generation" (p5); "this report moves beyond the protein-binder emphasis in prior PXDesign
   work [32] toward zero-shot antibody design, developability assessment, and hit discovery on
   challenging targets such as G protein-coupled receptors (GPCRs)" (p2). New formats: VHH/VHH-Fc, Fv
   (VH+VL) grafted to a full-length mAb.
7. **New design controls exposed to the user** (p2–3): epitope-targeting *or* site-agnostic
   generation; per-CDR loop length ranges; predefined frameworks/scaffolds importable into the design
   spec.
8. **Rankers.** "two rankers integrated in Protenix-v2 (Ranker A and Ranker B)" (p6), compared against
   a human expert. Not described, and not attributed to v1 or v2 in origin.
9. **Cross-variant design, stated as a direct improvement on the previous generation.** "Previous
   PXDesign mini-binders showed weak-to-none binding to the RBD of SARS-Cov-2 Omicron B.1.1.529. In
   contrast, when RBDs of both prototype and Omicron were jointly provided as inputs, Protenix-v2
   generated 2 dual-binding mini-binders out of 4 tested designs" (p9); the old binders are measured
   alongside the new ones in Table 2 (p9).

**What is NOT new — the direct answer to the conformational question:**
**Protenix-v2 adds NO conformational-state, multi-state, or state-controllability capability.** The
paper contains no apo/holo comparison, no alternative-state prediction, no state-annotated input, no
ensemble analysis, no state metric, and no discussion of conformational change other than as a
*difficulty* to be worked around on GPCR surfaces (p5). Every reported structure is a single ranked
top-1 model. The controllability this paper does add is over the **designed molecule** (epitope, CDR
lengths, framework, format) and over **local ligand chemistry** (TFG constraints on chirality,
planarity, torsion, distance) — never over the target's conformational state. See
`directional_control` and `states_generated`.

---

## A. Identity

- **citekey**: `protenix2026v2`
- **doi**: **10.64898/2026.04.10.717613** (bioRxiv) — p1 banner, repeated on every page: "bioRxiv
  preprint doi: https://doi.org/10.64898/2026.04.10.717613; this version posted April 11, 2026." No
  journal DOI, no arXiv ID, no version number beyond "this version".
- **year**: **2026.** Two dates are given and they differ by weeks: the bioRxiv banner says "this
  version posted April 11, 2026" (p1, every page), while the paper's own closing dateline on p10
  reads "April 2026 / When Beijing meets Seattle". Neither is the training cutoff — see
  `anti_memorization_design`.
- **venue**: **bioRxiv preprint, not certified by peer review.** p1: "The copyright holder for this
  preprint (which was not certified by peer review) is the author/funder, who has granted bioRxiv a
  license to display the preprint in perpetuity. It is made available under a **CC-BY-ND 4.0
  International license**." Tagged `preprint`; **not** `peer-reviewed`. **The ND clause matters for
  figure reuse** — see `reuse` in Section F.
- **title**: **Protenix-v2: Broadening the Reach of Structure Prediction and Biomolecular Design**
  — p1. Note: the running title is "…and Biomolecular **Design**", not "Modeling"; the word
  "modeling" appears only in the abstract's opening clause ("Advances in biomolecular modeling…", p1).
  Cite the title exactly as printed.
- **authors**: Yuxuan Zhang, Chengyue Gong, Jinyuan Sun, Jiaqi Guan, Milong Ren, Song Xue, Hanyu
  Zhang, Wenzhi Ma, Zhenyu Liu (all marked † "Core Contributors; equal contribution; order is
  random"), Xinshi Chen⋆, Wenzhi Xiao⋆ (⋆ corresponding). Affiliation: **ByteDance Seed** (single
  affiliation, p1). Correspondence: Xinshi Chen and Wenzhi Xiao (p1). No competing-interests
  statement, no funding statement, no data-availability statement, no code-availability statement
  anywhere in the PDF.

## B. Scope

- **system**: **General biomolecular complexes**, with three specific emphases: (1) **antibody–antigen
  interfaces** (the headline structure-prediction claim, p3–4); (2) **protein–ligand** complexes
  (§5.1, p7–8); (3) **antibody/binder design against soluble antigens and against GPCRs** (§4, p4–6).
  The GPCR involvement is real but is as an *antigen class for antibody design*, not as a
  conformational-modelling subject: "we included multiple GPCR targets, a therapeutically important
  receptor class whose accessible extracellular epitopes are often small and conformationally
  flexible, making them difficult settings for both de novo design and traditional antibody
  discovery" (p5). Four GPCRs are named — **CCR5, CCR7, CCR8, GPRC5D** (Figure 1 p1; Figure 4A p4;
  Table 4 p16). Also covered by the broader benchmarks: protein monomers, protein–ligand interfaces,
  protein–protein interfaces (Table 3, p14). No kinase, transporter, or fold-switching system
  anywhere. Tags `general-protein` and `gpcr`.
- **n_targets**: **no single number; every level recorded with its page.**
  - **Antibody-antigen structure-prediction benchmarks (p3, Figure 2 panel titles, entries/clusters):**
    - PXMeter-AB: **516 entries / 376 clusters**
    - FoldBench-AB: **104 / 160** — *as printed*. The caption states "the parenthesized pair is
      written as (number of entries/number of clusters)", which makes 160 clusters from 104 entries
      arithmetically impossible. Recorded verbatim; flagged in `unresolved`.
    - AF3-AB: **67 / 60**
  - **Ligand plausibility (p7, Table 1 caption):** PXM-22to25-Ligand, **623 test entries, 250
    clusters**.
  - **Broader benchmark suites (p14, Table 3 header):** FoldBench monomer 287/287, protein–ligand
    441/441, protein–protein 237/237; PXMeter monomer 769/500, protein–ligand 623/250,
    protein–protein 2126/1806.
  - **OF3p2 MSA/template sanity check (p14, Figure 10 p15):** common set of **267** FoldBench
    protein–protein interfaces.
  - **Antibody-design panel (Figure 1 p1, Figure 4A p4, Table 4 p16):** **13 distinct antigens / 15
    campaign bars.** Soluble: SOMA, UBC9, IDI2, AMBP (two separate epitopes = two campaigns), CEAM6,
    MTM1A, TACT, CD266 (labelled "CD226" in Figure 4A — see `unresolved`), IL-20, VEGF-A. GPCR:
    CCR5, CCR7, CCR8, GPRC5D — each run in **both VHH-Fc and mAb formats** (p5, Figure 1 p1).
  - **Cross-variant mini-binder study (p9):** 2 antigens (prototype and Omicron B.1.1.529 SC2RBD),
    **4 tested designs**.
  - **Training-set size:** **NOT REPORTED.** The paper never states how many structures, chains,
    clusters or tokens Protenix-v2 was trained on.
- **method_class**: **co-folding (structure prediction) + generative binder design.** p2: "Protenix-v2
  operates in two primary modes: (1) to predict and rank biomolecular structures, and (2) to generate
  and prioritize candidate binders for experimental validation." A third, smaller method component is
  **inference-time training-free guidance (TFG)** on the diffusion sampler for ligand geometry (p7).
  Tag `cofolding`. **Not** MSA-subsampling, **not** MSA-state-filtering, **not** template-state-bias,
  **not** MD, **not** enhanced sampling, **not** clustering, **not** benchmark-only. There is no tag
  in the v3 vocabulary for *de novo binder design*, which is half of this paper — see `unresolved`.
- **backbones**: **Protenix-v2 (this work)**, compared head-to-head against **Protenix-v1**,
  **AlphaFold3**, **Boltz-1**, **Boltz-1x**, **Boltz-2**, **Boltz-2x**, and **OpenFold3-preview2
  (OF3p2)** (Figure 2 p3, Figure 3 p3, Table 1 p7, Figure 7 p8, Table 3 p14). More than two backbones
  compared head to head → tag `multi-backbone`. Design-side comparators are **Chai-2** and
  **BoltzGen** hit rates (Figure 1 legend, p1), but those are published numbers on overlapping
  targets, not re-runs by these authors.
- **templates**: **NOT REPORTED for Protenix-v2.** The paper never states whether Protenix-v2 uses
  templates at inference. The *only* template statement in the PDF is about a **baseline**: "For
  OpenFold3-preview2 (OF3p2), we used an MMseqs2-derived MSA pipeline [24] **without templates**.
  This differs slightly from the setting described in the technical report [34]" (p14). Do not read
  that across to Protenix-v2.
- **msa_handling**: **NOT REPORTED for Protenix-v2.** Again the only MSA statement is about
  baselines: OF3p2 was run with an MMseqs2-derived MSA pipeline (p14), and the mismatch was quantified
  (69.29% vs 70.79% DockQ SR on 267 common interfaces, p14 / Figure 10 p15). No subsampling, no
  clustering, no state-filtering, no pinning is described anywhere for any model. The full/subsampled
  distinction cannot be established from this PDF.

## C. Conformational core

**Framing note.** This is a structure-prediction-and-design capability report. It reports a single
ranked prediction per target and evaluates it against a single deposited reference. Conformational
state is never an object of study, never a variable, and never a metric. The fields below say so
field by field rather than being silently blanked.

- **states_generated**: **one.** The reported quantity is always "the **ranked top-1** prediction at 5
  seeds" (Figure 2 caption, p3). Multiple samples *are* produced — the inference-time-scaling study
  runs the seed count from 1 to 1000 (Figure 3, p3) — but those samples are treated purely as a
  sampling budget for accuracy, collapsed by the model's own ranking score to a single reported
  structure, and never partitioned, clustered or labelled as distinct conformational states. I have
  deliberately **not** written `ensemble + single-state` here and have **not** applied the `ensemble`
  tag: the v3 note for that dual value describes a method that samples widely *and lands on a basin*,
  i.e. a paper in which basins are an object; here no basin, state or ensemble is ever defined. The
  seed sweep is an accuracy budget, not an ensemble. Flagged in `unresolved` as a judgement call.
  On the design side, generation produces many candidate *binders* (up to ~300 for VEGF-A, p6), which
  are distinct molecules, not distinct states of one molecule.
- **structural_priors_used**: **Substantial, and none of it is a methodological sin.**
  1. **Deposited structures define every benchmark reference.** "Input files for Protenix, Boltz, and
     OpenFold3 were generated from mmCIF structures using the gen-input module in PXMeter v1.1.0"
     (p14) — the *inputs* (sequence and chemical composition) are extracted from the ground-truth
     mmCIF files, which is the standard co-folding evaluation convention.
  2. **Antigen targets are chosen from deposited/commercially available proteins**, and the epitopes
     targeted are known functional interfaces: "aligning our epitope selection for novelty-filtered
     targets with the methodology used in the Chai-2 study [29], specifically **targeting native
     ligand-binding interfaces**" (p5). Native ligand-binding interfaces are prior structural/
     functional knowledge applied at design time.
  3. **Antibody frameworks are grafted from a solved therapeutic antibody**: "The designed Fv
     including VL and VH domains were grafted onto **Trastuzumab framework** as a full length mAb"
     (p15). VHH candidates were "formatted as VHH-Fc fusions with a C-terminal human IgG1 Fc (C220S)"
     (p15). Both are structural/sequence priors from known molecules.
  4. **Design specification can import known scaffolds**: "predefined frameworks or scaffolds can be
     integrated into the design specification to guide the generation process" (p3).
  5. **The dual-variant design was conditioned on both target structures jointly**: "when RBDs of both
     prototype and Omicron were jointly provided as inputs, Protenix-v2 generated 2 dual-binding
     mini-binders out of 4 tested designs" (p9).
  6. **Developability thresholds are calibrated against eleven clinical-stage reference antibodies**
     from Jain et al. (p17) — a prior-knowledge calibration set, correctly disclosed.
  None of these are conformational-state priors. There is **no state-annotated database, no
  GPCRdb/KLIFS/Kincore, no state-labelled template** anywhere in the paper.
- **oracle_leakage**: **All seven routes enumerated separately.** Summary: **no conformational-state
  oracle exists because no state is predicted. Pipeline leakage into structure prediction is not
  found; the real findings are (a) route 1 is under-specified because Protenix-v2's own input regime
  is never stated, and (b) genuine design-level (route 7) effects in panel and epitope selection,
  one of which was demonstrably decided after reading experimental outcomes.**

  1. **Structures used as input or template.** **NOT REPORTED / cannot be excluded, and this is the
     material gap.** For structure prediction, the input construction is disclosed only as: "Input
     files for Protenix, Boltz, and OpenFold3 were generated from mmCIF structures using the gen-input
     module in PXMeter v1.1.0. Since Boltz and OpenFold3 do not support ligands composed of multiple
     CCD codes or glycans, these components were excluded from their respective inputs. All models
     were run with 10 recycling iterations during inference." (p14). Whether Protenix-v2 was given
     templates is never stated (see `templates`). For design, the target is supplied as a structure —
     "Protenix-v2 enables flexible, target-conditioned generation that supports both precise
     epitope-targeting and site-agnostic design" (p2) — but the paper never says whether the target
     coordinates come from an experimental structure or a predicted model. Protocol pages: p2, p14.
  2. **State annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates or
     alignments.** **NONE FOUND.** No state-annotation database is named anywhere in the paper or its
     39 references. The only curated databases named are wwPDB/PDB (p2, p5), **SAbDab** (p5, used as a
     *novelty filter*, not a state annotation), and Sino Biological's antigen catalogue (Table 4,
     p16). Protocol described on p2, p5, p14.
  3. **Cluster labels derived from known states.** **NONE FOUND.** Clustering appears twice and
     neither instance is state-derived: (i) benchmark redundancy clustering, "the parenthesized pair
     is written as (number of entries/number of clusters)" (p3) and Table 3 header (p14); (ii) hit
     clustering by "antigen-aligned framework RMSD at 4 Å" (p6), i.e. binding-pose families of
     *designed binders*, not conformational states of the target. Protocol pages: p3, p6, p14.
  4. **Hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states.**
     **NONE FOUND for states** (no state exists to tune against). **Two adjacent findings recorded
     because they are the honest analogues, and neither is state leakage:**
     - The seed sweep is *reported* across the full evaluation set — "Figure 3 illustrates success
       rate curves up to 1000 seeds… Protenix-v2 consistently outperforms competitors across the
       entire explored seed range" (p4). Reporting a full curve on the evaluation set is disclosure,
       not tuning; no per-target seed count is selected.
     - The comparator selection rule was chosen by the authors and applied to the evaluation set:
       "Boltz-1 and AF3 FoldBench-AB results are from Xu et al. [37] and **we apply ranking score
       selector to the rest models for fair comparison**" (p3, Figure 2 caption). Disclosed, and
       applied uniformly, but it is an author-chosen selection rule on the evaluation set.
     - **No training/validation/test split, no hyperparameter-selection protocol, and no tuning
       description of any kind appears in the PDF.** The absence is total, so route 4 cannot be
       positively cleared beyond "no state-based tuning is possible in a paper with no states".
     Protocol pages: p2, p3, p14.
  5. **Success defined post hoc by RMSD or TM to a structure they had.** **PRESENT BY CONSTRUCTION on
     the structure-prediction side, and this is the standard convention, not a defect.** DockQ against
     the deposited reference at thresholds 0.23 / 0.49 / 0.8 (Figure 2 caption, p3); ligand success is
     "a joint success metric requiring both a pocket-aligned ligand RMSD below 2 Å and a validity
     pass" (p7). The mitigating fact is that these references are post-cutoff — see
     `anti_memorization_design`. **ABSENT on the design side**, which is the stronger claim: design
     success is defined by wet-lab BLI, not by RMSD to anything — "Positive binding candidates were
     identified based on an established threshold, defined as a binding response greater than the
     buffer background plus 0.05 nm" (p16).
  6. **Best/worst model labels assigned against a held reference.** **NONE FOUND — explicitly
     cleared.** Model selection is by the model's own ranking score, stated in the figure caption:
     "Success rates are reported across three benchmark collections using **the ranked top-1
     prediction** at 5 seeds" (p3). Nowhere does the paper report an oracle/best-of-N number selected
     against the reference. Protocol page: p3.
  7. **Design-level oracle use — inputs or systems chosen because the expected answer is known.**
     **PRESENT, and labelled design-level, not pipeline leakage.** Three separate instances:
     - **Panel construction is availability-filtered, not pre-registered:** "Rather than reproducing
       the full target panels from prior studies [23, 29], **we first restricted attention to
       antigens that were available for immediate experimental follow-up, and then sampled from that
       in-stock pool** to cover several published novelty regimes and target classes" (p5). The panel
       is a convenience sample from a stock list, then post-hoc mapped onto other papers' novelty
       regimes; comparator coverage is likewise conditional — "Direct comparisons are shown only where
       published VHH baselines are available" (p5).
     - **Epitope selection was revised after reading experimental outcomes:** "When targeting two
       different epitopes on the same AMBP protein, Protenix-v2 yielded hit rates of 4% and 48%,
       respectively. This variance highlights that the choice of surface patch can alter the
       difficulty of de novo design. **Consequently, we determined that aligning our epitope selection
       for novelty-filtered targets with the methodology used in the Chai-2 study [29], specifically
       targeting native ligand-binding interfaces.**" (p5). The selection rule for the reported panel
       was fixed *after* an experimental result on that panel was known. This is the single most
       consequential rigour observation in the paper.
     - **Comparator train-overlap is disclosed rather than excluded:** "while Protenix-v2-TFG is
       already comparable to Boltz-2x, the latter is shown for reference only, because its 2023
       training cutoff means that part of this evaluation set may overlap with its training data"
       (p7); Table 1 labels the two rows "Boltz-2 (train overlap)" and "Boltz-2x (train overlap)"
       (p7). Correct practice, recorded here because it is the authors' own leakage annotation.
     Tag `design-level-oracle`, **not** `oracle-leak`.
- **prospective**: **partial — and the split is clean.** **Prospective on the design side:** binders
  were generated and then tested in the lab against antigens for which no such binder existed;
  success is a BLI readout, not a comparison to a known answer (p5–6, p16). The GPCR campaigns are
  the strongest case — 16–30 designs tested per target with no prior binder to recover.
  **Retrospective on the structure-prediction side by construction:** every DockQ and RMSD number is
  scored against a deposited structure that already exists (p3, p7, p14). **Neither arm is
  pre-registered**, and panel/epitope selection was revised mid-study (route 7 above), so the design
  arm is prospective in execution but not pre-specified in design. Tag `prospective` applied on the
  strength of the wet-lab arm, with this caveat.
- **state_metric**: **NOT APPLICABLE — no conformational state is ever called, by any means.** For
  completeness, the predicates actually used, since they are the closest analogues and are worth
  having in the corpus:
  - **Interface quality:** DockQ binary thresholds **> 0.23** (acceptable, the headline), **> 0.49**
    (medium), **> 0.8** (high) — Figure 2 caption, p3. No justification of these thresholds is given;
    they are the DockQ community conventions used without citation on p3.
  - **Ligand pose:** joint predicate of **pocket-aligned ligand RMSD < 2 Å AND validity pass**,
    reported under the original PoseBusters criterion and a stricter "Revised" criterion (p7,
    Table 1). The revised criterion adds "planarity around sp2 carbon centers, planarity of amide
    groups, and non-planarity at sp3 carbon and nitrogen centers" (p7).
  - **Monomer:** LDDT; **protein–ligand:** "RMSD < 2 & LDDT > 0.8 percentage"; **protein–protein:**
    DockQ > 0.23 success rate (Table 3 caption, p14).
  - **Binding hit (design):** "a binding response greater than the buffer background plus 0.05 nm" at
    1000 nM single-concentration BLI, with most hits confirmed by multi-concentration K_D and "showed
    KD lower than 1000 nM" (p16).
  - **Binding-mode diversity:** structural clustering at **4 Å antigen-aligned framework RMSD** (p6).
  - **Developability:** Tm > 60 °C (DSF); corrected BVP score < 5.3; AC-SINS red shift < 11 nm — all
    three thresholds taken from Jain et al. and recalibrated on eleven in-house reference antibodies
    (Table 5 and text, p17). These are the only thresholds in the paper given an explicit
    justification and citation.
  Tag `binary-predicate`.
- **metric_saturation**: **YES — numeric ceiling in at least three reported arms.**
  1. **Figure 7 (p8), revised-validity subitem breakdown:** ground-truth structures sit at or
     essentially at **100.0%** on most of the ten checks, and the authors say so explicitly: "The
     near-100% pass rate of ground-truth structures on these checks further justifies the inclusion of
     the newly introduced metrics" (p8–9). Several model bars (Tetrahedral chirality, Volume overlap
     with protein, Min distance to inorganic cofactors) are also at ~100%, leaving no headroom.
  2. **Target-level design success is at the ceiling:** "Protenix-v2 achieves a 100% target-level
     success rate, meaning at least one experimentally confirmed binder was discovered for every
     antigen tested" (p5). A 13/13 result cannot discriminate further; the informative quantity is the
     per-target hit rate, which ranges 2%–88%.
  3. **Thermostability pass rate is exactly at the ceiling: 100.0%** (Figure 5 caption, p6;
     "100% for thermostability", p5).
  The truncated y-axis of Figure 7 is a **figure** defect and is recorded in `hides` on that row, not
  duplicated here, per the v3 rule.
- **directional_control**: **YES for design; NO for conformational state. This distinction is the
  whole answer, so it is spelled out.**
  - **What the paper CAN be instructed to do (all quoted from p2–p3):** "Protenix-v2 enables flexible,
    target-conditioned generation that supports both **precise epitope-targeting** and **site-agnostic
    design**. Its capabilities span diverse protein-binder classes, ranging from miniproteins and
    modular antibody formats such as variable domain of heavy chain of heavy-chain antibody (VHH), and
    variable fragment (Fv) including variable domain of heavy chain (VH) and compatible variable
    domain of light chain (VL). In antibody settings, Protenix-v2 **empowers users with granular
    control over binding regions: complementarity-determining region (CDR) loops can be independently
    assigned with specified length ranges, while predefined frameworks or scaffolds can be integrated
    into the design specification to guide the generation process.**" (p2–3). Named handles therefore:
    **target structure; epitope specification (or none); binder format/class; per-CDR loop length
    ranges; predefined framework or scaffold.**
  - **A second, chemistry-level handle:** the TFG variants "impose constraints on **chirality,
    planarity, torsional geometry, and pairwise distances**, thereby guiding the generative process
    toward ligand conformations that better satisfy fundamental stereochemical and geometric
    requirements" (p7), drawing on training-free guidance, projected diffusion and SHAKE. This is
    inference-time guidance on the diffusion sampler toward *local chemical validity*, not toward a
    named conformational state, and it acts on geometric constraints rather than on an internal
    representation tensor — so I have **not** tagged `latent-steering`; see `unresolved`.
  - **A third, multi-target handle:** joint conditioning on two antigen variants at once — "when RBDs
    of both prototype and Omicron were jointly provided as inputs" (p9).
  - **What the paper CANNOT be instructed to do:** there is **no handle of any kind for the
    conformational state of the target**. No partner-driven, ligand-driven, nanobody-driven,
    G-protein-mimetic, state-annotated-template or state-filtered-MSA mechanism is offered, discussed,
    or mentioned. The GPCR work treats receptor flexibility only as a *difficulty* to be overcome —
    "the exposed receptor surface is often limited, flexible, and poorly suited to conventional
    antibody discovery workflows" (p5) — never as something to be controlled or resolved. **Protenix-v2
    adds no conformational-state, multi-state, or state-controllability capability whatsoever.**
    Tags `directed-state` and the other Control tags are therefore **withheld** except `peptide-driven`
    /`nanobody`-adjacent design, which are about the *designed molecule*, not about steering the
    target's state — so those are withheld too, deliberately.
- **anti_memorization_design**: **YES — a training cutoff plus three distinct held-out constructions.**

  **THE TRAINING CUTOFF, VERBATIM, p2 (§2 Methods, second paragraph of the section):**

  > "To ensure rigorous evaluation and prevent data leakage, **Protenix-v2 is trained without wwPDB
  > [3] entries released on or after 2021-09-30.** This training cutoff aligns with established
  > conventions in recent models [8, 28, 34], ensuring that all reported results in structure
  > prediction and zero-shot design are assessed against truly novel or held-out data." — **p2**

  So the cutoff is **2021-09-30**, stated as an exclusive lower bound on exclusion ("released *on or
  after*" 2021-09-30 is excluded; the last included day is 2021-09-29). It is stated **once**, in that
  one sentence, and nowhere else in the paper.

  **Did the cutoff change from v1?** **The paper does not say.** It gives **no numeric cutoff for any
  earlier Protenix version**, and makes only the indirect claim that "This training cutoff aligns with
  established conventions in recent models [8, 28, 34]" (p2) — where [8] is the earlier Protenix
  report (Chen et al., bioRxiv 2025, doi 10.1101/2025.01.08.631967, p11), [28] is Chai-1, and [34] is
  the OpenFold3-preview-2 technical report. That sentence asserts *alignment with a convention*, which
  is the closest the paper comes to saying the date is unchanged, but **it is not a statement that
  Protenix-v1's cutoff was 2021-09-30, and it must not be cited as one.** The only other cutoff date
  in the paper belongs to a competitor: "its 2023 training cutoff" for Boltz-2/Boltz-2x (p7). Anyone
  citing a Protenix cutoff must cite **this** paper for 2021-09-30 as Protenix-v2's cutoff, and must
  go to the relevant earlier report for any earlier version's date. See `unresolved`.

  **Held-out set constructions, each with n and how it was defined:**
  1. **PXM-22to25-Ligand — post-cutoff by construction. n = 623 entries / 250 clusters.** "We evaluate
     our methods and several comparison baselines on the PXM-22to25-Ligand test set, which comprises
     protein–ligand complexes **released between 2022 and 2025** and therefore provides a challenging
     test of model performance on recent structures" (p7). Every entry postdates 2021-09-30.
  2. **Novelty-Filtered design targets — antibody-novelty filter, not structure-novelty.** "We also
     included targets from the available pool **after excluding antigens and homologs in SAbDab
     released prior to our training cutoff**, following the novelty-filtering logic used in Chai-2"
     (p5). Note carefully what this excludes: antigens with *known antibody complexes* in SAbDab. It
     does **not** exclude antigens whose apo or non-antibody structures are in the training set. n:
     not stated as a count; from Figure 1 (p1) the "Antibody-filtered novel targets" box contains 7
     antigens (SOMA, UBC9, IL-20, NTM1A, CD226, TACT, CEAM6).
  3. **Low-Homology Monomers — sequence-identity filter.** "we included monomeric targets satisfying
     the very-low-homology setting emphasized by BoltzGen, namely proteins that are **highly dissimilar
     to any earlier protein in the PDB under a 30% sequence identity threshold**" (p5). n = 2 from
     Figure 1 (AMBP, IDI2).
  4. **GPCR panel: no novelty or cutoff filter is claimed at all.** The GPCR targets are introduced
     purely on difficulty grounds (p5). CCR5/CCR7/CCR8/GPRC5D are not stated to satisfy any
     novelty criterion.
  5. **Antibody-antigen structure benchmarks (PXMeter-AB, FoldBench-AB, AF3-AB): cutoff basis NOT
     REPORTED in this PDF.** The paper does not state the release-date range of any of the three
     antibody benchmark collections, so their post-cutoff status cannot be verified from this document.
     Same for the FoldBench/PXMeter suites in Table 3 (p14).
- **anti_memorization_control**: **RUN, on the ligand arm and on the design arm; NOT RUN on the
  antibody-antigen structure arm. Design arm is UNPOWERED at the target level.**
  - **Run and analysed (ligand):** the entire §5.1 comparison is executed on the post-cutoff
    PXM-22to25-Ligand set (n = 623 entries / 250 clusters) with results in Table 1 and Figure 7 (p7–8).
    Crucially, the authors also **run and report the leakage-confounded comparator explicitly rather
    than dropping it**, annotating it: Table 1 rows "Boltz-2 (train overlap)" and "Boltz-2x (train
    overlap)", with the text "the latter is shown for reference only, because its 2023 training cutoff
    means that part of this evaluation set may overlap with its training data" (p7). That is a genuine,
    analysed leakage control on a competitor.
  - **Run and analysed (design):** the novelty-filtered and low-homology panels are actual wet-lab
    campaigns with BLI outcomes (Figure 1 p1, Figure 4A p4). **UNPOWERED at the target level**: 13
    antigens / 15 campaigns total, of which the low-homology arm is n = 2 antigens and the GPCR arm is
    n = 4 antigens × 2 formats. Per-target design counts are healthier (16–71 designs, 15–49 sent to
    BLI, Figure 4A p4), but the unit of the headline claim ("100% target-level success rate", p5) is
    the target, and n = 13 there.
  - **NOT RUN (antibody-antigen structure prediction):** no post-cutoff subset, no
    date-stratified arm, and no memorization control of any kind is run on PXMeter-AB, FoldBench-AB or
    AF3-AB. The 9–13 point gain over Protenix-v1 (p3) is reported on sets whose date composition is
    never stated. This is the cleanest gap in the paper.
  - Tag `anti-memorization` (a cutoff and post-cutoff arms genuinely exist and were run) — but note
    the antibody arm is uncontrolled, and tag `unpowered` for the 13-target design panel.
- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Post-cutoff ligand test set (PXM-22to25-Ligand, 2022–2025 releases, n = 623/250) | Memorization of ligand poses released before 2021-09-30 | p7 |
| Competitor train-overlap annotation (Boltz-2, Boltz-2x flagged "(train overlap)", shown "for reference only") | A leakage-inflated baseline being read as a fair comparator | p7, Table 1 |
| TFG ablation: Protenix-v1 vs Protenix-v1-TFG, Protenix-v2 vs Protenix-v2-TFG | That the plausibility gain comes from the base model rather than from the inference-time guidance | p7, Table 1 |
| Ground-truth structures scored through the same revised-validity checks | That the new sp2/sp3/amide-planarity checks are themselves unpassable or mis-specified | p8, Figure 7; text p8–9 |
| Original PoseBusters criterion reported alongside the Revised criterion | That the gain is an artefact of the authors' own stricter metric definition | p7, Table 1 |
| Baseline-inference-setting check: OF3p2 with authors' MMseqs MSA vs public FoldBench result, on 267 common interfaces (69.29% vs 70.79%) | That the OF3p2 baseline was crippled by the authors' MSA/template choice | p14, Figure 10 p15 |
| Ranked top-1 by the model's own ranking score, applied uniformly ("we apply ranking score selector to the rest models for fair comparison") | Oracle best-of-N selection inflating any model's success rate | p3, Figure 2 caption |
| Two epitopes on the same antigen (AMBP, hit rates 4% vs 48%) | That per-target hit rate is a property of the target alone rather than of the chosen surface patch | p5, Figure 4A p4 |
| Human expert ranker vs Ranker A vs Ranker B, ~300 VEGF-A candidates, 30 selected each | That model ranking merely reproduces expert intuition | p6, Figure 6 |
| Same GPCR targets run in two formats (VHH-Fc and mAb) | That the hit rate is format-specific rather than a property of the design method | p5, Figure 1 p1 |
| Eleven clinical-stage reference antibodies (Jain et al.) run alongside designs on every developability assay | Instrument- and lab-specific drift in developability pass thresholds | p17, Table 5 |
| Additional ELISA references (infliximab, bevacizumab, lenzilumab, gantenerumab) with linear-regression normalization of BVP scores | Plate/run-to-run drift in the polyreactivity readout | p17 |
| BLI buffer-background threshold (response > background + 0.05 nm), then multi-concentration K_D confirmation | Non-specific or background binding being scored as a hit | p16 |
| VEGF-A binders built as His6 rather than Fc fusions | Avidity from the Fc dimer being mistaken for affinity, given VEGF-A's homodimeric state | p15 |
| GPRC5D K_D explicitly flagged as measured under avidity conditions | The 112 pM figure being read as a monovalent affinity | p5, Figure 4 caption p4 |
| Prior-generation PXDesign mini-binders (SC2RBD Binder 4/14) measured against both RBDs alongside the new designs | That cross-variant binding is a property of any binder to this epitope rather than of the new dual-conditioned designs | p9, Table 2 |
| SEC-HPLC purity gate (>90%) and SDS-PAGE identity check before any kinetic assay | Aggregate or mis-assembled material driving the binding readout | p15 |

  **Controls NOT run, and their absence is total:** no scrambled/shuffled sequence arm, no
  non-binding decoy design arm, no irrelevant/off-target antigen arm for the designed antibodies, no
  apo arm, no negative-control designs of any kind, and no isotype control antibody. Every design that
  entered BLI was a design the model proposed.
- **confidence_as_discriminator**: **YES for accuracy-oriented selection and for binder
  prioritization; NEVER for conformational correctness (there is no conformational judgement to
  make). What the confidence machinery actually predicts is NOT REPORTED.**
  - **The words pLDDT, pTM, ipTM, PAE and "confidence" appear nowhere in this paper.** What exists
    instead is a **"ranking score"** and two **"rankers"**, and neither is defined.
  - **Structure prediction:** results are "the **ranked top-1** prediction at 5 seeds" (p3, Figure 2
    caption), and the same rule is imposed on baselines: "we apply **ranking score selector** to the
    rest models for fair comparison" (p3). What that score is a function of, what it is trained to
    predict, and how it was validated are all **NOT REPORTED**.
  - **Design:** "We compared a human expert with **two rankers integrated in Protenix-v2 (Ranker A and
    Ranker B)** on approximately 300 designed VHH candidates, each selecting 30 for experimental
    validation" (p6). Ranker A and Ranker B are never described — no architecture, no training
    objective, no score definition, no explanation of how they differ.
  - **The one genuine validation, and it is a real one:** the rankers were validated *prospectively
    against wet-lab outcome*, not against a held structure. "Ranker A and Ranker B identified 9 and 10
    binders, respectively, with 5 overlapping hits. Each model also contributed unique binders (4 for
    Ranker A and 5 for Ranker B), indicating complementary strengths. Also, the human expert
    identified 7 binders, all of which were unique and showed no overlap with either model. These
    results suggest that the rankers capture binding-relevant features that are largely orthogonal to
    human intuition." (p6) Plus Figure 6: "The model rankers recover more high-response binders, while
    the human expert tends to select weaker-response candidates… Human selections span a broader set
    of clusters, whereas the model rankers concentrate more strongly on a smaller number of productive
    clusters" (p6). So the claim is: **model ranking beats a human expert on hit yield and on binding
    response, at the cost of diversity.** n = 30 selections per ranker from ~300 candidates, on a
    single target (VEGF-A). Single-target, small-n, and unblinded (no statement that the human expert
    was blinded to model scores).
  - **No validation whatsoever** is offered for the structure-prediction ranking score: no
    correlation-with-DockQ analysis, no calibration plot, no oracle-vs-ranked gap.
  - Tag `confidence-as-discriminator` applied, **scoped to accuracy/binding selection**, not to
    conformational-state discrimination.

## D. Claims

- **central_conclusion**: Protenix-v2 is a single system that (a) substantially improves
  antibody–antigen interface prediction over Protenix-v1 and over AF3/Boltz-1/OF3p2 — 9 to 13 DockQ
  success-rate points at DockQ > 0.23 across three benchmark collections, with 5-seed performance
  exceeding Protenix-v1 at 1000 seeds — and (b) does zero-shot antibody design well enough to yield
  BLI-confirmed, developable, structurally diverse hits on every antigen in a 13-target panel,
  including four GPCRs, under 16–30 tested designs per GPCR target. Two secondary results: an
  inference-time guidance variant (TFG) that raises ligand-pose chemical plausibility under a stricter
  validity criterion the authors also introduce, and a pair of cross-variant SARS-CoV-2 RBD
  mini-binders with nanomolar K_D against both prototype and Omicron.
- **necessity_claims** (**verbatim + page**; the paper is conspicuously light on hard necessity
  language — there is no "requires", "essential" or "impossible" claim about method design anywhere):
  - p2: "To ensure rigorous evaluation and prevent data leakage, Protenix-v2 is trained without wwPDB
    [3] entries released on or after 2021-09-30."
  - p5: "Binding alone is not sufficient for practical antibody discovery. Successful antibody hits
    **must** also show favorable developability, including drug-like biophysical properties."
  - p7: "Ensuring the physical plausibility of predicted small-molecule structures is **critical** in
    ligand binding pose prediction, because strong agreement with the reference under conventional
    geometric metrics does **not necessarily guarantee** a chemically realistic local geometry."
  - p7: "our manual case review shows that good performance on the standard validity checks does
    **not imply** that predicted ligands satisfy other basic forms of chemical plausibility that are
    also important to medicinal chemists."
  - p9: "Breadth-oriented binder design provides a stringent test for Protenix-v2, as effective
    candidates **must** retain binding across variants with substantial sequence and epitope
    differences."
  - p2: "In practice, this **requires** models that can resolve not only folded structures but also
    interfaces and the quality of candidate interactions across diverse molecular settings."
  - p14: "Since Boltz and OpenFold3 do **not support** ligands composed of multiple CCD codes or
    glycans, these components were excluded from their respective inputs."
  - p15: "**Only** protein batches with a purity of greater than 90% as determined by SEC-HPLC were
    utilized for subsequent kinetic assays."
- **novelty_claims** (**verbatim + page**; note that **the words "first", "novel method",
  "unprecedented" and "for the first time" do not appear anywhere in this paper** — "novel" occurs
  only as "novel targets"/"target novelty"/"truly novel … data". The claims below are superiority and
  capability-extension claims, not priority claims. That restraint is itself the finding.):
  - p1 (abstract): "Protenix-v2 achieves antibody-antigen success rates with **up to 13-point gains
    over Protenix-v1**, while **5-seed performance surpasses previous 1000-seed results**."
  - p1 (abstract): "On the design side, Protenix-v2 demonstrates a **100% target-level success rate**
    in novelty-controlled VHH-Fc campaigns, reaching hit rates up to 48%."
  - p1 (abstract): "**Crucially, the model enables hit discovery on difficult GPCR targets** with hit
    rates of 16%–88% (VHH-Fc) and up to 50% (mAb) under 16–30 testing budgets per target."
  - p2: "Crucially, the model demonstrates a **massive leap in sampling efficiency**: its 5-seed
    performance notably surpasses previous 1000-seed results."
  - p4: "Remarkably, Protenix-v2 at only 5 seeds already exceeds the performance of Protenix-v1 at
    1000 seeds, indicating a clear gain in efficiency."
  - p4: "In direct comparisons, **Protenix-v2 moves from approximate parity with AlphaFold3 to a
    clear leading position in antibody-antigen modeling.**"
  - p5: "The design results reported here **move beyond the protein-binder focus of prior PXDesign
    work [32]** to achieve robust zero-shot antibody generation."
  - p6: "These results suggest that the rankers capture binding-relevant features that are **largely
    orthogonal to human intuition**."
  - p8–9: "These results further show that **existing models still exhibit significant weaknesses in
    generating chemically plausible small-molecule geometries**, even when they perform well under the
    original criterion."
  - p1/p2 (identical sentence): "These results **establish Protenix-v2 as a robust and powerful model
    for accelerated drug discovery**."
- **stated_limits**: **There is no limitations section, and the self-criticism is limited to
  in-line hedges.** Everything the authors concede, with pages:
  - Panel scope is acknowledged as a convenience sample and as provisional: "Rather than reproducing
    the full target panels from prior studies [23, 29], we first restricted attention to antigens that
    were available for immediate experimental follow-up" (p5); "a 100% target-level success rate **in
    the current panel**" (p2); "**The current** hit rates, developability, and diversity results are
    summarized in Figures 1 and 4 to 6" (p5); "Table 2 summarizes the **current** dual-binding SC2RBD
    results" (p10).
  - Comparability of design baselines is incomplete: "Direct comparisons are shown only where
    published VHH baselines are available, since some overlapping Chai-2 targets were reported only in
    scFv format" (p5).
  - Hit rate depends on a choice the model does not make: "This variance highlights that the choice of
    surface patch can alter the difficulty of de novo design" (p5).
  - The competitor comparison is explicitly not apples-to-apples: "the latter is shown for reference
    only, because its 2023 training cutoff means that part of this evaluation set may overlap with its
    training data" (p7).
  - The baseline's inference setting is not the published one: "This differs slightly from the setting
    described in the technical report [34]… We therefore view the mismatch in MSA/template features as
    **real but modest** in its effect on overall PPI performance" (p14).
  - The mechanistic structural story is admitted to be speculative: "we performed **preliminary
    analysis** to understand the design" (p9), with the mechanism described throughout in hedged terms
    — "**may** form polar interactions", "**likely** participate", "**potential** compensatory
    mechanisms" (p9).
  - One K_D is not a monovalent affinity: "The K_D* of GRPC5D is measured under avidity conditions due
    to the antigen's native dimeric state" (p4, Figure 4 caption; repeated p5).
  - The broader benchmarks are downgraded relative to the headline: "In this broader view, Protenix-v2
    remains **competitive** across all three interaction categories, while the main-text
    antibody-focused and ligand-related analyses provide the clearest picture of its strongest
    practical gains" (p14).
  - **Not conceded anywhere:** the absence of any architecture description; the absence of any
    training-set description; the absence of Protenix-v2's own MSA/template setting; the absence of
    negative-control designs; the date composition of the three antibody benchmarks; and that one mAb
    campaign returned 0% (stated on p5 in the number list but never discussed).
- **stance**: **`background` + `contrast` — PROVISIONAL, the user's call.**
  - **`background`**: this is the citation of record for what Protenix-v2 is and, more importantly,
    for **its 2021-09-30 training cutoff** — the anchor any held-out-set argument built against
    Protenix must cite. It is a backbone/tooling paper, not a competitor on our axis.
  - **`contrast`**: it is a 2026 state-of-the-art co-folding system from a major industrial lab that
    **adds no conformational-state capability at all**, treats receptor flexibility only as an
    obstacle to be routed around (p5), and reports a single ranked top-1 structure per target even
    while running up to 1000 seeds. That is a clean, current, high-profile demonstration that the
    frontier of co-folding is moving toward interfaces and design rather than toward states.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| DockQ > 0.23 success rate, ranked top-1, 5 seeds | **49.7** (Protenix-v2); 40.2 (Protenix-v1); 27.9 (OF3p2); 19.6 (Boltz-1); AF3 N/A | % of entries | PXMeter-AB, n = 516 entries / 376 clusters | p3, Fig 2 |
| DockQ > 0.23 success rate, ranked top-1, 5 seeds | **65.0** (Protenix-v2); 52.3 (Protenix-v1); 48.8 (AF3); 34.9 (OF3p2); 34.4 (Boltz-1) | % of entries | FoldBench-AB, n = 104 / 160 as printed | p3, Fig 2 |
| DockQ > 0.23 success rate, ranked top-1, 5 seeds | **53.5** (Protenix-v2); 40.4 (Protenix-v1); 47.0 (AF3); 30.9 (OF3p2); 14.9 (Boltz-1) | % of entries | AF3-AB, n = 67 / 60 | p3, Fig 2 |
| Absolute gain over Protenix-v1 at DockQ > 0.23 | **9 to 13** (author's phrasing); 9.5 / 12.7 / 13.1 by subtraction from Fig 2 | percentage points | the three AB collections above | p3 (text), p1–2 (abstract "up to 13-point") |
| DockQ > 0.8 (high-quality) subset | "gains at DockQ > 0.8 are comparably large" — **no numeric value is given in text or table**; readable only as stacked-bar segments in Fig 2 | % of entries | the three AB collections | p3 |
| Seed efficiency | Protenix-v2 at **5 seeds** exceeds Protenix-v1 at **1000 seeds** | seeds | same three AB collections | p2, p4, Fig 3 |
| RMSD < 2 Å & validity joint success, Revised criterion | **60.46** (Protenix-v2-TFG); 61.11 (Protenix-v1-TFG); 49.22 (Protenix-v2); 48.14 (Protenix-v1); 53.96 (Boltz-1x); 34.38 (Boltz-1); 62.86 (Boltz-2x, train overlap); 51.25 (Boltz-2, train overlap) | % | PXM-22to25-Ligand, n = 623 entries / 250 clusters | p7, Table 1 |
| RMSD < 2 Å & validity joint success, original PoseBusters criterion | **60.53** (Protenix-v2-TFG); 61.11 (Protenix-v1-TFG); 50.42 (Protenix-v2); 48.37 (Protenix-v1); 55.59 (Boltz-1x); 35.56 (Boltz-1); 63.51 (Boltz-2x); 51.31 (Boltz-2) | % | PXM-22to25-Ligand, n = 623 / 250 | p7, Table 1 |
| Monomer LDDT | **89.1** (Protenix-v2); 88.6 (Protenix-v1); 88.0 (AF3); 86.8 (OF3p2) | LDDT ×100 | FoldBench monomer, n = 287/287 | p14, Table 3 |
| Protein–ligand: RMSD < 2 Å & LDDT > 0.8 | **64.0** (Protenix-v2); 62.5 (Protenix-v1); 62.6 (AF3); 56.6 (OF3p2) | % | FoldBench protein–ligand, n = 441/441 | p14, Table 3 |
| Protein–protein DockQ > 0.23 success rate | **73.0** (Protenix-v2); 72.7 (Protenix-v1); 71.7 (AF3); 66.4 (OF3p2) | % | FoldBench protein–protein, n = 237/237 | p14, Table 3 |
| Monomer LDDT | **88.0** (Protenix-v2); 87.2 (Protenix-v1); 85.4 (OF3p2); AF3 not reported | LDDT ×100 | PXMeter monomer, n = 769/500 | p14, Table 3 |
| Protein–ligand: RMSD < 2 Å & LDDT > 0.8 | **49.2** (Protenix-v2); 48.1 (Protenix-v1); 47.9 (OF3p2) | % | PXMeter protein–ligand, n = 623/250 | p14, Table 3 |
| Protein–protein DockQ > 0.23 success rate | **73.9** (Protenix-v2); 72.9 (Protenix-v1); 63.4 (OF3p2) | % | PXMeter protein–protein, n = 2126/1806 | p14, Table 3 |
| Target-level design success rate | **100** (at least one BLI-confirmed binder per antigen) | % of targets | 13-antigen VHH panel | p1, p5 |
| BLI-confirmed VHH-Fc hit rate, soluble/novelty-filtered targets | **2 to 48** | % of designs sent to BLI | soluble antigen panel | p1, p5, Fig 4A p4 |
| Per-target hit rates, soluble (Protenix-v2) | SOMA 24; UBC9 14; IL-20 38; NTM1A 4; CD226 14; TACT 2; CEAM6 20; VEGF-A 30; AMBP 4 and 48 (two epitopes); IDI2 24 | % | Figure 1 badges | p1, Fig 1 |
| Published comparator hit rates on overlapping targets | Chai-2: SOMA 14, UBC9 0, NTM1A 6; BoltzGen: AMBP 0, IDI2 7 | % | same antigens, published numbers not re-run here | p1, Fig 1 |
| GPCR VHH-Fc hit rates | **16, 62, 40, 88** (CCR5 16, CCR8 62, GPRC5D 40, CCR7 88 per Fig 1) | % of 16–30 tested designs | 4 GPCR targets | p5 (text); p1, Fig 1 |
| GPCR mAb hit rates | **0, 17, 50, 44** per text; Figure 1 shows GPRC5D 50, CCR7 43, CCR8 17 (CCR5 not shown) | % of 16–30 tested designs | same 4 GPCR targets | p5 (text); p1, Fig 1 |
| Testing budget per GPCR target | **16–30** | designs tested | GPCR campaigns | p1, p5 |
| Lowest K_D achieved, GPRC5D VHH-Fc | **112** (avidity conditions, not monovalent) | pM | BLI multi-concentration | p5; Fig 4C p4 |
| Representative K_D, other VHH binders | IDI2 **38**; IL-20 **23.8** | nM | BLI multi-concentration | Fig 4C, p4 |
| Developability pass rate — thermostability (DSF, Tm > 60 °C) | **100.0** | % of candidates | designed VHH/mAb hits vs 11 clinical-stage references | p5, p6 Fig 5, p17 |
| Developability pass rate — self-interaction (AC-SINS, red shift < 11 nm) | **97.5** (Fig 5 caption) / **98** (text p5) | % of candidates | same | p5, p6 Fig 5, p17 |
| Developability pass rate — polyreactivity (BVP ELISA, corrected score < 5.3) | **93.3** (Fig 5 caption) / **93** (text p5) | % of candidates | same | p5, p6 Fig 5, p17 |
| Binding-mode diversity | multiple structural clusters per campaign; per-campaign cluster counts 1–11 from Fig 4A | clusters at 4 Å antigen-aligned framework RMSD | designed hits | p6, Fig 4A p4 |
| VEGF-A ranking: binders found from 30 selections | Ranker A **9**; Ranker B **10**; human expert **7**; 5 overlapping between rankers; 4 and 5 unique respectively; all 7 human hits unique | binders | ~300 designed VHH candidates | p6, Fig 6 |
| Cross-variant mini-binder K_D (prototype / Omicron B.1.1.529) | Design 1: **250 / 148**; Design 2: **201 / 146**; prior PXDesign SC2RBD Binder 4: 10.1 / weak, not measured; Binder 14: 10.3 / no binding | nM | BLI | p9, Table 2 |
| Cross-variant design yield | **2 of 4** tested designs dual-binding | designs | SC2RBD | p9 |
| OF3p2 baseline setting check | **69.29** (authors' MMseqs MSA, no templates) vs **70.79** (public FoldBench result); ≈1.5 points lower | % DockQ ≥ 0.23 SR | 267 common FoldBench PPIs | p14; Fig 10 p15 |
| Revised-validity subitem pass rates | ~92.5–100 across ten checks; largest model-vs-ground-truth gaps at sp2-center flatness and sp3-center non-flatness; ground truth ≈100 | % | PXM-22to25-Ligand, ligand-containing structures | p8, Fig 7 |

- **n_predictions**: **recorded at every level separately.**
  - **Structure prediction — samples per target:** **5 seeds** is the reported default for every
    headline number ("the ranked top-1 prediction at **5 seeds**", p3). The scaling study sweeps
    **1, 2, 5, 10, 20, 50, 100, 200, 500, 1000 seeds** (Figure 3 x-axis tick labels, p3). Inference
    used **10 recycling iterations** for all models (p14). Whether one structure or several diffusion
    samples are drawn per seed is **NOT REPORTED**.
  - **Structure prediction — targets:** see `n_targets`. Totals across benchmarks are **not** given by
    the paper; the largest single set is PXMeter protein–protein at 2126 entries / 1806 clusters
    (p14).
  - **Structure prediction — total predictions:** **NOT REPORTED**, and not derivable, since the
    seed-sweep panels do not state which subsets were run at which seed counts.
  - **Design — raw designs generated per target** (Figure 4A grey bars, p4): VEGF-A **71**; SOMA,
    UBC9, CEAM6, NTM1A, TACT, CD226, IDI2, AMBP-epitope-1 **50** each; AMBP-epitope-2 **27**; IL-20
    **24**; GPRC5D **30**; CCR8 **26**; CCR5 **19**; CCR7 **16**. Separately, the VEGF-A ranking study
    says "**approximately 300** designed VHH candidates" (p6) — see `unresolved` for this conflict
    with the 71 in Figure 4A.
  - **Design — sent to BLI per target** (Figure 4A blue bars, p4): 41, 45, 43, 42, 38, 28, 40, 49, 47,
    24, 19, 25, 22, 15, 16 (in the plotted order VEGF-A, SOMA, UBC9, CEAM6, NTM1A, TACT, CD226, IDI2,
    AMBP-ep1, AMBP-ep2, IL-20, GPRC5D, CCR8, CCR5, CCR7). GPCR budget stated in text as **16–30
    designs per target** (p1, p5).
  - **Design — confirmed hits per target** (Figure 4A green bars, p4): 21, 12, 7, 10, 2, 1, 7, 12, 2,
    13, 9, 12, 16, 3, 14.
  - **Design — structural clusters among hits** (Figure 4A yellow bars, p4): 11, 7, 2, 4, 2, 1, 3, 9,
    2, 8, 6, 5, 8, 2, 3.
  - **Design — ranking study:** 30 candidates selected each by human expert, Ranker A, Ranker B, from
    ~300 (p6).
  - **Design — cross-variant:** **4** designs tested, 2 dual binders (p9).
  - **Total molecules expressed and assayed:** **NOT REPORTED** as a single figure; summing the
    Figure 4A blue bars gives 494 across the 15 campaigns, but the paper never states this total.
- **comparable_to_ours**:
- **si_in_scope**: **NO EXTERNAL SI — but two headline result families are figure-only, which is the
  same practical problem.** There is no supplementary file, no external URL, no data-availability
  statement, no code repository and no model-weights link anywhere in this PDF; the appendix (§A
  Benchmark Details, §B Wet-Lab Experimental Details, p14–17) is the whole of the supporting material
  and it **is** held. However:
  - **Per-target design hit rates exist only as badges inside Figure 1 (p1) and as bar labels in
    Figure 4A (p4).** There is no table of per-target hit rates, design counts, or K_D values. The
    numbers in `metrics_reported` above were read off the rendered figures.
  - **DockQ > 0.49 and DockQ > 0.8 success rates exist only as stacked-bar segments in Figure 2
    (p3).** The paper asserts the high-quality gains are "comparably large" (p3) and never gives a
    number for either threshold, in text or table.
  - **Per-target DockQ values are never reported for any benchmark.**
  - **Figure 3's seed-scaling curves are given as curves only**; no table of success rate vs seed
    count exists.
  Record as: SI held in full; **per-target and per-threshold numbers NOT TABULATED anywhere**.

## F. Figures

14 panel-group rows across 10 figures. Tables 1–5 are tables, not figures, and are excluded.
Pages 1, 4, 6, 8 and 15 were rendered to establish panel structure the captions did not carry;
Figures 2, 3 and 9 were resolved from text/caption alone.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 1 | Graphical-abstract grid of antibody–antigen complex renders, one per design campaign, each carrying a coloured badge with the BLI hit rate for Protenix-v2 and, where published, for Chai-2 and BoltzGen | structure render (with numeric badges) | `RENDER \| facet: campaign (15: 10 soluble incl. AMBP twice + 4 GPCR VHH-Fc + 3 GPCR mAb) × target class (4 boxes: antibody-filtered novel, dimeric, low-homology, GPCR) × method badge (3: Protenix-v2, Chai-2, BoltzGen) \| views: 1 \| overlay: 1 designed binder on 1 antigen model per render \| axis: none` | 4 grouped boxes containing 15 renders; panels vary by target and by target class, plus a method dimension carried as badge colour/outline rather than as a panel | **Yes.** The only quantities shown are percentages with **no denominators** — hit rates of 2%–88% are badged with no n, and the denominators live in a different figure on a different page (Fig 4A, p4), and not at all for Chai-2/BoltzGen. Comparator badges appear only for 5 of 15 campaigns, with no marker for "not reported" vs "not tested". The renders are decorative — no structural claim is measured from them | CC-BY-**ND** 4.0 (p1 banner). **ND: no derivatives — redrawing or modifying is forbidden, not just copying.** Verbatim reproduction with attribution only |
| 2 | 3 | Antibody–antigen interface success rate at 5 seeds for 5 models across 3 benchmark collections, stacked by DockQ quality tier | bar (stacked) | `PLOT \| facet: benchmark collection (3: PXMeter-AB 516/376, FoldBench-AB 104/160, AF3-AB 67/60) \| vary: model (5: AF3, Boltz-1, OF3p2, PX-v1, PX-v2) \| series: DockQ quality tier (3, stacked: >0.8, 0.49–0.8, 0.23–0.49) \| measure: success rate (%) \| n: 516 / 104 / 67 entries per panel; each bar aggregates all entries in its panel` | 3 panels, varying by benchmark collection; AF3 is absent (labelled N/A) in the PXMeter-AB panel | **Yes.** Each bar pools every entry in the collection into one rate with **no dispersion shown at all** — no error bars, no per-cluster spread, no confidence interval, despite Figure 3 on the same page showing that bootstrap SD is available. Only the total (DockQ > 0.23) is labelled numerically; the >0.49 and >0.8 segment values, which the text calls "comparably large", are never given as numbers anywhere | CC-BY-ND 4.0, p3 (banner on every page). **ND clause applies** |
| 3 | 3 | Inference-time scaling: DockQ > 0.23 success rate as a function of seed count, 1→1000, per model per benchmark | line | `PLOT \| facet: benchmark collection (3) \| vary: number of seeds, 1–1000, log scale (continuous, ticked at 1,2,5,10,20,50,100,200,500,1000) \| series: model (5: AF3, Boltz-1, OF3p2, PX-v1, PX-v2) \| measure: DockQ > 0.23 success rate (%) \| n: 516 / 104 / 67 entries per panel per point; number of independent bootstrap resamples NOT REPORTED` | 3 panels varying by benchmark collection; AF3 degenerates to a single marker in the FoldBench-AB panel ("AlphaFold3 is available only at 5 seeds and is therefore shown as a single marker", caption) | **Yes.** All three y-axes are truncated and each is truncated **differently** (≈20–60, ≈30–70+, ≈10–70), so the three panels cannot be compared by eye and none starts at zero; the apparent separation between curves is set by the axis choice. Shaded bands are labelled "bootstrap standard deviation" with no resample count given | CC-BY-ND 4.0, p3. **ND clause applies** |
| 4A | 4 | Per-campaign counts of designs made, designs sent to BLI, confirmed hits, and structural clusters | bar (grouped) | `PLOT \| facet: none (1) \| vary: design campaign (15, incl. AMBP epitope 1 and epitope 2 separately) \| series: quantity (4: # of Designs, # Sent to BLI, # Hits, # Clusters) \| measure: count \| n: 1 per bar (each bar is a single count, value printed above it); 15 campaigns per panel` | 1 panel, 15 campaign groups × 4 bars | **Yes (mild).** The quantity the paper argues about — the **hit rate** — is never plotted; the reader must divide the green bar by the blue bar for each of 15 campaigns. Counts are integers with no uncertainty and none is expected, but the derived rate has binomial uncertainty that is nowhere shown, and several campaigns rest on very small denominators (TACT 1/28, AMBP-ep1 2/47, NTM1A 2/38) | CC-BY-ND 4.0, p4. **ND clause applies** |
| 4B | 4 | Representative designed VHH poses from distinct structural clusters, three antigens | structure render | `RENDER \| facet: antigen (3: IDI2, IL-20, GPRC5D) × structural cluster (3 representatives per antigen) \| views: 1 \| overlay: 1 designed binder on 1 antigen surface per render \| axis: none` | 9 renders in a 3 × 3 grid; rows vary by antigen, columns by cluster representative | **Yes.** Three representatives are shown out of a per-campaign cluster count of up to 11 (Fig 4A), and the caption says only "representative" — no selection rule is stated, and the diversity claim ("not confined to a single repeated pose family", p6) has no quantitative panel of its own anywhere in the paper | CC-BY-ND 4.0, p4. **ND clause applies** |
| 4C | 4 | BLI association/dissociation sensorgrams with fitted curves, one antigen per panel | line | `PLOT \| facet: antigen (3: IDI2, IL-20, GPRC5D) \| vary: time, 0–360 s (IDI2, IL-20) / 0–250 s (GPRC5D) (continuous) \| series: analyte concentration (5–6 per panel: 250→15.6 nM; 62.5→2.0 nM; 6.250→0.391 nM) \| measure: response (nm) \| n: 1 sensorgram trace per concentration; 1 binder shown per antigen out of 9–16 confirmed hits (selection rule NOT REPORTED)` | 3 stacked panels varying by antigen; within each, concentration series plus black fitted curves | **Yes.** One exemplar binder per antigen out of 9–16 hits, with no statement of how the exemplar was chosen; y-axis maxima differ by an order of magnitude across panels (0.4 / 0.5 / 0.14 nm); the GPRC5D K_D is starred as an avidity measurement, correctly, but is the number quoted as "112 pM" in the main text | CC-BY-ND 4.0, p4. **ND clause applies** |
| 5 | 6 | Per-candidate developability readouts as jittered point clouds against a pass/fail threshold line, designs vs clinical-stage references | scatter (strip/jitter) | `PLOT \| facet: assay (3: thermostability Tm DSF °C, self-interaction red shift Δλ nm, polyreactivity BVP score) \| vary: jitter position (arbitrary, no variable) \| series: molecule class (2: Our Designs, Reference) \| measure: assay value (°C / nm / BVP score) \| n: 1 per point; per-panel n NOT REPORTED numerically, ≈40–150 points readable per panel` | 3 panels varying by assay; each panel has a red dashed threshold line and a green shaded pass region; a letter is shared with the marginal-histogram row below | **Yes.** The per-panel **n is never printed** — only a pass rate (100.0%, 97.5%, 93.3%), so 97.5% could be 39/40 or 390/400 and the reader cannot tell. The thermostability panel's y-axis is truncated at 60 °C, which is exactly the pass threshold, so **every failing candidate is invisible by construction** — the 100.0% pass rate is unfalsifiable from the panel. The reference antibodies are plotted but their pass rate is not stated | CC-BY-ND 4.0, p6. **ND clause applies** |
| 5-marg | 6 | Marginal count histograms attached to the right edge of each Figure 5 panel | bar (histogram, horizontal) | `PLOT \| facet: assay (3, the same three panels) \| vary: assay value bin (continuous, same axis as the point cloud) \| series: none (1) \| measure: count \| n: same underlying candidates as the row above, count axis 0–25 / 0–25 / 0–50` | Same three panel letters as the row above — a letter appears in two rows here because each Figure 5 panel contains both a point cloud and a marginal histogram with different marks and different measures | **Yes.** The histogram count axes differ across panels (0–25, 0–25, 0–50) with no shared scale, and the histograms are not separated by molecule class, so the designs and the reference antibodies are pooled into one distribution | CC-BY-ND 4.0, p6. **ND clause applies** |
| 6A | 6 | Binding response at 1000 nM for confirmed VEGF-A binders, split by who selected them | scatter (strip) | `PLOT \| facet: none (1) \| vary: selector (3: Human, Ranker A, Ranker B) \| series: structural cluster ID (11 levels, colour) \| measure: response at 1000 nM (nm) \| n: 7 / 9 / 10 points per selector column (from p6 text); 26 points per panel` | 1 panel, 3 selector columns | **Yes.** n = 7, 9 and 10 — the entire "rankers beat human intuition" claim rests on 26 points from a **single target**, and no test, interval or effect size is reported. The 30-selections-each denominator is stated in text but not on the figure. There is no statement that the human expert was blinded to the model scores | CC-BY-ND 4.0, p6. **ND clause applies** |
| 6B | 6 | Structural-cluster composition of the binders each selector recovered | bar (stacked) | `PLOT \| facet: none (1) \| vary: selector (3: Human, Ranker A, Ranker B) \| series: cluster ID (11, stacked) \| measure: count of selections \| n: 7 / 9 / 10 per bar` | 1 panel, 3 stacked bars, shared 11-level cluster legend with 6A | **Yes.** Stacked counts of 7–10 across 11 cluster levels means most segments are a single molecule; the "human selections span a broader set of clusters" conclusion (p6) is a comparison of 7 items spread over 7 clusters against 10 items spread over 4, with no diversity statistic computed | CC-BY-ND 4.0, p6. **ND clause applies** |
| 7 | 8 | Per-subitem pass rate under the revised validity criterion, five model/reference conditions across ten PoseBusters-style checks | bar (grouped) | `PLOT \| facet: none (1) \| vary: validity subitem (10: tetrahedral chirality, non-aromatic ring non-flatness, double-bond flatness, sp2-center flatness, amide flatness, sp3-center non-flatness, internal steric clash, internal energy, min distance to inorganic cofactors, volume overlap with protein) \| series: condition (5: Ground truth, Boltz-2x, Boltz-1x, Protenix-v1-TFG, Protenix-v2-TFG) \| measure: success rate (%) \| n: 623 entries / 250 clusters behind each bar (PXM-22to25-Ligand)` | 1 panel, 10 subitem groups × 5 bars | **Yes, badly.** The y-axis is **truncated at ≈91.5%** with a top of 100.0, so a 92.5–100 window is stretched across the full panel height and every difference is visually inflated ≈12×. Worse, bars whose value falls below the axis floor **do not render at all**: the "Internal steric clash" group shows only a few short stubs, and the reader cannot distinguish "below 92.5%" from "missing". No n is printed on the figure and there are no error bars | CC-BY-ND 4.0, p8. **ND clause applies** |
| 8 | 8 | Three case studies of local ligand geometry, each comparing a TFG prediction, a failing baseline, and the deposited structure | structure render | `RENDER \| facet: case (3: PDB 7H60 twisted amide, 9MWU distorted aromatic ring, 9RDY incorrectly planar sp3 center) × condition (3 per row: Protenix-v2-TFG, the failing model, ground truth) \| views: 1 \| overlay: 1 predicted ligand pose in 1 pocket per render; no superposition of predictions on the reference \| axis: none` | 9 renders in a 3 × 3 grid; rows vary by case, columns by condition; two rows compare against Boltz-2x and one against Protenix-v2 | **Yes.** Three hand-picked cases out of 623 test entries, with no selection rule stated and, by the caption's own framing, chosen because "the TFG variants pass the check successfully while Protenix-v2 or other baseline model fail" — i.e. selected on the outcome being illustrated. Only the top row carries a quantitative annotation (dihedral ≈180° vs ≈150°); the other two rows are qualitative | CC-BY-ND 4.0, p8. **ND clause applies** |
| 9 | 9 | Interaction interfaces of the cross-variant mini-binder with Omicron and prototype RBD, key residues as sticks with polar contacts | structure render | `RENDER \| facet: RBD variant (2: Omicron left, prototype right) \| views: 1 \| overlay: 1 predicted binder complex per panel; no experimental reference structure is overlaid or exists \| axis: none` | 2 panels varying by variant | **Yes.** These are **predicted** complexes with no experimental structure of either complex, and every mechanistic statement drawn from them is hedged in the text ("may form", "likely participate", "potential compensatory mechanisms", p9). There is no distance table, no measured contact geometry, and no quantitative panel supporting the compensatory-mechanism claim | CC-BY-ND 4.0, p9. **ND clause applies** |
| 10 | 15 | Per-interface DockQ under the public OF3p2 FoldBench setting vs the authors' MMseqs-MSA-no-template setting | scatter (paired, with y = x) | `PLOT \| facet: none (1) \| vary: DockQ (OF3 official reported), 0.0–1.0 (continuous) \| series: none (1) \| measure: DockQ (OF3 with Protenix-MSA), 0.0–1.0 \| n: 1 per point, 267 interfaces per panel` | 1 panel; y = x reference line plus DockQ = 0.23 threshold gridlines on both axes | Blank — this is a well-made figure: it shows every point, both thresholds, the identity line, the n, and both summary success rates in-panel | CC-BY-ND 4.0, p15. **ND clause applies** |

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Opus 5), schema v3 pass
- **schema_version**: `v3`
- **confidence**: **high** on identity, the training cutoff, claims, benchmark identities and the
  headline metric table; **high** on the negative findings about conformational states, which were
  established by exhaustive grep across the full text as well as by reading; **medium** on the figure
  rows for Figures 1, 4A, 5 and 6, where per-mark values and n counts were read off 150-dpi renders
  rather than from any table (values are legible but the point counts in Figure 5 are estimates, and
  are recorded as such); **medium** on `n_predictions` for the design arm for the same reason;
  **low-confidence-adjacent gaps** are all recorded as NOT REPORTED rather than guessed — in
  particular Protenix-v2's own MSA/template regime, the ranking-score and Ranker A/B definitions, the
  architectural delta, and the training-set composition, none of which this paper describes at all.
  What was hard: the paper carries no methods content worth the name, so several Section B and C
  fields are NOT REPORTED not through omission on my part but because a 17-page report devotes two
  sentences to what changed in the model.
- **unresolved**:
  1. **THREE distinct Protenix reports exist and this corpus holds only one of them. Citations must
     not be conflated.** (a) The corpus entry **`protenix2025`** is reference **[8]** here — "Protenix
     - advancing structure prediction through a comprehensive alphafold3 reproduction", bioRxiv 2025,
     doi 10.1101/2025.01.08.631967 (p11). (b) Reference **[33]** is a *different* report — "Protenix-v1:
     Toward high-accuracy open-source biomolecular structure prediction", bioRxiv, pages 2026–02, 2026
     (p12) — **and it is [33], not [8], that is the "Protenix-v1" baseline against which every 9-to-13
     point gain in this paper is measured.** (c) This paper is the third. Page 2 confirms the
     three-way structure: "Relative to earlier Protenix iterations **[8, 33]**, Protenix-v2
     incorporates architectural refinements and training optimizations while retaining the same
     input-output setting." **Consequence: a manuscript citing "Protenix" for the v1 baseline numbers
     must cite [33] (not in this corpus), while a manuscript citing the original AF3 reproduction must
     cite `protenix2025`. Citing `protenix2025` for anything labelled "Protenix-v1" in this paper is
     wrong.** Whoever holds `STATUS.md` should decide whether [33] needs its own corpus entry.
  2. **Whether the training cutoff changed between versions cannot be resolved from this PDF.** This
     paper states 2021-09-30 (p2) and says only that it "aligns with established conventions in recent
     models [8, 28, 34]". It gives no date for [8] or [33]. Anyone needing "did the cutoff move?" must
     read the earlier reports; do not infer it from the alignment sentence.
  3. **FoldBench-AB is printed as "(104/160)"** (Figure 2 panel title, p3) under a caption stating the
     pair is "(number of entries/number of clusters)". 160 clusters cannot come from 104 entries. The
     pair is probably transposed, but the paper never corrects it and I have recorded it as printed.
  4. **VEGF-A design count conflicts between figure and text.** Figure 4A (p4) shows "# of Designs =
     71" for VEGF-A, while p6 says the ranking study used "approximately 300 designed VHH candidates"
     for VEGF-A. Either the 71 is a post-filter count or the ~300 includes designs never counted in
     Figure 4A; the paper does not say.
  5. **GPCR mAb hit rates conflict between text and figure.** p5 states "the corresponding mAb
     campaigns reached 0%, 17%, 50%, and 44%", but Figure 1 (p1) badges only three mAb campaigns —
     GPRC5D 50%, CCR7 **43%**, CCR8 17% — with no CCR5 mAb badge at all. So one value differs by a
     point (44 vs 43) and the 0% campaign is absent from the figure.
  6. **Antigen naming conflict:** Figure 4A (p4) and Figure 1 (p1) label a target **CD226**, while
     Table 4 (p16) lists the purchased antigen as **CD266** (Sino cat. 10565-H08H). One of the two is
     a typo and the paper does not reconcile them.
  7. **Self-interaction pass rate is 97.5% in the Figure 5 caption (p6) and 98% in the text (p5)**;
     polyreactivity is 93.3% vs 93%. Rounding, almost certainly, but recorded because the figure
     caption is the more precise source.
  8. **`states_generated` judgement call, flagged deliberately.** I wrote `one` and withheld the
     `ensemble` tag even though the paper draws up to 1000 samples per target, because no basin, state
     or ensemble is ever defined, partitioned or measured — the seeds are an accuracy budget collapsed
     by a ranking score to a single reported structure. If the corpus convention is that any
     multi-sample protocol earns `ensemble`, this row should be re-tagged; as written, tagging it
     would false-positive every conformational-ensemble query.
  9. **Tag I needed and could not use: there is no tag for de-novo binder/antibody design**, which is
     roughly half of this paper (§4, §5.2, and all of the wet-lab appendix). The v3 Method vocabulary
     has `cofolding`, `md-emulator`, `experimental` and so on, but nothing for a generative design
     system. `experimental` is explicitly wrong (it "marks a paper with no structure prediction in it
     at all"). Candidate names for the schema owner: `binder-design` or `de-novo-design`. I did not
     invent one.
  10. **Second tag gap: no tag for inference-time constraint guidance on the diffusion sampler.** The
      TFG variants (p7) impose chirality/planarity/torsion/distance constraints during generation.
      `latent-steering` is defined in v3 as "any inference-time intervention on an internal tensor —
      pair representation, trunk embedding, distogram head, conditioning embedding". TFG intervenes on
      the sampled **coordinates** via projected-diffusion/SHAKE-style constraint enforcement, not on
      an internal representation, so I withheld the tag. If the schema owner intends `latent-steering`
      to cover all inference-time steering of the generative process regardless of where it acts, this
      note should gain the tag and the schema's wording should be widened.
  11. **Protenix-v2's own MSA and template configuration is never stated.** Only the OF3p2 baseline's
      is (p14). `templates` and `msa_handling` are therefore NOT REPORTED, and no protocol tag
      (`templates-on`, `no-template-no-msa`) could be applied to this paper.
  12. **The architectural delta is one sentence.** "Relative to earlier Protenix iterations [8, 33],
      Protenix-v2 incorporates architectural refinements and training optimizations while retaining
      the same input-output setting" (p2). No refinement is named, no optimization is described, no
      ablation separates architecture from data from training recipe. Nothing in this note attributes
      the 9–13 point gain to any specific change, because the paper does not.
  13. **The prototype SARS-CoV-2 RBD is almost certainly inside the training window and the paper does
      not discuss it.** With a 2021-09-30 cutoff (p2), prototype spike RBD structures deposited in
      2020 are training data, while Omicron B.1.1.529 (first reported November 2021) is post-cutoff.
      The paper reports dual binding to both (p9, Table 2) without addressing the asymmetry. Recorded
      as an observation about the paper's silence, not as a leakage finding — the designs were
      generated and tested prospectively.
  14. **The GPCR antigens carry no novelty filter.** The SAbDab and 30%-identity filters are stated
      only for the soluble panels (p5); CCR5/CCR7/CCR8/GPRC5D are introduced on difficulty grounds
      alone. Their relationship to the training set is unstated.
  15. **No release statement of any kind.** No weights, no code repository, no inference URL, no
      licence for the model, no data availability. The only released artefact identifiable from the
      PDF is the evaluation harness **PXMeter v1.1.0**, named on p7 ("in the new version of PXMeter
      (v1.1.0), we extend the standard PoseBusters validity criterion…") and p14 ("the gen-input module
      in PXMeter v1.1.0"), and even that carries no URL here — only the citation to Ma et al. [16].
      Note the contrast: the word "open-source" appears twice in this paper, once describing the OF3p2
      **comparator** (p3) and once inside the **title of reference [33]** (p12); it is never used of
      Protenix-v2 itself.
  16. **Figure 3 seed-scaling values are not tabulated**, so the "5 seeds beats 1000 seeds" claim
      (p2, p4) can be checked only by reading curve positions off the plot.
- **why_it_matters**:

---

## Tags

`general-protein` `gpcr` `cofolding` `single-state` `binary-predicate` `saturating-metric`
`design-level-oracle` `prospective` `anti-memorization` `unpowered` `confidence-as-discriminator`
`multi-backbone` `experimental-validation` `preprint` `background` `contrast` `comparator-numbers`

**Tag notes (why each borderline tag was applied or withheld):**
- `gpcr` — applied: four GPCRs (CCR5, CCR7, CCR8, GPRC5D) are actual study targets (p5, p16). But
  they are targets for **antibody design**, not for conformational modelling; a query for GPCR
  conformational states will get a true-but-irrelevant hit here.
- `single-state` — applied; `ensemble` deliberately **withheld**. See `unresolved` item 8.
- `saturating-metric` — applied on the numeric ceilings in `metric_saturation` (100.0%
  thermostability, 100% target-level success, ~100% ground-truth validity subitems).
- `design-level-oracle` — applied (route 7: availability-sampled panel, and epitope-selection rule
  fixed after an experimental result on that panel). `oracle-leak` **withheld**: no pipeline leakage
  route was found.
- `prospective` — applied on the strength of the wet-lab design arm; the structure-prediction arm is
  retrospective by construction. See `prospective`.
- `anti-memorization` — applied (2021-09-30 cutoff, post-cutoff ligand set actually run,
  novelty-filtered and low-homology design panels actually run). `no-anti-memorization` would be
  wrong. But note the antibody-antigen structure benchmarks have **no** memorization control.
- `unpowered` — applied to the design panel: 13 antigens, GPCR arm n = 4, ranking study n = 26 points
  on 1 target.
- `confidence-as-discriminator` — applied, **scoped**: a ranking score selects the reported top-1
  structure and two undocumented "rankers" prioritize binders. It is **never** used to judge
  conformational correctness.
- `experimental-validation` — applied: BLI kinetics, DSF, AC-SINS, BVP ELISA, all in-house (p15–17).
  `experimental` **withheld** — that tag is for papers with no structure prediction at all.
- `comparator-numbers` — applied: Section E carries usable head-to-head numbers against AF3, Boltz-1,
  Boltz-1x, Boltz-2, Boltz-2x, OF3p2 and Protenix-v1 on named benchmarks.
- `figure-exemplar` — **withheld**. Thirteen of the fourteen panel-group rows have entries in `hides`, and
  the CC-BY-**ND** licence forbids redrawing anyway. Figure 10 (p15) alone is well made.
- Withheld with reason: `msa-subsample`, `msa-state-filter`, `template-state-bias`, `af-cluster`,
  `latent-steering`, `md`, `md-emulator`, `enhanced-sampling`, `benchmark-only` (method not used);
  `templates-on`, `no-template-no-msa`, `state-annotated-input` (Protenix-v2's input regime is never
  stated); `two-state`, `ensemble`, `continuum` (no states); `continuous-metric`, `rmsd-only`,
  `visual-metric` (interface quality is called by binary DockQ thresholds); `oracle-leak`;
  `no-anti-memorization`; every Control tag including `directed-state`, `partner-driven`,
  `ligand-driven`, `peptide-driven`, `g-protein-mimetic`, `nanobody`, `apo-sampling`, `seed-only`
  (all describe steering a **target's conformational state**, which this paper never does — the VHH
  and mAb formats here are the designed molecules, not state-steering handles, and the seed sweep is
  an accuracy budget); every Site tag `orthosteric`, `allosteric-site`, `cryptic-pocket`,
  `allosteric-failure` (no binding-site conformational analysis); `peer-reviewed`; `threat`;
  `negative-result`; `fold-switching`, `kinase`, `transporter`, `periplasmic-binding`, `atpase`.

**KEY FINDING FOR THE CORPUS, restated so it cannot be missed:** the training cutoff is
**2021-09-30**, stated once on **page 2** — "Protenix-v2 is trained without wwPDB [3] entries released
on or after 2021-09-30" — and **this paper never states any earlier version's cutoff**, so it cannot
be used to establish whether the date changed between Protenix versions.
