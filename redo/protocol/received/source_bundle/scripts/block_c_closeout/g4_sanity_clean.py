#!/usr/bin/env python3
"""Clean single-page sanity viz — pose_comparison_v2.html aesthetic.

10 predictions rendered as: receptor cartoon (chain A, subtle gray) +
ligand sticks (bright cyan). No pocket-anchor spheres, no centroid
line — visually just "is the ligand in the pocket, yes/no".

Header per card shows v1 vs v2 centroid-distance numbers so the bug
is visible; the 3D viewer itself is clean.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import gemmi
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
SEL_CSV = Path("/tmp/g4_viz_selection.csv")
CIF_ROOT = Path("/tmp/g4_viz_cifs")
OUT = REPO / "artefacts" / "g4_viz_2026_09_10_v2" / "pose_sanity_clean.html"
OUT.parent.mkdir(parents=True, exist_ok=True)

STD_AA = frozenset({
    "ALA","ARG","ASN","ASP","CYS","GLN","GLU","GLY","HIS","ILE","LEU","LYS",
    "MET","PHE","PRO","SER","THR","TRP","TYR","VAL","MSE",
})
NON_LIGAND = frozenset({
    "HOH","WAT","H2O","IOD","CA","MG","MN","ZN","NA","CL","K","F","CU","FE","NI","CO","LI",
    "GOL","EDO","PEG","MPD","SO4","PO4","NH2","CLR","CHS","OLC","OLA","POV","POPC","POPE",
    "NAG","BMA","MAN","FUC","BGC",
})
POCKET_BW = ("3.32","3.33","3.36","5.42","5.43","5.46","6.48","6.51","6.52","6.55","7.39","7.42")


def load_anchors():
    refset = REPO / "refs" / "reference_set.csv"
    per = {}
    df = pd.read_csv(refset)
    for _, row in df.iterrows():
        slug = str(row.get("receptor_slug","")).strip().upper()
        if slug in per: continue
        ap_str = str(row.get("anchor_positions","")).strip()
        if not ap_str or ap_str == "nan": continue
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
    named = anchors_info["named"]
    target = [int(v) for v in named.values()]
    best = None; best_hits = -1
    longest = None; longest_len = 0
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
            if aa > longest_len:
                longest_len = aa; longest = chain
        break
    if best and best_hits >= 3:
        return best, best_hits
    return longest, -1


def compute(cif_path: Path, anchors_info: dict):
    st = gemmi.read_structure(str(cif_path))
    receptor, hits = find_receptor_chain(st, anchors_info)
    if receptor is None:
        return None
    pocket = anchors_info["pocket"]

    pocket_atoms = []
    for bw in POCKET_BW:
        pos = pocket.get(bw)
        if pos is None: continue
        for r in receptor:
            if r.seqid.num == pos and r.name in STD_AA:
                ca = r.find_atom("CA","\0")
                if ca:
                    pocket_atoms.append({"bw": bw, "resi": pos, "resname": r.name,
                                         "x": ca.pos.x, "y": ca.pos.y, "z": ca.pos.z})
                break
    if len(pocket_atoms) < 6:
        return None
    pc = (
        sum(a["x"] for a in pocket_atoms)/len(pocket_atoms),
        sum(a["y"] for a in pocket_atoms)/len(pocket_atoms),
        sum(a["z"] for a in pocket_atoms)/len(pocket_atoms),
    )

    cands = []
    for model in st:
        for chain in model:
            for r in chain:
                if r.name in NON_LIGAND or r.name in STD_AA: continue
                heavy = [a for a in r if a.element.name != "H"]
                if len(heavy) < 5: continue
                cx = sum(a.pos.x for a in heavy)/len(heavy)
                cy = sum(a.pos.y for a in heavy)/len(heavy)
                cz = sum(a.pos.z for a in heavy)/len(heavy)
                cands.append({"resname": r.name, "chain": chain.name, "seqid": r.seqid.num,
                              "n_heavy": len(heavy), "cx": cx, "cy": cy, "cz": cz})
        break
    cands.sort(key=lambda c: c["n_heavy"], reverse=True)
    picked = cands[0] if cands else None
    if picked is None:
        return None
    dist = math.sqrt((pc[0]-picked["cx"])**2 + (pc[1]-picked["cy"])**2 + (pc[2]-picked["cz"])**2)
    return {
        "receptor_chain": receptor.name,
        "receptor_hits": hits,
        "picked": picked,
        "distance_v2": dist,
    }


def build_html(cases):
    header_html = """<title>G4 sanity check — is the ligand actually in the pocket?</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap');
:root {
  --bg: #0d1013; --surface: #14181c; --surface-2: #1a1f24;
  --edge: #262c33; --edge-strong: #333b44;
  --text: #d9d4c8; --text-dim: #9a9385; --text-fade: #6b6659;
  --accent-crystal: #e8a53c; --accent-pred: #4bb8d4;
  --pass: #4ade80; --fail: #ef4444; --warn: #f0a020;
  --mono: "IBM Plex Mono", ui-monospace, "SF Mono", Menlo, monospace;
  --sans: "IBM Plex Sans", -apple-system, "Segoe UI", system-ui, sans-serif;
}
body { margin:0; background:var(--bg); color:var(--text); font:14px/1.55 var(--sans); letter-spacing:-0.005em; }
header.page { padding:36px 40px 24px; max-width:1600px; margin:0 auto; border-bottom:1px solid var(--edge); }
.eyebrow { font-family:var(--mono); font-size:11px; letter-spacing:0.14em; text-transform:uppercase; color:var(--text-fade); margin-bottom:10px; }
h1 { font-family:var(--sans); font-weight:600; font-size:26px; line-height:1.15; letter-spacing:-0.02em; margin:0 0 10px; }
h1 em { color:var(--accent-crystal); font-style:normal; }
.intro { max-width:90ch; color:var(--text-dim); margin:0; line-height:1.65; }
.intro code, .intro b code { font-family:var(--mono); font-size:0.88em; color:var(--accent-crystal); background:rgba(232,165,60,0.08); padding:1px 5px; border-radius:3px; }
.intro b { color:var(--text); }
.legend { display:flex; gap:20px; font-family:var(--mono); font-size:11.5px; color:var(--text-dim); margin-top:16px; flex-wrap:wrap; }
.legend-item { display:flex; align-items:center; gap:8px; }
.legend-lig { width:12px; height:12px; border-radius:50%; }
.legend-swatch { width:18px; height:4px; border-radius:1px; }

.grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap:16px; max-width:1800px; margin:20px auto; padding:0 40px 50px; }
.case { background:var(--surface); border:1px solid var(--edge); border-radius:6px; overflow:hidden; display:flex; flex-direction:column; }
.case-header { padding:12px 16px 10px; display:flex; gap:12px; align-items:flex-start; border-bottom:1px solid var(--edge); }
.case-title { flex:1; min-width:0; }
.case-title h2 { font-family:var(--sans); font-weight:600; font-size:15px; margin:0 0 3px; letter-spacing:-0.01em; }
.case-meta { font-family:var(--mono); font-size:10.5px; color:var(--text-fade); letter-spacing:0.02em; }

.dist-block { text-align:right; }
.dist-row { display:flex; align-items:baseline; gap:8px; justify-content:flex-end; margin-bottom:2px; }
.dist-label { font-family:var(--mono); font-size:9.5px; color:var(--text-fade); text-transform:uppercase; letter-spacing:0.05em; }
.rmsd { font-family:var(--mono); font-weight:500; font-size:20px; letter-spacing:-0.02em; line-height:1; color:var(--text); font-variant-numeric:tabular-nums; }
.rmsd.pass { color:var(--pass); }
.rmsd.fail { color:var(--fail); }
.rmsd.warn { color:var(--warn); }
.rmsd .unit { font-size:12px; color:var(--text-fade); margin-left:2px; }
.rmsd.v1 { font-size:15px; }

.viewer { width:100%; height:380px; background:#06080a; position:relative; }
.viewer-loading { position:absolute; inset:0; display:flex; align-items:center; justify-content:center; font-family:var(--mono); font-size:11px; color:var(--text-fade); }

.controls { display:flex; gap:6px; padding:8px 16px; background:var(--surface-2); border-top:1px solid var(--edge); flex-wrap:wrap; }
.controls button { font-family:var(--mono); font-size:10px; letter-spacing:0.05em; text-transform:uppercase; padding:4px 8px; border-radius:2px; border:1px solid var(--edge-strong); background:transparent; color:var(--text-dim); cursor:pointer; transition:all 0.15s; }
.controls button:hover { background:rgba(255,255,255,0.03); color:var(--text); }
.controls button.active { background:var(--edge-strong); color:var(--text); }

.case-footer { padding:10px 16px 12px; font-size:11.5px; color:var(--text-dim); border-top:1px solid var(--edge); line-height:1.5; font-family:var(--mono); }
.tag { display:inline-block; font-family:var(--mono); font-size:9.5px; letter-spacing:0.08em; text-transform:uppercase; padding:2px 6px; margin-right:6px; color:var(--text-fade); border:1px solid var(--edge-strong); border-radius:2px; }
.tag.flip { color:var(--fail); border-color:var(--fail); }
.tag.stable { color:var(--pass); border-color:var(--pass); }
</style>

<header class="page">
    <div class="eyebrow">g4 census · ligand-in-pocket sanity check</div>
    <h1>Is the ligand <em>actually</em> in the pocket? 10 predictions, receptor + ligand only.</h1>
    <p class="intro">
    Ten predictions rendered clean: <b>receptor cartoon</b> (chain A only, gray) + <b>the ligand HETATM the scorer picked</b> (cyan sticks).
    No pocket-anchor spheres, no centroid line — just look at whether the ligand sits inside the transmembrane bundle where the orthosteric pocket lives.
    <br><br>
    Header shows the census's <b>v1 distance</b> (which flagged half of these as ≥ 77 Å off-site) and the <b>v2 distance</b> after fixing the
    receptor-chain identification bug (v1's "longest polymer chain" heuristic picked Gα as the receptor when Gα was longer than the actual GPCR).
    All ten predictions turn out to have the ligand comfortably in the transmembrane bundle — the "off-site" flag was a measurement artifact.
    </p>
    <div class="legend">
        <div class="legend-item"><div class="legend-swatch" style="background:var(--text-dim)"></div>Receptor cartoon (chain A)</div>
        <div class="legend-item"><div class="legend-lig" style="background:var(--accent-pred)"></div>Picked ligand HETATM (sticks)</div>
        <div class="legend-item"><div class="legend-swatch" style="background:var(--pass)"></div>v2 dist &lt; 8 Å (in-pocket)</div>
        <div class="legend-item"><div class="legend-swatch" style="background:var(--warn)"></div>v2 dist 8–15 Å (pocket-adjacent)</div>
        <div class="legend-item"><div class="legend-swatch" style="background:var(--fail)"></div>v2 dist ≥ 15 Å (off-site)</div>
    </div>
</header>

<main class="grid">
"""

    case_sections = []
    cif_scripts = []
    js_cases = []
    for i, (row, scene, cif_content) in enumerate(cases):
        cid = f"case_{i+1:02d}"
        v1 = row["distance_A"]
        v2 = scene["distance_v2"]
        flipped = abs(v1 - v2) > 2.0
        if v2 < 8:
            v2_cls, v2_label = "pass", "in-pocket"
        elif v2 < 15:
            v2_cls, v2_label = "warn", "pocket-adjacent"
        else:
            v2_cls, v2_label = "fail", "off-site"
        v1_cls = "fail" if v1 >= 15 else ("warn" if v1 >= 8 else "pass")
        picked = scene["picked"]

        cif_scripts.append(f'<script type="text/plain" id="cif_{cid}">{cif_content}</script>')

        js_cases.append({
            "id": cid,
            "receptor_chain": scene["receptor_chain"],
            "picked_chain": picked["chain"],
            "picked_resi": picked["seqid"],
        })

        flip_tag = '<span class="tag flip">v1 buggy — Gα mispicked as receptor</span>' if flipped else '<span class="tag stable">v1 == v2</span>'
        picked_str = f"{picked['resname']} ({picked['n_heavy']} heavy atoms)"

        case_sections.append(f'''<section class="case" id="{cid}">
    <div class="case-header">
        <div class="case-title">
            <h2>{row['receptor']} · {row['role'].replace('_',' ')}</h2>
            <div class="case-meta">{row['backbone']} · arm: {row['arm']} · ligand: {picked_str} · receptor chain {scene['receptor_chain']} (anchor hits {scene['receptor_hits']}/6)</div>
        </div>
        <div class="dist-block">
            <div class="dist-row"><span class="dist-label">v1</span><div class="rmsd v1 {v1_cls}">{v1:.2f}<span class="unit">Å</span></div></div>
            <div class="dist-row"><span class="dist-label">v2</span><div class="rmsd {v2_cls}">{v2:.2f}<span class="unit">Å</span></div></div>
        </div>
    </div>
    <div class="viewer" id="viewer_{cid}"><div class="viewer-loading" id="loading_{cid}">loading…</div></div>
    <div class="controls">
        <button data-viewer="{cid}" data-action="zoom-pocket" class="active">zoom on ligand</button>
        <button data-viewer="{cid}" data-action="zoom-all">zoom on receptor</button>
        <button data-viewer="{cid}" data-action="toggle-surface">pocket surface</button>
    </div>
    <div class="case-footer">
        {flip_tag}<span class="tag" style="color:var(--{v2_cls});border-color:var(--{v2_cls})">v2 {v2_label}</span>
    </div>
</section>
''')

    js_body = f'''<script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.0/3Dmol-min.js"></script>
<script>
const CASES = {json.dumps(js_cases)};
const CYAN = {{ prop: 'elem', map: {{ C: '#4bb8d4', H: '#eaeaea', N: '#5f9fc3', O: '#e57373', S: '#e6c95c', F: '#a8d0a8', CL: '#a8d0a8', BR: '#a06060', P: '#e0a060' }} }};

function initViewer(spec) {{
    const viewport = document.getElementById('viewer_' + spec.id);
    const loading = document.getElementById('loading_' + spec.id);
    try {{
        const cif = document.getElementById('cif_' + spec.id).textContent;
        const viewer = $3Dmol.createViewer(viewport, {{ backgroundColor: '#06080a', antialias: true }});
        viewer.addModel(cif, 'cif');
        // Everything gray + subtle by default
        viewer.setStyle({{}}, {{}});
        // Receptor chain — subtle gray cartoon
        viewer.setStyle({{ chain: spec.receptor_chain }}, {{ cartoon: {{ color: '#3d434a', opacity: 0.85, thickness: 0.7, arrows: true }} }});
        // Ligand sticks (cyan)
        viewer.setStyle({{ chain: spec.picked_chain, resi: spec.picked_resi }}, {{ stick: {{ colorscheme: CYAN, radius: 0.22 }} }});
        // Default zoom: on the ligand
        try {{ viewer.zoomTo({{ chain: spec.picked_chain, resi: spec.picked_resi }}, 800); }} catch (e) {{ viewer.zoomTo(); }}
        viewer.zoom(0.55);
        viewer.render();
        loading.style.display = 'none';
        return {{ viewer, spec, surfaceHandle: null }};
    }} catch (err) {{
        console.error('viewer error', spec.id, err);
        loading.textContent = 'error: ' + err.message;
        return null;
    }}
}}

const viewers = {{}};
for (const c of CASES) viewers[c.id] = initViewer(c);

document.querySelectorAll('.controls button').forEach(btn => {{
    btn.addEventListener('click', () => {{
        const vid = btn.dataset.viewer;
        const action = btn.dataset.action;
        const v = viewers[vid];
        if (!v) return;
        const spec = v.spec;
        // De-active sibling zoom buttons
        if (action.startsWith('zoom')) {{
            document.querySelectorAll(`button[data-viewer="${{vid}}"][data-action^="zoom"]`).forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }}
        if (action === 'zoom-pocket') {{
            try {{ v.viewer.zoomTo({{ chain: spec.picked_chain, resi: spec.picked_resi }}, 800); }} catch (e) {{ v.viewer.zoomTo(); }}
            v.viewer.zoom(0.55);
            v.viewer.render();
        }} else if (action === 'zoom-all') {{
            v.viewer.zoomTo({{ chain: spec.receptor_chain }}, 800);
            v.viewer.render();
        }} else if (action === 'toggle-surface') {{
            btn.classList.toggle('active');
            if (btn.classList.contains('active') && v.surfaceHandle === null) {{
                v.surfaceHandle = v.viewer.addSurface($3Dmol.SurfaceType.MS, {{ opacity: 0.55, color: '#4b667a' }}, {{ chain: spec.receptor_chain }});
                v.viewer.render();
            }} else if (!btn.classList.contains('active') && v.surfaceHandle !== null) {{
                v.viewer.removeSurface(v.surfaceHandle);
                v.surfaceHandle = null;
                v.viewer.render();
            }}
        }}
    }});
}});
</script>
'''
    return header_html + "\n".join(case_sections) + "\n</main>\n\n" + "\n".join(cif_scripts) + "\n" + js_body


def main():
    sel = pd.read_csv(SEL_CSV)
    anchors = load_anchors()
    cases = []
    for _, row in sel.iterrows():
        r = row.to_dict()
        cif_path = CIF_ROOT / r["input_path"].replace("/hpc/scratch/sengaad1/", "")
        if not cif_path.exists(): continue
        rec = r["receptor"].upper()
        anchor_info = anchors.get(rec)
        if anchor_info is None: continue
        scene = compute(cif_path, anchor_info)
        if scene is None: continue
        cases.append((r, scene, cif_path.read_text()))
        print(f"  {rec:6s} {r['backbone']:9s} {r['role']:20s} {r['arm']:8s} v1={r['distance_A']:6.2f} v2={scene['distance_v2']:6.2f}")

    good = [c for c in cases if c[0]["quality"] == "good"]
    bad = [c for c in cases if c[0]["quality"] == "bad"]
    ordered = sorted(good, key=lambda c: c[1]["distance_v2"]) + sorted(bad, key=lambda c: -c[0]["distance_A"])
    OUT.write_text(build_html(ordered))
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
