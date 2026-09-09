# RENDER_CONVENTIONS.md — how this literature draws a conformational change

Built 2026-09-09 by rasterizing and **viewing** render panels, not by reading notes. The figure
tables in `notes/` record `data_shape`, `panels` and `hides` but never recorded colour, so this
file closes that gap. It covers the render idiom for a **partner- or ligand-induced conformational
change** specifically, which is the claim this manuscript makes.

Panels viewed: `hilger2020gcgr` Fig 1 (p3) and Fig 3 (p5); `tejero2024opsin` Fig 5 (p8);
`tran2026nanogs` Fig 1 (p3); `ye2026multistatebias` Fig 4 (p12); `yang2025statespecific` Fig 4e (p6).

---

## 1. Grey means "not the subject", not "reference"

**There is no reference-grey / prediction-coloured convention in this literature.** The rule that
actually operates is subject versus context.

- `ye2026multistatebias` Fig 4A p12 is the clearest case and the most transferable. The entire
  receptor is drawn **grey**; only TM6 is coloured, red for the inactive reference (9CHU) and
  green for the active (8GEG). Everything that does not move is grey.
- `tran2026nanogs` Fig 1A-B p3: receptor **green**, peptide **orange**, both subjects; the rest of
  the receptor is a pale, near-transparent wash.
- `tran2026nanogs` Fig 1 "Design strategy" cartoon p3: the generic receptor barrel is **grey**, the
  designed peptide is **orange**. Grey is the thing you are not making a claim about.
- `hilger2020gcgr` Fig 1A p3: the accessory nanobody Nb35 is **grey** while every functional
  subunit is coloured (GCGR cyan, ZP3780 red, Gα<sub>s</sub> yellow, Gβ purple, Gγ dark blue).

**House rule this supports:** grey the invariant scaffold, colour only the element carrying the
claim. Do not grey a structure merely because it is the reference.

## 2. The partner is dropped or reduced when the receptor is the subject

This is the strongest convention found and the least obvious.

- `hilger2020gcgr` Fig 1B-D p3: the three-structure superposition showing the 18 Å TM6 movement
  contains **no G protein at all**, even though the active structure is a Gs complex. The partner
  appears only in the density map, panel A.
- `ye2026multistatebias` Fig 4A p12: same. 8GEG is Gs-bound; the render shows receptor only.
- `tejero2024opsin` Fig 5 p8: the partner is reduced to the contacting fragment, and the caption
  says so twice — *"Only the α5 helix of the Gα subunit is shown for the G protein."*

**For an α5 C-terminal render this is the licence to draw the peptide alone.** Showing the whole
heterotrimer would depict an input that was never supplied.

## 3. More than two states: distinct hue, and pairwise panels

Never lightness within one hue.

- `tejero2024opsin` Fig 5 p8: JSR1-jsGiq_1 **salmon**, JSR1-hGi **olive**, JSR1-jsGiq_2 **teal**,
  and the three states are shown as **three pairwise panels**, never one three-way overlay.
- `hilger2020gcgr` Fig 1B-D p3: three states in one overlay — active complex **cyan**, partial
  agonist 5YQZ **orange**, inactive 5XEZ **lavender**. Readable, but at three it is the ceiling.

## 4. Transparency de-emphasises; it is never applied to the subject

- `tejero2024opsin` Fig 5 p8: helices under discussion at full opacity, the rest of the bundle
  ghosted. This is what makes a busy superposition readable.
- `tran2026nanogs` Fig 1A-B p3: background receptor as a pale wash behind the sticks.

## 5. Conventions that recur and cost nothing to adopt

- **Two views, always the same pair**: side view along the bundle, plus a cytoplasmic view rotated
  90°. `hilger` Fig 3A-B, `ye` Fig 4A, `tejero` Fig 5a-b, `yang` Fig 4e.
- **Colour legend as coloured text above or inside the panel**, not a legend box.
  `hilger` Fig 1B, `tejero` Fig 5 (panel titles are the legend).
- **Emphasis by representation as well as colour**: `ye` Fig 4A draws TM6 as thick spheres against
  thin cartoon for everything else.
- **Arrows for direction of motion**, distinct from the colour coding.
- **Surface rather than cartoon** when the point is a cavity: `tran` Fig 1D-E (hydropathy-coloured
  surface), `yang` Fig 4e (pale pink surface with the peptide as sticks).
- **Per-residue detail goes in a strip below the render**, not as labels on it: `yang` Fig 4e
  carries an interaction fingerprint as a row of coloured circles with its own legend.

## 6. Where the magnitude goes — the field is split, and both halves fail

- **On the panel**: `hilger2020gcgr` prints "18 Å" and "105°" on Fig 1B, and "17.4 Å" on Fig 3A;
  `tejero2024opsin` prints "17°" on Fig 5c. But `hides` for `hilger` Fig 1B-D records that the
  numbers are drawn "with **no statement of which atoms were measured**", and Fig 3A-B records that
  17.4 Å and 18 Å "are the same physical displacement measured at two different residues" and are
  never reconciled.
- **Not on the panel**: `ye2026multistatebias` Fig 4A — `hides`: "The ~14 Å TM6 displacement quoted
  in text (p.13) is shown only as an arrow; no scale bar or measured distance on the figure."
  `tejero2024opsin` Fig 1C-E — "asserts the outward movement of TM5/TM6 with arrows and no distance
  annotation — the paper's central activation claim has no number in any panel."

**Neither half of the field annotates a magnitude with its atom pair.** Doing so is cheap and
puts a figure ahead of every render surveyed here.

## Licence, for anything adapted

`tejero2024opsin` CC BY 4.0 (redrawable) · `tran2026nanogs` CC BY-NC (redrawable, non-commercial) ·
`ye2026multistatebias` **CC-BY-NC-ND — look only** · `yang2025statespecific` **ND — look only** ·
`hilger2020gcgr` **Science, all rights reserved — look only**.
