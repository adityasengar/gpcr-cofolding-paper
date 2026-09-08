# Extraction prompt template (schema v2)

Substitute <CITEKEY> and <NPAGES>. One paper per subagent. Never two.

---
You are extracting ONE paper into a structured note for a literature corpus. You are
not writing prose and nothing you produce is a draft of anything.

WORKING DIRECTORY: /Users/aditya/Documents/tools/Novartis_projects/paper/lit
THE PAPER: citekey `<CITEKEY>`, at `pdfs/<CITEKEY>.pdf` (<NPAGES> pages).

HOW TO READ IT: run `./pagetext.sh <CITEKEY>` from the lit directory. This emits the
full text with `===== PAGE n of N =====` markers so every quote carries a real page
number. Read the WHOLE paper before writing anything. For a figure whose caption is
genuinely insufficient to fill `data_shape`, render that page with
`pdftoppm -f <page> -l <page> -r 150 -png pdfs/<CITEKEY>.pdf /tmp/<CITEKEY>_p<page>`
and Read the PNG. Do this only where the caption truly does not carry the panel
structure; each render costs real tokens.

FIRST: read `SCHEMA.md`. It is version 3. Read the `data_shape` grammar section and
the Changelog carefully — v3 fixed defects that a previous extractor hit, and the
fixes only work if you follow them exactly.

THEN: write `notes/<CITEKEY>.md` with every field in SCHEMA.md, in schema order,
under headings A through G, ending with a Tags section.

RULES THAT MATTER MORE THAN COMPLETENESS:

1. Read only this paper. Do not fill any field from memory of the literature or from
   what a similar paper did. If you are writing something you know rather than
   something you just read, stop and write NOT REPORTED.
2. `NOT REPORTED` is correct and expected. A note with every field populated is more
   suspicious than one with gaps.
3. `oracle_leakage` is the most important field. Enumerate EVERY route separately,
   each with a verbatim quote and page: state-annotated databases (GPCRdb, KLIFS,
   Kincore) driving templates or alignments, deposited structures as input, cluster
   labels from known states, tuning against known states, success defined post hoc by
   RMSD to a held reference, best/worst labels assigned against it. If genuinely
   absent, write NONE FOUND plus the page where the protocol is described.
4. `necessity_claims` and `novelty_claims` are quoted VERBATIM with pages. Paraphrase
   softens exactly the sentences whose strength matters.
5. `data_shape` uses the v2 grammar. Choose PLOT, RENDER or SCHEMATIC and fill the
   named slots in order. `facet` is what splits sub-panels; `x` is what varies within
   a panel. If there is no faceting write `facet: none (1)`. One row per PANEL GROUP,
   not per figure — a figure with a bar panel and two scatters is two rows, `3A` and
   `3B-C`.
6. `hides` only when a figure obscures its own result: pooling, bars over
   distributions, pinned or broken axes, missing n, a claim with no quantitative
   panel. Blank otherwise.
7. `anti_memorization_design` and `_control` are separate. A held-out set existing is
   not a control arm being run. `NONE RUN` is a common, correct answer.
8. `stance` may hold two values joined by ` + ` (e.g. `precedent on findings +
   contrast on rigour`). Flag it as provisional; it is the user's call.
9. Tags ONLY from the fixed v2 vocabulary. If you need one that does not exist, do
   NOT invent it — record it under `unresolved` and report it.
10. Leave `why_it_matters` EMPTY. `schema_version` is `v3`. `extracted_on` is
    2026-09-07. `extractor` is "claude subagent".

REPORT BACK CONCISELY:
- Note path and size in characters.
- Fields filled vs. marked NOT REPORTED (both counts).
- What `oracle_leakage` came out as, in one line plus the single most revealing quote.
- Figures catalogued (count panel-group rows), and how many pages you had to render.
- Any tag you needed but could not use.
- Any point where the v2 schema or the data_shape grammar was still ambiguous. Be
  blunt; the schema is still being tuned.

Do not summarise the paper's findings. The note is the deliverable.

---

**STALENESS WARNING (added 2026-09-08).** The body of this file above was written for
schema v2 and still describes the v2 `data_shape` grammar with `x`/`y` slots and three
forms. **SCHEMA.md v3 supersedes it**: slots are named by role (`facet`/`vary`/`series`/
`measure`/`mark`/`n`), there are five forms (PLOT, MATRIX, RENDER, TREE, SCHEMATIC), and
the panel-split rule is split-on-mark-or-measure. Where this file and SCHEMA.md disagree,
**SCHEMA.md wins**. `BATCH_PROMPT.md` carries the current v3 summary.
