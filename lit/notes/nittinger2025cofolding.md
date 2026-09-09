# nittinger2025cofolding

> **Extraction provenance.** Extracted 2026-09-09 from the **published Elsevier PDF** (CC BY-NC-ND),
> supplied by the user after the publisher's CAPTCHA blocked automated retrieval. The article
> carries article number 100136 and the PDF is internally paginated 1–10; locators below are
> **PDF pages**, which is the only pagination the article has. Main text read; Supporting
> Information S1 not retrieved. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `nittinger2025cofolding` |
| `doi` | 10.1016/j.ailsci.2025.100136 |
| `year`, `venue` | 2025 — **Artificial Intelligence in the Life Sciences 8:100136**, peer-reviewed, **CC BY-NC-ND** (ND: redrawing forbidden). |
| `title` | Co-folding, the future of docking – prediction of allosteric and orthosteric ligands |
| `authors` | Eva Nittinger, Özge Yoluk, Alessandro Tibo, Gustav Olanders, Christian Tyrchan (AstraZeneca) |

## B. Scope

| field | value |
|---|---|
| `system` | **general protein** — targets with paired allosteric and orthosteric ligand sets. No GPCR arm. |
| `n_targets` | **17 proteins, 40 ligands: 20 orthosteric and 20 allosteric** (p1). Deliberately balanced, which is the design's strength. |
| `method_class` | **benchmark-only** on co-folding backbones. |
| `backbones` | **NeuralPLexer, RoseTTAFold All-Atom, Boltz-1 / Boltz-1x** (p1). AF3 discussed but not run. → `multi-backbone`. |
| `templates` | NOT REPORTED in the retrieved text. |
| `msa_handling` | NOT REPORTED in the retrieved text. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **single-state per prediction, ligand poses only.** The protein conformation is not treated as a variable; the question is where the ligand lands. |
| `structural_priors_used` | Target and ligand-set selection requires proteins with both an allosteric and an orthosteric ligand deposited, so every target was chosen because both answers exist. Design-time. |
| `oracle_leakage` | **Route 5 PRESENT, definitionally** — success is pose RMSD to the deposited reference. **Route 7 PRESENT, design-level** — targets chosen for known allosteric and orthosteric sites. **Routes 1, 2, 3 NOT REPORTED** in the retrieved text; templates and MSA handling are not described there. **Routes 4 and 6 NOT REPORTED.** This is a thinner oracle account than the corpus average and is flagged in `unresolved`. |
| `prospective` | **no.** Retrospective benchmark against deposited complexes. |
| `state_metric` | **NOT APPLICABLE for protein conformational state.** Ligand-pose RMSD to reference plus site-identification success. The receptor's conformation is never assessed. |
| `metric_saturation` | **NOT EXTRACTED.** |
| `directional_control` | **The ligand is the only input variable**, and the finding is about where the model places it, not about steering a protein conformation. No conformational handle. |
| `anti_memorization_design` | **NOT REPORTED** in the retrieved text. No temporal cutoff is described. |
| `anti_memorization_control` | **NONE RUN.** |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT EXTRACTED.** |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| Matched orthosteric vs allosteric ligand sets on the same 17 proteins | that allosteric failure is a property of the targets rather than of the site type | p1 |
| Three independent co-folding backbones | that the failure is one model's artefact | p1 |
| **Absent:** temporal or training-set control | — | — |

## D. Claims

- **`central_conclusion`**: On a deliberately balanced set of 17 proteins carrying 20 orthosteric
  and 20 allosteric ligands, three co-folding methods place orthosteric ligands far better than
  allosteric ones. Co-folding is presented as the successor to docking, with allosteric site
  prediction identified as the outstanding failure mode.

- **`necessity_claims`** (verbatim + page):
  - p1: "Here, we focus on the prediction of allosteric binding sites, using a dataset of 17
    orthosteric/allosteric ligand sets."
  - p1: "A recent study showed based on one allosteric example, Cyclin-Dependent Kinase (CDK) 2,
    that DL-based diffusion docking methods, still struggle to find the allosteric binding site"
    *(attributed to ref 21, not their own result — quoted so the attribution is not lost)*.

- **`novelty_claims`**: **NOT FULLY EXTRACTED.** No explicit priority claim was located in the
  retrieved text beyond the framing in the title. Flagged in `unresolved`.

- **`stated_limits`**: **NOT EXTRACTED.** A dedicated limitations passage was not located.

- **`stance`**: `precedent` + `contrast` — provisional, the user's call. It joins
  `parikh2026allosteric`, `purnomo2026cafe` and `obendorf2026statespecific` as evidence that
  co-folding degrades sharply away from the orthosteric pocket, and it has the cleanest matched
  design of the four: same proteins, same models, only the site type varies. It carries no
  conformational-state axis and no GPCR, so it is background for our argument rather than a
  competitor.

## E. Quantitative comparators

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Benchmark size | 17 proteins, 40 ligands (20 orthosteric, 20 allosteric) | count | — | p1 |
| Backbones compared | 3 (NeuralPLexer, RFAA, Boltz-1/1x) | count | — | p1 |
| PDB scale cited for context | ~230,000 structures, ~100,000 unique | count | — | p1 |

**The per-method success rates are the paper's actual result and were not extracted from the
figures.** Flagged in `unresolved`.

- **`n_predictions`**: **NOT EXTRACTED.**
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI NOT HELD** — "Several adaptions have been made in order to enhance the
  quality of the structures used (for details see Supporting Information S1...)" (p1), so the
  dataset curation is outside this note.

## F. Figures

**NOT EXTRACTED.** Figure captions were not enumerated. Do not use this note for a figure-design
query. Licence is CC BY-NC-ND, so **redrawing any panel is forbidden**.

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium-low.** Identity, venue, licence, scope and the balanced design are
  solid. Method details, all result numbers, novelty claims, stated limits and figures were not
  extracted. This note is enough to place the paper and to cite it for its design; it is not
  enough to cite it for a number.
- **`unresolved`**:
  1. Per-method allosteric and orthosteric success rates.
  2. Templates and MSA handling; oracle routes 1–4 and 6.
  3. `novelty_claims` and `stated_limits` both need a second pass.
  4. Figures not enumerated.
  5. Whether any temporal or training-set control exists.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
general-protein kinase cofolding benchmark-only multi-backbone single-state rmsd-only
binary-predicate design-level-oracle no-anti-memorization ligand-driven orthosteric
allosteric-site allosteric-failure peer-reviewed precedent contrast negative-result
```

**Tag notes.** `kinase` applied because CDK2 is discussed as the motivating allosteric case;
verify against the full target list before relying on it in a reverse lookup. `gpcr`
**deliberately not applied** — there is no receptor in this study. `comparator-numbers`
**deliberately not applied**, because no number was extracted that our results could sit beside.
