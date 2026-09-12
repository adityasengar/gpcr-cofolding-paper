"""
Fig 5 variant C — Biotite matplotlib 3D wire rendering.

Uses biotite.structure.graphics.plot_atoms — no cartoon, no ray-tracing.
The receptor is drawn as a Cα wire (thin) inside a rasterized-blur cloud
for depth, pocket-residue heavy atoms as thicker cyan wires, and the
predicted / reference ligand as bond-thick sticks.
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from _pose_grid_common import (   # noqa: E402
    BACKBONES, BACKBONE_LABEL, CIF_REF, LIGANDS, OUT, POCKET_RESIDS,
    align_pred_onto_ref, find_pred_cif,
)


def _load_atomarray(cif_path: Path):
    import biotite.structure.io.pdbx as pdbx
    import biotite.structure as struc
    cif = pdbx.PDBxFile.read(str(cif_path))
    arr = pdbx.get_structure(cif, model=1)
    # add bond list from ChemicalComponent guesses
    arr.bonds = struc.connect_via_residue_names(arr)
    return arr


def _element_color(elem: str, is_pred: bool) -> np.ndarray:
    if elem == "C":
        return np.array([0.24, 0.55, 0.22]) if is_pred else np.array([0.30, 0.70, 0.85])
    if elem == "N": return np.array([0.24, 0.42, 0.70])
    if elem == "O": return np.array([0.76, 0.15, 0.18])
    if elem == "S": return np.array([0.90, 0.69, 0.03])
    if elem == "F": return np.array([0.64, 0.84, 0.64])
    if elem in ("Cl", "CL"): return np.array([0.49, 0.75, 0.49])
    return np.array([0.4, 0.4, 0.4])


def _atom_colors(atoms, is_pred: bool) -> np.ndarray:
    return np.stack([_element_color(a.element, is_pred) for a in atoms])


def _cell(ax3d, ref_arr, car_arr, pred_arr, rmsd: float, title: str) -> None:
    from biotite.structure.graphics import plot_atoms
    from biotite.structure import filter_amino_acids
    import biotite.structure as struc

    # centre camera on carazolol
    car_centroid = car_arr.coord.mean(axis=0)

    # RECEPTOR — protein-only Cα trace: thin light cyan
    prot_mask = filter_amino_acids(ref_arr)
    ca_mask = (ref_arr.atom_name == "CA") & prot_mask & (ref_arr.chain_id == "A")
    ca = ref_arr[ca_mask]
    if len(ca):
        # simple polyline connect Cα by residue order
        ax3d.plot(ca.coord[:, 0], ca.coord[:, 1], ca.coord[:, 2],
                  color="#4DB5D9", alpha=0.45, lw=1.2, zorder=1)

    # POCKET sidechains — dense stick wire
    poc_mask = (np.isin(ref_arr.res_id, POCKET_RESIDS) & prot_mask
                & (ref_arr.chain_id == "A") & (ref_arr.element != "H"))
    poc = ref_arr[poc_mask]
    if len(poc):
        colours = _atom_colors(poc, is_pred=False)
        # override C's to a dedicated pocket cyan
        colours[poc.element == "C"] = np.array([0.30, 0.70, 0.82])
        plot_atoms(ax3d, poc, colours, line_width=2.2,
                   center=car_centroid, size=22, zoom=1.0)

    # REFERENCE ligand (carazolol) — grey sticks
    if car_arr is not None and len(car_arr):
        col = _atom_colors(car_arr, is_pred=False)
        col[car_arr.element == "C"] = np.array([0.60, 0.60, 0.62])
        plot_atoms(ax3d, car_arr, col, line_width=2.3,
                   center=car_centroid, size=22, zoom=1.0)

    # PREDICTED ligand — green sticks (thicker, on top)
    if pred_arr is not None and len(pred_arr):
        col = _atom_colors(pred_arr, is_pred=True)
        plot_atoms(ax3d, pred_arr, col, line_width=3.0,
                   center=car_centroid, size=22, zoom=1.0)

    ax3d.set_facecolor("#F8F8FA")
    ax3d.grid(False)
    for spine in ax3d.xaxis.pane, ax3d.yaxis.pane, ax3d.zaxis.pane:
        spine.set_edgecolor("#EEE")
        spine.set_facecolor("#F8F8FA")
    ax3d.set_xticks([]); ax3d.set_yticks([]); ax3d.set_zticks([])
    ax3d.set_xlabel(""); ax3d.set_ylabel(""); ax3d.set_zlabel("")

    # oblique camera
    ax3d.view_init(elev=18, azim=-60)

    ax3d.text2D(0.03, 0.03, f"pocket Cα {rmsd:.2f} Å",
                transform=ax3d.transAxes, ha="left", va="bottom",
                fontsize=6.3, color="#333",
                bbox=dict(facecolor="white", edgecolor="none",
                          alpha=0.85, boxstyle="round,pad=0.2"),
                zorder=100)


def _isolate_pred_ligand_arr(pred_path: str):
    """Kabsch-align then return biotite AtomArray of ligand only."""
    aligned, rmsd = align_pred_onto_ref(pred_path)
    tmp = OUT / "_biotite_tmp.cif"
    aligned.make_mmcif_document().write_file(str(tmp))
    arr = _load_atomarray(tmp)
    # filter to ligand: non-protein residues on non-A chain
    from biotite.structure import filter_amino_acids
    lig_mask = (~filter_amino_acids(arr)) & (arr.chain_id != "A")
    return arr[lig_mask], rmsd


def _rdkit_smiles_png(smiles: str) -> np.ndarray:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw
    m = Chem.MolFromSmiles(smiles)
    AllChem.Compute2DCoords(m)
    img = Draw.MolToImage(m, size=(420, 360))
    return np.asarray(img)


def build_figure() -> None:
    from biotite.structure import filter_amino_acids

    ref_arr = _load_atomarray(CIF_REF)
    # carazolol residues
    car_mask = (ref_arr.res_name == "CAU") & (ref_arr.element != "H")
    car_arr = ref_arr[car_mask]

    n_rows, n_cols = len(LIGANDS), 1 + len(BACKBONES)
    mpl.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
                         "pdf.fonttype": 42, "ps.fonttype": 42,
                         "savefig.bbox": "tight", "savefig.dpi": 320})
    fig = plt.figure(figsize=(11.4, 2.3 * n_rows + 0.9))
    L, R, T, B = 0.045, 0.995, 0.88, 0.045
    gs = fig.add_gridspec(n_rows, n_cols,
                          left=L, right=R, top=T, bottom=B,
                          wspace=0.05, hspace=0.35,
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
            ax3d = fig.add_subplot(gs[r, 1 + c], projection="3d")
            pred_path = find_pred_cif(lig.code, bb)
            if pred_path is None:
                ax3d.text2D(0.5, 0.5, "no CIF", transform=ax3d.transAxes,
                            ha="center", va="center", fontsize=8, color="#B00")
                continue
            try:
                pred_arr, rmsd = _isolate_pred_ligand_arr(pred_path)
            except Exception as e:
                ax3d.text2D(0.5, 0.5, f"err\n{e.__class__.__name__}",
                            transform=ax3d.transAxes, ha="center", va="center",
                            fontsize=7, color="#B00")
                continue
            _cell(ax3d, ref_arr, car_arr, pred_arr, rmsd,
                  f"{lig.code}/{bb}")

    fig.text(L, 0.985,
             "ADRB2 orthosteric pose grid — Biotite 3D wire rendering",
             fontsize=12, ha="left", va="top", fontweight="bold")
    fig.text(L, 0.955,
             "Reference: ADRB2 · 2RH1. Light cyan wire = full Cα trace; darker cyan sticks = pocket residues; grey sticks = "
             "carazolol reference; green sticks = predicted ligand after Kabsch alignment on pocket Cα. Rendered with "
             "biotite.structure.graphics.plot_atoms into Matplotlib 3D.",
             ha="left", va="top", fontsize=7, color="#444")

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig5c_pose_grid_biotite.{ext}")
    plt.close(fig)


if __name__ == "__main__":
    build_figure()
    print(f"OK — wrote fig5c_pose_grid_biotite to {OUT}")
