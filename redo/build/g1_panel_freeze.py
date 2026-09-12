#!/usr/bin/env python3
"""g1_panel_freeze.py — the frozen Group 1 panel, and the two cognate columns.

Three decisions from Aditya, applied here so they are executable rather than
remembered.  Governing principle: **Group 1 is STRICT -- stricter than Group 0,
because Group 0 is us tuning a measure and Group 1 is what gets dispatched.**

DECISION 1 -- chimeric-reference receptors are INELIGIBLE for the primary panel.
  Rungs R1-R4 *are* the alpha5 C terminus.  On ten receptors the deposited active
  reference carries an engineered tip 8 of 21 residues from canonical Gq at the
  title's rung.  Supplying a wild-type peptide and scoring it against an
  engineered reference is not a measurement of what we claim to measure, so a
  strict primary panel cannot contain one.  All ten move to the extension tier,
  fully specified, with G19 (the deposited-tip arm) as the matched control.

  Implemented as an **eligibility filter on the pool**, not as a deletion of the
  chosen representative -- which is the faithful reading of "strict", and which
  matters: RUN_MATRIX §3.1 says "from each cluster take exactly one member, the
  one whose worse-resolution reference has the lowest resolution".  Filter the
  pool first and that rule re-selects inside any cluster that still has a clean
  member.  `BACKFILL = False` reproduces the harsher reading (drop the cluster
  outright); both counts are reported every run so the choice stays visible.

DECISION 2 -- the cognate assignment becomes TWO columns, not one.
  `supplied_partner_*` is the biology (what we hand the model) and
  `reference_tip_*` is the structure (what we score against).  We had been
  conflating them.  Where they disagree the row is flagged and the biology wins
  for the supplied partner.

DECISION 3 -- AA2AR is IN, as a declared override with its reason.
  It loses the adenosine cluster to AA1R by **0.14 A** of reference resolution
  and it is the only receptor on the panel with wet-lab data on our exact 21-mer
  (eddy2018extrinsictrp's W233-6.35 measurement and mazzoni2000's 11/13/15/17/19/21
  series are both A2AR).  The resolution rule stands everywhere else; this is an
  override, not a rule change, and it adds a receptor rather than a cluster.

Usage:  python3 redo/build/g1_panel_freeze.py
"""
import csv
import os
import sys
from collections import Counter, defaultdict

# Paths come from redo/paths.py so that moving a file costs one edit there
# and never silently changes what this script reads.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT, SPEC, BUILD, GATES, INPUTS, CACHE, STRUCTURES, RUNS, PROTOCOL, repo
OUT = os.path.join(INPUTS, "g1_panel_freeze.tsv")

BACKFILL = True
OVERRIDES_IN = {
    "AA2AR": "declared override: loses its cluster to AA1R by 0.14 A, and is the "
             "only panel receptor with wet-lab data on our exact 21-mer "
             "(eddy2018extrinsictrp W233-6.35; mazzoni2000's length series). "
             "Adds a receptor, not a cluster -- AA1R stays."
}

# family -> the declared representative subtype, for the SUPPLIED partner
FAMILY_REP = {"Gs": "Gs", "Gi/o": "Gi1", "Gq/11": "Gq", "G12/13": "G13"}
FAMOF = {"Gs": "Gs", "Golf": "Gs", "Gi1": "Gi/o", "Gi2": "Gi/o", "Gi3": "Gi/o",
         "Go": "Gi/o", "Gz": "Gi/o", "Gt1": "Gi/o", "Gt2": "Gi/o",
         "Ggust": "Gi/o", "Gq": "Gq/11", "G11": "Gq/11", "G14": "Gq/11",
         "G15": "Gq/11", "G12": "G12/13", "G13": "G12/13"}


def tsv(name):
    with open(os.path.join(INPUTS, name)) as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def main():
    problems = []
    rec = {r["slug"]: r for r in tsv("g1_receptors.tsv")}
    cog = {r["receptor_slug"]: r for r in tsv("g1_cognate.tsv")
           if r["rung"] == "R3_ct21"}
    cmap = {r["receptor_slug"]: r for r in tsv("coupling_cognate_map.tsv")}
    ca = {r["slug"]: r for r in csv.DictReader(
        open(os.path.join(INPUTS, "coupling_assignments.csv")))}

    ineligible = {s for s, c in cog.items() if not c["cognate_subtype"]}

    # ---- DECISION 1: re-run 3.1's rule on the eligible pool --------------
    clusters = defaultdict(list)
    for s, r in rec.items():
        clusters[r["cluster"]].append(s)
    frozen, lost, backfilled = set(), [], []
    for cl, members in sorted(clusters.items()):
        pool = [s for s in members if s not in ineligible]
        if not pool:
            lost.append(cl)
            continue
        pick = sorted(pool, key=lambda s: (float(rec[s]["worse_res"]), s))[0]
        was = [s for s in members if rec[s]["core32_provisional"] == "yes"]
        if not BACKFILL and was and was[0] in ineligible:
            lost.append(cl)
            continue
        if was and pick != was[0]:
            backfilled.append((cl, was[0], pick))
        frozen.add(pick)
    for s in OVERRIDES_IN:
        if s in ineligible:
            problems.append(f"override {s} is chimeric-reference and cannot be "
                            f"added to a strict panel")
        else:
            frozen.add(s)

    n_clusters = len({rec[s]["cluster"] for s in frozen})

    # ---- emit -------------------------------------------------------------
    rows = []
    for s in sorted(rec):
        c, cm = cog[s], cmap[s]
        ann = set(x for x in cm["annotation_family"].split(";") if x)
        st = c["cognate_subtype"]
        st_fam = FAMOF.get(st, "")
        # Decision 2: the biology column.  `recommended_family` is NOT usable as
        # the biology on its own -- 13 of 64 rows have recommended_basis "taken
        # from the deposited active reference", i.e. the structure already leaked
        # into it.  The structure-independent column is the annotated family set.
        basis = ca[s]["recommended_basis"]
        annot_only = not basis.startswith("taken from the deposited")
        supplied_fam = ca[s]["recommended_family"]
        # The column is ALWAYS populated -- an empty biology column re-conflates
        # the two questions by omission. What varies is its independence, and that
        # is recorded rather than hidden: on 13 of 64 receptors the coupling
        # table's recommendation was itself "taken from the deposited active
        # reference", so for those the two columns are not independent. On three
        # of them the deposited reference is the CHIMERA -- circular in exactly the
        # way a crystallisation scaffold is: its tip reads Gq because someone made
        # it read Gq.
        indep = ("annotation only -- independent of the structure" if annot_only
                 else ("NOT INDEPENDENT: the coupling recommendation was taken from "
                       "the deposited reference, and that reference is CHIMERIC"
                       if not st else
                       "NOT INDEPENDENT: the coupling recommendation was taken from "
                       "the deposited reference"))
        agree = "n/a" if not st else ("yes" if st_fam in ann or st_fam == supplied_fam
                                      else "NO")
        rows.append(dict(
            receptor_slug=s, cluster=rec[s]["cluster"],
            worse_res=rec[s]["worse_res"],
            core32_provisional=rec[s]["core32_provisional"],
            core_frozen="yes" if s in frozen else "no",
            tier=("PRIMARY" if s in frozen else
                  "EXTENSION-chimeric-reference" if s in ineligible else
                  "EXTENSION-census"),
            exclusion_reason=("chimeric active reference: engineered alpha5 tip, "
                              "ineligible for a strict primary panel"
                              if s in ineligible else ""),
            override_reason=OVERRIDES_IN.get(s, ""),
            # --- Decision 2: two columns, never one
            supplied_partner_family=supplied_fam,
            supplied_partner_subtype=(st if st and st_fam == supplied_fam
                                      else FAMILY_REP.get(supplied_fam, "")),
            supplied_partner_basis=("structure-read subtype inside the annotated "
                                    "family" if st and st_fam == supplied_fam
                                    else "annotation; declared family representative"),
            supplied_partner_independence=indep,
            reference_tip_subtype=st or "CHIMERIC -- no canonical subtype",
            reference_tip_family=st_fam or "CHIMERIC",
            reference_tip_evidence=c["evidence_class"],
            annotation_family_set=cm["annotation_family"],
            annotation_verdict=cm["annotation_verdict"],
            cognate_vs_reference_agree=agree,
            reverses_blockb_prior=c["reverses_blockb_prior"],
            blockb_prior=c["blockb_prior"]))

    cols = list(rows[0].keys())
    with open(OUT, "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r[c]) for c in cols) + "\n")

    w = sys.stderr.write
    w(f"# wrote {len(rows)} rows -> {OUT}\n\n")
    w(f"# DECISION 1 -- {len(ineligible)} chimeric-reference receptors ineligible: "
      f"{sorted(ineligible)}\n")
    w(f"#   of which were CORE-32 representatives: "
      f"{sorted(s for s in ineligible if rec[s]['core32_provisional']=='yes')}\n")
    if backfilled:
        w(f"#   backfilled by re-running 3.1 on the eligible pool "
          f"(BACKFILL={BACKFILL}):\n")
        for cl, was, now in backfilled:
            w(f"#     cluster {cl}: {was} -> {now} "
              f"({rec[was]['worse_res']} -> {rec[now]['worse_res']} A)\n")
    w(f"#   clusters lost outright (no eligible member): {len(lost)} {lost}\n")
    w(f"# DECISION 3 -- overrides IN: {sorted(OVERRIDES_IN)}\n")
    w(f"\n# FROZEN PRIMARY PANEL: {len(frozen)} receptors in {n_clusters} clusters\n")
    w(f"#   {sorted(frozen)}\n")
    prov_n = sum(1 for r in rec.values() if r["core32_provisional"] == "yes")
    w(f"#   was {prov_n} receptors in {prov_n} clusters\n")
    w(f"#   pooled half-widths scale by sqrt({prov_n}/{n_clusters}) = "
      f"{(prov_n / n_clusters) ** 0.5:.3f}\n")
    w(f"#   without backfill it would be {prov_n - len([s for s in ineligible if rec[s]['core32_provisional']=='yes'])}"
      f" clusters, scaling {(prov_n / (prov_n - len([s for s in ineligible if rec[s]['core32_provisional']=='yes']))) ** 0.5:.3f}\n")
    w(f"\n# DECISION 2 -- cognate vs reference tip, on all {len(rows)} receptors:\n")
    w(f"#   {dict(Counter(r['cognate_vs_reference_agree'] for r in rows))}\n")
    dis = sorted(r["receptor_slug"] for r in rows
                 if r["cognate_vs_reference_agree"] == "NO")
    w(f"#   family-level disagreements: {dis if dis else 'NONE on the 54 resolvable receptors'}\n")
    ni = sorted(r["receptor_slug"] for r in rows
                if r["supplied_partner_independence"].startswith("NOT"))
    nic = sorted(r["receptor_slug"] for r in rows
                 if "CHIMERIC" in r["supplied_partner_independence"])
    w(f"#   coupling recommendation NOT independent of the structure: "
      f"{len(ni)} -> {ni}\n")
    w(f"#     of which the structure is the chimera (circular): {nic}\n")
    w(f"#     any of those in the frozen primary panel? "
      f"{sorted(s for s in nic if any(r['receptor_slug']==s and r['core_frozen']=='yes' for r in rows)) or 'NO'}\n")
    w(f"#   reverses Block B's prior (a DIFFERENT question): "
      f"{sorted(r['receptor_slug'] for r in rows if r['reverses_blockb_prior']=='yes')}\n")
    if problems:
        w("\n!! PROBLEMS\n" + "\n".join("  " + p for p in problems) + "\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
