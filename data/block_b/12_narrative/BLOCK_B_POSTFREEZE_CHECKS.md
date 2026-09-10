# BLOCK B — POST-FREEZE VERIFICATION (bounded)

**Date**: 2026-09-10.
**Scope**: four bounded checks, read-only, no HPC, no subagent, no new phase.
**Baseline**: `block_b_freeze` at `d6c1bef` (12 commits after `pre-block-b-consolidation`).
**Discipline**: strictly the four checks. Any interesting side finding recorded here and stopped.

---

## Check 1 — SC-B-6 equivalence (REVISED: verdict UNDETERMINABLE)

**This section supersedes the first-pass EXCLUDED verdict.** The
initial pass compared a point-estimate ruler (Gs − Gi = 0.579 Å) to a
bootstrapped residual CI. That is a point vs interval comparison, not
an equivalence test. A bootstrap of the ruler itself, at the user's
direction, downgrades the verdict to UNDETERMINABLE. Details below.

### Direction correction (applied throughout this section)

`Gs → Gi` in Phase 5 notation reads: **Gi-coupled receptors receiving
a Gs donor**. Those 24 receptors are the Gi-coupled panel (n=24
matching Gi group), and their active references are Gi-anchored. Under
Outcome B the model reads the Gs donor and produces Gs-typical tilt,
which **overshoots** the receptor's own Gi-anchored reference. The
residual is therefore **positive**: `predicted_tilt − ref_tilt ≈
Gs_median − Gi_median = +0.579 Å` (point estimate). The right
comparison is against the native-only CI's **upper bound (+0.21)**,
not its lower bound (−0.41). The initial pass had this direction
inverted. The arithmetic result was the same either way — |0.579| >
|either bound| — but the reasoning as written was wrong. Fixed here
and in the claim sheet.

### Family grouping and per-family tilts

From `refs/reference_set.blockb_pinned.csv` + `refs/sealed_active_refs_2026_09_01.csv`,
40 Block B active references grouped by transducer family. Family for
each active reference is `alpha5_donor_class` when populated (except
`none_Ga`), else the receptor's cognate Gα from `refs/gpcr_coupling.csv`.

| Family | n | median (Å) | IQR (Å) | range |
|---|---:|---:|---:|---|
| Gi | 24 | 17.518 | 0.664 | [15.783, 19.879] |
| Gq | 10 | 17.183 | 1.121 | [15.773, 19.086] |
| Gs |  5 | 18.097 | 0.481 | [17.563, 18.452] |
| Gt |  1 | 17.586 | — | — |

**Gs group composition (n=5)**: AA2AR (18.10, mini-G), ADRB1 (18.43,
nanobody), ADRB2 (17.56, nanobody), FSHR (17.94, mini-G), LSHR (18.45,
mini-G). **Not native-Gs complexes.** The Gs group mixes engineered
scaffold anchors (mini-G, nanobody) rather than native transducer;
their tilt reflects the engineered construct, not native Gs biology.
With n=5, one or two such entries move the median substantially.

**Gi group composition (n=24)**: 19 native + 3 mini-G + 2 agonist-only.
Native-dominated; the median 17.518 Å is on native transducer complexes.

The two groups are asymmetric on active-stabilisation source. The Gi
group range [15.78, 19.88] **fully contains** the Gs group range
[17.56, 18.45].

### Bootstrap of the ruler (the computation that settles it)

Bootstrapped the Gs − Gi reference-median tilt gap. Percentile
bootstrap, 1000 draws, receptor-boot within family (resample n=5 Gs
with replacement AND resample n=24 Gi with replacement, compute
median-difference each draw). Seed `20260910`.

- Point estimate: **+0.579 Å**
- 95% CI on the gap: **[+0.006, +1.025]**

Sensitivity — Gs without AA2AR (E-B-3 exclusion; n=4):

- Point estimate: **+0.667 Å**
- 95% CI on the gap: **[−0.047, +1.015]** — spans zero.

The ruler CI barely excludes zero on the full Gs group (lower bound
0.006) and does span zero when AA2AR is excluded (a load-bearing
exclusion the dossier uses elsewhere).

### Comparison against the residual CI

Native-only Gs → Gi tilt residual CI (from Phase 6b, n=20 native-anchored
receptors): **[−0.41, +0.21]**. Direction: positive residual = Outcome-B
signature (Gs-typical opening in the Gi-anchored reference frame).

For SC-B-6 to upgrade to a signed equivalence claim, the ruler CI's
lower bound must exceed the residual CI's upper bound (+0.21). The
observed ruler CI lower bound is 0.006 (with AA2AR) or −0.047 (without).
Neither exceeds +0.21. The equivalence test's strict criterion is not
met.

### Reconciliation with Block A's restriction-of-range on tilt

Block A's dossier established that the tilt axis has restricted range
(SD 1.19 Å across 40 Class A active references, against NPxxY's 4.71 Å),
and Block A therefore stated that the tilt axis cannot test amplitude.
The Gs − Gi tilt gap here (0.579 Å point estimate, CI [0.006, 1.025])
sits within Block A's 1.19 Å SD envelope — the restriction of range
Block A named for amplitude also limits identity-sensitivity power on
this axis. **A stronger equivalence claim would contradict Block A's
own statement about this axis; the honest read is that this axis cannot
distinguish Outcome A from Outcome B at the resolution of Block B's
40 receptors.** SC-B-6 therefore stays as an Outcome-A signed
conclusion scoped by the reference-bias caveat (C-B-10), not an
equivalence claim.

### Verdict: **UNDETERMINABLE**

The pre-registered second branch. The equivalence-upgrade attempt does
not survive the ruler-side bootstrap; SC-B-6 reverts to the Phase 6b
wording ("Outcome A signed, CI spans zero on the native-only n=20
Gs→Gi residual"). Not a stronger claim, still a perfectly good result.
Re-powering the test is not in scope.

Text edits made this round:

1. SC-B-6 in `BLOCK_B_CLAIM_SHEET.md` reverted to Phase 6b wording,
   with a post-freeze note recording the equivalence-upgrade attempt
   and why it did not survive.
2. This Check 1 section rewritten with the direction correction, the
   ruler bootstrap, and the Block A restriction-of-range
   reconciliation.
3. Chimera + cognate mix in the Gs group (nanobody + mini-G,
   0 native) explicitly named as a limitation of the ruler.

---

## Check 2 — Two decoy numbers labelled frame_36

### Method

Recomputed the frame_36 decoy active fraction from
`experiments/019_block_b_partner_selection/analysis/rows.csv` under
multiple explicit filter combinations. Predicate: `d_npxxy_y558_y753_oh
< 9.082 AND d_gpcrdb_tm6_tilt_246_637_ca > 14.932`; NaN on either axis
→ False. frame_36 excludes `{ednra, ednrb, grpr, hrh3}` (all-NaN NPxxY
by 7.53 = L not Y).

| frame | aggregation | decoy rate | n |
|---|---|---:|---:|
| frame_40 | row_mean | 0.5021 | 8000 |
| frame_40 | receptor_midpoint | 0.5021 | 40 |
| frame_40 | cell_midpoint | 0.5021 | 160 |
| frame_36 | row_mean | **0.5579** | 7200 |
| frame_36 | receptor_midpoint | **0.5579** | 36 |
| frame_36 | cell_midpoint | **0.5579** | 144 |

Under the uniform (5, 10) × 40 design, `row_mean = receptor_midpoint =
cell_midpoint` to 4 decimal places.

### Source of the two numbers

- **`0.552`** is the dispatch-cited "published" number from the paper
  draft's prior claim and from the Block B consolidation dispatch prompt
  itself. It is a **pre-consolidation snapshot**, likely from an earlier
  corpus state or an earlier scorer commit that has since been superseded.
- **`0.558`** (precise: 0.5579) is the **on-corpus recomputation** from
  today's frozen rows.csv at commit `04531b8` under the exact frame_36
  filter definition. This is what `ladder_four_scorings.csv` records at
  `reproduction_36,decoy,panel,7200,0.5579…` and what Phase 7b's spot-
  check confirmed.

Both use frame_36 (n=36, exclude EDNRA/EDNRB/GRPR/HRH3). Both use the
two-instrument predicate (NPxxY-OH < 9.082 AND tilt > 14.932). The 0.552
falls inside the cluster-boot 95% CI [0.445, 0.664] of the 0.558 point
estimate, so the two numbers are not in statistical conflict — the 0.552
is a low-precision reproduction of the same underlying quantity.

### Bootstrap convention (Block A parity)

Two decoy CIs have appeared on Block B's decoy panel binary rate at
various points:

- **Cluster-boot over 26 paralog clusters**: `[0.445, 0.664]`.
  Stored in `ladder_four_scorings.csv` at
  `reproduction_36,decoy,panel,7200,…,cluster_boot_ci_lo_binary=0.4446,
  cluster_boot_ci_hi_binary=0.6640`. Wider because paralog resampling
  collapses within-cluster variance.
- **Receptor-boot over 40 receptors treated independent**: `[0.51, 0.60]`
  (approximate; noted in an earlier draft of the dossier table).
  Tighter because it ignores paralog dependency.

Per Block A's convention (`paper_af3_release/caveats/C-8_cluster_bootstrap_authoritative.md`),
**cluster-boot is authoritative**; receptor-boot is secondary and not
reported as primary. Block B matches. All CIs quoted in the claim sheet
and dossier are cluster-boot over the 26-cluster paralog map at
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`
(reconstructed 2026-09-09, seed 20260909, 1000 draws). Any tighter
receptor-boot CI in circulation from earlier drafts should be
disregarded in favor of the cluster-boot value.

### Verdict — canonical / variant

**Canonical**: `0.558` (on-corpus reproduction, frame_36 row_mean =
per-receptor midpoint = per-cell midpoint under uniform (5, 10) × 40).

**Documented variant**: `0.552` — pre-consolidation snapshot value. Falls
within the current-corpus 95% CI; is not a rounding of 0.558 but a
different-corpus point estimate. Every dossier/claim-sheet occurrence
of `0.552` is corrected to `0.558` in this pass. Downstream
decomposition math updates:

- Δ_occupancy (apo → decoy) = 0.558 − 0.158 = **0.400** (share ~55%
  of the 0.733 apo→cognate gap on the probability scale).
- Δ_α5CT_sequence (decoy → shuffled) = 0.809 − 0.558 = **0.251**
  (share ~34%).
- Δ_correct_family (shuffled → cognate) = 0.891 − 0.809 = **0.082**
  (share ~11%). Family term unchanged; SC-B-2 not affected.

The 55 / 34 / 11 share breakdown supersedes the dispatch-cited 54 / 35 / 11.

---

## Check 3 — AA2AR's family term (+0.19 vs +0.76 reconciliation)

### Method

Read `experiments/019_block_b_partner_selection/analysis/ladder_per_receptor.csv`
row `receptor=AA2AR`. Family term is `cognate_rate − shuffled_rate` on
the probability scale; logit-scale variant is
`logit(cognate) − logit(shuffled)`.

| backbone | apo | decoy | shuffled | cognate | family_term (prob) | family_term (logit) | ceiling_pinned | floor_pinned |
|---|---:|---:|---:|---:|---:|---:|---|---|
| boltz | 0.020 | 0.000 | 0.040 | 0.800 | **+0.760** | **+4.564** | False | True |
| chai | 0.000 | 0.900 | 1.000 | 1.000 | 0.000 | 0.000 | True | True |
| of3 | 0.000 | 0.560 | 1.000 | 1.000 | 0.000 | 0.000 | True | True |
| protenix | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 | True | True |

Panel mean across 4 backbones = (0.760 + 0.000 + 0.000 + 0.000) / 4 = **+0.190**.

### Reconciliation

**Phase 3 §3f cite `+0.19` = panel mean across 4 backbones.**
**Phase 6a cite `+0.76` = Boltz-only.**

The two numbers are the same underlying data on different aggregations,
not a 4× unexplained swing. Chai / OF3 / Protenix all show
`shuffled = cognate = 1.0` — fully saturated at ceiling on AA2AR — so
their family term is structurally zero. Boltz is the only backbone
where AA2AR's shuffled cell (0.04) remains far below cognate (0.80),
which is precisely the "non-saturation exposes what other cells hide"
pattern C-B-8 already names.

The +0.19 figure understates AA2AR's family-term magnitude at the
per-receptor per-backbone level; the +0.76 figure is the correct
per-cell answer on the one backbone where AA2AR is measurable. Both
are correct on their own aggregation; neither should be quoted without
naming the aggregation.

### Deposition-count degeneracy

Read `ladder_height_covariates.csv`: `deposition_count = 2` for every
one of the 40 receptors. Standard deviation is exactly zero on the
reference-set-based proxy. C-B-14 already flags this in the panel
table ("NaN slope; degenerate proxy") but the caveat introduction
lists four "candidate predictors" as if all four were tested. The
intro is tightened in this pass — see Edits.

### Verdict — RESOLVED and edits made

C-B-8 is amended with an explicit "Reconciliation across aggregations"
section showing the per-backbone table + panel mean. C-B-14 is
tightened to state that three predictors were tested and one
(deposition_count from reference set) was degenerate at scoring time.
No claim-sheet number changes.

---

## Check 4 — W-B-4 is misfiled

Outcome B was pre-registered as one side of a two-outcome test and was
the side that did not sign. That is a signed test result, not a claim
made and retracted.

`withdrawals/W-B-4_outcome_b_reads_partner_identity.md` reads like a
retraction, but the underlying event is: Phase 5 §5.0 pre-registered
Outcomes A and B with equal manuscript-facing status; the test signed
Outcome A on the load-bearing Gs → Gi cell and did not sign Outcome B
anywhere at 95% CI. Neither outcome was believed before the test; only
one turned out to sign. Withdrawals should be reserved for genuine
reversals — claims previously believed that are now retracted.

### Verdict — MOVE

W-B-4's content is moved to the claim sheet as **SC-B-14** — "The
pre-registered Outcome B (model reads partner identity on the continuous
axis) is NOT signed anywhere at 95% CI." Companion signed-side claim is
SC-B-6 (Outcome A). A pointer stub replaces `W-B-4` in
`withdrawals/W-B-4_outcome_b_reads_partner_identity.md` so the W-B
numbering remains auditable (W-B-1..W-B-3, W-B-5, W-B-6 continue to be
withdrawals; W-B-4 is a moved entry). A one-line pointer is also added
to `withdrawals/README.md`.

---

## Edits made in this pass (revised after Check 1 downgrade)

1. **`BLOCK_B_CLAIM_SHEET.md`**:
   - SC-B-1 panel decoy `0.552` → `0.558`.
   - SC-B-6 **REVERTED to Phase 6b wording** ("Outcome A signed, CI
     spans zero on native-only n=20"), plus a post-freeze note
     recording the equivalence-upgrade attempt and why the ruler-side
     bootstrap CI does not survive the strict criterion.
   - Added SC-B-14: pre-registered Outcome B not signed.
2. **`dossiers/BLOCK_B/EXPERIMENT_DOSSIER_BLOCK_B.md`**:
   - Executive summary decoy `0.552` → `0.558`.
   - Phase 3 §3d decomposition math updated (0.400 / 0.251 / 0.082;
     share 55 / 34 / 11).
   - Every remaining `0.552` corrected.
3. **`caveats/C-B-8_aa2ar_standing_anomaly.md`**:
   - "Reconciliation across aggregations" section (per-backbone table).
   - Per-cell note: AA2AR Boltz decoy 0.000 < apo 0.020 — rare
     negative occupancy term; only non-monotonic ladder cell in Block B.
4. **`caveats/C-B-14_no_covariate_slope_excludes_zero.md`**: tightened
   intro to "three predictors testable, one (deposition_count) degenerate
   from the reference set alone"; body unchanged.
5. **`withdrawals/W-B-4_outcome_b_reads_partner_identity.md`**: replaced
   with a pointer stub to SC-B-14.
6. **`withdrawals/README.md`**: added one-line pointer noting W-B-4
   moved to SC-B-14.
7. **This report `docs/BLOCK_B_POSTFREEZE_CHECKS.md`**:
   - Check 1 rewritten (direction correction, ruler bootstrap, Block A
     restriction-of-range reconciliation, Gs-group composition
     limitation, verdict UNDETERMINABLE).
   - Check 2 extended with bootstrap-convention note
     (cluster-boot authoritative per Block A, receptor-boot secondary).

---

## Tag convention

The `block_b_freeze` tag at `d6c1bef` stays where it is — it is on
origin and future readers may already have fetched it; moving it would
be a force-adjacent operation on a pushed ref, which the standing
CLAUDE.md discipline avoids.

**New tag**: `block_b_freeze_r2` on the HEAD after this commit lands.
Rationale: preserves the original tag pointer as an audit trail
(readers can `git diff block_b_freeze..block_b_freeze_r2` to see exactly
what the post-freeze checks changed) rather than silently moving the
pointer. This matches the "audit trail is a first-class deliverable"
pattern the campaign has used elsewhere (pre-scientific-review →
post-review-analysis-batch → block_a_freeze on the release repo).

---

## Stop

The four checks are complete. No further phase is opened. Block B's
remaining work is manuscript writing.
