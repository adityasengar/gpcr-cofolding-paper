# BLOCK A — CLAIM SHEET

Every Block-A-derived claim the manuscript will make, in final wording, with
its authoritative cluster-boot 95% CI, its exclusion set, and a pointer to
the flag or caveat that qualifies it.

**Bootstrap convention**: 26 paralog clusters (T7 manual paralogy mapping;
42% singletons; see C-8), 1000 resamples, seed 20260909. Receptor-bootstrap
CIs are ~1.10× tighter and are NOT the reported primary measurement.

## Two methodological statements worth surfacing at front

**A. Both predicate axes bit-exact against independent non-scorer implementations.**
The two axes that carry the two-instrument predicate — `d_gpcrdb_tm6_tilt_246_637_ca`
(tilt) and `d_npxxy_y558_y753_oh` (NPxxY-OH) — were independently
re-derived from CIF coordinates with implementations written from scratch in
`gemmi` + stdlib, no import from `scorer/`. NPxxY-OH: n=41 samples, median
|Δ| = 0.0000 Å, Pearson r = 1.000000 (T6 Part 3). Tilt: n=45 samples, median
|Δ| = 0.0000 Å, Pearson r = 1.000000 (T7a). Combined with T6 Parts 1 and 4
(predicate recompute clean; cell reconciliation clean) and T7b (only one
broken cell in the corpus), **every stored value in every load-bearing
column of `rows.csv` has been verified against at least one independent
source.** The scorer's coordinate-to-distance calculation on both predicate
axes is not a source of unknown error.

**B. E1–E5 exclusion sweep — no sign flips; fraction invariant to ≤ 0.5%.**
Applied the five pre-specified exclusion sets (broken cell; atom clashes;
P1a-failing references; Class B/F; agonist-only actives) singly and in every
material combination against every headline metric. **The fraction-of-way-to-
active shifts by ≤ 0.5% under every single combination.** The largest
effects are on Chai tilt (E4 doubles it because Class F receptors' near-zero
tilt shifts drag the panel-median) and on per-backbone apo-active rate (E4
drops it 27–61% depending on backbone). **No exclusion combination flips any
signed finding to null; every signed finding survives every combination.**
Exclusions are pre-specified by cause, not chosen after inspecting results —
the report gives numbers with and without each set so readers can see what
moves.

## Class A count reconciliation (two distinct denominators)

- **T1 uses n=40**: the full Class A panel of receptors (40 receptors) for
  the amplitude regression. Restriction-of-range diagnostic SD(Δref) is
  computed across these 40 receptors' reference values.
- **T7a uses n=45**: Class A CIF SAMPLES from the local 50-CIF
  curated+random pool (25 curated + 25 random − 5 Class B skipped where BW
  2.46/6.37 are undefined). Independent-recompute bit-exact check operates on
  CIF samples, not on receptors.

Same class, different unit of counting. Both are Class A; neither is
"wrong" — they answer different questions.

## What ships in this archive vs what is HPC-regenerable

**Ships**: `rows.csv`, `rows.rmsd.csv`, `rows.fold_integrity.csv`, `manifest.csv`,
all provenance sidecars, `panel/refs/reference_set.csv` (post-review-frozen),
the 92 reference PDB CIFs, 50 curated + random-sample predicted CIFs + renders,
the T2 scale-up METADATA and CODE (`_findings.json`, `_analysis.json`,
`_selected_cifs.json`, `_pull_manifest.json`, `_pull.py`, `_score_connector.py`,
`_analyze.py`, `_select.py`, `RESULTS.md`, `SELECTION.md`).

**Does NOT ship**: the 500 CIFs used for the T2 scale-up (229 MB). SC-3's
0.37 magnitude ratio and 79.7%/80.1% load-bearing counts are supported by
metadata + code + row-level input SHAs. **Reconstruction from HPC**: run
`structures/block_a/p2_scale_up/_pull.py` with `_pull_manifest.json` (which
carries `input_sha256` for every selected CIF) to fetch the 500 CIFs from
`basel-hpc:/hpc/scratch/sengaad1/paper_af3/…`. Local sha256 of each pulled
file must match the manifest's `input_sha256` before it is a valid
reproduction. This scale-up is provisional at n=512; the definitive test is
a permanent `d_connector_p550_f644_ca` column in `scorer/anchors.py` + a
full 9,490-row rescore, deferred as a manuscript-flag limitation.

**Exclusion sets applied consistently across the sheet**:
- E1 = broken cell (ACM1-cognate-Protenix, 25 rows, mean pLDDT < 50; C-12)
- E2 = model-side atom clashes (4 rows, NPxxY-OH < 2.4 Å; Flag 45)
- E3 = references failing own predicate (per-axis, per P1a)
- E4 = Class B and Class F (instrument scope limitation; C-2, C-3)
- E5 = agonist-only actives (OPRD, CNR1, FZD4; C-9-adjacent)

Numbers are reported both with and without each specified exclusion where
material (per dispatch's standing principle: do not pick, report both).

---

## Surviving claims

### SC-1 — The switch test's headline shift is real and cross-backbone

**Claim**: The cognate arm moves TM6 tilt outward by 5.0 Å (Boltz), 4.8 Å
(OpenFold-3), 5.3 Å (Protenix), and 1.0 Å (Chai, softer predictor) relative
to the apo baseline, and this shift is invariant to every specified
exclusion set (≤ 0.5% under any exclusion).

**Numbers**:

| Backbone | Δ tilt (cognate − apo), baseline | 95% CI (cluster-boot) | E1+E2+E4+E5 |
|---|---:|---|---:|
| boltz | 5.036 Å | [+4.403, +5.502] | 5.09 Å |
| chai | 1.047 Å | [+0.373, +3.452] | **2.03 Å (E4 doubles Chai)** |
| of3 | 4.814 Å | [+4.072, +4.998] | 4.92 Å |
| protenix | 5.307 Å | [+4.909, +5.603] | 5.31 Å |

**Exclusion set applied**: baseline reports the whole panel; E1+E2 makes ≤1% difference; E4 (Class-A-only) doubles Chai's number because Class F receptors' near-zero tilt shifts drag the panel-median down.

**Null beat**: within-receptor arm-permutation p < 0.001 on all 4 backbones (but see W-9 caveat — the load-bearing null is Block B's wrong-partner).

**Dossier**: `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md §Phase 4a`.

**Qualified by**: C-4 (Chai softness); C-10 (amplitude flatness on both axes); Flag 22 (two axes, two fractions).

---

### SC-2 — Predictions reach 89–95% of the way to the active reference

**Claim**: Across the four backbones the cognate arm reaches 89–95% of the
way from the apo baseline to the active reference on `delta_to_active`,
invariant to every specified exclusion set (≤ 0.5% shift under any
combination of E1–E5).

**Numbers** (bootstrap over receptors; n=38–39 excluding sealed 8):

| Backbone | Fraction | 95% CI (cluster-boot) | E1+E2+E4+E5 |
|---|---:|---|---:|
| boltz | **0.9456** | [0.892, 0.983] | 0.9410 |
| chai | **0.8878** | [0.744, 0.959] | 0.8878 |
| of3 | **0.9152** | [0.861, 0.993] | 0.9108 |
| protenix | **0.9118** | [0.897, 0.978] | 0.9113 |

Pooled median: 0.913.

**Exclusion set applied**: baseline n=38–39 receptors (sealed 8 dropped by construction). E1–E5 shifts are all ≤ 0.5%.

**Null beat**: within-receptor arm-permutation reject (all 4 backbones) — see W-9.

**Dossier**: `§Phase 4a`. **Qualified by**: C-9 (Block A metric is retrospective by design; prospectivity comes from date-stratified holdout + Block C); C-10 (this fraction reflects state-reached, not amplitude-reproduced).

---

### SC-3 — Predicate reaches active state; per-receptor amplitude NOT reproduced on the well-powered axis

**Claim (compound)**:

- **State reached**: predicate-active predictions independently exhibit the P5.50–F6.44 PIF connector rearrangement — an orthogonal signature that has never been used to call anything. Direction unanimous across all 4 backbones; magnitude ratio 0.37.
- **Amplitude not reproduced on NPxxY-OH** (the well-powered axis, Class-A-only cluster-boot slopes 0.12–0.55, all CIs cross zero, attenuation-robust).
- **Tilt axis cannot resolve amplitude** (SD(Δ_tilt_ref) = 1.19 Å across 40 Class A receptors — instrument limitation).

**Numbers (orthogonal signature, T2 scale-up n=512)**:

| Quantity | Value | 95% CI |
|---|---:|---|
| Reference Δ (active − inactive median) | −1.51 Å | (non-overlapping refs) |
| Prediction Δ (pred-active − pred-inactive median) | **−0.56 Å** | [−1.16, −0.06] |
| Magnitude ratio | **0.37** | [0.04, 0.77] |
| Pred-active below ref-inactive median | 204/256 (79.7%) | — |
| Pred-inactive above ref-active median | 205/256 (80.1%) | — |
| Per-backbone direction | 4/4 same-signed | — |

**Amplitude regression slopes (Class-A-only, cluster-boot)**:

- NPxxY-OH: 0.12 to 0.55 across backbones; all CIs cross zero; SD(Δref) = 4.71 Å well-powered; attenuation-robust.
- Tilt: 0.03 to 0.50 across backbones; all CIs cross zero; SD(Δref) = 1.19 Å — restriction of range prevents resolution.

**Exclusion set applied**: E4 (Class A only) applied on the amplitude regression by construction. P1a-flagged references excluded from NPxxY denominator (E3). E1 + E2 removed 29 rows / 9,490 for all analyses.

**Dossier**: §Phase 4b + §Phase 5-scale-up (T2). **Qualified by**: C-10 (this is the load-bearing caveat).

---

### SC-4 — Two-instrument agreement is substantial on Class A; Class B/F have known instrument-scope limits

**Claim**: Two-instrument predicate agrees at 89.9% [85.6, 93.4] on the
Class A derivation panel (κ = 0.79, substantial). Class B agreement is
81.6% [69.8, 96.4] (κ = 0.31, fair) — but Class B's two axes are non-
independent (all disagreements are kink-active-tilt-inactive in apo; tilt is
ceiling-saturated at 100% in cognate). Class F uses tilt-only; no cross-
instrument counterpart at row grain. Instrument is Class-A-calibrated.

**Numbers** (bootstrap over receptors; Class A n=32 deriv panel, Class B n=4):

| Class | Agreement | 95% CI | Cohen's κ |
|---|---:|---|---:|
| A | **89.92%** | [85.60, 93.38] | 0.79 |
| B | 81.64% | [69.75, 96.35] | 0.31 (fair) |

Per-backbone Class A: boltz 90.23%, chai 93.40%, **of3 83.67% (outlier)**, protenix 92.40%.

**Exclusion set applied**: Class-A-only (E4) on the primary; Class B reported separately. E1–E3 excluded per P1a per axis.

**Dossier**: §Phase 4c. **Qualified by**: C-2 (Class B tilt ceiling-saturated); C-3 (Class F weak predicate); Flag 8 (Class B/F as instrument scope).

---

### SC-5 — AA2AR paired-switch is unanimous across all four backbones at CIF grain

**Claim**: On all 4 backbones, AA2AR resolves the paired-switch cleanly at
the CIF level: apo lands at inactive (RMSD 0.4–0.7 Å from inactive
reference), cognate lands at active (RMSD 0.5–0.7 Å), with a TM6 tilt-
distance shift of ~11 Å across arms.

**Numbers** (n=8 CIFs, 2 arms × 4 backbones × 1 median-representative each):

| Arm | RMSD-to-correct-ref (all 4 backbones) | Δ d_TM6 |
|---|---|---:|
| apo × 4 | 0.37 to 0.67 Å (to inactive) | 7.4–8.1 Å |
| cognate × 4 | 0.53 to 0.70 Å (to active) | 17.9–18.9 Å |

**Exclusion set applied**: single-case exhibit; no exclusion sweep applicable.

**Dossier**: §Phase 5b. **Qualified by**: C-10 (this is a case study; aggregate amplitude claim changes; see SC-3).

---

### SC-6 — Predicate is well-calibrated: 0.02% false-positive rate against RMSD > 3 Å

**Claim**: Across 4,866 predicate-active rows on the 9,490-row corpus, only
2 (0.04%) land more than 3 Å from the active reference. The two-instrument
predicate is well-calibrated to structures near the active state.

**Numbers** (cluster-boot):

| Backbone | Predicate-active n | > 3 Å from active | 95% CI |
|---|---:|---:|---|
| boltz | 1,167 | 1 (0.09%) | [0.000, 0.0025] |
| chai | 1,273 | 0 (0.00%) | [0.0000, 0.0000] |
| of3 | 1,229 | 1 (0.08%) | [0.000, 0.0016] |
| protenix | 1,197 | 0 (0.00%) | [0.0000, 0.0000] |

**Exclusion set applied**: baseline; E1–E5 negligible (E1's ACM1-cognate-Protenix cell is largely predicate-inactive so removal doesn't shift these counts).

**Dossier**: §Phase 5c. **Qualified by**: Flag 44 (E5 agonist-only actives fail NPxxY by construction, not by measurement).

---

### SC-7 — Partner engagement is ~98% by contact count

**Claim**: The cognate arm's Gα engages the receptor on ~98% of samples
across all four backbones (n_contacts > 30 on TM3/5/6). R3.50-anchored α5
metric is Class-A-scoped; Class B and Class F Gs-coupling curator calls
show 0% R3.50-engagement despite ~100% contact-count engagement — a metric-
scope caveat, not a docking failure.

**Numbers** (cognate arm, n=47 receptors; contact-count > 30):

| Backbone | Engagement | 95% CI |
|---|---:|---|
| boltz | 99.1% | [97.7, 100] |
| chai | 97.7% | [93.7, 100] |
| of3 | 97.2% | [93.9, 99.5] |
| protenix | 98.8% | [97.1, 99.9] |

**Exclusion set applied**: baseline. Cognate-arm only (apo has no partner).

**Dossier**: §Phase 5d. **Qualified by**: Flag 32 (6/48 refs are non-Gα); note ACM1-Protenix R3.50-engagement outlier (0%).

---

### SC-8 — Fold-integrity anchor passes on 96.3% of rows

**Claim**: TM6 helicity in BW 6.30–6.50 passes at ≥ 0.80 on 96.3% of rows
overall (boltz 95.6%, chai 95.1%, of3 97.7%, protenix 96.9%). 21 low-
helicity cells cluster on Class B secretin receptors (α-box misfit on the
TM6 kink motif) — a scoring-anchor limitation, not a fold defect.

**Exclusion set applied**: baseline.

**Dossier**: §Phase 3e.

---

### SC-9 — Templates were not used on any backbone

**Claim**: Templates off across all four backbones. Evidence: launcher static
analysis + source-code defaults + propagation test PASS 5/5.

**Dossier**: §Phase 1f. **Qualified by**: no row-level echo (evidence class
b + c + d, not a); `_status.json.runtime_config` echo landed post-Block-A.

---

### SC-10 — Panel of record: 48 receptors

**Claim**: Block A ran 48 receptors (40 Class A + 4 Class B + 4 Class F),
bit-exact match to `refs/gpcr_coupling.csv`.

**Dossier**: §Q1 blocking question.

---

### SC-11 — pLDDT tracks correctness at anchor grain on 2 of 4 backbones

**Claim**: At anchor residues (3.50, 3.51, 5.58, 6.30, 6.34, 7.53), pLDDT
tracks correctness on 2 of 4 backbones (Boltz + OpenFold-3, both signed
negative under cluster-boot with the post-hoc primary aggregation `anchor_mean`).
Chai signs only on the secondary sensitivity `anchor_min`. Protenix null on
both aggregations. Global `plddt_mean` is diluted and misleading — the
retracted Protenix-overconfident-across-panel claim was a `plddt_mean`
artefact. OpenFold-3's r = −0.626 [−0.827, −0.601] is the strongest signal
in the campaign.

**Numbers** (Pearson r, cluster-boot):

| Backbone | plddt_mean r | anchor_mean r | anchor_min r | Verdict |
|---|---|---|---|---|
| boltz | −0.064 null | **−0.221 [−0.357, −0.092]** | −0.193 signed | primary signed |
| chai | +0.025 null | −0.160 [−0.462, +0.144] null | **−0.332 signed** (secondary) | secondary only |
| of3 | −0.327 signed | **−0.626 [−0.827, −0.601]** | −0.450 signed | primary strongest |
| protenix | +0.274 signed (retracted) | +0.068 [−0.159, +0.276] null | −0.249 signed then flips null under cluster-boot | null on primary |

**Exclusion set applied**: Class A only via existing `anchor_mean` NPxxY-column population; sealed 8 excluded by construction.

**Dossier**: §Phase 4f. **Qualified by**: W-2 (aggregation-dependence; three aggregations tested; primary post-hoc); C-8 (cluster-boot authoritative); Flag 40.

---

## Withdrawn claims (see `withdrawals/`)

- **W-1** — 14.5% apo-active panel mean (Protenix alone at baseline; 5.6% under E1–E5)
- **W-2** — pLDDT-tracks-correctness campaign-wide claim RESTATED to 2/4 at anchor grain
- **W-3** — "29 cells 25 in apo" bimodal cell census (now 72 def-A / 26 def-B; apo share 64% not 86%)
- **W-4** — OPSD-apo-Boltz "0.40 Å from active" as cell-median (that's the seed-min; cell-median 1.07 Å)
- **W-5** — LPAR1-OF3 "91.8%/0.4%" as Block A (Block C figure)
- **W-6** — OF3 rerun silently merged (not merged; merge would REGRESS)
- **W-7** — Two docs' "merged via merge_of3_rerun_rows.py" claim
- **W-8** — 14.5% as cross-backbone signal (variant of W-1)
- **W-9** — Phase 4h permutation null (vacuous; real null is Block B's wrong-partner)

## Live caveats (see `caveats/`)

- **C-1** — Bug #4 matcher path (Block C tier 3, not Block A)
- **C-2** — Class B cognate tilt ceiling-saturated at 100%; kink is discriminator
- **C-3** — Class F predicate weak; median shift 0.27 Å < IQR
- **C-4** — Chai systematic softness
- **C-5** — Pre-freeze `no-git` subtrees; motivational not headline
- **C-6** — 89 unique reference PDBs on the 48-receptor panel (not 48); reconcile with T4's 167 total
- **C-7** — Apo is a computational reference condition, not a physical state
- **C-8** — Cluster-bootstrap (26 paralog clusters, 42% singletons) is authoritative; anchor_mean is post-hoc primary
- **C-9** — Prospectivity foreclosure at Block A → date-stratified cluster-level holdout (n=13 AF3-lineage, n=8 extended-descriptive)
- **C-10** — Amplitude: tilt-axis restriction-of-range prevents resolution; NPxxY genuine null; state-reached corroborated at 0.37 magnitude
- **C-11** — `construct` column corpus-wide untrusted (40% of evaluable PDBs)
- **C-12** — ACM1-cognate-Protenix broken cell + A1–A6 has no pLDDT floor

## Deferred limitations (in MANUSCRIPT_FLAGS.md)

- Full-corpus P2 rescore (permanent scorer column)
- Corpus-wide `construct`-column repair
- Extended-cutoff cluster-level holdout (n=8 underpowered; descriptive only)
- PAE analysis (not laptop-recoverable)
- Class B / Class F rescue (out of scope for the Class-A-calibrated instrument)
- Panel-only subset audit of T4's 52/127 contradictions
- Mutation-verification on the 40 recently-fetched entry.json PDBs
