# C-B-13 — Paralog cluster map reconstructed 2026-09-09

## Caveat

The 26-cluster paralog map at
`experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`
was **reconstructed** on 2026-09-09 in Phase 3 for cluster-boot CI
computation. It is not a canonical shipped file.

**Two observed facts**:

1. Phase 0 addendum cites "26 paralog clusters" but shipped no file.
2. Every shipped Block C bootstrap (four implementations enumerated in
   `scripts/reaudit_2026_09_07/t2_bootstrap_sanity.py`) uses
   **receptor-as-cluster** (40 clusters), not paralog groups.

The reconstructed map hits 26 clusters by treating OPRX (nociceptin/NOP)
as its own cluster distinct from the DOR/MOR/KOR opioid triplet; other
groupings follow canonical aminergic / peptide / chemokine / opsin
family boundaries.

## Why it matters

- All Block B cluster-boot CIs in Phase 3/4/5/6 use the reconstructed
  26-cluster map. Every published Block B CI is anchored to this
  reconstruction, not to a git-committed authoritative file.
- Block A's cluster-boot convention (Block A caveat C-8) uses "26
  paralog clusters" but the Block A archive is not co-located with a
  cluster-map file either; the two are the same reconstruction
  implicitly.
- Downstream Phase 7 should decide whether to (a) formalise the
  reconstruction with a git commit + review, (b) fall back to
  receptor-as-cluster for consistency with existing Block C bootstraps,
  or (c) both. **Recommended: (a); (b) reported as sensitivity.**

## Affects

- SC-B-1 (cluster-boot CIs on the ladder).
- SC-B-2 (decomposition CIs).
- SC-B-3 (2×2 engagement × activation CIs).
- SC-B-6 (Phase 5 residual test CIs).
- SC-B-11 (ladder-height regression CIs).

## Manuscript sentence

> Confidence intervals are 1000-resample cluster-bootstrap over 26
> paralog clusters (aminergic subfamilies grouped; opioid triplet
> DOR/MOR/KOR + OPRX-nociceptin as separate cluster; chemokine and
> peptide-hormone family groupings per canonical GPCR taxonomy). The
> cluster map at
> `experiments/019_block_b_partner_selection/analysis/paralogy_clusters.csv`
> was reconstructed 2026-09-09 for this analysis; receptor-as-cluster
> bootstrap (40 clusters) is reported alongside as sensitivity in the
> supplementary.

## Related

- MANUSCRIPT_FLAGS.md Flag B-14.
- Phase 3 §3g.
- Block A caveat C-8 (cluster-boot authoritative).
