"""
Depth-of-field structure rendering in pure matplotlib.

Why this module exists. The PyMOL renders it replaces were correct and ugly:
a flat pale-grey cartoon on white, with the element carrying the claim only
slightly darker than the scaffold around it, every helix at the same apparent
distance from the camera, and the measured numbers exiled to a caption strip.
The technique here - taken from `figures/reference/side_quest_nsb_closeups.py`
- rasterises the Ca trace into a scalar canvas, Gaussian-blurs it, and lays it
under sharp vector sticks. That gives real depth of field, so the scaffold
recedes and the subject comes forward, and it keeps the output vector
everywhere except the one blurred backing layer.

Each function names the defect it prevents. They are not style preferences;
every one of them is a failure recorded in the corpus survey
(`figures/README.md`, `lit/RENDER_CONVENTIONS.md`) or a mistake made here and
fixed.

WHAT IS RASTER AND WHAT IS VECTOR
    Only the blurred backing images are raster, and they carry
    `set_rasterized(True)` so a PDF keeps everything else - sticks, dashes,
    values, atom-pair labels, scale bar - as vector text and paths. Call
    `raster_dpi(fig)` before saving so those images are written at print
    resolution rather than at the figure's 100 dpi default.

THE CAMERA IS NOT CHOSEN BY EYE
    `camera_frame()` imports `block_a/camera.py` rather than re-deriving the
    rule, so a matplotlib render and the PyMOL render of the same scene are
    the same viewpoint, and neither can be turned until a helix looks
    displaced. The projection here is orthographic where PyMOL's was a 20-deg
    perspective; that is the one deliberate difference, and it favours this
    module - a distance drawn across an orthographic projection is not
    foreshortened differently at the two ends.

GREY MEANS "NOT THE SUBJECT"
    The blurred backing is always neutral. State colour appears only on the
    element carrying the claim. Colouring a whole structure by which file it
    came from is the convention this field does NOT have (RENDER_CONVENTIONS
    s1), and it is what made the old renders unreadable: two receptors, two
    hues, and no way to see which part of either moved.
"""
import os
import sys

import numpy as np
from scipy.ndimage import gaussian_filter

import matplotlib as mpl
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "block_a"))

import camera as _camera                                      # noqa: E402
import cifread as CR                                          # noqa: E402


# --------------------------------------------------------------------------
# palette
# --------------------------------------------------------------------------
# CPK for the atoms themselves. The house palette (figstyle) governs the
# claim colours; CPK governs element identity, and mixing the two is what
# makes a stick figure unreadable - so the two vocabularies never overlap.
ELEMENT_COLOUR = {
    "C": "#3B3B3B", "N": "#3D6BB3", "O": "#B02418",
    "S": "#D9A404", "P": "#D96C00", "H": "#DDDDDD",
}
ELEMENT_R = {"C": 1.70, "N": 1.55, "O": 1.52, "S": 1.80, "P": 1.80, "H": 1.10}

PANEL_BG = "#F6F4F1"      # warm off-white; a pure-white ground gives the
                          # blurred layer nothing to be brighter than
SCAFFOLD = "#7C7770"      # the invariant bundle: grey, because it is not the
                          # subject - never because it is a reference


# --------------------------------------------------------------------------
# geometry
# --------------------------------------------------------------------------
class Frame(object):
    """An orthonormal camera basis plus the point it looks at.

    Prevents: a view chosen with a mouse. Two of the corpus's render defects
    are camera defects in disguise (part of the model cropped out of frame; a
    set of small multiples whose cells are not on one footing), and both are
    invisible in a caption. Here the basis is a stated rule over the
    coordinates and the same object drives every panel of a figure.
    """

    def __init__(self, right, up, out, centre, label):
        self.right = np.asarray(right, float)
        self.up = np.asarray(up, float)
        self.out = np.asarray(out, float)
        self.centre = np.asarray(centre, float)
        self.label = label

    def project(self, xyz):
        """(N,3) model coordinates -> (N,3) of (x, y, depth), all Angstrom.

        `depth` increases TOWARDS the viewer, because `out` is the camera's
        out axis. Every depth cue in this module assumes that sign; getting it
        backwards puts the far wall in focus and is invisible in the code.
        """
        d = np.atleast_2d(np.asarray(xyz, float)) - self.centre
        return np.stack([d @ self.right, d @ self.up, d @ self.out], axis=1)


def camera_frame(path, receptor_sel, tilt_anchors, view="side", ca=None):
    """Camera basis from `block_a/camera.py`'s rule - not re-derived here.

    Prevents: two renderers of the same scene disagreeing about the view. The
    membrane normal, the extracellular sign and the horizontal all come from
    the same functions the PyMOL path used, so the rule is written down in
    exactly one place.

    `ca` overrides the point cloud the bundle axis is fitted to, and it is not
    optional in practice. THE DEFECT IT FIXES: camera.py fits the first
    principal axis over every Ca in the receptor window, and DRD2's predicted
    ICL3 is 147 residues of mean-pLDDT-38.5 coil out of 414. Fitting through
    it tilts the "membrane normal" by 35.5 degrees, so the PyMOL side view of
    DRD2 is 35 degrees off the bundle axis and the alpha5 helix is drawn at an
    angle it does not have. camera.py's docstring already warns that this loop
    can flip the extracellular SIGN; it also bends the axis, and that had not
    been caught. Pass the same body the panel draws - 7TM minus ICL3 - and the
    view is the bundle's.
    """
    atoms = CR.frame(path)
    ch, lo, hi = receptor_sel
    if ca is None:
        ca = np.array([a["xyz"] for a in atoms
                       if a["name"] == "CA" and a["chain"] == ch
                       and lo <= a["resi"] <= hi and a["group"] == "ATOM"])
    ca = np.asarray(ca, float)
    if len(ca) < 20:
        raise ValueError("camera_frame: only %d CA in %s %s:%d-%d"
                         % (len(ca), os.path.basename(path), ch, lo, hi))
    p = np.array([CR.atom(atoms, c, r, "CA") for c, r in tilt_anchors])
    up_hint = _camera._extracellular_hint(atoms, ch, lo, hi, p)
    right, up, out, centre = _camera._basis(ca, up_hint, p[1] - p[0])
    if view == "side":
        return Frame(right, up, out, centre, "side view, extracellular up")
    if view == "cytoplasmic":
        # camera.cytoplasmic_view's rotation, verbatim: look up the bundle
        # from inside the cell, tilt axis still horizontal, so the two views
        # of a figure are one derivation and not two guesses.
        return Frame(right, out, -up, centre,
                     "view from the cytoplasm, up the bundle axis")
    raise ValueError("view must be 'side' or 'cytoplasmic'")


def ca_runs(atoms, chain, lo=None, hi=None):
    """Ca coordinates split into CONTIGUOUS runs of residue number.

    Prevents: a polyline drawn straight across a chain break. 2RH1 is modelled
    29-230 and 263-342 and 4LDE 1029-1231 and 1263-1342; a single polyline
    over either invents a 20 A helix through the middle of the receptor where
    ICL3 is disordered, and it is the blurred layer - the one that sets the
    whole shape of the panel - that would carry it.
    """
    ca = [(a["resi"], a["xyz"]) for a in atoms
          if a["name"] == "CA" and a["chain"] == chain and a["group"] == "ATOM"
          and (lo is None or a["resi"] >= lo) and (hi is None or a["resi"] <= hi)]
    ca.sort()
    runs, cur, prev = [], [], None
    for resi, xyz in ca:
        if prev is not None and resi != prev + 1:
            runs.append(np.asarray(cur))
            cur = []
        cur.append(xyz)
        prev = resi
    if cur:
        runs.append(np.asarray(cur))
    return [r for r in runs if len(r) >= 2]


def superpose(mobile_atoms, target_atoms, mobile_chain, target_chain,
              lo, hi, mobile_offset=0):
    """Kabsch fit of `mobile` onto `target` over shared Ca only.

    `lo`/`hi` are in TARGET numbering; `mobile_offset` is added to the target
    number to find the mobile residue (4LDE carries +1000, D21).

    Prevents: aligning a receptor onto a fusion partner. 2RH1's T4 lysozyme
    occupies 1002-1161 of the same chain as the receptor, so a selection
    written once and reused across both objects silently superposes the
    bundle onto the lysozyme (D21's practical trap). Matching residue by
    residue inside an explicit window makes that impossible.
    """
    def ca_map(atoms, chain):
        return dict((a["resi"], a["xyz"]) for a in atoms
                    if a["name"] == "CA" and a["chain"] == chain
                    and a["group"] == "ATOM")

    m, t = ca_map(mobile_atoms, mobile_chain), ca_map(target_atoms, target_chain)
    pairs = [(m[r + mobile_offset], t[r]) for r in range(lo, hi + 1)
             if (r + mobile_offset) in m and r in t]
    if len(pairs) < 30:
        raise ValueError("superpose: only %d shared Ca in %d-%d"
                         % (len(pairs), lo, hi))
    A = np.array([p[0] for p in pairs])
    B = np.array([p[1] for p in pairs])
    ca_, cb_ = A.mean(0), B.mean(0)
    H = (A - ca_).T @ (B - cb_)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    t_ = cb_ - ca_ @ R.T
    rms = float(np.sqrt((((A @ R.T + t_) - B) ** 2).sum(1).mean()))
    return R, t_, len(pairs), rms


def apply_rt(xyz, R, t):
    return np.atleast_2d(np.asarray(xyz, float)) @ R.T + t


def _spline(P, per=7):
    """Catmull-Rom resample, so a 30-residue helix reads as a helix.

    Prevents: the faceted, polygonal look of a raw Ca polyline, which at
    panel scale is read as model roughness rather than as a drawing choice.
    Interpolation is geometric only - no coordinate is moved, points are added
    between them - so nothing measured is drawn through a smoothed point.
    """
    P = np.asarray(P, float)
    if len(P) < 3:
        return P
    Q = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(len(Q) - 3):
        p0, p1, p2, p3 = Q[i], Q[i + 1], Q[i + 2], Q[i + 3]
        t = np.linspace(0.0, 1.0, per, endpoint=False)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-1][None, :])
    return np.vstack(out)


# --------------------------------------------------------------------------
# the blurred backing - the one raster layer
# --------------------------------------------------------------------------
def _rasterise(runs2d, xlim, ylim, W, H, depth_span):
    """Deposit each polyline segment into a scalar canvas, weighted by depth.

    Far segments deposit LESS ink. The exemplar's weighting is
    `1 - 0.4 * normalised(depth)` on an axis whose sign is whatever
    `cross(x, y)` produced, so it is as likely to brighten the far wall as the
    near one. Here `depth` is known to increase towards the viewer
    (Frame.project), so the sign is checked rather than inherited.
    """
    canvas = np.zeros((H, W), float)
    x0, x1 = xlim
    y0, y1 = ylim
    d0, d1 = depth_span
    for run in runs2d:
        if len(run) < 2:
            continue
        xs = (run[:, 0] - x0) / (x1 - x0) * (W - 1)
        ys = (run[:, 1] - y0) / (y1 - y0) * (H - 1)
        dn = (run[:, 2] - d0) / max(1e-9, d1 - d0)
        for k in range(len(xs) - 1):
            n = int(max(4, np.hypot(xs[k + 1] - xs[k], ys[k + 1] - ys[k]) * 1.5))
            t = np.linspace(0.0, 1.0, n)
            u = np.clip((xs[k] + t * (xs[k + 1] - xs[k])).astype(int), 0, W - 1)
            v = np.clip((ys[k] + t * (ys[k + 1] - ys[k])).astype(int), 0, H - 1)
            w = 0.45 + 0.55 * float(np.clip(0.5 * (dn[k] + dn[k + 1]), 0, 1))
            np.add.at(canvas, (v, u), w)
    return canvas


def blurred_layer(ax, runs2d, colour, xlim, ylim, depth_span,
                  sigma_A=1.6, base_alpha=0.30, gamma=0.45, res=880,
                  zorder=1):
    """One Gaussian-blurred pass of a Ca trace, drawn under everything.

    `sigma_A` is an ANGSTROM smoothing length, not a pixel count and not a
    fraction of the canvas. Prevents: a focal depth that changes with the crop
    or with the output resolution. A sigma in pixels makes a 60 A panel and a
    25 A close-up look like two different lenses even though both came from
    the same call - the "small multiples not on one footing" defect arriving
    by arithmetic - and a sigma as a fraction of the canvas breaks the moment
    the layer is a density rather than a trace, because atom spacing is
    physical: at 0.3 A the receptor renders as visible speckle.
    """
    W = res
    H = max(8, int(round(res * (ylim[1] - ylim[0]) / float(xlim[1] - xlim[0]))))
    canvas = _rasterise(runs2d, xlim, ylim, W, H, depth_span)
    sigma = max(1.0, sigma_A * (W - 1) / float(xlim[1] - xlim[0]))
    blurred = gaussian_filter(canvas, sigma=sigma)
    # Normalise on a high PERCENTILE of the inked pixels, not on the maximum.
    # Prevents: a panel whose whole density is set by its one densest crossing.
    # Dividing by max makes the typical helix sit at a tenth of full ink, so
    # the layer disappears and the panel reverts to the flat pale wash this
    # module exists to replace - which is exactly what the first version did.
    ink = blurred[blurred > 0]
    ref = np.percentile(ink, 97.0) if ink.size else 1.0
    if ref > 0:
        blurred = blurred / ref
    rgba = np.zeros((H, W, 4), float)
    rgba[..., :3] = np.array(mpl.colors.to_rgb(colour))
    rgba[..., 3] = np.clip(blurred, 0, 1) ** gamma * base_alpha
    im = ax.imshow(rgba, extent=(xlim[0], xlim[1], ylim[0], ylim[1]),
                   origin="lower", interpolation="bilinear", zorder=zorder)
    # The ONLY raster artist in the panel.
    im.set_rasterized(True)
    return im


def blurred_cloud(ax, proj, colour, xlim, ylim, depth_span=None,
                  sigma_A=1.5, base_alpha=0.42, gamma=0.38, res=880,
                  zorder=1.2):
    """Blur a cloud of ATOMS rather than a Ca polyline - a density, not a trace.

    Used where the subject is a cavity. PyMOL's answer is a semi-transparent
    molecular surface, and the render it produced is the worst panel in this
    figure set: a featureless grey blob filling the frame, with the peptide
    half outside it and the measured dashes buried under the surface. A
    depth-weighted density of the real heavy atoms shows the same enclosure,
    lets the near wall be lighter than the far one, and - because it is drawn
    UNDER the sharp layer rather than over it - cannot hide the measurement.
    """
    P = np.atleast_2d(np.asarray(proj, float))
    if depth_span is None:
        depth_span = (float(P[:, 2].min()), float(P[:, 2].max()))
    W = res
    H = max(8, int(round(res * (ylim[1] - ylim[0]) / float(xlim[1] - xlim[0]))))
    d0, d1 = depth_span
    xs = (P[:, 0] - xlim[0]) / (xlim[1] - xlim[0]) * (W - 1)
    ys = (P[:, 1] - ylim[0]) / (ylim[1] - ylim[0]) * (H - 1)
    dn = np.clip((P[:, 2] - d0) / max(1e-9, d1 - d0), 0, 1)
    keep = (xs >= 0) & (xs <= W - 1) & (ys >= 0) & (ys <= H - 1)
    canvas = np.zeros((H, W), float)
    np.add.at(canvas, (ys[keep].astype(int), xs[keep].astype(int)),
              0.35 + 0.65 * dn[keep])
    sigma = max(1.0, sigma_A * (W - 1) / float(xlim[1] - xlim[0]))
    blurred = gaussian_filter(canvas, sigma=sigma)
    ink = blurred[blurred > 0]
    ref = np.percentile(ink, 97.0) if ink.size else 1.0
    if ref > 0:
        blurred = blurred / ref
    rgba = np.zeros((H, W, 4), float)
    rgba[..., :3] = np.array(mpl.colors.to_rgb(colour))
    rgba[..., 3] = np.clip(blurred, 0, 1) ** gamma * base_alpha
    im = ax.imshow(rgba, extent=(xlim[0], xlim[1], ylim[0], ylim[1]),
                   origin="lower", interpolation="bilinear", zorder=zorder)
    im.set_rasterized(True)
    return im


def focal_plane(*claim_projections):
    """The depth of the near-most state-defining atom: where focus goes.

    Prevents: blurring the claim. See `depth_of_field`. Everything the panel
    is asserting - TM6, the anchor residues at 3.50/5.58/6x37/7.53, the
    partner peptide - goes in here, and the focal plane is put at the back of
    that set, so all of it is on the sharp side.
    """
    d = np.concatenate([np.atleast_2d(np.asarray(p, float))[:, 2]
                        for p in claim_projections if len(p)])
    return float(d.min())


def focus_report(claim_projections, focus_at, depth_span, name=""):
    """Refuse a view that cannot hold the whole claim in focus.

    Returns the fraction of the panel's depth range that lies BEHIND the focal
    plane - i.e. how much of the picture the blur is doing work on. Raises if
    any claim atom is behind the plane, which can only happen if a caller
    passed a focal plane it did not derive from the claim.
    """
    d = np.concatenate([np.atleast_2d(np.asarray(p, float))[:, 2]
                        for p in claim_projections if len(p)])
    if d.min() < focus_at - 1e-6:
        raise ValueError(
            "%s: %d of %d state-defining atoms sit behind the focal plane. "
            "Do not ship this view - blur would fall on the claim. Use a "
            "second view instead." % (name, int((d < focus_at).sum()), d.size))
    lo, hi = depth_span
    return float((focus_at - lo) / max(1e-9, hi - lo))


def depth_of_field_cloud(ax, proj, colour, xlim, ylim, depth_span=None,
                         far=(3.0, 0.30), near=(1.35, 0.42), split=0.45,
                         res=880, zorder=1.0, focus_at=None):
    """The two-pass focal stack, on an atom density rather than a Ca trace.

    At close-up scale a blurred Ca polyline is a glow; at whole-receptor scale
    it is a grey haze with no body, because 300 Ca in a 50 A frame are mostly
    empty space. The heavy atoms are not: blurring them gives the receptor
    actual mass, which is what a molecular-surface render buys and what the
    trace-only version of this panel was missing.
    """
    P = np.atleast_2d(np.asarray(proj, float))
    if depth_span is None:
        depth_span = (float(np.percentile(P[:, 2], 1)),
                      float(np.percentile(P[:, 2], 99)))
    cut = float(np.quantile(P[:, 2], split)) if focus_at is None \
        else float(focus_at)
    back, front = P[P[:, 2] < cut], P[P[:, 2] >= cut]
    if len(back):
        blurred_cloud(ax, back, colour, xlim, ylim, depth_span,
                      sigma_A=far[0], base_alpha=far[1], res=res,
                      zorder=zorder)
    if len(front):
        blurred_cloud(ax, front, colour, xlim, ylim, depth_span,
                      sigma_A=near[0], base_alpha=near[1], res=res,
                      zorder=zorder + 0.1)


def depth_of_field(ax, runs3d, colour, xlim, ylim, depth_span=None,
                   far=(2.4, 0.42), near=(0.95, 0.66), split=0.45,
                   res=880, zorder=1, focus_at=None):
    """Two blur passes, far and near, which is what makes a focal PLANE.

    A single blur is a flat wash and reads as a smudge. The exemplar layers
    sigma 9.0 / alpha 0.30 over sigma 3.2 / alpha 0.55 on the SAME trace;
    this splits the trace by depth first, so the wide soft pass carries only
    what is behind the focal plane and the tight strong pass only what is in
    front of it. That is the difference between a picture that is blurred and
    a picture that has depth.

    `split` is the depth quantile of the focal plane; `focus_at` overrides it
    with an absolute depth and is what every panel here uses.

    THE AXIS CONFLICT, and why `focus_at` is not optional. This literature
    de-emphasises by SUBJECT, not by depth: `tejero2024opsin` Fig 5 ghosts the
    helices not under discussion and keeps TM5/TM6/TM7 opaque wherever they
    sit in z. Depth of field de-emphasises along a different axis, so a
    focal plane chosen from the scaffold's median depth will sometimes put
    part of the claim behind it - and a reader trained on this literature
    reads a blurred helix as "not the subject". Nothing in the 78-paper corpus
    uses this technique, so there is no benefit of the doubt to be had.

    So the focal plane is placed AT THE CLAIM: `focal_plane()` returns the
    near-most depth of the state-defining elements, everything behind them
    gets the wide soft pass, and no part of the subject is ever on the far
    side of the plane. `focus_report()` checks it and refuses a view that
    cannot hold the whole claim in focus - use two views instead of blurring
    one of them. Blur encodes depth only. It carries no interpretive meaning,
    and every caption on one of these panels has to say so.
    """
    pts = np.vstack([r for r in runs3d if len(r)]) if runs3d else np.zeros((1, 3))
    if depth_span is None:
        depth_span = (float(pts[:, 2].min()), float(pts[:, 2].max()))
    cut = float(np.quantile(pts[:, 2], split)) if focus_at is None \
        else float(focus_at)
    back, front = [], []
    for run in runs3d:
        if len(run) < 2:
            continue
        m = run[:, 2] >= cut
        # keep each side as contiguous pieces so neither polyline bridges a
        # stretch that belongs to the other side of the focal plane
        for keep, bucket in ((~m, back), (m, front)):
            idx = np.where(keep)[0]
            if len(idx) < 2:
                continue
            brk = np.where(np.diff(idx) != 1)[0]
            for piece in np.split(idx, brk + 1):
                if len(piece) >= 2:
                    bucket.append(run[piece])
    blurred_layer(ax, back or runs3d, colour, xlim, ylim, depth_span,
                  sigma_A=far[0], base_alpha=far[1], res=res, zorder=zorder)
    blurred_layer(ax, front or runs3d, colour, xlim, ylim, depth_span,
                  sigma_A=near[0], base_alpha=near[1], res=res,
                  zorder=zorder + 0.1)


# --------------------------------------------------------------------------
# the sharp layer
# --------------------------------------------------------------------------
def _fade(colour, dn, bg=PANEL_BG, amount=0.62):
    """Blend a colour towards the panel ground by how far away it is."""
    c = np.array(mpl.colors.to_rgb(colour))
    b = np.array(mpl.colors.to_rgb(bg))
    f = amount * (1.0 - float(np.clip(dn, 0, 1)))
    return tuple(c * (1 - f) + b * f)


def ribbon(ax, proj, colour, lw=3.0, zorder=6.0, halo=PANEL_BG,
           halo_extra=1.9, depth_span=None, fade=0.12, alpha=1.0, per=7):
    """A depth-cued tube for the element that carries the claim.

    Prevents: emphasis carried by hue alone. `ye2026multistatebias` Fig 4A
    draws TM6 as thick spheres against thin cartoon, and that second channel
    is what makes the panel readable in greyscale and at column width. Here
    near segments are thicker, more saturated and drawn later; far ones fade
    into the ground. Segments are emitted back-to-front so the tube occludes
    itself correctly, which a single Line2D cannot do.
    """
    P = _spline(np.asarray(proj, float), per=per)
    if len(P) < 2:
        return
    if depth_span is None:
        depth_span = (P[:, 2].min(), P[:, 2].max())
    d0, d1 = depth_span
    seg = [(0.5 * (P[k, 2] + P[k + 1, 2]), k) for k in range(len(P) - 1)]
    seg.sort()
    for depth, k in seg:
        dn = (depth - d0) / max(1e-9, d1 - d0)
        x = [P[k, 0], P[k + 1, 0]]
        y = [P[k, 1], P[k + 1, 1]]
        w = lw * (0.74 + 0.44 * dn)
        z = zorder + dn * 0.8
        if halo is not None:
            ax.plot(x, y, color=halo, lw=w + halo_extra, alpha=alpha,
                    solid_capstyle="round", zorder=z - 0.05)
        ax.plot(x, y, color=_fade(colour, dn, amount=fade), lw=w,
                alpha=alpha, solid_capstyle="round", zorder=z)


def thin_trace(ax, runs3d, colour=SCAFFOLD, lw=0.5, alpha=0.62, zorder=3.0,
               depth_span=None, per=5):
    """A hairline Ca trace over the blur, so the fold is legible as a fold.

    The blurred layer alone gives mass without connectivity: a reader can see
    that something is there and not that it is a seven-helix bundle. This is
    deliberately thin and grey - it is context, and context that competes with
    the subject is the same defect as colouring the scaffold.
    """
    for run in runs3d:
        P = _spline(np.asarray(run, float), per=per)
        if len(P) < 2:
            continue
        ds = depth_span or (P[:, 2].min(), P[:, 2].max())
        seg = [(0.5 * (P[k, 2] + P[k + 1, 2]), k) for k in range(len(P) - 1)]
        seg.sort()
        for depth, k in seg:
            dn = (depth - ds[0]) / max(1e-9, ds[1] - ds[0])
            ax.plot([P[k, 0], P[k + 1, 0]], [P[k, 1], P[k + 1, 1]],
                    color=_fade(colour, dn, amount=0.38),
                    lw=lw * (0.8 + 0.4 * dn), alpha=alpha,
                    solid_capstyle="round", zorder=zorder + dn * 0.4)


def sticks(ax, res_atoms, proj, tint=None, alpha=1.0, ball=1.75, lw=1.3,
           zorder=6.5, halo_alpha=0.30, depth_span=None, carbon=None,
           fade=0.0):
    """One residue as CPK ball-and-stick with a state-tinted halo.

    The halo is the exemplar's trick and it is worth copying exactly: a large
    soft `scatter` in the state colour under each CPK ball lets active and
    inactive read apart at a glance WITHOUT recolouring the atoms, so element
    identity and state identity stay separate channels. Recolouring the atoms
    by state - the obvious alternative - throws element identity away, and
    then a stick figure is decoration.

    `fade` defaults to ZERO. These are the atoms the predicate is a rule over;
    fading one of them because it happens to be further from the camera would
    de-emphasise the claim along the wrong axis, which is the one thing depth
    of field must never be allowed to do here.
    """
    if not res_atoms:
        return None
    xy = proj[:, :2]
    dep = proj[:, 2]
    ds = depth_span or (dep.min(), dep.max())
    dn = (dep - ds[0]) / max(1e-9, ds[1] - ds[0])
    for i in range(len(res_atoms)):
        for j in range(i + 1, len(res_atoms)):
            if np.linalg.norm(res_atoms[i]["xyz"] - res_atoms[j]["xyz"]) > 1.95:
                continue
            mid = (xy[i] + xy[j]) / 2.0
            for p, q, e, d in ((xy[i], mid, res_atoms[i]["elem"], dn[i]),
                               (mid, xy[j], res_atoms[j]["elem"], dn[j])):
                col = carbon if (carbon and e == "C") else \
                    ELEMENT_COLOUR.get(e, "#666666")
                ax.plot([p[0], q[0]], [p[1], q[1]], color=_fade(col, d, amount=fade),
                        lw=lw * (0.8 + 0.4 * d), alpha=alpha,
                        solid_capstyle="round", zorder=zorder + d * 0.3)
    for a, (x, y), d in zip(res_atoms, xy, dn):
        col = carbon if (carbon and a["elem"] == "C") else \
            ELEMENT_COLOUR.get(a["elem"], "#666666")
        r = ELEMENT_R.get(a["elem"], 1.5) * ball
        s = np.pi * r ** 2
        if tint is not None:
            ax.scatter([x], [y], s=s * 2.0, c=[tint], alpha=halo_alpha * alpha,
                       linewidths=0, zorder=zorder + d * 0.3 + 0.05)
        ax.scatter([x], [y], s=s, c=[_fade(col, d, amount=fade)], alpha=alpha,
                   edgecolors="white", linewidths=0.35,
                   zorder=zorder + d * 0.3 + 0.10)
    k = next((i for i, a in enumerate(res_atoms) if a["name"] == "CA"), 0)
    return float(xy[k, 0]), float(xy[k, 1])


# --------------------------------------------------------------------------
# THE DIFFERENTIATOR: a measured distance, with the atoms it was measured on
# --------------------------------------------------------------------------
def measured_distance(ax, p, q, value, pair, colour, offset=(0.0, 0.0),
                      fontsize=5.0, pair_fontsize=4.2, zorder=8.5,
                      ha="auto", va="center", lw=0.9, leader=True,
                      note=None):
    """Dashed line between two projected atoms, labelled with BOTH the value
    and the atom pair it was measured between.

    This is the whole reason the module exists. The corpus survey found the
    field split and both halves failing: `hilger2020gcgr` prints "18 A" and
    "105 deg" with no statement of which atoms were measured, and reports the
    same physical displacement as 17.4 A and 18 A in two panels without ever
    reconciling them; `ye2026multistatebias` and `tejero2024opsin` draw the
    movement as an arrow with no number anywhere. Not one of the 232 render
    rows surveyed annotates a magnitude with its atom pair.

    `value` must have been reproduced from the coordinates being drawn -
    `cifread.verify_anchor` does that and refuses otherwise - and `pair` must
    name the two atoms, not the two residues, because the same residue pair
    measured Ca-Ca and OH-OH gives two different numbers.
    """
    p = np.asarray(p, float)
    q = np.asarray(q, float)
    ax.plot([p[0], q[0]], [p[1], q[1]], color=colour, lw=lw,
            ls=(0, (2.4, 1.9)), solid_capstyle="butt", zorder=zorder,
            alpha=0.95)
    for e in (p, q):
        ax.scatter([e[0]], [e[1]], s=7.0, c=[colour], linewidths=0.3,
                   edgecolors="white", zorder=zorder + 0.1)
    mid = 0.5 * (p + q)
    tx, ty = mid[0] + offset[0], mid[1] + offset[1]
    if ha == "auto":
        # Keep the label inside the panel without moving the anchor: a label
        # clipped at the frame edge is the same defect as a model cropped out
        # of it, and at 4 pt it is the easier one to miss.
        x0, x1 = ax.get_xlim()
        f = (tx - x0) / float(x1 - x0)
        ha = "left" if f < 0.34 else ("right" if f > 0.66 else "center")
    if leader and (abs(offset[0]) > 0.4 or abs(offset[1]) > 0.4):
        ax.plot([mid[0], tx], [mid[1], ty], color=colour, lw=0.4, alpha=0.6,
                zorder=zorder - 0.05)
    # Two stacked texts rather than one: the value has to be the thing the eye
    # lands on, and the provenance has to be right underneath it rather than
    # in a caption. matplotlib cannot vary size or colour inside one text.
    ax.annotate(value, (tx, ty), xytext=(0, 2.2), textcoords="offset points",
                ha=ha, va="bottom", fontsize=fontsize, color=colour,
                fontweight="bold", zorder=zorder + 1.1,
                bbox=dict(facecolor="white", edgecolor=colour, linewidth=0.4,
                          alpha=0.94, boxstyle="round,pad=0.22"))
    sub = pair if not note else (pair + u"\n" + note)
    ax.annotate(sub, (tx, ty), xytext=(0, -2.2), textcoords="offset points",
                ha=ha, va="top", fontsize=pair_fontsize, color="#333333",
                linespacing=1.3, zorder=zorder + 1.0,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.90,
                          boxstyle="round,pad=0.22"))


# --------------------------------------------------------------------------
# panel furniture
# --------------------------------------------------------------------------
def setup_axes(ax, xlim, ylim, bg=PANEL_BG):
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal", adjustable="box")
    ax.set_facecolor(bg)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def frame_limits(pts_list, aspect, pad=1.08, centre_on=None):
    """Symmetric limits that FRAME everything given, at a required aspect.

    Prevents: part of the model cropped out of the panel - a recorded corpus
    defect - and its opposite, a molecule swimming in empty space, which is
    what the PyMOL renders did and why they had to be auto-trimmed before
    placement. Everything passed in is guaranteed inside the frame.
    """
    P = np.vstack([np.atleast_2d(p) for p in pts_list if len(p)])
    c = np.array([P[:, 0].mean(), P[:, 1].mean()]) if centre_on is None \
        else np.asarray(centre_on, float)
    hw = np.abs(P[:, 0] - c[0]).max() * pad
    hh = np.abs(P[:, 1] - c[1]).max() * pad
    if hw / hh > aspect:
        hh = hw / aspect
    else:
        hw = hh * aspect
    return (c[0] - hw, c[0] + hw), (c[1] - hh, c[1] + hh)


def scale_bar(ax, length=10.0, colour="#444444", pad=0.045, fontsize=4.6,
              y_frac=None):
    """A scale bar in Angstrom.

    Prevents: `ye2026multistatebias` Fig 4A's recorded defect - a displacement
    shown as an arrow with "no scale bar or measured distance on the figure".
    Costs two lines and makes every unlabelled separation on the panel
    readable to about an Angstrom.
    """
    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    xa = x0 + (x1 - x0) * pad
    ya = y0 + (y1 - y0) * (pad if y_frac is None else y_frac)
    ax.plot([xa, xa + length], [ya, ya], color=colour, lw=1.3,
            solid_capstyle="butt", zorder=9)
    ax.annotate(u"%g Å" % length, (xa + length / 2.0, ya),
                xytext=(0, 2.0), textcoords="offset points", ha="center",
                va="bottom", fontsize=fontsize, color=colour, zorder=9)


def chip(ax, text, loc="upper left", fontsize=4.5, colour="#333333",
         weight="normal", edge="#CFCAC3", alpha=0.90, pad=0.018):
    """A corner text chip. Used for the selection rule and the percentile.

    Prevents: the single commonest render defect in the corpus - 59 of 232
    rows are a hand-picked example with the selection rule unstated. It is
    stated ON the panel, not in the caption, because a panel travels without
    its caption into slides and referee reports.
    """
    va, ha = ("top", "left")
    x, y = pad, 1 - pad
    if "lower" in loc:
        va, y = "bottom", pad
    if "right" in loc:
        ha, x = "right", 1 - pad
    ax.text(x, y, text, transform=ax.transAxes, ha=ha, va=va,
            fontsize=fontsize, color=colour, fontweight=weight,
            linespacing=1.35, zorder=10,
            bbox=dict(facecolor="white", edgecolor=edge, linewidth=0.35,
                      alpha=alpha, boxstyle="round,pad=0.28"))


def colour_key(ax, entries, loc="lower right", fontsize=4.5, pad=0.018,
               dy=0.042):
    """The legend as coloured text, which is what this literature does.

    `hilger2020gcgr` Fig 1B and `tejero2024opsin` Fig 5 both use coloured
    words rather than a legend box with keys; a box costs area a render needs
    and forces the reader's eye out of the picture and back.
    """
    ha = "right" if "right" in loc else "left"
    x = 1 - pad if ha == "right" else pad
    top = "lower" not in loc
    for i, (text, col) in enumerate(entries):
        y = (1 - pad - dy * i) if top else (pad + dy * (len(entries) - 1 - i))
        ax.text(x, y, text, transform=ax.transAxes, ha=ha, va="center",
                fontsize=fontsize, color=col, fontweight="bold", zorder=10,
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.82,
                          boxstyle="round,pad=0.14"))


def cell_aspect(fig, gs, row, col_slice):
    """The true width:height of one gridspec cell, in inches.

    Prevents: the render collapsing to a sliver. A render axes has to be
    `set_aspect("equal")` or an Angstrom is longer across the page than down
    it; with `constrained_layout` that makes the layout engine shrink the axes
    until something gives, and the first build of GA-1 came out with three
    postage stamps and overlapping titles. So the crop is computed to the
    cell's real aspect and the axes then fills it exactly. `constrained_layout`
    must be OFF for this - the geometry has to be fixed before the crop is
    chosen, not after.
    """
    bottoms, tops, lefts, rights = gs.get_grid_positions(fig)

    def span(x, n):
        if isinstance(x, slice):
            return (x.start or 0), (x.stop or n) - 1
        return x, x

    c0, c1 = span(col_slice, gs.ncols)
    r0, r1 = span(row, gs.nrows)
    w = (rights[c1] - lefts[c0]) * fig.get_figwidth()
    h = (tops[r0] - bottoms[r1]) * fig.get_figheight()
    return float(w / h)


def raster_dpi(fig, dpi=400):
    """Set the resolution the rasterised backing is written at.

    matplotlib writes a rasterised artist into a PDF at the FIGURE's dpi,
    which defaults to 100 - so a blurred layer that looks right on screen
    prints as visible blocks. Call this before saving. Text, sticks and dashes
    are unaffected: they stay vector.
    """
    fig.set_dpi(dpi)
