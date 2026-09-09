# ekstromkelvinius2024discriminator

> **Extraction provenance.** Extracted 2026-09-08 from the arXiv v2 PDF (`arXiv:2310.15817v2`,
> 21 Sep 2024), cross-checked against the official PMLR proceedings entry. Abstract, method,
> results and appendix training details read; figure panels not viewed. See `confidence`.

## A. Identity

| field | value |
|---|---|
| `citekey` | `ekstromkelvinius2024discriminator` |
| `doi` | arXiv:2310.15817 (v1 24 Oct 2023, v2 21 Sep 2024); proceedings at `proceedings.mlr.press/v238/ekstrom-kelvinius24a.html` |
| `year`, `venue` | 2024 — **AISTATS 2024**, Proceedings of the 27th International Conference on Artificial Intelligence and Statistics, **PMLR volume 238, pages 3403–3411**. Verified directly against the PMLR entry. `peer-reviewed`. |
| `title` | Discriminator Guidance for Autoregressive Diffusion Models |
| `authors` | Filip Ekström Kelvinius, Fredrik Lindsten (Linköping University) |

## B. Scope

| field | value |
|---|---|
| `system` | **other — 2-D molecular graphs, not 3-D structures.** Datasets are QM9 and MOSES: molecules as graphs of nodes and edges. **No protein, no 3-D coordinate, no conformation appears anywhere.** The word "molecular" here means chemical graph topology, and mistaking it for structural generation would be a serious misreading. |
| `n_targets` | NOT APPLICABLE — two datasets. QM9 training used "75 % of the full dataset as training data (roughly 98 000 molecules)" (p14); the MOSES discriminator training set "consists of 200 000 samples, which is ∼ 10% the size of the original dataset" (p14). |
| `method_class` | **other — inference-time discriminator guidance for discrete diffusion.** Three variants proposed: ARDG (autoregressive discriminator guidance), BSDG and FADG, the latter two being sequential Monte Carlo schemes for the suboptimal-discriminator case. |
| `backbones` | Autoregressive Diffusion Models (ARDM). DiGress is the external comparator. No structure model. |
| `templates` | NOT APPLICABLE. |
| `msa_handling` | NOT APPLICABLE. |

## C. Conformational core

| field | value |
|---|---|
| `states_generated` | **NOT APPLICABLE — the model generates molecular graphs, not conformations.** |
| `structural_priors_used` | **NONE.** No 3-D structure enters the work at any point. |
| `oracle_leakage` | **Routes 1, 2, 3, 5, 6, 7 NOT APPLICABLE** — no target structure exists. **Route 4 — PRESENT:** the discriminator learning rate was "tweaked by observing cross entropy on a validation set which consisted of both real and generated samples" (p14), and generation order and particle count N are swept against the reported metrics (Tables 1–2, pp7–8; Table 8, p17). Validation-set tuning, disclosed. |
| `prospective` | **NOT APPLICABLE** — no generated molecule is synthesised or assayed. |
| `state_metric` | **NOT APPLICABLE for conformational state.** Metrics are validity, uniqueness, novelty, filter pass rate, Fréchet ChemNet Distance and SNN similarity. |
| `metric_saturation` | **Yes, on QM9, and the authors say so.** p8: "As the metrics on [QM9] are very good…" and the appendix repeats "The metrics are very good, as we h[ave]…" (Table 3, p15). Validity on QM9 is near ceiling for every method, so the dataset cannot separate them; the discriminating results are on MOSES (Table 2, p8: validity 82.2 → 90.1). |
| `directional_control` | **Yes, at the algorithm level.** The handle is a learned discriminator separating real from generated samples, applied either as a per-step reweighting (ARDG) or through SMC resampling (BSDG, FADG). As with `kim2023refining`, the discriminator separates real from generated, **not** one target class from another, and the analogy to class-directed steering must stop there. |
| `anti_memorization_design` | **Partial, and it is a chemistry-specific form.** MOSES reports a *novelty* metric and the authors additionally recompute metrics "only on novel molecules" (Table 5, p16), which isolates performance on outputs not present in training. That is closer to a memorization control than most papers manage. It is not a temporal or held-out-structure split. |
| `anti_memorization_control` | **RUN, in the novelty-restricted form above (Table 5, p16), and analysed.** Its scope is narrow: it addresses training-set copying of graphs, not memorization of a target answer, because there is no target answer here. |
| `controls_run` | see table below |
| `confidence_as_discriminator` | **NOT APPLICABLE** in the pLDDT sense. |

### `controls_run`

| control | what it rules out | page |
|---|---|---|
| ARDM baseline with no guidance | that the gain is not from the discriminator | Tables 1–2, pp7–8 |
| ARDM* — matched-training-time baseline | that the gain is bought with extra training compute | p8, Table 2 |
| Metrics recomputed on novel molecules only | that the gain is training-set copying | Table 5, p16 |
| Generation-order ablation (Uniform, NEsN, NEN) | that the effect depends on one ordering | Tables 1, 4, pp7, 15 |
| Different-seed replication of both datasets | that the result is a seed artefact | Tables 6–7, pp16–17 |
| Particle-count sweep on MOSES | that the SMC variants need large N | Table 8, p17 |
| DiGress external comparator | that a purpose-built graph diffusion model is better | p8 |

## D. Claims

- **`central_conclusion`**: Discriminator guidance, previously developed for continuous score-based
  diffusion, can be carried over to discrete autoregressive diffusion. An optimal discriminator
  provably corrects the pre-trained model to exact sampling from the data distribution; for a
  realistic suboptimal discriminator the authors derive sequential Monte Carlo schemes that fold
  the discriminator's predictions into generation step by step. On molecular graph generation
  (QM9, MOSES) the guided variants improve validity and distributional metrics over the ungudied
  ARDM, at an inference cost that scales with discriminator evaluations.

- **`necessity_claims`** (verbatim + page):
  - p9: "This improved performance **naturally comes with an increased computational cost as the
    discriminator needs to be evaluated at each generation step**. Additionally, for SMC we sample
    multiple particles in parallel for each generated sample."
  - p5: "**even in the extreme case N = 1**, the two versions of SMC that we propose below will
    reduce to standard ARDM and ARDG, respectively. We therefore argue that **even a small N can be
    used to improve the performance** compared to the respective baselines."

- **`novelty_claims`** (verbatim + page):
  - p1: "First, **we show that using an optimal discriminator will correct the pretrained model and
    enable exact sampling from the underlying data distribution**."
  - p1: "Second, to account for the realistic scenario of using a suboptimal discriminator, **we
    derive a sequential Monte Carlo algorithm which iteratively takes the predictions from the
    discriminator into account during the generation process**."
  - p1: "**We test these approaches on the task of generating molecular graphs and show how the
    discriminator improves the generative performance over using only the pretrained model.**"

- **`stated_limits`** (verbatim + page):
  - p9: the compute cost, quoted above ("evaluated at each generation step").
  - p8 and p15, the QM9 ceiling: the authors note the metrics on QM9 "are very good", i.e. the
    dataset has little headroom, and lean on MOSES for the discriminating comparison.
  - p14, a disclosed training-set difference against the comparator: for QM9 "we used 75 % of the
    full dataset as training data (roughly 98 000 molecules), **slightly less than DiGress which
    used 100 000 molecules**."

- **`stance`**: `background` — **provisional, the user's call.** Definitional source for
  discriminator guidance in the *discrete* diffusion setting, and the companion to
  `kim2023refining` in the continuous setting. Nothing structural. No threat to any structural
  novelty claim.

## E. Quantitative comparators

| metric | value | units | measured against | page |
|---|---|---|---|---|
| MOSES validity, ARDM (no guidance) | 82.2 | % | dataset | p8, Table 2 |
| MOSES validity, ARDM\* (matched training time) | 82.6 | % | dataset | p8, Table 2 |
| MOSES validity, ARDG | 80.5 | % | dataset | p8, Table 2 |
| MOSES validity, BSDG | 85.9 | % | dataset | p8, Table 2 |
| MOSES validity, FADG | 90.1 | % | dataset | p8, Table 2 |
| MOSES metrics on novel molecules only | reported separately | mixed | dataset | p16, Table 5 |
| QM9 metrics | near ceiling; authors call them "very good" | mixed | dataset | p7 Table 1, p15 Table 3 |

**None comparable to a structural result.** Note that plain ARDG is *worse* than the ungudied
baseline on MOSES validity (80.5 vs 82.2) and only the two SMC variants improve on it. Anyone
citing this paper for "discriminator guidance works" must cite the variant, not the family.

- **`n_predictions`**: sample counts per metric NOT EXTRACTED.
- **`comparable_to_ours`**: *(left empty by the extractor, per SCHEMA v3.)*
- **`si_in_scope`**: **SI is held** — Appendix A–C and Tables 3–8 are inside the same PDF (pp14–17).

## F. Figures

| fig_no | page | gist | plot_type | data_shape | panels | hides | reuse |
|---|---|---|---|---|---|---|---|
| 1 | 2 | Illustration of ARDG applied to graphs; nodes and edges revealed in an order | schematic | `SCHEMATIC \| autoregressive graph generation order with discriminator reweighting \| no data` | 1 | — | arXiv non-exclusive; PMLR v238 entry carries the proceedings licence, NOT CHECKED |
| Table 1 | 7 | QM9 metrics by generation order and guidance type | table | not a figure | — | QM9 metrics near ceiling, so differences are small | as above |
| Table 2 | 8 | MOSES metrics by guidance type, uniform order | table | not a figure | — | — | as above |
| Tables 3–8 | 15–17 | Appendix replications: no-hydrogen QM9, generation orders, novel-only metrics, seed replication, particle-count sweep | table | not a figure | — | — | as above |

**The paper contains exactly one figure and eight tables.** That is unusual enough to record: a
figure-design query will find nothing reusable here.

## G. Provenance

- **`extracted_on`**: 2026-09-08
- **`extractor`**: Claude Opus 5, session `012o2XWtza3uVnp772dQHctU`
- **`schema_version`**: `v3`
- **`confidence`**: **medium-high.** Identity and venue verified against PMLR directly, including
  page range. Scope, mechanism, the MOSES table and the controls read directly. Low only on the
  full metric tables and the licence of the proceedings version.
- **`unresolved`**:
  1. Full QM9 and MOSES metric tables were read for validity only, not for FCD/SNN/filters.
  2. The PMLR proceedings licence was not checked; the arXiv posting's licence is not stated on
     the PDF.
  3. Sample counts behind each metric.
- **`why_it_matters`**: *(left empty by the extractor — the user's call.)*

## Tags

```
enhanced-sampling anti-memorization peer-reviewed background
```

**Tag notes — same vocabulary gap as `singhal2025fksteering` and `kim2023refining`.** No system tag
is applied: QM9 and MOSES are 2-D molecular graphs and the fixed vocabulary has no value for them.
`anti-memorization` **is** applied, on the strength of the novel-molecules-only arm (Table 5, p16),
with the scope caveat recorded in `anti_memorization_design`. `latent-steering` is **deliberately
not applied**. `saturating-metric` is **deliberately not applied** for the same reason as in
`kim2023refining`: it would false-positive conformational-state metric queries.
