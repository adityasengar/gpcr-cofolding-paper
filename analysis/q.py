#!/usr/bin/env python3
"""Reproducible queries behind every number in RESULTS.md.

Each function is one ledger row. Run:  python3 analysis/q.py <name>
                                       python3 analysis/q.py --list
Nothing here reads STATUS.md or RESULTS.md — this file is the evidence, they are
the claims. If a query cannot answer, it says so rather than returning a number.
"""
import csv, sys, collections, statistics as st, os, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv.field_size_limit(10**9)

def load(name):
    p = os.path.join(ROOT, "data", name)
    with open(p, newline="", errors="ignore") as fh:
        return list(csv.DictReader(fh))

def f(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def sha(name):
    p = os.path.join(ROOT, "data", name)
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()[:16]

STATE = ("active", "inactive", "borderline")

# ---------------------------------------------------------------- queries

def scope():
    """What the local export covers. Run this before trusting any other number."""
    P = load("predictions.csv")
    print(f"data/predictions.csv sha256[:16] = {sha('predictions.csv')}")
    print(f"rows                      : {len(P)}")
    print(f"distinct receptors        : {len({r['receptor'] for r in P})}")
    print(f"distinct backbones        : {sorted({r['backbone'] for r in P})}")
    print(f"distinct partner_type     : {len({r['partner_type'] for r in P})}")
    print(f"distinct experiment_cluster: {len({r['experiment_cluster'] for r in P})}")
    unc = sum(1 for r in P if r['classified_state'].strip() not in STATE)
    print(f"rows with NO classified_state: {unc}  ({100*unc/len(P):.1f}%)")
    roots = {r['prediction_path'].split('/')[1] for r in P if r['prediction_path'].startswith('/')}
    print(f"prediction_path roots     : {sorted(roots)}  <- source of truth is off-machine")

def ladder():
    """Fraction active by partner_type. Block B's activation ladder."""
    P = load("predictions.csv")
    by = collections.defaultdict(lambda: [0, 0])
    for r in P:
        if r['classified_state'].strip() not in STATE: continue
        b = by[r['partner_type']]; b[0] += 1
        if r['classified_state'].strip() == "active": b[1] += 1
    print(f"{'partner_type':<20} {'n':>7} {'active':>7} {'%active':>9}")
    for k, (n, a) in sorted(by.items(), key=lambda kv: -kv[1][0]):
        print(f"{k:<20} {n:>7} {a:>7} {100*a/n:>8.1f}%")
    print("\nNOTE: denominators exclude rows with no classified_state (39% of the export).")

def receptor_counts():
    """Every defensible definition of 'how many receptors'. None gives 48."""
    R = {r["receptor_slug"]: r for r in load("receptors.csv")}
    P = load("predictions.csv")
    y = lambda r, c: r.get(c, "").strip().lower() == "yes"
    apo = {p['receptor'] for p in P if p['partner_type'] == 'apo'}
    cog = {p['receptor'] for p in P if p['partner_type'] == 'cognate_ga'}
    thr = {k for k, r in R.items() if y(r, "in_state_thresholds")}
    ref = {k for k, r in R.items() if y(r, "in_reference_set")}
    bk = collections.defaultdict(set)
    for p in P: bk[p['receptor']].add(p['backbone'])
    four = {r for r, b in bk.items() if len(b) >= 4}
    for label, s in [
        ("appear anywhere in predictions.csv", {p['receptor'] for p in P}),
        ("in_reference_set = yes", ref),
        ("in_state_thresholds = yes", thr),
        ("in both apo and cognate arms", apo & cog),
        ("... and in_reference_set", apo & cog & ref),
        ("... and in_state_thresholds", apo & cog & thr),
        ("run on >= 4 backbones", four),
        ("run on >= 4 backbones, both arms, thresholds", four & apo & cog & thr),
    ]:
        print(f"{len(s):>5}  {label}")
    print("\nSTATUS.md Block A says 48. No definition above yields 48, 46 or 40.")

def aa2ar():
    """The infrastructure claim. Reports the confound rather than hiding it."""
    R = {r["receptor_slug"]: r for r in load("receptors.csv")}
    aa = R.get("AA2AR", {})
    print("AA2AR reference values in data/receptors.csv:")
    for k in ("ref_pdb_active", "ref_pdb_inactive", "d_tm6_active", "in_state_thresholds"):
        print(f"   {k:<20} {aa.get(k,'') or '(EMPTY)'}")
    print("   -> no active reference locally, so 'within 0.6 A of active' is NOT computable here.\n")
    P = [r for r in load("predictions.csv") if r['receptor'] == 'AA2AR']
    print(f"{'backbone':<10} {'n':>6} {'med d_tm6':>10} {'mean pLDDT':>11}  partner mix")
    for b in sorted({p['backbone'] for p in P}):
        g = [p for p in P if p['backbone'] == b]
        ds = [f(p['d_tm6']) for p in g if f(p['d_tm6']) is not None]
        ps = [f(p['plddt_at_anchors_mean']) for p in g if f(p['plddt_at_anchors_mean']) is not None]
        mix = collections.Counter(p['partner_type'] for p in g).most_common(3)
        print(f"{b:<10} {len(g):>6} {st.median(ds):>10.2f} {sum(ps)/len(ps):>11.2f}  {mix}")
    print("\nCONFOUND: partner mixes differ by backbone (boltz is mostly cognate+ligand,")
    print("chai is apo-only, af2mm is ligand-only). Cross-backbone medians here are NOT")
    print("a like-for-like comparison. Do not cite them as one.")

def coverage():
    """Receptor x condition coverage — where the design is thin."""
    C = load("conditions.csv")
    by = collections.defaultdict(set)
    for c in C: by[c['partner_type']].add(c['receptor'])
    print(f"{'partner_type':<20} {'receptors':>10}")
    for k, v in sorted(by.items(), key=lambda kv: -len(kv[1])):
        print(f"{k:<20} {len(v):>10}")

QUERIES = {k: v for k, v in list(globals().items())
           if callable(v) and not k.startswith("_") and v.__module__ == "__main__"
           and k not in ("load", "f", "sha")}

if __name__ == "__main__":
    a = sys.argv[1:] 
    if not a or a[0] in ("--list", "-l", "-h", "--help"):
        print("queries:")
        for k, v in sorted(QUERIES.items()):
            print(f"  {k:<18} {(v.__doc__ or '').splitlines()[0]}")
        sys.exit(0)
    for name in a:
        if name not in QUERIES:
            print(f"unknown query: {name}", file=sys.stderr); sys.exit(1)
        print(f"===== {name} =====")
        QUERIES[name]()
        print()
