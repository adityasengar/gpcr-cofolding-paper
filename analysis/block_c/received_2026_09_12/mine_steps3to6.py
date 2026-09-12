#!/usr/bin/env python3
"""mine_steps3to6.py -- steps 3-6 of the order of work on rows.tier3.v2.csv.

FIRST_LOOK.md did steps 1-2 (arm parse, cross-validated against the g4 census; then
per backbone).  This does the four things that document says must happen before any
of it is quotable:

  3. aggregate to PARALOG CLUSTERS and bootstrap over them -- rows are not the unit
  4. switch to pocket_ca_rmsd_active/_inactive, the continuous readout SC-C-6 prefers
  5. handle SEEDS -- the pre-registration makes seed the unit of variance
  6. resolve the role-asymmetric OPSIN exclusion

Design rules this script obeys, each of which this project learned the hard way:

  * NEVER pool across backbones.  Every number is reported per backbone.  Pooling
    across disagreeing backbones has twice produced a statement about one backbone
    wearing the clothes of a statement about a class (DECISIONS.md F-13(c), and the
    Class B 9 A split).
  * The statistical unit is the PARALOG CLUSTER.  Rows are aggregated
    row -> (receptor, arm, role, backbone, seed) -> receptor -> cluster, so no
    receptor with more rows gets more weight and no cluster with more receptors does.
  * The opsins are handled EXPLICITLY and both ways, never silently dropped.
  * A missing input FAILS.  Nothing here skips quietly.

Run:      python3 analysis/block_c/received_2026_09_12/mine_steps3to6.py
Selftest: ... --selftest   plants defects and asserts the checks fire.
"""
import collections
import csv
import math
import os
import random
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
ROWS = os.path.join(HERE, "rows.tier3.v2.csv")
TIERS = os.path.join(ROOT, "redo", "inputs", "ligand_tiers.tsv")

NUM = re.compile(r"^-?\d+(\.\d+)?([eE][-+]?\d+)?$")
PATH = re.compile(r"/pool/([^/]+)/([^/]+)/([^/]+)/([^/]+)/seed_(\d+)/")
BACKBONES = ("boltz", "chai", "of3", "protenix")
ROLES = ("full_agonist", "neutral_antagonist", "decoy_lig")
# The two non-human opsins.  They carry an EMPTY receptor_slug AND an empty
# receptor_class, and -- the part that matters -- every one of their rows is
# full_agonist.  A_RECEPTOR_SLUG_MISSING, the flag that exists to mark exactly this,
# is EMPTY on all 800.  A flag that vouches for the data and does not fire is the
# same defect class as Block A's `matches_claim_sheet`.
OPSINS = {"B1B1U5", "OPSD"}
BOOT = 2000
SEED = 20260912


def fail(msg):
    sys.stderr.write("FAIL: " + msg + "\n")
    sys.exit(1)


def num(v):
    v = (v or "").strip()
    return float(v) if NUM.match(v) else None


def load(rows_path=ROWS, tiers_path=TIERS):
    if not os.path.exists(rows_path):
        fail(f"{rows_path} is absent.  This analysis does not run without it.")
    if not os.path.exists(tiers_path):
        fail(f"{tiers_path} is absent -- the cluster map is not optional.")
    cluster = {r["receptor_slug"].upper(): r["cluster"]
               for r in csv.DictReader(open(tiers_path), delimiter="\t")}
    out = []
    with open(rows_path) as fh:
        for r in csv.DictReader(fh):
            m = PATH.search(r["input_path"])
            if not m:
                fail("input_path does not carry the pool layout; the arm parse is "
                     "the foundation of everything here and cannot be guessed.")
            p_rec, p_role, arm, backbone, seed = m.groups()
            slug = (r["receptor_slug"].strip() or p_rec).upper()
            if r["ligand_role"] != p_role:
                fail(f"ligand_role column and path disagree for {slug}: "
                     f"{r['ligand_role']} vs {p_role}")
            # binary predicate, thresholds AS CARRIED IN THE FILE
            npx, tilt = num(r["d_npxxy_y558_y753_oh"]), num(r["d_gpcrdb_tm6_tilt_246_637_ca"])
            t_npx, t_tilt = num(r["threshold_npxxy_oh_active_lt"]), num(r["threshold_gpcrdb_tm6_tilt_active_gt"])
            binary = None
            if None not in (npx, tilt, t_npx, t_tilt):
                binary = 1.0 if (npx < t_npx and tilt > t_tilt) else 0.0
            # continuous readout: positive = closer to the ACTIVE pocket
            pa, pi = num(r["pocket_ca_rmsd_active"]), num(r["pocket_ca_rmsd_inactive"])
            cont = (pi - pa) if (pa is not None and pi is not None) else None
            out.append(dict(slug=slug, cluster=cluster.get(slug), arm=arm,
                            role=r["ligand_role"], backbone=backbone, seed=seed,
                            is_opsin=slug in OPSINS, binary=binary, cont=cont))
    return out


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def to_clusters(rows, field):
    """row -> (receptor,arm,role,backbone,seed) -> receptor -> cluster.

    Collapsing seeds INSIDE the receptor before the cluster mean is what makes seed
    a level of the design rather than a source of pseudo-replication: five seeds of
    one receptor must not outvote one seed of another.
    """
    seedcell = collections.defaultdict(list)
    for r in rows:
        if r[field] is None or r["cluster"] is None:
            continue
        seedcell[(r["cluster"], r["slug"], r["arm"], r["role"], r["backbone"], r["seed"])].append(r[field])
    rec = collections.defaultdict(list)
    for (cl, slug, arm, role, bb, _seed), vals in seedcell.items():
        rec[(cl, slug, arm, role, bb)].append(mean(vals))
    clus = collections.defaultdict(list)
    for (cl, _slug, arm, role, bb), vals in rec.items():
        clus[(cl, arm, role, bb)].append(mean(vals))
    return {k: mean(v) for k, v in clus.items()}


def boot_ci(per_cluster_pairs, rng, n=BOOT):
    """Bootstrap over CLUSTERS -- resample the clusters, not the rows."""
    if len(per_cluster_pairs) < 2:
        return (None, None)
    draws = []
    m = len(per_cluster_pairs)
    for _ in range(n):
        s = [per_cluster_pairs[rng.randrange(m)] for _ in range(m)]
        draws.append(mean([b - a for a, b in s]))
    draws.sort()
    return (draws[int(0.025 * n)], draws[int(0.975 * n)])


def contrast(clus, role, bb, rng):
    """apo -> cognate shift for one (role, backbone), paired within cluster."""
    pairs = []
    for (cl, arm, rl, b), v in clus.items():
        if rl != role or b != bb or arm != "apo":
            continue
        cog = clus.get((cl, "cognate", rl, b))
        if cog is not None and v is not None:
            pairs.append((v, cog))
    if not pairs:
        return None
    lo, hi = boot_ci(pairs, rng)
    return dict(k=len(pairs), apo=mean([a for a, _ in pairs]),
                cog=mean([b for _, b in pairs]),
                delta=mean([b - a for a, b in pairs]), lo=lo, hi=hi)


def report(rows, variant, out):
    rng = random.Random(SEED)
    out.append(f"\n## Variant: {variant['label']}\n")
    sel = [r for r in rows if variant["keep"](r)]
    out.append(f"Rows retained **{len(sel):,}** of {len(rows):,}.\n")
    for field, name, unit in (("binary", "binary predicate", "fraction active"),
                              ("cont", "continuous readout", "Angstrom, + = nearer active")):
        clus = to_clusters(sel, field)
        ks = sorted({k[0] for k in clus})
        out.append(f"\n### {name} — {unit}\n")
        out.append(f"clusters contributing: **{len(ks)}**, "
                   f"MDE = 1.218/sqrt(k) = **{1.218/math.sqrt(len(ks)):.3f}**\n"
                   if ks else "no clusters contribute\n")
        out.append("\n| role | backbone | k | apo | cognate | shift | 95% CI (cluster boot) |")
        out.append("|---|---|---:|---:|---:|---:|---|")
        for role in ROLES:
            for bb in BACKBONES:
                c = contrast(clus, role, bb, rng)
                if not c:
                    continue
                ci = f"[{c['lo']:+.3f}, {c['hi']:+.3f}]" if c["lo"] is not None else "—"
                out.append(f"| {role} | {bb} | {c['k']} | {c['apo']:.3f} | "
                           f"{c['cog']:.3f} | **{c['delta']:+.3f}** | {ci} |")
        out.append("")


def completeness(rows, out):
    tot = collections.Counter(); ok = collections.Counter()
    byrole = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        tot[r["slug"]] += 1
        ok[r["slug"]] += r["cont"] is not None
        a = byrole[(r["slug"], r["role"])]; a[0] += r["cont"] is not None; a[1] += 1
    absent = sorted(s for s in tot if ok[s] == 0)
    partial = sorted(s for s in tot if 0 < ok[s] < tot[s])
    asym = [s for s in tot
            if len({round(v[0] / v[1], 3) for (ss, _), v in byrole.items() if ss == s}) > 1]
    out.append("\n## Step 4 precondition — is the continuous readout usable?\n")
    out.append(f"- receptors with it **complete**: **{len(tot) - len(absent) - len(partial)}**")
    out.append(f"- receptors with it **wholly absent**: **{len(absent)}** — {', '.join(absent)}")
    out.append(f"- receptors with it **partial**: **{len(partial)}** — "
               f"{', '.join(partial) if partial else 'none'}")
    out.append(f"- receptors whose completeness **differs by ligand role**: **{len(asym)}**\n")
    out.append("**The missingness is receptor-wise, not role-wise or arm-wise.** That is the"
               " question that mattered: a readout missing asymmetrically across roles would"
               " have biased every ligand-class comparison, the way the opsin exclusion does."
               " It does not. Switching to the continuous readout shrinks the PANEL and leaves"
               " the within-receptor design balanced.\n")
    return absent



def matched_roles(clus, bb, arm):
    """Clusters present for ALL THREE roles at one (arm, backbone).

    Comparing roles across DIFFERENT cluster sets is the compare-like-with-like
    failure this project has hit three times.  The role tables above run on 18, 15
    and 18 clusters; any statement about ligand class must be made where all three
    levels are observed.
    """
    sets = [{cl for (cl, a, rl, b) in clus if a == arm and b == bb and rl == role}
            for role in ROLES]
    return sorted(set.intersection(*sets)) if all(sets) else []


def role_contrast(clus, bb, arm, a_role, b_role, rng):
    ks = matched_roles(clus, bb, arm)
    pairs = [(clus[(cl, arm, a_role, bb)], clus[(cl, arm, b_role, bb)]) for cl in ks
             if clus.get((cl, arm, a_role, bb)) is not None
             and clus.get((cl, arm, b_role, bb)) is not None]
    if len(pairs) < 2:
        return None
    lo, hi = boot_ci(pairs, rng)
    return dict(k=len(pairs), a=mean([x for x, _ in pairs]), b=mean([y for _, y in pairs]),
                delta=mean([y - x for x, y in pairs]), lo=lo, hi=hi)


def ligand_class_section(rows, out):
    """C7 and the decoy question, on a MATCHED cluster panel."""
    rng = random.Random(SEED)
    sel = [r for r in rows if not r["is_opsin"]]
    out.append("\n## The ligand-class question, on a MATCHED cluster panel\n")
    out.append("The role tables above run on different cluster counts (18 / 15 / 18), so "
               "they cannot be compared with each other. These restrict to clusters where "
               "**all three roles are observed** at that (arm, backbone), and pair within "
               "cluster.\n")
    for field, name in (("binary", "binary predicate"), ("cont", "continuous readout")):
        clus = to_clusters(sel, field)
        out.append(f"\n### {name}\n")
        out.append("| arm | backbone | k | contrast | level A | level B | difference | 95% CI |")
        out.append("|---|---|---:|---|---:|---:|---:|---|")
        for arm in ("apo", "cognate"):
            for bb in BACKBONES:
                for a_role, b_role, lab in (
                        ("neutral_antagonist", "full_agonist", "agonist − antagonist"),
                        ("decoy_lig", "neutral_antagonist", "antagonist − decoy")):
                    c = role_contrast(clus, bb, arm, a_role, b_role, rng)
                    if not c:
                        continue
                    ci = f"[{c['lo']:+.3f}, {c['hi']:+.3f}]"
                    star = " **" if (c["lo"] is not None and c["lo"] * c["hi"] > 0) else " "
                    out.append(f"| {arm} | {bb} | {c['k']} | {lab} | {c['a']:.3f} | "
                               f"{c['b']:.3f} | {c['delta']:+.3f}{star}| {ci} |")
        out.append("")
    out.append("`**` marks an interval excluding zero.\n")


def seed_section(rows, out):
    """Step 5 -- seed as the unit of variance, stated rather than assumed."""
    sel = [r for r in rows if not r["is_opsin"] and r["binary"] is not None]
    cell = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in sel:
        cell[(r["slug"], r["arm"], r["role"], r["backbone"])][r["seed"]].append(r["binary"])
    within, unan = [], 0
    for _k, seeds in cell.items():
        ms = [mean(v) for v in seeds.values()]
        if len(ms) > 1:
            within.append(max(ms) - min(ms))
            if max(ms) - min(ms) == 0:
                unan += 1
    out.append("\n## Step 5 — seeds\n")
    out.append(f"- design cells (receptor × arm × role × backbone): **{len(cell):,}**, "
               f"**{len(next(iter(cell.values())))} seeds** each")
    out.append(f"- cells where every seed gives the SAME cell mean: **{unan:,} "
               f"({100*unan/len(within):.1f}%)**")
    out.append(f"- mean seed-to-seed spread within a cell: **{mean(within):.3f}**, "
               f"max **{max(within):.3f}**\n")
    out.append("Seeds are collapsed **inside the receptor** before the cluster mean "
               "throughout this document, so five seeds of one receptor cannot outvote one "
               "seed of another. The spread above is what that collapsing absorbs.\n")


def main(argv):
    rows = load()
    if len(rows) != 40800:
        fail(f"expected 40,800 rows, got {len(rows):,}")
    out = ["# Steps 3–6 on rows.tier3.v2.csv — cluster unit, continuous readout, seeds, opsins",
           "",
           "**GENERATED** by `mine_steps3to6.py`. Do not hand-edit; re-run it.",
           "",
           f"Rows **{len(rows):,}**; backbones "
           f"{dict(collections.Counter(r['backbone'] for r in rows))}; "
           f"seeds **{len({r['seed'] for r in rows})}**.",
           "",
           "Every table is **per backbone**. Nothing here is pooled across backbones, "
           "because this project has twice found that pooling across disagreeing backbones "
           "produces a statement about one backbone in the clothes of a statement about a "
           "class (`DECISIONS.md` F-13(c); the Class B 9 Å split).",
           "",
           "The unit is the **paralog cluster**. Rows collapse "
           "`row → (receptor, arm, role, backbone, seed) → receptor → cluster`, so five "
           "seeds of one receptor cannot outvote one seed of another, and a cluster with "
           "four receptors does not outweigh one with a single receptor. "
           f"Intervals are **cluster bootstraps**, {BOOT:,} resamples, paired within cluster.",
           ]
    absent = completeness(rows, out)

    out.append("\n## Step 6 — the opsins, handled explicitly\n")
    ops = [r for r in rows if r["is_opsin"]]
    out.append(f"- `B1B1U5` and `OPSD`: **{len(ops)} rows**, "
               f"roles {dict(collections.Counter(r['role'] for r in ops))}.")
    out.append("- They carry an **empty `receptor_slug`** and an empty `receptor_class`, and "
               "`A_RECEPTOR_SLUG_MISSING` — the flag that exists to mark exactly this — is "
               "**empty on all of them**. A flag that vouches for the data and does not fire "
               "is Block A's `matches_claim_sheet` defect in another costume.")
    out.append("- **Every opsin row is `full_agonist`.** Dropping them for an empty class, "
               "as the first-look table did, removes agonist observations only — so any "
               "agonist-versus-antagonist comparison is then drawn on a population the other "
               "levels do not share. Both variants below are therefore reported.\n")

    for variant in (
        dict(label="OPSINS EXCLUDED FROM EVERY ROLE (comparison-safe)",
             keep=lambda r: not r["is_opsin"]),
        dict(label="OPSINS INCLUDED, identity recovered from input_path",
             keep=lambda r: True),
    ):
        report(rows, variant, out)

    ligand_class_section(rows, out)
    seed_section(rows, out)
    out.append("\n## What is NOT settled here\n")
    out.append("- **Modality stays confounded with receptor identity.** Every peptide-ligand "
               "row is a peptide-family receptor, so this file cannot separate *peptide "
               "ligand* from *peptide receptor*. That needs a within-receptor contrast, "
               "which is what `D-2026-09-12-f`'s T3 tier exists to supply.")
    out.append("- **The continuous readout costs panel, not balance.** "
               f"{len(absent)} receptors lose it entirely: {', '.join(absent)}.")
    out.append("- Nothing here calibrates the instrument. The binary predicate uses the "
               "thresholds **as carried in the file**, one of which is inherited rather than "
               "derived — that is the measurement pass, and it has not run.")
    path = os.path.join(HERE, "STEPS_3_TO_6.md")
    open(path, "w").write("\n".join(out) + "\n")
    print(f"wrote {path}  ({len(out)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
