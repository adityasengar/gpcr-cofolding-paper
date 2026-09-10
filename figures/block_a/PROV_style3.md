# PROV_style3.md — GA-STYLE-3, the single-frame superposition

Candidate graphical abstract, "single-frame superposition" style. Built by
`figures/block_a/panels/ga_style3_superposition.py`; writes
`figures/out/ga_style3_superposition.{pdf,png}`. Rebuild with

```bash
python3 figures/block_a/panels/ga_style3_superposition.py --view side
python3 figures/block_a/steric_exclusion.py
```

This file is separate from `FIGURE_PROVENANCE.md` on purpose: three other style
candidates were in flight in the same tree and a shared ledger file would have
collided. Fold it in when a candidate is chosen.

**Nothing in `figures/` was modified except this file, the two scripts named
above, and `figures/structures/6CM4.cif` and `6ZFZ.cif` (downloads).**
`dofrender.py`, `dofscenes.py`, `figstyle.py`, `figpanels.py` and `ga1_hero.py`
are untouched and were imported read-only. No git command was run.

---

## The design decision, and why

The brief allowed either superposing two PREDICTIONS and saying plainly that
they are different receptors, or superposing one prediction on its own
deposited reference pair. **Neither was available as written**, and the third
option taken here is better than both:

* The drop ships four prediction CIFs — one apo (AA2AR) and three cognate
  (DRD2, ACM1 x2). No receptor has both arms, so two predictions means two
  different receptors. A single frame is the *worst* form in which to admit
  that: the reader sees one grey bundle and reads one object, and the panel
  ends up arguing against its own picture.
* No prediction has both of its deposited references shipped either. DRD2 has
  7JVR (active) and no inactive; AA2AR has 5G53 (active) and no inactive.

So: **one prediction against the same receptor's deposited INACTIVE panel
reference.** DRD2 row 8285 (cognate Ga, OpenFold-3) superposed on **6CM4**,
named as DRD2's inactive reference in `02_references/reference_predicates.csv`.
Same receptor, same residue numbering, same two atoms, one grey scaffold —
a true within-receptor contrast with no confound to caption away.

The cost is stated on the panel in full: **the blue helix is a crystal
structure, not an apo prediction.** The frame therefore shows the state
*reached* with the co-input, not that the apo prediction stays closed. That
half of the claim is carried quantitatively by the ruler beneath the render,
where DRD2's own 100 apo and 100 cognate rows sit as two non-overlapping
distributions on the same axis.

`6CM4.cif` is not in the drop. It was fetched from RCSB and **verified from its
own coordinates against both values the drop stores for it** before anything
was drawn — a stronger provenance chain than the shipped files, four of whose
`ALIGNMENT.md` notes name residues that do not reproduce their own distances
(D13, D20) and one of whose CIFs is the wrong protein (D18).

---

## Console output of the build

```
verified DRD2 row 8285  tilt 17.2766 A (LEU76-LEU375)  NPxxY-OH 3.9883 A (TYR209-TYR426)
written:
  /Users/aditya/Documents/tools/Novartis_projects/paper/figures/out/ga_style3_superposition.pdf
  /Users/aditya/Documents/tools/Novartis_projects/paper/figures/out/ga_style3_superposition.png
  view            side view, extracellular up
  fit             223 Ca, 2.572 A RMSD
  prediction tilt 17.2766 A   NPxxY 3.9883 A
  6CM4       tilt 11.4459 A   NPxxY 10.0304 A
  difference      5.8306 A
  behind focus    40%
  ruler           100 apo / 100 cognate DRD2 rows
```

---

## Required caption content, verbatim from the script

```
GA-STYLE-3 — provenance and required caption content.

WHAT IS DRAWN. One frame, no panels. DRD2 (dopamine D2 receptor) predicted by
OpenFold-3 with the cognate Ga supplied as a co-input (block_a_rows.csv row
8285), superposed on 6CM4 — DRD2's deposited INACTIVE panel reference — over 223
receptor Ca (34–218 and 399–441): 2.572 A, median per-residue deviation 1.42 A,
the tail being ECL2. TM6 (366–398) and ICL3 are excluded from the
superposition, so the fit cannot absorb the displacement the frame is drawn to
show. The same fit rule against 7JVR, DRD2's deposited ACTIVE reference, which
is NOT drawn: 1.037 A over 228 Ca. View: side view, extracellular up. Grey is the receptor bundle, both
structures, and carries no claim; colour appears only on TM6 of each structure
and on the alpha5 C-terminal 21 residues.

THE INPUT WAS THE FULL COGNATE Ga SUBUNIT (chain B, 354 residues). Only its
alpha5 C-terminal 21 residues (Ga 334–354) are DRAWN, which is what the claim
is about and what this literature does (tejero2024opsin Fig 5: "Only the alpha5
helix of the Ga subunit is shown"). BLOCK A DOES NOT TEST A 21-RESIDUE PEPTIDE
CO-INPUT — that is Block B, and CLAIMS.md forbids any Block A sentence that
implies the peptide result. Nothing in the caption may call the drawn 21-mer
"the co-input"; the panel's subtitle, colour key and footnote all state that
the input was the whole subunit.

THE MEASUREMENT, ONE PAIR, TWO VALUES.
  prediction, row 8285   17.2766 A   Leu76 (2x46) CA – Leu375 (6x37) CA
  6CM4, deposited        11.4459 A   Leu76 (2x46) CA – Ala375 (6x37) CA
  difference             5.8306 A
Both were reproduced from the coordinates being drawn before being drawn
(cifread.verify_anchor, tolerance 2e-3 A). The prediction's value reproduces
row 8285's stored d_gpcrdb_tm6_tilt_246_637_ca = 17.2766 A; 6CM4's reproduces
reference_predicates.csv's d_tilt_ref = 11.445926 A. 6x37 is Leu in the
prediction and Ala in 6CM4 — a construct difference in the deposited entry. The
measured atom is CA in both, so the pair is the same pair; it is named on the
panel for each structure separately rather than once, because printing one
residue name over two different constructs is how hilger2020gcgr ends up
reporting 17.4 A and 18 A for one displacement. The two dashes share their 2x46
endpoint: after the fit those two CA are 0.260 A apart.

PROJECTION FIDELITY, which no render in the survey states. An orthographic
projection foreshortens each segment independently, so two segments can be
drawn at a ratio the data does not have. Here they are drawn at 100.0% and
100.0% of their measured lengths; the panel refuses any view that distorts
either by more than 5%, and the cytoplasmic view is refused on exactly that
test (89.9% and 79.0%).

The NPxxY axis was verified for both structures and is NOT drawn: prediction
3.9883 A, 6CM4 10.0304 A. One frame carries one pair. The second axis is BA-1a.

6CM4 IS NOT IN THE DROP. `11_structures/` ships 7JVR (DRD2 active) and no
inactive DRD2, so 6CM4.cif was fetched from RCSB into figures/structures/.
  sha256 7db4e5f162464d7e91122350718cb0e7c34b33705e4b1801ef3acb57544404c0
It is verified against BOTH values the drop stores for it — 11.445926 A tilt
and 10.030448 A NPxxY-OH — at the same residue numbers, from its own
coordinates. No ALIGNMENT.md was consulted; four of them name residues that do
not reproduce their own shipped distances (D13, D20), and one shipped CIF is
the wrong protein entirely (D18). 6CM4 carries a T4L fusion replacing native
223–362; the fusion is renumbered 1002–1161 in the file, lies outside both the
drawn window and the fit window, and contains none of the four anchor atoms.
reference_metadata.csv flags `predicate_window_hit = both` for this entry,
which is a caveat about the deposited construct and not about this drawing.

SELECTION RULE, on the panel and here. DRD2 x OpenFold-3 x cognate cell,
n = 25 seeds: the row with the MEDIAN rmsd_to_active_ref in the cell (1.218 A
shipped; rank 13 of 25, cell range 1.020–1.507 A). A typical row of its cell,
not a best case; the predicate calls all 25 rows of that cell active. The
shipped RMSD does not reproduce from the coordinates (D22) and is therefore
quoted only as the statistic the row was selected on, never as something this
picture measures — which is why the two RMSDs printed on the panel are computed
here, on one stated atom set, for both references. 6CM4 was not selected: it is
the only inactive DRD2 panel reference in reference_predicates.csv.

STERIC EXCLUSION — the annotation in the lower left, and why the blue and green
tubes overlap. Superposed, 6CM4's TM6 lands in the volume the alpha5 occupies.
86 of the alpha5's 166 heavy atoms lie within 4.0 A of a 6CM4 TM6 heavy atom
(295 pairs below 3.0 A; closest 0.22 A, Glu368 CA – Leu348 N). Against the
PREDICTION's OWN TM6 the same count is 3 of 166, which is what "no exclusion"
looks like on this scale. This is MUTUAL EXCLUSION OF VOLUME and must never be
reported as a contact — a 0.22 A heavy-atom separation is a clash, and calling
it a contact invites the obvious objection. Atom sets, controls, and a second
receptor are in `figures/block_a/steric_exclusion.py`; its result is summarised
in PROV_style3.md. The active control is NOT zero and must not be reported as
though it were.

THE RULER. DRD2's own rows under E1+E2: 100 apo and 100 cognate, 4 backbones x
25 seeds x 2 arms, smoothed on the same tilt axis the render measures. Apo
median 11.86 A, cognate median 17.21 A. Both of DRD2's deposited references are
marked with dotted drop lines and carets (6CM4 11.446 A, 7JVR 17.586 A) and the
drawn row with a solid stem, so a crystal structure is never mixed into a cloud
of predictions. For scale beyond this receptor, Class A under E1+E2: apo median
12.19 A (n=3,992), cognate median 17.47 A (n=3,974) — stated as text on the figure, not
drawn, because this frame is about one receptor.

WHAT THE FRAME DOES NOT SHOW.
  * That the apo prediction stays closed. The blue helix is a crystal
    structure. DRD2's apo predictions are the grey distribution in the ruler;
    their coordinates are not in the drop.
  * Amplitude reproduction (BA-4), which is negative on three of four
    backbones. There is no arrow in the frame for that reason.
  * Anything about confidence. Row 8285 was selected on RMSD, not pLDDT.
  * A 21-residue peptide co-input. See above.

REPRESENTATION. The tubes and the hairline traces are the CA path smoothed with
a 4-residue running mean — the helix axis, which is what a cartoon tube is.
Without it two superposed CA coils 6 A apart read as a tangle. NOTHING MEASURED
PASSES THROUGH THE SMOOTHING: every dash, endpoint, printed value, RMSD and
steric count is computed from unsmoothed atom coordinates.

FOCUS. Both TM6 runs, all four tilt anchor atoms and the whole alpha5 are
passed to dofrender.focal_plane(); the focal plane sits at the back of that set
and focus_report() confirms nothing state-defining is behind it (40% of the
panel's depth range lies behind the plane and is softened). Soft focus encodes
depth only and carries no interpretive meaning. The caption must say so.

CAMERA. dofrender.camera_frame, i.e. block_a/camera.py's rule, fed the 7TM body
with ICL3 excluded. Not chosen by eye. camera.py fits the bundle axis to every
CA in the window and DRD2's predicted ICL3 (147 residues, mean pLDDT 38.5)
bends it by 35.5 degrees.
```

---

## Steric exclusion — the separate verification

The panel's lower-left annotation says the deposited INACTIVE TM6 occupies the
volume the alpha5 helix binds in. That was verified properly rather than
asserted, with two controls and a second receptor, by
`figures/block_a/steric_exclusion.py`.

**Framing.** The quantity is **mutual exclusion of volume**, never a contact
distance. A 0.22 A heavy-atom separation is a clash; reporting it as a contact
invites the obvious objection. The statistic is how many of the alpha5's own
heavy atoms lie within 4.0 A of a deposited-TM6 heavy atom, out of the
peptide's total.

**Atom sets.** A: the alpha5 C-terminal 21 residues of the prediction's partner
chain, all non-hydrogen ATOM records, in the prediction's own frame. B: the TM6
window of the deposited structure, all non-hydrogen ATOM records, moved onto the
prediction by a Kabsch fit over receptor CA in a set that **excludes TM6 and
ICL3** — so the fit is on the invariant scaffold and cannot be accused of having
pushed TM6 into the peptide. All-against-all distances between A and B. Every
deposited structure is verified against both stored reference values first.

```
STERIC EXCLUSION: does the deposited INACTIVE TM6 occupy the alpha5 site?
counts are heavy-atom pairs; 'alpha5 atoms<4' is how many of the peptide's own heavy atoms are buried in the TM6 volume

=== DRD2 · row 8285 · OpenFold-3 · cognate
    alpha5 B 334-354 : 166 heavy atoms
    CONTROL  own predicted TM6 366-398           pairs<4     6  <3    1   alpha5 atoms<4   3/166   closest 2.85 A  (Ala371 CA – Leu353 O)
    6CM4   inactive TM6 366-398  fit 223 CA 2.57 A   pairs<4   631  <3  295   alpha5 atoms<4  86/166   closest 0.22 A  (Glu368 CA – Leu348 N)
    7JVR   active   TM6 366-398  fit 228 CA 1.04 A   pairs<4    88  <3   38   alpha5 atoms<4  18/166   closest 0.44 A  (Lys367 CB – Phe354 CE2)

=== ACM1 · row 948 · Chai-1 · cognate
    alpha5 B 339-359 : 172 heavy atoms
    CONTROL  own predicted TM6 358-390           pairs<4    18  <3    2   alpha5 atoms<4   7/172   closest 2.74 A  (Ala363 CA – Leu358 O)
    6ZFZ   inactive TM6 358-390  fit 247 CA 2.07 A   pairs<4   463  <3  204   alpha5 atoms<4  67/172   closest 0.79 A  (Ala362 CB – Asn357 N)

Read: the quantity is MUTUAL EXCLUSION OF VOLUME, not a contact distance. What the
numbers support is an ordering - the deposited INACTIVE TM6 buries roughly half
the alpha5's heavy atoms, the deposited ACTIVE one about a fifth of that, and the
model's own TM6 almost none. The active control is not zero and must not be reported
as though it were.
```

### What it shows, and what it does not

| | alpha5 heavy atoms within 4 A of that TM6 |
|---|---|
| DRD2 vs **6CM4, deposited inactive** | **86 of 166 (52%)** |
| DRD2 vs 7JVR, deposited active | 18 of 166 (11%) |
| DRD2 vs the prediction's own TM6 | 3 of 166 (2%) |
| ACM1 (row 948, Chai-1) vs **6ZFZ, deposited inactive** | **67 of 172 (39%)** |
| ACM1 vs the prediction's own TM6 | 7 of 172 (4%) |

The ordering — inactive >> active > self — holds on both receptors that have a
deposited inactive reference and a cognate prediction in this drop. **The
active control is not zero and must not be reported as though it were**: 11%
of the peptide's atoms are still within 4 A of 7JVR's TM6, on a 1.04 A fit,
partly fit residual and partly a real difference between where this model puts
the alpha5 and where 7JVR's own Ga sits.

**Limits.** n = 2 receptors, because only two of the four shipped prediction
CIFs are cognate-arm predictions of a receptor that also has a deposited
inactive panel reference. AA2AR's shipped prediction is apo and has no partner
chain to test. The ACM1 Protenix row (967) was not used: its cell is the E1
broken cell (mean pLDDT below 50). A general claim needs the exclusion computed
across the panel from coordinates the drop does not contain — that is an import
request, not something to work around here.

**If it generalises**, the sentence it supports is a mechanism sentence, and it
should be phrased as exclusion of volume: *the transducer's alpha5 helix and
the inactive TM6 position occupy the same space, so the partner cannot be
accommodated unless TM6 moves; supplying it selects the only geometry that
admits it.* Never as a contact distance.

---

## Notes for whoever inherits this

* The panel refuses the cytoplasmic view. Its projection foreshortens the two
  measured segments by different amounts (89.9% and 79.0% of their true
  lengths), which would show a ratio the data does not have. The side view
  draws both at 100.0% and 100.0%. That check lives in `render()` and no
  render in the 232-row corpus survey does it.
* Tubes and traces are the CA path smoothed with a 4-residue running mean (the
  helix axis). Two superposed CA coils 6 A apart read as a tangle. **Nothing
  measured passes through the smoothing.**
* `--view cytoplasmic` is kept only so the refusal is demonstrable.
* Downloads: `figures/structures/6CM4.cif`, `figures/structures/6ZFZ.cif`.
  Neither is in git (the directory is excluded); both are verified against
  `reference_predicates.csv` at load time, so a wrong or corrupted download
  fails loudly rather than being drawn.
