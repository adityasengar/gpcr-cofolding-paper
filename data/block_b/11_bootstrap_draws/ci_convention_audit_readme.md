# CI Bootstrap-convention Audit — SC-B-1 (Item 2 of the closeout dispatch)

The post-freeze report (r2) compared cluster-boot [0.445, 0.664] against
a tighter [0.51, 0.60] and inferred "2× width ratio, some SC-B claims
will unsign". Item 2 recomputation shows the tighter interval was
row-boot (8000 decoy rows treated independent), NOT proper receptor-boot.

Proper receptor-boot over 40 receptors gives:

| arm | point | receptor_boot CI | cluster_boot CI | width_ratio_c/r |
|---|---:|---|---|---:|
| apo | 0.158 | [0.094, 0.233] | [0.083, 0.259] | 1.26 |
| decoy | 0.558 | [0.456, 0.652] | [0.450, 0.672] | 1.13 |
| shuffled | 0.809 | [0.735, 0.870] | [0.746, 0.870] | 0.92 |
| cognate | 0.891 | [0.828, 0.947] | [0.833, 0.940] | 0.90 |

Width ratios are 0.90–1.26, not 2×. **No SC-B claim's signed status
changes under cluster-boot vs proper receptor-boot.** Cluster-boot
remains authoritative per Block A's C-8 convention (Block A parity);
the r2 note about "2× wider" was based on comparing cluster-boot
against a mislabeled row-boot.

Full audit rows in `ci_convention_audit_sc_b_1.csv`.
