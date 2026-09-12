#!/usr/bin/env python3
"""Is the predicate's own residue at 5.58 a tyrosine, receptor by receptor?

WHY.  The predicate's first axis is d(Y5.58 OH, Y7.53 OH) -- a HYDROXYL-to-
HYDROXYL distance, which exists only if both positions are tyrosine.  A 30-
structure pilot of the off-panel calibration set
(`redo/inputs/g0_pilot_measurements.csv`) refused 13 of 30, and 11 of those 13
refused for one reason: position 5.58 is not a tyrosine.  It came back ASN, HIS,
ALA, SER, PHE, CYS, ILE and GLN.

That is not a bug in the measurement -- the identity check is doing exactly what
`analysis/block_d/cifmeasure.py` designed it to do -- it is a fact about Class A.
Y5.58 is conserved in the branch our 48-receptor panel happens to sit in and is
not conserved across the class.  Since the whole point of E0.1 is to calibrate on
receptors the panel does NOT contain, this bears directly on whether E0.1 can be
run at all, and on what its population really is.

This script answers it WITHOUT DOWNLOADING A SINGLE COORDINATE FILE.  GPCRdb's
`residues/extended` endpoint returns the amino acid at every generic position, so
one call per receptor entry settles it for every structure of that receptor.

OUTPUT
  g0_anchor_conservation.csv   one row per GPCRdb Class A entry: the residue at
                               5.58, 7.53, 2x46 and 6x37, and whether the NPxxY
                               axis is measurable on it at all
  stdout                       the counts GROUP0_SYSTEMS.md sec.3.4 quotes

USAGE  python3 redo/build/g0_anchor_conservation.py
       python3 redo/build/g0_anchor_conservation.py --limit 20   (smoke test)
"""
from __future__ import annotations

import argparse
import collections
import csv
import os
import sys

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
ROOT = os.path.dirname(os.path.dirname(INPUTS))
sys.path.insert(0, INPUTS)

from g0_measure_axes import (  # noqa: E402
    Api, get_generic_numbers, lookup_bw, lookup_generic,
    NPXXY_BW, TILT_GENERIC,
)

SRC = os.path.join(INPUTS, "g0_calibration_structures.csv")
OUT = os.path.join(INPUTS, "g0_anchor_conservation.csv")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--cache", default=STRUCTURES)
    a = ap.parse_args()
    api = Api(a.cache)

    src = [r for r in csv.DictReader(open(SRC)) if r["state"] != "Intermediate"]
    entries: dict[str, dict] = {}
    for r in src:
        e = entries.setdefault(r["gpcrdb_entry"], {
            "gpcrdb_entry": r["gpcrdb_entry"],
            "receptor_slug": r["receptor_slug"],
            "on_panel48": r["on_panel48"],
            "on_panel75": r["on_panel75"],
            "n_active": 0, "n_inactive": 0,
        })
        e["n_active"] += r["state"] == "Active"
        e["n_inactive"] += r["state"] == "Inactive"

    keys = sorted(entries)
    if a.limit:
        keys = keys[:a.limit]

    rows = []
    for i, k in enumerate(keys, 1):
        e = dict(entries[k])
        bw = get_generic_numbers(api, k)
        if not bw:
            e["status"] = "no GPCRdb residue map"
            for lbl in ("aa_5_58", "aa_7_53", "aa_2x46", "aa_6x37"):
                e[lbl] = ""
            e["npxxy_measurable"] = 0
            e["tilt_measurable"] = 0
            rows.append(e)
            print(f"[{i}/{len(keys)}] {k:<16} NO MAP", flush=True)
            continue
        hits = {}
        for lbl in NPXXY_BW:
            h = lookup_bw(bw, lbl)
            hits[lbl] = h
        for lbl in TILT_GENERIC:
            h = lookup_generic(bw, lbl)
            hits[lbl] = h
        e["aa_5_58"] = (hits["5.58"] or (None, ""))[1]
        e["aa_7_53"] = (hits["7.53"] or (None, ""))[1]
        e["aa_2x46"] = (hits["2x46"] or (None, ""))[1]
        e["aa_6x37"] = (hits["6x37"] or (None, ""))[1]
        e["pos_5_58"] = (hits["5.58"] or ("", ""))[0]
        e["pos_7_53"] = (hits["7.53"] or ("", ""))[0]
        e["pos_2x46"] = (hits["2x46"] or ("", ""))[0]
        e["pos_6x37"] = (hits["6x37"] or ("", ""))[0]
        e["npxxy_measurable"] = int(e["aa_5_58"] == "Y" and e["aa_7_53"] == "Y")
        e["tilt_measurable"] = int(bool(hits["2x46"]) and bool(hits["6x37"]))
        e["status"] = "ok"
        rows.append(e)
        print(f"[{i}/{len(keys)}] {k:<16} 5.58={e['aa_5_58'] or '-'} "
              f"7.53={e['aa_7_53'] or '-'} 2x46={e['aa_2x46'] or '-'} "
              f"6x37={e['aa_6x37'] or '-'}  "
              f"npxxy={'YES' if e['npxxy_measurable'] else 'NO '}", flush=True)

    cols = ["gpcrdb_entry", "receptor_slug", "on_panel48", "on_panel75",
            "n_active", "n_inactive", "aa_5_58", "aa_7_53", "aa_2x46", "aa_6x37",
            "pos_5_58", "pos_7_53", "pos_2x46", "pos_6x37",
            "npxxy_measurable", "tilt_measurable", "status"]
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)} ({len(rows)} rows)")

    def report(pop, name):
        n = len(pop)
        ok = [r for r in pop if r["npxxy_measurable"]]
        sa = sum(r["n_active"] for r in ok)
        si = sum(r["n_inactive"] for r in ok)
        ta = sum(r["n_active"] for r in pop)
        ti = sum(r["n_inactive"] for r in pop)
        print(f"  {name:<34} receptors {len(ok):>3}/{n:<3} measurable on NPxxY"
              f"   structures A {sa}/{ta}  I {si}/{ti}")

    print()
    print("## Can the NPxxY axis be measured at all?  (Y at 5.58 AND Y at 7.53)")
    report(rows, "all Class A entries")
    report([r for r in rows if r["on_panel48"] == "1"], "application set (panel48)")
    report([r for r in rows if r["on_panel48"] == "0"], "calibration set (off panel48)")
    print()
    print("## Residue at 5.58 across Class A entries")
    for aa, n in collections.Counter(r["aa_5_58"] or "-" for r in rows).most_common():
        onp = sum(1 for r in rows if (r["aa_5_58"] or "-") == aa and r["on_panel48"] == "1")
        print(f"   {aa}  {n:>3} entries   ({onp} of them on panel48)")
    print()
    print("## Residue at 7.53 across Class A entries")
    for aa, n in collections.Counter(r["aa_7_53"] or "-" for r in rows).most_common():
        print(f"   {aa}  {n:>3} entries")
    print()
    print("## Tilt anchors 2x46 / 6x37 present?")
    print(f"   both present: {sum(r['tilt_measurable'] for r in rows)} of {len(rows)} entries")
    for lbl, col in (("2x46", "aa_2x46"), ("6x37", "aa_6x37")):
        miss = [r["gpcrdb_entry"] for r in rows if not r[col]]
        print(f"   {lbl} absent on {len(miss)} entries" + (f": {miss[:12]}" if miss else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
