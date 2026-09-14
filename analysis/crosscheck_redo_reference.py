#!/usr/bin/env python3
"""Re-derive every load-bearing number in REDO_REFERENCE.md from the data files.

Each check states the claim, recomputes it, and fails loudly on a mismatch. This is
the third pass: the gathering agents derived, a second agent re-derived, this
re-derives independently again against the assembled text.
"""
import csv, collections, math, os, re, subprocess, sys

ROOT = "/Users/aditya/Documents/tools/Novartis_projects/paper"
DOC = os.path.join(ROOT, "redo/spec/REDO_REFERENCE.md")
text = open(DOC, encoding="utf-8").read()
R = []


def chk(what, got, want, tol=0):
    ok = (abs(got - want) <= tol) if isinstance(got, (int, float)) and isinstance(want, (int, float)) else got == want
    R.append((ok, what, got, want))


def rows(p):
    return list(csv.DictReader(open(os.path.join(ROOT, p), encoding="utf-8", errors="replace")))


def trows(p):
    return list(csv.DictReader(open(os.path.join(ROOT, p), encoding="utf-8", errors="replace"), delimiter="\t"))


g1 = rows("redo/inputs/g1_systems.csv")
g2 = rows("redo/inputs/g2_systems.csv")
reg = trows("redo/inputs/g1_partner_registry.tsv")

# --- Group 1 shape -----------------------------------------------------------
chk("g1 rows = 2,039", len(g1), 2039)
chk("g1 arms = 23", len({r["arm"] for r in g1}), 23)
chk("g1 receptors = 64", len({r["receptor_slug"] for r in g1}), 64)
chk("g1 clusters = 32", len({r["receptor_cluster"] for r in g1}), 32)
chk("g1 pooled predictions = 74,960",
    sum(int(r["predictions_pooled"] or 0) for r in g1), 74960)
chk("g1 per-cell predictions = 212,920",
    sum(int(r["predictions_percell"] or 0) for r in g1), 212920)

# --- MSA settings ------------------------------------------------------------
pm = collections.Counter(r["partner_msa"] for r in g1)
chk("partner_msa off = 1,855", pm["off"], 1855)
chk("partner_msa ON = 90", pm["ON"], 90)
chk("partner_msa n/a = 94", pm["n/a"], 94)
chk("receptor_msa on for all 2,039",
    collections.Counter(r["receptor_msa"] for r in g1)["on (default)"], 2039)

bb = collections.Counter(r["backbones"] for r in g1)
chk("four-backbone rows = 1,271", bb["boltz2|openfold3|protenix|chai1"], 1271)
chk("boltz2-only rows = 768", bb["boltz2"], 768)

fam = collections.Counter(r["supplied_partner_family"] for r in g1)
chk("Gi/o rows = 1,517", fam["Gi/o"], 1517)
chk("Gs rows = 372", fam["Gs"], 372)
chk("Gq/11 rows = 150", fam["Gq/11"], 150)

# --- receptor sets -----------------------------------------------------------
for name, nrec, ncl, nrow in (("CORE32(provisional)", 30, 29, 1500),
                              ("G10_SCAN(provisional)", 10, 10, 360),
                              ("C1_REST(provisional)", 24, 14, 72),
                              ("CORE32_GS(provisional)", 6, 6, 54)):
    sub = [r for r in g1 if r["receptor_set"] == name]
    chk("%s rows" % name, len(sub), nrow)
    chk("%s receptors" % name, len({r["receptor_slug"] for r in sub}), nrec)
    chk("%s clusters" % name, len({r["receptor_cluster"] for r in sub}), ncl)

# --- constructs --------------------------------------------------------------
con = collections.Counter(r["chain_b_construct"] for r in g1)
for k, v in (("R0_apo", 94), ("R1_ct11", 90), ("R1b_ct13", 30), ("R2_ct15", 60),
             ("R2b_ct17", 30), ("R2c_ct19", 30), ("R3_ct21", 154),
             ("R4_a5helix", 60), ("R5_a5plus", 90), ("R7_full", 124),
             ("R8_hetero", 30), ("R6a_da5", 30), ("R6b_a5perm", 30),
             ("R6c_a5polyA", 30), ("ubiquitin", 30), ("KaiB_2QKEE", 30)):
    chk("construct %s rows" % k, con[k], v)

chk("registry rows = 782", len(reg), 782)
chk("registry held=yes = 771",
    collections.Counter(r["held"] for r in reg)["yes"], 771)
chk("registry held=NO = 10", collections.Counter(r["held"] for r in reg)["NO"], 10)
# The `family` column holds 30 distinct values because reference-tip constructs put
# the RECEPTOR slug there. 17 is the count on the Ga rung constructs specifically.
chk("Ga families on ga_rung constructs = 17",
    len({r["family"] for r in reg
         if r["construct_class"] in ("ga_rung", "ga_rung_isoform")}), 17)
chk("distinct values in the family column = 30",
    len({r["family"] for r in reg}), 30)
chk("alpha5 helix Asp368-Leu394 = 27 residues", 394 - 368 + 1, 27)

# --- Group 2 -----------------------------------------------------------------
chk("g2 rows = 350", len(g2), 350)
chk("g2 receptors = 26", len({r["receptor_slug"] for r in g2}), 26)
chk("g2 clusters = 25", len({r["receptor_cluster"] for r in g2}), 25)
ds = collections.Counter(r["dispatch_status"] for r in g2)
chk("g2 READY = 313", ds["READY"], 313)
lt = collections.Counter(r["ligand_tier"] for r in g2)
chk("T1 small molecule = 296", lt["T1_small_molecule"], 296)
chk("T2 peptide = 12", lt["T2_peptide"], 12)
chk("T3 mixed = 42", lt["T3_mixed"], 42)

rdy = [r for r in g2 if r["dispatch_status"] == "READY"]
lf = [r for r in rdy if (r["ligand_role_actual"] or "none") == "none"]
chk("ligand-free READY rows = 98", len(lf), 98)
chk("ligand-free receptors = 25", len({r["receptor_slug"] for r in lf}), 25)
byrec = collections.defaultdict(set)
for r in rdy:
    byrec[r["receptor_slug"]].add((((r["ligand_role_actual"] or "none") != "none"),
                                   r["chain_b_construct"] != "R0_apo"))
full = [k for k, v in byrec.items() if len(v) == 4]
chk("receptors with the complete 2x2 = 20", len(full), 20)
chk("their clusters = 19",
    len({r["receptor_cluster"] for r in rdy if r["receptor_slug"] in full}), 19)
chk("READY pooled predictions = 8,716",
    sum(int(r["predictions_pooled"] or 0) for r in rdy), 8716)

# --- MDE arithmetic ----------------------------------------------------------
for k, want in ((11, 0.367), (12, 0.352), (15, 0.314), (17, 0.295),
                (19, 0.279), (22, 0.260), (24, 0.249), (26, 0.239),
                (29, 0.226), (32, 0.215)):
    chk("MDE at k=%d" % k, round(1.218 / math.sqrt(k), 3), want, 0.0005)
chk("interaction SD 2.80 x 0.435 = 1.218", round(2.80 * 0.435, 3), 1.218, 0.0005)

# --- Stage 1 measurement -----------------------------------------------------
m = [r for r in rows("redo/inputs/g0_measurements.csv")
     if r["state"] in ("Active", "Inactive")]


def num(v):
    try:
        f = float(v)
        return None if f != f else f
    except (TypeError, ValueError):
        return None


cal = [r for r in m if r["role"] == "calibration"]
app = [r for r in m if r["role"] == "application"]
chk("calibration Active/Inactive = 726", len(cal), 726)
chk("application Active/Inactive = 610", len(app), 610)
chk("intermediates = 21",
    sum(1 for r in rows("redo/inputs/g0_measurements.csv")
        if r["state"] == "Intermediate"), 21)

both = [r for r in cal if num(r["d_npxxy_oh"]) is not None and num(r["d_tilt"]) is not None]
chk("calibration rows with BOTH axes = 487", len(both), 487)
tilt = [r for r in cal if num(r["d_tilt"]) is not None]
chk("calibration rows with tilt = 585", len(tilt), 585)


def perf(sub, call):
    tp = sum(1 for r in sub if r["state"] == "Active" and call(r))
    fn = sum(1 for r in sub if r["state"] == "Active" and not call(r))
    fp = sum(1 for r in sub if r["state"] == "Inactive" and call(r))
    tn = sum(1 for r in sub if r["state"] == "Inactive" and not call(r))
    return tp / (tp + fn), tn / (tn + fp)


se, sp = perf(both, lambda r: num(r["d_npxxy_oh"]) < 9.08 and num(r["d_tilt"]) > 14.932)
chk("calibration AND sensitivity 86.5%", round(100 * se, 1), 86.5, 0.05)
chk("calibration AND specificity 100%", round(100 * sp, 1), 100.0, 0.05)
se, sp = perf(tilt, lambda r: num(r["d_tilt"]) > 14.932)
chk("calibration tilt-alone sensitivity 96.6%", round(100 * se, 1), 96.6, 0.05)
chk("calibration tilt-alone specificity 100%", round(100 * sp, 1), 100.0, 0.05)
chk("calibration inactives with tilt = 87",
    sum(1 for r in tilt if r["state"] == "Inactive"), 87)
chk("calibration inactives with both axes = 81",
    sum(1 for r in both if r["state"] == "Inactive"), 81)

lo_i = min(num(r["d_npxxy_oh"]) for r in both if r["state"] == "Inactive")
chk("lowest inactive NPxxY = 8.95", round(lo_i, 2), 8.95, 0.005)
lo_a = min(num(r["d_tilt"]) for r in both if r["state"] == "Active")
chk("lowest active tilt = 12.11", round(lo_a, 2), 12.11, 0.005)

# --- manifest ----------------------------------------------------------------
man = trows("redo/inputs/MANIFEST.tsv")
chk("manifest rows = 65", len(man), 65)
chk("unattributed inputs = 15",
    sum(1 for r in man if r["generator"] == "unattributed"), 15)

# --- does the document actually contain these numbers? -----------------------
for s in ("2,039", "74,960", "212,920", "1,855", "1,271", "1,517", "313", "8,716",
          "0.367", "0.226", "8.95", "12.11", "96.6", "86.5", "1,357", "726", "610"):
    R.append((s in text, "document contains %r" % s, s in text, True))

bad = [r for r in R if not r[0]]
for ok, what, got, want in R:
    if not ok:
        print("  MISMATCH  %-46s got %r want %r" % (what, got, want))
print("=" * 74)
print("%d of %d checks reproduce" % (len(R) - len(bad), len(R)))
sys.exit(1 if bad else 0)
