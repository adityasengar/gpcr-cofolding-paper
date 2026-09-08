#!/usr/bin/env python3
"""Does a quote cited as (p.N) actually occur on page N?"""
import re,os,glob,json,unicodedata,subprocess,random
BASE="/Users/aditya/Documents/tools/Novartis_projects/paper/lit"
def n(s):
    s=unicodedata.normalize("NFKD",s)
    for a,b in [("’","'"),("“",'"'),("”",'"'),("–","-"),("—","-"),("−","-")]: s=s.replace(a,b)
    return re.sub(r"[^a-z0-9]+","",s.lower())
# quote followed within 80 chars by a (p N) cite
PAT=re.compile(r'"([^"\n]{50,})"[^"\n]{0,80}?\(?\bp{1,2}\.?\s?(\d{1,3})\b',re.I)
random.seed(11); results={"onpage":0,"offby1":0,"elsewhere":0,"notfound":0}; detail=[]
keys=sorted(os.path.basename(x)[:-3] for x in glob.glob(f"{BASE}/notes/*.md"))
for key in keys:
    pt=f"{BASE}/validate/pages/{key}.txt"
    if not os.path.exists(pt):
        os.makedirs(f"{BASE}/validate/pages",exist_ok=True)
        if key=="hilger2020gcgr": open(pt,"w").write(open(f"{BASE}/ocr/hilger2020gcgr.txt",errors="ignore").read())
        else: open(pt,"w").write(subprocess.run([f"{BASE}/pagetext.sh",key],capture_output=True,text=True).stdout)
    raw=open(pt,errors="ignore").read()
    pages={}
    for m in re.finditer(r"===== PAGE (\d+) of \d+ =====",raw):
        s=m.end(); e=raw.find("===== PAGE",s); pages[int(m.group(1))]=n(raw[s:e if e>0 else len(raw)])
    body=open(f"{BASE}/notes/{key}.md",errors="ignore").read()
    cands=[(q,int(p)) for q,p in PAT.findall(body)]
    random.shuffle(cands)
    for q,p in cands[:6]:                       # sample up to 6 per paper
        nq=n(re.sub(r'<[^>]{1,12}>|\*+','',q))
        if len(nq)<35: continue
        if p in pages and nq in pages[p]: results["onpage"]+=1
        elif any(pp in pages and nq in pages[pp] for pp in (p-1,p+1)): results["offby1"]+=1
        elif any(nq in v for v in pages.values()): results["elsewhere"]+=1; detail.append((key,p,q[:80]))
        else: results["notfound"]+=1
tot=sum(results.values())
print(f"quote+page pairs sampled : {tot}")
for k,lab in [("onpage","exact page correct"),("offby1","off by one page"),
              ("elsewhere","found, different page"),("notfound","not located in text layer")]:
    print(f"  {lab:<28} {results[k]:>4}  ({100*results[k]/max(tot,1):.1f}%)")
if detail:
    print("\nexamples cited to the wrong page:")
    for d in detail[:6]: print(f"  {d[0]} cites p{d[1]}: {d[2]}")
