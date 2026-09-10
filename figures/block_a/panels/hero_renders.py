#!/usr/bin/env python3
"""
Build every structure render used by GA-1, BA-8 and S10.

Nothing here picks a residue, a camera or a distance by hand:

  * every anchor pair is VERIFIED against the value stored for that row in the
    tidy data before it is drawn (`cifread.verify_anchor`), because three of
    the shipped ALIGNMENT.md files name the wrong residues (D13) and each of
    them corroborates the others;
  * every camera comes from `camera.py`, a rule over the coordinates;
  * every render goes through `render_struct.py`, which refuses to run without
    `--selected-from` and `--selection-rule` and writes a `.prov.json`;
  * every measured distance is drawn ON the render with its value, because the
    field's characteristic failure on exactly this claim is an arrow labelled
    "activation" with no number anywhere on the panel.

SUPERSEDED, 2026-09-10, for everything except S10. The GA-1, BA-8 and BA-1a
renders are now built in matplotlib with real depth of field by
`figures/dofrender.py` and `dofscenes.py`, and they draw themselves into their
composites - `ga1_hero.py`, `ba8_alpha5.py`, `ba1a_instrument.py` - so the
bitmaps this module writes for `hero_a`, `hero_b`, `hero_c`, `ba8` and `ba1a`
feed nothing. The module stays because it is still the SINGLE SOURCE OF TRUTH
for the anchors, the structure paths, the selection-rule strings and
`verify()`, all of which `dofscenes.py` imports, and because `s10` still goes
through PyMOL.

One camera caveat if a PyMOL render is ever rebuilt from here: `camera.py`
fits the bundle axis to every Ca in the receptor window, and DRD2's predicted
ICL3 (147 residues, mean pLDDT 38.5) bends that axis by 35.5 degrees. The
matplotlib path passes the 7TM body with ICL3 excluded; this one does not.

Run: python3 figures/block_a/panels/hero_renders.py [--dry-run] [name ...]
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = os.path.dirname(HERE)
FIGDIR = os.path.dirname(BLOCK)
ROOT = os.path.dirname(FIGDIR)
sys.path.insert(0, BLOCK)

import camera                                                 # noqa: E402
import cifread as CR                                          # noqa: E402

ST = os.path.join(ROOT, "data", "block_a", "11_structures")
RENDER = os.path.join(FIGDIR, "render_struct.py")
SCENES = os.path.join(BLOCK, "scenes")
OUT = os.path.join(FIGDIR, "out")

AA2AR_APO = os.path.join(ST, "confidently_wrong",
                         "AA2AR__apo__boltz__seed748489558__row567.cif")
DRD2_COG = os.path.join(ST, "success_case",
                        "DRD2__cognate__of3__seed849213874__row8285.cif")
DRD2_REF = os.path.join(ST, "success_case", "7JVR.cif")
ACM1_BROKEN = os.path.join(ST, "broken_cell",
                           "ACM1__cognate__protenix__seed1340440218__row967__BROKEN.cif")
ACM1_HEALTHY = os.path.join(ST, "broken_cell",
                            "ACM1__cognate__chai__seed966761149__row948__HEALTHY.cif")

# ---------------------------------------------------------------------------
# The anchors. Ballmer-Wilson position -> residue, per structure. Each pair
# carries the value the tidy data stores for that row; verify_anchor refuses if
# the coordinates disagree.
# ---------------------------------------------------------------------------
ANCHORS = {
    # AA2AR, row 567 (block_a_rows.csv): tilt 11.7347, NPxxY-OH 9.6079
    "aa2ar": dict(chain="A", tilt=(48, 235), npxxy=(197, 288),
                  d_tilt=11.7347, d_npxxy=9.6079, tm6=(226, 258)),
    # DRD2, row 8285: tilt 17.2766, NPxxY-OH 3.9883
    "drd2":  dict(chain="A", tilt=(76, 375), npxxy=(209, 426),
                  d_tilt=17.2766, d_npxxy=3.9883, tm6=(366, 398)),
    # DRD2 reference 7JVR (reference_predicates.csv): 17.5860 / 4.2522
    "7jvr":  dict(chain="R", tilt=(76, 375), npxxy=(209, 426),
                  d_tilt=17.585960, d_npxxy=4.252152, tm6=(366, 398)),
    # ACM1 rows 967 / 948. The anchor pair is the same; the values are not.
    "acm1_broken":  dict(chain="A", tilt=(67, 367), npxxy=(208, 418),
                         d_tilt=21.5470, d_npxxy=26.6320, tm6=(358, 390)),
    "acm1_healthy": dict(chain="A", tilt=(67, 367), npxxy=(208, 418),
                         d_tilt=17.1660, d_npxxy=4.0160, tm6=(358, 390)),
    # ADRB2 panel references. 4LDE carries a +1000 auth-numbering offset, so
    # its L75/L275 and Y219/Y326 are 1075/1275 and 1219/1326. Both pairs
    # reproduce reference_predicates.csv exactly.
    "4lde": dict(chain="A", tilt=(1075, 1275), npxxy=(1219, 1326),
                 d_tilt=17.562509, d_npxxy=4.813055, tm6=(1266, 1298)),
    "2rh1": dict(chain="A", tilt=(75, 275), npxxy=(219, 326),
                 d_tilt=11.928282, d_npxxy=11.472679, tm6=(266, 298)),
}


# ---------------------------------------------------------------------------
# Selection rules. render_struct.py refuses to run without one, because 59 of
# the corpus's 232 render rows are a hand-picked example with the rule
# unstated. Each of these names the cell, its n, the statistic the row is
# extreme or median on, and the row's percentile within the cell.
# ---------------------------------------------------------------------------
RULE_567 = (
    "AA2AR x Boltz-2 x apo cell, n=25 rows: the row with the HIGHEST "
    "plddt_mean in the cell (73.93; cell median 72.04), i.e. the 100th "
    "percentile on confidence. 11_structures/SELECTION.md states a different "
    "rule ('top-quintile RMSD-to-active, highest pLDDT within') which selects "
    "row 552, not the shipped 567; highest-pLDDT-in-cell is what 567 actually "
    "satisfies. The directory name 'confidently_wrong' is WRONG and is not "
    "repeated anywhere: this row is 0.948 A from the INACTIVE reference and "
    "the predicate calls it inactive, which is where an apo prediction "
    "belongs (DISCREPANCY_REPORT D12). Camera from camera.side_view, a rule "
    "over the coordinates, not chosen by eye. Anchors verified against the "
    "row's own stored d_gpcrdb_tm6_tilt_246_637_ca = 11.7347 A (L48 2x46 CA - "
    "L235 6x37 CA) and d_npxxy_oh = 9.6079 A (Y197 5.58 OH - Y288 7.53 OH); "
    "confidently_wrong/ALIGNMENT.md names L88 and Y213 for two of those four "
    "and is wrong (D13). Quantitative panel: BA-6, which marks this row.")

RULE_8285 = (
    "DRD2 x OpenFold-3 x cognate cell, n=25 rows: the row with the MEDIAN "
    "rmsd_to_active_ref in the cell (1.218 A; rank 13 of 25, 50th "
    "percentile). Cell range 1.020-1.507 A and the predicate calls all 25 "
    "rows active, so this is a typical row of its cell and not a best case. "
    "Camera from camera.side_view on exactly the rule used for GA-1a. "
    "Anchors verified against the row's own stored "
    "d_gpcrdb_tm6_tilt_246_637_ca = 17.2766 A (L76 2x46 CA - L375 6x37 CA) "
    "and d_npxxy_oh = 3.9883 A (Y209 5.58 OH - Y426 7.53 OH). Block A's "
    "cognate arm supplies the FULL cognate Ga subunit (chain B, 354 "
    "residues); only its alpha5 C-terminal 21 residues (334-354) are drawn, "
    "because the heterotrimer is not what the panel is about. Quantitative "
    "panel: BA-6, which marks this row.")

RULE_8285_REF = (
    RULE_8285 + " Here that row is superposed on 7JVR - DRD2's deposited "
    "ACTIVE panel reference - on receptor CA 34-441 only (prediction chain A "
    "against 7JVR chain R), excluding 7JVR's Gi heterotrimer, scFv16 and "
    "bromocriptine from the superposition atoms. 7JVR's own predicate axes "
    "reproduce exactly from its coordinates at the same atom pairs: 17.5860 A "
    "tilt and 4.2522 A NPxxY-OH. Cytoplasmic view from "
    "camera.cytoplasmic_view. This panel shows the state that is reached; it "
    "is NOT evidence of amplitude reproduction, which is BA-4 and is negative "
    "on three of four backbones.")

RULE_8285_CAVITY = (
    RULE_8285 + " Receptor drawn as a semi-transparent surface so the "
    "intracellular cavity reads as a cavity rather than as a docking cartoon. "
    "The one contact drawn is R132 (3.50) to the nearest alpha5 atom in THIS "
    "structure, the backbone O of C351, at 3.16 A - measured here, not taken "
    "from a published complex. FIGURES.md records that 3SN6 and 6E67 disagree "
    "about which alpha5 residue contacts R3.50; this render inherits none of "
    "that, because the contact is measured on the model being drawn.")

RULE_967 = (
    "ACM1 x Protenix x cognate cell, n=25 rows, every one of them with a cell "
    "mean plddt_mean below 50 and therefore the whole of E1: the row with the "
    "MEDIAN plddt_mean in the cell (38.38, rank 13 of 25, 50th percentile). "
    "Anchors verified against the row's own stored tilt 21.5470 A (L67 2x46 "
    "CA - L367 6x37 CA) and NPxxY-OH 26.6320 A (Y208 5.58 OH - Y418 7.53 "
    "OH). This row passes every A1-A6 scorer gate (passed=True): the gates "
    "carry no pLDDT floor, which is caveat C-12, and E1 exists to remove it. "
    "Quantitative panel: S1a.")

RULE_948 = (
    "ACM1 x Chai-1 x cognate cell, n=25 rows: the row with the HIGHEST "
    "plddt_mean in the cell (69.23, 100th percentile) - the comparator named "
    "in broken_cell/ALIGNMENT.md. Anchors verified against the row's own "
    "stored tilt 17.1660 A and NPxxY-OH 4.0160 A, same atom pairs as S10a. "
    "Same receptor, same arm, same camera rule and same colour rule as S10a; "
    "only the backbone differs. Quantitative panel: S1a.")


def verify(path, key, what):
    a = ANCHORS[key]
    c = a["chain"]
    dt = CR.verify_anchor(path, (c, a["tilt"][0], "CA"), (c, a["tilt"][1], "CA"),
                          a["d_tilt"], what="%s tilt" % what)
    dn = CR.verify_anchor(path, (c, a["npxxy"][0], "OH"),
                          (c, a["npxxy"][1], "OH"), a["d_npxxy"],
                          what="%s NPxxY" % what)
    names = {}
    atoms = CR.frame(path)
    for k in ("tilt", "npxxy"):
        for r in a[k]:
            names[r] = CR.residue_name(atoms, c, r)
    print("  verified %-14s tilt %.4f A (%s%d-%s%d)  NPxxY-OH %.4f A (%s%d-%s%d)"
          % (what, dt, names[a["tilt"][0]], a["tilt"][0],
             names[a["tilt"][1]], a["tilt"][1], dn,
             names[a["npxxy"][0]], a["npxxy"][0],
             names[a["npxxy"][1]], a["npxxy"][1]))
    return dt, dn


# ---------------------------------------------------------------------------
# The house convention for every render in this set, taken from what the corpus
# actually does rather than from what a caption says it does:
#
#   GREY IS "NOT THE SUBJECT", not "reference". The invariant scaffold is grey
#   and thin; the element carrying the claim is opaque, thick and coloured. A
#   grey-reference / coloured-prediction scheme is not a convention this field
#   has, and it colours by which file a thing came from rather than by what
#   moves.
#   TRANSPARENCY DE-EMPHASISES. It is never applied to the subject.
#   REPRESENTATION CARRIES EMPHASIS TOO: TM6 is drawn as a thick tube against
#   thin cartoon, which doubles the signal for free.
#   THE PARTNER IS THE CONTACTING FRAGMENT ONLY. The alpha5 C-terminal 21
#   residues are drawn and the rest of the supplied Ga is not, because drawing
#   the heterotrimer would depict an input the figure is not about.
#   NO RESIDUE LABELS ON THE RENDER. Per-residue detail goes in the strip
#   below the panel, where it cannot collide with the cartoon. Only the two
#   measured distances carry a label, and each carries its VALUE.
# ---------------------------------------------------------------------------
C_ACTIVE = "0xD55E00"      # vermillion - predicate calls this row active
C_INACTIVE = "0x0072B2"    # blue       - predicate calls this row inactive
C_SCAFFOLD = "grey65"
C_TILT = "0x000000"        # black  - the 2x46 / 6x37 tilt axis
C_NPXXY = "0xCC79A7"       # purple - the Y5.58 / Y7.53 NPxxY anchors
C_PEPTIDE = "0x009E73"     # green  - the alpha5 C-terminal 21-mer


def scaffold_extra(key, obj="subject", state="inactive", transparency=0.62,
                   resi_range=None):
    """Grey thin scaffold, opaque thick TM6 coloured by the predicate call."""
    a = ANCHORS[key]
    c = a["chain"]
    lo, hi = resi_range if resi_range else (a["tm6"][0] - 400, a["tm6"][1] + 400)
    t0, t1 = a["tm6"]
    colour = C_ACTIVE if state == "active" else C_INACTIVE
    return "\n".join([
        "set cartoon_transparency, %.2f, %s" % (transparency, obj),
        "color %s, %s and polymer" % (C_SCAFFOLD, obj),
        "set cartoon_tube_radius, 0.55",
        "create %s_tm6, %s and chain %s and resi %d-%d and polymer"
        % (obj, obj, c, t0, t1),
        "hide everything, %s_tm6" % obj,
        "show cartoon, %s_tm6" % obj,
        "cartoon tube, %s_tm6" % obj,
        "color %s, %s_tm6" % (colour, obj),
        "set cartoon_transparency, 0, %s_tm6" % obj,
    ])


def anchor_extra(key, obj="subject", show_values=False, sphere=0.40,
                 dash_colour=None):
    """The four anchor atoms, and the two measured distances drawn as dashes
    WITH THEIR VALUE. The value on the panel is the whole point: the field's
    characteristic failure on exactly this claim is a displacement drawn as an
    arrow and measured nowhere, and the mirror failure is a number printed
    with no atom pair named. Here both axes carry their value, and the atom
    pair is named in the strip below the panel."""
    a = ANCHORS[key]
    c, (t1, t2), (n1, n2) = a["chain"], a["tilt"], a["npxxy"]
    ct = dash_colour or C_TILT
    cn = dash_colour or C_NPXXY
    L = [
        "set label_distance_digits, 2",
        "show spheres, %s and chain %s and resi %d+%d and name CA"
        % (obj, c, t1, t2),
        "color %s, %s and chain %s and resi %d+%d and name CA" % (ct, obj, c, t1, t2),
        "show spheres, %s and chain %s and resi %d+%d and name OH"
        % (obj, c, n1, n2),
        "color %s, %s and chain %s and resi %d+%d and name OH" % (cn, obj, c, n1, n2),
        "show sticks, %s and chain %s and resi %d+%d+%d+%d and sidechain and "
        "not hydrogens" % (obj, c, t1, t2, n1, n2),
        "color %s, %s and chain %s and resi %d+%d and elem C" % (ct, obj, c, t1, t2),
        "color %s, %s and chain %s and resi %d+%d and elem C" % (cn, obj, c, n1, n2),
        "set stick_radius, 0.13, %s" % obj,
        "set sphere_scale, %.2f" % sphere,
        "distance d_tilt_%s, %s and chain %s and resi %d and name CA, "
        "%s and chain %s and resi %d and name CA" % (obj, obj, c, t1, obj, c, t2),
        "distance d_npxxy_%s, %s and chain %s and resi %d and name OH, "
        "%s and chain %s and resi %d and name OH" % (obj, obj, c, n1, obj, c, n2),
        "color %s, d_tilt_%s" % (ct, obj),
        "color %s, d_npxxy_%s" % (cn, obj),
        "set dash_gap, 0.30",
        "set dash_width, 3.0",
        "set label_size, 22",
        "set label_color, black",
    ]
    if not show_values:
        L += ["hide labels, d_tilt_%s" % obj, "hide labels, d_npxxy_%s" % obj]
    return "\n".join(L)


def peptide_only(chain, lo, hi, obj="subject"):
    """Draw the alpha5 C-terminal fragment and nothing else of the partner."""
    return "\n".join([
        "hide everything, %s and chain %s and not resi %d-%d" % (obj, chain, lo, hi),
        "set cartoon_transparency, 0, partner",
        "set cartoon_tube_radius, 0.85",
    ])


def run(name, args, dry):
    cmd = [sys.executable, RENDER, "--out", name,
           "--outdir", OUT, "--scenedir", SCENES] + args
    if dry:
        cmd.append("--dry-run")
    print("\n=== %s" % name)
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise SystemExit("render %s failed" % name)


ADRB2_ACTIVE = os.path.join(ST, "connector_orthogonality", "4LDE.cif")
ADRB2_INACTIVE = os.path.join(ST, "instrument_schematic", "2RH1.cif")

BA1A_RULE = (
    "Reference structures, not predictions: ADRB2's two PANEL references from "
    "02_references/reference_predicates.csv - 4LDE (active, blue, the "
    "receptor's actual panel active reference) over 2RH1 (inactive, grey). "
    "selected_from 2 because ADRB2 has one active and three inactive panel "
    "references (2RH1, 3NYA, 6PS2) and 2RH1 is the one 11_structures ships. "
    "This REPLACES the earlier 3SN6-over-2RH1 version: 3SN6 is not in the "
    "reference set at all (DISCREPANCY_REPORT D13), so no number drawn on it "
    "could be sourced from a tidy file. Every value printed here reproduces "
    "reference_predicates.csv exactly from the deposited coordinates: 4LDE "
    "tilt 17.5625 A / NPxxY-OH 4.8131 A, 2RH1 tilt 11.9283 A / NPxxY-OH "
    "11.4727 A. Superposed on receptor CA only - 4LDE chain A 1029-1342 "
    "(the entry carries a +1000 auth-numbering offset) against 2RH1 chain A "
    "29-342 - excluding 2RH1's T4 lysozyme (1002-1161), 4LDE's Nb6B9 "
    "nanobody (chain B) and both ligands from the superposition atoms. "
    "Cameras derived by camera.side_view and camera.cytoplasmic_view, not by "
    "eye. Anchors are L75 (2x46) / L275 (6x37) CA and Y219 (5.58) / Y326 "
    "(7.53) OH; instrument_schematic/ALIGNMENT.md names L124/F282 for the "
    "tilt anchors, which measure 9.03 A on 2RH1 and are not what the scorer "
    "used.")

BA1A_COMMON = [
    "--structure", ADRB2_ACTIVE,
    "--reference", ADRB2_INACTIVE,
    "--align-on", "chain A and polymer and name CA and resi 1029-1342",
    "--align-ref-on", "chain A and polymer and name CA and resi 29-342",
    "--ligand", "chain A and resn P0G",
    "--transparency", "0.38",
    "--ref-transparency", "0.50",
    "--selected-from", "2",
    "--selection-rule", BA1A_RULE,
]


def _ba1a_extra():
    """Grey the invariant bundle, colour only what moves. Both structures show
    their own TM6 - vermillion where the predicate fires, blue where it does
    not - and their own two measured axes. Four numbers, every one of them in
    reference_predicates.csv; they are printed in the composite strip beside
    the panel rather than as colliding 3-D labels."""
    return "\n".join([
        "hide everything, subject and not (chain A and resi 1029-1342)",
        "show cartoon, subject and chain A and resi 1029-1342",
        "hide everything, refstruct and not (chain A and resi 29-342)",
        "show cartoon, refstruct and chain A and resi 29-342",
        scaffold_extra("4lde", obj="subject", state="active",
                       transparency=0.55),
        scaffold_extra("2rh1", obj="refstruct", state="inactive",
                       transparency=0.62),
        "color grey80, refstruct and polymer",
        anchor_extra("4lde", obj="subject"),
        anchor_extra("2rh1", obj="refstruct"),
    ])


def ba1a(dry):
    """BA-1a - the instrument, on two views, with all four numbers drawn."""
    verify(ADRB2_ACTIVE, "4lde", "4LDE (ADRB2 active ref)")
    verify(ADRB2_INACTIVE, "2rh1", "2RH1 (ADRB2 inactive ref)")
    a = ANCHORS["4lde"]
    anchors = (("A", a["tilt"][0]), ("A", a["tilt"][1]))
    side = camera.side_view(ADRB2_ACTIVE, ("A", 1029, 1342), anchors,
                            pad=1.16, aspect=1500 / 1650.)
    cyto = camera.cytoplasmic_view(ADRB2_ACTIVE, ("A", 1029, 1342), anchors,
                                   pad=1.12, aspect=1.0)
    run("ba1a_instrument_side", BA1A_COMMON + [
        "--extra", _ba1a_extra(),
        "--view", camera.as_arg(side),
        "--width", "1500", "--height", "1650",
    ], dry)
    run("ba1a_instrument_cyto", BA1A_COMMON + [
        "--extra", _ba1a_extra(),
        "--view", camera.as_arg(cyto),
        "--width", "1500", "--height", "1500",
    ], dry)


# ---------------------------------------------------------------------------

def hero_a(dry):
    """GA-1a - the receptor predicted alone. Side view, intracellular up."""
    verify(AA2AR_APO, "aa2ar", "AA2AR row 567")
    a = ANCHORS["aa2ar"]
    view = camera.side_view(AA2AR_APO, ("A", 1, 316),
                            (("A", a["tilt"][0]), ("A", a["tilt"][1])),
                            pad=1.16, aspect=1500 / 1750.)
    run("hero_a_apo_alone", [
        "--structure", AA2AR_APO,
        "--ligand", "none",
        "--transparency", "0.48",
        "--extra", "\n".join([
            "hide everything, subject and not (chain A and resi 1-316)",
            "show cartoon, subject and chain A and resi 1-316",
            scaffold_extra("aa2ar", state="inactive", transparency=0.48),
            anchor_extra("aa2ar"),
        ]),
        "--view", camera.as_arg(view),
        "--width", "1500", "--height", "1750",
        "--selected-from", "25",
        "--selection-rule", RULE_567,
        "--prediction-id", "567",
    ], dry)


def hero_b(dry):
    """GA-1b - the same models with the cognate Ga supplied. Same camera rule."""
    verify(DRD2_COG, "drd2", "DRD2 row 8285")
    a = ANCHORS["drd2"]
    view = camera.side_view(DRD2_COG, ("A", 30, 443),
                            (("A", a["tilt"][0]), ("A", a["tilt"][1])),
                            pad=1.16, aspect=1500 / 1750.)
    run("hero_b_cognate", [
        "--structure", DRD2_COG,
        "--ligand", "none",
        "--peptide", "chain B and resi 334-354",
        "--transparency", "0.48",
        "--extra", "\n".join([
            "hide everything, subject and chain B",
            "hide everything, subject and not (chain A and resi 30-443)",
            "show cartoon, subject and chain A and resi 30-443",
            scaffold_extra("drd2", state="active", transparency=0.48),
            "color %s, partner" % C_PEPTIDE,
            "set cartoon_transparency, 0, partner",
            anchor_extra("drd2"),
        ]),
        "--view", camera.as_arg(view),
        "--width", "1500", "--height", "1750",
        "--selected-from", "25",
        "--selection-rule", RULE_8285,
        "--prediction-id", "8285",
    ], dry)


def hero_c(dry):
    """GA-1c - the same prediction over the deposited active reference, seen
    from the cytoplasm: the second of the two canonical GPCR views."""
    verify(DRD2_COG, "drd2", "DRD2 row 8285")
    verify(DRD2_REF, "7jvr", "7JVR reference")
    a = ANCHORS["drd2"]
    view = camera.cytoplasmic_view(DRD2_COG, ("A", 30, 443),
                                   (("A", a["tilt"][0]), ("A", a["tilt"][1])),
                                   pad=1.20, aspect=1.0)
    run("hero_c_over_reference", [
        "--structure", DRD2_COG,
        "--reference", DRD2_REF,
        "--align-on", "chain A and polymer and name CA and resi 34-441",
        "--align-ref-on", "chain R and polymer and name CA and resi 34-441",
        "--ligand", "none",
        "--peptide", "chain B and resi 334-354",
        "--transparency", "0.58",
        "--ref-transparency", "0.62",
        "--extra", "\n".join([
            "hide everything, subject and chain B",
            "hide everything, subject and not (chain A and resi 30-443)",
            "show cartoon, subject and chain A and resi 30-443",
            "hide everything, refstruct and not (chain R and resi 30-443)",
            "show cartoon, refstruct and chain R and resi 30-443",
            scaffold_extra("drd2", obj="subject", state="active",
                           transparency=0.58),
            scaffold_extra("7jvr", obj="refstruct", state="active",
                           transparency=0.62),
            "color grey45, refstruct_tm6",
            "color %s, partner" % C_PEPTIDE,
            "set cartoon_transparency, 0, partner",
        ]),
        "--view", camera.as_arg(view),
        "--width", "1500", "--height", "1500",
        "--selected-from", "25",
        "--selection-rule", RULE_8285_REF,
        "--prediction-id", "8285",
    ], dry)


def ba8_alpha5(dry):
    """BA-8 - the alpha5 C-terminal helix in the intracellular cavity, drawn
    against a receptor SURFACE rather than a cartoon, because the subject is a
    cavity and a cartoon of a cavity reads as a docking picture."""
    verify(DRD2_COG, "drd2", "DRD2 row 8285")
    a = ANCHORS["drd2"]
    view = camera.cytoplasmic_view(DRD2_COG, ("A", 30, 443),
                                   (("A", a["tilt"][0]), ("A", a["tilt"][1])),
                                   pad=1.05, aspect=1.0)
    run("ba8_alpha5_cavity", [
        "--structure", DRD2_COG,
        "--ligand", "none",
        "--peptide", "chain B and resi 334-354",
        "--transparency", "1.0",
        "--extra", "\n".join([
            "hide everything, subject and chain B",
            "hide everything, subject and not (chain A and resi 30-443)",
            "set surface_quality, 1",
            "set transparency, 0.45",
            "set two_sided_lighting, on",
            "show surface, subject and chain A and resi 30-443 and polymer",
            "color %s, subject and chain A" % C_SCAFFOLD,
            "color %s, subject and chain A and resi %d-%d"
            % (C_ACTIVE, a["tm6"][0], a["tm6"][1]),
            "set cartoon_transparency, 0, partner",
            "set cartoon_tube_radius, 0.9",
            "cartoon tube, partner",
            "color %s, partner" % C_PEPTIDE,
            # R3.50 and the alpha5 atom that reaches it
            "show sticks, subject and chain A and resi 132 and sidechain and "
            "not hydrogens",
            "color 0x000000, subject and chain A and resi 132 and elem C",
            "show sticks, subject and chain B and resi 351 and not hydrogens",
            "color %s, subject and chain B and resi 351 and elem C" % C_PEPTIDE,
            "distance d_r350, subject and chain A and resi 132 and name NH2, "
            "subject and chain B and resi 351 and name O",
            "color black, d_r350",
            anchor_extra("drd2", sphere=0.40),
        ]),
        "--view", camera.as_arg(view),
        "--width", "1900", "--height", "1900",
        "--selected-from", "25",
        "--selection-rule", RULE_8285_CAVITY,
        "--prediction-id", "8285",
    ], dry)


def s10_broken(dry):
    """S10 - what E1 removes. One camera rule, one colour rule, a measured
    scalar on each panel."""
    for name, path, key, state, rule in (
        ("s10a_broken_cell", ACM1_BROKEN, "acm1_broken", "active", RULE_967),
        ("s10b_healthy_cell", ACM1_HEALTHY, "acm1_healthy", "active", RULE_948),
    ):
        verify(path, key, name)
        a = ANCHORS[key]
        view = camera.side_view(path, ("A", 1, 460),
                                (("A", a["tilt"][0]), ("A", a["tilt"][1])),
                                pad=1.16, aspect=1400 / 1650.)
        run(name, [
            "--structure", path,
            "--ligand", "none",
            "--peptide", "chain B and resi 339-359",
            "--transparency", "0.48",
            "--extra", "\n".join([
                "hide everything, subject and chain B",
                "hide everything, subject and not (chain A and resi 1-460)",
                "show cartoon, subject and chain A and resi 1-460",
                scaffold_extra(key, state=state, transparency=0.48),
                "color %s, partner" % C_PEPTIDE,
                "set cartoon_transparency, 0, partner",
                anchor_extra(key),
            ]),
            "--view", camera.as_arg(view),
            "--width", "1400", "--height", "1650",
            "--selected-from", "25",
            "--selection-rule", rule,
            "--prediction-id", name.split("_")[0],
        ], dry)


TARGETS = {
    "ba1a": ba1a,
    "hero_a": hero_a, "hero_b": hero_b, "hero_c": hero_c,
    "ba8": ba8_alpha5, "s10": s10_broken,
}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("names", nargs="*", default=None)
    p.add_argument("--dry-run", action="store_true")
    a = p.parse_args()
    names = a.names or list(TARGETS)
    print("verifying every anchor against the tidy data before drawing it")
    for n in names:
        TARGETS[n](a.dry_run)
    print("\nall renders done")


if __name__ == "__main__":
    main()
