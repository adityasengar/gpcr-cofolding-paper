#!/usr/bin/env python3
"""Analysis-stage table journal — plan §20 propagation guard.

Every step that emits a CSV under `experiments/*/analysis/` appends a
line to `<analysis_dir>/table_journal.jsonl`:

    {
      "path": "...",            # absolute path
      "sha256": "...",
      "n_rows": ...,
      "per_cell_count_hash": "...",  # sha256 of a sorted (class,arm,backbone)
                                     # count fingerprint (empty if columns
                                     # not present)
      "timestamp_utc": "...",
      "step": "..."             # optional label for the emitting step
    }

Any downstream step that reads a CSV can call
`assert_no_drift(path, expected_journal)` to refuse on a stale input.

The point is per plan §20:
    "a stage ran correctly against the wrong upstream, and reported
     success."
The journal makes upstream freshness observable across the pipeline.

CLI:
    python3 scripts/table_journal.py append \\
        --analysis-dir experiments/018_block_a_switch_test/analysis \\
        --path experiments/018_block_a_switch_test/analysis/rows.csv \\
        --step "primary_rescore"

    python3 scripts/table_journal.py check \\
        --analysis-dir experiments/018_block_a_switch_test/analysis \\
        --path experiments/018_block_a_switch_test/analysis/rows.rmsd.csv
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import hashlib
import json
import sys
from pathlib import Path


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _per_cell_count_hash(path: Path) -> str:
    """Sha256 of the sorted (receptor_class, input_state_claim,
    backbone_inferred) count fingerprint. Returns empty string if any
    required column is missing (i.e. not a rows-shaped table).
    """
    try:
        from collections import Counter
    except ImportError:  # pragma: no cover
        return ""
    hints = (("_boltz", "boltz"), ("_chai", "chai"), ("_of3", "of3"),
             ("_protenix", "protenix"), ("_af2mm", "af2mm"))
    counts: "Counter[tuple[str, str, str]]" = Counter()
    with path.open() as f:
        reader = csv.DictReader(f)
        needed = {"receptor_class", "input_state_claim", "input_path"}
        if not needed <= set(reader.fieldnames or []):
            return ""
        for r in reader:
            cls = (r.get("receptor_class") or "").strip()
            arm = (r.get("input_state_claim") or "").strip()
            ip = (r.get("input_path") or "").lower()
            bb = "unknown"
            for pat, name in hints:
                if pat in ip:
                    bb = name
                    break
            counts[(cls, arm, bb)] += 1
    body = json.dumps(sorted(counts.items()), separators=(",", ":"))
    return hashlib.sha256(body.encode()).hexdigest()


def _n_rows(path: Path) -> int:
    n = 0
    with path.open() as f:
        for i, _ in enumerate(f):
            n = i  # count minus 1 (header)
    return n


def journal_path(analysis_dir: Path) -> Path:
    return analysis_dir / "table_journal.jsonl"


def append(analysis_dir: Path, csv_path: Path, step: str = "") -> dict:
    """Append a new entry for csv_path to the journal. Returns the record."""
    entry = {
        "path": str(csv_path.resolve()),
        "sha256": _sha256(csv_path),
        "n_rows": _n_rows(csv_path),
        "per_cell_count_hash": _per_cell_count_hash(csv_path),
        "timestamp_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="seconds"),
        "step": step,
    }
    analysis_dir.mkdir(parents=True, exist_ok=True)
    with journal_path(analysis_dir).open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry


def _read_journal(analysis_dir: Path) -> list[dict]:
    p = journal_path(analysis_dir)
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def latest_for(analysis_dir: Path, csv_path: Path) -> dict | None:
    """Return the most recent journal entry for csv_path, or None."""
    target = str(csv_path.resolve())
    for entry in reversed(_read_journal(analysis_dir)):
        if entry.get("path") == target:
            return entry
    return None


def check(analysis_dir: Path, csv_path: Path) -> tuple[bool, str]:
    """Return (ok, message). Fails if the on-disk sha differs from the
    latest journal entry for the same path."""
    if not csv_path.exists():
        return False, f"missing {csv_path}"
    latest = latest_for(analysis_dir, csv_path)
    if latest is None:
        return False, f"no journal entry for {csv_path} — append first"
    cur = _sha256(csv_path)
    if cur != latest["sha256"]:
        return False, (
            f"{csv_path.name}: on-disk sha {cur[:12]} != journal "
            f"{latest['sha256'][:12]} (recorded at {latest.get('timestamp_utc')}). "
            f"Table changed since last journal entry — the downstream step "
            f"was run against a stale copy."
        )
    return True, f"OK — sha match {cur[:12]} at {latest.get('timestamp_utc')}"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_ap = sub.add_parser("append")
    p_ap.add_argument("--analysis-dir", type=Path, required=True)
    p_ap.add_argument("--path", type=Path, required=True)
    p_ap.add_argument("--step", default="")

    p_ck = sub.add_parser("check")
    p_ck.add_argument("--analysis-dir", type=Path, required=True)
    p_ck.add_argument("--path", type=Path, required=True)

    p_ls = sub.add_parser("list")
    p_ls.add_argument("--analysis-dir", type=Path, required=True)

    args = ap.parse_args(argv)

    if args.cmd == "append":
        entry = append(args.analysis_dir, args.path, step=args.step)
        print(json.dumps(entry, indent=2))
        return 0
    if args.cmd == "check":
        ok, msg = check(args.analysis_dir, args.path)
        print(msg)
        return 0 if ok else 1
    if args.cmd == "list":
        for entry in _read_journal(args.analysis_dir):
            path = entry.get("path", "?")
            step = entry.get("step") or "-"
            print(f"{entry.get('timestamp_utc')}  {step:<25}  "
                  f"n={entry.get('n_rows'):>6}  "
                  f"sha={entry.get('sha256', '')[:12]}  {path}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
