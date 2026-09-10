# Block C — discrepancy report

`verify_claims.py`: **53 checks, 53 reproduce, 0 do not.**

That is the first drop in this project where nothing in the claim sheet
disagrees with the shipped data. Block A ran 34 checks with 15 mismatches in 23
groups; Block B ran 109 with 21 mismatches in 8 groups. Block C: none.

**Read the next section before taking that at face value.**

---

## D-C-1 — Most of Block C is not independently checkable, and that is the finding

**Severity: high, and it is structural rather than an error.**

Blocks A and B shipped their prediction rows — 9,490 and 32,000 — so every
headline could be recomputed from source. **Block C ships one row-level file**:
`12_g4_off_site_census/g4_full_census_v2.csv`, 40,000 rows. Everything else
arrives as summary JSON, with the source table named by SHA-256 and not
included.

So the 53 checks split into two kinds, and the script labels every one:

| kind | n | what a green result means |
|---|---:|---|
| **RECOMPUTED** | 23 | derived from the census CSV, independent of any summary |
| **CONSISTENCY** | 30 | the same number read from two or more shipped files and compared |

A green CONSISTENCY check catches transcription error and staleness. **It cannot
catch a computation that was wrong in the same way in every file.** That is
exactly how Block B's per-backbone family shares passed their own
`matches_claim_sheet_bool` column while reproducing from nothing.

**What this means in practice.** SC-C-1's 2×2 interaction and SC-C-4's
classifier — the block's two surviving positives — are **not recomputable from
this bundle**. We can confirm the README, the claim sheet and the JSON agree with
each other. We cannot confirm any of them against the data.

This is not an accusation. It may be entirely deliberate: `rows.tier3.v2.csv` is
pinned by SHA and the analysis directories are consistent. But the paper cannot
say a number was verified when what was verified was a transcription, and our
Methods should not imply otherwise.

**Requested:** `rows.tier3.v2.csv` (SHA `5ccf58ac…`), or a tidy per-receptor
export sufficient to recompute the 2×2 interaction and the LORO folds.

---

## What reproduced, and what it took to get there

**The corrected off-site census, in full.** 40,000 rows; the three bands
recompute exactly — 25,559 in-pocket, 7,349 entrance-bound, 7,092 off-site,
pooled 17.73%. Per arm: apo **15.1%**, cognate **20.3%**. SC-C-1's numerator,
small-molecule apo × {agonist, antagonist}: **1.52%** on n=9,800.

**The v1 retraction is confirmed as a retraction.** The withdrawn 25.6% pooled
figure does not reproduce from the corrected census under any band definition;
the pooled value is 17.73%.

**The Chai far-mode tail.** 176 rows at or beyond 60 Å, **175 of them on
Chai** — exactly as the dispatch states. A single-backbone pathology, not a
block-wide qualifier.

**Peptide agonists at 17.5 Å median.** Confirmed, and the contrast is sharper
than the dispatch spells out: in the *same* apo agonist/antagonist cells,
small-molecule ligands are off-site on **1.52%** of rows and peptide ligands on
**66.53%**. Reporting a pooled number across both would produce a fictitious
failure rate. This is the single most dangerous number in the bundle for anyone
who filters by role name instead of by ligand type.

**The four dropped receptors.** B1B1U5, OPSD, FSHR and LSHR are absent from the
census, matching C-C-9. Two of those — B1B1U5 and OPSD — are the two non-human
receptors we independently identified in the panel-species audit, which the
drop calls "non-human-species pipeline failures". The two accounts agree.

**The structures.** 14 CIFs present, 7 targeted and 7 random. The bundle
`README.md` index says 2 files for that directory; the dispatch's §4(n) already
flags the index as stale and the data as correct. Confirmed.

**The Flag C-12 / C-C-3 conflict** the dispatch names in §4(m) is real and
present in the shipped files: Flag C-12 still reads "not recomputed" while
C-C-3 is marked RESOLVED and `g_scc1_cluster_boot.json` exists. C-C-3 wins, per
the dispatch. Logged for upstream correction.

**Cluster-boot is genuinely cluster-boot.** `g_scc1_cluster_boot.json` carries
`cluster_boot` and `receptor_boot_recomputed` as separate blocks with different
values, and the README quotes the cluster interval. Block A shipped a column
headed "cluster-boot" containing receptor-boot values; **Block C does not repeat
that defect**, and this was checked explicitly on all four backbones.

---

## Four checker bugs of mine, fixed before this report

Named so nobody re-reports them, and because the pattern is now consistent
enough to be worth stating: **on every block, my first run has been wrong before
the drop has.**

1. **I assumed off-site began at 8 Å.** The census uses three bands — in-pocket
   ≤8, entrance-bound 8–15, off-site >15 — with entrance-bound adjudicated a
   **valid pose**. My guess reported 34.8% against a claimed 15.1% and would
   have looked like a large discrepancy in the drop. The threshold is stated in
   the census JSON at `thresholds.off_site_A_lower`; I did not read it first.
2. **I filtered small-molecule rows by role name.** The role vocabulary is
   `{full_agonist, neutral_antagonist, decoy_lig}` and peptide agonists sit
   *inside* `full_agonist`. Filtering by name gave 16.76% against a claimed
   1.52% — the peptide rows leaking in. The correct filter is
   `ligand_source == "hetatm"`.
3. **I looked for the CIs at the wrong JSON depth**, under `ci_lo` rather than
   `cluster_boot.ci_lo`.
4. **I guessed key names for the threshold** instead of reading the file's own
   `thresholds` block.

Every one of these produced a plausible-looking discrepancy that would have gone
upstream as a finding.

---

## D-C-2 — 66 data files are named in Block C's own documents and not shipped

**Severity: high. This is the answer to "do we have all the results?" — no.**

The bundle is **complete as declared**: all thirteen directories match the
`README.md` index exactly, except `13_structures/`, whose index entry the
dispatch already flags as stale (it says 2 files; 16 are present, correctly).
All ten claims, eleven caveats and ten withdrawals are there.

What is missing is everything the bundle *refers to*. Scanning every `.md` and
`.json` in the drop for named `.csv`/`.json` files and checking each against
what shipped: **66 named, not present.**

Two are already covered from elsewhere in this repo and need no request:

- **`paralogy_clusters.csv`** — the resampling unit for every cluster-boot CI in
  the block. We hold a copy from Block B, and its SHA-256 is
  `6158081e…`, **byte-identical to the one `g_scc1_cluster_boot.json` names as
  its input**. 40 receptors, 26 clusters. Verified, not assumed.
- **`C-8_cluster_bootstrap_authoritative.md`** — Block A's convention document,
  present at `data/block_a/10_narrative/caveats/`.

### The two that block verification

| file | what it carries | claims affected |
|---|---|---|
| `rows.tier3.v2.csv` (SHA `5ccf58ac…`) | the primary corpus | SC-C-1, 2, 3, 4, 6, 9 |
| `rows.csv` (scorer `d9c646af…`) | the pose sibling corpus | SC-C-7 |

Without these, 30 of our 53 checks are consistency-only. The off-site census is
the one row-level file in the bundle and it carries centroid distances, not
pocket-Cα RMSD, so it cannot substitute.

### Whole analyses whose outputs are named and absent

These are not provenance stubs. Each is referenced as a completed piece of work
with a filename, and several would materially change what the paper can say:

- **`s4_bw_decomposition.json` / `s4_bw_position_decomposition.json`** — a
  Ballesteros–Weinstein **position** decomposition. This is the only mechanistic
  analysis named anywhere in Block C: *which residues carry the ligand-class
  signal.* The paper currently has no residue-level account in any block.
- **`task6_p0_correlation.json`** — a **cross-block** correlation on
  **n=35 common receptors**. Block A, B and C have never been related to one
  another quantitatively; this is the only file that claims to.
- **`task_D_species_match_root_cause.json`** — the root cause of the species
  failures. We independently found that B1B1U5 (jumping spider) and OPSD
  (bovine) are the panel's two non-human receptors, and C-C-9 attributes their
  loss to "non-human-species pipeline failures". This file apparently explains
  the mechanism.
- **`s7_nulls_ceilings.json`, `s7_s8_ceiling_domain.json`,
  `s8_applicability.json`** — the nulls, ceilings and applicability work behind
  SC-C-5.
- **`task_F_v2_apo_bistability_recheck.json`** and four sibling `task_F_*`
  files — apo bistability and reference-state stratification.
- **`nan_reason_census.csv` / `nan_reason_census_by_receptor.csv`** — why cells
  are unmeasurable, which is the evidence behind C-C-1's saturation claim.
- **`pr1`–`pr5`** — five pre-registered checks, including
  `pr2_fshr_lshr_class.json`, the basis for two of the four C-C-9 drops.
- **`s6_generalization.json`**, `s2_sample_budget.json`, `s3_cross_backbone_consensus.json`.

### One absence that is correct

`g4_scoped_centroid_census.csv` and `.json` are the **retracted v1 census** that
produced the 25.6% figure. They are named only in the superseded wrap report and
their absence is right — the retraction is recorded in prose without shipping the
bad numbers in a form a figure script could read.

### What we are asking for

1. **`rows.tier3.v2.csv`** — without it, the block's two surviving positives
   cannot be verified against anything but themselves.
2. **`s4_bw_decomposition.json`** — a residue-level result the paper does not
   otherwise have.
3. **`task6_p0_correlation.json`** — the only quantitative link between blocks.
4. **`task_D_species_match_root_cause.json`** — it bears on a panel-composition
   problem we found independently.
5. A statement of whether the other 60 are deliberately excluded as working
   record, or simply were not gathered. **"Tidy data only" is a defensible
   policy**; the point is that the bundle does not say which of the 66 fall
   under it.

---

## D-C-3 — SC-C-2's table is headed "Kendall's τ" and contains a fraction of receptors

**Severity: high. It reached our manuscript before a panel caught it.**

`BLOCK_C_CLAIM_SHEET.md` § SC-C-2 presents:

> **Numbers** (Kendall's τ, receptor-panel-median):
>
> | panel | boltz | chai | of3 | protenix |
> | Tier 3 apo × 23 | 74% | 65% | 74% | 87% |

Those values are **not** Kendall's τ and they are **not** a median. They are the
`fraction_positive_significant` field of the same JSON's own `summary` block —
the proportion of receptors whose τ is positive *and* significant.

| backbone | claim sheet "τ" | what it is | actual median τ |
|---|---:|---:|---:|
| Boltz-2 | 74% | fraction_positive_significant 0.7391 | **0.386** |
| Chai-1 | 65% | 0.6522 | **0.259** |
| OpenFold3 | 74% | 0.7391 | **0.328** |
| Protenix2 | 87% | 0.8696 | **0.366** |

Both quantities are real and both are worth reporting. The defect is the label:
a reader told "Kendall's τ of 74%" will take it as a correlation of 0.74, which
is roughly **twice** the true value.

**Reproduce.**
```bash
python3 -c "
import json, numpy as np
o=json.load(open('data/block_c/07_ordinal_recovery/s5_p4_ordinal.json'))
t=o['tier3_apo_23_receptors']
for bb in ['boltz','chai','of3','protenix']:
    taus=[v['tau'] for v in t['per_backbone'][bb].values()]
    print(bb, 'claim-sheet %.0f%%' % (100*t['summary'][bb]['fraction_positive_significant']),
          'median tau %.3f' % np.median(taus))"
```

**We published the mislabel and have corrected it.** The Results said *"gives
Kendall's τ of 65–87% across backbones"*. It now says a positive and significant
τ on 65–87% **of receptors**, states that this is a count rather than a
correlation, and gives the median τ (0.26–0.39) beside it.

**How it was caught, which is the point.** The claim sheet, the dispatch and our
own Results all carried the mislabel and all read fine. It surfaced only when
BC-2 was built and the per-receptor τ values were plotted: the violins sat around
0.3 while the panel medians printed 0.74. **A number that survives three prose
reviews can still be wrong, and drawing it is what finds out.**

**To close.** Relabel the SC-C-2 table, or report both columns. The underlying
JSON is correct and self-describing; only the claim sheet's heading is wrong.

## D-C-9 — NEW: the 2x2's scope cannot be confirmed, and its own cell counts are mislabelled

Raised 2026-09-10 when the corpus session rendered BC-1 and found the panel
asserting **"APO ARM ONLY"** on its face while the SI caption beneath it said
the shipped counts contradict that by a factor of two. A figure and its own
caption disagreeing on one page is what a referee circles.

**Checked, and neither side is confirmable from the bundle.**

`06_2x2_interaction/stage3_2x2_ligand_state_specificity.json` **ships no row
counts at all.** Its only per-cell field is `n_clusters`, and it holds 28 for
the agonist cells and 23 for the antagonist ones. Those cannot be cluster
counts: SC-C-1 resamples **16** paralog clusters over 23 receptors, and 28
exceeds the receptor count outright. The field is holding receptor counts under
a cluster name — a third self-mislabelled column in this block, after SC-C-2's
"Kendall's tau" that holds a fraction of receptors and `flag_low_confidence`
that cannot fire.

The census *can* be decomposed by role and arm, which was thought not to be
possible, and it does not settle the question either:

| role | receptors | rows per backbone, per arm | both arms |
|---|---:|---:|---:|
| `full_agonist` | 35 | 1,750 | 3,500 |
| `neutral_antagonist` | 29 | 1,450 | 2,900 |

Both arms are equally populated across the whole census, 20,000 / 20,000. But 35
and 29 are **supersets** of the 2x2's 28 and 23, so the census neither confirms
nor refutes the arm filter on the subset the interaction was estimated on.

**What is true, and what the panel now says.** The apo-only scope is stated as
*intent* rather than as fact, with one clause recording that the shipped files
cannot confirm the filter was applied. The design reason for wanting apo-only is
sound and is kept: with a cognate Ga in the complex the contrast cannot be
attributed to the ligand, because the partner supplies both mass and a strong
conformational preference of its own.

`rows.tier3.v2.csv` settles it in one line and did not ship. **It is the same
file the G4 gate needs** — Block C `DATA_REQUESTS.md` ask 1 now blocks two
separate Block C claims, which raises its priority above everything else in that
document.

**A correction to how this was reported to us.** The escalation cited shipped
`n_rows` of 2,800 and 2,300. Those values are not in the file; only `n_clusters`
is. The 2x factor was inferred rather than read, and the inference may well be
right — 28 x 100 is 2,800 — but it is not something the bundle states.

