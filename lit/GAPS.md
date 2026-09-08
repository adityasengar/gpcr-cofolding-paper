# GAPS.md — what the corpus does not know

Generated 2026-09-08 by aggregating the `confidence` and `unresolved` fields of all
66 notes. This is the Step 4 report `PROMPTS.md` asks for, which the build never produced.

`UNRESOLVED.md` covers DOI resolution only, despite its name. This file covers the per-note
`unresolved` field — the content SCHEMA.md says must never be silently dropped.

**Use it as a pre-citation check.** Before a draft sentence leans on a paper, look up that citekey
below. If the thing you are about to claim appears here, the extraction could not determine it and
the PDF has to be opened.

---

## Extraction confidence

**No paper was extracted at low confidence.** 56 high,
10 medium or medium-high, 0 recorded as a qualified split ("high on X, medium on Y").

Papers at medium — a claim drawn from these deserves a second look:
- `khaleq2026hyaline` — medium.** The text layer is clean and every number in Tables 1–4 and the body was legible. Confidence is held below high for two r
- `lee2026foldswitch` — medium-high.** The prose extracts cleanly and page markers are reliable. Two things were hard: (a) the PDF's two-column-plus-float
- `obendorf2026statespecific` — medium-high.** Text extraction was clean and the Methods are unusually explicit about the biasing pipeline, so B, C and D are soli
- `schafer2025confounds` — medium-high.** - *High* on all body text: the paper is six pages, the text layer is clean, and every claim in sections C, D and E 
- `stein2022speachaf` — medium-high.** - **High** for the mechanism, the protocol, the target list, the licence, the claims and the tags: the text layer i
- `suzuki2026pairscaling` — medium-high.** The text layer is clean and every quote above is verbatim from `pdftotext -layout`. Lower confidence on three thing
- `swapna2025memorization` — medium.** High for the protocol description, the claim quotations, the licence and the figure structure, all of which are unambigu
- `tran2026nanogs` — medium-high.** The text extracted cleanly and the argument is unambiguous. Two things reduce it: (1) **all quantitative pharmacolo
- `vo2026fiducials` — medium-high.** The text layer is clean and every main-text number was legible. Held below high for three reasons: (1) **the entire
- `waymentsteele2025reply` — medium-high.** - *High* on the argumentative content, the Methods and all of sections C and D: the paper's prose is unambiguous an

Papers with a split confidence statement: .

Five notes remain on schema v2 and lack `structural_priors_used`, `controls_run` and
`si_in_scope` entirely: `obendorf2026statespecific`, `suzuki2026pairscaling`, `tran2026nanogs`, `waymentsteele2024cluster`, `ye2026multistatebias`.

---

## Unresolved items — 358 across 51 of 66 papers

### abramson2024af3 (15)

- **Extended Data Fig. 4c values are not printed.** The homology-stratified PoseBusters result — the single most useful anti-memorization number in the paper — exists only as three bar heights (≈89 / ≈82 / ≈78%). No table, no SI held. Same for the ED Fig. 5b medians
- **No total prediction count and no compute figure** anywhere in the article, Methods or Extended Data
- **Fig. 1c mixes four measures on one axis** labelled "Success (%)" and the caption discloses this in prose only. Recorded in `hides`, but flagged here because it is the figure most likely to be re-quoted from this paper
- **The confidence-calibration arm has no homology control** ("with no homology filtering and including peptides", p5), so nothing in Fig. 4 or ED Fig. 8 separates calibration on training-similar chains from calibration on novel ones. Not resolvable from this PDF
- **SI not held** — see `si_in_scope` for the specific consequences
- **tags needed but not in the v3 vocabulary** (recorded, not invented):
- A **`model-release` / `foundation-model`** tag. This paper is neither a benchmark (`benchmark-only` is plainly wrong — it introduces a model) nor a state-handling method. The corpus now holds several papers that *use* AF3 and none that is *about* releasing a backbone. Without such a tag, "which pape
- A **`cutoff-authority` / `training-cutoff-source`** utility tag. The stated purpose of this note is that other papers define their held-out sets against AF3's cutoff. `comparator-numbers` is close but means accuracy numbers, not dates. A query for "where does our cutoff number come from" currently c
- A **`hallucination`** or **`disorder`** topic tag. The paper's hallucination/cross-distillation material (p4, p5–p6, ED Fig. 1) is substantive and reusable, and there is no tag that finds it
- A **`diffusion`** method tag. `cofolding` is correct and was used, but it does not distinguish a diffusion-based generative co-folding model from a regression-based one — a distinction that matters directly to whether a model can produce multiple states at all
- A **`privileged-input`** or **`pocket-conditioned`** tag for the fine-tuned pocket-specified arm. `oracle-leak` overstates it (the arm is deliberate, labelled, and reported separately); nothing else fits
- **schema ambiguities hit while extracting (blunt, as asked)**:
- **No field records architecture, model size, training compute or availability.** For a model paper these are the first things a reader wants and the schema has nowhere for them; I put code availability in section A as an ad-hoc addition, which will not join against anything
- **`n_targets` presupposes one number.** This paper has eleven evaluation arms with different units (targets, structures, clusters, complexes, interfaces). I wrote a per-arm list, which is not parseable as a number. A `n_targets_by_arm` sub-table, or an explicit instruction to list, would help
- **`system` has no value for "all of the PDB".** `general protein` is the closest and undersells a paper whose whole point is nucleic acids, ligands, ions and modifications. The `general-protein` tag has the same problem

### chai2024chai1 (10)

- **Antibody–protein n is 122 in the text and 121 in two figures.** p4 says "268 interfaces across 129 structures, forming 122 redundancy reduced clusters"; Figures 2 (p3) and S2 (p14) both label the axis n = 121. Table 2 gives no n. Which is right is not determinable from the PDF
- **Figure 5's caption contradicts itself on homology filtering** (p7): "we show results for all interfaces in our low homology subset, and do not restrict only to interfaces with low homology." If the second clause governs, the confidence-calibration analysis includes training-homologous interfaces a
- **The antibody–antigen evaluation set (Figure 4) has no stated size.** It is described only as differing from the antibody–protein set and as counting each antibody/antigen copy in a PDB separately (p5). Every Figure 4 percentage is therefore unpowered as far as this PDF can tell
- **The confidence model is never described.** p10 promises "A confidence model is then used for ranking (details below)" and no such details appear anywhere in the paper. Its architecture, training data, training objective and full output set are unknown; only ipTM and ligand interface pTM are named 
- **No parameter count, no training-set size, no training-step count** for Chai-1 (only 128 A100s × batch 128 × 30 days, p9). The 3B figure on p9 is the *language model's* size, not Chai-1's
- **AFDB and genetic-database vintages are not dated.** The 2021-01-12 cutoff is stated for PDB and PDB70 only; AFDB has no stated cutoff and sequence databases are deferred to reference [6] (p9–10). This limits how cleanly the single cutoff date characterises the model
- **Two dates on p1** — bioRxiv "this version posted October 15, 2024" versus the paper's own "Date: September 9, 2024". Both recorded in `year`; the citekey's 2024 is unaffected
- **Nucleic-acid numbers exist only as boxplots** (Figure S3, p14). No iLDDT or C1′-LDDT value is printed anywhere for Chai-1 or RoseTTAFold2NA, so the "similar performance" claim on p6 cannot be quantified from this paper
- **No version-2 changelog inside the PDF.** The task brief identifies this as bioRxiv v2; the document itself carries no revision note, so nothing here can be attributed to the revision
- **Second tag gap, lower priority:** there is no **Utility** or **Method** tag marking a model whose *weights are publicly released*, which is the single most consequential property of this paper for anyone building on it. `benchmark-only` is the opposite of what Chai-1 is, and no openness tag exists

### chakravarty2026statespace (6)

- **Provenance of the three EAAT TM-scores (p4: 0.608 / 0.834 / 0.897).** If computed here, this perspective contains a small amount of original analysis and is a different citation from one that contains none. The GitHub figure repository (p18) is not held and would settle it. Everything else in the 
- **Second tag needed but not available: something for "proposes evaluation criteria / reporting standards".** This document's most citable content is a prescription, and there is no tag for a paper that sets standards rather than reporting results. `comparator-numbers` is the closest utility tag and 
- **State-handling tags deliberately withheld** for the same reason: the paper argues for `ensemble` and `continuum` as the prediction *target* but generates neither
- **`stance` third value.** `threat` is arguable (see `stance`); not tagged, deferred to the user
- **Venue.** Typeset in Springer Nature journal style but posted only to arXiv, with no journal named and no submission statement. Whether a journal version exists is not determinable from this PDF
- **No figure licence anywhere in the PDF.** Every `reuse` cell is NOT REPORTED. arXiv's per-submission licence is not printed in the document

### chib2025gpcrstates (7)

- **Two different residue correspondences are used and never reconciled.** The superposition uses PyMOL's own sequence alignment (p6, SI p20); the distances use a separate Biopython longest-subsequence + residue-name best-match correspondence (SI p22–23). They need not agree, and no check that they do
- **Which AF3 server output was analysed is not stated** (p6). The server returns multiple ranked models; no seed, count or selection rule is given. The AF2 arm has the mirror-image gap: AFDB models are pLDDT-top-ranked by DeepMind, which the paper does not mention
- **Templates and MSA handling are entirely unreported for both arms** — the word "template" never appears, and "MSA" appears only as background on p3. For a paper whose conclusion is about training-data bias (p10), whether the reference structures were available as templates is a first-order question
- **No statistical test, correlation coefficient, mean or standard deviation appears anywhere in the paper.** The activity-level trend, the AF2-vs-AF3 difference and the class differences are all asserted from the visual appearance of scatter plots. Nothing in the PDF permits an effect size to be quot
- **The ~90 points in Figures 3 and S2 are not reconciled with the stated 16 GPCRs** (SI p23). Presumably multiple deposited structures per receptor, but the paper never says, so the per-panel n is genuinely unknown
- **No tag was needed that does not exist in v3.** Nothing was invented. Two vocabulary *choices* were close calls and are documented under Tags below (`multi-backbone`, `apo-sampling`)
- **Schema ambiguity — `n_targets` has no slot for "the headline analysis and a secondary analysis use different sets".** 75 for the metrics, 16 for the class analysis, and the paper states class-level conclusions from the 16. Recorded as sub-bullets, which will not join against a single integer in `I

### chitsazi2025gpcrdock4 (3)

- **Whether the assessors' AF3-era arm covered GPR139.** The Methods section is headed "End-to-end modeling of **APJ/Cmpd6** complexes" and describes runs for that complex only (p22), but the Results report a GPR139 finding from the same four methods (p12). Sample counts, seeds and settings for any GP
- **The 1 Å / 2 Å / 3 Å receptor-accuracy cutoffs are never justified.** They appear only in the Results prose (p10–p11) and in no Methods definition, with no citation and no rationale. Every "70% of models had TM RMSD < 1 Å"-style statement depends on an unjustified threshold. (The *ligand-side* thre
- **`si_in_scope` is the practical ceiling on this note.** No per-model score, no per-group method text, no country breakdown, no alternative-reference figure and no AF3-era panel is held. If we need any of those, the SI must be obtained from bioRxiv

### feldman2026alphainterp (9)

- **The random-unit-vector noise baseline for activation patching is specified in Methods (p31) and its result is reported nowhere.** I searched the full text for "random unit", "noise baseline", "random direction" and "random vector"; the only hit is the Methods sentence itself. This is the paper's s
- **How many Pairformer layers does AF3 have, in this study's setup?** Never stated. C₁ and C_N are both "after the final Pairformer layer", so **no intra-Pairformer depth resolution exists** and no claim in this paper can be attributed to a specific layer. Anyone citing this note for "layer-by-layer"
- **Which AlphaFold 3 implementation, version or weights?** Never named. The `pairedMsa` / `unpairedMsa` JSON fields (p31, p35) identify the official open-source interface, but no repository, commit, release date or weights identifier appears anywhere. There is likewise **no code or data availability 
- **The Novel-vs-Similar anti-memorisation control has no number, no test and no figure panel** — only the sentence "performance differences between the two groups were negligible at every checkpoint" (p9). The comparison that carries the memorisation argument is the only major analysis in the paper w
- **"Near-perfect accuracy" for amino-acid re-identification (p7) is never quantified.** It is the paper's probe-faithfulness control and has no number
- **Checkpoint A's recycling step is never stated.** B is explicitly r = 0, C₁ is r = 0, C_N is r = N−1; A is left unspecified, and since sequence initialisation is recomputed or carried across recycles depending on the module, this matters for interpreting the A → B contrast
- **Fold-switch domain count vs pair count.** The text says 46 pairs (p15, p25); Fig 3D/F report n = 92 with a 63/27/2 split. 92 = 46 × 2 is the obvious reconciliation, but the paper never states it, and it means each *pair* contributes two non-independent points to the waterfall
- **`refs.bib` records a different title from the PDF** (see `title`). The bib entry should probably be updated; I have not changed it
- **Blanket significance statement.** p37: "Unless otherwise noted, all statistical tests, correlations, and regression analyses reported are significant at p < 0.05." **No individual p-value appears anywhere in the paper**, and no multiple-comparison correction is mentioned despite ~60 printed correl

### ferguson2026deorphann (9)

- **Pair-count discrepancy: 20 035 vs 22 035.** p4 results text says "yielded 20 035 combinations"; the Figure 1A caption (p18) says "22 035 GPCR-peptide pairs". 65 × 339 = 22 035, so p4 is a typo. This note uses 22 035 and flags it
- ***Platynereis* count discrepancy.** p9 says "17 GPCRs and 124 peptides"; p13 methods say "resulting in 122 peptides" and "resulting in 18 receptors and 23 agonist interactions". Both counts are reported above; neither can be resolved from the PDF
- **The number of agonist pairs is given once and never derived.** p11 says "457 GPCR-agonist pairs", which is not reconstructible from any other number in the paper. The non-agonist count (22 035 − 457 = 21 578) is nowhere stated; it is inferred here and marked as such
- **Which AF-Multistate output was used is not stated beyond "top ranked".** p13: "The top ranked active state structures were processed" — ranked by what criterion, and how many candidates, is not said
- **No AF2/ColabFold version, database version, or MSA date.** p13 says only "local ColabFold75" with "All modelling settings were left at default". Whether ColabFold defaults meant templates off (they normally do) is not stated explicitly, though the paper's own "No Template" labelling in Figure 2 ma
- **The receptor counts in Figures 3F, 4F and 4E (~57 labelled rows/columns) do not match the stated 65 GPCRs or 55 genes.** Counted from the renders; the captions do not give a count and the discrepancy is unexplained
- **Peptide pLDDT selection circularity is unaddressed.** The reported peptide-pLDDT discriminator is a max-over-5-models statistic (p13), and the same metric selects the model. The paper never reports the metric on a fixed or random model, so the size of the inflation is unknown
- **v3 grammar gap — a dot plot with a categorical axis collapsed to one column.** Figure 1D plots 65 GPCRs as an unordered jittered column with the x-axis labelled just "GPCRs". `vary:` presupposes something actually varies along the independent axis; here nothing does. Written as `vary: GPCR (65, un
- **Tag boundary question — `unpowered`.** Applied here for the prospective wet-lab arm (2 receptors, 3 peptides), while the same paper's retrospective arms have n = 65 and n = 82. v3 defines `unpowered` per-paper, with no way to scope it to one arm, so the tag will read as if the whole paper is under

### georgiou2025heterogeneity (12)

- **directional_control**: **NOT APPLICABLE as a method property** — the review controls nothing. **But it is one of the best available inventories of the *physical* handles that direct a Class A receptor to a state**, which is why it matters to us:
- **Orthosteric ligand, graded by efficacy** — inverse agonist → S1/S2; neutral antagonist → inactive-like; **partial agonist → I2**; **full agonist → shifts toward A but does not reach it alone**; superefficacy agonist (BU72, lofentanil at μOR) → *"stabilize only the two active conformations, A^TM6 a
- **Transducer** — Gs / Gi / Go heterotrimer, **Gs^GDP vs Gs^empty** (nucleotide state changes the answer), mini-Gs (a 21-residue Gαs C-terminal peptide is enough to shift populations, p.10), Gα C-terminal peptides
- **G-protein-mimetic nanobodies** — **Nb80, Nb6B9, Nb39, Nb6** used throughout as the surrogate that produces A^TM6
- **β-arrestin** and **GRK** — direct to distinct, non-Gs active states; β-arr-biased agonists act on **TM7** rather than TM6 (p.15)
- **Allosteric modulators** — PAM Cmpd-6FA (β2AR, 6N48), NAMs amiloride/HMA/Fg754 at the Na⁺ site, SBI-553 at NTS1R
- **Ions** — **Na⁺ stabilises inactive**; **Ca²⁺/Mg²⁺ shift toward active** (I2/A), an effect amplified when agonist + mini-Gαs are present (p.9)
- **Lipids and membrane mimetic** — anionic phospholipids (**PIP₂**) *"enhanced the population of active-like conformation A^TM6, thus priming the receptor toward recognizing Gαs"*; **cholesterol/CHS acts oppositely in different receptors** — shifts A2AR toward active but acts as a **NAM against β1AR*
- **Mutations** — **R291^7.56A traps A2AR in I2^TM6** (the cleanest single state-trapping handle in the review, p.9); constitutively activating mutations I92^3.40N and R291^7.56Q; D52^2.50N reduces activity and *"eliminated the sensitivity of the receptor to the efficacy of bound ligands"* (p.13)
- **Construct artefacts that act as unintended handles** — **T4L fused into ICL3 forces active TM6 conformations regardless of ligand efficacy** in β2AR (p.16) and may create an artefactual broken lock in A2AR 3PWH (p.9). **Relevant to anyone using T4L-fusion structures as state references.**
- **anti_memorization_design**: **NOT APPLICABLE.** No trained model, no training set, no cut-off, nothing that could be memorised. The nearest analogue — whether the review's conclusions depend on structures deposited after some date — is not a meaningful question for a secondary source
- **anti_memorization_control**: **NOT APPLICABLE**, same reason. `NONE RUN` would be technically true and semantically empty

### heo2022multistate (7)

- **Scope of the 70% sequence-identity template exclusion.** p10 states it "For the benchmark test." Whether it also applied to the proteome-wide run or to the GPCR Dock submissions is not stated. If it did not, those arms could see the target's own homologues
- **Number of protein–ligand complexes in the docking benchmark** — Table S3, not held. The Figure 4A error bars are therefore uninterpretable from the PDF alone
- **No justification is given for the 1.5 Å TM-RMSD "high accuracy" threshold** or the 3 Å docking success threshold. Both are used throughout as if standard
- **Exact docking success percentages** for the model arms are given in prose as "around one third", "less than 10%", "around 30%", "less than 80%"; the numeric values exist only as bar heights. Values in `metrics_reported` marked "read from Figure 4A" are eyeballed from the 150 dpi render and should 
- **No tag was needed that does not exist in v3.** Nothing invented
- **Schema ambiguity — panel-group suffixes assume the figure has panel letters.** Figure 3 has eight panels and no letters at all, so `fig_no` had to carry a prose qualifier ("3 (density row of each pair)") which will not join cleanly against a `4A`-style key. Suggest allowing a positional suffix con
- **Schema ambiguity — `facet` in PLOT with two crossed variables.** Figure 3 is faceted by state *and* by predictor. The grammar shows a single `<var> (<n>)`; the RENDER worked example uses `×` for crossed facets, so `×` was borrowed into PLOT here. Worth stating explicitly in v4 that crossing with `

### hilger2020gcgr (12)

- **The [³H]-GDP dissociation rate constant for GCGR is 0.002 s⁻¹ in the body text (p.6) and 0.0022 s⁻¹ in the Fig. 5D caption (p.7).** Again both confirmed on renders. Cite the caption value with the caveat, or cite the ratio (~20-fold slower than β<sub>2</sub>AR), which is unaffected
- **TM6 outward movement is 18 Å at T351<sup>6.42</sup> (p.3, p.5) and 17.4 Å at F345<sup>6.36</sup> (Fig. 3A annotation, p.5).** These are two markers on the same helix, not two estimates of one quantity, but the paper never says so. If we quote "18 Å", quote it with the marker atom
- **"the α carbon of T356<sup>6.42</sup>" in the Fig. 3B discussion (p.5)** conflicts with **T351<sup>6.42</sup>** used in the Fig. 3 caption and panel label on the same page. Confirmed on the render; another printed typo. T351<sup>6.42</sup> is the correct residue (6.42 is consistent with the numberi
- **The DEER reliability-limit formulae on p.15 are unreadable in OCR and page 15 was not rendered.** The OCR gives `r_max ≈ 5·t_max/2s` and `σ_max ≈ 4·t_max/2Us`, which are nonsense as printed; the standard forms are cube roots of (t_max/2). **This note therefore does not quote them**, and anyone nee
- **No error, confidence interval or replicate count is given for any DEER distance distribution** — no n in the Fig. 6A–B caption, in the Results text, or in the DEER methods (pp. 8, 15). For a null result this is the single most important missing number, and it is missing from the main text; whether
- **Every kinetic rate constant is a bare point value with no error.** k<sub>on</sub>, k<sub>off</sub> and turnover rates are quoted to 1–2 significant figures with no CI anywhere in the main text; table S7 presumably has them and is not held. This limits how strongly the ~73-fold GEF ratio can be sta
- **The per-receptor G<sub>s</sub> dissociation rates for the eight non-GCGR receptors in Fig. 7A are not printed numerically anywhere in the held PDF** (table S9, not held). If the corpus needs, say, GLP-1R's rate to compare against a class B prediction, it must be read off the dot plot or obtained f
- **n for each receptor in Fig. 7A/B is not stated** — "Each dot represents data from individual independent experiments" with no count (p.10). Counting dots off the render gives roughly 4–6 per receptor; that is an estimate, not the paper's number
- **No copyright, licence or permissions statement appears anywhere in this scan** (checked on renders of pp. 1–11 and by OCR keyword search of pp. 12–17). The `reuse` column of every figure row therefore reads NOT REPORTED. Whoever prepares the manuscript must resolve AAAS permissions independently; 
- **The bibliographic identity (journal, volume, article number, DOI, year) is not printed on any page of the scan.** It is taken from `refs.bib` and `MANIFEST.csv`. If the citation matters, verify against the publisher record rather than against this PDF
- **Fig. 4 cites "PDB 6EG8 (73)" but the reference list in this PDF ends at 72** (visible on the render of p.6 and in the p.17 OCR). Either a reference is missing from the scan's final column or the citation number is off by one. The PDB code itself is unambiguous
- **The Supplementary Information is entirely absent** — figs. S1–S9 and tables S1–S9 (see `si_in_scope`). Notably, the **entire MD result** (fig. S8E) and the **HDL-particle DEER repeat** (fig. S7C) exist only as one-sentence summaries in the main text

### jedryszek2026probing (7)

- **No tag exists for a mechanistic-interpretability / probing study.** `latent-steering` correctly covers the causal half but says nothing about the linear-probe and SAE decoding half, which is two-thirds of the paper. A reverse lookup for "which papers probed internal representations" will not find 
- Whether Boltz-1 was run with templates on or off is **not stated anywhere**, so `templates` is NOT REPORTED rather than inferred. For a paper whose entire object is what the trunk represents, whether template features were present is not a trivial omission
- **Whether the 486 evaluation proteins overlap Boltz-1's training set is never addressed.** The sequence-identity control (A.5, p.9) governs probe folds only. Both `anti_memorization_design` and `_control` are therefore NONE against the predictor, and no statement in the paper contradicts or confirms
- The z-score threshold separating "steers" from "null" in Table S2 (p.17) is never given; it is bracketed only by the reported values (1.0 < z < 5.0)
- Fig. S13's ablation runs on n=24 with no explanation of why it is not the same 97 proteins as the additive arm
- The "companion study" recovering zinc-coordination and kinase catalytic-histidine latents (p.5) has no citation, no reference number and no data in this PDF; it cannot be followed up from the document
- External artefacts (SAE weights, activations, analysis code, "compute fan-out") are footnoted on p.1 and p.9 but not held by the corpus

### jung2026boltzperturb (9)

- **Boltz-2 training cutoff date is never stated**, though the phrase "Boltz-2 training cutoff" is the sole basis for the anti-memorization design (p5 ×2, p15 ×2). The RnP benchmark curation date is likewise never given. Both are inherited by citation
- **Table S2's `V highT` row (p18) duplicates the `Vx` row exactly** (2.25 / 3.01 / 9.01 / 3.82 / 7.21) and disagrees with Table 1's V_hT column (p6: 2.457 / 3.015 / 8.947 / 2.158 / 7.195). One of the two tables is wrong; the paper does not flag it
- **Sample size of the true-coordinate injection experiment is never reported** — no n per variance condition, no seed count, no total runs. §B.4 (p15) reports a qualitative success/ failure split ("some runs successfully recovered ... some did not") with no fraction attached
- **"Variance (run condition)" — the x-axis of Figure S1 — is never defined**, and the mapping from a variance threshold to a denoising step index is never given, although the tail-end window discussion (p17) shows the authors know that step 154 of 200 corresponds to t ≈ 0.25
- **p2 and p7 describe the same 17.7% → 30.6% pair differently**: p2 calls it "the fraction of predictions with ligand RMSD lower than 2Å", p7 calls it "the oracle success rate" over 62 targets. The numbers reconcile as 11/62 and 19/62, i.e. p7 is correct and p2 is a mislabel
- **The abstract's "2.6 to 7.8 fold" is not stated against named baselines anywhere.** It reconstructs from Figure 4's rounded SR20 values as 14.0/5.3 (vs vanilla) to 14.0/1.8 (vs MSA masking), so the upper end of the range is measured against the paper's weakest baseline
- **p23 says "we report the top-30 ranked poses" while every table and figure reports top-20.**
- **Templates**: never stated on or off for any arm
- **Tag I needed and could not use** — see the Tags section: there is no Control-block tag for an intervention that is deliberately *undirected*, and no Method-block tag for a diagnostic that injects the ground-truth answer to probe the landscape

### junker2026peptidedesign (3)

- **ETB complex count is inconsistent.** p3: "the Endothelin receptor type B (ETB) with **four** unique ETB-ligand complexes"; p10: "The Endothelin receptor type B (ETB) was present in the dataset a total of **five** times with different peptides". Only three are shown in Fig 7. S1 Table would settle 
- **Fig 5's caption colour key contradicts the figure** (caption p8: "blue: AF2IG, orange: Boltz2, green: RF3"; the plotted AF2IG marks and the in-figure legend are red/salmon). Verified by rendering p8
- **The 91 / 22 GPCR-peptide vs GPCR-protein split appears only in the abstract (p1).** The Results (p3) give 113 dimers, the class A/B1 breakdown and the four-nanobody count, but never restate the 91/22 split; the ≤50-residue peptide vs >50-residue protein boundary is defined at p3 and p5 but no coun

### kim2026mac1 (8)

- **Template usage is never stated.** "SMILES strings... and the sequence of the enzyme as inputs" (p4) is consistent with either templates on (defaults) or off. For a target with dozens of pre-cutoff deposited structures this is the difference between a sequence-only prediction and a template-guided 
- **Boltz-2's training cutoff is given two different dates**: "1 June 2023" (Methods, p17) and "2023-06-30" (Results, p3). One month, immaterial to the argument, but the corpus should quote the Methods date
- **Figure 4 panel b is missing from this version** — panel "a)" is printed twice on p11 while the caption and the p9 text both describe a panel b and cite three correlations from it (r = −0.297, −0.387, and a null). Likely a v3 layout error; recorded in `hides`
- **Figure 5 panel lettering contradicts the running text.** The Fig 5 caption and the rendered panel labels read a) σ₂, b) D4, c) AmpC; the p12–13 text cites "For AmpC (Fig. 5b)" and Fig 5c for D4. The AUROC values disambiguate it, but a reader following panel letters from the text will land on the w
- **The virtual-screen arm's relationship to the training cutoffs is never analysed.** Two of the three source campaigns (Lyu 2019, Alon 2021) predate AF3's 2021-09-30 cutoff. The paper characterises those sets by *chemical* similarity to training (Tc 0.11–0.19) but never by deposition date, so the ar
- **Chai-1 was dropped from the virtual-screen arm without explanation** — "only AlphaFold3 and Boltz-2 were used" (p18); no reason given
- **Only AF3 was tested for receptor conformational recovery.** Chai-1 and Boltz-2 conformational performance is unmeasured, so "co-folding does not recover the conformational change" rests on one model with n = 19 and n = 20
- **D4 n disagrees between sections**: Methods p18 says 549 molecules were prioritised, while p13 and SFig 12 give 205 actives + 336 inactives = 541, and p12 says 541 tested. Eight molecules unaccounted for

### krishna2024rfaa (5)

- **931 vs 938.** The covalent-modification test set is "931 recent entries" in the text (p7) and "938 recently solved structures" in the Fig 3B caption (p18). Neither is corrected. Seven structures unaccounted for; the 46% success rate is quoted against the 931 figure
- **PoseBusters set size.** Never stated in this PDF; the 42% / 38% / 52% comparison in `metrics_reported` therefore has no denominator here
- **Held-out ligand-binding-protein set size** for the RFAA-vs-RF2 comparison (Fig S3A, p26) is never given, although a paired t-test with p = 6.7e-10 is reported from it
- **No data-availability, code-availability or competing-interests statement** anywhere in this PDF. Unusual for a Baker-lab release; presumably added in the Science version
- **Samples per target is never stated** for RFAA. Whether the CAMEO server submitted one model or a ranked set, and how many recycles were used at inference, are both unrecoverable here

### ku2026promise (4)

- **Preprint or proceedings?** p1 carries both the bioRxiv "not certified by peer review" banner and a PMLR/ICML 2026 proceedings footer. Tagged `preprint` only. If the ICML acceptance is real, this note's publication tag needs revisiting
- **BioEmu's 71 vs 72 intrinsic clusters.** Figure 2B annotates "N=50/71" for BioEmu while every other model shows /72. The text never mentions a dropped cluster
- **Templates**: the paper never states whether any predictor's structural-template channel was enabled. This matters for a memorization argument and is simply absent
- **Whether any GPCR survives in the released dataset.** The paper reports none and explains why none would (p9), and the GO panels show no receptor wedge, but no per-target list is in the PDF; only the GitHub release could settle it definitively

### lam2026metadiffusion (7)

- **Whether templates were used is unrecoverable from the PDF.** The word never appears. For a paper whose claim is that the bias moves the structure, this is a material gap
- **Whether an MSA was used, and at what depth**, is likewise never stated for the authors' own runs
- **The 256 per-protein Pearson R values are in Supplementary File 1, which is not in the PDF** (see `si_in_scope`). The distribution behind the paper's only statistical claim is not in the corpus
- **Wasserstein-1 vs Cramér distance:** the text and figures label the SAXS metric one way and Methods names another (p5, p21 vs p9). Not resolvable from the PDF
- **The p5 chemical-shift sentence is internally garbled** ("with and without SAXS steering respectively" attached to arms that are actually unbiased vs steered). Direction resolved from Fig 5b in-panel values, but the sentence as written should not be quoted
- **No affiliation superscript is typeset for author Xing Er Ong** (p1)
- **The MfnG hinge-angle range claim** ("This range is larger than that of default Boltz-2", p3–4) is supported only by the Fig 2c density, whose n is never stated

### lee2025seqassoc (6)

- **The TM-score threshold used for the lowered cases is never stated**, nor is the list of targets it was applied to (p9 names only human lymphotactin, with "in some cases"). The success rate of 35% is therefore not reproducible from the paper
- **The origin of the seven-depth grid (1:2 … 64:128) is not given.** It is inherited from ref 20 (the authors' own prior work) and no justification, sweep or calibration for the specific endpoints appears in this paper. Whether the endpoints were ever tuned on a set containing the evaluation targets 
- **No false-positive rate for blind mode.** No single-fold (non-switching) protein set is run through blind mode anywhere in the paper. The 2.4% hit rate and the 5% extrapolation are uncorrected for false positives, and the authors acknowledge the risk in words (p9: "it may predict alternative confor
- **Number of known fold switchers recovered inside the E. coli blind screen is not given.** p7 names RfaH and MinE "along with homologs of fimbrial proteins", but no count and no denominator, so the blind screen's recall on its own positive controls cannot be computed
- **The E. coli arm's total structure count is not reported** (see `n_predictions`); 2126 × 200 is arithmetic, not an extracted number
- **Two internal cross-reference errors** that a later reader will trip on: p4 cites "Fig. 3h" where Fig 4h is meant, and p7 cites "Fig. 5c" where Fig 7c is meant. Noted so a quote-checking pass does not conclude the note misattributed a page

### lee2026confornets (17)

- **OF3p-preview's training cutoff and training set are never stated.** This is the single most consequential gap in the paper: without it, no claim about memorization of the 86 transfer targets (all deposited, all PDB-sourced) can be evaluated, and OOD60's "out-of-distribution" label demonstrably doe
- **Benchmark membership is not enumerated.** The 51 GPCR pairs, 20 kinase pairs, 34 cryptic pockets, 21 domain-motion, 15 fold-switch and 19 OOD60 proteins are described procedurally but not listed; only the 11 A-loop-flipping kinases are named (p15). The benchmarks are therefore not reproducible fro
- **No code or data availability statement.** Whether ConforNets will be released is not stated
- **Table 1 mixes recycling settings across rows** ("we report the better of R = 11 or R = 1 for all methods", p5). Any citation of a Table 1 value should say which R it came from; Tables A3 (R=1, p17) and A4 (R=11, p18) are the fixed-setting sources
- **Fig. 2a shows only Ours-dist and Fig. 3a only Ours-coord**, with no statement that the other arm was omitted. Whether the omitted arm would change the visual conclusion is undeterminable from the PDF
- **Whether the diversity-mode k=2 ConforNets can be steered at all is untested.** The paper never asks whether a diversity ConforNet, once trained, transfers — only transfer-trained ones are reused. So "reusable across proteins" (abstract, p1) is demonstrated only for the supervised variant
- **No cross-family transfer test.** Whether a GPCR ConforNet does anything to a kinase — the obvious null — is never run
- **The number of ConforNets behind each box/point in Figs. A6 and A8 is never given.**
- **Venue is ambiguous.** ICML-style formatting with an Impact Statement, but no conference is named; recorded as arXiv preprint. **Tag vocabulary gaps encountered (needed but not in the fixed v3 list — NOT invented, recorded here as the schema requires):**
- **A protocol tag for "templates off, MSA on".** v3 has `no-template-no-msa` and `templates-on` but nothing for the very common regime this paper uses in every main experiment: full MSAs from ColabFold, templates explicitly withheld (p13). I could not tag the paper's actual protocol. Suggest `templat
- **A method tag for diffusion/coordinate-space guidance.** `latent-steering` is defined as intervention on "pair representation, trunk embedding, distogram head, conditioning embedding" — ConforMix, run here as a full baseline arm, guides the *diffusion score* in coordinate space and fits no v3 metho
- **A tag for cross-protein transfer of a learned control.** `directed-state` covers "a state was directed", but the reusable-across-proteins property is this paper's distinguishing claim and has no tag. Suggest `transferable-control`
- **A rigour tag for "the training label is a deposited structure of the target state".** This is a different animal from `oracle-leak` (evaluation-time) and from `design-level-oracle` (route 7), and it is exactly what separates a learned control method from a sampling one. Suggest `supervised-on-targ
- Not needed but noted: `md-emulator` correctly describes BioEmu, which appears here only as a comparator, so the paper is not tagged with it. **v3 schema ambiguities hit while extracting (blunt, as asked):**
- **`method_class` has no entry for latent steering**, although the tag vocabulary gained `latent-steering` in v3. I wrote `other` plus a description. The B-table list and the tag list should be reconciled
- **`states_generated` dual form is under-specified for a paper with two modes.** "ensemble + one" is right but reads as one method that does both; here it is two methods. The schema's example ("ensemble + single-state") is a collapse *within* one method. A future reader of INDEX.md will not see the d
- **`metric_saturation` says "numeric saturation only", but a success@B metric saturates *structurally* (monotone in B, bounded at 1) as well as numerically in specific panels.** I recorded both and cross-referenced Fig. 6. Worth a sentence in the schema on max-over-samples metrics, which are now the 

### lewis2025bioemu (3)

- **Local-unfolding benchmark size: 20 or 21?** Main text p6 says "72% of locally folded and 74% of locally unfolded states across 20 protein examples"; SI p29 says "Local unfolding: A set of 21 examples"; Table S4 (p33) sums to 20 folded references and 20 unfolded. Fig. S3 (p36) shows 20 labelled pan
- **MEGAscale train/test split sizes are never given** (Fig. 4a, p9), so the headline ΔG MAE of 0.76 kcal/mol on test carries no n
- **Success threshold justification.** The 1.5 Å cryptic-pocket threshold is justified in words (p6); the 3 Å domain-motion threshold and the 0.3/0.7 FNC state boundaries are stated (p33, p36) but never justified. Recorded in `state_metric` as thresholds-without-justification

### li2026embedding (10)

- **Total structure count is not recoverable.** Sweep widths appear only as figure axes, and the arms are not fully crossed. Reported per-arm in `n_predictions` with a lower bound; the repository would settle it
- **No per-system numbers outside the galleries.** Fifteen of the seventeen figure rows carry data that exists nowhere in tabular form (see `si_in_scope`). Anything the corpus wants to cite per-target — beyond the cc values printed on Figs 5, 12, 13 — would have to be re-derived from the code
- **`prospective` deliberately not tagged.** The verdict is `partial`: one arm of 6 real targets is prospective in its inputs, two arms of 101 targets are not, and every arm scores against a deposited reference. Tagging `prospective` would return this paper for "which papers were prospective" on the s
- **`multi-backbone` deliberately not tagged.** Protenix and Boltz-1 both appear, but the schema sets the bar at "more than two are compared head to head", and the authors themselves say the two-backbone comparison is confounded with the method comparison (p9)
- **Third tag needed but not available: something for a documented failure mode of a *baseline* method.** `negative-result` exists under "Relation to us" and would misfile this as a negative result about the paper's own method, which it is not — the paper's DPS collapse data (p19, p22, p23) is a posit
- **`experimental-validation` deliberately not tagged.** The real cryo-EM arm uses experimental *data* as an input, which is not the same as testing a prediction in the lab; the tag's gloss ("tested a prediction in the lab (NMR, cryo-EM, an assay)") could be read either way. Read strictly here: nothin
- **`templates` is NOT REPORTED, not "off".** The word never occurs; Protenix's default template handling is not stated and must not be assumed
- **No licence anywhere in the PDF**, so every `reuse` cell is NOT REPORTED. The arXiv per-submission licence is not printed in the document. The code repository (`github.com/rs-station/embedopt`, p1) is not held and its licence is unknown
- **Venue.** NeurIPS-style typesetting, but the document says only "Preprint." (p1). Whether a conference version exists is not determinable from this PDF
- **Relationship to `Fadini et al. 2025` and to the concurrent `Maddipatla et al. 2026`** is stated by these authors (p5, p18) and taken at face value here; neither is held by the corpus as far as this extraction can tell, and both are direct methodological neighbours of the "optimise the embedding" i

### liu2026ensembletests (4)

- `extracted_on` — `BATCH_PROMPT.md` and the task both specify 2026-09-07, but today is 2026-09-08. I used 2026-09-07 as instructed
- **Starting structures for the 36 Lockbox simulations are never stated** (p14 gives the force field, water model, salt and length, but not the source of the initial coordinates). This matters for `structural_priors_used` and I could not resolve it
- **`metric_saturation` vs `hides` boundary was easy here but the `hides` column got crowded.** ED Fig. 7b/c use two different truncated y-axes (0.96–1.00 vs 0.4–0.9) to show an invariance next to a response — a figure defect, recorded in `hides` per v3 rule 9. The *numeric* invariance is in `metric_s
- **Fig. 3a's "ensemble-only rail"** places four models outside the plotting plane. I recorded it under `hides`, but it is arguably the correct design given post-gate is NA by task — v3 has no way to mark a figure choice as *defensible but potentially misleading*

### masters2025physics (6)

- **Seed / diffusion-sample count per prediction is never stated** for any of the four models, in the main text or Methods. This makes the case-study figures irreproducible as displayed and makes "the highest-confidence structure" (p.9) uninterpretable — highest of how many?
- **No templates-off arm.** The paper's own mechanism (pp.7–8) predicts the failure would weaken with templates and MSA disabled, and this is never tested. Whether the models were run with template search actually enabled is inferred from "default settings" (p.9), never stated
- **Model versions and dates are not given** for AF3, RFAA, Boltz-1 or Chai-1 — relevant because training-set membership (p.3, p.9) is version-dependent
- Fig. 3's per-bin n is not recoverable from the PDF; the 285 complexes are split across three pLDDT bins of unknown size
- The three additional AF3 mutagenesis systems (SI Fig. S17, p.9) are not identified in the main text
- Minor: the paper contains several typos in load-bearing sentences ("indicated the models are overfit", p.2; "not necessary slightly improves accuracy", p.2; "to proof the existence", p.5; "Columbic electrostatics", p.8; "insight into into", p.6). Quotes above are verbatim including these

### matic2023gpcrome (4)

- **AlphaFold-Multimer's training cutoff is never stated**, so how many of the 125 benchmark complexes were in AF2 v2.3's training set is unknown and unknowable from this PDF. Every accuracy number is therefore of undetermined memorization status
- **Number of AF seeds / recycles / ensembles is NOT REPORTED**; only "5 models generated for each complex" (p.13). The ×5 totals in `n_predictions` are my arithmetic from the stated protocol, not the paper's numbers
- **Per-complex DockQ values are not in the PDF** (Supplementary Data 5 / Source Data not held), so only the two means and two p-values are available as comparators
- **Fig. 5B-C "n = 12 independent experiments" with SEM ± 0.00** — I read the 12 as the 12 Rosetta multistate-design binding weights (p.14), which are settings of a deterministic protocol rather than independent experiments, but the caption's wording is the paper's and I could not confirm the reading 

### mattsson2026leakage (9)

- **How "similar binding pockets" was determined for Table 3 (p6) is never stated.** The table is the paper's evidence that leakage is not confined to JNK1/JNK2, and the grouping criterion — pocket-residue identity? a structural alignment? expert judgement? — is absent from both the caption and Append
- **Boltz-2 and IsoDDE are never evaluated on the Novelty-Tiered Affinity Benchmark.** The paper establishes a leakage floor (r = 0.14) but reports no co-folding number above it, so the question its own title implies — how much of Boltz-2's 0.66 survives leakage control — is left open. The authors say
- **No hyperparameter search is described** for the ligand-only baselines. Table 5 (p12) fixes d = 2048, d_target = 256, n_hidden = 4 and the schedule (p11) with no sweep, no seed count and no replicate runs. Whether a range was tuned against the FEP+ 4 / OpenFE test sets — the v3 route-4 concern — th
- **The Fig 2 Boltz-2 run has no reported configuration** — templates on/off, MSA depth, seeds, number of samples, which of several poses is shown. It carries no number, but it is the only structural evidence for the "same binding environment" claim
- **The Fig 5 sweep's semantics are ambiguous**: whether each x value is a cutoff applied cumulatively (all pairs below that identity) or a bin is never said. The 0.9 point (≈ 6,100) matches the cumulative reading against Table 1's 6,115, so cumulative is almost certainly right, but it is inferred
- **Distinct target counts are never given** — for the 6,115 correlated pairs, and for the NTAB tiers. Only assay and measurement counts are reported, so the census cannot be read as a statement about how many *proteins* mirror
- **Schema gap: v3 has no field for a proposed protocol or standard.** The splitting procedure is the most reusable content in this paper and had no home; I recorded it as a labelled block in section D alongside `anti_memorization_design`, which is the closest existing field but is scoped to what the 
- **`multi-backbone` judgement call**: Figure 3 puts Boltz-2 and IsoDDE side by side, but the values are quoted from [16] rather than rerun, and two backbones is not "more than two". Not tagged. Flagging in case the corpus wants the tag to cover literature-sourced comparisons
- **`saturating-metric` judgement call**: tagged on the strength of per-assay Pearson r reaching exactly ±1.00 in Fig 7 (p11). The paper's *headline* means never approach the ceiling. If the tag is meant only for a paper's primary reported metric, remove it

### migliorini2026pairsae (8)

- **How many pairformer layers does Boltz-2 have?** Never stated. Layers 33 and 64 cannot be placed as "early/middle/late" from this PDF alone, which weakens any depth-dependence claim. Likewise "third recycling step" — the total number of recycles is never given
- **Feature 1744 or 1774?** p11 text: "we highlight how feature 1744 and 1770 from R3-L33 activate in two ligands in Figure C.8". Fig C.8 caption (p12): "Ligands activating on feature 1770 (left) and feature 1774 (right)."
- **Boltz-2 template setting is never stated** (see `templates`). MSA is explicitly off; templates are simply not mentioned
- **The six Boltz-2 affinity output heads in Fig B.6** (`affinity_pred_value`, `_value1`, `_value2`, `affinity_probability_binary`, `_binary1`, `_binary2`) are never defined, and it is never said which one `AV` / `nAV` in eq. (8) refers to
- **"nAV" is used in every figure axis label but defined nowhere**; from Fig 3's caption ("negative affinity values from Boltz-2 (higher means more affine)") it is the negated affinity value, while eq. (8) writes the target as `AV`. The sign convention is inferable, not stated
- **No code, data or weights availability statement** anywhere in the PDF; no repository URL
- **Venue year conflict**: "NeurIPS 2025" workshop footer (p1) vs arXiv stamp 25 Jun 2026 (p1) and `refs.bib` `year = {2026}`
- **Typo in the body text, quoted [sic] above**: p4, "We speed up training by we computing a Monte Carlo approximation"

### mitjavila2026afsample2t (6)

- **AUC discrepancy for default AF2: 0.54 in the text (p.3) vs 0.55 in the Fig 2A legend (p.3).** Not addressed by the authors. Small, but it is the baseline every reported improvement is measured from
- **Which 4 of the 10 receptors are in AF2's training set is never stated** (p.8), so the training-membership control cannot be reconstructed from the paper even in principle
- **Ensemble arithmetic is not fully closed.** Table 1's AF2 column reports a *range* per receptor for the top-1% models, but 1% of 1,000 is 10 models per receptor per method, and whether the "top 1%" is taken within receptor or pooled across receptors is not stated explicitly (context implies within 
- **Whether the top-1% selection used the same actives/decoys as the reported enrichment, or a held-out ligand split, is not stated.** Reading of p.8 ("all binding-site models are ranked by ligand enrichment and the top-performing 1% are selected") is that it is the same set, i.e. no ligand-side hold-
- **`metric_saturation` and `hides` were still hard to separate for Fig 2A.** The curve genuinely ceilings at 1.0 (numeric → `metric_saturation`) *and* has a reversed, truncated axis (figure → `hides`). v3 fixed the double-recording problem but a reversed axis is neither a break nor a truncation and i
- **`state_metric` still assumes a conformational endpoint.** For this paper the honest answer is "RMSD-to-reference for the secondary structural check + a continuous ligand-ranking coordinate for the primary evaluation, and no state predicate at all". The dual form permitted in v3 made this recordabl

### obendorf2026statespecific (5)

- **Total number of predictions never stated**, and it is not said whether all 5 diffusion samples per condition were analysed or only the selected one. n for Fig 4B/C is not given
- **RF3 in Fig 4B/C legend** despite p15 stating the ligand-pLDDT analysis could not be performed for RF3 (ligand pLDDT fixed at 1.0). Unclear whether RF3 points appear in B only, in both, or in neither
- **Chai-1 and RF3 condition counts** are not stated in the Methods; taken from the figure axis
- **No model training cutoff dates are given** for AF3, Boltz-2, Chai-1 or RF3, so the claim that the benchmark structures are "absent from all model training sets" (p4) cannot be verified from the paper
- **No rule for the state calls.** "Correct active-state conformation", "inactive-like", "hybrid" ICL3 (p12) and Y2018/Y219 "recovered" (pp5, 7) are never operationalised, so no state-recovery rate can be extracted

### paajanen2026activation (7)

- **1010 vs. 1006.** The Methods twice say 1010 structures (pp.8, 10); the training columns of all three Supplementary Tables sum to 1006 (p.22). Four structures are unaccounted for. Separately, the held-out set is 345 by table arithmetic, and the text says eight new structures were discarded (p.10) —
- **The size of the feature set is never stated.** How many generic-numbered positions survived the "present in all structures" intersection — the dimensionality of the PCA input — appears nowhere (Fig. 4, p.9 shows it graphically only). Nor does PC1's own variance fraction, despite Supp. Fig. 3 exist
- **k = 2 in the GMM is asserted, not selected.** No BIC/AIC or likelihood comparison against k = 1 or k = 3 is reported, which matters because "intermediate" states exist in the GPCRdb annotation and were discarded for being too few to see on a graph (p.2), not for being absent
- **The temporal cutoff for the held-out set is "during the training phase" (p.10), never a date.** The split is therefore not reproducible by a third party
- **The Supplementary Information listing on p.11 says "Supplementary Figure 1-6, 1-8"**; only Figs. 1–6 exist in the document. Either two SI figures are missing from this version or the listing is a typo
- **The Supplementary Movie (p.12) is not in the PDF**, and it is the only presentation of the TM6-out/TM7-in interpolation that the paper's second Results section is entirely about (p.5). That section's claims cannot be checked from what we hold
- Minor: the paper's Fig. 2 x-axis is unlabelled for units, and the index sign convention (higher = active) is stated only in prose (p.4), never on the axis

### pandyszekeres2024gproteindb (5)

- **Model count discrepancy: 1,124 vs 1,121.** Methods p.3 says "1124 such models completed at time of writing"; Results p.4 says "structure models of 1121 GPCRs and heterotrimeric G proteins". Both refer to the heterotrimeric primary-transducer set. Not reconcilable from the PDF; both recorded in `me
- **No receptor activation state is assigned or verified for any model, by any criterion.** `state_metric` is NOT REPORTED, and this is informative rather than a reading failure. Downstream papers treating GproteinDb models as active-state structures are supplying an annotation the resource does not c
- **No validation against experimental structures exists.** Not one RMSD, TM-score, DockQ or contact-recovery number against a deposited complex appears in the paper. The only three-way comparison (Fig. 3D, 14/20/26 interface interactions) is a completeness count on a single complex with no ground tru
- **Sampling protocol is NOT REPORTED**: number of AF2M models generated per complex, seeds, recycles, and the selection rule for the released model. Also unstated: whether the 1,205 failing complexes were modelled and discarded or never modelled, and whether the 1,121 heterotrimeric models overlap th
- **AlphaFold2 v2.3.1's training cutoff is never stated**, so the memorization status of the 544 deposited GPCR–G protein complexes that overlap the modelled interactome is unknowable from this PDF. The 1 January 2023 date applies to *templates* only

### passaro2025boltz2 (5)

- **The Boltz-steering hyperparameter tuning set is not identified.** p23 says the Boltz-1x potentials were adopted "with tuned hyperparameters" and never says what they were tuned against. Under v3 route 4 this is potentially leakage; it is unfalsifiable from this PDF
- **Figure 6's middle panel is labelled "FEP+ OpenFE 8 internal targets"** while the text (p9) and Table 11 (p42) describe the OpenFE subset as 876 hit-to-lead measurements. Either the panel label or the text is wrong; I recorded both and did not reconcile them
- **The "1000× faster" claim's denominator shifts.** p1 abstract says "at least 1000× more computationally efficient than FEP"; Table 12 (p42) gives Boltz-2 at 20 GPU sec vs OpenFE at 6–12 GPU hours (≈1000–2000×) and ABFE at >20 GPU hours (≈3600×), while FEP+ has no time entry at all ("-"), so the com
- **v3 ambiguity: `hides` vs `metric_saturation` for a *shared* axis at different scales.** Figure 5 puts five metric groups on one axes where four are scaled 0.50–0.90 and one 0.00–0.35. That is neither a break (rule 9's case) nor numeric saturation. I put it in `hides`. A rule for "shared axis, inco
- **`si_in_scope` has no vocabulary for "SI present but the paper self-declares incomplete".** p40 states outright that template/contact/pocket evaluations are missing and will be added later. That is a different gap from "SI NOT HELD" and I described it in prose

### protenix2025 (4)

- **The number of *structures* behind the 993 and 64 protein-interface cluster counts is never stated**, so `n_predictions` cannot be totalled for the largest benchmark in the paper, and no power comparison against a per-structure benchmark is possible without recuration
- **Protenix's own parameter count is never given.** 386M is stated of AF3 (p13). Whether Protenix has the same count is not confirmed, though the reproduction framing implies it. Do not quote 386M as Protenix's size on the strength of this paper
- **The error bars in Figures 2A, 2C and 2D are never defined** — no caption or text says whether they are 95% CIs, bootstrap intervals, or standard errors, and no bootstrap procedure is described. Any statement about statistical significance drawn from those panels is unsupported by the paper
- **The `hides` field has no way to record "the axis is truncated in five separate figures".** I repeated the observation on each row as v3 requires (`metric_saturation` is numeric only), which is correct but means the note carries the same defect five times. A figure-level `hides` summary line, or a 

### protenix2026v2 (9)

- **Whether the training cutoff changed between versions cannot be resolved from this PDF.** This paper states 2021-09-30 (p2) and says only that it "aligns with established conventions in recent models [8, 28, 34]". It gives no date for [8] or [33]. Anyone needing "did the cutoff move?" must read the
- **FoldBench-AB is printed as "(104/160)"** (Figure 2 panel title, p3) under a caption stating the pair is "(number of entries/number of clusters)". 160 clusters cannot come from 104 entries. The pair is probably transposed, but the paper never corrects it and I have recorded it as printed
- **VEGF-A design count conflicts between figure and text.** Figure 4A (p4) shows "# of Designs = 71" for VEGF-A, while p6 says the ranking study used "approximately 300 designed VHH candidates" for VEGF-A. Either the 71 is a post-filter count or the ~300 includes designs never counted in Figure 4A; t
- **GPCR mAb hit rates conflict between text and figure.** p5 states "the corresponding mAb campaigns reached 0%, 17%, 50%, and 44%", but Figure 1 (p1) badges only three mAb campaigns — GPRC5D 50%, CCR7 **43%**, CCR8 17% — with no CCR5 mAb badge at all. So one value differs by a point (44 vs 43) and t
- **Antigen naming conflict:** Figure 4A (p4) and Figure 1 (p1) label a target **CD226**, while Table 4 (p16) lists the purchased antigen as **CD266** (Sino cat. 10565-H08H). One of the two is a typo and the paper does not reconcile them
- **Self-interaction pass rate is 97.5% in the Figure 5 caption (p6) and 98% in the text (p5)**; polyreactivity is 93.3% vs 93%. Rounding, almost certainly, but recorded because the figure caption is the more precise source
- **Protenix-v2's own MSA and template configuration is never stated.** Only the OF3p2 baseline's is (p14). `templates` and `msa_handling` are therefore NOT REPORTED, and no protocol tag (`templates-on`, `no-template-no-msa`) could be applied to this paper
- **The GPCR antigens carry no novelty filter.** The SAbDab and 30%-identity filters are stated only for the soluble panels (p5); CCR5/CCR7/CCR8/GPRC5D are introduced on difficulty grounds alone. Their relationship to the training set is unstated
- **Figure 3 seed-scaling values are not tabulated**, so the "5 seeds beats 1000 seeds" claim (p2, p4) can be checked only by reading curve positions off the plot

### roehrig2026docking (7)

- **Which AC and which Vina configuration is plotted in Fig 5 and modelled in Tab 2.** Fig 4's caption states AC_norm and Vina exh 100 for its own panels C–F; nothing states it for Fig 5 or Tab 2. This directly affects how the headline comparison should be cited — AC_norm vs AC_long differ by ~4–5 poi
- **Reconciliation of subset sizes.** 2,812 annotated → 2,806 prepared → 2,611 parameterised → 2,597 AC results (878 clusters) → 2,580 six-way docking common → 2,448 AF3-inclusive common; and 919 RNP-F → 891 → 854. The 164-case gap between 2,612 and 2,448 is presumably cases where RNP has no AF3 predi
- **The LDDT-PLI validity check is reported at a different threshold than the one used.** p5 validates that "almost all docking poses with a RMSD below 2 Å have a LDDT-PLI above 0.65", but the success criterion is LDDT-PLI > 0.8. The gap is not addressed; Fig S2 is not in the PDF
- **How many output poses per complex.** AC's *input* pose count is given (3,072 / 12,288) but the retained output count is not, and Vina/Smina/GNINA `num_modes` is never stated. The "all poses ≤ 2 Å" metric is a direct function of this
- **AF3 arm settings.** Number of seeds/samples, MSA depth, template usage, and which AF3 ranking was taken are all inherited silently from RNP (p5) and are unstated here
- **`refs.bib` metadata mismatch**: `@misc{roehrig2026docking, … year = {2025} …}` while the citekey and this posted version are 2026 (posted April 20, 2026). Someone should decide which year the bibliography should carry for a v2 preprint
- **The PDF does not print a version number.** "v2" is an external label; only "this version posted April 20, 2026" and the DOI stem `2025.12.09` are internal evidence

### schafer2025confounds (7)

- **Justification for max-seq = 1, 8, 64 is not in this PDF.** It is the single most important missing item: it determines whether route 4 is per-target tuning on the evaluation set or a principled a priori rule. It would be in Supplementary Methods, which is not held
- **CF-random ensemble sizes for Mad2 and RfaH are not reported** — only run counts (1 and 2). The %Success and MCC bars for those two proteins therefore have no stated n
- **Templates are never mentioned.** Whether ColabFold 1.5.3 ran with its default template search on is undeterminable from this PDF
- **How the single model displayed in each Figure 1b/1c panel was selected** out of hundreds is not stated — by plDDT, by RMSD, or by eye
- **No PDB accession codes** are given for any reference structure, so the reference set cannot be reproduced from the PDF alone
- **The out-of-training-set result is asserted, not shown.** "So does CF-random." (p5) has no supporting number, figure or supplementary pointer anywhere
- **Three inconsistent success thresholds** (3 Å / plDDT 55; 5 Å / plDDT 70; plDDT ≥ 70) are used in the text, Figure 1 and Figure 2 respectively, and the paper never reconciles them or says which governs the headline %Success and MCC numbers

### skrinjar2026generalization (4)

- **Whether the 2 Å / 0.8 success predicate was fixed before or after inspecting Fig 7A.** The justification on p19 is written retrospectively against the joint distribution of all 229,887 predictions. Both thresholds are cited to prior work, and an RMSD-only arm is run, so the conclusion is robust ei
- **The n=673 (Fig 1) vs n=674 (Fig 4) discrepancy** in the 80–100 bin, for what appears to be the same common-subset stratum. One ligand, unexplained
- **RoseTTAFold-All-Atom's version number** is never given (p17 says only "we followed the standard procedure as described in its documentation")
- **Number of distinct proteins in the benchmark.** Systems were clustered to 80% sequence identity for redundancy filtering (p16) but the resulting count is never reported, so "n proteins" cannot be stated — only n systems, n PDB IDs, n proper ligands and n SuCOS-pocket clusters

### stein2022speachaf (4)

- **No Protocol tag fits a no-template, full-MSA regime.** `templates-on` is false, `no-template-no-msa` requires *both* to be absent and the MSA here is full-depth, and `state-annotated-input` is false. A `templates-off` tag is needed. No Protocol tag applied
- **The training-set cutoff is not auditable from this PDF.** The 8/4 partition is inherited verbatim from ref [7] (p6, p9). No cutoff date, no PDB release dates, and no accessions appear in the article; Table A is in the unheld SI. `anti_memorization_design` is recorded as present and genuine, but it
- **LmrP's directed result is quantified only as "mostly".** p11: "These mutations prompted AF2 to generate mostly outward-open conformations that match the experimental structure". No count, no fraction; Fig I is in the unheld SI. The directional-control claim for LmrP therefore has no number attache
- **`n_targets` for a paper with several partly-overlapping target sets.** 16 distinct proteins, but 12 in the benchmark, 14 scored against two references, 2 in the directed arm (one of them a repeat), 1 negative control. A single integer loses the structure; I gave the integer plus the breakdown

### sun2026kinconfbench (5)

- **Supplementary Information is not held.** Tables S1–S4 and Figures S1–S4 carry the exact Top-K accuracies (S3), the 110-system joint-failure list (S4), the label-validity check (S2) and the per-model geometric distributions (S2 figure). Retrieving the SI, or the GitHub repository (https://github.co
- **Exact Top-1 accuracies.** Only the three deltas (+11.4 / +12.6 / +12.1) are printed (p7); the abstract's "∼65-75%" range is the only absolute figure in the main text. The Top-1 values in `metrics_reported` are derived by subtraction from Figure 2b endpoints and are explicitly labelled as such
- **Figure 3's "representative" prediction.** Which of each model's 20 samples is rendered, and by what rule, is not stated (p8)
- **DOI prefix.** The banner reads `10.64898/2026.04.07.716788` rather than bioRxiv's customary `10.1101/...`. Recorded as printed and matching `refs.bib`; not verified
- **Dropped-target count.** p13 excludes "targets that failed annotation because of malformed outputs or missing motifs" without giving n, so the denominator behind the 1,420 → 950 attrition is partly unaccounted

### suzuki2026conforflux (8)

- **Templates are never mentioned.** `templates` is `NOT REPORTED` rather than off. This is a real gap: it means the one input setting that most separates a biasing pipeline from an unbiased one is unstated for the paper's own method and for all nine baselines. `templates-on` and `no-template-no-msa` 
- **`periplasmic-binding` withheld.** The headline example in Fig. 1C is LAO (P02911) and the reproduction target in Fig. 7 is P0205 (RBP), both periplasmic binding proteins, but the paper never uses that category word and files them under "domain motion". Tagging would be my knowledge, not the paper'
- **`rmsd-only` withheld.** All four main-benchmark categories call the state by RMSD or TM to a reference and nothing else, which argues for the tag; but the DAT arm calls the state by four independent Cα mechanism indicators (p23–p24), which is exactly what the tag exists to mark the absence of. Not
- **How the stop fraction (0.8) was chosen is NOT REPORTED.** It appears only as a row in Table 6 (p16), is absent from the Appendix I sensitivity sweep, and no alternative value is reported anywhere in the paper
- **The embedding-target choice is unexplained.** Table 10 (p22) shows the shipped combined s̄ + z̄ update is worse than z̄-only on worst alt-RMSD (3.11 vs 2.17 Å) and worse than s̄-only on clashscore (12.4 vs 9.9). The text records both facts and then says only "We use the combined s̄ + z̄ update." (
- **Whether the 20 within-cutoff EGF pairs affect the Table 1 Transporter comparison asymmetrically is not analysable from the PDF.** All methods are run on all 35, but no within-cutoff / original-15 breakdown is given, so the Transporter row mixes two provenances
- **Total sample counts are never printed** — all totals in `n_predictions` are my arithmetic from per-target counts and target counts
- **Fig. 8's ten series and Figs. 10–14's grids were not rendered**; their `data_shape` rests on appendix text and captions (see `confidence`)

### suzuki2026pairscaling (6)

- **`kinase` tag withheld.** MS15 contains one target the authors file under "Kinases" (adenylate kinase, P69441, Table 2 p10), but adenylate kinase is a nucleotide kinase, not a protein kinase, and the corpus `kinase` tag most likely means the protein-kinase / KLIFS-Kincore sense. Tagging it would pr
- **β increment count.** Table 3 (p11) gives β ∈ {±0.15, …, ±0.75}; the text (p10) says 10 β values with β = 0 excluded, and Fig. 4's legend shows the 10 values plus a "Default" series. The exact grid is therefore ±{0.15, 0.30, 0.45, 0.60, 0.75}; the phrase "in fixed increments" (p9) never names the s
- **AF3 Server template setting NOT REPORTED**, so the one external-reference arm is not template-controlled the way the Boltz-2 arms are (p10)
- **Boltz-2 training cutoff NOT REPORTED**, which is what makes routes R4 and R6 uncheckable rather than merely unaddressed
- **AUC "significance" (p7) has no named test**, unlike the box-plot comparisons which state paired Wilcoxon signed-rank
- Whether "Random" in Fig. 2/3 scatter columns denotes the random-masking arm is inferred from the Methods naming, not stated in the caption

### swapna2025memorization (8)

- **No training-data cutoff is ever defined.** "Available in the PDB at the time of AF2 training" (p6, p11, p13) is used as the paper's independent variable with no date, no PDB release-date filter and no stated membership test. Whether AF3's different cutoff was accounted for when AF3 results are poo
- **Which five proteins occupy the one-state bin of S1 Table** is inferred, not read. The p6 narration gives only counts and one name (SLC19A1); the five names above come from combining p9 and p11 with the group sizes
- **Fig 4 caption contradicts the Results text.** Figure title says ESM-MODELLER; panel B caption says "modeled using ESM-AF2" (p10); p9 says ESM-AF2 failed for Vrg4 and ESM-MODELLER succeeded. One of the three is wrong and the PDF does not resolve it
- **SLC35F3 is named once (p6) and never shown.** It contributes to the n = 3 never-in-training bin but has no figure and no supporting panel in the listed SI
- **No operationalised inward-vs-outward predicate.** Used on all 10 targets, stated nowhere. Recorded as NOT REPORTED in `state_metric`
- **Iterative loop trimming has no stopping rule.** p14: "a few trials were made in the elimination of residues of the loop regions" — how many trials, on which targets, and what counted as an acceptable EC match are all unstated. This is the one place where the evaluation criterion could have shaped 
- **The distant-homologue-template arm for SLC35F2 (p10) has no reported result** beyond the blanket statement that only outward-open was returned; the number of templates, their PDB ids and the seeds used are not given
- **AF_Sample on the flipped sequence has no model count** (p11) — "exclusively inward-open" out of an unstated N. This is the paper's most striking control and its n is missing

### tang2026steeraf (11)

- **The multi-state failure counts do not sum.** p14: "7/18 proteins yielded only one predicted conformation, 7/18 proteins yielded two, and 2/18 proteins yielded three or more" — 7 + 7 + 2 = 16, not 18. Two proteins are unaccounted for. The in-house 18-protein dataset is never named, listed, or inclu
- **The sample ratio 𝜌 has two different "defaults".** Table S1 (p32) gives 𝜌 = 5%; Table 2 (p6) runs 𝜌 ∈ {10%, 5%} in the benchmark; §5.5 (p22) recommends 𝜌 ∈ {5%, 10%}; p16 recommends 𝜌 ≤ 20% for new systems. Any citation of "SteerAF's sample ratio" must say which
- **Error bars in Figure 1B are undefined.** The caption (p4) does not say whether they are SD, SEM or a CI, and no methods section defines them
- **The aggregation statistic in Figures S2 and S7 is never stated** — each point is one number per method per dataset over 15–23 systems, with no mean/median declared and no dispersion drawn
- **Code and data are unavailable**: "will be available upon publication" (p24). The raw per-target numbers, the GPU conversion factors, and the in-house 18-protein dataset are all inside that unreleased release
- **Whether SteerAF was ever run with templates on is untested.** Templates are simply disabled (p17); there is no arm testing whether the distogram's alternative peak survives template conditioning. This matters for anyone applying it to a system with a solved partner state
- **No deposition dates for 68 of 69 systems.** Only A6UVT1's is given (p16). The memorization confound cannot be assessed for the benchmark, which is a real gap given the paper's premise is that AF2 already knows both states
- **A protocol tag for "templates off, full MSA on".** v3 has `no-template-no-msa` and `templates-on` but nothing for this very common regime (p17: templates explicitly not used, deep MSA fully used). Suggest `templates-off`. *(Noted as also requested by the `lee2026confornets` extractor — two indepen
- **A rigour tag for "hyperparameters or sweep ranges tuned on the evaluation set".** v3 folds this into `oracle-leak`, which then reads identically to a paper that fed a deposited target-state structure into the model. Those are very different sins and this paper is a clean example of the milder one 
- **`method_class` has no entry for inference-time tensor optimization** even though the v3 tag list gained `latent-steering`. I wrote `other` plus a description. The B-table list and the tag list have drifted apart and should be reconciled
- **`anti_memorization_design` has no way to express "one incidental system, observed post hoc, used to explain a competitor's success rather than to test our own".** `NONE` understates it and a bare n=1 overstates it. I wrote both plus the quote

### tejero2024opsin (7)

- **The "without the AHD" clause on p12 is grammatically ambiguous** as to whether it modifies JSR1-hGi alone or all three depositions. The body text (p7, p11) supports "JSR1-hGi alone", and that is what the construct table records, but the deposition sentence itself does not settle it. Verifying requ
- **The accession codes appear exactly once in the whole paper** (p12). There is no second occurrence in any figure caption, Methods paragraph or table to cross-check against, so the name→code mapping rests on a single sentence. No contradiction was found; equally, no corroboration exists
- **Which incubation time Fig 1b shows** is not stated. Methods list 30, 60 and 120 min (p11); the figure shows one unlabelled time point
- **The contact-distance criterion behind "31 interactions" vs "18 interactions" and "eight" vs "five" C-hook contacts** (p7) is not given in the main text; it lives in Supplementary Tables 2 and 3, not held. The counts are therefore not reproducible from the held document
- **TM6 outward displacement is never quantified.** This is the most-cited single number for GPCR activation and the paper's comparative claims about it (jsGiq > hGi; JSR1 > bovine rhodopsin) rest entirely on a supplementary figure that is not held
- **Second tag gap, smaller:** there is no publication tag for *version of record with a public peer-review file*. `peer-reviewed` is correct and sufficient; noting only that the peer review file (p13) is a citable object the corpus has no slot for
- **Schema ambiguity in v3, reported bluntly** (see the closing note below)

### tran2026nanogs (5)

- **No scrambled-sequence peptide control.** The negative controls are all *structural* (unstapled, staple moved, substitutions removed) — none is a sequence-scrambled peptide of matched composition and helicity. So "any stapled 15-mer helix of this composition would do" is not formally excluded by th
- **Metadynamics scale not stated in main text**: number of walkers, bias parameters, and aggregate simulation time are not given (only "walker3, cluster 265" appears, p.10). Presumably in SI section 2.3
- **Quantified bimane readouts** (λmax values, shift magnitudes, n per experiment) are entirely in Table S9; the main text never gives a single numerical λmax
- **Why the R380Y peptides (6, 7) are better at D1R than at β2AR** is explicitly unexplained by the authors (p.8)
- **Whether peptide 4 has any intrinsic (agonist-free) activity below 50 μM cannot be determined** — the solubility ceiling and the negative result are confounded (p.9)

### wallner2023afsample (4)

- **The number of benchmark targets is never stated.** "Common CASP15 multimer targets" is the only description (p2). `n_targets`, the per-panel n for Fig 1b, and the total model count in `n_predictions` are all blocked by this single omission
- **The `ranking_confidence > 0.8` triage criterion (p3) is recommended after the CASP15 results were seen**, on the strength of two illustrative targets, one of which (T1187o) shows it failing a third of the time. It did not enter the reported pipeline, so it is not leakage, but it should not be read
- **Typos in the original that a quoting author should know about**: "NIBS-AF2- Multimer" on p2 versus "NBIS-AF2-multimer" everywhere else; "or the if the evolutionary constraints are weak" on p1. Both are quoted verbatim above
- **`controls_run` has no column for a control that was conspicuously *not* run.** The absent dropout-off arm is the most informative thing about this paper's causal claim, and it had to be written as prose beneath the table. A `controls NOT run` companion row-set, or an explicit instruction to note a

### waymentsteele2024cluster (6)

- **Cluster-count inconsistency for KaiB<sub>TE</sub>**: 329 AF-Cluster samples in the MSA-Transformer comparison (p9) vs n = 230 for AF-Cluster sampling in Extended Data Fig. 2e (p14). The paper does not reconcile these, and it is not stated which is the size of the Fig. 1f cloud
- **DBSCAN minimum-cluster-size (*k*) is never given** — the parameter is described (p9) but no value appears anywhere
- **AF2 run settings for the main experiments are unreported**: number of models, recycles and seeds are given only for the G<sub>A</sub>/G<sub>B</sub> arm (p11) and the no-MSA mutation scan (p17), not for KaiB, RfaH, MAD2 or the 628-family screen. Whether templates were enabled is never stated
- **AF2 training cutoff / training-set membership of the reference structures is never discussed** for any validation target
- **The 3 Å state-call threshold is never justified**, and no sensitivity analysis to it is reported
- **Panel counts on pp16–22** were taken from captions; only p23 was rendered. Sub-panel counts for ED Figs 4b (22 strips) and 9 (~1,055 leaves) are read off the render/caption and are approximate

### waymentsteele2025reply (7)

- **Templates are never mentioned** anywhere in the paper (see `templates`). This blocks the `no-template-no-msa` tag for the single-sequence arms, which otherwise fit it
- **Grey "all cluster samples" background layer** in Figs 4D–E, D1 and D2 has no n anywhere in the paper, yet it is the denominator against which the coloured points look localised
- **Dangling pointer**: "see Appendix 1" (p13, p14) has no referent; the figures meant are Appendix B's B1–B3
- **Typo in a figure cross-reference**: "To generate the data in Figure 1c [6],d of this preprint" (p11) appears to mean Figure 1c,d of this preprint, with the "[6]" misplaced
- **Malformed data URL**: `https://github.com/HWaymentSteele/AFCluster/coevolutionary_ ablation_2025` (p12) is missing the underscore used in the repository named elsewhere as `AF_Cluster`; neither repository is held by the corpus
- **Figure B3's per-box n is not stated** and is visibly unequal between the two compared series (see the `hides` cell on row B3)
- **Publication tag is dual and only one was applied.** `preprint` is tagged on the evidence of this PDF; the corpus's own records say this text also exists as a peer-reviewed JMB article, which would warrant `peer-reviewed`. Following the `schafer2025confounds` precedent, only the tag supported by th

### wohlwend2024boltz1 (8)

- **"resolution of at least 9Å" (p3) is almost certainly inverted.** Read literally it admits only structures worse than 9Å, which would exclude essentially the whole PDB. The intended meaning must be "no worse than 9Å" (a very permissive floor, consistent with AlphaFold3). Recorded verbatim as printe
- **CASP15 may intersect the validation set.** CASP15 targets (2022) fall inside the validation date window 2021-09-30 → 2023-01-13 (p4), and the paper never states whether any CASP15 target was in the 553-structure validation set used during development. Not determinable from the PDF
- **How the AlphaFold3 baseline was run is not stated** — server, weights, template usage, MSA substitution — beyond "we also used the same pre-computed MSA's up to 16384 sequences" (p15). Since Boltz-1 runs template-free by design and AlphaFold3 normally uses templates, the template configuration of 
- **The 52 test structures and 10 CASP15 targets dropped for OOM/failure/covalent ligands (p15) are not characterised.** If they are systematically the large or hard ones, every reported number is conditioned on an easier set
- **Tag needed but not available: `templates-off`.** v3 has `templates-on` and `no-template-no-msa` but no tag for the very common regime this paper occupies — full MSA, no templates. `no-template-no-msa` is plainly false here (MSAs are central and deep). So the paper's explicit, quotable "we do not i
- **Control tags withheld** (`ligand-driven`, `partner-driven`, `directed-state`): the architecture conditions on ligands and partners and offers explicit pocket conditioning, but **no experiment in the paper varies an input condition and measures the structural response**, so tagging a control handle
- **Metric tags: both `continuous-metric` and `binary-predicate` applied**, since the five metrics split cleanly into two continuous (LDDT, LDDT-PLI) and three thresholded rates (DockQ > 0.23, RMSD < 2Å, PoseBusters all-pass). `rmsd-only` deliberately withheld: RMSD is one metric of five, not the sole
- **Author-list defect in `refs.bib`:** Regina Barzilay (p1) is missing

### yang2025statespecific (7)

- **APJR peptide count.** Text says "11 peptides that met Filter-2 and were further prioritized using coarse MMGBSA scores were selected for synthesis" (p7) and Fig 4a labels the experiments stage n=11, but Table 1 lists 14 designed peptides of which 12 carry measured values. Whether 11, 12 or 14 were
- **Antagonist design-pool size for APJR** is never given; only the 2400-sequence agonist pool is stated (p7), and "A similar strategy is applied for antagonist design" (p7) is the entire description
- **Whether the design-campaign predictions used the 5-seed protocol.** The 5-seed / 5-model protocol is stated for the benchmark only (p4); §4.3 (p12) does not say how many seeds a candidate is folded with, so the total number of structure predictions is not computable
- **The state filter's threshold.** "a significant RMSD in the state-specific TM domain compared to the expected state" (p2) is the filter that enforces the state in the design pipeline, and its cut point is never given. Likewise the GHSR dWF cut point (p10)
- **Baseline training cutoffs.** Whether AF-Multimer and AF-Multistate had seen any of the 45 post-June-2021 benchmark complexes is never addressed
- **Withheld results.** "In certain instances, we identified peptides with picomolar affinities, although these findings have been omitted here due to commercial conflicts with our partners" (p11) — an unstated number of campaigns and outcomes are not reported, so the reported hit rate is not the comp
- **v3 ambiguity — see the schema note below.**

### ye2026multistatebias (4)

- **Colour key inconsistency in Fig 4.** The caption (p.12) assigns "Gαβγ-agonist-GTP (green)" and "apo (orange)"; the rendered legend shows purple and orange respectively, and the text (p.13) calls apo "yellow dots" and the partner series "(blue, purple)". The mapping is recoverable from the legend b
- **BioEmu's condition coverage is never stated.** BioEmu appears with only the apo series in Figs 3B and 4B, and only apo numbers are quoted for it (pp.10, 13). The paper never states that BioEmu accepts no ligand or partner input; it must be inferred from the figures
- **Sample counts.** n = 50 per arm is stated only twice (pp.8, 10) and n = 20 once for a BioEmu β2AR cluster (p.12). Whether 50 is the universal per-arm sample size, and what the totals are, is deferred to the SI (p.18) and Zenodo (p.20), neither of which is in this PDF
- **TM-score values.** TM-align was run "to confirm global fold preservation" (p.18) but no TM-score is reported anywhere in the main text

### zhang2026generalization (9)

- **Top-1 success 37.15% (p2) vs "Boltz succeeded in 114/253 (45.06%)" (p3)** — both are success at 2.5 Å on the same 253 cases and they disagree by ~8 points. Probably top-1-ranked *pose* vs top-*scored model*, but the paper never says. Do not quote both in one sentence without resolving
- **Templates** — whether Boltz was run with structural templates on or off is never stated (p5). This matters for the leakage argument and is unrecoverable from the PDF; the GitHub repo (p6) would settle it
- **Boltz-2 sampling depth** — "we re-ran the entire benchmark dataset with Boltz-2" (p3) without stating samples per complex or whether the 5-sample / 10-recycle setting carried over. No total prediction count is derivable for that arm
- **"Best Boltz model" and "best IFD-MD models"** (Fig. 3, p5) — the selection criterion is stated as "at least one pose with ligand RMSD < 2.5 Å that also passed FEP+ validation" (p4), but whether the *plotted* bar is the best-by-R², best-by-RMSE or best-by-RMSD model is not stated, and the three nee
- **"i-values of 0.066 and 0.029"** (p5) — from context these are Wilcoxon p-values, but the text says "i-values". Recorded verbatim above; treat as p-values with a caveat
- **Allosteric n** — the number of allosteric-ligand cases among the 253 is never stated, although they are highlighted in red in Fig. 1b–d and carry a headline failure claim (p2)
- **Which 55 cases are wrong-pocket, and how many of those are the allosteric ones** — not stated; needs Table S2 (not held)
- **The 27 → 14 series identities** and every per-series number are in Table S1 (not held)
- **Second tag gap:** there is no tag for **model-version comparison / memorization-by-version** (Boltz-1x vs Boltz-2 split by training-set membership). `multi-backbone` is wrong — it is one backbone, two versions — and `anti-memorization` covers the design but not the version-comparison design that m
