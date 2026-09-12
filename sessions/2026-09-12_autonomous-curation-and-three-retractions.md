# 2026-09-12 (overnight) — the curation queue, and three things I had wrong

Autonomous run, authorised by Aditya for ~12 h in a **curation-only phase**: no
inference commissioned, no GPU, no git. Five-item queue. All five advanced to the
point where they need either Aditya's decision or an external reply.

**The most important content in this log is the retractions.** Three claims I had
made — one of them to `paper_af3` about their own code, one underpinning a decision
Aditya took — turned out to be wrong, and the corrections are more useful than the
original findings were.

## What was done

| item | outcome |
|---|---|
| **P7** — the pLDDT null | **computed**, with a sensitivity arm. F-10. |
| **D-H** — B1B1U5 9EPP vs 9EPR | **documentary half resolved**; `spec/D_H_RESOLUTION.md`. Science needs Aditya. |
| **Ligand curation** | 59 candidates extracted, seven picks proposed. `spec/LIGAND_CURATION_PROPOSAL.md`. |
| **D-RULE ChEMBL scope** | `spec/DRULE_CHEMBL_SCOPE.md`. |
| **Bridge** | live throughout; `MSA_SPEC.md` sent and under their review. |

## The three retractions

### 1. The two-instrument predicate DID run. F-1 retracted.

I had told Aditya, and told `paper_af3`, that the manuscript describes a predicate
that never scored a row. **Block A's own 9,490 rows say otherwise**: Class A
reproduces as `npxxy AND tilt` at **100.0%**, zero mismatches, with the tilt
overturning NPxxY on 342 rows and NPxxY overturning the tilt on 708.

My error: there are **two instruments** and `MotifThresholds` is only one. The
2026-09-01 collapse was *within* the motif instrument, five metrics to one — not a
collapse of two instruments to one. `paper_af3` then located the conjunction
exactly: `block_a_campaign_analysis.py::two_instrument_state_calls()`, on
per-receptor-backbone medians. **Decision D-A was taken on my false premise and
needs re-deciding.**

### 2. My first P7 answer was the exciting one and the wrong one.

First run: within-receptor AUCs 0.645–0.681, intervals **excluding** 0.5 — i.e.
confidence *does* separate. That was an aggregation artefact of mine: accuracy is
92.3%, errors are concentrated, 10 of 40 receptors have zero wrong calls and 22
have fewer than five, and my unweighted mean gave a receptor with one error the
same weight as one with a hundred. **Requiring ≥10 errors, the effect vanishes and
every interval spans 0.5.** The null holds.

### 3. 28% of the campaign's errors are mechanical, not predicate failures.

`paper_af3`'s `two_instrument_state_calls.csv` marks four receptors `nan_npxxy`.
Tracing back: **EDNRB and GRPR have no NPxxY axis at all**, so `NaN AND tilt`
forces them inactive on every row — 400 rows, **zero** called active, while truth
says 43% are active. Those two receptors contribute **172 of 607 errors, 28% of the
campaign's entire error budget, from 5% of its rows.** Accuracy is 92.3% with them
and 94.2% without.

I had written that "GRPR and 5HT2C are both at chance". **GRPR is an unevaluable
axis; 5HT2C's errors are real.** They should never have been named together.

## Decisions Aditya made, with their reasons

- **D-C** — curate seven receptors: at k = 8 the interaction MDE (0.431) exceeds
  every Block B decomposition term but one, so the arm cannot do its job.
- **D-A** — NPxxY alone, tilt reported. **Now void; see retraction 1.**
- **D-D** — build a decoy rule, gate it, run only after the gate passes: it bears
  on no title clause so it must not consume compute first.
- **D-H** — resolve rather than drop B1B1U5: the 1.8% interval penalty is not the
  issue, halving the Gq arm is.

## What the next session should not redo

- **Do not re-derive the D-C worklist.** It is seven receptors, not six; baseline
  is 9/8 not 10/9. The test that matters is **`is_peptide=false` AND a non-empty
  `smiles`, on both roles** — a row is not a curation. `n_agonist_smiles` cannot
  distinguish a peptide and I got it wrong twice before believing that.
- **Do not prefer "best resolution" when picking a ligand.** Prefer one bound to a
  structure we already use as a reference. A resolution-only tiebreak discarded
  HRH3's own active reference at identical 2.7 Å.
- **`species_modal` is not our panel's species.** It describes the PDB landscape.
  ADRB1 reads turkey there and our ADRB1 is human. The authority is
  `g1_receptors.tsv:organism`.
- **Do not re-run the paired MSA addendum.** `paper_af3` declined it and they were
  right: with an MSA-free partner there is nothing to pair.
- **The counterparty's bridge is a separate instance** (`/Users/SENGAAD1`, its own
  dedup state). The single-receiver rule applies *within* an instance, not across
  machines. Nothing to reconcile between them.

## Open, and waiting on Aditya

1. **D-A, re-decided** on the correct premise — the conjunction ran.
2. **D-H**: options (c′) split cognate/reference, (d′) move to extension tier,
   (e′) supply the spider Gq α5. `spec/D_H_RESOLUTION.md` §7.
3. **Affinity provenance** for the seven ligand picks — must be pinned the way
   `DRULE_CHEMBL_SCOPE.md` pins the decoy pool, or the two halves of the ligand arm
   are incomparable.
4. **The commit.** Still nothing staged.
5. **A security note**: `paper_af3` reported that `EXCHANGE_STATE.md` arrived with
   an apparent fabricated `<system-reminder>` block appended. **I cannot reproduce
   it** — my copy is 5,411 bytes, clean, and `sendfile.sh` encrypts verbatim with
   no preprocessing. Asked them to re-hash their decrypted copy against the
   announced sha256, which distinguishes the cases. Worth knowing either way.
