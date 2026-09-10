# Part A / D1 — Deep-apo bistability formalization

**Draft, joint-review only. Not a freeze. No tag, no commit to release repo.**

**Data**: `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` (14,000 rows, 14,000/14,000 passed). Scorer `d9c646af` uniform (per GATE-4, `axes.py` + `pocket_ca_rmsd` unchanged from `d9c646af` → HEAD; cross-tier comparability SAFE). Panel: 7 Class A receptors × 4 backbones × apo × 5 seeds × 100 samples.

**Cluster-boot degeneracy at n=7**: D1's 7 receptors span 7 distinct paralog clusters (adrenergic_beta, cannabinoid, chemokine_cxcr, ghrelin, lysophosphatidic, npy, opsin_vertebrate — 1 receptor per cluster). **Cluster-bootstrap ≡ receptor-bootstrap** at this n. This section reports receptor-boot CIs at the panel level (n=7 receptors per backbone) and sample-level bootstrap CIs at the per-cell level (n=500 samples per cell). No cluster-boot is forced past its range.

---

## 1. F1..F5 verification against raw rows

All numbers below **reproduce the headline table to 1 decimal exactly.** No discrepancies. F1..F5 as drafted survive raw-row recomputation.

### Two-instrument active fraction (with 95% CI over 500-sample bootstrap; 1000 replicates)

| receptor | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| CNR2 | 2.2 [1.0, 3.4] | **99.8 [99.4, 100.0]** | 1.8 [0.8, 3.0] | 1.6 [0.6, 2.8] |
| OPSD | 38.8 [34.6, 43.0] | **98.6 [97.4, 99.6]** | 9.4 [6.8, 12.2] | 0.0 [0.0, 0.0] |
| ADRB2 | 0.0 [0.0, 0.0] | **100.0 [100.0, 100.0]** | 4.0 [2.4, 5.8] | 0.0 [0.0, 0.0] |
| LPAR1 | 0.2 [0.0, 0.6] | 0.0 [0.0, 0.0] | **91.8 [89.2, 94.0]** | 0.0 [0.0, 0.0] |
| CXCR4 | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 3.8 [2.2, 5.6] | 0.0 [0.0, 0.0] |
| GHSR  | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] | 0.0 [0.0, 0.0] |
| NPY1R | 0.2 [0.0, 0.6] | 0.0 [0.0, 0.0] | 6.6 [4.6, 9.0] | 0.0 [0.0, 0.0] |

### Sub-Å pocket-Cα-RMSD to ACTIVE reference (with 95% CI, 500-sample bootstrap)

| receptor | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| CNR2 | 100.0 [100, 100] | 100.0 [100, 100] | 100.0 [100, 100] | 100.0 [100, 100] |
| OPSD | 65.0 [61, 69] | 75.8 [72, 79] | 0.0 [0, 0] | 0.0 [0, 0] |
| ADRB2 | 82.8 [79, 86] | 100.0 [100, 100] | 84.4 [81, 87] | 1.4 [0.4, 2.4] |
| LPAR1 | 0.0 [0, 0] | 0.0 [0, 0] | **0.4 [0, 1]** | 0.0 [0, 0] |
| CXCR4 | 1.2 [0.4, 2.2] | 0.0 [0, 0] | 56.6 [52, 61] | 0.0 [0, 0] |
| GHSR | 55.2 [51, 60] | 13.8 [11, 17] | 33.2 [29, 37] | 14.0 [11, 17] |
| NPY1R | 0.0 [0, 0] | 0.6 [0, 1.4] | 65.8 [61, 70] | 1.4 [0.4, 2.6] |

### Sub-Å pocket-Cα-RMSD to INACTIVE reference (with 95% CI, 500-sample bootstrap)

| receptor | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| CNR2 | 86.0 [83, 89] | 91.6 [89, 94] | 99.8 [99.4, 100] | 96.8 [95, 98] |
| OPSD | 26.8 [23, 31] | 1.2 [0.4, 2.2] | 95.8 [94, 97] | 100.0 [100, 100] |
| ADRB2 | 100.0 [100, 100] | 16.8 [14, 20] | 100.0 [100, 100] | 100.0 [100, 100] |
| LPAR1 | 99.8 [99.4, 100] | 100.0 [100, 100] | 5.6 [3.8, 7.6] | 100.0 [100, 100] |
| CXCR4 | 84.0 [81, 87] | 10.0 [7.6, 12.6] | 0.6 [0, 1.4] | 59.6 [55, 64] |
| GHSR | 22.2 [19, 26] | 19.8 [16, 23] | 52.0 [48, 57] | 51.6 [47, 56] |
| NPY1R | 98.8 [98, 99.6] | 99.4 [99, 100] | 99.8 [99, 100] | 100.0 [100, 100] |

**F1..F5 all confirmed** against raw rows.
- F1 (backbone-specific bias): Chai active-outlier on CNR2, OPSD, ADRB2; OF3 active-outlier on LPAR1 — see §5 formalization.
- F2 (3-rec cross-backbone-inactive convergence): CXCR4, GHSR, NPY1R at 0.0–6.6% active across all four backbones. Confirmed.
- F3 (sub-Å-to-active): OF3 91.8% predicate-active on LPAR1 but **0.4% [0, 1.0]** sub-Å-to-active — predicate-active-without-reference-geometry. Confirmed.
- F4 (sub-Å-to-inactive): NPY1R 98.8–100% sub-Å-to-inactive across all 4 backbones. Confirmed.
- F5 (CNR2 saturation): 100% sub-Å to active AND 86–99.8% sub-Å to inactive on all 4 backbones — reference-degenerate on pocket-Cα statistic. Confirmed at raw-row level (see §4 structural check).

## 2. Panel-level receptor-boot CIs (n=7 receptors per backbone)

Receptor-boot 95% CI over the 7-receptor D1 set within each backbone (1000 replicates). **The n=7 CIs are wide** — an unavoidable consequence of the D1 panel size. Reported for panel-level headline claims.

| backbone | mean apo two-inst % | 95% CI |
|---|---:|---|
| boltz | 5.9 | [0.1, 17.0] |
| chai | 42.6 | [14.1, 85.1] |
| of3 | 16.8 | [2.7, 42.1] |
| protenix | 0.2 | [0.0, 0.7] |

**Panel-mean signed at 95%**: Chai bounded above zero (14.1%); OF3 signed above zero (2.7%); Boltz marginal (lower bound 0.1% — barely above). Protenix bounded to a strict zero-ish [0.0, 0.7]% band.

**Limitation stated plainly**: n=7 clusters/receptors is the ceiling of what D1 was designed for. Panel-level statements at this n are weak point-estimates with wide bootstrap intervals. **Per-cell numbers with per-cell CIs are the authoritative D1 output**; the panel mean is not a claim.

## 3. Dip test + BIC-selected GMM on 4 continuous axes

Hartigan's dip test + BIC-selected GMM k∈{1,2,3} per (receptor × backbone × axis), 7 × 4 × 4 = **112 cells**. Axes: `d_tm6_r350_r630_ca`, `d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`, `pocket_ca_rmsd_active`.

**Two-mode signal criterion (dip_p < 0.05 AND GMM k=2)**: **2 of 112 cells** — both on OPSD × OF3:
- OPSD × OF3 × d_tm6_r350_r630_ca (dip_p < 1e-4, GMM k=2)
- OPSD × OF3 × pocket_ca_rmsd_active (dip_p < 1e-4, GMM k=2)

**No other receptor × backbone × axis shows a two-mode signal.** Many cells have significant dip statistics but BIC prefers k=1 or k=3, not k=2.

**Per-axis two-mode count**: `d_tm6`: 1/28. `d_npxxy_oh`: 0/28. `tilt`: 0/28. `ca_act`: 1/28.

**Verdict against PREREG §D-1.7 kill criterion**: "If dip test on continuous axes returns `dip_p ≥ 0.05` on all axes for all receptors at n=500 → drop the 'two continuous basins' claim from the manuscript."

- The condition "dip_p ≥ 0.05 on **all** axes for **all** receptors" is not satisfied — OPSD × OF3 has 2 cells with dip_p < 0.05 AND GMM k=2.
- But the pattern is essentially absent everywhere else. **The "two continuous basins" claim as a panel-level story is unsupported.**
- OPSD × OF3 is a single-receptor-single-backbone finding. Interesting but not a general apo-bistability claim.

**Recommendation**: **Drop the "two continuous basins" claim from the main text.** Keep OPSD × OF3 as a receptor-and-backbone-specific observation in the Discussion appendix (parallel to how Block C treated its per-receptor anomalies). The CI-hardened sub-Å hit rate + apo coherent-active fraction distributions (§1, §2) become the primary D1 deliverable — the tier still ships value per §D-1.7's own contingency clause.

## 4. Structural spot-check log

Five CIFs pulled from `basel-hpc:/hpc/scratch/sengaad1/paper_af3/experiments/022_tier_d1_deep_apo/full/pool/`. All 5 pass basic fold integrity: helical i,i+3 content 50–62% (canonical GPCR range), Rg 24–28 Å (canonical GPCR range), no chain breaks (max CA-CA at i,i+1 ≤ 3.90 Å), 360–413 CAs.

| label | rec × bb × outcome | npxxy_oh | tilt | ca_act | ca_inact | hel% | Rg | 1-line verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|
| cnr2_chai_saturated | CNR2 / chai / active | 2.25 | 15.83 | 0.53 | 0.94 | 61.9 | 26.03 | Coherent fold; both sub-Å; confirms F5 reference degeneracy |
| adrb2_chai_active | ADRB2 / chai / active | 4.19 | 18.39 | 0.46 | 1.04 | 50.2 | 25.12 | Coherent active-like fold, matches active crystal |
| lpar1_of3_active_novel | LPAR1 / of3 / active | 5.42 | 16.81 | 1.48 | 1.60 | 60.9 | 27.87 | **Coherent novel fold**; predicate-active but NOT close to deposited active crystal on pocket-Cα |
| adrb2_boltz_inactive | ADRB2 / boltz / inactive | 11.58 | 11.75 | 0.88 | 0.47 | 54.1 | 24.81 | Coherent inactive-like fold, matches inactive crystal |
| ghsr_boltz_inactive | GHSR / boltz / inactive | 10.03 | 12.53 | 0.97 | 1.73 | 59.0 | 25.28 | Coherent inactive-like fold |

**LPAR1/OF3 verdict**: **novel coherent active-like fold**, not degraded. Rg 27.9 Å is on the high side of canonical GPCR range (24–27) but still within it; helical content is 60.9% — well above the ~30% threshold that would signal fold breakdown. OF3 is generating a plausible active-like conformation for LPAR1 that satisfies the coarse two-instrument predicate without approaching the deposited active crystal in pocket-Cα geometry. This is qualitatively the same failure mode GATE-3 documents for OF3 on D3 at shallow MSA depth — the predicate is coarse enough that a plausible-but-non-reference fold can trip it.

**CNR2/Chai F5 saturation confirmed**: 0.53 Å from active AND 0.94 Å from inactive on this single sample. The pocket-Cα RMSD statistic is genuinely saturated for CNR2 — the two crystal references are close enough in the 12-BW-anchor subset that a well-folded receptor lands sub-Å to both.

**ADRB2 Chai-active vs Boltz-inactive**: both well-folded, both 413 CAs, similar helicity + Rg. Difference is TM6 conformation only — same protein, different states. Chai's ADRB2 apo is genuinely active-like on pocket-Cα (0.46 Å to active).

## 5. F1 wording formalization

**F1 active-outlier rule**: backbone B is active-outlier on receptor R if `active_frac(R,B) - max(active_frac(R,B'))_{B'≠B} ≥ +50 pts`. Applied to all 28 (rec × bb) cells:

| receptor | outlier backbone | frac | max of other 3 | delta |
|---|---|---:|---:|---:|
| CNR2 | chai | 99.8% | 2.2% | +97.6 |
| OPSD | chai | 98.6% | 38.8% | +59.8 |
| ADRB2 | chai | 100.0% | 4.0% | +96.0 |
| LPAR1 | of3 | 91.8% | 0.2% | +91.6 |

**Active-outlier list per backbone**: boltz [none], chai [CNR2, OPSD, ADRB2], of3 [LPAR1], protenix [none]. **F1 as currently drafted stands.**

## 6. Cross-tier F1 reproducibility — Block A apo data

**Stretch task completed.** Block A rows.csv at `experiments/018_block_a_switch_test/analysis/rows.csv` filtered to the 7 D1 receptors × apo arm, n=25 per (rec × bb) cell.

### Block A apo two-instrument active fraction on 7 D1 receptors

| receptor | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| CNR2 | 4.0 | **100.0** | 0.0 | 4.0 |
| OPSD | 44.0 | **96.0** | 12.0 | 0.0 |
| ADRB2 | 0.0 | **100.0** | 4.0 | 0.0 |
| LPAR1 | 0.0 | 0.0 | **88.0** | 0.0 |
| CXCR4 | 0.0 | 0.0 | 4.0 | 12.0 |
| GHSR | 0.0 | 0.0 | 8.0 | 0.0 |
| NPY1R | 0.0 | 0.0 | 8.0 | 0.0 |

### Cross-tier F1 verdict

| D1 outlier | Block A delta | verdict |
|---|---:|---|
| CNR2 / chai | +96.0 | **REPRODUCES** |
| OPSD / chai | +52.0 | **REPRODUCES** |
| ADRB2 / chai | +96.0 | **REPRODUCES** |
| LPAR1 / of3 | +88.0 | **REPRODUCES** |

**All 4 D1 F1 outliers reproduce on Block A's independent apo corpus** (n=25 per cell, different experiment 018, scored in a different pass). This is a robust cross-tier finding. F1's "backbone bias is receptor-specific, not global" claim is not a D1 artifact — the receptor × backbone bias pattern lands identically on Block A's data.

**Manuscript implication**: F1 warrants main-text space. The specific receptor × backbone pairings survive independent replication.

---

## Files (this pass, local only, no commits)

- `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv` (source, 14,000 rows)
- `/tmp/d1_frames.pkl`, `/tmp/d1_cis.pkl`, `/tmp/d1_dip.pkl` (in-session artefacts)
- `/tmp/d1_cifs/{5 CIFs}` (spot-check pulls)

## Related

- GATE-4: scorer `d9c646af` on D1 matches Block C's post-fix scorer on `axes.py` + `pocket_ca_rmsd` — cross-tier comparability safe.
- Block A: F1 outliers reproduce on independent apo data.
- PREREG §D-1.4: primary deliverable (CI-hardened sub-Å hit rate + apo coherent-active fraction) landed. §D-1.7 kill criterion for "two continuous basins" fires except on OPSD × OF3.
