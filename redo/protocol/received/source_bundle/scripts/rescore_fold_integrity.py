#!/usr/bin/env python3
"""Driver — compute the four fold-integrity columns for every row in
Block A's ``rows.csv`` and emit a merged sidecar CSV.

Input:
    experiments/018_block_a_switch_test/analysis/rows.csv  (9,490 rows)

Output:
    experiments/018_block_a_switch_test/analysis/rows.fold_integrity.csv

The emitted CSV carries the 5 columns needed downstream:

    input_path, tm6_helicity_6_30_6_50, chain_breaks,
    ramachandran_outlier_frac, icl3_modelled_count

Additionally two diagnostic columns:

    load_error     — non-empty on CIF load failure
    icl3_range     — the GPCRdb-derived (lo,hi) range used, or empty on
                     cache miss (so the report can trace NaN causes)

Cited rules are written to the CSV header as a preamble line beginning
``# rules: {json}`` — reviewer transparency.

Reads GPCRdb ICL3 boundaries from the local cache at
``refs/cache/gpcrdb/residues_ext_<gpcrdb_slug>.json``. No network
access; missing cache → NaN.

Parallelisation via multiprocessing.Pool (fork), N workers configurable
on the CLI. Default is 16, matching the task's stated 16-core CPU
budget. Progress lines every 500 rows.

The driver DOES NOT touch rows.csv, the scorer modules, or reference
CSVs. All output is a NEW file at the sidecar path.
"""
from __future__ import annotations

import argparse
import csv
import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Worker state — populated by the mp initializer.
# ---------------------------------------------------------------------------


_WORKER: dict[str, Any] = {}


def _worker_init(cache_dir: str) -> None:
    """Pre-import the fold_integrity module and stash the cache-dir path."""
    from scorer import fold_integrity  # noqa: F401
    _WORKER["cache_dir"] = Path(cache_dir)
    _WORKER["icl3_cache"] = {}  # gpcrdb_slug -> (lo,hi) or None


def _get_icl3_range(gpcrdb_slug: str) -> tuple[int, int] | None:
    """Memoised load_icl3_range per-worker."""
    from scorer.fold_integrity import load_icl3_range
    cache = _WORKER["icl3_cache"]
    if gpcrdb_slug in cache:
        return cache[gpcrdb_slug]
    r = load_icl3_range(gpcrdb_slug, _WORKER["cache_dir"])
    cache[gpcrdb_slug] = r
    return r


def _score_one(row: dict[str, str]) -> dict[str, Any]:
    """Compute the four columns for one rows.csv row. Never raises — a
    CIF load error surfaces as `load_error` on the result dict; the
    four columns are NaN in that case."""
    from scorer.fold_integrity import compute_fold_integrity

    input_path = row["input_path"]
    chain_name = row.get("chain_selected") or "A"
    gpcrdb_slug = row.get("gpcrdb_slug") or ""
    pos_6_30_raw = row.get("anchor_6_30_uniprot_pos") or ""
    try:
        pos_6_30: int | None = int(pos_6_30_raw) if pos_6_30_raw else None
    except (ValueError, TypeError):
        pos_6_30 = None

    icl3_range = _get_icl3_range(gpcrdb_slug) if gpcrdb_slug else None

    fi = compute_fold_integrity(
        input_path=input_path,
        chain_name=chain_name,
        pos_6_30=pos_6_30,
        icl3_range=icl3_range,
    )
    out = {
        "input_path": input_path,
        "tm6_helicity_6_30_6_50": fi["tm6_helicity_6_30_6_50"],
        "chain_breaks": fi["chain_breaks"],
        "ramachandran_outlier_frac": fi["ramachandran_outlier_frac"],
        "icl3_modelled_count": fi["icl3_modelled_count"],
        "load_error": fi["load_error"],
        "icl3_range": (
            f"{icl3_range[0]}-{icl3_range[1]}" if icl3_range is not None else ""
        ),
    }
    return out


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def _read_rows(rows_csv: Path) -> list[dict[str, str]]:
    with rows_csv.open() as f:
        return list(csv.DictReader(f))


def _write_output(
    out_path: Path,
    results: list[dict[str, Any]],
    n_workers: int,
    wall_time_s: float,
    rows_csv_sha: str,
) -> None:
    from scorer.fold_integrity import (
        RAMACHANDRAN_RULE,
        TM6_HELICITY_RULE,
        CHAIN_BREAK_RULE,
    )
    columns = [
        "input_path",
        "tm6_helicity_6_30_6_50",
        "chain_breaks",
        "ramachandran_outlier_frac",
        "icl3_modelled_count",
        "load_error",
        "icl3_range",
    ]
    header = {
        "tm6_helicity_6_30_6_50": TM6_HELICITY_RULE,
        "chain_breaks": CHAIN_BREAK_RULE,
        "ramachandran_outlier_frac": RAMACHANDRAN_RULE,
        "icl3_modelled_count": (
            "Number of UniProt positions in the GPCRdb-defined ICL3 range "
            "(from local residues_extended cache) that have a CA atom in "
            "the selected chain. NaN when the GPCRdb cache is missing."
        ),
        "input_rows_csv_sha256": rows_csv_sha,
        "n_workers": n_workers,
        "wall_time_s": round(wall_time_s, 1),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        f.write("# rules: " + json.dumps(header, sort_keys=False) + "\n")
        w = csv.DictWriter(f, fieldnames=columns)
        w.writeheader()
        for r in results:
            w.writerow(r)


def _read_rows_sha(rows_csv: Path) -> str:
    """SHA-256 of the on-disk rows.csv — always computed directly, never
    read from the sidecar ``rows.csv.sha256`` file, which is known to be
    stale (Block-B claim audit finding §Stage 3.2).

    Recording it in the emitted CSV pins the join key for downstream
    consumption (the report script must not silently join against a
    different rows.csv)."""
    import hashlib
    h = hashlib.sha256()
    with rows_csv.open("rb") as f:
        for chunk in iter(lambda: f.read(64 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rescore(
    rows_csv: Path,
    out_csv: Path,
    n_workers: int,
    cache_dir: Path,
    chunksize: int = 8,
) -> dict[str, Any]:
    rows = _read_rows(rows_csv)
    n_total = len(rows)
    if n_total == 0:
        raise RuntimeError(f"{rows_csv} is empty")

    print(
        f"[fold-integrity] rows={n_total} workers={n_workers} "
        f"cache={cache_dir} out={out_csv}",
        file=sys.stderr,
    )

    ctx = mp.get_context("fork")
    t0 = time.time()
    results: list[dict[str, Any]] = []
    n_failed = 0
    with ctx.Pool(
        processes=n_workers,
        initializer=_worker_init,
        initargs=(str(cache_dir.resolve()),),
    ) as pool:
        for i, r in enumerate(
            pool.imap_unordered(_score_one, rows, chunksize=chunksize),
            start=1,
        ):
            results.append(r)
            if r["load_error"]:
                n_failed += 1
            if i % 500 == 0 or i == n_total:
                elapsed = time.time() - t0
                rate = i / elapsed if elapsed > 0 else 0.0
                print(
                    f"[fold-integrity] {i}/{n_total}  "
                    f"wall={elapsed:6.1f}s  rate={rate:5.1f} row/s  "
                    f"failed={n_failed}",
                    file=sys.stderr,
                )
    wall = time.time() - t0

    # deterministic row order — sort by input_path so the CSV is
    # reproducible even under imap_unordered
    results.sort(key=lambda r: r["input_path"])
    sha = _read_rows_sha(rows_csv)
    _write_output(out_csv, results, n_workers, wall, sha)

    return {
        "n_total": n_total,
        "n_failed": n_failed,
        "wall_time_s": wall,
        "rows_csv_sha256": sha,
        "out_csv": str(out_csv),
    }


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rescore_fold_integrity",
        description=(
            "Compute fold-integrity columns (TM6 helicity, chain breaks, "
            "Ramachandran outliers, ICL3 modelled count) for every row in "
            "Block A's rows.csv. CPU-only; parallel via mp.Pool."
        ),
    )
    p.add_argument(
        "--rows", type=Path,
        default=REPO
        / "experiments/018_block_a_switch_test/analysis/rows.csv",
    )
    p.add_argument(
        "--out", type=Path,
        default=REPO
        / "experiments/018_block_a_switch_test/analysis/rows.fold_integrity.csv",
    )
    p.add_argument(
        "--cache-dir", type=Path,
        default=REPO / "refs" / "cache",
        help="Root of the GPCRdb residues-extended cache "
             "(expects <cache-dir>/gpcrdb/residues_ext_<slug>.json).",
    )
    p.add_argument("--n-workers", type=int, default=16)
    p.add_argument("--chunksize", type=int, default=8)
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if not args.rows.exists():
        print(f"rows.csv not found: {args.rows}", file=sys.stderr)
        return 2
    summary = rescore(
        rows_csv=args.rows,
        out_csv=args.out,
        n_workers=args.n_workers,
        cache_dir=args.cache_dir,
        chunksize=args.chunksize,
    )
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
