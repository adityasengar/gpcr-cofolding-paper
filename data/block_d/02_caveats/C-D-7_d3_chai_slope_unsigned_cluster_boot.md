# C-D-7 — Chai's D3 slope is NOT signed under cluster-boot 95 % CI

## Caveat

D3 slopes (%/ln(depth), cluster-bootstrap over 22 paralog clusters,
1000 replicates per GATE-2):

- Boltz: −1.684 [−2.692, −0.812] — signed
- Chai: −0.815 **[−2.380, +0.357]** — **UNSIGNED** (crosses zero)
- OF3: −2.732 [−4.365, −1.145] — signed
- Protenix: −2.956 [−4.678, −1.581] — signed

Chai's point estimate is negative, but its cluster-boot 95 % CI
crosses zero. **The claim "Chai's slope is significantly negative"
cannot be made at n=22 clusters.** Any manuscript sentence must
respect the CI:

> "Chai's slope is −0.82 %/ln(depth) in point estimate but is not
> distinguishable from zero at n=22 clusters under cluster-boot
> convention (95 % CI [−2.38, +0.36])."

This aligns with headline F2's "muted response" language but now
quantifies it. The D3 mechanism split (SC-D-8) treats Chai as a
"muted lever" not because its slope is negative, but because its
fold-integrity is preserved (76-82 % geometric fidelity, matched-seed
Cα 2–5 Å, pLDDT stable) — a lever-like non-degrading response that
the depth axis doesn't strongly detect.

Consistent with Chai's D1 F5 receptor-locked-apo pattern: Chai
maintains a strong internal prior and MSA depth doesn't override it.

## References

- `dossiers/BLOCK_D/gates/GATE_2_D3_SLOPES.md` §Chai unsigned.
- `dossiers/BLOCK_D/partA/PARTA_D3.md` §1 (reframed F1).
- `dossiers/BLOCK_D/gates/GATE_3_STEERING_VS_DEGRADATION.md` §Chai muted lever verdict.
