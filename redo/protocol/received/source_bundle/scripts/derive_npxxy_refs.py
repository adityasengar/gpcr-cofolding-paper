"""Derive NPxxY CA-CA and OH-OH reference distances for panel receptors.

PREREG §2a requires an OH-OH NPxxY column alongside the frozen CA-CA
column so a literature-derived threshold (~7-8 Å, Weis & Kobilka 2018)
can be applied without ambiguity. `refs/reference_set.csv` today carries
only TM6-axis `d_r350_r630_ca_ref`; this tool augments it with two new
columns:

    d_npxxy_ca_ref   -- Y5.58 CA <-> Y7.53 CA, in Å.
    d_npxxy_oh_ref   -- Y5.58 OH <-> Y7.53 OH, in Å. NaN when either OH is
                        absent (non-Tyr residue at the position, or an
                        atom-level truncation).

The atom-picking idiom is the same one `scorer/axes.py::d_npxxy_y558_y753_oh`
uses at prediction time: gemmi's `find_atom("CA"/"OH", "\0")` on the
UniProt-renumbered residue map from `scorer/structure.build_uniprot_model`.

Only the 40 in-panel receptors (`refs/gpcr_coupling.csv`) get filled by
default; non-panel rows are left empty and can be back-filled later. The
JSR1/B1B1U5 active row's `d_r350_r630_ca_ref` (currently
``PENDING_9EPR_REGEN``) is regenerated at the same time from the same
crystal (9EPR).

Usage
-----
    python -m scripts.derive_npxxy_refs \
        --reference-set refs/reference_set.csv \
        --pdb-cache refs/cache/pdb \
        --gpcrdb-cache refs/cache/gpcrdb

Programmatic entry
------------------
    from scripts.derive_npxxy_refs import compute_npxxy_refs
    result = compute_npxxy_refs("6G79", "5ht1b_human", anchor_positions, api, pdb_cache)
    result.d_ca, result.d_oh, result.curation_note
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from scorer.anchors import resolve_anchors
from scorer.axes import compute_all_axes
from scorer.bw_numbering import Api
from scorer.cache import content_sha256
from scorer.refs_build import load_pdb_bytes
from scorer.structure import build_uniprot_model, one_letter
from scorer.verified import verify_reference_pdb


REPO = Path(__file__).resolve().parent.parent
NaN = float("nan")


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
# NPxxY derivation
# ---------------------------------------------------------------------------


@dataclass
class NpxxyResult:
    """One (receptor, role) NPxxY reference measurement."""
    d_ca: float
    d_oh: float
    d_tm6_ca: float                          # emitted only for JSR1 regen
    curation_note: str = ""
    obs_558: str | None = None
    obs_753: str | None = None
    chain: str | None = None
    identity: float = 0.0
    pdb_sha: str | None = None


def compute_npxxy_refs(
    pdb_id: str,
    entry_name: str,
    anchor_positions: dict[str, int],
    api: Api,
    pdb_cache: Path,
    rcsb_api: Api | None = None,
) -> NpxxyResult:
    """Derive NPxxY CA-CA + OH-OH distances from a curated PDB crystal.

    Follows the same idiom as `scorer/refs_build.cmd_build`: fetch coord
    file into `pdb_cache`, run `build_uniprot_model` (chain-pick +
    UniProt-renumber via A3), then read Y5.58 and Y7.53 residues from
    the renumbered map. CA / OH atom picking mirrors
    `scorer/axes.d_npxxy_y558_y753_oh` so ref and prediction values are
    directly comparable.
    """
    pos_558 = anchor_positions.get("5.58")
    pos_753 = anchor_positions.get("7.53")
    if pos_558 is None or pos_753 is None:
        return NpxxyResult(
            d_ca=NaN, d_oh=NaN, d_tm6_ca=NaN,
            curation_note=f"anchor_positions missing 5.58/7.53 in reference_set row",
        )

    # Coordinates (via RCSB, cached under pdb_cache).
    _rcsb = rcsb_api if rcsb_api is not None else Api(cache_dir=pdb_cache)
    raw, ext = load_pdb_bytes(_rcsb, pdb_id)
    out_pdb = pdb_cache / f"{pdb_id.lower()}.{ext}"
    if not out_pdb.exists():
        out_pdb.write_bytes(raw)
    pdb_sha = content_sha256(out_pdb)

    # Chain-picking + UniProt renumbering.
    model = build_uniprot_model(str(out_pdb), entry_name, api)

    r558 = model.residues.get(pos_558)
    r753 = model.residues.get(pos_753)
    obs_558 = one_letter(r558.name) if r558 is not None else None
    obs_753 = one_letter(r753.name) if r753 is not None else None

    notes: list[str] = []

    def _ca_pos(res):
        if res is None:
            return None
        a = res.find_atom("CA", "\0")
        return a.pos if a is not None else None

    def _oh_pos(res):
        if res is None:
            return None
        a = res.find_atom("OH", "\0")
        return a.pos if a is not None else None

    ca_558 = _ca_pos(r558)
    ca_753 = _ca_pos(r753)
    oh_558 = _oh_pos(r558)
    oh_753 = _oh_pos(r753)

    if r558 is None:
        notes.append(f"5.58 residue not resolved in {pdb_id}")
    elif obs_558 != "Y":
        notes.append(
            f"5.58 is not Tyr in this receptor (observed {obs_558}); "
            "NPxxY OH-OH not meaningful."
        )
    if r753 is None:
        notes.append(f"7.53 residue not resolved in {pdb_id}")
    elif obs_753 != "Y":
        notes.append(
            f"7.53 is not Tyr in this receptor (observed {obs_753}); "
            "NPxxY OH-OH not meaningful."
        )

    if ca_558 is None and r558 is not None:
        notes.append(f"5.58 CA missing in {pdb_id}")
    if ca_753 is None and r753 is not None:
        notes.append(f"7.53 CA missing in {pdb_id}")

    # Side-chain-only truncation: residue is Tyr but the deposition did not
    # model the OH atom (typical when density past Cβ is weak). Flag so a
    # downstream reader knows the NaN is real crystallography, not a
    # residue-identity issue.
    if r558 is not None and obs_558 == "Y" and oh_558 is None:
        notes.append(f"5.58 Y sidechain OH not resolved in {pdb_id}")
    if r753 is not None and obs_753 == "Y" and oh_753 is None:
        notes.append(f"7.53 Y sidechain OH not resolved in {pdb_id}")

    d_ca = ca_558.dist(ca_753) if (ca_558 is not None and ca_753 is not None) else NaN
    d_oh = oh_558.dist(oh_753) if (oh_558 is not None and oh_753 is not None) else NaN

    # Also measure d_tm6 on the deposited coords so B1B1U5's TM6 ref
    # (PENDING_9EPR_REGEN) can be regenerated from 9EPR in the same pass.
    try:
        aset = resolve_anchors(api, entry_name)
        vresult = verify_reference_pdb(model, aset)
        axes = compute_all_axes(vresult.model)
        d_tm6 = axes["d_tm6_r350_r630_ca"]
    except Exception as e:  # lint-allow: capture-and-record — surface, don't abort
        d_tm6 = NaN
        notes.append(f"d_tm6 measurement failed: {type(e).__name__}: {e}")

    return NpxxyResult(
        d_ca=d_ca,
        d_oh=d_oh,
        d_tm6_ca=d_tm6,
        curation_note="; ".join(notes),
        obs_558=obs_558,
        obs_753=obs_753,
        chain=model.chain_name,
        identity=model.identity,
        pdb_sha=pdb_sha,
    )


# ---------------------------------------------------------------------------
# CSV augmentation
# ---------------------------------------------------------------------------


def _fmt_dist(x: float) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.6f}"


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
    """Read reference_set.csv, compute NPxxY refs for panel rows, write back.

    Preserves column order, appends `d_npxxy_ca_ref` + `d_npxxy_oh_ref` at
    the end. For B1B1U5's active row, regenerates `d_r350_r630_ca_ref` +
    replaces `provenance_sha256`.
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

    new_cols = ["d_npxxy_ca_ref", "d_npxxy_oh_ref"]
    for col in new_cols:
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
        for col in new_cols:
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
            result = compute_npxxy_refs(
                pdb_id, entry_name, anchors,
                api=gpcrdb_api, pdb_cache=pdb_cache,
                rcsb_api=rcsb_api,
            )
        except Exception as e:  # lint-allow: capture-and-record — surface
            summary["rows_failed"].append({
                "receptor": receptor, "role": row.get("role"),
                "pdb_id": pdb_id,
                "error": f"{type(e).__name__}: {e}",
            })
            print(f"FAIL  {receptor:<8s} {row.get('role','?'):<10s} {pdb_id}  {type(e).__name__}: {e}",
                  file=sys.stderr)
            continue

        row["d_npxxy_ca_ref"] = _fmt_dist(result.d_ca)
        row["d_npxxy_oh_ref"] = _fmt_dist(result.d_oh)
        if result.curation_note:
            row["curation_note"] = _merge_curation(row.get("curation_note", ""),
                                                    result.curation_note)

        # JSR1/B1B1U5 active row: replace PENDING_9EPR_REGEN with a fresh
        # measurement + a real provenance sha over the (pdb_id, entry, chain,
        # identity, sha) tuple used for this run.
        if (receptor == "B1B1U5" and row.get("role") == "active"
                and str(row.get("provenance_sha256", "")).startswith("PENDING_")):
            row["d_r350_r630_ca_ref"] = _fmt_dist(result.d_tm6_ca)
            import hashlib
            prov_payload = json.dumps({
                "pdb_id": pdb_id,
                "uniprot_slug": entry_name,
                "receptor_slug": receptor,
                "role": row.get("role"),
                "chain": result.chain,
                "identity": result.identity,
                "pdb_sha256": result.pdb_sha,
                "d_tm6_r350_r630_ca_ref": result.d_tm6_ca,
                "d_npxxy_ca_ref": result.d_ca,
                "d_npxxy_oh_ref": result.d_oh,
            }, sort_keys=True, separators=(",", ":"))
            row["provenance_sha256"] = hashlib.sha256(prov_payload.encode()).hexdigest()

        summary["rows_processed"] += 1
        summary["measurements"].append({
            "receptor": receptor, "role": row.get("role"),
            "pdb_id": pdb_id, "chain": result.chain,
            "identity": result.identity,
            "obs_558": result.obs_558, "obs_753": result.obs_753,
            "d_ca": result.d_ca, "d_oh": result.d_oh,
            "d_tm6_ca": result.d_tm6_ca,
            "notes": result.curation_note,
        })
        print(f"OK    {receptor:<8s} {row.get('role','?'):<10s} {pdb_id}  "
              f"chain={result.chain} id={result.identity:.2%}  "
              f"d_ca={_fmt_dist(result.d_ca) or 'nan':>10s}  "
              f"d_oh={_fmt_dist(result.d_oh) or 'nan':>10s}  "
              f"558={result.obs_558} 753={result.obs_753}")

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
                    help="Compute NPxxY refs for all rows, not just the 40-receptor panel")
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
