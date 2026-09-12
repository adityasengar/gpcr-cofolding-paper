#!/usr/bin/env python3
"""Build HTML visualizations for the 10 sanity-check rows (5 good + 5 bad
dock cases from the G4 census).

Each HTML page shows:
 - Full receptor structure (cartoon).
 - The 12 BW pocket-anchor Cα atoms (spheres, one color).
 - The HETATM picked as "the ligand" (sticks, another color).
 - A red line from the pocket-anchor centroid to the ligand centroid.
 - The centroid distance annotated in a header.

The HTML is self-contained (3Dmol.js loaded from cdnjs). CIF content is
embedded as a JS string so no network fetch is needed at view time.

Also generates an INDEX.html linking to all 10.
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import gemmi
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SEL_CSV = Path("/tmp/g4_viz_selection.csv")
CIF_ROOT = Path("/tmp/g4_viz_cifs")
OUT_DIR = REPO / "artefacts" / "g4_viz_2026_09_10"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STD_AA = frozenset({
    "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE",
    "LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL","MSE",
})
NON_LIGAND = frozenset({
    "HOH","WAT","H2O","IOD","CA","MG","MN","ZN","NA","CL","K","F","CU",
    "FE","NI","CO","LI","GOL","EDO","PEG","MPD","SO4","PO4","NH2",
    "CLR","CHS","OLC","OLA","POV","POPC","POPE","NAG","BMA","MAN","FUC","BGC",
})
POCKET_BW = ("3.32","3.33","3.36","5.42","5.43","5.46","6.48","6.51","6.52","6.55","7.39","7.42")

# Load reference_set for anchor positions per receptor
def load_bw_maps():
    refset = REPO / "refs" / "reference_set.csv"
    per_rec = {}
    df = pd.read_csv(refset)
    for _, row in df.iterrows():
        slug = str(row.get("receptor_slug","")).strip().upper()
        if slug in per_rec: continue
        ap_str = str(row.get("anchor_positions","")).strip()
        if not ap_str or ap_str == "nan": continue
        try:
            ap = json.loads(ap_str)
            anchors = {str(k): int(v) for k, v in ap.items()}
            pocket = {}
            for bw in POCKET_BW:
                hel, off = bw.split(".")
                off = int(off)
                anchor_key = None; anchor_off = None
                for a_bw in anchors:
                    if a_bw.startswith(hel + "."):
                        anchor_key = a_bw
                        anchor_off = int(a_bw.split(".")[1])
                        break
                if anchor_key is None: continue
                pocket[bw] = anchors[anchor_key] + (off - anchor_off)
            per_rec[slug] = pocket
        except Exception:
            pass
    return per_rec


def resolve_cif_path(hpc_path: str) -> Path:
    """Turn HPC scratch path into local /tmp path."""
    return CIF_ROOT / hpc_path.replace("/hpc/scratch/sengaad1/", "")


def compute_scene(cif_path: Path, pocket_map: dict):
    """Return dict with pocket_ca positions, picked ligand atoms, centroids, and distance."""
    st = gemmi.read_structure(str(cif_path))
    # Find receptor chain
    receptor = None; receptor_len = 0
    for model in st:
        for chain in model:
            aa_count = sum(1 for r in chain if r.name in STD_AA)
            if aa_count >= 200 and aa_count > receptor_len:
                receptor = chain; receptor_len = aa_count
        break
    if receptor is None:
        return None

    # Pocket Cα atoms
    pocket_atoms = []
    for bw in POCKET_BW:
        pos = pocket_map.get(bw)
        if pos is None: continue
        for r in receptor:
            if r.seqid.num == pos:
                ca = r.find_atom("CA", "\0")
                if ca is not None:
                    pocket_atoms.append({
                        "bw": bw, "resi": pos, "resname": r.name,
                        "chain": receptor.name,
                        "x": ca.pos.x, "y": ca.pos.y, "z": ca.pos.z,
                    })
                break

    if len(pocket_atoms) < 6:
        return {"error": "insufficient_pocket_anchors", "pocket_atoms": pocket_atoms, "receptor_chain": receptor.name}

    pocket_centroid = {
        "x": sum(a["x"] for a in pocket_atoms) / len(pocket_atoms),
        "y": sum(a["y"] for a in pocket_atoms) / len(pocket_atoms),
        "z": sum(a["z"] for a in pocket_atoms) / len(pocket_atoms),
    }

    # Find picked ligand (largest HETATM ≥ 5 heavy atoms)
    all_hetatm_candidates = []
    for model in st:
        for chain in model:
            for r in chain:
                if r.name in NON_LIGAND or r.name in STD_AA: continue
                heavy = [a for a in r if a.element.name != "H"]
                if len(heavy) < 5: continue
                cx = sum(a.pos.x for a in heavy) / len(heavy)
                cy = sum(a.pos.y for a in heavy) / len(heavy)
                cz = sum(a.pos.z for a in heavy) / len(heavy)
                all_hetatm_candidates.append({
                    "resname": r.name, "chain": chain.name, "seqid": r.seqid.num,
                    "n_heavy": len(heavy), "centroid_x": cx, "centroid_y": cy, "centroid_z": cz,
                    "atoms": [{"name": a.name, "x": a.pos.x, "y": a.pos.y, "z": a.pos.z} for a in heavy],
                })
        break

    all_hetatm_candidates.sort(key=lambda c: c["n_heavy"], reverse=True)
    picked = all_hetatm_candidates[0] if all_hetatm_candidates else None

    if picked is None:
        return {
            "error": "no_ligand_hetatm", "pocket_atoms": pocket_atoms,
            "pocket_centroid": pocket_centroid, "receptor_chain": receptor.name,
            "all_hetatm_candidates": [],
        }

    dx = pocket_centroid["x"] - picked["centroid_x"]
    dy = pocket_centroid["y"] - picked["centroid_y"]
    dz = pocket_centroid["z"] - picked["centroid_z"]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)

    # Also enumerate all polymer chains for context
    chains_info = []
    for model in st:
        for chain in model:
            aa = sum(1 for r in chain if r.name in STD_AA)
            hetatm = sum(1 for r in chain if r.name not in NON_LIGAND and r.name not in STD_AA and len([a for a in r if a.element.name != "H"]) >= 5)
            chains_info.append({"name": chain.name, "n_aa": aa, "n_ligand_res": hetatm})
        break

    return {
        "pocket_atoms": pocket_atoms,
        "pocket_centroid": pocket_centroid,
        "picked_ligand": picked,
        "all_hetatm_candidates": all_hetatm_candidates,
        "distance_A": dist,
        "receptor_chain": receptor.name,
        "chains": chains_info,
    }


def build_html(row: dict, scene: dict, quality: str, cif_content: str) -> str:
    """Return the standalone HTML string."""
    receptor = row["receptor"]; backbone = row["backbone"]
    role = row["role"]; arm = row["arm"]
    dist = row["distance_A"]
    filename = row["input_path"].split("/")[-1]

    pocket_bws_str = "; ".join(
        f"BW {a['bw']} = {a['resname']}{a['resi']}" for a in scene.get("pocket_atoms", [])
    )
    pc = scene.get("pocket_centroid", {})
    picked = scene.get("picked_ligand")
    picked_str = f"{picked['resname']}/{picked['chain']}:{picked['seqid']} ({picked['n_heavy']} heavy atoms)" if picked else "(none)"
    all_candidates_str = "; ".join(
        f"{c['resname']}/{c['chain']}:{c['seqid']}(n={c['n_heavy']})"
        for c in scene.get("all_hetatm_candidates", [])[:10]
    )
    chains_str = "; ".join(
        f"{c['name']} (aa={c['n_aa']}, hetatm={c['n_ligand_res']})"
        for c in scene.get("chains", [])
    )

    quality_color = "#0a7f3f" if quality == "good" else "#c1272d"
    quality_label = "GOOD DOCK (in-pocket)" if quality == "good" else "BAD DOCK (off-site)"

    # Build a 3Dmol.js viewer script.
    # Highlight the receptor cartoon, the pocket Cα spheres (blue), and the picked ligand (yellow sticks + orange spheres).
    pocket_selector = "[" + ", ".join(f'{{"chain":"{a["chain"]}","resi":{a["resi"]},"atom":"CA"}}' for a in scene["pocket_atoms"]) + "]"
    picked_chain = picked["chain"] if picked else ""
    picked_resi = picked["seqid"] if picked else -1
    picked_resname = picked["resname"] if picked else ""

    return f"""<title>{receptor} · {backbone} · {role} · {arm} · d={dist:.2f}Å</title>
<style>
:root {{ --bg: #fafafa; --text: #222; --panel: #ffffff; --border: #d0d0d0; --accent: {quality_color}; }}
body {{ background: var(--bg); color: var(--text); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
h1 {{ font-size: 22px; margin: 0 0 4px 0; }}
h2 {{ font-size: 15px; color: #666; font-weight: normal; margin: 0 0 20px 0; }}
.badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; background: var(--accent); color: white; font-weight: 600; font-size: 13px; margin-right: 10px; }}
.viewer {{ width: 100%; height: 600px; border: 1px solid var(--border); background: white; position: relative; }}
.info {{ background: var(--panel); border: 1px solid var(--border); padding: 12px 16px; margin-top: 12px; border-radius: 4px; font-size: 13px; line-height: 1.5; }}
.info dt {{ font-weight: 600; color: #555; margin-top: 6px; }}
.info dd {{ margin: 2px 0 6px 12px; font-family: 'SF Mono', Consolas, monospace; font-size: 12px; }}
.legend {{ display: flex; gap: 20px; margin-top: 12px; font-size: 13px; }}
.legend-item {{ display: flex; align-items: center; gap: 6px; }}
.swatch {{ width: 14px; height: 14px; border-radius: 3px; display: inline-block; }}
</style>
<div class="container">
<h1><span class="badge">{quality_label}</span>{receptor} · {backbone} · {role} · {arm} arm</h1>
<h2>Centroid distance: <b>{dist:.2f} Å</b> · CIF: <code>{filename}</code></h2>

<div id="viewer" class="viewer"></div>

<div class="legend">
  <div class="legend-item"><span class="swatch" style="background:#a0a0a0"></span>Receptor cartoon</div>
  <div class="legend-item"><span class="swatch" style="background:#2266cc"></span>12 pocket-anchor Cα (spheres)</div>
  <div class="legend-item"><span class="swatch" style="background:#ffcc00"></span>Picked ligand (sticks)</div>
  <div class="legend-item"><span class="swatch" style="background:#f04040"></span>Centroid–centroid line ({dist:.2f} Å)</div>
</div>

<div class="info">
<dl>
<dt>Receptor chain</dt><dd>{scene.get("receptor_chain","?")}</dd>
<dt>Pocket-anchor Cα atoms found (n={len(scene.get("pocket_atoms",[]))} of 12 target BWs)</dt><dd>{pocket_bws_str}</dd>
<dt>Pocket centroid</dt><dd>({pc.get("x",0):.2f}, {pc.get("y",0):.2f}, {pc.get("z",0):.2f}) Å</dd>
<dt>All ligand-candidate HETATMs (large-first)</dt><dd>{all_candidates_str}</dd>
<dt>PICKED by scorer heuristic (largest heavy-atom count)</dt><dd>{picked_str}</dd>
<dt>All polymer chains in CIF</dt><dd>{chains_str}</dd>
</dl>
</div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js"></script>
<script>
const cif = {json.dumps(cif_content)};
const pocketSel = {pocket_selector};
const pickedChain = {json.dumps(picked_chain)};
const pickedResi = {picked_resi};
const pickedResname = {json.dumps(picked_resname)};
const pc = [{pc.get("x",0)}, {pc.get("y",0)}, {pc.get("z",0)}];
const lc = [{picked["centroid_x"] if picked else 0}, {picked["centroid_y"] if picked else 0}, {picked["centroid_z"] if picked else 0}];

const el = document.getElementById("viewer");
const viewer = $3Dmol.createViewer(el, {{ backgroundColor: 'white' }});
viewer.addModel(cif, 'cif');

// Receptor cartoon (gray)
viewer.setStyle({{}}, {{ cartoon: {{ color: '#a8a8a8' }} }});

// Pocket-anchor Cα as blue spheres — one per BW
pocketSel.forEach(sel => {{
    viewer.addStyle(sel, {{ sphere: {{ color: '#2266cc', radius: 1.5 }} }});
    // Label with BW position
    viewer.addLabel(sel.resi, {{ fontSize: 8, backgroundColor: '#2266cc', fontColor: 'white', showBackground: true }}, sel);
}});

// Picked ligand (yellow sticks)
if (pickedChain) {{
    viewer.setStyle({{ chain: pickedChain, resi: pickedResi }}, {{ stick: {{ color: '#ffcc00', radius: 0.3 }} }});
}}

// Pocket centroid (blue larger sphere at that xyz)
viewer.addSphere({{ center: {{x: pc[0], y: pc[1], z: pc[2]}}, radius: 1.2, color: '#4488ff', opacity: 0.6 }});

// Ligand centroid (yellow sphere at that xyz)
if (pickedChain) {{
    viewer.addSphere({{ center: {{x: lc[0], y: lc[1], z: lc[2]}}, radius: 1.2, color: '#ffcc00', opacity: 0.6 }});
    // Distance line
    viewer.addCylinder({{
        start: {{x: pc[0], y: pc[1], z: pc[2]}},
        end: {{x: lc[0], y: lc[1], z: lc[2]}},
        radius: 0.15, fromCap: 1, toCap: 1,
        color: '#f04040',
    }});
}}

viewer.zoomTo();
viewer.render();
</script>
"""


def build_index(records: list[dict]) -> str:
    rows = ""
    for r in records:
        color = "#0a7f3f" if r["quality"] == "good" else "#c1272d"
        rows += f"""<tr>
<td><a href="{r['filename']}">{r['receptor']}</a></td>
<td>{r['backbone']}</td>
<td>{r['role']}</td>
<td>{r['arm']}</td>
<td style="color:{color};font-weight:600">{r['distance_A']:.2f}</td>
<td>{r['quality']}</td>
<td>{r['picked_ligand']}</td>
</tr>
"""
    return f"""<title>G4 sanity check — 10 dock cases</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 24px; max-width: 1100px; margin: 0 auto; }}
h1 {{ font-size: 22px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th, td {{ border: 1px solid #d0d0d0; padding: 6px 10px; text-align: left; }}
th {{ background: #f0f0f0; }}
a {{ color: #0055aa; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; color: white; font-weight: 600; font-size: 11px; }}
.good {{ background: #0a7f3f; }} .bad {{ background: #c1272d; }}
.desc {{ background: #fafafa; border: 1px solid #d0d0d0; padding: 12px 16px; font-size: 13px; line-height: 1.5; margin: 20px 0; }}
</style>
<h1>G4 sanity check — 10 dock cases</h1>
<p style="color:#666">Ground-truth check on the scoped centroid census: does the measurement classify predictions the way a human would?</p>
<div class="desc">
<b>The metric</b>: distance between two centroids —
(1) the ligand's heavy-atom centroid (whichever HETATM has the most heavy atoms wins),
and (2) the pocket-anchor Cα centroid computed from 12 fixed BW positions (3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, 6.51, 6.52, 6.55, 7.39, 7.42).
Under 8 Å = in-pocket, ≥ 15 Å = off-site.
<br><br>
Each row below links to a standalone 3Dmol.js viewer showing the receptor cartoon, the 12 pocket Cα (blue spheres), the picked ligand (yellow sticks), and a red line between the two centroids. The 5 "good" cases have distance < 2 Å; the 5 "bad" cases have distance > 77 Å.
</div>
<table>
<thead><tr>
<th>receptor</th><th>backbone</th><th>role</th><th>arm</th><th>distance (Å)</th><th>quality</th><th>picked ligand</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
"""


def main():
    sel = pd.read_csv(SEL_CSV)
    bw_maps = load_bw_maps()

    records = []
    for _, row in sel.iterrows():
        r = row.to_dict()
        cif_path = resolve_cif_path(r["input_path"])
        if not cif_path.exists():
            print(f"MISSING CIF: {cif_path}", file=sys.stderr)
            continue
        rec = r["receptor"].upper()
        pocket_map = bw_maps.get(rec, {})
        scene = compute_scene(cif_path, pocket_map)
        if scene is None:
            print(f"scene failed: {cif_path}", file=sys.stderr)
            continue
        cif_content = cif_path.read_text()
        html = build_html(r, scene, r["quality"], cif_content)
        # Filename
        distance_str = f"{r['distance_A']:.1f}"
        filename = f"{r['quality']}_{r['distance_A']:07.2f}A_{rec}_{r['backbone']}_{r['role']}_{r['arm']}.html"
        (OUT_DIR / filename).write_text(html)
        picked = scene.get("picked_ligand")
        picked_str = f"{picked['resname']}/{picked['chain']}:{picked['seqid']}(n={picked['n_heavy']})" if picked else "(none)"
        records.append({
            "receptor": rec, "backbone": r["backbone"], "role": r["role"], "arm": r["arm"],
            "distance_A": r["distance_A"], "quality": r["quality"], "filename": filename,
            "picked_ligand": picked_str,
        })
        print(f"  wrote {filename}", file=sys.stderr)

    # Sort: good first (by distance asc), then bad (by distance desc)
    good = sorted([r for r in records if r["quality"] == "good"], key=lambda x: x["distance_A"])
    bad = sorted([r for r in records if r["quality"] == "bad"], key=lambda x: -x["distance_A"])
    (OUT_DIR / "INDEX.html").write_text(build_index(good + bad))
    print(f"\nWrote {len(records)} viewers + INDEX.html to {OUT_DIR}")


if __name__ == "__main__":
    main()
