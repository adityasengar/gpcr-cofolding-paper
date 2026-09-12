"""Apply the A4 schema fix (from commit 6019431) to refs/reference_pdbs.csv.

Commit 6019431 fixed 16 role/state mismatches in refs/reference_set.csv
DIRECTLY but never propagated the corrections back to the source
refs/reference_pdbs.csv. Regenerating reference_set.csv via
`refs_build build` would therefore regress those 16 rows to the pre-A4
state. This script re-applies the same 16 corrections to the source.
"""
import csv
from pathlib import Path

CORRECTIONS = {
    ("5HT1B", "inactive", "4IAR"): {"candidate_state": "inactive-antagonist"},
    ("5HT2A", "inactive", "7WC8"): {"candidate_state": "inactive-antagonist"},
    ("ACM1",  "inactive", "6ZFZ"): {"candidate_state": "inactive-antagonist"},
    ("APJ",   "inactive", "8S4D"): {"candidate_state": "inactive-antagonist"},
    ("CXCR3", "inactive", "8K2W"): {"candidate_state": "inactive-antagonist"},
    ("EDNRB", "inactive", "6IGK"): {"candidate_state": "inactive-antagonist"},
    ("GPR52", "inactive", "6LI0"): {"candidate_state": "inactive-antagonist"},
    ("GPR6",  "active",   "8TF5"): {"role": "inactive"},
    ("MTR1A", "inactive", "6ME2"): {"candidate_state": "inactive-antagonist"},
    ("MTR1B", "inactive", "6ME6"): {"candidate_state": "inactive-antagonist"},
    ("NTR1",  "inactive", "6YVR"): {"candidate_state": "inactive-antagonist"},
    ("SSR2",  "inactive", "7XN9"): {"candidate_state": "inactive-antagonist"},
    ("CASR",  "inactive", "8WPG"): {"candidate_state": "inactive-antagonist"},
    ("GP156", "inactive", "8IEP"): {"candidate_state": "inactive-antagonist"},
    ("SMO",   "inactive", "8CXO"): {"candidate_state": "inactive-antagonist"},
    ("T2R14", "inactive", "9IJA"): {"candidate_state": "inactive-antagonist"},
}

p = Path("refs/reference_pdbs.csv")
with p.open() as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

hits = 0
for r in rows:
    key = (r["receptor_slug"], r["role"], r["pdb_id"])
    if key in CORRECTIONS:
        for k, v in CORRECTIONS[key].items():
            r[k] = v
        hits += 1

assert hits == 16, f"expected 16 hits, got {hits}"

with p.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for r in rows:
        w.writerow(r)

print(f"Applied {hits} A4 schema corrections to refs/reference_pdbs.csv")
