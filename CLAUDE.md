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
| results | `dataquery` | `data/block_<x>/` | `analysis/block_<x>/` | **A, B, C and D landed** |
| drafting | *(no skill)* | `CLAIMS.md`, `lit/notes/`, the current block | `manuscript/` | **all four written** |
| figures | `figbuild` | the current block, `lit/notes/` | `figures/block_<x>/` | **4 main figures + 35 SI; ledger in `figures/FIGURES.md`** |
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

**All four blocks have landed and are written.** Each section states what it
does not claim. **Block D shipped no row-level data at all** — its three corpora,
42,180 predictions, are absent — so its verifier carries a third evidential class,
PROSE-ONLY, and a pass count there is not a claim count.

**ONE of the paper's three title clauses still has no result behind it** — this
said "two" until 2026-09-12. No arm in any block supplies a **peptide** of any
length: every partner arm is a complete Gα subunit or a nanobody, and the segment
this work actually manipulates is **eleven** residues, not 21. Until that is
resolved, no sentence may imply it.

**The agonist clause (C7) is ANSWERED as of 2026-09-12**, from
`rows.tier3.v2.csv` — see `analysis/block_c/received_2026_09_12/WHAT_IT_MEANS.md`.
Agonist-alone does not reproduce the partner effect on any backbone, **but it is
not inert**: on the continuous pocket readout it accounts for roughly a third of
the partner's shift, intervals excluding zero on all four backbones, and it
survives restriction to on-site rows. **Quote the continuous readout, never both** —
the binary predicate is floor-pinned in apo and puts the same effect at ~8%.

**A heading is not exempt from the evidence rule.** Scope gets asserted where it
is most read and qualified where it is least read: on 2026-09-11 a section
heading, an SI caption title and a build-note comment each carried a scope the
body text underneath correctly withdrew. When a scope changes, grep the **short**
text — headings, caption titles, panel titles, ledger status lines.

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
redo/            the SECOND campaign — has its own README.md, read it before
                 touching anything under it
```

## redo/ — the second campaign

**The manuscript is frozen as the record.** `redo/` is the campaign that
supersedes it, and it is a peer of `manuscript/` and `lit/`, not an analysis of
a block. It was `analysis/redo/` until 2026-09-11, where being a sibling of
`block_a..d` made it read as a fifth block, which it is not. **`analysis/redo/`
and `analysis/REDO_EXPERIMENT_CATALOGUE.md` no longer exist** — the catalogue is
`redo/spec/CATALOGUE.md`.

Blocks A–D are untouched and stay that way. No new claim is built on them.

The layout answers the question a flat directory cannot: **may I edit this file,
and has anyone already?**

| where | who may write it |
|---|---|
| `redo/spec/` | a human, once — decisions and what to run |
| `redo/build/`, `redo/gates/` | a human — generators and checks |
| `redo/inputs/` | **code only**, and every file is hashed in `inputs/MANIFEST.tsv` |
| `redo/cache/`, `redo/runs/`, `redo/protocol/` | **nobody** — it arrived from outside |

Four rules, and `redo/gates/layout.py` enforces the first three:

1. **Never hand-edit `redo/inputs/`.** Change the generator, re-run it, then
   `python3 redo/build/manifest.py` to restamp. A hand-edit trips the layout
   guard and the manifest check; **neither preflight gate notices**, which is
   why the layout guard exists separately from them.
   **But know what that guarantee is NOT** (`DECISIONS.md` F-21, F-22): L3
   compares a file to its **own** recorded hash, so it catches an edit made
   *after* stamping and is blind both to a file **created by hand** and then
   stamped, and to a file that has gone **stale** against the inputs it derives
   from. **14 of 64 inputs name no generator** (31 before the detector was fixed), and at least two — including
   `g1_recording_spec.tsv`, the campaign's own recording contract — have no
   writer anywhere in `redo/build/`. L8 reports the count on every run.
2. **Never compute a path from `__file__`** — import it from `redo/paths.py`.
3. **The top level is fixed at eight entries.** Growth goes into `runs/`.
4. **A landed run is read-only**, like `data/block_<x>/`.

`verify.sh` runs the layout guard, the manifest check, the run receipt, the ligand
gate, the decoy gate and all three preflight gates (Group 0, 1 and **2 — the
ligand arm, added 2026-09-12**).

**Which of those have RUNNABLE self-tests, as of 2026-09-12 — this list is the
honest one and the prose around it has been wrong twice:**

| gate | `--selftest` | covers |
|---|---|---|
| `g0_preflight.py` | yes | 12/12 checks |
| `g1_preflight.py` | yes | all blocking checks |
| `g2_preflight.py` | yes | 14 checks, 15 plants |
| `ligands.py` | yes | 10/10 |
| `drule.py` | yes | 16+ checks |
| `layout.py` | yes — **two flags** | `--selftest` L2 (6 plants); `--selftest-all` L1 and L3–L7 (6 plants) |
| `run_receipt.py`, `panel_verify.py` | **none** | — |
| `seqrec_verify.py` | `--plant` *(different flag)* | a roster defect |

**Do not read a gate's tally as coverage of the gate.** `layout.py --selftest`
prints a tally over plants against **L2 alone**; the other six live behind
`--selftest-all`, which also subtracts a baseline run, because a check already
failing on the unplanted tree cannot be proved by planting it. *(Until 2026-09-12
L1 and L3–L7 had no runnable plants at all while the docstring claimed otherwise.
Closed the same day.)*

**And run the self-tests rather than trusting the sentence.** On 2026-09-12 this
paragraph claimed every check in all six was proved by planting, and that had been
false for a day: `g0_preflight.py`'s harness copied only the *top-level* files of
`redo/`, correct while `redo/` was flat and silently wrong from the moment the
campaign moved to the guarded layout. Every plant failed to apply, every check
reported MISS, and the harness printed a tidy tally. The same extension-filter bug
recurred **twice more the same day** in two other harnesses — a hand-written
`(".tsv", ".csv")` list that silently dropped a `.gz` from every planted copy, which
scored one check as fired for the wrong reason and skipped eight others entirely.
**The fix that works is an assertion that the staged copy reproduces the real
directory, and that each plant actually changed bytes** — not a longer list.

**`redo/gates/run_receipt.py` is the one the old campaign never had.** It asks
whether a delivery matches what was requested — chain count, partner identity,
seed, partner MSA depth. The delivered pipeline compared output to input nowhere,
so a monomer returned where a dimer was asked for passed every check. **A missing
column is a FAILURE there, not a skip**: a check that quietly does nothing when its
input is absent is the defect it exists to catch.

**One standing trap in `verify.sh` itself:** the corpus line calls `ok()` on both
branches (`:26-27`), so it prints `drift reported` without failing the run. That
drift is the four deliberately-unread `refs.bib` entries and is expected. Do not
read that line as a broken build — and do not read its absence as a passing corpus
check.

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

### Skills

| skill | when |
|---|---|
| `litquery` | anything about prior work, and figure design by analogy |
| `dataquery` | anything about our own numbers |
| `figbuild` | making or checking a figure |
| `blockintake` | **a new block zip arrives** — carries the eight failure classes Block A hit |
| `wrap-session` | closing a session: housekeeping, then a compact and a resume prompt |

### What we ask the pipeline for, and where it lives

**Two files per block, and they have different audiences.** Keep them apart —
merging them produces a document neither reader can act on.

| file | audience | holds |
|---|---|---|
| `analysis/block_<x>/DATA_REQUESTS.md` | the **pipeline team** | numbered asks for files and columns, ranked by whether a manuscript sentence depends on the answer, each with a cost class; then open questions about the data |
| `rebuttals/BLOCK_<X>.md` | the **orchestrator agent** | **R**ebuttals (what the drop got wrong, with the recomputation), **Q**uestions (what we cannot resolve ourselves), **S**uggestions (experiments that would elevate the paper) |

Cost classes are **free** (re-analysis of data already held), **cheap**
(re-scoring existing predictions, no new inference) and **real** (new
predictions). Every ask carries one. As of 2026-09-11: Block A 15 asks, B 17,
C 18, D 12 — and **every Block C ask is free**, because its numbers are already
computed and sitting in files that were not zipped. **The single highest-value
ask in all four documents is Block C's ask 1, `rows.tier3.v2.csv`**: it unblocks
two Block C claims, the G4 off-site gate that fired on 8 of 12 cells, and the
uncrossed ligand-class × partner-presence result that 18,400 already-scored
predictions are sitting on.

`rebuttals/` also holds `PANEL_EXPANSION.md` and `PANEL_EXPANSION_CLASS_A.md`
(19 Class A receptors with both states that our panel lacks) and a `README.md`
carrying the conventions. Nothing here has been sent upstream yet.

**The rule that keeps these documents usable:** an ask for a file we already
hold destroys the credibility of every real ask beside it. `analysis/audit_asks.py`
checks every path in all six documents against the filesystem and fails on any
that is claimed absent and is not.

`sessions/` holds one log per session and `SESSIONS.md` is its index: git records *what* changed, `SESSIONS.md` records *why* and
what the next session should not redo. Note that `test-laptop` in the older log is **not a real machine** — it was a throwaway clone used to test the sync machinery.

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
