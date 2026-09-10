# What Block D still needs from the pipeline

Written 2026-09-10 on intake of `block_d_figure_data.zip`
(SHA-256 `c000b1636e1846c6…`). Companion to
`analysis/block_d/DISCREPANCY_REPORT.md` and `rebuttals/BLOCK_D.md`.

**Almost all of this document is one ask.** Block D shipped no row-level data,
so eleven of the twelve items below either are that ask or are downstream of it.
That is unusual and it is worth saying plainly rather than burying in a list:
the bundle's *documentation* is the best of the four blocks — GATE-2 refits the
headline slopes from scratch and finds they reproduce under exactly one
predictor convention, GATE-1 and GATE-4 chase provenance, ten withdrawal records
name claims that were tested and dropped — and its *evidence* is the thinnest,
because none of it can be re-run here.

Cost classes: **free** (re-analysis of data already held), **cheap** (re-scoring
existing predictions, no new inference), **real** (new predictions).

---

# Rank 1 — a manuscript sentence depends on the answer

## 1. The three row-level corpora. **free** — and it is eleven of the twelve asks in this document

**What we need.** The three files the claim sheet names by path:

```
experiments/022_tier_d1_deep_apo/analysis/full/rows.csv           14,000 rows
experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv   2,370
experiments/024_tier_d3_msa_depth/analysis/full/rows.csv          25,810
```

**Manuscript locator.** The entire directed-generation Results section, and the
final paragraph of it, which currently states that no headline fraction in the
block could be recomputed here.

**What it unblocks, precisely.** Twelve claims are recorded as PROSE-ONLY in
`verify_claims.py`. SC-D-1's per-cell fractions, SC-D-2's 6.6% ceiling, SC-D-3's
CNR2 double saturation, SC-D-5's three deltas, SC-D-8's sub-Ångström and
pLDDT and matched-seed lines, SC-D-9's entire 5 × 6 concordance table, SC-D-10's
cross-tier divergence, SC-D-11's Block A reproduction and SC-D-12's fold
descriptors. Not one of them can be checked against anything but another
sentence in the same bundle.

**Promised?** Yes — by the claim sheet, by name and by path, in its own header.

## 2. The bootstrap draws behind SC-D-8's four intervals. **free**

**Manuscript locator.** The four slope intervals quoted in Results, and
Figure BD-3, which prints them above each panel.

GATE-2 refit the four **point estimates** independently and reproduced them
exactly under `ln(depth)` with `full = 4096` — that is real corroboration and we
say so. But the cluster-boot intervals rest on draws that did not ship, so
`[-2.69, -0.81]` and its three siblings are transcribed values with nothing
behind them here. This is the gap between "the slope is −1.68" (corroborated)
and "the slope is signed" (not).

**Promised?** Implicitly, by quoting a 95% CI.

## 3. The seven D2 cells that were never populated. **free**

**Manuscript locator.** The D2 subsection's n, and Figure BD-2's caption.

The claim sheet's 2,370 reconciles exactly one way: 44 cells at n = 50, plus the
one 170-prediction cell C-D-5 documents, which implies **45** populated cells.
`PARTA_D2.md §2` says 44. The nominal grid is 13 arms × 4 backbones = **52**. So
seven cells are absent and are named nowhere.

We also need C-D-5's own arithmetic settled. It argues with itself inside its own
parentheses about whether a cell is 50 or 200 predictions. Every interval in the
claim sheet reproduces at n = 50 and none at n = 200, so we have written 50; a
one-line confirmation would close it.

## 4. OpenFold-3's training cutoff, as a date. **free**

**Manuscript locator.** The Methods sentence on the memorization confound, and
Figure BD-2's caption, which is the most load-bearing caption in the block.

C-D-12 is the campaign's largest caveat and it rests on all four nanobody
anchors predating every backbone's cutoff. Three cutoffs are dated in
`nanobody_state_anchors.csv`; the fourth column is literally named
`cutoff_of3_TBD`, and `ASSUMED_NOT_VERIFIED_BLOCK_D.md` confirms the lookup was
never done. All four anchors are 2013–2020 so no plausible answer changes the
conclusion — but the paper should not assert a date nobody has established.

## 5. The freeze tag, or a statement that the block ships unfrozen. **free**

The claim sheet's first line marks it **DRAFT** with `block_d_freeze` **not
placed**, held pending the §2.4 post-cutoff test. Flag D-8 then records that the
same test closed on the same day and that main-text framing is **locked**. The
condition has resolved and the tag has not followed. We have written the
Methods sentence saying the block is unfrozen; we would rather write that it is
frozen.

---

# Rank 2 — no sentence depends yet, but a claim we want does

## 6. Whichever of the fifteen structures Part A actually measured. **free**

`PARTA_D1.md §4` tabulates an NPxxY-OH distance for five D1 structures and
introduces them as "Five CIFs pulled from …" — the same five that ship, all
carrying one seed and one `sample_idx` in the manifest. Measured from the
coordinates they differ by up to 0.51 Å (D-D-8). No call changes. Either the
shipped file is a different sample from the measured one, or the two use
different atom conventions; the bundle does not say and there is no third source.

Related, and cheaper to fix than to explain: `MANIFEST.json`'s `dossier_finding`
for `d3_protenix_agtr1_depth8.cif` quotes "NPxxY 11 → 3.4 A", which is GATE-3's
**50-sample cell median**, beside a **single** coordinate file that measures
3.56 Å. Our own checker reported that as a discrepancy before the gate report
had been read. A manifest entry describing one file should carry that file's
value.

## 7. The three random-set structures that failed to pull. **cheap**

The random set is documented as seven and landed four; the manifest preserves
the SSH-throttle error text for the three, which is exactly the right way to
record it. A "does the corpus look sane" check on 4 of an intended 7 is worth
re-running rather than caveating.

## 8. A named source for the Block A cross-tier reproduction. **free**

SC-D-11 and Flag D-5 are the strongest result in the block — the four D1
outlier cells reproducing at ≥ +50 points on Block A's independent apo rows at
n = 25/cell. Which Block A rows, under which filter? We hold Block A and would
recompute this ourselves, which would make it the only Block D claim verifiable
end-to-end from data we possess.

---

# Rank 3 — table integrity; nothing depends on these today

## 9. An index file for the bundle. **free**

Ten numbered directories arrive with no README, no manifest of contents and no
data dictionary. The dispatch that accompanied the zip supplies a folder map;
the zip does not. Every previous block shipped one.

## 10. The phantom scorer SHA, already self-reported. **free**

W-D-10 and C-D-3 record that `891041e858f3747b` appears in two headline
documents and an auto-memory file and exists in no git history, and that the
row-level `d9c646af` is authoritative. Recorded here only so it is not
re-discovered: the correction is the pipeline's own and we have adopted it.

## 11. The derivation script for the D3 slopes. **free**

C-D-2 and GATE-2 both record that no script computed them and that GATE-2
grepped the experiment tree for seven plausible names and found nothing. GATE-2
then refit them by hand and reproduced them exactly. A committed script would
turn a one-off reproduction into a repeatable one.

## 12. TM6-tilt calibration on the nanobody anchors. **cheap**

`ASSUMED_NOT_VERIFIED_BLOCK_D.md` records it as deferred at roughly thirty
minutes of compute. NPxxY calibration on those anchors is done and passes on all
four; the tilt axis is the other half of the two-instrument predicate and the
negative result in the inactive direction is the block's most contested claim.
Half a calibrated instrument is an argument a referee will make for us.

---

# Not requested, deliberately

**Per-receptor D3 slopes.** `PARTA_D3.md §3` breaks them out by family at 2–8
receptors per cell. We will not build on them and are not asking for more; the
panel-level slopes already carry intervals that cross zero on one backbone.

**A rerun of anything.** Every ask above is `free` or `cheap` except none —
there is no `real` item in this document. Block D's problem is not that the
predictions are wrong or missing. They were run, scored, audited and withdrawn
from where they did not hold. They simply were not shipped.

**The two-state-versus-one-state framing.** Settled in the dossier §6.5 and
locked; we have represented it as written and are not reopening it.

---

# Open questions about the data itself

**A. Is the 170-prediction cell inside Part A's 44, or a 45th?** The arithmetic
says 45; the heading says 44. One sentence settles it.

**B. Why is `sample_idx` 5 and `seed` 1015473677 on all five D1 spot-checks?**
Five different receptor × backbone cells sharing one seed and one sample index
is consistent with a deliberate fixed pull rule, and we have assumed that. If
instead it is a placeholder, D-D-8's comparison is invalid and we would withdraw
it.

**C. What was the intended D2 grid?** 13 arms × 4 backbones × 50 is 2,600 and
2,370 shipped. Whether the seven missing cells were never dispatched, dispatched
and lost, or deliberately excluded changes whether SC-D-6's panel-scale negative
is over four receptors or over fewer.

**D. Does the D1 500-sample budget apply to all seven receptors?** 7 × 4 × 500 =
14,000 exactly, so on the arithmetic yes. Recorded because the D2 and D3 totals
both fall short of their nominal grids and D1's does not.
