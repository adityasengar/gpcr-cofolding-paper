"""Build the Block B Wide campaign queue for the 20-GPU pool.

Reads the full Block B Wide manifest (3,200 rows) from a specified path,
derives one prediction_sha per row via ``propose_row_key``, writes:

- ``{pool}/queue.csv``       — a superset of the manifest with
                                ``prediction_sha`` filled and a
                                worker-facing ``prediction_path`` column
                                that points at scratch.
- ``{pool}/queue_state.csv`` — one row per queue row, initial state
                                ``pending`` for every row (Block B has no
                                Block-A-style wave-1 pre-completion; there
                                is no analog to the DRD2 done-at-construction
                                override). An optional ``--smoke-receptor``
                                flag pauses everything except one receptor,
                                for a future smoke test — omit it and every
                                row lands ``pending``.

Usage (on basel-hpc):
    python3 scripts/build_block_b_campaign_queue.py \
        --manifest /home/sengaad1/paper_af3/experiments/019_block_b_partner_selection/manifest/manifest.csv \
        --pool /hpc/scratch/sengaad1/paper_af3/block_b_wide_2026_09_02

Optional:
    --smoke-receptor AA2AR    pauses every row except this receptor's
    --dry-run                 print counts + do not write
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scorer.rerun_dispatch import propose_row_key   # noqa: E402


STATE_COLUMNS = (
    "prediction_sha",
    "backbone",
    "state",           # pending | claimed | done | failed | paused
    "worker",
    "claimed_at",
    "finished_at",
    "last_reason",
)


def _pred_path(row: dict) -> str:
    """Reconstruct the prediction output directory from the manifest row.

    prediction_path in the manifest points at the model_0 output CIF's
    path. For a worker we need PRED_OUT_DIR (the seed_ directory);
    prediction_path.rsplit('/', 1)[0] would give us that at run time.
    We keep prediction_path here as the manifest gives it.
    """
    return (row.get("prediction_path") or "").strip()


def build_queue(manifest_path: Path,
                pool: Path,
                smoke_receptor: str | None,
                dry_run: bool) -> dict[str, int]:
    """Emit queue.csv + queue_state.csv into pool. Return counts."""
    pool.mkdir(parents=True, exist_ok=True)

    with manifest_path.open() as f:
        manifest_rows = list(csv.DictReader(f))
    if not manifest_rows:
        raise RuntimeError(f"empty manifest at {manifest_path}")

    n_input_sha_empty = sum(1 for r in manifest_rows
                            if not (r.get("input_sha") or "").strip())
    if n_input_sha_empty:
        raise RuntimeError(
            f"{n_input_sha_empty}/{len(manifest_rows)} manifest rows have "
            f"empty input_sha — cannot derive prediction_sha via "
            f"propose_row_key. Re-materialise the manifest on HPC first."
        )

    # Derive prediction_sha per row. Collisions unlikely (input_sha + new_seed)
    # but guard against duplicates so state file keys stay unique.
    seen_shas: set[str] = set()
    queue_rows: list[dict] = []
    for r in manifest_rows:
        sha = propose_row_key(r)
        if not sha:
            raise RuntimeError(f"propose_row_key returned empty for row: {r.get('request_id')}")
        if sha in seen_shas:
            raise RuntimeError(
                f"duplicate prediction_sha {sha[:12]}... — "
                f"input_sha + new_seed collision on request_id={r.get('request_id')}"
            )
        seen_shas.add(sha)
        # Freeze the derived sha onto the queue row (overwriting the
        # manifest's empty prediction_sha column).
        r["prediction_sha"] = sha
        queue_rows.append(r)

    # Determine initial state for each row: no Block-A wave-1 analog here.
    # Default is `pending` for every row; --smoke-receptor pauses everything
    # else for an optional single-receptor smoke pass.
    smoke = (smoke_receptor or "").upper()
    pending_count = 0
    paused_count = 0
    state_rows: list[dict[str, str]] = []
    for r in queue_rows:
        rec = (r.get("receptor_resolved") or "").upper()
        if smoke and rec != smoke:
            state = "paused"
            reason = f"smoke pass: only {smoke} pending"
            paused_count += 1
        else:
            state = "pending"
            reason = ""
            pending_count += 1
        state_rows.append({
            "prediction_sha": r["prediction_sha"],
            "backbone": r["backbone"],
            "state": state,
            "worker": "",
            "claimed_at": "",
            "finished_at": "",
            "last_reason": reason,
        })

    counts = {
        "n_manifest_rows": len(manifest_rows),
        "n_queue_rows": len(queue_rows),
        "pending": pending_count,
        "paused": paused_count,
    }
    if dry_run:
        return counts

    queue_csv = pool / "queue.csv"
    state_csv = pool / "queue_state.csv"

    fields = list(queue_rows[0].keys())
    with queue_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in queue_rows:
            w.writerow(r)

    with state_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(STATE_COLUMNS))
        w.writeheader()
        for sr in state_rows:
            w.writerow(sr)

    counts["queue_csv"] = str(queue_csv)
    counts["queue_state_csv"] = str(state_csv)
    return counts


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True,
                   help="path to the Block B Wide manifest.csv (with input_path + input_sha filled)")
    p.add_argument("--pool", type=Path, required=True,
                   help="pool directory on scratch (created if missing)")
    p.add_argument("--smoke-receptor", default=None,
                   help="receptor slug to leave pending; every other row is paused (e.g. AA2AR for smoke)")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args(argv)

    counts = build_queue(args.manifest, args.pool,
                          args.smoke_receptor, args.dry_run)
    for k, v in counts.items():
        print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
