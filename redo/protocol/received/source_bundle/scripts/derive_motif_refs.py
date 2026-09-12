"""Derive the four remaining motif-metric reference distances for panel receptors.

Companion to ``scripts/derive_npxxy_refs.py``. PREREG §2b lists six motif
metrics; the NPxxY OH-OH and NPxxY CA-CA references have already been
populated in ``refs/reference_set.csv`` by the earlier NPxxY-derivation
agent. This script fills in the remaining four references from the same
tier-1 crystals:

    d_y558_pack_ref     -- min heavy-atom distance from Y5.58 OH to nearest
                           atom within ±3 residues of the 3.50 or 6.30
                           anchors (excluding Y5.58 itself).
    d_dry_ref           -- R3.50 CZ to 6.30 side-chain carboxyl O (OE1/OE2
                           for E, OD1/OD2 for D). NaN when 6.30 is not E/D.
    d_tm5_out_ref       -- R3.50 CA to R5.58 CA (proxy for TM5 outward).
    icl2_helical_ref    -- helicity fraction over the 14-residue window
                           C-terminal to 3.50, counting (i, i+4) CA-CA in
                           the 3.8..6.4 Å α-helix envelope.

The scorer implementations in ``scorer/axes.py`` are called directly
(``d_y558_pack_min_heavy``, ``d_dry_sidechain_r350cz_e630oe1``,
``d_tm5_outward_r350_r558_ca``, ``icl2_helical_frac``) so reference values
and prediction-time values are computed by exactly the same code path.

Usage
-----
    python -m scripts.derive_motif_refs \
        --reference-set refs/reference_set.csv \
        --pdb-cache refs/cache/pdb \
        --gpcrdb-cache refs/cache/gpcrdb

Only the 40 in-panel receptors (``refs/gpcr_coupling.csv``) are processed
by default; non-panel rows keep empty values. The four columns are
appended at the end of the CSV — existing columns are never overwritten.
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
    d_dry_sidechain_r350cz_e630oe1,
    d_tm5_outward_r350_r558_ca,
    d_y558_pack_min_heavy,
    icl2_helical_frac,
)
from scorer.bw_numbering import Api
from scorer.refs_build import load_pdb_bytes
from scorer.structure import build_uniprot_model, one_letter
from scorer.verified import verify_reference_pdb

REPO = Path(__file__).resolve().parent.parent
NaN = float("nan")

NEW_COLS = ("d_y558_pack_ref", "d_dry_ref", "d_tm5_out_ref", "icl2_helical_ref")


# ---------------------------------------------------------------------------
# panel membership
# ---------------------------------------------------------------------------


def load_panel_receptors(coupling_csv: Path) -> set[str]:
    """Return the set of receptor_slug values in refs/gpcr_coupling.csv."""
    with coupling_csv.open() as f:
        return {r["receptor_slug"].strip().upper()
                for r in csv.DictReader(f)
                if r.get("receptor_slug")}


# ---------------------------------------------------------------------------
# Motif-metric derivation
# ---------------------------------------------------------------------------


@dataclass
class MotifResult:
    """Motif-metric measurements for one (receptor, role, PDB) triple."""
    d_y558_pack: float
    d_dry: float
    d_tm5_out: float
    icl2_helical: float
    curation_note: str = ""
    obs_350: str | None = None
    obs_558: str | None = None
    obs_630: str | None = None
    chain: str | None = None
    identity: float = 0.0


def compute_motif_refs(
    pdb_id: str,
    entry_name: str,
    anchor_positions: dict[str, int],
    api: Api,
    pdb_cache: Path,
    rcsb_api: Api | None = None,
) -> MotifResult:
    """Compute the four motif reference metrics for one curated crystal.

    Mirrors ``derive_npxxy_refs.compute_npxxy_refs``: load the PDB, chain-
    pick + UniProt-renumber, build a ``VerifiedModel`` via the lenient
    reference-verify path, then invoke the scorer's own axis functions.
    """
    pos_350 = anchor_positions.get("3.50")
    pos_558 = anchor_positions.get("5.58")
    pos_630 = anchor_positions.get("6.30")
    # 7.53 unused for these four axes.

    _rcsb = rcsb_api if rcsb_api is not None else Api(cache_dir=pdb_cache)
    raw, ext = load_pdb_bytes(_rcsb, pdb_id)
    out_pdb = pdb_cache / f"{pdb_id.lower()}.{ext}"
    if not out_pdb.exists():
        out_pdb.write_bytes(raw)

    model = build_uniprot_model(str(out_pdb), entry_name, api)
    anchor_set = resolve_anchors(api, entry_name)
    vresult = verify_reference_pdb(model, anchor_set)
    vmodel = vresult.model

    notes: list[str] = []

    # Residue identities at the anchors this bundle of metrics depends on
    def _obs(pos: int | None) -> str | None:
        if pos is None:
            return None
        r = vmodel.residues.get(pos)
        return one_letter(r.name) if r is not None else None

    obs_350 = _obs(pos_350)
    obs_558 = _obs(pos_558)
    obs_630 = _obs(pos_630)

    if obs_350 is None:
        notes.append(f"3.50 residue not resolved in {pdb_id}")
    elif obs_350 != "R":
        notes.append(
            f"3.50 is not Arg in this receptor (observed {obs_350}); "
            "DRY / TM5 / Y5.58-pack references are still emitted geometrically."
        )
    if obs_558 is None:
        notes.append(f"5.58 residue not resolved in {pdb_id}")
    elif obs_558 != "Y":
        notes.append(
            f"5.58 is not Tyr in this receptor (observed {obs_558}); "
            "Y5.58-pack reference not meaningful."
        )
    if obs_630 is None:
        notes.append(f"6.30 residue not resolved in {pdb_id}")
    elif obs_630 == "D":
        # OE1 preferred but Asp lacks OE1; scorer falls back to OD1/OD2.
        notes.append(
            f"6.30 is Asp (not Glu) in this receptor; DRY reference uses "
            "OD1 fallback in place of OE1."
        )
    elif obs_630 != "E":
        notes.append(
            f"6.30 is neither Glu nor Asp (observed {obs_630}); "
            "DRY ionic-lock reference will be NaN."
        )

    # Direct invocations of the scorer's axis functions.
    d_y558_pack = d_y558_pack_min_heavy(vmodel)
    d_dry = d_dry_sidechain_r350cz_e630oe1(vmodel)
    d_tm5_out = d_tm5_outward_r350_r558_ca(vmodel)
    icl2_hel = icl2_helical_frac(vmodel)

    if math.isnan(d_y558_pack) and obs_558 == "Y":
        notes.append(
            f"Y5.58-pack NaN despite Y at 5.58 in {pdb_id} "
            "(side-chain OH truncated or no TM3/6 neighbours resolved)."
        )
    if math.isnan(d_dry) and obs_630 in ("E", "D"):
        notes.append(
            f"DRY NaN despite E/D at 6.30 in {pdb_id} "
            "(R3.50 CZ or side-chain carboxyl truncated)."
        )
    if math.isnan(d_tm5_out):
        notes.append(f"TM5-out NaN in {pdb_id} (3.50 or 5.58 CA unresolved).")
    if math.isnan(icl2_hel):
        notes.append(f"ICL2 helicity NaN in {pdb_id} (no observed 3.50+1..+18 window).")

    return MotifResult(
        d_y558_pack=d_y558_pack,
        d_dry=d_dry,
        d_tm5_out=d_tm5_out,
        icl2_helical=icl2_hel,
        curation_note="; ".join(notes),
        obs_350=obs_350,
        obs_558=obs_558,
        obs_630=obs_630,
        chain=vmodel.chain_name,
        identity=vmodel.identity,
    )


# ---------------------------------------------------------------------------
# CSV augmentation
# ---------------------------------------------------------------------------


def _fmt_dist(x: float, digits: int = 6) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.{digits}f}"


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


def augment_reference_set(
    reference_set: Path,
    coupling_csv: Path,
    pdb_cache: Path,
    gpcrdb_cache: Path,
    rcsb_cache: Path,
    output: Path | None = None,
    only_panel: bool = True,
) -> dict[str, Any]:
    """Read reference_set.csv, compute motif refs for panel rows, write back.

    Preserves the existing column order and appends the four new columns
    at the end. Never modifies existing columns.
    """
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

        try:
            anchors = json.loads(row.get("anchor_positions") or "{}")
        except json.JSONDecodeError as e:
            summary["rows_failed"].append({
                "receptor": receptor, "role": row.get("role"),
                "pdb_id": row.get("pdb_id"),
                "error": f"anchor_positions JSON decode: {e}",
            })
            continue

        anchors = {k: int(v) for k, v in anchors.items()}
        pdb_id = (row.get("pdb_id") or "").strip()
        entry_name = (row.get("uniprot_slug") or "").strip()
        if not pdb_id or not entry_name:
            continue

        try:
            result = compute_motif_refs(
                pdb_id, entry_name, anchors,
                api=gpcrdb_api, pdb_cache=pdb_cache,
                rcsb_api=rcsb_api,
            )
        except Exception as e:  # lint-allow: capture-and-record — surface, don't abort
            summary["rows_failed"].append({
                "receptor": receptor, "role": row.get("role"),
                "pdb_id": pdb_id,
                "error": f"{type(e).__name__}: {e}",
            })
            print(f"FAIL  {receptor:<8s} {row.get('role','?'):<10s} {pdb_id}  "
                  f"{type(e).__name__}: {e}", file=sys.stderr)
            continue

        row["d_y558_pack_ref"] = _fmt_dist(result.d_y558_pack)
        row["d_dry_ref"] = _fmt_dist(result.d_dry)
        row["d_tm5_out_ref"] = _fmt_dist(result.d_tm5_out)
        # icl2_helical is a fraction, not a distance — keep more precision
        row["icl2_helical_ref"] = _fmt_dist(result.icl2_helical, digits=4)

        if result.curation_note:
            row["curation_note"] = _merge_curation(row.get("curation_note", ""),
                                                    result.curation_note)

        summary["rows_processed"] += 1
        summary["measurements"].append({
            "receptor": receptor, "role": row.get("role"),
            "pdb_id": pdb_id, "chain": result.chain,
            "identity": result.identity,
            "obs_350": result.obs_350, "obs_558": result.obs_558,
            "obs_630": result.obs_630,
            "d_y558_pack": result.d_y558_pack,
            "d_dry": result.d_dry,
            "d_tm5_out": result.d_tm5_out,
            "icl2_helical": result.icl2_helical,
            "notes": result.curation_note,
        })
        print(
            f"OK    {receptor:<8s} {row.get('role','?'):<10s} {pdb_id}  "
            f"chain={result.chain} id={result.identity:.2%}  "
            f"y558={_fmt_dist(result.d_y558_pack, 3) or 'nan':>7s}  "
            f"dry={_fmt_dist(result.d_dry, 3) or 'nan':>7s}  "
            f"tm5={_fmt_dist(result.d_tm5_out, 3) or 'nan':>7s}  "
            f"icl2={_fmt_dist(result.icl2_helical, 3) or 'nan':>6s}  "
            f"[350={result.obs_350} 558={result.obs_558} 630={result.obs_630}]"
        )

    with output.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=base_cols)
        w.writeheader()
        for row in rows:
            w.writerow({c: row.get(c, "") for c in base_cols})

    return summary


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reference-set", default=str(REPO / "refs" / "reference_set.csv"))
    ap.add_argument("--coupling-csv", default=str(REPO / "refs" / "gpcr_coupling.csv"))
    ap.add_argument("--pdb-cache", default=str(REPO / "refs" / "cache" / "pdb"))
    ap.add_argument("--gpcrdb-cache", default=str(REPO / "refs" / "cache" / "gpcrdb"))
    ap.add_argument("--rcsb-cache", default=str(REPO / "refs" / "cache" / "rcsb"))
    ap.add_argument("--output", default=None,
                    help="Destination CSV (defaults to overwrite of reference-set)")
    ap.add_argument("--include-non-panel", action="store_true",
                    help="Compute motif refs for all rows, not just the 40-receptor panel")
    ap.add_argument("--summary-json", default=None,
                    help="Optional path to write a run-summary JSON alongside stderr log")
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
        f"\n{summary['rows_processed']} panel rows measured "
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
