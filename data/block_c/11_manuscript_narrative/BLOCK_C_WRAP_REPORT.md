# BLOCK C WRAP — STOPPED at §1(b): material off-site fraction

**⚠️ SUPERSEDED 2026-09-10 by `docs/BLOCK_C_WRAP_REPORT_v2.md`.**

**Retraction**: this report claimed a pooled off-site fraction of **25.6 %**
based on a scoped 600-row stratified sample. That number is retracted.

**Reason**: the v1 census script
(`scripts/block_c_closeout/g4_scoped_centroid_census.py`) identified the
receptor chain by "longest polymer chain ≥ 200 aa". On cognate-arm rows,
Gα (~394 aa) is a polymer chain — for any receptor shorter than Gα
(CXCR4=352, 5HT5A=357, CNR2=360, HRH1, DRD2/3, most Class A), v1 picked
Gα as "the receptor". The pocket-Cα centroid was then computed at
nonsense positions on Gα, giving 60–82 Å distances from the actual
ligand. All 5 "bad dock" cases in the 10-row sanity sample were this
bug. Every one flipped to in-pocket or pocket-adjacent under a correct
receptor-chain picker (v2: chain that carries Cα atoms at the receptor's
own named anchor positions from `refs/reference_set.csv`).

**Corrected numbers** (full-corpus census v2, 40,000 rows, HPC 9 min):

| statistic | v1 (SUPERSEDED) | v2 (SUPERSEDED figure notwithstanding, this is the correct one) |
|---|---:|---:|
| pooled off-site fraction | 25.6 % (600 rows) | **17.7 %** (40,000 rows) |
| **apo-arm off-site** | not broken out | **15.1 %** |
| **cognate-arm off-site** | not broken out | **20.3 %** |
| SC-C-1 relevant (apo × {agonist, antag}, small-molecule only) | not broken out | **1.52 %** (149/9800) |

**Adjudication**: not material for SC-C-1 or SC-C-4. See
`docs/BLOCK_C_WRAP_REPORT_v2.md` for details.

**Retained here** as an audit-trail record — the retraction is part of
the ledger.

---

**Original report follows (retracted). Do not use the 25.6 % figure.**

---

**Date**: 2026-09-10.
**Baseline**: paper_af3 working repo `a233563` + paper_af3_release `f404729`.
**Dispatch**: BLOCK C WRAP §1–§4 + §5 output.

**Verdict on the dispatch's hard stop condition**:

> §1(b): "If it comes back material (i.e. large enough to change how any
> surviving Block C claim should be read), STOP and report rather than
> proceeding to §2 — that would be a claim-facing finding, not a
> packaging detail."

**§1(b) TRIGGERED. STOPPED.** §2 (targeted + random CIF samples), §3
(bundle refresh), §4 (tag placement) are all HELD pending user
adjudication of the §1 finding.

---

# §1 — G4 scoped stratified centroid census — RESULT: MATERIAL

## §1a — sampling rule (as executed)

**Strata**: 12 = 4 backbones × 3 ligand_roles.
**Per stratum**:
- 40 rows random-sample (seed 20260910) from Class-A `passed=True` rows.
- Up to 10 additional rows enriched for matcher-failure signals (rows
  whose `pocket_notes` contains `no_atom_match` or `no_ref_ligand`).
- Achieved n per stratum: **50 rows uniformly** (all strata had ≥ 10
  enriched candidates available).
- Total sample: **600 rows**.

**Metric**:
- Predicted CIF → find receptor chain (longest polymer, ≥ 200 STD_AA).
- Compute pocket-anchor-Cα centroid from the 12 BW pocket anchors
  (3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, 6.51, 6.52, 6.55, 7.39,
  7.42; same set as `scorer/pocket_metrics.py::POCKET_BW_LABELS`).
- Find HETATM ligand candidates in any chain (excluding lipids, waters,
  metals, buffers, glycans); pick the largest by heavy-atom count.
- Compute ligand-heavy-atom centroid.
- Distance = Euclidean between centroids.

**Binning** (matches scorer/pocket_metrics.py Bug #2 tripwire's 8 Å):
- `in-pocket`: < 8 Å
- `pocket-adjacent`: 8–15 Å
- `off-site`: ≥ 15 Å

**Execution**: `~/software/venvs/pipeline-tools/bin/python` on basel-hpc
(gemmi 0.7.5). Rows.tier3.v2.csv rsynced to HPC scratch. CIFs read from
`/hpc/scratch/sengaad1/paper_af3/experiments/021_block_c_tier3_pharmacology/tier3/pool/…`
directly. **Wall time: 10.5 s** (well inside the 1-hour budget — CIF
loading is fast per row when done in-place on HPC).

## §1b — result

### Pooled

| statistic | value |
|---|---:|
| total rows sampled | 600 |
| measurable (has HETATM ≥ 5 heavy atoms) | 497 |
| unmeasurable (`no_ligand_hetatm`) | 103 |
| in-pocket (< 8 Å) | 311 (62.6 % of measurable) |
| pocket-adjacent (8–15 Å) | 59 (11.9 %) |
| **off-site (≥ 15 Å)** | **127 (25.6 %)** |
| **off-site 95 % CI (Wilson)** | **[21.9 %, 29.6 %]** |

### Per-stratum

| backbone × role | n | in-pocket | adj | off-site | unmeas | off-site frac | note |
|---|---:|---:|---:|---:|---:|---:|---|
| **chai × decoy_lig** | 50 | 16 | 6 | **24** | 4 | **52.2 %** | worst |
| protenix × neutral_antag | 50 | 25 | 10 | 15 | 0 | 30.0 % |  |
| chai × full_agonist | 50 | 18 | 2 | 8 | 22 | 28.6 % | ligand-peptide unmeas |
| of3 × full_agonist | 50 | 17 | 1 | 7 | 25 | 28.0 % | ligand-peptide unmeas |
| boltz × neutral_antag | 50 | 29 | 7 | 14 | 0 | 28.0 % |  |
| of3 × decoy_lig | 50 | 29 | 5 | 13 | 3 | 27.7 % |  |
| chai × neutral_antag | 50 | 34 | 4 | 12 | 0 | 24.0 % |  |
| protenix × decoy_lig | 50 | 33 | 2 | 11 | 4 | 23.9 % |  |
| boltz × decoy_lig | 50 | 26 | 13 | 11 | 0 | 22.0 % |  |
| of3 × neutral_antag | 50 | 33 | 7 | 10 | 0 | 20.0 % |  |
| boltz × full_agonist | 50 | 27 | 2 | 2 | 19 | 6.5 % | ligand-peptide unmeas |
| **protenix × full_agonist** | 50 | 24 | 0 | 0 | 26 | **0.0 %** | ligand-peptide unmeas |

### Distance distribution (measurable rows)

- Q25 = 4.6 Å, median = 6.9 Å, Q75 = 18.6 Å, max = 81.7 Å.
- **Bimodal**: a large in-pocket cluster (< 10 Å) and a heavy off-site
  tail (up to 81 Å). Off-site rows are far outside the pocket — some
  60–80 Å away, suggesting the ligand docked at the extracellular
  surface, or in the Gα region on cognate-arm rows, or at some other
  distant site.

### Where the off-site fraction is largest

**Small-molecule ligands (decoy_lig, neutral_antagonist)** — always
measurable (0–4 unmeasurable per stratum):
- **decoy_lig pooled** (any backbone): 59 off-site of 189 measurable =
  **31.2 %**. Chai is the worst (52.2 %).
- **neutral_antagonist pooled**: 51 off-site of 200 measurable = **25.5 %**.
  Protenix worst (30.0 %); OF3 lowest (20.0 %).

**Full-agonist ligands** — mixed picture:
- 20 off-site of 108 measurable = **18.5 %**.
- 92 rows unmeasurable (46 % of the 200 full_agonist rows sampled)
  because the agonist is a peptide chain (not a HETATM ≥ 5 heavy atoms)
  on most receptors. Peptide agonists at 40 Class-A receptors include
  most of the neuropeptide receptors (GRPR, LPAR1, NPY-family, EDNRB,
  etc.); my HETATM-based measurement doesn't handle them. **The 18.5 %
  off-site is a LOWER BOUND** for full_agonist arms.

## §1(b) verdict — MATERIAL

Applied strictly to the dispatch's criterion — "large enough to change
how any surviving Block C claim should be read" — the answer is yes:

- **SC-C-1** (2×2 pocket-Cα-RMSD interaction): the interaction is
  computed by comparing predicted pocket-Cα against reference pocket-Cα.
  If 25 % of rows have the input ligand parked outside the pocket
  entirely, the "pocket geometry differentiates agonist from
  antagonist" claim is measured PARTLY on rows where the receptor is
  responding to a ligand that isn't in its pocket. The 2×2 interaction
  may still sign non-zero, but the reader needs the caveat "on rows
  where the ligand is in the pocket, and on rows where it isn't, in
  ~25 % / ~75 % proportion".
- **SC-C-2** (P4 ordinal on Δ = pocket_ca_rmsd_active − inactive):
  same concern. The ordinal recovery on the continuous axis may be
  driven partly by pocket-geometry effects that don't correspond to
  ligand-in-pocket physics.
- **SC-C-4** (S1 LORO classifier): pocket-Cα features across rows with
  and without the ligand in the pocket. If off-site rows have
  systematically different pocket geometry (unfolded, less
  constrained), the classifier may be picking up on that rather than
  ligand-class-specific pocket shape.
- **SC-C-7** (pose accuracy 6.93 % on OF3+Protenix × neutral_antag ×
  ref-matched): this claim already restricts to ref-matched rows, which
  likely coincide with in-pocket rows (a matched-reference ligand pose
  implies the ligand IS in the pocket). SC-C-7 is likely LEAST
  affected; but corpus-wide pose statements need the off-site fraction
  named alongside coverage asymmetry (C-C-8).
- **SC-C-5** (applicability domain — empirical failure list): the
  off-site fraction is another lens on the failure list. **Chai on
  decoy_lig at 52 % off-site** and **all four backbones at 20–30 %
  off-site on neutral_antag** together read as a systematic failure
  mode that the applicability paragraph should name.

**Applied per-backbone**, Chai is materially worse than the other three
on decoy_lig arm (52 % vs 22–28 %). Boltz + Protenix have the cleanest
pockets on their measurable-full-agonist subsets (6.5 % and 0 %). This
adds a backbone-specific note to C-C-2 (Chai softness).

## §1(c) — was it "not material"? — NO

Per dispatch §1(c): "If not material, record the number in `caveats/`
as the empirical bound, note that it rests on a stratified sample
rather than the full census, and continue."

The 25.6 % pooled + up-to-52 % per-stratum reading is not a
"small empirical bound"; it is a first-order finding. **Not the §1(c)
path.**

## Caveats on the measurement (before adjudication)

1. **Peptide-agonist rows are unmeasurable under my HETATM-based
   heuristic.** 92 of 200 full_agonist rows sampled fell into
   `no_ligand_hetatm`. For those receptors, the "ligand" is a polymer
   chain (a peptide agonist). A full analysis would treat those chains
   as ligands and compute the peptide's centroid. Not done in this pass.
   Effect on full_agonist off-site fraction: my 18.5 % is a lower
   bound (measurable subset only).
2. **My HETATM picker takes the largest by heavy-atom count.** For
   cognate-arm rows, if the prediction happens to place a HETATM
   larger than the intended ligand (unlikely in typical AF3-family
   outputs, since they don't add cofactors), the "ligand centroid"
   could be the wrong atom set. Spot-check of ~5 off-site rows shows
   distances of 27–74 Å — clearly outside any pocket-adjacent region,
   consistent with actual off-site placements rather than picker
   errors. Aggregate pattern robust.
3. **`no_ligand_hetatm` may reflect peptide OR failed prediction** —
   AF3-family predictions occasionally omit ligands entirely. Not
   attempting to distinguish here; both fail the "ligand in pocket"
   criterion.

None of these three caveats change the sign of the 25 % finding — they
suggest my number is likely a slight UNDERCOUNT (peptide-agonist rows
counted as "unmeasurable" rather than "in-pocket").

## Outputs from §1 on disk

- **HPC**: `~/paper_af3/experiments/021_block_c_tier3_pharmacology/analysis/verification/g4_scoped_centroid_census.{json,csv}`.
- **Working repo** (rsynced back):
  `experiments/021_block_c_tier3_pharmacology/analysis/verification/g4_scoped_centroid_census.json`
  (structured summary — per-stratum, pooled, sampling rule, binning).
- **Working repo**:
  `experiments/021_block_c_tier3_pharmacology/analysis/verification/g4_scoped_centroid_census.csv`
  (600 rows: input_path, backbone, role, arm, receptor, distance_A, note).
- **Working repo**: `scripts/block_c_closeout/g4_scoped_centroid_census.py`.

## Outputs from §1 to sync to release/ (proposed — NOT done here)

Pending user adjudication (see §4 below).

---

# §2 — targeted + random CIF samples — HELD

Not started. Reason: §1(b) STOP.

If the user adjudicates that the off-site fraction does NOT require
claim-facing rewrites (e.g., "restrict the SC-C-1 wording to acknowledge
the 25 % off-site tail but keep the signed non-zero conclusion"), then
§2 proceeds as designed. If the user adjudicates that claim rewrites
ARE needed, §2's selection rules should be redesigned to include
in-pocket vs off-site subsets as a stratification axis, and the wrap
becomes a bigger delivery.

---

# §3 — refresh writing bundle — HELD

Not started. Reason: §1(b) STOP.

The writing bundle would need to include the §1 census result no
matter what direction the adjudication goes. Given that direction
affects the framing of SC-C-1, SC-C-2, SC-C-4, and SC-C-7 wording, the
bundle refresh is downstream of that decision.

Pre-existing zip SHA on disk (still valid as-of-2026-09-10-morning):
`1394405acbdfbd79b7f51f7bc3c1f885b8c02063c262b3491044c8de3b0de501`
(`block_c_figure_data.zip`, per `artefacts/block_c_figure_data_manifest.md`).

**Superseded exports on disk to invalidate** (per dispatch §3f):
- Pre-audit / Tier 1 headline exports: NOT located on disk in this pass.
  A grep + find sweep did not surface any earlier `block_c_*.zip` under
  `artefacts/` or `paper_af3_release/`. The current
  `block_c_figure_data.zip` is the first Block C export.
  **State plainly**: if the user's own workspace has an earlier Block C
  export from any audit round or Tier 1 draft, it is superseded and
  must not be used.
- Pre-audit dossier files under
  `experiments/021_block_c_tier3_pharmacology/analysis/verification/STAGE_POST_AUDIT_REPORT_v1..v4.md`:
  superseded by v5 + the post-closeout reports. Retained on disk for
  provenance only.

---

# §4 — tag — NOT PLACED

`block_c_freeze` NOT placed. Reason: §1(b) STOP; the state that would
be tagged (with off-site-fraction unresolved) is not the state the
manuscript should ship from.

**Working repo commits**: `a233563` is the current tip (post-verification
closeout). This commit already carries the C-C-3 / C-C-9 RESOLVED
updates and the rebuild-harness truth-in-labeling changes. A §1-only
commit is landing now (with this report + the census artefacts +
census script).

**Release repo commits**: `f404729` is the current tip. Three unpushed
commits sit on top of `block_a_freeze`: `a01d774` + `f62811c` (Block B)
+ `4f6452f` (Block C closeout) + `f404729` (post-verification). §1-only
commit will add one more.

## §4(c) — Block B tag: OPEN ITEM

Per dispatch: the Block B tag is unplaced on paper_af3_release.
Two Block B unpushed commits (`a01d774` + `f62811c`) sit above
`block_a_freeze`. No `block_b_freeze` tag has been placed on the
release repo. The working repo has `block_b_final` at `c237120` but
that is on the working repo, not the release repo.

**Proposed action** (deferred here — reported for adjudication):
- Place `block_b_freeze` on paper_af3_release at `f62811c` (the tip
  before Block C's `4f6452f`).
- Or place `block_b_freeze` at `f62811c` alongside the Block C
  work — same commit-graph point since Block C's `4f6452f` is a Block C
  commit not a Block B rerun.

Not done here; reported as open item.

---

# §5 — this file

`docs/BLOCK_C_WRAP_REPORT.md` (working repo).

**No tag movement. No push.**

Local commit landing:
- `docs/BLOCK_C_WRAP_REPORT.md`
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g4_scoped_centroid_census.json`
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g4_scoped_centroid_census.csv`
- `scripts/block_c_closeout/g4_scoped_centroid_census.py`

Release repo: no changes this pass (would carry the census artefacts
and structures/block_c/ update after adjudication).

---

# Awaiting user adjudication

Three questions for the user:

1. **Is 25.6 % pooled off-site material enough to require SC-C-1 /
   SC-C-2 / SC-C-4 rewrites?** The point estimates in those claims
   are on all measurable rows, not on an in-pocket subset. Reading
   options:
   - **(A)** Scope the claims to "rows where the ligand is in the
     pocket" — requires filtering the primary corpus by a
     centroid-distance threshold and recomputing SC-C-1, SC-C-4 CIs.
     Recompute is straightforward once the ligand-centroid distance
     is a column in the corpus (my current census only has 600 rows;
     a full-corpus centroid measurement would be needed).
   - **(B)** Keep the claims as-is, add a caveat naming the 25 %
     off-site fraction as a scope limit. Requires only a new C-C caveat
     and updates to the SC-C-N qualifier lists.
   - **(C)** Withdraw one or more of SC-C-1 / SC-C-4 pending the full
     centroid recompute.

2. **Should the full-corpus centroid measurement fire?** ~40,800 CIFs
   at 10.5 s / 600 rows extrapolates to ~12 min on HPC (essentially
   free). If yes, add `d_ligand_centroid_to_pocket_A` as a corpus
   column and recompute SC-C-1 CIs both on the full corpus and on the
   in-pocket subset. This would fold cleanly into the dispatch's §2 CIF
   sample if the adjudication is option (A).

3. **Does the Block B tag get placed in this pass, or await a Block B
   dispatch?**

Not adjudicating any of the three here. Reporting the census and
stopping.
