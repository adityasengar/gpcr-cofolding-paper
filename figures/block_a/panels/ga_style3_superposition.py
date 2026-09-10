"""
GA-STYLE-3 - the graphical abstract as a SINGLE-FRAME SUPERPOSITION.

ONE RENDER. No left/right, no arrow, no sequence of scenes. The field's
dominant idiom for a conformational change is a single superposed frame in
which the whole receptor is grey and only the element that moves is coloured,
once per state: `ye2026multistatebias` Fig 4A greys the entire receptor and
colours only TM6, red for the inactive reference and green for the active;
`hilger2020gcgr` Fig 3A-B does the same across three states; `tejero2024opsin`
Fig 5 ghosts the helices not under discussion. This panel executes that idiom
and fixes the two things every render surveyed gets wrong.

WHAT THE CORPUS GETS WRONG, AND WHAT IS DONE HERE INSTEAD
    Four of the surveyed renders draw the activation magnitude as an ARROW and
    put the number in the running text, if anywhere. `hilger2020gcgr` prints
    17.4 A on Fig 3A and 18 A on Fig 1B for the same physical displacement,
    measured at two different residues, and never reconciles them. Not one of
    the 232 render rows in the survey annotates a magnitude with the atom pair
    it was measured between.

    So: no arrow anywhere, and the SAME atom pair - 2x46 CA to 6x37 CA, which
    in this receptor is Leu76 CA to residue 375 CA - is drawn on BOTH
    structures with BOTH values printed, each beside the dashes it belongs to,
    each carrying the file it came from. Two numbers, one pair, nothing to
    reconcile.

WHY THIS IS ONE RECEPTOR AND NOT TWO
    The archive ships four prediction CIFs: one apo (AA2AR) and three cognate
    (DRD2, and the ACM1 broken/healthy pair). No receptor has both arms, so a
    superposition of two PREDICTIONS is necessarily a superposition of two
    different receptors - and a single frame is exactly the form in which that
    confound is least visible, because the reader sees one grey bundle and
    reads one object. A frame that has to be captioned "these are two proteins"
    is a frame arguing against its own picture.

    So the second state here is DRD2's own deposited INACTIVE panel reference,
    6CM4, named in `02_references/reference_predicates.csv`. Same receptor,
    same residue numbering, same two atoms. The prediction supplies the active
    arm and the Ga co-input that produced it; the deposited structure supplies
    the inactive arm. Nothing in the frame is a different protein.

    6CM4's CIF is not in `11_structures/` - it was fetched from RCSB and is
    verified, from its own coordinates, to reproduce BOTH values the drop
    stores for it: d_tilt_ref = 11.445926 A and d_npxxy_oh_ref = 10.030448 A,
    at the same residue numbers the scorer used. That is a stronger provenance
    chain than the shipped ALIGNMENT.md files, four of which name residues that
    do not reproduce their own shipped distances (D13, D20).

THE INPUT WAS THE WHOLE Ga SUBUNIT, NOT A 21-MER
    Block A's cognate arm supplies the FULL cognate Ga (chain B, 354 residues).
    Only its alpha5 C-terminal 21 residues are DRAWN, which is what the claim
    is about and what this literature does (`tejero2024opsin` Fig 5: "Only the
    alpha5 helix of the Ga subunit is shown"). The paper's title claims a
    21-residue peptide co-input; BLOCK A DOES NOT TEST THAT, Block B will, and
    CLAIMS.md forbids any Block A sentence that implies the peptide result. So
    nothing on this panel may call the drawn 21-mer "the co-input": it is the
    part of the supplied Ga that is drawn. The subtitle, the colour key and the
    footnote all say the input was the whole subunit.

WHAT THE FRAME THEREFORE CLAIMS, AND WHAT IT DOES NOT
    It claims: given the cognate Ga as a co-input, the predicted TM6 of DRD2
    sits 5.83 A further open, at one named atom pair, than the same receptor's
    deposited inactive structure - and 0.31 A from its deposited ACTIVE
    reference on the same pair.

    It does not claim that the apo prediction stays closed: the blue helix is a
    crystal structure, not an apo prediction, and no picture here could show
    otherwise, because the apo DRD2 coordinates are not in the drop. That half
    of the claim is carried quantitatively by the ruler beneath, where DRD2's
    own 100 apo and 100 cognate rows sit as two separated distributions on the
    same axis. The render is one row; the ruler is the population it came from,
    which is the corpus's second commonest render defect (58 of 232 rows: no
    quantitative panel stands behind the claim the render makes).

    It does not claim amplitude reproduction - whether a receptor with further
    to travel travels further. That is BA-4 and it is NEGATIVE on three of four
    backbones. There is no arrow in this frame for exactly that reason: an
    unlabelled arrow between two helices is read as magnitude.

WHAT IS COLOURED
    Grey is the invariant scaffold and nothing else. Both bundles are grey -
    the prediction as a depth-weighted heavy-atom density with a hairline CA
    trace over it, the deposited structure as a fainter hairline alone, so the
    frame does not become blur over blur. Colour appears on exactly three
    things: TM6 of the prediction (vermillion, the predicate calls the row
    ACTIVE), TM6 of 6CM4 (blue, the predicate calls it inactive - and it does,
    `expected_fail` on both axes), and the alpha5 C-terminal 21-mer in the
    cavity (green). See above on what was actually supplied.

FOCUS
    Every state-defining atom - both TM6 runs, all four anchor atoms of both
    structures, the whole alpha5 - is passed to `focal_plane()` and the focal
    plane is set at the back of that set, so no part of the claim is ever on
    the blurred side. `focus_report()` refuses the view otherwise. Soft focus
    encodes DEPTH ONLY and the frame says so in its footnote; a blur may never
    soften the claim.

Run: python3 figures/block_a/panels/ga_style3_superposition.py [--view side|cytoplasmic]
"""
import argparse
import hashlib
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = os.path.dirname(HERE)
FIGDIR = os.path.dirname(BLOCK)
ROOT = os.path.dirname(FIGDIR)
for p in (HERE, BLOCK, FIGDIR):
    if p not in sys.path:
        sys.path.insert(0, p)

import badata as B                                             # noqa: E402
import cifread as CR                                           # noqa: E402
import figstyle as fs                                          # noqa: E402
import matplotlib.pyplot as plt                                # noqa: E402

import dofrender as D                                          # noqa: E402
import hero_renders as HR                                      # noqa: E402


# --------------------------------------------------------------------------
# the two structures
# --------------------------------------------------------------------------
PRED = HR.DRD2_COG                     # DRD2 x cognate Ga x OpenFold-3, row 8285
REF_INACTIVE = os.path.join(FIGDIR, "structures", "6CM4.cif")
REF_ACTIVE = HR.DRD2_REF               # 7JVR - NOT drawn; used for the second
                                       # RMSD in the chip and a ruler tick
REF_ACTIVE_TILT = 17.585960            # 7JVR, reference_predicates.csv

# 6CM4's anchors. NOT taken from any ALIGNMENT.md - four of those name residues
# that do not reproduce their own shipped distances (D13, D20). These are the
# residue numbers the DRD2 prediction uses, checked against the values
# 02_references/reference_predicates.csv stores for 6CM4.
ANCH_6CM4 = dict(chain="A", tilt=(76, 375), npxxy=(209, 426),
                 d_tilt=11.445926, d_npxxy=10.030448, tm6=(366, 398))
ANCH_PRED = HR.ANCHORS["drd2"]         # tilt (76, 375), npxxy (209, 426)

# One window rule for both structures, so the two bundles are the same body.
# 30-443 minus the ICL3 stretch. In the prediction that stretch is 147 residues
# of mean-pLDDT-38.5 coil; in 6CM4 it is where the T4L fusion replaced native
# 223-362 and is simply not modelled. Drawing it in one and not the other would
# make one receptor look like two kinds of object.
BODY = (30, 443)
ICL3 = (ANCH_PRED["npxxy"][0] + 10, ANCH_PRED["tm6"][0] - 1)     # 219-365

# The superposition window. TM6 AND ICL3 are excluded from the fit, so the fit
# cannot absorb the displacement the frame is drawn to show, and the T4L at
# 1002-1161 of 6CM4's chain A cannot be aligned onto anything (D21's practical
# trap: one selection reused across two objects fits the receptor to a fusion).
FIT = [r for r in range(34, 442)
       if not (ICL3[0] <= r <= ICL3[1])
       and not (ANCH_PRED["tm6"][0] <= r <= ANCH_PRED["tm6"][1])]

PEP = ("B", 334, 354)                  # the alpha5 C-terminal 21-mer

C_ACTIVE = fs.VERM        # the predicate calls this ACTIVE
C_INACTIVE = fs.BLUE      # ... or inactive
C_PEPTIDE = fs.GREEN      # the alpha5 21-mer, and the cognate arm in the ruler
C_APO = "#6E6E6E"
C_HEAD = "#1A1A1A"

XCOL = "d_gpcrdb_tm6_tilt_246_637_ca"


# --------------------------------------------------------------------------
# small structure helpers - local, so nothing outside this file is touched
# --------------------------------------------------------------------------
def _kept(lo, hi):
    """The residue spans actually drawn: the window minus ICL3."""
    out = []
    for a, b in ((lo, min(hi, ICL3[0] - 1)), (max(lo, ICL3[1] + 1), hi)):
        if b > a:
            out.append((a, b))
    return out


def _body_runs(atoms, chain):
    runs = []
    for a, b in _kept(*BODY):
        runs.extend(D.ca_runs(atoms, chain, a, b))
    return runs


def _body_heavy(atoms, chain):
    keep = _kept(*BODY)
    return np.array([x["xyz"] for x in atoms
                     if x["chain"] == chain and x["elem"] != "H"
                     and x["group"] == "ATOM"
                     and any(a <= x["resi"] <= b for a, b in keep)])


def _smooth(P, win=4):
    """A 4-residue running mean of a Ca run - i.e. the helix AXIS.

    Prevents: two interleaved corkscrews. `dofrender.ribbon` draws the Ca path
    itself, and the Ca path of an alpha helix is a coil with a 5.4 A pitch. One
    such coil reads as a helix; TWO of them superposed, 6 A apart, read as a
    tangle, and the first build of this frame was exactly that - the reader
    could not tell which turn belonged to which structure. A running mean over
    one helical turn collapses the coil onto its axis, which is what a cartoon
    tube is and what `ye2026multistatebias` Fig 4A draws.

    NOTHING MEASURED PASSES THROUGH HERE. The dashes, their endpoints and every
    printed value are computed from unsmoothed atom coordinates; this touches
    only the tubes and the hairline traces, and the panel says so.
    """
    P = np.asarray(P, float)
    if len(P) < win + 1:
        return P
    out = np.empty_like(P)
    for i in range(len(P)):
        lo = max(0, i - win // 2)
        hi = min(len(P), lo + win)
        lo = max(0, hi - win)
        out[i] = P[lo:hi].mean(axis=0)
    return out


def _tm6(atoms, chain, anch):
    runs = D.ca_runs(atoms, chain, anch["tm6"][0], anch["tm6"][1])
    return max(runs, key=len) if runs else np.zeros((0, 3))


def _fit_rt(mob_atoms, tgt_atoms, mob_chain, tgt_chain, resids):
    """Kabsch fit of `mob` onto `tgt` over an EXPLICIT residue set.

    `dofrender.superpose` takes a contiguous window; this frame needs a set
    with two holes in it (ICL3, and TM6 - the element under discussion), so the
    fit is written out here rather than by widening a shared function that
    three other panels are reading. Same maths, same failure mode guarded: the
    pairing is residue by residue inside a named set, so no fusion partner can
    enter the superposition.
    """
    def ca(atoms, chain):
        return dict((a["resi"], a["xyz"]) for a in atoms
                    if a["name"] == "CA" and a["chain"] == chain
                    and a["group"] == "ATOM")

    m, t = ca(mob_atoms, mob_chain), ca(tgt_atoms, tgt_chain)
    pairs = [(m[r], t[r]) for r in resids if r in m and r in t]
    if len(pairs) < 100:
        raise ValueError("fit: only %d shared CA" % len(pairs))
    A = np.array([p[0] for p in pairs])
    Bt = np.array([p[1] for p in pairs])
    ca_, cb_ = A.mean(0), Bt.mean(0)
    H = (A - ca_).T @ (Bt - cb_)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1.0, 1.0, d]) @ U.T
    t_ = cb_ - ca_ @ R.T
    dev = np.linalg.norm((A @ R.T + t_) - Bt, axis=1)
    rms = float(np.sqrt((dev ** 2).mean()))
    return R, t_, len(pairs), rms, float(np.median(dev))


def _clash(ref_atoms, pred_atoms, R, t):
    """How far the INACTIVE TM6 intrudes into the site the alpha5 occupies.

    Why this is in the frame at all. Superposed, 6CM4's TM6 lands on top of the
    alpha5 21-mer, and a reader who is not told why sees a rendering fault - two
    coloured tubes passing through each other. It is not a fault, it is the
    mechanism: the inactive TM6 position and the alpha5's site are the same
    volume, so they are mutually exclusive.

    THIS IS NOT A CONTACT and the panel must not call it one. A 0.22 A
    heavy-atom separation is a clash; reporting it as a contact distance
    invites the obvious objection. The quantity is MUTUAL EXCLUSION OF VOLUME -
    how many of the alpha5's own heavy atoms lie inside 4 A of the deposited
    TM6 - and it is reported against a floor: the same count against the
    PREDICTION's own TM6, which is what "no exclusion" looks like on this
    scale. `figures/block_a/steric_exclusion.py` runs the full version with the
    deposited-ACTIVE control and a second receptor.
    """
    tm6 = [a for a in ref_atoms if a["chain"] == "A" and a["elem"] != "H"
           and a["group"] == "ATOM"
           and ANCH_6CM4["tm6"][0] <= a["resi"] <= ANCH_6CM4["tm6"][1]]
    pep = [a for a in pred_atoms if a["chain"] == PEP[0] and a["elem"] != "H"
           and a["group"] == "ATOM" and PEP[1] <= a["resi"] <= PEP[2]]
    own = [a for a in pred_atoms if a["chain"] == "A" and a["elem"] != "H"
           and a["group"] == "ATOM"
           and ANCH_PRED["tm6"][0] <= a["resi"] <= ANCH_PRED["tm6"][1]]
    Y = np.array([a["xyz"] for a in pep])

    def burial(X):
        d = np.linalg.norm(np.asarray(X)[:, None, :] - Y[None, :, :], axis=2)
        i, j = np.unravel_index(np.argmin(d), d.shape)
        return d, int((d.min(axis=0) < 4.0).sum()), int((d < 3.0).sum()), i, j

    X = D.apply_rt([a["xyz"] for a in tm6], R, t)
    d, pep4, n3, i, j = burial(X)
    _, own4, _, _, _ = burial([a["xyz"] for a in own])
    return dict(pep4=pep4, n3=n3, own4=own4, n_pep=len(Y),
                dmin=float(d.min()),
                pair=u"%s%d %s – %s%d %s"
                     % (tm6[i]["resn"].title(), tm6[i]["resi"], tm6[i]["name"],
                        pep[j]["resn"].title(), pep[j]["resi"], pep[j]["name"]))


def _verify_6cm4():
    """Refuse to draw 6CM4 until it reproduces BOTH shipped reference values.

    The file is not in the drop, so this is the only thing standing between the
    figure and a downloaded structure being the wrong entry - which has already
    happened once inside the drop itself: 8FZQ.cif in
    `agonist_only_vs_ternary/` is CFTR, not a receptor complex (D18).
    """
    a = ANCH_6CM4
    c = a["chain"]
    dt = CR.verify_anchor(REF_INACTIVE, (c, a["tilt"][0], "CA"),
                          (c, a["tilt"][1], "CA"), a["d_tilt"],
                          what="6CM4 tilt")
    dn = CR.verify_anchor(REF_INACTIVE, (c, a["npxxy"][0], "OH"),
                          (c, a["npxxy"][1], "OH"), a["d_npxxy"],
                          what="6CM4 NPxxY")
    return dt, dn


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------
# the render
# --------------------------------------------------------------------------
def render(ax, aspect, view="side"):
    """The single frame. Returns everything printed, for the provenance block."""
    dt_p, dn_p = HR.verify(PRED, "drd2", "DRD2 row 8285")
    dt_i, dn_i = _verify_6cm4()

    pred = CR.frame(PRED)
    ref = CR.frame(REF_INACTIVE)
    R, t, npair, rms, med = _fit_rt(ref, pred, "A", "A", FIT)
    # The same fit rule against DRD2's deposited ACTIVE reference, which is NOT
    # drawn. One atom set, two references, so the two RMSDs are comparable -
    # which the shipped `rmsd_to_active_ref` is not, because it does not
    # reproduce from the coordinates and its atom set is documented nowhere in
    # the drop (D22). Quoted in the chip, never drawn as a measurement.
    _, _, npair_a, rms_a, _ = _fit_rt(CR.frame(REF_ACTIVE), pred, "R", "A", FIT)

    # camera: the same rule every other render in this figure set uses, fed the
    # 7TM body with ICL3 excluded (camera.py fits the axis to every CA in the
    # window, and DRD2's predicted ICL3 bends it by 35.5 degrees).
    ca = np.vstack(_body_runs(pred, "A"))
    frame = D.camera_frame(PRED, ("A", BODY[0], BODY[1]),
                           (("A", ANCH_PRED["tilt"][0]),
                            ("A", ANCH_PRED["tilt"][1])), view, ca=ca)

    pep = _smooth(np.vstack(D.ca_runs(pred, PEP[0], PEP[1], PEP[2])))
    ref_ca = np.vstack([D.apply_rt(r, R, t) for r in _body_runs(ref, "A")])

    P = frame.project(ca)
    Q = frame.project(pep)
    Rp = frame.project(ref_ca)
    xlim, ylim = D.frame_limits([P[:, :2], Q[:, :2], Rp[:, :2]], aspect,
                                pad=1.05)
    allz = np.concatenate([P[:, 2], Q[:, 2], Rp[:, 2]])
    ds = (float(allz.min()), float(allz.max()))

    # --- the claim, and where focus goes ---------------------------------
    tm6_p = frame.project(_smooth(_tm6(pred, "A", ANCH_PRED)))
    tm6_i = frame.project(_smooth(D.apply_rt(_tm6(ref, "A", ANCH_6CM4), R, t)))
    anch_p = frame.project([CR.atom(pred, "A", ANCH_PRED["tilt"][0], "CA"),
                            CR.atom(pred, "A", ANCH_PRED["tilt"][1], "CA")])
    anch_i = frame.project(D.apply_rt(
        [CR.atom(ref, "A", ANCH_6CM4["tilt"][0], "CA"),
         CR.atom(ref, "A", ANCH_6CM4["tilt"][1], "CA")], R, t))
    claim = [tm6_p, tm6_i, anch_p, anch_i, Q]
    focus = D.focal_plane(*claim)
    behind = D.focus_report(claim, focus, ds, "GA-style3 %s" % view)

    # --- is the picture allowed to draw these two segments at all? --------
    # An orthographic projection foreshortens a distance by the cosine of its
    # angle to the image plane, and it does so INDEPENDENTLY for each of the
    # two segments. If the two are foreshortened by different amounts, the
    # picture shows a ratio the data does not have - the reader compares the
    # drawn lengths, not the printed numbers. No render in the corpus survey
    # checks this. Here it is checked and reported, and a view that distorts
    # either segment by more than 5% is refused.
    fid = {}
    for name, xy, true in (("prediction", anch_p, dt_p), ("6cm4", anch_i, dt_i)):
        fid[name] = float(np.linalg.norm(xy[0, :2] - xy[1, :2]) / true)
    if min(fid.values()) < 0.95:
        raise ValueError(
            "GA-style3 %s: a measured segment is drawn at %.0f%% of its length "
            "(prediction %.3f, 6CM4 %.3f). The frame would show a ratio the "
            "data does not have. Use the other view."
            % (view, 100 * min(fid.values()), fid["prediction"], fid["6cm4"]))

    D.setup_axes(ax, xlim, ylim)

    # --- grey: the invariant scaffold, and only that ----------------------
    # ONE density, from the prediction, plus two hairline traces. Two densities
    # is blur over blur and at 8 cm it reads as fog; the two RMSDs in the chip
    # are what state how far apart the scaffolds actually are.
    D.depth_of_field_cloud(ax, frame.project(_body_heavy(pred, "A")),
                           D.SCAFFOLD, xlim, ylim, depth_span=ds,
                           far=(2.9, 0.30), near=(1.15, 0.58), zorder=1.0,
                           focus_at=focus)
    D.thin_trace(ax, [frame.project(_smooth(r)) for r in _body_runs(pred, "A")],
                 colour="#78736C", alpha=0.70, depth_span=ds, lw=1.30, per=3)
    D.thin_trace(ax, [frame.project(_smooth(D.apply_rt(r, R, t)))
                      for r in _body_runs(ref, "A")],
                 colour="#B2ACA4", alpha=0.80, depth_span=ds, lw=1.00, per=3)

    # --- colour: TM6 twice, and the drawn part of the supplied Ga ---------
    D.blurred_layer(ax, [Q], C_PEPTIDE, xlim, ylim, ds, sigma_A=1.2,
                    base_alpha=0.34, zorder=1.4)
    D.ribbon(ax, tm6_i, C_INACTIVE, lw=4.2, depth_span=ds, zorder=5.7,
             halo_extra=2.2)
    D.ribbon(ax, tm6_p, C_ACTIVE, lw=4.6, depth_span=ds, zorder=6.1,
             halo_extra=2.2)
    D.ribbon(ax, Q, C_PEPTIDE, lw=4.6, depth_span=ds, zorder=6.5,
             halo_extra=2.2)

    return dict(frame=frame, xlim=xlim, ylim=ylim, ds=ds, focus=focus,
                behind=behind, pred=pred, ref=ref, R=R, t=t,
                npair=npair, rms=rms, med=med, npair_a=npair_a, rms_a=rms_a,
                clash=_clash(ref, pred, R, t),
                endpoint_gap=float(np.linalg.norm(
                    D.apply_rt([CR.atom(ref, "A", ANCH_6CM4["tilt"][0],
                                        "CA")], R, t)[0]
                    - CR.atom(pred, "A", ANCH_PRED["tilt"][0], "CA"))),
                dt_p=dt_p, dn_p=dn_p, dt_i=dt_i, dn_i=dn_i, fid=fid,
                anch_p=anch_p, anch_i=anch_i, tm6_p=tm6_p, tm6_i=tm6_i,
                view=frame.label)


def annotate(ax, S, lab_p, lab_i, key_loc, chip_loc, sb_yfrac):
    """The two measurements, the key and the chip.

    A 7TM bundle seen from the side is about twice as tall as it is wide, and
    this frame is landscape, so there is a text column of empty ground either
    side of the molecule. That is not waste: it is where the four blocks the
    panel must carry - the selection rule, the colour key, and the two values
    with their atom pairs - sit without ever landing on the structure. Both
    value labels are placed OUT in those columns with leader lines back to the
    dashes they belong to, one on each side, so neither can be read as
    belonging to the other helix.

    `lab_p` / `lab_i` are absolute label positions in Angstrom, not offsets:
    the two dashes very nearly share their 2x46 endpoint, so their midpoints
    are 3 A apart and offsets from them are not a usable way to place two
    labels on opposite sides of the frame.
    """
    pred, ref = S["pred"], S["ref"]
    n_p = dict((r, CR.residue_name(pred, "A", r)) for r in ANCH_PRED["tilt"])
    n_i = dict((r, CR.residue_name(ref, "A", r)) for r in ANCH_6CM4["tilt"])
    t1, t2 = ANCH_PRED["tilt"]

    for p, colour in ((S["anch_p"], C_ACTIVE), (S["anch_i"], C_INACTIVE)):
        for xy in p[:, :2]:
            ax.scatter([xy[0]], [xy[1]], s=24, c=[colour], linewidths=0.6,
                       edgecolors="white", zorder=8.7)

    # THE DIFFERENTIATOR. Same pair, both structures, both values, each with
    # the residues it was measured on and the file it came from.
    for xy, lab, colour, names, value, note, ha in (
            (S["anch_p"], lab_p, C_ACTIVE, n_p, S["dt_p"],
             u"prediction + cognate Gα\nrow 8285", "left"),
            (S["anch_i"], lab_i, C_INACTIVE, n_i, S["dt_i"],
             u"6CM4\ndeposited inactive DRD2", "right")):
        mid = 0.5 * (xy[0, :2] + xy[1, :2])
        D.measured_distance(
            ax, xy[0, :2], xy[1, :2], u"%.2f Å" % value,
            u"%s%d (2×46) Cα –\n%s%d (6×37) Cα"
            % (names[t1].title(), t1, names[t2].title(), t2),
            colour, offset=(lab[0] - mid[0], lab[1] - mid[1]), ha=ha,
            fontsize=11.0, pair_fontsize=5.6, lw=1.6, note=note)

    D.colour_key(ax, [(u"TM6 — prediction + cognate Gα · predicate ACTIVE",
                       C_ACTIVE),
                      (u"TM6 — 6CM4, deposited INACTIVE DRD2", C_INACTIVE),
                      (u"α5 C-terminal 21-mer (Gα 334–354) — drawn from the "
                       u"supplied Gα", C_PEPTIDE),
                      (u"DRD2 bundle, both structures — not the subject",
                       "#8A8A8A")],
                 loc=key_loc, fontsize=5.4, dy=0.040)

    D.chip(ax, u"DRD2 · cognate Gα · OpenFold-3 · row 8285 · %s\n"
               u"selection: the MEDIAN rmsd_to_active_ref row of its 25-seed\n"
               u"cell (rank 13 of 25) — a typical row, not a best case\n"
               u"superposed on %d receptor Cα with TM6 and ICL3 OUT of the fit,\n"
               u"so it cannot absorb the displacement it is drawn to show: %.2f Å\n"
               u"(same rule vs 7JVR, the deposited ACTIVE reference: %.2f Å)"
               % (S["view"], S["npair"], S["rms"], S["rms_a"]),
           loc=chip_loc, fontsize=5.1)

    # WHY THE BLUE HELIX AND THE GREEN ONE PASS THROUGH EACH OTHER. Without
    # this the overlap reads as a rendering fault. It is the mechanism, and it
    # is measured on the coordinates drawn, with the closest pair named.
    c = S["clash"]
    D.chip(ax, u"THE INACTIVE TM6 OCCUPIES THE α5 VOLUME — the two tubes overlap\n"
               u"because the two states cannot both be occupied. %d of the α5's %d\n"
               u"heavy atoms lie within 4 Å of 6CM4's TM6 (%d pairs < 3 Å; closest\n"
               u"%.2f Å, %s — a clash, not a contact).\n"
               u"Against the prediction's OWN TM6: %d of %d. Mutual exclusion of\n"
               u"volume, not a measured contact distance."
               % (c["pep4"], c["n_pep"], c["n3"], c["dmin"], c["pair"],
                  c["own4"], c["n_pep"]),
           loc="lower left", fontsize=4.9)
    D.scale_bar(ax, y_frac=sb_yfrac, pad=0.855, fontsize=5.4)


# --------------------------------------------------------------------------
# the ruler - the population the one drawn row came from
# --------------------------------------------------------------------------
def _density(values, lo, hi, n=360, sigma_bins=6):
    v = np.asarray(values, float)
    v = v[np.isfinite(v)]
    edges = np.linspace(lo, hi, n + 1)
    h, _ = np.histogram(v, bins=edges)
    k = np.exp(-0.5 * (np.arange(-4 * sigma_bins, 4 * sigma_bins + 1)
                       / float(sigma_bins)) ** 2)
    k = k / k.sum()
    y = np.convolve(h.astype(float), k, mode="same")
    return 0.5 * (edges[:-1] + edges[1:]), y, len(v)


def ruler(ax, drd2, dt_p, dt_i, xlo=10.6, xhi=19.6):
    """DRD2's own 200 rows on the axis the render measures.

    It has to read as a ruler under the picture, not as a second panel: one
    axis, no box, no y scale, no grid. It is here because the commonest thing
    wrong with a structure render in this literature after the unstated
    selection rule is that no quantitative panel stands behind it (58 of 232
    rows). The render is one row of the green distribution.

    DEPOSITED REFERENCES GO BELOW THE AXIS, prediction rows above it. Marking a
    crystal structure inside a cloud of predictions without separating them is
    a category mix, and at ruler scale it is invisible.
    """
    peak = 0.0
    stats = {}
    curves = {}
    for arm, colour in ((u"apo", C_APO), (u"cognate", C_PEPTIDE)):
        s = drd2[drd2["arm"] == arm][XCOL]
        x, y, n = _density(s, xlo, xhi)
        peak = max(peak, y.max())
        stats[arm] = (n, float(np.median(s.dropna())))
        curves[arm] = (x, y, n, colour)
        ax.fill_between(x, 0, y, color=colour, alpha=0.32, linewidth=0,
                        zorder=2)
        ax.plot(x, y, color=colour, lw=0.9, zorder=3)

    # Everything above the axis, on three levels that cannot collide:
    #   0    -> 1.0   the two distributions
    #   1.05 -> 1.30  the arm labels, each pushed AWAY from the crowded middle
    #   1.55 -> 1.85  the two deposited references
    # and nothing below it but the scale itself, so the tick numbers are free.
    for arm, ha, dx, label in (
            (u"apo", "left", 0.14, u"apo — sequence alone"),
            (u"cognate", "right", -0.14, u"+ cognate Gα")):
        x, y, n, colour = curves[arm]
        j = int(np.argmax(y))
        ax.annotate(u"%s   n=%d" % (label, n), (x[j] + dx, peak * 1.04),
                    ha=ha, va="bottom", fontsize=6.0, color=colour,
                    fontweight="bold", zorder=6)

    ax.axvline(B.THR_TILT, color="#9A9A9A", lw=0.6, ls=(0, (2.5, 2)), zorder=1)
    ax.annotate(u"predicate threshold %.3f Å" % B.THR_TILT,
                (B.THR_TILT - 0.12, peak * 0.10), ha="right", va="bottom",
                fontsize=5.0, color="#8A8A8A", zorder=6)

    # the row that is drawn above - a solid stem through its own distribution
    ax.plot([dt_p, dt_p], [0, peak * 1.00], color=C_ACTIVE, lw=1.3,
            solid_capstyle="butt", zorder=7)
    ax.scatter([dt_p], [peak * 1.00], s=11, c=[C_ACTIVE], linewidths=0,
               zorder=7)
    ax.annotate(u"row 8285 — drawn above", (dt_p + 0.12, peak * 1.04),
                ha="left", va="bottom", fontsize=5.4, color=C_ACTIVE,
                fontweight="bold", zorder=7)

    # DEPOSITED REFERENCES ARE NOT PREDICTIONS and are kept off the axis the
    # predictions live on: a dotted drop line and a caret, on their own level.
    for value, colour, tag, ha, dx in (
            (dt_i, C_INACTIVE, u"6CM4 · deposited inactive", "left", 0.12),
            (REF_ACTIVE_TILT, "#7A736B", u"7JVR · deposited active",
             "left", 0.10)):
        ax.plot([value, value], [0, peak * 1.50], color=colour, lw=0.7,
                ls=(0, (1.6, 1.6)), alpha=0.75, zorder=6)
        ax.scatter([value], [peak * 1.50], s=13, marker="v", c=[colour],
                   linewidths=0, zorder=7)
        ax.annotate(tag, (value + dx, peak * 1.56), ha=ha, va="bottom",
                    fontsize=5.4, color=colour, zorder=7)

    ax.set_xlim(xlo, xhi)
    ax.set_ylim(0, peak * 1.95)
    ax.set_yticks([])
    ax.tick_params(axis="x", labelsize=5.8, length=2.2, width=0.5, pad=1.6)
    for side in ("left", "right", "top"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_linewidth(0.5)
    ax.spines["bottom"].set_position(("data", 0.0))
    return stats


# --------------------------------------------------------------------------
def provenance(S, stats, classA):
    """The block that goes to figures/block_a/PROV_style3.md, verbatim."""
    c = S["clash"]
    return u"""GA-STYLE-3 — provenance and required caption content.

WHAT IS DRAWN. One frame, no panels. DRD2 (dopamine D2 receptor) predicted by
OpenFold-3 with the cognate Ga supplied as a co-input (block_a_rows.csv row
8285), superposed on 6CM4 — DRD2's deposited INACTIVE panel reference — over %d
receptor Ca (34–218 and 399–441): %.3f A, median per-residue deviation %.2f A,
the tail being ECL2. TM6 (366–398) and ICL3 are excluded from the
superposition, so the fit cannot absorb the displacement the frame is drawn to
show. The same fit rule against 7JVR, DRD2's deposited ACTIVE reference, which
is NOT drawn: %.3f A over %d Ca. View: %s. Grey is the receptor bundle, both
structures, and carries no claim; colour appears only on TM6 of each structure
and on the alpha5 C-terminal 21 residues.

THE INPUT WAS THE FULL COGNATE Ga SUBUNIT (chain B, 354 residues). Only its
alpha5 C-terminal 21 residues (Ga 334–354) are DRAWN, which is what the claim
is about and what this literature does (tejero2024opsin Fig 5: "Only the alpha5
helix of the Ga subunit is shown"). BLOCK A DOES NOT TEST A 21-RESIDUE PEPTIDE
CO-INPUT — that is Block B, and CLAIMS.md forbids any Block A sentence that
implies the peptide result. Nothing in the caption may call the drawn 21-mer
"the co-input"; the panel's subtitle, colour key and footnote all state that
the input was the whole subunit.

THE MEASUREMENT, ONE PAIR, TWO VALUES.
  prediction, row 8285   %.4f A   Leu76 (2x46) CA – Leu375 (6x37) CA
  6CM4, deposited        %.4f A   Leu76 (2x46) CA – Ala375 (6x37) CA
  difference             %.4f A
Both were reproduced from the coordinates being drawn before being drawn
(cifread.verify_anchor, tolerance 2e-3 A). The prediction's value reproduces
row 8285's stored d_gpcrdb_tm6_tilt_246_637_ca = 17.2766 A; 6CM4's reproduces
reference_predicates.csv's d_tilt_ref = 11.445926 A. 6x37 is Leu in the
prediction and Ala in 6CM4 — a construct difference in the deposited entry. The
measured atom is CA in both, so the pair is the same pair; it is named on the
panel for each structure separately rather than once, because printing one
residue name over two different constructs is how hilger2020gcgr ends up
reporting 17.4 A and 18 A for one displacement. The two dashes share their 2x46
endpoint: after the fit those two CA are %.3f A apart.

PROJECTION FIDELITY, which no render in the survey states. An orthographic
projection foreshortens each segment independently, so two segments can be
drawn at a ratio the data does not have. Here they are drawn at %.1f%% and
%.1f%% of their measured lengths; the panel refuses any view that distorts
either by more than 5%%, and the cytoplasmic view is refused on exactly that
test (89.9%% and 79.0%%).

The NPxxY axis was verified for both structures and is NOT drawn: prediction
3.9883 A, 6CM4 10.0304 A. One frame carries one pair. The second axis is BA-1a.

6CM4 IS NOT IN THE DROP. `11_structures/` ships 7JVR (DRD2 active) and no
inactive DRD2, so 6CM4.cif was fetched from RCSB into figures/structures/.
  sha256 %s
It is verified against BOTH values the drop stores for it — 11.445926 A tilt
and 10.030448 A NPxxY-OH — at the same residue numbers, from its own
coordinates. No ALIGNMENT.md was consulted; four of them name residues that do
not reproduce their own shipped distances (D13, D20), and one shipped CIF is
the wrong protein entirely (D18). 6CM4 carries a T4L fusion replacing native
223–362; the fusion is renumbered 1002–1161 in the file, lies outside both the
drawn window and the fit window, and contains none of the four anchor atoms.
reference_metadata.csv flags `predicate_window_hit = both` for this entry,
which is a caveat about the deposited construct and not about this drawing.

SELECTION RULE, on the panel and here. DRD2 x OpenFold-3 x cognate cell,
n = 25 seeds: the row with the MEDIAN rmsd_to_active_ref in the cell (1.218 A
shipped; rank 13 of 25, cell range 1.020–1.507 A). A typical row of its cell,
not a best case; the predicate calls all 25 rows of that cell active. The
shipped RMSD does not reproduce from the coordinates (D22) and is therefore
quoted only as the statistic the row was selected on, never as something this
picture measures — which is why the two RMSDs printed on the panel are computed
here, on one stated atom set, for both references. 6CM4 was not selected: it is
the only inactive DRD2 panel reference in reference_predicates.csv.

STERIC EXCLUSION — the annotation in the lower left, and why the blue and green
tubes overlap. Superposed, 6CM4's TM6 lands in the volume the alpha5 occupies.
%d of the alpha5's %d heavy atoms lie within 4.0 A of a 6CM4 TM6 heavy atom
(%d pairs below 3.0 A; closest %.2f A, %s). Against the
PREDICTION's OWN TM6 the same count is %d of %d, which is what "no exclusion"
looks like on this scale. This is MUTUAL EXCLUSION OF VOLUME and must never be
reported as a contact — a %.2f A heavy-atom separation is a clash, and calling
it a contact invites the obvious objection. Atom sets, controls, and a second
receptor are in `figures/block_a/steric_exclusion.py`; its result is summarised
in PROV_style3.md. The active control is NOT zero and must not be reported as
though it were.

THE RULER. DRD2's own rows under E1+E2: %d apo and %d cognate, 4 backbones x
25 seeds x 2 arms, smoothed on the same tilt axis the render measures. Apo
median %.2f A, cognate median %.2f A. Both of DRD2's deposited references are
marked with dotted drop lines and carets (6CM4 11.446 A, 7JVR 17.586 A) and the
drawn row with a solid stem, so a crystal structure is never mixed into a cloud
of predictions. For scale beyond this receptor, Class A under E1+E2: apo median
%.2f A (n=%s), cognate median %.2f A (n=%s) — stated as text on the figure, not
drawn, because this frame is about one receptor.

WHAT THE FRAME DOES NOT SHOW.
  * That the apo prediction stays closed. The blue helix is a crystal
    structure. DRD2's apo predictions are the grey distribution in the ruler;
    their coordinates are not in the drop.
  * Amplitude reproduction (BA-4), which is negative on three of four
    backbones. There is no arrow in the frame for that reason.
  * Anything about confidence. Row 8285 was selected on RMSD, not pLDDT.
  * A 21-residue peptide co-input. See above.

REPRESENTATION. The tubes and the hairline traces are the CA path smoothed with
a 4-residue running mean — the helix axis, which is what a cartoon tube is.
Without it two superposed CA coils 6 A apart read as a tangle. NOTHING MEASURED
PASSES THROUGH THE SMOOTHING: every dash, endpoint, printed value, RMSD and
steric count is computed from unsmoothed atom coordinates.

FOCUS. Both TM6 runs, all four tilt anchor atoms and the whole alpha5 are
passed to dofrender.focal_plane(); the focal plane sits at the back of that set
and focus_report() confirms nothing state-defining is behind it (%.0f%% of the
panel's depth range lies behind the plane and is softened). Soft focus encodes
depth only and carries no interpretive meaning. The caption must say so.

CAMERA. dofrender.camera_frame, i.e. block_a/camera.py's rule, fed the 7TM body
with ICL3 excluded. Not chosen by eye. camera.py fits the bundle axis to every
CA in the window and DRD2's predicted ICL3 (147 residues, mean pLDDT 38.5)
bends it by 35.5 degrees.""" % (
        S["npair"], S["rms"], S["med"], S["rms_a"], S["npair_a"], S["view"],
        S["dt_p"], S["dt_i"], S["dt_p"] - S["dt_i"], S["endpoint_gap"],
        100 * S["fid"]["prediction"], 100 * S["fid"]["6cm4"],
        _sha256(REF_INACTIVE),
        c["pep4"], c["n_pep"], c["n3"], c["dmin"], c["pair"],
        c["own4"], c["n_pep"], c["dmin"],
        stats["apo"][0], stats["cognate"][0],
        stats["apo"][1], stats["cognate"][1],
        classA["apo"][1], "{:,}".format(classA["apo"][0]),
        classA["cognate"][1], "{:,}".format(classA["cognate"][0]),
        100 * S["behind"])


# --------------------------------------------------------------------------
VIEW_GEOM = {
    # per view: absolute label positions (A), key corner, chip corner,
    # scale-bar height. The two text columns either side of the bundle are the
    # composition, not slack: chip top-left, key top-right, and the two values
    # low, one in each column, with leaders back to their own dashes.
    "side": dict(lab_p=(27.0, 1.0), lab_i=(-26.0, -8.0),
                 key_loc="upper right", chip_loc="upper left",
                 sb_yfrac=0.045),
    "cytoplasmic": dict(lab_p=(24.0, -14.0), lab_i=(-22.0, -14.0),
                        key_loc="upper right", chip_loc="upper left",
                        sb_yfrac=0.045),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--view", default="side",
                    choices=["side", "cytoplasmic"])
    ap.add_argument("--stem", default="ga_style3_superposition")
    a = ap.parse_args()

    fs.use_house_style()

    rows = B.rows()
    core, label, n_core = B.core(rows)
    drd2 = core[core["receptor"] == "DRD2"]
    cA = core[core["gpcr_class"] == "A"]
    classA = dict((arm, (int(cA["arm"].eq(arm).sum()),
                         float(cA[cA["arm"] == arm][XCOL].median())))
                  for arm in ("apo", "cognate"))

    # 132 x 84 mm. A single wide frame: the bundle fills the height and the
    # empty ground left and right is where the two value labels and the key go,
    # so no annotation has to sit on top of the structure. Reduction to the
    # 80 mm a TOC entry gets is x0.61, which keeps the two values above 5 pt.
    fig = plt.figure(figsize=(140 * fs.MM, 108 * fs.MM))
    gs = fig.add_gridspec(1, 1, left=0.010, right=0.990, top=0.915,
                          bottom=0.315)
    aspect = D.cell_aspect(fig, gs, 0, 0)
    ax = fig.add_subplot(gs[0, 0])

    S = render(ax, aspect, view=a.view)
    annotate(ax, S, **VIEW_GEOM[a.view])

    fig.text(0.010, 0.990,
             u"One receptor, two TM6 positions, one atom pair",
             ha="left", va="top", fontsize=11.0, fontweight="bold",
             color=C_HEAD)
    fig.text(0.010, 0.955,
             u"DRD2 predicted with its cognate Gα (OpenFold-3, row 8285), "
             u"superposed on 6CM4 — the same receptor's deposited inactive "
             u"structure",
             ha="left", va="top", fontsize=6.4, color="#555555")

    axr = fig.add_axes([0.085, 0.180, 0.830, 0.098])
    stats = ruler(axr, drd2, S["dt_p"], S["dt_i"])
    axr.set_xlabel(u"TM6 tilt · Leu76 (2×46) Cα – Leu375 (6×37) Cα (Å) — "
                   u"every DRD2 prediction, both arms, 4 backbones × 25 seeds, "
                   u"E1+E2",
                   fontsize=6.0, labelpad=1.5)

    # Wrapped by hand: savefig.bbox is "tight", so one line wider than the
    # figure silently widens the canvas and squeezes everything else left.
    fig.text(0.5, 0.010,
             u"THE INPUT WAS THE FULL COGNATE Gα SUBUNIT; only its α5 "
             u"C-terminal 21 residues are drawn. Block A does not test a "
             u"21-residue peptide co-input — that is Block B.\nGrey is the "
             u"invariant bundle and carries no claim; colour is TM6 and the α5 "
             u"only. Soft focus encodes DEPTH ONLY and carries no interpretive "
             u"meaning. The blue helix is a\ndeposited structure, not an apo "
             u"prediction: that arm is the grey distribution above. No arrow — "
             u"this frame shows the state REACHED, not amplitude reproduction\n"
             u"(BA-4, negative on 3 of 4 backbones). Class A, E1+E2: apo "
             u"median %.2f Å (n=%s), cognate %.2f Å (n=%s). Selection rule, "
             u"sha256 and the steric controls in PROV_style3.md."
             % (classA["apo"][1], "{:,}".format(classA["apo"][0]),
                classA["cognate"][1], "{:,}".format(classA["cognate"][0])),
             ha="center", va="bottom", fontsize=5.0, color="#7A7A7A",
             linespacing=1.55)

    D.raster_dpi(fig)
    paths = fs.save(fig, a.stem)
    print("written:", *paths, sep="\n  ")
    print("  view            %s" % S["view"])
    print("  fit             %d Ca, %.3f A RMSD" % (S["npair"], S["rms"]))
    print("  prediction tilt %.4f A   NPxxY %.4f A" % (S["dt_p"], S["dn_p"]))
    print("  6CM4       tilt %.4f A   NPxxY %.4f A" % (S["dt_i"], S["dn_i"]))
    print("  difference      %.4f A" % (S["dt_p"] - S["dt_i"]))
    print("  behind focus    %.0f%%" % (100 * S["behind"]))
    print("  ruler           %d apo / %d cognate DRD2 rows"
          % (stats["apo"][0], stats["cognate"][0]))
    print("\n" + provenance(S, stats, classA))


if __name__ == "__main__":
    main()
