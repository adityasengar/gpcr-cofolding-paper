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

**`data/` here is a deliberate small import, not a mirror.** The real corpus is 1 TB+
and lives on the HPC and Aditya's other machine; it is brought over by ad-hoc import,
one claim's worth at a time. So a number that does not reproduce locally is **unverified here**, which is the
expected steady state, not a defect and not a finding about the experiments.

What is imported now: 17,568 predictions, against ~41,500 described in `STATUS.md`, with
39% of rows carrying no `classified_state`. `RESULTS.md` records claim by claim which
figures survive against it. Do not analyse this slice further for its own sake — when a
draft sentence needs a number that is not here, request the specific import in
`SESSIONS.md` rather than working around the gap.

## What is ready to write today, refresh or no refresh

- **Methods** — fully unblocked. `rows_enriched_v3_7.csv` already carries
  `scorer_git_sha`, `scorer_version`, `bw_derivation_source`, the GPCRdb hashes and
  `ref_pdb_sha_active/inactive`. Writing it now also forces the state predicate and its
  threshold to be pinned down before any Results sentence leans on them.
- **Introduction** — fully unblocked. Claims C1–C5 in `CLAIMS.md` are lit-only and all
  marked ready; the gap paragraph and its named near-miss (`yang2025statespecific`) do
  not depend on our numbers at all.
- Results, Discussion and Abstract are gated on the export. See `draft/OUTLINE.md`.

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

`lit/pdfs/` (452 MB), `lit/source/` (458 MB), `rows_enriched_v3_7.csv` (19 MB) and the
`pdftotext` caches are excluded to keep the repo small. They live on this laptop only,
so a fresh clone elsewhere has the 78 extractions in `lit/notes/` but no PDFs.

`overleaf/` is a separate clone of the Overleaf project, used only as an export target
via `./publish_overleaf.sh`. `manuscript/` is canonical.

### Who does what

Two working sessions on this one laptop. **Content versus machinery** is the split.

| | **lit agent** (runs in `paper/lit/`) | **orchestrator** (runs in `paper/`) |
|---|---|---|
| owns | the corpus and the words | how the paper is built |
| writes | `lit/**`, `manuscript/sections/*.tex`, `CLAIMS.md` | `manuscript/main.tex`, `analysis/**`, `tex/**`, this file |
| git | **never** | all of it |

Rule of thumb: **what the paper says → lit agent. How the paper is built → orchestrator.**

Aditya routes between them; there is no automation. Worked examples:

- *"Is this claim in the intro supported?"* → lit agent (it has `litquery` and the notes).
- *"Change the margins / spacing / fonts"* → orchestrator (`main.tex` is the container).
- *"Add or remove a paper"* → lit agent extracts and updates `lit/**`; then the
  orchestrator regenerates `manuscript/refs.bib` and commits.
- *"Rewrite the gap paragraph"* → lit agent, editing `sections/intro.tex` directly.
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

- Define the Block A denominator, then re-run `python3 analysis/q.py receptor_counts`.
- `lit/`: **the bibliography is fully extracted, 78 of 78.** Remaining: `why_it_matters`
  in `MANIFEST.csv`, provisional `stance` in `INDEX.md`, six notes still on schema v2,
  four notes with no page numbers, one partial note (`ingraham2023chroma`), and two open
  vocabulary decisions (`non-biomolecular`, and the `af-cluster` collision).
  See `lit/CLAUDE.md`.
- **`CLAIMS.md` threats table needs `yu2026domainmotion` added** — nonbinder ligands
  reproduce the conformational change in 82 enzymes, which directly exposes the decoy arm.
