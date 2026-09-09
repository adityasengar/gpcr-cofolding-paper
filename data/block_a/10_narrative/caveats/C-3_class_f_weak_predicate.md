# C-3 — Class F tilt-only predicate is weak

## Caveat

The Class F two-instrument predicate reduces to TM6 tilt alone (Class F
receptors lack the Class A NPxxY tyrosine and lack the Class B kink
motif). On Block A, the Class F cognate−apo median tilt shift is 0.27 Å,
smaller than the IQR width in either arm (apo IQR ≈ 1.2 Å, cognate IQR
≈ 2.7 Å). Predicate-active rate is 64% (apo) vs 87% (cognate) — a shift
that is not robustly signed at the population level.

## Affects

- Any Class F active-call rate claim on Block A / B / C.
- Class F receptors (SMO, FZD4, FZD6, FZD7) dominate the negative-delta
  tail on both the tilt and delta_to_active axes.
- FZD6 has |Δd_gpcrdb_tm6_tilt| = 1.03 Å between active and inactive
  references — flagged as reference-degenerate in Phase 1d.

## Evidence

- `dossiers/BLOCK_A/EXPERIMENT_DOSSIER_BLOCK_A.md` §Phase 3c, §Phase 4a, §Phase 1d
- FZD6 (Class F) reference pair 8JHB active vs 8JH7 inactive: tilt Δ 1.03 Å

## Manuscript sentence

> Class F receptors use a tilt-only predicate (they lack the Class A
> NPxxY tyrosine and the Class B kink). Median cognate−apo tilt shift on
> the four Class F receptors is 0.27 Å, within the IQR width in either
> arm; the predicate is a weak discriminator on Class F. FZD6's active-
> inactive reference pair itself differs by only 1.03 Å on TM6 tilt —
> the reference pair is reference-degenerate.
