# SCHEMA.md — extraction fields for the paper_af3 literature corpus

**Version 2** (2026-09-07). Revised after a pilot extraction of
`obendorf2026statespecific` exposed eight defects in v1. Changes are listed at the
bottom under **Changelog**; v1 is preserved as `SCHEMA.v1.md`. Any note written
against v1 must be re-extracted.

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
- Where a field's value is genuinely dual, say so rather than picking one. A forced
  single value is a lie the index then propagates.

---

## A. Identity

| Field | Notes |
|---|---|
| `citekey` | Matches the PDF filename and the `refs.bib` key. |
| `doi` | Resolved DOI or arXiv/bioRxiv ID. |
| `year`, `venue` | Preprint status noted explicitly, and tagged `preprint`. |
| `title`, `authors` | First author + et al. is fine. |

## B. Scope

| Field | Notes |
|---|---|
| `system` | GPCR / kinase / transporter / general protein / other. |
| `n_targets` | How many proteins studied. A single-system paper claiming generality is worth flagging. |
| `method_class` | co-folding / MSA-subsampling / MSA-state-filtering / template-biasing / MD / enhanced sampling / clustering / benchmark-only / other. |
| `backbones` | AF2, AF3, Boltz, Chai, OF3, Protenix, other. If more than two are compared head to head, tag `multi-backbone`. |
| `templates` | on / off / state-annotated / NOT REPORTED. |
| `msa_handling` | full / subsampled / clustered / state-filtered / pinned / NOT REPORTED. Note that **subsampled and state-filtered are different things**: one reduces depth, the other substitutes a state-specific alignment. Do not collapse them. |

## C. Conformational core

These are the axes the paper's novelty claim is measured against. Be strict here.

| Field | Notes |
|---|---|
| `states_generated` | one / two / ensemble / continuum. What did they actually produce, not what they say they could. |
| `oracle_leakage` | **The key field.** What knowledge of deposited structures of the target state entered the pipeline at any point: structures used as input or template; state annotations from a curated database (GPCRdb, KLIFS, Kincore) used to build templates or alignments; cluster labels derived from known states; hyperparameters, seeds or stopping criteria tuned against known states; success defined post hoc by RMSD to a structure they had; best/worst model labels assigned against a held reference. Enumerate **every route separately**, each with a verbatim quote and page. If genuinely absent, say `NONE FOUND` and give the page where the protocol is described so the claim is checkable. |
| `prospective` | yes / no / partial + one line why. Follows from `oracle_leakage`, not from the authors' own word for it. A paper may be prospective in its targets and retrospective in its biasing pipeline; say so. |
| `state_metric` | binary predicate / continuous coordinate / RMSD-to-reference / visual only. Record exact thresholds and their justification. |
| `metric_saturation` | Does the metric floor or ceiling in any arm they report? Also record **axis breaks and truncations**, which hide saturation visually rather than numerically. Relevant because a saturated predicate makes cells unresolvable and inverts conclusions. |
| `directional_control` | Can the method be *instructed* which state to produce, or does it only sample? Name the handle (partner, ligand, nanobody, peptide, state-annotated template, state-filtered MSA, seed, subsample depth). |
| `anti_memorization_design` | Is there a held-out or post-cutoff set at all? Give n and how the cutoff was defined. `NONE` if absent. |
| `anti_memorization_control` | Was a control **arm actually run and analysed**, as opposed to a held-out set merely existing? `NONE RUN` is a distinct and common answer. Mark `UNPOWERED` if n < ~10 or the held-out set overlaps training. These two fields were one field in v1, which made "they had recent structures but never used them as a control" unrecordable. |
| `confidence_as_discriminator` | Did they use pLDDT/pTM/ipTM to judge conformational correctness, and did they validate that use? |

## D. Claims

| Field | Notes |
|---|---|
| `central_conclusion` | One or two sentences, own words. |
| `necessity_claims` | **Verbatim + page.** Any statement that X is required, essential, or necessary, or that Y is not possible / cannot be done. These are the load-bearing sentences for contrast. |
| `novelty_claims` | **Verbatim + page.** Any claim to be first, novel, or unprecedented. Recorded separately from necessity claims because these are what a priority dispute turns on. |
| `stated_limits` | Limits the authors state themselves. Cheap insurance against being accused of attacking a strawman. |
| `stance` | `precedent` / `contrast` / `threat` / `background`. **A paper may hold two stances** — commonly `precedent` on findings and `contrast` on rigour. Write both, separated by ` + `, each with one line of why. Provisional until the user confirms; extractors must not present it as settled. |

## E. Quantitative comparators

Numbers our results can be placed next to in a table. **Render as a table**, one row
per metric — a prose field here is not parseable later.

| Field | Notes |
|---|---|
| `metrics_reported` | Table with columns: `metric` \| `value` \| `units` \| `measured against` \| `page`. One row per metric. |
| `n_predictions` | Scale of their sampling. Record samples per target, targets, and total separately; a single total is rarely what a power comparison needs. |
| `comparable_to_ours` | Which of our numbers this sits beside, or `NONE`. Hedge explicitly if the comparison needs a caveat. |

## F. Figures

One row per **panel group**, not per figure. A figure whose panels have different
data shapes (say, a bar chart plus two scatters) gets one row per shape, sharing a
`fig_no` with a letter suffix: `4A`, `4B-C`. Forcing heterogeneous panels into one
row produces a compound `data_shape` string that will not join against anything.

This table answers both "show me their figure" and "what figure should I make for
this data".

| Field | Notes |
|---|---|
| `fig_no`, `page` | Required. Use letter suffixes for panel groups. Without the page every retrieval re-reads the whole PDF. |
| `gist` | One line: what the figure shows. |
| `plot_type` | violin / box / scatter / line / bar / heatmap / structure render / grid of small multiples / schematic. |
| `data_shape` | **The join key for figure-design queries.** Use the grammar below. Describes the SHAPE of the data, never its subject matter. |
| `panels` | Panel count, and whether panels vary by condition, system, or view. |
| `hides` | Only when the figure obscures its own result: pooled where it should be per-system, bars hiding distributions, axes pinned or **broken**, n not shown, a claimed result with no quantitative panel at all. Leave blank otherwise. Negative examples are more instructive than good ones. |
| `reuse` | License and, critically, whether it carries an **ND (no derivatives)** clause, which forbids redrawing as well as modifying. Record the page the license appears on. |

### The `data_shape` grammar

v1 used `<n conditions> × <n levels> → <axes>`. That form has two defects: it
presupposes a plot with axes, so it cannot describe a structure render, and it does
not say **which slot is the facet**, so two extractors can write the same figure
two incompatible ways. Both are fixed by naming the roles explicitly.

Pick the form that matches the figure. Always use `key: value` pairs separated by
` | `, and always in the order given.

**Form 1 — quantitative plot (anything with axes):**

```
PLOT | facet: <variable> (<n>) | x: <variable> (<n>) | y: <measure> | mark: <bar|violin|box|point|line|cell> | n_per_cell: <k or NOT REPORTED>
```

`facet` is what splits the figure into sub-panels. `x` is what varies along the
horizontal within a panel. If there is no faceting, write `facet: none (1)`.
`n_per_cell` is how many underlying observations sit behind each mark — the number
that reveals whether a bar is hiding a distribution.

Worked example: `PLOT | facet: system (4) | x: model × input condition (20) | y: RMSD (Å) | mark: bar + overlaid point strip | n_per_cell: 5`

**Form 2 — structure render (no data axes):**

```
RENDER | systems: <n> | views: <n> (<what the views are>) | overlay: <k> predictions on <n> reference(s) | axis: none
```

Worked example: `RENDER | systems: 3 | views: 2 (ligand pose, ICL3 backbone) | overlay: ~20 predictions on 1 reference | axis: none`

**Form 3 — schematic, workflow, or any figure carrying no data:**

```
SCHEMATIC | <one line on what it depicts> | no data
```

Matching happens within a form. A `PLOT` row never joins against a `RENDER` row,
which is the point: if the user has quantitative data, structure renders are not
candidate designs for it.

## G. Provenance

| Field | Notes |
|---|---|
| `extracted_on`, `extractor` | Date and which model/session. |
| `schema_version` | `v2`. Notes written against an older schema are stale and must be re-extracted. |
| `confidence` | high / medium / low, with what was hard to read. |
| `unresolved` | Anything the extractor could not determine. Do not silently drop these. |
| `why_it_matters` | **Left empty by the extractor.** This is the user's call. |

---

## Tag vocabulary

Fixed list. Tags are the mechanism for reverse lookup ("which papers did X"), so
they must not drift — a tag invented on the fly is a tag no future query will find.
Adding a tag means editing this file and re-tagging the corpus.

**System:** `gpcr` `kinase` `transporter` `general-protein`

**Method:** `cofolding` `msa-subsample` `msa-state-filter` `template-state-bias`
`af-cluster` `md` `enhanced-sampling` `benchmark-only`

**State handling:** `single-state` `two-state` `ensemble` `continuum`

**Metric:** `binary-predicate` `continuous-metric` `rmsd-only` `saturating-metric`

**Rigour:** `oracle-leak` `prospective` `anti-memorization` `no-anti-memorization`
`unpowered` `confidence-as-discriminator` `multi-backbone`

**Control:** `directed-state` `partner-driven` `ligand-driven` `peptide-driven`
`nanobody` `apo-sampling` `seed-only`

**Site:** `orthosteric` `allosteric-site` `cryptic-pocket`

**Publication:** `preprint` `peer-reviewed`

**Relation to us:** `precedent` `contrast` `threat` `background` `negative-result`

**Utility:** `figure-exemplar` (kept mainly for its figures — may be outside our
field, and must be excluded from gap analysis) `comparator-numbers`

---

## Changelog: v1 → v2

Every change below was forced by a specific failure in the pilot extraction of
`obendorf2026statespecific`, not by taste.

1. **`data_shape` gained a three-form grammar.** Three of that paper's five figures
   were structure renders with no axes; the v1 grammar could not describe them and
   the extractor had to distort them into it.
2. **`data_shape` slots are now named.** v1's worked example put conditions in the
   facet slot while the extractor put them on the x-axis. Both readings were
   defensible, which means the join key silently breaks across extractors.
3. **Figure rows are now per panel group.** A figure with a bar panel and two
   scatters is two shapes; v1 forced one row and produced a compound string.
4. **`novelty_claims` added to the D table.** v1's preamble required it; the table
   omitted it.
5. **`metrics_reported` is now explicitly a table.** It asks for five things per
   metric and was specified as a single field.
6. **`anti_memorization` split into `_design` and `_control`.** The pilot paper has
   seven post-cutoff structures and never runs them as a control arm. v1 had no way
   to record that distinction, which is exactly the distinction the gap argument
   rests on.
7. **`stance` may hold two values.** The pilot paper is precedent on findings and
   contrast on rigour; forcing one loses the half that matters.
8. **Five tags added:** `msa-state-filter` and `template-state-bias` (the pilot
   paper's two primary state handles, and `msa-subsample` is wrong for both),
   `allosteric-site` / `cryptic-pocket`, `multi-backbone`, and
   `preprint` / `peer-reviewed`.
9. **`reuse` now calls out ND clauses**, which forbid redrawing, not just copying.
10. **`metric_saturation` now covers axis breaks**, which hide saturation visually
    rather than numerically.
