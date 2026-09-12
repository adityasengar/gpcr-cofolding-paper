#!/usr/bin/env python3
"""Parallel rescore driver — process-pool over `scorer.score_and_capture`.

Prototype (2026-09-02) that mirrors the manifest-mode of
`scripts/rescore_experiment.py` but shards the per-prediction scoring
loop across N worker processes. The scorer itself is unchanged; the
only new machinery is (a) a `multiprocessing.Pool` with
`imap_unordered`, (b) a single-writer aggregation phase, and (c) a
provenance JSON recording n_workers / wall-time / per-worker task
counts.

Non-goals:

* Not a replacement for `rescore_experiment.py` — that driver does
  scratch discovery + Exp-Layer 2 enrichment + rows.provenance.json +
  ligand-fasta regen. This driver only handles the score-and-write step
  in the middle. Feed it a pre-exploded rescore manifest (one row per
  prediction file, columns:
  ``prediction_path, receptor_slug, state_claim, input_species``).

* No incremental resume. If a shard fails mid-run the whole rescore is
  re-run — the same shape as the sequential driver.

Parallelisation hazards (documented in the benchmark report):

* GPCRdb file-cache under ``<cache-dir>/gpcrdb/`` is filename-keyed
  (`residues_ext_<entry>.json`). Writes are NOT atomic. Pre-warm the
  cache before dispatching workers so no worker takes the fetch/write
  branch — all workers become pure readers.

* All other module-level caches (`scorer.structure._ONE`, thresholds
  panel SHA, etc.) are populated lazily per-process and are idempotent
  under the fork model.

* The scorer emits per-row JSON sidecars in `_write_row`. This driver
  does NOT call `_write_row` — it aggregates ScorerRow objects in the
  parent and writes rows.csv + failure_census.json once at the end. If
  you need per-row JSON sidecars, fall back to the sequential driver.

Usage:

    scripts/rescore_parallel.py \
        --manifest /path/to/rescore_manifest.csv \
        --out /path/to/out_dir \
        --n-workers 32 \
        --ref-set refs/reference_set.csv \
        --cache-dir refs/cache
"""
from __future__ import annotations

import argparse
import csv
import datetime as _dt
import json
import multiprocessing as mp
import os
import sys
import time
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------
#
# Each worker imports the scorer lazily (on first task) so pool startup is
# cheap. `initializer` records the worker pid + start time so the parent
# can attribute per-worker counts.


_WORKER_STATE: dict[str, Any] = {}


def _worker_init(ref_set_csv_path: str | None, cache_dir: str, out_dir: str) -> None:
    """Called once per worker process at pool start. Pre-imports the scorer
    modules (so first-task latency is amortised) and stashes the shared
    scorer args on module state for the task function to pick up.

    Pre-loads the ``ReferenceSet`` here so every ``run_scorer`` call in
    this worker skips the ``from_csv`` re-parse. The sequential driver
    ALSO re-parses per row (via ``score_and_capture`` -> ``run_scorer``);
    caching it here is a fair single-parse-per-process optimisation the
    parallel driver can offer for free.
    """
    _WORKER_STATE["ref_set_csv_path"] = ref_set_csv_path
    _WORKER_STATE["cache_dir"] = cache_dir
    _WORKER_STATE["out_dir"] = out_dir
    _WORKER_STATE["pid"] = os.getpid()
    _WORKER_STATE["started_at"] = time.time()
    _WORKER_STATE["n_tasks"] = 0
    # Pre-import (fork model would inherit the imports already; explicit
    # import here also protects the spawn model on macOS if we ever run
    # the driver locally).
    from scorer import orchestrator  # noqa: F401
    from scorer.references import ReferenceSet
    if ref_set_csv_path and Path(ref_set_csv_path).exists():
        _WORKER_STATE["ref_set"] = ReferenceSet.from_csv(ref_set_csv_path)
    else:
        _WORKER_STATE["ref_set"] = ReferenceSet.empty()


def _score_one(row: dict[str, str]) -> dict[str, Any]:
    """Task fn: score a single manifest row. Never raises — the scorer's
    `score_and_capture` catches at the one sanctioned site and returns
    (row, err). We serialise the resulting ScorerRow to its CSV-row dict
    and return that plus the failing assertion id (or empty string).

    Also returns a per-task diagnostic block (pid + elapsed_ms) that the
    parent aggregates into the provenance JSON.
    """
    t0 = time.time()
    from scorer.orchestrator import score_and_capture

    prediction_path = row["prediction_path"]
    receptor = row.get("receptor_slug") or None
    state = row.get("state_claim") or "Ga-coupled-active"
    species = row.get("input_species") or "human"

    ref_set_csv_path = _WORKER_STATE["ref_set_csv_path"]
    cache_dir = _WORKER_STATE["cache_dir"]
    out_dir = _WORKER_STATE["out_dir"]
    ref_set = _WORKER_STATE["ref_set"]

    # Post-Audit Stage 1 (2026-09-05): the rescore manifest MAY carry
    # ligand-annotation columns from the campaign manifest. Feed them
    # into ``score_and_capture`` as manifest-fallback kwargs so the
    # orchestrator's ligand fields end up populated even when the
    # dispatched output tree has no ``_rerun_plan.json`` sidecars
    # (Block C Tier 3 dispatch via ``block_b_worker.sh``). Empty
    # strings are passed as-is; the orchestrator only substitutes when
    # the sidecar-lifted value is missing.
    m_lig_type = row.get("ligand_type") or None
    m_lig_smiles = row.get("ligand_smiles") or None
    m_lig_sequence = row.get("ligand_sequence") or None
    m_lig_role = row.get("ligand_role") or None

    # ref_set_csv_path is still passed so the scorer stamps
    # ref_set_csv_sha256 on the row (a cheap sha256 read). The parsed
    # ReferenceSet handed in via `ref_set=` short-circuits the CSV
    # parse in run_scorer — one parse per worker process instead of
    # one per row.
    scorer_row, err = score_and_capture(
        input_path=prediction_path,
        receptor_hint=receptor,
        input_state_claim=state,
        output_dir=out_dir,
        ref_set=ref_set,
        ref_set_csv_path=ref_set_csv_path if ref_set_csv_path else None,
        cache_dir=cache_dir,
        input_species=species,
        manifest_ligand_type=m_lig_type,
        manifest_ligand_smiles=m_lig_smiles,
        manifest_ligand_sequence=m_lig_sequence,
        manifest_ligand_role=m_lig_role,
    )

    _WORKER_STATE["n_tasks"] += 1

    return {
        "csv_row": scorer_row.to_csv_row(),
        "assertion_id": err.assertion_id if err is not None else "",
        "pid": _WORKER_STATE["pid"],
        "elapsed_ms": (time.time() - t0) * 1000.0,
    }


# ---------------------------------------------------------------------------
# Parent-side driver
# ---------------------------------------------------------------------------


def _load_manifest(manifest_path: Path) -> list[dict[str, str]]:
    with manifest_path.open() as f:
        return [
            row for row in csv.DictReader(f)
            if row and (row.get("prediction_path") or "").strip()
            and not (row.get("prediction_path") or "").startswith("#")
        ]


class JoinAssertionError(RuntimeError):
    """Raised by ``_assert_join_integrity`` when a write-time
    manifest-join invariant fails on the aggregated rescore output.

    Distinct from ``ScorerAssertionError`` — those A1..A6 failures live
    on a single row, whereas a join-assertion failure is a
    corpus-shape invariant. The batch driver halts before writing
    rows.csv when this fires and dumps the offending rows to
    ``verification/join_assertions_failed.jsonl`` for forensics.
    """


def _assert_join_integrity(
    rows: list[dict[str, Any]],
    manifest_rows: list[dict[str, str]],
    out_dir: Path,
) -> dict[str, Any]:
    """Post-Audit Stage 1 write-time assertions (2026-09-05).

    Runs BEFORE ``rows.csv`` is emitted. Halts on any failure and
    dumps the offending rows to
    ``<out_dir>/verification/join_assertions_failed.jsonl`` for
    forensics.

    Assertions:
      1. ``ligand_smiles`` varies across ``ligand_role`` within EVERY
         receptor — i.e., for each receptor, at least 2 distinct
         non-empty SMILES values across the 3 ligand_role states
         (agonist / antag / decoy). A receptor whose SMILES is
         constant means the join swapped rows OR the manifest was
         mono-ligand for that receptor. Passing rows only.
      2. Every scored row's ``ligand_role`` matches the manifest's
         ``ligand_role`` for the same ``prediction_path``.
      3. ``decoy_lig`` rows never carry a ``ligand_ccd`` — decoys are
         PubChem-sourced small molecules with no CCD code by design.
         An assigned CCD means the join wired the wrong sidecar.
      4. ``ligand_type`` is non-empty on 100 % of PASSING rows.

    Returns a dict with per-assertion counts + failure summary; caller
    is expected to log it. Raises ``JoinAssertionError`` on any
    failure with a message pointing at the JSONL dump.
    """
    verification_dir = out_dir / "verification"
    verification_dir.mkdir(parents=True, exist_ok=True)
    failed_rows: list[dict[str, Any]] = []
    summary: dict[str, Any] = {
        "n_rows_total": len(rows),
        "n_rows_passed": sum(
            1 for r in rows if str(r.get("passed", "")).lower() == "true"
        ),
        "assertion_1_ligand_smiles_varies": {
            "status": "ok",
            "n_receptors_checked": 0,
            "n_receptors_constant_smiles": 0,
            "failing_receptors": [],
        },
        "assertion_2_ligand_role_matches_manifest": {
            "status": "ok",
            "n_rows_checked": 0,
            "n_mismatches": 0,
        },
        "assertion_3_decoy_no_ccd": {
            "status": "ok",
            "n_decoy_rows": 0,
            "n_decoy_with_ccd": 0,
        },
        "assertion_4_ligand_type_populated": {
            "status": "ok",
            "n_passing_rows": 0,
            "n_empty_ligand_type": 0,
        },
    }

    # Build path → manifest-row index for assertion 2. The rescore
    # manifest's `prediction_path` is the ground-truth key.
    m_by_path: dict[str, dict[str, str]] = {
        r["prediction_path"]: r for r in manifest_rows
    }

    # Assertion 1 — the ligand identity varies across ligand_role per
    # receptor. Peptide-ligand receptors carry the identity in
    # ligand_sequence, small-molecule receptors in ligand_smiles; the
    # check uses whichever is populated so peptide receptors (APJ,
    # GHSR, GLP1R) don't mis-fire when SMILES is empty by design.
    # Passing rows only; NaN-passed rows shouldn't drive a false
    # positive.
    per_receptor: dict[str, set[str]] = {}
    per_receptor_roles: dict[str, set[str]] = {}
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        recep = str(r.get("receptor_slug", "")).strip().upper()
        smi = str(r.get("ligand_smiles", "")).strip()
        seq = str(r.get("ligand_sequence", "")).strip()
        role = str(r.get("ligand_role", "")).strip()
        if not recep:
            continue
        # Identity key = SMILES-or-sequence; empty when neither is
        # populated (apo / decoy-with-no-annotation).
        identity = smi or seq
        per_receptor.setdefault(recep, set()).add(identity)
        per_receptor_roles.setdefault(recep, set()).add(role)

    a1 = summary["assertion_1_ligand_smiles_varies"]
    for recep, idset in per_receptor.items():
        a1["n_receptors_checked"] += 1
        # Only "constant" is failure when the receptor's dispatch had
        # ≥ 2 ligand_roles (which is the Block C Tier 3 shape). A
        # receptor with a single role in the corpus is not a join
        # failure and gets a pass.
        nonempty = {s for s in idset if s}
        n_roles = len(per_receptor_roles.get(recep, set()) - {""})
        if len(nonempty) < 2 and n_roles >= 2:
            a1["n_receptors_constant_smiles"] += 1
            a1["failing_receptors"].append(recep)
            for r in rows:
                if str(r.get("receptor_slug", "")).strip().upper() == recep:
                    failed_rows.append({
                        "assertion": "1_ligand_smiles_varies",
                        "receptor": recep,
                        "prediction_path": r.get("prediction_path"),
                        "ligand_smiles": r.get("ligand_smiles"),
                        "ligand_sequence": r.get("ligand_sequence"),
                        "ligand_role": r.get("ligand_role"),
                    })
    if a1["n_receptors_constant_smiles"] > 0:
        a1["status"] = "FAIL"

    # Assertion 2 — ligand_role matches manifest.
    a2 = summary["assertion_2_ligand_role_matches_manifest"]
    for r in rows:
        a2["n_rows_checked"] += 1
        path = r.get("input_path") or r.get("prediction_path")
        m = m_by_path.get(str(path))
        if m is None:
            continue  # Manifest gap already surfaces via assertion 4.
        expected = (m.get("ligand_role") or "").strip()
        observed = str(r.get("ligand_role", "")).strip()
        if expected != observed:
            a2["n_mismatches"] += 1
            failed_rows.append({
                "assertion": "2_ligand_role_matches_manifest",
                "prediction_path": path,
                "expected_ligand_role": expected,
                "observed_ligand_role": observed,
            })
    if a2["n_mismatches"] > 0:
        a2["status"] = "FAIL"

    # Assertion 3 — decoy_lig rows never carry a ligand_ccd.
    a3 = summary["assertion_3_decoy_no_ccd"]
    for r in rows:
        if str(r.get("ligand_role", "")).strip() != "decoy_lig":
            continue
        a3["n_decoy_rows"] += 1
        # ligand_ccd lives in the manifest only (not a scorer output
        # column), so read it via the manifest index. If any decoy
        # manifest row carries a CCD, the pipeline swapped roles.
        path = r.get("input_path") or r.get("prediction_path")
        m = m_by_path.get(str(path))
        if m is None:
            continue
        ccd = (m.get("ligand_ccd") or "").strip()
        if ccd:
            a3["n_decoy_with_ccd"] += 1
            failed_rows.append({
                "assertion": "3_decoy_no_ccd",
                "prediction_path": path,
                "ligand_ccd_from_manifest": ccd,
            })
    if a3["n_decoy_with_ccd"] > 0:
        a3["status"] = "FAIL"

    # Assertion 4 — ligand_type populated on 100 % of passing rows.
    a4 = summary["assertion_4_ligand_type_populated"]
    for r in rows:
        if str(r.get("passed", "")).lower() != "true":
            continue
        a4["n_passing_rows"] += 1
        if not str(r.get("ligand_type", "")).strip():
            a4["n_empty_ligand_type"] += 1
            failed_rows.append({
                "assertion": "4_ligand_type_populated",
                "prediction_path": r.get("input_path") or r.get(
                    "prediction_path"
                ),
                "receptor": r.get("receptor_slug"),
            })
    if a4["n_empty_ligand_type"] > 0:
        a4["status"] = "FAIL"

    # Dump failed rows and raise if anything failed.
    any_fail = any(
        summary[k]["status"] == "FAIL"
        for k in (
            "assertion_1_ligand_smiles_varies",
            "assertion_2_ligand_role_matches_manifest",
            "assertion_3_decoy_no_ccd",
            "assertion_4_ligand_type_populated",
        )
    )
    if failed_rows or any_fail:
        dump_path = verification_dir / "join_assertions_failed.jsonl"
        with dump_path.open("w") as f:
            for entry in failed_rows:
                f.write(json.dumps(entry) + "\n")
    if any_fail:
        raise JoinAssertionError(
            "rescore write-time join assertions failed — see "
            f"{verification_dir}/join_assertions_failed.jsonl; "
            f"summary: {json.dumps(summary, indent=2)}"
        )
    return summary


def _write_rows_csv(rows: list[dict[str, Any]], out_dir: Path) -> Path:
    """Emit rows.csv in the same shape as scorer.cli._write_row.

    Uses the scorer's canonical CSV_COLUMNS so downstream tooling
    (enricher, MASTER builder) sees an identical layout to the
    sequential driver's output.
    """
    from scorer.schema import CSV_COLUMNS

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "rows.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(CSV_COLUMNS))
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return csv_path


def _write_failure_census(census: dict[str, int], total: int, out_dir: Path) -> Path:
    p = out_dir / "failure_census.json"
    p.write_text(json.dumps({
        "total": total,
        "passed": total - sum(census.values()),
        "by_assertion": census,
    }, indent=2))
    return p


def _write_provenance(
    out_dir: Path,
    manifest_path: Path,
    n_workers: int,
    wall_time_s: float,
    per_worker_counts: dict[int, int],
    per_worker_elapsed_ms: dict[int, float],
    total_task_elapsed_ms: float,
    n_total: int,
    n_failed: int,
) -> Path:
    """Emit rescore_parallel.provenance.json with the numbers the report
    consumes. Kept separate from any rows.provenance.json the outer
    rescore driver may write later."""
    p = out_dir / "rescore_parallel.provenance.json"
    speedup_vs_serial = (
        total_task_elapsed_ms / (wall_time_s * 1000.0) if wall_time_s > 0 else 0.0
    )
    p.write_text(json.dumps({
        "manifest_path": str(manifest_path.resolve()),
        "n_workers": n_workers,
        "n_total": n_total,
        "n_failed": n_failed,
        "wall_time_s": wall_time_s,
        "sum_task_elapsed_ms": total_task_elapsed_ms,
        "mean_task_elapsed_ms": total_task_elapsed_ms / n_total if n_total else 0.0,
        "throughput_rows_per_s": n_total / wall_time_s if wall_time_s > 0 else 0.0,
        "effective_parallel_efficiency": speedup_vs_serial / n_workers if n_workers else 0.0,
        "per_worker_task_counts": {str(k): v for k, v in per_worker_counts.items()},
        "per_worker_sum_elapsed_ms": {str(k): v for k, v in per_worker_elapsed_ms.items()},
        "finished_at_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(
            timespec="seconds"
        ),
    }, indent=2) + "\n")
    return p


def rescore_parallel(
    manifest_path: Path,
    out_dir: Path,
    n_workers: int,
    ref_set: Path,
    cache_dir: Path,
    chunksize: int = 4,
    join_assertions: bool = True,
    dry_run_head: int = 0,
) -> dict[str, Any]:
    """Run the scorer across `n_workers` processes over the manifest rows.

    Returns a summary dict; the caller (main) prints it as JSON.
    """
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    rows_in = _load_manifest(manifest_path)
    n_total = len(rows_in)
    if n_total == 0:
        raise RuntimeError(f"manifest {manifest_path} is empty")
    # Dry-run mode (Post-Audit Stage 1, 2026-09-05): truncate to the
    # first `dry_run_head` rows so the join assertions can be exercised
    # end-to-end on a small subset before dispatching the full 40,800.
    if dry_run_head > 0:
        rows_in = rows_in[:dry_run_head]
        n_total = len(rows_in)
        print(
            f"[rescore-parallel] DRY-RUN mode: truncated manifest to first "
            f"{n_total} rows for assertion check",
            file=sys.stderr,
        )

    print(
        f"[rescore-parallel] manifest={manifest_path} n_rows={n_total} "
        f"n_workers={n_workers} out={out_dir}",
        file=sys.stderr,
    )

    # ----- pool setup ---------------------------------------------------
    ref_set_str = str(ref_set) if ref_set.exists() else None
    ctx = mp.get_context("fork")  # Linux HPC: cheap, inherits open handles

    t_wall_0 = time.time()
    scored: list[dict[str, Any]] = []
    census: dict[str, int] = {}
    per_worker_counts: dict[int, int] = {}
    per_worker_elapsed_ms: dict[int, float] = {}
    total_task_elapsed_ms = 0.0

    with ctx.Pool(
        processes=n_workers,
        initializer=_worker_init,
        initargs=(ref_set_str, str(cache_dir.resolve()), str(out_dir)),
    ) as pool:
        for i, result in enumerate(
            pool.imap_unordered(_score_one, rows_in, chunksize=chunksize)
        ):
            csv_row = result["csv_row"]
            aid = result["assertion_id"]
            pid = result["pid"]
            elapsed = result["elapsed_ms"]

            scored.append(csv_row)
            if aid:
                census[aid] = census.get(aid, 0) + 1
            per_worker_counts[pid] = per_worker_counts.get(pid, 0) + 1
            per_worker_elapsed_ms[pid] = per_worker_elapsed_ms.get(pid, 0.0) + elapsed
            total_task_elapsed_ms += elapsed

            if (i + 1) % 100 == 0 or (i + 1) == n_total:
                elapsed_wall = time.time() - t_wall_0
                rate = (i + 1) / elapsed_wall if elapsed_wall > 0 else 0.0
                print(
                    f"[rescore-parallel] {i+1}/{n_total}  "
                    f"wall={elapsed_wall:6.1f}s  rate={rate:6.1f} row/s",
                    file=sys.stderr,
                )
    wall_time_s = time.time() - t_wall_0

    # ----- write-time join assertions (Post-Audit Stage 1, 2026-09-05) --
    # Runs BEFORE rows.csv is emitted. Fail-loud on any assertion
    # miss — halt the write, dump failed rows to
    # <out_dir>/verification/join_assertions_failed.jsonl, ntfy.
    join_summary: dict[str, Any] = {"status": "skipped"}
    if join_assertions:
        try:
            join_summary = _assert_join_integrity(scored, rows_in, out_dir)
            print(
                f"[rescore-parallel] join assertions PASSED  "
                f"(receptors={join_summary['assertion_1_ligand_smiles_varies']['n_receptors_checked']}, "
                f"rows_role_checked={join_summary['assertion_2_ligand_role_matches_manifest']['n_rows_checked']}, "
                f"decoy_rows={join_summary['assertion_3_decoy_no_ccd']['n_decoy_rows']}, "
                f"passing_rows={join_summary['assertion_4_ligand_type_populated']['n_passing_rows']})",
                file=sys.stderr,
            )
        except JoinAssertionError as e:
            print(
                f"[rescore-parallel] JOIN ASSERTION FAILURE — HALTING WRITE\n{e}",
                file=sys.stderr,
            )
            # Still emit failure_census + provenance so operators can
            # inspect what went wrong; skip rows.csv on purpose.
            fc_path = _write_failure_census(census, n_total, out_dir)
            prov_path = _write_provenance(
                out_dir=out_dir,
                manifest_path=manifest_path,
                n_workers=n_workers,
                wall_time_s=wall_time_s,
                per_worker_counts=per_worker_counts,
                per_worker_elapsed_ms=per_worker_elapsed_ms,
                total_task_elapsed_ms=total_task_elapsed_ms,
                n_total=n_total,
                n_failed=sum(census.values()),
            )
            # Write partial join_summary for post-mortem.
            (out_dir / "verification" / "join_assertions_summary.json").write_text(
                json.dumps(e.args[0] if e.args else "unknown", indent=2)
            )
            raise

    # ----- aggregate ----------------------------------------------------
    rows_csv = _write_rows_csv(scored, out_dir)
    fc_path = _write_failure_census(census, n_total, out_dir)
    prov_path = _write_provenance(
        out_dir=out_dir,
        manifest_path=manifest_path,
        n_workers=n_workers,
        wall_time_s=wall_time_s,
        per_worker_counts=per_worker_counts,
        per_worker_elapsed_ms=per_worker_elapsed_ms,
        total_task_elapsed_ms=total_task_elapsed_ms,
        n_total=n_total,
        n_failed=sum(census.values()),
    )

    # Write the join assertions summary alongside rows.csv on success.
    if join_assertions:
        summary_path = out_dir / "verification" / "join_assertions_summary.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(join_summary, indent=2))

    print(
        f"[rescore-parallel] done  wall={wall_time_s:.1f}s  "
        f"rows={rows_csv}  census={census}",
        file=sys.stderr,
    )

    return {
        "n_total": n_total,
        "n_failed": sum(census.values()),
        "wall_time_s": wall_time_s,
        "n_workers": n_workers,
        "rows_csv": str(rows_csv),
        "failure_census_json": str(fc_path),
        "provenance_json": str(prov_path),
        "census": census,
        "join_assertions": join_summary,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rescore_parallel",
        description="Parallel rescore driver (multiprocessing pool over score_and_capture).",
    )
    p.add_argument("--manifest", type=Path, required=True,
                   help="pre-exploded rescore manifest CSV — one row per "
                        "prediction file, columns: prediction_path, "
                        "receptor_slug, state_claim, input_species")
    p.add_argument("--out", type=Path, required=True,
                   help="output directory (rows.csv + failure_census.json "
                        "+ rescore_parallel.provenance.json land here)")
    p.add_argument("--n-workers", type=int, default=32,
                   help="worker process count (default: 32)")
    p.add_argument("--ref-set", type=Path,
                   default=REPO / "refs" / "reference_set.csv")
    p.add_argument("--cache-dir", type=Path,
                   default=REPO / "refs" / "cache")
    p.add_argument("--chunksize", type=int, default=4,
                   help="imap_unordered chunk size (default: 4)")
    p.add_argument("--no-join-assertions", action="store_true",
                   help="Disable Post-Audit Stage 1 write-time join "
                        "assertions (default: on). Only use for a "
                        "legacy rescore that predates the assertions.")
    p.add_argument("--dry-run-head", type=int, default=0,
                   help="Score only the first N manifest rows so the "
                        "join assertions can be exercised on a small "
                        "subset before the full dispatch (default 0 "
                        "= run everything).")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if not args.manifest.exists():
        print(f"manifest not found: {args.manifest}", file=sys.stderr)
        return 2
    summary = rescore_parallel(
        manifest_path=args.manifest,
        out_dir=args.out,
        n_workers=args.n_workers,
        ref_set=args.ref_set,
        cache_dir=args.cache_dir,
        chunksize=args.chunksize,
        join_assertions=(not args.no_join_assertions),
        dry_run_head=args.dry_run_head,
    )
    print(json.dumps(summary, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
