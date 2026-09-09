# richman2025conformix

> **Extraction provenance.** Extracted 2026-09-08 from the arXiv v2 PDF (`arXiv:2512.03312v2`,
> submitted 4 Feb 2026), obtained during this session. Read in full for Sections 1–5 and the
> Appendix A dataset definitions; figure panels were enumerated mechanically by page and read
> from captions rather than viewed. Where a field could not be settled from the text that was
> read, it says so rather than guessing. See `confidence` and `unresolved`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `richman2025conformix` |
| `doi` | arXiv:2512.03312 (v1 2 Dec 2025, v2 4 Feb 2026) |
| `year`, `venue` | 2025 — **NeurIPS 2025**, peer-reviewed conference paper. The footer states "39th Conference on Neural Information Processing Systems (NeurIPS 2025)." (p1). Tag `peer-reviewed`, not `preprint`: the arXiv posting is the camera-ready of an accepted paper. |
| `title` | Unlocking hidden biomolecular conformational landscapes in diffusion models at inference time |
| `authors` | Daniel D. Richman\*, Jessica Karaguesian\*, Carl-Mikael Suomivuori†, Ron O. Dror (Stanford; \*equal contribution; †present affiliation Yale School of Medicine) |

**Why this paper was a corpus blind spot.** ConforMix is used as a named baseline by
`lee2026confornets` ("competitive diversity-maximizing baselines such as ConforMix and
AFsample3") and sits adjacent to `suzuki2026conforflux`. It was cited *through* other corpus
papers for eleven months without ever being read. That is exactly the failure mode
`litquery`'s staleness check exists to prevent.

## B. Scope

| field | value |
|---|---|
| `system` | **general protein.** Four categories: domain motion, membrane transporter cycling, cryptic pocket formation, fold switching. **No GPCR and no protein kinase appears in any benchmark set or case study.** GPCRs enter only through the reference list (del Alamo 2022, Chiesa 2025, Heo & Feig 2022 are cited in Related Work). |
| `n_targets` | **99 benchmark proteins**, plus case studies. Domain motion **38** ("the non-overlapping set of 22 domain motion proteins curated by [17] and 23 open-closed (OC23) conformation proteins curated by [13]", Appendix A); membrane transporters **15** ("15 proteins from the transporter protein set (TP16)… One protein, SPF1, was excluded for compute considerations", Appendix A); cryptic pockets **31** in Table 1, described in Appendix A as "33 proteins… One protein, Q16539, was excluded"; fold switching **15**. Case studies: SemiSWEET sugar transporter (p9), plus a barnase/barstar motivating example (p1, not run). |
| `method_class` | **other — inference-time enhanced sampling on a frozen co-folding model.** Twisted sequential Monte Carlo (a particle filter) with classifier-style guidance potentials, physical-plausibility filtering, and optional MBAR reweighting for free-energy estimation. "We emphasize that ConforMix itself does not involve additional model training." (p3). Nearest fixed tags: `enhanced-sampling` + `cofolding`. |
| `backbones` | **Boltz-1** (primary, "ConforMixRMSD-Boltz"), **BioEmu** (second implementation, free-energy arm). Comparators implemented inside Boltz: AFCluster, AFsample2, CF-random, and default Boltz at 1,000 samples. Head-to-head across two generative backbones → tag `multi-backbone`. |
| `templates` | **NOT REPORTED.** Boltz-1 default inputs are used; the template setting is never stated. Do not assume either way. |
| `msa_handling` | **full** for the method itself (default inputs, p6). MSA clustering/subsampling appears only in the three comparator arms, which are reimplementations of other people's protocols, not part of ConforMix. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **ensemble + continuum.** The method produces a sampled distribution along continuous bias coordinates and estimates free energies over it, rather than two discrete endpoints. The baseline it improves on is single-state: default Boltz samples "are generally highly concentrated and are more usefully thought of as multiple approximations of the same static structure than as samples from the true conformational distribution" (p6). |
| `structural_priors_used` | **Substantial, and all at benchmark-construction time.** Every one of the four sets is imported from prior work and consists of proteins with two or more deposited conformations: Lewis et al. (BioEmu) for domain motion and cryptic pockets, Kalakoti et al. OC23 and TP16 for open/closed and transporters, Porter et al. for fold switchers (Appendix A). The cryptic-pocket RMSD is computed over "the cryptic pocket region defined by [17]" (Appendix A), so even the evaluation region is inherited. No deposited structure enters the *pipeline*; the priors are in what was chosen to test. |
| `oracle_leakage` | **Seven routes, each answered separately.**<br><br>**Route 1 — structures as input or template: NONE FOUND, and this is the paper's central methodological claim.** The `ConforMixRMSD` potential biases on deviation from *the model's own default prediction*, not from a deposited structure. Verbatim, p1 abstract: "to enable more efficient discovery of conformational variability **without requiring prior knowledge of major degrees of freedom**." And p2, contributions, positioning against prior art: "ConforMix-Boltz generates realistic and diverse conformations for a variety of proteins, without prior knowledge of important degrees of freedom. **In prior work, conditional sampling on biomolecular diffusion models has required additional input information, such as experimentally measured pairwise distances.**" Protocol described pp3–5.<br><br>**Route 2 — state annotations from a curated state database (GPCRdb / KLIFS / Kincore): NONE FOUND.** No curated state database is used anywhere. Sets are imported from prior benchmark papers, not from a state-annotation resource. Protocol: Appendix A.<br><br>**Route 3 — cluster labels derived from known states: NONE FOUND at inference.** The benchmark *sets* are state-labelled by construction (two deposited conformations per target), but no state label enters the sampler. Recorded under `structural_priors_used`.<br><br>**Route 4 — hyperparameters / sweep ranges tuned against known states: PARTIAL, and NOT FULLY DETERMINED.** The guidance potential carries a strength parameter α and a target-distance schedule λ_j ∈ [λ_min, λ_max] (Eq. 1, p3). How λ_min and λ_max are chosen, and whether the range was set by looking at benchmark performance, is **not stated in the main text that was read**. This is the one route where the paper could leak and the note cannot yet say. Flagged in `unresolved`.<br><br>**Route 5 — success defined post hoc by RMSD/TM to a held structure: PRESENT, definitionally.** Table 1's coverage metric is fraction of proteins with samples matching a deposited reference, "as measured by RMSD and TM-scores to PDB structures" (p6). Intrinsic to a retrospective benchmark and stated openly.<br><br>**Route 6 — best/worst model labels assigned against a held reference: PRESENT.** Figure 2 caption, p6: "Right: reference structures and **the closest structure generated by each sampling approach (lowest RMSD)**." Table 1 is explicitly split into "Worst-matched reference conformation (harder task)" and "Best-matched reference conformation (easier task)", i.e. both rows are oracle-selected against deposited structures.<br><br>**Route 7 — design-level oracle use: PRESENT, and labelled design-level.** All 99 targets were selected because two or more conformations are already deposited (Appendix A). The expected answer is known before any sample is read. Unavoidable for the question asked; weaker than pipeline leakage and must not be conflated with it. |
| `prospective` | **no.** Every target has its answer deposited, every metric is scored against that answer, and no prediction is made about a system whose alternative state is unknown. Prospective in neither targets nor evaluation. |
| `state_metric` | **RMSD-to-reference + continuous coordinate + binary predicate** (triple, and the schema's dual join is insufficient here). Continuous: Cα RMSD to each deposited reference, TM-score (Fig S4, p24), and the fill-ratio metric imported from Kalakoti et al. (Fig S5, p25). Binary: "coverage", the fraction of proteins with a sample matching a reference (Table 1, p6; Fig S1, p20). **The matching threshold behind "coverage" is NOT REPORTED in the text read** — flagged in `unresolved`. Principal-component projections of internal atomic distances are used as a qualitative state readout (Fig 3, p8; Fig S3, p22; Fig S11, pp32–37). |
| `metric_saturation` | **Yes, numerically, and it matters for how Table 1 should be read.** The "Best-matched reference conformation (easier task)" row is at ceiling for two of four datasets across *every* method including the unguided baseline: domain motion 0.87–0.97 with default Boltz already at 0.94, cryptic pockets 0.93–0.97 with default Boltz already at 0.94 (Table 1, p6). On those two datasets the easy row cannot separate methods at all, and the entire reported advantage lives in the worst-matched row (0.33 → 0.69 domain motion, 0.15 → 0.45 cryptic pockets). Anyone quoting a single ConforMix number must say which row it came from. |
| `directional_control` | **Partial, and the distinction is the useful part for us.** The *framework* accepts an arbitrary user-supplied potential, so a direction can in principle be specified: Eq. 1 (p3) is a distance restraint between two atom-group centroids, and the authors note "users can supply more informative biasing potentials, perhaps based on experimental evidence" (p10). But the *instantiation benchmarked throughout*, `ConforMixRMSD`, is **undirected**: it biases away from the model's own default prediction and explores whatever degrees of freedom the landscape offers. Handle: an operator-supplied scalar bias potential. There is no biological co-input handle anywhere in this paper — no ligand arm, no partner arm, no peptide arm. |
| `anti_memorization_design` | **NONE.** No temporal cutoff, no held-out split, no post-cutoff set, no sequence-identity stratification. The paper instead makes the opposite admission explicitly, p6: "we note that **many of the evaluated proteins were held out of training for BioEmu but were likely present in the Boltz training set**." |
| `anti_memorization_control` | **NONE RUN.** With no design there is no arm. The BioEmu comparison (Fig S2, p21) is a cross-model comparison confounded in the direction the authors themselves name in the sentence above, and is not framed or analysed as a memorization control. |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **Used, but for physical plausibility only, and never validated as a state discriminator.** p5: "we reject samples where any 10-residue sliding window has an average pLDDT value of more than 20% below that of the default prediction, as well as structures with clashes. The sliding window approach detects local non-physical perturbations from sampling beyond the protein's flexibility range" Figure S6 (p26) reports that this filter "rejects more samples as structure generation is biased further away from the default", i.e. confidence falls monotonically with the amount of steering. No claim is made, or tested, that pLDDT distinguishes a correct conformational state from an incorrect one. |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| Default Boltz sampling, 1,000 samples | that the gain is just more compute at the same sampler | p6, Table 1 |
| AFCluster-Boltz | that MSA clustering already achieves it | p6, Table 1 |
| CF-random-Boltz | that random shallow-MSA subsampling already achieves it | p6, Table 1 |
| AFsample2-Boltz | that MSA column masking already achieves it | p6, Table 1 |
| BioEmu comparison | that a purpose-trained ensemble model is strictly better | Fig S2, p21 |
| pLDDT sliding-window + clash filter | that the new states are unphysical artefacts of guidance | p5; Fig S6, p26 |
| Fold-switching set (method loses here) | over-claiming generality; the authors report their own negative | p6 |
| **Absent:** any memorization / post-cutoff arm | — | — |
| **Absent:** any receptor, kinase or biological co-input arm | — | — |

## D. Claims

- **`central_conclusion`**: Twisted sequential Monte Carlo, applied at inference time to a frozen
  AF3-lineage diffusion model, recovers deposited alternative conformations that the model's
  default sampling never reaches, without needing to be told which degree of freedom to move.
  On domain motion, transporter and cryptic-pocket sets it beats default sampling and all three
  MSA-manipulation baselines on the hard (worst-matched) coverage metric; on fold switchers it
  loses to MSA methods. Implemented in BioEmu it also speeds up free-energy estimation. The
  method is orthogonal to model training and would still be useful for a model that sampled the
  Boltzmann distribution exactly.

- **`necessity_claims`** (verbatim + page):
  - p1 (abstract): "ConforMix is orthogonal to improvements in model pretraining and **would
    benefit even a hypothetical model that perfectly reproduced the Boltzmann distribution**."
  - p1: "these methods are typically **extremely slow and suffer from accuracy problems**"
    (on Monte Carlo and MD).
  - p2: "Subsampling methods, however, **suffer from fundamental limitations**. First,
    subsampling necessarily involves reducing the information available to the model, which
    often produces poor-quality outputs. Second, molecular conformations are continuous, while
    subsampling of sequences or templates is a discrete operation. Third, the structure
    distribution accessed by subsampling methods is not well defined, and **despite years of
    study there is no clear means of reconstructing actual probabilistic ensembles**."
  - p2: "While these approaches have shown promise, they **do not yet accurately reproduce the
    thermodynamic ensembles of arbitrary proteins**." (on models trained on MD or experimental
    data)
  - p2 (on AF3-family default sampling): "While AlphaFold 3 generates five samples per run, for
    well-ordered proteins these samples are often almost identical and are **better understood as
    very similar predictions of the same static structure rather than a representation of
    conformational variety**."
  - p10: "The primary limitation of ConforMix, like other enhanced sampling methods, is that it
    **depends on the robustness and utility of the underlying energy landscape it samples**."

- **`novelty_claims`** (verbatim + page):
  - p2: "A **novel** algorithm combining twisted sequential Monte Carlo, which performs
    asymptotically exact sampling of conditional distributions, with an automated procedure for
    exploring the diffusion landscape, using conditional sampling as a subroutine. Optionally, a
    statistically optimal sample reweighting algorithm, **applied to diffusion models for the
    first time**, can be used to reconstruct the unconditional distribution from the conditional
    samples."
  - p2: "ConforMix-Boltz generates realistic and diverse conformations for a variety of proteins,
    without prior knowledge of important degrees of freedom. **In prior work, conditional sampling
    on biomolecular diffusion models has required additional input information, such as
    experimentally measured pairwise distances.**"
  - p6: "ConforMixRMSD recovers more alternate conformations than all baselines… **demonstrating
    its power explore conformational space in a novel manner**." (sic, verb omitted in the
    original)
  - p1 (abstract): "**Remarkably**, when applied to a diffusion model trained for static structure
    prediction, ConforMix captures structural changes including domain motion, cryptic pocket
    flexibility, and transporter cycling, while avoiding unphysical states."

- **`stated_limits`** (verbatim + page, p10 unless noted):
  - "The primary limitation of ConforMix, like other enhanced sampling methods, is that it depends
    on the robustness and utility of the underlying energy landscape it samples."
  - "ConforMix sampling enables us to identify major missing states: known experimental
    conformations that do not exist with realistic probabilities in the Boltz probability
    distribution."
  - "Other limitations include potential systematic errors due to the inexact sampling of twisted
    diffusion in the non-asymptotic regime and the statistical uncertainty associated with MBAR."
  - p6, the memorization admission: "many of the evaluated proteins were held out of training for
    BioEmu but were likely present in the Boltz training set."
  - p6, their own negative result: "MSA-based methods show stronger performance on fold switchers,
    suggesting such rearrangements are be better captured discrete input modulation, whereas
    ConforMixRMSD is better suited to continuous (e.g. domain, transporter, pocket) transitions."
    (sic)
  - p10: "If desired, ConforMix can be used in combination with input-modification approaches such
    as MSA subsampling, although we leave that exploration to future work."

- **`stance`**: `precedent + contrast` — **provisional, the user's call.**
  - *Precedent*: the strongest published demonstration that an AF3-lineage model's landscape
    already contains alternative states reachable at inference time with no reference structure.
    Its route-1 answer is cleaner than any other steering paper in the corpus.
  - *Contrast*: no receptor, no kinase, no biological co-input, no memorization control, and both
    coverage rows oracle-selected. **It does not threaten a GPCR-activation claim**, and its own
    exclusion of receptors puts it alongside `ku2026promise` and `suzuki2026conforflux` as a third
    strong multi-state method whose benchmark omits GPCR activation.

## E. Quantitative comparators

### `metrics_reported`

Table 1 (p6), coverage = fraction of proteins with samples matching a deposited reference.
Mean (± s.d.) across targets. Two rows per method: worst-matched (hard) and best-matched (easy).

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Coverage, worst-matched, domain motion (n=38) | 0.69 (±0.15) | fraction | deposited references, RMSD/TM | p6 |
| Coverage, worst-matched, domain motion — default Boltz | 0.33 (±0.14) | fraction | same | p6 |
| Coverage, worst-matched, domain motion — best MSA baseline (CF-random) | 0.51 (±0.17) | fraction | same | p6 |
| Coverage, worst-matched, transporters (n=15) | 0.33 (±0.23) | fraction | same | p6 |
| Coverage, worst-matched, transporters — default Boltz | 0.13 (±0.17) | fraction | same | p6 |
| Coverage, worst-matched, cryptic pockets (n=31) | 0.45 (±0.18) | fraction | same | p6 |
| Coverage, worst-matched, cryptic pockets — default Boltz | 0.15 (±0.12) | fraction | same | p6 |
| Coverage, worst-matched, fold switching (n=15) | 0.13 (±0.17) | fraction | same | p6 |
| Coverage, worst-matched, fold switching — best baseline (AFCluster) | 0.27 (±0.23) | fraction | same | p6 |
| Coverage, best-matched, domain motion | 0.97 (±0.04) | fraction | same | p6 |
| Coverage, best-matched, transporters | 0.79 (±0.19) | fraction | same | p6 |
| Coverage, best-matched, cryptic pockets | 0.94 (±0.08) | fraction | same | p6 |
| Coverage, best-matched, fold switching | **NOT REPORTED in the extracted text layer** (row truncated) | — | — | p6 |

**Read this table with the saturation note in `metric_saturation`.** On domain motion and
cryptic pockets the best-matched row is at ceiling for every method, default sampling included.

- **`n_predictions`**: **Samples per target:** 1,000 for the default-Boltz comparator (p6);
  ConforMix particle count and sample budget **NOT REPORTED in the text read** (see `unresolved`).
  **Targets:** 99 across four sets. **Total:** NOT REPORTED.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI is held** — the arXiv PDF carries Appendix A–E and Figures S1–S11
  (pp20–37) in the same file. Nothing material is in an external supplement.

## F. Figures

Enumerated mechanically by page from the v2 PDF. `plot_type` and `data_shape` are given where
the caption determines them and are marked `NOT EXTRACTED (panel not viewed)` where it does not.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1A-B | 3 | ConforMix adds conditioning to diffusion structure prediction; workflow overview | schematic | `SCHEMATIC \| method workflow from default inputs through bias potentials to conditional samples \| no data` | 2 (A, B) | — | arXiv; licence NOT REPORTED on the PDF, treat as arXiv non-exclusive |
| 2A-B | 6 | Sampling density relative to references, and PC projection, for one domain-motion protein and one transporter | density plot + scatter | `PLOT \| facet: system (2: domain motion, transporter) × view (2: density, PC projection) \| vary: RMSD to reference / PC1 (continuous) \| series: method (5) \| measure: sample density \| n: NOT REPORTED per panel` | 2 groups | Shows one exemplar per category; the per-target spread lives in Figs S7–S10 | as above |
| 2 (right) | 6 | Reference structures and the lowest-RMSD generated structure per method | structure render | `RENDER \| facet: method (5) \| views: 1 \| overlay: 1 selected prediction on 1 reference \| axis: none` | 1 | **Oracle display: shows "the closest structure generated by each sampling approach (lowest RMSD)"**, so it cannot show typical output | as above |
| 3A-B | 8 | PCA of sampled structures for dppA; direction-of-motion agreement across the domain-motion set | scatter + summary | `PLOT \| facet: none (1) \| vary: PC1 (continuous) \| series: method (5) \| measure: PC2 \| n: NOT REPORTED` | 2 (A, B) | — | as above |
| 4A | 9 | SemiSWEET transporter: recovery of all three deposited conformations | structure render + density | `RENDER \| facet: conformation (3) \| views: 1 \| overlay: NOT REPORTED predictions on 3 references \| axis: none` | ≥1 | Single case study | as above |
| 5 | 10 | Free-energy convergence in BioEmu, ConforMix vs default | line | `PLOT \| facet: none (1) \| vary: compute or sample count (continuous) \| series: method (2) \| measure: free-energy estimate \| n: NOT REPORTED` | ≥1 | — | as above |
| S1 | 20 | Coverage across methods and datasets | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| S2 | 21 | Coverage compared against BioEmu | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | Confounded by the training-overlap admission on p6 | as above |
| S3 | 22 | PCA of the domain-motion set, extended benchmarks | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| S4 | 23 | TM-score analysis across methods and datasets | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| S5 | 24 | Fill-ratio analysis across methods and datasets | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| S6 | 26 | pLDDT sliding-window filter rejects more samples as bias increases | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | **The most reusable negative panel in the paper**: it quantifies the confidence cost of steering | as above |
| S7 | 26–27 | Per-target sampling density, domain-motion set | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | grid of small multiples | — | as above |
| S8 | 28 | Per-target sampling density, transporter set | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | grid of small multiples | — | as above |
| S9 | 29–30 | Per-target sampling density, cryptic-pocket set | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | grid of small multiples | — | as above |
| S10 | 31 | Per-target sampling density, fold-switching set | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | grid of small multiples | — | as above |
| S11 | 32–37 | PCA per domain-motion protein | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | grid of small multiples, 6 pages | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-08
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium.** High on identity, venue, benchmark construction, Table 1, the
  oracle routes 1/5/6/7, the memorization admission and the stated limits, all read directly from
  the PDF text layer. **Low on the figure table below Figure 5** — supplementary panels were
  located by page and caption but not viewed, and are marked as such rather than guessed. Also
  low on sampling budget and the coverage threshold, which were not found in the text read.
- **`unresolved`**:
  1. **The coverage matching threshold.** Table 1 reports "fraction of proteins with samples
     matching a reference" and the cut-off for "matching" was not located. Without it the
     headline numbers are not reproducible.
  2. **ConforMix particle count and total sample budget.** Only the 1,000-sample default-Boltz
     comparator figure was found.
  3. **Oracle route 4.** How λ_min, λ_max and α (Eq. 1, p3) are chosen, and whether that range was
     set by looking at benchmark performance. This is the one route that could still make the
     paper leakier than recorded above.
  4. **An internal inconsistency in dataset attribution.** The main text (p6) attributes TP16 to
     "Xie & Huang [39]"; Appendix A attributes the same 15 transporters to "[13]" (Kalakoti).
     Both may be right (TP16 originating with Xie & Huang, re-curated by Kalakoti) but the paper
     does not say.
  5. **A cryptic-pocket count mismatch**: Table 1 header says n=31, Appendix A says 33 curated
     minus 1 excluded = 32. One protein is unaccounted for.
  6. **Templates setting for Boltz-1** never stated.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
general-protein transporter fold-switching cryptic-pocket cofolding enhanced-sampling
md-emulator msa-subsample af-cluster ensemble continuum rmsd-only continuous-metric
binary-predicate saturating-metric design-level-oracle oracle-leak no-anti-memorization
multi-backbone directed-state confidence-as-discriminator peer-reviewed precedent contrast
comparator-numbers
```

**Tag notes, so the choices are auditable.**
- `latent-steering` **deliberately NOT applied.** The intervention is on coordinates via a
  potential on the denoised estimate x̂₀, plus resampling of particles. It never touches the
  trunk, pair or single representations. Applying `latent-steering` here would false-positive
  every query for internal-tensor intervention.
- `gpcr` and `kinase` **deliberately NOT applied.** Neither appears in any benchmark set or case
  study. GPCRs are cited in Related Work only.
- `md-emulator` applied because BioEmu is one of the two backbones the method is implemented in.
- `directed-state` applied to the *framework* (an arbitrary potential can encode a direction),
  with the caveat recorded in `directional_control` that the benchmarked instantiation is
  undirected. If a future query needs "methods that can be told which state to produce", read
  the field, not the tag.
- `oracle-leak` **and** `design-level-oracle` both applied: routes 5 and 6 are pipeline-side
  evaluation leaks, route 7 is design-level.
- `peer-reviewed`, not `preprint`: NeurIPS 2025 acceptance, verified on OpenReview and stated in
  the PDF footer (p1).
