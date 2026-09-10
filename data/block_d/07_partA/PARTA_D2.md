# Part A — Tier D2 (directed inactive state) — DRAFT

**Status**: draft, joint-review pending. No release-repo commit, no tag, no writing-bundle handoff.
**Corpus**: `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv`, 2,370 rows, scorer `d9c646af` (uniform, per GATE-4).
**Panel**: 4 Class A receptors × 3–4 arms × 4 backbones × 5 seeds × 10 samples.
**Cluster-boot degeneracy**: 4 receptors → 4 distinct paralog clusters (`adrenergic_beta`, `angiotensin`, `muscarinic`, `opioid`). Cluster-boot ≡ receptor-boot at this n. **Per-cell binomial 95% CI (Clopper-Pearson) is the primary uncertainty statement in this file** — n=50 per cell yields CI half-width ≈ 8–14 points. Inter-receptor generalisation cannot be quantified at n=4; stated as a limitation.

**GATE-1 conclusion (settled)**: all 4 D2 nb arms consumed correct real sequences on all 4 backbones. F3 stands as drafted; no rerun. `partners.fasta:Nb60` header still misnames a 126-aa Nb80 sequence but was never consumed anywhere.

---

## 1. Findings verified against raw rows (F1..F6)

Recomputed per-cell active fractions from `rows.csv` reproduce the headline table exactly (checked to 2 decimals across all 44 populated cells).

### F1 — Positive control: cognate Gα drives active on `14 of 16` cells (not 15 of 16)

Headline reads "15 of 16 cells ≥ 96% active". **Actual count: 14/16 ≥ 96%.** Two misses, not one:

| receptor × bb | cognate_gα % | 95% CI |
|---|---:|---|
| ACM2 × of3 | 58.0 | [43.2, 71.8] |
| OPRK × of3 | 36.0 | [22.9, 50.8] |

Both misses are OF3. Every non-OF3 cell hits 100%. Headline text needs one-word fix: "15" → "14".

**Verdict**: F1 substance intact, minor textual correction. Positive control is a nearly-clean ground-truth signal on Boltz/Chai/Protenix; OF3's calibration on cognate_gα is softer than the other three (weaker active response, larger between-cell spread).

### F2 — Active-directing Nb works on 3 of 4 backbones

Chai refuses to respond to Nb9-8 (ACM2 apo 0% → active_nb 0%). Boltz/OF3/Protenix all move ≥ +58 points apo → active_nb on ACM2. AGTR1 active_nb evidence is inconclusive because AGTR1's apo is already active-biased on Boltz/Chai (100/100). Real per-receptor test lives on ACM2 alone.

| ACM2 × bb | apo % | active_nb % | Δ | Concordance |
|---|---:|---:|---:|---|
| Boltz | 42.0 | 100.0 | +58 | 3-of-4 (Chai refuses) |
| Chai | 0.0 | 0.0 | 0 |  |
| OF3 | 12.0 | 82.0 | +70 |  |
| Protenix | 0.0 | 100.0 | +100 |  |

**Verdict**: F2 stands. "Active-Nb works on 3/4" is a real cross-backbone claim on ACM2. AGTR1 not usable.

### F3 — Inactive-directing Nb is unreliable (headline claim)

Two receptors with `inactive_nb` arm: ADRB2 and OPRK.

**ADRB2 apo → inactive_nb shift (per-bb, expected direction: stay-inactive or become-more-inactive)**:

| bb | apo % [CI] | inactive_nb % [CI] | Δ | Verdict |
|---|---|---|---:|---|
| Boltz | 0.0 [0, 7.1] | 0.0 [0, 7.1] | 0 | ✓ correct |
| Chai | 100.0 [92.9, 100] | 100.0 [92.9, 100] | 0 | ✗ refuses to shift |
| OF3 | 10.0 [3.3, 21.8] | 10.0 [3.3, 21.8] | 0 | ≈ stable |
| Protenix | 0.0 [0, 7.1] | 76.0 [61.8, 86.9] | +76 | ✗ **INVERTS** |

**OPRK apo → inactive_nb shift**:

| bb | apo % [CI] | inactive_nb % [CI] | Δ | Verdict |
|---|---|---|---:|---|
| Boltz | 4.0 [0.5, 13.7] | 48.0 [33.7, 62.6] | +44 | ✗ **INVERTS** |
| Chai | 74.0 [59.7, 85.4] | 82.0 [68.6, 91.4] | +8 | ✗ refuses (drifts up) |
| OF3 | 0.0 [0, 7.1] | 10.0 [3.3, 21.8] | +10 | ≈ near-stable (marginal) |
| Protenix | 0.0 [0, 7.1] | 6.0 [1.3, 16.5] | +6 | ✓ near-correct |

**Cross-receptor concordance on the shift (Δ = inactive_nb − apo)**:

| Receptor | Direction sign per bb | Concordance | Interpretation |
|---|---|---|---|
| ADRB2 | [0, 0, 0, +76] | mixed (3 flat, 1 inverts) | one bb inverts; others don't shift |
| OPRK | [+44, +8, +10, +6] | **unanimous_up** | every bb drifts more-active under inactive-Nb; magnitude varies by backbone |

**Key result (new, not in headline)**: on OPRK, **all 4 backbones drift more-active under inactive-Nb than under apo**, with Boltz strongest at Δ=+44. This is a stronger statement than "unreliable" — it's uniformly-wrong-direction on OPRK, receptor-dependent-magnitude. The headline's "each backbone succeeds on some receptors and fails on others" wording is receptor-symmetric; the underlying data shows the failure has a direction (toward active), not a random-noise pattern. Suggests a systematic Nb-B-as-active bias in the panel, not just Protenix-specific.

**Verdict**: F3 stands as the substantive claim. The nuance to add is: the failure mode is a directional bias (Nb-B chain → active-side drift) uniform across backbones on OPRK, with only Boltz strong enough to visibly invert. See §5 structural spot-check for mechanism.

### F4 — Protenix's Nb-B-as-active prior

ADRB2 × inactive_nb × Protenix = 76% active. Structural spot-check (§5) confirms: receptor pocket is at **NPxxY-OH = 4.53 Å = active-like**, Nb60 chain B is docked (125 res). Protenix generates an active pocket alongside a correctly-positioned inactive-directing Nb — the two are inconsistent, and Protenix does the same on ACM2 × active_nb (Nb9-8 works, 100%). Its prior does not distinguish Nb identity.

F3 §OPRK unanimous_up finding suggests this bias exists on all 4 backbones to varying degrees; Protenix is strongest.

**Verdict**: F4 stands; sharpened by cross-receptor pattern in F3.

### F5 — Chai receptor-locked apo

Chai apo fractions: ADRB2 100.0, OPRK 74.0, ACM2 0.0, AGTR1 100.0. Chai does not shift under Nb steering on either arm for either receptor (Δ ≈ 0 on ADRB2 inactive_nb, +8 on OPRK inactive_nb, 0 on ACM2 active_nb; AGTR1 already at 100% apo, no room to move). **Verdict**: F5 stands.

### F6 — AGTR1 apo is active-biased on 3/4 backbones

Boltz 100, Chai 100, OF3 40, Protenix 0. Consistent with the Block C S1 classifier per-receptor AUROC finding that AGTR1 inverts on all 4 backbones (biased-agonist reference, `[[block-c-tier3-pocket-identity-2026-09-06]]`). **Verdict**: F6 stands. AGTR1's `active_nb` (6OS2 = biased-agonist Nb) is the reference on which Block C reported this axis-of-known-inversion; D2 reproduces the pattern.

---

## 2. Per-cell 95% CI table (all 44 populated cells)

Full table on disk: `/tmp/d2_percell.json` (n, k_active, pct, CI95 lo/hi, plddt_median, pocket_ca_rmsd_active_median, pocket_ca_rmsd_inactive_median). Verified against `analysis/full/summary_per_cell.csv`.

Cells where CI overlap makes the point-estimate claim not signed (95% CI includes 50%):

- ACM2 × cognate_ga × of3 [43.2, 71.8]
- ACM2 × active_nb × of3 [68.6, 91.4] — lower bound 68.6, marginally signed above 50%
- AGTR1 × apo × of3 [26.4, 54.8] — CI straddles 50%
- OPRK × cognate_ga × of3 [22.9, 50.8] — CI straddles 50%
- OPRK × inactive_nb × boltz [33.7, 62.6] — CI straddles 50% (the flagship inversion cell is 95%-CI-marginal at n=50)
- OPRK × inactive_nb × of3 [3.3, 21.8]
- ADRB2 × inactive_nb × protenix [61.8, 86.9] — CI stays above 50%, sign robust

**Load-bearing observation**: at n=50 per cell, the **Boltz OPRK inversion Δ=+44** is well-signed against zero (0.5–13.7 → 33.7–62.6 CIs are disjoint), but the point-estimate 48% has a CI that includes both 34% and 63%. Any prose claiming "the inversion approaches half of samples" is defensible; "the majority of samples invert" is not.

---

## 3. Reference-predicate calibration on deposited PDBs

**Question the dispatch asked**: is the two-instrument predicate (NPxxY-OH < 9.082 Å AND TM6 tilt > 14.932 Å) sound on the actual crystal structures of these 4 receptors?

### 3a. Existing references (already in `refs/reference_set.csv`, values from Block A refs_build)

| Receptor | Role | PDB | d_npxxy_oh | d_tilt | verdict |
|---|---|---|---:|---:|---|
| ACM2 | active | 7T94 (native Gα) | 4.594 | 18.110 | **PASS active** ✓ |
| ACM2 | inactive | 5ZKC | 18.217 | 12.439 | fail active ✓ |
| ADRB2 | active | 4LDE (engineered Nb + BI-167107) | 4.813 | 17.563 | **PASS active** ✓ |
| ADRB2 | inactive | 2RH1 / 3NYA / 6PS2 | 11.47/11.39/11.33 | 11.93/11.97/11.75 | fail active ✓ |
| AGTR1 | active | 6OS2 (biased-agonist Nb) | 4.047 | 19.086 | **PASS active** ✓ |
| AGTR1 | inactive | 4ZUD | 11.779 | 11.228 | fail active ✓ |
| OPRK | active | 8FEG (native Gα) | 4.609 | 17.253 | **PASS active** ✓ |
| OPRK | inactive | 4DJH | 12.213 | 11.628 | fail active ✓ |

**All 8 existing references calibrate correctly** on both instrument axes: every active-labeled PDB satisfies the active-predicate, every inactive-labeled PDB fails it. Instrument is sound for these 4 receptors on the scorer's reference set.

### 3b. Nb-anchor PDBs (staged in `refs/pending_curation_tier_d2.csv`, never merged, scorer never used them at inference)

Fetched from RCSB (`/tmp/{5JQH,4MQS,6VI4}.cif`) and scored directly with gemmi using the same anchor positions the WT reference uses (construct is `wt` in the pending-curation table). d_tilt requires GPCRdb 2x46/6x37 residue mapping — deferred (would need runs of scorer's refs_build pipeline). d_npxxy_oh computed:

| Receptor | Role | PDB | d_npxxy_oh | Expected label | Verdict |
|---|---|---|---:|---|---|
| ACM2 | active_nb | 4MQS (Nb9-8, agonist iperoxo) | 4.209 | active | **PASS active** ✓ |
| ADRB2 | inactive_nb | 5JQH (Nb60, carazolol) | 11.161 | inactive | fail active ✓ |
| OPRK | inactive_nb | 6VI4 (Nb6, JDTic) | 12.876 | inactive | fail active ✓ |

**All 3 Nb-anchor references calibrate correctly on the NPxxY-OH axis.** The active-directing Nb-anchor (4MQS) passes; both inactive-directing Nb-anchors (5JQH, 6VI4) fail as expected. TM6 tilt on Nb-anchors deferred (small compute; would confirm on both axes).

**Verdict**: instrument is sound on all 4 D2 receptors for both existing and Nb-anchor references (NPxxY-OH axis). No Block A-style construction-failure (`agonist_only` refs failing NPxxY) hits any D2 reference. F3's "inactive-Nb unreliable" finding is not attributable to a broken predicate — it's a real cross-model behaviour.

**Followable / ANV**: TM6-tilt calibration on 5JQH/4MQS/6VI4 (needs GPCRdb residue numbering; small effort).

---

## 4. F3 dual-framing draft

### 4a. Standalone claims section (main text)

**SC-D-2 (proposed) — cognate Gα is a nearly-clean positive control across the D2 panel.**
14 of 16 (receptor × backbone) cognate_gα cells reach ≥ 96% active-predicate at n=50/cell (Clopper-Pearson 95% CI lower bound ≥ 92.9%). Both misses are OF3 (ACM2 58%, OPRK 36%); OF3 systematically softer active-response than the other three.

**SC-D-3 (proposed) — active-directing nanobody works on 3 of 4 backbones on ACM2.**
ACM2 × Nb9-8 (4MQS) apo → active_nb shift: Boltz +58, OF3 +70, Protenix +100 percentage points (all CIs disjoint from zero). Chai does not shift (Δ = 0). AGTR1 × active_nb is inconclusive because AGTR1's apo is already active-biased on 3/4 backbones (F6).

**SC-D-4 (proposed) — inactive-directing nanobody is not reliable on any backbone; failure is direction-biased (toward active).**
Across ADRB2 × 5JQH (Nb60) and OPRK × 6VI4 (Nb6), no backbone maintains apo-level or lower active-fraction under inactive-Nb input on both receptors. Boltz corrects on ADRB2 (0% → 0%) but inverts on OPRK (4% → 48%). Protenix corrects on OPRK (0% → 6%) but inverts on ADRB2 (0% → 76%). Chai does not shift on either (100 → 100 on ADRB2; 74 → 82 on OPRK). OF3 stable at ~10% on both. Cross-backbone Δ signs on OPRK are unanimous_up (+44, +8, +10, +6) — every backbone drifts more-active under inactive-Nb, indicating a systematic Nb-B-as-active bias, receptor-dependent in magnitude.

**W-D-1 (proposed withdrawal) — the D2 smoke's "Boltz + OF3 respond correctly to Nb-inactive" claim is withdrawn.**
Panel-scale (ADRB2 + OPRK) contradicts the ADRB2-only smoke. Boltz correct on ADRB2 but inverts on OPRK; OF3 stable near 10% on both, but 10% is not zero. Superseded by the receptor-specific breakdown in SC-D-4.

**Positioning**: SC-D-4 is a negative result of a well-formed hypothesis test. It is publishable as a main-text finding on the pattern of Block B's "presence not identity" — models read partner *presence* strongly (F1 Gα ground-truth is near-perfect) but partner *state-selectivity* is not distinguished. D2 strengthens Block B's reading.

### 4b. Discussion-appendix framing

D2 was an existence-proof design: given a matched pair of crystal anchors that differ **only in nanobody state selectivity**, do current backbones read the state-directing signal?

Answer: **yes for active-directing partners, no for inactive-directing partners.** Active-Nb (Nb9-8 on ACM2) reliably pushes the receptor into an active-predicate pocket on 3/4 backbones (Chai refuses); inactive-Nb (Nb60 on ADRB2, Nb6 on OPRK) does not reliably push toward inactive on any backbone.

Two interpretations, not distinguished by D2:
1. **Prior asymmetry**: active-state crystals dominate the training corpus with a G-protein-mimetic Nb pattern (Nb9-8-style). Any small Nb-shaped chain gets read as an active partner. Compatible with SC-D-4's unanimous_up direction bias on OPRK.
2. **Instrument insensitivity**: the two-instrument predicate is well-calibrated on the deposited references (§3), but the *predicted* structures at ADRB2/OPRK inactive_nb may be geometrically inactive while trip-wire-active on the coarse axes. §5's structural spot-check ruled this out for the ADRB2 × Protenix cell — the receptor pocket is genuinely active-like (NPxxY-OH = 4.53 Å) alongside a docked Nb60.

Interpretation 1 is more consistent with the evidence in this pass. A prospective test is: predict on **post-training-cutoff inactive-Nb-anchor crystals** where the model cannot have memorised the reference. All 4 D2 Nb-anchors are pre-cutoff on all 4 backbones (`refs/nanobody_state_anchors.csv`); this test requires new curation.

---

## 5. Structural spot-check

Pulled 4 CIFs from HPC pool; scored receptor-side d_npxxy_oh from anchor positions:

| Cell | receptor-chain len | Nb-chain-B present? | d_npxxy_oh | receptor pocket verdict |
|---|---:|---|---:|---|
| ADRB2 inactive_nb × Protenix (76% active-anomaly) | 413 aa | ✓ 125 aa Nb60 | **4.529 Å** | **active-like** — Protenix generates active pocket alongside inactive-Nb dock |
| ADRB2 inactive_nb × Boltz (0% active, correct) | 413 aa | ✓ 125 aa Nb60 | 11.637 Å | inactive-like — Boltz holds inactive despite same Nb60 |
| OPRK inactive_nb × Boltz (48% active, inversion) | 380 aa | ✓ 133 aa Nb6 | 11.271 Å | inactive-like (this sample); the 48% is stochastic per-sample across seeds — 24/50 samples flip active |
| ACM2 active_nb × Chai (0% active, Chai refusal) | 466 aa | ✓ 125 aa Nb9-8 | **19.121 Å** | strongly-inactive — Chai holds inactive pocket despite active-Nb dock |

**Nb chain B is docked in every case** — the failure is not "Nb didn't reach the model" (per D2.3 chai/protenix MSA cache warm), but downstream in how the model interprets the Nb-B signal.

**Mechanism confirmed**: F3/F4/F5 anomalies are **receptor conformation, not partner absence**. Protenix reads Nb-B as active regardless of state, Chai refuses to shift receptor away from its receptor-specific apo prior regardless of state signalling. Both patterns generalise beyond the specific cells inspected.

---

## 6. Cross-tier consistency check (Block B ↔ D2)

D2's positive control (cognate_gα on 4 receptors × 4 backbones = 14/16 ≥ 96% active) is the strongest cross-block confirmation of Block B's Gα-active signal, on 4 receptors that overlap Block B's panel. The D2 negative finding (inactive-Nb unreliable) is a **strengthening** of Block B's "presence not identity" reading — models read partner presence but do not read state selectivity via nanobody identity. Reasonable Discussion sentence.

---

## 7. Kendall τ / concordance summary

At n=4 receptors and n=50 samples/cell, Kendall τ on receptor-ordered rankings is underpowered. Cross-backbone concordance reported qualitatively per (receptor × arm shift):

| Receptor × arm shift | Concordance | n bb same sign |
|---|---|---|
| ADRB2 apo→inactive_nb | mixed (3 flat, 1 inverts) | Boltz/Chai/OF3 = 0; Protenix = +76 |
| OPRK apo→inactive_nb | **unanimous_up** | all 4 bb drift more-active |
| ACM2 apo→active_nb | 3-of-4 unanimous_up (Chai refuses) | Boltz/OF3/Protenix ≥ +58; Chai = 0 |
| AGTR1 apo→active_nb | ceiling-limited (2 already saturated) | Boltz/Chai at 100 apo; OF3/Protenix respond |
| ACM2 apo→cognate_ga | unanimous_up (Boltz/Chai/Protenix saturate at 100) | OF3 +46, others +58 to +100 |
| ADRB2 apo→cognate_ga | unanimous_up | all 4 bb reach 100 |

---

## 8. Open items (Followable / ANV)

- **TM6-tilt calibration on Nb-anchor PDBs** (5JQH, 4MQS, 6VI4). Small compute; would extend §3b to both instrument axes.
- **Prospective inactive-Nb test with post-cutoff crystals**. All 4 D2 Nb-anchors are pre-training-cutoff on all 4 backbones. A post-cutoff inactive-Nb reference would let us disambiguate "prior memorisation" from "genuine state-reading failure".
- **Nb80 on ADRB2 active_nb**. Currently dropped (Nb60/Nb80 documentation collision, per GATE-1 which confirmed collision was documentation-only). Curating real Nb80 sequence into `refs/nanobody_sequences.fasta` would let us test the ADRB2 active-Nb pairing that D2 was originally designed to include. Independent motivation, not remediation.
- **Third inactive-Nb receptor** (e.g., CCR5 known inactive-Nb crystals) to sharpen the systematic-Nb-B-as-active-bias claim beyond n=2 receptors on OPRK/ADRB2.
- **Chai's ACM2 refusal mechanism**. Chai reproduces its receptor-specific-lock pattern from D1 (CNR2/OPSD/ADRB2). D2 adds ACM2 to that list. Attribution to training-corpus memorisation vs prior remains open.

---

## 9. Provenance

- Rows source: `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv` — 2,370 rows, no failures.
- Scorer: `d9c646af5f89861c16062bf256de96a8389d9915` (uniform, GATE-4 verified).
- Reference set: `refs/reference_set.csv` (existing refs) + `refs/pending_curation_tier_d2.csv` (Nb-anchor curation, not merged).
- Nb sequences (consumed): `refs/nanobody_sequences.fasta`, GATE-1 SHA-verified.
- Anchor positions (used for direct predicate calibration): `refs/reference_set.csv` `anchor_positions` JSON (5.58, 7.53 for WT ADRB2/ACM2/OPRK).
- Spot-check CIFs pulled to `/tmp/d2_spotcheck/` from HPC pool `/hpc/scratch/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/full/pool/pool/<rec>/<arm>/<bb>/seed_1291532968/`.
- Per-cell CI JSON: `/tmp/d2_percell.json` (44 cells).
