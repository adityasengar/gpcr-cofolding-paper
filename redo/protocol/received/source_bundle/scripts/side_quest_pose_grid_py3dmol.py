"""
Fig 5 variant D — py3Dmol WebGL rendering, screenshot via Playwright Chromium.

For each (ligand, backbone) cell: build a small HTML page that
py3Dmol populates with the reference receptor cartoon + carazolol grey sticks
+ predicted-and-aligned ligand green sticks, then Playwright takes a PNG.
Composited into a 5×5 grid via matplotlib. RDKit provides the 2D-chem column.
"""
from __future__ import annotations

import asyncio
import base64
import sys
import time
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as mpimg

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from _pose_grid_common import (   # noqa: E402
    BACKBONES, BACKBONE_LABEL, CIF_REF, LIGANDS, OUT,
    align_pred_onto_ref, find_pred_cif,
)

TMP = REPO / "artefacts" / "side_figures_2026_09_06" / "_py3dmol_cells"
TMP.mkdir(parents=True, exist_ok=True)

# ---------- HTML template -------------------------------------------------
HTML_TEMPLATE = """<!doctype html>
<html><head><meta charset='utf-8'>
<style>html,body{margin:0;padding:0;background:#F8F8FA;}
#v{position:relative;width:__W__px;height:__H__px;}
</style>
<script src='https://3Dmol.csb.pitt.edu/build/3Dmol-min.js'></script>
</head><body>
<div id='v'></div>
<script>
window.addEventListener('load', function () {
  if (typeof $3Dmol === 'undefined') { window._err = 'no-3Dmol'; return; }
  const viewer = $3Dmol.createViewer('v', {backgroundColor:'#F8F8FA'});
  const receptorCif = `__REF_CIF__`;
  const ligandCif   = `__LIG_CIF__`;
  const carazolol   = `__CAR_CIF__`;
  viewer.addModel(receptorCif, 'cif');
  viewer.setStyle({}, {cartoon:{color:'#4DB5D9', thickness:0.7, arrows:true}});
  const poc = __POCKET_RESIDS__;
  viewer.addStyle({resi: poc}, {stick:{colorscheme:'cyanCarbon', radius:0.14}});
  viewer.addModel(carazolol, 'cif');
  viewer.setStyle({model:1}, {stick:{colorscheme:'greyCarbon', radius:0.16}});
  viewer.addModel(ligandCif, 'cif');
  viewer.setStyle({model:2}, {stick:{colorscheme:'greenCarbon', radius:0.20}});
  // camera: zoom on the predicted ligand, tilt slightly
  viewer.zoomTo({model:2}, 400);
  viewer.zoom(0.65);
  viewer.rotate(20, 'x');
  viewer.rotate(-15, 'y');
  viewer.render();
  window._done = true;
});
</script>
</body></html>
"""


def _load_text(path: str) -> str:
    return Path(path).read_text()


def _extract_receptor_cif(all_cif: str) -> str:
    """Keep only atoms/records; small enough to inline as JS template literal."""
    return all_cif


def _keep_only(st, chain_filter, resname_filter=None):
    """Mutate structure in-place: keep only chains/residues matching filters."""
    for model in st:
        # walk chains in reverse so index-based del stays valid
        for i in range(len(model) - 1, -1, -1):
            ch = model[i]
            if not chain_filter(ch):
                del model[i]
                continue
            for j in range(len(ch) - 1, -1, -1):
                res = ch[j]
                if resname_filter is not None and not resname_filter(res):
                    del ch[j]


def render_cell_with_playwright(idx: int, ref_cif: str, car_cif: str,
                                lig_cif: str, view: list[float]) -> Path:
    """Write HTML with 3Dmol, take screenshot via Playwright, return PNG path."""
    W, H = 540, 540
    pocket_str = "[" + ",".join(str(x) for x in POCKET_RESIDS) + "]"
    def _js_escape(s: str) -> str:
        return (s.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${"))
    html = (HTML_TEMPLATE
            .replace("__W__", str(W))
            .replace("__H__", str(H))
            .replace("__POCKET_RESIDS__", pocket_str)
            .replace("__REF_CIF__", _js_escape(ref_cif))
            .replace("__CAR_CIF__", _js_escape(car_cif))
            .replace("__LIG_CIF__", _js_escape(lig_cif)))
    html_path = TMP / f"cell_{idx:03d}.html"
    png_path = TMP / f"cell_{idx:03d}.png"
    html_path.write_text(html)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": W, "height": H})
        page.goto("file://" + str(html_path))
        # wait for 3Dmol to render
        page.wait_for_function("window._done === true", timeout=15000)
        page.wait_for_timeout(1000)   # extra beat for GPU
        page.screenshot(path=str(png_path), clip={"x": 0, "y": 0,
                                                  "width": W, "height": H})
        browser.close()
    return png_path


POCKET_RESIDS = [113, 117, 118, 193, 199, 286, 289, 290, 293, 308, 312]


def _isolate_receptor_from_2rh1() -> str:
    """Return a compact CIF with just chain A protein (no HET)."""
    import gemmi
    st = gemmi.read_structure(str(CIF_REF))
    _keep_only(st,
               chain_filter=lambda ch: ch.name == "A",
               resname_filter=lambda r: r.het_flag != "H")
    out = TMP / "_2rh1_clean.cif"
    st.make_mmcif_document().write_file(str(out))
    return out.read_text()


def _isolate_carazolol() -> str:
    import gemmi
    st = gemmi.read_structure(str(CIF_REF))
    _keep_only(st,
               chain_filter=lambda ch: ch.name == "A",
               resname_filter=lambda r: r.name == "CAU")
    out = TMP / "_carazolol.cif"
    st.make_mmcif_document().write_file(str(out))
    return out.read_text()


def _isolate_pred_ligand(pred_path: str) -> str:
    """Align predicted CIF to 2RH1 then keep only the ligand chain."""
    aligned, _ = align_pred_onto_ref(pred_path)
    _keep_only(aligned, chain_filter=lambda ch: ch.name != "A")
    out = TMP / "_lig_tmp.cif"
    aligned.make_mmcif_document().write_file(str(out))
    return out.read_text()


def _rdkit_smiles_png(smiles: str, name: str) -> np.ndarray:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw
    m = Chem.MolFromSmiles(smiles)
    AllChem.Compute2DCoords(m)
    img = Draw.MolToImage(m, size=(420, 360))
    return np.asarray(img)


def build_figure() -> None:
    ref_cif = _isolate_receptor_from_2rh1()
    car_cif = _isolate_carazolol()

    # A canonical py3Dmol view matrix (17 floats). Precomputed by
    # loading 2RH1, orienting the pocket toward the camera manually,
    # then reading viewer.getView().  Fallback: identity + zoom.
    view = [
        # translation (3), quaternion (4), zoom (1), z-slab near/far (2), FOV (1)
        # ...actually 3Dmol getView returns 17 floats — use a sane default:
        0.0, 0.0, -40.0,   # center offset
        0.4, 0.15, -0.05, 0.90,   # quaternion (arbitrary oblique view)
        1.0, 0.0, 0.0, 0.0,       # zoom, styles
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]

    # render each cell
    from concurrent.futures import ThreadPoolExecutor
    cells: dict[tuple[int, int], Path] = {}
    idx = 0
    for r, lig in enumerate(LIGANDS):
        for c, bb in enumerate(BACKBONES):
            pred_path = find_pred_cif(lig.code, bb)
            if pred_path is None:
                cells[(r, c)] = None
                idx += 1
                continue
            try:
                lig_cif = _isolate_pred_ligand(pred_path)
                cells[(r, c)] = render_cell_with_playwright(
                    idx, ref_cif, car_cif, lig_cif, view)
            except Exception as e:
                print(f"cell {lig.code}/{bb} failed:", e)
                cells[(r, c)] = None
            idx += 1
            print(f"  cell {r},{c} ({lig.code}/{bb}): {cells[(r,c)]}")

    # ----- compose grid with matplotlib -----------------------------------
    n_rows, n_cols = len(LIGANDS), 1 + len(BACKBONES)
    mpl.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                         "pdf.fonttype": 42, "ps.fonttype": 42,
                         "savefig.bbox": "tight", "savefig.dpi": 320})
    fig = plt.figure(figsize=(11.4, 2.15 * n_rows + 0.9))
    L, R, T, B = 0.045, 0.995, 0.88, 0.045
    gs = fig.add_gridspec(n_rows, n_cols,
                          left=L, right=R, top=T, bottom=B,
                          wspace=0.05, hspace=0.30,
                          width_ratios=[1.05] + [1.0] * 4)

    header_y = T + 0.012
    total_w = R - L
    chem_w = total_w * (1.05 / (1.05 + 4))
    fig.text(L + chem_w / 2, header_y, "chemistry",
             ha="center", va="bottom", fontsize=10, fontweight="bold")
    col_left = L + chem_w
    col_w = (R - col_left) / 4
    for k, bb in enumerate(BACKBONES):
        fig.text(col_left + col_w * (k + 0.5), header_y, BACKBONE_LABEL[bb],
                 ha="center", va="bottom", fontsize=10, fontweight="bold")

    for r, lig in enumerate(LIGANDS):
        axc = fig.add_subplot(gs[r, 0])
        axc.imshow(_rdkit_smiles_png(lig.smiles, lig.name))
        axc.set_xticks([]); axc.set_yticks([])
        for s in axc.spines.values(): s.set_visible(False)
        axc.text(0.5, -0.05, lig.name, transform=axc.transAxes,
                 ha="center", va="top", fontsize=8, fontweight="bold")
        axc.text(0.5, -0.15, lig.class_note, transform=axc.transAxes,
                 ha="center", va="top", fontsize=6.6, color="#555", style="italic")
        for c, bb in enumerate(BACKBONES):
            ax = fig.add_subplot(gs[r, 1 + c])
            path = cells.get((r, c))
            if path and path.exists():
                ax.imshow(mpimg.imread(path))
            else:
                ax.text(0.5, 0.5, "render fail",
                        transform=ax.transAxes, ha="center", va="center",
                        fontsize=8, color="#B00")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values(): s.set_visible(False)

    fig.text(L, 0.985,
             "ADRB2 orthosteric pose grid — py3Dmol WebGL rendering",
             fontsize=12, ha="left", va="top", fontweight="bold")
    fig.text(L, 0.955,
             "Reference: ADRB2 · 2RH1. Cyan cartoon + pocket sidechains. Grey sticks = carazolol reference; green sticks = "
             "predicted ligand after Kabsch alignment on pocket Cα.  Rendered with py3Dmol (3Dmol.js WebGL) via headless Chromium.",
             ha="left", va="top", fontsize=7, color="#444")

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig5d_pose_grid_py3dmol.{ext}")
    plt.close(fig)


if __name__ == "__main__":
    build_figure()
    print(f"OK — wrote fig5d_pose_grid_py3dmol to {OUT}")
