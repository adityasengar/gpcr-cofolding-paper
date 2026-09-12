"""Mark 43 reference_pdbs.csv rows as excluded=true because they produced
NaN d_r350_r630_ca_ref in refs_build.

Motivation: the Finding #7 tripwire in scorer/refs_build.py raises when
any curated row measures NaN — this is the "silent-drop" class of bug
the scorer exists to eliminate. Rows that legitimately measure NaN
because their receptor's canonical Class-A axis doesn't apply
(Class B / C / F / adhesion / olfactory / T2R) or because the specific
PDB has a disordered 6.30 CA must be marked excluded so the tripwire
sees them as explicit exclusions rather than silent NaN emissions.

Categorisation (from HPC refs_build.34897946.log 2026-08-27):

  class_bcf_no_canonical_class_a_axis — 26 rows
    Class B / C / F / adhesion / orphan olfactory / T2R receptors whose
    natural residues at 3.50 / 5.58 / 6.30 / 7.53 do not carry the
    Class-A ionic-lock or NPxxY chemistry. The CA-CA axis can be
    computed geometrically but has no consistent activation-state
    correlation across the family.

  pdb_specific_anchor_disorder — 17 rows
    Class A receptor where the specific PDB has 6.30 CA disordered or
    excised by a fusion (T4L, BRIL, GFP replacing ICL3). Alternative
    PDBs for the same receptor may score cleanly if curated.
"""
import csv
from pathlib import Path

CLASS_BCF = "class_bcf_no_canonical_class_a_axis"
PDB_SPECIFIC = "pdb_specific_anchor_disorder"

# (receptor_slug, role, pdb_id) → excluded_reason
EXCLUSIONS: dict[tuple[str, str, str], str] = {
    # Class B / C / F / adhesion / orphan-family
    ("AGRE5", "active",   "8IKL"): CLASS_BCF + "; adhesion GPCR",
    ("AGRE5", "inactive", "8IKJ"): CLASS_BCF + "; adhesion GPCR",
    ("AGRL3", "active",   "7SF7"): CLASS_BCF + "; adhesion GPCR",
    ("AGRL3", "inactive", "8JMT"): CLASS_BCF + "; adhesion GPCR",
    ("CALRL", "active",   "6UVA"): CLASS_BCF + "; Class B (calcitonin receptor-like)",
    ("CALRL", "inactive", "7KNT"): CLASS_BCF + "; Class B (calcitonin receptor-like)",
    ("CASR",  "active",   "7M3G"): CLASS_BCF + "; Class C (calcium-sensing)",
    ("CASR",  "inactive", "8WPG"): CLASS_BCF + "; Class C (calcium-sensing)",
    ("GABR2", "active",   "7C7Q"): CLASS_BCF + "; Class C (GABA-B2)",
    ("GABR2", "inactive", "7C7S"): CLASS_BCF + "; Class C (GABA-B2)",
    ("GLP1R", "active",   "6X18"): CLASS_BCF + "; Class B (glucagon-like peptide 1)",
    ("GLR",   "active",   "8WG8"): CLASS_BCF + "; Class B (glucagon)",
    ("GLR",   "inactive", "5EE7"): CLASS_BCF + "; Class B (glucagon)",
    ("GP156", "active",   "8IED"): CLASS_BCF + "; adhesion/orphan",
    ("GP156", "inactive", "8IEP"): CLASS_BCF + "; adhesion/orphan",
    ("GRM2",  "active",   "8JD2"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("GRM2",  "inactive", "7EPE"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("GRM3",  "active",   "8TQB"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("GRM3",  "inactive", "8TR0"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("GRM4",  "active",   "8JD6"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("GRM4",  "inactive", "8WGD"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("GRM5",  "active",   "8TAO"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("GRM5",  "inactive", "6FFI"): CLASS_BCF + "; Class C (metabotropic glutamate)",
    ("O52E4", "active",   "8HTI"): CLASS_BCF + "; olfactory receptor family",
    ("O52E4", "inactive", "8W77"): CLASS_BCF + "; olfactory receptor family",
    ("PTH1R", "active",   "8FLQ"): CLASS_BCF + "; Class B (parathyroid hormone)",
    ("T2R14", "active",   "8VY7"): CLASS_BCF + "; T2R bitter-taste family",
    ("T2R14", "inactive", "9IJA"): CLASS_BCF + "; T2R bitter-taste family",
    # PDB-specific 6.30 disorder or fusion excising 6.30
    ("ADA1A", "active",   "8THK"): PDB_SPECIFIC + "; 6.30 CA disordered",
    ("C5AR1", "active",   "7Y67"): PDB_SPECIFIC + "; scFv-stabilised, 6.30 CA disordered",
    ("C5AR1", "inactive", "6C1R"): PDB_SPECIFIC + "; 6.30 CA disordered",
    ("CCR2",  "inactive", "6GPX"): PDB_SPECIFIC + "; 6.30 CA disordered",
    ("CCR6",  "inactive", "9D3E"): PDB_SPECIFIC + "; BRIL fusion, 6.30 CA disordered",
    ("CCR8",  "inactive", "8TLM"): PDB_SPECIFIC + "; GFP fusion excises 6.30",
    ("CXCR3", "inactive", "8K2W"): PDB_SPECIFIC + "; nanobody-stabilised, 6.30 CA disordered",
    ("DRD4",  "active",   "8IRU"): PDB_SPECIFIC + "; 6.30 CA disordered",
    ("GPR52", "active",   "8HMP"): PDB_SPECIFIC + "; orphan, 6.30 CA disordered",
    ("GPR52", "inactive", "6LI0"): PDB_SPECIFIC + "; orphan, 6.30 CA disordered",
    ("MTR1A", "active",   "7VGY"): PDB_SPECIFIC + "; melatonin receptor, 6.30 CA disordered",
    ("MTR1B", "active",   "7VH0"): PDB_SPECIFIC + "; melatonin receptor, 6.30 CA disordered",
    ("NTR1",  "inactive", "6YVR"): PDB_SPECIFIC + "; rat NTR1, 6.30 CA disordered",
    ("NTR1",  "inactive", "7UL2"): PDB_SPECIFIC + "; rat NTR1 + nanobody, 6.30 CA disordered",
    ("S1PR1", "inactive", "3V2Y"): PDB_SPECIFIC + "; T4L fusion, 6.30 CA disordered",
}

assert len(EXCLUSIONS) == 43, f"expected 43 rows, got {len(EXCLUSIONS)}"


def main() -> int:
    src = Path("refs/reference_pdbs.csv")
    with src.open() as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    hits = 0
    already_excluded = 0
    for r in rows:
        key = (r["receptor_slug"], r["role"], r["pdb_id"])
        if key not in EXCLUSIONS:
            continue
        if (r.get("excluded") or "").strip().lower() == "true":
            already_excluded += 1
            continue
        r["excluded"] = "true"
        r["excluded_reason"] = EXCLUSIONS[key]
        hits += 1

    with src.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"marked {hits} rows excluded=true "
          f"({already_excluded} were already excluded, skipped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
