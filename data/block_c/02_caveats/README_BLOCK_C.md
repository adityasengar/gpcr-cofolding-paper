# Block C caveats

Live limitations, distinct from withdrawals (which are retracted
claims from earlier draft versions — see `withdrawals/`).

Naming: `C-C-<n>_<slug>.md`. Block C prefix keeps them separate from
Block A's `C-<n>` and Block B's `C-B-<n>`.

| ID | Slug | Scope |
|---|---|---|
| C-C-1 | predicate_saturation_block_c | Binary two-instrument predicate ceiling/floor-pinned on Block C |
| C-C-2 | chai_softness_block_c | Chai AUROC softness + backbone-heterogeneous magnitudes |
| C-C-3 | 2x2_ci_convention_pending | Cluster-boot CI on 2×2 interaction not recomputed in this pass |
| C-C-4 | agtr1_biased_agonist_reference | AGTR1 active ref is unique category-d biased-agonist nanobody |
| C-C-5 | s1_receptor_count_pinned_15 | KILL-S1 n=15 not 14 (prereg subtraction error) |
| C-C-6 | matcher_path_ligand_only | Matcher affects only ligand_rmsd, not pocket_ca |
| C-C-7 | cxcr4_apo_pocket_reference | CXCR4's active ref has apo orthosteric pocket |
| C-C-8 | coverage_asymmetry | Agonist ~50% NaN vs antag ~93% coverage on ligand_rmsd |
| C-C-9 | panel_36_of_40_landed | 36 Class A landed of 40 dispatched |
| C-C-10 | role_routing_label_vs_resolution | Routing labels differ, resolved PDBs identical |
| C-C-11 | deferred_gates | G2d / G4 / G5 / G6b / G7 / 2×2 cluster-boot recompute deferred |

**Companion**: `withdrawals/README_BLOCK_C.md` for 10 retracted-claim
records. Manuscript §Withdrawn enumerates the same 10 in
`docs/BLOCK_C_PAPER_DRAFT_v1.md`.
