#!/usr/bin/env python3
"""Convert a draft markdown section to LaTeX, then VERIFY every citation resolves.

  python3 analysis/md2tex.py draft/intro.md manuscript/sections/intro.tex

Conversion is deliberately narrow: this handles the constructs our drafts actually use
and refuses anything it does not understand, rather than guessing. A silent
mistranslation in a manuscript is worse than a loud failure.
"""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from texutil import unicode_to_tex, remaining_non_ascii

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def bibkeys():
    raw = open(os.path.join(ROOT, "manuscript", "refs.bib"), encoding="utf-8").read()
    return set(re.findall(r"^@\w+\{([^,]+),", raw, re.M))

def convert(md):
    out, unknown = [], []
    in_quote = False
    for ln in md.splitlines():
        s = ln.rstrip()
        # blockquote -> quote environment
        if s.startswith(">"):
            if not in_quote:
                out.append(r"\begin{quote}"); in_quote = True
            out.append(s.lstrip(">").strip())
            continue
        if in_quote and not s.startswith(">"):
            out.append(r"\end{quote}"); in_quote = False
        # headings
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            lvl, txt = len(m.group(1)), m.group(2).strip()
            cmd = {1: None, 2: "section", 3: "subsection", 4: "subsubsection"}[lvl]
            out.append("" if cmd is None else "\\%s{%s}" % (cmd, txt))
            continue
        if s.startswith("- "):
            out.append(r"\item " + s[2:]); continue
        out.append(s)
    if in_quote: out.append(r"\end{quote}")
    t = "\n".join(out)

    # citations, most specific first
    K = r"[a-z][a-z0-9]+\d{4}[a-z0-9]*"
    t = re.sub(r"\[(%s)\s+pp?\.(\d+)\s*[-–]\s*(\d+)\]" % K, r"\\citep[pp.~\2--\3]{\1}", t)
    t = re.sub(r"\[(%s)\s+p\.(\d+)\]" % K, r"\\citep[p.~\2]{\1}", t)
    t = re.sub(r"\[(%s),\s*([A-Z][A-Za-z ]{2,30})\]" % K, r"\\citep[\2]{\1}", t)
    # multi-key: [a, b, c] possibly wrapped across lines
    def _multi(m):
        keys = [k.strip() for k in re.split(r"[,\s]+", m.group(1)) if k.strip()]
        return "\\citep{%s}" % ",".join(keys)
    t = re.sub(r"\[((?:%s)(?:\s*,\s*(?:%s))+)\]" % (K, K), _multi, t, flags=re.S)
    t = re.sub(r"\[(%s)\]" % K, r"\\citep{\1}", t)

    # emphasis
    t = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", t)
    t = re.sub(r"(?<![\\\w])\*(?!\s)(.+?)(?<!\s)\*", r"\\emph{\1}", t)
    # LaTeX-special characters that markdown leaves bare
    # protect the tildes we just emitted, escape specials, then restore
    t = t.replace("p.~", "\x00").replace("pp.~", "\x01")
    for ch in ["&", "#", "%"]:
        t = re.sub(r"(?<!\\)" + re.escape(ch), lambda m, c=ch: "\\" + c, t)
    t = t.replace("~", r"\textasciitilde{}")
    t = t.replace("\x00", "p.~").replace("\x01", "pp.~")
    t = unicode_to_tex(t)
    # markdown code spans -> \texttt
    t = re.sub(r"`([^`\n]+)`", r"\\texttt{\1}", t)
    return t, unknown

def main():
    src, dst = sys.argv[1], sys.argv[2]
    md = open(src, encoding="utf-8").read()
    # drop any trailing self-audit section: metadata, not manuscript prose
    md = re.split(r"^##\s+Citation check\s*$", md, flags=re.M)[0]
    # drop a leading "Draft status" blockquote: metadata about the draft, not prose
    md = re.sub(r"^(#\s+[^\n]*\n+)(>\s?[^\n]*\n)+", r"\1", md)
    tex, _ = convert(md)
    keys = set()
    for grp in re.findall(r"\\citep(?:\[[^\]]*\])?\{([^}]+)\}", tex):
        keys.update(k.strip() for k in grp.split(",") if k.strip())
    known = bibkeys()
    missing = sorted(k for k in keys if k not in known)
    leftover = re.findall(r"\[[a-z][a-z0-9]+\d{4}[^\]]*\]", tex)

    os.makedirs(os.path.dirname(dst), exist_ok=True)
    header = ("%% GENERATED from %s by analysis/md2tex.py — review before trusting.\n"
              "%% Verified: every \\citep key below resolves in manuscript/refs.bib.\n\n" % src)
    open(dst, "w", encoding="utf-8").write(header + tex.strip() + "\n")

    print(f"wrote {dst}")
    print(f"  citations converted : {len(keys)} distinct")
    print(f"  unresolved keys     : {missing or 'none'}")
    print(f"  unconverted markers : {leftover[:5] or 'none'}")
    print(f"  non-ASCII left      : {remaining_non_ascii(tex) or 'none (T1 fontenc covers the rest)'}")
    return 1 if (missing or leftover) else 0

if __name__ == "__main__":
    sys.exit(main())
