# approved_2026_09_12 — the files Aditya approved, delivered by hand

**Arrived 2026-09-12 as `paper6f_approved_2026_09_12.zip`**, sha256
`7bafbbc96c1631c787ca683621e93f94356e942a95a97134c61c5cceac1c5c69`.

**Why by hand.** `paper_af3` reported that Aditya approved all four asks in their
session, but their platform's classifier then refused **every** outbound file
regardless of size — `ligand_set.csv` at 33 KB was denied exactly as the large one
was. The approval was real and the delivery was blocked, which is a different
situation from the apo table. **Nobody looked for a way around that classifier**;
the files came from Aditya directly instead.

**What is here, and what is not.**

| file | rows | answers |
|---|---:|---|
| `ligand_set.csv` | 40 | ask 2 |
| `ligand_set_tier3.csv` | 64 | ask 2 |
| `derive_per_class_thresholds.py` | — | ask 4, **partly** |

`reference_set.csv` was in the zip and is **byte-identical to the copy already at
`../source_bundle/refs/reference_set.csv`**, so it is not duplicated here. That
identity is itself useful: it confirms the copy we already held is the threshold
fit input.

**Ask 1 is not here and was never going to be.** `rows.tier3.v2.csv` is 92 MB /
40,801 rows / ~100 columns. It moves as an agreed **ten-column projection**
including `ligand_type` — see `DECISIONS.md` F-17.

**Read `DECISIONS.md` F-18 before using any of this.** Two things matter: the
script does **not** derive the Class A thresholds, and one of the 104 ligand rows
is malformed.
