# C-D-2 — D3 slope derivation script not on disk

## Caveat

The four D3 headline slopes originally cited in
`experiments/024_tier_d3_msa_depth/analysis/tier_d3_full_headline_2026_09_08.md`
(Boltz −1.68, Chai −0.82, OF3 −2.73, Protenix −2.96 %/log(depth))
were produced by hand or one-shot inline compute that was not saved
to disk. GATE-2 of the Block D closeout searched for a derivation
script under `experiments/024_tier_d3_msa_depth/`, `scripts/`,
`analysis/`, `side_analyses/`, `spec/`, `manifest/` and grepped for
`slope`, `linregress`, `polyfit`, `%/log`, `log_depth`, `regression`,
`d3_slope` — nothing hit.

GATE-2's recompute is the authoritative reproduction. It landed as
`analysis/block_d/scripts/derive_d3_slopes.py` in this Block D
closeout pass. The script reproduces the four point estimates to
three decimals from `experiments/024_tier_d3_msa_depth/analysis/full/rows.csv`
under `%/ln(depth)` regression with `full=4096` nominal.

Methods paragraph should cite the recompute path explicitly rather
than treat the numbers as "produced during D3 analysis" — the actual
producer script is the derived one.

## References

- `dossiers/BLOCK_D/gates/GATE_2_D3_SLOPES.md` — search evidence + method + recompute output.
- `analysis/block_d/scripts/derive_d3_slopes.py` — authoritative reproduction script.
- `dossiers/BLOCK_D/partA/PARTA_D3.md` §3 (family-level extension using same method).
