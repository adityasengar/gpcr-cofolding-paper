# junker2026peptidedesign

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–21), and the PDF page
equals the printed page throughout** (PDF p9 prints "9 / 21"). Layout: p1 abstract +
front matter, p2–p3 Introduction, p3–p14 Results, p14–p16 Discussion, p16–p18 Methods,
p18 Supporting-information list, p18–p19 acknowledgements / author contributions,
p19–p21 references. Figures are inline with the text: Fig 1 p4, Fig 2 p5, Fig 3 p6,
Fig 4 p7, Fig 5 p8, Fig 6 p9, Fig 7 p10, Fig 8 p12, Fig 9 p13.

**THIS PAPER HAS TWO ARMS WITH DIFFERENT n AND DIFFERENT CONCLUSIONS.** They are kept
separate everywhere in this note and must not be blended:

- **Arm 1 — VALIDATION arm** (p3–p11, Figs 2–7). Reproducing 113 *deposited*
  GPCR–peptide/protein complexes with three structure predictors, 50 seeds each.
  n = 113 dimers × 50 seeds × 3 predictors = **16,950 predictions**. Conclusion:
  accuracy is mediocre and strongly seed- and training-cutoff-dependent, and
  **PAE-derived confidence over-estimates for misplaced peptides in all three
  predictors**.
- **Arm 2 — DESIGN arm** (p11–p14, Figs 8–9). Benchmarking three generative binder
  methods on **3** receptors, 10,000 designs each. n = 3 methods × 3 receptors ×
  10,000 = **90,000 designs**, of which 90 backbones were re-predicted. Conclusion:
  backbone sampling is adequate, simultaneous sequence generation is subpar and
  partially recoverable with ProteinMPNN, and BoltzGen shows apparent memorization.

**The main deliverable for us is the confidence over-estimation finding.** It is
recorded verbatim with pages in `confidence_as_discriminator` (section C) and its
numbers in `metrics_reported` (section E, Arm 1 block).

**RECEPTOR CONFORMATIONAL STATE WAS NEVER SCORED.** See `state_metric` and
`unresolved` item 1. The receptor is supplied as a fixed template/reference in every
prediction and is never re-predicted or evaluated; every metric in the paper scores
the *peptide* relative to that fixed receptor.

**License:** CC-BY 4.0, **no ND clause** — panels may be redrawn with attribution.
See `reuse` in section F.

**SI is not held.** All two supplementary tables and ten supplementary figures are
cited and none is in the 21-page PDF. See `si_in_scope`.

---

## A. Identity

- **citekey**: `junker2026peptidedesign`
- **doi**: **10.1371/journal.pone.0355549** (p1 citation block: "Junker H, Schoeder CT
  (2026) Assessment of generative de novo peptide design methods for G protein-coupled
  receptors. PLoS One 21(8): e0355549. https://doi.org/10.1371/journal.pone.0355549").
  Underlying data: Zenodo **10.5281/zenodo.18755322** (p2, Data availability statement).
- **year**: **2026.** Received March 17, 2026; Accepted July 23, 2026; Published
  August 27, 2026 (p1).
- **venue**: **PLOS One 21(8): e0355549. PEER-REVIEWED, not a preprint.** p1: "Peer
  Review History: PLOS recognizes the benefits of transparency in the peer review
  process; therefore, we enable the publication of all of the content of peer review
  and author responses alongside final, published articles." Editor: Shengwei Sun, KTH
  Royal Institute of Technology, Sweden (p1). Tagged `peer-reviewed`.
- **title**: "Assessment of generative de novo peptide design methods for G
  protein-coupled receptors" (p1).
- **authors**: Hannes Junker¹, Clara T. Schoeder\*¹˒² (p1). 1 = Institute for Drug
  Discovery, Leipzig University Medical Faculty, Leipzig, Germany; 2 = Center for
  Scalable Data Analytics and Artificial Intelligence ScaDS.AI, Dresden/Leipzig.
  Corresponding author clara.schoeder@medizin.uni-leipzig.de. Two authors only — not
  "et al." Funding: DFG CRC1423 "Structural Dynamics of GPCR Activation and Signaling"
  (project 421152132, project A02) (p2). Competing interests: none declared (p2).

## B. Scope

- **system**: **GPCR.** Exclusively GPCRs and their peptide/protein ligands. Both
  class A and class B1 (p3). Ligand types are heterogeneous by design: endogenous
  peptides, larger protein ligands (chemokines/chemotactic cytokines), and **four
  nanobodies**. p3: "The dataset further contains four nanobodies (nAbs), whose overall
  topology differ drastically from those of peptides, however, their CDR loops interact
  with the receptors in similar fashion as, for instance, cyclic peptides. From here on
  both peptide and protein ligands were collectively referred to as peptides."

- **n_targets**: **DUAL — the two arms have different n.**
  - **Arm 1 (validation): 113 unique GPCR–peptide dimers** (p3, p4). Abstract (p1)
    gives the split: "91 unique known GPCR-peptide and 22 unique GPCR-protein
    complexes including four nanobodies (nAbs)". Composition (p3): "74 peptides
    binding to 58 class A receptors and 26 peptides binding to 14 class B1 receptors"
    → **72 unique receptors, 100 ligand entries, 113 dimers**. Filtered down from 414
    GPCRdb protein/peptide entries (p3, Fig 2A p5). Peptide lengths 3–137 aa (Fig 2B
    p5); majority 5–21 aa; 27–61 aa mostly class B1 hormones; 62–73 aa mostly
    chemokines; >74 aa nanobodies/single-domain antibodies (p3, Fig 2 caption p5).
  - **Arm 2 (design): 3 receptors.** p11: AT2 receptor with Ang II (PDB 6jod, peptide
    length 8), ETB with sarafotoxin S6b (PDB 6lry, length 22), NOP receptor with
    nociceptin (PDB 8f7x, length 14).
  - **Generality flag**: the design-arm conclusions ("all generative methods sample
    backbone space sufficiently", p1 abstract) rest on **three** targets. The authors
    themselves hedge this — see `stated_limits`, p15: "the number of generations
    necessary remains elusive and highly target dependent" and "While our results do
    not show memorization for BindCraft and RFdiffusion3, it cannot be ruled out that
    these methods can show similar behavior for other targets."

- **method_class**: **benchmark-only.** No new method, model, weight or loss is
  introduced. p3: "We sought to address these questions in a GPCR-specific two-part
  benchmark that reflects typical de novo design pipeline setups (Fig 1)." The only
  authored code is analysis scripting (p17–p18). The *objects* benchmarked are
  co-folding predictors (Arm 1) and generative binder-design models (Arm 2).

- **backbones**: **Three structure predictors compared head to head → `multi-backbone`.**
  With versions where given:
  | tool | role | version / weights | page |
  |---|---|---|---|
  | **AlphaFold2 Initial Guess (AF2IG)** | predictor | `dl_binder_design` repo; **weights `model_2_ptm.npz`**, selected after testing model_1_ptm–model_5_ptm; seeds 1–50; script modified to dump the full PAE matrix and accept custom seeds | p16 |
  | **Boltz-2** | predictor | `jwohlwend/boltz`, default settings **plus `--use_potentials`**; **weights downloaded 06/20/25**; seeds 1–50; msa: empty | p16–p17 |
  | **RosettaFold3 (RF3)** | predictor | RosettaCommons `foundry` rf3; **installed 08/15/25, weights `rf3_latest.pt` obtained 08/15/25**; `early_stopping_plddt_threshold` set to 0.1; seeds 1–50 | p17 |
  | **BindCraft** | generative design | `martinpacesa/BindCraft`; `peptide_filters.json`; `peptide_3stage_multimer.json` advanced settings with `predict_initial_guess=false`, `enable_mpnn=false`; `Average_Binder_RMSD` and all stage-specific `Binder_RMSD` filters set to **null**; `Average_pLDDT`, `1_pLDDT`, `2_pLDDT` set to **0.5** | p16 |
  | **BoltzGen** | generative design | `HannesStark/boltzgen`; **peptide-anything protocol, design step only**; **weights cached 12/04/25** | p17 |
  | **RFdiffusion3** | generative design | RosettaCommons `foundry` rfd3; `infer_ori_strategy: hotspots` with TIP atoms; **`is_non_loopy = True`**; **weights `rfd3_latest.ckpt` obtained 12/03/25** | p17 |
  | **ProteinMPNN** | sequence redesign | installed from `dauparas/LigandMPNN`; `--model_type "protein_mpnn"`, **weights `protein_mpnn_v48_030.pt`**, `--temperature 0.05`; one sequence per backbone; peptide chain designable, receptor chain fixed | p17 |
  | **DockQ** | metric | `wallnerlab/DockQ`, **dockq = 2.1.3** | p16, p18 |
  Analysis stack (p17–p18): python 3.12, biopython 1.83, numpy 1.26.4, gemmi 0.7.2,
  scipy 1.13.1 (`mannwhitneyu`, `spearmanr`), pandas 2.2.2, matplotlib 3.8.4,
  seaborn 0.13.2. Rosetta `PerResidueClashMetric` for clash counting (p12).
  **AlphaFold3 and Chai-1 are cited (p2) but NOT benchmarked.**

- **templates**: **ON, and this is the load-bearing protocol choice.** p3: "We chose
  these three prediction methods as they support templating, where a structure template
  guides the prediction of a target receptor while the respective network is tasked
  with the placement of the peptide." p4: "the crystal structure of each of the 113
  receptors was provided as a template to Boltz-2 and RF3. In case of AF2IG, the dimer
  of the receptor and its peptide was the input, where the coordinates of the receptor
  are used to initialize the prediction." p16 (Boltz-2): "For the receptor chain the
  respective reference structure was provided ('apo', i.e., peptide chain removed)."
  p17 (RF3): "Analogous to Boltz-2, the apo version of the reference dimer was provided
  as a prediction component." Templates are **NOT state-annotated** — they are the
  deposited structure of the very complex being reproduced, with the peptide stripped.
  There is no state label, no active/inactive selection, and no alternative-state
  template arm anywhere.

- **msa_handling**: **NONE — MSAs off for every chain, deliberately.** p4: "For the
  prediction of the peptides multiple sequence alignments (MSAs) were not provided for
  either of the prediction methods with the rationale to mimic de novo peptide
  prediction." p16 (Boltz-2 Methods): "No MSAs were allowed for either of the chains
  (i.e., msa: empty)." This is **not** subsampling and **not** state-filtering — it is
  full ablation. Note the asymmetry the paper itself flags at p14 under
  `stated_limits`: "In this context it is worth noting that no MSAs have been used in
  our setup. This is a typical trade-off between runtime and accuracy and the number of
  false positive peptide predictions might decrease if MSAs were included."
  **Combination is unusual for this corpus: templates ON + MSA fully OFF.** Note that
  Boltz-2 additionally receives the full-length UniProt receptor *sequence* (not just
  the template residues) — p16–p17: "Contrary to AF2IG and RF3, where the receptor
  chain residues were taken from the template, including gaps in the crystal structure,
  Boltz-2 requires a sequence. We opted to provide the full-length sequence taken from
  uniprot.org."

## C. Conformational core

- **states_generated**: **`one + ensemble`** — dual, and the split matters.
  - **one (receptor):** the receptor conformation is *imposed* by the template/initial
    guess and is identical across all 50 seeds and all predictions. The paper never
    generates, samples or compares a second receptor state. There is no active/inactive
    arm, no apo-receptor arm, no G-protein-coupled arm.
  - **ensemble (peptide placement):** 50 seeds per dimer produce a genuine spread of
    peptide poses, and that spread is a headline finding. p6: "Inspecting the 50
    predictions per receptor-peptide dimer revealed that using different seeds seemed
    to result in vastly different prediction qualities (Fig 4)... e.g., PDB IDs 8flu or
    6b3j where, depending on the seed, the prediction of the peptide ligand can either
    be 'incorrect', with a DockQ score as low as 0.03 or 'high quality' with a DockQ
    score as high as 0.85."
  - In Arm 2, 10,000 designs per method/target are an ensemble of *ligands*, not of
    receptor states — the receptor is fixed input throughout (p11).
  - **NOT tagged `ensemble`** in the Tags section: the ensemble here is over ligand
    poses on a frozen receptor, and tagging it would false-positive every reverse
    lookup for conformational-ensemble methods. Tagged `single-state` only.

- **structural_priors_used**: **Extensive, declared, and not in itself a defect.**
  Enumerated:
  1. **Deposited receptor structures as templates / initial guess** for every one of
     the 16,950 predictions in Arm 1 and every design in Arm 2 (p4, p16, p17). This
     is the protocol, not a leak of the answer being scored — the answer being scored
     is the *peptide*.
  2. **GPCRdb as the dataset source.** p16: "We filtered the GPCRdb with ligand type
     'peptide' or 'protein' and downloaded the respective entries from RCSB.org."
     Used as a ligand-type filter only; **no state annotation is drawn from GPCRdb.**
  3. **The deposited peptide's length constrains generation** in Arm 2. p11: "In order
     to mimic the native peptide the de novo generation was restricted to exactly the
     length of the respective reference peptide."
  4. **Hotspot residues read off the reference complex.** p11: "For each reference
     complex, four to six residues closest to the pocket-intruding peptide terminus
     were selected as hotspot residues to guide generation into the orthosteric binding
     pocket (S2 Table and S6 Fig.)."
  5. **OPM database** deposits used to define the membrane plane for the
     inside-vs-outside-pocket analysis. p11: "by superimposing the designs onto the
     respective deposit in the Orientations of Proteins in Membranes (OPM) database
     (S7A Fig.)".
  6. **UniProt full-length receptor sequences** for Boltz-2 (p17).
  7. The three Arm-2 targets were **selected from the Arm-1 deposited set** (p11).

- **oracle_leakage**: **Seven routes, answered separately.** Summary: **route 1
  present by design and declared; route 4 present and undeclared as such; route 5
  present as the benchmark definition; route 7 present and strong in the design arm;
  routes 2, 3, 6 NONE FOUND.**

  **Route 1 — deposited structures as input or template: PRESENT, by declared design.**
  Verbatim, p4: "To this end, the crystal structure of each of the 113 receptors was
  provided as a template to Boltz-2 and RF3. In case of AF2IG, the dimer of the
  receptor and its peptide was the input, where the coordinates of the receptor are
  used to initialize the prediction."
  Verbatim, p16: "For the receptor chain the respective reference structure was
  provided ('apo', i.e., peptide chain removed)."
  Assessment: the *receptor* is the oracle; the *peptide placement* is the prediction.
  This is a legitimate benchmark protocol for the question asked (can the network place
  the peptide?), and it is stated openly. It does mean **the paper measures nothing
  about receptor structure or receptor state** — every reported number is conditional
  on the correct receptor conformation being handed in. Note AF2IG receives the full
  *dimer* including the reference peptide chain; the paper states only the receptor
  coordinates initialise the prediction (p4), but the peptide chain's presence in the
  input file is not further characterised. See `unresolved` item 9.

  **Route 2 — state annotations from a curated database (GPCRdb, KLIFS, Kincore)
  driving templates or alignments: NONE FOUND.** GPCRdb is used, but only as a
  ligand-type filter for dataset assembly. Verbatim, p16 (the whole of the Data
  collection and curation Methods section, which is where the protocol is described):
  "We filtered the GPCRdb with ligand type 'peptide' or 'protein' and downloaded the
  respective entries from RCSB.org [61]." No state annotation, no active/inactive
  label, no conformational classification is taken from GPCRdb or from anywhere else,
  at any point in either arm.

  **Route 3 — cluster labels derived from known states: NONE FOUND.** No clustering of
  any kind is performed. The protocol is described in full at p16–p18 (Methods) and
  contains no clustering step; the only grouping applied to predictions is the
  pre-/post-training-cutoff split (route-independent, and a *control*, see
  `anti_memorization_control`) and the DockQ quality categories (route 5).

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against
  known states / the evaluation set: PRESENT, and undeclared as leakage.** Verbatim,
  p16: "Seeds 1–50 were used for the predictions with model_2_ptm.npz weights (weights
  model_1_ptm to model_5_ptm were tested initially with **model_2_ptm showing highest
  recovery**; S9 Fig.)." That is a model-selection decision made **on the benchmark set
  itself**, which under v3 is leakage even though no per-target value is chosen — the
  *choice among five weight sets* was made by recovery on the 113 dimers.
  A second, weaker instance, p16: "Boltz-2 was installed and applied as described in
  https://github.com/jwohlwend/boltz with default settings apart from the addition of
  the `--use_potentials` flag. Initial tests considered both options for this flag but
  no significant difference could be observed (S10 Fig.)." Here the sweep found no
  difference, so the leak is inert, but the range was still evaluated on the benchmark
  set. A third, p17: "To prevent RF3 from aborting low-confident runs
  `early_stopping_plddt_threshold` was set to 0.1" — a stopping criterion relaxed so
  that *failures are retained*, which biases against RF3's headline numbers rather than
  for them; recorded for completeness. Fourth, p16 (BindCraft): `Average_Binder_RMSD`
  and all stage-specific `Binder_RMSD` filters set to null and pLDDT filters to 0.5,
  explicitly "In order to ensure comparability with respect to the actual space
  sampled" — a deliberate *loosening*, again biasing against BindCraft's apparent
  quality rather than for it.
  **S9 Fig and S10 Fig, which would let the size of the route-4 effect be checked, are
  not held.** See `si_in_scope`.

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had:
  PRESENT, as the benchmark's definition of accuracy.** Verbatim, p4–p5: "To measure
  the structural deviation of predictions to crystal structure reference, the predicted
  dimer was aligned with the crystal structure by superimposing the receptors. Next,
  the DockQ score [39] was calculated for the predicted peptide to the reference
  peptide." And p5: "Analogous to the categorization of the DockQ authors, we will
  refer to predictions as 'incorrect' (DockQ < 0.23), 'acceptable quality'
  (0.23 ≤ DockQ < 0.49), 'medium quality' (0.49 ≤ DockQ < 0.8) and 'high quality'
  (DockQ ≥ 0.80)." Assessment: unavoidable and standard for a reproduction benchmark;
  the thresholds are **borrowed, not tuned** ("Analogous to the categorization of the
  DockQ authors"), which is the clean version of this route. **Note the important
  contrast in Arm 2**, p13: "The respective initially designed peptide served as
  reference for DockQ in both cases" (Fig 9 caption) — in the design arm DockQ is a
  *self-consistency* measure against the design, not against any experimental
  structure, so route 5 does not apply there.

  **Route 6 — best/worst model labels assigned against a held reference: NONE FOUND,
  and the paper does the clean thing explicitly.** The "best seed" analysis, which is
  where this route would enter, selects by **confidence, not by DockQ**. Verbatim,
  Fig 6 caption, p9: "**Outlined dots represent the best seed according to the
  respective confidence metric.**" And p9: "However, selecting only the best seed for
  each respective confidence metric demonstrated an improving effect on the correlation
  between peptide plDDT and DockQ score for Boltz-2 and RF3 (ρ = 0.81 for both)."
  Selecting by confidence and *then* measuring the correlation with DockQ is the
  honest construction and is what makes the best-seed result usable. Worth citing as a
  positive example.

  **Route 7 — design-level oracle use (input conditions or systems chosen because the
  expected answer is already known): PRESENT AND STRONG IN ARM 2. Design-level, NOT
  pipeline leakage — keep distinct.** Three separate instances:
  (a) The generated peptide's length is pinned to the native peptide's length.
  Verbatim, p11: "In order to mimic the native peptide the de novo generation was
  restricted to exactly the length of the respective reference peptide."
  (b) The hotspots are read off the native complex. Verbatim, p11: "For each reference
  complex, four to six residues closest to the pocket-intruding peptide terminus were
  selected as hotspot residues to guide generation into the orthosteric binding pocket."
  (c) Success is measured as similarity to the native peptide. Verbatim, p3: "for three
  representative peptide-receptor complexes, we generated 10000 putative peptides with
  BindCraft, BoltzGen and RFdiffusion3 each **with the goal of mimicking the native
  peptide**. Through structural deviation to the reference peptide we examine the
  explorational power of each generative design model."
  Also in Arm 1, the ETB case study (p10–p11) is a design-level oracle: the three
  peptides shown were chosen **because** they are known to be in training. Verbatim,
  p10: "Lastly, it is worth noting that structures of all three peptide-receptor
  complexes were included in training of AF2, Boltz-2 and RF3, respectively."
  Assessment: (a)–(c) are a deliberate methodological choice for measuring *sampling
  breadth against a known answer*, and the paper is explicit about it. But it means the
  design arm cannot say anything about *prospective* de novo design — a designed
  peptide is called good when it looks like the endogenous one, which is precisely the
  memorization behaviour the paper flags as a problem elsewhere (p15).

- **prospective**: **no — fully retrospective in both arms.** Every one of the 113
  Arm-1 complexes is a deposited structure used as its own reference (p3, p4). Every
  Arm-2 design is scored against a deposited native peptide (p11) or against itself
  (p13). No experiment of any kind was performed; nothing was tested that was not
  already known. The nearest thing to prospectivity is the post-training-cutoff subset
  (route-independent; see `anti_memorization_control`), which is *retrospective but
  out-of-training* — the correct term, and a genuine strength — not prospective.

- **state_metric**: **`RMSD-to-reference` (DockQ family, PEPTIDE PLACEMENT ONLY)
  + `binary predicate` (borrowed DockQ category thresholds).
  RECEPTOR CONFORMATIONAL STATE WAS NEVER ASSESSED AT ALL.**

  **On receptor state — the explicit answer to the question asked of this note:** the
  receptor conformation is supplied as a fixed template or initial guess (p4, p16, p17)
  and is never re-predicted, never varied, and never scored. There is **no** TM6
  measurement, **no** active/inactive classification, **no** GPCRdb state label, **no**
  RMSD of the receptor to any reference, and **no** conformational-state predicate
  anywhere in the paper. The word "conformational" appears in a *state* sense exactly
  once, as a hypothetical risk in the Discussion, p15: "The fact that both prediction
  and generation methods are prone to reproducing previously seen complexes can
  negatively impact real drug design campains, where **conformational selectivity might
  be crucial**, i.e., when designing an antagonist for a receptor whose active
  structure-ligand complex has been memorized and thus resulting in inherently biased
  outputs." That is a stated concern, not a measurement. Recorded again under
  `unresolved` item 1 with the page.

  **On peptide placement — what actually is measured, with thresholds:**
  - **DockQ** (continuous, 0–1) is the primary metric, with the reason for choosing it
    over RMSD / TM-score / lDDT argued at length in Methods, p16: "The DockQ score was
    chosen over other scores such as RMSD, TM-score or lDDT as they were not fully
    applicable to any of the dimers in the dataset due to size of the peptides. For
    instance, since RMSD scales with the number of amino acids, a comparison between
    peptides of different lengths is hindered... we find that the DockQ score is most
    suitable for the task at hand as it takes into account ligand RMSD (LRMSD),
    interface RMSD (iRMSD) and the fraction of retained native contacts (fnat)."
  - **Thresholds, and they are borrowed not invented** — p5: "Analogous to the
    categorization of the DockQ authors, we will refer to predictions as 'incorrect'
    (DockQ < 0.23), 'acceptable quality' (0.23 ≤ DockQ < 0.49), 'medium quality'
    (0.49 ≤ DockQ < 0.8) and 'high quality' (DockQ ≥ 0.80)." Justification given: the
    DockQ authors' own categorisation. Clean.
  - **Components reported separately**: iRMSD (Å) and fnat (Fig 3B, 3C p6); LRMSD
    discussed but not plotted in the main text (p6).
  - **Arm 2 placement predicates are heuristic and NOT formally justified.** p11: "For
    our examples such misplaced peptides typically have an RMSD > 20 Å. Peptides that
    border the opening of the binding pocket but do not enter it are typically marked
    with a hotspot distance >10 Å in combination with an RMSD of ~15 Å or lower.
    Peptides that are 'flipped', i.e., enter with the opposite terminus than the
    reference peptide have a high RMSD but a short hotspot distance." These cut-offs
    are described as typical, per-example, with no stated derivation — the closest the
    paper comes to a rigour defect on the metric side. The inside/outside-pocket call
    is backed by an OPM membrane superposition plus contact analysis (p11, S7A Fig),
    which is an operationalised predicate, but the numeric bands above are not.
  - **Clash predicate**: Rosetta `PerResidueClashMetric`, "without
    minimization/relaxation" (Fig 8 caption p12) — binary at ≥1 clash.

- **metric_saturation**: **YES — numeric saturation is present, is explicitly named by
  the authors, and is part of the headline finding.**
  - **Ceiling on the confidence metrics.** Verbatim, p7→p9 (sentence spans the page
    break): "Conversely, there appears to be a ceiling effect where predictions with
    high DockQ score were rarely assigned a bad PAE, ipSAEmin or ipSAEmax score, in
    other words a low number of false-negatives." This is a stated *ceiling effect* in
    the paper's own words.
  - **Floor on ipSAEmin for AF2IG.** Fig 6 bottom-left panel (p9): AF2IG ipSAEmin sits
    at ≈0.0 across essentially the entire DockQ range 0–0.75, lifting only above
    DockQ ≈ 0.85. The reported ρ = 0.66 for that panel therefore rests on a metric that
    is floored for the great majority of predictions.
  - **Floor on DockQ and fnat for AF2IG.** p5: "AF2IG achieved a median DockQ score of
    0.03, with 70.65% of all predictions being 'incorrect'... marked by a median iRMSD
    of 12.2 Å and 68% of predictions with fnat ≤ 0.1." A metric whose median sits at
    0.03 on a 0–1 scale has bottomed out for that predictor.
  - **Complete floor on the distance-restricted PAE subset.** p9: "Specifically
    selecting entries from the PAE matrix that correspond to interchain pairs with
    ≤ 10 Å distance is entirely unsuitable to differentiate accurate from inaccurate
    placements (S5 Fig.)." (S5 Fig not held, so the shape of that failure cannot be
    checked.)
  - **Axis truncation is NOT recorded here** — per v3 it belongs to `hides`. Fig 8's
    "Outliers beyond 40 Å RMSD and 20 Å hotspot distance not shown for visual clarity"
    (p12) is cross-referenced to the Fig 8 row in section F.

- **directional_control**: **The method can be instructed *where the peptide goes*; it
  cannot be instructed *which receptor state to produce*, because the receptor state is
  imposed rather than predicted.** Handles, named:
  - **Arm 1 (prediction):** the *only* handles are (i) the **receptor template /
    initial guess**, which fixes the receptor conformation absolutely, and (ii) the
    **seed** (1–50). MSAs are ablated, so no MSA handle exists. There is no ligand
    handle, no partner handle, no nanobody handle, no state-annotated template. In
    practice this makes the prediction arm **seed-only** given a fixed template — hence
    the tag. And the seed handle is powerful and uncontrolled: p6, "using different
    seeds seemed to result in vastly different prediction qualities."
  - **Arm 2 (generation):** three explicit conditioning handles — **hotspot residues**
    (4–6 per target, p11), **peptide length** pinned to the native (p11), and
    **method-specific structure bias**: RFdiffusion3's `is_non_loopy = True` and
    `infer_ori_strategy: hotspots` on TIP atoms (p17), BindCraft's filter thresholds
    (p16), BoltzGen's peptide-anything protocol (p17). The introduction names the
    disorder handles generally, p2: "the first version of RFdiffusion, for instance,
    provides specific weights to reduce helical content, while BindCraft provides
    settings with softened AlphaFold2 confidence thresholds in order to allow the
    design of disordered peptides. Similarly, RFdiffusion3 biases generation towards
    unstructured protein segments via a 'is_non_loopy' flag."
  - **No state handle of any kind exists or is sought.** The vocabulary's Control tags
    (`ligand-driven`, `partner-driven`, `nanobody`, `g-protein-mimetic`,
    `apo-sampling`, `directed-state`) describe handles for *receptor* state and none
    of them applies. See `unresolved` item 12 on the missing "hotspot-driven" tag.

- **anti_memorization_design**: **YES — a per-method training-cutoff split, defined
  carefully, covering the full 113-dimer set.**
  - Cutoff dates, p6: **AF2IG 2021/10/30; Boltz-2 2023/01/06; RF3 2024/01/01.**
  - Split sizes, Fig 4 caption p7: "36/113 dimers were flagged pre AF2 training cutoff,
    68/113 dimers were flagged pre Boltz-2 training cutoff and 88/113 dimers were
    flagged pre RF3 training cutoff." → **post-cutoff n = 77 (AF2IG), 45 (Boltz-2),
    25 (RF3)** dimers, each × 50 seeds.
  - **How the cutoff was defined, and it is stricter than a bare release date.** p6:
    "Since several receptor-peptide pairs have been released multiple times we flagged a
    dimer as 'pre cutoff' if this specific pair was released prior to the respective
    training cutoff dates or a 'homologous' dimer prior to cutoff dates under a
    different PDB ID." Fig 4 caption, p7: "The 113 dimers were split into pre training
    cutoff and post training cutoff subsets according to their release date or the
    release date of a prior 'homologous' deposit, i.e., the same receptor-peptide pair
    under a different PDB ID." Crediting a redeposited pair to its earliest appearance
    is the correct conservative move and is worth citing.
  - **Arm 2 has NO cutoff design.** No training-cutoff analysis exists for BindCraft,
    BoltzGen or RFdiffusion3; their memorization is inferred from RMSD-to-native and
    sequence recovery instead (p11–p12).

- **anti_memorization_control**: **RUN AND ANALYSED for Arm 1 — this is one of the
  paper's two headline results. NONE RUN for Arm 2.** Not `UNPOWERED` at the dimer
  level for AF2IG (77) or Boltz-2 (45); the RF3 post-cutoff arm (25 dimers × 50 seeds)
  is the thinnest and should be quoted with that n attached.
  - Result, verbatim p5–p6: "When taking the release dates of the 113 dimers and the
    training cutoff dates of the three prediction methods into account, we further
    identified that **each of the three methods performs significantly better on dimers
    that could have been included in training** (Fig 4, S3 Fig)."
  - Effect size, p6: "The effect of training set inclusion was most visible in the
    fraction of 'high quality' predictions. Here, AF2IG, the model with the earliest
    training date cutoff (2021/10/30) showed the largest drop in 'high quality' models
    from **15.8% pre cutoff to 3.2% post cutoff**, followed by Boltz-2 (cutoff
    2023/01/06) with a reduction from **20.8% pre cutoff to 6.4% post cutoff**. The
    latest model, RF3 (cutoff 2024/01/01) was least impacted by the training cutoff
    split, with a reduction of **27.2% pre cutoff to 15.2% post cutoff**."
  - Restated in the Discussion, p14: "In fact, for all three prediction methods tested
    here, placement accuracy significantly decreases for complexes from our dataset
    that were submitted to the PDB for the first time after the respective training
    cutoffs."
  - **Caveat on "significantly":** `scipy.stats.mannwhitneyu` is named in Methods
    (p18), but no p-value, test statistic or effect-size CI for the pre/post comparison
    appears in the main text or in the Fig 4 panels. S3 Fig, which may carry it, is not
    held. See `unresolved` item 7.
  - **Arm 2: `NONE RUN`.** Memorization in the generative models is asserted from
    RMSD-to-native and sequence recovery — p12: "When targeting AT2 receptor, every
    generated peptide had an RMSD < 5 Å with 97.9% of peptides with an RMSD ≤ 1.5 Å.
    **This apparent memorization** also reflects on sequence level, where Boltzgen
    designs showed a sequence recovery of 0.25 for every AT2 design, while sequence
    recovery for any other method-target combination rarely exceeded 0.1 (S8A Fig.)."
    No training-cutoff split, no post-cutoff target, no held-out receptor is used for
    any generative method. The authors state the resulting limit, p15: "While our
    results do not show memorization for BindCraft and RFdiffusion3, it cannot be ruled
    out that these methods can show similar behavior for other targets."

- **controls_run**:

  | control | what it rules out | page |
  |---|---|---|
  | **Pre- vs post-training-cutoff split** of all 113 dimers, per predictor, with homologous-redeposit crediting | That reproduction accuracy is generalization rather than memorization. Rules it out for all three predictors: accuracy drops post-cutoff in every case | p6–p7, Fig 4, S3 Fig |
  | **50 seeds per prediction** (1–50, all three predictors) | That a single-seed result is representative; quantifies the seed-dependence of both DockQ and confidence | p4, p6, Fig 5 p8 |
  | **Peptide-ligand vs protein-ligand stratification** (≤50 vs >50 residues) | That ligand size is irrelevant. It is not: "100% of AF2IG-predicted, 82.1% of RF3-predicted and 35.5% of Boltz-2-predicted GPCR-protein ligand complexes achieve a DockQ score below 0.23" | p5, S2 Fig |
  | **Cyclic vs non-cyclic peptide split** | That disulfide cyclization explains the DockQ spread. It does not — "Splitting the dataset into cyclic and non-cyclic peptides, however, revealed no difference in DockQ score" | p5, S4 Fig |
  | **Length-stratified fnat vs iRMSD/LRMSD decomposition** | That failures on large ligands are misfolding of the ligand rather than global misplacement. Rules out misfolding-alone: "less than 20% retrieved native contacts, suggesting an overall misplacement relative to the receptor instead of a misfolded ligand alone" | p6, S2 Fig |
  | **Distance-restricted PAE subset (interchain pairs ≤10 Å)** | That a tighter interface-only PAE subset would rescue discrimination. It does not — "entirely unsuitable" | p9, S5 Fig |
  | **Best-seed vs all-seed confidence correlation**, best seed chosen by confidence not by DockQ | That seed-averaging is what destroys the confidence–accuracy correlation. Partially rules it in for pLDDT/ipSAEmax, rules it out for PAE (correlations *drop* on best-seed) | p9–p10, Fig 6 |
  | **AF2IG weight sweep, model_1_ptm–model_5_ptm** | That AF2IG's poor showing is an artefact of weight choice. **But the sweep was run on the benchmark set itself — see `oracle_leakage` route 4** | p16, S9 Fig |
  | **Boltz-2 `--use_potentials` on/off** | That the potentials flag is a confound. "no significant difference could be observed" | p16, S10 Fig |
  | **BindCraft RMSD/pLDDT filters set to null / 0.5** | That BindCraft's internal accept-reject filters truncate the sampled space and inflate its apparent quality; both Accepted and Rejected trajectories were collected | p16 |
  | **Rosetta `PerResidueClashMetric` on all 30,000 designs per method** | That in-pocket placement implies a physically valid pose. Rules it out: up to 87.4% clashing | p12, Fig 8 |
  | **OPM membrane-plane superposition + contact analysis** | That a short hotspot distance implies in-pocket placement. Rules it out — catches designs contacting the *outside* of the helix bundle: "A typical error in GPCR-targeting peptide design is that the designed peptide is placed on the outside of the helix bundle and in contact with membrane-facing residues. Such cases often result in a short hotspot distance" | p11, S7A/S7B Fig |
  | **ProteinMPNN redesign of the same 90 backbones** | That poor reprediction reflects poor backbones. Separates backbone quality from sequence quality — sequence is the weaker half | p13–p14, Fig 9 |
  | **Orthogonal cross-validation: every generative method re-predicted by all three predictors** | That a generative method is being flattered by its own paired predictor. "this allowed for each generative method to be evaluated both for prediction and generation, thus being cross-validated orthogonally" | p3, p13, Fig 9 |
  | **ETB multi-peptide case study** (3 near-identical peptides, one receptor) | That confidence tracks accuracy when the receptor and fold are held constant and only sequence varies — the tightest confidence control in the paper | p10–p11, Fig 7 |

  **Controls NOT run, and their absence matters:** no apo/no-peptide arm; no scrambled
  or shuffled peptide sequence arm; no decoy or off-target receptor arm; no MSA-on
  comparison arm (acknowledged, p14); no alternative-receptor-state template arm; no
  experimental arm of any kind.

- **confidence_as_discriminator**: **YES — this is the paper's central question, and
  they validated the use of confidence against a structural ground truth. THIS IS THE
  MAIN DELIVERABLE FOR US.**

  **The claim, verbatim, abstract, p1:**
  > "Our results indicate that current design pipelines primarily suffer from
  > **significant confidence overestimation for misplaced peptides** in the validation
  > phase **across all three prediction methods**."

  **Framing, verbatim, abstract, p1:**
  > "The recent advances of deep learning-based protein structure generation and
  > structure prediction offer a multitude of peptide design stategies for GPCRs, yet
  > **confidence metrics rarely correlate with experimental success**. In the context of
  > peptides, this problem is exacerbated due to the lack of elaborate tertiary
  > structures in peptides, raising the question of whether this is due to inadequate
  > sampling or insufficient scoring."

  **The mechanism, verbatim, Results, p7:**
  > "An overall trend with the other PAE confidences is **over-estimation, where
  > incorrect predictions exhibit the same PAE or ipSAE scores as correct predictions,
  > signifying a large number of false positives. This is most prominent with Boltz-2,
  > where medium to low quality predictions were indistinguishable from high quality
  > predictions through PAE-based confidence alone.**"

  **The complementary ceiling, verbatim, p7→p9:**
  > "Conversely, there appears to be a ceiling effect where predictions with high DockQ
  > score were rarely assigned a bad PAE, ipSAEmin or ipSAEmax score, in other words a
  > low number of false-negatives."

  **The concrete demonstration (ETB case study), verbatim, p11:**
  > "In contrast, Boltz-2 reproduced endothelin-1 virtually perfectly with a narrow
  > distribution in both DockQ and inter-chain PAE scores, yet it demonstrated stronger
  > seed-dependent DockQ variance for endothelin-3 and sarafotoxin S6b. **The
  > corresponding inter-chain PAE scores, however, only increased slightly compared to
  > the near-perfect predictions of endothelin-1, highlighting that incorrectly placed
  > peptides are not necessarily detectable through confidence values.**"

  **And for RF3, verbatim, p11:**
  > "Lastly, RF3 demonstrated significant seed-dependent spread in DockQ scores for
  > endothelin-1, ranging from incorrect to high-quality predictions. For endothelin-3
  > it was unable to predict correct peptide placements and for sarafotoxin S6b the
  > structural prediction was predominantly of medium quality. **This diversity was
  > strongly contrasted by high prediction confidences with narrow spread across all
  > three peptides, demonstrating that for RF3, incorrect predictions are
  > indistinguishable from correct predictions when considering PAE confidences
  > alone.**"

  **The Discussion restatement, verbatim, p14:**
  > "By simulating a de novo peptide design task with known structural references we
  > substantiated the fact that **PAE matrix-derived confidence metrics often
  > overestimate and are generally insufficient in differentiating correct peptide
  > placements from incorrect placements**, with peptide pLDDT and inter-chain PAE
  > being the best performing metrics."

  **And the transferability warning, verbatim, p14:**
  > "This complicates comparability of de novo design protocols centered around
  > specific prediction methods as **confidence thresholds are not transferable**."

  **Which metrics over-estimate, and by how much.** The paper quantifies
  discrimination as Spearman ρ between the confidence metric and DockQ, over
  **n = 5,650 predictions per predictor** (113 dimers × 50 seeds), and identifies
  over-estimation qualitatively from the point clouds in Fig 6 (p9) rather than as a
  count of miscalibrated cases (see `unresolved` item 8):

  | metric | AF2IG | Boltz-2 | RF3 | source |
  |---|---|---|---|---|
  | inter-chain PAE (all seeds) | ρ = **−0.829** (text) / **−0.84** (panel) | ρ = **−0.56** (text) / **−0.50** (panel) | ρ = **−0.894** (text) / **−0.89** (panel) | p7 text; Fig 6 middle row p9 |
  | inter-chain PAE (best seed) | −0.83 | **−0.27** | −0.89 | Fig 6 p9; p10 |
  | PAE peptide (all → best seed) | −0.50 → −0.46 | **−0.56 → −0.34** | −0.77 → −0.76 | Fig 6 top row p9; p10 |
  | ipSAEmin (all → best seed) | 0.66 → 0.68 | **0.65 → 0.52** | **0.79 → 0.71** | Fig 6 bottom row p9; p9 |
  | ipSAEmax (all → best seed) | NOT REPORTED | 0.63 → **0.79** | 0.74 → **0.84** | p9 |
  | peptide pLDDT (all seeds) | **ρ = 0.02** | 0.76 | 0.71 | p7, S6 Fig |
  | peptide pLDDT (best seed) | NOT REPORTED | **0.81** | **0.81** | p9 |
  | distance-restricted PAE (≤10 Å interchain pairs) | "entirely unsuitable" | "entirely unsuitable" | "entirely unsuitable" | p9, S5 Fig |

  **Reading of the table.** Boltz-2 — the *most accurate* predictor by median DockQ
  (0.56, p5) — is the *worst calibrated*: its inter-chain PAE ρ is −0.50/−0.56 against
  −0.83/−0.89 for the other two, and it degrades to −0.27 on best-seed selection. AF2IG
  — the *least accurate* (median DockQ 0.03) — has essentially **zero** pLDDT–accuracy
  correlation (ρ = 0.02) while its inter-chain PAE is the second-best discriminator. So
  accuracy and calibration are decoupled across predictors, and no single confidence
  metric is best across all three. The authors' recommendation, p15: "we suggest
  rationally motivated peptide generation as opposed to 'blind' exploration, with
  inter-chain PAE or peptide pLDDT as primary scoring metrics" and "To avoid the
  reliance on a single structure prediction tool for validation, we suggest the use of
  orthogonal structure validation, e.g., by using both RosettaFold3 and Boltz-2 with a
  large number of seeds."

  **A dramatic single case:** Boltz-2's best median DockQ coexists with catastrophic
  outliers that confidence does not flag — p5: "Although the majority of Boltz-2
  predictions showed a low iRMSD (median of 2.2 Å), a small number of peptide
  predictions were drastically misplaced with an **iRMSD of 66.26 Å**."

  **Was the use of confidence validated?** Yes — that is what Fig 6 (p9) is. Confidence
  is plotted against an independent structural ground truth (DockQ to the crystal
  reference) over all 5,650 predictions per predictor, with Spearman ρ and p-values
  printed in every panel, and the best-seed selection made by **confidence, not by
  DockQ** (Fig 6 caption, p9). This is the validated-use case and is exactly why the
  finding is citable.

## D. Claims

- **central_conclusion**: Across a 113-complex GPCR–peptide/protein reproduction
  benchmark and a 90,000-design generative benchmark on three receptors, PAE-derived
  confidence metrics systematically over-estimate for misplaced peptides in all three
  tested predictors (AF2IG, Boltz-2, RF3), so confidence-first filtering cannot
  separate correct from incorrect peptide placement; accuracy is additionally strongly
  seed-dependent and drops significantly for complexes deposited after each model's
  training cutoff, i.e. memorization is present in all three predictors and (as
  apparent memorization) in BoltzGen. Separately, all three generative methods sample
  the constrained orthosteric pocket adequately at the backbone level, but their
  simultaneous sequence generation is the weak half and is partially recovered by a
  single ProteinMPNN sequence per backbone.

- **necessity_claims** — **verbatim + page:**
  1. p3: "As high-throughput production and testing of de novo peptides is
     significantly less feasible compared to de novo proteins **robust filters and
     selection criteria are imperative**."
  2. p3: "For de novo peptides to mimic or compete with endogenous peptides, **similar
     specificity is mandatory**."
  3. p11: "**These two distances must be considered together** to differentiate
     peptides placed inside the binding pocket from peptides placed outside the binding
     pocket."
  4. p9 (impossibility form): "Specifically selecting entries from the PAE matrix that
     correspond to interchain pairs with ≤ 10 Å distance is **entirely unsuitable** to
     differentiate accurate from inaccurate placements (S5 Fig.)."
  5. p11 (impossibility form): "...demonstrating that for RF3, **incorrect predictions
     are indistinguishable from correct predictions** when considering PAE confidences
     alone."
  6. p14: "In the light of frequent release of new tools, **re-occurring assessment of
     their performance on peptide design is imperative**."
  7. p14: "This complicates comparability of de novo design protocols centered around
     specific prediction methods as **confidence thresholds are not transferable**."
  8. p15 (impossibility form): "On that note, **it is important to remember that
     structure prediction and structure generation tools are not equivalent to
     protein-protein or peptide-protein docking algorithms.** While they are extremely
     powerful in providing a statistical approximation for the placement and
     orientation of the peptide, **they lack the required precision for side-chain
     interactions.**"
  9. p15 (strong recommendation, one step below a necessity claim): "This ties into the
     current limitations of confidence-first filters and **we strongly suggest
     incorporating supplemental structural filters for de novo peptide design**, either
     through measuring the recovery of hotspot residue contacts, through scaffolding or
     through comparison with known peptides in combination with physics-informed
     validations such as the Rosetta interface_ΔG or shape complementarity, similar to
     BindCrafts filter implementation."

- **novelty_claims** — **verbatim + page:**
  1. p3 (the priority claim): "While prediction accuracies specifically of the entire
     ligand-GPCR-G protein complex have been assessed previously for AlphaFold2 and
     AlphaFold3 [33,34], **a de novo design-centric benchmark for GPCRs is missing**."
  2. p14: "**Here, we offer a peptide-GPCR-specific assessment** of current
     possibilities and limitations of recently released methods in structure prediction
     and generation."
  3. p14 (novelty framed as substantiation rather than firstness — note the wording):
     "The problem of high false positive rates in computational design is not new but
     due to the lack of references for de novo proteins, it is often viewed from the
     perspective of experimental success [50,51]. **By simulating a de novo peptide
     design task with known structural references we substantiated the fact that** PAE
     matrix-derived confidence metrics often overestimate..." — i.e. the authors
     explicitly do **not** claim the confidence problem is a new discovery; they claim
     novelty in demonstrating it against structural references on GPCRs.
  4. p1 abstract: "Taken together, **our benchmark offers guidance** for the design of
     peptides specifically using deep learning-based pipelines."

- **stated_limits** (author-stated, verbatim where load-bearing):
  1. **No MSAs**, p14: "In this context it is worth noting that no MSAs have been used
     in our setup. This is a typical trade-off between runtime and accuracy and the
     number of false positive peptide predictions might decrease if MSAs were included."
  2. **GPCR-specific, may not transfer**, p14: "At the same time, this might be
     different for other design targets as GPCRs are structurally and mechanistically
     highly conserved while the orthosteric binding site requires less conservation to
     facilitate ligand selectivity."
  3. **Memorization not excluded for two of three generative methods**, p15: "While our
     results do not show memorization for BindCraft and RFdiffusion3, it cannot be ruled
     out that these methods can show similar behavior for other targets."
  4. **Sampling depth unresolved**, p15: "Overall, the number of generations necessary
     remains elusive and highly target dependent. However, it can likely be reduced by
     fine-tuning the location and number of hotspot residues."
  5. **Near-default settings only**, p15: "Furthermore, we applied each method with
     near-default settings or peptide-specific settings recommended by the authors and
     each method offers a number of adjustments to balance designability and diversity,
     which have to be evaluated before designing on a specific target."
  6. **Clashing designs discarded, possibly wrongly**, p15: "We purposefully excluded
     sterically clashing designs from further analysis although they might still be
     plausible candidates if they were subjected to refinement, i.e., in the form of
     Rosetta minimization or relaxation."
  7. **ProteinMPNN's improvement may be circular**, p15: "In this context it is
     important to note that the improved prediction placement of these sequences is not
     an immediate indicator for downstream experimental success as ProteinMPNN
     inherently produces sequences favored by prediction tools." — a self-aware
     statement about the predictor-favouring loop, worth citing on its own.
  8. **Functional groups stripped from the peptides**, p16: "Any functional groups
     attached to the binding pocket-intruding terminus, such as NH2, were removed.
     Although these functional groups usually are crucial for GPCR activation, we argue
     that they play a minor role in the prediction process of the remaining peptide
     backbone."
  9. **Membrane placement is a known, unfixed failure mode**, p15: "Similarly, in the
     special case of membrane-bound proteins, a substantial improvement in avoiding
     placements in the membrane region could be achieved by solubilizing the target
     protein, either through the use of SolubleMPNN or through rationally mutating the
     respective positions."
  **Not stated by the authors as a limit** (extractor observation, recorded here so it
  is not mistaken for an author admission): there is **no experimental validation of
  any kind**, and **receptor conformational state is never assessed** — see
  `unresolved` items 1 and 11.

- **stance**: **`precedent` + `contrast` — PROVISIONAL, the user's call.**
  - **precedent (on findings):** a peer-reviewed, GPCR-specific, n = 16,950-prediction
    demonstration that confidence over-estimates for misplaced ligands across three
    independent predictors, plus a clean training-cutoff memorization control. This is
    directly citable support for a confidence-does-not-track-correctness claim on our
    system class.
  - **contrast (on scope and on rigour):** the receptor is handed in as a fixed
    template and its conformational state is **never** assessed (see `state_metric`),
    so nothing here speaks to state prediction; MSAs are fully ablated, so the numbers
    are a floor rather than a realistic pipeline; the design arm's success criterion is
    similarity to the native peptide (design-level oracle, route 7) on **three**
    targets; and the model-weight choice was made on the benchmark set (route 4).

## E. Quantitative comparators

### metrics_reported

**Arm 1 — VALIDATION arm.** n = 113 dimers × 50 seeds = **5,650 predictions per
predictor**, 16,950 total, unless a row says otherwise.

| metric | value | units | measured against | page |
|---|---|---|---|---|
| median DockQ, AF2IG | 0.03 | DockQ (0–1) | crystal reference peptide, all 5,650 preds | p5 |
| median DockQ, Boltz-2 | **0.56** | DockQ | same | p5 |
| median DockQ, RF3 | 0.41 | DockQ | same | p5 |
| % 'incorrect' (DockQ<0.23), AF2IG | 70.65 | % of preds | same | p5 |
| % 'incorrect', RF3 | 36.31 | % of preds | same | p5 |
| % 'high quality' (DockQ≥0.8), AF2IG | 7.15 | % of preds | same | p5 |
| % 'high quality', RF3 | 24.22 | % of preds | same | p5 |
| % 'acceptable'+'medium' (0.23–0.8), RF3 | 39.46 | % of preds | same | p5 |
| % 'medium quality' or better, Boltz-2 | 62.16 | % of preds | same | p5 |
| median iRMSD, AF2IG | 12.2 | Å | crystal reference interface | p5 |
| median iRMSD, Boltz-2 | 2.2 | Å | same | p5 |
| worst iRMSD, Boltz-2 | **66.26** | Å | same | p5 |
| % preds with fnat ≤ 0.1, AF2IG | 68 | % of preds | native contacts of reference | p5 |
| % protein-ligand complexes with DockQ<0.23 | AF2IG 100 / RF3 82.1 / Boltz-2 35.5 | % | 22 GPCR–protein complexes | p5, S2 Fig |
| cyclic vs non-cyclic DockQ | "no difference" | — | crystal reference | p5, S4 Fig |
| 'high quality' pre→post training cutoff, AF2IG | 15.8 → 3.2 | % of subset | 36 pre / 77 post dimers | p6, Fig 4 p7 |
| 'high quality' pre→post, Boltz-2 | 20.8 → 6.4 | % of subset | 68 pre / 45 post dimers | p6, Fig 4 p7 |
| 'high quality' pre→post, RF3 | 27.2 → 15.2 | % of subset | 88 pre / 25 post dimers | p6, Fig 4 p7 |
| 'medium quality' pre→post | AF2IG 6.0→10.8 / Boltz-2 50.3→47.0 / RF3 17.8→29.2 | % of subset | same subsets | Fig 4 p7 |
| 'acceptable quality' pre→post | AF2IG 10.4→16.0 / Boltz-2 12.2→30.4 / RF3 20.4→23.1 | % of subset | same subsets | Fig 4 p7 |
| 'incorrect' pre→post | AF2IG 67.8→70.1 / Boltz-2 16.7→16.2 / RF3 34.5→32.4 | % of subset | same subsets | Fig 4 p7 |
| pre-cutoff subset sizes | 36 / 68 / 88 of 113 | dimers | AF2 / Boltz-2 / RF3 | Fig 4 caption p7 |
| training cutoff dates | 2021/10/30 / 2023/01/06 / 2024/01/01 | date | AF2 / Boltz-2 / RF3 | p6 |
| Spearman ρ, inter-chain PAE vs DockQ | AF2IG −0.829 / Boltz-2 −0.56 / RF3 −0.894 (text); −0.84 / −0.50 / −0.89 (Fig 6 panels) | ρ | 5,650 preds per predictor | p7; Fig 6 p9 |
| Spearman ρ, PAE peptide vs DockQ | AF2IG −0.50 / Boltz-2 −0.56 / RF3 −0.77 | ρ | same | Fig 6 p9 |
| Spearman ρ, ipSAEmin vs DockQ | AF2IG 0.66 / Boltz-2 0.65 / RF3 0.79 | ρ | same | Fig 6 p9 |
| Spearman ρ, ipSAEmax vs DockQ (all seeds) | Boltz-2 0.63 / RF3 0.74 | ρ | same | p9 |
| Spearman ρ, peptide pLDDT vs DockQ | AF2IG **0.02** / Boltz-2 0.76 / RF3 0.71 | ρ | same | p7, S6 Fig |
| best-seed ρ, peptide pLDDT | Boltz-2 0.81 / RF3 0.81 | ρ | 113 best-seed preds per predictor | p9 |
| best-seed ρ, ipSAEmin | Boltz-2 0.65→0.52 / RF3 0.79→0.71 | ρ | same | p9 |
| best-seed ρ, ipSAEmax | Boltz-2 0.63→0.79 / RF3 0.74→0.84 | ρ | same | p9 |
| best-seed ρ, inter-chain PAE, Boltz-2 | −0.50 → −0.27 | ρ | same | p10 |
| best-seed ρ, PAE peptide, Boltz-2 | −0.56 → −0.34 | ρ | same | p10 |
| distance-restricted PAE (≤10 Å) | "entirely unsuitable" | — | same | p9, S5 Fig |
| seed-driven DockQ range, single dimer (8flu, 6b3j; AF2IG) | 0.03 – 0.85 | DockQ | 50 seeds on one dimer | p6, S1 Fig |
| per-target divergence, 7w53 | RF3 0.81 / Boltz-2 0.24 / AF2IG 0.12 | median DockQ | 50 seeds, 7-aa peptide | p6 |
| per-target divergence, 8f7w | Boltz-2 0.83 / AF2IG 0.24 / RF3 0.43 | median DockQ | 50 seeds, 8-aa peptide | p6 |

**Arm 2 — DESIGN arm.** n = 10,000 designs per method per receptor; 30,000 per method;
**90,000 designs total**; 3 receptors (AT2 6jod / ETB 6lry / NOP 8f7x).

| metric | value | units | measured against | page |
|---|---|---|---|---|
| designs generated | 10,000 × 3 methods × 3 receptors = 90,000 | designs | — | p11, Fig 8 p12 |
| BoltzGen designs placed inside the pocket | **100** (all 30,000) | % | OPM membrane plane + contact analysis | p11 |
| RFdiffusion3 designs placed outside the pocket / membrane-contacting | 85.8 (AT2) / 15.02 (NOP) | % of 10,000 | same | p11, S7B Fig |
| BoltzGen ETB designs with RMSD ≤ 5 Å to reference | 79.8 | % of 10,000 | native sarafotoxin S6b (6lry) | p11 |
| BoltzGen AT2 designs with RMSD < 5 Å | 100 | % of 10,000 | native Ang II (6jod) | p11–p12 |
| BoltzGen AT2 designs with RMSD ≤ 1.5 Å | **97.9** | % of 10,000 | same | p12 |
| BoltzGen AT2 sequence recovery | **0.25** for every design | fraction | native Ang II sequence | p12, S8A Fig |
| sequence recovery, all other method–target combinations | "rarely exceeded 0.1" | fraction | native peptide sequence | p12, S8A Fig |
| clashing designs, BindCraft | AT2 23.1 / ETB 51.7 / NOP 43.6 | % of 10,000 | Rosetta PerResidueClashMetric, no relax | Fig 8 p12 |
| clashing designs, BoltzGen | AT2 60.3 / ETB 62.0 / NOP 36.6 | % of 10,000 | same | Fig 8 p12 |
| clashing designs, RFdiffusion3 | AT2 14.6 / ETB **87.4** / NOP 66.5 | % of 10,000 | same | Fig 8 p12, p12 text |
| reprediction 'high quality', initial design sequences | BindCraft+AF2IG **60.9** / BoltzGen+RF3 39.2 / BoltzGen+Boltz-2 32.1 / RFdiffusion3+RF3 12.2 | % | DockQ vs the initially designed peptide | p13 |
| ProteinMPNN gain, 'medium quality', RFdiffusion3 designs | AF2IG 23.1→34.2 / Boltz-2 16.9→39.2 / RF3 22.3→48.1 | % | same | p14 |
| ProteinMPNN effect on 'high quality' | "a reduction in the DockQ high quality category" (no number given) | — | same | p14 |
| ProteinMPNN sequence recovery | "remained on the same level as with the initially produced sequences for all designs, apart from BindCraft designs targeting AT2" | — | native peptide sequence | p14 |
| BindCraft design attempts before downsampling | 15,304 (6jod) / 13,520 (6lry) / 16,810 (8f7x) = **45,634** | trajectories | — | p16 |

**Dataset-assembly numbers (both arms).**

| metric | value | units | measured against | page |
|---|---|---|---|---|
| GPCRdb protein/peptide entries retrieved | 414 | complexes | GPCRdb ligand-type filter | p3, Fig 2A p5 |
| after filtering (non-redundant, gapless, canonical AAs, dimers only, best resolution) | **113** | dimers | — | p3, p16, Fig 2A p5 |
| class A receptors / ligands | 58 / 74 | count | — | p3, Fig 2A p5 |
| class B1 receptors / ligands | 14 / 26 | count | — | p3, Fig 2A p5 |
| GPCR–peptide vs GPCR–protein split | 91 / 22 (incl. 4 nAbs) | complexes | — | p1 abstract |
| peptide length range | 3 – 137 | amino acids | — | p3, Fig 2B p5 |
| shortest peptide | 3 aa (substance P fragment, MRGPRX2, PDB 7vdm) | aa | — | p3 |
| most-represented receptors | GLP1R (5 complexes), ETB (4 complexes per p3; "five times" per p10 — see `unresolved` item 3) | complexes | — | p3, p10 |

- **n_predictions**: recorded separately, per the field's instruction.
  - **Arm 1, samples per target:** **50** (seeds 1–50), for each of the three
    predictors (p4, p16, p17).
  - **Arm 1, targets:** **113** dimers (p3).
  - **Arm 1, total:** 113 × 50 = **5,650 predictions per predictor**;
    × 3 predictors = **16,950 predictions**.
  - **Arm 2, samples per target:** **10,000** designs per generative method per
    receptor (p11).
  - **Arm 2, targets:** **3** receptors (AT2, ETB, NOP) × 3 generative methods (p11).
  - **Arm 2, total generated:** **90,000 designs** (30,000 per method).
  - **Arm 2, BindCraft raw attempts before random downsampling:** 45,634 across the
    three targets, downsampled to 10,000 each with `pandas.DataFrame.sample()` (p16).
  - **Arm 2, reprediction sub-study:** **90 backbones** (10 per method × receptor cell)
    × 2 sequence sources (initial design sequence, one ProteinMPNN sequence) ×
    3 predictors × 50 seeds = **27,000 predictions**. Selection rule, Fig 9 caption
    p13: "10 out of 10000 generated peptides per method and reference (90 in total)
    were selected uniformly along peptide RMSD ≤ 18 Å and with hotspot distance ± 2 Å
    of reference hotspot distance." **n = 10 per cell is at the schema's `UNPOWERED`
    boundary; see `unresolved` item 10.**
  - **Grand total of structure predictions in the paper:** 16,950 (Arm 1) + 27,000
    (Arm 2 reprediction) = **43,950**, plus 90,000 generative designs.

- **comparable_to_ours**: *(left empty by the extractor per schema v3 — populated by
  whoever holds `STATUS.md` and the manuscript)*

- **si_in_scope**: **SI NOT HELD.** The PDF is the 21-page main text only. Cited and
  absent (list at p18): **S1 Table** (the 113 complexes — PDB IDs, receptors, peptides,
  and the release dates the entire cutoff analysis depends on), **S2 Table** (the
  hotspot residues), **S1 Fig** (exemplary 6lry predictions), **S2 Fig** (DockQ
  components stratified by ligand length), **S3 Fig** (DockQ components stratified by
  training-set inclusion — the per-component version of the memorization control),
  **S4 Fig** (cyclic vs non-cyclic), **S5 Fig** (the distance-restricted PAE result),
  **S6 Fig** (input structures for generation; also cited at p7 and p14 as the source
  of the pLDDT correlations and the distance-based PAE comparison — see `unresolved`
  item 5), **S7 Fig** (membrane definition and design placements), **S8 Fig** (sequence
  recovery), **S9 Fig** (the AF2IG weight sweep — the route-4 leakage evidence),
  **S10 Fig** (the Boltz-2 `--use_potentials` test). Underlying data are on Zenodo,
  10.5281/zenodo.18755322 (p2), not retrieved.
  **Impact on this note: MODERATE, not fatal.** Unlike several papers in this corpus,
  **the headline confidence numbers are in the main text and in Fig 6 (p7, p9, p10)**,
  and the memorization percentages are in Fig 4 (p7). What is lost to the SI: all
  per-complex data, the pLDDT scatter itself, the sequence-recovery distributions, and
  the two Methods sweeps that constitute the route-4 leakage.

## F. Figures

**12 panel-group rows across 9 figures.** Pages 4, 5 (×2), 6, 7, 8, 9, 10 (×3), 12, 13.
Five pages were rendered at 150 dpi to fill `data_shape` where the captions did not
carry panel structure (pp. 5, 6, 7, 8, 10) plus two confirmatory renders (pp. 9, 12,
13); all renders were deleted afterwards.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| **1** | 4 | Two-arm benchmark workflow: 113 dimers → 3 predictors → DockQ + confidence (A); 3 targets → 3 generative methods → 10,000 designs each → filter → ProteinMPNN → repredict (B) | schematic | `SCHEMATIC \| two-arm benchmark workflow: prediction arm (113 dimers, template + no MSA, 50 seeds, DockQ/confidence) and generation arm (3 targets, 10000 designs, hotspot distance/RMSD/clashes, 90 designs repredicted) \| no data` | 2 (A = validation arm, B = design arm); vary by arm | | CC-BY 4.0, no ND (p1) |
| **2A** | 5 | Dataset funnel: 414 GPCRdb entries → 113 unique pairs, and the class A/B1 receptor and ligand counts | bar | `PLOT \| facet: none (1) \| vary: dataset category (6: GPCRdb entries, filtered unique pairs, class A receptors, class A ligands, class B1 receptors, class B1 ligands) \| series: none (1) \| measure: count of entries \| mark: bar \| n: 1 count per mark, 6 marks per panel` | 1 | | CC-BY 4.0, no ND (p1) |
| **2B** | 5 | Histogram of peptide lengths in the 113-complex set, 3–137 aa | bar (histogram) | `PLOT \| facet: none (1) \| vary: peptide length 3–137 aa (continuous) \| series: none (1) \| measure: count of complexes \| mark: bar \| n: 113 complexes per panel, 1–9 per bin` | 1 | x-axis tick labels are non-uniformly spaced (1, 5, 10, 20, 30, 40, 50, 60, 70, 99, 112, 125, 129, 137) so the long-ligand tail is visually compressed relative to the short-peptide mode | CC-BY 4.0, no ND (p1) |
| **3A-C** | 6 | Pooled distributions of DockQ, iRMSD and fnat over all 5,650 predictions per predictor — the headline accuracy panel | violin | `PLOT \| facet: metric (3: DockQ, iRMSD, fnat) \| vary: prediction method (3: AF2IG, Boltz-2, RF3) \| series: prediction method (3, colour redundant with vary) \| measure: DockQ + iRMSD (Å) + fraction of retrieved native contacts \| mark: violin (with inner box) \| n: 5650 per violin (113 dimers × 50 seeds), 3 violins per panel` | 3 (A/B/C), vary by metric — one row, per the v3 rule that panels differing only in metric under identical faceting share a compound measure | pools all 113 systems into one violin per predictor, so per-system behaviour — which the paper's own Fig 5 shows is the dominant variance — is invisible here; the training-cutoff split is also pooled away | CC-BY 4.0, no ND (p1) |
| **4** | 7 | Memorization control: percent of each DockQ quality class, pre vs post training cutoff, per predictor | bar | `PLOT \| facet: DockQ quality class (4: high ≥0.8, medium 0.49–0.8, acceptable 0.23–0.49, incorrect <0.23) \| vary: prediction method (3) \| series: training-set inclusion (2: pre cutoff hatched, post cutoff solid) \| measure: percent of subset \| mark: bar \| n: pre-cutoff 36/68/88 and post-cutoff 77/45/25 dimers for AF2IG/Boltz-2/RF3, each ×50 seeds; per-bar n NOT shown on the figure` | 4 panels (2×2), vary by DockQ class; 6 bars each | **bars hide distributions** — each bar collapses 1,250–4,400 predictions to one percentage; **n is not shown on any bar** (it is only in the caption, and only as dimer counts); **no error bars, no CIs and no significance markers** although the accompanying text claims all three methods "perform significantly better" pre-cutoff (p5–p6) and no p-value appears anywhere in the main text | CC-BY 4.0, no ND (p1) |
| **5** | 8 | Per-complex DockQ over 50 seeds, all 113 receptor–peptide pairs × 3 predictors, sorted by ligand length — the seed-variance panel | box | `PLOT \| facet: length-sorted row block (6) \| vary: receptor–peptide pair (113 PDB IDs, sorted by ligand length 3–137 aa) \| series: prediction method (3: AF2IG, Boltz-2, RF3) \| measure: DockQ \| mark: box \| n: 50 per box, 3 boxes per PDB ID, ~57 boxes per row, 339 boxes total` | 6 rows of ~19 PDB IDs; a vertical rule in row 4 separates peptide from protein ligands | **the caption's colour key is wrong**: it states "blue: AF2IG, orange: Boltz2, green: RF3" but the plotted AF2IG marks and the figure's own legend are red/salmon, not blue (verified by rendering p8 at 150 dpi). Also: 339 boxes at this density make individual medians unreadable without magnification, and the six row-blocks share no common x-axis, so the length ordering is only legible from the printed tick labels | CC-BY 4.0, no ND (p1) |
| **6** | 9 | **The confidence figure.** Three PAE-family confidence metrics against DockQ, for each predictor, all 5,650 predictions each, with in-panel Spearman ρ and p for all-seeds and best-seed | scatter | `PLOT \| facet: confidence metric (3: PAE peptide, inter-chain PAE, ipSAEmin) × prediction method (3: AF2IG, Boltz-2, RF3) = 9 \| vary: DockQ, 0–1 (continuous) \| series: seed selection (2: all seeds as translucent dots, best-seed-by-confidence as outlined dots) \| measure: confidence value (PAE in Å, 0–30; ipSAEmin unitless, 0–1) \| mark: point \| n: 5650 points per panel, of which 113 are outlined best-seed points` | 9 (3 metric rows × 3 method columns); ρ and p printed in every panel for both seed selections | | CC-BY 4.0, no ND (p1) |
| **7A-left** | 10 | Superposition of ETB with endothelin-1, endothelin-3 and sarafotoxin S6b — three near-identical peptide folds, different sequences | structure render | `RENDER \| facet: none (1) \| views: 1 (extracellular, looking into the orthosteric pocket) \| overlay: 3 peptide structures on 1 receptor \| axis: none` | 1 | | CC-BY 4.0, no ND (p1) |
| **7A-right** | 10 | Sequence alignment of the three ETB peptides, residues differing from endothelin-1 in red, disulfide brackets below | schematic | `SCHEMATIC \| sequence alignment of endothelin-1, endothelin-3 and sarafotoxin S6b with substitutions coloured and two disulfide bridges bracketed \| no data` | 1 | | CC-BY 4.0, no ND (p1) |
| **7B** | 10 | The confidence-miscalibration case study: DockQ and inter-chain PAE over 50 seeds for three structurally near-identical ETB peptides | box | `PLOT \| facet: peptide (3: endothelin-1/8iy5, endothelin-3/6igk, sarafotoxin S6b/6lry) \| vary: prediction method (3) \| series: prediction method (3, colour) \| measure: DockQ + inter-chain PAE (Å) on paired sub-axes \| mark: box \| n: 50 predictions per box; 6 boxes per facet (3 methods × 2 measures)` | 3 facets, each with a paired DockQ sub-axis and inter-chain PAE sub-axis — one row per the compound-measure rule (same mark, same faceting) | **all three peptides shown are pre-training-cutoff for all three predictors** (stated at p10: "structures of all three peptide-receptor complexes were included in training of AF2, Boltz-2 and RF3"), so the panel cannot separate confidence miscalibration from memorization; **only 3 of the 4–5 ETB complexes in the dataset are shown**, with no stated reason for dropping the others; AF2IG's boxes are missing entirely from the endothelin-1 and endothelin-3 facets in the rendered figure (consistent with the text's "AF2IG is unable to reproduce the correct peptide placement", p10–p11, but the absent box reads as missing data rather than as a floored result) | CC-BY 4.0, no ND (p1) |
| **8** | 12 | Sampling breadth of the three generative methods: RMSD-to-native against hotspot distance for 10,000 designs per method per receptor, clashing designs greyed | scatter | `PLOT \| facet: generative method (3: BindCraft, BoltzGen, RFdiffusion3) × target receptor (3: AT2, ETB, NOP) = 9 \| vary: shortest hetero-atom distance to hotspots, 0–20 Å (continuous) \| series: clash status (2: non-clashing coloured by method, ≥1 steric clash in grey) \| measure: Cα-RMSD of designed peptide to native peptide, 0–40 Å \| mark: point \| n: 10000 designs per panel, 90000 total; per-panel clash percentage printed in-panel` | 9 (3 method columns × 3 receptor rows); dotted line marks the reference peptide's own hotspot distance | **both axes are truncated and the removed points are exactly the failure mode under study**: "Outliers beyond 40 Å RMSD and 20 Å hotspot distance not shown for visual clarity" (caption, p12), and the number of designs removed per panel is not given — so the worst-misplaced designs, which the text characterises as "RMSD > 20 Å" membrane-facing failures (p11), are partly cropped out of the panel that is supposed to show them. The 85.8% out-of-pocket figure for RFdiffusion3 on AT2 is quoted in the text from S7B Fig (not held) rather than being readable here | CC-BY 4.0, no ND (p1) |
| **9** | 13 | Reprediction of 90 selected designs with and without ProteinMPNN sequence redesign, DockQ against the designed peptide | violin (split) | `PLOT \| facet: generative design method (3: BindCraft, BoltzGen, RFdiffusion3) \| vary: validating prediction method (3: AF2IG, Boltz-2, RF3) \| series: sequence source (2: initial design sequence = clear half, one ProteinMPNN sequence = dotted half) \| measure: DockQ vs the initially designed peptide \| mark: split violin \| n: 1500 per half-violin (10 designs × 3 receptors × 50 seeds), 3000 per violin, 9000 per panel` | 3 stacked panels, vary by design method; 3 split violins each | **the three target receptors are pooled into every violin** although the paper's own Fig 8 shows strongly target-dependent behaviour (RFdiffusion3: 85.8% out-of-pocket on AT2 vs 15.02% on NOP, p11) — no per-receptor split is shown anywhere; **n per violin is not printed** on the figure; the measure is DockQ **against the designed peptide, not against any experimental structure** (stated in the caption but the axis is labelled simply "DockQ", identical to Figs 3/5/7 where it means DockQ-to-crystal — a reader comparing axes across figures will conflate two different quantities); the caption's cross-reference to "Fig 6" for hotspot distance should read Fig 8 | CC-BY 4.0, no ND (p1) |

**`reuse` in full, all figures.** p1: "Copyright: © 2026 Junker, Schoeder. This is an
open access article distributed under the terms of the **Creative Commons Attribution
License**, which permits unrestricted use, distribution, and reproduction in any medium,
provided the original author and source are credited." **CC-BY, no version number
printed on p1 (PLOS One's standard is CC-BY 4.0); NO ND clause**, so redrawing,
recolouring, cropping and adapting are all permitted with attribution. Each figure
carries its own DOI on its page (g001–g009), e.g. `10.1371/journal.pone.0355549.g006`
for the confidence figure (p9).

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent
- **schema_version**: v3
- **confidence**: **high** on sections A, B, D, E-Arm-1 and the confidence finding —
  the paper is clearly written, the Methods give tool versions and weight dates, and
  every headline number is in the main text or printed in a figure panel.
  **medium** on section F `n` values for Figs 3, 5, 6, 9 (per-mark n is arithmetic from
  113 × 50 and 10 × 3 × 50; the figures never print it) and on the Arm-2
  percentages that are quoted in the text from unheld supplementary figures (85.8% /
  15.02% out-of-pocket from S7B, the 0.25 sequence recovery from S8A).
  **What was hard to read:** the two-column PLOS layout puts figures mid-sentence and
  splits one key sentence across the p7/p9 page break (the ceiling-effect sentence),
  so quotes near page boundaries were reassembled from the `pagetext.sh` output and
  re-checked against 150-dpi renders. Figures 2, 3, 4, 5, 7 carry no plot-type
  information in their captions and were resolved by rendering pp. 5–10, 12–13.

- **unresolved**:
  1. **RECEPTOR CONFORMATIONAL STATE IS NEVER ASSESSED — asked for explicitly, and the
     answer is a clear negative.** The receptor is supplied as a fixed template or
     initial guess (p4: "the crystal structure of each of the 113 receptors was provided
     as a template to Boltz-2 and RF3"; p16: "For the receptor chain the respective
     reference structure was provided ('apo', i.e., peptide chain removed)"; p17:
     "Analogous to Boltz-2, the apo version of the reference dimer was provided as a
     prediction component") and is **never re-predicted, never varied and never
     scored**. Every metric in the paper — DockQ, iRMSD, fnat, LRMSD, Cα-RMSD, hotspot
     distance, clash count — measures the **peptide** relative to that frozen receptor.
     There is no active/inactive annotation, no TM6 or ionic-lock measure, no GPCRdb
     state label, and no state-stratified analysis anywhere in the 21 pages. The single
     mention of conformational state is a hypothetical in the Discussion, **p15**: "The
     fact that both prediction and generation methods are prone to reproducing
     previously seen complexes can negatively impact real drug design campains, where
     conformational selectivity might be crucial, i.e., when designing an antagonist for
     a receptor whose active structure-ligand complex has been memorized and thus
     resulting in inherently biased outputs." **The paper raises receptor-state bias as
     a consequence of memorization but never measures it.**
  2. **Text/figure disagreement on the inter-chain PAE correlations.** p7 states
     Spearman ρ = −0.829 (AF2IG), −0.894 (RF3) and "for Boltz-2 showed only a moderate
     correlation (ρ = −0.56)" for inter-chain PAE. The Fig 6 middle-row panels (p9)
     print **−0.84, −0.89 and −0.50** for the same quantity, and **−0.56 is the Boltz-2
     value in the top row (PAE peptide)**, which is also what p10 confirms ("inter-chain
     PAE from −0.50 to −0.27, and peptide PAE from −0.56 to −0.34"). The p7 sentence
     therefore appears to quote the wrong row for Boltz-2. **When citing, use the Fig 6
     panel values (−0.84 / −0.50 / −0.89) or quote both with the discrepancy noted.**
  3. **ETB complex count is inconsistent.** p3: "the Endothelin receptor type B (ETB)
     with **four** unique ETB-ligand complexes"; p10: "The Endothelin receptor type B
     (ETB) was present in the dataset a total of **five** times with different
     peptides". Only three are shown in Fig 7. S1 Table would settle it; not held.
  4. **Fig 5's caption colour key contradicts the figure** (caption p8: "blue: AF2IG,
     orange: Boltz2, green: RF3"; the plotted AF2IG marks and the in-figure legend are
     red/salmon). Verified by rendering p8.
  5. **Supplementary figure cross-references appear inconsistent.** S6 Fig is cited at
     p11 as "Input structures for peptide generation" (matching the p18 SI list) but
     also at p7 as the source of the peptide-pLDDT correlations and at p14 as the source
     of the distance-based PAE comparison — a role the p18 list assigns to S5 Fig.
     Likewise Fig 9's caption (p13) cross-references "Fig 6" for hotspot distance, which
     is Fig 8. Cannot be resolved without the SI.
  6. **The 91 / 22 GPCR-peptide vs GPCR-protein split appears only in the abstract
     (p1).** The Results (p3) give 113 dimers, the class A/B1 breakdown and the
     four-nanobody count, but never restate the 91/22 split; the ≤50-residue peptide vs
     >50-residue protein boundary is defined at p3 and p5 but no count is attached to it
     outside the abstract.
  7. **No p-value is reported for the "significantly better pre-cutoff" claim.**
     `scipy.stats.mannwhitneyu` is named in Methods (p18), but neither the main text
     (p5–p6, p14) nor the Fig 4 panels (p7) carry a test statistic, p-value or effect
     size for the pre/post-cutoff comparison. S3 Fig may; not held. The same applies to
     "significantly less effective (12.2% 'high quality')" at p13.
  8. **The confidence over-estimation is never quantified as a count or a false-positive
     rate.** The claim ("significant confidence overestimation for misplaced peptides",
     p1) is supported by (a) Spearman correlations, (b) the visual overlap of incorrect
     and correct predictions in Fig 6, and (c) the ETB case study. The paper never
     reports "k of n predictions were high-confidence-and-wrong", never states a
     confidence threshold at which an FPR could be computed, and never gives a
     precision/recall or AUROC for any confidence metric as a correct/incorrect
     classifier. **If we need a single quotable effect size, the strongest available are
     the Boltz-2 inter-chain-PAE ρ = −0.50/−0.56 (vs −0.84 and −0.89 for the other two
     predictors) and the AF2IG peptide-pLDDT ρ = 0.02.** The word "significant" in the
     abstract is used descriptively, not as a reported test result.
  9. **AF2IG's input is the full dimer, and the consequence is not characterised.**
     p4: "In case of AF2IG, the dimer of the receptor and its peptide was the input,
     where the coordinates of the receptor are used to initialize the prediction."
     p16 adds only that the peptide chain was reordered first. The paper does not state
     whether the reference peptide's coordinates are stripped, zeroed or ignored, and
     AF2IG's "initial guess" mechanism is not further described. This is the one place
     where the strength of route-1 leakage for AF2IG could not be pinned down from the
     PDF.
  10. **The Arm-2 reprediction cell size is n = 10 designs**, at the schema's
      `UNPOWERED` boundary (10 per method × receptor cell, 90 total; Fig 9 caption p13).
      The 1,500 predictions per half-violin come from 50 seeds on those 10 backbones and
      are not 1,500 independent designs. **I did not apply the `unpowered` tag**, because
      it is a paper-level tag and would mislabel the 113-complex validation arm; flagged
      here instead so a reverse lookup does not miss it.
  11. **No experimental validation of any kind is performed, and the authors never state
      this as a limitation.** Every number is in silico. The Discussion cites others'
      experimental-success meta-analyses (refs 50, 51, p14) but runs no assay, and the
      closest acknowledgement is the ProteinMPNN caveat at p15 ("not an immediate
      indicator for downstream experimental success"). Recorded so this is not mistaken
      for an author-stated limit.
  12. **Tags I needed and could not use (none invented):**
      - **A tag for "memorization was DETECTED"**, as opposed to designed against. The
        vocabulary has `anti-memorization` (a control exists) and `no-anti-memorization`
        (none exists), but nothing marks the *positive finding* that training-set
        memorization was measured and found — which is one of this paper's two headline
        results and is exactly what a reverse lookup would want. I tagged
        `anti-memorization` for the control; the finding itself is unfindable by tag.
      - **A Control tag for hotspot-residue conditioning.** The design arm's only
        directional handle is 4–6 hotspot residues per target (p11). None of
        `directed-state`, `partner-driven`, `ligand-driven`, `peptide-driven`,
        `g-protein-mimetic`, `nanobody`, `apo-sampling` or `seed-only` describes it. A
        `hotspot-driven` tag would.
      - **A Method tag for generative binder / de novo design** (RFdiffusion3,
        BindCraft, BoltzGen class). `benchmark-only` describes this paper's *role* but
        not the method class under test, so a reverse lookup for "which papers involve
        generative binder design" will not find it.
      - **A way to mark that a paper's two arms have opposite anti-memorization
        status.** Arm 1 has a cutoff control that was designed and run; Arm 2 has none.
        Tagging both `anti-memorization` and `no-anti-memorization` would be
        self-contradictory for reverse lookup, so I tagged only the former and recorded
        the asymmetry in `anti_memorization_control`.
  13. **v3 schema ambiguity — the panel-split rule does not cover a change in the *kind*
      of `vary`.** Fig 2A is a categorical bar chart of six dataset counts; Fig 2B is a
      histogram over a continuous peptide-length axis. Same `mark` (bar), same `measure`
      (count), same `facet` (none) — so the stated rule ("split when `mark` or `measure`
      differs; do not split when only `facet` differs") says do **not** split, yet the
      two have plainly different data shapes and would never be candidate designs for
      each other. **I split them into 2A and 2B.** Suggested fix: add "or when `vary`
      changes between categorical and continuous" to the split rule.
  14. **v3 schema ambiguity — `series` is often redundant with `vary`.** In Figs 3 and
      7B the colour dimension *is* the method already on the independent axis, so
      `series` either duplicates `vary` or must be written `none (1)` when a legend
      demonstrably exists. I wrote `series: prediction method (3, colour redundant with
      vary)`. A one-line rule for the redundant-encoding case would stop this drifting
      across extractors.
  15. **v3 schema ambiguity — `n_targets` and `n_predictions` have no per-arm form.**
      Both fields presuppose one experimental design per paper. This paper has two arms
      with n = 113 and n = 3, and a single value in either field would be a lie the
      index then propagates. I recorded both arms explicitly under each field, but a
      per-arm sub-structure (or an explicit instruction to use one) would be better.

- **why_it_matters**: *(left empty by the extractor per schema v3 — the user's call)*

---

## Tags

`gpcr` `benchmark-only` `cofolding` `templates-on` `single-state` `continuous-metric`
`saturating-metric` `oracle-leak` `design-level-oracle` `anti-memorization`
`confidence-as-discriminator` `multi-backbone` `seed-only` `orthosteric`
`peer-reviewed` `precedent` `contrast` `negative-result` `comparator-numbers`

Tag rationale, where a choice was made:

- **`gpcr`** — 72 unique receptors across classes A and B1; nothing non-GPCR is studied.
- **`benchmark-only`** — no new method, weights or loss; `method_class` is benchmark.
- **`cofolding`** — the three predictors under test (AF2IG, Boltz-2, RF3) all co-fold
  the peptide with the receptor in one pass; included so a co-folding reverse lookup
  finds this benchmark.
- **`templates-on`** — the deposited receptor is supplied as a template or initial
  guess for every prediction (p4, p16, p17). **NOT** `no-template-no-msa`: MSAs are off
  but templates are emphatically on, and the pairing is the paper's defining protocol.
  **NOT** `state-annotated-input`: the template is the deposited complex itself, with no
  state label attached (`oracle_leakage` route 2 is NONE FOUND).
- **`single-state`** — the receptor conformation is fixed input and never varies.
  **Deliberately NOT `ensemble`**, even though 50 seeds produce a spread: that spread is
  over *ligand poses on a frozen receptor*, and tagging it `ensemble` would false-
  positive every reverse lookup for conformational-ensemble methods. See
  `states_generated`.
- **`continuous-metric`** — DockQ, iRMSD, fnat, PAE, ipSAE, pLDDT and Spearman ρ are all
  continuous. **NOT `rmsd-only`**: the authors explicitly reject bare RMSD and argue for
  DockQ instead (p16). **NOT `visual-metric`**: no state or outcome is called by eye
  (the Arm-2 inside/outside-pocket call is backed by an OPM superposition and a contact
  analysis, p11). `binary-predicate` is arguably also earned by the four borrowed DockQ
  thresholds, but those are a *categorisation of a continuous score* rather than a
  predicate replacing one, so it is not applied.
- **`saturating-metric`** — the ceiling effect is named by the authors (p7→p9) and the
  AF2IG ipSAEmin floor and AF2IG DockQ floor (median 0.03) are visible in Fig 6 and
  reported at p5.
- **`oracle-leak`** — applied for **route 4**: AF2IG's weight set was chosen from five
  candidates by recovery **on this benchmark's own 113 dimers** (p16, S9 Fig), which is
  leakage under v3 even though no per-target value was picked; route 1 (deposited
  receptor as template) and route 5 (DockQ-to-reference as the success definition) are
  also present but are the declared benchmark protocol. See `oracle_leakage` for the
  route-by-route breakdown.
- **`design-level-oracle`** — applied for **route 7**, and kept distinct from
  `oracle-leak` per the v3 changelog: the design arm pins peptide length to the native,
  takes hotspots from the native complex, and scores success as similarity to the native
  peptide (p11, p3); the ETB case study peptides were chosen *because* they are known to
  be in training (p10).
- **`anti-memorization`** — a per-method training-cutoff split with homologous-redeposit
  crediting was both designed **and run and analysed** (p6–p7, Fig 4). Applies to Arm 1
  only; Arm 2 has none — see `unresolved` item 12.
- **`confidence-as-discriminator`** — the paper's central question, validated against
  DockQ over 16,950 predictions. This is the main reason the paper is in the corpus.
- **`multi-backbone`** — three predictors head to head (AF2IG, Boltz-2, RF3), plus three
  generative methods head to head, plus a full 3×3 orthogonal cross-validation (p13).
- **`seed-only`** — with the receptor template fixed and MSAs ablated, the seed (1–50)
  is the only remaining source of variation in the prediction arm, and the resulting
  variance is a headline finding (p6). No Control-vocabulary tag exists for the design
  arm's hotspot conditioning; see `unresolved` item 12.
- **`orthosteric`** — the orthosteric peptide-binding pocket is the entire subject
  (p2–p3, p11). **NOT `allosteric-site`, `cryptic-pocket` or `allosteric-failure`**:
  no allosteric site is targeted or sampled anywhere.
- **`peer-reviewed`** — PLOS One 21(8):e0355549, published 27 Aug 2026, with a published
  peer review history (p1). **NOT `preprint`.**
- **`precedent`** + **`contrast`** + **`negative-result`** — precedent on the confidence
  and memorization findings; contrast on scope (state never assessed, MSAs ablated,
  design arm n = 3) and on the route-4/route-7 oracle use; `negative-result` because the
  paper's headline is a failure of the confidence metrics rather than a positive
  capability. Stance is **provisional**, per schema.
- **`comparator-numbers`** — ~60 quotable numbers in section E across two arms, with n
  and pages attached, including three predictors' median DockQ, four confidence
  metrics' Spearman ρ, and a pre/post-cutoff memorization table.
- **NOT `figure-exemplar`** — that tag is for papers kept mainly for their figures and
  excluded from gap analysis; this paper is squarely in our field and must be *inside*
  gap analysis. (Fig 6 p9 is nonetheless the single best confidence-vs-accuracy figure
  design in the corpus for our purposes, and CC-BY with no ND clause permits redrawing.)
- **NOT `experimental-validation`, NOT `experimental`, NOT `prospective`,
  NOT `msa-subsample`, NOT `msa-state-filter`, NOT `template-state-bias`,
  NOT `af-cluster`, NOT `latent-steering`, NOT `md`, NOT `md-emulator`,
  NOT `enhanced-sampling`, NOT `unpowered`** — none applies; see the fields above for
  the reasoning on each, and `unresolved` item 10 on `unpowered`.
