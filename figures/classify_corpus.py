"""
classify_corpus.py — turn the mined corpus into the flat tables the corpus
figures are drawn from. Run `mine_corpus.py` first.

Everything here is a rule applied to text the notes already wrote. No paper is
read, judged or summarised; the rules are keyword tests against vocabulary that
`lit/SCHEMA.md` itself fixes, so a reader can re-derive every count. Where a
rule cannot decide, the row is labelled `unclassified` and stays in the
denominator — dropping it would quietly improve every rate on the figures.

Writes into figures/data_lit/:

    tags.csv          citekey x tag, long form, from lit/INDEX.md (78 papers)
    metric_kinds.csv  which of the schema's four state-metric kinds each paper uses
    oracle_routes.csv the seven oracle_leakage routes x 78 papers, 4-level status
    antimem.csv       anti-memorization design class x control class per paper
    figdefects.csv    one row per panel group, with its defect classes

Run:  python3 classify_corpus.py
"""
from __future__ import print_function
import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "data_lit")
INDEX = os.path.join(HERE, "..", "lit", "INDEX.md")


def read(name):
    with open(os.path.join(OUT, name)) as fh:
        return list(csv.DictReader(fh))


def write(name, rows, cols):
    p = os.path.join(OUT, name)
    with open(p, "w") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print("%-18s %5d rows" % (name, len(rows)))


# ---------------------------------------------------------------- tags -----

def parse_index():
    """
    lit/INDEX.md is one block per paper with fixed line prefixes. Returns
    {citekey: {line-prefix: text}} for the prefixes this module needs.
    """
    blocks = {}
    key = None
    with open(INDEX) as fh:
        for ln in fh:
            m = re.match(r"^###\s+([A-Za-z0-9_]+)\s+—", ln)
            if m:
                key = m.group(1)
                blocks[key] = {}
                continue
            if key is None:
                continue
            m = re.match(r"^(claim|system/method|states|oracle|figs|tags|stance):\s*(.*)$", ln)
            if m:
                blocks[key][m.group(1)] = m.group(2).strip()
    return blocks


# --------------------------------------------------- state-metric kinds ----
# SCHEMA.md fixes the vocabulary for `state_metric`:
#   binary predicate / continuous coordinate / RMSD-to-reference / visual only
# and says the value may be dual (or, several notes found, triple). These
# patterns test for those exact phrases in the note's own field text.

METRIC_KINDS = [
    ("binary predicate",      r"binary[^.]{0,18}predicate"),
    ("continuous coordinate", r"continuous\s+(?:coordinate|metric)|"
                              r"\bcontinuous\b(?=[^.]{0,25}(?:only|:|coordinate))"),
    ("RMSD-to-reference",     r"rmsd[-\s]to[-\s]reference|\btm[-\s]to[-\s]reference|"
                              r"rmsd-only|deviation-from-reference"),
    ("visual only",           r"visual\s+only|visual\s*/|"
                              r"visual\b(?=[^.]{0,35}(?:component|call|metric|assignment|"
                              r"structural|pca))"),
]
# The field's opening verdict decides. A field that opens NOT APPLICABLE and
# then lists "the metrics that do appear, for completeness" still calls no
# conformational state, and those metrics must not be counted as state metrics.
NO_STATE = r"^\W*(not applicable|not reported|none\b)"
# "No binary predicate and no threshold is imposed" is not a use of a binary
# predicate. Reject a phrase match that is negated immediately before it.
NEGATED = re.compile(r"(?:\bno|\bnot|\bnever|\bnothing|\bwithout)\b[^.]{0,14}$", re.I)


def verdict_window(text):
    """
    The part of `state_metric` that states the schema value, as opposed to the
    per-arm detail beneath it. The notes put the value first and then break
    into ` - ` bullets; the bullets name metrics used for other objects
    (ligand pose, accuracy) that are not the paper's state call.
    """
    w = re.split(r"\s-\s", text)[0]
    parts = re.split(r"(?<=[.!?])(?=[\s*])", w)
    out = ""
    for part in parts[:3]:
        if out and len(out) + len(part) > 330:
            break
        out += part
    return out or w[:330]


def _kind_hits(txt):
    low = txt.lower()
    hits = {}
    for name, pat in METRIC_KINDS:
        found = 0
        for m in re.finditer(pat, low):
            if NEGATED.search(low[max(0, m.start() - 16):m.start()]):
                continue
            found = 1
            break
        hits[name] = found
    return hits


def classify_metrics(papers):
    rows = []
    for p in papers:
        txt = p["state_metric"]
        rec = {"citekey": p["citekey_file"]}
        if re.match(NO_STATE, txt.lower().lstrip("*`_ ")):
            hits = {n: 0 for n, _ in METRIC_KINDS}
            window = verdict_window(txt)
        else:
            window = verdict_window(txt)
            hits = _kind_hits(window)
            if not any(hits.values()):
                # the value was carried by the bullets, not the opening line
                window = txt[:700]
                hits = _kind_hits(window)
        rec.update(hits)
        n = sum(hits.values())
        rec["no state metric"] = 1 if n == 0 else 0
        rec["n_kinds"] = n
        rec["window"] = window[:300]
        rows.append(rec)
    return rows


# --------------------------------------------------- oracle-leak routes ----
# INDEX.md's `oracle:` line names which of SCHEMA.md's seven oracle_leakage
# routes fire, in clauses. A clause carrying a negation word describes routes
# that are clean; a clause without one describes routes that fire.

NEG = re.compile(r"clean|none found|not applicable|inapplicable|absent|"
                 r"no pipeline|\bnone\b|blind\b", re.I)
NOTDET = re.compile(r"not determinable|not reported|not extracted|"
                    r"under-specified|unstated|NOT EXTRACTED", re.I)
DESIGN = re.compile(r"design[- ]level|in kind|weakly|mild|benign|definitional", re.I)
PARTIAL = re.compile(r"partial", re.I)
ROUTE_RE = re.compile(r"\b(?:routes?|R)\s*([0-9][0-9,\s\-–and]*)", re.I)

# obendorf2026statespecific's index line says "six routes" with no numbers.
# Its note enumerates them 1-6 explicitly under `oracle_leakage`
# ("PRESENT - six distinct routes", routes numbered 1..6), so that is used.
INDEX_LINE_OVERRIDE = {
    "obendorf2026statespecific": "routes 1,2,3,4,5,6 present; route 7 design-level",
}


def _route_numbers(s):
    out = set()
    for chunk in re.split(r",|\band\b", s):
        chunk = chunk.strip()
        m = re.match(r"^([0-9])\s*[\-–]\s*([0-9])$", chunk)
        if m:
            for i in range(int(m.group(1)), int(m.group(2)) + 1):
                out.add(i)
            continue
        m = re.match(r"^([0-9])", chunk)
        if m:
            out.add(int(m.group(1)))
    return {i for i in out if 1 <= i <= 7}


def classify_oracle(blocks):
    rows = []
    for key in sorted(blocks):
        line = INDEX_LINE_OVERRIDE.get(key, blocks[key].get("oracle", ""))
        status = {i: "" for i in range(1, 8)}
        # split into clauses; an em dash or a semicolon starts a new statement
        clauses = re.split(r"[;—]|\s-\s|,\s*(?=(?:routes?\s*)?[0-9](?:\s*[,\-–][0-9])*\s+"
                           r"(?:partial|present|clean|design|only|none|absent|not\b))",
                           line)
        assigned = False
        for cl in clauses:
            nums = set()
            for m in ROUTE_RE.finditer(cl):
                nums |= _route_numbers(m.group(1))
            if not nums:
                if re.search(r"all seven routes|routes? 1\s*[\-–]\s*7", cl, re.I):
                    nums = set(range(1, 8))
                else:
                    continue
            pos = re.search(r"present|by design|by construction|severe|"
                            r"genuine|dominant|only\b", cl, re.I)
            if NOTDET.search(cl):
                verdict = "not stated"
            elif NEG.search(cl) and pos:
                verdict = "partial"          # named as firing in one arm, clean in another
            elif NEG.search(cl):
                verdict = "clean / not applicable"
            elif PARTIAL.search(cl):
                verdict = "partial"
            elif DESIGN.search(cl):
                verdict = "design-level only"
            else:
                verdict = "present"
            for i in nums:
                status[i] = verdict
                assigned = True
        if not assigned and NEG.search(clauses[0]):
            # e.g. "NONE FOUND - genuinely blind CASP15 submission"
            for i in range(1, 8):
                status[i] = "clean / not applicable"
        rec = {"citekey": key, "source_line": line}
        fired = 0
        for i in range(1, 8):
            v = status[i] or "unclassified"
            rec["route%d" % i] = v
            if v == "present":
                fired += 1
        rec["n_routes_present"] = fired
        rows.append(rec)
    return rows


# ------------------------------------------------- anti-memorization -------
# Both fields open with a verdict in the schema's own words. The tests are
# ordered: a field that says "split" or names both answers is `partial`,
# whatever else it goes on to say.

def _head(t, n):
    """The verdict, without the ` - ` detail bullets that follow it."""
    s = re.sub(r"[*`]", "", t).strip()
    s = re.split(r"\s-\s", s)[0]
    return s[:n].lower()


def _neg(head, word):
    """True where `word` occurs only in a negated position ('not UNPOWERED')."""
    for m in re.finditer(word, head):
        before = head[max(0, m.start() - 12):m.start()]
        if not re.search(r"\b(not|never|no)\b[^.]{0,8}$", before):
            return False
    return True


def _class_design(t):
    head = _head(t, 160)
    if not head:
        return "unclassified"
    if re.match(r"^\W*(none)\b", head):
        return "none"
    if "not applicable" in head[:45]:
        return "not applicable (nothing trained)"
    if re.match(r"^\W*(not extracted|not reported)", head):
        return "not reported"
    if re.match(r"^\W*(partial|present but|present in substance|two mechanisms|"
                r"held-out sets exist|one set exists|yes, but)", head):
        return "partial / weak"
    if re.match(r"^\W*(yes|present|this paper is|several|dual|held-out)", head):
        return "held-out or post-cutoff set exists"
    if re.search(r"held-out (set|split)s? (exist|are)|post-cutoff|temporal split|"
                 r"time split|entire construction|design centrepiece", head):
        return "held-out or post-cutoff set exists"
    return "unclassified"


def _class_control(t):
    head = _head(t, 150)
    if not head:
        return "unclassified"
    if "not applicable" in head[:45]:
        return "not applicable (nothing trained)"
    if re.match(r"^\W*(not extracted|not reported)", head):
        return "not reported"
    starts_run = bool(re.match(r"^\W*(run\b|control arms? (were |was )?(actually )?run|"
                               r"run and analysed)", head))
    says_none = bool(re.search(r"none run|not run|no held-out arm run", head)) \
        and not _neg(head, r"none run|not run|no held-out arm run")
    if re.match(r"^\W*(split answer|partial|two answers|partially run)", head):
        return "partial"
    if starts_run and says_none:
        return "partial"               # run in one arm, never run in another
    if re.match(r"^\W*(none run|no held-out arm run|none as|effectively none run|"
                r"none\b)", head):
        return "none run"
    if re.search(r"unpowered|invalid for this method", head) \
            and not _neg(head, "unpowered"):
        return "run but unpowered"
    if re.search(r"\brun\b|analysed|are the primary evaluation", head):
        return "run and analysed"
    return "unclassified"


def classify_antimem(papers):
    rows = []
    for p in papers:
        rows.append({
            "citekey": p["citekey_file"],
            "design_class": _class_design(p["anti_memorization_design"]),
            "control_class": _class_control(p["anti_memorization_control"]),
            "design_text": p["anti_memorization_design"][:300],
            "control_text": p["anti_memorization_control"][:300],
        })
    return rows


# ------------------------------------------------------ figure defects -----
# `hides` is filled only when a figure obscures its own result, so a blank
# cell means "no defect recorded". The blank markers actually used in the
# corpus are: empty, an em/en dash, and a parenthetical "(blank - why)".
#
# NOTE ON A DISCREPANCY: figures/README.md reports 189 of 232 render rows as
# carrying a defect; this rule gives 186, because three render rows whose
# `hides` cell reads "*(blank - <reason>)*" are blanks that a naive non-empty
# test counts as defects. 186/232 is the corrected number.

def is_blank_hides(h):
    s = h.strip().strip("*_ ").lower()
    if not s:
        return True
    if re.match(r"^[—–\-\s\.]*$", s):
        return True
    if s.startswith("(blank") or s.startswith("blank") or s == "none" \
            or s.startswith("n/a"):
        return True
    return False


# High-precision patterns for the defect classes the corpus survey named.
# A row may carry several. Rows matching none land in `other / uncategorised`,
# which is reported rather than dropped.
DEFECTS = [
    ("hand-picked or k-of-N example, rule unstated",
     r"hand-?pick|cherry-?pick|selected (successful )?example|representative|"
     r"selection (rule|criterion)[^.]{0,30}(un|not )stated|"
     r"no statement of how|\b\d[\d,]* of \d[\d,\s]*(are )?"
     r"(shown|plotted|displayed|clusters|channels)|single case study|"
     r"exemplars? stand for|chosen (to illustrate|as|from)|no criterion given|"
     r"showcase|illustrative example"),
    ("n or counts not shown",
     r"\bno n\b|\bn\b[^.]{0,12}not (printed|shown|stated|given|reported)|"
     r"no printed n|without (an? )?n\b|no counts?\b|"
     r"counts? (are )?not (shown|printed|given)|"
     r"number of \w+ (is )?not (stated|given|shown)|"
     r"not stated (on|in) the (panel|figure|caption)|no per-\w+ n\b|"
     r"n per (panel|mark|cell)[^.]{0,14}not|n is never|never stated"),
    ("axis broken, truncated or pinned",
     r"broken|truncat|axis (starts|begins) at|cut off at|clipped|pinned|"
     r"capped|tops out at|axis break"),
    ("axes not comparable across panels",
     r"different (x-|y-)?(axis|axes|scale|scales|range|ranges|colour-scale|"
     r"color-scale)|own (x-|y-)?(axis |colour |color )?ranges?|do not share|"
     r"independent (axes|y-axes|scales|colour)|twin (y-)?ax|"
     r"not on a common scale|different colour"),
    ("bar or mean standing in for a distribution",
     r"bars? (hide|over|stand)|hides? the (per-\w+ )?(distribution|spread)|"
     r"means? only|single (bar|value|point) per|no distribution|"
     r"distribution (is )?(not|never) shown|kernel density on"),
    ("no dispersion, error bar, CI or test",
     r"no (confidence interval|ci\b|error bars?|dispersion|test\b|p-value|"
     r"significance|summary statistic|statistic|spread)|"
     r"without (a )?(test|p-value|error bar|ci\b)|no measure of spread|"
     r"no effect size"),
    ("pooled where per-system was needed", r"pool"),
    ("two measures on one axis",
     r"two measures|twin (y-)?ax|different (measures|quantities|units) (share|on)|"
     r"share (a|one|the same) axis|same axis|two quantities"),
    ("claim with no quantitative panel",
     r"no quantitative|has no panel|not quantified|supported only by|"
     r"asserted (rather than|visually|from)|no (rmsd|numeric|number)\b|by eye"),
    ("oracle-selected model displayed",
     r"oracle|best-of-\d|best[- ]of[- ]n|lowest rmsd|closest structure|"
     r"best/?(and )?worst|selected by (pldd?t|rmsd|confidence|its own)|"
     r"chosen (against|by) the reference|post[- ]hoc"),
    ("failures not shown beside successes",
     r"only the (best|success|mutations that worked)|failures? (are )?not shown|"
     r"no (render|panel|example)[^.]{0,20}for the (two )?failures|"
     r"successes only|no failure (render|case|example)|"
     r"failure(s)? (is|are) (deferred|omitted|absent)"),
]


def classify_figrows(figrows):
    rows = []
    for r in figrows:
        blank = is_blank_hides(r["hides"])
        low = r["hides"].lower()
        rec = {"citekey": r["citekey"], "fig_no": r["fig_no"],
               "form": r["form"] or "unclassified",
               "plot_type": r["plot_type"],
               "has_defect": 0 if blank else 1}
        hit = 0
        for name, pat in DEFECTS:
            v = 0 if blank else (1 if re.search(pat, low) else 0)
            rec[name] = v
            hit += v
        rec["other / uncategorised"] = 1 if (not blank and hit == 0) else 0
        rec["hides"] = r["hides"][:300]
        rows.append(rec)
    return rows


def main():
    papers = read("papers.csv")
    figrows = read("figrows.csv")
    blocks = parse_index()
    print("index blocks parsed: %d" % len(blocks))

    tags = []
    for key in sorted(blocks):
        for t in blocks[key].get("tags", "").split():
            tags.append({"citekey": key, "tag": t})
    write("tags.csv", tags, ["citekey", "tag"])

    mk = classify_metrics(papers)
    write("metric_kinds.csv", mk,
          ["citekey"] + [n for n, _ in METRIC_KINDS] +
          ["no state metric", "n_kinds", "window"])

    orc = classify_oracle(blocks)
    write("oracle_routes.csv", orc,
          ["citekey"] + ["route%d" % i for i in range(1, 8)] +
          ["n_routes_present", "source_line"])

    am = classify_antimem(papers)
    write("antimem.csv", am,
          ["citekey", "design_class", "control_class",
           "design_text", "control_text"])

    fd = classify_figrows(figrows)
    write("figdefects.csv", fd,
          ["citekey", "fig_no", "form", "plot_type", "has_defect"] +
          [n for n, _ in DEFECTS] + ["other / uncategorised", "hides"])

    # ---- console audit, so the rules can be checked without opening the CSVs
    import collections
    print("\nunclassified oracle cells: %d of %d"
          % (sum(1 for r in orc for i in range(1, 8)
                 if r["route%d" % i] == "unclassified"), len(orc) * 7))
    print("unclassified antimem design : %s"
          % [r["citekey"] for r in am if r["design_class"] == "unclassified"])
    print("unclassified antimem control: %s"
          % [r["citekey"] for r in am if r["control_class"] == "unclassified"])
    print("papers with no state metric : %d"
          % sum(r["no state metric"] for r in mk))
    c = collections.Counter((r["form"], r["has_defect"]) for r in fd)
    for form in sorted(set(r["form"] for r in fd)):
        n = c[(form, 0)] + c[(form, 1)]
        print("  %-14s %3d of %3d rows carry a recorded defect"
              % (form, c[(form, 1)], n))


if __name__ == "__main__":
    main()
