# SCHEMA.md — extraction fields for the paper_af3 literature corpus

This file defines **what gets recorded about every paper**. It is static and short:
it is loaded on every query, so it must never accumulate per-paper data. Per-paper
data lives in `INDEX.md` (compact, all papers) and `notes/<citekey>.md` (full).

Field rules:

- Every field appears in every note. If the paper does not report it, write
  `NOT REPORTED` — never omit the line, and never infer a value.
- Anything that could become a sentence in the manuscript carries a page number.
- Necessity, impossibility and novelty claims are recorded **verbatim** with a page,
  because those are the sentences the paper's argument is built against and
  paraphrase silently softens them.

---

## A. Identity

| Field | Notes |
|---|---|
| `citekey` | Matches the PDF filename and the `refs.bib` key. |
| `doi` | Resolved DOI or arXiv/bioRxiv ID. |
| `year`, `venue` | Preprint status noted explicitly. |
| `title`, `authors` | First author + et al. is fine. |

## B. Scope

| Field | Notes |
|---|---|
| `system` | GPCR / kinase / transporter / general protein / other. |
| `n_targets` | How many proteins studied. A single-system paper claiming generality is worth flagging. |
| `method_class` | co-folding / MSA-subsampling / MD / enhanced sampling / clustering / benchmark-only / other. |
| `backbones` | AF2, AF3, Boltz, Chai, OF3, Protenix, other. |
| `templates` | on / off / NOT REPORTED. |
| `msa_handling` | full / subsampled / clustered / pinned / NOT REPORTED. |

## C. Conformational core

These are the axes the paper's novelty claim is measured against. Be strict here.

| Field | Notes |
|---|---|
| `states_generated` | one / two / ensemble / continuum. What did they actually produce, not what they say they could. |
| `oracle_leakage` | **The key field.** What knowledge of deposited structures of the target state entered the pipeline at any point: structures used as input or template; cluster labels derived from known states; hyperparameters, seeds or stopping criteria tuned against known states; success defined post hoc by RMSD to a structure they had. Quote the sentence that reveals it, with page. If genuinely absent, say `NONE FOUND` and give the page where the protocol is described so the claim is checkable. |
| `prospective` | yes / no / partial + one line why. Follows from `oracle_leakage`, not from the authors' own word for it. |
| `state_metric` | binary predicate / continuous coordinate / RMSD-to-reference / visual only. Record exact thresholds and their justification. |
| `metric_saturation` | Does the metric floor or ceiling in any arm they report? Relevant because a saturated predicate makes cells unresolvable and inverts conclusions. |
| `directional_control` | Can the method be *instructed* which state to produce, or does it only sample? Name the handle (partner, ligand, nanobody, seed, subsample depth). |
| `anti_memorization` | What control, on what set, and how many cases. `UNPOWERED` if fewer than ~10 or if the held-out set overlaps training. |
| `confidence_as_discriminator` | Did they use pLDDT/pTM/ipTM to judge conformational correctness, and did they validate that use? |

## D. Claims

| Field | Notes |
|---|---|
| `central_conclusion` | One or two sentences, own words. |
| `necessity_claims` | **Verbatim + page.** Any statement that X is required, essential, necessary, or that Y is not possible / cannot be done. These are the load-bearing sentences for contrast. |
| `stated_limits` | Limits the authors state themselves. Cheap insurance against being accused of attacking a strawman. |
| `stance` | `precedent` (we build on it) / `contrast` (we differ) / `threat` (it may pre-empt or contradict us) / `background`. One line of why. |

## E. Quantitative comparators

Numbers our results can be placed next to in a table.

| Field | Notes |
|---|---|
| `metrics_reported` | Metric name, value, units, what it was measured against, page. |
| `n_predictions` | Scale of their sampling, if reported. Needed for any "well-powered" comparison. |
| `comparable_to_ours` | Which of our numbers this sits beside, or `NONE`. |

## F. Figures

One row per figure. This table answers both "show me their figure" and
"what figure should I make for this data".

| Field | Notes |
|---|---|
| `fig_no`, `page` | Required. Without the page every retrieval re-reads the whole PDF. |
| `gist` | One line: what the figure shows. |
| `plot_type` | violin / box / scatter / line / heatmap / structure render / grid of small multiples / schematic. |
| `data_shape` | **The join key for figure-design queries.** Write as `<n conditions> × <n levels> → <what is on each axis>`. Example: `2 conditions × 5 systems → per-system violin of RMSD, faceted by condition`. This is what lets a query match on the shape of *your* data rather than on their subject matter. |
| `panels` | Panel count and whether panels are conditions or systems. |
| `hides` | Only when the figure obscures its own result: pooled where it should be per-system, bars hiding distributions, axes pinned at ceiling or floor, n not shown. Negative examples are more instructive than good ones. |
| `reuse` | License / permission status, if reproduction in the manuscript is conceivable. |

## G. Provenance

| Field | Notes |
|---|---|
| `extracted_on`, `extractor` | Date and which model/session. |
| `confidence` | high / medium / low, with what was hard to read. |
| `unresolved` | Anything the extractor could not determine. Do not silently drop these. |

---

## Tag vocabulary

Fixed list. Tags are the mechanism for reverse lookup ("which papers did X"), so
they must not drift — a tag invented on the fly is a tag no future query will find.
Adding a tag means editing this file and re-tagging the corpus.

**System:** `gpcr` `kinase` `transporter` `general-protein`

**Method:** `cofolding` `msa-subsample` `af-cluster` `md` `enhanced-sampling` `benchmark-only`

**State handling:** `single-state` `two-state` `ensemble` `continuum`

**Metric:** `binary-predicate` `continuous-metric` `rmsd-only` `saturating-metric`

**Rigour:** `oracle-leak` `prospective` `anti-memorization` `no-anti-memorization`
`unpowered` `confidence-as-discriminator`

**Control:** `directed-state` `partner-driven` `ligand-driven` `nanobody`
`apo-sampling` `seed-only`

**Relation to us:** `precedent` `contrast` `threat` `background` `negative-result`

**Utility:** `figure-exemplar` (kept mainly for its figures — may be outside our
field, and must be excluded from gap analysis) `comparator-numbers`
