"""CURATE Phase 3 — derive active-state references for 6 curable no-active
Class A receptors + OPRD 8F7S replacement.

Emits `refs/reference_set.pending_curation.csv` — 7 rows, same schema as
`refs/reference_set.csv`. Does NOT modify `refs/reference_set.csv`.

Zero GPU. Uses the same scorer axis functions the runtime uses so ref
and prediction values are byte-comparable. Uses the Gate-2 RCSB polymer-
entity classifier (verify_active_stabilization.py) to verify each active
PDB's `active_stabilization_source`.

Targets:
  ACM1   6OIJ  (curation gap; only 1 active in GPCRdb)
  ADA2A  9CBL  (2.8 Å 2024 EM)
  ADRB1  7BU7  (2.6 Å X-ray)
  CCKAR  9BKK  (2.51 Å EM 2024)
  DRD3   8IRT  (2.7 Å EM 2023)
  OX2R   7L1V  (3.0 Å 2021)
  OPRD   8F7S  (3.0 Å 2022; Gi-bound REPLACEMENT for 6PT2 agonist-only)

Usage:
    python3 scripts/curate_phase3_derive_refs.py
"""
from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path
from typing import Any

# Make scripts.verify_active_stabilization importable as a helper.
REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

from scorer.anchors import resolve_anchors
from scorer.axes import (
    a100_component_1_ca,
    a100_component_2_ca,
    a100_component_3_ca,
    a100_component_4_ca,
    a100_component_5_ca,
    a100_index,
    angle_class_b_tm6_kink_639_650_654_deg,
    d_dry_sidechain_r350cz_e630oe1,
    d_gpcrdb_tm6_tilt_246_637_ca,
    d_npxxy_y558_y753_ca,
    d_npxxy_y558_y753_oh,
    d_tm5_outward_r350_r558_ca,
    d_tm6_r350_r630_ca,
    d_y558_pack_min_heavy,
    icl2_helical_frac,
)
from scorer.bw_numbering import Api
from scorer.refs_build import load_pdb_bytes
from scorer.structure import build_uniprot_model, one_letter
from scorer.verified import verify_reference_pdb

# Import the Gate-2 stabilization classifier verbatim.
from scripts.verify_active_stabilization import (
    classify,
    fetch_entry,
    summarise_nonpolymers,
    summarise_polymers,
)


# ---------------------------------------------------------------------------
# The 7 targets
# ---------------------------------------------------------------------------

TARGETS: list[dict[str, str]] = [
    # (receptor_slug, pdb_id, uniprot_slug, species, expected_notes)
    {"receptor_slug": "ACM1",  "pdb_id": "6OIJ", "uniprot_slug": "acm1_human",  "species": "human", "note": "Only 1 active in GPCRdb; verify Gα-heterotrimer if present."},
    {"receptor_slug": "ADA2A", "pdb_id": "9CBL", "uniprot_slug": "ada2a_human", "species": "human", "note": "2.8 Å 2024 EM; verify Gα stabilisation."},
    {"receptor_slug": "ADRB1", "pdb_id": "7BU7", "uniprot_slug": "adrb1_human", "species": "human", "note": "2.6 Å X-ray; verify not just a mini-G."},
    {"receptor_slug": "CCKAR", "pdb_id": "9BKK", "uniprot_slug": "cckar_human", "species": "human", "note": "2.51 Å EM 2024."},
    {"receptor_slug": "DRD3",  "pdb_id": "8IRT", "uniprot_slug": "drd3_human",  "species": "human", "note": "2.7 Å EM 2023; verify Gα heterotrimer."},
    {"receptor_slug": "OX2R",  "pdb_id": "7L1V", "uniprot_slug": "ox2r_human",  "species": "human", "note": "3.0 Å 2021; earlier structure."},
    {"receptor_slug": "OPRD",  "pdb_id": "8F7S", "uniprot_slug": "oprd_human",  "species": "human", "note": "REPLACEMENT for 6PT2 agonist-only — 3.0 Å 2022 Gi-bound cryo-EM."},
]

# Sanity-check ranges for Class A active-state references.
# TM6 Class A active canonical range 12-18 Å (per task brief).
# NPxxY OH-OH Class A active canonical range 3-6 Å (per task brief).
# GPCRdb TM6 tilt Class A active canonical range 15-20 Å (per task brief).
CLASS_A_TM6_RANGE = (12.0, 18.0)
CLASS_A_NPXXY_OH_RANGE = (3.0, 6.0)
CLASS_A_TM6_TILT_RANGE = (15.0, 20.0)

# Schema of refs/reference_set.csv — must match exactly.
CSV_COLS: list[str] = [
    "receptor_slug", "role", "pdb_id", "uniprot_slug", "species",
    "resolved_state", "stabilising_elements", "construct", "construct_offset",
    "d_r350_r630_ca_ref", "anchor_positions", "provenance_sha256",
    "active_stabilization_source", "alpha5_donor_class", "curation_note",
    "d_npxxy_ca_ref", "d_npxxy_oh_ref", "d_y558_pack_ref", "d_dry_ref",
    "d_tm5_out_ref", "icl2_helical_ref", "d_gpcrdb_tm6_tilt_ref",
    "a100_index_ref", "a100_component_1_ref", "a100_component_2_ref",
    "a100_component_3_ref", "a100_component_4_ref", "a100_component_5_ref",
    "angle_class_b_kink_ref",
    "icl3_status", "icl3_residues_missing", "icl3_residues_missing_count",
    "fusion_partner", "fusion_partner_insertion_range",
]

OUT_CSV = REPO / "refs" / "reference_set.pending_curation.csv"
OUT_JSON = REPO / "experiments" / "018_block_a_switch_test" / "analysis" / "curate_phase3.json"


def _fmt(x: float, ndigits: int = 6) -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    return f"{x:.{ndigits}f}"


def _short_stab_source(verified: str) -> tuple[str, str]:
    """Map the Gate-2 verified label to the (active_stabilization_source,
    alpha5_donor_class) tuple used in refs/reference_set.csv.

    Reference-set uses short labels: native, mini_G, chimera, nanobody,
    agonist_only, DVL_DEP. Gate-2 emits long labels like
    "Gα-heterotrimer-native", "Gα-heterotrimer-miniG", "Gα-only-miniG",
    "Gα-α5-CT-peptide", "nanobody-stabilised", "agonist-only", with
    optional "+aux-scFv" / "+aux-nanobody" auxiliary tags. Alpha5-donor
    is not encoded in the Gate-2 label — the alpha5 donor is either the
    receptor's cognate Gα or (for chimeras) a different family, and
    disambiguation is manual.
    """
    v = verified.lower()
    if "chimera" in v:
        primary = "chimera"
    elif "minig" in v:
        primary = "mini_G"
    elif v.startswith("gα-heterotrimer-native") or v.startswith("gα-only-native"):
        primary = "native"
    elif "gα-α5-ct-peptide" in v:
        primary = "native"  # historical convention: α5-CT-only refs marked "native"
    elif "nanobody-stabilised" in v:
        primary = "nanobody"
    elif "agonist-only" in v:
        primary = "agonist_only"
    else:
        primary = ""
    # α5 donor class isn't inferrable from Gate-2 label alone;
    # empty for now — curator can fill in from RCSB entity details.
    return primary, ""


def verify_stabilization(pdb: str) -> tuple[str, str, list[dict[str, Any]], list[dict[str, Any]], str]:
    """Return (verified_class, class_notes, polymers, nonpolymers, title)
    for the active PDB. Uses the same Gate-2 classifier that produced
    reference_state_verification_report.md.
    """
    entry = fetch_entry(pdb)
    if entry is None:
        return "unresolved", "entry fetch failed", [], [], ""
    title = (entry.get("struct", {}) or {}).get("title", "") or ""
    ci = entry.get("rcsb_entry_container_identifiers", {}) or {}
    poly_ids = ci.get("polymer_entity_ids", []) or []
    nonpoly_ids = ci.get("non_polymer_entity_ids", []) or []
    polymers = summarise_polymers(pdb, poly_ids)
    nonpolymers = summarise_nonpolymers(pdb, nonpoly_ids)
    verified, cls_notes = classify(pdb, polymers, nonpolymers, title)
    return verified, cls_notes, polymers, nonpolymers, title


def compute_all_ref_axes(
    pdb_id: str,
    entry_name: str,
    api: Api,
    pdb_cache: Path,
    rcsb_api: Api,
) -> dict[str, Any]:
    """Fetch coords, chain-pick + UniProt-renumber, run every axis function.

    Returns the fully-populated axes dict plus per-anchor availability +
    observed AA and chain-identity diagnostics used to populate the row.
    """
    raw, ext = load_pdb_bytes(rcsb_api, pdb_id)
    out_pdb = pdb_cache / f"{pdb_id.lower()}.{ext}"
    if not out_pdb.exists():
        out_pdb.write_bytes(raw)

    model = build_uniprot_model(str(out_pdb), entry_name, api)
    aset = resolve_anchors(api, entry_name)
    vresult = verify_reference_pdb(model, aset)
    vmodel = vresult.model

    def _obs(pos: int | None) -> str | None:
        if pos is None:
            return None
        r = vmodel.residues.get(pos)
        return one_letter(r.name) if r is not None else None

    pos_350 = aset.anchors["3.50"].uniprot_pos if "3.50" in aset.anchors else None
    pos_558 = aset.anchors["5.58"].uniprot_pos if "5.58" in aset.anchors else None
    pos_630 = aset.anchors["6.30"].uniprot_pos if "6.30" in aset.anchors else None
    pos_753 = aset.anchors["7.53"].uniprot_pos if "7.53" in aset.anchors else None

    notes: list[str] = []
    obs_350 = _obs(pos_350)
    obs_558 = _obs(pos_558)
    obs_630 = _obs(pos_630)
    obs_753 = _obs(pos_753)
    if obs_350 is None:
        notes.append(f"3.50 residue not resolved in {pdb_id}")
    elif obs_350 != "R":
        notes.append(f"3.50 is not Arg (observed {obs_350}).")
    if obs_558 is None:
        notes.append(f"5.58 residue not resolved in {pdb_id}")
    elif obs_558 != "Y":
        notes.append(f"5.58 is not Tyr (observed {obs_558}); Y5.58-pack meaningless.")
    if obs_630 is None:
        notes.append(f"6.30 residue not resolved in {pdb_id}")
    elif obs_630 == "D":
        notes.append("6.30 is Asp; DRY reference uses OD1 fallback in place of OE1.")
    elif obs_630 != "E":
        notes.append(f"6.30 is neither Glu nor Asp (observed {obs_630}); DRY will be NaN.")
    if obs_753 is None:
        notes.append(f"7.53 residue not resolved in {pdb_id}")
    elif obs_753 != "Y":
        notes.append(f"7.53 is not Tyr (observed {obs_753}); NPxxY-OH not meaningful.")

    d_tm6 = d_tm6_r350_r630_ca(vmodel)
    d_np_ca = d_npxxy_y558_y753_ca(vmodel)
    d_np_oh = d_npxxy_y558_y753_oh(vmodel)
    d_tm5 = d_tm5_outward_r350_r558_ca(vmodel)
    d_pack = d_y558_pack_min_heavy(vmodel)
    d_dry = d_dry_sidechain_r350cz_e630oe1(vmodel)
    icl2 = icl2_helical_frac(vmodel)

    d_tilt = d_gpcrdb_tm6_tilt_246_637_ca(vmodel)
    a100_c1 = a100_component_1_ca(vmodel)
    a100_c2 = a100_component_2_ca(vmodel)
    a100_c3 = a100_component_3_ca(vmodel)
    a100_c4 = a100_component_4_ca(vmodel)
    a100_c5 = a100_component_5_ca(vmodel)
    a100 = a100_index(vmodel)
    kink = angle_class_b_tm6_kink_639_650_654_deg(vmodel)

    if math.isnan(d_dry) and obs_630 in ("E", "D"):
        notes.append(f"DRY NaN despite E/D at 6.30 in {pdb_id} (side-chain truncated).")
    if math.isnan(d_pack) and obs_558 == "Y":
        notes.append(f"Y5.58-pack NaN despite Y at 5.58 in {pdb_id} (OH truncated).")
    if math.isnan(d_np_oh) and obs_558 == "Y" and obs_753 == "Y":
        notes.append(f"NPxxY-OH NaN despite Y5.58/Y7.53 in {pdb_id} (OH truncated).")

    anchor_positions_min = {
        k: aset.anchors[k].uniprot_pos
        for k in ("3.50", "3.51", "5.58", "6.30", "6.34", "7.53")
        if k in aset.anchors
    }

    return {
        "d_tm6": d_tm6,
        "d_np_ca": d_np_ca,
        "d_np_oh": d_np_oh,
        "d_tm5": d_tm5,
        "d_pack": d_pack,
        "d_dry": d_dry,
        "icl2": icl2,
        "d_tilt": d_tilt,
        "a100_c1": a100_c1, "a100_c2": a100_c2, "a100_c3": a100_c3,
        "a100_c4": a100_c4, "a100_c5": a100_c5,
        "a100": a100,
        "kink": kink,
        "chain": vmodel.chain_name,
        "identity": vmodel.identity,
        "matched": vmodel.matched,
        "anchor_positions": anchor_positions_min,
        "observed": {"3.50": obs_350, "5.58": obs_558, "6.30": obs_630, "7.53": obs_753},
        "notes": notes,
    }


def sanity_check(axes: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return (pass, failure_reasons)."""
    fails: list[str] = []
    d_tm6 = axes["d_tm6"]
    d_np_oh = axes["d_np_oh"]
    d_tilt = axes["d_tilt"]
    if math.isnan(d_tm6):
        fails.append(f"d_r350_r630_ca_ref is NaN (need finite for Class A active).")
    elif not (CLASS_A_TM6_RANGE[0] <= d_tm6 <= CLASS_A_TM6_RANGE[1]):
        fails.append(
            f"d_r350_r630_ca_ref={d_tm6:.2f} Å outside "
            f"Class A active range [{CLASS_A_TM6_RANGE[0]}, {CLASS_A_TM6_RANGE[1]}]."
        )
    if math.isnan(d_np_oh):
        # NPxxY-OH being NaN alone does not fail sanity — a receptor with
        # non-Tyr 5.58 or 7.53 or an OH truncation is a documented per-
        # receptor gap. Record as a soft warning only.
        pass
    elif not (CLASS_A_NPXXY_OH_RANGE[0] <= d_np_oh <= CLASS_A_NPXXY_OH_RANGE[1]):
        fails.append(
            f"d_npxxy_oh_ref={d_np_oh:.2f} Å outside "
            f"Class A active range [{CLASS_A_NPXXY_OH_RANGE[0]}, {CLASS_A_NPXXY_OH_RANGE[1]}]."
        )
    if math.isnan(d_tilt):
        fails.append("d_gpcrdb_tm6_tilt_ref is NaN (need finite for Class A active).")
    elif not (CLASS_A_TM6_TILT_RANGE[0] <= d_tilt <= CLASS_A_TM6_TILT_RANGE[1]):
        fails.append(
            f"d_gpcrdb_tm6_tilt_ref={d_tilt:.2f} Å outside "
            f"Class A active range [{CLASS_A_TM6_TILT_RANGE[0]}, {CLASS_A_TM6_TILT_RANGE[1]}]."
        )
    return (len(fails) == 0), fails


def build_row(
    target: dict[str, str],
    verified_class: str,
    class_notes: str,
    title: str,
    axes: dict[str, Any],
    sanity_ok: bool,
    sanity_reasons: list[str],
) -> dict[str, str]:
    primary, donor = _short_stab_source(verified_class)
    curation_note_parts = []
    curation_note_parts.append(f"CURATE Phase 3 (2026-09-02): {target['note']}")
    curation_note_parts.append(f"Gate-2 verified stabilization: {verified_class}")
    if class_notes:
        curation_note_parts.append(class_notes)
    if title:
        curation_note_parts.append(f"RCSB title: {title}")
    if axes["notes"]:
        curation_note_parts.append("; ".join(axes["notes"]))
    if sanity_ok:
        curation_note_parts.append(
            "SANITY-CHECK PASS (Class A active ranges d_tm6∈[12,18], "
            "d_npxxy_oh∈[3,6], d_tilt∈[15,20])."
        )
    else:
        curation_note_parts.append("SANITY-CHECK FAIL: " + " | ".join(sanity_reasons))

    row = {
        "receptor_slug": target["receptor_slug"],
        "role": "active",
        "pdb_id": target["pdb_id"],
        "uniprot_slug": target["uniprot_slug"],
        "species": target["species"],
        "resolved_state": "Ga-coupled-active",
        "stabilising_elements": "none",  # matches existing convention;
                                          # active_stabilization_source is
                                          # the load-bearing column
        "construct": "wt",
        "construct_offset": "0",
        "d_r350_r630_ca_ref": _fmt(axes["d_tm6"]),
        "anchor_positions": json.dumps(
            {k: axes["anchor_positions"][k] for k in axes["anchor_positions"]},
            separators=(",", ":"),
        ),
        "provenance_sha256": "",  # populated at merge time by refs_build
        "active_stabilization_source": primary,
        "alpha5_donor_class": donor,
        "curation_note": " | ".join(curation_note_parts),
        "d_npxxy_ca_ref": _fmt(axes["d_np_ca"]),
        "d_npxxy_oh_ref": _fmt(axes["d_np_oh"]),
        "d_y558_pack_ref": _fmt(axes["d_pack"]),
        "d_dry_ref": _fmt(axes["d_dry"]),
        "d_tm5_out_ref": _fmt(axes["d_tm5"]),
        "icl2_helical_ref": _fmt(axes["icl2"], ndigits=4),
        "d_gpcrdb_tm6_tilt_ref": _fmt(axes["d_tilt"]),
        "a100_index_ref": _fmt(axes["a100"], ndigits=3),
        "a100_component_1_ref": _fmt(axes["a100_c1"]),
        "a100_component_2_ref": _fmt(axes["a100_c2"]),
        "a100_component_3_ref": _fmt(axes["a100_c3"]),
        "a100_component_4_ref": _fmt(axes["a100_c4"]),
        "a100_component_5_ref": _fmt(axes["a100_c5"]),
        # Class A: kink is not applicable — leave blank per task brief.
        "angle_class_b_kink_ref": "",
        "icl3_status": "",
        "icl3_residues_missing": "",
        "icl3_residues_missing_count": "",
        "fusion_partner": "",
        "fusion_partner_insertion_range": "",
    }
    return row


def main() -> int:
    pdb_cache = REPO / "refs" / "cache" / "pdb"
    gpcrdb_cache = REPO / "refs" / "cache" / "gpcrdb"
    rcsb_cache = REPO / "refs" / "cache" / "rcsb"
    pdb_cache.mkdir(parents=True, exist_ok=True)
    gpcrdb_api = Api(cache_dir=gpcrdb_cache)
    rcsb_api = Api(cache_dir=rcsb_cache)

    rows: list[dict[str, str]] = []
    audit: list[dict[str, Any]] = []

    for target in TARGETS:
        slug = target["receptor_slug"]
        pdb = target["pdb_id"]
        print(f"\n=== {slug} {pdb} ===", flush=True)

        verified_class, class_notes, polymers, nonpolymers, title = verify_stabilization(pdb)
        print(f"  Gate-2 verified: {verified_class}")
        if class_notes:
            print(f"  notes: {class_notes}")

        try:
            axes = compute_all_ref_axes(
                pdb, target["uniprot_slug"],
                api=gpcrdb_api, pdb_cache=pdb_cache, rcsb_api=rcsb_api,
            )
        except Exception as e:  # lint-allow: surface + skip row
            print(f"  DERIVATION FAILED: {type(e).__name__}: {e}", file=sys.stderr)
            audit.append({
                "target": target,
                "verified_class": verified_class,
                "class_notes": class_notes,
                "derivation_failed": f"{type(e).__name__}: {e}",
                "row_included": False,
            })
            continue

        print(f"  chain={axes['chain']} identity={axes['identity']:.2%} matched={axes['matched']}")
        print(f"  d_tm6={_fmt(axes['d_tm6'], 2)}  d_npxxy_oh={_fmt(axes['d_np_oh'], 2)}  "
              f"d_tilt={_fmt(axes['d_tilt'], 2)}  A100={_fmt(axes['a100'], 2)}")

        sanity_ok, sanity_reasons = sanity_check(axes)
        print(f"  SANITY: {'PASS' if sanity_ok else 'FAIL — ' + ' | '.join(sanity_reasons)}")

        row = build_row(target, verified_class, class_notes, title, axes, sanity_ok, sanity_reasons)
        audit.append({
            "target": target,
            "verified_class": verified_class,
            "class_notes": class_notes,
            "title": title,
            "polymers": polymers,
            "nonpolymers": nonpolymers,
            "chain": axes["chain"],
            "identity": axes["identity"],
            "matched": axes["matched"],
            "observed": axes["observed"],
            "axes": {
                "d_r350_r630_ca_ref": axes["d_tm6"],
                "d_npxxy_ca_ref": axes["d_np_ca"],
                "d_npxxy_oh_ref": axes["d_np_oh"],
                "d_y558_pack_ref": axes["d_pack"],
                "d_dry_ref": axes["d_dry"],
                "d_tm5_out_ref": axes["d_tm5"],
                "icl2_helical_ref": axes["icl2"],
                "d_gpcrdb_tm6_tilt_ref": axes["d_tilt"],
                "a100_index_ref": axes["a100"],
                "a100_component_1_ref": axes["a100_c1"],
                "a100_component_2_ref": axes["a100_c2"],
                "a100_component_3_ref": axes["a100_c3"],
                "a100_component_4_ref": axes["a100_c4"],
                "a100_component_5_ref": axes["a100_c5"],
                "angle_class_b_kink_ref": axes["kink"],
            },
            "sanity_pass": sanity_ok,
            "sanity_reasons": sanity_reasons,
            "notes": axes["notes"],
            "row_included": sanity_ok,
        })

        if sanity_ok:
            rows.append(row)
        else:
            print(f"  ROW EXCLUDED (sanity fail).", file=sys.stderr)

    # Write pending_curation CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS)
        w.writeheader()
        for row in rows:
            w.writerow(row)
    print(f"\nWROTE {OUT_CSV} with {len(rows)} rows.")

    # Write JSON sidecar with full audit trail
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps({
        "targets": TARGETS,
        "audit": audit,
        "sanity_ranges": {
            "d_r350_r630_ca_ref": CLASS_A_TM6_RANGE,
            "d_npxxy_oh_ref": CLASS_A_NPXXY_OH_RANGE,
            "d_gpcrdb_tm6_tilt_ref": CLASS_A_TM6_TILT_RANGE,
        },
    }, indent=2, default=str))
    print(f"WROTE {OUT_JSON}")

    n_pass = sum(1 for a in audit if a.get("sanity_pass") is True)
    n_fail = sum(1 for a in audit if a.get("sanity_pass") is False)
    n_deriv_fail = sum(1 for a in audit if a.get("derivation_failed"))
    print(f"\nSummary: {n_pass} PASS, {n_fail} sanity-FAIL, {n_deriv_fail} derivation-FAIL out of {len(TARGETS)}.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
