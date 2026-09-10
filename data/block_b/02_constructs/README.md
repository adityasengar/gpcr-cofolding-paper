# 02_constructs/ — decoy + shuffled construct identity

## Files

- `donor_ga_class.csv` — 640 rows, one per (receptor × arm × backbone) cell.
  Columns: `receptor, arm, backbone, donor_ga_identity, donor_ga_class,
  cognate_ga_identity, cognate_ga_class`. Empty donor cells on apo (no partner
  chain). Phase 5 and Phase 6b depend on this table.
- `construct_build_report.md` — Phase 1b decoy construction narrative
  (byte-identical prefix, tail edit at α5-CT, Hamming ≥ 7).
- `decoy_scramble_verification.md` — Phase 1c shuffled arm wrong-family audit.
- `d2_arm_sequence_audit.csv` — Block D D2 arm-sequence audit
  (facts-only from Phase 6c; retained here for cross-block context, not
  Block-B-load-bearing).

## SC-B claims supported

- **SC-B-8** (construct identity verified on 40/40 receptors by content) — see
  `claim_answers.csv`.

Compensating control per C-B-12: `propose_py_git_sha` and
`build_manifest_py_git_sha` are empty in `manifest.provenance.json`; construct
identity is verified by content (byte-identical prefix, tail Hamming ≥ 7,
parent-Gα routing) not by generator revision.

## Source

Working repo: `experiments/019_block_b_partner_selection/analysis/`.
