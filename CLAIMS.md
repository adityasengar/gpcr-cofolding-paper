# CLAIMS.md — the argument spine

**DURABLE.** Survives a data refresh; a block landing changes which claims have
evidence, never what the claims are.

Each claim carries a `needs:` line naming the block that must supply its
evidence. A claim with an open `needs:` is not yet writable, however good it
sounds. Numbers are verified by `analysis/block_<x>/verify_claims.py`, never
quoted from a claim sheet.

## Which block defends which claim

| claim | evidence from | status |
|---|---|---|
| C1–C5 | the literature corpus alone | **ready** — written into the intro |
| C6 (peptide drives active) | **not Block A — see below** | **no evidence yet** |
| C7 (agonist alone does not) | needs a ligand-only arm | **no evidence yet** |
| C8 (confidence ≠ correctness) | **Block A** | **written** — 2 of 4 backbones at anchor grain |
| C9 (decomposition) | needs decoy / shuffled / mutant arms | **no evidence yet** |
| *(new)* whole-Gα co-input drives active state, at panel scale | **Block A** | **written** |

## ⚠ The title claims something Block A does not test

The manuscript title is *"A Gα α5 C-terminal **peptide** co-input drives GPCR
co-folding models into the active state"*, and the introduction is built around
that claim. **Block A's cognate arm supplies the whole Gα subunit**, not a
21-mer: `d_ga_alpha5_r350_ca` and `plddt_ga_alpha5` score the α5 as a *feature
of the supplied subunit*, and the hero figure states in-frame that "the full
cognate Gα was supplied, only its α5 C-terminal 21 residues are drawn".

So Block A is **scale, instrument and controls for whole-partner co-input** —
which is how its Results section is written, and it is honest as written. But
the paper currently promises a peptide result in its title and intro and
delivers a whole-subunit result in its Results.

**This needs a decision before submission**, and it is Aditya's:

1. a later block supplies the 21-mer arm and carries the titular claim, with
   Block A as its groundwork; or
2. the title and intro are rewritten around whole-Gα co-input.

Until it is resolved, no Block A sentence should imply the peptide claim. None
currently does — checked 2026-09-10.

---

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
- **QUALIFIED 2026-09-09 and no longer true as written.** `[chiesa2025templatebias]` supplies the G protein as a co-input to AlphaFold-Multimer on 63 post-cutoff class A pairs and measures the receptor's activation state, finding that the partner beats operator-supplied active templates on TM5/TM6/TM7 (p6302, p6305). The claim must be narrowed to the four distinctions that survive: (i) whole Gα or heterotrimer, not a 21-residue α5-CT peptide, so the α5 contact is never isolated; (ii) state scored by RMSD to the deposited active reference of that same complex, not by a predicate applicable to an unsolved receptor; (iii) no decoy or scrambled-partner arm, so occupancy and identity are not separated; (iv) AF2/AFM only, no AF3-lineage backbone (they say so, p6299).
- status: **needs rewriting** — the old sentence would be caught immediately by these authors

**C5. The largest GPCR + G-protein co-folding studies supply the partner and never
verify receptor state.**
- evidence: `[matic2023gpcrome]` 825 ligand-free models, no activation criterion; `[miglionico2026atlas]` whole GPCRome, "no state criterion"; `[pandyszekeres2024gproteindb]` 5,595 released complexes, no state assigned
- **QUALIFIED 2026-09-09.** The word that has to carry the claim is now **largest**. `[chiesa2025templatebias]` supplies the partner *and* verifies state, at 63 pairs — two orders of magnitude smaller than the resources above, but it is a genuine exception and the sentence must name it rather than imply none exists.
- status: **ready with the qualification above**

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
| **a ligand known NOT to bind reproduces the conformational change** | `[yu2026domainmotion, Significance/Discussion]` — 82 enzymes, 500 AF3 models per condition, no templates | **the sharpest published challenge to our decoy arm.** They show the training-set prior (40.3 pp between apo- and holo-dominated enzymes) is 3–4× the ligand effect (9.1–17.5 pp), and that ligand pLDDT is "generally not sufficient for discriminating between binder and nonbinder ligands". Our decoy and shuffled arms are exactly the control they call for, so this is answerable — but the answer must be quantitative and must cite them by name. Added 2026-09-09. |
| co-folding wins only near training distribution | `[skrinjar2026generalization]`, `[roehrig2026docking]` | needs our anti-memorization arm — Block C claims it survives; verify when data lands |
| sequence-identity splits do not stop leakage | `[mattsson2026leakage]` | directly exposes our generalisation framing |
| **Boltz-2's output can be insensitive to target shuffling and to binding-site mutations that abolish binding** | `[bret2025boltz2docking]` — 943 screening hits, 10 mostly-GPCR targets | adjacent to our **shuffled arm** on one of our four backbones. Different quantity (affinity head, not geometry) and different shuffle direction, so not a refutation — but the response must be that we read receptor geometry, not an internal score. Sits with `[masters2025physics]`. Added 2026-09-09. |

---

## Refresh procedure — when new data lands

1. `python3 analysis/fingerprint.py --check` — confirms the data moved.
2. Re-run every query: `python3 analysis/q.py scope ladder receptor_counts aa2ar coverage`.
3. Update the verdict block in `RESULTS.md`; **do not edit this file** unless the
   *argument* changed.
4. `python3 analysis/fingerprint.py --stamp`.
5. Re-check every `blocked on data` claim above and flip the ones that clear.
