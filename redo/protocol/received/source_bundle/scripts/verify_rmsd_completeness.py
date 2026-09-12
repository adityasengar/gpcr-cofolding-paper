#!/usr/bin/env python3
"""Completeness gate for `rows.rmsd.csv` (or any derived table) against
its parent `rows.csv`.

Countermeasure per plan §14 + §20: a derived table that was computed
against a stale parent is invisible to output-level audits (the numbers
look reasonable, they just were not computed on the current data). The
stale-RMSD failure was:

    rows.csv        — regenerated 2026-09-02 with post-fix OF3 paths
    rows.rmsd.csv   — never regenerated; every OF3 row still on the
                       pre-fix `seed_2746317213` CIFs

Three checks, all must pass:

  1. Identity — the ``input_path`` set of the derived table equals the
     ``input_path`` set of the parent (bidirectional set equality).
  2. Row count — ``len(derived) == len(parent)``.
  3. Per-cell count — for every (receptor_class × input_state_claim ×
     backbone_inferred) cell in the parent, the derived table has the
     same count.

The gate exits 0 on pass, non-zero on any failure, and prints a
human-readable diff on failure. It writes a JSON provenance blob
alongside the derived table so subsequent readers can assert
``parent_rows_csv_sha`` matches.

Usage
-----
    python3 scripts/verify_rmsd_completeness.py \
        --parent experiments/018_block_a_switch_test/analysis/rows.csv \
        --derived experiments/018_block_a_switch_test/analysis/rows.rmsd.csv \
        [--write-provenance]

Extensibility (plan §20 generalisation): the same driver works on any
derived table that inherits input_path from rows.csv — replace
``--derived`` with the target file. Backbone inference uses a small
path-regex table shared with the analysis code path.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path


BACKBONE_HINTS: tuple[tuple[str, str], ...] = (
    ("_boltz", "boltz"),
    ("_chai", "chai"),
    ("_of3", "of3"),
    ("_protenix", "protenix"),
    ("_af2mm", "af2mm"),
)


def _infer_backbone(path: str) -> str:
    p = path.lower()
    for pat, name in BACKBONE_HINTS:
        if pat in p:
            return name
    return "unknown"


def _load(path: Path) -> list[dict[str, str]]:
    with path.open() as f:
        return list(csv.DictReader(f))


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _cell_counts(rows: list[dict[str, str]]) -> Counter:
    c: Counter = Counter()
    for r in rows:
        rc = (r.get("receptor_class") or "").strip()
        sc = (r.get("input_state_claim") or "").strip()
        bb = _infer_backbone(r.get("input_path") or "")
        c[(rc, sc, bb)] += 1
    return c


def verify(parent: Path, derived: Path) -> tuple[bool, list[str]]:
    p_rows = _load(parent)
    d_rows = _load(derived)
    problems: list[str] = []

    # (2) row count
    if len(p_rows) != len(d_rows):
        problems.append(
            f"row count mismatch: parent={len(p_rows)} derived={len(d_rows)}"
        )

    # (1) identity: input_path set equality
    p_paths = {r.get("input_path") for r in p_rows if r.get("input_path")}
    d_paths = {r.get("input_path") for r in d_rows if r.get("input_path")}
    only_p = p_paths - d_paths
    only_d = d_paths - p_paths
    if only_p or only_d:
        problems.append(
            f"input_path set mismatch: {len(only_p)} in parent-only, "
            f"{len(only_d)} in derived-only"
        )
        for x in list(only_p)[:3]:
            problems.append(f"  parent-only sample: {x}")
        for x in list(only_d)[:3]:
            problems.append(f"  derived-only sample: {x}")

    # (3) per-cell counts
    p_cells = _cell_counts(p_rows)
    d_cells = _cell_counts(d_rows)
    all_keys = set(p_cells) | set(d_cells)
    cell_diffs: list[tuple[tuple[str, str, str], int, int]] = []
    for k in sorted(all_keys):
        if p_cells[k] != d_cells[k]:
            cell_diffs.append((k, p_cells[k], d_cells[k]))
    if cell_diffs:
        problems.append(
            f"per-cell count mismatch on {len(cell_diffs)} "
            f"(class, state, backbone) cells:"
        )
        for k, p_n, d_n in cell_diffs[:10]:
            problems.append(f"  {k}: parent={p_n} derived={d_n}")

    return (not problems), problems


def write_provenance(parent: Path, derived: Path) -> Path:
    """Write ``<derived>.provenance.json`` recording the parent's SHA
    and the derived's row count. Plan §20 propagation guard: on read,
    a downstream stage compares ``parent_rows_csv_sha`` with the current
    parent SHA and refuses on drift.
    """
    prov_path = derived.with_suffix(derived.suffix + ".provenance.json")
    body = {
        "derived_path": str(derived.resolve()),
        "parent_rows_csv_path": str(parent.resolve()),
        "parent_rows_csv_sha256": _sha256(parent),
        "derived_sha256": _sha256(derived),
        "derived_n_rows": len(_load(derived)),
    }
    prov_path.write_text(json.dumps(body, indent=2) + "\n")
    return prov_path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--parent", type=Path, required=True,
                    help="parent CSV — usually rows.csv")
    ap.add_argument("--derived", type=Path, required=True,
                    help="derived CSV to verify — usually rows.rmsd.csv")
    ap.add_argument("--write-provenance", action="store_true",
                    help="also emit <derived>.provenance.json on pass")
    args = ap.parse_args(argv)

    if not args.parent.exists():
        print(f"missing parent {args.parent}", file=sys.stderr)
        return 2
    if not args.derived.exists():
        print(f"missing derived {args.derived}", file=sys.stderr)
        return 2

    ok, problems = verify(args.parent, args.derived)
    if ok:
        print(
            f"PASS — {args.derived.name} matches {args.parent.name} "
            f"on identity, row count, and per-cell counts"
        )
        if args.write_provenance:
            prov = write_provenance(args.parent, args.derived)
            print(f"provenance: {prov}")
        return 0

    print(
        f"FAIL — {args.derived.name} is not a complete derivation of "
        f"{args.parent.name}:",
        file=sys.stderr,
    )
    for p in problems:
        print(f"  {p}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
