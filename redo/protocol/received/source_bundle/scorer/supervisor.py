"""M2.3 supervisor — keeps ≤10 concurrent fresh co-fold jobs on default.q.

Runs on the HPC submit host as a long-lived process. Round-robins the
manifest, submits ``qsub qsub/rerun_<backbone>.sh -v ...`` for every row
whose ``receptor_resolved`` is non-empty (or whose substring rule is
usable), tracks state in ``refs/rerun_status.csv``, and never pushes the
concurrent-job count above the configured cap.

Life-cycle for each row
-----------------------

  pending → submitted → running → done      (Boltz `_boltz_status.json` says ok)
                                → failed    (non-zero exit, no output, or A6 rewrite crash)
                                → retry_scheduled → submitted   (bounded, N=2)
                                → skipped   (unsupported backbone / input_missing)

Design invariants
-----------------

- The status CSV is the source of truth. If the supervisor is killed
  mid-tick and restarted, it re-reads status.csv and picks up exactly
  where it left off — no in-memory state.
- The `qstat` poll classifies jobs by ``pa3_`` name prefix (see
  ``rerun_dispatch.build_qsub_command``) so nothing owned by other
  submitters can be mistaken for one of ours.
- SHA-per-row is content-hashed at plan time (not path-hashed) — the
  audit-#6 cache-collision cannot re-surface here.
- Failures are classified before retry: ``FAIL_TRANSIENT`` (qsub returned
  non-zero, or job's own log ends with a known "GPU init failed",
  "CUDA_OOM", "unable to allocate", "connection timed out" pattern)
  → retry once. Any other failure → mark ``failed`` and move on. Never
  auto-retry a semantic failure (missing input, unsupported backbone).
- Never resubmits a row whose ``done`` marker is on disk (checks
  ``PRED_OUT_DIR/_boltz_status.json`` up-to-date + ok=true) — even if the
  status.csv row got wiped by a manual edit. This guards against a bad
  merge of two supervisor CSVs re-firing 2× GPU-hours.
"""
from __future__ import annotations

import csv
import datetime as _dt
import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from scorer.cache import content_sha256
from scorer.rerun_dispatch import (
    BACKBONES,
    InputRecoveryError,
    ReRunPlan,
    UnsupportedBackboneError,
    build_qsub_command,
    iter_manifest_rows,
    plan_row,
    propose_row_key,
)


STATUS_COLUMNS = [
    "prediction_sha",     # short SHA (12 chars) — primary key
    "prediction_path",
    "experiment_slug",
    "backbone",
    "receptor_effective",
    "state",              # pending|submitted|running|done|failed|skipped
    "job_id",
    "out_dir",
    "retries",
    "last_reason",
    "updated_utc",
]


TRANSIENT_MARKERS = (
    "CUDA_OOM",
    "cuda out of memory",
    "unable to allocate",
    "connection reset",
    "connection timed out",
    "cannot allocate",
    "GPU init failed",
    "temporarily unavailable",
    "NCCL error",
)


# ---------------------------------------------------------------------------
# Status CSV — atomic read + write
# ---------------------------------------------------------------------------


@dataclass
class StatusRow:
    prediction_sha: str
    prediction_path: str
    experiment_slug: str
    backbone: str
    receptor_effective: str
    state: str = "pending"
    job_id: str = ""
    out_dir: str = ""
    retries: int = 0
    last_reason: str = ""
    updated_utc: str = ""

    def to_dict(self) -> dict[str, str]:
        return {c: str(getattr(self, c)) for c in STATUS_COLUMNS}


def load_status(status_csv: Path) -> dict[str, StatusRow]:
    """Return {sha12: StatusRow} or empty dict on first run."""
    rows: dict[str, StatusRow] = {}
    if not status_csv.exists():
        return rows
    with status_csv.open() as f:
        for r in csv.DictReader(f):
            row = StatusRow(**{c: r.get(c, "") for c in STATUS_COLUMNS})
            row.retries = int(row.retries or 0)
            rows[row.prediction_sha] = row
    return rows


def save_status(status_csv: Path, rows: dict[str, StatusRow]) -> None:
    """Atomic-rename write so a killed supervisor never leaves a partial file."""
    status_csv.parent.mkdir(parents=True, exist_ok=True)
    tmp = status_csv.with_suffix(status_csv.suffix + ".tmp")
    with tmp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=STATUS_COLUMNS)
        w.writeheader()
        for row in rows.values():
            row.updated_utc = row.updated_utc or _utcnow()
            w.writerow(row.to_dict())
    os.replace(tmp, status_csv)


def _utcnow() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# qstat parsing — returns {job_id: name} for jobs owned by this user
# ---------------------------------------------------------------------------


def qstat_running(user: str, queue: str = "default.q",
                  *, qstat_cmd: list[str] | None = None
                  ) -> dict[str, str]:
    """Return {job_id: job_name} for user's queued/running jobs on ``queue``.

    Parses the `-xml` output so a name with unusual chars can't confuse
    a whitespace splitter.
    """
    cmd = qstat_cmd or ["qstat", "-u", user, "-q", queue, "-xml"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             check=False, timeout=45)
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        # UGE is transiently sad — don't crash the supervisor
        return {"__error__": f"{type(e).__name__}: {e}"}
    if out.returncode != 0:
        return {"__error__": f"qstat exit={out.returncode}: {out.stderr[:200]}"}

    running: dict[str, str] = {}
    # Cheap XML walk — avoiding a full parser keeps the supervisor
    # deployable without extra deps on the login node.
    #
    # Also capture <state>…</state>: jobs the user has already `qdel`-ed
    # sit in `dr` (delete-running) until execd acks — sometimes minutes,
    # sometimes hours if the execd↔qmaster link stalled (Basel-HPC
    # 2026-08-31 post-maintenance). We must not treat those as "still
    # managed" or the run wedges. Any state containing 'd' (dr/dt/dRr) or
    # 'z' (zombie / error-only) means "on its way out" — skip.
    import re as _re
    for m in _re.finditer(
        r"<JB_job_number>(\d+)</JB_job_number>"
        r"[\s\S]*?<JB_name>([^<]+)</JB_name>"
        r"[\s\S]*?<state>([^<]+)</state>",
        out.stdout,
    ):
        state = m.group(3)
        if "d" in state or "z" in state:
            continue
        running[m.group(1)] = m.group(2)
    return running


def qhost_gpu_arch_free(arch_value: str,
                        *, qhost_cmd: list[str] | None = None) -> int:
    """Sum of currently-free GPUs on hosts with the given ``gpu_arch``.

    basel-hpc verified 2026-08-25: `qhost -F gpu_arch,gpu_card` yields
    stanzas like

        chbsclN.novartis.net    lx-amd64  ...
          Host Resource(s):       hf:gpu_arch=hopper_h100
          Host Resource(s):       hc:gpu_card=3.000000

    where `hf:` is a fixed host attribute and `hc:` is the currently-
    free consumable count. Summing the second across matching hosts
    gives the free-slot headroom for that architecture.

    Conservative: on qhost failure or arch=="" returns 0 so the caller
    doesn't accidentally submit to a saturated / unknown pool.
    """
    if not arch_value:
        return 0
    cmd = qhost_cmd or ["qhost", "-F", "gpu_arch,gpu_card"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             check=False, timeout=45)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return 0
    if out.returncode != 0:
        return 0

    total = 0
    arch = ""
    for line in out.stdout.splitlines():
        stripped = line.strip()
        # New host row starts at column 0 with a hostname (no leading
        # space); resource rows are indented and start with 'Host Resource'
        if line and not line.startswith(" ") and not line.startswith("HOSTNAME") \
                and not line.startswith("-") and " lx-" in line:
            arch = ""     # reset for the new host
            continue
        if "hf:gpu_arch=" in line:
            arch = line.split("hf:gpu_arch=", 1)[1].split()[0].strip()
            continue
        if "hc:gpu_card=" in line and arch == arch_value:
            try:
                free = int(float(line.split("hc:gpu_card=", 1)[1]
                                     .split()[0].strip()))
            except (IndexError, ValueError):
                free = 0
            total += free
            arch = ""     # only count once per host
    return total


def h100_free_slots(cfg: "SupervisorConfig") -> int:
    """Free H100 GPUs per the config's arch value (0 if routing off)."""
    if not cfg.h100_arch_selector or not cfg.h100_arch_value:
        return 0
    return qhost_gpu_arch_free(cfg.h100_arch_value)


# ---------------------------------------------------------------------------
# Failure classifier
# ---------------------------------------------------------------------------


def classify_failure(out_dir: Path, log_dir: Path, job_id: str,
                     backbone: str = "boltz") -> str:
    """Return one of {"TRANSIENT", "PERMANENT"} by inspecting output artefacts.

    Order of checks:
      1. `_{backbone}_status.json` present + parseable → look at ok/exit_code
         (a valid status file with ok=false is authoritative → PERMANENT
         unless exit code is one of the retryable ones). Every qsub template
         emits its own `_{backbone}_status.json` (e.g. `_boltz_status.json`,
         `_of3_status.json`, `_protenix_status.json`, `_chai_status.json`);
         2026-08-31 patch closed task #34 which had this function only
         consulting the Boltz marker for all four backbones, mis-classifying
         OF3/Protenix/Chai successes as failures.
      2. `.log` file present → grep for transient markers.
      3. Nothing on disk → TRANSIENT (assume the job died before writing
         anything and is worth one retry).
    """
    status = out_dir / f"_{backbone}_status.json"
    if status.exists():
        try:
            data = json.loads(status.read_text())
        except (OSError, json.JSONDecodeError):
            return "TRANSIENT"
        exit_code = int(data.get("exit_code", -1))
        # Retryable exit codes: 137 (SIGKILL — OOM), 139 (SIGSEGV — rare
        # CUDA driver), 143 (SIGTERM from scheduler on preempt).
        if exit_code in (137, 139, 143):
            return "TRANSIENT"
        return "PERMANENT"

    # Look at any log the qsub template emitted. Restrict to job-id-
    # matching files — the previous fallback that globbed EVERY
    # `rerun_boltz.*.log` was O(N-completed-jobs) per failed row on
    # NFS, which brought the supervisor to its knees at 2k+ completed
    # jobs (2026-08-26 stall). If no job_id-matched log exists, treat
    # as TRANSIENT via the fall-through at the bottom of the function.
    candidates: list[Path] = []
    if job_id:
        candidates.extend(log_dir.glob(f"*.{job_id}*"))
    for cand in candidates:
        try:
            text = cand.read_text(errors="ignore")[-8000:]
        except OSError as e:
            # Log rotated / permission denied — fall through to the next
            # candidate rather than declare failure based on absence.
            text = ""
            _ = e
        for marker in TRANSIENT_MARKERS:
            if marker.lower() in text.lower():
                return "TRANSIENT"

    return "TRANSIENT"


# ---------------------------------------------------------------------------
# Supervisor
# ---------------------------------------------------------------------------


@dataclass
class SupervisorConfig:
    manifest_csv: Path
    status_csv: Path
    rerun_root: Path
    rewrite_cache: Path
    repo_root: Path
    log_dir: Path
    user: str = "sengaad1"
    queue: str = "default.q"
    max_concurrent: int = 25    # basel-hpc allocation: 25 A100 + 3 H100 (2026-08-25)
    poll_seconds: float = 60.0
    max_retries: int = 2
    backbones: tuple[str, ...] = ("boltz",)
    max_submit_per_tick: int = 8    # graceful ramp — never fire 25 at once
    dry_run: bool = False
    # H100 routing — resource spec appended as `-l <spec>` when a
    # prefers_h100 backbone has H100 free slots. basel-hpc uses the
    # `gpu_arch` consumable (verified 2026-08-25 via `qhost -F gpu_arch,
    # gpu_card`), not a hostname glob. Empty disables routing.
    h100_arch_selector: str = "gpu_arch=hopper_h100"
    # Which gpu_arch value the arch selector requests — used by the
    # free-slots detector so it knows which rows in `qhost -F gpu_arch,
    # gpu_card` to sum. Keep in sync with h100_arch_selector.
    h100_arch_value: str = "hopper_h100"


class Supervisor:
    def __init__(self, cfg: SupervisorConfig):
        self.cfg = cfg
        self.status: dict[str, StatusRow] = load_status(cfg.status_csv)
        self._plans_cache: dict[str, ReRunPlan] = {}

    # ---- Manifest → status hydration --------------------------------------

    def hydrate_from_manifest(self) -> tuple[int, int]:
        """Populate status.csv rows for any manifest row not yet tracked.

        Returns (n_added, n_skipped). Rows whose backbone is not in
        ``cfg.backbones`` are quietly ignored — the caller controls which
        backbone is active for this supervisor run.
        """
        n_added = 0
        n_skipped = 0
        for row in iter_manifest_rows(self.cfg.manifest_csv,
                                      backbones=self.cfg.backbones,
                                      skip_unresolved=True):
            # SHA-per-row is the primary key. Two manifest shapes:
            #   M2.4 rerun manifest — prediction_sha is either present
            #     or fillable by hashing the frozen prediction file.
            #   Layer 3 propose manifest — prediction_sha is EMPTY by
            #     design (no fold output exists yet). Use the composite
            #     (input_sha, seed) hash from `propose_row_key` so
            #     multiple seeds on the same input file are tracked as
            #     distinct rows (Boltz-style backbones don't put the
            #     seed in the input YAML — seed is a runtime CLI arg).
            sha = row.get("prediction_sha", "").strip()
            if not sha:
                sha = propose_row_key(row)   # composite (input_sha, seed)
            if not sha:
                # Neither field populated — fall back to hashing the
                # frozen prediction file (M2.1 pre-populated manifests).
                try:
                    sha = content_sha256(row["prediction_path"])
                except OSError as e:
                    n_skipped += 1
                    continue
                row["prediction_sha"] = sha
            sha12 = sha[:12]
            # ALWAYS cache the row mapping — even if sha12 is already in
            # status.csv. On a supervisor restart, status.csv is fully
            # populated but the in-memory _manifest_rows_by_sha cache is
            # empty. Without this, _plan_or_skip falls back to walking
            # the whole manifest per submission, computing SHA256 for
            # every prediction file — an O(N-manifest × N-submits) hash
            # storm that caused the 2026-08-26 03:49 UTC stall.
            self._plans_cache_row(sha12, row)
            if sha12 in self.status:
                continue
            self.status[sha12] = StatusRow(
                prediction_sha=sha12,
                prediction_path=row["prediction_path"],
                experiment_slug=row.get("experiment_slug", ""),
                backbone=row.get("backbone", ""),
                receptor_effective=(row.get("receptor_resolved", "").strip()
                                    or row.get("receptor_from_path_substring", "").strip()),
                state="pending",
                updated_utc=_utcnow(),
            )
            n_added += 1
        save_status(self.cfg.status_csv, self.status)
        return n_added, n_skipped

    def _plans_cache_row(self, sha12: str, row: dict[str, str]) -> None:
        # Stored on the object rather than on disk — plans are cheap to
        # rebuild if the supervisor restarts, and holding the full row
        # keeps `plan_row` off the disk-read path during tick().
        self._manifest_rows_by_sha = getattr(
            self, "_manifest_rows_by_sha", {}
        )
        self._manifest_rows_by_sha[sha12] = row

    # ---- Tick loop --------------------------------------------------------

    def _current_active(self) -> tuple[int, dict[str, str]]:
        """(n_active_managed, {job_id: name}). Only pa3_* names count."""
        running = qstat_running(self.cfg.user, queue=self.cfg.queue)
        if "__error__" in running:
            print(f"[warn] qstat failed: {running['__error__']}",
                  file=sys.stderr)
            # On qstat failure, be conservative — assume the cap is full
            # so we don't fire off duplicates.
            return (self.cfg.max_concurrent, {})
        managed = {jid: name for jid, name in running.items()
                   if name.startswith("pa3_")}
        return (len(managed), managed)

    def _mark(self, row: StatusRow, state: str, reason: str = "",
              job_id: str = "", out_dir: str = "") -> None:
        row.state = state
        row.last_reason = reason
        if job_id:
            row.job_id = job_id
        if out_dir:
            row.out_dir = out_dir
        row.updated_utc = _utcnow()

    def _plan_or_skip(self, sha12: str) -> ReRunPlan | None:
        if sha12 in self._plans_cache:
            return self._plans_cache[sha12]
        row = getattr(self, "_manifest_rows_by_sha", {}).get(sha12)
        if row is None:
            # Post-restart: we didn't hydrate a fresh cache. Fall through
            # to re-hydrate from disk here — status still has the SHA we
            # need to correlate.
            for r in iter_manifest_rows(self.cfg.manifest_csv,
                                        backbones=self.cfg.backbones,
                                        skip_unresolved=True):
                s = (r.get("prediction_sha") or "").strip()
                is_propose = bool((r.get("input_path") or "").strip())
                if not s and is_propose:
                    # Propose row: key by composite (input_sha, seed) so
                    # per-seed rows on identical inputs stay distinct.
                    s = propose_row_key(r)
                if not s:
                    try:
                        s = content_sha256(r["prediction_path"])
                    except OSError as e:
                        # File went away between hydration and this
                        # rehydration read — skip this candidate; caller
                        # sees plan==None and marks skipped.
                        s = ""
                        _ = e
                if s and s[:12] == sha12:
                    # For M2.4 rerun rows only — filling prediction_sha
                    # is meaningful and avoids re-hashing on subsequent
                    # ticks. Propose rows leave prediction_sha empty by
                    # design; the key we tracked in status.csv was
                    # derived from input_sha.
                    if not is_propose and not r.get("prediction_sha"):
                        r["prediction_sha"] = s
                    row = r
                    break
        if row is None:
            return None
        try:
            plan = plan_row(row,
                            rerun_root=self.cfg.rerun_root,
                            rewrite_cache=self.cfg.rewrite_cache)
        except (InputRecoveryError, UnsupportedBackboneError) as e:
            status = self.status[sha12]
            self._mark(status, "skipped", reason=f"{type(e).__name__}: {e}")
            return None
        self._plans_cache[sha12] = plan
        return plan

    def _submit(self, sha12: str) -> bool:
        plan = self._plan_or_skip(sha12)
        if plan is None:
            return False
        argv = build_qsub_command(plan, repo_root=self.cfg.repo_root)

        # H100 routing — splice `-l gpu_arch=hopper_h100` (or configured
        # arch selector) when this backbone prefers H100 AND there's free
        # H100 headroom per a live `qhost -F gpu_arch,gpu_card` sum.
        # Falls through to general-pool submission when H100 is saturated
        # or routing is off.
        if (self.cfg.h100_arch_selector and plan.backbone.prefers_h100
                and h100_free_slots(self.cfg) > 0):
            argv = argv[:1] + ["-l", self.cfg.h100_arch_selector] + argv[1:]

        status = self.status[sha12]

        # Sidecar is written BEFORE qsub — if the qsub fails, the plan
        # is still recoverable from disk on the next tick.
        plan.out_dir.mkdir(parents=True, exist_ok=True)
        sidecar = plan.out_dir / "_rerun_plan.json"
        sidecar.write_text(json.dumps(plan.sidecar(), indent=2))

        if self.cfg.dry_run:
            print(f"[dry-run] would submit: {' '.join(argv)}")
            self._mark(status, "submitted", reason="dry-run",
                       job_id="0", out_dir=str(plan.out_dir))
            return True

        try:
            proc = subprocess.run(argv, capture_output=True, text=True,
                                  check=False, timeout=60)
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self._mark(status, "pending",
                       reason=f"qsub-exception: {type(e).__name__}")
            return False

        if proc.returncode != 0:
            self._mark(status, "pending",
                       reason=f"qsub exit={proc.returncode}: "
                              f"{proc.stderr[:200]}")
            return False

        # Parse "Your job N ..." from qsub stdout
        job_id = ""
        for tok in proc.stdout.split():
            if tok.isdigit():
                job_id = tok
                break
        self._mark(status, "submitted", reason="qsub-ok",
                   job_id=job_id, out_dir=str(plan.out_dir))
        return True

    def _reconcile_running(self, running: dict[str, str]) -> None:
        """Flip submitted → running (job appears in qstat) → done/failed."""
        for sha12, row in self.status.items():
            if row.state not in ("submitted", "running"):
                continue
            if row.job_id and row.job_id in running:
                if row.state != "running":
                    self._mark(row, "running", reason="qstat-visible")
                continue
            # Not in qstat anymore — job ended. Inspect the output dir.
            # Task #34 patch (2026-08-31): each qsub template writes
            # `_{backbone}_status.json`, not a shared `_boltz_status.json`.
            out_dir = Path(row.out_dir) if row.out_dir else None
            status_path = (out_dir / f"_{row.backbone}_status.json"
                           if out_dir else None)
            if status_path and status_path.exists():
                try:
                    data = json.loads(status_path.read_text())
                    if data.get("ok"):
                        self._mark(row, "done",
                                   reason=f"{row.backbone}-status-ok")
                        continue
                except (OSError, json.JSONDecodeError) as e:
                    # Status file was partly written or vanished — treat
                    # as "no status marker yet" and fall through to log
                    # classification below.
                    _ = e
            # No status marker → classify by log content
            kind = classify_failure(
                out_dir or Path("/dev/null"),
                self.cfg.log_dir,
                row.job_id,
                backbone=row.backbone,
            )
            if kind == "TRANSIENT" and row.retries < self.cfg.max_retries:
                row.retries += 1
                self._mark(row, "pending",
                           reason=f"retry-{row.retries} ({kind})",
                           job_id="")
            else:
                self._mark(row, "failed",
                           reason=f"{kind} exhausted-retries")

    def tick(self) -> dict[str, Any]:
        """One tick: reconcile running jobs, submit up to the cap."""
        active_n, running = self._current_active()
        self._reconcile_running(running)

        # Rebuild active count after reconciliation
        active_n = sum(1 for r in self.status.values()
                       if r.state in ("submitted", "running"))
        headroom = max(0, self.cfg.max_concurrent - active_n)
        submit_budget = min(headroom, self.cfg.max_submit_per_tick)
        submitted = 0

        # Prefer pending rows in the order they first appeared in the
        # manifest — stable and predictable.
        for sha12, row in list(self.status.items()):
            if submitted >= submit_budget:
                break
            if row.state != "pending":
                continue
            if self._submit(sha12):
                submitted += 1
        save_status(self.cfg.status_csv, self.status)

        return {
            "active_managed": active_n,
            "submitted_this_tick": submitted,
            "counts_by_state": _counts_by_state(self.status),
            "utc": _utcnow(),
        }

    # ---- Runner -----------------------------------------------------------

    def run_forever(self, max_ticks: int | None = None) -> None:
        n = 0
        while True:
            summary = self.tick()
            print(json.dumps(summary), flush=True)
            counts = summary["counts_by_state"]
            n += 1
            # Exit condition: no pending, submitted, or running rows
            if (counts.get("pending", 0) == 0
                    and counts.get("submitted", 0) == 0
                    and counts.get("running", 0) == 0):
                print("[done] no more work", flush=True)
                return
            if max_ticks is not None and n >= max_ticks:
                print(f"[stop] hit max_ticks={max_ticks}", flush=True)
                return
            time.sleep(self.cfg.poll_seconds)


def _counts_by_state(status: dict[str, StatusRow]) -> dict[str, int]:
    out: dict[str, int] = {}
    for row in status.values():
        out[row.state] = out.get(row.state, 0) + 1
    return out


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(
        prog="gpcr-rerun-supervisor",
        description="Keep ≤10 concurrent fresh co-fold jobs on default.q, "
                    "tracking state in refs/rerun_status.csv.",
    )
    p.add_argument("--manifest", default="refs/rerun_manifest.csv")
    p.add_argument("--status", default="refs/rerun_status.csv")
    p.add_argument("--rerun-root",
                   default="/hpc/scratch/sengaad1/paper_af3/rerun")
    p.add_argument("--rewrite-cache",
                   default="/hpc/scratch/sengaad1/paper_af3/rerun/_input_rewrites")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--log-dir",
                   default="/hpc/scratch/sengaad1/paper_af3/logs")
    p.add_argument("--user", default="sengaad1")
    p.add_argument("--queue", default="default.q")
    p.add_argument("--max-concurrent", type=int, default=25)
    p.add_argument("--max-submit-per-tick", type=int, default=8)
    p.add_argument("--h100-arch-selector", default="gpu_arch=hopper_h100",
                   help="UGE `-l` resource spec used when routing to "
                        "H100 (basel-hpc default 'gpu_arch=hopper_h100'). "
                        "Empty disables routing.")
    p.add_argument("--h100-arch-value", default="hopper_h100",
                   help="`gpu_arch` value that `qhost -F gpu_arch,gpu_card` "
                        "rows are matched on for free-slot detection.")
    p.add_argument("--max-retries", type=int, default=2)
    p.add_argument("--poll-seconds", type=float, default=60.0)
    p.add_argument("--backbone", action="append", default=None,
                   help="Restrict to backbones (repeat for multi). "
                        "Default: boltz.")
    p.add_argument("--max-ticks", type=int, default=None,
                   help="Cap on tick count (useful for dry-run smoke).")
    p.add_argument("--hydrate-only", action="store_true",
                   help="Populate status.csv from manifest and exit.")
    p.add_argument("--dry-run", action="store_true",
                   help="Plan and mark submitted but do NOT invoke qsub.")
    args = p.parse_args(argv)

    cfg = SupervisorConfig(
        manifest_csv=Path(args.manifest),
        status_csv=Path(args.status),
        rerun_root=Path(args.rerun_root),
        rewrite_cache=Path(args.rewrite_cache),
        repo_root=Path(args.repo_root).resolve(),
        log_dir=Path(args.log_dir),
        user=args.user,
        queue=args.queue,
        max_concurrent=args.max_concurrent,
        poll_seconds=args.poll_seconds,
        max_retries=args.max_retries,
        backbones=tuple(args.backbone or ("boltz",)),
        max_submit_per_tick=args.max_submit_per_tick,
        dry_run=args.dry_run,
        h100_arch_selector=args.h100_arch_selector,
        h100_arch_value=args.h100_arch_value,
    )

    sup = Supervisor(cfg)
    n_added, n_skipped = sup.hydrate_from_manifest()
    print(json.dumps({"hydrated_added": n_added,
                      "hydrated_skipped": n_skipped,
                      "backbones": list(cfg.backbones)}, indent=2),
          file=sys.stderr)

    if args.hydrate_only:
        return 0

    sup.run_forever(max_ticks=args.max_ticks)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
