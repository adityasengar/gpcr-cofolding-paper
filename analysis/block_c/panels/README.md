# Block C panel specs

**Specs, not images**, per the dispatch §6: no PNG, PDF or SVG, one panel per
file, spec ID only, no manuscript figure number, and no main-versus-SI call.

**All four are built**, and each states its evidential class on its own face.
An earlier version of this file said three of them could not be, because
`rows.tier3.v2.csv` was not delivered. That was wrong: the shipped JSONs carry
more than summaries. `s5_p4_ordinal.json` holds a Kendall's τ for **every
receptor**, and the 2×2 and classifier JSONs hold cell means, intervals and a
permutation null. What is genuinely missing is the 23 per-receptor values behind
SC-C-1 and the per-receptor LORO folds.

A four-value summary and a per-receptor distribution are different objects, and
this project has twice found the first concealing the second — so the class is
on the panel, not only in this file:

| spec | claim | built from | class |
|---|---|---|---|
| `BC-1_pocket_2x2.md` | SC-C-1 | cell means + cluster and receptor intervals | **SUMMARY** |
| `BC-2_ordinal_recovery.md` | SC-C-2 | a τ per receptor | **PER-RECEPTOR** |
| `BC-3_loro_classifier.md` | SC-C-4 | AUROC, intervals, permutation null | **SUMMARY** |
| `BC-4_ligand_placement.md` | SC-C-1 numerator, §4(a), §4(i) | 40,000 rows | **FULL** |

**BC-2 is the panel that earned the exercise.** Plotting the per-receptor τ
showed violins around 0.3 against printed panel values of 0.74 — which is how
D-C-3 was found: SC-C-2's table is headed "Kendall's τ" and contains a fraction
of receptors. That mislabel had passed the claim sheet, the dispatch and our own
Results, and it reached the manuscript.

Every figure-candidate number in these specs already exists as a shipped row or
a shipped JSON field. Nothing is estimated.
