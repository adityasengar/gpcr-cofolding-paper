# C-C-11 — Deferred gate deliverables

**Applies to**: reviewer-facing notes about scope of this closeout pass.

**Recorded-not-followed** — Part-A deliverables that were designed but
not completed in this pass:

1. **G2d — fold-integrity 10-receptor subset origin test**. Question:
   is Check 2's fold-integrity-finite 10-receptor subset drawn
   disproportionately from the low-pocket-Cα-reference-separation mode?
   `check2_fi_finite_subset.json` records per-backbone AUROC but not
   the receptor list. Re-run required.
2. **G4 full CIF ligand-centroid census** (40,800 CIFs; distance from
   ligand centroid to BW-pocket-anchor centroid; off-site fraction per
   backbone × class). Estimated cost ~5–10 h single-threaded. A minimal
   G4 CIF sample (best/worst/inverted per backbone, 12–16 CIFs) lands
   in `release/structures/block_c/`; the full corpus census does not.
3. **G5 full reference-predicate calibration** — per-reference NPxxY-OH
   + tilt on all 168 Block C references. Partial audit landed (Bug #2
   firing on 10 refs; `active_stabilization_source=agonist_only` count
   = 3 in the whole survey). Full per-ref two-instrument evaluation
   deferred.
4. **G6b fast-path match-count row-level detail** — of the 2,300
   Boltz + Chai fast-path rows on `rescore_t7c_full/rows.csv`, how
   many have exactly 5 tuple matches vs ≥ 6? The manifest column that
   would carry match-count is absent; provenance-sidecar dive or a
   re-scoring pass required.
5. **G7 orthogonal corroboration** — pocket-lining side-chain contact
   fingerprint classifier proposed in the gating report. Not
   implemented in this pass.
6. **Cluster-boot recompute on the 2×2 interaction** (see C-C-3).
7. **Full rebuild-and-diff harness** — the release-repo Makefile has
   scaffolding for `make all` invoking per-block rebuild scripts, but
   `rebuild_block_a.py` is currently a stub (exits 20, does not
   compute), and no `rebuild_block_b.py` or `rebuild_block_c.py` script
   exists. The only integrity check that runs today is `make
   ledger-check` (SHA-256 verification of every explicit
   `<file>.sha256=<hash>` assertion in `LEDGER.csv` — enforces file
   integrity but not scientific correctness of any claim's number).
   Full rebuild-and-diff (all three blocks) is tracked as
   deferred-post-submission; not silently dropped. See
   `release/VERSION.md` §"Rebuild-and-diff harness — deferred, tracked".

**Manuscript posture**: none of these are load-bearing on any surviving
Block C claim. Each has a Discussion sentence available if a reviewer
raises it. The manuscript should not depend on any of these six items
for its abstract or headline claims.
