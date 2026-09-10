# ASSUMED-NOT-VERIFIED — Block D

Items on which Block D's dispatches demanded verification that the
executed passes did not accomplish. Recorded so future readers can
distinguish "claim based on verified data" from "claim resting on
plausible-looking proxies or scope-limited execution."

Consolidated from `EXPERIMENT_DOSSIER_BLOCK_D.md §Section 4 (caveats)`
+ `BLOCK_D_S2_4_POST_CUTOFF_SCOPING.md §Uncertainties` + Part A/D2
§Reference-predicate calibration. This file is the canonical
enumeration.

---

## OF3 training cutoff — TBD in the anchor CSV

**Claim in dispatch**: `refs/nanobody_state_anchors.csv` columns
`cutoff_chai_2021_01_12`, `cutoff_protenix_2021_09_30`,
`cutoff_boltz2_2023_06_01`, `cutoff_of3_TBD` — OF3's training cutoff
was not established when the D2 anchors were curated (2026-09-06).

**What was actually done**: 3-of-4 backbone cutoffs pinned; OF3 left as
`TBD`. All four D2 Nb-anchor PDBs (5JQH 2016, 6VI4 2020, 4MQS 2013,
6OS2 2019) predate the earliest confirmed cutoff (Chai-1 2021-01-12);
whether they also predate OF3's cutoff is not verified.

**What was NOT done**: OpenFold-3-preview release-notes lookup to
confirm the training-data cutoff date. Likely mid-2024 or earlier
based on release timing, but this is inference, not verified fact.

**Consequence for §2.4 post-cutoff test**: PDB 9HB3 (primary
post-cutoff test candidate per v2 §2.4 scoping, deposited 2024-11-05)
clears Chai-1 / Protenix / Boltz-2 unambiguously (17 months margin
past Boltz-2). Whether it clears OF3 depends on OF3's actual cutoff.
If OF3 saw entries deposited after 2024-11-05, the disambiguation
test would not discriminate for OF3 alone — but the test would still
discriminate for the other three backbones. 5-minute doc lookup
pending adoption. WebFetch attempts on aqlaboratory / openfold.readthedocs.io
returned no cutoff info in this pass.

---

## Reference-predicate calibration on Nb-anchor TM6-tilt axis — deferred

**Claim in dispatch (§3 D2 addition)**: apply the two-instrument
predicate (NPxxY-OH < 9.082 Å AND TM6 tilt > 14.932 Å) to each of
the 4 D2 receptors' deposited active AND inactive reference PDB
structures — confirming the instrument classifies references correctly
before F3 rests on it.

**What was actually done** (per Part A/D2 §3): the pre-existing
references in `refs/reference_set.csv` calibrate correctly on both
axes for all 4 receptors (ADRB2/4LDE, ADRB2/5JQH, ACM2/4MQS,
AGTR1/6OS2, OPRK/6VI4 active + existing inactives). Nb-anchor PDBs
(5JQH/4MQS/6VI4) fetched from RCSB and scored directly on NPxxY-OH:
ACM2/4MQS active PASSES at 4.21 Å; ADRB2/5JQH inactive FAILS at
11.16 Å; OPRK/6VI4 inactive FAILS at 12.88 Å — all as expected.

**What was NOT done**: TM6-tilt (`d_gpcrdb_tm6_tilt_246_637_ca`)
computation on the Nb-anchor PDBs. Requires GPCRdb 2×46 / 6×37
residue-position mapping for each of the 3 Nb-anchor PDBs — small
compute (~ 30 min) but not run in this pass.

**Consequence**: F3's negative finding (SC-D-6: inactive-Nb
unreliable) rests on NPxxY-OH calibration passing on the Nb-anchor
PDBs, which it does. TM6-tilt calibration is the second half of the
same instrument; residual chance that TM6-tilt would flip a
verdict is low but not zero. Named as C-D-9.

---

## MOR curation status for §2.4 test — CLOSED, not pursued (closeout dispatch)

**Status**: the post-cutoff-inactive-Nb test was closed as attempted-and-documented at the Block D closeout (2026-09-10), not dispatched. The three items below were the pre-dispatch checks that would have been required had 9PXU been adopted; they are explicitly not pursued and do not remain pending verification. Retained here for the audit trail of what a future revisit would need.

The full search record + candidate-by-candidate disposition + reusable filter rule now lives at `dossiers/BLOCK_D/BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`.

**Items that would have needed verification for 9PXU dispatch (not pursued for this manuscript)**:
1. **8EFQ BW-anchor completeness on the MOR chain** — whether 8EFQ's 367-aa MOR resolves the 3.50 / 5.58 / 6.30 / 6.34 / 7.53 BW-anchor residues the scorer's pocket-Cα-RMSD path expects.
2. **9PXU BW-anchor completeness + fusion-chain boundary parsing** — 9PXU contains a single 622-aa fused chain (BRIL + MOR + Nb6), requiring verified residue-boundary parsing before use as a two-chain prediction input.
3. **OF3 training cutoff** — still `TBD`. External release-notes lookup pending.

**References found on the way** (retained in case revisit picks this up):
- `refs/reference_set.csv` grep for human OPRM1 (P35372) → no entry; only mouse OPRM at 4DKL (P42866, tier4_sidebar, training_cutoff_verified=NO). Do not reuse mouse ref for human MOR test.
- 8EFQ RCSB metadata verified 2026-09-10 — human OPRM1 P35372 ✓, DAMGO agonist, Gi cognate heterotrimer, Cell 2022 cryo-EM. Valid human MOR active reference if the test is ever picked up.

**Historical note (v2 candidate 9HB3/V2R — retracted)**: v2 scoping promoted 9HB3 (Vasopressin V2 receptor + "Mambaquaretin1") on novelty grounds. Retracted — the 141-aa VHH-shaped chain I labelled "Mambaquaretin1" was the anti-BRIL-Fab fiducial-Nb from a standardised cryo-EM scaffolding toolkit; actual Mambaquaretin1 is a 57-residue Kunitz-fold peptide toxin from mamba venom. Same fiducial-Nb error hit v2 backups (9EKH/9EE5 DP1, 9EHS A3R). All four disqualified. Filter rule captured in `BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`.

**Consequence for §2.4 cost**: unchanged from v1 (~600 preds
compute, ~1.5-day wall, ~2–3 h curation ceremony because MOR active
reference 8EFQ + MOR inactive reference 9PXU + Nb6_9PXU sequence are
all new to the campaign).

---

## MCHR1 D3 ligand_rmsd_to_ref reconciliation — CLOSED but retained for audit trail

**Claim in dispatch**: GATE-4 flagged 990 rows of MCHR1 D3 populated
with `ligand_rmsd_to_ref` values; D3 is apo-only so this shouldn't
have fired.

**What was actually done in Part-A-D3**: fresh compute on the on-disk
`experiments/024_tier_d3_msa_depth/analysis/full/rows.csv` showed 100
% NaN on `ligand_rmsd_to_ref` across all 25,810 rows.

**Reconciliation in this pass (2026-09-10)**: empirical recount
confirms 25,810/25,810 NaN. **GATE-4's 990 claim is retracted**;
Part-A-D3 stands. Bug #4 (`9e640d5`) `NOT MATERIAL` verdict is unaffected
because both readings converge: the ligand path never fires on D3.

**Consequence**: C-D-11 downgraded from active caveat to
closed-reconciliation note. Retained here for the audit trail. No
downstream impact.

---

## D3 Chai + OF3 190-pred shortfall — not investigated

**Claim in dispatch**: 26,000 preds dispatched, 25,810 landed. 190
short: Chai 90 + OF3 100.

**What was actually done**: the 190 deltas were counted (Chai 6,410 +
OF3 6,400 vs Boltz/Protenix 6,500 canonical) and concentrated on
shallow-depth cells. Reported cell-level fractions use actual landed
denominators.

**What was NOT done**: root-cause investigation of the specific
(bb × depth × receptor × seed × sample) cells that dropped.
`experiments/024_tier_d3_msa_depth/analysis/full/rescore_parallel.provenance.json`
records the rescore's 100 % pass on landed rows but does not
enumerate the 190 predictions that never landed.

**Consequence**: 0.73 % coverage loss, distributed unevenly. Named as
C-D-6. Cell-specific footnote where n is quoted; no re-run planned.

---

## AGTR1 × active_nb × OF3 30-row shortfall — not investigated

**Claim in dispatch**: 200 preds per cell canonical; AGTR1 × active_nb
× OF3 landed 170.

**What was actually done**: OF3 stragglers killed after ~3 h of no
progress (per `tier_d2_full_headline_2026_09_07.md`). Reported
fraction uses n=170.

**What was NOT done**: OF3 straggler root-cause diagnosis (Triton
error? MSA rebuild? memory pressure?). No re-fire attempted.

**Consequence**: cell-specific 15 % coverage loss on one cell only.
Named as C-D-5. Manuscript sentences quoting AGTR1 active_nb OF3
figures need a footnote.

---

## D1 dip-test panel-scale — technically informative on OPSD × OF3 only

**Claim in dispatch (§D-1.4 secondary)**: Hartigan's dip test + GMM
k-mode fit on 4 continuous axes per (receptor × backbone) — 112 cells
total.

**What was actually done**: 2 of 112 cells signed dip_p < 0.05 AND
BIC-selected GMM k=2 — both on OPSD × OF3 (d_tm6, pocket_ca_rmsd_active).
§D-1.7 kill fires on the "two continuous basins" claim.

**What was NOT done**: extending the dip test to Block A or D3 data
to check whether OPSD × OF3 is a persistent two-basin cell across
tiers. Small compute; not run.

**Consequence**: main-text two-basin claim dropped (W-D-8);
Discussion appendix note on OPSD × OF3 as the single-cell signal
that survives. Whether OPSD × OF3 is a robust two-basin cell
cross-tier is unresolved.

---

## Kickoff Q5 stretch — cross-tier F1 reproducibility on Block B and Block C

**Claim in dispatch**: kickoff Q5 stretch — does F1 (receptor-specific
backbone-active-outlier pattern) reproduce beyond Block A?

**What was actually done in Part A/D1**: F1 reproduces on Block A
independent data at n=25/cell (all 4 outliers: Chai on CNR2/OPSD/ADRB2,
OF3 on LPAR1, ≥+50-pt delta). Robust cross-tier finding on Block A.

**What was NOT done**: cross-check on Block B (partner-selection) or
Block C (Tier 3 pharmacology) data. These would have different arm
designs (Block B has cognate/shuffled/decoy; Block C has agonist/decoy/antag)
so the analysis needs a per-block methodology — not the direct grep
that worked on Block A's apo arm.

**Consequence**: F1's cross-tier robustness is verified on Block A;
extension to B/C is inferred but not empirically checked. Named as
kickoff Q5 stretch, deferred. SC-D-11 rests on Block A cross-check.

---

## Backbone-training-cutoff × D-tier: full 204 candidate deep-dive

**Claim in §2.4**: 204 GPCR + nanobody structures deposited after
2023-06-01 (Boltz-2 cutoff) via RCSB search.

**What was actually done (v2 revision, 2026-09-10)**: FULL 204-candidate
metadata pull completed after the v1 primary (9PXU) was demoted. Local
filtering surfaced: primary 9HB3 (V2R + Mambaquaretin1) + companion
9HAP (V2R + tolvaptan + Mambaquaretin1) + backups 9EKH/9EE5 (DP1 +
ONO-antagonist + Nb) + 9EHS (A3R + LUF7602 + Nb). Not-recommended:
9W3F (identical Nb60), 9YFU (orphan + hinge-Nb), 9LMO/9JFU (orphan),
8TH4 (AGTR1 already in D2 + cousin-Nb).

**What was NOT done**: (a) BW-anchor completeness verification on 9HB3
V2R chain, (b) V2R Gs cognate reference lookup in refs/reference_set.csv,
(c) OF3 training cutoff confirmation via external release notes,
(d) mechanism verification on 9EKH/9EE5's Nb (chaperone vs
state-directing anchor), (e) synthetic-construct homology check on
Mambaquaretin1 against training-corpus VHH library.

**Consequence**: 9HB3 is the recommended primary target. If BW-anchor
completeness (b) or Gs cognate (c) checks fail, fall back to 9EKH/9EE5
(DP1) with Nb-mechanism verification (d) first. If all named
candidates fail, 9PXU remains a last-resort fallback with cousin-Nb
transfer caveat explicit.

---

## Rebuild-and-diff harness — deferred (parity with Block A/B/C)

**Claim in dispatch (parity with Block A/B/C VERSION.md)**: a
release-level rebuild script that re-runs D1/D2/D3 analyses from
`data/block_d/{d1,d2,d3}/rows.csv` and diffs against the shipped
verification outputs.

**What is on disk**: `analysis/block_d/scripts/derive_d3_slopes.py` (this
pass, reproduces GATE-2). No end-to-end `rebuild_block_d.py`.

**What was NOT done**: implementing a Block D rebuild script that
regenerates all SC-D-N numbers from the raw rows. Same status as
Block A / Block C rebuild-and-diff. Only `make ledger-check` runs
today.

**Consequence**: scientific correctness of any SC-D-N claim's number
is NOT end-to-end verified by the release-repo's automated tools.
Reviewer must inspect the analysis outputs directly. Named in
`VERSION.md §"Rebuild-and-diff harness — deferred, tracked"`.
