#!/usr/bin/env python3
"""Recompute every checkable number in redo/spec/PANEL.md from source files.

Run from the repo root:  python3 redo/gates/panel_verify.py
Exits non-zero and names the failing claim on any disagreement.

Sources are the frozen snapshot + the drops; the two companion CSVs written by the
panel session are treated as derived and are themselves rechecked against the snapshot.
"""
import json, csv, collections, sys, os, hashlib

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo


P = lambda p: os.path.join(ROOT, p)
FAIL = []

def check(label, got, want):
    ok = got == want
    print(("  ok   " if ok else "  FAIL ") + f"{label}: got {got!r}, expected {want!r}")
    if not ok:
        FAIL.append(label)

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

print("== frozen inputs ==")
check("gpcrdb snapshot sha", sha(P('lit/panels/cache/gpcrdb_structures.json'))[:8], "77e0b077")
check("confornets csv sha", sha(P('lit/panels/si_tables/lee2026confornets_gpcr_references.csv'))[:8], "bd08abab")
check("blockb pinned refs sha", sha(P('data/block_b/09_references/reference_set.blockb_pinned.csv'))[:8], "6ee2cad8")

S = json.load(open(P('lit/panels/cache/gpcrdb_structures.json')))
AI = [e for e in S if e['state'] in ('Active', 'Inactive')]
A = [e for e in AI if e['class'].startswith('Class A')]

print("== §1 the universe ==")
check("snapshot entries", len(S), 1716)
check("Class A entries", len([e for e in S if e['class'].startswith('Class A')]), 1358)
check("Class A Active/Inactive", len(A), 1336)
check("Class A Intermediate", len([e for e in S if e['class'].startswith('Class A') and e['state'] == 'Intermediate']), 21)
prot = collections.defaultdict(set)
for e in A:
    prot[e['protein']].add(e['state'])
check("Class A proteins with A or I", len(prot), 199)
both66 = {p for p, s in prot.items() if len(s) == 2}
check("Class A both-state, species-strict", len(both66), 66)
check("...collapsed to slugs", len({p.split('_')[0] for p in both66}), 64)
slug = collections.defaultdict(set)
for e in A:
    slug[e['protein'].split('_')[0]].add(e['state'])
check("...slugs allowing cross-species", len({p for p, s in slug.items() if len(s) == 2}), 65)
check("...human only", len({p for p in both66 if p.endswith('_human')}), 61)
aprot = collections.defaultdict(set)
for e in AI:
    aprot[e['protein']].add(e['state'])
allboth = {p for p, s in aprot.items() if len(s) == 2}
check("all-class both-state, species-strict", len(allboth), 86)
check("...of which human", len([p for p in allboth if p.endswith('_human')]), 80)
check("q9wtk1 is guinea-pig LTB4R, inactive only",
      sorted({(e['pdb_code'], e['species'], e['state']) for e in S if e['protein'] == 'q9wtk1_cavpo'}),
      [('5X33', 'Cavia porcellus', 'Inactive')])
check("lt4r1_human has active structures",
      bool([e for e in S if e['protein'] == 'lt4r1_human' and e['state'] == 'Active']), True)

print("== §2 ConfoRNets overlap ==")
by_pdb = collections.defaultdict(list)
for e in S:
    by_pdb[e['pdb_code'].upper()].append(e)
cn = list(csv.DictReader(open(P('lit/panels/si_tables/lee2026confornets_gpcr_references.csv'))))
check("ConfoRNets pairs", len(cn), 51)
cn_prot, unresolved = set(), []
for r in cn:
    for col in ('pdbidchain_i', 'pdbidchain_j'):
        pdb = r[col].split('_')[0].upper()
        if pdb not in by_pdb:
            unresolved.append(pdb)          # fail loudly; never skip
        else:
            cn_prot.add(by_pdb[pdb][0]['protein'])
check("ConfoRNets PDBs unresolved in snapshot", unresolved, [])
check("ConfoRNets distinct GPCRdb proteins", len(cn_prot), 53)
ours = {r['uniprot'] for r in csv.DictReader(open(P('data/block_a/01_rows/block_a_rows.csv')))}
ours40 = {r['uniprot'] for r in csv.DictReader(open(P('data/block_a/01_rows/block_a_rows.csv'))) if r['gpcr_class'] == 'A'}
check("our panel size", len(ours), 48)
check("our Class A panel size", len(ours40), 40)
check("overlap, exact protein entry, vs our 48", len(cn_prot & ours), 29)
check("overlap, slug, vs our 48", len({p.split('_')[0] for p in cn_prot} & {p.split('_')[0] for p in ours}), 30)
check("overlap, slug, vs our 40 Class A", len({p.split('_')[0] for p in cn_prot} & {p.split('_')[0] for p in ours40}), 27)
check("the 29/30 difference is ADRB1 turkey",
      sorted(p for p in cn_prot if p.split('_')[0] in {q.split('_')[0] for q in ours} and p not in ours),
      ['adrb1_melga'])
cls = collections.Counter(by_pdb[r['pdbidchain_i'].split('_')[0].upper()][0]['class'] for r in cn)
check("ConfoRNets Class A test cases", cls['Class A (Rhodopsin)'], 46)
check("every one of our 40 Class A is both-state", ours40 - both66, set())

print("== §7 clusters ==")
fam = collections.defaultdict(collections.Counter)
for e in S:
    fam[e['protein'].split('_')[0]][e['family']] += 1
old = {r['receptor']: r['cluster_id'] for r in csv.DictReader(open(P('data/block_b/09_references/paralogy_clusters.csv')))}
check("current reconstructed map rows", len(old), 40)
check("current reconstructed map clusters", len(set(old.values())), 26)
rows = list(csv.DictReader(open(P('redo/inputs/panel_systems.csv'))))
core = [r for r in rows if 'C1' in r['tier'].split('|')]
check("core panel size", len(core), 64)
check("core clusters", len({r['cluster_gpcrdb_fam3'] for r in core}), 32)
check("core singleton clusters",
      sum(1 for v in collections.Counter(r['cluster_gpcrdb_fam3'] for r in core).values() if v == 1), 16)
check("clusters over our 40 under the new map",
      len({r['cluster_gpcrdb_fam3'] for r in core if r['in_our40A'] == '1'}), 23)
conflict = collections.defaultdict(set)
for r in rows:
    if r['paralog_cluster']:
        conflict['_'.join(fam[r['gpcrdb_slug']].most_common(1)[0][0].split('_')[:3])].add(r['paralog_cluster'])
check("families the current map splits",
      sorted(k for k, v in conflict.items() if len(v) > 1),
      ['001_001_003', '001_002_022', '001_003_002', '001_009_001'])

print("== §8 cutoffs ==")
check("post-Boltz-2 active", sorted(r['slug'] for r in core if r['active_post_boltz2'] == '1'),
      ['ADA1A', 'B1B1U5', 'CCR8', 'CXCR3', 'CXCR4', 'DRD4', 'GPR6', 'HRH2', 'HRH3', 'MCHR1', 'PD2R2', 'TA2R'])
check("both states post-Boltz-2", sorted(r['slug'] for r in core if r['both_post_boltz2'] == '1'),
      ['ADA1A', 'CCR8', 'CXCR3', 'GPR6', 'MCHR1'])
check("post-Protenix active", sum(1 for r in core if r['active_post_protenix'] == '1'), 32)
check("post-Chai active", sum(1 for r in core if r['active_post_chai'] == '1'), 42)
gp = {e['pdb_code'].upper(): e for e in S}
noG = sorted(r['slug'] for r in core if not ((gp[r['gdb_active'].upper()].get('signalling_protein') or {}).get('type')))
check("active refs GPCRdb records as G-protein complexes", len(core) - len(noG), 58)
check("active refs GPCRdb records no transducer for",
      noG, ['AA2AR', 'ADRB1', 'AGTR1', 'NTR1', 'OPRD', 'OPRM'])

print("== §9 axis coverage in the pinned reference set ==")
pin = list(csv.DictReader(open(P('data/block_b/09_references/reference_set.blockb_pinned.csv'))))
nz = lambda x: x not in ('', 'NaN', 'nan', 'None')
onpanel = {r['receptor'] for r in csv.DictReader(open(P('data/block_a/01_rows/block_a_rows.csv')))}
on = [r for r in pin if r['receptor_slug'] in onpanel]
off = [r for r in pin if r['receptor_slug'] not in onpanel]
check("pinned rows", len(pin), 162)
check("pinned rows with tilt axis", len([r for r in pin if nz(r['d_gpcrdb_tm6_tilt_ref'])]), 162)
check("pinned rows with NPxxY axis", len([r for r in pin if nz(r['d_npxxy_oh_ref'])]), 64)
check("off-panel rows with NPxxY axis", len([r for r in off if nz(r['d_npxxy_oh_ref'])]), 0)
check("on-panel rows", len(on), 93)
d = collections.defaultdict(set)
for r in pin:
    if nz(r['d_npxxy_oh_ref']) and nz(r['d_gpcrdb_tm6_tilt_ref']):
        d[r['receptor_slug']].add(r['role'])
check("receptors with both roles on both axes", len([k for k, v in d.items() if v == {'active', 'inactive'}]), 28)

print("== §10 ligands ==")
check("core with agonist and antagonist records",
      sum(1 for r in core if r['agonist_modalities'] and r['antagonist_modalities']), 57)
check("core with no antagonist record",
      sorted(r['slug'] for r in core if not r['antagonist_modalities']),
      ['APJ', 'FSHR', 'GPR52', 'LSHR', 'MTR1A', 'MTR1B'])
check("core with no agonist record", sorted(r['slug'] for r in core if not r['agonist_modalities']), ['GPR6'])
bc = collections.defaultdict(set)
for r in csv.DictReader(open(P('data/block_c/12_g4_off_site_census/g4_full_census_v2.csv'))):
    bc[r['receptor']].add(r['role'])
check("Block C receptors", len(bc), 36)
check("Block C with both agonist and antagonist",
      len([k for k, v in bc.items() if {'full_agonist', 'neutral_antagonist'} <= v]), 28)

print("== §11 membership deltas ==")
check("Class A receptors added", sorted(r['slug'] for r in core if r['in_our40A'] != '1'),
      ['5HT2A', 'ADA1A', 'C5AR1', 'CCR2', 'CCR6', 'CCR8', 'CXCR3', 'DRD4', 'GPR52', 'GPR6', 'HRH2',
       'MTR1A', 'MTR1B', 'NK1R', 'NTR1', 'OPRM', 'OXYR', 'PD2R2', 'PE2R4', 'S1PR1', 'S1PR5',
       'SSR2', 'TA2R', 'TSHR'])
proposed = {r['slug'] for r in rows if r['tier'] and 'X' not in r['tier'].split('|')}
cnr = [r for r in rows if r['in_confornets'] == '1']
check("ConfoRNets cases covered by the proposed panel", sum(1 for r in cnr if r['slug'] in proposed), 50)
check("ConfoRNets case not covered", [r['slug'] for r in cnr if r['slug'] not in proposed], ['ACM3'])
check("non-human core receptors",
      sorted((r['slug'], r['gdb_species_pair']) for r in core if r['gdb_species_pair'] != 'Homo sapiens'),
      [('B1B1U5', 'Hasarius adansoni'), ('OPRM', 'Mus musculus'), ('OPSD', 'Bos taurus')])
check("OPSD rule-R pair is still 4X1H / 7ZBC",
      [(r['gdb_active'], r['gdb_inactive']) for r in core if r['slug'] == 'OPSD'], [('4X1H', '7ZBC')])
check("class B1 both-state receptors",
      sorted(r['slug'] for r in rows if r['gpcr_class'] == 'B1'),
      ['CALRL', 'CRHR1', 'GCGR', 'GLP1R', 'PTH1R'])
check("FZD6 has no inactive structure",
      [e['state'] for e in S if e['protein'] == 'fzd6_human' and e['state'] == 'Inactive'], [])
check("GCGR maps to glr_human and not by lowercasing",
      sorted({r['gpcrdb_primary_protein'] for r in rows if r['slug'] == 'GCGR'}), ['glr_human'])
check("CRHR1 maps to crfr1_human", sorted({r['gpcrdb_primary_protein'] for r in rows if r['slug'] == 'CRHR1'}), ['crfr1_human'])
check("PE2R4 is in the core", 'PE2R4' in {r['slug'] for r in core}, True)

print("== §3 obsolete entry ==")
st = json.load(open(P('redo/cache/panel_rcsb_status.json')))
check("7EVW is REMOVED/OBS, replaced by 8YY8", st.get('7EVW'), ['REMOVED', 'OBS', '8YY8'])
check("no other reference candidate is non-current",
      sorted(k for k, v in st.items() if v[0] != 'CURRENT'), ['7EVW'])

print("== §14 strict-ConfoRNets filter columns ==")
DEG = {r['pdb'].upper(): r for r in csv.DictReader(open(P('redo/inputs/panel_gpcrdb_degree.csv')))}
MUT = {r['pdb'].upper(): r for r in csv.DictReader(open(P('redo/inputs/panel_gpcrdb_constructs.csv')))}
check("degree companion rows", len(DEG), 1716)
check("construct companion rows", len(MUT), 1716)
check("degree companion PDB set equals the snapshot's", DEG.keys() == {e['pdb_code'].upper() for e in S}, True)
check("construct companion PDB set equals the snapshot's", MUT.keys() == {e['pdb_code'].upper() for e in S}, True)
check("degree companion disagrees with the snapshot on no state label",
      [k for k in DEG if DEG[k]['state'] != next(e['state'] for e in S if e['pdb_code'].upper() == k)], [])
check("structures with a numeric activation degree", sum(1 for v in DEG.values() if v['degree_active'].replace('.', '', 1).isdigit()), 1591)
check("structures at degree exactly 100", sum(1 for v in DEG.values() if v['degree_active'] == '100'), 991)
check("structures with mutation count 0", sum(1 for v in MUT.values() if v['mutations'] == '0'), 1455)
check("structures with mutation count 1", sum(1 for v in MUT.values() if v['mutations'] == '1'), 95)
check("core passes_strict TRUE", sum(1 for r in core if r['passes_strict'] == 'TRUE'), 61)
check("core passes_strict FALSE", sorted(r['slug'] for r in core if r['passes_strict'] == 'FALSE'), ['ACM1', 'ADRB1', 'S1PR1'])
check("core passes_strict UNRESOLVED", [r['slug'] for r in core if r['passes_strict'] == 'UNRESOLVED'], [])
check("UNRESOLVED cells anywhere in the filter columns",
      [(r['slug'], c) for r in rows for c in ('ref_activation_degree', 'n_mut_active', 'n_mut_inactive') if r[c] == 'UNRESOLVED'], [])
check("rows carrying NO_REFERENCE rather than a value",
      sorted(r['slug'] for r in rows if r['ref_activation_degree'] == 'NO_REFERENCE'), ['ACM3', 'FZD6'])
check("core receptors that are ConfoRNets members", sum(1 for r in core if r['confornets_member'] == 'TRUE'), 45)
check("4BVN mutation count (ConfoRNets' ADRB1 inactive)", MUT['4BVN']['mutations'], '11')
check("human ADRB1 has no degree-100 active",
      sorted({DEG[e['pdb_code'].upper()]['degree_active'] for e in S if e['protein'] == 'adrb1_human' and e['state'] == 'Active'}), ['99'])
strict = list(csv.DictReader(open(P('redo/inputs/panel_strict_confornets.csv'))))
check("strict rule pairs", len(strict), 71)
check("strict rule Class A entries", sum(1 for r in strict if r['gpcr_class'] == 'A'), 62)


# ===========================================================================
# D-H, 2026-09-12.  Two checks that exist because PANEL.md contradicted itself
# about B1B1U5's active reference for two days and nothing noticed: §6.1's table
# said 9EPP, §6's prose said Rule 4 gives 9EPR, and the frozen artefacts followed
# the table.  Neither check is about B1B1U5 in particular.
# ===========================================================================
import re

def parse_c1():
    """PANEL.md §6.1 -> slug -> (active_pdb, inactive_pdb).

    Parsed HERE rather than read back from g1_receptors.tsv on purpose: a gate
    that checks the generator's own output against the generator's own input is
    not checking the document.
    """
    text = open(P('redo/spec/PANEL.md')).read().splitlines()
    start = next(i for i, l in enumerate(text) if l.startswith('## 6.1 Tier C1'))
    end = next(i for i, l in enumerate(text[start + 1:], start + 1) if l.startswith('## '))
    ref = re.compile(r'^\s*(\S+)\s+([0-9.]+)\s*Å')
    out = {}
    for line in text[start:end]:
        if not line.startswith('|'):
            continue
        f = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(f) < 12 or not f[0].isdigit():
            continue
        a, i = ref.match(f[6]), ref.match(f[7])
        out[f[1].replace('*', '').strip()] = (a.group(1) if a else '',
                                              i.group(1) if i else '')
    return out

C1REF = parse_c1()
check("§6.1 parses to 64 rows", len(C1REF), 64)

print("== D-H: the spider Gaq1 segment is derivable from RCSB alone ==")
# tejero2024opsin Methods p10 records human Gai1 337-354 replaced by jumping-spider
# Gaq1 (INSDC LC799818).  If applying RCSB's OWN pdbx_mutation record for 9EPP_2 to
# human Gai1 reproduces that segment byte for byte, the literature string is
# corroborated by the PDB entry and does not have to be taken on trust.  If it ever
# stops reproducing, one of the two sources moved and (e') must not be built.
SPIDER_SEG = "CAVKDTILQNNLKECNLV"
W0, W1 = 337, 354
_rs = list(csv.DictReader(open(P('redo/inputs/coupling_refstructures.csv'))))
_ga = [r for r in _rs if r['pdb'] == '9EPP' and r['kind'] == 'G-alpha']
check("9EPP has exactly one G-alpha entity", len(_ga), 1)
_gi1 = [r for r in csv.DictReader(open(P('redo/inputs/seq_rungs.tsv')), delimiter='\t')
        if r['family'] == 'Gi1' and r['rung'] == 'R7_full']
check("seq_rungs.tsv carries Gi1 R7_full", len(_gi1), 1)
if _ga and _gi1:
    _host = _gi1[0]['sequence']
    _win = list(_host[W0 - 1:W1])
    _inside = 0
    for _tok in filter(None, (t.strip() for t in _ga[0]['pdbx_mutation'].split(','))):
        _wt, _pos, _to = _tok[0], int(_tok[1:-1]), _tok[-1]
        if W0 <= _pos <= W1:
            _inside += 1
            _win[_pos - W0] = _to if _win[_pos - W0] == _wt else '?'
    check(f"9EPP_2 pdbx_mutation substitutions inside {W0}-{W1}", _inside, 8)
    check("...applied to human Gai1 they reproduce the spider Gaq1 segment",
          "".join(_win), SPIDER_SEG)
    check("the 3 residues before the spider window are HUMAN backbone "
          "(so no spider ct21 exists)", _host[W0 - 4:W0 - 1], _ga[0]['ct21'][:3])
    check("...and the deposited ct21 is exactly backbone + spider segment",
          _ga[0]['ct21'], _host[W0 - 4:W0 - 1] + SPIDER_SEG)

print("== §6 note: receptors with a non-canonical alpha5 tip on the rule-R active reference ==")
# PANEL.md §6 names this set in prose.  Prose drifts; the census does not.
_chim = sorted({r['slug'] for r in
                csv.DictReader(open(P('redo/inputs/g1_refchimera.tsv')), delimiter='\t')
                if r['is_rule_r_reference'] == 'active'})
_sec6 = open(P('redo/spec/PANEL.md')).read().split('## 6.1 Tier C1')[0]
_lists = [m.group(1).split() for m in
          re.finditer(r'^> `([A-Z0-9 ]+)`\s*$', _sec6, re.M)]
check("§6 carries exactly one blockquoted slug list", len(_lists), 1)
check("§6's named non-canonical-tip list equals g1_refchimera.tsv's",
      sorted(_lists[0]) if _lists else [], _chim)

print("== no spec document contradicts PANEL.md §6.1 on a reference ==")
# WHAT THIS CHECKS, AND WHAT IT DOES NOT.  It is not a general prose linter and it
# does not try to be: the spec tree is full of legitimate sentences naming an
# alternative reference -- ConfoRNets' pick, the strict rule's pick, our old pinned
# pair, a resolution-only pick.  Those are comparisons, and comparing is the point.
#
# What it catches is the ONE shape that produced D-H: a sentence that says OUR OWN
# Rule R selects a PDB entry, where that entry is not what §6.1's table says.  So a
# sentence is flagged only when all four hold --
#
#   (1) it names Rule R, or rule 3 / rule 4 by number (our rule, not someone else's);
#   (2) it uses a selection verb;
#   (3) it names a C1 receptor -- in the sentence or anywhere in its paragraph,
#       because "B1B1U5 ... Rule R selects X" is often split across sentences;
#   (4) it names a PDB entry OF THAT RECEPTOR that §6.1 does not select.
#
# The escape hatch is a visible marker on the paragraph, one of two:
#
#   {ref-history}  this paragraph RECORDS a superseded or rejected selection --
#                  what we used to pin, what a rule would have given.
#   {ref-alt}      this paragraph deliberately COMPARES our pick with another
#                  rule's -- ConfoRNets', the strict rule's, resolution-only.
#
# Both are greppable on purpose: an escape hatch nobody can see is one that
# swallows the check.  `grep -rn '{ref-history}\|{ref-alt}' redo/spec/` is the
# audit, and the count is printed every run so it stays visible if it grows.
MARKER = re.compile(r'\{ref-(history|alt)\}')
OURRULE = re.compile(r'\bRule[- ]R\b|\brule\s*[34]\b|\bRule\s*[34]\b|\bstep\s*[34]\b', re.I)
VERB = re.compile(r'\b(select(?:s|ed)?|pick(?:s|ed)?|promot(?:e|es|ed)|keep(?:s)?|kept'
                  r'|choos(?:e|es)|chose|resolv(?:e|es|ed)?\s+to|give(?:s)?|gave'
                  r'|take(?:s)?|took|overrid(?:e|es)|flip(?:s)?\s+to|settle(?:s)?\s+on'
                  r'|point(?:s)?\s+at|is the reference|reference is|updated to)\b', re.I)
PDBTOK = re.compile(r'\b([0-9][A-Za-z0-9]{3})\b')
BYREC = collections.defaultdict(set)
for _r in _rs:
    BYREC[_r['slug']].add(_r['pdb'].upper())
for _p, _d in DEG.items():
    if _d['receptor'] in C1REF:
        BYREC[_d['receptor']].add(_p)
SLUGRE = {s: re.compile(r'\b' + re.escape(s) + r'\b') for s in C1REF}

contradictions, marked = [], 0
for _fn in sorted(os.listdir(P('redo/spec'))):
    if not _fn.endswith('.md'):
        continue
    for _para in re.split(r'\n\s*\n', open(P('redo/spec/' + _fn)).read()):
        if not OURRULE.search(_para):
            continue
        _here = {s for s, rx in SLUGRE.items() if rx.search(_para)}
        if not _here:
            continue
        # Markdown prose is hard-wrapped, so a sentence routinely spans lines.
        # Flatten first -- splitting on newline was silently hiding every claim
        # whose subject and verb sat on different lines, which is most of them.
        for _sent in re.split(r'(?<=[.!?])\s+', " ".join(_para.split())):
            if not (OURRULE.search(_sent) and VERB.search(_sent)):
                continue
            _pdbs = {t.upper() for t in PDBTOK.findall(_sent)}
            for _slug in sorted(_here):
                _off = sorted((_pdbs & BYREC[_slug]) - set(C1REF[_slug]))
                if not _off:
                    continue
                if MARKER.search(_para):
                    marked += 1
                    continue
                contradictions.append(
                    f"{_fn}: {_slug} -> {_off} (§6.1 says {C1REF[_slug]}) :: "
                    + " ".join(_sent.split())[:100])
check("spec sentences claiming Rule R selects what §6.1 does not", contradictions, [])
print(f"  note   {marked} sentence(s) sit in paragraphs marked {{ref-history}} or {{ref-alt}} and "
      f"are read as record, not claim")

print()
if FAIL:
    print(f"FAILED {len(FAIL)} claim(s): " + "; ".join(FAIL))
    sys.exit(1)
print(f"All {len(FAIL) + sum(1 for _ in [0])} checks pass." if False else "All checks pass.")
