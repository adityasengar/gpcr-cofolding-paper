"""Build Block C property-matched decoy ligands for Gate 0.4 (Tier 1 + Tier 3).

Tier 1 (8 Class A small-mol receptors, ligand_set.csv):
  - 8 receptors get their `decoy_lig` row filled in `refs/ligand_set.csv`
    (GLP1R Tier 1 peptide decoy was dropped upstream; legacy handling
    remains gated on presence in the CSV).

Tier 3 (28 additional Class A receptors, ligand_set_tier3.csv):
  - 26 small-mol decoys (verify-only; not written to any refs/ CSV)
  - 2 scrambled-peptide decoys (APJ, GHSR — peptide-only agonists,
    antag=NA in tier3.csv)
  - 4 NA receptors documented as intentional (B1B1U5, OPSD, FSHR, LSHR)

For each decoy the script computes:
  - RDKit canonical SMILES + InChI + property axes (MW, logP, HBD, HBA,
    rot, formal charge)
  - Morgan (r=2, 1024 bit) Tanimoto vs every real (non-peptide) ligand
    for that receptor. Hard gate: Tanimoto < 0.30.
  - Property tolerance (±20 % of receptor real-ligand mean per axis).
    Formal-charge mismatch is reported not raised (Decision A —
    aminergic +1 anchors force neutral decoys).

Peptide decoys (scrambled-native pattern):
  - composition-preserved permutation of the native agonist sequence
  - deterministic seed = SHA-256(receptor|salt|variant)
  - MIN_HAMMING = max(8, round(0.65 * len(sequence)))
  - Tier 1 GLP1R salt = "block_c_decoy_lig_v1" (legacy)
  - Tier 3 APJ / GHSR salt = "block_c_tier3_decoy_lig_v1"

Byte-level discipline:
  - non-decoy rows of `refs/ligand_set.csv` are preserved byte-for-byte
    (raw-line pass-through + SHA-256 pre/post check)
  - Tier 3 CSV (`refs/ligand_set_tier3.csv`) is READ-ONLY
  - deterministic: fixed random seed, RDKit canonical SMILES, seeded
    scramble, idempotent — a second run of this script produces
    byte-identical outputs
  - two-run self-check (--selfcheck) diffs bytes against a temp-dir
    replay for BOTH the Tier 1 verification MD and the Tier 3 notes MD

Deliverables:
  * refs/ligand_set.csv                       (Tier 1 decoy_lig rows filled;
                                               8 receptors only after GLP1R drop)
  * experiments/020_block_c_ligand_pharmacology/analysis/decoy_verification.md
  * experiments/021_block_c_tier3_pharmacology/curation/S3_decoy_construction_notes.md
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import random
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path

from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import Crippen, Descriptors, Lipinski
from rdkit.Chem.rdFingerprintGenerator import GetMorganGenerator

RDLogger.DisableLog("rdApp.*")

REPO = Path(__file__).resolve().parent.parent
LIGAND_SET_CSV = REPO / "refs" / "ligand_set.csv"
LIGAND_SET_TIER3_CSV = REPO / "refs" / "ligand_set_tier3.csv"
VERIFICATION_MD = (
    REPO
    / "experiments"
    / "020_block_c_ligand_pharmacology"
    / "analysis"
    / "decoy_verification.md"
)
TIER3_NOTES_MD = (
    REPO
    / "experiments"
    / "021_block_c_tier3_pharmacology"
    / "curation"
    / "S3_decoy_construction_notes.md"
)

# ---- Decoy candidates (one primary per receptor; source cited in MD) ------
#
# Two receptor buckets:
#   - Tier 1 (8 slugs): decoys are WRITTEN into refs/ligand_set.csv
#   - Tier 3 (26 slugs): decoys are VERIFY-ONLY, sourced from
#     refs/ligand_set_tier3.csv, emitted into S3_decoy_construction_notes.md
#
# A receptor's bucket is determined by which CSV its real-ligand rows live
# in. The script auto-detects (Tier 1 receptors present in ligand_set.csv,
# Tier 3 present in ligand_set_tier3.csv). Both dicts are merged into one
# `DECOY_SMILES` per the task contract.

DECOY_SMILES: dict[str, tuple[str, str, str]] = {
    # ---- Tier 1 (8, unchanged from 2026-09-03 landing) ------------------
    # receptor:   (canonical-ish SMILES, iupac/common name, source string)
    "ADRB2": (
        "CN(C)C[C@@H]1CCCC[C@@]1(O)c1cccc(OC)c1",
        "tramadol",
        "FDA-approved analgesic (μ-opioid + SNRI); no known β-adrenergic activity",
    ),
    "DRD3": (
        "Cc1cccc(C)c1Nc1ccccc1C(=O)O",
        "mefenamic acid",
        "FDA-approved NSAID (COX-1/2); no dopaminergic activity",
    ),
    "AA2AR": (
        "Cc1cc(Cc2cnc(N)nc2N)cc(OC)c1OC",
        "trimethoprim",
        "FDA-approved DHFR-inhibitor antibiotic; no adenosinergic activity",
    ),
    "ACM4": (
        "CNC(=N/C#N)/NCCSCc1ccc(CN(C)C)o1",
        "ranitidine",
        "FDA-approved H2-antihistamine; selective, no muscarinic activity",
    ),
    "OX2R": (
        "COc1ccc(CC(C)(C#N)CCCN(C)CCc2ccc(OC)c(OC)c2)cc1",
        "verapamil",
        "FDA-approved L-type Ca²⁺ channel blocker; no orexin activity",
    ),
    "ACM2": (
        "Cc1[nH]cnc1CSCC/N=C(\\NC)NC#N",
        "cimetidine",
        "FDA-approved H2-antihistamine; no muscarinic activity",
    ),
    "5HT1B": (
        "NS(=O)(=O)c1cc(C(=O)O)c(NCc2ccco2)cc1Cl",
        "furosemide",
        "FDA-approved loop diuretic (NKCC2 inhibitor); no 5-HT activity",
    ),
    "AA1R": (
        "COC(=O)C1=C(C)NC(C)=C(C(=O)OC)C1c1ccccc1[N+](=O)[O-]",
        "nifedipine",
        "FDA-approved L-type Ca²⁺ channel blocker (dihydropyridine); no adenosinergic activity",
    ),
    # ---- Tier 3 (26 new, Block C Tier 3 Stage 3 2026-09-04) -------------
    # Approvals: FDA / EMA / DEA schedule status per PubChem/DrugBank.
    # "No known binding" claim rests on receptor-family paralog literature
    # (see S3_decoy_construction_notes.md for the per-decoy IUPHAR /
    # PubChem BindingDB annotation review). Coordinator-approved uncertainty
    # flags recorded in that same MD.
    "5HT2C": (
        "CC(C)c1cccc(C(C)C)c1O",
        "propofol",
        "FDA-approved iv anesthetic (Diprivan, 1989); GABA-A PAM primary target; no 5-HT-family activity",
    ),
    "5HT5A": (
        "Cc1cc(NS(=O)(=O)c2ccc(N)cc2)no1",
        "sulfamethoxazole",
        "FDA-approved sulfonamide antibacterial (bacterial DHPS inhibitor); no 5-HT-family activity",
    ),
    "ACM1": (
        "CCCCNC(=O)NS(=O)(=O)c1ccc(C)cc1",
        "tolbutamide",
        "FDA-approved first-generation sulfonylurea antidiabetic (K-ATP channel closure); no muscarinic activity",
    ),
    "ADA2A": (
        "COc1ccccc1OCC(O)CO",
        "guaifenesin",
        "FDA-approved expectorant (Mucinex); no adrenergic-receptor family activity",
    ),
    "ADRB1": (
        "CC(=O)Oc1ccccc1C(=O)O",
        "aspirin",
        "FDA-approved NSAID (irreversible COX-1/2 acetylation); no adrenergic activity",
    ),
    "AGTR1": (
        "Oc1ccc(cc1)[C@@H]1[C@H](CC[C@H](O)c2ccc(F)cc2)C(=O)N1c1ccc(F)cc1",
        "ezetimibe",
        "FDA-approved cholesterol-absorption inhibitor (NPC1L1); no angiotensin-family activity",
    ),
    "CCKAR": (
        "CN(C)C(=O)C(CCN1CCC(O)(c2ccc(Cl)cc2)CC1)(c1ccccc1)c1ccccc1",
        "loperamide",
        "FDA-approved antidiarrheal (gut-restricted μ-opioid agonist); no CCK-family activity",
    ),
    "CCR5": (
        "Cc1ccc(NC(=O)c2ccc(CN3CCN(C)CC3)cc2)cc1Nc1nccc(-c2cccnc2)n1",
        "imatinib",
        "FDA-approved BCR-Abl / c-Kit / PDGFR tyrosine-kinase inhibitor (Gleevec); no CCR-family activity",
    ),
    "CNR1": (
        "CC(C)(C)C(=O)O[C@@H]1C[C@H](C)C=C2C=C[C@@H](C)[C@H](CC[C@@H]3C[C@H](O)CC(=O)O3)[C@@H]12",
        "simvastatin",
        "FDA-approved HMG-CoA reductase inhibitor (Zocor); no cannabinoid-receptor activity",
    ),
    "CNR2": (
        "CC[C@H](C)C(=O)O[C@@H]1C[C@H](C)C=C2C=C[C@@H](C)[C@H](CC[C@@H]3C[C@H](O)CC(=O)O3)[C@H]21",
        "lovastatin",
        "FDA-approved HMG-CoA reductase inhibitor (Mevacor); no cannabinoid-receptor activity",
    ),
    "CXCR2": (
        "CCC1=C(C)C(=O)N(CCC(=O)NCCc2ccc(S(=O)(=O)NC(=O)NC3CCC(C)CC3)cc2)C1",
        "glimepiride",
        "FDA-approved third-generation sulfonylurea antidiabetic (Amaryl); no CXC-chemokine activity",
    ),
    "CXCR4": (
        "CCN(CC)CCCC(C)Nc1c2ccc(Cl)cc2nc2cc(OC)ccc12",
        "quinacrine",
        "FDA-approved acridine antimalarial (mechanism: DNA intercalation, prostaglandin inhibition); no CXC-chemokine activity",
    ),
    "DRD2": (
        "Cc1ncc(C[S](=O)c2nc3cc(OC)ccc3[nH]2)c(OC)c1C",
        "omeprazole",
        "FDA-approved proton-pump inhibitor (H+/K+-ATPase covalent inhibitor, Prilosec); no dopaminergic activity",
    ),
    "EDNRA": (
        "CC(C)OC(=O)C(C)(C)Oc1ccc(C(=O)c2ccc(Cl)cc2)cc1",
        "fenofibrate",
        "FDA-approved PPAR-α agonist (Tricor, hypolipidemic fibrate); no endothelin-family activity",
    ),
    "EDNRB": (
        "CC(C)(C(=O)O)c1ccc(C(O)CCCN2CCC(C(O)(c3ccccc3)c3ccccc3)CC2)cc1",
        "fexofenadine",
        "FDA-approved second-generation H1 antihistamine (Allegra); no endothelin-family activity",
    ),
    "GRPR": (
        "CCCc1nc2c(=O)[nH]c(-c3cc(S(=O)(=O)N4CCN(C)CC4)ccc3OCC)nc2n1C",
        "sildenafil",
        "FDA-approved PDE5 inhibitor (Viagra); no bombesin/GRP-family activity",
    ),
    "HRH1": (
        "CN(C)C(=N)N=C(N)N",
        "metformin",
        "FDA-approved biguanide antidiabetic (AMPK activation); no histamine-receptor activity",
    ),
    "HRH3": (
        "CC(=O)O[C@@H]1[C@H](c2ccc(OC)cc2)Sc2ccccc2N(CCN(C)C)C1=O",
        "diltiazem",
        "FDA-approved benzothiazepine L-type Ca²⁺ channel blocker (Cardizem); no histamine-receptor activity",
    ),
    "LPAR1": (
        "CC(C)c1nc(N(C)S(=O)(=O)C)nc(-c2ccc(F)cc2)c1/C=C/[C@@H](O)C[C@@H](O)CC(=O)O",
        "rosuvastatin",
        "FDA-approved HMG-CoA reductase inhibitor (Crestor); no lysophospholipid-receptor activity",
    ),
    "LT4R1": (
        "CC(C)(CCCC(C)Oc1ccc(C)cc1C)C(=O)O",
        "gemfibrozil",
        "FDA-approved fibrate hypolipidemic (Lopid, PPAR-α agonist); no leukotriene-receptor activity",
    ),
    "MCHR1": (
        "CC/C(=C(/c1ccccc1)c1ccc(OCCN(C)C)cc1)c1ccccc1",
        "tamoxifen",
        "FDA-approved selective estrogen receptor modulator (SERM); no MCH-family activity",
    ),
    "NPY1R": (
        "CC(C)(C)NC(=O)[C@@H]1C[C@@H]2CCCC[C@@H]2CN1C[C@@H](O)[C@H](Cc1ccccc1)NC(=O)[C@@H](CC(N)=O)NC(=O)c1cc2ccccc2cn1",
        "saquinavir",
        "FDA-approved HIV-1 protease inhibitor (Invirase); no neuropeptide-Y-family activity",
    ),
    "NPY2R": (
        "Cc1cn(-c2cc(NC(=O)c3ccc(C)c(Nc4nccc(-c5cccnc5)n4)c3)cc(C(F)(F)F)c2)cn1",
        "nilotinib",
        "FDA-approved BCR-Abl tyrosine-kinase inhibitor (Tasigna); no neuropeptide-Y-family activity",
    ),
    "OPRD": (
        "CCOC(=O)N1CCC(=C2c3ccc(Cl)cc3CCc3cccnc32)CC1",
        "loratadine",
        "FDA-approved second-generation H1 antihistamine (Claritin); no opioid-receptor activity at therapeutic doses",
    ),
    "OPRK": (
        "Clc1ccc2c(c1)CCc1cnccc1/C2=C1\\CCNCC1",
        "desloratadine",
        "FDA-approved active metabolite of loratadine (Clarinex, H1 antihistamine); no opioid-receptor activity at therapeutic doses",
    ),
    "OPRX": (
        "C[C@H](Cc1cccc(C(F)(F)F)c1)NCCCc1cccc2ccccc12",
        "cinacalcet",
        "FDA-approved calcimimetic (calcium-sensing receptor PAM, Sensipar); no opioid-receptor activity",
    ),
}

# ---- Peptide decoys ------------------------------------------------------
#
# receptor: (native_sequence, common_name, salt_variant)
#
# Peptide decoys use a composition-preserved scramble of the native
# agonist sequence with:
#   - deterministic seed = SHA-256(receptor|salt|variant)
#   - MIN_HAMMING = max(8, round(0.65 * len(sequence)))
#
# GLP1R is Tier 1 legacy (kept for byte-preserving replay if it's ever
# restored to ligand_set.csv). It was dropped at Step 1.5 (2026-09-02); the
# entry is guarded by presence-in-CSV at build time.

PEPTIDE_DECOYS: dict[str, tuple[str, str, str]] = {
    "GLP1R": (
        "HAEGTFTSDVSSYLEGQAAKEFIAWLVKGRG",
        "GLP-1(7-36)",
        "block_c_decoy_lig_v1",
    ),
    "APJ": (
        "QRPRLSHKGPMPF",
        "apelin-13",
        "block_c_tier3_decoy_lig_v1",
    ),
    "GHSR": (
        "GSSFLSPEHQRVQQRKESKKPPAKLQPR",
        "ghrelin-28",
        "block_c_tier3_decoy_lig_v1",
    ),
}

# GLP1R Tier 1 legacy alias — kept for backwards compatibility with the
# original build_glp1r_peptide_decoy_row() naming.
GLP1_NATIVE = PEPTIDE_DECOYS["GLP1R"][0]
SCRAMBLE_SALT = PEPTIDE_DECOYS["GLP1R"][2]

# ---- Tier 3 NA receptors (documented as intentional NA in notes.md) ------

TIER3_NA_RECEPTORS: dict[str, str] = {
    "B1B1U5": (
        "Jumping-spider rhodopsin (JSR1/Kumopsin1). Dark-state ligand is "
        "9-cis retinal covalently bound to conserved opsin Lys via Schiff "
        "base — pharmacologically an inverse agonist (dropped from Tier 3 "
        "per amendment §C-1). Photoactivated agonist all-trans retinal is "
        "also covalent. No diffusible small-molecule or peptide decoy "
        "paradigm applicable."
    ),
    "OPSD": (
        "Bovine/human rhodopsin. Same covalent-retinal Schiff-base "
        "paradigm as B1B1U5. Dark-state 11-cis retinal is inverse "
        "agonist (dropped per §C-1). No competitive diffusible ligand "
        "paradigm; no decoy applicable."
    ),
    "FSHR": (
        "Follicle-stimulating hormone receptor. Endogenous agonist FSH is "
        "a heterodimeric N-glycosylated glycoprotein hormone (α-CGA + "
        "β-FSHB). No cleanly-classified small-molecule antagonist or "
        "agonist with high-affinity co-crystal in RCSB; concatenating "
        "α:seq;β:seq would silently mis-fold in all 4 backbones and "
        "poison analysis. Ligand-identity paradigm not applicable at "
        "either the small-molecule or peptide layer."
    ),
    "LSHR": (
        "Luteinising-hormone / choriogonadotropin receptor. Endogenous "
        "agonists LH and hCG are heterodimeric N-glycosylated glycoprotein "
        "hormones (α-CGA + β-LHB/CGB). Same heterodimer + no small-mol "
        "high-affinity crystal reasoning as FSHR. No decoy applicable."
    ),
}

MAX_SEED_RETRIES = 256


def min_hamming_for(sequence: str) -> int:
    """Per-peptide Hamming floor: 65% of length, minimum 8."""
    return max(8, round(len(sequence) * 0.65))


# Backwards-compat alias (Tier 1 legacy — 31-mer GLP-1(7-36) → 20)
MIN_HAMMING = min_hamming_for(GLP1_NATIVE)

# Per-property tolerance (fraction of mean).
PROPERTY_TOLERANCE = 0.20

# Property axes we report on.
PROPERTY_AXES = ("mw", "logp", "hbd", "hba", "rot", "charge")

# Tanimoto cutoff (topological dissimilarity floor).
TANIMOTO_MAX = 0.30

MORGAN = GetMorganGenerator(radius=2, fpSize=1024)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _rel_to_repo(p: Path) -> str:
    """Return path relative to REPO if under it; else the absolute path."""
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(p)


def sha256_hex(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def seed_from(receptor_slug: str, salt: str, variant: int = 0) -> int:
    composite = f"{receptor_slug}|{salt}|{variant}".encode("utf-8")
    return int.from_bytes(hashlib.sha256(composite).digest()[:8], "big") & (
        (1 << 63) - 1
    )


def hamming(a: str, b: str) -> int:
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} != {len(b)}")
    return sum(1 for x, y in zip(a, b) if x != y)


def compute_props(smiles: str) -> dict | None:
    """Return property dict, or None on parse failure."""
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    canon = Chem.MolToSmiles(mol, canonical=True)
    inchi = Chem.MolToInchi(mol)
    return {
        "canonical_smiles": canon,
        "inchi": inchi,
        "mw": round(Descriptors.MolWt(mol), 3),
        "logp": round(Crippen.MolLogP(mol), 3),
        "hbd": int(Lipinski.NumHDonors(mol)),
        "hba": int(Lipinski.NumHAcceptors(mol)),
        "rot": int(Lipinski.NumRotatableBonds(mol)),
        "charge": int(Chem.GetFormalCharge(mol)),
        "hac": int(mol.GetNumHeavyAtoms()),
        "atom_counter": dict(Counter(a.GetSymbol() for a in mol.GetAtoms())),
        "canonical_sha256": sha256_hex(canon),
    }


def morgan_fp(smiles: str):
    m = Chem.MolFromSmiles(smiles)
    if m is None:
        return None
    return MORGAN.GetFingerprint(m)


def tanimoto(smi_a: str, smi_b: str) -> float | None:
    fa = morgan_fp(smi_a)
    fb = morgan_fp(smi_b)
    if fa is None or fb is None:
        return None
    return DataStructs.TanimotoSimilarity(fa, fb)


def within_tolerance(decoy_val: float, mean_val: float, tol: float) -> bool:
    """Within ±tol × |mean| of mean. Guard on zero mean."""
    if mean_val == 0:
        return decoy_val == 0
    return abs(decoy_val - mean_val) <= tol * abs(mean_val)


# ---------------------------------------------------------------------------
# CSV row model
# ---------------------------------------------------------------------------

CSV_HEADER = [
    "receptor",
    "ligand_role",
    "ligand_variant",
    "is_peptide",
    "smiles",
    "inchi",
    "peptide_sequence",
    "iupac_name",
    "bound_pdb",
    "affinity_metric",
    "affinity_value_nM",
    "affinity_source",
    "activity_class",
    "pdb_deposition_date",
    "tautomer_note",
    "protonation_ph74_note",
    "notes",
]


def read_ligand_set_lines(path: Path) -> list[str]:
    """Return raw lines preserving newlines (line-by-line pass-through)."""
    with open(path, "r", newline="", encoding="utf-8") as fh:
        return fh.read().splitlines(keepends=True)


def parse_row_key(line: str) -> tuple[str, str] | None:
    """Return (receptor, ligand_role) for a data line, or None for header."""
    r = next(csv.reader(io.StringIO(line)))
    if not r or r[0] == "receptor":
        return None
    return (r[0], r[1] if len(r) > 1 else "")


def parse_row_dict(line: str) -> dict[str, str]:
    r = next(csv.reader(io.StringIO(line)))
    # Pad to CSV_HEADER length.
    while len(r) < len(CSV_HEADER):
        r.append("")
    return dict(zip(CSV_HEADER, r))


def format_csv_row(row: dict[str, str]) -> str:
    """Emit one CSV row using csv.writer (QUOTE_MINIMAL) + LF newline."""
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)
    w.writerow([row.get(k, "") for k in CSV_HEADER])
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Peptide scramble (Block B pattern)
# ---------------------------------------------------------------------------


def scramble_peptide(
    sequence: str,
    receptor_slug: str,
    salt: str = SCRAMBLE_SALT,
    min_hamming: int | None = None,
) -> tuple[str, int, int]:
    """Return (scrambled, seed_used, variant_used).

    Composition-preserved shuffle; Hamming ≥ `min_hamming` (defaults to
    max(8, round(0.65 * len(sequence)))). Salt is per-peptide — Tier 1
    GLP1R uses `block_c_decoy_lig_v1`, Tier 3 APJ/GHSR use
    `block_c_tier3_decoy_lig_v1` (SCRAMBLE_SALT is only the Tier-1 default).
    """
    if min_hamming is None:
        min_hamming = min_hamming_for(sequence)
    original = list(sequence)
    for variant in range(MAX_SEED_RETRIES):
        seed = seed_from(receptor_slug, salt, variant)
        rng = random.Random(seed)
        letters = list(original)
        rng.shuffle(letters)
        scrambled = "".join(letters)
        if scrambled == sequence:
            continue
        if hamming(scrambled, sequence) >= min_hamming:
            if Counter(scrambled) != Counter(sequence):
                raise AssertionError(
                    "composition drift — permutation must preserve counts"
                )
            return scrambled, seed, variant
    raise RuntimeError(
        f"could not achieve MIN_HAMMING={min_hamming} scramble for "
        f"{receptor_slug} within {MAX_SEED_RETRIES} tries"
    )


# ---------------------------------------------------------------------------
# Real-ligand harvest
# ---------------------------------------------------------------------------

REAL_ROLES = {"full_agonist", "neutral_antagonist", "inverse_agonist"}


def harvest_real_ligands(
    *line_lists: list[str],
    origin_tags: tuple[str, ...] | None = None,
) -> dict[str, list[dict]]:
    """Return {receptor: [ {name, smiles, activity_class, is_peptide,
    peptide_sequence, props_or_None, origin} ]}.

    Accepts multiple line-lists (Tier 1 + Tier 3 CSVs). Each real-ligand
    row is tagged with its origin (`origin_tags[i]` if given, else the
    positional index as a string). Receptor slugs are namespaced only
    implicitly — if a slug appears in both CSVs, the merged list carries
    both.
    """
    if origin_tags is None:
        origin_tags = tuple(str(i) for i in range(len(line_lists)))
    if len(origin_tags) != len(line_lists):
        raise ValueError(
            f"origin_tags length {len(origin_tags)} != line_lists count "
            f"{len(line_lists)}"
        )
    out: dict[str, list[dict]] = {}
    for tag, lines in zip(origin_tags, line_lists):
        for line in lines[1:]:
            if not line.strip():
                continue
            row = parse_row_dict(line)
            activity = row["activity_class"]
            if activity not in REAL_ROLES:
                continue
            receptor = row["receptor"]
            name = row["iupac_name"] or activity
            smi = row["smiles"].strip()
            peptide_seq = row["peptide_sequence"].strip()
            is_peptide = row["is_peptide"].strip().upper() == "TRUE"
            entry = {
                "receptor": receptor,
                "activity_class": activity,
                "name": name,
                "smiles": smi,
                "is_peptide": is_peptide,
                "peptide_sequence": peptide_seq,
                "props": None,
                "parse_error": None,
                "origin": tag,
            }
            if not is_peptide and smi:
                props = compute_props(smi)
                if props is None:
                    entry["parse_error"] = "RDKit failed to parse SMILES"
                else:
                    entry["props"] = props
            out.setdefault(receptor, []).append(entry)
    return out


def mean_and_sigma(vals: list[float]) -> tuple[float, float]:
    if not vals:
        return (float("nan"), float("nan"))
    mean = sum(vals) / len(vals)
    if len(vals) < 2:
        return (mean, 0.0)
    var = sum((v - mean) ** 2 for v in vals) / (len(vals) - 1)
    return (mean, var**0.5)


def per_receptor_property_window(real: list[dict]) -> dict[str, tuple[float, float]]:
    """Return {axis: (mean, sigma)} across parseable real-ligand rows only."""
    parseable = [r for r in real if r["props"] is not None]
    window: dict[str, tuple[float, float]] = {}
    for axis in PROPERTY_AXES:
        vals = [float(r["props"][axis]) for r in parseable]
        window[axis] = mean_and_sigma(vals)
    return window


# ---------------------------------------------------------------------------
# Decoy row builders
# ---------------------------------------------------------------------------


def build_small_mol_decoy_row(
    receptor: str,
    decoy_smiles: str,
    decoy_name: str,
    decoy_source: str,
    props: dict,
    real_ligands: list[dict],
    charge_missmatched: bool,
) -> dict[str, str]:
    """Compose the ligand_set.csv row for a small-molecule decoy."""
    real_parseable = [r for r in real_ligands if r["props"] is not None]
    n_real = len(real_parseable)
    tanimoto_summary = "; ".join(
        f"T({r['name']})={tanimoto(decoy_smiles, r['smiles']):.3f}"
        for r in real_parseable
    )
    notes_parts = [
        f"Block C decoy_lig built by scripts/build_block_c_decoys.py (Gate 0.4)",
        f"source: {decoy_source}",
        f"Morgan(r=2,1024)_max_Tanimoto_vs_real_ligands<0.3 (n={n_real} parseable): {tanimoto_summary}",
        f"canonical_smiles_sha256={props['canonical_sha256']}",
    ]
    if charge_missmatched:
        notes_parts.append("formal_charge_missmatched=true")
    notes = "; ".join(notes_parts)
    return {
        "receptor": receptor,
        "ligand_role": "decoy_lig",
        "ligand_variant": "",
        "is_peptide": "FALSE",
        "smiles": props["canonical_smiles"],
        "inchi": props["inchi"],
        "peptide_sequence": "",
        "iupac_name": decoy_name,
        "bound_pdb": "",
        "affinity_metric": "",
        "affinity_value_nM": "",
        "affinity_source": "decoy_none_known",
        "activity_class": "decoy_lig",
        "pdb_deposition_date": "",
        "tautomer_note": "",
        "protonation_ph74_note": "",
        "notes": notes,
    }


def build_peptide_decoy_row(
    receptor: str,
    native_seq: str,
    common_name: str,
    salt: str,
    scrambled: str,
    seed_used: int,
    h_dist: int,
    min_hamming: int,
) -> dict[str, str]:
    """Generalised peptide-decoy CSV row builder (GLP1R + APJ + GHSR)."""
    peptide_sha = sha256_hex(scrambled)
    notes = "; ".join(
        [
            "Block C decoy_lig built by scripts/build_block_c_decoys.py (Gate 0.4)",
            f"property-matched PEPTIDE non-binder: composition-preserved scramble of native {common_name}",
            f"scramble_salt={salt}",
            f"scramble_seed={seed_used}",
            f"hamming_vs_native={h_dist}/{len(native_seq)} (floor={min_hamming})",
            f"peptide_sequence_sha256={peptide_sha}",
            "no receptor-binding motif preserved; deterministic per receptor slug + salt (Block B α5-CT pattern)",
        ]
    )
    return {
        "receptor": receptor,
        "ligand_role": "decoy_lig",
        "ligand_variant": "",
        "is_peptide": "TRUE",
        "smiles": "",
        "inchi": "",
        "peptide_sequence": scrambled,
        "iupac_name": f"{common_name} composition-preserved scramble [Block C decoy]",
        "bound_pdb": "",
        "affinity_metric": "",
        "affinity_value_nM": "",
        "affinity_source": "decoy_none_known",
        "activity_class": "decoy_lig",
        "pdb_deposition_date": "",
        "tautomer_note": "peptide backbone standard amide tautomers",
        "protonation_ph74_note": (
            "side chains at pH 7.4 match native peptide composition "
            "(E/D anionic, K/R cationic)"
        ),
        "notes": notes,
    }


# Backwards-compat alias — GLP1R-specific caller signature preserved
def build_glp1r_peptide_decoy_row(
    scrambled: str, seed_used: int, h_dist: int
) -> dict[str, str]:
    return build_peptide_decoy_row(
        receptor="GLP1R",
        native_seq=GLP1_NATIVE,
        common_name="GLP-1(7-36)",
        salt=SCRAMBLE_SALT,
        scrambled=scrambled,
        seed_used=seed_used,
        h_dist=h_dist,
        min_hamming=MIN_HAMMING,
    )


# ---------------------------------------------------------------------------
# CSV rewrite with byte-integrity check
# ---------------------------------------------------------------------------


def rewrite_ligand_set(
    lines: list[str],
    decoy_rows_by_key: dict[tuple[str, str], dict[str, str]],
) -> tuple[list[str], list[tuple[str, str, str]]]:
    """
    Return (new_lines, byte_diffs_on_non_decoy_rows).

    byte_diffs_on_non_decoy_rows is empty on success. Each entry is
    (key_repr, old_line, new_line). If any non-decoy row's bytes change,
    the caller aborts.
    """
    out: list[str] = []
    diffs: list[tuple[str, str, str]] = []
    for line in lines:
        key = parse_row_key(line)
        if key is None:
            # header line
            out.append(line)
            continue
        if key in decoy_rows_by_key:
            new_line = format_csv_row(decoy_rows_by_key[key])
            out.append(new_line)
        else:
            # NON-DECOY: pass through byte-for-byte
            out.append(line)
            # Byte-integrity check: re-format and compare. If our
            # format_csv_row is byte-identical to the pass-through, that
            # is a bonus discipline check but not required.
    return out, diffs


def verify_non_decoy_byte_integrity(
    original_lines: list[str],
    new_lines: list[str],
    decoy_keys: set[tuple[str, str]],
) -> list[str]:
    """Return list of receptor|role keys whose non-decoy line changed."""
    changed: list[str] = []
    if len(original_lines) != len(new_lines):
        raise RuntimeError(
            f"line count changed: {len(original_lines)} -> {len(new_lines)}"
        )
    for orig, new in zip(original_lines, new_lines):
        key = parse_row_key(orig)
        if key is None:
            if orig != new:
                changed.append("<HEADER>")
            continue
        if key in decoy_keys:
            # decoy row is expected to change
            continue
        if orig != new:
            changed.append("|".join(key))
    return changed


# ---------------------------------------------------------------------------
# Verification MD emitter
# ---------------------------------------------------------------------------


def _fmt_pct_delta(decoy_val: float, mean_val: float) -> str:
    if mean_val == 0:
        return "n/a"
    return f"{(decoy_val - mean_val) / mean_val * 100:+.1f}%"


def emit_verification_md(
    receptors_report: list[dict],
    glp1r_report: dict | None,
    parse_failures: list[tuple[str, str, str]],
    out_path: Path,
) -> None:
    lines: list[str] = []
    ap = lines.append

    ap("# Block C — decoy ligand verification (Gate 0.4)")
    ap("")
    ap(
        "Emitted by `scripts/build_block_c_decoys.py`. Deterministic; a second run "
        "of the script produces byte-identical outputs (canonical SMILES via "
        "`Chem.MolToSmiles(..., canonical=True)`, peptide scramble seeded from "
        f"`SHA-256('receptor|{SCRAMBLE_SALT}|variant')[:8]`, single fixed "
        "PROPERTY_TOLERANCE, no non-determinism)."
    )
    ap("")
    ap("## Method")
    ap("")
    ap(
        "For each of the 9 `decoy_lig` receptor rows in `refs/ligand_set.csv`:"
    )
    ap("")
    ap("1. Harvest real-ligand rows for the receptor (`activity_class` in "
       "`{full_agonist, neutral_antagonist, inverse_agonist}` with a non-empty "
       "SMILES or peptide_sequence).")
    ap("2. Compute RDKit properties on each real-ligand SMILES: MW "
       "(Descriptors.MolWt), logP (Crippen.MolLogP), HBD (Lipinski.NumHDonors), "
       "HBA (Lipinski.NumHAcceptors), rotatable bonds (Lipinski.NumRotatableBonds), "
       "formal charge (Chem.GetFormalCharge). Real ligands that fail RDKit "
       "canonicalisation are logged as parse failures and excluded from the "
       "property window (§ Parse failures below).")
    ap("3. Compute the per-axis mean (and σ) across the parseable real ligands "
       "for that receptor. This is the property target for the decoy.")
    ap(f"4. Score the receptor's committed decoy candidate on each axis "
       f"against ±{int(PROPERTY_TOLERANCE * 100)} % of the mean. Rows that miss "
       f"formal-charge match are flagged `formal_charge_missmatched=true` per "
       f"coordinator Decision A (2026-09-03) — aminergic receptors where the "
       f"topology + no-known-binding constraint forces a neutral decoy.")
    ap(f"5. Compute Morgan fingerprint (radius 2, 1024 bits) Tanimoto against "
       f"every parseable real ligand. Require Tanimoto < {TANIMOTO_MAX} for all "
       f"pairs. This is the topological-dissimilarity floor.")
    ap("6. Byte-level verification: SHA-256 of the canonical SMILES (small "
       "molecules) or the raw peptide sequence (GLP1R). Atom-composition "
       "Counter and heavy-atom count are diffed against the most-similar real "
       "ligand.")
    ap("")
    ap(
        "Live ChEMBL was not queried; the no-known-binding classification "
        "relies on published FDA-approved pharmacology and well-characterised "
        "off-target profiles of each decoy. Any post-hoc cross-reactivity "
        "finding for a specific (decoy, receptor) pair must go through "
        "re-selection via this same script (add a fallback candidate, rerun)."
    )
    ap("")

    ap("## Summary")
    ap("")
    ap(
        "| receptor | decoy | canonical SMILES SHA-256 (short) | max Tanimoto vs real "
        "ligands | axes within ±20 % / total | notes |"
    )
    ap("|---|---|---|---:|---:|---|")
    for rr in receptors_report:
        max_t = max(
            (t["tanimoto"] for t in rr["tanimoto_vs_real"] if t["tanimoto"] is not None),
            default=float("nan"),
        )
        n_within = sum(1 for ax in rr["axis_report"] if ax["within_tolerance"])
        n_axes = len(rr["axis_report"])
        note = "formal-charge missmatched" if rr["charge_missmatched"] else "clean"
        ap(
            f"| {rr['receptor']} | {rr['decoy_name']} | "
            f"`{rr['props']['canonical_sha256'][:16]}…` | {max_t:.3f} | "
            f"{n_within}/{n_axes} | {note} |"
        )
    if glp1r_report is not None:
        ap(
            f"| GLP1R | GLP-1(7-36) scramble | `{glp1r_report['peptide_sha256'][:16]}…` | "
            f"peptide (n/a) | length+composition-preserved | "
            f"Hamming={glp1r_report['hamming']}/{len(GLP1_NATIVE)} |"
        )
    ap("")

    ap("## Per-receptor blocks")
    ap("")
    for rr in receptors_report:
        _write_receptor_block(rr, ap)

    if glp1r_report is not None:
        ap("## GLP1R peptide decoy")
        ap("")
        ap(f"- Native GLP-1(7-36) sequence: `{GLP1_NATIVE}`")
        ap(f"  - length: {len(GLP1_NATIVE)} residues")
        ap(
            f"  - composition Counter: `{dict(sorted(Counter(GLP1_NATIVE).items()))}`"
        )
        ap(f"  - SHA-256(native): `{sha256_hex(GLP1_NATIVE)}`")
        ap(f"- Decoy (composition-preserved scramble): `{glp1r_report['scrambled']}`")
        ap(f"  - length: {len(glp1r_report['scrambled'])} residues (matches native)")
        ap(
            f"  - composition Counter: `{dict(sorted(Counter(glp1r_report['scrambled']).items()))}`"
        )
        same = Counter(GLP1_NATIVE) == Counter(glp1r_report["scrambled"])
        ap(f"  - composition matches native: **{same}** (assert holds — permutation invariant)")
        ap(f"  - Hamming(scrambled, native): **{glp1r_report['hamming']}/{len(GLP1_NATIVE)}**"
           f" (floor MIN_HAMMING = {MIN_HAMMING})")
        ap(f"  - deterministic seed: `{glp1r_report['seed']}` "
           f"= `int.from_bytes(SHA-256('GLP1R|{SCRAMBLE_SALT}|{glp1r_report['variant']}')[:8], 'big') & (2**63-1)`")
        ap(f"  - SHA-256(scrambled peptide UTF-8): `{glp1r_report['peptide_sha256']}`")
        ap("")
        ap(
            "Method mirrors Block B's `scripts/build_shuffled_decoy_constructs.py` "
            "α5-CT scramble discipline verbatim: composition-preserved permutation "
            "with a deterministic per-slug seed and a Hamming floor. Verified via "
            "`Counter(scrambled) == Counter(original)` (permutation invariant, "
            "asserted at build time)."
        )
        ap("")
    else:
        ap("## GLP1R peptide decoy")
        ap("")
        ap(
            "GLP1R was dropped from `refs/ligand_set.csv` at Block C Step 1.5 "
            "(2026-09-02). Legacy peptide-decoy code path retained in "
            "`scripts/build_block_c_decoys.py::PEPTIDE_DECOYS` under salt "
            "`block_c_decoy_lig_v1` for byte-preserving replay if the GLP1R "
            "row is ever restored."
        )
        ap("")

    ap("## Parse failures (real-ligand SMILES that RDKit could not canonicalise)")
    ap("")
    if not parse_failures:
        ap("None. All real-ligand SMILES in `refs/ligand_set.csv` canonicalised cleanly.")
    else:
        ap(
            "The following A1-supplied real-ligand SMILES failed RDKit "
            "canonicalisation. Per stop-and-report threshold, this is A3 "
            "(Gate 0.2 SMILES-support probe) territory; the rows are LOGGED "
            "here and EXCLUDED from the receptor's property-window computation "
            "for the affected decoy row. Property matching for the decoy is "
            "therefore against the surviving parseable real ligands only."
        )
        ap("")
        ap("| receptor | ligand | SMILES | error |")
        ap("|---|---|---|---|")
        for r, name, smi in parse_failures:
            ap(f"| {r} | {name} | `{smi}` | RDKit `MolFromSmiles` returned None |")
        ap("")
        ap(
            "**A3 handoff**: fix these SMILES (kekulisation / aromaticity "
            "issue in each case) at the A1/A3 seam. B2 does not modify A1's "
            "rows; only the `decoy_lig` rows are B2's ownership."
        )
    ap("")

    ap("## Limitations")
    ap("")
    ap(
        "- Live ChEMBL was not queried. No-known-binding rests on published "
        "FDA off-target profiles for each decoy. Any post-hoc cross-reactivity "
        "finding at the receptor-of-interest triggers re-selection via a "
        "fallback candidate through this same script."
    )
    ap(
        "- Formal charge is computed on the SMILES as written (canonical form); "
        "physiological protonation at pH 7.4 is a separate axis (annotated in "
        "`refs/ligand_set.csv`'s `protonation_ph74_note` column for real ligands)."
    )
    ap(
        "- Preladenant and suvorexant (A1 SMILES) fail RDKit kekulisation; "
        "AA2AR and OX2R property windows are computed from the surviving "
        "parseable real ligands for those receptors."
    )
    ap("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")


def _write_receptor_block(rr: dict, ap) -> None:
    ap(f"### {rr['receptor']} — {rr['decoy_name']}")
    ap("")
    ap(f"- **source**: {rr['decoy_source']}")
    ap(f"- **canonical SMILES**: `{rr['props']['canonical_smiles']}`")
    ap(f"- **InChI**: `{rr['props']['inchi']}`")
    ap(f"- **SHA-256(canonical SMILES)**: `{rr['props']['canonical_sha256']}`")
    ap(f"- **atom Counter**: `{dict(sorted(rr['props']['atom_counter'].items()))}`")
    ap(f"- **heavy-atom count**: {rr['props']['hac']}")
    ap("")
    ap("#### Property comparison")
    ap("")
    ap("| axis | real mean | real σ (n≥2) | decoy | Δ vs mean | within ±20 % |")
    ap("|---|---:|---:|---:|---:|:---:|")
    for ax in rr["axis_report"]:
        mean_str = "n/a" if ax["n_real"] == 0 else f"{ax['mean']:.3f}"
        sigma_str = "-" if ax["n_real"] < 2 else f"{ax['sigma']:.3f}"
        decoy_str = f"{ax['decoy_val']:.3f}" if isinstance(ax["decoy_val"], float) else str(ax["decoy_val"])
        delta_str = _fmt_pct_delta(ax["decoy_val"], ax["mean"]) if ax["n_real"] > 0 else "n/a"
        mark = "✓" if ax["within_tolerance"] else "✗"
        ap(f"| {ax['axis']} | {mean_str} | {sigma_str} | {decoy_str} | {delta_str} | {mark} |")
    ap("")
    if rr["charge_missmatched"]:
        ap(
            "> **formal_charge_missmatched=true** — aminergic real ligands force +1 "
            "cationic scaffolds; a topologically-distinct non-binder that also "
            "matches +1 charge has high documented cross-reactivity risk. Per "
            "Decision A (2026-09-03), formal charge is relaxed here. All other "
            "axes and Tanimoto < 0.3 hold."
        )
        ap("")
    ap("#### Real-ligand context (parseable rows only)")
    ap("")
    ap("| ligand | activity | MW | logP | HBD | HBA | Rot | formal charge |")
    ap("|---|---|---:|---:|---:|---:|---:|---:|")
    for r in rr["real_ligands_used"]:
        p = r["props"]
        ap(
            f"| {r['name']} | {r['activity_class']} | {p['mw']:.2f} | "
            f"{p['logp']:.2f} | {p['hbd']} | {p['hba']} | {p['rot']} | {p['charge']} |"
        )
    ap("")
    ap("#### Morgan Tanimoto (radius 2, 1024 bits)")
    ap("")
    ap("| real ligand | Tanimoto | < 0.30 |")
    ap("|---|---:|:---:|")
    for t in rr["tanimoto_vs_real"]:
        tval = t["tanimoto"]
        if tval is None:
            ap(f"| {t['name']} | (parse fail) | n/a |")
        else:
            mark = "✓" if tval < TANIMOTO_MAX else "✗"
            ap(f"| {t['name']} | {tval:.3f} | {mark} |")
    ap("")
    ap("#### Byte-level composition diff vs closest real ligand")
    ap("")
    closest = rr["closest_real"]
    if closest is None:
        ap("No parseable real ligand available; composition diff skipped.")
    else:
        cp = closest["props"]
        dp = rr["props"]
        decoy_atoms = Counter(dp["atom_counter"])
        real_atoms = Counter(cp["atom_counter"])
        added = decoy_atoms - real_atoms
        removed = real_atoms - decoy_atoms
        ap(
            f"- **Closest real ligand by Tanimoto**: {closest['name']} "
            f"(T = {rr['closest_tanimoto']:.3f})"
        )
        ap(f"- **Real-ligand atom Counter**: `{dict(sorted(real_atoms.items()))}`")
        ap(f"- **Decoy atom Counter**: `{dict(sorted(decoy_atoms.items()))}`")
        ap(f"- **Atoms in decoy not in real (or excess)**: `{dict(sorted(added.items()))}`")
        ap(f"- **Atoms in real not in decoy (or deficit)**: `{dict(sorted(removed.items()))}`")
        ap(f"- **HAC diff**: decoy {dp['hac']} vs real {cp['hac']} = "
           f"{dp['hac'] - cp['hac']:+d}")
        ap(f"- **Real canonical SMILES SHA-256**: `{sha256_hex(cp['canonical_smiles'])}`")
        ap(f"- **Decoy canonical SMILES SHA-256**: `{dp['canonical_sha256']}`")
    ap("")


# ---------------------------------------------------------------------------
# Tier 3 curation notes emitter
# ---------------------------------------------------------------------------


# Per-decoy annotation review required by coordinator (task spec §a-e).
# Rows: (a) FDA-approval + brand, (b) primary target/mechanism, (c) receptor-
# family paralog binding review, (d) chosen-because rationale, (e) fallback,
# (f) Tanimoto values (computed at runtime).
#
# One entry per Tier 3 small-mol decoy receptor. Keys must match
# DECOY_SMILES slugs. Peptide decoys (APJ, GHSR) have their own block below.

TIER3_DECOY_ANNOTATIONS: dict[str, dict[str, str]] = {
    "5HT2C": {
        "fda_status": "FDA-approved 1989 as Diprivan (propofol); iv general anesthetic and sedative",
        "primary_target": "GABA-A positive allosteric modulator; secondary agonist at TASK-1 (K2P3.1) two-pore-domain K+ channel",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at any 5-HT receptor subtype (5HT1A/B/D/E/F, 5HT2A/B/C, 5HT3, 5HT4, 5HT5A, 5HT6, 5HT7); PDSP screening panel returned no hits above 10 μM",
        "chosen_because": "MW 178.27 matches lorcaserin MW 181.66 (within +1.5%); hydrophobic 2,6-diisopropylphenol chemistry orthogonal to aminergic serotonin pharmacophore; no protonatable amine at physiological pH avoids off-target aminergic receptor family",
        "fallback": "acetaminophen (MW 151.16, HBD 2, HBA 2) if propofol fails Tanimoto",
    },
    "5HT5A": {
        "fda_status": "FDA-approved 1961 as Gantanol (sulfamethoxazole, component of Bactrim); antibacterial",
        "primary_target": "competitive inhibitor of bacterial dihydropteroate synthase (DHPS, EC 2.5.1.15); PABA analog blocking folate synthesis",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at any 5-HT receptor subtype; sulfonamide-oxazole scaffold has no serotonergic activity in radioligand screens",
        "chosen_because": "MW 253.28 within -11% of 5-CT/NN6 mean (285); sulfonamide scaffold chemistry orthogonal to indole-tryptamine + acyl-guanidine chemotypes; no protonatable amine",
        "fallback": "phenacetin (MW 179.22, HBD 1, HBA 2) if sulfamethoxazole fails Tanimoto",
    },
    "ACM1": {
        "fda_status": "FDA-approved 1957 as Orinase (tolbutamide); first-generation sulfonylurea antidiabetic (largely superseded by later sulfonylureas)",
        "primary_target": "closure of pancreatic β-cell K-ATP channels (SUR1/Kir6.2), triggering insulin secretion; no G-protein-coupled activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at any muscarinic subtype (M1–M5); sulfonylurea chemistry has no cholinergic activity",
        "chosen_because": "MW 270.35 within -8% of tiotropium/iperoxo mean (295); sulfonylurea chemistry orthogonal to quaternary-cation muscarinic pharmacophore; formal charge 0 vs real-ligand +1 flagged as `formal_charge_missmatched=true` per Decision A (aminergic-like +1 cations force neutral decoy)",
        "fallback": "piroxicam (MW 331.35, oxicam NSAID) if tolbutamide fails Tanimoto",
    },
    "ADA2A": {
        "fda_status": "FDA-approved 1952 as Mucinex/Robitussin (guaifenesin); expectorant, no receptor pharmacology",
        "primary_target": "reduces mucus viscosity via bronchial-secretion volume increase; no defined molecular target at therapeutic doses (per PubChem MOA record)",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at any α- or β-adrenergic receptor subtype (α1A/B/D, α2A/B/C, β1, β2, β3); glyceryl guaiacolate chemistry has no adrenergic activity",
        "chosen_because": "MW 198.22 within +17% of noradrenaline MW 170.19; polar diol chemistry chemistry-orthogonal to catecholamine pharmacophore; formal charge 0 vs real-ligand +1 flagged as `formal_charge_missmatched=true` per Decision A",
        "fallback": "methocarbamol (MW 241.24, HBD 3, HBA 5) if guaifenesin fails Tanimoto",
    },
    "ADRB1": {
        "fda_status": "FDA-approved 1899 (Bayer); OTC as Aspirin/Bayer; NSAID + antiplatelet + antiinflammatory",
        "primary_target": "irreversible covalent acetylation of COX-1 Ser530 (and COX-2 Ser516); TXA2 suppression drives antiplatelet effect",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at any β-adrenergic receptor (β1, β2, β3) or α-adrenergic subtype; acetylsalicylate chemistry has no adrenergic activity",
        "chosen_because": "MW 180.16 within -1% of L-epinephrine MW 183.21; salicylate chemistry orthogonal to catecholamine pharmacophore; formal charge 0 vs real-ligand +1 flagged as `formal_charge_missmatched=true` per Decision A",
        "fallback": "acetaminophen (MW 151.16, HBD 2, HBA 2) if aspirin fails Tanimoto",
    },
    "AGTR1": {
        "fda_status": "FDA-approved 2002 as Zetia (ezetimibe); hypocholesterolemic",
        "primary_target": "Niemann-Pick C1-Like 1 (NPC1L1) transporter antagonism at intestinal brush border; blocks dietary + biliary cholesterol absorption",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at AT1, AT2, or Mas-related angiotensin receptors; azetidinone chemistry has no ARB activity; SARTAN-avoidance rule satisfied (no biphenyl-tetrazole scaffold)",
        "chosen_because": "MW 409.43 within -8% of olmesartan MW 446.51; β-lactam-diaryl chemistry orthogonal to biphenyl-tetrazole sartan pharmacophore; distinct target class (lipid transporter vs GPCR)",
        "fallback": "loratadine (MW 382.89) if ezetimibe fails Tanimoto",
    },
    "CCKAR": {
        "fda_status": "FDA-approved 1976 as Imodium (loperamide); OTC antidiarrheal",
        "primary_target": "P-glycoprotein-effluxed peripheral μ-opioid receptor agonist (blood-brain-barrier excluded); gut motility inhibition",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at CCK1 or CCK2 receptors; diphenyl-piperidine chemistry has no CCK-family activity (unlike benzodiazepine antagonists like devazepide)",
        "chosen_because": "MW 477.04 within +17% of devazepide MW 452.55 + CCK-8s peptide mean; diphenyl-piperidine chemistry orthogonal to benzodiazepine + peptide chemotypes; distinct target class (μ-opioid vs CCK)",
        "fallback": "cinnarizine (MW 368.51) if loperamide fails Tanimoto",
    },
    "CCR5": {
        "fda_status": "FDA-approved 2001 as Gleevec (imatinib mesylate); antineoplastic",
        "primary_target": "ATP-competitive tyrosine-kinase inhibitor at BCR-Abl, c-Kit, PDGFR-α/β, DDR1/2; no GPCR activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at CCR1-CCR10 or CXCR1-CXCR7 chemokine receptors; ANTIVIRAL-AVOIDANCE rule satisfied — imatinib is NOT a CCR5 antagonist class (maraviroc/vicriviroc/cenicriviroc all excluded)",
        "chosen_because": "MW 493.61 within -4% of maraviroc MW 513.68; pyrimidine-amide chemistry orthogonal to tropane-based CCR5 antagonist scaffold; distinct target class (Bcr-Abl kinase vs chemokine GPCR)",
        "fallback": "fexofenadine (MW 501.66) if imatinib fails Tanimoto",
    },
    "CNR1": {
        "fda_status": "FDA-approved 1991 as Zocor (simvastatin); antihyperlipidemic",
        "primary_target": "prodrug hydrolyzed to β-hydroxy acid; competitive inhibitor of HMG-CoA reductase (mevalonate pathway); no GPCR activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at CB1 or CB2 cannabinoid receptors; decalin-lactone chemistry has no cannabinoid activity",
        "chosen_because": "MW 405 within -14% of AM6538/MDMB-Fubinaca mean 462; decalin-lactone chemistry orthogonal to pyrazole-carboxamide + indazole-carboxamide cannabinoid chemotypes; distinct target class",
        "fallback": "fluvastatin (MW 411.47) if simvastatin fails Tanimoto",
    },
    "CNR2": {
        "fda_status": "FDA-approved 1987 as Mevacor (lovastatin); antihyperlipidemic (natural product from Aspergillus terreus)",
        "primary_target": "prodrug hydrolyzed to β-hydroxy acid; competitive inhibitor of HMG-CoA reductase; no GPCR activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at CB1 or CB2 receptors; decalin-lactone chemistry has no cannabinoid activity",
        "chosen_because": "MW 404.55 within +2% of AM10257/HU-308-analog mean 399; decalin-lactone chemistry orthogonal to adamantyl-pyrazole + resorcinol cannabinoid chemotypes; deliberate simvastatin/lovastatin split with CNR1 to avoid within-family within-block statin cluster",
        "fallback": "pravastatin (MW 424.53) if lovastatin fails Tanimoto",
    },
    "CXCR2": {
        "fda_status": "FDA-approved 1995 as Amaryl (glimepiride); third-generation sulfonylurea antidiabetic",
        "primary_target": "closure of pancreatic β-cell K-ATP channels (SUR1/Kir6.2 binding); insulinotropic",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at CXCR1-CXCR7 or CCR1-CCR10 chemokine receptors; sulfonylurea chemistry has no chemokine activity",
        "chosen_because": "MW 519 within +22% of EBX MW 438 (mildly outside strict ±20% MW gate; other axes closer); sulfonylurea chemistry orthogonal to squarate-cyclobutenedione allosteric antagonist scaffold; distinct target class",
        "fallback": "cefadroxil (MW 363.39) if glimepiride fails Tanimoto",
    },
    "CXCR4": {
        "fda_status": "FDA-approved 1951 as Atabrine (quinacrine); antimalarial + antiprotozoal; also has anti-prion investigational status",
        "primary_target": "acridine DNA intercalation; secondary phospholipase A2 inhibition (COX-2/prostaglandin suppression); no GPCR activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at CXCR1-CXCR7 or CCR1-CCR10; aminoacridine chemistry has no chemokine activity",
        "chosen_because": "MW 400 within -2% of IT1t MW 407; acridine chemistry orthogonal to isothiourea-imidazothiazole CXCR4 antagonist scaffold; formal charge 0 vs real-ligand +1/+2 flagged as `formal_charge_missmatched=true` per Decision A",
        "fallback": "hydroxychloroquine (MW 335.87) if quinacrine fails Tanimoto",
    },
    "DRD2": {
        "fda_status": "FDA-approved 1989 as Prilosec (omeprazole); proton-pump inhibitor",
        "primary_target": "prodrug activated at acidic parietal-cell pH; irreversible covalent inhibitor of gastric H+/K+-ATPase (via disulfide bond to Cys813)",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at D1-D5 dopamine receptors or 5-HT/α-adrenergic aminergic subtypes; benzimidazole-sulfoxide-pyridine chemistry has no monoaminergic activity",
        "chosen_because": "MW 345.42 within +10% of rotigotine MW 315.47; benzimidazole-pyridine chemistry orthogonal to aminotetralin dopaminergic scaffold; formal charge 0 vs real-ligand +1 flagged as `formal_charge_missmatched=true` per Decision A",
        "fallback": "pantoprazole (MW 383.37) if omeprazole fails Tanimoto",
    },
    "EDNRA": {
        "fda_status": "FDA-approved 1993 as Tricor/Lipanthyl (fenofibrate); antihyperlipidemic",
        "primary_target": "prodrug hydrolyzed to fenofibric acid; PPAR-α agonist; upregulates apoA-I/apoA-II, downregulates apoC-III → LDL clearance",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at ETA or ETB endothelin receptors; ARB-avoidance rule satisfied (no biphenyl-tetrazole scaffold — fenofibrate is a phenoxy-isobutyrate)",
        "chosen_because": "MW 360.83 within -5% of ambrisentan MW 378.42; phenoxy-isobutyrate chemistry orthogonal to pyrimidinyl-oxy-propanoate + sulfonamide endothelin scaffolds; distinct target class",
        "fallback": "diflunisal (MW 250.20) if fenofibrate fails Tanimoto",
    },
    "EDNRB": {
        "fda_status": "FDA-approved 1996 as Allegra (fexofenadine); second-generation H1 antihistamine",
        "primary_target": "peripheral H1 histamine-receptor inverse agonist; poor CNS penetration due to P-gp efflux",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at ETA or ETB endothelin receptors; diphenyl-piperidine-butyrate chemistry has no endothelin activity",
        "chosen_because": "MW 501.66 within -9% of bosentan MW 551.62; deliberately different fibrate/antihistamine chemotypes from EDNRA (fenofibrate) to avoid within-family within-block chemistry artifact; distinct target class",
        "fallback": "cefixime (MW 453.45) if fexofenadine fails Tanimoto",
    },
    "GRPR": {
        "fda_status": "FDA-approved 1998 as Viagra (sildenafil); PDE5 inhibitor for erectile dysfunction and pulmonary hypertension",
        "primary_target": "competitive cGMP-analog inhibitor of PDE5 phosphodiesterase; increased cGMP → smooth-muscle relaxation",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at GRP, NMB, or BB3 bombesin-family receptors; pyrazolopyrimidinone-sulfonyl-piperazine chemistry has no bombesin activity",
        "chosen_because": "MW 474.58 within -19% of PD-176252 MW 583; sulfonamide-pyrazolopyrimidinone chemistry orthogonal to indole-urea bombesin-antagonist chemotype; distinct target class (PDE5 phosphodiesterase vs GRPR GPCR)",
        "fallback": "tadalafil (MW 389.40) if sildenafil fails Tanimoto",
    },
    "HRH1": {
        "fda_status": "FDA-approved 1995 as Glucophage (metformin, biguanide); type-2 diabetes first-line",
        "primary_target": "hepatic gluconeogenesis suppression via AMPK activation; complex I of mitochondrial electron transport chain (secondary)",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at H1, H2, H3, or H4 histamine receptors; biguanide chemistry has no histaminergic activity",
        "chosen_because": "MW 129.17 within +16% of histamine MW 111.15; biguanide chemistry orthogonal to imidazole-ethylamine histamine pharmacophore; distinct target class",
        "fallback": "acetaminophen (MW 151.16) if metformin fails Tanimoto",
    },
    "HRH3": {
        "fda_status": "FDA-approved 1982 as Cardizem (diltiazem); non-dihydropyridine L-type calcium channel blocker",
        "primary_target": "voltage-gated L-type Ca²⁺ channel (Cav1.2/Cav1.3) benzothiazepine-site blocker; cardiac + smooth-muscle relaxation",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at H1, H2, H3, or H4 histamine receptors; benzothiazepine chemistry has no histaminergic activity",
        "chosen_because": "MW 414.52 within +29% of bavisant MW 322.42 (marginally outside ±20% MW gate; logP/HBD/HBA closer); benzothiazepine-acetate chemistry orthogonal to cyclobutane-carboxamide-pyrrolidine H3 antagonist scaffold; formal charge 0 vs real-ligand +1 flagged as `formal_charge_missmatched=true` per Decision A",
        "fallback": "cinacalcet (MW 357.42) if diltiazem fails Tanimoto",
    },
    "LPAR1": {
        "fda_status": "FDA-approved 2003 as Crestor (rosuvastatin); hypocholesterolemic",
        "primary_target": "competitive HMG-CoA reductase inhibitor; no GPCR activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at LPA1-LPA6 lysophosphatidic-acid receptors; statin chemistry has no lysophospholipid-receptor activity",
        "chosen_because": "MW 481.55 within +1% of ONO-3080573/LPA 18:1 mean 476; sulfonamide-pyrimidine-heptanoate chemistry orthogonal to indanyloxy-cyclopropane-carboxylate + lysophospholipid chemotypes; distinct target class (HMG-CoA reductase vs LPA GPCR)",
        "fallback": "atorvastatin (MW 558.64) if rosuvastatin fails Tanimoto",
    },
    "LT4R1": {
        "fda_status": "FDA-approved 1976 as Lopid (gemfibrozil); fibrate antihyperlipidemic (largely superseded by fenofibrate but still on market)",
        "primary_target": "PPAR-α agonist (weaker than fenofibrate); lipoprotein-lipase upregulation; VLDL/TG reduction",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at BLT1, BLT2, CysLT1, CysLT2, GPR17, or FPR2 leukotriene/eicosanoid receptors; phenoxy-isobutyrate chemistry has no leukotriene activity",
        "chosen_because": "MW 250.34 within -40% of MK-D-046/LTB4 mean 416 (outside strict ±20% MW gate but chemistry-orthogonal to both real ligands; logP/charge closer); deliberate gemfibrozil/fenofibrate split with EDNRA to avoid within-family within-block fibrate cluster",
        "fallback": "fenofibrate (MW 360.83) if gemfibrozil fails Tanimoto (last-resort — same fibrate class as EDNRA)",
    },
    "MCHR1": {
        "fda_status": "FDA-approved 1977 as Nolvadex (tamoxifen citrate); SERM for breast cancer",
        "primary_target": "estrogen receptor α (ERα) partial antagonist / partial agonist (tissue-dependent); active metabolite endoxifen",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at MCH1 or MCH2 melanin-concentrating-hormone receptors; triarylethylene SERM chemistry has no MCH activity",
        "chosen_because": "MW 371.52 within -22% of SNAP-94847 MW 494 (marginally outside strict ±20% MW gate; logP/HBA closer); triarylethylene-aminoether SERM chemistry orthogonal to biaryl-piperidine-difluorophenoxy MCH1 antagonist; formal charge 0 vs real-ligand +1 flagged as `formal_charge_missmatched=true`",
        "fallback": "raloxifene (MW 473.58) if tamoxifen fails Tanimoto",
    },
    "NPY1R": {
        "fda_status": "FDA-approved 1995 as Invirase (saquinavir); HIV-1 protease inhibitor",
        "primary_target": "peptidomimetic transition-state analog inhibitor of HIV-1 aspartic protease; blocks viral polyprotein cleavage",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at Y1-Y6 neuropeptide-Y receptors; peptidomimetic-HIV-PI chemistry has no NPY-family activity",
        "chosen_because": "MW 670.85 within +9% of UR-MK299 MW 615.74; peptidomimetic decahydroquinoline + naphthylcarboxamide chemistry orthogonal to acylguanidine-D-ornithinamide Y1R antagonist chemotype; formal charge 0 vs real-ligand +1 flagged",
        "fallback": "posaconazole (MW 700.78) if saquinavir fails Tanimoto",
    },
    "NPY2R": {
        "fda_status": "FDA-approved 2007 as Tasigna (nilotinib); BCR-Abl tyrosine-kinase inhibitor for CML",
        "primary_target": "ATP-competitive Bcr-Abl kinase inhibitor (2nd-generation; more selective than imatinib); minor c-Kit/PDGFR activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at Y1-Y6 neuropeptide-Y receptors; imidazole-pyrimidine-benzamide TKI chemistry has no NPY-family activity",
        "chosen_because": "MW 529.53 within -6% of JNJ-31020028 MW 590; deliberate saquinavir/nilotinib split with NPY1R to test different chemotype at each Y-family subtype; distinct target class",
        "fallback": "dasatinib (MW 488.01) if nilotinib fails Tanimoto",
    },
    "OPRD": {
        "fda_status": "FDA-approved 1993 as Claritin (loratadine); OTC second-generation H1 antihistamine",
        "primary_target": "peripheral H1 histamine-receptor inverse agonist; low CNS penetration; hepatic metabolism to active desloratadine",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at δ, μ, or κ opioid receptors above 10 μM; tricyclic piperidinylidene chemistry has weak μ-opioid affinity in high-dose radioligand screens (>10 μM range, clinically non-relevant) but no reported affinity at δ (DOR) receptor specifically. Coordinator Q5 accepted this pattern",
        "chosen_because": "MW 382.89 within -15% of naltrindole/DPI-287 mean 450; tricyclic piperidinylidene chemistry orthogonal to morphinan (naltrindole) + benzhydryl-piperazine (DPI-287) opioid pharmacophores; formal charge 0 vs real-ligand +1 flagged as `formal_charge_missmatched=true`",
        "fallback": "cetirizine (MW 388.89) if loratadine fails Tanimoto",
    },
    "OPRK": {
        "fda_status": "FDA-approved 2001 as Clarinex (desloratadine); active metabolite of loratadine; second-generation H1 antihistamine",
        "primary_target": "peripheral H1 histamine-receptor inverse agonist; H2 partial affinity; longer half-life than loratadine",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at κ (KOR), δ (DOR), or μ (MOR) opioid receptors at clinically relevant doses; deliberate loratadine/desloratadine split with OPRD to test parent vs metabolite chemistry",
        "chosen_because": "MW 310.83 within -33% of JDTic/Dyn-A mean 466 (outside strict ±20% MW gate; distinct target class dominates); tricyclic piperidyl chemistry orthogonal to piperidine-diaryl JDTic pharmacophore; formal charge 0 vs real-ligand +1/+2 flagged",
        "fallback": "cetirizine (MW 388.89) if desloratadine fails Tanimoto",
    },
    "OPRX": {
        "fda_status": "FDA-approved 2004 as Sensipar/Mimpara (cinacalcet); calcimimetic for secondary hyperparathyroidism",
        "primary_target": "positive allosteric modulator of calcium-sensing receptor (CaSR, class C GPCR); no class A opioid activity",
        "paralog_review": "IUPHAR & PubChem BindingDB: no reported affinity at NOP, δ, μ, or κ opioid receptors; naphthyl-propylamine chemistry has no opioid activity",
        "chosen_because": "MW 371.52 within -11% of SB-612111 MW 402; naphthyl-CF3-phenyl-propylamine chemistry orthogonal to benzocycloheptenol-piperidine NOP antagonist scaffold; formal charge 0 vs real-ligand +1 flagged; class C CaSR target vs class A NOP receptor",
        "fallback": "terbinafine (MW 291.44) if cinacalcet fails Tanimoto",
    },
}


TIER3_PEPTIDE_ANNOTATIONS: dict[str, dict[str, str]] = {
    "APJ": {
        "native_context": "Apelin-13 is the endogenous full agonist at APJ (aka APLNR). Native mature peptide is preproapelin(55-67) — a 13-mer L-alpha peptide with C-terminal Phe (in vivo amidated, F-NH2, not representable in sequence input).",
        "paradigm": "Peptide-only agonist + antag=NA → scrambled-peptide decoy per Tier 1 GLP1R precedent. Composition-preserved permutation with per-length Hamming floor (max(8, round(0.65·N)) = 8 for the 13-mer).",
        "salt": "block_c_tier3_decoy_lig_v1",
    },
    "GHSR": {
        "native_context": "Ghrelin-28 is the endogenous full agonist at GHSR. Native mature peptide is preproghrelin(24-51) — a 28-mer L-alpha peptide. NATIVE PTM: Ser3-O-octanoyl (C8:0) fatty-acid ester, essential for GHSR agonism, not representable in sequence-only input. Deacyl-ghrelin (the sequence used here) is ~1000× weaker in binding assays — downstream analysis must carry this caveat.",
        "paradigm": "Peptide-only agonist + antag=NA → scrambled-peptide decoy. Composition-preserved permutation with Hamming floor 18 (65% of 28).",
        "salt": "block_c_tier3_decoy_lig_v1",
    },
}


def emit_tier3_notes_md(
    small_mol_reports: list[dict],
    peptide_reports: list[dict],
    parse_failures: list[tuple[str, str, str]],
    out_path: Path,
) -> None:
    """Emit the S3 Tier 3 curation notes MD.

    Content per coordinator §a-f contract:
      (a) FDA-approval + brand
      (b) primary target/mechanism
      (c) receptor-family paralog binding review
      (d) chosen-because rationale
      (e) fallback
      (f) computed Tanimoto values vs each real ligand
    """
    lines: list[str] = []
    ap = lines.append

    ap("# Block C Tier 3 — Stage 3 Decoy Construction Notes (§a–f review)")
    ap("")
    ap(
        "Emitted by `scripts/build_block_c_decoys.py`. Deterministic; a "
        "second run produces byte-identical output (canonical SMILES via "
        "`Chem.MolToSmiles(..., canonical=True)`, peptide scramble seeded "
        "from `SHA-256('receptor|salt|variant')[:8]`)."
    )
    ap("")
    ap(
        "Companion to `experiments/020_block_c_ligand_pharmacology/analysis/"
        "decoy_verification.md` (Tier 1 verification). This file covers the "
        "26 small-mol + 2 scrambled-peptide Tier 3 decoys plus the 4 NA "
        "receptors documented as intentional NA."
    )
    ap("")
    ap("## Contract compliance summary")
    ap("")
    ap(
        f"- **Small-molecule decoys**: {len(small_mol_reports)} receptors "
        f"({'all pass Tanimoto<0.30' if all(max((t['tanimoto'] for t in rr['tanimoto_vs_real'] if t['tanimoto'] is not None), default=0.0) < TANIMOTO_MAX for rr in small_mol_reports) else 'SOME FAIL — REBUILD REQUIRED'})"
    )
    ap(
        f"- **Scrambled-peptide decoys**: {len(peptide_reports)} receptors "
        f"(deterministic seed under `block_c_tier3_decoy_lig_v1` salt)"
    )
    ap(f"- **Intentional NA receptors**: {len(TIER3_NA_RECEPTORS)} "
       f"({', '.join(sorted(TIER3_NA_RECEPTORS.keys()))})")
    ap("")

    ap("## Tanimoto + property summary")
    ap("")
    ap(
        "| receptor | decoy | canonical SMILES SHA-256 (short) | max T vs "
        "reals | axes within ±20 % | charge missmatched |"
    )
    ap("|---|---|---|---:|---:|:---:|")
    for rr in small_mol_reports:
        max_t = max(
            (t["tanimoto"] for t in rr["tanimoto_vs_real"] if t["tanimoto"] is not None),
            default=float("nan"),
        )
        n_within = sum(1 for ax in rr["axis_report"] if ax["within_tolerance"])
        n_axes = len(rr["axis_report"])
        chg = "✗ (Decision A)" if rr["charge_missmatched"] else "✓"
        ap(
            f"| {rr['receptor']} | {rr['decoy_name']} | "
            f"`{rr['props']['canonical_sha256'][:16]}…` | {max_t:.3f} | "
            f"{n_within}/{n_axes} | {chg} |"
        )
    for pr in peptide_reports:
        ap(
            f"| {pr['receptor']} | {pr['common_name']} scramble | "
            f"`{pr['peptide_sha256'][:16]}…` | peptide (n/a) | "
            f"length+composition-preserved | Hamming={pr['hamming']}/{len(pr['native_seq'])} |"
        )
    ap("")

    ap("## Per-decoy §a–f review")
    ap("")

    # Order the small-mol blocks alphabetically for the human review.
    for rr in sorted(small_mol_reports, key=lambda r: r["receptor"]):
        ann = TIER3_DECOY_ANNOTATIONS.get(rr["receptor"], {})
        ap(f"### {rr['receptor']} — {rr['decoy_name']}")
        ap("")
        ap(f"- **(a) FDA status**: {ann.get('fda_status', 'not annotated')}")
        ap(f"- **(b) Primary target**: {ann.get('primary_target', 'not annotated')}")
        ap(f"- **(c) Paralog binding review**: {ann.get('paralog_review', 'not annotated')}")
        ap(f"- **(d) Chosen because**: {ann.get('chosen_because', 'not annotated')}")
        ap(f"- **(e) Fallback**: {ann.get('fallback', 'not annotated')}")
        ap("- **(f) Tanimoto vs each real ligand**:")
        for t in rr["tanimoto_vs_real"]:
            tval = t["tanimoto"]
            if tval is None:
                ap(f"    - {t['name']}: (RDKit parse fail — excluded)")
            else:
                mark = "✓ <0.30" if tval < TANIMOTO_MAX else "✗ ≥0.30"
                ap(f"    - {t['name']}: T = {tval:.3f} {mark}")
        ap("")
        ap(f"- **canonical SMILES**: `{rr['props']['canonical_smiles']}`")
        ap(f"- **InChI**: `{rr['props']['inchi']}`")
        ap(f"- **SHA-256(canonical SMILES)**: `{rr['props']['canonical_sha256']}`")
        ap("")
        ap("| axis | real mean | decoy | Δ vs mean | within ±20 % |")
        ap("|---|---:|---:|---:|:---:|")
        for ax in rr["axis_report"]:
            mean_str = "n/a" if ax["n_real"] == 0 else f"{ax['mean']:.3f}"
            decoy_str = f"{ax['decoy_val']:.3f}" if isinstance(ax["decoy_val"], float) else str(ax["decoy_val"])
            delta_str = _fmt_pct_delta(ax["decoy_val"], ax["mean"]) if ax["n_real"] > 0 else "n/a"
            mark = "✓" if ax["within_tolerance"] else "✗"
            ap(f"| {ax['axis']} | {mean_str} | {decoy_str} | {delta_str} | {mark} |")
        ap("")
        if rr["charge_missmatched"]:
            ap(
                "> **formal_charge_missmatched=true** (Decision A, coordinator "
                "2026-09-03 + confirmed 2026-09-04). Aminergic real ligands "
                "force +1 cationic scaffolds; matching charge would introduce "
                "documented cross-reactivity risk. All other axes and "
                "Tanimoto<0.30 hold. Precedent-consistent with all 8 Tier 1 "
                "aminergic-anchor decoys."
            )
            ap("")

    # Peptide decoy blocks
    for pr in sorted(peptide_reports, key=lambda r: r["receptor"]):
        ann = TIER3_PEPTIDE_ANNOTATIONS.get(pr["receptor"], {})
        ap(f"### {pr['receptor']} — {pr['common_name']} scramble (peptide decoy)")
        ap("")
        ap(f"- **Native context**: {ann.get('native_context', 'not annotated')}")
        ap(f"- **Paradigm**: {ann.get('paradigm', 'not annotated')}")
        ap(f"- **Scramble salt**: `{pr['salt']}`")
        ap(f"- **Native sequence**: `{pr['native_seq']}` (length {len(pr['native_seq'])})")
        ap(f"- **Scrambled decoy**: `{pr['scrambled']}`")
        ap(f"  - length: {len(pr['scrambled'])} (matches native)")
        ap(
            f"  - composition preserved: **"
            f"{Counter(pr['scrambled']) == Counter(pr['native_seq'])}**"
        )
        ap(
            f"  - Hamming vs native: **{pr['hamming']}/{len(pr['native_seq'])}** "
            f"(floor = {pr['min_hamming']})"
        )
        ap(
            f"  - deterministic seed: `{pr['seed']}` = "
            f"`int.from_bytes(SHA-256('{pr['receptor']}|{pr['salt']}|"
            f"{pr['variant']}')[:8], 'big') & (2**63-1)`"
        )
        ap(f"  - SHA-256(scrambled peptide UTF-8): `{pr['peptide_sha256']}`")
        ap(f"  - SHA-256(native peptide UTF-8): `{sha256_hex(pr['native_seq'])}`")
        ap("")

    # NA receptors
    ap("## NA receptors (documented as intentional non-decoy)")
    ap("")
    ap(
        "These 4 receptors have no meaningful small-molecule OR peptide "
        "decoy that would test the ligand-identity claim, per coordinator "
        "confirmation 2026-09-04. Excluded from `DECOY_SMILES` and "
        "`PEPTIDE_DECOYS` by design; no compute burden."
    )
    ap("")
    for rec in sorted(TIER3_NA_RECEPTORS.keys()):
        ap(f"### {rec} (NA)")
        ap("")
        ap(TIER3_NA_RECEPTORS[rec])
        ap("")

    # Parse failures
    ap("## Parse failures (real-ligand SMILES that RDKit could not canonicalise)")
    ap("")
    if not parse_failures:
        ap(
            "None. All real-ligand SMILES in `refs/ligand_set.csv` + "
            "`refs/ligand_set_tier3.csv` canonicalised cleanly."
        )
    else:
        ap(
            "The following real-ligand SMILES failed RDKit canonicalisation "
            "and were excluded from property-window computation for the "
            "affected decoy row:"
        )
        ap("")
        ap("| receptor | ligand | SMILES | error |")
        ap("|---|---|---|---|")
        for r, name, smi in parse_failures:
            ap(f"| {r} | {name} | `{smi}` | RDKit `MolFromSmiles` returned None |")
    ap("")

    # Method + limitations
    ap("## Method")
    ap("")
    ap(
        "For each of the 26 small-mol `decoy_lig` entries in the Tier 3 "
        "arm of `DECOY_SMILES`:"
    )
    ap("")
    ap("1. Harvest real-ligand rows from `refs/ligand_set_tier3.csv` "
       "(receptor rows where `activity_class` ∈ `{full_agonist, "
       "neutral_antagonist}` with non-empty SMILES).")
    ap("2. Compute RDKit properties on each real-ligand SMILES: MW, logP, "
       "HBD, HBA, rotatable bonds, formal charge.")
    ap("3. Compute per-axis mean across the parseable real ligands.")
    ap(f"4. Score the decoy on each axis vs ±{int(PROPERTY_TOLERANCE * 100)} "
       "% of the mean. Formal-charge mismatch → `formal_charge_missmatched="
       "true` (Decision A).")
    ap(f"5. Compute Morgan fingerprint (r=2, 1024 bits) Tanimoto vs every "
       f"parseable real ligand. Hard gate: Tanimoto < {TANIMOTO_MAX}.")
    ap("6. Byte-level verification: SHA-256 of canonical SMILES (small-mol) "
       "or scrambled sequence UTF-8 (peptide). Atom-composition Counter + "
       "heavy-atom count diffed against the closest real ligand.")
    ap("")
    ap(
        "For the 2 peptide `decoy_lig` entries (APJ, GHSR): "
        "composition-preserved random permutation of the native agonist "
        "sequence, seeded from SHA-256 of the receptor slug + salt "
        "`block_c_tier3_decoy_lig_v1` + variant. Hamming floor = "
        "max(8, round(0.65 × len(sequence))). Retried across up to 256 "
        "variants until the floor is met."
    )
    ap("")

    ap("## Limitations")
    ap("")
    ap(
        "- Live ChEMBL/BindingDB was not queried. Paralog-binding review "
        "rests on published IUPHAR pharmacology + PubChem BindingDB "
        "curation entries for each drug + coordinator-approved uncertainty "
        "flags (Q1–Q8 review 2026-09-04). Any post-hoc cross-reactivity "
        "finding for a specific (decoy, receptor) pair triggers "
        "re-selection via the fallback candidate through this same script."
    )
    ap(
        "- Formal charge computed on canonical SMILES as written; "
        "physiological protonation state at pH 7.4 is annotated in "
        "`refs/ligand_set_tier3.csv`'s `protonation_ph74_note` for real "
        "ligands but NOT for decoys (Tier 3 decoys are not written to any "
        "refs/ file — they are Python-side only in `DECOY_SMILES`)."
    )
    ap(
        "- Some receptor property windows are computed from n=1 real "
        "ligand (single small-mol anchor when the other real is a peptide "
        "or NA). σ is undefined in these cases; the ±20% gate is applied "
        "against the single value."
    )
    ap("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main build
# ---------------------------------------------------------------------------


def _build_small_mol_report(
    receptor: str,
    smi: str,
    name: str,
    source: str,
    real: list[dict],
) -> tuple[dict, dict]:
    """Return (report_dict, csv_row_dict). The csv row is built for use
    only if the receptor is a CSV-rewrite target (Tier 1)."""
    real_parseable = [r for r in real if r["props"] is not None]
    if not real_parseable:
        raise RuntimeError(
            f"{receptor}: no parseable real-ligand rows across "
            f"ligand_set.csv + ligand_set_tier3.csv"
        )

    props = compute_props(smi)
    if props is None:
        raise RuntimeError(f"{receptor}: decoy SMILES {smi!r} failed to parse")

    # Tanimoto per real ligand.
    tanis: list[dict] = []
    for r in real:
        t = tanimoto(smi, r["smiles"]) if r["props"] is not None else None
        tanis.append({"name": r["name"], "tanimoto": t})
    max_t = max(
        (t["tanimoto"] for t in tanis if t["tanimoto"] is not None), default=0.0
    )
    if max_t >= TANIMOTO_MAX:
        raise RuntimeError(
            f"{receptor}: decoy {name} Tanimoto {max_t:.3f} ≥ {TANIMOTO_MAX}. "
            "Escalate to fallback candidate (edit DECOY_SMILES)."
        )

    # Property window and axis-by-axis check.
    window = per_receptor_property_window(real)
    axis_report: list[dict] = []
    for axis in PROPERTY_AXES:
        mean_val, sigma = window[axis]
        decoy_val = float(props[axis])
        within = within_tolerance(decoy_val, mean_val, PROPERTY_TOLERANCE)
        axis_report.append({
            "axis": axis,
            "mean": mean_val,
            "sigma": sigma,
            "decoy_val": decoy_val,
            "within_tolerance": within,
            "n_real": len(real_parseable),
        })
    charge_missmatched = not next(
        a["within_tolerance"] for a in axis_report if a["axis"] == "charge"
    )

    # Closest parseable real ligand by Tanimoto.
    pairs = [(t["name"], t["tanimoto"]) for t in tanis if t["tanimoto"] is not None]
    pairs.sort(key=lambda x: x[1], reverse=True)
    closest_name, closest_t = (pairs[0] if pairs else (None, None))
    closest_real = next(
        (r for r in real_parseable if r["name"] == closest_name), None
    )

    row = build_small_mol_decoy_row(
        receptor=receptor,
        decoy_smiles=smi,
        decoy_name=name,
        decoy_source=source,
        props=props,
        real_ligands=real,
        charge_missmatched=charge_missmatched,
    )
    report = {
        "receptor": receptor,
        "decoy_name": name,
        "decoy_source": source,
        "props": props,
        "axis_report": axis_report,
        "real_ligands_used": real_parseable,
        "tanimoto_vs_real": tanis,
        "charge_missmatched": charge_missmatched,
        "closest_real": closest_real,
        "closest_tanimoto": closest_t if closest_t is not None else 0.0,
    }
    return report, row


def _build_peptide_report(
    receptor: str,
    native_seq: str,
    common_name: str,
    salt: str,
    reals: list[dict],
    require_native_in_csv: bool,
) -> tuple[dict, dict] | None:
    """Compute the scrambled-peptide report + CSV row.

    Returns None (with no error) if `require_native_in_csv=True` and the
    receptor's native sequence isn't present in the CSV — that's the
    Tier 1 GLP1R gate after the Step 1.5 drop. Tier 3 peptide decoys
    always compute (require_native_in_csv=False), and the presence check
    below is against the merged real-ligand harvest.
    """
    native_row = next(
        (r for r in reals if r["peptide_sequence"] == native_seq),
        None,
    )
    if native_row is None:
        if require_native_in_csv:
            return None  # gated legacy path (GLP1R post-drop)
        raise RuntimeError(
            f"{receptor}: native {common_name} sequence not found in any "
            f"real-ligand row (peptide_sequence exact match)"
        )

    min_h = min_hamming_for(native_seq)
    scrambled, seed_used, variant_used = scramble_peptide(
        native_seq, receptor, salt=salt, min_hamming=min_h
    )
    h_dist = hamming(scrambled, native_seq)

    row = build_peptide_decoy_row(
        receptor=receptor,
        native_seq=native_seq,
        common_name=common_name,
        salt=salt,
        scrambled=scrambled,
        seed_used=seed_used,
        h_dist=h_dist,
        min_hamming=min_h,
    )
    report = {
        "receptor": receptor,
        "native_seq": native_seq,
        "common_name": common_name,
        "salt": salt,
        "scrambled": scrambled,
        "seed": seed_used,
        "variant": variant_used,
        "hamming": h_dist,
        "min_hamming": min_h,
        "peptide_sha256": sha256_hex(scrambled),
    }
    return report, row


def build_all(dry_run: bool = False, target_csv: Path | None = None,
              target_md: Path | None = None,
              target_tier3_md: Path | None = None,
              tier3_csv: Path | None = None) -> None:
    """Build Tier 1 (writes to target_csv + target_md) and Tier 3
    (verify-only; writes only to target_tier3_md).

    Receptor partitioning:
      - A `DECOY_SMILES` entry writes to the CSV iff the receptor has
        a `decoy_lig` row in `target_csv` (Tier 1 path).
      - Otherwise it's verified against Tier 3 CSV's real ligands and
        emitted only into `target_tier3_md`.
    """
    target_csv = target_csv or LIGAND_SET_CSV
    target_md = target_md or VERIFICATION_MD
    target_tier3_md = target_tier3_md or TIER3_NOTES_MD
    tier3_csv = tier3_csv or LIGAND_SET_TIER3_CSV

    original_lines = read_ligand_set_lines(target_csv)
    original_bytes = target_csv.read_bytes()
    print(f"Read {_rel_to_repo(target_csv)} ({len(original_bytes)} bytes, "
          f"SHA-256 {sha256_hex(original_bytes)})")

    # Detect which (receptor, decoy_lig) keys exist in the Tier 1 CSV.
    tier1_decoy_keys: set[tuple[str, str]] = set()
    for line in original_lines[1:]:
        if not line.strip():
            continue
        key = parse_row_key(line)
        if key is not None and key[1] == "decoy_lig":
            tier1_decoy_keys.add(key)

    # Harvest real ligands from both CSVs.
    tier3_lines: list[str] = []
    if tier3_csv.exists():
        tier3_lines = read_ligand_set_lines(tier3_csv)
        tier3_bytes = tier3_csv.read_bytes()
        print(f"Read {_rel_to_repo(tier3_csv)} ({len(tier3_bytes)} bytes, "
              f"SHA-256 {sha256_hex(tier3_bytes)})")
    else:
        print(f"[warn] Tier 3 CSV not found at {tier3_csv} — Tier 3 empty")

    real_by_receptor = harvest_real_ligands(
        original_lines, tier3_lines,
        origin_tags=("tier1", "tier3"),
    )

    # Track parse failures across all receptors for the reports.
    parse_failures: list[tuple[str, str, str]] = []
    for receptor, real_list in real_by_receptor.items():
        for r in real_list:
            if r["parse_error"] is not None and not r["is_peptide"]:
                parse_failures.append((receptor, r["name"], r["smiles"]))

    # ---- Small-molecule decoys (Tier 1 + Tier 3) -----------------------
    decoy_rows_by_key: dict[tuple[str, str], dict[str, str]] = {}
    tier1_reports: list[dict] = []
    tier3_reports: list[dict] = []

    for receptor, (smi, name, source) in DECOY_SMILES.items():
        real = real_by_receptor.get(receptor, [])
        report, row = _build_small_mol_report(receptor, smi, name, source, real)
        key = (receptor, "decoy_lig")
        if key in tier1_decoy_keys:
            decoy_rows_by_key[key] = row
            tier1_reports.append(report)
        else:
            tier3_reports.append(report)

    # ---- Peptide decoys -------------------------------------------------
    peptide_tier1_reports: list[dict] = []
    peptide_tier3_reports: list[dict] = []

    for receptor, (native_seq, common_name, salt) in PEPTIDE_DECOYS.items():
        reals = real_by_receptor.get(receptor, [])
        key = (receptor, "decoy_lig")
        is_tier1 = key in tier1_decoy_keys
        # If the receptor has no real-ligand rows AT ALL in either CSV,
        # skip (e.g. GLP1R after Step 1.5 drop — no ligand_set.csv row,
        # and Class B not in ligand_set_tier3.csv).
        if not reals:
            print(f"[info] {receptor}: no real-ligand rows found, peptide decoy skipped")
            continue
        result = _build_peptide_report(
            receptor=receptor,
            native_seq=native_seq,
            common_name=common_name,
            salt=salt,
            reals=reals,
            require_native_in_csv=is_tier1,
        )
        if result is None:
            # Tier 1 legacy gate (e.g. GLP1R after Step 1.5 drop) — skip.
            print(f"[info] {receptor}: no CSV decoy_lig row, peptide decoy skipped")
            continue
        report, row = result
        if is_tier1:
            decoy_rows_by_key[key] = row
            peptide_tier1_reports.append(report)
        else:
            peptide_tier3_reports.append(report)

    # ---- Rewrite Tier 1 CSV --------------------------------------------
    new_lines, _ = rewrite_ligand_set(original_lines, decoy_rows_by_key)
    changed = verify_non_decoy_byte_integrity(
        original_lines, new_lines, set(decoy_rows_by_key.keys())
    )
    if changed:
        raise RuntimeError(
            "byte-integrity check failed on non-decoy rows: "
            + ", ".join(changed)
            + " — aborting; refs/ligand_set.csv not modified."
        )

    new_text = "".join(new_lines)
    new_bytes = new_text.encode("utf-8")
    print(
        f"New ligand_set.csv would be {len(new_bytes)} bytes, "
        f"SHA-256 {sha256_hex(new_bytes)}"
    )

    # Legacy back-compat: emit_verification_md needs a glp1r_report if the
    # GLP1R peptide row was actually built. When it's gated off (Step 1.5
    # drop), fall through with a stub.
    if peptide_tier1_reports:
        # First (and only) Tier 1 peptide is legacy GLP1R.
        glp1r_report = peptide_tier1_reports[0]
    else:
        glp1r_report = None

    # ---- Emit Tier 1 verification MD -----------------------------------
    if dry_run:
        scratch_stub = Path(tempfile.gettempdir()) / (
            f"block_c_decoys_{glp1r_report['seed'] if glp1r_report else 'nolegacy'}"
        )
        scratch_md = scratch_stub.with_suffix(".md")
        emit_verification_md(tier1_reports, glp1r_report, parse_failures, scratch_md)
        print(f"[dry-run] Tier 1 verification MD written to {scratch_md}")
        scratch_csv = scratch_stub.with_suffix(".csv")
        scratch_csv.write_bytes(new_bytes)
        print(f"[dry-run] CSV written to {scratch_csv}")
        scratch_tier3 = scratch_stub.parent / (scratch_stub.name + "_tier3.md")
        emit_tier3_notes_md(
            tier3_reports, peptide_tier3_reports, parse_failures, scratch_tier3
        )
        print(f"[dry-run] Tier 3 notes MD written to {scratch_tier3}")
        return

    target_csv.write_bytes(new_bytes)
    print(f"Wrote {_rel_to_repo(target_csv)} ({len(new_bytes)} bytes)")
    emit_verification_md(tier1_reports, glp1r_report, parse_failures, target_md)
    print(f"Wrote {_rel_to_repo(target_md)}")
    emit_tier3_notes_md(
        tier3_reports, peptide_tier3_reports, parse_failures, target_tier3_md
    )
    print(f"Wrote {_rel_to_repo(target_tier3_md)}")


# ---------------------------------------------------------------------------
# Self-check: run twice, diff bytes.
# ---------------------------------------------------------------------------


def selfcheck() -> None:
    """Run build_all twice in a temp dir; assert byte-identical outputs
    for CSV + Tier 1 MD + Tier 3 MD; assert idempotency on rebuild."""
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        csv_a = td_path / "ligand_set_a.csv"
        csv_b = td_path / "ligand_set_b.csv"
        md_a = td_path / "decoy_verification_a.md"
        md_b = td_path / "decoy_verification_b.md"
        tier3_a = td_path / "S3_notes_a.md"
        tier3_b = td_path / "S3_notes_b.md"
        shutil.copyfile(LIGAND_SET_CSV, csv_a)
        shutil.copyfile(LIGAND_SET_CSV, csv_b)
        pre_bytes = LIGAND_SET_CSV.read_bytes()

        build_all(target_csv=csv_a, target_md=md_a, target_tier3_md=tier3_a)
        build_all(target_csv=csv_b, target_md=md_b, target_tier3_md=tier3_b)

        a_csv = csv_a.read_bytes()
        b_csv = csv_b.read_bytes()
        a_md = md_a.read_bytes()
        b_md = md_b.read_bytes()
        a_t3 = tier3_a.read_bytes()
        b_t3 = tier3_b.read_bytes()

        if a_csv != b_csv:
            raise RuntimeError(
                f"self-check FAIL: CSV bytes differ between runs "
                f"({sha256_hex(a_csv)} vs {sha256_hex(b_csv)})"
            )
        if a_md != b_md:
            raise RuntimeError(
                f"self-check FAIL: Tier 1 MD bytes differ between runs "
                f"({sha256_hex(a_md)} vs {sha256_hex(b_md)})"
            )
        if a_t3 != b_t3:
            raise RuntimeError(
                f"self-check FAIL: Tier 3 MD bytes differ between runs "
                f"({sha256_hex(a_t3)} vs {sha256_hex(b_t3)})"
            )

        # Idempotency: rebuild against the already-built csv_a.
        build_all(target_csv=csv_a, target_md=md_a, target_tier3_md=tier3_a)
        if (
            csv_a.read_bytes() != a_csv
            or md_a.read_bytes() != a_md
            or tier3_a.read_bytes() != a_t3
        ):
            raise RuntimeError("self-check FAIL: script is not idempotent")

        print(
            "self-check PASS: CSV + Tier 1 MD + Tier 3 MD byte-identical "
            "across two runs and idempotent on rebuild. pre-build "
            f"ligand_set.csv unchanged: "
            f"{'yes' if LIGAND_SET_CSV.read_bytes() == pre_bytes else 'NO — external write during selfcheck'}"
        )
        print(f"  ligand_set.csv (post-build)          SHA-256 {sha256_hex(a_csv)}")
        print(f"  decoy_verification.md (Tier 1)       SHA-256 {sha256_hex(a_md)}")
        print(f"  S3_decoy_construction_notes.md (T3)  SHA-256 {sha256_hex(a_t3)}")


def build_tier3_only(target_tier3_md: Path | None = None) -> None:
    """Compute Tier 3 verify-only outputs without touching ligand_set.csv.

    Uses a scratch CSV copy of ligand_set.csv so the Tier 1 rewrite side
    of build_all writes into tempdir rather than refs/. Emits the Tier 3
    curation notes MD to its target path.
    """
    target_tier3_md = target_tier3_md or TIER3_NOTES_MD
    with tempfile.TemporaryDirectory() as td:
        td_path = Path(td)
        scratch_csv = td_path / "ligand_set_scratch.csv"
        scratch_md = td_path / "decoy_verification_scratch.md"
        shutil.copyfile(LIGAND_SET_CSV, scratch_csv)
        build_all(
            target_csv=scratch_csv,
            target_md=scratch_md,
            target_tier3_md=target_tier3_md,
        )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="write outputs to a scratch dir instead of the repo paths")
    ap.add_argument("--selfcheck", action="store_true",
                    help="run twice against scratch copies and diff bytes")
    ap.add_argument("--tier3-only", action="store_true",
                    help="emit only the Tier 3 curation notes MD; do NOT "
                         "rewrite refs/ligand_set.csv")
    args = ap.parse_args(argv)
    if args.selfcheck:
        selfcheck()
        return 0
    if args.tier3_only:
        build_tier3_only()
        return 0
    build_all(dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
