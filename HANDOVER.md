# HANDOVER.md — orchestrator session

Two prompts. The first compacts THIS session. The second starts a fresh one.
(`lit/HANDOVER.md` is the lit agent's, and predates the manuscript — ignore it here.)

---

## 1. Paste after `/compact`

```
Compact this conversation. It set up the orchestration and build machinery for a GPCR
co-folding manuscript. Keep the following; discard the rest.

KEEP — how work is organised:
- One laptop, two sessions. ORCHESTRATOR runs in paper/ and is the ONLY session that
  touches git. LIT AGENT runs in paper/lit/, owns lit/** and the words in
  manuscript/sections/*.tex, and never runs git.
- Split: what the paper SAYS -> lit agent. How the paper is BUILT -> orchestrator.
- Aditya is the message bus. He must say "the lit agent is done" before the
  orchestrator commits.
- NEVER `git add -A`: both sessions share one working tree, and a commit once swallowed
  another session's five extractions and a 319-line draft. Stage explicit paths.
- The lit/orchestrator split does NOT enforce the two-pass rule. The lit agent both owns
  the corpus and wrote the introduction; retrieval and drafting already share a session.
  The split earns its keep on context, not evidential integrity.

KEEP — state of the work:
- Repo github.com/adityasengar/gpcr-cofolding-paper (private). lit/pdfs, lit/source and
  rows_enriched_v3_7.csv are gitignored and live on this laptop only.
- manuscript/ is canonical LaTeX. ./manuscript/build.sh -> 16 pages, 63 citations,
  0 undefined. main.tex is the container (orchestrator); sections/*.tex are the words
  (author). Nature Communications submission format: double spaced, line numbers.
- draft/intro.md is SUPERSEDED by manuscript/sections/intro.tex.
- Corpus complete: 78 of 78 references extracted, nothing citable is unread. Four notes
  have no PDF (publisher bot-walls) and cite as [citekey] with a section name, not a
  page. Four notes still on schema v2.
- TeX Live 2026, 375 packages pinned in tex/tex-packages.txt. ./tex/check_tex.sh
  verifies. helvet/courier deliberately NOT loaded — BasicTeX lacks their font metrics.
- Overleaf demoted to an export target: ./publish_overleaf.sh. overleaf/ is gitignored.
- Scripts: verify.sh (full self-check), session_start.sh, session_end.sh,
  lit/corpus_check.sh, analysis/q.py, analysis/fingerprint.py, analysis/sync_bib.py,
  analysis/md2tex.py.

KEEP — findings that bear on the manuscript:
- chiesa2025templatebias NARROWS THE NOVELTY CLAIM. It supplies a G protein as co-input
  to a co-folding model AND measures receptor activation state, on 63 post-cutoff class A
  pairs. Nothing else in the corpus does both. Remaining distinctions: 21-mer peptide vs
  whole Galpha; operationalised predicate vs RMSD to the deposited answer; the decoy and
  shuffled arms; AF3-lineage backbones.
- tran2026nanogs: PDB 3SN6 and 6E67 disagree about which residue contacts R131(3.50)
  (Y391 vs E392) and the paper exploits rather than resolves it — any claim about which
  alpha5 contact matters inherits that. It also ran NO scrambled-sequence control and no
  Gi/Gq selectivity, so our decoy and shuffled arms are complementary, not redundant.
- bret2025boltz2docking was read from the HAL author version; its page numbers do NOT
  match published JCIM pagination. Convert before citing.
- STATUS.md holds CLAIMS; RESULTS.md records which reproduce. "48 receptors" reproduces
  under no definition; the activation ladder's middle rungs are off by 31 points. Never
  cite a number straight from STATUS.md.
- Blocks D1, D2, D3, T1.5 have NOT run.

KEEP — my own corrections:
- I had the machine roles inverted for most of the session.
- I claimed the session split enforced the two-pass rule; it does not.
- My sync_bib.py hid unread entries with "%%", which BibTeX ignores because it scans for
  "@" regardless — 12 unread papers were silently citable until the lit agent fixed it.

DISCARD: the two-laptop setup and its abandonment, TeX Live 2025->2026 version fights,
gitignore inline-comment bugs, the Overleaf clone migration, gh auth troubleshooting,
per-commit mechanics, and all tool debugging.
```

---

## 2. Paste into a fresh orchestrator session

Start it in `paper/`. `CLAUDE.md` loads automatically, so this is short.

```
Read CLAUDE.md, then run ./verify.sh and ./session_start.sh. Report what you see.

You are the ORCHESTRATOR for the GPCR alpha5-CT co-folding manuscript. You own the
machinery: manuscript/main.tex (container and house style), analysis/**, tex/**, the
scripts, and ALL git. The lit agent runs separately in paper/lit/, owns lit/** and the
words in manuscript/sections/*.tex, and never runs git — Aditya will tell you when it
has finished, and then you commit with EXPLICIT PATHS, never `git add -A`.

Next task: figures. figures/ is empty. The corpus has a data_shape grammar built for
exactly this — litquery's "design by analogy" matches on the SHAPE of data rather than
subject matter, and flags the `hides` field on near-matches. 24 of 78 papers carry
figure reuse restrictions (15 ND, which forbids redrawing, not just copying).

Do not draft manuscript prose in this session. Tell me what you have loaded, then wait.
```

---

## Notes

The restart prompt ends with "then wait" so a fresh session does not start answering
from general knowledge before reading `CLAUDE.md` and the ledgers.

Figures are the next piece of work. Nothing exists yet: `figures/` is empty, no plotting
code, and `RESULTS.md` is mostly `NOT-LOCALLY-CHECKABLE` because the real data is 1 TB+
elsewhere. Expect the first question to be which numbers can actually be plotted here.
