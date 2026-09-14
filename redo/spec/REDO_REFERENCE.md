# REDO_REFERENCE.md — the single reference for the redo campaign

**Generated 2026-09-14 by `analysis/` tooling from the files it cites.** Every count
was produced by a command actually run against `redo/inputs/`, then independently
re-derived by a second pass. Part 12 records what that second pass rejected.

**Where this document and `redo/inputs/` disagree, `inputs/` wins.**

---

## Contents

1. [0. What this document is, and how to read it](#0-what-this-document-is-and-how-to-read-it)
2. [1. What the paper is trying to show, and the honest status of each claim](#1-what-the-paper-is-trying-to-show-and-the-honest-status-of-each-claim)
3. [2. Vocabulary and conventions — read before any table below](#2-vocabulary-and-conventions--read-before-any-table-below)
4. [3. The receptors — every GPCR in the campaign](#3-the-receptors--every-gpcr-in-the-campaign)
5. [4. The partner constructs — every chain B, with its length](#4-the-partner-constructs--every-chain-b-with-its-length)
6. [5. The ligands](#5-the-ligands)
7. [6. THE DECOY SETUP — D-RULE, its gate, and its refusal](#6-the-decoy-setup--d-rule-its-gate-and-its-refusal)
8. [7. The MSA and alignment setup](#7-the-msa-and-alignment-setup)
9. [8. The 45 catalogued experiments](#8-the-45-catalogued-experiments)
10. [9. The five-stage plan — what runs, in what order, and what each stage settles](#9-the-five-stage-plan--what-runs-in-what-order-and-what-each-stage-settles)
11. [10. Thirteen experiments that are NOT in the catalogue](#10-thirteen-experiments-that-are-not-in-the-catalogue)
12. [11. Verification machinery — how to check anything in this document](#11-verification-machinery--how-to-check-anything-in-this-document)
13. [12. Disagreements found while writing this document](#12-disagreements-found-while-writing-this-document)
14. [13. Known defects — stated, not hidden](#13-known-defects--stated-not-hidden)
15. [14. Decisions waiting on the PI](#14-decisions-waiting-on-the-pi)
16. [15. Two failure patterns that govern how any result here may be reported](#15-two-failure-patterns-that-govern-how-any-result-here-may-be-reported)

---

# Part 0. What this document is, and how to read it

**This is the single reference for the redo campaign.** It is meant to make the other
23 documents in `redo/spec/` unnecessary for anyone who is not editing them.

**How it was built, and what that buys you.** Every data section below was produced
under one standing rule: *every number must come from a command actually run, and a
count stated in a prose document must be RE-DERIVED from the data file rather than
copied.* Each section was then given to a second, independent pass that re-derived the
numbers with its own commands. **Where the two disagreed, the disagreement is recorded
in Part 12 rather than quietly resolved** — including the places where a number in this
repository's own specification documents turned out to be wrong.

**Where this document and `redo/inputs/` disagree, `inputs/` wins.** `inputs/` is what
dispatches; this is what explains. Part 11 tells you how to check any claim here in one
command.

### The one fact that governs everything else

**Nothing in this campaign has run. Zero predictions. No GPU time has been spent.**

Every factor is still choosable, every arm can still be added or cut, and every
free-now-impossible-later item is still free. This is not a half-finished campaign
being salvaged. Work that HAS happened used no inference: measurement of deposited PDB
structures, and re-analysis of the four delivered blocks from the frozen campaign.

### Reading routes

| if you want | read |
|---|---|
| the shortest useful orientation | Part 1, Part 2, Part 9 |
| what we are actually simulating | Parts 3, 4, 5, 6 |
| the decoy design specifically | **Part 6** — the longest section here |
| what could still be added | Part 10 |
| to check something yourself | Part 11 |
| what is wrong or unresolved | Parts 12, 13, 14 |

---

# Part 1. What the paper is trying to show, and the honest status of each claim

Three claims. They are independent of one another, and they are in very different
states of evidence.

| # | claim | status |
|---|---|---|
| **1** | A 21-residue piece of the Gα α5 C-terminus, supplied as a **second input chain**, drives four co-folding models into the **active** GPCR state | **No peptide arm has ever run.** Every partner arm in the frozen campaign is a complete Gα subunit or a nanobody, and the segment that was actually varied is **11 residues**, not 21 |
| **2** | The **agonist alone** does not do this | **Claimed, then retracted the same day** (`DECISIONS.md` F-23). Every row of the file used to answer it carries a ligand — "apo" there meant *no partner*, not *no ligand* — so "agonist alone" was never predicted |
| **3** | Model **confidence** does not track state correctness | The only clause with data behind it |

**The redo exists to put evidence behind claims 1 and 2 without weakening claim 3.**

Two consequences follow, and they shape the whole plan:

- **Claim 1 needs a peptide arm that has never existed.** That is the length ladder,
  Part 4 and Stage 3.
- **Claim 2 needs ligand-free predictions.** Those exist as 98 enumerated, READY rows
  that cost nothing extra, and their pre-registration is written and unsealed
  (`spec/C7_PREREGISTRATION.md`). It is worth nothing once anything runs.

---

# Part 2. Vocabulary and conventions — read before any table below

### 2.1 The models

Four structure-prediction systems, referred to throughout as **backbones**:
**Boltz-2**, **OpenFold3** (preview), **Protenix** (v2), **Chai-1**.

In `inputs/`, the `backbones` field is either `boltz2|openfold3|protenix|chai1`
(1,271 of 2,039 Group 1 rows) or `boltz2` alone (768 rows — the pilots and the
single-backbone scans, which exist to prove a contract before four-backbone money is
spent).

### 2.2 The chains

**Chain A is always the GPCR.** **Chain B, when present, is the partner** — a Gα
fragment, a complete Gα subunit, or a control protein. **Chain C** appears only in the
heterotrimer arm (Gβ1, 340 aa, and Gγ2, 71 aa).

### 2.3 The state readout

A predicted structure is called **active** when both of:

```
d(Y5.58 hydroxyl , Y7.53 hydroxyl)  <  9.08 Å      "NPxxY-OH"
d(2×46 Cα        , 6×37 Cα)         > 14.932 Å     "TM6 tilt"
```

Both thresholds are `midpoint(mean of actives, mean of inactives)`, fitted on the
32-receptor panel, averaging PDBs within a receptor before averaging across receptors
(`DECISIONS.md` F-17). The continuous values are recorded alongside the binary call,
because the binary call alone discards the size of the effect.

**Two numbering systems are in play and the difference is load-bearing.** NPxxY anchors
are looked up on Ballesteros–Weinstein labels (`5.58`, `7.53`); tilt anchors are looked
up on GPCRdb generic numbers (`2x46`, `6x37`). Where a helix carries a bulge the two
diverge, and matching the tilt anchors on the BW field would land on a different
residue in exactly the receptors whose TM6 geometry is most unusual.

### 2.4 The statistical unit is the paralog cluster

Two receptors in the same paralog cluster are not independent evidence. Every power
calculation uses **k = number of clusters**, never number of receptors.

```
interaction effects:  MDE = 2.80 × 0.435 / √k  =  1.218 / √k
main effects:         MDE = 0.189 – 0.242
```

| k | 11 | 12 | 15 | 17 | 19 | 22 | 24 | 26 | 29 | 32 |
|---|---|---|---|---|---|---|---|---|---|---|
| **MDE** | 0.367 | 0.352 | 0.314 | 0.295 | 0.279 | 0.260 | 0.249 | 0.239 | 0.226 | 0.215 |

**This is why C1_REST matters as a cautionary case**: it holds 24 receptors in only 14
clusters, so reporting it as n=24 would overstate the evidence by nearly a factor of
two in effective sample size.

### 2.5 Cost classes

| class | meaning |
|---|---|
| **free** | re-analysis of data already on disk. No inference of any kind |
| **cheap** | re-scoring predictions that already exist. No new inference |
| **real** | new GPU inference. Always quoted as a number of predictions |

**There is no GPU-hour model anywhere in this campaign.** Every cost figure in every
document is a *count of predictions*, and `RUN_MATRIX.md` §1.4's own cost bracket spans
a factor of **13** because the cost of a two-chain prediction has never been measured.
One line from the pipeline team on that rate would re-order most priority lists here.

### 2.6 Prediction counts come in two grains

`predictions_pooled` uses **n = 10** samples per cell and supports pooled claims only.
`predictions_percell` uses **n = 50** and supports per-receptor claims. Group 1's full
enumeration totals **74,960 pooled / 212,920 per-cell** across all 2,039 rows;
`PLAN.md`'s first pass is a **≈38,300-prediction subset** of that.

### 2.7 "DECOY" MEANS TWO DIFFERENT THINGS. Do not conflate them.

This is the single most important piece of vocabulary in the document, because both
senses appear in the same tables and one of them is the subject of Part 6.

| | **decoy PARTNER** (chain B) | **decoy LIGAND** (small molecule) |
|---|---|---|
| what it is | a Gα-like protein whose **α5 C-terminal tail has been edited or scrambled** | a compound **matched to the real ligand on eight physicochemical axes**, topologically dissimilar, with no measured activity at the target |
| where it appears | Block B's four arms: `apo / decoy / shuffled / cognate`; in the redo as `R6b_a5perm`, `R6c_a5polyA`, `ct21@scramble#*` | Group 2's `decoy_lig` role, selected by **D-RULE** |
| what it controls for | "is the effect the α5 sequence, or just a protein of that size?" | "is the effect the drug's pharmacology, or just an occupied pocket?" |
| its known problem | **confounded at the MSA** — editing the tail also changes the partner's alignment | **does not exist for part of the panel** — see F-19, Part 6.9 |
| Part | 4 | **6** |

**Block B's published ladder — apo 0.158 → decoy 0.558 → shuffled 0.809 → cognate
0.891 — is a ladder of PARTNERS, not of ligands.** Reading that "decoy 0.558" as a
small-molecule result would be a serious error.

---

# Part 3. The receptors — every GPCR in the campaign

Scope was closed to **class A only** on 2026-09-12 (`DECISIONS.md` § `D-2026-09-12-d`).
Class B and class F receptors are excluded, not deferred. `g1_receptors.tsv` carries
`gclass = A` on all 64 rows, so the decision costs the campaign nothing — it makes a
scope that was already incidental into one that is claimed.

### 3.1 The population: 64 receptors in 32 paralog clusters

| quantity | value | file |
|---|---:|---|
| distinct receptors in `g1_systems.csv` | **64** | `inputs/g1_systems.csv` (2,039 rows) |
| distinct receptors in `g2_systems.csv` | **26** | `inputs/g2_systems.csv` (350 rows) |
| distinct receptors in the union | **64** | — |
| distinct paralog clusters (union) | **32** | `receptor_cluster` |
| receptors in **both** g1 and g2 | **26** | g2 is a strict subset of g1 |
| receptors in **g2 but not g1** | **0** | — |
| receptors in **g1 but not g2** | **38** | — |
| receptors with a `rule_r_active_pdb` | **64 of 64**, all distinct | `coupling_cognate_map.tsv` |
| receptors with a distinct `chain_a_sha256` | **64 of 64** | one frozen chain-A sequence per receptor |

Every receptor attribute (`receptor_uniprot`, `receptor_organism`, `receptor_cluster`,
`chain_a_sha256`) is byte-identical between `g1_systems.csv` and `g2_systems.csv` for
all 26 shared receptors — **0 mismatches**. The two files are two views of one panel,
not two panels.

### 3.2 The master table — all 64 receptors

`receptor_set(s)` lists membership across both files; the `LIG_*` sets come from
`g2_systems.csv`, the rest from `g1_systems.csv` (where every value carries a literal
`(provisional)` suffix, stripped here). `tier` is `g1_panel_freeze.tsv:tier`, which
partitions the 64 exactly: PRIMARY = CORE32, EXT-census = C1_REST, EXT-chimeric =
EXT_CHIMERA. "active PDB" is `coupling_cognate_map.tsv:rule_r_active_pdb`; the
resolution is `g1_receptors.tsv:active_res`.

| slug | UniProt | organism | cluster | tier | receptor_set(s) | g1 rows | g2 rows | cognate family | subtype | evidence class | verdict | active PDB (Å) |
|---|---|---|---|---|---|---:|---:|---|---|---|---|---|
| **5HT1B** | P28222 | human | `001_001_001` | EXT-census | C1_REST | 3 | 0 | Gi/o | Go | STRUCTURE_NEAR | frozen | 6G79 (3.78) |
| **5HT2A** | P28223 | human | `001_001_001` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 8UWL (2.8) |
| **5HT2C** | P28335 | human | `001_001_001` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 8DPF (2.84) |
| **5HT5A** | P47898 | human | `001_001_001` | PRIMARY | CORE32 + LIG_T1 | 50 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7X5H (3.1) |
| **AA1R** | P30542 | human | `001_006_001` | PRIMARY | CORE32 + LIG_T1 | 50 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7LD3 (3.2) |
| **AA2AR** | P29274 | human | `001_006_001` | PRIMARY | CORE32 + CORE32_GS + LIG_T1 + LIG_T1_INV_EXTRA | 59 | 20 | Gs | Gs | CONVENTION_FALLBACK | frozen_by_convention | 8WDT (3.34) |
| **ACM1** | P11229 | human | `001_001_002` | EXT-census | C1_REST | 3 | 0 | Gq/11 | Gq | STRUCTURE_EXACT | frozen | 6OIJ (3.3) |
| **ACM2** | P08172 | human | `001_001_002` | EXT-census | C1_REST | 3 | 0 | Gi/o | Go | STRUCTURE_EXACT | frozen | 7T94 (3.16) |
| **ACM4** | P08173 | human | `001_001_002` | PRIMARY | CORE32 + G10_SCAN + LIG_T1 + LIG_T1_INV_EXTRA | 86 | 20 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7TRP (2.4) |
| **ADA1A** | P35348 | human | `001_001_003` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 7YM8 (2.92) |
| **ADA2A** | P08913 | human | `001_001_003` | EXT-census | C1_REST | 3 | 0 | Gi/o | Go | STRUCTURE_EXACT | frozen | 7EJ8 (3.0) |
| **ADRB1** | P08588 | human | `001_001_003` | PRIMARY | CORE32 + CORE32_GS + LIG_T1 | 59 | 18 | Gs | Gs | CONVENTION_FALLBACK | frozen_by_convention | 7BU7 (2.6) |
| **ADRB2** | P07550 | human | `001_001_003` | EXT-census | C1_REST | 3 | 0 | Gs | Gs | STRUCTURE_EXACT | frozen | 8GG0 (2.9) |
| **AGTR1** | P30556 | human | `001_002_001` | PRIMARY | CORE32 + LIG_T3 | 50 | 6 | Gq/11 | Gq | CONVENTION_FALLBACK | frozen_by_convention | 6OS2 (2.7) |
| **APJ** | P35414 | human | `001_002_002` | PRIMARY | CORE32 + G10_SCAN | 86 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8XZH (2.6) |
| **B1B1U5** | B1B1U5 | **spider** | `001_009_001_inv` | PRIMARY | CORE32 + REFCHIMERA_CORE32 + LIG_T1 | 52 | 18 | Gq/11 | Gq | STRUCTURE_NEAR | frozen | 9EPP (4.06) |
| **C5AR1** | P21730 | human | `001_002_006` | PRIMARY | CORE32 + G10_SCAN + LIG_T2 | 86 | 6 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7Y66 (2.9) |
| **CCKAR** | P32238 | human | `001_002_005` | PRIMARY | CORE32 + CORE32_GS + LIG_T1 | 59 | 18 | Gs | Gs | STRUCTURE_EXACT | frozen | 7MBX (1.95) |
| **CCR2** | P41597 | human | `001_003_002` | PRIMARY | CORE32 + G10_SCAN + LIG_T3 | 86 | 6 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7XA3 (2.9) |
| **CCR5** | P51681 | human | `001_003_002` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7O7F (3.15) |
| **CCR6** | P51684 | human | `001_003_002` | EXT-census | C1_REST | 3 | 0 | Gi/o | Go | STRUCTURE_NEAR | frozen | 6WWZ (3.34) |
| **CCR8** | P51685 | human | `001_003_002` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8KFX (2.96) |
| **CNR1** | P21554 | human | `001_004_005` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8GHV (2.8) |
| **CNR2** | P34972 | human | `001_004_005` | PRIMARY | CORE32 + G10_SCAN + LIG_T1 | 86 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8GUR (2.84) |
| **CXCR2** | P25025 | human | `001_003_002` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 6LFO (3.4) |
| **CXCR3** | P49682 | human | `001_003_002` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8HNM (2.94) |
| **CXCR4** | P61073 | human | `001_003_002` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8U4N (2.72) |
| **DRD2** | P14416 | human | `001_001_004` | EXT-census | C1_REST | 3 | 0 | Gi/o | Go | STRUCTURE_EXACT | frozen | 8TZQ (3.2) |
| **DRD3** | P35462 | human | `001_001_004` | PRIMARY | CORE32 + G10_SCAN + LIG_T1 + LIG_T1_INV_EXTRA | 86 | 20 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8IRT (2.7) |
| **DRD4** | P21917 | human | `001_001_004` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gi/o | — | CHIMERA_SPLIT | needs_decision | 8IRU (3.2) |
| **EDNRA** | P25101 | human | `001_002_007` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 8HCQ (3.01) |
| **EDNRB** | P24530 | human | `001_002_007` | PRIMARY | CORE32 + G10_SCAN + LIG_T3 | 86 | 6 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8IY5 (2.8) |
| **FSHR** | P23945 | human | `001_003_003` | EXT-census | C1_REST | 3 | 0 | Gs | Gs | STRUCTURE_EXACT | frozen | 8I2G (2.8) |
| **GHSR** | Q92847 | human | `001_002_010` | PRIMARY | CORE32 + LIG_T1 | 50 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7NA7 (2.7) |
| **GPR52** | Q9Y2T5 | human | `001_010_001` | PRIMARY | CORE32 + CORE32_GS | 59 | 0 | Gs | Gs | STRUCTURE_NEAR | frozen | 8HMP (2.77) |
| **GPR6** | P46095 | human | `001_010_001` | EXT-census | C1_REST | 3 | 0 | Gs | Gs | STRUCTURE_EXACT | frozen | 8TYW (3.43) |
| **GRPR** | P30550 | human | `001_002_003` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 8H0Q (3.3) |
| **HRH1** | P35367 | human | `001_001_005` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 8YN2 (2.66) |
| **HRH2** | P25021 | human | `001_001_005` | EXT-census | C1_REST | 3 | 0 | Gs | Gs | STRUCTURE_NEAR | frozen | 8YN3 (2.56) |
| **HRH3** | Q9Y5N1 | human | `001_001_005` | PRIMARY | CORE32 + G10_SCAN + LIG_T1 | 86 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8YN5 (2.7) |
| **LPAR1** | Q92633 | human | `001_004_003` | PRIMARY | CORE32 + LIG_T1 | 50 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7TD0 (2.83) |
| **LSHR** | P22888 | human | `001_003_003` | EXT-census | C1_REST | 3 | 0 | Gs | Gs | STRUCTURE_NEAR | frozen | 7FII (4.3) |
| **LT4R1** | Q15722 | human | `001_004_002` | PRIMARY | CORE32 + LIG_T1 | 50 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7VKT (2.9) |
| **MCHR1** | Q99705 | human | `001_002_013` | PRIMARY | CORE32 + LIG_T3 | 50 | 6 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8WWK (2.61) |
| **MTR1A** | P48039 | human | `001_005_001` | PRIMARY | CORE32 | 50 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7VGY (3.1) |
| **MTR1B** | P49286 | human | `001_005_001` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7VH0 (3.46) |
| **NK1R** | P25103 | human | `001_002_029` | PRIMARY | CORE32 + CORE32_GS + LIG_T3 | 59 | 6 | Gs | Gs | STRUCTURE_NEAR | frozen | 8U26 (2.5) |
| **NPY1R** | P25929 | human | `001_002_020` | PRIMARY | CORE32 + LIG_T3 | 50 | 6 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7X9A (3.2) |
| **NPY2R** | P49146 | human | `001_002_020` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8K6N (3.2) |
| **NTR1** | P30989 | human | `001_002_021` | PRIMARY | CORE32 + LIG_T3 | 50 | 6 | Gi/o | Gi1 | CONVENTION_FALLBACK | frozen_by_convention | 8JPF (3.02) |
| **OPRD** | P41143 | human | `001_002_022` | PRIMARY | CORE32 + LIG_T1 | 50 | 18 | Gi/o | Gi1 | CONVENTION_FALLBACK | frozen_by_convention | 6PT2 (2.8) |
| **OPRK** | P41145 | human | `001_002_022` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8FEG (2.54) |
| **OPRM** | P42866 | **mouse** | `001_002_022` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | CONVENTION_FALLBACK | frozen_by_convention | 5C1M (2.07) |
| **OPRX** | P41146 | human | `001_002_022` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8F7X (3.28) |
| **OPSD** | P02699 | **bovine** | `001_009_001_vert` | PRIMARY | CORE32 + REFCHIMERA_CORE32 + LIG_T1 | 51 | 18 | Gi/o | Gt1 | PEPTIDE_ENTITY | frozen_with_caveat | 4X1H (2.29) |
| **OX2R** | O43614 | human | `001_002_023` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 7L1V (3.0) |
| **OXYR** | P30559 | human | `001_002_032` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 7RYC (2.9) |
| **PD2R2** | Q9Y5Y4 | human | `001_004_008` | PRIMARY | CORE32 + G10_SCAN + LIG_T1_BLOCKED | 86 | 2 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 8XXV (2.33) |
| **PE2R4** | P35408 | human | `001_004_008` | EXT-census | C1_REST | 3 | 0 | Gs | Gs | STRUCTURE_EXACT | frozen | 8GDB (3.1) |
| **S1PR1** | P21453 | human | `001_004_004` | PRIMARY | CORE32 + G10_SCAN + LIG_T1 | 86 | 18 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7TD4 (2.6) |
| **S1PR5** | Q9H228 | human | `001_004_004` | EXT-census | C1_REST | 3 | 0 | Gi/o | Gi1 | STRUCTURE_EXACT | frozen | 7EW1 (3.4) |
| **SSR2** | P30874 | human | `001_002_028` | PRIMARY | CORE32 + LIG_T2 | 50 | 6 | Gi/o | **Gi3** | STRUCTURE_EXACT | frozen | 7T10 (2.5) |
| **TA2R** | P21731 | human | `001_004_008` | EXT-chimeric | REFCHIMERA_CORE32 + EXT_CHIMERA | 5 | 0 | Gq/11;Gs | — | CHIMERA_SPLIT | needs_decision | 8XJN (3.06) |
| **TSHR** | P16473 | human | `001_003_003` | PRIMARY | CORE32 + CORE32_GS | 59 | 0 | Gs | Gs | STRUCTURE_NEAR | frozen | 7UTZ (2.4) |

### 3.3 The receptor sets, and how they nest

The eleven `receptor_set` values are not eleven panels. Three of them partition the 64
exactly; the rest are subsets carved out for particular arms.

```
64 receptors  =  CORE32 (30)  ⊔  C1_REST (24)  ⊔  EXT_CHIMERA (10)       ← a partition
                   ├── CORE32_GS (6)            ⊂ CORE32
                   ├── G10_SCAN (10)            ⊂ CORE32
                   └── LIG_T1/T2/T3 (26 total)  ⊂ CORE32   (all of g2)
REFCHIMERA_CORE32 (12) = EXT_CHIMERA (10) + B1B1U5 + OPSD    ← crosses the partition
```

Verified as set identities, not as prose: `PRIMARY == CORE32`, `EXTENSION-census ==
C1_REST`, `EXTENSION-chimeric-reference == EXT_CHIMERA` all return `True`;
`CORE32_GS ⊆ CORE32`, `G10_SCAN ⊆ CORE32`, `EXT_CHIMERA ⊆ REFCHIMERA_CORE32` and
`g2 receptors ⊆ CORE32` all return `True`; `CORE32 ∩ C1_REST = ∅`.

#### Counts per set, with the MDE each implies

| receptor_set | file | rows | **receptors** | **clusters** | rec/clu | interaction MDE `1.218/√k` | main-effect MDE `2.80·SD/√k`, SD 0.189–0.242 |
|---|---|---:|---:|---:|---:|---:|---:|
| CORE32 | g1 | 1,500 | **30** | **29** | 1.03 | **0.226** | 0.098 – 0.126 |
| CORE32_GS | g1 | 54 | 6 | 6 | 1.00 | 0.497 | 0.216 – 0.277 |
| G10_SCAN | g1 | 360 | 10 | 10 | 1.00 | 0.385 | 0.167 – 0.214 |
| REFCHIMERA_CORE32 | g1 | 23 | 12 | 11 | 1.09 | 0.367 | 0.160 – 0.204 |
| C1_REST | g1 | 72 | **24** | **14** | **1.71** | 0.326 | 0.141 – 0.181 |
| EXT_CHIMERA | g1 | 30 | 10 | 9 | 1.11 | 0.406 | 0.176 – 0.226 |
| LIG_T1 | g2 | 288 | 16 | 15 | 1.07 | 0.314 | 0.137 – 0.175 |
| LIG_T1_INV_EXTRA | g2 | 6 | 3 | 3 | 1.00 | 0.703 | 0.306 – 0.391 |
| LIG_T1_BLOCKED | g2 | 2 | 1 | 1 | 1.00 | 1.218 | 0.529 – 0.678 |
| LIG_T2 | g2 | 12 | 2 | 2 | 1.00 | 0.861 | 0.374 – 0.479 |
| LIG_T3 | g2 | 42 | 7 | 7 | 1.00 | 0.460 | 0.200 – 0.256 |
| **g1, all sets** | g1 | 2,039 | **64** | **32** | 2.00 | **0.215** | 0.094 – 0.120 |
| **g2, all sets** | g2 | 350 | **26** | **25** | 1.04 | **0.244** | 0.106 – 0.136 |
| **union** | both | 2,389 | **64** | **32** | 2.00 | **0.215** | 0.094 – 0.120 |

> **Read the two MDE columns as different quantities.** `1.218 = 2.80 × 0.435`, where
> 0.435 is the median *interaction* cluster SD (`RUN_MATRIX.md:515`). The main-effect
> cluster SDs are **0.189** (`cognate − apo`) and **0.242** (`cognate − decoy`)
> (`RUN_MATRIX.md:490,492`) — those are **standard deviations, not MDEs**. Quoting
> "0.189–0.242" as the main-effect MDE drops the `2.80/√k` and makes the number
> independent of panel size, which it is not. The main-effect MDE column above is
> `2.80 × SD / √k`; at k = 32 it reproduces RUN_MATRIX's own tabulated 0.094 and 0.120
> exactly, which is the check that the formula is being applied the way that file
> applies it. See `C7_PREREGISTRATION.md:43-52`, which corrected this same slip on
> 2026-09-13.

#### Which arms run on which set

| receptor_set | experiments | arms |
|---|---|---|
| CORE32 | E1.1, E1.2, E1.3, E1.4, E1.6, E1.7, E1.9 | `ladder` (210), `ladder_pilot` (210), `composition_controls` (300), `deposited_minig_anchor` (90), `intermediate_nested` (90), `intermediate_pilot` (90), `wetlab_length_series` (90), `a5null` (90), `non_ga_bulk` (90), `partner_msa_on` (90), `hd_deletion_companion` (30), `intermediate_optional` (30), `family_swap` (30), `gi_gt_single_residue` (30), `heterotrimer` (30) |
| CORE32_GS | E1.1, E1.8, E1.8+E1.1 | `wetlab_matched_peptides` (18), `uncoupling_full` (12), `uncoupling_peptide` (24) |
| G10_SCAN | E1.5 | `ala_scan` (210), `gi_to_gs_series` (150) |
| REFCHIMERA_CORE32 | E1.1 | `reference_matched_tip` (23) |
| C1_REST | E1.1 | `wide_replication` (72) |
| EXT_CHIMERA | E1.1 | `chimeric_ref_extension` (30) |
| LIG_T1 | E2.2, E2.4 | `ligand_x_partner` (96), `ligand_x_partner_pilot` (96), `ligand_x_partner_full_subunit` (48), `decoy_third_role` (32), `decoy_third_role_full_subunit` (16) |
| LIG_T1_INV_EXTRA | E2.3 | `efficacy_ladder_inverse_agonist` (6) |
| LIG_T1_BLOCKED | E2.2 | `blocked_ligand_identity` (2) |
| LIG_T2 | E2.2 | `ligand_x_partner_peptide_tier` (12) |
| LIG_T3 | E2.2 | `ligand_x_partner_mixed_tier` (42) |

### 3.4 Receptors versus clusters, and why the difference is the whole point

The statistical unit is the **paralog cluster**, not the receptor. A cluster is a GPCRdb
family code at depth 3 — `001_003_002` is the chemokine receptors, `001_002_022` the
opioids — so two receptors in one cluster share most of their sequence and most of their
binding pocket. If a co-folding model gets CXCR2 right it will very probably get CXCR3
right for the same reason, so counting them as two independent observations inflates
precision without adding evidence. Every MDE in this document therefore divides by √k
where **k is the cluster count**, never the receptor count.

The two counts diverge unevenly across the panel, and CORE32 was built so that they
barely diverge at all: **30 receptors in 29 clusters**, the one collapse being AA1R and
AA2AR, both adenosine (`001_006_001`), and AA2AR is in CORE32 only as a declared
override (`g1_panel_freeze.tsv:override_reason` — it "adds a receptor, not a cluster").
**C1_REST is the opposite construction: 24 receptors in only 14 clusters**, a ratio of
1.71, because it is a *census* — it sweeps up every remaining class-A receptor with both
deposited states rather than one representative per family. Six of its 24 are chemokine
receptors in a single cluster and three are opioid receptors in another:

| cluster | family | C1_REST members | n |
|---|---|---|---:|
| `001_003_002` | chemokine (CCR + CXCR) | CCR5, CCR6, CCR8, CXCR2, CXCR3, CXCR4 | **6** |
| `001_002_022` | opioid (+ nociceptin) | OPRK, OPRM, OPRX | **3** |
| `001_001_002` | muscarinic | ACM1, ACM2 | 2 |
| `001_001_003` | adrenergic (α + β) | ADA2A, ADRB2 | 2 |
| `001_003_003` | glycohormone | FSHR, LSHR | 2 |
| nine others | — | one each | 1 |

The practical consequence: C1_REST's 24 receptors buy the power of 14, an MDE of
**0.326** rather than the 0.249 that 24 independent units would give — a **31 %** loss
that a receptor-level count would hide entirely. This is why C1_REST is `wide_replication`
(72 rows, one arm) rather than a place where headline contrasts are estimated. Conversely
`CORE32` and `G10_SCAN` are near-1:1 by design, so their receptor counts are honest proxies
for their statistical n.

`PANEL.md:453-458` records which depth-3 splits are defensible and which are not: the
adrenergic α/β split, the CCR/CXCR split and the opioid/nociceptin split are all rejected
as paralogous, so those receptors stay merged; only the opsin split is kept (see below).

### 3.5 Species

Row-level, `g1_systems.csv`: **1,933 human, 52 *Hasarius adansoni*, 51 *Bos taurus*,
3 *Mus musculus*.** Row-level, `g2_systems.csv`: **314 human, 18 spider, 18 bovine,
0 mouse.**

Receptor-level, over the 64:

| organism | receptors | which | where |
|---|---:|---|---|
| *Homo sapiens* | **61** | — | everywhere |
| *Hasarius adansoni* (jumping spider) | **1** | **B1B1U5**, a jumping-spider rhodopsin | CORE32, REFCHIMERA_CORE32, LIG_T1 |
| *Bos taurus* | **1** | **OPSD**, bovine rhodopsin | CORE32, REFCHIMERA_CORE32, LIG_T1 |
| *Mus musculus* | **1** | **OPRM**, µ-opioid receptor | C1_REST only |

**No sentence may call this panel human** (`PANEL.md:621`). Two of the three non-human
receptors are in the PRIMARY panel.

**Why they are retained.** The panel-selection rule (Rule P) chooses a species explicitly
per receptor and then requires that a receptor's active and inactive reference structures
be **the same species**. Computed over all 64 receptors from `panel_systems.csv`
(`our_active_species` vs `our_inactive_species`): **zero cross-species reference pairs**.
So the non-human receptors never put a species difference *inside* the active-versus-
inactive comparison the predicate measures — B1B1U5 is scored spider-against-spider
(9EPP / 6I9K), OPSD bovine-against-bovine (4X1H / 7ZBC), OPRM mouse-against-mouse
(5C1M / 7UL4). Dropping them would remove receptors, not remove a confound. ACM3 *was*
dropped for exactly the opposite reason — its only both-state pair is human-active
against rat-inactive (`PANEL.md:418-427`).

**The opsins additionally buy a cluster.** `001_009_001` is split into
`001_009_001_vert` (OPSD) and `001_009_001_inv` (B1B1U5) — the only depth-3 split the
panel makes by hand, and `PANEL.md:457` defends it: "bovine rhodopsin and a jumping-spider
opsin are not paralogs in any useful sense." Removing B1B1U5 would cost CORE32 a whole
cluster, taking k from 29 to 28.

**B1B1U5 carries three caveats that must reach Methods.** (i) Its cognate family is Gq,
and the deposited α5 tip is genuine jumping-spider Gαq1 (INSDC `LC799818`) grafted onto a
human Gαi1 backbone — the 0.86 tip identity is **species divergence, not engineering**
(`DECISIONS.md` D-2026-09-12-b). (ii) **No native complex exists for this receptor**:
9EPP is a chimera and the alternative 9EPR is human Gαi1 reconstituted *in vitro* with
bovine Gβ1γ1. `PANEL.md` Rule 4 is inapplicable here, not merely unimplemented.
(iii) At 4.06 Å it is the worst-resolved active reference in the primary panel, and
`tejero2024opsin` reports that TM6 opens *further* in the chimera than in the hGi complex
— the very axis the predicate measures. `DECISIONS.md:79` calls its reference geometry
"the least trustworthy in the primary panel" and asks for a per-receptor sensitivity check.

**OPSD's active reference is known to be mis-annotated.** 4X1H is labelled `native` in
RCSB but carries an engineered 11-residue peptide as its partner, deposited as its own
molecule rather than as a mutant of the subunit it derives from, so RCSB's mutation record
is empty and **no rule written on receptor-entity metadata can catch it**
(`PANEL.md:674`). That 11-mer is why OPSD's evidence class is `PEPTIDE_ENTITY`.

### 3.6 Cognate G-protein assignment — the evidence classes

`coupling_cognate_map.tsv` assigns each receptor one cognate family and subtype by
reading the α5 C-terminus of the Rule-R active reference against canonical human Gα
sequences. Every receptor gets a class saying how that read was obtained.

| evidence class | n | what it means | receptors |
|---|---:|---|---|
| `STRUCTURE_EXACT` | **39** | the deposited α5 tip matches a canonical human Gα exactly over ct21 | 5HT5A, AA1R, ACM1, ACM2, ACM4, ADA2A, ADRB2, APJ, C5AR1, CCKAR, CCR2, CCR5, CCR8, CNR1, CNR2, CXCR2, CXCR3, CXCR4, DRD2, DRD3, EDNRB, FSHR, GHSR, GPR6, HRH3, LPAR1, LT4R1, MCHR1, MTR1A, MTR1B, NPY1R, NPY2R, OPRK, OPRX, PD2R2, PE2R4, S1PR1, S1PR5, SSR2 |
| `CHIMERA_SPLIT` | **10** | scaffold and α5 tip read **different families**; the rule does not choose | 5HT2A, 5HT2C, ADA1A, DRD4, EDNRA, GRPR, HRH1, OX2R, OXYR, TA2R |
| `STRUCTURE_NEAR` | **8** | tip differs from the nearest canonical at 1 of 21 positions | 5HT1B, B1B1U5, CCR6, GPR52, HRH2, LSHR, NK1R, TSHR |
| `CONVENTION_FALLBACK` | **6** | the active reference contains **no Gα entity**; family comes from annotation, subtype is the declared family representative | AA2AR, ADRB1, AGTR1, NTR1, OPRD, OPRM |
| `PEPTIDE_ENTITY` | **1** | partner is an 11-residue peptide, so ct21 does not exist; scored on ct11 | OPSD |

Verdicts track the classes: **47 `frozen`**, **10 `needs_decision`** (exactly the
CHIMERA_SPLIT ten), **6 `frozen_by_convention`** (exactly the CONVENTION_FALLBACK six),
**1 `frozen_with_caveat`** (OPSD).

Cognate families across the 64: **Gi/o 40, Gs 12, `Gq/11;Gs` 9, Gq/11 3.** Subtypes:
**Gi1 32, Gs 12, blank 10, Go 5, Gq 3, Gt1 1 (OPSD), Gi3 1 (SSR2).** Within CORE32 the
split is **Gi/o 22, Gs 6, Gq/11 2**.

### 3.7 Every caveated cognate assignment

#### (a) Ten receptors whose assignment is UNDECIDED — `CHIMERA_SPLIT` / `needs_decision`

These are the `EXT_CHIMERA` set. Their only deposited active reference is a coupling
chimera: the Gα scaffold reads one family and the α5 tip reads another, and the tip
matches **no** canonical human Gα (best ct21 identity 0.62, or 0.71 for DRD4). Both
readings are honest; the rule refuses to pick. `cognate_subtype` is **empty** for all ten,
and `cognate_vs_reference_agree` is `n/a` — the comparison is undefined.

| receptor | scaffold reads | α5 tip reads | recorded family | annotation backs | ct21 identity |
|---|---|---|---|---|---:|
| 5HT2A | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| 5HT2C | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| ADA1A | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| EDNRA | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| GRPR | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| HRH1 | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| OXYR | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| TA2R | Gs | Gq/11 | `Gq/11;Gs` | A / tip | 0.62 |
| OX2R | Gs | Gq/11 | `Gq/11;Gs` | **A / tip + B / scaffold** | 0.62 |
| **DRD4** | Gs | **Gi/o** | `Gi/o` | A / tip | 0.71 |

These ten are held in `EXT_CHIMERA` / tier `EXTENSION-chimeric-reference` precisely so
that they cannot silently enter a primary count. `g1_panel_freeze.tsv:exclusion_reason`
on all ten: *"chimeric active reference: engineered alpha5 tip, ineligible for a strict
primary panel."*

#### (b) Six receptors assigned by CONVENTION, not by structure

The Rule-R active reference contains no Gα entity at all — the partner is a nanobody,
antibody or other. The family is taken from `coupling_assignments.csv:recommended_family`
and the subtype is the **declared representative** of that family, not a structure read.

| receptor | active PDB | what is in it instead | corroborating off-Rule-R structure |
|---|---|---|---|
| AA2AR | 8WDT | nanobody/antibody, other | 6GDG — same subtype |
| ADRB1 | 7BU7 | nanobody/antibody, other | 8DCS — same subtype |
| AGTR1 | 6OS2 | nanobody/antibody, other | 7F6G — same subtype |
| NTR1 | 8JPF | other | 6OS9 — same subtype |
| OPRD | 6PT2 | other | 8F7S — same subtype |
| **OPRM** | 5C1M | nanobody/antibody, other | **none — no active reference of this receptor contains a Gα at all, so there is no structural check** |

#### (c) Eight `STRUCTURE_NEAR` — one substitution away

5HT1B, B1B1U5, CCR6, GPR52, HRH2, LSHR, NK1R, TSHR. The deposited tip differs from the
nearest canonical human Gα at **1 of 21 positions**, and the file states plainly that
"whether that is engineering or species divergence is not readable from the sequence."
Family and subtype are nonetheless unambiguous because every canonical at the best score
falls in one family. B1B1U5 is the exception where the cause **is** known (species
divergence, §3.5).

#### (d) One `PEPTIDE_ENTITY` — OPSD

ct21 does not exist because the partner entity is an 11-residue peptide, so the read is
scored on ct11. The nearest canonicals — Ggust / Gt1 / Gt2 — are 4 substitutions away
over 11 positions; the nearest canonical of any *other* family is 7 away, so the family
is unambiguous. **`Gt1` is the tie representative of a three-way tie**, not a
discriminated subtype.

#### (e) Thirty-two subtypes are TIE REPRESENTATIVES, not discriminated reads

`coupling_cognate_map.tsv:tie_set` is non-empty and multi-valued for **32 of 64**
receptors. Where it reads `Gi1/Gi2`, the α5 tip is identical in both subtypes and "Gi1"
is a label chosen from a tie, not a measurement.

| tie set | n | receptors |
|---|---:|---|
| `Gi1/Gi2` | **29** | 5HT5A, AA1R, ACM4, APJ, C5AR1, CCR2, CCR5, CCR8, CNR1, CNR2, CXCR2, CXCR3, CXCR4, DRD3, EDNRB, GHSR, HRH3, LPAR1, LT4R1, MCHR1, MTR1A, MTR1B, NPY1R, NPY2R, OPRK, OPRX, PD2R2, S1PR1, S1PR5 |
| `G11/Gq` | 2 | ACM1, B1B1U5 |
| `Ggust/Gt1/Gt2` | 1 | OPSD |

(Single-valued `tie_set` entries — `Gs` on 10 receptors, `Go` on 5, `Gi3` on SSR2 — are
unique reads and carry no tie caveat.)

#### (f) Fifteen receptors where the cognate call is NOT INDEPENDENT of the reference

`g1_panel_freeze.tsv:supplied_partner_independence`. This column exists to keep the
biology (what the receptor couples in assays) apart from the structure (what the deposited
reference contains). On 15 of 64 receptors the two are the same evidence:

| sub-class | n | receptors |
|---|---:|---|
| coupling recommendation taken from the deposited reference | **10** | AA1R, C5AR1, CCKAR, CCR6, CNR1, GHSR, GPR52, HRH2, NK1R, NTR1 |
| …taken from the deposited reference, **and that reference is CHIMERIC** | **3** | 5HT2C, EDNRA, TA2R |
| **no non-structure coupling authority at all** — no assay, no GproteinDb row, no IUPHAR entry | **2** | **B1B1U5**, **OPSD** |

The remaining 49 read "annotation only — independent of the structure." The 13 in the
first two rows correspond exactly to the 13 rows of `coupling_assignments.csv` whose
`recommended_basis` begins "taken from the deposited active reference, following
`chiesa2025templatebias` p.6302." The last two were a **generator defect fixed on
2026-09-12**: the column had claimed independence for B1B1U5 and OPSD, both PRIMARY,
when `coupling_assignments.csv` gives both `n_authorities = 1` and that authority is
`authority_structure` (`DECISIONS.md` D-2026-09-12-b).

#### (g) Four receptors whose cognate call REVERSES the Block B prior

`g1_panel_freeze.tsv:reverses_blockb_prior == yes` on **4 of 64**. Anything inherited
from Block B about these receptors is wrong for the redo:

| receptor | Block B assigned | Rule-R structure reads |
|---|---|---|
| **B1B1U5** | Gi (Gi/o) | **Gq/11** |
| **CCKAR** | Gq (Gq/11) | **Gs** |
| **EDNRB** | Gq (Gq/11) | **Gi/o** |
| **GHSR** | Gq (Gq/11) | **Gi/o** |

#### (h) Annotation-level conflict, independent of the structural read

`coupling_cognate_map.tsv:annotation_verdict`, which summarises what the *assay and
database* authorities say, irrespective of the structure: **42 `cognate_ambiguous`,
14 `cognate_conflicted`, 8 `cognate_confident`.** Only eight receptors on the whole panel
have a clean annotation-level cognate: **CCR2, CCR8, CXCR3, DRD3, DRD4, HRH3, NPY1R,
PD2R2.** From `coupling_assignments.csv`, **39 of 64 have a single primary family and 25
do not**. The standing sentence in `coupling_assignments.csv:reason` is the right one to
quote in Methods: *"'the cognate Gα' is a choice, not a fact."*

### 3.8 g1 versus g2 — which receptors carry ligand work

**g2 is a strict subset of g1: all 26 g2 receptors are in g1, and all 26 are PRIMARY
(CORE32).** There are **no** g2-only receptors. The 38 g1-only receptors are every
C1_REST member (24), every EXT_CHIMERA member (10), and four CORE32 members:

```
g1-only, 38 receptors:
  5HT1B  5HT2A  5HT2C  ACM1   ACM2   ADA1A  ADA2A  ADRB2
  APJ*   CCR5   CCR6   CCR8   CNR1   CXCR2  CXCR3  CXCR4
  DRD2   DRD4   EDNRA  FSHR   GPR52* GPR6   GRPR   HRH1
  HRH2   LSHR   MTR1A* MTR1B  NPY2R  OPRK   OPRM   OPRX
  OX2R   OXYR   PE2R4  S1PR5  TA2R   TSHR*
        * = in CORE32 but carries no ligand row: APJ, GPR52, MTR1A, TSHR
```

So the ligand campaign covers **26 of the 30 CORE32 receptors**, in **25 of 29 clusters**.

#### Per-receptor g2 detail

| receptor | g2 rows | ligand tier | non-`none` roles present | READY | blocked |
|---|---:|---|---|---:|---|
| 5HT5A | 18 | T1_small_molecule | agonist, antagonist, decoy | 18 | — |
| AA1R | 18 | T1_small_molecule | agonist, antagonist, decoy | 15 | DECOY_UNAVAILABLE ×3 |
| AA2AR | 20 | T1_small_molecule | agonist, antagonist, inverse, decoy | 17 | DECOY_UNAVAILABLE ×3 |
| ACM4 | 20 | T1_small_molecule | agonist, antagonist, inverse, decoy | 20 | — |
| ADRB1 | 18 | T1_small_molecule | agonist, inverse, decoy | 18 | — |
| AGTR1 | 6 | T3_mixed | agonist, inverse | 6 | — |
| B1B1U5 | 18 | T1_small_molecule | agonist, inverse, decoy | 15 | DECOY_UNAVAILABLE ×3 |
| C5AR1 | 6 | T2_peptide | agonist, antagonist | 2 | CHAIN_NO_SEQUENCE ×4 |
| CCKAR | 18 | T1_small_molecule | agonist, antagonist, decoy | 18 | — |
| CCR2 | 6 | T3_mixed | agonist, antagonist | 2 | UNRESOLVED_UNCURATED ×4 |
| CNR2 | 18 | T1_small_molecule | agonist, antagonist, decoy | 18 | — |
| DRD3 | 20 | T1_small_molecule | agonist, antagonist, inverse, decoy | 20 | — |
| EDNRB | 6 | T3_mixed | agonist, antagonist | 6 | — |
| GHSR | 18 | T1_small_molecule | agonist, antagonist, decoy | 18 | — |
| HRH3 | 18 | T1_small_molecule | agonist, antagonist, decoy | 15 | DECOY_UNAVAILABLE ×3 |
| LPAR1 | 18 | T1_small_molecule | agonist, antagonist, decoy | 15 | DECOY_UNAVAILABLE ×3 |
| LT4R1 | 18 | T1_small_molecule | agonist, antagonist, decoy | 18 | — |
| MCHR1 | 6 | T3_mixed | agonist, antagonist | 6 | — |
| NK1R | 6 | T3_mixed | agonist, antagonist | 2 | UNRESOLVED_UNCURATED ×4 |
| NPY1R | 6 | T3_mixed | agonist, antagonist | 6 | — |
| NTR1 | 6 | T3_mixed | agonist, inverse | 2 | UNRESOLVED_UNCURATED ×4 |
| OPRD | 18 | T1_small_molecule | agonist, antagonist, decoy | 18 | — |
| OPSD | 18 | T1_small_molecule | agonist, inverse, decoy | 18 | — |
| **PD2R2** | 2 | T1_small_molecule | agonist | **0** | LIGAND_IDENTITY ×2 |
| S1PR1 | 18 | T1_small_molecule | agonist, antagonist, decoy | 18 | — |
| SSR2 | 6 | T2_peptide | agonist, antagonist | 2 | CHAIN_NO_SEQUENCE ×4 |

**313 of 350 g2 rows are `READY`.** The 37 blocked rows fall in four classes:
`BLOCKED_DECOY_UNAVAILABLE` 15 rows / 5 receptors (AA1R, AA2AR, B1B1U5, HRH3, LPAR1);
`BLOCKED_UNRESOLVED_UNCURATED` 12 / 3 (CCR2, NK1R, NTR1);
`BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE` 8 / 2 (C5AR1, SSR2 — both peptide-ligand tier);
`BLOCKED_LIGAND_IDENTITY` 2 / 1 (**PD2R2**, whose only two g2 rows are both blocked —
it is the sole member of `LIG_T1_BLOCKED` and contributes nothing dispatchable).

#### The C7 instrument, in receptor terms

**98 of 350 g2 rows are ligand-free (`ligand_role_actual == none`), and all 98 are
`READY`.** Crossing those against the full-agonist rows in the same arm gives
**20 receptors carrying the complete 2×2** (ligand present/absent × partner
cognate/apo, all four cells READY), spanning **19 distinct paralog clusters**:

```
5HT5A  AA1R   AA2AR  ACM4   ADRB1  AGTR1  B1B1U5 CCKAR  CNR2   DRD3
EDNRB  GHSR   HRH3   LPAR1  LT4R1  MCHR1  NPY1R  OPRD   OPSD   S1PR1
```

The one cluster collapse is AA1R + AA2AR (`001_006_001`). At k = 19 the interaction MDE
is **0.279** and the main-effect MDE — which is what C7 actually tests — is
**0.121–0.155**.

### 3.9 How CORE32 came to be 30 and not 32

`g1_panel_freeze.tsv` carries both columns. `core32_provisional == yes` on **32**
receptors; `core_frozen == yes` on **30**. The difference is six receptors, not two:

| receptor | provisional | frozen | why |
|---|---|---|---|
| 5HT2A | yes | **no** | chimeric active reference — moved to EXT_CHIMERA |
| GRPR | yes | **no** | chimeric active reference — moved to EXT_CHIMERA |
| OX2R | yes | **no** | chimeric active reference — moved to EXT_CHIMERA |
| OXYR | yes | **no** | chimeric active reference — moved to EXT_CHIMERA |
| 5HT5A | no | **yes** | backfilled the serotonin cluster vacated by 5HT2A |
| AA2AR | no | **yes** | declared override — "loses its cluster to AA1R by 0.14 Å, and is the only panel receptor with wet-lab data on our exact 21-mer (`eddy2018extrinsictrp` W233-6.35; `mazzoni2000`'s length series). Adds a receptor, not a cluster — AA1R stays." |

Net: −4 chimeric, +1 backfill, +1 override = **30 receptors in 29 clusters**. The name
`CORE32` is historical and refers to the 32 *provisional* members; **it is 30 today, and
the value in `g1_systems.csv` still reads `CORE32(provisional)` on all 1,500 rows.**
`GROUP2_LIGANDS.md:329` records this trap explicitly.

---

# Part 4. The partner constructs — every chain B, with its length

Chain A of every Group 1 system is the GPCR. Chain B is the partner: a Gα fragment, a
full Gα subunit, or a deliberately wrong molecule. Nothing here has been run; every row
is still choosable.

Two files govern this domain, and they answer different questions.

| file | rows | answers |
|---|---:|---|
| `redo/inputs/g1_partner_registry.tsv` | **782** data rows | *what molecules exist as bytes on this laptop*, keyed by sha256 of the uppercase one-letter sequence |
| `redo/inputs/g1_systems.csv` | **2,039** data rows | *which of them get dispatched, to which receptor, in which arm, at what n* |

Both hash clean against the manifest:
`shasum -a 256 g1_partner_registry.tsv` → `26ca0d3e1f22f2f559468ea05901a1f48fcbdfa7cea8b355c2337cac47abd4a5`,
`g1_systems.csv` → `debdd5bec4192ae1871faa0b238383f4fa6bcc32d07bd505df6886e9528ef0e3`,
each matching its `MANIFEST.tsv` line exactly.

**The registry is keyed by hash, never by header.** `partners.fasta` carries three known
mislabels (`Nb60` holds the Nb80 CDR3, `GASR` is the gastrin *receptor*, `arrestin_FL` is
β-arrestin-1 residues 22–36 and not a finger loop), so an arm that resolves its partner
by name can silently dispatch the wrong molecule. That is the reason the registry exists.

---

### 4.1 The registry at a glance

`awk -F'\t' 'NR>1{print $8}' g1_partner_registry.tsv | sort | uniq -c`

| `held` | rows |
|---|---:|
| `yes` | **771** — every one carries a full 64-hex sha256 |
| `NO` | **10** — named in the design, bytes not held anywhere |
| `yes-but-mislabelled` | **1** (`arrestin_FL`) |

**782 rows, 50 distinct construct names, 64 distinct (class, construct) pairs, 13
construct classes.** A construct name can appear in more than one class — `R1_ct11`
exists as a `ga_rung`, as a `ga_rung_isoform` (GoB) and as an `uncoupling_mutant`.

`awk -F'\t' 'NR>1{print $1}' g1_partner_registry.tsv | sort | uniq -c | sort -rn`

| construct_class | rows | source table(s) |
|---|---:|---|
| `peptide_control` | 336 | `seq_controls.tsv` 240 + 96 derived here (Gi3, Go) |
| `ga_rung` | 261 | `seq_rungs.tsv` 112, `g1_midrungs.tsv` 80, `seq_a5null.tsv` 21, 48 derived here |
| `ala_scan` | 105 | derived from `seq_rungs.tsv` |
| `ref_tip` | 23 | `g1_refchimera.tsv` |
| `gi_to_gs_scan` | 15 | derived from `seq_rungs.tsv` |
| `not_dispatchable` | 11 | — (no bytes) |
| `uncoupling_mutant` | 8 | derived from `seq_rungs.tsv` |
| `ga_rung_isoform` | 6 | live fetch (UniProt P09471-2 = GoB) |
| `species_matched_tip` | 5 | derived from `g1_refchimera.tsv` |
| `non_ga_chain` | 5 | live fetch, each hash-checked against `SEQUENCES.md` |
| `wetlab_matched` | 3 | derived from `seq_rungs.tsv` |
| `minig_deposited` | 3 | `g1_minig.tsv` (RCSB) |
| `boundary_variant` | 1 | derived from `seq_rungs.tsv` |

---

### 4.2 The 17 Gα families

Sequences exist for exactly **17 Gα families**, all human. **This count is over the
`ga_rung` and `ga_rung_isoform` construct classes.** Querying the registry's `family`
column without that filter returns **30 distinct values**, because the reference-tip
constructs put the **receptor** slug in that column (`5HT2A`, `ADA1A`, `GRPR`, `HRH1`,
`OPSD`, `OX2R`, `OXYR`, `TA2R`, `EDNRA`, `DRD4`, `5HT2C`, `B1B1U5`) and ten rows leave
it empty. Filter on `construct_class` before counting families.

The seventeen:

```
Gs  Golf                      (Gs)
Gi1 Gi2 Gi3 Go GoB Gz         (Gi/o)
Gt1 Gt2 Ggust                 (Gi/o, transducin branch)
Gq  G11 G14 G15               (Gq/11)
G12 G13                       (G12/13)
```

Sixteen come from `seq_rungs.tsv`. The seventeenth, **GoB**, is UniProt **P09471-2**
(GNAO1 isoform Alpha-2), fetched live and registered as `ga_rung_isoform`. This matters
for reading every other document: `seq_rungs.tsv`'s bare label `Go` is P09471 **canonical
= isoform Alpha-1 = GoA**, verified by hash, and the bare label should be read as GoA
everywhere. GoB differs from GoA by 1 substitution at ct11, 2 at ct15, 3 at ct21, 3 at
a5helix, 5 at a5plus (registry `note` column).

The registry's `family` column carries 30 distinct values, of which 17 are Gα. The other
13 are **not families**: one empty string (the 10 non-Gα / un-held rows), `B1B1U5` (the
spider *Gαq1* accession), and eleven **receptor slugs** — `5HT2A 5HT2C ADA1A DRD4 EDNRA
GRPR HRH1 OPSD OX2R OXYR TA2R` — used to key each receptor's own deposited α5 tip.

Per-family accessions and the α5 window, from `seq_constructs.tsv`:

| family | accession | full length | CGN G.H5 (α5) | G.S6 | ct11 | ct21 |
|---|---|---:|---|---|---|---|
| Gs | P63092 | 394 | 369–394 | 359–363 | 384–394 | 374–394 |
| Golf | P38405 | 381 | 356–381 | 346–350 | 371–381 | 361–381 |
| Gi1 | P63096 | 354 | 329–354 | 319–323 | 344–354 | 334–354 |
| Gi2 | P04899 | 355 | 330–355 | 320–324 | 345–355 | 335–355 |
| Gi3 | P08754 | 354 | 329–354 | 319–323 | 344–354 | 334–354 |
| Go (=GoA) | P09471 | 354 | 329–354 | 319–323 | 344–354 | 334–354 |
| GoB | P09471-2 | 354 | — (not in `seq_constructs.tsv`) | — | — | — |
| Gz | P19086 | 355 | 330–355 | 320–324 | 345–355 | 335–355 |
| Gt1 | P11488 | 350 | 325–350 | 315–319 | 340–350 | 330–350 |
| Gt2 | P19087 | 354 | 329–354 | 319–323 | 344–354 | 334–354 |
| Ggust | A8MTJ3 | 354 | 329–354 | 319–323 | 344–354 | 334–354 |
| Gq | P50148 | 359 | 334–359 | 324–328 | 349–359 | 339–359 |
| G11 | P29992 | 359 | 334–359 | 324–328 | 349–359 | 339–359 |
| G14 | O95837 | 355 | 330–355 | 320–324 | 345–355 | 335–355 |
| G15 | P30679 | 374 | 349–374 | 339–343 | 364–374 | 354–374 |
| G12 | Q03113 | 381 | 356–381 | 346–350 | 371–381 | 361–381 |
| G13 | Q14344 | 377 | 352–377 | 342–346 | 367–377 | 357–377 |

**G.H5 is 26 residues in all 16 families** (`H5_len` is `26` on 16 of 17 rows; the 17th
row is `Gt1_bovine` P04695, whose H5 is `NA`). **`Gt1_bovine` is held in
`seq_constructs.tsv` but is not a registry family and is never dispatched** — do not
confuse `seq_constructs.tsv`'s 17 rows (16 human + bovine Gt1) with the registry's 17 Gα
families (16 human + GoB).

#### Families collapse at peptide length — and this is load-bearing

At every rung from 11 to 36 residues the 17 families reduce to only **13 distinct
molecules**:

| rung | residues | families held | **distinct sequences** | byte-identical groups |
|---|---:|---:|---:|---|
| `R1_ct11` | 11 | 17 | **13** | Gi1≡Gi2 · Ggust≡Gt1≡Gt2 · G11≡Gq |
| `R1b_ct13` | 13 | 16 | 12 | same three |
| `R2_ct15` | 15 | 17 | **13** | same three |
| `R2b_ct17` | 17 | 16 | 12 | same three |
| `R2c_ct19` | 19 | 16 | 12 | same three |
| `R3_ct21` | 21 | 17 | **13** | same three |
| `R4_a5helix` | 26 | 17 | **13** | same three |
| `R5_a5plus` | 36 | 17 | **13** | same three |
| `M1_h4s6` | 44–56 | 16 | 14 | Gi1≡Gi2 · G11≡Gq |
| `M2_h4` | 60–73 | 16 | 15 | G11≡Gq |
| `M3_h3` / `M4_he` / `M5_dHD` / `R6a_da5` | ≥112 | 16 | **16** | none |
| `R7_full` | 350–394 | 17 | **17** | none |

A "family contrast" at any peptide rung between Gi1 and Gi2, or between Gq and G11, or
among Ggust/Gt1/Gt2, **is the same molecule run twice**. Family only becomes a real
variable at M1 and above.

---

### 4.3 The suffix rule — checked, and it holds with three named exceptions

**Claim:** every rung is a C-terminal suffix of the parent Gα subunit.

**Verified mechanically, not assumed.** For each family, the parent `R7_full` sequence
was taken from `seq_rungs.tsv`, its last *N* residues sliced, sha256'd, and compared to
the registry's recorded hash:

- **129 / 129** `ga_rung` + `boundary_variant` rows at lengths 11, 13, 15, 17, 19, 21, 26,
  27, 36 reproduce **exactly**, zero failures.
- **64 / 64** `g1_midrungs.tsv` rows for `M1_h4s6`, `M2_h4`, `M3_h3`, `M4_he` reproduce
  exactly.
- The hash convention itself is confirmed: `sha256("QRMHLRQYELL")` =
  `f159565cbda52c2b…` = the registry's Gs `R1_ct11`.

So the sentence "every rung is a C-terminal suffix of the parent, only the start moves"
is **true for R1 through R5, R4b and M1 through M4** — and the nesting is strict:
R1_ct11 ⊂ R1b_ct13 ⊂ R2_ct15 ⊂ R2b_ct17 ⊂ R2c_ct19 ⊂ R3_ct21 ⊂ R4_a5helix ⊂ R5_a5plus ⊂
M1 ⊂ M2 ⊂ M3 ⊂ M4 ⊂ R7_full, in all 16 seq_rungs families (80/80 adjacent-pair suffix
checks pass).

**Three constructs are NOT suffixes, by design, and the registry says so on every row:**

| construct | why not a suffix | where it says so |
|---|---|---|
| `M5_dHD` | full subunit with the helical domain **excised** (Gs: residues 85–199 removed, `resid_range` `1-84+200-394`) — it keeps the N terminus | `g1_midrungs.tsv:nested_in_ladder` = `NO -- keeps the N terminus`, on all 16 rows |
| `R6a_da5` | full subunit with G.H5 **deleted** — it is the parent's *prefix*, `full[:-26]` | `seq_a5null.tsv:rule` = `full subunit, CGN G.H5 deleted (1..L-26)` |
| `R6b_a5perm`, `R6c_a5polyA` | full subunit with the last 26 **replaced** in place | `seq_a5null.tsv:rule` |

`g1_systems.csv`'s own note on the M5 arm is blunt about it: *"OFF-LADDER: keeps the N
terminus, so not a nested suffix."*

The three `MG_*` deposited mini-Gs are also not truncations, and the registry records the
exact mismatch count per construct — see §4.6.

#### The α5 boundary: 26 or 27?

Both numbers are in the repo and they mean different things.

- **CGN G.H5 = 369–394 = 26 residues** (Gs). This is the campaign's operative definition
  and is what `R4_a5helix` is, in all 17 families.
- **Asp368–Leu394 = 27 residues** is the *literature* (Sunahara) α5 window. It is
  registered once, as `boundary_variant` / `R4b_a5helix27` / Gs, sha
  `f0936d17fc8bb8f0…`, provenance `P63092 368-394 (Asp368-Leu394)`, with the note:
  *"the literature alpha5 boundary; CGN G.H5 is 369-394 (26). They differ by one
  N-terminal residue, D368. Not a rung — a reconciliation artefact, so the convention is
  auditable."*

**Constructs that exceed the α5 helix:** `R5_a5plus` (36 = G.S6 → C-term, i.e. β6-s6h5-α5),
every `M*` rung, `R6a/b/c`, `R7_full`, `R8_hetero`, all three `MG_*`, and `R4b_a5helix27`
by exactly one residue. Methods must never describe `R5_a5plus` as "a longer α5" — it is
α5 plus the ten preceding residues of S6 and the s6h5 loop.

---

### 4.4 The length ladder — R0 through R8

**`R0_apo` and `R8_hetero` are not in the registry.** They are synthesised inside
`g1_systems.py:resolve()`: `R0_apo` returns length `0` with no chain B at all
(`n_chains=1`, `partner_msa=n/a`), and `R8_hetero` returns `R7_full` length **+ 411**,
because Gβ1 (P62873, 340 aa) + Gγ2 (P59768, 71 aa) = 411. All other 80 chain-B constructs
in `g1_systems.csv` resolve into the registry.

**Caveat on `R8_hetero`'s `chain_b_len`:** it is the *sum of all three chains*, not the
length of chain B. Chain B alone is the cognate `R7_full` (350–394); `chain_c` carries
`Gbeta1 P62873 + Ggamma2 P59768`.

| construct | residues | Gα families in registry | rows in `g1_systems` | pooled preds | held | role |
|---|---:|---:|---:|---:|---|---|
| `R0_apo` | **0** | n/a (synthesised) | **94** | 2,860 | n/a | receptor alone. The floor the whole ladder is read against |
| `R1_ct11` | 11 | **17** | **90** | 7,500 | yes | shortest rung; also the anchor for the Gi/Gt single-residue arm |
| `R1b_ct13` | 13 | 16 | **30** | 1,200 | yes | wet-lab rung — `mazzoni2000`'s two-residue ladder needs 13 |
| `R2_ct15` | 15 | **17** | **60** | 1,500 | yes | ladder rung |
| `R2b_ct17` | 17 | 16 | **30** | 1,200 | yes | wet-lab rung; helicity rises steeply from ~17 up |
| `R2c_ct19` | 19 | 16 | **30** | 1,200 | yes | wet-lab rung |
| `R3_ct21` | 21 | **17** | **154** | 10,060 | yes | **the title's construct**, and the reference rung for every control |
| `R4_a5helix` | 26 | **17** | **60** | 1,500 | yes | CGN G.H5 — the α5 helix as the campaign defines it |
| `R4b_a5helix27` | **27** | 1 (Gs) | **0** | 0 | yes | the Sunahara literature boundary, held so the 26-vs-27 convention is auditable. **Not dispatched** |
| `R5_a5plus` | 36 | **17** | **90** | 2,700 | yes | G.S6 → C-term. Past α5, and must not be called "a longer α5" |
| `R6a_da5` | 324–368 | 16 | **30** | 1,200 | yes | full subunit, α5 deleted (see §4.5) |
| `R6b_a5perm` | 350–394 | 7 | **30** | 1,200 | yes | full subunit, α5 scrambled in place (see §4.5) |
| `R6c_a5polyA` | 350–394 | 7 | **30** | 1,200 | yes | full subunit, α5 → poly-Ala (see §4.5) |
| `R7_full` | **350–394** | **17** | **124** | 4,060 | yes | the complete Gα subunit. The ceiling |
| `R8_hetero` | **761–805** | n/a (synthesised) | **30** | 6,000 | n/a | Gα + Gβ1 + Gγ2, three chains. A harness change, not a new molecule |

Per-family rung lengths (residues), from `seq_rungs.tsv` + `g1_midrungs.tsv` + registry:

| family | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | M1 | M2 | M3 | M4 | M5 | R6a | R7 |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Gs | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 47 | 63 | 130 | 221 | 279 | 368 | **394** |
| Golf | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 47 | 63 | 130 | 221 | 266 | 355 | 381 |
| Gi1 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 61 | 113 | 204 | 240 | 328 | 354 |
| Gi2 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 61 | 113 | 204 | 240 | 329 | 355 |
| Gi3 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 61 | 113 | 204 | 240 | 328 | 354 |
| Go | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 44 | 60 | 112 | 203 | 239 | 328 | 354 |
| GoB | 11 | — | 15 | — | — | 21 | 26 | 36 | — | — | — | — | — | — | 354 |
| Gz | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 61 | 113 | 204 | 240 | 329 | 355 |
| Gt1 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 61 | 113 | 204 | 236 | 324 | **350** |
| Gt2 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 61 | 113 | 204 | 240 | 328 | 354 |
| Ggust | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 61 | 113 | 204 | 240 | 328 | 354 |
| Gq | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 44 | 61 | 113 | 204 | 246 | 333 | 359 |
| G11 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 44 | 61 | 113 | 204 | 246 | 333 | 359 |
| G14 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 44 | 61 | 113 | 204 | 242 | 329 | 355 |
| G15 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 56 | 73 | 125 | 216 | 261 | 348 | 374 |
| G12 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 44 | 61 | 113 | 204 | 264 | 355 | 381 |
| G13 | 11 | 13 | 15 | 17 | 19 | 21 | 26 | 36 | 45 | 62 | 114 | 205 | 256 | 351 | 377 |

The ct21 sequences themselves, for the seven families that carry a full control set:

```
Gs    RVFNDCRDIIQRMHLRQYELL   (374-394, P63092)
Gi1   FVFDAVTDVIIKNNLKDCGLF   (334-354, P63096)
Gi3   FVFDAVTDVIIKNNLKECGLY   (334-354, P08754)
Go    VVFDAVTDIIIANNLRGCGLY   (334-354, P09471)
Gt1   FVFDAVTDIIIKENLKDCGLF   (330-350, P11488)
Gq    FVFAAVKDTILQLNLKEYNLV   (339-359, P50148)
G13   LVFRDVKDTILHDNLKQLMLQ   (357-377, Q14344)
```

#### The 13/17/19-mers

`R1b_ct13`, `R2b_ct17` and `R2c_ct19` exist for **16 Gα families**, **50 registry rows**
(48 `ga_rung` + 2 `wetlab_matched` C379A variants), **all `held=yes`, all with a full
64-hex sha256**. `g1_systems.csv` already enumerates them as **90 `wetlab_length_series`
rows** over the same 30 receptors, **3,600 pooled predictions**. They are missing only
from `seq_rungs.tsv`, which is why prose that reads only that file calls them absent.

---

### 4.5 Negative controls — "is it just bulk, or just a helix?"

Every peptide control runs at **the same rung the real peptide runs at**; a control at a
different length is uninterpretable. All were reproduced from bytes here, not trusted:

| construct | residues | rows | pooled | what it removes | mechanical check run here |
|---|---:|---:|---:|---|---|
| `R6a_da5` | 324–368 | 30 | 1,200 | the α5 helix, from an otherwise intact subunit | 7/7 rows reproduce as `sha256(full[:-26])` |
| `R6b_a5perm` | 350–394 | 30 | 1,200 | α5's **order**, keeping its composition in place | 7/7 hash-match; 7/7 are true permutations of wild-type α5; 0/7 equal wild type |
| `R6c_a5polyA` | 350–394 | 30 | 1,200 | α5's **side chains**, keeping its length | 7/7 reproduce as `sha256(full[:-26] + "A"*26)` |
| `ubiquitin` | 76 | 30 | 1,200 | Gα identity — an unrelated protein of mini-G scale | hash `233b4b0b8c461609…`, UniProt P0CG48 1–76 |
| `KaiB_2QKEE` | 91 | 30 | 1,200 | a second unrelated protein, different fold | hash `e7e1c7e7d0960a55…`, RCSB 2QKE entity 1, residues 5–95 |
| `ct21@polyA` | 21 | 30 | 1,200 | composition, charge, identity; **raises** helical propensity | 20/20 rows are all-alanine |
| `ct21@reversed` | 21 | 30 | 1,200 | order and register (N→C direction) | 20/20 rows equal `wt[::-1]` exactly |
| `ct21@scramble#1..5` | 21 | 150 | 1,200 | order, register and the hydrophobic face | 100/100 are permutations of wt; 0/100 equal wt |
| `ct21@face_scramble#1..3` | 21 | 90 | 1,080 | residue identity **only** — amphipathic face and helical moment preserved | 60/60 are permutations of wt; 0/60 equal wt |
| `ct21@gcn4_window` | 21 | 30 | 1,200 | any evolutionary relationship to Gα, keeping strong helical propensity | UniProt P03069 249–259 window; 20/20 differ from wt |

`R6b_a5perm` is the **true mass-matched bulk control at subunit scale** — not ubiquitin,
not KaiB.

The `peptide_control` class holds **336 rows** = 4 rungs (`ct11`, `ct15`, `ct21`,
`a5helix`) × 7 families (`Gs Gi1 Gi3 Go Gq Gt1 G13`) × 12 variants (`wt`, `reversed`,
`polyA`, `gcn4_window`, `scramble#1..5`, `face_scramble#1..3`). `seq_controls.tsv`
supplies 240 of them for 5 families; the registry generator builds the remaining **96 for
Gi3 and Go**, which `seq_controls.tsv` does not cover.

**All 28 `wt` control rows are byte-identical to the matching ladder rung** (28/28 sha
match `R1_ct11`/`R2_ct15`/`R3_ct21`/`R4_a5helix` of the same family). The control arm's
reference *is* the ladder rung, which is why `ct21@wt` is never separately dispatched.

The scramble and face-scramble sets are split into `k` draws (`n_shared_draws` in
`g1_systems.csv` divides the arm's n), so a permutation behaves as a random effect rather
than a single draw and the total prediction count is unchanged.

---

### 4.6 The mini-Gα / intermediate series

Two different things share the "mini-G" word, and the campaign keeps them apart
deliberately — `georgiou2025heterogeneity` uses "mini-Gs" for a ~229-residue construct and
for a 21-residue peptide two sentences apart, which is why preflight check **B5** refuses
any system row whose chain B has a name but no resolved numeric length.

**Synthetic intermediates (`M1`–`M5`), 16 families each, from `g1_midrungs.tsv`:**

| construct | rule | length range | rows | pooled | nested? |
|---|---|---:|---:|---:|---|
| `M1_h4s6` | CGN G.h4s6 → C-term | 44–56 | 60 | 1,500 | **yes** — below `junker`'s 50-residue boundary |
| `M2_h4` | CGN G.H4 → C-term | 60–73 | 60 | 1,500 | **yes** — the α4-β6-α5 receptor-facing motif, just above the boundary |
| `M3_h3` | CGN G.H3 → C-term | 112–130 | 30 | 1,200 | **yes** — C-terminal half of the Ras domain, mid-gap |
| `M4_he` | CGN H.HE → C-term | 203–221 | 60 | 1,500 | **yes** — first rung that re-enters the helical domain |
| `M5_dHD` | full subunit, H.HA…H.HF deleted | 236–279 | 30 | 1,200 | **NO** — keeps the N terminus |

`M5_dHD` is length-paired with `M4_he` but topologically its complement: M4 keeps the
C-terminal half of the helical domain, M5 deletes the whole of it. If they agree, length
dominates; if they disagree, composition does.

**Deposited mini-Gs (`MG_*`), from `g1_minig.tsv` — real crystallised constructs, block by
block:**

| construct | PDB | family | residues | canonical blocks kept | residues **not** matching canonical | rows | pooled |
|---|---|---|---:|---|---:|---:|---:|
| `MG_6fuf` | 6FUF entity 2 | Go (P09471) | **214** | 19-41; 44-63; 177-226; 242-249; 251-331; 336-354 | **13** | 30 | 300 |
| `MG_5g53` | 5G53 entity 2 | Gs (P63092) | **229** | 26-48; 51-62; 204-248; 264-271; 273-371; 376-394 | **23** | 30 | 300 |
| `MG_8f76` | 8F76 entity 3 | Gs (P63092) | **261** | 5-48; 51-64; 204-248; 264-371; 376-394 | **31** | 30 | 300 |

All three carry `is_pure_c_terminal_truncation = NO` — the non-matching residues are
engineered substitutions, linkers or tags. They are an **off-ladder anchor**, run only on
receptors whose cognate family matches the construct's, and they exist to tie the
synthetic M4/M5 rungs to something that has actually been crystallised.

---

### 4.7 Specificity constructs

| construct family | residues | rows | pooled | question |
|---|---:|---:|---:|---|
| `ct21@ala_pos01..21` | 21 | **210** | 4,200 | **alanine scan** — each of 21 positions → Ala, one at a time. 5 registry families (`Gs Gi1 Gq Gt1 G13`), 105 rows; dispatched on 10 receptors, all Gi1-coupled |
| `ct21@gi2gs_sub01..15` | 21 | **150** | 3,000 | **Gi → Gs walk** — 15 single substitutions, one per position where Gi1 and Gs ct21 differ. Registry family Gi1 only |
| `R2b_ct17@C379A`, `R2c_ct19@C379A`, `R3_ct21@C379A` | 17 / 19 / 21 | 18 | 180 | `mazzoni2000`'s three synthesised peptides, byte for byte. Gs-specific — the aligned position is not a cysteine in Gi1/Gq/Gt1/G13, so this is an anchor arm and not a rung |
| `R3_ct21@F376A+L388A`, `R4_a5helix@F376A+L388A` | 21 / 26 | 12 | 2,400 | the known Gs uncoupling double mutant, as a peptide |
| `R3_ct21@F376A+R380A+L388A`, `R4_a5helix@F376A+R380A+L388A` | 21 / 26 | 12 | 2,400 | the triple null, as a peptide |
| `alphas_F376A_L388A_mutant` | 394 | 6 | 1,200 | the same double mutant in the full subunit |
| `alphas_F376A_L388A_R380A_triple_null` | 394 | 6 | 1,200 | the same triple null in the full subunit |
| **family swap** (`R3_ct21`, arm `family_swap`) | 21 | 30 | 1,200 | the receptor's **non-cognate** α5-CT, chosen as argmax Hamming to cognate at ct21 over {Gs, Gi1, Gq, G13, Gt1} |
| **Gi/Gt pair** (`R1_ct11`, arm `gi_gt_single_residue`) | 11 | 30 | 1,200 | Gi1 and Gt1 both supplied to every receptor at the rung where they differ by exactly one residue |

Everything in this table was re-derived rather than read:

- **Gi1 vs Gs ct21 differ at exactly 15 positions** — 1, 4, 5, 6, 7, 9, 11, 12, 13, 14,
  16, 17, 18, 19, 21 — which is why there are 15 substitutions and not 11. The registry's
  own note says *"THE CATALOGUE SAYS 11; recomputed, Gi1 and Gs ct21 differ at 15
  positions (11 is the ct15 number, 9 is the ct11 number)."* Independently confirmed here.
- **Gi1 vs Gt1 hamming is 1 at ct11, 2 at ct15, 2 at ct21, 4 at a5helix, 6 at a5plus**
  (`IKNNLKDCGLF` vs `IKENLKDCGLF`). The single-residue arm is therefore anchored at
  `R1_ct11`; at `R3_ct21` it would be a two-substitution pair and not the experiment it is
  named for.
- **F376, R380 and L388 map to ct21 positions 3, 7 and 15** (`R`ange 374–394; residues
  `F`, `R`, `L`) and to a5helix positions 8, 12, 20. **F376 and R380 fall outside the
  11-mer** (384–394), so at `R1_ct11` the double and triple mutants collapse to the same
  molecule — registry sha `bf09617db466…` on both rows. Neither is dispatched at ct11;
  running both there would be one arm run twice.
- **Gs C379 is ct21 position 6**, so `R3_ct21@C379A` is byte-identical to Gs
  `ct21@ala_pos06` (both sha `087df286de75…`). Expected, and a useful internal consistency
  proof.

#### Four alanine positions are no-ops

Four `ala_scan` rows are byte-identical to their family's wild-type ct21, because the
position is already alanine:

| family | position | already |
|---|---:|---|
| Gi1 | 5 | A |
| Gq | 4 | A |
| Gq | 5 | A |
| Gt1 | 5 | A |

The registry flags each with `note` beginning `NO-OP:` and preflight **B6** treats those
as declared free wild-type replicates rather than as a within-arm molecule collision. My
independent recomputation found exactly the same four rows — no more, no fewer.

**Consequence for the dispatched arm:** all 10 `ala_scan` receptors resolve to **Gi1**, so
`ct21@ala_pos05` (10 rows, 200 pooled predictions) is a wild-type replicate. The
alanine scan as dispatched has **20 informative positions, not 21**, and must be described
that way. (Gq's `ala_pos04`/`ala_pos05` are also identical to each other — sha
`ca9c43b3512d…` — but Gq is not among the dispatched families.)

---

### 4.8 Reference-matched tips — and the collision inside them

Twelve receptors have a Rule-R ACTIVE deposited reference whose Gα α5 tip is **not
canonical for any of the 17 human Gα families**. The registry holds each deposit's own
tip so the model can be asked whether it cares about the residues that separate them.

`ref_tip`, 23 rows, all `held=yes`, from `g1_refchimera.tsv`:

| receptor | PDB entity | deposited partner len | `reftip_ct11` | `reftip_ct21` | nearest canonical |
|---|---|---:|---|---|---|
| 5HT2A | 8UWL_2 | 246 | `LQMNLREYNLV` | `RIFNDCKDIILQMNLREYNLV` | G11, Hamming 2/11 |
| 5HT2C | 8DPF_2 | 246 | same | same | G11, 2/11 |
| ADA1A | 7YM8_1 | 246 | same | same | G11, 2/11 |
| EDNRA | 8HCQ_1 | 246 | same | same | G11, 2/11 |
| GRPR | 8H0Q_3 | 361 | same | same | G11, 2/11 |
| HRH1 | 8YN2_1 | 246 | same | same | G11, 2/11 |
| OX2R | 7L1V_1 | 244 | same | same | G11, 2/11 |
| OXYR | 7RYC_3 | 326 | same | same | G11, 2/11 |
| TA2R | 8XJN_1 | 246 | same | same | G11, 2/11 |
| DRD4 | 8IRU_1 | 361 | `IKMNLRDCGLF` | `RIFNDVTDIIIKMNLRDCGLF` | Ggust, 2/11 |
| B1B1U5 | 9EPP_2 | 352 | `LQNNLKECNLV` | `FVFCAVKDTILQNNLKECNLV` | G11, 2/11 (identity 0.86 at ct21) |
| OPSD | 4X1H_2 | **11** | `VLEDLKSCGLF` | *(none)* | Ggust, 4/11 — C-terminus unrecognised at 0.64 |

**Nine of the twelve `reftip_ct11` rows are the same molecule** (sha `ceb5781d7f4b…`) and
**nine of the eleven `reftip_ct21` rows are the same molecule** (sha `c63a424ec6f9…`):
the Gi2-scaffold/mini-Gq-tip chimera used across most of these structures. Only 4 distinct
`reftip_ct11` sequences and 3 distinct `reftip_ct21` sequences exist across all 12
receptors. **None of the 23 matches any canonical human Gα ct11 or ct21 hash.**

OPSD's deposited partner is an 11-residue peptide, so it has no `reftip_ct21` cell — 12
ct11 rows + 11 ct21 rows = 23, matching the 23-row `reference_matched_tip` arm exactly
(480 + 440 = 920 pooled predictions).

`g1_refchimera.tsv` itself has 13 rows because ADA1A has two qualifying deposits (7YM8 and
8THK, identical tips); only 7YM8 reaches the registry.

---

### 4.9 Species-matched (spider) tips — the D-H extension arm

`tejero2024opsin` (Nat Commun 2024;15:8928) Methods p10 records **18 residues** of spider
Gαq1 (INSDC LC799818, aligned to Gi1 337–354). We do not hold LC799818 itself.

**Held, 5 rows, `species_matched_tip`, family `B1B1U5`:**

| construct | residues | sha256 (16) |
|---|---:|---|
| `spidertip_R1_ct11` | 11 | `d1d0f8709eaeb247` |
| `spidertip_R1b_ct13` | 13 | `5b67a13c34c056b3` |
| `spidertip_R2_ct15` | 15 | `43477dc528c9e56a` |
| `spidertip_R2b_ct17` | 17 | `9e8e890334524084` |
| `spidertip_ct18` | **18** | `1e20c2435d0d78ec` — the ceiling; the longest species-matched construct the source supports |

`spidertip_R1_ct11` is **byte-identical to `ref_tip/reftip_ct11/9EPP`** (`d1d0f8709eae…`):
at 11 residues the whole window lies inside the spider segment, so the species-matched arm
and the deposited-tip arm are literally the same molecule at that rung. They diverge at
13 and above.

This arm is an **EXTENSION**, deliberately outside the primary ladder, because it puts a
non-human partner into a human-partner ladder. None of the five is currently enumerated in
`g1_systems.csv`.

---

### 4.10 Non-Gα chains

`non_ga_chain`, 5 rows, all fetched live and hash-checked against `SEQUENCES.md`:

| construct | residues | source | sha256 (16) | used as |
|---|---:|---|---|---|
| `gcn4_leucine_zipper_33` | 33 | UniProt P03069 249–281 | `9569a7eb08514dbd` | **not dispatched** — only the 21-residue window `ct21@gcn4_window` is |
| `ubiquitin` | 76 | UniProt P0CG48 1–76 | `233b4b0b8c461609` | chain B, `non_ga_bulk`, 30 rows |
| `KaiB_2QKEE` | 91 | RCSB 2QKE entity 1, residues 5–95 | `e7e1c7e7d0960a55` | chain B, `non_ga_bulk`, 30 rows |
| `Gbeta1` | **340** | UniProt P62873 | `731c013dfd2af08e` | **chain C**, not chain B — the `R8_hetero` arm |
| `Ggamma2` | **71** | UniProt P59768 | `32ec703375c0e761` | **chain C**, not chain B — the `R8_hetero` arm |

340 + 71 = **411**, which is exactly the offset `g1_systems.py` adds to `R7_full` to get
`R8_hetero`'s reported chain length.

---

### 4.11 The ten rows with `held=NO`, and the one mislabel

`awk -F'\t' 'NR>1 && $8!="yes"' g1_partner_registry.tsv`

| construct | class | stated length | sha256 | why not held |
|---|---|---|---|---|
| `spidertip_R2c_ct19` | not_dispatchable | 19 | `UNKNOWN` | needs 19 spider residues; the source records only 18. The missing 1 would have to come from LC799818, which we do not hold |
| `spidertip_R3_ct21` | not_dispatchable | 21 | `UNKNOWN` | needs 21; 3 missing. The deposited 21-mer at 9EPP is **not** a spider 21-mer — its first three residues are human backbone |
| `spidertip_R4_a5helix` | not_dispatchable | 26 | `UNKNOWN` | 8 missing |
| `spidertip_R5_a5plus` | not_dispatchable | 36 | `UNKNOWN` | 18 missing |
| `spidertip_R6a_da5` | not_dispatchable | **UNKNOWN** | `UNKNOWN` | D-H has no full-subunit form; LC799818 records 18 residues, not a subunit |
| `spidertip_R7_full` | not_dispatchable | **UNKNOWN** | `UNKNOWN` | same |
| `random_helix_40mer` | not_dispatchable | 40 | `UNKNOWN` | a 40-aa designed helix; its recorded hash is not derivable from any database record. It was to be the helicity-matched arm; the substitute is `gcn4_window` at matched rung length |
| `arrestin_Ctail` | not_dispatchable | 41 | `UNKNOWN` | no 41-mer window of P49407, P32121, P08168, P10523, P30518, P08100 or P02699 hashes to the recorded prefix. Source unresolved |
| `DAMGO` | not_dispatchable | 5 | `UNKNOWN` | a synthetic opioid peptidomimetic; not a UniProt subsequence |
| `Nb60` | not_dispatchable | 126 | `UNKNOWN` | carries the Nb80 CDR3 and is not byte-identical to RCSB 3P0G entity 2 or 4LDE entity 2 |
| `arrestin_FL` | not_dispatchable | 15 | `a0a09ab53dbc98a2...` | **held but mislabelled** — 15 bytes = β-arrestin-1 P49407 residues 22–36, a β-strand of the N-domain, not the finger loop and not full length. Must be respecified from a named source before use |

**Two constructs have `length = UNKNOWN`: `spidertip_R6a_da5` and `spidertip_R7_full`.**
Ten have `sha256 = UNKNOWN`.

`arrestin_FL`'s sha256 field is a **16-hex prefix followed by a literal `...`** — not a
hash. Preflight **B3** tests only rows with `held == "yes"`, so it does not fire on this
row; **B4** (`held != "yes"` must not be dispatched) is what keeps it out of the run, and
it is indeed referenced by zero `g1_systems.csv` rows. The guard is sound, but the field
is a placeholder, not a value.

---

### 4.12 What is held but never dispatched

**503 of the 782 registry rows are reachable from at least one `g1_systems.csv` row; 279
are not.**

| unreachable | rows | why |
|---|---:|---|
| `peptide_control` at `ct11`, `ct15`, `a5helix` | 252 | only the **ct21** controls are enumerated; the shorter and longer control sets are built and hashed but not costed |
| `peptide_control` `ct21@wt` | 7 | the wild-type control *is* `R3_ct21`, already dispatched in the ladder arm |
| `not_dispatchable` | 11 | by definition |
| `species_matched_tip` | 5 | the D-H extension arm is specified but not enumerated |
| `non_ga_chain` `Gbeta1`, `Ggamma2`, `gcn4_leucine_zipper_33` | 3 | the first two run as chain C; the third only as its 21-mer window |
| `boundary_variant` `R4b_a5helix27` | 1 | a reconciliation artefact, held so the 26-vs-27 convention is auditable |

Expanding the control set from ct21 to all four rungs is therefore a **free** construction
decision — the bytes already exist and are hashed; only the GPU cost is new.

---

### 4.13 Where chain B is still unresolved

`g1_systems.csv:chain_b_sha256` resolution state over all 2,039 rows:

| state | rows | meaning |
|---|---:|---|
| full 64-hex sha256 | **1,451** | fully pinned |
| `resolved, explicit (see g1_partner_registry.tsv)` | 294 | pinned, but the hash is not copied into this file (arms `gi_to_gs_series`, `deposited_minig_anchor`, `uncoupling_peptide`, `wetlab_matched_peptides`, `uncoupling_full`) |
| `-` | 94 | `R0_apo` — there is no chain B |
| `resolved, family-invariant` | 90 | the three `non_ga_bulk` cells, identical for every receptor |
| Gi1 + Gt1 pair hash | 30 | `gi_gt_single_residue`, both supplied |
| heterotrimer triple hash | 30 | `R8_hetero`: cognate `R7_full` + `731c013dfd2af08e` + `32ec703375c0e761` |
| **`PENDING:COUPLING.md`** | **30** | `family_swap` — the non-cognate partner is chosen by a rule (argmax Hamming) that has not yet been executed |
| **`PENDING:PI-DECISION`** | **20** | `chimeric_ref_extension` — 10 receptors × `R3_ct21` and `R7_full`, `CHIMERA_SPLIT` evidence: tip says Gq (or Gi1), scaffold says Gs, and nobody has chosen |

**50 rows out of 2,039 have no chain-B molecule fixed yet.** The ten receptors awaiting a
PI decision are `5HT2A 5HT2C ADA1A DRD4 EDNRA GRPR HRH1 OX2R OXYR TA2R`; all ten sit in
the `EXTENSION-chimeric-reference` tier and cannot enter a primary count.

---

### 4.14 Dispatch summary for Group 1

`g1_systems.csv` holds **2,039 rows, 23 arms, 10 experiments (E1.1–E1.9), 82 distinct
`chain_b_construct` labels, 64 receptors in 32 clusters**, every row enumerated per
receptor with nothing templated.

- Tier: **PRIMARY 1,917**, `EXTENSION-census` 72, `EXTENSION-chimeric-reference` 50.
- Chain count: **1,915 two-chain, 94 one-chain (`R0_apo`), 30 three-chain (`R8_hetero`)`.
- Partner MSA: **off on 1,855 rows** (the primary condition), `ON` on 90 (`partner_msa_on`,
  the E1.9 contrast), `n/a` on 94 (`R0_apo`).
- Ligand: **`none` on all 2,039 rows** — Group 1 is ligand-free by construction; the
  ligand work is Group 2 (`g2_systems.csv`).
- Receptor MSA: `on (default)` on all 2,039 rows.
- Backbones: all four (`boltz2|openfold3|protenix|chai1`) on 1,271 rows; `boltz2` alone on
  768 (the pilots).
- Total budget: **74,960 pooled predictions / 212,920 per-cell**.

Partner family as dispatched, from `supplied_partner_family`:

| family | all rows | **excluding `R0_apo`** |
|---|---:|---:|
| Gi/o | 1,517 | **1,455** |
| Gs | 372 | **354** |
| Gq/11 | 150 | **136** |

The second column is the honest one: `supplied_partner_family` is a **per-receptor
annotation** carried on every row of that receptor, including the 94 `R0_apo` rows that
have no partner at all. Partner subtypes actually named: Gi1 1,401 · Gs 372 · Gq 150 ·
Gt1 51 · Gi3 50 · Go 15.

---

# Part 5. The ligands

Everything in this section is recomputed from `redo/inputs/g2_systems.csv`
(350 data rows, 47 columns, sha256 `7846c009…a8c5f1`, generator
`redo/build/g2_systems.py`, hash confirmed live against `inputs/MANIFEST.tsv`).
Nothing here has run: Group 2 is enumerated, gated and frozen, and zero GPU
time has been spent.

### 1. What this file is

`g1_systems.csv` (2,039 rows) enumerates the **partner-length** axis and carries
`ligand = none` on every one of its rows — verified, 2039/2039. `g2_systems.csv`
is the other half of the crossing: it varies the **ligand** while holding the
partner axis at three levels. Chain A is always the GPCR; chain B is the partner;
a ligand is either a non-polymer entity (a HETATM component, `ligand_is_chain = 0`)
or **an additional polymer chain** (`ligand_is_chain = 1`). That distinction is
the whole reason the tiers exist — §8.

The file covers **26 receptors in 25 paralog clusters**, all Class A
(D-2026-09-12-d), drawn from the frozen primary panel of 30 receptors / 29
clusters in `ligand_tiers.tsv`. The four PRIMARY receptors not present here
(`APJ`, `GPR52`, `MTR1A`, `TSHR`) are tier `X_single_sided` — they have a ligand
on one state only, so they cannot carry an agonist/antagonist contrast at all.

### 2. Two role columns, and why

Every row carries **both** `ligand` (the *design level*) and `ligand_role_actual`
(the *pharmacology*). They are not the same, and conflating them is a blocking
failure (gate check **G-4**).

| `ligand` (design level) | → `ligand_role_actual` | rows |
|---|---|---:|
| `none` | `none` | 98 |
| `full_agonist` | `full_agonist` | 100 |
| `antagonist` | `neutral_antagonist` | 79 |
| `antagonist` | **`inverse_agonist`** | **19** |
| `inverse_agonist` | `inverse_agonist` | 6 |
| `decoy_lig` | `decoy_lig` | 48 |

**`antagonist` is a level, not a molecule.** It resolves per receptor. Where a
receptor has no plain antagonist in the curation at all, the level is filled by an
inverse agonist and recorded as one — never relabelled. That happens on **five
receptors**: `ADRB1`, `B1B1U5`, `OPSD` (the three T1 cases that amendment C-1's
relaxation unblocked, D-2026-09-12-f) plus `AGTR1` and `NTR1` in T3.

The six `ligand = inverse_agonist` rows are a *separate* level — the E2.3 efficacy
ladder — on `AA2AR`, `ACM4` and `DRD3`, receptors that already have a plain
neutral antagonist. These are extra, not substitutes.

### 3. The complete ligand roster

**66 distinct `(ligand_name, ligand_ccd, ligand_inchikey)` triples** appear on the
252 ligand-bearing rows. Each resolved decoy cell carries **three** molecules
pipe-delimited in one row (`n_shared_draws = 3`, the three decoys *are* the three
draws), so after splitting those bundles the file names **85 distinct chemical
entities**: 25 full agonists, 20 neutral antagonists, 7 inverse agonists and
**33 D-RULE decoys**.

Columns: **chain** = `ligand_is_chain`; **key** = `ligand_must_key_by`, the field
a pipeline must join on; **levels** = which partner levels the ligand is
enumerated at (`apo` = `R0_apo`, `ct21` = `R3_ct21`, `full` = `R7_full`).
Decoy triples are shown with `·` where the file uses `|`.

#### 3.1 T1 — small-molecule tier (17 receptors, 16 clusters; 16 / 15 curated)

| receptor | role | ligand | CCD | InChIKey | chain | provenance | key | dispatch | levels | rows |
|---|---|---|---|---|---|---|---|---|---|---:|
| 5HT5A | full_agonist | 5-carboxamidotryptamine (5-CT) | 8K3 | WKZLNEWVIAGNAW-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| 5HT5A | neutral_antagonist | compound-N6 (Zhang 2022 tool) | NN6 | YBJHLGWWZWMRCD-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| 5HT5A | decoy_lig | CHEMBL1490875 · CHEMBL3289526 · CHEMBL3289540 | – | PEHSVUKQDJULKE · VCMVENPCUDGFSK · GQGXTXAPHRNTIO (all -UHFFFAOYSA-N) | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| AA1R | full_agonist | adenosine | ADN | OIRDTQYFTABQOQ-KQYNXXCUSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| AA1R | neutral_antagonist | DPCPX / CPX / PD-116948 | – | FFBDFADSZUINTG-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| AA1R | decoy_lig | *(none — `fewer_than_k_accepted`)* | – | – | 0 | BLOCKED_DECOY_UNAVAILABLE | inchikey | **BLOCKED** | apo+ct21+full | 3 |
| AA2AR | full_agonist | NECA (5′-N-ethylcarboxamidoadenosine) | NEC | JADDQZYHOWSFJD-FLNNQWSLSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| AA2AR | neutral_antagonist | ZM241385 | ZMA | PWTBZOIUWZOPFT-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| AA2AR | inverse_agonist | preladenant (SCH-420814) | – | DTYWJKSSUANMHD-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21 | 2 |
| AA2AR | decoy_lig | *(none — `fewer_than_k_accepted`)* | – | – | 0 | BLOCKED_DECOY_UNAVAILABLE | inchikey | **BLOCKED** | apo+ct21+full | 3 |
| ACM4 | full_agonist | iperoxo | IXO | WXXOCGISBCTWPW-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| ACM4 | neutral_antagonist | tiotropium cation | 0HK | LERNTVKEWCAPOY-FPISHFTHSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| ACM4 | inverse_agonist | atropine | – | RKUNBYITZUJHSG-PJPHBNEVSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21 | 2 |
| ACM4 | decoy_lig | CHEMBL166330 · CHEMBL284257 · CHEMBL502684 | – | KPXVKKBJROCIJB · XYFBJOKZCLYMEM · OFBLNBCFCXAZGW (all -UHFFFAOYSA-N) | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| ADRB1 | full_agonist | CHEMBL1615159 | P0G | NWQXBEWHTDRJIP-KRWDZBQOSA-N | 0 | RESOLVED_REDO (7BU7) | **ccd** | READY | apo+ct21+full | 5 |
| ADRB1 | inverse_agonist | carazolol *(fills the antagonist level)* | CAU | BQXQGZPYHWWCEB-ZDUSSCGKSA-N | 0 | RESOLVED_REDO (7BVQ) | **ccd** | READY | apo+ct21+full | 5 |
| ADRB1 | decoy_lig | CHEMBL1098442 · CHEMBL3401301 · CHEMBL4760919 | – | QFKNUCVKOWGNCX-LBPRGKRZSA-N · YASYZUJSAWTGNM-UHFFFAOYSA-N · CKOYOYZZWAJOMZ-HNNXBMFYSA-N | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| B1B1U5 | full_agonist | 11,20-ethanoretinal | A1H6M | FOYUFPJPFUUNOX-ZRTTZBFNSA-N | 0 | RESOLVED_REDO (9EPP) | **ccd** | READY | apo+ct21+full | 5 |
| B1B1U5 | inverse_agonist | **retinal (11-cis)** | RET | NCYCYZXNIZJOKI-**IOUUIBBYSA**-N | 0 | RESOLVED_REDO (6I9K) | **inchikey** | READY | apo+ct21+full | 5 |
| B1B1U5 | decoy_lig | *(none — `eligibility_unestablishable_no_chembl_target`)* | – | – | 0 | BLOCKED_DECOY_UNAVAILABLE | inchikey | **BLOCKED** | apo+ct21+full | 3 |
| CCKAR | full_agonist | SR146131 | IA1 | NFDFTMICKVDYLQ-UHFFFAOYSA-N | 0 | RESOLVED_REDO (7XOV) | **ccd** | READY | apo+ct21+full | 5 |
| CCKAR | neutral_antagonist | devazepide (MK-329, L-364,718) | 1OZ | NFHRQQKPEBFUJK-HSZRJFAPSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| CCKAR | decoy_lig | CHEMBL1669025 · CHEMBL306924 · CHEMBL96554 | – | UCVTWXSYIUJCNM · TYTZWWYHRHCWBP · IKSMFLPUCVAYHQ (all -UHFFFAOYSA-N) | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| CNR2 | full_agonist | CB2 phenol-cyclohexanol agonist (HU-308-type, 8GUR) | 9GF | YNZFFALZMRAPHQ-SYYKKAFVSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| CNR2 | neutral_antagonist | AM10257 | 9JU | FMJXYCCDMAGPLE-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| CNR2 | decoy_lig | CHEMBL2336073 · CHEMBL270026 · CHEMBL3671056 | – | NQSBLPSEBZEEPP-MTDXEUNCSA-N · NCTDWZFQXDIUEY-SANMLTNESA-N · RFSPCEJTXAVJPJ-HXUWFJFHSA-N | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| DRD3 | full_agonist | PD 128907 | G6O | YOILXOMTHPUMRG-TZMCWYRMSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| DRD3 | neutral_antagonist | S-(−)-eticlopride | ETQ | AADCDMQTJNYOSS-LBPRGKRZSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| DRD3 | inverse_agonist | haloperidol | – | LNEPOXFFQSENCJ-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21 | 2 |
| DRD3 | decoy_lig | CHEMBL156131 · CHEMBL4739937 · CHEMBL6189412 | – | CISTXXCPQIZSIS-UHFFFAOYSA-N · NMQSOAPOAUZPPJ-WCBMZHEXSA-N · SJLUDZSXHFQCFJ-UHFFFAOYSA-N | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| GHSR | full_agonist | ibutamoren | 1KD | UMUPQWIGCOZEOY-JOCHJYFZSA-N | 0 | RESOLVED_REDO (7NA8) | **ccd** | READY | apo+ct21+full | 5 |
| GHSR | neutral_antagonist | CHEMBL1956994 | 8QX | LMBFVVBQYYWDKN-INIZCTEOSA-N | 0 | RESOLVED_REDO (6KO5) | **ccd** | READY | apo+ct21+full | 5 |
| GHSR | decoy_lig | CHEMBL302063 · CHEMBL3901466 · CHEMBL483469 | – | NIVVQBFSLKXZPE-DHIUTWEWSA-N · YIJXZOJTKRAPAH-VKDGWMQASA-N · XGGZNUZGXSDCLP-UHFFFAOYSA-N | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| HRH3 | full_agonist | histamine | HSM | NTYJJOPFIAHURM-UHFFFAOYSA-N | 0 | RESOLVED_REDO (8YN5) | **ccd** | READY | apo+ct21+full | 5 |
| HRH3 | neutral_antagonist | PF-03654746 (bavisant) | 1IB | SXMBKHYDZOCBMT-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| HRH3 | decoy_lig | *(none — `fewer_than_k_accepted`)* | – | – | 0 | BLOCKED_DECOY_UNAVAILABLE | inchikey | **BLOCKED** | apo+ct21+full | 3 |
| LPAR1 | full_agonist | 1-oleoyl-LPA (LPA 18:1) | **MALFORMED_PROVENANCE** | WRGQSWVCFNIUNZ-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| LPAR1 | neutral_antagonist | ONO-3080573 | ON3 | FVESDCZDESZGHA-URLMMPGGSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| LPAR1 | decoy_lig | *(none — `fewer_than_k_accepted`)* | – | – | 0 | BLOCKED_DECOY_UNAVAILABLE | inchikey | **BLOCKED** | apo+ct21+full | 3 |
| LT4R1 | full_agonist | leukotriene B4 (LTB4) | LTB | VNYSSYRCGWBHLG-AMOLWHMGSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| LT4R1 | neutral_antagonist | MK-D-046 | VRJ | DJXXSNJFTPBZSH-BXKMTCNYSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| LT4R1 | decoy_lig | CHEMBL117031 · CHEMBL119562 · CHEMBL4649582 | – | KARRQFDDSYYFAE · ATXJVJPQVHFGIA · BZFMOMUMMMUZDV (all -UHFFFAOYSA-N) | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| OPRD | full_agonist | DPI-287 | OWY | PQMGDEIHRXQPCQ-FSGGQHMVSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| OPRD | neutral_antagonist | naltrindole | EJ4 | WIYUZYBFCWCCQJ-IFKAHUTRSA-N | 0 | INHERITED_SMILES_PARSED | inchikey | READY | apo+ct21+full | 5 |
| OPRD | decoy_lig | CHEMBL3676860 · CHEMBL4797752 · CHEMBL5646702 | – | OXYSILQZQLVAHW-AQYVVDRMSA-N · HDFGGNSQPFXQRL-UHFFFAOYSA-N · OZWIFUZORWEWKP-AREMUKBSSA-N | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| OPSD | full_agonist | **retinal (all-trans)** | RET | NCYCYZXNIZJOKI-**OVSJKPMPSA**-N | 0 | RESOLVED_REDO (5DYS) | **inchikey** | READY | apo+ct21+full | 5 |
| OPSD | inverse_agonist | **retinal (11-cis)** *(fills the antagonist level)* | RET | NCYCYZXNIZJOKI-**IOUUIBBYSA**-N | 0 | RESOLVED_REDO (7ZBC) | **inchikey** | READY | apo+ct21+full | 5 |
| OPSD | decoy_lig | CHEMBL125010 · CHEMBL261494 · CHEMBL4761208 | – | DZTLWQKJNBRKAL-UHFFFAOYSA-N · WMICXNJEJDOUPN-SJLPKXTDSA-N · AIEKRROFITYDKB-WEVVVXLNSA-N | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |
| PD2R2 | full_agonist | **REFUSED** | – | – | 0 | BLOCKED_LIGAND_IDENTITY | inchikey | **BLOCKED** | apo+ct21 | 2 |
| S1PR1 | full_agonist | siponimod | J8C | KIHYPELVXPAIDH-HNSNBQBZSA-N | 0 | RESOLVED_REDO (7TD4) | **ccd** | READY | apo+ct21+full | 5 |
| S1PR1 | neutral_antagonist | W146 | ML5 | FWJRVGZWNDOOFH-OAHLLOKOSA-N | 0 | RESOLVED_REDO (3V2Y) | **ccd** | READY | apo+ct21+full | 5 |
| S1PR1 | decoy_lig | CHEMBL462053 · CHEMBL5080279 · CHEMBL5593523 | – | DNCAQTJFFOGJNV-UHFFFAOYSA-N · KLBPFBHIAMXJAI-GMKZXUHWSA-N · RUNGRPLELDGZQJ-UHFFFAOYSA-N | 0 | RESOLVED_DRULE_DECOY | inchikey | READY | apo+ct21+full | 3 |

#### 3.2 T2 — peptide tier (2 receptors, 2 clusters). **Every pharmacological row is blocked.**

| receptor | role | ligand | CCD | InChIKey | chain | provenance | dispatch | levels | rows |
|---|---|---|---|---|---|---|---|---|---:|
| C5AR1 | full_agonist | BM213 | – | – | **1** | REDO:ligand_set_redo.tsv (7Y66) | BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE | apo+ct21 | 2 |
| C5AR1 | neutral_antagonist | PMX53 | – | – | **1** | REDO:ligand_set_redo.tsv (6C1R) | BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE | apo+ct21 | 2 |
| SSR2 | full_agonist | somatostatin | – | – | **1** | REDO:ligand_set_redo.tsv (7T10) | BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE | apo+ct21 | 2 |
| SSR2 | neutral_antagonist | CYN 154806 | – | – | **1** | REDO:ligand_set_redo.tsv (7XNA) | BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE | apo+ct21 | 2 |

Only T2's four ligand-free rows are READY. `ligand_set_redo.tsv` carries a SMILES
for somatostatin, and **a SMILES is not a chain input** — the whole axis of this
tier is chain-ness, so a chain row with no sequence is unresolved however much
chemistry sits beside it.

#### 3.3 T3 — mixed tier (7 receptors, 7 clusters). Agonist is a chain, antagonist is not.

| receptor | role | ligand | CCD | InChIKey | chain | provenance | dispatch | rows |
|---|---|---|---|---|---|---|---|---:|
| AGTR1 | full_agonist | angiotensin II (DRVYIHPF, native 8-mer) | – | – | **1** | INHERITED_CHAIN_SEQUENCE (6OS0) | READY | 2 |
| AGTR1 | inverse_agonist | olmesartan free acid | OLM | VTRAEEWXHOVJFV-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED (4ZUD) — flagged `source_row_role_disagrees_with_gpcrdb` | READY | 2 |
| CCR2 | full_agonist | C-C motif chemokine 2 (CCL2) | – | – | **1** | UNCURATED (named in `ligand_tiers.tsv`, no bytes) | BLOCKED_UNRESOLVED_UNCURATED | 2 |
| CCR2 | neutral_antagonist | MK-0812 | – | – | 0 | UNCURATED | BLOCKED_UNRESOLVED_UNCURATED | 2 |
| EDNRB | full_agonist | endothelin-1 (native 21-mer, 2 disulfides) | – | – | **1** | INHERITED_CHAIN_SEQUENCE (8IY6) | READY | 2 |
| EDNRB | neutral_antagonist | bosentan | K86 | GJPICJJJRGTNOD-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED (5XPR) | READY | 2 |
| MCHR1 | full_agonist | MCH (19-mer cyclic, C7–C16 disulfide) | – | – | **1** | INHERITED_CHAIN_SEQUENCE (8WWK) | READY | 2 |
| MCHR1 | neutral_antagonist | SNAP-94847 | A1D6T | VMLZFUVIKCGATC-UHFFFAOYSA-N | 0 | INHERITED_SMILES_PARSED (8YNS) | READY | 2 |
| NK1R | full_agonist | substance P | – | – | **1** | UNCURATED | BLOCKED_UNRESOLVED_UNCURATED | 2 |
| NK1R | neutral_antagonist | L760735 | – | – | 0 | UNCURATED | BLOCKED_UNRESOLVED_UNCURATED | 2 |
| NPY1R | full_agonist | neuropeptide Y (native 36-mer, C-terminally amidated) | – | – | **1** | INHERITED_CHAIN_SEQUENCE (7X9A) | READY | 2 |
| NPY1R | neutral_antagonist | UR-MK299 | 9AO | VQHNWOOVOKYJNL-HHHXNRCGSA-N | 0 | INHERITED_SMILES_PARSED (5ZBQ) | READY | 2 |
| NTR1 | full_agonist | JMV431 | – | – | **1** | UNCURATED | BLOCKED_UNRESOLVED_UNCURATED | 2 |
| NTR1 | inverse_agonist | meclinertant (SR48692) | – | – | 0 | UNCURATED | BLOCKED_UNRESOLVED_UNCURATED | 2 |

**Endothelin-1 is exactly 21 residues**, the same length as the `R3_ct21` partner
peptide. D-2026-09-12-f retired the hazard where it would have shared a prediction
with `ct21` by placing EDNRB in T3 rather than T2.

### 4. Identity provenance

`ligand_identity_status` is the authoritative provenance field. Every value, with
its live count (sums to 350):

| status | rows | what it means |
|---|---:|---|
| `RESOLVED_NO_LIGAND` | 98 | the ligand-free level; `n_nonpolymer_entities = 0` on all 98 |
| `INHERITED_SMILES_PARSED` | 114 | `paper_af3`'s `ligand_set.csv` / `ligand_set_tier3.csv` — files **we do not hold**; SMILES re-parsed and InChIKey recomputed here |
| `RESOLVED_REDO` | 60 | our own enacted picks, `redo/inputs/ligand_set_redo.tsv` |
| `RESOLVED_DRULE_DECOY` | 33 | D-RULE selection from a pinned ChEMBL_37 pool, `drule_selected.tsv` |
| `BLOCKED_DECOY_UNAVAILABLE` | 15 | D-RULE refused the receptor; carried at zero, named |
| `UNRESOLVED_UNCURATED` | 12 | named by the GPCRdb census, no bytes held (CCR2, NK1R, NTR1) |
| `INHERITED_CHAIN_SEQUENCE` | 8 | T3 peptide agonists whose sequence came in the received bundle |
| `UNRESOLVED_CHAIN_NO_SEQUENCE` | 8 | T2 — curated *structurally*, sequence nowhere in `redo/inputs/` |
| `BLOCKED_LIGAND_IDENTITY` | 2 | PD2R2, refused |

**Nine T1 receptors carry ligands that are inherited only** — `5HT5A AA1R AA2AR
ACM4 CNR2 DRD3 LPAR1 LT4R1 OPRD` — recomputed here and matching
D-2026-09-12-f exactly. Their tier eligibility is independently derived from the
GPCRdb snapshot, but their SMILES and roles are not inspectable on our side.
This is the largest unverified surface in the ligand arm. Five T1 receptors are
entirely redo-resolved (`ADRB1 B1B1U5 GHSR OPSD S1PR1`); two are mixed
(`CCKAR HRH3`).

#### 4.1 The join key, and why it is not always the CCD

`ligand_must_key_by` says which field a downstream pipeline must join on:
**199 rows keyed by InChIKey, 53 by CCD, 98 not applicable** (ligand-free).

`redo/build/ligand_ccd_verify.py` compares every CCD-sourced pick to RCSB and
writes `ligand_ccd_verification.tsv`: **10 `ok`, 2 `STEREO_DIFFERS`, 4
`n/a_chain`** (16 rows). The two mismatches are the demonstration behind F-11:

> RCSB's canonical **`RET` is all-trans retinal** (`NCYCYZXNIZJOKI-OVSJKPMPSA-N`),
> the **agonist** form. Both our inverse-agonist picks are **11-cis**
> (`NCYCYZXNIZJOKI-IOUUIBBYSA-N`). A pipeline resolving `RET` through the CCD
> silently gets the agonist where the row says inverse agonist. It bites
> **B1B1U5 as well as OPSD**, which a within-receptor shared-CCD test misses.

Those **10 rows** (5 per receptor across the three partner levels) carry
`ligand_flag = ccd_resolves_to_other_isomer` and `must_key_by = inchikey`.
`RET` is the only CCD in the file used for two different molecules.

#### 4.2 The other `ligand_flag` values

| flag | rows | meaning |
|---|---:|---|
| *(empty)* | 285 | nothing to declare |
| `EXPLORATORY_MISSED_PREREG_CLUSTER_BAR` | 33 | every resolved decoy row — see §6.1 |
| `EXPLORATORY_MISSED_PREREG_CLUSTER_BAR; DECOY_UNAVAILABLE:fewer_than_k_accepted` | 12 | AA1R, AA2AR, HRH3, LPAR1 |
| `EXPLORATORY_MISSED_PREREG_CLUSTER_BAR; DECOY_UNAVAILABLE:eligibility_unestablishable_no_chembl_target` | 3 | B1B1U5 |
| `ccd_resolves_to_other_isomer` | 10 | 11-cis retinal on B1B1U5 and OPSD |
| `column_shift_in_source_row` | 5 | LPAR1's full-agonist row; `ligand_ccd` reads `MALFORMED_PROVENANCE` (F-18). Detected **by shape** — a CCD containing a space or longer than five characters — not by name. Chemistry unaffected; the InChIKey is sound |
| `source_row_role_disagrees_with_gpcrdb` | 2 | AGTR1's olmesartan: `ligand_set_tier3.csv` keys `OLM` @ 4ZUD as `neutral_antagonist`, GPCRdb types it **inverse agonist**. Taken under the census's role and flagged, not absorbed |

### 5. The design: ligand role × partner level

Three partner levels: `R0_apo` (no chain B, `chain_b_len = 0`), `R3_ct21` (the
21-residue Gα C-terminal peptide, the title's rung) and `R7_full` (the whole
cognate Gα subunit, 350–394 aa). Partner MSA is **off** on every cognate row and
`n/a` on every apo row, so a G1 row and a G2 row at the same rung differ in the
ligand and nothing else (gate **G-11**).

#### 5.1 All 350 rows

| `ligand_role_actual` | R0_apo | R3_ct21 | R7_full | total |
|---|---:|---:|---:|---:|
| `none` | 41 | 41 | 16 | 98 |
| `full_agonist` | 42 | 42 | 16 | 100 |
| `neutral_antagonist` | 33 | 33 | 13 | 79 |
| `inverse_agonist` | 11 | 11 | 3 | 25 |
| `decoy_lig` | 16 | 16 | 16 | 48 |
| **total** | **143** | **143** | **64** | **350** |

#### 5.2 READY only (313 rows)

| `ligand_role_actual` | R0_apo | R3_ct21 | R7_full | total |
|---|---:|---:|---:|---:|
| `none` | 41 | 41 | 16 | 98 |
| `full_agonist` | 36 | 36 | 16 | 88 |
| `neutral_antagonist` | 29 | 29 | 13 | 71 |
| `inverse_agonist` | 10 | 10 | 3 | 23 |
| `decoy_lig` | 11 | 11 | 11 | 33 |
| **total** | **127** | **127** | **59** | **313** |

#### 5.3 BLOCKED only (37 rows)

| `ligand_role_actual` | R0_apo | R3_ct21 | R7_full | total |
|---|---:|---:|---:|---:|
| `none` | 0 | 0 | 0 | **0** |
| `full_agonist` | 6 | 6 | 0 | 12 |
| `neutral_antagonist` | 4 | 4 | 0 | 8 |
| `inverse_agonist` | 1 | 1 | 0 | 2 |
| `decoy_lig` | 5 | 5 | 5 | 15 |
| **total** | **16** | **16** | **5** | **37** |

**No ligand-free row is ever blocked.** That is what makes the C7 arm free — §7.

#### 5.4 The arms, and what each costs

Nine `item` values across three experiments. `predictions = n × |backbones|`,
verified reproducing on all 350 rows with zero exceptions (gate **G-10**).

| item | exp | arm | tier | cells | backbones | n (pooled/per-cell) | preds @n=10 | preds @n=50 | blocked @10 | blocked @50 |
|---|---|---|---|---:|---|---|---:|---:|---:|---:|
| P2b | E2.2 | `ligand_x_partner_pilot` | T1 | 96 | boltz2 only | 10 / 10 | 960 | 960 | — | — |
| **G6a/G6b** | E2.2 | `ligand_x_partner` | T1 | 96 | all four | 10 / 50 | **3,840** | **19,200** | — | — |
| **G6d** | E2.4 | `decoy_third_role` *(EXPLORATORY)* | T1 | 32 | all four | 3 / 16 × 3 draws | **264** | **1,408** | 120 | 640 |
| G6f *(option)* | E2.2 | `ligand_x_partner_full_subunit` | T1 | 48 | all four | 10 / 50 | 1,920 | 9,600 | — | — |
| G6fd *(option)* | E2.4 | `decoy_third_role_full_subunit` *(EXPLORATORY)* | T1 | 16 | all four | 3 / 16 × 3 draws | 132 | 704 | 60 | 320 |
| G21 *(proposed)* | E2.3 | `efficacy_ladder_inverse_agonist` | T1 | 6 | all four | 10 / 50 | 240 | 1,200 | — | — |
| G6-T2 | E2.2 | `ligand_x_partner_peptide_tier` | T2 | 12 | all four | 10 / 50 | 160 | 800 | 320 | 1,600 |
| G6-T3 | E2.2 | `ligand_x_partner_mixed_tier` | T3 | 42 | all four | 10 / 50 | 1,200 | 6,000 | 480 | 2,400 |
| G6x | E2.2 | `blocked_ligand_identity` | T1 | 2 | — | 0 / 0 | — | — | — | — |
| **TOTAL** | | | | **350** | | | **8,716** | **39,872** | **980** | **4,960** |

Every figure reproduces from the file. `G6x` is the only blocked class costing
zero in *both* the dispatchable and the blocked columns — PD2R2 is carried as a
row so that the absence is visible, not so it is counted.

The decoy `n` splits across `DECOY_DRAWS = 3`, and **the split truncates**:
10/50 over three draws realises **9/48**. The generator prints it rather than
hiding it, because a decoy arm quietly running 9 where the agonist arm runs 10 is
an unbalanced design that would not show in the totals.

### 6. The five `dispatch_status` values

| status | rows | receptors | clusters | tier(s) | blocked preds (10 / 50) | recoverable? |
|---|---:|---:|---:|---|---|---|
| `READY` | 313 | 25 | 24 | T1 279, T2 4, T3 30 | — | dispatchable now |
| `BLOCKED_DECOY_UNAVAILABLE` | 15 | 5 | 4 | T1 | 180 / 960 | **partly** — §6.1 |
| `BLOCKED_UNRESOLVED_UNCURATED` | 12 | 3 | 3 | T3 | 480 / 2,400 | **yes, cheaply** — curation only |
| `BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE` | 8 | 2 | 2 | T2 | 320 / 1,600 | **yes** — four sequences |
| `BLOCKED_LIGAND_IDENTITY` | 2 | 1 | 1 | T1 | 0 / 0 | **no** — needs a deposition |

`dispatch_status` and `ligand_identity_status` agree one-to-one: no row is READY
with an unresolved ligand and none is blocked with a resolved one (gate **G-8**).

#### 6.1 `BLOCKED_DECOY_UNAVAILABLE` — 15 rows, 5 receptors, 4 clusters

D-RULE ran against a pinned pool (`drule_pool_molecules.tsv`, **ChEMBL_37**,
120,973 molecules, scope `within_panel`, k=3, clogp window `absolute:1.0`,
diversity max Tanimoto 0.3). `drule_selected.tsv` holds 38 rows: **33 accepted
on 11 receptors / 11 clusters, 5 decoy-unavailable**, each with its own verbatim
reason. Two *categorically different* refusal classes, never flattened:

| receptor | cluster | class | verbatim reason | `n_eligible` | `n_accepted` |
|---|---|---|---|---:|---:|
| AA1R | 001_006_001 | `fewer_than_k_accepted` | only 1 candidate(s) pass the gate; §5.3 needs 3 … Decisive axis — **no single axis unblocks this receptor** | 111,240 | 1 |
| AA2AR | 001_006_001 | `fewer_than_k_accepted` | only 0 … Decisive axis — **mw**: dropping it alone would give 1 | 111,240 | 0 |
| HRH3 | 001_001_005 | `fewer_than_k_accepted` | only 0 … Decisive axis — **mw**: dropping it alone would give 11 | 114,172 | 0 |
| LPAR1 | 001_004_003 | `fewer_than_k_accepted` | only 0 … Decisive axis — **tanimoto**: dropping it alone would give 1 | 120,207 | 0 |
| B1B1U5 | 001_009_001_inv | `eligibility_unestablishable_no_chembl_target` | the receptor has no resolved ChEMBL target, so the pool holds **no exclusion rows** and an empty exclusion set would read as universal eligibility | **0** | 0 |

**Recoverability.** The four `fewer_than_k_accepted` receptors are recoverable
only by relaxing a pinned rule (HRH3 would yield 11 candidates if the molecular-weight
window alone were dropped; AA1R would not be unblocked by any single axis).
B1B1U5 is not recoverable at all through the pool — it needs a ChEMBL target
assignment first. Doing either changes the frozen selection and therefore requires
amending `DECISIONS.md` D-2026-09-12-h first; `redo/gates/drule.py` (26 checks,
26 proved by planting) asserts the ChEMBL-id set, the InChIKey set **and the
receptor:molecule assignment** under three digests, so a silent redraw fails.

**The decoy arm therefore runs EXPLORATORY.** `CAMPAIGN.md` §5.3 pre-registers
≥12 paralog clusters; 11 pass. Interaction MDE at k=11 is **0.367** against
**0.352** at k=12 — a **4.4 %** loss of sensitivity, all three figures recomputed
here. Aditya's decision (D-2026-09-12-h) was to run it and pay the loss.
**No confirmatory claim may rest on this arm**, and every decoy row carries
`EXPLORATORY_MISSED_PREREG_CLUSTER_BAR` so that reading it as one cannot happen
by accident.

**And the 11 survivors are a biased subset.** The five refused are the small and
polar references plus a dianionic lipid, so what survives is the lipophilic,
drug-like end of the panel. The ligand-class contrast is evaluated on narrower
chemical space than the agonist arm it is compared against, and **k does not
capture that**.

The 33 accepted decoys are genuinely dissimilar to their reference ligands:
max Morgan Tanimoto to any real ligand ranges **0.138 – 0.290**, median **0.185**,
all below the 0.30 bar; between 4 and 180 real ligands were screened per receptor.

#### 6.2 `BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE` — 8 rows, 2 receptors (T2)

C5AR1's BM213 and PMX53, SSR2's somatostatin and CYN 154806. All four are curated
*structurally* — the deposition is named in `ligand_set_redo.tsv` — but **the
polymer-chain sequence is nowhere in `redo/inputs/`**. **Recoverable**: it needs
four sequences and no new chemistry. Until then the entire T2 tier has only its
four ligand-free rows dispatchable.

#### 6.3 `BLOCKED_UNRESOLVED_UNCURATED` — 12 rows, 3 receptors (T3)

CCR2 (CCL2 / MK-0812), NK1R (substance P / L760735) and NTR1 (JMV431 /
meclinertant) are named by the GPCRdb census in `ligand_tiers.tsv` but were never
enacted — no SMILES, no sequence, no CCD. **Recoverable at curation cost only**
(`free`/`cheap`); it is the cheapest way to grow the T3 tier from 4 READY
receptors to 7.

#### 6.4 `BLOCKED_LIGAND_IDENTITY` — 2 rows, PD2R2

PD2R2 is tier-eligible and was **never curated by anyone**. The GPCRdb snapshot's
record for `9IYB` reads `{name: PGD2, type: lipid, function: Agonist, PDB: A1D5Q}`
— but **CCD `A1D5Q` is C43 H81 O13 P, a phosphatidylinositol**, while PGD2 is
C20 H32 O5. Two different molecules in one record, with no SMILES to arbitrate.
Enacting it would have supplied a membrane lipid as the agonist. **Not
recoverable from any file we hold or could request**: PD2R2 appears in *neither*
of `paper_af3`'s two ligand sets (40 and 64 ligands), so they never curated one
either. Unblocking it means an agonist identity for `8XXV`, i.e. a deposition,
not a file. It is carried at zero predictions rather than omitted, because a
receptor that vanishes from a table looks exactly like one nobody considered.

### 7. The C7 arm — the agonist clause, at zero marginal cost

**C7 — "the agonist alone does not drive the active state" — has never been
tested.** Blocks A, B and D supply no agonist-alone arm, and Block C was believed
to but does not: all 40,800 rows of `rows.tier3.v2.csv` carry a ligand, so "apo"
there means *no partner*, not *no ligand* (`DECISIONS.md` **F-23**). The redo
already contains the experiment.

#### 7.1 The claim, verified

The brief's claim of **98 ligand-free READY rows, 20 receptors, 19 clusters**
is **CORRECT in all three numbers**, and so is the MDE of **0.279**.

| quantity | claimed | recomputed | verdict |
|---|---:|---:|---|
| ligand-free rows | — | **98** (all 98 READY, all `RESOLVED_NO_LIGAND`, all `n_nonpolymer_entities = 0`) | ✔ |
| receptors with the complete 2×2 | 20 | **20** | ✔ |
| clusters | 19 | **19** | ✔ |
| interaction MDE at k=19 | 0.279 | **0.279** (= 2.80 × 0.435 / √19) | ✔ |

The 20 receptors, and the one cluster that carries two of them:

> 5HT5A · **AA1R** · **AA2AR** · ACM4 · ADRB1 · AGTR1 · B1B1U5 · CCKAR · CNR2 ·
> DRD3 · EDNRB · GHSR · HRH3 · LPAR1 · LT4R1 · MCHR1 · NPY1R · OPRD · OPSD · S1PR1

AA1R and AA2AR share cluster `001_006_001`; that is the whole of the 20 → 19 gap.

The definition is robust to how "partner present" is read: taking the four cells
as `{apo, cognate} × {none, full_agonist}` (the gate's definition, where `cognate`
pools `R3_ct21` and `R7_full`) and taking them as `{R0_apo, R3_ct21} × {none,
full_agonist}` both give exactly 20 receptors / 19 clusters.

#### 7.2 The complete 2×2

Rows, restricted to the 20 pre-registered receptors and READY only:

| | ligand `none` | ligand `full_agonist` |
|---|---:|---:|
| **partner `apo`** (`R0_apo`) | **36** | **36** |
| **partner `cognate`** (`R3_ct21` + `R7_full`) | **36** | **36** |

Perfectly balanced, 144 rows. Broken out by partner construct and by arm:

| cell | G6a/G6b | P2b (pilot) | G6-T3 | G6f *(option)* | total |
|---|---:|---:|---:|---:|---:|
| `none` × `R0_apo` | 16 | 16 | 4 | — | 36 |
| `none` × `R3_ct21` | 16 | 16 | 4 | — | 36 |
| `none` × `R7_full` | — | — | — | 16 | 16 |
| `full_agonist` × `R0_apo` | 16 | 16 | 4 | — | 36 |
| `full_agonist` × `R3_ct21` | 16 | 16 | 4 | — | 36 |
| `full_agonist` × `R7_full` | — | — | — | 16 | 16 |

Across the 20 receptors these 176 rows carry **5,120 predictions at n=10 /
23,040 at n=50**; excluding the single-backbone P2b pilot, **4,480 / 22,400**.

Across the whole file, the pre-registration's own two figures also reproduce:
**41 READY `apo`/`none` rows** and **57 READY `cognate`/`none` rows** (41 at
`R3_ct21` + 16 at `R7_full`), summing to the 98.

#### 7.3 Why it is free

The 98 ligand-free rows collapse to **66 distinct `(receptor, partner construct)`
cells**, and **all 66 already exist in `g1_systems.csv`** — checked directly, zero
cells absent. They are enumerated in `g2_systems.csv` so the design reads as a cube
and the gate can check it is complete, **not so they are dispatched twice**.
Run once, read twice. C7's marginal cost is therefore zero: Group 2 dispatches
every one of these rows regardless of whether C7 is analysed.

#### 7.4 The five receptors that *cannot* join the C7 arm

25 of the 26 receptors carry ligand-free rows (PD2R2 has none — its only two rows
are its refused agonist). Of those 25, exactly five lack the complete 2×2, and in
every case the reason is the **agonist**, never the ligand-free cell:

| receptor | tier | agonist dispatch status |
|---|---|---|
| C5AR1 | T2 | `BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE` |
| SSR2 | T2 | `BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE` |
| CCR2 | T3 | `BLOCKED_UNRESOLVED_UNCURATED` |
| NK1R | T3 | `BLOCKED_UNRESOLVED_UNCURATED` |
| NTR1 | T3 | `BLOCKED_UNRESOLVED_UNCURATED` |

Curating those five agonists would take the C7 arm from 20/19 to **25/24**
(interaction MDE 0.279 → 0.249) at no GPU cost beyond the rows already enumerated.

#### 7.5 The power figure, and the correction that matters

`RUN_MATRIX.md` §4.2–4.3 gives the cluster-grain SDs and the MDE formula
**2.80 × SD / √k** (80 % power, two-sided α = 0.05). The interaction constant
1.218 is **2.80 × 0.435**, where 0.435 is the median interaction cluster SD.
Main effects have their own, smaller SDs.

| quantity | cluster SD | MDE at k = 19 | MDE at k = 20 |
|---|---:|---:|---:|
| main effect, `cognate − apo` — **the C7 contrast** | 0.189 | **0.121** | 0.118 |
| main effect, `cognate − decoy` | 0.242 | **0.155** | 0.152 |
| interaction, partner × ligand | 0.435 | **0.279** | 0.272 |

`C7_PREREGISTRATION.md` quoted 0.279 first and corrected it on 2026-09-13:
0.279 is the **interaction** figure and C7's primary contrast is a **main effect**.
Quoting it was conservative — it understated our power — but it carried a constant
across contrast types without re-deriving it.

**And a limit that matters more than either number.** Both figures are in
**binary-predicate units** (`redo/build/matrix_power.py` computes its SDs on
`d(Y5.58-OH, Y7.53-OH) < 9.08 Å AND d(2×46 CA, 6×37 CA) > 14.932 Å`), so they are
percentage points of active-call rate. The pre-registration declares a
**continuous** axis primary, and no MDE exists for it. The honest statement is
that **the primary axis for C7 is not yet powered**, and the figures above bound a
secondary readout. The free thing that fixes it is `E7.4`, the interaction power
injection, marked `FREE_UNSCHEDULED` in `run_registry.tsv`; both `CAMPAIGN.md`
§2.8 and `RUN_MATRIX` §4.3 say it must precede the ligand arm.

#### 7.6 What is pre-registered, and what enforces it

`redo/spec/C7_PREREGISTRATION.md` is **ENACTED AND BINDING** (D-2026-09-13-a §3).
It fixes, before any data exists: the contrast (`apo/agonist` − `apo/none`), the
unit (paralog cluster, seeds collapsed inside the receptor first), the interval
(cluster bootstrap, paired within cluster, **never pooled across backbones**), the
readout rule (report every axis the recording spec carries, per backbone, on its
own scale) and **what counts as C7 failing**.

Two clauses are worth repeating verbatim because they are the easiest to lose:

> **The agonist's effect is NEVER to be expressed as a share or percentage of the
> partner effect.** Measured on Block C, that share spans an order of magnitude
> across readouts on the same predictions and the same panel — 27–67 % on pocket-Cα,
> 5–17 % on TM6 tilt, 3–16 % on NPxxY-OH, 5–9 % on the binary predicate. It is a
> property of the readout, not of the ligand.

> **`pocket_ca_rmsd_active` is declared BIASED for this contrast, in advance.**
> It scores the pocket against a deposited *active* reference, which for these
> receptors is *agonist-bound* — so it is the axis most responsive to an agonist by
> construction. It is reported, and it is not the primary axis.

Gate check **G-15** in `redo/gates/g2_preflight.py` fails the run if the arm
shrinks below 20 receptors / 19 clusters / 98 ligand-free READY rows. It passes
today. The gate is proved by a planted defect (`--selftest` case G-15).
The whole gate currently reports **15 blocking checks passed, 0 failed, 7 pending**,
with **16 plants over 15 blocking checks proved**.

**This expires at dispatch.** After Group 2 runs, the same analysis is an
unregistered post-hoc contrast.

### 8. Why T1, T2 and T3 are never pooled

The tiering rule (`ligand_tiers.tsv`, D-2026-09-12-f) is about **chain-ness, not
the database's type string**. A ligand carrying a CCD code is a HETATM component
and is not a chain, whatever its `type` says — exactly one record in 872 is typed
`peptide` and carries a CCD (EDNRB's IRL 2500, a peptidomimetic), and that single
record was the only thing making EDNRB look like a matched-peptide receptor.

| tier | rule | receptors | clusters | interaction MDE |
|---|---|---:|---:|---:|
| **T1** | both arms chain-free | 17 eligible, **16 curated** | **15** | **0.314** |
| T2 | both arms a chain | 2 | 2 | — |
| T3 | one arm a chain, one not | 7 | 7 | — |
| X | one side has no ligand at all | 4 | 4 | *(not enumerated in G2)* |

T1+T2 = 17 clusters (0.295); all three tiers = 24 (0.249). All four figures
recompute exactly.

**The reason, stated as chain counts rather than as an assertion.** `n_chains`
is recorded per row, and the pattern is the whole argument:

| tier | role | `R0_apo` | `R3_ct21` | `R7_full` | `n_nonpolymer_entities` |
|---|---|---|---|---|---|
| T1 | `none` | 1 chain | 2 | 2 | 0 |
| T1 | agonist / antagonist / inverse / decoy | **1 chain** | **2** | **2** | 1 |
| T2 | `none` | 1 chain | 2 | — | 0 |
| T2 | agonist **and** antagonist | **2 chains** | **3** | — | 0 |
| T3 | `none` | 1 chain | 2 | — | 0 |
| T3 | agonist *(a chain)* | **2 chains** | **3** | — | 0 |
| T3 | antagonist / inverse *(not a chain)* | **1 chain** | **2** | — | 1 |

- **In T1 the ligand axis is clean.** Every ligand enters as a non-polymer entity,
  so chain count is constant at 1 (apo) or 2 (cognate) across all five ligand
  levels. Varying the ligand varies the ligand and nothing else.
- **In T3 the ligand axis is confounded with chain count *within a single
  receptor*.** At `R0_apo`, EDNRB's endothelin-1 row is a 2-chain prediction and
  its bosentan row is a 1-chain prediction. A difference between them is a
  difference between "agonist and antagonist" *and* between "two polymer chains
  and one". Pooling T3 into T1 would mix a within-receptor modality change into
  the headline agonist/antagonist contrast.
- **In T2 the agonist/antagonist contrast is balanced** — both sides are chains,
  2 and 2 — but the `none` → ligand step is not: adding the ligand adds a chain.
  So T2 can carry a within-tier agonist-vs-antagonist comparison but not a
  clean ligand-presence comparison, and its chain count at any given partner level
  is one higher than T1's, which changes what the model is being asked to fold.
- **And the statistical reason is independent of all that.** At 2 and 7 clusters,
  neither T2 nor T3 can carry the contrast: interaction MDE at k=2 and k=7 is 0.861
  and 0.460, against a headline of 0.314 at k=15. Saying so is the point of
  tiering them.

There is a further limit the tiers do **not** remove: **modality stays confounded
with receptor identity.** Every peptide-ligand row is a peptide-family receptor,
so nothing here separates *peptide ligand* from *peptide receptor*. T3 is the
within-receptor contrast that can, and it is why T3 exists as a tier rather than
being folded into T2.

**One consequence for C7 that is not recorded anywhere else.** Four of the 20
pre-registered C7 receptors — **AGTR1, EDNRB, MCHR1, NPY1R** — are T3, and their
`full_agonist` is a **polymer chain**. In those four, the C7 contrast
(`apo/agonist` − `apo/none`) is a 2-chain versus 1-chain comparison, while in the
other 16 it is a comparison at constant chain count. The arm restricted to
small-molecule agonists is **16 receptors / 15 clusters** (interaction MDE 0.314,
main-effect MDE 0.137–0.175). Reporting C7 on the 20 and on the 16 separately
costs nothing and is the only way to show the effect is not a chain-count artefact.

### 9. The two ligand-adjacent registries

| file | rows | what it is |
|---|---:|---|
| `ligand_tiers.tsv` | 64 receptors | the **census**: which receptor is eligible for which tier, derived from the GPCRdb snapshot. 30 PRIMARY / 29 clusters; 24 EXTENSION-census; 10 EXTENSION-chimeric-reference. Carries `agonist_is_chain` / `antagonist_is_chain`, the axis tiering is built on, plus `n_allosteric_skipped` and `n_antibody_skipped` (PAM/NAM and antibody ligands are skipped completely) |
| `ligand_set_redo.tsv` | 18 picks | the **enacted** redo choices, with bound PDB, resolution, state, GPCRdb role, SMILES, canonical SMILES and InChIKey |
| `ligand_ccd_verification.tsv` | 16 | RCSB cross-check of every CCD-sourced pick — 10 ok, 2 STEREO_DIFFERS, 4 n/a_chain |
| `drule_selected.tsv` | 38 | the frozen decoy selection, 33 accepted + 5 refused, with the full property profile of every candidate |

---

# Part 6. THE DECOY SETUP — D-RULE, its gate, and its refusal

Everything below was re-derived from `redo/inputs/` and `analysis/block_c/received_2026_09_12/rows.tier3.v2.csv` on 2026-09-14. Where a spec document states a number, it is re-derived here and any disagreement is flagged inline. Nothing in this section has run on a GPU: the decoy arm is 33 READY cells that have never been dispatched.

---

### 1. Why a decoy arm exists at all

The paper's ligand axis compares a **full agonist** against a **neutral antagonist**. That contrast is pharmacologically meaningful but it is not a test of *occupancy*: both molecules bind, both are shaped to bind, and both carry the chemotype the model has seen in every deposited structure of that receptor. If the predicted receptor moves toward the active state when an agonist is docked, three explanations survive that contrast:

1. the model is responding to the **specific ligand's binding chemistry** (what we want to claim);
2. the model is responding to **something being in the pocket at all** — mass, volume, buried surface;
3. the model is responding to **the chemotype's association with active-state structures in its training set**, i.e. memorised co-occurrence.

A neutral antagonist controls for none of these. It is a binder, it fills the pocket, and its chemotype is equally well represented in the PDB (usually in *inactive*-state structures, which is why it is the wrong control — it has its own directional prior).

A **decoy** is the control that separates (1) from (2) and (3): a molecule that is matched to the real agonist on every measurable physicochemical property — so the pocket is filled by the same amount of the same kind of matter — while being **topologically unrelated** to it and **having no measured activity** at that receptor or any of its paralogs. If the receptor still opens, the response is not ligand recognition.

**"Inactive compound" is not enough, for three separate reasons, and each one has a named failure in this project's history:**

- **Property mismatch turns the decoy into a different experiment.** The frozen campaign's decoys were approved drugs picked by hand. All 8 Tier-1 picks miss their own stated ±20 % property window on **three to five of six axes** (`MAP_LIGANDS_AND_ANALYSIS.md` §2.2). A molecule that is 80 Da smaller, two log units less lipophilic and neutral where the reference is cationic does not control for occupancy — it varies occupancy *and* identity at once.
- **Charge is the axis that fails silently.** The frozen builder's own comment reads *"Formal-charge mismatch is reported not raised (Decision A — aminergic +1 anchors force neutral decoys)"*. Every aminergic receptor's real ligand is protonated at pH 7.4; every hand-picked decoy was neutral. The decoy arm therefore differed from the ligand arms **systematically in net charge** across the aminergic panel, one-directionally, with nothing downstream stratifying on it.
- **Asserted inactivity is not measured inactivity.** The frozen rule's justification for each pick was prose in a second hard-coded dict (`paralog_review`: *"IUPHAR & PubChem BindingDB: no reported affinity at any muscarinic subtype"*). **No code checked it.** D-RULE replaces the assertion with a query against a hash-pinned database, and records which axis refused every candidate it rejected.

The published challenge this arm answers by name is **`yu2026domainmotion`** (82 enzymes, 500 AF3 models per condition, templates off): nonbinder ligands reproduce the domain motion, the training-composition prior is **40.3 pp** against a ligand effect of **9.1–17.5 pp**, and pLDDT does not discriminate binder from nonbinder. A referee who knows that paper will ask for exactly this arm.

> ### Two different things are called "the decoy arm" — do not merge them
> - **The LIGAND decoy** (this section, `g2_systems.csv` item `G6d`/`G6fd`, experiment `E2.4`): a *small molecule* in the pocket, chain count unchanged. This is what D-RULE builds.
> - **The PARTNER decoy** (Block B, `build_shuffled_decoy_constructs.py`): chain B is the full cognate Gα with its **last 11 residues permuted** in place (`cognate_seq[:-11] + scrambled_ct`), composition preserved, Hamming ≥ 5. No ligand is involved.
>
> Section 9 below is about the **partner** decoy. Sections 2–8 and 10 are about the **ligand** decoy.

---

### 2. D-RULE, the enacted rule in one block

Source: `redo/spec/CAMPAIGN.md` §5.3, implemented verbatim in `redo/build/drule_select.py`, plus **Amendment A** and **Amendment B** approved 2026-09-12 *after* the rule as pre-registered failed. The timing is recorded deliberately — it is what distinguishes a correction from a fit.

> For each receptor, the **reference ligand** is its curated **full agonist** (not the mean over all real ligands). Build a candidate pool from ChEMBL restricted to compounds with (i) no measured activity at the receptor, (ii) no measured activity at any receptor in its **paralog cluster**, and (iii) ≥1 measured activity at some unrelated target. Compute eight axes on every candidate and on the reference. Accept a candidate iff **MW and TPSA are each within ±20 %** of the reference's, **cLogP is within ±1.0 log unit**, every integer axis is within **±1**, **charge exactly equal**, and **Morgan (r = 2, 1024 bit) Tanimoto < 0.30** against every curated real ligand of the receptor **and of every receptor in its paralog cluster**. From the accepted set draw **k = 3** decoys by a seeded draw recorded in the row, subject to **pairwise Tanimoto < 0.30 among the three drawn**. A receptor with fewer than 3 accepted candidates is *decoy-unavailable*, named in the paper, and excluded. **No candidate is ever taken "anyway"; a draw is never topped up.**

**Enacted parameters, frozen by `D-2026-09-12-g` and asserted by `drule.py` D-17/D-18 on every row of `drule_selected.tsv`:**

| parameter | value | verified |
|---|---|---|
| ChEMBL release | `ChEMBL_37` | all 64 target rows, all 120,973 pool rows |
| download digest | `33c20374…c290d281` (sha256) | single value across the pool table |
| pool scope | `within_panel` | single value across the pool table |
| cLogP window | `absolute:1.0` | single value across all 38 selection rows |
| within-draw cap | `0.3` | single value across all 38 selection rows |
| k | `3` | single value across all 38 selection rows |
| draw seed | `20260912` | single value across all 33 accepted rows |
| rule string | `CAMPAIGN.md 5.3 D-RULE + amendments A,B 2026-09-12` | single value |

---

### 3. The eight axes and their exact tolerance windows

All eight are computed **from SMILES with RDKit 2022.09.5, by one function (`drule_select.axes()`), for reference and candidate alike**. ChEMBL's own `compound_properties` columns (`mw`, `logp`, `hbd`, `hba`, `rot`) are carried in the pool table but **are never consulted by the gate** — they exist only to be disagreed with under `--crosscheck`. This is deliberate: comparing a ChEMBL property against an RDKit property is a different-instrument comparison, and this project has produced three false discrepancies exactly that way.

Salts are handled first: `largest_fragment()` keeps the fragment with the most heavy atoms, ties broken by canonical SMILES.

| # | axis | RDKit call | window (`window()` in `drule_select.py:484`) | form |
|---|---|---|---|---|
| 1 | `mw` | `Descriptors.MolWt` | `[ref − 0.20·\|ref\|, ref + 0.20·\|ref\|]` | ±20 %, proportional |
| 2 | `clogp` | `Crippen.MolLogP` | `[ref − 1.0, ref + 1.0]` | **±1.0 log unit, ABSOLUTE (Amendment A)** |
| 3 | `tpsa` | `Descriptors.TPSA` | `[ref − 0.20·\|ref\|, ref + 0.20·\|ref\|]` | ±20 %, proportional |
| 4 | `hbd` | `Lipinski.NumHDonors` | `[ref − 1, ref + 1]` | ±1 integer |
| 5 | `hba` | `Lipinski.NumHAcceptors` | `[ref − 1, ref + 1]` | ±1 integer |
| 6 | `rot` | `Lipinski.NumRotatableBonds` | `[ref − 1, ref + 1]` | ±1 integer |
| 7 | `rings` | `rdMolDescriptors.CalcNumRings` | `[ref − 1, ref + 1]` | ±1 integer |
| 8 | `charge` | **`charge_ph74()`, never `Chem.GetFormalCharge`** | `[ref, ref]` | **exactly equal** |

Constants, read from the module: `CONTINUOUS_TOL = 0.20`, `INTEGER_TOL = 1`, `CLOGP_WINDOW = ("absolute", 1.0)`, `CONTINUOUS = ("mw","clogp","tpsa")`, `INTEGER = ("hbd","hba","rot","rings")`.

**The rejection vocabulary has NINE entries, not eight.** `AXES = ("mw","clogp","tpsa","hbd","hba","rot","rings","charge","tanimoto")`. The eighth *property* axis is charge; `tanimoto` is the similarity screen, carried in the same tuple so that the rejection table can name it. The gate prints `vocabulary 9 axes`. Read "all eight axes" as the property block only.

**No cascade.** All nine tests are evaluated for every candidate, so an axis's rejection count is a fact about the chemistry, not about test order. `first_failed_axis` is the first entry of the fixed `AXES` tuple, which makes the per-axis attribution stable across runs and machines.

#### 3.1 Formal charge at pH 7.4 — the axis the module exists for

`Chem.GetFormalCharge` returns the charge **as written in the SMILES**, which is a depositor convention, not chemistry. RDKit 2022.09.5 ships no pKa model and nothing may be installed, so charge is assigned by an explicit, auditable SMARTS rule (`drule_select.py:240-330`):

- **Neutralise first.** Every charge a protonation equilibrium could have chosen is stripped (`[NH3+] → N`, `[O-] → OH`). Charges no equilibrium can remove — quaternary ammonium, the N⁺/O⁻ of a nitro group — survive and are carried through as `residual`.
- **BASIC, +1 each** (3 SMARTS): guanidine (pKa ~12–13), amidine (~11–12), aliphatic amine (~9–11; **excluded**: N bonded to a heteroatom, to an aromatic ring atom (aniline ~4.6), amide/thioamide/imide N, sulfonamide/sulfinamide N, enamine N, nitrile N, imine N, α-halo-alkyl amine). Plus quaternary N⁺ (permanent).
- **ACIDIC, −1 each** (7 SMARTS, the *site* is claimed rather than the whole match): carboxylic acid, tetrazole, acyl sulfonamide, sulfonimide, sulfonic acid, sulfinic acid, **phosphonic/phosphoric OH — both OH counted**, so a phosphate monoester is **−2**. That is why LPAR1's LPA reference is −2, and it is the axis that decides LPAR1.
- **Explicitly NEUTRAL at 7.4**, stated so the omission is deliberate: aromatic ring N (pyridine ~5.2, imidazole ~6.0–7.0 *including histamine's*), aniline, amide/sulfonamide N–H, phenol, alcohol, thiol, hydroxamic acid, imide.
- **Damping**: a second basic centre within **3 bonds** of an accepted one takes no second proton (piperazine pKa2 ~5.6), so piperazine is +1 not +2. Centres are accepted in ascending atom index, which makes it deterministic.

**Validation is a gate, not a claim.** `validate_charge_rule()` runs on **every invocation, before anything is selected**, over **35** molecules whose charge at 7.4 is not in dispute — including the frozen campaign's own hand-picked decoys. Six are marked load-bearing: the panel's aminergic full agonists **5HT5A (5-CT), ACM4 (iperoxo), DRD3 (PD 128907), OPRD (DPI-287), ADRB1 (CHEMBL1615159), HRH3 (histamine)** must all come out **+1**. A failure **stops the module**; there is no fallback to `GetFormalCharge`. Measured: 35/35 at the expected charge, 6/6 aminergic at +1.

#### 3.2 Amendment A — why cLogP's window is absolute

§5.3 as pre-registered put *every* continuous axis within ±20 % of the reference. cLogP is already a logarithm, so `0.20·|cLogP_ref|` makes the window width proportional to a quantity whose zero point is arbitrary — a units artefact, not a chemical tolerance. Measured on the 16-receptor decoy panel (half-width = `0.2·|ref_clogp|`):

| receptor | ref cLogP | ±20 % half-width | receptor | ref cLogP | ±20 % half-width |
|---|---:|---:|---|---:|---:|
| **HRH3** (histamine) | −0.089 | **0.018** | CCKAR (SR146131) | 7.902 | **1.580** |
| **ACM4** (iperoxo) | 0.446 | **0.089** | S1PR1 (siponimod) | 6.773 | **1.355** |
| 5HT5A | 0.768 | 0.154 | OPSD (all-*trans*-retinal) | 5.717 | 1.143 |
| GHSR (ibutamoren) | 1.765 | 0.353 | OPRD | 5.558 | 1.112 |
| DRD3 | 1.937 | 0.387 | CNR2 | 5.657 | 1.131 |
| AA2AR (NECA) | −1.836 | 0.367 | LPAR1 (LPA) | 5.037 | 1.007 |
| AA1R (adenosine) | −1.980 | 0.396 | LT4R1 | 4.158 | 0.832 |
| ADRB1 | 2.676 | 0.535 | B1B1U5 | 6.251 | 1.250 |

The percentage form is simultaneously too tight (HRH3 ±0.02, ACM4 ±0.09) and too loose (CCKAR ±1.58, wider than the absolute window that replaces it).

**The absolute form is not a loosening, and this is the arithmetic that proves it** (all four re-derived):

| quantity | ±20 % of \|ref\| | **±1.0 log (enacted)** | ±1.5 log |
|---|---:|---:|---:|
| eligible (receptor, candidate) pairs refused by cLogP | 1,453,291 | **1,410,953** | 1,247,463 |
| as % of the 1,721,751 eligible pairs | **84.4 %** | **81.9 %** | 72.5 % |

At ±1.0 cLogP still refuses 81.9 % of eligible candidates and is the **sole** refuser of **1,836 of the 3,679** candidates that pass all seven other axes — it halves the otherwise-qualifying set. The conservation identity closes exactly: **1,843 accepted + 1,836 cLogP-only refusals = 3,679**. The window **redistributed** refusals; it did not remove them.

#### 3.3 The (window × cap) grid — reported as a shape, not a point

Because the change was made after seeing a failure, a single post-hoc number is not evidence. Clusters reaching k = 3, out of 15 (14 is the real ceiling — B1B1U5 can never pass). **Independently re-derived here and it reproduces `D-2026-09-12-g` cell for cell:**

| cLogP window | cap 0.30 | cap 0.40 | cap 0.50 | no cap |
|---|---|---|---|---|
| ±20 % of \|ref\| *(as pre-registered)* | **9r/9c** | 9r/9c | 9r/9c | 9r/9c |
| ±0.5 log | 7r/7c | 7r/7c | 7r/7c | 9r/9c |
| **±1.0 log** *(enacted)* | **11r/11c** ★ | 11r/11c | 11r/11c | 11r/11c |
| ±1.5 log | 11r/11c | 11r/11c | 11r/11c | 11r/11c |

**±0.5 is worse than ±20 %, and that is the artefact's signature**, not a bug: for two-thirds of the panel the relative window was already wider than half a log unit. **±1.5 adds zero clusters** while refusing 11.6 % fewer candidates than ±1.0 — a width that buys nothing costs credibility for free.

*Note on the ±0.5 / no-cap cell: ten receptors reach ≥3 accepted candidates there, but OPSD's three include a pair with identical Morgan fingerprints (T = 1.0), and `diverse_draw`'s test is strict `<`, so even an "uncapped" draw of 1.0 rejects it. Nine, not ten.*

---

### 4. The Tanimoto constraints — two of them, doing different jobs

Fingerprint, stated in code: **Morgan, radius 2, 1024 bits**, via `rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)` — one generator instance, so reference, candidate and within-draw comparisons all use the same object.

| constraint | threshold | against what | enforced |
|---|---|---|---|
| **similarity to the real ligands** (§5.3) | `TANIMOTO_MAX = 0.30`, **strictly `<`** | every curated real ligand of the receptor **and of every receptor in its paralog cluster** | `failed_axes()`; axis name `tanimoto`; gate D-12 recomputes it |
| **within-draw diversity** (Amendment B) | `DIVERSITY_MAX = 0.30`, **strictly `<`** | pairwise among the k = 3 drawn decoys of one receptor | `diverse_draw()`; gate D-16 recomputes it from SMILES |

**Why the second exists.** §5.3 caps similarity to the real ligands and says nothing about similarity *among* the three decoys. Its own justification for k = 3 is that it *"converts is this one molecule odd into a within-receptor distribution"* — and the first run drew OPSD two near-identical GPR52 ligands at pairwise **T = 0.641**, same MW to one decimal, same cLogP. That is one molecule wearing three hats. The cap is set to the **same 0.30** already used against the real ligands, so the rule carries one dissimilarity number and one justification rather than two. **On this panel it costs nothing** — 11 clusters at 0.30, 0.40, 0.50 and uncapped — so its value is set by consistency, not by what it buys, and that is stated rather than implied.

**What "every curated real ligand" resolves to.** Nine of the sixteen receptors are inherited and their cluster-mates (5HT2A, ADA1A, DRD4, OPRM, S1PR5, HRH2, CNR1, OPRK, OPRX…) are curated nowhere in `inputs/`. Taking "curated" to mean only our own enacted rows would make the screen weakest exactly where we know least. So the screen is the **union of three sources**, and the count is written into every row as `n_real_ligands_screened`:

1. `redo/inputs/ligand_set_redo.tsv` — our own enacted picks (`status = enacted`); these **win** over an inherited row for the same (receptor, role).
2. `redo/protocol/received/approved_2026_09_12/ligand_set.csv` and `ligand_set_tier3.csv` — `paper_af3`'s inherited curation.
3. `redo/inputs/ligand_census_records.tsv` — every small-molecule or lipid ligand observed bound to any receptor in the cluster, `role != apo`. This source only ever makes the screen **stricter**; nothing is filtered on a role string beyond dropping `apo`.

Realised breadth per accepted receptor: ADRB1 **180**, OPSD 58, ACM4 44, 5HT5A 40, CNR2 37, OPRD 35, DRD3 22, S1PR1 20, CCKAR 5, GHSR 5, LT4R1 **4**. (Self-test check: DRD3 alone is 9 real ligands; widened to cluster `['DRD2','DRD3','DRD4']` it is 22.)

**Delivered margins.** Worst similarity to any real ligand across all 33 decoys is **T = 0.2903** (LT4R1 / `CHEMBL4649582`), comfortably below 0.30. Worst within-draw pair on the panel is **T = 0.2736** (CCKAR) against 0.641 before Amendment B; OPSD is 0.2542 and keeps its three.

---

### 5. The inactivity requirement, precisely

From `redo/spec/DRULE_CHEMBL_SCOPE.md` §"What 'no measured activity' must mean, precisely", enforced in `redo/build/drule_pool.py`. Each clause is a decision, and each is a place the extraction could go quietly wrong.

| decision | enacted | why |
|---|---|---|
| **release** | pinned by version **and** download sha256, both written into **every** output row | an unpinned pull is `paper_af3`'s ColabFold problem in another costume. `drule_pool.py` **refuses to run against the live web API**; it requires `--db` + `--release` + `--sha256`. |
| **activity types** | `Ki`, `Kd`, `IC50`, `EC50` **only** | `AC50`, `%inhibition` and `Potency` mix functional and binding readouts and share no scale |
| **assay confidence** | `confidence_score >= 8` (direct single-protein target) | below 8 the assay may target a complex or a homologue, so "no activity here" becomes unverifiable |
| **what counts as ACTIVITY** | **any qualifying record, whatever its value** — plus `standard_value IS NOT NULL` | a weak measured affinity is still evidence the molecule binds; thresholding on potency would admit known weak binders as decoys |
| **what counts as ABSENCE** | no qualifying record at the receptor **or at any cluster-mate** | see the limitation below |
| **candidate** | **≥1** qualifying activity somewhere | so the molecule is a real ligand of *something*, not an untested compound |
| **target mapping** | UniProt accession → ChEMBL **SINGLE PROTEIN** target only | slug or gene-symbol matching collides across species, and the panel carries three non-human receptors |
| **species** | **recorded, never filtered** | a human-only filter would silently drop the *Hasarius adansoni*, *Mus musculus* and *Bos taurus* entries |

The two SQL predicates, verbatim in structure:

```sql
-- ACTIVE AT (used for both the receptor alone and the whole cluster)
SELECT DISTINCT act.molregno FROM activities act JOIN assays a ON a.assay_id = act.assay_id
 WHERE a.tid IN (...) AND a.confidence_score >= 8
   AND act.standard_type IN ('Ki','Kd','IC50','EC50') AND act.standard_value IS NOT NULL
```

**The limitation that must be stated, not hidden.** *"No measured activity in ChEMBL" is absence of evidence, not evidence of absence.* A decoy chosen this way may simply never have been assayed against that receptor. This is inherent to the method, is not fixable by a better query, and belongs in Methods. It is also the strongest reason to keep the **paralog-cluster** exclusion rather than the receptor-only one: a molecule untested at the receptor but inactive across its whole cluster is a better-evidenced decoy than one merely untested.

**"Non-binder" may NOT be used in the paper.** The enacted pool scope is `within_panel`, so **every one of the 33 accepted decoys is a known active at some other panel GPCR** (33/33, verified), and **17 of the 33 are actives at another receptor inside the decoy arm itself** (verified). The Methods may say only *"no measured activity at this receptor or its paralog cluster."*

---

### 6. The pool

#### 6.1 Target resolution — `redo/inputs/drule_targets.tsv`

| quantity | value |
|---|---|
| rows (one per panel receptor) | **64** |
| resolved to a ChEMBL SINGLE PROTEIN target | **63** |
| unresolved | **1 — `B1B1U5`**, the jumping-spider opsin (*Hasarius adansoni*), no ChEMBL target exists |
| ambiguous (accession → >1 target) | **0** — all 63 are `n_targets_matched = 1` |
| clusters with ≥1 resolved target | **31 of 32** |
| release naming the mapping | `ChEMBL_37`, single value |
| organisms | 61 human, 1 *Hasarius adansoni*, 1 *Mus musculus*, 1 *Bos taurus* |

The unresolved receptor is **recorded with an empty target, never dropped** — a receptor that silently vanishes from a decoy pool looks exactly like one that had no decoys.

#### 6.2 The candidate pool — two normalised tables, not one flat one

| file | rows | bytes | generator |
|---|---:|---:|---|
| `redo/inputs/drule_pool_molecules.tsv` | **120,973** | 25,167,183 | `drule_pool.py` |
| `redo/inputs/drule_pool_exclusions.tsv` | **363,367** | 30,726,529 | `drule_pool.py` |
| `redo/inputs/drule_rejections.tsv.gz` | **1,719,908** | 7,157,345 (85.4 MiB raw) | `drule_select.py` |
| `redo/inputs/drule_selected.tsv` | **38** (33 accepted + 5 unavailable) | 16,393 | `drule_select.py` |
| `redo/inputs/drule_targets.tsv` | **64** | 7,428 | `drule_targets.py` |

All five sha256 values in `inputs/MANIFEST.tsv` verify against the files on disk.

**Why normalised.** The spec asks for one row per (receptor, candidate). Run as written that is **120,973 × 63 = 7,621,299 rows / ~2.0 GB**, because the absence rule excludes only **4.77 %** (363,367 of 7,621,299) — so 95 % of the table would be the same molecules repeated 63 times with a property block copied each time. Stored instead as the molecule set **once** plus only the **excluded** (receptor, molecule) pairs, each with the axis that excluded it. Eligibility is then *"in the molecule table and not in the exclusion table for this receptor"*, which is exactly what the flat form encoded, at ~40 MB instead of 2 GB. Nothing is lost: the exclusion table still records **which** axis refused each pair.

**Pool scope — the decision that shrank it tenfold.** Measured against ChEMBL_37 itself, the spec's literal *"≥1 qualifying activity ANYWHERE"* reading yields **1,203,741 molecules** per receptor (~36 M pool rows — that is a copy of ChEMBL, not a candidate table). Restricting "elsewhere" to **another receptor on our own panel** yields **120,973**, and every one of the 63 resolved receptors still has known ligands (**median 1,589, min 2, max 11,076** actives at the receptor itself — re-derived here and matching). It is also better science: the rule wants a molecule *matched on everything except binding*, and a compound that demonstrably binds a **different GPCR** is far closer to that than an arbitrary approved drug. `anywhere` is kept as an explicit reachable option, and whichever is used is stamped on every row.

**What the exclusions are:**

| `ineligible_because` | rows |
|---|---:|
| `measured activity at the receptor` | **170,737** |
| `measured activity at a cluster-mate` | **192,630** |
| **total** | **363,367** |

Spread over **63 receptors** (B1B1U5 has none): min 2, median 5,879, max 12,409 exclusions per receptor.

**Pool provenance columns**, uniform across all 120,973 rows: `chembl_release = ChEMBL_37`, `chembl_sha256 = 33c20374…c290d281`, `pool_scope = within_panel`, `activity_types = Ki,Kd,IC50,EC50`, `min_confidence_score = 8`. Per-molecule: `n_targets_with_activity` (min 1, median 1, max 28) and `n_qualifying_activities` (min 1, median 1, max 318).

**130 pool rows carry an empty SMILES and 133 in total fail to produce the eight axes under RDKit.** These are silently absent from every eligible set. `n_eligible` is therefore *(120,973 − 133 unparseable) − (this receptor's exclusions)*, and on that definition all 16 recorded `n_eligible` values reconcile exactly.

---

### 7. The selection procedure

1. **Scope is re-derived, never assumed.** `load_scope()` reads the receptors of the decoy arm off `g2_systems.csv` (`ligand == 'decoy_lig'`) — **16 receptors in 15 paralog clusters**. If that file names no decoy cells the module raises rather than proceeding.
2. **Reference** = the receptor's curated **`full_agonist`** SMILES, our own enactment winning over the inherited row. If there is no parseable full agonist the receptor is `decoy-unavailable` with `blocking = no_reference`.
3. **Trap 1 first.** A receptor with **no resolved ChEMBL target has no exclusion rows**, so a naive implementation reads "nothing excluded" as "everything eligible" and hands the receptor we know *least* about the **largest** accepted set on the panel. Instead: `n_eligible = 0`, `decoy-unavailable`, reason *"eligibility is unestablishable"*.
4. **Eligible set** = parseable pool molecules minus this receptor's exclusions.
5. **Tanimoto maxima** computed by `BulkTanimotoSimilarity` of every real-ligand fingerprint against the whole eligible set.
6. **Nine tests, no short-circuit**, for every eligible candidate. Accepted → candidate list; refused → one row in `drule_rejections.tsv.gz` naming **every** failing axis plus the deterministic first.
7. **Gate.** `n_accepted < 3` → `decoy-unavailable`, with the **decisive axis** computed as `argmax` over *sole-axis* failures (the axis which, dropped alone, would admit the most) — **not** the most common failing axis, which is MW on every receptor here and is the blocker on none of them.
8. **The draw.** `diverse_draw(accepted, fp_of, receptor_seed(slug), k=3, cap=0.30)`:
   - accepted ids are **sorted**, so input order cannot depend on how the pool was read;
   - shuffled with `random.Random(receptor_seed(slug))` where `receptor_seed(slug) = int(sha256(f"drule|{slug}|20260912").hexdigest()[:16], 16)` — e.g. `OPSD → 9096820163344338901`, recomputed and asserted by gate D-10 on all 33 rows;
   - the permutation is **walked once, in order**; a candidate is skipped if its Morgan Tanimoto to an already-taken pick is `>= 0.30`; stop at 3.
   - **It is never re-seeded until it succeeds.** *"A draw that is re-seeded until it produces an answer is a search wearing a draw's clothes, and the count it produces is not the count the rule has."* A receptor whose accepted set holds no 3 mutually dissimilar members comes back **short** and is `decoy-unavailable`. **Never topped up with a near-copy.** At `cap = 1.0` nothing is skipped and this *is* §5.3's uniform sample of k.

**How ties are broken.** There is no value-ranking to tie: every accepted candidate is equally acceptable. Determinism comes from three places — (a) `sorted(accepted)` before the shuffle, (b) the receptor-specific seed, (c) `first_failed_axis` being the first entry of the fixed `AXES` tuple. `draw_rank` (1, 2, 3) is then assigned by `sorted(draw)`, i.e. **lexicographic ChEMBL id**, not draw order — so the rank column is stable independently of the shuffle.

---

### 8. The gate — `redo/gates/drule.py`, 26 checks, 26 proved by planting

Run read-only: **`CLEAN — 26 checks pass`**. Run with `--selftest`: **`26/26 checks proved by planting the defect each one exists to catch`** (executed 2026-09-14, exit 0).

| id | asserts | its plant |
|---|---|---|
| **D-1** | the ChEMBL target mapping is present and names exactly ONE release | delete `drule_targets.tsv` |
| **D-2** | every one of the 64 panel receptors has a row, resolved or not | drop CCKAR from the mapping |
| **D-3** | an unresolved receptor is recorded with an empty target, never dropped | blank the slug on the unresolved row so it vanishes quietly |
| **D-4** | no accession maps to more than one SINGLE PROTEIN target | make one accession map to two |
| **D-5** | every exclusion names a molecule in the pool **and** the axis that excluded it | strip the reason from an exclusion |
| **D-6** | every pool row records release, digest and scope | blank the release on a pool row |
| **D-7** | every receptor in scope carries exactly k decoys **or** a named refusal at zero (never both, never neither, refusal rows carry no molecule and no empty reason) | drop one OPRD decoy so it runs at k−1 |
| **D-8** | **THE TRAP** — a receptor with no resolved ChEMBL target acquires no decoy and is refused specifically because eligibility is *unestablishable* | hand a decoy to the receptor with no ChEMBL target |
| **D-9** | every accepted decoy is in the pool **and** carries no exclusion row for its own receptor | accept a decoy that carries an exclusion row for its receptor |
| **D-10** | every drawn decoy records the seed, and the seed **recomputes** from the receptor slug | blank the seed on a drawn decoy |
| **D-11** | every rejection names axes from the declared vocabulary, a deterministic `first_failed_axis`, `n_failed_axes` consistent, and no row is both accepted and rejected | name an axis the rule does not have (`mw → vibes`) |
| **D-12** | every accepted decoy still passes all eight axes **and** the Tanimoto screen on **recomputation from SMILES** against the *current* ligand tables, at the window **the row records** | swap an accepted decoy's SMILES for one that fails the window |
| **D-13** | the pH 7.4 protonation rule validates (35 molecules) and the six aminergic full agonists come out +1 | revert the charge axis to `Chem.GetFormalCharge` (a **code** plant, not a file plant) |
| **D-14** | `accepted + rejected == eligible` for every receptor with a resolved target — nothing vanishes between the pool and the two tables | set `n_eligible` to 999999 |
| **D-15** | every row records the enacted cLogP window and diversity cap, and the run used ONE of each | blank the enacted cLogP window on a row |
| **D-16** | the k decoys of a receptor are dissimilar **to each other**, recomputed from SMILES, and `max_intra_draw_tanimoto` is recorded consistently | make two of a receptor's three decoys the same molecule |
| **D-17** | the six rule parameters are the frozen ones **on every row** | change the cLogP window back to `relative:0.2` |
| **D-18** | the pool came from the frozen ChEMBL download **by digest**, not by release name | swap the pinned sha256 |
| **D-19** | exactly 11 receptors / 11 clusters accepted and 5 refused, and exactly **which** | drop a passing receptor (OPSD) out of the accepted set |
| **D-20** | the refusal **classes**, frozen per receptor — B1B1U5 separately from the other four | flatten B1B1U5's refusal into the other four's class (give it a nonzero `n_eligible`) |
| **D-21** | 33 accepted decoys, and **no molecule is reused across receptors** | reuse one receptor's decoy as another's |
| **D-22** | the SET of 33 ChEMBL ids hashes to the frozen digest | swap one drawn decoy for an undrawn one the rule also accepted — **no count in the gate changes** |
| **D-23** | the SET of 33 InChIKeys hashes to the frozen digest | move the chemistry under a stable accession (the ChEMBL-id hash still matches) |
| **D-24** | the MDE **recomputed** from the observed cluster count equals the frozen value | collapse two accepted receptors into one cluster, so k and the MDE move |
| **D-25** | the frozen selection reaches `g2_systems.csv` at 33 READY / 15 BLOCKED decoy cells | flip one READY decoy cell to BLOCKED |
| **D-26** | each decoy is frozen **to its receptor**, not merely to the panel | permute the assignment — the same 33 molecules against the wrong receptors, **both** set-hashes still matching |

#### 8.1 The three digests, and why two were not enough

All three re-derived here and all three match.

| digest | value | what it catches |
|---|---|---|
| ChEMBL-id set | `9d363f1f600796b5ef92b07c5457bb4e2a4f5acd0623c64fa89a6d318e84114b` | a **different molecule** was drawn |
| InChIKey set | `a694022dc0b56c96d199cf2eddb048ecadd963666778b0c7ab9bbfd3416c4fe1` | the **chemistry moved** under a stable accession (a ChEMBL id can be merged or withdrawn upstream; an InChIKey cannot) |
| **assignment pairs** | `e60eb91c8b6ea48c2f654d02dc1ac1031f6654a914cdb9114995aa4f55a04eff` | **the right molecules against the wrong receptors** |

Each is `sha256` over the `"|"`-joined **sorted** values, which makes the first two invariant to row order *and* to which receptor drew which molecule — the point being that they pin the arm's molecular identity and nothing else. **The third exists because the first plant written for the freeze proved nothing:** permuting one DRD3 decoy with one GHSR decoy leaves both set-hashes byte-identical, moves no count (33 rows, 33 distinct ids, 11 receptors, 11 clusters, 5 refused all still true), gives neither molecule an exclusion row (so D-9 stays quiet), and leaves `smiles` untouched (so D-12 still recomputes clean). **The same 33 molecules scored against the wrong reference ligands would have passed the entire freeze.** D-26, over the sorted `slug:chembl_id` pairs, is the only check that sees it. It surfaced only because the harness *runs* its plants instead of asserting that they work.

#### 8.2 Two properties of the harness worth copying

- **A missing input is a FAILURE, never a quiet skip.** `drule_select.require()` raises with *"A check that does nothing when its input is missing is the defect it exists to catch; this one stops instead."* D-7 does the same for `drule_selected.tsv` and the rejection table.
- **The staging asserts what it staged, and asserts the plant changed bytes.** `_stage()` symlinks every regular file in `redo/inputs/`, copies only the file a plant rewrites, then **raises unless the staged directory set equals the real one**. A plant whose target is byte-identical afterwards is scored `MISS`, not `ok`. This exists because on 2026-09-12 a hand-written `(".tsv", ".csv")` extension filter silently dropped the newly-gzipped rejection table from every planted copy: D-7 was scored "fired" for a reason unrelated to its plant and **D-8 through D-16 never ran at all**, while the harness printed a tidy tally. *The fix that works is an assertion that the staged copy reproduces the real directory — not a longer extension list.*

#### 8.3 The generator's own self-test

`python3 redo/build/drule_select.py --selftest` → **23/23**, run 2026-09-14. It proves both halves separately: the **rule** (charge exactness, the ±20 % boundary from both sides, the ±1 integer boundary from both sides, `T = 0.299` accepted / `0.30` refused / `0.31` refused, all four failing axes recorded with a deterministic first, both amendments including *"a set with no k dissimilar members returns SHORT — never topped up"*) **and the plumbing** a fixture would hand over for free (scope resolving to 16 receptors off `g2_systems.csv`, every receptor resolving to a curated full agonist, the Tanimoto screen actually widening to the cluster, the B1B1U5 trap being live, and the gz being byte-deterministic across two writes).

---

### 9. The refusal — F-19

Applying D-RULE to 120,973 candidate molecules from a hash-pinned release, **five of the sixteen Class A GPCRs in the decoy arm admit no set of three property-matched, charge-matched, topologically dissimilar decoys at all.**

| receptor | reference agonist | ref MW / cLogP / TPSA / charge | eligible | accepted | the axis that refuses |
|---|---|---|---:|---:|---|
| **B1B1U5** | 11,20-ethanoretinal | 310.5 / 6.25 / 17.1 / 0 | **0** | 0 | **no ChEMBL target — eligibility unestablishable** |
| **AA1R** | adenosine | 267.2 / **−1.98** / **139.5** / 0 (HBA 9) | 111,240 | **1** | **none singly** — 0 candidates fail on exactly one axis |
| **AA2AR** | NECA | 308.3 / **−1.84** / **148.4** / 0 (HBA 9) | 111,240 | 0 | **MW** — dropping it alone gives 1 |
| **HRH3** | histamine | **111.1** / −0.09 / 54.7 / +1 | 114,172 | 0 | **MW** — window **[88.9, 133.4]**; dropping it alone gives 11 |
| **LPAR1** | LPA (1-oleoyl-LPA) | 436.5 / 5.04 / 113.3 / **−2**, **0 rings, 20 rot** | 120,207 | 0 | **Tanimoto** — dropping it alone gives 1 |

Every "decisive axis" figure above is re-derived from the rejection table's sole-axis counts and matches the recorded reason string exactly.

**The refusals are chemistry, not curation effort.** They concentrate on receptors whose native agonist is chemically extreme — a 111 Da biogenic amine, a doubly-anionic lipid with no rings and 20 rotatable bonds, two polar nucleosides at cLogP ≈ −2 with TPSA ≈ 140–148 — and a pool of GPCR-active molecules contains almost nothing that small, that charged, or that polar.

**HRH3 is the cleanest evidence the cLogP repair did real work.** Before Amendment A no single axis unblocked it. After, its blocker is **MW**. The repair **exposed the next binding constraint rather than dissolving the gate** — which is what a units fix looks like; a loosening would have unblocked it.

#### 9.1 The outcome, frozen

| | |
|---|---|
| accepted | **11 receptors / 11 clusters** — `5HT5A ACM4 ADRB1 CCKAR CNR2 DRD3 GHSR LT4R1 OPRD OPSD S1PR1` |
| refused | **5** — `AA1R AA2AR HRH3 LPAR1` as `fewer_than_k_accepted`; **`B1B1U5` separately** as `eligibility_unestablishable_no_chembl_target` |
| molecules | **33, all distinct across receptors**; none reused |
| pre-registered bar | **≥12 of 15 clusters** |
| **k** | **11** |
| **MDE** | **1.218/√11 = 0.367** against **1.218/√12 = 0.352** at the bar — **+4.4 %** |
| status | **EXPLORATORY**, `D-2026-09-12-h` |

**Three things are now known that were not:**

1. **≥12 of 15 was probably never attainable.** B1B1U5 is unresolvable in ChEMBL by construction and is the sole member of its cluster, so the bar is really **≥12 of 14 — 86 % of the panel** must yield three matched, charge-matched, mutually dissimilar non-binders.
2. **"Decoy" cannot be worded as "non-binder"** (see §5).
3. **The arm was never on the critical path.** Title clause 2 is *"the agonist alone does not drive the active state"*, which is answered by **agonist vs. no-ligand at fixed partner condition**, not by agonist vs. decoy. The refusal costs the paper a referee's answer, not a claim.

**The decision was to run it at k = 11 as an explicit, recorded deviation.** The bar stays at 12; the arm is not claimed to have met it; it is labelled exploratory **in the data as well as in the prose** — every one of the 48 decoy rows in `g2_systems.csv` carries `ligand_flag = EXPLORATORY_MISSED_PREREG_CLUSTER_BAR`. Four alternatives were declined on the record: a third amendment to the chemistry (indistinguishable from fitting the rule to the outcome after two amendments already followed failures); widening the pool to `anywhere` (costs a ChEMBL re-download — the 28 GB database was deleted 2026-09-12 — **weakens** the control, and probably would not rescue HRH3 anyway, since the smaller and more generic a molecule is the more "no activity recorded" means *never assayed*); DUD-E / LIT-PCBA as a source (DUD-E decoys carry **no measured activity at all**, so adopting them would *lower* our evidential standard — keep DUD-E as the citation justifying the axis choice, not as a source); isomers of the true agonist (an isomer is not *rendered* a non-binder by being one — this campaign's own F-11 is about retinal isomers behaving differently — and has no activity data by construction); and de novo/generative decoys (declined most firmly: a synthetic SMILES never seen in the PDB or ChEMBL may place badly *because it is novel*, which **maps precisely onto our own result** — we would have manufactured our own positive).

#### 9.2 The caveat that MDE does not capture, and that is easy to miss

**The surviving 11 are a biased subset.** `k` counts clusters and says nothing about *which* clusters. The five refused receptors are the small-and-polar end of the panel — histamine (111 Da), adenosine and NECA — plus a dianionic lipid and the spider opsin. **The 11 that survive are systematically the lipophilic, drug-like end**, so the ligand-class contrast is evaluated on a narrower chemical space than the agonist arm it is compared against. The bias is a *consequence of the rule working*: D-RULE refuses exactly where matched chemistry is unreachable, so the arm's coverage is correlated with its own admission criterion. **One sentence stating this belongs wherever the arm is reported, and quoting MDE 0.367 does not discharge it.**

#### 9.3 The dispatch consequence

`redo/inputs/g2_systems.csv` carries **48 decoy cells** = 16 receptors × 3 partner levels (`R0_apo`, `R3_ct21` cognate 21-mer, `R7_full` whole subunit; `partner_msa = off` on both partnered levels).

| | cells | pooled predictions | per-cell predictions |
|---|---:|---:|---:|
| **READY** (`ligand_identity_status = RESOLVED_DRULE_DECOY`) | **33** | **396** | **2,112** |
| **BLOCKED_DECOY_UNAVAILABLE** | **15** | 0 (396 blocked) | 0 (2,112 blocked) |

Each READY cell is `n_pooled = 3` shared draws × 4 backbones = 12 pooled, and `n_percell = 16` × 4 = 64. The decoy molecules reach the table **keyed by InChIKey, never by copied SMILES** (`ligand_must_key_by = inchikey`), with `ligand_name` carrying the three ChEMBL ids pipe-joined. **Cell counts are frozen; prediction totals deliberately are not** — 132 of the 396 are `G6fd(option)` at `R7_full`, behind an open `pi_choice`, and `n = 10/50` is a separate open decision; `g2_preflight` G-10 re-derives the totals from backbones × n.

---

### 10. What the frozen campaign got wrong

#### 10.1 The ligand decoy — a hand-picked drug with an unenforced window

`scripts/build_block_c_decoys.py` holds a literal `DECOY_SMILES` dict of **34 entries** (8 Tier-1 + 26 Tier-3): ADRB2 → tramadol, ADRB1 → aspirin, DRD3 → mefenamic acid, AA2AR → trimethoprim, HRH1 → metformin, CCR5 → imatinib, MCHR1 → tamoxifen. Plus 3 `PEPTIDE_DECOYS`. There is **no candidate pool, no search, no property-matched draw and no random draw**.

- `PROPERTY_AXES = ("mw","logp","hbd","hba","rot","charge")` — **six**, not eight: no TPSA, no ring count.
- `PROPERTY_TOLERANCE = 0.20`, tested against the **mean over the receptor's real ligands** (a mean over mixed pharmacological roles, which is what produced their n = 1 and n = 2 windows).
- **No branch raises on a property miss.** The only consequence is a string appended to a CSV `notes` field. `TANIMOTO_MAX = 0.30` is the **only** gate that can reject.
- All 8 Tier-1 decoys pass the Tanimoto gate comfortably (max T = 0.157) and **all 8 miss the ±20 % window on three to five of six axes**; three Tier-3 `chosen_because` strings say in prose that the pick is outside the window and was taken anyway.
- **The gate is stale relative to the ligand set it guards.** ADRB2's frozen decoy notes still name `S-(-)-propranolol`, replaced by `(S)-alprenolol` on 2026-09-04, and nothing noticed. This is why `drule.py` **D-12 recomputes** rather than reading a stored cell.

**The operative rule was therefore "topologically dissimilar approved drug with a plausible no-binding story", not "property-matched non-binder."**

#### 10.2 The partner decoy — confounded at the MSA

*(This is the α5-CT scramble arm of Block B, not the ligand arm. `F-26` §1 records that this was described in this project as holding "mass, fold, composition, chain count **and MSA depth** constant" — the construct half is true, the MSA half is false, and `CATALOGUE.md` already listed it under "Failed to establish".)*

Scrambling the tail also disrupts inter-chain MSA pairing at the same columns. Homolog rows come from MMseqs2 against UniRef/BFD and **cannot align into a scrambled α5-CT**, so the profile the model sees at exactly the positions under test changes with the edit. Measured in `03_msa_audit/PHASE_1D_EXTENSION.md` (6 receptors × 2 arms × 3 backbones = 36 MSAs):

| | Boltz-2 | OpenFold-3 | Protenix v2 | Chai-1 |
|---|---|---|---|---|
| decoy edit **read** as uppercase aligned columns in the query row | 6/6 | 6/6 (by construction; raw MSA purged) | 6/6 | **0/40 — NOT read at column level** |
| decoy MSA **byte-identical** to the same receptor's cognate MSA | **0/6** | **0/6** (hash-key) | **0/6** | — |
| WT-match % at the 11 α5-CT columns, cognate → decoy | 11.0–14.0 → 6.3–13.5 | — | 22.6–24.9 → 6.2–23.0 | — |
| **gap fraction** at the α5-CT columns, cognate → decoy | 36.4–40.5 % → **36.9–52.6 %** | — | 34.5–41.7 % → **42.3–70.3 %** | — |

**Perturbing the alignment is unavoidable when you scramble a tail — it is not a build error.** The consequence is that the frozen decoy-vs-cognate contrast varies the construct *and* the alignment regime together, on 3 of 4 backbones; on Chai-1 the edit does not reach the model as aligned columns at all. **The redo's `partner_msa = off` design is the one that holds the alignment regime constant by construction**, which the frozen decoy arm cannot do. (The campaign's own critical-stop trigger — "decoy edit not read at column level by ≥3 backbones" — was **not** met: 3 READ, 1 not.)

Depth was held: all 40/40 decoys fall within ±5 % of their cognate parent's MSA depth (min −3.45 %, max +3.68 %, mean +0.41 %). Depth is not the confound; **pairing and column content are.**

---

### 11. What a null on this arm would mean

On the **already-paid-for** Block C rows (`rows.tier3.v2.csv`, 40,800 rows; decoy 14,400 = 7,200 apo + 7,200 cognate), the hand-picked decoy is **indistinguishable from the curated neutral antagonist on all four backbones.**

Binary two-instrument predicate (`d_npxxy_y558_y753_oh < threshold` **and** `d_gpcrdb_tm6_tilt_246_637_ca > threshold`, thresholds as carried in the file), Class A rows only, **cognate arm**, active fraction:

| backbone | full agonist | neutral antagonist | decoy | **antagonist − decoy** |
|---|---:|---:|---:|---:|
| boltz | 0.806 | 0.736 | 0.725 | **+0.011** |
| chai | 0.634 | 0.614 | 0.618 | **−0.004** |
| of3 | 0.738 | 0.663 | 0.679 | **−0.016** |
| protenix | 0.879 | 0.854 | 0.858 | **−0.004** |

*n = 1,750 agonist / 1,450 antagonist / 1,800 decoy per backbone per arm.* All twelve rates and all four contrasts reproduce exactly.

**Two caveats on those four numbers, both found by re-derivation:**

- **The denominators include rows whose predicate cannot be computed.** Per backbone-arm cell, 150 agonist / 200 antagonist / 200 decoy rows (receptors EDNRA, EDNRB, GRPR, and HRH3 on the antagonist and decoy arms) have no computable two-instrument call and are counted as **not active**. Restricted to rows where the predicate is computable (1,600/1,250/1,600), `antagonist − decoy` in the cognate arm is **+0.038, +0.017, +0.005, +0.026** — all four positive, no longer straddling zero. **The conclusion survives either way: |Δ| ≤ 0.04 on every backbone.**
- **They are the cognate-arm LEVEL, not the apo→cognate shift.** The shift difference is **+0.010, −0.020, −0.023, +0.001** — different numbers.

#### 11.1 The correction that reshapes what "null" means

On the **continuous** readout `pocket_ca_rmsd_inactive − pocket_ca_rmsd_active` (positive = nearer active) — the one `SC-C-6` says to prefer, because the binary predicate is floor-pinned in apo at rates of 0.01–0.35 — aggregated **to the paralog cluster** with seeds collapsed inside receptor, the three classes **do** separate, in a consistent order:

> **agonist > decoy > antagonist**, nearest-active first.

On the 14 clusters present in all three roles: **apo/boltz agonist −0.120, decoy −0.289, antagonist −0.401** (re-derived, matching F-19's citation). `antagonist − decoy` excludes zero on **7 of 8** (arm × backbone) cells under a 2,000-resample cluster bootstrap — re-derived independently and reproducing the recorded 7/8, with protenix/cognate the single cell that includes zero.

**The ordering is biologically coherent**, which is part of why it is believable: a neutral antagonist actively stabilises the inactive state; a decoy does nothing, so the receptor sits at its unliganded preference; the agonist pushes toward active. A decoy falling *between* the two is exactly what that predicts.

**Therefore: "decoy ≈ antagonist" may no longer be cited in support of F-19.** F-19 is unaffected and rests where its evidence actually is — **the chemistry**: the frozen decoys fail their own ±20 % window on 3–5 of 6 axes, are systematically uncharged where the reference ligands are cationic, and a properly-constructed decoy is provably unavailable for a third of the panel. None of that depended on the contrast.

#### 11.2 How to read the rebuilt arm

- **If the rebuilt arm still shows antagonist ≈ decoy on the readout the drop prefers, that is a finding about the models** — it is the direct GPCR analogue of `yu2026domainmotion`'s result, on a state call rather than a domain motion, and it must cite them by name.
- **As the frozen arm stands, it is a finding about the decoys**, not about the predictors: the negative control was not a controlled negative.
- **A null is a finding, not a failure**, and the arm's goal must be worded as *"measure the ligand's contribution at fixed partner condition"* — never as "show the drug flips the receptor".
- **No confirmatory claim may rest on this arm.** `k = 11 < 12`, MDE 0.367 against 0.352, `EXPLORATORY_MISSED_PREREG_CLUSTER_BAR` on every row.
- **All three numbers go in the paper, with dates**: the rule as pre-registered gave **9 of 15** clusters; the two amendments of 2026-09-12 gave **11**; the bar was **12** and was not met. Reporting only the 11 would hide a decision; reporting only the 9 would hide a real defect in our own rule.

**The three sentences F-19 earns, written once:**

1. *A decoy rule requiring measured activity at an unrelated target, matched molecular properties on eight axes, equal formal charge at pH 7.4 and topological dissimilarity from every ligand of the receptor and its paralog cluster admits no viable decoy set for 5 of 16 Class A GPCRs, including the histamine H₃ and LPA₁ receptors.*
2. *The limit is set by the native agonist's chemistry, not by curation effort: the failures are the receptors whose agonists are smallest, most charged or most polar.*
3. *A decoy arm built by hand-picking approved drugs does not meet this standard on any of its 8 receptors — all 8 miss their own stated ±20 % property window on three to five of six axes and are uncharged where the reference ligands are cationic — so its agonist-versus-decoy contrast is not a controlled comparison for pocket occupancy.*

**What F-19 does NOT claim.** It does not say decoys are impossible — widening the pool beyond panel GPCRs would change the answer. It says that under a stated, pre-registered rule on a pinned release, the `within_panel` pool cannot supply them for a third of this panel, and it **names the axis that refuses in each case**.

---

### Appendix A — the 33 accepted decoys

`candidate_name` is empty on all 33: these are unnamed ChEMBL compounds (the pool table carries `pref_name` where ChEMBL has one, e.g. `CHEMBL2 = PRAZOSIN`, but none of the drawn 33 has one).

| receptor | rank | ChEMBL id | MW | cLogP | TPSA | HBD | HBA | rot | rings | q | max T (real) | max T (draw) | also a known active at |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 5HT5A | 1 | `CHEMBL1490875` | 170.2 | 0.579 | 78.6 | 3 | 3 | 3 | 1 | +1 | 0.196 | 0.208 | ADA2A, **HRH3** |
| 5HT5A | 2 | `CHEMBL3289526` | 233.3 | 1.494 | 68.1 | 4 | 2 | 3 | 2 | +1 | 0.154 | 0.208 | ADA2A |
| 5HT5A | 3 | `CHEMBL3289540` | 179.2 | 1.391 | 71.1 | 3 | 2 | 3 | 1 | +1 | 0.185 | 0.208 | ADA2A |
| ACM4 | 1 | `CHEMBL166330` | 204.3 | 1.299 | 32.3 | 1 | 3 | 2 | 2 | +1 | 0.182 | 0.220 | **ADRB1** |
| ACM4 | 2 | `CHEMBL284257` | 193.2 | 1.349 | 30.5 | 1 | 3 | 2 | 2 | +1 | 0.164 | 0.220 | ADA1A |
| ACM4 | 3 | `CHEMBL502684` | 193.2 | 1.054 | 30.5 | 1 | 3 | 3 | 2 | +1 | 0.197 | 0.220 | **HRH3** |
| ADRB1 | 1 | `CHEMBL1098442` | 359.5 | 2.801 | 103.9 | 4 | 5 | 7 | 2 | +1 | 0.207 | 0.182 | HRH1, HRH2, **HRH3** |
| ADRB1 | 2 | `CHEMBL3401301` | 330.4 | 2.333 | 83.1 | 3 | 5 | 5 | 3 | +1 | 0.175 | 0.182 | **AA2AR** |
| ADRB1 | 3 | `CHEMBL4760919` | 421.9 | 2.737 | 107.9 | 3 | 6 | 5 | 3 | +1 | 0.229 | 0.182 | CXCR2 |
| CCKAR | 1 | `CHEMBL1669025` | 682.6 | 7.176 | 114.0 | 2 | 6 | 10 | 6 | −1 | 0.164 | **0.274** | PE2R4 |
| CCKAR | 2 | `CHEMBL306924` | 582.7 | 7.317 | 98.6 | 1 | 7 | 11 | 6 | −1 | 0.217 | **0.274** | AGTR1 |
| CCKAR | 3 | `CHEMBL96554` | 672.8 | 7.277 | 112.3 | 1 | 8 | 11 | 4 | −1 | 0.183 | **0.274** | AGTR1 |
| CNR2 | 1 | `CHEMBL2336073` | 420.5 | 4.998 | 70.9 | 2 | 4 | 10 | 3 | 0 | 0.213 | 0.260 | **S1PR1** |
| CNR2 | 2 | `CHEMBL270026` | 417.5 | 5.116 | 69.6 | 3 | 3 | 10 | 3 | 0 | 0.229 | 0.260 | **ADRB1**, ADRB2 |
| CNR2 | 3 | `CHEMBL3671056` | 388.9 | 5.393 | 61.4 | 3 | 3 | 9 | 2 | 0 | 0.177 | 0.260 | **S1PR1** |
| DRD3 | 1 | `CHEMBL156131` | 204.3 | 2.311 | 38.9 | 1 | 3 | 3 | 2 | +1 | 0.256 | 0.121 | HRH1 |
| DRD3 | 2 | `CHEMBL4739937` | 217.3 | 2.504 | 48.4 | 1 | 3 | 3 | 3 | +1 | 0.167 | 0.121 | 5HT2A, 5HT2C |
| DRD3 | 3 | `CHEMBL6189412` | 259.4 | 1.290 | 44.4 | 2 | 3 | 2 | 3 | +1 | 0.180 | 0.121 | 5HT2A, 5HT2C |
| GHSR | 1 | `CHEMBL302063` | 525.7 | 2.265 | 137.4 | 3 | 5 | 9 | 4 | +1 | 0.193 | 0.164 | C5AR1 |
| GHSR | 2 | `CHEMBL3901466` | 487.5 | 2.156 | 107.1 | 3 | 5 | 9 | 4 | +1 | 0.152 | 0.164 | **OPRD** |
| GHSR | 3 | `CHEMBL483469` | 543.0 | 2.650 | 124.2 | 2 | 7 | 7 | 5 | +1 | 0.161 | 0.164 | **AA1R, AA2AR** |
| LT4R1 | 1 | `CHEMBL117031` | 355.5 | 4.635 | 83.6 | 3 | 2 | 14 | 1 | −1 | 0.153 | 0.246 | **S1PR1** |
| LT4R1 | 2 | `CHEMBL119562` | 307.4 | 4.065 | 69.6 | 3 | 2 | 15 | 0 | −1 | 0.177 | 0.246 | **S1PR1** |
| LT4R1 | 3 | `CHEMBL4649582` | 351.5 | 3.757 | 79.5 | 2 | 4 | 14 | 1 | −1 | **0.290** | 0.246 | PE2R4 |
| OPRD | 1 | `CHEMBL3676860` | 410.6 | 5.723 | 45.5 | 1 | 3 | 7 | 4 | +1 | 0.253 | 0.239 | 5HT2A, DRD2, **DRD3** |
| OPRD | 2 | `CHEMBL4797752` | 443.3 | 4.745 | 41.6 | 1 | 3 | 7 | 3 | +1 | 0.202 | 0.239 | ADA1A, DRD2 |
| OPRD | 3 | `CHEMBL5646702` | 452.6 | 5.543 | 50.2 | 1 | 4 | 7 | 5 | +1 | 0.274 | 0.239 | CCR5 |
| OPSD | 1 | `CHEMBL125010` | 310.5 | 6.569 | 20.2 | 1 | 1 | 5 | 2 | 0 | 0.138 | 0.254 | CNR1, **CNR2** |
| OPSD | 2 | `CHEMBL261494` | 274.4 | 5.173 | 20.2 | 1 | 1 | 5 | 2 | 0 | 0.179 | 0.254 | **CNR2** |
| OPSD | 3 | `CHEMBL4761208` | 315.2 | 4.821 | 17.1 | 0 | 1 | 5 | 2 | 0 | 0.186 | 0.254 | GPR52 |
| S1PR1 | 1 | `CHEMBL462053` | 505.5 | 7.079 | 50.2 | 1 | 5 | 8 | 4 | 0 | 0.200 | 0.133 | CNR1, **CNR2** |
| S1PR1 | 2 | `CHEMBL5080279` | 453.7 | 7.121 | 73.5 | 2 | 4 | 9 | 4 | 0 | 0.152 | 0.133 | **CNR2** |
| S1PR1 | 3 | `CHEMBL5593523` | 488.6 | 5.801 | 62.8 | 2 | 4 | 8 | 5 | 0 | 0.238 | 0.133 | OX2R |

**Bold** in the last column = a receptor that is itself in the decoy arm. **17 of 33** decoys are actives at another receptor inside the arm; **33 of 33** are actives at some panel GPCR.

### Appendix B — per-receptor selection detail

| receptor | cluster | reference (source) | n eligible | n accepted | rejections | outcome |
|---|---|---|---:|---:|---:|---|
| 5HT5A | 001_001_001 | 5-CT (`ligand_set_tier3.csv`) | 111,093 | 8 | 111,085 | accepted |
| ACM4 | 001_001_002 | iperoxo (`ligand_set.csv`) | 115,584 | 8 | 115,576 | accepted |
| ADRB1 | 001_001_003 | `CHEMBL1615159` (`ligand_set_redo.tsv`) | 114,950 | 98 | 114,852 | accepted |
| DRD3 | 001_001_004 | PD 128907 (`ligand_set.csv`) | 108,622 | 324 | 108,298 | accepted |
| **HRH3** | 001_001_005 | histamine (`ligand_set_redo.tsv`) | 114,172 | **0** | 114,172 | **refused — MW** |
| CCKAR | 001_002_005 | SR146131 (`ligand_set_redo.tsv`) | 120,245 | 27 | 120,218 | accepted |
| GHSR | 001_002_010 | ibutamoren (`ligand_set_redo.tsv`) | 118,717 | 133 | 118,584 | accepted |
| OPRD | 001_002_022 | DPI-287-class (`ligand_set_tier3.csv`) | 108,479 | 1,065 | 107,414 | accepted |
| LT4R1 | 001_004_002 | (`ligand_set_tier3.csv`) | 120,432 | 28 | 120,404 | accepted |
| **LPAR1** | 001_004_003 | LPA (`ligand_set_tier3.csv`) | 120,207 | **0** | 120,207 | **refused — Tanimoto** |
| S1PR1 | 001_004_004 | siponimod (`ligand_set_redo.tsv`) | 116,741 | 116 | 116,625 | accepted |
| CNR2 | 001_004_005 | HU-308-type (`ligand_set_tier3.csv`) | 109,191 | 24 | 109,167 | accepted |
| **AA1R** | 001_006_001 | adenosine (`ligand_set.csv`) | 111,240 | **1** | 111,239 | **refused — no single axis** |
| **AA2AR** | 001_006_001 | NECA (`ligand_set.csv`) | 111,240 | **0** | 111,240 | **refused — MW** |
| **B1B1U5** | 001_009_001_inv | 11,20-ethanoretinal | **0** | **0** | 0 | **refused — unestablishable** |
| OPSD | 001_009_001_vert | all-*trans*-retinal (`ligand_set_redo.tsv`) | 120,838 | 11 | 120,827 | accepted |
| | | **totals** | **1,721,751** | **1,843** | **1,719,908** | **11 / 5** |

`accepted + rejected == eligible` holds globally and for every receptor with a resolved target (gate D-14).

### Appendix C — the rejection table, by axis

1,719,908 rows over 15 receptors (B1B1U5 has none), over 1,721,751 eligible (receptor, candidate) pairs.

| axis | appears in N rejections | % of eligible | is `first_failed_axis` in | **is the SOLE refuser of** |
|---|---:|---:|---:|---:|
| `mw` | 1,230,930 | 71.5 % | 1,230,930 | 393 |
| `clogp` | 1,410,953 | 81.9 % | 355,048 | **1,836** |
| `tpsa` | 1,371,957 | 79.7 % | 97,566 | 2,231 |
| `hbd` | 869,652 | 50.5 % | 16,838 | 376 |
| `hba` | 1,146,027 | 66.6 % | 5,886 | 545 |
| `rot` | 1,392,200 | 80.9 % | 11,061 | **3,145** |
| `rings` | 986,433 | 57.3 % | 496 | 216 |
| `charge` | 1,154,799 | 67.1 % | 1,746 | 1,699 |
| `tanimoto` | 17,069 | **1.0 %** | 337 | 337 |

**Read the last column, not the second.** MW is the most common first-failing axis on every receptor and is the blocker on none of them. The sole-refuser column is the one that answers "which axis killed this receptor" — which is why `drule_select.py` computes the refusal reason as `argmax` over it.

`tanimoto` refusing only 1.0 % of eligible candidates is the quantitative statement of §1: **topological dissimilarity is nearly free; property matching is what is scarce.** The frozen campaign enforced only the free constraint.

---

# Part 7. The MSA and alignment setup

*Every number in this section was recomputed from the file named beside it. Where a spec
document states a different number, both appear and the disagreement is flagged.*

---

### 1. The setup in one paragraph

Every enumerated system in the redo gives the **receptor chain (chain A) its normal, full,
unmanipulated alignment** and gives the **partner chain (chain B) an explicit query-only
alignment — the partner's own sequence and nothing else, depth 1 — at every rung, on all four
backbones.** Nothing else is enumerated. There is no receptor-depth arm anywhere in
`redo/inputs/`: `receptor_msa` takes exactly one value, `"on (default)"`, on all 2,039 rows of
`g1_systems.csv` and all 350 rows of `g2_systems.csv`. The depth axis that the campaign talks
about (Group 8 / G5) exists only as a multiplication in a cost model; it has no systems file,
no per-row sequences and no hashes.

That single design choice — pinning the partner to depth 1 — is the whole reason the length
ladder is interpretable, and it is also the campaign's single largest unmeasured manipulation.
Both halves are argued below.

---

### 2. What is declared today, counted from the files

#### 2.1 Group 1 — the partner-length work

```
python3 - <<'EOF'
import csv, collections
r = list(csv.DictReader(open('redo/inputs/g1_systems.csv')))
print(len(r), collections.Counter(x['partner_msa'] for x in r),
              collections.Counter(x['receptor_msa'] for x in r))
EOF
```

| `partner_msa` | rows | what it means | `n_chains` |
|---|---:|---|---|
| `off` | **1,855** | the partner chain gets a **query-only** alignment (depth 1) | 1,825 two-chain, 30 three-chain |
| `n/a` | **94** | there is no partner chain | all 94 are `n_chains = 1` |
| `ON` | **90** | the partner chain gets its **real** alignment | all 90 two-chain |
| **total** | **2,039** | | |

`receptor_msa` = `"on (default)"` on **2,039 of 2,039** rows. `ligand` = `"none"` on
**2,039 of 2,039** rows. Distinct arms: **23**.

Of the 1,945 rows that have a partner chain (`n_chains != 1`), **1,855 (95.4 %) run the partner
MSA-free and 90 (4.6 %) run it on** — and all 90 belong to one arm.

#### 2.2 Group 1, arm by arm

```
python3 - <<'EOF'
import csv, collections
r = list(csv.DictReader(open('redo/inputs/g1_systems.csv')))
t = collections.Counter((x['item'], x['arm'], x['partner_msa'], x['n_chains']) for x in r)
for k in sorted(t): print(k, t[k])
EOF
```

| item | arm | `partner_msa` | `receptor_msa` | `n_chains` | rows |
|---|---|---|---|---:|---:|
| G1a/G1b | `ladder` | `n/a` | on (default) | 1 | 30 |
| G1a/G1b | `ladder` | `off` | on (default) | 2 | 180 |
| G1c/G1d | `intermediate_nested` | `off` | on (default) | 2 | 90 |
| G1c-opt | `intermediate_optional` | `off` | on (default) | 2 | 30 |
| G1e | `hd_deletion_companion` | `off` | on (default) | 2 | 30 |
| G1f | `deposited_minig_anchor` | `off` | on (default) | 2 | 90 |
| G2 | `wide_replication` | `n/a` | on (default) | 1 | 24 |
| G2 | `wide_replication` | `off` | on (default) | 2 | 48 |
| G3a/G3b | `a5null` | `off` | on (default) | 2 | 90 |
| G3a/G3b | `non_ga_bulk` | `off` | on (default) | 2 | 90 |
| G4a/G4b | `composition_controls` | `off` | on (default) | 2 | 300 |
| G9 | `family_swap` | `off` | on (default) | 2 | 30 |
| G10 | `ala_scan` | `off` | on (default) | 2 | 210 |
| G10b | `gi_to_gs_series` | `off` | on (default) | 2 | 150 |
| G11 | `heterotrimer` | `off` | on (default) | **3** | 30 |
| G12 | `gi_gt_single_residue` | `off` | on (default) | 2 | 30 |
| G16 | `uncoupling_full` | `off` | on (default) | 2 | 12 |
| G16 | `uncoupling_peptide` | `off` | on (default) | 2 | 24 |
| **G17** | **`partner_msa_on`** | **`ON`** | on (default) | 2 | **90** |
| G18a | `wetlab_length_series` | `off` | on (default) | 2 | 90 |
| G18b | `wetlab_matched_peptides` | `off` | on (default) | 2 | 18 |
| G19 | `reference_matched_tip` | `off` | on (default) | 2 | 23 |
| G20 | `chimeric_ref_extension` | `n/a` | on (default) | 1 | 10 |
| G20 | `chimeric_ref_extension` | `off` | on (default) | 2 | 20 |
| P1 | `ladder_pilot` | `n/a` | on (default) | 1 | 30 |
| P1 | `ladder_pilot` | `off` | on (default) | 2 | 180 |
| P1b | `intermediate_pilot` | `off` | on (default) | 2 | 90 |

Two facts worth reading off this table. **`n/a` appears only on `R0_apo` rows** — 94 rows across
four arms (`ladder` 30, `ladder_pilot` 30, `wide_replication` 24, `chimeric_ref_extension` 10).
And **`ON` appears only in G17**, the arm whose entire purpose is to measure what the query-only
choice cost.

The `off` rows span **64 distinct receptors in 32 paralog clusters** and **81 distinct chain-B
constructs**, from `R1_ct11` (90 rows) through `R3_ct21` (124 rows, the most-used rung) to
`R7_full` (94 rows).

#### 2.3 Group 2 — the ligand work

```
python3 - <<'EOF'
import csv, collections
r = list(csv.DictReader(open('redo/inputs/g2_systems.csv')))
print(len(r), collections.Counter(x['partner_msa'] for x in r),
              collections.Counter(x['receptor_msa'] for x in r))
print(collections.Counter((x['partner_level'], x['partner_msa']) for x in r))
EOF
```

| `partner_msa` | rows | `partner_level` |
|---|---:|---|
| `off` | **207** | all 207 are `cognate` |
| `n/a` | **143** | all 143 are `apo` |
| **total** | **350** | |

`receptor_msa` = `"on (default)"` on **350 of 350**. Distinct arms: **9**. The mapping
`partner_level → partner_msa` is perfectly determined: cognate ⇒ `off`, apo ⇒ `n/a`, with no
exceptions. 26 distinct receptors, 25 clusters. `dispatch_status`: 313 READY, 37 blocked.

| item | arm | `partner_msa` | `n_chains` | rows |
|---|---|---|---:|---:|
| G6a/G6b | `ligand_x_partner` | `n/a` / `off` | 1 / 2 | 48 / 48 |
| G6-T2 | `ligand_x_partner_peptide_tier` | `n/a` / `n/a` / `off` / `off` | 1 / **2** / 2 / **3** | 2 / 4 / 2 / 4 |
| G6-T3 | `ligand_x_partner_mixed_tier` | `n/a` / `n/a` / `off` / `off` | 1 / **2** / 2 / **3** | 14 / 7 / 14 / 7 |
| G6d | `decoy_third_role` | `n/a` / `off` | 1 / 2 | 16 / 16 |
| G6f(option) | `ligand_x_partner_full_subunit` | `off` | 2 | 48 |
| G6fd(option) | `decoy_third_role_full_subunit` | `off` | 2 | 16 |
| G6x | `blocked_ligand_identity` | `n/a` / `off` | 1 / 2 | 1 / 1 |
| G21 | `efficacy_ladder_inverse_agonist` | `n/a` / `off` | 1 / 2 | 3 / 3 |
| P2b | `ligand_x_partner_pilot` | `n/a` / `off` | 1 / 2 | 48 / 48 |

#### 2.4 The gates that hold this in place, and they are proved by planting

| check | file | what it asserts | proved? |
|---|---|---|---|
| **B7** | `g1_preflight.py:157-162` | `partner_msa ∈ {off, ON, n/a}` **and** `receptor_msa == "on (default)"` on every row | yes — `--selftest` plants a defect in `g1_systems.csv`, B7 fires |
| **B8** | `g1_preflight.py:164-168` | among rows with `n_chains != 1`, `count(off) > count(ON)` | yes — fires under plant |
| **B11** | `g1_preflight.py:207-214` | the recording spec carries `partner_msa_depth` and `partner_msa_mode` (among 12 required columns) | yes — fires under plant |
| **G-11** | `g2_preflight.py:319-325` | every `R0_apo` row is `n/a`, every non-apo row is `off` | yes — fires under plant |
| **R4** | `run_receipt.py:108-123` | on a delivered run, `partner_msa_depth_observed == partner_msa_depth_expected` on every row; **a missing column is a FAILURE, not a skip** | **no runnable self-test exists for `run_receipt.py`** |

`python3 redo/gates/g1_preflight.py --selftest` → "18 plants, all blocking checks proved";
`python3 redo/gates/g2_preflight.py --selftest` → "16 plants over 15 blocking checks proved".

**B7 also blocks the depth arm.** `receptor_msa != "on (default)"` is hard-coded into B7's
failure condition, so a row carrying `receptor_msa = "8"` fails the gate. A receptor-depth arm
cannot be added to `g1_systems.csv` without deliberately widening B7 and re-proving it by
planting. (B8 would *not* block it — B8 only compares `off` against `ON` counts on the partner
column.)

---

### 3. The naming defect: `off` does not mean off

**`partner_msa = "off"` is a misnomer and should read `query_only`.** The chain gets *itself* —
a one-row alignment containing the partner sequence — not *nothing*.

The two are not equivalent, and `MSA_SPEC.md` §4 spends a page on why:

- **An absent alignment depends on four unmeasured fallback behaviours.** The bad case is
  specific: a backbone that quietly generates its own alignment for a chain it finds no file for
  delivers **full depth exactly where we intended zero** — the inverse of the design — with
  nothing in any status JSON to show it.
- **A query-only alignment is constant by construction** (depth 1 at every rung, every Gα
  family), **is one operation rather than four fallbacks**, and **is verifiable after the fact**:
  depth 1 is a number you can read off the artefact, whereas an absence is only an absence.
- The one backbone where this is settled is Chai-1: chai-lab 0.6.1
  `data/dataset/msas/load.py:47-58`, `if not path.is_file()` returns
  `MSAContext.create_single_seq()` — no fetch, no generation. **On Chai, absent and query-only
  are behaviourally identical.** The explicit `.pqt` buys verifiability, not different behaviour.
  Two caveats survive: that fallback path **has never fired in a real campaign** (the launcher
  pre-checks every chain's `.pqt` and refuses to launch without one, so it is dormant code), and
  omission stops being safe the moment `--use-msa-server` is added.

So the column value and the specification are one word apart and mean opposite things on three
of four backbones. The fix is free — it is a string in `redo/build/g1_systems.py:514` and
`g2_systems.py:656`, not a hand-edit of an input — but it is **not yet made**: the value is still
`off` in both files today, and it has already propagated into the recording spec, where
`partner_msa_mode` is documented as *"off (primary) / on (E1.9 contrast)"*.

Either rename the level to `query_only`, or add an explicit `partner_msa_depth_target = 1`
column, **before someone implements `off` as `off`**.

---

### 4. Why query-only: the partner-depth cliff, recomputed

The ladder varies one thing — the length of the partner chain. That reading requires length to
be the *only* thing changing. Under an MSA-on design it is not, because partner alignment depth
is a steep function of rung.

```
python3 - <<'EOF'
import csv, collections
r = [x for x in csv.DictReader(open('redo/protocol/received/rung_msa_depth.csv'))
     if x['note'] == 'ok']
by = collections.defaultdict(list)
for x in r: by[x['rung']].append((x['family'], int(x['len']), int(x['unpaired_depth'])))
for k in ['R1_ct11','R2_ct15','R3_ct21','R4_a5helix','R5_a5plus','R6a_da5','R7_full']:
    d=[z for _,_,z in by[k]]
    print(k, len(by[k]), min(d), max(d), sum(1 for z in d if z==0))
EOF
```

`redo/protocol/received/rung_msa_depth.csv` — 112 rows = 7 rungs × 16 Gα families, measured
off-GPU by the pipeline team. Three rows carry `unpaired_depth = -1`, a ColabFold **timeout
sentinel, not a depth** (`R7_full`/Gi2, `R7_full`/Gz, `R6a_da5`/Gz); they must be filtered on
`note == "ok"`, leaving 109.

| rung | length(s) | families ok | depth = 0 | min (family) | max (family) | Gs |
|---|---|---:|---:|---|---|---:|
| `R1_ct11` | 11 | 16 | **16 of 16** | 0 | 0 | 0 |
| `R2_ct15` | 15 | 16 | **5** (Gq, G11, G12, G14, G15) | 0 | **459 (Gs)** | 459 |
| `R3_ct21` | 21 | 16 | 0 | 47 (G15) | **582 (Golf)** | 581 |
| `R4_a5helix` | 26 | 16 | 0 | 186 (G15) | 1,995 (Gq) | 604 |
| `R5_a5plus` | 36 | 16 | 0 | 2,273 (G15) | 3,043 (Gi3) | 2,651 |
| `R6a_da5` | 324–368 | 15 | 0 | **5,764 (G12)** | 9,176 (Gi1) | 7,396 |
| `R7_full` | 350–394 | 14 | 0 | **6,289 (G12)** | 9,203 (Gi1) | 7,248 |

The ten non-zero `R2_ct15` families are 2, 6, 18, 21, 21, 21, 25, 33, 33, 42 — every one ≤ 42,
against Gs at 459.

**Read that as a design problem.** Three of four backbones pair their MSAs; Chai does not. Under
an MSA-on design the partner's alignment regime is therefore a function of **both rung and Gα
family**:

- `ct11` runs single-sequence by force, on every family.
- `ct15` runs single-sequence for five families, near-single-sequence for ten more, and
  **aligned for Gs alone** — and Gs is the most common cognate partner on any GPCR panel,
  including ours.
- `ct21` and above run aligned, with depth climbing three orders of magnitude.

**A monotone trend along that ladder is exactly what a pairing artefact looks like.** "More α5
drives more activation" and "more α5 retrieves more homologs" are not separable, and at `ct15` a
Gs-specific effect could not be told from chemistry. Query-only removes the confound rather than
modelling it.

#### 4.1 Depth at peptide length tracks conservation, not length

The same point from the other direction, from the pipeline's own Chai `.aligned.pqt` cache
(`data/block_b/03_msa_audit/msa_depth_report.md`):

| entry | aa | total depth |
|---|---:|---:|
| DAMGO | 5 | **1** |
| substanceP | 11 | **1** |
| `random_helix_40mer` | 40 | **1** |
| `arrestin_Ctail` | 41 | **1** |
| `arrestin_FL` | 15 | 84 |
| `gcn4_leucine_zipper_33` | 33 | 224 |
| endothelin1 | 21 | **732** |
| cognate Gα (5 canonical) | 350–394 | **11,904 – 14,986** |

A 21-mer retrieves more than a 33-mer; a designed 40-mer returns query-only while a 15-mer
returns 84. **The predictor is naturalness — whether the sequence has homologs in the searched
databases — not length.** `arrestin_Ctail` is the governing case: 41 residues, an *excised
fragment* of a larger protein, depth 1. Our α5-CT rungs are excised fragments of Gα, the same
case. And the α5-CT is among the most conserved 21 residues in the proteome — byte-identical
across Gi1/Gi2, across Gt1/Gt2/Ggust, and across Gq/G11 — so a wild-type-vs-scramble contrast at
21 residues run MSA-on would be **a pure alignment-depth contrast**, not a sequence-recognition
contrast. That is worse than the Block B confound it replaces: in Block B both arms at least had
deep alignments.

#### 4.2 The two partner-depth series are not the same quantity

A provenance caveat that no spec document states. The rung measurement and the Chai cache
disagree by a factor of ~1.7 on the same molecule, because they count different things:

```
## rung_msa_depth.csv R7_full vs msa_depth_report.md "Cognate Ga partner depths (5 canonical)"
```

| family | R7_full len | `rung_msa_depth` unpaired | Chai-cache total | Chai-cache UniRef90 | ratio to UniRef90 |
|---|---:|---:|---:|---:|---:|
| Gs | 394 | 7,248 | 12,080 | 7,355 | 0.985 |
| Gi1 | 354 | 9,203 | 14,986 | 9,327 | 0.987 |
| Gq | 359 | 8,720 | 14,368 | 8,842 | 0.986 |
| G13 | 377 | 6,573 | 11,904 | 6,690 | 0.983 |
| Gt1 | 350 | 8,896 | 14,314 | 9,015 | 0.987 |

The `rung_msa_depth.csv` "unpaired depth" reproduces the Chai cache's **UniRef90 count** to
within 1.7 % and is ~60 % of its **total**. **Do not quote a number from one series against a
threshold derived from the other.** This is the same class of problem as §7 item 6 below: nobody
has written down what "depth" counts.

---

### 5. The undeclared chain: a peptide ligand supplied as a polymer

**22 rows of `g2_systems.csv` supply the ligand as a chain rather than as a small molecule**, and
nothing anywhere declares what alignment that chain receives.

```
python3 -c "
import csv,collections
r=list(csv.DictReader(open('redo/inputs/g2_systems.csv')))
lc=[x for x in r if x['ligand_is_chain']=='1']
print(len(lc), collections.Counter((x['partner_level'],x['n_chains'],x['partner_msa']) for x in lc))
print([c for c in r[0] if 'msa' in c.lower()])"
```

| arm | receptors | apo rows (`n_chains=2`) | cognate rows (`n_chains=3`) |
|---|---|---:|---:|
| G6-T2 `ligand_x_partner_peptide_tier` | C5AR1, SSR2 | 4 | 4 |
| G6-T3 `ligand_x_partner_mixed_tier` | AGTR1, CCR2, EDNRB, MCHR1, NK1R, NPY1R, NTR1 | 7 | 7 |

The eleven peptide ligands are BM213, PMX53, somatostatin, CYN 154806, angiotensin II (8-mer),
CCL2, **endothelin-1 (native 21-mer)**, MCH (19-mer), **substance P (11-mer)**, NPY (36-mer) and
JMV431.

Three consequences, and they are not hypothetical:

1. **`g2_systems.csv` carries exactly two MSA columns, `partner_msa` and `receptor_msa`.** There
   is no `ligand_msa`. The string `ligand_msa` appears **nowhere in `redo/`**
   (`grep -rn "ligand_msa" redo/` returns nothing).
2. **Gate G-11 checks only `partner_msa`.** A peptide-ligand chain fetching its own full-depth
   alignment would pass every enumerated check.
3. **The depths involved are exactly the ones §4 warns about.** Block B measured substance P
   (11 aa) at depth **1** and endothelin-1 (21 aa) at depth **732**. If any backbone default
   fires, the ligand chain's alignment regime varies by two-and-a-half orders of magnitude
   *across the ligand axis*, which is the §4 confound transposed onto Group 2. And
   endothelin-1 is **exactly 21 residues, the same as `R3_ct21`**, so EDNRB cannot be crossed
   with a peptide rung without explicit chain labelling.

The risk is recognised in prose — `DECISIONS.md` D-C (*"a peptide agonist is a third protein
chain and flips OpenFold-3's `use_paired_msas`"*) — but **it has not been converted into a
column or a check.** Per the project's own standing rule, a dependency written down is not a
check.

---

### 6. The three regimes, and why two of them cannot be deployed today

Three regimes were proposed: **(a)** subsample the receptor MSA; **(b)** subsample receptor +
G-protein partner; **(c)** receptor + partner in the presence of a ligand.

#### 6.1 Regime (b) is not a regime — it is already at the floor

Verified in §2: **1,855 of the 1,945 two-chain rows already run the partner at query-only**,
which is depth 1, and B8 asserts it. Regime (b) as literally stated asks us to reduce the depth
of an alignment the design has already pinned to its floor. It is a no-op.

Three further reasons not to fix that by turning the partner MSA back on:

1. **Partner depth is collinear with the factor being measured** (§4's table). At `R1_ct11` a
   depth target is *unreachable on every family*, and
   `subsample_msa.py:106-107` **returns the input unchanged when it is shorter than the target
   while the manifest still records the target label** — so a "partner depth 8" arm at ct11
   would be a depth-0 arm wearing a depth-8 label, on 16 of 16 families, silently.
2. **The binary version is better posed and already costed** — that is G17 / catalogue E1.9.
   Two levels, not five.
3. **It is the only arm that bounds the cost of our own primary design** (§8).

#### 6.2 The per-chain mapping problem — this is what blocks (a)-Stage-2 and (c)

**A regime we cannot set identically on four backbones is not a four-backbone claim.** The four
backbones key a per-chain MSA mapping four incompatible ways:

| backbone | how a per-chain MSA is keyed | source |
|---|---|---|
| **OpenFold-3** | **chain ID** — `msa_a3m_path.get(cid)`, `cid = chain["chain_ids"][0]` | `propose.py:462` |
| **Protenix** | **integer position** — `msa_a3m_path.get(protein_idx)`, a 0-based counter | `propose.py:595` |
| **Boltz-2** | a per-chain dict exists, commented *"D3 multi-chain support, currently unused"*; **no caller uses it** | `propose.py:358-360` |
| **Chai-1** | **not per-chain at all** — resolved by `sha256(sequence.upper())` inside `--msa-directory` | `rerun_chai.sh:167` |

The consequence is the part to internalise. A caller passing `{"A": receptor_a3m, "B": ""}`

- **works on OpenFold-3**;
- **fails silently on Protenix**: `.get("A")` against a dict keyed `{0:…, 1:…}` returns `None`,
  hits `if not path: continue`, sets **no MSA at all**, and Protenix falls through to its
  launcher default — **a live server fetch at full depth on both chains**, with nothing in any
  status JSON.

And the two failures run in **opposite directions**. Get it wrong one way on OF3 and a rejected
basename yields `warnings.warn` plus single-sequence featurisation — depth 1 where you asked for
128. Get it wrong on Protenix and you get full depth where you asked for 8. **Neither raises**,
and neither shows in a status file, because `'use_msa_server': True` and
`'msa_server_mode': 'protenix'` are **hardcoded Python literals** written on the same code path
that may have just disabled the server.

So today a four-backbone two-chain depth cell can produce, in one cell, a genuine depth-8
(Boltz, if the untested dict path works), a depth-1 (OF3, silent degradation), a full-depth live
fetch (Protenix, silent inflation) and whatever the cache happened to hold (Chai) — with
`ok: true` on all four.

**This is the failure mode `MSA_SPEC.md` §4 argues against, reached through the mechanism
`MSA_SPEC.md` §3 proposes.** The only thing that catches it is the observed-partner-depth
assertion (§7), which is the argument for that column being non-optional rather than nice to
have.

#### 6.3 Two more mechanism facts that bear on the regime

**The paired slot must be specified, not inherited.** `propose.py:471-472` (OF3) and `:599-600`
(Protenix) each assign **one path to both the unpaired and the paired slot**. For a depth-1 file
that is *probably* inert — there is nothing to pair — but "probably inert" is the same epistemic
footing §4 rejects for omission. OF3 additionally carries a query-level `use_paired_msas` flag,
and leaving it true against a depth-1 paired file is a third unmeasured behaviour. **State the
partner's paired-slot content explicitly** — an empty list, or the same query-only file,
declared either way.

**Chai's cache key is an operational trap for any depth arm.** Chai resolves an alignment by
sequence hash, and the receptor sequence is identical at depth 8 and at full — so the same key
must resolve to two different files. The only way is **one `--msa-directory` per depth arm** (per
depth × draw × receptor), with the partner's `.pqt` written into the *same* directory. Block D's
D3 did this implicitly. **A flat shared cache silently serves the wrong depth and nothing catches
it.**

**And on OF3, a short partner may not be typed as a partner at all.** `use_paired_msas` counts
chains with `molecule_type == PROTEIN` (`propose.py:502-504, 524-525`), so **`R0_apo` and
`R1_ct11` are not "partner absent vs partner present" in OF3's alignment machinery** unless
`molecule_type` is set deliberately.

#### 6.4 Deployability verdict

| regime | needs the per-chain mapping? | deployable on 4 backbones today? |
|---|---|---|
| **(a) Stage 1** — receptor depth, **apo monomer**, no ligand | **No** — one chain, one string | **YES.** This is the Block D / D3 code path; it landed 25,810 predictions on all four backbones. |
| **(a) Stage 2** — receptor depth × partner rung | **Yes** | **NO** — §6.2 |
| **(b)** — partner depth ladder | Yes, plus a partner MSA already pinned to 1 | **NO**, and §6.1 says it should not be built |
| **(c)** — receptor depth × partner × ligand | Yes | **NO** — same blocker as Stage 2, plus a third factor |

**The distinguishing fact is not (a) vs (b) vs (c).** All three of the *interesting* forms need
the same unbuilt, untested per-chain mapping across three incompatible keying conventions. What
separates them is only how many factors sit on top. That is what drives the staging in §9.

#### 6.5 And there is no systems file for any of it

`g5_systems.csv` does not exist. `SYSTEMS_LINK` in `redo/build/matrix_cost.py:165-178` carries
**12 entries and no G5 entry**, so `check_against_systems()` is structurally blind to the gap.

> **Group 8 is a multiplication in a cost model. Group 1 and Group 2 are specifications with
> per-row sequences and hashes. The depth axis has no input artefact of any kind.**

Whichever regime is chosen needs its own systems file plus a deliberate B7 widening, both
re-proved by planting.

---

### 7. The depth levels: `{1, 8, 32, default}`

The current spec (`RUN_MATRIX.md:653`, G5a) is `{8, 128, default}`. The proposal is **drop 128
and 512, add 1**.

#### 7.1 Three points cannot see a curve, and the curve is non-monotone

All four corpus papers that swept a depth or masking axis report a **turning point**; none reports
a monotone trend, and two say the optimum **moves per target**:

| paper | levels swept | optimum | target-dependent? |
|---|---|---|---|
| `kalakoti2025afsample2` (AF2, column masking) | 0/5/…/50 % | operating point 15 %; *"beyond 30 % masking, performance drops"* | **yes, explicitly** |
| `kalakoti2026afsample3` (AF3 **and** AF2, same operation) | 2 networks × 6 masking levels × 2 subsampling states | **AF3 40 %, AF2 20 %** | **yes** — *"the optimal level of MSA randomization is protein specific"* |
| `mitjavila2026afsample2t` (AF2, pocket-targeted masking) | 0/10/20/30 % deployed, 50 % swept | pooled mixture; *"50 % collapses"* | pooled |
| `li2026embedding` (fraction of full MSA) | 100/75/50/25/0 % | *"all methods collapse at 0 % MSA"* | not stated |

Three things follow, and they change the design rather than the level count:

**(i) The turning point is architecture-dependent, and our four backbones are all on the side
that tolerates more.** `kalakoti2026afsample3` is the only paper that runs the same operation on
both generations and finds **AF2 degrades past 20 % while AF3 does not**. Boltz-2, OF3, Protenix
and Chai-1 are all AF3-lineage. So the AF2-derived optima (15 %, 20 %) are the wrong prior for
us, and the AF3 one (40 %) is more aggressive than anything our ladder has reached.

**(ii) Our own data agrees — no backbone has turned over at depth 8.**

```
python3 - <<'EOF'
import csv, collections, re
r = list(csv.DictReader(open('analysis/block_d/received_2026_09_13/rows.d3_msa_depth.csv')))
pat = re.compile(r'/(depth\d+|full)/(boltz|chai|of3|protenix)/')
c = collections.defaultdict(lambda: [0, 0])
for x in r:
    d, bb = pat.search(x['input_path']).groups()
    a = float(x['d_npxxy_y558_y753_oh']); b = float(x['d_gpcrdb_tm6_tilt_246_637_ca'])
    c[(bb, d)][0] += (a < 9.08 and b > 14.932); c[(bb, d)][1] += 1
EOF
```

Predicate-active %, recomputed **row-level from all 25,810 Block D D3 rows** (thresholds read
from the rows themselves: `9.08` / `14.932`, identical on all 25,810):

| backbone | depth 8 | depth 32 | depth 128 | depth 512 | full |
|---|---:|---:|---:|---:|---:|
| Boltz-2 | **17.77** (n=1,300) | **7.00** (1,300) | 4.92 (1,300) | 5.38 (1,300) | 5.08 (1,300) |
| Chai-1 | 25.08 (1,280) | 20.16 (1,270) | 19.69 (1,300) | 18.38 (1,300) | 19.37 (1,260) |
| OpenFold3 | 28.00 (1,300) | 26.17 (1,280) | 21.92 (1,300) | 15.35 (1,270) | 12.40 (1,250) |
| Protenix | 15.54 (1,300) | **16.77** (1,300) | 9.69 (1,300) | 2.08 (1,300) | 0.08 (1,300) |

*(This reproduces `GATE_2_D3_SLOPES.md:38-43` to two decimals in all 20 cells, from the row
level rather than from the gate report.)*

Read the rows, not the slopes:

- **Boltz spends 10.8 of its 12.7-point swing between depth 8 and 32.** Above 32 it is flat
  (7.00 / 4.92 / 5.38 / 5.08). On a `{8, 128, default}` ladder, Boltz's 128 and `default` are the
  same point and the arm is effectively two levels.
- **Protenix is non-monotone at exactly the level the current spec drops**: 15.54 → **16.77** is
  the only up-step in the table, and it is at 32.
- OF3 and Protenix do most of their collapse between 128 and full, which `GATE_3` classifies as
  *degradation*, not steering, and which Block D has already characterised at n ≈ 1,250/cell.
- **Nothing has turned over at 8.** All four sit at an extreme there. Read next to
  `li2026embedding`'s floor at zero and `kalakoti2026afsample3`'s "AF3 does not degrade past
  20 %", **the shallow end is the unexplored end.**

**(iii) Masking and subsampling are not substitutes.** `kalakoti2026afsample3`: *"employing
subsampling along with MSA masking was the optimal strategy for a sizable number of targets."*
A referee cannot be told that our depth arm covers the masking family.

#### 7.2 The proposal, and why depth 1 specifically

**Drop 128 and 512:**

- **128 and 512 earn nothing.** Block D measured both, apo, at n ≈ 1,250–1,300/cell. 128 is where
  three of four backbones show no step; 512 sits inside the collapse region `GATE_3` classifies
  as degradation. Neither carries a turning point.

**Add 1:**

- **It is the anchor the ladder has never had** — `li2026embedding`'s floor, and the level
  `schafer2025confounds` and `feldman2026alphainterp` use. It is the only point on the axis where
  the answer is known in advance, which is precisely what makes it useful as a bound.
- **Depth 1 on the receptor is the mirror of what we already do to the partner.** A receptor at
  depth 1 beside a full-Gα partner at query-only is a **pure single-sequence two-chain
  prediction**: no evolutionary information anywhere in the input. If the α5 effect survives that,
  it is steric or structural by construction. It is the cheapest and cleanest version of E1.9's
  question and it comes free as a level on an axis already being varied.

**State honestly in the Methods: depth 1 is not a point on a depth continuum, it is the "no
evolutionary information" endpoint.** Treat it as an anchor, not as a regression point — and in
particular do **not** include it when fitting a slope in `ln(depth)`, where `ln(1) = 0` would
give it leverage it has not earned.

| ladder | cells/receptor (× 3 rungs × 2 ligands) | CORE-L17 × 4 bb × n=10 |
|---|---:|---:|
| G5a as specified `{8, 128, default}` | 18 | **12,240** |
| **proposed `{1, 8, 32, default}`** | **24** | **16,320** |
| G5b `{8, 32, 128, 512, default}` | 30 | **20,400** |

**+4,080 over G5a (8.9 % of MINIMAL) and 4,080 *fewer* than G5b**, for a ladder placed where the
evidence says the shape is. If only three levels are affordable, the honest three are
`{1, 8, default}`. `{8, 128, default}` is the one combination that spends three levels to learn
nothing new.

#### 7.3 A unit problem nobody has written down

**The corpus's optimum is in fraction units; our ladder is in count units; and the denominator
was never recorded.** All four non-monotone papers report a **rate** (masking % or MSA fraction).
The papers that report a **raw row count** — `ye2026multistatebias` (U10, U100),
`waymentsteele2024cluster` (|MSA| = 10, 100), `suzuki2026conforflux` ({2…128}),
`feldman2026alphainterp` ({1,5,10}, {1,10,20,50,100}) — are a different set, and **none of them
is one of the four that found a turning point.** The optimum is only ever reported in a unit our
ladder does not use.

The bridging unit is absent too. **Neff appears in exactly two corpus papers —
`abramson2024af3` Ext. Data Fig 7A p.18 and `suzuki2026pairscaling` Fig 7 p.10 — and in both it
is a *descriptive* property of natural alignments. No paper reports a subsampling depth in Neff
units.** *(An earlier form of this claim, "no Neff figure exists anywhere in the corpus", is
false and is still sitting in `MSA_SUBSAMPLING.md` §5.2(b); lit withdrew it 2026-09-12.)*

And the denominator varies ninefold across our own panel:

```
## parsed from data/block_b/03_msa_audit/msa_depth_report.md, 48 receptors
```

**Receptor alignment depth spans 1,996 (CNR2) to 18,146 (DRD2), median 8,764, no receptor below
1,000, ratio 9.09×.** So:

| depth level | % of CNR2's alignment | % of DRD2's |
|---:|---:|---:|
| 1 | 0.050 % | 0.006 % |
| 8 | 0.401 % | 0.044 % |
| 32 | 1.603 % | 0.176 % |
| 128 | **6.413 %** | **0.705 %** |
| 512 | 25.651 % | 2.822 % |

**A count-based ladder is a different manipulation on each receptor**, and the two units do not
convert without the per-receptor full depth — which, per F-6, was never stored.

**Proposal: keep counts as the primary axis** (so the new ladder joins Block D's, which is worth
more than matching the corpus), **and record `receptor_msa_depth_at_full` per row** so fraction
is derivable post hoc. Report fraction as the secondary axis. **Do not add a fraction-based arm**
— the derived column gets most of the value for zero predictions.

#### 7.4 One published design not to copy

`mitjavila2026afsample2t` deploys a **pooled mixture** — 250 models each at 0/10/20/30 % masking,
contributing 16/14/26/44 % of the top-1 % enriching models. It does not transfer, and the reason
is the readout. **Their metric is best-of-N enrichment against a reference, where pooling
strictly helps: adding any level can only add candidates. Ours is a rate** — the fraction of
samples satisfying a state predicate — where pooling across levels estimates a weighted average
of the levels you happened to pool, with the weights a design choice masquerading as a result.
**Keep the levels separate, report per-level rates, do not pool.**

#### 7.5 `full` is not `default`, and the anchor is not yet fixed

`build_tier_d3_manifest.py:59` says `"full"` means "live-fetch or no subsample", but
`msa_a3m_path_for()` returns a concrete cached path for `full` too, which sets `MSA_A3M_PATH` and
therefore **disables** the live server. **`full` is a cached full fetch through the subsample
pipeline; `default` is a live fetch.** `PARTA_D3.md:128` records 12 of 28 cells disagreeing
between the two. Catalogue **E8.3 marks fixing this anchor as blocking**, and the record columns
must carry `default` and `full` as **distinct** values, never collapsed.

---

### 8. G17 — the partner-MSA binary. Blocking, not supplementary.

**What it is.** `item = G17(proposed)`, `arm = partner_msa_on`, **90 rows** of
`g1_systems.csv`, `partner_msa = ON`, at three fixed lengths — `R3_ct21`, `R5_a5plus`,
`R7_full` — over **30 receptors in 29 clusters**, on all four backbones. It is the MSA-**on**
half of a contrast whose MSA-**off** half is already the primary condition on every other row.
It maps to catalogue **E1.9**.

**What it costs.**

```
python3 redo/build/matrix_cost.py
```

| id | grain | panel | backbones | cells/rec | n | predictions |
|---|---|---:|---:|---:|---:|---:|
| **G17a** | pooled | 30 receptors | 4 | 3 | 10 | **3,600** |
| **G17b** | per-cell | 30 receptors | 4 | 3 | 50 | **18,000** |

Both reproduce exactly from `g1_systems.csv`'s own `predictions_pooled` / `predictions_percell`
columns (`check_against_systems()`: 12/12 linked items agree). **3,600 is 7.9 % of the MINIMAL
tier (45,860).**

**Why it is blocking rather than supplementary.** Three independent arguments:

1. **The primary design does something nobody in 83 papers has done.** Lit, three clean absences
   quoted as absences: *"One-chain-only single-sequence in a complex: absent from corpus"* —
   depth 1 exists in `feldman2026alphainterp` and `schafer2025confounds`, **but all monomers**.
   *"No paper in 83 subsamples, masks, deletes or otherwise manipulates the PAIRED MSA of a
   complex as an experimental variable. Nobody even reports what they did with it"* — only 5 of
   83 notes mention paired/unpaired at all, four of them pipeline description. *"Zero papers"*
   report whether perturbing one chain's MSA in a complex affects the other chain or the
   interface. **So by running every cognate row with the partner at query-only, the primary
   Group 1 design is the first instance of one-chain single-sequence inside a complex anywhere in
   the corpus.** Whether that is *a novelty worth claiming* or *an uncontrolled choice worth
   bounding* is decided entirely by whether G17 runs.
   *(Trap: `feldman2026alphainterp` p.35 — "All paired MSAs are replaced with the query sequence"
   — is 400 **monomers**, AF3 input-schema housekeeping. Do not cite it as a complex
   manipulation.)*
2. **It bounds the price of the headline arm.** At `R7_full`, query-only runs a complete Gα with
   a crippled alignment, removing the co-evolutionary pairing signal **from the arm that carries
   the paper's headline**. G17 is the only thing that measures what that cost was — *"how much
   did we change by doing that?"*, which is the first question a referee asks
   (`MSA_SPEC.md` §8; `DECISIONS.md` D-B; `CAMPAIGN.md` D-B option (c)).
3. **It answers a mechanistic question the corpus has never asked of a protein partner.**
   E1.9: *"If the effect survives MSA-free, it is steric or structural; if it collapses, it is
   co-evolutionary."* `CATALOGUE.md:1660`: the MSA-mechanism debate is mature and entirely about
   the *receptor's* alignment — **"Nobody asks it of a protein partner."**

**Its budget status is the anomaly.** G17a and G17b are enumerated, costed and cross-checked, and
they appear in **no budget tier**: `TIERS` in `matrix_cost.py:209-217` lists MINIMAL, INTENDED and
EXPANSIVE, and **none of G16a/b, G17a/b, G18a/b, G19, G20, G1c-opt, G1e, G1f, G10b** appears in
any of them. Twelve costed items, zero budget lines. G17 is the one of the twelve with a
first-order claim behind it.

**Not to be confused with Group 8.** E1.9 varies **pairing on the partner chain**, binary, at
fixed lengths. Group 8 varies **the depth of the receptor's own alignment**. Different factor,
different literature, different open question. Both should run; neither substitutes for the
other; **a design document that lists only one of them has an MSA gap.**

**And one arm it preempts.** "Scrambled partner × partner-MSA on" is **not** a new experiment:
`SEQUENCES.md` §6 tabulates the expected depth for every ct21 control as ≈ 1, so the new cell is
probably an input-equivalent copy of the existing MSA-off cell and the interaction collapses to
the already-funded G17 main effect.

---

### 9. The staged plan

Every stage is a stopping point that buys a complete sentence. **Marginal costs, not gross —
each stage reuses the cells below it.**

#### Stage 0 — zero GPU. Blocking on everything below.

| item | what | cost |
|---|---|---|
| **E8.3 / P3** | Anchor the ladder: is D3's `full` rung the same condition as `default`? `PARTA_D3.md:128` — 12 of 28 cells outside D1's Wilson CI | free (one sentence from the pipeline team) or 600 preds |
| **Option Z** | Measure receptor-side and **paired** depth per (receptor, rung) on CORE-L17. **A paired depth has never been measured by anyone** | 0 preds, ~200–400 server queries |
| **the record columns** (§10) | especially the two pocket-RMSD columns | 0 preds |
| **the four-backbone mapping test** | one system, one depth, all four backbones; plant a chain-ID-keyed dict and assert Protenix **fails** rather than silently full-depth-fetching | ~8 preds |
| **the rename** | `off` → `query_only` | 0 preds |
| **SEQUENCES.md §6.1(4)** | submit the ~60 distinct peptide-rung sequences and record `n_seqs` — hours of wall-clock, no inference. **Still an open WAIT in `g1_preflight.py`** | 0 preds |

**Do not commission a two-chain depth cell before the mapping test passes by planting.** §6.2 is
a defect that produces a plausible number in every artefact.

#### Stage 1 — regime (a), apo. The competing-explanation control.

Receptor depth `{1, 8, 32, default}` × **R0 apo** × no ligand,
**CORE-L17 (17) × 4 backbones × n=10 = 2,720 predictions.**

**Why first:** the competing explanation is *"a shallow MSA alone drives GPCRs into the active
state."* That claim is **apo and partnerless by construction**, so measuring it is a **monomer** —
it never touches the broken per-chain mapping, and it runs on the exact code path that already
landed 25,810 predictions on four backbones.

It also removes the confound in the corpus's best existing answer. `ye2026multistatebias` asks our
question on our receptor with a state readout and answers against the competing explanation —
*"MSA-level manipulation alone, whether through evolutionary clustering or random subsampling, is
largely insufficient to overcome the systematic conformational bias"* — while the partner
*"shifted predictions toward the expected active conformation across predictors"* (p.13, p.15).
But its subsampling leg is explicitly a different architecture, verbatim p.15: *"To provide a
baseline comparison using an **AlphaFold2-based** MSA manipulation approach distinct from the
newer architectures evaluated above, we applied AF-Cluster to all four target proteins."* Two
caveats, both to be stated carefully rather than pushed: **samples and seeds per strategy are NOT
REPORTED**, and the one count that is given (SecA: *"only four DBSCAN clusters of size four to
five sequences each"*) shows that baseline was underpowered by MSA composition — **a statement
about SecA and AF-Cluster, not about β2AR or about uniform subsampling.**

> **Sentence it buys:** *"On the same panel and the same four models, reducing the receptor
> alignment to N rows raises the apo active-predicate fraction by X points, while supplying the
> α5 C-terminus raises it by Y — and of the shallow-MSA predicate-actives only Z % are within
> 1 Å of the deposited active pocket, against W % for the co-input."*

That last clause is the strong form, and it is buyable today because Block D already carries the
fidelity columns. Recomputed from the 25,810 D3 rows, among **predicate-active** samples, the
fraction within 1 Å of the deposited **active** pocket:

| backbone | depth 8 | full |
|---|---:|---:|
| Boltz-2 | **88.74 %** (n=231) | 98.48 % (n=66) |
| Chai-1 | 75.70 % (n=321) | 77.87 % (n=244) |
| OpenFold3 | **42.86 %** (n=364) | **56.77 %** (n=155) |
| Protenix | **68.32 %** (n=202) | 100 % (n=1) |

If the partner arm's predicate-actives are ~90 % sub-Å and the shallow-apo ones are ~43 %, then
*"shallow MSA also produces active calls"* is **not a competing explanation** — it produces a
**different object that trips the same two distances.** That is a far stronger result than an
effect-size comparison.

**What Stage 1 does not buy:** any statement about interaction. It cannot say whether depth and
the partner act on one mechanism or two.

**Stage 1 also carries two further arms, and their settings are inherited, not tuned** (§11):

| arm | job | where the setting comes from |
|---|---|---|
| uniform random depth `{1,8,32,default}` | the cheap floor; connects to Block D | **coverage** — placed where the response is unexplored |
| **column masking at 40 %** | the strongest available attack; **never done on GPCRs** | **inherited from `kalakoti2026afsample3`** |
| column shuffle at one shallow cell | information, or noise? | `waymentsteele2025reply`'s own control |

*(No document in `redo/spec/` states a prediction count for the 40 % masking arm. That is a real
gap in the plan, not an omission here.)*

#### Stage 2 — regime (a) × partner rung. E8.1.

Depth `{1, 8, 32, default}` × `{R0, R3_ct21, R7_full}` × no ligand, CORE-L17 × 4 bb × n=10 =
**8,160 predictions — of which Stage 1 already supplies the 2,720 R0 cells, so the marginal cost
is 5,440.** Gated on Stage 0's mapping test.

**One live tension, currently unreconciled between two documents, and neither cites the other.**
`CATALOGUE.md:1318-1332` advises **against** crossing depth with apo and cognate, because both
endpoints are pinned (apo 0.158, cognate 0.891), and recommends the **middle rungs** — that
optimises for *estimating an interaction*. The control question in Stage 1 needs the pinned
endpoints. G5a includes R0, R3_ct21 and R7_full, so it satisfies both. **Resolution: keep all
three rungs and say in advance which contrast answers which question.** R0 vs R7_full is the
control; R3_ct21 is where the interaction has headroom.

> **Sentence it buys:** *"A supplied α5 C-terminus flattens / does not flatten the depth slope"* —
> one mechanism or two. Either result is publishable and they are distinguishable.

**Caveat to state in advance, never afterwards:** interaction MDE at k=17 clusters is **0.295**
(`1.218/sqrt(17) = 0.2954`). An interaction below that is reported as *unestimable at this n*,
**never as absent.**

#### Stage 2b — the partner-MSA binary, in place of regime (b). G17 / E1.9.

**3,600 predictions** (§8).

#### Stage 3 — regime (c), add the ligand. E8.2 / the full cube.

Depth `{1, 8, 32, default}` × 3 rungs × `{none, agonist}`, CORE-L17 × 4 bb × n=10 = **16,320**;
Stage 2 is a subset, so the marginal cost is **+8,160**.

**The crossing is unoccupied, from both directions, and the corpus says so in its own words.**
`jung2026boltzperturb` perturbs the MSA with the ligand held fixed; `lazou2026cryptic` varies the
ligand with the MSA held fixed. *"Neither crosses them, so the interaction between alignment
depth and ligand occupancy is unmeasured on AF3-lineage models from both directions."*
*(Trap: `xing2025purified` looks like a crossing and is not — protein-alone is AF2, the ligand
leg is AF3, p.5.)*

**One prior effect size exists and it points the other way from the apo result.**
`jung2026boltzperturb` measures MSA perturbation *in the presence of* a ligand on Boltz and
reports **SR_O 10.53 % masked, 12.28 % subsampled, both below vanilla** (p.7). So with a ligand
held present, degrading the alignment **hurts** — the opposite sign to Block D's apo effect
(+12–16 points of predicate-active at depth 8). That is either a readout difference or a real
ligand × depth interaction, and either way it is the first quantitative reason to expect the
ligand factor to do something.

**(c) is not premature — the ligands exist.** `g2_systems.csv` carries 100 `full_agonist` rows
over 26 receptors, of which 20 are `dispatch_status = READY` spanning 19 clusters. CORE-L17 is 17
receptors in 17 clusters, so the ligand panel covers it. **But it is third**, because its
headline is a three-factor statement resting on an interaction the design may not resolve.

> **Sentence it buys:** *"A partner rescues what depth removed; an agonist does not"* — or, if the
> ligand does rescue, `ye2026multistatebias`'s asymmetry does not survive on an AF3-lineage panel
> at scale, **which is the more interesting result**.

#### Two cheap additions to fund before Stage 3

- **Option Z2 — the column-shuffle control, 680 predictions** (17 rec × 4 bb × 1 extra level ×
  n=10, restricted to the apo shallow cell). `waymentsteele2025reply`: *"column shuffling destroys
  the state-specific predictions."* Same row count, shuffled columns — **depth held exactly
  constant while local coevolution is destroyed.** It is the direct analogue of our
  scrambled-partner arm applied to the alignment, and it converts *"shallow MSA also produces
  active calls"* from an effect size into a mechanism statement. It is also the control
  `schafer2025confounds` says AF-Cluster lacked.
- **The seeds-only cell, 300 predictions** (6 rec × 1 bb × 1 cell × n=50 at `default` depth).
  `stein2022speachaf` **concedes seeds alone reach some alternate states** (p.8, p.13). Without
  this, the subsample-draw variance probe measures draw-variance against an unmeasured baseline.

**980 predictions, 2.1 % of MINIMAL, and each answers a question a published paper has already
shown matters.**

#### The bill

| stage | marginal predictions | cumulative | % of MINIMAL (45,860) |
|---|---:|---:|---:|
| Stage 0 — anchor, Z, mapping test, columns | ~600 (or free) | 600 | 1.3 % |
| **Stage 1 — (a) apo, 4 depths** | **2,720** | 3,320 | 7.2 % |
| Z2 + seeds-only | 980 | 4,300 | 9.4 % |
| Stage 2 — (a) × partner rung (+R3, +R7) | 5,440 | 9,740 | 21.2 % |
| **Stage 2b — G17a, partner MSA on/off** | **3,600** | 13,340 | 29.1 % |
| Stage 3 — + agonist level | 8,160 | 21,500 | 46.9 % |

For comparison: G5a as specified is 12,240, MINIMAL is 45,860, and the whole A–D campaign was
124,470. **Stages 0–2b total 13,340 — 9.0 % more than G5a alone, and they include G17, which G5a
does not.** Every intermediate stage is a stopping point that buys a complete sentence; G5a as a
single 12,240-prediction commitment buys nothing until all of it lands. **That is the case for
staging, and it is not a budget argument.**

---

### 10. What must be recorded

`redo/inputs/g1_recording_spec.tsv` carries **49 declared columns today** (50 lines, one header;
all 49 names distinct). **Four are MSA-related:**

| column | grain | dtype | status |
|---|---|---|---|
| `partner_msa_mode` | row | str | new |
| `partner_msa_depth` | row | int | new |
| `partner_msa_depth_uniref90` | row | int | new |
| `receptor_msa_depth` | row | int | exists |

They are necessary and roughly half sufficient. **Twelve additions are named as blocking. Two of
the twelve have landed; ten have not.**

```
python3 -c "
import csv
have={r['column'] for r in csv.DictReader(open('redo/inputs/g1_recording_spec.tsv'),delimiter='\t')}
for w in [...]: print(('PRESENT ' if w in have else 'ABSENT  ')+w)"
```

| # | column | why | present today? |
|---|---|---|---|
| 1–2 | `pocket_ca_rmsd_active`, `pocket_ca_rmsd_inactive` | the depth sweep's only reference-based readout; separates *"active by predicate"* from *"active like the crystal"* | **PRESENT** (rows 48–49, added since the review) |
| 3 | `receptor_msa_depth_target` **and** `receptor_msa_depth_realised`, as two columns | `subsample_msa.py:106-107`'s silent no-op means a rung label is not a depth. *"A rung label is a design fact; a depth is a measurement"* | **ABSENT** |
| 4 | `receptor_msa_depth_at_full` | the denominator (§7.3) | **ABSENT** |
| 5 | `msa_target_unreached` (bool) | the no-op must be **true**, never silent | **ABSENT** |
| 6 | a written definition of what `depth` counts — is the query row in or out? | `rung_msa_depth.csv` says **0** for ct11; the Chai cache says **1** for an 11-mer; `MSA_SPEC.md:151` asserts `== 1`. **Two of those three conventions make that check fire on every correct row** | **ABSENT** (one sentence in the spec) |
| 7 | `msa_mode_label`, with `default` and `full` as **distinct** values | `PARTA_D3.md:128` — 12 of 28 cells disagree otherwise | **ABSENT** |
| 8 | `receptor_msa_sha256`, `partner_msa_sha256` | the file actually consumed | **ABSENT** |
| 9 | `msa_paired_depth`, `msa_paired_is_copy_of_unpaired` (bool) | a paired depth has **never been measured by anyone**, and `propose.py:471-472` / `:599-600` assign one path to both slots without raising | **ABSENT** |
| 10 | `msa_source` — `live-colabfold` / `live-protenix` / `prefetched` / `cache`, **derived from the env var actually set** | two of four launchers assert it as a hardcoded literal today | **ABSENT** |
| 11 | `msa_subsample_draw_id`, `msa_subsample_seed`, distinct from the prediction seed | D3 shared one stream (`subsample_msa.py:104`), so draw-variance and seed-variance are **not separable** in anything D3 shipped | **ABSENT** |
| 12 | `chai_msa_directory` and its hash | Chai resolves by sequence hash and the sequence is identical at every depth. **The directory is the only artefact that distinguishes a depth-8 Chai row from a depth-full one.** Record it or Chai's depth arm is unfalsifiable | **ABSENT** |

**Why any of this is needed: F-6.** Across all 42,180 predictions of the frozen campaign, **no MSA
metadata reaches any scored row at all** — a grep of every row-touching scorer module for
`msa|a3m|pqt` returns nothing. Verified again here directly on the delivered rows: the 25,810-row
Block D D3 file
(`analysis/block_d/received_2026_09_13/rows.d3_msa_depth.csv`, 102 columns) has **zero columns
matching `msa|depth|a3m`**. The depth of a D3 row is recoverable only by parsing it out of
`input_path`. **You cannot join MSA depth, source or pairing state to a scored prediction.**

#### And the checks, each proved by planting its defect

- `partner_msa_depth == <the agreed query-only value>` on every two-chain row. **Plant a row
  carrying the partner's real alignment; the check must fail.** This is the *only* thing that
  catches §6.2's Protenix key mismatch.
- `receptor_msa_depth_realised <= target`, and `== target` unless
  `receptor_msa_depth_at_full < target`, in which case `msa_target_unreached` is **true**. Plant a
  short alignment; the flag must fire.
- Receptor depth unchanged between a ladder row and the matched apo row for the same receptor.
  Plant a subsampled receptor MSA; must fail.
- Output matches input: returned chain count and returned partner sequence match what was
  requested. This closes the class nothing currently checks — **a monomer returned where a dimer
  was asked for passes every existing check.**
- **A missing column is a FAILURE, not a skip.** An MSA check that skips when
  `receptor_msa_depth_realised` is null is F-6 recurring in the shape of a passing gate.

---

### 11. Two rules that govern every hyperparameter here

#### 11.1 Inheritance, and what oracle leakage means here

> **Every hyperparameter is INHERITED from published work on other proteins and is never swept on
> our panel.**

**Every paper in this area that tuned its subsampling hyperparameter against deposited structures
is recorded in our corpus as oracle leakage.** Concretely:

- `kalakoti2025afsample2` — *"The masking fraction was chosen by scoring the sweep against the
  deposited open/closed structures **of the OC23 evaluation targets themselves**"*, and the
  confidence-screening threshold *"is likewise tuned against a reference-defined optimum."*
- `kalakoti2026afsample3` — **the paper we inherit the 40 % from** — *"the masking fraction and k
  are tuned on the **same 238-target set the results are reported on**, there is **no post-cutoff
  or memorization control at all**."*
- `mitjavila2026afsample2t` — *"the masking level and the 0–30 % ensemble composition were fixed
  by maximising accuracy against the deposited structures of the **same 10 evaluation targets**."*

**Oracle leakage, in this project's usage, means: a hyperparameter whose value was selected by
consulting the deposited structure the experiment is supposed to predict.** Once that happens,
the reported accuracy is partly a measure of the tuner and not of the method, and there is no
prospective claim left. The clean counter-example the corpus supplies is `suzuki2026pairscaling`:
a **structure-free** selection criterion on a fixed shared MSA. **What separates the two is
whether the criterion references the deposited answer.**

Two consequences for us:

1. **We take 40 % from `kalakoti2026afsample3` and do not re-tune it.** Inheriting a
   possibly-overfit constant from another panel is a *transfer*, which is honest and testable;
   re-fitting it on ours would reproduce the leakage.
2. **One honest disclosure to make in the Methods, in these words.** Our depth levels
   `{1, 8, 32, default}` were placed partly because no backbone turned over at depth 8 in Block D.
   **That is our own data — but used for coverage, not to maximise an outcome.** Say so
   explicitly rather than leaving it implicit.

#### 11.2 DBSCAN / AF-Cluster is DECLINED, on five grounds

| # | ground | evidence |
|---|---|---|
| 1 | **50–300× the cost, and it does not win at matched n.** Plain random shallow (CF-random) needs **1–2 runs** per ensemble (KaiB 2, Mad2 1, RfaH 2); AF-Cluster needs **95–329** (KaiB 329, Mad2 95, RfaH 250). At matched ensemble sizes — *"CF-random 330 vs AF-cluster 329 for KaiB"* — **the cheap method still matches or beats the expensive one** | `schafer2025confounds` p.4 Fig 2b, p.5 |
| 2 | **There is a published rebuttal against it**, and it reports that AF-Cluster *"mistakes some single-folding KaiB homologs for fold switchers"* | `schafer2025confounds` |
| 3 | **`min_samples` (the DBSCAN *k*) is NEVER REPORTED anywhere.** Epsilon is swept 3–20; the *k* is described in Methods and no value appears in the paper. **We could not reproduce it faithfully even if we wanted to** | `waymentsteele2024cluster` p.9 |
| 4 | **None of the three clustering papers touches a GPCR, and two say so explicitly.** `waymentsteele2024cluster`: *"No membrane proteins, GPCRs, kinases or transporters are studied."* `bryant2024cfold`: *"No GPCR, and no 7TM or membrane receptor of any kind, is named anywhere in the main text, any figure, any figure caption, or the Methods."* `cheng2026af3cluster` is abstract-only and unverified | lit, first-hand |
| 5 | **`bryant2024cfold`'s chain filter actively discards the G-protein / arrestin / nanobody partners that define an active-state GPCR entry** — so the method as published cannot see the systems we study | `bryant2024cfold` note |

**And the positive finding behind the decline:** on GPCRs *no* subsampling family has a positive
claim, the strongest-in-general families have never been tested on a GPCR state readout, and the
**one family that has been so tested failed** (`ye2026multistatebias`, β2AR). The most dangerous
attack a referee could name is **not a published result** — it is column masking at AF3's 40 %
optimum applied to GPCRs, which nobody has done. That is why the 40 % masking arm is in Stage 1
and DBSCAN is not.

---

### 12. The caveat this whole design owes, stated up front

> **An apo-only control defeats the rival explanation *as stated*, and does NOT bound the complex
> case.**

Across all 83 corpus papers the **monomer → complex boundary is never discussed as a boundary.**
`mitjavila2026afsample2t` is the only paper with the design to measure transfer — it masks the
same receptor alone *and* in complex, 250 models per cell — and it **never contrasts them**: the
two cells are pooled into one docking ensemble, the state label is assigned to the input condition
*a priori*, and the readout is binding-site side-chain RMSD, producing *"local side-chain and
backbone heterogeneity in the pocket, not alternative global states."* Sharper still:
**`ye2026multistatebias`'s subsampling arm runs on AlphaFold2, not Multimer, so the only GPCR
MSA-manipulation test with a state readout is itself apo-side.**

**Write the caveat; do not spend predictions pretending to close it.**

Seven further things this design does **not** control for, to be stated rather than implied:

1. **Three of the four MSA-manipulation families.** Ours is **uniform random depth reduction**
   only (`subsample_msa.py:104-117`): keep row 0 (the query), draw `depth − 1` rows uniformly with
   `random.Random(seed)`, sort back into a3m order, write atomically. Untested: **clustering**
   (which rows, by sequence similarity), **composition purification** (which rows, by "sequence
   purity" — explicitly *not* depth), **column masking** (which *positions*, not which rows).
   Column masking must be named separately: it is what the corpus's only `factors-crossed` paper
   does, it is the family in which the non-monotone optimum was established, and
   `kalakoti2026afsample3` — the one paper that ran both on the same targets — found them
   **complementary, not substitutes**.
2. **The paired depth**, unless the record columns land. **Nobody has ever manipulated the paired
   MSA of a complex as an experimental variable, and nobody reports what they did with it.** So
   there is no published convention to inherit and no prior to cite. Until we record it,
   *"we subsampled the receptor MSA"* is, on three of four backbones, actually *"we subsampled the
   receptor's unpaired MSA **and** replaced its paired MSA with the same file."*
3. **The cross-chain effect — zero papers, ours included.** *"Nothing in the corpus reports whether
   perturbing one chain's MSA in a complex affects the other chain's predicted structure or the
   interface."* Our design perturbs one chain (the partner, to query-only) and reads out the other
   (the receptor's state). G17 bounds **one binary contrast**; it does not characterise a
   cross-chain effect. **Say that.**
4. **The cold/warm paired-search asymmetry between the two arms the paper contrasts.** The
   pre-warm submitted one sequence per ticket in mode `env`, never a pair; Boltz's paired mode
   string is `pairgreedy-env`. **Every cognate-arm prediction on Boltz/OF3/Protenix paid a cold
   paired search while its apo counterpart hit a warm cache.** Stated as a code-level inference,
   not a measurement. Uncontrolled in Blocks A–D and would remain so.
5. **Whether a short partner is typed as a partner at all** on OF3 (§6.3).
6. **Chai is not the same experiment.** It never pairs, so its apo→cognate delta is one chain
   where the other three are one chain plus an alignment regime. And Chai's depth slope **does not
   survive its CI** — `−0.815 [−2.380, +0.357]`, withdrawal `W-D-5`. **"All four backbones" is
   already withdrawn once on this axis. Do not let it back in through a heading.**
7. **Confidence cannot arbitrate a depth sweep.** `kalakoti2025afsample2` p.6: *"model confidences
   from different MSA masking levels are not directly comparable"*, with confidence decaying
   monotonically (~2 % per 5 pp of masking, ≈89 at 0 % → ≈63 at 50 %) even where accuracy does
   not. So do **not** use pLDDT/ipTM to pick a depth level or compare across them. **This is the
   same phenomenon as the paper's third title clause, arriving on a new axis** — and it is why the
   two pocket-RMSD columns are the difference between a depth ladder that has a readout and one
   that does not.
8. One organism, one receptor class, 17 of 32 clusters. CORE-L17 is the ligand-complete
   one-per-cluster panel, not the census. And `li2026embedding`'s floor — the published anchor for
   depth 1 — is the **least-sampled point on every one of its curves** (n = 3 at the two endpoint
   depths vs 9 elsewhere), so do not quote the collapse as firmly as the interior. Our own depth-1
   arm at 17 receptors × 4 backbones × n=10 would be considerably better sampled than the
   published floor it is anchored to, **which is a point in its favour, not against**.

---

### 13. Disagreements found while checking

| where | document says | the file says | status |
|---|---|---|---|
| `MSA_SPEC.md:35` (a document **sent to the pipeline team**) | R6a/R7 partner depth **"8,474–9,203"** | `R6a_da5` **5,764–9,176**, `R7_full` **6,289–9,203** over `note=="ok"` rows. 8,474 is Gq's single R6a value | **wrong; lower bound understated by ~2,700 rows.** Four families (G12, G13, Golf, G15) sit below 7,000 on both rungs. Argument unaffected — still three orders of magnitude above ct11 — but the number is wrong. Already caught in `MSA_SUBSAMPLING.md` §2; **still not fixed in `MSA_SPEC.md`** |
| `MSA_SPEC.md:35` | R6a/R7 lengths **"368 / 394"** | those are **Gs**; families span **324–368** (R6a) and **350–394** (R7) | wrong-as-stated |
| `DECISIONS.md` F-5 table | R6a/R7 **"8,474–9,203"**; R3_ct21 **"47-581"** | same as above; R3_ct21 max is **582 (Golf)**, 581 is Gs | the same stale number in a second document |
| `MSA_SUBSAMPLING_REGIMES.md` §4, §7 | the recording spec carries **47 columns**; `pocket_ca_rmsd_active/inactive` **"verified absent"** | **49 columns**; both pocket-RMSD columns **PRESENT** (rows 48–49), added by `redo/build/g1_recording_spec.py` | **stale — the ask was satisfied after the review was written.** The other ten blocking columns are still absent |
| `FROZEN_VS_REDO.md:22` | "47-column recording spec … `pocket_ca_rmsd_active/inactive` is **absent**" | 49 columns, both present | same staleness |
| `CLAUDE.md` (project brief) | "**14 of 64 inputs name no generator**", and `g1_recording_spec.tsv` "has no writer anywhere in `redo/build/`" | `MANIFEST.tsv` has **65 rows and 0 blank generators**; `redo/build/g1_recording_spec.py` **exists**. 16 entries name a generator that is not a file in `redo/build/` — 15 of them the literal string `unattributed`, one a comma-separated pair | **stale on both counts.** The real residual is 15 `unattributed` + 1 unparsed pair |
| `GATE_2_D3_SLOPES.md` | worst cells "n=1,250 at OF3×full and Chai×full" | OF3×full **n=1,250**; Chai×full **n=1,260** (Chai's smallest is depth 32 at **n=1,270**… smallest overall is OF3×full) | minor; the 20-cell table itself reproduces exactly |
| `rung_msa_depth.csv` vs the Block B Chai cache | both called "partner MSA depth" | the ColabFold rung series ≈ **0.985 × the Chai cache's UniRef90 count** and ≈ **0.60 × its total** | **not a disagreement between documents — a units problem nobody has written down.** Do not compare a value from one series against a threshold from the other |
| `g2_systems.csv` | — | **22 rows supply the ligand as a polymer chain** (`ligand_is_chain = 1`); the file has **no `ligand_msa` column**, the string `ligand_msa` appears nowhere in `redo/`, and gate G-11 checks only `partner_msa` | **an undeclared and unchecked third chain**, including substance P (Block B depth **1**) and endothelin-1 (depth **732**) |
| `g1_systems.csv` / `MSA_SPEC.md` | level named `off` | the specification is **query-only, depth 1**, and `MSA_SPEC.md` §4 argues at length that *absent* and *query-only* are **not** equivalent on three of four backbones | **the naming defect of §3. Free to fix in a generator; not yet fixed** |
| `g1_preflight.py` B18 vs `g1_systems.csv` | "21 arms, all costed" | B18 counts **distinct `item` values (21)**, not arms; distinct `arm` values are **23** | not an error in the check — the passing message uses "arms" for "items". Worth a word-change so the number is not mis-quoted |

---

# Part 8. The 45 catalogued experiments

### What the catalogue is

`redo/spec/CATALOGUE.md` (1,847 lines, compiled 2026-09-11) is the menu of everything the
redo campaign *could* run. It is explicitly **"a catalogue with costs and a ranking, not a
programme"** — nothing in it is authorised, and as of 2026-09-14 **nothing has run**.
Each entry states a question, a design, a cost class, its dependencies, and a *novelty
verdict* graded against the 81-paper literature corpus in `lit/`.

Three separate documents describe the same 45 entries from different angles, and a reader
needs all three:

| document | what it is | what it decides |
|---|---|---|
| `redo/spec/CATALOGUE.md` | the menu — question, design, cost, novelty, per-experiment | nothing; it is input to a decision |
| `redo/spec/PLAN.md` | the ordering of record — six pillars plus a ten-step route | what runs and when |
| `redo/inputs/run_registry.tsv` | the hand-authored join, 45 rows × 19 columns | which catalogue entry sits in which pillar |

**`run_registry.tsv` is the only machine-readable join between the catalogue and the plan,
and it exists because `PLAN.md`'s pillar sections name almost no experiment ids.** Read the
registry's `pillar` column rather than inferring a mapping from `PLAN.md` prose.

### How many experiments there actually are

```
grep -cE '^### E[0-9]' redo/spec/CATALOGUE.md                              -> 45
grep -E  '^### E[0-9]' redo/spec/CATALOGUE.md | grep -oE 'E[0-9]+\.[0-9]+' | sort -u | wc -l  -> 46
grep -cE '^## Group '  redo/spec/CATALOGUE.md                              -> 10
awk 'END{print NR-1}'  redo/inputs/run_registry.tsv                        -> 45
```

There are **45 headings carrying 46 distinct experiment ids across 10 groups**. The
46th id exists because **E6.2 and E6.3 share a single heading** (`### E6.2 / E6.3 — Ship
the three Block D rows.csv and rows.tier3.v2.csv`). `run_registry.tsv` has 45 rows and
**no E6.3 row at all** — E6.3 is folded into E6.2. Every "45" in this project is a count
of headings, not of ids.

The catalogue's own header records that this count was wrong before: it, its header and
`RUN_MATRIX.md` all said **"33 experiments in 9 groups"** until 2026-09-12.

### How to read the cost class

The project's three classes, plus two the catalogue adds because the existing vocabulary
hid the largest category:

| class | meaning | who pays |
|---|---|---|
| **free** | re-analysis of row data we already hold in `data/block_*/` | us, hours |
| **free (them)** | already computed upstream, sitting in a file that was never zipped | them, minutes |
| **free\*** | new measurement on *deposited* structures — no inference, but real labour and a download | us, days |
| **cheap** | re-scoring existing predictions, no new inference | them, hours |
| **real** | new predictions | GPU |

**Accounting unit:** one *cell* = one (receptor × backbone × arm) at 50 predictions
(5 seeds × 10 samples), the Block B grid. One arm on the 40-receptor Class A panel across
4 backbones = 8,000 predictions; on the 64-receptor both-state census = 12,800.

### How to read the novelty verdict

Graded against `lit/INDEX.md`, audited by the lit session 2026-09-11. `DONE` means **do
not claim it**. `ADJACENT` means the idea exists but not this crossing. `OPEN` means the
corpus records the absence.

Two counting rules the catalogue imposes on itself, both worth carrying forward:

- **"Zero of 81" is banned as a denominator.** `input_factor_design` is populated on 11 of
  81 notes, so "zero of 81" was really "zero of the 11 where anyone looked". Every absence
  claim must be stated as *"zero of the N papers that could hold it"*, with N derived from
  a tag that is actually exercised. For ligand × partner, N = **7**.
- **Co-occurrence of two tags is a candidate list, not a crossing.** `vo2026fiducials`
  carries `msa-subsample`, `ligand-driven` and `partner-driven` together and crosses none
  of them.

**38 of the 45 headings carry a `Novelty` bullet** (`grep -c '^- \*\*Novelty'
redo/spec/CATALOGUE.md` → 38). Seven carry none: **E4.3, E6.1, E6.2/E6.3, E6.4, E7.5,
E9.1, E9.3** — all of them infrastructure, conventions or panel decisions rather than
claims.

---

## Group 0 — the instrument

**What it is for.** Everything the paper says is a rate, and every rate is produced by one
two-distance predicate: a structure is ACTIVE when d(Y5.58-OH, Y7.53-OH) < 9.08 Å **and**
d(2×46 Cα, 6×37 Cα) > 14.932 Å. Group 0 asks whether that ruler is trustworthy. Its
central problem is circularity — the thresholds were fitted on the same GPCRdb
Active/Inactive annotations the predicate is then used to grade, which is the first
methodological objection a referee makes (`methods.tex:95`). E0.1 breaks the circle by
refitting on 726 structures the panel does not contain; E0.2 checks the geometric rule
against an independent learned coordinate; E0.3 asks whether a binary predicate is the
right shape at all; E0.4 demotes the threshold from a fact to a reported choice. **All five
E0 entries are `BLOCKED` on the measurement pass (`PLAN.md` Pillar 1), which does not start
without Aditya's word**, and everything downstream that reports a rate is graded by
whatever this group concludes. E0.5 is closed: Aditya dropped classes B and F on
2026-09-12 (`DECISIONS.md` D-2026-09-12-d), on measured grounds — a 9 Å inter-backbone
disagreement on class B and no discriminating power at all on class F.

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E0.1** | Recalibrate the predicate on the off-panel Class A population | Where do the two thresholds sit when fitted on structures the panel does not contain? | `free*` (~726 downloads, days not hours) | Nothing. **Everything else that reports a rate depends on it.** | `paajanen2026activation` **DONE** at scale (1,351 structures, learned PC1, GMM threshold −1.72 ± 0.44) but **not reimplementable** — no weight vector, no residue list, no repository. `khaleq2026hyaline` **DONE** as a supervised classifier (1,590 structures, AuROC 0.99) but its threshold is unreported and it has never been run on a *predicted* structure. Our claim is a *reimplementable, per-axis, off-panel-calibrated* predicate, not a new idea. |
| **E0.2** | Concordance against an independent state index | Where does a two-distance geometric rule disagree with a learned coordinate, and on what kind of structure? | `free*`, rides on E0.1's pass | **E0.1** | **ADJACENT.** The indices exist; the cross-validation does not. Scope limit: `paajanen2026activation` **excluded arrestins and intermediates**, so option (c) cannot check E7.6's arrestin arm or E0.3's intermediates. |
| **E0.3** | Admit a third state | Should the predicate be binary at all? | `free*`, 21 structures, rides on E0.1 | (none stated) | **OPEN, small, honestly underpowered.** Both `georgiou2025heterogeneity` and `paajanen2026activation` describe intermediates; nobody scores them through a fixed predicate, and paajanen **declined to report** at exactly this n ("their number is too low to be distinguished from the graph", p.2). Pre-commit: *if ≥15 of 21 fall strictly between the two cuts, report a middle band; otherwise report scatter and make no three-state claim.* |
| **E0.4** | Report the axes continuously and the predicate as a derived call | How much of every result is threshold placement? | `free` on A and B today | (none stated) | **Not a novelty claim; a robustness one.** |
| **E0.5** | Decide the class B and class F instrument | Is there a predicate for these, or are they scope decoration? | (a) free, (b) `free*` | (none stated) | No verdict stated. `hilger2020gcgr` supplies the biology — in class B agonist alone produces no TM6 opening — which makes class B the *sharpest* venue for a length ladder (E7.2) and argues against dropping it. **CLOSED 2026-09-12 at option (a): drop B and F. Registry status `DROPPED`, verdict `DIES` as an experiment, `SURVIVES` as one Methods sentence. Guarded by `g0_preflight.py` check G0-13.** |

---

## Group 1 — partner length: the centrepiece

**What it is for.** This is the group that answers the paper's first title clause, and
E1.1 is the only experiment in the catalogue that answers it outright. Every block to date
supplied either nothing or a complete Gα subunit; nobody has asked *how much of the
transducer the models actually need*. Group 1 builds a nested ladder from apo through an
11-mer, a 21-mer, the α5 helix, α5+β6, an α5-deleted full subunit and the full cognate Gα,
then attacks it from every side: a mass-matched non-Gα bulk control (E1.2), scrambled and
composition-matched peptides (E1.3), a family swap (E1.4), a per-position alanine scan
(E1.5), a one-residue natural pair (E1.6), heterotrimer versus Gα alone (E1.7), uncoupling
point mutants (E1.8), and partner-MSA on/off (E1.9). **It is also the only group whose
systems are fully enumerated in `redo/inputs/` — all nine entries have rows in
`g1_systems.csv`** — and the only group `PLAN.md` schedules wholesale (Pillar 3).

Two specification warnings that apply across the group:

- **Never express a rung as a fixed residue range.** `analysis/block_b/DATA_REQUESTS.md:221`
  and `rebuttals/BLOCK_B.md:479` both specify "Gα residues 334–354". That is the C-terminal
  21 **only for Gi1**; for Gs (GNAS, 394 aa) it ends 40 residues short. The spec must read
  *"the last N residues of the cognate subunit"* or four of five classes are built wrong.
- **The ladder crosses a placement-accuracy boundary between R4 (~45 aa) and R5/R6
  (350–394 aa).** `junker2026peptidedesign` stratified at 50 residues and found
  "35.5% of Boltz-2-predicted GPCR–protein ligand complexes achieve a DockQ score below
  0.23" (p5). A graded response to length could be a placement artefact. The engagement-depth
  column is the mitigation and is **required for interpretation**, not merely carried.

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E1.1** | The α5-CT length ladder | How much of the transducer do the models need? Is the response to length graded or a step? | `real` — **40,000** (5 rungs × 40 rec × 4 bb × 50); 64,000 on the 64-rec census; **10,000** single-backbone pilot | E0.1 for the threshold; nothing else. Dispatchable before calibration if axes ship continuously. | **OPEN, and the safest novelty claim available.** **Four independent recorded absences:** `ye2026multistatebias` ("No truncated, decoy or scrambled partner is run", p.18); `chiesa2025templatebias`; `heo2022multistate` ("ligand, nanobody, G-protein and arrestin are never used as inputs"); `miglionico2026atlas`, the largest partner-supplying study in the corpus (10,413 pairs, 801 receptors), whose note states the absence explicitly (pp19–20). |
| **E1.2** | Bulk control, crossed at two rungs | Is the 55% occupancy term specificity or literal occupancy? | `real` — **16,000** (2 arms); **2,000** pilot | **E4.2 — CORRECTED**; this row previously said "Nothing". Without stratifying each receptor by its deposited active:inactive ratio a null is uninterpretable. | **OPEN for protein partners.** No paper runs a scrambled or decoy *protein* partner. The **ligand analogue is DONE and is the threat**: `yu2026domainmotion` (nonbinders reproduce the motion; pLDDT does not separate them), `masters2025physics`, `bret2025boltz2docking`. E1.2 therefore tests whether yu's finding extends to protein co-inputs. |
| **E1.3** | Composition- and order-matched controls at peptide length | At peptide length, where nothing but the tail is left, does sequence identity finally matter? | `real` — **32,000** (4 new arms); **8,000** on one backbone | E1.1 R2 existing (dispatchable together) | **OPEN.** Nearest `tran2026nanogs`: "ABSENT — scrambled-sequence peptide … none scrambles the sequence while preserving length and charge." Converts Block B's decoy arm from confounded to decisive — in Block B the scramble sat on the tail of a 354-residue subunit, so 97% of the partner was unchanged. |
| **E1.4** | Family swap at peptide length | Block B found the models nearly blind to partner family (+0.082 of a 0.733 rise). Is that blindness real, or is it bulk drowning the signal? | `real` — **8,000** (1 swap arm) | E1.1 R2 | **ADJACENT** to Block B's own shuffled arm, **OPEN** against the corpus as a prediction experiment. Has a wet-lab twin: `miglionico2026atlas` ran 11 Gαq chimeras with swapped Gα C-termini, with a ΔC control, QRFPR r = 0.66, P = 0.026. **Cite the chimeras as biology, never as precedent for a truncated co-input** — all 10,413 of its predictions used the full heterotrimer. |
| **E1.5** | Per-position scan inside the supplied α5-CT | Which residues carry the effect, and does the model's answer match the structural biology? | `real` but scalable — **4,200** (21 arms × 10 rec × 1 bb × 20 samples) | E1.1 (a length must be chosen first), plus the retrieval confound that constrains *which* length | **OPEN.** `/deep mutational\|saturation mutagenesis\|mutational scan/` returns **0 of 81**; `/alanine scan/` returns 1 (`hilger2020gcgr`, wet lab); `/per-position/` returns 5, none on a partner. Protocol to copy: `waymentsteele2024cluster` (8-point scan, **no MSA**, three mutations flip the predicted state). **Must run at peptide length** — `masters2025physics` p.9: a mutated sequence retrieves the wild-type MSA and template, so a null would be a retrieval artefact. |
| **E1.6** | The Gi/Gt single-residue natural pair | Is the instrument sensitive to one residue? | `real`, 1 arm — **8,000**; 2,000 on one backbone | (none stated) | **OPEN**; a sensitivity floor for E1.5 rather than a headline. Gi `IKNNLKDCGLF` vs Gt `IKENLKDCGLF` differ at one position. |
| **E1.7** | Gα alone versus heterotrimer | Every block supplies Gα alone; the deposited active references are heterotrimers. Does adding Gβγ change predicted state, or only the interface? | `real`, 1 arm — **8,000**. **Requires a three-chain input schema** — a harness change, not only a dispatch | (none stated) | **ADJACENT.** `ye2026multistatebias` and `mitjavila2026afsample2t` both supply heterotrimers; neither contrasts them against Gα alone. |
| **E1.8** | Uncoupling point-mutant Gα arms | Does a full subunit that cannot couple still open TM6? | `real`, small — **2,000** (2 arms × 5 Gs receptors) | (none stated) | **OPEN.** The partner-side analogue of `masters2025physics` and `bret2025boltz2docking`, and a sharper control than the scramble because the mutation is biologically motivated. Both reagents (`alphas_F376A_L388A_mutant`, `alphas_F376A_L388A_R380A_triple_null`, 394 aa) already exist in the pipeline's `partners.fasta`, consumed by zero rows. |
| **E1.9** | Coevolution versus sterics: partner MSA on and off | Does the partner's effect survive when the model has no alignment for it? | `real`, 2 arms — **16,000**; 4,000 on one backbone | (none stated) | **ADJACENT.** The MSA-mechanism debate is mature but entirely about the *receptor's* alignment (`waymentsteele2025reply`, `lee2025seqassoc`, `xing2025purified`, `feldman2026alphainterp`). **Nobody asks it of a protein partner.** **Not to be confused with Group 8** — this varies *pairing* on the partner chain, binary, at two rungs; Group 8 varies the *depth of the receptor's own alignment*. |

---

## Group 2 — the ligand axis

**What it is for.** The paper's second title clause says the agonist alone does not drive
the active state. Group 2 is the only group that can speak to it. Its situation is awkward:
Block C ran 40,800 predictions bearing on this and shipped a 16-column census with **no
state column**, so E2.1 and E2.4 are "already answered upstream, just not exported". E2.2
is the experiment the paper actually needs — the honest 2×2 of ligand presence × partner
presence on one panel with one scorer — and the catalogue's own judgement is that
**re-running it clean is the honest option**, because Block B and Block C used different
scorers, panels and reference sets. E2.3 extends the ligand axis to pharmacological
efficacy and is bottlenecked on curation, not compute.

**The C7 trap.** `CLAUDE.md` records that all 40,800 rows of `rows.tier3.v2.csv` carry a
ligand — "apo" there means *no partner*, not *no ligand* — so the agonist *alone* was never
predicted (`DECISIONS.md` F-23). What Block C measured is agonist versus neutral antagonist
at a fixed partner condition, which is real but is not the title clause.

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E2.1** | Export the state call on Block C's existing predictions | What does the predicate say on 7,000 apo × agonist and 7,000 cognate × agonist predictions? | **`free (them)`** — the predictions are scored, the file is SHA-pinned in twenty places | **An instruction, not data.** Block C's dispatch forbids connecting the block to two-state generation; Flag C-3 forbids quoting a binary rate for a ligand-class discrimination claim. Clause 2 is neither. Somebody upstream has to rule. | **ADJACENT, not open.** `ye2026multistatebias` already reports small molecules move predicted state weakly and inconsistently (β2AR, n=1); `vo2026fiducials` reports the opposite experimentally. **An "agonist alone does not" sentence is a confirmation at scale, not a discovery, and must cite both.** |
| **E2.2** | The real 2×2: ligand presence × partner presence | Do the two inputs compose? Additively, redundantly, or synergistically? | `real` if re-run — **22,400** (4 cells × 28 rec × 4 bb × 50). Potentially `free (them)`, but **re-running clean is the honest option** | (none stated) | **OPEN, on a real denominator.** **Exactly 7 of 81 notes carry both `ligand-driven` and `partner-driven`, and none of the seven crosses them.** Strongest ADJACENT is `ku2026promise` — both co-input types against five models, each present/absent, but kept in **separate non-overlapping sets** with different success criteria. **`suzuki2026conforflux`'s non-additivity sentence is about two algorithmic hyperparameters, not two biological co-inputs** — citation corrected in the catalogue. |
| **E2.3** | Efficacy ladder | Is the pocket response graded with pharmacological efficacy, or binary? | `real` — **11,200** (2 new roles × 28 rec × 4 bb × 50), plus curation of inverse- and partial-agonist ligands, which is the harder half | (none stated) | **OPEN.** No paper varies pharmacological class across a GPCR panel and calls state with a fixed predicate. Nearest in kind `kohlhoff2014gpcr` (MD, one receptor). Expectation from `georgiou2025heterogeneity`: inverse → S1/S2, partial → I2, full agonist shifts toward active but does not reach it alone (p.21). **Registry verdict `DIES` for this campaign; triage `NEEDS_PI_DECISION`.** |
| **E2.4** | The agonist-versus-decoy-ligand result | Does a ligand known not to bind reproduce the conformational change? | **`free (them)`** | (none stated) | **The question is DONE and is the sharpest published challenge to this paper.** `yu2026domainmotion`: 82 enzymes, 500 AF3 models per condition, no templates — nonbinders reproduce the motion, the training prior (40.3 pp) is 3–4× the ligand effect (9.1–17.5 pp), pLDDT does not discriminate. **Block C ran 14,400 `decoy_lig` predictions and reports nothing on them.** A referee who knows that paper will ask for exactly this arm. `yu2026domainmotion` is still not in `CLAIMS.md`'s threats table. |

---

## Group 3 — confidence

**What it is for.** The paper's third title clause says model confidence does not track
state correctness. Group 3's job is to make that claim survive contact with a literature in
which it is already well established — the catalogue's blunt verdict is that the headline is
**DONE many times over** and must be framed as confirmation on a new axis, not discovery.
What is genuinely unreported sits in the details: the re-aggregation finding (a confidence
metric changing sign between whole-complex and anchor grain), the operational half (does
picking the top-confidence seed beat picking at random), and the partner-chain question —
does the model's confidence in the peptide *it was handed* predict whether the receptor
opened. All three are `free` on rows already in hand.

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E3.1** | Restate the confidence result arm- and receptor-conditionally | Does confidence track *which structure is right*, or only *which receptor is easy*? | `free`, on 9,490 Block A rows | (none stated) | **DONE many times over** — `bryant2024cfold`, `ye2026multistatebias`, `sun2026kinconfbench` (wrong-state structure ranked first in >11% of cases), `schafer2025confounds`, `junker2026peptidedesign`, `yu2026domainmotion`, `ku2026promise`, `kalakoti2025afsample2`. **Frame clause 3 as confirmation.** Genuinely unreported: the re-aggregation finding — Protenix2 +0.33 → +0.07, OpenFold3 −0.26 → −0.63. |
| **E3.2** | The operational test | If you must pick one structure, does picking the highest-confidence seed beat picking at random? | `free` | (none stated) | **ADJACENT** — `ku2026promise` runs confidence-ranked vs uniform-random top-k at matched budget and reaches the same verdict. Cite its numbers: AF3 0.15 vs 0.17 (intrinsic), 0.49 vs 0.48 (ligand); BioEmu 0.18 vs 0.18. **Our +1.1 pp and ku's ≈0 agree**, making our result a replication. Already computed: +1.1 pp overall, sign flipping −3.1 to +4.9 across backbones, and **300 of 319 cells seed-unanimous** (only 19 of 319, 6.0%, show any seed-to-seed disagreement). |
| **E3.3** | Confidence on the supplied partner chain | Does the model's confidence in the *peptide it was handed* predict whether the receptor opened? | `free` on Block A; a **required column** on any new peptide arm | (none stated) | **CORRECTED.** The first version claimed nobody had asked it of a protein partner — false. `miglionico2026atlas` reports **per-residue pLDDT at Gα position H5.11, ROC AUC 0.762** (p5), and **hard-protects the 7 C-terminal Gα residues** from its own pLDDT<70 filter. What survives is sharper: **nobody has asked it of a protein partner against a receptor conformational-state outcome** — and there is now **a published number to beat, AUC 0.762 for coupling.** |

---

## Group 4 — memorisation and generalisation

**What it is for.** The largest single threat to the paper is that the models are recalling
deposited active-state structures rather than responding to the co-input. The Methods
already concedes it: **35 of 43 dated panel active references (81%) predate Boltz-2's
2023-06-01 cutoff** (`methods.tex:222–246`). Group 4 is the defence. E4.1 builds a
date-stratified holdout from receptors whose active state is post-cutoff; E4.2 correlates
per-receptor effect size against training exposure; E4.3 makes the anti-memorisation
argument *by construction* for the peptide arm; E4.4 asks whether "no backbone steers
inactive" is a property of the models or of what they memorised. The catalogue's verdict on
E4.1 is worth repeating: **"Not doing it is what would be unusual."**

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E4.1** | A date-stratified holdout panel | Does the co-input effect hold on receptors whose active state the models could not have seen? | `real` — **7,200** at 3 rungs (12 rec × 4 bb × 3 × 50) | **Per-backbone cutoffs.** Boltz-2 2023-06-01, Protenix 2021-09-30, Chai-1 2021-01-12 (**but Chai-1 also trains on AlphaFoldDB — do not write "saw nothing after January 2021"**), OpenFold3 **undated and still an open ask** | The **design is DONE** and well established — `skrinjar2026generalization` (8–25% success in the least-similar stratum vs 81–89% in the most similar), `swapna2025memorization`, `kim2026mac1`, `chiesa2025templatebias`. **Not doing it is what would be unusual.** Set: 12 both-state Class A receptors whose earliest active entry is post-cutoff; **5 entirely post-cutoff** (`ada1a ccr8 cxcr3 gpr6 mchr1`), four of them off our panel. |
| **E4.2** | Training exposure against effect size | Is per-receptor ladder height correlated with that receptor's training-set exposure? | `free` — Block B rows plus the GPCRdb snapshot, both in hand. **`deposition_count` in the Block B covariates is constant and its regression ships NaN**, so the exposure variable must be rebuilt from the snapshot | (none stated) | **ADJACENT.** Nearest `yu2026domainmotion`, which quantifies the enzyme version at 40.3 pp. `ye2026multistatebias` notes a 10:1 state ratio as a contributor. |
| **E4.3** | The wild-type 21-mer as an unseen input | Can the peptide arm be argued prospective by construction? | `free` to establish (a search over the deposited set); rides on E1.1 to use | (none stated) | *(no Novelty bullet)* — **4X1H is the only peptide-bound entry among the 80 references**; its chain C is an **11-mer** `VLEDLKSCGLF` differing from native bovine Gαt1 `IKENLKDCGLF` at **four of eleven** positions — an engineered high-affinity analogue. **No wild-type 21-mer α5-CT appears with a receptor in any deposited structure.** That is a quantitative anti-memorisation argument and the best single reason to run the 21-mer before the 11-mer. **Do not** cite 4X1H as precedent or score a 21-mer against it. |
| **E4.4** | A post-cutoff inactive-state binder | Is "no backbone steers inactive" a property of the models or of what they have memorised? | `real`, **~600–2,000** | **Finding a candidate.** The earlier search was closed rather than answered; it disqualified four, three because a 141-residue "nanobody" was an anti-BRIL cryo-EM fiducial. That filter rule is reusable. | **OPEN.** The `nanobody` tag fires on three corpus papers and **none of them runs a predictor** (`georgiou2025heterogeneity` review, `hilger2020gcgr` cryo-EM/DEER, `tran2026nanogs` wet lab). **Prerequisite:** Block D's D2 ADRB2 arms fed the same sequence to both subarms — any re-run must verify chain B by SHA **before** dispatch. |

---

## Group 5 — mechanism

**What it is for.** Every other group reports *what* the models do. Group 5 is the only one
that asks *why*, and the paper currently has one mechanistic measurement at **n = 2
receptors**: α5 heavy atoms fall within 4 Å of where TM6 sits in the deposited **inactive**
structure on 52% and 39% of contacts, against 11% for the active structure and 2–4% for the
prediction's own TM6 — the partner cannot be placed without displacing TM6. E5.1 extends
that to the panel. E5.2 asks where in the pocket the signal lives (across all four blocks
the paper has **no residue-level account of anything**). E5.3 replaces a mean with an
ensemble. E5.4 converts a threshold argument into a dose–response. E5.5 looks for a rule
governing failure. **Four of the five cost nothing new.**

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E5.1** | Steric exclusion at panel scale | *Why* does the co-input work? | **`cheap`** — the predictions exist; the coordinates were not shipped (item 7 of `analysis/block_a/DATA_REQUESTS.md`) | (none stated) | **OPEN.** No paper in the corpus offers a steric account from coordinates for a partner-induced state change. At n=48 with the active-structure control quantified it becomes the mechanistic section the paper lacks. |
| **E5.2** | Per-Ballesteros–Weinstein decomposition | *Where* in the pocket, and at which residues, is the signal? | **`free (them)`** | (none stated) | Fills a hole rather than claiming ground. `s4_bw_decomposition.json` and `s4_bw_position_decomposition.json` are named in two Block C narrative reports and **neither ships**. Registry verdict: **`DIES` as an ask, `SURVIVES` as our own analysis.** |
| **E5.3** | Report the ensemble, not its mean | Does the partner *shift* the ensemble or *narrow* it? | `free` | (none stated) | **ADJACENT.** `ku2026promise` recovers all known states in only ~8–29% of clusters and traces the collapse to the structure module; `jung2026boltzperturb` reports vanilla Boltz-2 ligand RMSF < 2.3 Å across 180 samples. Bimodality is already visible in the binary result: 111 of 160 apo cells never fire, 108 of 159 cognate cells always fire. |
| **E5.4** | Dose–response on engagement depth | Replace a threshold argument with a dose–response one | `free` | (none stated) | **ADJACENT.** Dose ladders exist on MSA and steering knobs (`mitjavila2026afsample2t`, `kalakoti2025afsample2`, `jedryszek2026probing`) but **nobody titrates a biological co-input and reads a graded state response.** Combined with E1.1 this is the first co-input dose–response in the literature. The 20 Å α5-tip-to-R3.50 cutoff is ~4× the cognate median insertion depth of 12.19 Å and the drop's own C-B-6 flags it as permissive. |
| **E5.5** | What the failures have in common | Is there a rule for when the co-input fails? | `free` on A and B; needs Block D's rows for D | (none stated) | **DONE as a genre.** Nearest `skrinjar2026generalization`; value is internal. Regress failure against *published* correlates rather than inventing new ones. **Block C attempted the paralog-cluster version as a pre-registered applicability domain and it was refuted — the slope ran negative** — so this must be framed post-hoc unless pre-registered afresh. |

---

## Group 6 — the delivery contract

**What it is for.** Three of four campaigns are partly or wholly unverifiable: Block D
shipped **0 of 42,180** predictions, Block C shipped a 16-column census with no state, and
Block B ships **no boolean state column at all**. Group 6 exists to stop a fifth campaign
repeating that. E6.1 is a row-level contract agreed *before* the campaign runs — one tidy
table, one row per prediction, with a named column list and a list of defects banned by
contract. E6.2/E6.3 is the single highest-value item in the whole catalogue by
value-to-cost: shipping two already-computed files. E6.4 is free now and **impossible after
dispatch**. **None of this group is an experiment in the ordinary sense; it is the
precondition that makes the others recomputable.**

The contract's banned defects, verbatim from the catalogue, because each is a real observed
failure: self-certifying columns that can never fire (`flag_low_confidence` False on 40,000
rows; `passed` True on all of A, B and C); placeholder strings in place of nulls
(`reference_audit.csv`'s `method` and `resolution` on all 80 rows, both non-null so a null
check passes); all-NaN audit blocks (A1–A6 on 9,490 and 32,000 rows); CSVs with unquoted
commas (`tier_d3_panel.csv`); and **nominal levels standing in for measured quantities** —
`msa_depth_realised` must be the row count the backbone actually consumed. *A rung label is
a design fact; a depth is a measurement, and a regression needs the second.*

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E6.1** | A row-level delivery contract, agreed before the campaign runs | Will the redo be recomputable? | `free`, **and it is a precondition rather than an experiment** | (none stated) | *(no Novelty bullet)* — not a claim. **A fifth campaign that repeats the Block C/D delivery is not worth running.** |
| **E6.2 / E6.3** | Ship the three Block D `rows.csv` and `rows.tier3.v2.csv` | *(no Question bullet)* | **`free (them)`** | (none stated) | *(no Novelty bullet)* — between them these two files close **~18 of the 62 open asks** across the four request documents; Block D's own S1 puts it at "eleven of the twelve asks"; Block C's ask 1 says the one file closes asks 2, 6, 7, 8, 10 and 14 alongside itself. **Block D's verifier goes from 40 recomputed checks to something near 120. Nothing in the catalogue has a better ratio of value to cost.** *(Note: `CLAUDE.md` records both files have since landed — `rows.tier3.v2.csv` and Block D's three corpora at `analysis/block_d/received_2026_09_13/`.)* |
| **E6.4** | Pair seeds across arms | Can within-seed differences be read? | **free if specified before dispatch; impossible afterwards** | (none stated) | *(no Novelty bullet)* — Block A's seeds are not paired between arms. A ladder whose rungs share seeds supports a matched-pair analysis **at no extra compute** and materially tightens every interval. **Registry verdict: `SURVIVES`, blocking.** Blocks A and B both failed it: **1,898 distinct `seed_outer` over 380 cells**, so the same seed never ran both arms of a cell. |

---

## Group 7 — new directions

**What it is for.** Group 7 holds the entries that are not extensions of an existing arm:
the ones that change what kind of paper this is. E7.1 asks whether an inactive-directing
co-input exists at all — Block D found the inactive direction does not work but could not
distinguish "no backbone steers inactive" from "nothing in this setup could have steered
inactive". E7.2 takes the ladder to class B, where the biology says the partner matters
more. E7.3 is the only experiment in the catalogue whose design does not presuppose the
answer — run the predicate where no reference exists. E7.4 turns every null in the paper
from unfalsifiable into bounded, for free. E7.5 is a panel multiplier rather than an
experiment. E7.6 supplies a *positive* control the project has never had: a non-Gα
biological partner that should work, against a non-Gα non-biological partner that should
not.

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E7.1** | What would an inactive-directing co-input even be? | The active direction has a natural co-input. Does the inactive direction have one at all? | **free to write; `real` to test** | (none stated) | **OPEN, per E4.4.** Candidates honestly ranked: (a) a post-cutoff inactive-state nanobody — the only clean one, and it may not exist; (b) an inverse agonist — the right handle, weak in these models; (c) a Gα α5 mutant that binds without opening — speculative; (d) the *absence* of a partner, which is the apo arm and is not a control. **Being unable to name a good one is itself a result** and belongs in the Discussion. |
| **E7.2** | Cross-class transfer: the class B ladder | Does partner length behave the same way where the biology says the partner matters *more*? | `free*` for the predicate, then `real` — **6,400** (8 rec × 4 bb × 4 rungs × 50) | **E0.5**, which closed at "drop B and F" | **ADJACENT on coverage** (`heo2022multistate`, `chib2025gpcrstates`, `khaleq2026hyaline`) but **OPEN as transfer**: no paper tests class transfer *as* transfer with a held-out class. **PARKED 2026-09-12, not killed.** `hilger2020gcgr` on GCGR: "TM6 activation is only triggered by the engagement of the α5 helix of Gαs", and agonist alone produces no TM6 opening at all — so **class B should show a larger step**. Needs a calibrated class B instrument first, which is a second paper's work. |
| **E7.3** | A prospective arm on receptors with no solved active state | The whole argument for an intrinsic predicate is that it runs where no reference exists. Have we ever run it there? | `real` — **5,400** (9 rec × 4 bb × 3 rungs × 50) | (none stated) | **The closest thing to prospectivity available.** Of 78 papers **exactly three report an unqualified prospective result and none is of the relevant kind** — `tran2026nanogs` (wet lab, no structures), `wallner2023afsample` (blind CASP, no conformational state), `ingraham2023chroma` (de novo design). Even `richman2025conformix` scores coverage against deposited references. Set: **9 Class A receptors with inactive structures only** — `acm5 ada1b ada2c ccr7 ccr9 gnrhr lgr4 ox1r q9wtk1`. **Honest limit: nobody can grade it.** Pair it with a falsifiable pre-registration or it is decoration. |
| **E7.4** | Estimate the interaction, with power stated in advance | Not "do the inputs compose" but "could we have detected it if they did?" | `free` once one row-level ligand table exists | (none stated) | **Not novel; load-bearing.** `suzuki2026conforflux` is the only corpus paper to attempt an interaction term between two factors and reports it **cannot resolve non-additivity** at n=10 and ~0.6 Å SE. Block C's null on the applicability domain has the same shape: a null nobody can size. **This is the cheapest way to stop the paper's negatives from being unanswerable.** |
| **E7.5** | Extend the panel to the Class A both-state census | Is the panel a census or a sample? | `real` **multiplier** — every arm becomes 12,800 instead of 8,000, a **1.6× uplift on everything.** Adopt only for arms whose conclusions depend on power | (none stated) | *(no Novelty bullet)* — adds the 24 off-panel Class A both-state receptors to reach **64 of 64 slugs**, a complete census. Fixes three weaknesses at once: Gs-coupled receptors rise from 5 (powering E1.4 and E1.8); Block B's collapsed Gs→Gq (n=3) and Gi→Gs (n=0) strata gain members; four of five entirely-post-cutoff receptors join the panel. A 64-slug census contains **45 of ConfoRNets' 51** test cases. **Known panel defects to fix while extending: `B1B1U5` is a jumping-spider opsin and `OPSD` is bovine — no sentence may call this panel human.** Registry verdict: **`DIES` as a uniform multiplier, `SURVIVES` as one replication arm.** |
| **E7.6** | A second biological co-input at peptide length: the arrestin finger loop | Is the effect about the α5 specifically, or about *any* cognate intracellular partner element? | `real`, 1–2 arms — **8,000–16,000**; 2,000 on one backbone | (none stated) | **OPEN, supporting sentence CORRECTED.** Arrestin appears in **7 notes**, not one; **none supplies arrestin to a predictor**, so OPEN holds. Cite `heo2022multistate`'s recorded absence rather than the review. `khaleq2026hyaline` already counts arrestin-coupled structures as active in its label rule, supporting the premise. **Circularity check first:** if any arrestin-coupled structure defines "active" in **our own** reference set, this arm is partly circular — a free check against `data/block_b/09_references/reference_audit.csv`. **And E0.2's option (c) cannot check it**, because paajanen excluded arrestins. Falsifiable prediction: the finger loop **moves the NPxxY axis more than the tilt axis**. |

---

## Group 8 — MSA depth as a crossed factor

**What it is for.** Depth was varied in Block D and appeared nowhere in the first draft of
the catalogue. Group 8 closes that. It is *not* E1.9 (which varies **pairing** on the
partner chain, binary) and not E5.4 (physical insertion depth): Group 8 varies the **depth
of the receptor's own alignment** and crosses it with a co-input. The competing explanation
the whole paper must defeat is "the models call the receptor active because the alignment
was starved, not because a partner is present", and Group 8 is where that is measured
directly. The group's non-obvious design choice: **do not cross depth with apo and cognate**
— both endpoints are pinned (apo at 0.158, cognate at 0.891) and Block C is the cautionary
case of a campaign whose predicate saturated mid-flight. Cross depth with the **middle
rungs**, where the response has headroom in both directions.

**What Block D actually did (D3):** 26 Class A receptors × 4 backbones × 5 depths
(8, 32, 128, 512, full) × 5 seeds × 10 samples = 26,000 dispatched, **25,810 landed**
(190 rows lost, 0.73%, non-uniform). **Apo only** — no partner at any depth, no ligand at
any depth. FSHR and LSHR were dropped as "compute-heavy glycoprotein-hormone big complexes",
which is a hardware decision, not a scientific one, and it matters for Group 9.

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E8.1** | Cross depth with partner, in the middle of the ladder | Does a physical co-input **rescue** what removing the alignment took away? Do depth and partner act on the same mechanism or on different ones? | `real` **(the catalogue states no class token for this entry — the only one of the 45)**. Sizes: full three-way 2,080 cells; depth × partner all depths 1,040 cells; 3 depths 624 cells / 31,200; **2 depths (full/8), 1 backbone, 104 cells → ~2,600 new. Run this version first.** | **E8.3 first — the anchor must be fixed or the top rung is undefined.** Also E1.1 if the middle rungs are used; the cognate-level version can run alone | **OPEN.** Of 81 papers, **exactly one crosses an MSA manipulation with a co-input inside a single model** — `mitjavila2026afsample2t` (column masking 0/10/20/30% × partner presence, 250 models per cell, **no ligand channel at all**). `cheng2026af3cluster` combines MSA clustering with co-folded binders but does not cross them. **The result to engage: `xing2025purified` — "the successful sampling of alternative states depends not on MSA depth but on sequence purity" (p.3).** *Caution: if `cheng2026af3cluster`'s PDF is read and `factors-crossed` lands, "exactly one" becomes "two".* |
| **E8.2** | Cross depth with ligand, at fixed partner condition | A ligand and a protein partner are not interchangeable co-inputs, and the corpus says so | `real` — **26,000** (5 depths × 1 new ligand arm × 26 rec × 4 bb × 50); **2,600** at 2 depths on 1 backbone | **E8.3**; plus Block C ligand curation (35 of 36 receptors have a usable agonist; HRH3 lacks the role entirely) | **OPEN**, same evidence as E8.1. `lazou2026cryptic` varies the ligand with the MSA held constant; `jung2026boltzperturb` varies the representation with the ligand held constant. **They bracket the question from opposite sides and neither crosses it.** Falsifiable hypothesis from `ye2026multistatebias` (p.2): **a partner rescues depth loss and a ligand does not.** If the ligand *does* rescue, that asymmetry does not survive on an AF3-lineage panel at scale — a more interesting result than the expected one. |
| **E8.3** | Fix the depth anchor before any depth work. **Blocking.** | *(no Question bullet)* | `free (them)` for (i), (ii), (iv); `real` but trivial for (iii) — **~500 predictions** | (none stated) | **None; it is a prerequisite.** Closes Block D's open Q8 and caveat C-D-8. **The problem:** on OPSD × Boltz-2, D1 reports 38.8% at n=500 and D3's *full-depth rung* reports 10.0% at n=50 — a **28.8-point, ~3σ gap**. Block B's apo arm is an independent third measurement: **D1's point estimate falls inside Block B's 95% Wilson interval on 26 of 28 cells**, so Block B reproduces D1 and the undersampling explanation is not supported (observing 5 of 50 against a true 0.388 is a ~3.7σ draw, p ≈ 5 × 10⁻⁴). **The surviving reading is an upstream difference between D3's `full` rung and the default apo condition — which is worse for depth work than undersampling would have been.** `CAMPAIGN.md` adds a second mechanism: `subsample_msa.py:106-107` returns the input unchanged when `len(entries) <= depth` while the manifest still records the nominal depth, so a "512" arm on a 300-row alignment is a 300-row arm labelled 512. **And the slope refit is not cosmetic:** the four headline slopes reproduce only under `ln(depth)` with `full` **imputed as 4,096**, while Block B's MSA audit shows Boltz consuming **13,678 alignment rows** for one ADRB1 cell — an x-axis whose highest point is wrong by more than an e-fold. |

---

## Group 9 — the deep-apo floor

**What it is for.** The four backbones do not share a baseline. On β₂AR apo, Chai-1 calls
100% of 500 samples active and Boltz-2 calls 0%. **Every ladder rung is measured against a
different floor per backbone, so a rung at 40% means opposite things on two of them** — and
pooling across backbones is exactly what produced the withdrawn "spontaneous apo
bistability" claim, a 50% average over two backbones that disagreed completely. Group 9
turns the floor from a baseline to be subtracted silently into a reported result, decides
where deeper sampling actually buys anything, and fixes a reporting convention. **Two of its
three entries are `free` and largely already computed.**

**The floor, recomputed from `data/block_b/01_rows/rows_tidy.csv`, 160 apo cells
(40 Class A × 4 backbones):** 16 cells have the NPxxY axis undefined; **91 are pinned at 0**
(never fire on any of 50); **9 are pinned at 1**; **44 are mixed** — and of the 44, **24 sit
between 0.10 and 0.90** while 20 sit at ≤0.08. *The information is in ~24 cells and the
variance risk is in 20 more; the other 100 need no deeper sampling at all.*

**Two campaigns agree on the floor.** Block A (Class A, NPxxY-defined) gives Boltz 13.6%,
Chai 31.9%, OF3 11.0%, Protenix 7.7%; Block B's apo arm gives 12.7 / 32.3 / 11.0 / 7.2 —
**within 0.9 points on every backbone.**

| id | title | question | cost | depends on | novelty |
|---|---|---|---|---|---|
| **E9.1** | Characterise the floor from data already held. **free.** | Which receptor × backbone apo cells carry information, and which are pinned? | **`free`**, and most of it is already done | (none stated) | *(no Novelty bullet)* — **The receptor the existing panels miss: FSHR is mixed on all four backbones** (Protenix 0.92, Boltz 0.90, Chai 0.72, OF3 0.30) — the only panel receptor intermediate *everywhere* rather than backbone-split. It is in neither D1's 7 nor D3's 26, dropped as a "compute-heavy glycoprotein-hormone big complex". **The single most informative receptor for a deep-apo arm was excluded for hardware reasons.** This entry supplies input to `PANEL.md` and `RUN_MATRIX.md` and decides neither. |
| **E9.2** | Deep apo sampling, targeted rather than uniform | At what n is an apo cell's rate stable, and does the ladder's bottom rung need a different sampling budget from its other rungs? | `real`, and **targeting is most of the value**: all 160 cells 80,000 @500 / 32,000 @200; **the 44 mixed cells 22,000 @500 / 8,800 @200; the 24 informative cells 12,000 @500 / 4,800 @200.** Uniform deep sampling costs **6.7×** the targeted version and buys nothing on 100 pinned cells | **E9.1** for selection; **E0.1**, because recalibrating thresholds moves which cells are pinned — **run the selection after calibration, not before** | **ADJACENT.** Corpus sampling budgets run from 5 (`wohlwend2024boltz1`, `zhang2026generalization`) to 6,000 (`wallner2023afsample`), with 500 per condition common. What is unusual is spending them **asymmetrically by measured cell variance rather than uniformly**, and saying so. At n=50 a binomial on an intermediate cell has SE ~7 points — **the width of an entire ladder step.** |
| **E9.3** | Report every rung against its own backbone's floor. **free.** | An analysis convention, not an experiment, and it changes what the results mean | **`free`** | (none stated) | *(no Novelty bullet)* — report each rung as a shift from that backbone's own apo floor as well as an absolute rate, and **never pool a rate across backbones.** Block D already established the rule after pooling produced a withdrawn finding. **What it also fixes: it makes Chai-1 legible.** Chai-1 is the "soft predictor" on every Block A metric partly because its floor is 2–4× every other backbone's (31.9% against 7.2–13.6%), so it has the least headroom to rise. |

---

## Cross-reference: what `PLAN.md` actually schedules

### The mechanism of the join

`PLAN.md` is an **ordering** document organised as **six pillars (Pillar 0 through Pillar
5)** plus a separate ten-step route table in §0a. Its pillar sections name almost no
experiment ids, so the join to the catalogue is hand-authored in
`redo/build/run_registry.py` and materialised as the `pillar` column of
`redo/inputs/run_registry.tsv` (sha256 `a275c4dd…`, stamped in `inputs/MANIFEST.tsv`).

```
python3 /path/to/xref.py       # classifies each of the 45 by registry pillar and catalogue cost class
```

| pillar | what it is | experiments it discharges | count |
|---|---|---|---:|
| **Pillar 0** | Free. Nothing below starts before this. | E2.1, E6.1, E8.3 | **3** |
| **Pillar 1** | The instrument. CPU only, no GPU. The measurement pass: 726 calibration + 610 application + 98 pinned reference rows | E0.1, E0.2 | **2** |
| **Pillar 2** | The defence. Apo, monomer, four backbones. MSA-manipulation controls | **none** | **0** |
| **Pillar 3** | The main claim. The ladder, with G17 as a blocking companion | E1.1, E1.2, E1.3, E1.4, E1.5, E1.6, E1.7, E1.8, E1.9 | **9** |
| **Pillar 4** | The ligand. Partner held, ligand swapped. **This is title clause C7** | E2.2, E2.4 | **2** |
| **Pillar 5** | The SI: peptide tiers T2/T3, the decoy-refusal finding, the date-stratified holdout | E4.1 | **1** |
| | | **TOTAL SCHEDULED** | **17** |

**Pillar 2 discharges no catalogued experiment at all.** `PLAN.md` records this itself: its
arms come from `MSA_SUBSAMPLING_REGIMES.md`, whose **Stage 1 (2,720 predictions — that
document's own top recommendation) carries no E-id**. Either Stage 1 gets an id or the
catalogue is missing the experiment it is.

### The headline split

| | count | ids |
|---|---:|---|
| **Scheduled** (registry `pillar` ≠ none) | **17** | E0.1 E0.2 E1.1–E1.9 E2.1 E2.2 E2.4 E4.1 E6.1 E8.3 |
| **Unscheduled** (`pillar` = none) | **28** | the rest |
| — of those, **costing no new inference** (`free` / `free*` / `free (them)` / `cheap`) | **18** | E0.3 E0.4 E0.5 E3.1 E3.2 E3.3 E4.2 E4.3 E5.1 E5.2 E5.3 E5.4 E5.5 E6.2 E6.4 E7.4 E9.1 E9.3 |
| — of those, **requiring new GPU inference** (`real`) | **8** | E2.3 E4.4 E7.3 E7.5 E7.6 E8.1 E8.2 E9.2 |
| — of those, **mixed** (a free half and a real half) | **2** | E7.1 (free to write, real to test), E7.2 (free* predicate then real) |

**Eighteen of the twenty-eight unscheduled experiments cost no new inference.** `PLAN.md`
itself lists eleven of them as omissions in its own §"Corrections from the registry triage":
E7.4 (which `RUN_MATRIX` §4.3 and `CAMPAIGN` §2.8 both say must **precede** the ligand arm),
E4.2 (a **hard predecessor** of the bulk control), E5.4, E9.1, E9.3, E0.4, E4.3, E3.3, E5.3,
E5.5, E7.1. And **E6.4 is in no pillar and is free now and impossible after Pillar 3
dispatches.**

### Cost class across all 45

```
python3 /path/to/xref.py   ->  real 19 | free 15 | free (them) 5 | free* 3 | cheap 1 | mixed free/real 2
```

| class | count | note |
|---|---:|---|
| `real` | **19** | all nine of Group 1, plus E2.2 E2.3 E4.1 E4.4 E7.3 E7.5 E7.6 E8.1 E8.2 E9.2 |
| `free` | **15** | |
| `free (them)` | **5** | E2.1 E2.4 E5.2 E6.2 E8.3 — the category that does not exist in the project's three-class vocabulary |
| `free*` | **3** | E0.1 E0.2 E0.3 — deposited-structure measurement, no inference |
| `cheap` | **1** | E5.1 |
| mixed | **2** | E7.1 E7.2 |

### Registry status, triage and campaign verdict

| column | distribution |
|---|---|
| `status` | `NOT_ENUMERATED` 27 · `ENUMERATED` 12 · `BLOCKED` 4 (E0.1 E0.2 E0.3 E0.4) · `PARKED` 1 (E7.2) · `DROPPED` 1 (E0.5) |
| `triage` | `COVERED_BY_PILLAR` 16 · `FREE_UNSCHEDULED` 11 · `NEEDS_PI_DECISION` 10 · `SUPERSEDED` 7 · `NEEDS_TRIAGE` 1 (E4.4) |
| `campaign_verdict` | `SURVIVES` 25 · `CHANGES` 16 · `DIES` 4 (E0.5 E2.3 E5.2 E7.5) |
| `named_in_run_matrix` | yes 30 · no 15 |
| `systems_enumerated` | yes 12 · no 33 |

### What is actually enumerated in `redo/inputs/`

Only **12 of the 45** have their systems enumerated to row level. Every count below was
re-derived from the CSVs and **all 12 reproduce the registry exactly**:

| id | arm(s) | rows | receptors | clusters | pooled predictions |
|---|---|---:|---:|---:|---:|
| E1.1 | `ladder`, `ladder_pilot`, `wetlab_length_series`, +9 more | 1,007 | 64 | 32 | 31,880 |
| E1.2 | `non_ga_bulk`, `a5null` | 180 | 30 | 29 | 7,200 |
| E1.3 | `composition_controls` | 300 | 30 | 29 | 4,680 |
| E1.4 | `family_swap` | 30 | 30 | 29 | 6,000 |
| E1.5 | `ala_scan`, `gi_to_gs_series` | 360 | 10 | 10 | 7,200 |
| E1.6 | `gi_gt_single_residue` | 30 | 30 | 29 | 6,000 |
| E1.7 | `heterotrimer` | 30 | 30 | 29 | 6,000 |
| E1.8 | `uncoupling_full`, `uncoupling_peptide` | 36 | 6 | 6 | 7,200 |
| E1.9 | `partner_msa_on` | 90 | 30 | 29 | 3,600 |
| E2.2 | `ligand_x_partner` ×5 variants, `blocked_ligand_identity` | 296 | 26 | 25 | 8,080 |
| E2.3 | `efficacy_ladder_inverse_agonist` | 6 | 3 | 3 | 240 |
| E2.4 | `decoy_third_role`, `…_full_subunit` | 48 | 16 | 15 | 396 |

**`g1_systems.csv`: 2,039 rows, 23 distinct arms, 74,960 pooled predictions.
`g2_systems.csv`: 350 rows, 9 distinct arms, 8,716 pooled predictions, 313 READY
(BLOCKED: 15 decoy-unavailable, 12 unresolved-uncurated, 8 unresolved-chain-no-sequence,
2 ligand-identity). Total enumerated: 83,676 pooled predictions** — against `PLAN.md`'s
first-pass route of **≈38,300**.

*Counting note:* 24 rows of `g1_systems.csv` carry the compound value `E1.8+E1.1` in the
`experiment` column. The registry counts a row into an experiment if the id appears
anywhere in that field, so those 24 rows are counted into **both** E1.1 (983 + 24 = 1,007)
and E1.8 (12 + 24 = 36). Under strict comma-splitting the counts are 983 and 12. Both are
defensible; the registry's semantics are the substring one, and they reproduce exactly.

### `RUN_MATRIX.md` — the other scheduling document

`RUN_MATRIX.md` §7.1 costs the run as **items** (P*, G*) and §7.3 as **Stage 0** (S0.1–S0.7).
Its items map to experiments as follows (from the registry's `staged_as` column):

| RUN_MATRIX item | experiment(s) | predictions |
|---|---|---:|
| S0.1 | E6.2 / E6.3 | free (them) |
| S0.2 | E0.1 | free* |
| S0.3 | E2.1, E2.4 | free (them) |
| S0.4 | E7.4 | free |
| S0.5 | E6.1 **+ E6.4** + MSA hashing | free |
| S0.6 | E5.1 | cheap |
| S0.7 | E0.4, E3.1, E3.2, E3.3, E4.2, E5.3, E5.4 | free |
| G3a/b | E1.2 **and E7.6** | 7,680 / 38,400 |
| G4a/b | E1.3 | 5,120 / 25,600 |
| G6a/b | E2.2 | 5,440 / 27,200 |
| G8 | E4.1 | 7,200 |
| G9 | E1.4 | 6,400 |
| G10 | E1.5 | 4,200 |
| G11 | E1.7 | 6,400 |
| G12 | E1.6 | 6,400 |
| G13 | E4.4 | 600 |
| G14 | E7.3 | 4,800 |
| ~~G15~~ | ~~E7.2~~ — **struck** with the class B/F scope decision | ~~4,000~~ |
| G16a / G16b | E1.8 / E1.8+E1.1 | 2,400 / 4,800 |
| G17a / G17b | E1.9 | 3,600 / 18,000 |

`RUN_MATRIX` budget tiers: **MINIMAL 45,860** predictions (1.4 Block-B drops, 4.1% of the
core factorial), **INTENDED 155,100** (1.25× the campaign to date), **EXPANSIVE 249,540**.

**Pillar 0 is NOT `RUN_MATRIX` Stage 0**, and the difference is eleven free items: Stage 0
covers 14 experiments across S0.1–S0.7; Pillar 0 lists four and **none of them is an S0.x
row.**

---

## Flagged: blocking experiments

Four experiments are marked **blocking** in the campaign record
(`redo/inputs/run_registry.tsv`, `campaign_verdict_line` column; sourced from
`redo/spec/CAMPAIGN.md`):

| id | line | why |
|---|---|---|
| **E0.1** | *SURVIVES, promoted to blocking* | Every rate in the redo is graded by this ruler. **All five E0 experiments are `BLOCKED` on the Pillar 1 measurement pass**, which does not start without Aditya's word. Until it runs, every state call rests on a threshold inherited from the frozen campaign. |
| **E3.1** | *SURVIVES, promoted to blocking* | **F-2: it cannot be done at all under the inherited scorer** — below pLDDT 50 the call *is* the confidence. Redo it with the early return removed. |
| **E6.4** | *SURVIVES, blocking* | **Free before dispatch, impossible after.** Blocks A and B both failed it (1,898 distinct `seed_outer` across 380 Block A cells). |
| **E8.3** | *SURVIVES, blocking, and it got worse* | The only experiment whose **catalogue heading itself carries "Blocking."** Blocking for everything in Group 8. `CAMPAIGN.md` adds a second mechanism nobody had: `subsample_msa.py:106-107` returns the input unchanged when `len(entries) <= depth` while the manifest records the nominal depth. **The `full` rung is not a condition, it is a name.** |

Two further blocking dependencies live in `PLAN.md` rather than in the registry:

- **E1.9 / G17 — "partner MSA on vs off — is BLOCKING and belongs here, not in the SI"**
  (`PLAN.md` Pillar 3, 3,600 predictions). The primary design runs the partner chain at
  query-only depth, which is **the first instance of one-chain single-sequence inside a
  complex anywhere in 83 papers**. With G17 that is a measured choice with its price
  attached; without it, it is an unmeasured manipulation under the arm that carries the
  headline.
- **Two recording columns are blocking, not cosmetic** (`PLAN.md` Pillar 0):
  `g1_recording_spec.tsv` carried 47 columns and no pocket-RMSD column when this was written; it carries **79** today and both pocket columns are present (Part 12 records the correction). Without
  `pocket_ca_rmsd_active` and `_inactive` a depth sweep has no reference-free readout,
  because `kalakoti2025afsample2` [p.6] states model confidences across masking levels are
  *"not directly comparable"*.

Hard orderings recorded in `RUN_MATRIX` §7.4: **S0.2 before any rate is reported**;
**P3/P3b before any depth cell**; **G1 before G9, G10, G12** (each needs a rung length);
**G11 last** (it is a harness change); **S0.7's E4.2 before G3** (the exposure covariate and
its median split must exist before the bulk control dispatches).

---

## Flagged: experiments the literature has already done

Six entries carry a `DONE` in their Novelty line. Each means something different and the
difference is load-bearing.

| id | what is DONE | what survives | must cite |
|---|---|---|---|
| **E3.1** | **The headline, DONE many times over.** Eight papers. | The *re-aggregation* finding — a confidence metric changing sign between whole-complex and anchor grain (Protenix2 +0.33 → +0.07; OpenFold3 −0.26 → −0.63). **Frame clause 3 as confirmation on a new axis, not as discovery.** | `bryant2024cfold`, `ye2026multistatebias`, `sun2026kinconfbench`, `schafer2025confounds`, `junker2026peptidedesign`, `yu2026domainmotion`, `ku2026promise`, `kalakoti2025afsample2` |
| **E2.4** | **The question is DONE and is the sharpest published challenge to this paper.** | Nothing about the question. **We have run 14,400 decoy predictions and not looked at them.** The answer must be quantitative and must cite them by name. | `yu2026domainmotion` |
| **E4.1** | **The design is DONE and well established.** | The *application* to a co-input effect. **"Not doing it is what would be unusual."** | `skrinjar2026generalization`, `swapna2025memorization`, `kim2026mac1`, `chiesa2025templatebias` |
| **E0.1** | **DONE twice at scale**, by `paajanen2026activation` (learned PC1, GMM threshold) and `khaleq2026hyaline` (supervised classifier, AuROC 0.99). | Neither is reimplementable: paajanen publishes no weight vector, residue list or repository; khaleq does not report its decision threshold and **has never been run on a predicted structure** — its authors propose exactly our use case as future work. Our claim is a *reimplementable, per-axis, off-panel-calibrated* predicate. | `paajanen2026activation`, `khaleq2026hyaline` |
| **E5.5** | **DONE as a genre**, with several correlates already published. | Nothing novel. **Value is internal** — use the published correlates rather than rediscovering them. | `skrinjar2026generalization`, `yu2026domainmotion`, `chib2025gpcrstates` |
| **E1.2** | **The ligand analogue is DONE and is the threat.** | **OPEN for protein partners** — no paper runs a scrambled or decoy *protein* partner. E1.2 tests whether yu's finding extends to protein co-inputs, which is stronger than confirming it. | `yu2026domainmotion`, `masters2025physics`, `bret2025boltz2docking` |

Two more entries disclaim novelty without using the word:

- **E7.4** — *"Not novel; load-bearing."*
- **E8.3** — *"None; it is a prerequisite."*
- **E0.4** — *"Not a novelty claim; a robustness one."*
- **E5.2** — *"Fills a hole rather than claiming ground."*

And two carry a **partial** DONE that must not be quoted flat:

- **E2.1** — **ADJACENT, not open.** An "agonist alone does not" sentence is a confirmation
  at scale, and must cite both `ye2026multistatebias` (small molecules move state weakly)
  **and** `vo2026fiducials` (agonist alone drives β2AR TM6 nearly fully out, with the Gs α5
  adding under 1 Å) — which say opposite things.
- **E3.3** — the corrected line. `miglionico2026atlas` **did** ask the partner-confidence
  question at an α5 position (AUC 0.762), but **for binding, not for conformational
  correctness**. What survives is narrower and has a published number to beat.

---

## Disagreements found while deriving these numbers

Recorded because the project's standing rule is that a disagreement found is worth more
than a tidy number copied.

**1. "45 experiments" is a count of headings, not of ids.** 45 headings carry **46** distinct
ids; `run_registry.tsv` has 45 rows and no E6.3 row. The registry's `title` field for E6.2
is the truncated fragment `"/ E6.3 — Ship the three Block D rows.csv and rows.tier3.v2.csv"`
— the heading's leading `E6.2` was consumed by the id parser. Cosmetic, but it means the
registry's own title column cannot be pasted into a document as-is.

**2. `PLAN.md`'s correction #1 is false as written today.** It states *"`PLAN.md` names ZERO
experiment ids. A grep returns nothing."* A grep today returns **16 hits over 15 distinct
ids**, and one of them is in the **plan body**, not the corrections section: line 31, step 4
of the §0a route table, *"the free registry items, **E7.4 first** — it must precede the
ligand arm"*. The other 15 hits are at lines 359–380, inside the corrections section itself.
The underlying claim — that the *pillar sections* name no ids — remains true.

**3. `PLAN.md` has six pillars, not five.** `grep -E '^## ' redo/spec/PLAN.md` returns
`Pillar 0` through `Pillar 5`, plus a separate ten-step route table (steps 0–9) in §0a. Any
description of "the five-stage ordering" is under-counting. **Pillar 2 discharges zero
catalogued experiments**, which the plan records itself.

**4. Three prediction counts in the catalogue do not reproduce from their own stated
factors**, under the catalogue's own header convention of 50 predictions per cell:

| where | catalogue says | re-derived | gap |
|---|---:|---:|---|
| E1.5, "at 50 samples and 4 backbones" | **84,000** | 21 × 10 × 4 × 50 = **42,000** | exactly 2× |
| E8.1 table, full three-way (2,080 cells) | **260,000** | 2,080 × 50 = **104,000** | exactly 2.5× |
| E8.1 table, depth × partner all depths (1,040 cells) | **130,000 gross / ~104,000 new** | 1,040 × 50 = **52,000 gross**, minus D3's existing 26,000 = **26,000 new** | 2.5× |

The cell counts themselves (2,080 and 1,040) are correct; it is the per-cell multiplier that
drifts. The same table's last two rows (624 cells → 31,200; 144 cells → 7,200) *do* use 50
per cell, so the table is internally inconsistent. A third row — "2 depths, 1 backbone,
104 cells → ~2,600 new" — is correct **as new** (5,200 gross minus the 2,600 D3 already
holds), but the neighbouring "3 depths → ~31,200 new" is the *gross* figure mislabelled as
new (new would be ~15,600). Every other prediction count in the catalogue reproduces: **28 of
31 arithmetic checks pass.**

**5. `E8.1` is the only one of the 45 with no cost-class token.** Its Cost bullet reads
*"Cost, with the affordable projections spelled out"* followed by a table, so the registry's
`cost_class` field for E8.1 is **empty**. Its content is unambiguously `real`.

**6. The registry's `named_in_run_matrix` column under-reports by two.** `grep -oE
'E[0-9]+\.[0-9]+' redo/spec/RUN_MATRIX.md | sort -u` returns **33** ids; the registry marks
**30** as `yes`. The three-way difference: **E0.5** and **E4.3** appear in `RUN_MATRIX.md`
prose and its dependency graph (lines 423, 903, 923) but have no costed line item, and
**E6.3** has no registry row. The column means "has a costed line item", not "is mentioned"
— a defensible semantics, but the name invites the wrong reading.

**7. `g2_systems.csv`'s antagonist level is not homogeneous, and E2.3 is not as empty as the
registry says.** 19 rows requested as `ligand = antagonist` carry `ligand_role_actual =
inverse_agonist` — **all 19 inside E2.2**, on 5 receptors (`ADRB1 AGTR1 B1B1U5 NTR1 OPSD`),
17 of them READY, 10 flagged `ccd_resolves_to_other_isomer` and 2
`source_row_role_disagrees_with_gpcrdb`. Together with E2.3's own 6 rows that is **25
inverse-agonist rows enumerated and 23 READY**, while E2.3's registry verdict is `DIES` and
the catalogue's E2.3 text says Block C has "no partial and no inverse agonist". Both
statements are true of *Block C*; neither is true of the redo's own enumeration. **An
experiment marked DIES has a usable arm already sitting in the inputs, and E2.2's antagonist
level mixes two pharmacological classes.**

**8. `CLAUDE.md`'s input-provenance figures are stale.** It states *"14 of 64 inputs name no
generator"* and that `g1_recording_spec.tsv` *"has no writer anywhere in `redo/build/`"*.
Today `redo/inputs/MANIFEST.tsv` holds **65 rows, of which 15 carry `generator =
unattributed`**, and `redo/build/g1_recording_spec.py` **exists** (12,802 bytes) and is named
as that file's generator in the manifest. `CLAUDE.md` itself says its corpus counts are
allowed to lag; this is one of them. The 15 unattributed are: `g0_measurements.csv`,
`g0_pilot_measurements.csv`, `g0_selftest.txt`, `p7_confidence_separation.csv`,
`p7_per_receptor.csv`, `panel_gpcrdb_constructs.csv`, `panel_gpcrdb_degree.csv`,
`panel_reference_qc.csv`, `panel_strict_confornets.csv`, `panel_systems.csv`,
`panel_uniprot.tsv`, `seq_a5null.tsv`, `seq_constructs.tsv`, `seq_controls.tsv`,
`seq_rungs.tsv`. All 65 manifest entries are present on disk and no disk file is missing from
the manifest.

**9. The catalogue records its own earlier miscount, and it is the same failure mode.** The
document, its header and `RUN_MATRIX.md` all said **"33 experiments in 9 groups"** until
2026-09-12. The body held 45 in 10 the whole time. *"The body is authoritative; the count in
any summary is not."*

---

# Part 9. The five-stage plan — what runs, in what order, and what each stage settles

The ordering principle, from `PLAN.md`: **do everything that needs no GPU first, so
that the decisions which need the PI stop blocking the rest.** Each stage is a stopping
point that settles a complete sentence. Nothing here is a single commitment that buys
nothing until all of it lands.

### Stage 0 — costs nothing, and blocks everything below

| item | what | why it blocks |
|---|---|---|
| Mine `rows.tier3.v2.csv` | cluster unit, continuous readout, seeds | **done** |
| **Add two pocket-RMSD columns** | distance from the predicted pocket to the deposited **active** and to the deposited **inactive** structure | Without them a depth sweep has **no reference-free readout**, because model confidences are not comparable across masking levels. They are also the only thing that separates *"shallow MSA moves the number"* from *"shallow MSA produces a different object that happens to trip the same two distances"* — and the second is a much stronger result that we currently could not claim even if it were true |
| **Option Z** | measure the real alignment depth per (receptor, rung), receptor-side **and paired** | **A paired depth has never been measured by anyone** |
| Re-derive the thresholds | | decides which receptors are evaluable at all |
| **Pair the random seeds across arms** | | **free now, impossible after dispatch.** Blocks A and B both failed it — 1,898 distinct `seed_outer` over 380 cells, so the same seed never ran both arms of a cell |

### Stage 1 — the instrument. CPU only. **This has already run.**

**What it did.** Measured both state axes on **1,357 deposited PDB structures**:
**726 calibration** (no ortholog of the receptor appears anywhere in our panel),
**610 application** (on-panel, held out), **21 intermediates**.

**Why it exists.** The thresholds were fitted on the same annotated structures the
study then grades with. The first methodological objection a referee makes is that the
ruler was built from the answer sheet. Measuring off-panel is the answer, and it costs
no GPU time.

**The result — the inherited rule, applied unchanged to structures it never saw:**

| set | rule | n | sensitivity | specificity | Youden |
|---|---|---:|---:|---:|---:|
| calibration | both axes (AND) | 487 | 86.5 % | **100.0 %** | +0.865 |
| calibration | NPxxY-OH alone | 487 | 86.7 % | 98.8 % | +0.855 |
| calibration | **TM6 tilt alone** | 585 | 96.6 % | **100.0 %** | **+0.966** |
| application | both axes (AND) | 485 | 93.4 % | 100.0 % | +0.934 |
| application | NPxxY-OH alone | 485 | 93.4 % | 99.4 % | +0.928 |
| application | **TM6 tilt alone** | 501 | 100.0 % | 97.8 % | +0.978 |

**Two findings fall out.**

**(a) The inherited rule survives off-panel**, with **zero false positives on 81
calibration inactives**. That is a direct, cheap answer to the circularity objection.

**(b) The conjunction is worse than one of its two halves.** On the same 487 rows, TM6
tilt alone scores **+0.973** against the AND rule's **+0.865** — identical perfect
specificity, eleven points more sensitivity. The NPxxY axis is removing true actives
and adding nothing. **The paper currently presents the two-instrument conjunction as a
methodological strength.** Caution: that comparison runs on rows where both axes are
measurable, a population the NPxxY axis itself selected, so it is not yet safe to act
on.

**Two counterexamples to carry into decision D4:** one off-panel **inactive** sits at
**8.95 Å** on NPxxY, below the 9.08 cut; one off-panel **active** sits at **12.11 Å** on
tilt, below 14.932. Both current cuts already have a counterexample outside the panel
they were fitted on.

**What Stage 1 did NOT do: fit a new threshold.** `GROUP0_SYSTEMS.md` §6 forbids
fitting before the balancing rule is settled, and that is **D4**, still open (Part 14).

**A defect found while running it (`DECISIONS.md` F-30).** The two axes were
**coupled** in our own measurement code: a non-tyrosine at position 5.58 silently
discarded the **tilt** measurement too, on an axis that shares no atom, no residue and
no identity requirement with NPxxY. Separating them re-opened a wrong-residue failure
mode that produced Cα–Cα distances up to 71.5 Å; restoring the documented rule that the
identity-numbering strategy requires **all four** anchors fixed it. Net: **0 previously
produced values changed, 54 withdrawn** (several sitting on the decision boundary —
14.760, 14.920, 14.951 against a cut at 14.932), **115 gained**.

### Stage 2 — the competing explanation. Apo, monomer, four backbones.

**The rival claim is: "the models call the receptor active because you starved the
alignment, not because you added a partner."**

That claim is **apo and partnerless by construction**, so testing it needs only **one
chain** — which is why this is the only stage deployable on all four backbones today.
It never touches the per-chain MSA mapping that blocks the other regimes.

Full detail in Part 7. The controlling rule is worth repeating here: **every
hyperparameter is inherited from published work on other proteins and is never tuned on
our panel**, because any parameter tuned until it gives the wanted answer produces an
agreement that carries no information (Part 15, F-33).

### Stage 3 — the main claim. The ladder.

`inputs/g1_systems.csv`, **2,039 rows, 23 arms** (Part 4 for constructs, Part 3 for
receptors). The arms, by size:

| arm | item | rows | receptors | what it asks |
|---|---|---:|---:|---|
| `composition_controls` | G4a/G4b | 300 | 30 | is it the sequence, or just bulk? |
| `ladder` | G1a/G1b | 210 | 30 | **the main curve** |
| `ladder_pilot` | P1 | 210 | 30 | the same, as a contract proof before the real run |
| `ala_scan` | G10 | 210 | 10 | which of the 21 positions matter |
| `gi_to_gs_series` | G10b | 150 | 10 | walking one family's tip into another's |
| `intermediate_nested` | G1c/G1d | 90 | 30 | the mini-Gα series, 44 → 279 residues |
| `intermediate_pilot` | P1b | 90 | 30 | its pilot |
| `deposited_minig_anchor` | G1f | 90 | 30 | deposited mini-G constructs as anchors |
| `wetlab_length_series` | G18a | 90 | 30 | **the 13/17/19-mers** |
| `a5null` | G3a/G3b | 90 | 30 | the full subunit with α5 removed |
| `non_ga_bulk` | G3a/G3b | 90 | 30 | ubiquitin and KaiB |
| `partner_msa_on` | **G17** | 90 | 30 | **blocking** — prices the query-only partner choice |
| `wide_replication` | G2 | 72 | 24 | does it hold on 24 further receptors |
| `family_swap` | **G9** | 30 | 30 | non-cognate partner — **NOT BUILT**, Part 13 |
| `gi_gt_single_residue` | G12 | 30 | 30 | a natural single-residue Gi/Gt pair |
| `heterotrimer` | G11 | 30 | 30 | Gα + Gβ1 + Gγ2, three chains |
| `hd_deletion_companion` | G1e | 30 | 30 | helical-domain deletion |
| `intermediate_optional` | G1c-opt | 30 | 30 | |
| `chimeric_ref_extension` | G20 | 30 | 10 | chimera-only receptors |
| `uncoupling_peptide` / `_full` | G16 | 36 | 6 | known uncoupling mutants |
| `reference_matched_tip` | G19 | 23 | 12 | tip matched to the reference structure |
| `wetlab_matched_peptides` | G18b | 18 | 6 | peptides matched to published wet-lab work |

**Analyse length as a continuous covariate, not as a step test.** The proposed mechanism
is helix formation, and helicity rises gradually with peptide length — published
wet-lab work reports that peptides of 17 residues and more have a *stronger propensity*
to adopt an α-helix, and the 11-mer and 21-mer form helices of different length
(Arg389–Leu394 against Asp381–Leu394). **A smooth monotone response is what the
mechanism predicts; a sharp step at any particular residue count is what would be
surprising.**

**No 16-residue rung.** AlphaFold3's "16" governs how its training and evaluation sets
were built, not what it does at inference; Chai-1 uses 9 and keeps those peptides;
Boltz-2 has no such line; OpenFold3 has no length branch at inference at all. There is
no boundary at inference for a 16-mer to resolve (`DECISIONS.md` F-16).

**A construct-naming ceiling.** The α5 helix is **Asp368–Leu394, 27 residues**.
`R4_a5helix` (26) sits inside it; **`R5_a5plus` (36) is past it**, so the Methods must
describe that construct as α5 **plus flanking sequence**, never as "a longer α5".

### Stage 4 — the ligand

`inputs/g2_systems.csv`, **313 READY rows, 8,716 pooled predictions**. Part 5 for the
design, Part 6 for the decoy arm inside it.

**State the goal as measurement, not as a predicted direction.** The honest goal is
*"measure the ligand's contribution at a fixed partner condition"*. It is **not** "show
the drug flips the receptor" — our own data points the other way: on
`rows.tier3.v2.csv` the decoy ligand is indistinguishable from the neutral antagonist on
all four backbones (**+0.011, −0.004, −0.016, −0.004**), and the ligand effect is small
beside the partner's. **A null here is a finding**, and the goal is worded so that it
can be reported as one.

### Stage 5 — supporting material

- **Peptide ligand tiers kept separate from small molecules.** A peptide ligand is
  another polymer chain, so pooling the tiers would confound the ligand axis with the
  chain-count axis (`D-2026-09-12-f`).
- **The F-19 decoy-refusal finding** (Part 6.9), which stands whether or not the arm
  runs, and is a result about the field's standard negative control rather than about
  us.
- **A date-stratified holdout** for the memorisation risk, using **Protenix's
  2021-09-30** as primary (32/32 receptors, 23 against 20 clusters, zero panel change)
  — **conditional on re-deriving the cutoff from the model cards ourselves**, because
  the pipeline team report that three of their own documents give three different
  cutoff sets for the same quantity and every value is flagged unverified in their own
  pre-registration. **OpenFold3 has no published cutoff at all** and is excluded from
  any date stratification by their documented position, not by our choice.

### The one adaptive parameter, and why it is a band rather than a maximum

The PI asked that the partner condition used in the ligand arm be informed by what the
ladder finds. It is, and this is the mechanism that makes it an adaptive design rather
than a choice made after seeing results. **The rule is committed before Stage 3 runs;
only then is the adaptation mechanical.**

> **The ligand crossing runs at the SHORTEST rung whose pooled apo→cognate shift,
> measured on the Group 1 ladder, falls inside the band `[PI lower]`–`[PI upper]`.**
> Ties break toward the shorter construct. A rung is excluded **on feasibility** —
> never on its effect size — if (i) any backbone cannot represent it natively, or
> (ii) Option Z shows its partner alignment is single-sequence in practice at that rung.

**Why a band and not the maximum.** The criterion must reference **headroom**, which is
a property of the measurement, and never **effect size**, which is a property of the
result. Selecting the rung with the largest shift would select the partner condition
that most flatters our own effect — the same error as tuning a masking rate on our own
panel. And headroom is the binding constraint here: **apo sits at 0.158 and cognate at
0.891, both pinned**, so an interaction estimated at either endpoint has nowhere to
move.

**What is not adaptive.** The cognate identity is frozen, because the supplied peptide
and the scoring reference must be the same molecule; re-picking the cognate on which
the assignment agrees better would destroy that guarantee. And the matched nulls run at
**whatever rung the real peptide runs at** — a null and its treatment at different rungs
is an uninterpretable comparison, and it is precisely the failure an adaptive design
produces by accident.

**The band is not set.** Roughly 0.25–0.75 is the shape; the number is the PI's, and it
must be recorded **with its date, before any ladder result exists**. A gate then asserts
mechanically that the enacted rung equals the rule applied to the Group 1 results, so
the adaptation cannot drift silently — the same treatment `drule.py` gives the decoy
selection.

---

# Part 10. Thirteen experiments that are NOT in the catalogue

Found 2026-09-14 by an audit run against all 45 catalogued experiments. Nineteen were
proposed; each was screened three ways — already-catalogued, already-published,
feasible-and-powered — and **19 screen verdicts rejected proposals** across DUPLICATE,
INFEASIBLE, UNDERPOWERED and PREEMPTED, so the screens were not rubber-stamping.
Thirteen cleared. **Six cost nothing.** Full detail in
`redo/spec/EXPERIMENT_GAPS_2026_09_14.md`.

The four that matter most:

**R0 — the recording-contract amendment.** Not an experiment; a precondition, and the
highest-value item found. See Part 13, defect 1.

**T2 — the register slide. 600 predictions.** `GROUP1_SYSTEMS.md` makes "every emitted
construct is a suffix of its parent" a construction invariant and proves it by
planting. That invariant is exactly why the ladder cannot answer its own question:
every rung, every null and every scramble shares the same C-terminal residue, so the
campaign varies length, composition and identity and has **never varied register**.
Take the native α5 sequence and slide the window along it. If a 21-mer taken from the
wrong section works as well, **the title must say "an α5-derived peptide", not "the α5
C-terminus"** — and that is the finding, not a failure.

**X1 — the anchor-admissibility census. Free.** Recomputed on Block B's 32,000 rows:
**65.5 % carry at least one predicate-defining anchor below pLDDT 70** (3.85 % below
50). The gate is severely arm-imbalanced and moves control arms in *opposite*
directions — keep-rate at ≥70 is apo 28.6 %, decoy 22.1 %, shuffled 31.2 %, cognate
55.9 %, and **OpenFold3's apo cells keep 19 of 2,000 rows**. So every arm contrast in
the paper is partly a survivorship contrast and nobody has looked. Carry
`min_plddt_at_anchor` as a **covariate**, never as a filter — conditioning on a
post-treatment variable is a collider.

**T1 — template state × partner presence.** Templates are the field's standard channel
for supplying structural information, and **nobody has ever switched them on in either
campaign**. This matters because the strongest published counter-example to this work
reaches alternative conformations **with templates ON** and a similarity cutoff dropped
to 1 %, and reports that templates carry state information at shallow MSA depth.

**Runner-up, and it would be third on a different day: X5, the placebo axes.** It is
the only proposal that adds a quantity that is supposed *not* to move — the difference
between "the bulk control did nothing" and "the bulk control distorted the receptor".
With the current recording contract those two produce **the same number**, and Stage 3's
bulk and composition controls are 64,000 predictions of exactly that comparison.

---

# Part 11. Verification machinery — how to check anything in this document

*Everything in this section was executed on 2026-09-14 from the repository root
`/Users/aditya/Documents/tools/Novartis_projects/paper`. Every number below is the
output of the command printed beside it, not a transcription from a prose document.
Where a prose document disagrees, both values are given and the disagreement is
flagged.*

---

### 1. What the machinery is

The redo campaign has produced **67 generated input files** (64.3 MiB) and **zero
predictions**. Nothing has run on a GPU. Consequently every claim in the spec
documents is a claim about *inputs* — what will be dispatched, to which receptors,
with which partner and which ligand — and the verification machinery exists to make
each of those claims re-derivable in one command.

There are three layers:

| layer | what it proves | where |
|---|---|---|
| **the gates** (9 Python files in `redo/gates/`) | a claim recomputes from the data files | `redo/gates/*.py` |
| **the manifest** | no input file has changed since it was stamped | `redo/inputs/MANIFEST.tsv`, written by `redo/build/manifest.py` |
| **the self-tests** | each check actually fires when the defect it names is present | `--selftest` flags on 6 of the 9 gates |

The third layer exists because of a documented failure in this repository: four
checkers once reported nothing because their reporting path never ran, and on
2026-09-12 `g0_preflight.py`'s plant harness was found to have been staging only the
*top-level* files of `redo/` — every plant failed to apply, every check reported MISS,
and the harness printed a tidy tally. **Do not read a gate's tally as coverage of the
gate. Run the self-test.**

---

### 2. The gate inventory — measured, not quoted

Every row was produced by running the file. Timings are wall-clock on the author's
laptop.

| gate | lines | checks it prints | exit today | runtime | self-test flag | plants | runtime |
|---|---:|---:|---|---:|---|---:|---:|
| `layout.py` | 491 | **8** (L1–L8) | 0 CLEAN | 0.2 s | `--selftest` **and** `--selftest-all` | 7 + 7 | 0.1 s / 4.2 s |
| `g0_preflight.py` | 488 | **13** blocking (G0-1…G0-13) + 8 WAIT | 0 FROZEN | 0.2 s | `--selftest` | **12** | 3.6 s |
| `g1_preflight.py` | 589 | **18** blocking (B1…B18) + 5 WAIT | **2** (pending) | 0.1 s | `--selftest` | 18 | 1.6 s |
| `g2_preflight.py` | 641 | **15** blocking (G-1…G-15) + 7 WAIT | **2** (pending) | 0.1 s | `--selftest` | **16** | 0.8 s |
| `ligands.py` | 332 | **10** (L-1…L-10) | 0 CLEAN | 0.1 s | `--selftest` | 10 | 0.4 s |
| `drule.py` | 1145 | **26** (D-1…D-26) | 0 CLEAN | 7.3 s | `--selftest` | 26 | **206 s** |
| `seqrec_verify.py` | 330 | **60** | 0 (60/60) | 1.6 s | `--plant` *(one plant, not one-per-check)* | 1 | 1.6 s |
| `panel_verify.py` | 381 | **92** in 13 sections | 0 | 0.8 s | **none** | 0 | — |
| `run_receipt.py` | 150 | **4 per run** (R1–R4) | 0 *("no runs yet")* | 0.1 s | **none** | 0 | — |

**Totals: 242 checks executed today across 8 gates** (8 + 13 + 18 + 15 + 10 + 26 + 60
+ 92), plus 4 defined-but-never-executed checks in `run_receipt.py`. **97 planted
defects** prove 155 of those 242.

Exit-code semantics differ between families and this matters when scripting:

- `layout.py`, `ligands.py`, `drule.py`, `run_receipt.py`, `seqrec_verify.py` — **0 = clean, 1 = a check failed.**
- `g0_preflight.py` — **0 = FROZEN, 1 = NOT FROZEN.** `WAIT` items never fail the gate.
- `g1_preflight.py`, `g2_preflight.py` — **0 = ready to dispatch, 1 = a BLOCKING check failed, 2 = all blocking checks pass but a PENDING dependency is outstanding.** Both exit **2** today. `verify.sh` matches on the string `0 failed`, not on the exit code, which is why a 2 does not break the build.
- Every `--selftest` exits **0** when all its plants fire.

---

### 3. `redo/gates/layout.py` — the eight structural checks

`layout.py` answers the one question a flat directory cannot: *may I edit this file,
and has anyone already?* Run it with `python3 redo/gates/layout.py`.

Live output, 2026-09-14:

```
  PASS  L1  redo/ holds only its eight declared entries  9 entries, all declared
  PASS  L2  every file is the kind its directory is for  6 directories clean
  PASS  L3  every generated input matches its recorded hash  67 files, all match
  PASS  L4  the manifest has no row without a file  65 rows all resolve
  PASS  L5  every run directory has the same three files  no runs yet
  PASS  L6  every run names input hashes we hold  no runs yet
  PASS  L7  the regenerable bulk is gitignored, and nothing else is  only redo/cache/structures/
  PASS  L8  every input's named generator exists  15 of 67 name NO generator ...
  CLEAN -- 8 checks pass.
```

| check | what it asserts, precisely | failure mode it catches |
|---|---|---|
| **L1** | `redo/` contains only `{README.md, paths.py, spec, build, gates, inputs, cache, runs, protocol}`. *(Note: the check name says "eight declared entries" and the detail line reports **9 entries** — the `TOP` set in the source has nine members. The count in the label is stale; the set is what is enforced.)* | growth at the top level instead of inside `runs/` |
| **L2** | every file's extension matches its directory's allow-list, and no unexpected subdirectory exists. `spec/` `.md`; `build/` `.py`; `gates/` `.py`; `inputs/` `.tsv .csv .fasta .txt .json .gz`; `cache/` `.json` + the `structures/` subdir; `protocol/` `.md` + `received/` | a scratch file, a shell script, or a stray directory landing in a curated folder |
| **L3** | for every file in `inputs/`, `sha256(file)` equals the digest recorded in `MANIFEST.tsv`, **and** no file on disk is absent from the manifest | a hand-edit made *after* stamping; a regeneration that was not restamped |
| **L4** | every row in `MANIFEST.tsv` resolves to a file that exists | a deleted input leaving an orphan manifest row |
| **L5** | every directory under `runs/` contains exactly `manifest.json`, `rows.csv`, `README.md` | a half-landed delivery |
| **L6** | every hash in a run's `manifest.json` `input_sha256` list is one of the digests in `MANIFEST.tsv` | a run dispatched against inputs we do not hold |
| **L7** | `.gitignore` contains `redo/cache/structures/` **and no other `redo/` rule** | committing 297 mmCIF files; or an over-broad rule silently excluding `inputs/` from git |
| **L8** | every `generator` named in `MANIFEST.tsv` exists as a file in `redo/build/`. **Blocking on the strong error** (named-and-absent). **Reporting-with-a-count on the weak error** (no generator named) — 15 of 67 today | a file that cannot be regenerated at all |

#### The two self-tests, and why they are separate

```
$ python3 redo/gates/layout.py --selftest
  ok   the admitted kinds pass, .gz included
  ok   planted secret.sh      -> L2 fires
  ok   planted notes.md       -> L2 fires
  ok   planted scratch        -> L2 fires
  ok   planted archive.zip    -> L2 fires
  ok   planted table.tsv.bz2  -> L2 fires
  ok   planted a subdirectory  -> L2 fires
  L2: 7/7 plants fire -- .gz is admitted and nothing else new is.

$ python3 redo/gates/layout.py --selftest-all
  ok    the staged copy passes unplanted
  ok    planted L1  -> L1 fires=True
  ok    planted L3  -> L3 fires=True
  ok    planted L4  -> L4 fires=True
  ok    planted L5  -> L5 fires=True
  ok    planted L6  -> L6 fires=True
  ok    planted L7  -> L7 fires=True
  ok    planted L8  -> L8 fires=True
  L1,L3-L8: 7/7 plants fire (L2 has its own harness: --selftest)
```

Three design points worth copying:

1. **`--selftest` prints a tally over plants against L2 alone**, not over the guard's
   eight checks. The source comments say so explicitly. A one-check self-test printing
   "8/8" beside an eight-check guard is the header-count failure class inside a test
   harness.
2. **`--selftest-all` subtracts a baseline run.** A check already failing on the
   unplanted tree cannot be proved by planting it — it would fire for a reason
   unrelated to the plant. The first line of the output is the baseline verdict.
3. **The staging asserts it reproduces `redo/` before any plant runs.** `_stage()`
   walks `redo/` into a temp directory as symlinks, then builds a file inventory of
   both trees and raises `AssertionError` if they differ. This is the fix for the
   2026-09-12 harness bug; a plant that needs to modify bytes calls `_materialise()`
   first so it can never write through a symlink into the real tree.

---

### 4. `redo/build/manifest.py` — the sha256 guard, and exactly what it is blind to

#### How it works

```
python3 redo/build/manifest.py           # rewrite MANIFEST.tsv
python3 redo/build/manifest.py --check   # exit 1 if it is stale, write nothing
```

`MANIFEST.tsv` has four columns: `file`, `sha256`, `bytes`, `generator`. `rows()`
walks `redo/inputs/`, skipping `MANIFEST.tsv` itself and dotfiles, and hashes every
regular file with a streaming SHA-256 (1 MiB chunks). `--check` renders the table in
memory and compares it byte-for-byte against the file on disk; any difference in
*any* column — a changed hash, a changed size, a changed generator attribution —
makes it exit 1.

Verified today:

```
$ python3 redo/build/manifest.py --check   ; echo $?
0
```

and, regenerated into a throwaway copy of the tree:

```
MANIFEST.tsv: 67 files  (51 attributed, 1 ambiguous, 15 unattributed)
$ diff <scratch>/redo/inputs/MANIFEST.tsv redo/inputs/MANIFEST.tsv
(identical)
```

So the committed manifest is exactly what the generator produces.

#### How the `generator` column is derived

By **static AST analysis**, never by observing a run. `generators()` parses every
`.py` in `redo/build/` and `redo/gates/` and records a filename → script edge only
when a name is **bound to an `os.path.join(..., "literal")` and then reaches
`open(..., "w"|"a")`**, directly or as a loop target. Three refinements matter:

- **Rebinding is handled by source line.** `g0_calibration_set.py` rebinds `out` once
  per output file; a naive name→literal dict keeps only the last and loses eight
  attributions. Each write is matched to the nearest binding *above* it.
- **Test scaffolding is not authorship.** Writes inside a function whose name contains
  `selftest`, `plant`, `stage`, `materialise` or `materialize` are excluded — without
  this, `layout.py` was recorded as the generator of `ligand_tiers.tsv` because its L3
  plant appends to it in a staged copy, which is statically indistinguishable from the
  real file.
- **Ambiguity is preserved, not guessed.** Two writers → both names, comma-joined
  (one file today); zero writers → the literal string `unattributed`. The docstring's
  reasoning: *a wrong generator is worse than a blank one — it says which code is
  answerable for a number, and that is a claim.*

#### The current attribution split

`awk -F'\t' 'NR>1{print $4}' redo/inputs/MANIFEST.tsv | sort | uniq -c`

| status | count | of 65 |
|---|---:|---:|
| **attributed to exactly one generator** | **49** | 75.4% |
| **ambiguous** (two writers) — `coupling_refstructures.csv` → `coupling_assign.py,coupling_fetch.py` | **1** | 1.5% |
| **unattributed** | **15** | 23.1% |

> **DISAGREEMENT.** `CLAUDE.md` states *"14 of 64 inputs name no generator (31 before
> the detector was fixed)"*; `DECISIONS.md` F-22 states *"31 of 64"* in its heading and
> *"now 14"* in its body; `layout.py`'s own L8 source comment says *"31 of 64 files are
> in that state today"*. The live value is **15 of 65**. The tree gained one input and
> one unattributed file since those sentences were written. `layout.py` L8 prints the
> live count on every run — read that, not the prose.

#### The 15 unattributed files — and why each one is unattributed

This split is not in any document; it was derived by reading each candidate
generator's write idiom. **Nine of the fifteen do have a generator; the detector
cannot see the idiom they use.** Six have no writer anywhere in the repository.

| file | bytes | generator (verified by reading the source) | why the AST walk misses it |
|---|---:|---|---|
| `seq_rungs.tsv` | 27,279 | `build/seq_rungs.py` | **writes to stdout**; the file is made by shell redirection |
| `seq_controls.tsv` | 55,115 | `build/seq_controls.py` | writes to stdout |
| `seq_a5null.tsv` | 3,420 | `build/seq_a5null.py` | writes to stdout |
| `seq_constructs.tsv` | 7,418 | `build/seq_build.py` | writes to stdout |
| `p7_confidence_separation.csv` | 1,618 | `build/p7_confidence_separation.py:217` | **pandas `to_csv`**, not `open(...,"w")` |
| `p7_per_receptor.csv` | 1,418 | `build/p7_confidence_separation.py:219` | pandas `to_csv` |
| `panel_systems.csv` | 106,700 | `build/panel_strict_columns.py:95` | `open(P('redo/inputs/...'), 'w')` — a **`P()` helper**, not `os.path.join` |
| `panel_strict_confornets.csv` | 9,536 | `build/panel_strict_confornets.py:87` | same `P()` helper |
| `g0_measurements.csv` | 345,233 | `build/g0_measure_axes.py:98,682` | `open(a.out, "w")` — an **argparse attribute**, not a bound `Name` |
| `g0_pilot_measurements.csv` | 7,266 | **none** — mentioned only in `g0_anchor_conservation.py`'s docstring | no writer exists |
| `g0_selftest.txt` | 2,242 | **none** — `g0_preflight.py` only reads it | no writer exists |
| `panel_gpcrdb_degree.csv` | 129,694 | **none** — a GPCRdb structure-browser export | hand-downloaded |
| `panel_gpcrdb_constructs.csv` | 40,339 | **none** — a GPCRdb construct-browser export | hand-downloaded |
| `panel_reference_qc.csv` | 350,945 | **none** anywhere in the repo | hand-made |
| `panel_uniprot.tsv` | 12,565 | **none** anywhere in the repo | hand-made |

`g0_measurements.csv` deserves a line of its own: it is the measured state axes on all
1,357 calibration structures — the campaign's central measurement product — and it is
regenerable (`g0_measure_axes.py`) but not *attributed*, so L8 counts it among the
fifteen.

> `CLAUDE.md` says *"at least two — including `g1_recording_spec.tsv`, the campaign's
> own recording contract — have no writer anywhere in `redo/build/`."* **That is now
> out of date.** `build/g1_recording_spec.py` exists (created 2026-09-12 under F-22),
> is named in the manifest, and `python3 redo/build/g1_recording_spec.py --check`
> prints `OK  49 columns, file matches the generator`. The count of files with no
> writer anywhere is **six**, listed above.

#### What L3 catches, and what it is BLIND to

L3 recomputes `sha256(file)` and compares it against the digest the manifest recorded
**for that same file**. That is a strictly narrower property than "this input is
correct", and two named findings sit in the gap.

**L3 catches:** a hand-edit made *after* stamping. Demonstrated today in a throwaway
copy of the tree:

```
$ printf 'HAND_EDITED\n' >> <copy>/redo/inputs/ligand_tiers.tsv
$ python3 <copy>/redo/gates/layout.py
  FAIL  L3  every generated input matches its recorded hash
            hand-edited or regenerated without restamping: ['ligand_tiers.tsv']
  LAYOUT VIOLATED -- 2 check(s) failed.
$ python3 <copy>/redo/build/manifest.py --check
MANIFEST.tsv is stale -- run: python3 redo/build/manifest.py      (exit 1)
```

**L3 is blind to — blind spot 1 (F-22): a file created by hand and then stamped.**
The digest was taken *from the hand-made bytes*, so the file passes L3 for ever.
Nothing checks that a file in `inputs/` came from code at all. The `generator` column
is the only record of provenance, and until 2026-09-12 nothing read it. L8 now reads
it, but L8 is only blocking on *named-and-absent*; a blank generator is reported with
a count, not failed, because failing 15 of 65 would stop the campaign rather than
improve it. **Six inputs today have no writer anywhere in the repository** — they are
hand-made files sitting in a directory declared code-only, and the guard set cannot
see that.

**L3 is blind to — blind spot 2 (F-21): a file gone stale against its own inputs.**
L3 compares a file to its own recorded hash, never to the hashes of the files its
generator consumed. The recorded instance: `run_registry.tsv` was written at 11:56;
`g2_systems.csv` was regenerated at 16:20 carrying three new experiments; the registry
was never re-run, so three experiments read as untriaged that had been enumerated five
hours earlier — **and `manifest.py --check` passed throughout, correctly**. The guard
set proves an input has not been *tampered with*. It does not prove an input is
*current*. Those are different properties.

The proposed fix for both — each generator declares what it writes and what it
consumed; `manifest.py` records the input digests alongside the output digest; a new
check fails when a consumed file's hash has moved — **is not built**. Until it is, a
generator whose inputs have moved must be re-run by hand, and the only thing standing
between the campaign and a stale artefact is somebody remembering.

---

### 5. The preflight gates

#### `g0_preflight.py` — is the Group 0 instrument frozen?

`GROUP0_SYSTEMS.md` is frozen as of 2026-09-11. This gate is what makes "frozen"
checkable: it re-reads every artefact the document quotes and confirms or refuses.
Three verdicts — `PASS`, `FAIL`, and `WAIT` (a declared dependency that cannot be
satisfied here yet; `WAIT` never fails the gate).

**13 blocking checks, all passing.** Live output:

| check | asserts | value today |
|---|---|---|
| G0-1 | every Group 0 companion file is present | 12 in `inputs/`, 3 in `build/` |
| G0-2 | the calibration/application split is the frozen 726/610 | 726/610, catalogue agrees |
| G0-3 | no receptor appears in both calibration and application | 147 vs 40 receptors, disjoint |
| G0-4 | the NPxxY axis is definable on 157/199 entries | 5.58 Tyr 164, 7.53 Tyr 189, both 157 |
| G0-5 | the frozen filter ladder F4 = 433 | 433 (372 A / 61 I, 106 receptors, 17 both-state) |
| G0-6 | the retracted rule Q0c is not reinstated | degree-100 gate absent from code and ladder |
| G0-7 | the independence ladder I1/I2/I3/I4 | 433 / 289 / 260 / 193 |
| G0-8 | pinned reference set shape | 162 rows, 64 with NPxxY, 0 of 69 off-panel populated |
| G0-9 | no active reference at or below GPCRdb's 11.9 Å inactive line | 0 of 95 |
| G0-10 | the class F defect is present as described | 700 class F rows at threshold 14.932 |
| G0-11 | the build-step self-test still reads 14 MATCH / 2 MISMATCH | 14 / 2 in `g0_selftest.txt` |
| G0-12 | the 1–3 GB mmCIF cache is gitignored | `redo/cache/structures/` present in `.gitignore` |
| G0-13 | the redo is Class A only, in both populations | calibration 1,357 rows all Class A; panel 64 receptors all A |

Eight `WAIT` dependencies are outstanding (D1–D4, Q4, Q6, the measurement pass, and
the F3 sensitivity question). They are the outstanding-decision list, not defects.

```
$ python3 redo/gates/g0_preflight.py --selftest
baseline: gate passes.  Planting one defect per blocking check.
  ok   G0-1 … G0-11, G0-13   (12 lines, every one "check fired")
  12/12 blocking checks proved by planting.
```

> **DISAGREEMENT / GAP.** `CLAUDE.md` records this gate as *"12/12 checks"*. The gate
> has **13** blocking checks and the harness has **12** plants: the `PLANTS` list in
> the source (lines 329–367) has no entry for **G0-12**. The tally line prints
> `{len(PLANTS) - bad}/{len(PLANTS)}`, i.e. a count over *plants*, not over *checks* —
> the same "tally over plants reads as coverage of the gate" trap that `layout.py`'s
> docstring warns about, occurring inside `g0_preflight.py`. **G0-12 (the gitignore
> check) has never been proved by planting.** It is the least consequential of the
> thirteen, but the sentence "12/12 blocking checks proved" is literally false.

The staging function `_clone()` (line 413) copies `redo/`, `data/block_b/09_references`
and `data/block_a/01_rows` with a recursive `shutil.copytree` — the top-level-only bug
is fixed — and `chmod`s the scratch copy writable, because `copy2` preserved the
read-only bit on `data/block_*` and that had stopped the G0-9 plant from applying.
**It does not, however, assert that the clone reproduces the original**, and it does
not assert that each plant changed bytes. Only `layout.py` and `g2_preflight.py` do
both.

#### `g1_preflight.py` — dispatch readiness for Group 1 (the partner-length work)

**18 blocking checks, all passing; 5 pending dependencies; exit 2.**

| check | asserts |
|---|---|
| B1 | every input artefact exists (12 named files) — a short-circuit: if any is absent the gate reports and returns 1 immediately |
| B2 | every chain-B construct in `g1_systems.csv` resolves to a row in `g1_partner_registry.tsv` |
| B3 | every held construct carries a full 64-hex sha256 |
| B4 | no system dispatches a construct whose bytes are not held |
| B5 | every system row resolves chain B to a numeric length |
| B6 | no two cells within one arm are the same molecule (two construct keys → identical bytes) |
| B7 | every row declares a partner-MSA and a receptor-MSA condition |
| B8 | MSA-free on the partner chain is the primary condition |
| B9 | the frozen primary panel is one receptor per cluster, overrides declared, no chimeric-reference receptor |
| B10 | `R6a_da5` agrees byte-for-byte between `seq_rungs.tsv` and `seq_a5null.tsv` |
| B11 | the per-row recording spec carries the load-bearing columns |
| B12 | every engineered-α5-reference receptor is carried explicitly |
| B13 | every cognate row resolves or names its three options |
| B14 | every cognate row carries its evidence class |
| B15 | every α5-null construct comes from `seq_a5null.tsv`, one generator |
| B16 | every row carries **both** the supplied-partner family and the reference tip, never one without the other |
| B17 | every Block-B reversal supplies a natively-represented Gα family (3 of 4 have structural evidence; B1B1U5 is closed by D-H) |
| B18 | every arm in `g1_systems.csv` has a line item in `matrix_cost.py` — 21 arms costed, `matrix_cost` declares 41 ids |

```
$ python3 redo/gates/g1_preflight.py --selftest
  ok   B1 … B18   (18 lines, every one "rc=1, B<n> fired=True")
all blocking checks proved
```

> **GAP — the extension-filter bug is still live here.** `g1_preflight.py:493` stages
> the planted copy with a hand-written filter:
>
> ```python
> for f in os.listdir(real):
>     if f.endswith((".tsv", ".csv", ".md")):
>         shutil.copy(os.path.join(real, f), tmp)
> ```
>
> That drops **5 of the 65 inputs** from every planted copy —
> `drule_rejections.tsv.gz`, `g0_selftest.txt`, `p7_confidence_separation.json`,
> `seqrec_canonical.fasta`, `seqrec_trimmed.fasta`. It happens to be harmless today
> because B1–B18 read none of those five, but it is precisely the idiom that
> *"recurred twice the same day"* per `CLAUDE.md`, and `g2_preflight.py` already
> carries the fix. `g1_preflight.py` also has **no reproduction assertion** and **no
> "the plant changed bytes" assertion**, so a plant that silently failed to apply
> would score as a MISS with no explanation rather than as `THE PLANT DID NOT APPLY`.
> The harness additionally mutates the module-level `INPUTS` global and runs in-process.

#### `g2_preflight.py` — dispatch readiness for Group 2 (the ligand arm)

Added 2026-09-12. Same contract as g1. **15 blocking checks, all passing; 7 pending;
exit 2.** Its organising rule is stated in the docstring: *a missing input FAILS, it
does not skip* — `drule_selected.tsv` is in the `NEED` list for exactly this reason,
because `g2_systems.csv`'s decoy cells are resolved against it and a gate tolerating
its absence would be checking those cells against nothing.

| check | asserts |
|---|---|
| G-1 | every input artefact exists (8 named files, including `drule_selected.tsv`) |
| G-2 | no T2 or T3 row is pooled with T1 (D-2026-09-12-f: at 2 and 7 clusters neither can carry the headline contrast) |
| G-3 | every enacted ligand resolves to a row in the enumeration |
| G-4 | no inverse agonist is recorded as a neutral antagonist |
| G-5 | no blocked receptor carries a dispatchable row |
| G-6 | a resolved decoy cell names exactly three accepted decoys, three distinct InChIKeys, and dispatches |
| G-7 | every receptor set is exactly the tier table's membership |
| G-8 | no READY row carries an unresolved chain B or ligand |
| G-9 | every arm is completely crossed over its partner axis |
| G-10 | every prediction count reproduces from backbones × n |
| G-11 | every cognate row runs the partner MSA-free, every apo row n/a |
| G-12 | a decoy-unavailable receptor is blocked at zero predictions and carries its **own** recorded reason, verbatim |
| G-13 | the receptors with a resolved decoy are exactly those the selection accepted, **in both directions** |
| G-14 | every decoy row carries the `EXPLORATORY_MISSED_PREREG_CLUSTER_BAR` marker in `ligand_flag` and the deviation arithmetic in `note` |
| G-15 | the C7 arm is present and READY — the ligand-free 2×2 has not shrunk |

```
$ python3 redo/gates/g2_preflight.py --selftest
  ok   G-1 … G-12, G-13a, G-13b, G-14, G-15
16 plants over 15 blocking checks proved
```

G-13 gets **two** plants because its identity has two directions: it must fire both
when a refused receptor acquires a decoy and when a passing receptor's arm goes
missing, and one plant can only ever show one of those.

> **DISAGREEMENT.** `CLAUDE.md` records this gate as *"14 checks, 15 plants"*. It is
> **15 checks, 16 plants**.

`g2_preflight.py`'s harness is the reference implementation of the staging fix and
should be copied when the others are repaired:

```python
want = {f for f in os.listdir(INPUTS)
        if os.path.isfile(os.path.join(INPUTS, f)) and not f.startswith(".")}
for f in want: shutil.copy(os.path.join(INPUTS, f), tmp)
assert set(os.listdir(tmp)) == want, "staging did not reproduce inputs/"
before = open(os.path.join(tmp, fn), "rb").read()
corrupt(os.path.join(tmp, fn))
after  = open(p, "rb").read() if os.path.exists(p) else None
...
good = rc == 1 and fired and (after != before)   # the plant must have CHANGED BYTES
```

Every regular file, not an extension list; an assertion that the staging reproduced
the directory; and an assertion that the plant actually changed bytes, reported as
`THE PLANT DID NOT APPLY` when it did not.

---

### 6. The content gates

#### `ligands.py` — the curated ligand table

**10 checks, all passing; 10 plants, all firing.** The gate exists because the frozen
campaign measured its own curation-error rate on memory-sourced SMILES at **40–46%**,
and because the error that put carazolol in this table as a *neutral antagonist* —
when GPCRdb calls it an *inverse agonist* — was made on 2026-09-12 and caught by a
check, not by reading.

| check | asserts | value today |
|---|---|---|
| L-1 | the curated ligand table is present — **a missing input FAILS, it does not skip** | `ligand_set_redo.tsv` |
| L-2 | every enacted pick traces to exactly one candidate row | 16 picks all resolve |
| L-3 | no enacted role disagrees with GPCRdb's own `function_raw` label | 16 picks, every role matches |
| L-4 | every enacted SMILES parses, and no receptor's pair is one molecule | 16 parse, 7 receptors chemically distinct |
| L-5 | every blocked receptor says why, in the table itself | 1 blocked: PD2R2 |
| L-6 | no T1 pick supplies a separate polymer chain | 38 T1 receptors, both arms chain-free |
| L-7 | every pick's species matches the panel receptor's organism | no cross-species pick |
| L-8 | no allosteric (PAM/NAM) ligand was picked | 34 allosteric records skipped |
| L-9 | any pair sharing a CCD is flagged to key by InChIKey | 1 receptor flagged: OPSD |
| L-10 | every CCD-sourced pick matches RCSB; isomer mismatches are flagged | 10 verified, 2 isomer mismatches flagged, 4 n/a |

The role vocabulary is pinned in the source: `full_agonist → {agonist}`,
`neutral_antagonist → {antagonist}`, `inverse_agonist → {inverse agonist}` — with the
comment that an inverse agonist is an admissible off-state ligand *recorded as its own
role and never relabelled a neutral antagonist*.

> **DISAGREEMENT.** `DECISIONS.md:514` says *"`ligands.py`, 5 checks, each proved by
> planting"*. It is **10 checks, 10 plants**.

#### `drule.py` — the decoy rule

The largest gate: 1,145 lines, **26 checks, 26 plants, all firing**, 206 s for the
self-test. D-1…D-6 cover the target mapping and the candidate pool; D-7…D-26 cover the
selection.

| check | asserts | value today |
|---|---|---|
| D-1 | the target mapping is present and names ONE ChEMBL release | 64 rows, `ChEMBL_37` |
| D-2 | every panel receptor has a row, resolved or not | 64 receptors |
| D-3 | unresolved receptors are recorded with an empty target, not dropped | 1 unresolved: B1B1U5 |
| D-4 | no accession maps to more than one SINGLE PROTEIN target | every resolved accession 1:1 |
| D-5 | every exclusion names a molecule in the pool AND the axis that excluded it | **120,973 molecules, 363,367 exclusions** |
| D-6 | every pool row records the release, its digest and the scope | `ChEMBL_37`, `within_panel` |
| D-7 | every receptor carries exactly *k* decoys or a NAMED refusal at zero | 16 receptors: 11 with 3, 5 decoy-unavailable |
| D-8 | **the B1B1U5 trap** — a receptor with no resolved ChEMBL target acquires no decoy, refused on the ground that eligibility is *unestablishable*, because "no exclusion rows" is not "nothing is excluded" | B1B1U5 refused |
| D-9 | every accepted decoy is in the pool AND carries no exclusion row for its own receptor | 33 accepted, all eligible |
| D-10 | every drawn decoy records the seed, and the seed recomputes from the receptor | `draw_seed 20260912`, all 33 reproduce |
| D-11 | every rejection names axes from the declared vocabulary, a deterministic first axis, no overlap with accepted | **1,719,908 rejections** over 15 receptors, 9 axes |
| D-12 | every accepted decoy still passes all eight axes and the Tanimoto screen **on recomputation from SMILES** | 33 recomputed, no drift |
| D-13 | the pH 7.4 protonation rule validates; six aminergic full agonists come out +1 | 35 molecules at the expected charge |
| D-14 | accepted + rejected == eligible, for every receptor — no candidate silently dropped | conserved over 15 receptors |
| D-15 | every row records the enacted cLogP window and diversity cap, and the run used ONE of each | ±1.0 log units, Tanimoto cap 0.3 |
| D-16 | the *k* decoys of a receptor are dissimilar to **each other**, not only to the real ligands | worst within-draw pair **T = 0.274** |
| D-17 | the rule's parameters are the frozen ones, on every row | window 1.0, cap 0.3, k 3, seed 20260912 |
| D-18 | the pool came from the frozen ChEMBL download, **by digest not by name** | — |
| D-19 | exactly 11 receptors / 11 clusters accepted and 5 refused, and exactly which | — |
| D-20 | B1B1U5's refusal class is frozen **separately** from the other four | — |
| D-21 | 33 accepted decoys, no molecule reused across receptors | — |
| D-22 | the SET of 33 ChEMBL ids hashes to the frozen digest | — |
| D-23 | the SET of 33 InChIKeys hashes to the frozen digest | — |
| D-24 | the MDE recomputed from the observed cluster count is the frozen one | k=11 → 1.218/√11 = **0.367** vs **0.352** at the pre-registered k=12, **+4.4%** |
| D-25 | the frozen selection reaches `g2_systems.csv` at the frozen cell counts | 33 READY / 15 BLOCKED decoy cells |
| D-26 | each of the 33 decoys is frozen **to its receptor**, not merely to the panel | — |

Two design points to carry into any future gate:

- **The two set-hashes (D-22, D-23) are the load-bearing entries.** Every *count* in
  this gate survives a re-run that silently draws a different molecule for one
  receptor; the hashes do not. They are SHA-256 over the `|`-joined *sorted* values,
  so they are invariant to row order and to which receptor a molecule was drawn for —
  which is the point: they pin molecular identity and nothing else. **D-26 exists
  because both set-hashes still match under a permutation** that gives the same 33
  molecules to the wrong receptors; its plant is exactly that permutation.
- **MDE is deliberately not frozen as a constant.** D-24 recomputes `1.218/√k` from
  the observed cluster count and compares. A number frozen into a CSV cell drifts away
  from the table that produced it — `MAP §2.4` records the frozen campaign's ADRB2
  decoy notes still naming a ligand replaced on 2026-09-04, with nothing noticing.

> **DISAGREEMENT.** `DECISIONS.md:724` says *"`drule.py` is 16 checks, 16 proved by
> planting"*; `CLAUDE.md` says *"16+ checks"*. `PLAN.md:246` says *"26 checks, 26
> proved"* and is correct. It is **26 / 26**.

#### `seqrec_verify.py` — every number quoted in `SEQ_RECEPTORS.md`

**60 checks, 60 passing.** Same role as `analysis/block_<x>/verify_claims.py`: the
document is allowed to go stale, this is not. Each check prints its own name, its
recomputed value and the value the document asserts. It reads only the `seqrec_*`
companions plus `panel_systems.csv`.

Its `--plant` flag is **not** one-plant-per-check. It is a **single** defect —
`core = core[:-1]`, dropping one receptor from the 64-member core roster — and the
harness exits 0 because it *expects* failures. Today it fires **7** of the 60 checks:

```
$ python3 redo/gates/seqrec_verify.py --plant
[FAIL] core receptors                                       got 63   want 64
[FAIL] core with 7 UniProt TM helices                       got 63   want 64
[FAIL] core with a signal peptide                           got [5 slugs]  want [6 slugs]
[FAIL] core entries with >1 isoform                         got 28   want 29
[FAIL] core receptors never dispatched by Block A or B      got 23   want 24
[FAIL] post-TM7 residues in the core, total                 got 3561 want 3644
[FAIL] roster agrees with panel_systems.csv                 got ['planted'] want [64 slugs]
53/60 checks pass
(--plant expects failures; a clean run here would mean the checks are not reading what they claim to)
```

**53 of 60 checks have never been exercised by a plant.** The flag proves the roster
plumbing reads what it says it reads; it does not prove the other 53.

`verify.sh` carries a comment explaining why this gate is wired in: it was *not run
here* until 2026-09-13, so it sat at 53/54 — one failing check — while `verify.sh`
printed `ALL CHECKS PASSED`. A gate nothing runs is a gate nobody can rely on.

#### `panel_verify.py` — every checkable number in `PANEL.md`

**92 checks in 13 sections, all passing. No self-test of any kind, and it is the one
gate `verify.sh` does not run.**

Sections, in output order: `frozen inputs`, `§1 the universe`, `§2 ConfoRNets
overlap`, `§7 clusters`, `§8 cutoffs`, `§9 axis coverage in the pinned reference set`,
`§10 ligands`, `§11 membership deltas`, `§3 obsolete entry`, `§14 strict-ConfoRNets
filter columns`, `D-H: the spider Gαq1 segment is derivable from RCSB alone`, `§6 note:
receptors with a non-canonical α5 tip`, `no spec document contradicts PANEL.md §6.1 on
a reference`.

The pattern is `check(label, got, want)` where `got` is recomputed from a source file
and `want` is a literal in the gate. It pins its three frozen inputs by digest prefix
first (`gpcrdb_structures.json` → `77e0b077`, `lee2026confornets_gpcr_references.csv`
→ `bd08abab`, `reference_set.blockb_pinned.csv` → `6ee2cad8`), so a moved snapshot
fails loudly rather than shifting every downstream count.

Unlike the other gates it also **parses the spec document itself** (`PANEL.md §6.1`
into slug → (active_pdb, inactive_pdb); `§6`'s blockquoted slug list) and cross-checks
prose against the census — the last section scans every spec document for sentences
claiming Rule R selects what §6.1 does not, and reports 13 sentences that sit in
paragraphs marked `{ref-history}` or `{ref-alt}` and are therefore read as record, not
claim.

#### `run_receipt.py` — the one the old campaign never had

**4 checks per run. Zero runs exist, so it has never executed a single one.**

```
$ ls redo/runs/
README.md
$ python3 redo/gates/run_receipt.py
  no runs yet — nothing to check       (exit 0)
```

Finding F-9 is its reason for existing: **nothing in the delivered pipeline compared
output to input.** Not sequence, not chain count, not seed-used against
seed-requested, not MSA depth. `ok = exit_code == 0 and len(produced) > 0`, so a
monomer returned where a receptor + Gα dimer was requested passed every existing check.

| check | the equality it asserts | columns it needs in `rows.csv` |
|---|---|---|
| R1 | requested chain count == returned chain count | `n_chains_requested`, `n_chains_returned` |
| R2 | partner identity dispatched == partner identity returned | `partner_requested`, `partner_returned` |
| R3 | `seed_used` == `seed_requested` | `seed_requested`, `seed_used` |
| R4 | observed partner MSA depth == the depth the arm declares | `partner_msa_depth_observed` in `rows.csv`; `partner_msa_depth_expected` in `manifest.json` |

Each is an equality between something sent and something that came back. None needs a
model, a threshold or a judgement call, so none can drift into an opinion. R4 is the
fourth because F-5 made the alignment regime a designed quantity — the ladder needs
depth 1 at every rung.

**The rule this gate enforces about itself: a missing column is a FAILURE, not a
skip.** The `need()` helper returns `None` when a column is absent, and every branch
then appends to `bad`, not to `ok`:

```
R1 cannot run — rows.csv has no chain-count columns
R4 cannot run — no partner_msa_depth_observed column
               (F-6: the delivered campaign recorded no MSA metadata at all)
```

`layout.py` L5/L6 check that a run has the right *files* and that its declared input
hashes are ones we hold; that is bookkeeping. This checks the *content*. Runs are
read-only once landed, so a failure here is never repaired in place — the run is
re-requested, or accepted with the defect recorded.

---

### 7. Self-tests inside the generators

Nine files in `redo/build/` carry their own proof mechanism. These are not gates and
`verify.sh` does not run them, but they are how a generator's *logic* is checked
rather than its output.

| generator | flag | what it printed today |
|---|---|---|
| `drule_select.py` | `--selftest` | `23/23 checks pass` — includes "the rejection table gzips DETERMINISTICALLY (two writes, same sha256 `e301b297781f`)" and the B1B1U5 trap |
| `run_registry.py` | `--selftest` | `12/12 checks proved` |
| `drule_pool.py` | `--selftest` | `6/6 rule branches behave as specified, across BOTH scopes` |
| `coupling_summary.py` | `--selftest` | `SELFTEST PASSED: all 4 checks fired on a planted defect` |
| `coupling_cognate_map.py` | `--selftest` | `SELFTEST PASSED: every branch of R-COG fired on a planted input`; 590 cached entities agree |
| `seqrec_refs.py` | `--selftest` | `SELFTEST PASS` |
| `seqrec_trim.py` | `--selftest` | `SELFTEST PASS` |
| `seqrec_icl3_audit.py` | `--selftest` | `SELFTEST PASS` (ADRB2 ICL3 = 221–274) |
| `g0_measure_axes.py` | `--selftest` | 16 axis comparisons: **14 MATCH, 2 MISMATCH** (5G53), plus 8 anchor-position rows all AGREE against the pinned reference set |

Two generators have a **regenerate-and-diff** mode, which is stronger than a self-test
because it proves the committed artefact *is* what the code produces:

```
$ python3 redo/build/g1_recording_spec.py --check
OK  49 columns, file matches the generator        (exit 0)

$ python3 redo/build/g1_midrungs.py --check       (exit 0)
```

`seq_a5null.py` has `--verify-only` / `--no-verify`, and refuses to emit a table it
cannot reproduce: *"ABORTING: refusing to emit a table the generator cannot
reproduce."*

**Only 13 of the 44 files in `redo/build/` have any check mode at all.** Fifteen of
the 44 reach the network (RCSB, GPCRdb, UniProt, ChEMBL), so "regenerate and diff" is
not universally available — which is why F-21 proposes recording input digests instead.

---

### 8. `verify.sh` — what the repository-wide self-check does and does not cover

`./verify.sh` from the repository root. It runs git checks, the corpus check, the TeX
pin, the manuscript build, Block A row counts, then the redo campaign:

```
redo/gates/seqrec_verify.py     redo/gates/layout.py       redo/build/manifest.py --check
redo/gates/run_receipt.py       redo/gates/ligands.py      redo/gates/drule.py
redo/gates/g0_preflight.py      redo/gates/g1_preflight.py redo/gates/g2_preflight.py
```

**Three things it does not do:**

1. **It never runs `panel_verify.py`.** That is 92 checks — the largest single block in
   the campaign — outside the repository self-check. `grep -c panel_verify verify.sh`
   returns **0**.
2. **It never runs any `--selftest`.** `grep -c selftest verify.sh` returns **0**. The
   proof layer is opt-in and manual. (`drule.py --selftest` takes 206 s, which is
   presumably why.)
3. **The corpus line cannot fail the run.** `verify.sh:26-27`:
   ```bash
   lit/corpus_check.sh >/dev/null 2>&1 && ok "corpus consistent" "OK" \
     || ok "corpus" "drift reported — run lit/corpus_check.sh"
   ```
   `ok()` on both branches, and only `bad()` sets `FAIL=1`. It prints `drift reported`
   and exits clean. That drift is the four deliberately-unread `refs.bib` entries and
   is expected — but do not read the line's *absence* as a passing corpus check.
   (`verify.sh:23`, the working-tree line, is the same shape and deliberately so.)

One thing it does well and worth copying: **every check count in the output is read
from the gate's own tally, never hard-coded in the script.** Two of these lines
carried hand-written counts and both had gone stale by 2026-09-12 — `ligands` said 5
against 10, `drule` said 6 against 14. The comment in the file names the failure class:
*a count in a label is a claim nobody re-derives.*

---

### 9. How to verify a specific claim — recipes

#### 9.1 Check a row count

CSV and TSV files here contain quoted fields with embedded newlines, so `wc -l` is
wrong. Use a CSV parser:

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper/redo
python3 - <<'PY'
import csv
for f, d in [("g1_systems.csv", ","), ("g2_systems.csv", ","),
             ("g1_partner_registry.tsv", "\t"), ("g0_calibration_structures.csv", ","),
             ("coupling_cognate_map.tsv", "\t"), ("panel_systems.csv", ",")]:
    rows = list(csv.DictReader(open("inputs/" + f, newline=""), delimiter=d))
    print(f"{f:34s} {len(rows):6d} data rows  {len(rows[0]):4d} cols")
PY
```

Output, 2026-09-14 — these are the authoritative row counts:

| file | data rows | columns | the spec says |
|---|---:|---:|---|
| `g1_systems.csv` | **2,039** | 36 | 2039 ✓ |
| `g2_systems.csv` | **350** | 47 | 350 ✓ |
| `g1_partner_registry.tsv` | **782** | 11 | 782 ✓ |
| `g0_calibration_structures.csv` | **1,357** | 26 | 1357 ✓ |
| `g0_measurements.csv` | **1,357** | 25 | one measurement row per structure ✓ |
| `coupling_cognate_map.tsv` | **64** | 37 | one per Class A panel receptor |
| `coupling_assignments.csv` | **64** | 27 | one per panel receptor |
| `panel_systems.csv` | **75** | 138 | the 64-receptor core sits inside 75 |
| `ligand_set_redo.tsv` | **17** | 24 | 16 enacted picks + 1 blocked (PD2R2) |
| `drule_selected.tsv` | **38** | 41 | 33 accepted decoys + 5 refusals |
| `g1_recording_spec.tsv` | **49** | 6 | 47 inherited + 2 added |

#### 9.2 Check a derived quantity, not just a count

Never accept a count where the claim is about a *design*. Example — the C7 2×2, which
`CLAUDE.md` describes as "98 READY ligand-free rows and 20 receptors / 19 clusters with
the complete 2×2":

```bash
python3 - <<'PY'
import csv, collections
r = list(csv.DictReader(open("redo/inputs/g2_systems.csv", newline="")))
ready = [x for x in r if x["dispatch_status"] == "READY"]
free  = [x for x in ready if x["ligand"] == "none"]
cells = collections.defaultdict(set)
for x in ready:
    lig = x["ligand"] if x["ligand"] == "none" else x["ligand_role_actual"]
    cells[(x["receptor_slug"], x["receptor_cluster"])].add((x["partner_level"], lig))
want = {("apo","none"),("cognate","none"),("apo","full_agonist"),("cognate","full_agonist")}
full = [k for k, v in cells.items() if want <= v]
print("READY rows                 :", len(ready))
print("READY ligand-free rows     :", len(free))
print("receptors with the full 2x2:", len(full))
print("distinct paralog clusters  :", len({c for _, c in full}))
print("interaction MDE at that k  :", round(1.218 / len({c for _, c in full})**0.5, 3))
PY
```

```
READY rows                 : 313
READY ligand-free rows     : 98
receptors with the full 2x2: 20
distinct paralog clusters  : 19
interaction MDE at that k  : 0.279
```

All four re-derive. `dispatch_status` over all 350 rows: **313 READY**, 15
`BLOCKED_DECOY_UNAVAILABLE`, 12 `BLOCKED_UNRESOLVED_UNCURATED`, 8
`BLOCKED_UNRESOLVED_CHAIN_NO_SEQUENCE`, 2 `BLOCKED_LIGAND_IDENTITY`.

#### 9.3 Check a sha256

```bash
cd /Users/aditya/Documents/tools/Novartis_projects/paper
## one file, by hand
shasum -a 256 redo/inputs/g1_systems.csv
grep -P '^g1_systems\.csv\t' redo/inputs/MANIFEST.tsv | cut -f2

## all 65 at once, with the verdict
python3 redo/gates/layout.py | grep L3
## PASS  L3  every generated input matches its recorded hash  67 files, all match

## or, equivalently, including the bytes and generator columns
python3 redo/build/manifest.py --check ; echo "exit=$?"    # 0 = in sync
```

`g1_systems.csv` today: `debdd5bec4192ae1871faa0b238383f4fa6bcc32d07bd505df6886e9528ef0e3`,
which is exactly the digest in `MANIFEST.tsv`.

#### 9.4 Re-run a generator and confirm it reproduces its own output byte-for-byte

**Never run a generator against the real tree** — `redo/inputs/` is code-only and a
regeneration that is not restamped trips L3. Copy the tree first:

```bash
SCRATCH=$(mktemp -d)
cp -R /Users/aditya/Documents/tools/Novartis_projects/paper/redo "$SCRATCH/redo"
chmod -R u+w "$SCRATCH"
cd "$SCRATCH"
python3 redo/build/g1_systems.py >/dev/null
diff redo/inputs/g1_systems.csv \
     /Users/aditya/Documents/tools/Novartis_projects/paper/redo/inputs/g1_systems.csv \
  && echo "IDENTICAL"
```

This works because `redo/paths.py` derives every path from its own location, so a
generator run inside the copy writes inside the copy. **Result today:** `IDENTICAL`,
and the recomputed sha256 matches the manifest digest exactly. The generator's own
stderr summary reconciles too: `TOTAL(enumerated) 2039 rows, 74,960 pooled
predictions, 212,920 per-cell predictions`.

The same procedure reproduces `g2_systems.csv` byte-for-byte. `manifest.py` run inside
the copy produces a `MANIFEST.tsv` identical to the committed one, and prints its own
tally: `MANIFEST.tsv: 65 files (49 attributed, 1 ambiguous, 15 unattributed)`.

Two shortcuts that need no copy, because they regenerate in memory and only diff:

```bash
python3 redo/build/manifest.py --check            # the whole manifest
python3 redo/build/g1_recording_spec.py --check   # OK  49 columns, file matches
python3 redo/build/g1_midrungs.py --check
```

#### 9.5 Prove a check actually fires before trusting it

```bash
python3 redo/gates/layout.py --selftest        # 7 plants against L2         0.1 s
python3 redo/gates/layout.py --selftest-all    # 7 plants, L1 and L3-L8      4.2 s
python3 redo/gates/ligands.py --selftest       # 10/10                       0.4 s
python3 redo/gates/g0_preflight.py --selftest  # 12 plants over 13 checks    3.6 s
python3 redo/gates/g1_preflight.py --selftest  # 18/18                       1.6 s
python3 redo/gates/g2_preflight.py --selftest  # 16 plants over 15 checks    0.8 s
python3 redo/gates/drule.py --selftest         # 26/26                       206 s
python3 redo/gates/seqrec_verify.py --plant    # one plant, 7 of 60 fire     1.6 s
```

Or plant one by hand, in a copy, and watch it fire:

```bash
SCRATCH=$(mktemp -d); cp -R .../redo "$SCRATCH/redo"; chmod -R u+w "$SCRATCH"
printf 'HAND_EDITED\n' >> "$SCRATCH/redo/inputs/ligand_tiers.tsv"
python3 "$SCRATCH/redo/gates/layout.py"
##   FAIL  L3  every generated input matches its recorded hash
##             hand-edited or regenerated without restamping: ['ligand_tiers.tsv']
##   LAYOUT VIOLATED -- 2 check(s) failed.
python3 "$SCRATCH/redo/build/manifest.py" --check
##   MANIFEST.tsv is stale -- run: python3 redo/build/manifest.py     (exit 1)
```

#### 9.6 Check a threshold

The state-readout thresholds are **not** stored anywhere in `redo/`. They live in the
Block A drop, one value per row:

```bash
python3 -c "
import csv, collections
r = list(csv.DictReader(open('data/block_a/01_rows/block_a_rows.csv')))
print(len(r), 'rows')
for c in ('threshold_npxxy_used','threshold_tilt_used'):
    print(c, collections.Counter(x[c] for x in r).most_common())"
```

```
9490 rows
threshold_npxxy_used [('9.08', 9490)]
threshold_tilt_used  [('14.932', 9490)]
```

Both are constant across all 9,490 Block A rows. `g0_preflight.py` G0-10 is the only
redo gate that reads them (it asserts the class F defect at `14.932`), and
`matrix_power.py` is the only other file under `redo/` that mentions either.

---

### 10. What is NOT guarded — where a wrong number could still get through

Ordered by how easily a wrong number reaches a sentence.

| # | gap | evidence | consequence |
|---|---|---|---|
| **1** | **Staleness against upstream inputs (F-21, open).** No guard compares a generated input against the *current* hashes of the files its generator consumed. | `manifest.py --check` passed throughout the `run_registry.tsv` incident and was correct to | A regenerated `g2_systems.csv` and a stale `run_registry.tsv` coexist, both pass L3, and the derived count is wrong. This has already happened once and produced a wrong number in conversation (30 experiments where there were 27). |
| **2** | **A file created by hand and then stamped (F-22, open).** L3 compares a file to its *own* digest, taken from the hand-made bytes. | **6 of 65 inputs have no writer anywhere in the repository**: `panel_reference_qc.csv` (351 KB), `panel_uniprot.tsv`, `panel_gpcrdb_degree.csv` (130 KB), `panel_gpcrdb_constructs.csv`, `g0_pilot_measurements.csv`, `g0_selftest.txt` | A typo in a hand-made input is permanent and invisible. `g0_selftest.txt` is read by G0-11, i.e. one gate's evidence is a hand-made file. |
| **3** | **`run_receipt.py` has never executed a single check.** Zero run directories exist; R1–R4 are unexercised code, and the gate has **no self-test**. | `ls redo/runs/` → `README.md` only | The one gate written specifically to catch the delivered pipeline's central defect (F-9) is unproven. Its behaviour on a real delivery is unknown. Write a fixture run directory and plant each of R1–R4 **before** the first delivery lands, not after. |
| **4** | **`panel_verify.py`: 92 checks, no self-test, not in `verify.sh`.** | `grep -c panel_verify verify.sh` → 0; no `--selftest`/`--plant` string in the file | The largest single check block in the campaign is both unproved and unrun by the repository self-check. A silent check looks exactly like a passing one. |
| **5** | **`seqrec_verify.py`: 53 of 60 checks unproved.** `--plant` is a single roster defect. | `--plant` fires 7 of 60 | A check reading the wrong column would report `[ok ]` forever. This gate already sat at 53/54 unnoticed for weeks because nothing ran it. |
| **6** | **`g0_preflight.py` G0-12 has no plant**, and the tally prints `12/12` over `len(PLANTS)`, not over the 13 blocking checks. | `PLANTS` list, `g0_preflight.py:329-367`; tally at `:397` | The gate's own summary line overstates its coverage. This is the exact failure class the gate family exists to catch. |
| **7** | **`g1_preflight.py`'s plant harness still uses a hand-written extension filter** (`.tsv`, `.csv`, `.md`), drops 5 of 65 inputs from every staged copy, and asserts neither that the staging reproduced `inputs/` nor that the plant changed bytes. | `g1_preflight.py:493`; the 5 files are `drule_rejections.tsv.gz`, `g0_selftest.txt`, `p7_confidence_separation.json`, `seqrec_canonical.fasta`, `seqrec_trimmed.fasta` | Harmless today because B1–B18 read none of them. The moment a B-check reads a `.fasta` or the `.gz`, its plant scores as fired for the wrong reason. `g2_preflight.py` already carries the fix; copy it. |
| **8** | **`verify.sh` runs no self-test and skips `panel_verify.py`.** | `grep -c selftest verify.sh` → 0 | `./verify.sh` printing `ALL CHECKS PASSED` says the gates *ran*, not that they *work*. |
| **9** | **The corpus line in `verify.sh` cannot fail the run** — `ok()` on both branches at `:26-27`. | source | `drift reported` prints and the run still exits 0. |
| **10** | **The main-effect MDE (0.189–0.242) is asserted nowhere in code.** Only `1.218` (the interaction constant) appears in `gates/` and `build/` — 8 occurrences across `g2_preflight.py`, `drule.py`, `g2_systems.py`. The main-effect figures live only in prose. | `grep -rn "0\.189\|0\.242" redo/` → only `spec/EXPERIMENT_GAPS_2026_09_14.md:43` and `spec/C7_PREREGISTRATION.md` | A power claim about a main effect has no gate behind it. D-24 recomputes the *interaction* MDE only. |
| **11** | **The state-readout thresholds are unpinned inside `redo/`.** 9.08 Å and 14.932 Å live in `data/block_a/01_rows/block_a_rows.csv` and are asserted by exactly one redo check (G0-10, and only the tilt one). | `grep -rl "14.932" redo/gates redo/build` → `g0_preflight.py`, `matrix_power.py` | If either threshold is ever revised, nothing in the redo's input layer fails. |
| **12** | **Nine generators write in idioms the attribution detector cannot see** (stdout redirection ×4, pandas `to_csv` ×2, a `P()` path helper ×2, an argparse attribute ×1). | §4 table above | These files *are* reproducible, but L8 counts them as unattributed, which dilutes the signal: the count of 15 conflates "has no generator" (6) with "has one the parser cannot see" (9). A reader acting on L8's number will over- or under-estimate the real debt depending on which way they guess. |
| **13** | **Ambiguous attribution is not distinguished from correct attribution by L8.** `coupling_refstructures.csv` names two generators; L8 checks only that both files *exist*. | `MANIFEST.tsv`, row `coupling_refstructures.csv` | Nothing says which of the two actually produced the bytes. |
| **14** | **No gate checks the spec documents' own internal counts**, except `panel_verify.py`'s last section (which covers `PANEL.md §6.1` only). | The six disagreements in §11 below were all found by hand | Prose counts drift silently. This is the `a-header-count-is-a-claim-nobody-checks` failure class, and it is live across `CLAUDE.md` and `DECISIONS.md`. |

**The single highest-value unbuilt check**, from the above: the F-21 input-digest
record. It is one change to `manifest.py` plus a declaration per generator, and it
closes gap 1 and most of gap 2 at once. `DECISIONS.md` F-21 records that the identical
fix is already proven in-house in `lit/` (`GAPS.md` was made generated, and
`corpus_check.sh` fails on divergence; it caught injected drift when tested).

---

### 11. Disagreements found between prose and data

Every row was re-derived from the file named. **The data wins.**

| # | document | what it says | what the data says | command |
|---|---|---|---|---|
| 1 | `CLAUDE.md` | "14 of 64 inputs name no generator" | **15 of 65** | `awk -F'\t' 'NR>1&&$4=="unattributed"' redo/inputs/MANIFEST.tsv \| wc -l`; `awk 'NR>1' redo/inputs/MANIFEST.tsv \| wc -l` |
| 2 | `layout.py` docstring (L8 comment), `DECISIONS.md` F-22 heading | "31 of 64 files are in that state today" | **15 of 65** | as above; `python3 redo/gates/layout.py \| grep L8` |
| 3 | `CLAUDE.md` | `g0_preflight.py --selftest` "12/12 checks" | gate has **13** blocking checks; harness has **12** plants; **G0-12 is unplanted** | `python3 redo/gates/g0_preflight.py \| grep -c 'PASS  G0-'` → 13; `grep -c '("G0-' redo/gates/g0_preflight.py` → 12 |
| 4 | `CLAUDE.md` | `g2_preflight.py` "14 checks, 15 plants" | **15 checks, 16 plants** | `python3 redo/gates/g2_preflight.py \| grep -c 'PASS  G-'`; `python3 redo/gates/g2_preflight.py --selftest \| tail -1` |
| 5 | `CLAUDE.md` | `drule.py` "16+ checks"; `DECISIONS.md:724` "16 checks, 16 proved" | **26 checks, 26 proved** (`PLAN.md:246` is correct) | `python3 redo/gates/drule.py \| tail -2` |
| 6 | `DECISIONS.md:514` | `ligands.py`, "5 checks, each proved by planting" | **10 checks, 10 plants** | `python3 redo/gates/ligands.py \| tail -2` |
| 7 | `CLAUDE.md` | `layout.py --selftest` "L2 (6 plants)"; `--selftest-all` "L1 and L3–L7 (6 plants)" | **7 plants each**, and `--selftest-all` covers **L1 and L3–L8** (L8 included) | `python3 redo/gates/layout.py --selftest \| tail -2`; `... --selftest-all \| tail -2` |
| 8 | `CLAUDE.md` | "`g1_recording_spec.tsv` … has no writer anywhere in `redo/build/`" | it has one: `build/g1_recording_spec.py`, and `--check` confirms the file matches | `grep g1_recording_spec redo/inputs/MANIFEST.tsv`; `python3 redo/build/g1_recording_spec.py --check` |
| 9 | `layout.py` check label L1 | "redo/ holds only its **eight** declared entries" | the detail line reports **9 entries**, and the `TOP` set has nine members (`README.md`, `paths.py`, and seven directories) | `python3 redo/gates/layout.py \| grep L1` |
| 10 | `layout.py` `selftest_all()` header | "=== layout guard self-test: L1 and **L3-L7**, planted ===" | it plants **L3–L8** — the footer line is right, the header is stale | `python3 redo/gates/layout.py --selftest-all \| head -3` |
| 11 | `CLAUDE.md` | C7 2×2 "(MDE 0.279)" | 0.279 is the **interaction** MDE at k=19. `spec/C7_PREREGISTRATION.md` corrected this on 2026-09-13: C7's primary contrast is a **main effect**, whose MDE at k=19 is **0.121–0.155** (cluster SD 0.189–0.242). 0.279 was conservative, so nothing was overclaimed — but it is the wrong constant for the contrast. | `sed -n '40,52p' redo/spec/C7_PREREGISTRATION.md`; the 2×2 itself re-derived in §9.2 |
| 12 | brief / `CATALOGUE.md` | "45 experiments E0.1–E9.3" | **45 headings**, but **46 distinct ids** are referenced. **E6.3 has no heading of its own** — it shares one with E6.2 (`### E6.2 / E6.3 — Ship the three Block D rows.csv…`). `CAMPAIGN.md:151` already records this: *"carries two experiments — so 46 experiments in 10 groups."* | `grep -oE '^#+ *E[0-9]+\.[0-9]+' redo/spec/CATALOGUE.md \| grep -oE 'E[0-9]+\.[0-9]+' \| sort -uV \| wc -l` → 45; same without the `^#+` anchor → 46; `comm` → E6.3 |

Nothing above changes a scientific conclusion. Items 3, 4, 5, 6 and 7 all understate
or misstate how much verification exists, and item 3 is the only one where a stated
coverage figure is **higher** than the real one.

---

# Part 12. Disagreements found while writing this document

**Every data section above was re-derived from the data files rather than copied from
prose, and a second independent pass re-derived the numbers again with its own
commands.** This part records what that turned up. It is here rather than silently
fixed because a specification that quietly absorbs its own errors teaches nobody where
to look next.

**None of these changes a scientific conclusion.** All of them are numbers a reader
would otherwise have trusted.

### What the second pass rejected

Two claims from the first pass did not reproduce and are corrected here:

1. **The C7 2×2 per-cell counts.** The claim was "36 rows in each of the four cells".
   Keyed on `partner_level`, the real counts are **36 / 36 / 52 / 52 = 176**, because
   `partner_level == cognate` covers **both** `R3_ct21` and `R7_full` (36 + 16). The
   144 figure is reachable only by restricting to
   `chain_b_construct in ('R0_apo','R3_ct21')`. **Both totals are right under a
   construct-keyed definition; the per-cell claim was wrong under the partner-keyed
   one that the pre-registration itself uses.**
2. **Catalogue arithmetic: 26 of 31, not 28 of 31.** Two further stated products fail
   against their own factors and were missed: Block A's "48 × 4 × 2 × 25 = 9,490"
   (the product is **9,600**) and Block C's "36 × 4 × 3 × 2 × 50 = 40,000" (the product
   is **43,200**). Both are reachable only if those numbers are read as delivered row
   counts rather than design products — a defensible reading the catalogue text does
   not signal.

Also corrected: the ligand-arm per-cell grain is **not** uniformly n=50. Of the 176
rows, **112 carry n=50 on four backbones and 64 are pilot rows at n=10 on Boltz-2
alone** (22,400 + 640 = 23,040). The `n_pooled` column *is* uniformly 10.

## From the receptors section

FOUR disagreements between spec prose and the frozen input files, plus one already-recorded correction.

1. **`COUPLING.md:1209-1211` undercounts CORE32 by two.** It tabulates `CORE32_Gs` = 5 (ADRB1, CCKAR, GPR52, NK1R, TSHR), `CORE32_Gio` = 21 and `CORE32_Gq11` = 2, summing to **28**. Recomputed from `g1_systems.csv` joined to `coupling_cognate_map.tsv`, CORE32 is **30 receptors: Gi/o 22, Gs 6, Gq/11 2**. The two missing are **AA2AR** (Gs, added by the declared override in `g1_panel_freeze.tsv:override_reason`) and **5HT5A** (Gi/o, the backfill for the serotonin cluster vacated by 5HT2A). `GROUP1_SYSTEMS.md:246` already flags half of this ("`CORE32_GS` is now 6"); the 5HT5A half is not flagged anywhere I found. COUPLING.md's table is stale, not wrong-at-the-time. Command: `python3 -c "import csv;from collections import Counter;cc={r['receptor_slug']:r for r in csv.DictReader(open('coupling_cognate_map.tsv'),delimiter='\t')};core=set(r['receptor_slug'] for r in csv.DictReader(open('g1_systems.csv')) if r['receptor_set'].startswith('CORE32('));print(len(core),Counter(cc[s]['cognate_family'] for s in core))"` -> `30 Counter({'Gi/o': 22, 'Gs': 6, 'Gq/11': 2})`.

2. **"MDE ... 0.189–0.242 for main effects" is a category error, and it is in the task brief, in `REDO_REFERENCE.md:48`, and in `EXPERIMENT_GAPS_2026_09_14.md:43`.** 0.189 and 0.242 are **cluster standard deviations** (`RUN_MATRIX.md:490,492`), not MDEs. The MDE is `2.80 × SD / √k`. Presenting them as MDEs makes the main-effect MDE independent of panel size, which it is not — a 6-receptor set and a 30-receptor set would get the same number. Re-derived: `2.80*0.189/√32 = 0.094` and `2.80*0.242/√32 = 0.120`, which is exactly what `RUN_MATRIX.md:490,492` tabulates in its own k=32 column, confirming the formula. `C7_PREREGISTRATION.md:43-52` corrected this same slip on 2026-09-13 and gives 0.121–0.155 at k=19; I reproduce that number exactly. I have written §3.3 with a separate, k-dependent main-effect MDE column and a note.

3. **`PANEL.md:894` and `PANEL.md:1057` say the panel has FOUR non-human receptors including "NTR1 (**rat**)".** The frozen panel has **three**: B1B1U5 (spider), OPRM (mouse), OPSD (bovine). `g1_receptors.tsv` and `g1_systems.csv` both give NTR1 `organism = Homo sapiens (Human)`, `uniprot = P30989`. Read in context, those two lines describe the **alternative strict-ConfoRNets panel** of §14, not the frozen Rule-P panel — §14.5's own comparison column labels it "strict". `PANEL.md:528` and `:621` give the correct 3 for the frozen panel. This is not an error in the data; it is a scope trap of exactly the "scope is asserted where it is most read" kind, because the "4" appears in a bare summary row that reads as global. Any sentence quoting "four non-human receptors" is describing a panel this campaign does not use. Command: `python3 -c "import csv;print([ (r['slug'],r['organism']) for r in csv.DictReader(open('g1_receptors.tsv'),delimiter='\t') if r['organism']!='Homo sapiens (Human)'])"` -> `[('B1B1U5','Hasarius adansoni'),('OPRM','Mus musculus (Mouse)'),('OPSD','Bos taurus (Bovine)')]`.

4. **`CLAUDE.md` says "14 of 64 inputs name no generator"; `MANIFEST.tsv` holds 65 rows and 15 unattributed.** Outside my domain (I found it while checking file provenance), and the project brief itself says 65 inputs, so `CLAUDE.md`'s 64 is the stale figure. Command: `python3 -c "import csv;from collections import Counter;m=list(csv.DictReader(open('MANIFEST.tsv'),delimiter='\t'));print(len(m),Counter(r['generator'] for r in m)['unattributed'])"` -> `65 15`.

NOT a disagreement, recorded for completeness: **`GROUP2_LIGANDS.md:329` states "'`g1_systems.py`'s CORE32 is 32 receptors.' It is **30**"** — that is a correction already made in the spec, and the data agrees with the corrected value. The label `CORE32(provisional)` still appears literally on all 1,500 CORE32 rows of `g1_systems.csv`, so the name will keep inviting the mistake.

Everything else I checked agreed: `REDO_REFERENCE.md`'s existing §3 figures (CORE32 30/29/1500, CORE32_GS 6/6/54, G10_SCAN 10/10/360, C1_REST 24/14/72, EXT_CHIMERA+REFCHIMERA 10 and 12 / 53 rows, species 1933/52/51/3) all reproduce exactly; `DECISIONS.md:268`'s "64 receptors, every one gclass = A, 32 core-32 provisional" reproduces exactly; `DECISIONS.md:23`'s "30 receptors / 29 clusters" reproduces exactly; `C7_PREREGISTRATION.md`'s "98 ligand-free rows READY, 20 receptors in 19 clusters" reproduces exactly; `GROUP1_SYSTEMS.md:282`'s "structure column on 13 of 64 receptors" reproduces exactly.

---

## From the constructs section

Five places where a spec document or a generator docstring states a count the data file contradicts. In every case I re-derived the number from the data file and the data wins.

1. **`redo/spec/GROUP1_SYSTEMS.md:605` says the registry holds "588 constructs".** The file holds **782 data rows**, of which **771 are `held=yes`** and **50 are distinct construct names** / **64 distinct (class, construct) pairs**. No reading of the file produces 588. The same document says **771** at `:29` and `:1305`, so it disagrees with itself. Command: `awk 'NR>1' g1_partner_registry.tsv | wc -l` → 782; `awk -F'\t' 'NR>1{print $8}' g1_partner_registry.tsv | sort | uniq -c` → 771 yes / 10 NO / 1 yes-but-mislabelled.

2. **`GROUP1_SYSTEMS.md:612` breaks `ga_rung` (261) down as "`seq_rungs.tsv` 112, `g1_midrungs.tsv` 80, `seq_a5null.tsv` 15".** The registry's own `source_table` column gives **`seq_a5null.tsv` 21**, not 15. 112 + 80 + 21 + 48 = 261, which is the class total the same row states; with 15 the arithmetic does not close. Command: `python3 -c "import csv;from collections import Counter;print(dict(Counter(r['source_table'] for r in csv.DictReader(open('g1_partner_registry.tsv'),delimiter='\t') if r['construct_class']=='ga_rung')))"`.

3. **The same class table is stale in two further places.** It lists **`not_dispatchable` = 5** ("`random_helix_40mer`, `arrestin_Ctail`, `DAMGO`, `Nb60` … `arrestin_FL`"); the file has **11** — the six `spidertip_*` rows were added later. And it **omits `species_matched_tip` (5 rows) entirely**, so the table enumerates 12 classes where the file has 13. The table's column sums to 771; the file sums to 782, and the 11-row difference is exactly these two omissions (6 + 5). Command: `awk -F'\t' 'NR>1{print $1}' g1_partner_registry.tsv | sort | uniq -c | sort -rn`.

4. **`GROUP1_SYSTEMS.md:613` says the 96 derived peptide controls were "built this session for Gi3".** They cover **two** families, **Gi3 (48 rows) and Go (48 rows)**. Command: `python3 -c "import csv;from collections import Counter;print(dict(Counter(r['family'] for r in csv.DictReader(open('g1_partner_registry.tsv'),delimiter='\t') if r['source_table']=='derived here via seq_controls.py')))"`.

5. **`redo/build/g1_partner_registry.py`'s own docstring (line 13) says `seq_a5null.tsv` holds "R6a/R6b/R6c full-subunit variants, 5 families".** The file holds **7 families** (G13, Gi1, Gi3, Go, Gq, Gs, Gt1), 21 rows. Command: `awk -F'\t' 'NR>1{print $2}' seq_a5null.tsv | sort -u`.

Two further things that are not outright contradictions but are *mislabels a reader will trip on*, both confirmed against the data:

6. **`redo/spec/REDO_REFERENCE.md:118` reports "Dispatched families across Group 1: Gi/o 1,517 rows, Gs 372, Gq/11 150."** Those counts include the **94 `R0_apo` rows, which have no chain B at all** — `supplied_partner_family` is a per-receptor annotation, not a statement that a partner was supplied. Excluding `R0_apo`: **Gi/o 1,455, Gs 354, Gq/11 136**.

7. **`g1_systems.csv:chain_b_len` for `R8_hetero` (761–805) is the sum of all three chains**, not the length of chain B. Chain B alone is the cognate `R7_full` (350–394); the +411 is Gβ1 (340) + Gγ2 (71), which sit in `chain_c`. A reader taking the column at face value will report an 805-residue chain B.

Two claims in the existing `REDO_REFERENCE.md` that I checked and that **hold**, worth recording so nobody re-litigates them: the per-construct row counts in its §4.1–§4.3 tables (R0 94, R1 90, R1b 30, R2 60, R2b 30, R2c 30, R3 154, R4 60, R5 90, R7 124, R8 30; controls 30/30/30/30/30/150/90/30; ala_scan 210; gi2gs 150; point mutants 42; full-subunit mutants 12; family swap 30) all reproduce exactly, and its "families held" column (17/16/17/16/16/17/17/17/17) is correct once you read it as the **union across `ga_rung` and `ga_rung_isoform`** — the 17th family is GoB, which exists only at R1/R2/R3/R4/R5/R7 and not at the 13/17/19-mers or any `M*` rung.

One presentational tension in the same document: it writes "The α5 helix is Asp368–Leu394, 27 residues" while calling `R4_a5helix` (26 residues, 369–394) "the α5 helix as crystallographers define it". Both boundaries are real and both are in the repo — 369–394 is CGN G.H5 and is what every `R4_a5helix` construct is; 368–394 is the Sunahara literature window, held once as `R4b_a5helix27` precisely so the choice is auditable — but the two sentences sit two rows apart in the same table without saying they are different conventions.

Finally, a data defect rather than a prose one: **`arrestin_FL`'s `sha256` field is the literal string `a0a09ab53dbc98a2...`** — a 16-hex prefix plus an ellipsis, not a hash. Preflight check **B3** tests only rows with `held == "yes"`, and this row is `yes-but-mislabelled`, so B3 does not fire on it. **B4** does keep it out of dispatch (zero `g1_systems.csv` rows reference it), so nothing is at risk today, but the field is a placeholder that no check validates.

---

## From the ligands section

FOUR disagreements found; none change a scientific conclusion, but all four are numbers a reader would otherwise trust.

1. **`GROUP2_LIGANDS.md` understates the gate by one check, in two places, and `CLAUDE.md` does too.**
   - `GROUP2_LIGANDS.md` header: "Gate: `redo/gates/g2_preflight.py`, **11 blocking checks**, each proved by planting the defect it catches."
   - `GROUP2_LIGANDS.md` §3.4 closing line: "**15 plants over 14 blocking checks**, all proved."
   - `paper/CLAUDE.md` self-test table: `g2_preflight.py` — "**14 checks, 15 plants**".
   - Live: `python3 redo/gates/g2_preflight.py` prints "**15 passed, 0 failed, 7 pending**"; `--selftest` prints "**16 plants over 15 blocking checks proved**". Fifteen `B()` calls exist in the file (G-1..G-15).
   The missing one is **G-15**, the C7-arm guard, added 2026-09-13 with the pre-registration. All three prose statements were correct when written and went stale the same way the repo's own notes warn about. Recommendation for REDO_REFERENCE.md: state 15 blocking checks / 16 plants, and say it was 14/15 before G-15 landed.

2. **The task brief I was given conflates a cluster SD with an MDE.** The brief says "MDE = 1.218/sqrt(k) for interactions; **0.189-0.242 for main effects**". Re-derived from `RUN_MATRIX.md:485-492` and `:503-520`: the MDE formula is **2.80 x SD / sqrt(k)**, 0.435 is the median *interaction* cluster SD (2.80 x 0.435 = 1.218), and **0.189 / 0.242 are the main-effect cluster SDs, not MDEs**. The main-effect MDE numerators are 2.80 x 0.189 = 0.529 and 2.80 x 0.242 = 0.678, giving **0.121-0.155 at k=19**, which is exactly what `C7_PREREGISTRATION.md` states after its 2026-09-13 correction. Quoting "0.189-0.242" as an MDE would overstate the detectable effect by a factor of 2.8. `C7_PREREGISTRATION.md` itself is correct; the brief is not.

3. **Gate G-15 still prints the interaction MDE for a main-effect contrast.** `g2_preflight.py:355` computes `mde = 1.218 / sqrt(len(c7_clusters))` and the passing line reads "MDE 0.279". That is the interaction figure, and `C7_PREREGISTRATION.md` §2 explicitly corrected C7's primary contrast to a main effect with MDE 0.121-0.155. The gate's guard logic (>=20 receptors / >=19 clusters / >=98 rows) is correct and is not affected; only the printed diagnostic carries the superseded constant. This is the same `compare-like-with-like` failure the pre-registration records, still live in the gate's own output. Not a defect I fixed (read-only session) -- flagging it.

4. **`ligand_tiers.tsv` (the census) and `g2_systems.csv` (the enacted dispatch) name DIFFERENT molecules for several receptors, and nothing records it.** Agonists differ on 6 receptors -- AGTR1 (census `TRV026`, enacted **angiotensin II**), CNR2 (census `CP55940`, enacted the HU-308-type `9GF`), DRD3 (census `rotigotine`, enacted **PD 128907**), AA2AR (census a phenyldiazenyl-adenosine, enacted **NECA**), LT4R1 and PD2R2 (formatting/refusal). Antagonists differ too: AA1R (census `DU172`, enacted **DPCPX**), CCKAR (census `lintitript`, enacted **devazepide**), EDNRB (census `K-8794`, enacted **bosentan**). The tier assignment is unaffected -- I checked `agonist_is_chain` / `antagonist_is_chain` against `ligand_is_chain` across every shared receptor and found **zero disagreements**, and tiering is defined on chain-ness, not identity. But a reader who treats `ligand_tiers.tsv` as the ligand roster will name the wrong molecule. REDO_REFERENCE.md should say plainly: `ligand_tiers.tsv` is the tier census (it answers "is this receptor eligible, and is each side a chain"), and `g2_systems.csv` + `ligand_set_redo.tsv` are the molecule of record.

MINOR, outside this domain but observed while verifying: `paper/CLAUDE.md` says "**14 of 64 inputs name no generator**". `inputs/MANIFEST.tsv` currently holds **65** data rows, of which **15** carry generator `unattributed` (`awk -F'\t' 'NR>1{print $4}' inputs/MANIFEST.tsv | sort | uniq -c`). CLAUDE.md is explicitly allowed to lag on corpus counts, so this is a note, not a defect.

EVERYTHING ELSE CHECKED REPRODUCED EXACTLY. In particular: the 98 / 20 / 19 C7 claim is correct in all three numbers and under both plausible definitions of the 2x2; `GROUP2_LIGANDS.md` §4's nine provenance counts (98/114/60/33/15/12/8/8/2) all match; §5's entire budget table including the 8,716 / 39,872 / 980 / 4,960 totals reproduces row by row; the MDE figures 0.314 (k=15), 0.295 (k=17), 0.249 (k=24), 0.367 (k=11), 0.352 (k=12) and the 4.4% loss all reproduce; "13 of the 16 curated T1 receptors" take a neutral antagonist and ADRB1/B1B1U5/OPSD take an inverse agonist; the "nine inherited T1 receptors" list matches D-2026-09-12-f exactly; `ligand_ccd_verify`'s "10 verified, 2 isomer mismatches, 4 chains n/a" matches; the frozen primary panel is 30 receptors / 29 clusters; and the decoy freeze (33 accepted / 11 receptors / 11 clusters, 5 refused in two classes) matches `drule_selected.tsv`.

---

## From the decoys section

SIX disagreements found between spec prose and the data files, plus two of my own checker bugs that I resolved.

1. **D-2026-09-12-h's three illustrative cross-activity molecules are STALE — none is in the frozen selection.** The decision record says: *"all three of LT4R1's decoys are S1PR1 ligands, CCKAR's `CHEMBL4279831` is a CNR1/CNR2 ligand, OPRD's `CHEMBL5915578` is an ACM4 ligand."* Re-derived from `drule_selected.tsv` + `drule_pool_exclusions.tsv`: LT4R1's three frozen decoys are `CHEMBL117031` (S1PR1), `CHEMBL119562` (S1PR1) and `CHEMBL4649582` (**PE2R4, not S1PR1**) — **two of three**, not three of three. `CHEMBL4279831` and `CHEMBL5915578` are in the pool but are **NOT among the frozen 33** and are drawn for nothing. D-2026-09-12-g's related figure, "6 of the first 27 cases", is **17 of 33** in the frozen selection. The substantive point ("non-binder" may not be used) is strengthened, not weakened — but the three named examples must be replaced before any of them reaches Methods. Command: see key_numbers entry "Decoy cross-activity inside the panel and inside the arm", plus `python3 -c "import csv; print([r['candidate_chembl_id'] for r in csv.DictReader(open('redo/inputs/drule_selected.tsv'),delimiter='\t') if r['receptor_slug']=='LT4R1' and r['decoy_status']=='accepted'])"`.

2. **"eleven of sixteen references have |cLogP| > 2.5" is nine of sixteen.** Stated in both `CAMPAIGN.md` §5.3 Amendment A and `DECISIONS.md` D-2026-09-12-g. Measured on the 16 `ref_smiles` values with `Crippen.MolLogP`: 9 exceed 2.5 (ADRB1 2.676, B1B1U5 6.251, CCKAR 7.902, CNR2 5.657, LPAR1 5.037, LT4R1 4.158, OPRD 5.558, OPSD 5.717, S1PR1 6.773). It is also 9 at >2.0 and 13 at >1.5, so no nearby threshold gives eleven. The argument is unaffected; the count is wrong.

3. **"±1.5 adds zero clusters while refusing 13% fewer candidates" — measured 11.6%.** `DECISIONS.md` D-2026-09-12-g. Re-derived: cLogP refuses 1,410,953 eligible pairs at ±1.0 and 1,247,463 at ±1.5, i.e. **11.6% fewer** (or 9.4 percentage points of the 1,721,751 eligible). No obvious alternative reading gives 13%. The "adds zero clusters" half reproduces exactly (11r/11c at both widths, every cap).

4. **`WHAT_IT_MEANS.md` §2(a) mislabels the four decoy numbers.** It says *"That comparison was of the apo→cognate SHIFT"*. Re-derived: (+0.011, −0.004, −0.016, −0.004) are the **cognate-arm LEVEL** difference (antagonist − decoy), which is exactly what `PER_BACKBONE.md` §3 says they are. The apo→cognate **shift** difference is (+0.010, −0.020, −0.023, +0.001) — different numbers. The §2 correction's conclusion (the shift is ligand-independent, the level is not) is supported by the continuous-readout evidence, but the sentence attributing those four numbers to the shift is wrong.

5. **`PER_BACKBONE.md`'s denominators silently include rows whose predicate cannot be computed.** Re-derived: 5,200 of 40,800 rows have no computable two-instrument call (EDNRA, EDNRB, GRPR on all three roles; HRH3 on antagonist and decoy; both opsins). The published table scores them as **not active** and keeps them in the denominator (n = 1,750/1,450/1,800). On computable rows only (1,600/1,250/1,600) the same contrast is **+0.038, +0.017, +0.005, +0.026** — all four positive, no longer "straddles zero, three of four negative". The headline conclusion (|Δ| ≤ 0.04 on all four backbones, decoy indistinguishable from antagonist) survives either way, but the "straddles zero" wording is an artefact of the convention and should not be repeated without the caveat.

6. **`F-26` §1 overstates the MSA gap-fraction range and conflates two different 0/40-style findings.** It says *"Chai decoy MSAs are 0/40 byte-identical to their cognate parents; Boltz and Protenix differ 6/6 by sha256; gap fraction at the α5-CT columns rises from ~36% to 47–70%."* Measured in `PHASE_1D_EXTENSION.md`: cognate gap fraction is **34.5–41.7%** and decoy is **36.9–70.3%** (Boltz decoy min is 36.9% at ACM1, well below 47%). Chai's "0/40" is its **uppercase-aligned** finding (the edit does not reach the model as aligned columns), not a byte-identity count; byte-identity was measured 0/6 on each of Boltz, OF3 and Protenix (0/18), and OF3 is omitted from F-26's sentence although it also differs 6/6.

STALE-BUT-NOT-WRONG (flagged so the reference document does not inherit them):
- `DECISIONS.md` D-2026-09-12-g says `gates/drule.py` is **"16 checks, 16 proved by planting"**. It is now **26 checks, 26 proved** (verified by running both). `PLAN.md` and `REDO_REFERENCE.md` already say 26.
- `DRULE_CHEMBL_SCOPE.md`'s STATUS box still says the pool is **not built** and the gate is **4 checks**. Both are superseded: the pool is built (120,973 molecules, ChEMBL_37, sha `33c20374…`) and the gate is 26.
- `CAMPAIGN.md` §5.3 still ends **"THE ARM DOES NOT RUN."** Superseded by D-2026-09-12-h: it runs as EXPLORATORY at k=11, 33 READY cells in `g2_systems.csv`.
- `DRULE_CHEMBL_SCOPE.md` deliverable 1 names the output `redo/inputs/drule_candidate_pool.tsv`; **that file does not exist**. The pool was stored normalised as `drule_pool_molecules.tsv` + `drule_pool_exclusions.tsv` (drule_pool.py's `OUT` constant is also still the dead name).
- `drule_select.py`'s docstring says the gzipped rejection table is **"7.9 MB"**; it is 7,157,345 bytes (6.83 MiB). DECISIONS' "6.8 MB" is right.
- `drule_select.py`'s docstring says `validate_charge_rule` covers "the six aminergic full agonists ... plus 27 further molecules" (33); `CHARGE_VALIDATION` holds **35** entries (6 flagged + 29).
- Read "all eight axes" as the property block only: `AXES` has **nine** entries because `tanimoto` shares the rejection vocabulary. The gate prints "vocabulary 9 axes".

TWO OF MY OWN CHECKER BUGS, resolved rather than reported as findings (per [[my-first-run-is-wrong-before-the-drop-is]]):
- My first `n_eligible` reconciliation showed 15 of 16 receptors "MISMATCH". Cause: I subtracted exclusions from the **full** 120,973-molecule pool. `n_eligible` is computed over the **parseable** pool — 133 molecules fail `DS.axes()` (130 have an empty SMILES). Re-derived correctly, all 16 reconcile exactly. The data was right; my derivation was not.
- My first pass at the cLogP sweep gave 10 receptors at ±0.5 / no cap where D-2026-09-12-g says 9. Cause: I counted "≥3 accepted" and skipped the draw. `diverse_draw`'s test is strict `<`, so even at cap = 1.0 a pair with identical Morgan fingerprints (T = 1.0) is refused — which is exactly OPSD's case at that window. With the draw applied my grid reproduces the published grid cell for cell.

---

## From the msa section

TEN disagreements found, four of them material.

1. MATERIAL — `redo/spec/MSA_SPEC.md:35`, a document SENT TO THE PIPELINE TEAM, gives the R6a_da5/R7_full partner MSA depth range as "8,474-9,203". Recomputed from `redo/protocol/received/rung_msa_depth.csv` on `note=="ok"` rows: R6a_da5 is 5,764 (G12) - 9,176 (Gi1) over 15 families, R7_full is 6,289 (G12) - 9,203 (Gi1) over 14 families. 8,474 is Gq's single R6a_da5 value (csv line 78), not a range bound. The lower bound is understated by ~2,700 rows and four families (G12, G13, Golf, G15) sit below 7,000 on both rungs. The argument is unaffected — everything is still three orders of magnitude above ct11 — but the number is wrong. `MSA_SUBSAMPLING.md` §2 already caught this on 2026-09-12 and MSA_SPEC.md has NOT been corrected.

2. MATERIAL — the same stale "8,474-9,203" appears a second time in `redo/spec/DECISIONS.md` F-5's measured table. That table additionally gives R3_ct21 as "47-581"; the true max is 582 (Golf). 581 is the Gs value.

3. MATERIAL — `redo/spec/MSA_SUBSAMPLING_REGIMES.md` §4 and §7 state that `g1_recording_spec.tsv` carries "47 columns" and that `pocket_ca_rmsd_active` / `pocket_ca_rmsd_inactive` are "Verified absent: I grepped all 47 column names". The file today carries 49 declared columns and BOTH pocket-RMSD columns are PRESENT as rows 48 and 49, added by `redo/build/g1_recording_spec.py` (which asserts the 47 inherited columns byte-for-byte and appends two). The review's most-emphasised blocking ask was satisfied after it was written; the same stale claim also sits in `FROZEN_VS_REDO.md:22`. The other ten blocking MSA columns (target/realised depth, depth_at_full, msa_target_unreached, msa_mode_label, the two sha256s, the two paired-slot columns, msa_source, the two subsample-draw columns, chai_msa_directory) are all genuinely still absent.

4. MATERIAL — `redo/inputs/g2_systems.csv` enumerates 22 rows in which the LIGAND is supplied as a polymer chain (`ligand_is_chain = 1`): 11 apo rows at n_chains=2 and 11 cognate rows at n_chains=3, covering C5AR1, SSR2, AGTR1, CCR2, EDNRB, MCHR1, NK1R, NPY1R, NTR1. The file declares only `partner_msa` and `receptor_msa`; the string `ligand_msa` appears NOWHERE in `redo/`; and gate G-11 checks only `partner_msa`. So the third chain's alignment regime is undeclared and unchecked — and the molecules include substance P (Block B measured depth 1) and endothelin-1 (depth 732), the exact two-and-a-half-order spread that `MSA_SPEC.md` §2 exists to eliminate on the partner axis. The risk is recorded in prose (`DECISIONS.md` D-C, `CAMPAIGN.md` D-C) but has not been converted into a column or a check.

5. `CLAUDE.md` (the project brief) states "14 of 64 inputs name no generator" and that `g1_recording_spec.tsv` "has no writer anywhere in `redo/build/`". `MANIFEST.tsv` has 65 rows and ZERO blank generators, and `redo/build/g1_recording_spec.py` exists. The surviving residual is different in kind: 16 manifest entries name a generator that is not a file in `redo/build/` — 15 of them the literal string `unattributed`, one a comma-separated pair (`coupling_assign.py,coupling_fetch.py`).

6. The naming defect, still unfixed: `g1_systems.csv` / `g2_systems.csv` label the primary partner condition `off`, while `MSA_SPEC.md` §3-§4 specifies it as query-only depth 1 and argues at length that *absent* and *query-only* are NOT equivalent on Boltz/OF3/Protenix — an omitted alignment may trigger a live fetch at full depth, "the inverse of the design". The value is still `off` in both input files and in both generators (`g1_systems.py:514`, `g2_systems.py:656`), and it has propagated into the recording spec (`partner_msa_mode` documented as "off (primary) / on (E1.9 contrast)").

7. `rung_msa_depth.csv`'s "unpaired depth" and the Block B Chai cache's "total MSA depth" are both called partner MSA depth and are NOT the same quantity: the rung series reproduces the Chai cache's UniRef90 count to within 1.7% (ratios 0.983-0.987 across Gs, Gi1, Gq, G13, Gt1) and is ~60% of its total. Gs full is 7,248 in one and 12,080 in the other. No document states this. Compounding it, nothing anywhere defines whether "depth" includes the query row: `rung_msa_depth.csv` reports 0 for ct11, the Chai cache reports 1 for an 11-mer, and `MSA_SPEC.md:151` asks for a check `partner_msa_depth == 1`. Two of those three conventions make that check fire on every correct row.

8. `MSA_SPEC.md:35` gives the R6a/R7 lengths as "368 / 394". Those are the Gs values; the families span 324-368 (R6a_da5) and 350-394 (R7_full).

9. `GATE_2_D3_SLOPES.md` names the worst cells as "n=1,250 at OF3×full and Chai×full". Recomputed: OF3×full is n=1,250, Chai×full is n=1,260 (Chai's smallest cell is depth 32 at n=1,270). Cosmetic — the 20-cell predicate-active table itself reproduces exactly from the row level.

10. `g1_preflight.py` B18's passing message reads "[21 arms, all costed]" but the number counts distinct `item` values, not `arm` values. `g1_systems.csv` has 21 distinct items and 23 distinct arms. Not an error in the check, but the number should not be quoted as an arm count — and the brief for this document says "23 arms", which is the one that matches `arm`.

NOT a disagreement, checked and confirmed: `receptor_msa` genuinely does not vary anywhere — one value across all 2,039 g1 rows and all 350 g2 rows; there is no depth arm in `redo/inputs/` at all, no `g5_systems.csv`, and no G5 entry in `SYSTEMS_LINK`, so `check_against_systems()` is structurally blind to the gap. G17 IS enumerated and costed (90 rows; matrix_cost 3,600/18,000 agreeing exactly with `g1_systems.csv`); it is only unbudgeted. The Block D depth × backbone table and the GATE-3 sub-angstrom fidelity figures both reproduce exactly from the 25,810 row-level records.

---

## From the experiments section

NINE disagreements found, all re-derived from the data files.

(1) "45 experiments" counts HEADINGS, not ids. `grep -cE '^### E[0-9]' redo/spec/CATALOGUE.md` = 45, but the distinct E-ids in those headings = 46, because E6.2 and E6.3 share one heading. `run_registry.tsv` has 45 rows and NO E6.3 row at all; its E6.2 title field is the truncated fragment "/ E6.3 — Ship the three Block D rows.csv and rows.tier3.v2.csv".

(2) PLAN.md's own correction #1 says "PLAN.md names ZERO experiment ids. A grep returns nothing." FALSE today: `grep -noE 'E[0-9]+\.[0-9]+' redo/spec/PLAN.md` returns 16 hits over 15 distinct ids, and one (E7.4) is at line 31, inside the §0a route table in the plan body — not in the corrections section. The narrower claim (the PILLAR sections name no ids) still holds.

(3) The task brief calls PLAN.md "the five-stage ordering". `grep -nE '^## ' redo/spec/PLAN.md` shows SIX pillars (Pillar 0 … Pillar 5) plus a separate ten-step route (steps 0–9) in §0a. Pillar 2 discharges ZERO catalogued experiments — the plan records this itself.

(4) THREE prediction counts in CATALOGUE.md do not reproduce from their own stated factors under the document's own 50-predictions-per-cell convention. (a) E1.5 "at 50 samples and 4 backbones it is 84,000" — derived 21*10*4*50 = 42,000, exactly 2x off. (b) E8.1 full three-way: catalogue 260,000, derived 2,080 cells * 50 = 104,000, 2.5x off. (c) E8.1 depth x partner all depths: catalogue "130,000 gross, ~104,000 new", derived 1,040 cells * 50 = 52,000 gross and 26,000 new after subtracting D3's existing 26,000. The same table's other rows (624 cells -> 31,200; 144 cells -> 7,200) DO use 50/cell, so the E8.1 table is internally inconsistent. A fourth row, "3 depths -> ~31,200 new", is the GROSS figure mislabelled as new (new would be ~15,600). 28 of 31 arithmetic checks pass.

(5) E8.1 is the only one of the 45 with no cost-class token in its Cost bullet ("Cost, with the affordable projections spelled out" followed by a table), so `run_registry.tsv`'s cost_class field for E8.1 is EMPTY. Its content is unambiguously `real`.

(6) The registry's `named_in_run_matrix` column under-reports by two. `grep -oE 'E[0-9]+\.[0-9]+' redo/spec/RUN_MATRIX.md | sort -u` returns 33 ids; the registry flags 30 as yes. The difference is E0.5 and E4.3 (present in RUN_MATRIX prose and its dependency graph at lines 423, 903, 923 but with no costed line item) plus E6.3 (no registry row). The column means "has a costed line item", not "is mentioned" — defensible, but the name invites the wrong reading.

(7) g2_systems.csv's antagonist level is not homogeneous, and E2.3 is less empty than the registry says. 19 rows requested as `ligand=antagonist` carry `ligand_role_actual=inverse_agonist` — ALL 19 inside E2.2, on receptors ADRB1 AGTR1 B1B1U5 NTR1 OPSD, 17 READY, 10 flagged `ccd_resolves_to_other_isomer` and 2 `source_row_role_disagrees_with_gpcrdb`. With E2.3's own 6 rows that is 25 enumerated inverse-agonist rows (23 READY), while E2.3's registry verdict is DIES and CATALOGUE.md's E2.3 text says there is "no partial and no inverse agonist". Both statements are true of BLOCK C; neither is true of the redo's own enumeration. Two consequences: an experiment marked DIES already has a usable arm sitting in the inputs, and E2.2's antagonist level mixes two pharmacological classes.

(8) CLAUDE.md's input-provenance figures are stale. It says "14 of 64 inputs name no generator" and that g1_recording_spec.tsv "has no writer anywhere in redo/build/". Today MANIFEST.tsv holds 65 rows of which 15 are `unattributed`, and redo/build/g1_recording_spec.py EXISTS (12,802 bytes) and is named as that file's generator in the manifest. CLAUDE.md itself states its corpus counts are allowed to lag.

(9) Recorded by the catalogue against itself, and verified: the document, its own header and RUN_MATRIX.md all said "33 experiments in 9 groups" until 2026-09-12. The body held 45 in 10 the whole time.

---

## From the gates section

TWELVE disagreements found, every one re-derived from the data file. In each case the data wins.

1. CLAUDE.md: "14 of 64 inputs name no generator". DATA: 15 of 65.
   `awk -F'\t' 'NR>1&&$4=="unattributed"' redo/inputs/MANIFEST.tsv | wc -l` -> 15; `awk 'NR>1' redo/inputs/MANIFEST.tsv | wc -l` -> 65.

2. redo/gates/layout.py's own L8 source comment AND DECISIONS.md F-22 heading: "31 of 64 files are in that state today". DATA: 15 of 65. (F-22's body says "now 14", also stale.) The gate PRINTS the live count on every run: `python3 redo/gates/layout.py | grep L8` -> "15 of 65 name NO generator".

3. CLAUDE.md gate table: g0_preflight.py "--selftest | yes | 12/12 checks". DATA: the gate has 13 blocking checks (G0-1..G0-13) and the harness has 12 plants. G0-12 (the gitignore check) HAS NO PLANT. The tally line at g0_preflight.py:397 prints `{len(PLANTS)-bad}/{len(PLANTS)}` -- a count over plants, not over checks -- so "12/12 blocking checks proved by planting" is literally false about the gate. This is the same "tally over plants reads as coverage of the gate" trap that layout.py's own docstring warns about, occurring inside g0_preflight.py.
   `python3 redo/gates/g0_preflight.py | grep -c 'PASS  G0-'` -> 13; `grep -c '("G0-' redo/gates/g0_preflight.py` -> 12.

4. CLAUDE.md: g2_preflight.py "14 checks, 15 plants". DATA: 15 checks, 16 plants.
   `python3 redo/gates/g2_preflight.py | grep -c 'PASS  G-'` -> 15; `--selftest | tail -1` -> "16 plants over 15 blocking checks proved".

5. CLAUDE.md: drule.py "16+ checks"; DECISIONS.md:724: "drule.py is 16 checks, 16 proved by planting". DATA: 26 checks, 26 proved. (PLAN.md:246 says "26 checks, 26 proved" and is the only correct statement.)
   `python3 redo/gates/drule.py | tail -2` -> "CLEAN -- 26 checks pass."; `--selftest | tail -2` -> "26/26 checks proved by planting".

6. DECISIONS.md:514: "ligands.py, 5 checks, each proved by planting". DATA: 10 checks, 10 plants.
   `python3 redo/gates/ligands.py | tail -2` -> "CLEAN -- 10 checks pass."

7. CLAUDE.md: layout.py "--selftest L2 (6 plants); --selftest-all L1 and L3-L7 (6 plants)". DATA: 7 plants each, and --selftest-all covers L1 and L3-L8 (eight checks exist, L8 included).
   `--selftest | tail -2` -> "L2: 7/7 plants fire"; `--selftest-all | tail -2` -> "L1,L3-L8: 7/7 plants fire".

8. CLAUDE.md: "at least two [inputs] -- including g1_recording_spec.tsv, the campaign's own recording contract -- have no writer anywhere in redo/build/". DATA: g1_recording_spec.tsv now HAS a generator (build/g1_recording_spec.py, created under F-22 on 2026-09-12), it is named in MANIFEST.tsv, and `python3 redo/build/g1_recording_spec.py --check` prints "OK  49 columns, file matches the generator". The correct count of inputs with no writer anywhere in the repo is SIX: g0_pilot_measurements.csv, g0_selftest.txt, panel_gpcrdb_degree.csv, panel_gpcrdb_constructs.csv, panel_reference_qc.csv, panel_uniprot.tsv.

9. layout.py's own L1 check LABEL: "redo/ holds only its eight declared entries". DATA: the detail line on the same row reports "9 entries, all declared", and the TOP set in the source has nine members (README.md, paths.py, spec, build, gates, inputs, cache, runs, protocol). The count in the label is stale; the set is what is enforced. (CLAUDE.md repeats "The top level is fixed at eight entries.")

10. layout.py's selftest_all() header string: "=== layout guard self-test: L1 and L3-L7, planted ===". DATA: it plants L3 THROUGH L8 -- seven cases including L8. The footer line ("L1,L3-L8: 7/7") is correct; the header and the function docstring are stale.

11. CLAUDE.md on the C7 arm: "20 receptors / 19 clusters with the complete 2x2 (MDE 0.279)". The 20/19 re-derive exactly from g2_systems.csv. The MDE does not belong to that contrast: 0.279 = 1.218/sqrt(19) is the INTERACTION figure. spec/C7_PREREGISTRATION.md corrected this on 2026-09-13 -- C7's primary contrast is a MAIN EFFECT, cluster SD 0.189-0.242, MDE at k=19 of 0.121-0.155. Quoting 0.279 was conservative (it understated power, so nothing was overclaimed) but it carried a constant across contrast types. SEPARATELY: neither 0.189 nor 0.242 appears anywhere in redo/gates/ or redo/build/ -- the main-effect power figure has no gate behind it, while 1.218 appears 8 times in code.

12. The brief and CATALOGUE.md: "45 experiments E0.1-E9.3". DATA: 45 HEADINGS but 46 distinct ids referenced. E6.3 has no heading of its own -- it shares one with E6.2 ("### E6.2 / E6.3 -- Ship the three Block D rows.csv and rows.tier3.v2.csv"). CAMPAIGN.md:151 already records this: "carries two experiments -- so 46 experiments in 10 groups." So 45 and 46 are both defensible but they count different things, and no document says which it means.

NOTE ON DIRECTION: items 3, 4, 5, 6 and 7 all UNDERSTATE how much verification exists -- the machinery is larger than the prose claims. Item 3 is the only one where a stated coverage figure is HIGHER than the real one (12/12 asserted against 12 plants over 13 checks), and it is therefore the only one that could mislead someone into trusting an unproved check.

---

# Part 13. Known defects — stated, not hidden

1. **The recording contract records LESS confidence information than the frozen
   campaign already holds.** `inputs/g1_recording_spec.tsv` is 49 rows and names
   `plddt_partner_chain_mean` and `plddt_ga_alpha5` — **both partner-side**. It does
   **not** name `plddt_mean`, `plddt_at_anchors`, `min_plddt_at_anchor`, ipTM, PAE,
   `ramachandran_outlier_frac`, `chain_breaks`, `templates_used` or
   `recycles_realised`. **Blocks B and D each hold four confidence columns.**
   **Title clause 3 is a confidence claim**, so as specified the redo would record
   strictly less of the quantity its own headline depends on.
   **Fixable by the documented route** — edit `build/g1_recording_spec.py`, re-run it,
   then `build/manifest.py` to restamp; the generator reproduces its own output
   byte-for-byte and refuses with a named FAIL when the file has drifted from it.
   **Free today, impossible after dispatch.**
2. **`family_swap` (G9) is enumerated and NOT built.** All 30 rows carry
   `chain_b_sha256 = PENDING:COUPLING.md`. Dispatching today would send an unbuilt
   control arm.
3. **Templates have never been a factor in either campaign.** The string "template"
   appears zero times in `g1_recording_spec.tsv`, `g1_systems.csv`, `g2_systems.csv`,
   `CAMPAIGN.md` and `MSA_SPEC.md`. The frozen campaign's templates-off state rests on
   **evidence class (b) + (c)** — launcher static analysis and upstream defaults — and
   **never on a per-row runtime echo**. Nobody has verified templates were off, let
   alone set them on.
4. **15 of the 65 files in `inputs/` name no generator** in `MANIFEST.tsv`. Two of them
   — `g0_measurements.csv` and `g0_pilot_measurements.csv` — are unattributable **by
   construction**, because they are written through an argparse `--out` that the static
   attribution walk cannot see.
5. **There is no GPU-hour model.** See Part 2.5.
6. **`PLAN.md` schedules by stage, not by experiment id**, so the stage ↔ experiment
   join had to be authored by hand in `build/run_registry.py`. Read
   `run_registry.tsv`'s pillar column rather than inferring a join from the plan text.
7. **Stage 2 discharges no catalogued experiment at all.** Its main arm carries no
   E-id, so either the arm needs one or the catalogue is missing the experiment it is.
8. **A contradiction that needs a decision, not a patch.** Stage 2 says an apo-only
   control *"does NOT bound the complex case … write the caveat; do not spend
   predictions pretending to close it"*, while `MSA_SUBSAMPLING_REGIMES.md` §5 schedules
   Stage 2 as depth × partner rung and `CAMPAIGN.md` §2.9 says the corresponding
   experiment "SURVIVES, and gains urgency". Those cannot all stand.

---

# Part 14. Decisions waiting on the PI

| decision | what it is | what it blocks | where |
|---|---|---|---|
| **D4** | the balancing rule for fitting the state threshold: prevalence-weighted, equal-weight by class, matched sampling, Youden on balanced classes, or unsupervised mixture | **the entire Group 0 fit.** `GROUP0_SYSTEMS.md` §6 states the section must be settled *before any threshold is fitted* | `GROUP0_SYSTEMS.md` §6, `ASKS.md` |
| **the adaptation band** | the interior band `[PI lower]`–`[PI upper]` | must be recorded **with its date before Stage 3 runs**, or the adaptive design becomes a post-hoc choice | Part 9 |
| **the recording contract** | whether to add the confidence columns the redo currently omits | free now, impossible after dispatch | Part 13, defect 1 |
| **which of the thirteen** | funding from the gap audit | — | Part 10 |

**On D4, the two facts that make it a real decision rather than a detail.** The
calibration set is **5.7 active per inactive**; the application set is **1.9 to 1**.
Fit on the pool as it stands and the threshold inherits which receptors happened to get
solved with a G protein bound, treated as though that were a fact about activation.
Reweight to equal classes and the cut sits where the two class densities cross. Those
give different numbers.

The recommendation on record is **equal-weight as the headline, with prevalence-weight,
Youden and the unsupervised mixture all reported** — equal-weight because the
application set's prior differs from the calibration set's, so a prevalence-weighted cut
is calibrated for a population we will never grade; prevalence-weight because a reader
will ask; Youden because it names an operating point; the mixture because it consumes
no labels.

Whatever is chosen, **the fit must be grouped by receptor**: 147 receptors supply 726
structures and 113 of them are active-only, so a pooled ROC confounds receptor identity
with state, and a leave-one-receptor-out estimate is the only honest one. That is
separate from the balancing rule and is not optional.

---

# Part 15. Two failure patterns that govern how any result here may be reported

Both were named on 2026-09-14, after each had already occurred more than once. They are
recorded in general form because the specific forms keep recurring in new costumes.

### F-32 — a count is not a rate until you can name what was in the denominator and what could never have been in the numerator

Two Block D receptors, **EDNRB and GRPR, carry leucine at position 7.53**. The NPxxY
hydroxyl distance is therefore a quantity that does not exist for them: all **1,960** of
their rows are `nan` on that axis, and every one of those 1,960 rows nonetheless carries
`passed = True`. They were entered into a published concordance table at **0 % active**,
which reads "never active" and means **"never measurable"**. That single convention
lifted **29 of 30** cells in the table and **flipped two signs**.

The same failure has a literature form: "no paper reports X" was a claim about the
**corpus**, stated as a claim about the **literature**, and the corpus turned out not to
contain the AlphaFold paper.

**The data form is worse, and it is worth being clear why.** A corpus negative is at
least visible as an absence once somebody asks. **A null over an undefined population
looks like data**: it has a value, a row count and a confidence interval, and all three
are well-formed.

Four instances are tabulated in `DECISIONS.md` F-32 — this one, the C7 retraction, the
decoy refusal, and the corpus negative. **`verify.sh` was green through every one**,
because a gate checks that a computation is *right* and this is a defect in what the
computation is *about*.

### F-33 — when the selection criterion is the result, the agreement is not information

If we choose the subsampling method that produces the most active-state calls, we have
chosen the method that best mimics our own result, and its agreement with us carries no
information.

The sharpest instance comes from the literature: the authors of the strongest
counter-example write that AlphaFold reaches active GPCR states because *"the
composition of the AF2 training set … featured the structures of many active GPCRs"*.
**If active is the memorised default, then reaching active is what the null does**, and
any method selected for reaching active has been selected for agreeing with the prior.
**Reaching INACTIVE is the informative direction.** That turns the strongest piece of
counter-evidence into a design constraint on our own MSA arm rather than something to
rebut.

**The rule both patterns impose, and it is cheap only because nothing has run:**

> **Every arm whose method or parameter is chosen must pre-register the choice rule,
> and the rule must not mention the outcome.** Select on a property of the **input** —
> alignment depth, sequence diversity, cluster count. Never on a property of the
> **output** — predicate-active fraction, agreement with our own call. Where
> performance must decide, decide it on a **held-out** system set that is not in the
> reported panel, and say so in the Methods.

### The practical consequence: pre-register the expected shape, not the expected answer

Worked example, already written down for an arm that is free and has deliberately not
been run. A published index reports that *"many active nanobody structures are predicted
to be weakly active"*. Block D's nanobody arms are held at row level, so testing that
costs nothing.

The framing matters more than the test. `khaleq2026hyaline`'s labelling rule counts
G-protein-mimetic nanobody-bound structures as active **by construction**. So a
disagreement would **not** be evidence that our labels are wrong — it would be a
measured gap between **two published conventions**, one geometric and one
pharmacological, and **nobody has measured that gap on predicted structures.**

**Writing that down first is what makes both outcomes reportable**: a gap is a result
about the conventions, and no gap is a concordance that strengthens both. **Neither
reading survives being looked at first**, which is exactly why it was written before the
query was run.
