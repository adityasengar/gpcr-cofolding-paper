# CURATE-E addendum — A1 identity-anchor rule correction (Q#3 fix)

**Date**: 2026-08-26
**Owner**: paper_af3 experiment-analyst subagent
**Context**: Correcting a plan-vs-code discrepancy that caused CURATE-E to over-refuse 5 receptors.

## What went wrong

The delegation brief I wrote for the Phase 2 CURATE subagents stated the identity-anchor rule as:

> **Guardrail (1)**: Identity-defining anchors (3.50 R, 5.58 Y, 7.53 Y) must match GPCRdb-reported residues. No exceptions, no soft-fail.

**This was factually incorrect.** The actual scorer contract:

- **`scorer/anchors.py:78-81`** (`resolve_anchors`): builds the `AnchorSet` from GPCRdb `services/residues/extended/<slug>/`, populating each `Anchor.aa_expected` from the **receptor-specific** residue at the BW-generic position. It is NOT a hardcoded R/Y/Y table.
- **`scorer/verified.py:181-192`**: A1 gate at build time checks `if aa != anchor.aa_expected and label in identity_defining` where `identity_defining = ("3.50", "5.58", "7.53")`. The check is per-receptor — a receptor whose native 5.58 is Cys has `anchor.aa_expected = "C"`, and A1 passes when the crystal has `C` at 5.58.

The comment at `verified.py:173-177` explains the rationale ("3.50 R needed for DRY guanidinium CZ", etc.), but the code doesn't enforce family-canonical residues — it enforces per-receptor consistency.

**Rule as actually enforced by the scorer**:
- A1 hard-raises when the crystal residue at 3.50 / 5.58 / 7.53 differs from what GPCRdb says the wt residue is for THAT receptor at that BW position.
- Side-chain-specific axes (`d_dry` needs R guanidinium; `d_y558_pack` needs Y OH) return per-axis NaN for receptors where the side chain isn't R/Y — but this is a per-axis measurement outcome, not an A1 gate.
- CA-CA axes (`d_r350_r630_ca` primary axis; `d_npxxy` between 5.58 CA and 7.53 CA) work regardless of side-chain identity.

## Receptors CURATE-E REFUSED that ACTUALLY pass A1

CURATE-E's REFUSED-at-receptor-level list (§ "Identity-anchor policy — 5-receptor question"):

| Receptor | Non-canonical residue | Native at that position | A1 verdict under ACTUAL contract |
|---|---|---|---|
| GPR55 | 5.58 = **C** (Cys) | GPCRdb reports 5.58 = C for GPR55 (native) | **PASSES** (C matches C) |
| GP132 (GPR132) | 5.58 = **N** (Asn) | GPCRdb reports 5.58 = N for GPR132 | **PASSES** (N matches N) |
| P2Y10 | 5.58 = **T** (Thr) | GPCRdb reports 5.58 = T for P2Y10 | **PASSES** (T matches T) |
| FFAR2 | 7.53 = **F** (Phe) | GPCRdb reports 7.53 = F for FFAR2 (native NPxxF variant) | **PASSES** (F matches F) |
| HCAR3 | 5.58 = **S** (Ser) | GPCRdb reports 5.58 = S for HCAR3 | **PASSES** (S matches S) |

**Verification**: an individual per-prediction `.scorer.json` for these receptors would show `anchor_5_58_aa_expected` == the native non-canonical residue AND `anchor_5_58_aa_observed` == same. Fields agree. A1 does not raise. The rows would enter `reference_set.csv` with numeric `d_r350_r630_ca_ref` computed as CA-CA distance (side-chain-agnostic).

## Consequences for each receptor's classification

For all 5 receptors:
- Primary axis `d_r350_r630_ca` (R3.50 CA to R6.30 CA) works — CA atoms don't care about side chain.
- `d_npxxy_y558_y753_ca` (5.58 CA to 7.53 CA) works — CA atoms only.
- `d_dry_sidechain_r350cz_e630oe1` (3.50 guanidinium CZ to 6.30 carboxylate OE) — all 5 have 3.50=R (canonical); this axis works. The 6.30 residue's OE would need to be aspartate/glutamate — check per receptor.
- `d_y558_pack_min_heavy` (Y5.58 side-chain packing) — **fails for GPR55/GP132/P2Y10/HCAR3** (no Tyr OH). Returns per-axis NaN. FFAR2 has Y at 5.58 → works.

Bottom line: the primary axis measurement works for all 5. Some auxiliary axes return per-axis NaN. That's the design (per-axis NaN is legitimate, not a gate failure).

## Corrected proposal for CURATE-E's 5 REFUSED cases

Under the ACTUAL scorer contract, these 5 receptors move from **REFUSED-wholesale** → **PROPOSE (single-side active only)**. None has an inactive PDB with resolved 6.30 CA (per CURATE-E's structure enumeration, confirmed via GPCRdb), so no delta-pair is possible for any of them — same limitation as the 9 already-PROPOSE-active-only receptors in CURATE-E.

| Receptor | UniProt | Best active PDB | Resolution | d_r350_r630_ca (measured by CURATE-E) | Notes |
|---|---|---|---:|---:|---|
| GPR55 | Q9Y2T6 | **8ZX4** (LPI + Gα13) | 2.85 Å | not measured (CURATE-E refused early) | 5.58=C native; d_y558_pack per-axis NaN; other axes work |
| GP132 (GPR132) | Q9UNW8 | **8HQE** (apo + Gi, BRIL N-term fusion) | 2.97 Å | not measured | 5.58=N native; d_y558_pack per-axis NaN |
| P2Y10 | O00398 | **8KGG** (only deposit; Gα13 + LysoPS) | not stated | not measured | 5.58=T native; only 1 P2Y10 structure ever solved |
| FFAR2 | O15552 | **8J24** (Gi + acetic acid) | 2.60 Å | not measured | 7.53=F native (NPxxF variant); all CA-CA axes work; canonical NPxxY interpretation doesn't apply |
| HCAR3 | P49019 | **8JEI** (Gi + CW3) | 2.73 Å | not measured | 5.58=S native; d_y558_pack per-axis NaN |

**Recommendation**: append these 5 to the CURATE-E PROPOSE-active-only list. Total single-side active-only under corrected rules: **14 receptors** (was 9).

**Prerequisites for materialisation**:
1. CURATE-E's measurements for the 5 corrected receptors need to be computed (~5 min per receptor, mirroring CURATE-E's own script trace). Someone needs to run `d_r350_r630_ca` on the 5 chosen PDBs to fill the Δ column.
2. The 5 rows need to be added to `refs/reference_pdbs.csv` (same edit path as AA2AR/MC3R materialisation, currently in-flight).
3. Q#1 (active-only classification path) must be answered — if the scorer's `state_thresholds.csv` fallback classifies from `d_active_ref` alone, these 5 unlock predictions; if not, they unlock 0 via the delta axis and 0 via the fallback.

## Prediction-count impact

From the never-curated bucket in earlier analysis:
- GPR55: ~40 predictions in the corpus
- GP132: ~40
- P2Y10: ~30
- FFAR2: ~40
- HCAR3: ~30

**Total: ~180 additional predictions become classifiable IF Q#1 answered "yes" to active-only classification.** Under strict delta-pair-only interpretation, the gain is 0.

## What this does NOT change

- GPR34 marginal case (|Δd|=2.96 vs 3.0 threshold): still rejected under the 3.0 rule. Q#4 stands as a separate policy decision.
- The 9 other CURATE-E PROPOSE-active-only receptors (GP101, GPR3, GPR12, GPR15, GPR34, GPR84, GPER1, DRD5, SUCR1): unchanged. Still active-only.
- Structural ceiling for Class B/C/F receptors that genuinely lack a canonical 6.30 anchor: unchanged. These 5 GPR-orphans are Class A with a non-canonical side chain at ONE identity anchor — different failure mode.

## Broader lesson

The plan brief hardcoded a stricter rule than the code implements. Two options going forward:

- **(a) Keep the code as-is**: per-receptor A1 gate is the correct behavior. Fix future plan briefs to match. Add a test that asserts a non-canonical-5.58 receptor (e.g. GPR55) passes A1 when crystal-observed matches GPCRdb-expected.
- **(b) Make the code stricter** to match the plan brief's intent: hard-fail on family-canonical mismatch (5.58 must be Y regardless of what GPCRdb says the native is). This would BAN these 5 receptors permanently.

Recommendation: **(a)**. The per-receptor rule is defensible science (each receptor's native residue IS what its structure evolved to fold on) and unlocks ~180 predictions. Option (b) would be more conservative but scientifically unjustified — a Cys at 5.58 in GPR55 is real biology, not a construct artefact.

## Merge instructions

When merging CURATE proposals into the final `refs/reference_pdbs_proposal_FINAL.md`:
- Move the 5 receptors from CURATE-E's REFUSED section to its PROPOSE-active-only section
- Cite this addendum in the merge document
- Note that CURATE-E's own measurements need to be extended to include these 5 (currently just PDBs picked, not d_r350_r630_ca computed)

## Follow-up code work

Recommend adding a unit test in `tests/test_verified.py` (or `tests/test_delta_population.py`) that specifically covers the non-canonical-5.58 case:

```python
def test_a1_passes_when_crystal_matches_per_receptor_gpcrdb_expected():
    """CURATE-E Q#3 regression: a receptor whose native 5.58 is Cys
    (e.g. GPR55) must pass A1 when the crystal has Cys at 5.58.
    Family-canonical rule is NOT enforced — per-receptor GPCRdb rule is."""
    # Build an AnchorSet where aa_expected at 5.58 = 'C'
    # Provide an UnverifiedReference with residue 'C' at 5.58's uniprot_pos
    # Assert verify_reference_pdb does NOT raise A1
    ...
```

This test prevents future subagents (or future code changes) from re-introducing the family-canonical assumption.
