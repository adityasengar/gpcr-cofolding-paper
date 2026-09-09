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

## Planned

### F1 — the α5-CT contrast
```
claim   C6, C7
shows   TM6 opens under the α5-CT co-input and under cognate Gα, and does not under
        agonist alone; the decoy and shuffled arms stay closed
data    d_tm6 by partner_type, data/predictions.csv (8 arms) — [R-B-LADDER]
build   python3 make_demo.py   (panel a; promote to panels/fig1.py when settled)
status  draft — the arms and the shape are right; the ladder's middle rungs are off
        by 31 points against RESULTS.md, so the y-axis numbers are not yet citable
```

### F2 — within-receptor, so nothing hides in the pooling
```
claim   C6
shows   77 receptors each measured apo and with cognate Gα; almost all move up, and
        the ones that do not are visible rather than averaged away
data    median d_tm6 per receptor, apo vs cognate_ga — [R-B-LADDER]
build   python3 make_demo.py   (panel d)
status  draft — strongest local panel; needs the Block A denominator settled before
        the receptor count in the caption is quotable
```

### F3 — confidence does not track state
```
claim   C8
shows   mean pLDDT at the state anchors against d_tm6, coloured by classified state;
        confident predictions land in both basins
data    plddt_at_anchors_mean vs d_tm6, data/predictions.csv — [R-A-PREDICATE]
build   python3 make_demo.py   (panel c)
status  draft — only 30 of the corpus's 739 plot rows put a confidence score on an
        axis at all, so this panel is close to novel; check it hard
```

### F4 — what was actually run
```
claim   none — this is the honest answer to "what did you run"
shows   receptor × backbone coverage; empty cells drawn as absent, not as zero
data    prediction counts, data/predictions.csv — [R-SCOPE]
build   python3 make_demo.py   (panel e)
status  draft — Block A denominator undefined, see paper/CLAUDE.md
```

### F5 — the α5-CT in the receptor
```
claim   C6 — the structural companion to F1
shows   the 21-mer as an opaque helix in the receptor's intracellular cavity, the
        receptor a pale ghost behind it, R131(3.50) and the α5 contacts labelled
data    structure render; no measured quantity — pair it with F1, never show it alone
build   see scenes/demo_overlay.pml
status  draft — currently 3SN6 over 2RH1 as a smoke test. Must become one of OUR
        predictions with a stated selection rule before it can appear
```

## Notes that outlive any one figure

**Y391 vs E392.** 3SN6 and 6E67 disagree about which residue contacts R131(3.50), and
`tran2026nanogs` exploits the disagreement rather than resolving it. Any labelled
render that names an α5 contact inherits that. Say which structure the label came from.

**F5 must never appear without F1.** 58 of the corpus's 232 render rows are flagged
because a render carries a claim with no quantitative panel behind it. That is the
single easiest defect to commit here.

## Block A

Panels built from `data/block_a/`, the self-contained Block A drop. Their
per-panel provenance — source file, exact filter, n after filtering, claim —
is in `block_a/FIGURE_PROVENANCE.md`, which is the companion to these entries
and carries the material a caption needs. The scripts are in
`block_a/panels/`; the shared loader and the exclusion filters are in
`block_a/badata.py`.

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
build   python3 block_a/panels/ba1_reference_landscape.py
        + the render_struct.py command in block_a/FIGURE_PROVENANCE.md
status  ready — but the caption must say 3SN6 is NOT the ADRB2 panel active
        reference (4LDE is), and the tilt anchors are L75/L275, not the
        L124/F282 that instrument_schematic/ALIGNMENT.md names
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

## Corpus figures

Figures whose data is the **literature corpus**, not our predictions. Every number
comes from `lit/notes/*.md` and `lit/INDEX.md` via two scripts that live here:

```
python3 mine_corpus.py       # notes  -> data_lit/papers.csv, figrows.csv, metrics.csv
python3 classify_corpus.py   # those  -> data_lit/tags.csv, metric_kinds.csv,
                             #           oracle_routes.csv, antimem.csv, figdefects.csv
```

`data_lit/*.csv` is the citable artefact and carries, for every classified row, the
note text the rule fired on. These figures do **not** touch `data/predictions.csv`,
so `analysis/fingerprint.py` drift does not stale them; what stales them is a change
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
