#!/usr/bin/env python3
"""ligand_census.py -- per-receptor ligand census for the 64-receptor tier-C1 panel.

Promoted from a scratchpad worksheet to a generated input on 2026-09-12, because
ligand_tiers.py consumes it and an input with no generator in build/ is exactly
what inputs/MANIFEST.tsv exists to make impossible.

Source: lit/panels/cache/gpcrdb_structures.json -- the frozen GPCRdb snapshot
(1,716 structures, 1,828 ligand records) whose sha256 PANEL.md sec 10 pins.

THREE AXES, NEVER COLLAPSED
---------------------------
role      from the raw `function` string
modality  from the raw `type` string
site      DERIVED from role (allosteric roles name themselves)

Every raw value in the snapshot is enumerated below. If a value appears that is
not in the map the script FAILS -- a silent "other" bucket is the defect this
guard exists to catch.

Usage:  python3 redo/build/ligand_census.py            # writes redo/inputs/
        python3 redo/build/ligand_census.py <root> <out_dir>
"""
import csv
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import ROOT as _ROOT, INPUTS  # noqa: E402

# --- axis 1: role.  Raw `function` -> role.  All 12 observed values mapped. ---
ROLE_MAP = {
    "Agonist":               "agonist",
    "Agonist (partial)":     "partial_agonist",
    "Antagonist":            "antagonist",
    "Inverse agonist":       "inverse_agonist",
    "PAM":                   "pam",
    "NAM":                   "nam",
    "Ago-PAM":               "ago_pam",
    "Allosteric agonist":    "allosteric_agonist",
    "Allosteric antagonist": "allosteric_antagonist",
    "Apo (no ligand)":       "apo",
    "Cofactor":              "other_cofactor",
    "unknown":               "other_unknown",
    "":                      "other_unknown",
}

# --- axis 2: modality.  Raw `type` -> modality.  All 5 observed values mapped. --
MOD_MAP = {
    "small-molecule": "small-molecule",
    "peptide":        "peptide",
    "protein":        "protein",
    "lipid":          "lipid",
    "none":           "none",
    "":               "none",
}

# --- axis 3: site.  DERIVED from role, not read from the snapshot. -------------
# GPCRdb names the allosteric roles explicitly; everything with an orthosteric
# pharmacology name is treated as orthosteric.  apo/cofactor/unknown get n/a
# because the snapshot gives no basis to place them.
SITE_MAP = {
    "agonist":               "orthosteric",
    "partial_agonist":       "orthosteric",
    "antagonist":            "orthosteric",
    "inverse_agonist":       "orthosteric",
    "pam":                   "allosteric",
    "nam":                   "allosteric",
    "ago_pam":               "allosteric",
    "allosteric_agonist":    "allosteric",
    "allosteric_antagonist": "allosteric",
    "apo":                   "n/a",
    "other_cofactor":        "n/a",
    "other_unknown":         "n/a",
}

# --- class grouping used by every inclusion rule ------------------------------
# "activating" = agonist-side, "blocking" = antagonist-side.  Orthosteric-only
# membership is reported separately via the site axis; these sets deliberately
# include the allosteric roles so that rule (c) can subtract them rather than
# never having seen them.
ACTIVATING = {"agonist", "partial_agonist", "allosteric_agonist", "ago_pam", "pam"}
BLOCKING = {"antagonist", "inverse_agonist", "allosteric_antagonist", "nam"}
ORTHO_ACTIVATING = {"agonist", "partial_agonist"}
ORTHO_BLOCKING = {"antagonist", "inverse_agonist"}

# modalities that are a CHAIN in a co-folding model, not a SMILES
CHAIN_MODALITIES = {"peptide", "protein"}


def load(root):
    snap = json.load(open(os.path.join(root, "lit", "panels", "cache",
                                       "gpcrdb_structures.json")))
    g1 = list(csv.DictReader(
        open(os.path.join(root, "redo", "inputs", "g1_receptors.tsv")), delimiter="\t"))
    psys = {r["slug"]: r for r in csv.DictReader(
        open(os.path.join(root, "redo", "inputs", "panel_systems.csv")))}
    freeze = {r["receptor_slug"]: r for r in csv.DictReader(
        open(os.path.join(root, "redo", "inputs", "g1_panel_freeze.tsv")), delimiter="\t")}
    return snap, g1, psys, freeze


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else _ROOT
    outdir = sys.argv[2] if len(sys.argv) > 2 else INPUTS
    snap, g1, psys, freeze = load(root)

    # --- resolve each panel slug to every GPCRdb protein entry, EVERY species.
    # HANDOVER.md: never let _human be a silent default.  The snapshot holds both
    # adrb1_human and adrb1_melga and the panel's ADRB1 is human.
    known = sorted({str(e.get("protein", "")).lower() for e in snap})
    slug2prots = {}
    for r in g1:
        g = (psys.get(r["slug"], {}).get("gpcrdb_slug", "") or "").lower()
        if not g:
            raise SystemExit(f"no gpcrdb_slug for {r['slug']}")
        hits = [p for p in known if p == g or p.startswith(g + "_")]
        slug2prots[r["slug"]] = hits

    # collision guard: no GPCRdb protein entry may serve two panel slugs
    owner = {}
    for s, ps in slug2prots.items():
        for p in ps:
            if p in owner:
                raise SystemExit(f"COLLISION: {p} claimed by {owner[p]} and {s}")
            owner[p] = s
    prot2slug = owner

    # --- long-form record table ------------------------------------------------
    unmapped_fn, unmapped_ty = set(), set()
    records = []
    for e in snap:
        prot = str(e.get("protein", "")).lower()
        slug = prot2slug.get(prot)
        if slug is None:
            continue
        for lg in e.get("ligands") or []:
            fn = lg.get("function")
            ty = lg.get("type")
            fk = fn if fn is not None else ""
            tk = ty if ty is not None else ""
            if fk not in ROLE_MAP:
                unmapped_fn.add(fk)
                continue
            if tk not in MOD_MAP:
                unmapped_ty.add(tk)
                continue
            role = ROLE_MAP[fk]
            mod = MOD_MAP[tk]
            records.append({
                "receptor": slug,
                "gpcrdb_protein": prot,
                "structure_species": e.get("species") or "",
                "pdb": e.get("pdb_code") or "",
                "structure_state": e.get("state") or "",
                "resolution": e.get("resolution") if e.get("resolution") is not None else "",
                "role": role,
                "modality": mod,
                "site": SITE_MAP[role],
                "function_raw": fk,
                "type_raw": tk,
                "ligand_name": lg.get("name") or "",
                "ligand_ccd": lg.get("PDB") or "",
                "has_smiles": "1" if (lg.get("SMILES") or "").strip() else "0",
                "is_chain_coinput": "1" if mod in CHAIN_MODALITIES else "0",
            })

    if unmapped_fn or unmapped_ty:
        raise SystemExit(f"UNMAPPED function={sorted(unmapped_fn)} type={sorted(unmapped_ty)}")

    reccols = ["receptor", "gpcrdb_protein", "structure_species", "pdb",
               "structure_state", "resolution", "role", "modality", "site",
               "function_raw", "type_raw", "ligand_name", "ligand_ccd",
               "has_smiles", "is_chain_coinput"]
    p1 = os.path.join(outdir, "ligand_census_records.tsv")
    with open(p1, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=reccols, delimiter="\t")
        w.writeheader()
        for r in sorted(records, key=lambda r: (r["receptor"], r["role"],
                                                r["modality"], r["ligand_ccd"])):
            w.writerow(r)

    # --- per-receptor summary ---------------------------------------------------
    by = defaultdict(list)
    for r in records:
        by[r["receptor"]].append(r)

    def mods(rows, roleset, ortho_only=False, species_match=None):
        out = set()
        for r in rows:
            if r["role"] not in roleset:
                continue
            if ortho_only and r["site"] != "orthosteric":
                continue
            if species_match is not None and r["species_ok"] != species_match:
                continue
            out.add(r["modality"])
        return out

    srows = []
    for r in g1:
        s = r["slug"]
        rows = by.get(s, [])
        panel_sp = r["organism"].split(" (")[0].strip()
        for x in rows:
            x["species_ok"] = "1" if x["structure_species"].strip() == panel_sp else "0"
        d = {
            "receptor": s,
            "cluster": r["cluster"],
            "organism": r["organism"],
            "tier": freeze.get(s, {}).get("tier", ""),
            "core32_provisional": r["core32_provisional"],
            "panel_ligands_col": r["ligands"],
            "n_structures": len({x["pdb"] for x in rows}),
            "n_ligand_records": len(rows),
        }
        for label, roleset, ortho in (
                ("act", ACTIVATING, False), ("blk", BLOCKING, False),
                ("oact", ORTHO_ACTIVATING, True), ("oblk", ORTHO_BLOCKING, True)):
            m = mods(rows, roleset, ortho)
            d[f"{label}_modalities"] = ";".join(sorted(m)) if m else ""
            msp = mods(rows, roleset, ortho, species_match="1")
            d[f"{label}_modalities_panelspecies"] = ";".join(sorted(msp)) if msp else ""
        # per-role counts, every role kept separate
        for role in sorted(SITE_MAP):
            d[f"n_{role}"] = sum(1 for x in rows if x["role"] == role)
        for mod in ("small-molecule", "peptide", "protein", "lipid", "none"):
            d[f"n_mod_{mod}"] = sum(1 for x in rows if x["modality"] == mod)
        d["n_site_orthosteric"] = sum(1 for x in rows if x["site"] == "orthosteric")
        d["n_site_allosteric"] = sum(1 for x in rows if x["site"] == "allosteric")
        srows.append(d)

    scols = list(srows[0].keys())
    p2 = os.path.join(outdir, "ligand_census_receptors.tsv")
    with open(p2, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=scols, delimiter="\t")
        w.writeheader()
        for d in sorted(srows, key=lambda d: d["receptor"]):
            w.writerow(d)

    print(f"wrote {p1}  ({len(records)} ligand records)")
    print(f"wrote {p2}  ({len(srows)} receptors)")
    print(f"receptors with zero snapshot ligand records: "
          f"{[d['receptor'] for d in srows if d['n_ligand_records'] == 0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
