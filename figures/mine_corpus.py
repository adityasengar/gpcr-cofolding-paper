"""
mine_corpus.py — mechanical extraction of the literature corpus into flat CSVs.

Reads every note in ../lit/notes/*.md and writes, into figures/data_lit/:

    papers.csv    one row per paper, the A-E scalar fields
    figrows.csv   one row per panel-group row of every note's `## F. Figures`
                  table, with the data_shape form and slots split out
    metrics.csv   one row per `metrics_reported` row in `## E.`

Nothing here interprets a paper. It parses the note. Where a note says
NOT REPORTED that string is carried through verbatim, because "how many papers
never state their threshold" is the number several of these figures are about.

Three note dialects exist in the corpus and all three are handled:

    - **field**: value        (53 notes)
    | `field` | value |       (24 notes, A-section identity tables)
    - `field`: value          (1 note, bugrova2026representation)

Markdown table cells contain escaped pipes (\\|) inside data_shape strings, so
every table row is split on UNESCAPED pipes only. Splitting naively silently
shreds every data_shape in the corpus into fragments.

Run:  python3 mine_corpus.py
"""
from __future__ import print_function
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.join(HERE, "..", "lit", "notes")
OUT = os.path.join(HERE, "data_lit")

SECTION_RE = re.compile(r"^#{1,4}\s+([A-G])\.\s", re.M)

# --- table splitting --------------------------------------------------------

_UNESC_PIPE = re.compile(r"(?<!\\)\|")


def split_pipes(line):
    """Split a markdown table row on unescaped pipes; return trimmed cells."""
    parts = _UNESC_PIPE.split(line)
    if parts and not parts[0].strip():
        parts = parts[1:]
    if parts and not parts[-1].strip():
        parts = parts[:-1]
    return [p.strip() for p in parts]


def is_sep_row(cells):
    return bool(cells) and all(re.match(r"^:?-{2,}:?$", c) for c in cells)


# --- note structure ---------------------------------------------------------

def sections(text):
    """Split a note into its A-G sections. Returns {letter: body-text}."""
    out = {}
    marks = [(m.start(), m.group(1)) for m in SECTION_RE.finditer(text)]
    for i, (pos, letter) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(text)
        out[letter] = text[pos:end]
    return out


def _clean(v):
    v = v.strip()
    v = re.sub(r"\s+", " ", v)
    return v.strip()


def get_field(body, name):
    """
    Pull one schema field out of a section body, in any of the three dialects.
    Returns the raw value text (whitespace-collapsed), or '' if absent.
    """
    if not body:
        return ""
    lines = body.split("\n")

    # dialect 2/3: a table row `| `name` | value |` (or `| **name** | value |`)
    for ln in lines:
        if _UNESC_PIPE.search(ln):
            cells = split_pipes(ln)
            if len(cells) >= 2:
                head = cells[0].strip().strip("`*_ ")
                heads = [h.strip().strip("`*_ ").lower()
                         for h in head.split(",")]
                if name in heads:
                    return _clean(" | ".join(cells[1:]))

    # dialect 1: `- **name**: value`, continuing until the next field bullet.
    # Emphasis markers may be doubled (`- **`name`**:`) and the separator may be
    # a colon or an em dash, both of which occur in the corpus.
    pat = re.compile(
        r"^\s*[-*]?\s*[`*_ ]*" + re.escape(name) + r"[`*_ ]*\s*(?::|\u2014)", re.I)
    stop = re.compile(r"^\s*[-*]\s*[`*]{1,3}[a-z_]+[`*]{1,3}\s*(?::|\u2014)")
    for i, ln in enumerate(lines):
        if pat.match(ln):
            buf = [pat.sub("", ln, count=1)]
            for nxt in lines[i + 1:]:
                if stop.match(nxt) or SECTION_RE.match(nxt) or nxt.startswith("#"):
                    break
                if _UNESC_PIPE.search(nxt) and len(split_pipes(nxt)) >= 3:
                    break  # ran into a table
                buf.append(nxt)
            return _clean(" ".join(buf))

    # dialect 4: the field is its own sub-heading, `### `name``, with the value
    # in the prose beneath it until the next sub-heading.
    head = re.compile(r"^#{3,4}\s*[`*_ ]*" + re.escape(name) + r"[`*_ ]*\s*$", re.I)
    for i, ln in enumerate(lines):
        if head.match(ln):
            buf = []
            for nxt in lines[i + 1:]:
                if nxt.startswith("#"):
                    break
                buf.append(nxt)
            return _clean(" ".join(buf))
    return ""


# --- data_shape grammar -----------------------------------------------------

FORMS = ("PLOT", "MATRIX", "RENDER", "TREE", "SCHEMATIC")


def parse_shape(shape):
    """
    Split a `data_shape` string into its form and its `key: value` slots.
    Handles the v2 dialect (x/y/n_per_cell) as well as v3 (vary/measure/n).
    """
    s = shape.strip().strip("`").strip()
    form = ""
    for f in FORMS:
        if s.upper().startswith(f):
            form = f
            break
    slots = {}
    if form:
        rest = s[len(form):].lstrip()
        rest = rest.lstrip("|").strip()
    else:
        rest = s
    for chunk in _UNESC_PIPE.split(rest):
        chunk = chunk.strip()
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_ ]*)\s*:\s*(.*)$", chunk)
        if m:
            slots[m.group(1).strip().lower()] = m.group(2).strip()
    # normalise the v2 axis names onto the v3 roles
    if "vary" not in slots and "x" in slots:
        slots["vary"] = slots["x"]
    if "measure" not in slots and "y" in slots:
        slots["measure"] = slots["y"]
    if "n" not in slots and "n_per_cell" in slots:
        slots["n"] = slots["n_per_cell"]
    if "views" not in slots and "systems" in slots:
        slots["facet"] = slots.get("facet", slots["systems"])
    return form, slots


# --- figure table -----------------------------------------------------------

FIG_HEADERS = ("fig_no", "page", "gist", "plot_type", "data_shape",
               "panels", "hides", "reuse")


def parse_fig_table(body):
    """Return a list of dicts, one per panel-group row of the `## F.` table."""
    rows = []
    header = None
    for ln in body.split("\n"):
        if not _UNESC_PIPE.search(ln):
            header = None
            continue
        cells = split_pipes(ln)
        if is_sep_row(cells):
            continue
        low = [c.lower().strip("`* ") for c in cells]
        if "fig_no" in low and "data_shape" in low:
            header = low
            continue
        if header is None or len(cells) < 3:
            continue
        row = {}
        for k, v in zip(header, cells):
            row[k] = v
        if row.get("fig_no", "").lower().strip("`* ") in ("fig_no", ""):
            continue
        rows.append(row)
    return rows


def parse_metrics_table(body):
    """Rows of the `metrics_reported` table in section E."""
    rows = []
    header = None
    for ln in body.split("\n"):
        if not _UNESC_PIPE.search(ln):
            continue
        cells = split_pipes(ln)
        if is_sep_row(cells):
            continue
        low = [c.lower().strip("`* ") for c in cells]
        if "metric" in low and "value" in low:
            header = low
            continue
        if header is None or len(cells) < 3:
            continue
        rows.append(dict(zip(header, cells)))
    return rows


# --- per-paper scalar fields ------------------------------------------------

PAPER_FIELDS = [
    ("A", "citekey"), ("A", "year"), ("A", "venue"), ("A", "title"),
    ("B", "system"), ("B", "n_targets"), ("B", "method_class"),
    ("B", "backbones"), ("B", "templates"), ("B", "msa_handling"),
    ("C", "states_generated"), ("C", "structural_priors_used"),
    ("C", "oracle_leakage"), ("C", "prospective"), ("C", "state_metric"),
    ("C", "metric_saturation"), ("C", "directional_control"),
    ("C", "anti_memorization_design"), ("C", "anti_memorization_control"),
    ("C", "confidence_as_discriminator"),
    ("D", "stance"),
    ("E", "n_predictions"), ("E", "si_in_scope"),
    ("G", "schema_version"),
]


def main():
    if not os.path.isdir(NOTES):
        sys.exit("no notes directory at %s" % NOTES)
    os.makedirs(OUT, exist_ok=True)
    names = sorted(f for f in os.listdir(NOTES) if f.endswith(".md"))

    papers, figrows, metrics = [], [], []
    for fn in names:
        key = fn[:-3]
        with open(os.path.join(NOTES, fn)) as fh:
            text = fh.read()
        sec = sections(text)

        rec = {"citekey_file": key}
        for letter, field in PAPER_FIELDS:
            rec[field] = get_field(sec.get(letter, ""), field)
        # NOTE: tags are deliberately NOT read from the notes. The notes
        # discuss tagging decisions in prose ("Do not tag `msa-state-filter`",
        # "tags needed but not in the v3 vocabulary") and carry no single
        # consolidated tags line; a regex over them returns those sentences.
        # The consolidated per-paper tag set lives on the `tags:` line of
        # lit/INDEX.md and is read there, by classify_corpus.py.
        papers.append(rec)

        for r in parse_fig_table(sec.get("F", "")):
            form, slots = parse_shape(r.get("data_shape", ""))
            figrows.append({
                "citekey": key,
                "fig_no": r.get("fig_no", ""),
                "page": r.get("page", ""),
                "gist": r.get("gist", ""),
                "plot_type": r.get("plot_type", ""),
                "data_shape": r.get("data_shape", ""),
                "form": form,
                "slot_facet": slots.get("facet", ""),
                "slot_vary": slots.get("vary", ""),
                "slot_series": slots.get("series", ""),
                "slot_measure": slots.get("measure", ""),
                "slot_mark": slots.get("mark", ""),
                "slot_n": slots.get("n", ""),
                "slot_rows": slots.get("rows", ""),
                "slot_cols": slots.get("cols", ""),
                "slot_value": slots.get("value", ""),
                "slot_views": slots.get("views", ""),
                "slot_overlay": slots.get("overlay", ""),
                "panels": r.get("panels", ""),
                "hides": r.get("hides", ""),
                "reuse": r.get("reuse", ""),
            })

        for r in parse_metrics_table(sec.get("E", "")):
            metrics.append({
                "citekey": key,
                "metric": r.get("metric", ""),
                "value": r.get("value", ""),
                "units": r.get("units", ""),
                "measured_against": r.get("measured against",
                                          r.get("measured_against", "")),
                "page": r.get("page", ""),
            })

    def dump(name, rows, cols):
        p = os.path.join(OUT, name)
        with open(p, "w") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow(r)
        print("%-14s %5d rows -> %s" % (name, len(rows), p))

    dump("papers.csv", papers,
         ["citekey_file"] + [f for _, f in PAPER_FIELDS])
    dump("figrows.csv", figrows, list(figrows[0].keys()))
    dump("metrics.csv", metrics,
         ["citekey", "metric", "value", "units", "measured_against", "page"])

    print("\npapers parsed: %d" % len(papers))
    missing = {}
    for _, f in PAPER_FIELDS:
        n = sum(1 for r in papers if not r[f])
        if n:
            missing[f] = n
    if missing:
        print("fields empty for some papers (dialect misses or genuinely absent):")
        for k, v in sorted(missing.items(), key=lambda kv: -kv[1]):
            print("   %-28s %d" % (k, v))
    print("figure rows: %d over %d papers"
          % (len(figrows), len(set(r["citekey"] for r in figrows))))
    print("metric rows: %d over %d papers"
          % (len(metrics), len(set(r["citekey"] for r in metrics))))


if __name__ == "__main__":
    main()
