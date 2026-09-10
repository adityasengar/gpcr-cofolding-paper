# BLOCK B — MANUSCRIPT FLAGS

**Purpose**: central index of every claim, phrasing, or Methods-line item
that requires attention in the manuscript. Each flag names what changes if
the item is not addressed. Flags are load-bearing across the paper; a
reviewer who reads the manuscript without seeing the corresponding
correction will surface the issue.

**Provenance**: this list was compiled from the Block B dossier phases
(Phase 0..6). Each flag names the phase report that raised it. All
"manuscript sentence" items across the seven phase docs are catalogued
here — the list is closed against those docs.

**Status legend**:
- `text_only` — a Methods/Results sentence needs to be written or amended; no data change.
- `data_pending` — a rescore or curation-file edit would resolve this; not yet done.
- `open_decision` — pending user adjudication among 2+ options.
- `resolved` — addressed elsewhere in the archive (dossier phase, withdrawal, or caveat).

---

## Flag B-1 — Ladder decomposition family term reports BOTH scales

**Source**: Phase 3 §3e.
**Content**: The "correct family" share of the apo → cognate ladder is
11.1% on the probability scale [0.047, 0.125] and 17.4% on the logit
scale [0.39, 1.09] — share ratio 1.57×. All four backbones agree the
logit family share is 17–21%; probability-scale variation (0.024 for
Protenix to 0.148 for OF3) is a ceiling artefact. The 11% probability
figure understates the identity-driven contribution because 24–34 of
40 receptors × backbones are ceiling-pinned at cognate (see C-B-7). The
manuscript must pick a scale and defend it explicitly, OR report both.
**Recommendation: report both scales in the primary table; use logit
share (17%) when contrasting occupancy vs α5-CT-sequence vs family
because the ceiling compression on the family term alone otherwise
misleads.**
**Related**: SC-B-2, C-B-7, W-B-1.
**Status**: `text_only`.

---

## Flag B-2 — Chai is systematically different (three tells)

**Source**: Phase 1 §1d, Phase 3 §3d/§3c, Phase 4d, Phase 4a.
**Content**: Three independent Chai findings, load-bearing for the
manuscript:

1. **Partial MSA read at the decoy α5-CT.** Chai's `.aligned.pqt` cache
   anchors the decoy query row to WT-parent residues, gaps, or lowercase
   insertions at the α5-CT positions (0 of 40 uppercase-aligned). The
   other three backbones (Boltz, OF3, Protenix) verify uppercase-aligned
   decoy edits (18 of 18 audited cells). Chai's Block B decoy-vs-cognate
   contrast at the MSA-column layer is a partial-read outlier
   (SC-B-9, C-B-2).

2. **Tilt-axis inversion on the top rung.** Chai shows a continuous
   shuffled → cognate median-tilt going DOWN (−0.19 Å) while the binary
   rate rises (0.66 → 0.74). The chai family-term signal lives on
   NPxxY-OH (cognate 6.79 Å vs shuffled 7.24 Å), not tilt (Phase 3 §3c).

3. **pLDDT-inversion tell unmeasurable in Block B.** The Block A "chai
   non-engaged partner pLDDT higher than engaged" tell is not present
   here — Chai's Block B cognate arm produces near-uniformly engaged
   partners (99.75%); only 5 non-engaged rows in 2,000, below the 5-row
   floor for a comparison claim (Phase 4d). Null replication, not
   falsification; the Block A finding is not tested by Block B.

**Manuscript sentence**: "Chai is a per-backbone outlier on Block B on
three axes: partial MSA read at the scrambled α5-CT (0 of 40 decoy pqts
carry the scrambled residues as aligned uppercase columns), tilt-axis
inversion on the shuffled → cognate rung (family signal lives on NPxxY-OH
instead), and unmeasurable partner-pLDDT engagement tell (0.25% non-engaged
cognate rows). Any pooled-across-backbones Block B statement should note
Chai's deviation." **Related**: SC-B-9, C-B-2, Flag B-12.
**Status**: `text_only`.

---

## Flag B-3 — D2 arm-audit resolves the ADRB2 concern; no retraction required

**Source**: Phase 6 D2 arm-sequence audit.
**Content**: The Phase 1 §1a cross-block finding — the `partners.fasta`
Nb60 entry is actually Nb80 (mislabel confirmed by hash) — raised concern
that Block D D2's active-Nb vs inactive-Nb ADRB2 contrast might be
confounded. Phase 6 D2 audit resolves it:

- ADRB2 **active_nb** (Nb80 slot) arm was **INTENTIONALLY DROPPED** at
  drain time — `partner_perturbation = placeholder_nb80_from_nb60_5jqh`
  flags the failed Nb80 substitution; `tier_d2_full_headline_2026_09_07.md`
  line 11 confirms "ADRB2 active_nb intentionally dropped". Zero rows
  from the contaminated arm contribute to the D2 manuscript sentence.
- ADRB2 **inactive_nb** (Nb60 slot) arm consumed **real** Nb60_5JQH
  (125 aa, sha `1406ad7e…`) — 200 rows in analysed corpus.
- The `partners.fasta:Nb60` mislabel (126 aa, sha `b9ad1bad…`) was
  **never consumed** by any D2 arm. All four nanobody-arm consumers drew
  from `refs/nanobody_sequences.fasta`, not `partners.fasta`.
- OPRK, ACM2, AGTR1 nanobody arms all consumed their real, correctly-named
  nanobodies.

**No D2 manuscript-sentence modification recommended.** The mislabel is
a documentation defect without a downstream consequence in D2 as-analysed.
**Related**: SC-B-9, C-B-2 (Chai partial MSA — orthogonal issue), Flag B-19.
**Status**: `resolved` (facts recorded; no sentence change needed).

---

## Flag B-4 — Outcome A firmed by native-only re-run — sentence upgrade

**Source**: Phase 5 §5.6, Phase 6b §6b.2.
**Content**: The pre-registered Outcome A ("model treats α5-CT as bulk;
family identity not encoded on continuous axes") is signed at Phase 5 on
median-sign, CI-gated verdict. Phase 6b's native-only re-run tests
whether the reference-bias caveat (37.5% non-native panel-wide) hides an
Outcome-B signal in the largest cell. Result: Gs→Gi shuffled tilt residual
moves from +0.024 Å [-0.29, +0.30] (all refs, n=24) to −0.062 Å [-0.41,
+0.21] (native only, n=20). Sign flips within noise, CI still spans zero,
CI width unchanged. **Outcome A firms up.**

The load-bearing Gs→Gi cell is 83.3% native-anchored (20/24) — the
reference-bias caveat does NOT localise to this cell (see C-B-10). Under
the reference-bias caveat, the Gs→Gi ≈ 0 finding is formally ambiguous
between Outcome A ("bulk-only reading") and Outcome B ("correct family
reading that renders as near-zero on cognate-anchored axes"). The paper
should name this ambiguity.

**Manuscript sentence** (per Phase 6 sentence-change §1):
> "On the Gs→Gi shuffled cell (24 receptors, 83% native-anchored active
> reference), the tilt residual is +0.024 Å with cluster-boot 95% CI
> [−0.29, +0.30] indistinguishable from zero. Restricted to the 20
> receptors whose active reference is native (`active_stabilization_source
> = native`), the residual moves to −0.062 Å [−0.41, +0.21] — sign flips
> within noise, CI still spans zero, CI width unchanged. The Outcome-A
> reading survives the reference-bias caveat on this cell."

**Related**: SC-B-6, C-B-10, W-B-3, W-B-4.
**Status**: `text_only`.

---

## Flag B-5 — Templates-off is evidence class (b)+(c), not (a)

**Source**: Phase 0 §0d, Phase 0 templates-sweep.
**Content**: Load-bearing for the entire prospectivity framing — templates
must be off on Block B. Evidence supports the claim but is (b) launcher
static analysis + (c) upstream source defaults, not (a) per-row runtime
echo. A 20-file stratified sweep of HPC `_<backbone>_status.json`
(5 per backbone across receptors and arms) confirmed **0 of 20** files
carry a `runtime_config` block, and **0 of 20** carry any template-field
key at any depth. This is not evidence of template regression — the
audit-#9 regression detector is negative on the sample — but it is not
the strongest evidence class either.

**Manuscript sentence** (per templates-sweep verdict):
> "Templates were off across all four backbones on Block B. Evidence:
> launcher static analysis (`qsub/rerun_of3.sh` carries the explicit
> `--use-templates false` flag mandated by audit #9; no template flag in
> any other launcher) + upstream source defaults (Chai
> `use_templates_server=False` at `chai_lab/chai1.py:334`; Protenix
> `use_templates=False` model-config default; Boltz input YAML never
> populates the `templates:` field). The per-row runtime echo audit #9's
> post-dispatch coverage design contemplated is not present on Block B
> `_<backbone>_status.json` files (design landed later or not on Block
> B's launcher revision); a 20-file stratified HPC sample carries no
> `runtime_config` block."

Do not strengthen to "runtime-verified"; do not weaken by claiming
template use. **Related**: SC-B-7, C-B-1.
**Status**: `text_only`.

---

## Flag B-6 — Missing-inactive-refs preload does NOT apply to Block B primaries

**Source**: Phase 6c preload check #3.
**Content**: Six inactive references were added to `refs/reference_set.csv`
between `6ee2cad8` (Block B scoring bytes) and `7a261988` (commit
`d9c646a`, 2026-09-06): AA2AR/5MZP, ADA1A/7YMJ, ADRB2/2RH1, ADRB2/3NYA,
CCR5/4MBS, CNR1/5TGZ. Three receptors in the Block B 40 (AA2AR, ADRB2,
CNR1) gained an additional inactive reference AFTER Block B ran. The
dispatch initially flagged this as a possible NaN-on-inactive-axis
concern.

**Resolution**: the primary inactive references for these three receptors
(AA2AR/5NM4, ADRB2/6PS2, CNR1/5U09) were present in `6ee2cad8` and
computable on both axes. `delta_to_inactive` and `rmsd_to_inactive_ref`
are not forced NaN by this preload for AA2AR / ADRB2 / CNR1. The added
inactive refs are secondaries. **The concern does not localise to Block B
scoring-time bytes.**

The 4 receptors with all-NaN NPxxY-OH (EDNRA, EDNRB, GRPR, HRH3) are NaN
because 7.53 = L not Y in the receptor sequence — intrinsic biology, not
a missing-reference issue (see C-B-15).
**Related**: SC-B-13, C-B-9.
**Status**: `resolved` (no manuscript-facing action needed beyond a
one-line Methods statement pointing at `refs/reference_set.blockb_pinned.csv`).

---

## Flag B-7 — Frame-36 vs frame-40 denominator must be named in every headline table

**Source**: Phase 3 §3d + Phase 4b + Phase 6 §Midpoint ladder.
**Content**: Every published Block B two-instrument number uses frame_36
(n=36 receptors after excluding EDNRA/EDNRB/GRPR/HRH3 with all-NaN
NPxxY-OH). Every published tilt-only headline number uses frame_40
(tilt doesn't go NaN there). The two conventions disagree by 1–9% per
arm. Currently signposting is implicit: `BLOCK_B_CLAIM_AUDIT.md §C3`
documents the finding, `headline_results.md` uses tilt-only,
`BLOCK_C_LIGAND_BLOCK_PLAN_2026_09_03.md §1` uses two-instrument on n=36.
Neither is wrong; readers need explicit signposting. **The manuscript
must call which convention each cited number uses.**
**Related**: SC-B-1, SC-B-3, C-B-5.
**Status**: `text_only`.

---

## Flag B-8 — 20 Å engagement cutoff permissive at cognate; report both 14 Å and 20 Å

**Source**: Phase 4b sensitivity sweep.
**Content**: The 20 Å engagement cutoff is permissive at cognate (4×
median depth of 12.19 Å); p(active|engaged) is nearly flat 10 → 20 Å at
cognate (0.897 → 0.893). On decoy the same sweep moves p(active|engaged)
from 0.53 to 0.66 — the choice of cutoff moves the decoy-arm active
fraction more than the cognate-arm one. Any chemistry-claim table
comparing cognate to decoy engagement must quote both 14 Å and 20 Å;
citing 20 Å alone hides how much of the decoy-arm active fraction is
cutoff-choice-driven.

**Suggested Methods sentence**:
> "Engagement is defined at a 20 Å tip-to-R3.50 Cα cutoff; sensitivity
> across 10–20 Å moves cognate p(active|engaged) by ≤ 0.01 but moves
> decoy p(active|engaged) by 0.13. Both 14 Å and 20 Å values are reported
> in the primary table."

**Related**: SC-B-3, C-B-6.
**Status**: `text_only`.

---

## Flag B-9 — Ceiling-pinning on the family term: use logit, not probability

**Source**: Phase 3 §3f + Phase 3 §3e.
**Content**: Between 60% (of3) and 85% (protenix) of receptors are
ceiling-pinned at cognate (cognate rate ≥ 0.98); correspondingly 62–90%
are floor-pinned at apo (apo rate ≤ 0.02). Under this compression the
probability-scale family term is a **bimodal average** where three-quarters
of the cells produce zero family shift and one-quarter produce a large
one (top 5 receptors by boltz Δp: NPY2R 0.68, NPY1R 0.28, OX2R 0.20,
DRD3 0.20, ACM4 0.19 — all have shuffled < 0.85 so the ceiling has
room). Manuscript sentence-check: "everywhere else the term is ≈ 0"
(Block C plan §1.1) is arithmetically accurate but the mechanism is
ceiling saturation, not intrinsic model insensitivity. Reporting on the
logit scale bypasses the compression; all four backbones agree at 17–21%
logit-family-share.
**Related**: SC-B-2, C-B-7, Flag B-1.
**Status**: `text_only`.

---

## Flag B-10 — Per-receptor midpoint ladder 0.130 / 0.500 / 0.801 / 0.887 has no reproducible source

**Source**: Phase 3 §3d + Phase 6 midpoint reconciliation.
**Content**: Under uniform (5, 10) × 40 design, per-receptor midpoint
mean equals panel mean (arithmetic identity when cells are uniform-sized).
Panel mean binary predicate on frame_36 = 0.158 / 0.558 / 0.809 / 0.891
(reproduces dispatch cite exactly). The cited "per-receptor midpoint
ladder: 0.130 / 0.500 / 0.801 / 0.887" does not reproduce on any tried
n=28 subset. Phase 6 tried 7 candidate subsets (native-only n=22 gets
closest at cognate=0.892 but under-shoots decoy and apo by ~0.03);
none of these reproduces the target within 0.02 per arm. **The four
numbers likely come from either (a) a different corpus (Block A rather
than Block B), (b) a different weighting scheme, or (c) a per-receptor
median rather than mean — none documented on disk.** The manuscript
should cite the reproduction_36 ladder (0.158 / 0.558 / 0.809 / 0.891)
and note the discrepancy with the earlier cite as a documentation
ambiguity, OR withdraw the cite.
**Related**: SC-B-1, W-B-2.
**Status**: `text_only`.

---

## Flag B-11 — AA2AR is anomalous by non-saturation, NOT by missing reference

**Source**: Phase 6c + Phase 6a.
**Content**: AA2AR is called anomalous across three separate analyses
across the campaign. On Block B: family term +0.76 (boltz cognate 0.80
− shuffled 0.04) — the single largest per-receptor family term in the
panel. Active ref 5G53 (mini-G, tilt 18.10 Å, NPxxY-OH 3.71 Å); inactive
ref 5NM4 (tilt 11.99 Å, NPxxY-OH 9.73 Å) — **primary inactive ref present,
both axes populated, both delta and RMSD to inactive computable.** AA2AR
is the only receptor in Block B where a single backbone (boltz) has
shuffled < 0.10 and cognate < 1.0 — the family term is measurable
rather than saturation-flattened. **The recurrent-anomaly line in the
paper does not need a "missing reference" caveat; it needs a
"non-saturated exposes what other cells hide" caveat.** AA2AR contributes
to the panel-level Δ_ref tilt continuous slope entirely on its own (+0.049
→ −0.003 when AA2AR excluded).
**Related**: SC-B-11, C-B-8.
**Status**: `text_only`.

---

## Flag B-12 — Chai partner-pLDDT tell unmeasurable — null replication, not falsification

**Source**: Phase 4d.
**Content**: Block A's "chai cognate non-engaged partner pLDDT > engaged
partner pLDDT" finding (the "abandoned partner" tell) is not present in
Block B — engaged rows carry ≥ non-engaged partner pLDDT on every arm
(cognate delta +13.7, shuffled +1.4, decoy +0.5). But Block A's cognate
non-engaged pLDDT-high stratum was ~5–10% of rows; on Block B it is
0.25% (5 of 2,000). **The Block A finding is not falsified; it is
unmeasurable on this corpus** because Chai's Block B cognate arm produced
near-uniformly engaged partners (99.75%). Flag for the manuscript.
**Related**: SC-B-12 (contact register), C-B-2, Flag B-2.
**Status**: `text_only`.

---

## Flag B-13 — "1,263 of 1,935 non-inserted decoy contacts" does not exactly reproduce

**Source**: Phase 4b non-inserted decoy check.
**Content**: The dispatch's cited "1,263 of 1,935 non-inserted decoy rows
make > 20 contacts" pair does not exactly reproduce on the final Block
B corpus. At frame_40, tip ≥ 20 Å, n = 2,398 non-inserted decoy rows:
1,623 (68%) have > 20 interface contacts, 1,253 (52%) have > 30 contacts.
At frame_36: 1,427 of 2,133. The (1,263, > 30) count is close numerically
but the 1,935-denominator is not reproducible in this data. Most likely
the dispatch quoted a mid-Phase-2 pre-drop count.
**Restatement for the manuscript**: **1,623 of 2,398 non-inserted decoy
rows carry > 20 interface contacts (frame_40; 1,427 of 2,133 in frame_36).**
Story unchanged (majority engagement without insertion).
**Related**: SC-B-3, W-B-6.
**Status**: `text_only`.

---

## Flag B-14 — Cluster-bootstrap over 26 reconstructed paralog clusters is authoritative

**Source**: Phase 3 §3g.
**Content**: The paralog cluster map is **reconstructed 2026-09-09** at
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`.
Phase 0 addendum cited "26 paralog clusters" but shipped no file; shipped
Block C bootstraps use receptor-as-cluster (40 clusters), not paralog
groups. The 26-cluster map treats OPRX (nociceptin/NOP) as its own cluster
distinct from the DOR/MOR/KOR opioid triplet; other groupings follow
canonical GPCR family taxonomy. All Block B bootstraps in this dossier
resample paralog clusters. Downstream analyses should either (a) formalize
this reconstruction with a git commit + review, (b) fall back to
receptor-as-cluster for consistency with existing Block C bootstraps,
or (c) both. **Recommended: (a); (b) reported as sensitivity.**
**Related**: C-B-13, C-8-adjacent (Block A convention).
**Status**: `text_only` (Methods sentence + `data_pending` for formal
git-commit of the cluster map).

---

## Flag B-15 — Contact register is canonical; no non-canonical binding-face signature

**Source**: Phase 4a.
**Content**: Across 160 engaged cells per arm, the receptor BW positions
most in contact with the last-5 partner residues are R3.50, TM6 apex
(6.29–6.36), H8 (8.47/8.49), TM2 (2.39), TM7 (7.56) — the canonical
Class A Gα-binding face — on every arm (cognate, shuffled, decoy). No
non-canonical binding-face signature appears. The decoy arm makes
fewer TM6-apex contacts even when engaged (6.33 counts fall
apo → shuffled → decoy: 327 → 297 → 156). Contributes to the "engaged
but not fully inserted" reading of the decoy engaged-but-inactive cell.
**Related**: SC-B-4, SC-B-12.
**Status**: `text_only`.

---

## Flag B-16 — Gs→Gq third finding does NOT survive native-only power — no manuscript sentence

**Source**: Phase 5 §5.5 + Phase 6b §6b.2.
**Content**: The Phase 5 "third finding" — Gs donor into Gq receptor
produces LESS TM6 tilt than the Gq-cognate active reference expects
(panel median −0.47 Å [-0.81, -0.05], 3 of 4 backbones same-signed) —
does NOT survive native-only power analysis at 95% CI. Native n=3 of 8;
point estimate preserved (−0.51 vs −0.47 Å) but CI blows out to
[-2.79, +0.14] and no longer excludes zero. **The third finding cannot
earn a manuscript sentence on the strength of Phase 5 alone.**

**Retraction target**: replace any prose citing "the Gs-into-Gq cell
shows a small (~0.5 Å) family-mismatch penalty" with the Phase 6
sentence-change #2 recommendation, OR drop the sentence entirely. The
Gs→Gq "Hold" from Phase 5 is not lifted.
**Related**: W-B-3.
**Status**: `text_only`.

---

## Flag B-17 — "94%" cites reconcile to Block A protenix cognate (94.4%), NOT Block B

**Source**: Phase 3 §3g + Phase 6 94%-reconciliation.
**Content**: Three "94%" referents surfaced on grep:

1. Item #4 = Block A **protenix cognate active-call fraction, 94.4%**
   on Class A n=36 two-instrument (`campaign_completion_report.md` line
   240). This is the load-bearing "94%".
2. Items #5/#6 = Block A cognate normalised-position ~94% (`campaign_completion_report.md`
   §1; POST_BLOCK_A_CLEANUP §median normalised-position) — a **position
   on a continuous axis**, not an activation fraction.
3. `BLOCK_B_DISPATCH_PLAN_2026_09_02.md` line 105 claim "Shuffled at 94%
   active in Block A" — **Block A had no shuffled arm** (only apo +
   cognate per PREREG §12; shuffled was reserved for Block B). This is
   a dispatch-plan drafting error, not a real Block A number. **The 94%
   belongs to Block A cognate, not Block A shuffled.**

**E1's 94%** cited in older docs is not surfaced from Block A / Block B
docs on grep; consistent with first-era corpus origin. Recorded as
UNVERIFIED, not closed.

**Manuscript-facing action**: attribute every "94%" cite explicitly.
Retract any Block A shuffled 94% phrasing if inherited from the dispatch
plan.
**Related**: W-B-5.
**Status**: `text_only`.

---

## Flag B-18 — `partners.fasta` Nb60 and GASR mislabels — documented, not consumed

**Source**: Phase 1 §1a.
**Content**: Two mislabels in the primary partner file, both confirmed by
sequence hash:

- `partners.fasta:Nb60` (126 aa, sha `b9ad1bad…`) is actually **Nb80**
  by CDR3 (Rasmussen 2011 β2AR active-state, PDB 3P0G). The real Nb60
  (Staus 2016 β2AR inactive-state, PDB 5JQH) is at 125 aa,
  sha `1406ad7e…` in `refs/nanobody_sequences.fasta`.
- `partners.fasta:GASR` (header self-declared `Gα`, 396 aa,
  sha `30f4709b…`) is actually the **CCKB / gastrin receptor** by
  sequence — a Class A GPCR with seven TM helices, not a Gα.

**Both entries UNUSED by Block B.** No Block B row consumed either
sequence; corpus not invalidated. The mislabels remain in the primary
partner file and would silently masquerade in any future block that
routes partners by header rather than by hash. **Recommendation**: fix
both headers in `partners.fasta` at a future dispatch preparation step.
Not a blocker for the Block B manuscript.
**Related**: SC-B-8, Flag B-3.
**Status**: `data_pending` (partner file annotation edit; scope well
defined; execution deferred).

---

## Flag B-19 — Block D D2 arm-audit results (no retraction)

**Source**: Phase 6 D2 arm-sequence audit.
**Content**: Same content as Flag B-3, summarised as manuscript-facing
sentence action: **no Block D D2 manuscript sentence needs to be modified
on the strength of Phase 6.** The concern that D2 active-Nb-vs-inactive-Nb
ADRB2 is confounded by the Nb60/Nb80 mislabel is resolved: the ADRB2
active_nb arm was intentionally dropped (0 rows); the ADRB2 inactive_nb
arm consumed real Nb60_5JQH; no arm consumed the `partners.fasta`
mislabel. The 30-row deficit on AGTR1 active_nb is a straggler-drain
artefact, not a sequence issue.
**Related**: Flag B-3, C-B-2 (Chai; separate concern).
**Status**: `resolved`.

---

## Flag B-20 — rows.csv sidecar deferred with recorded_at discipline for future

**Source**: Phase 0 addendum item 1.
**Content**: rows.csv's bytes match the derived-from pointer in
`rows.rmsd.csv.provenance.json:parent_rows_csv_sha256 = c65b93c2…`
exactly. There is no `rows.csv.provenance.json` sidecar on the primary
table today. Any sidecar authored today for Block B rows.csv must carry
`"recorded_at": "consolidation_time_2026_09_09"` and NOT carry any field
suggesting run-time creation, per the addendum's rule. **Rule for future
dispatches (from Block D forward): stamp sidecars at scoring time.**
Not a corpus-invalidating gap; recorded as a discipline note.
**Related**: (methods reproducibility section).
**Status**: `data_pending` for future dispatches; **DEFERRED** for the
existing Block B rows.csv.

---

## Flag B-21 — Empty `propose_py_git_sha` / `build_manifest_py_git_sha` — compensating content control

**Source**: Phase 0 addendum item 2.
**Content**: `manifest.provenance.json` carries empty
`propose_py_git_sha` and `build_manifest_py_git_sha`. These are the code
that produced the decoy scrambles and shuffled-partner assignments —
load-bearing files for Phase 1b (decoy) and Phase 1c (shuffled). The
compensating control: **construct identity is verified by content in
Phase 1b/1c**, not by generator version (byte-identical prefix, length
parity, tail Hamming, parent-Gα routing against `refs/gpcr_coupling.csv`,
non-cognate-family Gα for shuffled). Content verification supersedes
generator provenance for these files on this corpus. Caveat, not blocker.
**Related**: SC-B-8, C-B-12.
**Status**: `text_only`.

---

## Flag B-22 — No `outputs/` symlink for Block B (ergonomic)

**Source**: Phase 2 §2e.
**Content**: `experiments/019_block_b_partner_selection/` has no
`outputs -> /hpc/scratch/…` symlink of the kind Block A carries. Every
Block B `input_path` in rows.csv is an HPC absolute path. **Corpus is
byte-addressable via `input_sha256` regardless** — this is a
laptop-side path-resolution ergonomic gap, not a reproducibility gap.
Recommend adding the symlink to match Block A's convention.
**Related**: C-B-4.
**Status**: `data_pending` (one symlink creation; scope trivial).

---

## Flag B-23 — `rows.fold_integrity.csv` 0% coverage on scorer_git_sha / input_sha256 / ref_set_csv_sha256

**Source**: Phase 2 §2d.
**Content**: `rows.fold_integrity.csv` carries **0%** coverage on the
three load-bearing provenance columns (`scorer_git_sha`, `input_sha256`,
`ref_set_csv_sha256`); `input_path` is 100% populated. The fold-integrity
emitter does not write per-row provenance columns. Every row is joinable
back to `rows.csv` via `input_path`, and the parent SHA pin lives in the
`# rules:` header comment on line 1 (`input_rows_csv_sha256 = c65b93c2…`,
matches on-disk rows.csv byte-for-byte). Not corpus-invalidating; **fix
the emitter for future dispatches** (per memory: D3 memory note already
lands per-row `scorer_git_sha` on fold_integrity).
**Related**: SC-B-5, C-B-3.
**Status**: `data_pending` (emitter fix for future dispatches).

---

## Flag B-24 — `rows.pocket.csv` scored under a different (later) scorer_git_sha than rows.csv

**Source**: Phase 2 §2d.
**Content**: rows.csv `scorer_git_sha = 04243c45…` (RMSD 7TM-only +
completeness gate, 2026-09-02); rows.pocket.csv `scorer_git_sha =
fd87133…` (Block C plan amendment, 2026-09-03; pocket layer ran ~a day
later). Both on `origin/main`. Both pin the same `ref_set_csv_sha256 =
6ee2cad8…`. Not a defect — layered analysis generates layered scorer
versions — but any cross-layer claim must cite both SHAs.
**Related**: SC-B-13.
**Status**: `text_only`.

---

## Flag B-25 — Block A vs Block B OF3 effective-n asymmetry (constant-seed bug)

**Source**: Phase 0 addendum "OF3 effective-n asymmetry".
**Content**: Block A ran with the OF3 seed bug in place (all rows silently
used constant `seed_2746317213`); Phase 0 verified 0 sentinel hits on
Block B. **Block A OF3 effective seed replication per cell = 5 samples
only; Block B = 50 (5 seeds × 10 samples).** Any pooled A+B statistic,
any "same pattern in both blocks" sentence, and any bootstrap treating
Block A and Block B OF3 rows as exchangeable must account for the ~10×
asymmetry. Standing dossier note.
**Related**: SC-B-10, C-B-16.
**Status**: `text_only`.

---

## Flag B-26 — Chai `.aligned.pqt` code-inspection deferred

**Source**: Phase 1 §1d GATE 1 CONDITIONAL item 1.
**Content**: The 40/40 Chai decoy pqt query rows do NOT contain the
scrambled α5-CT residues as aligned uppercase columns. **Whether Chai's
downstream MSA-feature builder ingests the raw decoy sequence (from the
input yaml, 354 aa) and re-aligns it against the pqt, OR ingests the
pqt's query row as-is (350 aa nogap for 5HT1B) and pads** is not decided
by Phase 1. Both routes have load-bearing consequences for what the model
reads at scrambled positions. Chai code inspection is out of scope for
Phase 1. Not blocking manuscript sentence per SC-B-9 (three-backbone read
holds); if Chai's decoy behaviour becomes load-bearing to a specific
paper sentence, a targeted read of `chai_lab`'s msa loader and a paired
probe of one Chai decoy run's runtime tensor at positions 343–353 would
settle it in an afternoon.
**Related**: SC-B-9, C-B-2.
**Status**: `data_pending`.

---

## Flag B-27 — Gi→Gs shuffled cell cannot be resolved on Block B references alone

**Source**: Phase 6b §6b.2.
**Content**: The Gi→Gs shuffled cell (5 receptors) has 0/5 native-anchored
active references (AA2AR/mini_G, ADRB1/nanobody, ADRB2/nanobody + FSHR/LSHR
which the field labels native but the Phase 5 caveat calls chimera-anchored
via glycoprotein-hormone conventions). Under the strict
`active_stabilization_source = native` filter, n=0. **The Gi→Gs cell
cannot be resolved by native-only re-run on Block B references alone.**
Deferred to a redesign (widened reference set, or an alternative axis
anchoring on inactive references). Not blocking Outcome A on the
manuscript-load-bearing Gs→Gi cell.
**Related**: SC-B-6.
**Status**: `data_pending` (redesign).

---

## Summary counts

| Category | n |
|---|---:|
| Total flags | 27 |
| `text_only` | 18 |
| `data_pending` | 8 |
| `open_decision` | 0 |
| `resolved` | 3 |

**Load-bearing manuscript changes for Block B**:

1. Report ladder decomposition on BOTH scales (Flag B-1); retire single "~11%" figure (W-B-1).
2. Cite Chai's per-backbone deviations (Flag B-2); note pooled statements attenuate.
3. Adopt Phase 6b sentence-change #1 (Flag B-4) as the Phase 5 headline (SC-B-6).
4. Withdraw the Gs→Gq third-finding manuscript sentence (Flag B-16, W-B-3).
5. Name frame_36 vs frame_40 in every headline table (Flag B-7).
6. Report both 14 Å and 20 Å engagement cutoffs (Flag B-8).
7. Move family-term reporting to logit scale where practical (Flag B-9).
8. Attribute the "94%" figures explicitly; retract "Block A shuffled 94%" phrasing (Flag B-17, W-B-5).
9. Frame AA2AR as "non-saturated exposes what other cells hide", not "broken reference" (Flag B-11).
10. Templates-off wording: keep at class (b)+(c) strength; do NOT upgrade to "runtime-verified" (Flag B-5).

**Deferred limitations** (also listed in the claim sheet's "Deferred
limitations" section):

- Runtime-config echo audit at Block B row-grain (only on 20-file sample; Flag B-5)
- rows.csv self-SHA sidecar (Flag B-20)
- Chai `.aligned.pqt` code-inspection (Flag B-26)
- Gi→Gs shuffled cell resolution (Flag B-27)
- Deposition_count as covariate (needs external RCSB source; Flag B-11-adjacent)
- Panel-wide MSA α5-CT column audit on Block D and later blocks (Flag B-2-adjacent)
- Partner-file mislabel fixes: Nb60 → real Nb60_5JQH; GASR → real CCKB (Flag B-18)
- `rows.fold_integrity.csv` per-row provenance columns (Flag B-23)
- `outputs/` symlink for Block B (Flag B-22)

**Pending user decisions**: none. The two Phase 6-adjacent open decisions
(AGTR1 6OS2 / CNR2 5ZTY re-anchoring) are Block-C-level and Block-A-level
issues respectively; Block B was scored against the pre-correction
annotations and neither shifts a Block B numeric value (see C-B-11).
