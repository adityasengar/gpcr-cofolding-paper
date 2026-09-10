---
name: wrap-session
description: Close down a working session on this manuscript cleanly. Use when the user says wrap up, wrap session, I'm stopping, let's compact, end of session, or asks for a compact prompt and a resume prompt. Runs housekeeping first — checks for work in flight, verifies the build, refreshes HANDOVER.md and SESSIONS.md — and only then emits the two prompts. Do not emit prompts without doing the housekeeping.
---

# wrap-session

Two prompts at the end, but **housekeeping first**. A compact prompt written
over an unverified tree preserves a description of a state that does not exist.

## Step 1 — is anything in flight?

```bash
git status --porcelain
```

**Uncommitted files under `lit/` or `manuscript/sections/intro.tex` belong to the
lit session. Do not commit them.** Ask, or leave them. Commit `7e03642` once
swallowed another session's five extractions and a 319-line draft because this
check was skipped.

Check for running subagents. If any are still working, **say so and stop** —
wrapping mid-agent loses their output. Either wait, or record in `HANDOVER.md`
exactly what is running and what it was asked for.

## Step 2 — verify

```bash
./verify.sh                                       # all green?
./manuscript/build.sh                             # pages, bibitems, 0 undefined?
python3 analysis/block_<x>/verify_claims.py       # mismatches are EXPECTED; count them
./analysis/block_<x>/check_deliverables.sh        # 7/7?
```

A red build at wrap time is fine **if it is understood** — three undefined
citations because the lit session cited papers it has not extracted yet is the
guard working. A red build nobody has diagnosed is not.

## Step 3 — hunt stale references

Deleted files still named in briefs send the next session to nothing:

```bash
grep -rl "<name of anything deleted this session>" \
  --exclude-dir=.git --exclude-dir=data . | grep -v "^./lit/notes/"
```

Fix the machinery and the briefs. `lit/notes/` hits are usually other papers'
filenames — check before editing.

## Step 4 — refresh the two durable files

**`SESSIONS.md`** — append what changed and *why*, and what the next session
should not redo. Git records what; this records why.

**`HANDOVER.md`** — rewrite, do not append. It must answer, in this order:
where the project is; the decisions waiting on Aditya; how the sessions divide;
what to do when the next block arrives; what was learnt the hard way; and where
the state lives. If a decision was resolved this session, remove it. If a new
one opened, add it at the top.

## Step 5 — emit the two prompts

### The compact prompt

Tell it what to KEEP and what to DISCARD, explicitly. For this project the
categories are stable:

**Keep** — the three-session split and the git rule; the state of the manuscript,
the corpus and the current block; every discrepancy that bears on a sentence;
**every correction the assistant made to its own earlier claims**; decisions
Aditya made and their reasons; what is in flight.

**Discard** — tool and environment debugging, LaTeX escaping fights, version
churn, per-commit mechanics, path fixing, and any exploration that was abandoned.
On this project that is most of the volume and none of the value.

The corrections category is the one that matters most and the one most easily
lost. A summary that drops them hands the next session the first answer instead
of the corrected one. Name them individually.

### The resume prompt

Keep it **short**: `CLAUDE.md` auto-loads and carries the detail. It needs only:
read `CLAUDE.md` then `HANDOVER.md`, run `./verify.sh` and `./session_start.sh`,
who this session is and what it owns, the one next task, and **"then wait"** —
so a fresh session does not start answering from general knowledge before
reading the ledgers.

## What this project's wrap always has to capture

- **Discrepancies are the asset.** Block A carries 22 groups; five would have put
  something false or unsupported in the paper. Never compact them away.
- **Decisions with their reasons**, not just their outcomes — e.g. Block A is
  groundwork and Block B carries the titular peptide claim.
- **Anything the assistant got wrong and corrected.** There is always something.
- **Which agent is mid-task**, and the exact brief it was given.
