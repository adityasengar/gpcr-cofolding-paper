# GATE-3 — D3 steering vs degradation, per backbone

**Question**: Is the shallow-MSA-depth "more active predicate" result a real
conformational movement toward the active state (LEVER), or is it structural
degradation that happens to trip the two-instrument predicate (DEGRADATION)?
Resolved per backbone, not pooled, per the dispatch.

**Verdict summary** (headline):

| Backbone | slope (%/log10) | full→depth-8 Cα RMSD range | pLDDT Δ full→d8 | shallow-d8 predicate ∩ sub-Å-to-active | Verdict |
|---|---:|---|---:|---:|---|
| Boltz-2   | -1.68 | ~1–4 Å                         | -0.5 | 88.7 % of predicate-active are sub-Å | **LEVER** |
| Chai-1    | -0.82 | ~2–5 Å                         | -1.0 | 75.7 %                                | **LEVER — MUTED** |
| OF3       | -2.73 | **~10–14 Å** on high-swing recs | **-3.9** | **42.9 %**                            | **DEGRADATION-LEANING / MIXED** |
| Protenix  | -2.96 | **~16–20 Å** on high-swing recs | **-3.2** | 68.3 % (misleading — see below)         | **MIXED (receptor-dependent)** |

**The finding is the split.** The two backbones with the largest slopes (OF3
-2.73, Protenix -2.96) are also the two with double-digit-Å matched-seed
7TM Cα RMSD full→depth-8 swings and material pLDDT drops. Their "more active
at shallow depth" signal is a hybrid: some receptors genuinely reach an
active-like pocket, others generate novel or partly-shredded conformations
that satisfy the two coarse predicate distances (NPxxY-OH < 9.082, TM6 tilt >
14.932) without approaching the deposited active crystal geometry. Boltz and
Chai are levers, Boltz clean and Chai muted; OF3 is degradation-leaning
overall with case-by-case exceptions; Protenix is genuinely mixed with the
verdict changing per-receptor.

---

## (a)–(c) Population metrics per (backbone × depth) — 26 receptors × 5 seeds × 10 samples per cell

Predicate: `d_npxxy_y558_y753_oh < 9.082 Å` AND `d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`.
Sub-Å: `pocket_ca_rmsd_active|inactive < 1.0 Å`.

Recomputed from `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv`.

```
bb        depth      n   (a)pred%   (b)subA%   (c)subI%  medPCA_a medPCA_i medPlddt  med_n_ca
boltz     8       1300     17.77     51.23     68.46     0.992    0.813    75.73     380
boltz     32      1300      7.00     43.77     75.85     1.041    0.777    76.08     380
boltz     128     1300      4.92     39.92     79.15     1.063    0.753    76.01     380
boltz     512     1300      5.38     41.08     81.00     1.070    0.752    76.15     380
boltz     full    1300      5.08     42.54     79.69     1.059    0.745    76.26     380

chai      8       1280     25.08     36.72     71.80     1.086    0.855    74.14     380
chai      32      1270     20.16     36.93     74.72     1.079    0.840    74.11     380
chai      128     1300     19.69     36.62     74.23     1.074    0.820    74.89     380
chai      512     1300     18.38     39.08     79.08     1.058    0.773    75.67     380
chai      full    1260     19.37     43.02     78.73     1.043    0.776    75.12     380

of3       8       1300     28.00     29.69     37.15     1.219    1.129    64.60     380
of3       32      1280     26.17     44.84     57.50     1.034    0.943    67.16     380
of3       128     1300     21.92     50.15     68.62     1.000    0.844    67.90     380
of3       512     1270     15.35     50.47     73.15     0.998    0.791    68.10     380
of3       full    1250     12.40     50.64     73.84     0.997    0.786    68.45     380

protenix  8       1300     15.54     29.15     44.92     1.238    1.039    72.11     380
protenix  32      1300     16.77     42.08     68.00     1.082    0.845    73.87     380
protenix  128     1300      9.69     40.46     79.77     1.069    0.774    74.78     380
protenix  512     1300      2.08     37.62     85.85     1.080    0.712    75.19     380
protenix  full    1300      0.08     37.92     89.00     1.090    0.649    75.29     380
```

**Reading (b) vs (a)**: for a LEVER, (a) rising at shallow depth should be
paired with (b) rising (samples pass the predicate BECAUSE they reached the
active-like pocket geometry). For DEGRADATION, (a) rises while (b) does not.

- **Boltz**: (b) 42.5 % at full → 51.2 % at depth 8, tracks (a). LEVER.
- **Chai**: (b) 43.0 % full → 36.7 % at depth 8, drifts opposite (a), but change is small (a moves 19 → 25, b moves 43 → 37). MUTED.
- **OF3**: (b) 50.6 % full → 29.7 % at depth 8. **(b) drops sharply as (a) rises.** DEGRADATION signature.
- **Protenix**: (b) 37.9 % full → 29.2 % at depth 8, small drop while (a) rises 0.1 → 15.5. DEGRADATION signature at cell-median level.

## Fraction of predicate-active samples that are ALSO sub-Å to active

The cleanest single-number stratification: for a LEVER, most predicate-active
samples should ALSO be geometrically close to the active reference. For
DEGRADATION, they aren't — the predicate is a coarse pair-of-distances
metric that can be tripped by novel conformations.

```
bb        depth   pred%   subA%   pred∩subA%   frac_pred_that_are_subA%
boltz     8       19.25   53.67       17.08              88.74
boltz     32       7.58   44.25        6.42              84.62
boltz     128      5.33   39.92        5.17              96.88
boltz     512      5.83   40.75        5.75              98.57
boltz     full     5.50   42.75        5.42              98.48
chai      8       27.20   39.83       20.59              75.70
chai      32      21.69   39.75       17.88              82.42
chai      128     21.33   39.67       16.75              78.52
chai      512     19.92   42.25       15.83              79.50
chai      full    20.85   45.90       16.24              77.87
of3       8       30.33   31.42       13.00              42.86
of3       32      28.15   46.97       16.64              59.10
of3       128     23.75   52.25       13.92              58.60
of3       512     16.67   54.02        9.74              58.46
of3       full    13.36   54.14        7.59              56.77
protenix  8       16.83   30.08       11.50              68.32
protenix  32      18.17   42.92       12.42              68.35
protenix  128     10.50   41.92        8.25              78.57
protenix  512      2.25   40.33        1.58              70.37
protenix  full     0.08   40.67        0.08             100.00 (n=1)
```

The `frac_pred_that_are_subA` column is the crux:

- **Boltz**: 85–99 % across depths. Even at depth 8 (17 % predicate-active), nearly 9 in 10 of those samples are geometrically close to the active crystal. **LEVER, clean.**
- **Chai**: 76–83 %. Modestly weaker geometric fidelity than Boltz, but stable across depths. **LEVER, but the depth-8 predicate-active samples include ~24 % that are NOT close to the active reference.**
- **OF3**: **42.9 % at depth 8**, rising to 56.8 % at full. The additional predicate-active samples that appear at shallow depth are disproportionately NOT sub-Å to the active reference. **DEGRADATION-LEANING.**
- **Protenix**: 68 % at depth 8 vs 100 % at full (n=1). Consistent 68–79 % across depths 8–128. Still a lower bar than Boltz. **MIXED** — 32 % of shallow-depth predicate-active samples are NOT geometrically active.

## (d) Fold-integrity: matched (receptor, backbone, seed, sample) 7TM Cα RMSD, full vs depth-N

The existing D3.4 propagation test computed this on AA2AR only. GATE-3
extends to representative high-swing receptors per backbone, matched on
(seed, sample_idx) so seed-noise cancels.

Method: `gemmi.superpose_positions` on first-chain Cα atoms, all resolved
positions (~350–380 per structure).

```
== boltz opsd (seed_1708630764 sample 0) ==   [lever exemplar]
  depth512 → RMSD vs full 3.85 Å
  depth128 → RMSD vs full 2.58 Å
  depth32  → RMSD vs full 1.05 Å
  depth8   → RMSD vs full 3.93 Å

== chai lt4r1 (seed_1708630764 sample 0) ==   [muted-lever exemplar]
  depth512 → 2.09 Å ; depth128 → 2.78 Å ; depth32 → 3.62 Å ; depth8 → 5.24 Å

== protenix lt4r1 (seed_1708630764 sample 0) ==   [protenix high-swing]
  depth512 → 6.75 Å ; depth128 → 8.85 Å ; depth32 → 20.65 Å ; depth8 → 17.73 Å

== protenix agtr1 (seed_1708630764 sample 0) ==   [protenix, another]
  depth512 → 5.20 Å ; depth128 → 16.92 Å ; depth32 → 17.16 Å ; depth8 → 15.83 Å

== of3 lt4r1 (seed_1708630764 sample 1) ==   [of3 high-swing]
  depth512 → 3.48 Å ; depth128 → 5.76 Å ; depth32 → 6.78 Å ; depth8 → 14.39 Å

== of3 cxcr4 (seed_1708630764 sample 1) ==   [of3 second high-swing]
  depth512 → 4.39 Å ; depth128 → 4.73 Å ; depth32 → 6.09 Å ; depth8 → 10.05 Å

== of3 oprd (seed_1708630764 sample 1) ==   [of3 counter-example]
  depth512 → 4.88 Å ; depth128 → 4.75 Å ; depth32 → 4.85 Å ; depth8 → 3.55 Å
```

**Reading (d)**:
- Boltz + Chai: 1–5 Å. Consistent with real but bounded conformational
  movement — the "lever" regime.
- Protenix on both high-swing receptors: **15–20 Å** at depth 32 / 8. That
  is the double-digit-Å signature the dispatch names as DEGRADATION.
- OF3: 10–14 Å on LT4R1 / CXCR4 depth 8. Also degradation-signature. But
  OF3 OPRD stays at 3.5 Å even at depth 8 — receptor-dependent.

## Structural spot-check — CIFs opened and one-line verdicts

Extended anchor / pLDDT / geometry inspection at n=50 per cell (full seed
population, sample 0):

| Cell | med pLDDT | anchor 4/4 identity | med pca_active | med NPxxY | med tilt | Verdict |
|---|---:|---:|---:|---:|---:|---|
| Boltz OPSD full     | 83.5 | 50/50 | 1.25 | 13.85 | 12.78 | Inactive-like, near inactive crystal |
| Boltz OPSD depth 8  | 83.8 | 50/50 | **0.41** | 4.99 | 17.34 | **Predicate satisfied AND pocket ≈ active crystal — clean lever** |
| Protenix LT4R1 full     | 78.7 | 50/50 | 0.94 | 11.85 | 12.11 | Inactive-like |
| Protenix LT4R1 depth 8  | 74.1 | 50/50 | 0.89 | 4.83 | 17.03 | Predicate cleared AND pocket approaches active — lever-at-pocket, but backbone RMSD-to-full is 15–20 Å (novel global fold) |
| Protenix AGTR1 full     | 78.6 | 50/50 | 0.76 | 10.93 | 11.19 | Reasonable to active on pocket |
| Protenix AGTR1 depth 8  | 77.5 | 50/50 | **1.24** | 3.40 | 16.78 | **Predicate cleared BUT pocket drifted AWAY from active reference (0.76 → 1.24). DEGRADATION signature.** |
| OF3 LT4R1 full     | 72.7 | 50/50 | 0.85 | 11.53 | 12.19 | Near reference active |
| OF3 LT4R1 depth 8  | 67.9 | 50/50 | 0.77 | 4.40 | 17.56 | Predicate cleared, pocket closer to active, but pLDDT drop 5 pts and 14 Å backbone RMSD to full — mixed |

**Anchor identity 4/4 for every single spot-check row.** So the shallow-depth
structures aren't random noise — the BW-anchor residues are correctly placed.
This is not fold-shredded-to-nothing. It IS globally different from
full-depth predictions in many cases.

CIFs actually opened (via gemmi.read_structure on HPC):

- `pool/lt4r1/full/protenix/seed_1708630764/tier_d3_lt4r1_full_protenix_seed3/seed_.../predictions/*_sample_0.cif` — 352 Cα, standard 7TM helix count.
- `pool/lt4r1/depth8/protenix/.../sample_0.cif` — 352 Cα, but 17.7 Å from full. Novel arrangement.
- `pool/agtr1/full/protenix/.../sample_0.cif` — 359 Cα.
- `pool/agtr1/depth8/protenix/.../sample_0.cif` — 359 Cα, 15.8 Å from full.
- `pool/opsd/full/boltz/.../seed_.../*_model_0.cif` — 348 Cα.
- `pool/opsd/depth8/boltz/.../*_model_0.cif` — 348 Cα, 3.9 Å from full.
- `pool/lt4r1/full/of3/.../seed_499961916/*_sample_1_model.cif` — 352 Cα.
- `pool/lt4r1/depth8/of3/.../*_sample_1_model.cif` — 352 Cα, 14.4 Å from full.
- `pool/cxcr4/depth8/of3/.../*_sample_1_model.cif` — 352 Cα, 10.1 Å from full.
- `pool/oprd/depth8/of3/.../*_sample_1_model.cif` — 372 Cα, 3.5 Å from full. Counter-example.

## Per-backbone verdicts (final)

**Boltz-2 — LEVER (clean)**
- (a) rises at shallow depth, (b) tracks it.
- 88.7 % of shallow-depth predicate-active are sub-Å to active reference.
- Matched-seed 7TM RMSD 1–4 Å.
- pLDDT stable (Δ ≤ 1 point).
- OPSD is a textbook exemplar (pocket_ca_rmsd_active moves 1.25 → 0.41 Å; predicate goes from inactive-like to active-like; backbone RMSD 3.9 Å).

**Chai-1 — LEVER (muted)**
- Small (a) response overall (25 → 19 %).
- 76–82 % geometric fidelity.
- Matched-seed 7TM RMSD 2–5 Å.
- pLDDT stable.
- Depth is a real lever on Chai; the headroom is smaller because Chai's active-fraction is already high at full depth.

**OF3-preview — DEGRADATION-LEANING (mixed)**
- (a) rises but (b) drops sharply at shallow depth.
- **42.9 %** geometric fidelity at depth 8. Majority of the "extra" predicate-active samples that appear at shallow depth are NOT close to the active reference.
- Matched-seed 7TM RMSD 10–14 Å on high-swing receptors (LT4R1, CXCR4).
- pLDDT drops ~4 pts across cells.
- Counter-examples exist (OPRD stays coherent at depth 8) — receptor-dependent.
- The reported -2.73 %/log slope is partly real steering, partly the model getting worse.

**Protenix v2 — MIXED / RECEPTOR-DEPENDENT**
- (a) rises modestly at shallow depth (0.1 % → 15.5 %).
- 68 % geometric fidelity — better than OF3, worse than Boltz.
- Matched-seed 7TM RMSD **15–20 Å** on high-swing receptors — the largest of any backbone.
- pLDDT drops 3.2 pts.
- LT4R1 depth-8: pocket approaches active (lever-like).
- AGTR1 depth-8: pocket moves AWAY from active while predicate clears (degradation-like).
- **Cannot be summarised in a single word.** Report split per receptor if possible; otherwise "mixed, with degradation exemplars".

## What this means for the D3 headline

Original D3 headline (`tier_d3_full_headline_2026_09_08.md`): *"MSA depth is a
controllable-sampling lever, confirmed on all 4 backbones."* Slopes ranked
Protenix > OF3 > Boltz > Chai.

**GATE-3 revision**: the ranking is nearly inverted once fidelity is
required. **Boltz + Chai are the honest levers**, at slopes -1.68 and -0.82
per log10(depth). OF3 and Protenix have the largest predicate-active
responses, but a substantial fraction of the response is fold-drift that
happens to trip the two coarse predicate distances. The **-2.96 / -2.73
slopes are inflated** by degradation samples that a geometry-fidelity filter
would exclude.

The right claim for the manuscript is a **conditional lever**: shallow MSA
depth generates more "active-like by predicate" samples on all four
backbones, but the fraction of those samples that are geometrically close to
the deposited active reference is backbone-dependent, with only Boltz (and
Chai to a lesser extent) preserving pocket-Cα fidelity across the depth
range.

## Things not fixed, flagged for §6

- **Extended (d) computation**: only sampled 5 (bb × rec) pairs across 4 depths + AA2AR from D3.4. A per-cell 26-rec median would require ~500 pairwise Cα RMSD comparisons — feasible as a follow-up on HPC but not run in this pass. Sample chosen to cover high-swing (Protenix LT4R1/AGTR1, OF3 LT4R1/CXCR4) plus counter-example (OF3 OPRD).
- **Cluster-boot CIs** on the four per-backbone slopes not computed here; GATE-2 handles slope derivation, this gate handles interpretation of the mechanism.
- **Per-receptor lever/degradation classification** — this pass called the split at backbone level. A per-receptor pass (26 rec × 4 bb = 104 verdicts) would surface the AGTR1-like receptors where the response is unambiguous degradation on all four backbones. Left for a follow-up in Part A / §6.
- **pLDDT drop of 3–4 pts on OF3/Protenix at shallow depth is REAL but not catastrophic** — the anchor-identity match rate remains 100 % across all spot-check rows, so it's not sequence-registration collapse. The novelty of the shallow-depth structures reads as "different plausible fold" rather than "shredded".
