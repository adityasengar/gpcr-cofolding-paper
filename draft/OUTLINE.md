# OUTLINE.md — the manuscript skeleton

Target: Nature Communications on the landed corpus (Nature Methods conditional on D2).
Preprint to bioRxiv first. See `../STATUS.md`.

Sections are written **one per session**, from `../CLAIMS.md` plus the two ledgers —
never from raw PDFs or raw CSVs. Each section below states what it may cite and what
gates it.

---

## Abstract — write last
Gate: every claim it compresses is already `ready` in `CLAIMS.md`.

## Introduction (~2 printed pages)
Structure, per `../lit/PROMPTS.md` Prompt 2:
1. **Problem** — C1. Why state matters, why single-structure prediction is insufficient.
2. **What has been tried** — grouped by approach, not one paper per sentence. Template
   biasing, MSA manipulation, latent steering, benchmarks. Every group cites citekeys.
3. **The gap** — C3, C4, C5. Built by reading down the `oracle_leakage`, `prospective`,
   `states_generated` and `anti_memorization` columns of `lit/INDEX.md`. **Name the
   nearest near-miss explicitly** — a gap paragraph that names none is not credible.
   The near-miss is `yang2025statespecific`.
4. **What we do** — landed blocks only.
5. **Contributions** — three or four, each falsifiable.

- may cite: `lit/` citekeys with page numbers. **No `[R-*]` numbers.**
- gate: **ready now.** C1–C5 are all lit-only and all marked ready.
- rebuild trigger: if D2 lands, the gap paragraph must be rewritten — the papers worth
  contrasting against change.

## Results
Ordered by block: A (apo vs cognate) → B (ladder + decomposition) → C (ligand class) →
intermediate census → the confidence finding.
- may cite: `[R-*]` ledger ids **only**, plus lit citekeys for contrast.
- gate: **blocked.** Most of `RESULTS.md` is `NOT-LOCALLY-CHECKABLE` on the current
  export. Do not draft prose against `STATUS.md` numbers directly.
- every number needs its denominator in the sentence or the caption.

## Methods
- may cite: the provenance columns of `rows_enriched_v3_7.csv` — `scorer_git_sha`,
  `scorer_version`, `bw_derivation_source`, `gpcrdb_*`, `ref_pdb_sha_active/inactive`,
  `input_sha256`.
- gate: **ready now, and independent of the data refresh.** The protocol, scorer
  version, thresholds, reference sets and anchor derivation are all already recorded.
- must state: the state predicate and its threshold, how borderline is defined, the
  reference set construction, and the anti-memorization design.

## Discussion
- must engage, not omit: `tran2026nanogs`, `vo2026fiducials`, `ku2026promise`,
  `mattsson2026leakage`, `skrinjar2026generalization`. See the threats table in
  `../CLAIMS.md`.
- gate: needs Results.

## Figures → `../figures/`
Design by analogy through `litquery` (match on `data_shape`, not subject matter).
**Check `reuse` before adapting any panel** — 24 of 66 corpus papers carry a
restriction: 15 ND, 3 all-rights-reserved, 6 with no licence statement. ND forbids
redrawing, not merely copying.

## References
`lit/refs.bib`, 70 entries. Four have no note and no PDF and must not be cited:
`chiesa2025templatebias`, `bret2025boltz2docking`, `nittinger2025cofolding`,
`yu2026domainmotion`.

---

## Order I would write in

1. **Methods** — ready now, unblocked by the refresh, and it forces the state predicate
   to be pinned down before any Results sentence leans on it.
2. **Introduction** — ready now; C1–C5 are lit-only.
3. Results, once the export lands. Then Discussion, then Abstract.
