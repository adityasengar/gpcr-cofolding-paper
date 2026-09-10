# PART A / D3 — MSA-depth conformational-generation sweep (reframed)

**Status**: Part A/D3 draft. Author: fork of Block D closeout. Synthesizes GATE-2 (slope derivation) + GATE-3 (steering vs degradation) + fresh recomputes on the D3 corpus.

**Corpus**: `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` — 25,810 predictions.
- Panel: 26 Class A receptors × 4 backbones × 5 depths (8, 32, 128, 512, full) × 5 seeds × 10 samples.
- Scorer `d9c646af5f89861c16062bf256de96a8389d9915` uniform at row level (GATE-4).
- Paralog cluster coverage: 22 clusters (cluster-boot valid).
- Coverage note: 190 of 26,000 dispatched rows did not land (0.73%); non-uniform across (bb, depth) with worst-case n=1,250 at OF3 × full and Chai × full. See §7 Coverage.

**Documentation drift** (GATE-4): headline doc `tier_d3_full_headline_2026_09_08.md:6` cites scorer `891041e858f3747b…` in prose. That SHA does not exist in git. Same phantom-SHA pattern Block C's `T7C_POST_FIX_HEADLINE.md` carried; the row-level `d9c646af` is authoritative.

---

## §1 — F1 reframed (the reversal)

**Old F1** (`tier_d3_full_headline_2026_09_08.md`): *"Depth is a controllable lever on 3 of 4 backbones (Boltz, OF3, Protenix). Slopes −1.7 to −3.0 %/log(depth) across the 26-receptor panel. Protenix has the strongest monotonic response. All 4 backbones have NEGATIVE slope — PREREG §D-3 hypothesis is CONFIRMED across the full 26-receptor panel on all 4 backbones."*

**W-D-# withdrawal**: withdraw the sentence "PREREG §D-3 hypothesis is CONFIRMED on all 4 backbones" and the paired sentence about Protenix being the strongest depth-response backbone. Not because the fractions are wrong — they reproduce exactly — but because "response of the model to depth" was implicitly conflated with "the model steers toward the active reference conformation at shallow depth." GATE-3's structural evidence shows those are different things. Withdrawal basis: `paper_af3_release/dossiers/BLOCK_D/draft/gates/GATE_3_STEERING_VS_DEGRADATION.md`. Also citable: (b) sub-Å-to-active fraction from raw D3 rows, tabulated in this section.

**Reframed F1** (draft, for joint review):

*"MSA depth modulates predicate-active sampling on all four backbones, but the mechanism differs. Boltz-2's shallow-depth response is a clean conformational lever: the predicate-active fraction rises from 5.1 % → 17.8 % and pocket-Cα sub-Å-to-active rises with it (42.5 % → 51.2 %) while fold quality holds (pLDDT 76.3 → 75.7). Chai-1's response is muted (19.4 % → 25.1 %; slope not distinguishable from zero under cluster-bootstrap), with pocket-Cα-to-active flat and fold quality stable — real but small headroom. OF3-preview and Protenix v2 show the largest apparent slopes (−2.73, −2.96 %/ln-depth) but shallow depth degrades their fold: pocket-Cα-to-active does not track the rising predicate (OF3 50.6 % → 29.7 %; Protenix 37.9 % → 29.2 %), matched-seed 7TM Cα RMSD to their own full-depth prediction lands in the 10–20 Å range, and pLDDT drops materially (OF3 −3.9; Protenix −3.2). We report all four slopes as measured but do not describe OF3 or Protenix as controllable levers on this axis."*

### Full per-cell table (25,810 rows, verified from raw)

| bb | metric | 8 | 32 | 128 | 512 | full |
|---|---|---:|---:|---:|---:|---:|
| **Boltz-2** | predicate active % | 17.8 | 7.0 | 4.9 | 5.4 | 5.1 |
|  | sub-Å pocket-Cα active % | 51.2 | 43.8 | 39.9 | 41.1 | 42.5 |
|  | sub-Å pocket-Cα inactive % | 68.5 | 75.8 | 79.2 | 81.0 | 79.7 |
|  | pLDDT median | 75.73 | 76.08 | 76.01 | 76.15 | 76.26 |
| **Chai-1** | predicate active % | 25.1 | 20.2 | 19.7 | 18.4 | 19.4 |
|  | sub-Å pocket-Cα active % | 36.7 | 36.9 | 36.6 | 39.1 | 43.0 |
|  | sub-Å pocket-Cα inactive % | 71.8 | 74.7 | 74.2 | 79.1 | 78.7 |
|  | pLDDT median | 74.14 | 74.11 | 74.89 | 75.67 | 75.12 |
| **OF3-preview** | predicate active % | 28.0 | 26.2 | 21.9 | 15.4 | 12.4 |
|  | sub-Å pocket-Cα active % | 29.7 | 44.8 | 50.2 | 50.5 | 50.6 |
|  | sub-Å pocket-Cα inactive % | 37.2 | 57.5 | 68.6 | 73.1 | 73.8 |
|  | pLDDT median | 64.60 | 67.16 | 67.90 | 68.10 | 68.45 |
| **Protenix v2** | predicate active % | 15.5 | 16.8 | 9.7 | 2.1 | 0.1 |
|  | sub-Å pocket-Cα active % | 29.2 | 42.1 | 40.5 | 37.6 | 37.9 |
|  | sub-Å pocket-Cα inactive % | 44.9 | 68.0 | 79.8 | 85.8 | 89.0 |
|  | pLDDT median | 72.11 | 73.87 | 74.78 | 75.19 | 75.29 |

**Reading the table**: predicate-active is what the two-instrument test sees. Sub-Å-to-active is whether the predicted pocket-Cα geometry actually approaches the deposited active crystal. For Boltz they move together; for OF3 and Protenix they move in OPPOSITE directions at shallow depth — the predicate opens, but the pocket-Cα moves AWAY from the active reference. That's the degradation signature.

---

## §2 — Slopes (from GATE-2, retained as recompute)

`ln(depth)` regression, `full=4096` nominal, cluster-boot 95 % CI over 22 paralog clusters, 1,000 replicates. All numbers `% per ln(depth)`:

| backbone | slope | 95 % CI | verdict under cluster-boot |
|---|---:|---|---|
| Boltz-2 | −1.684 | [−2.692, −0.812] | signed |
| Chai-1 | −0.815 | [−2.380, +0.357] | **crosses zero — inconclusive** |
| OF3-preview | −2.732 | [−4.365, −1.145] | signed but degradation-inflated (see §1) |
| Protenix v2 | −2.956 | [−4.678, −1.581] | signed but degradation-inflated (see §1) |

**Unit correction (from GATE-2)**: headline says `%/log(depth)` — the slope was fit against natural log, not log10. Manuscript sentence must say `%/ln(depth)` or "per e-fold change." Off by factor ~2.303 otherwise.

**C-D-# caveat**: no derivation script exists on disk for the original slopes. The point estimates reproduce exactly, but the fitting method was inferred (ln, full=4096) rather than replayed from code. GATE-2's recompute becomes the authoritative script and should be committed alongside the dossier if this analysis rides into the paper.

---

## §3 — Family-level slopes (secondary S1)

Cluster-bootstrap 95 % CI within family (small n within-family; cluster count in parentheses):

| family | recs / clu | Boltz | Chai | OF3 | Protenix |
|---|---:|---|---|---|---|
| aminergic | 6/5 | −1.41 [−3.90, −0.05] | +0.06 [−0.00, +0.17] | −0.68 [−2.31, +0.48] | −0.45 [−1.24, +0.00] |
| peptide | 8/7 | −1.29 [−3.17, +0.00] | +0.78 [−0.00, +2.31] | −2.31 [−5.35, +0.06] | −2.86 [−6.72, +0.00] |
| chemokine | 3/2 | −2.38 [−3.50, −1.27] | −3.94 [−7.88, +0.00] | −3.86 [−7.67, −0.06] | −8.26 [−8.60, −7.92] |
| opioid | 3/2 | −0.29 [−0.57, +0.00] | −0.88 [−1.76, +0.00] | −6.40 [−7.15, −5.65] | −2.48 [−2.48, −2.48] |
| lipid | 2/2 | −2.11 [−3.23, −0.99] | +0.07 [+0.00, +0.14] | +1.80 [−1.57, +5.17] | −1.65 [−3.29, −0.01] |
| other | 4/4 | −3.05 [−7.41, +0.00] | −1.45 [−4.39, +0.03] | −5.02 [−9.53, −0.50] | −3.77 [−9.42, +0.00] |

**Reading**: chemokine and opioid family results carry very tight CIs, but each family has only 2 clusters — degenerate cluster-boot, functionally receptor-boot. The Protenix chemokine slope of −8.26 is the largest single-family slope in the table and comes from just 2 receptors' behaviour amplifying at shallow depth; not a general finding, worth flagging.

**Family-signal question**: does depth response track chemistry? **Weak signal.** Aminergic slopes are the flattest across all backbones; peptide receptors trend larger absolute slopes on OF3/Protenix; chemokines have the widest per-family responses but small n. No clean chemistry gradient — the backbone-level effect dominates the family-level effect. Family-stratified reporting is honest but not the headline.

---

## §4 — Kendall τ cross-backbone rank concordance (P3)

τ over the 26 receptors' per-cell active fractions, all 6 backbone-pair combinations, at each depth:

| depth | bol~cha | bol~of3 | bol~pro | cha~of3 | cha~pro | of3~pro |
|---|---:|---:|---:|---:|---:|---:|
| 8 | +0.25 | +0.15 | +0.13 | +0.17 | −0.03 | +0.59 |
| 32 | +0.26 | +0.24 | +0.42 | +0.11 | +0.08 | +0.47 |
| 128 | +0.52 | +0.14 | +0.19 | +0.15 | +0.21 | +0.29 |
| 512 | +0.42 | +0.03 | −0.12 | +0.08 | −0.18 | +0.23 |
| full | +0.44 | +0.02 | −0.08 | −0.06 | −0.11 | +0.30 |

**Reading**: Boltz~Chai is the strongest cross-backbone correlation (τ 0.25–0.52, positive at every depth). OF3~Protenix is second strongest — those two backbones agree with each other more than with Boltz or Chai. All other pairwise correlations hover near or below zero. **The two "clean lever" backbones (Boltz, Chai) rank receptors similarly. The two "degradation-leaning" backbones (OF3, Protenix) rank receptors similarly to each other but not to the levers.** Consistent with §1's reframe.

---

## §5 — Cross-tier consistency check (S3) — D1 vs D3-full on 7 overlap receptors

D3-full at (5, 10) sampling vs D1-full at (5, 100). D1's 95 % Wilson CI on the (n=500) per-cell active fraction; check whether D3-full's (n=50) point estimate lands inside:

| receptor | bb | D1 % | D3 % | in D1 95 % CI? |
|---|---|---:|---:|---|
| CNR2 | boltz | 2.2 | 0.0 | ✗ (D1 CI 1.2–3.9) |
| CNR2 | chai | 99.8 | 100.0 | ✗ (CI 98.9–100) |
| CNR2 | of3 | 1.8 | 0.0 | ✗ (CI 0.9–3.4) |
| CNR2 | protenix | 1.6 | 0.0 | ✗ (CI 0.8–3.1) |
| **OPSD** | **boltz** | **38.8** | **10.0** | ✗ (CI 34.6–43.1) |
| OPSD | chai | 98.6 | 88.0 | ✗ (CI 97.1–99.3) |
| OPSD | of3 | 9.4 | 4.0 | ✗ (CI 7.1–12.3) |
| OPSD | protenix | 0.0 | 0.0 | ✓ |
| ADRB2 | boltz | 0.0 | 0.0 | ✓ |
| ADRB2 | chai | 100.0 | 100.0 | ✗ (rounding artefact; both are ≥99 %) |
| ADRB2 | of3 | 4.0 | 4.0 | ✓ |
| ADRB2 | protenix | 0.0 | 0.0 | ✓ |
| LPAR1 | boltz | 0.2 | 0.0 | ✗ (marginal) |
| LPAR1 | chai | 0.0 | 0.0 | ✓ |
| LPAR1 | of3 | 91.8 | 98.0 | ✗ (CI 89.1–93.9) |
| LPAR1 | protenix | 0.0 | 0.0 | ✓ |
| CXCR4 (all 4) | | matches | matches | ✓ |
| GHSR (all 4) | | matches | matches | ✓ |
| NPY1R | of3 | 6.6 | 0.0 | ✗ |

**28 cells; 12 outside D1's Wilson 95 % CI.**

Of those 12, most are Wilson-CI-narrowness artefacts (D1's n=500 gives extremely tight CI around 0 % or 100 %; a D3 point that rounds to the same fraction technically falls outside a CI that's only 0.8 pt wide). Filtering to genuinely material divergences:

- **OPSD × Boltz** — 38.8 % → 10.0 %, a real 28.8-point drop. This is a **material inconsistency** between D1's (5, 100) resample and D3's (5, 10) sampling on the same apo × Boltz × OPSD cell. Two possible readings: (a) OPSD × Boltz apo has real bimodality where (5, 10) undersamples the active mode, (b) some upstream difference between the D1 and D3 apo constructs (checked: same panel_receptor_sequence, same MSA discipline) that I did not chase. Flag for §6 discussion; the OPSD × Boltz claim in D1 F3 stays scoped to D1's sample count.
- **OPSD × Chai** — 98.6 → 88.0. Chai locks-in-apo pattern (D2 F5) is stable in direction; the 10-point drop at (5, 10) is n=50 undersampling of near-saturated cell.
- **OPSD × OF3, NPY1R × OF3, LPAR1 × OF3** — small-magnitude drops on OF3, likely n=50 tail-sampling variance in a cell where D1's n=500 caught 1–20 samples.

**Cross-tier verdict**: D1 and D3 are broadly consistent except on **OPSD × Boltz**, where they disagree at the 3-sigma level. Every other apparent divergence is either a rounding artefact (both are 0 % or both are ≥ 99 %) or a modest n=50 undersampling of a small tail. The D3 numbers as reported in the depth table above are internally consistent (same corpus, same sampling); the cross-tier consistency check just says that at D3's "full" depth on OPSD × Boltz, the (5, 10) undersamples relative to D1's (5, 100).

---

## §6 — MCHR1 ligand_rmsd flag (from GATE-4) — could not reproduce

GATE-4 reported 990 rows in D3 with populated `ligand_rmsd_to_ref`, all MCHR1. **Recompute on the current on-disk corpus** (`experiments/024_tier_d3_msa_depth/analysis/full/rows.csv`): `ligand_rmsd_to_ref` is 100 % NaN across all 25,810 rows. Same for the D3 smoke corpus (880 rows, 100 % NaN). GATE-4 either observed an earlier state of this file (pre-final-rescore) or misread its own aggregation.

**Verdict**: Bug #4 (`MCS_FALLBACK_MIN_COVERAGE`) has **zero downstream effect on D3** — not because the guard prevented false matches, but because the ligand-scoring code path never fired on any D3 row. D3 is apo-only across the entire corpus; no ligand chain, no ligand_rmsd. GATE-4's "SAFE" verdict on cross-tier comparability stands regardless.

Note this as a small **housekeeping item**: reconcile whether GATE-4 was reading an intermediate version of `rows.csv`, or whether an aggregation column labeled `ligand_rmsd_to_ref` in a summary table caused the mismatch. Not blocking Block D.

---

## §7 — Fold-quality slope per backbone (new)

pLDDT_mean regressed on ln(depth); cluster-boot 95 % CI over 22 paralog clusters:

| backbone | slope (pLDDT-pts / ln-depth) | 95 % CI | verdict |
|---|---:|---|---|
| Boltz-2 | +0.051 | [−0.044, +0.143] | **crosses zero** — fold quality stable across depths |
| Chai-1 | +0.192 | [+0.110, +0.269] | signed weak — small quality gain with depth |
| OF3-preview | +0.682 | [+0.538, +0.841] | **signed strong** — pLDDT tracks depth on OF3 |
| Protenix v2 | +0.577 | [+0.396, +0.791] | **signed strong** — pLDDT tracks depth on Protenix |

**Reading**: this recapitulates the §1 story from a fourth angle. Boltz's fold quality does not depend on MSA depth; whatever additional predicate-active sampling it produces at shallow depth is at unchanged pLDDT. OF3 and Protenix's fold quality declines materially at shallow depth (~3–4 pLDDT-pts across the 8→full range) — the shallow-depth predicate-active regime is a lower-confidence regime for those two backbones. **Bug in the old F3**: headline said "pLDDT stable on Boltz+Chai, tracks depth on OF3+Protenix" — that is what we find, but the headline framed it as "the model's confidence tracks MSA depth" (implying the tracking is desirable). Combined with §1's sub-Å-to-active analysis, tracking is the degradation signature, not a desirable property.

---

## Coverage / caveats

- 190 of 26,000 dispatched rows did not land (0.73 %). Non-uniformly distributed:

  | | 8 | 32 | 128 | 512 | full |
  |---|---:|---:|---:|---:|---:|
  | Boltz | 1300 | 1300 | 1300 | 1300 | 1300 |
  | Chai | 1280 | 1270 | 1300 | 1300 | 1260 |
  | OF3 | 1300 | 1280 | 1300 | 1270 | 1250 |
  | Protenix | 1300 | 1300 | 1300 | 1300 | 1300 |

  All fractions in §1's table are computed on the delivered n per cell. Losses concentrate on OF3 × full (1,250) and Chai × full (1,260); no meaningful bias since the missing rows are within-cell (5-tuple failures, not receptor drops).

- `891041e858f3` phantom SHA in headline doc (from GATE-4). Manuscript-time correction: replace with `d9c646af` per row-level authority.
- No derivation script for the four slopes; GATE-2 recompute is authoritative.
- Kendall τ is over 26 receptors; treating each receptor as an independent unit (26, not 22 clusters). Same-cluster ties are inherited but do not inflate τ meaningfully.

---

## Cross-references

- Reframe basis: `paper_af3_release/dossiers/BLOCK_D/draft/gates/GATE_3_STEERING_VS_DEGRADATION.md`.
- Slope method: `paper_af3_release/dossiers/BLOCK_D/draft/gates/GATE_2_D3_SLOPES.md`.
- Scorer + Bug #4 relevance: `paper_af3_release/dossiers/BLOCK_D/draft/gates/GATE_4_SCORER_DIFF.md`.
- Headline this supersedes: `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md`.
- Memory pointer this supersedes: `[[d3_full_confirmed_2026_09_08]]` — the "confirmed on all 4 backbones" reading is superseded by the two-lever-two-degradation split.
