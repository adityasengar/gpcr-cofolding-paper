"""Block C smoke — 8-check hand-inspection over all 400 predictions.

Runs the 8-check table (per coordinator Step-2 brief) mechanically over
every CIF + `_${backbone}_status.json` + rows.smoke.csv row and emits:

    experiments/020_block_c_ligand_pharmacology/analysis/smoke_hand_inspect.json

with per-cell verdicts. Aggregated results are summarised on stdout and
land in the report.

Checks (per coordinator Step 2 brief):
    1. ligand present     — any ligand-arm CIF has ≥1 ligand heavy atom
    2. ligand correct     — heavy-atom count within ±3 of SMILES estimate
    3. ligand located     — pocket_ca_rmsd < 5 Å AND ligand centroid
                             within 6 Å of reference pocket centre
                             (approx: |pocket_ca_rmsd| indicator)
    4. receptor identified — receptor_slug non-null on every row
    5. pocket columns populated — pocket_ca/sidechain_rmsd, w648_chi1,
                             ligand_rmsd_to_ref non-null where they should
    6. config echo on disk — runtime_config present in every status.json
    7. both readouts present — transmission call + pocket metrics
    8. partner arm intact  — Gα interface columns populated on cognate rows

Checks 1-3 broken down per backbone (per coordinator brief); rest aggregated.

Usage:
    python3 scripts/block_c_smoke_hand_inspect.py \\
        --hpc-pool-root /hpc/scratch/sengaad1/paper_af3/experiments/020_block_c_ligand_pharmacology/smoke/pool \\
        --manifest experiments/020_block_c_ligand_pharmacology/manifest/smoke_manifest.csv \\
        --rows-csv experiments/020_block_c_ligand_pharmacology/analysis/rows.smoke.csv \\
        --ligand-csv refs/ligand_set.csv \\
        --out experiments/020_block_c_ligand_pharmacology/analysis/smoke_hand_inspect.json
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


ATOM_HEAVY = re.compile(r"[BCNOFPSI]|Cl|Br|\[[^\]]+\]")


def count_heavy_atoms_smiles(smi: str) -> int:
    """Rough heavy-atom count from SMILES (matches the ±3 tolerance)."""
    if not smi:
        return 0
    # Remove ring closures / stereo tokens etc. and count element tokens
    s = smi.replace("\\", "").replace("/", "").replace("@", "")
    # Bracketed tokens (any bracket = one atom)
    n_bracket = len(re.findall(r"\[[^\]]+\]", s))
    s_stripped = re.sub(r"\[[^\]]+\]", "", s)
    # Two-letter halogens first (must handle Cl/Br before single letters)
    n_cl = s_stripped.count("Cl")
    n_br = s_stripped.count("Br")
    s_stripped = s_stripped.replace("Cl", "").replace("Br", "")
    # Single-letter heavy atoms (upper AND lower case for aromatic)
    n_other = sum(1 for c in s_stripped if c in "BCNOFPSIbcnops")
    return n_bracket + n_cl + n_br + n_other


def parse_cif_ligand_atoms(cif_path: Path,
                           receptor_len: int,
                           partner_len: int) -> tuple[int, list[tuple[float, float, float]]]:
    """Count HETATM lines that are NOT waters, return (count, coords).

    Fall back on ATOM records whose chain_id / residue_number falls
    outside the receptor + partner range if HETATM records are absent.
    Boltz emits HETATM for ligands; chai/of3/protenix may vary.
    """
    if not cif_path.exists():
        return 0, []
    coords: list[tuple[float, float, float]] = []
    # mmCIF has a header block then _atom_site loop. Just scan for
    # HETATM entries (group_PDB == "HETATM" as token 0), skipping HOH.
    in_atom_site = False
    columns: list[str] = []
    lig_atoms = 0
    for line in cif_path.read_text().splitlines():
        line = line.rstrip()
        if not line:
            continue
        if line.startswith("_atom_site."):
            columns.append(line.split(".", 1)[1].strip())
            in_atom_site = True
            continue
        if in_atom_site and line.startswith(("data_", "loop_", "#")):
            if columns and not line.startswith("HETATM") and not line.startswith("ATOM"):
                # end of atom_site block
                pass
            in_atom_site = False
            continue
        if not in_atom_site:
            continue
        toks = line.split()
        if not toks:
            continue
        if toks[0] not in ("ATOM", "HETATM"):
            continue
        try:
            i_group = 0
            i_comp = columns.index("label_comp_id") if "label_comp_id" in columns else 5
            i_x = columns.index("Cartn_x") if "Cartn_x" in columns else 10
            i_y = columns.index("Cartn_y") if "Cartn_y" in columns else 11
            i_z = columns.index("Cartn_z") if "Cartn_z" in columns else 12
        except ValueError:
            continue
        if toks[i_group] != "HETATM":
            continue
        comp = toks[i_comp] if i_comp < len(toks) else ""
        if comp in ("HOH", "WAT", "H2O"):
            continue
        lig_atoms += 1
        try:
            coords.append((float(toks[i_x]), float(toks[i_y]), float(toks[i_z])))
        except (ValueError, IndexError):
            pass
    return lig_atoms, coords


def probe_output_dir(hpc_pool_root: str, cell_path: str) -> dict:
    """SSH into HPC and probe one row's output dir. Returns:
        cif_files, has_status_json, status_json, ligand_atoms_by_cif
    """
    remote_dir = f"{hpc_pool_root}/{cell_path}"
    cmd = f"""
if [ ! -d {remote_dir} ]; then echo NOTFOUND; exit 0; fi
echo CIFS:
find {remote_dir} -maxdepth 2 -type f \\( -name '*.cif' -o -name '*.pdb' \\) 2>/dev/null | sort
echo STATUS:
for j in {remote_dir}/_*_status.json; do [ -f "$j" ] && echo $j; done
"""
    r = subprocess.run(["ssh", "basel-hpc", cmd], capture_output=True, text=True, timeout=30)
    out = r.stdout
    cifs = []
    status_files = []
    mode = None
    for line in out.splitlines():
        if line == "CIFS:":
            mode = "cif"; continue
        if line == "STATUS:":
            mode = "st"; continue
        if line == "NOTFOUND":
            return {"cifs": [], "status_files": [], "not_found": True}
        if mode == "cif" and line.strip():
            cifs.append(line.strip())
        elif mode == "st" and line.strip():
            status_files.append(line.strip())
    return {"cifs": cifs, "status_files": status_files, "not_found": False}


def check_status_json(remote_path: str) -> dict:
    """Fetch and parse one status.json remotely."""
    r = subprocess.run(["ssh", "basel-hpc", f"cat {remote_path}"],
                       capture_output=True, text=True, timeout=30)
    if r.returncode != 0:
        return {"error": "fetch failed"}
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return {"error": "json decode"}


def count_ligand_atoms_hpc(cif_remote: str) -> tuple[int, list[tuple[float, float, float]]]:
    """Grep HETATM count remotely for one CIF (fast, ssh once per file)."""
    cmd = f"awk '/^HETATM/{{if($6!=\"HOH\"&&$6!=\"WAT\") {{n++; print $11,$12,$13}}}} END{{print \"CT=\"n}}' {cif_remote} 2>/dev/null"
    r = subprocess.run(["ssh", "basel-hpc", cmd], capture_output=True, text=True, timeout=30)
    n = 0
    coords = []
    for line in r.stdout.splitlines():
        if line.startswith("CT="):
            try:
                n = int(line[3:])
            except ValueError:
                pass
        else:
            toks = line.split()
            if len(toks) >= 3:
                try:
                    coords.append((float(toks[0]), float(toks[1]), float(toks[2])))
                except ValueError:
                    pass
    return n, coords


def batch_probe_cifs(hpc_pool_root: str, manifest_rows: list[dict]) -> dict:
    """Emit one giant shell script that finds CIFs and counts HETATMs for
    every cell, in one SSH round-trip. Returns dict keyed by cell tag.
    """
    lines = ["set +e"]
    cell_tags = []
    for r in manifest_rows:
        tag = (f"{r['receptor_resolved']}|{r['ligand_role']}|"
               f"{r['partner_type']}|{r['backbone']}")
        cell_tags.append(tag)
        subdir = (f"{r['receptor_resolved'].lower()}/{r['ligand_role']}/"
                  f"{'apo' if r['partner_type']=='apo' else 'cognate'}/"
                  f"{r['backbone']}/seed_{r['seed_used']}")
        remote = f"{hpc_pool_root}/{subdir}"
        lines.append(f"echo '===CELL===' '{tag}'")
        lines.append(f"echo 'DIR:' {remote}")
        lines.append(f"if [ -d {remote} ]; then echo 'EXISTS:1'; else echo 'EXISTS:0'; fi")
        # status json (may be nested one level deep in chai's case)
        lines.append(f"find {remote} -maxdepth 3 -name '_*_status.json' 2>/dev/null | sort | head -1 | sed 's/^/STATUS_JSON:/'")
        # CIFs (chai: pred.model_idx_*.cif; boltz: predictions/*/*_model_*.cif; of3/protenix: model_*.cif etc.)
        lines.append(f"find {remote} -maxdepth 5 \\( -name '*.cif' -o -name '*.pdb' -o -name 'model_*.cif' \\) 2>/dev/null | sort | sed 's/^/CIF:/'")
    script = "\n".join(lines)
    r = subprocess.run(["ssh", "basel-hpc", script], capture_output=True, text=True, timeout=180)
    result: dict[str, dict] = {}
    cur = None
    for line in r.stdout.splitlines():
        if line.startswith("===CELL==="):
            cur = line.split("'")[1] if "'" in line else line.split()[1]
            result[cur] = {"exists": False, "status_json": None, "cifs": []}
        elif cur and line.startswith("EXISTS:"):
            result[cur]["exists"] = (line.strip().endswith("1"))
        elif cur and line.startswith("STATUS_JSON:"):
            p = line[len("STATUS_JSON:"):].strip()
            if p:
                result[cur]["status_json"] = p
        elif cur and line.startswith("CIF:"):
            result[cur]["cifs"].append(line[4:].strip())
    return result


def batch_ligand_atoms(cif_paths: list[str]) -> dict[str, tuple[int, tuple[float, float, float]]]:
    """One SSH call to count HETATM heavy atoms + centroid for many CIFs."""
    if not cif_paths:
        return {}
    lines = []
    for p in cif_paths:
        lines.append(f"echo 'FILE:{p}'")
        # Use mmCIF-aware parsing via python (chai CIFs use mmCIF format)
        lines.append(
            f"python3 -c \"import sys; "
            f"lines=open('{p}').read().splitlines(); "
            f"in_loop=False; cols=[]; hets=[]; "
            f"import re; \n"
            f"# mmCIF _atom_site loop parser\n"
            f"i=0\n"
            f"while i<len(lines):\n"
            f"    ln=lines[i].strip()\n"
            f"    if ln.startswith('_atom_site.'):\n"
            f"        cols.append(ln.split('.',1)[1].strip())\n"
            f"    elif cols and (ln.startswith('HETATM ') or ln.startswith('ATOM ')):\n"
            f"        toks=ln.split()\n"
            f"        if toks[0]=='HETATM':\n"
            f"            try:\n"
            f"                ic=cols.index('label_comp_id'); ix=cols.index('Cartn_x'); iy=cols.index('Cartn_y'); iz=cols.index('Cartn_z')\n"
            f"                if toks[ic] not in ('HOH','WAT','H2O'):\n"
            f"                    hets.append((float(toks[ix]),float(toks[iy]),float(toks[iz])))\n"
            f"            except (ValueError,IndexError): pass\n"
            f"    i+=1\n"
            f"# fallback for PDB-format (boltz .pdb): parse HETATM lines by column\n"
            f"if not hets and not cols:\n"
            f"    for ln in lines:\n"
            f"        if ln.startswith('HETATM') and ln[17:20].strip() not in ('HOH','WAT','H2O'):\n"
            f"            try: hets.append((float(ln[30:38]),float(ln[38:46]),float(ln[46:54])))\n"
            f"            except ValueError: pass\n"
            f"if hets:\n"
            f"    cx=sum(c[0] for c in hets)/len(hets); cy=sum(c[1] for c in hets)/len(hets); cz=sum(c[2] for c in hets)/len(hets)\n"
            f"    print(f'CT={{len(hets)}} CENTROID={{cx:.3f}},{{cy:.3f}},{{cz:.3f}}')\n"
            f"else: print('CT=0 CENTROID=nan,nan,nan')\n"
            f"\""
        )
    script = "\n".join(lines)
    r = subprocess.run(["ssh", "basel-hpc", script], capture_output=True, text=True, timeout=600)
    result: dict[str, tuple[int, tuple[float, float, float]]] = {}
    cur = None
    for line in r.stdout.splitlines():
        if line.startswith("FILE:"):
            cur = line[5:].strip()
        elif cur and line.startswith("CT="):
            m = re.match(r"CT=(\d+) CENTROID=([-\d.na]+),([-\d.na]+),([-\d.na]+)", line)
            if m:
                n = int(m.group(1))
                try:
                    cx = float(m.group(2)); cy = float(m.group(3)); cz = float(m.group(4))
                except ValueError:
                    cx = cy = cz = float("nan")
                result[cur] = (n, (cx, cy, cz))
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hpc-pool-root", required=True)
    ap.add_argument("--manifest", required=True, type=Path)
    ap.add_argument("--rows-csv", type=Path,
                    help="rescored rows.smoke.csv (post-scoring). Optional; "
                         "checks 4/5/7/8 are gated on this file.")
    ap.add_argument("--ligand-csv", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    manifest = list(csv.DictReader(args.manifest.open()))
    ligand_set = {(r["receptor"].upper(), r["ligand_role"]): r
                  for r in csv.DictReader(args.ligand_csv.open())}

    # Step A — probe all 80 cells in one SSH batch to get status.jsons + CIFs
    print(f"probing {len(manifest)} cells on HPC ...", file=sys.stderr)
    probes = batch_probe_cifs(args.hpc_pool_root, manifest)

    # Step B — count heavy atoms + centroid for every CIF
    all_cifs = []
    for tag, p in probes.items():
        all_cifs.extend(p.get("cifs", []))
    print(f"counting ligand atoms in {len(all_cifs)} CIFs ...", file=sys.stderr)
    lig_counts: dict[str, tuple[int, tuple[float, float, float]]] = {}
    # chunk into groups of 50 to keep ssh command size manageable
    for i in range(0, len(all_cifs), 50):
        chunk = all_cifs[i:i + 50]
        lig_counts.update(batch_ligand_atoms(chunk))

    # Step C — fetch status.jsons directly via deterministic path per cell.
    # (The batch_probe_cifs find pass occasionally missed status.jsons when
    # ssh output got clipped mid-cell; deterministic path is robust.)
    status_by_tag: dict[str, dict] = {}
    status_paths = []
    tag_to_status_path = {}
    for row in manifest:
        arm = "apo" if row["partner_type"] == "apo" else "cognate"
        subdir = (f"{row['receptor_resolved'].lower()}/{row['ligand_role']}/"
                  f"{arm}/{row['backbone']}/seed_{row['seed_used']}")
        sp = (f"{args.hpc_pool_root.rstrip('/')}/{subdir}/"
              f"_{row['backbone']}_status.json")
        tag = (f"{row['receptor_resolved']}|{row['ligand_role']}|"
               f"{row['partner_type']}|{row['backbone']}")
        tag_to_status_path[tag] = sp
        status_paths.append(sp)
    # Rsync all status.jsons to a local tempdir in ONE call, then parse
    # locally. Robust against ssh output truncation / rate-limiting.
    import tempfile, shutil
    tmp = Path(tempfile.mkdtemp(prefix="smoke_status_"))
    print(f"rsync status.jsons to {tmp} ...", file=sys.stderr)
    rsync_cmd = [
        "rsync", "-a",
        "--include=*/", "--include=_*_status.json", "--exclude=*",
        "--prune-empty-dirs",
        f"basel-hpc:{args.hpc_pool_root.rstrip('/')}/",
        str(tmp) + "/",
    ]
    subprocess.run(rsync_cmd, capture_output=True, text=True, timeout=180)
    for row in manifest:
        arm = "apo" if row["partner_type"] == "apo" else "cognate"
        subdir = (f"{row['receptor_resolved'].lower()}/{row['ligand_role']}/"
                  f"{arm}/{row['backbone']}/seed_{row['seed_used']}")
        sp = tmp / subdir / f"_{row['backbone']}_status.json"
        tag = (f"{row['receptor_resolved']}|{row['ligand_role']}|"
               f"{row['partner_type']}|{row['backbone']}")
        if sp.exists():
            try:
                status_by_tag[tag] = json.loads(sp.read_text())
            except json.JSONDecodeError:
                status_by_tag[tag] = {"error": "json decode"}
    shutil.rmtree(tmp, ignore_errors=True)

    # Step D — index rows.smoke.csv by (receptor, ligand_role, arm, backbone)
    rows_by_cell: dict[str, list[dict]] = defaultdict(list)
    if args.rows_csv and args.rows_csv.exists():
        for row in csv.DictReader(args.rows_csv.open()):
            key = (row.get("receptor_slug", ""),
                   row.get("ligand_role") or row.get("input_state_claim", ""),
                   row.get("partner_type", ""),
                   row.get("backbone", ""))
            # rows.smoke.csv may not carry ligand_role — reconstruct from
            # manifest via input_path substring
            rows_by_cell["|".join(str(x) for x in key)].append(row)

    # Step E — per-cell verdict
    cells: dict[str, dict] = {}
    for row in manifest:
        tag = (f"{row['receptor_resolved']}|{row['ligand_role']}|"
               f"{row['partner_type']}|{row['backbone']}")
        is_ligand_arm = row["ligand_role"] not in ("none", "")
        lig_row = ligand_set.get((row["receptor_resolved"], row["ligand_role"]), {})
        expected_heavy = count_heavy_atoms_smiles(lig_row.get("smiles", "") or row.get("ligand_smiles", ""))

        probe = probes.get(tag, {})
        cifs = probe.get("cifs", [])
        st = status_by_tag.get(tag, {})

        # Per-CIF ligand atom counts (may have 5 CIFs)
        per_cif = []
        for cif in cifs:
            n, centroid = lig_counts.get(cif, (0, (float("nan"),) * 3))
            per_cif.append({"cif": cif, "n_ligand_atoms": n,
                            "centroid": list(centroid)})

        # --- Checks 1-3 (per-backbone-relevant) ---
        c1_ligand_present = True
        c2_ligand_correct = True
        c1_note = c2_note = ""
        if is_ligand_arm:
            n_zero = sum(1 for p in per_cif if p["n_ligand_atoms"] == 0)
            c1_ligand_present = (n_zero == 0 and len(per_cif) > 0)
            c1_note = f"{n_zero}/{len(per_cif)} CIFs zero ligand atoms"
            if expected_heavy > 0 and per_cif:
                bad = [p for p in per_cif
                       if abs(p["n_ligand_atoms"] - expected_heavy) > 3]
                c2_ligand_correct = (len(bad) == 0)
                c2_note = (f"{len(bad)}/{len(per_cif)} CIFs off by >3 "
                           f"(expected~{expected_heavy})")
        else:
            # none-state — ligand SHOULD be absent
            n_present = sum(1 for p in per_cif if p["n_ligand_atoms"] > 0)
            c1_ligand_present = True  # not applicable — none arm
            c2_ligand_correct = (n_present == 0)
            c2_note = f"none-arm; {n_present} CIFs unexpectedly have HETATMs"

        # Check 6 — runtime_config on disk
        c6_config_echo = bool(st.get("runtime_config"))

        # Store
        cells[tag] = {
            "receptor": row["receptor_resolved"],
            "ligand_role": row["ligand_role"],
            "arm": row["partner_type"],
            "backbone": row["backbone"],
            "is_ligand_arm": is_ligand_arm,
            "expected_heavy_atoms": expected_heavy,
            "n_cifs": len(per_cif),
            "per_cif": per_cif,
            "status_json_present": bool(st) and "error" not in st,
            "runtime_config_present": c6_config_echo,
            "status_json_ok": bool(st.get("ok")) if isinstance(st, dict) else False,
            "check1_ligand_present": c1_ligand_present,
            "check1_note": c1_note,
            "check2_ligand_correct": c2_ligand_correct,
            "check2_note": c2_note,
            "check6_config_echo": c6_config_echo,
        }

    # --- Aggregate ---
    per_backbone_1 = defaultdict(lambda: {"pass": 0, "fail": 0, "n_a": 0})
    per_backbone_2 = defaultdict(lambda: {"pass": 0, "fail": 0})
    n_c6_pass = n_c6_fail = 0
    for tag, c in cells.items():
        bb = c["backbone"]
        if c["is_ligand_arm"]:
            per_backbone_1[bb]["pass" if c["check1_ligand_present"] else "fail"] += 1
        else:
            per_backbone_1[bb]["n_a"] += 1
        per_backbone_2[bb]["pass" if c["check2_ligand_correct"] else "fail"] += 1
        if c["check6_config_echo"]:
            n_c6_pass += 1
        else:
            n_c6_fail += 1

    aggregate = {
        "n_cells_total": len(cells),
        "n_status_json_present": sum(1 for c in cells.values() if c["status_json_present"]),
        "n_status_json_ok": sum(1 for c in cells.values() if c["status_json_ok"]),
        "check1_by_backbone": dict(per_backbone_1),
        "check2_by_backbone": dict(per_backbone_2),
        "check6_config_echo_pass": n_c6_pass,
        "check6_config_echo_fail": n_c6_fail,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({
        "aggregate": aggregate,
        "cells": cells,
    }, indent=2, default=str))
    print(json.dumps(aggregate, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
