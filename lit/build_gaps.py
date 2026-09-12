#!/usr/bin/env python3
"""
build_gaps.py — regenerate GAPS.md from the `unresolved` and `confidence` fields of every note.

GAPS.md was hand-built on 2026-09-08 against 66 notes and went stale immediately; by 2026-09-10 the
corpus was at 81 and the file still reported "358 items across 51 papers". A hand-built index of
what the corpus does not know is the last thing that should be hand-built. Run this after any
extraction.

    python3 build_gaps.py            # rewrite GAPS.md
    python3 build_gaps.py --check    # exit 1 if GAPS.md is out of date, print nothing else

Notes carry these fields in two shapes — a markdown table row `| `unresolved` | ... |` and a bullet
`- **unresolved**:` followed by an indented list. Both are handled; anything unparseable is counted
and named in the output rather than dropped, because a silently skipped note is exactly the failure
this file exists to prevent.
"""
import re, glob, os, sys, datetime

NOTES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "notes", "*.md")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GAPS.md")


def field(text, name):
    """Return the raw text of one schema field, table or bullet form."""
    m = re.search(r'^\|\s*\**`?' + name + r'`?\**\s*\|(.*?)\|\s*$', text, re.M)
    if m:
        return m.group(1).strip()
    m = re.search(r'^- \*\*`?' + name + r'`?\*\*:(.*?)(?=^- \*\*|^\#\#|\Z)', text, re.M | re.S)
    return m.group(1).strip() if m else ""


RESOLVED = re.compile(r'~~|\bRESOLVED\b', re.I)


def items(raw):
    """Split an unresolved field into individual items.

    Returns (open_items, resolved_count). Items already marked RESOLVED or struck through are
    NOT gaps and must not be counted as such — chiesa's Table S1 was closed on 2026-09-10 and a
    first version of this script still reported it as unknown.

    Bold markers are left intact: stripping only a leading ** leaves an orphan closing ** and
    breaks the rendered markdown.
    """
    if not raw:
        return [], 0
    out, resolved = [], 0
    for chunk in re.split(r'(?:^|\n)\s*(?:\d+\.|[-*])\s+', raw):
        c = " ".join(chunk.split()).strip()
        if len(c) <= 15:
            continue
        if RESOLVED.search(c):
            resolved += 1
            continue
        # balance bold markers rather than stripping one side
        if c.count("**") % 2:
            c += "**"
        out.append(c)
    if not out and not resolved and len(" ".join(raw.split())) > 15:
        out = [" ".join(raw.split())]
    return out, resolved


def build():
    rows, unparsed, total, closed = [], [], 0, 0
    for f in sorted(glob.glob(NOTES)):
        k = os.path.basename(f)[:-3]
        t = open(f).read()
        un, conf = field(t, "unresolved"), field(t, "confidence")
        its, res = items(un)
        closed += res
        if un and not its and not res:
            unparsed.append(k)
        total += len(its)
        rows.append((k, its, " ".join(conf.split())[:400]))
    return rows, unparsed, total, closed


def render(rows, unparsed, total, closed):
    with_items = [r for r in rows if r[1]]
    L = []
    L.append("# GAPS.md — what the corpus does not know\n")
    L.append(f"**Generated {datetime.date.today().isoformat()} by `build_gaps.py`** from the "
             f"`unresolved` and `confidence` fields of all {len(rows)} notes. "
             f"**{total} OPEN items across {len(with_items)} papers**"
             + (f"; {closed} further items are marked RESOLVED in their notes and are excluded.\n"
                if closed else ".\n"))
    L.append("Regenerate with `python3 build_gaps.py` after any extraction. `python3 build_gaps.py "
             "--check` exits non-zero when this file is stale — wire it into `corpus_check.sh` if "
             "it starts drifting again.\n")
    L.append("`UNRESOLVED.md` covers DOI resolution only, despite its name. This file covers the "
             "per-note `unresolved` field — the content `SCHEMA.md` says must never be silently "
             "dropped.\n")
    L.append("**Use it as a pre-citation check.** Before a draft sentence leans on a paper, look up "
             "that citekey below. If the thing you are about to claim appears here, the extraction "
             "could not determine it and the PDF has to be opened.\n")
    if unparsed:
        L.append(f"> **{len(unparsed)} notes have an `unresolved` field this script could not "
                 f"parse** and their items are NOT counted above: {', '.join(unparsed)}. "
                 f"Treat those as unknown-unknown, not as clean.\n")
    papers_clean = [r[0] for r in rows if not r[1]]
    L.append(f"> {len(papers_clean)} notes record no unresolved items. That is not the same as "
             f"having none — several are short notes where the extractor did not fill the field.\n")
    L.append("---\n")
    for k, its, conf in sorted(rows, key=lambda r: -len(r[1])):
        if not its:
            continue
        L.append(f"## `{k}` — {len(its)} item{'s' if len(its) != 1 else ''}\n")
        if conf:
            L.append(f"*confidence:* {conf}\n")
        for i in its:
            L.append(f"- {i}")
        L.append("")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    rows, unparsed, total, closed = build()
    text = render(rows, unparsed, total, closed)
    if "--check" in sys.argv:
        cur = open(OUT).read() if os.path.exists(OUT) else ""
        strip = lambda s: re.sub(r'\*\*Generated \d{4}-\d\d-\d\d.*?\n', '', s)
        sys.exit(0 if strip(cur) == strip(text) else 1)
    open(OUT, "w").write(text)
    print(f"GAPS.md: {total} open items across {len([r for r in rows if r[1]])} papers, "
          f"{closed} resolved excluded, {len(rows)} notes scanned, {len(unparsed)} unparseable")
