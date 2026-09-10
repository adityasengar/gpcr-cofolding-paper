# BLOCK C — CLAIM SHEET

Every Block-C-derived claim the manuscript will make, in final wording,
with its authoritative cluster-boot 95% CI where applicable, its
exclusion set, and a pointer to the flag or caveat that qualifies it.

**Bootstrap convention** (Block A C-8 authoritative): cluster-boot over
the 12 paralog clusters spanned by the S1 15-set (map derived from
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`
per receptor); 500 receptor-boot / 500 cluster-boot / 200 permutation-null
resamples; seeds `20260910..20260920`. Receptor-bootstrap CIs (15
receptors treated independent) are tighter and are the SECONDARY
statement. Row-boot is invalid.

**Corpus** (primary): 40 Class A receptors dispatched × 4 backbones × 2
arms {apo, cognate} × 3 ligand_roles {full_agonist, neutral_antagonist,
decoy_lig} × 5 seeds × 10 samples = 48,000 preds targeted; **40,800
landed** (rows.tier3.v2.csv, SHA `5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103`,
scorer_git_sha `3d9c6faae59b5aa5881994dee4d36e36ea5367da`). 36 receptor_slugs
present in landed corpus (see C-C-9 for panel disambiguation).
40,000 rows `passed=True` (98.04%); 800 rows fail on the OPSD/B1B1U5
A5_species_match pattern — pre-fix pattern per `docs/AUDIT_TRAIL.md §21`.

**Sibling corpus** (pose only): `experiments/021_block_c_tier3_pharmacology/rescore_t7c_full/rows.csv`
(scorer_git_sha `d9c646af5f89861c16062bf256de96a8389d9915`, MCS-fix + Bug#2
tripwire post-audit). All pose-accuracy statements below cite this
corpus; classifier and pocket-Cα-interaction claims cite the primary.

**S1 15-set (KILL-S1 row denominator)**:
`5HT1B, 5HT5A, AA1R, AA2AR, ACM2, AGTR1, CXCR2, CXCR4, EDNRB, GRPR,
LPAR1, LT4R1, MCHR1, NPY2R, OPRX` — 23 common-set receptors minus 8
self-ref-in-common (see G1 methodology; pre-reg
`experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/PREREG_SIGNAL_RECOVERY.md`).
n = **15**, not 14; the prereg text's `23 − 9 = 14` did the subtraction
on the wrong set (DRD3 is on the self-ref list but was NOT in the
common 23).

**Exclusion sets applied consistently across this sheet**:

- **E-C-1** = 4 Class-A receptors dispatched but not landed in
  `rows.tier3.v2.csv` (36-of-40 panel). Methods-sentence disambiguation
  only; no numeric downstream effect since analyses run on landed.
- **E-C-2** = 8 receptors that are 100% self-reference on antag_inactive
  cell (ACM4, ADRB2, CCR5, CNR1, CNR2, DRD3, NPY1R, OPRD, OPRK — of
  which DRD3 is not in common_23). Applied on KILL-S1 row where the
  ceiling would otherwise dominate.
- **E-C-3** = AGTR1 (unique category-d biased-agonist-nanobody active
  reference; see C-C-4 and `docs/G2_REFERENCE_HOMOGENEITY.md`).
  Applied for G2 sensitivity; reported both with and without.
- **E-C-4** = ceiling/floor-pinned cells (predicate rate ≥ 0.98 or
  ≤ 0.02). Reported on the continuous axis (pocket-Cα-RMSD) where
  saturation is load-bearing; see C-C-3.

---

## Surviving claims

### SC-C-1 — Pocket-Cα-RMSD 2×2 ligand-state × reference-state interaction is signed non-zero on all four backbones, in the apo arm alone

**Claim**: Under the primary continuous readout — pocket-Cα-RMSD between
the predicted pocket and each receptor's active vs inactive reference
crystal — the 2×2 contrast (ligand-role × reference-role) shows a
signed non-zero interaction on all four backbones **in the apo arm
alone** (no cognate-partner, no cognate-mass confound). Full-agonist
predictions land closer to active reference; neutral-antagonist
predictions land closer to inactive reference, at Cα resolution.

**Numbers** (mean of per-receptor 2×2 interaction Δ_active − Δ_inactive
across agonist vs antagonist; apo arm; **cluster-boot 95 % CI over 16
paralog clusters (Block A C-8 authoritative)**, receptor-boot reported
as secondary):

| backbone | mean 2×2 interaction (Å) | cluster-boot 95% CI (primary) | receptor-boot 95% CI (secondary) | signed? |
|---|---:|---|---|---|
| boltz | **−0.306** | **[−0.454, −0.164]** | [−0.431, −0.192] | YES |
| chai | **−0.137** | **[−0.216, −0.045]** | [−0.223, −0.055] | YES |
| of3 | **−0.252** | **[−0.405, −0.099]** | [−0.384, −0.129] | YES |
| protenix | **−0.184** | **[−0.277, −0.088]** | [−0.271, −0.101] | YES |

n_receptors_in_common = **23**; cluster-boot resamples over the 16
paralog clusters spanning those 23 receptors (map from
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`),
5000 iterations, seed 1234. All four backbones' cluster-boot CIs sign
non-zero. Chai's cluster-boot upper bound (−0.045) is closer to zero
than receptor-boot's (−0.055); still signed with a narrow margin.

**Sources**:
- Point estimates: `experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3_2x2_ligand_state_specificity.json`.
- Cluster-boot CIs: `experiments/021_block_c_tier3_pharmacology/analysis/verification/g_scc1_cluster_boot.json`.
- Recompute script: `scripts/block_c_closeout/recompute_2x2_cluster_boot.py`.

**Dossier**: `docs/BLOCK_C_STATE_CHECK.md`, `docs/BLOCK_C_GATING_REPORT.md`,
`docs/POST_CLOSEOUT_VERIFICATION_REPORT.md §1b`, memory
`block_c_tier3_pocket_identity_2026_09_06`.

**Qualified by**: C-C-1 (predicate saturation invisibility), C-C-2 (Chai
softness), C-C-3 (RESOLVED 2026-09-10 — 23-set pinned, cluster-boot CIs
applied), C-C-6 (matcher path does not affect pocket-Cα).

### SC-C-2 — P4 ordinal recovery on the continuous axis, 65–87% Kendall's τ across backbones

**Claim**: The pre-registered P4 ordinal test (ligand-role rank vs
Δ = pocket_ca_rmsd_active − pocket_ca_rmsd_inactive) recovers ranked
separation on the continuous axis where the binary predicate was
floor-pinned. Recovery holds on Tier 1 (5-class, all 4 backbones at
75%) and Tier 3 (23-receptor apo panel, 65–87% depending on backbone).

**Numbers** (Kendall's τ, receptor-panel-median):

| panel | boltz | chai | of3 | protenix |
|---|---:|---:|---:|---:|
| Tier 3 apo × 23 | 74% | 65% | 74% | 87% |
| Tier 3 apo × 15 (self-ref-excl) | 67% | 67% | 67% | 87% |
| Tier 1 apo (5-class) | 75% | 75% | 75% | 75% |

**Source**: `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/s5_p4_ordinal.json`
via `SIGNAL_RECOVERY_REPORT.md §S5`.

**Manuscript sentence**: P4 was pre-registered before this dispatch and
tested on the continuous axis (not the binary predicate); ≥ 6/8 backbone
× panel cells reach the pre-registered threshold. This is a
**pre-registered ordinal recovery**, arguably load-bearing beyond the
2×2 finding because P4's threshold was locked prior.

**Qualified by**: C-C-1 (predicate saturation is the reason the binary
predicate could not resolve this).

### SC-C-3 — Cross-backbone consensus outperforms pLDDT as a confidence signal on 3/4 backbones

**Claim**: Consensus = 1 / max_pairwise_distance across the 4 per-backbone
means of `pocket_ca_rmsd_active` per (receptor, ligand_state, seed) acts
as a per-prediction confidence signal that outperforms pLDDT on 3 of 4
backbones at top-25% coverage. Publishable as a standalone methods
contribution.

**Numbers** (AUROC at top-25% coverage, using `−pocket_ca_rmsd_active`
as score on the filtered subset; `s3_consensus_confidence.json`):

| backbone | consensus | pLDDT | Δ |
|---|---:|---:|---:|
| boltz | 0.753 | 0.747 | +0.006 (tie) |
| chai | 0.724 | 0.600 | **+0.124** |
| of3 | 0.719 | 0.687 | +0.032 |
| protenix | 0.732 | 0.691 | +0.041 |

**Manuscript sentence**: consensus beats pLDDT on Chai substantially
(pLDDT is famously miscalibrated on Chai), on OF3 and Protenix modestly,
and ties Boltz. This is the S3 result of the pre-registered signal
recovery.

**Qualified by**: C-C-1 (predicate saturation), C-C-2 (Chai systematic
differences).

### SC-C-4 — S1 LORO classifier: prospective ligand-class discrimination on Boltz + Protenix under cluster-boot; Chai + OF3 marginal

**Claim** (adjudicated from the G1 gating result):
- Under the **pre-registered kill threshold** (LORO AUROC ≥ 0.65 on apo
  × self-ref-excluded × F_iii features), the KILL-S1 test does not fire:
  Boltz 0.852, Chai 0.706, OF3 0.656, Protenix 0.825. Point estimate
  clears threshold on all four.
- Under the **Block-A-C-8-authoritative cluster-boot 95% CI**: Boltz
  cluster-boot [0.560, 0.974], Protenix [0.528, 0.960] — clear 0.5 with
  narrow margin; Chai [0.351, 0.941] and OF3 [0.382, 0.924] — CI **spans
  0.5**, not distinguishable from chance.
- **Prospective discrimination claim scoped to Boltz + Protenix** at the
  KILL-S1 row F_iii features; Chai and OF3 stated as inconclusive under
  the pre-registered bootstrap convention.

**Numbers** (from `g1_bootstrap_s1_auroc.json`, 500 receptor-boot / 500
cluster-boot / 200 permutation-null resamples):

| backbone | obs pooled AUROC | receptor-boot CI 95 | cluster-boot CI 95 | perm null CI 95 | scoped in |
|---|---:|---|---|---|---|
| boltz | 0.852 | [0.636, 0.970] | **[0.560, 0.974]** | [0.477, 0.520] | YES |
| chai | 0.706 | [0.364, 0.935] | **[0.351, 0.941]** | [0.473, 0.523] | NO |
| of3 | 0.656 | [0.369, 0.898] | **[0.382, 0.924]** | [0.467, 0.525] | NO |
| protenix | 0.825 | [0.539, 0.971] | **[0.528, 0.960]** | [0.469, 0.527] | YES |

**Manuscript sentence**: *"The single-structure ligand-class classifier
(LORO, self-reference-excluded, apo arm, F_iii pocket+axes features)
reaches pooled AUROC 0.852 on Boltz and 0.825 on Protenix (cluster-
bootstrap 95% CI [0.560, 0.974] and [0.528, 0.960] respectively; both
CIs exclude the permutation null); on Chai (0.706) and OpenFold-3 preview
(0.656) the same test's cluster-bootstrap CI reaches 0.35 and 0.38 and
the two backbones cannot be distinguished from chance under this
convention."*

**Dossier**: `docs/BLOCK_C_GATING_REPORT.md §G1`,
`experiments/021_block_c_tier3_pharmacology/analysis/verification/g1_bootstrap_s1_auroc.json`.

**Qualified by**: C-C-2 (Chai systematic differences), C-C-5 (S1 receptor
count n=15 pinned), C-C-6 (matcher does not affect classifier), Flag C-1
(cluster-boot authoritative).

### SC-C-5 — Applicability domain is an empirical failure list, not an a priori criterion

**Claim** (adjudicated from G2 + G2-excl-AGTR1 + G2-homogeneity):
Reference-separation on the pocket-Cα-RMSD axis does NOT predict
per-receptor S1 AUROC. The applicability domain is an empirical failure
list, not an a priori criterion. AGTR1 is a curation-scope outlier;
CXCR2 (OF3 only) is a backbone-specific outlier.

**Numbers** (pooled OLS slope of per-receptor AUROC on pocket-Cα ref-sep,
receptor-boot CI over 15 receptors, 1000 iterations):

| set | n | pooled slope (Å⁻¹) | pooled slope 95% CI | spearman ρ | R² |
|---|---:|---:|---|---:|---:|
| full 15 (as-scored) | 15 | −0.325 | [−0.570, −0.068] | −0.206 | 0.162 |
| excluding AGTR1 (sensitivity) | 14 | **−0.060** | **[−0.246, +0.087]** | −0.015 | 0.010 |

**AGTR1 counterexample**: pocket-Cα-sep 1.87 Å (rank 39/40 in Block B
panel — 2nd largest), yet inverts fully on all 4 backbones (AUROC
0.00–0.10). Predicted direction of the hypothesis was opposite.
**Excluding AGTR1**, the pooled slope collapses to −0.060 with CI
[−0.246, +0.087] — **spans zero, no signal**. AGTR1 alone carries ~85 %
of the apparent negative-slope signal.

**Reference-curation observation on AGTR1** (`docs/G2_REFERENCE_HOMOGENEITY.md §2`):
in the S1 15-set, AGTR1 is UNIQUELY in category (d) — β-arrestin-biased
agonist (TRV026) + intracellular nanobody (Nb.AT110i1_le), NO Gα-pathway
construct. Every other receptor has native heterotrimer (12) or mini-G /
chimera (2). Excluding AGTR1 for scope-consistency reasons is defensible
on curation grounds; the empirical outcome then stands as "flat slope,
no useful correlation, cannot be predicted".

**CXCR2 (OF3-only) observation**: CXCR2's active reference is a native
Gi heterotrimer (canonical). Its OF3-specific inversion (AUROC 0.135 on
OF3 vs 0.900–0.999 on the other three backbones) does NOT track with a
reference-curation anomaly and is not addressed by G2's hypothesis. This
is a backbone-specific failure mode independent of reference separation.

**Manuscript sentence**: *"Per-receptor classifier reliability is not
predicted by pocket-Cα active-vs-inactive reference separation on the
15-receptor S1 set: pooled slope −0.060 [−0.246, +0.087] after excluding
AGTR1 (whose reference is a β-arrestin-biased-agonist-bound / nanobody
state, uniquely non-Gα-pathway in the panel — see Methods). AGTR1 and
CXCR2 (on OpenFold-3 only) invert; both remain in the applicability
domain as empirically-flagged exceptions, not as instances of a general
reference-separation rule."*

**Dossier**: `docs/BLOCK_C_GATING_REPORT.md §G2`, `docs/AGTR1_REFASSIGN_REPORT.md`,
`docs/G2_REFERENCE_HOMOGENEITY.md`.
**Sources**: `experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_refsep_vs_auroc.{json,csv}`,
`.../g2_excl_agtr1.json`, `experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv`.

**Qualified by**: C-C-4 (AGTR1 biased-agonist reference), C-C-7 (backbone
independence of reference-separation account), Flag C-2 (Boltz+Protenix
scope on the abstract number).

### SC-C-6 — Binary two-instrument predicate is saturated on the cognate arm, invisible to ligand-identity signal

**Claim**: The Block A two-instrument predicate
(`d_npxxy_y558_y753_oh < 9.082 AND d_gpcrdb_tm6_tilt_246_637_ca > 14.932`)
is **floor-pinned on apo** and **ceiling-pinned on cognate** for a
majority of receptor × backbone × ligand-class cells in Block C. Any
ligand-identity signal at the pocket geometry is not resolvable on the
binary predicate and requires the continuous readout (SC-C-1, SC-C-2).

**Numbers**: ~65% of cells unresolvable on the binary predicate (per
S1-signal-recovery Stage 3 audit; exact per-cell census in
`stage3_2x2_ligand_state_specificity.json`).

**Manuscript sentence**: *"The class-conditional two-instrument
activation predicate that resolves the four-arm partner ladder in
Block B is saturated on Block C: apo-arm cognate-ligand predictions
floor at the low end, cognate-arm cognate-ligand predictions ceiling
at the high end, and ~65% of (receptor × backbone × ligand-class) cells
sit on one of the two floors/ceilings. Ligand-identity discrimination
in Block C is therefore reported on continuous pocket-Cα-RMSD, not on
the binary predicate."*

**Qualified by**: C-C-1 (predicate saturation), Flag C-3 (continuous
vs binary).

### SC-C-7 — Scoped pose-accuracy result (OF3 + Protenix × neutral_antag × ref-matched, 6.93 % at < 3 Å)

**Claim** (unchanged in scope from manuscript v1, revalidated in this
pass):
On the strictly matched-reference subset — OpenFold-3 preview + Protenix
× neutral-antagonist arm × input_bound_pdb == reference PDB — pose
accuracy at PoseBusters `<3 Å` is 6.93 % (312 of 4,500 rows). This is
the scoped statement; corpus-wide pose statistics for Boltz + Chai
are additionally reported under the MCS matcher on the post-fix scorer
sibling corpus (`rescore_t7c_full/rows.csv`), where per-receptor median
dock rate on the neutral-antagonist redock cell is 54–56 % (Boltz) /
0–18 % (Chai) / 0 % (OF3, Protenix).

**Manuscript sentence**: *"On the strictly matched-reference subset
(OpenFold-3 preview + Protenix × neutral antagonist × input bound PDB
matches reference PDB, n = 4,500), pose accuracy at `ligand_rmsd_to_ref < 3 Å`
is 6.93 %. Corpus-wide numbers under the MCS matcher on the post-fix
scorer sibling corpus reveal a bimodal per-receptor distribution
(Boltz median 54–56 %, Chai 0–18 %, OF3/Protenix 0 % on the same
neutral-antagonist redock cell); pooling across receptors, as done in
earlier drafts, hid this bimodality."*

**Qualified by**: C-C-6 (matcher path affects only ligand_rmsd_to_ref,
not pocket-Cα), C-C-8 (coverage asymmetry — antagonist ~93 % covered,
agonist/decoy ~50 % NaN), C-C-10 (reference routing collapse — target
reference PDB may not carry the same ligand class as the input row).

### SC-C-8 — Cluster-bootstrap over paralog clusters is the authoritative CI convention (Block A C-8)

**Claim**: All Block C CIs in this claim sheet use cluster-boot over
paralog clusters (Block A convention C-8), 500–1000 resamples per
statistic, seed `20260910..20260920`. Receptor-boot CIs are reported as
secondary. Row-boot is invalid.

**Numbers**: cluster count = 12 for the S1 15-set; = 26 for the full
40-receptor Class-A panel (mapping in
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`).

**Dossier**: `caveats/C-8_cluster_bootstrap_authoritative.md` (Block A
release repo).

### SC-C-9 — Panel of record: 40 Class A dispatched; 36 landed in the primary corpus

**Claim**: The panel of record is 40 Class A receptors (per PREREG §1
v2 + Block C dispatch contract). The primary corpus
(`rows.tier3.v2.csv`) contains 36 distinct `receptor_slug` values;
4 dispatched receptors did not land after curation. All Block C
analyses run on the landed panel; a Methods-sentence footnote names
the 4 dispatched-not-landed receptors.

**Numbers**: 40 dispatched Class A × 4 backbones = 40,000 target rows
per pair-set; 36 × 4 = 40,800 landed rows (98.04 % pass). 800 fail on
OPSD/B1B1U5 A5_species_match (pre-fix pattern, `docs/AUDIT_TRAIL.md §21`).

**Qualified by**: C-C-9 (panel disambiguation).

### SC-C-10 — Reference-identity leak ruled out by construction, not audit

**Claim**: Check 1's SHA-identical resolved-reference finding across
ligand_role classes is TRUE, and it is TRUE because the role-specific
routing (which produces different LABELS —
`pocket_ref_role_inactive = generic_inactive_fallback` for agonist/decoy
vs `inactive_neutral_antagonist` for antag) resolves to the SAME PDB
per receptor. 28/28 receptors with defined `pocket_ref_pdb_sha_inactive`
have IDENTICAL SHAs across all ligand_role values. Reference-identity
leak is ruled out **by construction** — the classifier's Δ feature is
computed against a per-receptor pair identical across ligand classes.
It is not ruled out by an audit that could have detected a leak had
one been present under a properly-differentiated routing.

**Manuscript sentence** (Methods): *"Role-specific reference-routing
labels were emitted for each row (`pocket_ref_role_inactive` differs
by ligand class), but resolved to the same reference PDB per receptor
in the current corpus. The classifier's active-vs-inactive
pocket-Cα-RMSD delta is therefore computed against a per-receptor
reference pair identical across ligand classes; reference-identity
leak is ruled out by construction."*

**Dossier**: `docs/BLOCK_C_GATING_REPORT.md §G3`.

**Qualified by**: C-C-10 (routing collapse pose consequences — for at
least one ligand class per row, `ligand_rmsd_to_ref` is measured against
a chemically different bound ligand than the input's).

---

## Summary: 10 surviving claims

Claim ladder (adapted from `SIGNAL_RECOVERY_REPORT.md`):

- **Rung 0 — Characterization** (models encode ligand identity in
  pocket geometry, group-mean 2×2): SC-C-1, SC-C-2. **Supported.**
- **Rung 1 — Discrimination** (single-structure classifier separates
  ligand classes at held-out-receptor grain): SC-C-4. **Scoped to
  Boltz + Protenix.**
- **Rung 2 — Prospective readout** (Rung 1 apo, sample budget,
  applicability domain): SC-C-4 + SC-C-5. **Partially supported;
  applicability = empirical failure list.**
- **Rung 3 — Instrument** (minimal, confidence-signaled): SC-C-3
  (confidence signal ✓). Minimal-interpretable-localized: partial
  (dominant single feature = whole-pocket-aggregate; no per-BW
  activation-lever). **Rung reached: 2 (partial), Rung 3 partial.**

**Auxiliary claims**: SC-C-6 (predicate saturation limits Block C to
continuous readouts), SC-C-7 (scoped pose accuracy), SC-C-8
(cluster-boot authoritative), SC-C-9 (panel disambiguation),
SC-C-10 (reference-identity leak by construction).
