# STATUS.md — what has landed, what has not

Read before any query that touches the draft. The distinction below is the one
thing an agent cannot infer and will otherwise get wrong in a way that reads
perfectly fine.

**Rule for any agent using this file:** no sentence in any draft may depend on a
block listed under PLANNED. If a draft sentence needs one, flag it rather than
writing it.

---

## LANDED — may be cited in the draft

### Block A — apo vs. cognate
- ~9,500 predictions, 48 receptors, 4 backbones
- Cognate Gα drives active state; apo lands inactive on medians but produces
  active-like structures at ~14.5% mean rate
- OPSD/apo/Boltz within 0.40 Å of active crystal
- Two-instrument predicate: 90.5% agreement, 572 genuine disagreements over ~6,000
- Status: audited

### Block B — apo / decoy / shuffled / cognate
- ~32,000 predictions
- Graded activation ladder ~16% → 55% → 81% → 89%
- Decomposition: occupancy ~54%, α5-CT sequence ~35%, correct family ~11%
- Status: audited

### Block C — ligand class separation
- Binary-predicate negative result inverted under continuous pocket geometry
  (binary predicate floor-pinned in apo, ceiling-pinned in cognate; ~65% of cells
  unresolvable)
- All four backbones produce ligand-class-specific pocket conformations
- Survives a well-powered anti-memorization test
- Status: audited

### Intermediate conformation census
- Decoy arm interior fraction ~53.8% — real intermediate density, not mode-mixing
- Partner construct tunes a continuous coordinate rather than switching states

### Infrastructure finding
- Boltz-2 lands ~9 Å at AA2AR with higher pLDDT than OF3/Protenix, which land
  within 0.6 Å. Model confidence does not discriminate conformational correctness.
- AA2AR: bimodal with sparse in-between (not "bistable")

---

## PLANNED — NOT RUN. Must not appear in any draft sentence.

### D1 — deep apo sampling on bistability candidates
- ~12,000 predictions. NOT RUN.

### D2 — β2AR Nb60/Nb80 directed-inactive nanobody arm
- ~800–4,800 predictions. NOT RUN.
- If it lands, the claim moves from state selection to directional conformational
  control, and the gap paragraph in the intro must be rebuilt — the papers worth
  contrasting against change.

### D3 — MSA-depth tier
- ~26,000 predictions, 2-receptor smoke test first. NOT RUN.

### T1.5 — redocking (CPU)
- Runs alongside drafting. Status: in progress / not landed.

---

## Venue target
Nature Communications on the landed corpus. Nature Methods conditional on D2.
Preprint to bioRxiv on the current corpus.
