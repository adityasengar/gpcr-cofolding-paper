"""Derive literature-metric reference values on tier-1 crystals.

Parallel to `scripts/derive_npxxy_refs.py`. Computes three new metric
values on every panel receptor × role in `refs/reference_set.csv`:

    d_gpcrdb_tm6_tilt_ref     — 2.46 CA <-> 6.37 CA, Å (GPCRdb cross-class
                                TM6-tilt marker; Class A/B/C).
    a100_index_ref            — Ibrahim/Wifling/Clark 2019 composite.
    a100_component_1_ref … 5  — the five Cα-Cα distances (Å) that feed the
                                composite. Emitted for downstream diagnostics.
    angle_class_b_kink_ref    — Class B TM6 kink angle 6.39-6.50-6.54 (deg).

Every value carries the same "NaN on missing anchor / missing CA" semantics
as the runtime axis functions in `scorer/axes.py` — this script uses those
functions directly so ref and prediction values are byte-comparable.

Usage
-----
    python -m scripts.derive_lit_metric_refs \\
        --reference-set refs/reference_set.csv \\
        --pdb-cache refs/cache/pdb \\
        --gpcrdb-cache refs/cache/gpcrdb \\
        --rcsb-cache refs/cache/rcsb

Only panel receptors (`refs/gpcr_coupling.csv`) are processed by default;
use `--include-non-panel` to cover every row in `reference_set.csv`.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scorer.anchors import resolve_anchors
from scorer.axes import (
    a100_component_1_ca,
    a100_component_2_ca,
    a100_component_3_ca,
    a100_component_4_ca,
    a100_component_5_ca,
    a100_index,
    angle_class_b_tm6_kink_639_650_654_deg,
    d_gpcrdb_tm6_tilt_246_637_ca,
)
from scorer.bw_numbering import Api
from scorer.refs_build import load_pdb_bytes
from scorer.structure import build_uniprot_model
from scorer.verified import verify_reference_pdb


REPO = Path(__file__).resolve().parent.parent
NaN = float("nan")


# ---------------------------------------------------------------------------
# panel membership
# ---------------------------------------------------------------------------


def load_panel_receptors(coupling_csv: Path) -> set[str]:
    with coupling_csv.open() as f:
        return {r["receptor_slug"].strip().upper()
                for r in csv.DictReader(f)
                if r.get("receptor_slug")}


# ---------------------------------------------------------------------------
# per-crystal measurement
# ---------------------------------------------------------------------------


@dataclass
class LitMetricResult:
    d_gpcrdb_tm6_tilt: float
    a100_index: float
    a100_c1: float
    a100_c2: float
    a100_c3: float
    a100_c4: float
    a100_c5: float
    angle_class_b_kink: float
    chain: str | None = None
    identity: float = 0.0
    curation_note: str = ""


def compute_lit_metric_refs(
    pdb_id: str,
    entry_name: str,
    api: Api,
    pdb_cache: Path,
    rcsb_api: Api | None = None,
) -> LitMetricResult:
    """Fetch coords, chain-pick + UniProt-renumber, run the axis functions.

    Anchor resolution goes through `resolve_anchors` — the same call
    the scoring pipeline uses — so the set of resolvable BW positions
    is identical between reference and prediction.
    """
    _rcsb = rcsb_api if rcsb_api is not None else Api(cache_dir=pdb_cache)
    raw, ext = load_pdb_bytes(_rcsb, pdb_id)
    out_pdb = pdb_cache / f"{pdb_id.lower()}.{ext}"
    if not out_pdb.exists():
        out_pdb.write_bytes(raw)

    model = build_uniprot_model(str(out_pdb), entry_name, api)
    aset = resolve_anchors(api, entry_name)

    # verify_reference_pdb is the lenient A1/A2 gate for curated crystals
    # (identity-defining anchors only; per-anchor availability recorded).
    vresult = verify_reference_pdb(model, aset)
    vmodel = vresult.model

    notes: list[str] = []
    for label in ("2.46", "6.37"):
        if label not in aset.anchors:
            notes.append(f"{label} not in GPCRdb for {entry_name}")
    return LitMetricResult(
        d_gpcrdb_tm6_tilt=d_gpcrdb_tm6_tilt_246_637_ca(vmodel),
        a100_index=a100_index(vmodel),
        a100_c1=a100_component_1_ca(vmodel),
        a100_c2=a100_component_2_ca(vmodel),
        a100_c3=a100_component_3_ca(vmodel),
        a100_c4=a100_component_4_ca(vmodel),
        a100_c5=a100_component_5_ca(vmodel),
        angle_class_b_kink=angle_class_b_tm6_kink_639_650_654_deg(vmodel),
        chain=model.chain_name,
        identity=model.identity,
        curation_note="; ".join(notes),
    )


# ---------------------------------------------------------------------------
# CSV augmentation
# ---------------------------------------------------------------------------


def _fmt(x: float, ndigits: int = 6) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.{ndigits}f}"


def _merge_curation(existing: str, addition: str) -> str:
    existing = (existing or "").strip()
    addition = (addition or "").strip()
    if not addition:
        return existing
    if not existing:
        return addition
    if addition in existing:
        return existing
    return f"{existing} | {addition}"


NEW_COLS: tuple[str, ...] = (
    "d_gpcrdb_tm6_tilt_ref",
    "a100_index_ref",
    "a100_component_1_ref",
    "a100_component_2_ref",
    "a100_component_3_ref",
    "a100_component_4_ref",
    "a100_component_5_ref",
    "angle_class_b_kink_ref",
)


def augment_reference_set(
    reference_set: Path,
    coupling_csv: Path,
    pdb_cache: Path,
    gpcrdb_cache: Path,
    rcsb_cache: Path,
    output: Path | None = None,
    only_panel: bool = True,
) -> dict[str, Any]:
    output = output or reference_set
    panel = load_panel_receptors(coupling_csv)
    gpcrdb_api = Api(cache_dir=gpcrdb_cache)
    rcsb_api = Api(cache_dir=rcsb_cache)
    pdb_cache.mkdir(parents=True, exist_ok=True)

    with reference_set.open() as f:
        reader = csv.DictReader(f)
        rows = [dict(r) for r in reader]
        base_cols = list(reader.fieldnames or [])

    for col in NEW_COLS:
        if col not in base_cols:
            base_cols.append(col)

    summary: dict[str, Any] = {
        "rows_total": len(rows),
        "rows_panel": 0,
        "rows_processed": 0,
        "rows_failed": [],
        "measurements": [],
    }

    for row in rows:
        for col in NEW_COLS:
            row.setdefault(col, "")
        receptor = (row.get("receptor_slug") or "").strip().upper()
        if only_panel and receptor not in panel:
            continue
        summary["rows_panel"] += 1

        pdb_id = (row.get("pdb_id") or "").strip()
        entry_name = (row.get("uniprot_slug") or "").strip()
        if not pdb_id or not entry_name:
            continue

        try:
            r = compute_lit_metric_refs(
                pdb_id, entry_name,
                api=gpcrdb_api, pdb_cache=pdb_cache,
                rcsb_api=rcsb_api,
            )
        except Exception as e:  # lint-allow: capture-and-record — surface
            summary["rows_failed"].append({
                "receptor": receptor, "role": row.get("role"),
                "pdb_id": pdb_id,
                "error": f"{type(e).__name__}: {e}",
            })
            print(f"FAIL  {receptor:<8s} {row.get('role','?'):<10s} {pdb_id}  "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
            continue

        row["d_gpcrdb_tm6_tilt_ref"] = _fmt(r.d_gpcrdb_tm6_tilt)
        row["a100_index_ref"] = _fmt(r.a100_index, ndigits=3)
        row["a100_component_1_ref"] = _fmt(r.a100_c1)
        row["a100_component_2_ref"] = _fmt(r.a100_c2)
        row["a100_component_3_ref"] = _fmt(r.a100_c3)
        row["a100_component_4_ref"] = _fmt(r.a100_c4)
        row["a100_component_5_ref"] = _fmt(r.a100_c5)
        row["angle_class_b_kink_ref"] = _fmt(r.angle_class_b_kink, ndigits=3)
        if r.curation_note:
            row["curation_note"] = _merge_curation(row.get("curation_note", ""),
                                                    r.curation_note)

        summary["rows_processed"] += 1
        summary["measurements"].append({
            "receptor": receptor, "role": row.get("role"), "pdb_id": pdb_id,
            "chain": r.chain, "identity": r.identity,
            "d_gpcrdb_tm6_tilt": r.d_gpcrdb_tm6_tilt,
            "a100_index": r.a100_index,
            "angle_class_b_kink": r.angle_class_b_kink,
            "notes": r.curation_note,
        })
        print(f"OK    {receptor:<8s} {row.get('role','?'):<10s} {pdb_id}  "
              f"chain={r.chain} id={r.identity:.2%}  "
              f"tm6tilt={_fmt(r.d_gpcrdb_tm6_tilt) or 'nan':>10s}  "
              f"A100={_fmt(r.a100_index, 3) or 'nan':>8s}  "
              f"Bkink={_fmt(r.angle_class_b_kink, 2) or 'nan':>8s}")

    with output.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=base_cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in base_cols})

    return summary


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-set", default=str(REPO / "refs" / "reference_set.csv"))
    ap.add_argument("--coupling-csv", default=str(REPO / "refs" / "gpcr_coupling.csv"))
    ap.add_argument("--pdb-cache", default=str(REPO / "refs" / "cache" / "pdb"))
    ap.add_argument("--gpcrdb-cache", default=str(REPO / "refs" / "cache" / "gpcrdb"))
    ap.add_argument("--rcsb-cache", default=str(REPO / "refs" / "cache" / "rcsb"))
    ap.add_argument("--output", default=None)
    ap.add_argument("--include-non-panel", action="store_true")
    ap.add_argument("--summary-json", default=None)
    args = ap.parse_args(argv)

    summary = augment_reference_set(
        reference_set=Path(args.reference_set),
        coupling_csv=Path(args.coupling_csv),
        pdb_cache=Path(args.pdb_cache),
        gpcrdb_cache=Path(args.gpcrdb_cache),
        rcsb_cache=Path(args.rcsb_cache),
        output=Path(args.output) if args.output else None,
        only_panel=not args.include_non_panel,
    )
    print(
        f"\n{summary['rows_processed']} rows measured "
        f"(of {summary['rows_panel']} panel rows / {summary['rows_total']} total). "
        f"{len(summary['rows_failed'])} row(s) failed.",
        file=sys.stderr,
    )
    for fail in summary["rows_failed"]:
        print(f"  FAIL {fail['receptor']:<8s} {fail['role']:<10s} "
              f"{fail['pdb_id']}  {fail['error']}", file=sys.stderr)
    if args.summary_json:
        Path(args.summary_json).write_text(json.dumps(summary, indent=2, default=str))
    return 0 if not summary["rows_failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
