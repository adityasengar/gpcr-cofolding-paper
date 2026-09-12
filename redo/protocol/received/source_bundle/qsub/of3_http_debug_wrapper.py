"""OF3 HTTP-logging wrapper — one-shot diagnostic 2026-09-01.

Monkey-patches `requests.get` / `requests.post` at module level to append
one JSONL entry per HTTP call (endpoint, timeout param, duration, status,
short body preview / error), then invokes OpenFold-3's CLI unchanged.
Purpose: determine whether the OF3 ColabFold flakiness surfaced by the
post-warm timings is a genuine 6.02s-timeout problem or a cache-miss
(OF3's cache key doesn't match what msa_prewarm registered).

Usage (from a qsub or an interactive shell):
    OF3_HTTP_LOG=/hpc/scratch/.../logs/of3_http.jsonl \
    python3 /home/sengaad1/paper_af3/qsub/of3_http_debug_wrapper.py \
        predict --query-json ... --output-dir ... --use-msa-server true ...

The wrapper leaves stdout/stderr alone — OF3's own logging still flows.
"""
from __future__ import annotations

import functools
import json
import os
import sys
import time
from pathlib import Path

import requests


def _install_http_probe() -> None:
    log_path = Path(os.environ.get(
        "OF3_HTTP_LOG",
        "/hpc/scratch/sengaad1/paper_af3/logs/of3_http.jsonl",
    ))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text("")  # fresh log per invocation

    _orig_get = requests.get
    _orig_post = requests.post

    def _record(method: str, url: str, kwargs: dict,
                resp, err, dt_s: float) -> None:
        entry = {
            "t": time.strftime("%H:%M:%S", time.gmtime()),
            "method": method,
            "url": url,
            "timeout": kwargs.get("timeout"),
            "dt_s": round(dt_s, 3),
        }
        if err is not None:
            entry["err"] = f"{type(err).__name__}: {str(err)[:240]}"
        else:
            entry["status"] = resp.status_code
            try:
                entry["body"] = resp.text[:400]
            except Exception:  # noqa: BLE001
                entry["body"] = "<binary>"
        with log_path.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def _wrap_get(*args, **kwargs):
        url = args[0] if args else kwargs.get("url", "?")
        t0 = time.time()
        try:
            resp = _orig_get(*args, **kwargs)
            _record("GET", url, kwargs, resp, None, time.time() - t0)
            return resp
        except Exception as e:  # noqa: BLE001
            _record("GET", url, kwargs, None, e, time.time() - t0)
            raise

    def _wrap_post(*args, **kwargs):
        url = args[0] if args else kwargs.get("url", "?")
        t0 = time.time()
        try:
            resp = _orig_post(*args, **kwargs)
            _record("POST", url, kwargs, resp, None, time.time() - t0)
            return resp
        except Exception as e:  # noqa: BLE001
            _record("POST", url, kwargs, None, e, time.time() - t0)
            raise

    requests.get = _wrap_get
    requests.post = _wrap_post
    print(f"[of3_http_debug] logging HTTP to {log_path}", flush=True)


def main() -> int:
    _install_http_probe()
    # Re-execute OF3's `run_openfold` CLI in-process so the monkey-patches
    # apply to every requests call under it (including deep imports).
    from openfold3.run_openfold import cli
    # argv[0] cosmetic — OF3's CLI reads sys.argv[1:] as the actual args.
    sys.argv[0] = "run_openfold"
    return cli() or 0


if __name__ == "__main__":
    raise SystemExit(main())
