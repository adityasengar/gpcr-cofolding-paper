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
| drafting | *(not built)* | `CLAIMS.md`, `lit/notes/`, `RESULTS.md` **only** | `draft/` | outline ready |
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

`lit/notes/` (4.8 MB) **does** travel, so the 66 extractions with their verbatim quotes
and page numbers are available on both machines. That is the layer most queries need.

`paper_tex/` is its own git repo with the Overleaf remote and is **excluded** from this
one — clone it separately on each machine. Overleaf is the sync channel for LaTeX;
this repo is the sync channel for everything else.

### Roles, and who owns which file

The two sessions do **different work**, and that is what makes the relay safe. The
rule is one owner per file. The non-owner may read anything, but proposes changes as a
note in `SESSIONS.md` rather than editing — that is how "they never update together"
stops depending on luck.

| file / tree | owner | the other side |
|---|---|---|
| `paper_tex/**` (LaTeX, sections, figures in situ) | **drafting** | read only |
| `draft/**` | **drafting** | read only |
| `CLAIMS.md` — the argument | **drafting** | proposes evidence-status flips in SESSIONS.md |
| `lit/**` — corpus, notes, INDEX, SCHEMA, refs.bib | **corpus/data** | read only; request extractions in SESSIONS.md |
| `analysis/**`, `RESULTS.md`, `data/**`, `STATUS.md` | **corpus/data** | read only; cite `[R-*]` ids |
| `CLAUDE.md`, `lit/CLAUDE.md`, the skills | **corpus/data** | proposes in SESSIONS.md |
| `SESSIONS.md` | **both**, append-only at the top | never rewrite an old entry |

**This makes the two-pass rule physical.** The design has always said retrieval and
drafting must not share a session, because a session that does both writes the
paragraph first and then finds support for it. With separate machines and separate
owners, that is no longer a promise an agent has to keep — it is enforced by which
files each one can write.

**The one thing that can still silently drift:** `paper_tex/refs.bib` is generated from
`lit/refs.bib` by `analysis/sync_bib.py`, but they travel on *different* channels —
Overleaf for the first, this repo for the second. The drafting machine can therefore be
citing a stale bibliography with nothing complaining. `session_start.sh` should
regenerate and diff it; until it does, run `python3 analysis/sync_bib.py` by hand after
any pull that touched `lit/refs.bib`.

### Not yet done

`git init` and a private remote. Until then `session_start.sh` degrades gracefully and
just prints the handoff notes and integrity checks.

## Open, and owned by you

- Define the Block A denominator, then re-run `python3 analysis/q.py receptor_counts`.
- `lit/`: `why_it_matters` in `MANIFEST.csv`, provisional `stance` in `INDEX.md`, four
  papers never obtained, five notes still on schema v2.
