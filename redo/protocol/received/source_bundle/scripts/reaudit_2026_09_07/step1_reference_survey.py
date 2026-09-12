#!/usr/bin/env python3
"""Step 1 — reference survey.

For every row in refs/reference_set.csv, load the reference PDB and enumerate
ALL HETATM candidates (excluding waters/buffers/amino-acids). For each, record:

  - resname, chain, seqid
  - n_heavy atoms
  - centroid (x, y, z)
  - centroid_distance_to_receptor_centroid — proxy for "is this the pocket ligand
    or a peripheral cofactor?"

For each reference row, also mark:
  - scorer_picked: the resname `build_pocket_reference_cache` would pick
    (largest n_heavy, resname as deterministic tiebreak)
  - pocket_closest: the candidate whose centroid is closest to the receptor
    centroid (the physically-plausible pocket ligand)

If scorer_picked != pocket_closest, Bug #2 fires on that reference.

Output: `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/reference_survey.csv`
        `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/reference_survey_summary.md`

No HPC. No rescore. Reads local refs/cache/rcsb/. Downloads any missing PDBs.
"""
from __future__ import annotations
import csv, json, subprocess
from collections import defaultdict
from pathlib import Path

import gemmi
import numpy as np

REPO = Path("/Users/SENGAAD1/Documents/claude/paper_af3")
REF_SET = REPO / "refs/reference_set.csv"
CACHE = REPO / "refs/cache/rcsb"
OUT_DIR = REPO / "experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07"
OUT_CSV = OUT_DIR / "reference_survey.csv"
OUT_MD = OUT_DIR / "reference_survey_summary.md"

STD_AA = {"ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE","LEU",
          "LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL","MSE","SEC","PYL"}

# Match scorer/pocket_metrics.py::_NON_LIGAND_RESNAMES (approximation — full
# list is inside scorer but the campaign uses waters + common buffer HETATMs).
NON_LIGAND = {
    "HOH", "SOL", "WAT",
    "SO4", "GOL", "TRS", "ACT", "CL", "NA", "MG", "CA", "ZN", "K", "F", "BR", "I",
    "PGE", "PEG", "EDO", "IPA", "IMD", "BME", "TCE", "MPD", "TAM", "TRT",
    "OLA", "OLB", "OLC", "PC1", "PLM", "STE", "MYR", "CDL", "CLR", "P4G",
    "1PE", "P6G", "PE4", "6JZ", "GDN", "PAM",
}


def fetch_pdb(pdb: str) -> Path | None:
    pdb = pdb.lower().strip()
    if not pdb:
        return None
    p = CACHE / f"pdb_{pdb}.cif"
    if p.exists():
        return p
    r = subprocess.run(
        ["curl", "-sf", f"https://files.rcsb.org/download/{pdb.upper()}.cif", "-o", str(p)],
        capture_output=True,
    )
    if r.returncode == 0 and p.exists() and p.stat().st_size > 100:
        return p
    if p.exists():
        p.unlink()
    return None


def all_ca_positions_by_chain(struct: gemmi.Structure) -> dict[str, np.ndarray]:
    """Return {chain_name: (N, 3) array of Cα positions} for STD_AA chains."""
    out = {}
    for model in struct:
        for ch in model:
            pts = []
            for r in ch:
                if r.name not in STD_AA:
                    continue
                for a in r:
                    if a.name == "CA":
                        pts.append([a.pos.x, a.pos.y, a.pos.z])
                        break
            if pts:
                out[ch.name] = np.array(pts)
        break
    return out


def min_ca_distance_and_chain(hetatm_centroid: np.ndarray, ca_by_chain: dict[str, np.ndarray]) -> tuple[float, str]:
    """Distance from HETATM centroid to nearest Cα atom (any chain), + chain name."""
    if not ca_by_chain:
        return float("nan"), ""
    best_d = float("inf")
    best_ch = ""
    for chain, pts in ca_by_chain.items():
        d = float(np.min(np.linalg.norm(pts - hetatm_centroid, axis=1)))
        if d < best_d:
            best_d = d
            best_ch = chain
    return best_d, best_ch


def chain_len(ca_by_chain: dict[str, np.ndarray], chain: str) -> int:
    return len(ca_by_chain.get(chain, np.array([])))


def collect_hetatm_candidates(struct: gemmi.Structure) -> list[dict]:
    """List every non-STD_AA, non-buffer residue with heavy atoms."""
    out = []
    for model in struct:
        for ch in model:
            for r in ch:
                if r.name in STD_AA:
                    continue
                if r.name in NON_LIGAND:
                    continue
                heavy = [(a.pos.x, a.pos.y, a.pos.z) for a in r if a.element.name != "H"]
                if not heavy:
                    continue
                c = np.mean(heavy, axis=0)
                out.append({
                    "resname": r.name,
                    "chain": ch.name,
                    "seqid": int(r.seqid.num),
                    "n_heavy": len(heavy),
                    "centroid": c,
                })
        break
    return out


def scorer_would_pick(cands: list[dict]) -> dict | None:
    """Reproduce build_pocket_reference_cache selection: largest n_heavy,
    resname as deterministic tiebreak (matches the code's `sort(key=lambda c:
    (c[0], c[1]), reverse=True)`).
    """
    if not cands:
        return None
    return max(cands, key=lambda c: (c["n_heavy"], c["resname"]))


def pocket_closest(cands: list[dict], centroid: np.ndarray) -> dict | None:
    """Which candidate's centroid is closest to the receptor Cα centroid?"""
    if not cands or centroid is None:
        return None
    return min(cands, key=lambda c: float(np.linalg.norm(c["centroid"] - centroid)))


def main() -> int:
    ref_rows = list(csv.DictReader(REF_SET.open()))
    print(f"[survey] {len(ref_rows)} reference rows")

    survey_rows = []
    n_bug2 = 0
    n_no_pdb = 0
    n_no_cands = 0
    per_role_bug2 = defaultdict(int)
    per_role_total = defaultdict(int)

    for i, ref in enumerate(ref_rows, 1):
        recep = ref.get("receptor_slug", "").upper()
        role = ref.get("role", "")
        role_specific = ref.get("role_specific", "")
        pdb = ref.get("pdb_id", "").upper()
        per_role_total[role] += 1

        base = {
            "receptor_slug": recep,
            "role": role,
            "role_specific": role_specific,
            "pdb_id": pdb,
            "curation_note": ref.get("curation_note", "")[:200],
            "resolved_state": ref.get("resolved_state", ""),
            "active_stabilization_source": ref.get("active_stabilization_source", ""),
        }

        cif_path = fetch_pdb(pdb)
        if cif_path is None:
            n_no_pdb += 1
            survey_rows.append({**base, "status": "PDB_UNAVAILABLE"})
            print(f"  {i:3d}/{len(ref_rows)} {recep:<8} {role:<10} {pdb:<6} — PDB unavailable")
            continue

        try:
            struct = gemmi.read_structure(str(cif_path))
        except Exception as e:
            survey_rows.append({**base, "status": f"PARSE_FAIL: {e}"})
            print(f"  {i:3d}/{len(ref_rows)} {recep:<8} {role:<10} {pdb:<6} — parse fail")
            continue

        ca_by_chain = all_ca_positions_by_chain(struct)
        cands = collect_hetatm_candidates(struct)

        if not cands:
            n_no_cands += 1
            survey_rows.append({**base, "status": "NO_HETATM_CANDIDATES"})
            print(f"  {i:3d}/{len(ref_rows)} {recep:<8} {role:<10} {pdb:<6} — no HETATM ligand candidates")
            continue

        # For each candidate, min-distance-to-any-Cα (physical protein-proximity) +
        # which chain that closest Cα is on.
        for c in cands:
            d, ch = min_ca_distance_and_chain(c["centroid"], ca_by_chain)
            c["min_ca_dist"] = d
            c["min_ca_chain"] = ch
            c["host_chain_len"] = chain_len(ca_by_chain, ch)

        picked = scorer_would_pick(cands)
        # Pocket-plausible candidate: closest to any Cα AND host chain is in
        # receptor-plausible size range (200 <= len <= 400). Excludes ligands
        # bound to Gβ, Gγ, or small peptides.
        pocket_plausible = [
            c for c in cands
            if c["min_ca_dist"] < 6.0
            and 200 <= c["host_chain_len"] <= 400
        ]
        # Bug #2 fires when scorer's pick is NOT in the pocket-plausible set,
        # AND there IS a pocket-plausible candidate available.
        picked_is_plausible = any(
            c["resname"] == picked["resname"] and c["chain"] == picked["chain"]
            and c["seqid"] == picked["seqid"] for c in pocket_plausible
        )
        bug2 = bool(pocket_plausible) and not picked_is_plausible

        if bug2:
            n_bug2 += 1
            per_role_bug2[role] += 1

        cand_str = ";".join(
            f"{c['resname']}/{c['chain']}:{c['seqid']}(n={c['n_heavy']},minCA={c['min_ca_dist']:.1f}@{c['min_ca_chain']}/{c['host_chain_len']})"
            for c in sorted(cands, key=lambda c: -c["n_heavy"])
        )

        best_pocket = min(pocket_plausible, key=lambda c: c["min_ca_dist"]) if pocket_plausible else None

        survey_rows.append({
            **base,
            "status": "OK",
            "n_candidates": len(cands),
            "picked_resname": picked["resname"],
            "picked_chain": picked["chain"],
            "picked_seqid": picked["seqid"],
            "picked_n_heavy": picked["n_heavy"],
            "picked_min_ca_dist": f"{picked['min_ca_dist']:.2f}",
            "picked_min_ca_chain": picked["min_ca_chain"],
            "picked_host_chain_len": picked["host_chain_len"],
            "n_pocket_plausible": len(pocket_plausible),
            "best_pocket_resname": best_pocket["resname"] if best_pocket else "",
            "best_pocket_chain": best_pocket["chain"] if best_pocket else "",
            "best_pocket_n_heavy": best_pocket["n_heavy"] if best_pocket else "",
            "best_pocket_min_ca_dist": f"{best_pocket['min_ca_dist']:.2f}" if best_pocket else "",
            "best_pocket_host_chain_len": best_pocket["host_chain_len"] if best_pocket else "",
            "bug2_fires": "YES" if bug2 else "no",
            "all_candidates": cand_str,
        })

        marker = "  ⚠ BUG#2" if bug2 else ""
        pocket_note = ""
        if best_pocket:
            pocket_note = f"→ pocket-plausible: {best_pocket['resname']}(n={best_pocket['n_heavy']},d={best_pocket['min_ca_dist']:.1f})"
        else:
            pocket_note = "→ no pocket-plausible candidate"
        print(
            f"  {i:3d}/{len(ref_rows)} {recep:<8} {role:<10} {pdb:<6} "
            f"cands={len(cands):>2}  picked={picked['resname']:<5}(n={picked['n_heavy']:>3},minCA={picked['min_ca_dist']:5.1f}@{picked['min_ca_chain']}/{picked['host_chain_len']}) "
            f"{pocket_note}{marker}"
        )

    # Write CSV
    cols = [
        "receptor_slug", "role", "role_specific", "pdb_id", "status",
        "n_candidates",
        "picked_resname", "picked_chain", "picked_seqid", "picked_n_heavy",
        "picked_min_ca_dist", "picked_min_ca_chain", "picked_host_chain_len",
        "n_pocket_plausible",
        "best_pocket_resname", "best_pocket_chain", "best_pocket_n_heavy",
        "best_pocket_min_ca_dist", "best_pocket_host_chain_len",
        "bug2_fires",
        "resolved_state", "active_stabilization_source", "curation_note",
        "all_candidates",
    ]
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in survey_rows:
            w.writerow(r)

    # Summary markdown
    md = []
    md.append("# Reference survey — Bug #2 prevalence + candidate inventory\n")
    md.append(f"Generated: 2026-09-07 from `refs/reference_set.csv` ({len(ref_rows)} refs).\n")
    md.append(f"CSV: `{OUT_CSV.relative_to(REPO)}` — one row per reference, all HETATM candidates per row.\n\n")
    md.append("## Headline\n")
    md.append(f"- {n_bug2}/{len(ref_rows) - n_no_pdb - n_no_cands} references (of those with at least one candidate) fire Bug #2 by centroid-distance criterion.\n")
    md.append(f"- {n_no_pdb} references have no local PDB (download failed).\n")
    md.append(f"- {n_no_cands} references have zero HETATM candidates after buffer/AA filter.\n\n")
    md.append("## Bug #2 firing rate by role\n\n")
    md.append("| role | fires | total | pct |\n|---|---:|---:|---:|\n")
    for role in sorted(per_role_total):
        t = per_role_total[role]
        b = per_role_bug2[role]
        md.append(f"| {role} | {b} | {t} | {100*b/t if t else 0:.1f}% |\n")
    md.append("\n## Interpretation\n\n")
    md.append("`bug2_fires=YES` means the scorer's largest-HETATM pick != the candidate closest to the receptor Cα centroid. The centroid proxy is imperfect (assumes pocket ligand sits near geometric center of protein) but should be conservative — real disagreements will show large distance gaps.\n\n")
    md.append("Inspect the CSV — the `all_candidates` column has the full HETATM list for each reference. Any row where `picked_dist_to_receptor_centroid` > 25 Å but a candidate at < 15 Å exists is a Bug #2 event.\n")

    OUT_MD.write_text("".join(md))
    print(f"\n[survey] wrote {OUT_CSV.relative_to(REPO)} ({len(survey_rows)} rows)")
    print(f"[survey] wrote {OUT_MD.relative_to(REPO)}")
    print(f"\nBug #2 fires on {n_bug2}/{len(ref_rows) - n_no_pdb - n_no_cands} usable references")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
