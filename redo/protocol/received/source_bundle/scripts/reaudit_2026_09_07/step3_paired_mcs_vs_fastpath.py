#!/usr/bin/env python3
"""Step 3 — paired MCS-vs-fast-path estimator control.

Runs on HPC (needs prediction CIFs + reference cache access). Deployed via
scp + ssh to `/home/sengaad1/paper_af3/` so it uses the fixed scorer.

For a sample of rows where the fast path succeeded (OF3+Protenix on any
role with method='atom_name_element' or v2 numeric), re-run MCS on the
same pred/ref pair. Report per-row (fast_path_rmsd, mcs_rmsd, delta).

Bug #3 hypothesis: MCS pairing is not automorphism-safe. If MCS reproduces
the fast-path RMSD within noise on these rows, MCS is validated. If not,
the bias is quantified on rows with a known-good ground truth.

Sample size: 500 rows across (backbone × ligand_role × arm) to bound
runtime. Deterministic sample.
"""
from __future__ import annotations
import csv, json, random, sys
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, "/home/sengaad1/paper_af3")

import gemmi
from scorer.pocket_metrics import (
    _mcs_ligand_rmsd, _superpose_transform,
    POCKET_BW_LABELS, resolve_pocket_uniprot_positions,
    build_pocket_reference_cache, ligand_rmsd_to_ref,
    tm_positions_from_bw_map,
)
from scorer.structure import build_uniprot_model, STD_AA, one_letter
from scorer.references import _role_for_state
from scorer.bw_numbering import load_bw_map, BW_MAP_ROOT
from scorer.receptors import load_receptor_map, RECEPTOR_MAP_PATH
from scorer.cli import _make_api

REPO = Path("/home/sengaad1/paper_af3")


def main() -> int:
    rows_csv = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv"
    manifest = REPO / "experiments/021_block_c_tier3_pharmacology/analysis/rescore_manifest.tier3.v2.csv"
    ref_set_csv = REPO / "refs/reference_set.csv"
    cache_dir = REPO / "refs/cache"

    # Manifest for backbone + ligand_role join
    m_idx = {r["prediction_path"]: r for r in csv.DictReader(manifest.open())}

    # Sample: OF3+Protenix rows with numeric ligand_rmsd_to_ref
    candidates = []
    for r in csv.DictReader(rows_csv.open()):
        if r.get("passed", "").lower() != "true":
            continue
        lrmsd = r.get("ligand_rmsd_to_ref", "")
        try:
            v = float(lrmsd)
            if v != v: continue
        except (ValueError, TypeError):
            continue
        ip = r.get("input_path", "")
        m = m_idx.get(ip)
        if not m: continue
        bb = m["backbone"].lower()
        if bb not in ("of3", "protenix"): continue
        # v2 was pre-MCS, so ALL these are fast-path successes
        candidates.append({
            "input_path": ip,
            "backbone": bb,
            "ligand_role": m["ligand_role"],
            "partner_type": m["partner_type"],
            "receptor": r.get("receptor_slug", "").upper(),
            "state_claim": r.get("input_state_claim", ""),
            "ligand_type": m.get("ligand_type", ""),
            "fast_path_rmsd": v,
        })

    print(f"[step3] {len(candidates)} OF3+Protenix candidate rows with fast-path RMSD", flush=True)

    # Stratified sample: 500 total, spread across (backbone × ligand_role × arm)
    rng = random.Random(20260907)
    strata = defaultdict(list)
    for c in candidates:
        arm = "apo" if c["partner_type"] == "apo" else "cognate"
        strata[(c["backbone"], c["ligand_role"], arm)].append(c)
    n_per_stratum = max(1, 500 // len(strata))
    sample = []
    for s, xs in strata.items():
        rng.shuffle(xs)
        sample.extend(xs[:n_per_stratum])
    print(f"[step3] sampled {len(sample)} across {len(strata)} strata", flush=True)

    # Load ref set + build receptor map + BW map
    ref_set = list(csv.DictReader(ref_set_csv.open()))
    receptor_map = load_receptor_map(str(RECEPTOR_MAP_PATH))
    api = _make_api(str(cache_dir))

    # Cache PocketReferenceCache by (receptor, role, role_specific)
    ref_cache = {}
    def get_ref(receptor, role, role_specific=""):
        key = (receptor.upper(), role, role_specific)
        if key in ref_cache:
            return ref_cache[key]
        # Find the reference PDB
        pdb = None
        for r in ref_set:
            if (r.get("receptor_slug","").upper() == receptor.upper()
                and r.get("role","").lower() == role
                and r.get("role_specific","").strip() == role_specific):
                pdb = r.get("pdb_id","").strip()
                break
        if not pdb and role_specific:
            # fallback to generic inactive
            return get_ref(receptor, role, "")
        if not pdb:
            ref_cache[key] = None
            return None
        # Locate CIF
        cif = REPO / f"refs/cache/rcsb/pdb_{pdb.lower()}.cif"
        if not cif.exists():
            ref_cache[key] = None
            return None
        # entry_name from receptor_map
        entry_name = receptor_map.get(receptor.upper(), {}).get("uniprot_entry_name", "")
        if not entry_name:
            ref_cache[key] = None
            return None
        cache = build_pocket_reference_cache(str(cif), entry_name, api, pdb_id=pdb)
        ref_cache[key] = cache
        return cache

    # For each sampled row, load prediction and re-run MCS
    results = []
    for i, c in enumerate(sample, 1):
        if i % 20 == 0:
            print(f"[step3] {i}/{len(sample)}", flush=True)
        try:
            struct = gemmi.read_structure(c["input_path"])
            # Build vmodel
            entry_name = receptor_map.get(c["receptor"], {}).get("uniprot_entry_name", "")
            if not entry_name:
                results.append({**c, "mcs_rmsd": "no_entry_name", "delta": ""})
                continue
            vmodel = build_uniprot_model(c["input_path"], entry_name, api)
            # BW map
            bw_map = load_bw_map(c["receptor"], BW_MAP_ROOT)
            if bw_map is None:
                results.append({**c, "mcs_rmsd": "no_bw_map", "delta": ""})
                continue
            pocket_positions, _missing_bw = resolve_pocket_uniprot_positions(bw_map, "A")
            tm_positions = tm_positions_from_bw_map(bw_map)
            # Determine ref
            role, role_specific = ("active", "") if c["ligand_role"] in ("full_agonist", "decoy_lig", "none", "") \
                else ("inactive", "inactive_neutral_antagonist" if c["ligand_role"] == "neutral_antagonist"
                      else "inactive_inverse_agonist" if c["ligand_role"] == "inverse_agonist" else "")
            ref = get_ref(c["receptor"], role, role_specific)
            if ref is None or ref.ligand_atoms_positions is None or len(ref.ligand_atoms_positions) == 0:
                results.append({**c, "mcs_rmsd": "no_ref_ligand", "delta": ""})
                continue

            # Run 7TM Kabsch
            pred_ca = []
            ref_ca = []
            for pos_u in sorted(tm_positions):
                pred_res = vmodel.residues.get(pos_u)
                ref_pos = ref.ca_by_uniprot.get(pos_u)
                if pred_res is None or ref_pos is None: continue
                pred_atom = pred_res.find_atom("CA", "\0")
                if pred_atom is None: continue
                pred_ca.append(pred_atom.pos)
                ref_ca.append(ref_pos)
            sup = _superpose_transform(pred_ca, ref_ca)
            if sup is None:
                results.append({**c, "mcs_rmsd": "kabsch_failed", "delta": ""})
                continue
            to_pred_frame = sup.transform.inverse()

            # Collect prediction ligand atoms (using scorer's post-fix logic)
            _chain_std_aa_count = {}
            model = struct[0]
            for _ch in model:
                _chain_std_aa_count[_ch.name] = sum(1 for _r in _ch if one_letter(_r.name) in STD_AA)
            pred_atoms = []
            for ch in model:
                chain_is_gprotein = _chain_std_aa_count.get(ch.name, 0) >= 50
                for r in ch:
                    if one_letter(r.name) in STD_AA:
                        if ch.name == "A" or chain_is_gprotein: continue
                    if r.name in {"HOH","WAT","DOD","NA","K","MG","CA","ZN","MN","FE","CL","BR","IOD","F",
                                  "SO4","PO4","PEG","GOL","EDO","TRS","BOG","BME","MPD","DMS",
                                  "OLC","OLA","OLB","PLM","CLR","CHS","CHD","CLA","PGV","LMT",
                                  "STE","PC1","PEE","LFA","MPG","PGE","1PE","P6G","ACT","FMT","IPA"}:
                        continue
                    if one_letter(r.name) == "?" and len(r.name) == 1: continue
                    for a in r:
                        if a.element.name == "H": continue
                        pred_atoms.append((a.name, gemmi.Position(a.pos.x, a.pos.y, a.pos.z), a.element.name))
            if not pred_atoms:
                results.append({**c, "mcs_rmsd": "no_pred_ligand", "delta": ""})
                continue

            # Transform reference ligand atoms
            ref_atoms_transformed = []
            for pos, name, elem in zip(ref.ligand_atoms_positions, ref.ligand_atom_names, ref.ligand_atom_elements):
                if elem == "H": continue
                v = to_pred_frame.apply(pos)
                p = gemmi.Position(v.x, v.y, v.z)
                ref_atoms_transformed.append((name, p, elem))

            # Force MCS (skip fast-path)
            mcs_rmsd, mcs_note, method = _mcs_ligand_rmsd(pred_atoms, ref_atoms_transformed)
            delta = mcs_rmsd - c["fast_path_rmsd"] if mcs_rmsd == mcs_rmsd else float("nan")
            results.append({**c, "mcs_rmsd": mcs_rmsd, "delta": delta, "mcs_note": mcs_note, "mcs_method": method})
        except Exception as e:
            results.append({**c, "mcs_rmsd": f"exception:{type(e).__name__}:{e}", "delta": ""})

    # Write
    OUT = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/step3_paired_mcs_vs_fastpath.csv"
    with OUT.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["backbone","receptor","ligand_role","partner_type","fast_path_rmsd","mcs_rmsd","delta","mcs_method","input_path"])
        for r in results:
            w.writerow([
                r.get("backbone",""), r.get("receptor",""), r.get("ligand_role",""), r.get("partner_type",""),
                r.get("fast_path_rmsd",""), r.get("mcs_rmsd",""), r.get("delta",""),
                r.get("mcs_method",""), r.get("input_path",""),
            ])

    # Summary
    valid = [r for r in results if isinstance(r.get("delta"), float) and r["delta"] == r["delta"]]
    print()
    print(f"[step3] wrote {OUT}")
    print(f"  n_valid_pairs={len(valid)} / {len(results)}")
    if valid:
        deltas = [r["delta"] for r in valid]
        import statistics
        deltas_abs = [abs(d) for d in deltas]
        n_flipped = sum(
            1 for r in valid
            if (r["fast_path_rmsd"] < 3.0) != (r["mcs_rmsd"] < 3.0)
        )
        n_inflated = sum(1 for d in deltas if d > 0.5)
        n_deflated = sum(1 for d in deltas if d < -0.5)
        print(f"  fast_path_median={statistics.median(r['fast_path_rmsd'] for r in valid):.3f}")
        print(f"  mcs_median={statistics.median(r['mcs_rmsd'] for r in valid):.3f}")
        print(f"  delta_median={statistics.median(deltas):.3f}   mean={statistics.mean(deltas):.3f}   sd={statistics.stdev(deltas) if len(deltas)>1 else 0:.3f}")
        print(f"  |delta| median={statistics.median(deltas_abs):.3f}   max={max(deltas_abs):.3f}")
        print(f"  n_flipped_verdict (fast<3 vs mcs<3 disagree): {n_flipped}/{len(valid)} ({100*n_flipped/len(valid):.1f}%)")
        print(f"  n_inflated (MCS > FP by 0.5 Å): {n_inflated}")
        print(f"  n_deflated (MCS < FP by 0.5 Å): {n_deflated}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
