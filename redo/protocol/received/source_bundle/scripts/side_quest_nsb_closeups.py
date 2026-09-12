"""
Side-quest #2 — Nat Struct Biol style activation-switch close-ups.

The trick: render the backbone as a *pre-rasterised, Gaussian-blurred* image
in the background, then overlay sharp ball-and-stick side chains on top.  This
gives the authentic depth-of-field look that molecular graphics people spend
hours in PyMOL to fake — done here in pure matplotlib + scipy.

Outputs (artefacts/side_figures_2026_09_06/):
    fig4_switch_closeups.{pdf,png}
"""
from __future__ import annotations

import io
import json
import warnings
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Bio.PDB import MMCIFParser
from scipy.ndimage import gaussian_filter

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parents[1]
REF_CSV = REPO / "refs" / "reference_set.csv"
CIF_DIR = REPO / "refs" / "cache" / "rcsb"
OUT = REPO / "artefacts" / "side_figures_2026_09_06"
OUT.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 8,
    "axes.titlesize": 9.5,
    "axes.linewidth": 0.6,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "savefig.bbox": "tight",
    "savefig.dpi": 350,
})

ELEMENT_COLOR = {
    "C": "#3B3B3B",
    "N": "#3D6BB3",
    "O": "#C1272D",
    "S": "#E5B008",
    "P": "#E76F00",
    "H": "#E5E5E5",
}
ELEMENT_R = {
    "C": 1.7, "N": 1.55, "O": 1.52, "S": 1.8, "P": 1.8, "H": 1.1,
}
STATE_TINT = {
    "inactive": "#345995",
    "active":   "#C1272D",
}
BB_ATOMS = {"N", "CA", "C", "O"}


# ---------------------------- IO -----------------------------------------
@dataclass
class Atom:
    name: str
    element: str
    coord: np.ndarray
    resid: int
    resname: str


def load_atoms(pdb_id: str) -> list[Atom]:
    path = CIF_DIR / f"pdb_{pdb_id.lower()}.cif"
    parser = MMCIFParser(QUIET=True)
    struc = parser.get_structure(pdb_id, str(path))
    model = next(iter(struc))
    best: list[Atom] = []
    for ch in model:
        atoms: list[Atom] = []
        for res in ch:
            if res.id[0] != " " or res.get_resname() == "HOH":
                continue
            for a in res:
                elem = (a.element or a.get_name()[0]).strip().upper()
                atoms.append(Atom(
                    name=a.get_name(),
                    element=elem,
                    coord=np.asarray(a.coord, float),
                    resid=res.id[1],
                    resname=res.get_resname(),
                ))
        if len(atoms) > len(best):
            best = atoms
    return best


def ca_of(atoms: list[Atom]) -> tuple[np.ndarray, np.ndarray]:
    ca = [a for a in atoms if a.name == "CA"]
    return (np.asarray([x.coord for x in ca]),
            np.asarray([x.resid for x in ca]))


def anchors(pdb_id: str, ref_df: pd.DataFrame) -> dict[str, int]:
    row = ref_df[ref_df["pdb_id"] == pdb_id].iloc[0]
    return {k: int(v) for k, v in json.loads(row["anchor_positions"]).items()}


# --------------------------- geometry ------------------------------------
def kabsch(mobile: np.ndarray, target: np.ndarray,
           mobile_ids: np.ndarray, target_ids: np.ndarray
           ) -> tuple[np.ndarray, np.ndarray]:
    common = np.intersect1d(mobile_ids, target_ids)
    A = mobile[np.isin(mobile_ids, common)]
    B = target[np.isin(target_ids, common)]
    ca, cb = A.mean(0), B.mean(0)
    H = (A - ca).T @ (B - cb)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    t = cb - ca @ R.T
    return R, t


def apply_rt(x: np.ndarray, R: np.ndarray, t: np.ndarray) -> np.ndarray:
    return x @ R.T + t


def orient_frame(motif_coords: np.ndarray, all_ca: np.ndarray) -> np.ndarray:
    """Return a 3x3 rotation that puts the motif's principal axis on x
    and the receptor's long axis on y — so the projected plane looks
    like the classic 'side view of TM6' close-up."""
    # long axis of the whole bundle → new y
    ca0 = all_ca - all_ca.mean(0)
    _, v_all = np.linalg.eigh(np.cov(ca0.T))
    long_axis = v_all[:, -1]

    # local axis around the motif → in the plane
    m0 = motif_coords - motif_coords.mean(0)
    _, v_m = np.linalg.eigh(np.cov(m0.T))
    motif_axis = v_m[:, -1]

    # build orthonormal frame (x, y, z) — y = long_axis, x ⊥ y in-plane
    y = long_axis / np.linalg.norm(long_axis)
    x = motif_axis - (motif_axis @ y) * y
    if np.linalg.norm(x) < 1e-6:
        x = np.array([1.0, 0.0, 0.0])
    x = x / np.linalg.norm(x)
    z = np.cross(x, y)
    return np.stack([x, y, z], axis=1)     # columns are basis vectors


# --------------------------- rendering -----------------------------------
def blurred_backbone(ax, ca2d: np.ndarray, colour: str,
                     xlim: tuple[float, float], ylim: tuple[float, float],
                     depth: np.ndarray | None = None,
                     sigma: float = 6.0, base_alpha: float = 0.85) -> None:
    """Rasterise a Cα trace into a small image, Gaussian-blur it,
    and imshow it under the sharp overlays. Real depth-of-field."""
    # canvas resolution
    W, H = 900, 900
    xs = (ca2d[:, 0] - xlim[0]) / (xlim[1] - xlim[0]) * (W - 1)
    ys = (ca2d[:, 1] - ylim[0]) / (ylim[1] - ylim[0]) * (H - 1)
    # rasterise as a polyline into a scalar canvas
    canvas = np.zeros((H, W), float)
    for k in range(len(xs) - 1):
        n = int(max(4, np.hypot(xs[k+1] - xs[k], ys[k+1] - ys[k]) * 1.4))
        t = np.linspace(0, 1, n)
        u = xs[k] + t * (xs[k+1] - xs[k])
        v = ys[k] + t * (ys[k+1] - ys[k])
        iu = np.clip(u.astype(int), 0, W - 1)
        iv = np.clip(v.astype(int), 0, H - 1)
        weight = 1.0 if depth is None else (1.0 - 0.4 *
                    (depth[k] - depth.min()) / (depth.max() - depth.min() + 1e-9))
        np.add.at(canvas, (iv, iu), weight)
    # heavy Gaussian blur → DOF
    blurred = gaussian_filter(canvas, sigma=sigma)
    if blurred.max() > 0:
        blurred = blurred / blurred.max()
    # convert to RGBA with the state tint
    rgb = np.array(mpl.colors.to_rgb(colour))
    rgba = np.zeros((H, W, 4), float)
    rgba[..., :3] = rgb
    rgba[..., 3] = np.clip(blurred, 0, 1) ** 0.6 * base_alpha
    # NB origin='lower' so y increases upwards
    ax.imshow(rgba, extent=(*xlim, *ylim), origin="lower",
              interpolation="bilinear", zorder=1)


def draw_residue_2d(ax, atoms: list[Atom], proj: np.ndarray,
                    tint: str, alpha: float = 1.0,
                    ball_scale: float = 1.0,
                    label: str | None = None,
                    label_offset: tuple[float, float] = (0.3, 0.9)) -> tuple[float, float] | None:
    """Draw one residue as CPK sticks + balls with a state-tinted shadow."""
    if not atoms:
        return None
    xy = proj[:, :2]
    depth = proj[:, 2]

    # bonds — intra-residue only, < 1.9 Å
    for i in range(len(atoms)):
        for j in range(i + 1, len(atoms)):
            if np.linalg.norm(atoms[i].coord - atoms[j].coord) > 1.9:
                continue
            ci = ELEMENT_COLOR.get(atoms[i].element, "#666")
            cj = ELEMENT_COLOR.get(atoms[j].element, "#666")
            mid = (xy[i] + xy[j]) / 2
            for p, q, col in [(xy[i], mid, ci), (mid, xy[j], cj)]:
                ax.plot([p[0], q[0]], [p[1], q[1]],
                        color=col, lw=2.2, alpha=alpha,
                        solid_capstyle="round", zorder=6)

    # atom balls — depth-scaled slight halo
    depth_norm = (depth - depth.min()) / max(1e-9, (depth.max() - depth.min()))
    for atom, (x, y), dn in zip(atoms, xy, depth_norm):
        col = ELEMENT_COLOR.get(atom.element, "#666")
        r = ELEMENT_R.get(atom.element, 1.5) * ball_scale
        s = np.pi * (r * 3.2) ** 2       # 5x smaller than v1 — reads clean
        # state-tinted outer halo so active vs inactive is readable
        ax.scatter(x, y, s=s * 1.9, c=tint, alpha=0.32 * alpha,
                   linewidths=0, zorder=6.5)
        ax.scatter(x, y, s=s, c=col, alpha=alpha,
                   edgecolors="white", linewidths=0.6, zorder=7)

    # label near the residue's Cα (or centroid)
    ca_idx = next((k for k, a in enumerate(atoms) if a.name == "CA"), 0)
    lx, ly = xy[ca_idx]
    if label:
        # place label on whichever side has more room in the panel
        xlo, xhi = ax.get_xlim()
        ha = "right" if lx > (xlo + xhi) / 2 else "left"
        dx = -label_offset[0] if ha == "right" else label_offset[0]
        ax.annotate(label, (lx, ly),
                    xytext=(dx, label_offset[1]), textcoords="offset points",
                    fontsize=6.6, color="#111", fontweight="bold",
                    ha=ha, va="bottom", clip_on=False,
                    bbox=dict(facecolor="white", edgecolor="#999",
                              alpha=0.9, boxstyle="round,pad=0.22",
                              linewidth=0.4),
                    zorder=9)
    return (lx, ly)


# --------------------------- close-ups -----------------------------------
@dataclass
class CloseUp:
    title: str
    subtitle: str
    active_pdb: str
    inactive_pdb: str
    residues: tuple[str, ...] = ("3.50", "6.30", "7.53", "5.58")
    span: float = 12.0             # ± span along projection axes (Å)
    y_shift: float = 0.0           # nudge camera along membrane axis
    x_shift: float = 0.0
    distance_pairs: list[tuple[str, str, str, str, str]] = field(default_factory=list)
    # (state, bw_a, atom_a, bw_b, atom_b) — a dashed line + Å label


CLOSEUPS: list[CloseUp] = [
    CloseUp(
        title="Class A · CNR2 (CB2 cannabinoid)",
        subtitle="R3.50 · D6.30 · Y7.53 — the canonical Class A switch",
        active_pdb="8GUR", inactive_pdb="5ZTY",
        residues=("3.50", "6.30", "7.53", "5.58"),
        span=11.0,
        distance_pairs=[
            ("inactive", "3.50", "CA", "6.30", "CA"),
        ],
    ),
    CloseUp(
        title="Class A · OPRK (κ-opioid)",
        subtitle="R3.50 – E/D6.30 salt-bridge breaks; Y7.53 rotates in",
        active_pdb="8FEG", inactive_pdb="4DJH",
        residues=("3.50", "6.30", "7.53", "5.58"),
        span=11.0,
        distance_pairs=[
            ("inactive", "3.50", "CA", "6.30", "CA"),
        ],
    ),
    CloseUp(
        title="Class B · GLP1R (glucagon-like peptide-1 R)",
        subtitle="TM6 hinge sharpens from ~160° to ~90° on activation",
        active_pdb="6X18", inactive_pdb="5VEW",
        residues=("3.50", "6.30", "6.34"),
        span=14.0,
        distance_pairs=[
            ("inactive", "3.50", "CA", "6.30", "CA"),
        ],
    ),
    CloseUp(
        title="Class F · SMO (Smoothened)",
        subtitle="Modest cytoplasmic TM6 opening — the only Class F switch that scores",
        active_pdb="6XBL", inactive_pdb="4JKV",
        residues=("3.50", "6.30", "7.53"),
        span=13.0,
        distance_pairs=[
            ("inactive", "3.50", "CA", "6.30", "CA"),
        ],
    ),
]


def render_closeup(ax, cu: CloseUp, ref_df: pd.DataFrame) -> None:
    a_atoms = load_atoms(cu.active_pdb)
    i_atoms = load_atoms(cu.inactive_pdb)
    a_ca, a_ids = ca_of(a_atoms)
    i_ca, i_ids = ca_of(i_atoms)

    # align active onto inactive on the full receptor Cα intersection
    R, t = kabsch(a_ca, i_ca, a_ids, i_ids)
    a_ca_al = apply_rt(a_ca, R, t)

    # anchor lookups
    a_anch = anchors(cu.active_pdb,   ref_df)
    i_anch = anchors(cu.inactive_pdb, ref_df)

    # centre & camera frame from the inactive motif
    motif_coords = np.stack([
        a.coord for a in i_atoms
        if a.name == "CA" and any(a.resid == i_anch.get(bw) for bw in cu.residues)
    ])
    centre = motif_coords.mean(0)
    F = orient_frame(motif_coords, i_ca)

    def project(c: np.ndarray) -> np.ndarray:
        return (c - centre) @ F        # (x, y, z=depth)

    # ---- Backbone: rasterise blurred glow (both states) --------------------
    i_ca_proj = project(i_ca)
    a_ca_proj = project(apply_rt(a_ca, R, t))
    x_lo, x_hi = -cu.span + cu.x_shift, cu.span + cu.x_shift
    y_lo, y_hi = -cu.span + cu.y_shift, cu.span + cu.y_shift

    # two-layer glow: wide halo + tighter mid-focus glow → real DOF feel
    blurred_backbone(ax, i_ca_proj, STATE_TINT["inactive"],
                     (x_lo, x_hi), (y_lo, y_hi),
                     depth=i_ca_proj[:, 2], sigma=9.0, base_alpha=0.30)
    blurred_backbone(ax, a_ca_proj, STATE_TINT["active"],
                     (x_lo, x_hi), (y_lo, y_hi),
                     depth=a_ca_proj[:, 2], sigma=9.0, base_alpha=0.30)
    blurred_backbone(ax, i_ca_proj, STATE_TINT["inactive"],
                     (x_lo, x_hi), (y_lo, y_hi),
                     depth=i_ca_proj[:, 2], sigma=3.2, base_alpha=0.55)
    blurred_backbone(ax, a_ca_proj, STATE_TINT["active"],
                     (x_lo, x_hi), (y_lo, y_hi),
                     depth=a_ca_proj[:, 2], sigma=3.2, base_alpha=0.55)

    # ---- Foreground residues -----------------------------------------------
    # look-up helper
    def residue_atoms(atoms: list[Atom], rid: int) -> list[Atom]:
        return [a for a in atoms if a.resid == rid]

    # inactive residues
    residue_ca_cache: dict[tuple[str, str], tuple[float, float]] = {}
    for state, atoms, anch, xform in [
        ("inactive", i_atoms, i_anch, (np.eye(3), np.zeros(3))),
        ("active",   a_atoms, a_anch, (R, t)),
    ]:
        R_local, t_local = xform
        for bw in cu.residues:
            if bw not in anch:
                continue
            rid = anch[bw]
            atoms_r = residue_atoms(atoms, rid)
            if not atoms_r:
                continue
            coords = np.stack([a.coord for a in atoms_r])
            coords = apply_rt(coords, R_local, t_local)
            proj = (coords - centre) @ F

            # residue label — only draw for inactive to avoid double-labeling
            resname = atoms_r[next(k for k, a in enumerate(atoms_r) if a.name == "CA")].resname
            label = f"{resname.title()}{rid} · {bw}" if state == "inactive" else None

            # tag class-B kink target with tint
            xy = draw_residue_2d(ax, atoms_r, proj,
                                 tint=STATE_TINT[state],
                                 alpha=0.98,
                                 ball_scale=1.0,
                                 label=label,
                                 label_offset=(6, 6))
            if xy is not None:
                residue_ca_cache[(state, bw)] = xy

    # ---- distance annotations ----------------------------------------------
    for state, bw_a, atom_a, bw_b, atom_b in cu.distance_pairs:
        atoms_src = i_atoms if state == "inactive" else a_atoms
        anch = i_anch if state == "inactive" else a_anch
        R_local, t_local = ((np.eye(3), np.zeros(3)) if state == "inactive"
                            else (R, t))
        if bw_a not in anch or bw_b not in anch:
            continue
        rid_a, rid_b = anch[bw_a], anch[bw_b]
        pa = next((a for a in atoms_src
                   if a.resid == rid_a and a.name == atom_a), None)
        pb = next((a for a in atoms_src
                   if a.resid == rid_b and a.name == atom_b), None)
        if pa is None or pb is None:
            continue
        ca_c = apply_rt(np.stack([pa.coord, pb.coord]), R_local, t_local)
        proj = (ca_c - centre) @ F
        d = np.linalg.norm(pa.coord - pb.coord)
        col = STATE_TINT[state]
        ax.plot(proj[:, 0], proj[:, 1], color=col, ls=(0, (2.5, 2)),
                lw=1.1, alpha=0.95, zorder=8)
        mid = proj.mean(0)
        # nudge label perpendicular to the line so it doesn't sit on top of
        # residue chips at either end
        vec = proj[1, :2] - proj[0, :2]
        n = np.array([-vec[1], vec[0]]) / max(1e-6, np.linalg.norm(vec))
        off = 0.75 * n
        ax.text(mid[0] + off[0], mid[1] + off[1], f"{d:.1f} Å (inactive)",
                fontsize=6.4, color=col, fontweight="bold",
                ha="center", va="center", zorder=9,
                bbox=dict(facecolor="white", edgecolor="none",
                          alpha=0.85, boxstyle="round,pad=0.15"))

    # ---- axis polish ------------------------------------------------------
    ax.set_xlim(x_lo, x_hi)
    ax.set_ylim(y_lo, y_hi)
    ax.set_aspect("equal", adjustable="box")
    ax.set_facecolor("#F7F5F0")   # warm off-white to give the glow contrast
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])

    # top-left title chip
    ax.text(0.02, 0.98, cu.title, transform=ax.transAxes,
            ha="left", va="top", fontweight="bold", fontsize=9,
            color="#111",
            bbox=dict(facecolor="white", edgecolor="#CCC",
                      alpha=0.92, boxstyle="round,pad=0.35",
                      linewidth=0.4))
    # top-right state legend (colored dots)
    ax.text(0.98, 0.98,
            f"inactive {cu.inactive_pdb}\nactive   {cu.active_pdb}",
            transform=ax.transAxes, ha="right", va="top", fontsize=6.3,
            color="#333", family="monospace",
            bbox=dict(facecolor="white", edgecolor="#CCC",
                      alpha=0.92, boxstyle="round,pad=0.3",
                      linewidth=0.4))
    # bottom-left subtitle (single line, less obtrusive)
    ax.text(0.02, 0.02, cu.subtitle, transform=ax.transAxes,
            ha="left", va="bottom", fontsize=6.5, color="#333",
            bbox=dict(facecolor="white", edgecolor="none",
                      alpha=0.85, boxstyle="round,pad=0.25"))


def figure4() -> None:
    ref_df = pd.read_csv(REF_CSV)
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 7.2),
                             gridspec_kw={"hspace": 0.06, "wspace": 0.06})
    for ax, cu in zip(axes.flat, CLOSEUPS):
        render_closeup(ax, cu, ref_df)
    fig.suptitle(
        "Activation-switch close-ups — CPK side chains, Gaussian-blurred Cα glow",
        fontsize=10, y=0.995, x=0.02, ha="left", fontweight="bold",
    )
    fig.text(0.02, 0.965,
             "Foreground: side chains in CPK (C grey · N blue · O red · S yellow). "
             "Background: full 7TM Cα trace of both states, rasterised and Gaussian-blurred "
             "(σ ≈ 7.5 px) — inactive (blue) vs active (red). Dashed lines are Cα–Cα "
             "distances between anchor residues.",
             ha="left", va="top", fontsize=6.7, color="#333")
    fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.02)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig4_switch_closeups.{ext}")
    plt.close(fig)


if __name__ == "__main__":
    figure4()
    print(f"OK — wrote fig4_switch_closeups to {OUT}")
