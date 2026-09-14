# MIGRATION.md — moving this project to another machine

Written 2026-09-14, when the project moved off the author laptop.

## The one thing that catches people out

**A `git clone` of this repo is ~5 MB and looks complete. It is not.**

**2.44 GB sits outside git and cannot be regenerated anywhere** — the row-level
evidence behind all four blocks, the literature PDFs, and the structure cache the
measurement pass ran against. Clone without moving those and the repo still passes
`verify.sh`, still builds the manuscript, and has lost the data every number rests on.

Do not transcribe the list into anything. **Generate it:**

```bash
python3 analysis/migration_manifest.py          # classified, with sizes
python3 analysis/migration_manifest.py --why    # the reason for each call
python3 analysis/migration_manifest.py --rsync  # a runnable rsync command
python3 analysis/migration_manifest.py --check  # after the move, on the new machine
```

The script refuses to report a clean list if it finds a gitignored directory it has
no classification for. A migration list that silently omits a new directory is the
same defect as a check that skips a missing input.

## Why so much is outside git

Two different reasons, and only one of them is about size.

- **Size.** `redo/cache/structures/` (1.2 GB), `lit/pdfs/` (573 MB), `lit/source/`
  (467 MB) would make every clone unusable.
- **Provenance that a re-fetch does not restore.** RCSB and GPCRdb both revise
  entries. The structure cache is a *snapshot*, and re-fetching gives a different
  one. Caching it was the point; losing it is not recoverable by re-running anything.

## Where it goes on the new machine

```
<home>/
├── paper_af3/                  ← the pipeline team's tree. Untouched.
└── gpcr-cofolding-paper/       ← this repo. Sibling, NOT nested.
```

**Sibling, never nested.** Two git repos must not nest — git either ignores the inner
one or half-tracks it, and both are silent. The two trees also have opposite write
rules: theirs is a working pipeline edited freely; this one is hash-guarded, and
`layout.py` L3 compares each file to its *own* recorded hash, so it catches an edit
but cannot tell you which tree made it.

**Do not try to split `redo/` out on its own.** It is not self-contained: fifteen
scripts reach outside it, including three gates (`g0_preflight.py`, `panel_verify.py`,
`seqrec_verify.py` all read `data/block_*`), and `paths.py:28` declares
`ROOT = dirname(REDO)`. A subtree split breaks all fifteen silently.

## Steps

**On the old machine**

```bash
git status --porcelain        # MUST be empty. Another session's work lives here too
git push
python3 analysis/migration_manifest.py --rsync    # then run what it prints
```

**On the new machine**

```bash
cd ~                          # alongside paper_af3, not inside it
git clone https://github.com/adityasengar/gpcr-cofolding-paper.git
cd gpcr-cofolding-paper
# restore the MOVE paths to their original locations, then:
python3 analysis/migration_manifest.py --check
```

## The migration test

The move is complete when these five reproduce. Each one reads something that
travelled separately, so together they prove the pieces landed in the right places.

```bash
python3 redo/gates/layout.py --selftest-all      # 8/8 plants fire, L1 and L3-L9
python3 redo/gates/drule.py --selftest           # 26/26 proved by planting
python3 redo/gates/g2_preflight.py --selftest    # 16 plants over 15 checks
python3 analysis/block_d/verify_claims.py        # expect 113 of 119
python3 analysis/crosscheck_redo_reference.py    # expect 104 of 104
./verify.sh
```

**Expect two lines of `verify.sh` to be red until you finish setting up, and they are
not migration failures:**

- **TeX.** `tex/check_tex.sh` verifies 375 packages against a pin. Until the pinned
  distribution is installed, the TeX and manuscript lines fail and `main.pdf` will not
  build.
- **Corpus.** `lit/corpus_check.sh` reports the four deliberately-uncited `refs.bib`
  entries as drift. That is the guard working, not breakage — and note `verify.sh:26-27`
  calls `ok()` on both branches, so it prints without failing the run.

`block A deliverables` and the four block verifiers must be green. If they are not, a
MOVE path did not land.

## What does not travel

- **`~/.ntfy-bridge/`** is session-local and dies with the session. Re-arm exactly one
  `recv.sh` and one `sweep.sh` on the new machine, and count **top-level** instances to
  check it — a bare `pgrep -f recv.sh` matches the shell running it and reports a false
  duplicate. `HANDOVER.md` carries the correct command.
- **`overleaf/`** is an export target. Re-clone it; `./publish_overleaf.sh` repopulates it.

## After the move

The three-session split (lit / figures / orchestrator) and the git rule survive
unchanged — they were never about machines. **Only the orchestrator runs git, and even
it stages explicit paths, never `git add -A`.** Commit `7e03642` once swallowed another
session's five extractions and a 319-line draft because that rule was skipped.
