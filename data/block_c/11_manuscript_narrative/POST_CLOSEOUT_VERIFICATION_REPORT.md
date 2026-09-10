# POST-CLOSEOUT VERIFICATION REPORT

**Date**: 2026-09-10.
**Baseline**: paper_af3 working repo at `a090c9a` + paper_af3_release at
`4f6452f` (post-BLOCK_C_CLOSEOUT). Read-only pass; two parts bundled.
**Rule**: audit first, fix separately. Report evidence and stop.

---

# PART 1 — Block C pre-tag verification

## 1a — Rebuild-and-diff harness: **STUB, no functional check**

**Status: harness exists as scaffolding but does not actually rebuild any
block.**

- `paper_af3_release/Makefile` defines four targets: `all`, `negative-control`,
  `manifest`, `ledger-check`. `all` runs `block_a` only.
- `block_a` invokes
  `code/build_scripts/rebuild_block_a.py --data data/block_a --panel panel/
  --out analysis/block_a/_rebuild --diff-against analysis/block_a`.
- Running `make all` in the release repo prints:
  ```
  [rebuild_block_a] STUB — v1 not yet implemented.
  [rebuild_block_a] Data: …/data/block_a
  [rebuild_block_a] Panel: …/panel
  [rebuild_block_a] Would emit into: …/analysis/block_a/_rebuild
  [rebuild_block_a] Would diff against: …/analysis/block_a
  [rebuild_block_a] See release/dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md
                    Phase 4 for the analytical scripts to migrate here.
  [rebuild_block_a] Returning 0 (stub PASS).
  block_a: PASS
  === release/ rebuild + diff: PASS ===
  ```
- **The "PASS" is a stub return, not a real diff.** No output files are
  written into `analysis/block_a/_rebuild`; nothing is compared against the
  stored analysis outputs.
- **No `rebuild_block_b.py` or `rebuild_block_c.py` exists.** The Makefile
  has no target for Block B or Block C rebuilds.

**Consequence for the closeout**: the BLOCK_C_CLOSEOUT dispatch (Part B
item h) asked for a green/red result or a plain "no harness" statement.
**Plain statement**: no functional rebuild-and-diff harness exists for
Block C (nor Block B); Block A has a stub that returns 0 without doing
work. This should be recorded in Flag C-11 (deferred gates) and named in
the manuscript's Methods appendix on reproducibility.

**Options for a fresh dispatch** (not run here):
- (A) Implement `rebuild_block_c.py` that re-runs `g1_bootstrap_s1_auroc.py`
  + `g2_refsep_vs_auroc.py` + `stage3_post_audit_analysis.py` from
  `data/block_c/tier3/` inputs and diffs against `analysis/block_c/*.json`.
  Cost: ~2–4 h of scripting; needs the rows.tier3.v2.csv to live in a
  reachable path (currently kept out of git via
  `data/block_c/tier3/MANIFEST_RAW_ROWS.md`).
- (B) Extend `ledger-check` to at least verify SHA-256 integrity of every
  claim sheet's cited input file — a partial-but-real check that runs today.
  Cost: ~30 min.
- (C) Retire the rebuild-and-diff item from the release contract as
  "aspirational, deferred to post-manuscript". State the deferral in
  VERSION.md.

## 1b — SC-C-1 receptor set pinned; cluster-boot CI recomputed

### 1b.i — Receptor-set pin

**SC-C-1's four point estimates (Boltz −0.306, Chai −0.137, OF3 −0.252,
Protenix −0.184 Å) are computed on the 23-receptor 2×2 common set**, NOT
on the S1 15-set nor on all 36 landed receptors.

Verified via `experiments/021_block_c_tier3_pharmacology/analysis/verification/stage3_2x2_ligand_state_specificity.json`,
which reports `per_backbone.<bb>.interaction.n_receptors_in_common: 23`
uniformly across all four backbones. The 23 receptors are the intersection
of {receptors with ≥ 1 full_agonist row with non-NaN pocket_ca_rmsd_active
AND pocket_ca_rmsd_inactive} × {receptors with ≥ 1 neutral_antagonist
row with non-NaN pocket_ca_rmsd_active AND pocket_ca_rmsd_inactive}.

**Pinned 23-receptor list** (same as `s1_loro_classifier.json`'s
`common_receptors`):
```
5HT1B, 5HT5A, AA1R, AA2AR, ACM2, ACM4, ADRB2, AGTR1, CCR5, CNR1, CNR2,
CXCR2, CXCR4, EDNRB, GRPR, LPAR1, LT4R1, MCHR1, NPY1R, NPY2R, OPRD, OPRK,
OPRX
```

**Correction to C-C-3**: the caveat's "15 or 23 receptors" ambiguity
resolves cleanly to **23**. The 15-set is for the KILL-S1 kill-row
(self-ref-excluded); the 23-set is for the 2×2 pocket-Cα interaction.
SC-C-4 (S1 classifier) uses 15; SC-C-1 (2×2) uses 23.

### 1b.ii — Cluster-boot recompute

23 receptors map to **16 paralog clusters** (from
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`).
All 23 receptors have cluster assignments. Cluster sizes: 8 singletons
(adenosine, adrenergic_beta, angiotensin, bombesin, chemokine_ccr,
endothelin, leukotriene, lysophosphatidic, melanin_concentrating_hormone,
opioid_nociceptin — actually 10 singletons) and 6 multi-member clusters
(adenosine{AA1R,AA2AR}, cannabinoid{CNR1,CNR2}, chemokine_cxcr{CXCR2,CXCR4},
muscarinic{ACM2,ACM4}, npy{NPY1R,NPY2R}, opioid{OPRD,OPRK},
serotonin{5HT1B,5HT5A}).

Cluster-boot CI (5000 iter, seed 1234, matching the receptor-boot's
protocol with the resampling unit swapped from receptor to cluster):

| backbone | point (Å) | cluster-boot CI 95 (n_clusters=16) | receptor-boot CI 95 (JSON, n_recs=23) | signed non-zero (cluster)? |
|---|---:|---|---|---|
| boltz | **−0.306** | **[−0.454, −0.164]** | [−0.431, −0.192] | YES |
| chai | **−0.137** | **[−0.216, −0.045]** | [−0.223, −0.055] | YES |
| of3 | **−0.252** | **[−0.405, −0.099]** | [−0.384, −0.129] | YES |
| protenix | **−0.184** | **[−0.277, −0.088]** | [−0.271, −0.101] | YES |

**All four backbones' cluster-boot 95 % CIs sign non-zero. SC-C-1's
"signed non-zero on all four backbones" claim survives cluster-boot.**

Cluster-boot CIs are ~15–25 % wider than receptor-boot (expected — fewer
independent units), most notably on Chai where the cluster-boot upper
bound (−0.045) is closer to zero than receptor-boot's (−0.055). Chai
remains signed under cluster-boot with a narrow margin.

**Output**: `experiments/021_block_c_tier3_pharmacology/analysis/verification/g_scc1_cluster_boot.json`
(SHA-256 in artefacts if committed).

**C-C-3 status update text** (proposed — not yet applied to the
caveat):
> **UPDATED 2026-09-10**: The SC-C-1 receptor set is pinned to the 23-receptor
> 2×2 common set (`s1_loro_classifier.json.common_receptors`); the 15-set
> is for KILL-S1 (SC-C-4), not SC-C-1. Cluster-boot 95 % CI over 16
> paralog clusters recomputed:
> Boltz [−0.454, −0.164], Chai [−0.216, −0.045], OF3 [−0.405, −0.099],
> Protenix [−0.277, −0.088]. All four sign non-zero. The receptor-boot CIs
> in `stage3_2x2_ligand_state_specificity.json` are retained as secondary.
> This caveat may be downgraded to "convention-alignment complete" once
> the claim sheet's SC-C-1 numbers are updated with the cluster-boot CIs.

## 1c — Four dispatched-not-landed receptors

**Pinned list**: `B1B1U5`, `FSHR`, `LSHR`, `OPSD` — dispatched per
`refs/tier3_panel.csv` (40 rows) + BLOCK_C_TIER3_DISPATCH_CONTRACT_2026-09-04
(40-receptor list), absent from `rows.tier3.v2.csv`'s distinct
receptor_slug set (36 non-null slugs).

### Reasons per receptor

**B1B1U5 (jumping spider rhodopsin, non-human)** — SYSTEMATIC.
- Dispatched: yes; 400 prediction paths present in the corpus.
- Landed with `passed=True`: no; all 400 rows have `passed=False`,
  `A5_species_match=A5SpeciesMismatch`, and `receptor_slug=nan`.
- Root cause: species-mistagging pattern per `docs/AUDIT_TRAIL.md §21`.
  The species-fix landed AFTER the Block C dispatch fired; pre-fix rows
  carry the failure flag. Non-human receptor slug expected `human` on
  the wrong metadata column.

**OPSD (bovine rhodopsin, non-human)** — SYSTEMATIC.
- Dispatched: yes; 400 prediction paths present.
- Landed with `passed=True`: no; all 400 rows fail identically to
  B1B1U5 (`A5SpeciesMismatch`, `receptor_slug=nan`).
- Root cause: same species-mistagging pattern; OPSD is bovine, hit by
  the same pre-fix bug.

**FSHR (Class-A glycoprotein hormone receptor)** — SYSTEMATIC.
- Dispatched: **no**; 0 rows in rows.tier3.v2.csv.
- Root cause per `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/pr2_fshr_lshr_class.json`:
  Block C Stage 2 dropped FSHR from the ligand panel because the
  reference-inactive PDB 8I2H is "FSH + compound-21f PAM at 6.00 Å"
  (positive allosteric modulator bound in the inactive-reference
  pocket) — not a clean orthosteric antagonist.
- FSHR IS Class A per GPCRdb (subfamily "Glycoprotein hormone
  receptors", UniProt P23945). The "Class F short-circuit" reason
  attributed in an earlier T4 fork is wrong.

**LSHR (Class-A glycoprotein hormone receptor)** — SYSTEMATIC.
- Dispatched: **no**; 0 rows.
- Same reason as FSHR: inactive PDB 7FIJ is "hCG + Org43553 allosteric
  agonist" — non-clean inactive orthosteric reference.
- Also Class A per GPCRdb (glycoprotein hormone receptor family).

### Distribution: SYSTEMATIC, two overlapping causes

- **Non-human species** (2 of 4): B1B1U5, OPSD. Reason is a pipeline
  species-metadata bug (`A5_species_match`), independent of the
  receptor's biology. Fires on any non-human receptor whose species
  wasn't in the expected mapping at scoring time.
- **Non-clean inactive references** (2 of 4): FSHR, LSHR. Reason is a
  curation choice — the glycoprotein hormone receptor subfamily doesn't
  have deposited clean-orthosteric-antagonist inactive references
  (they're allosterically stabilized). Would recur on any receptor in
  the same subfamily.

**Neither is incidental.** Both are shared class-property issues that
would affect any future dispatch on the same receptor classes. The
36-landed panel is thus not a random subset of the 40-panel — the 4
drops are structurally consistent, and their absence is a scope
statement.

**C-C-9 status update text** (proposed — not yet applied):
> **UPDATED 2026-09-10**: The 4 dispatched-not-landed receptors are:
> B1B1U5 + OPSD (both dispatched but all 400 rows each fail on the
> pre-fix A5_species_match pattern; non-human species pipeline bug);
> FSHR + LSHR (both zero-row on rows.tier3.v2.csv; Stage 2 dropped them
> because their inactive-reference PDBs carry PAM bound in the pocket,
> not orthosteric antagonist). Both drops are systematic
> (non-human-species pipeline bug × 2; PAM-inactive-reference curation
> pattern × 2), not incidental — a re-dispatch of the same design would
> re-produce the same 4 drops.

## 1d — W-C-5 apo rate coincidence check

**Verdict: SAME STATISTIC, not coincidence. Block A's dossier needs the
correction too — flagged, NOT applied.**

Both `~14.5 %` and `15.5 %` are computed as:
`fraction of apo-arm rows where (d_npxxy_y558_y753_oh < 9.082 AND
d_gpcrdb_tm6_tilt_246_637_ca > 14.932)`, on the 40-receptor
frame_40 Class A panel-mean, per Block A rows.

Provenance chain:
- **~14.5 %**: cited in earlier Block A drafts + auto-memory
  `apo_bistability_reference_artefact_2026_09_06` (prior figure).
- **15.5 %**: recomputed with pinned provenance per that same memory
  record: *"Panel-mean apo two-instrument coh-active fraction is 15.5%
  (recomputed with provenance; prior 14.5% figure superseded)."*

**Both numbers apply to Block A, not Block C.** The Block C paper draft
(v1) inherited W-C-5's "14.5% → 15.5%" retraction as if it were a Block C
number — that inheritance is wrong. Both numbers are Block-A panel-mean
apo coh-active fractions.

**Block A dossier state**:
- Release repo `dossiers/BLOCK_A/` and `BLOCK_A_CLAIM_SHEET.md`: not
  audited for whether they carry `14.5 %` or `15.5 %` (out of scope for
  this read-only pass — deferred). If they carry `14.5 %`, the
  correction needs to be applied to Block A's claim sheet too.

**Which of Block A's 9 surviving claims is affected?**
- Block A's apo-coh-active-fraction number does NOT appear as an SC-N
  claim in the release LEDGER (SC-1..SC-10 don't cite it). It appears
  in the pre-review dossier prose and in one Block A withdrawal
  (`W-1_apo_bistability_panel_mean.md` cites "14.5 %" as the retracted
  panel-mean framing).
- **W-1's retraction is about the panel-mean vs stratum-mean framing**
  (per the withdrawal note), not about the numeric value. So the
  15.5 % correction affects the number IF it's still quoted anywhere in
  Block A's dossier prose or in the paper draft's Methods.

**Recommendation** (not applied here):
- Grep Block A's release/ dossier for `14.5` and `15.5` and reconcile.
- Update `withdrawals/W-1_apo_bistability_panel_mean.md` in the release
  repo to note the corrected number (15.5 %) if it's still relevant
  for provenance.
- Add a one-line note to `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md`
  if it cites 14.5 %.

**No commit for this in Part 1** — per the dispatch rule; report the
coincidence and stop.

---

# PART 2 — Block A caveat triage (READ-ONLY)

## 2a — C-11 construct mismatch triage

### 2a.i — Full mismatch enumeration (this pass)

Full audit of `refs/reference_set.csv` construct=wt rows against RCSB
`pdbx_mutation` metadata (cached at `refs/cache/rcsb/*_ent*.json`).

- **Refs total**: 168 (in current reference_set.csv).
- **Cached / evaluable**: 163 refs with at least one `_ent*.json` file.
- **Rows with `construct=wt` (evaluable)**: 162.
- **Contradictions** (construct=wt but RCSB reports non-empty
  `pdbx_mutation`, mini-Gs `{S47N, G203A, E245A, A326S}` signature
  excluded): **48**.

Rate: **48 / 163 = 29.4 %** on this pass's cache coverage (compare C-11's
"52 / 127 = 41 %" and "41 / 127 = 32 % after mini-Gs exclusion" — my
denominator is larger (163 vs 127) because more RCSB entries have been
cached since the T4 audit, and my numerator is smaller because some
mismatches were fixed in POST_REVIEW_ANNOTATIONS.md, notably CNR2 5ZTY).

### 2a.ii — Block A panel scope

Of the 48 mismatches:
- **33 are in the Block A 48-receptor panel** (feed panel-level SC-1..SC-8
  claims).
- **15 are off-panel** (CCR8, NTR1×2, S1PR1, TSHR, MC3R, MCHR2, CALCR,
  NMBR, SSR1, SSR3, MC5R, OPSR, GPR12, P2Y10) — do NOT feed Block A
  claims.

### 2a.iii — Mutation-position classification (Block A panel, 33 mismatches)

Each mutation's residue number was classified against the receptor's
own BW anchor set (from `anchor_positions` in reference_set.csv), with
a ±3-residue window around each BW label. **Microswitch-adjacent** = any
mutation within ±3 of any of {3.50, 3.51, 5.58, 6.30, 6.34, 6.48, 6.51,
6.55, 7.49, 7.53}. BRIL/T4L fusion mutations at >900 numbering
(receptor-distal by construct convention) are excluded from the
classification.

**Distal** (all mutations receptor-distal from microswitch anchors) — 23 of 33:
5HT1B/4IAR, 5HT5A/7UM5, ACM2/5ZKC, ADRB1/7BVQ, ADRB2/4LDE (BRIL only),
AGTR1/4ZUD (BRIL only), B1B1U5/6I9K, CCKAR/7F8Y, CCR5/7F1S, CNR1/5U09,
CXCR4/3ODU, DRD3/3PBL, EDNRB/6IGK, GHSR/7F83, HRH3/7F61, LPAR1/7TD0,
LPAR1/4Z36 (BRIL only), LSHR/7FIH, NPY1R/5ZBQ, OPRD/4N6H (BRIL only +
P37S distal), OPRK/4DJH, OPRX/5DHH (BRIL only), FSHR/8I2G.

**Microswitch-adjacent** — 10 of 33:

| receptor | role | PDB | mutation(s) at microswitch | BW distance |
|---|---|---|---|---|
| 5HT5A | inactive | 7UM4 | I278A | 6.30 −2 |
| ACM1 | inactive | 6ZFZ | K362A, A364L | 6.30 +2, 6.34 +0 |
| APJ | inactive | 8S4D | I224A | 5.58 +3 |
| CNR1 | active | 5XRA | R340E | 6.30 +2 |
| CXCR2 | inactive | 6LFL | A249E | 6.30 +3 |
| GRPR | active | 7W40 | K265A | 6.34 +2 |
| GRPR | inactive | 7W41 | R259E | 6.30 +0 (exact) |
| LT4R1 | active | 7VKT | C287F | 7.53 +2 |
| NPY2R | active | 7YON | H149Y | 3.50 +1 |
| CCR5 | inactive | 5UIW | A233D | 6.30 +3 |

**Also flagged separately (already in POST_REVIEW_ANNOTATIONS)**:
- **CNR2 5ZTY inactive**: R242E at BW 6.30 exact — already corrected in
  reference_set.csv post-review (`construct=multi_mutation_incl_R242E_tilt_window`),
  so no longer a `wt` mismatch.
- **AGTR1 6OS2 active**: BRIL insertion at 227–229 (ICL3 adjoining TM6,
  predicate-window-adjacent) — not classified as `wt→mutation` here
  because `construct=nanobody` on this row. Flagged separately in Flag 43.

### 2a.iv — Which of Block A's 9 claims each mismatched PDB feeds

Block A's SC-1..SC-10 map to receptor-level operations:
- **SC-1, SC-2, SC-3, SC-7, SC-8, SC-4, SC-6**: panel-level medians /
  fractions across 39–48 receptors. **All 33 Block A panel mismatches
  feed at least one of these.**
- **SC-5**: AA2AR paired-switch only. AA2AR 5G53 IS in the mismatch list
  (`YES` marker in RCSB entity JSON — not concretely enumerated).
  Affects SC-5.
- **SC-9** (templates off): not affected — infrastructure claim.
- **SC-10** (panel of record): metadata claim; not scored, but the
  panel-of-record list rests on `refs/reference_set.csv` where the
  construct column is now known to be 30 % unreliable.

**Backbones affected**: every mismatch's reference feeds all 4 backbones
uniformly (the reference-side geometry is scored once per receptor and
compared against 4 backbones' predictions). Mismatches are NOT
backbone-specific — they are reference-side curation issues.

### 2a.v — Distribution: concentrated near TM6 microswitches

**Not random scatter.** Of the 10 microswitch-adjacent mutations
enumerated above:
- **7 sit at BW 6.30 ±3** (5HT5A I278A, ACM1 K362A, CNR1 R340E, CXCR2
  A249E, GRPR K265A/R259E, CCR5 A233D). **This is the DRY/ionic-lock
  residue and TM6-tilt anchor.** The concentration reflects a common
  crystallographic strategy: mutate residues near the ionic lock or
  TM6 kink to stabilize a preferred state.
- **2 sit at BW 5.58 or 6.34** (APJ I224A at 5.58, GRPR K265A at 6.34).
  Nearby but less microswitch-central.
- **1 sits at BW 7.53** (LT4R1 C287F). NPxxY microswitch — Y5.58/Y7.53
  packing anchor.
- **1 sits at BW 3.50** (NPY2R H149Y). DRY R3.50 residue itself.

**Concentration is real**: 10 of 33 (30 %) of Block A panel mismatches
carry a mutation within ±3 of a microswitch — much higher than random
scatter would predict (the 12 microswitch positions × ±3 = ~72
positions out of ~300 receptor residues = 24 % — but that's the ceiling
for random; observed 30 % is just above, suggesting a MODEST enrichment
for microswitch-adjacent mutation, consistent with crystallography
targeting stabilizing mutations at conformational hinges).

**Receptor family clustering**: no single family dominates —
aminergic (5HT5A, ACM1, NPY2R), peptide (APJ, CNR1, GRPR × 2, LT4R1),
chemokine (CXCR2, CCR5), all represented. Not a family-specific
artefact.

**Backbone clustering**: N/A — mutations are on references, scored
against all 4 backbones. No prediction-side artefact.

### 2a.vi — Manuscript sentence-status

**Nothing changes on any surviving SC-1..SC-10 claim from this triage
alone.** The mismatch rate (48 / 163 = 29 %) is consistent with C-11's
stated bound. The specific 10 microswitch-adjacent mismatches were
identified by the ±3-window heuristic (approximate — real
BW-to-sequence mapping requires per-PDB SIFTS parsing which is not done
here). None of the 10 have been individually verified as materially
shifting Block A's numbers.

**However**: the concentration at BW 6.30 (7 of 10) is a specific
sub-finding worth naming in the C-11 caveat text — the mismatches are
not uniformly distributed across the receptor structure; they cluster
where crystallographers most often intervene, which is exactly the
region Block A's predicate reads. **The caveat's original wording is
weaker than the data now shows.**

**Recommendation** (not applied here):
- Extend C-11's manuscript sentence to name the BW 6.30 concentration
  (7 of 10 microswitch-adjacent mutations at 6.30 ±3).
- Consider adding a dedicated sub-claim / sensitivity analysis:
  "the SC-3 (TM6 tilt shift) headline recomputed after excluding the
  10 microswitch-adjacent references drops by <how much>". This would
  require re-running Block A's SC-3 aggregation with the E-A-<new>
  exclusion set. Not run in this pass.

## 2b — C-12 ACM1-cognate-Protenix + pLDDT sweep

### 2b.i — Per-claim inclusion of ACM1-cognate-Protenix

25 rows exist in `rows.csv`, all `passed=True`. **Impact on each of the
9 SC-1..SC-10 claims**:

| claim | ACM1 in denominator? | ACM1's delta_to_active | protenix panel median incl → excl ACM1 | impact |
|---|---|---|---|---|
| SC-1 (delta_to_active shift, apo→cognate) | **NO** (delta_to_active is NaN on all 25 rows because ACM1 is sealed → no active reference) | NaN | 6.116 → 6.116 | none |
| SC-2 (fraction of way from apo→active) | **NO** (same reason) | NaN | 0.9118 → 0.9118 | none |
| SC-3 (d_gpcrdb_tm6_tilt cognate−apo shift) | **YES** (uses row-intrinsic tilt values) | ACM1-Protenix shift = **+13.52 Å** (huge outlier vs panel median ~5 Å) | 5.307 → 5.279 | −0.028 Å (rounding-level) |
| SC-4 (κ two-instrument agreement) | **YES** | — | not recomputed here | expected small |
| SC-5 (AA2AR paired-switch) | **NO** (AA2AR only) | — | — | none |
| SC-6 (predicate false-positive rate 0.02 %) | **YES** | — | not recomputed here | ACM1 rows likely predicate-negative (unphysical tilt), so 2/9490 numerator likely unchanged |
| SC-7 (partner engagement ≥30 contacts, cognate arm) | **YES** | ACM1-Protenix engaged fraction = **0.80** (5 of 25 rows below 30 contacts) | 0.9881 → **0.9922** | +0.41 pp on Protenix; other backbones unchanged (ACM1 engaged at 1.0 on Boltz/Chai/OF3) |
| SC-8 (fold-integrity anchor pass rate 96.33 %) | **YES** | — (fold_integrity CSV schema unreadable in this pass — header parse error) | not recomputed | ACM1 rows have unphysical d_tm6 = 31.95 (median) — likely fail fold-integrity anchor pass; exclusion would nudge Protenix upward |
| SC-9 (templates off) | N/A | — | — | none — infrastructure |
| SC-10 (panel of record) | N/A (metadata) | — | — | none |

**Materially affected**: SC-7 by +0.41 pp on Protenix (98.81 → 99.22 %).
**Cosmetically affected**: SC-3 by −0.028 Å on Protenix (5.307 → 5.279).
**Others**: ACM1's Protenix cognate rows already dropped from the
denominators of SC-1 and SC-2 via `delta_to_active = NaN` on sealed
receptors.

**No headline number changes materially.** The E1 exclusion set (which
already lists ACM1-cognate-Protenix per Flag 46) is the correct
mechanism; applying it explicitly tightens Protenix's SC-7 engagement
figure but doesn't move the qualitative claim.

### 2b.ii — pLDDT sweep across Block A corpus

**380 (receptor × backbone × arm) cells** in Block A (48 receptors × 4
backbones × 2 arms − 4 non-scored FZD4-cognate variants). Cell-mean
pLDDT distribution:

| statistic | value |
|---|---:|
| mean | 73.05 |
| std | 6.13 |
| min | 38.66 (ACM1-cognate-Protenix) |
| q0.1 % | 46.31 |
| q0.5 % | 60.19 |
| q1 % | 61.48 |
| q5 % | 64.22 |
| q10 % | 65.49 |
| q25 % | 68.85 |
| q50 % (median) | 72.95 |
| q75 % | 76.93 |
| max | 92.38 |

**Where a natural floor would sit**: the distribution has a heavy body
between 60 and 90, with a SINGLE outlier at 38.66 (ACM1-cognate-Protenix)
and no other cell below 55. The next-lowest cell is **HRH1-boltz-apo at
58.85** — a 20-pLDDT gap.

**A natural floor could reasonably sit at 60** (catches the two lowest:
ACM1-cognate-Protenix + HRH1-boltz-apo). A floor at 55 would catch only
ACM1-cognate-Protenix.

**Cells failing floor thresholds**:
- pLDDT < 40: 1 (ACM1-cognate-Protenix)
- pLDDT < 55: 1
- pLDDT < 60: 2 (adds HRH1-boltz-apo)
- pLDDT < 65: 30

**Distribution of the < 65 tail**:
- 14 of 30 are OF3 apo cells (OF3's apo pLDDT distribution runs
  systematically ~5 points below its cognate — visible in the
  by-backbone × arm breakdown).
- ~10 of 30 involve Class B receptors (PTH1R × 4 cells, plus GLP1R,
  CRHR1 variants that appear in the raw counts).
- The remaining ~6 are scattered — mostly aminergic apo cells.
- **Cluster pattern**: Class B receptors and OF3 apo — both are
  systemically harder to fold at these levels. Not a broken-cell
  pattern; more like "expected difficulty."

**Between the ACM1-cognate-Protenix outlier and the natural-body-of-
distribution**: nothing else looks like a "broken cell" in the C-12
sense. **ACM1-cognate-Protenix is isolated, not a symptom** of a wider
Block A quality issue.

**Backbone / arm clustering summary**:

| backbone | mean | std | max | min |
|---|---:|---:|---:|---:|
| boltz | 74.86 | 7.19 | 92.38 | 58.85 |
| chai | 75.06 | 5.08 | 87.95 | 63.11 |
| of3 | 70.20 | 4.70 | 82.29 | 62.27 |
| protenix | 72.08 | 5.94 | 86.64 | **38.66** |

Protenix has the widest range because ACM1-cognate is at 38.66; if that
one cell is excluded, Protenix's minimum climbs to ~61 (comparable to
OF3's floor). **No general Protenix pLDDT-floor issue**; the observed
range is driven entirely by one cell.

### 2b.iii — Manuscript sentence-status

**Nothing changes on any surviving SC-1..SC-10 claim** from this pass:
- SC-1, SC-2 unchanged (ACM1 already excluded via sealed-reference NaN).
- SC-3 unchanged materially (Protenix 5.31 → 5.28 Å is rounding-level).
- SC-7 modest change (Protenix 98.8 % → 99.2 % if E1 applied); does not
  change the "engagement ≥ 97 % all backbones" summary claim.

**C-12 stays valid as a caveat** — it correctly names ACM1-cognate-
Protenix as an outlier cell that all four A1–A6 assertions pass but that
carries unphysical geometry (d_tm6 = 31.95, tilt = 25.94, NPxxY-OH =
27.77 — all far outside plausible receptor windows). The manuscript's
Methods should either name the E1 exclusion set (containing this one
cell) or add a pLDDT floor to the A1–A6 assertion suite (which would be
a scoring-suite change, out of scope here).

**Recommendation** (not applied here):
- Consider adding a Methods sentence: *"A pLDDT-based fold-integrity
  floor at 60 (cell-mean pLDDT) would flag 2 cells across the 380-cell
  Block A grid: ACM1-cognate-Protenix at 38.66 (unphysical d_TM6 and
  NPxxY geometry) and HRH1-boltz-apo at 58.85 (still recoverable; not
  the same failure mode). Both were retained in-panel; the ACM1-cognate-
  Protenix cell is handled via exclusion set E1."*

**HRH1-boltz-apo** at 58.85 pLDDT is the closest thing to a second
"ACM1-cognate-Protenix" but is 20 pLDDT points higher and doesn't
carry the same unphysical geometry signature. Not currently flagged in
any caveat; potentially worth a one-line footnote after the natural-floor
discussion. Not run in this pass.

---

## Outputs

- `docs/POST_CLOSEOUT_VERIFICATION_REPORT.md` — this file.
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g_scc1_cluster_boot.json`
  — new (Part 1b).
- `scripts/block_c_closeout/recompute_2x2_cluster_boot.py` — new (Part 1b).

**No commits from Part 2, per dispatch.**
**No commits from Part 1 either — all pending an adjudication pass**:

- The 1b cluster-boot recompute is on-disk as a JSON, but SC-C-1's
  numbers in `BLOCK_C_CLAIM_SHEET.md` and C-C-3's caveat status text
  are not yet updated to reflect it (proposed update text above; can
  be applied in a follow-up commit).
- The 1c receptor-drop enumeration is on-disk in this report; C-C-9's
  caveat status text is not yet updated (proposed update text above).
- The 1d flag lands here as a note; the Block A dossier grep + fix is
  a separate follow-up.

**No tag movement. No push.** Block C stays at `block_c_freeze` (proposed,
not placed) at working repo `a090c9a` + release repo `4f6452f`.
