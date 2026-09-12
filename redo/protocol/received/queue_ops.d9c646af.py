"""Atomic queue operations for the h100_pool worker pool.

Two subcommands:

- ``pop <worker_id> [--state-csv PATH] [--queue-csv PATH]``
    Atomically claim one row (state=pending → state=claimed, worker=<id>).
    Prints shell-eval'able env-var assignments (PRED_INPUT, PRED_OUT_DIR,
    PRED_SEED, PRED_SAMPLES, PRED_SIDECAR, BACKBONE, CLAIM_SHA) on stdout.
    Exit codes: 0 = claimed one row; 1 = queue empty (no pending rows);
    2 = queue.csv row missing (state/queue out of sync).

- ``mark <sha> <new_state> [--state-csv PATH]``
    Atomically transition the row with prediction_sha=<sha> from claimed
    to <new_state> (typically done or failed). No-op if row not found.

Lock file: ``<state_csv>.lock`` (fcntl exclusive lock over full operation).

Design invariants:
- Never overwrite a done or failed row.
- Every state transition writes the CSV via os.replace (atomic on POSIX).
- Timestamp added on every claim/mark for audit trail.
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import fcntl
import os
import sys
from pathlib import Path

DEFAULT_POOL = Path("/hpc/scratch/sengaad1/paper_af3/h100_pool")
STATE_COLUMNS = (
    "prediction_sha",
    "backbone",
    "state",           # pending | claimed | done | failed
    "worker",
    "claimed_at",
    "finished_at",
    "last_reason",
)


def _utcnow() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


def _load_state(state_csv: Path) -> list[dict[str, str]]:
    with state_csv.open() as f:
        return list(csv.DictReader(f))


def _save_state(state_csv: Path, rows: list[dict[str, str]]) -> None:
    tmp = state_csv.with_suffix(state_csv.suffix + ".tmp")
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(STATE_COLUMNS))
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in STATE_COLUMNS})
    os.replace(tmp, state_csv)


def _lock_path(state_csv: Path) -> Path:
    return state_csv.parent / f".{state_csv.name}.lock"


def _find_queue_row(queue_csv: Path, sha: str) -> dict[str, str] | None:
    with queue_csv.open() as f:
        for r in csv.DictReader(f):
            if r.get("prediction_sha", "") == sha:
                return r
    return None


def _worker_filter(state_csv: Path, worker_id: str) -> tuple[set[str], bool]:
    """Read per-worker filter from ``<pool>/filters/<worker_id>.txt``.

    Format:
        line 1: comma-separated allowed backbones (e.g. ``of3`` or
                ``boltz,chai,protenix``). Empty / missing → no filter.
        line 2 (optional): the keyword ``strict``. When present, the
                worker's pop() returns exit=1 (no work) when the filter
                matches nothing, instead of falling back to any pending
                row. Use this to "skip a backbone for now" — pending rows
                for the excluded backbone stay pending until a later
                pass without the filter.

    Returns ``(allowed_set, strict_flag)``.
    """
    filter_path = state_csv.parent / "filters" / f"{worker_id}.txt"
    if not filter_path.exists():
        return set(), False
    lines = filter_path.read_text().strip().splitlines()
    if not lines or not lines[0].strip():
        return set(), False
    allowed = {bb.strip() for bb in lines[0].split(",") if bb.strip()}
    strict = len(lines) > 1 and lines[1].strip().lower() == "strict"
    return allowed, strict


def cmd_pop(args) -> int:
    lock = _lock_path(args.state_csv)
    lock.parent.mkdir(parents=True, exist_ok=True)
    allowed, strict = _worker_filter(args.state_csv, args.worker_id)
    with lock.open("w") as fp:
        fcntl.flock(fp, fcntl.LOCK_EX)
        rows = _load_state(args.state_csv)
        claim_sha = None
        # First pass: try to find a pending row matching the filter
        if allowed:
            for r in rows:
                if r["state"] == "pending" and r["backbone"] in allowed:
                    r["state"] = "claimed"
                    r["worker"] = args.worker_id
                    r["claimed_at"] = _utcnow()
                    claim_sha = r["prediction_sha"]
                    break
        # Second pass: no filter, or non-strict filter had no matches
        # → any pending row. Strict-filter workers exit early instead.
        if claim_sha is None and not strict:
            for r in rows:
                if r["state"] == "pending":
                    r["state"] = "claimed"
                    r["worker"] = args.worker_id
                    r["claimed_at"] = _utcnow()
                    claim_sha = r["prediction_sha"]
                    break
        if claim_sha is None:
            return 1
        _save_state(args.state_csv, rows)
        fcntl.flock(fp, fcntl.LOCK_UN)

    q = _find_queue_row(args.queue_csv, claim_sha)
    if q is None:
        print(f"queue_ops.pop: sha={claim_sha} not in {args.queue_csv}",
              file=sys.stderr)
        return 2

    # Emit shell-eval assignments matching what qsub -v … would set.
    pred_path = q.get("prediction_path", "").strip()
    out_dir = pred_path.rsplit("/", 1)[0] if pred_path else ""
    print(f"export PRED_INPUT={q.get('input_path', '')!r}")
    print(f"export PRED_OUT_DIR={out_dir!r}")
    print(f"export PRED_SEED={q.get('new_seed', '')!r}")
    print(f"export PRED_SAMPLES={q.get('samples_per_seed', '1')!r}")
    print(f"export PRED_SIDECAR={out_dir + '/_rerun_plan.json'!r}")
    print(f"export BACKBONE={q.get('backbone', '')!r}")
    print(f"export CLAIM_SHA={claim_sha!r}")
    return 0


def cmd_mark(args) -> int:
    lock = _lock_path(args.state_csv)
    with lock.open("w") as fp:
        fcntl.flock(fp, fcntl.LOCK_EX)
        rows = _load_state(args.state_csv)
        for r in rows:
            if r["prediction_sha"] == args.sha:
                r["state"] = args.new_state
                r["finished_at"] = _utcnow()
                if args.reason:
                    r["last_reason"] = args.reason
                break
        else:
            print(f"queue_ops.mark: sha={args.sha} not found", file=sys.stderr)
            return 1
        _save_state(args.state_csv, rows)
        fcntl.flock(fp, fcntl.LOCK_UN)
    return 0


def _queue_sha_to_row(queue_csv: Path) -> dict[str, dict[str, str]]:
    with queue_csv.open() as f:
        return {r["prediction_sha"]: r for r in csv.DictReader(f)
                if r.get("prediction_sha")}


def cmd_bulk_transition(args) -> int:
    lock = _lock_path(args.state_csv)
    with lock.open("w") as fp:
        fcntl.flock(fp, fcntl.LOCK_EX)
        rows = _load_state(args.state_csv)
        want_receptor = (args.receptor or "").upper().strip()
        want_backbone = (args.backbone or "").strip()
        q_by_sha: dict[str, dict[str, str]] = {}
        if want_receptor or want_backbone:
            q_by_sha = _queue_sha_to_row(args.queue_csv)
        n_hit = 0
        for r in rows:
            if r["state"] != args.from_state:
                continue
            if want_receptor or want_backbone:
                q = q_by_sha.get(r["prediction_sha"])
                if not q:
                    continue
                if want_receptor and (q.get("receptor_resolved") or "").upper() != want_receptor:
                    continue
                if want_backbone and (q.get("backbone") or "") != want_backbone:
                    continue
            r["state"] = args.to_state
            if args.reason:
                r["last_reason"] = args.reason
            n_hit += 1
        _save_state(args.state_csv, rows)
        fcntl.flock(fp, fcntl.LOCK_UN)
    print(f"bulk_transition: {n_hit} rows {args.from_state} -> {args.to_state}"
          + (f" receptor={want_receptor}" if want_receptor else "")
          + (f" backbone={want_backbone}" if want_backbone else ""))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="queue_ops")
    sub = p.add_subparsers(dest="cmd", required=True)

    pop = sub.add_parser("pop", help="atomically claim one pending row")
    pop.add_argument("worker_id")
    pop.add_argument("--state-csv", type=Path,
                     default=DEFAULT_POOL / "queue_state.csv")
    pop.add_argument("--queue-csv", type=Path,
                     default=DEFAULT_POOL / "queue.csv")
    pop.set_defaults(func=cmd_pop)

    mark = sub.add_parser("mark", help="mark a row done/failed/pending/paused")
    mark.add_argument("sha")
    mark.add_argument("new_state", choices=("done", "failed", "pending", "paused"))
    mark.add_argument("--reason", default="")
    mark.add_argument("--state-csv", type=Path,
                      default=DEFAULT_POOL / "queue_state.csv")
    mark.set_defaults(func=cmd_mark)

    bulk = sub.add_parser(
        "bulk_transition",
        help=("atomically flip every row from --from-state to --to-state, "
              "optionally filtered by --receptor and/or --backbone. "
              "Used by phase-4 dispatch (paused → pending) and by the "
              "STOP escape hatch (pending → paused)."),
    )
    bulk.add_argument("--from-state", required=True,
                      choices=("pending", "paused", "done", "failed", "claimed"))
    bulk.add_argument("--to-state", required=True,
                      choices=("pending", "paused", "done", "failed", "claimed"))
    bulk.add_argument("--receptor", default="",
                      help="upper-case receptor slug filter (matches queue.csv "
                           "receptor_resolved). Empty = no filter.")
    bulk.add_argument("--backbone", default="",
                      help="backbone filter. Empty = no filter.")
    bulk.add_argument("--reason", default="bulk_transition")
    bulk.add_argument("--state-csv", type=Path,
                      default=DEFAULT_POOL / "queue_state.csv")
    bulk.add_argument("--queue-csv", type=Path,
                      default=DEFAULT_POOL / "queue.csv")
    bulk.set_defaults(func=cmd_bulk_transition)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
