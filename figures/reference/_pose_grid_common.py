"""
Shared helpers for the four fig5 pose-grid variants.

Data-only utilities: find predicted CIFs, load atoms via gemmi, Kabsch-align
predicted pockets onto 2RH1, extract predicted ligand atoms and write them to
a per-cell temp CIF that a downstream renderer (PyMOL, Biotite, py3Dmol) can
open.  Handles the four backbones' ligand-naming quirks in one place.
"""
from __future__ import annotations

import glob
import tempfile
import warnings
from dataclasses import dataclass
from pathlib import Path

import gemmi
import numpy as np

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parents[1]
CIF_REF = REPO / "refs" / "cache" / "rcsb" / "pdb_2rh1.cif"
PROBE = REPO / "experiments" / "020_block_c_ligand_pharmacology" / "analysis" / "_probe_stage"
OUT = REPO / "artefacts" / "side_figures_2026_09_06"
OUT.mkdir(parents=True, exist_ok=True)

# BW-anchor pocket-defining positions on ADRB2 (uniprot / 2RH1 auth numbering)
POCKET_RESIDS = [113, 117, 118, 193, 199, 286, 289, 290, 293, 308, 312]

# ADRB2 ligands to compare (rows)
@dataclass
class Ligand:
    code: str
    name: str
    smiles: str
    class_note: str


LIGANDS: list[Ligand] = [
    Ligand("ip", "R-isoproterenol",
           "CC(C)[NH2+]C[C@@H](O)c1ccc(O)c(O)c1",
           "beta-adrenergic full agonist"),
    Ligand("pp", "S-propranolol",
           "CC(C)[NH2+]C[C@H](O)COc1cccc2ccccc12",
           "beta-antagonist"),
    Ligand("dp", "dopamine",
           "[NH3+]CCc1ccc(O)c(O)c1",
           "wrong receptor (D-family)"),
    Ligand("hs", "histamine",
           "[NH3+]CCc1c[nH]cn1",
           "wrong receptor (H-family)"),
    Ligand("hp", "haloperidol",
           "O=C(c1ccc(F)cc1)CCC[NH+]2CCC(O)(c3ccc(Cl)cc3)CC2",
           "wrong receptor (D2 antagonist)"),
]

BACKBONES = ["of3", "boltz", "chai", "protenix"]
BACKBONE_LABEL = {
    "of3": "OpenFold3",
    "boltz": "Boltz-1",
    "chai": "Chai-1",
    "protenix": "Protenix",
}


def find_pred_cif(code: str, backbone: str) -> str | None:
    base = PROBE / backbone / code
    matches: list[str] = []
    if backbone == "boltz":
        matches = glob.glob(str(base / f"boltz_results_{code}_boltz" /
                                 "predictions" / f"{code}_boltz" /
                                 f"{code}_boltz_model_0.cif"))
    elif backbone == "chai":
        matches = glob.glob(str(base / "pred.model_idx_0.cif"))
    elif backbone == "of3":
        matches = glob.glob(str(base / f"gate02_{code}_of3" / "seed_*" /
                                 f"gate02_{code}_of3_seed_*_sample_1_model.cif"))
    elif backbone == "protenix":
        matches = glob.glob(str(base / f"gate02_{code}_protenix" / "seed_*" /
                                 "predictions" / f"gate02_{code}_protenix_sample_0.cif"))
    return matches[0] if matches else None


# ---------- geometry ----------
def kabsch(m: np.ndarray, t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ca, cb = m.mean(0), t.mean(0)
    H = (m - ca).T @ (t - cb)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    R = Vt.T @ np.diag([1, 1, d]) @ U.T
    T = cb - ca @ R.T
    return R, T


def _pocket_ca_from_struct(st: gemmi.Structure, resids: list[int]) -> tuple[np.ndarray, np.ndarray]:
    m = st[0]
    xs, ids = [], []
    for ch in m:
        if ch.name != "A":
            continue
        for res in ch:
            if res.seqid.num in resids:
                for a in res:
                    if a.name.strip() == "CA":
                        xs.append([a.pos.x, a.pos.y, a.pos.z])
                        ids.append(res.seqid.num)
                        break
    return np.asarray(xs), np.asarray(ids)


def align_pred_onto_ref(pred_path: str, ref_path: str = str(CIF_REF),
                        resids: list[int] = POCKET_RESIDS) -> tuple[gemmi.Structure, float]:
    """Return (aligned-pred-Structure, pocket-Cα-RMSD-after-alignment).
    The returned Structure is mutated in-place with the Kabsch RT."""
    pred = gemmi.read_structure(pred_path)
    ref = gemmi.read_structure(ref_path)
    pred_ca, pred_ids = _pocket_ca_from_struct(pred, resids)
    ref_ca, ref_ids = _pocket_ca_from_struct(ref, resids)
    common = np.intersect1d(pred_ids, ref_ids)
    if len(common) < 4:
        return pred, float("nan")
    A = pred_ca[np.isin(pred_ids, common)]
    B = ref_ca[np.isin(ref_ids, common)]
    R, T = kabsch(A, B)
    # apply to every atom in `pred`
    for model in pred:
        for ch in model:
            for res in ch:
                for a in res:
                    v = np.array([a.pos.x, a.pos.y, a.pos.z])
                    w = v @ R.T + T
                    a.pos = gemmi.Position(*w)
    A_al = A @ R.T + T
    rmsd = float(np.sqrt(((A_al - B) ** 2).sum(axis=1).mean()))
    return pred, rmsd


def write_aligned_pred(pred_path: str, out_path: str,
                       ref_path: str = str(CIF_REF)) -> float:
    """Write aligned predicted CIF to `out_path`. Return pocket-Cα RMSD."""
    aligned, rmsd = align_pred_onto_ref(pred_path, ref_path)
    aligned.make_mmcif_document().write_file(out_path)
    return rmsd


def receptor_and_ligand_chains(pred_path: str) -> tuple[str, str, str]:
    """Return (receptor-chain, ligand-chain, ligand-resname) for a predicted CIF.
    Convention: receptor is always chain A; ligand is any non-protein residue on
    a different chain."""
    protein_res = {"ALA", "ARG", "ASN", "ASP", "CYS", "GLN", "GLU", "GLY",
                   "HIS", "ILE", "LEU", "LYS", "MET", "PHE", "PRO", "SER",
                   "THR", "TRP", "TYR", "VAL"}
    st = gemmi.read_structure(pred_path)
    for ch in st[0]:
        if ch.name == "A":
            continue
        for r in ch:
            if r.name not in protein_res:
                return "A", ch.name, r.name
    return "A", "", ""


def reference_ligand_info(ref_path: str = str(CIF_REF)) -> tuple[str, str]:
    return "A", "CAU"   # 2RH1 carazolol lives on chain A as CAU
