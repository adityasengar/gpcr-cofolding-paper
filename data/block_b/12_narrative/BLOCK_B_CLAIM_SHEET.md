# BLOCK B — CLAIM SHEET

Every Block-B-derived claim the manuscript will make, in final wording, with
its authoritative cluster-boot 95% CI, its exclusion set, and a pointer to
the flag or caveat that qualifies it.

**Bootstrap convention**: 26 paralog clusters (reconstructed 2026-09-09;
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`;
see C-B-13), 1000 resamples, seed `20260909`. Receptor-bootstrap CIs
(40 receptors treated independent) are tighter and are NOT the reported
primary measurement.

**Corpus**: 40 Class A receptors × 4 backbones × 4 arms {apo, decoy,
shuffled, cognate} × 5 seeds × 10 samples = 32,000 rows. Phase 2 grid-complete
census: zero cells non-conforming (see SC-B-10). Class B/F not in Block B
(see C-B-15).

**Predicate of record (Class A)**: `d_npxxy_y558_y753_oh < 9.082 Å AND
d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`. NaN on either axis → False.
Two published frames:

- **frame_36** — n=36 receptors after excluding EDNRA / EDNRB / GRPR / HRH3
  (all-NaN NPxxY-OH by 7.53 = L not Y). Every published two-instrument
  Block B number uses frame_36.
- **frame_40** — n=40, the naïve denominator. Only used when explicitly
  named. Frame convention **must** be stated in every headline table
  (see Flag B-7, C-B-5).

**Reference set of record**: `refs/reference_set.blockb_pinned.csv`
(SHA-256 `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`),
recovered from git commit `a355977` and durably archived at commit `8e5ea48`.
Every row of Block B rows.csv carries this SHA in `ref_set_csv_sha256`.
On-disk `refs/reference_set.csv` at HEAD is a superset (annotation-only
delta plus 6 inactive rows added post-run for 3 Block B receptors — none of
those receptors' primary inactive references shift; see C-B-9).

**Exclusion sets applied consistently across this sheet**:

- **E-B-1** = four receptors with all-NaN NPxxY under the current axis
  definition (EDNRA, EDNRB, GRPR, HRH3). Frame-36 = whole panel − E-B-1.
- **E-B-2** = AA2AR (recurrently anomalous; excluded from pooled inference
  where noted). See C-B-8.
- **E-B-3** = non-native-anchored active references (15 of 40 receptors:
  chimera + mini-G + nanobody + scFv + agonist-only + DVL-DEP;
  `active_stabilization_source ≠ native`). Applied where Phase 5's
  reference-bias caveat is load-bearing (see C-B-10).
- **E-B-4** = ceiling-pinned cells (cognate rate ≥ 0.98). Reported on the
  logit scale to bypass this compression (see C-B-7).

Numbers are reported both with and without each specified exclusion where
material.

---

## Surviving claims

### SC-B-1 — The four-arm ladder is monotonic and reproduces exactly under the two-instrument predicate

**Claim**: Across 40 Class A receptors × 4 backbones × 4 arms × 5 seeds × 10
samples (32,000 predictions), the two-instrument active-call fraction rises
monotonically apo < decoy < shuffled < cognate at the panel level. Every
receptor × backbone × arm cell delivers exactly 50 rows.

**Numbers** (frame_36, two-instrument predicate, panel-level, cluster-boot
95% CI over 26 paralog clusters):

| Arm | binary predicate | 95% CI | Δ_to_active median (Å) | logit |
|---|---:|---|---:|---:|
| apo | **0.158** | [0.081, 0.256] | −5.93 | −1.67 |
| decoy | **0.558** | [0.445, 0.664] | −1.35 | +0.23 |
| shuffled | **0.809** | [0.747, 0.869] | +0.04 | +1.45 |
| cognate | **0.891** | [0.838, 0.942] | −0.35 | +2.10 |

**Exclusion set applied**: frame_36 = whole panel − E-B-1 (four all-NaN-NPxxY
receptors).

**Continuous axes** also monotonic apo → decoy → shuffled → cognate at panel
level: `d_npxxy_y558_y753_oh` medians 11.30 / 8.19 / 7.31 / 6.60 Å;
`d_gpcrdb_tm6_tilt_246_637_ca` medians 13.05 / 15.61 / 16.42 / 16.75 Å.

**Dossier**: `dossiers/BLOCK_B/EXPERIMENT_DOSSIER_BLOCK_B.md §Phase 3d, §Phase 3a`.
**Source CSV**: `experiments/019_block_b_partner_selection/analysis/ladder_four_scorings.csv`.

**Qualified by**: C-B-5 (frame convention), C-B-7 (ceiling-pinning),
C-B-13 (cluster map), C-B-15 (Class A only), Flag B-7, Flag B-14.

---

### SC-B-2 — Ladder decomposition: occupancy 55% / α5-CT sequence 34% / correct family 11–17% (scale-dependent)

**Claim (compound)**: The apo → cognate ladder decomposes into three
telescoping terms whose share depends on the reporting scale.

**Numbers** (frame_36, panel-level, cluster-boot over 26 paralog clusters):

| contrast | probability estimate | prob share | prob 95% CI | logit estimate | logit share | logit 95% CI |
|---|---:|---:|---|---:|---:|---|
| Δ_occupancy (apo→decoy) | +0.400 | **54.6%** | [0.328, 0.464] | +1.907 | **50.5%** | [1.52, 2.40] |
| Δ_α5CT_seq (decoy→shuffled) | +0.252 | **34.3%** | [0.188, 0.321] | +1.214 | **32.1%** | [0.97, 1.49] |
| Δ_correct_family (shuffled→cognate) | +0.082 | **11.1%** | [0.047, 0.125] | +0.656 | **17.4%** | [0.39, 1.09] |
| total (apo→cognate) | +0.733 | 100% | | +3.776 | 100% | |

**Per-backbone logit family share** (all four backbones agree, 17–21%):
boltz 17.4%, chai 17.5%, of3 20.9%, protenix 17.5%.

**Per-backbone probability family term**: boltz 0.066, chai 0.089, of3
0.148, protenix 0.024. Protenix's probability CI [-0.021, +0.061] crosses
zero — a ceiling artefact (cognate = 0.974, shuffled = 0.950). Logit
CI [0.35, 1.05] squarely positive.

**Exclusion set applied**: frame_36. E-B-4 (ceiling-pinning) is why the
probability-scale family term is smaller than the logit-scale family term.

**Dossier**: `§Phase 3e`. **Source CSV**:
`experiments/019_block_b_partner_selection/analysis/ladder_decomposition.csv`
+ `ladder_decomposition_bootstrap_draws.csv`.

**Qualified by**: C-B-7 (ceiling-pinning drives the scale gap), Flag B-1
(both scales must appear in the paper), W-B-1 (bare "~11%" figure is
retired).

---

### SC-B-3 — Panel-wide 2×2 engagement × activation reproduces the published triples

**Claim**: At the 20 Å tip-to-R3.50 engagement cutoff on frame_36, all
three published (arm × p_engaged × p_active|engaged) triples reproduce
inside cluster-boot 95% CIs and inside a ±0.012 tolerance.

**Numbers** (frame_36, two-instrument predicate, panel-level, cluster-boot
over 26 paralog clusters):

| arm | p(engaged) | 95% CI | p(active\|engaged) | 95% CI | published |
|---|---:|---|---:|---|---|
| cognate | 0.9983 | [0.995, 1.000] | 0.8926 | [0.840, 0.944] | 0.999 / 0.894 |
| shuffled | 0.9674 | [0.929, 0.996] | 0.8353 | [0.774, 0.891] | 0.966 / 0.837 |
| decoy | 0.7037 | [0.571, 0.816] | 0.6647 | [0.554, 0.754] | 0.715 / 0.665 |

**Engaged-but-inactive floor** (the mechanism-claim cell): decoy arm
n = 1,699 rows pooled (278–540 per backbone) — well above the ≥5-row
floor. 10–13 cells per backbone; paralog-cluster resample coverage
defensible.

**Sensitivity sweep** (cognate arm, frame_36, cutoff sweep): p(active|engaged)
is nearly flat 10 → 20 Å at cognate (0.897 → 0.893); on decoy the same
sweep moves p(active|engaged) from 0.53 to 0.66. The 20 Å cutoff is
permissive at cognate (4× median depth of 12.19 Å) but load-bearing at
decoy (see C-B-6).

**Exclusion set applied**: frame_36. Panel is Class A only (Class B/F not
in Block B).

**Dossier**: `§Phase 4b`. **Source CSV**: `interface_2x2.csv`.

**Qualified by**: C-B-6 (cutoff sensitivity), C-B-5 (frame), C-B-15,
Flag B-8, Flag B-13.

---

### SC-B-4 — Engaged-but-inactive decoy rows sit at apo geometry on the PIF connector

**Claim**: On the P5.50–I3.40–F6.44 Cα-Cα PIF connector (an orthogonal
axis not used to call activation), decoy-arm cells that are engaged
(tip < 20 Å) but not two-instrument-active carry PIF-sum-Cα geometry
statistically indistinguishable from apo, and clearly below cognate and
shuffled active-engaged cells.

**Numbers** (per-cell representative CIFs, 640 cells; median of cell-medians
in Å):

| subset | n cells | median | IQR |
|---|---:|---:|---|
| apo (all) | 160 | 15.35 | [14.85, 15.89] |
| cognate active_engaged | 130 | 16.04 | [15.76, 16.40] |
| shuffled active_engaged | 118 | 16.00 | [15.70, 16.38] |
| decoy active_engaged | 69 | 16.03 | [15.70, 16.56] |
| **decoy engaged-but-inactive** | **47** | **15.42** | **[14.86, 15.86]** |

**Per-backbone sign**: 3 of 4 backbones sign in the predicted direction
cleanly (boltz 15.09, chai 15.18, protenix 15.40 vs their respective
cognate active_engaged medians ~16.0); OF3 at 15.83 remains on the
inactive side of its own cognate active_engaged 15.98 by 0.15 Å (same
signed direction, smaller magnitude).

**Exclusion set applied**: baseline. Per-cell representative CIF pick =
row minimizing joint (NPxxY-OH, tilt) z-distance to cell centroid.

**Dossier**: `§Phase 4c`. **Source CSV**: `interface_pif_connector.csv`.

**Qualified by**: C-B-6 (cutoff for engagement).

---

### SC-B-5 — Fold integrity: panel-wide TM6 helicity pass rate 0.988

**Claim**: TM6 helicity across BW 6.30–6.50 passes at ≥ 0.80 on 0.988 of
Block B rows overall (arm × backbone cell floor: 0.941, Chai shuffled).
Above the Block A baseline (0.963) by 2.5 points. Every arm × backbone
cell above 0.94.

**Numbers** (per-arm × backbone pass rate; n=2,000 per cell):

| arm | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| apo | 0.979 | 0.981 | 1.000 | 1.000 |
| cognate | 0.990 | 0.975 | 0.995 | 1.000 |
| shuffled | 0.987 | 0.942 | 0.995 | 0.998 |
| decoy | 0.992 | 0.971 | 0.999 | 1.000 |

Partner-chain last-11 helicity median 0.727 (α5-CT tip helical, canonical)
across engaged cells; single outlier decoy-boltz at 0.591 correlates with
decoy-arm elevated BSA (3,211 Å² vs cognate 2,906 Å²) — a docking-mode
artefact on that cell, not corpus-wide.

**Exclusion set applied**: baseline. rows.fold_integrity.csv is joined by
`input_path` to rows.csv (see C-B-3 — the per-row provenance columns are
absent from this file; parent-SHA pin lives in the `# rules:` header).

**Dossier**: `§Phase 4e`. **Source CSV**: `interface_fold_integrity.csv`.

**Qualified by**: C-B-3 (fold_integrity provenance is header-pin, not
per-row).

---

### SC-B-6 — The model treats the α5-CT partner as bulk on the continuous cavity-geometry axes below the binary predicate — Outcome A signed and firmed by native-only power analysis

**Claim (compound)**: On the largest shuffled cell (Gs donor into
Gi-cognate receptor; 24 receptors × 4 backbones = 4,800 rows), the
tilt residual against each receptor's active reference is +0.024 Å
with cluster-boot 95% CI [-0.29, +0.30] — indistinguishable from zero.
Restricted to the 20 receptors whose active reference is native
(`active_stabilization_source = native`), the residual moves to
−0.062 Å [-0.41, +0.21]: sign flips within noise, CI still spans zero,
CI width unchanged. Outcome A survives the reference-bias caveat on
this cell.

**Post-freeze note (2026-09-10, reverted to Phase 6b wording)**: an
attempt to strengthen SC-B-6 to an equivalence-style claim
("family-specific opening ruled out above ~0.4 Å on the panel's own
reference-tilt scale") did not survive a bootstrap of the ruler side.
Bootstrapping the Gs − Gi reference-median tilt gap across Block B's
own 40 active references (percentile bootstrap, 1000 draws, receptor-boot
within family, seed 20260910) yields a CI of **[0.006, 1.025]** with
point estimate 0.579 Å. This CI does not exceed the residual CI upper
bound of +0.21, and without AA2AR (a load-bearing E-B-3 exclusion) the
Gs − Gi CI opens to **[−0.047, +1.015]** and spans zero. The ruler is
under-powered by construction (Gs group is n=5, mixing nanobody and
mini-G active-stabilisation sources rather than native transducer
complexes; Gi group is n=24 native-dominated). This is an
UNDETERMINABLE result on the equivalence question, and SC-B-6 stays
as the "Outcome A signed, CI spans zero" Phase 6b wording — a bulk-
reading claim scoped by the reference-bias caveat, not an equivalence
claim. See `docs/BLOCK_B_POSTFREEZE_CHECKS.md` Check 1 (revised) for
the ruler bootstrap and the reconciliation with Block A's
restriction-of-range statement.

**Numbers** (panel-level, cluster-boot over 26 paralog clusters):

| stratum | axis | n_receptors (all) | median (all) | 95% CI (all) | n_receptors (native) | median (native) | 95% CI (native) |
|---|---|---:|---:|---|---:|---:|---|
| Gs→Gi (load-bearing) | `residual_tilt` | 24 | +0.024 | [-0.29, +0.30] | 20 | **−0.062** | **[-0.41, +0.21]** |
| Gs→Gi | `residual_npxxy` | 23 | −0.150 | [-0.50, +0.29] | 19 | +0.109 | [-0.26, +0.47] |
| Gs→Gi | `residual_delta_to_active` | 21 | +0.054 | [-0.32, +0.50] | 17 | −0.033 | [-0.38, +0.36] |

**CI-gated verdict** (per Phase 5 §5.4, per-backbone): 0–1 cells of 9
qualifying strata × axes sign in the Outcome-B direction with CI
excluding zero; panel-level 0/9. Weak Outcome-B trend on median-sign
alone (5–7 of 9 per backbone; 6/9 at panel level) but never crossing
cluster-boot noise.

**Load-bearing exclusion**: E-B-3 (non-native active references) applied
as the native-only re-run in Phase 6b. The Phase 5 reference-bias caveat
(37.5% panel-wide non-native) does NOT localise to the manuscript-load-bearing
Gs→Gi cell — that cell is 83.3% native-anchored (20/24). See C-B-10.

**Anchor sanity** (§5.2): cognate rows anchor within cluster-boot CI of
zero on every stratum × backbone on tilt and NPxxY-OH. Apo rows anchor
at −4.75 to −5.28 Å on tilt (the "receptor alone" floor).

**Dossier**: `§Phase 5, §Phase 6b`. **Source CSV**:
`donor_class_residuals_summary.csv` + `phase5_power_analysis.csv`.

**Qualified by**: C-B-10 (reference-bias caveat does not localise to
load-bearing cell), W-B-3 (Gs→Gq third finding held pending native-only
power), W-B-4 (Outcome B withdrawn).

---

### SC-B-7 — Templates were not used on any of the four backbones (Class b + c evidence)

**Claim**: Templates off across Boltz-2, Chai-1, OpenFold-3-preview, and
Protenix v2 on all 32,000 Block B rows. Evidence class (b) launcher static
analysis + class (c) upstream source defaults. Class (a) per-row runtime
echo is not present on Block B outputs (see C-B-1).

**Evidence table** (per Phase 0 §0d + Phase 0 templates-sweep):

| Backbone | (a) rows.csv echo | (b) launcher grep | (c) upstream default |
|---|---|---|---|
| Boltz-2 | absent | no template flag in `qsub/rerun_boltz.sh` | input YAML never populates `templates:` field |
| Chai-1 | absent | no template flag in `qsub/rerun_chai.sh` | `use_templates_server = False` default at `chai_lab/chai1.py:334, 492` |
| OpenFold-3-preview | absent | **explicit `--use-templates false`** on both paths of `qsub/rerun_of3.sh` | (also default) |
| Protenix v2 | absent | no template flag in `qsub/rerun_protenix.sh` | `use_templates = False` model-config default |

**Templates-sweep** (20 HPC `_<backbone>_status.json` files, 5 per backbone,
stratified across receptors and arms): 0 of 20 files carry a
`runtime_config` block; 0 of 20 carry any `template*` / `pdb70` /
`pdb_seqres` / `custom_templates` key at any depth. Regression detector
(audit #9 template regression) negative on the sample.

**Exclusion set applied**: baseline.

**Dossier**: `§Phase 0d + §Phase 0 templates-sweep`. **Source docs**:
`docs/BLOCK_B_DOSSIER_PHASE_0_PROVENANCE.md §0d`,
`docs/BLOCK_B_DOSSIER_PHASE_0_TEMPLATES_SWEEP.md`.

**Qualified by**: C-B-1 (evidence class (b)+(c) not (a); no row-level
runtime echo), Flag B-5.

---

### SC-B-8 — Construct identity verified by sequence hash on 40/40 receptors

**Claim**: Every decoy is length-matched to its cognate Gα parent,
byte-identical over the first 339–349 residues, and edited over the last
9–11 residues at the α5-CT tail (median tail Hamming 9.5). Every shuffled
donor is strictly outside the receptor's `{cognate_class} ∪
{secondary_classes}` — no same-class or same-secondary confusions on any
of the 40 Class A receptors. Only three distinct donor sequences are used
across the 40 shuffled arms (alphas × 33, alphai1 × 6, alpha13 × 1).

**Compensating control**: The manifest emitter's `propose_py_git_sha` and
`build_manifest_py_git_sha` are empty in `manifest.provenance.json`
(see C-B-12). Construct identity is verified by content, not by generator
version — byte-identical prefix, length parity, tail confined to α5-CT,
tail Hamming ≥ 7 per row; parent-Gα routing checked against
`refs/gpcr_coupling.csv` (40/40 including edge cases OPSD → alphat and
EDNRA → alphaq).

**Exclusion set applied**: baseline.

**Dossier**: `§Phase 1b, §Phase 1c`. **Source CSV**:
`experiments/019_block_b_partner_selection/analysis/donor_ga_class.csv`
(640 rows, one per cell).

**Qualified by**: C-B-12 (empty generator SHAs, compensating control
by content).

---

### SC-B-9 — The decoy α5-CT edit reaches the model as an aligned MSA column on 3 of 4 backbones

**Claim**: On Boltz-2, OpenFold-3, and Protenix v2, the decoy query row
in the MSA the backbone consumes carries the scrambled α5-CT residues as
uppercase aligned columns (verified on 18/18 audited cells, 6 receptors
× 2 arms × 3 backbones). On Chai-1, the local `.aligned.pqt` cache anchors
the decoy query row to WT-parent residues, gaps, or lowercase insertions
at the α5-CT positions (0/40 uppercase aligned).

**Numbers** (Phase 1D extension aggregate):

| Category | Boltz | OF3 | Protenix | Total (Chai excluded — Phase 1) |
|---|---:|---:|---:|---:|
| Decoy edit READ as uppercase aligned columns in query row | 6/6 | 6/6 (by construction) | 6/6 | 18/18 |
| Decoy MSA byte-identical to cognate MSA (same-receptor) | 0/6 | 0/6 (hash-key) | 0/6 | 0/18 |
| Query row shows scrambled residues as lowercase / soft-masked | 0/6 | n/a | 0/6 | 0/12 empirical |

**OF3 caveat**: raw MSA is purged from `$TMPDIR/of3-of-sengaad1/colabfold_msas/`
after each job; direct column-level inspection impossible. Compensating
chain of evidence: `inference_query_set.json` records decoy sequence
bytes as chain-B query; ColabFold shim forwards them verbatim; row 0 of
any ColabFold return is the queried sequence by construction (empirically
confirmed on Boltz + Protenix on the same queries).

**Critical-stop trigger** ("decoy edit not read at column level by ≥ 3
backbones") is NOT met — only Chai has the not-read-at-column-level
pattern.

**Exclusion set applied**: baseline. Chai's non-read is not corpus-invalidating
but is a per-backbone caveat (see C-B-2).

**Dossier**: `§Phase 1d, §Phase 1d extension`. **Source docs**:
`docs/BLOCK_B_DOSSIER_PHASE_1_CONSTRUCT_IDENTITY.md §1d`,
`docs/BLOCK_B_DOSSIER_PHASE_1D_EXTENSION.md`.

**Qualified by**: C-B-2 (Chai systematically different).

---

### SC-B-10 — Corpus grid-complete: 32,000 / 32,000 rows delivered, zero cells non-conforming

**Claim**: Every one of the 640 (receptor × arm × backbone) cells has
exactly 5 distinct dispatch seeds × 10 samples per seed = 50 rows.
Zero arm shortfall (apo/cognate/shuffled/decoy all 8,000 rows exactly).
Zero rows with `seed_used = "2746317213"` (OF3 seed-bug sentinel).

**Numbers**:

| Statistic | Value | Expected | Match |
|---|---:|---:|---|
| Total rows | 32,000 | 32,000 | ✓ |
| (receptor, arm, backbone) cells | 640 | 640 | ✓ |
| Rows per cell — set of unique values | {50} | {50} | ✓ |
| Distinct seeds per cell — all 640 cells | 5 | 5 | ✓ |
| Rows with OF3 sentinel seed | 0 | 0 | ✓ |
| Rows with `scorer_git_sha = "no-git"` | 0 | 0 | ✓ |

**Recovery journey** (three rounds, `docs/BLOCK_B_DOSSIER_PHASE_2_EXECUTION_CENSUS.md §2a`):
Round-1 queue-state 99.16% (with 300 silent-fails; patched at `50cf136`)
→ Round-2 (m_mem_free=64G) recovered 26 of 27 residuals → Round-3
(`b08ec91`, OF3 purge-race) closed remaining rows. Final rescore:
`rescore_parallel.provenance.json` records `n_total=32000, n_failed=0`,
`finished_at_utc=2026-09-03T16:10:56+00:00`.

**Intermediate-state OF3 decoy/cognate ratio 6.0×** (Round-1 residual
n=27) does exceed a 3× "surface immediately" threshold — but the
population it describes was fully recovered; it does not survive into
the delivered corpus. Recorded as diagnostic-provenance note, not a
live bias. Round-2 report attributes it to memory pressure at 32G,
not a shallow-MSA-arm bug.

**Exclusion set applied**: baseline.

**Dossier**: `§Phase 2`. **Source CSV**:
`experiments/019_block_b_partner_selection/analysis/rows.csv` +
`rescore_parallel.provenance.json`.

**Qualified by**: C-B-16 (Block A OF3 seed bug asymmetry with Block B).

---

### SC-B-11 — No ladder-height covariate has a slope excluding zero at 95% CI

**Claim**: On the three usable predictors (Δ_ref NPxxY-OH, Δ_ref TM6-tilt,
coupling promiscuity from `refs/gpcr_coupling.csv`), no panel slope
excludes zero at 95% CI on either continuous or logit scale, with or
without AA2AR. Under the CI-gated reading, ladder height does not scale
with reference gap or coupling promiscuity at the resolution 40 receptors
support.

**Numbers** (panel regressions; cluster-boot 95% CI over 26 paralog
clusters):

| predictor | scale | n | slope (all) | 95% CI | n (no AA2AR) | slope (no AA2AR) | 95% CI (no AA2AR) |
|---|---|---:|---:|---|---:|---:|---|
| Δ_ref NPxxY | continuous | 28 | -0.002 | [-0.037, +0.032] | 27 | -0.009 | [-0.045, +0.025] |
| Δ_ref NPxxY | logit | 34 | -0.037 | [-0.128, +0.080] | 33 | -0.037 | [-0.127, +0.086] |
| Δ_ref tilt | continuous | 32 | +0.049 | [-0.122, +0.270] | 31 | -0.003 | [-0.149, +0.143] |
| Δ_ref tilt | logit | 40 | +0.134 | [-0.222, +0.486] | 39 | +0.137 | [-0.220, +0.492] |
| coupling promiscuity | continuous | 32 | -0.106 | [-0.563, +0.342] | 31 | -0.017 | [-0.464, +0.430] |
| coupling promiscuity | logit | 40 | -0.072 | [-0.841, +0.663] | 39 | -0.074 | [-0.877, +0.665] |
| deposition_count | (both) | — | NaN (degenerate: every receptor has 2 refs, std=0) | | | | |

**AA2AR sensitivity**: Δ_ref tilt continuous slope drops +0.049 → −0.003
when AA2AR is excluded, i.e. AA2AR alone accounts for the entire
panel-level slope on this predictor × scale combination. Other predictors
stable to AA2AR removal.

**Exclusion set applied**: E-B-2 (AA2AR) reported alongside the panel.

**Dossier**: `§Phase 6a`. **Source CSV**: `ladder_height_covariates.csv`,
`ladder_height_regressions.csv`.

**Qualified by**: C-B-8 (AA2AR anomaly), C-B-14 (no signal on any
predictor).

---

### SC-B-12 — Contact register at the receptor–Gα interface is canonical across every arm

**Claim**: The receptor BW positions most frequently in contact with the
last-5 partner residues on 160 engaged cells per arm are the canonical
Class A Gα-binding face — R3.50, TM6 apex (6.29–6.36), H8 (8.47/8.49),
TM2 (2.39), TM7 (7.56). No non-canonical binding-face signature appears
on any arm. Absolute counts on TM6 apex positions fall
apo → shuffled → decoy (e.g. 6.33: 327 → 297 → 156), i.e. decoy makes
fewer TM6-apex contacts even when engaged.

**Numbers** (top BW positions by contact count; aggregated across 160
engaged cells per arm):

| arm | top BW positions (occurrence count in decreasing order) |
|---|---|
| cognate | 3.50 (379), 8.47 (325), 6.36 (313), 6.33 (304), 2.39 (285), 7.56 (238), 6.32 (235), 6.29 (184) |
| shuffled | 6.36 (321), 6.33 (297), 8.47 (273), 3.50 (273), 6.32 (247), 6.29 (216), 7.56 (202), 2.39 (199) |
| decoy | 3.50 (227), 8.47 (212), 6.36 (171), 7.56 (159), 6.33 (156), 2.39 (146), 8.49 (120), 6.32 (118) |

**Exclusion set applied**: baseline. Restricted to engaged cells
(tip < 20 Å) by construction.

**Dossier**: `§Phase 4a`. **Source CSV**: `interface_pif_connector.csv`
(BW register JSON per cell).

**Qualified by**: C-B-6 (engagement cutoff sensitivity).

---

### SC-B-13 — Reference audit clean: 0 new curation errors, 0 changed PDB assignments

**Claim**: Of the 80 references (40 receptors × 2 roles) that Block B was
scored against at `ref_set_csv_sha256 = 6ee2cad8…`, 25 active refs are
Ga-complexed-native, 10 are chimera-or-miniG, 3 are nanobody-stabilised,
2 are agonist-only-no-partner. Two pending-curation items (AGTR1/6OS2
β-arrestin-biased annotation; CNR2/5ZTY multi-mutation annotation) were
committed at `cda27e2` after Block B ran; neither shifts a PDB ID and
neither shifts a numeric column. **No GATE 6 FAIL trigger.**

**Numbers**:

| activation_class | count | fraction |
|---|---:|---:|
| Ga-complexed-native | 25 | 62.5% |
| Ga-complexed-chimera-or-miniG | 10 | 25.0% |
| nanobody-stabilised | 3 | 7.5% |
| agonist-only-no-partner | 2 | 5.0% |
| **total non-native** | **15** | **37.5%** |

**Preload check** — the 6 inactive references added post-run (AA2AR/5MZP,
ADA1A/7YMJ, ADRB2/2RH1, ADRB2/3NYA, CCR5/4MBS, CNR1/5TGZ) are all
secondary; the primary inactive references for the 3 Block B receptors
in the list (AA2AR/5NM4, ADRB2/6PS2, CNR1/5U09) were present in
`6ee2cad8` and computable on both axes. `delta_to_inactive` is not
forced NaN by this preload on any Block B receptor (see C-B-9).

**The 4 receptors with all-NaN NPxxY-OH** (EDNRA, EDNRB, GRPR, HRH3) NaN
because 7.53 = L not Y in the receptor sequence — intrinsic-biology axis
property, not a missing-reference issue.

**Exclusion set applied**: baseline. Reference set = `6ee2cad8` scoring-time
bytes (recovered from commit `a355977`, archived at `refs/reference_set.blockb_pinned.csv`,
commit `8e5ea48`).

**Dossier**: `§Phase 6c`. **Source CSV**: `reference_audit.csv`.

**Qualified by**: C-B-9 (scoring-time reference set), C-B-11 (AGTR1/CNR2
annotation refinements).

---

### SC-B-14 — The pre-registered Outcome B (model reads partner identity on the continuous axis) is NOT signed anywhere at 95% CI

**Claim**: Phase 5 §5.0 pre-registered two outcomes with equal
manuscript-facing status: Outcome A (residuals near zero → model
treats partner as bulk) and Outcome B (Gs donors overshoot Gi/Gq
receptors' references and vice versa → model reads partner identity
on continuous axes below the binary predicate's resolution). Under
the pre-registered CI-gated test, **Outcome A signed on the load-
bearing Gs→Gi cell (SC-B-6) and Outcome B did not sign anywhere.**
This is a signed test result on a pre-registered alternative, not a
retracted claim; it lives on the claim sheet rather than in
withdrawals.

**Numbers** (from Phase 5 §5.4 CI-gated sign test, panel-level,
per-backbone breakdown in `donor_class_residuals_summary.csv`):

| stratum | cells with CI excluding 0 in Outcome-B direction | cells with CI excluding 0 in anti-B direction | undetermined |
|---|---:|---:|---:|
| boltz | 0 | 1 (Gs→Gq tilt, anti-B) | 8 |
| chai | 0 | 0 | 9 |
| of3 | 1 (Gi→Gs delta) | 2 (Gs→Gq tilt; Gs→Gq NPxxY anti-B) | 6 |
| protenix | 0 | 1 (Gs→Gi NPxxY anti-B) | 8 |
| **panel** | **0** | **1** | **8** |

Panel-level: **0/9 qualifying strata × axes sign in the Outcome-B
direction with CI excluding zero.** A weak Outcome-B trend on median-
sign alone (6/9 at panel; 5–7 of 9 per backbone) but never crossing
cluster-boot noise.

**Exclusion set applied**: baseline; E-B-4 (native-only) applied
alongside for the Gs→Gi power analysis (see SC-B-6).

**Dossier**: `§Phase 5 §5.4` + `§Phase 6b`. **Source CSVs**:
`donor_class_residuals_summary.csv`, `phase5_power_analysis.csv`,
`donor_class_covariate_regression.csv`.

**Qualified by**: SC-B-6 (Outcome A signed and firmed); C-B-10
(reference-bias caveat does not localise to load-bearing cell). Formerly
filed as W-B-4; moved 2026-09-10 per `docs/BLOCK_B_POSTFREEZE_CHECKS.md`
Check 4 — pre-registered non-signature is a result, not a withdrawal.

---

## Withdrawn claims (see `withdrawals/`)

- **W-B-1** — Family term as "~11%" as a single scale-neutral number
- **W-B-2** — Per-receptor midpoint ladder 0.130 / 0.500 / 0.801 / 0.887
- **W-B-3** — Phase 5 Gs→Gq third finding (−0.47 Å tilt) as manuscript line
- **W-B-4** — Outcome B ("model reads partner identity on continuous axis")
- **W-B-5** — Dispatch-plan "Block A shuffled 94%" misattribution
- **W-B-6** — "1,263 of 1,935 non-inserted decoy contact count > 20" as an
  exact reproducible pair on the delivered Block B corpus

## Live caveats (see `caveats/`)

- **C-B-1** — Templates-off evidence class b+c, not a (no per-row runtime echo)
- **C-B-2** — Chai systematically different (partial MSA read, tilt inversion, pLDDT test unmeasurable)
- **C-B-3** — `rows.fold_integrity.csv` carries 0% per-row provenance columns
- **C-B-4** — No `outputs/` symlink for Block B — ergonomic gap
- **C-B-5** — Frame-36 vs frame-40 denominator convention
- **C-B-6** — 20 Å engagement cutoff permissive at cognate; report both 14 Å and 20 Å
- **C-B-7** — Ceiling-pinning on family term (24–34 of 40 receptors × backbones)
- **C-B-8** — AA2AR recurrently anomalous; excluded from pooled inference where noted
- **C-B-9** — Reference-set scored at `6ee2cad8`; 6 inactive rows added post-run but none as primaries
- **C-B-10** — Phase 5 reference-bias caveat: 37.5% non-native panel-wide but does not localise to the load-bearing Gs→Gi cell (83.3% native there)
- **C-B-11** — AGTR1 6OS2 + CNR2 5ZTY annotation refinements; both invert on Block C classifier
- **C-B-12** — Manifest emitter empty `propose_py_git_sha` / `build_manifest_py_git_sha`; compensating control by content
- **C-B-13** — Paralog cluster map reconstructed 2026-09-09 (26 clusters, 40 receptors)
- **C-B-14** — Ladder-height covariates: no panel slope excludes zero at 95% CI
- **C-B-15** — Class A only (Class B/F not in Block B)
- **C-B-16** — Block A vs Block B OF3 effective-n asymmetry (constant-seed bug vs 5 distinct seeds)

## Deferred limitations (in BLOCK_B_MANUSCRIPT_FLAGS.md)

- Runtime-config echo audit at Block B row-grain (only on 20-file sample)
- rows.csv self-SHA sidecar (deferred with recorded_at discipline for future dispatches)
- Chai `.aligned.pqt` code-inspection to determine whether the pqt query row or the raw decoy sequence is what Chai's MSA-feature builder ingests at column level (out of Phase 1 scope; not blocking manuscript sentence per SC-B-9)
- Gi→Gs shuffled cell resolution (n=5, 0 native — cannot resolve on Block B references alone)
- Deposition_count as a covariate (proxy degenerate on this corpus; requires external RCSB source)
- Panel-wide MSA α5-CT column audit on Block D and later blocks
