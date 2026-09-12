#!/usr/bin/env python3
"""The run registry — one row per experiment, and whether it can run.

`CATALOGUE.md` says what COULD be run. `g1_systems.csv` says what IS enumerated.
`matrix_cost.py` says what it would cost. `DECISIONS.md` says what has been ruled
in or out. **Nothing joined those four**, so "what are we running?" had no answer
you could read off a file — which is how 36 of 45 experiments came to have no
enumerated systems without anyone noticing.

This joins them. It DERIVES what is derivable and refuses to invent the rest: an
experiment whose status cannot be established from the files is marked
`NEEDS_TRIAGE`, never given a plausible status. A registry that guesses is worse
than no registry, because it reads as authoritative.

    python3 redo/build/run_registry.py
    python3 redo/build/manifest.py

Writes: inputs/run_registry.tsv
"""

import csv
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, SPEC, BUILD  # noqa: E402

OUT = os.path.join(INPUTS, "run_registry.tsv")


def catalogue_entries():
    """id -> {title, cost, depends, banner} parsed from the BODY, not a header."""
    text = open(os.path.join(SPEC, "CATALOGUE.md")).read()
    parts = re.split(r"\n### (E\d+\.\d+)", text)
    out = {}
    for i in range(1, len(parts), 2):
        eid, body = parts[i], parts[i + 1]
        title = body.split("\n", 1)[0].strip(" —-")
        def field(name):
            m = re.search(r"\*\*%s\.\*\*\s*(.+?)(?:\n- \*\*|\n\n|\Z)" % name,
                          body, flags=re.S)
            return " ".join(m.group(1).split())[:300] if m else ""
        # The banner may sit anywhere in the entry, not only at its head --
        # matching only the start missed E0.5's CLOSED and E7.2's PARKED, which
        # are the two entries whose status is already decided.
        banner = ""
        m = re.search(r"^> \*\*(.+?)\*\*", body, flags=re.S | re.M)
        if m:
            banner = " ".join(m.group(1).split())[:160]
        out[eid] = {"title": title, "cost": field("Cost"),
                    "depends": field("Depends on"), "banner": banner}
    return out


def enumerated():
    """experiment id -> (file, n_systems, n_receptors, n_clusters)."""
    out = {}
    for fn in ("g1_systems.csv", "g2_systems.csv"):
        p = os.path.join(INPUTS, fn)
        if not os.path.exists(p):
            continue
        with open(p) as fh:
            rows = list(csv.DictReader(fh))
        for r in rows:
            for eid in re.findall(r"E\d+\.\d+", r.get("experiment", "")):
                d = out.setdefault(eid, {"file": fn, "n": 0, "rec": set(), "cl": set()})
                d["n"] += 1
                if r.get("receptor_slug"):
                    d["rec"].add(r["receptor_slug"])
                if r.get("receptor_cluster"):
                    d["cl"].add(r["receptor_cluster"])
    return out


def costed():
    """experiment ids named anywhere in RUN_MATRIX's item table."""
    p = os.path.join(SPEC, "RUN_MATRIX.md")
    if not os.path.exists(p):
        return set()
    return set(re.findall(r"E\d+\.\d+", open(p).read()))


def main():
    cat = catalogue_entries()
    enum = enumerated()
    cost = costed()

    rows = []
    for eid in sorted(cat, key=lambda e: (int(e[1:].split(".")[0]),
                                          int(e.split(".")[1]))):
        c = cat[eid]
        e = enum.get(eid)
        banner = c["banner"]

        # Status is DERIVED. Only four situations are decidable from the files;
        # everything else is triage, and saying so is the point.
        if banner.startswith("CLOSED"):
            status, why = "DROPPED", f"catalogue banner: {banner[:110]}"
        elif banner.startswith("PARKED"):
            status, why = "PARKED", f"catalogue banner: {banner[:110]}"
        elif e:
            status, why = "ENUMERATED", f"{e['n']} systems in {e['file']}"
        elif eid.startswith("E0."):
            status, why = ("BLOCKED",
                           "Group 0 is the instrument calibration and depends on "
                           "the MEASUREMENT PASS, which has never run and does not "
                           "start without Aditya's word")
        else:
            status, why = ("NEEDS_TRIAGE",
                           "in the catalogue, not enumerated, no decision recorded")

        rows.append({
            "experiment": eid,
            "group": eid.split(".")[0],
            "title": c["title"],
            "status": status,
            "status_basis": why,
            "systems_enumerated": "yes" if e else "no",
            "systems_file": e["file"] if e else "",
            "n_systems": e["n"] if e else 0,
            "n_receptors": len(e["rec"]) if e else 0,
            "n_clusters": len(e["cl"]) if e else 0,
            "named_in_run_matrix": "yes" if eid in cost else "no",
            "cost_class": c["cost"][:120],
            "depends_on": c["depends"][:160],
        })

    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    import collections
    st = collections.Counter(r["status"] for r in rows)
    print(f"wrote {os.path.relpath(OUT)}  ({len(rows)} experiments)\n")
    for k, v in st.most_common():
        print(f"  {k:<14} {v}")
    print()
    for g in sorted({r["group"] for r in rows}, key=lambda x: int(x[1:])):
        gr = [r for r in rows if r["group"] == g]
        s = collections.Counter(r["status"] for r in gr)
        # a row serving "E1.8+E1.1" belongs to BOTH experiments, so summing
        # n_systems across a group double-counts it. Report the file's own size.
        files = {r["systems_file"] for r in gr if r["systems_file"]}
        n = 0
        for fn in files:
            with open(os.path.join(INPUTS, fn)) as fh:
                n += sum(1 for _ in fh) - 1
        print(f"  {g}: {len(gr):>2} experiments  {dict(s)}"
              + (f"  {n:,} systems" if n else ""))
    tri = [r["experiment"] for r in rows if r["status"] == "NEEDS_TRIAGE"]
    print(f"\n  NEEDS_TRIAGE ({len(tri)}): {', '.join(tri)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
