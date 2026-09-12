#!/usr/bin/env python3
"""Compute per-receptor pocket_ca_rmsd midpoint thresholds for Gate 0.1.

For each Class A receptor with both an active and an inactive reference
PDB in ``refs/reference_set.csv``, compute the pocket_ca_rmsd between
the two references (treating active as "prediction" and inactive as
"reference"). The midpoint threshold is that divided by 2:

    threshold_pocket_midpoint = 0.5 * pocket_ca_rmsd(active vs inactive)

Rationale: pocket_ca_rmsd on a Ga-coupled-active / apo prediction row
measures "distance to the ACTIVE reference." A prediction whose
pocket_ca_rmsd is BELOW this midpoint is "closer to active than to
inactive" — the pocket has morphed toward the active conformation.
Same shape as the §14 midpoint discipline for the RMSD-primary axis.

Fallback: receptors without an inactive reference (or without cached
pdb files, or without gpcrdb residues cache) fall back to the panel
median (computed by the downstream analysis script from the row
population).

Class A only; Class B / F emit a class-deferred marker.

Outputs a CSV:
    receptor_slug, class, active_pdb, inactive_pdb, uniprot_slug,
    pocket_ca_a_vs_i, midpoint_threshold, method, notes
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))

import gemmi  # noqa: E402

from scorer.pocket_metrics import (  # noqa: E402
    build_pocket_reference_cache,
    resolve_pocket_uniprot_positions,
    tm_positions_from_bw_map,
    _superpose_transform,
    pocket_ca_rmsd as compute_pocket_ca_rmsd,
    MIN_KABSCH_CA,
)
from scorer.bw_numbering import Api, get_generic_numbers  # noqa: E402
from scorer.receptors import receptor_class as _receptor_class  # noqa: E402


def _ref_pdb_path(pdb_id: str, cache_dir: Path) -> Path | None:
    for ext in ("cif", "pdb"):
        p = cache_dir / "pdb" / f"{pdb_id.lower()}.{ext}"
        if p.exists():
            return p
    return None


def _pocket_ca_rmsd_ref_vs_ref(
    active_cache, inactive_cache, receptor_class: str,
    bw_map: dict,
) -> tuple[float, str]:
    """pocket_ca_rmsd(active_ref as "prediction" vs inactive_ref)."""
    pocket_positions, _ = resolve_pocket_uniprot_positions(bw_map, receptor_class)
    if not pocket_positions:
        return float("nan"), "class_deferred"
    tm_positions = tm_positions_from_bw_map(bw_map)

    pred_ca = []
    ref_ca = []
    for pos_u in sorted(tm_positions):
        p_pos = active_cache.ca_by_uniprot.get(pos_u)
        r_pos = inactive_cache.ca_by_uniprot.get(pos_u)
        if p_pos is None or r_pos is None:
            continue
        pred_ca.append(p_pos)
        ref_ca.append(r_pos)
    if len(pred_ca) < MIN_KABSCH_CA:
        return float("nan"), f"7tm_kabsch_low_n_{len(pred_ca)}"
    sup = _superpose_transform(pred_ca, ref_ca)
    if sup is None:
        return float("nan"), "kabsch_failed"

    to_pred_frame = sup.transform.inverse()
    ref_ca_transformed = {}
    for uniprot_pos in pocket_positions.values():
        r_pos = inactive_cache.ca_by_uniprot.get(uniprot_pos)
        if r_pos is None:
            continue
        v = to_pred_frame.apply(r_pos)
        ref_ca_transformed[uniprot_pos] = gemmi.Position(v.x, v.y, v.z)

    class _AtomShim:
        def __init__(self, pos):
            self.pos = pos
    class _ResShim:
        def __init__(self, ca_pos):
            self._ca = ca_pos
        def find_atom(self, name, alt):
            return _AtomShim(self._ca) if name == "CA" else None

    class _VModelShim:
        pass
    vm = _VModelShim()
    vm.residues = {p: _ResShim(ca) for p, ca in active_cache.ca_by_uniprot.items()}

    rmsd, note = compute_pocket_ca_rmsd(
        vm, pocket_positions, ref_ca_transformed, receptor_class,
    )
    return rmsd, note


def main() -> int:
    cache_dir = REPO / "refs" / "cache"
    gpcrdb_cache = cache_dir / "gpcrdb"
    api = Api(cache_dir=gpcrdb_cache)

    # Load reference_set.csv directly
    per_recep: dict = {}
    with (REPO / "refs" / "reference_set.csv").open() as f:
        for row in csv.DictReader(f):
            rec = row["receptor_slug"].upper()
            per_recep.setdefault(rec, {})[row["role"]] = row

    # Also load sealed active refs (which live in refs/sealed_active_refs_2026_09_01.csv).
    # File has leading '#' comment lines — strip before csv parsing.
    sealed = REPO / "refs" / "sealed_active_refs_2026_09_01.csv"
    if sealed.exists():
        with sealed.open() as f:
            lines = [ln for ln in f if not ln.startswith("#")]
        for row in csv.DictReader(lines):
            rec = (row.get("receptor_slug") or "").upper()
            if rec:
                per_recep.setdefault(rec, {}).setdefault("active", row)

    # Class from scorer.receptors.receptor_class() — the sanctioned lookup.
    def _cls(rec: str) -> str:
        try:
            return _receptor_class(rec)
        except Exception:
            return "?"

    out_rows = []
    for rec in sorted(per_recep):
        rec_cls = _cls(rec)
        active = per_recep[rec].get("active")
        inactive = per_recep[rec].get("inactive")

        active_pdb = (active or {}).get("pdb_id", "")
        inactive_pdb = (inactive or {}).get("pdb_id", "")
        uniprot = (active or inactive or {}).get("uniprot_slug", "").lower()

        base = {
            "receptor_slug": rec, "class": rec_cls,
            "active_pdb": active_pdb, "inactive_pdb": inactive_pdb,
            "uniprot_slug": uniprot,
            "pocket_ca_a_vs_i": "",
            "midpoint_threshold": "",
        }

        if rec_cls != "A":
            base.update(method="class_deferred",
                        notes=f"class_{rec_cls}_pocket_deferred")
            out_rows.append(base)
            continue
        if not active or not inactive:
            base.update(method="fallback_panel_median",
                        notes="missing_active" if not active else "missing_inactive")
            out_rows.append(base)
            continue

        a_path = _ref_pdb_path(active_pdb, cache_dir)
        i_path = _ref_pdb_path(inactive_pdb, cache_dir)
        if not a_path or not i_path:
            base.update(method="fallback_panel_median",
                        notes=f"missing_pdb_cache_active={not a_path}_inactive={not i_path}")
            out_rows.append(base)
            continue

        try:
            bw_map = get_generic_numbers(api, uniprot)
        except Exception as e:
            base.update(method="fallback_panel_median",
                        notes=f"gpcrdb_fetch_failed:{str(e)[:80]}")
            out_rows.append(base)
            continue

        try:
            active_cache = build_pocket_reference_cache(
                str(a_path), uniprot, api, pdb_id=active_pdb.upper(),
            )
            inactive_cache = build_pocket_reference_cache(
                str(i_path), uniprot, api, pdb_id=inactive_pdb.upper(),
            )
        except Exception as e:
            base.update(method="fallback_panel_median",
                        notes=f"cache_build_failed:{str(e)[:80]}")
            out_rows.append(base)
            continue

        if active_cache is None or inactive_cache is None:
            base.update(method="fallback_panel_median",
                        notes="cache_build_returned_none")
            out_rows.append(base)
            continue

        rmsd, note = _pocket_ca_rmsd_ref_vs_ref(
            active_cache, inactive_cache, rec_cls, bw_map,
        )
        midpoint = rmsd * 0.5 if (rmsd == rmsd) else float("nan")
        base.update(
            pocket_ca_a_vs_i=f"{rmsd:.4f}" if (rmsd == rmsd) else "",
            midpoint_threshold=f"{midpoint:.4f}" if (midpoint == midpoint) else "",
            method="per_receptor_midpoint" if (midpoint == midpoint) else "fallback_panel_median",
            notes=note or "",
        )
        out_rows.append(base)

    out_path = REPO / "experiments" / "020_block_c_ligand_pharmacology" / "analysis" / "gate_0_1_per_receptor_pocket_thresholds.csv"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["receptor_slug", "class", "active_pdb", "inactive_pdb",
                  "uniprot_slug", "pocket_ca_a_vs_i", "midpoint_threshold",
                  "method", "notes"]
    with out_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    n_valid = sum(1 for r in out_rows if r["midpoint_threshold"])
    n_fallback = sum(1 for r in out_rows if r["method"] == "fallback_panel_median")
    n_class_bf = sum(1 for r in out_rows if r["method"] == "class_deferred")
    print(f"wrote {out_path}: {len(out_rows)} rows")
    print(f"  per_receptor_midpoint: {n_valid}")
    print(f"  fallback_panel_median: {n_fallback}")
    print(f"  class_deferred (B/F): {n_class_bf}")
    if n_valid > 0:
        vals = sorted(float(r["midpoint_threshold"]) for r in out_rows
                     if r["midpoint_threshold"])
        print(f"  midpoints range: min={vals[0]:.4f} med={vals[len(vals)//2]:.4f} max={vals[-1]:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
