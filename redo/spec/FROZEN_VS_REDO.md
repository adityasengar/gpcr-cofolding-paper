# FROZEN_VS_REDO.md — rating the two systems, with evidence

**Written 2026-09-12.** A rating is worthless without the thing it is based on, so
every line points at a finding. Where the frozen system is better, this says so —
and on the one dimension that matters most it is better by an enormous margin.

## The honest headline first

**The frozen system ran 124,470 predictions and produced four written blocks. The
redo has run zero.** Every advantage claimed below is an advantage *on paper*, held
by a system that has never met real data. The frozen campaign's defects are the
defects of something that was actually built; ours are still hypothetical, and
hypothetical systems have a perfect record.

**That asymmetry should be read before anything else here.**

## Rating by dimension

| dimension | frozen | redo | verdict |
|---|---|---|---|
| **output vs input** | **nothing anywhere compares them** (F-9). A monomer returned where a dimer was asked for passed every check | `gates/run_receipt.py`: chain count, partner identity, seed, partner MSA depth — and **a missing column is a FAILURE, not a skip** | **redo, decisively.** This is the single largest structural gap in the frozen system |
| **what a scored row records** | **no MSA metadata reaches any scored row** — not depth, source, pairing or hash (F-6) | 47-column recording spec; but the subsampling review found it **about half** of what is needed, and `pocket_ca_rmsd_active/inactive` is **absent** | **redo, but not yet sufficient** — and we know that only because we checked |
| **checks proved by planting** | a handful of guards, none proved | 4 gates, **every check proved by planting the defect it catches** — and on 2026-09-12 that claim was found **false for a day** (G0's harness was dead after the layout migration) | **redo, with a caveat that proves the point**: the discipline only works if you run the self-tests |
| **statistical unit** | **four different units across ~24 implementations**, most calling the receptor a "cluster"; the pre-registration says seed and contains the word "cluster" zero times | declared: the **paralog cluster**, n=29, with the power model published per k | **redo** |
| **threshold provenance** | derivation not shipped, fit rows identified by no file | rule now known (F-17) and reproduced to within 1–1.5%; **the fit set is still unknown** | **draw** — we understand it now, we still cannot rebuild it |
| **scope discipline** | Class A thresholds re-used on B and F, which their own docstring calls **saturation** | Class A only, on measured grounds, guarded by `G0-13` | **redo** — but see below, they had diagnosed this first |
| **panel construction** | 48 receptors; the "40/40 match" is a coincidence of two forties | 64 in 32 clusters, one frozen freeze file, tiers as filter columns | **redo** |
| **ligand curation** | decoys **hand-picked FDA drugs in a Python dict**; one gate that can reject; a ±20% property window that **cannot**; Tier-3 decoys never RDKit-canonicalised | tiered on **chain-ness**, 10 gate checks all proved, CCD verified against RCSB, one pick **refused** for a name/CCD conflict | **redo** |
| **MSA handling** | three backbones fetch **live** from an unpinnable API; Chai does not pair; a run went **silently single-sequence** while reporting `ok=true` | `MSA_SPEC.md` — which **they found a defect in** | **draw, and we owe them** |
| **having actually run** | **124,470 predictions, four blocks, a written paper** | **zero** | **frozen, overwhelmingly** |

## Where the frozen system is better than its reputation here

This matters, because a project that only records the other side's mistakes is
building a case rather than an understanding.

1. **Their pre-registration anticipated two things we "discovered".**
   `PREREG.md:183` already reduced Class F to **SMO only** on transducer-taxonomy
   grounds, and `:277` already excluded FZD4 because its transducer is Dishevelled,
   not a Gα. We reached the first from apo measurements and flagged the second as a
   *gap*. **They were there first, in writing, before the data.**
2. **Their threshold script diagnoses its own failure.** Its docstring names the
   Class B/F re-use as saturation, quantifies it, and carries a gate demoting any
   metric below 3/4 derivation-set accuracy to descriptive-only, with the reason:
   *"reporting saturated 4/4/4/4 numbers dressed as unanimous is the anti-pattern
   this exists to prevent."* That is better self-criticism than most published
   methods sections contain.
3. **`gate_ligand_ccd_match.py` exists because they measured their own error rate**
   at 40–46% on name-sourced SMILES and acted on it. We rebuilt that gate; we did
   not invent it.
4. **`refs_build.py` has a silent-NaN tripwire** that raises rather than writing a
   NaN. That is the same instinct as our "a missing column is a FAILURE".
5. **They caught and guarded the Chai single-sequence bug before we ever saw it.**

## The fair summary

**The frozen system's failures are almost all failures of *recording and
verification*, not of *thinking*.** The people who built it knew about saturation,
about circular labels, about ligand-curation error rates, and wrote those down. What
it lacked was the machinery to stop a defect reaching a number: no output-vs-input
check, no MSA metadata on a scored row, no proved guards, and a statistical unit
that drifted between implementations and the pre-registration.

**The redo is, so far, exactly that missing machinery** — and nothing else. It has
better instruments, a defensible scope, a declared unit, and gates that have caught
**eleven** of my own errors in two days. It has produced no science whatsoever.

**Rating, stated plainly.** As a *measurement system*: the redo is substantially
better, and the gap is widest precisely where the frozen campaign's own findings say
it hurt. As a *scientific contribution*: the frozen campaign is four blocks ahead
and the redo is a specification. **The redo earns its keep only if it runs.**

## What that implies for sequencing

The registry (`inputs/run_registry.tsv`) says **9 of 45 experiments are enumerated,
1 dropped, 1 parked, 4 blocked on the measurement pass, and 30 need triage**. The
risk this comparison exposes is not that the redo is badly designed — it is that it
stays a design. Group 1 is fully specified and gated; that is one group of ten.
