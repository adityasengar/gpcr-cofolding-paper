# BLOCK D — Claim Sheet (SC-D-1..12)

**Status**: DRAFT (2026-09-10). Freeze tag `block_d_freeze` **NOT placed** — held pending §2.4 post-cutoff-inactive-Nb test decision.

**Corpora**: D1 = 14,000 preds (`experiments/022_tier_d1_deep_apo/analysis/full/rows.csv`); D2 = 2,370 (`experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv`); D3 = 25,810 (`experiments/024_tier_d3_msa_depth/analysis/full/rows.csv`). All three on scorer `d9c646af5f89861c16062bf256de96a8389d9915`; `ref_set_csv_sha256 = 7a261988ff73eedc...` uniform.

**CI convention** (per D-flag D-1): D3 (22 paralog clusters, 26 recs) uses cluster-boot 95 % CI. D1 (7 recs, 7 clusters) and D2 (4 recs, 4 clusters) use receptor-boot with explicit degeneracy statement — cluster-boot at 1 rec/cluster adds nothing.

---

## D1 tier — Deep apo bistability (14,000 preds, 7 recs, apo arm only, 500 samples/cell)

- **SC-D-1** — Backbone active-outlier pattern is **receptor-specific, not global**. Chai active-outlier (≥+50 pts vs max-of-others) on CNR2 (Δ 98.4 pts), OPSD (60.2), ADRB2 (98.0); OF3 on LPAR1 (91.6). Reproduces on Block A independent data at n=25/cell across all 4 outliers — robust cross-tier finding.
- **SC-D-2** — Three receptors (CXCR4, GHSR, NPY1R) converge inactive across all 4 backbones at n=500 predicate-active fraction (max 6.6 % on any cell). v5 point estimates at n=100 did not reproduce as backbone-averaged fractions.
- **SC-D-3** — CNR2 pocket-Cα-RMSD is a **saturated statistic** (100 % sub-Å to BOTH active AND inactive references across all 4 backbones). Receptor-specific reference geometric degeneracy — active + inactive crystals are pocket-Cα close. Two-instrument predicate discriminates on CNR2 where RMSD cannot.

## D2 tier — Directed inactive-state (2,370 preds, 4 recs, 3–4 arms each, 50 samples/cell)

- **SC-D-4** — Gα cognate is a **near-perfect positive control**. 14/16 (rec × bb) cells reach ≥ 96 % predicate-active. Both misses are OF3 (ACM2 58 %, OPRK 36 %). Boltz + Chai + Protenix hit 100 % on all 4 cognate_gα cells.
- **SC-D-5** — Active-directing Nb reproduces Gα-active on 3/4 backbones. Clean per-receptor test on ACM2 (AGTR1 apo already active-biased): apo→active_nb Δ = +58 / +70 / +100 pts for Boltz / OF3 / Protenix; Chai Δ = 0 (refuses).
- **SC-D-6** — **Inactive-directing Nb is unreliable**. Panel-scale: no backbone reliably steers inactive on the 2 receptors with inactive-Nb arms (ADRB2, OPRK). Directional bias on OPRK: all 4 backbones shift UP toward active under inactive-Nb (Boltz +44, Chai +8, OF3 +10, Protenix +6). Systematic Nb-B-as-active prior, not random noise. **All four Nb-anchor references (5JQH, 6VI4, 4MQS, 6OS2) predate every backbone's training cutoff** (see C-D-12); memorization-availability not yet ruled out as alternative to a genuine directional-steering limit. **Flagship OPRK × Boltz cell (4 % → 48 %, Δ+44) has 95 % binomial CI [33.7, 62.6] at n=50** — "approaches half" is supported; "majority invert" is not.
- **SC-D-7** — Protenix has a **backbone-specific Nb-B-as-active prior**. ADRB2 × inactive_nb × Protenix 76 % (Clopper-Pearson 95 % CI [61.8, 86.9]). Structural spot-check: Protenix generates active receptor pocket (NPxxY-OH 4.53 Å) alongside correctly-docked inactive-Nb (chain B properly seated, 125-aa Nb60). Predicted mechanism: Protenix training data dominated by G-protein-mimetic Nbs, generalised "Nb-B → active" as a prior.

## D3 tier — MSA-depth ladder (25,810 preds, 26 recs, 5 depths, apo arm only, 50 samples/cell)

- **SC-D-8** — MSA depth modulates predicate-active sampling on all 4 backbones, but the **mechanism differs per backbone**. Cluster-boot 95 % CI slopes (%/ln(depth)): Boltz **−1.68** [−2.69, −0.81] (signed, LEVER); Chai **−0.82** [−2.38, +0.36] (UNSIGNED, muted); OF3 **−2.73** [−4.37, −1.15] (signed, but degradation-leaning); Protenix **−2.96** [−4.68, −1.58] (signed, but mixed/receptor-dependent). Four converging lines of evidence for the split: (a) predicate-active rises; (b) sub-Å-to-active fraction DROPS on OF3/Protenix (Boltz +8.7, Chai —, OF3 −20.9, Protenix −8.7 points, full→depth-8); (d) matched-seed 7TM Cα deviation stays 1–4 Å on Boltz vs 10–14 Å on OF3 and 15–20 Å on Protenix; (e) pLDDT vs ln(depth) slope: +0.05 [unsigned] Boltz, +0.19 [signed weak] Chai, +0.68 [signed strong] OF3, +0.58 [signed strong] Protenix — the two "degradation" backbones are exactly the two whose pLDDT tracks depth.
- **SC-D-9** — Cross-backbone Kendall τ concordance table (5 depths × 6 backbone pairs = 30 values). Highest concordance at intermediate depths; drops at both endpoints. Full matrix at `07_partA/PARTA_D3.md §4`.
- **SC-D-10** — Cross-tier D1↔D3 consistency at 7 overlap receptors: broadly consistent except **OPSD × Boltz** (D1 38.8 % at n=500 vs D3-full 10.0 % at n=50). 3σ divergence. Flag but do not retract; both cells use scorer `d9c646af`; hypothesis is depth-preparation drift in D3's `full` rung not exactly reproducing D1's full-mode.

## D-tier cross-cutting

- **SC-D-11** — F1 (D1) backbone active-outlier pattern reproduces on Block A independent data at n=25/cell. Four outliers (Chai on CNR2, OPSD, ADRB2; OF3 on LPAR1) all satisfy ≥+50-pt delta on Block A rows. Robust cross-tier — not a D1-panel artifact.
- **SC-D-12** — OF3 + Protenix have a **coherent-non-reference-active-like-fold signature**. LPAR1/OF3 at full-depth D1 (predicate-active 91.8 %, sub-Å-to-active 0.4 %, helix 60.9 %, Rg 27.9 Å — plausible fold, not garbage) AND Protenix AGTR1 at depth-8 D3 (predicate clears; pocket-Cα moves AWAY from active; matched-seed Cα moves 15.8 Å; 4/4 BW anchors correct — plausible fold). Cross-tier signature: two-instrument predicate + pocket-Cα-RMSD disagreement is not a D3-shallow-MSA-only phenomenon; it's an OF3+Protenix behavioural mode.

---

**See also**: `02_caveats/` (C-D-1..12), `03_withdrawals/` (W-D-1..10), `04_flags/BLOCK_D_MANUSCRIPT_FLAGS.md` (D-1..12), `08_dossier/EXPERIMENT_DOSSIER_BLOCK_D.md` (canonical dossier of record).
