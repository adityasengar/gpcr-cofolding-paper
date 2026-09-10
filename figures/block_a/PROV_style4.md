# PROV_style4.md — provenance for `ga_style4_axis`

**Candidate graphical abstract, style 4: "the measurement is the spine".**
Built 2026-09-10 by the figures session, in parallel with three other candidate
styles. Not yet a ledger entry in `FIGURES.md` — it is a candidate, and only the
one Aditya picks earns an entry.

| | |
|---|---|
| script | `figures/block_a/panels/ga_style4_axis.py` |
| output | `figures/out/ga_style4_axis.pdf` · `.png` (600 dpi) |
| page | **100 × 130 mm, portrait**, fixed canvas (`savefig.bbox` disabled) |
| PDF MediaBox | `283.4646 × 368.5039 pt` = 100.000 × 130.000 mm — checked |
| reduction | ×0.615 to an 80 mm long edge, the same factor GA-1 was built for |
| rebuild | `python3 figures/block_a/panels/ga_style4_axis.py` |

Nothing outside `figures/` was written. `dofrender.py`, `dofscenes.py`,
`figstyle.py`, `figpanels.py`, `ga1_hero.py`, `FIGURES.md` and
`FIGURE_PROVENANCE.md` were **read and imported, never modified** — three other
candidates were reading them at the same time. The receptor-drawing helpers,
the ICL3 window rule and the anchor table are imported from `dofscenes` /
`hero_renders` rather than forked, and the script asserts at import that those
names still exist rather than failing halfway through a render.

---

## What the figure is

One vertical ruler, in Ångström, carrying **TM6 tilt, 2×46 Cα – 6×37 Cα**.
Everything in the composition is placed on it:

- the **predicate's tilt threshold**, 14.932 Å, drawn edge to edge;
- the **population** as a back-to-back density, apo growing left out of the
  ruler and cognate growing right;
- the **two rendered predictions**, whose boxes are positioned so that the box
  centre sits at the row's measured value. They are not labelled with their
  values; their position *is* the value, and a leader ties the box edge, the
  point on that arm's own density, and a tick across the ruler at one height.

Ruler scale: **9.684 mm per Å** over 10.4–19.9 Å. The gap between the two boxes'
centres is **53.67 mm = 5.542 Å**, printed by the script on every run.

---

## Numbers on the figure, and where each comes from

| on the figure | value | source |
|---|---|---|
| apo render value | **11.7347 Å** | AA2AR row 567, `d_gpcrdb_tm6_tilt_246_637_ca`; re-measured Leu48 Cα – Leu235 Cα |
| cognate render value | **17.2766 Å** | DRD2 row 8285, same column; re-measured Leu76 Cα – Leu375 Cα |
| threshold | **14.932 Å** | `badata.THR_TILT`, constant across all 9,490 rows |
| apo n | **3,992** | Class A, E1+E2 excluded, arm = apo |
| cognate n | **3,974** | Class A, E1+E2 excluded, arm = cognate |
| apo % above threshold | **17.2%** | fraction of those 3,992 with tilt > 14.932 |
| cognate % above threshold | **94.0%** | fraction of those 3,974 |

**Filter, stated in full.** `badata.core()` — E1 (broken cell, cell mean pLDDT
< 50) and E2 (impossible geometry, NPxxY-OH < 2.4 Å) excluded, 9,461 of 9,490
rows kept — then **E4** (Class A only), removing 1,495 Class B/F rows, leaving
7,966. `excl_any` is **never** used: it fires on 54% of rows and is wrong for a
raw distribution, because E3 is only relevant where a reference value is a
denominator or a regression predictor and E5 is a sensitivity filter.

Both rendered rows are inside that population (`row_id` 567 and 8285 both have
`gpcr_class == "A"`, `excl_E1 == False`, `excl_E2 == False`).

**Anchor verification.** Both pairs go through
`hero_renders.verify` → `cifread.verify_anchor`, which refuses any pair whose
coordinate distance differs from the row's stored value by more than 2×10⁻³ Å.
Run log:

```
verified AA2AR row 567  tilt 11.7347 A (LEU48-LEU235)  NPxxY-OH 9.6079 A (TYR197-TYR288)
verified DRD2 row 8285  tilt 17.2766 A (LEU76-LEU375)  NPxxY-OH 3.9883 A (TYR209-TYR426)
```

Four of the drop's `ALIGNMENT.md` files name residues that do **not** reproduce
the shipped distances (DISCREPANCY_REPORT D13, D20); none of those residue
numbers reaches this figure. The box position is additionally asserted in page
units: the script raises if a render box centre lands more than 0.03 mm from
`mm(measured value)`.

**Every measured distance carries its atom pair.** Each render draws the dashed
2×46 Cα – 6×37 Cα segment with its two endpoint atoms and the pair named on the
panel (`Leu48 (2×46) Cα / Leu235 (6×37) Cα`, `Leu76 / Leu375`). The *value* for
that segment is on the ruler, tied to it by the leader — that is the point of
the style. Not one of the 232 render rows in the corpus survey annotates a
magnitude with its atom pair.

---

## The hazard this style creates, and what was done about it

A metric axis with two structures on it invites the reading *"the models
reproduce this scale"*. **They do not.** Amplitude reproduction is negative on
three of four backbones (BA-4), and under `class_a_only` the tilt slopes go
negative for two of them (D3); `sd_predictor` on the tilt axis is 1.17 Å, i.e.
essentially no dynamic range. So:

- **no arrow and no caliper** between the two structures, and the vertical gap
  is deliberately left unlabelled — labelling it would convert "where two
  predictions fall" into "how far a receptor moved";
- **no deposited reference value is marked on the ruler.** Putting 7JVR's
  17.586 Å beside DRD2's 17.277 Å would be a magnitude-tracking picture in
  miniature;
- the footnote opens with it, in words, rather than burying it at the end:
  *"The ruler says WHERE these two predictions fall. It is NOT evidence that
  predicted magnitude tracks reference magnitude (BA-4: negative on 3 of 4
  backbones), so nothing here measures the gap between them."*

## What was SUPPLIED versus what is DRAWN — the correction of 2026-09-10

**Block A supplies the FULL cognate Gα subunit as the co-input.** The α5
C-terminal 21 residues (Gα 334–354) are what is *drawn*, following
RENDER_CONVENTIONS §2 and `tejero2024opsin` Fig 5. Those are different
statements, and conflating them asserts the peptide result that Block A does not
test — Block B will — against `CLAIMS.md`'s explicit rule, *"No Block A sentence
may imply the peptide result."*

The first build of this figure headlined **"Supply the Gα α5 C-terminal 21-mer
and the prediction lands on the active side of the TM6-tilt threshold"** — the
forbidden claim, in the largest type on the page, two inches above an annotation
that stated it correctly. Caught in review by the coordinator and corrected the
same day. The split now enforced:

| element | says | correct because |
|---|---|---|
| headline | "Supply the **cognate Gα** and the prediction lands on the active side of the TM6-tilt threshold" | names the INPUT |
| render titles | "+ cognate Gα supplied" | names the INPUT |
| arm label | "+ cognate Gα supplied as a co-input" | names the INPUT |
| colour key | "α5 C-terminal 21-mer (Gα 334–354)" | names the DRAWN element |
| footnote, last line | "The INPUT was the full cognate Gα subunit; only its α5 C-terminal 21 residues are drawn." | states the gap |
| caption block | "Block A's cognate arm supplies the FULL cognate Gα subunit; only its alpha5 C-terminal 21 residues (Gα 334-354) are drawn" | states the gap |

The module docstring carries a `WHAT THE HEADLINE MAY NOT SAY` section so the
next edit to the headline cannot re-introduce it silently. That footnote line
replaced "Selection rules are in the caption", which was implied.

## Different receptors — and this style makes it more visible, not less

`11_structures/` ships one apo prediction (AA2AR) and three cognate ones; no
receptor has both arms, so the two renders cannot be the same receptor. A shared
axis invites subtraction by eye, so the limitation is handled explicitly rather
than hidden: each render is titled with its own receptor and backbone, and the
footnote says *"The two renders are DIFFERENT RECEPTORS — the archive ships one
prediction per case — so the density, not the pair, carries the contrast."*

## Two scales on one page

The ruler is 9.68 mm/Å; the renders are roughly 0.4 mm/Å and each carries its
own 10 Å bar. Positions on the ruler are at ruler scale; nothing is measured
across the boundary. Stated in the footnote.

## Render conventions honoured

- **Grey is the invariant scaffold**, never "reference" (RENDER_CONVENTIONS §1):
  the receptor bundle is a grey depth-weighted heavy-atom density plus a grey
  hairline Cα trace, in both renders.
- **Colour only on what carries the claim**: TM6 (blue where the predicate calls
  the row inactive, vermillion where active) and the α5 C-terminal 21-mer
  (green). Green means "the cognate Gα co-input" throughout, which is why the
  cognate density and the α5 helix are the same green.
- **The α5 21-mer alone, never the heterotrimer** (§2). Block A's cognate arm
  supplies the full Gα subunit; only Gα 334–354 is drawn, and the caption says
  the full subunit was the input.
- **Colour key as coloured words**, not a legend box (§5).
- **ICL3 dropped by one rule in both panels** (`dofscenes._icl3_window`) and the
  omission recorded in the caption block with the pLDDT of what was dropped.
- **Soft focus encodes depth only** and the footnote says so, as required.
  Focal planes are at the claim (`dofrender.focal_plane` / `focus_report`):
  50% of panel depth behind focus for the apo render, 36% for the cognate one,
  and no state-defining atom is on the blurred side of either.

## Defects deliberately avoided

- selection rule stated (in the caption block the script prints, and in the
  render sub-titles: "row 567 of 25 seeds", "row 8285 of 25 seeds") — the
  corpus's commonest render defect, 59 of 232 rows;
- a quantitative panel stands behind the render claim — the density *is* that
  panel, and it is the spine rather than a strip underneath — 58 of 232 rows;
- n stated on the figure for both arms;
- one axis, one measure — no second measure shares it;
- no bar standing in for a distribution;
- the axis is not broken: it runs 10.4–19.9 Å against a data range of
  10.67–19.67 Å.

## Caption

`ga_style4_axis.py` prints the full required caption text on every run
(`caption_block()`); it is reproduced verbatim into `manuscript/sections/
figures.tex` if this candidate is chosen. It carries the two selection rules,
the anchor verification, the two-scale statement, the amplitude caveat, the
different-receptors statement, the population and filter, and the ICL3
omissions.

## Known limitations

1. **The apo render is muddier than the cognate one.** Same code path and same
   blur parameters; AA2AR is a 316-residue receptor in a tighter crop, so its
   heavy-atom density is denser. Not corrected, because correcting it per panel
   would put the two cells on different footings.
2. **The tilt axis alone is not the predicate.** The predicate is tilt **AND**
   NPxxY-OH; only the tilt axis is drawn. Both rendered rows agree on both axes
   (row 567: 11.73 / 9.61, inactive on both; row 8285: 17.28 / 3.99, active on
   both), and the footnote states the restriction. The percentages on the figure
   are "above the tilt threshold", not "predicate-active" — those are 14.5% and
   79.6% respectively and are **not** shown here.
3. **The fixed canvas clips rather than expands.** That is deliberate — a
   position on this page is a measured quantity, so the page may not be
   rescaled after the geometry is fixed — but it means an over-long string is
   lost silently. Two guards now exist: the footnote wrap raises if it would run
   off the bottom, and each render title's width is measured and raises if it
   would cross the page edge. Both were added after a one-line cognate
   sub-title lost its final word.
4. **The apo arm label sits high on the left**, where the apo lobe has nothing
   to say, because the lower-left quadrant is occupied by the apo render. A
   swatch flush against the apo side of the ruler, filled at the same colour and
   alpha as the lobe, is what ties the words to the curve.
