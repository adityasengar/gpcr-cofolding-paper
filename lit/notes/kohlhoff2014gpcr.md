# kohlhoff2014gpcr

> **Extraction provenance and two caveats.** Extracted 2026-09-09 from the **Europe PMC full-text
> XML** of the **NIH author manuscript** (PMC3923464 / NIHMS550310), not the published Nature
> Chemistry typesetting. **No PDF in `pdfs/`, so locators are SECTION names, not page numbers**;
> published pagination is Nat Chem 6(1):15–21. **A corrigendum exists**: Nat Chem 7:759 (2015),
> doi 10.1038/nchem.2272, PMID 26291949, which is recorded here because a manuscript citing this
> paper should cite it. The corrigendum's content was not retrieved. See `unresolved`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `kohlhoff2014gpcr` |
| `doi` | 10.1038/nchem.1821 (corrigendum 10.1038/nchem.2272) |
| `year`, `venue` | 2014 — **Nature Chemistry 6(1):15–21**, peer-reviewed. Published online 15 Dec 2013, in issue Jan 2014. |
| `title` | Cloud-based simulations on Google Exacycle reveal ligand modulation of GPCR activation pathways |
| `authors` | Kai J. Kohlhoff, Diwakar Shukla, Morgan Lawrenz, Gregory R. Bowman, David E. Konerding, Dan Belov, Russ B. Altman, Vijay S. Pande (Stanford; Kohlhoff, Konerding and Belov at Google) |

**Note on the title.** The published title reads "ligand modulation"; the author-manuscript XML
carries "ligand-modulation" with a hyphen. `refs.bib` uses the published form, which is correct.

## B. Scope

| field | value |
|---|---|
| `system` | **GPCR, class A — β2 adrenergic receptor (β2AR)**, single receptor. |
| `n_targets` | **1 receptor**, in **three ligand conditions**: agonist BI-167107, inverse agonist carazolol, and **apo**. |
| `method_class` | **MD + clustering.** Tens of thousands of short independent trajectories on Google Exacycle, aggregated into **Markov state models**; activation trajectories then generated from the MSM. Transition Path Theory used to extract intermediates. |
| `backbones` | NOT APPLICABLE — no structure predictor. |
| `templates` | NOT APPLICABLE. |
| `msa_handling` | NOT APPLICABLE. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **ensemble + continuum.** A Markov state model over β2AR conformational space per ligand condition, from which 150 μs activation trajectories are generated. |
| `structural_priors_used` | Deposited inactive and active β2AR structures define the endpoints and the structural criteria used to project trajectories. Ligands are taken from their deposited complexes. Design-time and appropriate. |
| `oracle_leakage` | **Routes 1–7 largely NOT APPLICABLE** — no prediction pipeline, no held-out answer, no scored success. Recorded route by route.<br>**Route 1:** deposited β2AR structures seed the simulations. Design-time, recorded under `structural_priors_used`.<br>**Routes 2, 3:** NONE FOUND.<br>**Route 4:** MSM lag time and state decomposition are chosen against the data, which is standard MSM practice and validated internally rather than against a held answer.<br>**Route 5:** NOT APPLICABLE — no RMSD-to-reference success criterion.<br>**Route 6:** NONE FOUND.<br>**Route 7 — PRESENT, design-level.** β2AR was chosen precisely because its active and inactive structures and its pharmacology are known, and the ligands chosen are a canonical full agonist and a canonical inverse agonist. |
| `prospective` | **partial.** The activation pathway and its intermediates are new; the endpoint states and the ligands' pharmacological classes were known in advance. |
| `state_metric` | **continuous coordinate**, four structural criteria applied simultaneously. Trajectories are projected "along the four described structural criteria" per ligand condition (Results, Fig 1b–d). No binary predicate and no threshold is imposed. The exact four criteria were **not** isolated in the retrieved text and are flagged in `unresolved`. |
| `metric_saturation` | Not applicable numerically. The reported limit is sampling: apo and inverse-agonist conditions simply do not reach the active region on all criteria, which is a finding rather than a metric artefact. |
| `directional_control` | **The ligand is the handle, and it works here.** Agonist BI-167107 drives sampling of active-state conformations; carazolol and apo do not. Verbatim, Results: "inverse agonist and apo simulations do not sample active state conformations along all structural metrics." This is a **ligand-driven, partner-free** demonstration in a physical model. |
| `anti_memorization_design` | **NOT APPLICABLE** — no learned model. |
| `anti_memorization_control` | **NOT APPLICABLE.** |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE.** MSM validation against prior computational and experimental results plays the analogous role: "Markov state models aggregate independent simulations into a single statistical model that is validated by previous computational and experimental results" (Abstract). |

### `controls_run`

| control | what it rules out | locator |
|---|---|---|
| Apo arm | that the agonist is not doing the work | Results, Fig 1d |
| Inverse agonist (carazolol) arm | that any ligand would drive activation | Results, Fig 1c |
| Agonist (BI-167107) arm | — (the positive) | Results, Fig 1b |
| MSM validation against prior computational and experimental results | that the model is an artefact of the sampling scheme | Abstract |
| Four independent structural criteria rather than one | that the conclusion depends on one coordinate | Results |

## D. Claims

- **`central_conclusion`**: Two milliseconds of aggregate β2AR dynamics, run as tens of thousands
  of short independent simulations on commodity cloud infrastructure and stitched together with a
  Markov state model, resolve the receptor's activation pathways. Agonist and inverse agonist
  interact differentially with those pathways: the agonist condition samples active-state
  conformations while the inverse agonist and apo conditions do not reach them on all structural
  metrics. Transition Path Theory intermediates from the MSM are then shown to enrich chemotypes
  that docking to a small number of deposited structures would miss.

- **`necessity_claims`** (verbatim + section locator):
  - Abstract: "Simulations can provide tremendous insight into atomistic details of biological
    mechanisms, but micro- to milliseconds timescales are historically only accessible on
    dedicated supercomputers."
  - Discussion: "The unprecedented millisecond simulation time scales presented here for GPCR
    activation require computing architectures capable of such extensive sampling."
  - Results, the load-bearing negative for us: "inverse agonist and apo simulations do not sample
    active state conformations along all structural metrics."

- **`novelty_claims`** (verbatim + section locator):
  - Abstract: "We demonstrate that cloud computing is a viable alternative, bringing long-timescale
    processes within reach of a broader community."
  - Discussion: "The unprecedented millisecond simulation time scales presented here for GPCR
    activation" — a priority claim on scale.
  - Discussion: "Our work on Google's Exacycle platform demonstrates that large-scale exploratory
    analysis in the cloud can deliver new insight into biological problems."
  - Abstract: "Agonists and inverse agonists interact differentially with these pathways, with
    profound implications for drug design".
  - Results: "These results show that docking to intermediates identified by MSM Transition Path
    Theory analysis enriches more diverse chemotypes that could be missed by screens of only a few
    structures."

- **`stated_limits`**: **NOT FULLY EXTRACTED.** The author-manuscript XML was read for scope,
  method and the ligand-condition result; a dedicated limitations passage was not located. Given
  the 2015 corrigendum, no limitation should be attributed to these authors without checking both
  the published version and the corrigendum. Flagged in `unresolved`.

- **`stance`**: `background` + `precedent` — provisional, the user's call.
  - *Background*: the canonical MD demonstration that β2AR activation proceeds through resolvable
    intermediates rather than a two-state jump, and the reference for using MSM intermediates as
    docking targets.
  - *Precedent, with a tension worth stating plainly.* Its apo arm does **not** reach active-state
    conformations on all structural metrics. Our own apo arm produces active-like structures at a
    non-zero rate in AF3-lineage predictions. Those two observations are about different objects,
    a physical equilibrium versus a learned generative distribution, and the difference is
    interesting rather than contradictory. But a referee may read them as contradictory, so if our
    apo result is discussed, this paper should be cited alongside it and the distinction made
    explicitly rather than left to the reader.

## E. Quantitative comparators

| metric | value | units | measured against | locator |
|---|---|---|---|---|
| Aggregate simulation time | 2 | milliseconds | β2AR | Abstract |
| Generated activation trajectories from the MSM | 150 | μs | β2AR | Results |
| Independent simulations | "tens of thousands" | count | — | Results |
| Prior state of the art cited for comparison | "several hundred μs" on special-purpose hardware | simulation time | — | Introduction |
| Ligand conditions | 3 (agonist BI-167107, inverse agonist carazolol, apo) | count | — | Results |
| Structural criteria used for projection | 4 | count | — | Results |

- **`n_predictions`**: NOT APPLICABLE.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI NOT HELD.** The text references Supplementary Figures up to S22, which
  hold the docking-enrichment results.

## F. Figures

Only Figure 1 was resolvable from the retrieved text. **Panels not viewed.** Recorded
conservatively.

| fig_no | locator | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1B-D | Results | MSM-generated activation trajectories projected along four structural criteria, one panel per ligand condition | line / trajectory projection | `PLOT \| facet: ligand condition (3: agonist BI-167107, inverse agonist carazolol, apo) \| vary: simulation progress (continuous) \| series: structural criterion (4) \| measure: criterion value \| n: 150 μs of MSM-generated trajectory per panel` | 3 (b, c, d) | — | **Nature Chemistry 2014; the author manuscript carries the NIH public-access terms, the published version is all rights reserved. Treat as no-reuse and check before adapting any panel.** |
| S1–S22 | SI (not held) | Docking enrichment against MSM intermediates, and supporting analyses | NOT EXTRACTED | NOT EXTRACTED | — | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium.** High on identity, scale, ligand conditions and the apo/inverse-
  agonist negative result. Low on the four structural criteria, on the MSM construction details,
  on figure structure and on everything in the SI. This is a **2014 paper read as an NIH author
  manuscript**, so both pagination and final wording may differ from the published version.
- **`unresolved`**:
  1. **No PDF and no page numbers.** Section locators only, from the author-manuscript version.
  2. **The 2015 corrigendum (Nat Chem 7:759, 10.1038/nchem.2272) was not retrieved.** Its content
     is unknown and could touch any number quoted above. Retrieve it before citing this paper.
  3. **The four structural criteria are never enumerated in the retrieved text.** They are the
     part most useful to us, since they are a 2014 precedent for a multi-criterion GPCR state
     readout.
  4. `stated_limits` not located.
  5. MSM lag time, microstate and macrostate counts not extracted.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
gpcr md enhanced-sampling af-cluster ensemble continuum continuous-metric ligand-driven
apo-sampling orthosteric design-level-oracle peer-reviewed background precedent
comparator-numbers
```

**Tag notes.** `af-cluster` is applied in its literal sense of clustering trajectories into a state
model, **not** in the AF-Cluster / MSA-clustering sense the tag usually carries in this corpus.
That is a genuine collision in the fixed vocabulary and it should be resolved rather than left:
either rename the tag or add `markov-state-model`. Flagged for the user alongside the
`non-biomolecular` decision. `two-state` **deliberately not applied** — the whole result is that
activation passes through intermediates.
