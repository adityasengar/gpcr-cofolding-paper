# CLAIMS.md — the argument, and what each claim needs

The paper's spine. **This file is durable**: the argument does not change when the
HPC export is refreshed. Only the evidence status of the numeric claims does.

Each claim carries the evidence it needs, in two currencies:
`[citekey p.N]` for prior work (verify via `litquery`) and `[R-*]` for our numbers
(verify via `dataquery` against `RESULTS.md`).

**Gate:** a claim is draftable when every evidence slot is filled *and* no slot depends
on a `STATUS.md` planned block. `needs:` lines that are still open are the work.

---

## The setup — why the question exists

**C1. Conformational state is the thing that matters for GPCRs, and a single predicted
structure cannot express it.**
- evidence: `[georgiou2025heterogeneity]` for the multistate/rheostat picture; `[paajanen2026activation]` for apo/agonist bimodality across deposited structures
- status: **ready** — lit only, no numbers needed

**C2. Current co-folding models collapse onto one basin, and their own authors say so.**
- evidence: `[abramson2024af3 p6]` — "multiple random seeds ... do not produce an approximation of the solution ensemble", and "AF3 exclusively predicts the closed state for both holo and apo systems". Corroborated by `[ku2026promise]`, `[ye2026multistatebias]`, `[sun2026kinconfbench]`
- status: **ready** — strongest citation in the corpus

## The gap — what nobody has done

**C3. The multi-state benchmarks that exist exclude GPCR activation by construction.**
- evidence: `[ku2026promise p9]` names "GPCR TM6 displacement" as excluded in its own Limitations; the TM-score 0.8 admission rule in `[bryant2024cfold]` and inherited by `[kalakoti2026afsample3]` has the same effect without naming it
- status: **ready**

**C4. Where directional state control exists, the state is supplied by the operator,
not induced by a biological co-input.**
- evidence: `[heo2022multistate]` state-annotated templates + MSA deletion; `[yang2025statespecific]` operator declares the state and the peptide is the designed *output*; `[ferguson2026deorphann]` pinned active templates; `[lee2026confornets]` transfer label is itself a deposited structure
- status: **ready** — this is the sentence that protects our novelty

**C5. The largest GPCR + G-protein co-folding studies supply the partner and never
verify receptor state.**
- evidence: `[matic2023gpcrome]` 825 ligand-free models, no activation criterion; `[miglionico2026atlas]` whole GPCRome, "no state criterion"; `[pandyszekeres2024gproteindb]` 5,595 released complexes, no state assigned
- status: **ready** — derived mechanically from the INDEX metric column

## The result — what we claim

**C6. An α5-CT peptide co-input drives the active state.**
- needs: `[R-B-LADDER]` at full n, plus a defined denominator (`[R-A-RECEPTORS]`)
- status: **blocked on data** — ordering reproduces, rungs do not

**C7. The agonist alone does not.**
- needs: `[R-B-LADDER]` ligand arm vs cognate arm
- lit support: `[hilger2020gcgr]` — "TM6 activation is only triggered by the engagement of the α5 helix of Gαs" (class B, GCGR)
- **must engage:** `[vo2026fiducials p8]` shows a high-efficacy agonist alone drives β2AR TM6 "almost complete outward movement", with the Gs α5 helix adding "less than 1 Å further outward at most positions". This is the strongest counter to C7 in the corpus and the draft must meet it head-on, not omit it. Note their state calls are visual, with no quantitative panel.
- status: **blocked on data + needs an argued position on vo2026fiducials**

**C8. Model confidence does not track conformational correctness.**
- needs: `[R-INFRA-AA2AR]` on a **partner-matched** subset — the current cross-backbone comparison is confounded by unequal partner mixes
- lit support: `[bryant2024cfold]` plDDT cannot select conformations; `[schafer2025confounds]`; `[junker2026peptidedesign]` PAE over-estimates for misplaced GPCR peptides
- status: **blocked on data** — one clause currently contradicted locally

**C9. The effect decomposes into occupancy, α5-CT sequence, and correct family.**
- needs: `[R-B-DECOMPOSITION]` — requires decoy and shuffled arms at full n
- status: **blocked on data**

## Threats a reviewer will raise — plan the response now

| threat | source | current position |
|---|---|---|
| the isolated peptide does **not** stabilise the active state without agonist | `[tran2026nanogs p8]` wet-lab, verbatim | ours is a *prediction-model* input, not a solution-phase equilibrium. State this explicitly; do not let it read as contradiction. |
| agonist alone nearly suffices at β2AR | `[vo2026fiducials p8]` | see C7 |
| partner-induced changes are predicted **worse** than ligand-induced | `[ku2026promise]` (their term is "protein-induced") | our result runs against this; engage it rather than omitting it |
| co-folding wins only near training distribution | `[skrinjar2026generalization]`, `[roehrig2026docking]` | needs our anti-memorization arm — Block C claims it survives; verify when data lands |
| sequence-identity splits do not stop leakage | `[mattsson2026leakage]` | directly exposes our generalisation framing |

---

## Refresh procedure — when new data lands

1. `python3 analysis/fingerprint.py --check` — confirms the data moved.
2. Re-run every query: `python3 analysis/q.py scope ladder receptor_counts aa2ar coverage`.
3. Update the verdict block in `RESULTS.md`; **do not edit this file** unless the
   *argument* changed.
4. `python3 analysis/fingerprint.py --stamp`.
5. Re-check every `blocked on data` claim above and flip the ones that clear.
