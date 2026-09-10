# G2 ACTIVE-REFERENCE HOMOGENEITY CHECK

**Date**: 2026-09-10.
**Scope**: read-only cross-check of the AGTR1 diagnostic's curation
observation. Answer: is AGTR1 the only receptor in the G2 15-set with
a non-Gα-pathway active reference, or are others in the same category?
**Rule**: report the table, the count, and the two cross-checks — no
adjudication.

---

## Section 1 — Active-reference stabilization category for every G2 receptor

15 receptors from the S1 15-set. Data pulled from
`refs/reference_set.csv` (active-role rows) + CIF entity/title
inspection at `../paper_af3_release/panel/refs/pdb/*.cif`.

| receptor | active PDB | category | one-line source note |
|---|---|---|---|
| 5HT1B | 6G79 | **(a) native heterotrimer** | Native Gα-o + Gβ + Gγ + 5HT1B; title *"Coupling specificity of heterotrimeric Go to the 5-HT1B receptor"* |
| 5HT5A | 7UM5 | **(b) mini-G + scFv16** | miniGo + Gβ + Gγ + scFv16 + 5HT5A |
| AA1R | 7LD3 | **(a) native heterotrimer** | Native Gα-i2 + Gβ + Gγ + A1R (M4-A1R fusion chimera on receptor side) |
| AA2AR | 5G53 | **(b) mini-G / chimera** | Engineered mini-Gs (single-chain minimal Gα, no Gβγ) — `active_stabilization_source = mini_G` |
| ACM2 | 7T94 | **(a) native heterotrimer + scFv16** | Native Gα-o + Gβ + Gγ + scFv16 + M2R |
| **AGTR1** | **6OS2** | **(d) biased-agonist-selective nanobody** | **AT1R–BRIL chimera + Nb.AT110i1_le + TRV026 peptide; NO Gα, NO Gβγ; nanobody selects the β-arrestin-biased state; TRV026 is a β-arrestin-biased-agonist peptide** |
| CXCR2 | 6LFO | **(a) native heterotrimer + scFv16** | Native Gα-i + Gβ + Gγ + scFv16 + CXCR2 + IL-8 |
| CXCR4 | 8U4N | **(a) native heterotrimer** ⚠️ | Native Gα-i + Gβ + Gγ + CXCR4; title *"Structure of Apo CXCR4/Gi complex"* — Gα-coupled active BUT orthosteric pocket is APO (no bound ligand) |
| EDNRB | 8IY5 | **(a) native heterotrimer + scFv16** | Native Gα-i + Gβ + Gγ + scFv16 + EDNRB + endothelin-1 |
| GRPR | 7W40 | **(a) native heterotrimer + scFv16** | Native Gα-q + Gβ + Gγ + scFv16 + GRPR + bombesin(6-14) analog |
| LPAR1 | 7TD0 | **(a) native heterotrimer** | Native Gα-i + Gβ + Gγ + LPAR1 + LPA |
| LT4R1 | 7VKT | **(a) native heterotrimer + scFv16** | Native Gα-i + Gβ + Gγ + scFv16 + BLT1 + LTB4 |
| MCHR1 | 8WWK | **(a) native heterotrimer + scFv16** | Native Gα-i + Gβ + Gγ + scFv16 + MCHR1 + MCH |
| NPY2R | 7YON | **(a) native heterotrimer + scFv16** | Native Gα-i + Gβ + Gγ + scFv16 + NPY2R + PYY(3-36) |
| OPRX | 8F7X | **(a) native heterotrimer + scFv16** | Native Gα-i + Gβ + Gγ + scFv16 + OPRX + nociceptin |

**Category conventions used**:
- **scFv16** is an anti-Gα-Gβ-interface single-chain antibody that
  stabilizes an already-assembled heterotrimer. It does NOT replace
  Gα; complexes carrying WT Gα + scFv16 are (a) native heterotrimer.
- The Block A/B `active_stabilization_source` schema is the source of
  truth for coarse (a)/(b) categorization; refined here by direct CIF
  inspection.

**Cross-check against Block B's E1**:
E1 (`docs/BLOCK_B_FOLLOWUP_E1_E4.md` §E1) surveyed the 45-receptor
Class-A + Gα-complexed reference-set stratum, using the same
`active_stabilization_source` categories. Its schema included
`{native, mini_G, chimera, nanobody, agonist_only, DVL_DEP}`. Of the
G2 15-set: 12 map to native, 2 to mini_G, 1 (AGTR1) to nanobody. No
receptor in the 15-set maps to chimera, agonist_only, or DVL_DEP.
**No discrepancy with E1**; the fine-grained categorization here
(distinguishing category d "biased-agonist / arrestin-pathway
nanobody" from a hypothetical Nb35-class G-protein-mimetic) is a
refinement E1's schema did not distinguish.

---

## Section 2 — Homogeneity answer

**AGTR1 is the ONLY receptor in category (d) in the G2 15-set.**
Count: **1/15**.

**No receptor lands in category (c)** (G-protein-mimetic nanobody
like Nb35 — the class that stabilizes a G-protein-BOUND conformation
without a G protein). All non-native effectors in the 15-set are
either mini-G/chimeric-Gα (still Gα-pathway) or, in AGTR1's case, a
β-arrestin-biased-selective nanobody + biased-agonist peptide.

**No receptor lands in category (e)** (agonist-only, no effector).

**No receptor lands in category (f)** (other).

**Per-receptor S1 LORO AUROC** on the KILL-S1 row (F_iii, apo,
self-ref-excluded, per `s1_loro_classifier.json`):

| receptor | category | boltz | chai | of3 | protenix | inverted count |
|---|---|---:|---:|---:|---:|---:|
| 5HT1B | (a) native het | 0.979 | 0.722 | 0.805 | 0.983 | 0 |
| 5HT5A | (b) mini-G | 1.000 | 0.713 | 0.932 | 0.708 | 0 |
| AA1R | (a) native het | 1.000 | 1.000 | 1.000 | 1.000 | 0 |
| AA2AR | (b) mini-G | 1.000 | 1.000 | 1.000 | 1.000 | 0 |
| ACM2 | (a) native het + scFv16 | 0.687 | 1.000 | 0.997 | 0.994 | 0 |
| **AGTR1** | **(d) biased-agonist nanobody** | **0.100** | **0.000** | **0.000** | **0.000** | **4** |
| CXCR2 | (a) native het + scFv16 | 0.900 | 0.928 | **0.135** | 0.999 | 1 |
| CXCR4 | (a) native het (apo pocket) | 0.993 | 0.457 | 0.804 | 1.000 | 0 |
| EDNRB | (a) native het + scFv16 | 0.997 | 1.000 | 0.976 | 1.000 | 0 |
| GRPR | (a) native het + scFv16 | 0.984 | 1.000 | 0.985 | 1.000 | 0 |
| LPAR1 | (a) native het | 1.000 | 1.000 | 0.894 | 1.000 | 0 |
| LT4R1 | (a) native het + scFv16 | 1.000 | 0.692 | 0.776 | 1.000 | 0 |
| MCHR1 | (a) native het + scFv16 | 0.946 | 0.926 | 0.584 | 0.672 | 0 |
| NPY2R | (a) native het + scFv16 | 0.986 | 0.404 | 1.000 | 1.000 | 0 |
| OPRX | (a) native het + scFv16 | 1.000 | 0.999 | **0.361** | 1.000 | 1 |

"inverted count" = number of backbones on which AUROC < 0.30. AGTR1
inverts on all four. CXCR2 inverts on OF3 only. OPRX inverts on OF3
only.

**Since AGTR1 is the only receptor in category (c) or (d)**, the
dispatch's "pull per-receptor AUROC and G2 residual for other
category-c/d receptors" step yields no additional rows. There is no
comparison population to place AGTR1 within. The (c)/(d) category
count in the panel is n = 1 = AGTR1.

**The two other partial-inversion receptors (CXCR2 on OF3 only, OPRX
on OF3 only) both use canonical native Gα-i heterotrimeric active
references** with orthosteric ligand + scFv16 — category (a), no
curation-level anomaly on the stabilizer axis. Their inversion on
OF3 alone therefore does NOT track with an unusual reference
construct; it is a separate OF3-specific pattern that this dispatch
does not address.

**Direct answer**: **AGTR1's active-reference construct is unique in
the G2 15-set**. No other receptor sits in category (c) or (d). The
"non-canonical active-reference construct predicts outlier behaviour"
hypothesis has a sample size of 1 and cannot be tested against
counterexamples in this panel; the empirical fact is that the one
receptor with a biased-agonist-selective nanobody active reference
also happens to be the one receptor that inverts on all four
backbones. The remaining 14 in the panel share Gα-pathway active
references (native heterotrimer × 12; mini-G/chimera × 2).

---

## Section 3 — Two cheap cross-checks

### 3a — What does G2d check, and does §1–§2 answer it?

**G2d (`fold-integrity subset origin test`, dispatch language)**: asks
whether the 10-receptor "fold-integrity-finite" subset used in Check 2
of the S1-signal-recovery pass is drawn disproportionately from the
LOW-pocket-Cα-reference-separation mode. If yes, Check 2's AUROC
instability across the 10-receptor subset would have the same
underlying explanation as G2's overall pattern (whatever that
explanation is).

**Does §1–§2 above answer G2d?** **No.** G2d is orthogonal:
- §1–§2 examines the ACTIVE-REFERENCE STABILIZATION CATEGORY across
  the S1 15-set.
- G2d examines the RECEPTOR MEMBERSHIP OF A DIFFERENT SUBSET (the 10
  receptors kept by Check 2's fold-integrity filter) vs the
  POCKET-Cα-SEPARATION DISTRIBUTION.

The 10-receptor list needed for G2d is not in the JSON that would
normally carry it: `check2_fi_finite_subset.json` records only
per-backbone AUROC + row count + delta-from-original (schema keys:
`results`, `n_fi_finite_pair_rows`, `pct_fi_finite`). No
`fi_finite_receptors` list is present. Enumerating the 10 receptors
requires re-running the fold-integrity filter over the corpus, which
is a separate task.

**Verdict**: G2d stays on its own deferred-caveats line; §1–§2 does
NOT retire it. §1–§2 does inform G2d weakly: since AGTR1 sits at
pocket-Cα-sep rank 39/40 (very HIGH) and drives G2's main negative
slope, if AGTR1 were IN Check 2's FI-finite subset, its presence
would push the FI-finite subset toward high sep, not low. Whether
AGTR1 is in the subset is answerable when the enumeration is done.

### 3b — Bug #2 firing on AGTR1's references

**Neither of AGTR1's references fires Bug #2.**

From `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/reference_survey.csv`:
- **6OS2 (AGTR1 active)**: `bug2_fires = no`, `status = OK`.
- **4ZUD (AGTR1 inactive)**: `bug2_fires = no`, `status = OK`.

The AGTR1 diagnostic's predicate-check verdict (§2b of
`docs/AGTR1_REFASSIGN_REPORT.md`) — that both references pass the
two-instrument predicate on their labels — is UNAFFECTED. This is a
note for the record, not a re-check trigger.

**Adjacent finding for the record**: the 10 references that DO fire
Bug #2 across the 168-ref survey are:
{ACM4/5DSG-inactive, MTR1B/6ME6-inactive, OPRX/5DHH-inactive,
OPSD/4X1H-active, TSHR/7T9M-inactive, **AA2AR/5G53-active**,
ACM3/8E9Z-active, CALCR/8F0J-active, GCGR/5XEZ-inactive,
FZD4/8WM9-active}. Two of these receptors are in the G2 15-set:
- **AA2AR active reference 5G53** — Bug #2 fires. **Not in this
  dispatch's scope** to re-check, but worth flagging: AA2AR's per-
  receptor AUROC on all four backbones is 1.000, so if Bug #2 does
  affect its scoring, the effect is invisible at classifier level
  (both classes score identically). Recorded here without acting on
  it.
- **OPRX inactive reference 5DHH** — Bug #2 fires. OPRX's active
  reference (8F7X) is fine. OPRX inverts on OF3 only. Whether
  Bug #2 on the inactive reference contributes to OF3-only inversion
  is out of scope here; recorded.

---

## Outputs

- `docs/G2_REFERENCE_HOMOGENEITY.md` — this file.

No JSON produced (no bootstrap, no new statistic — the table + counts
are the deliverable). No commits, no shared-corpus edits.

**Held state**: BLOCK_C_CLOSEOUT Parts B/C remain held. AGTR1
diagnostic remains recorded but not adjudicated. The framing choice
(bounded negative + one-flagged-outlier scope vs empirical-failure-list-
only) remains outside this dispatch.
