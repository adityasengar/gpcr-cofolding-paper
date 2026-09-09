# C-6 — Reference PDB set is 89 unique, not 48

## Caveat

The campaign panel is 48 receptors. Naive framing might suggest 48
reference PDBs (one per receptor). The actual reference PDB set for Block
A is **89 unique PDBs** — 41 unique active + 48 unique inactive (some
receptors share the same PDB as their active reference where the same
structure represents multiple receptors; inactive references are unique
per receptor).

The `refs/cache/pdb/` directory on-disk holds 92 CIFs including two
fetched read-only during Phase 5 (6LMK, 6P9X) plus one PDB that is
referenced but historically has been swapped once.

## Affects

- Any manuscript sentence enumerating the reference set — "48 reference
  structures" is wrong; "89 unique reference PDBs" is right.
- Downstream blocks (Block C tier 3 adds antagonist references and Class
  F alternative active poses; D-tier may add).

## Evidence

- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md` §Phase 1d
- `panel/refs/reference_set.csv` (on-disk, 89 unique PDBs across active+inactive columns for the 48-receptor Block A panel)

## Manuscript sentence

> The reference structure set for Block A comprises 89 unique
> Protein Data Bank entries: 41 unique active-state references (some
> receptors share the same structural context) and 48 unique inactive-
> state references. All references are frozen as
> `panel/refs/reference_set.csv` with row-level `ref_pdb_sha_active` and
> `ref_pdb_sha_inactive` SHAs in the corpus data.
