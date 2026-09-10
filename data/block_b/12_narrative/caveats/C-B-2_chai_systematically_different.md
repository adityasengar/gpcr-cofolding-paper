# C-B-2 — Chai is systematically different on Block B (three independent tells)

## Caveat

Chai is a per-backbone outlier on Block B on three independent axes.
Cross-backbone pooling that includes Chai attenuates every effect it
is averaged into; per-backbone reporting is the primary unit.

### Tell 1 — Partial MSA read at the decoy α5-CT

Chai's on-HPC `.aligned.pqt` cache anchors the decoy query row to
WT-parent residues, gaps, or lowercase insertions at the α5-CT positions.
**Panel-wide across all 40 decoy pqts** (Phase 1 §1d):

| observation | count / 40 |
|---|---:|
| decoy pqt query row ends with scrambled tail (uppercase) | **0** |
| decoy pqt query row ends with WT parent tail (uppercase) | 2 (ADRB1, LSHR) |
| decoy pqt query row has ≥3 trailing gaps at the α5-CT position | 19 |
| decoy pqt query row has 1–2 trailing gaps + mostly-WT residues before them | 19 |

For 21 of 40 decoys, scrambled-position residues appear as **lowercase**
(MMseqs2 "insertion") rather than uppercase-aligned. The other three
backbones (Boltz, OF3, Protenix) carry the scrambled α5-CT residues as
**uppercase-aligned** columns in the query row on 6 of 6 audited cells
each (Phase 1D extension). Whether Chai's downstream MSA-feature
builder re-aligns against the raw decoy sequence or trusts the pqt query
row as-is is out of Phase 1 scope (see Flag B-26).

### Tell 2 — Tilt-axis inversion on the shuffled → cognate rung

Chai shows a continuous median-tilt going DOWN shuffled → cognate
(−0.19 Å) while the binary two-instrument rate rises (0.66 → 0.74). The
chai family-term signal lives on NPxxY-OH (cognate 6.79 Å vs shuffled
7.24 Å), not on tilt. Every other backbone signs the top-rung tilt
positively (boltz +0.71, of3 +0.39, protenix +0.55 Å median shift).

### Tell 3 — pLDDT-inversion tell unmeasurable

Block A found Chai carries HIGHER non-engaged partner-pLDDT than engaged
("abandoned partner" tell). Block B replicates the direction reversal
(engaged ≥ non-engaged on every arm) but only 5 of 2,000 Chai cognate
rows are non-engaged (0.25%). **The Block A tell is not falsified; it
is unmeasurable on Block B** — Chai's cognate arm produced near-uniformly
engaged partners.

## Why it matters

- Cross-backbone pooling on the decoy arm reads different MSA
  content on Chai vs the other three; the manuscript's decoy-vs-cognate
  contrast at the MSA-feature layer is a three-backbone claim
  (Boltz + OF3 + Protenix), with Chai reported separately as a
  partial-read outlier.
- The tilt-axis inversion means any manuscript sentence that pins the
  top rung of the ladder to tilt alone will misrepresent Chai.
- The pLDDT-tell falsification test is under-powered on Block B; the
  Block A finding is left unfalsified but untested.

## Affects

- SC-B-6 (Outcome A) — pooled inference on residual axes attenuates
  Chai's per-backbone behaviour but does not remove it.
- SC-B-9 (MSA read-through) — Chai is the one backbone of four where the
  decoy edit is NOT read as uppercase-aligned at column level.
- SC-B-12 (contact register) — Chai contributes to the aggregate but
  has smaller effect magnitudes.
- Any pooled-across-backbones median.

## Evidence

- Phase 1 §1d (Chai `.aligned.pqt` audit; 40/40 decoy pqts).
- Phase 1D extension (Boltz + OF3 + Protenix comparison; 18/18 uppercase).
- Phase 3 §3c (tilt inversion at shuffled → cognate).
- Phase 4d (pLDDT engagement test on Block B).

## Manuscript sentence

> Chai is a per-backbone outlier on Block B on three axes: (i) partial
> MSA read at the scrambled α5-CT — 0 of 40 decoy `.aligned.pqt` query
> rows carry the scrambled residues as aligned uppercase columns
> (the other three backbones verify 18 of 18 cells uppercase-aligned);
> (ii) tilt-axis inversion on the shuffled → cognate rung — Chai's family
> signal lives on NPxxY-OH, not tilt; (iii) unmeasurable partner-pLDDT
> engagement tell — 0.25% non-engaged cognate rows below the 5-row floor.
> Cross-backbone pooling attenuates every effect Chai is averaged into;
> per-backbone reporting is the primary unit.

## Related

- MANUSCRIPT_FLAGS.md Flag B-2, Flag B-12, Flag B-26.
- Block A caveat C-4 (Chai systematic softness — different manifestation,
  same underlying model behaviour).
- Auto-memory `chai_cnr2_apo_model_bias_2026_09_06.md`.
