# BW numbering source

**One sanctioned source, always:** GPCRdb `services/residues/extended/<entry>/`.
Fetched per-PDB, cached under `refs/cache/gpcrdb/`.

Ported verbatim from `github.com/adityasengar/gpcr-structure-pipeline` (see
`docs/AUDIT_TRAIL.md` for the frozen conventions we do **not** carry).

`bw_derivation_source` on every row takes one of exactly two values:

- `"gpcrdb:services/residues/extended"` — GPCR inputs (Class A/B/C receptors)
- `"uniprot_canonical:calmodulin_human"` — CaM inputs (via `scorer/noncanonical.py`)

Adding a third value requires a corresponding entry in `scorer/anchors.py` /
`scorer/noncanonical.py` and a test in `tests/`. There is no free-text path.

Detail: filled at commit 4.
