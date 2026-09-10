# FIGURES.md — the figure ledger

One entry per figure. **DURABLE** — it survives a data refresh, the images do not.
An entry exists *before* an image does. A panel with no entry is not a figure.

Fields, and that is all of them:

```
claim   which CLAIMS.md claim this defends, or `none` for a design/coverage panel
shows   one line, what a reader takes away
data    the columns and file, plus the [R-*] ids for every number shown
build   the exact command that makes it
status  draft | ready | blocked on <what>
```

Renders carry their provenance in `scenes/<name>.prov.json`, not here — which
prediction, out of how many, and why that one. Do not duplicate it.

---

## Superseded

F1-F5 described panels built on an earlier data export that was a different
campaign and was deleted on 2026-09-10. The entries are removed rather than
kept: a ledger entry pointing at data that no longer exists is worse than no
entry. Git history holds them.


## Block A

Panels built from `data/block_a/`, the self-contained Block A drop. Their
per-panel provenance — source file, exact filter, n after filtering, claim —
is in `block_a/FIGURE_PROVENANCE.md`, which is the companion to these entries
and carries the material a caption needs. The scripts are in
`block_a/panels/`; the shared loader and the exclusion filters are in
`block_a/badata.py`.

**The render rule for every Block A entry, added 2026-09-10.** Structure
renders are built in matplotlib by `figures/dofrender.py` and
`block_a/panels/dofscenes.py`, not PyMOL, and they draw themselves into their
composite — there is no separate render step and no bitmap to place. Three
things are non-negotiable in them and are enforced in code, not by care:

1. **Every measured distance carries its value AND the atom pair, on the
   panel.** `dofrender.measured_distance` will not draw a line without both.
   Not one of the 232 render rows in the corpus survey does this.
2. **Grey means "not the subject".** The invariant bundle is a grey density;
   colour is TM6 and the α5 21-mer only. Never grey-because-reference.
3. **The soft focus encodes DEPTH ONLY and every caption must say so.** A
   corpus check found no paper in the 78 using the technique, so it gets no
   benefit of the doubt, and this literature de-emphasises by subject rather
   than by depth. The focal plane is placed behind every state-defining
   element (`dofrender.focal_plane`) and `focus_report` raises if any of them
   would fall on the blurred side; where two measures cannot share one focal
   plane, use two views rather than blurring one of them.

`hero_renders.py`'s PyMOL targets for GA-1, BA-8 and BA-1a are superseded; S10
still uses them.

**The filter rule for every Block A entry.** `excl_any` fires on 5,093 of
9,490 rows (54%) and is the wrong filter almost everywhere: the five flags are
independent sets with different scopes. E1 (25 rows) and E2 (4) are always
excluded and keep 99.7% of the corpus. E3 is applied only where a reference
value is a denominator or a regression predictor, and then through the
per-axis flags `excl_E3_npxxy` / `excl_E3_tilt`, never the union. E4 is for
Class-A-scoped claims; E5 is a sensitivity contrast. Every caption states its
filter and its n.

`fraction_of_way_to_active` is a Table T2 quantity and appears in no figure.

### BA-1 — the instrument and its calibration
```
claim   the predicate is a rule over two distances, and it behaves on
        structures whose state is already known
shows   a: 3SN6 over 2RH1, TM-bundle superposition, the two predicate axes
        drawn; b: all 168 references on the predicate plane with both
        thresholds, the 98 with no NPxxY axis as a rug, and all 9 deviations
        named and shaped by all five deviation_class levels; c: the reference
        gap per receptor, tilt SD 2.07 A against NPxxY SD 5.22 A; d: the
        predicate call census over 168
data    02_references/{reference_predicates,reference_metadata,
        reference_separation}.csv; 11_structures/instrument_schematic/
        (no [R-*] ids: Block A ships its own tidy tables, not RESULTS.md)
build   python3 block_a/panels/ba1_reference_landscape.py   (b, c, d)
        python3 block_a/panels/ba1a_instrument.py            (BA-1a, own figure)
status  ready — BA-1a was REBUILT on 2026-09-09 and REBUILT AGAIN on
        2026-09-10 as its own figure with the quantitative panel it was
        missing. It is 4LDE (ADRB2's panel ACTIVE reference) over 2RH1 (its
        inactive one) on TWO views: a side view carrying the NPxxY
        measurement and a cytoplasmic view carrying the TM6 tilt, one measure
        per view because the two do not lie in one plane and an end-on
        distance is a dot. All four values are sourced from
        reference_predicates.csv and reproduce from the deposited
        coordinates: 4LDE 17.5625 / 4.8131, 2RH1 11.9283 / 11.4727, each drawn
        WITH the atom pair. Panels c and d put both references on the axis
        distribution of all 167 / 70 references that carry each axis, so the
        render is not a hand-picked pair standing alone. The 2026-09-09
        version was two loose PNGs with no quantitative panel; the version
        before that was 3SN6 over 2RH1 with no numbers drawn, and 3SN6 is not
        in the reference set at all. Tilt anchors are L75/L275, not the
        L124/F282 instrument_schematic/ALIGNMENT.md names. The renders are
        matplotlib depth-of-field, not PyMOL: THE CAPTION MUST SAY THE BLUR
        ENCODES DEPTH ONLY
```

### BA-2 — the main effect
```
claim   C6, C7 — SC-1
shows   TM6 tilt opens under the cognate Ga co-input on all four backbones and
        does not under apo; within receptor as well as pooled; and the
        headline shift with its CLUSTER-bootstrap interval
data    01_rows/block_a_rows.csv (E1+E2, n=9,461); receptor_summary.csv;
        headline_by_backbone.csv *_cluster_ci_* columns only
build   python3 block_a/panels/ba2_arm_shift.py
status  ready — CIs are the cluster columns, not the receptor columns the
        claim sheet mislabels as cluster (D5); effective n is 47 receptors,
        not the 48 that n_receptors_tilt records
```

### BA-3 — the orthogonal signature
```
claim   C6 — SC-3, state-reached half
shows   predictions the predicate calls active sit where active references sit
        on the P5.50-F6.44 connector, a coordinate never used to call anything:
        204/256 and 205/256 row-level agreement. The magnitude difference is
        -0.56 A with a cluster interval of [-1.196, +0.026], which INCLUDES
        ZERO, and zero is drawn
data    05_connector/*.csv, n=512 (the T2 scale-up; excl_* does not apply)
build   python3 block_a/panels/ba3_connector.py
status  ready — leads with the agreement counts. No magnitude ratio is
        plotted: the ratio is taken on the absolute delta, so its interval
        cannot cross zero by construction (D2)
```

### BA-4 — amplitude, the negative result
```
claim   C6 — SC-3, amplitude half; C-10
shows   whether a receptor with further to travel travels further. Unity on
        every regression panel and marked on every forest, because the null
        under test is slope=1. Protenix on NPxxY is +0.257 [0.074, 0.552] and
        does NOT cross zero; tilt slopes go negative (Boltz -0.298, Chai
        -0.659); tilt SD(predictor) is 1.17 A against NPxxY's 5.22 A
data    04_amplitude/{amplitude_points,amplitude_fits,
        attenuation_sensitivity}.csv, inclusion set class_a_only,
        n=28 receptors (NPxxY) / 32 (tilt)
build   python3 block_a/panels/ba4_amplitude.py
status  ready — do not write "all CIs cross zero" (D1); do not quote a
        positive tilt slope range (D3); the tilt axis is uninformative for
        amplitude, which is an instrument property, not a result
```

### BA-5 — confidence does not track state
```
claim   C8 — SC-11 as restated by W-2
shows   pLDDT against RMSD-to-active for all three aggregations and four
        backbones, cluster CIs, zero drawn. Signed on the primary aggregation
        for 2 of 4 backbones. The aggregation choice moves the answer: OF3
        -0.258 -> -0.626, Protenix +0.327 -> +0.068. Panel e is the most
        confident AA2AR apo model over the active reference
data    06_confidence/{plddt_correlations,plddt_per_receptor}.csv;
        01_rows/block_a_rows.csv restricted to Class A rows carrying an active
        reference, n=1,595-1,600 per backbone over 32 receptors
build   python3 block_a/panels/ba5_confidence.py
        + the render_struct.py command in block_a/FIGURE_PROVENANCE.md
status  ready — the caption MUST say plddt_at_anchors was designated primary
        post hoc. plddt_correlations.csv records n_receptors=40; the
        population has 32 and the panels quote 32. Panel e must not be
        captioned "confidently wrong": that row is 0.95 A from the INACTIVE
        reference, which is where an apo prediction belongs
```

### S1-S9 — supplementary
```
claim   none individually; together they are the audit trail BA-1 to BA-5 rest
        on, and S8 is the required quantitative panel behind the BA-5e render
shows   S1 what each exclusion flag covers and what every combination does to
        every headline metric (no sign flip in 160 cells) · S2 the reference
        set audit, including three columns that are empty in the drop ·
        S3 cluster against receptor bootstrap, the only place receptor
        intervals appear · S4 every receptor x backbone, absent cells drawn
        absent · S5 the amplitude slopes under all three inclusion sets ·
        S6 predicate calibration with the untestable rows counted separately ·
        S7 the paralog clustering and the holdout · S8 the AA2AR case ·
        S9 fold integrity, one axis per class
data    01_rows/, 02_references/, 03_aggregates/, 04_amplitude/,
        06_confidence/, 07_clusters_and_holdout/, 08_exclusions/
build   python3 block_a/panels/s{1..9}_*.py
status  ready
```

### F1 — the workflow (Figure 1)
```
claim   none directly — it establishes the instrument and the population every
        later figure depends on. Venue norm: Figure 1 is a pipeline schematic
        in 4 of 4 of the corpus's Nature Communications papers, and this figure
        set had no schematic at all
shows   a the two predicates and the ATOM PAIRS they are measured between,
        named once for the whole paper, with both thresholds; b the 167
        deposited references scored on those two axes, 69 with both axes and
        98 rugged; c the design, 48 receptors x 2 arms x 4 backbones x 25
        seeds = 384 nominal cells, 380 run, 9,490 rows of a nominal 9,600, and
        what is and is not recorded about how they were run; d where the 9,490
        rows go — E1 25, E2 4, 9,461 scored, Class A 7,966 / B 795 / F 700,
        predicate active 4,863 / inactive 4,598
data    01_rows/block_a_rows.csv (all 9,490, unfiltered — the figure is about
        where they go); 02_references/reference_predicates.csv (all 168, 167
        with a tilt value)
build   python3 block_a/panels/f1_workflow.py
status  ready — it must imply NOTHING about magnitude, and it carries no arrow
        that is labelled with anything. Panel c says templates-off is SC-9's
        claim from launcher static analysis and a propagation test with NO
        row-level echo, and that no MSA setting appears in the drop at all;
        neither may be upgraded to a plain assertion
```

### GA-1 — the graphical abstract: one co-input, one state change
```
claim   C6, C7 — SC-1, in one image
shows   ONE left-to-right composition, not a lettered grid: a receptor
        predicted from sequence alone with TM6 closed; the cognate Ga
        co-input arriving, drawn as its alpha5 C-terminal 21-mer in the
        intracellular cavity; the same models with the partner and TM6 open.
        The SAME atom pair is measured on left and right and both values are
        printed, so the reader subtracts them by eye. Beneath, one thin
        full-width strip: every Class A prediction on that one axis, apo
        against cognate, with both rendered rows marked
data    left  AA2AR/boltz/apo row 567, tilt 11.7347 A (Leu48 2x46 Ca -
              Leu235 6x37 Ca), verified from the CIF
        centre, right  DRD2/of3/cognate row 8285, tilt 17.2766 A (Leu76 -
              Leu375), same BW pair, verified from the CIF
        strip 01_rows/block_a_rows.csv, core (E1+E2), Class A: 3,992 apo and
              3,974 cognate rows of 9,490, smoothed on the tilt axis;
              predicate threshold 14.932 A drawn
build   python3 block_a/panels/ga1_hero.py       (renders AND composition)
status  ready — REDESIGNED 2026-09-10. It was five lettered panels with
        sub-captions, which is figure grammar: a graphical abstract is one
        image carrying one idea, legible at thumbnail size, and the two
        explicit graphical abstracts in the corpus are both single
        left-to-right compositions. There are now NO PANEL LETTERS anywhere.
        Built at 130 x 76 mm so the load-bearing type survives reduction to
        the 80 mm a TOC entry gets.

        NO ARROW anywhere, and no "=" either. An arrow labelled "activation"
        is the field's characteristic failure on this exact claim and an
        unlabelled one reads as magnitude, which is BA-4 and is negative on
        three of four backbones; an "=" would be literally false because left
        and right are different receptors. A green "+" between the receptor
        and the thing added to it carries the addition and asserts no
        direction of change.

        LEFT AND RIGHT ARE DIFFERENT RECEPTORS and the figure says so in
        frame. 11_structures/ ships four prediction CIFs — one apo (AA2AR)
        and three cognate (DRD2 and the two ACM1 broken/healthy rows) — so no
        receptor has both arms. Checked again during the redesign. The strip,
        not the two renders, is the within-condition contrast.

        THE CAPTION IS LOAD-BEARING. Selection rules, cell sizes and
        percentiles were deliberately taken OUT of the frame and MUST go into
        the LaTeX caption. `ga1_hero.py:caption_block()` prints the exact
        required text and it is reproduced in FIGURE_PROVENANCE.md. It
        includes: both selection rules and percentiles, that the archive
        ships one prediction per case, that Block A's cognate arm supplies
        the FULL cognate Ga and only the alpha5 21-mer is drawn, that the
        soft focus encodes depth only, and that the figure does NOT show
        amplitude reproduction. No fraction_of_way_to_active anywhere.
```

### BA-6 — the predicate plane, for the predictions
```
claim   C6, C7 — the two-axis form of SC-1
shows   the predicate is a rule over two coordinates, and the co-input moves
        the panel across BOTH at once. apo and cognate as two clouds on the
        same plane the 69 Class A references anchor; the same axis limits and
        the same colour rule on every facet; the quadrant census underneath,
        which is where the two axes are shown to agree
data    01_rows/block_a_rows.csv, core (E1+E2) + Class A. n = 7,166 rows with
        both axes (3,592 apo / 3,574 cognate), 800 with no NPxxY drawn as a
        rug. 02_references/reference_predicates.csv, 69 Class A references
        with both axes (30 active / 39 inactive). Thresholds 9.082 / 14.932
build   python3 block_a/panels/ba6_state_plane.py
status  ready — BA-1b is the reference-only version of this plane; BA-6 is the
        prediction version and the two must keep the same axes and thresholds.
        Quadrant census apo 2,611 neither / 318 NPxxY-only / 86 tilt-only /
        577 both; cognate 157 / 23 / 232 / 3,162
```

### BA-7 — a switch, not a dial
```
claim   C6, C7 — the seed-level form. Also bounds C8's seed-variance story
shows   within a receptor x backbone cell the 25 seeds almost always agree:
        111 of 160 apo cells never fire the predicate and 108 of 159 cognate
        cells fire on every seed. The co-input flips a switch rather than
        turning a dial, and the graded minority (39 apo / 24 cognate cells) is
        drawn rather than averaged away
data    01_rows/block_a_rows.csv, core (E1+E2) + Class A. 319 cells, 314 of
        them 25 seeds, 4 at 24 and 1 at 20; 159 receptor x backbone pairs with
        both arms. 120 cells up, 37 unchanged, 2 down (LPAR1/OF3 0.88->0.80,
        LT4R1/OF3 0.04->0.00)
build   python3 block_a/panels/ba7_switch_not_dial.py
status  ready — histogram over a fixed seed budget on a SHARED vertical scale
        with n stated (the corpus's one clean version of this panel is
        sun2026kinconfbench 2C). Never a bar with an SEM over a bimodal cell
        distribution: purnomo2026cafe 2A does that against its own thesis
```

### BA-8 — the alpha5 in the intracellular cavity
```
claim   C6 — the structural companion to BA-6, and it may not appear without it
shows   the cognate Ga alpha5 C-terminal helix seated in the DRD2 intracellular
        cavity, with the four state-defining anchors labelled and the two
        predicate distances drawn. The anchor identities are the point: the
        predicate is a rule over these four atoms and nothing else
data    DRD2/of3/cognate row 8285. Anchors L76 (2x46) / L375 (6x37) CA and
        Y209 (5.58) / Y426 (7.53) OH, each VERIFIED by reproducing the row's
        stored d_gpcrdb_tm6_tilt_246_637_ca = 17.2766 A and d_npxxy_oh =
        3.9883 A from the CIF to 1e-3 A
build   python3 block_a/panels/ba8_alpha5.py     (render AND composite)
status  ready — the render is panel a and the cell it came from is panels b and
        c of the SAME figure, all 25 seeds on both predicate axes with row 8285
        ringed, so the render cannot be separated from its population. BA-6 is
        the panel-wide version. REBUILT 2026-09-10 in matplotlib depth of
        field: a SIDE view cropped to the intracellular half (the cytoplasmic
        view showed the cavity mouth end-on, which is a uniform disc) and a
        heavy-atom density rather than a PyMOL surface (a semi-transparent
        surface renders both walls at once and fills the cavity in). Three
        measured distances, each with its atom pair: 17.28, 3.99, and the
        R3.50 contact at 3.16 A - Arg132 NH2 to Cys351 O, the closest
        heavy-atom contact to the alpha5 21-mer in THIS model. Caption MUST
        state that the blur encodes depth only
```

### S10 — what E1 removes
```
claim   none — it is the picture behind S1a's E1 = 25 rows
shows   the broken ACM1/cognate/Protenix cell beside the healthy
        ACM1/cognate/Chai comparator, one camera, same grey, the measured
        distance printed under each. The A1-A6 scorer gates carry no pLDDT
        floor (C-12), so these rows pass every identity check and are removed
        by E1 alone
data    row 967 (median plddt_mean in its 25-row cell, 38.38, tilt 21.547,
        NPxxY-OH 26.632) and row 948 (highest plddt_mean in its 25-row cell,
        69.23, tilt 17.166, NPxxY-OH 4.016)
build   python3 block_a/panels/hero_renders.py s10
        python3 block_a/panels/s10_broken_cell.py
status  ready — panel c is the quantitative half and is in the same figure:
        both cells' pLDDT distributions with the E1 rule drawn and both
        rendered rows ringed. All 25 E1 rows carry passed=True (C-12)
```


## Figure order, decided

```
Fig 1   F1    the workflow — the predicate, its atom pairs, the references,
              the design, and where every row goes
Fig 2   BA-7  a switch, not a dial
Fig 3   BA-4  amplitude — the negative result
Fig 4   BA-5  confidence does not track state
GA-1          the graphical abstract, outside the numbering
```

BA-7 is deliberately NOT Figure 1. A bimodality claim placed before the
predicate is established invites a reader to doubt the predicate rather than
accept the bimodality, and it only reframes the amplitude null as a property of
the mechanism if the instrument is already credible. BA-2, BA-3, BA-6 and BA-8
follow the four numbered figures or move to supplementary as space allows.

## Corpus figures

Figures whose data is the **literature corpus**, not our predictions. Every number
comes from `lit/notes/*.md` and `lit/INDEX.md` via two scripts that live here:

```
python3 mine_corpus.py       # notes  -> data_lit/papers.csv, figrows.csv, metrics.csv
python3 classify_corpus.py   # those  -> data_lit/tags.csv, metric_kinds.csv,
                             #           oracle_routes.csv, antimem.csv, figdefects.csv
```

`data_lit/*.csv` is the citable artefact and carries, for every classified row, the
note text the rule fired on. These figures do **not** touch any results block,
so a new block does not stale them; what stales them is a change
to `lit/`. Re-run both scripts after any corpus edit.

`data_lit/oracle_routes.csv` is produced but **no figure uses it** — see the note at
the bottom of this section.

### LF1 — how prior work decides which state it got
```
claim   C5 — the corpus-wide form of "supplies the partner and never verifies state"
shows   the field has no shared way to call a conformational state: 36/78 papers use
        a continuous coordinate, 36/78 RMSD-to-reference, 35/78 a binary predicate,
        18/78 call it by eye, and 20/78 operationalise no state metric at all; 52 of
        the 58 that do call a state use two or more kinds at once
data    `state_metric` from all 78 notes -> data_lit/metric_kinds.csv (no [R-*] ids;
        no number here comes from our predictions)
build   python3 panels/lit1_state_metrics.py   -> out/lit1_state_metrics.{pdf,png}
status  ready — every assignment carries the note text it was read from, in the
        `window` column of metric_kinds.csv
```

### LF2 — leakage, and what is done about it
```
claim   C4 — the state, or the expected answer, is supplied rather than induced
shows   the nine SCHEMA.md rigour tags across all 78 papers, one column per paper:
        58/78 carry design-level oracle use (route 7), 42/78 pipeline leakage
        (routes 1-6), only 14 carry neither, and 10 of the 42 leaking papers are
        nevertheless tagged prospective
data    the `tags:` line of lit/INDEX.md, all 78 papers -> data_lit/tags.csv
build   python3 panels/lit2_rigour_landscape.py -> out/lit2_rigour_landscape.{pdf,png}
status  ready — but read the caveat under LF5 about INDEX.md before quoting a cell
```

### LF3 — a held-out set is not a control arm
```
claim   none — rigour landscape; supports the "wins only near training distribution"
        threat in CLAIMS.md rather than a numbered claim
shows   `anti_memorization_design` against `anti_memorization_control` for all 78
        papers. 37 have a held-out or post-cutoff set; only 21 of those ran and
        analysed a control arm on it. 29 of 78 ran none at all. The v3 schema split
        these two fields precisely to make this cell visible, and this is that cell
data    both anti_memorization fields from all 78 notes -> data_lit/antimem.csv
build   python3 panels/lit3_antimemorization.py -> out/lit3_antimemorization.{pdf,png}
status  ready — classification is from each field's opening verdict; antimem.csv
        carries the verdict text beside every label
```

### LF4 — the corpus's own figure-defect landscape
```
claim   none — this is the evidence base for the refusal rules in figpanels.py
shows   957 of 1,226 panel-group rows carry a recorded defect; 186/232 renders,
        644/739 plots, 76/85 matrices. The recurring named defects are n or counts
        absent (241), a broken or truncated axis (139), no dispersion/CI/test (131)
        and a claim with no quantitative panel (121). The median paper has a defect
        on 85% of its own panel groups, so this is the field, not a few papers
data    the `## F. Figures` table of all 78 notes -> data_lit/figdefects.csv
build   python3 panels/lit4_figure_defects.py  -> out/lit4_figure_defects.{pdf,png}
status  ready — but note 957, not the 968 in README.md. README's count treated three
        `*(blank — reason)*` cells as defects; the rule here does not. Fix README
        when someone touches it; do not quote 968.
```

### LF5 — which handle drives the state, and in which system
```
claim   C4 — and it is the sharpest panel for it
shows   state handles split into operator-supplied (state-annotated input, biased
        template, state-filtered MSA, MSA subsampling/clustering, latent steering,
        seed budget) and biological co-input (ligand, protein partner, G-protein
        mimetic, peptide, nanobody, apo), against the system studied. Of 31 GPCR
        papers, 3 use a peptide as the handle and 2 a G-protein mimetic; 8 supply a
        state-annotated input and 6 a state-biased template
data    Method / Protocol / Control / System tags, all 78 papers -> data_lit/tags.csv
build   python3 panels/lit5_control_handles.py -> out/lit5_control_handles.{pdf,png}
status  ready — tags overlap, so cells do not sum to 78; the panel says so

        CAVEAT for LF2 and LF5. INDEX.md says of itself "This file is lossy by
        design. Never answer a manuscript-bound question from it." That warning is
        about thresholds, n and quotes, which the index compresses away; the `tags:`
        line is the one field the index exists to serve ("the reverse-lookup
        mechanism"), and a landscape count is a reverse lookup. Still: before a
        specific paper's cell goes into a sentence, open its note. The notes carry
        no consolidated tags line of their own — they argue tagging decisions in
        prose — so INDEX.md is the only mechanical source, and that is a corpus
        property worth telling the lit agent about.
```

**Why there is no per-route oracle-leakage figure.** The seven `oracle_leakage`
routes are the obvious matrix to draw and it is not drawable from the index: the
`oracle:` line names the routes that fire and only sometimes the complement, so a
mechanical parse leaves 265 of 546 route cells (48%) with no recorded verdict.
`data_lit/oracle_routes.csv` holds that partial parse with an explicit `unclassified`
level. The per-route detail is in each note's `oracle_leakage` field, in prose, and
would need a per-note extraction pass to become a figure. LF2 is the complete-data
substitute.

## Block B

Panels built from `data/block_b/` and `data/block_b_structures/`. The loader is
`figures/block_b/badata.py`, and **every Block B panel must load through it**.

**Two rules specific to this block, both from failures already recorded in
`analysis/block_b/DISCREPANCY_REPORT.md`:**

1. **Never write `excl_E_B_n` in a panel script.** The claim sheet mislabels
   three of the four exclusion flags — its header says E-B-2 is AA2AR when the
   shipped flag is OPRD+CNR1, and E-B-3 is the 15 non-native when the shipped
   flag is AA2AR alone. `badata.exclude()` takes sets by MEANING
   (`npxxy_undefined`, `agonist_only_ref`, `aa2ar_anomaly`, `non_native_ref`)
   and there is no way to ask it for an E-B-n.
2. **Recompute, then check against the shipped table before drawing.** BB-1's
   guard fired on its first run and exposed D-B-3: the shipped aggregates used
   the untruncated NPxxY threshold 9.082 while every row carries 9.08, which
   differs on five rows of 32,000 and moves AA2AR/chai/decoy from 0.90 to 0.88.

### BB-1 — the four-arm ladder
```
claim   SC-B-1 — the ladder is monotonic across apo < decoy < shuffled < cognate
shows   the two-instrument active-call fraction on all four arms, four
        backbones drawn individually and the panel drawn bold with
        cluster-bootstrap intervals; a logit companion beside it because the
        probability scale saturates at cognate
data    01_rows/rows_tidy.csv recomputed per row, cross-checked against
        04_ladder/ladder_four_scorings.csv on all 20 cells; frame_36, n=36
        receptors, 24 paralog clusters
build   cd figures/block_b/panels && python3 bb1_ladder.py
status  ready — DEPARTS FROM ITS SPEC IN ONE PLACE, deliberately. The spec says
        to draw 0.158 / 0.552 / 0.810 / 0.892 as reference dashes; those are the
        SUPERSEDED values the drop's own README retires, and the spec
        contradicts itself two paragraphs later. The dashes are not drawn and
        the panel says so in red.
```
