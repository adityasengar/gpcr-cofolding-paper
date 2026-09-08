#!/usr/bin/env python3
"""Verify every quoted string in every note actually occurs in that paper's text."""
import re, os, glob, json, unicodedata

BASE = "/Users/aditya/Documents/tools/Novartis_projects/paper/lit"
MINLEN = 45          # ignore short fragments: they match by chance

def norm(s):
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’","'").replace("‘","'")
    s = s.replace("“",'"').replace("”",'"')
    s = s.replace("–","-").replace("—","-").replace("−","-")
    s = s.lower()
    s = re.sub(r"\[[^\]]{0,25}\]", "", s)   # drop [OCR corrections] and [4] citations
    s = re.sub(r"[^a-z0-9]+", "", s)        # collapse to alphanumerics only
    return s

# quoted strings: "..." and blockquote lines
QPAT = re.compile(r'"([^"\n]{%d,})"' % MINLEN)

rows, per_paper = [], {}
for note in sorted(glob.glob(f"{BASE}/notes/*.md")):
    key = os.path.basename(note)[:-3]
    txtf = f"{BASE}/validate/txt2/{key}.txt"
    if not os.path.exists(txtf): continue
    hay = norm(open(txtf, errors="ignore").read())
    body = open(note, errors="ignore").read()
    quotes = set()
    for m in QPAT.finditer(body):
        quotes.add(m.group(1).strip())
    for line in body.splitlines():                 # blockquotes
        if line.lstrip().startswith(">"):
            t = line.lstrip()[1:].strip().strip('"').strip("*").strip()
            if len(t) >= MINLEN: quotes.add(t)
    ok = miss = 0; missed = []
    for q in quotes:
        nq = norm(q)
        if len(nq) < 30: continue
        if nq in hay: ok += 1
        else:
            # try the longest contiguous 60% of the quote (handles elisions/joins)
            L = len(nq); w = int(L*0.6)
            found = any(nq[i:i+w] in hay for i in range(0, L-w+1, max(1,w//4)))
            if found: ok += 1
            else:
                miss += 1
                missed.append(q[:150])
    per_paper[key] = {"checked": ok+miss, "verified": ok, "unverified": miss,
                      "examples": missed[:3]}
    rows.append((key, ok+miss, ok, miss))

tot_c = sum(r[1] for r in rows); tot_ok = sum(r[2] for r in rows); tot_m = sum(r[3] for r in rows)
print(f"papers checked        : {len(rows)}")
print(f"quotes checked        : {tot_c}")
print(f"verified in source    : {tot_ok}  ({100*tot_ok/max(tot_c,1):.1f}%)")
print(f"NOT found in source   : {tot_m}  ({100*tot_m/max(tot_c,1):.1f}%)")
print()
worst = sorted(rows, key=lambda r: -r[3])[:12]
print("papers with most unverified quotes:")
for k,c,o,m in worst:
    if m: print(f"  {k:<30} {m:>3} of {c:>3} unverified")
json.dump(per_paper, open(f"{BASE}/validate/quote_report.json","w"), indent=1)
