#!/usr/bin/env python3
"""Apply lee2026confornets' stated selection rule strictly, and reconcile against their 51.

Rule, verbatim (lee2026confornets p.15, App. D.1):
  "We selected GPCRs with both fully active (100 per cent activation degree) and inactive
   structures available. We selected pairs with the fewest engineered mutations and highest
   crystallographic resolution, retaining 51 pairs where both structures contained at most
   one mutation."

Two of its four criteria are NOT in lit/panels/cache/gpcrdb_structures.json:
  - activation degree  -> redo/inputs/panel_gpcrdb_degree.csv     (GPCRdb structure browser)
  - mutation count     -> redo/inputs/panel_gpcrdb_constructs.csv (GPCRdb construct browser)
Both companions were scraped from gpcrdb.org on 2026-09-11 and validated against the cached
snapshot: same 1,716 PDB entries, zero state disagreements.

Writes redo/inputs/panel_strict_confornets.csv and prints the reconciliation.
"""
import csv, json, collections, os, sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo


P = lambda p: os.path.join(ROOT, p)

S = json.load(open(P('lit/panels/cache/gpcrdb_structures.json')))
DEG = {r['pdb'].upper(): r for r in csv.DictReader(open(P('redo/inputs/panel_gpcrdb_degree.csv')))}
MUT = {r['pdb'].upper(): r for r in csv.DictReader(open(P('redo/inputs/panel_gpcrdb_constructs.csv')))}

MISSING = []
def degree(pdb):
    v = DEG.get(pdb.upper(), {}).get('degree_active', '-')
    try:
        return float(v)
    except ValueError:
        return None                       # '-' : GPCRdb publishes no degree

def nmut(pdb):
    v = MUT.get(pdb.upper(), {}).get('mutations', '')
    try:
        return int(v)
    except ValueError:
        MISSING.append(pdb)               # never infer; never silently pass
        return None

CAP = 1
byprot = collections.defaultdict(list)
for e in S:
    byprot[e['protein']].append(e)

def sortkey(e):
    return (nmut(e['pdb_code']), e['resolution'] if e['resolution'] is not None else 99.9,
            e['publication_date'] or '9999')

rows, unresolved = [], []
for prot, ent in byprot.items():
    act = [e for e in ent if e['state'] == 'Active' and degree(e['pdb_code']) == 100.0]
    ina = [e for e in ent if e['state'] == 'Inactive']
    if not act or not ina:
        continue                                   # criterion (i)+(ii)
    act_ok = [e for e in act if nmut(e['pdb_code']) is not None and nmut(e['pdb_code']) <= CAP]
    ina_ok = [e for e in ina if nmut(e['pdb_code']) is not None and nmut(e['pdb_code']) <= CAP]
    act_unk = [e for e in act if nmut(e['pdb_code']) is None]
    ina_unk = [e for e in ina if nmut(e['pdb_code']) is None]
    if not act_ok or not ina_ok:
        status = 'UNRESOLVED' if (act_unk and not act_ok) or (ina_unk and not ina_ok) else 'FAILS_CAP'
        unresolved.append((prot, status,
                           min([nmut(e['pdb_code']) for e in act if nmut(e['pdb_code']) is not None], default=None),
                           min([nmut(e['pdb_code']) for e in ina if nmut(e['pdb_code']) is not None], default=None)))
        continue
    a = sorted(act_ok, key=sortkey)[0]
    i = sorted(ina_ok, key=sortkey)[0]
    rows.append(dict(
        gpcrdb_protein=prot, slug=prot.split('_')[0].upper(),
        gpcr_class={'Class A (Rhodopsin)': 'A', 'Class B1 (Secretin)': 'B1', 'Class B2 (Adhesion)': 'B2',
                    'Class C (Glutamate)': 'C', 'Class F (Frizzled)': 'F'}.get(a['class'], a['class']),
        species=a['species'],
        active_pdb=a['pdb_code'], active_degree=degree(a['pdb_code']), active_nmut=nmut(a['pdb_code']),
        active_res=a['resolution'], active_method=a['type'], active_date=a['publication_date'],
        inactive_pdb=i['pdb_code'], inactive_degree=degree(i['pdb_code']), inactive_nmut=nmut(i['pdb_code']),
        inactive_res=i['resolution'], inactive_method=i['type'], inactive_date=i['publication_date'],
        n_active_qualifying=len(act_ok), n_inactive_qualifying=len(ina_ok)))

rows.sort(key=lambda r: r['slug'])
with open(P('redo/inputs/panel_strict_confornets.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

print(f"STRICT ConfoRNets rule, cap<={CAP}: {len(rows)} pairs")
print('  by class:', dict(collections.Counter(r['gpcr_class'] for r in rows)))
print('  Class A slugs:', len({r['slug'] for r in rows if r['gpcr_class'] == 'A'}))
print('  non-human:', sorted({(r['slug'], r['species']) for r in rows if r['species'] != 'Homo sapiens'}))
print(f"  receptors with both states but failing the cap: {len([u for u in unresolved if u[1]=='FAILS_CAP'])}")
print(f"  UNRESOLVED (no mutation count published): {len([u for u in unresolved if u[1]=='UNRESOLVED'])}")
if MISSING:
    print(f"  structures with no GPCRdb mutation count encountered: {len(set(MISSING))}")
print()
for cap in (0, 1, 2, 3, 5, 10**6):
    n = 0
    for prot, ent in byprot.items():
        act = [e for e in ent if e['state'] == 'Active' and degree(e['pdb_code']) == 100.0]
        ina = [e for e in ent if e['state'] == 'Inactive']
        ok = lambda lst: any(nmut(e['pdb_code']) is not None and nmut(e['pdb_code']) <= cap for e in lst)
        if act and ina and ok(act) and ok(ina):
            n += 1
    print(f"  cap<={cap if cap < 1000 else 'inf'}: {n} pairs")
