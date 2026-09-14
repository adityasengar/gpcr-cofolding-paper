# Block D — discrepancy report

Written 2026-09-10 by the orchestrator session, on intake of
`block_d_figure_data.zip` (SHA-256 `c000b1636e1846c6…`). Verifier:
`analysis/block_d/verify_claims.py` — **54 checks, 48 reproduce, 6 do not**;
40 RECOMPUTED, 14 CONSISTENCY, and **12 claims recorded as PROSE-ONLY because
nothing in the bundle can test them.** Five of the six mismatches are
sub-Ångström and change no call (D-D-4, D-D-8).

The count that matters is not 48/54. It is that Block D's claim sheet carries
twelve claims and **no row-level file behind any of them.**

---

## D-D-1 — Block D ships no row-level data at all

The claim sheet names its three corpora explicitly:

```
experiments/022_tier_d1_deep_apo/analysis/full/rows.csv       14,000 preds
experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv   2,370
experiments/024_tier_d3_msa_depth/analysis/full/rows.csv          25,810
```

**None of the three is in the bundle.** Five CSVs ship in total and all five are
panel or reference metadata: three tier panels, a paralogy map, and the nanobody
anchor table. The remaining 56 files are markdown and fifteen coordinate files.

This is the third consecutive block to tighten in the same direction, and the
trend is the finding:

| block | row-level files shipped | consequence |
|---|---|---|
| A | full row table, 9,490 rows | 47 checks, most RECOMPUTED |
| B | full row table, 32,000 rows | 109 checks, 21 recorded mismatches |
| C | one file, 40,000 rows | 30 of 53 checks consistency-only |
| **D** | **none** | **every headline number is prose** |

**What this does and does not mean.** It does not mean the numbers are wrong.
The internal documentation is unusually good — GATE-2 reproduced the four D3
slopes from scratch and found they match only under `ln(depth)` with
`full = 4096`, GATE-1 and GATE-4 chase provenance, and ten withdrawals record
claims that were tested and dropped. That is more self-audit than either of the
previous two blocks shipped. But an audit we cannot re-run is a report about a
verification, not a verification, and this project's standing rule is that a
sentence carries a locator or a recomputation.

**What we could still recompute, and did.** Everything not requiring the rows:

- the three panel sizes (7, 4, 26) and the paralogy map (40 receptors, 26 clusters);
- **D3's 22 clusters over 26 receptors**, which Flag D-1 uses to license
  cluster-boot — reproduces exactly;
- **D1 and D2 cluster-boot degeneracy** — 7 receptors in 7 clusters, 4 in 4, so
  cluster-boot is arithmetically identical to receptor-boot, exactly as Flag D-1
  states;
- **all six exact binomial intervals** quoted in the claim sheet and Part A,
  by Clopper–Pearson at n = 50 — every one reproduces to the stated decimal,
  including the flagship OPRK × Boltz `[33.7, 62.6]` and Protenix's
  `[61.8, 86.9]`;
- **C-D-12's memorization premise** — all four nanobody anchor PDBs do predate
  every *dated* backbone cutoff. OF3's cutoff is `TBD` in the shipped table, so
  for OF3 the premise is untested rather than confirmed;
- the ln-versus-log₁₀ factor behind Flag D-2 (−3.877 / −1.684 = 2.302 = ln 10);
- **fifteen NPxxY hydroxyl distances, measured from the coordinates.**

## D-D-2 — the structures reproduce, and that is worth stating plainly

`analysis/block_d/cifmeasure.py` measures d(Y5.58 OH, Y7.53 OH) in all fifteen
shipped CIFs. Y7.53 is located from each file's own NPxxY motif, needing no
external numbering; on all fifteen it agrees with the GPCRdb-mapped position in
Block B's pinned anchor table, which is what licenses taking 5.58 from the same
table. Both anchors are identity-checked and the script refuses rather than
guesses.

| structure | measured | stated in MANIFEST |
|---|---:|---|
| `d2_adrb2_inactive_nb_protenix` | **4.53 Å** | 4.53 Å — **exact** |
| `d2_acm2_active_nb_chai` | **19.12 Å** | 19.1 Å — **exact** |
| `d3_protenix_agtr1_depth8` | **3.56 Å** | 3.4 Å — see D-D-4 |

And every spot-check's state call matches the claim it was chosen to illustrate:
ADRB2 × Chai apo active at 4.22 Å against ADRB2 × Boltz apo inactive at 11.31 Å
on the same receptor (SC-D-1's per-backbone divergence); GHSR × Boltz inactive at
10.09 Å (SC-D-2); LPAR1 × OF3 active at 4.91 Å with the claim that its
sub-Å-to-active is 0.4 % (SC-D-12's coherent non-reference fold).

Block A shipped four `ALIGNMENT.md` files whose named residues did not reproduce
the shipped distances, and one coordinate file that was the wrong protein
entirely. Block D's fifteen are clean. **This is the strongest evidence in the
bundle that the pipeline's geometry is sound**, and it is worth more than any
consistency check, because it is the one place a number could be checked against
something other than another sentence.

## D-D-3 — D2's prediction total implies 45 populated cells; Part A says 44

`PARTA_D2.md §2` is headed "all 44 populated cells". The claim sheet's total is
2,370. Those reconcile exactly one way:

```
44 cells x 50 samples          = 2,200
+ AGTR1 x active_nb x OF3      =   170   (C-D-5: three OF3 stragglers killed)
                                 -----
                                 2,370   exactly the claim sheet's total
```

which implies **45** populated cells, not 44. Against a nominal grid of 13 arms
× 4 backbones = **52**, that leaves **seven cells that were never populated and
are named nowhere.**

Low severity for any sentence we would write — no D2 claim rests on the total —
but it is a denominator nobody can reconstruct, and it is the class of defect
that quietly dilutes a rate. Asked in `DATA_REQUESTS.md`.

**C-D-5 also argues with itself about its own grid**, in its own parentheses:
*"Total canonical n per cell = 50 × 4 sample subruns = 200 preds (2 sample
subruns per seed × 10 samples? actually 5 seeds × 10 samples = 50 per cell; but
D2 uses 4 fold-multiplier per cell to reach 200/cell canonical in the
dispatch)."* The statistics settle it: **every interval in the claim sheet
reproduces at n = 50** and none reproduces at n = 200. Fifty is the effective n
and the manuscript will say so.

## D-D-4 — WITHDRAWN on the same day it was written: the manifest quotes a cell median

**This entry was wrong and is kept as a correction, not a finding.**

The manifest's `dossier_finding` for `d3_protenix_agtr1_depth8.cif` reads
*"NPxxY 11 → 3.4 A"*, and measuring that file gives **3.56 Å**. Recorded here as
a 0.16 Å discrepancy. It is not one. `GATE_3_STEERING_VS_DEGRADATION.md` §
tabulates the same cell with its columns headed **"med pLDDT | anchor 4/4
identity | med pca_active | med NPxxY | med tilt"** — 3.40 Å is the **median over
the cell's 50 samples**, not a property of the one structure that shipped.

Comparing a single shipped sample against a cell median is a category error, and
the checker made it before the gate report had been read. The check now asserts
only what the file can settle: that this sample sits on the active side of the
9.08 Å threshold, which it does at 3.56 Å.

The residual observation is about labelling, not arithmetic: a manifest entry
that describes one coordinate file should not quote a statistic computed over
fifty, because a reader measuring the file will get a different number and
believe they have found a defect. Raised as a question, not a rebuttal.

**This also weakens D-D-8**, which compares `PARTA_D1 §4`'s five values against
the same five shipped files. That table is presented per-structure — it is headed
"Structural spot-check log" and its rows are single CIFs with helix content and
Rg, which are not cell statistics — so the comparison is probably legitimate
there. Probably is not certain, and the question now asked upstream covers both.

## D-D-5 — the block is not frozen, and its own claim sheet says so

The claim sheet's first line: **"Status: DRAFT (2026-09-10). Freeze tag
`block_d_freeze` NOT placed — held pending §2.4 post-cutoff-inactive-Nb test
decision."**

Flag D-8 then reports that the same §2.4 test *closed* as
attempted-and-documented on 2026-09-10, and that main-text framing is
**locked** per dossier §6.5. So the condition the freeze was held for has been
resolved, and the freeze has not followed. Every Block D number in the
manuscript is therefore built on an unfrozen draft. Stated in Methods; asked in
`DATA_REQUESTS.md`.

## D-D-6 — no derivation script exists for the four headline slopes

C-D-2 and GATE-2 both record it: the D3 slopes were not produced by any script
in the repository. GATE-2 grepped for `slope`, `linregress`, `polyfit`,
`%/log`, `log_depth`, `d3_slope` and `regression` across the experiment tree and
found nothing, then reproduced the numbers by fitting them itself — exactly, and
only under natural log with `full = 4096`.

**This is the drop auditing itself and getting it right**, and it is why the
slopes are quotable at all. But the reproduction lives in a markdown report; the
draws behind the cluster-boot intervals are not shipped either, so SC-D-8's four
confidence intervals are PROSE-ONLY even though its four point estimates have
been independently refitted.

## D-D-7 — one dated cutoff is missing, and it is load-bearing for the caveat

C-D-12 — the memorization confound the dispatch calls "the big one" — rests on
all four nanobody anchors predating every backbone's training cutoff. Three
cutoffs are dated in `nanobody_state_anchors.csv` (Chai 2021-01-12, Protenix
2021-09-30, Boltz-2 2023-06-01) and **OF3's column is literally named
`cutoff_of3_TBD`**. `ASSUMED_NOT_VERIFIED_BLOCK_D.md` confirms the OF3
release-notes lookup was never done.

So for three of four backbones the confound is established; for OF3 it is
assumed. Any sentence saying "all four backbones' cutoffs" must instead say
three, and OF3 separately. No claim collapses — 5JQH (2016), 6VI4 (2020), 4MQS
(2013) and 6OS2 (2019) all predate any plausible 2024-or-later OF3 cutoff — but
the paper should not assert a date nobody has.

## D-D-8 — the D1 spot-check coordinates do not reproduce Part A's own distances

`PARTA_D1.md §4` tabulates an NPxxY-OH value for each of five D1 structures and
introduces them as *"Five CIFs pulled from ..."* — the same five that ship in
`10_structures/spot_check/`, and `MANIFEST.json` gives all five a single seed
(`1015473677`) and a single `sample_idx` (5). They should be the same objects.

| structure | Part A §4 | measured here | difference |
|---|---:|---:|---:|
| `d1_adrb2_chai_apo` | 4.19 | 4.22 | +0.03 |
| `d1_ghsr_boltz_apo` | 10.03 | 10.09 | +0.06 |
| `d1_adrb2_boltz_apo` | 11.58 | 11.31 | −0.27 |
| `d1_cnr2_chai_apo` | 2.25 | 2.61 | +0.36 |
| `d1_lpar1_of3_apo` | 5.42 | 4.91 | **−0.51** |

**No state call changes** — every pair sits on the same side of the 9.08 Å
threshold, so nothing in SC-D-1, SC-D-2 or SC-D-12 moves.

What makes this worth recording is the contrast with D-D-2. The two D2 manifest
distances reproduce to the decimal (4.53 exactly; 19.12 against 19.1), and ADRB2
appears in *both* sets — so a wrong 5.58 or 7.53 assignment cannot explain it,
because the same anchors give an exact match on the D2 file and a 0.27 Å gap on
the D1 file for the same receptor. Either the shipped D1 coordinates are a
different sample from the one Part A measured, or the two measurements use
different atom conventions. The bundle does not say which, and with no row
table there is no third source to break the tie.

This is Block A's `ALIGNMENT.md` failure class in a much milder form: there, four
of four named anchor sets failed to reproduce the shipped distances and one
coordinate file was the wrong protein. Here the anchors are right, the proteins
are right, and the disagreement is sub-Ångström. It is still a disagreement
between two files in the same bundle. Asked in `DATA_REQUESTS.md`; the
manuscript quotes the measured values and says they were measured.

## What reproduces, which is most of what could be tested

Worth stating, because the four items above are about provenance and scope
rather than about the result. Every claim that could be checked without the row
tables checked out: three panel sizes, two cluster counts, both degeneracy
assertions, six exact binomial intervals, the ln-versus-log₁₀ factor, the four
anchor PDB identities, the cutoff comparison on three of four backbones, fifteen
NPxxY measurements, and fourteen cross-document consistency checks spanning the
claim sheet, the Part A documents, the gate reports and the flags.

**All six mismatches are sub-Ångström and change no call.** On the evidence available,
Block D's internal bookkeeping is the most careful of the four blocks. It is
also the least verifiable, and those two facts are not in tension — they are the
same fact seen from two sides.

## D-D-9 — SC-D-3's number and its wording name different quantities

**Found 2026-09-14, the first Block D claim to fail against its own rows.**

The claim: *"CNR2 100% sub-Å to BOTH references on all 4 backbones."* It was
PROSE-ONLY until `rows.d1_deep_apo.csv` landed on 2026-09-13.

**Recomputed, and the data resolves it cleanly:**

| quantity | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| sub-Å to **both** references *(the claim as worded)* | 86.0% | 91.6% | 99.8% | 96.8% |
| sub-Å to the **active** reference alone | **100.0%** | **100.0%** | **100.0%** | **100.0%** |

**Why:** CNR2's worst-case pocket Cα RMSD **to active is 0.791 Å** — every one of its
2,000 samples is sub-Ångström, on every backbone. Its worst **to inactive is 1.270 Å**,
so not every sample is sub-Å to both.

**What we will write.** The saturation point the claim is making survives and is if
anything cleaner: *CNR2 is sub-Ångström to its active reference on 100% of samples
across all four backbones.* **The "to both" phrasing does not reproduce and must not be
used.** Checked at `<` and `≤`, on all rows and on `passed` rows only — all 2,000 CNR2
rows carry `passed=True`, so no filter accounts for the difference. A 1.5 Å threshold
*does* give 100% to both, which is the other reading that would make the sentence true.

**For `paper_af3`:** this is one sentence to settle — was the intended quantity sub-Å to
active, or sub-1.5 Å to both? Either way the claim's *point* holds. Not urgent, and no
file is needed to answer it.
