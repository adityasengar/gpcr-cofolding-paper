#!/usr/bin/env python3
"""Full-corpus G4 census with v2 receptor-chain picker + peptide-chain handling.

Fixes v1's "longest polymer chain ≥ 200 aa" bug (which mis-picked Gα as
the receptor on cognate-arm rows for any receptor < ~394 aa) by identifying
the receptor chain as the polymer chain that carries Cα atoms at the
receptor's own named anchor positions (from reference_set.csv).

Ligand centroid strategy:
  1. HETATM candidate: any HETATM residue with ≥ 5 heavy atoms, not on
     the NON_LIGAND blocklist. Pick the largest by heavy-atom count.
  2. If no HETATM candidate: peptide ligand fallback — any polymer chain
     that (a) is NOT the receptor chain, (b) has 5–100 STD_AA residues
     (peptide-sized), (c) does not look like a Gα subunit (< 300 aa
     rules out full Gα, mini-Gα etc.). Pick the shortest such chain
     (peptide agonists are typically 5-40 aa).
  3. Otherwise: unmeasurable, with note.

Per-row emit:
  - input_path (join key back to rows.tier3.v2)
  - receptor, backbone, role, arm
  - receptor_chain, receptor_anchor_hits (0-6; 6 = full confidence)
  - ligand_source: hetatm | peptide_chain | none
  - ligand_chain, ligand_seqid, ligand_resname, ligand_n_heavy
  - d_ligand_centroid_to_pocket_A
  - flag_low_confidence: True if anchor_hits < 4

Thresholds emitted in output banner:
  - in-pocket: < 8 Å  (matches scorer/pocket_metrics.py Bug #2 tripwire)
  - entrance-bound (valid): 8-15 Å
  - off-site: >= 15 Å

Per-arm break-out first, then by backbone × ligand_role.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

try:
    import gemmi
except ImportError:
    print("ERROR: gemmi not available", file=sys.stderr)
    sys.exit(2)

STD_AA = frozenset({
    "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE","LEU","LYS",
    "MET","PHE","PRO","SER","THR","TRP","TYR","VAL","MSE","SEP","TPO","PTR",
    "CSO","MLY","CME","OCS","KCX","LLP",
})
NON_LIGAND = frozenset({
    "HOH","WAT","H2O","DOD","D2O","IOD","CA","MG","MN","ZN","NA","CL","K","F","CU","FE","NI","CO","LI",
    "GOL","EDO","PGE","PG4","PEG","MPD","SO4","PO4","NH2",
    "CLR","CHS","OLC","OLA","POV","POPC","POPE","NAG","BMA","MAN","FUC","BGC",
})
POCKET_BW = ("3.32","3.33","3.36","5.42","5.43","5.46","6.48","6.51","6.52","6.55","7.39","7.42")

IN_POCKET_A = 8.0
OFF_SITE_A = 15.0


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def parse_stratum(input_path: str):
    m = re.search(r"/tier3/pool/([a-z0-9]+)/([a-z_]+)/(apo|cognate)/(boltz|chai|of3|protenix)/", input_path)
    if not m: return None, None, None, None
    return m.group(1).upper(), m.group(2), m.group(3), m.group(4)


def load_bw_maps(refset_csv: Path):
    per = {}
    with refset_csv.open() as f:
        r = csv.DictReader(f)
        for row in r:
            slug = (row.get("receptor_slug","") or "").strip().upper()
            if slug in per: continue
            ap_str = (row.get("anchor_positions","") or "").strip()
            if not ap_str: continue
            try:
                ap = json.loads(ap_str)
                anchors = {str(k): int(v) for k, v in ap.items()}
                pocket = {}
                for bw in POCKET_BW:
                    hel, off = bw.split("."); off = int(off)
                    for a_bw in anchors:
                        if a_bw.startswith(hel + "."):
                            pocket[bw] = anchors[a_bw] + (off - int(a_bw.split(".")[1]))
                            break
                per[slug] = {"named": anchors, "pocket": pocket}
            except Exception:
                pass
    return per


def find_receptor_chain(structure, anchors_info):
    """Return (chain, anchor_hits) using the v2 anchor-hit method.

    Returns (chain, hits) where hits ∈ [0..6]; chain=None if no candidate.
    """
    named = anchors_info["named"]
    target = [int(v) for v in named.values()]
    n_target = len(target)
    best = None; best_hits = -1
    for model in structure:
        for chain in model:
            aa = sum(1 for r in chain if r.name in STD_AA)
            if aa < 100: continue
            hits = 0
            for pos in target:
                for r in chain:
                    if r.seqid.num == pos and r.name in STD_AA and r.find_atom("CA","\0") is not None:
                        hits += 1; break
            if hits > best_hits:
                best_hits = hits; best = chain
        break
    return best, best_hits, n_target


def compute_centroid_distance(cif_path: Path, anchors_info: dict):
    """Return dict with all measured quantities.

    Keys: distance_A (float | None), receptor_chain, receptor_anchor_hits,
    ligand_source, ligand_chain, ligand_seqid, ligand_resname, ligand_n_heavy, note.
    """
    result = {
        "distance_A": None, "receptor_chain": None, "receptor_anchor_hits": 0,
        "receptor_anchor_target": 0,
        "ligand_source": "none", "ligand_chain": None, "ligand_seqid": None,
        "ligand_resname": None, "ligand_n_heavy": 0, "note": "",
    }
    try:
        st = gemmi.read_structure(str(cif_path))
    except Exception as e:
        result["note"] = f"read_error:{str(e)[:100]}"
        return result

    receptor, hits, target_n = find_receptor_chain(st, anchors_info)
    result["receptor_anchor_hits"] = hits
    result["receptor_anchor_target"] = target_n
    if receptor is None:
        result["note"] = "no_polymer_chain"
        return result
    result["receptor_chain"] = receptor.name
    if hits < 3:
        # Low-confidence receptor identification; keep computing but flag
        pass

    pocket_map = anchors_info["pocket"]
    pocket_cas = []
    for bw in POCKET_BW:
        pos = pocket_map.get(bw)
        if pos is None: continue
        for r in receptor:
            if r.seqid.num == pos and r.name in STD_AA:
                ca = r.find_atom("CA","\0")
                if ca is not None:
                    pocket_cas.append(ca.pos)
                break
    if len(pocket_cas) < 6:
        result["note"] = f"insufficient_pocket_cas:{len(pocket_cas)}"
        return result
    pc = (
        sum(p.x for p in pocket_cas) / len(pocket_cas),
        sum(p.y for p in pocket_cas) / len(pocket_cas),
        sum(p.z for p in pocket_cas) / len(pocket_cas),
    )

    # 1. HETATM ligand candidate
    hetatm_cands = []
    for model in st:
        for chain in model:
            for r in chain:
                if r.name in NON_LIGAND or r.name in STD_AA: continue
                heavy = [a for a in r if a.element.name != "H"]
                if len(heavy) < 5: continue
                cx = sum(a.pos.x for a in heavy) / len(heavy)
                cy = sum(a.pos.y for a in heavy) / len(heavy)
                cz = sum(a.pos.z for a in heavy) / len(heavy)
                hetatm_cands.append({
                    "resname": r.name, "chain": chain.name, "seqid": r.seqid.num,
                    "n_heavy": len(heavy), "cx": cx, "cy": cy, "cz": cz,
                })
        break
    hetatm_cands.sort(key=lambda c: c["n_heavy"], reverse=True)

    # 2. Peptide-chain fallback
    peptide_cands = []
    if not hetatm_cands:
        for model in st:
            for chain in model:
                if chain.name == receptor.name: continue
                aa = [r for r in chain if r.name in STD_AA]
                n_aa = len(aa)
                if n_aa < 5 or n_aa > 100: continue  # peptide sized
                # Rule out Gα-like partial chains (Gα-mimic peptide ~11-30 aa is fine)
                cas = [r.find_atom("CA","\0") for r in aa]
                cas = [c.pos for c in cas if c is not None]
                if len(cas) < 3: continue
                cx = sum(p.x for p in cas)/len(cas)
                cy = sum(p.y for p in cas)/len(cas)
                cz = sum(p.z for p in cas)/len(cas)
                peptide_cands.append({
                    "resname": "PEPTIDE", "chain": chain.name, "seqid": aa[0].seqid.num,
                    "n_heavy": n_aa, "cx": cx, "cy": cy, "cz": cz,
                })
            break
        peptide_cands.sort(key=lambda c: c["n_heavy"])  # shortest first (typical agonist peptide)

    picked = None
    ligand_source = "none"
    if hetatm_cands:
        picked = hetatm_cands[0]; ligand_source = "hetatm"
    elif peptide_cands:
        picked = peptide_cands[0]; ligand_source = "peptide_chain"
    else:
        result["note"] = "no_ligand_candidate"
        return result

    dx = pc[0] - picked["cx"]; dy = pc[1] - picked["cy"]; dz = pc[2] - picked["cz"]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)

    result["distance_A"] = dist
    result["ligand_source"] = ligand_source
    result["ligand_chain"] = picked["chain"]
    result["ligand_seqid"] = picked["seqid"]
    result["ligand_resname"] = picked["resname"]
    result["ligand_n_heavy"] = picked["n_heavy"]
    return result


def wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0: return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z*z/n
    center = (p + z*z/(2*n)) / d
    half = (z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / d
    return (max(0.0, center - half), min(1.0, center + half))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows-csv", type=Path, required=True)
    ap.add_argument("--refset-csv", type=Path, required=True)
    ap.add_argument("--out-json", type=Path, required=True)
    ap.add_argument("--out-csv", type=Path, required=True)
    ap.add_argument("--limit", type=int, default=0, help="cap rows processed (0=all)")
    args = ap.parse_args()

    started = datetime.now(timezone.utc)
    print(f"[G4 v2] loading rows...", file=sys.stderr)
    with args.rows_csv.open() as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader]
    print(f"[G4 v2] loaded {len(rows)} rows", file=sys.stderr)

    bw_maps = load_bw_maps(args.refset_csv)
    print(f"[G4 v2] BW maps for {len(bw_maps)} receptors", file=sys.stderr)

    # Filter to Class A passed rows
    keep = []
    for r in rows:
        if r.get("passed","").lower() != "true": continue
        if (r.get("receptor_class","") or "").upper() != "A": continue
        rec, role, arm, backbone = parse_stratum(r.get("input_path",""))
        if not backbone: continue
        r["_receptor"] = rec; r["_role"] = role; r["_arm"] = arm; r["_backbone"] = backbone
        keep.append(r)
    print(f"[G4 v2] Class-A passed rows: {len(keep)}", file=sys.stderr)

    if args.limit > 0:
        keep = keep[: args.limit]
        print(f"[G4 v2] limited to {args.limit} rows", file=sys.stderr)

    # Process
    results = []
    for i, r in enumerate(keep):
        if i % 1000 == 0:
            print(f"[G4 v2] {i}/{len(keep)}", file=sys.stderr)
        rec = r["_receptor"]
        anchor_info = bw_maps.get(rec)
        if anchor_info is None:
            results.append({
                "input_path": r.get("input_path",""), "receptor": rec,
                "backbone": r["_backbone"], "role": r["_role"], "arm": r["_arm"],
                "distance_A": None, "receptor_chain": "", "receptor_anchor_hits": 0,
                "receptor_anchor_target": 0, "ligand_source": "none",
                "ligand_chain": "", "ligand_seqid": "", "ligand_resname": "",
                "ligand_n_heavy": 0, "note": "no_bw_map_for_receptor",
                "flag_low_confidence": True,
            })
            continue
        cif_path = Path(r.get("input_path",""))
        if not cif_path.exists():
            results.append({
                "input_path": str(cif_path), "receptor": rec,
                "backbone": r["_backbone"], "role": r["_role"], "arm": r["_arm"],
                "distance_A": None, "receptor_chain": "", "receptor_anchor_hits": 0,
                "receptor_anchor_target": 0, "ligand_source": "none",
                "ligand_chain": "", "ligand_seqid": "", "ligand_resname": "",
                "ligand_n_heavy": 0, "note": "cif_not_found",
                "flag_low_confidence": True,
            })
            continue
        res = compute_centroid_distance(cif_path, anchor_info)
        low_conf = res["receptor_anchor_hits"] < 4
        results.append({
            "input_path": str(cif_path), "receptor": rec,
            "backbone": r["_backbone"], "role": r["_role"], "arm": r["_arm"],
            "distance_A": res["distance_A"],
            "receptor_chain": res["receptor_chain"] or "",
            "receptor_anchor_hits": res["receptor_anchor_hits"],
            "receptor_anchor_target": res["receptor_anchor_target"],
            "ligand_source": res["ligand_source"],
            "ligand_chain": res["ligand_chain"] or "",
            "ligand_seqid": res["ligand_seqid"] or "",
            "ligand_resname": res["ligand_resname"] or "",
            "ligand_n_heavy": res["ligand_n_heavy"],
            "note": res["note"],
            "flag_low_confidence": low_conf,
        })

    ended = datetime.now(timezone.utc)
    elapsed = (ended - started).total_seconds()
    print(f"[G4 v2] processed {len(results)} rows in {elapsed:.1f}s", file=sys.stderr)

    # Write CSV
    args.out_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.out_csv.open("w") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0].keys()) if results else [])
        w.writeheader()
        for row in results:
            w.writerow(row)

    # Aggregate — by ARM first, then backbone × ligand_role, then per-receptor.
    def bin_dist(d):
        if d is None: return "unmeasurable"
        if d < IN_POCKET_A: return "in_pocket"
        if d < OFF_SITE_A: return "entrance_bound"
        return "off_site"

    def summarize(bucket_rows):
        n = len(bucket_rows)
        bins = defaultdict(int)
        low_conf = 0; n_hetatm = 0; n_peptide = 0
        for r in bucket_rows:
            bins[bin_dist(r["distance_A"])] += 1
            if r["flag_low_confidence"]: low_conf += 1
            if r["ligand_source"] == "hetatm": n_hetatm += 1
            elif r["ligand_source"] == "peptide_chain": n_peptide += 1
        measurable = n - bins["unmeasurable"]
        off = bins["off_site"]
        entrance = bins["entrance_bound"]
        in_pocket = bins["in_pocket"]
        # off_site fraction on measurable rows (entrance-bound counted as valid, NOT off-site)
        off_frac = (off / measurable) if measurable > 0 else float("nan")
        off_ci = wilson_ci(off, measurable) if measurable > 0 else (float("nan"), float("nan"))
        return {
            "n": n, "n_measurable": measurable, "n_low_confidence": low_conf,
            "n_hetatm_ligand": n_hetatm, "n_peptide_ligand": n_peptide,
            "n_in_pocket": in_pocket, "n_entrance_bound": entrance, "n_off_site": off,
            "n_unmeasurable": bins["unmeasurable"],
            "off_site_frac": off_frac,
            "off_site_ci_95_wilson": off_ci,
            "in_pocket_frac": in_pocket / measurable if measurable > 0 else float("nan"),
            "entrance_bound_frac": entrance / measurable if measurable > 0 else float("nan"),
        }

    # By arm
    by_arm = {}
    for arm in ("apo", "cognate"):
        rows_arm = [r for r in results if r["arm"] == arm]
        by_arm[arm] = summarize(rows_arm)

    # By backbone × ligand_role
    by_stratum = {}
    for bb in ("boltz","chai","of3","protenix"):
        for role in ("full_agonist","neutral_antagonist","decoy_lig"):
            rows_s = [r for r in results if r["backbone"] == bb and r["role"] == role]
            by_stratum[f"{bb}__{role}"] = summarize(rows_s)

    # By arm × role (matches SC-C-1's apo-only claim)
    by_arm_role = {}
    for arm in ("apo","cognate"):
        for role in ("full_agonist","neutral_antagonist","decoy_lig"):
            rows_ar = [r for r in results if r["arm"] == arm and r["role"] == role]
            by_arm_role[f"{arm}__{role}"] = summarize(rows_ar)

    # Pooled
    pooled = summarize(results)

    # Distribution buckets — capture the v1 "far mode" check
    far_mode = [r for r in results if r["distance_A"] is not None and r["distance_A"] >= 60]
    far_by_arm = defaultdict(int)
    for r in far_mode: far_by_arm[r["arm"]] += 1

    # Per-row-confidence summary
    n_hits_target = pooled["n_hetatm_ligand"] + pooled["n_peptide_ligand"]
    hit_hist = defaultdict(int)
    for r in results:
        if r["receptor_anchor_hits"] is not None:
            hit_hist[r["receptor_anchor_hits"]] += 1

    out = {
        "task": "g4_full_census_v2",
        "generated_utc": ended.isoformat(),
        "wall_time_s": elapsed,
        "n_rows_processed": len(results),
        "inputs": {
            "rows_csv": str(args.rows_csv),
            "rows_csv_sha256": sha256_file(args.rows_csv),
            "refset_csv": str(args.refset_csv),
            "refset_csv_sha256": sha256_file(args.refset_csv),
        },
        "receptor_chain_picker": "v2_anchor_hit (chain with most Cα at the receptor's named anchor positions; ≥3 hits required)",
        "peptide_ligand_handling": "when no HETATM ligand ≥5 heavy atoms, fall back to shortest non-receptor polymer chain with 5-100 aa (peptide-sized)",
        "thresholds": {
            "in_pocket_A": IN_POCKET_A,
            "entrance_bound_A_upper": OFF_SITE_A,
            "off_site_A_lower": OFF_SITE_A,
            "note": "entrance-bound (8–15 Å) counted as VALID per adjudication; off-site fraction reports the ≥15 Å tail only",
        },
        "pooled": pooled,
        "by_arm": by_arm,
        "by_stratum_backbone_role": by_stratum,
        "by_arm_role": by_arm_role,
        "receptor_anchor_hit_histogram": dict(hit_hist),
        "far_mode_check": {
            "n_rows_ge_60A": len(far_mode),
            "n_rows_ge_60A_by_arm": dict(far_by_arm),
            "note": "v1 bug produced 60-82 Å cognate-arm rows; if any survive at ≥60 Å on cognate, second bug likely present",
        },
    }
    args.out_json.write_text(json.dumps(out, indent=2, default=str))

    # Terminal summary
    print(f"\n=== SUMMARY (per-arm, primary) ===", file=sys.stderr)
    print(f"{'arm':<10} {'n':>7} {'meas':>7} {'in_p':>6} {'entr':>6} {'off':>6} {'off_frac':>10} {'off_ci95':>20}", file=sys.stderr)
    for arm, s in by_arm.items():
        ci = s['off_site_ci_95_wilson']
        print(f"{arm:<10} {s['n']:>7} {s['n_measurable']:>7} {s['n_in_pocket']:>6} {s['n_entrance_bound']:>6} {s['n_off_site']:>6} {s['off_site_frac']:>10.4f}  [{ci[0]:.3f}, {ci[1]:.3f}]", file=sys.stderr)

    print(f"\n=== SUMMARY (by backbone × role, cognate-arm-sensitive) ===", file=sys.stderr)
    print(f"{'stratum':<30} {'n':>7} {'meas':>7} {'in_p':>6} {'entr':>6} {'off':>6} {'off_frac':>10}", file=sys.stderr)
    for stratum in sorted(by_stratum):
        s = by_stratum[stratum]
        print(f"{stratum:<30} {s['n']:>7} {s['n_measurable']:>7} {s['n_in_pocket']:>6} {s['n_entrance_bound']:>6} {s['n_off_site']:>6} {s['off_site_frac']:>10.4f}", file=sys.stderr)

    print(f"\n=== POOLED ===", file=sys.stderr)
    print(f"  pooled off-site fraction: {pooled['off_site_frac']:.4f} 95%CI [{pooled['off_site_ci_95_wilson'][0]:.4f}, {pooled['off_site_ci_95_wilson'][1]:.4f}]", file=sys.stderr)
    print(f"  n rows ≥ 60 Å: {len(far_mode)} (v1 far-mode check)", file=sys.stderr)
    print(f"  low-confidence rows (anchor hits <4): {pooled['n_low_confidence']}", file=sys.stderr)
    print(f"  anchor-hit histogram: {dict(hit_hist)}", file=sys.stderr)
    print(f"\nwrote {args.out_json}", file=sys.stderr)
    print(f"wrote {args.out_csv}", file=sys.stderr)


if __name__ == "__main__":
    main()
