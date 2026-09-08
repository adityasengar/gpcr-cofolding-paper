#!/usr/bin/env python3
"""Fingerprint the data inputs so a stale RESULTS.md announces itself.

  python3 analysis/fingerprint.py          # print current fingerprint
  python3 analysis/fingerprint.py --check  # compare against .datafingerprint, exit 1 if changed
  python3 analysis/fingerprint.py --stamp  # record current state as the new baseline

Every RESULTS.md verdict is only true for one fingerprint. When the HPC export is
refreshed this changes, and every verdict must be re-derived rather than trusted.
"""
import hashlib, os, sys, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUTS = ["data/predictions.csv", "data/conditions.csv", "data/receptors.csv",
          "data/backbones.csv", "data/coverage_matrix.csv", "data/experiments.jsonl",
          "rows_enriched_v3_7.csv"]
STAMP = os.path.join(ROOT, ".datafingerprint")

def _excluded(rel):
    """True if git deliberately excludes this path (so absence is by design)."""
    import subprocess
    try:
        return subprocess.run(["git", "-C", ROOT, "check-ignore", "-q", rel],
                              capture_output=True).returncode == 0
    except Exception:
        return False

def fp():
    out = {}
    for rel in INPUTS:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            out[rel] = {"missing": True}; continue
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
        n = sum(1 for _ in open(p, errors="ignore"))
        out[rel] = {"sha256": h.hexdigest()[:16], "lines": n,
                    "bytes": os.path.getsize(p)}
    return out

def main():
    cur = fp()
    arg = sys.argv[1] if len(sys.argv) > 1 else ""
    if arg == "--stamp":
        json.dump(cur, open(STAMP, "w"), indent=1, sort_keys=True)
        print(f"stamped {STAMP}"); return 0
    if arg == "--check":
        if not os.path.exists(STAMP):
            print("no baseline; run --stamp"); return 1
        old = json.load(open(STAMP))
        changed, absent = [], []
        for k in sorted(set(old) | set(cur)):
            o, c = old.get(k, {}), cur.get(k, {})
            if o == c:
                continue
            # A file excluded from the repo is absent by design on a second machine.
            # Reporting that as "changed" trains the reader to ignore this warning.
            if c.get("missing") and not o.get("missing") and _excluded(k):
                absent.append(k)
            else:
                changed.append((k, o, c))
        for k in absent:
            print(f"  not on this machine (excluded from the repo): {k}")
        if not changed:
            if absent:
                print("verdicts still apply for everything present here.")
            else:
                print("data unchanged - RESULTS.md verdicts still apply")
            return 0
        print("DATA CHANGED. Every RESULTS.md verdict is stale until re-derived:")
        for k, o, c in changed:
            print(f"  {k}: {o.get('lines','-')} -> {c.get('lines','-')} lines, "
                  f"{o.get('sha256','-')} -> {c.get('sha256','-')}")
        print("\nRe-run:  python3 analysis/q.py " + " ".join(sorted(
            n for n in ["scope","ladder","receptor_counts","aa2ar","coverage"])))
        return 1

    for k, v in sorted(cur.items()):
        print(f"  {k:<28} {v.get('sha256','MISSING')}  {v.get('lines','-')} lines")
    return 0

if __name__ == "__main__":
    sys.exit(main())
