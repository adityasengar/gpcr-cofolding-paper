# BLOCK C — MANUSCRIPT FLAGS

Flags that the figure agent, prose agent, or a reviewer will need to
respect. These are NOT withdrawals or caveats — they are load-bearing
scope decisions and framing conventions that persist across figures.

## Flag C-1 — Cluster-bootstrap is authoritative for Block C

Every CI in `BLOCK_C_CLAIM_SHEET.md` uses cluster-boot over paralog
clusters (Block A C-8 convention). Receptor-boot is the secondary
statement. Row-boot is invalid.

**For the S1 15-set specifically**: 12 clusters. The mapping is
receptor-name-verbatim from `experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`
(reconstructed 2026-09-09).

**Any panel/figure quoting a CI must name cluster-boot in the caption**,
along with cluster count and seed.

## Flag C-2 — Abstract-number scope: Boltz + Protenix

The manuscript's classifier-AUROC headline is **scoped to Boltz + Protenix**
under the cluster-boot convention (see SC-C-4). Chai and OF3 point
estimates clear the pre-registered KILL-S1 threshold (≥ 0.65), but
their cluster-boot 95 % CIs span 0.5 and cannot be distinguished from
chance. Both formulations must appear together — the point estimate
survives the pre-registered test, the interval does not.

**Two-line prose template**: *"The single-structure classifier reaches
pooled LORO AUROC 0.852 on Boltz and 0.825 on Protenix (cluster-bootstrap
95 % CI [0.560, 0.974] and [0.528, 0.960]); the same test is inconclusive
on Chai (0.706 [0.351, 0.941]) and OpenFold-3 preview (0.656 [0.382,
0.924]) under the cluster-bootstrap convention."*

## Flag C-3 — Continuous readout, not binary predicate

Ligand-identity discrimination in Block C is reported on
**continuous pocket-Cα-RMSD**, not on the Block A / Block B binary
two-instrument predicate. The predicate is floor/ceiling-saturated in
Block C (SC-C-6). No Block C figure or table quotes a binary-predicate
"active fraction" for a ligand-class discrimination claim.

## Flag C-4 — AGTR1 is a curation-scope outlier, not a metric outlier

AGTR1 inverts on all 4 backbones. The root cause is not a mechanical
scorer defect (per `docs/AGTR1_REFASSIGN_REPORT.md` §2 — no swap, no
mapping error, both refs pass the two-instrument predicate on their
labels). **AGTR1's active reference (6OS2) is unique in the S1 15-set:
β-arrestin-biased-agonist (TRV026) + intracellular nanobody, no
Gα-pathway construct** (per `docs/G2_REFERENCE_HOMOGENEITY.md` §2, count 1/15).

The manuscript should:
1. Report AGTR1's inversion as-scored.
2. Report the excluded-AGTR1 sensitivity result (SC-C-5's flat slope).
3. Name the reference-curation reason for the exclusion, not just
   "AGTR1 was an outlier".
4. Give AGTR1 its OWN footnote separate from CXCR2 — the mechanisms
   differ (parity with Block B's five-independent-footnote treatment
   of AA2AR — `docs/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md`).

## Flag C-5 — CXCR2 (OF3 only) is a backbone-specific outlier

CXCR2 inverts on OpenFold-3 preview only (AUROC 0.135) — Boltz 0.900,
Chai 0.928, Protenix 0.999. CXCR2's active reference (6LFO) is a
canonical native Gi heterotrimer — no reference-curation anomaly.
This is a **backbone-specific failure mode** whose mechanism is not
addressed by G2. Manuscript should name CXCR2's OF3-only inversion
as a separate finding from AGTR1's four-backbone inversion; the two
have different mechanisms.

## Flag C-6 — Pose section: scope is 6.93 %, not 42 %

The manuscript's pose-accuracy claim is **scoped to OF3 + Protenix ×
neutral-antagonist × input-bound-pdb == reference-pdb (n = 4,500)**
at `ligand_rmsd_to_ref < 3 Å` = 6.93 %. Corpus-wide MCS-fixed pose
statistics on the sibling corpus (`rescore_t7c_full/rows.csv`) show
per-receptor bimodal distributions with Boltz median 54–56 % on
neutral-antagonist redock — reported as a companion observation, but
the headline stays scoped. Pooling across receptors hides bimodality
(§SC-C-7).

**Coverage asymmetry**: agonist rows ~50 % NaN on `ligand_rmsd_to_ref`,
antagonist rows ~93–97 % covered. Not MAR — chemistry-and-matcher
correlated. Any corpus-wide pose statement quotes the coverage
imbalance.

## Flag C-7 — Two scorer commits in Block C corpora

Two distinct scorer_git_sha values appear in Block C's on-disk data:
- **Primary corpus** (`rows.tier3.v2.csv`, classifier + 2×2 interaction):
  scorer `3d9c6faae59b5aa5881994dee4d36e36ea5367da`.
- **Pose corpus** (`rescore_t7c_full/rows.csv`, T7c post-fix pose accuracy):
  scorer `d9c646af5f89861c16062bf256de96a8389d9915`.

Every manuscript sentence citing a pose number must cite the pose
corpus explicitly; every classifier or interaction sentence must cite
the primary corpus. Do not conflate.

**Note**: `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/T7C_POST_FIX_HEADLINE.md`
cites scorer `891041e858f3747b…` in prose. That string does not match
the row-level `scorer_git_sha` column value (`d9c646af…`) — documentation
drift. **The row-level value is authoritative**; the prose headline
needs a correction pass at manuscript-editing time.

## Flag C-8 — Panel of record vs landed panel

40 Class A receptors dispatched (per PREREG §1 v2 + Block C dispatch
contract). **36 receptor_slugs landed** in `rows.tier3.v2.csv`. Every
manuscript sentence saying "40 Class A" needs a Methods footnote naming
the 4 that did not land, or a change to "36 landed of a 40-receptor
panel of record". See SC-C-9 + C-C-9.

## Flag C-9 — Tier 1 retired, Tier 3 authoritative

Block C's live data is Tier 3 (40,800 rows, 40-receptor Class-A panel).
Tier 1 (8-receptor pilot, ~14,800 preds) is retired per two citable
records:
- Manuscript §Withdrawn item #9 in `docs/BLOCK_C_PAPER_DRAFT_v1.md`.
- Auto-memory `block_c_tier3_pocket_identity_2026_09_06` header line
  ("SUPERSEDES block-c-tier1-headline-2026-09-04").

Tier 1 data files still exist under
`experiments/020_block_c_tier1_ligand/` for provenance-audit purposes.
Release-repo state: `release/data/block_c/tier1/` → `release/_internal/`.

## Flag C-10 — Reference-routing label vs resolution

Row-level `pocket_ref_role_inactive` DIFFERS by ligand class
(`generic_inactive_fallback` for full_agonist + decoy_lig; `inactive_neutral_antagonist`
for neutral_antagonist). But the RESOLVED PDB SHA is **identical across
ligand classes per receptor** for every receptor in the S1 set. Any
Methods sentence about "role-specific reference routing" needs to say
the label routes but the resolution collapses. See SC-C-10 and C-C-10.

## Flag C-11 — G2d, G4, G5, G7, G6b — recorded-not-followed

Five deliverables the dispatch listed but this pass did not complete:
- **G2d** (fold-integrity 10-receptor subset draw test): the
  fi_finite_receptors list is not in `check2_fi_finite_subset.json`;
  requires re-run.
- **G4 full CIF ligand-centroid census** (40,800 CIFs; off-site
  fraction). Estimated cost ~5–10 h compute. A minimal G4 sample
  (best/worst/inverted CIFs per backbone) lands in
  `release/structures/block_c/`; the full census does not.
- **G5 full reference-predicate calibration** (168 refs × NPxxY + tilt
  per-ref). Partial audit landed (Bug #2 firing on 10 refs; agonist_only
  count = 3). Full per-ref two-instrument evaluation deferred.
- **G6b fast-path match-count row-level detail** (how many of the
  2,300 Boltz + Chai fast-path rows have exactly 5 tuple matches vs
  ≥ 6). Manifest column absent.
- **G7 orthogonal corroboration** (pocket-lining side-chain contact
  fingerprint classifier). Design proposal in gating report; not
  implemented.

Manuscript should NOT depend on any of these; each has a Discussion
sentence if the reviewer asks.

## Flag C-12 — Cluster-boot CI on the 2×2 interaction NOT recomputed

SC-C-1's 2×2 interaction values (Boltz −0.306, Chai −0.137, OF3 −0.252,
Protenix −0.184 Å) are reproduced from the post-audit
`stage3_2x2_ligand_state_specificity.json`. **Cluster-boot 95 % CI on
the 2×2 interaction under Block A C-8's convention was not recomputed
in this closeout pass** — the JSON's CI is receptor-boot. Before
manuscript submission, rerun the cluster-boot CI on the 2×2 interaction
and update the SC-C-1 table accordingly. Not blocking Part B / Part C
because the point estimates are unchanged, but the CI convention needs
alignment.

## Flag C-13 — β-arrestin-biased-agonist reference as a Discussion sentence

AGTR1's biased-agonist active reference (6OS2 + TRV026 + Nb.AT110i1_le)
opens a Discussion sentence about a class of active states the current
scorer's `resolved_state = Ga-coupled-active` schema does not
distinguish. The `stabilising_elements` field on AGTR1's row IS accurate
(`nanobody_beta_arrestin_biased_agonist`); the `resolved_state` label is
imprecise. A future scorer schema change would add
`resolved_state ∈ {Ga-coupled-active, biased-agonist-active,
partial-agonist-active}` as separate values. **Recorded-not-followed**;
noted in the manuscript's Methods appendix as a schema-limitation
paragraph.
