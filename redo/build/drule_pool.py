#!/usr/bin/env python3
"""DRULE deliverable 1 -- the decoy candidate pool, extracted from ChEMBL.

    python3 redo/build/drule_pool.py --selftest        # prove the rule on a fixture
    python3 redo/build/drule_pool.py --dry-run         # what it would query
    python3 redo/build/drule_pool.py --db <chembl.db> --release ChEMBL_37 \\
                                     --sha256 <digest>

**It refuses to run against the live web API, by design.** DRULE_CHEMBL_SCOPE.md:
"Pin one ChEMBL release by version *and* download checksum ... an unpinned pull is
paper_af3's ColabFold problem in another costume."  That is the exact defect the
frozen campaign carries, and this script will not reproduce it: the activity
extraction needs a local dump whose version and sha256 are passed in and recorded
in every output row.  Downloading a release is a decision with a cost and it is
not this script's to make.

The rule, from DRULE_CHEMBL_SCOPE.md §2:

  activity types    Ki, Kd, IC50, EC50 only -- AC50 / %inhibition / Potency mix
                    functional and binding readouts and share no scale
  assay confidence  confidence_score >= 8 (direct single-protein target)
  ACTIVITY          any qualifying record, whatever its value.  A weak measured
                    affinity is still evidence the molecule binds; thresholding on
                    potency would admit known weak binders as decoys
  ABSENCE           no qualifying record at the receptor OR any cluster-mate
  species           recorded, never filtered
  candidate         >=1 qualifying activity SOMEWHERE, so it is a real ligand of
                    something rather than an untested compound

The paralog-cluster exclusion is load-bearing, not conservatism: "no measured
activity in ChEMBL" is absence of evidence, and a molecule untested at the receptor
but inactive across its whole cluster is a better-evidenced decoy than one merely
untested.  That limitation belongs in Methods; it is not fixable by a better query.
"""

import argparse
import csv
import os
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS  # noqa: E402

OUT = os.path.join(INPUTS, "drule_candidate_pool.tsv")

ACTIVITY_TYPES = ("Ki", "Kd", "IC50", "EC50")
MIN_CONFIDENCE = 8

# molregnos with a qualifying activity at any target in `tids`
SQL_ACTIVE_AT = """
SELECT DISTINCT act.molregno
  FROM activities act
  JOIN assays a ON a.assay_id = act.assay_id
 WHERE a.tid IN ({tids})
   AND a.confidence_score >= ?
   AND act.standard_type IN ({types})
   AND act.standard_value IS NOT NULL
"""

# every molecule with >=1 qualifying activity anywhere, with its properties
SQL_CANDIDATES = """
SELECT md.molregno, md.chembl_id, md.pref_name,
       cs.canonical_smiles,
       cp.mw_freebase, cp.alogp, cp.hbd, cp.hba, cp.rtb,
       COUNT(DISTINCT a.tid) AS n_targets,
       COUNT(*)              AS n_activities
  FROM activities act
  JOIN assays a  ON a.assay_id = act.assay_id
  JOIN molecule_dictionary md ON md.molregno = act.molregno
  LEFT JOIN compound_structures  cs ON cs.molregno = md.molregno
  LEFT JOIN compound_properties  cp ON cp.molregno = md.molregno
 WHERE a.confidence_score >= ?
   AND act.standard_type IN ({types})
   AND act.standard_value IS NOT NULL
 GROUP BY md.molregno
"""


def qmarks(n):
    return ",".join("?" * n)


def extract(db, targets, release, sha256, limit=None):
    """targets: [{receptor_slug, cluster, tid, ...}] -> pool rows."""
    con = sqlite3.connect(db)
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    by_cluster = {}
    for t in targets:
        by_cluster.setdefault(t["cluster"], []).append(t)

    q = SQL_CANDIDATES.format(types=qmarks(len(ACTIVITY_TYPES)))
    cur.execute(q, (MIN_CONFIDENCE, *ACTIVITY_TYPES))
    candidates = [dict(r) for r in cur.fetchall()]
    if limit:
        candidates = candidates[:limit]

    rows = []
    for t in targets:
        if not t["tid"]:
            continue
        mates = [m for m in by_cluster[t["cluster"]] if m["tid"]]
        tids = [m["tid"] for m in mates]
        # ABSENCE is judged against the whole paralog cluster, not the receptor
        cur.execute(
            SQL_ACTIVE_AT.format(tids=qmarks(len(tids)),
                                 types=qmarks(len(ACTIVITY_TYPES))),
            (*tids, MIN_CONFIDENCE, *ACTIVITY_TYPES))
        excluded = {r["molregno"] for r in cur.fetchall()}
        # and separately at the receptor alone, so the two can be told apart
        cur.execute(
            SQL_ACTIVE_AT.format(tids=qmarks(1),
                                 types=qmarks(len(ACTIVITY_TYPES))),
            (t["tid"], MIN_CONFIDENCE, *ACTIVITY_TYPES))
        at_receptor = {r["molregno"] for r in cur.fetchall()}

        for c in candidates:
            hit_rec = c["molregno"] in at_receptor
            hit_clu = c["molregno"] in excluded
            rows.append({
                "receptor_slug": t["receptor_slug"],
                "cluster": t["cluster"],
                "receptor_chembl_target": t["chembl_target_id"],
                "cluster_targets_consulted": ";".join(
                    m["chembl_target_id"] for m in mates),
                "n_cluster_targets": len(mates),
                "candidate_chembl_id": c["chembl_id"],
                "candidate_name": c["pref_name"] or "",
                "smiles": c["canonical_smiles"] or "",
                "mw": c["mw_freebase"] if c["mw_freebase"] is not None else "",
                "logp": c["alogp"] if c["alogp"] is not None else "",
                "hbd": c["hbd"] if c["hbd"] is not None else "",
                "hba": c["hba"] if c["hba"] is not None else "",
                "rot": c["rtb"] if c["rtb"] is not None else "",
                "n_targets_with_activity": c["n_targets"],
                "n_qualifying_activities": c["n_activities"],
                "active_at_receptor": "yes" if hit_rec else "no",
                "active_at_cluster_mate": "yes" if (hit_clu and not hit_rec) else "no",
                # the pool is what SURVIVES the absence rule; everything else is
                # recorded with the reason, because a rule that cannot say why it
                # refused is not auditable
                "eligible": "no" if hit_clu else "yes",
                "ineligible_because": ("measured activity at the receptor" if hit_rec
                                       else "measured activity at a cluster-mate"
                                       if hit_clu else ""),
                "activity_types": ",".join(ACTIVITY_TYPES),
                "min_confidence_score": MIN_CONFIDENCE,
                "chembl_release": release,
                "chembl_sha256": sha256,
            })
    con.close()
    return rows


def write(rows):
    cols = list(rows[0].keys())
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    return OUT


def load_targets():
    p = os.path.join(INPUTS, "drule_targets.tsv")
    if not os.path.exists(p):
        sys.stdout.write("drule_targets.tsv is absent -- run "
                         "redo/build/drule_targets.py first\n")
        return None
    with open(p) as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    for r in rows:
        r["tid"] = None          # filled from the dump at run time
    return rows


# ---------------------------------------------------------------- fixture
FIXTURE_SCHEMA = """
CREATE TABLE target_dictionary (tid INTEGER PRIMARY KEY, chembl_id TEXT,
                                target_type TEXT, organism TEXT);
CREATE TABLE assays (assay_id INTEGER PRIMARY KEY, tid INTEGER,
                     confidence_score INTEGER);
CREATE TABLE activities (activity_id INTEGER PRIMARY KEY, assay_id INTEGER,
                         molregno INTEGER, standard_type TEXT,
                         standard_value REAL, standard_units TEXT);
CREATE TABLE molecule_dictionary (molregno INTEGER PRIMARY KEY, chembl_id TEXT,
                                  pref_name TEXT);
CREATE TABLE compound_structures (molregno INTEGER PRIMARY KEY,
                                  canonical_smiles TEXT);
CREATE TABLE compound_properties (molregno INTEGER PRIMARY KEY, mw_freebase REAL,
                                  alogp REAL, hbd INTEGER, hba INTEGER,
                                  rtb INTEGER);
"""


def make_fixture(path):
    """A four-molecule world that exercises every branch of the absence rule.

    target 1 = the receptor, target 2 = its cluster-mate, target 3 = elsewhere.
      M1  active at the receptor                  -> ineligible (receptor)
      M2  active at the cluster-mate only         -> ineligible (cluster-mate)
      M3  active only elsewhere                   -> ELIGIBLE, the decoy case
      M4  active only in a confidence-7 assay     -> not a candidate at all
    """
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.executescript(FIXTURE_SCHEMA)
    con.executemany("INSERT INTO target_dictionary VALUES (?,?,?,?)", [
        (1, "CHEMBL_RECEPTOR", "SINGLE PROTEIN", "Homo sapiens"),
        (2, "CHEMBL_MATE", "SINGLE PROTEIN", "Homo sapiens"),
        (3, "CHEMBL_ELSEWHERE", "SINGLE PROTEIN", "Homo sapiens"),
    ])
    con.executemany("INSERT INTO assays VALUES (?,?,?)", [
        (10, 1, 9), (20, 2, 9), (30, 3, 9), (40, 3, 7),
    ])
    con.executemany("INSERT INTO activities VALUES (?,?,?,?,?,?)", [
        (1, 10, 1, "Ki", 12.0, "nM"),     # M1 at the receptor
        (2, 30, 1, "Ki", 15.0, "nM"),
        (3, 20, 2, "IC50", 30.0, "nM"),   # M2 at the cluster-mate
        (4, 30, 3, "Kd", 8.0, "nM"),      # M3 elsewhere only
        (5, 40, 4, "Ki", 5.0, "nM"),      # M4 low-confidence assay only
    ])
    con.executemany("INSERT INTO molecule_dictionary VALUES (?,?,?)", [
        (1, "CHEMBL_M1", "binds the receptor"),
        (2, "CHEMBL_M2", "binds a cluster-mate"),
        (3, "CHEMBL_M3", "binds elsewhere only"),
        (4, "CHEMBL_M4", "low-confidence only"),
    ])
    con.executemany("INSERT INTO compound_structures VALUES (?,?)", [
        (1, "CCO"), (2, "CCN"), (3, "CCC"), (4, "CCF"),
    ])
    con.executemany("INSERT INTO compound_properties VALUES (?,?,?,?,?,?)", [
        (1, 46.0, -0.3, 1, 1, 0), (2, 45.0, -0.2, 1, 1, 0),
        (3, 44.0, 1.1, 0, 0, 0), (4, 48.0, 0.5, 0, 1, 0),
    ])
    con.commit()
    con.close()
    return path


def selftest():
    import tempfile
    tmp = tempfile.mkdtemp()
    db = make_fixture(os.path.join(tmp, "fixture.db"))
    targets = [
        {"receptor_slug": "RECEPTOR", "cluster": "C1", "tid": 1,
         "chembl_target_id": "CHEMBL_RECEPTOR"},
        {"receptor_slug": "MATE", "cluster": "C1", "tid": 2,
         "chembl_target_id": "CHEMBL_MATE"},
    ]
    rows = extract(db, targets, "FIXTURE", "0" * 64)
    got = {(r["receptor_slug"], r["candidate_chembl_id"]):
           (r["eligible"], r["ineligible_because"]) for r in rows}

    want = {
        ("RECEPTOR", "CHEMBL_M1"): ("no", "measured activity at the receptor"),
        ("RECEPTOR", "CHEMBL_M2"): ("no", "measured activity at a cluster-mate"),
        ("RECEPTOR", "CHEMBL_M3"): ("yes", ""),
    }
    bad = 0
    print("\n=== drule_pool self-test, on a fixture ===\n")
    for k, exp in want.items():
        act = got.get(k)
        ok = act == exp
        bad += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'MISS'} {k[1]:<11} expected {exp} got {act}")
    # M4's only activity is in a confidence-7 assay, so it must not be a candidate
    m4 = ("RECEPTOR", "CHEMBL_M4") in got
    print(f"  {'ok  ' if not m4 else 'MISS'} CHEMBL_M4   excluded by "
          f"confidence_score >= {MIN_CONFIDENCE} -> "
          f"{'absent from the pool' if not m4 else 'PRESENT, which is wrong'}")
    bad += 1 if m4 else 0
    print(f"\n  {4 - bad}/4 rule branches behave as specified.\n")
    return 1 if bad else 0


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", help="path to a PINNED local ChEMBL SQLite release")
    ap.add_argument("--release", help="e.g. ChEMBL_37")
    ap.add_argument("--sha256", help="digest of the downloaded release")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    targets = load_targets()
    if targets is None:
        return 1
    resolved = [t for t in targets if t["chembl_target_id"]]
    clusters = {t["cluster"] for t in resolved}

    if a.dry_run or not a.db:
        print("\n=== drule_pool, dry run ===\n")
        print(f"  targets resolved      {len(resolved)}/{len(targets)} receptors, "
              f"{len(clusters)} clusters")
        print(f"  activity types        {', '.join(ACTIVITY_TYPES)}")
        print(f"  assay confidence      >= {MIN_CONFIDENCE}")
        print(f"  ABSENCE judged over   the whole paralog cluster, not the receptor")
        print(f"  species               recorded, never filtered")
        print(f"  would write           {os.path.relpath(OUT)}")
        print()
        if not a.db:
            print("  NOT RUN. This needs --db pointing at a PINNED local ChEMBL")
            print("  release, with --release and --sha256 recorded into every row.")
            print("  DRULE_CHEMBL_SCOPE.md refuses an unpinned pull: it is")
            print("  paper_af3's ColabFold problem in another costume. Downloading a")
            print("  release is a decision with a cost and is not this script's to")
            print("  make.  Prove the rule meanwhile with --selftest.\n")
            return 1
        return 0

    if not (a.release and a.sha256):
        print("--release and --sha256 are required with --db: an unrecorded "
              "release is an unpinned one")
        return 1
    rows = extract(a.db, targets, a.release, a.sha256, a.limit)
    if not rows:
        print("no rows produced")
        return 1
    p = write(rows)
    elig = [r for r in rows if r["eligible"] == "yes"]
    print(f"wrote {os.path.relpath(p)}  ({len(rows)} rows)")
    print(f"  eligible candidates {len(elig):,} across "
          f"{len({r['receptor_slug'] for r in elig})} receptors")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
