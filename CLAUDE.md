# CLAUDE.md — orchestrator for the α5-CT conformational-control manuscript

This folder produces one paper. The claim it defends: for GPCRs, a 21-residue Gα α5
C-terminal peptide supplied as a **co-input** drives Boltz-2 / OpenFold3 / Protenix /
Chai-1 into the **active** state; the agonist alone does not; and model confidence does
not track state correctness.

## Stages, and who owns what

| stage | skill | reads | writes | status |
|---|---|---|---|---|
| prior work | `litquery` | `lit/SCHEMA.md`, `lit/INDEX.md`, `lit/notes/` | nothing | **built** |
| results | `dataquery` | `data/`, `rows_enriched_v3_7.csv`, `analysis/q.py` | `RESULTS.md` | **built** |
| drafting | *(no skill yet)* | `CLAIMS.md`, `lit/notes/`, `RESULTS.md` **only** | `manuscript/`, `draft/` | outline ready; builds |
| figures | *(not built)* | `data/`, `analysis/` | `figures/` | pending |
| submission | *(not built)* | `draft/`, `lit/refs.bib` | — | pending |

## The rule that makes this work

**Every sentence in the paper carries a locator.** Prior work cites `[citekey p.N]`;
our own numbers cite a `RESULTS.md` entry id such as `[R-B-LADDER]`. A sentence with
neither is not ready, whatever it sounds like.

**Retrieval and drafting never share a session.** A session that both computes and
writes produces the paragraph first and then finds support for it — the citations
become decoration for a conclusion already reached, and the output is indistinguishable
from the grounded version. `litquery` and `dataquery` both refuse to write manuscript
prose for this reason. Do not relax it when the drafting stage is built.

**`STATUS.md` planned blocks are radioactive.** D1, D2, D3 and T1.5 have **not** run.
No draft sentence may depend on them. If D2 lands, the gap paragraph in the intro must
be rebuilt, because the papers worth contrasting against change.

## Layout

```
CLAUDE.md        this file
STATUS.md        landed vs planned blocks — CLAIMS, not evidence
CLAIMS.md        the argument spine — DURABLE, survives a data refresh
RESULTS.md       the ledger: one entry per citable number — PERISHABLE, snapshot only
draft/OUTLINE.md manuscript skeleton, per-section gates and citation rules
manuscript/      the LaTeX (canonical) + build.sh
tex/             pinned TeX environment + check_tex.sh
analysis/q.py    the queries behind the ledger — `python3 analysis/q.py --list`
analysis/fingerprint.py  --check before citing; --stamp after a refresh
data/            predictions.csv (17,568) · conditions · receptors · backbones · coverage
rows_enriched_v3_7.csv   19M, 68 cols, full per-prediction provenance
report/          existing summary.tex / summary.pdf
lit/             the literature corpus — has its own CLAUDE.md, read it before
                 answering anything about prior work
```

## Durable vs perishable — read this before trusting any number here

New experimental data will land and may override what is currently in `data/`. The
repo is arranged so that a refresh invalidates as little as possible:

| durable — survives a data refresh | perishable — dies with the refresh |
|---|---|
| `CLAIMS.md` — the argument and its evidence slots | `RESULTS.md` verdicts and numbers |
| `analysis/q.py` — the queries | the answers those queries currently give |
| `draft/OUTLINE.md` — section structure and gates | any drafted Results prose |
| `lit/` — the entire literature corpus | — |

**Always run `python3 analysis/fingerprint.py --check` before citing a number.** It
compares the data against `.datafingerprint` and tells you whether `RESULTS.md` still
applies. If it reports a change, every verdict is stale until re-derived — do not
paper over it.

The current export is a **partial** one: 17,568 predictions against ~41,500 described
in `STATUS.md`, all paths pointing at `/hpc/scratch/sengaad1/`, and 39% of rows with no
`classified_state`. Several `STATUS.md` numbers do not reproduce against it. That is
recorded in `RESULTS.md` and is expected to change — it is **not** a finding about the
experiments, and should not be treated as one. Do not spend effort analysing this
snapshot further; the paper-shaped work below is what is worth doing now.

## What is ready to write today, refresh or no refresh

- **Methods** — fully unblocked. `rows_enriched_v3_7.csv` already carries
  `scorer_git_sha`, `scorer_version`, `bw_derivation_source`, the GPCRdb hashes and
  `ref_pdb_sha_active/inactive`. Writing it now also forces the state predicate and its
  threshold to be pinned down before any Results sentence leans on them.
- **Introduction** — fully unblocked. Claims C1–C5 in `CLAIMS.md` are lit-only and all
  marked ready; the gap paragraph and its named near-miss (`yang2025statespecific`) do
  not depend on our numbers at all.
- Results, Discussion and Abstract are gated on the export. See `draft/OUTLINE.md`.

## Working across two machines

Two Claude sessions, two laptops, **never concurrent**. This is a relay, not a merge.

**Start every session with `./session_start.sh`.** It pulls, then shows: the commits
since *this machine* last signed off, the files they touched, the last two handoff
notes, corpus integrity, data freshness, and which heavy assets are missing locally.

**End every session with `./session_end.sh "what I did"`**, then commit and push. The
commit message must contain `session-end(<machine>)` — `session_start.sh` finds it to
compute "since my last visit". Set the machine name in `.machine` (defaults to hostname).

`SESSIONS.md` is the handoff log, newest first. Git records *what* changed; SESSIONS.md
records *why*, and what the next session should not redo.

### What travels, and what does not

The shared repo is ~21 MB. `.gitignore` excludes the heavy, reconstructible things:

| stays local | why | consequence on the other machine |
|---|---|---|
| `lit/pdfs/` (452M) | re-downloadable from the DOIs in `refs.bib` | `litquery`'s "open the PDF when the note is too coarse" step **cannot run**. Say "the PDF is not on this machine" — never answer from memory instead. |
| `lit/source/` (458M) | hard links to the same PDFs | provenance only |
| `rows_enriched_v3_7.csv` (19M) | HPC export, not authored here | `dataquery` falls back to `data/*.csv`; the provenance columns are unavailable |
| `lit/validate/txt*`, `ocr/` | regenerable with `pdftotext` | quote re-verification cannot run |

`lit/notes/` (5.9 MB) **does** travel, so the 71 extractions with their verbatim quotes
and page numbers are available on both machines. That is the layer most queries need.

`paper_tex/` is its own git repo with the Overleaf remote and is **excluded** from this
one — clone it separately on each machine. Overleaf is the sync channel for LaTeX;
this repo is the sync channel for everything else.

### Who does what — corrected 2026-09-09

Earlier versions of this file had these roles backwards. This is the real layout.

| | **this laptop** | **the other laptop** |
|---|---|---|
| role | authors the manuscript; runs several sessions in different folders | holds the scripts and data; can also compile the LaTeX |
| writes | `manuscript/**`, `CLAIMS.md`, `draft/**`, `lit/**` | `data/**`, `analysis/**`, `RESULTS.md`, `STATUS.md` |
| reads | everything | everything |
| authors LaTeX? | **yes** | no — compiles and checks only |

**Data lives on the other laptop.** What is in `data/` here is a copy. When the two
disagree, that machine wins.

### Two different sharing problems — do not confuse them

**Across the two laptops.** They never run at once. Git handles it: `./session_start.sh`
to pull and see what changed since this machine last signed off, `./session_end.sh` to
record why. Working and tested.

**Several sessions on THIS laptop, in different folders.** Git gives **no protection
here** — they share one working tree. If two sessions edit the same file the last write
silently wins; `git add -A` in one can commit another's half-finished edit. There is no
conflict and no warning, because these sessions never become separate commits.

The rule: **only one session writes at a time.** The others read. `./session_start.sh`
runs `.session-guard.sh`, which warns when another session claimed the tree recently and
reports uncommitted work already present. It is advisory — it cannot stop anything.

If you genuinely need two writing at once, give each its own `git worktree` (separate
directory, separate branch, one repository) and merge afterwards. Do not skip that and
hope.

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
`manuscript/` into the `paper_tex/` clone and pushes, so you can share a read-only link.
Edits made in the Overleaf web editor do **not** come back — they will be overwritten on
the next publish.

### Setting up the second machine

```bash
git clone https://github.com/adityasengar/gpcr-cofolding-paper.git paper
cd paper
echo "<a-name-for-that-laptop>" > .machine     # NOT committed; per-machine
git clone https://git@git.overleaf.com/6aa05386f57a5fee700a37ff paper_tex
./session_start.sh
```

The Overleaf project is a **separate** clone — `paper_tex/` is gitignored here on
purpose, because nesting git repos causes submodule grief. Overleaf syncs the LaTeX;
this repo syncs everything else.

That machine will **not** have `lit/pdfs/`, `lit/source/`, `rows_enriched_v3_7.csv` or
the pdftotext caches. `session_start.sh` prints which are missing. It *will* have all
71 extractions in `lit/notes/`.

## Open, and owned by you

- Define the Block A denominator, then re-run `python3 analysis/q.py receptor_counts`.
- `lit/`: `why_it_matters` in `MANIFEST.csv`, provisional `stance` in `INDEX.md`, seven
  papers with no full text, six notes still on schema v2, and one open vocabulary
  decision (a `non-biomolecular` system tag). See `lit/CLAUDE.md`.
