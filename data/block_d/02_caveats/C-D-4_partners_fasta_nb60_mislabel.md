# C-D-4 — `partners.fasta:Nb60` was a 126-aa Nb80 sequence (removed 2026-09-10)

## Caveat

`docs/EXPERIMENT_CATALOG/sequences/partners.fasta` carried an entry
keyed `>Nb60` with a 126-aa sequence (sha `b9ad1bad…`) whose CDR3
matches Nb80 (from PDB 3P0G, Rasmussen 2011), not Nb60 (from PDB
5JQH, Staus 2016). Mis-labeled.

**Never consumed by any D2 arm** (GATE-1 row-hash audit). D2 sources
nanobody sequences from `refs/nanobody_sequences.fasta` (the
dedicated Nb FASTA), NOT from `docs/EXPERIMENT_CATALOG/sequences/partners.fasta`
(which is set up for Gα family partners: alphas, alphai1, alphaq,
alpha13, alphagust, GP161, arrestin_FL). The mislabelled entry was
the only nanobody entry in `partners.fasta`.

**Resolution 2026-09-10** (joint-review §6.6): the entry was
removed from `partners.fasta` rather than renamed to `Nb80`. Rationale:
`partners.fasta` is set up for Gα family + arrestin partners; nothing
else in it is a nanobody; removing is cleaner than relabeling a stray
entry. The Nb80 sequence is preserved in provenance memory
`block_d_d2_nanobody_collision_2026_09_09.md` and in the audit CSV
`experiments/019_block_b_partner_selection/analysis/d2_arm_sequence_audit.csv`.

Documentation defect; no data-integrity impact.

## References

- `gates/GATE_1_D2_NB_SHA.md` — verifying no D2 arm consumed the mislabel.
- Working-repo memory `block_d_d2_nanobody_collision_2026_09_09.md` — the mislabel provenance.
- `experiments/019_block_b_partner_selection/analysis/d2_arm_sequence_audit.csv` — per-arm SHA audit trail.
