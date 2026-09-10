"""
Side-quest — Nat Struct Biol level figure suite for the 48-receptor panel.

Inputs:
    refs/reference_set.csv     — precomputed discriminator metrics per PDB
    refs/gpcr_coupling.csv     — panel class assignment (A / B / F)
    refs/cache/rcsb/*.cif      — cached RCSB structures for Cα-trace overlays

Outputs (artefacts/side_figures_2026_09_06/):
    fig1_class_conditional_landscape.pdf/png   — 6-panel discriminator landscape
    fig2_structural_overlays.pdf/png           — Cα-trace overlays per class
    fig3_two_instrument_scatter.pdf/png        — class-conditional predicate map
    stats_effect_sizes.csv                     — Cohen's d / AUC per metric per class
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json

from Bio.PDB import MMCIFParser

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parents[1]
REF_CSV = REPO / "refs" / "reference_set.csv"
CPL_CSV = REPO / "refs" / "gpcr_coupling.csv"
CIF_DIR = REPO / "refs" / "cache" / "rcsb"
OUT = REPO / "artefacts" / "side_figures_2026_09_06"
OUT.mkdir(parents=True, exist_ok=True)


# ------------------------------ style ------------------------------------
def apply_style() -> None:
    """Nature-family visual defaults."""
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8,
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "axes.linewidth": 0.75,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "legend.fontsize": 7,
        "legend.frameon": False,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.bbox": "tight",
        "savefig.dpi": 300,
    })


PALETTE = {
    "active":   "#C1272D",      # brick red — active/agonist-bound
    "inactive": "#345995",      # deep blue — inactive/antagonist-bound
    "A":        "#2E7D32",      # class A — dark green
    "B":        "#EF6C00",      # class B — orange
    "F":        "#6A1B9A",      # class F — purple
}


# ---------------------------- data loading -------------------------------
def load_panel() -> pd.DataFrame:
    ref = pd.read_csv(REF_CSV)
    cpl = pd.read_csv(CPL_CSV)[["receptor_slug", "panel_extension_source", "primary_ga_class"]]

    def cls(row) -> str:
        if row["panel_extension_source"] == "class_a_original":
            return "A"
        if row["receptor_slug"] in ("GLP1R", "GCGR", "PTH1R", "CRHR1"):
            return "B"
        return "F"

    cpl["class"] = cpl.apply(cls, axis=1)
    panel = cpl["receptor_slug"].tolist()
    df = ref[ref["receptor_slug"].isin(panel)].merge(
        cpl[["receptor_slug", "class", "primary_ga_class"]], on="receptor_slug"
    )
    df = df[df["role"].isin(("active", "inactive"))].copy()
    return df


# ---------------------------- statistics ---------------------------------
def cohens_d(a: np.ndarray, b: np.ndarray) -> float:
    """Standardised mean diff — Hedge-uncorrected; pooled sd."""
    a = a[np.isfinite(a)]
    b = b[np.isfinite(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    na, nb = len(a), len(b)
    va, vb = a.var(ddof=1), b.var(ddof=1)
    s = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if s == 0:
        return np.nan
    return (a.mean() - b.mean()) / s


def auc_mannwhitney(active: np.ndarray, inactive: np.ndarray) -> float:
    """ROC-AUC via ranks — how well the metric separates active from inactive."""
    a = active[np.isfinite(active)]
    b = inactive[np.isfinite(inactive)]
    if len(a) < 2 or len(b) < 2:
        return np.nan
    x = np.concatenate([a, b])
    r = pd.Series(x).rank().values
    ra = r[:len(a)].sum()
    u = ra - len(a) * (len(a) + 1) / 2.0
    return u / (len(a) * len(b))


METRICS = [
    ("d_npxxy_oh_ref",        "NPxxY-OH (Å)",         "A"),
    ("d_gpcrdb_tm6_tilt_ref", "GPCRdb TM6 tilt (Å)",  "ABF"),
    ("d_r350_r630_ca_ref",    "3.50–6.30 Cα (Å)",     "ABF"),
    ("angle_class_b_kink_ref","TM6 kink (°)",         "B"),
    ("d_dry_ref",             "DRY salt-bridge (Å)",  "A"),
    ("d_tm5_out_ref",         "TM5 outward (Å)",      "A"),
    ("d_y558_pack_ref",       "Y7.53 packing (Å)",    "A"),
]


def build_effect_sizes(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col, label, applies in METRICS:
        for cls in ("A", "B", "F"):
            if cls not in applies:
                continue
            sub = df[df["class"] == cls]
            a = sub[sub["role"] == "active"][col].values
            i = sub[sub["role"] == "inactive"][col].values
            rows.append({
                "metric": col,
                "label": label,
                "class": cls,
                "n_active": int(np.isfinite(a).sum()),
                "n_inactive": int(np.isfinite(i).sum()),
                "mean_active": float(np.nanmean(a)) if len(a) else np.nan,
                "mean_inactive": float(np.nanmean(i)) if len(i) else np.nan,
                "cohens_d": cohens_d(a, i),
                "auc": auc_mannwhitney(a, i),
            })
    return pd.DataFrame(rows)


# ---------------------------- figure 1 -----------------------------------
def _swarm(ax, values, x, color, jitter=0.12, alpha=0.75, size=14):
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    rng = np.random.default_rng(hash(f"{x}-{color}") & 0xFFFF)
    jx = rng.uniform(-jitter, jitter, size=v.size)
    ax.scatter(np.full_like(v, x) + jx, v, s=size, c=color,
               edgecolors="white", linewidths=0.4, alpha=alpha, zorder=3)


def _box(ax, values, x, color, width=0.55):
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return
    q1, med, q3 = np.percentile(v, [25, 50, 75])
    ax.add_patch(mpl.patches.Rectangle(
        (x - width/2, q1), width, q3 - q1,
        fill=True, facecolor=color, alpha=0.18,
        edgecolor=color, linewidth=0.9, zorder=2))
    ax.plot([x - width/2, x + width/2], [med, med],
            color=color, lw=1.4, zorder=4, solid_capstyle="round")


def _pair(ax, sub, col, x_active=0, x_inactive=1, jitter=0.11):
    a = sub[sub["role"] == "active"][col].values
    i = sub[sub["role"] == "inactive"][col].values
    _box(ax, i, x_inactive, PALETTE["inactive"])
    _box(ax, a, x_active,   PALETTE["active"])
    _swarm(ax, i, x_inactive, PALETTE["inactive"], jitter=jitter)
    _swarm(ax, a, x_active,   PALETTE["active"],   jitter=jitter)
    ax.set_xticks([x_active, x_inactive])
    ax.set_xticklabels(["active", "inactive"])
    ax.set_xlim(-0.6, 1.6)


def _annotate_d(ax, sub, col):
    a = sub[sub["role"] == "active"][col].values
    i = sub[sub["role"] == "inactive"][col].values
    d = cohens_d(a, i)
    auc = auc_mannwhitney(a, i)
    if np.isfinite(d):
        ax.text(0.98, 0.97,
                f"d = {d:+.2f}\nAUC = {auc:.2f}\nn = {np.isfinite(a).sum()}/{np.isfinite(i).sum()}",
                transform=ax.transAxes, ha="right", va="top", fontsize=6.5,
                color="#333", family="monospace")


def figure1(df: pd.DataFrame, es: pd.DataFrame) -> None:
    fig = plt.figure(figsize=(7.2, 6.4))
    gs = fig.add_gridspec(3, 3, hspace=0.65, wspace=0.55,
                          left=0.07, right=0.99, top=0.94, bottom=0.07)

    # ---- Panel A — NPxxY-OH (Class A only, the class-A activation gate)
    ax = fig.add_subplot(gs[0, 0])
    sub = df[df["class"] == "A"]
    _pair(ax, sub, "d_npxxy_oh_ref")
    ax.set_ylabel("Distance (Å)")
    ax.set_title("a  NPxxY-OH (Class A)", loc="left", fontweight="bold")
    _annotate_d(ax, sub, "d_npxxy_oh_ref")

    # ---- Panel B — GPCRdb TM6 tilt (three classes side-by-side)
    ax = fig.add_subplot(gs[0, 1:])
    positions = {"A": (0, 1), "B": (2.4, 3.4), "F": (4.8, 5.8)}
    d_by_cls = {}
    for cls, (xa, xi) in positions.items():
        sub = df[df["class"] == cls]
        _box(ax, sub[sub["role"] == "inactive"]["d_gpcrdb_tm6_tilt_ref"].values,
             xi, PALETTE["inactive"])
        _box(ax, sub[sub["role"] == "active"]["d_gpcrdb_tm6_tilt_ref"].values,
             xa, PALETTE["active"])
        _swarm(ax, sub[sub["role"] == "inactive"]["d_gpcrdb_tm6_tilt_ref"].values,
               xi, PALETTE["inactive"])
        _swarm(ax, sub[sub["role"] == "active"]["d_gpcrdb_tm6_tilt_ref"].values,
               xa, PALETTE["active"])
        d_by_cls[cls] = cohens_d(
            sub[sub["role"] == "active"]["d_gpcrdb_tm6_tilt_ref"].values,
            sub[sub["role"] == "inactive"]["d_gpcrdb_tm6_tilt_ref"].values)
    ax.set_xticks([0.5, 2.9, 5.3])
    ax.set_xticklabels(["Class A", "Class B", "Class F"])
    ax.set_ylabel("2×46 – 6×37 Cα distance (Å)")
    ax.set_title("b  GPCRdb TM6 tilt — cross-class", loc="left", fontweight="bold")
    # place d annotations BELOW the x-axis line, well clear of the title
    for cls, (xa, xi) in positions.items():
        ax.text((xa + xi) / 2, -0.14,
                f"d = {d_by_cls[cls]:+.2f}", ha="center", va="top",
                transform=ax.get_xaxis_transform(),
                fontsize=6.5, color="#333", family="monospace")
    handles = [plt.Line2D([], [], marker="o", ls="", color=PALETTE["active"],
                          markeredgecolor="white", label="active"),
               plt.Line2D([], [], marker="o", ls="", color=PALETTE["inactive"],
                          markeredgecolor="white", label="inactive")]
    ax.legend(handles=handles, loc="lower right", ncol=2, handletextpad=0.2)

    # ---- Panel C — Class B kink
    ax = fig.add_subplot(gs[1, 0])
    sub = df[df["class"] == "B"]
    _pair(ax, sub, "angle_class_b_kink_ref")
    ax.set_ylabel("Angle (°)")
    ax.set_title("c  TM6 kink (Class B)", loc="left", fontweight="bold")
    _annotate_d(ax, sub, "angle_class_b_kink_ref")

    # ---- Panel D — DRY salt bridge (Class A canonical ionic lock)
    ax = fig.add_subplot(gs[1, 1])
    sub = df[df["class"] == "A"]
    _pair(ax, sub, "d_dry_ref")
    ax.set_ylabel("Distance (Å)")
    ax.set_title("d  DRY ionic lock (Class A)", loc="left", fontweight="bold")
    _annotate_d(ax, sub, "d_dry_ref")

    # ---- Panel E — TM5 outward (Class A)
    ax = fig.add_subplot(gs[1, 2])
    sub = df[df["class"] == "A"]
    _pair(ax, sub, "d_tm5_out_ref")
    ax.set_ylabel("Distance (Å)")
    ax.set_title("e  TM5 outward (Class A)", loc="left", fontweight="bold")
    _annotate_d(ax, sub, "d_tm5_out_ref")

    # ---- Panel F — effect-size heatmap
    ax = fig.add_subplot(gs[2, :])
    pivot = es.pivot_table(index="label", columns="class", values="cohens_d")
    order = [lab for _, lab, _ in METRICS if lab in pivot.index]
    pivot = pivot.reindex(order)
    pivot = pivot.reindex(columns=["A", "B", "F"])
    vmax = np.nanmax(np.abs(pivot.values))
    im = ax.imshow(pivot.values, aspect="auto",
                   cmap="RdBu_r", vmin=-vmax, vmax=+vmax)
    ax.set_xticks(range(pivot.shape[1]))
    ax.set_xticklabels([f"Class {c}" for c in pivot.columns])
    ax.set_yticks(range(pivot.shape[0]))
    ax.set_yticklabels(pivot.index)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            v = pivot.values[i, j]
            if np.isfinite(v):
                ax.text(j, i, f"{v:+.2f}", ha="center", va="center",
                        color="white" if abs(v) > vmax * 0.55 else "black",
                        fontsize=7)
            else:
                ax.text(j, i, "—", ha="center", va="center",
                        color="#888", fontsize=8)
    cbar = fig.colorbar(im, ax=ax, shrink=0.7, pad=0.02)
    cbar.set_label("Cohen's d  (active − inactive)")
    ax.set_title("f  Effect size (Cohen's d) — active vs inactive, by class",
                 loc="left", fontweight="bold")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.suptitle(
        "Class-conditional discriminators of GPCR activation "
        f"(panel of record — {df['receptor_slug'].nunique()} receptors, "
        f"{len(df)} reference structures)",
        fontsize=9.5, y=0.995, x=0.02, ha="left", fontweight="bold",
    )
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig1_class_conditional_landscape.{ext}")
    plt.close(fig)


# ---------------------------- figure 2 -----------------------------------
@dataclass
class Trace:
    coords: np.ndarray  # (N, 3) Cα
    resids: np.ndarray  # (N,) integer resids


def load_ca_trace(pdb_id: str, resid_lo: int | None = None,
                  resid_hi: int | None = None) -> Trace | None:
    """Load Cα coordinates for the receptor chain (highest CA count),
    optionally trimmed to [resid_lo, resid_hi]."""
    path = CIF_DIR / f"pdb_{pdb_id.lower()}.cif"
    if not path.exists():
        return None
    parser = MMCIFParser(QUIET=True)
    struc = parser.get_structure(pdb_id, str(path))
    model = next(iter(struc))
    best: tuple[list[np.ndarray], list[int]] | None = None
    for ch in model:
        cas: list[np.ndarray] = []
        rids: list[int] = []
        for res in ch:
            if res.id[0] != " ":       # skip HETATM / water
                continue
            if "CA" not in res:
                continue
            rid = res.id[1]
            if resid_lo is not None and rid < resid_lo:
                continue
            if resid_hi is not None and rid > resid_hi:
                continue
            cas.append(res["CA"].coord)
            rids.append(rid)
        if len(cas) < 100:
            continue
        if best is None or len(cas) > len(best[0]):
            best = (cas, rids)
    if best is None:
        return None
    return Trace(coords=np.asarray(best[0]), resids=np.asarray(best[1]))


def anchors_for(pdb_id: str, ref_df: pd.DataFrame) -> dict[str, int] | None:
    """Return BW→resid map for this PDB from reference_set.csv."""
    row = ref_df[ref_df["pdb_id"] == pdb_id]
    if row.empty:
        return None
    try:
        return {k: int(v) for k, v in json.loads(row.iloc[0]["anchor_positions"]).items()}
    except Exception:
        return None


def align_traces(mobile: Trace, target: Trace) -> Trace:
    """Superimpose `mobile` onto `target` using shared Cα by resid."""
    common = np.intersect1d(mobile.resids, target.resids)
    if len(common) < 30:
        return mobile
    tmask = np.isin(target.resids, common)
    mmask = np.isin(mobile.resids, common)
    # Kabsch on the shared subset
    A = mobile.coords[mmask]
    B = target.coords[tmask]
    ca = A.mean(0); cb = B.mean(0)
    A0 = A - ca; B0 = B - cb
    H = A0.T @ B0
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    aligned = (mobile.coords - ca) @ R.T + cb
    return Trace(coords=aligned, resids=mobile.resids)


def _principal_axes(coords: np.ndarray) -> np.ndarray:
    """Return orthonormal frame with axis 0 = long axis (7TM bundle)."""
    c = coords - coords.mean(0)
    cov = np.cov(c.T)
    w, v = np.linalg.eigh(cov)
    # eigenvectors sorted ascending → reverse so principal is first
    return v[:, ::-1]


def draw_overlay(ax, active_pdb: str, inactive_pdb: str, title: str,
                 ref_df: pd.DataFrame,
                 view: tuple[float, float] = (12, -60)) -> None:
    """Overlay active vs inactive Cα trace, trimmed to the 7TM bundle.

    Trimming uses the BW anchor range in reference_set.csv (min − 30 to max + 15)
    so ECDs, fusion partners, and long ICL3 loops don't dominate. TM6
    (6.30 → 7.53−10) is highlighted with a thicker overlay in each state.
    """
    a_anch = anchors_for(active_pdb,   ref_df)
    i_anch = anchors_for(inactive_pdb, ref_df)
    if a_anch is None or i_anch is None:
        ax.set_title(f"{title}\n(no anchor row)")
        ax.set_axis_off()
        return
    a_lo, a_hi = min(a_anch.values()) - 30, max(a_anch.values()) + 15
    i_lo, i_hi = min(i_anch.values()) - 30, max(i_anch.values()) + 15

    a = load_ca_trace(active_pdb,   a_lo, a_hi)
    i = load_ca_trace(inactive_pdb, i_lo, i_hi)
    if a is None or i is None:
        ax.set_title(f"{title}\n(missing CIF)")
        ax.set_axis_off()
        return

    # Align in original resid space — assumes shared numbering for the receptor
    # chain. Where sequences differ slightly, drop resids that aren't in both.
    common = np.intersect1d(a.resids, i.resids)
    if len(common) < 80:
        ax.set_title(f"{title}\n(few shared residues: {len(common)})")
        ax.set_axis_off()
        return
    a_trim = Trace(a.coords[np.isin(a.resids, common)], common)
    i_trim = Trace(i.coords[np.isin(i.resids, common)], common)
    a_trim = align_traces(a_trim, i_trim)

    # orient the receptor so the membrane axis is roughly vertical
    frame = _principal_axes(i_trim.coords)
    a_coords = (a_trim.coords - i_trim.coords.mean(0)) @ frame
    i_coords = (i_trim.coords - i_trim.coords.mean(0)) @ frame

    def tm6_slice(pdb_anch: dict[str, int]) -> np.ndarray:
        lo, hi = pdb_anch["6.30"], pdb_anch["7.53"] - 8
        return (common >= lo) & (common <= hi)

    tm6_mask = tm6_slice(i_anch)     # use inactive anchors, common set

    for xyz, colour, lbl in [
        (i_coords, PALETTE["inactive"], f"inactive {inactive_pdb}"),
        (a_coords, PALETTE["active"],   f"active {active_pdb}"),
    ]:
        # base trace — muted
        ax.plot(xyz[:, 0], xyz[:, 1], xyz[:, 2],
                color=colour, lw=1.0, alpha=0.55,
                solid_capstyle="round")
        # TM6 highlight — bolder
        tm6 = xyz[tm6_mask]
        if tm6.size:
            ax.plot(tm6[:, 0], tm6[:, 1], tm6[:, 2],
                    color=colour, lw=2.4, alpha=0.95,
                    label=lbl, solid_capstyle="round")
        else:
            ax.plot([], [], color=colour, lw=2.4, label=lbl)

    # anchor Cα markers: 3.50 (base of TM3), 6.30 (TM6 cytoplasmic end)
    for pos_key, mkr in (("3.50", "s"), ("6.30", "^")):
        rid = i_anch[pos_key]
        if rid in common:
            k = int(np.where(common == rid)[0][0])
            for xyz, colour in [(i_coords, PALETTE["inactive"]),
                                (a_coords, PALETTE["active"])]:
                ax.scatter(*xyz[k], s=22, c=colour, marker=mkr,
                           edgecolors="white", linewidths=0.7, zorder=6)

    pts = np.vstack([a_coords, i_coords])
    span = np.percentile(np.linalg.norm(pts - pts.mean(0), axis=1), 98)
    for setter in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        setter(-span, span)
    try:
        ax.set_box_aspect((1, 1, 1))
    except Exception:
        pass
    ax.set_title(title, pad=1, fontweight="bold", fontsize=8)
    elev, azim = view
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.04),
              ncol=2, handletextpad=0.3, fontsize=6.2)


def figure2(df: pd.DataFrame) -> None:
    """Cα overlays for two exemplars per class — one panel per exemplar."""
    picks = [
        ("Class A · 5HT2C (serotonin 2C)",     "8DPF", "6BQH"),
        ("Class A · DRD2 (dopamine D2)",       "7JVR", "6CM4"),
        ("Class A · CNR2 (CB2 cannabinoid)",   "8GUR", "5ZTY"),
        ("Class A · OPRK (κ-opioid)",          "8FEG", "4DJH"),
        ("Class B · GLP1R (glucagon-like 1)",  "6X18", "5VEW"),
        ("Class F · SMO (smoothened)",         "6XBL", "4JKV"),
    ]
    ref_df = pd.read_csv(REF_CSV)
    fig = plt.figure(figsize=(7.2, 5.4))
    for k, (title, act, ina) in enumerate(picks):
        ax = fig.add_subplot(2, 3, k + 1, projection="3d")
        draw_overlay(ax, act, ina, title, ref_df)
    fig.subplots_adjust(left=0.0, right=1.0, top=0.87, bottom=0.02,
                        hspace=0.25, wspace=0.02)
    fig.suptitle(
        "Cα-trace overlays — TM6 outward opening across three GPCR classes",
        fontsize=10, y=0.985, x=0.02, ha="left", fontweight="bold",
    )
    # subtitle / legend key just below the suptitle, above the panels
    fig.text(0.02, 0.955,
             "Bold segment: TM6 cytoplasmic half (Cα 6.30 to 7.53-8). "
             "Squares mark Cα 3.50; triangles mark Cα 6.30. "
             "Aligned on shared receptor Cα (fusion partners, ECDs and long "
             "ICL3 loops trimmed).",
             ha="left", va="top", fontsize=6.8, color="#333")
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig2_structural_overlays.{ext}")
    plt.close(fig)


# ---------------------------- figure 3 -----------------------------------
def figure3(df: pd.DataFrame) -> None:
    """The class-conditional two-instrument scatter — NPxxY vs TM6 tilt.
    Illustrates why the predicate had to be split by class (§15 cleanup).
    """
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 2.9),
                             gridspec_kw={"wspace": 0.35})
    axes = list(axes)
    class_labels = [
        ("A", "Class A  —  NPxxY  +  TM6 tilt"),
        ("B", "Class B  —  kink  +  TM6 tilt"),
        ("F", "Class F  —  TM6 tilt only"),
    ]
    ymetrics = {
        "A": ("d_npxxy_oh_ref",        "NPxxY-OH (Å)"),
        "B": ("angle_class_b_kink_ref","TM6 kink (°)"),
        "F": ("d_r350_r630_ca_ref",    "3.50–6.30 Cα (Å)"),
    }
    xcol = "d_gpcrdb_tm6_tilt_ref"

    for ax, (cls, title) in zip(axes, class_labels):
        sub = df[df["class"] == cls]
        ycol, ylabel = ymetrics[cls]
        for role in ("inactive", "active"):
            r = sub[sub["role"] == role]
            ax.scatter(r[xcol], r[ycol],
                       s=32, c=PALETTE[role],
                       edgecolors="white", linewidths=0.5, alpha=0.9,
                       label=role, zorder=3)
        # decision-boundary shading — inactive quadrant vs active quadrant
        # class F has only the x-axis, so shade single-axis
        if cls == "F":
            xa = sub[sub["role"] == "active"][xcol].dropna()
            xi = sub[sub["role"] == "inactive"][xcol].dropna()
            if len(xa) and len(xi):
                thr = (xa.mean() + xi.mean()) / 2
                ax.axvline(thr, ls="--", lw=0.8, color="#666", zorder=1)
        else:
            xa = sub[sub["role"] == "active"][xcol].dropna()
            xi = sub[sub["role"] == "inactive"][xcol].dropna()
            ya = sub[sub["role"] == "active"][ycol].dropna()
            yi = sub[sub["role"] == "inactive"][ycol].dropna()
            if len(xa) and len(xi):
                thr_x = (xa.mean() + xi.mean()) / 2
                ax.axvline(thr_x, ls="--", lw=0.8, color="#666", zorder=1)
            if len(ya) and len(yi):
                thr_y = (ya.mean() + yi.mean()) / 2
                ax.axhline(thr_y, ls="--", lw=0.8, color="#666", zorder=1)
        # label off-signature points only — receptors on the "wrong" side of
        # their class boundary read as interesting; the dense agonist / apo
        # clusters would just be a wall of text.
        for _, r in sub.iterrows():
            x, y = r[xcol], r[ycol]
            if pd.isna(x) or pd.isna(y):
                continue
            interesting = False
            if r["role"] == "active":
                if cls == "F":
                    interesting = x < (thr if 'thr' in dir() else 0)  # rare, but keep
                else:
                    # active but NOT below y-threshold and above x-threshold
                    interesting = not (x > thr_x and y < thr_y if cls == "A"
                                       else x > thr_x and y > thr_y)
            else:
                if cls == "F":
                    interesting = x > (thr if 'thr' in dir() else 999)
                else:
                    interesting = not (x < thr_x and (y > thr_y if cls == "A"
                                                     else y < thr_y))
            # also always label class B / F points since they're sparse
            if cls in ("B", "F"):
                interesting = True
            if interesting:
                ax.annotate(r["receptor_slug"], (x, y),
                            fontsize=5.2, color="#333", alpha=0.85,
                            xytext=(3, 2), textcoords="offset points")
        ax.set_xlabel("GPCRdb TM6 tilt (Å)")
        ax.set_ylabel(ylabel)
        ax.set_title(title, loc="left", fontweight="bold", pad=2)
        if cls == "A":
            ax.legend(loc="best", handletextpad=0.2)
    fig.suptitle(
        "Class-conditional two-instrument predicate — why one axis will not do",
        fontsize=9.5, y=1.02, x=0.02, ha="left", fontweight="bold",
    )
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig3_two_instrument_scatter.{ext}")
    plt.close(fig)


# ------------------------------ main -------------------------------------
def main() -> None:
    apply_style()
    df = load_panel()
    es = build_effect_sizes(df)
    es.to_csv(OUT / "stats_effect_sizes.csv", index=False)
    figure1(df, es)
    figure3(df)
    figure2(df)
    print(f"OK — {len(df)} rows, wrote to {OUT}")


if __name__ == "__main__":
    main()
