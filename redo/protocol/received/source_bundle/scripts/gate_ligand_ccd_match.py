#!/usr/bin/env python3
"""Regression gate for CCD-sourced SMILES in refs/ligand_set.csv.

For every row with `smiles_source` starting `CCD:<pdb>:<ccd>`, this script:

  1. Re-fetches the CCD SMILES via RCSB Data REST API.
  2. Compares its RDKit-canonical form against the row's stored `ccd_smiles`.
  3. Confirms the RDKit-InChIKey connectivity block (first 14 chars) matches.
  4. Emits per-row PASS / FAIL / WARN.

Runs cheaply (~30 HTTP GETs) with an on-disk cache so repeated runs are fast.
Non-zero exit if any row FAILs -- this is a Block C pre-dispatch gate.

Rationale (Block C Step 1.1, 2026-09-04):
  Curation-error rate on memory-based SMILES was ~40-46% (four verification passes
  logged in experiments/020_block_c_ligand_pharmacology/analysis/
  ligand_curation_notes.md). CCD sourcing keys on the actual crystal chemistry
  rather than on named-molecule PubChem lookups. This gate ensures that the
  CCD-sourced SMILES do not silently drift: if a future edit or hand-fix changes
  the `smiles` or `ccd_smiles` column for a CCD-sourced row, this gate detects
  the drift against the authoritative RCSB CCD entry.

Primary-ligand disambiguation at multi-non-polymer PDBs (used only when
  regenerating ligand_set.csv from scratch -- NOT part of this gate's runtime):
  the default rule is "largest formula_weight after excluding waters, ions,
  lipids (CLR/OLA/OLC/OLB/1WV etc.), detergents (LMT/BOG/HTG), buffers
  (PGE/PG4/1PE/PEG/GOL/EDO/MES/EPE), glycans (NAG/BMA/BGC), cryoprotectants
  (EDT/TAM)". Two rows deliberately override that rule with an
  orthosteric-preferred pick because a drug-shaped PAM co-crystallised alongside
  the orthosteric agonist and outweighs it:
    - ACM4 full_agonist @ 7TRP: pick IXO (iperoxo, 0.197 kDa, orthosteric)
      not IUE (0.312 kDa, M4 positive allosteric modulator).
    - AA1R full_agonist @ 7LD3: pick ADN (adenosine, 0.267 kDa, orthosteric)
      not XTD (0.45 kDa, A1 PAM, bis-CF3-thiophene / chlorophenyl methanone).
  Block C pharmacology measures orthosteric-pocket engagement, so the crystal
  ligand of record is the orthosteric partner even when the PAM is heavier.
  Any future rebuild of the CSV must re-apply that override — this gate itself
  only verifies whatever ccd_code the CSV declares, so drift there would present
  as a "ccd_code column != smiles_source" FAIL if the CSV rebuild picks the PAM.

Usage:
  python scripts/gate_ligand_ccd_match.py                # pretty per-row
  python scripts/gate_ligand_ccd_match.py --fail-warns   # WARN also non-zero
  python scripts/gate_ligand_ccd_match.py --no-cache     # force refresh
  python scripts/gate_ligand_ccd_match.py --csv <path>   # custom CSV path

Exit codes:
  0  all CCD-sourced rows match RCSB
  1  at least one FAIL (connectivity mismatch or fetch failure)
  2  --fail-warns and at least one WARN (canonical-SMILES byte drift only)
"""
from __future__ import annotations
import argparse, csv, hashlib, json, os, sys
from pathlib import Path

import requests
try:
    from rdkit import Chem, RDLogger
    RDLogger.DisableLog("rdApp.*")
except ImportError:
    sys.stderr.write("ERROR: rdkit is required (pip install rdkit).\n")
    sys.exit(3)

REPO = Path(__file__).resolve().parent.parent
DEFAULT_CSV = REPO / "refs" / "ligand_set.csv"
CACHE_DIR = Path(os.environ.get("CCD_GATE_CACHE", str(REPO / ".cache" / "ccd_gate")))
RCSB_BASE = "https://data.rcsb.org/rest/v1"


def fetch_chemcomp(ccd: str, use_cache: bool = True) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache = CACHE_DIR / f"cc_{ccd}.json"
    if use_cache and cache.exists():
        return json.loads(cache.read_text())
    r = requests.get(f"{RCSB_BASE}/core/chemcomp/{ccd}", timeout=45)
    r.raise_for_status()
    j = r.json()
    cache.write_text(json.dumps(j))
    return j


def ccd_isomeric_smiles(cc: dict) -> tuple[str | None, str | None]:
    """Return (isomeric_smiles, stored_inchikey) preferring OpenEye SMILES_CANONICAL."""
    desc = cc.get("pdbx_chem_comp_descriptor", []) or []
    oe_iso = cactvs_iso = ikey = None
    for d in desc:
        t, p, v = d.get("type"), d.get("program"), d.get("descriptor")
        if t == "SMILES_CANONICAL" and p and "OpenEye" in p:
            oe_iso = v
        elif t == "SMILES_CANONICAL" and p == "CACTVS":
            cactvs_iso = v
        elif t == "InChIKey":
            ikey = v
    return (oe_iso or cactvs_iso), ikey


def parse_smiles_source(src: str) -> tuple[str, str] | None:
    """Parse 'CCD:<pdb>:<ccd>' -> (pdb, ccd); return None for other schemes."""
    if not src.startswith("CCD:"):
        return None
    _, _, tail = src.partition(":")
    pdb, _, ccd = tail.partition(":")
    if not pdb or not ccd:
        return None
    return pdb, ccd


def check_row(row: dict, use_cache: bool) -> dict:
    """Return {status, row_key, detail}."""
    key = f"{row['receptor']}/{row['ligand_role']}"
    src = row.get("smiles_source", "")
    parsed = parse_smiles_source(src)
    if parsed is None:
        return {"key": key, "status": "SKIP", "detail": f"non-CCD source: {src!r}"}
    pdb, ccd_expected = parsed

    if row.get("ccd_code") != ccd_expected:
        return {"key": key, "status": "FAIL",
                "detail": f"ccd_code column {row.get('ccd_code')!r} != smiles_source {ccd_expected!r}"}

    stored_ccd_smiles = row.get("ccd_smiles", "")
    stored_smiles = row.get("smiles", "")
    stored_pdb = row.get("bound_pdb", "")
    if stored_pdb != pdb:
        return {"key": key, "status": "FAIL",
                "detail": f"bound_pdb column {stored_pdb!r} != smiles_source pdb {pdb!r}"}

    try:
        cc = fetch_chemcomp(ccd_expected, use_cache=use_cache)
    except Exception as e:
        return {"key": key, "status": "FAIL", "detail": f"RCSB fetch failed for CCD {ccd_expected}: {e}"}

    ccd_smi, ccd_ikey = ccd_isomeric_smiles(cc)
    if ccd_smi is None:
        return {"key": key, "status": "FAIL", "detail": f"CCD {ccd_expected}: no isomeric SMILES in RCSB response"}

    mol_ccd = Chem.MolFromSmiles(ccd_smi)
    mol_row = Chem.MolFromSmiles(stored_ccd_smiles)
    if mol_ccd is None:
        return {"key": key, "status": "FAIL", "detail": f"CCD {ccd_expected}: RCSB SMILES unparseable: {ccd_smi!r}"}
    if mol_row is None:
        return {"key": key, "status": "FAIL", "detail": f"stored ccd_smiles unparseable: {stored_ccd_smiles!r}"}

    # Compare on connectivity InChIKey (first 14 chars). Full-stereo comparison is
    # not required here -- CCD's stored InChIKey and RDKit-computed InChIKey often
    # disagree on stereo layer even when both are correct encodings of the same
    # crystal ligand (RDKit and PDB use different chirality conventions on rings
    # with ambiguous stereo like ester CH in scopine-core tiotropium).
    row_ikey = Chem.MolToInchiKey(mol_row)
    ccd_rdkit_ikey = Chem.MolToInchiKey(mol_ccd)
    row_conn = row_ikey.split("-")[0]
    ccd_conn = ccd_rdkit_ikey.split("-")[0]
    if row_conn != ccd_conn:
        return {"key": key, "status": "FAIL",
                "detail": (f"CCD {ccd_expected} connectivity mismatch: "
                           f"stored_conn={row_conn} vs rcsb_conn={ccd_conn} "
                           f"(stored_ikey={row_ikey}, rcsb_rdkit_ikey={ccd_rdkit_ikey})")}

    # smiles column must equal ccd_smiles column for CCD-sourced rows
    if stored_smiles != stored_ccd_smiles:
        return {"key": key, "status": "FAIL",
                "detail": "smiles column diverges from ccd_smiles column for a CCD-sourced row"}

    # Byte-level SMILES check: if CCD's stored SMILES differs textually from the
    # stored value, warn (crystal-truth chemistry is preserved but the canonical
    # form drifted -- may reflect an RCSB SMILES normalization update).
    if ccd_smi != stored_ccd_smiles:
        # Verify RDKit-canonical equivalence (weaker check)
        can_row = Chem.MolToSmiles(mol_row)
        can_ccd = Chem.MolToSmiles(mol_ccd)
        if can_row != can_ccd:
            return {"key": key, "status": "FAIL",
                    "detail": (f"CCD {ccd_expected} SMILES canonical drift: "
                               f"stored_canonical={can_row!r} vs rcsb_canonical={can_ccd!r}")}
        return {"key": key, "status": "WARN",
                "detail": (f"CCD {ccd_expected} SMILES byte-drift (canonical equivalent): "
                           f"stored={stored_ccd_smiles!r} vs rcsb={ccd_smi!r}")}

    return {"key": key, "status": "PASS",
            "detail": f"CCD {ccd_expected} @ {pdb}: connectivity {row_conn} matches RCSB"}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--fail-warns", action="store_true",
                    help="also non-zero-exit on WARN (SMILES byte-drift with same canonical)")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not args.csv.exists():
        sys.stderr.write(f"ERROR: CSV not found: {args.csv}\n")
        sys.exit(3)

    with open(args.csv) as f:
        rows = list(csv.DictReader(f))

    ccd_rows = [r for r in rows if str(r.get("smiles_source","")).startswith("CCD:")]
    if not args.quiet:
        print(f"# gate_ligand_ccd_match  csv={args.csv}  ccd-sourced-rows={len(ccd_rows)}")
        print(f"# cache={CACHE_DIR}  no_cache={args.no_cache}")

    counts = {"PASS":0,"FAIL":0,"WARN":0,"SKIP":0}
    fails = []
    warns = []
    for r in rows:
        if not str(r.get("smiles_source","")).startswith("CCD:"):
            continue
        result = check_row(r, use_cache=not args.no_cache)
        counts[result["status"]] += 1
        if not args.quiet or result["status"] != "PASS":
            print(f"  [{result['status']}] {result['key']:30s}  {result['detail']}")
        if result["status"] == "FAIL":
            fails.append(result)
        elif result["status"] == "WARN":
            warns.append(result)

    print(f"\n# summary: PASS={counts['PASS']}  WARN={counts['WARN']}  FAIL={counts['FAIL']}  "
          f"(of {len(ccd_rows)} CCD-sourced rows)")
    if fails:
        print("# GATE FAILED -- see FAIL lines above")
        sys.exit(1)
    if warns and args.fail_warns:
        print("# GATE FAILED -- --fail-warns enabled and WARN present")
        sys.exit(2)
    print("# GATE PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
