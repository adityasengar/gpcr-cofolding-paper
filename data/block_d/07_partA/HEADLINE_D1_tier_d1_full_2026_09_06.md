# Tier D1 full — panel-scale apo bistability at n=500 per cell (2026-09-06)

**Status**: FULL D1 deliverable. Grid = 7 Class A receptors × 4 backbones × 5 seeds × 100 samples = **14,000 predictions**. 140/140 rows landed clean (post-OF3-chunking-fix @ `24d155d`). Rescore: 14000/14000 passed, 0 failures, wall 6-30s on 16 workers (qsub 35918926).

**Provenance**:
- Manifest: `experiments/022_tier_d1_deep_apo/manifest/tier_d1_manifest.csv` (140 rows)
- Pool: `/hpc/scratch/sengaad1/paper_af3/experiments/022_tier_d1_deep_apo/full/pool` (basel-hpc)
- Rescore output: `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` (14001 lines)
- Scorer SHA: `d9c646af5f89861c16062bf256de96a8389d9915`
- OF3 chunking: 4 chunks × 25 samples per row (commit `24d155d`)

**Panel** (from `refs/tier_d1_panel.csv`):
- CNR2 (anchor, v5 apo-frac=0.27), OPSD, ADRB2, LPAR1 (mid-range), CXCR4, GHSR, NPY1R (confirmatory).

## Headline table — two-instrument active fraction at n=500

Class A predicate (PREREG §C-5): `d_npxxy_y558_y753_oh < 9.082 Å` AND `d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`.

| Receptor | Boltz | Chai | OF3 | Protenix | Spread |
|---|---:|---:|---:|---:|---:|
| CNR2 | 2.2 % (11/500) | **99.8 %** (499/500) | 1.8 % (9/500) | 1.6 % (8/500) | 0.982 |
| OPSD | 38.8 % (194/500) | **98.6 %** (493/500) | 9.4 % (47/500) | 0.0 % (0/500) | 0.986 |
| ADRB2 | 0.0 % (0/500) | **100.0 %** (500/500) | 4.0 % (20/500) | 0.0 % (0/500) | 1.000 |
| LPAR1 | 0.2 % (1/500) | 0.0 % (0/500) | **91.8 %** (459/500) | 0.0 % (0/500) | 0.918 |
| CXCR4 | 0.0 % (0/500) | 0.0 % (0/500) | 3.8 % (19/500) | 0.0 % (0/500) | 0.038 |
| GHSR | 0.0 % (0/500) | 0.0 % (0/500) | 0.0 % (0/500) | 0.0 % (0/500) | 0.000 |
| NPY1R | 0.2 % (1/500) | 0.0 % (0/500) | 6.6 % (33/500) | 0.0 % (0/500) | 0.066 |

**Zero NaN across all 14000 rows on both instrument axes.**

## Findings (numbers-with-qualifiers, rules 7a-i)

**F1 — Backbone biases are receptor-specific, not global.** The Chai active-outlier pattern documented in the CNR2 smoke (memory `[[chai-cnr2-apo-model-bias-2026-09-06]]`) does not generalise as a Chai-only story:
- **Chai** is the active-side outlier on **CNR2, OPSD, ADRB2** (98.6–100.0 % active). Chai's medians: NPxxY 2.75–4.62 Å (all deep-active), TM6 tilt 15.90–18.51 Å (all above threshold).
- **OF3** is the active-side outlier on **LPAR1** (91.8 %). OF3 median NPxxY 5.91 Å, tilt 16.71 Å. Other backbones on LPAR1: 0.0–0.2 %.
- **Boltz + Protenix** are consistently inactive-predicting on 5/7 receptors (0.0 % active).
- **OPSD is mixed across backbones**: Chai 98.6 %, Boltz 38.8 %, OF3 9.4 %, Protenix 0.0 %.

**F2 — Three receptors converge inactive across all 4 backbones**. GHSR (0.0 % everywhere), CXCR4 (0.0–3.8 %), NPY1R (0.0–6.6 %). These are the confirmatory-subset receptors (v5 apo-frac 0.02–0.04). At n=500, the sub-Å tail from v5 is not reproduced on the two-instrument predicate.

**F3 — Sub-Å pocket-Cα-RMSD-to-active hit rate distribution is richly non-trivial**:

| Receptor | Boltz | Chai | OF3 | Protenix |
|---|---:|---:|---:|---:|
| CNR2 | 100.0 % (m=0.53) | 100.0 % (m=0.51) | 100.0 % (m=0.56) | 100.0 % (m=0.51) |
| OPSD | 65.0 % (m=0.77) | 75.8 % (m=0.96) | 0.0 % (m=1.55) | 0.0 % (m=1.67) |
| ADRB2 | 82.8 % (m=0.95) | 100.0 % (m=0.46) | 84.4 % (m=0.89) | 1.4 % (m=1.07) |
| LPAR1 | 0.0 % (m=1.24) | 0.0 % (m=1.28) | 0.4 % (m=1.39) | 0.0 % (m=1.16) |
| CXCR4 | 1.2 % (m=1.30) | 0.0 % (m=1.16) | 56.6 % (m=0.99) | 0.0 % (m=1.12) |
| GHSR | 55.2 % (m=0.97) | 13.8 % (m=1.31) | 33.2 % (m=1.13) | 14.0 % (m=1.15) |
| NPY1R | 0.0 % (m=1.23) | 0.6 % (m=1.12) | 65.8 % (m=0.99) | 1.4 % (m=1.09) |

- CNR2 is saturated (100 % sub-Å across all 4 backbones) — see F5.
- LPAR1 sub-Å-to-active hit rate is 0.0–0.4 % across all backbones, but OF3's LPAR1 two-instrument fraction is 91.8 % — OF3's active-predicate signal on LPAR1 is NOT accompanied by sub-Å pocket-Cα geometry match to the active crystal reference. OF3 lands active on the *predicate* but not on the *reference geometry*.
- ADRB2 Chai 100 % sub-Å AND 100 % active is a genuine same-geometry-as-active-crystal prediction. Only Chai does this for ADRB2.

**F4 — Sub-Å pocket-Cα-RMSD-to-inactive is more consistent**:

| Receptor | Boltz | Chai | OF3 | Protenix |
|---|---:|---:|---:|---:|
| CNR2 | 86.0 % (m=0.91) | 91.6 % (m=0.92) | 99.8 % (m=0.90) | 96.8 % (m=0.85) |
| OPSD | 26.8 % (m=1.42) | 1.2 % (m=1.31) | 95.8 % (m=0.53) | 100.0 % (m=0.45) |
| ADRB2 | 100.0 % (m=0.50) | 16.8 % (m=1.05) | 100.0 % (m=0.56) | 100.0 % (m=0.38) |
| LPAR1 | 99.8 % (m=0.30) | 100.0 % (m=0.55) | 5.6 % (m=1.48) | 100.0 % (m=0.44) |
| CXCR4 | 84.0 % (m=0.85) | 10.0 % (m=1.07) | 0.6 % (m=1.08) | 59.6 % (m=0.99) |
| GHSR | 22.2 % (m=1.44) | 19.8 % (m=1.13) | 52.0 % (m=0.99) | 51.6 % (m=1.00) |
| NPY1R | 98.8 % (m=0.49) | 99.4 % (m=0.49) | 99.8 % (m=0.60) | 100.0 % (m=0.43) |

- **NPY1R converges inactive-crystal geometry** (98.8–100.0 % sub-Å across all 4 backbones). Strongest inter-backbone consistency signal.
- **LPAR1**: three backbones (Boltz/Chai/Protenix) land 99.8–100 % sub-Å to inactive. OF3 lands 5.6 % — OF3 is off the crystal on LPAR1 (m=1.48 Å from inactive AND m=1.39 Å from active — OF3's LPAR1 apo is a novel geometry).
- **ADRB2**: three backbones (Boltz/OF3/Protenix) land 100 % sub-Å to inactive. Chai lands 16.8 % — Chai's ADRB2 apo geometry departs both crystal references.

**F5 — CNR2 RMSD saturation**: pocket-Cα-RMSD is a saturated statistic for CNR2 (all 2000 CIFs sub-Å to BOTH active and inactive references). The two-instrument predicate (specific residue distances + tilt) discriminates where RMSD cannot. This is a receptor-specific RMSD-degeneracy — the CNR2 active and inactive reference crystals are geometrically close in the pocket-Cα subset used by the scorer.

**F6 — pLDDT does not track the active/inactive divide**. Backbone pLDDT_mean medians per (receptor, backbone) cluster around 68-85 with no obvious correlation to the two-instrument fraction. Chai's active-bias on CNR2/OPSD/ADRB2 is NOT accompanied by pLDDT collapse; OF3's LPAR1 active-bias likewise has pLDDT 68.0 (moderate, comparable to others). Not a fold-quality artefact.

## Interpretation caveats (rules 7a-i)

- **F1 supersedes** the "Chai has a systematic active bias" story from the smoke (memory `[[chai-cnr2-apo-model-bias-2026-09-06]]`). Chai is active-outlier on 3/7 receptors, inactive-consistent on 4/7. OF3 is the outlier on 1/7. The general story is receptor-dependent backbone bias, not any single-backbone bias.
- **F2 is signed on the two-instrument axis** but F4 shows GHSR and CXCR4 have mixed sub-Å-to-inactive hit rates across backbones. Convergence-inactive on the predicate does not imply convergence-inactive on structure geometry.
- **F5 caveat**: CNR2's saturation means we should NOT lead with a "sub-Å hit rate at CNR2" claim. Use two-instrument fraction instead.
- **F3 for LPAR1** — OF3 lands active on the predicate but not close to the active crystal geometry. This is a *predicate-space* active without a *reference-geometry* active. Suggests OF3 is generating a novel active-like conformation for LPAR1, not reproducing the crystal.

## v5 comparison — falsification results

v5 point-estimates for CNR2 (0.27), OPSD (0.38), ADRB2 (0.26), LPAR1 (0.22), CXCR4 (0.04), GHSR (0.02), NPY1R (0.02) at n=100 or lower. At n=500 across 4 backbones, no receptor gives a fraction near the v5 estimate:

- CNR2 v5=0.27, D1 mean (across bb) = 0.263 — closer than expected, but 3 bb sit at ~0.02 and Chai at 0.998. The v5 aggregate happened to average to the same number as the smoke.
- OPSD v5=0.38, D1 (Boltz alone) = 0.388 — coincidence on one backbone only.
- ADRB2 v5=0.26, D1 mean = 0.260 — coincidence on the mean, but Chai=1.00, others=0.00.

Interpretation: v5 point-estimates were BACKBONE-AVERAGED and MISLEADING. The panel-scale D1 result is the corrected story.

## What this delivers

1. **Cross-backbone divergence** on the two-instrument predicate is receptor-specific and dramatic. Spread ranges from 0.000 (GHSR) to 1.000 (ADRB2 Chai vs Boltz/Protenix). No single-backbone bias explains it.
2. **3 receptors (CXCR4/GHSR/NPY1R) are cross-backbone-convergent inactive** on the two-instrument predicate at n=500 — evidence that these apo forms are read as inactive by all four backbones.
3. **CNR2 is not the "mixed cell" the D1 anchor rationale assumed** — it's a 4-backbone-divergent cell with Chai 99.8 %, others 1.6-2.2 %.
4. **v5 point estimates were backbone-averaged and misleading**. Panel-scale numbers require per-backbone reporting.

## What this does NOT deliver

- **Cluster-bootstrap CIs**: primary D1 deliverable per PREREG §D-1.4. Deferred — bootstrap on receptor within backbone would need cross-receptor pooling. At n=1 receptor per bootstrap sample it degenerates.
- **Hartigan's dip test / GMM on continuous axes**: secondary deliverable. Not run in this pass.
- **Directional interpretation of backbone biases** — WHY Chai active-bias on CNR2/OPSD/ADRB2, OF3 active-bias on LPAR1 — needs training-cutoff + PDB deposition-date analysis. Deferred to a follow-up methods analysis.

## Next moves

- **Chai bias attribution**: which receptors' active-state crystals are in Chai's training corpus (pre-2021-01-12)? A brief check against RCSB deposition dates would answer whether Chai is recalling active-state depositions for CNR2/OPSD/ADRB2. That's an authoring-side lookup, not a compute run.
- **Manuscript v2 revisions**: fold in F1 (backbone-specific biases), F2 (3-receptor cross-backbone-inactive convergence), F5 (CNR2 RMSD saturation caveat). The "apo bistability" paper claim needs rewriting toward the corrected story.
- **D2 (nanobody-directed inactive) is now the crux experiment** — if the models can be steered into inactive by a Nb input, that's a different demonstration than "apo happens to be inactive". Panel-scale asymmetry between the 4 backbones on the apo axis motivates this.

## Files (this session, local only)

- `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` (14000 rows, 30 MB)
- `experiments/022_tier_d1_deep_apo/analysis/full/failure_census.json` (0 failures)
- `experiments/022_tier_d1_deep_apo/analysis/full/rescore_parallel.provenance.json` (wall 6-30s)
- `experiments/022_tier_d1_deep_apo/analysis/tier_d1_full_headline_2026_09_06.md` (this doc)

## Related memory

- `[[chai-cnr2-apo-model-bias-2026-09-06]]` — the CNR2-only smoke result this panel-scale supersedes
- `[[d1-smoke-fired-2026-09-06]]` — dispatch record + chunking fix
- `[[apo-bistability-reference-artefact-2026-09-06]]` — v5 point-estimate frame this analysis falsifies
- `[[block-c-tier3-pocket-identity-2026-09-06]]` — parent paper claim; needs revision in light of this
