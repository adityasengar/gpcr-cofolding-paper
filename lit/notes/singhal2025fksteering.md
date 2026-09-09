# singhal2025fksteering

> **Extraction provenance.** Extracted 2026-09-08 from the arXiv v5 PDF (`arXiv:2501.06848v5`,
> 18 Jul 2025). Abstract, introduction, method and results scope read directly; figure and table
> inventory enumerated mechanically by page from captions, panels not viewed. Fields that could
> not be settled from what was read say so. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `singhal2025fksteering` |
| `doi` | arXiv:2501.06848 (v1 12 Jan 2025, v5 18 Jul 2025) |
| `year`, `venue` | 2025 — **ICML 2025 (poster)**. Acceptance verified on OpenReview; the arXiv page itself carries no venue line, so cite the venue from the proceedings, not from arXiv. `peer-reviewed`. |
| `title` | A General Framework for Inference-time Scaling and Steering of Diffusion Models |
| `authors` | Raghav Singhal\*, Zachary Horvitz\*, Ryan Teehan\*, Mengye Ren, Zhou Yu, Kathleen McKeown, Rajesh Ranganath (NYU / Columbia; \*equal contribution) |

## B. Scope

| field | value |
|---|---|
| `system` | **other — not a biomolecular paper.** Text-to-image diffusion and discrete text diffusion. **No protein, no structure, no molecule is generated or evaluated anywhere in this paper.** The word "protein" appears three times in the body, all in motivation or related-work framing (p1 twice, p16 once) and once in the reference list. This matters: the paper is routinely cited as steering precedent for structure models, and that citation is correct at the level of the algorithm and false at the level of the evidence. |
| `n_targets` | NOT APPLICABLE. Benchmarks are GenEval prompt sets, ImageReward / HPS human-preference rewards, ImageNet class-conditional generation, and text-quality and toxicity rewards. |
| `method_class` | **other — inference-time steering.** Feynman-Kac interacting particle system: multiple diffusion trajectories ("particles") are simulated jointly and resampled at intermediate steps using potentials built from a reward evaluated on intermediate states. No gradient of the reward is required and no model is retrained. |
| `backbones` | Stable Diffusion family text-to-image models (0.8B and 2.6B parameter comparisons, p1, p3), plus discrete text diffusion models. No structure-prediction backbone. |
| `templates` | NOT APPLICABLE. |
| `msa_handling` | NOT APPLICABLE. |

## C. Conformational core

Every field in this section is `NOT APPLICABLE` and that is a property of the paper, not a gap in
the extraction. Recorded field by field so a reverse lookup cannot mistake absence for oversight.

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE — no protein conformations are generated.** |
| `structural_priors_used` | **NONE.** No deposited structure enters this work at any point. |
| `oracle_leakage` | **NOT APPLICABLE for the seven routes as written**, all of which presuppose a target structure. Routes 1, 2, 3, 5, 6, 7 have no referent here. The nearest analogue of **route 4** is present and should be recorded: potentials, resampling schedules and the λ parameter are compared on the same benchmarks that report the headline scores (Tables 5, 9, 10, pp14, 22), which is evaluation-set tuning of a sweep range. Protocol pp10–15, 21–23. |
| `prospective` | **NOT APPLICABLE** — no prediction about an unknown system is made or tested. |
| `state_metric` | **NOT APPLICABLE for conformational state.** The metrics used are GenEval prompt fidelity, ImageReward, HPS, perplexity, linguistic acceptability and toxicity-classifier scores. |
| `metric_saturation` | **NOT DETERMINED** — tables were read for scope, not for distributional behaviour. |
| `directional_control` | **Yes, at the algorithm level, and this is the paper's contribution.** The handle is an arbitrary reward function evaluated on intermediate states, used as a particle weight rather than as a gradient. Notably the direction requires no differentiable objective: "enables gradient-free control of attributes like toxicity" (p1). Nothing here is a biological handle. |
| `anti_memorization_design` | **NONE.** Not a concept the paper engages with. |
| `anti_memorization_control` | **NONE RUN.** |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE** in the pLDDT/pTM sense. The closest analogue is Figure 5 (p15), which reports the correlation between the reward evaluated on an intermediate state and the reward on the final sample, i.e. whether a partial state predicts the outcome. That question is the direct analogue of "is the conformation readable before it is fixed", and is the single most transferable result in the paper. |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| Comparison against a larger fine-tuned model (0.8B steered vs 2.6B fine-tuned) | that the gain merely reflects model capacity | p1, p3, Table 1 p10 |
| Steering applied on top of an already fine-tuned model | that steering and fine-tuning are redundant | Table 2, p11 |
| Comparison against gradient guidance | that a simpler gradient method suffices | Table 3, p11 |
| Particle-count scaling sweep | that the effect is not a compute artefact | Figure 4, p12 |
| Potential-choice ablation (max vs difference vs sum) | that the specific potential does not matter | Table 5 p14; Figure 7 p27 |
| λ and resampling-schedule ablation, reported as a diversity cost | that steering is free of a diversity penalty | Tables 9, 10, pp22; Figure 6 p26 |
| **Absent:** any biomolecular or structural evaluation | — | — |

## D. Claims

- **`central_conclusion`**: Diffusion models can be steered toward user-specified properties at
  inference time by running several particles, scoring intermediate states with a reward-derived
  potential, and resampling. On text-to-image generation this lets a 0.8B model beat a 2.6B
  fine-tuned model on prompt fidelity with no training; on text diffusion it lowers perplexity and
  gives gradient-free attribute control. The framework is presented as reward-agnostic and
  model-agnostic. It is never tested on a structure model.

- **`necessity_claims`** (verbatim + page):
  - p1: "Recent research proposes fine-tuning models to maximize rewards that capture desired
    properties, but **these methods require expensive training and are prone to mode collapse**."
  - p1: "However, **generating samples with user-specified properties remains a challenge**."
  - p2: "Gradient-based guidance presents an efficient alternative, but it is **limited to
    differentiable reward functions and continuous-state diffusion models**. Therefore, steering a
    diffusion model at inference-time with arbitrary rewards **remains a challenge**."

- **`novelty_claims`** (verbatim + page):
  - p1: "In this work, **we present Feynman-Kac (FK) steering, an inference-time framework for
    steering diffusion models with reward functions**."
  - p2: "In this work, we present Feynman-Kac steering (FK STEERING), **a flexible framework for
    steering diffusion-based generative models with arbitrary rewards** that uses FK interacting
    particle system methods."
  - p1: "**Our results demonstrate that inference-time scaling and steering of diffusion models –
    even with off-the-shelf rewards – can provide significant sample quality gains and
    controllability benefits.**"
  - p1: "we find that FK steering a 0.8B parameter model **outperforms a 2.6B parameter fine-tuned
    model on prompt fidelity, with faster sampling and no training**."

- **`stated_limits`**: **NOT FULLY EXTRACTED.** The discussion section was not read in full. One
  limitation is reported inside the results and is recorded here because it is the one that
  transfers: resampling reduces sample diversity, quantified against λ and the resampling schedule
  (Tables 9–10, p22; Figure 6, p26). A second-pass reading of the discussion is needed before any
  limitation is attributed to the authors. Flagged in `unresolved`.

- **`stance`**: `background` — **provisional, the user's call.** It is the definitional source for
  Feynman-Kac / SMC steering as an inference-time mechanism, and nothing more for this manuscript.
  It is **not** a precedent for conformational control, and it is **not** a threat to any
  structural novelty claim, because it contains no structural experiment. Cite it for the method's
  existence and provenance only.

## E. Quantitative comparators

- **`metrics_reported`**: **NONE COMPARABLE.** Every number in the paper is a GenEval, ImageReward,
  HPS, perplexity, or toxicity score. There is no metric in this paper that our results can be
  placed next to. Recorded as an explicit empty table rather than omitted:

| metric | value | units | measured against | page |
|---|---|---|---|---|
| *(none comparable to a structural result)* | — | — | — | — |

- **`n_predictions`**: Particle counts k are swept (Figure 4, p12; Table 8, p21 gives parameter
  counts and timing). Exact sample budgets NOT EXTRACTED.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI is held** — appendices and Tables 8–11, Figures 6–9 are inside the same
  arXiv PDF (pp21–27).

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 2 | Schematic of FK steering as a particle system with resampling | schematic | `SCHEMATIC \| particle trajectories with intermediate resampling \| no data` | 1 | — | arXiv non-exclusive licence; NOT REPORTED on PDF |
| 2 | 3 | Small steered models vs larger fine-tuned models, quality against compute | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 3 | 4 | Prompt fidelity and sample quality, independent sample vs steered | image grid | `RENDER \| facet: method (2) \| views: 1 \| overlay: none \| axis: none` | ≥2 rows | Curated image examples, no distribution shown | as above |
| 4 | 12 | Effect of scaling particle count | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 5 | 15 | Correlation between intermediate-state reward and final-state reward | scatter | `PLOT \| facet: NOT EXTRACTED \| vary: reward at intermediate state (continuous) \| series: NOT EXTRACTED \| measure: reward at final state \| n: NOT REPORTED` | — | — | as above |
| 6 | 26 | Effect of λ on diversity | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 7 | 27 | Max versus difference potential | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 8 | 27 | Effect of interval resampling on diversity | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 9 | 27 | Increased prompt fidelity, k=8 independent vs k=8 steered | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| Tables 1–11 | 10–23 | Quantitative results and ablations | table | not a figure | — | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-08
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium.** High on identity, venue, scope and the central negative (no
  structural experiment), all verified directly. Low on figure internals, sample budgets and the
  authors' own stated limitations, none of which were read in full.
- **`unresolved`**:
  1. `stated_limits` needs a second pass over the discussion.
  2. Sample budgets and particle counts per experiment.
  3. Whether the ICML camera-ready differs from arXiv v5 in any claim.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
peer-reviewed background
```

**Tag notes — and a vocabulary gap the user must rule on.**
- **No system tag is applied.** The fixed vocabulary in `SCHEMA.md` offers only `gpcr`, `kinase`,
  `transporter`, `periplasmic-binding`, `atpase`, `fold-switching` and `general-protein`. This
  paper studies images and text. `general-protein` would be a false statement that every
  system-level reverse lookup would then propagate, and SCHEMA v3 forbids inventing a tag. The
  honest outcome is a paper with no system tag, flagged here. **A `non-biomolecular` system tag
  should be added to the vocabulary**, or these papers stay unreachable by system.
- `latent-steering` **deliberately not applied**: the intervention is on particle weights, not on
  any internal tensor.
- `directed-state` **deliberately not applied**: there is no conformational state here.
- `comparator-numbers` **deliberately not applied**: no number in this paper is comparable to a
  structural result.
