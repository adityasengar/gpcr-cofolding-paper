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
| you read | `data/block_a/`, `analysis/block_a/`, `CLAIMS.md`, `lit/notes/`, `lit/INDEX.md` |
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
block_a/         the current block: badata.py loader, cifread.py anchor
                 verification, panels/, FIGURE_PROVENANCE.md
mine_corpus.py   lit/notes/*.md -> data_lit/*.csv, the corpus figures' input
classify_corpus.py  rules over those tables — DURABLE, every rule is auditable
data_lit/        extracted corpus tables — DURABLE, in git
panels/          one script per finished figure
figpanels.py     panel generators; each names the defect it prevents
render_struct.py PyMOL renders, driven from the command line
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

**Run `python3 ../analysis/block_a/verify_claims.py` before believing any number.**
It recomputes every checkable claim from the tidy files and exits 1 on any
mismatch. Mismatches are expected and recorded — what matters is that a panel
never draws a number the check does not reproduce.

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

## The data you work from

**One block at a time.** The current block is `data/block_a/` — 9,490 scored
predictions, 48 receptors, 4 backbones, 2 arms (apo and cognate). It is
**read-only**; never edit the drop. Load it through
`figures/block_a/badata.py`, which knows the thresholds and the exclusion flags.

Block B will arrive as its own zip and supersede Block A for new claims. When it
does, add `figures/block_b/` beside the existing one rather than editing it.

**Read `analysis/block_a/DISCREPANCY_REPORT.md` before drawing anything.** The
shipped claim sheet and the shipped data disagree in 21 places. Four were named
in the brief; seventeen were found here, including a structure file that is the
wrong protein entirely and four `ALIGNMENT.md` files naming anchors that do not
reproduce the shipped distances. **Recompute every anchor and every distance
from coordinates before drawing it** — `figures/block_a/cifread.py:verify_anchor`
refuses to return one that does not match the tidy value.

## Render conventions

`lit/RENDER_CONVENTIONS.md` records how this literature actually draws these
figures, surveyed by viewing panels rather than reading captions. The two that
matter most:

- **Grey means "not the subject", never "reference".** Grey the invariant
  scaffold and colour only the element carrying the claim.
- **Annotate every measured distance with the atom pair it was measured
  between.** No render in the 232-row corpus survey does this; doing it puts us
  ahead of all of them.
