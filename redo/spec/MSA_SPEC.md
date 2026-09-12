# MSA_SPEC.md — the partner-chain alignment regime for the α5-CT ladder

**Audience: the `paper_af3` pipeline team, for review.** This is a specification to
argue with, not a change request. Nothing here should be implemented off a message;
it exists so that a review has something concrete in front of it.

**The requirement is the constancy of the alignment regime across the ladder. The
mechanism below is our proposal, not our condition.** If review lands on a
different route that delivers a constant regime, we will design to that instead.

---

## 1. What we are running, and why the alignment matters

The Group 1 ladder varies one thing: the length of the partner chain supplied
alongside the receptor. Eight rungs, from apo through 11, 15, 21, 26 and 36-residue
fragments of the Gα C-terminus, up to the complete Gα subunit at 350–394 residues.
The claim it tests is that supplying the α5 C-terminus drives the model into the
active state, and that the effect scales with how much of it you supply.

That reading requires length to be **the only thing changing along the ladder.**

## 2. It is not, today — and the measurement is yours

`paper_af3`'s pre-flight, 112 rows, 16 Gα families × 7 rungs, in
`protocol/received/rung_msa_depth.csv` (sha256 `bb45b4b1…`):

| rung | length | unpaired ColabFold depth |
|---|---:|---|
| `R1_ct11` | 11 | **0 in 16 of 16 families** |
| `R2_ct15` | 15 | **0 in 5 families; ≤42 in 10 more; Gs = 459** |
| `R3_ct21` | 21 | 47–582 |
| `R4_a5helix` | 26 | 186–1,995 |
| `R5_a5plus` | 36 | 2,273–3,043 |
| `R6a_da5` / `R7_full` | 368 / 394 | 8,474–9,203 |

*(Filter on `note == "ok"`: three timed-out rows carry `unpaired_depth = -1` as a
sentinel, not a depth.)*

Three of four backbones pair their MSAs; Chai does not. So under an MSA-on design
the partner's alignment regime is a function of **both rung and Gα family**:

- `ct11` runs single-sequence by force, everywhere.
- `ct15` runs single-sequence for fifteen families and **aligned for Gs alone** —
  and Gs is the most common cognate partner on any GPCR panel, including ours.
- `ct21` and above run aligned, with depth climbing two orders of magnitude.

**A monotone trend along that ladder is what a pairing artefact looks like.** We
cannot distinguish "more α5 drives more activation" from "more α5 retrieves more
homologs" — and at `ct15`, a Gs-specific effect could not be told from chemistry.

This is the confound the redo exists to remove, so we would rather remove it than
model it.

## 3. What we propose

**The partner chain receives an explicit query-only alignment — depth 1, the
partner sequence and nothing else — at every rung R1…R7, on all four backbones.
The receptor chain keeps its normal full alignment throughout.**

The per-chain route already exists and is reported feasible:

| backbone | field | status |
|---|---|---|
| OpenFold-3 | `chains[*].main_msa_file_paths` / `paired_msa_file_paths` | per-chain today |
| Protenix | `proteinChain.unpairedMsaPath` / `pairedMsaPath` | per-chain today |
| Boltz-2 | `sequences[*].protein.msa` (inline YAML) | per-chain today |
| Chai-1 | `--msa-directory`, keyed by sequence sha256 | **the one gap** |

Needed: a caller building a per-chain mapping rather than passing a plain string.
Chai needs the intended `.pqt` written directly rather than resolved by hash
against the shared cache.

> ### THE TWO BACKBONES ARE NOT KEYED THE SAME WAY — found by `paper_af3` in review
>
> This is the one place this document was actively dangerous, and it was inside the
> mechanism this section recommends. Verified against source:
>
> | backbone | line | key |
> |---|---|---|
> | OpenFold-3 | `propose.py:462` | `msa_a3m_path.get(cid)`, `cid = chain["chain_ids"][0]` — **chain ID** |
> | Protenix | `propose.py:595` | `msa_a3m_path.get(protein_idx)`, a 0-based counter — **integer position** |
>
> So a caller passing `{"A": receptor_a3m, "B": ""}` works on OF3 and **fails
> silently on Protenix**: `.get("A")` against a dict keyed `{0:…, 1:…}` returns
> `None`, hits `if not path: continue`, sets **no MSA at all**, and Protenix then
> falls through to its launcher default — **a live server fetch, full depth on both
> chains**, with nothing in any status JSON.
>
> **That is precisely the failure mode §4 argues against, reached through the
> mechanism §3 proposes.** Whoever implements this must key Protenix by position or
> normalise the two. **And §6's first check — assert observed partner depth == 1 —
> is what catches it, which is the argument for §6 being non-optional.**

**The PAIRED slot must be specified, not inherited.** This document previously said
what the partner gets in the main/unpaired slot and nothing about the paired one.
Since `:471-472` (OF3) and `:599-600` (Protenix) both assign **one path to both
slots**, a query-only file would land in the paired slot by default. For a depth-1
file that is *probably* inert — there is nothing to pair — but **"probably inert" is
the same epistemic footing §4 rejects for omission.** OF3 additionally carries a
query-level `use_paired_msas` flag, and leaving it true against a depth-1 paired
file is a third unmeasured behaviour.

**Required: state the partner's paired-slot content explicitly** — an empty list,
or the same query-only file, declared either way — rather than inheriting whatever
`:471-472` does.

## 4. Why query-only rather than absent

`paper_af3` offered both. They are not equivalent and the difference is a silent
failure mode.

**Omission depends on four backbones' fallback behaviour when a chain has no
alignment file, and none of those behaviours has been measured.** The bad case is
specific: a backbone that quietly generates its own alignment for a chain it finds
no file for would deliver **full depth exactly where we intended zero** — the
inverse of the design — with nothing in any status JSON to show it. That is the
same shape as the Chai single-sequence bug `paper_af3` found and fixed: a path that
does something reasonable and reports nothing.

A query-only alignment is better on three counts:

1. **Constant by construction.** Depth 1 at every rung, every family. The regime
   cannot vary because there is nothing left to vary.
2. **One operation, not four fallbacks.** Identical on Boltz, OF3, Protenix and Chai.
3. **Verifiable after the fact.** Depth 1 is a number that can be read off the
   artefact. An absence is only an absence.

**CLOSED by `paper_af3` from source, no test needed.** chai-lab 0.6.1,
`data/dataset/msas/load.py:47-58`: `get_msa_contexts_for_seq` builds
`msa_directory/expected_basename(seq)`, and `if not path.is_file()` returns
`MSAContext.create_single_seq()`. **No fetch, no generation.** Chai reaches its
fetch branch only when `use_msa_server` *and* `msa_directory` are both truthy
(`chai1.py:339`, `:368`), and their launcher never passes `--use-msa-server`.

**So for Chai, absent and query-only are behaviourally identical — both depth 1.**
The explicit `.pqt` buys **verifiability, not different behaviour**: it converts
"depth 1 because we understand the fallback" into "depth 1 because here is the
artefact and its hash". Worth keeping for that alone. Two caveats `paper_af3`
raised and we keep: that fallback path **has never fired in a real campaign** —
their launcher pre-checks every chain's `.pqt` and refuses to launch without it, so
it is dormant code, not production-tested; and omission stops being safe the moment
`--use-msa-server` is added, where an explicit depth-1 file would still be honoured.

## 5. What must be recorded

**The partner chain's OBSERVED alignment depth on every row — not its intended
depth.** Read back from what the backbone actually consumed, alongside the
receptor's depth and the pairing state.

We ask because of what the existing campaign cannot do: **no MSA metadata reaches
any scored row at all**, across all 42,180 predictions. A grep of every row-touching
scorer module for `msa|a3m|pqt` returns nothing. That is precisely why the `ct11`
cliff had to be established from a side report rather than from the rows.

With observed depth on each row, *"the alignment regime was constant along the
ladder"* is **demonstrable from the delivered data**. Without it, it is an
assertion about a harness — and this week the harness has three times turned out to
be doing something undocumented.

Our `g1_recording_spec.tsv` (sha256 `ef1d8233…`, already sent) carries columns for
this. **If they do not map onto what you can emit, change ours, not yours** — tell
us the column names you produce and we will adopt them.

## 6. How we would verify it

Following this project's rule that every check is proved by planting the defect it
catches:

1. **Constancy** — assert `partner_msa_depth == 1` on every ladder row. Prove by
   planting a row with the partner's real alignment; the check must fail.
2. **Receptor unaffected** — assert receptor depth is unchanged between a ladder row
   and the matched apo row for the same receptor. Prove by planting a subsampled
   receptor MSA.
3. **Output matches input** — assert the returned chain count and the returned
   partner sequence match what was requested. This closes the class `paper_af3`
   confirmed nothing currently checks: a monomer returned where a dimer was asked
   for passes every existing check.

## 7. What we are NOT asking for

- Not a change to anything already delivered. The manuscript is **frozen as the
  record**; Blocks A–D stand as what was done.
- Not a fix to the one-file-in-both-MSA-slots defect as a precondition. It should
  be fixed — and it is **TWO sites, not one**: `propose.py:471-472` for OF3 and
  `:599-600` for Protenix, identical shape. It will fire on the first two-chain depth run
  — but with no partner alignment there is nothing to pair, so it is **not on our
  critical path**.
- Not an answer today. Nothing on our side is blocked by the review taking its time.

## 8. Alternatives we would accept

| alternative | our view |
|---|---|
| Any mechanism giving a constant partner-alignment regime | **Equally good.** The requirement is constancy. |
| Query-only on three backbones, Chai excluded | **This row was a FALSE CHOICE and is withdrawn.** Chai gets the constant depth-1 regime for free either way (§4), so skipping the explicit `.pqt` there trades away *verifiability*, not the falsification test. Do not weaken the design on the belief that it does. |
| MSA-on with observed depth recorded per row | **Rejected** — depth is near-collinear with the factor. This is the confounded design. |
| MSA-on and MSA-free at two rungs, as a residual arm | **Wanted anyway**, on top of the primary. It answers "how much did we change by doing that?", which is the first question a referee asks. |
