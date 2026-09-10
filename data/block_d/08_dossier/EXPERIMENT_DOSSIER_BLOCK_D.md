# EXPERIMENT DOSSIER — BLOCK D (D1 / D2 / D3)

**Status**: CLOSED 2026-09-10 at `block_d_freeze`. Post-cutoff-inactive-Nb search (§2.4) closed as attempted-and-documented — see `BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`. §6.5 Discussion text LOCKED. Writing agent can proceed.

**Repo state at freeze**:
- paper_af3 (working repo): closeout commit landing bundle manifest v4 alongside this dossier's release-repo close.
- paper_af3_release: `block_d_freeze` on the closeout commit; supersedes prior DRAFT commits.
- D-tier corpora on scorer `d9c646af5f89861c16062bf256de96a8389d9915` (uniform), same as Block C `rescore_t7c_full`.

**Release precedence rule** (following Block A / Block C convention):
> This document is the canonical Block D dossier of record. Where its content disagrees with any file in `analysis/block_d/`, or with the experiment-side headlines at `experiments/022_tier_d1_deep_apo/analysis/tier_d1_full_headline_2026_09_06.md`, `experiments/023_tier_d2_directed_inactive/analysis/tier_d2_full_headline_2026_09_07.md`, `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md`, **this document wins**.

**Corpora**: 42,180 predictions across three tiers. D1 = 14,000 (7 recs × 4 bb × 100 samples × 5 seeds × apo). D2 = 2,370 (4 recs × 3–4 arms × 4 bb × 10 samples × 5 seeds). D3 = 25,810 (26 recs × 5 depths × 4 bb × 10 samples × 5 seeds × apo). All three run on scorer `d9c646af5f89861c16062bf256de96a8389d9915` — cross-tier comparability trivially safe (Q2, GATE-4). Ref set `7a261988ff73eedc...` uniform.

**Phase status**:

| Phase | Status | Companion file |
|---|---|---|
| STATE_CHECK (Q1–Q6) | complete 2026-09-10 | `BLOCK_D_STATE_CHECK.md` |
| GATE-1 D2 Nb SHA audit | complete 2026-09-10 | `gates/GATE_1_D2_NB_SHA.md` |
| GATE-2 D3 slope derivation | complete 2026-09-10 | `gates/GATE_2_D3_SLOPES.md` |
| GATE-3 D3 steering vs degradation | complete 2026-09-10 | `gates/GATE_3_STEERING_VS_DEGRADATION.md` |
| GATE-4 scorer SHA discrepancy | complete 2026-09-10 | `gates/GATE_4_SCORER_DIFF.md` |
| Part A / D1 | complete 2026-09-10 | `partA/PARTA_D1.md` |
| Part A / D2 | complete 2026-09-10 | `partA/PARTA_D2.md` |
| Part A / D3 | complete 2026-09-10 | `partA/PARTA_D3.md` |
| Part B (release populate) | DEFERRED to joint review | this file (skeleton only) |
| Part C (writing bundle) | DEFERRED to joint review | this file (skeleton only) |

---

## Section 0 — Blocking questions (STATE_CHECK abbreviated)

Full detail: `BLOCK_D_STATE_CHECK.md`. Verdict summary:

- (a) **Panel of record**: established per tier (D1 = 7, D2 = 4, D3 = 26). No panel drift. All three tiers consume subsets of Block C's landed 36-rec Class A panel.
- (b) **Corpus SHAs**: uniform `d9c646af` across all three tiers. Matches Block C's `rescore_t7c_full` pose corpus. Documentation drift on phantom `891041e858f3` prose SHA in D2 + D3 headline docs; row-level authoritative.
- (c) **Chain identification**: uniform `identity_match_to_wt` (v2 anchor-hit + SIFTS) across 42,180 rows. No v1 longest-polymer regression risk.
- (d) **Reference set**: uniform `7a261988` across all D-tier rows. Nb sequences verified per GATE-1: real Nb60/Nb6/Nb9-8/Nb.AT110i1_le consumed on all four D2 arms.
- (e) **Predicate scope**: unchanged from Block C §C-5 (NPxxY-OH < 9.082 Å AND TM6 tilt > 14.932 Å). Reference-predicate calibration on D2's 4 receptors: **instrument sound** (Part A/D2 §3). NPxxY-OH calibration on Nb-anchor PDBs verified (ACM2/4MQS active passes at 4.21 Å; ADRB2/5JQH inactive fails at 11.16 Å; OPRK/6VI4 inactive fails at 12.88 Å). TM6-tilt calibration on Nb-anchors deferred as ANV.
- (f) **Paralog cluster coverage**: D1 (7 clusters), D2 (4 clusters) both degenerate at 1 rec/cluster; use receptor-boot with limitation stated. D3 (22 clusters) is cluster-boot-valid.

No hard-stop conditions triggered.

---

## Section 1 — What each tier asked, what each tier delivered

### D1 — Deep apo bistability (PREREG §D-1)

**Asked**: Harden the manuscript's apo-bistability claim from 2–4 sub-Å draws (per Block C `apo_bistability_reference_artefact_2026_09_06`) to a bootstrap-testable distribution at 10× n (100 samples/seed × 5 seeds = 500/cell). Test Hartigan's dip + GMM on continuous axes for two-mode signal.

**Delivered**:
- 14,000 preds, 0 failures. Per-(rec × bb) predicate-active fractions + sub-Å-to-active + sub-Å-to-inactive verified against raw rows to 1 decimal.
- Per-cell binomial 95 % CI at n=500 (Clopper-Pearson-style bootstrap).
- Panel-level **receptor-boot** 95 % CI at n=7 (cluster-boot ≡ receptor-boot at 1 rec/cluster degeneracy).
- Dip test + GMM on 4 continuous axes × 7 recs × 4 bb = 112 cells: **2/112 signed** (both OPSD × OF3). PREREG §D-1.7 kill fires on the two-continuous-basins claim; §D-1.7's own contingency clause retains D1 as a CI-hardened deliverable.
- Cross-tier F1 reproducibility on Block A independent data: all 4 outliers pass ≥+50-pt delta at n=25/cell (robust cross-tier finding).

### D2 — Directed inactive state via nanobody (PREREG §D-2)

**Asked**: Existence-proof of controllable two-state generation. Does inactive-directing nanobody drive the receptor to inactive on models that otherwise sample active-like?

**Delivered**:
- 2,370 preds (30 short: AGTR1 × active_nb × OF3 stragglers).
- Positive control (Gα cognate) verified: **14/16** cells ≥ 96 % active (headline mistakenly said 15/16 — one-word fix; both misses are OF3).
- Active-Nb works on 3/4 bb (Chai refuses on ACM2; AGTR1 inconclusive because apo already active-biased).
- **Inactive-Nb is unreliable** (F3). Sharpened per Part A/D2: on OPRK all 4 backbones shift **UP** toward active under inactive-Nb (Boltz +44 / Chai +8 / OF3 +10 / Protenix +6). Systematic Nb-B-as-active bias, not random noise. Flagship OPRK × Boltz cell CI [33.7, 62.6] straddles 50 % at n=50 — "approaches half" supported, "majority invert" not. All four Nb-anchor references predate every backbone's training cutoff (C-D-12) — training-data-availability is not yet ruled out as alternative to a genuine directional-steering limit.
- Reference-predicate calibration: all 4 receptors' active + inactive references calibrate correctly on both axes (or on NPxxY-OH where TM6-tilt on Nb-anchor is deferred). F3 negative not attributable to broken instrument.
- GATE-1: all 4 D2 Nb arms consumed correct real sequences. F3 stands; no rerun.

### D3 — MSA-depth ladder (PREREG §D-3)

**Asked**: Is MSA depth a controllable-sampling lever, or a fold-degradation confound?

**Delivered**:
- 25,810 preds (190 short: Chai 90 + OF3 100 on shallow-depth cells).
- Per-(bb × depth) predicate-active fraction verified. Headline table reproduces to 2 decimals from raw rows.
- Slopes recomputed via GATE-2: `%/ln(depth)` (NOT `%/log(depth)`) with `full=4096` nominal. Boltz −1.684 [−2.692, −0.812] (signed); Chai −0.815 [−2.380, +0.357] (**unsigned**); OF3 −2.732 [−4.365, −1.145] (signed); Protenix −2.956 [−4.678, −1.581] (signed). No derivation script on disk; GATE-2 recompute is authoritative.
- D3.4 propagation test extended to all 4 backbones × 5 depths per GATE-3. **Backbone split identified**: Boltz clean lever, Chai muted lever, OF3 degradation-leaning, Protenix mixed / receptor-dependent. Four converging lines of evidence: (a) predicate-active fraction, (b) sub-Å-to-active fraction, (d) matched-seed 7TM Cα RMSD, and (e) pLDDT vs `ln(depth)` slope.
- Cross-tier D1↔D3 check on 7 overlap recs: broadly consistent except **OPSD × Boltz** 3σ divergence (D1 38.8 % at n=500 vs D3-full 10.0 % at n=50). Flag but do not retract.

---

## Section 2 — Surviving claims (SC-D-1..SC-D-12)

**D1 tier**:

- **SC-D-1** — Backbone active-outlier pattern is **receptor-specific, not global**. Chai is active-outlier (≥+50 pts vs max-of-others) on CNR2 (98.4 pts) / OPSD (60.2 pts) / ADRB2 (98.0 pts); OF3 is active-outlier on LPAR1 (91.6 pts). Reproduces on Block A independent data (all 4 outliers, n=25/cell). Cross-tier robust.
- **SC-D-2** — Three receptors (CXCR4, GHSR, NPY1R) converge inactive across all 4 backbones at n=500 predicate-active fraction (max 6.6 % on any cell); v5 point estimates (~ 0.02–0.04) at n=100 did not reproduce as backbone-averaged fractions.
- **SC-D-3** — CNR2 pocket-Cα-RMSD is a **saturated statistic** (100 % sub-Å to BOTH active AND inactive references across all 4 backbones). Receptor-specific reference geometric degeneracy (active + inactive crystals are pocket-Cα close). The two-instrument predicate discriminates on CNR2 where RMSD cannot.

**D2 tier**:

- **SC-D-4** — Gα cognate is a **near-perfect positive control**. 14/16 (receptor × backbone) cells reach ≥ 96 % predicate-active. OF3 is the softest backbone (ACM2 58 %, OPRK 36 % — its two misses). Boltz + Chai + Protenix hit 100 % on all 4 cognate_gα cells.
- **SC-D-5** — Active-directing Nb reproduces Gα-active on 3/4 backbones. On ACM2 (the clean per-receptor test since AGTR1 apo is already active-biased): apo→active_nb Δ = +58 / +70 / +100 pts for Boltz / OF3 / Protenix; Chai Δ = 0 (refuses).
- **SC-D-6** — **Inactive-directing Nb is unreliable**. Panel-scale finding: no backbone reliably steers inactive on the 2 receptors with inactive-Nb arms (ADRB2, OPRK). Directional bias on OPRK: all 4 backbones shift UP toward active under inactive-Nb (Boltz +44, Chai +8, OF3 +10, Protenix +6). Systematic Nb-B-as-active prior, not random noise. All four Nb-anchor reference structures used here (5JQH, 6VI4, 4MQS, 6OS2) predate the backbones' training cutoffs (see C-D-12); memorization-availability is not yet ruled out as an alternative to a genuine directional-steering limit. Wording caveat on the OPRK × Boltz flagship cell (4 % → 48 %, Δ+44): its own binomial 95 % CI is [33.7, 62.6] at n=50, straddling 50 %. "Approaches half" is supported; "majority invert" is not. Manuscript sentences citing this cell must respect the CI.
- **SC-D-7** — Protenix has a **backbone-specific Nb-B-as-active prior**. ADRB2 × inactive_nb × Protenix 76 % active (Clopper-Pearson 95 % CI [61.8, 86.9]). Structural spot-check: Protenix generates an active receptor pocket (NPxxY-OH 4.53 Å) alongside a correctly-docked inactive-Nb (Nb chain B properly seated, 125 aa Nb60). Predicted mechanism: Protenix training data dominated by G-protein-mimetic Nbs, generalised "Nb-B → active" as prior.

**D3 tier**:

- **SC-D-8** — MSA depth modulates predicate-active sampling on all 4 backbones, but the **mechanism differs per backbone**. Signed slopes (%/ln(depth)): Boltz −1.68 (signed, lever), Chai −0.82 (unsigned under cluster-boot, muted lever), OF3 −2.73 (signed, but degradation-leaning), Protenix −2.96 (signed, but mixed/receptor-dependent). Four converging lines of evidence for the split: (a) predicate-active rises, (b) sub-Å-to-active fraction DROPS on OF3/Protenix (Boltz +8.7, Chai —, OF3 −20.9, Protenix −8.7 points full→depth-8), (d) matched-seed 7TM Cα deviation stays 1–4 Å on Boltz vs 10–14 Å on OF3 and 15–20 Å on Protenix, (e) pLDDT vs ln(depth) slope: +0.05 [unsigned] Boltz, +0.19 [signed weak] Chai, +0.68 [signed strong] OF3, +0.58 [signed strong] Protenix — the two "degradation" backbones are exactly the two whose pLDDT tracks depth.
- **SC-D-9** — Cross-backbone Kendall τ concordance table (5 depths × 6 backbone pairs = 30 values). See `partA/PARTA_D3.md` §4 for the full matrix. Highest concordance at intermediate depths; drops at both endpoints.
- **SC-D-10** — Cross-tier D1↔D3 consistency at 7 overlap receptors: broadly consistent except **OPSD × Boltz** (D1 38.8 % at n=500 vs D3-full 10.0 % at n=50). 3σ divergence. Flag but do not retract; both cells use scorer `d9c646af`; hypothesis is depth-preparation drift in D3's `full` rung not exactly reproducing D1's full-mode.

**D-tier cross-cutting**:

- **SC-D-11** — F1 (backbone active-outlier pattern is receptor-specific, not global) reproduces on Block A independent data at n=25/cell. The four D1 F1 outliers (Chai on CNR2 / OPSD / ADRB2, OF3 on LPAR1) all satisfy ≥+50-pt delta on Block A rows. Robust cross-tier — not a D1-panel artifact. Warrants main-text space.
- **SC-D-12** — OF3 + Protenix have a **coherent-non-reference-active-like-fold signature**. LPAR1/OF3 at full-depth D1 (predicate-active 91.8 %, sub-Å-to-active 0.4 %, but helix 60.9 % + Rg 27.9 Å = plausible fold, not garbage) AND Protenix AGTR1 at depth-8 D3 (predicate clears, pocket-Cα moves AWAY from active, matched-seed Cα moves 15.8 Å, but 4/4 BW anchors correct = plausible fold). Cross-tier signature: two-instrument predicate + pocket-Cα-RMSD disagreement is not a D3-shallow-MSA-only phenomenon; it's an OF3+Protenix behavioural mode.

---

## Section 3 — Withdrawals (W-D-1..W-D-10)

Each withdrawal cites the panel-scale evidence that supersedes it. Every withdrawal has a citable JSON, CIF, or bootstrap output at the release-repo path listed.

- **W-D-1** — D1 smoke's *"Chai has systematic active bias"* claim. Superseded by panel-scale F1 (SC-D-1): Chai is active-outlier on 3/7 D1 recs, inactive-consistent on 4/7. Panel evidence: `experiments/022_tier_d1_deep_apo/analysis/full/rows.csv`.
- **W-D-2** — v5 (Block C Tier 3) point estimates of apo-active-fraction as backbone-averaged claims (CNR2 v5=0.27; OPSD v5=0.38; ADRB2 v5=0.26). D1 shows the mean-across-4-bb happens to average to the v5 estimate but the underlying distribution is bimodal per backbone (Chai near 1.0, others near 0.0). Backbone-averaged reporting is misleading.
- **W-D-3** — D2 smoke's *"Boltz + OF3 respond correctly to Nb-inactive; Chai + Protenix fail"* claim. Panel-scale F3 (SC-D-6): no backbone is reliable. Boltz correct on ADRB2 but inverts on OPRK; Protenix mirror; Chai stays where it started; OF3 stable at ~10 % on both.
- **W-D-4** — Companion to W-D-3: the dichotomous "correct backbones vs failing backbones" framing. Replaced with F3's per-receptor breakdown + OPRK's unanimous_up direction as the systematic Nb-B-as-active signature.
- **W-D-5** — D3 headline F1 *"Depth is a controllable lever on all 4 backbones"*. Superseded by SC-D-8's per-backbone mechanism split (lever on Boltz clean, muted on Chai, degradation-inflated on OF3 + Protenix). GATE-3 provides the direct evidence.
- **W-D-6** — D3 headline unit label *"%/log(depth)"*. Corrected via GATE-2 to *"%/ln(depth)"* — off by factor ~2.3 otherwise. Small, load-bearing (~ 2.6× on the slope magnitude).
- **W-D-7** — D3 auto-memory `d3_full_confirmed_2026_09_08.md` header *"PREREG §D-3 hypothesis is validated on all 4 backbones"*. Replaced with backbone-specific hypothesis: confirmed for Boltz, inconclusive for Chai (unsigned under cluster-boot), refuted (as controlled lever) for OF3 + Protenix on grounds of fold-degradation at shallow depth. Memory file needs updating.
- **W-D-8** — D1 secondary deliverable *"two continuous basins"* claim (PREREG §D-1.4). Dip-test panel-scale outcome: 2/112 cells signed (both OPSD × OF3). §D-1.7 kill fires. Dropped from main text; kept as OPSD × OF3 single-cell Discussion appendix note. D1 still ships value via §D-1.7's own contingency clause.
- **W-D-9** — Any Block D framing that treats ADRB2 as a "matched-pair" receptor for D2's arm-by-arm 2×2. The active_nb slot was collision-dropped (per `block_d_d2_nanobody_collision_2026_09_09.md` + GATE-1), so ADRB2 contributes 3 arms (apo + cognate_gα + inactive_nb), not 4. Matched-pair 2×2 framing must name the drop. Inactive_nb data (200 rows across 4 bb) is scientifically clean (real 125-aa Nb60 consumed per GATE-1).
- **W-D-10** — Two headline docs cite scorer SHA `891041e858f3747b`. The SHA does not exist in git (no ref, no orphan, not in reflog). Retracted as phantom; superseded by row-level `d9c646af5f89861c16062bf256de96a8389d9915`. Same shape as Block C's T7C headline drift. Correction pass in Part B.

---

## Section 4 — Caveats (C-D-1..C-D-11)

- **C-D-1** — Cluster-boot degeneracy on D1 (7 recs, 7 clusters) and D2 (4 recs, 4 clusters). Cluster-boot = receptor-boot at 1 rec/cluster. Per-cell CIs are the authoritative D1/D2 output; panel-mean CIs are wide by construction (D1 Chai panel-mean 42.6 % [14.1, 85.1] receptor-boot, for example). D3 (22 clusters) has valid cluster-boot.
- **C-D-2** — D3 slope derivation script not on disk. Original four numbers were hand/one-shot inline compute that was not saved. GATE-2's recompute is the authoritative reproduction; note explicitly in Methods.
- **C-D-3** — Phantom scorer SHA (`891041e858f3`) in D2 + D3 headline docs (and memory `d3_full_confirmed_2026_09_08.md`). Documentation drift only; row-level `d9c646af` is authoritative. Correction pending in Part B.
- **C-D-4** — `docs/EXPERIMENT_CATALOG/sequences/partners.fasta:Nb60` mislabels a 126-aa Nb80 sequence. Never consumed by any D2 arm (GATE-1). Documentation defect; rename recommended in §6.6.
- **C-D-5** — AGTR1 × active_nb × OF3 landed 170 preds vs 200 dispatched (30 short). Reported fraction uses actual landed n = 170. Cell-specific footnote if AGTR1 active_nb figures are cited.
- **C-D-6** — D3 Chai + OF3 short 90 + 100 preds vs 26,000 dispatched, concentrated in shallow-depth cells. Reported fractions use landed denominators. Cell-specific footnote if any cell's n is quoted.
- **C-D-7** — D3 slope for Chai (−0.815) is not signed under cluster-boot 95 % CI [−2.380, +0.357]. Point estimate negative but CI crosses zero. Manuscript sentence must say "Chai's slope is negative in point estimate but not distinguishable from zero at n=22 clusters."
- **C-D-8** — Cross-tier OPSD × Boltz 3σ divergence (D1 38.8 % at n=500 vs D3-full 10.0 % at n=50). Both cells scored on `d9c646af`; panel-of-record same receptor + same predicate. Root-cause hypothesis: D3's "full" MSA rung materially differs from D1's full-mode default (D3 uses a per-depth-cell MSA subsampling pipeline; the "full" arm reflects that pipeline's identity behaviour, which is not necessarily bit-identical to Block A / D1's upstream default). Flag; do not retract.
- **C-D-9** — D2 reference-predicate calibration on Nb-anchor PDBs is partial (NPxxY-OH only). TM6-tilt calibration deferred as ANV — needs GPCRdb 2×46 / 6×37 residue mapping. Small compute (~ 30 min); deferred.
- **C-D-10** — D2 n=4 receptors is a small panel. F3 (inactive-Nb unreliable) rests on 2 receptors (ADRB2, OPRK). A third inactive-Nb receptor (CCR5 candidate) would strengthen generalisation. Named as ANV.
- **C-D-11** — MCHR1 D3 ligand_rmsd_to_ref: GATE-4 originally flagged 990 rows populated (all MCHR1); Part-A-D3 disputed with 100 % NaN. Reconciled 2026-09-10 in this pass: **Part-A-D3 is correct**. Empirical recount on `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` shows 25,810 / 25,810 rows NaN on `ligand_rmsd_to_ref` (0 populated). GATE-4's 990 claim retracted. Bug #4's `NOT MATERIAL` verdict stands unchanged. C-D-11 downgraded from active caveat to closed-reconciliation note.
- **C-D-12** — All four D2 Nb-anchor reference structures (5JQH, 6VI4, 4MQS, 6OS2) predate model training cutoffs on all four backbones (per Part A/D2 §8; anchors deposited 2013–2020 vs earliest training cutoff Chai-1 2021-01-12). SC-D-6's negative finding (inactive-Nb unreliable) cannot currently be distinguished from a training-data-availability effect: the models may be "recognising" the co-deposited state rather than integrating the Nb chain as a state-directing partner. Disambiguating experiment: a post-cutoff inactive-Nb test on a receptor + Nb complex deposited after 2023-06-01 (see joint-review §2.4). Not yet run.

---

## Section 5 — Manuscript-facing flags (D-1..D-12)

- **D-1** — Cluster-boot authoritative except at n < 10 clusters where receptor-boot equals it AND must be stated. D1/D2 use receptor-boot with explicit limitation; D3 (22 clusters) uses cluster-boot.
- **D-2** — D3 slope unit is `%/ln(depth)`. Any manuscript figure or table quoting slopes needs the correct unit label.
- **D-3** — D3 backbone-specific mechanism: LEVER for Boltz, MUTED (unsigned) for Chai, DEGRADATION-inflated for OF3 + Protenix. Do not describe OF3 or Protenix as controllable levers on the depth axis.
- **D-4** — D1 two-continuous-basins claim was pre-registered secondary and dropped by dip-test outcome. Main text should not carry it.
- **D-5** — F1 (backbone active-outlier receptor-specificity) is a cross-tier finding; reproduces on Block A. Warrants main-text space.
- **D-6** — OF3 + Protenix have a coherent-non-reference-active-like-fold signature (LPAR1 at full-depth D1; Protenix AGTR1 at shallow-depth D3). Cross-tier, not D3-specific.
- **D-7** — All three D-tier corpora share scorer `d9c646af`. Cross-tier comparability trivially safe. Phantom SHA `891041e858f3` in D2 / D3 headline docs needs correction.
- **D-8** — Panel-scale F3 "no backbone reliably steers inactive" is a negative finding subject to a training-data-availability confound (C-D-12). Main-text framing LOCKED per §6.5 (2026-09-10). Post-cutoff-inactive-Nb search closed as attempted-and-documented; see `BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`. Writing agent uses §6.5's exact wording.
- **D-9** — D2 Gα positive control is 14/16 cells ≥ 96 % (headline said 15/16). One-word fix in any manuscript sentence.
- **D-10** — D2 F3 OPRK unanimous_up direction: all 4 backbones shift UP toward active under inactive-Nb (Boltz +44 / Chai +8 / OF3 +10 / Protenix +6). Systematic bias, not random. Manuscript sentence must convey the directional pattern. **The flagship OPRK × Boltz cell (4 % → 48 %) has 95 % binomial CI [33.7, 62.6] at n=50** — "approaches half" is supported; "majority invert" is not. Writing agent to respect the CI.
- **D-11** — D2 F1 mistake propagation: any prior sentence quoting "15/16" as the Gα positive-control cell count needs correction to 14/16.
- **D-12** — D2 reference-predicate calibration on Nb-anchor PDBs (NPxxY-OH) verified: F3's negative finding is NOT due to a broken instrument.

---

## Section 6 — Open for Adjudication

*This is the actual deliverable for the joint session. Aditya's decisions land here.*

### 6.1 — GATE verdicts (one line each)

- **GATE-1 (D2 Nb SHA)**: **false alarm**. All 4 D2 Nb arms consumed correct real sequences (Nb60 125 aa / Nb6 133 aa / Nb9-8 125 aa / Nb.AT110i1_le 128 aa). F3 stands as drafted.
- **GATE-2 (D3 slopes)**: original point estimates reproduce exactly under `%/ln(depth)` (NOT `%/log(depth)`) with `full=4096` nominal. **Chai's slope [−2.380, +0.357] crosses zero** under cluster-boot 95 % CI — unsigned. No derivation script on disk; GATE-2 recompute is authoritative.
- **GATE-3 (D3 steering vs degradation)**: **the split IS the finding**. Boltz clean lever; Chai muted lever; OF3 degradation-leaning; Protenix mixed / receptor-dependent. Four converging lines of evidence (predicate-active, sub-Å-to-active, matched-seed 7TM Cα, pLDDT vs depth).
- **GATE-4 (scorer SHA)**: **cross-tier comparability SAFE**. All three D-tier corpora share scorer `d9c646af`; `axes.py` + `pocket_ca_rmsd` UNCHANGED from `d9c646af` to HEAD. Bug #4 (`9e640d5`) NOT ancestor of `d9c646af`; not material to D-tier (D1/D2/D3 have no populated `ligand_rmsd_to_ref` — GATE-4 flagged 990 MCHR1 rows but Part-A-D3 could not reproduce; reconciliation open, non-blocking). **Documentation drift**: `891041e858f3` cited in headline docs is a phantom SHA that does not exist in git.

### 6.2 — D2 rerun call

**MOOT per GATE-1**. All 4 D2 Nb arms consumed correct real sequences. No rerun warranted. Independent D2 augmentation motivations remain live as future experiments (see §6.6): (a) curate real Nb80 to un-drop ADRB2 active_nb, (b) add a third inactive-Nb receptor (CCR5 candidate). These are forward-planning, not remediation.

### 6.3 — D2 dossier shape (standalone vs appendix)

Both framings drafted in `partA/PARTA_D2.md` §5 (standalone) and §6 (appendix). **My lean, clearly marked as a lean, not a decision**: **standalone** — F3 is a negative existence-proof with panel-scale evidence + a structural signature (OPRK unanimous_up direction, Protenix Nb-B-as-active prior verified in CIFs). The Gα positive-control at 14/16 ≥ 96 % gives the sentence a floor. Bury it in an appendix and it reads as an afterthought; give it main-text space and it says something the field should hear.

**Counterargument if you disagree**: the panel is 4 receptors and F3 rests on 2 (ADRB2 + OPRK). At n=2 the panel-scale claim is fragile; the appendix framing preserves the finding without over-selling generalisation. Aditya's call.

### 6.4 — D3 mechanism: why controllable toward active and not inactive? (Kickoff Q3)

**Candidate explanations, with what this pass supports or undermines**:

1. **Training asymmetry** — most nanobody-bound structures in PDB training corpora are G-protein-mimetic active stabilisers (Nb80 / Nb9-8 / Nb.AT110i1_le / mini-G-derived). Models see "Nb-B-chain → active" as the dominant conditional. **Supported**: Protenix's F4 Nb-B-as-active prior fires exactly this pattern on ADRB2 inactive_nb. **Undermined by**: Boltz's OPRK inversion — Boltz has the largest OPRK Δ (+44) but is otherwise the cleanest lever on D3. If it were pure training asymmetry we'd expect all 4 backbones symmetric; only Protenix is symmetric.

2. **Active-pocket entropy is lower than inactive-pocket entropy** — active state has more constraints (G-protein binding, agonist coordination, NPxxY packing). Models are better at "converge to the specific active pose" than "avoid the specific inactive pose". **Supported by**: F5 CNR2 saturation on D1 (100 % sub-Å to BOTH refs) — the models can't distinguish, they collapse to the mean pocket. **Supported by**: F1 Gα cognate at 14/16 ≥ 96 % vs F3 inactive-Nb at 2/8 correct sign. Active-direction has a stronger internal signal.

3. **Coarse predicate confounds** — NPxxY-OH + TM6-tilt are two distances. The models may generate structures that satisfy these distances without approaching either reference pocket. **Supported by**: GATE-3's Protenix + OF3 degradation signature — predicate clears, sub-Å-to-active DROPS. Also LPAR1/OF3 on D1 (91.8 % predicate-active, 0.4 % sub-Å-to-active). This is a real confound of the readout, not the mechanism.

4. **Nb-B chain length + secondary structure** — the ~125–133 aa nanobody chain forms a specific β-sandwich CDR-loop scaffold regardless of state. Models may read the Nb fold shape more than the CDR3 residues. **Supported by**: Chai receptor-locking (F5) — Chai reads the receptor's own registration, ignores whichever Nb is attached. **Undermined by**: ACM2 active-Nb WORKS on 3/4 bb (Boltz +58, OF3 +70, Protenix +100) — Nb-B chain is not enough on its own; the CDR3 chemistry does matter for active-Nb.

Do not pick one. The four explanations are not mutually exclusive; each has partial support. The manuscript's Discussion sentence should probably layer at least (1) + (2) + (3) — training asymmetry + active-pocket-entropy floor + coarse-predicate confound. (4) is speculative.

### 6.5 — Framing (LOCKED 2026-09-10)

> *"Partner identity drives model state-readout asymmetrically, and — as tested — only in the active direction. Cognate Gα and active-directing nanobodies reliably drive the models to active-like sampling (14/16 Gα cells ≥ 96%; active-Nb Δ up to +100 points on 3/4 backbones). Inactive-directing nanobodies did not produce a reliable shift toward inactive on either receptor tested (ADRB2, OPRK); the failure is directionally systematic rather than random — all four backbones drift toward active under inactive-Nb on OPRK. Every inactive-Nb reference used in this test predates the backbones' training cutoffs, so this result cannot be distinguished from a training-data-availability effect. We searched for a post-cutoff inactive-directing nanobody structure to resolve this; no candidate identified could be verified as both genuinely post-cutoff and a genuine state-directing reagent within the scope of this study (see `BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`). We report the protocol as demonstrated for active-direction; whether directed inactive generation is achievable remains open."*

This is the final Discussion text for the D2 framing. The post-cutoff-inactive-Nb search (§2.4) closed as attempted-and-documented, not resolved. Full search record + candidate-by-candidate disposition + reusable filter rule at `BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`.

### 6.6 — Anything else genuinely judgment-call

Not resolved autonomously; recorded here for adjudication:

1. **`partners.fasta:Nb60` mislabel rename** — the 126-aa sequence under the `Nb60` header is Nb80 (CDR3 matches 3P0G Nb80). Never consumed by any D2 arm; documentation defect only. Rename to `Nb80` recommended. Would touch `docs/EXPERIMENT_CATALOG/sequences/partners.fasta`; not a data file. **Small edit; recommend approve.**

2. **Auto-memory `d3_full_confirmed_2026_09_08.md` update** — carries the phantom `891041e858f3` SHA AND the "PREREG §D-3 hypothesis is validated on all 4 backbones" claim. Both need updating. Would use the memory system's update path. **Recommend approve — otherwise the memory misleads future sessions.**

3. **Cross-tier D1↔D3 OPSD × Boltz 3σ divergence** (C-D-8) — do we want a follow-up run to reconcile, or a footnote citing both numbers and noting the divergence? Follow-up is cheap (a single D3-style dispatch on OPSD × Boltz alone at n=500). **Small; propose deferral to a follow-up methods note.**

4. **D3 slope re-derivation** — GATE-2 recomputed but did not commit a script to `analysis/block_d/scripts/`. Would be a small `derive_d3_slopes.py` (~50 lines). Should this land as part of Part B, or explicitly stay ANV? **Recommend: land as part of Part B — the recompute is trivial and reproducibility matters.**

5. **D2 augmentation** — Nb80 curation to un-drop ADRB2 active_nb + third inactive-Nb receptor (CCR5 or similar). Both are compute-costly forward experiments, not remediation. **Recommend: park as future D-tier extension; do not gate current dossier on either.**

6. **MCHR1 D3 ligand_rmsd_to_ref reconciliation** (C-D-11) — GATE-4 vs Part-A-D3 disagree. Non-blocking (Bug #4 verdict stands either way). Would take 10 minutes to re-run the check. **Recommend: quick reconciliation in a follow-up; do not block dossier on it.**

### Structural spot-check log (curated CIFs opened this pass)

- **D1** — LPAR1/OF3 apo (predicate 91.8 %, sub-Å-to-active 0.4 %): novel coherent active-like fold; helix 60.9 %, Rg 27.9 Å, no chain breaks. CIF at `/hpc/scratch/sengaad1/paper_af3/experiments/022_tier_d1_deep_apo/full/pool/lpar1/apo/of3/...`.
- **D1** — CNR2/Chai apo: 100 % sub-Å to BOTH refs; confirmed reference geometric degeneracy.
- **D1** — ADRB2/Chai vs ADRB2/Boltz apo: same receptor, different predicate outcome (100 % vs 0 %).
- **D1** — GHSR any-bb apo: inactive-like, confirms F2.
- **D2** — ADRB2 × inactive_nb × Protenix sample_0: Nb60 chain B correctly docked (125 aa), receptor NPxxY-OH 4.53 Å (active-like). Confirms F4 at atomic level.
- **D2** — ADRB2 × inactive_nb × Boltz sample_0: Nb60 docked, NPxxY-OH inactive-like — F3 correct-case.
- **D2** — OPRK × inactive_nb × Boltz sample_0: Nb6 docked, NPxxY-OH 11.27 Å inactive-like on this sample (48 % inversion is stochastic across 50).
- **D2** — ACM2 × active_nb × Chai sample_0: Nb9-8 correctly docked, NPxxY-OH 19.1 Å strongly inactive — F5 confirmed at atomic level.
- **D3** — Protenix AGTR1 depth-8 vs depth-full: matched seed + sample. pocket_ca_rmsd_active 0.76 → 1.24 Å (WORSENS); NPxxY predicate clears (11 → 3.4 Å); TM6 tilt clears (11 → 17 Å); 7TM Cα deviation 15.8 Å from full. 4/4 BW anchors correct in both. Confirms "coherent non-reference fold" at shallow depth.
- **D3** — Boltz OPSD depth-8: pocket_ca_rmsd_active 1.25 → 0.41 Å (IMPROVES). Confirms Boltz clean lever.

### Things found but explicitly NOT fixed (audit-first-fix-separately)

- Phantom SHA `891041e858f3` in D2 headline (line 6), D3 headline (line 6), memory `d3_full_confirmed_2026_09_08.md`. No file touched.
- `partners.fasta:Nb60` mislabel. No file touched.
- Auto-memory `d3_full_confirmed_2026_09_08.md` still says "validated on all 4 backbones". No update.
- MCHR1 ligand_rmsd disagreement between GATE-4 (990 populated) and Part-A-D3 (100 % NaN). No investigation beyond flagging.
- D3 slope derivation script does not exist on disk. No script written (recomputed inline in GATE-2).
- AGTR1 × active_nb × OF3 30-row shortfall. No rerun.
- D3 Chai + OF3 190-pred shortfall on shallow depth. No rerun.

---

## Section 7 — Skeleton for Parts B + C (DEFERRED to joint review)

*Not populated this pass; framework for the joint session's decisions.*

### Part B — release repo population

Following Block A / Block B / Block C convention:

- `paper_af3_release/dossiers/BLOCK_D/EXPERIMENT_DOSSIER_BLOCK_D.md` — this file (final version after §6 adjudication).
- `paper_af3_release/dossiers/BLOCK_D/{ASSUMED_NOT_VERIFIED_BLOCK_D.md, BLOCK_D_STATE_CHECK.md}` — companion.
- `paper_af3_release/analysis/block_d/` — MISSING; needs creation.
- `paper_af3_release/claims/` — append SC-D-1..12 to LEDGER.csv per Block A/B/C shape.
- `paper_af3_release/caveats/` — 11 new files C-D-1..11.
- `paper_af3_release/withdrawals/` — 10 new files W-D-1..10.
- `paper_af3_release/data/block_d/{d1,d2,d3}/` — MANIFEST_RAW_ROWS.md pinning the 3 rows.csv files by SHA (per Block C data-in-git-convention: raw CSVs pinned, not shipped).
- `paper_af3_release/VERSION.md` — D1/D2/D3 rows populated with scorer `d9c646af` + tag `block_d_freeze` (placed at closeout 2026-09-10).

### Part C — writing bundle

- `block_d_figure_data.zip` — self-contained, mirroring Block C's v2.1 structure. Contents:
  - `01_claims/BLOCK_D_CLAIM_SHEET.md`
  - `02_caveats/` (11 C-D-# files)
  - `03_withdrawals/` (10 W-D-# files)
  - `04_flags/BLOCK_D_MANUSCRIPT_FLAGS.md` (D-1..12)
  - `05_state_check/BLOCK_D_STATE_CHECK.md`
  - `06_gate_reports/{GATE_1..4}.md`
  - `07_partA/{PARTA_D1..D3}.md`
  - `08_dossier/EXPERIMENT_DOSSIER_BLOCK_D.md`
  - `09_references/{tier_d1_panel.csv, tier_d2_panel.csv, tier_d3_panel.csv, nanobody_state_anchors.csv, paralogy_clusters.csv}`
  - `10_structures/` — curated best/worst/exemplar + random-sample CIFs, mirroring Block A/B/C practice.
- SHA-256 manifest at `artefacts/block_d_figure_data_manifest.md` (analogous to Block C v2.1).

### Tag position

`block_d_freeze` placed at closeout 2026-09-10 on the commit that landed the locked §6.5 + `BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`.

---

**End DRAFT.** Next step is joint review of §6.
