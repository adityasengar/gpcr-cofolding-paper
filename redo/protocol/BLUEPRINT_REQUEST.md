# BLUEPRINT_REQUEST.md — the full operating blueprint for Blocks A → D3

**To:** the team that ran the campaigns (`paper_af3` / `paper_af3_release`, HPC +
MacBook).
**From:** the manuscript side.
**Drafted:** 2026-09-11. **Status: SENT 2026-09-11**, reviewed in full by the
orchestrator and released on Aditya's explicit instruction. Delivered over the
encrypted ntfy bridge as an attachment, with a covering message.

---

## Why we are asking

The campaign is being redone. The PI's framing, in his words: *"the stuff is highly
complicated now… in the new phase we want a very clean setup… get exact information on
the blueprint of all simulations we ran in this campaign: Block A → D3, and how each
system is trusted."*

So this is **not an audit**. It is a request to be able to **rebuild your pipeline from
a bare machine and reproduce your numbers**, so that the new campaign starts from a
setup we both understand rather than from a re-derivation. Where we quote something
from your drops below, it is because we could not work out what the artefact *means* —
not because we think it is wrong. Several of the sharpest things in this document are
things **you** found and wrote down first; that is why we are comfortable asking
openly.

What we want, concretely: **how to set it up, how to run it, how to analyse it, and
what would have caught it if any of that were wrong** — at the level of "how is a CSV
row built", "how is a residue number extracted", "how do you decide a ligand is in the
pocket", not at the level of a Methods paragraph.

**Please prefer sending the artefact over describing it.** A job script answers better
than a paragraph about a job script. Nearly every item below is phrased as "send us X"
for that reason. §13 is the consolidated file list if you would rather work from that.

---

## 0. Ground rules for answering — please read this section

### 0.1 Source every answer from the artefact, not from memory

This is the one request the PI asked to be put at the top rather than buried.

**Open the file and quote it. Give the path. Give a hash where you have one.** If the
artefact contradicts your memory of the design, **report the artefact and flag the
divergence** — that divergence is one of the most useful things you can send us.

The reason is specific and it is not about trust. A description of a pipeline written
from memory is fluent, plausible, and — on the page — completely indistinguishable from
a correct one. We have been bitten by exactly this from our own side repeatedly: our
first pass at a check is wrong more often than the drop is. We are not asking you to
prove anything; we are asking you to protect both of us from a confident paragraph that
nobody can tell is stale.

### 0.2 Mark every answer with how it was established

Please tag each answer:

| tag | meaning |
|---|---|
| **VERIFIED** | read out of the artefact just now; path (and ideally hash) given |
| **RECALLED** | from memory, not re-checked |
| **UNKNOWN** | not recorded anywhere, or no longer recoverable |

A clearly-labelled RECALLED answer is genuinely useful. An unlabelled one is a
liability, because we cannot tell it apart from a VERIFIED one and will have to
re-derive it anyway. **We would much rather have three VERIFIED sections than nine
unlabelled ones.**

UNKNOWN is a real and valuable answer. "The raw MSA was in per-job scratch and is gone"
is a finding; a plausible reconstruction of what it probably contained is not.

### 0.3 We will cross-check on receipt, and we will send back what we find

Not as a threat — because knowing an answer will be checked changes how carefully it is
given, and because when our cross-check disagrees with you we want the disagreement to
be interesting rather than embarrassing. We will check answers against the shipped
bundles (`data/block_a/`, `data/block_b/`, `data/block_c/`, `data/block_d/` on our
side), and we will send you the result either way, including the cases where we were
the ones who were wrong. Our house rule for that is already written down: *"Where their
number is right and our first reading was wrong, say so in the entry — it is the
cheapest way to be trusted on the rest."*

### 0.4 Answer incrementally

**Do not wait until you can answer all of it.** Each section is self-contained and each
item is individually numbered (`A1`, `E7`, `Q3`…). Send §E on its own if §C is going to
take a week. The three items in §1 are worth more to us finished than the whole document
half-done.

### 0.5 Negative knowledge is explicitly requested

What has gone wrong before and been fixed. What failed *silently* and was caught late.
What you do not trust in your own setup today. §11 asks for this directly.

We ask because your own records already do this unusually well and we would rather build
on that habit than work around it. Block D shipped **ten** withdrawal records
(`data/block_d/03_withdrawals/W-D-1…W-D-10`) naming claims that were tested and dropped;
`GATE_3_STEERING_VS_DEGRADATION.md` forced the withdrawal of the block's own headline F1;
`GATE_4_SCORER_DIFF.md` diagnosed a phantom SHA by running `git cat-file` and publishing
the null result; and `C-D-5_agtr1_active_nb_of3_30_short.md` openly argues with itself
inside its own parentheses about what the per-cell sampling multiplier actually was,
rather than papering over it. That is why we are asking plainly instead of carefully.

### 0.6 What we will send you in return

See §14. Short version: our verifier scripts, our recalibration method, and the
acceptance tests we intend to run on the new campaign's outputs — **before** you produce
them, so you can see exactly what your outputs will be checked against rather than being
measured against a standard you have not seen.

---

## 1. The three that matter most

If nothing else in this document gets answered, these three unblock the redo.

**① `scorer/` — the scoring module itself, at the two SHAs of record.**
`04243c45bdd2285ca195add098a7f333a0d60476` (Blocks A and B — verified constant on all
9,490 Block A rows and all 32,000 Block B rows) and
`d9c646af5f89861c16062bf256de96a8389d9915` (Blocks C and D). If you can send only two
files, send **`scorer/pocket_metrics.py`** and **`scorer/bw_numbering.py`** — between them
they define the pocket, the generic-number mapping, every distance and every RMSD. After
those: `scorer/axes.py`, `scorer/anchors.py`, `scorer/references.py`, `scorer/propose.py`,
`scorer/_version_sha.py`. Everything in §6 and most of §8 stops being a question the
moment we can read this code. **This is the single highest-value item in the document.** A
tarball of the module at each SHA is fine; we do not need repo access.

**② The four launchers plus the MSA plumbing, verbatim.**
`qsub/rerun_boltz.sh`, `qsub/rerun_chai.sh`, `qsub/rerun_of3.sh`,
`qsub/rerun_protenix.sh`, `qsub/colabfold_shim.py`, `scripts/queue_ops.py`,
`scripts/subsample_msa.py`, `scripts/clean_a3m.py`. These carry the inference
configuration, the template flags, the MSA routing and the per-row env plumbing — none
of which is recoverable from any drop. Four shell scripts answer §3 and §4 almost
completely.

**③ One worked example, end to end, for a single prediction.**
Pick any one row — we suggest `OPSD × boltz × apo` from D1, since it is the cell §12 Q2
is about. Then walk it: the manifest row that produced it → the exact input file handed
to the backbone (the actual bytes) → the command line and job submission → the output
path → the scoring call → the finished `rows.csv` line. **One traced example is worth
more than three sections of prose**, because it pins down every hand-off at once, and it
is the thing we will use to write the Methods.

---

## 2. Section A — environment, pinning, and "can you re-run 2026-09-06 today?"

- **A1.** How is the environment pinned, on each of the two machines (HPC and MacBook)?
  Container image + digest, conda env + `environment.yml`, venv + lockfile, or none of
  the above? Please send the actual lockfile / env export / Dockerfile if one exists,
  and say which machine it describes.
- **A2.** **What is deliberately *not* pinned?** (e.g. the ColabFold public API, CUDA
  driver, a `pip install -e .` of a dirty tree.) Your own documents raise three of these
  themselves and we would rather have the full list than discover it:
  - `GATE_4_SCORER_DIFF.md:34` — the phantom SHA `891041e858f3`, "most likely artifact of
    a venv install from a dirty/rebased tree";
  - `C-5_pre_freeze_no_git_subtrees.md:6-9` — eight pre-freeze subtrees carrying
    `scorer_git_sha=no-git` because "the venv was pip-installed without `setup.py`'s
    `build_py` step running";
  - `C-B-12_empty_generator_shas.md:5-13` — `manifest.provenance.json` carries
    `propose_py_git_sha = ""` and `build_manifest_py_git_sha = ""`, i.e. **the code that
    produced the decoy scrambles and shuffled assignments has no recorded identity.** Can
    those two commits be identified retroactively? (We note the compensating control —
    content-hash verification in Phase 1b/1c — and agree it is a good one; we would like
    both.)
- **A3.** **Could you re-run a job from 2026-09-06 today and get the same answer — and
  have you actually tried?** Both halves matter, and "no" or "never tested" is a
  perfectly good answer that we would much rather have now than discover in month two.
  If you have a byte-identical replay anywhere, name it. (`scripts/subsample_msa.py` is
  described in `HEADLINE_D3…:139` as having "byte-identical replay" — is that a property
  of that script alone, or of the pipeline?)
- **A4.** **Per-backbone identity — the biggest single hole in all four drops.** For
  Boltz-2, Chai-1, OpenFold-3-preview and Protenix v2: repo URL, git tag or commit,
  pip/conda package version, container image + digest, and **weights checkpoint filename
  and hash**. We checked: no version string, no commit, no digest and no checkpoint name
  appears anywhere in the four drops beyond the informal labels "Boltz-2", "Chai-1",
  "OF3-preview", "Protenix v2". We also opened the 15 shipped Block D CIFs directly —
  none carries a `_software` or producer-version record; the only metadata is
  `_audit_conform.dict_version` (1.4.6 Boltz, 1.4.9 Chai) and Protenix/OF3 CIFs carry no
  provenance block at all. So today the corpus can prove what **scored** a row and not
  what **predicted** it.
  - **A4a.** Would you be willing to extend the pattern you already use for the scorer —
    a row-level `scorer_git_sha` column, treated as authoritative over prose — to the
    four backbones, as a per-row or per-manifest stamp? That one change would retire
    most of this section permanently.
- **A5.** Where did each backbone's weights come from (release download, internal build),
  and were they re-downloaded at any point during Blocks A→D? A silent checkpoint change
  mid-campaign is the kind of thing only you can rule out.
- **A6.** GPU/hardware: the drops mention H100s (25 H100 workers for the D3 drain,
  `HEADLINE_D3…:3-6`). Was every backbone run on the same hardware and precision
  throughout? Any mixed-precision or TF32 setting that differed per backbone?
- **A7.** **Cost, which no document in our possession records:** roughly how long does
  one prediction take, per backbone, for a ~400-residue receptor alone and for receptor +
  partner? And what is the practical compute budget? Every "N predictions" figure in our
  redo planning is a count, not an hour-estimate, and the ranking of experiments would
  change if one backbone is 10× another. One line is enough.

---

## 3. Section B — orchestration: how one run is launched, and what happens when it breaks

- **B1.** **Which scheduler?** `qsub` and job IDs (35918926 D1 rescore, 35920895 D2,
  35921904 D3) appear in `data/block_d/07_partA/HEADLINE_D*.md`, and
  `data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md:93` refers to "when the SGE job
  exits" — but the scheduler is never named in a way we can cite. SGE? PBS? Please also
  send a representative submission script with its resource requests (queue, wall limit,
  GPU count, memory), and say whether array jobs were used.
- **B2.** **The dispatch path, end to end.** Our reading from your documents is:
  `refs/*` + `partners.fasta` → a manifest builder (`scripts/build_manifest.py`,
  `build_block_a_manifest.py`, with `CONDITION_PRESETS['block_b']`) → per-row input files
  via `scorer/propose.py::materialise_inputs` / `_row_input_content` → `qsub/rerun_*.sh`
  → a pool directory on HPC → rsync to the MacBook → rescore → `rows.csv`. Is that
  right, and what is missing from it? A diagram or a numbered list is fine.
- **B3.** What runs on HPC and what runs on the MacBook? Our reading is: inference on
  HPC, rescoring on the laptop (D1 rescore "wall 6-30s on 16 workers", D3 "~5 min wall on
  16 CPU workers"). Is scoring ever run on HPC? Is inference ever run locally?
- **B4.** **Seeds.** How are the five seeds per cell generated — fixed list, derived from
  a run ID, or drawn? Are they recorded per row or only derivable from the output path?
  Three things we observed and cannot interpret:
  - The D3 canonical seeds are published as literals
    (`1742850888/1717002185/564473205/1708630764/2092191293`, `HEADLINE_D3…:13-14`), and
    job names carry a **seed index** (`seed0`…`seed4`) alongside the numeric seed.
  - The index→numeric mapping is **not stable across tiers**: from
    `data/block_d/10_structures/MANIFEST.json`, `seed4` is `1015473677` in D1,
    `1291532968` in D2 and `2092191293` in D3.
  - **OF3 paths carry two different numeric seeds.** e.g.
    `…/of3/seed_1015473677/chunk_0/tier_d1_lpar1_apo_of3_seed4_seed4/seed_2344327426/…_seed_2344327426_sample_5_model.cif`
    — an outer seed and a derived inner one, with only the outer recorded in the
    manifest. Is `seed` therefore a different object for OF3 than for the other three,
    and are per-seed comparisons across backbones like-for-like?
- **B5.** **OF3 chunking.** `HEADLINE_D1…:10` records "OF3 chunking: 4 chunks × 25
  samples per row (commit `24d155d`)". So D1's "5 seeds × 100 samples" is, for OF3,
  5 × 4 × 25 with a per-chunk derived seed. Does each chunk get an independent seed, and
  are the 100 OF3 samples statistically equivalent to the 100 Boltz samples for the
  purpose of a per-cell rate? This is load-bearing for every per-backbone comparison in
  the paper.
- **B6.** **Failure handling — OOM, timeout, straggler.** `HEADLINE_D2…:3` records "3
  OF3 stragglers on `AGTR1 × active_nb` hung ~3 h with no progress; workers killed to
  reclaim H100 slots", and `C-D-5` adds "No retry attempted". So this has happened and
  you documented it well. What we need for the redo:
  - Is **partial output** ever included in the analysed corpus, or only whole rows?
  - Does a **retried** job get the same seed, or a fresh one?
  - Is there a **resume** path after a partial campaign failure, and **can it
    double-count** — i.e. can a retried row and its original both land in the pool and
    both be scored?
  - Is the landed/dispatched shortfall detected automatically, or by someone reading a
    count? (The D3 shortfall is reported in two units in two places — "19 rows failed
    (0.7 %)" at dispatch-row level in `HEADLINE_D3…:113` vs "190 of 26,000 dispatched
    rows did not land (0.73 %)" at prediction level in `PARTA_D3.md:167` — which we read
    as two views of the same event, but it would help to have the canonical one.)
- **B6a.** **The OF3 Round-1/2/3 recovery is the most instructive failure record in the
  drops and we would like the mechanism behind it.**
  `EXPERIMENT_DOSSIER_BLOCK_B.md:202` records that OF3 Round-1 residuals showed a **6.0×
  decoy/cognate failure ratio (12 vs 2 of 200)**, exceeding the dispatch's 3×
  surface-immediately threshold, and that it was fully recovered by Round-2 (26/27 at
  64 GB memory) and Round-3 (purge-race fix, commit `b08ec91`) — with the note that it is
  recorded so *"the same recovery run twice would not restore this bias"* is auditable.
  We are not raising this as a defect: you state the bias is not in the delivered corpus
  and we have no reason to doubt it. The questions are forward-looking:
  - **An arm-dependent failure rate is an arm-dependent selection effect** if recovery is
    ever incomplete. Is there a standing check for differential missingness by arm, or was
    the 3× threshold applied by hand this once?
  - Was the failure mode (memory, then a purge race) diagnosed, or worked around?
  - Is the Round-2/Round-3 recovery a documented procedure or a one-off?
- **B6b.** **Re-runs and double-counting.** Block A has an OF3 seed-fix rerun subtree
  (`018_block_a_switch_test_of3_rerun_2026_09_02/`, 2,375 rows) and a merge driver
  `scripts/merge_of3_rerun_rows.py` that **was never executed** — `W-6` withdraws the
  earlier claim that it had been, and records that the primary Block A `rows.csv` points
  at the **same CIFs** as the rerun tree (100 % `input_path` overlap on 2,375 CIFs) while
  carrying the correct `04243c45…` stamp. So the corpus is fine. But it means two trees
  can reference one set of coordinates, and a merge script exists that would change the
  provenance if run. **Is there a rule about which tree is authoritative when a cell has
  been re-run, and is it enforced anywhere other than by not running the script?**
- **B9.** **The runtime-echo gap — probably the cheapest permanent fix in this document.**
  `EXPERIMENT_DOSSIER_BLOCK_B.md:109-117` reports 3,200 `_<backbone>_status.json` sidecars
  (800 per backbone) and a stratified 20-file sweep finding that **0/20 carry a
  `runtime_config` / `experiment_settings` / `config_snapshot` block**, and that every
  file is the minimal 5–6 key form `{exit_code, n_produced, ok, produced_files, seed}`
  (+ `backbone` on three of four). `C-B-1_templates_evidence_class.md:5-9` then classifies
  all backbone-configuration evidence as class (b) launcher static analysis + class (c)
  upstream defaults, explicitly **not** class (a) runtime echo, *because no runtime config
  was ever written to disk*.
  That single gap is why §2 (versions), §3 (inference config) and C6 (templates) all have
  to be asked as questions rather than read off an artefact. **Would you be willing to
  have each launcher dump its fully-resolved config — including the backbone version and
  weights identity — into the status sidecar in the redo?** If so, most of this document
  becomes unnecessary for the next campaign, and we would rather spend the effort there
  than on reconstructing the last one.
- **B7.** **Transfer.** Three `random` entries in
  `data/block_d/10_structures/MANIFEST.json` carry
  `"landed": false, "error": "kex_exchange_identification… rsync(23885): unexpected end
  of file"`. Is the HPC→laptop transfer verified by hash after the fact, or by exit
  code? Could a truncated file ever be scored? (Block D ask 7 already asks for those
  three structures; this is the general question, not a repeat of that ask.)
- **B8.** Where do outputs land, and what is the directory grammar? We can reconstruct
  four different per-backbone layouts from `MANIFEST.json` `hpc_path` fields — Boltz
  `…_model_5.cif`, Chai `pred.model_idx_5.cif`, Protenix `…_sample_55.cif`, OF3
  `…_sample_5_model.cif`, plus a doubled `full/pool/pool/` segment — and we would rather
  have the rule than the reverse-engineering. **How is `sample_idx` derived from each
  backbone's own file naming, and is sample index comparable across backbones?**

---

## 4. Section C — MSA preparation, per backbone

**This has its own section because it may decide whether "backbone" is a clean factor at
all.** Boltz-2, OpenFold-3, Protenix and Chai-1 each expect a different MSA format and
each ship a different default pipeline. So there are two possible worlds:

- **one alignment built once and reformatted four ways** — in which case "backbone" is a
  clean factor; or
- **four independent MSA pipelines** — in which case **backbone is confounded with input
  construction**, and every per-backbone difference in the paper is partly a harness
  artefact rather than a model property.

We are not guessing at which: **your own audit already demonstrates divergence.**
`data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md` finds Boltz, Protenix and OF3 all carry
the scrambled decoy α5-CT as **aligned uppercase columns in the query row** (6/6 each),
while Chai's `.aligned.pqt` cache anchors the decoy query row to WT-parent residues, gaps
or lowercase insertions on **0 of 40** — and `msa_depth_report.md:56-68` finds Chai's
`pairing_key` empty on 100 % of rows **in every arm, cognate included**. That is one
backbone reading a different input from the other three, on the single edit the decoy arm
exists to make.

So the question is not whether the pipelines differ. It is **what else differs**, and
whether the redo should unify them.

- **C0.** **Which world is it — one MSA reformatted four ways, or four pipelines?** And
  if four: which parts are genuinely forced by each backbone's format, and which are
  incidental? We would like to unify everything incidental in the redo, and to state the
  irreducible remainder in the Methods.
- **C1.** **Were all four backbones given byte-identical *sequence* inputs?** Our reading
  from
  `data/block_b/02_constructs/construct_build_report.md:196-210` is that one partner
  FASTA is wrapped per backbone by `scorer/propose.py::materialise_inputs` /
  `_row_input_content(backbone, …)` into Boltz YAML, OF3 JSON, Protenix JSON and Chai
  FASTA — so the **sequence** is shared but the **wrapper** is not. Is that right, and
  is there anything else that differs per backbone at the input layer?
- **C2.** **MSA provider, per backbone — please confirm or correct our reading.** From
  `data/block_b/03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md:276` and
  `PHASE_1D_EXTENSION.md:56,60,93,128`:
  - **Chai** reads a local cache, `/hpc/scratch/sengaad1/paper_af3/msa_cache/chai/<sha256>.aligned.pqt`,
    via `CHAI_MSA_DIRECTORY` defaulted in `qsub/rerun_chai.sh`.
  - **Boltz** and **OF3** consume ColabFold — OF3 fetching at inference time through
    `qsub/colabfold_shim.py` → `api.colabfold.com/ticket/msa`, writing to per-job scratch
    `$TMPDIR/of3-of-sengaad1/colabfold_msas/{main,paired,template}/` that is purged when
    the job exits.
  - **Protenix** invoked its **own** MSA server (`--msa_server_mode protenix`), described
    as "separate from the ColabFold public API pipeline".

  If that is right, then **the four backbones did not receive the same alignments**, and
  that is a first-class design fact for the redo rather than a defect. We would like it
  stated explicitly, per backbone, so the Methods can say it.
- **C3.** **Databases and versions.** For each MSA route: which databases (UniRef90,
  BFD/Uniclust, MGnify, ColabFoldDB, …), which release, what search tool and parameters
  (MMseqs2/jackhmmer/hhblits, iterations, e-value), and **on what date** the alignments
  were generated. No database name or version appears in any of the four drops. If the
  ColabFold public API was used, its server-side DB version at the time is probably not
  recoverable — if so, **UNKNOWN is the answer we want**, not a best guess.
- **C3a.** **Where does each backbone's MSA physically live, and in what format?** From
  `PHASE_1D_EXTENSION.md:25-27,62,93` the four layouts are already different objects:
  Chai a per-chain `.aligned.pqt` keyed by sequence sha256; Boltz a two-column
  `key,sequence` CSV at `…/boltz_results_<N>/msa/<N>_1.csv` plus
  `msa/<N>_paired_tmp_pairgreedy-env/pair.a3m` and
  `msa/<N>_unpaired_tmp_env/{uniref,bfd.mgnify30.metaeuk30.smag30}.a3m`; Protenix
  `…/msa/<K>/{pairing,non_pairing}.a3m` with `K ∈ {0,1}`; OF3 nothing retained but the
  hashed paths in `inference_query_set.json`. **Is any conversion lossy?** Specifically:
  does the Chai `.aligned.pqt` conversion drop lowercase insertion columns, and is that
  what produces the decoy read-through difference?
- **C3b.** **Is the Chai finding a cache-format artefact or a model-input artefact?** i.e.
  did Chai's model actually see WT residues at the α5-CT, or only the cache
  representation we can inspect? This decides whether Block B's decoy result is a
  three-backbone or a four-backbone result, and `rebuttals/BLOCK_B.md` **Q9** asks the
  same thing from the other side ("Is a rerun with a forced MSA feasible?").
- **C4.** **Depth caps and effective depth.** Was any `max_seqs` / `max_msa` /
  `max_msa_clusters` / `max_extra_msa` cap applied at inference, per backbone? Distinct
  from the D3 subsampling ladder — we mean the default run. Related, and flagged in your
  own report (`msa_depth_report.md:246-252`): raw row count is **not** effective sequence
  count after clustering, and "this cache format doesn't expose the post-clustering
  effective-N". **If the model logs an effective N anywhere, we want that number, not the
  row count.**
- **C5.** **Pairing.** Were MSAs paired across chains, and how? What we can see:
  - Boltz: "format supports pairing; paired and unpaired subdirectories both present"
    (`PHASE_1D_EXTENSION.md:56`).
  - Protenix: separate `pairing.a3m` and `non_pairing.a3m` under `msa/{0,1}/`, with
    "chain-to-subdir order not stable across cells (matched here by query length)"
    (`:60`). That instability is worth a sentence of its own — how is chain order
    determined?
  - OF3: `use_paired_msas: true`, both `paired_msa_file_paths` and `main_msa_file_paths`
    populated (`:131`).
  - Chai: `pairing_key` and `comment` are **empty-string on every row of all 120 cache
    files** (`msa_depth_report.md:59-68`), and `SEQUENCES.md` §6.2 reads that as pairing
    never having been wired in for Chai.

  So our reading is **three backbones paired, one not**. Confirm or correct. And: for a
  paired two-chain input, when we say "MSA depth", which number do we mean — the main
  MSA, the paired MSA, or the union? The two differ by roughly 2× in your own tables
  (Boltz ADRB1 cognate: 13,678 main rows at `PHASE_1D_EXTENSION.md:39`, 6,820 paired at
  `:67`).
### Section C2 — the rest of the input: templates, ligands, chains, sequences

- **C6.** **Templates.** `data/block_b/12_narrative/BLOCK_B_CLAIM_SHEET.md:301-304`
  records templates absent on all four, but by four different evidence classes: no
  template flag in `qsub/rerun_boltz.sh`; `use_templates_server = False` default at
  `chai_lab/chai1.py:334,492`; explicit `--use-templates false` on both paths of
  `qsub/rerun_of3.sh`; `use_templates = False` model-config default for Protenix. Two of
  those are *defaults*, not *settings*. For the redo we would like templates set
  **explicitly** on all four — and for the record, please confirm no template path was
  ever active in Blocks A–D. (The word "template" does not appear anywhere in the Block D
  bundle.)
- **C7.** **Ligand representation.** SMILES or CCD code, per campaign? Block B's row
  table carries both `ligand_smiles` and `ligand_sequence` columns. How is a ligand
  chosen for a receptor, what happens when a receptor has no ligand for a role, and how
  are peptide ligands represented (polymer chain vs ligand entity)?
  `scorer/pocket_metrics.py`'s `MCS_FALLBACK_MIN_COVERAGE=0.8` guard is described as
  preventing "fast-path spurious matches on SMILES-derived atom names" — which suggests
  atom naming differs by backbone. Does it?
- **C7a.** **Nothing shipped identifies which molecule was placed.** `ligand_resname` in
  the Block C census takes exactly six values across all 40,000 rows — `LIG0` (8,300),
  `LIG1` (8,300), `LIG2` (4,150), `LIG3` (4,150), `l01` (8,300), `PEPTIDE` (6,800) —
  i.e. slot labels, not chemistry. Were CCD codes or SMILES available at census time, and
  can they be carried per row in the redo? (`rebuttals/BLOCK_C.md` **Q10**. It is the
  difference between being able to check that a `decoy_lig` is the decoy it was meant to
  be and having to take it on trust.)
- **C8.** **Chain order and stoichiometry.** Is the receptor always chain A and the
  partner chain B? Is that guaranteed at input or recovered at scoring? Protenix's
  "chain-to-subdir order is not stable across cells" (C5) makes us want this stated. Any
  ions, lipids, waters, or tags in the input? (We note
  `nanobody_state_anchors.csv` records "C6xHis tag retained verbatim from FASTA" for
  Nb60.)
- **C9.** **Receptor sequence source.** `refs/panel_receptor_sequences.fasta` (51
  entries) vs `docs/EXPERIMENT_CATALOG/sequences/receptors.fasta` — `HEADLINE_D3…:97-99`
  records AA2AR being fetched from the wrong one ("fusion-tagged sequence… 479 aa instead
  of the panel sequence… 412 aa. Refetched, cache rebuilt"). Which file is canonical, are
  construct boundaries (truncations, fusions, tags) recorded per receptor, and is there a
  check that the dispatched sequence matches the panel file?

---

## 5. Section D — arm definitions and construct rules

- **D1.** For every arm that has ever run — `apo`, `cognate_ga`, `decoy`, `shuffled`,
  `active_nb`, `inactive_nb`, and anything in Block A's partner-diversity work — please
  give the exact construction rule and the exact residue ranges used.
- **D2.** **The α5-CT length convention.** We need this stated once, precisely, because
  we found our *own* documents specifying it wrongly. Two of our files specify the 21-mer
  as "Gα residues 334–354"; from your `construct_build_report.md` the five canonical
  partners are Gs/GNAS 394 aa, Gi/GNAI1 354, Gq/GNAQ 359, G12/GNA13 377, Gt/GNAT1 350 —
  so 334–354 is the C-terminal 21 **only for Gi1**, and for Gs it ends 40 residues short.
  **That error is ours, not yours**, and we are flagging it because the redo will ask you
  to build a length ladder and we want the convention fixed before anything is
  dispatched. Our proposal: lengths are always expressed **from the C terminus**, never
  as absolute residue ranges. Does anything in your pipeline resist that?
- **D3.** **What the decoy scramble preserves.** `construct_build_report.md:91-108`
  documents it well: the last 11 residues permuted with a per-receptor seed
  `SHA-256(receptor_slug + '|block_b_decoy_v1|' + variant)`, Hamming floor 5, composition
  preserved by construction with an asserted `Counter` check, rest of the Gα scaffold
  byte-identical. Two follow-ups: (a) is `scripts/build_shuffled_decoy_constructs.py`
  available? (b) composition is preserved but **helical propensity and net charge are
  not** — was either measured?
- **D4.** **Nanobody arms.** We hold both the consumed FASTA and the anchor table
  (`data/block_d/09_references/nanobody_sequences.fasta` and `nanobody_state_anchors.csv`)
  — **not asking for either.** What we cannot see: were tags (the C-terminal His6 that
  `nanobody_state_anchors.csv` notes as "retained verbatim from FASTA") included in the
  dispatched sequence, and does a retained tag affect the scoring chain-picker or the
  interface contact count?
- **D5.** **Full Gα vs mini-Gα vs heterotrimer.** Every partner arm in all four blocks
  appears to be a **complete Gα subunit** (or a nanobody) — no arm supplies a peptide of
  any length, and `construct_build_report.md:105-108` states β and γ "are outside the
  scope of the single-partner-chain pipeline". Confirm: is the input schema
  **single-partner-chain** throughout, and would a three-chain input (Gα + Gβ + Gγ) be a
  harness change rather than a config change?
- **D6.** `partners.fasta` carries two documented mislabels that your own audit found —
  `GASR` (self-declared Gα, actually the gastrin receptor) and `Nb60` (carrying the Nb80
  CDR3). Neither was consumed by Block B. Is there a corrected version of the file, and
  would you be willing to key constructs by **sequence hash rather than header** in the
  redo? We intend to, on both sides.

---

## 6. Section E — scoring: how a `rows.csv` line is built, column by column

**This is the section the PI cares most about.** Sending `scorer/` (§1 ①) answers most
of it; the questions below are the ones we would still ask after reading the code, and
they are the ones that will go into Methods.

### E.a Residue numbering — how the scheme was *decided*, and how a generic number becomes an atom

We would like this as a decision record, not only as an implementation note: **which
scheme, from which source, at which version, and why that one.**

- **E1.** **Where does the generic numbering come from?**
  `data/block_b/12_narrative/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md:33` cites
  `docs/BW_SOURCE.md`. Please send it. Which GPCRdb release, fetched when, and is it
  cached or fetched live?
- **E1a.** **Which scheme per entity?** Class A appears to use Ballesteros–Weinstein /
  GPCRdb generic (`3.50`, `5.58`, `6.30`, `7.53`); Class B appears to use **Wootten**
  (`6.39/6.50/6.54` for the kink); Class F uses tilt alone. Is there a **CGN** (common
  Gα numbering) scheme in use for the partner chain, or is the α5-CT indexed from the C
  terminus? For the redo we will be manipulating the α5 segment directly, so the Gα-side
  convention needs to be explicit.
- **E1b.** **Class-conditional mapping.** Class B and Class F receptors need a different
  anchor mapping from Class A — `MANUSCRIPT_FLAGS.md:265` records "5 Class B rows skipped
  (BW 2.46/6.37 undefined in Wootten numbering)" and Flag 48 records
  `anchor_6_30_uniprot_pos = -1` as an encoded not-applicable on 200 GCGR rows. How is
  the per-class mapping selected, and what is the not-applicable convention (`-1` vs
  NaN vs skip)? This matters because a pooled "predicate-active rate" over 48 receptors
  mixes three instruments.
- **E2.** **How is a generic number mapped onto a predicted structure that has no
  deposited numbering?** From the one scoring script you shipped —
  `data/block_c/12_g4_off_site_census/g4_full_census_v2.py:84-104` — the rule appears to
  be: read a per-receptor `anchor_positions` JSON from `refs/reference_set.csv`, then for
  each wanted BW label find **any anchor in the same helix** and compute
  `anchors[a_bw] + (off - int(a_bw.split(".")[1]))` — i.e. a **linear offset from the
  nearest same-helix anchor**, with residue numbers read straight off the model
  (`r.seqid.num == pos`).
  - **E2a.** Is that the same rule `scorer/anchors.py` uses for the predicate axes, or
    does the scorer do something different from the census script?
  - **E2b.** The linear-offset rule assumes no insertion, deletion or bulge between the
    anchor and the target position within the helix. Is that assumption checked
    anywhere, and does it hold across all 48 receptors?
  - **E2c.** It also assumes the predicted structure's residue numbering equals the
    1-based index into the supplied construct sequence. Is that guaranteed for all four
    backbones, including when a tag or a truncation is present?
  - **E2d.** **The mapping appears to exist upstream and not to have been shipped.**
    Four documents reference `rows.csv:anchor_*_uniprot_pos` as the per-prediction
    anchor→residue mapping (`block_a/11_structures/success_case/ALIGNMENT.md:27`,
    `broken_cell/ALIGNMENT.md:25`, `block_a/DATA_DICTIONARY.md:437`,
    `MANUSCRIPT_FLAGS.md:263`), but **no `anchor_*_uniprot_pos` column is in either
    shipped row table.** We hold the mapping for *references*
    (`data/block_b/09_references/reference_set.blockb_pinned.csv::anchor_positions`,
    which ships and which we are not asking for) but not for *predictions*. Carrying
    those columns into the row table would turn most of §E.a from a question into a
    verifiable artefact, at essentially zero cost.
  - **E2e.** **What would happen downstream if the mapping were off by one — and which
    check would catch it?** An off-by-one on 5.58 or 7.53 moves the NPxxY axis by roughly
    a residue's worth of geometry and would flip predicate calls near the threshold,
    silently. Is there any check that would fire? We would like the honest answer even if
    it is "none".
  - **E2f.** What happens on an **insertion, a deletion, or a missing loop** between the
    anchor and the target position — is it detected, or does the offset arithmetic just
    return the wrong residue?
- **E3.** **How are the `anchor_positions` themselves established** per receptor — by
  sequence alignment to a GPCRdb reference, by SIFTS, by hand? `EXPERIMENT_DOSSIER_BLOCK_D.md:38`
  mentions "`identity_match_to_wt` (v2 anchor-hit + SIFTS)", which is the only mention of
  SIFTS we have. What happens when an anchor does not resolve?
- **E4.** **Please enumerate the 12 pocket BW positions and the predicate anchors.** We
  have the pocket 12 from two independent places and they agree —
  `BLOCK_B_ITEM3…:15-21` quoting `scorer/pocket_metrics.py:81-86` (`POCKET_BW_LABELS`),
  and the `POCKET_BW` tuple in the census script: 3.32, 3.33, 3.36, 5.42, 5.43, 5.46,
  6.48, 6.51, 6.52, 6.55, 7.39, 7.42. We would like that confirmed as canonical, plus the
  positions behind the predicate column names (`y558`/`y753` = 5.58/7.53; `246`/`637` =
  GPCRdb 2×46/6×37; `r350`/`r630` = 3.50/6.30), and the "4/4 BW anchors" used by the
  anchor-identity QC in `GATE_3…:159-170`.

### E.b The metric inventory — one line each, please

**E4a.** Here is every metric column we can find across the shipped row files, recomputed
from the files today (Block A 55 columns, Block B 76, Block C's census 16, Block D none).
**For each one we would like four things: the exact atoms, the exact definition, where it
is computed, and whether it is emitted by the model or derived downstream.** A table is
the ideal form; a filled-in version of this list would close §E almost entirely.

| group | columns (A = Block A, B = Block B) |
|---|---|
| **predicate axes** | `d_npxxy_y558_y753_oh` (B) / `d_npxxy_oh` (A); `d_gpcrdb_tm6_tilt_246_637_ca` (A,B); `d_npxxy_y558_y753_ca` (B); `angle_class_b_tm6_kink_639_650_654_deg` (B) / `tm6_kink_angle` (A) |
| **thresholds** | `threshold_npxxy_oh_active_lt`, `threshold_gpcrdb_tm6_tilt_active_gt`, `thresholds_panel_csv_sha256` (B) vs `threshold_npxxy_used`, `threshold_tilt_used`, `threshold_kink_used` (A) |
| **other geometry** | `d_tm6_r350_r630_ca`, `d_tm5_outward_r350_r558_ca`, `d_y558_pack_min_heavy`, `d_dry_sidechain_r350cz_e630oe1`, `w648_chi1`, `icl2_helical_frac`, `tm6_helicity_6_30_6_50`, `tm6_helicity_pass` |
| **partner engagement** | `d_ga_alpha5_r350_ca`, `n_interface_contacts_ga_receptor`, `plddt_ga_alpha5` |
| **RMSD family** | `rmsd_to_active_ref`, `rmsd_to_inactive_ref`, `rmsd_pos`, `rmsd_n_residues_used`, `pocket_ca_rmsd`, `pocket_sidechain_rmsd`, `ligand_rmsd_to_ref`, plus free-text `rmsd_note`, `pocket_notes` |
| **confidence** | `plddt_mean`, `plddt_at_anchors`, `plddt_at_anchors_list` (A only), `min_plddt_at_anchor`, `confidence_flag` |
| **derived** | `delta_to_active`, `delta_to_inactive`, `receptor_midpoint` |

Two things we would like raised explicitly against that list.

- **E4b.** **Block A and Block B name the same quantity differently, and we need to know
  whether the definition changed.** `d_npxxy_oh` (A) vs `d_npxxy_y558_y753_oh` (B);
  three `threshold_*_used` columns (A) vs two `threshold_*_active_*` columns (B);
  `tm6_kink_angle` (A) vs `angle_class_b_tm6_kink_639_650_654_deg` (B); `seed_outer` +
  `seed_inner` (A) vs `seed_used` (B); and Block A ships a boolean `active` while **Block
  B ships no boolean state column at all**. Block A's own dictionary records the mapping
  `d_npxxy_oh ← rows.csv:d_npxxy_y558_y753_oh`, which reads as a rename only. **If it is
  only a rename, say so and we will stop worrying.** If the definition changed between
  campaigns, no cross-block comparison is safe — and we make several, including the
  Block B ↔ D1 comparison in Q2 above.
- **E4c.** **Which metrics have free-text companions, and what values do those take?**
  `rmsd_note`, `pocket_notes`, and the census's `note`. A free-text field carrying a
  caveat that no code reads is a **silent exclusion**: the row looks fine, the number is
  wrong, and nothing downstream knows. We can tell you the census's `note` is empty on
  all 40,000 rows; we would like the value distribution for the other two, and a
  statement of whether any consumer parses them.
- **E4d.** **Engagement is defined differently in the two blocks.** Block A ships a
  derived `engaged` column (`n_interface_contacts_ga_receptor > 30`); Block B has no
  `engaged` column and instead applies a **tip-depth cutoff on `d_ga_alpha5_r350_ca`,
  swept over {10, 12, 14, 16, 18, 20} Å** with 20 Å headline and 14 Å as the required
  sensitivity. Was that a deliberate change of instrument, and which should the redo use?

### E.c Distances and RMSDs

- **E5.** For each distance column in the row tables — `d_npxxy_y558_y753_oh`,
  `d_gpcrdb_tm6_tilt_246_637_ca`, `d_tm6_r350_r630_ca`, `d_npxxy_y558_y753_ca`,
  `d_tm5_outward_r350_r558_ca`, `d_y558_pack_min_heavy`,
  `d_dry_sidechain_r350cz_e630oe1`, `d_ga_alpha5_r350_ca` — **which two atoms, exactly?**
  The names imply OH/CA/CZ/OE1 but we would like it from the code or a table. And
  `d_y558_pack_min_heavy` reads as a minimum over a set — over which set?
- **E6.** **Superposition.** `GATE_3…:117-118` gives `gemmi.superpose_positions` on
  "first-chain Cα atoms, all resolved positions (~350–380 per structure)". Is that the
  same superposition used for `rmsd_to_active_ref` / `rmsd_to_inactive_ref` /
  `pocket_ca_rmsd`, or do those differ? `BLOCK_B_ITEM3…:63-64` describes a different
  sequence for the reference table: Kabsch transform on TM Cα, then residue-wise RMSD on
  pocket Cα. Which applies where?
- **E6a.** **What is the 7TM residue set, and what is the completeness gate?** The scorer
  commit of record is titled "RMSD: 7TM-only residue selection + completeness gate"
  (`EXPERIMENT_DOSSIER_BLOCK_B.md:71`), so both exist; neither is written down. Same for
  the pocket-residue set behind `pocket_ca_rmsd` / `pocket_sidechain_rmsd` — is it the
  same 12 BW positions as E4, or a different set?
- **E6b.** **Two different reference-reduction rules appear to operate on one file.**
  `rmsd_to_active_ref` is documented as RMSD to the **closest** active reference, while
  `receptor_d_active_ref` is documented as the **median** over references
  (`block_b/DATA_DICTIONARY.md:57,87-91`) — and receptors have up to three references per
  role in `reference_set.blockb_pinned.csv`. Is that deliberate (min for a structural
  distance, median for a calibration anchor), or did one of them drift? Related: `PARTA_D2.md:117-126`
  shows ADRB2 with three inactive references (2RH1 / 3NYA / 6PS2) and does not say which
  is used.
- **E7.** How are **missing residues in the reference** handled — are RMSDs computed on
  the intersection, and is the residue count recorded? (Block B has
  `rmsd_n_residues_used` and `rmsd_note`; Block A does not.)
- **E8.** `angle_class_b_tm6_kink_639_650_654_deg` and `icl2_helical_frac`,
  `tm6_helicity_6_30_6_50`, `w648_chi1`, `ramachandran_outlier_frac`, `chain_breaks`,
  `icl3_modelled_count` — definition and threshold for each. The Class B kink angle and
  the Class F tilt-only predicate are separate instruments from the Class A predicate;
  please state all three.

### E.d The pocket itself — which twelve residues, and why those twelve

**This is a different question from the cutoffs in E.e.** Those are thresholds *on* a
distance; this is **what the distance is measured to**. Move one of these twelve positions
and two separate results in the paper move with it: the entire Block C 2×2 is
`pocket_ca_rmsd_active − pocket_ca_rmsd_inactive` over these residues, and the whole
40,000-prediction placement audit measures to **their centroid**. The G4 gate that fired on
8 of 12 cells is, mechanically, a statement about these twelve positions.

What we can see. `data/block_b/12_narrative/BLOCK_B_ITEM3_AA2AR_AND_POCKET_CA.md:14-22`
records the set verbatim from `scorer/pocket_metrics.py:81-86` (the constant
`POCKET_BW_LABELS`):

```
3.32, 3.33, 3.36
5.42, 5.43, 5.46
6.48, 6.51, 6.52, 6.55
7.39, 7.42
```

and `:30-34` gives the mapping source as a GPCRdb `residues/extended/<entry>/` cache at
`refs/cache/gpcrdb/residues_ext_<uniprot_slug>.json`, "the campaign's canonical BW source
(see `scorer/bw_numbering.py:118-150` and `docs/BW_SOURCE.md`)", with all 12 labels
resolving on all 40 receptors (`n_pocket=12` on every row).

**The manuscript states none of it.** `manuscript/sections/methods.tex:418` says only "the
C$\alpha$ RMSD of the ligand-binding pocket" and `:440` "the distance from the ligand
centroid to the pocket centroid". A reader cannot learn which residues those are. We would
like to fix that, and we cannot write the sentence without you.

- **E8a.** **Where did the twelve come from?** A citation, a contact-frequency analysis
  over deposited complexes, an author's judgement — **any of those is a fine answer.**
  Unstated is the only one we cannot write down.
- **E8b.** **Were they fixed before the analysis ran, or adjusted after seeing results?**
  And was any alternative set tried? If a set was tried and discarded, that is exactly the
  kind of negative knowledge §11 asks for, and saying so costs nothing.
- **E8c.** **What pocket was used for the 4 Class B and 4 Class F receptors in Block A?**
  `BLOCK_B_ITEM3…:20-22` is careful to scope its statement — "Class A only; Block B panel
  is Class A only … so the pocket definition applies to every row" — which correctly
  covers Block B and leaves the other eight receptors in Block A unaccounted for. BW
  numbering does not apply to them. Is there a second pocket definition, or was pocket
  RMSD simply not computed for those rows?
- **E8d.** **How does a BW label become an actual atom** in a predicted structure with no
  deposited numbering — is it the GPCRdb cache lookup, the linear-offset arithmetic seen
  in the census script (E2), or both in different places? And **what would catch it being
  off by one?** (Same question as E2e, asked here because the pocket centroid is the place
  where a one-residue error is least visible: a centroid over twelve positions absorbs a
  single wrong residue without looking wrong.)
- **E8e.** **Please send `scorer/pocket_metrics.py` and `scorer/bw_numbering.py`.** Those
  two files probably answer half of §6 on their own, and they are the two we would pick if
  we could only have two.

### E.e "Is the ligand in the pocket" — the exact test

This definition is load-bearing: the G4 gate fired on 8 of 12 cells and its remedy was
never applied, so we need the test itself, not a summary of its results. The artefact we
are asking against is `data/block_c/12_g4_off_site_census/g4_full_census_v2.csv` (40,000
rows) and the script beside it, whose 16 columns are `input_path, receptor, backbone,
role, arm, distance_A, receptor_chain, receptor_anchor_hits, receptor_anchor_target,
ligand_source, ligand_chain, ligand_seqid, ligand_resname, ligand_n_heavy, note,
flag_low_confidence`.

- **E9.** **Please confirm this is the canonical test, and say where else a different one
  is used.** From `g4_full_census_v2.py` (docstring lines 8-33, constants at :66-67,
  binning at :349-354) our reading is: the pocket reference is the **centroid of the 12
  pocket-BW Cα atoms**, requiring ≥6 of 12 resolved (`:173-179`); the ligand is picked as
  the largest HETATM residue with ≥5 heavy atoms not on a blocklist, else a peptide-chain
  fallback (non-receptor polymer, 5–100 standard residues, <300 aa, shortest such chain);
  the measured quantity is `d_ligand_centroid_to_pocket_A`; and the bins are **in-pocket
  <8 Å, entrance-bound 8–15 Å, off-site ≥15 Å**, entrance-bound counted as valid.
- **E9a.** **What exactly is `distance_A`?** Ligand **centroid** to pocket **centroid**,
  or nearest heavy atom to nearest pocket atom, or something else? The column name in the
  CSV (`distance_A`) is more generic than the docstring's
  `d_ligand_centroid_to_pocket_A`, and centroid-to-centroid and
  nearest-atom-to-nearest-atom differ by several Å on a large ligand — enough to move a
  row across the 8 Å bin edge.
- **E9b.** **What is `receptor_anchor_target`, and where did that anchor set come from?**
  It takes exactly two values across the 40,000 rows: **6** on 38,800 and **20** on
  1,200. So the target is evidently the count of named anchors in that receptor's
  `anchor_positions` — six for most receptors, twenty for one. Which receptor has twenty,
  why, and is the pocket centroid computed over a different residue set for it?
- **E9c.** **What does `receptor_anchor_hits` count, and has it ever been informative?**
  We recomputed: `receptor_anchor_hits == receptor_anchor_target` on **all 40,000 rows**,
  `receptor_chain` is `A` on **all 40,000**, `flag_low_confidence` is `False` on **all
  40,000**, and `note` is **empty on all 40,000**. So the chain picker never disagreed
  with itself, the low-confidence guard (documented as firing when hits < 4) has never
  fired, and the unmeasurable path never ran. That may simply mean the pipeline is
  clean — or it may mean the two columns are written from the same source and cannot
  disagree. **Which is it?** This is the clearest instance in the corpus of the §9
  question "has this check ever actually fired", and we would rather know than assume.
- **E9d.** **How was the 8 Å cutoff chosen, and was it fixed before the census ran?** The
  script annotates it as matching "`scorer/pocket_metrics.py` Bug #2 tripwire", and
  `GATE_4…:56,84` describes Bug #2 as an "8 Å pocket-proximity tripwire on HETATM picker"
  replacing a "LEGACY largest-HETATM picker" in `build_pocket_reference_cache`, commit
  `48ddfc1`. Same for the 15 Å off-site edge and the decision to count 8–15 Å as valid —
  pre-specified, or set after seeing the distribution? Either is defensible; only one of
  them can be written in Methods.
- **E9e.** **Two pickers, one constant.** The census script has its own picker and
  `pocket_metrics.py` has another. Are they the same rule? Which rows were scored before
  commit `48ddfc1`, and were any migrated?
- **E9f.** **What happens when the ligand is absent, multi-copy, or split across
  chains?** The "largest by heavy-atom count" rule silently picks one of several copies;
  the peptide fallback picks the shortest non-receptor chain, which in a cognate-arm row
  could in principle select something other than the intended ligand. `ligand_source`
  splits 33,200 `hetatm` / 6,800 `peptide_chain` with no `none` at all, so the third
  branch never ran on this corpus. Is there a per-row record of *how many* candidates
  there were?
- **E12.** Is there any ligand-in-pocket test applied at **scoring** time (as opposed to
  this post-hoc census), and does it ever gate a row's inclusion?

### E.f Confidence

- **E13.** **How is pLDDT aggregated?** `plddt_mean`, `plddt_at_anchors`,
  `min_plddt_at_anchor`, `plddt_ga_alpha5`, `confidence_flag` — over which atoms, which
  chains, mean or median? This matters because partner-bearing rows have two chains, and
  because Block D uses both "pLDDT median" (`GATE_3…:38`) and "pLDDT_mean"
  (`PARTA_D3.md:152`) as cell statistics.
- **E14.** **Where is pLDDT read from, per backbone?** Protenix CIFs store it in
  `_atom_site.B_iso_or_equiv` while Boltz and Chai use ModelCIF `_ma_*` QA blocks. Is the
  scorer's extraction verified to be on the same scale for all four? A per-backbone
  offset here would silently move every confidence result in the paper.
- **E15.** Is any other confidence output captured — PAE, ipTM, pTM, per-chain pLDDT? If
  they exist in the raw outputs but are not in `rows.csv`, we would like them in the redo.

### E.g `passed`, exclusions, and what a row means

- **E16.** **What predicate sets `passed`?** In Block A it is `True` on 9,490 of 9,490
  rows while its six evidence columns `A1_amino_acid_identity`…`A6_receptor_identity` are
  100 % NaN, documented as "empty on pass by design" — so a suite that ran and passed and
  a suite that never ran are byte-identical in the shipped data. Block A ask 8 already
  requests explicit `pass`/`fail`/`not_run` values, so we are not re-asking; what we need
  **here** is the list of checks the suite actually contains, and whether a failing row is
  dropped from the corpus or retained with a flag.
- **E16a.** **What does each of A1–A6 actually assert?** We know the six names and that
  they are schema/identity checks; we do not know what any one of them tests. The list of
  assertions, one line each, would let us say in Methods what `passed` means.
- **E17.** **Exclusion flags.** Block A ships `excl_E1`…`excl_E5` (+ `excl_E3_tilt`,
  `excl_E3_npxxy`); Block B ships `excl_E_B_1`…`excl_E_B_4`. Please define each, and say
  **at which stage each is applied** — at scoring, at aggregation, or only by the
  consumer. Are any applied before the headline rates are computed? And: **which is
  authoritative for the exclusion flags, the claim-sheet header or the shipped
  definitions file?** (`rebuttals/BLOCK_B.md` **Q1**.) We ask because our own reading of
  the headline rates is that they reproduce with **no** exclusions applied on all 48
  receptors, while Methods says E1 and E2 "are applied everywhere" — and our first attempt
  to check this was wrong, so we would rather have it from you than from a third
  recomputation.
- **E18.** **The row schemas differ between blocks and we would like to know whether that
  was deliberate.** Block A's table (55 columns) has `active`, `npxxy_active`,
  `tilt_active`, `seed_outer`/`seed_inner`, `ref_pdb_sha_active`/`ref_pdb_sha_inactive`.
  Block B's (76 columns) has none of those; it has `ref_set_csv_sha256`, `seed_used`,
  and **no boolean state column at all** — every Block B state call in our draft is
  recomputed here from the two axis columns and the two threshold columns. For the redo we
  would like **one schema**, and we would rather agree it with you than impose one; see
  §14.
- **E19.** **Which columns come from the model and which are computed downstream?** A
  simple three-way tagging of the schema — model output / computed at scoring / carried
  from the manifest — would be extremely useful and is probably a 20-minute job.

---

## 7. Section F — references and the state annotation

- **F1.** **How was the active reference chosen for each receptor, and the inactive one?**
  Rule, not list. What resolution/method floor, what handling of engineered mutations,
  fusions and thermostabilising constructs? We could not find a selection rule anywhere in
  either drop — everything reference-side is a post-hoc audit of choices already made, and
  the audits are good ones. Two specifics that make the rule worth writing down:
  - **The Class A Gs Gα-complexed reference set contains no native heterotrimer.** All of
    it is mini-G, nanobody or chimera stabilised, and `native_gs_curation_audit.csv`
    records that **3SN6 exists for ADRB2 and was not selected** — so this is a curation
    choice, not an availability constraint. What was the reason? (`block_b/README.md:242-247`;
    `ASSUMED_NOT_VERIFIED_E.md:8-20`.)
  - **`reference_audit.csv`'s `method` and `resolution` columns hold a single placeholder
    string on all 80 rows** — `X-ray or cryo-EM (schema lacks explicit method column)` and
    `not tracked in reference_set schema`. They are non-null, so a `notna()` check passes
    and reports both columns as populated. Is method/resolution recoverable, and can the
    redo's reference schema carry them as real fields? (`rebuttals/BLOCK_A.md` **Q-A1**
    item 2 asks the same thing in the context of the panel rule; Block B ask 17 asks for
    the values.)
- **F1a.** **How was the panel selected?** (`rebuttals/BLOCK_A.md` **Q-A1**, flagged there
  as "the first question a referee asks".) All 40 Class A receptors have both a deposited
  active and inactive reference, 40 of 40, so "both states solved" is almost certainly the
  operative criterion — but that is inferred from the output. Was the panel *every*
  receptor meeting that criterion or a subset; was any qualifying receptor excluded and
  why; and when was the selection frozen relative to the deposition record? The redo's
  panel decision depends on this answer more than on anything else in the document.
- **F1b.** **`alpha5_donor_class` is empty on 78 of 80 reference rows**, so the Gα
  identity in the reference complex is mostly inferred from the receptor's cognate
  coupling rather than verified per structure (`ASSUMED_NOT_VERIFIED_E.md:83-101`). Can it
  be filled from the deposited entity list?
- **F2.** **Where does the active/inactive state label come from** — GPCRdb's activation
  annotation, a curated call, or the geometry itself? This is the one question that
  decides whether the instrument is circular, and it is currently a `[PI]` placeholder in
  our own Methods. Somebody knows the answer and it costs no compute.
- **F3.** **How were the two thresholds derived?** The Class A predicate is
  `d_npxxy_y558_y753_oh < 9.082 Å` AND `d_gpcrdb_tm6_tilt_246_637_ca > 14.932 Å`
  (PREREG §C-5, quoted identically in `HEADLINE_D1…:17`, `HEADLINE_D2…:23`,
  `GATE_2…:35-36`, `GATE_3…:32`). Our Methods says these came from 80 tier-1 rows; **how
  were those 80 selected** — by crystallographic tier, or by curated state label? And is
  `scripts/derive_per_class_thresholds.py` available?
- **F4.** **Multi-reference receptors.** `PARTA_D2.md:117-126` shows ADRB2 with three
  inactive references (2RH1 / 3NYA / 6PS2) and their individual predicate values. What is
  the selection or aggregation rule — first, best, mean? It is never stated and it moves
  numbers.
- **F5.** What does `refs_build` do? It is named once (`PARTA_D2.md:132`, "would need
  runs of scorer's refs_build pipeline") and never described, yet it produces the anchor
  positions and reference geometry everything else depends on.
- **F6.** **Which reference set applies to which block?** We measure
  `ref_set_csv_sha256 = 6ee2cad8e2d7410a920f72192c12c5abaf2ac55c84b58a4b6ec2b19a965202ef`
  constant on all 32,000 Block B rows, and Block C's README pins the same value; Block D
  reports `7a261988ff73eedc…` (`HEADLINE_D2…:17`). So **Block D used a different
  reference set from Blocks B and C.** What changed between them? This bears directly on
  whether D1 and Block B numbers are comparable — see Q2.
- **F7.** `refs/reference_set.csv` is already requested in Block C ask 5 and Block A
  ask 1; not repeating. But we would like the **generating script or rule** alongside the
  file, which is not part of those asks.

---

## 8. Section G — analysis, rescoring, and statistics

- **G1.** **How does rescoring work?** Are stored rows rescored **in place**, or are all
  quantities **recomputed from the coordinates** every time? The word "rescore" appears
  throughout the Block D headlines with a pass count but no mechanism.
- **G2.** **What happens to rows scored under an older scorer** — are they migrated,
  re-run, or mixed? `GATE_4_SCORER_DIFF.md` exists precisely because a scorer-SHA
  discrepancy appeared across D1 vs D2/D3, and it concluded SAFE. Is there a rule, or is
  it adjudicated per incident? For the redo we would like **one scorer SHA per campaign**
  and a hard failure if a row carries another.
- **G3.** Please send the **rescore driver** — the entry point behind "16 CPU workers"
  and `analysis/full/rescore_parallel.provenance.json`. The command line would do.
- **G4.** **Precision and rounding at each hand-off.** Block B ask 1 already asks for
  `threshold_npxxy_oh_active_lt` at full precision; the general question is where in the
  chain numbers are rounded — at scoring, at CSV write, at aggregation — and to what.
- **G4a.** **Join keys.** `rows_tidy.csv` is assembled by joining `rows.csv` +
  `rows.rmsd.csv` + `rows.pocket.csv` on `input_sha256`, but `rows.fold_integrity.csv` on
  **`input_path`**, because that file carries no per-row sha — and its `# rules:` header,
  which is where its provenance lives, is **stripped on join** (`C-B-3`). Two questions:
  is `input_path` unique per row in every campaign, and can the fold-integrity emitter
  stamp per-row provenance in the redo?
- **G5.** **Where does the paralog-cluster assignment come from?** The shipped
  `data/block_d/09_references/paralogy_clusters.csv` carries, on every row,
  `reconstructed=2026-09-09, reconstruction_source=standard_GPCR_family_taxonomy,
  note="no on-disk canonical map found; Phase 0 addendum cites 26 clusters but ships no
  file"`. So the cluster map used for every cluster-bootstrap CI in the paper was
  **reconstructed after the fact from taxonomy, not from the map used during the run**.
  `rebuttals/BLOCK_B.md` **Q5** puts the consequence plainly: *"If the run and the audit
  resampled different clusters, the intervals are not the ones the analysis was designed
  around."* Does the original map still exist anywhere? (Note the counts also disagree:
  Block A resolves 29 clusters + 16 singletons, Block B and the manuscript say 26, Block D
  reconstructs 22 for its own panel.) For the redo, the cluster map should be an input
  artefact with a hash, not a reconstruction.
- **G5a.** **Layered scorers within one block.** `rows.pocket.csv` was scored under
  `fd87133` while the other 32,000 rows are at `04243c45` (`rebuttals/BLOCK_B.md` **Q6**).
  Confirm nothing in the pocket layer feeds a claim that also depends on the earlier
  scorer — and for the redo, is a single scorer SHA per campaign achievable, or is
  layering structurally necessary?
- **G6.** **Bootstrap implementation.** GATE-2 documents its own clearly — "cluster-
  bootstrap over the 26 receptors used in D3, 1000 replicates, seed 20260910… each
  bootstrap replicate resamples receptors with replacement and re-pools", OLS one slope
  per backbone on `ln(depth)`. Is that the house implementation, and is it in a script?
- **G6a.** **Independence assumptions in the shipped intervals.**
  `g4_full_census_v2.json.pooled.off_site_ci_95_wilson` is `[0.1736, 0.1811]`, and the
  per-arm intervals in `data/block_c/README.md` are the same construction — a Wilson
  interval over 40,000 rows treated as independent when they are 50-sample replicates
  within 800 cells over 36 receptors (`rebuttals/BLOCK_C.md` **Q11**). Confirm the
  construction and we will replace them with cluster-bootstrapped intervals ourselves; we
  are not asking you to redo them. The general question for the redo is: **at what grain
  is a row independent**, and should the delivery contract state the resampling unit
  alongside every interval?
- **G7.** **Interval conventions are not uniform and we would like one.** Within Block D
  alone we can see "Clopper-Pearson-style bootstrap" (`EXPERIMENT_DOSSIER…:55`),
  "Clopper-Pearson" (`PARTA_D2.md:6`) and "Wilson" (`PARTA_D3.md:104`), plus cluster-boot.
  Also: GATE-2's own §7 states its recompute "treats receptors as independent (26, not
  22)" and that a true cluster-boot "would be **wider**", while `PARTA_D3.md:52` labels
  the same numbers "cluster-boot 95 % CI over 22 paralog clusters". We read that as a
  labelling slip in one of the two rather than a numerical error — **which is
  authoritative?**
- **G8.** **Which numbers in the claim sheets are recomputed from rows, and which are
  carried forward from an earlier stage?** This is the PI's explicit question and it is
  the one we most want answered honestly, because it tells us which numbers we can
  re-derive and which we must take on trust. A per-claim-sheet annotation — even just
  "recomputed / carried / hand-computed" against each SC-x — would be enormously
  valuable. We already know of one case where the honest answer is "hand-computed":
  GATE-2 searched for the D3 slope derivation and concluded *"The headline numbers were
  produced by hand or by a one-shot inline computation that was not saved."* That is
  exactly the kind of answer we want, and nobody is going to be criticised for it.
- **G9.** Several analyses ran inline and wrote only to `/tmp` (`PARTA_D1.md:155-159`
  lists `/tmp/d1_frames.pkl`, `/tmp/d1_cis.pkl`, `/tmp/d1_dip.pkl`;
  `PARTA_D2.md:236` lists `/tmp/d2_percell.json`). Do any of those still exist? If not,
  that is a clean UNKNOWN and the redo should make analysis scripts a committed artefact.

---

## 9. Section H — tests and trust: what each check would catch, and what it would not

The PI's framing: **a check that has never fired is not evidence of correctness.**

- **H1.** For each check, guard, gate or assertion in the pipeline, please give four
  things:
  1. what it checks;
  2. **what it would catch**;
  3. **what it would NOT catch** — the failure mode it is silent about;
  4. **has it ever actually fired**, and on what.

  We know some of the answers and they are good ones: GATE-3 fired and forced the
  withdrawal of D3's headline F1; GATE-2 fired partially (Chai's slope CI crossing zero);
  GATE-1 and GATE-4 did not fire as stops but each produced a documentation retraction;
  the "sentinel-seed guard (OF3 audit #13)" fires "when input seed 42 → derived seed
  2746317213" (`HEADLINE_D3…:102-104`); the D3 matched-structure propagation test was
  built specifically because "the config-echo layer has produced false-green propagation
  tests before". That last one is the best example in the whole corpus of the distinction
  we are asking about, and it is yours.
- **H1a.** **The exemplar, so it is clear what a good answer looks like.** Block A's T6
  Part 3 and T7a re-derived both predicate axes from CIF coordinates with from-scratch
  implementations in gemmi + stdlib, **with no import from `scorer/`**, and got median
  |Δ| = 0.0000 Å and Pearson r = 1.000000 on n=41 and n=45 respectively
  (`BLOCK_A_CLAIM_SHEET.md:13-24`, Flag 49). That is a check that **proves** something: an
  independent implementation agreeing to the last digit rules out a whole class of error
  in the two most load-bearing columns in the paper. We would like to know which other
  quantities have that kind of backing and which rest on the single implementation — and
  in the redo we would like to extend it to `pocket_ca_rmsd` and the pLDDT extraction.
- **H1b.** **The counter-exemplar, also from your files.** In the Block C off-site census
  we measure `flag_low_confidence = False` on all 40,000 rows, `receptor_anchor_hits ==
  receptor_anchor_target` on all 40,000, `receptor_chain = A` on all 40,000 and `note`
  empty on all 40,000 (E9c). Four guards, none of which has ever produced a non-default
  value. That may mean the corpus is clean. **What would make each of them fire?** If the
  answer for any of them is "nothing could", we would like to retire it rather than count
  it as evidence.
- **H2.** **The 504-test suite.** `HEADLINE_D3…:109` records "2 new tests, 504-test suite
  green" at commit `9e640d5`. What does it cover — the scorer only, or the dispatch path
  too? Is it run in CI or by hand? Are there golden-file / regression tests that would
  catch a silent numerical change in `pocket_metrics.py`? Please send the test suite, or
  at least the list of test names.
- **H3.** **For each stage, what would a wrong answer look like downstream, and which
  stage would be silent about it?** Worked example of the shape we mean, from your own
  Block A data: the ACM1 / cognate / Protenix cell, 25 rows at mean pLDDT 38.7 with an
  unfolded TM6, carries `passed = True` because the A1–A6 suite has no pLDDT floor. The
  check ran, the check passed, and the cell is broken. We would like the other instances
  of that shape, if you know them.
- **H4.** **What does a green run actually prove?** Concretely: if the campaign completes
  with 100 % pass and no gate fires, which of these are guaranteed and which are merely
  not-disproven — (a) every dispatched input contained the sequence the manifest says;
  (b) every backbone read the MSA it was given; (c) every generic-number anchor resolved
  to the right residue; (d) every reference pair is the intended one; (e) no row is
  duplicated; (f) no row is truncated in transfer.
- **H5.** Is there a check that the **input file handed to the backbone** matches the
  manifest row, byte for byte, at dispatch time? `GATE_1…:61` asserts "the seed is a
  prediction-side parameter; the input sequence file is shared. No per-seed hash drift
  possible by construction" — that is a construction argument. Is it also an executed
  check anywhere?
- **H6.** Is there any duplicate detection — same (receptor, arm, backbone, seed, sample)
  appearing twice in a corpus?

---

## 10. Section I — provenance and identity

- **I1.** **How is a run identified?** There is an `experiments/NNN_name/` convention
  (019 Block B, 022 D1, 023 D2, 024 D3). Is there a run ID beyond the directory name, and
  is it carried into the rows?
- **I2.** **What SHAs are recorded, and of what?** We can see `scorer_git_sha`,
  `scorer_version`, `input_sha256`, `ref_set_csv_sha256`, `cache_key`,
  `thresholds_panel_csv_sha256`, `ref_pdb_sha_active`/`_inactive` — but not all in the
  same block. Please give the canonical list and say what each one hashes (file bytes?
  sequence? normalised sequence?). In particular: **`input_sha256` — of what exactly?**
- **I3.** **What is in a dispatch manifest?** Please send one — e.g.
  `experiments/022_tier_d1_deep_apo/manifest/tier_d1_manifest.csv` (140 rows) or
  `experiments/019_block_b_partner_selection/manifest/manifest.csv` (3,200 rows). Column
  list and a few rows is enough if the whole file is awkward.
- **I4.** **`backbone` is reconstructed from the path in at least one analysis.**
  `GATE_4…:95-98` recovers it by string-matching `boltz|chai|of3|protenix` against
  `input_path` segments. Is there a `backbone` column in the D-tier `rows.csv`, or is the
  path the only source? (Blocks A and B both have one.)
- **I5.** `paper_af3` (working) and `paper_af3_release` — what is the split, and what is
  the rule for what goes into the release repo? Block A ships from tag `block_a_freeze` /
  commit `e433db9`; Block C from "HEAD (see commit landing this bundle)"; Block D's
  `block_d_freeze` and `paper_af3_release/analysis/block_d/` are described as needing
  creation.
- **I6.** Block A's README records "Build scripts: sequential `_build/step*.py` (dropped
  from the shipped zip)". Do those still exist? They are the only description of how the
  Block A bundle was assembled.

---

## 11. Section J — your own verdict

This is the section that usually returns the most value, and we would rather have your
judgement than a defence.

- **J1.** **If you were starting fresh tomorrow, what would you build differently?**
- **J2.** **What in the current setup do you consider fragile?** Not what is broken —
  what you would not want to depend on.
- **J3.** **What has failed silently and been caught late?** You have already published
  several: the v1 census "longest polymer chain ≥ 200 aa" picker that mis-identified Gα as
  the receptor on cognate-arm rows; the phantom scorer SHA propagated across two headline
  documents; the AA2AR fusion-tagged sequence fetched instead of the panel sequence; the
  `constant-seed bug` referenced in `msa_depth_report.md:256`. Are there others, and is
  there a running list? (`ASSUMED_NOT_VERIFIED_BLOCK_D.md` ships in the drop and is close
  to what we mean — is there an equivalent for A, B and C?)
- **J4.** **Which of the four backbones do you trust least, and why?**
- **J5.** **What would you want from us** to make the redo easier? Including anything in
  the way we have been asking for things.
- **J6.** If any part of this document asks for something that does not exist, or asks
  the wrong question about something that does, tell us — that is a useful answer and it
  costs you less than constructing one.

---

## 12. Specific questions we cannot resolve from the shipped bundles

Each of these is verified from your own files, with the path, so you can find it. Each is
a question about what the artefact **means**, not a claim that anything is wrong.

### Q1 — Does `cognate_ga = alphas` in D2 mean Gs was supplied to all four receptors?

`data/block_d/06_gate_reports/GATE_1_D2_NB_SHA.md:35,37,42,44` records
`partner_identity = alphas` on the `cognate_ga` arm for **ACM2, ADRB2, AGTR1 and OPRK**.
ACM2 and OPRK couple Gi/Go; AGTR1 couples Gq/G11. We cannot tell from the drop whether
`alphas` is a generic label for "the Gα partner arm" or whether Gs was literally
supplied to all four, because the D2 audit hashed only the **nanobody** chains (`:59`,
"the chain-B (nanobody) sequence was extracted and hashed") and the D2 `rows.csv` is not
in the bundle.

Either answer is fine and neither is a problem — but they mean very different things for
the D2 result. Block B's cognate routing is explicitly per-receptor (four distinct
identities matched against `refs/gpcr_coupling.csv:primary_ga_identity`, 40/40 OK,
`PHASE_1_CONSTRUCT_IDENTITY.md:41`), so if D2 used a single Gs for all four that would be
a deliberate D2 choice rather than a continuation of B. **What settles it:** the chain-A/
chain-B sequence hashes for the four D2 `cognate_ga` cells, or one sentence.

### Q2 — What exactly differs between D1's "full" and D3's "full" rung?

`data/block_d/02_caveats/C-D-8_opsd_boltz_cross_tier_divergence.md:11-18` reports
OPSD × Boltz-2 apo at **38.8 %** (D1, n=500) and **10.0 %** (D3 full rung, n=50), and
hypothesises that "D3's… `full` rung is NOT bit-identical to D1's upstream default
MSA-mode — D3 sub-samples then re-inflates", marked "hypothesis only", "not verified this
pass".

We have now measured the same cell a third time, independently. **Block B's apo arm gives
30.0 % [19.1, 43.8] (15/50, Wilson 95 %)**, recomputed here from
`data/block_b/01_rows/rows_tidy.csv` by thresholding `d_npxxy_y558_y753_oh` and
`d_gpcrdb_tm6_tilt_246_637_ca` against the two threshold columns — a different campaign
(019 vs 022), a different scorer (`04243c45` vs `d9c646af`), a different panel. That
interval **contains D1 and excludes D3**. Across all 28 shared cells, D1's point estimate
falls inside Block B's 95 % interval on 26 of 28. And if the true rate were D1's 0.388,
observing 5/50 would be a ~3.7σ draw — so undersampling does not account for D3.

We are not asserting D3 is wrong; a per-cell difference is also consistent with the
panel-level agreement you report (D3-full vs Block B apo within 3.2 points on all four
backbones). **What settles it:** a description of what `full` does in the D3 subsampling
pipeline versus an unmanipulated run — specifically whether it re-inflates, re-orders, or
re-fetches. **Until it is settled we are not quoting any depth slope**, so this is
blocking a whole experimental group.

### Q3 — Can realised MSA depth be emitted per row, rather than the rung label?

`GATE_2_D3_SLOPES.md:104-107` states it plainly: *"`full = 4096` is a nominal fitting
choice — the actual full-MSA row count is per-receptor and ranges ~2K–11K"*, and
`HEADLINE_D3…:12` gives the same range. Separately, Block B's own audit records Boltz
consuming **13,678 alignment rows** in the main MSA for the ADRB1 cognate cell
(`data/block_b/03_msa_audit/PHASE_1D_EXTENSION.md:39`) and 6,820 in the paired MSA
(`:67`) — a different object from D3's receptor-only apo depth, which is why we are
asking rather than concluding.

The concern is narrow: the four D3 slopes are `%/ln(depth)` fitted against an x-axis
whose top point is a **single imputed constant** for every receptor, when your own
documents say the realised value is per-receptor and spans a factor of ~5. If the true
top rung is materially above 4,096, every slope is fitted against a wrong highest point.

**What we would like:** a `realised_msa_rows` column per prediction — per chain, if the
input has two — rather than a rung label. You already emit `msa_subsample_seed` per cell,
so the plumbing exists. This is free and it retires Q2 and Q3 together.

### Q4 — `partners.fasta`: were the 25 unconsumed entries ever run?

`data/block_b/03_msa_audit/PHASE_1_CONSTRUCT_IDENTITY.md:13` enumerates
`docs/EXPERIMENT_CATALOG/sequences/partners.fasta` at 29 entries, and `:54` names **25
that no Block B row consumed** — including `ubiquitin` (76 aa), `KaiB_2QKEE` (91),
`gcn4_leucine_zipper_33` (33), `random_helix_40mer` (40), `arrestin_FL` (15),
`arrestin_Ctail` (41), and the two Gs α5 uncoupling mutants
`alphas_F376A_L388A_mutant` and `alphas_F376A_L388A_R380A_triple_null`.

All 25 are hashed and MSA-depth-audited in `msa_depth_report.md:353-378`, so they were at
least prepared. **Were they dispatched in Block A's partner-diversity work and simply not
analysed, or never dispatched at all?**

This is the highest-upside question in the section for us. If runs exist, they already
contain the **mass-matched non-Gα bulk control** and the **helix-length control** that we
were about to ask you to commission — which would turn a `real` experiment into a `free`
one. If they do not exist, the sequences are still built, hashed and audited, so the
control is a dispatch rather than a construction job either way.

(One caution we would apply on both sides: `partners.fasta:GASR` and `partners.fasta:Nb60`
are mislabelled in the header per your own audit, so any re-use should key on sequence
hash. See D6.)

### Q5 — Where do the unshipped row tables live?

Two sets of row-level tables are pinned or named in the drops and present in none of
them. We have checked the filesystem: neither is anywhere in our tree.

- **`rows.tier3.v2.csv`** — pinned by SHA-256 `5ccf58acc8a6b0151250007c6b40d1f728ad4b42c2eeab22bd6509b5809e2103`
  in **21 places across 19 files**, including `data/block_c/README.md:28-29` and ten
  shipped JSONs. It is the primary Block C corpus.
- **Block D's three `rows.csv`** — 42,180 predictions, named by HPC path in
  `data/block_d/10_structures/MANIFEST.json` → `source_rows_csv`
  (`experiments/{022_tier_d1_deep_apo,023_tier_d2_directed_inactive,024_tier_d3_msa_depth}/analysis/full/rows.csv`)
  and in every Block D headline. `HEADLINE_D3…:143` labels its file list "**(this session,
  local only)**".

Block C ask 1 and Block D ask 1 already request these, so **this is not a new ask** — the
question here is different and practical: **are they in `paper_af3_release` rather than
the figure bundles, or only on the MacBook?** `EXPERIMENT_DOSSIER_BLOCK_D.md:260` describes
a planned `MANIFEST_RAW_ROWS.md` pinning them by SHA "per Block C data-in-git-convention:
raw CSVs pinned, not shipped", and `:256` flags
`paper_af3_release/analysis/block_d/` as "MISSING; needs creation". If the convention is
deliberately to pin and not ship, **say so and we will stop asking for them in bundles and
ask for a transfer instead.** Note also that we hold no SHA for the three Block D files at
all, so we could not verify a copy if we had one.

### Q6 — Why is `sample_idx = 5` and `seed = 1015473677` on all five D1 spot-check structures?

Asked at `analysis/block_d/DATA_REQUESTS.md:186`; we have since looked harder and can
narrow it, which may make it a one-word answer.

From `data/block_d/10_structures/MANIFEST.json`, the **spot-check** set is grouped
exactly by tier: all five D1 entries share `seed 1015473677 / sample_idx 5` (job names
carry `seed4`), all four D2 entries share `1291532968 / 0` (also `seed4`), and both D3
entries share `1708630764 / 0` (`seed3`). The **random** set, by contrast, is genuinely
varied across seeds and sample indices, and its top-level `sample_seed` is `20260910`.

That pattern reads clearly as a **deliberate fixed (seed-index, sample-index) pull rule
per tier**, which is what we have assumed. We would just like it confirmed, because the
alternative — a placeholder — would invalidate the comparison D-D-8 draws from those five
structures and we would withdraw it rather than carry it.

### Q6a — Is a D2 cell 50 predictions or 200?

`rebuttals/BLOCK_D.md` **Q3**, and the reason it is still open is that your own caveat
argues both sides in one parenthesis. `C-D-5_agtr1_active_nb_of3_30_short.md:5-11` reads:
*"Canonical D2 grid: (5 seeds × 10 samples) = 50 preds per (receptor, arm, backbone) cell.
Total canonical n per cell = 50 × 4 sample subruns = 200 preds (2 sample subruns per seed
× 10 samples? actually 5 seeds × 10 samples = 50 per cell; but D2 uses 4 fold-multiplier
per cell to reach 200/cell canonical in the dispatch)."* GATE-1's census then shows 200
rows per landed cell. Every shipped interval we can check reproduces at n=50.

We would rather have this from you than pick one: **what is the sampling structure of a D2
cell, and what is the correct denominator for a D2 rate?** And we would like to record
that the honest self-argument in that parenthesis is *why* we can ask the question
precisely — a tidied version would have hidden it.

### Q6b — May a Block C apo × agonist predicate rate be quoted at all?

`rebuttals/BLOCK_C.md` **Q5**, and it is the question with the most riding on it for the
manuscript. Block C is the first block that supplies a ligand: `ligand_type` is NaN on all
32,000 Block B rows and Block A has no ligand column, while Block C carries **7,000 apo ×
full_agonist predictions over 35 receptors** — agonist, no partner — and 7,000 more with
the cognate Gα alongside. SC-C-6 states the predicate floor-pins on apo and ceiling-pins
on cognate, which read plainly *is* the answer, and then declines to quote the rate.

Two instructions appear to block it and they may not be the same instruction: the dispatch
forbids connecting Block C to two-state generation, and Flag C-3 forbids quoting a
binary-predicate rate for a **ligand-class discrimination** claim — which this is not.
**If the answer is still no, we need the reason in one sentence for the Limitations**,
because one of the paper's three title clauses is about the agonist alone, and a silence
about it reads worse than a stated boundary. This is a scoping question for you, not a
number request.

### Q7 — Is `seed` comparable across backbones?

Raised in B4/B5 and repeated here because it is a result-level question, not just an
orchestration one. OF3 paths carry an outer seed and a derived inner seed and a
`chunk_0` layer; the other three carry one seed. If OF3's 100 samples are 4 chunks × 25
with per-chunk derived seeds while Boltz's 100 are one seeded trajectory, then seed-level
and sample-level variance are not the same quantity across backbones — and Block C's
variance decomposition (σ²_seed 0.0004 vs σ²_within-seed 0.0023, ratio 0.11) is
per-backbone-conditional in a way nothing currently states.

### Q8 — Were Block A and Block B seeds paired across arms?

Block A ships `seed_outer`/`seed_inner`; Block B ships `seed_used`. Our Block A open
question C notes seeds are not paired between arms. For the redo, **pairing seeds across
arms within a cell** would remove a variance component from every arm-vs-arm contrast in
the paper at zero extra compute. Is there any obstacle to doing that?

### Q9 — Is `ligand_rmsd_to_ref` populated anywhere in Block D?

`GATE_4_SCORER_DIFF.md:76,105-109` reports 990 populated MCHR1 rows;
`PARTA_D3.md:140-146` then recomputes and finds *"`ligand_rmsd_to_ref` is 100 % NaN across
all 25,810 rows. GATE-4 either observed an earlier state of this file (pre-final-rescore)
or misread its own aggregation"*, and `C-D-11` retracts the 990 claim. We are not
re-raising a resolved item — the question is the **mechanism**: if a gate can read a
pre-rescore state of a file and publish a number from it, what ordering guarantee exists
between rescore completion and analysis? That is a redo-design question.

### Q10 — Which `full` is which in the D3 manifest?

In `MANIFEST.json`, `random_07_d3_npy1r_apo_chai.cif` has `depth: null` and an
`hpc_path` containing `/npy1r/full/chai/`. So the `full` rung is encoded as a path segment
and not as a depth value. Is `depth` null-for-full by design in the row tables too? If so,
any depth analysis that reads the column rather than the path will silently drop the top
rung.

### Q11 — Were the 8 sealed receptors ever unsealed?

`refs/sealed_active_refs_2026_09_01.csv` and the sealed set (ACM1, ADA2A, ADRB1, CCKAR,
DRD3, EDNRA, HRH3, OX2R, per `tier_d3_panel.csv`'s header comment) are described as
"physically moved out of `refs/reference_set.csv` and never accessed by any scoring
step". Block A ask 10 and Block B ask 2 both ask for them to be scored. The question here
is only: **is the seal still intact**, i.e. has any scoring run since 2026-09-01 had those
references available? A yes/no.

---

## 13. The artefact list — "send the file" beats "describe the file"

Everything below is named in your own shipped documents. We have checked each against our
filesystem: **none of these is anywhere in our tree**, except where noted. If any of them
is actually something we already hold under another name, tell us and we will drop it —
an ask for a file we already have costs the credibility of every real ask beside it, which
is why we run `analysis/audit_asks.py` over these documents before sending them.

### 13.1 Code — the highest value per byte

| artefact | why | named at |
|---|---|---|
| `scorer/pocket_metrics.py` | every distance, RMSD, pocket and ligand metric; `POCKET_BW_LABELS` at :81-86 | `BLOCK_B_ITEM3…:15,69`; `GATE_4…:44` |
| `scorer/bw_numbering.py` | BW → UniProt position mapping, the campaign's canonical BW source | `BLOCK_B_ITEM3…:32` |
| `refs/cache/gpcrdb/residues_ext_<slug>.json` | the cached GPCRdb `residues/extended/` records the mapping reads | `BLOCK_B_ITEM3…:31,182-183` |
| `scorer/axes.py` | the predicate axes; unchanged across both scorer SHAs | `GATE_4…:62` |
| `scorer/anchors.py` | generic-number → residue mapping | `GATE_4…` diff table |
| `scorer/references.py` | reference selection and loading | `GATE_4…` diff table |
| `scorer/propose.py` | per-backbone input generation (`materialise_inputs`, `_row_input_content`, `_partner_fasta`, `_BACKBONE_EXT`, `_boltz_yaml_two_chain`, `_of3_query_dict`, `_protenix_ligand_entry`, `msa_a3m_path` kwarg) | `construct_build_report.md:202-208`; `GATE_4…:64` |
| `scorer/_version_sha.py` | how the SHA stamp is produced | `GATE_4…:19` |
| `qsub/rerun_boltz.sh`, `rerun_chai.sh`, `rerun_of3.sh`, `rerun_protenix.sh` | inference config, template flags, MSA routing | `BLOCK_B_CLAIM_SHEET.md:301-304`; `HEADLINE_D3…:137` |
| `qsub/colabfold_shim.py` | the MSA fetch for OF3 | `PHASE_1D_EXTENSION.md:93,128` |
| `scripts/queue_ops.py` | per-row env plumbing, dispatch | `HEADLINE_D3…:138` |
| `scripts/subsample_msa.py`, `scripts/clean_a3m.py` | the depth ladder and a3m normalisation | `HEADLINE_D3…:13,95` |
| `scripts/build_manifest.py`, `build_block_a_manifest.py` (+ `CONDITION_PRESETS`) | how a campaign grid becomes rows | `construct_build_report.md:216-221` |
| `scripts/build_shuffled_decoy_constructs.py` | the decoy/shuffled construction | `construct_build_report.md` |
| `scripts/derive_per_class_thresholds.py` | where 9.082 and 14.932 come from | drop references |
| `scripts/rescore_rmsd.py`, `scripts/merge_of3_rerun_rows.py`, `scripts/rebuild_block_a.py`, `scripts/ledger_check.py` | the rescore and rebuild path | drop references |
| `_build/step*.py` | how the Block A bundle was assembled | `data/block_a/README.md:14` |
| the 504-test suite (or its test-name list) | H2 | `HEADLINE_D3…:109` |

`analysis/block_d/scripts/derive_d3_slopes.py` is **not** on this list: `GATE_2…:15-28`
establishes it does not exist, and Block D ask 11 already covers it.

`scripts/block_c_closeout/g4_full_census_v2.py` is **not** on this list either — you
shipped it inside `data/block_c/12_g4_off_site_census/`, and it is the single most useful
artefact in all four drops for understanding the scoring. **More of exactly that, please.**

### 13.2 Reference and specification files

| artefact | why |
|---|---|
| `docs/BW_SOURCE.md` | the generic-numbering source (E1) |
| `refs/PREREG.md` (incl. §C-5, §11c-d, §14, §D-1/2/3 and amendments) | quoted constantly; never shipped |
| `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` + `receptors.fasta` | Q4, C9. Block B ask 6 touches `partners.fasta` for a different purpose |
| `refs/gpcr_coupling.csv` | already in Block A ask 11 — listed for completeness only |
| `refs/panel_receptor_sequences.fasta`, `refs/constructs_block_b/*.fasta` + `build_manifest.csv` | construct identity |
| `refs/tier3_panel.csv` | the 40 Class A panel of record, referenced by the tier panels we hold |
| the thresholds panel CSV, sha `242b509f7b7af56669d72cd71906d91edd18ef43706c21d23a8be5bf1e08366b` | pinned per row as `thresholds_panel_csv_sha256`; the file itself ships nowhere |

**We already hold these — please do not resend:**
`data/block_d/09_references/{nanobody_sequences.fasta, nanobody_state_anchors.csv,
tier_d1_panel.csv, tier_d2_panel.csv, tier_d3_panel.csv, paralogy_clusters.csv}`;
`data/block_b/09_references/{reference_set.blockb_pinned.csv, reference_audit.csv,
native_gs_curation_audit.csv, paralogy_clusters.csv}`;
`data/block_a/02_references/{reference_predicates.csv, reference_metadata.csv,
reference_separation.csv, denominator_populations.csv}`;
`data/block_c/12_g4_off_site_census/g4_full_census_v2.py`.
| `experiments/024_tier_d3_msa_depth/spec/D3_BACKBONE_PLUMBING_SPEC.md` | the `MSA_A3M_PATH` design; directly relevant to Q2/Q3 |
| one dispatch manifest, e.g. `experiments/022_tier_d1_deep_apo/manifest/tier_d1_manifest.csv` | I3 |
| `experiments/024_tier_d3_msa_depth/analysis/verification/matched_structure_probe_final.json` | the one propagation test that cannot be faked by the config-echo layer |
| an example `inference_query_set.json` (OF3) | it records per-chain query bytes and MSA hash keys; the only retained OF3 input record |

### 13.3 Would a template help?

Yes, for three things, and we will supply them (see §14): a **row-schema contract**, an
**environment manifest**, and a **per-check trust table** in the H1 four-column shape. If
you would rather fill in a form than write prose for §2, §6 and §9, say so and we will
send the forms first.

---

## 14. What we will send you

Offered up front so that you are not being measured against a standard you have not seen.

1. **Our verifier scripts.** `analysis/block_a/verify_claims.py` and its siblings — the
   code that recomputes every checkable number in each claim sheet from the tidy files.
   You will be able to see exactly which of your numbers we re-derive and how.
2. **The recalibration method** we intend to use for the predicate, including the
   balancing rule for the calibration population, before it is fitted.
3. **The acceptance tests** we intend to run on the new campaign's outputs — ideally
   agreed with you *before* the campaign runs rather than discovered afterwards. This is
   the row-level delivery contract idea: an agreed column list, an agreed NaN policy, and
   an agreed set of columns that must be present for a row to be analysable.
4. **`analysis/audit_asks.py`**, the tool we run over our own request documents to catch
   asks for files we already hold. It has a documented false-positive history and we would
   rather you see that than assume our lists are machine-verified when they are only
   partly so.
5. **Our recomputations**, whenever they disagree with a drop — with the filter and the
   one-line reproduction, so you can disagree with us the same way. Including, explicitly,
   the cases where we were wrong; several of the entries in our discrepancy reports are
   our own parsing bugs and they are labelled as such.
6. **Two construct errors we found in our own documents**, so they do not propagate into a
   dispatch: the 21-mer residue-range error in D2 above, and a slug-mapping error where
   `GCGR` and `CRHR1` do not resolve in GPCRdb by lowercasing (they are `glr_human` and
   `crfr1_human`), which silently drops them from any panel join.

---

## 15. What this document deliberately does not ask

- **The 62 numbered asks already in flight** (Block A 15, Block B 17, Block C 18, Block D
  12, in `analysis/block_*/DATA_REQUESTS.md`) are **not repeated here.** Where a question
  above touches one of them, it says so and asks the different question. If those
  documents have not reached you yet, they should go first — many are `free`, and every
  Block C ask is free because the numbers are already computed and sitting in files that
  were not zipped.
- **Scientific interpretation.** Nothing above asks what a result means. That conversation
  is better had once the blueprint is settled.
- **Anything we can compute ourselves** from the row data we already hold — 9,490 Block A
  rows and 32,000 Block B rows are complete and we are not asking you to re-derive
  anything from them.
- **Commitments and dates.** Nothing here is a deadline and nothing here commits anyone to
  a scope. The PI decides what the redo runs; this document only aims to make that
  decision an informed one.

---

## 16. An open invitation — please tell us what we did not know to ask

We hope the questions above make clear what kind of setup we are trying to build: **clean,
simple, and reproducible end to end** — a campaign where the blueprint is an artefact
rather than a reconstruction, where a number in a table can be walked back to the
coordinates it came from, and where the checks that guard it have all fired at least once
in testing.

Everything we have asked is shaped by what we could see from the delivered bundles and our
own reconstruction. **That is a real limit.** You know where the bodies are and we do not,
and the most valuable thing in your reply may well be something that appears nowhere in
this document because we did not know it existed. So, explicitly and sincerely: **if you
see anything else that would help explain the paper, or that we clearly did not know to
ask about, we would very much appreciate having it.**

Concretely, the kinds of thing we mean:

- **Scripts or notebooks we have not asked for** — including one-offs, including ones that
  only ran once.
- **Intermediate files that explain a step.** A file that shows what a stage produced
  before the next stage consumed it is often worth more than the stage's description.
- **Anything you built and abandoned, and why.** An arm that was designed and never
  dispatched, a metric that was computed and dropped, a panel that was drafted and
  replaced. The reasons are usually good and they are invisible from the outside.
- **Any place where the shipped summary and your own working notes diverge.** We would
  much rather hear it from you than find it — and we would rather find it than have it
  reach a reviewer.
- **Conventions that are obvious to you and invisible to us.** Directory grammars, naming
  rules, what a suffix means, which of two similarly-named files is the real one, what
  "full" means in a path segment. Several of the questions above exist only because a
  convention was never written down, not because anything was wrong.
- **Anything you would tell a new member of your own team on day one.** That is close to
  exactly what we are asking for.

**A partial or messy answer sent early is worth more to us than a polished one sent
late.** We would genuinely rather receive a script with a comment saying *"this bit is a
hack"* than a tidied version that no longer matches what ran — the hack is information and
the tidy version is not. Same for a half-finished section, a bullet list instead of prose,
or a screenshot of a terminal. None of this needs to be presentable.

And this runs both ways. As set out in §14, we will send our verifier scripts, the
recalibration method, and the acceptance tests we intend to run — before you produce the
outputs they will be run against — so that you can see what is being checked and tell us
where the check itself is wrong. If our tests encode an assumption you know to be false,
we would much rather find that out now.

---

## Appendix — how we verified the citations in this document

Every file path asserted above as *absent* was checked against the filesystem; every path
asserted as *present* was opened. The numeric claims we make about your data were
recomputed here rather than quoted:

- OPSD × boltz × apo in Block B: n=50, k=15, **30.0 %**, Wilson 95 % **[19.1, 43.8]**,
  from `data/block_b/01_rows/rows_tidy.csv` thresholding `d_npxxy_y558_y753_oh <
  threshold_npxxy_oh_active_lt` AND `d_gpcrdb_tm6_tilt_246_637_ca >
  threshold_gpcrdb_tm6_tilt_active_gt`.
- `scorer_git_sha` is constant at `04243c45…` on all 9,490 Block A rows and all 32,000
  Block B rows; `ref_set_csv_sha256` is constant at `6ee2cad8…` on all 32,000 Block B rows.
- `5ccf58ac…` occurs 21 times across 19 files in our tree; `rows.tier3.v2.csv` and all
  Block D `rows*.csv` are absent from it.
- The `MANIFEST.json` seed/sample groupings in Q6 were read directly from the JSON.

Where a number in this document came from one of our own internal documents rather than
from your files, we went back to your file and re-derived it. Two of our own errors were
caught that way and are recorded here rather than quietly fixed, because §0.3 would be
worth nothing if we only applied it to you:

- An internal note cited the 13,678-row Boltz MSA figure to `msa_depth_report.md`. It is
  not there; it is at `PHASE_1D_EXTENSION.md:39`, written as `13 678` with a thin space,
  which is why a naive grep missed it. The number is yours and correct; our citation was
  wrong.
- A path-existence audit over this document's own citations caught us about to ask for two
  files we already hold — `nanobody_sequences.fasta` and `tier_d1_panel.csv`, both shipped
  in `data/block_d/09_references/`. Both asks were removed and §13.2 now carries an
  explicit do-not-resend list. This is the check `analysis/audit_asks.py` exists to run,
  and it is one of the scripts we are offering in §14.

If anything here still misreads one of your artefacts, that is our error and we would like
to be told.
