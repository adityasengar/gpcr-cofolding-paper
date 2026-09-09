# C-4 — Chai is systematically softer than the other three backbones

## Caveat

Chai produces predictions that lean toward smaller structural changes
between apo and cognate arms — a systematic softness relative to Boltz,
OF3, and Protenix.

**Evidence at Block A row grain**:

| Metric | Chai value | Others (median across 3) |
|---|---:|---:|
| Median tilt shift cognate−apo (Å) | 1.05 | 5.04 |
| Median delta_to_active shift cognate−apo (Å) | 2.77 | 5.27 |
| Fraction-of-way-to-active | 0.888 | 0.913 |
| Cognate TM6 tilt % active | 81.8% | 97.4% |
| Not-engaged cognate rows partner-pLDDT median | **88.2** | 80.3 |
| Two-instrument κ (Class A) | 0.865 | 0.83 (avg boltz+protenix) |
| Panel-mean apo-active rate | 32.67% | 18.20% (median of 3) |

**Chai's not-engaged cognate rows carry HIGHER partner-pLDDT than
engaged rows** (88.2 vs 83.5) — Chai is confident about partner position
when it is wrong.

## Affects

- Any pooled-across-backbones median. Chai attenuates every effect it is
  averaged into.
- Chai CNR2 apo bias (100% active vs 0–4% others; see W-1 and D1
  auto-memory).
- Cross-backbone MSA-depth comparability — MSA is per-receptor on Chai
  (via `.aligned.pqt` cache); the other three use live ColabFold.

## Evidence

- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md` §Phase 3c, §Phase 4a, §Phase 5d
- Auto-memory `chai_cnr2_apo_model_bias_2026_09_06.md`

## Manuscript sentence

> Chai is a systematically softer predictor: its cognate-apo shifts on
> TM6 tilt (1.05 Å) and on delta_to_active (2.77 Å) are approximately
> one-fifth the magnitude of the other three backbones. Cross-backbone
> pooling that includes Chai therefore attenuates every effect; the
> per-backbone table is the primary reporting unit.
