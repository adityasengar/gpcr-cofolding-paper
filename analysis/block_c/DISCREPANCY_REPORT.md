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
