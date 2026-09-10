# block_c_figure_data.zip — v2 (post-verification refresh)

**Generated**: 2026-09-10 (after BLOCK_C_WRAP_v2 dispatch).
**Zip source**:
- paper_af3 working repo HEAD (see commit landing this bundle)
- paper_af3_release HEAD (see commit landing this bundle)

**Scope**: everything a figure agent / prose agent needs to build
Block C's Results, Limitations, and Methods, INCLUDING the corrected
off-site-fraction census (v2) and the retraction of the v1 25.6 %
figure. Tidy data only; **no PNG / PDF / SVG**.

## Supersedes

- **`1394405acbdfbd79b7f51f7bc3c1f885b8c02063c262b3491044c8de3b0de501`** —
  `block_c_figure_data.zip` v1 (built pre-post-closeout-verification,
  missing cluster-boot CIs on the 2×2 interaction and missing the G4
  census). **Do not use v1.** Delete if held.
- **Any pre-audit Tier 1 headline export** on disk — Block C Tier 1 is
  retired (W-C-9). If you find a `block_c_tier1_*.zip` or similar in a
  workspace, it is superseded by this bundle. No such file appears in
  the working repo or release repo today; the notice is for
  reviewer-side workspaces.

## Provenance pins

- **Primary corpus** rows.tier3.v2.csv SHA-256:
  `5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103`.
- **Pose sibling corpus** rescore_t7c_full/rows.csv scorer_git_sha:
  `d9c646af5f89861c16062bf256de96a8389d9915`.
- **Block B E4 pocket-Cα ref-sep table** SHA-256:
  `ed8505771108beec1be739d12802d253b93a0dc3f5429b50bf85d065c53b57cb`.
- **Reference set** (blockb_pinned; Block C uses the same):
  `6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`.

## What's new vs the v1 bundle (invalidated)

1. **`06_2x2_interaction/g_scc1_cluster_boot.json`** — cluster-boot CIs
   on SC-C-1's 2×2 interaction (Block A C-8 authoritative convention).
2. **`12_g4_off_site_census/`** — corrected full-corpus centroid census
   (40,000 rows). The v1 scoped census (25.6 % pooled) is retracted; see
   `11_manuscript_narrative/BLOCK_C_WRAP_REPORT.md` §SUPERSEDED for the
   retraction record.
3. **`13_structures/`** — 7 targeted + 7 random CIF selection rules +
   MANIFEST (actual CIFs at `release/structures/block_c/`).
4. **`11_manuscript_narrative/POST_CLOSEOUT_VERIFICATION_REPORT.md`** +
   **`POST_VERIFICATION_CLOSEOUT_REPORT.md`** — reports covering §1a
   rebuild-harness fix, §2 cluster-boot recompute, §5a C-11 exclusion
   sensitivity (1.78× enrichment vs corrected 17 % random-baseline).
5. **Caveats C-C-3 and C-C-9**: status RESOLVED 2026-09-10.
6. **Caveats C-C-11 + C-12** extended (deferred-rebuild item;
   pLDDT-floor-at-60 Methods sentence).

## Load-bearing numbers (post-verification)

- **SC-C-1 2×2 interaction, cluster-boot 95 % CI** (16 paralog clusters):
  Boltz [−0.454, −0.164]; Chai [−0.216, −0.045]; OF3 [−0.405, −0.099];
  Protenix [−0.277, −0.088]. All 4 sign non-zero.
- **SC-C-4 S1 LORO classifier, cluster-boot 95 % CI** (12 clusters):
  Boltz 0.852 [0.560, 0.974]; Chai 0.706 [0.351, 0.941]; OF3 0.656
  [0.382, 0.924]; Protenix 0.825 [0.528, 0.960]. Scoped to Boltz +
  Protenix (Chai + OF3 CIs cross 0.5).
- **G4 off-site rate (v2, corrected)**:
  - Apo arm: **15.1 %** (95 % CI [14.6, 15.6]).
  - Cognate arm: **20.3 %** (95 % CI [19.8, 20.9]).
  - Small-molecule apo × {agonist, antag} (SC-C-1's numerator): **1.52 %**.
    Not material for SC-C-1.
  - Peptide-agonist "off-site" median centroid 17.5 Å — extracellular
    vestibule binding by biology, not a docking failure.
  - Chai residual far-mode: 175 rows ≥ 60 Å (1.7 % Chai-specific tail).

## Bundle index

| directory | files | content |
|---|---:|---|
| `01_claims/` | 2 | SC-C-1..SC-C-10 claim sheet (cluster-boot primary) + 13 flags |
| `02_caveats/` | 12 | C-C-1..C-C-11 + README |
| `03_withdrawals/` | 11 | W-C-1..W-C-10 + README |
| `04_classifier/` | 2 | G1 bootstrap + S1 LORO JSON |
| `05_ref_separation/` | 4 | G2 + G2-excl-AGTR1 + Block B E4 pocket-Cα table |
| `06_2x2_interaction/` | 2 | Stage 3 2×2 JSON + cluster-boot recompute |
| `07_ordinal_recovery/` | 1 | S5 P4 JSON |
| `08_confidence_signal/` | 1 | S3 consensus JSON |
| `09_references/` | 4 | reference_survey + summary + AGTR1 refassign + G2 homogeneity |
| `10_pose_accuracy/` | 3 | T7C headline + T7b + Task E v3 scoped |
| `11_manuscript_narrative/` | 8 | state check, gating, POST_CLOSEOUT_VERIFICATION, POST_VERIFICATION_CLOSEOUT, BLOCK_C_WRAP (retracted), SIGNAL_RECOVERY, PREREG_SIGNAL_RECOVERY, paper draft v1 |
| `12_g4_off_site_census/` | 3 | full census JSON + per-row CSV + census script |
| `13_structures/` | 2 | targeted+random selection MANIFEST + README |

## Reproduction

```
unzip -l /Users/SENGAAD1/Documents/claude/paper_af3/block_c_figure_data.zip
sha256sum /Users/SENGAAD1/Documents/claude/paper_af3/block_c_figure_data.zip
```
