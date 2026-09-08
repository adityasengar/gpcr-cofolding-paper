# ferguson2026deorphann

Schema v3 extraction. Every field present; `NOT REPORTED` where the paper does not say.

**Which version was read.** The held PDF is the **bioRxiv preprint**, doi
`10.1101/2025.03.19.644234`, "this version posted March 20, 2025", 36 pages. `refs.bib`
and `MANIFEST.csv` record a **journal version, *Molecular Cell* 2026, doi
`10.1016/j.molcel.2026.07.006`, which is NOT held and was NOT read.** Every page number,
quote and number below is from the preprint. Between a March-2025 preprint and a 2026
*Molecular Cell* paper there is a full review cycle; numbers, panel letters and figure
counts may have moved. See `unresolved`.

**Page numbers are PDF page numbers from `./pagetext.sh` markers (1–36), and the PDF page
equals the printed page throughout** (PDF p18 prints "18"). Layout: title p1, abstract +
significance p2, introduction p2–4, results p4–10, discussion p10–12, methods p12–16,
resource availability p16, acknowledgements/contributions p17, Figures 1–6 p18–26,
Table 1 p26, Supplemental Figures 1–2 p27–28, references p28–36.

**SI status: split.** Supplemental **Figures** 1 and 2 are bound into this PDF (p27–28)
with full captions and are read here. Supplemental **Data** 1 and 2 (all GPCR and peptide
sequences, the agonist pair lists for training and validation sets) are named on p27 but
are **separate files not held**. See `si_in_scope`.

**Text-layer note:** the body text layer is clean. Mathematical notation is mangled
(`ℝ{" × %&'}` on p6 is `ℝ^{n × 128}`; the AP formula on p14 is unreadable in text) —
dimensions were recovered from the p21 render of Figure 3A, which prints them correctly.
Axis labels, legends, AUC values in panel legends, marks and axis breaks are **not** in
the text layer and were read from 110 dpi renders of pages 18, 20, 21, 23, 25, 27 and 28.

---

## A. Identity

- **citekey**: `ferguson2026deorphann`
- **doi**: **dual, and the two must not be conflated.**
  - Held PDF: **bioRxiv `10.1101/2025.03.19.644234`** — p1 header, repeated on every
    page: "bioRxiv preprint doi: https://doi.org/10.1101/2025.03.19.644234; this version
    posted March 20, 2025."
  - Journal of record per `refs.bib` / `MANIFEST.csv`: **`10.1016/j.molcel.2026.07.006`**
    (*Molecular Cell*, 2026). This DOI appears **nowhere in the held PDF** and the journal
    version was not read.
- **year**: **2025 for the read preprint** (p1: "this version posted March 20, 2025");
  **2026 for the journal version** recorded in `refs.bib`. The citekey says 2026; the
  content in this note is 2025 preprint content.
- **venue**: **bioRxiv preprint, not peer reviewed.** p1, on every page: "(which was not
  certified by peer review) is the author/funder, who has granted bioRxiv a license to
  display the preprint in perpetuity." Journal version is *Molecular Cell* 2026 per
  `refs.bib`, not held. p1 also carries an author-supplied classification line
  ("Biological Sciences—Biophysics and Computational Biology") and a
  Significance Statement (p2), i.e. it was formatted for PNAS submission at the time of
  posting, yet published in *Molecular Cell*. Tagged **`preprint`**, not `peer-reviewed`.
- **title**: "DeorphaNN: Virtual screening of GPCR peptide agonists using
  AlphaFold-predicted active state complexes and deep learning embeddings" — p1.
- **authors**: Larissa Ferguson (corresponding; MRC Laboratory of Molecular Biology,
  Cambridge), Sébastien Ouellet (independent researcher, Ottawa), Elke Vandewyer (KU
  Leuven), Christopher Wang, Zaw Wunna, Tony K.Y. Lim (Univ. Cambridge Pharmacology),
  William R. Schafer and Isabel Beets (§ senior authors, equal contribution) — p1.
  **Relevant to the dataset's provenance:** senior author Isabel Beets is first author of
  ref 9 (Beets et al., *Cell Rep.* 2023, "System-wide mapping of peptide-GPCR interactions
  in *C. elegans*"), which is the source of both the training dataset and the ground-truth
  agonist labels, and also the source of the already-known agonists for NPR-34 and SEB-2
  in Table 1 (p26, "Source: Beets et al.9"). The training labels and the paper are from
  the same lab.
- **Code and data**: p16 — code at `https://github.com/Zebreu/DeorphaNN`; datasets at
  `https://huggingface.co/datasets/lariferg/DeorphaNN`.

## B. Scope

- **system**: **GPCR, exclusively — peptide-activated GPCRs, screened against peptide
  agonists.** p2: "G protein-coupled receptors (GPCRs) are important cell surface
  receptors..." No non-GPCR system appears anywhere. The task is **functional
  classification (agonist vs non-agonist), not structural accuracy**: no experimental
  structure is used as a reference at any point in the paper.

- **Organism — this is the load-bearing scope limit and must not be glossed.**
  - **Training and primary evaluation: *Caenorhabditis elegans*.** p4: "our final dataset
    contained 65 GPCRs from 55 genes and 339 unique peptides derived from 93 genes."
    p11: "Despite being trained on a relatively small dataset of 457 GPCR-agonist pairs
    from *C. elegans*, DeorphaNN's predictions generalize across species."
  - **Cross-species evaluation 1: *Platynereis dumerilii*** (marine annelid). p9: "we
    evaluated its performance on a dataset from the bilaterian marine annelid,
    *Platynereis dumerilii*."
  - **Cross-species evaluation 2: human.** p13: "we utilized a previously published list
    of GPCR-peptide agonist interactions compiled across diverse species... We limited our
    analysis to agonist interactions involving human GPCRs, while using peptides from all
    species (excluding those longer than 50 residues) to augment the dataset with
    **synthetic** non-agonist interactions."
  - **Every experimental validation is in *C. elegans*.** The two deorphanized receptors
    (H23L24.4, NPR-33) and all EC₅₀ values are *C. elegans* (p10, Fig 6, p26). **No human
    receptor is tested in the lab in this paper.** The human arm is entirely
    retrospective and its negatives are **synthetic**, generated by ESM-2 dissimilarity
    (p9, p13) — so the human mAP of 0.72 is measured against non-agonists that were never
    experimentally shown to be non-agonists. Generalisation to human receptors is
    therefore supported by a ranking benchmark with fabricated negatives, not by any human
    assay.

- **n_targets**: **counts differ between the results text and the methods; do not collapse
  them.**
  - *C. elegans* training set: **65 GPCRs from 55 genes**, 339 unique peptides from 93
    genes (p4 and p12–13). Derived from a screen of 161 putative peptide-activated GPCRs
    (p4).
  - *Platynereis*: **results text p9 says "17 GPCRs and 124 peptides"; methods p13 says
    "resulting in 18 receptors and 23 agonist interactions"** and "resulting in 122
    peptides." The two are inconsistent; see `unresolved`.
  - Human: **82 human GPCRs**, "345 agonist and 3370 non-agonist GPCR-peptide pairs
    across 82 human GPCRs" (p13).
  - Prospective screen: **4 receptors** (NPR-34, SEB-2 — already deorphanized elsewhere;
    H23L24.4, NPR-33 — genuinely orphan), ranked against 364 candidate peptides (p10,
    Table 1 p26).
  - **Generality claim from one nematode dataset:** the paper trains on 65 *C. elegans*
    receptors and claims species generalisation (p11, p12). The claim is tested on
    ranking benchmarks, not on new wet-lab work outside *C. elegans*.

- **method_class**: **co-folding + template-biasing + a downstream supervised classifier.
  Genuinely three things:**
  1. **co-folding** — AF-Multimer folds GPCR sequence and peptide sequence together into a
     complex (p13: "Primary amino acid sequences for each GPCR-peptide complex were input
     together into AF-Multimer26,31 using local ColabFold75").
  2. **template-biasing, state-annotated** — AF-Multistate-derived active-state receptor
     models are trimmed and supplied as templates (p13; see `oracle_leakage` route 1).
  3. **supervised learning on AF internals** — random forest on pooled single/pair
     representations (p14), then a GATv2 graph neural network (DeorphaNN) on graphs whose
     nodes/edges carry pair-representation embeddings and Arpeggio interaction edges
     (p14–15).
  Not `benchmark-only`; not MD; no MSA subsampling in this paper's own pipeline (the
  restricted-MSA step is inside the cited AF-Multistate protocol, see `msa_handling`).

- **backbones**: **AF2 / AF-Multimer only, via local ColabFold.** p13: "input together
  into AF-Multimer26,31 using local ColabFold75 on a high-performance computing cluster.
  All modelling settings were left at default, resulting in the generation of 5 predicted
  structures, corresponding confidence metrics, and hidden layer protein representations
  (single and pair)." **AF-Multistate (Heo & Feig 2022, ref 34) is an AF2-based protocol,
  not a separate backbone.** No AF3, Boltz, Chai, OF3 or Protenix run anywhere. AF3 is
  mentioned only as future work (p12: "with the recent open-source release of
  AlphaFold372, these limitations may be addressed in future work"). Two other neural
  models appear but are **not structure backbones**: ESM-2-150M (peptide embeddings, used
  only to fabricate human non-agonists, p13) and SpatialPPIv2 (a protein-protein
  interaction predictor used as a comparator, p9). **`multi-backbone` is NOT applicable** —
  exactly one structure backbone.

- **templates**: **dual, and the contrast between the two arms is the paper's Figure 2
  result.**
  - **OFF** for the baseline arm — ColabFold "All modelling settings were left at default"
    (p13); the paper consistently calls this arm "No Template" (Fig 2B, 2D, 2E captions,
    p20).
  - **ON and state-annotated** for the main arm — one **GPCR-specific, AF-predicted,
    trimmed active-state template per receptor** (p13). **These templates are AlphaFold
    predictions of the target sequence itself, not deposited PDB coordinates.** That is
    the crucial distinction for `oracle_leakage` route 1.
  - Recorded as: `off (baseline arm) + on, state-annotated, AF-predicted per-receptor
    (main arm)`.

- **msa_handling**: **dual — and the two levels are different operations, exactly the
  distinction SCHEMA.md warns against collapsing.**
  - **AF-Multimer complex prediction step: FULL MSA, explicitly and deliberately.** p14:
    "MSA reduction was not necessary as the templates were derived from the same sequence
    as the target GPCRs76, and retaining the full MSA preserves coevolutionary signals
    that are vital for driving accurate inter-protein contact predictions77."
  - **AF-Multistate template-generation step: state-filtered / restricted MSA**, inherited
    from ref 34 and not implemented here. p13: "we generated active state GPCR templates
    using AF2-Multistate34. **This approach leverages state-annotated GPCR databases to
    guide predictions with a restricted MSA protocol.**"
  - So: `full (AF-Multimer step, explicitly retained) + state-filtered (upstream
    AF-Multistate template-generation step, via ref 34)`. **Not subsampled** — depth is
    never reduced in this paper's own step, and the paper says so.

## C. Conformational core

**Framing note that governs this whole section.** This is a *ligand-classification* paper
that uses a conformational trick as a feature engineering step. It never measures a
conformation. There is no RMSD, no TM-score, no activation coordinate, no comparison to
any deposited structure anywhere in the 36 pages. The "active state" is **asserted by
construction** (it came out of AF-Multistate, therefore it is called active) and validated
only **indirectly and functionally** — by whether it improves agonist ranking. Several
fields below are therefore `NOT REPORTED` not through sloppiness but because the paper's
success criterion is a wet-lab agonist label, not a structure.

- **states_generated**: **`two (as two pipeline arms) + single-state (per run)`.**
  - Per pipeline run: **one** receptor conformation. Five AF models are produced per
    complex (p13) but all five are seeded by the same template; they are treated as
    replicates, not as states — one is selected by confidence for structural analysis and
    all five are **averaged** for representation analysis (p13: "we averaged
    representations across all five AF-Multimer models to prevent learning artefacts from
    individual model variations").
  - Across the paper: **two** conformational variants exist per receptor, because every
    one of the 22 035 complexes is modelled twice — once with no template and once with an
    active-state template — and the two are compared head to head (Fig 2B–2F, p20).
  - **But the no-template arm is never shown to be inactive.** p6 asserts it from the
    literature only: "AF2 is inherently biased towards modelling GPCRs in an inactive
    conformation34, likely due to having been exposed to predominantly inactive-state GPCR
    structures during training." No state predicate is applied to either arm. So "two" is
    a statement about pipeline arms, not a verified two-state result.
  - No ensemble, no continuum, no sampling over states.

- **structural_priors_used**: **substantial, and none of it is a defect — this is design-
  time structural knowledge, recorded here rather than in `oracle_leakage`.**
  1. **Where peptide agonists bind, from solved complexes.** p4–5: "As experimentally
     determined structures show that peptide agonists typically interact with the helical
     cavity ('binding pocket') and extracellular loops of GPCRs35, we hypothesized that
     AF-Multimer would predominantly model agonist peptides within the GPCR binding
     pocket." This prior defines the "binding pocket" region that every subsequent feature
     (pocket PAE, pocket subregion, interaction subregion) is built on.
  2. **The class A activation mechanism, from solved active/inactive pairs.** p10: "Agonist
     binding to GPCRs induces conformational changes that drive conserved transmembrane
     (TM) rearrangements, a hallmark of receptor activation38,52,53. A key feature of this
     process is the outward movement of TM654, facilitated by kinking at conserved motifs
     and disruption of ionic interactions between TM3 and TM6/755–57." This is the stated
     rationale for the whole active-state template design and for which template regions
     to keep: p6, "Second, we preserved the transmembrane helices, as shifts to an
     active-state conformation are driven by displacement of the transmembrane
     helices38–40."
  3. **Toggle-switch / anchor-driver interaction theory** shaping the graph design. p11:
     "Agonists activate GPCRs through interactions with key 'toggle switch' residues in the
     GPCR binding pocket61,62. Triggering these toggle switches is thought to require two
     distinct types of intermolecular interactions: 'anchor' interactions that provide
     stability for ligand binding, and 'driver' interactions that directly engage with
     toggle switches to induce conformational changes63–65. To enable DeorphaNN to learn
     patterns corresponding to these interactions, we engineered DeorphaNN to utilize
     Arpeggio-defined edges..."
  4. **AF2's own pretraining on the PDB**, acknowledged as the transfer source. p11:
     "DeorphaNN leverages the AF2 algorithm, which was pretrained on approximately 170 000
     protein structures from diverse species26, and adapts it for the specialized task of
     GPCR-peptide agonism prediction."
  5. **The state annotations behind AF-Multistate** (p13) — a prior on what "active" means,
     derived from deposited structures of *other* (mostly mammalian) GPCRs. This is also
     `oracle_leakage` route 2; it is recorded in both places because it is simultaneously a
     legitimate design prior and a route by which deposited-structure state knowledge
     enters the pipeline.
  6. **NOT used as a prior:** no deposited structure of any *C. elegans* GPCR (none exist,
     and the paper never mentions one); no sequence–structure alignment to a solved
     homologue; no docking to a crystal pocket. The binding-pocket definition is derived
     from a **sequence-based topology predictor**, not a structure: p5, "we defined a
     putative GPCR binding pocket as residues within ±5 positions from the
     DeepTMHMM36-predicted extracellular-membrane boundary."

- **oracle_leakage**: **all seven routes enumerated separately. Headline: route 2 fires
  (state-annotated databases, inherited via AF-Multistate); route 4 fires weakly
  (empirically chosen thresholds, one of them fixed on the evaluation set); route 7 fires
  at design level. Routes 3, 5 and 6 are genuinely clean, and routes 5 and 6 are clean in
  an unusually strong way — there is no held structural reference in this paper at all.**

  **Route 1 — deposited structures used as input or template.** **PARTIAL, and the precise
  answer is: templates yes, deposited templates no.**
  - The full protocol, quoted whole from p13 because this is the sentence the caller needs:
    > "To bias AF-Multimer predictions towards GPCR active-state conformations, we
    > generated active state GPCR templates using AF2-Multistate34. This approach leverages
    > state-annotated GPCR databases to guide predictions with a restricted MSA protocol.
    > The top ranked active state structures were processed by trimming intracellular
    > residues with pLDDT values below 70 and all extracellular residues, based on
    > DeepTMHMM36 annotations. These processed structures served as GPCR-specific templates
    > in subsequent AF-Multimer predictions for each GPCR-peptide pair, generating
    > state-biased predictions." — **p13**
  - The design rationale, from the results text, p6:
    > "To model active-state GPCR-peptide complexes, we generated GPCR-specific templates
    > using AF-Multistate34 and refined them through targeted adjustments (Figure 2A).
    > First, we trimmed extracellular regions from the template, as these domains mediate
    > ligand binding. This allows AF-Multimer to model peptide interactions without
    > interference from pre-defined extracellular structures. Second, we preserved the
    > transmembrane helices, as shifts to an active-state conformation are driven by
    > displacement of the transmembrane helices38–40. Third, we removed low-confidence
    > residues in the intracellular domain (involved in G-protein interactions), preventing
    > inaccuracies in the template from distorting AF-Multimer's predictions of active state
    > GPCR-peptide complexes." — **p6**
  - Caption confirming the same, p20 (Figure 2A): "Predicted active-state structures were
    generated for each GPCR using AF-Multistate. After trimming extracellular regions and
    low confidence (pLDDT < 70) intracellular regions, these templates were then used in
    AF-Multimer to model GPCR-peptide complexes."
  - **What this means concretely.** The template fed to AF-Multimer is an **AlphaFold
    prediction of the target receptor's own sequence**, produced by AF-Multistate and then
    trimmed to the TM bundle. **No PDB coordinate file enters the pipeline directly.** The
    targets are *C. elegans* GPCRs, for which no experimental structure exists, so no
    structure of the target state could have been used even in principle. The baseline arm
    runs ColabFold at "default" settings (p13), which is the no-template arm the paper
    itself labels "No Template" (Fig 2B/2D/2E, p20).
  - **Verdict: no deposited coordinates as input. The route is nonetheless "on" in the
    weaker sense that a state-biased template is used at all — and where that template's
    "activeness" comes from is route 2.**

  **Route 2 — state annotations from a curated database driving templates or alignments.**
  **PRESENT. This is the central leakage route in the paper, and it is inherited rather
  than implemented.**
  - Verbatim, p13: **"This approach leverages state-annotated GPCR databases to guide
    predictions with a restricted MSA protocol."**
  - The one sentence quoted above is the **entirety** of what the paper says about how the
    active state is obtained. It does **not name the database** (GPCRdb, PDB-derived, or
    other), does **not** say what the state annotation is, does **not** give the size or
    composition of the annotated set, does **not** say how the restricted MSA is
    constructed, and does **not** state whether any *C. elegans* sequence appears in the
    annotated set. All of that is delegated to ref 34 (Heo, L. & Feig, M. "Multi-state
    modeling of G-protein coupled receptors at experimental accuracy." *Proteins* 90,
    1873–1885, 2022 — full citation on p32). **Marked `NOT REPORTED` at the level of this
    paper; resolvable only from ref 34, which is separately held in this corpus as
    `notes/heo2022multistate.md` and was deliberately not consulted for this extraction.**
  - **Why this matters and why it is milder than target-level leakage.** The state
    annotations describe deposited structures of *other* GPCRs — the C. elegans targets
    have no deposited structures. So the pipeline transfers a *general* notion of the
    active conformation into a receptor family where the answer is unknown, rather than
    reading the answer for the target off a database. It is nonetheless a route by which
    knowledge derived from deposited active-state structures enters every single prediction
    in the paper, and every result after Figure 2 depends on it: p6, "Therefore, we used
    active-state templates to generate GPCR-peptide complexes for all subsequent analyses."
  - The receiving step is confirmed template-driven and MSA-full: p14, "MSA reduction was
    not necessary as the templates were derived from the same sequence as the target
    GPCRs76."

  **Route 3 — cluster labels derived from known states.** **NONE FOUND.** No clustering of
  any kind is performed. The protocol is fully described on p13–16 (AlphaFold, mAP,
  Supervised learning algorithms, Arpeggio, Graph construction, Model architecture and
  training) and contains no clustering step, no AF-Cluster, no MSA clustering, no
  conformational clustering. Cross-validation *groups* exist but they are **gene- and
  family-based, not state-based**: p14, "Grouping by GPCR was performed to minimize leakage
  of receptor-specific information between folds. Isoforms from the same GPCR gene were
  treated as a single unit, ensuring they appear together (55 unique GPCR genes)."

  **Route 4 — hyperparameters, sweep ranges, seeds or stopping criteria tuned against known
  states.** **PARTIAL — no tuning against any *conformational* ground truth (there is
  none), but several thresholds are fixed empirically, and at least one is fixed directly
  on an evaluation set.**
  - **The clearest instance, and it is on the human evaluation set**, p9: "we selected
    peptides with a distance exceeding **an empirical threshold—chosen to ensure at least 3
    non-agonists per GPCR**." Methods give the value, p13: "identified, for each GPCR,
    peptides with Euclidean distances **> 3.9** from known agonists, ensuring at least 3
    putative non-agonists per GPCR." The 3.9 cut is chosen against the very human dataset
    on which the headline mAP of 0.72 (Fig 5C, p25) is then reported, and it is chosen with
    reference to the **known agonists** of each receptor. This constructs the negative class
    of the benchmark using the answer key. By SCHEMA.md's route-4 clause — tuning a range on
    the evaluation set is leakage even when no per-target value is picked — this fires.
  - Other thresholds stated without derivation or justification (`NOT REPORTED` how each
    was chosen): binding-pocket definition "±5 positions" (p5); peptide-in-pocket cutoff
    "12.5 Å" (p5, repeated p14); template trimming at "pLDDT values below 70" (p13);
    distance-edge ablation at "residues ≤6 Å apart" (p8) / "< 6 Å" (p14); positive:negative
    subsampling "a balanced training set with a 1:4 ratio" (p16); "Training was performed
    for 30 epochs" (p16); GNN hyperparameters — "10 attention heads, a dropout rate of 0.5,
    and 64 hidden channels", "learning rate of 0.0005" (p15) — given as fixed values with
    no sweep reported.
  - **Model selection is on validation ranking, not on structure:** p16, "The final model
    for each fold was chosen based on the highest validation average precision score
    achieved during training." Random forests are explicitly untuned: p14, "We implemented
    random forest classifiers using scikit-learn79 with **default hyperparameters**."
  - **Seeds:** p14, "To maintain consistency across all cross-validation splits, we used
    identical random seed and data partitions." One fixed seed; no seed sweep, so no
    seed-level leakage.

  **Route 5 — success defined post hoc by RMSD or TM to a structure they had.**
  **NONE FOUND, and emphatically so.** Success in this paper is **a wet-lab functional
  label**, defined before any modelling: p4, "Combining each GPCR with each peptide
  ('GPCR-peptide complex') yielded 20 035 combinations, all of which were **experimentally
  confirmed** to be either agonist or non-agonist matches9." The ranking metric is defined
  purely over those labels: p14, "where 𝑟𝑒𝑙@𝑘 equals 1 if the 𝑘-th ranked peptide is
  relevant (i.e. an agonist) and 0 otherwise." **The words RMSD, TM-score, lDDT-to-
  reference and "experimentally determined structure of this receptor" do not appear as a
  success criterion anywhere in the paper.** The only structural predicate is a
  self-referential geometric one — is the peptide within 12.5 Å of the predicted pocket
  (p5) — and the paper reports that predicate **fails** to discriminate (p5).

  **Route 6 — best/worst model labels assigned against a held reference.**
  **NONE FOUND. Model selection among the five AF models is by self-confidence only.**
  p13: "For confidence metric analyses, we utilized the model with the highest ipTM,
  highest peptide pLDDT, or lowest pocket PAE, depending on the metric being analysed. To
  determine whether the peptide was modelled within the binding pocket, we carried out
  analysis on the predicted structure with the highest peptide pLDDT." p14 (Arpeggio):
  "The top-ranked GPCR-peptide structure according to peptide pLDDT was examined." The
  AF-Multistate step likewise: "The top ranked active state structures were processed"
  (p13) — top-ranked by the AF-Multistate protocol's own criterion, not by a reference.
  For the representation analyses no selection at all is made: p13, "For all protein
  representation analyses, we averaged representations across all five AF-Multimer models."
  **Note the mild circularity that is present instead:** selecting the model by peptide
  pLDDT and then reporting peptide pLDDT as a discriminator (Fig 1F) means the reported
  discriminator is a max-over-5 statistic, not a random draw. The paper does not flag this.

  **Route 7 — design-level oracle: input conditions or systems chosen because the expected
  answer is already known.** **PRESENT, in three distinguishable forms. All are design-
  level and weaker than pipeline leakage; none contaminates the model's inputs.**
  1. **The receptor set is conditioned on the answer existing.** p4: "We only included
     GPCRs that showed concentration-dependent activation by at least one peptide, as a
     lack of activity could have been due to factors such as non-functional expression,
     misfolding, or failure to couple with Gα16, rather than the absence of a true
     agonist." Restated p12–13: "we excluded GPCRs lacking concentration-dependent agonist
     responses in the screening data." Every receptor scored is one known in advance to
     have at least one agonist in the peptide list — which is exactly the condition under
     which AP is well defined and non-trivially achievable. Same for the validation sets:
     p13, "We omitted GPCRs that had no confirmed agonists among the included peptides."
  2. **Two of the four "deorphanization" receptors already had published agonists when
     DeorphaNN was run on them.** p10: "we first applied the model to newly deorphanized
     receptors, NPR-34 and SEB-2. Neither GPCR was found to have agonist-induced activity
     with any of the peptides in the training dataset, but **subsequent experiments
     demonstrated that both receptors respond to peptides recently identified through
     phylogenetic approaches9**. As shown in Table 1, the confirmed agonists for these
     GPCRs are ranked first out of 364 candidates." Table 1 (p26) marks their Source as
     "Beets et al.9", i.e. the same lab's prior paper, not this one. **These two 1/364
     ranks are retrospective, and the note's `metrics_reported` records them as such.**
  3. **The expected conformation is declared before the result is read.** p6: "Therefore,
     we hypothesized that biasing the GPCR in each GPCR-peptide complex toward an active
     conformation would preferentially improve the confidence of AF-Multimer predictions
     for agonists." The active state is chosen as the target state on mechanistic grounds
     (p10) and never independently confirmed in any prediction.
  - **Not route 7:** H23L24.4 and NPR-33 (p10). Both were orphans with no known ligands,
    predictions were made, and the top-ranked candidates were then tested in the lab. That
    arm is genuinely prospective.

- **prospective**: **partial — and the split is clean and worth quoting in a manuscript.**
  - **Prospective:** two orphan receptors, predicted then tested. p10: "We then applied
    DeorphaNN to two orphan *C. elegans* GPCRs with no known ligands, H23L24.4 and NPR-33.
    The highest-ranked candidate agonists for these receptors were experimentally tested
    using a CHO Gα16-mediated calcium signalling assay." Three peptide predictions were
    tested (NLP-69-1 rank 5/364; NLP-70-2 rank 1/364; NLP-70-1 rank 156/364, tested as a
    same-gene-family follow-up), and all three activated their receptor (Fig 6, p26).
  - **Retrospective:** everything else. All mAP numbers (Figs 1, 2, 3, 4, 5) are computed
    over a pre-existing, fully labelled screen. NPR-34 and SEB-2 had known answers
    (route 7 above). The *Platynereis* and human arms are re-ranking of published data,
    with the human negatives fabricated.
  - **Retrospective in the biasing pipeline too:** the active-state template step imports
    state knowledge from an existing annotated database into every prediction, including
    the prospective ones (p13).

- **state_metric**: **`binary predicate + NONE FOR CONFORMATION`. Both halves matter.**
  - **The one operationalised structural predicate is about the ligand, not the state:**
    peptide inside vs outside the pocket. p5: "We then computed the minimum
    peptide-to-pocket residue distance (using a **12.5 Å cutoff**) to classify peptides as
    being 'inside' or 'outside' the GPCR binding pocket." The 12.5 Å value is stated but
    **its justification is `NOT REPORTED`**. The ±5-residue pocket definition (p5) is
    likewise unjustified. This predicate is applied again as a filter before Arpeggio, p14:
    "Peptides located more than 12.5 Å from the binding pocket were excluded from further
    analysis."
  - **There is no metric of receptor conformational state anywhere in the paper.** No RMSD,
    no TM-score, no TM3–TM6 distance, no activation index, no comparison of a template-arm
    model to a no-template-arm model in Å, and no comparison to any deposited structure. A
    model is "active state" because it came from an active-state template. The claim in the
    title — "AlphaFold-predicted active state complexes" — is never tested structurally.
  - **What is used in its place is a functional proxy:** ranking metrics (AP/mAP,
    ROC-AUC, PR-AUC) against wet-lab agonist labels, plus peptide pLDDT deltas (Fig 2F).
  - **`visual only` is NOT applied.** Figures 2B–2C show side-by-side renders of one agonist
    and one non-agonist complex with and without a template, but the caption ties the claim
    to pLDDT ("The use of an active-state template improved peptide pLDDT", p20), not to
    visual state assignment. No state is called by eye either.

- **metric_saturation**: **yes, in two places, both numeric.**
  1. **The pocket-occupancy feature ceilings, and the paper says so.** Figure 1E caption,
     p18–19: "99.8% of agonists are modelled within the GPCR binding pocket, compared to
     96.6% of non-agonists." p5: "only one agonist peptide was modelled outside of the
     binding pocket of its respective GPCR, while approximately 3.4% of non-agonist
     peptides were modelled outside the binding pocket." The paper draws the correct
     conclusion, p5: "Due to the prevalence of peptides positioned in the binding pocket
     irrespective of ligand class, this feature alone does not provide a reliable basis for
     distinguishing between agonist and non-agonist GPCR-peptide complexes." **This is a
     genuine ceiling — with 99.8% vs 96.6% there is almost no dynamic range left.**
  2. **AP ceilings at 1.0 with visible pile-up on the human benchmark.** AP is bounded
     [0,1]; the Figure 5C render (p25) shows a dense stack of DeorphaNN points against the
     right-hand edge at AP = 1.0, consistent with the reported mAP of 0.72 against a random
     baseline of 0.30. Many human receptors in that benchmark have very few agonists among
     mostly synthetic non-agonists, so AP = 1.0 is easily reached.
  - **Bounded-but-not-saturating:** pLDDT (0–100), ipTM (0–1). PAE is hard-capped and the
    paper states the cap, p5: "output as a 2D array with values ranging from 0 Å (low
    positional error) to **a cap at 31.75 Å** (high positional error)." No pile-up at the
    PAE cap is reported.
  - **Axis truncations and breaks are NOT recorded here** — per v3 they are figure defects
    and are recorded in `hides` on rows 1B, 1E, 2F, 4D, S1A, S2B.

- **directional_control**: **YES — the method can be instructed which state to produce, and
  the handle is named and swappable.**
  - **Primary handle: a state-annotated, AF-predicted, trimmed template.** p13: "To bias
    AF-Multimer predictions towards GPCR active-state conformations, we generated active
    state GPCR templates using AF2-Multistate34... These processed structures served as
    GPCR-specific templates in subsequent AF-Multimer predictions for each GPCR-peptide
    pair, **generating state-biased predictions**." The direction is set by which
    AF-Multistate state is requested; the paper only ever requests **active**. **The
    inactive direction is never run** — the comparison arm is "no template", not "inactive
    template". That is a real gap: it means the improvement in Figure 2D could in principle
    come from *any* trimmed TM-bundle template, not specifically from an active one. The
    paper does not run that control. See `controls_run`.
  - **Secondary handle: the co-folded peptide partner.** Every prediction is a
    GPCR + peptide complex (p13), and the peptide is the ligand whose agonism is at issue.
  - **Trimming is part of the handle:** extracellular regions removed so the peptide can be
    placed freely, TM helices kept, low-confidence ICL residues removed (p6, p13).
  - **Not handles here:** seeds (one fixed seed, p14), MSA depth (explicitly not reduced,
    p14), G protein or nanobody (never co-folded — the intracellular G-protein-facing
    region is *deleted* from the template, p6).

- **anti_memorization_design**: **held-out sets exist, three kinds, none of them date-based.**
  1. **Grouped cross-validation, held out by receptor gene and by family.** p14:
     "we employed stratified group 10-fold cross-validation. Grouping by GPCR was performed
     to minimize leakage of receptor-specific information between folds. Isoforms from the
     same GPCR gene were treated as a single unit, ensuring they appear together (55 unique
     GPCR genes)... For Figures 3D and 3E, we employed leave-one-group-out
     cross-validation." p16: "the dataset was divided into groups based on GPCR families,
     and multiple random splits were generated... This method ensures that the model is
     evaluated on **previously unseen GPCR families**." n = 55 gene groups / 11
     shuffle-groups-out splits (p8).
  2. **Cross-species held-out sets.** *Platynereis* (17 or 18 GPCRs; see `n_targets`) and
     human (82 GPCRs, 345 agonist + 3370 synthetic non-agonist pairs, p13). Both are
     entirely disjoint from the *C. elegans* training data.
  3. **Held-out peptides: 25 peptides discovered after the training screen.** p10: "ranked
     first out of 364 candidates (339 peptides from the training dataset **plus 25 recently
     identified peptides** [Supplemental Data 1])" and p10: "Peptidomics and comparative
     genomics studies have since expanded the number of peptides known in *C. elegans*
     beyond those included in the training dataset45–47."
  - **NO date/cutoff design of any kind.** The paper never states AF2's training cutoff,
    never asks whether any receptor or complex could have been memorised, and never
    partitions anything by deposition date. The words "training cutoff", "memorization" and
    "post-cutoff" do not appear. `NOT REPORTED`. Note the mitigating fact the paper never
    makes: *C. elegans* GPCRs have essentially no deposited structures, so structural
    memorisation of the targets is implausible — but the paper does not say this, does not
    test it, and it does not cover the human arm, where the 82 receptors include many with
    deposited active-state structures inside AF2's training set.

- **anti_memorization_control**: **PARTIALLY RUN — the generalisation arms were run and
  analysed as arms; the memorization question was never posed.**
  - **Run and analysed:** the *Platynereis* arm (Fig 5A, p25, mAP 0.35 vs random,
    Wilcoxon matched-pairs signed rank, p < 0.01); the human benchmark arm (Fig 5C, p25,
    mAP 0.72 vs SpatialPPIv2 0.33 vs random 0.30, Friedman with Dunn's, p < 0.0001); the
    reverse arm, human-trained model tested on *C. elegans* (Fig 5B, p25, mAP 0.32 vs
    random, p < 0.0001); leave-one-group-out and shuffle-groups-out CV (Figs 3D, 3E, 4D).
  - **NONE RUN for memorization specifically.** There is no post-cutoff arm, no
    date-stratified arm, no "receptors with deposited structures vs without" arm, and no
    sequence-identity-to-PDB analysis. The strongest memorization-adjacent evidence is
    indirect: the model transfers to two phyla it never saw.
  - **UNPOWERED where it counts most.** The prospective, wet-lab-validated arm — the only
    part of the paper that is not re-ranking existing labels — is **2 receptors and 3
    peptides** (Table 1, p26; Fig 6, p26). That is n < 10 by any reading. The *Platynereis*
    arm at 17–18 receptors and only **23 agonist interactions** (p13) is thin but above
    the ~10 threshold on receptors.

- **controls_run**:

| control | what it rules out | page |
|---|---|---|
| Random ranking baseline, 100 randomisations per GPCR/family, AP averaged | That reported mAP is achievable by chance under this class imbalance. Baselines: 0.035 (*C. elegans*, Fig 1F), 0.30 (human, Fig 5C) | p14 (method), p19, p25 |
| **No-template arm** vs active-state-template arm, same 22 035 complexes | That the active-state template does nothing; isolates the template's contribution to mAP (0.36 vs 0.32), to non-agonist exclusion from the pocket (5.5% vs 3.4%) and to peptide pLDDT gain | p6, p20 (Fig 2D–2F) |
| Agonist vs non-agonist pLDDT gain from the template, compared directly (Welch's t-test, p < 0.0001) | That the template raises confidence indiscriminately rather than preferentially for agonists | p20 (Fig 2F) |
| Experimentally confirmed **non-agonists** as the negative class (not decoys) in the *C. elegans* arm | That negatives are untested or artificial — 22 035 pairs "all of which were experimentally confirmed to be either agonist or non-agonist matches" | p4 |
| Exclusion of GPCRs with no concentration-dependent response in the source screen | That non-agonist labels are assay artefacts (misfolding, no expression, no Gα16 coupling) rather than true negatives | p4, p12–13 |
| Peptide-in-pocket predicate applied to agonists **and** non-agonists | That pocket placement alone explains agonism — it does not (99.8% vs 96.6%) | p5, p18–19 (Fig 1D–1E) |
| Three confidence metrics compared against each other and against random (Friedman + FDR) | That any single AF confidence metric was cherry-picked; establishes peptide pLDDT > ipTM ≈ pocket PAE | p19 (Fig 1F), p27 (Supp Fig 1C–D) |
| Single vs pair representation, and three pooling subregions, head to head (2-way RM ANOVA) | That the choice of AF internal tensor is arbitrary | p21 (Fig 3B–3D) |
| Pair-representation subregion ablation (peptide / GPCR-bp / bp–peptide intersection) | That one subregion carries all the signal — it does not; per-family performance varies | p7, p21 (Fig 3E–3F) |
| **Graph ablation, 2×2:** Arpeggio edges vs 6 Å distance edges × with vs without edge features; shuffle-groups-out CV, 11 splits | That either biophysical edge definition or interaction edge features alone accounts for GNN performance | p8, p23–24 (Fig 4D), p28 (Supp Fig 2A) |
| Representations averaged over 5 AF models vs "rank 001" model vs highest-peptide-pLDDT model | That the representation result is an artefact of single-model variation (5-model average ROC-AUC > 0.80 is best) | p13, p28 (Supp Fig 2B) |
| DeorphaNN vs peptide pLDDT on the same complexes (Wilcoxon, p < 0.001) | That the GNN adds nothing over the best raw AF confidence metric (0.41 vs 0.32) | p24 (Fig 4E–4F) |
| **SpatialPPIv2** (state-of-the-art general PPI predictor) on the same augmented human dataset | That any structure-aware PPI model would score as well — it does not (0.33, "not significantly different from random ranking") | p9, p25 (Fig 5C–5D) |
| Human-trained model evaluated on the *C. elegans* set, "which contains no synthetic data" | That the ESM-2-generated synthetic non-agonists are biologically meaningless — validates the augmented human benchmark | p9, p25 (Fig 5B) |
| Grouped CV: stratified group 10-fold by GPCR gene; leave-one-group-out by family; group shuffle-split by family | Receptor-identity and family leakage between train and validation folds | p14, p16 |
| Class-balance subsampling to 1:4 positive:negative per fold | That the classifier is exploiting class imbalance | p16 |
| **Assay negative control: BSA**; **positive control: ATP** (endogenous CHO receptor); lysis for maximal Ca²⁺ normalisation | Non-specific calcium responses and dead/untransfected wells | p16 |
| **Empty-plasmid (no GPCR) transfection** challenged with NLP-70-1, NLP-70-2, NLP-69-1 at 10 µM | That the peptides activate an endogenous CHO receptor rather than the transfected GPCR | p28 (Supp Fig 2C) |
| **Off-peptide control on the deorphanized receptor:** H23L24-4-1 responds to NLP-69-1 but **not** to FLP-21-1 at 10 µM | That the receptor responds to any peptide — a receptor-level specificity control | p28 (Supp Fig 2D) |
| NLP-70-1 (ranked 156/364) tested alongside NLP-70-2 (ranked 1/364) on NPR-33 | That rank is uninformative within a peptide gene family — EC₅₀ 1.16 µM vs 76.3 nM tracks rank | p10, p26 (Fig 6B–6C) |

  **Controls conspicuously NOT run**, each of which the corpus should note:
  - **No inactive-state template arm.** The comparison is active-template vs *no* template,
    never active vs inactive. Nothing in the paper distinguishes "the active state helps"
    from "a trimmed TM-bundle template of any state helps."
  - **No shuffled/scrambled peptide-sequence arm** and no decoy peptides in the *C.
    elegans* work; negatives are real tested non-agonists (a strength) but no
    sequence-shuffle control on the model itself.
  - **No structural control of any kind** — nothing checks that the "active-state"
    complexes are active.
  - **No date-cutoff or memorization arm** (see `anti_memorization_control`).
  - **No orthogonal assay** for the two deorphanized receptors: agonism is established in
    one CHO/Gα16 aequorin assay only, the same platform that generated the training labels.

- **confidence_as_discriminator**: **YES — this is the paper's opening result and it is
  reported as a *partial* success. Quoted verbatim below, since the corpus needs the exact
  hedging.**
  - **Abstract, p2:** "Leveraging a dataset of experimentally validated agonist and
    non-agonist GPCR-peptide interactions from *Caenorhabditis elegans*, we show that
    **AF-Multimer confidence metrics enable partial discrimination between GPCR-agonist and
    non-agonist complexes.** To better reflect agonist-bound conformations, AF-Multistate
    templates are used to produce active-state GPCR-peptide complexes, **improving
    discriminatory power.**"
  - **Introduction, p4:** "we first evaluate AF-Multimer confidence metrics as indicators
    of agonist activity, **revealing their modest discriminative capability.** This
    capability is enhanced when active-state GPCR-peptide complexes—modelled using
    templates derived from AF-Multistate34—are utilized, aligning receptor confirmations
    with functional binding sites."
  - **Results section heading, p5:** "**AF-Multimer confidence metrics partially
    discriminate peptide agonists from non-agonists**"
  - **Discussion, p10:** "Previous studies have shown that pLDDT from AlphaFold predictions
    correlate with interaction affinity31,32,48, aligning with our findings that **pLDDT has
    partial ability to discriminate agonists from non-agonists. However, affinity alone is
    insufficient to determine agonist function49,50.** While affinity is a prerequisite for
    agonism, it fails to capture additional mechanisms like intrinsic efficacy51—the
    propensity of a ligand to induce conformational changes in the GPCR and activation of
    downstream G protein signalling."
  - **The statistics, exactly.**

    | quantity | peptide pLDDT | ipTM | pocket PAE | random | page |
    |---|---|---|---|---|---|
    | mAP, no template | **0.32** | 0.26 | 0.24 | 0.035 | p19 (Fig 1F caption) |
    | mAP, active-state template | **0.36** | NOT REPORTED | NOT REPORTED | — | p20 (Fig 2D caption) |
    | ROC-AUC | **0.77** | 0.76 | 0.71 | 0.50 | p27 (Supp Fig 1C legend, from render) |
    | PR-AUC | **0.09** | 0.07 | 0.06 | ~0.02 (no-skill) | p27 (Supp Fig 1D legend, from render) |

    Statistics: "Friedman test with FDR correction using the Benjamini, Krieger, and
    Yekutieli method, q < 0.05" (p19); template improvement "Wilcoxon signed-rank test,
    p < 0.05" (p20).
  - **The ROC/PR gap is the sharpest quantitative statement of "only partial" in the
    paper, and the paper does not comment on it.** ROC-AUC 0.77 looks respectable; PR-AUC
    0.09 on the same data says that under the real class balance (~457 agonists in 22 035
    pairs, ≈2%) the metric is nearly useless for prioritisation. The two numbers appear
    only inside the Supp Fig 1C–D panel legends and are not quoted in the text.
  - **What is being discriminated is agonism (function), not conformational correctness.**
    The paper never uses pLDDT/ipTM/PAE to judge whether a *state* is right, because it
    never assesses a state. This is the key scoping caveat for our corpus: a
    `confidence-as-discriminator` reverse lookup will return this paper, and what it found
    is that AF confidence partially predicts a *functional* label.
  - **The confidence metric used is peptide-restricted, not global**, and the reason is a
    ceiling: p5, "Since the transmembrane regions of GPCRs are typically predicted with high
    confidence by AF2, we focused on confidence metrics of the peptide. pLDDT scores were
    averaged across peptide residues to yield a single aggregated 'peptide pLDDT' score."
    PAE likewise is restricted: "Per-residue PAE scores for the peptide aligned on the GPCR
    binding pocket residues were averaged to yield a single 'pocket PAE' score."
  - **Validated for its use?** Only functionally and only against ranking: the metric was
    validated against wet-lab agonist labels via mAP/AUC (Fig 1F, Supp Fig 1C–D), and it
    was **not** validated against any structural ground truth. Its selection circularity
    (best-of-5 by the same metric being reported) is unaddressed — see `oracle_leakage`
    route 6.

## D. Claims

- **central_conclusion**: AlphaFold-Multimer's confidence metrics only partially separate
  peptide agonists from non-agonists for GPCRs, and its internal **pair** representations
  carry much more of the discriminative signal than single representations. Biasing every
  complex toward an active receptor conformation with AF-Multistate-derived, trimmed,
  receptor-specific templates measurably improves that separation (mAP 0.32 → 0.36). A
  graph neural network (DeorphaNN) built on these active-state complexes — Arpeggio
  interatomic-interaction edges, pair-representation node and edge features — reaches
  mAP 0.41 on *C. elegans*, transfers to *Platynereis* (0.35) and to a human benchmark
  (0.72 vs 0.33 for a general PPI model), and its top-ranked candidates yielded
  experimentally confirmed agonists for two previously orphan *C. elegans* receptors.

- **necessity_claims** (verbatim + page):
  - p14 — **the MSA-necessity claim, directly relevant to any MSA-manipulation contrast:**
    "MSA reduction was not necessary as the templates were derived from the same sequence
    as the target GPCRs76, and **retaining the full MSA preserves coevolutionary signals
    that are vital for driving accurate inter-protein contact predictions**77."
  - p5 — "Due to the prevalence of peptides positioned in the binding pocket irrespective
    of ligand class, **this feature alone does not provide a reliable basis for
    distinguishing between agonist and non-agonist GPCR-peptide complexes.**"
  - p10 — "**However, affinity alone is insufficient to determine agonist function**49,50.
    While affinity is a prerequisite for agonism, it fails to capture additional mechanisms
    like intrinsic efficacy51—the propensity of a ligand to induce conformational changes in
    the GPCR and activation of downstream G protein signalling."
  - p11 — "**Triggering these toggle switches is thought to require two distinct types of
    intermolecular interactions**: 'anchor' interactions that provide stability for ligand
    binding, and 'driver' interactions that directly engage with toggle switches to induce
    conformational changes63–65."
  - p3 — "Docking methods are able to predict peptide-binding poses to GPCRs24, however
    **they struggle to identify peptide agonists for GPCRs**25, **underscoring the need for
    next-generation computational tools specifically designed to address the unique
    structural and mechanistic complexities of GPCR-peptide interactions.**"
  - p3 — "**these approaches are less effective for GPCRs with no clear orthologues**"
    (of phylogeny-based ligand prediction).
  - p12 — "Additionally, **AF2 cannot account for posttranslational modifications of GPCRs
    and peptides.**"
  - p12 — "for peptides, posttranslational modifications such as C-terminal amidation or
    pyroglutamation **are often important for agonist activity**49."
  - p9 (design necessity for the human benchmark) — "**While this dataset includes human
    GPCR-agonist pairs, it lacks non-agonist interactions. To address this gap, we generated
    synthetic non-agonist GPCR-peptide pairs**..."

- **novelty_claims** (verbatim + page):
  - p11 — "Compared to existing methods, **DeorphaNN represents a significant advancement
    in GPCR-peptide agonism prediction. To our knowledge, the only other model that predicts
    peptide agonists for GPCRs utilizes a support vector machine algorithm trained on
    peptide descriptors (PD-incorporated SVM)**, representing sequence patterns of one to
    five residues that are then one-hot encoded into a numeric array for machine
    learning42."
  - p12 — "By integrating active-state biasing and pairwise embeddings in a GNN framework,
    **we present a novel deep learning approach to GPCR deorphanization** that offers a
    powerful complement to traditional screening methods."
  - p3 — "**computational tools for in silico peptide agonist screening are still
    emerging**, in part because the complexity of peptides—larger, more flexible ligands
    than small molecules—poses a challenge23."
  - p11 — "**Unlike a purely sequence-based approach, DeorphaNN incorporates structural
    predictions from AF-Multimer, deep learning-derived protein representations, and
    intermolecular interaction data. These features enable DeorphaNN to learn relationships
    from three-dimensional structures and biophysical interaction patterns that are not
    captured by the primary sequence**, providing a more comprehensive and biologically
    relevant approach to GPCR-peptide agonism prediction across diverse receptors."
  - p8 — "**Overall, the complete graph structure—using Arpeggio-defined edges and
    interaction embeddings—outperformed all ablated versions, demonstrating the synergistic
    value of biophysically meaningful edges and interaction-aware edge features for agonist
    classification.**"
  - p2 (significance) — "We have developed a machine learning model that combines predicted
    active state complexes, interatomic interactions, and deep learning protein
    representations obtained from AlphaFold-Multimer to identify potential peptide agonists
    for GPCRs."
  - **No claim to be first at active-state template biasing.** The active-state step is
    explicitly credited to AF-Multistate (ref 34) throughout (p4, p6, p10, p13). The
    novelty claimed is the *integration*, not the state biasing.

- **stated_limits** (the paper's own, p10–12):
  1. **Single-assay training data.** p11–12: "because the dataset used for training was
     derived from a single experimental screen, it may have missed interactions dependent
     on specific downstream pathways—such as those involving distinct G protein
     coupling—potentially misclassifying those complexes as non-agonists."
  2. **Dependence on AF2 structural accuracy, with a specific pocket caveat.** p12: "our
     model's performance depends on AF2's ability to accurately predict GPCR-peptide
     complexes—therefore, inaccurate structural predictions may fail to capture the true
     nature of GPCR-peptide relationships, impacting DeorphaNN's effectiveness. Indeed,
     **AF2-predicted GPCR structures demonstrate deviations in the shapes of ligand-binding
     pockets and extracellular domains when compared to experimentally determined
     structures**68,69."
  3. **No post-translational modifications.** p12: "AF2 cannot account for posttranslational
     modifications of GPCRs and peptides... the omission of such posttranslational
     modifications in AF2 predictions may result in lost interaction information." Peptides
     were preprocessed by stripping them: p12, "we preprocessed peptide sequences by
     removing C-terminal glycine residues for amidated peptides and N-terminal glutamine
     residues for pyroglutamated peptides."
  4. **Small training set.** p11: "Despite being trained on a relatively small dataset of
     457 GPCR-agonist pairs from *C. elegans*..."
  5. **Potency bias in the ranking.** p10: "Although we found activation of the receptor,
     the EC50 value (1.16 µM...) is significantly higher than that of the NLP-70-2 peptide,
     **suggesting that DeorphaNN may be intrinsically tuned to prioritize high-potency
     agonist interactions**" — i.e. genuine low-potency agonists will be ranked poorly
     (NLP-70-1 ranked 156/364 and is a real agonist).
  - **Limits the paper does NOT state**, and which the corpus should hold against it: no
    inactive-template control; no structural verification that the "active state" complexes
    are active; the ROC-AUC 0.77 / PR-AUC 0.09 gap; the synthetic nature of every human
    negative; the circularity of selecting a model by peptide pLDDT and then reporting
    peptide pLDDT; the absence of any memorization control.

- **stance**: **`precedent on findings + contrast on rigour`. Provisional — the user's
  call, not the extractor's.**
  - **Precedent**: it is the corpus's clearest worked example of the *templates-based*
    route to a directed active state — AF-Multistate templates, trimmed and pinned into
    AF-Multimer — used at scale (22 035 complexes) and carried through to a
    functional, wet-lab-confirmed endpoint. Its confidence-metric result ("partial
    discrimination", mAP 0.32) is a directly quotable comparator for any claim about what
    AF confidence can and cannot separate. It also demonstrates that an inference-time state
    intervention improves a *downstream functional* task, which is a different and stronger
    kind of evidence than an RMSD improvement.
  - **Contrast**: the active state is asserted, never measured. There is no conformational
    metric, no inactive-template control, and no structural check anywhere in the paper, so
    "active-state complexes" in the title is an unverified property of the pipeline. State
    knowledge enters via an unnamed state-annotated database (route 2) with no accounting of
    what that database contains. The human generalisation rests on fabricated negatives with
    a threshold tuned on the evaluation set.

## E. Quantitative comparators

- **metrics_reported**:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| mAP, peptide pLDDT, no template | 0.32 | mAP (0–1) | Experimentally confirmed agonist/non-agonist labels, 65 *C. elegans* GPCRs | p19 (Fig 1F) |
| mAP, ipTM, no template | 0.26 | mAP | same | p19 (Fig 1F) |
| mAP, pocket PAE, no template | 0.24 | mAP | same | p19 (Fig 1F) |
| mAP, random ranking (*C. elegans*) | 0.035 | mAP | 100 randomisations per GPCR | p19 (Fig 1F), p14 |
| ROC-AUC, peptide pLDDT / ipTM / pocket PAE | 0.77 / 0.76 / 0.71 | AUC | same labels, pooled pairs | p27 (Supp Fig 1C legend, from render) |
| PR-AUC, peptide pLDDT / ipTM / pocket PAE | 0.09 / 0.07 / 0.06 | AUC | same labels, pooled pairs | p27 (Supp Fig 1D legend, from render) |
| **mAP, peptide pLDDT, ACTIVE-STATE TEMPLATE** | **0.36** (vs 0.32 no template; Wilcoxon signed-rank p < 0.05) | mAP | same | p20 (Fig 2D) |
| % peptides modelled outside pocket, no template | 3.4 ± 0.6 (SEM); per-GPCR range 0–24.5 | % | 12.5 Å pocket cutoff, per GPCR | p18 (Fig 1D), p5 |
| % peptides modelled outside pocket, active template | 5.5 ± 0.6 (SEM); paired t-test p < 0.0001 | % | same | p20 (Fig 2E) |
| Agonists modelled inside pocket | 99.8 | % | 12.5 Å cutoff | p18–19 (Fig 1E) |
| Non-agonists modelled inside pocket | 96.6 | % | 12.5 Å cutoff | p18–19 (Fig 1E) |
| Peptide pLDDT gain from template, agonists vs non-agonists | ≈3.9 vs ≈0.4 (from p20 render); Welch's t-test p < 0.0001 | ΔpLDDT | paired same-complex comparison | p20 (Fig 2F) |
| ROC-AUC / PR-AUC, RF on pair vs single representations, 3 subregions | pair > single for GPCR and GPCR-bp subregions; peptide subregion best overall; 2-way RM ANOVA F(1,56)=21.72 p<0.0001 (ROC), F(1,56)=8.602 p<0.01 (PR) | AUC | stratified group 10-fold CV | p21 (Fig 3B–3C) |
| mAP, RF peptide subregion: single vs pair (leave-one-group-out) | single 0.18; **pair 0.28** | mAP per GPCR family | leave-one-group-out CV by gene family | p22 (Fig 3D) |
| mAP, RF by pair subregion | peptide 0.28; bp/peptide intersection **0.31**; GPCR bp 0.23 (Friedman + FDR, q<0.01) | mAP per family | leave-one-group-out CV | p22 (Fig 3E) |
| GNN ablation: Arpeggio + edge features vs ablations | complete graph highest; 2-way RM ANOVA F(1,10)=28.75, p=0.0003; all ablations significantly lower (q<0.05). Absolute mAP range in Fig 4D render ≈0.36–0.44 | mAP | shuffle-groups-out CV, 11 splits | p24 (Fig 4D) |
| **mAP, DeorphaNN (*C. elegans*)** | **0.41** (vs peptide pLDDT 0.32; Wilcoxon signed-rank p < 0.001) | mAP | held-out GPCR families | p24 (Fig 4E) |
| **mAP, DeorphaNN on *Platynereis dumerilii*** | **0.35**, significantly > random (Wilcoxon matched-pairs signed rank, p < 0.01) | mAP | 17–18 annelid GPCRs, 23 agonist interactions | p25 (Fig 5A) |
| mAP, human-trained model → *C. elegans* | 0.32, significantly > random (Wilcoxon, p < 0.0001) | mAP | *C. elegans* set, no synthetic data | p25 (Fig 5B) |
| **mAP, DeorphaNN on augmented human dataset** | **0.72** | mAP | 82 human GPCRs, 345 real agonist + 3370 **synthetic** non-agonist pairs | p9, p25 (Fig 5C) |
| mAP, SpatialPPIv2 on the same human dataset | 0.33 — "not significantly different from random ranking" | mAP | same | p9, p25 (Fig 5C) |
| mAP, random baseline (human) | 0.30 | mAP | same | p9, p25 (Fig 5C) |
| RF ROC-AUC, 5-model-averaged vs single-model representations | 5-model average > 0.80, best of three; rank-001 ≈0.765, highest-pLDDT ≈0.775 (render) | ROC-AUC | CV folds | p13, p28 (Supp Fig 2B) |
| **Prospective rank, NLP-69-1 on orphan H23L24.4** | **5 / 364** | rank | DeorphaNN ranking of 364 candidate peptides | p10, p26 (Table 1) |
| **Prospective EC₅₀, H23L24.4 + NLP-69-1** | **231.7 nM**, n = 6 | nM | CHO Gα16 aequorin calcium assay | p10, p26 (Fig 6A) |
| **Prospective rank, NLP-70-2 on orphan NPR-33** | **1 / 364** | rank | same ranking | p10, p26 (Table 1) |
| **Prospective EC₅₀, NPR-33 + NLP-70-2** | **76.3 nM**, n = 6 | nM | CHO Gα16 aequorin calcium assay | p10, p26 (Fig 6B) |
| Rank and EC₅₀, NPR-33 + NLP-70-1 (same-gene follow-up) | rank **156 / 364**; EC₅₀ **1.16 µM**, n = 6 | rank; µM | same assay | p10, p26 (Fig 6C, Table 1) |
| Retrospective rank, SNET-1-1 on NPR-34 (agonist already known, Beets et al.) | 1 / 364 | rank | same ranking | p26 (Table 1) |
| Retrospective rank, NLP-73-3 on SEB-2 (agonist already known, Beets et al.) | 1 / 364 | rank | same ranking | p26 (Table 1) |
| Median agonists per GPCR (*C. elegans*) | 3 (range 1–61) | count | training dataset | p4, p18 (Fig 1B) |
| Median peptide length | 11 (range 3–37) | residues | training dataset | p4, p27 (Supp Fig 1B) |

  **Predicted vs experimentally confirmed — the distinction the caller asked for, stated
  plainly:**
  - **Experimentally confirmed IN THIS PAPER (new wet-lab work): three receptor–peptide
    pairs across two receptors, all *C. elegans*.** H23L24.4 + NLP-69-1 (EC₅₀ 231.7 nM);
    NPR-33 + NLP-70-2 (EC₅₀ 76.3 nM); NPR-33 + NLP-70-1 (EC₅₀ 1.16 µM). Assay: CHO-K1 cells
    co-expressing the GPCR, promiscuous human Gα16 and mitochondrial apo-aequorin;
    concentration–response curves, n = 6; BSA negative control, ATP positive control, lysis
    normalisation (p16); plus an empty-plasmid control and an off-peptide (FLP-21-1) control
    (Supp Fig 2C–D, p28). **Two receptors deorphanized.**
  - **Predicted only, never tested in this paper:** every mAP number above; the entire human
    arm; the entire *Platynereis* arm; the NPR-34 and SEB-2 ranks (their agonists were
    confirmed by Beets et al., ref 9, not here — Table 1 "Source" column, p26).
  - **The 457 agonist and ~21 578 non-agonist labels used for training are experimentally
    confirmed, but by ref 9, not by this paper** (p4: "all of which were experimentally
    confirmed to be either agonist or non-agonist matches9").

- **n_predictions**: **record the levels separately; the totals are large and the
  prospective level is tiny.**
  - **Per target (per GPCR-peptide pair): 5 AF-Multimer models.** p13: "All modelling
    settings were left at default, resulting in the generation of 5 predicted structures."
  - **Targets — *C. elegans* complexes: 22 035.** Figure 1A caption, p18: "65 GPCRs and 339
    endogenous peptides (**22 035** GPCR-peptide pairs)". 65 × 339 = 22 035, so the caption
    is arithmetically correct and **the results text on p4 ("yielded 20 035 combinations")
    is a typo**; see `unresolved`.
  - **Total *C. elegans* structure predictions: ≈110 175 per arm** (22 035 × 5), and the
    dataset is modelled **twice** — once without a template and once with an active-state
    template (Fig 2D–2F compares them on the same complexes) — so **≈220 350 AF-Multimer
    structure predictions** for the *C. elegans* work alone. The paper never states either
    total; both are derived here from stated numbers.
  - **Plus 65 AF-Multistate template-generation runs** (one active-state model per receptor,
    p13), and the same again for each validation-set receptor.
  - ***Platynereis*: 18 × 122 = 2 196 complexes** by the methods counts (p13), or 17 × 124 =
    2 108 by the results text (p9) — see `unresolved`. ×5 models.
  - **Human: 3 715 pairs** (345 agonist + 3370 synthetic non-agonist, p13), ×5 models.
  - **Prospective screen: 364 candidate peptides × 4 receptors ≈ 1 456 complexes**, of which
    **3 were tested in the lab** (p10, Table 1 p26).
  - **GNN ensemble at inference: 10 models.** p16: "The final predictions reported were
    generated using an ensemble of 10 GNNs trained via bootstrap aggregating, with each
    model trained on a distinct 90% bootstrap sample of the training data."
  - **Random baseline: 100 randomisations per GPCR or family** (p14).

- **comparable_to_ours**: *(left empty per SCHEMA.md v3 — populated by whoever holds
  `STATUS.md` and the manuscript)*

- **si_in_scope**: **PARTIALLY HELD — and what is missing is per-pair, not per-metric.**
  - **HELD:** Supplemental Figures 1 and 2 with full captions, bound as PDF pages 27–28.
    These carry real numbers the main text omits — the ROC/PR AUCs for all three confidence
    metrics (Supp Fig 1C–D, read from the render), the 5-model vs single-model
    representation comparison (Supp Fig 2B), and both assay specificity controls
    (Supp Fig 2C–D).
  - **SI NOT HELD:** Supplemental Data 1 and 2, named on p27 — "A list of the names and
    primary sequences of all GPCRs and peptides in the *C. elegans* training dataset, with a
    list of the experimentally validated agonist pairs" and the same for the *Platynereis*
    and human validation datasets. These hold every per-receptor and per-peptide
    identity, all agonist pair labels, and the 25 recently identified peptides. **Nothing in
    `metrics_reported` is emptied by this** — all headline metrics are in the main figures —
    but no per-receptor value, no per-pair prediction and no dataset composition beyond the
    aggregate counts can be recovered from the held PDF.
  - **Also unheld and relevant:** per-GPCR AP values exist only as heatmap colour (Figs 3F,
    4F, 5D) with no numeric table anywhere, so they are unreadable at any useful precision.

## F. Figures

Panel-group rows follow the v3 rule: split on `mark` or `measure`, never on `facet` alone;
panels differing only in which metric they show, under identical faceting, share one row
with a compound `measure` (the SCHEMA.md worked example). License applies to every row and
is stated once at the end.

| fig_no | page | gist | plot_type | data_shape | panels | hides |
|---|---|---|---|---|---|---|
| 1A | 18 | Dataset → AF-Multimer workflow: 65 GPCRs × 339 peptides = 22 035 pairs into AlphaFold2-Multimer | schematic | `SCHEMATIC \| dataset composition and the AF-Multimer modelling step \| no data` | 1 | |
| 1B | 18 | Frequency distribution of agonists per GPCR | bar | `PLOT \| facet: none (1) \| vary: agonists per GPCR, 0–62 (continuous, binned) \| series: none (1) \| measure: frequency (count of GPCRs) \| mark: bar \| n: 65 GPCRs per panel, 1–17 per bar` | 1 | **x-axis broken twice** (20→40 and 45→60) to accommodate the promiscuous tail; the break makes the 61-agonist outlier look adjacent to the mode |
| 1C | 18 | AF-Multimer models of NPR-11-1 with an agonist (FLP-34-4) and a non-agonist (NLP-36-1) | structure render | `RENDER \| facet: ligand class (2: agonist, non-agonist) \| views: 1 (side-on, membrane normal vertical) \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 2 | Two hand-picked complexes stand for 22 035; no quantitative panel accompanies them and no selection criterion is given |
| 1D | 18 | Per-GPCR percentage of peptides modelled outside the binding pocket | scatter (dot plot) | `PLOT \| facet: none (1) \| vary: GPCR (65, unordered categorical collapsed to one column) \| series: none (1) \| measure: % peptides modelled outside binding pocket \| mark: point \| n: 339 peptides per point, 65 points per panel` | 1 | |
| 1E | 18–19 | Proportion inside vs outside the pocket, agonists vs non-agonists | bar (100% stacked) | `PLOT \| facet: none (1) \| vary: ligand class (2: agonist, non-agonist) \| series: pocket occupancy (2: inside, outside) \| measure: % of pairs \| mark: bar \| n: ~457 agonist and ~21 578 non-agonist pairs per bar` | 1 | **y-axis broken and truncated** (jumps from 0 to ~86%, then 86–100), which visually magnifies a 99.8% vs 96.6% difference the text correctly calls non-discriminative; **n not shown on the panel** |
| 1F | 18–19 | Average precision per GPCR for three AF confidence metrics and random | scatter (dot plot, log x) | `PLOT \| facet: none (1) \| vary: average precision per GPCR, 0.005–1 (continuous, log) \| series: metric (4: peptide pLDDT, ipTM, pocket PAE, random) \| measure: average precision \| mark: point + mean±SEM crossbar \| n: 1 GPCR per point, 65 points per series` | 1 (4 stacked series rows) | |
| 2A | 20 | AF-Multistate → trim → GPCR-specific template → AF-Multimer with peptide | schematic | `SCHEMATIC \| the active-state template pipeline: AF2-multistate model, extracellular and low-pLDDT intracellular trimming, template-driven AF-Multimer co-folding \| no data` | 1 | |
| 2B-C | 20 | Same peptide NLP-12-1 modelled into an agonist receptor (CKR-1-1) and a non-agonist receptor (FRPR-18-2), each with and without an active-state template; pLDDT-coloured | structure render | `RENDER \| facet: receptor–ligand class (2: agonist pair CKR-1-1:NLP-12-1, non-agonist pair FRPR-18-2:NLP-12-1) × template (2: none, active state) \| views: 1 (pocket close-up) \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 4 (2 per letter) | Two exemplars stand for 22 035 complexes; **B and C have opposite left/right template ordering** (B: "without (left) and with (right)"; C: "with (left) and without (right)"), which invites misreading |
| 2D | 20 | Average precision per GPCR, no template vs active-state template | scatter (dot plot, log x) | `PLOT \| facet: none (1) \| vary: average precision per GPCR, 0.005–1 (continuous, log) \| series: template condition (2: no template, active-state biased template) \| measure: average precision \| mark: point + mean±SEM crossbar \| n: 1 GPCR per point, 65 points per series` | 1 (2 series rows) | |
| 2E | 20 | Per-GPCR % peptides outside pocket, paired across template conditions, plus the paired differences | scatter with paired connecting lines | `PLOT \| facet: none (1) \| vary: template condition (2: no template, active state) + difference column (1) \| series: GPCR identity (65, as pairing lines) \| measure: % peptides modelled outside binding pocket, and its paired difference \| mark: point + connecting line \| n: 339 peptides per point, 65 pairs per panel` | 1 (2 sub-columns + a difference axis) | The difference sub-panel uses a **second right-hand y-axis on a different scale** in the same frame |
| 2F | 20 | Mean pLDDT gain from the active-state template, agonists vs non-agonists | bar | `PLOT \| facet: none (1) \| vary: ligand class (2: agonist, non-agonist) \| series: none (1) \| measure: peptide pLDDT difference (active-state template − no template) \| mark: bar + SEM whisker \| n: ~457 agonist and ~21 578 non-agonist complexes per bar` | 1 | **Two bars hide two distributions of ~457 and ~21 578 paired values**; only mean ± SEM is drawn, so the overlap between the classes — which is what "preferentially improves agonists" needs — is invisible; **n not shown** |
| 3A | 21 | How single (ℝ^{n×256}) and pair (ℝ^{n×n×128}) representations are pooled over four residue subregions | schematic | `SCHEMATIC \| tensor-slicing and local average pooling of AF-Multimer single and pair representations into GPCR / GPCR-bp / peptide / bp-peptide feature vectors \| no data` | 1 | |
| 3B-C | 21 | Random-forest performance by representation type and subregion, in ROC and PR space | scatter (dot plot) | `PLOT \| facet: metric (2: ROC-AUC in B, PR-AUC in C) \| vary: subregion (3: GPCR, GPCR bp, peptide) \| series: representation type (2: single, pair) \| measure: ROC-AUC (B) + precision-recall AUC (C) \| mark: point + mean bar \| n: 1 CV fold per point, 10 folds per series` | 2 (one metric each, identical faceting → one row per the v3 worked example) | y-axes do not share a range between B (0.2–1.0) and C (0.0–0.4), which is correct but makes the two panels look more similar than they are |
| 3D | 21 | Per-family AP, single vs pair representations, leave-one-group-out | scatter (dot plot, log x) | `PLOT \| facet: none (1) \| vary: average precision, 0.005–1 (continuous, log) \| series: representation type (2: single, pair) \| measure: average precision per GPCR family \| mark: point + mean±SEM crossbar \| n: 1 family per point, 55 gene groups per series` | 1 (2 series rows) | |
| 3E | 21 | Per-family AP across three pair-representation subregions | scatter (dot plot, log x) | `PLOT \| facet: none (1) \| vary: average precision, 0.005–1 (continuous, log) \| series: pair subregion (3: bp/peptide, GPCR bp, peptide) \| measure: average precision per GPCR family \| mark: point + mean±SEM crossbar \| n: 1 family per point, 55 gene groups per series` | 1 (3 series rows) | |
| 3F | 21 | Which subregion predicts which GPCR family | heatmap | `MATRIX \| rows: GPCR family (57 labelled rows, AEX-2 … TRHR-1) \| cols: pair subregion (3: peptide, GPCR bp, bp/peptide) \| value: average precision (0–1, sequential colourbar) \| facet: none (1)` | 1 | Values readable only as colour; **no numeric table anywhere in the paper**, and the SI holding per-pair data is not bound in |
| 4A | 23 | Graph representation: peptide nodes, GPCR nodes, sequence edges, Arpeggio edges, edge features | schematic | `SCHEMATIC \| the GPCR-peptide graph and its two edge types \| no data` | 1 | |
| 4B | 23 | Arpeggio-identified interatomic interactions drawn on one predicted complex | structure render | `RENDER \| facet: none (1) \| views: 2 (whole complex, and a zoomed pocket inset) \| overlay: NOT REPORTED predictions on 0 references \| axis: none` | 1 (+ inset) | |
| 4C | 23 | Pair-representation slicing into GPCR / peptide / interaction subregions and pooling into node and edge features | schematic | `SCHEMATIC \| per-residue cross-axis pooling of pair-representation sub-tensors into 128-d node embeddings and interaction edge features \| no data` | 1 | |
| 4D | 23 | 2×2 ablation of edge definition and edge features | scatter (dot plot) | `PLOT \| facet: none (1) \| vary: edge features (2: absent, present) \| series: edge definition (2: 6 Å distance edges, Arpeggio edges) \| measure: mAP \| mark: point + mean±SEM crossbar \| n: 1 CV split per point, 11 shuffle-groups-out splits per series` | 1 (4 groups) | **y-axis truncated to 0.36–0.46 and does not include zero or the random baseline (0.035)**, which visually inflates a ~0.05 mAP spread into the full panel height |
| 4E | 23 | Per-GPCR AP, DeorphaNN vs peptide pLDDT | scatter (dot plot, log x) | `PLOT \| facet: none (1) \| vary: average precision, 0.002–1 (continuous, log) \| series: predictor (2: peptide pLDDT, GNN prediction) \| measure: average precision per GPCR \| mark: point + mean±SEM crossbar \| n: 1 GPCR per point, ~57 points per series` | 1 (2 series rows) | |
| 4F | 23 | Which GPCRs DeorphaNN rescues relative to pLDDT | heatmap | `MATRIX \| rows: predictor (2: peptide pLDDT, GNN prediction) \| cols: GPCR (57, labelled) \| value: average precision (0–1, sequential colourbar) \| facet: none (1)` | 1 | Column labels are rotated and set at a size that is unreadable at print scale; values are colour-only with no numeric table |
| 5A-C | 25 | Cross-species generalisation: *Platynereis*, human-trained → *C. elegans*, and DeorphaNN vs SpatialPPIv2 vs random on human | scatter (dot plot, log x) | `PLOT \| facet: evaluation arm (3: A *Platynereis* n=17–18 GPCRs, B human-trained model on *C. elegans* n=65, C augmented human n=82) \| vary: average precision, 0.005–1 (continuous, log) \| series: predictor (2 in A and B; 3 in C: DeorphaNN, SpatialPPIv2, random) \| measure: average precision per GPCR \| mark: point + mean±SEM crossbar \| n: 1 GPCR per point; 17–18 (A), 65 (B), 82 (C) points per series` | 3 (identical mark and measure, differ only by dataset → one row per the v3 split rule) | Panel C's negatives are **synthetic** (ESM-2 dissimilarity, threshold 3.9 fixed on this dataset) and the panel does not say so; the caption calls it an "augmented" dataset only |
| 5D | 25 | Per-GPCR AP, DeorphaNN vs SpatialPPIv2 on the human set | heatmap | `MATRIX \| rows: predictor (2: SpatialPPIv2, DeorphaNN) \| cols: human GPCR (82, labelled) \| value: average precision (0–1, sequential colourbar) \| facet: none (1)` | 1 | 82 rotated column labels, unreadable at print scale; colour-only values with no numeric table |
| 6A-C | 26 | Concentration–response curves for the three newly confirmed receptor–peptide pairs | line (sigmoid fit) + point | `PLOT \| facet: receptor–peptide pair (3: H23L24-4-1+NLP-69-1, NPR-33-1+NLP-70-2, NPR-33-1+NLP-70-1) \| vary: log peptide concentration (continuous) \| series: none (1) \| measure: % of maximal calcium response \| mark: point + fitted sigmoid line with error bars \| n: 6 replicates per point, n = 6 per panel` | 3 | |
| S1A-B | 27 | Distribution of agonists-by-gene per GPCR, and of peptide length | bar (histogram) | `PLOT \| facet: quantity binned (2: A agonist genes per GPCR 0–30, B peptide length 3–37 AA) \| vary: bin (continuous, binned) \| series: none (1) \| measure: frequency (count) \| mark: bar \| n: 65 GPCRs (A), 339 peptides (B) per panel` | 2 (same mark and measure → one row) | Panel A's **x-axis is broken** between 10 and 20 and again at 25, hiding how isolated the promiscuous tail is |
| S1C-D | 27 | ROC and PR curves for the three confidence metrics, pooled over all pairs | line | `PLOT \| facet: curve type (2: C ROC, D precision-recall) \| vary: false positive rate 0–1 (C) / recall 0–1 (D) (continuous) \| series: metric (4: peptide pLDDT, ipTM, pocket PAE, no-skill) \| measure: true positive rate (C) + precision (D) \| mark: line \| n: 22 035 pairs pooled per curve, NOT REPORTED per point` | 2 (identical faceting, two metrics → one row per the v3 worked example) | **These panels carry the paper's most damaging number and it is only in the legend:** PR-AUC 0.09/0.07/0.06 against ROC-AUC 0.77/0.76/0.71. Neither AUC set appears in the main text. Curves are **pooled across all 65 GPCRs**, not per receptor, so they weight promiscuous receptors heavily — the exact bias the paper elsewhere adopts mAP to avoid |
| S2A | 28 | Per-GPCR benefit of edge features on Arpeggio graphs | box | `PLOT \| facet: none (1) \| vary: GPCR (~57, labelled categorical) \| series: GPCR (~57, colour, redundant with vary) \| measure: relative difference in AP (with edge features − without) \| mark: box with whiskers and outlier points \| n: 11 shuffle-groups-out splits per box, ~57 boxes per panel` | 1 | Colour encodes the same variable as the x-axis and carries no information; a single ~25 outlier stretches the y-axis so ~50 of the ~57 boxes are compressed into a flat band at 0 |
| S2B | 28 | Whether averaging representations over 5 AF models beats using one selected model | scatter (dot plot) | `PLOT \| facet: none (1) \| vary: model-selection strategy (3: 5-model average, rank-001 model, highest peptide pLDDT model) \| series: none (1) \| measure: ROC-AUC \| mark: point + mean±SEM crossbar \| n: 1 CV fold per point, ~10 folds per strategy` | 1 | **y-axis truncated to 0.6–0.9**, excluding the 0.5 chance line, which magnifies a ~0.04 AUC difference |
| S2C-D | 28 | Assay specificity controls: empty-plasmid transfection, and an off-target peptide on the deorphanized receptor | bar | `PLOT \| facet: control type (2: C empty plasmid vs three peptides, D H23L24-4-1 vs BSA/ATP/FLP-21-1/NLP-69-1) \| vary: peptide or control (3 in C, 4 in D) \| series: stimulus class (3 in C: ATP, BSA, peptide; 1 in D) \| measure: ratio of total calcium response \| mark: bar + SEM whisker \| n: NOT REPORTED per bar` | 2 (same mark and measure → one row) | **n is not reported for any bar** in either panel, in the two panels that carry the specificity controls for the paper's only new wet-lab claim |

- **reuse (applies to every row above)**: **CC-BY 4.0 International — no ND clause,
  derivatives and redrawing are permitted with attribution.** Stated in the bioRxiv banner
  on **every page, including p1**: "It is made available under a CC-BY 4.0 International
  license." **Caveat:** this license covers the **preprint**. The *Molecular Cell* 2026
  version (`10.1016/j.molcel.2026.07.006`) is not held and its license is
  **`NOT REPORTED`** — an Elsevier version may carry different terms, so reuse of any
  *journal* figure must be checked separately. Reuse of the **preprint** figures at these
  page numbers is safe under CC-BY 4.0 with attribution.

- **Table 1 (p26)** is a data table, not a figure, and so has no row above. It is the
  single most quotable object in the paper: five GPCR–peptide pairs with UniProt IDs,
  peptide sequences, DeorphaNN rank out of 364, and a **Source column that separates the
  two rows credited to "Beets et al.9" (retrospective) from the three credited to "This
  paper" (prospective)**.

## G. Provenance

- **extracted_on**: 2026-09-07
- **extractor**: claude subagent (Claude Opus 5), single-paper extraction under
  `EXTRACT_PROMPT.md` with the v3 amendments in `BATCH_PROMPT.md`.
- **schema_version**: v3
- **confidence**: **high** for A, B, D, E and for `oracle_leakage` routes 3–7,
  `controls_run` and `confidence_as_discriminator`; **medium** for `oracle_leakage`
  routes 1–2, because the entire active-state mechanism is delegated to ref 34 in a single
  sentence and this paper never names the state-annotated database, never describes the
  restricted MSA protocol, and never states which AF-Multistate state model was taken;
  **medium** for the figure rows, where marks, axis ranges, break positions, series counts
  and the Supp Fig 1C–D AUC values had to be read from renders because the text layer
  carries none of them and the captions name no plot types. What was hard: the mathematical
  notation is destroyed in the text layer (recovered from the p21 render); per-GPCR AP
  values exist only as heatmap colour and cannot be read at any precision; and the two
  Supplemental Data files, which hold every sequence and every pair label, are not in the
  PDF.
- **unresolved**:
  1. **Journal version not held.** The corpus cites *Molecular Cell* 2026,
     `10.1016/j.molcel.2026.07.006`; the PDF is the March 2025 bioRxiv preprint. Figure
     numbering, panel letters, statistics and the Table 1 contents may all have changed in
     review, and *Molecular Cell* would normally require the STAR Methods format, which
     this preprint does not use. **Do not cite a page number from this note against the
     journal version.** The venue split is recorded as instructed; the tag applied is
     `preprint`.
  2. **The state-annotated database is never named.** p13 says only "This approach
     leverages state-annotated GPCR databases to guide predictions with a restricted MSA
     protocol." Which database (GPCRdb or other), how many annotated structures, what the
     annotation is, whether any nematode sequence is in it, and how the MSA restriction
     works are all delegated to ref 34 (Heo & Feig 2022). Resolvable from
     `notes/heo2022multistate.md`, which was **deliberately not consulted** for this
     extraction under rule 1 of `EXTRACT_PROMPT.md`. Someone should cross-link the two
     notes at index time.
  3. **Pair-count discrepancy: 20 035 vs 22 035.** p4 results text says "yielded 20 035
     combinations"; the Figure 1A caption (p18) says "22 035 GPCR-peptide pairs". 65 × 339
     = 22 035, so p4 is a typo. This note uses 22 035 and flags it.
  4. ***Platynereis* count discrepancy.** p9 says "17 GPCRs and 124 peptides"; p13 methods
     say "resulting in 122 peptides" and "resulting in 18 receptors and 23 agonist
     interactions". Both counts are reported above; neither can be resolved from the PDF.
  5. **The number of agonist pairs is given once and never derived.** p11 says "457
     GPCR-agonist pairs", which is not reconstructible from any other number in the paper.
     The non-agonist count (22 035 − 457 = 21 578) is nowhere stated; it is inferred here
     and marked as such.
  6. **Which AF-Multistate output was used is not stated beyond "top ranked".** p13: "The
     top ranked active state structures were processed" — ranked by what criterion, and how
     many candidates, is not said.
  7. **No AF2/ColabFold version, database version, or MSA date.** p13 says only "local
     ColabFold75" with "All modelling settings were left at default". Whether ColabFold
     defaults meant templates off (they normally do) is not stated explicitly, though the
     paper's own "No Template" labelling in Figure 2 makes it near-certain.
  8. **The receptor counts in Figures 3F, 4F and 4E (~57 labelled rows/columns) do not
     match the stated 65 GPCRs or 55 genes.** Counted from the renders; the captions do not
     give a count and the discrepancy is unexplained.
  9. **Peptide pLDDT selection circularity is unaddressed.** The reported peptide-pLDDT
     discriminator is a max-over-5-models statistic (p13), and the same metric selects the
     model. The paper never reports the metric on a fixed or random model, so the size of
     the inflation is unknown.
  10. **v3 grammar ambiguity — the split rule contradicts its own worked example.** "Split
      when `mark` or `measure` differs" is stated as deterministic, but the immediately
      following example says "four box panels showing four metrics under the same faceting
      are one row with a compound measure". Panels 3B/3C, S1C/S1D and S2C/S2D each show a
      *different measure* with an *identical* mark and faceting. I followed the worked
      example (one row, compound `measure`), which contradicts the rule as literally
      written. **The rule should be restated as: split on `mark`; split on `measure` only
      when the faceting also differs.** Three rows in this note depend on that reading.
  11. **v3 grammar gap — PLOT has no slot for a paired/repeated-measures structure.**
      Figure 2E connects 65 points across two conditions by GPCR identity; that pairing is
      the whole point of the panel and the reported paired t-test depends on it. `series`
      is the only slot available and is a poor fit (65 "series" of two points each), and a
      figure-design query for "paired before/after with connecting lines" will not join on
      anything in this grammar.
  12. **v3 grammar gap — a dot plot with a categorical axis collapsed to one column.**
      Figure 1D plots 65 GPCRs as an unordered jittered column with the x-axis labelled
      just "GPCRs". `vary:` presupposes something actually varies along the independent
      axis; here nothing does. Written as `vary: GPCR (65, unordered categorical collapsed
      to one column)`, which is a hack.
  13. **v3 gap — `states_generated` has no vocabulary for "two pipeline arms, neither
      verified".** This paper models every complex twice, with and without an active-state
      template, but never applies a state predicate to either. `one`, `two`, `ensemble` and
      `continuum` all mislead. Written as `two (as two pipeline arms) + single-state (per
      run)` using the v3 dual-value permission, with the caveat spelled out in the field.
  14. **v3 gap — no field records that a paper's success criterion is *functional* rather
      than structural.** This is a structure-prediction paper whose entire evaluation is a
      wet-lab agonist label and whose `state_metric` is therefore honestly "none for
      conformation". That is a striking property and it currently has to be smuggled into a
      preamble note. A `success_criterion` field (structural / functional / both) would
      capture it.
  15. **Tag needed but unavailable (recorded, not invented):** there is **no tag for
      "cross-species generalisation" or "transfer learning"**, which is one of this paper's
      two headline claims (trained on *C. elegans*, evaluated on annelid and human).
      `anti-memorization` is the closest available and is not the same thing. Also **no tag
      for "synthetic/fabricated negatives"**, which is how the entire human benchmark's
      negative class was constructed (p9, p13) and is a material rigour caveat that a
      reverse lookup should be able to find. Both were left uninvented per rule 9.
  16. **Tag boundary question — `unpowered`.** Applied here for the prospective wet-lab arm
      (2 receptors, 3 peptides), while the same paper's retrospective arms have n = 65 and
      n = 82. v3 defines `unpowered` per-paper, with no way to scope it to one arm, so the
      tag will read as if the whole paper is underpowered. It is not; only the arm that
      matters most is.
- **why_it_matters**: *(left empty — the user's call)*

## Tags

`gpcr` `cofolding` `template-state-bias` `msa-state-filter` `templates-on`
`state-annotated-input` `single-state` `binary-predicate` `continuous-metric`
`saturating-metric` `oracle-leak` `design-level-oracle` `prospective` `anti-memorization`
`unpowered` `confidence-as-discriminator` `experimental-validation` `directed-state`
`peptide-driven` `orthosteric` `preprint` `precedent` `contrast` `negative-result`
`comparator-numbers`

Tag notes, so the reverse lookups stay honest:

- **`template-state-bias`** is the primary method tag and is unambiguous: an active-state
  template per receptor, trimmed and pinned into every AF-Multimer run (p13). **This is the
  corpus's cleanest templates-based alternative to steering the internals.** Note what the
  template is: an *AlphaFold prediction* of the target sequence, not a deposited structure.
- **`msa-state-filter`** applied, but **scoped and inherited**. This paper does not filter
  an MSA itself — it explicitly retains the full MSA and says so (p14). The state-filtered
  ("restricted MSA") step lives inside the AF-Multistate call that generates the templates
  (p13). A reverse lookup for MSA state filtering *should* surface this paper, because the
  mechanism is load-bearing for every result after Figure 2, but whoever follows the lookup
  must read this note, not assume the paper implements it. **`msa-subsample` is NOT
  applied** — depth is never reduced, and v3 is explicit that these are different things.
- **`templates-on` + `state-annotated-input`** applied for the main arm. **`no-template-
  no-msa` is NOT applied** even though a no-template arm exists, because that arm keeps the
  full MSA and so is not the de-novo input regime the tag marks.
- **`cofolding`** — AF-Multimer folds receptor and peptide together in every prediction
  (p13). This is co-folding of a protein–peptide complex, not small-molecule co-folding.
- **`single-state`** applied, `two-state` **deliberately withheld**. Each run yields one
  conformation, there is no ensemble and no sampling over states. The paper does model every
  complex twice (no template / active template, Fig 2), but it never applies a state
  predicate to either arm, so calling it `two-state` would false-positive a query looking
  for methods that demonstrably produce two verified states. The two-arm structure is
  recorded in `states_generated` and `unresolved` item 13 instead. `ensemble` and
  `continuum` are both plainly wrong.
- **`binary-predicate` + `continuous-metric`**, matching the dual `state_metric`.
  `binary-predicate` is the 12.5 Å peptide-in-pocket call (p5); `continuous-metric` covers
  AP/mAP, AUC, pLDDT and EC₅₀. **`rmsd-only` is emphatically NOT applied — there is no RMSD,
  TM-score or any structural reference metric anywhere in this paper.** **`visual-metric` is
  NOT applied**: no state is called by eye either; Figures 1C and 2B–C are illustrative and
  the claims attached to them are made quantitatively elsewhere.
- **`saturating-metric`** refers to two real numeric ceilings: the pocket-occupancy feature
  at 99.8% vs 96.6% (Fig 1E, p18–19), which the paper itself identifies as the reason the
  feature is useless; and AP piling up at 1.0 on the human benchmark (Fig 5C, p25). Axis
  breaks and truncations — Figs 1B, 1E, 2F, 4D, S1A, S2B — are **figure** defects and are
  recorded in `hides`, per v3 rule 9, not here.
- **`oracle-leak`** applied **for route 2 only**, and scoped. State knowledge derived from
  deposited structures enters every prediction via AF-Multistate's state-annotated databases
  (p13). It is *not* target-level leakage: the targets are *C. elegans* GPCRs with no
  deposited structures, so no answer for a scored target could have been read off a
  database. Routes 3, 5 and 6 are genuinely clean, and routes 5–6 are clean in an unusually
  strong way — there is no held structural reference in this paper at all, so success cannot
  be defined post hoc against one. Route 4 fires weakly (the ESM-2 threshold of 3.9 was
  fixed on the human evaluation set against its known agonists, p9/p13).
- **`design-level-oracle`** applied for route 7, kept distinct from `oracle-leak` as v3
  requires: receptors were included only if already known to have an agonist (p4); two of
  the four "deorphanization" receptors had published agonists before DeorphaNN ranked them
  (p10, Table 1 p26); and the active state was declared the target state before any result
  was read (p6).
- **`prospective`** applied, scoped: genuinely prospective for two orphan receptors and
  three peptides that were predicted then tested in the lab (p10, Fig 6). Everything else
  is retrospective re-ranking. See `prospective` for the split.
- **`anti-memorization`** applied because held-out sets exist **and were run as arms**
  (cross-species *Platynereis* and human, family-grouped CV, 25 post-training-screen
  peptides). **`no-anti-memorization` is NOT applied**, but read `anti_memorization_control`
  before relying on it: the held-out design is by **species and gene family, never by
  date**, and the paper never asks a memorization question, never states AF2's cutoff and
  never analyses the 82 human receptors — many of which do have deposited active-state
  structures inside AF2's training set — for possible memorization.
- **`unpowered`** applied for the prospective wet-lab arm only: 2 receptors, 3 peptides.
  The retrospective arms are not underpowered (65, 82 receptors). v3 offers no way to scope
  the tag to an arm; see `unresolved` item 16.
- **`confidence-as-discriminator`** applied, and this is one of the strongest instances in
  the corpus — the paper's Figures 1F and Supp 1C–D exist for exactly this question. **But
  note the scope in `confidence_as_discriminator` before quoting it:** what pLDDT/ipTM/PAE
  are shown to partially discriminate is **agonism, a functional label**, not conformational
  correctness. The paper never uses confidence to judge a state.
- **`experimental-validation`** applied: a computational paper that took its own top-ranked
  predictions into a CHO/Gα16 aequorin calcium assay and confirmed three receptor–peptide
  pairs with EC₅₀ values (p10, p16, Fig 6 p26), with empty-plasmid and off-peptide controls
  (Supp Fig 2C–D, p28). **`experimental` is NOT applied** — that tag marks a paper with *no*
  structure prediction in it, and this paper is built on structure prediction.
- **`directed-state`** applied: the state is instructed, not sampled, and the handle is
  named (active-state AF-Multistate template). **`peptide-driven`** applied: the co-folded
  partner is a peptide and the peptide is the ligand under test. **`ligand-driven` is NOT
  applied** — it reads as small-molecule in this vocabulary and `peptide-driven` is the
  specific tag. **`g-protein-mimetic` and `nanobody` are NOT applied**: nothing is co-folded
  but the peptide, and the G-protein-facing intracellular region is *deleted* from the
  template (p6). **`seed-only` is NOT applied**: one fixed seed, no seed sweep (p14).
  **`apo-sampling` is NOT applied**: every scored prediction is a holo complex. The
  AF-Multistate template-generation step is receptor-only, but tagging on that would
  false-positive a query looking for apo conformational sampling as a result.
- **`orthosteric`** applied: the site studied is the peptide-binding helical cavity, which
  the paper calls the orthosteric pocket (p10: "reconfigure the surface of the orthosteric
  binding pocket58,59"). **`allosteric-site`, `cryptic-pocket` and `allosteric-failure` are
  NOT applied** — no allosteric site is studied and no such result is reported.
- **`multi-backbone` NOT applied** — exactly one structure backbone (AF2/AF-Multimer via
  ColabFold). ESM-2 and SpatialPPIv2 are not structure backbones.
- **`af-cluster`, `latent-steering`, `md`, `md-emulator`, `enhanced-sampling` and
  `benchmark-only` all NOT applied.** In particular **`latent-steering` is wrong**, and the
  distinction matters for this corpus: DeorphaNN **reads** AF-Multimer's pair representation
  and feeds it to a downstream classifier; it never intervenes on it. The state intervention
  here is a template, upstream of the trunk, not a tensor edit inside it.
- **`preprint`** applied per the venue split; **`peer-reviewed` NOT applied** even though a
  *Molecular Cell* 2026 version exists, because the held and read artefact is the
  uncertified preprint. See `unresolved` item 1.
- **`precedent` + `contrast`** — matching the dual `stance`; provisional.
- **`negative-result`** applied, scoped to two findings that are genuinely negative and
  genuinely useful: pocket placement does not discriminate agonists at all (99.8% vs 96.6%,
  p5), and AF confidence metrics only *partially* do (mAP 0.32, PR-AUC 0.09, p19/p27).
- **`comparator-numbers`** applied — the paper is unusually rich in directly quotable
  numbers (the mAP ladder 0.035 → 0.24/0.26/0.32 → 0.36 → 0.41, the ROC/PR AUC pair, two
  EC₅₀ values with ranks). **`figure-exemplar` NOT applied**: the figures are competent and
  the per-GPCR paired dot plot is a reusable design, but several panels carry real defects
  (truncated and broken axes, bars over 21 578-value distributions, colour-only heatmaps
  with no numeric table), so they should not be recommended as templates.
