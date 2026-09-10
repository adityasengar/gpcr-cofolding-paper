# Block C panel specs

**Specs, not images**, per the dispatch §6: no PNG, PDF or SVG, one panel per
file, spec ID only, no manuscript figure number, and no main-versus-SI call.

There is a second reason they are specs here and it is not a preference.
**Three of the four cannot be built from this bundle.** `rows.tier3.v2.csv` was
not delivered, so the 2×2 interaction, the ordinal recovery and the classifier
have no row-level data to plot. Only the ligand-placement panel is buildable
today, and it is marked as such.

| spec | claim | buildable now? |
|---|---|---|
| `BC-1_pocket_2x2.md` | SC-C-1 | **no** — needs `rows.tier3.v2.csv` |
| `BC-2_ordinal_recovery.md` | SC-C-2 | **no** — same |
| `BC-3_loro_classifier.md` | SC-C-4 | summary-only; CIs plottable from JSON, per-receptor points are not |
| `BC-4_ligand_placement.md` | SC-C-1 numerator, dispatch §4(a), §4(i) | **yes** — 40,000-row census is shipped |

Every figure-candidate number in these specs already exists as a shipped row or
a shipped JSON field. Nothing is estimated.
