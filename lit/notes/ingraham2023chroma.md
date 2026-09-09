# ingraham2023chroma

> **Extraction provenance, and this note is deliberately PARTIAL.** Extracted 2026-09-09 from the
> **publisher HTML** at nature.com, read through the browser because every scripted route to the
> PDF is bot-walled. The page yielded the Abstract, the Discussion and the data-availability
> statement; **the Results and Methods were truncated by the retrieval and were never read.**
> No PDF in `pdfs/`, so locators are SECTION names, not page numbers; published pagination is
> Nature 623(7989):1070–1078. Several schema fields below therefore say `NOT EXTRACTED` rather
> than `NOT REPORTED`, and the difference is deliberate: it means the paper may well report it and
> this note cannot say. **Do not use this note for a novelty or priority argument until it has
> been re-extracted from the PDF.** See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `ingraham2023chroma` |
| `doi` | 10.1038/s41586-023-06728-8 |
| `year`, `venue` | 2023 — **Nature 623(7989):1070–1078**, peer-reviewed, **open access, CC-BY**. Published 15 November 2023. |
| `title` | Illuminating protein space with a programmable generative model |
| `authors` | John B. Ingraham, Max Baranov, Zak Costello, Karl W. Barber, Wujie Wang, Ahmed Ismail, Vincent Frappier, Dana M. Lord, Christopher Ng-Thow-Hing, Erik R. Van Vlack, Shan Tie, Vincent Xue, Sarah C. Cowles, Alan Leung, João V. Rodrigues, Claudio L. Morales-Perez, Alex M. Ayoub, Robin Green, Katherine Puentes, Frank Oplinger, Nishant V. Panwar, Fritz Obermeyer, Adam R. Root, Andrew L. Beam, Frank J. Poelwijk, Gevorg Grigoryan (Generate Biomedicines) — 26 authors, full list verified against Crossref |

## B. Scope

| field | value |
|---|---|
| `system` | **general protein — de novo design.** Proteins and protein complexes generated from scratch, not conformational states of an existing sequence. |
| `n_targets` | **310 proteins experimentally characterised** (Abstract). **2 crystal structures** solved, agreeing with the samples at "a backbone root-mean-square deviation of around 1.0 Å" (Abstract). Complexes of more than 3,000 residues are generated (Discussion). |
| `method_class` | **other — generative diffusion for protein design.** A diffusion process "that respects the conformational statistics of polymer ensembles", a sub-quadratic-scaling architecture, layers synthesising 3-D structure from predicted inter-residue geometries, and a low-temperature sampling algorithm (Abstract). |
| `backbones` | Chroma itself. **No co-folding model is used and none is compared against.** |
| `templates` | NOT APPLICABLE. |
| `msa_handling` | NOT APPLICABLE — generation is unconditional on alignments. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE for conformational state.** Chroma samples *new proteins*, not alternative conformations of a given one. Nothing in this paper produces two states of one sequence. |
| `structural_priors_used` | **NOT EXTRACTED.** Training-set construction was in the un-retrieved Methods. |
| `oracle_leakage` | **Routes 1, 2, 3, 5, 6 NOT APPLICABLE** — there is no target conformational state to leak, and success is experimental rather than RMSD-to-a-held-answer for the main claim. **Route 4: NOT EXTRACTED** (hyperparameter selection was in the Methods). **Route 7: PRESENT in a mild, disclosed form**, in that the two crystallised designs are the ones that were carried forward; but the paper explicitly argues *against* the usual down-selection, see `controls_run`. |
| `prospective` | **yes, and unusually so for this corpus.** 310 designs were expressed and characterised, and the paper deliberately declines to filter them first. Discussion: "We reasoned that the best way to determine the plausibility of the protein space parameterized by Chroma was to draw independent samples from the model and test them experimentally." |
| `state_metric` | **NOT APPLICABLE for conformational state.** The reported structural metric is backbone RMSD between a designed sample and its solved crystal structure, ~1.0 Å (Abstract). |
| `metric_saturation` | **NOT EXTRACTED.** |
| `directional_control` | **Yes, and this is the paper's headline and its only real relevance to us.** Generation can be conditioned on "symmetries, substructure, shape, semantics and even natural-language prompts" (Abstract), framed as "protein design as Bayesian inference under external constraints" (Abstract). The Discussion enumerates the handles: "inter-residue distance and contact, domain, sub-structure and semantic specification **from classifiers**". **Classifier conditioning of a protein diffusion model is therefore established prior art as of 2023**, which is the fact this entry exists to record. The conditioning targets designed properties, not a conformational state of a given receptor. |
| `anti_memorization_design` | **NOT EXTRACTED.** |
| `anti_memorization_control` | **NOT EXTRACTED.** The experimental characterisation of novel designs is a strong argument against pure memorisation, but the paper's own training-set-overlap analysis, if any, was not read. |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT EXTRACTED.** |

### `controls_run`

| control | what it rules out | locator |
|---|---|---|
| **No down-selection of designs before experiment** | that the success rate is a filtering artefact. Stated deliberately: "this is a departure from the prototypical protein-design protocol, in which initial proposal designs are down-selected using a custom set of filters" (Discussion) | Discussion |
| Crystal structures of two designs | that folded-and-expressed implies the intended structure | Abstract |
| A conservative accounting of success | over-counting: the Discussion restricts to "only the proteins we purified and characterized individually in solution" as successes | Discussion |
| **Not extracted:** all computational ablations | — | Methods (not read) |

## D. Claims

- **`central_conclusion`**: Chroma is a generative diffusion model over protein structure and
  sequence that can be steered at sampling time by user-specified constraints, including
  classifier-supplied and natural-language ones, and that produces designs which express, fold and
  match their intended structures at usable rates without any down-selection before experiment.

- **`necessity_claims`** (verbatim + section locator):
  - Abstract: "Accessing this potential has been challenging for both computation and experiments
    because the space of possible protein molecules is much larger than the space of those likely
    to have functions."
  - Discussion, on the cost of the conventional protocol: "Although the latter practice, which is
    broadly adopted in the field, can be effective at increasing design success rates, it does
    require a custom set of filters for each design project and makes fully automated design
    difficult to achieve."

- **`novelty_claims`** (verbatim + section locator):
  - Abstract: "Here we introduce Chroma, a generative model for proteins and protein complexes
    that can directly sample novel protein structures and sequences, and that can be conditioned
    to steer the generative process towards desired properties and functions."
  - Abstract: "Chroma achieves protein design as Bayesian inference under external constraints,
    which can involve symmetries, substructure, shape, semantics and even natural-language
    prompts."
  - Discussion: "Chroma is programmable in the sense that it can sample proteins with a wide array
    of user-specified properties, including inter-residue distance and contact, domain,
    sub-structure and semantic specification from classifiers."
  - Discussion: "it has even begun to demonstrate the ability to accept descriptions of desired
    properties as free text."
  - Discussion: "Our experimental validation shows that Chroma has learnt a sufficiently accurate
    distribution such that sampling from it results in proteins that express, fold, have
    favourable biophysical properties and conform to intended structures at non-trivial rates."

- **`stated_limits`**: **NOT EXTRACTED.** The Discussion continues past the retrieved text.

- **`stance`**: `background` — provisional, the user's call. It is the 2023 precedent that a
  protein diffusion model can be conditioned by classifiers at sampling time, which matters for
  any novelty claim about classifier-guided structure generation. It is **not** a conformational-
  control paper and carries no receptor, no state and no co-folding comparison, so it should not
  appear in a multi-state or GPCR argument.

## E. Quantitative comparators

| metric | value | units | measured against | locator |
|---|---|---|---|---|
| Designed proteins experimentally characterised | 310 | count | expression, folding, biophysics | Abstract |
| Crystal structures solved | 2 | count | — | Abstract |
| Backbone RMSD, design vs solved structure | ~1.0 | Å | crystal structure of the design | Abstract |
| Largest systems generated | > 3,000 | residues | — | Discussion |
| Generation time for those | "a few minutes" on one NVIDIA V100 | wall clock | — | Discussion |

**Every per-experiment rate is in the un-retrieved Results.** The success rates that a reader
would actually want are not in this note.

- **`n_predictions`**: **NOT EXTRACTED.**
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **NOT DETERMINED.** Nature papers of this type carry extensive Supplementary
  Information; none of it was retrieved.

## F. Figures

**NOT EXTRACTED.** No figure caption was retrieved. The figure table is deliberately left empty
rather than populated with guesses, and this note must not be used for a figure-design query.

## G. Provenance

- **`extracted_on`**: 2026-09-09
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3-partial`
- **`confidence`**: **low.** Identity, venue and author list are verified against Crossref. The
  Abstract and Discussion quotes are verbatim from the publisher page. **Results, Methods, figures
  and all supplementary material were never read.** This is the weakest note in the corpus and is
  marked as such so no query mistakes it for a full extraction.
- **`unresolved`**:
  1. **Results and Methods not read.** Training data, architecture details, ablations, all
     computational metrics and every design success rate.
  2. **Figures not extracted at all.**
  3. `stated_limits`, `anti_memorization_*`, `metric_saturation`, `confidence_as_discriminator`
     and oracle route 4 all unresolved.
  4. **No PDF and no page numbers.** The paper is CC-BY, so obtaining it is permitted and only
     the download is blocked; a manual download closes every item above.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
general-protein directed-state prospective experimental-validation peer-reviewed background
```

**Tag notes.** `latent-steering` **deliberately not applied**: the conditioning is Bayesian
constraint-based sampling, not an intervention on an internal representation of a frozen model.
`cofolding` **deliberately not applied** — Chroma is not a co-folding model. `ensemble`,
`single-state`, `continuum` and every metric tag are **deliberately not applied** because the paper
has no conformational-state axis and tagging it would false-positive multi-state queries. The tag
list is short because the note is partial; **it will need revisiting after a full extraction.**
