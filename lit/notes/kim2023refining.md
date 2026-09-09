# kim2023refining

> **Extraction provenance.** Extracted 2026-09-08 from the arXiv v4 PDF (`arXiv:2211.17091v4`,
> 4 Jun 2023). Abstract, method and results scope read directly; the 48-page appendix was
> enumerated by page and caption, not read. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `kim2023refining` |
| `doi` | arXiv:2211.17091 (v1 28 Nov 2022, v4 4 Jun 2023) |
| `year`, `venue` | 2023 — **ICML 2023**, stated on the arXiv record. `peer-reviewed`. |
| `title` | Refining Generative Process with Discriminator Guidance in Score-based Diffusion Models |
| `authors` | Dongjun Kim\*, Yeongmin Kim\*, Se Jung Kwon, Wanmo Kang, Il-Chul Moon (KAIST; NAVER Cloud; Summary.AI; \*equal contribution) |

## B. Scope

| field | value |
|---|---|
| `system` | **other — not a biomolecular paper.** Image generation only: CIFAR-10, CelebA 64×64, FFHQ 64×64, ImageNet 256×256, plus an image-to-image translation arm. **No protein, no molecule, no structure appears anywhere.** |
| `n_targets` | NOT APPLICABLE — four image datasets. |
| `method_class` | **other — inference-time guidance.** A discriminator is trained *after* the score network is frozen, and its density-ratio gradient is added as a correction to the pre-trained score during sampling. |
| `backbones` | EDM, LSGM, ADM, DiT-XL/2, Soft Truncation, SDEdit. No structure model. |
| `templates` | NOT APPLICABLE. |
| `msa_handling` | NOT APPLICABLE. |

## C. Conformational core

Every field is `NOT APPLICABLE`, and that is a property of the paper. Recorded field by field so a
reverse lookup cannot mistake absence for oversight.

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE.** |
| `structural_priors_used` | **NONE.** |
| `oracle_leakage` | **Routes 1, 2, 3, 5, 6, 7 NOT APPLICABLE** — no target structure exists. **Route 4 — PRESENT** in the analogous form: the discriminator-guidance weight w<sub>t</sub>, the noise range over which guidance is applied, the discriminator training epoch and the Bregman divergence choice are all swept and selected against benchmark FID (Figures 9, 10, 17, 18, 20, 21, 29, 30; Tables 7, 10). Range selection on the evaluation set. |
| `prospective` | **NOT APPLICABLE.** |
| `state_metric` | **NOT APPLICABLE.** Metrics are FID, sFID, Inception Score, precision, recall, F1 and NLL. |
| `metric_saturation` | **Yes, and the authors make it their headline.** FID 1.83 with recall 0.64 on ImageNet 256×256 is reported against the validation data's own FID 1.68 and recall 0.66 (p1, p7), i.e. the metric is within noise of its achievable floor and can no longer separate methods on that dataset. Quoted verbatim under `novelty_claims`. |
| `directional_control` | **Yes, at the algorithm level.** The handle is a learned discriminator between real and generated data, applied as a score correction. This is the closest published analogue in the corpus to "train a classifier on partially denoised states and use it as a control signal", and the analogy should be stated at that level and no further: the discriminator here separates *real from generated*, not one target class from another. |
| `anti_memorization_design` | **NONE.** |
| `anti_memorization_control` | **NONE RUN.** |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE** in the pLDDT sense. |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| Blind discriminator (d ≡ 0.5) baseline | that the gain comes from anything other than discriminator signal | p4, Table 1 |
| All EDM/LSGM hyperparameters held fixed | that the gain comes from retuning the base sampler | p7 |
| Discriminator-training-epoch ablation | that the effect is an artefact of one checkpoint | Figs 10, 29, pp8, 27 |
| Comparison against Classifier Guidance, and combined with it | that discriminator guidance duplicates classifier guidance | p2, Fig 2; Table 10 p24 |
| NFE ablation | that the gain is bought with extra function evaluations | Fig 9 p8; Fig 31 p28 |
| Component-wise compute budget table | that the cost is hidden | Table 6, p7 |

## D. Claims

- **`central_conclusion`**: A discriminator trained after score training, and used to estimate the
  gap between the true and the learned score, can be added as a correction term during sampling to
  refine a frozen diffusion model. Training the discriminator separately rather than jointly makes
  it stable and fast to converge. The method reaches state-of-the-art image-generation numbers and
  improves precision and recall simultaneously, which classifier guidance alone does not.

- **`necessity_claims`** (verbatim + page):
  - p1: "The proposed method, Discriminator Guidance, aims to improve sample generation of
    pre-trained diffusion models."
  - *(Further necessity/impossibility statements were not extracted; the discussion and Section 3.3
    analysis were read for structure only. Flagged in `unresolved`.)*

- **`novelty_claims`** (verbatim + page):
  - p1: "Specifically, **we propose using a discriminator as an auxiliary degree of freedom to the
    pre-trained model**."
  - p1: "Using our algorithm, **we achive state-of-the-art results on ImageNet 256x256 with FID
    1.83 and recall 0.64, similar to the validation data's FID (1.68) and recall (0.66)**." (sic,
    "achive")
  - p5: "we can interpret that **Discriminator Guidance introduces an additional axial degree of
    freedom ϕ that reparametrizes the score error Eθ∞ into a discriminator-adjusted score error
    Eθ∞,ϕ**." *(The PDF text layer renders this as "discriminatoradjusted" because the hyphen falls
    on a line break; the hyphen is restored here and the artifact is recorded so a future quote
    check does not flag it as fabricated.)*

- **`stated_limits`**: **NOT FULLY EXTRACTED.** Two future directions are named at p9 (rewriting in
  terms of Bregman divergence; simultaneous training of score and discriminator networks), and the
  compute cost is disclosed in Table 6 (p7). A second pass is needed before attributing any
  limitation to the authors. Flagged in `unresolved`.

- **`stance`**: `background` — **provisional, the user's call.** Definitional source for
  discriminator guidance in continuous score-based diffusion. Cite for the mechanism's provenance
  only. It is not a precedent for anything structural and threatens no structural novelty claim.

## E. Quantitative comparators

| metric | value | units | measured against | page |
|---|---|---|---|---|
| ImageNet 256×256, FID | 1.83 | FID | validation data FID 1.68 | p1, p7 |
| ImageNet 256×256, recall | 0.64 | fraction | validation data recall 0.66 | p1, p7 |
| CIFAR-10, unconditional FID (EDM-G++) | 1.77 | FID | dataset | p6, Table 3; Fig 47 p44 |
| CIFAR-10, conditional FID (EDM-G++) | 1.64 | FID | dataset | Fig 48, p45 |
| CIFAR-10, LSGM-G++ FID | 1.94 | FID | dataset | Fig 46, p43 |
| CelebA, Soft-Truncation-G++ FID | 1.34 | FID | dataset | Fig 49, p46 |
| FFHQ, EDM-G++ FID | 1.98 | FID | dataset | Fig 50, p47 |

**None of these is comparable to a structural result.** They are recorded so the paper's own
performance claims are checkable, not because they can sit next to our numbers.

- **`n_predictions`**: sample counts per FID evaluation NOT EXTRACTED.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI is held** — appendices A–D and Figures 14–51 are inside the same arXiv
  PDF (pp14–48).

## F. Figures

51 figures and 10 tables, enumerated by page. Figures 32–51 (pp29–48) are uncurated image sample
grids and carry no measured data. Only the rows a future query could plausibly want are given
`data_shape`; the rest are marked as not viewed.

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 1 | Denoising process with and without discriminator guidance | schematic | `SCHEMATIC \| two denoising trajectories, corrected and uncorrected \| no data` | 2 | — | arXiv non-exclusive; NOT REPORTED |
| 3 | 4 | FID against discriminator training epochs on CIFAR-10 | line | `PLOT \| facet: none (1) \| vary: discriminator training epoch 0–60 (continuous) \| series: method (2: EDM, EDM-G++) \| measure: FID \| n: NOT REPORTED` | 1 | — | as above |
| 5 | 5 | FID and recall trade-off on DiT-XL-G++ | scatter or line | `PLOT \| facet: none (1) \| vary: guidance strength (continuous) \| series: NOT EXTRACTED \| measure: FID and recall \| n: NOT REPORTED` | — | — | as above |
| 8 | 8 | Sample trajectories with respect to the density ratio, FFHQ | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 10 | 8 | Precision and recall by discriminator training | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 11 | 8 | Loss contribution by noise scale | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | **Directly analogous to a readability-vs-noise-level curve**, which is why this row is kept | as above |
| 15–16 | 17–18 | 2-D bimodal Gaussian toy case, adjusted score visualised | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 20 | 21 | Guidance sweet spot shifts to small t₀ | NOT EXTRACTED (panel not viewed) | NOT EXTRACTED | — | — | as above |
| 32–51 | 29–48 | Uncurated sample grids | image grid | `RENDER \| facet: model (several) \| views: 1 \| overlay: none \| axis: none` | many | Qualitative only | as above |
| Tables 1–10 | 4–24 | Quantitative results and ablations | table | not a figure | — | — | as above |

## G. Provenance

- **`extracted_on`**: 2026-09-08
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium.** High on identity, venue, scope, mechanism and the headline numbers.
  Low on `necessity_claims`, `stated_limits` and every appendix figure.
- **`unresolved`**:
  1. `necessity_claims` and `stated_limits` both need a second pass.
  2. Figure 11 ("Loss contribution by noise scale") should be viewed properly — it is the closest
     published analogue to a noise-level readability curve and may be directly reusable.
  3. Sample counts behind each FID.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
peer-reviewed background
```

**Tag notes — same vocabulary gap as `singhal2025fksteering`.** No system tag is applied, because
the fixed vocabulary has no value for a non-biomolecular paper and inventing one is forbidden by
SCHEMA v3. `latent-steering` is **deliberately not applied**: the correction is added to the score,
not to an internal representation. `saturating-metric` is **deliberately not applied** despite the
FID ceiling, because that tag is used in this corpus for conformational-state metrics and applying
it here would false-positive every state-metric query.
