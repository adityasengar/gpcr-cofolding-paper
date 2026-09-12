# Figure allocation and main-text shape — a proposal

Written 2026-09-10 by the lit session, at Aditya's request and to answer `paper-6f`'s five
placement questions. **This is a proposal, not an edit.** Nothing in `figures/`,
`sections/*.tex` or `FIGURES.md` was touched.

Everything below is a corpus count with a method stated. Where the corpus has no answer I say so.

---

## The five questions, answered with counts

### Q1 — how many main-text figures do comparable papers run?

**Median 5, range 3–9, n = 13.** Measured by counting caption-initial `Figure N` occurrences in
the PDFs of peer-reviewed papers with a comparable shape (structure-prediction benchmark or GPCR
state work), not from the notes — the notes' figure tables record *panel-group rows*, and the
schema splits one figure across several, so neither `INDEX.md` nor `notes/` gives a usable figure
count. That is a limitation of our own instrument and it is why this number was measured directly.

| paper | venue | main figs |
|---|---|---|
| `zhang2026generalization` | npj Drug Discovery | 3 |
| `paajanen2026activation` | — | 4 |
| `lewis2025bioemu` | — | 4 (+8 SI) |
| `abramson2024af3` | **Nature** | **5** |
| `krishna2024rfaa` | **Science** | **5 (+11 SI)** |
| `chiesa2025templatebias` | JCIM | 5 |
| `mitjavila2026afsample2t` | JCIM | 5 |
| `chitsazi2025gpcrdock4` | — | 5 |
| `stein2022speachaf` | — | 5 |
| `waymentsteele2024cluster` | — | 5 |
| `lazou2026cryptic` | Commun Biol | 6 |
| `matic2023gpcrome` | — | 9 |
| `nittinger2025cofolding` | AILSCI | 9 |

**The two highest-profile venues in the corpus both run exactly 5 main figures with a heavy SI.**
That is the Nature-family pattern and it is the one to copy: a small, load-bearing main sequence,
with everything else in SI. `heo2022multistate` and `wallner2023afsample` returned 0 and are
extraction artifacts (uppercase or non-standard caption format), not zero-figure papers — excluded
rather than counted as 0.

**Recommendation: 6 main figures.** One above the median is defensible for a paper spanning four
blocks; 8+ would be arguing against every comparator we have.

### Q2 — do per-receptor / per-target breakdowns go to main or SI?

**Main, overwhelmingly: 93 main-text vs 18 SI**, counted across every figure row in 74 notes whose
gist or data_shape mentions per-target, per-receptor or per-system.

This **reverses the assumption in the question.** Promoting BC-2 and BB-6 is not cutting against
convention, it is following it. And the independent argument is stronger than the conventional one:
BC-2 caught a mislabel *because* it showed the distribution rather than the summary. This project
has already had one headline result inverted by pooling over per-system, which is why `hides` is a
schema field at all. **Promote both.**

### Q3 — is a workflow/schematic Figure 1 normal, and is it ever criticised?

**Normal. 19 of 31 papers with a parseable Figure 1 lead with a schematic or workflow (61%)**,
against 6 leading with a structure render and 6 with a result. `chiesa2025templatebias` — our
nearest neighbour — leads with a schematic, as do `chai2024chai1`, `kalakoti2026afsample3` and
`yang2025statespecific`.

**No criticism of the practice appears anywhere in the corpus.** Spend Figure 1 on the schematic.
For a paper whose contribution is partly an instrument, that is the convention *and* the honest
choice.

### Q4 — is there precedent for a main-text figure whose message is "this does not work"?

**Yes, and it is strong: 37 main-text negative-result panels vs 3 in SI.**

`yu2026domainmotion` (PNAS 123(10)) is the model, and its *entire contribution* is negative.
Non-binder ligands reproduce nearly the same domain motion as the native trigger — the ligand raises
the holo-like fraction by only 11.9% and 9.1% in two groups against a 40.3% difference attributable
to training-set composition alone. Its confidence finding is put plainly in the Significance
statement: pLDDT values *"are generally not sufficient for discriminating between binder and
nonbinder ligands"*, and the non-binder arm sits in **main-text Fig. 5**.

It also reports the effect in both directions rather than only where it helps — for one group
"the nonbinders are placed with almost the same confidence as the trigger ligands", for another
"the nonbinder ligands have substantially lower pLDDT values". **That two-directional honesty is
the framing to copy for BA-4 and BA-5.** Put both in main text.

### Q5 — precedent for a main-text instrument-calibration panel?

**Yes, though thinner: 9 main vs 1 SI.** `lee2026confornets` figs 2B and 3B, `chai2024chai1` fig
5A–B, `protenix2025` fig 8A–C, `vo2026fiducials` fig 2, `junker2026peptidedesign` fig 7B.

So BA-1 in main text is precedented, and the reasoning in the question is right: our two-instrument
predicate is the paper's foundation, and an instrument shown only in SI reads as assumed rather
than checked. **Keep BA-1 in main text, but merge it into Figure 1 with the schematic** — that is
what `chai2024chai1` and `protenix2025` effectively do, and it buys a main-figure slot.

---

## Proposed main text: 6 figures

| # | content | source panels | why main |
|---|---|---|---|
| **1** | Schematic + the predicate, calibrated on structures of known state | F1 + BA-1 + BA-6 | Q3 (61% precedent) and Q5; establishes the instrument before any claim rests on it |
| **2** | The main effect: co-input drives active-state geometry, four backbones | BA-2 + BA-3 | the Block A result the paper is built on |
| **3** | The ladder: four arms including decoy and shuffled, **plus per-receptor** | BB-1 + BB-6 | the titular claim; Q2 says per-receptor belongs here |
| **4** | Decomposition — presence vs sequence vs family; engagement separable from activation | BB-2 + BB-3 + BB-5 | what the effect actually decomposes into |
| **5** | **The negatives:** amplitude is a switch not a dial; confidence does not track state | BA-4 + BA-7 + BA-5 | Q4 (37 vs 3); `yu2026domainmotion` independently corroborates the confidence half |
| **6** | Block C: pocket 2×2 and ordinal recovery per receptor | BC-1 + BC-2 | Q2; BC-2 earned promotion by catching a mislabel |

**Everything else to SI**, which on current inventory is BA-8, GA-1 (graphical abstract, separate),
S1–S10, BB-4, BC-3, BC-4 and the five Block D panels — roughly 22 SI figures. That ratio is
`krishna2024rfaa`'s (5 main / 11 SI) taken further, and it is exactly what Aditya asked for:
build everything, keep the main sequence small.

### Where Block D goes — flagged, not decided

`paper-6f` reports Block D adds five candidate panels and that **Block D ships no row-level data**:
all three named corpora (42,180 predictions) are absent, five CSVs ship and all five are panel
metadata, and twelve of twelve claims are prose-only in whole or part.

**A prose-only claim should not carry a main-text figure.** On current evidence Block D belongs in
SI in full, and its MSA-depth ladder needs the `xing2025purified` sentence answered first — p.3,
*"the successful sampling of alternative states depends not on MSA depth but on sequence purity"* —
before any D3 panel is promoted. If depth *does* steer state here, that contradicts a published
claim and becomes a main-text result; if it does not, it is confirmatory and stays in SI.

### Dependencies — read before acting

**RESOLVED — all three landed 2026-09-10. See `VERIFICATION_SUMMARY.md` for the consolidated
result.** Blocks A, B and C returned 5, 8 and 5 BLOCKING findings respectively. **Every one is
claim-side; the data reproduced bit-exactly in all three.**

Effect on the sequence above: **Figures 1 and 2 are unaffected and can be built now. Figures 3-6
are on hold pending restatement** — Fig 3 because the ladder's headline term should become
`decoy -> cognate` (the one clean alpha5-CT contrast, +0.333 [+0.244, +0.435]); Fig 4 because the
family term is unsigned on 3 of 4 backbones and the per-backbone shares are misreported; Fig 5
because the pLDDT backbone split is an arm-pooling artifact; Fig 6 because "in the apo arm alone"
is false by a factor of two.

The allocation itself is **not withdrawn** — no result was found to be absent. Holding four panels
now is cheaper than redrawing them later, which is precisely why the dependency was written down
before any panel was made. Block D was deliberately excluded from re-verification because
`paper-6f` was mid-intake on it.

---

## Intro integrity check against the two new papers — performed 2026-09-10, PASSED

`xing2025purified` and `cheng2026af3cluster` were extracted today because they falsified a novelty
claim this project was *considering*. The question is whether they falsify anything already written.
They do not.

**The gap paragraph (`intro.tex` ~L371–378) survives unchanged.** It claims three things jointly:
the co-input reduced to the minimal contact that carries activation; its contribution separated
from mere occupancy by graded decoy and sequence-scrambled controls; and the state called by a
predicate fixed in advance rather than by proximity to a structure that must already exist.

- `xing2025purified` supplies no protein partner at all, scores by RMSD to deposited references,
  and runs no decoy or scrambled arm. It touches none of the three.
- `cheng2026af3cluster` recovers alternative conformations against apo/holo targets — it needs the
  answer, and it names no state in advance. It touches none of the three.

No sentence in `intro.tex` asserts anything about MSA subsampling crossed with a ligand, so nothing
needs retracting. Grepped for negative-existence claims across the whole file; the four that exist
(L71, L94, L233, L339) are all about pre-assembly, ligand poses, ConforNets' supervision and
`ku2026promise`'s evaluation sets, and none is affected.

**But there is a conditional debt.** The intro's survey of alignment manipulation (~L147–156)
currently stops at AF2-lineage work plus `kalakoti2026afsample3`. **If Block D3's MSA-depth ladder
enters the paper, that paragraph needs two additions before Results can cite it:**

1. `xing2025purified` p.3 — *"the successful sampling of alternative states depends not on MSA depth
   but on sequence purity"* — which D3 either contradicts or confirms, and either way must be met.
2. `cheng2026af3cluster` — MSA clustering carried to AF3 with a binder co-input present.

I have deliberately **not** made those edits, because MSA handling is not currently part of this
paper's claim (templates off, MSA default and unvaried), and adding the survey material before the
D3 fork is decided would be scope creep. The debt is recorded here so it is not discovered late.
