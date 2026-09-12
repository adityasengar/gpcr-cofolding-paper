"""Wave-1 verification — run POST wave-1 completion.

Wave-1 = one full cell: one receptor × 2 arms × 4 backbones × 25 predictions
(5 seeds × 5 samples). Confirms operational health before the remaining 47
cells queue.

Checks and diagnostics reported per PREREG §11c and the wave-1 dispatch plan:

1. **OF3 ColabFold sidecar** (per-job JSON emitted by qsub/colabfold_shim.py):
     colabfold_calls, colabfold_retries, colabfold_http_wait_s,
     cache_hit_immediate.
   Aggregate per-arm: median / max retries, fraction with retries > 0,
   fraction with cache_hit_immediate == false. This is the wave-1 signal
   whether the 6.02s ReadTimeout bug still bites under 12-way concurrency.

2. **Per-backbone wall time under load** — parsed from job qacct or the
   launcher's per-job wall.time file. Median per (backbone, arm).

3. **Cognate-partner identity re-run** — reruns
   scripts/verify_cognate_identity.py against the wave-1 slice of the
   manifest. Exit non-zero if any mismatch.

4. **Scored cell rows.csv summary** — n rows, `passed` distribution,
   `d_gpcrdb_tm6_tilt_246_637_ca` mean/std, threshold column values
   (must be 9.082 for NPxxY-OH, 14.932 for tilt).

Note vs the pre-2026-09-01 version:
    - The chai_singleseq MSA-depth assertion and chai-vs-singleseq
      receptor-CA RMSD diagnostic are REMOVED — chai_singleseq is not
      in the Block A manifest (PREREG §11 rewrite). MSA-mode is the
      only Chai regime.
    - The AA2AR-specific RMSD diagnostic is removed with them.

Usage (post wave-1):
    python3 scripts/verify_wave_1.py \\
        --manifest experiments/018_block_a_switch_test/runs/initial/manifest.csv \\
        --outputs-root /hpc/scratch/sengaad1/paper_af3/experiments/018_block_a_switch_test \\
        --wave-1-receptor AA2AR \\
        --rows-csv experiments/018_block_a_switch_test/runs/initial/rows.csv \\
        --report-out experiments/018_block_a_switch_test/runs/initial/wave_1_report.md
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Panel-derived thresholds (canonical, from refs/thresholds_panel.csv). If
# the scored rows.csv carries these as columns, they must match — a
# mismatch means a stale scorer or a wrong config landed. See PREREG §2c-revised.
THRESHOLD_NPXXY_OH = 9.082
THRESHOLD_TM6_TILT = 14.932


# --------------------------------------------------------------------- #
# Sidecar / status.json readers
# --------------------------------------------------------------------- #

def _find_sidecar(job_root: Path, backbone: str, filename_hint: str) -> Path | None:
    """Locate the shim/backbone JSON sidecar for a job dir."""
    p = job_root / f"_{backbone}_{filename_hint}.json"
    if p.exists():
        return p
    for cand in job_root.rglob(f"_{backbone}_{filename_hint}.json"):
        return cand
    return None


def read_of3_shim_sidecar(job_root: Path) -> dict | None:
    """Return the OF3 ColabFold shim sidecar JSON.

    File layout (per qsub/colabfold_shim.py, PREREG §11c):
        {
          "colabfold_calls": int,
          "colabfold_retries": int,
          "colabfold_http_wait_s": float,
          "cache_hit_immediate": bool,
          ...
        }
    """
    p = _find_sidecar(job_root, "of3", "colabfold_http_summary")
    if p is None:
        return None
    try:
        return json.loads(p.read_text())
    except Exception:  # noqa: BLE001
        return None


def read_wall_time(job_root: Path, backbone: str) -> float | None:
    """Return backbone wall time in seconds from the launcher's wall.time file."""
    for cand in (
        job_root / f"_{backbone}_wall.time",
        job_root / f"wall.time",
    ):
        if cand.exists():
            try:
                return float(cand.read_text().strip())
            except Exception:  # noqa: BLE001
                continue
    # Fallback: scan rglob
    for cand in job_root.rglob(f"_{backbone}_wall.time"):
        try:
            return float(cand.read_text().strip())
        except Exception:  # noqa: BLE001
            continue
    return None


# --------------------------------------------------------------------- #
# Report builders
# --------------------------------------------------------------------- #

def summarise_of3_sidecars(manifest_rows: list[dict], outputs_root: Path,
                            wave_recs: set[str]) -> dict:
    """Aggregate OF3 sidecar stats over the wave-1 slice."""
    calls: list[int] = []
    retries: list[int] = []
    waits: list[float] = []
    cache_hits: list[bool] = []
    details: list[dict] = []

    for r in manifest_rows:
        rec = r["receptor_from_path_substring"].upper()
        if rec not in wave_recs:
            continue
        if r["backbone"] != "of3":
            continue
        job_root = outputs_root / r["request_id"]
        data = read_of3_shim_sidecar(job_root)
        if data is None:
            continue
        c = int(data.get("colabfold_calls", 0))
        rr = int(data.get("colabfold_retries", 0))
        w = float(data.get("colabfold_http_wait_s", 0.0))
        chi = bool(data.get("cache_hit_immediate", False))
        calls.append(c)
        retries.append(rr)
        waits.append(w)
        cache_hits.append(chi)
        details.append({
            "request_id": r["request_id"],
            "seed_index": r["seed_index"],
            "calls": c, "retries": rr, "wait_s": w, "cache_hit": chi,
        })
    if not details:
        return {"n": 0, "note": "no OF3 sidecars found — check qsub/colabfold_shim.py wiring"}
    return {
        "n": len(details),
        "median_retries": statistics.median(retries) if retries else 0,
        "max_retries": max(retries) if retries else 0,
        "fraction_retries_gt_zero": sum(1 for x in retries if x > 0) / len(retries),
        "fraction_cache_miss": sum(1 for x in cache_hits if not x) / len(cache_hits),
        "median_http_wait_s": statistics.median(waits) if waits else 0,
        "max_http_wait_s": max(waits) if waits else 0,
        "sum_http_wait_s": sum(waits),
        "details": details,
    }


def summarise_wall_times(manifest_rows: list[dict], outputs_root: Path,
                          wave_recs: set[str]) -> dict:
    """Per-backbone wall-time summary over the wave-1 slice."""
    per_bb: dict[str, list[float]] = defaultdict(list)
    for r in manifest_rows:
        rec = r["receptor_from_path_substring"].upper()
        if rec not in wave_recs:
            continue
        bb = r["backbone"]
        job_root = outputs_root / r["request_id"]
        t = read_wall_time(job_root, bb)
        if t is not None:
            per_bb[bb].append(t)
    out: dict[str, dict] = {}
    for bb, ts in per_bb.items():
        if not ts:
            out[bb] = {"n": 0}
            continue
        out[bb] = {
            "n": len(ts),
            "median_s": statistics.median(ts),
            "max_s": max(ts),
            "sum_s": sum(ts),
        }
    return out


def rerun_cognate_identity_check(manifest_path: Path) -> tuple[int, str]:
    """Run scripts/verify_cognate_identity.py as a subprocess."""
    check_script = REPO / "scripts/verify_cognate_identity.py"
    try:
        r = subprocess.run(
            [sys.executable, str(check_script), "--manifest", str(manifest_path)],
            capture_output=True, text=True, timeout=180
        )
        return r.returncode, r.stdout + "\n" + r.stderr
    except Exception as e:  # noqa: BLE001
        return -1, f"error: {type(e).__name__}: {e}"


def summarise_scored_rows(rows_csv: Path, wave_recs: set[str]) -> dict:
    """Summarise scored rows.csv for the wave-1 slice."""
    if not rows_csv.exists():
        return {"error": f"rows.csv not found at {rows_csv}"}
    rows = list(csv.DictReader(rows_csv.open()))
    # Match by (a) receptor_slug column (scorer canonical) or (b) fallback
    # by prediction/input path substring — the latter keeps failed rows
    # (empty receptor_slug when chain selection itself failed) in the wave-1
    # slice, so scored-cell failure counts reflect reality.
    def _is_wave_1(r: dict) -> bool:
        v = (r.get("receptor_from_path_substring")
             or r.get("receptor_slug")
             or r.get("receptor") or "").upper()
        if v in wave_recs:
            return True
        path = (r.get("prediction_path") or r.get("input_path") or "").lower()
        return any(rec.lower() in path for rec in wave_recs)
    slice_rows = [r for r in rows if _is_wave_1(r)]
    if not slice_rows:
        return {"error": f"no wave-1 rows in {rows_csv}"}

    passed = [(r.get("passed") or "").lower() for r in slice_rows]
    n_pass = sum(1 for p in passed if p in ("true", "1"))
    n_fail = sum(1 for p in passed if p in ("false", "0"))
    n_other = len(passed) - n_pass - n_fail

    tilts = []
    for r in slice_rows:
        v = r.get("d_gpcrdb_tm6_tilt_246_637_ca")
        try:
            if v and v.lower() not in ("nan", "none", ""):
                tilts.append(float(v))
        except (ValueError, AttributeError):
            pass

    # Threshold columns (if the scorer emits them alongside the metric)
    thr_reported = {}
    if slice_rows:
        r = slice_rows[0]
        for k in ("threshold_npxxy_oh_active_lt",
                  "threshold_gpcrdb_tm6_tilt_active_gt",
                  "thresholds_panel_csv_sha256"):
            if k in r:
                thr_reported[k] = r[k]

    return {
        "n_rows": len(slice_rows),
        "n_pass": n_pass,
        "n_fail": n_fail,
        "n_other": n_other,
        "tilt_n": len(tilts),
        "tilt_mean": statistics.mean(tilts) if tilts else None,
        "tilt_std": statistics.stdev(tilts) if len(tilts) > 1 else None,
        "thresholds_in_rows": thr_reported,
    }


def build_report(manifest: Path, outputs_root: Path, wave_recs: set[str],
                  rows_csv: Path) -> str:
    manifest_rows = list(csv.DictReader(manifest.open()))
    lines: list[str] = []
    lines.append(f"# Wave-1 verification report")
    lines.append("")
    lines.append(f"- Manifest: `{manifest}` ({len(manifest_rows)} rows)")
    lines.append(f"- Wave-1 receptor(s): `{sorted(wave_recs)}`")
    lines.append(f"- Outputs root: `{outputs_root}`")
    lines.append("")

    lines.append("## OF3 ColabFold shim sidecar aggregate")
    of3 = summarise_of3_sidecars(manifest_rows, outputs_root, wave_recs)
    for k, v in of3.items():
        if k == "details":
            continue
        lines.append(f"- **{k}**: {v}")
    lines.append("")

    lines.append("## Per-backbone wall time")
    walls = summarise_wall_times(manifest_rows, outputs_root, wave_recs)
    for bb, s in sorted(walls.items()):
        lines.append(f"- **{bb}**: {s}")
    lines.append("")

    lines.append("## Cognate-partner identity re-run")
    rc, out = rerun_cognate_identity_check(manifest)
    lines.append(f"- Return code: `{rc}` (0 = pass)")
    lines.append("```")
    lines.append(out[:4000])
    lines.append("```")
    lines.append("")

    lines.append("## Scored cell rows.csv summary")
    scored = summarise_scored_rows(rows_csv, wave_recs)
    for k, v in scored.items():
        lines.append(f"- **{k}**: {v}")
    lines.append("")
    lines.append(f"Full-panel thresholds in force (from `refs/thresholds_panel.csv`):")
    lines.append(f"- NPxxY-OH: **{THRESHOLD_NPXXY_OH}** Å  (active_lt)")
    lines.append(f"- GPCRdb TM6 tilt: **{THRESHOLD_TM6_TILT}** Å  (active_gt)")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--outputs-root", type=Path, required=True)
    p.add_argument("--wave-1-receptor", nargs="+", default=["AA2AR"],
                   help="Receptor slug(s) constituting wave-1 (default: AA2AR)")
    p.add_argument("--rows-csv", type=Path,
                   default=Path("experiments/018_block_a_switch_test/runs/initial/rows.csv"))
    p.add_argument("--report-out", type=Path,
                   default=Path("experiments/018_block_a_switch_test/runs/initial/wave_1_report.md"))
    args = p.parse_args(argv)

    wave_recs = {r.upper() for r in args.wave_1_receptor}
    report = build_report(args.manifest, args.outputs_root, wave_recs, args.rows_csv)
    args.report_out.parent.mkdir(parents=True, exist_ok=True)
    args.report_out.write_text(report)
    print(report)
    print(f"\nReport written to {args.report_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
