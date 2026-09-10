"""
The Block A structure scenes, drawn with `figures/dofrender.py`.

One scene per render. Each is a function that takes an axes and the aspect
ratio of the cell it is being drawn into, draws the render, and returns a dict
of what it drew - so the composite script can print the same numbers in its
own strip without a second, independent derivation of them.

Nothing here chooses an anchor, a camera or a distance:

  * anchors, structure paths and selection rules are imported from
    `hero_renders.py`, which is the single source of truth for them, and every
    pair is re-verified against the tidy value with `cifread.verify_anchor`
    before this module will draw it (four of the drop's ALIGNMENT.md files
    name residues that do not reproduce the shipped distances - D13, D20);
  * every camera comes from `camera.py`'s rule via `dofrender.camera_frame`,
    so these renders and the PyMOL ones they replace are the same viewpoint;
  * every distance drawn carries its value AND the atom pair, on the panel.

WHAT IS DELIBERATELY NOT DRAWN
  The heterotrimer. Block A's cognate arm supplies the full Ga subunit, but
  the paper's claim is about a 21-residue alpha5 C-terminal co-input, and a
  render of the trimer would depict an experiment this figure is not
  reporting. Only Ga 334-354 is drawn, which is also what this literature
  does (`tejero2024opsin` Fig 5: "Only the alpha5 helix of the Ga subunit is
  shown"). The full-Ga input is stated in the chip, not hidden.

  A "confidently wrong" case. `11_structures/confidently_wrong/` ships row
  567, and the row is a correct apo prediction sitting 0.95 A from AA2AR's
  INACTIVE reference (D12). It is drawn here as what it is.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = os.path.dirname(HERE)
FIGDIR = os.path.dirname(BLOCK)
for p in (HERE, BLOCK, FIGDIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import cifread as CR                                          # noqa: E402
import dofrender as D                                         # noqa: E402
import figstyle as fs                                         # noqa: E402
import hero_renders as HR                                     # noqa: E402

ANCHORS = HR.ANCHORS

C_ACTIVE = fs.VERM        # the predicate calls this row active
C_INACTIVE = fs.BLUE      # ... or inactive
C_PEPTIDE = fs.GREEN      # the alpha5 C-terminal 21-mer
C_TILT = "#111111"        # the 2x46 / 6x37 tilt measure
C_NPXXY = fs.PURPLE       # the Y5.58 / Y7.53 NPxxY measure
C_REF = "#4A4A4A"         # a deposited structure that is context, not subject


# --------------------------------------------------------------------------
def _res(atoms, chain, resi, sidechain_only=False):
    out = [a for a in atoms if a["chain"] == chain and a["resi"] == resi
           and a["group"] == "ATOM" and a["elem"] != "H"]
    if sidechain_only:
        keep = [a for a in out if a["name"] not in ("N", "C", "O")]
        return keep or out
    return out


def _proj_runs(frame, runs, R=None, t=None):
    out = []
    for r in runs:
        c = r if R is None else D.apply_rt(r, R, t)
        out.append(frame.project(c))
    return out


def _tm6_run(atoms, chain, key):
    lo, hi = ANCHORS[key]["tm6"]
    runs = D.ca_runs(atoms, chain, lo, hi)
    return max(runs, key=len) if runs else np.zeros((0, 3))


def _icl3_window(key):
    """The TM5-to-TM6 stretch, by the same rule in every panel.

    Prevents: cells that are not on one footing, and a crop set by a coil.
    The predicted ICL3 is 147 residues in DRD2 and 19 in AA2AR; drawing it in
    one panel and not the other would make two receptors look like two kinds
    of object, and letting it into the frame at all expands the crop until the
    7TM bundle - the thing the claim is about - is a small object in the
    middle of a grey haze, which is what the first version of GA-1b did.

    So the window is dropped from every panel by one rule, and the panel SAYS
    it dropped it, with the confidence of what was dropped. In DRD2 row 8285
    that stretch has mean pLDDT 38.5 against 81.7 for the rest of the
    receptor - a fact the old render buried rather than stated.
    """
    a = ANCHORS[key]
    return a["npxxy"][0] + 10, a["tm6"][0] - 1


def _kept(lo, hi, key):
    ilo, ihi = _icl3_window(key)
    out = []
    for a, b in ((lo, min(hi, ilo - 1)), (max(lo, ihi + 1), hi)):
        if b > a:
            out.append((a, b))
    return out


def _body_runs(atoms, chain, lo, hi, key):
    """Ca runs of everything that is drawn: the 7TM window minus ICL3."""
    out = []
    for a, b in _kept(lo, hi, key):
        out.extend(D.ca_runs(atoms, chain, a, b))
    return out


def _body_heavy(atoms, chain, lo, hi, key):
    keep = _kept(lo, hi, key)
    return np.array([x["xyz"] for x in atoms
                     if x["chain"] == chain and x["elem"] != "H"
                     and x["group"] == "ATOM"
                     and any(a <= x["resi"] <= b for a, b in keep)])


def _omitted(atoms, chain, lo, hi, key, predicted=True):
    """What the ICL3 rule dropped from this panel, in words, or None."""
    ilo, ihi = _icl3_window(key)
    inside = [a["bfac"] for a in atoms if a["chain"] == chain
              and a["name"] == "CA" and a["group"] == "ATOM"
              and ilo <= a["resi"] <= ihi and lo <= a["resi"] <= hi]
    if len(inside) < 5:
        return None
    outside = [a["bfac"] for a in atoms if a["chain"] == chain
               and a["name"] == "CA" and a["group"] == "ATOM"
               and not (ilo <= a["resi"] <= ihi) and lo <= a["resi"] <= hi]
    if predicted:
        return (u"not drawn: predicted ICL3 Cα %d–%d (%d residues, mean "
                u"pLDDT %.1f vs %.1f for the rest)"
                % (ilo, ihi, len(inside), np.mean(inside), np.mean(outside)))
    return u"not drawn: ICL3 Cα %d–%d (%d residues)" % (ilo, ihi, len(inside))


def _claim_points(frame, atoms, key, chain=None, R=None, t=None, extra=()):
    """Every projected atom the panel is making a claim about.

    TM6, the four anchor atoms the predicate is a rule over, and anything else
    the caller names (the alpha5 21-mer, a contact partner). The focal plane
    is put at the back of this set, so no part of the claim is ever on the
    blurred side of it - the axis conflict described in dofrender's
    `depth_of_field`. Depth of field here is a cue about distance and nothing
    else, and the caption has to say so.
    """
    a = ANCHORS[key]
    c = chain or a["chain"]
    pts = [frame.project(_xf(_tm6_run(atoms, c, key), R, t))]
    for resi in a["tilt"] + a["npxxy"]:
        ra = _res(atoms, c, resi)
        pts.append(frame.project(_xf([x["xyz"] for x in ra], R, t)))
    pts.extend(extra)
    return [q for q in pts if len(q)]


def _xf(xyz, R=None, t=None):
    xyz = np.atleast_2d(np.asarray(xyz, float))
    return xyz if R is None else D.apply_rt(xyz, R, t)


def _verify(path, key, what):
    """Re-verify here as well as in hero_renders: a distance is not drawn by
    this module until it has been reproduced from the coordinates it is being
    drawn on."""
    return HR.verify(path, key, what)


def _anchor_labels(atoms, key, chain=None):
    a = ANCHORS[key]
    c = chain or a["chain"]
    n = dict((r, CR.residue_name(atoms, c, r)) for r in a["tilt"] + a["npxxy"])
    t1, t2 = a["tilt"]
    y1, y2 = a["npxxy"]
    return {
        "tilt": u"%s%d (2×46) Cα – %s%d (6×37) Cα"
                % (n[t1].title(), t1, n[t2].title(), t2),
        "npxxy": u"%s%d (5.58) OH – %s%d (7.53) OH"
                 % (n[y1].title(), y1, n[y2].title(), y2),
    }


def _draw_receptor(ax, frame, atoms, chain, lo, hi, key, xlim, ylim,
                   depth_span, R=None, t=None, blur_alpha=(0.54, 0.76),
                   trace_alpha=0.42, colour=D.SCAFFOLD, zorder=1.0,
                   focus_at=None):
    """The invariant bundle: a grey depth-of-field density plus a grey
    hairline Ca trace. Never coloured.

    GREY MEANS "NOT THE SUBJECT". `ye2026multistatebias` Fig 4A draws the
    whole receptor grey and colours only TM6; that is the convention this
    field actually has, and it is the one that survives being printed small.
    Colouring a whole structure by which FILE it came from - the scheme the
    old renders used - colours by provenance rather than by what moves.
    """
    heavy = _body_heavy(atoms, chain, lo, hi, key)
    if R is not None:
        heavy = D.apply_rt(heavy, R, t)
    D.depth_of_field_cloud(ax, frame.project(heavy), colour, xlim, ylim,
                           depth_span=depth_span,
                           far=(3.0, blur_alpha[0]),
                           near=(1.35, blur_alpha[1]), zorder=zorder,
                           focus_at=focus_at)
    sharp = _proj_runs(frame, _body_runs(atoms, chain, lo, hi, key), R, t)
    D.thin_trace(ax, sharp, colour=colour, alpha=trace_alpha,
                 depth_span=depth_span)
    return sharp


# --------------------------------------------------------------------------
# GA-1a - the receptor predicted alone
# --------------------------------------------------------------------------
def hero_a(ax, aspect=1.0):
    key, path, chain = "aa2ar", HR.AA2AR_APO, "A"
    dt, dn = _verify(path, key, "AA2AR row 567")
    atoms = CR.frame(path)
    a = ANCHORS[key]
    body = _body_runs(atoms, chain, 1, 316, key)
    ca = np.vstack(body)
    frame = D.camera_frame(path, (chain, 1, 316),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    P = frame.project(ca)
    xlim, ylim = D.frame_limits([P[:, :2]], aspect, pad=1.10)
    ds = (P[:, 2].min(), P[:, 2].max())

    claim = _claim_points(frame, atoms, key, chain)
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, "GA-1a")

    D.setup_axes(ax, xlim, ylim)
    _draw_receptor(ax, frame, atoms, chain, 1, 316, key, xlim, ylim, ds,
                   focus_at=focus)

    tm6 = frame.project(_tm6_run(atoms, chain, key))
    D.ribbon(ax, tm6, C_INACTIVE, lw=2.5, depth_span=ds, zorder=6.0)

    lab = _anchor_labels(atoms, key)
    for resi, tint, carbon in ((a["tilt"][0], C_INACTIVE, C_TILT),
                               (a["tilt"][1], C_INACTIVE, C_TILT),
                               (a["npxxy"][0], C_INACTIVE, C_NPXXY),
                               (a["npxxy"][1], C_INACTIVE, C_NPXXY)):
        ra = _res(atoms, chain, resi)
        D.sticks(ax, ra, frame.project([x["xyz"] for x in ra]), tint=tint,
                 depth_span=ds, carbon=carbon)

    p1 = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA")])[0]
    p2 = frame.project([CR.atom(atoms, chain, a["tilt"][1], "CA")])[0]
    D.measured_distance(ax, p1[:2], p2[:2], u"%.2f Å" % dt, lab["tilt"],
                        C_TILT, offset=(-15.0, 10.0))
    q1 = frame.project([CR.atom(atoms, chain, a["npxxy"][0], "OH")])[0]
    q2 = frame.project([CR.atom(atoms, chain, a["npxxy"][1], "OH")])[0]
    D.measured_distance(ax, q1[:2], q2[:2], u"%.2f Å" % dn, lab["npxxy"],
                        C_NPXXY, offset=(15.0, -9.0))

    D.colour_key(ax, [(u"TM6 — predicate: INACTIVE", C_INACTIVE),
                      (u"receptor bundle (not the subject)", "#8A8A8A")],
                 loc="lower right")
    D.chip(ax, u"AA2AR · apo · Boltz-2 · row 567\n"
               u"1 of 25 seeds in the cell · 100th percentile on pLDDT\n"
               u"selection: highest plddt_mean in the cell (73.93; median 72.04)\n"
               u"0.95 Å Cα RMSD to AA2AR's INACTIVE reference",
           loc="upper left")
    D.scale_bar(ax)
    return dict(row=567, d_tilt=dt, d_npxxy=dn, labels=lab,
                view=frame.label, behind_focus=behind,
                omitted=_omitted(atoms, chain, 1, 316, key))


# --------------------------------------------------------------------------
# GA-1b - the same models, cognate Ga supplied
# --------------------------------------------------------------------------
def hero_b(ax, aspect=1.0):
    key, path, chain = "drd2", HR.DRD2_COG, "A"
    dt, dn = _verify(path, key, "DRD2 row 8285")
    atoms = CR.frame(path)
    a = ANCHORS[key]
    ca = np.vstack(_body_runs(atoms, chain, 30, 443, key))
    frame = D.camera_frame(path, (chain, 30, 443),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    pep = np.vstack(D.ca_runs(atoms, "B", 334, 354))
    P = frame.project(ca)
    Q = frame.project(pep)
    xlim, ylim = D.frame_limits([P[:, :2], Q[:, :2]], aspect, pad=1.10)
    ds = (min(P[:, 2].min(), Q[:, 2].min()), max(P[:, 2].max(), Q[:, 2].max()))

    claim = _claim_points(frame, atoms, key, chain, extra=[Q])
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, "GA-1b")

    D.setup_axes(ax, xlim, ylim)
    _draw_receptor(ax, frame, atoms, chain, 30, 443, key, xlim, ylim, ds,
                   focus_at=focus)

    # the co-input: its own soft green glow, then a sharp tube on top. The
    # glow is what stops a 21-residue helix disappearing into a 400-residue
    # bundle at column width.
    D.blurred_layer(ax, [Q], C_PEPTIDE, xlim, ylim, ds,
                    sigma_A=1.1, base_alpha=0.34, zorder=1.4)
    tm6 = frame.project(_tm6_run(atoms, chain, key))
    D.ribbon(ax, tm6, C_ACTIVE, lw=2.5, depth_span=ds, zorder=6.0)
    D.ribbon(ax, Q, C_PEPTIDE, lw=3.0, depth_span=ds, zorder=6.6)

    lab = _anchor_labels(atoms, key)
    for resi, carbon in ((a["tilt"][0], C_TILT), (a["tilt"][1], C_TILT),
                         (a["npxxy"][0], C_NPXXY), (a["npxxy"][1], C_NPXXY)):
        ra = _res(atoms, chain, resi)
        D.sticks(ax, ra, frame.project([x["xyz"] for x in ra]), tint=C_ACTIVE,
                 depth_span=ds, carbon=carbon)

    p1 = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA")])[0]
    p2 = frame.project([CR.atom(atoms, chain, a["tilt"][1], "CA")])[0]
    D.measured_distance(ax, p1[:2], p2[:2], u"%.2f Å" % dt, lab["tilt"],
                        C_TILT, offset=(-16.0, 12.0))
    q1 = frame.project([CR.atom(atoms, chain, a["npxxy"][0], "OH")])[0]
    q2 = frame.project([CR.atom(atoms, chain, a["npxxy"][1], "OH")])[0]
    D.measured_distance(ax, q1[:2], q2[:2], u"%.2f Å" % dn, lab["npxxy"],
                        C_NPXXY, offset=(17.0, -6.0))

    D.colour_key(ax, [(u"TM6 — predicate: ACTIVE", C_ACTIVE),
                      (u"α5 C-terminal 21-mer (Gα 334–354)", C_PEPTIDE),
                      (u"receptor bundle (not the subject)", "#8A8A8A")],
                 loc="lower right")
    D.chip(ax, u"DRD2 · cognate Gα · OpenFold-3 · row 8285\n"
               u"1 of 25 seeds in the cell · 50th percentile on RMSD-to-active\n"
               u"selection: median rmsd_to_active_ref (1.218 Å; rank 13 of 25)\n"
               u"input was the FULL cognate Gα; only α5 334–354 is drawn",
           loc="upper left")
    D.scale_bar(ax)
    return dict(row=8285, d_tilt=dt, d_npxxy=dn, labels=lab,
                view=frame.label, behind_focus=behind,
                omitted=_omitted(atoms, chain, 30, 443, key))


# --------------------------------------------------------------------------
# GA-1c - the same prediction over the deposited active state
# --------------------------------------------------------------------------
def hero_c(ax, aspect=1.0):
    key, path, chain = "drd2", HR.DRD2_COG, "A"
    dt, dn = _verify(path, key, "DRD2 row 8285")
    rt, rn = _verify(HR.DRD2_REF, "7jvr", "7JVR reference")
    atoms = CR.frame(path)
    ref = CR.frame(HR.DRD2_REF)
    a = ANCHORS[key]
    R, t, npair, rms = D.superpose(ref, atoms, "R", chain, 34, 441)

    ca = np.vstack(_body_runs(atoms, chain, 30, 443, key))
    frame = D.camera_frame(path, (chain, 30, 443),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "cytoplasmic", ca=ca)
    pep = np.vstack(D.ca_runs(atoms, "B", 334, 354))
    P, Q = frame.project(ca), frame.project(pep)
    xlim, ylim = D.frame_limits([P[:, :2], Q[:, :2]], aspect, pad=1.06)
    ds = (min(P[:, 2].min(), Q[:, 2].min()), max(P[:, 2].max(), Q[:, 2].max()))

    claim = (_claim_points(frame, atoms, key, chain, extra=[Q])
             + _claim_points(frame, ref, "7jvr", "R", R=R, t=t))
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, "GA-1c")

    D.setup_axes(ax, xlim, ylim)
    # Both bundles grey: the claim is that TWO TM6 helices land on each other,
    # so the bundles are context in both structures and neither gets a hue.
    _draw_receptor(ax, frame, atoms, chain, 30, 443, key, xlim, ylim, ds,
                   focus_at=focus)
    _draw_receptor(ax, frame, ref, "R", 34, 441, "7jvr", xlim, ylim, ds,
                   R=R, t=t, blur_alpha=(0.15, 0.26), trace_alpha=0.34,
                   colour="#A8A29B", focus_at=focus)

    # The reference TM6 is drawn as a THICK PALE SHADOW and the prediction as
    # a thinner bright tube inside it. Drawn at equal weight - the first
    # version - the prediction simply hides the reference and the panel shows
    # one helix, which is the opposite of the claim: the claim is that they
    # coincide, and a reader has to be able to SEE the one inside the other.
    ref_tm6 = frame.project(D.apply_rt(_tm6_run(ref, "R", "7jvr"), R, t))
    D.ribbon(ax, ref_tm6, "#B4AEA6", lw=6.2, depth_span=ds, zorder=5.2,
             halo=None, fade=0.10)
    tm6 = frame.project(_tm6_run(atoms, chain, key))
    D.ribbon(ax, tm6, C_ACTIVE, lw=2.4, depth_span=ds, zorder=6.2,
             halo_extra=1.2)
    D.ribbon(ax, Q, C_PEPTIDE, lw=3.2, depth_span=ds, zorder=6.6)

    lab = _anchor_labels(atoms, key)
    # the SAME atom pair, measured on both structures - which is the thing the
    # corpus never does: hilger2020gcgr reports 17.4 A and 18 A for one
    # displacement at two different residues and never reconciles them.
    p1 = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA")])[0]
    p2 = frame.project([CR.atom(atoms, chain, a["tilt"][1], "CA")])[0]
    D.measured_distance(ax, p1[:2], p2[:2], u"%.2f Å" % dt, lab["tilt"],
                        C_ACTIVE, offset=(-7.0, 10.0),
                        note=u"prediction, row 8285")
    r1 = frame.project(D.apply_rt(
        [CR.atom(ref, "R", ANCHORS["7jvr"]["tilt"][0], "CA")], R, t))[0]
    r2 = frame.project(D.apply_rt(
        [CR.atom(ref, "R", ANCHORS["7jvr"]["tilt"][1], "CA")], R, t))[0]
    D.measured_distance(ax, r1[:2], r2[:2], u"%.2f Å" % rt, lab["tilt"],
                        "#7A736B", offset=(-9.0, -8.0),
                        note=u"7JVR, deposited active")

    D.colour_key(ax, [(u"prediction TM6 (row 8285)", C_ACTIVE),
                      (u"inside 7JVR TM6 — deposited active", "#8F887F"),
                      (u"α5 C-terminal 21-mer", C_PEPTIDE)],
                 loc="upper right")
    # The RMSD is NOT drawn as a measured quantity on the panel. The shipped
    # rmsd_to_active_ref for this row is 1.218 A; superposing these two files
    # on every shared receptor Ca gives 1.295 A, and no trimmed window tried
    # here reproduces 1.218 (see FIGURE_PROVENANCE). A number that does not
    # reproduce from the coordinates being drawn may be quoted as the
    # SELECTION statistic - which is all it is - but it may not be presented
    # as something this picture measures.
    D.chip(ax, u"selection: median rmsd_to_active_ref 1.218 Å (shipped; rank 13 of 25,\n"
               u"cell range 1.020–1.507 Å). Superposed here on %d shared receptor Cα\n"
               u"34–441: %.3f Å. The shipped 1.218 Å does not reproduce from these\n"
               u"coordinates; the scorer's atom set is not recorded in the drop.\n"
               u"State REACHED — NOT amplitude reproduction (BA-4)"
               % (npair, rms), loc="lower left")
    D.scale_bar(ax, y_frac=0.955)
    return dict(row=8285, d_tilt=dt, d_npxxy=dn, ref_tilt=rt, ref_npxxy=rn,
                rmsd=rms, n_ca=npair, labels=lab, view=frame.label,
                behind_focus=behind, shipped_rmsd=1.218,
                omitted=_omitted(atoms, chain, 30, 443, key))


# --------------------------------------------------------------------------
# BA-8 - the alpha5 21-mer in the intracellular cavity
# --------------------------------------------------------------------------
def ba8_cavity(ax, aspect=1.0):
    key, path, chain = "drd2", HR.DRD2_COG, "A"
    dt, dn = _verify(path, key, "DRD2 row 8285")
    atoms = CR.frame(path)
    a = ANCHORS[key]
    ca = np.vstack(_body_runs(atoms, chain, 30, 443, key))
    frame = D.camera_frame(path, (chain, 30, 443),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    pep_runs = D.ca_runs(atoms, "B", 334, 354)
    pep = np.vstack(pep_runs)
    Q = frame.project(pep)
    P = frame.project(ca)
    # A SIDE view cropped to the intracellular half, not the cytoplasmic view
    # of GA-1c. Looking up the bundle shows the cavity mouth end-on, and a
    # 42 A crop of a 7TM bundle seen end-on is a uniform disc of density with
    # the peptide lying across it - which is what the PyMOL surface version of
    # this panel showed, and it is unreadable as a cavity. Side-on, the helix
    # is seen going IN.
    #
    # The crop is a rule: centred on the midpoint of the alpha5 centroid and
    # the two tilt anchors, half-extent 24 A. Centring on the peptide alone -
    # the obvious choice, and the first one tried - puts the receptor in the
    # top half and empty ground in the bottom, because the peptide sticks out
    # of the cavity it is entering.
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    centre = 0.38 * Q[:, :2].mean(axis=0) + 0.62 * anch[:, :2].mean(axis=0)
    xlim, ylim = D.frame_limits(
        [np.array([[centre[0] - 24, centre[1] - 24],
                   [centre[0] + 24, centre[1] + 24]])], aspect, pad=1.0)

    heavy = _body_heavy(atoms, chain, 30, 443, key)
    H = frame.project(heavy)
    ds = (float(np.percentile(H[:, 2], 1)), float(np.percentile(H[:, 2], 99)))

    claim = _claim_points(frame, atoms, key, chain,
                          extra=[Q, frame.project([x["xyz"] for x in
                                                   _res(atoms, chain, 132)]),
                                 frame.project([x["xyz"] for x in
                                                _res(atoms, "B", 351)])])
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, "BA-8a")

    D.setup_axes(ax, xlim, ylim)
    # The cavity as a depth-weighted atom density rather than a PyMOL surface,
    # with the two passes far apart in strength: seen from the cytoplasm the
    # near wall is the wall of the cavity and the extracellular half is behind
    # it. A surface renders both at once and fills the cavity in - which is
    # exactly what the PyMOL version of this panel did.
    D.depth_of_field_cloud(ax, H, "#8E8880", xlim, ylim, depth_span=ds,
                           far=(3.4, 0.20), near=(1.3, 0.92),
                           focus_at=focus, zorder=1.0)
    D.thin_trace(ax, _proj_runs(frame, _body_runs(atoms, chain, 30, 443, key)),
                 colour=D.SCAFFOLD, alpha=0.34, depth_span=ds, lw=0.36)

    tm6 = frame.project(_tm6_run(atoms, chain, key))
    D.ribbon(ax, tm6, C_ACTIVE, lw=3.0, depth_span=ds, zorder=6.0)
    D.blurred_layer(ax, [Q], C_PEPTIDE, xlim, ylim, ds, sigma_A=1.3,
                    base_alpha=0.38, zorder=1.5)
    D.ribbon(ax, Q, C_PEPTIDE, lw=4.4, depth_span=ds, zorder=6.8)

    lab = _anchor_labels(atoms, key)
    for resi, carbon in ((a["tilt"][0], C_TILT), (a["tilt"][1], C_TILT),
                         (a["npxxy"][0], C_NPXXY), (a["npxxy"][1], C_NPXXY)):
        ra = _res(atoms, chain, resi)
        D.sticks(ax, ra, frame.project([x["xyz"] for x in ra]), tint=C_ACTIVE,
                 depth_span=ds, carbon=carbon, ball=1.7)

    # R3.50 and the alpha5 atom it reaches, both drawn, contact measured here
    r132 = _res(atoms, chain, 132)
    D.sticks(ax, r132, frame.project([x["xyz"] for x in r132]), tint=C_ACTIVE,
             depth_span=ds, carbon="#111111", ball=2.4)
    c351 = _res(atoms, "B", 351)
    D.sticks(ax, c351, frame.project([x["xyz"] for x in c351]),
             tint=C_PEPTIDE, depth_span=ds, carbon=C_PEPTIDE, ball=2.4)

    contact = float(np.linalg.norm(CR.atom(atoms, chain, 132, "NH2")
                                   - CR.atom(atoms, "B", 351, "O")))
    c1 = frame.project([CR.atom(atoms, chain, 132, "NH2")])[0]
    c2 = frame.project([CR.atom(atoms, "B", 351, "O")])[0]
    D.measured_distance(ax, c1[:2], c2[:2], u"%.2f Å" % contact,
                        u"Arg132 (3.50) NH2 – Cys351 O (α5)", C_PEPTIDE,
                        offset=(7.5, -6.0),
                        note=u"closest heavy-atom contact, measured on this model")

    p1 = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA")])[0]
    p2 = frame.project([CR.atom(atoms, chain, a["tilt"][1], "CA")])[0]
    D.measured_distance(ax, p1[:2], p2[:2], u"%.2f Å" % dt, lab["tilt"],
                        C_TILT, offset=(14.0, 4.5))
    q1 = frame.project([CR.atom(atoms, chain, a["npxxy"][0], "OH")])[0]
    q2 = frame.project([CR.atom(atoms, chain, a["npxxy"][1], "OH")])[0]
    D.measured_distance(ax, q1[:2], q2[:2], u"%.2f Å" % dn, lab["npxxy"],
                        C_NPXXY, offset=(-15.0, -2.0))

    D.colour_key(ax, [(u"α5 C-terminal 21-mer (Gα 334–354)", C_PEPTIDE),
                      (u"TM6 — predicate: ACTIVE", C_ACTIVE),
                      (u"receptor heavy-atom density", "#8A8A8A")],
                 loc="lower right")
    D.chip(ax, u"DRD2 · cognate Gα · OpenFold-3 · row 8285 · side view\n"
               u"1 of 25 seeds · 50th percentile on RMSD-to-active\n"
               u"crop: ±24 Å of the α5 centroid, intracellular half\n"
               u"input was the FULL cognate Gα; only α5 334–354 is drawn",
           loc="upper left")
    D.scale_bar(ax)
    return dict(row=8285, d_tilt=dt, d_npxxy=dn, contact=contact, labels=lab,
                view=frame.label, behind_focus=behind,
                omitted=_omitted(atoms, chain, 30, 443, key))


# --------------------------------------------------------------------------
# BA-1a - the instrument: two measurements, two views
# --------------------------------------------------------------------------
def _ba1a_common():
    at_a = CR.frame(HR.ADRB2_ACTIVE)
    at_i = CR.frame(HR.ADRB2_INACTIVE)
    da_t, da_n = _verify(HR.ADRB2_ACTIVE, "4lde", "4LDE (ADRB2 active ref)")
    di_t, di_n = _verify(HR.ADRB2_INACTIVE, "2rh1", "2RH1 (ADRB2 inactive ref)")
    # 2RH1 moves onto 4LDE, over the receptor window only: 2RH1's T4 lysozyme
    # sits at 1002-1161 of the SAME chain, and one selection reused across
    # both objects superposes the bundle onto the lysozyme (D21).
    R, t, npair, rms = D.superpose(at_i, at_a, "A", "A", 1029, 1342,
                                   mobile_offset=-1000)
    a = ANCHORS["4lde"]
    return at_a, at_i, (da_t, da_n), (di_t, di_n), R, t, npair, rms, a


def _ba1a_scene(ax, aspect, view, measure):
    at_a, at_i, (da_t, da_n), (di_t, di_n), R, t, npair, rms, a = _ba1a_common()
    ca = np.vstack(_body_runs(at_a, "A", 1029, 1342, "4lde"))
    frame = D.camera_frame(HR.ADRB2_ACTIVE, ("A", 1029, 1342),
                           (("A", a["tilt"][0]), ("A", a["tilt"][1])), view,
                           ca=ca)
    P = frame.project(ca)
    xlim, ylim = D.frame_limits([P[:, :2]], aspect, pad=1.08)
    ds = (P[:, 2].min(), P[:, 2].max())

    claim = (_claim_points(frame, at_a, "4lde", "A")
             + _claim_points(frame, at_i, "2rh1", "A", R=R, t=t))
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, "BA-1a %s" % view)

    D.setup_axes(ax, xlim, ylim)
    _draw_receptor(ax, frame, at_a, "A", 1029, 1342, "4lde", xlim, ylim, ds,
                   focus_at=focus)
    _draw_receptor(ax, frame, at_i, "A", 29, 342, "2rh1", xlim, ylim, ds,
                   R=R, t=t, blur_alpha=(0.14, 0.24), trace_alpha=0.32,
                   colour="#A8A29B", focus_at=focus)

    i_tm6 = frame.project(D.apply_rt(_tm6_run(at_i, "A", "2rh1"), R, t))
    D.ribbon(ax, i_tm6, C_INACTIVE, lw=3.0, depth_span=ds, zorder=5.6)
    a_tm6 = frame.project(_tm6_run(at_a, "A", "4lde"))
    D.ribbon(ax, a_tm6, C_ACTIVE, lw=3.0, depth_span=ds, zorder=6.0)

    lab_a = _anchor_labels(at_a, "4lde")
    lab_i = _anchor_labels(at_i, "2rh1")

    def pt(atoms, key, which, name, xform=False):
        c = ANCHORS[key]["chain"]
        r = ANCHORS[key][which]
        p = np.array([CR.atom(atoms, c, r[0], name),
                      CR.atom(atoms, c, r[1], name)])
        if xform:
            p = D.apply_rt(p, R, t)
        return frame.project(p)

    if measure == "tilt":
        pa = pt(at_a, "4lde", "tilt", "CA")
        pi = pt(at_i, "2rh1", "tilt", "CA", xform=True)
        D.measured_distance(ax, pa[0, :2], pa[1, :2], u"%.2f Å" % da_t,
                            lab_a["tilt"], C_ACTIVE, offset=(1.0, 10.0),
                            note=u"4LDE, deposited ACTIVE")
        D.measured_distance(ax, pi[0, :2], pi[1, :2], u"%.2f Å" % di_t,
                            lab_i["tilt"], C_INACTIVE, offset=(0.0, -11.0),
                            note=u"2RH1, deposited INACTIVE")
        shown = u"TM6 tilt · threshold 14.932 Å · active = above it"
    else:
        pa = pt(at_a, "4lde", "npxxy", "OH")
        pi = pt(at_i, "2rh1", "npxxy", "OH", xform=True)
        D.measured_distance(ax, pa[0, :2], pa[1, :2], u"%.2f Å" % da_n,
                            lab_a["npxxy"], C_ACTIVE, offset=(11.0, 4.5),
                            note=u"4LDE, deposited ACTIVE")
        D.measured_distance(ax, pi[0, :2], pi[1, :2], u"%.2f Å" % di_n,
                            lab_i["npxxy"], C_INACTIVE, offset=(-11.0, -6.0),
                            note=u"2RH1, deposited INACTIVE")
        shown = u"NPxxY · threshold 9.080 Å · active = below it"

    D.colour_key(ax, [(u"4LDE TM6 — ADRB2 active reference", C_ACTIVE),
                      (u"2RH1 TM6 — ADRB2 inactive reference", C_INACTIVE),
                      (u"both bundles (not the subject)", "#8A8A8A")],
                 loc="lower right")
    D.chip(ax, u"ADRB2 reference structures, not predictions\n"
               u"selected from 2: the panel active reference and the inactive\n"
               u"one 11_structures ships (3 inactive references exist)\n"
               u"superposed on receptor Cα 1029–1342 / 29–342, %d pairs, %.2f Å\n"
               u"%s" % (npair, rms, shown), loc="upper left")
    D.scale_bar(ax)
    return dict(a_tilt=da_t, a_npxxy=da_n, i_tilt=di_t, i_npxxy=di_n,
                labels_a=lab_a, labels_i=lab_i, n_ca=npair, rmsd=rms,
                view=frame.label, behind_focus=behind, measure=measure)


def ba1a_side(ax, aspect=1.0):
    """Side view, carrying the NPxxY measurement on both references."""
    return _ba1a_scene(ax, aspect, "side", "npxxy")


def ba1a_cyto(ax, aspect=1.0):
    """Cytoplasmic view, carrying the TM6 tilt measurement on both."""
    return _ba1a_scene(ax, aspect, "cytoplasmic", "tilt")


# --------------------------------------------------------------------------
# GA-1 - the graphical abstract. ONE composition, not a lettered grid.
#
# These three scenes are deliberately not `hero_a/b/c` with smaller type. A
# graphical abstract is read as a single image at thumbnail size, so almost
# everything the figure panels carry has to come out: no panel letters, no
# selection-rule chip, no percentile, no second measurement, no residue
# ball-and-stick beyond the two atoms the one printed distance is measured
# between. What stays is the one idea and the one number that supports it.
#
# WHAT IS DELIBERATELY ABSENT: an arrow between left and right. The centre
# scene IS the connector, and it is labelled with what was SUPPLIED rather
# than with what happened. An arrow labelled "activation" is the field's
# characteristic failure on exactly this claim, and an unlabelled one is read
# as magnitude - which is BA-4, and BA-4 is negative on three of four
# backbones. A left-to-right composition with the co-input drawn in the middle
# says the same thing and asserts nothing about amplitude.
#
# THE SAME ATOM PAIR ON BOTH. The pair is 2x46 Ca - 6x37 Ca in both scenes and
# is printed ONCE, large, under the composition; each render carries only its
# own two residue names, which keeps the strings short enough to survive
# reduction to 8 cm. Printing the pair once is also the strongest available
# statement that it IS one pair: `hilger2020gcgr` reports one displacement as
# 17.4 A and 18 A at two different residues and never reconciles them.
# --------------------------------------------------------------------------
GA_VALUE_FS = 11.5        # sizes are for a 130 mm figure reduced to ~80 mm
GA_PAIR_FS = 7.5


def _ga_tilt_only(ax, atoms, chain, key, frame, ds, offset, colour=C_TILT,
                  value_fs=GA_VALUE_FS, pair_fs=GA_PAIR_FS):
    """The one printed measurement: value, and the two residues it is on.

    Only the two atoms the distance is measured between are drawn, as small
    spheres. The four-residue ball-and-stick of the figure panels is right for
    a figure and wrong here - at thumbnail size it is a smudge, and it invites
    the eye to look for a claim that this composition is not making.
    """
    a = ANCHORS[key]
    c = chain
    names = dict((r, CR.residue_name(atoms, c, r)) for r in a["tilt"])
    p = frame.project([CR.atom(atoms, c, a["tilt"][0], "CA"),
                       CR.atom(atoms, c, a["tilt"][1], "CA")])
    d = float(np.linalg.norm(CR.atom(atoms, c, a["tilt"][0], "CA")
                             - CR.atom(atoms, c, a["tilt"][1], "CA")))
    for xy in p[:, :2]:
        ax.scatter([xy[0]], [xy[1]], s=13, c=[colour], linewidths=0.5,
                   edgecolors="white", zorder=8.6)
    D.measured_distance(
        ax, p[0, :2], p[1, :2], u"%.2f Å" % d,
        u"%s%d / %s%d" % (names[a["tilt"][0]].title(), a["tilt"][0],
                          names[a["tilt"][1]].title(), a["tilt"][1]),
        colour, offset=offset, fontsize=value_fs, pair_fontsize=pair_fs,
        lw=1.1)
    return d


def ga_left(ax, aspect=1.0):
    """Receptor from sequence alone. TM6 closed, one distance."""
    key, path, chain = "aa2ar", HR.AA2AR_APO, "A"
    dt, _ = _verify(path, key, "AA2AR row 567")
    atoms = CR.frame(path)
    a = ANCHORS[key]
    ca = np.vstack(_body_runs(atoms, chain, 1, 316, key))
    frame = D.camera_frame(path, (chain, 1, 316),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    P = frame.project(ca)
    xlim, ylim = D.frame_limits([P[:, :2]], aspect, pad=1.06)
    ds = (P[:, 2].min(), P[:, 2].max())

    tm6 = frame.project(_tm6_run(atoms, chain, key))
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    focus = D.focal_plane(tm6, anch)
    behind = D.focus_report([tm6, anch], focus, ds, "GA-1 left")

    D.setup_axes(ax, xlim, ylim)
    _draw_receptor(ax, frame, atoms, chain, 1, 316, key, xlim, ylim, ds,
                   focus_at=focus, trace_alpha=0.34)
    D.ribbon(ax, tm6, C_INACTIVE, lw=3.4, depth_span=ds, zorder=6.0)
    d = _ga_tilt_only(ax, atoms, chain, key, frame, ds, offset=(-13.0, 9.0))
    return dict(row=567, d_tilt=d, behind_focus=behind, view=frame.label,
                omitted=_omitted(atoms, chain, 1, 316, key))


def ga_centre(ax, aspect=1.0):
    """The co-input arriving: the alpha5 21-mer entering the cavity.

    Drawn from the cognate model on the right, cropped to the cavity. It is
    the only directional element in the composition and it is labelled with
    what was SUPPLIED, never with an outcome. No distance is drawn here - the
    contact geometry is BA-8's job, and a third number would make this read as
    a panel rather than as a transition.
    """
    key, path, chain = "drd2", HR.DRD2_COG, "A"
    _verify(path, key, "DRD2 row 8285")
    atoms = CR.frame(path)
    a = ANCHORS[key]
    ca = np.vstack(_body_runs(atoms, chain, 30, 443, key))
    frame = D.camera_frame(path, (chain, 30, 443),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    pep = np.vstack(D.ca_runs(atoms, "B", 334, 354))
    Q = frame.project(pep)
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    # same crop rule as BA-8a, tightened: the cavity and the helix in it
    centre = 0.50 * Q[:, :2].mean(axis=0) + 0.50 * anch[:, :2].mean(axis=0)
    xlim, ylim = D.frame_limits(
        [np.array([[centre[0] - 22, centre[1] - 22],
                   [centre[0] + 22, centre[1] + 22]])], aspect, pad=1.0)
    heavy = _body_heavy(atoms, chain, 30, 443, key)
    H = frame.project(heavy)
    ds = (float(np.percentile(H[:, 2], 1)), float(np.percentile(H[:, 2], 99)))

    tm6 = frame.project(_tm6_run(atoms, chain, key))
    focus = D.focal_plane(tm6, Q)
    behind = D.focus_report([tm6, Q], focus, ds, "GA-1 centre")

    D.setup_axes(ax, xlim, ylim)
    D.depth_of_field_cloud(ax, H, "#8E8880", xlim, ylim, depth_span=ds,
                           far=(3.4, 0.20), near=(1.3, 0.90),
                           focus_at=focus, zorder=1.0)
    D.thin_trace(ax, _proj_runs(frame, _body_runs(atoms, chain, 30, 443, key)),
                 colour=D.SCAFFOLD, alpha=0.30, depth_span=ds, lw=0.34)
    D.ribbon(ax, tm6, C_ACTIVE, lw=3.2, depth_span=ds, zorder=6.0)
    D.blurred_layer(ax, [Q], C_PEPTIDE, xlim, ylim, ds, sigma_A=1.4,
                    base_alpha=0.42, zorder=1.5)
    D.ribbon(ax, Q, C_PEPTIDE, lw=5.0, depth_span=ds, zorder=6.8)
    return dict(behind_focus=behind, view=frame.label)


def ga_right(ax, aspect=1.0):
    """The same models with the partner supplied. TM6 open, same atom pair."""
    key, path, chain = "drd2", HR.DRD2_COG, "A"
    dt, _ = _verify(path, key, "DRD2 row 8285")
    atoms = CR.frame(path)
    a = ANCHORS[key]
    ca = np.vstack(_body_runs(atoms, chain, 30, 443, key))
    frame = D.camera_frame(path, (chain, 30, 443),
                           ((chain, a["tilt"][0]), (chain, a["tilt"][1])),
                           "side", ca=ca)
    pep = np.vstack(D.ca_runs(atoms, "B", 334, 354))
    P, Q = frame.project(ca), frame.project(pep)
    xlim, ylim = D.frame_limits([P[:, :2], Q[:, :2]], aspect, pad=1.06)
    ds = (min(P[:, 2].min(), Q[:, 2].min()), max(P[:, 2].max(), Q[:, 2].max()))

    tm6 = frame.project(_tm6_run(atoms, chain, key))
    anch = frame.project([CR.atom(atoms, chain, a["tilt"][0], "CA"),
                          CR.atom(atoms, chain, a["tilt"][1], "CA")])
    focus = D.focal_plane(tm6, anch, Q)
    behind = D.focus_report([tm6, anch, Q], focus, ds, "GA-1 right")

    D.setup_axes(ax, xlim, ylim)
    _draw_receptor(ax, frame, atoms, chain, 30, 443, key, xlim, ylim, ds,
                   focus_at=focus, trace_alpha=0.34)
    D.blurred_layer(ax, [Q], C_PEPTIDE, xlim, ylim, ds, sigma_A=1.1,
                    base_alpha=0.34, zorder=1.4)
    D.ribbon(ax, tm6, C_ACTIVE, lw=3.4, depth_span=ds, zorder=6.0)
    D.ribbon(ax, Q, C_PEPTIDE, lw=3.6, depth_span=ds, zorder=6.6)
    d = _ga_tilt_only(ax, atoms, chain, key, frame, ds, offset=(-16.0, 5.0))
    return dict(row=8285, d_tilt=d, behind_focus=behind, view=frame.label,
                omitted=_omitted(atoms, chain, 30, 443, key))
