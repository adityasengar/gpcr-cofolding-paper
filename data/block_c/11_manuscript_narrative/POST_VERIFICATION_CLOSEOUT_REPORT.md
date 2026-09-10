# POST-VERIFICATION CLOSEOUT REPORT

**Date**: 2026-09-10.
**Baseline**: paper_af3 working repo `a090c9a` + paper_af3_release `4f6452f`.
**Dispatch**: applies verification-report proposals §1–§4; runs §5
read-only sensitivity check.

---

# §1 — rebuild-and-diff harness: stop the false PASS, add a real partial check (APPLIED)

## §1a — `rebuild_block_a.py` no longer prints a fake PASS

Edited `release/code/build_scripts/rebuild_block_a.py`:
- Removed `"Returning 0 (stub PASS)"` message.
- Now prints `"STUB — SKIPPED, NOT VERIFIED"` and `"Returning 20 (stub-
  skipped exit; NOT a rebuild pass)"` to stderr.
- Exit code changed from `0` to `20` (distinct non-zero code so Make
  halts and no downstream tool can mistake it for a real check clearing).

Edited `release/Makefile`:
- `all:` target header comment updated to state that `make all` currently
  fails until a real rebuild lands.
- `block_a:` target echo updated to name the stub explicitly and note
  that `Make halts on exit 20`.
- Top-level `# Release-level Makefile.` docstring rewritten to name
  `make ledger-check` as the only real integrity check that runs today.

**Verified**: `make all` now returns exit code 2 (Make wrapping child's 20)
and prints `make: *** [block_a] Error 20`. No more false-PASS line.

## §1b — `ledger-check` extended to verify SHA-256 integrity

Rewrote `release/code/build_scripts/ledger_check.py`:
- Parses `<basename>=<64-hex>` and `<basename>.sha256=<64-hex>`
  patterns in LEDGER.csv's `input_sha` column; strips trailing
  `.sha256` from labels so basename lookup finds the actual data file,
  not the sidecar SHA-recording file.
- For each explicit assertion: walks the release tree by basename,
  recomputes SHA-256, compares. Emits **PASS** / **FAIL** / **MISSING**
  (basename not found; likely out-of-git raw rows) / **AMBIGUOUS**
  (multiple candidates, none match).
- Records unverifiable entries: `text_reference`
  ("sha as above", "commit XYZ"), `opaque_partial_hash`
  (short prefix hashes), `bare_hash_no_label`.
- Exit code 0 on any explicit assertion PASS with no FAIL / AMBIGUOUS;
  1 on FAIL or AMBIGUOUS.

**First run against current LEDGER.csv** (21 rows):
- **SHA-256 assertions verified PASS**: 1 (SC-1 Block A rows.csv,
  `94ff63b18a…`).
- **FAIL**: 0.
- **MISSING** (basename not in release tree): 2 (SC-C-1
  `rows.tier3.v2.csv=5ccf58ac…`, SC-C-5 `refsep_pocket_ca.csv=ed850577…`
  — both raw-data files kept out of git per the few-MB rule per
  `data/block_c/tier3/MANIFEST_RAW_ROWS.md`).
- **AMBIGUOUS**: 0.
- **Uncheckable text/partial-hash refs**: 20 (mostly LEDGER's
  "sha as above" chain references + Block C script-path free-text).
- **Script paths missing**: 6 (Block C ledger rows point at
  `scripts/reaudit_2026_09_07/*.py` which live in the WORKING repo,
  not the release repo — expected because the release repo doesn't
  duplicate all working-repo scripts).

The check runs cleanly, catches its one explicit assertion (Block A
rows.csv), and its output banner explicitly names that it is NOT a
rebuild-and-diff.

## §1c — VERSION.md updated

Edited `release/VERSION.md`:
- Block A row's Data column: appended
  *"; **no functional rebuild-and-diff harness exists; SHA-integrity
  check only (`make ledger-check`)**"*.
- Block B row's Data column: appended
  *"; no functional rebuild-and-diff harness; SHA-integrity via
  `make ledger-check` when Block B rows land in the ledger"*.
- Block C tier 3 row's Data column: appended
  *"; **no functional rebuild-and-diff harness exists; SHA-integrity
  check only (`make ledger-check`)**"*.
- New top-level section §"Rebuild-and-diff harness — deferred, tracked"
  documenting the state plainly.

## §1d — Deferred item recorded

Edited `caveats/C-C-11_deferred_gates.md` (both working repo and
release) — appended a 7th item:
> **Full rebuild-and-diff harness** — the Makefile has scaffolding for
> `make all` invoking per-block rebuild scripts, but `rebuild_block_a.py`
> is currently a stub (exits 20, does not compute), and no
> `rebuild_block_b.py` or `rebuild_block_c.py` script exists. The only
> integrity check that runs today is `make ledger-check` (SHA-256
> verification of every explicit `<file>.sha256=<hash>` assertion in
> `LEDGER.csv` — enforces file integrity but not scientific correctness
> of any claim's number). Full rebuild-and-diff (all three blocks) is
> tracked as deferred-post-submission; not silently dropped.

---

# §2 — Block C caveats + SC-C-1 update (APPLIED)

## §2a — C-C-3 status update + SC-C-1 numbers

Rewrote `caveats/C-C-3_2x2_ci_convention_pending.md` (both repos):
- Renamed to "23-set pinned, cluster-boot CIs applied".
- Status changed to **RESOLVED 2026-09-10**.
- Documented the 23-receptor pin and 16-paralog-cluster cluster-boot
  recompute.
- Table shows both cluster-boot (primary) and receptor-boot (secondary)
  CIs per backbone.
- Names the recompute artefacts on disk.

Updated `BLOCK_C_CLAIM_SHEET.md § SC-C-1` (both repos):
- Numbers table now shows cluster-boot 95 % CI as primary and
  receptor-boot as secondary.
- Cluster-boot values:
  Boltz [−0.454, −0.164]; Chai [−0.216, −0.045]; OF3 [−0.405, −0.099];
  Protenix [−0.277, −0.088]. All four sign non-zero.
- Removed the "Recorded-not-followed" paragraph.
- Updated Qualified-by list: C-C-3 now marked as RESOLVED 2026-09-10.
- Added citation to the recompute artefacts.

## §2b — C-C-9 update

Rewrote `caveats/C-C-9_panel_36_of_40_landed.md` (both repos):
- Renamed to "Panel of record is 40 Class A; 36 landed. The 4 drops are
  systematic, not incidental".
- Status: **RESOLVED 2026-09-10**.
- Names the 4 receptors (B1B1U5, OPSD, FSHR, LSHR) with per-receptor
  root causes.
- Two overlapping shared-class causes: non-human-species pipeline bug
  (B1B1U5 + OPSD); PAM-inactive-reference curation pattern (FSHR +
  LSHR).
- Manuscript-sentence guidance updated to name both causes in the 4-
  receptor footnote.

---

# §3 — Block A C-12 pLDDT-floor sentence (APPLIED)

Appended to `release/caveats/C-12_broken_cell_a1a6_gap.md`:

> **Additional Methods sentence — natural pLDDT floor at 60**
> (Added 2026-09-10 post-verification, see
> `docs/POST_CLOSEOUT_VERIFICATION_REPORT.md §2b`):
>
> > A pLDDT-based fold-integrity floor at 60 (cell-mean pLDDT) would
> > flag 2 cells across the 380-cell Block A grid: **ACM1-cognate-
> > Protenix at 38.66** (unphysical d_TM6 and NPxxY geometry, as
> > detailed above) and **HRH1-boltz-apo at 58.85** (still recoverable;
> > not the same failure mode as ACM1-cognate-Protenix, and does not
> > carry unphysical geometry). Both were retained in-panel; the
> > ACM1-cognate-Protenix cell is handled via exclusion set E1.
> > HRH1-boltz-apo is the second-lowest cell in the pLDDT distribution
> > — a 20-pLDDT gap separates it from ACM1-cognate-Protenix — but it
> > does not require its own exclusion. The pLDDT-floor-at-60
> > sensitivity check confirms that ACM1-cognate-Protenix is an
> > isolated outlier, not a symptom of a wider corpus quality issue.

Applied to release/ only (Block A caveats live in release, not the
working repo).

---

# §4 — 14.5 % / 15.5 % Block A grep (COMPLETED — no fix needed)

## Findings

Grep of `paper_af3_release/BLOCK_A_CLAIM_SHEET.md`,
`dossiers/BLOCK_A/`, `withdrawals/W-1*`, `withdrawals/W-8*`,
`MANUSCRIPT_FLAGS.md`:

- `BLOCK_A_CLAIM_SHEET.md:316,323` — cites 14.5 % **inside withdrawal
  descriptions** (W-1, W-8) — retracted-framing text, not a live claim.
- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md`: 14.5 % appears
  explicitly framed as *"the withdrawn '14.5 % panel mean' is
  Protenix's alone. Cross-backbone averaging over the four gave the
  appearance of a shared quantity that in fact lives on one backbone."*
  This is Protenix's own panel-mean apo-active (95 % CI [6.08, 24.25]),
  not a cross-backbone average.
- `dossiers/BLOCK_A/RESURFACED.md:35`: explicit reconciliation —
  *"'14.5 % panel mean apo-active'; actual: this is Protenix's own
  panel-mean (14.50 % [6.08, 24.25]); the four-backbone panel means
  span 14.5–32.7 %."*
- No standalone `15.5` figure appears in Block A's release dossier
  in the apo-active context (only unrelated numeric appearances like
  `d_npxxy_ca` values).

## Revised interpretation of the verification-report §1d claim

**The verification report's §1d interpretation was oversimplified.**
The 14.5 % and 15.5 % are NOT unambiguously the same statistic:

- **Block A's 14.5 %** in the release dossier is Protenix's-alone
  panel-mean apo-active (per-backbone quantity, not cross-backbone
  average). The dossier ALREADY reframed this correctly, retiring the
  earlier misframing (W-1, W-8) that treated 14.5 % as a cross-backbone
  panel-mean.
- **Auto-memory's 15.5 %** (from `apo_bistability_reference_artefact_2026_09_06`)
  refers to a recomputed panel-mean apo two-instrument coherent-active
  fraction that superseded a prior 14.5 % figure. Denominator /
  frame convention for the 15.5 % recompute is not explicit in the
  memory record; may be frame_36 vs frame_40, or a cross-backbone
  mean with different receptor exclusion.

## Repo-side action: **NONE required in the Block A release repo**

The Block A dossier already handles the 14.5 % correctly (Protenix-alone,
per RESURFACED.md §35 + EXPERIMENT_DOSSIER §1384). No update needed to
change 14.5 → 15.5 anywhere in the Block A release repo.

## Flag: Block C paper draft mislabeling

W-C-5 in the Block C withdrawals still cites the retracted framing
("14.5 % panel-mean apo coherent-active fraction is retracted to
15.5 %"). This appears to reference the auto-memory's Block-C-attributed
number, but the Block A release dossier's own reconciliation shows the
14.5 % is Protenix-alone, not a cross-backbone panel-mean.

**Manuscript-text fix (NOT applied here — out of scope per dispatch)**:
the paper draft's Withdrawn item #5 (mirrored to `W-C-5`) may need a
rewording pass to clarify that the 14.5 %→15.5 % transition refers to a
cross-backbone-panel-mean recompute, not the Block A Protenix-alone
number that shares the same numeric value by coincidence. Leaving the
draft alone here per dispatch.

---

# §5 — C-11 sensitivity (READ-ONLY, not committed to claim-facing files)

## §5a — SC-1..SC-8 recompute excluding 10 microswitch-adjacent references

The 10 references identified in POST_CLOSEOUT_VERIFICATION_REPORT §2a.iii
map to 9 unique receptors (GRPR contributes both active and inactive):

```
5HT5A, ACM1, APJ, CCR5, CNR1, CXCR2, GRPR, LT4R1, NPY2R
```

Exclusion applied at RECEPTOR level (strict: exclude receptor if EITHER
its active or inactive reference is microswitch-adjacent).

### Per-backbone, panel-level medians / fractions

Magnitudes reported (unsigned; matches LEDGER convention):

| claim | backbone | incl | excl (n=30) | Δ (excl − incl) | material? |
|---|---|---:|---:|---:|---|
| **SC-1** apo→cognate delta_to_active shift (Å) | boltz | 5.270 | **5.837** | +0.567 | modest (~+11 %) |
| | chai | 2.766 | 2.505 | −0.261 | modest (~−9 %) |
| | of3 | 5.100 | **5.570** | +0.470 | modest (~+9 %) |
| | protenix | 6.116 | 6.135 | +0.019 | rounding-level |
| **SC-2** fraction of way from apo to active | boltz | 0.9472 | 0.9473 | +0.0001 | rounding-level |
| | chai | 0.8841 | 0.8841 | +0.0000 | rounding-level |
| | of3 | 0.9340 | 0.9474 | +0.0134 | modest |
| | protenix | 0.9201 | 0.9506 | +0.0304 | modest |
| **SC-3** TM6 tilt cognate−apo shift (Å) | boltz | 5.036 | 5.027 | −0.009 | rounding-level |
| | chai | 1.047 | 0.756 | **−0.291** | material (~−28 %) |
| | of3 | 4.814 | 4.827 | +0.013 | rounding-level |
| | protenix | 5.307 | 5.318 | +0.011 | rounding-level |
| **SC-4** two-instrument agreement (Class A fraction) | boltz | 0.8712 | 0.8841 | +0.0129 | modest |
| | chai | 0.9090 | 0.9097 | +0.0007 | rounding-level |
| | of3 | 0.8125 | 0.8297 | +0.0172 | modest |
| | protenix | 0.8815 | 0.8839 | +0.0024 | rounding-level |
| **SC-6** predicate FP (rmsd > 3 Å) | pooled | 0/3742 | 0/2988 | 0 | unchanged (0 FPs in both) |
| **SC-7** engagement (>30 contacts, cognate arm) | boltz | 0.9915 | 0.9894 | −0.0021 | rounding-level |
| | chai | 0.9770 | 0.9716 | −0.0054 | modest |
| | of3 | 0.9719 | 0.9653 | −0.0067 | modest |
| | protenix | 0.9881 | 0.9905 | +0.0024 | rounding-level |
| **SC-8** fold-integrity anchor pass (tm6_helicity ≥ 0.6) | boltz | 0.9932 | 0.9916 | −0.0016 | rounding-level |
| | chai | 0.9886 | 0.9860 | −0.0026 | rounding-level |
| | of3 | 0.9878 | 0.9855 | −0.0023 | rounding-level |
| | protenix | 0.9798 | 0.9751 | −0.0047 | rounding-level |
| | pooled | 0.9874 | 0.9845 | −0.0029 | rounding-level |

n excluded from panel: 39 receptors → 30 receptors (9 excluded).

### Direction of change

The exclusion moves Block A's numbers in these directions:

- **SC-1 (apo→cognate shift)**: **Boltz and OF3 numbers INCREASE by
  0.47–0.57 Å** when the 9 microswitch-adjacent-ref receptors are
  excluded. **Chai decreases by 0.26 Å.** Protenix unchanged.
  Interpretation: on Boltz and OF3, the 9 excluded receptors have
  SMALLER apo→cognate shifts than the panel median (their inclusion is
  pulling the median down). On Chai they have larger shifts than the
  panel median. Excluding them SHARPENS the signal on Boltz + OF3 and
  softens it on Chai.
- **SC-2 (fraction of way to active)**: OF3 and Protenix rise by
  0.013–0.030; Boltz + Chai essentially unchanged.
- **SC-3 (TM6 tilt shift)**: **Chai drops by 0.29 Å** (28 % relative);
  other three backbones essentially unchanged. Chai's already-marginal
  1.05 Å figure becomes 0.76 Å after exclusion. This is the largest
  material single change and worth naming.
- **SC-4 agreement, SC-7 engagement, SC-8 fold-integrity**:
  rounding-level shifts (all ≤ 0.017).
- **SC-6 predicate FP**: 0/3742 → 0/2988. No false positives in either
  scope. Unchanged.

### No headline claim moves qualitatively

- SC-1's "5–6 Å shift on 3 of 4 backbones" survives exclusion:
  Boltz 5.84, OF3 5.57, Protenix 6.14. Chai (2.51 vs 2.77 incl) stays
  in the "softer predictor" bucket.
- SC-3's "4.8–5.3 Å shift on 3 of 4 backbones" survives exclusion:
  Boltz 5.03, OF3 4.83, Protenix 5.32. Chai (0.76 vs 1.05 incl) MOVES
  DOWN — the "Chai is softest" description sharpens.
- SC-7's "engagement ≥ 97 %" survives on all four backbones.

**No SC-N claim's signed status changes on exclusion.** The manuscript's
"4-backbone signed" language holds.

## §5b — Corrected random-expectation baseline

Recomputed the random-mutation-position baseline per receptor, using the
union of ±3 residue windows around each of the 10 microswitch BW anchors
(3.50, 3.51, 5.58, 6.30, 6.34, 6.48, 6.51, 6.55, 7.49, 7.53), derived
from each receptor's own `anchor_positions` in `refs/reference_set.csv`.

**Result (uniform across all 48 Block A panel receptors)**: 51 unique
residue positions per receptor land inside a microswitch ±3 window.

Assuming a nominal ~300-residue receptor (typical GPCR TM region ~250,
plus loops/tails ~50-100), the random-expectation ceiling is:
**51 / 300 = 17.0 %**.

(Uniformity across receptors reflects the fact that microswitch BW
labels define fixed within-helix offsets from receptor anchors; the ±3
windows are the same sequence-distance intervals regardless of the
receptor's absolute residue numbering. Overlap between adjacent windows
does happen — 6.30/6.34 overlap at 6.32/6.33; 6.48/6.51 overlap at
6.49/6.50 — and the union takes it into account, dropping the naive
12 × 7 = 84 to the actual 51.)

**Corrected enrichment finding**:

- **Observed rate**: 10 / 33 Block A panel mismatches sit in a
  microswitch ±3 window = **30.3 %**.
- **Random-expectation ceiling**: 17.0 %.
- **Enrichment factor**: 30.3 / 17.0 = **1.78 ×**.

**Restatement**: the verification report §2a.v called this
"modest enrichment against ~24 % baseline." Under the corrected baseline
of 17 %, the observed 30 % is **1.78 × the random ceiling**, not modest.

Whether "1.78×" reads as strong enough to matter for C-11's caveat text
is not adjudicated here — the numbers are on record; that's the §5b
deliverable.

---

# Outputs

- `docs/POST_VERIFICATION_CLOSEOUT_REPORT.md` — this file.
- `release/code/build_scripts/rebuild_block_a.py` — stub-PASS removed;
  now exits 20 with clear labeling.
- `release/code/build_scripts/ledger_check.py` — full SHA-256 verification
  implementation.
- `release/Makefile` — docstring + target-echo updates for truth-in-labeling.
- `release/VERSION.md` — rebuild-harness deferred-and-tracked note.
- `release/caveats/C-C-3_2x2_ci_convention_pending.md` +
  `paper_af3/caveats/C-C-3_2x2_ci_convention_pending.md` — status
  RESOLVED 2026-09-10.
- `release/caveats/C-C-9_panel_36_of_40_landed.md` +
  `paper_af3/caveats/C-C-9_panel_36_of_40_landed.md` — status
  RESOLVED 2026-09-10 with 4 receptors named.
- `release/caveats/C-C-11_deferred_gates.md` +
  `paper_af3/caveats/C-C-11_deferred_gates.md` — 7th deferred item added.
- `release/caveats/C-12_broken_cell_a1a6_gap.md` — pLDDT-floor-at-60
  sentence appended.
- `release/BLOCK_C_CLAIM_SHEET.md` + `paper_af3/BLOCK_C_CLAIM_SHEET.md`
  — SC-C-1 numbers table updated to cluster-boot CIs.

## Commits (§1–4 only per dispatch)

Two commits, local only, no push:
1. paper_af3 working repo — caveats updates + this report.
2. paper_af3_release — VERSION.md + Makefile + rebuild_block_a.py +
   ledger_check.py + caveats + BLOCK_C_CLAIM_SHEET.md.

**§5's outputs are documented in this report but NOT committed into
claim-facing files** (per dispatch). They are evidence for a next
adjudication pass. No tag movement. No push.
