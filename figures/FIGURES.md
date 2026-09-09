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
