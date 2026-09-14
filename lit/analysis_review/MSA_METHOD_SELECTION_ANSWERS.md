# Choosing a subsampling regime — multiple methods or staged selection?

lit-3d, 2026-09-12, for paper-6f. Retrieval only. Corpus 83/83/87, staleness clean.

**The short version, because it bears on your provisional view: the corpus supports it.
Every paper that selected its subsampling hyperparameter against deposited structures is
recorded in this corpus as route-4 oracle leakage, and the one published rebuttal in the area
attacks exactly that class of practice. And no subsampling family of any kind has a positive
claim on GPCRs — the one direct attempt failed.**

---

## 1. DBSCAN specifically

### `waymentsteele2024cluster` — the origin paper

- **What is clustered:** sequences of an unmodified ColabFold/MMseqs2 UniRef MSA, **by edit
  distance**. Verbatim p3: *"We therefore clustered the MSA by edit distance using DBSCAN35, and
  ran AF2 predictions using these clusters as the input."* Pipeline definition: *"we refer to
  this entire pipeline as AF-Cluster—generating a MSA with ColabFold, clustering MSA sequences
  with DBSCAN and running AF2 predictions for each cluster."*
- **Pre-filter:** sequences with more than 25% gaps removed before clustering (p3).
- **Hyperparameters:** **epsilon swept 3–20 in steps of 0.5** with an "epsmax" rule
  (Methods p9; ED2A-B p14). For the 628-family screen the sweep ran *"on a randomly selected 25%
  of the MSA to accelerate computation"* (p9). **`min_samples` / the DBSCAN *k* is NEVER
  REPORTED** — the parameter is described at p9 and no value appears anywhere in the paper.
  *(Note the figure defect recorded for ED2A-B: the x-axis is drawn only to ~9 although the
  sweep ran to 20, so the large-epsilon regime the text argues about is not visible.)*
- **Predictions per target:** KaiB — **230 clustered** models, against **500 each** for uniform
  |MSA| = 10 and |MSA| = 100 (p14, ED Fig).
- **Systems:** KaiB, RfaH, MAD2, plus a 628-family screen and 10 Mpt53 homologues.
- **GPCRs: NO, explicitly.** Note: *"**No membrane proteins, GPCRs, kinases or transporters are
  studied** (transporters appear only as prior work)."* Also: *"no curated state database (no
  GPCRdb/KLIFS analogue)."*

### `bryant2024cfold`

- **What is clustered:** MSA sequences; training sequences clustered at **30% identity** with
  MMseqs2 (*"a more stringent cutoff than the 40% identity used in AlphaFold2"*), and a
  **90%-identity re-clustering** used as a control *"To see if these are truly alternative
  conformations and not a result of sequence variations."*
- **Predictions per target:** **104** = *"13 samples × 8 cluster sizes [16, 32, 64, 128, 256,
  512, 1024, 5120]"*.
- **GPCRs: NO, and the note answers it explicitly** — *"**No GPCR, and no 7TM or membrane
  receptor of any kind, is named anywhere in the main text, any figure, any figure caption, or
  the Methods.**"* Two structural reasons make presence very unlikely rather than merely
  unattested, one of which matters to us: the chain filter *"discards the
  G-protein/arrestin/nanobody partners that define an active-state GPCR entry."* What cannot be
  settled: the 244/155 target list is not printed in the 12-page PDF.

### `cheng2026af3cluster` — **do not quote its body**

`v3.2-abstract-only`; the PDF is not held. Its DBSCAN description in the note is marked
`[SUBAGENT — UNVERIFIED]`. Its only GPCR-relevant line is the note's own judgement: *"this is
not a GPCR paper, its ligands are sugars rather than…"*. **No hyperparameters, no per-target
counts are available.**

**So: none of the three clustering papers touches a GPCR, and two say so explicitly.**

## 2. Head-to-head across families — yes, and broader than you have

**`suzuki2026conforflux` is the broadest and the most useful to you.** **Nine baselines
actually run**, spanning four perturbation families plus two other intervention levels, and —
critically — **at matched budget on the identical MSA**: *"Eight further matched baselines at
**500 samples on the identical MSA** (CF-random, AFsample3, AF-cluster, Boltz-sample,
ConforMix-RMSD-Boltz-1, ConforMix-RMSD-Boltz-2, BioEmu) | that any inference-time intervention
at any pipeline level would do as well"* (p5, p16–p17). Family depths/rates: **CF-random
{2,4,8,16,32,64,128}**; AFsample3 column masking; AF-cluster DBSCAN *"following the original
implementation [Wayment-Steele et al.]"*. **This is the matched-budget four-family comparison
you were looking for.**

**`kalakoti2026afsample3`** is the largest by target count: AFsample3 vs **AF2vanilla,
AF3vanilla, MSA subsampling and AFsample2** across **238 two-state Cfold targets**.

**`richman2025conformix`** implements **AFCluster, AFsample2, CF-random and default Boltz at
1,000 samples** inside one codebase (p6, Table 1).

**`suzuki2026pairscaling`** runs MSA-subsampling, MSA random masking and AF-Cluster-inspired
clustering as baselines on a **fixed, shared AF3-server MSA used for every method** (p9) —
the cleanest MSA-controlled design of the four.

So `schafer2025confounds` and `ye2026multistatebias` are **not** the only comparisons; there
are at least four broader ones, three of them matched-budget.

## 3. Cost per target, by family

| family | runs/samples to make its claim | source |
|---|---|---|
| **plain random shallow (CF-random)** | **1–2 runs** per ensemble — KaiB 2, Mad2 1, RfaH 2 | `schafer2025confounds` p4 Fig 2b, p5 |
| **AF-Cluster (DBSCAN)** | **95–329 runs** — KaiB 329, Mad2 95, RfaH 250 | same |
| AF-Cluster, origin paper | **230** clustered models (KaiB) | `waymentsteele2024cluster` p14 |
| uniform depth (origin paper's own comparator) | **500 each** at \|MSA\|=10 and \|MSA\|=100 | same |
| **MSA clustering (Cfold)** | **104**/target = 13 × 8 cluster sizes | `bryant2024cfold` |
| **column masking (AFsample2)** | **1,000** models *per masking level*; the OC23 sweep is 23 × 10 × 1,000 = **230,000** | `kalakoti2025afsample2` |
| **targeted masking (AFsample2T)** | **250 per level**, pooled 0/10/20/30% → 1,000, plus 1,000 default = **2,000/receptor** | `mitjavila2026afsample2t` |
| matched-budget comparison | **500 samples** per baseline | `suzuki2026conforflux` |
| Boltz-internal comparison | **1,000 samples** per comparator | `richman2025conformix` |
| `ye2026multistatebias` per-strategy | **NOT REPORTED** (only SecA's 4 clusters of 4–5 sequences) | — |

**The ratio you asked for: roughly 50–300× between plain random shallow and AF-Cluster for
reaching the same result.** One caveat that matters, and `schafer2025confounds` handles it
honestly: the 1–2 figure is runs needed to *succeed*, not ensemble size. For the false-positive
comparison they matched sizes — *"Matched ensemble sizes, **CF-random 330 vs AF-cluster 329** for
KaiB | Rules out that the false-positive difference is an artifact of unequal numbers of
predictions"* (p4). **So at equal n the cheap method still matches or beats the expensive one.**
Also recorded: the cost figure is drawn on a linear axis that renders the CF-random bars as
invisible stubs.

## 4. Does anyone tune on a subset then apply to the rest? — **Yes, and the corpus flags it as leakage every time**

**This is the crux, and it supports your reading.**

**The closest thing to Aditya's proposal, and it is hyperparameter transfer across sets:**
`kalakoti2026afsample3`, p4 — *"The 20% for AFsample2 **agrees with what was previously reported
to be the optimal for a smaller set of 23 proteins (OC23)** for AFsample2."* So the AF2 level
was fixed on an earlier, smaller benchmark and carried over. **But its own AF3 level was not
transferred — it was tuned in place:** the note records *"the masking fraction and k are tuned on
the **same 238-target set the results are reported on** (p4, p9), there is **no post-cutoff or
memorization control at all** (p10)."* Recorded as route 4, plus routes 5 and 6.

**Every other selection in this area is recorded as oracle leakage:**

- `kalakoti2025afsample2` — *"The masking fraction was chosen by scoring the sweep against the
  deposited open/closed structures **of the OC23 evaluation targets themselves**"*; and the
  confidence-screening threshold *"is likewise tuned against a reference-defined optimum"*.
  Summary: *"the masking fraction and sampling budget are tuned on the evaluation set (route 4),
  and success is TM to the held references (routes 5–6)."*
- `mitjavila2026afsample2t` — *"the masking level and the 0–30% ensemble composition were fixed
  by maximising accuracy against the deposited structures of the **same 10 evaluation targets**"*
  → routes 4 and 5.

**And there is a published criticism of exactly this class of practice.**
`schafer2025confounds` p1: *"However, their Paper **lacks some essential controls** needed to
assess AF-cluster's reliability."* Its concrete complaint about method-comparison hygiene, p2:
*"This would seem to be an inappropriate control because the AF-cluster predictions of RfaH were
generated using AF25. **Controls should be performed with the same software.**"*

**Two counter-examples show the escape route, and it is a structure-free criterion:**

- `waymentsteele2024cluster` claims it: *"**The clustering hyperparameter is tuned on the
  sequences, not on the answer**"*, and *"We selected DBSCAN to perform clustering because we
  found that it offered an automated route to optimizing clustering **a priori**"*. **But the
  note records Route 5 as CONTESTED-BY-CONSTRUCTION and keeps both halves**, because the epsilon
  sweep was evaluated by plotting the resulting landscapes in RMSD-to-both-known-states
  coordinates. So the claim is made and is disputed within our own extraction.
- `suzuki2026pairscaling` demonstrates it cleanly: its clustering baseline's *"own hyperparameter
  is chosen on a **structure-free criterion** — 'We varied eps from …'"*, on a fixed shared MSA
  used for every method.

**So the answer to "is staged method selection normal or a recognised confound?" is: it is
normal, and it is a recognised confound, and both are documented. The distinction that decides
which one you are doing is whether the selection criterion references the deposited answer.**

## 5. Has method choice changed a conclusion? — yes, by system class

**`richman2025conformix` reports different families winning on different categories**:
*"Coverage, worst-matched, **domain motion** — best MSA baseline (**CF-random**)"* versus
*"Coverage, worst-matched, **fold switching** — best baseline (**AFCluster**)"* (p6, Table 1).
So which family looks strongest depends on the system class being tested.

**`kalakoti2026afsample3` reports a near-even per-target split** for combining families:
*"Improvement : deterioration, AFsample3+subsampling vs AFsample3 | **36:49** (subsampled arm
better for 36, worse for 49)"* (p10, Fig S1 p12) — with the text conceding *"employing
subsampling along with MSA masking was the optimal strategy for a sizable number of targets."*

**`kalakoti2025afsample2` reports it at the level of individual targets**: *"20% masking
generates the best model for P40131, while **5% masking is optimal for P71147**"* (p3).

**Beyond the AF-Cluster dispute I found no case of two families giving opposite answers on the
same system with a state call.** The three above are "different family wins", not "opposite
conclusion". **That specific case: absent from corpus.**

## 6. Which family is most dangerous to us? — **on GPCRs, none, and that is the finding**

**General proteins.** The strongest claim by scale is **MSA column masking**:
`kalakoti2026afsample3` — random column masking at AF3 inference, **40% optimal**, *"yields
better alternate-state models and markedly more diverse ensembles than AF2vanilla, AF3vanilla,
MSA subsampling and AFsample2 across **238 two-state** Cfold targets"*, with *"no retraining and
essentially no compute overhead"*. The strongest claim **per unit cost** is **plain random
shallow MSA (CF-random)**, which `schafer2025confounds` shows matches or beats AF-Cluster at
1–2 runs against 95–329, and at matched n = 330 vs 329.

**AF-Cluster has the loudest origin claim** — both states of KaiB, RfaH and MAD2 with high
plDDT *"where the full MSA and uniform subsampling do not"* — **but it is the one family with a
published rebuttal against it**, and the rebuttal reports it *"mistakes some single-folding KaiB
homologs for fold switchers."*

**On GPCRs specifically: no family has any positive claim, and the corpus is unambiguous.**

- None of the three clustering papers studies a GPCR (§1) — two say so explicitly.
- `mitjavila2026afsample2t` masks GPCR MSAs but its own note records that the masking generates
  *"**local side-chain and backbone heterogeneity in the pocket**, not alternative global
  states"*, and that the method is directable *"in site, not in state"* — state comes only from
  including or omitting Gα/Gβ/Gγ.
- `vo2026fiducials` subsampled only in a benchmark sweep and its receptor states are
  `NOT APPLICABLE`.
- **The one direct attempt failed.** `ye2026multistatebias` ran AF-Cluster + U10 + U100 on β2AR
  with a state readout and reports *"MSA-level manipulation alone, whether through evolutionary
  clustering or random subsampling, is largely insufficient to overcome the systematic
  conformational bias."*

**So the honest answer is the one you said would be more useful: on GPCRs no subsampling family
has a strong claim, the strongest-in-general families have never been tested on a GPCR state
readout, and the only family that has been so tested failed.** If you want the most dangerous
attack, it is not a published result — it would be **column masking at AF3's 40% optimum
(`kalakoti2026afsample3`) applied to GPCRs, which nobody has done**. That is the gap a referee
could point at, and running it yourselves is the way to close it.

---

## Negatives, for direct use

1. **No clustering paper (AF-Cluster, Cfold, AF3-Cluster) studies a GPCR or any 7TM protein.**
2. **No case in the corpus of two subsampling families giving opposite state conclusions on the
   same system**, beyond the AF-Cluster dispute itself.
3. **`ye2026multistatebias` does not report samples per subsampling strategy.**
4. **`waymentsteele2024cluster` never reports the DBSCAN `min_samples`/*k* value.**
5. **No subsampling family has a published positive claim on GPCR conformational state.**
