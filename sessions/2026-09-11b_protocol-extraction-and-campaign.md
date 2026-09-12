# 2026-09-11 (evening) — the protocol was extracted, and the campaign changed because of it

Orchestrator session, continuing from the afternoon. No block landed. Three things
happened: **the redo moved to a top-level `redo/` with a guarded layout**, **`paper_af3`
sent their entire source tree and we read it**, and **a measurement they ran tonight
changed our experimental design rather than confirming it**.

## What happened

**`redo/` is now a top-level campaign directory**, a peer of `manuscript/` and `lit/`.
Eight entries, fixed; `spec/ build/ gates/ inputs/ cache/ runs/ protocol/` plus
`README.md` and `paths.py`. The move was proved lossless — 98 files byte-identical —
and both preflight gates reproduced their baselines exactly. `analysis/redo/` and
`analysis/REDO_EXPERIMENT_CATALOGUE.md` no longer exist. **Blocks A–D untouched.**

**`redo/gates/layout.py`** — seven checks, each proved by planting the defect it
catches. L3 rehashes all 47 generated inputs against `inputs/MANIFEST.tsv`, so a
hand-edit is detectable. Wired into `verify.sh`, and that wiring was proved too.

**`paper_af3` delivered their whole tree** — 407 entries — plus the GPCRdb cache,
a dispatch manifest and the three missing status JSONs. Everything hash-verified.

**We read ~75,000 lines of it.** Six documents in `redo/protocol/`, 5,376 lines,
every claim carrying file:line.

**Nine findings became design requirements** in `redo/spec/DECISIONS.md`, and
`redo/spec/CAMPAIGN.md` (1,302 lines) re-plans the campaign against them.

## Decisions Aditya made, with their reasons

- **`redo/` at top level, new work only.** It is a peer of the manuscript, not a
  fifth block; retrofitting A–D would touch 302 verifier checks on frozen work for
  no gain.
- **The manuscript stays frozen even though it describes a predicate that never ran.**
  The paper is the record of what was done. The findings go where they can still
  change something — the redo.
- **Green light on the MSA-depth pre-flight**, the first compute ever asked of the
  pipeline side.
- **Send the frozen input set**, including the row-format proposal, so shape is
  agreed before anything runs.

## What the protocol extraction established

- **The predicate is single-metric NPxxY-OH < 9.08**, `K_OF_N=1`. The two-instrument
  class-conditional rule our manuscript describes **never scored a row** — the
  collapse preceded the Block A dispatch tag. `PREREG.md` §2a was never amended and
  still asserts the unused rule.
- **The state call is not independent of confidence.** Rows below pLDDT 50 are
  called inactive before geometry is read. `paper_af3`: "a real circularity."
- **P7, the pre-registered null that pLDDT does not separate, was never computed.**
  It is a title clause, and it is free on Block A's existing 9,490 rows.
- **Block C's cognate arm supplies a blanket `alphas` to 35 of 40 receptors** — the
  failure Block A's own code names and avoids. Asked; unanswered.
- **A decoy is a hand-picked FDA-approved drug**, one per receptor. The only enforced
  gate is Tanimoto < 0.30; the ±20% property window is computed and ignored, and all
  8 Tier-1 decoys miss it.
- **The bootstrap is labelled cluster and implemented over receptors** (once over
  rows). The seed-collapse code has zero callers.
- **Nothing compares output to input** anywhere in the pipeline.

## The measurement that changed the design

`paper_af3` ran the α5-CT MSA-depth pre-flight: **112 rows, 16 Gα families × 7 rungs.**

**`ct11` returns depth 0 across 16 of 16 families.** `ct15` is family-dependent — 0
for Gq/G11/G14/G15/G12, 2–459 for the rest. `ct21`+ has homologs.

So **at a single rung the alignment regime varies by Gα family.** Neither side
predicted that. The MSA-free partner is now mandatory rather than one option of four,
and the per-chain harness change is on the critical path. **Decision D-B is closed by
measurement, not by choice.**

## What I got wrong and corrected

- **I said `ANCHOR_KEYS` was 6.** It is 20. My grep matched the `CANONICAL_ANCHOR_KEYS`
  line above it; the subagent was right and I nearly overruled it.
- **I told Aditya 9.082 was our drift**, accepting `paper_af3`'s word. Their own
  `thresholds_panel.csv` says 9.082; the code constant 9.08 is rounded. Withdrawn
  with them.
- **I counted 51 distinct receptor names in a FASTA where there are 48.** `|` is not
  whitespace, so my `\S+` took the whole header. Three receptors are duplicated.
- **I relayed "the manifest settles the peptide question."** It cannot — it is the
  deep-apo tier, `partner_type=apo` on all 140 rows.
- **I asked `paper_af3` to write up the MSA recipe and the reference rule** while
  `PREREG.md` and `refs_build.py` sat unread on our own disk. Withdrawn.
- **`CATALOGUE.md`'s header says "33 experiments in 9 groups"; the body holds ~46 in
  10.** Our own scope-in-the-header failure, in a document I supervised.
- **I left duplicate and orphaned bridge watchers running.** Every `recv.sh` shares
  one `.seen`; an orphan whose monitor was stopped still consumes and deduplicates
  messages while writing nowhere. Torn down and rebuilt as exactly one of each.

## What the next session should not redo

- **The bridge is session-local and dies with the session.** Re-arm exactly ONE
  `recv.sh` and ONE sweep. Check `pgrep` afterwards — more than one receiver chain
  means messages can be silently swallowed.
- **Attachments expire in ~3 hours; text lasts ~12.** `paper_af3` was told to hold
  files until we signal. **Signal first, then expect files.**
- **Do not re-read the bundle.** The six documents in `redo/protocol/` are the map.
- **Do not ask `paper_af3` for anything derivable from what they sent.** That is
  why the ask list is down to four.
- **Do not re-derive the panel, sequences, cognate map or either gate.** Frozen and
  unaffected by all nine findings.
