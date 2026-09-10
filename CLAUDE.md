# CLAUDE.md — orchestrator for the α5-CT conformational-control manuscript

> **This file is owned by the ORCHESTRATOR session (the one running in `paper/`).**
> If you are the lit agent, the drafting agent, or the data agent: **do not edit this
> file**, not even to refresh a number. Propose the change in `SESSIONS.md` instead.
> Corpus counts here are allowed to lag; `lit/corpus_check.sh` is the live source of
> truth for them. A brief that several agents rewrite is a brief nobody can trust.
> Each agent has its own file: `lit/CLAUDE.md` for the corpus, this one for the whole.

This folder produces one paper. The claim it defends: for GPCRs, a 21-residue Gα α5
C-terminal peptide supplied as a **co-input** drives Boltz-2 / OpenFold3 / Protenix /
Chai-1 into the **active** state; the agonist alone does not; and model confidence does
not track state correctness.

## Stages, and who owns what

| stage | skill | reads | writes | status |
|---|---|---|---|---|
| prior work | `litquery` | `lit/SCHEMA.md`, `lit/INDEX.md`, `lit/notes/` | nothing | **built** |
| results | `dataquery` | `data/block_<x>/` | `analysis/block_<x>/` | **Block A landed** |
| drafting | *(no skill)* | `CLAIMS.md`, `lit/notes/`, the current block | `manuscript/` | **Block A written** |
| figures | `figbuild` | the current block, `lit/notes/` | `figures/block_<x>/` | **Block A: 5 main, 16 SI** |
| submission | *(not built)* | `manuscript/`, `lit/refs.bib` | — | pending |

## The rule that makes this work

**Every sentence in the paper carries a locator.** Prior work cites `[citekey p.N]`;
our own numbers are recomputed from the current block by
`analysis/block_<x>/verify_claims.py`. A sentence with
neither is not ready, whatever it sounds like.

**Retrieval and drafting never share a session.** A session that both computes and
writes produces the paragraph first and then finds support for it — the citations
become decoration for a conclusion already reached, and the output is indistinguishable
from the grounded version. `litquery` and `dataquery` both refuse to write manuscript
prose for this reason. Do not relax it when the drafting stage is built.

**Later blocks are not yet run.** Blocks B, C and D have not landed. No draft
sentence may depend on one, and the Block A section states explicitly what it
does not claim.

## Layout

```
CLAUDE.md        this file
CLAIMS.md        the argument spine — DURABLE, survives a data refresh
data/block_a/    the Block A drop, pristine and read-only
analysis/block_a/  verify_claims.py, DISCREPANCY_REPORT.md, tables/,
                 DATA_REQUESTS.md, LIT_COORDINATION.md
figures/         the toolkit and every panel — has its own CLAUDE.md
manuscript/      the LaTeX (canonical): main.tex, si.tex, sections/, tables/
tex/             pinned TeX environment + check_tex.sh
lit/             the literature corpus — has its own CLAUDE.md, read it before
                 answering anything about prior work
```

## How data arrives: one block at a time

**Each block arrives as a zip and supersedes everything before it.** Block A
landed 2026-09-09 as `block_a_figure_data.zip` and lives in `data/block_a/`.
Block B will arrive the same way. When it does, Block A is not deleted — it
remains the record behind the Block A section — but no new claim is built on it.

The earlier export (`data/predictions.csv`, `rows_enriched_v3_7.csv`,
`RESULTS.md`, `STATUS.md`, `analysis/q.py`, `analysis/fingerprint.py`) was
**deleted on 2026-09-10**. It described a *different campaign*: only 28 of Block
A's 48 receptors appeared in it, no prediction paths coincided, and it carried
arms and a backbone Block A does not have. Keeping it invited exactly one
mistake — a number from the wrong campaign reaching a sentence. It is in git
history if ever needed.

**Rules for a block.**

- `data/block_<x>/` is **read-only**. Never edit the drop.
- Everything derived goes in `analysis/block_<x>/`: `verify_claims.py`
  recomputing every checkable number from the tidy files, a
  `DISCREPANCY_REPORT.md`, tables, and `DATA_REQUESTS.md` for the pipeline agent.
- **The data wins over the claim sheet, always**, and the disagreement is
  recorded rather than smoothed. Block A carries 21 recorded discrepancies —
  four named in the brief, seventeen found here.
- Panels go in `figures/block_<x>/panels/`; images to `figures/out/`, which is
  gitignored because it is regenerable.

## Durable vs perishable

| durable | perishable |
|---|---|
| `CLAIMS.md` — the argument and its evidence slots | any number tied to one block |
| `analysis/block_*/verify_claims.py` — the checks | the answers they give today |
| `figures/**` — toolkit and panel scripts | `figures/out/` — the images |
| `lit/` — the entire literature corpus | — |

## How work is organised

One laptop. A second was set up on 2026-09-09 and abandoned as more complexity than it
was worth; data from the other machine now arrives by ad-hoc import instead.

`./session_start.sh` at the start of a session (pulls, then checks corpus integrity, TeX
against the pin, the bibliography, and whether another session has work in flight).
`./verify.sh` runs the full self-check. `./session_end.sh "summary"` writes a handoff
note into `SESSIONS.md` before committing.

`SESSIONS.md` is the log: git records *what* changed, `SESSIONS.md` records *why* and
what the next session should not redo. Note that `test-laptop` in that file is **not a
real machine** — it was a throwaway clone used to test the sync machinery.

### What is deliberately not in git

`lit/pdfs/` (452 MB), `lit/source/` (458 MB), `data/block_a/11_structures/` (13 MB),
`figures/out/` and the `pdftotext` caches are excluded to keep the repo small. They live on this laptop only,
so a fresh clone elsewhere has the 78 extractions in `lit/notes/` but no PDFs.

`overleaf/` is a separate clone of the Overleaf project, used only as an export target
via `./publish_overleaf.sh`. `manuscript/` is canonical.

### Who does what

Three working sessions on this one laptop. **Content versus machinery** is the split,
with figures as their own seat because a figure is simultaneously a claim and an
artefact.

| | **lit** (`paper/lit/`) | **figures** (`paper/figures/`) | **orchestrator** (`paper/`) |
|---|---|---|---|
| owns | the corpus and the words | every figure, and its caption | how the paper is built |
| writes | `lit/**`, `sections/intro.tex`, `CLAIMS.md` | `figures/**`, `sections/figures.tex` | `main.tex`, `analysis/**`, `tex/**`, this file |
| skill | `litquery` | `figbuild` + `litquery` | `dataquery` |
| git | **never** | **never** | all of it |

Rule of thumb: **what the paper says → lit. What a figure shows → figures. How the
paper is built → orchestrator.**

Captions belong to the figures session, not to lit. A caption's load-bearing content
is n, the selection rule, the threshold and the provenance — the `.prov.json`
material — and the corpus is blunt about what happens when whoever writes it does not
hold that.

Aditya routes between them; there is no automation. The sessions do not message each
other, so nothing may depend on one knowing what another said: `figures/FIGURES.md`
and `SESSIONS.md` carry state across, and both outlive any session.

Worked examples:

- *"Is this claim in the intro supported?"* → lit (it has the notes).
- *"Plot the α5-CT arm" / "the render looks wrong"* → figures.
- *"What figure should I make for this data?"* → figures; it has `litquery` for
  design-by-analogy and does not need to route through lit.
- *"Change the margins / spacing / fonts"* → orchestrator (`main.tex` is the container).
- *"Add or remove a paper"* → lit extracts and updates `lit/**`; then the
  orchestrator regenerates `manuscript/refs.bib` and commits.
- Build broken, PDF won't compile, anything git → orchestrator.

### The rule that keeps this safe

**Only the orchestrator runs git. The lit agent edits files and nothing else.**

Both sessions share one working tree, so git gives no isolation: if one runs
`git add -A` while the other is mid-edit, it commits half-finished work under a
misleading message, with no conflict and no warning. That has already happened —
commit `7e03642` swallowed the lit agent's five extractions and a 319-line intro draft.

So: **even the orchestrator stages explicit paths, never `git add -A`.** And Aditya
tells the orchestrator when the lit agent has finished; without that signal it either
commits mid-edit or lets two pieces of work merge into one commit describing neither.

### Two-pass discipline — where it actually stands

The design principle was that the session which retrieves evidence must not be the one
that writes prose, because it will write first and find support afterwards. **That
separation has collapsed**: the lit agent both owns the corpus and wrote the
introduction. The current split is about *context* — one session cannot comfortably hold
the schema, the index, 78 extractions, the build system and the git history — not about
evidential integrity.

Restore it with a third, prose-only session when Results land and numbers start entering
sentences. It is not worth it for an introduction that is purely literature.

### The manuscript

`manuscript/` in this repo is **canonical**. Build on either laptop with the same
command:

```bash
./manuscript/build.sh          # compile; reports bibitems and undefined citations
./manuscript/build.sh clean
```

`manuscript/refs.bib` is generated from `lit/refs.bib` by `analysis/sync_bib.py` — never
hand-edit it. Unread papers are emitted with their `@` stripped so citing one fails
loudly; `build.sh` names the offending key.

**Overleaf is an export target, not a workspace.** `./publish_overleaf.sh` copies
`manuscript/` into the `overleaf/` clone and pushes, so you can share a read-only link.
Edits made in the Overleaf web editor do **not** come back — they will be overwritten on
the next publish.

## Open, and owned by you

- `lit/`: **the bibliography is fully extracted, 78 of 78.** Remaining: `why_it_matters`
  in `MANIFEST.csv`, provisional `stance` in `INDEX.md`, four notes with no page
  numbers, one partial note (`ingraham2023chroma`), and two open vocabulary decisions
  (`non-biomolecular`, and the `af-cluster` collision). **The schema-v2 backlog closed
  on 2026-09-09 — all 78 notes are v3.**
  See `lit/CLAUDE.md`.
- **`CLAIMS.md` threats table needs `yu2026domainmotion` added** — nonbinder ligands
  reproduce the conformational change in 82 enzymes, which directly exposes the decoy arm.
