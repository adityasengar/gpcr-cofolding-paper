"""
Side-quest #3 — Nat Comms style pose-comparison grid.

Rows  = ligand chemistry (5 ADRB2 probes: dopamine, histamine, isoproterenol,
        propranolol, haloperidol).
Cols  = 2D chem structure + 4 backbones (AF3/OF3, Boltz-1, Chai-1, Protenix).
Each cell shows the predicted ligand pose (green) overlaid on the reference
ADRB2 pocket residues (cyan sticks) + reference ligand carazolol (grey sticks)
from 2RH1. All predictions are Kabsch-aligned to 2RH1 on pocket Cα atoms.

Output: artefacts/side_figures_2026_09_06/fig5_pose_grid.{pdf,png}
"""
from __future__ import annotations

import glob
import io
import warnings
from dataclasses import dataclass
from pathlib import Path

import gemmi
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image as mpimg
from scipy.ndimage import gaussian_filter

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parents[1]
CIF_REF = REPO / "refs" / "cache" / "rcsb" / "pdb_2rh1.cif"
PROBE = REPO / "experiments" / "020_block_c_ligand_pharmacology" / "analysis" / "_probe_stage"
OUT = REPO / "artefacts" / "side_figures_2026_09_06"
OUT.mkdir(parents=True, exist_ok=True)

# BW-anchor pocket-defining positions on ADRB2 (uniprot numbering — matches 2RH1
# auth_seq_id).  A canonical orthosteric-pocket sampling: TM3 3.32/3.36/3.37,
# TM5 5.42/5.46, TM6 6.48/6.51/6.55, TM7 7.39/7.43.
POCKET_RESIDS = [113, 117, 118, 193, 199, 286, 289, 290, 293, 308, 312]

# five ADRB2 ligands, ordered by chemistry (native → off-target)
@dataclass
class Ligand:
    code: str
    name: str
    smiles: str
    class_note: str

LIGANDS: list[Ligand] = [
    Ligand("ip", "R-isoproterenol",
           "CC(C)[NH2+]C[C@@H](O)c1ccc(O)c(O)c1",
           "β-adrenergic full agonist"),
    Ligand("pp", "S-propranolol",
           "CC(C)[NH2+]C[C@H](O)COc1cccc2ccccc12",
           "β-antagonist"),
    Ligand("dp", "dopamine",
           "[NH3+]CCc1ccc(O)c(O)c1",
           "wrong receptor (D-family)"),
    Ligand("hs", "histamine",
           "[NH3+]CCc1c[nH]cn1",
           "wrong receptor (H-family)"),
    Ligand("hp", "haloperidol",
           "O=C(c1ccc(F)cc1)CCC[NH+]2CCC(O)(c3ccc(Cl)cc3)CC2",
           "wrong receptor (D2 antagonist)"),
]

BACKBONES = ["of3", "boltz", "chai", "protenix"]
BACKBONE_LABEL = {
    "of3": "OpenFold3",
    "boltz": "Boltz-1",
    "chai": "Chai-1",
    "protenix": "Protenix",
}
ELEMENT_COLOR = {
    "C": "#3D8B37",   # predicted ligand: green C
    "N": "#3D6BB3",
    "O": "#C1272D",
    "S": "#E5B008",
    "P": "#E76F00",
    "F": "#A3D7A3",
    "CL": "#7EBF7E",
    "Cl": "#7EBF7E",
}
REF_LIG_COLOR = {   # grey palette for reference carazolol
    "C": "#8A8A8A",
    "N": "#4C6F9C",
    "O": "#A15252",
    "S": "#B8931F",
    "F": "#BFBFBF",
    "CL": "#B0B0B0", "Cl": "#B0B0B0",
}
POCKET_C_COLOR = "#4FB3D9"   # cyan carbon for pocket sticks
POCKET_HALO = "#B8E7F5"

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.dpi": 320,
})


# --------------------------- CIF helpers ---------------------------------
@dataclass
class Atom:
    name: str
    element: str
    xyz: np.ndarray
    resid: int
    resname: str
    chain: str


def _element(a: gemmi.Atom) -> str:
    e = a.element.name.strip().upper()
    return e or a.name[0].upper()


def read_cif(path: str) -> list[Atom]:
    st = gemmi.read_structure(path)
    m = st[0]
    out: list[Atom] = []
    for ch in m:
        for res in ch:
            for a in res:
                out.append(Atom(
                    name=a.name.strip(),
                    element=_element(a),
                    xyz=np.array([a.pos.x, a.pos.y, a.pos.z]),
                    resid=res.seqid.num,
                    resname=res.name,
                    chain=ch.name,
                ))
    return out


def pocket_ca(atoms: list[Atom], resids: list[int]) -> tuple[np.ndarray, np.ndarray]:
    xs, ids = [], []
    for a in atoms:
        if a.name == "CA" and a.resid in resids and a.chain in ("A",):
            xs.append(a.xyz)
            ids.append(a.resid)
    return np.asarray(xs), np.asarray(ids)


def pocket_sidechain_atoms(atoms: list[Atom], resids: list[int]) -> list[Atom]:
    # keep every non-hydrogen atom of every pocket residue → dense wall of sticks
    return [a for a in atoms if a.resid in resids and a.chain == "A"
            and a.element != "H"]


def ligand_atoms(atoms: list[Atom], names: tuple[str, ...] = ("CAU",),
                 chains: tuple[str, ...] | None = None,
                 exclude_resname: tuple[str, ...] = ("HOH", "SO4", "GLC",
                                                     "PGE", "PEG", "EDO", "CLR", "PLM")
                 ) -> list[Atom]:
    # find non-protein residues in named chains
    protein_res = {"ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY",
                   "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER",
                   "THR", "TRP", "TYR", "VAL"}
    keep = []
    for a in atoms:
        if a.resname in protein_res:
            continue
        if a.resname in exclude_resname:
            continue
        if chains is not None and a.chain not in chains:
            continue
        if names and a.resname not in names:
            # match starts-with for LIG0/1/2
            if not any(a.resname.startswith(n) for n in names):
                continue
        keep.append(a)
    return keep


# --------------------------- geometry ------------------------------------
def kabsch(m: np.ndarray, t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ca, cb = m.mean(0), t.mean(0)
    H = (m - ca).T @ (t - cb)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    T = cb - ca @ R.T
    return R, T


def apply_rt(x: np.ndarray, R: np.ndarray, T: np.ndarray) -> np.ndarray:
    return x @ R.T + T


def align_pred_to_ref(ref_atoms: list[Atom], pred_atoms: list[Atom],
                      resids: list[int]) -> tuple[np.ndarray, np.ndarray]:
    ref_ca, ref_ids = pocket_ca(ref_atoms, resids)
    pred_ca, pred_ids = pocket_ca(pred_atoms, resids)
    common = np.intersect1d(ref_ids, pred_ids)
    if len(common) < 4:
        return np.eye(3), np.zeros(3)
    A = pred_ca[np.isin(pred_ids, common)]
    B = ref_ca[np.isin(ref_ids, common)]
    return kabsch(A, B)


def compute_camera(pocket_atoms: list[Atom], carazolol_xyz: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """3x3 frame + centre — look down the pocket axis with the ligand at the origin."""
    xs = np.stack([a.xyz for a in pocket_atoms])
    all_pts = np.vstack([xs, carazolol_xyz])
    centre = all_pts.mean(0)
    x0 = all_pts - centre
    cov = np.cov(x0.T)
    _, evec = np.linalg.eigh(cov)
    # x = largest spread → in-plane; y = 2nd; z (depth) = smallest
    F = evec[:, ::-1]  # columns descending eigenvalue
    # ensure right-handed
    if np.linalg.det(F) < 0:
        F[:, 2] *= -1
    return F, centre


# --------------------------- drawing -------------------------------------
def _bond_pairs(atoms: list[Atom], max_d: float = 1.85) -> list[tuple[int, int]]:
    n = len(atoms)
    xs = np.stack([a.xyz for a in atoms])
    d = np.linalg.norm(xs[:, None] - xs[None, :], axis=-1)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            if 0.9 < d[i, j] < max_d:
                pairs.append((i, j))
    return pairs


def draw_sticks(ax, atoms: list[Atom], proj: np.ndarray, colours: dict[str, str],
                *, lw: float = 2.1, ball_r: float = 3.0, alpha: float = 1.0,
                edge: str = "white", zorder: float = 6, ball_edge_lw: float = 0.5,
                halo: str | None = None) -> None:
    if not atoms:
        return
    xy = proj[:, :2]
    pairs = _bond_pairs(atoms)
    for i, j in pairs:
        ci = colours.get(atoms[i].element, colours.get("C", "#666"))
        cj = colours.get(atoms[j].element, colours.get("C", "#666"))
        mid = (xy[i] + xy[j]) / 2
        for p, q, col in ((xy[i], mid, ci), (mid, xy[j], cj)):
            ax.plot([p[0], q[0]], [p[1], q[1]], color=col, lw=lw,
                    alpha=alpha, solid_capstyle="round", zorder=zorder)
    for atom, (x, y) in zip(atoms, xy):
        col = colours.get(atom.element, colours.get("C", "#666"))
        s = np.pi * (ball_r) ** 2
        if halo is not None:
            ax.scatter(x, y, s=s * 1.9, c=halo, alpha=0.35 * alpha,
                       linewidths=0, zorder=zorder + 0.3)
        ax.scatter(x, y, s=s, c=col, alpha=alpha, edgecolors=edge,
                   linewidths=ball_edge_lw, zorder=zorder + 0.5)


def draw_pocket_wire(ax, pocket_atoms: list[Atom], proj: np.ndarray,
                     colour: str = POCKET_C_COLOR,
                     alpha: float = 0.65) -> None:
    """Blurred backdrop + faint stick strokes for the pocket."""
    if not pocket_atoms:
        return
    xy = proj[:, :2]
    pairs = _bond_pairs(pocket_atoms, max_d=2.2)
    # rasterise stroke set to blur behind
    xlim, ylim = ax.get_xlim(), ax.get_ylim()
    W, H = 640, 640
    canvas = np.zeros((H, W), float)
    for i, j in pairs:
        p, q = xy[i], xy[j]
        n = int(max(3, np.hypot(q[0] - p[0], q[1] - p[1]) * 40))
        t = np.linspace(0, 1, n)
        u = ((p[0] + t * (q[0] - p[0])) - xlim[0]) / (xlim[1] - xlim[0]) * (W - 1)
        v = ((p[1] + t * (q[1] - p[1])) - ylim[0]) / (ylim[1] - ylim[0]) * (H - 1)
        iu = np.clip(u.astype(int), 0, W - 1)
        iv = np.clip(v.astype(int), 0, H - 1)
        np.add.at(canvas, (iv, iu), 1.0)
    blurred = gaussian_filter(canvas, sigma=5.0)
    if blurred.max() > 0:
        blurred = blurred / blurred.max()
    rgb = np.array(mpl.colors.to_rgb(colour))
    rgba = np.zeros((H, W, 4), float)
    rgba[..., :3] = rgb
    rgba[..., 3] = np.clip(blurred, 0, 1) ** 0.7 * 0.6
    ax.imshow(rgba, extent=(*xlim, *ylim), origin="lower",
              interpolation="bilinear", zorder=2)
    # crisp thin stroke overlay for a couple of key backbone contours
    for i, j in pairs:
        ax.plot([xy[i, 0], xy[j, 0]], [xy[i, 1], xy[j, 1]],
                color=colour, lw=0.8, alpha=alpha * 0.4,
                solid_capstyle="round", zorder=3)


def get_pred_ligand_atoms(atoms: list[Atom]) -> list[Atom]:
    """Return the non-protein ligand atoms from a predicted CIF.

    Backbones name the ligand differently: Boltz LIG1, Chai LIG2, OF3 LIG0,
    Protenix l01. Anything non-protein on a chain other than A qualifies —
    the receptor is always on A."""
    protein_res = {"ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY",
                   "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER",
                   "THR", "TRP", "TYR", "VAL"}
    return [a for a in atoms if a.chain != "A" and a.resname not in protein_res]


# --------------------------- 2D chem panel -------------------------------
def draw_smiles_panel(ax, ligand: Ligand) -> None:
    from rdkit import Chem
    from rdkit.Chem import Draw, AllChem
    mol = Chem.MolFromSmiles(ligand.smiles)
    if mol is None:
        ax.text(0.5, 0.5, ligand.name + "\n(SMILES fail)", ha="center",
                va="center", transform=ax.transAxes, fontsize=7)
        ax.set_xticks([]); ax.set_yticks([])
        return
    AllChem.Compute2DCoords(mol)
    img = Draw.MolToImage(mol, size=(360, 300))
    ax.imshow(np.asarray(img))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.text(0.5, -0.03, ligand.name,
            transform=ax.transAxes, ha="center", va="top",
            fontsize=8, fontweight="bold", color="#111")
    ax.text(0.5, -0.15, ligand.class_note,
            transform=ax.transAxes, ha="center", va="top",
            fontsize=6.6, color="#555", style="italic")


# --------------------------- pose cell ------------------------------------
def find_pred_cif(code: str, backbone: str) -> str | None:
    base = PROBE / backbone / code
    matches: list[str] = []
    if backbone == "boltz":
        matches = glob.glob(str(base / f"boltz_results_{code}_boltz" /
                                 "predictions" / f"{code}_boltz" /
                                 f"{code}_boltz_model_0.cif"))
    elif backbone == "chai":
        matches = glob.glob(str(base / "pred.model_idx_0.cif"))
    elif backbone == "of3":
        matches = glob.glob(str(base / f"gate02_{code}_of3" / "seed_*" /
                                 f"gate02_{code}_of3_seed_*_sample_1_model.cif"))
    elif backbone == "protenix":
        matches = glob.glob(str(base / f"gate02_{code}_protenix" / "seed_*" /
                                 "predictions" / f"gate02_{code}_protenix_sample_0.cif"))
    return matches[0] if matches else None


def render_pose_cell(ax, ref_atoms: list[Atom],
                     ligand: Ligand, backbone: str,
                     camera_F: np.ndarray, camera_centre: np.ndarray,
                     span: float = 8.5) -> str:
    """Return short status: 'ok', 'missing', 'noalign'."""
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-span, span); ax.set_ylim(-span, span)
    ax.set_aspect("equal", adjustable="box")
    ax.set_facecolor("#F8F8FA")
    for s in ax.spines.values():
        s.set_visible(False)

    # ---- reference pocket + carazolol (grey) — same in every cell ----------
    pocket = pocket_sidechain_atoms(ref_atoms, POCKET_RESIDS)
    pocket_xyz = np.stack([a.xyz for a in pocket]) if pocket else np.zeros((0, 3))
    ref_lig = ligand_atoms(ref_atoms, names=("CAU",))
    ref_lig_xyz = np.stack([a.xyz for a in ref_lig]) if ref_lig else np.zeros((0, 3))

    def project(xyz: np.ndarray) -> np.ndarray:
        return (xyz - camera_centre) @ camera_F

    if len(pocket_xyz):
        proj = project(pocket_xyz)
        draw_pocket_wire(ax, pocket, proj)

    if len(ref_lig_xyz):
        proj = project(ref_lig_xyz)
        # sticks lw thin, semi-translucent — grey reference feel
        draw_sticks(ax, ref_lig, proj, REF_LIG_COLOR,
                    lw=1.6, ball_r=2.7, alpha=0.9,
                    halo="#D8D8D8", zorder=5)

    # ---- predicted ligand (green) ------------------------------------------
    cif = find_pred_cif(ligand.code, backbone)
    if cif is None:
        ax.text(0.5, 0.5, "no CIF", transform=ax.transAxes,
                ha="center", va="center", fontsize=8, color="#B00")
        return "missing"
    try:
        pred_all = read_cif(cif)
    except Exception as exc:
        ax.text(0.5, 0.5, f"parse err\n{type(exc).__name__}",
                transform=ax.transAxes,
                ha="center", va="center", fontsize=7, color="#B00")
        return "parse_err"
    R, T = align_pred_to_ref(ref_atoms, pred_all, POCKET_RESIDS)
    pred_lig = get_pred_ligand_atoms(pred_all)
    if not pred_lig:
        ax.text(0.5, 0.5, "no ligand", transform=ax.transAxes,
                ha="center", va="center", fontsize=8, color="#B00")
        return "no_lig"
    xyz = apply_rt(np.stack([a.xyz for a in pred_lig]), R, T)
    proj = project(xyz)
    draw_sticks(ax, pred_lig, proj, ELEMENT_COLOR,
                lw=2.0, ball_r=3.1, alpha=0.98,
                halo="#B8E68A", zorder=7)

    # Cα-RMSD tag over pocket residues
    ref_ca, ref_ids = pocket_ca(ref_atoms, POCKET_RESIDS)
    pred_ca, pred_ids = pocket_ca(pred_all, POCKET_RESIDS)
    common = np.intersect1d(ref_ids, pred_ids)
    if len(common) >= 3:
        A = pred_ca[np.isin(pred_ids, common)]
        B = ref_ca[np.isin(ref_ids, common)]
        A_al = apply_rt(A, R, T)
        rmsd = float(np.sqrt(((A_al - B) ** 2).sum(axis=1).mean()))
        # place RMSD chip opposite the predicted-ligand centroid so it never
        # sits under green atoms (bit haloperidol's drooping tail otherwise)
        pred_lig_xy = proj[:, :2]
        cxg, cyg = pred_lig_xy.mean(0)
        xlo, xhi = ax.get_xlim()
        ylo, yhi = ax.get_ylim()
        # normalize centroid to [0,1] then pick opposite corner
        u = (cxg - xlo) / (xhi - xlo)
        v = (cyg - ylo) / (yhi - ylo)
        fx = 0.97 if u < 0.5 else 0.03
        fy = 0.97 if v < 0.5 else 0.03
        ha = "right" if fx > 0.5 else "left"
        va = "top"   if fy > 0.5 else "bottom"
        ax.text(fx, fy, f"pocket Cα RMSD {rmsd:.2f} Å",
                transform=ax.transAxes, ha=ha, va=va,
                fontsize=6.3, color="#333",
                bbox=dict(facecolor="white", edgecolor="none",
                          alpha=0.9, boxstyle="round,pad=0.2"),
                zorder=10)
    return "ok"


# --------------------------- figure --------------------------------------
def figure5() -> None:
    ref_atoms = read_cif(str(CIF_REF))
    # pick camera on reference pocket + carazolol centroid
    pocket = pocket_sidechain_atoms(ref_atoms, POCKET_RESIDS)
    caraz = ligand_atoms(ref_atoms, names=("CAU",))
    caraz_xyz = np.stack([a.xyz for a in caraz])
    F, centre = compute_camera(pocket, caraz_xyz)

    n_rows = len(LIGANDS)
    n_cols = 1 + len(BACKBONES)
    fig = plt.figure(figsize=(11.4, 2.15 * n_rows + 0.9))
    LEFT, RIGHT, TOP, BOTTOM = 0.045, 0.995, 0.88, 0.045
    gs = fig.add_gridspec(
        n_rows, n_cols,
        left=LEFT, right=RIGHT, top=TOP, bottom=BOTTOM,
        wspace=0.05, hspace=0.30,
        width_ratios=[1.05] + [1.0] * len(BACKBONES),
    )

    # column titles — right above row 1 axes
    header_y = TOP + 0.012
    total_w = RIGHT - LEFT
    chem_w = total_w * (1.05 / (1.05 + 4))
    fig.text(LEFT + chem_w / 2, header_y, "chemistry",
             ha="center", va="bottom",
             fontsize=10, fontweight="bold", color="#111")
    col_frac_left = LEFT + chem_w
    col_width = (RIGHT - col_frac_left) / 4
    for k, bb in enumerate(BACKBONES):
        cx = col_frac_left + col_width * (k + 0.5)
        fig.text(cx, header_y, BACKBONE_LABEL[bb],
                 ha="center", va="bottom",
                 fontsize=10, fontweight="bold", color="#111")

    for r, ligand in enumerate(LIGANDS):
        ax_chem = fig.add_subplot(gs[r, 0])
        draw_smiles_panel(ax_chem, ligand)
        for c, bb in enumerate(BACKBONES):
            ax = fig.add_subplot(gs[r, 1 + c])
            render_pose_cell(ax, ref_atoms, ligand, bb, F, centre)

    fig.text(LEFT, 0.985,
             "ADRB2 orthosteric pose grid — 5 ligand chemistries x 4 co-folders",
             fontsize=12, ha="left", va="top", fontweight="bold", color="#111")
    fig.text(LEFT, 0.955,
             "Reference: ADRB2 · 2RH1 (inactive, carazolol). Grey sticks = carazolol reference ligand · cyan cloud + sticks = "
             "pocket residues (BW 3.32/3.36/3.37/5.42/5.46/6.48/6.51/6.55/7.39/7.43). Green sticks = predicted ligand from each "
             "backbone after Kabsch alignment on pocket Cα. Predictions from Block-C _probe_stage.",
             ha="left", va="top", fontsize=7, color="#444", wrap=True)

    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig5_pose_grid.{ext}")
    plt.close(fig)


if __name__ == "__main__":
    figure5()
    print(f"OK — wrote fig5_pose_grid to {OUT}")
