#!/usr/bin/env python3
"""Resolve every panel receptor to its ChEMBL SINGLE PROTEIN target.

This is deliverable 1's prerequisite and the only part of the decoy extraction
that does not need a pinned ChEMBL dump: target identifiers are metadata, they are
stable across releases, and the API reports which release answered.  The ACTIVITY
extraction is the part that needs the pin, and drule_pool.py refuses to run
without one.

DRULE_CHEMBL_SCOPE.md's rules, applied here:
  target mapping   UniProt accession -> ChEMBL target, SINGLE PROTEIN only.
                   Never slug or gene symbol: those collide across species and the
                   panel carries three non-human receptors.
  species          recorded, never filtered.

    python3 redo/build/drule_targets.py
    python3 redo/build/drule_targets.py --refresh
    python3 redo/build/manifest.py

Writes: inputs/drule_targets.tsv, and caches the raw responses.
"""

import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, CACHE  # noqa: E402

API = "https://www.ebi.ac.uk/chembl/api/data"
CACHE_FILE = os.path.join(CACHE, "drule_chembl_targets.json")
OUT = os.path.join(INPUTS, "drule_targets.tsv")


def get(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def main(argv):
    refresh = "--refresh" in argv
    cache = {}
    if os.path.exists(CACHE_FILE) and not refresh:
        cache = json.load(open(CACHE_FILE))

    status = cache.get("_status")
    if status is None:
        status = get(f"{API}/status.json")
        cache["_status"] = status
    release = status["chembl_db_version"]
    print(f"ChEMBL release answering: {release} ({status['chembl_release_date']}), "
          f"{status['activities']:,} activities, {status['targets']:,} targets")

    with open(os.path.join(INPUTS, "g1_receptors.tsv")) as fh:
        rec = list(csv.DictReader(fh, delimiter="\t"))

    rows, unresolved = [], []
    for r in rec:
        acc = r["uniprot"]
        if acc not in cache:
            q = urllib.parse.urlencode({
                "target_components__accession": acc,
                "target_type": "SINGLE PROTEIN",
                "limit": 20,
            })
            cache[acc] = get(f"{API}/target.json?{q}")
            time.sleep(0.12)
        hits = cache[acc].get("targets", [])
        if not hits:
            unresolved.append(r["slug"])
            rows.append({
                "receptor_slug": r["slug"], "uniprot": acc,
                "receptor_organism": r["organism"], "cluster": r["cluster"],
                "core32_provisional": r["core32_provisional"],
                "chembl_target_id": "", "chembl_pref_name": "",
                "chembl_organism": "", "n_targets_matched": 0,
                "chembl_release": release,
            })
            continue
        # More than one SINGLE PROTEIN target on one accession would be an
        # ambiguity we must not resolve silently; record the count either way.
        t = hits[0]
        rows.append({
            "receptor_slug": r["slug"], "uniprot": acc,
            "receptor_organism": r["organism"], "cluster": r["cluster"],
            "core32_provisional": r["core32_provisional"],
            "chembl_target_id": t["target_chembl_id"],
            "chembl_pref_name": t["pref_name"],
            "chembl_organism": t["organism"],
            "n_targets_matched": len(hits),
            "chembl_release": release,
        })

    os.makedirs(CACHE, exist_ok=True)
    json.dump(cache, open(CACHE_FILE, "w"), indent=1, sort_keys=True)

    cols = list(rows[0].keys())
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    ok = [r for r in rows if r["chembl_target_id"]]
    amb = [r for r in rows if r["n_targets_matched"] > 1]
    clusters = {r["cluster"] for r in rows}
    covered = {r["cluster"] for r in ok}
    print(f"wrote {os.path.relpath(OUT)}  ({len(rows)} rows)")
    print(f"  resolved   {len(ok)}/{len(rows)} receptors")
    print(f"  clusters   {len(covered)}/{len(clusters)} have at least one target")
    if amb:
        print(f"  AMBIGUOUS  {len(amb)}: " +
              ", ".join(f"{r['receptor_slug']}({r['n_targets_matched']})" for r in amb))
    if unresolved:
        print(f"  UNRESOLVED {len(unresolved)}: {', '.join(unresolved)}")
        print("             -- these receptors cannot have a ChEMBL-evidenced decoy;")
        print("                the absence is recorded, not silently dropped.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
