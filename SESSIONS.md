# SESSIONS.md — handoff log

Newest first. Every session **ends** by running `./session_end.sh "summary"`, and
**starts** by running `./session_start.sh`.

Git records what changed; this file records *why*, and what the next session should
not redo. Two machines, never concurrent — so this is a relay baton, not a merge.

## 2026-09-08 20:46  ·  MacBook-Pro-3

Set up the two-machine handoff. Before this, work was single-machine.

- Built `lit/` corpus (66 papers), `CLAIMS.md`, `RESULTS.md`, `analysis/`, Overleaf clone.
- Overleaf push verified end to end: clean compile, 9 bibitems, 0 undefined citations.
- **Open decision:** the 8 steering/MD refs added 2026-09-08 are commented out in
  `paper_tex/refs.bib` (citing one fails), but `lit/CLAUDE.md` says they are
  "citable for venue and identifier only". Those conflict. Resolve before drafting.
- TODO for next session: pick a side on that, then `git init` + private remote.
