# C-D-11 — MCHR1 D3 ligand_rmsd_to_ref: reconciled (closed)

## Caveat

**Status: CLOSED / reconciled 2026-09-10.** Retained here for the
audit trail.

**Original conflict**: GATE-4 flagged 990 rows of D3 populated with
`ligand_rmsd_to_ref` values, all on MCHR1 — a D3 receptor that is
apo-only (no small-molecule ligand path should fire). Part-A-D3
disputed the finding with an independent empirical count showing 100
% NaN across all 25,810 D3 rows.

**Reconciliation** (this Block D closeout pass): empirical recount
on the on-disk `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv`
returned **25,810 / 25,810 rows NaN** on `ligand_rmsd_to_ref`; 0
populated. **Part-A-D3 is correct**; GATE-4's 990 claim is retracted.

**Consequence**: GATE-4's downstream verdict — Bug #4 (`9e640d5`
fast-path coverage guard in `scorer/pocket_metrics.py::ligand_rmsd_to_ref`)
is `NOT MATERIAL` to D-tier — stands unchanged. The ligand path never
fires on any D-tier row by construction (D1/D3 are apo-only; D2 has
partner chains but no small-molecule ligands relevant to
`ligand_rmsd_to_ref`).

Downgraded from active caveat to closed-reconciliation note. No
downstream flag; no manuscript-side action needed.

## References

- `dossiers/BLOCK_D/gates/GATE_4_SCORER_DIFF.md` §Bug #4 relevance verdict.
- `dossiers/BLOCK_D/partA/PARTA_D3.md` §6 (MCHR1 investigation).
- Empirical recount 2026-09-10 (Block D closeout).
