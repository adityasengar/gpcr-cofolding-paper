"""
Fig 5 variants A (ray-traced) and B (draw/OpenGL) — PyMOL rendering.

Runs under the conda pymol env:
    /Users/SENGAAD1/miniforge3/envs/pymol/bin/python scripts/side_quest_pose_grid_pymol.py --ray
    /Users/SENGAAD1/miniforge3/envs/pymol/bin/python scripts/side_quest_pose_grid_pymol.py --draw
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as mpimg

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from _pose_grid_common import (   # noqa: E402
    BACKBONES, BACKBONE_LABEL, CIF_REF, LIGANDS, OUT, POCKET_RESIDS,
    align_pred_onto_ref, find_pred_cif,
)

TMP = OUT / "_pymol_cells"
TMP.mkdir(parents=True, exist_ok=True)


def render_cell_pymol(ref_cif: Path, aligned_pred_cif: Path, out_png: Path,
                      *, use_ray: bool, W: int = 640, H: int = 640) -> None:
    """Full PyMOL rendering of a single cell — cartoon + pocket sticks + ligand."""
    from pymol import cmd, preset
    cmd.reinitialize()
    cmd.bg_color("white")
    cmd.load(str(ref_cif), "ref")
    cmd.load(str(aligned_pred_cif), "pred")

    # split reference into protein + carazolol
    cmd.create("receptor", "ref and polymer and chain A")
    cmd.create("carazolol", "ref and resn CAU")
    cmd.delete("ref")

    # split predicted into protein (drop) + ligand (keep)
    cmd.create("pred_lig", "pred and not polymer")
    cmd.delete("pred")

    # cartoon for receptor
    cmd.hide("everything")
    cmd.show("cartoon", "receptor")
    cmd.color("skyblue", "receptor")
    cmd.set("cartoon_transparency", 0.15, "receptor")
    cmd.set("cartoon_fancy_helices", 1)

    # pocket sidechains as sticks in slightly darker cyan
    poc_sel = "receptor and resi " + "+".join(str(r) for r in POCKET_RESIDS)
    cmd.show("sticks", poc_sel)
    cmd.color("lightblue", poc_sel + " and elem C")
    cmd.set("stick_radius", 0.14, poc_sel)

    # reference carazolol — grey sticks
    cmd.show("sticks", "carazolol")
    cmd.color("gray70", "carazolol and elem C")
    cmd.set("stick_radius", 0.16, "carazolol")

    # predicted ligand — green sticks (thicker, on top)
    cmd.show("sticks", "pred_lig")
    cmd.color("splitpea", "pred_lig and elem C")   # slight yellow-green
    cmd.set("stick_radius", 0.22, "pred_lig")
    # tiny balls at atoms for readability
    cmd.set("stick_ball", 1, "pred_lig")
    cmd.set("stick_ball_ratio", 1.8, "pred_lig")

    # element colouring for non-C atoms across everything
    for obj in ("carazolol", "pred_lig", "receptor"):
        cmd.color("blue", f"{obj} and elem N")
        cmd.color("red",  f"{obj} and elem O")
        cmd.color("orange", f"{obj} and elem S")
        cmd.color("palegreen", f"{obj} and elem F")
        cmd.color("chartreuse", f"{obj} and elem Cl")

    # zoom on the pocket / ligand region
    cmd.orient("carazolol")
    cmd.zoom("carazolol expand 10", buffer=2, complete=1)

    # publication settings
    cmd.set("ray_shadows", 1)
    cmd.set("ray_shadow_decay_factor", 0.10)
    cmd.set("ambient", 0.20)
    cmd.set("specular", 0.4)
    cmd.set("depth_cue", 1)
    cmd.set("fog_start", 0.6)
    cmd.set("ray_opaque_background", 0)
    cmd.set("antialias", 2)
    cmd.set("ray_trace_mode", 1)   # 1 = outlines; 0 = plain
    cmd.set("ray_trace_color", "grey30")

    cmd.set("cartoon_side_chain_helper", 1)

    if use_ray:
        cmd.ray(W, H)
    else:
        cmd.draw(W, H, antialias=1)
    cmd.png(str(out_png), dpi=300)


def _prepare_aligned_pred_cifs() -> dict[tuple[str, str], tuple[Path, float]]:
    """Kabsch-align every predicted CIF once, save to TMP.  Returns {(code, bb): (path, rmsd)}."""
    import gemmi
    out: dict[tuple[str, str], tuple[Path, float]] = {}
    for lig in LIGANDS:
        for bb in BACKBONES:
            path = find_pred_cif(lig.code, bb)
            if not path:
                out[(lig.code, bb)] = (None, float("nan"))
                continue
            aligned_path = TMP / f"aligned_{lig.code}_{bb}.cif"
            if aligned_path.exists():
                # still need rmsd — recompute
                _, rmsd = align_pred_onto_ref(path)
                out[(lig.code, bb)] = (aligned_path, rmsd)
                continue
            aligned, rmsd = align_pred_onto_ref(path)
            aligned.make_mmcif_document().write_file(str(aligned_path))
            out[(lig.code, bb)] = (aligned_path, rmsd)
    return out


def _rdkit_smiles_png(smiles: str) -> np.ndarray:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw
    m = Chem.MolFromSmiles(smiles)
    AllChem.Compute2DCoords(m)
    img = Draw.MolToImage(m, size=(420, 360))
    return np.asarray(img)


def build_figure(use_ray: bool) -> None:
    aligned = _prepare_aligned_pred_cifs()
    cells: dict[tuple[int, int], tuple[Path | None, float]] = {}
    for r, lig in enumerate(LIGANDS):
        for c, bb in enumerate(BACKBONES):
            pred_cif, rmsd = aligned[(lig.code, bb)]
            if pred_cif is None:
                cells[(r, c)] = (None, rmsd)
                continue
            out_png = TMP / f"cell_{'ray' if use_ray else 'draw'}_{lig.code}_{bb}.png"
            print(f"  render {lig.code}/{bb} → {out_png.name}", flush=True)
            render_cell_pymol(CIF_REF, pred_cif, out_png, use_ray=use_ray)
            cells[(r, c)] = (out_png, rmsd)

    # ---- compose grid ----
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
        axc.imshow(_rdkit_smiles_png(lig.smiles))
        axc.set_xticks([]); axc.set_yticks([])
        for s in axc.spines.values(): s.set_visible(False)
        axc.text(0.5, -0.05, lig.name, transform=axc.transAxes,
                 ha="center", va="top", fontsize=8, fontweight="bold")
        axc.text(0.5, -0.15, lig.class_note, transform=axc.transAxes,
                 ha="center", va="top", fontsize=6.6, color="#555", style="italic")
        for c, bb in enumerate(BACKBONES):
            ax = fig.add_subplot(gs[r, 1 + c])
            path, rmsd = cells.get((r, c), (None, float("nan")))
            if path and path.exists():
                ax.imshow(mpimg.imread(path))
                ax.text(0.03, 0.03,
                        f"pocket Cα {rmsd:.2f} Å",
                        transform=ax.transAxes, ha="left", va="bottom",
                        fontsize=6.3, color="#333",
                        bbox=dict(facecolor="white", edgecolor="none",
                                  alpha=0.85, boxstyle="round,pad=0.2"),
                        zorder=10)
            else:
                ax.text(0.5, 0.5, "render fail",
                        transform=ax.transAxes, ha="center", va="center",
                        fontsize=8, color="#B00")
            ax.set_xticks([]); ax.set_yticks([])
            for s in ax.spines.values(): s.set_visible(False)

    style = "ray-traced" if use_ray else "OpenGL draw()"
    fig.text(L, 0.985,
             f"ADRB2 orthosteric pose grid — PyMOL {style} rendering",
             fontsize=12, ha="left", va="top", fontweight="bold")
    fig.text(L, 0.955,
             "Reference: ADRB2 · 2RH1. Cyan cartoon + pocket sidechains (BW 3.32-7.43). Grey sticks = carazolol reference; green sticks = "
             "predicted ligand after Kabsch alignment on pocket Cα. Rendered with PyMOL open-source " + style + ".",
             ha="left", va="top", fontsize=7, color="#444")

    tag = "a_pymol_ray" if use_ray else "b_pymol_draw"
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig5{tag}_pose_grid.{ext}")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    grp = ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--ray", action="store_true", help="ray-traced")
    grp.add_argument("--draw", action="store_true", help="OpenGL")
    args = ap.parse_args()
    build_figure(use_ray=args.ray)
    print("OK — wrote", "fig5a_pymol_ray_pose_grid" if args.ray
                        else "fig5b_pymol_draw_pose_grid", "to", OUT)


if __name__ == "__main__":
    main()
