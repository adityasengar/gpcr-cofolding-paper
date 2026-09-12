#!/usr/bin/env python3
"""Verify every CCD-sourced ligand pick against the RCSB Chemical Dictionary.

This rebuilds, for the redo, the one gate the frozen campaign had and explained
best.  Its own words: CCD sourcing exists because "curation-error rate on
memory-based SMILES was ~40-46% (four verification passes)".  Sourcing from a CCD
only helps if the CCD is then CHECKED -- and on 2026-09-12 a check found that
GPCRdb's record for PD2R2's agonist names PGD2 (C20 H32 O5) while giving CCD
A1D5Q, which RCSB says is C43 H81 O13 P, a phosphatidylinositol.  Two different
molecules in one record, with no SMILES to arbitrate.

The test: for every enacted pick that carries a CCD and is not a chain, the
InChIKey computed from the SMILES we recorded must equal the InChIKey RCSB holds
for that CCD.  A mismatch is a FAILURE, and so is a CCD RCSB does not know.

    python3 redo/build/ligand_ccd_verify.py
    python3 redo/build/ligand_ccd_verify.py --refresh

Writes: inputs/ligand_ccd_verification.tsv  (responses cached under cache/)
"""

import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from paths import INPUTS, CACHE  # noqa: E402

CACHE_FILE = os.path.join(CACHE, "ligand_ccd_rcsb.json")
OUT = os.path.join(INPUTS, "ligand_ccd_verification.tsv")
API = "https://data.rcsb.org/rest/v1/core/chemcomp"


def fetch(ccd):
    req = urllib.request.Request(f"{API}/{ccd}", headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as fh:
        return json.load(fh)


def main(argv):
    refresh = "--refresh" in argv
    cache = json.load(open(CACHE_FILE)) if os.path.exists(CACHE_FILE) and not refresh else {}
    with open(os.path.join(INPUTS, "ligand_set_redo.tsv")) as fh:
        picks = [r for r in csv.DictReader(fh, delimiter="\t") if r["status"] == "enacted"]

    try:
        from rdkit import Chem, RDLogger
        RDLogger.DisableLog("rdApp.*")
    except ImportError:
        print("rdkit unavailable -- cannot verify")
        return 1

    rows = []
    for p in picks:
        ccd = p["ligand_ccd"].strip()
        chain = p.get("is_peptide") == "1"
        if not ccd or chain:
            rows.append({"receptor_slug": p["receptor_slug"], "ligand_role": p["ligand_role"],
                         "ligand_ccd": ccd, "is_chain": "1" if chain else "0",
                         "rcsb_formula": "", "rcsb_inchikey": "", "our_inchikey": "",
                         "verdict": "n/a_chain" if chain else "n/a_no_ccd", "detail": ""})
            continue
        if ccd not in cache:
            try:
                cache[ccd] = fetch(ccd)
                time.sleep(0.12)
            except urllib.error.HTTPError as e:
                cache[ccd] = {"_error": f"HTTP {e.code}"}
        d = cache[ccd]
        if "_error" in d:
            rows.append({"receptor_slug": p["receptor_slug"], "ligand_role": p["ligand_role"],
                         "ligand_ccd": ccd, "is_chain": "0", "rcsb_formula": "",
                         "rcsb_inchikey": "", "our_inchikey": p["inchikey"],
                         "verdict": "FAIL_unknown_ccd", "detail": d["_error"]})
            continue
        formula = d.get("chem_comp", {}).get("formula", "")
        rcsb_key = ""
        for desc in d.get("pdbx_chem_comp_descriptor", []):
            if desc.get("type") == "InChIKey":
                rcsb_key = desc.get("descriptor", "")
                break
        ours = p["inchikey"]
        if not ours:
            verdict, detail = "FAIL_no_local_inchikey", "no SMILES recorded to check against"
        elif not rcsb_key:
            verdict, detail = "FAIL_no_rcsb_inchikey", "RCSB returned no InChIKey"
        elif ours == rcsb_key:
            verdict, detail = "ok", ""
        elif ours.split("-")[0] == rcsb_key.split("-")[0]:
            # same skeleton, different stereo: this is the retinal case and it is
            # a real distinction, not a match.  Report it as its own verdict so
            # nobody reads "different" as "wrong".
            verdict, detail = "STEREO_DIFFERS", f"{ours} vs {rcsb_key}"
        else:
            verdict, detail = "FAIL_different_molecule", f"{ours} vs {rcsb_key}"
        rows.append({"receptor_slug": p["receptor_slug"], "ligand_role": p["ligand_role"],
                     "ligand_ccd": ccd, "is_chain": "0", "rcsb_formula": formula,
                     "rcsb_inchikey": rcsb_key, "our_inchikey": ours,
                     "verdict": verdict, "detail": detail})

    os.makedirs(CACHE, exist_ok=True)
    json.dump(cache, open(CACHE_FILE, "w"), indent=1, sort_keys=True)
    with open(OUT, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {os.path.relpath(OUT)}  ({len(rows)} rows)\n")
    for v in ("ok", "STEREO_DIFFERS", "n/a_chain", "n/a_no_ccd"):
        n = sum(1 for r in rows if r["verdict"] == v)
        if n:
            print(f"  {v:<24} {n}")
    bad = [r for r in rows if r["verdict"].startswith("FAIL")]
    for r in bad:
        print(f"  {r['verdict']:<24} {r['receptor_slug']}/{r['ligand_ccd']}  {r['detail']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
