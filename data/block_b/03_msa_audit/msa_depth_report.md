# MSA depth report — Block A + Block B unique sequences

Zero-GPU, read-only audit of the Chai MSA cache on HPC
(`/hpc/scratch/sengaad1/paper_af3/msa_cache/chai/*.aligned.pqt`). Covers
every unique sequence fed to any backbone across Block A and Block B:
the 48-receptor panel of record, the 5 canonical cognate Gα partners, the
40 Block B decoy Gα constructs, and (for completeness) the 24 other
`partners.fasta` entries used in earlier Block A partner-diversity work.

Depth = row count in the `.aligned.pqt` (includes the 1 `query` row, i.e.
the input sequence itself, plus all `uniref90` and `bfd_uniclust` hits).

## Overview

**Unique-sequence census** (by `sha256(sequence.upper()).hexdigest()`,
not by 8-char header hint):

| Source | Entries | Unique sequences |
|---|---:|---:|
| `refs/panel_receptor_sequences.fasta` | 51 | 51 |
| `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` | 29 | 29 |
| `refs/constructs_block_b/*_decoy.fasta` | 40 | 40 |
| `refs/constructs_block_b/*_shuffled.fasta` | 40 | **0 new** (all 3 sha values already counted under partners.fasta) |
| **Total unique sequences** | | **120** |

Cross-checked against the HPC cache: **120 unique local sequences ↔ 120
cache files, exact 1:1 match, zero orphans in either direction.** Every
sequence anyone could have dispatched to Chai/Boltz/Protenix/OF3 across
Block A and Block B has a pre-computed MSA on disk; every cache file
traces to a known sequence.

**Scope correction vs. the original task framing**: `panel_receptor_sequences.fasta`
contains 51 entries, not 40. Breakdown:
- **40** Class A receptors (the original panel).
- **8** Class B (CRHR1, GCGR, GLP1R, PTH1R) + Class F (FZD4, FZD6, FZD7,
  SMO) receptors, tagged `source=chai_input_2026_09_01_addendum` — these
  are exactly the remainder of CLAUDE.md's 48-receptor panel of record
  (40 Class A + 4 Class B + 4 Class F).
- **3** construct **variants** of receptors already in the 40: `ADRB1`
  G389R polymorphism, and second-sequence variants of `FSHR` and `MCHR1`
  (both tagged `chai_input_2026_09_01_addendum`, different construct
  boundaries than their Class-A entries — not new receptors).

40 + 8 + 3 = 51. Per coordinator direction: the primary receptor table
below covers all **48** (Block A dispatched all 48 per PREREG §1; Block B
is Class-A-only, so the 40-subset is what applies to Block B specifically).
The 3 variants are broken out in their own appendix table.

**Block A vs Block B coverage**: Block A used all 48 panel receptors ×
(cognate Gα + assorted exploratory partners, hence the 24 `other_partner`
entries). Block B uses only the 40 Class A receptors × 2 arms (shuffled,
reusing cognate-class Gα sequences with zero new uniques; decoy, 40 new
scrambled-α5-CT Gα constructs). No Block-B-specific receptor sequences
exist — same panel, same MSAs, already warmed.

**Format note (pairing_key / comment)**: full pass across all 120 files
confirms `pairing_key` and `comment` are **empty-string on every single
row of every file** (`nunique()==1`, value `''`, in all 120). The only
depth stratification recoverable from `.aligned.pqt` is by
`source_database` (`uniref90` / `bfd_uniclust` / one `query` row per
file). There is no paired-MSA-specific subset encoded in these columns —
contrary to what the column names suggest. **Any future analysis of
paired-MSA-specific effects (e.g. does the *paired* subset drive
receptor–Gα docking coevolution differently from each chain's
individual-search hits) will need to re-derive that split from raw a3m
files if archived, or from ColabFold API response metadata that never
made it into this `.aligned.pqt` cache.** This cache format only supports
per-database, not per-pairing-mode, depth analysis.

## Receptor MSA depth table (48, sorted by depth)

| Receptor | Class | Species | Length | Total | UniRef90 | BFD/Uniclust | Flag |
|---|---|---|---:|---:|---:|---:|---|
| CNR2 | A | human | 360 | 1996 | 1546 | 449 |  |
| SMO | F | human | 787 | 3404 | 2458 | 945 |  |
| LSHR | A | human | 699 | 3590 | 2624 | 965 |  |
| EDNRA | A | human | 427 | 3610 | 2331 | 1278 |  |
| CNR1 | A | human | 472 | 3647 | 2249 | 1397 |  |
| FSHR | A | human | 695 | 3752 | 2639 | 1112 |  |
| EDNRB | A | human | 442 | 4670 | 2939 | 1730 |  |
| LPAR1 | A | human | 364 | 6124 | 4465 | 1658 |  |
| MCHR1 | A | human | 353 | 6217 | 4311 | 1905 |  |
| FZD6 | F | human | 706 | 6819 | 4994 | 1824 |  |
| LT4R1 | A | human | 352 | 6965 | 5130 | 1834 |  |
| CRHR1 | B | human | 415 | 6965 | 5114 | 1850 |  |
| GHSR | A | human | 366 | 7011 | 4932 | 2078 |  |
| GRPR | A | human | 384 | 7250 | 4619 | 2630 |  |
| GCGR | B | human | 477 | 7608 | 6183 | 1424 |  |
| AGTR1 | A | human | 359 | 7704 | 4189 | 3514 |  |
| GLP1R | B | human | 463 | 7765 | 6403 | 1361 |  |
| B1B1U5 | A | 9arac | 372 | 7810 | 5760 | 2049 |  |
| PTH1R | B | human | 593 | 7836 | 6221 | 1614 |  |
| FZD4 | F | human | 537 | 7939 | 5769 | 2169 |  |
| FZD7 | F | human | 574 | 7953 | 5637 | 2315 |  |
| CXCR4 | A | human | 352 | 8283 | 4504 | 3778 |  |
| CCR5 | A | human | 352 | 8428 | 5056 | 3371 |  |
| OPSD | A | bovin | 348 | 8701 | 6335 | 2365 |  |
| APJ | A | human | 380 | 8827 | 5205 | 3621 |  |
| CXCR2 | A | human | 360 | 9041 | 4816 | 4224 |  |
| NPY1R | A | human | 384 | 9229 | 5594 | 3634 |  |
| 5HT5A | A | human | 357 | 9255 | 5725 | 3529 |  |
| AA1R | A | human | 326 | 9506 | 6848 | 2657 |  |
| OPRD | A | human | 372 | 9983 | 5275 | 4707 |  |
| NPY2R | A | human | 381 | 10212 | 5744 | 4467 |  |
| OPRX | A | human | 370 | 10352 | 5873 | 4478 |  |
| AA2AR | A | human | 412 | 10619 | 6657 | 3961 |  |
| CCKAR | A | human | 428 | 10656 | 6246 | 4409 |  |
| 5HT2C | A | human | 458 | 10834 | 6837 | 3996 |  |
| OPRK | A | human | 380 | 11605 | 6400 | 5204 |  |
| ADRB2 | A | human | 413 | 11677 | 6769 | 4907 |  |
| OX2R | A | human | 444 | 12097 | 6840 | 5256 |  |
| 5HT1B | A | human | 390 | 12439 | 6909 | 5529 |  |
| HRH3 | A | human | 445 | 12584 | 7902 | 4681 |  |
| DRD3 | A | human | 400 | 13676 | 7479 | 6196 |  |
| ACM1 | A | human | 460 | 14104 | 8734 | 5369 |  |
| ADRB1 | A | human | 477 | 14449 | 8709 | 5739 |  |
| ACM2 | A | human | 466 | 15270 | 9716 | 5553 |  |
| HRH1 | A | human | 487 | 15350 | 9669 | 5680 |  |
| ACM4 | A | human | 479 | 16037 | 10383 | 5653 |  |
| ADA2A | A | human | 465 | 16045 | 9211 | 6833 |  |
| DRD2 | A | human | 443 | 18146 | 10030 | 8115 |  |

**No receptor in the 48-panel falls below 1000 depth, and none falls
below 100.** The shallowest is CNR2 at 1996 (well above both flag
thresholds). This is a corrective finding against the task brief's a
priori expectation:

- **B1B1U5 (arachnid, 9arac species)** sits mid-distribution at 7,810 —
  *not* an outlier. Being a non-human/non-mammalian sequence did not
  meaningfully suppress MSA retrieval.
- **OPSD (bovine)** sits at 8,701 — also *not* an outlier; bovine rhodopsin
  is extremely well-characterized in sequence databases, so this is
  unsurprising in hindsight.
- The genuinely shallow end of the distribution is dominated by Class A
  receptors with narrow/derived phylogenetic families (CNR1/CNR2
  cannabinoid, LSHR/FSHR glycoprotein-hormone receptors, EDNRA/EDNRB
  endothelin), plus three of the four Class F Frizzled/Smoothened
  entries (SMO, FZD6 lowest; FZD4/FZD7 mid-pack) — consistent with
  Frizzled/Smoothened being a smaller, more divergent receptor family
  than rhodopsin-like Class A.
- No receptor here should be treated with *depth-driven* caution by the
  stated thresholds (<1000/<100). If a stricter internal threshold is
  wanted for the Wide dispatch, CNR2/SMO/LSHR/EDNRA/CNR1/FSHR/EDNRB (the
  bottom 7, all <5000) are the candidates for a "shallower half" flag —
  see the quintile recommendation below.

## Receptor construct variants (appendix — not part of the 48-panel table)

| Receptor variant | Provenance | Species | Length | Total | UniRef90 | BFD/Uniclust | vs Class-A counterpart |
|---|---|---:|---:|---:|---:|---:|---|
| ADRB1 | G389R_polymorphism | human | 477 | 14164 | 8538 | 5625 | 14449 → 14164 (-2.0%) |
| FSHR | chai_input_2026_09_01_addendum | human | 695 | 3762 | 2648 | 1113 | 3752 → 3762 (+0.3%) |
| MCHR1 | chai_input_2026_09_01_addendum | human | 422 | 6752 | 4750 | 2001 | 6217 → 6752 (+8.6%) |

All three variants track their Class-A counterpart closely (largest shift
+8.6% for the longer MCHR1 construct, plausibly just extra flanking
residues pulling in a few more partial hits). No provenance concern.

## Cognate Gα partner depths (5 canonical)

| Class | Slug | Gene/UniProt | Length | Total | UniRef90 | BFD/Uniclust |
|---|---|---|---:|---:|---:|---:|
| Gs | alphas | GNAS/P63092 | 394 | 12080 | 7355 | 4724 |
| Gi | alphai1 | GNAI1/P63096 | 354 | 14986 | 9327 | 5658 |
| Gq | alphaq | GNAQ/P50148 | 359 | 14368 | 8842 | 5525 |
| G12 | alpha13 | GNA13/Q14344 | 377 | 11904 | 6690 | 5213 |
| Gt | alphat | GNAT1/P11488 | 350 | 14314 | 9015 | 5298 |

All five are deep (11.9k–15.0k), as expected for the near-universal Gα
family. Gs (alphas) and G12 (alpha13) are the two shallowest of the five
(~12k), still an order of magnitude above any receptor-depth concern
threshold.

## Shuffled arm — no new sequences to check

Confirmed by exact-sha256 cross-reference: all 40 `*_shuffled.fasta`
files resolve to just **3** distinct sequences — `alphas` (Gs), `alphai1`
(Gi), `alpha13` (G12) — matching the antagonist-swap distribution in
`construct_build_report.md` (Gi↔Gs is the dominant swap; Gq/Gt targets
route through Gs/G12/Gi per the fallback rule; no receptor is ever
shuffled into Gq or Gt). **The per-receptor shuffled slug is
identity/provenance metadata only — it is not a new sequence and requires
no separate MSA.** The three MSAs it needs are already covered by the
cognate-Gα table above (same sha256, same cache file). No further action
needed for the record.

## Decoy Gα depths (40) — decoy vs. cognate parent

| Receptor | Cognate class | Parent (cognate) depth | Decoy depth | Δ | Δ% | Hamming (α5-CT) |
|---|---|---:|---:|---:|---:|---:|
| 5HT1B | Gi | 14986 | 15120 | +134 | +0.89% | 10 |
| 5HT2C | Gq | 14368 | 14623 | +255 | +1.77% | 9 |
| 5HT5A | Gi | 14986 | 15101 | +115 | +0.77% | 10 |
| AA1R | Gi | 14986 | 15253 | +267 | +1.78% | 11 |
| AA2AR | Gs | 12080 | 12227 | +147 | +1.22% | 9 |
| ACM1 | Gq | 14368 | 14010 | -358 | -2.49% | 9 |
| ACM2 | Gi | 14986 | 15513 | +527 | +3.52% | 9 |
| ACM4 | Gi | 14986 | 15012 | +26 | +0.17% | 7 |
| ADA2A | Gi | 14986 | 15206 | +220 | +1.47% | 9 |
| ADRB1 | Gs | 12080 | 12102 | +22 | +0.18% | 10 |
| ADRB2 | Gs | 12080 | 11930 | -150 | -1.24% | 10 |
| AGTR1 | Gq | 14368 | 14143 | -225 | -1.57% | 10 |
| APJ | Gi | 14986 | 15411 | +425 | +2.84% | 7 |
| B1B1U5 | Gi | 14986 | 14977 | -9 | -0.06% | 10 |
| CCKAR | Gq | 14368 | 14138 | -230 | -1.60% | 8 |
| CCR5 | Gi | 14986 | 15091 | +105 | +0.70% | 10 |
| CNR1 | Gi | 14986 | 15085 | +99 | +0.66% | 8 |
| CNR2 | Gi | 14986 | 15080 | +94 | +0.63% | 9 |
| CXCR2 | Gi | 14986 | 14811 | -175 | -1.17% | 10 |
| CXCR4 | Gi | 14986 | 15066 | +80 | +0.53% | 9 |
| DRD2 | Gi | 14986 | 15538 | +552 | +3.68% | 9 |
| DRD3 | Gi | 14986 | 15288 | +302 | +2.02% | 9 |
| EDNRA | Gq | 14368 | 14383 | +15 | +0.10% | 11 |
| EDNRB | Gq | 14368 | 14169 | -199 | -1.39% | 10 |
| FSHR | Gs | 12080 | 12176 | +96 | +0.79% | 11 |
| GHSR | Gq | 14368 | 14431 | +63 | +0.44% | 8 |
| GRPR | Gq | 14368 | 14350 | -18 | -0.13% | 9 |
| HRH1 | Gq | 14368 | 13872 | -496 | -3.45% | 9 |
| HRH3 | Gi | 14986 | 14977 | -9 | -0.06% | 9 |
| LPAR1 | Gi | 14986 | 15132 | +146 | +0.97% | 10 |
| LSHR | Gs | 12080 | 12227 | +147 | +1.22% | 9 |
| LT4R1 | Gi | 14986 | 15103 | +117 | +0.78% | 11 |
| MCHR1 | Gi | 14986 | 15402 | +416 | +2.78% | 11 |
| NPY1R | Gi | 14986 | 14821 | -165 | -1.10% | 11 |
| NPY2R | Gi | 14986 | 15097 | +111 | +0.74% | 11 |
| OPRD | Gi | 14986 | 15256 | +270 | +1.80% | 9 |
| OPRK | Gi | 14986 | 15201 | +215 | +1.43% | 10 |
| OPRX | Gi | 14986 | 15068 | +82 | +0.55% | 11 |
| OPSD | Gt | 14314 | 14104 | -210 | -1.47% | 10 |
| OX2R | Gq | 14368 | 14006 | -362 | -2.52% | 9 |

**Δ% distribution across all 40**: min **-3.45%** (HRH1), max **+3.68%**
(DRD2), mean **+0.41%**, median **+0.64%**, stdev **1.60%**.
**All 40/40 decoys fall within ±5% of their cognate parent's depth; 0/40
exceed ±20%.**

## Depth vs prediction quality (analytical note)

MSA depth affects the four backbones differently by architecture:

- **AF2-lineage / MSA-transformer-style inputs (Chai, Boltz, Protenix)**
  all consume the MSA through an Evoformer-derived pairwise/row-attention
  stack. Depth below ~30-100 effective sequences (post-redundancy
  reduction) is where AlphaFold2-family accuracy degrades sharply in the
  original CASP14/AF2 ablations; above a few hundred effective sequences,
  marginal accuracy gains flatten. All 48 receptor MSAs here have raw
  depth ≥1996 (CNR2) and the cognate/decoy Gα are all >11,900 — comfortably
  past the AF2-family degradation knee even after typical clustering/
  diversity reduction, though raw row count is not the same as *effective*
  sequence count (redundant near-identical hits are down-weighted
  internally by these models; this cache format doesn't expose the
  post-clustering effective-N).
- **OF3**: per project memory
  (`of3_seed_bug_fixed_2026_09_02.md`, `refs/of3_seed_bug_mechanism.md`),
  OF3's dominant historical source of low apparent variance was the
  constant-seed bug, not MSA depth — that confound is now fixed and not
  revisited here. No paper_af3 memory file records an OF3-specific
  MSA-depth sensitivity study; this remains an open question for a
  dedicated ablation, not something this read-only pass can settle.
- **General expectation regardless of backbone**: complex-level docking
  accuracy (receptor + Gα) depends more on the *paired*-search coverage
  spanning the interface than on either chain's raw single-sequence
  depth. Since this cache's `pairing_key` field carries no information
  (see Overview), this report cannot directly assess paired-MSA depth —
  only single-chain depth by source database. This is the single biggest
  analytical gap this audit surfaces.

## Analytical implications

1. **No receptor MSA is shallow enough (<1000) to warrant depth-driven
   caution.** The a priori concern flagged for B1B1U5 (arachnid) and
   OPSD (bovine) does not materialize — both are mid-distribution
   (7,810 and 8,701 respectively). If a caution flag is still wanted for
   the Wide analysis, it should target the *bottom of the observed
   distribution* (CNR2, SMO, LSHR, EDNRA, CNR1, FSHR, EDNRB — all
   <5000, i.e. the bottom 7/48), not a fixed absolute threshold that
   nothing crosses.

2. **Decoy depth is NOT systematically lower than cognate depth.** All
   40 decoy/cognate pairs land within ±3.45% to +3.68% of parent depth
   (mean +0.41%, i.e. slightly positive on average, essentially
   symmetric noise around zero). This directly answers the coordinator's
   question: **ColabFold does not reject the scrambled α5-CT.** The
   pattern is consistent with the first hypothesis floated — the search
   is effectively retrieving the same homolog set as the intact parent,
   because 340+/354 (or equivalent) identical residues dominate the
   sequence-similarity signal used for database retrieval, and an
   11-residue scramble at the C-terminus (hamming 7-11 out of 11) is far
   too small a perturbation to shift which homologs get returned. There
   is no visible classification-boundary effect (no decoy is
   "dramatically shallower" — max deviation is under 4%), and no
   correlation is evident between hamming distance (7-11) and Δ% (e.g.
   ACM4 has the lowest hamming=7 with a negligible +0.17%, while APJ also
   has hamming=7 but +2.84%; MCHR1/NPY1R/NPY2R/OPRX at hamming=11 span
   -1.10% to +2.78%) — the small residual scatter looks like ordinary
   run-to-run ColabFold search noise, not a systematic scramble effect.
   **This is a preliminary read on n=40 single-chain, non-paired depth;
   it says nothing about whether the paired/interface-relevant subset of
   hits differs**, which this cache format cannot answer (see Overview).

3. **Recommendation for post-Wide analysis**: Given finding #1 (no
   receptor crosses the stated absolute thresholds) and finding #2 (decoy
   depth is not confounded with cognate depth), MSA-depth quintile
   stratification is **low-priority as a confound-control measure for
   the decoy-vs-cognate comparison** — depth is not a plausible mediator
   there. It remains **worth doing for the receptor axis alone**, since
   receptor depth spans a real ~9x range (1996-18146) driven by
   phylogenetic family (cannabinoid/endothelin/glycoprotein-hormone
   receptors and 3 of 4 Frizzled/Smoothened entries cluster shallow;
   aminergic/muscarinic/dopamine receptors cluster deep) — if any Wide
   metric shows a receptor-family-correlated effect, MSA depth is a
   candidate mediator to control for via quintile bucketing on the
   48-receptor table above.

## Provenance

- **HPC cache directory**: `/hpc/scratch/sengaad1/paper_af3/msa_cache/chai/`
  (basel-hpc, `ssh basel-hpc`, read-only access — no writes, no qsub, no
  interference with the running Block B dispatch pool).
- **File count at time of read**: 120 `.aligned.pqt` files.
- **Read timestamp**: 2026-09-03T06:48:39Z (UTC).
- **Manifest sha256** (of `ls <cache_dir>/*.aligned.pqt | xargs -n1 basename | sort | sha256sum`,
  i.e. a checksum over the sorted filename listing — confirms exactly
  which 120 filenames were read, independent of file contents):
  `b9d2a98fab2e44cd83afe03b507e0fe2244ba44df2fd47c65e00b310c575507f`
- **Depth-extraction method**: single `ssh basel-hpc` session, one Python
  process (Chai venv, `pandas`/`pyarrow`), looping all 120 files once and
  emitting one CSV row per file (`sha256, total_rows, uniref90,
  bfd_uniclust, query, other_db_names, pairing_key_nonempty,
  comment_nonempty, pairing_key_unique_n, comment_unique_n`) — not 120
  separate round-trips. Local join against sha256(seq.upper()) computed
  from `refs/panel_receptor_sequences.fasta`,
  `docs/EXPERIMENT_CATALOG/sequences/partners.fasta`, and
  `refs/constructs_block_b/*.fasta`.
- **Every local sequence resolved to exactly one cache file and vice
  versa** (120=120, zero orphans) — no ambiguity in the shuffled arm
  (reuses cognate sha) or in decoy/cognate/receptor overlap (all three
  categories are pairwise disjoint by sha256, confirmed directly, not
  assumed).

## Appendix — non-Block-B partner MSAs (cache existence only)

The remaining 24 `partners.fasta` entries beyond the 5 canonical cognate
Gα were pre-warmed for exploratory Block A partner-diversity work (Gα
paralogs, dominant-negative mutants, misc GPCR/partner proteins,
nanobody, arrestin fragments, short peptide ligands, ubiquitin control).
Not part of the Block A/B receptor-Gα narrative — listed here only to
confirm the cache is complete and to record what's available for future
analyses without re-warming:

| Name | Length | partners.fasta category | Total | UniRef90 | BFD/Uniclust |
|---|---:|---|---:|---:|---:|
| random_helix_40mer | 40 | decoy | 1 | 0 | 0 |
| arrestin_Ctail | 41 | arrestin | 1 | 0 | 0 |
| substanceP | 11 | partner_misc | 1 | 0 | 0 |
| DAMGO | 5 | partner_misc | 1 | 0 | 0 |
| arrestin_FL | 15 | arrestin | 84 | 79 | 4 |
| gcn4_leucine_zipper_33 | 33 | decoy | 224 | 153 | 70 |
| endothelin1 | 21 | partner_misc | 732 | 565 | 166 |
| Gg2 | 71 | partner_misc | 3191 | 2335 | 855 |
| HCAR2 | 363 | partner_misc | 5711 | 4872 | 838 |
| GP161 | 511 | partner_misc | 5822 | 3961 | 1860 |
| GIPR | 528 | partner_misc | 6292 | 5289 | 1002 |
| KaiB_2QKEE | 91 | partner_misc | 7894 | 2309 | 5584 |
| GASR | 396 | Gα | 9934 | 6151 | 3782 |
| TAAR1 | 339 | partner_misc | 10068 | 6322 | 3745 |
| ACM3 | 568 | partner_misc | 11425 | 6434 | 4990 |
| Nb60 | 126 | nanobody | 11934 | 10500 | 1433 |
| alphas_F376A_L388A_mutant | 394 | Gα | 11996 | 7405 | 4590 |
| alphas_F376A_L388A_R380A_triple_null | 394 | Gα | 12080 | 7423 | 4656 |
| alphaz | 355 | Gα | 13149 | 8047 | 5101 |
| alphagust | 354 | Gα | 14294 | 9040 | 5253 |
| alphai2 | 355 | Gα | 14500 | 8996 | 5503 |
| alpha11 | 359 | Gα | 14509 | 8941 | 5567 |
| alphao | 354 | Gα | 15016 | 9277 | 5738 |
| ubiquitin | 76 | ubiquitin_control | 21576 | 9855 | 11720 |

Note: the four entries with total depth = 1 (`random_helix_40mer`,
`arrestin_Ctail`, `substanceP`, `DAMGO`) are short synthetic/peptide
sequences (5-41 residues) with no homology-search hits beyond the query
itself — expected for non-natural or very short sequences, not a cache
or pipeline defect. None of these four are receptors or canonical Gα, so
this does not affect the Block A/B primary tables above.
