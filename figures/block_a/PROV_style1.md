# PROV_style1.md — GA style 1, the PIPELINE SCHEMATIC candidate

One of four graphical-abstract candidates built in parallel on 2026-09-10. This
file is the whole provenance record for **this candidate only**. It is
deliberately separate from `FIGURE_PROVENANCE.md` and `figures/FIGURES.md`,
which three other sessions were writing to at the same time; if this candidate
is chosen, fold this file into `FIGURE_PROVENANCE.md` then and not before.

| | |
|---|---|
| script | `figures/block_a/panels/ga_style1_pipeline.py` |
| output | `figures/out/ga_style1_pipeline.{pdf,png}` |
| size | 154 × 76 mm landscape; tested legible downsampled to 80 mm |
| data | `data/block_a/01_rows/block_a_rows.csv`, sha256 `28852f6048e9d313…` (12,050,840 B) |
| built | 2026-09-10 |
| modifies | nothing outside this file and the two files above |

`dofrender.py`, `dofscenes.py`, `figstyle.py`, `figpanels.py` and `ga1_hero.py`
are **read and imported, never written**. The two scene functions this
candidate needs (`_prep_active` / `_prep_inactive` / `draw_inset`) live inside
`ga_style1_pipeline.py`.

---

## What the figure asserts, stage by stage

**1 INPUT.** Two chips — receptor sequence alone (apo arm) and receptor
sequence + cognate Gα (cognate arm) — that **converge** into one process lane.

**2 PREDICT.** Four co-folding backbones, one model per seed, 25 seeds per
receptor × backbone × arm, no structural template supplied.

**3 SCORE.** The state predicate: TM6 tilt ≥ 14.932 Å **AND** NPxxY-OH ≤ 9.08 Å.

**4 CALL.** Two outcome boxes — *called ACTIVE* and *called INACTIVE* — each
carrying one small render pinned to that call and the rate at which that call
fires in each arm.

The arms converge before stage 2 and the flow forks only at stage 4. That
ordering is load-bearing: if the apo lane ran along the top of the figure and
the "called ACTIVE" box sat at the top right, a reader would trace a straight
line from apo to active. Arm and call are different axes and are not allowed to
line up.

---

## CAPTION BLOCK — required content, do not drop any line

> **A 21-residue Gα α5 C-terminal co-input drives the predicted receptor into
> the active state.** Every Class A receptor was predicted twice — from
> sequence alone (apo arm) and with the cognate Gα subunit supplied as a
> co-input (cognate arm) — by four co-folding backbones (Boltz-2, Chai-1,
> OpenFold-3, Protenix), 25 seeds per receptor × backbone × arm, with no
> structural template supplied. Each prediction was called *active* only if
> **both** predicate axes fired: TM6 tilt (2×46 Cα – 6×37 Cα) ≥ 14.932 Å and
> NPxxY (Tyr 5.58 OH – Tyr 7.53 OH) ≤ 9.08 Å. Bars are the fraction of rows in
> each arm receiving each call, with numerator and denominator printed.
>
> **Insets.** *Called active*: dopamine D2 (DRD2) predicted by OpenFold-3 with
> the cognate Gα supplied; TM6 open, 2×46 Cα – 6×37 Cα = 17.28 Å (Leu76 Cα /
> Leu375 Cα). *Called inactive*: adenosine A2A (AA2AR) predicted by Boltz-2
> from sequence alone; TM6 closed, the same atom pair = 11.73 Å (Leu48 Cα /
> Leu235 Cα). Grey is the invariant receptor, drawn as a depth-weighted
> heavy-atom density; colour is TM6 and the α5 21-mer only. Soft focus encodes
> depth only and carries no interpretive meaning. Both insets are drawn at one
> scale (10 Å bars).
>
> **THE TWO INSETS ARE DIFFERENT RECEPTORS.** `11_structures/` ships one apo
> prediction and one success-case cognate prediction and no receptor has both
> arms, so the within-condition contrast is the bar pair, not the two renders.
>
> **SELECTION RULES.** *Called-inactive inset*: AA2AR × Boltz-2 × apo cell,
> n = 25 seeds; the row with the highest `plddt_mean` in the cell (73.93; cell
> median 72.04), i.e. the 100th percentile on confidence. It sits 0.95 Å from
> AA2AR's INACTIVE reference and the predicate calls it inactive, which is
> where an apo prediction belongs; the directory name `confidently_wrong` is
> wrong (DISCREPANCY_REPORT **D12**), and this figure does not repeat it.
> *Called-active inset*: DRD2 × OpenFold-3 × cognate cell, n = 25 seeds; the
> row with the **median** `rmsd_to_active_ref` in the cell (1.218 Å shipped;
> rank 13 of 25, cell range 1.020–1.507 Å) — a typical row of its cell, not a
> best case. All 25 seeds of that cell are called active.
>
> **BOTH ANCHOR PAIRS WERE VERIFIED** against the tidy data from the
> coordinates drawn: Leu48 Cα / Leu235 Cα reproduces AA2AR row 567's stored
> `d_gpcrdb_tm6_tilt_246_637_ca` = 11.7347 Å, and Leu76 Cα / Leu375 Cα
> reproduces DRD2 row 8285's 17.2766 Å. Four of the drop's `ALIGNMENT.md` files
> name residues that do not reproduce the shipped distances (**D13**, **D20**).
>
> **POPULATION.** All Class A predictions under E1+E2 (broken cell, impossible
> geometry): 3,992 apo and 3,974 cognate rows, 7,966 of 9,490 total, over 40
> Class A receptors. Block A's cognate arm supplies the **full** cognate Gα
> subunit; only its α5 C-terminal 21 residues (Gα 334–354) are drawn, because
> the heterotrimer is an input this figure is not reporting.
>
> **WHAT THIS FIGURE DOES NOT SHOW:** amplitude reproduction — whether a
> receptor with further to travel travels further — which is BA-4 and is
> negative on three of four backbones. No arrow in the composition carries an
> outcome word, and every arrow is a process connector.
>
> **†** Templates-off rests on launcher static analysis, source defaults and a
> propagation test, **not** on per-row provenance: `block_a_rows.csv` has no
> column recording template usage across all 55 columns (**D19**). The figure
> marks the claim with a dagger for that reason.

---

## Every number in the frame, and where it comes from

All rates are recomputed at build time from `block_a_rows.csv` through
`figures/block_a/badata.py:core()` (E1+E2 only), restricted to
`gpcr_class == "A"`. Nothing is transcribed from the claim sheet.

| in frame | value | derivation |
|---|---|---|
| 40 Class A receptors | 40 | `cA.receptor.nunique()` |
| 25 seeds per cell | 25 | modal cell size; 378 of 380 cells are 25 rows, 2 are 20 |
| n = 3,992 predictions (apo) | 3,992 | Class A, arm == apo, E1+E2 |
| n = 3,974 predictions (cognate) | 3,974 | Class A, arm == cognate, E1+E2 |
| n = 7,966 predictions | 7,966 | the two above; 9,490 total rows, 9,461 survive E1+E2 |
| TM6 tilt ≥ 14.932 Å | 14.932 | `threshold_tilt_used`, constant on every row |
| NPxxY ≤ 9.08 Å | 9.08 | `threshold_npxxy_used`, constant on every row |
| apo → active 14.5% | 577 / 3,992 | |
| cognate → active 79.6% | 3,162 / 3,974 | |
| apo → inactive 85.5% | 3,415 / 3,992 | |
| cognate → inactive 20.4% | 812 / 3,974 | |
| 17.28 Å (Leu76 Cα / Leu375 Cα) | 17.2766 | measured from row 8285's coordinates; `cifread.verify_anchor` against the stored value, tol 2e-3 Å |
| 11.73 Å (Leu48 Cα / Leu235 Cα) | 11.7347 | measured from row 567's coordinates, same check |

**Predicate direction, checked rather than assumed.** `active` is exactly
`npxxy_active & tilt_active` on all 7,966 rows (verified). `tilt_active` rows
run 14.937–19.667 Å and non-firing rows 10.672–14.924 Å, so tilt is a
**≥** test; `npxxy_active` rows run 2.404–9.078 Å and non-firing rows
9.080–23.531 Å, so NPxxY-OH is a **≤** test. The inequality glyphs in the SCORE
box were set from those ranges, not from the axis names.

### NEW — a mis-named column in `headline_by_backbone.csv`

`apo_active_rate_panel_mean` and `cognate_active_rate_panel_mean` are **not
panel means.** They reproduce, to every digit, the *pooled row-level* rate over
**all** rows and **all** GPCR classes with no exclusions:

| backbone | shipped `apo_active_rate_panel_mean` | pooled row-level, all rows | unweighted mean of cell `both_fire_rate` |
|---|---:|---:|---:|
| boltz | 0.159833 | **0.159833** | 0.101667 |
| chai | 0.326667 | **0.326667** | 0.240000 |
| of3 | 0.241667 | **0.241667** | 0.083333 |
| protenix | 0.145000 | **0.145000** | 0.057500 |

The true unweighted per-cell mean differs by up to 16 percentage points. The
column name will mislead anyone who quotes it as a panel mean; it should be
read as a pooled rate. **This figure does not use those columns.** It draws
Class-A-only pooled row-level rates under E1+E2, which are 14.5% / 79.6%; the
corresponding all-class pooled rates are 21.8% / 81.8%. Restricting to Class A
is the E4 rationale in `badata.py` — the predicate is Class-A calibrated — and
the frame says "40 Class A receptors" and "Class A" so the restriction is not
hidden. *(Not filed in `DISCREPANCY_REPORT.md`: this session must not edit it.
Someone should.)*

`analysis/block_a/verify_claims.py` was run before this build: 15 of 34 checks
mismatch, none of them on anything this figure draws. The SC-2 mismatches are
about `fraction_of_way_to_active` and its denominator; the SC-1 mismatches are
about which bootstrap column the CIs came from. Neither quantity is in the
frame.

---

## Render provenance

Both insets are matplotlib depth-of-field renders through `figures/dofrender.py`
— no PyMOL in this path.

| | called ACTIVE inset | called INACTIVE inset |
|---|---|---|
| file | `11_structures/success_case/DRD2__cognate__of3__seed849213874__row8285.cif` | `11_structures/confidently_wrong/AA2AR__apo__boltz__seed748489558__row567.cif` |
| sha256 (first 16) | `10a0d49ab36db71d…` | `813d34c27aa3f915…` |
| row | 8285 | 567 |
| cell | DRD2 × OpenFold-3 × cognate, n = 25 | AA2AR × Boltz-2 × apo, n = 25 |
| selection | median `rmsd_to_active_ref`, rank 13/25 | highest `plddt_mean`, 100th pct |
| camera | `camera.py` side view, extracellular up, via `dofrender.camera_frame` | same rule |
| drawn window | chain A 30–443 minus ICL3 | chain A 1–316 minus ICL3 |
| ICL3 dropped | Cα 219–365, 147 residues, mean pLDDT 38.5 vs 86.0 for the rest | Cα 207–225, 19 residues, mean pLDDT 70.0 vs 84.3 |
| depth behind focal plane | 36% | 50% |
| partner drawn | Gα 334–354 only (chain B), green | none |
| measured | 17.2766 Å, Leu76 Cα – Leu375 Cα | 11.7347 Å, Leu48 Cα – Leu235 Cα |

**One scale across both insets.** `dofrender.frame_limits` frames whatever it
is given, which is right for a standalone panel and wrong for a pair: two
renders each cropped to their own extent are at two different
Ångström-per-millimetre, and a reader comparing where TM6 sits in one against
the other is then comparing two rulers ("small multiples not on one footing",
a recorded corpus camera defect). So the half-height `frame_limits` would
choose is computed for **both** scenes first and the larger is imposed on both,
and a 10 Å bar is drawn on each so the shared scale is visible rather than
merely asserted. The larger half-height is DRD2's, so nothing is clipped from
either.

**The camera passes the 7TM body with ICL3 excluded.** `camera.py` fits the
bundle axis over every Cα in the receptor window, and DRD2's predicted ICL3 is
147 residues of mean-pLDDT-38.5 coil out of 414; fitting through it tilts the
"membrane normal" by 35.5° and draws the α5 helix at an angle it does not have.
Both insets pass `ca=` explicitly for that reason.

**Grey is the invariant scaffold** (`RENDER_CONVENTIONS` §1). Colour appears on
exactly three things and each means one thing everywhere in the figure:

| colour | meaning | where it appears |
|---|---|---|
| green `#009E73` | the cognate Gα co-input | input chip 2, the α5 21-mer in the active inset, the cognate bar in both outcome boxes |
| vermillion `#D55E00` | the predicate called it active | TM6 in the active inset, the *called ACTIVE* header and border |
| blue `#0072B2` | the predicate called it inactive | TM6 in the inactive inset, the *called INACTIVE* header and border |

Everything else — the scaffold, the process boxes, the connectors, the apo bar
— is grey. The apo arm is grey **because it is the control**, which is the same
rule, not a second one.

---

## Defects this composition closes by construction

| corpus defect | count in the 232-render survey | how it is closed here |
|---|---:|---|
| hand-picked example, selection rule unstated | 59 | both selection rules are in the caption block above, with cell, n, statistic and percentile |
| no quantitative panel behind the render's claim | 58 | the quantitative panel **is** the outcome box: the render and the rate it illustrates share a border |
| magnitude with no statement of which atoms | — (`hilger2020gcgr`) | every drawn distance carries the atom pair, and the pairs are defined once in the SCORE box |
| displacement drawn as an arrow with no number | — (`ye2026multistatebias`, `tejero2024opsin`) | no arrow anywhere carries an outcome word; the numbers are on the renders and in the bars |
| small multiples not on one footing | — | both insets share one imposed scale, with 10 Å bars |
| bar standing in for a distribution | recurring | the bars are **proportions with numerator and denominator printed**, not summaries of a distribution; the distribution behind the same contrast is BA-6 / BA-7 |

---

## Known limitations of this candidate

1. **The renders are small.** 16 × 18.6 mm each. At 80 mm reduction a reader
   sees a grey bundle with one coloured helix; they do not read TM6 geometry
   off it. That is the pipeline form's price and it is paid deliberately — the
   bars carry the result, the renders carry recognition.
2. **Two receptors, again.** The archive constraint is not fixable by
   composition. This form softens it (the insets illustrate a call rather than
   forming a comparison) but does not remove it.
3. **Text density.** Four boxes of small type is more reading than a
   before/after pair. It survives 80 mm but it is not a one-second read.
4. **The α5 21-mer appears only in the active inset**, where it is 2.8 pt of
   green line. The co-input is named three times in words and drawn once, small.
   If the paper's claim is *the peptide is the cause*, this form under-draws the
   cause and over-draws the machinery.
5. **`n_receptors` for the drop is 48** (40 A, 4 B, 4 F). This figure scopes to
   Class A and says so, but a reader who wants the whole drop will not find it
   in the frame.
