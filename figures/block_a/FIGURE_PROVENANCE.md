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

### BA-1a `out/ba1a_instrument_schematic.png` — **SUPERSEDED 2026-09-09**
> Replaced by `ba1a_instrument_{side,cyto}.png` (4LDE over 2RH1, two views,
> all four values drawn). See the entry at the end of this file. The record
> below is kept because the superposition and anchor notes still hold.
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

---

# Added 2026-09-09 — the workflow figure, the graphical abstract, and the
# renders rebuilt on the subject/context convention

## The render conventions used from here on

Taken from what the corpus does when its panels are viewed rather than from
what its captions say. Every render below obeys all six.

1. **Grey is "not the subject", not "reference".** The invariant bundle is grey
   and thin; the element carrying the claim is opaque, thick and coloured.
   Colouring by which file a thing came from — grey reference, coloured
   prediction — is not a convention this field has, and it encodes provenance
   where the reader needs mechanism.
2. **Colour by predicate call.** TM6 is vermillion where the predicate fires
   and blue where it does not, on predictions and on references alike, and the
   reference marks in BA-6, GA-1 and F1b use the same two colours. The ARM
   (grey apo / green cognate) is a different variable and keeps its own pair.
3. **Transparency de-emphasises and is never applied to the subject.**
4. **Representation carries emphasis too**: TM6 is a thick tube against thin
   cartoon.
5. **The partner is the contacting fragment only.** The α5 C-terminal 21
   residues (Gα 334–354; ACM1 339–359) are drawn and the rest of the supplied
   Gα is not. Block A's cognate arm supplies the FULL cognate Gα subunit — 354
   residues, chain B — and every caption says so. Drawing the whole subunit
   would put the reader's attention on an object the figure is not about;
   silently drawing 21 residues without saying what was supplied would be
   worse.
6. **No residue labels on the render.** Per-residue detail goes in the strip
   below the panel, where it cannot collide with the cartoon. Only the measured
   distances are annotated, and each carries its value AND its atom pair.

**Every camera is derived, not chosen.** `figures/block_a/camera.py` builds the
18-number PyMOL view from the coordinates: the bundle axis from the first
principal component of the receptor Cα cloud, signed extracellular-up from the
mean of the first ten modelled Cα against the two intracellular tilt anchors,
and the tilt axis placed horizontal. `cytoplasmic_view` is the same derivation
rotated to look up the bundle from inside the cell. Two things were wrong on
the first attempt and are recorded because they are invisible in code and
obvious in the picture: PyMOL's rotation block is **column-major** (row-major
gives a plausible but wrong oblique camera), and the view's distance must be
divided by tan(fov/2) or the molecule is cropped to a few helices.

**Every anchor is verified before it is drawn.** `figures/block_a/cifread.py`
`verify_anchor` refuses to return a distance that does not reproduce the value
stored for that row in the tidy data, to a 2e-3 Å tolerance. Nothing below
draws a residue number that has not passed it.

---

## F1 — the workflow `out/f1_workflow.{pdf,png}` — `f1_workflow.py`

- **source** `01_rows/block_a_rows.csv` (all 9,490 rows, unfiltered: the figure
  is about where they go) and `02_references/reference_predicates.csv` (all
  168; 167 carry a tilt value and are drawn).
- **a** the two rules with their atom pairs and thresholds. Worked pairs, each
  verified from coordinates: ADRB2 L75/L275 + Y219/Y326 · AA2AR L48/L235 +
  Y197/Y288 · DRD2 L76/L375 + Y209/Y426 · ACM1 L67/L367 + Y208/Y418.
- **b** 167 references, **69 with both axes** (30 active, 39 inactive) and
  **98 with no NPxxY-OH value**, drawn as a rug rather than dropped.
- **c** 48 receptors (40 A / 4 B / 4 F) × 2 arms × 4 backbones × 25 seeds =
  **384 nominal cells, 380 run**; the 4 absent are FZD4 cognate on all four
  backbones. **9,490 rows of a nominal 9,600**; 378 cells carry 25 seeds and
  2 carry 20.
- **c states what is NOT recorded.** Templates-off is SC-9's claim from
  launcher static analysis, source defaults and a 5/5 propagation test, with
  **no row-level echo** — evidence class b+c+d, not a — and **no MSA setting
  appears anywhere in the drop**. The panel says both. No reference structure
  is supplied to any prediction; references enter only at scoring.
- **d** 9,490 → E1 25 · E2 4 → 9,461 scored → Class A 7,966 / B 795 / F 700 →
  predicate active 4,863 / inactive 4,598. Class A firing rate: apo 14.5%,
  cognate 79.6%.
- **carries no magnitude claim and no labelled arrow**, by construction.

## GA-1 — the graphical abstract `out/ga1_hero.{pdf,png}` — `ga1_hero.py`

Three renders over two data panels. Renders built first by `hero_renders.py`.

- **a `out/hero_a_apo_alone.png`** — AA2AR × Boltz-2 × apo, **n = 25 in cell**,
  the **highest-`plddt_mean` row (73.93; cell median 72.04), 100th percentile**.
  This is row 567 out of `11_structures/confidently_wrong/`, and **the
  directory name is not repeated anywhere**: 567 is 0.948 Å from AA2AR's
  INACTIVE reference and the predicate calls it inactive, which is correct for
  an apo prediction (D12). `SELECTION.md`'s stated rule selects row 552, not
  567. Drawn: tilt **11.7347 Å** (L48 2×46 Cα – L235 6×37 Cα) and NPxxY-OH
  **9.6079 Å** (Y197 5.58 OH – Y288 7.53 OH), both verified from the CIF;
  `confidently_wrong/ALIGNMENT.md` names L88 and Y213 and is wrong (D13).
- **b `out/hero_b_cognate.png`** — DRD2 × OpenFold-3 × cognate, **n = 25**, the
  **median `rmsd_to_active_ref` row (1.218 Å; rank 13 of 25, 50th
  percentile)**; cell range 1.020–1.507 Å and all 25 rows are called active.
  Drawn: tilt **17.2766 Å** (L76 – L375) and NPxxY-OH **3.9883 Å** (Y209 –
  Y426), both verified.
- **c `out/hero_c_over_reference.png`** — the same row 8285 superposed on
  **7JVR**, DRD2's deposited ACTIVE panel reference, on receptor Cα 34–441 only
  (prediction chain A against 7JVR chain R), excluding 7JVR's Gi heterotrimer,
  scFv16 and bromocriptine from the superposition atoms. 7JVR's own axes
  reproduce exactly at the same pairs: **17.5860 Å** and **4.2522 Å**.
  Cytoplasmic view — the second of the two canonical GPCR views.
- **d** the population a and b were drawn from: `core` (E1+E2) + Class A,
  **7,966 rows**, of which **7,166 have both axes** (apo 3,592 / cognate
  3,574) and **800 have no NPxxY-OH value and are rugged**. 69 Class A
  references overlaid. **Both rendered rows are ringed on it**, which is what
  stops the render and its supporting number drifting apart.
- **e** per-cell active fraction, apo against cognate, **159 paired Class A
  cells**, 25 seeds each: **120 up, 37 unchanged, 2 down**.
- **the caption must say a and b are DIFFERENT RECEPTORS** — the archive ships
  one prediction per case — and the panel says so itself.
- **what it may not say**: it shows the state that is REACHED. It is not
  evidence of amplitude reproduction (BA-4, negative on 3 of 4 backbones), and
  panel c says so on the panel. There is **no arrow anywhere in the figure**.
- `fraction_of_way_to_active` appears nowhere.

## BA-6 — the predicate plane for the predictions
`out/ba6_state_plane.{pdf,png}` — `ba6_state_plane.py`

- **source** `01_rows/block_a_rows.csv`; `02_references/reference_predicates.csv`
- **filter** `core` (E1+E2) then **Class A**. **n = 7,966**, of which 7,166
  have both axes and 800 are rugged. E3 is NOT applied: the thresholds are
  panel constants, not per-receptor references, so no reference value is a
  denominator or a predictor anywhere in this figure.
- **a** pooled plane. Every observation drawn at α=0.10 plus a contour of its
  own smoothed 2-D density, because a scatter of 7,166 points is a blob and a
  contour alone hides the tails. The two arms are within 0.5% of the same n, so
  the contours are comparable; the generator returns both ns and prints them.
- **b** four backbone facets on **identical limits and one colour rule**. Four
  independent corpus papers draw this exact plot type with per-facet axis
  ranges, and two more clip a 0–100 confidence colour at 50–90; the generator
  takes `xlim`/`ylim` as arguments for that reason.
- **c** quadrant census, both arms, of the 7,166 with both axes:
  apo **2,611 neither / 318 NPxxY-only / 86 tilt-only / 577 both**;
  cognate **157 / 23 / 232 / 3,162**. This is where the two axes are shown to
  move together rather than one carrying the result.
- **the active corner is drawn as a box whose edges ARE the two thresholds**,
  with their values printed. The corpus's best version of this panel draws
  state boxes whose coordinates are never given.

## BA-7 — a switch, not a dial
`out/ba7_switch_not_dial.{pdf,png}` — `ba7_switch_not_dial.py`

- **source** `01_rows/block_a_rows.csv`
- **filter** `core` (E1+E2) then Class A. **319 cells**, 314 at 25 seeds, 4 at
  24, 1 at 20; **159 receptor × backbone pairs with both arms**.
- **a** **111 of 160 apo cells never fire on any seed; 108 of 159 cognate cells
  fire on every seed.** Interior: 39 apo, 24 cognate. Bins are aligned to the
  seed budget so one bar is one achievable count out of 25 and the two end bars
  are exactly "never" and "always"; both arms share one vertical scale.
  Not a bar with an SEM: one corpus paper drew exactly that over per-fragment
  rates whose bimodality was its own stated thesis.
- **b** **120 up, 37 unchanged, 2 down.** The two that go down are named on the
  panel: LPAR1/OF3 0.88 → 0.80 and LT4R1/OF3 0.04 → 0.00. The identity line is
  labelled in words, because 13 corpus papers draw a diagonal and every one of
  them uses it as a state-call boundary.
- **c** the per-cell matrix, both arms, 40 Class A receptors × 4 backbones,
  **one shared colour scale**. The single absent cell (ACM1 × Protenix cognate,
  E1) is grey **and crossed**: on a sequential map zero is nearly white, so
  "white for missing" would make absent and zero identical.
- **supports** C6/C7 at seed grain, and bounds what seed variance can be
  blamed for.

## BA-8 — the α5 in the cavity `out/ba8_alpha5.{pdf,png}` — `ba8_alpha5.py`

- **a** `out/ba8_alpha5_cavity.png`, DRD2 × OpenFold-3 × cognate row 8285, the
  **median-RMSD row of its 25-row cell (50th percentile)**. Receptor drawn as a
  semi-transparent **surface**, not a cartoon, because the subject is a cavity.
  Only Gα 334–354 drawn. One contact is drawn: **R132 (3.50) to the backbone O
  of C351, 3.16 Å, measured on this model** — not taken from a published
  complex, so the 3SN6-vs-6E67 disagreement about which α5 residue contacts
  R3.50 is not inherited.
- **b, c** the same cell on both predicate axes, all 25 seeds, thresholds
  drawn, row 8285 ringed. Tilt median 17.343 Å (range 16.81–17.78); NPxxY-OH
  median 4.161 Å (range 3.83–7.97). All 25 rows are called active.
- the render and its population are in **one figure**, so the render cannot be
  reproduced without them.

## S10 — what E1 removes `out/s10_broken_cell.{pdf,png}` — `s10_broken_cell.py`

- **a** ACM1 × Protenix × cognate row 967 — the **median `plddt_mean` row
  (38.38, rank 13 of 25)** of a cell in which **every one of the 25 rows is
  E1**. Tilt **21.5470 Å**, NPxxY-OH **26.6320 Å**, both verified; the tilt
  axis would have fired on it.
- **b** ACM1 × Chai-1 × cognate row 948 — the **highest-`plddt_mean` row
  (69.23, 100th percentile)** of its cell, the comparator named in
  `broken_cell/ALIGNMENT.md`. Tilt 17.1660 Å, NPxxY-OH 4.0160 Å, same atom
  pairs, same camera rule, same colour rule.
- **c** both cells' pLDDT distributions with the E1 rule drawn (cell MEAN < 50;
  the cell means are 38.66 and 68.83) and both rendered rows ringed.
  **E1 fires on 25 rows corpus-wide and they are this one cell.**
  **`passed` is True on all 25** — verified in the script — because the A1–A6
  gates carry no pLDDT floor (C-12).

## BA-1a — REBUILT `out/ba1a_instrument_{side,cyto}.png`

The earlier version (3SN6 over 2RH1, one view, no numbers drawn) is superseded.

- **why** it drew both predicate axes as dashed lines with **no value on
  either**, which is the field's characteristic failure on precisely this
  claim; and it could not be fixed as it stood, because **3SN6 is not in the
  reference set at all**, so no number drawn on it could be sourced from a tidy
  file.
- **now** **4LDE** (ADRB2's panel ACTIVE reference) over **2RH1** (its
  inactive one), **two views** — a side view and a cytoplasmic view, the
  canonical GPCR pair — with all four values sourced from
  `reference_predicates.csv` and reproduced from the coordinates:
  **4LDE tilt 17.5625 Å / NPxxY-OH 4.8131 Å; 2RH1 11.9283 Å / 11.4727 Å.**
- **superposition** receptor Cα only: 4LDE chain A **1029–1342** against 2RH1
  chain A **29–342**, excluding 2RH1's T4 lysozyme (1002–1161), 4LDE's Nb6B9
  nanobody (chain B) and both ligands. **4LDE carries a +1000 auth-numbering
  offset**, so its L75/L275 and Y219/Y326 are residues 1075/1275 and 1219/1326;
  2RH1's T4L occupies 1002–1161, which overlaps that range numerically, so the
  two selections must be written separately — one string for both objects would
  align the receptor onto the lysozyme.
- **the caption must say which is which**: 4LDE active, TM6 vermillion; 2RH1
  inactive, TM6 blue; both bundles grey.
- **do not quote a Δ of −6.581 Å for this pair.** That value is ADRB2's
  NPxxY separation against the **median** of its three inactive references
  (3NYA, 11.394 Å). The pairwise 4LDE − 2RH1 difference is **−6.660 Å**.

---

## New discrepancies found while building these, not in DISCREPANCY_REPORT.md

The figures session cannot edit `analysis/`, so they are recorded here for the
orchestrator to carry across.

- **`11_structures/agonist_only_vs_ternary/8FZQ.cif` is not δOR–Gi. It is
  CFTR.** Its own `_struct.title` reads *"Dehosphorylated, ATP-bound human
  cystic fibrosis transmembrane conductance regulator (CFTR)"*: one chain,
  1,152 Cα, ATP and Mg bound, no receptor and no G protein. `ALIGNMENT.md`
  describes it as "8FZQ (δOR–Gi complex)" and `SELECTION.md` lists the pair as
  a "canonical agonist-only vs ternary contrast". **The agonist-only vs ternary
  render cannot be built from this directory.** 6PT2 is correct (δ-opioid with
  peptide agonist KGCHM07, BRIL fusion, no transducer) and its shipped
  `d_npxxy_oh_ref` of 16.7487 Å is the E5 rationale, but it has no partner to
  contrast against. Every other CIF in `11_structures/` was checked against its
  own title and is what it claims to be.
- **`broken_cell/ALIGNMENT.md` names the wrong NPxxY anchor for ACM1.** It
  gives Y5.58 ≈ Y213; the pair that reproduces both rows' stored
  `d_npxxy_oh` exactly is **Y208/Y418**. Tilt is **L67/L367**, which the file
  does not name at all. Same failure mode as D13 in two more files.
- **`success_case/ALIGNMENT.md` names the wrong NPxxY anchors for DRD2.** It
  gives Y5.58 ≈ Y208 and Y7.53 ≈ Y399; the pair reproducing row 8285's stored
  3.9883 Å and 7JVR's stored 4.252152 Å is **Y209/Y426**. D13 again.
- **5G53 chain A does not reproduce AA2AR's shipped reference values exactly.**
  L48/L235 measures 18.124 Å against a shipped `d_tilt_ref` of 18.0974, and
  Y197/Y288 measures 3.7158 Å against 3.7052. 5G53 has two copies of the
  receptor (chains A and B); the shipped value is presumably the other copy or
  a mean. No figure annotates a 5G53 number, so nothing depends on it, but a
  future panel that wants one must say which chain.

## Structural renders that CANNOT be built from this drop

Recorded so nobody re-derives the gap.

- **A small multiple of the same view across the four backbones.** It needs
  four prediction CIFs of one receptor × arm. The drop ships **two** that share
  a receptor and an arm (ACM1 cognate, Chai-1 and Protenix) and no others, so
  the grid would be 2 of 4 cells with the other two silently absent — the
  `pandyszekeres2024gproteindb` defect exactly. S10 uses that pair for what it
  can support instead.
- **An apo → cognate contrast on ONE receptor.** The drop ships one apo
  prediction (AA2AR) and one cognate prediction (DRD2, plus the two ACM1
  cognate rows), and no receptor has both. GA-1a and GA-1b are therefore
  different receptors and the figure says so.
- **An inactive-reference overlay for the apo render.** AA2AR's inactive
  references (5MZP, 5NM4) are not in `11_structures/`; only 5G53, its active
  one, is. Row 567's 0.948 Å distance to the inactive reference is therefore
  stated as a number and not drawn.

## Toolkit changes made for these panels

| where | what | why |
|---|---|---|
| `figpanels.density_plane` | every observation at low alpha PLUS a contour of its own smoothed 2-D density; `xlim`/`ylim` are arguments; optional reference anchors and ringed marks | a scatter of 7,166 points is a blob and a contour alone hides the tails; per-facet axis ranges and per-facet colour scales are recorded on this plot type in four independent corpus papers; the ringed marks are what bind a render to its own point |
| `figpanels.bounded_fraction_hist` | count histogram of a k-of-N fraction, bins aligned to the sample budget, both end bins exact, one shared vertical scale | a mean and an SEM over a U-shaped per-cell rate erases the result; arbitrary bins report an end count that is not the count anyone quotes |
| `figpanels._smooth2d` | separable Gaussian blur of a 2-D histogram | scipy is not importable in this environment (`libmkl_core` missing) |
| `block_a/camera.py` | PyMOL view derived from the coordinates: bundle axis, extracellular-up sign, tilt axis horizontal, and a distance that actually frames the molecule | a camera chosen by mouse cannot be checked; two of the corpus's render defects are camera defects in disguise |
| `block_a/cifread.py` | minimal mmCIF reader plus `verify_anchor`, which REFUSES a distance that does not reproduce the tidy value | Biopython rejects the prediction CIFs (no `_atom_site.occupancy`); three shipped ALIGNMENT.md files name residues that do not reproduce, and each corroborates the others |
| `block_a/panels/hero_renders.py` | one driver for every render: verifies, derives the camera, calls `render_struct.py`, carries the selection rule | the rule, the anchors and the camera are then in one auditable place per panel |
