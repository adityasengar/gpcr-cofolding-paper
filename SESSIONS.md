# SESSIONS.md — handoff log

Newest first. Every session **ends** by running `./session_end.sh "summary"`, and
**starts** by running `./session_start.sh`.

Git records what changed; this file records *why*, and what the next session should
not redo.

**`test-laptop` below is not a real machine.** It was a throwaway clone used on
2026-09-08 to test the sync machinery. A second laptop was set up on 2026-09-09 and
abandoned the same day as more complexity than it was worth; entries mentioning two
machines describe a setup that no longer exists.

## 2026-09-09 07:50  ·  MacBook-Pro-3 (orchestrator)

Restructured for the corrected machine roles. Also made, and recorded, the exact mistake
the new guard exists to prevent.

- **Roles were inverted in the docs and are now fixed.** This laptop authors the
  manuscript and runs several sessions; the other laptop holds scripts/data and can
  compile. `data/` here is a copy; that machine wins on conflict.
- **`manuscript/` is now canonical**, in this repo, built by `./manuscript/build.sh`
  on either laptop. Overleaf demoted to an export target via `./publish_overleaf.sh`.
  This removes the two-remote bibliography drift entirely.
- **TeX pinned**: BasicTeX/TeX Live 2025, 355 packages, `tex/tex-packages.txt`.
  `latexmk` is missing on both machines and should be installed on both.

- **MISTAKE, for the record.** Commit `7e03642` is titled "Correct the machine roles;
  move LaTeX into the repo" but it also swept up another session's uncommitted work:
  5 new extractions (fksteering, conformix, tds, refining, discriminator) and
  `draft/intro.md`, a 319-line introduction citing 52 papers. Nothing was lost or
  corrupted, but that work is filed under a misleading message, so `git log` will not
  show when the intro or those extractions actually landed.
  Cause: `git add -A` while another session had work in progress. `.session-guard.sh`
  had already warned "18 uncommitted changes ... possibly another session's work" and
  it was ignored.
  **Rule from now on: on this laptop, stage explicit paths, never `git add -A`.**

- TODO next: install latexmk on both machines; set up the other laptop; decide whether
  `data/` should live here at all now that the other machine is canonical for it.

## 2026-09-08 21:01  ·  test-laptop

Relay test from a simulated second machine

- corpus drift categories: 1
- data: not on this machine (excluded from the repo): rows_enriched_v3_7.csv
- TODO for next session: (edit me before committing)

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
