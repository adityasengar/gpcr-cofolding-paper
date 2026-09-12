#!/usr/bin/env python3
"""Count PDB deposits per receptor via the RCSB Search API by UniProt.

Post-Audit Stage 3c (2026-09-05).

For each unique receptor in ``refs/reference_set.csv``, resolve the
UniProt accession via ``uniprot_slug`` (e.g., "5ht1b_human") → primary
accession lookup on UniProt, then hit the RCSB Search API for the
count of entries whose polymer entity contains that accession.

The receptor→UniProt accession table is small (~48 rows) so we hit
UniProt once per unique slug. RCSB Search is one POST per slug.
Total: ~100 API calls, ~30 s wall.

Emits ``refs/cache/pdb_entries_per_receptor.json``:

    {
      "per_receptor": {
        "5HT1B": {"uniprot_accession": "P28222", "n_entries": 42},
        ...
      },
      "generated_at_utc": "2026-09-05T..."
    }

Cached; re-run with --rebuild to refresh.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/search?query=id:{}&fields=accession&format=tsv"
RCSB_SEARCH_URL = "https://search.rcsb.org/rcsbsearch/v2/query"


def _slug_to_accession(slug: str) -> str | None:
    """slug like `5ht1b_human` → UniProt accession like `P28222`.
    Returns None on any lookup failure."""
    req = urllib.request.Request(UNIPROT_URL.format(slug), headers={
        "Accept": "text/plain"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8").strip().splitlines()
        if len(body) < 2:
            return None
        return body[1].strip() or None
    except Exception:
        return None


def _count_pdb_entries_for_accession(acc: str) -> int:
    """Ask RCSB Search API how many entries have a polymer_entity
    whose rcsb_polymer_entity_container_identifiers.reference_sequence_
    identifiers.database_accession == acc."""
    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
                "operator": "exact_match",
                "value": acc,
            },
        },
        "return_type": "entry",
        "request_options": {
            "return_counts": True,
        },
    }
    req = urllib.request.Request(
        RCSB_SEARCH_URL,
        data=json.dumps(query).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        return int(data.get("total_count") or 0)
    except urllib.error.HTTPError as e:
        if e.code == 204:
            return 0
        raise
    except Exception:
        return 0


def _receptors_and_slugs(ref_set: Path) -> dict[str, str]:
    """Return {receptor_upper: uniprot_slug} (first-seen slug wins)."""
    out: dict[str, str] = {}
    with ref_set.open() as f:
        for row in csv.DictReader(f):
            recep = (row.get("receptor_slug") or "").strip().upper()
            slug = (row.get("uniprot_slug") or "").strip().lower()
            if recep and slug and recep not in out:
                out[recep] = slug
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ref-set", type=Path,
                   default=REPO / "refs" / "reference_set.csv")
    p.add_argument("--out", type=Path,
                   default=REPO / "refs" / "cache" / "pdb_entries_per_receptor.json")
    p.add_argument("--rebuild", action="store_true")
    args = p.parse_args(argv)

    per_slug = _receptors_and_slugs(args.ref_set)
    existing: dict = {}
    if args.out.exists() and not args.rebuild:
        try:
            existing = json.loads(args.out.read_text())
        except Exception:
            existing = {}
    per_receptor = existing.get("per_receptor", {}) if isinstance(
        existing, dict
    ) else {}

    n_new = 0
    n_cached = 0
    n_failed = 0
    for recep, slug in sorted(per_slug.items()):
        cache = per_receptor.get(recep, {})
        if cache.get("n_entries") is not None and not args.rebuild:
            n_cached += 1
            continue
        acc = _slug_to_accession(slug)
        time.sleep(0.5)
        if not acc:
            per_receptor[recep] = {"uniprot_slug": slug,
                                    "uniprot_accession": None,
                                    "n_entries": None,
                                    "error": "no accession from uniprot"}
            n_failed += 1
            print(f"  {recep}: FAIL (no accession)", file=sys.stderr)
            continue
        n = _count_pdb_entries_for_accession(acc)
        time.sleep(0.5)
        per_receptor[recep] = {"uniprot_slug": slug,
                                "uniprot_accession": acc,
                                "n_entries": n}
        n_new += 1
        print(f"  {recep} ({acc}): {n} PDB entries", file=sys.stderr)

    out = {
        "generated_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(
            timespec="seconds"
        ),
        "n_receptors": len(per_slug),
        "n_new": n_new,
        "n_cached": n_cached,
        "n_failed": n_failed,
        "per_receptor": per_receptor,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "n_receptors": len(per_slug),
        "n_new": n_new,
        "n_cached": n_cached,
        "n_failed": n_failed,
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
