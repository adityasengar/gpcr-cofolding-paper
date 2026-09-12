"""Bootstrap refs/reference_pdbs.csv from the frozen panel + explicit exclusions.

Runnable helper — not a scorer module. Reads
    /Users/SENGAAD1/Documents/claude/subsampling-cap-exp/inputs/reference_panel_v2.csv
and emits refs/reference_pdbs.csv as the input to `gpcr-refs build`.

Excluded PDBs (from docs/AUDIT_TRAIL.md and docs/REFERENCE_SET.md):
  5C1M   nanobody Nb39-stabilised (OPRM, wrong class)
  8UWL   scFv16 + lisuride (5HT2A, re-check class)
  8YN3   chain-B curation bug (HRH2)
  7T10   Tier-5 flagged (SSR2, replace with 7WIG)
  6HLP   Tier-5 flagged (NK1R, replace with 6E59)
  5WF5   non-discriminating pair (AA2AR w/ 4EIY)
  4EIY   non-discriminating pair (AA2AR w/ 5WF5)
  adrb1_melga  turkey species; use adrb1_human
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

SOURCE = Path("/Users/SENGAAD1/Documents/claude/subsampling-cap-exp/inputs/reference_panel_v2.csv")
OUT = Path("refs/reference_pdbs.csv")


# State-claim inference from active_ligand_function
LIGAND_TO_STATE = {
    "Agonist": "Ga-coupled-active",
    "Antagonist": "inactive-antagonist",
    "Inverse agonist": "inactive-inverse-agonist",
    "Partial agonist": "Ga-coupled-active",
    "Positive allosteric modulator": "Ga-coupled-active",
    "Negative allosteric modulator": "inactive-antagonist",
    "Allosteric agonist": "Ga-coupled-active",
    "Allosteric antagonist": "inactive-antagonist",
}


EXCLUSIONS: dict[str, str] = {
    "5C1M": "nanobody Nb39-stabilised; wrong-class conformational-selection artefact (audit #4)",
    "8UWL": "mini-Gq + scFv16 + lisuride; re-check class assignment (audit #2 polarity)",
    "8YN3": "chain-B curation bug — chain B was GLY-ILE fragment, not receptor",
    "7T10": "Tier-5 flagged; use 7WIG",
    "6HLP": "Tier-5 flagged; use 6E59",
    "5WF5": "AA2AR non-discriminating pair with 4EIY (1.7 Å apart)",
    "4EIY": "AA2AR non-discriminating pair with 5WF5",
}


SPECIES_EXCLUSION_SLUGS = {
    "adrb1_melga",  # turkey — refuse against human β1AR constructs
}


def slug_to_receptor(slug: str) -> str:
    """`adrb2_human` -> `ADRB2`. Handles digit-prefix slugs like 5ht2a."""
    stem = slug.split("_")[0]
    return stem.upper()


def slug_to_species(slug: str) -> str:
    parts = slug.split("_")
    if len(parts) < 2:
        return "human"
    return parts[-1]


def infer_state_claim(role: str, ligand_function: str) -> str:
    if role == "active":
        return LIGAND_TO_STATE.get(ligand_function, "Ga-coupled-active")
    # inactive
    return LIGAND_TO_STATE.get(ligand_function, "inactive-antagonist")


def main() -> int:
    if not SOURCE.exists():
        print(f"source not found: {SOURCE}", file=sys.stderr)
        return 2
    rows_out: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    with SOURCE.open() as f:
        reader = csv.DictReader(f)
        for r in reader:
            slug = r["receptor"].strip()
            receptor = slug_to_receptor(slug)
            species = slug_to_species(slug)
            for role, pdb_col, func_col in [
                ("active", "active_pdb", "active_ligand_function"),
                ("inactive", "inactive_pdb", "inactive_ligand_function"),
            ]:
                pdb = (r.get(pdb_col) or "").strip().upper()
                if not pdb:
                    continue
                state = infer_state_claim(role, r.get(func_col, ""))
                excluded = "false"
                reason = ""
                if pdb in EXCLUSIONS:
                    excluded = "true"
                    reason = EXCLUSIONS[pdb]
                elif slug in SPECIES_EXCLUSION_SLUGS:
                    excluded = "true"
                    reason = f"species {species!r} — refuse against human construct"
                key = (receptor, role, pdb)
                if key in seen:
                    continue
                seen.add(key)
                rows_out.append({
                    "receptor_slug": receptor,
                    "role": role,
                    "pdb_id": pdb,
                    "uniprot_slug": slug,
                    "species": species,
                    "candidate_state": state,
                    "stabilising_elements_manual": "",  # detected at build time
                    "excluded": excluded,
                    "excluded_reason": reason,
                    "notes": "",
                })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="") as f:
        cols = [
            "receptor_slug", "role", "pdb_id", "uniprot_slug", "species",
            "candidate_state", "stabilising_elements_manual",
            "excluded", "excluded_reason", "notes",
        ]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for row in rows_out:
            w.writerow(row)
    print(f"wrote {OUT} with {len(rows_out)} rows "
          f"({sum(1 for r in rows_out if r['excluded'] == 'true')} excluded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
