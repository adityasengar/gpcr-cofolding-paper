#!/usr/bin/env python3
"""
build_panels.py - assemble the receptor panels of the corpus's key GPCR papers.

The panels live in supplementary tables. Where the SI has been obtained, its table IS
the panel and is used verbatim (provenance `SI-verified`). Where it has not, the paper's
stated selection rule is re-run against GPCRdb and scored against the published counts
(provenance `reconstructed`).

    python3 build_panels.py            # build panels.csv
    python3 build_panels.py --refresh  # re-fetch GPCRdb first

THE LESSON THAT GOVERNS THIS FILE. Reconstruction was first validated by comparing
counts. zhang's rule reproduced 250 complexes against a published 253 - 1.2% - and was
marked REPRODUCED. When Table S2 was later obtained, the reconstruction turned out to
share only 222 of its 253 entries: 31 missed and 28 invented, ~12% wrong in each
direction, at a count error of 1.2%. **A matching count is not a matching membership.**
So a reconstructed panel is now labelled `count-only` no matter how well the count
agrees, and is never treated as a receptor list. Only an SI join proves membership.

Second finding, from chiesa: a stated rule can under-determine its own panel. Its
Table S1 reproduces all four published counts exactly, yet the rule as written admits
152 further structures in the same window, spanning 23 receptors the panel omits
entirely, with no difference in method or resolution. The rule cannot be repaired from
the paper's text.
"""
import json, os, sys, csv, urllib.request, time

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "cache")
SI = os.path.join(HERE, "si_tables")
GPCRDB = os.path.join(CACHE, "gpcrdb_structures.json")


def load(refresh=False):
    if refresh or not os.path.exists(GPCRDB):
        req = urllib.request.Request("https://gpcrdb.org/services/structure/",
                                     headers={"accept": "application/json"})
        d = json.load(urllib.request.urlopen(req, timeout=90))
        json.dump(d, open(GPCRDB, "w"))
    else:
        d = json.load(open(GPCRDB))
    # GPCRdb's `publication_date` was checked against RCSB `initial_release_date` on
    # 2026-09-10: identical on all 1,713 matched entries. It already IS the PDB release
    # date - do not "correct" it.
    for x in d:
        x["rel"] = x["publication_date"]
    return d


def galpha(x):
    s = x.get("signalling_protein") or {}
    if s.get("type") != "G protein":
        return ""
    for e in (s.get("data") or {}).values():
        if e.get("entry_name", "").startswith("gna"):
            return e["entry_name"]
    return ""


def ligand_modality(x):
    t = {l.get("type") for l in (x.get("ligands") or [])}
    for k in ("small-molecule", "peptide", "protein"):
        if k in t:
            return k
    return "none" if not t else sorted(t)[0]


def fam(x, lvl):
    return "_".join(x["family"].split("_")[:lvl])


def row(paper, pdb, G, provenance, **extra):
    x = G.get(pdb.upper(), {})
    r = dict(paper=paper, pdb_id=pdb.upper(),
             receptor=x.get("protein", "NOT-IN-GPCRDB"),
             receptor_class=x.get("class", ""), gpcrdb_family=x.get("family", ""),
             state=x.get("state", ""), state_source="", resolution=x.get("resolution", ""),
             method=x.get("type", ""), release_date=x.get("rel", ""),
             partner_type=(x.get("signalling_protein") or {}).get("type", "none"),
             partner_galpha=galpha(x) if x else "",
             ligand_modality=ligand_modality(x) if x else "",
             ligand_ccd="", ligand_pharmacology="", panel_unit="structure",
             subset="benchmark", provenance=provenance)
    r.update(extra)
    return r


# ---------------- SI-verified panels ----------------

def si_zhang(G):
    """Table S2, 253 entries. Extracted from the npj SI DOCX."""
    out = []
    for t in csv.DictReader(open(os.path.join(SI, "zhang2026generalization_tableS2.csv"))):
        out.append(row("zhang2026generalization", t["PDB ID"], G, "SI-verified",
                       state=t["GPCR State"], state_source="paper Table S2",
                       resolution=t["Resolution"], receptor_class=t["GPCR Class"],
                       ligand_modality="small-molecule", ligand_ccd=t["Ligand CCD"],
                       ligand_pharmacology=t["Ligand Pharmacology"]))
    # NB: `families` here is OUR GPCRdb level-4 count over their PDB IDs, not their
    # figure. It differs from their published 74 because GPCRdb reclassifies; the panel
    # itself is verbatim and exact. Reported as context, not as a discrepancy.
    return out, dict(complexes=len(out),
                     families_gpcrdb_l4=len({fam(G[r["pdb_id"]], 4) for r in out if r["pdb_id"] in G}))


def si_chiesa(G):
    """Table S1, 145 entries across 55 receptors. Extracted from the ACS SI PDF."""
    out = []
    for t in csv.DictReader(open(os.path.join(SI, "chiesa2025templatebias_tableS1.csv"))):
        out.append(row("chiesa2025templatebias", t["pdb_id"], G, "SI-verified",
                       state_source="paper Table S1 (all active)"))
        out[-1]["receptor_family_paper"] = t["receptor_family"]
        out[-1]["receptor_paper"] = t["receptor"]
    recs = {r["receptor_paper"] for r in out}
    return out, dict(structures=len(out), receptors=len(recs),
                     families=len({r["receptor_family_paper"] for r in out}),
                     pairs=len({(r["receptor_paper"], r["partner_galpha"]) for r in out}))


def si_heo(G):
    """bioRxiv v2 SI (the revision that became Proteins 90:1873). Table S2 is a RECEPTOR
    list with per-state structure counts, not a structure list - hence panel_unit.
    Table S3 (the docking subset, whose n the note recorded as NOT REPORTED) is a
    structure list and is emitted as a separate subset."""
    names = {x["protein"] for x in G.values()}
    out = []
    for t in csv.DictReader(open(os.path.join(SI, "heo2022multistate_tableS2.csv"))):
        gene = t["gene"].split("-")[0].lower() + "_human"
        r = row("heo2022multistate", "", G, "SI-verified",
                state_source="paper Table S2 (per-state structure counts)")
        r.update(pdb_id="", panel_unit="receptor", subset="benchmark",
                 receptor=gene if gene in names else "NOT-IN-GPCRDB",
                 receptor_paper=t["gene"], receptor_class="Class " + t["cls"],
                 state=f"active={t['n_active']};inactive={t['n_inactive']}")
        out.append(r)
    n_rec = len(out)
    a = sum(1 for t in csv.DictReader(open(os.path.join(SI, "heo2022multistate_tableS2.csv"))) if int(t["n_active"]) > 0)
    i = sum(1 for t in csv.DictReader(open(os.path.join(SI, "heo2022multistate_tableS2.csv"))) if int(t["n_inactive"]) > 0)
    b = sum(1 for t in csv.DictReader(open(os.path.join(SI, "heo2022multistate_tableS2.csv")))
            if int(t["n_active"]) > 0 and int(t["n_inactive"]) > 0)
    for t in csv.DictReader(open(os.path.join(SI, "heo2022multistate_tableS3_docking.csv"))):
        r = row("heo2022multistate", t["pdb_id"], G, "SI-verified",
                state_source="paper Table S3")
        r.update(subset="docking", state=t["state"], receptor_paper=t["gene"],
                 ligand_ccd=t["ligand_ccd"])
        out.append(r)
    return out, dict(receptors=n_rec, active=a, inactive=i, both=b,
                     docking_complexes=sum(1 for r in out if r["subset"] == "docking"))


def si_lee(G):
    """assets/gpcr/references.csv from the authors' repo, github.com/aqlaboratory/confornets.
    51 receptor pairs, 102 structures, no structure reused across pairs. Column
    `pdbidchain_i` is the ACTIVE member and `pdbidchain_j` the INACTIVE member in all 51
    rows, checked against GPCRdb. The paper publishes only the pair count; the repo is the
    only enumeration of which receptors."""
    out = []
    for t in csv.DictReader(open(os.path.join(SI, "lee2026confornets_gpcr_references.csv"))):
        for col, role in (("pdbidchain_i", "active"), ("pdbidchain_j", "inactive")):
            pdb, chain = t[col].split("_")
            r = row("lee2026confornets", pdb, G, "authors-repo",
                    state_source="authors' benchmark file (state cross-checked vs GPCRdb)")
            r.update(subset=f"gpcr-pair:{role}", receptor_paper=t["test_case"], chain=chain)
            out.append(r)
    return out, dict(pairs=len(out) // 2, structures=len({r["pdb_id"] for r in out}))


# ---------------- rule-only reconstructions ----------------

def rule_lee(d, G):
    pool = [x for x in d if x["rel"] <= "2025-12-31"]
    act = {x["protein"] for x in pool if x["state"] == "Active"}
    ina = {x["protein"] for x in pool if x["state"] == "Inactive"}
    both = act & ina
    sel = [x for x in pool if x["protein"] in both and x["state"] in ("Active", "Inactive")]
    return ([row("lee2026confornets", x["pdb_code"], G, "count-only",
                 state_source="GPCRdb annotation") for x in sel],
            dict(receptors=len(both)))


def rule_heo(d, G):
    sel = [x for x in d if x["species"] == "Homo sapiens" and "2018-04-30" < x["rel"] <= "2021-06-30"]
    a = {x["protein"] for x in sel if x["state"] == "Active"}
    i = {x["protein"] for x in sel if x["state"] == "Inactive"}
    return ([row("heo2022multistate", x["pdb_code"], G, "count-only",
                 state_source="GPCRdb annotation") for x in sel],
            dict(receptors=len(a | i), active=len(a), inactive=len(i), both=len(a & i)))


PANELS = [
    dict(paper="zhang2026generalization", kind="SI", fn=si_zhang,
         published=dict(complexes=253),
         source="npj Drug Discovery SI, Table S2"),
    dict(paper="chiesa2025templatebias", kind="SI", fn=si_chiesa,
         published=dict(structures=145, receptors=55, families=31, pairs=63),
         source="ACS JCIM SI (ci5c00489_si_001.pdf), Table S1"),
    dict(paper="lee2026confornets", kind="SI", fn=si_lee,
         published=dict(pairs=51),
         source="authors' repo github.com/aqlaboratory/confornets, assets/gpcr/references.csv"),
    dict(paper="heo2022multistate", kind="SI", fn=si_heo,
         published=dict(receptors=68, active=49, inactive=30, both=15),
         source="bioRxiv v2 SI, Tables S2 (receptors) + S3 (docking structures)"),
]


def main():
    d = load(refresh="--refresh" in sys.argv)
    G = {x["pdb_code"].upper(): x for x in d}
    print(f"GPCRdb structures: {len(d)}\n")

    rows = []
    for P in PANELS:
        sel, got = P["fn"](G) if P["kind"] == "SI" else P["fn"](d, G)
        tag = "VERIFIED" if P["kind"] == "SI" else "count-only (NOT a receptor list)"
        print(f"{P['paper']:28s} {tag}")
        print(f"    {P['source']}")
        for k, w in P["published"].items():
            g = got.get(k)
            mark = "exact" if g == w else (f"{abs(g-w)/w*100:.1f}% off" if g is not None else "-")
            print(f"    {k:12s} published {w:5d}   ours {str(g):>5}   {mark}")
        for k, v in got.items():
            if k not in P["published"]:
                print(f"    {k:12s} (ours only)      {v}")
        print()
        if P["kind"] == "SI":
            rows += sel
        else:
            print("    -> no rows emitted: a count-only rule is not a receptor list\n")

    fields = ["paper", "subset", "panel_unit", "pdb_id", "receptor", "receptor_paper", "receptor_class", "chain",
              "gpcrdb_family", "receptor_family_paper", "state", "state_source",
              "resolution", "method", "release_date", "partner_type", "partner_galpha",
              "ligand_modality", "ligand_ccd", "ligand_pharmacology", "provenance"]
    out = os.path.join(HERE, "panels.csv")
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"wrote {out}: {len(rows)} verified rows across "
          f"{len({r['paper'] for r in rows})} panels, "
          f"{len({r['receptor'] for r in rows})} distinct receptors")


if __name__ == "__main__":
    main()
