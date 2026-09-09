# wu2023tds

> **Extraction provenance.** Extracted 2026-09-08 from the arXiv v2 PDF (`arXiv:2306.17775v2`,
> 23 Nov 2024). Abstract, contributions, method, the simulation study framing, the protein
> motif-scaffolding case study and the discussion were read; appendices were not. Figure inventory
> enumerated mechanically by page. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `wu2023tds` |
| `doi` | arXiv:2306.17775 (v1 30 Jun 2023, v2 23 Nov 2024) |
| `year`, `venue` | 2023 — **NeurIPS 2023**. `peer-reviewed`. |
| `title` | Practical and Asymptotically Exact Conditional Sampling in Diffusion Models |
| `authors` | Luhuan Wu\*, Brian L. Trippe\*, Christian A. Naesseth, David M. Blei, John P. Cunningham (Columbia; Naesseth at Amsterdam; \*equal contribution) |

**Why it is in this corpus.** TDS is the twisted sequential Monte Carlo algorithm that
`richman2025conformix` builds ConforMix on, and that `singhal2025fksteering` and
`passaro2025boltz2` sit alongside. It is the definitional source, and the only one of the four
SMC-family papers in the corpus with any protein experiment at all.

## B. Scope

| field | value |
|---|---|
| `system` | **general protein**, in one arm only. Three experiment families: a Gaussian simulation study, ImageNet class-conditional generation and inpainting, and **protein motif-scaffolding** (p9–10). The protein arm is **de novo design**, not conformational sampling of an existing protein. |
| `n_targets` | Motif-scaffolding benchmark problems from the RFdiffusion-era test set; the exact count is **NOT EXTRACTED** (Figure 3b, p10, reports "# problems with higher success rate" but the denominator was not read). Named test case: 5IUS (p10). |
| `method_class` | **other — inference-time conditional sampling.** Sequential Monte Carlo with twisting functions built from the denoised estimate x̂θ(xt); extended to Riemannian manifold diffusion for protein backbones. No retraining. |
| `backbones` | Image diffusion models for the vision arm; a Riemannian protein backbone diffusion model (FrameDiff-family) for the protein arm. **No co-folding model.** AF3, Boltz, Chai and Protenix do not appear. |
| `templates` | NOT APPLICABLE. |
| `msa_handling` | NOT APPLICABLE — the protein arm is backbone generation from noise, with no alignment input. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE for conformational state.** The protein arm generates scaffolds around a fixed functional motif; it does not produce two conformations of one sequence. Nothing in this paper is a conformational ensemble of a given protein. |
| `structural_priors_used` | **The motif itself.** Each scaffolding problem supplies the 3D coordinates of a functional motif taken from a deposited structure, as the conditioning information y. That is a structural prior by design and no methodological fault; it is what the task is. Protocol p9. |
| `oracle_leakage` | **Routes 1–3, 5–7 NOT APPLICABLE as written** — there is no target conformational state to leak. Recorded route by route so the absence is checkable.<br>**Route 1:** the motif coordinates are supplied as input by construction (p9). This is the task definition, not leakage, and belongs in `structural_priors_used`.<br>**Route 2:** NONE FOUND — no state database.<br>**Route 3:** NONE FOUND.<br>**Route 4 — PRESENT.** Particle count, twist scale and number of motif rotations are swept and the sweep is reported against benchmark success rate (Figure 3a, p10: "TDS motif-scaffolding success rate (test case 5IUS) improves with more particles, and degrees of freedom, and twist-scale"). Range selection is made on the evaluation set, which SCHEMA v3 counts as leakage even without a per-target value.<br>**Route 5:** success is defined by a self-consistency criterion (designability), not by RMSD to a held reference of the answer, so this route is **NONE FOUND** in the usual sense. The exact success predicate was **NOT EXTRACTED**.<br>**Route 6:** NOT DETERMINED.<br>**Route 7 — PRESENT, design-level.** Benchmark problems are ones with known solvable motifs. |
| `prospective` | **no.** Retrospective benchmark throughout; no designed protein is synthesised or assayed. |
| `state_metric` | **NOT APPLICABLE for conformational state.** The protein arm uses a designability / success-rate predicate; the vision arm uses conditional-mean estimation error and sample-quality scores. |
| `metric_saturation` | **NOT DETERMINED.** |
| `directional_control` | **Yes, at the algorithm level.** The handle is an arbitrary likelihood py\|x0(y\|x0) plus its twisting approximation. For proteins the direction is "place this motif", supplied by the operator as coordinates. No biological co-input handle. |
| `anti_memorization_design` | **NONE.** |
| `anti_memorization_control` | **NONE RUN.** |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE** — no pLDDT/pTM analogue is used or discussed. |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| Gaussian simulation study with exact ground truth | that the sampler is not actually asymptotically exact | p7, Figure 1 |
| Comparison against heuristic conditioning approaches | that a cheaper heuristic suffices | pp7, 10 |
| Particle-count sweep down to 2 particles | that the gain requires large compute | p1, p10 |
| Comparison against the conditionally trained state of the art | that inference-time conditioning cannot match training-time conditioning | p2, p10 |
| **Absent:** any conformational-state arm | — | — |

## D. Claims

- **`central_conclusion`**: Conditional sampling from an unconditional diffusion model can be made
  practical and asymptotically exact by treating it as sequential Monte Carlo with twisting
  functions computed from the denoised estimate. TDS applies across inpainting, class-conditional
  generation and, via a Riemannian extension, protein motif-scaffolding, where it allows more
  flexible conditioning criteria than a conditionally trained model and, on short scaffolds,
  higher success rates.

- **`necessity_claims`** (verbatim + page):
  - p1: "However, these achievements have primarily depended on **task-specific conditional
    training or error-prone heuristic approximations**."
  - p10: "**A limitation of TDS is its requirement for additional computes to simulate multiple
    particles.** While we observe improved performance with just two particles in some cases, **the
    optimal number is problem dependent**."

- **`novelty_claims`** (verbatim + page):
  - p1: "To this end, **we introduce the Twisted Diffusion Sampler, or TDS**."
  - p2: "(i) **We propose a practical SMC algorithm, Twisted Diffusion Sampler or TDS, for
    asymptotically exact conditional sampling from diffusion models**; (ii) We show that TDS applies
    to a range of conditional generation problems, and extends to Riemannian manifold diffusion
    models"
  - p2: "(iv) **On protein motif-scaffolding problems with short scaffolds TDS provides greater
    flexibility and achieves higher success rates than the state-of-the-art conditionally trained
    model.**"
  - p1: "on benchmark tasks, **TDS allows flexible conditioning criteria and often outperforms the
    state-of-the-art, conditionally trained** [model]"

- **`stated_limits`** (verbatim + page):
  - p10: "A limitation of TDS is its requirement for additional computes to simulate multiple
    particles. While we observe improved performance with just two particles in some cases, the
    optimal number is problem dependent."
  - Scope limit stated in the abstract and repeated at p2: the protein result is claimed for
    **short scaffolds** specifically, not for motif-scaffolding in general.

- **`stance`**: `background` — **provisional, the user's call.** Definitional source for twisted
  SMC in diffusion models, and the algorithmic ancestor of `richman2025conformix`. Not a precedent
  for conformational control: its protein arm designs new backbones around a fixed motif and never
  produces two states of one sequence.

## E. Quantitative comparators

| metric | value | units | measured against | page |
|---|---|---|---|---|
| Motif-scaffolding success rate, test case 5IUS | increases with particles, degrees of freedom and twist scale; **exact values NOT EXTRACTED** | % | designability criterion | p10, Fig 3a |
| Number of problems with higher success rate than the conditionally trained baseline | **NOT EXTRACTED** (denominator not read) | count | baseline comparison | p10, Fig 3b |
| ImageNet sample quality | reported in Table 1 | FID-family | 16k samples, 100 steps | p27 |

- **`n_predictions`**: particle counts swept; per-problem sample budgets **NOT EXTRACTED**.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI is held** — Appendices A–C are inside the same arXiv PDF (pp14–32).

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 7 | Conditional-mean estimation error across methods, 2 SEM bars, 25 replicates | line or point with error bars | `PLOT \| facet: NOT EXTRACTED \| vary: NOT EXTRACTED \| series: method (several) \| measure: conditional-mean estimation error \| n: 25 replicates per point` | — | — | arXiv non-exclusive licence; NOT REPORTED on PDF |
| 2 | 9 | ImageNet class-conditional generation with twist scaling | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 3A-B | 10 | Protein motif-scaffolding: success rate vs particles/DoF/twist scale (a); problems improved vs baseline (b) | line (a) + bar or count (b) | `PLOT \| facet: none (1) \| vary: particle count / twist scale (continuous) \| series: degrees of freedom \| measure: success rate \| n: NOT REPORTED` | 2 (a, b) | Panel (a) is a single test case (5IUS); the per-problem spread is only summarised in (b) | as above |
| Table 1 | 27 | ImageNet sample-quality comparison | table | not a figure | — | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-08
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium.** High on identity, venue, algorithm, scope and the central negative
  (no conformational-state arm). Low on the motif-scaffolding numbers, the success predicate and
  the figure internals, none of which were read in full.
- **`unresolved`**:
  1. The motif-scaffolding success predicate and its threshold.
  2. The benchmark problem count and the named baseline in Figure 3b.
  3. Oracle route 6 (best-of-N reporting) not determined.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
general-protein enhanced-sampling no-anti-memorization oracle-leak design-level-oracle
peer-reviewed background
```

**Tag notes.** `general-protein` is applied because the motif-scaffolding arm is genuinely a
protein experiment. `cofolding` is **deliberately not applied** — no co-folding model is used.
`latent-steering` is **deliberately not applied** — the intervention is on particle weights and on
the denoised coordinate estimate, never on an internal tensor. `directed-state` is **deliberately
not applied** — the conditioning is a motif placement, not a conformational state.
