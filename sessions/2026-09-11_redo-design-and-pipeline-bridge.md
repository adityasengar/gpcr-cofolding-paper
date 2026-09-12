# 2026-09-11 (afternoon) — the redo is designed, and we opened a live channel to the pipeline

> **Paths in this log are as they were when it was written.** Later the same day
> the campaign moved to a top-level `redo/`: `analysis/REDO_EXPERIMENT_CATALOGUE.md`
> is now `redo/spec/CATALOGUE.md`, the seven specs are `redo/spec/`, the
> generators `redo/build/`, the gates `redo/gates/`, the generated artefacts
> `redo/inputs/`, and `af3_received/` is `redo/protocol/received/`.
> See `redo/README.md`.

Orchestrator session. No block landed. Two things happened that change how this
project works: **Aditya froze the existing manuscript as a record and committed to
redoing the campaign**, and we built an encrypted bridge to `paper_af3` — the party
that actually ran every simulation — and started extracting their protocol.

## What happened

**The manuscript is FROZEN AS THE RECORD.** Not a fallback, not a draft to fix. The
four blocks stand as what was done; the redo supersedes them. Consequence: findings
about the current paper stop being defects to correct and become input to the redo.

**A redo programme now exists on disk.** `analysis/REDO_EXPERIMENT_CATALOGUE.md`
(1,806 lines, 33 experiments in 9 groups) plus seven specs under `analysis/redo/`:
`PANEL.md`, `SEQUENCES.md`, `SEQ_RECEPTORS.md`, `COUPLING.md`, `GROUP0_SYSTEMS.md`,
`GROUP1_SYSTEMS.md`, `RUN_MATRIX.md`, `BLUEPRINT_REQUEST.md` — 97 files including
generators, verifiers and two preflight gates.

**Group 0 and Group 1 are FROZEN**, each with a gate that fails loudly:
- `g0_preflight.py` — 11 blocking checks pass, 9 dependencies outstanding
- `g1_preflight.py` — 16 blocking checks pass, 7 dependencies outstanding
- **every check in both was proved by planting a defect**

**An encrypted bridge to `paper_af3` is live and has delivered 28 files**, every hash
verified first time, zero resends. See "The bridge" below — it is session-local and
must be re-armed.

## Decisions Aditya made, with their reasons

- **Freeze the manuscript as the record.** Stops us correcting a paper that will be
  superseded; converts five open decisions into three closed ones.
- **Relaxed 64-receptor panel, strict as a filter column.** Deciding later is then a
  one-line filter on a file that already exists. Strict costs 3 Class A receptors,
  not the ~18 I first estimated — my figure conflated database growth with the cap.
- **Read the cognate Gα off the structure the receptor was solved with.** Chosen so
  the supplied peptide and the scoring reference are the same molecule.
- **Group 0 may be flexible, Group 1 must be strict.** "Group 0 is just us playing
  with a measure." This is the governing principle for both freezes and it is the
  reason the chimeras were excluded from the primary panel.
- **NPxxY hydroxyl-vs-Cα deferred** — does not block, resolve when calibration runs.
- **Ask `paper_af3` for their protocol, framed as reproduction not audit.** That
  framing is why the exchange has been as open as it has.

## Decisions I made on his instruction to "GO and wrap this up"

- **Chimeras excluded from the primary panel**, carried in an extension tier with
  the deposited-tip arm as a matched control. Rungs R1–R4 *are* the α5 C-terminus and
  on those ten the reference carries an engineered tip 8 of 21 residues from canonical.
- **Cognate becomes two columns** — `cognate_family` (biology, what we supply) and
  `reference_tip` (structure, what we score against). We had been conflating them.
- **AA2AR overridden back into the primary panel.** It lost the adenosine cluster by
  **0.14 Å** and is the only receptor with wet-lab data on our exact 21-mer.

## The bridge — READ THIS BEFORE RESUMING

`~/.ntfy-bridge/` — encrypted channel to `paper_af3` over public ntfy.sh.
`send.sh` / `sendfile.sh` / `recv.sh` / `sweep.sh`, key and topic in that directory,
setup for the other machine in `BEDROCK_SETUP.txt`.

**IT IS SESSION-LOCAL. Both Monitors die when the session ends.** A resumed session
with the key on disk and no watcher looks exactly like a working bridge and is not.
Re-arm with two persistent Monitors: `~/.ntfy-bridge/recv.sh` (live) and
`~/.ntfy-bridge/sweep.sh` (5-minute reconciliation, silent unless something is wrong).

Limits, all measured: **text 4 KB** (over it, ntfy silently converts to an attachment
which decrypts on a different path), **attachment 15 MB**, **attachment expiry ~3 h**,
message retention 12 h. `send.sh` auto-splits at 2,200 chars.

Received files are in `~/.ntfy-bridge/inbox/` (28) and the three cross-check files are
copied into the repo at `analysis/redo/af3_received/` with their verified hashes.

## What the pipeline exchange established

**Nothing that mattered drifted between campaigns.** Both predicate axes byte-identical
between the Blocks A/B and C/D scorers. Pocket arithmetic byte-identical. MSA
configuration unchanged — every launcher diff is status-JSON capture. Input
construction unchanged. Three risks we had been carrying, all closed by measurement.

**Structural facts now stated by the party that ran it:**
- **No three-chain path exists in any backbone templater.** The heterotrimer was never
  run. `_partner_fasta` returns a whole catalogue entry verbatim and cannot truncate.
- **No arm ever supplied a peptide.** Every cognate arm is receptor + one complete Gα.
  This is the factual basis of the entire redo and was previously our inference.

**Three defects we could not have found ourselves:**
- `rows.pocket.csv` stamps `fd87133`, a commit whose tree has no pocket module. The
  pocket code was **new at `ea9efe5`**, not refactored out of `axes.py` — I inferred a
  refactor from the re-export comments and was wrong. Cross-block comparison is
  nonetheless safe: the core pocket functions are byte-identical `ea9efe5`→`d9c646af`.
- **Three of four backbones pair their MSAs; Chai does not.** Apo is a monomer and
  cognate is two chains, so for Boltz/OF3/Protenix the apo→cognate transition changes
  the partner *and* the alignment regime, and for Chai only the partner. Chai reads as
  the "soft predictor" throughout Blocks A/B — part of that may be the harness.
- **ColabFold's public API is an unpinnable live dependency.** The traced row fetched
  its MSA live; that alignment cannot be regenerated, only re-requested.

**And one they found, fixed and guarded before we saw it:** Chai ran silently
single-sequence while `_chai_status.json` reported `ok=true`. It appears in our tree in
exactly one place — a Block C narrative aside — and in no claim sheet.

## What I got wrong and corrected

- **"256 of 319 cells unanimous across seeds"** — that is the SAMPLE-grain count.
  Seed grain is **300 of 319**; only 19 cells (6.0%) disagree seed-to-seed. The error
  originated in `HANDOVER.md`, which is mine, and propagated into the catalogue.
- **I inferred a refactor from `axes.py`'s re-export comments.** There was none; the
  pocket code was new. "Lives in the sibling module" meant *is*, not *moved*.
- **I recommended GPCRdb activation degree = 100% as an independent criterion.** It
  MEANS "transducer-bound" — circular for a paper testing whether a transducer drives
  the active state. lit retracted it; the Group 0 agent had already implemented it and
  now has a check that prevents it returning.
- **I reported "4 of 5 cognate predictions failed."** Biased sample — I tested only
  the receptors already flagged as likely reversals. True rate is **31 of 35 agreeing**,
  and all four remaining "disagreements" appear in `paper_af3`'s own *secondary*
  coupling column. Two sources answering different questions, not a conflict.
- **I said the mutation cap costs ~18 Class A receptors.** It costs **3**; I had
  attributed database growth to the filter.
- **I misattributed the chain-A agent's work** (ICL3 audit, mutation recount, cap
  analysis) to the sequences agent. Attribution is a claim about who verified what.
- **I sent `paper_af3` a broken chunker**, then fixed mine and never sent the fix.
  They hit the same fork bomb. Recursion: each part got a prefix that pushed it back
  over the split threshold.
- **I over-costed the chimera exclusion** at 1.069×; with backfill it is **1.050×**,
  three clusters not four.

## What the next session should not redo

- **Do not reinstate GPCRdb activation degree as a calibration criterion.** `g0_preflight.py`
  check G0-6 exists to catch it. The *inactive* pole (2×46–6×37 ≤ 11.9 Å class A) is
  genuine geometry and may be used — **but it is our tilt axis**, so only NPxxY-vs-inactive
  is a clean comparison. Carry the circularity per axis, not per pole.
- **Do not re-derive the cognate map from scratch.** `coupling_cognate_map.tsv` is frozen:
  47 from structure, 6 by convention, 1 with caveat, 10 chimeras that stop deliberately.
- **Do not treat the 64→30 reduction as receptors being discarded.** All 64 are in
  `g1_systems.csv`; the primary arms run on cluster representatives and `G2` replicates
  across the rest. The statistical unit is clusters.
- **Do not ask `paper_af3` to run anything without Aditya's word.** Everything to date
  has been "send us X". The MSA-depth pre-flight would be the first compute ask and
  cannot be done locally — no MSA tooling on this machine.
