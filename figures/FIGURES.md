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
