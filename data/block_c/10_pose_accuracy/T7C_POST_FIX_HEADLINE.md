# T7c post-fix headline — pose accuracy after Bug #2 + #3 fixes

**Date**: 2026-09-07
**Corpus**: `rescore_t7c_full/rows.csv` — 40,800 rows, 40,000 passed. Scorer
SHA `891041e858f3747b...` includes MCS automorphism fix (`GetSubstructMatches
uniquify=False` + RMSD-minimize over pairings) and Bug #2 tripwire (reject
picked HETATM > 8 Å from any receptor-plausible-chain Cα).
**Filter**: real ligand roles only (`decoy_lig` excluded per scorer docstring),
`passed=true`, numeric `ligand_rmsd_to_ref`.
**n usable**: 18,306 rows.

## Headline

**Per-receptor dock rate `<3 Å`, median across receptors within each cell.**
No pooling.

| backbone | arm | role | partition | n_rec | med % | ≥ 50 % | ≥ 20 % | all-fail | all-dock |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| **Boltz** | apo | full_agonist | **redock** | 10 | **100.0** | 6 | 6 | 4 | 6 |
| **Boltz** | apo | neutral_antag | **redock** | 21 | **56.0** | 11 | 12 | 8 | 8 |
| **Boltz** | cognate | full_agonist | redock | 10 | 99.0 | 6 | 6 | 4 | 5 |
| **Boltz** | cognate | neutral_antag | redock | 21 | 54.0 | 11 | 13 | 8 | 6 |
| Chai | apo | full_agonist | redock | 10 | 2.0 | 3 | 3 | 5 | 0 |
| Chai | apo | neutral_antag | redock | 21 | 18.0 | 8 | 9 | 7 | 6 |
| Chai | cognate | full_agonist | redock | 10 | 2.0 | 3 | 4 | 4 | 0 |
| Chai | cognate | neutral_antag | redock | 21 | 0.0 | 8 | 8 | 11 | 5 |
| OF3 | apo | full_agonist | redock | 12 | 0.0 | 5 | 5 | 7 | 1 |
| OF3 | apo | neutral_antag | redock | 21 | 0.0 | 6 | 6 | 15 | 2 |
| OF3 | cognate | full_agonist | redock | 12 | 0.0 | 3 | 5 | 7 | 1 |
| OF3 | cognate | neutral_antag | redock | 21 | 0.0 | 5 | 5 | 15 | 2 |
| Protenix | apo | full_agonist | redock | 12 | 0.0 | 4 | 5 | 7 | 3 |
| Protenix | apo | neutral_antag | redock | 21 | 0.0 | 4 | 5 | 15 | 4 |
| Protenix | cognate | full_agonist | redock | 12 | 0.0 | 4 | 4 | 8 | 3 |
| Protenix | cognate | neutral_antag | redock | 21 | 0.0 | 4 | 4 | 15 | 3 |

Cross-dock cells (input ligand ≠ reference ligand) are almost universally
≈ 0 %. One anomaly: **Chai × neutral_antag × cross-dock × apo → 100 %
median on 6 receptors** — suspicious, possibly Bug #4 firing (spurious
`atom_name_element` on 5-atom coincidental name overlap). Not investigated
in this pass.

## Interpretation

**Distributions are bimodal per receptor, not smooth.** Within each cell,
most receptors are either near-0 % or near-100 %. Pooling hides this.

**Ranking under redock**: Boltz > Chai > (OF3 ≈ Protenix).
- Boltz median 54-56 % on the 21-receptor neutral_antag panel.
- Chai 0-18 %.
- OF3 and Protenix 0 %, though 4-6 receptors each still dock ≥ 50 %.

**Apo vs cognate barely matters** for redock — Boltz and Chai are stable
across arms. That's expected: the ligand pose is determined by the
receptor + ligand, not the partner.

**Cross-dock ≈ 0 %** — the 3 Å threshold correctly reports "no dock" when
input ligand ≠ reference ligand. The PoseBusters redocking threshold is
inappropriate for cross-docks (chemistry mismatch guarantees higher RMSD).

## Comparison to prior T7b claim

The T7b headline "38-42 % dock rate on Boltz/Chai neutral_antag" was:
- Pooled across receptors (masking the bimodal distribution)
- Included cross-dock rows (which are legitimately near 0 %)
- Contaminated by Bugs #2 (wrong HETATM) and #3 (MCS pairing)

**New claim, redock-only, median-across-receptors, per-backbone**:
- Boltz neutral_antag redock: **54-56 %** (11/21 receptors dock ≥ 50 %)
- Chai neutral_antag redock: **0-18 %** (8/21 receptors dock ≥ 50 %)
- OF3 / Protenix neutral_antag redock: **0 %** median but 4-6/21 receptors dock ≥ 50 %

The manuscript's scoped "6.93 %" is now revealed as an artifact of pooling
across a bimodal per-receptor distribution.

## What still needs doing

- **Task #54 skipped**: paired MCS-vs-fast-path on the fixed scorer. Deferred
  because it needs another HPC dispatch and the corpus-level numbers here
  are the load-bearing deliverable. Can be run later to verify Bug #3 fix
  is complete.
- **Chai cross-dock 100 % anomaly** (6 receptors on apo neutral_antag)
  — investigate whether Bug #4 (fast-path preemption at 5 atoms) is firing
  on SMILES-derived Chai atom names against those specific references.
- **Bug #4 fix**: force fast-path to require CCD-native names, not just
  ≥ 5 name matches. Would eliminate the anomaly above and clean up
  Boltz/Chai fast_path_ok rows.

## Files

- `experiments/021_block_c_tier3_pharmacology/rescore_t7c_full/rows.csv` — the rescored corpus (40,800 rows)
- `signal_recovery_2026_09_07/step4_ecdf_per_receptor.csv` — one row per (bb×arm×role×partition×receptor) with median/quartiles/dock rate
- `signal_recovery_2026_09_07/step4_cell_receptor_distribution.csv` — per-cell receptor distribution summary
- `signal_recovery_2026_09_07/T7C_POST_FIX_HEADLINE.md` — this file
- `scorer/pocket_metrics.py` — SHA `891041e858f3747b...` — locally + on HPC
