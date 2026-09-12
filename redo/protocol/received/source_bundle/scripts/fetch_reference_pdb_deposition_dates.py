#!/usr/bin/env python3
"""Fetch deposition dates from RCSB for every PDB in refs/reference_set.csv.

Post-Audit Stage 3b (2026-09-05) — memorization stratification.

Fetches `rcsb_accession_info.deposit_date` for each unique PDB ID in
the reference set from ``https://data.rcsb.org/rest/v1/core/entry/<PDB>``
and writes a JSON table keyed by PDB ID.

Cached locally at ``refs/cache/rcsb_deposit_dates.json`` to avoid
re-hitting RCSB across runs. The cache is CSV-hash-keyed so a change
to reference_set.csv triggers a re-fetch of any newly-added PDB IDs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
RCSB_URL = "https://data.rcsb.org/rest/v1/core/entry/{pdb}"


def _pdbs_from_ref_set(path: Path) -> list[str]:
    pdbs: set[str] = set()
    with path.open() as f:
        for row in csv.DictReader(f):
            p = (row.get("pdb_id") or "").strip().upper()
            if p:
                pdbs.add(p)
    return sorted(pdbs)


def _fetch_one(pdb: str, *, retries: int = 3, sleep_s: float = 0.5) -> dict:
    url = RCSB_URL.format(pdb=pdb.upper())
    last_err = None
    for i in range(retries):
        try:
            with urllib.request.urlopen(url, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            return {
                "pdb": pdb.upper(),
                "deposit_date": data.get("rcsb_accession_info", {}).get(
                    "deposit_date"
                ),
                "release_date": data.get("rcsb_accession_info", {}).get(
                    "initial_release_date"
                ),
                "revision_date": data.get("rcsb_accession_info", {}).get(
                    "revision_date"
                ),
                "status_code": 200,
            }
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}"
            if e.code == 404:
                return {"pdb": pdb.upper(), "status_code": 404, "error": "not found"}
            time.sleep(sleep_s * (i + 1))
        except Exception as e:
            last_err = str(e)
            time.sleep(sleep_s * (i + 1))
    return {"pdb": pdb.upper(), "status_code": 0, "error": last_err or "unknown"}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ref-set", type=Path,
                   default=REPO / "refs" / "reference_set.csv")
    p.add_argument("--out", type=Path,
                   default=REPO / "refs" / "cache" / "rcsb_deposit_dates.json")
    p.add_argument("--rebuild", action="store_true",
                   help="Ignore cache and re-fetch every PDB")
    args = p.parse_args(argv)

    pdbs = _pdbs_from_ref_set(args.ref_set)
    ref_sha = hashlib.sha256(args.ref_set.read_bytes()).hexdigest()

    existing: dict = {}
    if args.out.exists() and not args.rebuild:
        try:
            existing = json.loads(args.out.read_text())
        except Exception:
            existing = {}

    per_pdb = existing.get("per_pdb", {}) if isinstance(existing, dict) else {}
    n_new = 0
    n_cached = 0
    n_failed = 0
    for pdb in pdbs:
        if pdb in per_pdb and per_pdb[pdb].get("status_code") == 200:
            n_cached += 1
            continue
        row = _fetch_one(pdb)
        per_pdb[pdb] = row
        if row.get("status_code") == 200:
            n_new += 1
        else:
            n_failed += 1
        # RCSB is generous — 3/s is well within the budget.
        time.sleep(0.35)
        print(f"  fetched {pdb}: {row.get('deposit_date') or row.get('error')}",
              file=sys.stderr)

    out = {
        "ref_set_csv_sha256": ref_sha,
        "n_pdbs_in_refs": len(pdbs),
        "n_fetched_this_run": n_new,
        "n_cache_hits": n_cached,
        "n_failed": n_failed,
        "per_pdb": per_pdb,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "n_pdbs": len(pdbs),
        "n_new": n_new,
        "n_cached": n_cached,
        "n_failed": n_failed,
        "out": str(args.out),
    }, indent=2))
    return 0 if n_failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
