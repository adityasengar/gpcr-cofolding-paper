# FIGURE_PROVENANCE.md — Block A panels

One entry per panel: the source file it reads, the exact filter applied, the n
after filtering, and the claim it supports. Written by the figures session;
regenerate any panel with `python3 figures/block_a/panels/<script>.py`.

Everything here traces to a file in `data/block_a/`. Nothing is invented, and
where the shipped claim sheet and the shipped data disagree, **the panel draws
the data and says so on the panel**.

---

## The exclusion filters, once

The five `excl_*` flags are five independent sets with different scopes, and
`excl_any` — their union — fires on **5,093 of 9,490 rows (53.7%)**. It is the
wrong filter for almost every panel here. The filters actually used:

| name in `badata.py` | rule | rows kept |
|---|---|---|
| `core` | `not (E1 or E2)` | 9,461 of 9,490 (99.7%) |
| `core_class_a` | `core` and Class A | 7,966 |
| `core_npxxy_refs` | `core` and not `excl_E3_npxxy` | for NPxxY denominators/predictors only |
| `core_tilt_refs` | `core` and not `excl_E3_tilt` | for tilt denominators/predictors only |
| `confidence_population` | Class A rows carrying `rmsd_to_active_ref` | 6,395 (32 receptors) |

E3 is applied **only** where a reference value is a denominator or a regression
predictor — the amplitude fits and the fraction metric — and then always
through the per-axis flags, never the `excl_E3` union. It is irrelevant to raw
distributions, predicate firing rates and confidence correlations.

`fraction_of_way_to_active` appears in **no figure**. It is a Table T2 quantity
by hard rule. The one place it is named is S1b, whose subject is the filters
rather than the value, and the panel says so.

---

## BA-1 — the instrument and its calibration

### BA-1a `out/ba1a_instrument_schematic.png`
- **source** `data/block_a/11_structures/instrument_schematic/{3SN6,2RH1}.cif`
- **filter** none — reference structures, not predictions. `selected_from = 1`:
  the pair is fixed by `11_structures/SELECTION.md`, not chosen from candidates.
- **n** 2 structures.
- **superposition** receptor Cα TM1–TM7 only: 3SN6 chain R resi 30–342 against
  2RH1 chain A resi 29–342, excluding T4 lysozyme (resi 1002+ **on both**, not
  only on 2RH1), the Gs heterotrimer and Nb35, per `ALIGNMENT.md`.
  This needed a new `--align-ref-on` flag on `render_struct.py`: the two files
  name the receptor differently (chain R vs chain A) and one selection string
  for both objects would have aligned on whatever it happened to match.
- **camera** derived from the geometry, not chosen by eye: membrane normal
  vertical (first principal axis of the receptor Cα cloud, intracellular side
  up), the active-minus-inactive displacement of the 6×37 Cα in the image plane.
  The 18 numbers are in `scenes/ba1a_instrument_schematic.pml`.
- **anchors drawn** L75 (2×46) and L275 (6×37) Cα; Y219 (5.58) and Y326 (7.53)
  OH. Verified by reproducing 2RH1's shipped `d_tilt_ref` = 11.9283 Å and
  `d_npxxy_oh_ref` = 11.4727 Å **exactly** from the CIF.
  `instrument_schematic/ALIGNMENT.md` names L124 and F282 for the tilt anchors;
  those give 9.03 Å on 2RH1 and are not the anchors the scorer used.
- **measured here** 3SN6 tilt 18.400 Å / NPxxY-OH 4.282 Å; 2RH1 tilt 11.928 Å /
  NPxxY-OH 11.473 Å. Both predicate axes therefore fire on 3SN6 and on neither
  for 2RH1.
- **caption must state** 3SN6 is **not** the ADRB2 panel active reference —
  4LDE is — so no panel-derived number is annotated on this render.
- **supports** the predicate definition; the quantitative panel beside it is
  BA-1b. It must never appear without BA-1b.

### BA-1b/c/d `out/ba1_reference_landscape.{pdf,png}` — `ba1_reference_landscape.py`
- **source** `02_references/reference_predicates.csv`, `reference_metadata.csv`,
  `reference_separation.csv`
- **filter** none. These are reference structures; `excl_*` are row-level flags
  on predictions and do not apply.
- **n** 168 references (98 on the 48-receptor panel, 70 off-panel).
  - **b** 70 have both axes measurable and are in the scatter; **98 have no
    NPxxY-OH value at all** and are drawn as a rug with their own n rather than
    dropped. Filled marker = panel PDB, open = off-panel.
  - **b** 9 references deviate from their own deposited label. All five
    `deviation_class` levels are drawn with their own shape:
    `unclassified` 5, `curation_error` 1, `expected_biology` 1,
    `measurement_artifact` 1, `curation_error_or_expected_biology` 1.
    Restricted to panel PDBs there are 7 deviations, 3 of them unclassified.
    Every deviation is labelled with its receptor, including the 5 on the rug.
  - **c** reference gap per receptor: tilt n=48, SD 2.074 Å; NPxxY-OH n=28,
    SD 5.222 Å.
  - **d** predicate call over all 168: expected_pass 88, expected_fail 62,
    missing_axis 9, active_fails_predicate 5, inactive_passes_predicate 4.
- **supports** that the predicate behaves on structures of known state, and
  that the tilt axis has a fifth of the NPxxY axis's dynamic range — which is
  what BA-4c returns to.

---

## BA-2 — the main effect `out/ba2_arm_shift.{pdf,png}` — `ba2_arm_shift.py`

- **source** `01_rows/block_a_rows.csv`, `03_aggregates/{headline_by_backbone,
  receptor_summary,cell_summary}.csv`
- **filter (a, b, c)** `core` — E1+E2 only. **n = 9,461 of 9,490 rows.**
  E3 is not applied: no reference value is a denominator or a predictor
  anywhere in this figure. E4/E5 are not applied; S1 shows what they do.
- **n per cell, panel a** apo/cognate: Boltz 1,195/1,170 · Chai 1,199/1,175 ·
  OF3 1,199/1,174 · Protenix 1,199/1,150.
- **panel b** 47 paired receptors per backbone. Receptors moving the *wrong*
  way: Boltz 2, Chai 5, OF3 4, Protenix 0.
- **panel c CIs are the `*_cluster_ci_*` columns.** The claim sheet's SC-1
  table quotes the **receptor** intervals under a "95% CI (cluster-boot)"
  heading (DISCREPANCY_REPORT D5). Values drawn:
  Boltz 5.036 [3.528, 5.545] · Chai 1.047 [0.358, 3.763] ·
  OF3 4.814 [3.951, 5.215] · Protenix 5.307 [4.633, 5.743].
  Effective n = **47** receptors, not the 48 that `n_receptors_tilt` records.
- **filter (d)** Class A cells only, **n = 320 of 380 cells**, using
  `both_fire_rate`, which is the (NPxxY and tilt) rate and equals the
  class-aware `active` predicate exactly on Class A and not on Class B/F.
  The open diamonds are the pooled row-level rate, which is what
  `headline_by_backbone.csv` reports; it differs from the per-cell median
  substantially (e.g. OF3 apo: pooled 0.099, per-cell median 0.020).
- **supports** SC-1: the cognate arm moves TM6 outward on all four backbones,
  Chai softly (C-4).

---

## BA-3 — the PIF connector `out/ba3_connector.{pdf,png}` — `ba3_connector.py`

- **source** `05_connector/{connector_predictions,connector_summary,
  connector_references}.csv`
- **filter** none applicable. This is the T2 scale-up: a balanced stratified
  sample, **n = 512 rows**, 16 strata of 32 (backbone × arm × predicate call).
  It is not the 9,490-row corpus, so the `excl_*` flags do not apply.
- **a (the lead panel)** row-level agreement per backbone against a fixed
  denominator of 64. Pooled: **204/256 (79.7%)** predicate-active below the
  reference-inactive median and **205/256 (80.1%)** predicate-inactive above
  the reference-active median. Both reproduce exactly.
- **b** ECDF of the connector distance by predicate call, n=256 each, with the
  reference medians (active 10.48 Å, inactive 11.99 Å, aggregates over 77
  Class A reference CIFs) drawn as lines. The per-reference distances are not
  in the archive, so no reference distribution is drawn. Log x, because the
  upper tail reaches 43.8 Å; **the axis is not truncated**.
- **c** pooled and per-backbone delta with cluster CIs. Pooled −0.560 Å,
  **[−1.196, +0.026] — includes zero**, as does every per-backbone interval.
  Zero is drawn; the reference Δ (−1.51 Å) is drawn as a second reference.
- **no magnitude ratio is plotted.** The claim sheet's "0.37, CI [0.04, 0.77]"
  reads as a signed effect and is not one: the ratio is computed from the
  absolute value of the delta, so its interval cannot cross zero by
  construction (DISCREPANCY_REPORT D2).
- **supports** SC-3's state-reached half, at agreement strength, not at
  signed-magnitude strength.

---

## BA-4 — amplitude `out/ba4_amplitude.{pdf,png}` — `ba4_amplitude.py`

- **source** `04_amplitude/{amplitude_points,amplitude_fits,
  attenuation_sensitivity}.csv`
- **filter** inclusion set **`class_a_only`** throughout: Class A (E4) with the
  per-axis E3 already applied upstream, because here the reference gap IS the
  regression predictor. **n = 28 receptors on NPxxY, 32 on tilt.** All three
  shipped sets are in S5.
- **a** four small multiples on NPxxY with the fit, its slope-CI fan, and
  **the unity line on every panel**.
- **b** slopes as a forest, **both axes**, with **zero and unity both marked**.
  NPxxY: Boltz +0.042 [−0.327, +0.561] · Chai +0.366 [−0.001, +0.901] ·
  OF3 +0.176 [−0.036, +0.410] · **Protenix +0.257 [+0.074, +0.552], which
  excludes zero** — and excludes it in all three inclusion sets (S5).
  Tilt: Boltz **−0.298** · Chai **−0.659** · OF3 +0.233 · Protenix +0.082;
  all four intervals include zero.
- **c** SD of the predictor: tilt **1.171 Å** (n=32) beside NPxxY **5.222 Å**
  (n=28). The tilt axis is presented as uninformative for amplitude — an
  instrument property (C-10), not a result about the models.
- **d** attenuation sweep, σ 0–2 Å. NPxxY: 0 of 84 swept points unstable and
  the correction moves nothing. Tilt: **44 of 84 unstable**, the region shaded
  rather than trimmed, and the curves drawn to their full extent.
- **supports** SC-3's amplitude half, reworded: three of four backbones show no
  evidence of amplitude reproduction; one (Protenix) shows a weak signed
  positive slope of 0.26, roughly a quarter of the expected scaling and far
  below unity. **Not** "all CIs cross zero".

---

## BA-5 — confidence `out/ba5_confidence.{pdf,png}` — `ba5_confidence.py`

- **source** `06_confidence/{plddt_correlations,plddt_per_receptor}.csv` and
  `01_rows/block_a_rows.csv`
- **filter (a, b, d)** the population behind `plddt_correlations.csv`: Class A
  rows carrying an RMSD to an active reference. **n = 1,595–1,600 per backbone,
  6,395 rows, 32 distinct receptors.** Verified by reproducing all twelve
  Pearson r values to 1e-4. Note the shipped correlations do **not** apply
  E1/E2; panel c does, which removes 4 further rows and moves r by ≤ 0.0001.
- **`plddt_correlations.csv` records `n_receptors = 40` on every row.** The
  population has 32, and `plddt_per_receptor.csv` itself carries 32 per
  (backbone, aggregation). The panels quote 32.
- **a** all three aggregations × four backbones, cluster CIs, zero drawn, the
  primary aggregation banded. **`plddt_at_anchors` was designated primary POST
  HOC**, after all three had been computed (W-2); the panel and the caption
  must say so. Signed at cluster bootstrap on the primary aggregation for
  **2 of 4** backbones: Boltz −0.221, OF3 −0.626; Chai and Protenix null.
- **b** OF3 strengthens from −0.258 (global mean) to −0.626 (anchor mean);
  Protenix collapses from +0.327 to +0.068.
- **c** the scatter, E1+E2 applied, n = 1,595/1,599/1,598/1,599.
- **d** per-receptor sign census out of 32: OF3 anchor mean 31/32 negative;
  Protenix global mean **0/32** negative despite a pooled r of +0.327.
- **supports** SC-11 as restated by W-2.

### BA-5e `out/ba5e_most_confident_apo.png`
- **source** `11_structures/confidently_wrong/{AA2AR__apo__boltz__seed748489558__row567.cif, 5G53.cif}`
- **selected from** the AA2AR × Boltz-2 × apo cell, **n = 25 rows**.
- **selection rule** the row with the **highest `plddt_mean` in the cell**
  (73.93; cell median 72.04) — 100th percentile on confidence.
  `11_structures/SELECTION.md` states the rule as "top-quintile RMSD-to-active,
  highest pLDDT within", which selects **row_id 552**, not 567. The shipped CIF
  is 567, and what 567 satisfies is highest-pLDDT-in-cell.
- **the directory name is wrong and the caption must not repeat it.** Row 567
  is `rmsd_to_active_ref` = 3.102 Å but `rmsd_to_inactive_ref` = **0.948 Å**:
  it is a confident **apo** prediction sitting on the **inactive** reference,
  which is where an apo prediction belongs. It is far from active by
  construction, not confidently wrong.
- **superposition** receptor Cα resi 6–312, chain A on both sides; 5G53's
  mini-Gs chains excluded. Camera derived as for BA-1a.
- **anchors drawn** L48 (2×46) / L235 (6×37) Cα and Y197 (5.58) / Y288 (7.53)
  OH — verified by reproducing row 567's stored
  `d_gpcrdb_tm6_tilt_246_637_ca` = 11.7347 Å and `d_npxxy_oh` = 9.6079 Å
  exactly from the CIF. `confidently_wrong/ALIGNMENT.md` names L88 for 2×46
  (should be L48) and Y213 for 5.58 (should be Y197).
- **quantitative panel beside it** S8b, which marks this exact row. The render
  must never appear without it.

---

## Supplementary

### S1 `out/s1_exclusions.{pdf,png}` — `s1_exclusions.py`
- **source** `01_rows/block_a_rows.csv`, `08_exclusions/*`
- **filter** none — the panel is *about* the filters.
- **n** 9,490 rows; sweep 160 rows (5 metrics × 4 backbones × 8 combinations).
- **a** E1 25 · E2 4 · **E1∪E2 29 (0.3%)** · E3 union 4,890 · E3-NPxxY 4,690 ·
  E3-tilt 2,000 · E4 1,495 · E5 500 · **`excl_any` 5,093 (53.7%)**.
- **b** every combination × every metric, as % shift from baseline.
  **No sign flip anywhere: 0 of 160 cells.** Largest: Chai median tilt shift
  +222.0% under `all_E1-E5` and +95.3% under E4; Protenix apo rate −92.5%.
- **supports** claim-sheet statement B, and it is the panel that stops anyone
  filtering on `excl_any`.

### S2 `out/s2_reference_audit.{pdf,png}` — `s2_reference_audit.py`
- **source** `02_references/{reference_metadata,reference_predicates}.csv`
- **filter** none. **n = 168** references (98 panel / 70 off-panel).
- **a** fusion partner 52/168 (51 on panel) · fusion inside the tilt window
  16/168 · inside the NPxxY window 11/168 · transducer bound 30/168 ·
  a predicate window hit 18/168 · RCSB entry cached 163/168 ·
  deviates from its label 9/168 · construct annotated non-wt 1/168.
- **empty columns, stated on the panel**: `engineered_mutation_count`,
  `engineered_mutation_positions` and `construct_contradicted_by_rcsb` are
  **0 of 168 non-null** in this drop, so no engineered-mutation count can be
  shown at all. The construct annotation is untrusted corpus-wide (C-11).
- **b** resolution by state, n=163 with a value (5 have none);
  median 2.84 Å active / 2.71 Å inactive. Methods: EM 98, X-ray 65, 5 unknown.

### S3 `out/s3_bootstrap_comparison.{pdf,png}` — `s3_bootstrap_comparison.py`
- **source** `03_aggregates/{headline_by_backbone,receptor_summary}.csv`
- **filter** none beyond what is in the shipped aggregate.
- **the only panel in the set that draws receptor-bootstrap intervals**, per
  Methods 8.4.
- **cluster / receptor width ratio, all 8 rows**: tilt 1.84 / 1.11 / 1.91 /
  1.43; delta-to-active 1.00 / 1.00 / 1.07 / 2.20. The claim sheet and the drop
  README both describe the receptor bootstrap as "~1.10× tighter"; that holds
  on 2 of these 8 rows.
- also records that `n_receptors_tilt` = 48 against 47 non-null per-receptor
  values, and `n_receptors_delta` = 48 against 39.

### S4 `out/s4_per_receptor.{pdf,png}` — `s4_per_receptor.py`
- **source** `03_aggregates/receptor_summary.csv`
- **filter** as shipped (E1/E2 upstream). No E3/E4/E5 — every receptor is
  drawn, with its GPCR class on the axis.
- **n** 48 receptors × 4 backbones = 192 cells, **4 absent** (FZD4 on every
  backbone), drawn white rather than zero.
- **11 of 188 non-null cells are negative.** Most negative: SMO/OF3 −2.14 (F),
  LT4R1/Chai −0.63, CCR5/OF3 −0.40, FZD6/Boltz −0.38, AGTR1/Chai −0.30.
- **supports** BA-2c by showing that the median is not hiding a bimodal panel.

### S5 `out/s5_inclusion_sets.{pdf,png}` — `s5_inclusion_sets.py`
- **source** `04_amplitude/amplitude_fits.csv`, all 24 rows.
- **n by (axis, set)**: NPxxY 28 / 28 / 23; tilt 39 / 32 / 27.
- **SD(predictor) by (axis, set)**: NPxxY 5.222 / 5.222 / 4.486;
  tilt 2.169 / 1.171 / 1.195.
- **NPxxY `baseline` and `class_a_only` are byte-identical** — verified in the
  script. No shipped inclusion set produces the claim sheet's n=34 / SD=4.71.
- Protenix on NPxxY excludes zero in **all three** sets; nothing else does,
  on either axis.
- Both panels share one x scale.

### S6 `out/s6_predicate_calibration.{pdf,png}` — `s6_predicate_calibration.py`
- **source** `01_rows/block_a_rows.csv`
- **filter** `core` — E1+E2. **n = 9,461.**
- **predicate-active**: 4,863 rows; **4,253 carry an active reference and are
  testable; 610 cannot be tested at all**; 2 exceed 3 Å.
  **Testable rate 0.047%** (2/4,253). The rate against all predicate-active
  rows, which is what SC-6 and DISCREPANCY_REPORT D7 both use, is 0.041%
  (2/4,866 on the unfiltered corpus).
  Per backbone: Boltz 1/1,022 · Chai 0/1,056 · OF3 1/1,103 · Protenix 0/1,072.
- **predicate-inactive** (the comparison a one-sided FP rate leaves out):
  4,598 rows, 3,633 testable, 965 untestable, **224 exceed 3 Å = 6.17%**.
- Both panels share one x scale; neither axis is truncated.

### S7 `out/s7_clusters_holdout.{pdf,png}` — `s7_clusters_holdout.py`
- **source** `07_clusters_and_holdout/{cluster_map,holdout_counts}.csv`
- **n** 48 receptors in **29 clusters, 16 of them singletons (55%)**. The
  manuscript quotes 26 clusters with 42% singletons; the drop README says the
  panel-slug-to-family map was reconstructed heuristically. Sizes: 16×1, 9×2,
  2×3, 2×4.
- **holdout**: Boltz (cutoff 2021-09-30) 9 receptors / 2 clusters; Chai, OF3
  and Protenix (cutoff 2023-01-13) 4 receptors / 0 clusters each.
  **`powered` is False on all four rows.**
- **supports** C-8, and it is the panel that shows what the cluster bootstrap
  has to work with.

### S8 `out/s8_aa2ar_case.{pdf,png}` — `s8_aa2ar_case.py`
- **source** `06_confidence/aa2ar_case.csv`, all **200 rows** (4 backbones × 2
  arms × 25 seeds). One AA2AR row in the corpus carries E2 (row 7440); it is
  not in this file's arm/seed slice and nothing is dropped.
- **a** 195 of 200 rows sit nearer their own arm's reference. Apo: 1.36–3.29 Å
  from active, 0.33–2.21 Å from inactive. Cognate: 0.49–2.27 Å from active,
  0.99–2.98 Å from inactive.
- **b** marks row 567, the BA-5e render: pLDDT-at-anchors 84.65,
  `plddt_mean` 73.93, 3.10 Å from active, **0.95 Å from inactive**.
- **supports** SC-5, and it is the required quantitative panel for BA-5e.

### S9 `out/s9_fold_integrity.{pdf,png}` — `s9_fold_integrity.py`
- **source** `01_rows/block_a_rows.csv`
- **filter** `core` — E1+E2, **n = 9,461**. Deliberately **not**
  Class-A-restricted: the point of the panel is where the failures are.
- **overall pass 96.32%** (SC-8 claims 96.3%): Boltz 95.64 · Chai 95.07 ·
  OF3 97.72 · Protenix 96.85.
- **by class: A 99.05%, B 65.79%, F 100%.** Failures per backbone are
  Class B 71/76/51/74 out of 200; Class A 32/41/3/0 out of ~1,999; Class F 0.
  Each class has its own axis, because their cell sizes differ (≈1,999 / 200 /
  175) and one shared denominator would have misstated every Class B and
  Class F row.
- **supports** SC-8 with its scope caveat (C-2).

---

## Toolkit changes made for these panels

All in `figures/`, all with a docstring naming the defect they prevent.

| where | what | why |
|---|---|---|
| `figpanels.forest` | point + interval with the **null drawn**, optional second reference (unity), hollow marker when the interval includes the null, optional banded rows | "no dispersion/CI/test" is 131 of 1,226 corpus rows; the subtler failure is an interval drawn without the value it must exclude |
| `figpanels.regression_with_unity` | scatter + fit + slope-CI fan + **unity line that cannot be forgotten** | an amplitude slope judged against zero is judged against the wrong null |
| `figpanels.predicate_plane` | two axes + thresholds + **rug for items only one axis can measure**, every categorical level drawn or an exception | 98 of 168 references have no NPxxY value; a plain scatter drops them silently |
| `figpanels.curve_family` | swept-parameter curves with the **unstable region shaded, not trimmed** | trimming a divergent sweep is a truncated axis dressed as tidiness |
| `figpanels.grouped_strip` | `strip_violin` for two crossed factors, with staggered n labels | collapsing two factors onto one axis invites comparing across the wrong one; collided n labels are the same defect as missing ones |
| `figpanels.matrix` | annotation contrast now from the **colormap's own luminance** | the value-position rule painted every above-midpoint cell white on a diverging map, including the pale ones |
| `figpanels.count_dots` | `label_gap` | the count label sat on top of its own dot |
| `figstyle` | `BACKBONE_*`, `ARM_*`, `DEVIATION_*` fixed encodings | a colour must mean the same thing in every panel of the paper |
| `render_struct.py` | `--align-ref-on` | 3SN6 calls the receptor chain R and 2RH1 calls it chain A; one selection string for both objects silently aligns on whatever it matches |
