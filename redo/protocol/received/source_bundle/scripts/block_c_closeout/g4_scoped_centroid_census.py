#!/usr/bin/env python3
"""G4 — scoped stratified ligand-centroid vs pocket-anchor-centroid census.

Runs on HPC (where prediction CIFs live in
/hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool/).

Sampling rule:
  - Stratify by (backbone × ligand_role) → 12 strata.
  - Within each stratum: 40 rows random-sample (seed 20260910), plus
    up to 10 additional rows where pocket_notes contains
    "no_atom_match" (matcher-failure enriched — the most-likely off-
    site cases).
  - Total budget: ~500 rows.

Metric:
  - Predicted CIF has receptor chain + ligand HETATM chain(s).
  - Compute ligand-heavy-atom centroid.
  - Compute pocket-anchor-Cα centroid from the 12 BW pocket anchors
    (same set as scorer/pocket_metrics.py): 3.32, 3.33, 3.36, 5.42,
    5.43, 5.46, 6.48, 6.51, 6.52, 6.55, 7.39, 7.42.
  - Distance = Euclidean distance between the two centroids.
  - Bin: in-pocket (< 8 Å), pocket-adjacent (8-15 Å), off-site (>= 15 Å).

The scorer's Bug #2 tripwire uses an 8 Å cutoff to declare a HETATM
"pocket-plausible"; matching that threshold here means "in-pocket".

Outputs:
  - JSON with per-stratum n_sampled, n_in_pocket, n_pocket_adjacent,
    n_off_site, off_site_fraction with 95% Wilson CI.
  - CSV with per-row measurement.

Usage on HPC:
  python3 g4_scoped_centroid_census.py \\
    --rows-csv /hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/analysis/rows.tier3.v2.csv \\
    --refset-csv /hpc/scratch/sengaad1/paper_af3/refs/reference_set.csv \\
    --out-json g4_scoped_centroid_census.json \\
    --out-csv g4_scoped_centroid_census.csv
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

# Only stdlib — HPC may not have pandas/gemmi in every venv. Fall back to
# gemmi if available (we need it for CIF parsing).
try:
    import gemmi
except ImportError:
    print("ERROR: gemmi not available; install gemmi in the venv running this script")
    sys.exit(2)

STD_AA = frozenset({
    "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE",
    "LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL",
    "MSE","SEP","TPO","PTR","CSO","MLY","CME","OCS","KCX","LLP",
    # Common modified residues that should count as protein
})

# Match scorer/pocket_metrics.py::POCKET_BW_LABELS
POCKET_BW = ("3.32","3.33","3.36","5.42","5.43","5.46","6.48","6.51","6.52","6.55","7.39","7.42")

# Buffer / crystallization / lipid resnames to skip in HETATM scan
NON_LIGAND_RESNAMES = frozenset({
    "HOH","WAT","H2O","DOD","D2O","IOD","CA","MG","MN","ZN","NA","CL",
    "K","F","CU","FE","NI","CO","LI","BR","SR","BA","CS","RB",
    "GOL","EDO","PGE","PG4","PEG","MPD","SO4","PO4","NH2",
    "CLR","CHS","OLC","OLA","POV","POPC","POPE",  # lipids
    "NAG","BMA","MAN","FUC","BGC",  # glycans
})


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def parse_stratum(input_path: str):
    m = re.search(r"/tier3/pool/([a-z0-9]+)/([a-z_]+)/(apo|cognate)/(boltz|chai|of3|protenix)/", input_path)
    if not m:
        return None, None, None, None
    return m.group(1).upper(), m.group(2), m.group(3), m.group(4)


def wilson_ci(k: int, n: int, z: float = 1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z*z/n
    center = (p + z*z/(2*n)) / d
    half = (z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / d
    return (max(0.0, center - half), min(1.0, center + half))


def compute_centroid_distance(cif_path: Path, receptor_uniprot_pos_map: dict) -> tuple[float | None, dict]:
    """Return (centroid_distance_A, note_dict). None if measurement fails.

    Method:
      - Read CIF.
      - Find the receptor chain: longest polymer chain with ≥ 200 STD_AA residues.
      - Compute pocket-anchor-Cα centroid from the 12 pocket BW positions'
        UniProt residues.
      - Find HETATM ligand candidates in any chain. Pick the largest by
        heavy-atom count (as scorer/pocket_metrics.py does).
      - Compute ligand-heavy-atom centroid.
      - Return Euclidean distance between centroids.
    """
    notes = {}
    try:
        st = gemmi.read_structure(str(cif_path))
    except Exception as e:
        notes["read_error"] = str(e)[:200]
        return None, notes

    # 1. Find receptor chain: longest chain with mostly STD_AA
    receptor_chain = None
    receptor_len = 0
    for model in st:
        for chain in model:
            aa_count = sum(1 for r in chain if r.name in STD_AA)
            if aa_count >= 200 and aa_count > receptor_len:
                receptor_chain = chain
                receptor_len = aa_count
        break
    if receptor_chain is None:
        notes["no_receptor_chain"] = True
        return None, notes

    # 2. Compute pocket-anchor-Cα centroid using SIFTS from CIF's struct_ref_seq
    # Since SIFTS parsing is complex, fall back to auth_seq_id = UniProt-pos assumption
    # (works for AF3-family predictions where numbering is straight UniProt).
    pocket_positions = []
    for bw in POCKET_BW:
        pos = receptor_uniprot_pos_map.get(bw)
        if pos is None: continue
        pocket_positions.append((bw, pos))
    if len(pocket_positions) < 6:
        notes["insufficient_pocket_anchors"] = len(pocket_positions)
        return None, notes

    pocket_cas = []
    missing_bws = []
    for bw, pos in pocket_positions:
        found = None
        for r in receptor_chain:
            if r.seqid.num == pos:
                ca = r.find_atom("CA", "\0")
                if ca is not None:
                    found = ca.pos
                    break
        if found is None:
            missing_bws.append(bw)
        else:
            pocket_cas.append(found)
    if len(pocket_cas) < 6:
        notes["insufficient_pocket_cas"] = len(pocket_cas)
        notes["missing_bws"] = missing_bws
        return None, notes

    pocket_centroid = (
        sum(p.x for p in pocket_cas) / len(pocket_cas),
        sum(p.y for p in pocket_cas) / len(pocket_cas),
        sum(p.z for p in pocket_cas) / len(pocket_cas),
    )

    # 3. Find ligand HETATM(s) — pick largest by heavy-atom count
    best_ligand_atoms = None
    best_ligand_size = 0
    for model in st:
        for chain in model:
            for r in chain:
                if r.name in NON_LIGAND_RESNAMES: continue
                if r.name in STD_AA: continue
                heavy = [a for a in r if a.element.name != "H"]
                if len(heavy) < 5: continue  # too small to be an orthosteric ligand
                if len(heavy) > best_ligand_size:
                    best_ligand_atoms = heavy
                    best_ligand_size = len(heavy)
        break
    if best_ligand_atoms is None:
        notes["no_ligand_hetatm"] = True
        return None, notes

    ligand_centroid = (
        sum(a.pos.x for a in best_ligand_atoms) / len(best_ligand_atoms),
        sum(a.pos.y for a in best_ligand_atoms) / len(best_ligand_atoms),
        sum(a.pos.z for a in best_ligand_atoms) / len(best_ligand_atoms),
    )

    dx = pocket_centroid[0] - ligand_centroid[0]
    dy = pocket_centroid[1] - ligand_centroid[1]
    dz = pocket_centroid[2] - ligand_centroid[2]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)
    notes["n_pocket_cas"] = len(pocket_cas)
    notes["n_ligand_heavy"] = best_ligand_size
    return dist, notes


def load_receptor_bw_maps(refset_csv: Path):
    """Return receptor_slug (upper) → {bw_label → uniprot_pos}."""
    per_rec_map = {}
    with refset_csv.open() as f:
        r = csv.DictReader(f)
        for row in r:
            slug = row.get("receptor_slug","").strip().upper()
            if slug in per_rec_map: continue
            ap_str = row.get("anchor_positions","").strip()
            if not ap_str: continue
            try:
                ap = json.loads(ap_str)
                # ap only has 6 named anchors. Derive the 12 pocket anchors
                # by within-helix offsets from those.
                anchors = {str(k): int(v) for k, v in ap.items()}
                # For each pocket BW, find helix anchor in ap
                pocket_map = {}
                for bw in POCKET_BW:
                    hel = bw.split(".")[0]
                    off = int(bw.split(".")[1])
                    anchor_key = None; anchor_off = None
                    for a_bw in anchors:
                        if a_bw.startswith(hel + "."):
                            anchor_key = a_bw
                            anchor_off = int(a_bw.split(".")[1])
                            break
                    if anchor_key is None: continue
                    pocket_map[bw] = anchors[anchor_key] + (off - anchor_off)
                per_rec_map[slug] = pocket_map
            except Exception:
                pass
    return per_rec_map


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows-csv", type=Path, required=True)
    ap.add_argument("--refset-csv", type=Path, required=True)
    ap.add_argument("--out-json", type=Path, required=True)
    ap.add_argument("--out-csv", type=Path, required=True)
    ap.add_argument("--n-per-stratum", type=int, default=40,
                    help="random rows per (backbone × ligand_role) stratum")
    ap.add_argument("--n-enriched-per-stratum", type=int, default=10,
                    help="additional rows enriched for matcher-failure signals")
    ap.add_argument("--seed", type=int, default=20260910)
    args = ap.parse_args()

    # Load rows
    print("[G4] loading rows...", file=sys.stderr)
    with args.rows_csv.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    print(f"[G4] loaded {len(rows)} rows", file=sys.stderr)

    # Load receptor BW maps
    bw_maps = load_receptor_bw_maps(args.refset_csv)
    print(f"[G4] BW maps for {len(bw_maps)} receptors", file=sys.stderr)

    # Filter to Class A passed rows, enrich with stratum
    filtered = []
    for r in rows:
        if r.get("passed", "").lower() != "true": continue
        if (r.get("receptor_class", "") or "").upper() != "A": continue
        rec, role, arm, backbone = parse_stratum(r.get("input_path", ""))
        if not backbone: continue
        r["_stratum"] = f"{backbone}__{role}"
        r["_receptor"] = rec
        r["_role"] = role
        r["_arm"] = arm
        r["_backbone"] = backbone
        filtered.append(r)
    print(f"[G4] filtered to {len(filtered)} Class-A passed rows", file=sys.stderr)

    # Group by stratum
    by_stratum = defaultdict(list)
    for r in filtered:
        by_stratum[r["_stratum"]].append(r)

    # Sample
    rng = random.Random(args.seed)
    sample = []
    for stratum, srows in by_stratum.items():
        rng.shuffle(srows)
        rand_pick = srows[: args.n_per_stratum]
        # Enriched: rows with pocket_notes containing "no_atom_match" or "no_ref_ligand"
        enriched = [
            r for r in srows[args.n_per_stratum :]
            if any(t in (r.get("pocket_notes", "") or "") for t in ["no_atom_match", "no_ref_ligand"])
        ]
        enriched_pick = enriched[: args.n_enriched_per_stratum]
        sample.extend(rand_pick + enriched_pick)
    print(f"[G4] sample size: {len(sample)}", file=sys.stderr)

    # Process each sampled row
    results = []
    started = datetime.now(timezone.utc)
    for i, r in enumerate(sample):
        if i % 20 == 0:
            print(f"[G4] {i}/{len(sample)}...", file=sys.stderr)
        rec = r["_receptor"]
        bw_map = bw_maps.get(rec, {})
        cif_path = Path(r.get("input_path", ""))
        if not cif_path.exists():
            results.append({
                "input_path": str(cif_path), "backbone": r["_backbone"],
                "role": r["_role"], "arm": r["_arm"], "receptor": rec,
                "distance_A": None, "note": "cif_not_found",
            })
            continue
        d, notes = compute_centroid_distance(cif_path, bw_map)
        results.append({
            "input_path": str(cif_path), "backbone": r["_backbone"],
            "role": r["_role"], "arm": r["_arm"], "receptor": rec,
            "distance_A": d, "note": ";".join(f"{k}={v}" for k, v in notes.items()) if notes else "",
        })

    ended = datetime.now(timezone.utc)
    elapsed = (ended - started).total_seconds()

    # Per-stratum bins
    per_stratum = defaultdict(lambda: {"n":0, "in_pocket":0, "pocket_adj":0, "off_site":0, "unmeasurable":0})
    for row in results:
        key = f"{row['backbone']}__{row['role']}"
        s = per_stratum[key]
        s["n"] += 1
        d = row.get("distance_A")
        if d is None:
            s["unmeasurable"] += 1
        elif d < 8.0:
            s["in_pocket"] += 1
        elif d < 15.0:
            s["pocket_adj"] += 1
        else:
            s["off_site"] += 1
    for key, s in per_stratum.items():
        n_measurable = s["n"] - s["unmeasurable"]
        s["n_measurable"] = n_measurable
        if n_measurable > 0:
            s["frac_off_site"] = s["off_site"] / n_measurable
            s["frac_in_pocket"] = s["in_pocket"] / n_measurable
            ci_lo, ci_hi = wilson_ci(s["off_site"], n_measurable)
            s["off_site_ci_95"] = [ci_lo, ci_hi]

    # Pooled
    pooled_off = sum(s["off_site"] for s in per_stratum.values())
    pooled_meas = sum(s.get("n_measurable", 0) for s in per_stratum.values())
    pooled_frac = pooled_off / pooled_meas if pooled_meas else float("nan")
    pooled_ci = wilson_ci(pooled_off, pooled_meas)

    out = {
        "task": "G4_scoped_centroid_census",
        "generated_utc": ended.isoformat(),
        "wall_time_s": elapsed,
        "inputs": {
            "rows_csv": str(args.rows_csv),
            "refset_csv": str(args.refset_csv),
        },
        "seed": args.seed,
        "sampling_rule": {
            "strata": "backbone × ligand_role (12 strata)",
            "per_stratum_random": args.n_per_stratum,
            "per_stratum_enriched_matcher_failure": args.n_enriched_per_stratum,
            "enriched_criterion": "pocket_notes contains 'no_atom_match' or 'no_ref_ligand'",
        },
        "binning": {
            "in_pocket_A": "<8.0",
            "pocket_adjacent_A": "[8.0, 15.0)",
            "off_site_A": ">=15.0",
        },
        "per_stratum": dict(per_stratum),
        "pooled": {
            "n_measurable": pooled_meas,
            "n_off_site": pooled_off,
            "frac_off_site": pooled_frac,
            "off_site_ci_95_wilson": pooled_ci,
        },
    }
    args.out_json.write_text(json.dumps(out, indent=2, default=str))

    # CSV
    with args.out_csv.open("w") as f:
        w = csv.DictWriter(f, fieldnames=["input_path","backbone","role","arm","receptor","distance_A","note"])
        w.writeheader()
        for row in results:
            w.writerow(row)

    print(f"[G4] pooled off-site fraction: {pooled_frac:.4f} ({pooled_off}/{pooled_meas}) 95%CI [{pooled_ci[0]:.4f}, {pooled_ci[1]:.4f}]", file=sys.stderr)
    print(f"[G4] wall: {elapsed:.1f}s", file=sys.stderr)
    for stratum, s in sorted(per_stratum.items()):
        print(f"[G4]   {stratum:<25} n={s['n']:>3} in-pocket={s['in_pocket']:>3} adj={s['pocket_adj']:>3} off={s['off_site']:>3} unmeas={s['unmeasurable']:>3} off_frac={s.get('frac_off_site', float('nan')):.3f}", file=sys.stderr)


if __name__ == "__main__":
    main()
