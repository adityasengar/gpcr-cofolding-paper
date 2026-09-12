# redo/ — the second campaign

The manuscript in `manuscript/` is **frozen as the record**. This directory is
the campaign that supersedes it. Nothing here builds on Blocks A–D; they remain
the evidence behind a finished paper and are not touched.

## The one thing to understand

A flat directory cannot answer the question you actually have when you open a
file: **may I edit this, and has anyone already?** So the layout answers it by
position. There are four kinds of thing here, and the difference between them is
who may write them:

| where | who may write it | if it is lost |
|---|---|---|
| `spec/` | a human, once | the reasoning is gone — irreplaceable |
| `build/`, `gates/` | a human | rewrite it |
| `inputs/` | **code only** | re-run the generator |
| `cache/`, `runs/`, `protocol/` | **nobody** — it came from outside | re-fetch, or re-ask |

Editing a file in `inputs/` by hand is a defect, and `gates/layout.py` will
find it: every one of the 47 files is hashed in `inputs/MANIFEST.tsv`.

## Layout

```
README.md     this file
paths.py      every path declared once — nothing computes its own
spec/         what to run and why.  CATALOGUE.md is the menu (33 experiments);
              PANEL, SEQUENCES, SEQ_RECEPTORS, COUPLING, GROUP0_SYSTEMS,
              GROUP1_SYSTEMS, RUN_MATRIX are the frozen specs
build/        28 generators — code that turns spec into inputs
gates/        the checks: g0_preflight, g1_preflight, panel_verify,
              seqrec_verify, layout
inputs/       47 generated artefacts + MANIFEST.tsv (sha256 of each)
cache/        what RCSB / GPCRdb / UniProt said on the day we froze.  Committed
              as provenance — those databases change, so a re-fetch is not the
              same data.  cache/structures/ (297 mmCIF, 59 MB) is gitignored
runs/         deliveries.  One directory per run, read-only once landed,
              identical shape inside.  See runs/README.md
protocol/     what we asked paper_af3, and what they answered
```

Growth goes into `runs/` and nowhere else. That is the property that makes this
survive a few hundred runs: `spec/` never grows, `build/` grows slowly, and the
top level is fixed at eight entries by check **L1**.

## The rules

1. **Never hand-edit `inputs/`.** Change the generator in `build/`, re-run it,
   then `python3 redo/build/manifest.py` to restamp.
2. **Never compute a path from `__file__`.** Import it from `paths.py`. A move
   then costs one edit instead of silently changing what a script reads.
3. **A landed run is read-only**, like `data/block_a/`. Defects in a delivery
   get recorded, not repaired.
4. **Every check is proved by planting the defect it catches**, before it is
   trusted. A silent check looks exactly like a passing one.

## Where to start

```bash
python3 redo/gates/layout.py         # is the structure intact?
python3 redo/gates/g0_preflight.py   # Group 0 — 12 pass, 8 dependencies
python3 redo/gates/g1_preflight.py   # Group 1 — 16 pass, 7 dependencies
```

Then `spec/CATALOGUE.md` for what could be run, and `spec/RUN_MATRIX.md` for
what it costs.
