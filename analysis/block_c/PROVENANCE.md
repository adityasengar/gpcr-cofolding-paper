# Block C — provenance of the drop

Landed 2026-09-10. Hashes checked **before** extraction.

| bundle | SHA-256 | verdict |
|---|---|---|
| `block_c_figure_data.zip` | `2c3af76441882654128884ef73b15b32a8ad664b8472ab211c9dc13ff1751da9` | **matches the dispatch's expected current SHA** |
| `block_c_structures.zip` | `1375f5e9f3c145e650991ff4bdb04edbb39efffb49001f96937ed948c858b01b` | **not named anywhere in the dispatch** — see below |

70 files, matching the dispatch's stated count. Landed at `data/block_c/`,
`chmod a-w`.

## The two SHAs the dispatch warns about

- **NOT** `1394405a…` — the invalid v1 that predates the cluster-boot recompute
  and the corrected off-site census. We do not hold it; checked every zip in
  `~/Downloads` and the repo.
- **NOT** `b6e820ad…` — the same content minus the 14 CIFs. Ours has
  `13_structures/targeted/` and `13_structures/random/` populated with 14 `.cif`
  files, which the dispatch says is the test that matters regardless of SHA.

## The unannounced second zip

`block_c_structures.zip` appears in no part of the dispatch, which places the
structures inside the main bundle at `13_structures/`. It is **fully redundant**:
16 files, rooted at `block_c/` instead of `13_structures/`, and every one is
**byte-identical** to its counterpart in the main bundle — verified by SHA-256,
16 identical, 0 differing, 0 extra.

It has not been ingested. Nothing reads from it. Recorded here so that a future
session finding two Block C zips does not have to re-derive which is
authoritative: **the main bundle is, and the second adds nothing.**

Worth asking upstream why it was sent, in case it was meant to be a *different*
set of structures and the wrong file was attached.

## Note on the bundle's own index

The dispatch's §4(n) says `README.md` undercounts `13_structures/` as 2 files
when there are 16. Confirmed: 14 CIFs plus README and MANIFEST are present. The
index is stale, not the data.

## What is committed

Tabular and narrative content is committed so every number traces to a shipped
file. Not committed: the two zips (kept at the repo root for re-extraction) and
`data/block_c/13_structures/**/*.cif`. Same rule as Blocks A and B.
