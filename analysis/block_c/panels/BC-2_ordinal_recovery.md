# BC-2 — the pre-registered ordinal test recovers the same ordering

**Claim**: SC-C-2. **Not buildable from this bundle** — needs
`rows.tier3.v2.csv`. `07_ordinal_recovery/s5_p4_ordinal.json` ships the
summary only.

## Encoding

Kendall's tau, ligand-role rank against the continuous axis, per backbone and per
panel definition.

| panel | Boltz-2 | Chai-1 | OpenFold3 | Protenix2 |
|---|---:|---:|---:|---:|
| Tier 3 apo x 23 | 74% | 65% | 74% | 87% |
| Tier 3 apo x 15, self-ref excluded | 67% | 67% | 67% | 87% |
| Tier 1 apo, 5-class | 75% | 75% | 75% | 75% |

## Required on the panel

- **The threshold was locked before the campaign ran.** That is why this test
  carries weight the 2x2 does not, and the panel should say so rather than
  presenting it as a second confirmatory statistic.
- Show all three panel definitions. Showing only the most favourable row would
  be the same error the pose result already made and corrected.
- 6 of 8 backbone x panel cells reach the pre-registered threshold; say which
  two do not.
