# PROV_style2.md — provenance for GA-STYLE-2, "population first"

One of four graphical-abstract candidates built in parallel on 2026-09-10. This file
belongs to this candidate only; it deliberately does not touch `FIGURES.md` or
`FIGURE_PROVENANCE.md`, which three other sessions are writing to.

| | |
|---|---|
| script | `figures/block_a/panels/ga_style2_population.py` |
| output | `figures/out/ga_style2_population.pdf` · `.png` (600 dpi) |
| canvas | drawn at 152 × 126 mm; `savefig.bbox="tight"` trims it to **145.3 × 120.1 mm** (412 × 340 pt) |
| built | `python3 figures/block_a/panels/ga_style2_population.py` — prints the required caption to stdout |
| style | the DATA is the hero; the two structure renders are subordinate callouts pinned to the axis |

---

## What the figure claims

A 21-residue Gα α5 C-terminal co-input, supplied alongside the receptor sequence,
separates the predicted Class A population into two on the TM6 tilt axis. It claims
**which state is reached**, and nothing about amplitude.

## Population and filter

| | |
|---|---|
| source | `data/block_a/01_rows/block_a_rows.csv` (sha256 `28852f6048e9d313…`, 12,050,840 bytes) |
| loader | `figures/block_a/badata.py: core_class_a()` |
| filter | **E1+E2 excluded, Class A only (E4)** — `excl_E1 | excl_E2` dropped, `gpcr_class == "A"` kept |
| n | **7,966 of 9,490 rows** — 3,992 apo, 3,974 cognate |
| coverage | 40 receptors × 4 backbones × 25 seeds (median cell size) |

`excl_any` is **not** used anywhere. E3 is a property of the receptor's *reference*
and cannot apply to a raw distribution, which divides by nothing; E5 is a sensitivity
set. Both are recorded in `badata.py`'s "exclusion trap" docstring.

## Every number drawn, and where it comes from

All of these are recomputed inside the script from the frame it plots. **No number in
this figure is a typed-in constant** — including the two percentages in the lane
labels, the receptor/backbone/seed counts in the subline, and the active rates in the
bottom sentence.

| drawn | value | derivation |
|---|---:|---|
| apo n | 3,992 | `(arm == "apo").sum()` after the filter |
| cognate n | 3,974 | `(arm == "cognate").sum()` |
| apo median tilt | 12.186 Å | `median(d_gpcrdb_tm6_tilt_246_637_ca)` |
| apo IQR | 11.792 – 13.678 Å | 25th/75th percentile |
| cognate median tilt | 17.471 Å | as above |
| cognate IQR | 17.061 – 17.928 Å | as above |
| tilt threshold | 14.932 Å | `badata.THR_TILT`, constant across all 9,490 rows |
| apo above threshold | 17.2% | `(tilt > THR_TILT).mean()` |
| cognate above threshold | 94.0% | as above |
| NPxxY threshold | 9.080 Å | `badata.THR_NPXXY` |
| apo called active | 14.5% | `active.mean()` — the shipped predicate column |
| cognate called active | 79.6% | as above |
| rate ratio | 5.5× | 0.7957 / 0.1445 |
| apo card value | 11.7347 Å | row 567, verified from coordinates (below) |
| cognate card value | 17.2766 Å | row 8285, verified from coordinates (below) |
| apo card percentile | 20th | `(apo tilt < 11.7347).mean()` |
| cognate card percentile | 39th | `(cognate tilt < 17.2766).mean()` |

The gap between **94.0% (tilt alone)** and **79.6% (the predicate)** is the reason the
NPxxY strip is in the figure at all. A composition that marks one threshold on the hero
axis and then reports the predicate rate is mis-stating its own rule unless the second
axis is drawn.

## The two render cards

Both are drawn by `dofrender.py` through `dofscenes.py`'s geometry helpers (imported,
not modified). Side view, camera from `camera.py`'s rule via `dofrender.camera_frame`,
with the 7TM body minus ICL3 passed as the axis-fitting cloud — DRD2's predicted ICL3
bends a whole-window principal axis by 35.5°.

### Left card — AA2AR, apo

| | |
|---|---|
| file | `data/block_a/11_structures/confidently_wrong/AA2AR__apo__boltz__seed748489558__row567.cif` (sha256 `813d34c27aa3f915…`) |
| row | 567 · AA2AR × Boltz-2 × apo · `cell_id AA2AR_apo_boltz` |
| selected from | 25 seeds in the cell |
| selection rule | the row with the **highest `plddt_mean`** in the cell (73.93; cell median 72.04) — the 100th percentile on confidence |
| where it falls | **20th percentile of the apo arm** on tilt — a typical apo row, not an extreme one |
| predicate | INACTIVE (TM6 drawn in `figstyle.BLUE`) |
| note | it sits 0.95 Å Cα RMSD from AA2AR's **inactive** reference. The directory name `confidently_wrong` is wrong — this is a correct apo prediction (DISCREPANCY_REPORT **D12**) and the name is not repeated anywhere in this figure. |
| `11_structures/SELECTION.md` | states a different rule ("top-quintile RMSD-to-active, highest pLDDT within") which selects row 552, not the shipped 567. Highest-pLDDT-in-cell is what 567 actually satisfies. |

### Right card — DRD2, cognate Gα

| | |
|---|---|
| file | `data/block_a/11_structures/success_case/DRD2__cognate__of3__seed849213874__row8285.cif` (sha256 `10a0d49ab36db71d…`) |
| row | 8285 · DRD2 × OpenFold-3 × cognate · `cell_id DRD2_cognate_of3` |
| selected from | 25 seeds in the cell |
| selection rule | the row with the **median `rmsd_to_active_ref`** in the cell (1.218 Å shipped; rank 13 of 25, cell range 1.020–1.507 Å). All 25 seeds of that cell are called active, so this is a typical row, not a best case. |
| where it falls | **39th percentile of the cognate arm** on tilt |
| predicate | ACTIVE (TM6 drawn in `figstyle.VERM`) |
| partner drawn | **only Gα 334–354, the α5 C-terminal 21-mer**, in `figstyle.GREEN`. Block A's cognate arm supplies the FULL cognate Gα subunit (chain B, 354 residues); the heterotrimer is an input this figure is not reporting, and the card says so in one line. `tejero2024opsin` Fig 5 is the precedent ("Only the α5 helix of the Gα subunit is shown"). |
| not used | `rmsd_to_active_ref` is quoted as the **selection statistic only**. It does not reproduce from the coordinates (D22 / FIGURE_PROVENANCE) and is not presented as anything this figure measures. |

### Anchor verification — run before anything is drawn

`hero_renders.verify()` → `cifread.verify_anchor()`, tolerance 2e-3 Å, raises otherwise.

```
verified AA2AR row 567  tilt 11.7347 Å (LEU48–LEU235)  NPxxY-OH 9.6079 Å (TYR197–TYR288)
verified DRD2 row 8285  tilt 17.2766 Å (LEU76–LEU375)  NPxxY-OH 3.9883 Å (TYR209–TYR426)
```

Both reproduce the values stored for those rows in `block_a_rows.csv` exactly. The
script additionally asserts the drawn value equals the CSV value before saving. Four of
the drop's `ALIGNMENT.md` files name residues that do **not** reproduce the shipped
distances (**D13**, **D20**); `confidently_wrong/ALIGNMENT.md` names L88 and Y213 for
two of AA2AR's four anchors and is wrong.

### ICL3, dropped by one rule and stated

`dofscenes._icl3_window` drops the TM5→TM6 stretch from both cards by the same rule, and
the caption reports what was dropped with its confidence:

- AA2AR row 567 — Cα 207–225, 19 residues, mean pLDDT 70.0 against 84.3 for the rest
- DRD2 row 8285 — Cα 219–365, 147 residues, mean pLDDT 38.5 against 86.0 for the rest

## Encoding

| channel | meaning |
|---|---|
| grey `#6E6E6E` | the **apo arm** in the population; also the invariant receptor bundle in both cards (`dofrender.SCAFFOLD`) — never "reference" |
| green `#009E73` | the **cognate Gα arm**, and the α5 C-terminal 21-mer in the right card. One colour, one meaning, throughout the paper (`figstyle.ARM_COLOURS`) |
| blue `#0072B2` | TM6 where the predicate calls the row **inactive** (`figstyle.STATE_COLOURS`) |
| vermillion `#D55E00` | TM6 where the predicate calls it **active**; also the pale tint on the active side of each threshold |
| soft focus | **depth only.** It carries no interpretive meaning, and the footnote says so on the panel. Nothing in the corpus uses this technique, so there is no benefit of the doubt to be had — `dofrender.focal_plane` puts the focal plane at the back of the claim set and `focus_report` refuses a view that cannot hold the whole claim in focus (apo card: 50% of depth behind the plane; cognate card: 36%). |

Palette is Okabe-Ito throughout. The two colour vocabularies — arm and predicate call —
are both named in the frame: the lane labels carry the arm, and each card carries
"TM6 — predicate: ACTIVE/INACTIVE" printed in the colour TM6 is drawn in.

## Design decisions a reviewer may ask about

**Why the population leads.** The two dominant defects in the corpus's 232 structure
renders are a hand-picked example with the selection rule unstated (59 rows) and no
quantitative panel standing behind the claim the render makes (58 rows). Both are
failures of *hierarchy*. Drawing the distribution ten times larger than the renders, and
labelling each render with its percentile within its own arm, makes both structurally
impossible rather than merely disclosed.

**Why the cards sit cross-lane.** Each render's tilt value falls at its own arm's mode,
so a card placed near its own value would sit on top of its own data. The only regions
of the frame with nothing drawn in them are the cognate lane below 13 Å and the apo lane
above 17.9 Å. The leader line, not the card's x position, is what pins each card to its
value; the tick it lands on stands in the row's own lane. Both minor modes — apo above
the threshold, cognate below it — are real and are left visible.

**Why the value is beside the card and not on it.** This is the one place the
composition departs from `dofrender.measured_distance`, and it is a legibility decision:
at 21 mm the value's label box covers half the receptor, and after reduction its
atom-pair line falls under 2 pt. The card draws the dash and its two endpoint atoms in
the house grammar; the block beside it carries the value **and** the atom pair
("TM6 tilt 11.73 Å · Leu48 Cα – Leu235 Cα") at a size that survives. Every measured
distance still carries both.

**Why no on-axis value labels.** A white label box at either mark lands on the rising
flank of that arm's own density and would hide the observations the mark exists to sit
among. The value is printed once, larger, at the other end of the leader line.

**Why no arrow, and no line joining the two values.** An arrow between the lanes would be
read as magnitude — that is BA-4, which is negative on three of four backbones. The
composition contains no arrow, no delta and no connecting line, and the footnote states
in the frame that amplitude reproduction is not what is shown.

**Two measures, two axes.** Tilt and NPxxY never share an axis. The NPxxY strip has its
own scale, its own threshold and its own stated direction (active is *below*).

**No truncated axes.** The tilt axis runs 10.35–20.05 Å against an observed range of
10.67–19.67; the NPxxY axis runs 2.0–24.0 against 2.40–23.53. Nothing is clipped.

## Known limitations of this candidate

1. **Aspect is 1.21 : 1**, not the ~1.5 : 1 a TOC slot usually prefers. The height is
   set by the two 21 × 26 mm cards plus the two lanes plus the bottom band; buying a
   wider aspect means shrinking the cards further, which is the one thing that stops
   working at 80 mm. Redrawing at 180 mm wide would give 1.5 : 1 at the cost of taking
   the load-bearing type below 5 pt after reduction.
2. **At 80 mm the 4.7 pt footnote lines are decorative**, not readable. Everything
   load-bearing — headline, both lane labels with their n and percentage, both card
   values, the threshold, the axis — reads at that size; the footnote is a
   panel-travels-without-its-caption safeguard, not thumbnail content.
3. The renders are icons at thumbnail size: a grey bundle with a coloured TM6 and a
   dashed measurement. That is the intended trade of this style, and it is the thing to
   judge it on against the render-led candidates.

## Reproduce

```bash
python3 analysis/block_a/verify_claims.py          # before believing any number
python3 figures/block_a/panels/ga_style2_population.py
```

The script prints the verified anchor lines, the lane statistics, both card percentiles,
and the full required caption text to stdout.
