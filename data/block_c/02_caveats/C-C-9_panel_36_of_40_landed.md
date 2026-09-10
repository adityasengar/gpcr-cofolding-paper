# C-C-9 — Panel of record is 40 Class A; 36 landed. The 4 drops are systematic, not incidental

**Applies to**: every manuscript sentence quoting "40 Class A receptors"
or a per-receptor statistic that would otherwise imply 40 denominators.

**Status: RESOLVED 2026-09-10** — the 4 dispatched-not-landed receptors
are enumerated below and both root causes are named. The panel is not a
random 36 of 40; the 4 drops share class-property patterns that would
recur on any similar dispatch.

## The 4 dispatched-not-landed receptors

**B1B1U5** (jumping spider rhodopsin, non-human) — SYSTEMATIC.
- Dispatched: yes; 400 prediction paths present in `rows.tier3.v2.csv`.
- Landed with `passed=True`: no; all 400 rows carry `passed=False`,
  `A5_species_match=A5SpeciesMismatch`, and `receptor_slug=nan`.
- Root cause: species-mistagging pipeline pattern per
  `docs/AUDIT_TRAIL.md §21`. The species-fix landed AFTER the Block C
  dispatch fired; pre-fix rows retain the failure flag. Would recur on
  any non-human receptor whose species metadata wasn't in the pipeline's
  species map at scoring time.

**OPSD** (bovine rhodopsin, non-human) — SYSTEMATIC.
- Same rows-present-but-failing pattern as B1B1U5: 400 rows,
  `passed=False`, `A5SpeciesMismatch`, `receptor_slug=nan`.
- Same root cause: non-human species not in the pre-fix pipeline map.

**FSHR** (Class-A glycoprotein hormone receptor) — SYSTEMATIC.
- Dispatched: **no**; 0 rows in `rows.tier3.v2.csv`.
- Root cause (per
  `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/pr2_fshr_lshr_class.json`):
  Block C Stage 2 dropped FSHR because inactive-reference PDB 8I2H is
  "FSH + compound-21f PAM at 6.00 Å" — a positive-allosteric-modulator
  bound in the "inactive" pocket, not a clean orthosteric antagonist
  reference. FSHR IS Class A per GPCRdb (glycoprotein hormone receptor
  family, UniProt P23945).

**LSHR** (Class-A glycoprotein hormone receptor) — SYSTEMATIC.
- Dispatched: **no**; 0 rows.
- Same reason as FSHR: inactive PDB 7FIJ is "hCG + Org43553 allosteric
  agonist" — non-clean inactive orthosteric reference.

## Two overlapping shared-class causes

- **Non-human-species pipeline bug** (2 of 4): B1B1U5 + OPSD. Fires on
  any non-human receptor whose species metadata wasn't in the pipeline
  species map at dispatch time. Independent of the receptor's biology.
- **PAM-inactive-reference curation pattern** (2 of 4): FSHR + LSHR.
  Fires on any receptor in a subfamily whose deposited "inactive"
  references carry allosteric agonists / positive allosteric modulators
  in the pocket, disqualifying them as clean-orthosteric-antagonist
  references. Glycoprotein hormone receptors are the affected
  subfamily.

**Neither drop is incidental.** Both patterns would recur on any
future dispatch against similar receptor classes. The 36-landed panel
is thus not a random subset of the 40-panel; the 4 drops are
structurally consistent with these two shared causes.

## Rows failure rate

800 of 40,800 rows fail on the OPSD/B1B1U5 A5_species_match pattern.
These 800 rows are the B1B1U5 (400) + OPSD (400) rows that dispatched
but failed at scoring. FSHR + LSHR contribute 0 rows.

## Consequence

All Block C analyses run on the 36 landed receptors. Any manuscript
sentence saying "our 40-receptor Class-A panel" needs either:
- **(a)** a Methods footnote naming the 4 dropped receptors and both
  root causes (non-human-species pipeline bug for B1B1U5 + OPSD;
  PAM-inactive-reference curation for FSHR + LSHR), OR
- **(b)** language change to "36 receptors landed of a 40-receptor
  Class A panel of record" with the same 4-receptor footnote.

Downstream analyses that condition on `passed=True` operate on
40,000 rows; the S1 15-set is a subset of the 36 landed receptors after
2×2 common-set filtering.

## Sources

- `rows.tier3.v2.csv` receptor_slug distinct-count = 36 (37 including
  `nan`, which absorbs the 800 A5-species-mismatch rows).
- `refs/tier3_panel.csv` receptor_slug distinct-count = 40.
- `experiments/021_block_c_tier3_pharmacology/signal_recovery_2026_09_07/pr2_fshr_lshr_class.json`
  for the FSHR / LSHR Stage 2 drop reason.
- `docs/AUDIT_TRAIL.md §21` for the species-mistagging pattern.
