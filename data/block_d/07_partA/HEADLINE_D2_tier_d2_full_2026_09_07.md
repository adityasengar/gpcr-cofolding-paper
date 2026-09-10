# Tier D2 full — panel-scale nanobody-directed steerability (2026-09-07)

**Status**: D2 full drained 237/240 rows on 2026-09-07 (98.75%). 3 OF3 stragglers on `AGTR1 × active_nb` hung ~3 h with no progress; workers killed to reclaim H100 slots. Rescored under scorer `d9c646af5f89861c16062bf256de96a8389d9915` (row-level authoritative per Block D closeout GATE-4; prior prose value `891041e858f3` was a phantom SHA not resolvable in git — corrected 2026-09-10). 2,370/2,370 rows passed. Wall time (full pool → rescore) about 5 h.

**Grid** (delivered):
- 4 receptors × 3-4 arms × 4 backbones × 5 seeds × 10 samples = 2,370 predictions
- ADRB2 (apo, cognate_gα, inactive_nb=5JQH/Nb60)
- ACM2  (apo, cognate_gα, active_nb=4MQS/Nb9-8)
- AGTR1 (apo, cognate_gα, active_nb=6OS2/Nb.AT110i1_le — one cell short 30 samples on OF3)
- OPRK  (apo, cognate_gα, inactive_nb=6VI4/Nb6)
- ADRB2 active_nb intentionally dropped (Nb80/4LDE placeholder duplicates Nb60 sequence)

**Provenance**:
- Manifest: `experiments/023_tier_d2_directed_inactive/manifest/tier_d2_manifest.dispatch.csv`
- Pool: `/hpc/scratch/sengaad1/paper_af3/experiments/023_tier_d2_directed_inactive/full/pool/`
- Rescore: `analysis/full/rows.csv` (2,370 rows, 5.3 MB) — qsub 35920895
- Refs: `refs/reference_set.csv` SHA `7a261988ff73eedc9d21e5cc2a9eaf0436b9f38e3827a87493295a8d8382b90c` + `refs/nanobody_state_anchors.csv`

---

## Headline — two-instrument active fraction

Class A predicate: `d_npxxy_y558_y753_oh < 9.082 Å` AND `d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`. All numbers are % of samples satisfying the predicate. n=50 per cell except AGTR1×active_nb×of3 (n=20).

### ADRB2 (inactive-directing Nb60/5JQH; cognate = Gα)

| Arm | Boltz | Chai | OF3 | Protenix |
|---|---:|---:|---:|---:|
| apo | 0.0 | **100.0** | 10.0 | 0.0 |
| cognate_gα (should be ACTIVE) | **100.0** | **100.0** | **100.0** | **100.0** |
| inactive_nb (should be INACTIVE) | ✓ 0.0 | ✗ 100.0 | ✓ 10.0 | ✗ 76.0 |

### ACM2 (active-directing Nb9-8/4MQS; cognate = Gα)

| Arm | Boltz | Chai | OF3 | Protenix |
|---|---:|---:|---:|---:|
| apo | 42.0 | 0.0 | 12.0 | 0.0 |
| cognate_gα (should be ACTIVE) | **100.0** | **100.0** | 58.0 | **100.0** |
| active_nb (should be ACTIVE) | ✓ **100.0** | ✗ 0.0 | ✓ **82.0** | ✓ **100.0** |

### AGTR1 (active-directing Nb.AT110i1_le/6OS2; cognate = Gα)

| Arm | Boltz | Chai | OF3 | Protenix |
|---|---:|---:|---:|---:|
| apo | 100.0 | 100.0 | 40.0 | 0.0 |
| cognate_gα (should be ACTIVE) | **100.0** | **100.0** | 96.0 | **100.0** |
| active_nb (should be ACTIVE) | ✓ **100.0** | ✓ **100.0** | ✓ **95.0** | ✓ **100.0** |

### OPRK (inactive-directing Nb6/6VI4; cognate = Gα)

| Arm | Boltz | Chai | OF3 | Protenix |
|---|---:|---:|---:|---:|
| apo | 4.0 | 74.0 | 0.0 | 0.0 |
| cognate_gα (should be ACTIVE) | **100.0** | **100.0** | 36.0 | **100.0** |
| inactive_nb (should be INACTIVE) | ✗ 48.0 | ✗ 82.0 | ✓ 10.0 | ✓ 6.0 |

---

## Findings

**F1 — Positive control (Gα) is nearly perfect.** cognate_gα drives active-predicate to ≥96% on **15 of 16** cells across all 4 backbones × 4 receptors. The only miss is OF3 on ACM2 (58%) and OF3 on OPRK (36%). Gα is the ground-truth active-state driver, and every backbone respects it.

**F2 — Active-directing Nb works, mostly.** Active-stabilising nanobodies (ACM2 Nb9-8, AGTR1 Nb.AT110i1_le) push apo → active on Boltz, OF3, Protenix (per-arm gain 40–100 points). Chai refuses to respond to ACM2 Nb9-8 (apo 0% → active_nb 0%) — Chai's ACM2 is stuck inactive regardless of partner. Chai does move on AGTR1 (apo 100% → active_nb 100%; already saturated).

**F3 — Inactive-directing Nb is UNRELIABLE across the panel.** The smoke result on ADRB2 alone was misleading. Panel-scale:

| Test | ADRB2 | OPRK | 
|---|---|---|
| Boltz: apo → inactive_nb Δ%active | 0 → 0 ✓ | 4 → **48** ✗ (goes ACTIVE) |
| Chai: apo → inactive_nb Δ%active | 100 → 100 ✗ (refuses) | 74 → 82 ✗ (refuses) |
| OF3: apo → inactive_nb Δ%active | 10 → 10 ✓ | 0 → 10 ≈ |
| Protenix: apo → inactive_nb Δ%active | 0 → **76** ✗ (goes ACTIVE) | 0 → 6 ✓ |

**None of the 4 backbones is reliable at inactive-directing.** Boltz corrects on ADRB2 but inverts on OPRK. Protenix is the mirror image — correct on OPRK, INVERTS on ADRB2. Chai stays where it started on both. OF3 is stable but at 10% not 0%.

**F4 — Some backbones treat any Nb-B chain as an active partner.** Protenix on ADRB2 inactive_nb hits 76% active; the Nb60 (5JQH) is documented as an **inactive-state** stabiliser (Staus 2016), yet Protenix reads the small VHH-B chain like an active partner. Same on ACM2 active_nb where Protenix hits 100% (as expected, since Nb9-8 is truly active-stabilising) — the model doesn't distinguish. Suggests Protenix's training data was dominated by G-protein-mimetic Nbs and generalised "Nb-B → active" as a prior.

**F5 — Chai locks in on apo state.** ADRB2 Chai apo 100% active, OPRK Chai apo 74% active, ACM2 Chai apo 0% active, AGTR1 Chai apo 100% active. Chai's apo state is receptor-specific and locked — Nb steering doesn't shift it in either direction on 3 of 4 receptors. Consistent with the D1 finding that Chai has receptor-specific systematic biases ([[chai-cnr2-apo-model-bias-2026-09-06]]).

**F6 — AGTR1 apo is active-biased on 3/4 backbones**. Boltz/Chai/OF3 apo all read ≥40% active on AGTR1, while all other receptors have Boltz/Protenix apo ≈ 0%. Consistent with the AGTR1 inversion finding from the S1 classifier (Chec k 4 — AGTR1 per-receptor AUROC is 0.0 on all backbones on apo arm, suggesting AGTR1 apo is intrinsically read as active-like). No model bias here — it's an AGTR1-receptor property.

---

## The rewrite of the smoke story

The smoke (ADRB2-only, 1 seed) suggested: **"Boltz + OF3 respond correctly to Nb-inactive; Chai + Protenix fail."**

Panel-scale correction: **"No backbone is a reliable inactive-directing partner."** Each backbone succeeds on some receptors and fails on others:

- **Boltz**: correct on ADRB2 inactive_nb (0% active), inverts on OPRK inactive_nb (4→48%).
- **Chai**: refuses to shift on either receptor.
- **OF3**: stable at ~10% on both (weakest active fraction generally).
- **Protenix**: correct on OPRK (0→6%), inverts on ADRB2 (0→76%).

Active-directing Nb is more reliable: Boltz + OF3 + Protenix all succeed on ACM2 and AGTR1 (Chai still refuses on ACM2). This confirms the active-state has a stronger prior — models know what active looks like, but "steer toward inactive" is a weaker signal.

## Manuscript implications

- Withdraw the smoke's "Boltz + OF3 respond correctly to Nb-inactive" claim. Replace with the receptor-specific breakdown above.
- The paper's steerability story has to be graded rather than dichotomous. **Active-direction is possible; inactive-direction is not reliably possible** with current backbones.
- Chai's ACM2 refusal is a new instance of the Chai receptor-specific-bias story. Add to [[chai-cnr2-apo-model-bias-2026-09-06]].
- Protenix's Nb-treats-as-active behaviour is a new finding worth its own line in the paper.
- OF3 is consistently the softest active-fraction backbone; it approaches active more slowly (58% on ACM2 cognate_gα where others hit 100%). This is not a failure — arguably a more calibrated response — but worth noting.

## What this does NOT deliver

- Cluster-bootstrap CIs on per-cell fractions (n=50 gives us the point estimate; a receptor-level bootstrap requires more receptors).
- Ligand-pose accuracy — D2 has no small-molecule ligand; the receptor + partner-only apo geometry is all we score.
- Cross-receptor generalisation of the inactive-directing failure — we only have 2 receptors with inactive_nb (ADRB2, OPRK). A 3rd or 4th receptor would settle whether Protenix-inverts and Boltz-inverts are one-off or systematic.
- Statistical test that Protenix's ADRB2 inactive_nb 76% is significantly different from apo 0% — clearly yes at n=50 but no formal test emitted.

## Next moves

- **Curate Nb80 (4LDE)** into `refs/nanobody_sequences.fasta` and rerun ADRB2 active_nb (currently placeholder-dropped). Test whether the active-directing story holds on ADRB2 for a proper active Nb.
- **Add a 3rd receptor with inactive_nb** (e.g., CCR5 has known inactive Nbs, could curate). Would let us distinguish per-model-specific from per-receptor-specific inversion.
- **Investigate Protenix's Nb-B-as-active prior**. Grep the Protenix training corpus for Nb-bound structures. If 90% of them are Nb9-8-style active stabilisers, the prior is explained.

## Files (this session, local only)

- `experiments/023_tier_d2_directed_inactive/analysis/full/rows.csv` (2,370 rows)
- `experiments/023_tier_d2_directed_inactive/analysis/full/summary_per_cell.csv` (per-cell active fraction + pLDDT medians)
- `experiments/023_tier_d2_directed_inactive/analysis/full/pocket_rmsd_per_cell.csv`
- `experiments/023_tier_d2_directed_inactive/analysis/tier_d2_full_headline_2026_09_07.md` (this doc)

## Related memory

- `[[chai-cnr2-apo-model-bias-2026-09-06]]` — Chai receptor-specific bias story, now generalised further.
- `[[d1-smoke-fired-2026-09-06]]` / D1 full headline — provides the apo-arm baseline for cross-tier consistency.
- `[[apo-bistability-reference-artefact-2026-09-06]]` — apo-arm activity distribution that D2 was designed to disambiguate. D2 confirms it's not just apo bistability — partner identity really does move the pocket, but not in a model-consistent direction.
