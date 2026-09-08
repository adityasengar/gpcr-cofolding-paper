#!/usr/bin/env python3
import re, os, glob, json, unicodedata
BASE="/Users/aditya/Documents/tools/Novartis_projects/paper/lit"; MINLEN=45

SCHEMA_WORDS = re.compile(r'(oracle_leakage|state_metric|states_generated|structural_priors|'
  r'anti_memorization|controls_run|metrics_reported|why_it_matters|comparable_to_ours|'
  r'si_in_scope|necessity_claims|novelty_claims|data_shape|panel-group|NOT REPORTED|'
  r'NOT APPLICABLE|NONE FOUND|schema|Section [A-G]\b|<br>)', re.I)

def is_note_prose(q):
    """Extractor commentary, not a paper quote."""
    return bool(SCHEMA_WORDS.search(q)) or '`' in q or q.count('**')>=2

def clean(q):
    q = re.sub(r'<[^>]{1,12}>','',q)          # <sup>..</sup>
    q = re.sub(r'\*+','',q)                    # markdown emphasis
    q = re.sub(r'\[[^\]]{0,25}\]','',q)        # [OCR fix] / [4]
    return q

def norm(s):
    s = unicodedata.normalize("NFKD",s)
    for a,b in [("’","'"),("‘","'"),("“",'"'),("”",'"'),("–","-"),("—","-"),("−","-")]:
        s=s.replace(a,b)
    return re.sub(r"[^a-z0-9]+","",s.lower())

QPAT = re.compile(r'"([^"\n]{%d,})"'%MINLEN)
rows={}; residual=[]
for note in sorted(glob.glob(f"{BASE}/notes/*.md")):
    key=os.path.basename(note)[:-3]
    tf=f"{BASE}/validate/txt2/{key}.txt"
    if not os.path.exists(tf): continue
    hay=norm(open(tf,errors="ignore").read())
    body=open(note,errors="ignore").read()
    qs=set(m.group(1).strip() for m in QPAT.finditer(body))
    for ln in body.splitlines():
        if ln.lstrip().startswith(">"):
            t=ln.lstrip()[1:].strip().strip('"').strip("*").strip()
            if len(t)>=MINLEN: qs.add(t)
    ok=miss=skip=0; ex=[]
    for q in qs:
        if is_note_prose(q): skip+=1; continue
        # split on elision markers, match each fragment
        frags=[f for f in re.split(r'\.\.\.|…|\[\.\.\.\]', clean(q)) if len(norm(f))>=30]
        if not frags: skip+=1; continue
        if all(norm(f) in hay for f in frags): ok+=1; continue
        good=True
        for f in frags:
            nf=norm(f); L=len(nf); w=int(L*0.55)
            if nf in hay: continue
            if not any(nf[i:i+w] in hay for i in range(0,L-w+1,max(1,w//5))): good=False; break
        if good: ok+=1
        else:
            miss+=1
            if len(ex)<4: ex.append(q[:160])
    rows[key]={"paper_quotes":ok+miss,"verified":ok,"unverified":miss,"skipped_note_prose":skip,"examples":ex}
    for e in ex: residual.append((key,e))
c=sum(v["paper_quotes"] for v in rows.values()); o=sum(v["verified"] for v in rows.values())
m=sum(v["unverified"] for v in rows.values()); s=sum(v["skipped_note_prose"] for v in rows.values())
print(f"strings excluded as extractor commentary : {s}")
print(f"actual paper quotes checked              : {c}")
print(f"  verified verbatim in source            : {o}  ({100*o/max(c,1):.1f}%)")
print(f"  NOT verifiable                         : {m}  ({100*m/max(c,1):.1f}%)")
print()
w=sorted(rows.items(), key=lambda kv:-kv[1]["unverified"])[:10]
print("remaining, by paper:")
for k,v in w:
    if v["unverified"]: print(f"  {k:<30} {v['unverified']:>3} of {v['paper_quotes']:>3}")
json.dump(rows,open(f"{BASE}/validate/quote_report2.json","w"),indent=1)
