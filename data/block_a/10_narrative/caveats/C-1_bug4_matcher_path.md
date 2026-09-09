# C-1 — Bug #4 matcher-path scope

## Caveat

`scorer/pocket_metrics.py::ligand_rmsd_to_ref` has a 5-atom-name-overlap
fast-path that preempts MCS matching. On Block C tier 3 (40,800 rows),
approximately 2,300 rows land on the fast path rather than the
MCS-safe path. Any pose-accuracy claim over the pooled 40,800 rows
carries mixed matcher paths.

## Affects

- Block C tier 3 pose-accuracy claims (`ligand_rmsd_to_ref` distribution).
- Any downstream claim that pools across the T7c full corpus without
  gating on `pocket_ligand_atom_map_method`.
- **NOT affected**: Block A (no ligand). Block B (no ligand). D1/D2/D3
  (nanobody / partner selection / MSA depth — non-ligand).

## Evidence

- Auto-memory `docking_measurement_bug_hunt_2026_09_07.md`
- `dossiers/BLOCK_A` §RESURFACED (flagged forward)
- Fix landed at commit `48ddfc1` for three related bugs (Gα-atoms-in-pool,
  largest-HETATM-picked, MCS-not-automorphism-safe); Bug #4 fast-path is
  still open

## Manuscript sentence

> Pocket-Cα-RMSD is used as the primary pose axis; ligand-side
> `ligand_rmsd_to_ref` is reported as a secondary axis for OF3 and
> Protenix on ref-matched cells (n=4,500) — Chai and Boltz atom-name
> conventions preempt the MCS-safe matcher path on approximately 2,300
> rows in the pooled corpus.
