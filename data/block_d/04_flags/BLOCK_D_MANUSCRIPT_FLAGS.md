# BLOCK D — MANUSCRIPT FLAGS

Flags that the figure agent, prose agent, or a reviewer will need to
respect. These are NOT withdrawals or caveats — they are load-bearing
scope decisions and framing conventions that persist across figures.

## Flag D-1 — Cluster-boot authoritative EXCEPT at n < 10 clusters

Every CI in `LEDGER.csv` for D-tier claims uses cluster-boot over
paralog clusters (Block A C-8 convention). D3 (26 receptors, 22
clusters) has valid cluster-boot. **D1 (7 receptors, 7 clusters) and D2
(4 receptors, 4 clusters) are cluster-boot-degenerate** — cluster-boot
equals receptor-boot at 1 rec/cluster. D1/D2 use receptor-boot with
the limitation explicitly stated.

Any panel/figure quoting a CI for D1 or D2 must name **receptor-boot**
in the caption, along with the n-limitation.

## Flag D-2 — D3 slope unit is `%/ln(depth)`, not `%/log(depth)`

The four D3 headline slopes reproduce **only under natural log**, not
common log. Any manuscript figure or table quoting them must use the
correct unit label. Off by factor ~2.303 otherwise.

**Two-line prose template**: *"MSA depth modulates the two-instrument
active fraction with per-backbone slopes (%/ln(depth)) of −1.68 (Boltz)
… . The magnitude is per e-fold change in MSA depth."*

## Flag D-3 — D3 backbone-specific mechanism (do NOT describe OF3 or Protenix as levers)

The reframed D3 story (SC-D-8) has **four converging lines of evidence**
for a per-backbone split:

- **Boltz** — LEVER (clean). Signed slope, sub-Å-to-active tracks
  predicate-active, matched-seed 7TM Cα stays 1–4 Å.
- **Chai** — LEVER (muted). Slope negative in point but **unsigned under
  cluster-boot** (crosses zero). Fold-quality preserved.
- **OF3** — DEGRADATION-LEANING. Predicate clears while sub-Å-to-active
  DROPS 20.9 pts; matched-seed Cα 10–14 Å; pLDDT drops 3.9.
- **Protenix** — MIXED / RECEPTOR-DEPENDENT. Largest apparent slope but
  worst fold fidelity (15–20 Å Cα deviation on high-swing receptors).

**Do not describe OF3 or Protenix as controllable levers on the depth
axis.** Any figure showing all four slopes must annotate per-backbone
mechanism.

## Flag D-4 — D1 two-continuous-basins claim was pre-registered secondary and dropped

The dip-test outcome (2/112 cells signed; both OPSD × OF3) fires
PREREG §D-1.7's kill on the two-continuous-basins claim. **Main text
must not carry the "two continuous basins" reading.** OPSD × OF3 lives
in a Discussion appendix as a single-cell signal, not as a
panel-scale finding.

D1 still ships value via §D-1.7's contingency clause — CI-hardened
per-cell distributions on the two-instrument axis and sub-Å-to-active
axis are the surviving primary output.

## Flag D-5 — F1 (backbone active-outlier receptor-specificity) reproduces cross-tier on Block A

D1's F1 finding is not a D1-panel artefact. All 4 outliers (Chai on
CNR2 +96.0, OPSD +52.0, ADRB2 +96.0 pts; OF3 on LPAR1 +88.0 pts vs
max-of-others) reproduce at ≥+50-pt delta on Block A independent data
at n=25/cell. Robust cross-tier — warrants main-text space alongside
the D1 CI-hardened distributions.

## Flag D-6 — OF3 + Protenix have a "coherent-non-reference-active-fold" behavioural mode

The predicate + pocket-Cα-RMSD DISAGREEMENT signature is a cross-tier
finding, not D3-shallow-MSA-only. Two receptor-scale instances:

- **LPAR1 / OF3 at full-depth D1** (predicate-active 91.8 %,
  sub-Å-to-active 0.4 %). Helix 60.9 %, Rg 27.9 Å, no chain breaks —
  novel coherent active-like fold that trips the coarse predicate.
- **Protenix AGTR1 at depth-8 D3** (predicate clears, pocket-Cα
  moves AWAY from active; matched-seed Cα 15.8 Å; 4/4 BW anchors correct).

Manuscript sentence: "the two-instrument predicate + pocket-Cα-RMSD
disagreement is a per-backbone behavioural signature of OF3 and
Protenix, not a scoring artefact." Cite both cells.

## Flag D-7 — All three D-tier corpora share scorer `d9c646af`

Cross-tier comparability is **trivially safe** — D1, D2, D3 all ran
on `d9c646af5f89861c16062bf256de96a8389d9915`; also matches Block C's
`rescore_t7c_full` pose corpus.

**Correction required at authoring**: phantom SHA `891041e858f3747b`
appears in `experiments/023_tier_d2_directed_inactive/analysis/tier_d2_full_headline_2026_09_07.md`
line 6, `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md`
line 6, and auto-memory `d3_full_confirmed_2026_09_08.md`. The SHA
does not exist in git. Row-level `d9c646af` is authoritative.

## Flag D-8 — F3 "no backbone reliably steers inactive" is provisional pending §2.4 post-cutoff test

Panel-scale F3 (SC-D-6) is a negative finding subject to a
**training-data-availability confound** (C-D-12: all 4 D2 Nb-anchor
PDBs deposited 2013–2020, predate every backbone's training cutoff).

**Main-text framing is LOCKED per dossier §6.5** (2026-09-10). The
post-cutoff-inactive-Nb search closed as attempted-and-documented, not
resolved — full record + reusable filter rule at
`dossiers/BLOCK_D/BLOCK_D_POST_CUTOFF_SEARCH_NOTE.md`. Locked
Discussion text reports the active/inactive asymmetry as demonstrated
only in the active direction; whether directed inactive generation is
achievable remains open. Writing agent uses §6.5's exact wording;
this is no longer a provisional paragraph.

## Flag D-9 — D2 Gα positive control is 14/16 cells ≥ 96 %, not 15/16

Any prior manuscript sentence quoting "15/16" as the Gα positive-control
cell count needs correction to **14/16**. Both misses are OF3 (ACM2
58 %, OPRK 36 %). Boltz + Chai + Protenix hit 100 % on all 4 cognate_gα
cells. One-word fix.

## Flag D-10 — D2 F3 OPRK unanimous_up direction; respect the flagship-cell CI

On OPRK × inactive_nb, all 4 backbones shift UP toward active (Boltz
+44, Chai +8, OF3 +10, Protenix +6). **Systematic Nb-B-as-active
bias, not random noise.** Manuscript sentence must convey the
directional pattern.

**The flagship OPRK × Boltz cell (4 % → 48 %) has 95 % binomial CI
[33.7, 62.6] at n=50** — "approaches half" is supported; "majority
invert" is not. Writing agent to respect the CI in all sentences
citing this cell.

## Flag D-11 — D2 F1 mistake propagation (14 vs 15)

Companion to Flag D-9. Any prior sentence quoting "15/16" as the
Gα positive-control cell count needs the same correction. Applies
to headline docs, memory files, prior HANDOFF notes, and any figure
captions.

## Flag D-12 — D2 reference-predicate calibration verified on NPxxY-OH; TM6-tilt calibration deferred

Part A/D2 §3 confirms the two-instrument predicate is sound on all 4
D2 receptors: NPxxY-OH calibration on Nb-anchor PDBs verified
(ACM2/4MQS active PASS 4.21 Å; ADRB2/5JQH inactive FAIL 11.16 Å;
OPRK/6VI4 inactive FAIL 12.88 Å). TM6-tilt calibration on Nb-anchor
PDBs deferred as ANV (needs GPCRdb 2×46/6×37 mapping; ~30 min compute).

**F3's negative finding is NOT attributable to a broken instrument.**
The training-data-availability confound (C-D-12) is a separate
concern from the instrument's soundness.
