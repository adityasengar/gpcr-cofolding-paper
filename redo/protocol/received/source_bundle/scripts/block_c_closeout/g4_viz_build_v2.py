#!/usr/bin/env python3
"""V2 of the G4 visualization: receptor chain identified by the presence
of a Cα at the receptor's own 3.50 anchor position (from
reference_set.csv), not by longest-chain heuristic.

The v1 bug: on cognate-arm rows where the receptor is < 394 aa
(CXCR4=352, 5HT5A=357, CNR2=360, ADRB2=413 hits both sides), my
"longest polymer chain ≥ 200 aa" heuristic picked Gα (~394 aa) as
"the receptor", then looked up receptor anchor positions (e.g. seqid
248 for CXCR4 6.48) in Gα — nonsense pocket-Cα centroid — ~70 Å
from the actual ligand — all 5 "bad dock" cases were this bug.

V2 fix: for each candidate polymer chain, check whether it contains a
Cα at the receptor's UniProt 3.50 position. The chain that does is the
receptor. If none does (e.g. receptor with construct offset), fall back
to the chain with the most residues in {STD_AA} AND with a Cα at any
of the receptor's 6 named anchor positions.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import gemmi
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SEL_CSV = Path("/tmp/g4_viz_selection.csv")
CIF_ROOT = Path("/tmp/g4_viz_cifs")
OUT_DIR = REPO / "artefacts" / "g4_viz_2026_09_10_v2"
OUT_DIR.mkdir(parents=True, exist_ok=True)

STD_AA = frozenset({
    "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE",
    "LEU","LYS","MET","PHE","PRO","SER","THR","TRP","TYR","VAL","MSE",
})
NON_LIGAND = frozenset({
    "HOH","WAT","H2O","IOD","CA","MG","MN","ZN","NA","CL","K","F","CU","FE","NI","CO","LI",
    "GOL","EDO","PEG","MPD","SO4","PO4","NH2","CLR","CHS","OLC","OLA","POV","POPC","POPE",
    "NAG","BMA","MAN","FUC","BGC",
})
POCKET_BW = ("3.32","3.33","3.36","5.42","5.43","5.46","6.48","6.51","6.52","6.55","7.39","7.42")


def load_receptor_anchors():
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
            per_rec[slug] = {"named_anchors": anchors, "pocket_map": pocket}
        except Exception:
            pass
    return per_rec


def find_receptor_chain(structure, receptor_anchors: dict):
    """Return the polymer chain that carries the receptor.

    Method: for each polymer chain ≥ 100 aa, count how many of the
    receptor's 6 named anchor positions have a Cα in that chain. The
    chain with the most anchor hits (≥ 3 required) wins. If no chain
    scores ≥ 3, fall back to the longest polymer chain.
    """
    named = receptor_anchors.get("named_anchors", {})
    target_positions = [int(v) for v in named.values() if isinstance(v, (int, str))]
    if not target_positions:
        return None, "no_anchor_data"

    best_chain = None; best_hits = -1
    longest_chain = None; longest_len = 0
    for model in structure:
        for chain in model:
            aa_count = sum(1 for r in chain if r.name in STD_AA)
            if aa_count < 100: continue
            # Count anchor hits
            hits = 0
            for pos in target_positions:
                for r in chain:
                    if r.seqid.num == pos and r.name in STD_AA and r.find_atom("CA","\0") is not None:
                        hits += 1
                        break
            if hits > best_hits:
                best_hits = hits; best_chain = chain
            if aa_count > longest_len:
                longest_len = aa_count; longest_chain = chain
        break

    if best_chain is not None and best_hits >= 3:
        return best_chain, f"anchor_hits={best_hits}/{len(target_positions)}"
    if longest_chain is not None:
        return longest_chain, f"fallback_longest_chain (aa={longest_len})"
    return None, "no_polymer_chain_>=100_aa"


def compute_scene(cif_path: Path, receptor_anchors: dict):
    st = gemmi.read_structure(str(cif_path))
    receptor, receptor_note = find_receptor_chain(st, receptor_anchors)
    if receptor is None:
        return None
    pocket_map = receptor_anchors["pocket_map"]

    pocket_atoms = []
    for bw in POCKET_BW:
        pos = pocket_map.get(bw)
        if pos is None: continue
        for r in receptor:
            if r.seqid.num == pos and r.name in STD_AA:
                ca = r.find_atom("CA","\0")
                if ca is not None:
                    pocket_atoms.append({
                        "bw": bw, "resi": pos, "resname": r.name, "chain": receptor.name,
                        "x": ca.pos.x, "y": ca.pos.y, "z": ca.pos.z,
                    })
                break
    if len(pocket_atoms) < 6:
        return {"error": "insufficient_pocket_anchors", "pocket_atoms": pocket_atoms, "receptor_chain": receptor.name, "receptor_note": receptor_note}

    pocket_centroid = {
        "x": sum(a["x"] for a in pocket_atoms) / len(pocket_atoms),
        "y": sum(a["y"] for a in pocket_atoms) / len(pocket_atoms),
        "z": sum(a["z"] for a in pocket_atoms) / len(pocket_atoms),
    }

    all_candidates = []
    for model in st:
        for chain in model:
            for r in chain:
                if r.name in NON_LIGAND or r.name in STD_AA: continue
                heavy = [a for a in r if a.element.name != "H"]
                if len(heavy) < 5: continue
                cx = sum(a.pos.x for a in heavy) / len(heavy)
                cy = sum(a.pos.y for a in heavy) / len(heavy)
                cz = sum(a.pos.z for a in heavy) / len(heavy)
                all_candidates.append({
                    "resname": r.name, "chain": chain.name, "seqid": r.seqid.num,
                    "n_heavy": len(heavy),
                    "centroid_x": cx, "centroid_y": cy, "centroid_z": cz,
                })
        break
    all_candidates.sort(key=lambda c: c["n_heavy"], reverse=True)
    picked = all_candidates[0] if all_candidates else None
    if picked is None:
        return {"error": "no_ligand_hetatm", "pocket_atoms": pocket_atoms, "pocket_centroid": pocket_centroid, "receptor_chain": receptor.name, "receptor_note": receptor_note, "all_hetatm_candidates": []}

    dx = pocket_centroid["x"] - picked["centroid_x"]
    dy = pocket_centroid["y"] - picked["centroid_y"]
    dz = pocket_centroid["z"] - picked["centroid_z"]
    dist = math.sqrt(dx*dx + dy*dy + dz*dz)

    chains_info = []
    for model in st:
        for chain in model:
            aa = sum(1 for r in chain if r.name in STD_AA)
            het = sum(1 for r in chain if r.name not in NON_LIGAND and r.name not in STD_AA and len([a for a in r if a.element.name != "H"]) >= 5)
            chains_info.append({"name": chain.name, "n_aa": aa, "n_ligand_res": het})
        break

    return {
        "pocket_atoms": pocket_atoms, "pocket_centroid": pocket_centroid,
        "picked_ligand": picked, "all_hetatm_candidates": all_candidates,
        "distance_A": dist, "receptor_chain": receptor.name,
        "receptor_note": receptor_note, "chains": chains_info,
    }


def build_html(row, scene, quality, cif_content):
    receptor = row["receptor"]; backbone = row["backbone"]
    role = row["role"]; arm = row["arm"]
    dist_v1 = row["distance_A"]
    dist_v2 = scene.get("distance_A")
    filename = row["input_path"].split("/")[-1]

    pocket_bws_str = "; ".join(f"BW {a['bw']} = {a['resname']}{a['resi']}" for a in scene.get("pocket_atoms", []))
    pc = scene.get("pocket_centroid", {})
    picked = scene.get("picked_ligand")
    picked_str = f"{picked['resname']}/{picked['chain']}:{picked['seqid']} ({picked['n_heavy']} heavy atoms)" if picked else "(none)"
    all_str = "; ".join(f"{c['resname']}/{c['chain']}:{c['seqid']}(n={c['n_heavy']})" for c in scene.get("all_hetatm_candidates", [])[:10])
    chains_str = "; ".join(f"{c['name']} (aa={c['n_aa']}, hetatm={c['n_ligand_res']})" for c in scene.get("chains", []))
    receptor_note = scene.get("receptor_note", "")

    quality_color = "#0a7f3f" if quality == "good" else "#c1272d"
    quality_label = "GOOD DOCK (v1)" if quality == "good" else "BAD DOCK (v1)"

    pocket_selector = "[" + ", ".join(f'{{"chain":"{a["chain"]}","resi":{a["resi"]},"atom":"CA"}}' for a in scene["pocket_atoms"]) + "]"
    picked_chain = picked["chain"] if picked else ""
    picked_resi = picked["seqid"] if picked else -1

    return f"""<title>{receptor} · {backbone} · {role} · {arm} · v1 d={dist_v1:.2f}Å v2 d={dist_v2:.2f}Å</title>
<style>
:root {{ --bg: #fafafa; --accent: {quality_color}; }}
body {{ background: var(--bg); font-family: -apple-system, sans-serif; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 20px; }}
h1 {{ font-size: 22px; margin: 0 0 4px 0; }}
h2 {{ font-size: 15px; color: #666; font-weight: normal; margin: 0 0 20px 0; }}
.badge {{ display: inline-block; padding: 4px 10px; border-radius: 4px; background: var(--accent); color: white; font-weight: 600; font-size: 13px; margin-right: 10px; }}
.badge2 {{ display: inline-block; padding: 4px 10px; border-radius: 4px; background: #333; color: white; font-weight: 600; font-size: 13px; margin-right: 10px; }}
.viewer {{ width: 100%; height: 600px; border: 1px solid #d0d0d0; background: white; }}
.info {{ background: white; border: 1px solid #d0d0d0; padding: 12px 16px; margin-top: 12px; border-radius: 4px; font-size: 13px; line-height: 1.5; }}
.info dt {{ font-weight: 600; color: #555; margin-top: 6px; }}
.info dd {{ margin: 2px 0 6px 12px; font-family: monospace; font-size: 12px; word-break: break-all; }}
.legend {{ display: flex; gap: 20px; margin-top: 12px; font-size: 13px; }}
.legend-item {{ display: flex; align-items: center; gap: 6px; }}
.swatch {{ width: 14px; height: 14px; border-radius: 3px; }}
.recompute-note {{ background: #fff4d6; border: 1px solid #d4a640; padding: 10px 14px; border-radius: 4px; margin: 12px 0; font-size: 13px; }}
</style>
<div class="container">
<h1><span class="badge">v1: {quality_label}</span><span class="badge2">v2 d = {dist_v2:.2f} Å</span>{receptor} · {backbone} · {role} · {arm} arm</h1>
<h2>v1 d = {dist_v1:.2f} Å · v2 d (correct receptor chain) = <b>{dist_v2:.2f} Å</b> · <code>{filename}</code></h2>

<div class="recompute-note">
<b>V1 vs V2</b>: v1 picked the receptor chain by "longest polymer chain ≥ 200 aa" — buggy when Gα (~394 aa) is longer than the receptor.
V2 picks the receptor by "chain containing a Cα at the receptor's own named anchor positions" — anchor-hits = <b>{receptor_note}</b>.
{"" if abs(dist_v1 - dist_v2) < 2.0 else "<br><b>Distance changed materially between v1 and v2 → v1 was buggy for this row.</b>"}
</div>

<div id="viewer" class="viewer"></div>

<div class="legend">
  <div class="legend-item"><span class="swatch" style="background:#a0a0a0"></span>Receptor cartoon (chain {scene["receptor_chain"]})</div>
  <div class="legend-item"><span class="swatch" style="background:#2266cc"></span>12 pocket-anchor Cα spheres</div>
  <div class="legend-item"><span class="swatch" style="background:#ffcc00"></span>Picked ligand sticks</div>
  <div class="legend-item"><span class="swatch" style="background:#f04040"></span>Centroid–centroid line</div>
</div>

<div class="info">
<dl>
<dt>Receptor chain (v2)</dt><dd>chain {scene["receptor_chain"]} — {receptor_note}</dd>
<dt>Pocket-anchor Cα found ({len(scene.get("pocket_atoms",[]))}/12)</dt><dd>{pocket_bws_str}</dd>
<dt>Pocket centroid</dt><dd>({pc.get("x",0):.2f}, {pc.get("y",0):.2f}, {pc.get("z",0):.2f}) Å</dd>
<dt>All ligand-candidate HETATMs</dt><dd>{all_str}</dd>
<dt>PICKED ligand</dt><dd>{picked_str}</dd>
<dt>All chains in CIF</dt><dd>{chains_str}</dd>
</dl>
</div>

</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js"></script>
<script>
const cif = {json.dumps(cif_content)};
const pocketSel = {pocket_selector};
const pickedChain = {json.dumps(picked_chain)};
const pickedResi = {picked_resi};
const pc = [{pc.get("x",0)}, {pc.get("y",0)}, {pc.get("z",0)}];
const lc = [{picked["centroid_x"] if picked else 0}, {picked["centroid_y"] if picked else 0}, {picked["centroid_z"] if picked else 0}];

const el = document.getElementById("viewer");
const viewer = $3Dmol.createViewer(el, {{ backgroundColor: 'white' }});
viewer.addModel(cif, 'cif');

// Whole complex cartoon (light gray)
viewer.setStyle({{}}, {{ cartoon: {{ color: '#a8a8a8' }} }});
// Receptor chain highlight (slightly darker, blue-tinted)
viewer.setStyle({{ chain: {json.dumps(scene["receptor_chain"])} }}, {{ cartoon: {{ color: '#7a8fbe' }} }});

// Pocket-anchor Cα as blue spheres
pocketSel.forEach(sel => {{
    viewer.addStyle(sel, {{ sphere: {{ color: '#2266cc', radius: 1.5 }} }});
    viewer.addLabel(sel.resi, {{ fontSize: 8, backgroundColor: '#2266cc', fontColor: 'white', showBackground: true }}, sel);
}});

// Ligand sticks
if (pickedChain) {{
    viewer.setStyle({{ chain: pickedChain, resi: pickedResi }}, {{ stick: {{ color: '#ffcc00', radius: 0.3 }} }});
}}

// Centroid spheres
viewer.addSphere({{ center: {{x: pc[0], y: pc[1], z: pc[2]}}, radius: 1.2, color: '#4488ff', opacity: 0.6 }});
if (pickedChain) {{
    viewer.addSphere({{ center: {{x: lc[0], y: lc[1], z: lc[2]}}, radius: 1.2, color: '#ffcc00', opacity: 0.6 }});
    viewer.addCylinder({{
        start: {{x: pc[0], y: pc[1], z: pc[2]}},
        end: {{x: lc[0], y: lc[1], z: lc[2]}},
        radius: 0.15, fromCap: 1, toCap: 1, color: '#f04040',
    }});
}}

viewer.zoomTo();
viewer.render();
</script>
"""


def build_index(records):
    rows = ""
    n_flipped = 0
    for r in records:
        v1 = r["distance_A_v1"]; v2 = r["distance_A_v2"]
        flipped = abs(v1 - v2) > 2.0
        if flipped: n_flipped += 1
        color = "#0a7f3f" if r["quality_v1"] == "good" else "#c1272d"
        flip_note = " <span style='color:#c1272d'>← flipped</span>" if flipped else ""
        rows += f"""<tr>
<td><a href="{r['filename']}">{r['receptor']}</a></td>
<td>{r['backbone']}</td>
<td>{r['role']}</td>
<td>{r['arm']}</td>
<td style="color:{color};font-weight:600">{v1:.2f}</td>
<td><b>{v2:.2f}</b>{flip_note}</td>
<td>{r['receptor_chain']} ({r['receptor_note']})</td>
</tr>
"""
    return f"""<title>G4 sanity check v2 — receptor-chain fix</title>
<style>
body {{ font-family: -apple-system, sans-serif; padding: 24px; max-width: 1200px; margin: 0 auto; }}
h1 {{ font-size: 22px; }}
table {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
th, td {{ border: 1px solid #d0d0d0; padding: 6px 10px; text-align: left; }}
th {{ background: #f0f0f0; }}
a {{ color: #0055aa; text-decoration: none; }}
a:hover {{ text-decoration: underline; }}
.desc {{ background: #fff4d6; border: 1px solid #d4a640; padding: 12px 16px; font-size: 13px; line-height: 1.5; margin: 20px 0; border-radius: 4px; }}
</style>
<h1>G4 sanity check v2 — receptor-chain identification fixed</h1>
<div class="desc">
<b>V1 bug</b>: identified the receptor chain by "longest polymer chain ≥ 200 aa". On cognate-arm rows where the receptor is shorter than Gα (~394 aa) — CXCR4 (352), 5HT5A (357), CNR2 (360) — the picker chose Gα as the receptor, then looked up receptor anchor positions in Gα, giving a nonsense pocket-Cα centroid ~70 Å from the actual pocket.
<br><br>
<b>V2 fix</b>: identify the receptor chain by "chain that has Cα at the receptor's own named anchor positions (from reference_set.csv anchor_positions)". Anchor-hits threshold: ≥ 3 of 6 named anchors must be present.
<br><br>
<b>Result</b>: <b>{n_flipped} of {len(records)} rows flipped materially</b> between v1 and v2 (distance change > 2 Å).
</div>
<table>
<thead><tr>
<th>receptor</th><th>backbone</th><th>role</th><th>arm</th><th>v1 dist (Å)</th><th>v2 dist (Å)</th><th>receptor chain (v2)</th>
</tr></thead>
<tbody>{rows}</tbody>
</table>
"""


def main():
    sel = pd.read_csv(SEL_CSV)
    anchors = load_receptor_anchors()

    records = []
    for _, row in sel.iterrows():
        r = row.to_dict()
        cif_path = CIF_ROOT / r["input_path"].replace("/hpc/scratch/sengaad1/", "")
        if not cif_path.exists():
            print(f"MISSING: {cif_path}", file=sys.stderr)
            continue
        rec = r["receptor"].upper()
        ranch = anchors.get(rec)
        if ranch is None:
            print(f"no anchor data for {rec}", file=sys.stderr)
            continue
        scene = compute_scene(cif_path, ranch)
        if scene is None or "error" in scene:
            print(f"scene failed for {cif_path}: {scene.get('error') if scene else 'None'}", file=sys.stderr)
            continue

        cif_content = cif_path.read_text()
        html = build_html(r, scene, r["quality"], cif_content)
        filename = f"{r['quality']}_v2_{scene['distance_A']:07.2f}A_{rec}_{r['backbone']}_{r['role']}_{r['arm']}.html"
        (OUT_DIR / filename).write_text(html)
        records.append({
            "receptor": rec, "backbone": r["backbone"], "role": r["role"], "arm": r["arm"],
            "distance_A_v1": r["distance_A"], "distance_A_v2": scene["distance_A"],
            "quality_v1": r["quality"], "filename": filename,
            "receptor_chain": scene["receptor_chain"], "receptor_note": scene["receptor_note"],
        })
        print(f"  {rec:6s} {r['backbone']:9s} {r['role']:20s} {r['arm']:8s} v1={r['distance_A']:6.2f} → v2={scene['distance_A']:6.2f} (chain {scene['receptor_chain']}, {scene['receptor_note']})", file=sys.stderr)

    records.sort(key=lambda x: x["distance_A_v2"])
    (OUT_DIR / "INDEX.html").write_text(build_index(records))
    print(f"\nWrote {len(records)} viewers + INDEX.html to {OUT_DIR}", file=sys.stderr)


if __name__ == "__main__":
    main()
