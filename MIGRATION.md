# MIGRATION.md — moving this project to another machine

Written 2026-09-14, when the project moved off the author laptop.

## Transport: git carries everything that matters (revised 2026-09-14)

**The 161 MB that cannot be re-obtained is now IN the repo.** So on a corporate
laptop, where USB is usually DLP-blocked and a drive is a request rather than a
plan, the whole migration is:

```bash
git clone https://github.com/adityasengar/gpcr-cofolding-paper.git
cd gpcr-cofolding-paper
gunzip -k analysis/block_c/received_2026_09_12/rows.tier3.v2.csv.gz
python3 analysis/migration_manifest.py --verify-assets      # expect OK, 87 assets
```

**Verify the assets.** A clone that silently dropped or truncated a file looks
exactly like a clone that worked, and these are the files behind four blocks.
`MIGRATION_ASSETS.sha256` pins all 87.

**Why `rows.tier3.v2.csv` travels gzipped:** 87.7 MB is under GitHub's 100 MB hard
block but over its 50 MB warning, and it would sit in every future clone. Gzipped
with `-n` (no name, no mtime) it is 21.8 MB and its digest is stable -- the same
reasoning `layout.py` already applies to `drule_rejections.tsv.gz`.

### What did NOT come through git, and what that costs

2.44 GB was outside git. Only 161 MB of it was irreplaceable. The rest:

| | size | where it comes from |
|---|---:|---|
| `analysis/block_d/received_2026_09_13/` | 89 MB | **tracked on paper_af3's own `origin/main` at `10d6493`** -- clone it there once read access lands |
| `redo/cache/structures/` | 1.2 GB | re-fetchable from RCSB |
| `lit/pdfs/`, `lit/source/` | 1.04 GB | re-downloadable from the publishers |
| `figures/out/`, the built PDFs, the pdftotext caches | 177 MB | regenerate from scripts the clone carries |

**Re-fetching costs provenance, not evidence.** RCSB and GPCRdb revise entries, so a
re-fetch is a *different snapshot*. But the measurement pass is done and
`g0_measurements.csv` is committed, so nothing that has landed is invalidated --
only future re-measurement (X5's placebo axes, or adding a receptor class) would run
against newer coordinates. Likewise all 87 corpus extractions are in git; only the
source PDFs are gone, so a page-numbered quote cannot be re-verified without
re-downloading the paper.

**If you want the full 2.44 GB anyway** (an external drive, a corporate file share,
or the HPC as a staging point), the old route still works:
`python3 analysis/migration_manifest.py --rsync`, dry-run it first.

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

**On the old machine** — already done as of 2026-09-14, kept for the next time.

```bash
git status --porcelain        # MUST be empty. Another session's work lives here too
git push
```

**On the new machine**

```bash
cd ~                          # alongside paper_af3, not inside it
git clone https://github.com/adityasengar/gpcr-cofolding-paper.git
cd gpcr-cofolding-paper
gunzip -k analysis/block_c/received_2026_09_12/rows.tier3.v2.csv.gz
python3 analysis/migration_manifest.py --verify-assets
```

`--verify-assets` is the one that matters: it re-hashes all 87 carried files against
`MIGRATION_ASSETS.sha256`. `--check` is the older drive-based check and only applies
if you also rsync'd the 2.25 GB.

## The migration test

The move is complete when these five reproduce. Each one reads something that
travelled separately, so together they prove the pieces landed in the right places.

```bash
python3 redo/gates/layout.py --selftest-all      # 8/8 plants fire, L1 and L3-L9
python3 redo/gates/drule.py --selftest           # 26/26 proved by planting (~3.5 min)
python3 redo/gates/run_receipt.py --selftest     # 13/13 plants over R1-R5
python3 redo/gates/g2_preflight.py --selftest    # 16 plants over 15 checks
python3 analysis/block_d/verify_claims.py        # expect 113 of 119
python3 analysis/crosscheck_redo_reference.py    # expect 121 of 121
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

`block A deliverables` and the four block verifiers must be green. If they are not, an
asset did not land — run `--verify-assets` first, it names the file.

**Block D's verifier will fail until you get its rows**, which did NOT come through
git: they are 89 MB on paper_af3's own `origin/main` at `10d6493`, pending read
access. That is expected, not a broken migration.

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
