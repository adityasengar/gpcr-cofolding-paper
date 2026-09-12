#!/usr/bin/env python3
"""Add the strict-ConfoRNets filter columns to panel_systems.csv.

The panel is the relaxed 64 (PANEL.md Rule P). The strict question is a FILTER on that
one table, not a second list. UNRESOLVED is a first-class value everywhere: a missing
activation degree or a missing mutation count is never silently read as FALSE.
"""
import sys
import csv, json, collections, os

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo


P = lambda p: os.path.join(ROOT, p)
U = 'UNRESOLVED'

S = json.load(open(P('lit/panels/cache/gpcrdb_structures.json')))
DEG = {r['pdb'].upper(): r for r in csv.DictReader(open(P('redo/inputs/panel_gpcrdb_degree.csv')))}
MUT = {r['pdb'].upper(): r for r in csv.DictReader(open(P('redo/inputs/panel_gpcrdb_constructs.csv')))}
STRICT = {r['gpcrdb_protein']: r for r in csv.DictReader(open(P('redo/inputs/panel_strict_confornets.csv')))}

byprot = collections.defaultdict(list)
for e in S:
    byprot[e['protein']].append(e)

def deg(pdb):
    if not pdb:
        return 'NO_REFERENCE'          # Rule R selects no pair for this receptor
    if pdb.upper() not in DEG:
        return U
    v = DEG[pdb.upper()]['degree_active']
    try:
        return str(int(float(v)))
    except ValueError:
        return U                      # GPCRdb publishes '-' for 125 structures

def mut(pdb):
    if not pdb:
        return 'NO_REFERENCE'
    if pdb.upper() not in MUT:
        return U
    v = MUT[pdb.upper()]['mutations']
    return v if v.isdigit() else U

rows = list(csv.DictReader(open(P('redo/inputs/panel_systems.csv'))))
n_unres = collections.Counter()
for r in rows:
    prot = r['gpcrdb_primary_protein']
    r['confornets_member'] = 'TRUE' if r['in_confornets'] == '1' else 'FALSE'
    r['ref_activation_degree'] = deg(r['gdb_active'])
    r['n_mut_active'] = mut(r['gdb_active'])
    r['n_mut_inactive'] = mut(r['gdb_inactive'])
    for c in ('ref_activation_degree', 'n_mut_active', 'n_mut_inactive'):
        if r[c] == U:
            n_unres[c] += 1

    # passes_strict: does SOME pair for this protein entry satisfy the published rule?
    ent = byprot.get(prot, [])
    act = [e for e in ent if e['state'] == 'Active']
    ina = [e for e in ent if e['state'] == 'Inactive']
    if not act or not ina:
        r['passes_strict'] = 'FALSE'
        r['strict_active_pdb'] = r['strict_inactive_pdb'] = ''
        r['strict_fail_reason'] = 'no Active and Inactive for one UniProt entry'
    else:
        num = lambda v: v.isdigit()
        a_ok = [e for e in act if deg(e['pdb_code']) == '100' and num(mut(e['pdb_code'])) and int(mut(e['pdb_code'])) <= 1]
        i_ok = [e for e in ina if num(mut(e['pdb_code'])) and int(mut(e['pdb_code'])) <= 1]
        a_unk = [e for e in act if deg(e['pdb_code']) == U or mut(e['pdb_code']) == U]
        i_unk = [e for e in ina if mut(e['pdb_code']) == U]
        s = STRICT.get(prot)
        if a_ok and i_ok:
            r['passes_strict'] = 'TRUE'
            r['strict_active_pdb'] = s['active_pdb'] if s else sorted(a_ok, key=lambda e: (int(mut(e['pdb_code'])), e['resolution'] or 99))[0]['pdb_code']
            r['strict_inactive_pdb'] = s['inactive_pdb'] if s else sorted(i_ok, key=lambda e: (int(mut(e['pdb_code'])), e['resolution'] or 99))[0]['pdb_code']
            r['strict_fail_reason'] = ''
        elif (not a_ok and a_unk) or (not i_ok and i_unk):
            r['passes_strict'] = U      # never silently FALSE
            r['strict_active_pdb'] = r['strict_inactive_pdb'] = ''
            r['strict_fail_reason'] = 'a candidate structure has no published degree or mutation count'
            n_unres['passes_strict'] += 1
        else:
            r['passes_strict'] = 'FALSE'
            r['strict_active_pdb'] = r['strict_inactive_pdb'] = ''
            why = []
            if not a_ok:
                why.append('no Active with degree=100 and <=1 mutation')
            if not i_ok:
                why.append('no Inactive with <=1 mutation')
            r['strict_fail_reason'] = '; '.join(why)

with open(P('redo/inputs/panel_systems.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

core = [r for r in rows if 'C1' in r['tier'].split('|')]
print(f'panel_systems.csv now {len(rows[0])} columns')
print('core-64 passes_strict:', dict(collections.Counter(r['passes_strict'] for r in core)))
print('core-64 confornets_member:', dict(collections.Counter(r['confornets_member'] for r in core)))
print('UNRESOLVED cells across all 75 rows:', dict(n_unres) or 'none')
for r in core:
    if r['passes_strict'] != 'TRUE':
        print(f"  {r['slug']}: {r['passes_strict']} - {r['strict_fail_reason']}")
