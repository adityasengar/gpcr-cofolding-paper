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
status  BLOCKED on a restatement, 2026-09-10 — DO NOT DRAW THIS PANEL YET.
        The correlations it plots POOL the apo and cognate arms while scoring
        every row against the ACTIVE reference, which is the wrong target for
        an apo row, and the two arms differ in both variables at once. The
        "2 of 4 backbones" above is an artefact of that pooling. Conditioned on
        arm: cognate -0.30 / -0.43 / -0.42 / -0.16, all four negative and
        consistent, OF3 NOT an outlier; apo +0.04 / +0.01 / -0.37 / +0.10. The
        direction of the claim survives and its per-backbone shape does not.
        Found by an independent re-verification, recomputed here, and left as a
        [PI] in results.tex because choosing the new headline is Aditya's.
        Still true when it is redrawn: the caption MUST say plddt_at_anchors
        was designated primary post hoc; plddt_correlations.csv records
        n_receptors=40 where the population has 32 and the panels quote 32; and
        panel e must not be captioned "confidently wrong", because that row is
        0.95 A from the INACTIVE reference, which is where an apo prediction
        belongs
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
        REVISED 2026-09-11: panel headings sentence-cased; the census line
        broken over two lines because it overran its box; constrained_layout
        replaced with explicit gridspec geometry (it reported "at least one
        axes collapsed" on EVERY hspace including the shipped one, so the pads
        were a no-op and b's x-label ran into d's heading); and panel c now
        says this is THE FIRST OF FOUR CAMPAIGNS. That label is on c, not on
        the figure title, because a and b are the instrument and its
        calibration and are shared by all four. No number changed
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

### BB-12 — the ladder AND its decomposition (MAIN-TEXT FIGURE 3)
```
claim   SC-B-1 and its decomposition, restated
shows   a: the four-arm ladder, four backbones plus panel with cluster-boot
        CIs, with the two clean steps bracketed in a band below the data;
        b: the same fractions on the logit scale; c: what each contrast
        actually varies, including the shipped one, named CONFOUNDED
data    01_rows/rows_tidy.csv (per-backbone rates, predicate recomputed per
        row) AND 04_ladder/ladder_per_receptor.csv (decomposition terms).
        Checked against 04_ladder/ladder_four_scorings.csv and
        05_decomposition/ladder_decomposition.csv
build   python3 block_b/panels/bb12_ladder_decomposition.py
status  ready — MERGED FROM BB-1 AND BB-2 on 2026-09-11, Aditya's call. They
        drew the SAME LADDER TWICE: BB-2's left panel was titled "the ladder,
        and the two steps that telescope" and redrew the four rungs BB-1 had
        already drawn, 45 lines earlier in the prose.
        THE MERGE REMOVES THE DUPLICATION RATHER THAN CARRYING IT INSIDE ONE
        FLOAT. A 2x2 of BB-1's two panels beside BB-2's two would have put two
        ladders in one figure. The ladder is drawn ONCE and the steps are
        bracketed on it.
        ONE THING WAS DROPPED IN THE MERGE AND IT WAS RIGHT TO DROP IT. BB-2
        drew the panel line apo->decoy->cognate with a grey dashed detour
        through shuffled. That geometry cannot survive: BB-1's ladder runs
        THROUGH all four arms, so the "route not taken" lies exactly under the
        panel line and is invisible while the legend claims it is drawn — the
        same defect class as a check that never runs. The legend entry went
        with it; panel c carries the argument in words instead.
        TWO ROUTES, CHECKED AGAINST EACH OTHER. The rates and the terms come
        from different files. The script asserts they agree on all four rungs
        (max gap 1.4e-4) before drawing one ladder that claims to be both, and
        refuses rather than picking a winner.
        Both original guards kept. U+2192 is MISSING FROM THE HOUSE FONT and
        renders as a blank box — use "->" in fig.text, mathtext in labels
```

### BB-1 — the four-arm ladder (SI; superseded in the main text by BB-12)
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

### BB-2 — the decomposition, on both scales (SUPERSEDED by BB-12, and now
### placed NOWHERE: si.tex never carried it. Still renders; do not delete)
```
claim   SC-B-2 — occupancy 55%, α5-CT sequence 34%, correct family 11% on the
        probability scale and 17.4% on the logit scale
shows   a, the three telescoping terms as shares, probability beside logit, so
        the reader sees that only the family share moves between them;
        b, the per-backbone family term as SHIPPED against as CLAIMED
data    05_decomposition/ladder_decomposition.csv, frame reproduction_36
build   cd figures/block_b/panels && python3 bb2_decomposition.py
status  ready — panel b exists BECAUSE the claim does not reproduce. SC-B-2 says
        "all four backbones agree, 17-21%"; the file says 14.2 / 22.9 / 23.6 /
        10.9. The claimed values are drawn as dashes over the real bars rather
        than quietly replaced. Three of four intervals span zero (D-B-6, D-B-7)
```

### BB-7 — the per-backbone family term (SI)
```
claim   SC-B-2's per-backbone half, which reproduces nowhere
shows   the four per-backbone family terms plus the panel estimate, logit
        scale, zero marked. Signed on OpenFold-3 alone: +0.939
        [+0.459, +1.631]. Boltz +0.586 [-0.074, +1.595], Chai +0.519
        [-0.235, +1.523], Protenix +0.674 [-0.047, +5.148]. Panel +0.656
        [+0.389, +1.094], signed only because pooling narrows it
data    05_decomposition/ladder_decomposition.csv, frame reproduction_36
build   python3 block_b/panels/bb7_family_term.py
status  ready — BUILT BY THE LIT SESSION 2026-09-11 to close an orphan. The
        prose had this result and NO figure carried it: BB-2's ledger entry
        promised a per-backbone panel, the 2026-09-10 rebuild replaced the
        figure entirely, and the entry was never updated. The claim was in
        the paper with nothing behind it for a day.
        WHAT IT CAUGHT, verified independently by the orchestrator. The claim
        sheet reads "Per-backbone logit family share (all four backbones
        agree, 17-21%): boltz 17.4%, chai 17.5%, of3 20.9%, protenix 17.5%".
        Shipped: 14.2 / 22.9 / 23.6 / 10.9. THREE OF THE FOUR CLAIMED VALUES
        MATCH NOTHING IN THE FILE on either scale or either frame. The fourth,
        boltz 17.4%, matches exactly one row -- `reproduction_36 / panel /
        logit`, the POOLED estimate. Boltz is never 17.4% anywhere. That the
        panel value was copied into the boltz slot is the obvious reading and
        is an INFERENCE, not established; what is established is that one
        entry of a four-value per-backbone list is the pooled number.
        Protenix's upper bound of 5.15 flattens the others, so the VIEW is
        clipped at 2.0 and the clip is annotated. No interval is truncated.
        DOES NOT PRE-EMPT SC-B-2, which is Aditya's decision: the panel shows
        what the data says, the decision is about what the paper claims
```

### BB-3 — engagement and activation are separable
```
claim   SC-B-3 — and the engaged-but-inactive decoy cell, which is the only cell
        in Block B that can support a chemistry claim
shows   a, the three partner arms on the engagement × activation plane;
        b, the full cutoff sweep, because 20 Å is a choice and the decoy arm
        moves 0.53 → 0.66 across it while cognate barely moves;
        c, the mechanism cell populated on every backbone, 278–540
data    06_interface/interface_2x2.csv, frame_36, two_instrument, all 6 cutoffs
build   cd figures/block_b/panels && python3 bb3_engagement.py
status  ready — apo is absent from a and b BY CONSTRUCTION, not omission: with
        no partner, p(engaged)=0 and p(active|engaged) is undefined. Said on the
        panel rather than left as a gap a reader has to explain to themselves
```

### BB-4 — the PIF connector
```
claim   SC-B-4 — decoy cells engaged but not active sit at apo geometry on an
        axis the predicate never reads
shows   a, five subsets as distributions with every cell drawn;
        b, the per-backbone companion
data    06_interface/interface_pif_connector.csv, 640 cells
build   cd figures/block_b/panels && python3 bb4_connector.py
status  ready — reproduces all five medians and all five cell counts exactly
        (160/130/118/69/47 at 15.35/16.04/16.00/16.03/15.42). NO STRUCTURAL
        RENDER OF THIS EXISTS AND NONE SHOULD: the whole spread is 0.7 Å, which
        cannot be drawn honestly at a legible scale. The addendum forbids it and
        the addendum is right
```

### BB-5 — the models do not read partner family
```
claim   SC-B-6 (Outcome A signed) and SC-B-14 (Outcome B signed nowhere)
shows   a, the three donor strata at their true widths, all receptors against
        native-referenced only, open markers where the interval spans zero;
        b, 0 of 9 stratum × axis combinations sign the pre-registered alternative
data    07_donor_residuals/phase5_power_analysis.csv, panel rows, residual_tilt
build   cd figures/block_b/panels && python3 bb5_residuals.py
status  ready — TWO THINGS IT MUST NOT SAY, and does not: this is not an
        equivalence result (that upgrade was attempted and retracted), and the
        interval supporting the conclusion spans zero, which is drawn rather
        than glossed. One stratum carries it: Gs→Gi at 20 native references,
        against Gs→Gq at 3 and Gi→Gs at none
```

### BB-6 — the ladder, per receptor
```
claim   SC-B-1 at receptor grain
shows   a, every receptor's own ladder under the median; b, the distribution at
        each rung with the ceiling drawn
data    04_ladder/ladder_per_receptor.csv, frame_36, 144 cells over 36 receptors
build   cd figures/block_b/panels && python3 bb6_per_receptor.py
status  ready — the panel a mean is a mean over a population that is pinned at
        the top: 115 of 144 cognate cells sit at or above 0.98. That ceiling is
        the reason the family term differs between scales, and this is the panel
        that shows it rather than asserting it
```

## Block C

Panels built from `data/block_c/`. The loader is `figures/block_c/bcdata.py`, and
**every Block C panel must load through it**.

**The rule specific to this block: state the evidential class on the panel's own
face.** Block C shipped exactly one row-level file (`12_g4_off_site_census`,
40,000 rows). Everything else is a summary JSON. So three of these four panels
draw intervals over a distribution nobody outside the pipeline has seen, and each
says so on itself rather than letting four tidy intervals imply otherwise. The
class per panel is in `analysis/block_c/panels/README.md` and is repeated in each
entry below.

**Three bands, and the middle one is not failure.** In-pocket ≤8 Å,
entrance-bound 8–15 Å, off-site >15 Å. Entrance-bound is 7,349 of 40,000 rows and
is an **adjudicated VALID pose**; counting it as error reports 34.8% where the
truth is 15.1%. `bcdata` carries the thresholds and there is no way to ask it for
a two-band split.

**`ligand_source` is the load-bearing split, not the role name.** `hetatm` vs
`peptide_chain`. In the same apo agonist/antagonist cells they are 1.52% and
66.53% off-site, because peptide receptors bind at the extracellular vestibule.
Filtering small-molecule rows by role name silently pools them — that is D-C-4,
and it caught me on my first verification run.

### BC-1 — agonist and antagonist pockets separate, in the apo arm alone
```
claim   SC-C-1 — ligand class is written into pocket geometry, and the partner
        erases it
shows   the 2x2 of arm (apo, cognate) by ligand role (agonist, antagonist) on
        pocket-Ca RMSD difference, per backbone, with the interaction interval
data    06_2x2_interaction/ + g_scc1_cluster_boot.json, 16 paralog clusters;
        cluster-boot CIs are the authoritative convention (Block A C-8)
build   cd figures/block_c/panels && python3 bc1_pocket_2x2.py
status  ready — SUMMARY PANEL, and it says so on its face. rows.tier3.v2.csv was
        not shipped, so the 23 per-receptor values behind each cell mean do not
        exist here. Do not let four intervals imply a distribution
```

### BC-2 — the pre-registered ordinal test, per receptor
```
claim   SC-C-2 — ligand role ranks against the same continuous axis
shows   a, tau per receptor over 23; b, the same with self-reference excluded,
        n=15. Median tau 0.26-0.39, NOT the 65-87% the claim sheet prints
data    07_ordinal_recovery/s5_p4_ordinal.json — carries a tau per receptor
build   cd figures/block_c/panels && python3 bc2_ordinal.py
status  ready — PER-RECEPTOR PANEL, the only one in this block, and the panel
        that earned the exercise. Plotting the distribution showed violins around
        0.3 against printed panel values of 0.74, which is how D-C-3 was found:
        SC-C-2's table is headed "Kendall's tau" and holds a FRACTION OF
        RECEPTORS. That mislabel had passed the claim sheet, the dispatch and our
        own Results, and it reached the manuscript. Both panel definitions are
        drawn because showing only the more favourable one is the error the pose
        result in this same block already made and corrected
```

### BC-3 — prospective ligand-class discrimination, on two backbones of four
```
claim   SC-C-4 — leave-one-receptor-out classification of ligand class
shows   AUROC per backbone with cluster-boot 95% CI over 12 clusters and the
        permutation null: Boltz 0.852 [0.560, 0.974], Protenix 0.825
        [0.528, 0.960]; Chai 0.706 and OF3 0.656 both span 0.5
data    04_classifier/g1_bootstrap_s1_auroc.json + the S1 LORO JSON
build   cd figures/block_c/panels && python3 bc3_classifier.py
status  ready — SUMMARY PANEL; the per-receptor LORO folds were not shipped.
        THE ONE THING IT MUST NOT DO is let a reader take Chai-1 and OpenFold3 as
        negative. Their intervals span 0.5, which means the test cannot separate
        them from chance — not that they carry no signal. That difference decides
        whether the paper says two backbones work or two fail, and the panel
        draws it rather than ranking four bars
```

### BC-4 — where the ligands actually are
```
claim   SC-C-1's numerator, plus the dispatch's 4(a) retraction and its 4(i)
        peptide adjudication
shows   the three-band census over the full corpus: in-pocket, entrance-bound,
        off-site, split by ligand_source and by arm. Apo 15.1% off-site
        [14.6, 15.6]; cognate 20.3% [19.8, 20.9]; the v1 pooled 25.6% is retracted
data    12_g4_off_site_census/ — 40,000 rows, the one row-level file the campaign
        shipped
build   cd figures/block_c/panels && python3 bc4_ligand_placement.py
status  ready — FULL-DATA PANEL, the only one in Block C. It exists to prevent
        two errors that have each already caught someone: reading entrance-bound
        as failure (34.8% vs the true 15.1%), and pooling small-molecule with
        peptide ligands (1.52% vs 66.53% off-site in the SAME cells). Chai
        carries a residual far mode of 175 rows beyond 60 A, drawn not trimmed
```

## Block D

Panels built from `data/block_d/`. The loader is `figures/block_d/bddata.py`,
and **every Block D panel must load through it**.

**The rule specific to this block, and it is the whole of it: Block D shipped no
row-level data.** All three corpora its claim sheet names — 42,180 predictions —
are absent from the bundle. Five CSVs ship and every one is panel or reference
metadata. So `bddata` is not a filter, it is a **transcription of record**: each
table is typed in once, beside the document and section it came from, and no
panel may hold its own copy of a number. The one exception is the structures,
which are measured from coordinates rather than transcribed.

**Three traps, encoded rather than documented.**

1. **The CI method is not uniform across tiers.** D3 (26 receptors, 22 clusters)
   uses cluster-boot. D1 (7, 7) and D2 (4, 4) are cluster-boot-*degenerate* —
   one receptor per cluster, so the two bootstraps are the same computation —
   and use receptor-boot. Ask `bddata.ci_method(tier)`; it returns the method
   *and* the reason, and both belong in the caption.
2. **The D3 slope unit is `%/ln(depth)`.** Under log10 the same fits read −3.877
   for Boltz rather than −1.684. `bddata.SLOPE_UNIT` is the only string
   available for that axis.
3. **OpenFold-3 and Protenix are not levers.** They carry the two largest slopes
   and the two weakest claims. `bddata.MECHANISM` holds the four verdicts and
   any panel with a backbone axis must annotate from it.

**Never pool across backbones.** There is no pooling helper in `bddata`. The
original D1 headline was a backbone-averaged apo fraction and was withdrawn
(W-D-2) because the underlying behaviour is bimodal: on ADRB2, Chai calls 100%
of 500 apo samples active and Boltz calls 0%, and the average of those describes
nothing that happened.

### BD-1 — the unsteered apo landscape is receptor- and backbone-specific
```
claim   SC-D-1, SC-D-11
shows   a, b: 7 receptors x 4 backbones on the predicate and on sub-A-to-active,
        apo only, 500 samples/cell; c: the four active-outlier cells drawn twice,
        once on D1 and once on Block A's independent corpus at n=25
data    PARTA_D1.md section 1 (transcribed); the five ringed cells carry an
        NPxxY distance measured here from the shipped coordinates
build   cd figures/block_d/panels && python3 bd1_apo_landscape.py
status  ready — SUMMARY, and it says so. The cross-tier panel c is the strongest
        result in the block because it is the only one that survives a change of
        corpus. Panel a rings ADRB2 on Chai (4.22 A) against ADRB2 on Boltz
        (11.31 A): same receptor, opposite call, measured not transcribed
```

### BD-2 — steering works in the active direction and not the other
```
claim   SC-D-4, SC-D-5, SC-D-6, SC-D-7
shows   a: ACM2 apo -> active-Nb per backbone, with the Ga positive-control band;
        b: the two inactive-Nb receptors, apo -> inactive-Nb, with exact binomial
        intervals
data    PARTA_D2.md F1/F2/F3, n=50 per cell. THE INTERVALS ARE RECOMPUTED — all
        six Clopper-Pearson intervals reproduce from k and n to the stated decimal
build   cd figures/block_d/panels && python3 bd2_direction_asymmetry.py
status  ready — THE CAPTION CARRIES C-D-12 AND THAT IS LOAD-BEARING. All four
        nanobody anchors predate every datable cutoff, so panel b cannot separate
        "cannot steer inactive" from "cannot steer inactive on complexes already
        seen". Two things it must not say, and does not: the OPRK x Boltz cell is
        48% [33.7, 62.6] at n=50, which supports "approaches half" and not "a
        majority invert"; and 14 of 16 control cells clear 96%, so the control
        works and OF3 is the exception
```

### BD-3 — MSA depth moves the predicate for two different reasons
```
claim   SC-D-8; binding on Flag D-2 and Flag D-3
shows   a-d: one panel per backbone, predicate-active and sub-A-to-active against
        depth on a log axis, the two degradation panels shaded; e: matched-seed
        7TM Ca deviation; f: the sub-A and pLDDT deltas
data    PARTA_D3.md section 1 and GATE_3 section 1 (transcribed)
build   cd figures/block_d/panels && python3 bd3_depth_ladder.py
status  ready — the figure IS the gap between the two lines. Where they track,
        depth steers; where they diverge, depth degrades and the coarse predicate
        accepts it. Slopes are printed in %/ln(depth); Chai's crosses zero and is
        printed grey. The four point estimates were refit independently by GATE-2
        and reproduce exactly, but their intervals rest on draws that were not
        shipped
```

### BD-4 — what the directed-nanobody models actually built
```
claim   SC-D-7, plus the F3 and F5 contrast cases
shows   four D2 structures on the NPxxY axis against the 9.08 A threshold, each
        with its one-line verdict
data    10_structures/spot_check/, MEASURED from coordinates by
        analysis/block_d/cifmeasure.py — nothing transcribed
build   cd figures/block_d/panels && python3 bd4_nb_structures.py
status  ready — NOT a render, deliberately: four publication renders under
        RENDER_CONVENTIONS are the figures session's work. What this carries is
        the evidence, which is the number. Selection rule stated on the panel:
        these are the pipeline's hand-picked illustrations, one sample each, not
        a draw, and no rate may be read from them. Row 3 is the honest one — the
        OPRK cell inverts on 48% of samples and this file is one that did not
```

### BD-5 — the same predicate call, reached two opposite ways
```
claim   SC-D-12; binding on Flag D-6
shows   Boltz/OPSD against Protenix/AGTR1, full depth -> depth 8, on the pocket
        axis (which disagrees) and the NPxxY axis (which agrees)
data    GATE_3 cell medians over 50 samples; the shipped single structure for
        each cell is plotted SEPARATELY, measured here
build   cd figures/block_d/panels && python3 bd5_lever_vs_degradation.py
status  ready — the clearest single argument in the block, and it needs no
        statistics. A one-sample value and a 50-sample median are different
        objects and are drawn apart on purpose: confusing them produced a phantom
        discrepancy in our own first checker (D-D-4)
```
