# W-D-5 — "MSA depth is a controllable lever on all 4 backbones" (D3 headline F1)

## Claim as previously stated

D3 headline F1 (per `experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md`):
"Depth is a controllable lever on 3 of 4 backbones (Boltz, OF3,
Protenix). Slopes −1.7 to −3.0 %/log(depth) across the 26-receptor
panel. Protenix has the strongest monotonic response: from 15.5 %
active at depth 8 down to 0.1 % at full — depth is nearly the sole
driver of Protenix's apo two-instrument fraction."

## Retraction

**Withdrawn as-drafted.** GATE-3 (four converging lines of evidence)
shows the depth response is a per-backbone **mechanism split**, not a
universal-lever finding:

- **Boltz** — clean lever. Predicate rises, sub-Å-to-active rises,
  matched-seed Cα 1–4 Å, pLDDT stable. Slope signed under cluster-boot.
- **Chai** — muted lever. Slope point-negative but **unsigned under
  cluster-boot** (crosses zero). Fold-quality preserved.
- **OF3** — degradation-leaning. Predicate rises but sub-Å-to-active
  DROPS 20.9 points; matched-seed Cα 10–14 Å; pLDDT drops 3.9.
- **Protenix** — mixed / receptor-dependent. Largest apparent slope
  but 15–20 Å Cα deviation on high-swing receptors; pLDDT drops 3.2.

**The largest slopes (Protenix −2.96, OF3 −2.73) are inflated by
fold-degradation at shallow depth**, not by conformational steering.
Do NOT describe OF3 or Protenix as controllable levers on the depth
axis.

## Basis

- `dossiers/BLOCK_D/gates/GATE_3_STEERING_VS_DEGRADATION.md` — full per-backbone verdict + structural spot-check.
- `dossiers/BLOCK_D/partA/PARTA_D3.md` §1 (reframed F1).
- `dossiers/BLOCK_D/EXPERIMENT_DOSSIER_BLOCK_D.md` §SC-D-8.

## What the manuscript should say instead

> MSA depth modulates predicate-active sampling on all four backbones,
> but the mechanism differs. Boltz is a clean conformational lever;
> Chai's slope is not distinguishable from zero under cluster-boot
> convention; OF3 and Protenix show the largest apparent slopes but
> shallow depth degrades their fold — pocket-Cα moves AWAY from active
> while pLDDT drops 3–4 pts. Only Boltz (and Chai, muted) preserve
> pocket-Cα fidelity across the depth range.
