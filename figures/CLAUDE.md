# CLAUDE.md — the figures session

> **This file is owned by the FIGURES session (the one running in `paper/figures/`).**
> The orchestrator owns `paper/CLAUDE.md`; the lit agent owns `lit/CLAUDE.md`.
> Do not edit either of those from here. Propose changes in `SESSIONS.md`.

This folder makes every figure in the manuscript. The claim they have to carry: for
GPCRs, a 21-residue Gα α5 C-terminal peptide supplied as a **co-input** drives
Boltz-2 / OpenFold3 / Protenix / Chai-1 into the **active** state; the agonist alone
does not; and model confidence does not track state correctness.

## What you own

| | |
|---|---|
| you write | `figures/**`, and figure **captions** in `manuscript/sections/figures.tex` |
| you read | `data/`, `CLAIMS.md`, `RESULTS.md`, `lit/notes/`, `lit/INDEX.md` |
| you never touch | git, `manuscript/main.tex`, anything under `lit/` or `analysis/` |

Body prose belongs to the lit agent. Captions belong to you, because a caption's
load-bearing content is n, the selection rule, the threshold and the provenance —
the material in `.prov.json`. The corpus is blunt about what happens when whoever
writes the caption does not hold that: 59 renders with an unstated selection rule.

**You never run git.** Aditya tells the orchestrator when you are done and it commits
with explicit paths. Both sessions share one working tree, so `git add -A` from
anywhere commits half-finished work under a misleading message. That has already
happened once.

## Layout

```
FIGURES.md       the ledger: one entry per figure — DURABLE
figstyle.py      house style: sizes, fonts, palette, save()
mine_corpus.py   lit/notes/*.md -> data_lit/*.csv, the corpus figures' input
classify_corpus.py  rules over those tables — DURABLE, every rule is auditable
data_lit/        extracted corpus tables — DURABLE, in git
panels/          one script per finished figure
figpanels.py     panel generators; each names the defect it prevents
render_struct.py PyMOL renders, driven from the command line
make_demo.py     builds one of every panel from data/predictions.csv
scenes/          .pml sources and camera views — DURABLE, in git
structures/      downloaded PDBs — not in git
out/             generated images — not in git
README.md        the corpus survey the design rules come from
```

Durable vs perishable is the same split the rest of the repo uses: the scripts, the
ledger and the scenes survive a data refresh; the images do not.

## The two rules

**Every figure has a ledger entry before it has an image.** An entry names the claim
it defends and the `[R-*]` ids of every number it shows. A panel with no entry is not
a figure, it is a plot.

**Run `python3 ../analysis/fingerprint.py --check` before believing any number.** If
the data moved, every `RESULTS.md` verdict is stale and so is every panel built on one.

## Asking the corpus

You have `litquery`. Use it for two things and not for others:

- *"show me their figure 3"* — the note's figure table gives figure → page.
- *"I have this shape of data, what figure should I make"* — design by analogy,
  which matches on `data_shape` rather than subject matter, so a good design from an
  unrelated field is fair game. It also surfaces `hides` on near-matches.

Do not use it to settle what a paper claims — that is the lit agent's job, and it
holds the context to do it properly.

**Before adapting anyone's panel, check the licence.** 15 papers are ND, which
forbids redrawing and not merely copying, and 4 are all-rights-reserved. The list is
in `README.md`. ND does not reserve a plot *type* — a violin faceted by predictor is
a convention, not property — so this only bites if you adapt a specific figure.

## What the corpus says about failure

Parsing the `## F. Figures` table of all 78 notes gives 1,226 panel-group rows.
**80% of the 232 structure renders carry a recorded defect** (186; corrected from
81%/189 on 2026-09-09 - three `*(blank - reason)*` cells were being counted as
defects, see `README.md`). Corpus-wide it is 957 of 1,226. The two that dominate:
a hand-picked example with the selection rule unstated (59), and no quantitative
panel standing behind the claim the render makes (58).

So `render_struct.py` refuses to run without `--selected-from` and `--selection-rule`.
On the plot side the recurring failures are bars standing in for distributions,
missing n, broken axes, and two measures sharing one axis. Do not do those.

## What can be plotted today

`data/predictions.csv` — 17,568 rows, 16,388 scored — carries `d_tm6`, `d_npxxy`,
`classified_state`, `plddt_at_anchors_mean` and the eight-arm `partner_type`. The
central contrast, the decoy and shuffled arms, the confidence-vs-state scatter and
the coverage grid are all derivable **locally, now**.

`delta_to_active` is null for 41% of rows — several receptors carry no active
reference — so any panel measuring distance *to the deposited active state* still
waits on an import from the HPC. `d_tm6` is the raw geometry and does not.
