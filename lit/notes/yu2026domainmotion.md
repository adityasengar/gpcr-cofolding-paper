# yu2026domainmotion

> **PDF SUPPLIED 2026-09-14 and now held at `pdfs/yu2026domainmotion.pdf` (10 pp).**
> This note was extracted from publisher HTML because every scripted route to the PDF was
> bot-walled, so **its locators are SECTION NAMES, not pages** — cite as
> `[yu2026domainmotion, Discussion]` until a re-pass converts them. **A page-number re-pass is
> now possible and is owed**; it matters because this is a threats-table paper and its numbers
> (the 40.3% training-composition gap against the 9.1–17.5% ligand effect) will be argued
> against. **The SI Appendix, which carries every significance test behind those numbers, is
> still not held.**


> **Extraction provenance, and a locator caveat that applies to this whole note.** Extracted
> 2026-09-09 from the **publisher HTML full text** at pnas.org (FREE ACCESS), read through the
> browser because every scripted route to the PDF is bot-walled. **There is no PDF in
> `pdfs/`, so this note carries SECTION locators, not page numbers.** Every quote below is
> verbatim and searchable in the article text; cite as `[yu2026domainmotion, Discussion]` rather
> than inventing a page. Abstract, Significance, Results, Discussion and Methods were all
> retrieved in full. The SI Appendix (23.93 MB) was **not** retrieved, and most per-protein
> numbers live there. See `si_in_scope` and `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `yu2026domainmotion` |
| `doi` | 10.1073/pnas.2530709123 |
| `year`, `venue` | 2026 — **PNAS 123(10):e2530709123**, peer-reviewed. Received 26 Oct 2025, accepted 4 Feb 2026, published online 4 Mar 2026, in issue 10 Mar 2026. Edited by G. Marius Clore. |
| `title` | Bias in the AlphaFold3 prediction of ligand-induced domain motion in enzymes |
| `authors` | Hao Yu, Ayse A. Bekar-Cesaretli, Maria Lazou, Dima Kozakov, Diane Joseph-McCarthy, Sandor Vajda (Boston University; Kozakov at Stony Brook) |

**Relation to the corpus.** Same group as `lazou2026cryptic` (Maria Lazou is an author on both),
and the natural companion to it: `lazou2026cryptic` reports that a cognate ligand opens a cryptic
pocket, while this paper reports that a **non-binding** ligand opens an enzyme domain just as well.
Read the two together or the ligand-as-handle story comes out one-sided.

## B. Scope

| field | value |
|---|---|
| `system` | **general protein — enzymes with open/closed domain motion.** No GPCR, no receptor. Domains and trigger ligands taken from the DynDom database. |
| `n_targets` | **82 enzymes**, partitioned by their apo:holo ratio in the PDB: **Group 1** = 19 proteins with more apo than holo structures; **Group 2** = 25 with more holo than apo; **Group 3** = 38 with five or fewer structures, or exactly equal numbers. Twelve are discussed in detail (Table 1). |
| `method_class` | **benchmark-only**, adversarial in design. Two matched arms (no ligand, trigger ligand) plus a third non-binder arm, stratified by training-set composition. |
| `backbones` | **AF3** primary, default model parameters. **AF2** run as a confirmation arm on Group 2. |
| `templates` | **off, explicitly.** Methods: "We used 100 random seeds to generate 500 models for every set of input with **no template structure**." |
| `msa_handling` | **full.** "MSAs were generated for all protein sequences using MMseqs2 (Release 18) against the BFD/MGnify3 and Uniclust3052 databases, using the default search parameters." (Methods) |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **ensemble + two-state.** 500 models per input condition, plotted as a distribution in a 2-D RMSD-to-apo vs RMSD-to-holo coordinate system, then assigned to the nearer reference. Not a collapse: the ensembles are genuinely spread, and the finding is about where the mass sits. |
| `structural_priors_used` | **Heavy, all at design time and all disclosed.** Domains, trigger ligands and reference apo/holo pairs come from the DynDom database; the apo:holo counts that define the three groups are read off the PDB. Every target was chosen because both states are deposited. This is what the study is *about*, so it is a prior rather than a leak. |
| `oracle_leakage` | **Seven routes, each answered separately.**<br><br>**Route 1 — structures as input or template: NONE FOUND, and it is stated in the Methods.** Templates are off; input is sequence + MSA (+ ligand SMILES in the ligand arms).<br><br>**Route 2 — curated state database driving templates or alignments: NONE FOUND for the pipeline.** DynDom supplies the *evaluation* definitions (domains, trigger ligand, reference pair), never an input.<br><br>**Route 3 — cluster labels from known states: NONE FOUND at inference.** The apo/holo grouping is applied after the models are generated.<br><br>**Route 4 — hyperparameters tuned against known states: NONE FOUND.** AF3 default parameters, a fixed 100-seed / 500-model budget applied uniformly to every protein and every arm. This is unusually clean for the corpus and is worth noting when citing them.<br><br>**Route 5 — success defined post hoc by RMSD to a held structure: PRESENT, definitionally.** Every model is scored by RMSD (and TM-score) to the deposited apo and holo references after aligning the fixed domain. Openly stated in Results.<br><br>**Route 6 — best/worst model labels against a held reference: NONE FOUND.** Distributions of all 500 models are reported, not a best-of-N. This is the reason the paper's numbers are worth more than most in the corpus.<br><br>**Route 7 — design-level oracle: PRESENT.** All 82 proteins were selected because both conformations are deposited, and the expected answer is declared before any model is read. Design-level, unavoidable for the question, and must not be conflated with pipeline leakage. |
| `prospective` | **no.** Retrospective by construction. Every reference structure and every apo:holo count predates the predictions. |
| `state_metric` | **RMSD-to-reference + continuous coordinate** (dual, and reported both ways). Each model is placed in a 2-D system of RMSD-to-apo-reference against RMSD-to-holo-reference, computed **after aligning the fixed domain**, which is the methodological point: a global RMSD would not resolve a domain hinge. A **TM-score** replication of the entire analysis is reported in SI Fig. S1 / Table S3 and reaches the same conclusion. **The assignment rule is nearest-reference; no threshold is imposed**, so there is no arbitrary cutoff to argue about. |
| `metric_saturation` | **No numeric saturation.** Fractions reported are 42% to 80%, mid-range throughout; the 2-D scatter shows the full distribution rather than a summary statistic. The one boundary effect is that clusters of apo and holo X-ray structures "may even overlap for some of the proteins" (Results), which compresses the coordinate for those targets; the authors check this and report that "the average pairwise RMSD between apo and holo structures is always larger than the average pairwise RMSDs within the group of apo and holo structures" (Results). |
| `directional_control` | **The ligand is the intended handle, and the finding is that it barely works.** Adding the trigger ligand raises the holo-like fraction by only **11.9%** in Group 1 and **9.1%** in Group 2, against a **40.3%** difference between those two groups attributable to training-set composition alone (Discussion). In Group 3, where the PDB contains few structures and the memorised prior is weak, the ligand's effect is larger at **17.5%**. So the handle works where the model does not already know the answer, and is swamped where it does. |
| `input_factor_design` | **New in v3.2. MSA HELD, but LIGAND x TRAINING-COMPOSITION genuinely crossed — the sharpest control in the corpus for a ligand-as-handle claim.** **MSA**: full MMseqs2, **constant across all arms**. **templates**: off, explicitly — "no template structure" (Methods). **ligand**: **VARIED AT THREE LEVELS** — none, native trigger, and a ligand known not to bind. **partner**: none. <br>`crossings:` **MSA x ligand HELD** (ligand varied, MSA fixed) — the same shape as `lazou2026cryptic`. But the ligand axis is crossed with a **training-set-composition stratification** into three groups, and that crossing is what produces the paper's result: the trigger ligand raises the holo-like fraction by only 11.9% and 9.1% in Groups 1 and 2, against a **40.3%** difference between those groups attributable to training composition alone, rising to 17.5% in Group 3 where the memorised prior is weak. **The handle works where the model does not already know the answer and is swamped where it does.** Any decoy-arm interpretation of our own has to meet this design, not just its headline. |
| `anti_memorization_design` | **This paper is an anti-memorization design, and that is its whole contribution.** Rather than a temporal cutoff, the stratification variable *is* the training-set composition: proteins are grouped by their apo:holo ratio in the PDB and the same protocol is run across all three groups. That is a stronger test than a date cutoff for this question, because it varies the memorisable prior continuously instead of assuming a cutoff removes it. |
| `anti_memorization_control` | **RUN, ANALYSED, AND POWERED — n = 82, with two independent control arms.** Arm 1: the three-group stratification itself, with statistical significance reported in the SI Appendix. Arm 2: **the non-binder ligand arm**, which is the sharpest control in this corpus for a ligand-as-handle claim. Arm 3: an **AF2 replication** on Group 2 confirming the same memorisation, which rules out the effect being an AF3 architecture artefact. Nothing in the corpus does this better. |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **Tested explicitly, and it fails — this is a direct, independent corroboration of our own confidence claim.** Significance statement: "While the pLDDT values of such ligands are slightly lower, these are generally **not sufficient for discriminating between binder and nonbinder ligands**." The effect is group-dependent and the authors report it honestly in both directions: for Group 1, "the distributions of ligand pLDDT values become broader or shift to slightly lower values, but the changes are small, so this means that **the nonbinders are placed with almost the same confidence as the trigger ligands**" (Results); for Group 2, "the nonbinder ligands have substantially lower pLDDT values than the native ligands" (Results). Summarised as: "Thus, while AF3 predicts similar domain motions either with binder or nonbinder ligands, the latter are placed with lower confidence than the native ones" (Results). |

### `controls_run`

| control | what it rules out | locator |
|---|---|---|
| No-ligand arm, 500 models, every protein | that the holo-like models require the ligand | Results, Fig. 4 left |
| Trigger-ligand arm, 500 models, every protein | — (the paired comparison) | Results, Fig. 4 right |
| **Non-binder ligand arm** | **that the conformational change is caused by the specific ligand rather than by any occupant** | Results, Fig. 5 |
| Three-group stratification by PDB apo:holo ratio | that the effect is a property of the protein rather than of the training set | Results, Discussion |
| AF2 replication on Group 2 | that memorisation is an AF3 architecture artefact | Abstract, Results |
| Templates off, MSA fixed, defaults, uniform 500-model budget | that the result is a settings artefact | Methods |
| Apo/holo cluster separation check | that the two reference groups are not actually distinguishable | Results |
| TM-score replication of the whole analysis | that the conclusion depends on RMSD as the metric | SI Fig. S1, Table S3 |

## D. Claims

- **`central_conclusion`**: Whether AF3 returns the open (apo) or closed (holo) conformation of an
  enzyme is governed mainly by how many apo and holo structures of that enzyme are in the PDB, not
  by whether the triggering ligand is supplied. For enzymes with more apo than holo structures,
  64.8% of ligand-free models are nearer the open state; for enzymes with more holo than apo,
  75.5% of **ligand-free** models are already in the holo conformation. Supplying the ligand moves
  the fraction by roughly a tenth, against a forty-point gap between the two groups. Non-binding
  ligands induce nearly the same domain motion as the native trigger, and ligand pLDDT does not
  reliably separate the two. AF2 shows the same behaviour.

- **`necessity_claims`** (verbatim + section locator):
  - Significance: "However, results may depend more on the number of structures available for
    training than on the presence of a ligand in the calculation."
  - Significance: "Relatively small differences in the ratio of apo to holo structures can
    fundamentally change the type of the predicted structure, demonstrating very strong
    memorization."
  - Significance: "While the pLDDT values of such ligands are slightly lower, these are generally
    not sufficient for discriminating between binder and nonbinder ligands."
  - Abstract: "In many enzymes, movement of domains from open to closed state forms the
    environment required for catalysis."
  - Results: "In many enzymes movement of domains, induced by the binding of substrates or
    coenzymes, is necessary to form the chemical environment required for the catalytic reaction."
  - Discussion: "As machine learning methods move away from biophysics, it has become less clear
    what the program actually models".
  - Discussion: "More generally, the models are likely to be similar to the dominant conformation
    present in its training data, but it is not immediately clear from analysis of pLDDT scores or
    PAE graphs whether they resemble the apo or holo form of the protein."
  - Discussion: "This overwhelming difference reveals a high level of memorization."
  - Discussion: "While the common assumption is that it is difficult to dock ligands that require
    large conformational changes, this is clearly not entirely true for docking by cofolding to
    proteins with many different holo structures in the PDB."

- **`novelty_claims`** (verbatim + section locator): **No explicit priority claim is made.** The
  words "first", "novel" and "unprecedented" do not appear as self-positioning anywhere in the
  retrieved text. The strongest self-positioning statements are findings, not claims to priority:
  - Discussion: "Our main observation is that the predictions, for each protein, depend more on
    the ratio of apo to holo structures in the training set than on the presence of the ligand."
  - Abstract: "We have found that nonbinder ligands also generate similar domain motion, and the
    distributions of the predicted enzyme conformations remain close to those obtained with the
    native trigger ligands, but with lower ligand pLDDT values."

- **`stated_limits`** (verbatim + section locator):
  - Results, on reference-set quality: "The apo or holo X-ray structures may show some
    conformational variation, may form multiple subclusters, and clusters of apo and holo
    structures may even overlap for some of the proteins."
  - Results, on classification impurity in both directions: "Most holo structures bind ligands in
    addition to the "trigger" ligand. Many structures that are classified as apo also have some
    bound small molecules." *(The original uses typographic double quotes around the word trigger;
    they are reproduced here rather than downgraded to single quotes, so a mechanical quote check
    matches.)*
  - Discussion, conceding that the ligand does do something: the ligand effect "increases the
    fraction of holo-like models slightly more (by 17.5%) for Group 3 proteins that have fewer
    structures in the PDB and hence weaker conformation-specific bias".
  - Statistical significance is deferred: "The statistical significance of these differences is
    analyzed in the SI Appendix." (Discussion) — and the SI is not held here.

- **`stance`**: **`threat` + `precedent`** — provisional, the user's call, and **this is the most
  consequential stance assignment made since the corpus was built.**
  - *Threat, and a direct one.* Our Block B design attributes part of the α5-CT effect to
    occupancy of the cytoplasmic cleft, and separates it from the α5-CT sequence and from correct
    Gα family by decoy and shuffled arms. This paper shows, on 82 enzymes with 500 models each,
    that **a ligand known not to bind produces nearly the same conformational change as the native
    trigger**, and that confidence does not reliably separate them. A referee who knows this paper
    will ask whether our decoy arm is measuring the same generic occupancy artefact. Our answer
    has to be quantitative, not rhetorical, and it has to engage this paper by name.
  - *Precedent, and a helpful one.* It is independent, large-n, PNAS-published corroboration that
    (i) co-folding output tracks training-set composition rather than the input condition, and
    (ii) confidence does not discriminate a correct from an incorrect ligand-induced state. Both
    are claims we also make. It also sets the methodological bar: 500 models per condition, all
    reported as distributions, no best-of-N, defaults throughout, plus a non-binder arm and an
    architecture-replication arm.
  - **Action required:** add to the threats table in `../CLAIMS.md` alongside `tran2026nanogs` and
    `vo2026fiducials`, and engage it explicitly in the Discussion.

## E. Quantitative comparators

| metric | value | units | measured against | locator |
|---|---|---|---|---|
| Ligand-free models nearer the open apo reference, Group 1 (more apo than holo) | 64.8% | % of 500 models, pooled over 19 proteins | RMSD to deposited apo vs holo, fixed domain aligned | Abstract |
| Ligand-free models in the holo conformation, Group 2 (more holo than apo) | 75.5% | % of 500 models, pooled over 25 proteins | same | Abstract |
| Increase in holo-like fraction on adding the trigger ligand, Group 1 | +11.9% | percentage points | same | Discussion |
| Increase in holo-like fraction on adding the trigger ligand, Group 2 | +9.1% | percentage points | same | Discussion |
| Increase in holo-like fraction on adding the trigger ligand, Group 3 (few structures) | +17.5% | percentage points | same | Discussion |
| **Difference in holo-like fraction between Group 1 and Group 2** | **40.3%** | percentage points | same | Discussion |
| Native ligand placed < 2 Å RMSD, Group 2 | 80% | % of models | reference holo X-ray ligand pose | Discussion |
| Native ligand placed < 2 Å RMSD, Group 3 | 73.7% | % of models | same | Discussion |
| Native ligand placed < 2 Å RMSD, Group 1 | 42% | % of models | same | Discussion |

**The comparison that matters for us** is the 40.3% against the 9.1–17.5%: the training-set prior
is roughly three to four times the size of the input-condition effect. Any claim we make that a
co-input moves state has to be argued against a baseline of that shape.

- **`n_predictions`**: **500 models per protein per input condition**, from 100 random seeds, no
  templates (Methods). Targets: 82. Conditions: at least three (no ligand, trigger ligand,
  non-binder ligand), the non-binder arm run on the 12 detailed proteins. Total for the two main
  arms: 82 × 2 × 500 = **82,000 models**, which is my arithmetic from the stated protocol, not a
  number the paper prints.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI NOT HELD, and it is material.** SI Appendix is a separate 23.93 MB PDF
  containing Table S1 (all 82 proteins), Table S2 (all PDB IDs and ligands, plus the apo/holo
  cluster separation analysis), Table S3 (per-protein model counts by RMSD **and** TM-score),
  Fig. S1 (the TM-score replication of Fig. 4) and Fig. S4, **and the statistical significance
  analysis of the headline differences**. Every per-protein number and every significance test is
  therefore outside what this note can verify. Data at `zenodo.org/records/18217188`; code at
  `bitbucket.org/bu-structure/af3conformations`.

## F. Figures

Captions retrieved from the HTML; **panels not viewed and no page numbers available**, so
`data_shape` is given only where the caption fully determines it.

| fig_no | locator | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | Results | Four Group 1 enzymes; per protein a column of four graphs: 500 no-ligand models, 500 ligand models, ligand-RMSD histogram, ligand pLDDT vs ligand RMSD | scatter + histogram | `PLOT \| facet: protein (4) × arm (4 rows) \| vary: RMSD to reference apo (continuous) \| series: AF3 ranking score (continuous colour) \| measure: RMSD to reference holo \| n: 500 models per panel` | 4 columns × 4 rows | — | **CC BY-NC-ND 4.0 — ND, redrawing forbidden** |
| 2 | Results | Same layout, Group 2 enzymes (more holo than apo) | scatter + histogram | as Fig 1 | 4 columns × 4 rows | — | as above |
| 3 | Results | Same layout, Group 3 enzymes (very few X-ray structures). **Caption says "Group 2" in error where the text says Group 3** | scatter + histogram | as Fig 1 | 4 columns × 4 rows | Caption/text mismatch, recorded in `unresolved` | as above |
| 4 | Results | Fractions of models closer to apo (red) and holo (blue), without ligand (left) and with ligand (right), by group | stacked or grouped bar | `PLOT \| facet: arm (2: no ligand, ligand) \| vary: group (3) \| series: nearer reference (2: apo, holo) \| measure: fraction of 500 models \| n: 500 per protein, 19/25/38 proteins per group` | 2 | **Pools proteins within a group**, so per-protein spread is only in SI Table S3; no error bars described in the caption | as above |
| 5 | Results | **The non-binder arm.** Per protein three graphs: holo-model RMSD distributions, models with a non-binder ligand, and pLDDT distributions for native vs non-binder | scatter + density | `PLOT \| facet: protein (12) × view (3) \| vary: RMSD to reference apo (continuous) \| series: ligand identity (2: native, nonbinder) \| measure: RMSD to reference holo / pLDDT density \| n: 500 models per panel` | 12 × 3 | **The single most reusable panel design in the corpus for a decoy-arm figure** | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium-high on the main text, low on anything in the SI.** Abstract,
  Significance, Results, Discussion and Methods were retrieved complete and every quote above is
  verbatim from them. All per-protein numbers, all significance testing and the TM-score
  replication are in an SI Appendix that was not retrieved. **No page numbers exist for this
  note** because no PDF could be obtained.
- **`unresolved`**:
  1. **No PDF, therefore no page numbers.** Locators are section names. If this paper is cited in
     the manuscript, obtain the PDF first and convert the locators.
  2. **SI Appendix not held** — Tables S1–S3, Figs S1 and S4, and the statistical significance
     analysis of the 11.9 / 9.1 / 17.5 / 40.3 numbers.
  3. **Fig. 3's caption says "Group 2" where the body text says Group 3.** One of the two is a
     typo; the body text is almost certainly right.
  4. **Non-binder arm scope.** It is presented for the 12 proteins of Table 1; whether it was run
     across all 82 is not stated in the main text.
  5. **How non-binder ligands were chosen** is not described in the retrieved Methods.
  6. Ligand pLDDT values are given as distributions in figures, not as numbers in the text.
- **`why_it_matters`**: *(left empty by the extractor — the user's call. But see `stance`: this is
  a threats-table paper and the Discussion has to meet it.)*

## Tags

```
general-protein cofolding benchmark-only ensemble two-state rmsd-only continuous-metric
no-template-no-msa design-level-oracle anti-memorization multi-backbone ligand-driven
directed-state confidence-as-discriminator seed-only peer-reviewed threat precedent
negative-result comparator-numbers
```

**Tag notes.**
- `oracle-leak` **deliberately NOT applied.** Only route 5 fires, and it is evaluation-side and
  unavoidable in a retrospective benchmark; routes 1, 2, 3, 4 and 6 are all clean, which is rare
  enough in this corpus to be worth protecting from a false positive. `design-level-oracle` is
  applied for route 7.
- `no-template-no-msa` applied for the template half only: templates are off, but a full MMseqs2
  MSA is supplied. The tag is the closest available and this caveat must be read with it.
- `anti-memorization` applied, and this paper is close to the reference example of it in the
  corpus, alongside `skrinjar2026generalization`.
- `multi-backbone` applied for the AF2 confirmation arm.
- `unpowered` **deliberately NOT applied**: n = 82 proteins × 500 models per arm.
- `gpcr` **deliberately NOT applied** — enzymes only.
