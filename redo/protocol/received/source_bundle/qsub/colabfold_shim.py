"""colabfold_shim.py — generic timeout patch + retry logging for any
inference backbone that talks to `api.colabfold.com`.

Third appearance of the same class of bug:
  - chai-lab 0.6.1  — hardcoded `timeout=6.02` on POST /ticket/msa and
                       GET /ticket/{ID}. Now unused (chai runs via
                       --msa-directory in Block A).
  - openfold3      — hardcoded `timeout=6.02` on
                       GET /result/download/{ID} — surfaced 2026-09-01
                       (91 ReadTimeouts on ONE prediction, cache hit
                       confirmed by POST /ticket/msa returning
                       status=COMPLETE in 0.7 s).
  - (next)         — whatever endpoint appears in Blocks B/C/D.

Rather than patch per-endpoint, this shim wraps `requests.get` and
`requests.post` at module level and enforces a floor on the timeout
tuple for any request whose URL contains `api.colabfold.com`:

    (connect_min = 30 s, read_min = 600 s)

Anything the caller passes below that floor is silently bumped up.
Anything already at or above the floor is left alone.

The shim also records a summary of ColabFold HTTP activity to a
sidecar (`_colabfold_http_summary.json`) so retry counts and total
HTTP wait are visible to post-run analysis across all 5,500
predictions — not just the one the human happens to measure.

Usage from a qsub launcher:

    export COLABFOLD_SIDECAR=$PRED_OUT_DIR/_colabfold_http_summary.json
    python3 /path/to/colabfold_shim.py of3 predict [OF3 args...]
    python3 /path/to/colabfold_shim.py chai fold  [chai args...]
    python3 /path/to/colabfold_shim.py boltz predict [Boltz args...]

Env:
    COLABFOLD_SIDECAR   path to write the summary JSON (default:
                        `_colabfold_http_summary.json` in cwd)
    COLABFOLD_MIN_READ  read-timeout floor in seconds (default 600)
    COLABFOLD_MIN_CONN  connect-timeout floor in seconds (default 30)
"""
from __future__ import annotations

import atexit
import json
import os
import sys
import time
from pathlib import Path

import requests

# Module-level, safe under torch DataLoader worker re-import (spawn mode).
# The argv-pop that dispatches the backbone CLI lives inside the
# `if __name__ == "__main__"` guard at the bottom — otherwise every
# worker subprocess re-runs the pop and corrupts sys.argv, which is
# exactly what killed the first smoke test (2026-09-01, job 34913980:
# workers crashed with "DataLoader worker exited unexpectedly").
MIN_READ = float(os.environ.get("COLABFOLD_MIN_READ", "600"))
MIN_CONN = float(os.environ.get("COLABFOLD_MIN_CONN", "30"))
SIDECAR = Path(os.environ.get("COLABFOLD_SIDECAR",
                              "_colabfold_http_summary.json"))

_stats = {
    "backbone": None,  # populated by the __main__ block once the arg is popped
    "policy": {"min_connect_s": MIN_CONN, "min_read_s": MIN_READ},
    "colabfold_calls": 0,          # total HTTP calls to api.colabfold.com
    "colabfold_retries": 0,        # calls that hit ReadTimeout (before the shim's floor)
    "colabfold_http_wait_s": 0.0,  # cumulative wall-time inside colabfold HTTP calls
    "cache_hit_immediate": False,  # POST /ticket/... returned status=COMPLETE on first call
    "colabfold_success_calls": 0,
    "colabfold_error_calls": 0,
    "endpoints_seen": {},          # normalised-endpoint → call count
}

_orig_get = requests.get
_orig_post = requests.post


def _norm_url(url: str) -> str:
    """Replace ticket / result IDs with '<ID>' so counts aggregate."""
    for pat in ("/ticket/", "/result/download/"):
        if pat in url:
            head, _tail = url.split(pat, 1)
            return head + pat + "<ID>"
    return url


def _bump_timeout(kwargs: dict) -> dict:
    """Raise the timeout to the floor if it is below.  In-place OK because we
    always pass a fresh copy of kwargs from the wrapper."""
    t = kwargs.get("timeout")
    if t is None:
        kwargs["timeout"] = (MIN_CONN, MIN_READ)
    elif isinstance(t, tuple):
        c, r = t
        kwargs["timeout"] = (max(c, MIN_CONN), max(r, MIN_READ))
    else:  # scalar — treat as read-only
        kwargs["timeout"] = (MIN_CONN, max(float(t), MIN_READ))
    return kwargs


def _is_colabfold(url: str) -> bool:
    return "api.colabfold.com" in url


def _record(url: str, dt: float, err: BaseException | None) -> None:
    _stats["colabfold_calls"] += 1
    _stats["colabfold_http_wait_s"] += dt
    key = _norm_url(url)
    _stats["endpoints_seen"][key] = _stats["endpoints_seen"].get(key, 0) + 1
    if err is None:
        _stats["colabfold_success_calls"] += 1
    else:
        _stats["colabfold_error_calls"] += 1
        if isinstance(err, requests.exceptions.ReadTimeout):
            _stats["colabfold_retries"] += 1


def _wrap(fn, method: str):
    def inner(*args, **kwargs):
        url = args[0] if args else kwargs.get("url", "")
        cf = _is_colabfold(url)
        if cf:
            kwargs = _bump_timeout(dict(kwargs))
        t0 = time.time()
        try:
            resp = fn(*args, **kwargs)
            dt = time.time() - t0
            if cf:
                _record(url, dt, None)
                # Immediate-cache-hit detection: POST /ticket/... on the
                # first call returns {"status": "COMPLETE"} when the
                # ColabFold server already has this sequence's MSA
                # cached. If it's PENDING/RUNNING, the pre-warm didn't
                # cover this sequence and OF3/chai will fall into the
                # normal ticket-poll loop.
                if (method == "POST"
                        and "/ticket/" in url
                        and _stats["colabfold_calls"] == 1):
                    try:
                        body = resp.json()
                        if body.get("status") == "COMPLETE":
                            _stats["cache_hit_immediate"] = True
                    except Exception:  # noqa: BLE001
                        pass
            return resp
        except BaseException as e:  # noqa: BLE001
            dt = time.time() - t0
            if cf:
                _record(url, dt, e)
            raise
    return inner


requests.get = _wrap(_orig_get, "GET")
requests.post = _wrap(_orig_post, "POST")


def _write_sidecar() -> None:
    try:
        SIDECAR.parent.mkdir(parents=True, exist_ok=True)
        with SIDECAR.open("w") as f:
            json.dump(_stats, f, indent=2)
        print(
            f"[colabfold_shim] backbone={_stats.get('backbone')} "
            f"calls={_stats['colabfold_calls']} "
            f"retries={_stats['colabfold_retries']} "
            f"wait={_stats['colabfold_http_wait_s']:.1f}s "
            f"cache_hit_immediate={_stats['cache_hit_immediate']} "
            f"→ {SIDECAR}",
            flush=True,
        )
    except Exception as e:  # noqa: BLE001
        print(f"[colabfold_shim] failed to write sidecar: {e}",
              file=sys.stderr, flush=True)


def _dispatch(backbone: str) -> int:
    """Hand control to the requested backbone's CLI. Only runs in the
    main process (guarded by `if __name__ == '__main__'`); worker
    subprocesses re-import this module but skip this dispatch."""
    if backbone == "of3":
        from openfold3.run_openfold import cli
        sys.argv[0] = "run_openfold"
        return cli() or 0
    if backbone == "chai":
        sys.argv[0] = "chai-lab"
        try:
            from chai_lab.main import cli as chai_cli
            return chai_cli() or 0
        except ImportError:
            import runpy
            runpy.run_module("chai_lab.main", run_name="__main__")
            return 0
    if backbone == "boltz":
        sys.argv[0] = "boltz"
        try:
            from boltz.main import cli as boltz_cli
            return boltz_cli() or 0
        except ImportError:
            import runpy
            runpy.run_module("boltz.main", run_name="__main__")
            return 0
    print(f"unknown backbone: {backbone!r}. Use one of: chai, of3, boltz.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    # Only pop and dispatch from the main process; worker subprocesses
    # under torch multiprocessing's spawn mode re-import this module
    # and would otherwise run this code with sys.argv already trimmed.
    if len(sys.argv) < 2:
        print(
            "usage: colabfold_shim.py <backbone> <subcommand> [args...]\n"
            "  backbones: chai | of3 | boltz",
            file=sys.stderr,
        )
        raise SystemExit(2)
    _backbone = sys.argv.pop(1)
    _stats["backbone"] = _backbone
    atexit.register(_write_sidecar)
    raise SystemExit(_dispatch(_backbone))
