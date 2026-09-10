# GATE-2 — D3 slope derivation

**Verdict**: **Original headline slopes reproduce EXACTLY** under a specific
method (`ln(depth)` regression, `full = 4096`). No derivation script exists
on disk. Recompute is now authoritative and adds a 95% CI (cluster-boot
over 26 receptors) that was missing from the headline.

**Signed conclusion**: 3 of 4 slopes are signed negative at 95% CI; **Chai
is inconclusive** ([−2.380, +0.357] crosses zero). The headline phrase
"all 4 backbones have negative slope" is a point-estimate statement; it
does not survive the cluster-boot 95% CI test.

---

## 1. Script search — negative

Grepped for `slope`, `linregress`, `polyfit`, `%/log`, `log_depth`,
`d3_slope`, `regression` under `experiments/024_tier_d3_msa_depth/`,
`scripts/`, `side_analyses/`, `analysis/`.

Only hits:
- `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md` (the file quoting the slopes).
- `experiments/024_tier_d3_msa_depth/analysis/tier_d3_smoke_headline_2026_09_07.md`.
- `scripts/block_c_closeout/g2_refsep_vs_auroc.py` (Block C, unrelated).
- `scripts/block_c_closeout/g2_excl_agtr1.py` (Block C, unrelated).

No script computed the four D3 slopes. **The headline numbers were produced
by hand or by a one-shot inline computation that was not saved.**

## 2. Fraction verification vs raw `rows.csv`

Recomputed per-cell active fractions from
`experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` using the
class-A two-instrument predicate (`d_npxxy_y558_y753_oh < 9.082 AND
d_gpcrdb_tm6_tilt_246_637_ca > 14.932`), pooled across the 26 receptors
per (backbone × depth) cell:

| backbone | depth 8 | depth 32 | depth 128 | depth 512 | full |
|---|---:|---:|---:|---:|---:|
| Boltz | 17.77 (n=1300) | 7.00 (n=1300) | 4.92 (n=1300) | 5.38 (n=1300) | 5.08 (n=1300) |
| Chai | 25.08 (n=1280) | 20.16 (n=1270) | 19.69 (n=1300) | 18.38 (n=1300) | 19.37 (n=1260) |
| OF3 | 28.00 (n=1300) | 26.17 (n=1280) | 21.92 (n=1300) | 15.35 (n=1270) | 12.40 (n=1250) |
| Protenix | 15.54 (n=1300) | 16.77 (n=1300) | 9.69 (n=1300) | 2.08 (n=1300) | 0.08 (n=1300) |

**Matches** the headline table to two decimals for every cell.
Also matches the pre-derived `analysis/full/summary_per_cell.csv` exactly.
**Fractions are sound.**

## 3. Slope method — grid search

Fit a linear regression of `active_fraction (%)` against a function of
depth, per backbone. Tried three log bases × three treatments of "full":

| BB | log10, drop-full | ln, drop-full | log2, drop-full | log10, full=2048 | ln, full=2048 | log2, full=2048 | log10, full=4096 | **ln, full=4096** | log2, full=4096 | x=ord (0..4) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Boltz | −6.516 | −2.830 | −1.962 | −4.485 | −1.948 | −1.350 | −3.877 | **−1.684** | −1.167 | −2.700 |
| Chai | −3.413 | −1.482 | −1.027 | −2.192 | −0.952 | −0.660 | −1.877 | **−0.815** | −0.565 | −1.320 |
| OF3 | −7.007 | −3.043 | −2.109 | −6.979 | −3.031 | −2.101 | −6.290 | **−2.732** | −1.894 | −4.202 |
| Protenix | −7.883 | −3.424 | −2.373 | −7.577 | −3.290 | −2.281 | −6.806 | **−2.956** | −2.049 | −4.562 |

**Headline numbers**: Boltz −1.68, Chai −0.82, OF3 −2.73, Protenix −2.96.

**Match**: `ln(depth)` with `full = 4096`. To three decimals: Boltz −1.684,
Chai −0.815, OF3 −2.732, Protenix −2.956. **Exact.**

## 4. Method — authoritative (as recomputed)

- **Data**: `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` (25,810 rows).
- **Cell definition**: per (backbone, depth) across all 26 receptors, all seeds and samples pooled.
- **Response variable**: active fraction (%) under the class-A two-instrument predicate
  (`d_npxxy_y558_y753_oh < 9.082` AND `d_gpcrdb_tm6_tilt_246_637_ca > 14.932`).
- **Predictor**: `ln(depth)` where `depth ∈ {8, 32, 128, 512, 4096}`. The nominal `4096` value
  for the `full` label is a fitting choice — the actual per-receptor MSA depth at
  `full` ranges ~2K–11K (headline §Grid).
- **Regression**: OLS, one slope per backbone.
- **CI**: cluster-bootstrap over the 26 receptors used in D3, 1000 replicates, seed 20260910.
  Point estimate = pooled slope on the observed sample; each bootstrap replicate
  resamples receptors with replacement and re-pools.
- **The label "%/log(depth)" in the headline elides that the log is `ln`, not `log10`.**
  Correct annotation is "%/ln(depth)" or "per e-fold depth change".

## 5. Recomputed slopes + 95% CI

| Backbone | Point slope (%/ln(depth)) | Boot median | 95% CI | Signed non-zero? |
|---|---:|---:|---:|---:|
| Boltz | **−1.684** | −1.624 | [−2.692, −0.812] | **YES** |
| Chai | **−0.815** | −0.755 | [−2.380, +0.357] | **NO — crosses zero** |
| OF3 | **−2.732** | −2.662 | [−4.365, −1.145] | **YES** |
| Protenix | **−2.956** | −2.924 | [−4.678, −1.581] | **YES** |

## 6. What this changes downstream

1. **The four point estimates stand — reproduced exactly. NOT SUPERSEDED as
   point values.**
2. **The blanket claim "all 4 backbones show negative slope" does NOT
   survive cluster-boot 95% CI.** Chai's slope is inconclusive under the
   convention. The D3 headline §Findings F2 phrasing "Chai's depth-response
   is real but muted" is a point-estimate statement; under CI it becomes
   "Chai's slope is negative in point estimate but not distinguishable from
   zero under cluster-bootstrap over the 26-receptor panel."
3. **The label "%/log(depth)" is imprecise** — it's natural log, not log10.
   A manuscript sentence quoting the number needs to be `%/ln(depth)` or
   `per e-fold depth change`, else the number is off by factor ~2.303.
4. **`full = 4096` is a nominal fitting choice** — the actual full-MSA
   row count is per-receptor and ranges ~2K–11K. Alternative values (e.g.
   the per-receptor median full-depth) would shift the slopes by a fixed
   factor without changing signs. Documenting the choice as `full = 4096`
   (nominal) is a caveat, not a fault.

## 7. What this does NOT settle

- Whether cluster-boot over 26 D3 receptors matches the paralog-cluster
  convention Block A/B/C used. If the 26 receptors span fewer than 26
  paralog clusters, the true cluster-boot CI would be **wider** than what
  is reported here (this recompute treats receptors as independent). The
  paralog-cluster join is not part of GATE-2 scope; flag for the Block D
  dossier open-items list.
- Whether the *shape* of the response is truly linear in `ln(depth)`.
  Chai in particular sits flat 18–25% across all five depths — a
  saturation model would fit as well or better. Not addressed here.
- Whether "predicate-active fraction increases at shallow depth" reflects
  a real conformational shift or a fold-degradation artefact. **That is
  GATE-3's question, not GATE-2's.** GATE-2 only certifies the numbers.

## 8. Provenance

- Rows: `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` (25,810 rows).
- Path-parse regex for (rec, depth, bb): `/pool/([^/]+)/([^/]+)/([^/]+)/seed_\d+/`.
- Predicate columns: `d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`.
- Recompute output logged in this document; no new file written to `experiments/024_tier_d3_msa_depth/`.
- Bootstrap seed: 20260910.
