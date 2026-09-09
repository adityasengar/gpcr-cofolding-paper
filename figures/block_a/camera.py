"""
Derive a PyMOL camera from the geometry, so the view is a stated rule.

The camera is the one thing a command line chooses badly, and it is also the
one thing that makes a render arguable: a reader cannot tell whether a helix
looks displaced because it is or because the view was turned until it did. Two
of the corpus's render defects are camera defects in disguise - part of the
prediction cropped out of frame, and a set of small multiples in which the
cells are not on one footing.

So every render in this figure set gets its view from a rule over the
coordinates, written down here, rather than from a mouse:

  vertical    the first principal axis of the receptor Ca cloud - the membrane
              normal for a 7TM bundle - signed so the EXTRACELLULAR end is up,
              which is the field's convention (receptor above, transducer
              below). The sign comes from the mean of the first ten modelled
              Ca, which is the extracellular N-terminus in every class A
              receptor here, against the mean of the two intracellular tilt
              anchors. It deliberately does NOT come from the whole-cloud
              centroid: DRD2's predicted ICL3 is ~130 residues of intracellular
              coil, enough to drag the centroid past the anchors and flip the
              whole image, which it did.
  horizontal  the component of a named in-plane direction perpendicular to
              that axis. For a side view this is the 2x46 -> 6x37 vector, so
              the axis the tilt measures lies across the image.
  depth       the right-handed completion.

`cytoplasmic()` is the same rule rotated 90 degrees to look down the bundle
from the intracellular side, which is the second of the two canonical GPCR
views. A displacement claim wants both: the side view shows the direction of
the movement, the cytoplasmic view shows the cavity it opens.

PyMOL's 18-number view is: 9 rotation-matrix entries in COLUMN-major order,
so that the camera's right / up / out axes, expressed in model coordinates,
are the matrix's rows before flattening and its columns after;
then the camera position relative to the rotation origin (0, 0, -distance);
then the rotation origin in model coordinates; then near, far and the
orthoscopic field-of-view flag.
"""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import cifread as CR                                          # noqa: E402


def _unit(v):
    n = np.linalg.norm(v)
    if n < 1e-9:
        raise ValueError("camera: degenerate direction vector")
    return v / n


def _extracellular_hint(atoms, chain, lo, hi, anchor_pts):
    """
    A direction that points out of the cell, from two landmarks that are
    reliable in every class A receptor here: the modelled N-terminus, which is
    extracellular, and the 2x46 / 6x37 tilt anchors, which are intracellular.
    """
    ca = [(a["resi"], a["xyz"]) for a in atoms
          if a["name"] == "CA" and a["chain"] == chain
          and lo <= a["resi"] <= hi and a["group"] == "ATOM"]
    ca.sort()
    nterm = np.array([x for _, x in ca[:10]]).mean(axis=0)
    return nterm - anchor_pts.mean(axis=0)


def _basis(coords, up_hint, right_hint):
    """Right-handed camera basis from a point cloud and two hints."""
    c = coords.mean(axis=0)
    x = coords - c
    # First principal axis of the Ca cloud: the bundle axis.
    _, _, vt = np.linalg.svd(x, full_matrices=False)
    up = _unit(vt[0])
    if np.dot(up, up_hint) < 0:
        up = -up
    right = right_hint - np.dot(right_hint, up) * up
    right = _unit(right)
    out = np.cross(right, up)
    return right, up, out, c


FOV = 20.0          # degrees; the 18th view number, negative = orthoscopic


def _distance_for(coords, centre, right, up, out, pad, aspect):
    """
    Camera distance that actually FRAMES the molecule.

    PyMOL's view carries a distance, not a zoom: what is visible is
    2 * distance * tan(fov / 2) tall. Setting the distance to the molecule's
    own size - the obvious thing, and what a first attempt here did - crops
    the structure to a handful of helices, which is the corpus's recorded
    "part of the prediction cropped out of the render" defect arriving by
    arithmetic rather than by carelessness. So the half-extents are measured
    in the camera's own basis, the wider of the two is taken after correcting
    for the image aspect, and the distance follows from the field of view.
    """
    d = coords - centre
    half_h = np.abs(d @ up).max() * pad
    half_w = np.abs(d @ right).max() * pad
    half = max(half_h, half_w / float(aspect))
    dist = half / np.tan(np.radians(FOV) / 2.0)
    depth = np.abs(d @ out).max() * pad
    return float(dist), float(depth)


def view_matrix(right, up, out, centre, distance, depth=None, slab=None):
    # PyMOL stores the 3x3 block COLUMN-major. Emitting it row-major produces
    # a plausible-looking but wrong camera - the bundle comes out lying at an
    # angle - which is the kind of error that is invisible in the code and
    # obvious in the picture. Verified empirically against a TM6-coloured
    # test render before this line was written.
    R = np.vstack([right, up, out]).T
    if slab is None:
        if depth is None:
            depth = distance * 0.45
        slab = (max(1.0, distance - depth * 1.6), distance + depth * 1.6)
    return list(R.ravel()) + [0.0, 0.0, -float(distance)] + \
        list(map(float, centre)) + [float(slab[0]), float(slab[1]), -FOV]


def _fmt(view):
    return ", ".join("%.6f" % v for v in view)


def side_view(path, receptor_sel, tilt_anchors, distance=None, pad=1.35,
              flip=False, aspect=1.0, extra_sel=None):
    """
    Membrane normal vertical, intracellular end up, the tilt axis across frame.

    `receptor_sel`  (chain, lo, hi) - the receptor Ca atoms only
    `tilt_anchors`  ((chain, resi), (chain, resi)) - 2x46 and 6x37 Ca; their
                    midpoint defines which end of the bundle is intracellular
                    and their difference defines the horizontal.
    """
    atoms = CR.frame(path)
    ch, lo, hi = receptor_sel
    ca = np.array([a["xyz"] for a in atoms
                   if a["name"] == "CA" and a["chain"] == ch
                   and lo <= a["resi"] <= hi and a["group"] == "ATOM"])
    if len(ca) < 20:
        raise ValueError("camera: only %d CA in %s %s:%d-%d"
                         % (len(ca), os.path.basename(path), ch, lo, hi))
    p = np.array([CR.atom(atoms, c, r, "CA") for c, r in tilt_anchors])
    up_hint = _extracellular_hint(atoms, ch, lo, hi, p)
    right_hint = p[1] - p[0]
    right, up, out, centre = _basis(ca, up_hint, right_hint)
    if flip:
        right, out = -right, -out
    frame_pts = ca if extra_sel is None else np.vstack([ca, extra_sel])
    dist, depth = _distance_for(frame_pts, centre, right, up, out, pad, aspect)
    return view_matrix(right, up, out, centre,
                       distance if distance is not None else dist, depth)


def cytoplasmic_view(path, receptor_sel, tilt_anchors, distance=None,
                     pad=1.9, aspect=1.0, extra_sel=None):
    """The side view rotated 90 deg: looking down the bundle from inside the
    cell. Same rule, same anchors, so the two views are one derivation."""
    atoms = CR.frame(path)
    ch, lo, hi = receptor_sel
    ca = np.array([a["xyz"] for a in atoms
                   if a["name"] == "CA" and a["chain"] == ch
                   and lo <= a["resi"] <= hi and a["group"] == "ATOM"])
    p = np.array([CR.atom(atoms, c, r, "CA") for c, r in tilt_anchors])
    up_hint = _extracellular_hint(atoms, ch, lo, hi, p)
    right_hint = p[1] - p[0]
    right, up, out, centre = _basis(ca, up_hint, right_hint)
    # Look from the CYTOPLASM: the camera's out axis - the one pointing at the
    # viewer - must point intracellular, which is -up. The remaining axis
    # follows from right x new_up = new_out, so the tilt axis stays horizontal
    # in both views and the two are one derivation.
    new_out, new_up, new_right = -up, out, right
    frame_pts = ca if extra_sel is None else np.vstack([ca, extra_sel])
    dist, depth = _distance_for(frame_pts, centre, new_right, new_up, new_out,
                                pad, aspect)
    return view_matrix(new_right, new_up, new_out, centre,
                       distance if distance is not None else dist, depth)


def as_arg(view):
    """The 18 numbers as render_struct.py's --view expects them."""
    return _fmt(view)
