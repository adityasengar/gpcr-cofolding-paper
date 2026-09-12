# Pre-registration — Block A switch test (draft, not final)

**Status**: DRAFT, not yet final. Complete before Block A dispatch.
**Panel of record**: [`refs/gpcr_coupling.csv`](gpcr_coupling.csv), **48 rows** (40 Class A + 4 Class B + 4 Class F), Class B/F extension landed 2026-09-01 via `scripts/merge_class_bf_into_panel.py --commit`.
**Eligible pool for §12/§14 draws**: [`refs/eligible_pool.csv`](eligible_pool.csv) — 48 rows carrying `excluded` + `exclusion_reason`. Eligible Class A pool = 40 − 6 = **34 receptors** after §1a exclusions (B1B1U5, CNR1, OPRD, OPSD, LSHR, FSHR). Class B/F receptors are marked excluded from A-only draws.
**Reference set**: [`refs/reference_set.csv`](reference_set.csv) — Class B/F rows merged in from `refs/reference_set_class_bf.csv` in the same pass.
**Shuffle arm eligibility**: [`refs/shuffled_arm_status.csv`](shuffled_arm_status.csv) — no longer on the Block A critical path (shuffled + decoy return in Block B on 12 pre-registered receptors, see §12).
**Per-class anchor table**: `refs/anchors_per_class.csv` (Class A convention-locked, Class B/F max-margin-selected, both demoted to reported-secondary; primary mechanics predicate is GPCRdb TM6 tilt per §2c-revised).

The purpose of this document is to nail down every design choice, threshold, statistic, and stratification rule **before any Block A prediction is dispatched**. Anything not in this file is either not decided or a free parameter that can be tuned post hoc.

---

**Tag semantics note (2026-09-01)**: the git tag `block-a-dispatch-2026-09-01` at commit `e54a7f8` was applied before the design settled and points at a PREREG that describes a different manifest (40 Class A only, chai + chai_singleseq arms, non-uniform (m,n)). It is **retroactively renamed in semantics to "scorer-freeze marker only"** — it documents the frozen state of `scorer/` at e54a7f8 and nothing else. A separate parallel tag `scorer-freeze-2026-09-01` is applied to the same commit for clarity. The **actual dispatch tag** for the corrected-manifest campaign will be applied to a subsequent commit AFTER the user approves the summary table.

---

## 0. Fresh campaign, not a reproduction (2026-09-01 framing)

Block A is a **fresh prospective campaign**, not a reproduction of any prior corpus. Prior-corpus numbers — E1 ladder rates, Round 3 verdicts, mn_consensus results, frozen-branch scored rows — are context for design choices only. They are **not baselines to match, not validation targets, and nothing in the Block A analysis compares against them**.

The instrument changed at multiple layers between the prior corpus and this campaign:

- **References**: reference_set.csv is per-receptor (own active + own inactive) rather than shared Class A reference; 8 Class B/F receptors added; construct-audit column populated; ICL3 status columns added.
- **Thresholds**: full-panel calibration (9.08 Å NPxxY-OH, 14.93 Å GPCRdb TM6 tilt) is new to this pass. Prior work used ad-hoc thresholds.
- **Predicate**: single-metric NPxxY-OH + GPCRdb TM6 tilt two-instrument (§2c-revised), replacing the earlier k-of-5 motif composite and R3.50-6.30 CA-CA mechanics.
- **MSA path**: pre-computed cache is on the critical path for all four backbones (§11c). Chai in particular ran single-sequence in all prior work by construction (see §11d).
- **Templates**: OFF across all four backbones (§11b). OF3 previously ran with its default template search on.

Old numbers therefore came from a different instrument and are not comparable. Analysis reports Block A on its own terms — no delta-vs-prior tables, no "improvement" or "regression" framing against earlier scored rows.

The one exception is **methods-level findings** — e.g., "Chai's default was single-sequence in prior work; the correction flipped the DRD2 state call" — which are the reason the campaign is a fresh run rather than an extension. Recorded as reported findings in §11d, not as scientific baselines.

---

## 1. Coupling-class strata (48-receptor panel, 2026-09-01)

Locked prior to any prediction. Panel breakdown after the 2026-09-01 Class B/F extension:

| GPCR class | Primary | Notes |
|---|---:|---|
| **Class A Gs** | 5 (AA2AR, ADRB1, ADRB2, FSHR, LSHR) | See §1a — usable Gs primaries = 2 (ADRB1, ADRB2) |
| **Class A Gi** | 23 | Largest stratum. CNR1 + OPRD reported-secondary (agonist-only active refs, swap to 6N4B / 6PT3 post-Block-A). |
| **Class A Gq** | 10 | |
| **Class A Gt** | 1 (OPSD) | Uses GNAT1 sequence, not the Gαi1 proxy. See §4. |
| **Class A non-mammalian** | 1 (B1B1U5 = JSR1) | Reported-secondary — stratify never pool. See §5. |
| **Class A G12/13 primary** | 0 — untestable as a cognate class in this panel. Present only in secondary for AGTR1, GHSR, LPAR1. |
| **Class B (secretin)** | 4 (GLP1R, GCGR, PTH1R, CRHR1) | All primary Gs. Paired active+inactive with G-protein-coupled active reference. §2c-revised. |
| **Class F** | 4 (SMO, FZD4, FZD6, FZD7) | Individual case studies, no pooled Class F number. Three transducer mechanisms across four receptors (§2c-revised). **FZD4 — apo only in Block A; DVL2 substitution deferred as Block-A-post follow-up. FZD6 alphas_XLas → alphas is fine (α5-CT identical to canonical alphas).** |
| **Class C** | 0 — excluded | Dimer-interface activation mechanism uninterpretable on a monomeric construct. |

**Panel total: 48 receptors.** Class A primary result rides on the 40-receptor Class A stratum minus reported-secondary receptors (JSR1, CNR1, OPRD) = 37 receptors. Class B and Class F are reported per-class (B) or per-receptor (F).

### 1a. Usable Gs stratum is effectively 2

Of the 5 Gs-primary receptors:
- **FSHR** and **LSHR** — **pre-registered apo failures**. See `refs/pathology_receptors.md` (to be written) — these were flagged in the M2.x pipeline for structural pathology in the apo/inactive reference and their d_tm6 delta will not be interpretable.
- **AA2AR** — Boltz anomaly documented in `experiments/mn_consensus/README.md` and `ROUND3_REPORT.md`; Round 3 confirmed the samples-winner claim for Protenix on AA2AR was N=5 noise, but Boltz-specific behaviors on this receptor remain unresolved.
- **ADRB1**, **ADRB2** — the two "clean" Gs receptors, maximally represented in the PDB. **Any Gs-specific claim in Block A rests on these two.**

Consequence: report Gs-specific results with n=2 receptors explicitly. Do not average Gs summary statistics across five receptors as if all are equally usable.

## 2. Success definition — two instruments

Class A: **motif-metric composite**. Class B/F: **paired-reference midpoint crossing** (after Step 5 delivers those references and per-class anchors).

### 2a. Class A motif metrics (all 40, regardless of reference-coverage tier)

Five metrics, all in the current scorer schema:

1. **NPxxY packing** — `d_npxxy_y558_y753` — computed both as CA–CA (existing column) **and OH–OH** (new column, added before dispatch). Literature threshold is on OH–OH at ~7-8 Å; the CA–CA column at ~14.5 Å cannot carry a literature-derived threshold. Both columns emitted from the same run.
2. **Y5.58 packing** — `d_y558_pack_min_heavy` — min heavy-atom distance from Y5.58 to nearest packing partner.
3. **DRY ionic-lock breakage** — `d_dry_sidechain_r350cz_e630oe1` — R3.50 CZ to E6.30 OE1 distance; broken lock ⇔ active state.
4. **TM5 outward** — `d_tm5_outward_r350_r558_ca`.
5. **ICL2 helicity** — `icl2_helical_frac`.

**Combination rule** (locked, no post hoc tuning):

> A prediction is called **active-like** iff **≥ 3 of the 5 metrics** cross their pre-registered threshold in the active direction, AND **`confidence_flag` != "low"**.

*Justification for k-of-n:* AND is too fragile against a single-metric NaN/low-confidence outlier; OR is trivially permissive. 3/5 with an explicit confidence gate is the minimum defensible middle.

**Unmeasurable-metric behaviour** (locked):

> If a metric is NaN (residue-not-resolved / template-broken / ligand-occlusion), the prediction is counted against the ≥3-of-5 threshold as if the metric had failed — never treated as pass-by-default. If ≥ 2 of 5 metrics are NaN, the prediction is dropped with `metric_coverage_insufficient` and excluded from the receptor's numerator and denominator both.

### 2b. Per-metric threshold sources — panel calibration complete + composite VALIDATED (2026-09-01)

All six metric refs derived from tier-1 crystals; thresholds in `refs/thresholds_panel.csv`. **Full validation pass documented in `docs/BLOCK_A_STEP3_VALIDATION_2026_09_01.md`** — 4×4 Pearson matrix + self-classification accuracy on 80 tier-1 rows. Findings restructured the composite:

| Metric | Threshold | Direction | n | Separation | Self-class accuracy | In composite? |
|---|---:|---|---:|---:|---:|:---:|
| DRY ionic lock | 11.54 Å | active_gt | 38 | +10.05 Å | 92.1% | ❌ **dropped** (r=+0.913 with d_tm6 — not independent) |
| **NPxxY OH–OH** | **9.08 Å** | **active_lt** | **70** | **+7.59 Å** | **94.3%** | ✅ **primary motif** |
| Y5.58 pack | 4.37 Å | active_lt | 76 | +1.87 Å | 71.1% | ❌ dropped (r=+0.784 with NPxxY-OH, 17/37 inactive false positives) |
| NPxxY CA–CA | 16.57 Å | active_lt | 80 | +4.00 Å | – | ❌ secondary QA only (redundant with OH-OH) |
| TM5 outward | 8.59 Å | active_gt | 80 | −0.07 Å | – | ❌ dropped (flat) |
| ICL2 helicity | 0.402 | active_gt | 80 | −0.018 | – | ❌ dropped (inverted) |

**Motif composite (final)**: **single-metric NPxxY-OH**. K_OF_N = 1, MAX_MISSING = 0. Receptors with non-Tyr at 5.58 or 7.53 (EDNRA, EDNRB, GRPR, HRH3, plus 6 others where OH is truncated in the crystal) drop with `metric_coverage_insufficient` and fall back to midpoint-crossing on `d_tm6_r350_r630_ca` as the sole active-call.

**Why not a 2-metric composite?** — All motif-metric pairs are collinear (Pearson r 0.463-0.913). No independent second axis available among the current metrics. Adding A100 index / GPCRdb TM6 tilt / Class B kink (item 2) as scorer columns will let a future re-derivation revisit the composite; for Block A dispatch, single-metric NPxxY-OH + midpoint-crossing d_tm6 is the two-instrument design.

**DRY, Y5.58-pack, NPxxY-CA, TM5-out, ICL2-helicity are all still emitted** as reported diagnostic columns. Do not fold them into the success predicate.

**Cross-instrument correlation** (motif vs midpoint): NPxxY-OH vs d_tm6 r = −0.681 across 70 rows — different enough to carry non-redundant signal.

Threshold-authoritative CSV: `refs/thresholds_panel.csv`. Code: `scorer/switch_signal.py::MotifThresholds` (updated 2026-09-01 with single-metric collapse).

**Why TM5-out and ICL2 helicity are dropped**:
- Both are project-specific proxies with no literature backing (`refs/thresholds_sourced.md`).
- Panel means show ~0 separation — the metrics do not discriminate active from inactive on the tier-1 crystal set.
- ICL2 helicity is fractionally *inverted* on this panel (inactive slightly more helical) — sign-mismatched to the biology.
- Reporting them anyway would either force k-of-5 = k-of-3 (mostly noise contributing) or bias the composite. Cleanest to drop.

**Why NPxxY CA-CA is secondary**: same active/inactive direction as OH-OH but with 2× less separation (+4.0 vs +7.6 Å). Not redundant enough to drop, not strong enough to add to the composite. Reported for QA — cross-check for OH-OH.

**DRY caveat (locked)**: DRY only fires on 19/40 receptors (those with E/D at 6.30). On the other 21, DRY is NaN. Under `MAX_MISSING = 1` in the k-of-n rule, a NaN-DRY is treated permissively — it does not count as a fail toward the k-of-2 quorum — so DRY-NaN receptors can still be called active-like on NPxxY OH + Y5.58 pack alone.

**Two-axis framing vindicated on Block A (2026-09-02 update).** The (m,n) corpus agreement between NPxxY-OH and GPCRdb TM6 tilt was 99.9 % (one disagreement of 950), which suggested collapsing to a coherence check. Under Block A's cognate-vs-apo variation the second instrument carries independent information: on the 32 Class A threshold-derivation receptors (sealed 8 excluded), **5,995 prediction rows have both metrics non-NaN, 90.5 % agree on active/inactive call (5,423 / 5,995), 572 disagree, Pearson r = −0.738 between the two axes**. Verified 2026-09-02 by direct recomputation on `experiments/018_block_a_switch_test/analysis/rows.csv`. The two-instrument design is defensible for the paper — do not collapse. See `docs/campaign_completion_report.md` → "Confirmed findings" for the breakdown.

Threshold-authoritative CSV: `refs/thresholds_panel.csv`. Code: `scorer/switch_signal.py::MotifThresholds` (updated 2026-09-01).

### 2c. Class B/F midpoint crossing — extended panel discovered (2026-09-01)

Step 5 discovery landed **8 tier-1 non-Class-A receptors** with own paired active/inactive structures:

| Class | Receptors (tier-1) | Cognate transducer | Anchor pair | Separation |
|---|---|---|---|---:|
| **B (Wootten numbering)** | GLP1R, GCGR, PTH1R, CRHR1 | Gαs (all four) | **3.50 — 6.34** | **+9.59 Å** |
| **F (GPCRdb-F numbering)** | FZD4, FZD6, FZD7, SMO | Dishevelled DEP domain (FZD4), atypical Gs (FZD6/7), Gs (SMO) | **3.50 — 6.31** | **+1.80 Å** |

Anchor derivation is empirical: for each class, the pair whose CA-CA distance most consistently separates active from inactive across paired members. Class A's 3.50 — 6.30 is convention-locked and included in `refs/anchors_per_class.csv` for consistency.

Per-class midpoint-crossing success rule (final):
1. Anchor pair chosen once per class from `refs/anchors_per_class.csv`.
2. Midpoint = (d_active_ref + d_inactive_ref) / 2 from that receptor's own crystals.
3. Prediction called **active-like** iff d_prediction > midpoint AND `confidence_flag != "low"`.

**Two-instrument summary**: Class A success rides on motif metrics (biology-derived, 3-metric composite). Class B/F success rides on midpoint crossing (crystallography-derived, per-class anchors). §3 below tests their agreement on tier-1 Class A where both are computable.

**Class F caveat (recorded)**: FZD4's active reference (8WM9) is Dishevelled-DEP-stabilized, not Gα-stabilized. `active_stabilization_source` vocabulary extended to include `DVL_DEP` for this receptor. FZD6/FZD7 active-state Gs coupling is structurally documented but non-canonical relative to standard Wnt/DVL signaling — marked `coupling_evidence = curator_call`.

**Excluded from Step 5 (recorded)**: GIPR, SCTR, VIPR1, VIPR2, PAC1R, CALCR (Class B — no inactive full-length TM crystal); FZD5 (no active partner). Class C explicitly not searched per §5 (dimer-interface activation mechanism).

**Extended panel merge policy**: Class B/F receptors land in `refs/reference_set_class_bf.csv` and `refs/gpcr_coupling_class_bf.csv` (agent output). Merge into the primary panel files requires coordinator decision (`scripts/merge_class_bf_into_panel.py --emit → --commit`).

### 2c-revised (2026-09-01 update)

**Class B/F primary anchor switches to GPCRdb TM6 tilt (2x46 CA – 6x37 CA)** — externally validated cross-class measure per GPCRdb's own activation-classifier docs, replacing the empirically max-margin-selected pairs (3.50/6.34 for B, 3.50/6.31 for F). The max-margin pairs were derived from C(9,2)=36 and C(7,2)=21 candidate pairs on n=4 receptors per class — **overfit by construction**. Both landed pairs demoted to reported-secondary in `refs/anchors_per_class.csv`.

**Implementation status (2026-09-01)**: LANDED (commit `f71a20a`). All three externally-validated metrics + supporting BW anchors added to the scorer as emit-only columns. `ANCHOR_KEYS` extended with 14 new BW labels (2.46, 6.37, 1.53, 7.55, 2.50, 3.37, 3.42, 4.42, 5.66, 6.58, 7.35, 6.39, 6.50, 6.54). New axis functions in `scorer/axes.py`. Reference derivation script `scripts/derive_lit_metric_refs.py`. Test suite 332 → 354 (+22).

**Panel-derived thresholds and self-classification accuracy** (from `refs/thresholds_panel.csv`):

| Metric | Threshold | Self-classification | Correlation vs NPxxY-OH | Correlation vs d_tm6 |
|---|---:|---:|---:|---:|
| **GPCRdb TM6 tilt (2.46-6.37 CA)** | **14.93 Å** | **98.8 % (79/80)** | −0.669 | +0.888 |
| A100 index (Ibrahim et al. 2019, DOI 10.1021/acs.jcim.9b00604) | 12.84 | 88.7 % | −0.621 | +0.719 |
| Class B TM6 kink (6.39-6.50-6.54 angle) | 159.95° | 76.2 % on Class A panel | −0.514 | +0.578 |

**Predicate decision** (LOCKED 2026-09-01 following user review of Step 3 validation):

- **Motif instrument**: NPxxY-OH single-metric (unchanged). Threshold **9.08 Å**, active < threshold. Self-classification 94.3 %.
- **Mechanics instrument**: **`d_gpcrdb_tm6_tilt_246_637_ca` REPLACES `d_tm6_r350_r630_ca`** as of user approval this pass. Threshold **14.93 Å**, active > threshold. Self-classification 98.8 %.
- **All other metrics** (d_tm6, d_dry, d_y558_pack, d_npxxy_ca, d_tm5_out, icl2_helical, a100_index, class_b_kink) are emitted as reported-diagnostic columns; NOT in the predicate. Analysts consult them separately.

**Rationale for the swap** (user-approved 2026-09-01, ordered by defensibility):

1. **Externally validated**. GPCRdb TM6 tilt (2x46 CA – 6x37 CA) is GPCRdb's own published activation-classifier measure for cross-class use. Not a max-margin pair we selected on our own panel.
2. **Cross-class applicability**. Works on Class A / B / C. `d_tm6_r350_r630_ca` (R3.50-6.30 CA) is Class A-only — 6.30 is not a canonical anchor in Class B/F and the DRY motif doesn't exist in Class B1. Block A intentionally includes Class B/F receptors; requires a metric defined for them.
3. **Independent enough of the motif instrument**. Pearson r = −0.669 with NPxxY-OH across 70 tier-1 rows — under |r| < 0.7 threshold for treating two metrics as distinct axes. Preserves the two-instrument design (motif chemistry vs mechanics).

**Self-classification figures reported as descriptive, not held-out**:

The 98.8% figure (79/80) is derivation-set accuracy — same 80 rows the threshold was derived from. It was chosen as the max across ~8 candidate metrics, so it is selection-on-noise on n=80 (79/80 vs 75/80 is 4 structures). Do not treat as held-out predictive accuracy. Reported as one line of the panel-calibration table; not load-bearing for the swap decision. Held-out validation across new (non-tier-1) receptors will follow when the panel extends.

**Follow-ups triggered by the swap**:
1. **Rescore existing mn_consensus predictions** with the new scorer (populates all 3 new metric columns on the ~1,319 pre-existing rows). Delegated to agent post-swap.
2. **Re-run Step 3 cross-validation** with NPxxY-OH-motif vs GPCRdb-tilt-mechanics. Expected to show agreement ≥ current NPxxY-OH-vs-d_tm6 agreement (both metrics stronger individually).
3. **A100 index and Class B TM6 kink** stay reported-diagnostic. A100 below the 94 % bar on our panel (88.7 %). Class B kink is Class B-specific and the current panel is majority Class A; its 76 % is expected and non-informative. Both stay in scorer output for the 8 Class B/F tier-1 receptors (Block A extension).

**Class F reduced to SMO only for primary result**. FZD4 uses Dishevelled DEP not Gα, FZD6/7 use atypical Gs (curator-called), SMO uses Gi — three transducer mechanisms across four receptors cannot share a derived anchor. GPCRdb itself uses a different TM6 measure for Class F. FZD4/6/7 stay in `refs/reference_set_class_bf.csv` unmerged for now; reported as case studies alongside SMO.

**Class B TM6 kink angle** (Kobayashi et al., *Nature* 2023): Cα angle at 6.39 / G6.50 / 6.54, sharp ~90° = active, moderate ~145° = moderate. NPxxY and DRY don't exist in Class B1 (PxxG motif drives the kink instead). To be implemented as a scorer column before dispatch (item 2). This is Class B's real activation switch.

**Class B apo arm is a pre-registered EXPECTED failure**. Hilger et al., *Science* 2020: for GCGR, agonist binding alone does NOT induce TM6 outward movement — both agonist AND G protein are required, due to the barrier to forming the kinked, partially unwound TM6. Class B apo failure is **correct biology**, not model failure. Pre-registered here to prevent reading model-good biology as model-bad prediction.

**Prior art (record)**: bioRxiv 2026.03.26.714415 reports independently from experimental structures that a stable active state is established only on G protein binding, agonist alone being insufficient. Corroborates the Phase 4 ligand-blindness result.

### Block A hypothesis (from Chai MSA pilot + DRD2 forensics, 2026-09-01)

*Chai + MSA-server on DRD2 (Gαi1 + dopamine, seeds=5, samples=5) shifts the TM6 population from active-like to inactive-crystal-like. The shift is confirmed on two independent TM6 markers: `d_tm6_r350_r630_ca` (mean 14.11 → 8.41 Å; receptor midpoint 11.83) and `d_gpcrdb_tm6_tilt_246_637_ca` (mean 16.71 → 11.78 Å; receptor midpoint 14.52; panel threshold 14.93). Both modes use identical full-length human DRD2 (P14416, 443 aa, SHA256 `8c2b6e14…cefd3e0`); the pLDDT at BW 3.50 and 6.30 is 65-80 on every MSA-mode row and all six A-gates pass. The apparent excursion of MSA-mode d_tm6 (8.41 Å) below the 6CM4 inactive-ref value (8.74 Å) is __inside__ the within-mode std (0.78 Å) and is compounded by an ICL3 length mismatch: both reference crystals (7JVR active, 6CM4 inactive) excise or omit DRD2 residues ~223-362 (~140 aa ICL3), while the prediction models them explicitly. Tilt disagrees marginally (11.78 sits just above 11.45 inactive-ref), supporting an "inactive-crystal-like" call rather than a "past-inactive" call.*

**Wave-1 test**: predictions on the 40-receptor panel should distinguish four alternatives:
1. **Generalizes across Class A Gi/Go** — MSA-induced inactive-collapse affects the Gi/Go coupling class broadly (23 Gi + 1 Gt receptors on the panel).
2. **Idiosyncratic to DRD2's long ICL3** — the receptor's ICL3 length in the input sequence drives the collapse.
3. **Chai-specific** — Boltz + OF3 + Protenix on the same DRD2 input do not show the collapse.
4. **Tracks ICL3 excision in the reference, not in the receptor input** — the effect is proportional to how much of ICL3 the receptor's own inactive reference crystal excises (T4L/BRIL/rubredoxin fusion or unresolved-loop excision), regardless of what the input sequence models.

The Item-1 panel ICL3 audit landed 2026-09-01 (commit `a765c04`, `docs/BLOCK_A_ICL3_AUDIT_2026_09_01.md`): **panel is heavily affected but the effect could not be surfaced at n=3.**

- **72.5% of inactive references have ICL3 residues missing** (29/40); majority via BRIL or T4L fusion.
- **Task B correlation**: Spearman r = −1.0 on d_tm6, −0.5 on tilt across the 3 receptors with landed mn_consensus predictions (AA2AR, ADRB2, DRD2). |r|=1.0 crosses effect-size but not significance (permutation p = 0.333 minimum at n=3). Null result on this sample size.
- **9 receptors have >50 ICL3 residues missing in the inactive reference**, 8 of them ALSO in the active reference (double confound): HRH1 (175), ACM2/ACM4 (152), DRD2 (135), ACM1 (128), HRH3 (105), DRD3 (91), 5HT1B (58), CCKAR (55). Aminergic + muscarinic subfamily dominates.
- **Task C recommendation adopted**: predict full-length ICL3 in Block A. Flag these 9 receptors — their prediction-vs-inactive-reference residuals must be interpreted at ≥ ±0.5 Å tolerance.
- Wave-1 will re-run the Spearman test at n ≈ 40, at which point the panel-scale ICL3 vs residual correlation gets a real hypothesis test.

**Manifest parameter locked**: model ICL3 full-length. New columns `icl3_status`, `icl3_residues_missing`, `icl3_residues_missing_count`, `fusion_partner`, `fusion_partner_insertion_range` in `refs/reference_set.csv`.

**AA2AR/ADRB2 result** (Section D of the forensics doc): MSA vs single-sequence Chai gives identical active-like calls on both axes. 100/100 predictions active in both modes on both metrics. **Not a Block-A signal** — do not pre-register as a hypothesis about backbone limitation.

Forensics detail: `docs/BLOCK_A_DRD2_MSA_FORENSICS_2026_09_01.md` (commit `fea188b`).

## 3. Primary panel result — Δd_tm6(cognate − apo)

**Definition (locked)**:

For each (receptor r, backbone b):
- Let `S_cognate(r, b)` = set of predictions in the cognate-Gα arm for (r, b), one prediction per seed × sample.
- Let `S_apo(r, b)` = set of predictions in the apo arm for (r, b), one prediction per seed × sample.
- Aggregate each arm to a **per-seed mean** first (variance-of-variance safe), then compute `Δ = mean_seed(cognate) − mean_seed(apo)`.
- **Seed is the unit of variance.** Report CI via bootstrap over seeds, not over rows.

**Not done**: pairwise row-by-row subtraction across arms. Seeds are not matched between arms; subtracting individual rows would fabricate pairing.

**Report**: Δd_tm6 per (r, b); per-backbone mean-of-Δ across receptors, stratified by coupling class (Gs / Gi / Gq / Gt); confidence intervals; effect size vs 0.

## 4. Gαt vs Gαi1 substitution (OPSD)

**Change 2026-09-01**: OPSD's `primary_ga_identity` in `refs/gpcr_coupling.csv` switched from `alphai1` (proxy) to `alphat` (real transducin GNAT1, UniProt P11488).

**Required before Block A dispatch**:
1. Add GNAT1_HUMAN sequence to `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` under header `alphat|classification=partner|length=~350|category=Gα`.
2. Emit an α5-CT diff report: sequence alignment of the C-terminal 21 residues of GNAT1 vs GNAI1 (P63096), position-by-position, with substitution positions annotated against the L15/E19/L21 "chemistry-claim" residues (the α5-CT positions the mechanism-level claim depends on).
3. Record diff magnitude in this file, with sensitivity on OPSD-specific Δd_tm6 to the alphat-vs-alphai1 substitution.

**Until (1)–(3) are done, OPSD is dispatch-blocked.** No Block A prediction for OPSD may be dispatched with the Gαi1 proxy.

## 5. B1B1U5 = JSR1 (jumping spider rhodopsin-1) — non-mammalian singleton

**Resolution 2026-09-01**: B1B1U5 resolves to *Hasarius adansoni* rhodopsin-1 (JSR1), gene HaRh1. Inactive reference = 6I9K (Varma et al., PNAS 2019 — dark-state crystal). Active reference = **9EPR** (Tejero et al., *Nat Commun* 2024 — **native** Gi heterotrimer, NOT 9EPP/9EPQ which are Gi/q chimeras and would mis-assign coupling via UniProt-accession lookup).

**Stratification rule (locked)**: JSR1 is the **only non-mammalian receptor in the panel**. Aggregate statistics MUST be reported stratified — never pool JSR1 into a mammalian-panel headline. Bistable opsin: primary coupling Gi (per reference), secondary Gq (invertebrate visual phototransduction canonical).

## 6. Chimeric-construct hazard (panel-wide)

**Rule (locked)**: `active_stabilization_source` in `refs/reference_set.csv` is a controlled vocabulary — `{native, mini_G, chimera, nanobody, agonist_only}` — **curated from PDB entry text**, never inferred from UniProt Gα accession alone. Where `chimera`, `alpha5_donor_class` names the parent whose α5 C-terminus is grafted.

**Rationale**: Gi/q chimeras (e.g., 9EPQ) carry a Gαi1 scaffold but Gαq α5 C-terminus. Their PDBe/SIFTS-derived UniProt map returns P63096 (GNAI1), and a naive "look up the Gα UniProt" pipeline would mis-assign coupling. Since α5-CT positions are the same residues the mechanism claim rests on, this is not a labelling nit — the segment we're claiming to characterize is the segment being mis-labelled.

**Audit** (Step 1): every active reference in `refs/reference_set.csv` inspected against PDB entry text for construct type; results populate `active_stabilization_source` and `alpha5_donor_class`. Receptors whose current coupling assignment came from a chimeric-scaffold reference are re-evaluated.

## 7. Shuffled arm — eligibility

Locked per `refs/shuffled_arm_status.csv`. Summary:

| Status | Count | Receptors |
|---|---:|---|
| eligible | 39 | 4-way shuffle available (Gs↔Gi↔Gq↔G12 as needed to escape primary+secondary coverage) |
| g12_fallback | 1 | EDNRA (primary Gq, secondary Gs+Gi → must use G12) |
| exempt | 0 | |

**Rule**: for EDNRA, the shuffled arm uses G12 as the "not-in-known-coupling" decoy. **Record + stratify**: if positives-in-shuffle correlate with G12-fallback receptors, the arm is partly testing G12 specifically, not partner discrimination.

## 8. Coupling-evidence provenance

Locked per `refs/gpcr_coupling.csv` column `coupling_evidence` ∈ `{primary_reference, assayed_no_coupling, not_assayed, curator_call}`.

**Rule**: a shuffled-arm draw against an `assayed_no_coupling` class is a valid negative control. A shuffled-arm draw against a `not_assayed` class **may be a real secondary partner** — a positive there is correct biology, NOT a control failure. This must be treated in analysis: `not_assayed` shuffle results are reported as "informative but ambiguous".

## 9. Design geometry (Block A run manifest)

**Block A dispatches 2 arms** (cognate + apo). Shuffled and decoy return in Block B on 12 pre-registered receptors (§12).

Arms in Block A:
1. **cognate** — receptor + primary Gα per coupling table (Gs → alphas, Gi → alphai1, Gq → alphaq, Gt → alphat). **FZD4 is apo-only in Block A** (DVL2 transducer, not Gα; substituting alphas as proxy is the W54 taxonomy failure at n=1 — deferred as Block-A-post follow-up).
2. **apo** — receptor alone (no partner).

Arms deferred to Block B (registered here for provenance, dispatched later on the §12 12-receptor subset):
3. **shuffled** — receptor + a non-primary, non-secondary Gα class (per `refs/shuffled_arm_status.csv`).
4. **decoy** — receptor + `random_helix_40mer` or `gcn4_leucine_zipper_33` (structurally-plausible non-Gα helix).

*(An earlier design referenced a fifth "α5-peptide" arm. That arm is NOT in the current 4-arm design. If added, it enters here explicitly, with a defined peptide sequence and a pre-registered interpretation rule.)*

**K, N**: **locked at (5, 5) uniform across all four backbones** 2026-09-01 (user decision, this pass). Rationale: 5 seeds is the bootstrap-CI floor (`scorer/switch_signal.py::delta_d_tm6_per_cell` requires ≥ 2 seeds; 5 gives usable CI width). 5 samples per seed captures backbone diffusion diversity. Total = 25 predictions per (receptor, arm, backbone) cell.

**OF3 seed-std ≈ 0.006 Å (effectively deterministic across seeds)** — measured on the (m,n) consensus panel. The (m,n) study's own OF3 recommendation was (1, 5) — one seed, five samples. **Uniform (5, 5) is chosen over (1, 5) for OF3 to preserve cross-backbone comparability**: same manifest cell shape, same bootstrap CI mechanics, same n at every analysis step. Trade-off recorded explicitly here.

**Consequence — OF3's per-cell CI will be near zero**. That is low seed variance, not false precision. Any analysis reader tempted to read "OF3 CI = 0" as an artifact should recognise it as measured OF3 stochasticity: the model's seed-to-seed variability is roughly two orders of magnitude smaller than Boltz's or Chai's on the same metric. Flagged here so a near-zero interval is interpreted correctly.

## 10. Partner-interface metrics (dispatch-blocking scorer addition)

Three metrics **must be in the scorer output** before Block A dispatch — otherwise the shuffled / decoy arms are ambiguous between "partner rejected" and "partner mis-docked":

1. `d_ga_alpha5_r350_ca` — distance from Gα α5 C-terminal residue (CA) to receptor R3.50 CA.
2. `n_interface_contacts_ga_receptor` — count of Gα residues within 5 Å heavy-atom of receptor TM3/TM5/TM6.
3. `plddt_ga_alpha5` — mean pLDDT over Gα α5-helix residues.

Missing any of these makes the shuffled / decoy arm outcomes non-diagnostic.

## 11. Per-backbone inference parameters (pre-registered)

Every non-default parameter that materially affects inference is locked here — no launcher default counts as an implicit design choice. Rows also lock the MSA source (all four backbones feed from a pre-computed cache, no live server dependence) and the template-usage flag (see §11b — templates locked OFF across all four backbones).

| Backbone | Version | Seeds × Samples | Recycles | Diffusion steps | Templates | MSA source |
|---|---|---:|---:|---:|---|---|
| **Boltz-2** | 2.2.1 | **5 × 5** | 3 | **200** *(sampling_steps, upstream default)* | **off** | pre-warmed ColabFold public API |
| **Protenix v2** | 2.0.0 | **5 × 5** | 3 *(cycle)* | **50** *(step)* | **off** | pre-warmed ColabFold public API (mode: `protenix`), own server |
| **OpenFold-3** | preview p2-155k | **5 × 5** | model default | model default *(`num-diffusion-samples` unchanged)* | **off** *(`--use-templates false` via `qsub/colabfold_shim.py of3`)* | pre-warmed ColabFold public API via shim |
| **Chai-1** | 0.6.1 | **5 × 5** | 3 *(trunk-recycles)* | **50** *(diffn-timesteps)* | **off** *(upstream default `use_templates_server=False`)* | local `.aligned.pqt` cache (`--msa-directory` via `CHAI_MSA_DIRECTORY`) |

Where `Seeds × Samples` is §9's locked (5, 5) design (K seeds × N samples/seed). Uniform across all four backbones for cross-backbone comparability; OF3's near-zero per-cell CI is expected (see §9).

**`chai_singleseq` arm considered and dropped before dispatch (2026-09-01).** An earlier design ran both `chai` (MSA) and `chai_singleseq` (no MSA) as parallel arms at (5, 5) to probe MSA-presence as a design factor. **Dropped**: MSA-presence-as-a-factor crossed with only one of four backbones invites the question of why not all four; a 4×2 backbone × MSA-presence factorial is a different study, not a cross-backbone comparison. Block A instead pins all four backbones to their MSA-enabled configuration and asks a clean cross-backbone question. The MSA-vs-no-MSA question is answered as a **methods finding on Chai alone** (§11d), not as a Block-A arm.

**Surviving `chai` arm caveat (retained):** the (5, 5) numbers for Chai were derived under the single-sequence regime in the (m,n) consensus study — not re-derived after the MSA integration landed. An MSA-mode (m,n) re-derivation is a **post-Block-A follow-up (task #89)**; if it lands materially different from (5, 5), a re-dispatch of the Chai arm becomes an option. Not fatal for the primary Δd_tm6 result: samples-vs-seeds axis was chosen where diffusion diversity was the dominant variance source, and MSA conditioning is not expected to invert that ranking within a factor of two.

### 11a. Boltz `sampling_steps = 200` — upstream default + empirical A/B (LOCKED 2026-09-01, revised)

Boltz-2 upstream default in `boltz/main.py:1051` is `sampling_steps: int = 200`. Our launcher `qsub/rerun_boltz.sh` runs the upstream default explicitly (rather than dropping the flag) so the value is greppable in the launcher and pinned against a future upstream change.

**Empirical A/B on AA2AR cognate (2026-09-01).** Independent quick-validation dispatch (`experiments/timing_boltz_50_vs_200_ab_2026_09_01/`, `docs/BOLTZ_SAMPLING_STEPS_AB_2026_09_01.md` — commit 9763a68): AA2AR + Gαs + NECA, MSA-server on, 3 seeds × 5 samples × 2 configs = 30 predictions, seeds shared across configs for paired analysis. All 30 scored under the frozen scorer with zero failures.

| metric | Δmean (200−50), Å | ~95% CI (paired-seed t, n=3) | verdict |
|---|---|---|---|
| `d_gpcrdb_tm6_tilt_246_637_ca` | +0.146 | [−0.181, +0.474] | within noise |
| `d_tm6_r350_r630_ca`           | +0.491 | [−0.835, +1.818] | within noise |
| `d_npxxy_y558_y753_oh`         | −0.043 | [−0.457, +0.370] | within noise |

Mean position of every scored activation axis is equivalent within noise between the two configs; 0 lies inside every paired-seed 95% CI. One 50-step sample (seed 22374063, model 4) drops to 11.83 Å on `d_tm6_r350_r630_ca` vs the 200-step range 17.93–18.59 Å — a tail-variance observation that does not shift the mean or flip the state call.

**Decision: `qsub/rerun_boltz.sh` runs `--sampling_steps 200` (Boltz-2 upstream default) for the campaign.** Chosen over 50 for the tighter tail on `d_tm6_r350_r630_ca` and to keep the methods sentence at "Boltz-2 with default settings." Wall time is identical (MSA-bound: 90.7 vs 91.3 s per 5-sample job on H100 in the A/B). DRD2 wave-1 Boltz outputs originally run at 50 steps were quarantined to `/hpc/scratch/sengaad1/paper_af3/quarantine/drd2_boltz_50step_2026_09_01/` and re-dispatched at 200 steps before rescore.

### 11b. Templates — disabled for all four backbones (LOCKED 2026-09-01)

All four backbones run **without templates** at Block-A dispatch settings. The prospectivity claim of the paper — de novo prediction of a conformational state absent a reference structure — makes template-based inference a hard disqualifier, not merely a comparability issue:

- OpenFold-3's default template search fetches from `data.rcsb.org/graphql` at inference time (verified 2026-09-01 HTTP diagnostic). For any receptor whose Gs-bound active structure is in the PDB, "predicted the active state" would reduce to "retrieved it." That result cannot support a prospectivity claim, even in a separately-reported column.
- Boltz's audit description ("input-driven — loops `target.templates.items()`, empty for us") means templates are off *because nothing populates the field*, not because they are disabled. Same effective state, but a change to the input generator could silently turn them on. Locked here explicitly so any regression is caught.
- Protenix defaults `use_templates=False` in the model config.
- Chai defaults `use_templates_server: bool = False`.

**Locked defaults:**

| Backbone | Flag / mechanism to disable templates |
|---|---|
| Boltz-2 | Input YAML `sequences[*].protein.templates` field never populated by our propose emitter. |
| Protenix v2 | Upstream default `use_templates=False`; not overridden by our qsub. |
| OpenFold-3 | `--use-templates false` on `run_openfold predict` (via `qsub/colabfold_shim.py of3 predict`). |
| Chai-1 | Upstream default `use_templates_server=False`; not overridden by our qsub. |

**OF3 accuracy trade-off:** deliberately accepted. Templates typically add a few pLDDT points on well-covered targets; the loss is the cost of the prospectivity claim. Any subsequent analysis MUST not restore templates for OF3 on this panel without a fresh PREREG entry.

**Gate coverage:** `of3_launcher_uses_shim` already asserts the launcher routes through the shim. A separate `manifest_no_templates` check (added 2026-09-01) inspects the generated Block A manifest to assert no per-chain / per-entity template field is populated for any backbone.

### 11c. MSA source — locked

All four backbones feed from a pre-computed MSA cache. No live ColabFold fetch is on the critical path:

- **Chai**: reads `/hpc/scratch/sengaad1/paper_af3/msa_cache/chai/{sha256(seq)}.aligned.pqt` via `--msa-directory`. 69/69 files present. Silent single-seq fallback gated by `chai_aligned_pqt` + `chai_launcher_uses_cache` + `chai_launcher_no_server` (step7_dispatch_gate).
- **Boltz + OF3 + Protenix**: ColabFold public-API cache is pre-warmed (67/67 required sequences returned `status=COMPLETE` immediately on 2026-09-01 diagnostic). OF3 additionally routes through `qsub/colabfold_shim.py` to enforce a `(connect=30, read=600)` timeout floor on every `api.colabfold.com` request — mitigates the hardcoded `timeout=6.02` ReadTimeout bug that surfaced in the post-warm timing (91 retries on one prediction). Gated by `of3_launcher_uses_shim` + `of3_launcher_no_direct`.

If any receptor's ColabFold API cache expires mid-campaign, the fallback is fresh live fetch under the shim's expanded timeout — slow but never a silent single-seq degradation the way chai fails.

### 11d. Chai MSA-mode correction — methods finding (2026-09-01)

Chai-1 ran **single-sequence in all prior work** on this project — not by explicit design, but because the default `--msa-directory` path was not wired into the launcher and the `--use-msa-server` flag was never set. The failure mode was silent: chai-lab 0.6.1 does not raise when no MSA is provided; it prints `"No MSA found for sequence"` at INFO and falls back to single-sequence. On a DRD2 pilot re-run with the `.aligned.pqt` cache correctly wired in via `CHAI_MSA_DIRECTORY`, the MSA-mode Chai prediction **flipped the state call**: the TM6 population shifted from active-like (mean d_tm6 14.11 Å, tilt 16.71 Å) toward inactive-crystal-like (mean d_tm6 8.41 Å, tilt 11.78 Å), on identical DRD2 input and seed range. Full forensics: `docs/CHAI_MSA_CACHE_VERIFY_2026_09_01.md`, `docs/BLOCK_A_CHAI_MSA_COMPARISON_2026_09_01.md`, `docs/BLOCK_A_DRD2_MSA_FORENSICS_2026_09_01.md`, audit trail #9.

**Consequence for Block A**: the surviving `chai` arm dispatches under the corrected MSA-mode path (§11c). **The prior Chai corpus is not comparable to the other three backbones** — its input regime was different at inference-time and unknowingly so at analysis-time. This is part of why Block A is framed as a fresh campaign (§0), not an extension of the earlier scored rows.

---

## 12. Block B pre-registration — selection rule locked BEFORE Block A results (2026-09-01)

Shuffled and decoy arms return in **Block B**, on **12 receptors** selected from the 48-receptor Block A panel. Registered in this section **before Block A dispatches** so the Block B panel is not chosen on Block A's specific outcomes (which would be circular).

**Superseded criterion recorded — α5-CT 21-mer identity degeneracy (2026-09-01):**

> The α5-CT 21-mer diff criterion is degenerate at the class level — all Gi↔Gs pairs tie at 6/21 identity (15/21 sites differ). Sequence divergence at the α5-CT cannot rank shuffled partners at the class level.

The initial α5 21-mer identity rule (rank ascending, top-12 with alphabetical tiebreak) collapsed to a 29-way tie at 6/21 and produced an alphabetical, aminergic-heavy, near-Gq-free panel. That selection is retired; the finding remains as rationale for changing the axis.

**Prior draw retired (recorded for provenance, 2026-09-01).** The initial per-class draw at seed 20260902 pulled its Gs slots from the full Class A Gs stratum with no pool-eligibility filter and therefore took **FSHR + LSHR** — both pre-registered apo failures per §1a — as the 2 Gs receptors, and pulled Gi slots that included **CNR1 + OPRD** (agonist-only active refs) and **NPY2R + CXCR4** (§13 held-out set). It also carried the "exclude B1B1U5" carve-out as a receptor-level clause instead of routing the whole draw through the panel-of-record eligibility file. That draw is retired and replaced by the v2 rule below; the finding stands as rationale for building `refs/eligible_pool.csv` and switching every future §12/§14 draw to source from it.

**Selection rule (locked, 2026-09-01 — v2, sourced from eligible pool):**

1. **Pool**: `refs/eligible_pool.csv` filtered to `excluded=0`. This applies the §1a exclusions (B1B1U5, CNR1, OPRD, OPSD, LSHR, FSHR) and the Class-B/F-out-of-scope rule in one place, so both §12 (Block B) and §14 (sealed) draw from the same 34-receptor Class A eligible pool.
2. **Class quota**: **7 Gi + 3 Gq + 2 Gs = 12**. Mirrors the Class A primary ratio (21 Gi : 10 Gq : 3 Gs post-eligibility, modulo rounding); ensures Block B covers all three canonical Class A transducer classes and is not dominated by the largest stratum. Note the Gs pool is 3 (AA2AR, ADRB1, ADRB2) after §1a exclusions remove FSHR + LSHR, so the 2 Gs slots are drawn from those three; that is the intended fix.
3. **Within-class draw**: `random.Random(20260903).sample(sorted(pool_class_c), quota_c)` for each class `c` ∈ (Gi, Gq, Gs). Seed **20260903** (day+2 from the panel finalization) — a fresh seed, not the retired-draw's 20260902, so the reproducible provenance points at the correct pool. Deterministic; the previous alphabetical-aminergic bias is not reintroduced.

**Class B/F receptors are excluded from Block B** — Class B all-Gs cognate makes the shuffle question uninformative; Class F is per-receptor case study by construction. Encoded via `excluded=1` in the eligible pool.

**The 12 Block-B receptors (locked, seed=20260903, pool = `refs/eligible_pool.csv` excluded=0):**

| Class | Receptor | Primary Gα |
|---|---|---|
| Gi | ACM2 | alphai1 |
| Gi | ACM4 | alphai1 |
| Gi | CCR5 | alphai1 |
| Gi | CNR2 | alphai1 |
| Gi | DRD2 | alphai1 |
| Gi | LPAR1 | alphai1 |
| Gi | LT4R1 | alphai1 |
| Gq | AGTR1 | alphaq |
| Gq | EDNRA | alphaq |
| Gq | GRPR | alphaq |
| Gs | ADRB1 | alphas |
| Gs | ADRB2 | alphas |

Per-class breakdown: **7 Gi + 3 Gq + 2 Gs = 12**. Block B queues after Block A rows.csv is landed. Overlap with §14 sealed 8: `{ADRB1, EDNRA}` — allowed by design (a sealed receptor may appear in Block B; its sealed active reference stays sealed regardless of which block it is scored in).

---

## 13. Held-out threshold validation (2026-09-01)

**Question addressed**: the current thresholds (NPxxY-OH 9.082 Å, GPCRdb TM6 tilt 14.932 Å) are midpoints derived on the same 80 tier-1 reference rows they are evaluated against, and tilt was selected as the best-of-~8 candidate metrics. Held-out validation withholds 8 Class A receptors, re-derives both thresholds on the remaining 32, and reports accuracy on the held-out 8 under both the re-derived and full-panel thresholds.

**Selection**: `random.Random(20260901).sample(sorted(class_a_40), 8)` → **`['5HT2C', 'AGTR1', 'CXCR2', 'CXCR4', 'DRD2', 'LPAR1', 'MCHR1', 'NPY2R']`** (seed = today's date YYYYMMDD).

**Results** (`scripts/held_out_threshold_validation.py`; full report at `experiments/018_block_a_switch_test/analysis/held_out_validation.md`):

| Metric | Direction | Re-derived thr (train n=32) | Full-panel thr | Δ | Held-out acc @ re-derived | Held-out acc @ full-panel |
|---|---|---:|---:|---:|---:|---:|
| `d_npxxy_oh_ref` | active_lt | 9.126 Å | 9.082 Å | +0.044 | **14/16 (87.5%)** | **14/16 (87.5%)** |
| `d_gpcrdb_tm6_tilt_ref` | active_gt | 14.945 Å | 14.932 Å | +0.013 | **16/16 (100.0%)** | **16/16 (100.0%)** |

**Interpretation**: The re-derived thresholds differ from the full-panel thresholds by < 0.05 Å on both metrics; held-out accuracy is **identical** under either threshold. The two NPxxY-OH held-out misses (5HT2C active 12.5 Å, MCHR1 active 11.6 Å — both above the 9.08 Å threshold in the active direction) are misses under both thresholds, not artefacts of re-derivation. This is a **validation figure demonstrating threshold stability**, not a re-calibration.

**Block A scoring uses the full-panel thresholds** (NPxxY-OH 9.082 Å active_lt; GPCRdb TM6 tilt 14.932 Å active_gt) — the numbers already in `refs/thresholds_panel.csv` and codified in `scorer/switch_signal.py::MotifThresholds`. This section adds an **out-of-fold validation figure to report** alongside the in-fold self-classification numbers (§2b).

---

## 14. Sealed active-reference subset (2026-09-01, **v3 — eligible-pool draw**)

**Question addressed**: every receptor in the Block A panel has deposited active-state structures predating every backbone's training cutoff. Without a pre-committed sealed subset, the campaign cannot distinguish prediction from recall. A pre-registered sealed subset lets the paper assert prospectivity by demonstration, at zero compute cost.

**Prior attempts retired (recorded for provenance).**
1. **v1 (seed 20260901).** Not a physical seal — left rows in `reference_set.csv` under an analysis-side gate only. Also collided with §13 held-out (same seed). Retired.
2. **v2 (seed 20260902).** Physical move landed and was disjoint from §13, but the pool was `class_a_40 − held_out_8` with no §1a filter, so the draw took **B1B1U5** (JSR1 non-mammalian singleton) and **FSHR** (pre-registered apo failure) among its 8 — both of which the panel explicitly downgrades to non-primary. A sealed subset that contains pathologies cannot function as the prospectivity demonstrator (either the sealed number carries their pathology, or it excludes them post hoc — either way, retired). Retired 2026-09-01.

**Selection (v3, locked)**: `random.Random(20260903).sample(sorted(eligible_pool ∩ excluded=0 ∩ ∉ held_out_8), 8)` → **`['ACM1', 'ADA2A', 'ADRB1', 'CCKAR', 'DRD3', 'EDNRA', 'HRH3', 'OX2R']`**

- Seed `20260903` (day+2 from panel finalization; fresh seed, not the retired v2 seed).
- **Pool source**: `refs/eligible_pool.csv` filtered to `excluded=0` (34 rows), then intersected with the complement of §13 held-out set → **26-receptor sealed pool**. Held-out set explicitly excluded so seal ∩ held-out = ∅ by construction.
- Sample without replacement.

**Sealed CSV**: `refs/sealed_active_refs_2026_09_01.csv` — 8 active-role rows **physically moved** out of `refs/reference_set.csv` and into this file, with sealed-until header metadata (including `pool_source: refs/eligible_pool.csv`).

**SHA256**: `879046326c6b8469f8b2f78f82280876da980f004a0b2c7f4cfc3095b2d9bc8e`

**Seal timestamp (UTC)**: `2026-09-01T14:33:41Z`

**Operational semantics — physical move:**

- The 8 sealed receptors' active-role rows are **no longer in `refs/reference_set.csv`** — they have been moved into the sealed CSV. Anything reading `reference_set.csv` (scorer, analysis scripts) no longer sees them.
- The scorer reads active references only at **scoring time** (post-prediction), not at dispatch time. Prediction input files never contain the active reference — the receptor sequence + partner sequence are all the input needs. The physical move is therefore safe for dispatch.
- **Unseal condition (pre-registered)**: Block A predictions landed AND `experiments/018_block_a_switch_test/runs/initial/rows.csv` frozen (git-tagged with the frozen-corpus tag). At the unseal moment, the sealed rows are merged back into the working `reference_set.csv` for scoring the sealed 8.
- Enforced physically: any analysis script that needs an active reference for a sealed receptor MUST go to the sealed file (`refs/sealed_active_refs_2026_09_01.csv`), and doing so is the documented unseal step.

**Gate check**: `scripts/step7_dispatch_gate.py::check_sealed_refs_physically_moved` — reads the sealed slugs from the sealed CSV, asserts no active-role row survives in `reference_set.csv` for any of them, and asserts the sealed CSV SHA256 matches the pinned value above. The gate blocks dispatch if either invariant is violated.

**Reproducibility check**: `scripts/seal_active_refs.py` re-runs the seed-20260903 draw from the eligible pool. Idempotent: on re-run against an already-sealed state, no-ops with a clear message. Reversible: if invoked against a prior-seed sealed state (e.g. v2), the script first restores the prior-sealed active rows back to `refs/reference_set.csv`, then physically moves out the new draw.

---

## 15. Amendments (locked, external documents)

Amendments to this pre-registration live in dedicated documents under `docs/` and are enumerated here for traceability. Each amendment is section-numbered (§A, §B, §C, §D, ...) and is version-locked at its authoring date; edits to a locked amendment require a superseding amendment.

- **§C — Block C ligand-state tiers (Tier 1 + Tier 3)** — `docs/BLOCK_C_PREREG_AMENDMENT_2026_09_03.md` — §C-1 through §C-13 locked 2026-09-03. Covers the ligand-state grid (agonist / antagonist / decoy) at Class A panel scale, the fire-gate ordering, sealed-subset discipline, and the class-conditional two-instrument predicate (§C-5).
- **§D — Post-Tier-3 final leg (D1 deep apo, D2 directed inactive, D3 MSA-depth)** — `docs/BLOCK_D_PREREG_AMENDMENT_2026_09_06.md` — §D-1 through §D-3 locked 2026-09-06. Covers the three follow-up tiers with grids, fire-gates, expected nulls, kill-criteria, and the (5, 100) sample-count departure for D1 as a targeted resampling.

Any future amendment gets its own §-numbered document + a one-line pointer here.

---

## Open TODOs (all before Block A dispatch)

- [x] §2a-b: all 6 metric thresholds derived from tier-1 crystals. **TM5-outward and ICL2-helicity DROPPED from composite** (both flat / wrong-signed on panel). Composite is now k-of-2 over 3 metrics: DRY (11.54 Å, 19/40), NPxxY OH (9.08 Å), Y5.58 pack (4.37 Å). Codified in `scorer/switch_signal.py::MotifThresholds`.
- [x] §2c: Class B/F anchors derived. Class B (Wootten) = 3.50 — 6.34, margin +9.59 Å. Class F (GPCRdb-F) = 3.50 — 6.31, margin +1.80 Å. 8 tier-1 non-A receptors (GLP1R, GCGR, PTH1R, CRHR1, FZD4, FZD6, FZD7, SMO) available for panel extension via `scripts/merge_class_bf_into_panel.py`.
- [x] §4: GNAT1 sequence in `partners.fasta` (350 aa, sha `61cc7bb7`); α5-CT diff report at `refs/gnat1_vs_gnai1_alpha5ct_diff.md` — 2 substitutions in last 21 aa, 0 on L15/E19/L21 chemistry positions.
- [x] §6: construct audit complete. `active_stabilization_source` + `alpha5_donor_class` populated in `refs/reference_set.csv`. 2 in-panel chimeras (5HT2C/8DPF, ACM1/6OIJ) — both donor-Gq matches primary-Gq; no coupling corruption.
- [x] §8: `coupling_evidence` filled for all 40 rows (all `primary_reference`).
- [x] §9: K, N locked at (5, 5). 5 seeds is the bootstrap-CI floor; user-approved 2026-09-01.
- [x] §10: 3 partner-interface metrics (`d_ga_alpha5_r350_ca`, `n_interface_contacts_ga_receptor`, `plddt_ga_alpha5`) + NPxxY OH-OH implemented in scorer (commit 411340b, 18 new tests all passing).

Sign-off block below the horizontal rule when all TODOs are cleared.

**Remaining hard-blockers before Block A dispatch**:
1. §2c Class B/F anchors (agent-in-flight)
2. Y5.58/DRY/TM5/ICL2 tier-1 crystal refs (agent-in-flight; blocks §2a-b full closure)
3. §9 user picks (m,n) rule
4. Rescore existing mn_consensus predictions with new scorer to enable Step 3 full agreement matrix
5. MSA pre-warm for all 40 receptor sequences (~3-4 hrs, zero-GPU)

---

## Consolidated findings (2026-09-01 curation pass — Steps 0-6)

Coordinator progress against the pre-dispatch TODO. Not sign-off — surfacing what's landed and what's still open.

### Step 0 — panel verification ✅
Confirmed `refs/gpcr_coupling.csv` (sha256 `253e5d36…`, 40 rows). No alternate coupling CSV. DRD1/DRD4/HRH2/HRH4/TSHR/MC1R/TRHR are NOT in the panel — the stale references in `docs/RECEPTOR_READINESS_*` and `docs/EXPERIMENT_CATALOG/*` are now stamped SUPERSEDED.

### Step 1 — reference-provenance audit (`refs/reference_provenance_grid.csv`) ✅
- **TM6 axis**: 40/40 tier-1 (own active + own inactive) — headline unchanged.
- **NPxxY axis**: 40/40 `not_computed` — reference_set.csv currently only carries `d_r350_r630_ca_ref`. **Dispatch blocker** — NPxxY OH-OH + CA-CA references must be derived from tier-1 crystals before threshold calibration.
- **Chimera scan**: 2 in-panel chimeras (5HT2C/8DPF, ACM1/6OIJ) — both α5-donor Gq matches primary Gq; **no coupling-assignment corruption** in the panel.
- **JSR1 fix**: B1B1U5 active reference updated from 9EPP (Gi/q chimera, α5-donor Gq — would have contradicted primary Gi) to 9EPR (native Gi heterotrimer). TM6 ref pending re-derivation.

### Step 2 — threshold sourcing (`refs/thresholds_sourced.md`) ⚠
**0 of 6 metrics** with HIGH-confidence literature thresholds — publisher-paywall + missing WebSearch blocked primary-source access. All six metrics default to **panel-derived** with ±20% sensitivity sweep. Weak field-folklore backing on 3: DRY (5 Å, standard salt-bridge criterion), NPxxY OH-OH (~7.5 Å), ICL2 helicity (~0.5).

**DRY caveat**: not universally intact in Class A inactive crystals (β2AR, some aminergics have broken lock even inactive). Per-receptor DRY discrimination must be reported separately in panel calibration; receptors with inactive `d_dry > 5 Å` flagged as "lock-uninformative for this receptor."

The threshold table in §2b is superseded by `refs/thresholds_sourced.md` — merge into §2b once panel-derived values are computed.

### Step 4 — switch-signal analysis module ✅
Landed as `scorer/switch_signal.py` with 19 passing tests (`tests/test_switch_signal.py`). Enforces:
- **Seed as unit of variance** — `per_seed_mean()` collapses to seed-level; bootstrap CI never over rows.
- **No cross-arm row pairing** — `delta_d_tm6_per_cell()` bootstraps seeds independently in each arm, subtracts arm means.
- **k-of-n (≥3 of 5) motif rule** with NaN-as-fail semantics and `confidence_flag == "low"` as hard-fail.
- **Placeholder thresholds in `MotifThresholds`** — must be replaced with panel-derived values from §2b before Block A dispatch.

### Step 5 — Class B / F discovery + per-class anchors 🕓
Delegated (agent still running). Writes to `refs/reference_set_class_bf.csv`, `refs/anchors_per_class.csv`, `refs/gpcr_coupling_class_bf.csv`. Class C excluded on activation-mechanism grounds (dimer interface).

### Step 6 — A1 refactor 🎯
**Finding from Step 1**: with 40/40 tier-1 on TM6 and `pc4_identity_anchors_match` already deriving `aa_expected` from GPCRdb (which for Class A IS the receptor's own crystal-derived canonical), A1 is **already effectively per-receptor-strict** for the current panel. The refactor collapses to:
1. **Tighten** the orchestrator gate: `warn_A1` → hard fail for Block A panel dispatch (soft warn remains for non-panel).
2. **Extend** for Class B/F: when Step 5 delivers the extended panel, `pc4_from_reference_set()` variant reads BW→AA from `refs/reference_set.csv` locally instead of hitting GPCRdb (cross-class robustness + audit trail).

Item 1 is a small, targeted change in the dispatch layer, not the scorer. Item 2 lands post-Step-5. See `experiments/block_a_switch_test_deferred/BLOCK_A_STEP6_A1_NOTE.md`.

### New dispatch blockers surfaced by this pass

- **NPxxY OH-OH + CA-CA reference derivation** for all 40 receptors from tier-1 crystals (agent in-flight).
- **Panel-derived threshold computation** for all 6 motif metrics (drops out of NPxxY ref derivation + rescore of existing predictions).
- **Partner-interface metric implementation** (`d_ga_alpha5_r350_ca`, `n_interface_contacts_ga_receptor`, `plddt_ga_alpha5`) — agent in-flight.

---

*Not yet signed off. Sign-off requires all TODOs in §Open TODOs closed AND Consolidated Findings §Step 5 delivered AND the two in-flight agents landed.*
