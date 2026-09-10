# AGTR1_REFASSIGN_REPORT — G2 follow-up

**Date**: 2026-09-10.
**Scope**: single-receptor diagnostic on AGTR1's reference assignment,
follow-up to G2's pocket-Cα-separation vs S1-AUROC regression
(reference: `docs/BLOCK_C_GATING_REPORT.md` §G2).
**Rule**: report evidence and propose. Do not patch shared corpus or
pipeline in this dispatch. Do not resume BLOCK_C_CLOSEOUT Parts B/C.

---

## Section 1 — Assignment pulled from disk

### 1a — Reference PDB IDs, paths, SHAs

**Active reference (AGTR1)**:
- **PDB ID**: `6OS2`
- Reference PDB file on disk: `../paper_af3_release/panel/refs/pdb/6os2.cif`
  (release-repo path; symlinked or copied from the working repo's
  reference set). Also present in the working repo at
  `panel/refs/pdb/6os2.cif`.
- `ref_pdb_sha_active` (row-level column, per-row identical for AGTR1):
  **`b67a9d76f42e2bcdd286cbf890e6a94130d1f5bc8d841213ecf148d4957ce560`**.
- `pocket_ref_pdb_sha_active` (row-level, per-row identical for AGTR1):
  **`e9123681f8c210b0d3f66be0e4d09281921a8abecee21e8767d8301c280fc5a0`** —
  different SHA than `ref_pdb_sha_active` because the pocket cache stamps
  the SHA of the pocket-reference CIF (which may be a pre-processed
  variant of the raw ref PDB). Both trace to the same source (6OS2).
- Structure title: *"Structure of synthetic nanobody-stabilized
  angiotensin II type 1 receptor bound to TRV026."*
- Deposition entities:
  1. Chimeric polymer (Type-1 AT1 receptor + soluble cytochrome b562
     BRIL fusion protein).
  2. Nanobody Nb.AT110i1_le.
  3. TRV026 peptide.
  4–7. Non-polymer (NAG, OLC = oleyl carbonate, CHOLESTEROL, water).

**Inactive reference (AGTR1)**:
- **PDB ID**: `4ZUD`.
- Reference PDB file on disk: `../paper_af3_release/panel/refs/pdb/4zud.cif`.
- `ref_pdb_sha_inactive`: **`11d8b43441263e85b3c4fa66f18f34f28c27deda34c9d2dc8f3e605626b55d99`**.
- `pocket_ref_pdb_sha_inactive`: **`3aa3c0e2a9ee7736ae15375320a05fe649d60452926c3a878151f2caf7d85871`**.
- Structure title: *"Crystal Structure of Human Angiotensin Receptor in
  Complex with Inverse Agonist Olmesartan at 2.8A resolution."*
- Deposition entities:
  1. Chimeric polymer (BRIL + AT1 receptor).
  2. Olmesartan (`OLM` HETATM), an inverse agonist.

**Cross-corpus role labels** (from `rows.tier3.v2.csv`, AGTR1 rows):
- `pocket_ref_role_active` = `active` for every AGTR1 row (1,200 rows).
- `pocket_ref_role_inactive` = `generic_inactive_fallback` (800 rows,
  full_agonist + decoy_lig) or `inactive_neutral_antagonist` (400 rows,
  neutral_antagonist).
- **Both role labels resolve to the SAME `pocket_ref_pdb_sha_inactive`
  SHA `3aa3c0e2…` per receptor** — the label routes but the resolved
  PDB collapses (identical to the corpus-wide G3 finding at
  `docs/BLOCK_C_GATING_REPORT.md §G3`).

### 1b — BW-anchor mapping (12 pocket positions)

Per AGTR1's row-level `anchor_positions` JSON, the six named
receptor-anchor positions are:

| BW | UniProt pos | AA (expected) | AA (observed on rows) |
|---|---:|---|---|
| 3.50 | 126 | R | R |
| 3.51 | 127 | Y | Y |
| 5.58 | 215 | Y | Y |
| 6.30 | 235 | N (Asn — atypical DRY) | N |
| 6.34 | 239 | F | F |
| 7.53 | 302 | Y | Y |

**Note**: AGTR1's 6.30 = **Asn**, not the canonical DRY-motif Glu/Asp.
`curation_note` on both references flags this: *"6.30 is neither Glu
nor Asp (observed N); DRY ionic-lock reference will be NaN."* This is
a KNOWN AGTR1 idiosyncrasy, unrelated to the pocket-Cα classifier
feature (which uses pocket-lining residues, not the DRY motif).

The 12 pocket BW anchors from `scorer/pocket_metrics.py::POCKET_BW_LABELS`
are 3.32, 3.33, 3.36, 5.42, 5.43, 5.46, 6.48, 6.51, 6.52, 6.55, 7.39,
7.42. Their UniProt positions in AGTR1 (derived from the receptor-anchor
table via within-helix offset):

| BW | UniProt pos |
|---|---:|
| 3.32 | 108 |
| 3.33 | 109 |
| 3.36 | 112 |
| 5.42 | 199 |
| 5.43 | 200 |
| 5.46 | 203 |
| 6.48 | 253 |
| 6.51 | 256 |
| 6.52 | 257 |
| 6.55 | 260 |
| 7.39 | 288 |
| 7.42 | 291 |

### 1c — E2 cross-validation coverage

**Cannot resolve on disk**: the dispatch references "curator E2" as an
independent cross-validation label; the repository's `docs/`, `refs/`,
and audit-trail files use `E1..E4` as *Block B FOLLOWUP phases* (§E1
external ruler, §E2 scope note, §E3 cluster-boot audit, §E4 AA2AR
reference-separation), not as a curator label. There is no
receptor-list documented under a "curator E2 cross-validation" tag.

**AGTR1 does appear in three other independent audit tracks**:
1. Block A step-3 cross-validation dossier
   (`docs/BLOCK_A_STEP3_CROSSVAL_2026_09_01.md`, per grep) — AGTR1 is
   not flagged as reference-swap-candidate there (CNR1 and OPRD are).
2. Auto-memory `apo_bistability_reference_artefact_2026_09_06.md`:
   AGTR1 (6OS2 nanobody) named as a member of the G-protein-free
   stratum in Block A apo bistability — implicitly acknowledges 6OS2
   is nanobody-stabilised, not G-protein-coupled.
3. Auto-memory `block_d_d2_nanobody_collision_2026_09_09.md`: AGTR1
   nanobody arm consumed the correct sequence — verification unrelated
   to the reference-assignment question here.

**No independent curator cross-validation** (in the sense of a
receptor-by-receptor review of active/inactive PDB choice) is on disk
for AGTR1. Reference-choice governance for AGTR1 is inherited from
`refs/reference_pdbs.csv` + `refs/reference_set.csv` at the point of
Block A dispatch (`block-a-dispatch-2026-09-01` tag).

---

## Section 2 — Three checks

### 2a — Swap check (file content vs label)

**No swap.** Verified by reading each CIF's header + entity list:

| PDB | Structure title | Chain composition | Bound ligand(s) | State evidence |
|---|---|---|---|---|
| **6OS2** (labeled active) | "Structure of synthetic nanobody-stabilized AT1R bound to TRV026" | AT1R-BRIL chimera + Nb.AT110i1_le + TRV026 peptide | TRV026 peptide (β-arrestin-biased agonist), NAG, cholesterol, oleyl carbonate | β-arrestin-biased-agonist-bound + intracellular nanobody stabilizer |
| **4ZUD** (labeled inactive) | "Crystal Structure of Human Angiotensin Receptor in Complex with Inverse Agonist Olmesartan at 2.8A resolution" | BRIL-AT1R chimera | Olmesartan (`OLM`, inverse agonist) | Canonical inverse-agonist state |

**Files match their labels at the "active-state deposition" scope the
dispatch names** (G-protein mimetic / nanobody / biased-agonist
stabilizer for active; inverse agonist for inactive). Neither is a
mis-labeled file.

**Curation observation** (not a swap; recorded as a finding):
6OS2's active-state character is **β-arrestin-biased agonist +
intracellular nanobody**, NOT a canonical G-protein-coupled or
G-protein-mimetic active state. `refs/reference_set.csv` labels 6OS2's
`resolved_state = Ga-coupled-active`, and `stabilising_elements =
nanobody_beta_arrestin_biased_agonist`. The `stabilising_elements`
field is accurate; the `resolved_state` label is arguably imprecise —
"Ga-coupled-active" suggests G-protein coupling, which 6OS2 does not
carry. This is a **curation label choice**, not a mechanical defect.

### 2b — Predicate cross-check

Ran the class-A two-instrument activation predicate directly on the
scorer-recorded reference values in `refs/reference_set.csv`:

**Predicate**: `d_npxxy_y558_y753_oh < 9.082 AND d_gpcrdb_tm6_tilt_246_637_ca > 14.932` → active.

| PDB | label | NPxxY-OH (Å) | TM6 tilt (Å) | Predicate → | Match? |
|---|---|---:|---:|---|---|
| 6OS2 | active | **4.047** (< 9.082 ✓) | **19.086** (> 14.932 ✓) | ACTIVE | ✓ |
| 4ZUD | inactive | **11.779** (> 9.082, fails) | **11.228** (< 14.932, fails) | NOT-ACTIVE | ✓ |

Both references pass their labels on the two-instrument predicate
independently of the S1 classifier. **No swap detected on predicate
cross-check.**

### 2c — Mapping check (12 BW pocket anchors)

**Both structures use a BRIL–AT1R chimeric polymer in chain A, with
DIFFERENT author-numbering conventions:**

Parsed via `_struct_ref_seq` in the CIFs.

**6OS2 chain A entity 1** (3-part alignment):
- entity_seq[9..233] → UniProt AGTR1 (P30556) residues 2..226 →
  auth_seq_id 2..226 (AGTR1 N-terminus + TM1–TM4 + ICL2 + TM5 up to 226).
- entity_seq[234..332] → BRIL (P0ABE7) residues 24..122 →
  auth_seq_id 227..1226 (BRIL insertion; 1000-offset shift begins mid-chain).
- entity_seq[333..425] → UniProt AGTR1 residues 227..319 →
  **auth_seq_id 1227..1319** (AGTR1 TM6 onwards under 1000-offset numbering).

**4ZUD chain A entity 1** (3-part alignment):
- entity_seq[1..106] → BRIL residues 23..128 → auth_seq_id 1001..1106.
- entity_seq[107..111] → AGTR1 residues 2..6 → auth_seq_id 12..16.
- entity_seq[112..410] → AGTR1 residues 17..315 → **auth_seq_id 17..315**
  (native AGTR1 numbering).

**Direct comparison of AGTR1 sequence around W6.48 (UniProt 253) in
both structures** (verified by parsing each CIF's chain A polymer):

| BW | UniProt pos | 6OS2 auth | 6OS2 residue | 4ZUD auth | 4ZUD residue | Match? |
|---|---:|---:|---|---:|---|---|
| 6.48 | 253 | **1253** | TRP | 253 | TRP | ✓ |
| 6.51 | 256 | 1256 | HIS | 256 | HIS | ✓ |
| 6.52 | 257 | 1257 | GLN | 257 | GLN | ✓ |
| 6.55 | 260 | 1260 | THR | 260 | THR | ✓ |
| 7.39 | 288 | 1288 | ILE | 288 | ILE | ✓ |
| 7.42 | 291 | 1291 | ALA | 291 | ALA | ✓ |
| 7.53 | 302 | 1302 | TYR | 302 | TYR | ✓ |

The AGTR1 sequences at the pocket-lining residues are **identical in
both structures**. No indel, no truncation, no loop insertion near the
pocket. The 1000-offset difference in author numbering is entirely
resolvable via SIFTS / struct_ref_seq (both present in the CIFs).

The scorer's `build_uniprot_model` (called by
`scorer/pocket_metrics.py::build_pocket_reference_cache`) is designed
to consume this mapping and index CAs by UniProt position, not by
auth_seq_id. **Given that Block B's E4 pocket-Cα script reported
n_pocket = 12 (all 12 anchors resolved on both sides) and
tm_kabsch_rmsd = 2.55 Å on 226 common TM residues, the mapping did
resolve correctly** — the pocket-Cα RMSD of 1.87 Å between the two
references is a genuine Kabsch-aligned pocket geometry difference,
not a mapping artefact.

Also verified: on the pocket-Cα RMSD-active side (predictions vs 6OS2),
the corpus-level `pocket_ca_rmsd_active` median for AGTR1 is 0.44 Å
(full_agonist) / 0.56 Å (neutral_antagonist) — SMALL. If the mapping
were mismatched (comparing wrong residues), we'd expect this value to
be inflated. The values are small and comparable to `pocket_ca_rmsd`
distributions on other well-behaved receptors — consistent with a
correct mapping.

**No mapping error detected.**

### 2 — verdict

**No mechanical defect (no swap, no mapping error).** The three
checks return clean. The candidate for a Section-3 corrected-value
rerun is NOT triggered.

**A curation-level observation stands, worth naming for a subsequent
dispatch**: 6OS2's active-reference character is **β-arrestin-biased
agonist + intracellular nanobody**, not a canonical Gα-coupled active
state, and the `refs/reference_set.csv` label
`resolved_state=Ga-coupled-active` is imprecise. This is a
JUDGMENT-CALL issue (dispatch: "not a judgment call"), not a mechanical
error, and no correction is proposed here — see §Proposals below.

---

## Section 3 — Sensitivity: G2 with AGTR1 excluded

Always-run per dispatch. Excluded, not corrected — the Section-2
threshold for a corrected rerun is not met.

**Output**: `experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_excl_agtr1.json`.

### 3a — Per-backbone slope

Regression: per-receptor S1 LORO AUROC (from `s1_loro_classifier.json`
variant `C_no_selfref_apo` × `F_iii_pocket_plus_axes`) on
pocket-Cα separation (from
`experiments/019_block_b_partner_selection/analysis/reference_separation_pocket_ca.csv`).

| backbone | slope full (n=15, Å⁻¹) | slope excl AGTR1 (n=14, Å⁻¹) | Δ slope | rho full | rho excl | R² full | R² excl |
|---|---:|---:|---:|---:|---:|---:|---:|
| boltz | −0.278 | **−0.002** | +0.276 | −0.297 | −0.128 | 0.182 | 0.000 |
| chai | −0.239 | **+0.040** | +0.279 | −0.247 | −0.066 | 0.085 | 0.004 |
| of3 | −0.491 | **−0.294** | +0.197 | −0.319 | −0.161 | 0.292 | 0.137 |
| protenix | −0.292 | **+0.017** | +0.309 | −0.093 | +0.151 | 0.156 | 0.003 |
| **pooled** | **−0.325** | **−0.060** | **+0.265** | −0.206 | −0.015 | 0.162 | 0.010 |

**Pooled slope CIs (receptor-boot, 1000 iter)**:
- Full 15-set: **[−0.570, −0.068]** — excludes zero (nominally sign-negative).
- Excluding AGTR1: **[−0.246, +0.087]** — **spans zero**.

**Bimodality (n_inverted_lt_0.30 per backbone) — where did the
inversions live?**

| backbone | n_inverted full | n_inverted excl AGTR1 |
|---|---:|---:|
| boltz | 1 | 0 |
| chai | 1 | 0 |
| of3 | 2 | 1 (CXCR2 remains) |
| protenix | 1 | 0 |

AGTR1 is the ONLY inversion on Boltz, Chai, and Protenix. On OF3, both
AGTR1 AND CXCR2 invert; excluding AGTR1 leaves CXCR2. This matches the
manuscript's existing pattern statement ("AGTR1 on all four backbones;
CXCR2 on OF3").

### 3b — Interpretation

Two readings, both fair:

**Reading 1 (AGTR1 as outlier)**: AGTR1 alone drives ~85 % of the
apparent negative-slope signal that led G2 to call the ref-sep
hypothesis refuted. With AGTR1 excluded, the pooled slope is
essentially flat (−0.060, CI [−0.246, +0.087]) — the reference-
separation hypothesis is neither supported nor refuted, it is simply
uninformative on the remaining 14 receptors. This flat behaviour is
consistent with pocket-Cα-sep not being an a-priori applicability
criterion; the empirical failure list stays (AGTR1, CXCR2 on OF3), the
mechanism is unexplained.

**Reading 2 (AGTR1 as legitimate data)**: AGTR1 sits at pocket-Cα-sep
rank 39/40 AND inverts on all four backbones. Excluding it corrects
for a curationally-suspect reference (biased-agonist + nanobody, not
Gα-coupled). The full-15 numbers stay in the report as the
data-as-scored, but the excl-AGTR1 numbers reflect the intended
"canonical Gα-coupled active" scope.

**Neither reading revives the ref-sep hypothesis as an a-priori
criterion** — no version of the slope predicts AUROC well enough
(R² ≤ 0.14 on OF3, ≤ 0.01 on the other three, excluding AGTR1).

### 3c — Corrected-value rerun

**NOT RUN.** The dispatch's condition — *"Only if Section 2 finds an
unambiguous, mechanical defect (a clear swap or a clear mapping error
— not a judgment call), apply the correction locally"* — is not met.
The biased-agonist curation observation is a judgment call, not a
mechanical defect.

`g2_corrected_agtr1.json` is intentionally NOT produced.

---

## Impact on the manuscript-sentence at stake

**Manuscript sentence at stake** (from dispatch): the G2 applicability-
domain claim — main-text negative result, re-scoped, or withdrawn as
artefact-driven.

**What this diagnostic changes**:

- The G2 applicability-domain claim as originally computed
  (full-15-receptor slope) is **not artefact-driven** in the mechanical
  sense: no swap, no mapping error, both references pass the
  two-instrument predicate on their labels, sequence identity at all
  12 pocket anchors is preserved. G2's mechanical basis is clean.
- But **~85 % of the negative-slope signal is one receptor**. On any
  reasonable manuscript standard, a slope that flattens from −0.325
  to −0.060 on a single-receptor removal is not a robust negative
  correlation.
- The excl-AGTR1 result is *closer to inconclusive than to refuted*:
  slope CI includes zero, R² ≈ 0.01 on three backbones. The
  reference-separation hypothesis becomes neither predictive nor
  clearly refuted; it is uninformative on the 14 remaining receptors.

**Two rewrite paths** for a Discussion sentence, both defensible:

- **(A) Bounded negative, one-flagged-outlier scope**: state the G2
  finding as "no useful positive correlation between pocket-Cα
  reference-separation and per-receptor classifier AUROC on the
  15-receptor S1 set (pooled slope −0.325 [−0.570, −0.068] Å⁻¹);
  the signal is substantially carried by AGTR1, whose active
  reference is a β-arrestin-biased-agonist-bound state (6OS2, TRV026
  + nanobody Nb.AT110i1_le) — a state that may not represent the
  canonical Gα-coupled active reference the classifier is trained
  against; excluding AGTR1 the slope is −0.060 [−0.246, +0.087]".
  This gives the reader BOTH the finding as scored AND the sensitivity.
- **(B) Empirical failure list only, no ref-sep claim**: state
  "AGTR1 inverts on all four backbones (AUROC 0.00–0.10) and CXCR2
  inverts on OF3; the mechanism is not resolved by reference-separation
  or by the checks in this diagnostic; the applicability domain is
  the 14 (or 15) non-inverted receptors as an empirical set, not a
  criterion".

House convention (dispatch: "negative/bounded results get main-text
space") favours (A) — the finding is real as scored, has a clean
sensitivity analysis, and the curation nuance about 6OS2 is a
material limitation worth stating.

---

## Proposals (for adjudication, NOT applied here)

Three proposals, ordered by cost. All are OUT OF SCOPE for this
dispatch (no patch, no shared-corpus edit).

1. **Reference-set relabel** (documentation-only): change
   `refs/reference_set.csv` for AGTR1's active row: `resolved_state`
   from `Ga-coupled-active` to `nanobody-biased-agonist-active`
   (or add a `state_specifier` column). No rescore needed. Touches
   a design-locked file (`refs/reference_set.csv` — PREREG-frozen) so
   requires explicit go per CLAUDE.md.

2. **Reference swap for AGTR1** (rescore-triggering): if a canonical
   Gα-coupled AT1R active reference exists in the PDB and predates
   backbone training cutoffs, swap 6OS2 → that PDB in the AGTR1
   active-role position. Candidates to check (NOT verified here): the
   AT1R-Gq heterotrimer entries deposited post-2019; verify each's
   deposition date against the backbone training cutoffs. If a
   pre-cutoff Gα-coupled AT1R crystal exists, propose the swap in a
   fresh dispatch. If none exists, AGTR1's active reference cannot be
   "corrected" to Gα-coupled without violating the training-cutoff
   discipline — the biased-agonist reference is the best available
   pre-cutoff active-state option.

3. **Curator E2 cross-validation**: instantiate what the dispatch
   called "curator E2" as an actual curator-level receptor-by-receptor
   review of active/inactive PDB choice. AGTR1 is the strongest
   candidate to review first. Cost: 1-2 h per receptor for a manual
   review of RCSB deposition dates + resolved state + ligand
   identity + stabilizer type; ~40-80 h for the full 40-receptor
   Class-A panel. Deferrable; useful for a next campaign.

---

## Outputs

- `docs/AGTR1_REFASSIGN_REPORT.md` — this file.
- `experiments/021_block_c_tier3_pharmacology/analysis/verification/g2_excl_agtr1.json`
  — slopes + CIs, all 4 backbones + pooled, full-15 vs excl-AGTR1-14.
- `scripts/block_c_closeout/g2_excl_agtr1.py`.
- **No** `g2_corrected_agtr1.json` (Section-2 corrected-rerun condition
  not met).

**No commit. No shared-corpus edit. No release/, no push, no tag.
BLOCK_C_CLOSEOUT Parts B/C remain held.**
