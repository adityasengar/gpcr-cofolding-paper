# SCHEMA.md — extraction fields for the paper_af3 literature corpus

**Version 3** (2026-09-07). Revised after five parallel extractions against v2
independently hit the same walls. When five extractors reading five different papers
report the same defect, it is structural, not taste. Changes are at the bottom under
**Changelog v2 → v3**; v1 and v2 are preserved as `SCHEMA.v1.md` and `SCHEMA.v2.md`.

Notes carrying `schema_version: v2` are **partially stale**: their A–E content is
unaffected by the v3 changes, but their figure tables and tag lists were written
against the older grammar and vocabulary. They need a figure-and-tags re-pass, not a
full re-extraction.

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
| `states_generated` | one / two / ensemble / continuum. What did they actually produce, not what they say they could. **May be dual, joined by ` + `** — "ensemble + single-state" is the correct answer for a method that samples broadly and collapses onto one basin, and that collapse is usually the paper's actual result. For a paper that displaces an existing equilibrium rather than generating structures (wet-lab), write `NOT APPLICABLE — equilibrium displaced, nothing generated`. |
| `structural_priors_used` | **New in v3, and required for every paper.** What deposited structural knowledge shaped the work at *design* time, as distinct from leaking into the *pipeline*. A wet-lab paper that designs a peptide from a solved complex has used a structural prior and committed no methodological sin; `oracle_leakage` had nowhere honest to record that and forced extractors to either mislabel it or drop it. Prediction papers fill this too: it is where "we picked these systems because both states are deposited" belongs. |
| `oracle_leakage` | **The key field.** What knowledge of deposited structures of the target state entered the pipeline at any point. Enumerate **every route separately**, each with a verbatim quote and page, and say `NONE FOUND` per route where a route is genuinely absent, giving the page where the protocol is described so the claim is checkable. The routes to check, each considered separately: (1) structures used as input or template; (2) state annotations from a curated database (GPCRdb, KLIFS, Kincore) driving templates or alignments; (3) cluster labels derived from known states; (4) hyperparameters, sweep ranges, seeds or stopping criteria tuned against known states — **note that tuning a *range* on the evaluation set is leakage even when no single value is picked per target**; (5) success defined post hoc by RMSD or TM to a structure they had; (6) best/worst model labels assigned against a held reference; (7) **design-level oracle use — input conditions or systems chosen because the expected answer is already known.** Route 7 is new in v3: a paper can feed the model nothing leaky and still declare the expected state before reading the result. That is a weaker finding than pipeline leakage and must be labelled as design-level, not conflated with it. |
| `prospective` | yes / no / partial + one line why. Follows from `oracle_leakage`, not from the authors' own word for it. A paper may be prospective in its targets and retrospective in its biasing pipeline; say so. |
| `state_metric` | binary predicate / continuous coordinate / RMSD-to-reference / visual only. **May be dual, joined by ` + `** — a paper that scores placement by RMSD and calls the state by eye is doing both, and forcing one loses the half that is the rigour defect. Record exact thresholds and their justification, or `NOT REPORTED` where a threshold is used but never stated. |
| `metric_saturation` | Does the metric itself floor or ceiling in any arm they report? **Numeric saturation only.** Axis breaks and truncations are a *figure* defect and belong in `hides`, not here — v2 left this undefined and three extractors recorded the same axis break twice. Cross-reference the figure row rather than duplicating. |
| `directional_control` | Can the method be *instructed* which state to produce, or does it only sample? Name the handle (partner, ligand, nanobody, peptide, state-annotated template, state-filtered MSA, seed, subsample depth). |
| `coinput_composition` | **New in v3.1, and required for every paper that supplies anything alongside the receptor.** List *every* molecule handed to the model or added to the system in each arm, and then answer the attribution question explicitly: **can the paper separate the contribution of one co-input from another, or were they supplied together?** Write it as one line per arm, e.g. `arm 2: receptor + agonist + Ga-b-g (together, never separated)`. This field exists because the same confound was found independently in three of the strongest partner papers in the corpus and none of them flags it: `ye2026multistatebias` and `zhang2026generalization` both supply agonist and transducer in a single condition and have no partner-alone arm, and `chiesa2025templatebias` has no decoy or scrambled-partner arm. `directional_control` records *that* there is a handle; this field records **what else was in the tube at the same time**, which is what decides whether a causal claim survives. Where a paper truly varies one co-input at a time, say so — that is the rare and citable case. |
| `binding_order` | **New in v3.1.** Which mechanistic route to the ternary complex the paper assumes, tests or supports, and with what evidence. GPCR activation is not a single sequence: agonist may bind first and the transducer engage a receptor already shifted toward active (**conformational selection at the ligand level, induced fit at the transducer level**), or receptor and G protein may be **pre-coupled** before agonist arrives, with the complex sitting in an activation intermediate until agonist and nucleotide release drive it on. Most papers in this corpus never state which they assume, and that silence is itself the answer — write `NOT ADDRESSED` rather than inferring one. For prediction papers, note additionally that co-folding has **no notion of order at all**: everything is supplied simultaneously, so any predicted complex is order-agnostic by construction and cannot adjudicate between the routes. Say that explicitly where it applies, because it bounds what a prediction result can claim about mechanism. |
| `input_factor_design` | **New in v3.2, and required for every paper that runs a prediction.** Record which *input* factors the paper varied and, for each pair, whether they were **CROSSED** (both varied independently, so their interaction is estimable), **HELD** (one varied while the other stayed fixed), or **CONFOUNDED** (changed together in a single condition, so neither is attributable). The four factors that matter in this literature are **MSA** (full / subsampled / masked / clustered / absent / state-filtered), **templates** (off / on / state-annotated), **ligand** (absent / present / varied), **partner** (absent / present / truncated / decoy / scrambled). Write one line per factor, then a `crossings:` line naming only the non-obvious pairs, e.g. `crossings: MSA x ligand HELD (ligand present in every arm, never removed); partner x ligand CONFOUNDED`. <br><br>**Why this is separate from `coinput_composition`.** That field answers *what else was in the tube*; this one answers *what was turned independently*. The distinction is not cosmetic: answering "has anyone crossed a ligand co-input with MSA subsampling?" required opening sixty notes and reading two fields against each other, because a paper can supply a ligand in every arm (so `coinput_composition` looks rich) while never varying it (so no interaction is estimable). `jung2026boltzperturb` is the worked example — ligand present throughout, MSA masked and subsampled in baseline arms, and therefore **MSA x ligand HELD, not crossed**, which is exactly why its negative result does not settle the question it appears to settle. Where a paper genuinely crosses two input factors, tag it `factors-crossed`; that is rare and citable. **Note for anyone backfilling in bulk: notes use three different field styles** — a markdown table row, a `- **field**:` bullet, and a `### \`field\`` heading. A script that anchors on only one will silently skip the others. |
| `anti_memorization_design` | Is there a held-out or post-cutoff set at all? Give n and how the cutoff was defined. `NONE` if absent. |
| `anti_memorization_control` | Was a control **arm actually run and analysed**, as opposed to a held-out set merely existing? `NONE RUN` is a distinct and common answer. Mark `UNPOWERED` if n < ~10 or the held-out set overlaps training. These two fields were one field in v1, which made "they had recent structures but never used them as a control" unrecordable. |
| `controls_run` | **New in v3.** A short table of every control arm the paper actually ran, with what each rules out: columns `control` \| `what it rules out` \| `page`. For prediction papers this is decoys, shuffles, apo arms, scrambled partners. For wet-lab papers it is unstapled peptide, scrambled sequence, no-peptide, off-target receptor. v2 had nowhere to put these and an extractor smuggled a twelve-row control table into `stated_limits`; that table was the most reusable content in the note. |
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
| `comparable_to_ours` | **Extractors leave this EMPTY.** Removed from extraction in v3. An extractor cannot see our numbers, so anything written here is a guess dressed as a finding — one correctly refused to fill it. Populated later, by whoever holds `STATUS.md` and the manuscript. |
| `si_in_scope` | Whether the paper's real numbers live in supplementary material not present in the PDF. Several papers put every potency value or per-target result in an SI table the corpus does not hold, which silently empties `metrics_reported`. Record `SI NOT HELD` where that happens so the gap is visible rather than looking like the paper reported nothing. |

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

Slots are named by **role, not by screen position**. A Cleveland dot plot with the
measure running horizontally still puts the measure in `measure:`. Roles always win
over where the ink sits; v2 named slots `x` and `y` and an extractor correctly
objected that a transposed plot then has nowhere legal to go.

Pick the form that matches. Always `key: value` pairs separated by ` | `, in the
order given. Matching happens **within a form** — a `PLOT` row never joins a
`RENDER` row, which is the point: if you hold quantitative data, structure renders
are not candidate designs for it.

**Form 1 — PLOT.** Anything with a dependent measure.

```
PLOT | facet: <var> (<n>) | vary: <var> (<n> or continuous range) | series: <var> (<n>) | measure: <what> | mark: <bar|violin|box|point|line> | n: <per mark, and per panel>
```

- `facet` splits the figure into sub-panels. No faceting: `facet: none (1)`.
- `vary` is the categorical or continuous variable running along the independent
  axis. For a continuous axis give the range, not a level count:
  `vary: emission wavelength 430–510 nm (continuous)`.
- `series` is the **colour/legend dimension within a panel**. New in v3. Three
  extractors independently had a condition variable with nowhere to go and each
  parked it somewhere different — inside `mark`, inside `x`, or in prose. That is
  precisely the drift the named-slot rule was meant to prevent.
- `n` records observations behind each mark **and** per panel, because for a point
  cloud the per-mark answer is trivially 1 and useless. Where a single
  representative is shown out of many, write it as `1 of 5 (pLDDT-selected)` — the
  bar-hiding-a-distribution case this field exists to catch. `NOT REPORTED` when
  the paper never says.

Worked example: `PLOT | facet: predictor (4) | vary: RMSD to active ref, 0–12 Å (continuous) | series: input condition (4: apo, agonist, partner+agonist, +GTP) | measure: RMSD (Å) | mark: point | n: 1 per mark, NOT REPORTED per panel`

**Form 2 — MATRIX.** Heatmaps and contact maps, where both axes are indices and the
value lives in the cell. New in v3: v2 forced these into PLOT, which put a variable
in the measure slot.

```
MATRIX | rows: <var> (<n>) | cols: <var> (<n>) | value: <what the cell encodes> | facet: <var> (<n>)
```

**Form 3 — RENDER.** Structures, with no data axes.

```
RENDER | facet: <var> (<n>) | views: <n> (<what the views are>) | overlay: <k or NOT REPORTED> predictions on <n> reference(s) | axis: none
```

`facet` is new in v3. In v2 the `views` slot was carrying two incompatible things:
genuine camera angles of one system, and different local markers across systems.
Markers and systems are facets; camera angles are views. `overlay` takes
`NOT REPORTED` explicitly, because render captions almost never give k and v2 forced
extractors to write unjoinable prose.

Worked example: `RENDER | facet: system (3) × feature (2: ligand pose, ICL3) | views: 1 | overlay: NOT REPORTED predictions on 1 reference | axis: none`

**Form 4 — TREE.** Phylogenies and dendrograms carrying per-leaf data. New in v3;
these fit none of the earlier forms, and calling one `SCHEMATIC | no data` is a
false statement the index would then propagate.

```
TREE | leaves: <n> | annotation: <var> (<n levels>) | layout: <radial|rectangular>
```

**Form 5 — SCHEMATIC.** Workflows, chemical structures, alignment listings, anything
carrying no measured data.

```
SCHEMATIC | <one line on what it depicts> | no data
```

### Splitting a figure into panel-group rows

One row per panel group. The rule, which v2 left to judgement and two extractors
asked for explicitly:

**Split when `mark` or `measure` differs. Do not split when only `facet` differs.**

So four box panels showing four metrics under the same faceting are one row with a
compound measure; a box panel plus a bar panel is two rows. Suffix the shared
`fig_no` with the panel letters, `4A` and `4B-C`. Where a single panel letter
genuinely contains two shapes — common in Nature Extended Data — a letter may appear
in two rows; say so in `panels` rather than distorting the split.

## G. Provenance

| Field | Notes |
|---|---|
| `extracted_on`, `extractor` | Date and which model/session. |
| `schema_version` | `v3.2` for notes written or re-passed after 2026-09-10. Notes reading `v3` or `v3.1` are current on A–E content but predate `input_factor_design`; notes reading `v2` are **partially stale** and must be re-extracted. Absence of `input_factor_design` on a v3/v3.1 note means *not yet backfilled*, never `NOT ADDRESSED`. |
| `confidence` | high / medium / low, with what was hard to read. |
| `unresolved` | Anything the extractor could not determine. Do not silently drop these. |
| `why_it_matters` | **Left empty by the extractor.** This is the user's call. |

---

## Tag vocabulary

Fixed list. Tags are the mechanism for reverse lookup ("which papers did X"), so
they must not drift — a tag invented on the fly is a tag no future query will find.
Adding a tag means editing this file and re-tagging the corpus.

**System:** `gpcr` `kinase` `transporter` `periplasmic-binding` `atpase`
`fold-switching` `general-protein`

`fold-switching` is a system property, not a fold family, and covers metamorphic
proteins. Note that `kinase` means protein kinase; adenylate kinase and other
small-molecule kinases are `general-protein`, or a reverse lookup for kinase
conformational states returns false positives.

**Method:** `cofolding` `msa-subsample` `msa-state-filter` `template-state-bias`
`af-cluster` `latent-steering` `md` `md-emulator` `enhanced-sampling`
`benchmark-only` `experimental`

`latent-steering` is any inference-time intervention on an internal tensor — pair
representation, trunk embedding, distogram head, conditioning embedding. It is not
MSA manipulation, not template bias, not seeds. `md-emulator` is a generative model
trained on MD trajectories, which is neither `md` nor `cofolding`. `experimental`
marks a paper with no structure prediction in it at all, whose section C will be
mostly NOT APPLICABLE by design rather than by sloppiness.

**Protocol:** `no-template-no-msa` `templates-on` `state-annotated-input`

`no-template-no-msa` marks the de-novo input regime, which is what separates an
unbiased benchmark from every biasing paper in the corpus and had no tag in v2.

**State handling:** `single-state` `two-state` `ensemble` `continuum`

May be combined: `ensemble` + `single-state` is the correct pair for a method that
samples widely and collapses onto one basin.

**Metric:** `binary-predicate` `continuous-metric` `rmsd-only` `visual-metric`
`saturating-metric`

`visual-metric` means the state was called by eye from a render, with no
operationalised predicate. It is usually a rigour defect and was inexpressible in v2.

**Rigour:** `oracle-leak` `design-level-oracle` `prospective` `anti-memorization`
`no-anti-memorization` `unpowered` `confidence-as-discriminator` `multi-backbone`
`experimental-validation`

`design-level-oracle` is route 7: the pipeline is clean but the expected answer was
declared before the result was read. Weaker than `oracle-leak`; keep them distinct.
`experimental-validation` marks a computational paper that tested a prediction in the
lab (NMR, cryo-EM, an assay) — rare, and a strong distinguishing feature.

**Control:** `directed-state` `partner-driven` `ligand-driven` `peptide-driven`
`g-protein-mimetic` `nanobody` `apo-sampling` `seed-only` `coinput-confounded`
`factors-crossed`

`factors-crossed` is new in v3.2 and marks a paper that varies **two input factors
independently** — MSA, templates, ligand or partner — so that their interaction is estimable.
It is the positive counterpart to `coinput-confounded` and is expected to be rare: the common
pattern in this literature is to vary one factor and hold the rest, which looks like a control
arm and is not one. Grep this tag to ask whether an interaction has ever been measured.

`coinput-confounded` is new in v3.1 and marks a paper that supplies two or more co-inputs
together in the same arm and never separates them, so no single co-input can be credited with
the effect. It is a rigour marker, not a control handle, but it lives here because it is a
property of how the handle was used.

**Mechanism (new in v3.1):** `conformational-selection` `induced-fit` `pre-coupled`
`order-agnostic`

These mark the route to the ternary complex a paper assumes or supports. `pre-coupled` is for
receptor–G protein complexes that form before agonist. `order-agnostic` is the honest tag for
every co-folding prediction paper: all co-inputs are supplied at once, so the method has no
notion of binding order and cannot adjudicate between the routes. Use `order-agnostic` freely;
use the other three only where the paper presents evidence, not merely a citation to someone
else's model.

**Site:** `orthosteric` `allosteric-site` `cryptic-pocket` `allosteric-failure`

`allosteric-failure` is the *result* that no model or setting ever sampled the
allosteric site. The site tags mark what was studied; this marks what happened.

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

---

## Changelog: v2 → v3

Every change was forced by a defect that **two or more of five parallel extractors
reported independently**, reading five different papers. Single-extractor
observations were held back unless the gap was plainly structural.

1. **`data_shape` slots renamed by role, not screen position** (`vary`/`measure`
   replacing `x`/`y`). A transposed Cleveland dot plot had nowhere legal to put its
   measure. Reported by 1, but it invalidates the join for a whole plot family.
2. **`series:` slot added to PLOT.** Reported by 3. A colour/legend dimension had no
   home, and each extractor parked it somewhere different — inside `mark`, inside
   `x`, or in prose. This is the exact drift the v2 named-slot rule existed to stop.
3. **Continuous axes allowed in `vary`.** Reported by 2. `<var> (<n>)` presupposed a
   categorical axis with a level count; scatters and spectra have neither.
4. **`n` replaces `n_per_cell`, and records per-mark and per-panel.** Reported by 2.
   For a point cloud the per-mark answer is 1 and meaningless. The `1 of 5
   (pLDDT-selected)` form was added because that is the bar-hiding-a-distribution
   case the field exists for and v2 could only express it as unjoinable prose.
5. **MATRIX form added.** A heatmap forced into PLOT puts a variable in the measure
   slot.
6. **TREE form added.** Annotated phylogenies fit nothing; `SCHEMATIC | no data` was
   a false statement about a figure carrying real per-leaf data.
7. **RENDER gained `facet`, and `overlay` takes NOT REPORTED.** Reported by 1 in
   detail. The `views` slot was conflating camera angles with per-system markers.
8. **Panel-splitting rule made deterministic:** split on `mark` or `measure`, not on
   `facet`. Reported by 2 as under-specified. A letter may now appear in two rows.
9. **`metric_saturation` is numeric only; axis truncation belongs to `hides`.**
   Reported by 3, all of whom recorded the same axis break twice with no rule for
   which was canonical.
10. **`oracle_leakage` route 7 added — design-level oracle use.** Reported by 2. A
    paper can feed the model nothing leaky and still declare the expected state
    before reading the result. Also clarified that tuning a sweep *range* on the
    evaluation set is leakage even when no per-target value is chosen.
11. **`structural_priors_used` added.** Reported by 1, sharply. A wet-lab paper
    designing a peptide from a solved complex has used a structural prior and
    committed no sin; v2 forced that into `oracle_leakage` or nowhere.
12. **`controls_run` added.** An extractor smuggled a twelve-row control table into
    `stated_limits` because it had no home, and called it the most reusable content
    in the note.
13. **`comparable_to_ours` removed from extraction.** An extractor correctly refused
    it: nobody who cannot see our numbers can fill it.
14. **`si_in_scope` added.** Two papers keep their real numbers in SI absent from the
    PDF, which silently empties `metrics_reported` and makes the paper look
    unquantified.
15. **`states_generated` and `state_metric` may be dual.** Both were forcing a single
    value where the honest answer was two, and in both cases the discarded half was
    the interesting one.
16. **Fourteen tags added:** `latent-steering`, `md-emulator`, `experimental`,
    `visual-metric`, `design-level-oracle`, `experimental-validation`,
    `no-template-no-msa`, `templates-on`, `state-annotated-input`, `fold-switching`,
    `allosteric-failure`, `g-protein-mimetic`, `periplasmic-binding`, `atpase`.
    Every one was requested by an extractor who correctly declined to invent it.
17. **`kinase` scoped to protein kinases**, after an extractor flagged that tagging
    adenylate kinase would false-positive every kinase-conformation query.


---

## Changelog: v3 → v3.1

Two fields and five tags, added 2026-09-09. Unlike the v2 → v3 revision, this one was **not**
forced by extractor failure — it was forced by a pattern that only became visible once the
corpus was complete and could be read down by column.

1. **`coinput_composition` added.** Reading `directional_control` down all 78 notes shows *that*
   a paper has a handle but not *what else was supplied at the same time*. Three of the strongest
   partner-driven GPCR papers turn out to bundle agonist and transducer into one condition
   (`ye2026multistatebias`, `zhang2026generalization`) or to omit a decoy arm entirely
   (`chiesa2025templatebias`), and in each case the omission had to be rediscovered by reading
   the methods rather than by querying the index. That is exactly the failure the schema exists
   to prevent.

2. **`binding_order` added.** GPCR activation admits at least two routes to the ternary complex,
   and the corpus contains evidence for both: conformational selection at the ligand level with
   induced fit at the transducer level (`paajanen2026activation`), and a pre-coupled
   receptor–G protein complex that precedes agonist (`georgiou2025heterogeneity`). Nothing in
   the schema recorded which route a paper assumed, and for prediction papers the answer is
   structural rather than incidental: co-folding supplies everything at once and therefore
   cannot speak to order at all.

3. **Five tags added:** `coinput-confounded`, and the mechanism set
   `conformational-selection` / `induced-fit` / `pre-coupled` / `order-agnostic`.

**Population status, stated honestly.** The two new fields are **not yet populated across the
corpus**. `coinput_composition` applies to the 21 prediction papers that supply a co-input;
`binding_order` applies to all 78 but will be `NOT ADDRESSED` or `order-agnostic` for most.
Until that pass is run, a reverse lookup on either field is incomplete and must not be used to
support a "no paper does X" claim.

## Changelog: v3.1 → v3.2

1. **`input_factor_design` added.** The corpus was asked a question it should have been able to
   answer by grep — *has anyone supplied a ligand co-input to an AF3-lineage model while also
   subsampling the MSA, and measured receptor state?* — and answering it took a mechanical sweep
   of sixty notes plus an external search, because the two halves live in different fields
   (`msa_handling`, `coinput_composition`) and neither records whether the factors were varied
   **together, independently, or not at all**. A paper can look rich on co-inputs and still hold
   every one of them fixed.

   The answer that sweep produced is the field's justification. `jung2026boltzperturb` runs
   Boltz-2 with a ligand present in every arm and degrades the MSA in two baseline arms (masking
   at rate 0.1 → SR_O 10.53%; depth reduced to 4,086 rows → SR_O 12.28%, both below vanilla,
   p.7, p.15). That reads as a settled negative until you notice the ligand is never removed:
   **MSA x ligand is HELD, not CROSSED**, so the interaction was never estimated, and the
   masking rate is far below the 40% `kalakoti2026afsample3` finds optimal for AF3. A field that
   recorded the crossing would have made that visible in one line.

2. **Tag `factors-crossed` added**, for the rare paper that varies two input factors
   independently. **It fires on exactly one paper in 81**: `mitjavila2026afsample2t`, which crosses
   masking level (0/10/20/30%) with partner presence, balanced at 250 models per cell (p.8). `coinput-confounded` already marks the opposite case at the co-input level;
   this marks the positive case across factor types, and is the tag to grep when asking whether
   an interaction has ever been measured.

**Backfill status as of 2026-09-10: populated on 11 of 81 notes** — `cheng2026af3cluster`, `chiesa2025templatebias`, `heo2022multistate`, `jung2026boltzperturb`, `lazou2026cryptic`, `mitjavila2026afsample2t`, `vo2026fiducials`, `xing2025purified`, `ye2026multistatebias`, `yu2026domainmotion`, `zhang2026generalization`. Do not treat its absence on the other 70 as
`NOT ADDRESSED`. The cheapest useful backfill is the 21 prediction papers that supply a
co-input, since those are the only ones where a crossing is possible at all; the rest can be
filled opportunistically as notes are next touched. Until then, any query about factor
interactions must be answered by reading `msa_handling` and `coinput_composition` together,
not by grepping this field and finding it empty.

**What the first nine backfills already show.** Two papers bracket the same open question from
opposite sides and neither closes it: `jung2026boltzperturb` varies the MSA with the ligand present
in every arm, and `lazou2026cryptic` varies the ligand with the MSA explicitly held constant
("the same MSAs can be used to predict different conformations depending on the presence of a
ligand", p6). `ye2026multistatebias` and `xing2025purified` both run the two legs but in *different
models*, so neither crosses them either. `heo2022multistate` is confounded by construction — its
method is state-annotated templates **plus** total MSA deletion applied together. That pattern was
invisible before this field existed and is the clearest evidence that it earns its place.
