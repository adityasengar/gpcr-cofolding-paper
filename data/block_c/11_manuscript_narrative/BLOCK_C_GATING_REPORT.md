# BLOCK C — GATING REPORT

**Date**: 2026-09-10.
**Baseline**: `block_b_final` (`c237120`) + STATE_CHECK at `docs/BLOCK_C_STATE_CHECK.md`.
**Scope**: Part A gates G1–G7 of the Block C closeout dispatch.
**Rule**: report evidence, do not adjudicate; status is set outside this
dispatch.

---

## Verdict at a glance

**Gate NOT clear.** Three of the five section-4 stop conditions are met:

1. **G1**: CI on the abstract number Chai and OF3 both cross 0.5 on
   receptor-boot AND cluster-boot; Boltz's `~0.85` figure does not
   survive receptor-boot (lower bound 0.64). *(hard-stop condition #1)*
2. **G2**: applicability-domain claim changes — the reference-separation
   → AUROC hypothesis is refuted. AGTR1 sits at pocket-Cα-sep rank 39/40
   (top of range) and inverts fully on all four backbones. Slopes are
   NEGATIVE (opposite of predicted direction). No a-priori threshold
   emerges. *(hard-stop condition #2)*
3. **G3**: reference routing did not effectively fire — all 28 receptors
   with defined `pocket_ref_pdb_sha_inactive` have IDENTICAL SHAs across
   all ligand_roles. `pocket_ref_role_inactive` labels differ
   (`generic_inactive_fallback` vs `inactive_neutral_antagonist`), but
   the resolved PDB is the same per receptor.
   *(hard-stop condition #3)*

G4 (structural + ligand placement census) and G7 (orthogonal
corroboration) are **recorded-not-followed** — with three hard-stop
conditions triggered, further expensive analyses are deferred until the
user adjudicates. G5 (reference-predicate calibration on Block C refs)
is a scope statement rather than a triggered gate; a partial audit lands
in this report.

**Not proceeding to Part B (release commit) or Part C (writing bundle)
in this run.** Status: awaiting adjudication.

---

## G1 — Receptor-boot + cluster-boot CI on S1 AUROC

**Baseline number under test** (from `s1_loro_classifier.json`, KILL-S1
row × F_iii × apo × self-ref-excl):

| backbone | published pooled AUROC (JSON, N=1) |
|---|---:|
| boltz | 0.852 |
| chai | 0.706 |
| of3 | 0.656 |
| protenix | 0.825 |

**Bootstrap results** (this session; `experiments/021_block_c_tier3_pharmacology/analysis/verification/g1_bootstrap_s1_auroc.json`):

*Note*: G1's independent re-run of the observed pooled AUROC reproduces
the JSON's point estimates to 3 decimals (Boltz 0.852, Chai 0.706, OF3
0.656, Protenix 0.825). The bootstrap median differs from the point
estimate because bootstrap resamples receptors with replacement, which
shifts the median relative to the observed AUROC on the fixed 15-set.

| backbone | obs | receptor-boot median | receptor-boot CI 95 | cluster-boot CI 95 | perm null CI 95 | CI 95 crosses 0.5? |
|---|---:|---:|---|---|---|---|
| boltz | 0.852 | 0.809 | [0.636, 0.970] | [0.560, 0.974] | [0.477, 0.520] | NO (cluster-boot lower 0.560) |
| chai | 0.706 | 0.626 | [0.364, 0.935] | [0.351, 0.941] | [0.473, 0.523] | **YES** (0.351 < 0.5) |
| of3 | 0.656 | 0.626 | [0.369, 0.898] | [0.382, 0.924] | [0.467, 0.525] | **YES** (0.382 < 0.5) |
| protenix | 0.825 | 0.769 | [0.539, 0.971] | [0.528, 0.960] | [0.469, 0.527] | NO (cluster-boot lower 0.528 — barely) |

Cluster-boot n_clusters = 12 (mapping from Block B's `paralogy_clusters.csv`).
Bootstrap iterations: 500 receptor-boot, 500 cluster-boot, 200 permutation
null per backbone.

**G1 observed pooled AUROC values match the JSON** to 3 decimal places
(Boltz 0.852, Chai 0.706, OF3 0.656, Protenix 0.825). The earlier
mismatch noted in the STATE_CHECK draft was a stale-log artefact from
mid-run; the finalized run reproduces the JSON's point estimates.

**Hard-stop assessment**:

- **Boltz cluster-boot [0.560, 0.974]**. CI does NOT cross 0.5, but
  the lower bound (0.560) is well below the manuscript-cited point
  estimate (0.852) — the receptor-boot median 0.809 is closer to the
  bottom of a wide interval than to the ceiling. The "~0.85" narrative
  weight does not survive when the interval is presented alongside.
- **Chai cluster-boot [0.351, 0.941]**. **Interval SPANS 0.5.** Chai's
  Class-C-no-selfref-apo × F_iii AUROC is not distinguishable from
  chance under the pre-registered cluster-boot convention (Block A's
  C-8). The permutation null upper bound is 0.523; the observed 0.706
  is nominally above null, but the sampling distribution reaches down
  to 0.351.
- **OF3 cluster-boot [0.382, 0.924]**. **Interval SPANS 0.5.** Same
  interpretation as Chai. The KILL-S1 pre-registered threshold (≥ 0.65)
  was cleared by the point estimate; the cluster-boot lower bound
  slips well beneath it.
- **Protenix cluster-boot [0.528, 0.960]**. CI just excludes 0.5.
  Marginally above chance under the cluster-boot convention.

**Bootstrap unit convention**: cluster-boot is authoritative
(Block A C-8, honoured in Block B). Cluster map uses 12 clusters over
the 15-receptor S1 set (mapping in
`g1_bootstrap_s1_auroc.json.per_backbone.<bb>.cluster_boot.cluster_map_receptor_to_cluster`).
Fewer clusters than Block B's 26-over-40 because S1's set is smaller.
Receptor-boot is secondary and reported alongside for parity.

**Permutation null**: 200 draws per backbone, ligand-class labels
shuffled WITHIN receptor, full LORO pipeline re-run each draw. Null
CIs are all tight around 0.50 (as expected).

**HARD-STOP condition #1: YES.** Chai and OF3 CIs cross 0.5 on both
receptor-boot AND cluster-boot. Boltz's `~0.85` figure has a
cluster-boot lower bound at 0.56 — the point estimate is a wide
interval away from 0.85. Under the pre-registered
"cluster-boot authoritative" convention, the abstract number's
strength collapses from four-backbone-signed to *marginal on
Boltz + Protenix only*.

## G1 methodological note

The G1 bootstrap resamples RECEPTORS (or CLUSTERS) with replacement
and re-runs LORO within each drawn set. This departs from
receptor-permutation-null-only (S1's original evaluation, which held
the receptor set fixed and shuffled labels within receptor). Both
tests answer different questions:
- Permutation-null-only: is the observed AUROC greater than chance,
  given THIS receptor set? Yes on all four backbones — the p_perm
  values in the JSON are ~0 with 5-permutation resolution.
- Bootstrap CI: how much does AUROC vary if the receptor set is
  slightly different? Answered here: substantially. On Chai and OF3
  the sampling distribution reaches below 0.5.

The two answers are complementary, not contradictory. The manuscript
should carry BOTH numbers.

## G2 — Reference separation vs per-receptor AUROC

**Full output**: `experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_refsep_vs_auroc.json`
+ `.csv`.

**Data joined**: per-receptor AUROC (from `s1_loro_classifier.json`
variant `C_no_selfref_apo` × F_iii) × pocket-Cα separation (from
`experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv`,
Block B E4-adjacent O-3 output, SHA `ed850577…`). All 15 S1 receptors
are in the pocket-Cα table.

### G2a — Regression per backbone (AUROC ~ pocket_ca_sep, n=15)

| backbone | slope (AUROC per Å) | slope CI 95 (receptor-boot) | Spearman ρ | R² | bimodal fraction (≥ 0.85 or < 0.30) |
|---|---:|---|---:|---:|---:|
| boltz | −0.278 | [−0.752, +0.080] | −0.297 | 0.182 | 0.933 |
| chai | −0.239 | [−0.840, +0.196] | −0.247 | 0.085 | 0.667 |
| of3 | −0.491 | [−1.010, −0.008] | −0.319 | 0.292 | 0.667 |
| protenix | −0.292 | [−0.900, +0.162] | −0.093 | 0.156 | 0.867 |
| **pooled** | **−0.325** | **[−0.571, −0.064]** | −0.206 | 0.162 | 0.783 |

**Direction of slope**: NEGATIVE on all four backbones. The hypothesis
predicted POSITIVE — that small pocket-Cα separation would collapse the
Δ feature to ~0 and drop AUROC. Observed slopes go the other way.

**Slope CI**: only OF3's per-backbone CI excludes zero (barely). Pooled
slope excludes zero, but the pooled model treats the 4 backbones as
independent replicates, which they are not.

**R² on all backbones ≤ 0.30.** Whatever mechanism drives bimodality,
pocket-Cα reference separation is not it.

### G2b — Applicability-domain threshold

**No clean threshold on any backbone.** No pocket-Cα-sep value τ exists
such that median AUROC(receptors with sep ≥ τ) ≥ 0.85 AND zero
inversions remain. Reason: AGTR1 sits at pocket-Cα-sep 1.87 Å (rank
39/40 in the Block B panel — 2nd largest), and it inverts fully on all
four backbones (AUROC 0.00–0.10). Any threshold that excludes AGTR1
must exclude every receptor with larger separation too — leaving no
receptors on the high-sep side.

### G2c — AGTR1 counterexample (dispatch-mandated test)

Dispatch: *"AGTR1 is well separated on the tilt axis (19.09 vs 11.23)
and still inverts. Does it fit on the pocket-Cα metric or break the
account?"*

**Numbers**:
- AGTR1 pocket_ca_sep = **1.87 Å** (rank **39/40** in Block B panel,
  percentile ~93 % in the S1 15-set).
- AGTR1 Δ_ref_tilt = 7.86 Å (large).
- AGTR1 Δ_ref_npxxy = −6.02 Å (large-magnitude).
- Per-backbone AUROC on AGTR1: boltz **0.100**, chai **0.000**,
  of3 **0.000**, protenix **0.000**.

**Verdict**: **AGTR1 BREAKS the pocket-Cα account.** AGTR1 has one of
the largest reference separations in the entire panel across all three
axes (pocket-Cα, tilt, NPxxY), and yet it is the most severely
inverted receptor on all four backbones. The hypothesis was that small
reference separation drives inversion (Δ feature collapses); AGTR1
inverts at LARGE reference separation on every axis. Whatever drives
AGTR1's inversion, it is not reference-separation.

### G2d — Fold-integrity 10-receptor subset draw test

**Not resolved in this pass.** `check2_fi_finite_subset.json` was
scanned; no `fi_finite_receptors` list was found in the recognised
schema keys. G2's `fold_integrity_check_2_test` field in the JSON output
returns empty. **Recorded-not-followed**: build the FI-finite 10-recep
list from Check 2's actual output and repeat this draw test in a
separate pass.

**HARD-STOP condition #2: YES.** Applicability-domain claim changes:
what the manuscript currently frames as "reliable on 14/15 receptors,
AGTR1 catastrophic + CXCR2 on OF3" becomes an EMPIRICAL failure list
that does not lift to an a-priori criterion. The specific reference-
separation hypothesis is refuted.

## G3 — Reference routing reconciliation

**Three findings under reconciliation**:
1. Re-audit found antagonist rows routing to `pocket_ref_role_inactive
   = inactive_neutral_antagonist`.
2. Check 1 found the resolved-reference PDB SHA IDENTICAL across
   ligand_role classes on all 23 receptors.
3. `block_b_worker.sh` (reused for tier 3) does not emit
   `_rerun_plan.json`.

**G3a — Reference-PDB SHA per receptor, per ligand_role**:

For each of the 36 receptors in the Class-A landed corpus:
- **`pocket_ref_pdb_sha_active`** has **1 distinct value per receptor**
  (28 receptors) or 0 (8 receptors with all-NaN — no active PDB
  resolved). **No receptor has more than one distinct SHA.**
- **`pocket_ref_pdb_sha_inactive`** has **1 distinct value per receptor**
  (36 receptors) or 0 (0). **No receptor has more than one distinct SHA.**

Extended check: **for the 28 receptors with defined
`pocket_ref_pdb_sha_inactive`, is the SHA the SAME across `ligand_role`
subsets?** Answer: **28/28 identical, 0/28 differ**.

**G3b — Role-label vs role-resolution divergence**:

`pocket_ref_role_inactive` VALUES observed:
- `decoy_lig` rows: `generic_inactive_fallback` (11200 rows) + NaN (3200).
- `full_agonist` rows: `generic_inactive_fallback` (11200 rows) + NaN (3600).
- `neutral_antagonist` rows: `inactive_neutral_antagonist` (11600 rows,
  0 NaN).

The label DOES differ by ligand_role (agonist/decoy → `generic_inactive_fallback`;
antag → `inactive_neutral_antagonist`). But the resolved SHA is the
SAME for each receptor across roles. Interpretation: for these
receptors, the "generic inactive fallback" AND the
"inactive_neutral_antagonist" resolve to the SAME PDB entry. The
role-specific routing logic ran but produced no differentiation.

**G3c — Hypothesis verdict**:

Dispatch's hypothesis: *"role-specific routing never fired, every row
fell through to the generic reference, and that is WHY Check 1 passed."*

**PARTIAL SUPPORT.** More precisely:
- The role-specific routing produced DIFFERENT LABELS across
  ligand_roles (evidence: `pocket_ref_role_inactive` differs), which
  means the routing logic executed.
- But the routing LABELS all resolved to the SAME PDB per receptor
  (evidence: `pocket_ref_pdb_sha_inactive` is 28/28 identical across
  roles). This is the collapse the dispatch anticipated.
- Check 1's SHA-identical result is TRUE, and it is TRUE because the
  routing collapsed to one PDB per receptor. Check 1's finding
  correctly documents the state; it does NOT establish that a proper
  role-specific curation would produce the same finding.

**G3d — Two consequences (dispatch asks these be reported separately)**:

**(i) Classifier consequence**: S1's feature Δ = `pocket_ca_rmsd_active
− pocket_ca_rmsd_inactive` is computed against a per-receptor pair
(one active PDB + one inactive PDB) that is identical for every
ligand_role on that receptor. Therefore Δ carries NO class-identity leak
via the reference PDB — Boltz/Chai/OF3/Protenix all get the same targets
per receptor, and Δ becomes a pure per-prediction feature. **Classifier
is clean.** Reference-identity leak is ruled out by construction, not by
audit.

**(ii) Pose consequence**: `ligand_rmsd_to_ref` for a NEUTRAL_ANTAGONIST
input row scores the predicted ligand against a reference PDB whose
bound ligand is the antagonist / inverse agonist — a like-for-like
comparison. But **`ligand_rmsd_to_ref` for a FULL_AGONIST input row
scores the predicted ligand against a reference PDB whose bound ligand
is either the antagonist (if the inactive-side reference was used) OR
the agonist bound in the active reference (if active-side reference).**
Which target the scorer selects for the agonist rows requires reading
the scorer source. In either case: for at least ONE ligand class,
`ligand_rmsd_to_ref` is being computed against a chemically different
ligand than the input row's ligand — a chemistry mismatch that guarantees
non-zero RMSD unrelated to prediction quality. **This affects the pose
section, not the classifier.**

**HARD-STOP condition #3: YES.** G3 establishes that reference routing
did not effectively fire — the labels differ but the resolved PDBs
collapse to one per receptor.

## G4 — Structural + ligand placement census

**Recorded-not-followed.** Rationale: three hard-stop conditions already
triggered (G1, G2, G3). The full-corpus ligand-centroid census requires
loading and parsing 40,800 CIFs (~5–10 hours single-threaded plus
cluster-Cα computation). Deferring this cost until adjudication is
complete.

**Design (for a fresh dispatch)**:
1. For each row's `input_path`, load the predicted CIF via `gemmi.read_structure`.
2. Parse HETATM candidates; pick the largest by scorer's rule.
3. Compute ligand centroid.
4. Compute pocket-anchor centroid from receptor Cα at 12 BW positions
   (3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, 6.51, 6.52, 6.55, 7.39,
   7.42) via `scorer/pocket_metrics.py`'s existing routine.
5. Emit `d_ligand_centroid_to_pocket_A` per row.
6. Bin: {< 5 Å inside}, {5–10 Å near}, {10–15 Å margin}, {≥ 15 Å off-site}.
7. Cross-tabulate off-site fraction by (backbone × ligand_role × arm).
8. If off-site fraction is material (dispatch heuristic: ≥ 5 % per
   backbone per class), restate G1 and G2 on the on-site subset before
   Part B.

**Manuscript sentence at stake**: *"whether the pocket-geometry claim
holds on all rows or only on rows where a ligand is actually in the
pocket."* — deferred to fresh dispatch.

**Structural inspection at CIF grain (dispatch item 4a-b, 4d)**: also
deferred. The dispatch calls for pulling CIFs for the best, worst, and
two mid-range cells per backbone, plus at least one AUROC≈1.000 receptor
and one AUROC≈0 receptor (CNR2 or AGTR1). Render for visual inspection.
Not started.

## G5 — Reference-predicate calibration on Block C refs

**Partial audit — full calibration is recorded-not-followed.**

**What was checked** (from `signal_recovery_2026_09_07/reference_survey.csv`,
168 references, SHA in G5 output):

| item | value |
|---|---|
| total refs | 168 |
| active-role refs | 95 |
| inactive-role refs | 73 |
| refs with `status=OK` (HETATM found) | 126 (75 %) |
| refs with `status=NO_HETATM_CANDIDATES` | 42 (25 %) — 37 active, 5 inactive |
| Bug #2 firing rate (scorer's largest-HETATM pick ≠ pocket-plausible candidate) | 10 / 126 (7.9 %) |
| active stabilization split (n=95 active) | native 64, mini_G 17, chimera 7, nanobody 3, agonist_only 3, DVL_DEP 1 |
| resolved inactive states | inactive-antagonist 54, inactive-inverse-agonist 12, inactive-neutral-antagonist 5, inactive-full-length 1, inactive-apo 1 |

**What is recorded-not-followed**: the actual two-instrument calibration
per reference. Block A ran NPxxY_OH < 9.082 AND tilt > 14.932 on each
of its 89 references and found agonist-only actives fail NPxxY by
construction. Doing the equivalent for Block C's 168 refs requires
parsing each reference PDB, computing the two instruments, and
tabulating pass/fail. Not attempted here. Approx cost: 168 × PDB parse
+ 2 metric computations ≈ 30–60 min compute.

**Preliminary observations** (from surveys alone):
- **42 refs have no HETATM candidates** (25 %) — most (37/42) are
  active-role. Interpretation: many active refs are G-protein-bound
  without a co-crystallised orthosteric ligand, so the HETATM filter
  finds nothing acceptable.
- **Only 3 refs are `active_stabilization_source=agonist_only`** — the
  category Block A flagged as failing NPxxY by construction. This is
  a much smaller share than Block A's set had. If the calibration
  fires, it fires on a small fraction.
- **Bug #2 fires on 10 refs (5.3 % active, 6.8 % inactive)** — the
  scorer's HETATM pick doesn't match the pocket-plausible candidate.
  These 10 refs are candidates for the scoped Methods sentence about
  reference-side curation limits.

## G6 — Matcher path and coverage

**Full output**: derivations below reference on-disk state; no separate
JSON emitted (the numbers below suffice for adjudication).

### G6a — Matcher path distribution

Read `pocket_ligand_atom_map_method` from
`experiments/021_block_c_tier3_pharmacology/rescore_t7c_full/rows.csv`
(scorer `d9c646af…`, the post-Bug-#2/#3 corpus).

| matcher method | n rows | notes |
|---|---:|---|
| `mcs` | 14,415 | MCS ≥ 6 atoms |
| `atom_name_element` (fast-path) | 10,500 | 5-atom name coincidence risk |
| `mcs_too_small` | 3,085 | MCS found < 6 atoms; NaN returned |
| NaN | 12,800 | no matcher path succeeded |

**Per-backbone × method**:

| backbone | mcs | atom_name_element | mcs_too_small | NaN |
|---|---:|---:|---:|---:|
| boltz | 4,333 | 1,800 | 867 | 3,200 |
| chai | 5,426 | 500 | 1,074 | 3,200 |
| of3 | 2,325 | 4,100 | 575 | 3,200 |
| protenix | 2,331 | 4,100 | 569 | 3,200 |

### G6b — Fast-path wrong-not-NaN risk

The fast-path `atom_name_element` matches by `(atom_name, element)`
tuples. For OF3 and Protenix, ligand atom names follow CCD convention,
so name-matching is intended. For Boltz and Chai, ligand names are
SMILES-derived, so name-matching between predicted and reference is
coincidence-dependent. The risk mode: coincidental ≥ 5 (atom_name,
element) tuple matches return a numeric RMSD that is not the
correspondence the chemistry demands.

**Fast-path row counts on Boltz + Chai (the wrong-not-NaN risk zone)**:
Boltz **1,800 rows**; Chai **500 rows**. **Total 2,300 rows**, ~5.6 % of
the corpus.

The dispatch asks how many of these have ≥ 5 (atom_name, element)
matches (the "wrong not NaN" trap). The `pocket_ligand_atom_map_method`
column records the path taken (`atom_name_element`), but the
match count per row is not exposed as a column. Deriving it requires
either rescoring or reading the scorer's per-row provenance sidecar.
**Recorded-not-followed.** However, since the fast-path only succeeds
when ≥ 5 tuples match (per scorer source: `_min_matched=5` threshold
before falling back to `mcs_too_small`), the 2,300-row upper bound is
effectively the population — every fast-path row on Boltz/Chai passed
the 5-tuple threshold. Whether the correspondence is chemistry-correct
requires row-by-row inspection (out of scope here).

### G6c — Does matcher path affect pocket_ca_rmsd or only ligand RMSD?

**Answer from scorer source (`scorer/pocket_metrics.py`)**: pocket
residues are defined by 12 FIXED BW positions (3.32, 3.33, 3.36, 5.42,
5.43, 5.46, 6.48, 6.51, 6.52, 6.55, 7.39, 7.42). BW anchors are
receptor-side; the pocket-Cα RMSD is computed on receptor Cα atoms
aligned to the reference receptor via Kabsch, using a fixed anchor set.
**The matcher path is a ligand-side computation and does NOT enter
`pocket_ca_rmsd` at any step.** The S1 classifier features
(`pocket_ca_rmsd_active`, `pocket_ca_rmsd_inactive`, and their delta)
are UNAFFECTED by the matcher path. Only `ligand_rmsd_to_ref` and other
ligand-side metrics inherit the matcher path.

**Consequence**: the pose-section limitation is scoped to `ligand_rmsd_to_ref`.
The classifier and 2×2 pocket-Cα interaction claim are NOT touched by
G6.

### G6d — Coverage by backbone × role × arm

`ligand_rmsd_to_ref` NaN rate per (backbone × ligand_role) from
`rescore_t7c_full/rows.csv`:

| backbone | full_agonist NaN | neutral_antag NaN | decoy_lig NaN |
|---|---:|---:|---:|
| boltz | 51.4 % | 6.9 % | 54.6 % |
| chai | 54.1 % | 6.9 % | 57.6 % |
| of3 | 48.5 % | 3.4 % | 52.2 % |
| protenix | 48.6 % | 3.4 % | 52.0 % |

**Coverage confirms the ~50 %-agonist vs ~93 %-antagonist asymmetry**
the dispatch cited. Antagonist rows cover ~93–97 % (NaN 3–7 %); agonist
and decoy rows cover ~46–52 %.

**Is the missing structure at random?** From cell-level counts: the NaN
rows on agonist/decoy cluster on backbones whose ligand naming is
SMILES-derived AND for which the MCS matcher does not find ≥ 6 atoms.
This is a chemistry-and-matcher artefact, not random. **Not MAR
(missing at random)** — missingness is chemistry-correlated. Any
pooled pose-accuracy statistic ignores the asymmetry.

**Manuscript sentence at stake**: the pose-section limitation. The
pocket-Cα-RMSD classifier claim is NOT touched (per G6c).

## G7 — Orthogonal corroboration

**Recorded-not-followed.** Rationale: with G1, G2, G3 already
triggering hard stops, and given G7 requires (a) proposing a novel
metric independent of the three classifier features, (b) implementing
its scorer, (c) running it on the on-disk CIFs — the cost is
substantial and the marginal information is small if the classifier is
being downgraded.

**Design (for a fresh dispatch)**:
Candidate signature: **pocket-lining side-chain contact fingerprint**.
For each row's predicted CIF:
- Enumerate side-chain heavy atoms within 4.5 Å of the ligand centroid
  from the 12 BW pocket positions.
- Encode as a 12-bit vector (position i lit if any side-chain heavy
  atom of the residue at BW position i is within 4.5 Å of the ligand
  heavy atoms).
- Compare fingerprints per (agonist, antag) pair per receptor via
  Hamming distance.
- Per-receptor LORO AUROC on fingerprint-based classifier.

This measure is independent of pocket_ca_rmsd (which is Kabsch on Cα)
and pocket_sidechain_rmsd (which is Cα-Cβ + rotamer). If a per-receptor
AUROC on the fingerprint tracks the pocket-Cα-RMSD AUROC, the shape
claim has independent support. If it does not track, the manuscript's
"pocket-shape claim" has no independent corroboration and the
Discussion should say so.

Not run. Cost: ~30–60 min if scorer routine is written; ~half a day if
implemented from scratch.

**Manuscript sentence at stake**: *"whether the pocket-shape claim has
independent support."*

---

## Consolidated hard-stop analysis

| section-4 condition | this session's evidence | triggered? |
|---|---|---|
| G1 CI changes headline number's status (backbone crosses 0.5 OR ~0.85 does not survive) | Chai and OF3 CIs cross 0.5 on both boot conventions; Boltz's ~0.85 cluster-boot lower bound is 0.56 | YES |
| G2 changes applicability-domain claim in either direction | Slope NEGATIVE (not positive); AGTR1 sits at rank 39/40 pocket-Cα-sep AND inverts fully on all 4 backbones; no a priori threshold exists | YES |
| G4 material off-site fraction requiring G1/G2 restatement | not run | UNKNOWN |
| G3 establishes reference routing did not fire | 28/28 receptors have identical `pocket_ref_pdb_sha_inactive` across all `ligand_role` values; the label routes but the resolution collapses | YES |
| Any surviving claim in current claim set changes status | see Deltas below | see Deltas |

**Three of the four evaluable conditions triggered.** G4 unevaluated.

---

## Deltas to the manuscript claim set

Ordered by manuscript-impact.

1. **S1 classifier's abstract number needs a confidence interval.**
   Manuscript v1 §Abstract cites 0.85 as the S1 AUROC on Boltz without
   an interval. G1's cluster-boot CI on Boltz is [0.56, 0.97], which
   does not sit centred on 0.85. Chai and OF3 CIs cross 0.5. Either:
   (a) the abstract's classifier claim is stated with the interval,
   which changes its rhetorical weight (from "~0.85 AUROC" to "0.85
   [0.56, 0.97] on Boltz, with Chai and OF3 not distinguishable from
   chance under bootstrap"); or (b) the claim is scoped to Boltz alone
   with the interval; or (c) the claim is withdrawn.

2. **Applicability domain is empirical failure list, not an a priori
   criterion.** The reference-separation hypothesis is refuted (§G2).
   The manuscript's future-work paragraph should NOT claim
   "reference-separation predicts failure"; the empirical list
   (AGTR1 inverts on all 4 backbones; CXCR2 on OF3) stays.

3. **Reference-identity leak was ruled out by construction, not by
   audit.** §G3. Manuscript's Methods currently frames Check 1's
   SHA-identical finding as an anti-leak audit; the correct framing is
   that role-specific routing was designed to differentiate refs
   between ligand_roles but resolved to the same PDB per receptor, so
   Check 1's SHA-identity is expected rather than earned. This is a
   Methods-sentence fix, not a Results claim change.

4. **Pose-section limitation named.** §G3 + §G6d. For at least ONE
   ligand class per row, `ligand_rmsd_to_ref` is being computed against
   a chemically different ligand (agonist vs antagonist), which
   guarantees a floor RMSD unrelated to prediction quality. Combined
   with the missingness asymmetry (agonist/decoy ~50 % NaN, antag
   ~93 % coverage), the pooled 6.93 %-at-<3 Å number scoped to OF3 +
   Protenix × neutral_antag × ref-matched stays defensible AS SCOPED
   in the manuscript's current wording, but corpus-wide pose statements
   need the caveat.

5. **Bootstrap-unit convention statement missing on Block C.**
   Block A + Block B state cluster-boot as authoritative. Block C's
   audit reports currently mix receptor-boot and (in one case) row-boot
   labels. Any Block C CI in the manuscript needs cluster-boot naming.

6. **Panel size of record vs landed.** State check found 36 of 40 Class
   A receptors landed in `rows.tier3.v2.csv`. Any "40-receptor" language
   in the manuscript needs a dispatch-vs-landed disambiguation.

---

## Recorded-and-not-followed

Per the hard-scope rule, everything not delivered but relevant:

1. **G4 full CIF ligand-centroid census** (40,800 CIFs; ligand centroid
   vs BW pocket centroid; off-site binning; on-site restatement of G1
   + G2 if material).
2. **G4 structural inspection sample** (best/worst/mid CIFs per backbone
   plus near-1.000 and inverted receptors; visual render).
3. **G5 full reference-predicate calibration** (two-instrument predicate
   on each of 168 Block C references; per-ref method / resolution /
   fusion / bound-ligand table).
4. **G6b fast-path match-count row-level detail** (how many of the
   2,300 Boltz + Chai fast-path rows have exactly 5 tuple matches;
   the "1–4 spurious" case if it exists in the corpus).
5. **G7 orthogonal corroboration** (pocket-lining side-chain contact
   fingerprint classifier).
6. **G2d fold-integrity 10-receptor subset draw test** (whether Check 2's
   subset is drawn disproportionately from the low-separation mode).
7. **Rescore-to-post-fix-scorer for the classifier** (primary corpus
   `rows.tier3.v2.csv` uses scorer `3d9c6fa…`; pose corpus
   `rescore_t7c_full/rows.csv` uses scorer `d9c646af…`; running the
   classifier on the post-fix corpus was not done in this pass).
8. **`T7C_POST_FIX_HEADLINE.md` scorer-SHA prose vs column mismatch**
   (`891041e858f3747b…` in prose vs `d9c646af…` in column — documentation
   drift, not a scientific finding).
9. **Cluster-map coverage on the 15-receptor S1 set** (mapping to
   12 clusters via Block B's paralog table; report the mapping and
   whether any singleton clusters distort bootstrap variance).

---

## Not proceeding to Part B / Part C

With three hard-stop conditions met, Part B (release/ commit) and Part C
(writing bundle) are held. Part B would tag `block_c_freeze` on a state
that has open adjudication questions on the abstract number, on the
applicability domain, and on the reference routing — landing that tag
on origin would encode a status that has not been set. Standing
convention is: never move a pushed tag, so any tag placed prematurely
is durable.

Awaiting adjudication.

---

## Outputs

- `docs/BLOCK_C_STATE_CHECK.md` (Section 0)
- `docs/BLOCK_C_GATING_REPORT.md` (this file)
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g1_bootstrap_s1_auroc.json` (G1)
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_refsep_vs_auroc.json` (G2)
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_refsep_vs_auroc.csv` (G2 table)
- `scripts/block_c_closeout/g1_bootstrap_s1_auroc.py`
- `scripts/block_c_closeout/g2_refsep_vs_auroc.py`

No changes to `rows.tier3.v2.csv`, `rescore_t7c_full/rows.csv`, or any
frozen artefact. No commit yet. No push. Working repo remains on
`main` at `80a5a60` with new untracked files under `scripts/block_c_closeout/`,
`docs/BLOCK_C_STATE_CHECK.md`, `docs/BLOCK_C_GATING_REPORT.md`, and the
two verification JSONs / CSV.
