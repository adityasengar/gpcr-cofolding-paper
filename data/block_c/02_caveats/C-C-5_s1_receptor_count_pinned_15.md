# C-C-5 — S1 KILL-S1 receptor count is 15, not 14

**Applies to**: any manuscript text quoting the S1 kill-row receptor count.

**The finding**: `PREREG_SIGNAL_RECOVERY.md` (locked 2026-09-07 pre-
numbers) states: *"9 receptors that are 100 % self-reference on the
antag_inactive cell: ACM4, ADRB2, CCR5, CNR1, CNR2, DRD3, NPY1R, OPRD,
OPRK. S1 self-reference-excluded run: 14 receptors (23 − 9)."*

The actual KILL-S1 evaluation (`s1_loro_classifier.json` variant
`C_no_selfref_apo`) reports `n_receptors_evaluated: 15` on all four
backbones × F_ii/F_iii feature sets. Root cause: **DRD3 is on the
self-ref list but was NOT in the common 23-receptor set** (dropped in
pre-classifier curation). Actual intersection is 23 common − 8 self-ref-
that-are-in-common = **15**. Prereg text's `23 − 9 = 14` did the
subtraction on the wrong set.

**Pinned 15-receptor S1 KILL-S1 set** (from JSON variant 26):
5HT1B, 5HT5A, AA1R, AA2AR, ACM2, AGTR1, CXCR2, CXCR4, EDNRB, GRPR,
LPAR1, LT4R1, MCHR1, NPY2R, OPRX.

**Consequence**: any manuscript sentence saying "14 held-out receptors"
must be corrected to 15. The per-receptor AUROC dict in the JSON
contains 15 keys; downstream analyses that iterated over 14 receptors
would silently land on the same 15 because the JSON's shape is what
they read.

**Sources**: `s1_loro_classifier.json` variant 26 (Boltz F_iii
`C_no_selfref_apo`), `PREREG_SIGNAL_RECOVERY.md`.
