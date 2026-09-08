# SESSIONS.md — handoff log

Newest first. Every session **ends** by running `./session_end.sh "summary"`, and
**starts** by running `./session_start.sh`.

Git records what changed; this file records *why*, and what the next session should
not redo. Two machines, never concurrent — so this is a relay baton, not a merge.

## 2026-09-08 20:56  ·  MacBook-Pro-3

Set up the shared remote. The two-machine relay is now live.

- **Remote:** https://github.com/adityasengar/gpcr-cofolding-paper (PRIVATE, verified).
  125 files, 20.2 MB. `lit/pdfs`, `lit/source`, `rows_enriched_v3_7.csv` and the
  pdftotext caches are excluded; `lit/notes/` (all 66 extractions) travels.
- **Overleaf stays separate.** `paper_tex/` is gitignored; clone it per machine.
- Bugs found and fixed today, all before anything was published:
  1. `.gitignore` used trailing inline comments, which git does not strip — none of
     the heavy excludes were working. Caught by auditing the staged set.
  2. The first bad `git add` wrote 423 MB of PDF blobs into `.git`; reclaimed to 5.2 MB.
  3. `sync_bib.py` "commented out" unread entries with `%%`, which BibTeX ignores —
     it scans for `@` regardless. All 12 unread papers were silently citable.
     Verified by experiment; fixed by stripping the `@`. The drafting session had
     already fixed this by hand in the committed file and was right to.
  4. `fingerprint.py --check` reported DATA CHANGED on a fresh clone just because an
     excluded file was absent. A warning that cries wolf gets ignored; it now
     distinguishes "excluded by design" from "actually changed".
- **Still open, needs Aditya:** the 8 steering/MD refs are non-citable by construction
  in `paper_tex/refs.bib`, while `lit/CLAUDE.md` calls them "citable for venue and
  identifier only". Pick one; correct the loser.
- TODO next: decide whether `data/predictions.csv` (6.9M) and
  `report/predictions_minimal.csv` (8.0M) — 74% of the repo — need to travel at all.

## 2026-09-08 20:46  ·  MacBook-Pro-3

Set up the two-machine handoff. Before this, work was single-machine.

- Built `lit/` corpus (66 papers), `CLAIMS.md`, `RESULTS.md`, `analysis/`, Overleaf clone.
- Overleaf push verified end to end: clean compile, 9 bibitems, 0 undefined citations.
- **Open decision:** the 8 steering/MD refs added 2026-09-08 are commented out in
  `paper_tex/refs.bib` (citing one fails), but `lit/CLAUDE.md` says they are
  "citable for venue and identifier only". Those conflict. Resolve before drafting.
- TODO for next session: pick a side on that, then `git init` + private remote.
