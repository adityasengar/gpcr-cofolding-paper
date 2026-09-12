# MAP_LIFECYCLE.md — the life of one prediction, end to end

**Framing: REPRODUCTION, not audit.** Everything below is written so that someone
holding `paper_af3`'s repo and their cluster can take one receptor and one partner,
reproduce a single prediction, and then scale to a matrix without discovering a new
decision at every stage. Where their code contains a defect, it is recorded because
**the redo must put a guard there before spending**, not as a criticism of a finished
campaign.

**Source.** Their complete source tree at
`redo/protocol/received/source_bundle/`, plus the reference files in
`redo/protocol/received/`. Every claim carries `file:line`. Paths written bare
(`scorer/propose.py:787`) are relative to `source_bundle/`; paths written
`received/...` are the loose reference files.

**Rule followed throughout:** every apparent discrepancy was treated as our own
checker bug first. §11 records what was checked and turned out **not** to be a
finding.

---

## 0. The one-paragraph summary

A campaign starts as a **grid declaration in a Python builder** (`scripts/build_tier_d1_manifest.py`
and its siblings), not as a YAML request. The builder resolves receptor sequences from a
FASTA, derives seeds from a salted SHA-256, calls one of ten pure templater functions per
backbone to produce the model input file's *content as a string*, writes it, sha256s it,
and emits a 34-column manifest CSV — one row per `(receptor × arm × backbone × seed)`.
That manifest becomes a queue. A worker claims a queue row under an `flock`, exports five
to seven `PRED_*` environment variables, and runs `qsub/rerun_<backbone>.sh` — which is an
SGE job script but in the production path is executed **inline inside an already-running
`qrsh` session**, so its `#$` resource directives are inert. The launcher invokes the
backbone CLI once (OF3: once per 25-sample chunk), then calls `qsub/status_writer.py`,
which writes `_<backbone>_status.json` next to the outputs. That JSON, the `_rerun_plan.json`
sidecar, the copied `_input_used.*`, and a deep per-sample directory tree are what lands
on disk. Scoring is a separate later pass (`scorer/orchestrator.py`) that re-discovers
provenance by **parsing the output path** when the sidecar is absent.

---

## 1. Two dispatch paths, and you must know which one you are on

This is the first thing to fix in your head, because almost every question below has two
different answers.

| | **Path A — supervisor** | **Path B — worker pool** |
|---|---|---|
| driver | `scorer/supervisor.py` (long-lived process on the submit host) | `scripts/{block_a,block_b,h100}_worker.sh` inside tmux + `qrsh` |
| unit of work | one `qsub` per manifest row | one claimed queue row per worker iteration |
| state | `refs/rerun_status.csv` (`scorer/supervisor.py:64-76`) | `<pool>/queue.csv` + `<pool>/queue_state.csv` (`scripts/queue_ops.py:34-42`) |
| retries | automatic, ≤2 (`scorer/supervisor.py:328`) | **none automatic** — `failed` is terminal |
| completion test | `_<bb>_status.json` `ok == true` (`scorer/supervisor.py:560-565`) | launcher shell exit code only (`scripts/block_a_worker.sh:116`) |
| writes `_rerun_plan.json` | **yes**, before qsub (`scorer/supervisor.py:509-513`) | not on every tier — see §5.3 |
| resources come from | the `#$` block in the launcher | the `qrsh -l` line in `qsub/dispatch_*.sh` |

Both paths end at the same four launcher scripts and the same status writer. **Blocks A–D
production ran Path B.** Path A is the M2.3-era rerun supervisor. If the redo dispatches
through their harness, pick one and say so in writing — the two disagree about what
"done" means (§5.5).

---

## 2. How an input is constructed

### 2.1 The trace, in order

```
receptor slug
   │  ① sequence source
   ▼
receptor sequence string  ──┐
partner sequence string ────┤  ② templater (one of ten)
ligand type/seq/smiles  ────┘
   │
   ▼  a STRING (file content), pure function of its arguments
write_text() to <inputs_dir>/<backbone>/<request_id>.<ext>
   │  ③
   ▼
sha256(content) ──────────► manifest column `input_sha`
```

### 2.2 ① Sequence source — there are three, and they disagree

| route | function | source | used by |
|---|---|---|---|
| **GPCRdb WT** | `_wt_receptor_fasta` (`scorer/propose.py:279-317`) | live/cached GPCRdb `get_generic_numbers`, reconstructed residue-by-residue from the BW map (`:309-317`) | the `gpcr-propose` YAML route |
| **panel FASTA** | `_parse_fasta` on `refs/panel_receptor_sequences.fasta` (`scripts/build_tier_d1_manifest.py:172-185`, `:218`) | a committed file, 51 entries | **every Block/Tier campaign builder** |
| **inline override** | `spec["receptor_sequence_fasta"]` (`scorer/propose.py:933-935`) | the analyst's YAML | constructs, thermostabilised variants, chimeras |

`_wt_receptor_fasta`'s docstring is explicit that it **deliberately does not** read the
construct FASTA, because those carry FLAG tags, signal peptides and thermostabilising
mutations (`scorer/propose.py:287-292`). The campaign builders take the opposite decision
and read the construct FASTA directly. **For a reproduction this matters: you will not get
the same sequence from the two routes.** If you reproduce one Tier D1 cell, use
`refs/panel_receptor_sequences.fasta`; the OPSD chain-A sequence actually dispatched is the
348-residue string in `received/_input_used.tier_d1_opsd_apo_boltz_seed2.yaml:5`.

Partner sequences come from one place: `_partner_fasta` (`scorer/propose.py:320-334`),
reading `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` (path constant at `:76`), keyed
by the first `|`-separated token of the header and tried in three casings (`:331-333`). The
copy we hold is `received/partners.fasta` (28 entries). An unresolvable identity raises
`SpecError` (`scorer/propose.py:964-970`) — it does **not** silently fall through to apo.

### 2.3 ② The ten templaters

All ten are pure functions of their sequence arguments and return the file **content as a
string**; the caller writes it and hashes it (`scorer/propose.py:346-350`). This is the
single most reusable property in their design — it makes an input byte-reproducible
without a cluster.

| # | templater | `file:line` | backbone | chains | emits |
|---|---|---|---|---|---|
| 1 | `_boltz_yaml_monomer` | `scorer/propose.py:373-381` | Boltz | A | `version: 1` + one `protein:` entry |
| 2 | `_boltz_yaml_two_chain` | `scorer/propose.py:384-397` | Boltz | A, B | two `protein:` entries |
| 3 | `_of3_json_monomer` | `scorer/propose.py:515-528` | OF3 | A | `{seeds:[N], queries:{name:{chains,…}}}` |
| 4 | `_of3_json_two_chain` | `scorer/propose.py:531-542` | OF3 | A, B | same, `use_paired_msas: true` |
| 5 | `_protenix_json_monomer` | `scorer/propose.py:603-611` | Protenix | A | `[{name, sequences:[{proteinChain:{sequence,count}}]}]` |
| 6 | `_protenix_json_two_chain` | `scorer/propose.py:614-625` | Protenix | A, B | two `proteinChain` entries |
| 7 | `_chai_fasta_monomer` | `scorer/propose.py:651-653` | Chai | A | `>protein\|name=<n>` FASTA |
| 8 | `_chai_fasta_two_chain` | `scorer/propose.py:656-662` | Chai | A, B | two `>protein\|name=` records |
| 9 | `_af2mm_fasta_monomer` | `scorer/propose.py:665-667` | AF2-multimer | A | bare-header FASTA |
| 10 | `_af2mm_fasta_two_chain` | `scorer/propose.py:670-671` | AF2-multimer | A, B | two bare headers |

**Five monomer (1,3,5,7,9) and five two-chain (2,4,6,8,10) — exactly as reported.**

**Which is used when.** The switch is `_row_input_content` (`scorer/propose.py:687-746`).
It selects on `backbone` and on a single boolean `apo`:

```python
apo = _partner_is_apo(partner_type, partner_identity)   # propose.py:947
```
`_partner_is_apo` (`scorer/propose.py:674-679`) is true when `partner_type == "apo"` **or**
both `partner_type` and `partner_identity` are empty. Apo → monomer templater; anything
else → two-chain templater, with the partner on chain B.

Three further facts a reproducer needs:

- **There is no three-chain templater.** Every two-chain function is hardcoded to exactly
  `A` and `B` (`scorer/propose.py:534-537`, `:617-620`). A heterotrimer cannot be expressed.
- **Ligands are a fourth chain appended after the fact**, chain id `L`, by a separate
  family of helpers — `_boltz_ligand_block` (`:400-428`), `_of3_ligand_chain` (`:492-512`),
  `_protenix_ligand_entry` (`:545-571`), `_chai_ligand_fasta` (`:628-648`). A **peptide**
  ligand becomes a `protein:`/`PROTEIN`/`proteinChain`/`>protein|name=lig` record — so a
  peptide ligand is a third protein chain in every backbone but AF2-mm, which has no ligand
  support at all.
- **An eleventh path exists and is not in the ten:** `_receptor_nb_content`
  (`scorer/propose.py:749-779`), the Tier D2 nanobody branch. It introduces no new schema —
  it calls templaters 2, 4, 6 and 8 — but it is a separate dispatch entry point. AF2-mm is
  not supported there (`:779`).

**Small-molecule partners are refused**, not templated: `materialise_inputs` raises
`SpecError` for `partner.type` in the small-molecule family (`scorer/propose.py:948-957`,
predicate at `:682-684`). Small molecules can only enter as a *ligand*, never as the
partner.

### 2.4 MSA plumbing is an input-file property, not a CLI flag

Three of the four backbones take pre-fetched MSAs by having paths **written into the input
file**, not by a launcher argument:

| backbone | field written | function |
|---|---|---|
| Boltz | `      msa: <path>` inside the chain entry | `_boltz_msa_field` (`scorer/propose.py:353-370`) |
| OF3 | `main_msa_file_paths` + `paired_msa_file_paths` (a **directory**, not a file — `:470`) | `_of3_apply_msa_paths` (`:431-472`) |
| Protenix | `unpairedMsaPath` + `pairedMsaPath` on each `proteinChain` | `_protenix_apply_msa_paths` (`:574-600`) |
| **Chai** | **none — no MSA field exists in the Chai FASTA** | — |

Chai's MSA arrives only through `--msa-directory`, a content-addressed cache
(§4.4, §9.1). Every one of the three path-writing functions is a **no-op when
`msa_a3m_path` is falsy** (`:362-363`, `:453-454`, `:587-588`), and the default is falsy —
so the default for Blocks A–D was **live ColabFold server fetch at inference time**. The
OPSD Boltz input we hold has no `msa:` line (`received/_input_used.tier_d1_opsd_apo_boltz_seed2.yaml`,
4 lines total), confirming live fetch for that cell.

### 2.5 ③ The sha256, and the seed that enters the file

`input_sha = content_sha256(input_path)` — a streaming SHA-256 of the file bytes, which
raises rather than swallowing a missing file (`scorer/cache.py:24-36`). The campaign
builders hash the string directly before writing (`scripts/build_tier_d1_manifest.py:262-263`).
Same value either way.

**The seed is inside the OF3 input file and nowhere else.** `_of3_query_dict` writes
`"seeds": [seed]` (`scorer/propose.py:478-479`), and `_of3_json_monomer` / `_of3_json_two_chain`
take `seed` as a positional argument. Boltz, Protenix, Chai and AF2-mm templaters take no
seed at all. Consequence for reproduction: **the OF3 input file's sha256 changes with the
seed; the other three backbones' do not.** And per `refs/of3_seed_bug_mechanism.md:37`, the
OF3 query-JSON `seeds:` field **only names an output subdirectory** — it does not reach the
sampler. So the one file that carries a seed is the one where the seed is decorative.

### 2.6 Where the seed actually comes from

Two derivations, both SHA-256, both deterministic, and they are **not the same function**.

**Campaign builders — a salted per-index seed** (`scripts/build_tier_d1_manifest.py:147-154`):

```python
_SEED_SALT = "tier_d1_2026_09_06"
_h = hashlib.sha256(f"{_SEED_SALT}_seed_{_i}".encode()).digest()
CANONICAL_SEEDS.append(int.from_bytes(_h[:4], "big") % (2**31))
```

Verified locally — the five Tier D1 seeds are
`1965127769, 1060594406, 1800878580, 1330640762, 1015473677`. Seed index 4 → `1015473677`,
which is exactly the `seed` field and the `seed_1015473677/` directory in
`received/_of3_status.json`. Seed index 2 → `1800878580`, matching the Boltz output path in
`received/rows_csv_line.txt`. **The seed derivation is confirmed against real dispatched
artefacts.**

The same seed value is used for **every receptor, every arm and every backbone** at that
seed index — the loop at `scripts/build_tier_d1_manifest.py:245` enumerates
`CANONICAL_SEEDS` inside the receptor/arm/backbone loops. That is a deliberate
cross-backbone pairing and worth preserving.

**Proposal route — a composite-key seed** (`scorer/propose.py:787-793`):

```python
composite = f"{request_id}|{backbone}|{seed_index}".encode("utf-8")
sha = hashlib.sha256(composite).hexdigest()
return fresh_seed_for(sha)
```
with `fresh_seed_for(hex) = int(hex[:8], 16) & 0x7fffffff` (`scorer/rerun.py:749-751`).
Here backbone *does* enter, so the same seed index gives different seeds per backbone.

**The redo must choose one and state it.** They are incompatible conventions and both are
live in the same tree.

---

## 3. How a job is launched

### 3.1 Scheduler and resources

**SGE/UGE.** All directives are `#$`; the code reads `SGE_HGR_gpu_card`
(`qsub/rerun_boltz.sh:42`), `JOB_ID`, and `TMPDIR=/scratch/tmp/$JOB_ID.$SGE_TASK_ID.$queue`
(`scripts/block_b_worker.sh:136-137`). Submission is `qsub` (Path A) or `qrsh` (Path B).

| launcher | `-N` | `h_rt` | `m_mem_free` | `-pe smp` | gpu | `file:line` |
|---|---|---|---|---|---|---|
| Boltz | `pa3_boltz_rerun` | 04:00:00 | 8G | 4 | `gpu_card=1` | `qsub/rerun_boltz.sh:26-33` |
| Chai | `pa3_chai_rerun` | 06:00:00 | 8G | 4 | `gpu_card=1` | `qsub/rerun_chai.sh:21-28` |
| OF3 | `pa3_of3_rerun` | 05:00:00 | 16G | 4 | `gpu_card=1` | `qsub/rerun_of3.sh:21-28` |
| Protenix | `pa3_ptx_rerun` | 05:00:00 | 16G | 4 | `gpu_card=1` | `qsub/rerun_protenix.sh:20-27` |
| AF2-mm | `pa3_af2mm_rerun` | 08:00:00 | 16G | 8 | `gpu_card=1` | `qsub/rerun_af2mm.sh:23-30` |

No `-q` in any launcher; the only queue reference is the comment `# mandatory on default.q`
(`qsub/rerun_boltz.sh:32`). No `gpu_arch` constraint in any launcher.

**These numbers are inert in the production path.** `scripts/block_b_worker.sh:158` runs
`bash "$REPO/qsub/rerun_${BACKBONE}.sh"` inside an existing `qrsh` session. The effective
resource line is in the dispatch script, e.g.
`qrsh -q default.q -l h_rt=$H_RT,gpu_card=1,gpu_arch=hopper_h100,m_mem_free=32G`
(`qsub/dispatch_tier1.sh:83`). **32G, not 8/16G; `gpu_arch=hopper_h100`, which the launcher
never asks for.** Reproduce from the `qrsh` line, not the `#$` block.

Module loads differ: Boltz/Chai load only `proxy/GLOBAL` (`qsub/rerun_boltz.sh:38`,
`qsub/rerun_chai.sh:47`); Protenix adds `CUDA/12.1.1` (`qsub/rerun_protenix.sh:33`); AF2-mm
loads `AlphaFold/2.3.2-foss-2023a-CUDA-12.1.1` (`qsub/rerun_af2mm.sh:36`).

### 3.2 No array jobs. A persistent worker pool instead.

`grep '^#\$ -t' qsub/` and `grep -- '-tc '` both return nothing. There are **no SGE array
jobs and no scheduler-level throttle anywhere in the bundle.** Concurrency is set entirely
by how many tmux windows the dispatch script opens, each holding one long-lived `qrsh`
running a queue-draining worker (`qsub/dispatch_tier1.sh:83-93`):

```bash
tmux new-session -d -s "$POOL_NAME" -n "w0"
tmux send-keys -t "$POOL_NAME:w0" "$ENV_EXPORT && $QRSH_H100 bash $WORKER w0" Enter
for i in $(seq 1 $((N_H100 - 1))); do ... done
```

| dispatch script | workers | `h_rt` | arch | `file:line` |
|---|---|---|---|---|
| `dispatch_smoke.sh` | 25 H100 | 04:00:00 | hopper_h100 | `:33-34, :80` |
| `dispatch_tier1.sh` | 25 H100 | 12:00:00 | hopper_h100 | `:36-37, :83` |
| `dispatch_tier3.sh` | 25 H100 + 10 A100 | 24:00:00 | hopper_h100 / ampere_a100 | `:50-52, :99, :113` |
| `dispatch_tier_d1_smoke.sh` | 6 H100 | 04:00:00 | hopper_h100 | `:31-32, :84` |
| `dispatch_tier_d2_full.sh` | 12 H100 | 04:00:00 | hopper_h100 | `:39-40, :92` |
| `dispatch_tier_d3_smoke.sh` | 25 H100 | 04:00:00 | hopper_h100 | `:39-40, :92` |

The A100 pool is boltz-only, and that restriction is enforced **in the worker**, not the
scheduler — a non-boltz row claimed by an A100 worker is released back to `pending`
(`scripts/block_b_worker.sh:105-112`).

### 3.3 Seeds, per backbone — the flag each one actually takes

One seed per job everywhere. `PRED_SEED` passes through unmodified in four of five.

| backbone | flag | `file:line` |
|---|---|---|
| Boltz | `--seed "$PRED_SEED"` | `qsub/rerun_boltz.sh:130-136` |
| Chai | `--seed "$PRED_SEED"` | `qsub/rerun_chai.sh:197-204` |
| Protenix | `--seeds "$PRED_SEED"` — **plural** | `qsub/rerun_protenix.sh:112-118` |
| AF2-mm | `-r "$PRED_SEED"` (→ `--random_seed`) | `qsub/rerun_af2mm.sh:74-82` |
| **OF3** | **no seed flag at all** — see §3.5 | `qsub/rerun_of3.sh:80-94` |

The Protenix plural is not cosmetic. `qsub/rerun_protenix.sh:90-95` records that
`--seed` (singular) made `protenix pred` exit immediately on an argparse error, **"which the
M2.4 supervisor logged as a permanent failure."** A flag-name typo was indistinguishable
from a scientific failure. Copy the plural.

Boltz's comment is worth carrying too: `--seed` "takes precedence over any seed baked into
the input YAML" (`qsub/rerun_boltz.sh:107-108`).

### 3.4 Sample counts and chunking

`N_SAMPLES="${PRED_SAMPLES:-1}"` in all four (`qsub/rerun_boltz.sh:115`,
`rerun_chai.sh:122`, `rerun_protenix.sh:97`, `rerun_of3.sh:95`). It reaches the model as
`--diffusion_samples` (Boltz), `--num-diffn-samples` (Chai), `--sample` (Protenix),
`--num-diffusion-samples` (OF3). AF2-mm has no sample-multiplicity flag at all.

**Only OF3 chunks.** `grep chunk` over the other three launchers returns zero hits. OF3
splits because of a hard Triton limit, documented in the launcher
(`qsub/rerun_of3.sh:138-145`):

> OF3's fused evoformer attention kernel fails with "Triton Error [CUDA]: invalid argument"
> when `--num-diffusion-samples` exceeds ~25 on typical GPCR sequences (~350 aa + 150-row
> MSA). Ceiling bracket 2026-09-06 (Tier D1 CNR2 apo): n=25 → ok=True 25 CIFs; n=50 →
> ok=False 0 CIFs.

`OF3_MAX_PER_CALL="${OF3_MAX_PER_CALL:-25}"` (`:159`); `N_CHUNKS = ceil(N/25)` (`:173`).
Tier D1's 100 samples therefore become **four OF3 calls**, each writing its own
`chunk_<i>/` subdirectory (`:183`). This is the single largest asymmetry between backbones
and it changes the output tree shape (§6.2).

### 3.5 The OF3 inner seed — **RESOLVED**

This was the known gap. The previous reading implemented
`random.seed(PRED_SEED); randint(0, 2**32-1)` from `received/rerun_of3.d9c646af.sh:100-113`,
got `945550830` for outer seed `1015473677`, and could not match the observed `2344327426`
(`CLAIM_VS_CODE.md:699-708`).

**The formula is per-chunk, and it is in the version of the launcher that shipped in this
bundle but not in the snapshot previously sent.** `qsub/rerun_of3.sh:185-198`:

```bash
        # Deterministic sub-seed per chunk from PRED_SEED
        CHUNK_YAML="$CHUNK_DIR/_runner_seeds.yml"
        python3 - "$PRED_SEED" "$CHUNK_IDX" "$N_SEEDS" "$CHUNK_YAML" <<'PY'
import random, sys
from pathlib import Path
pred_seed  = int(sys.argv[1])
chunk_idx  = int(sys.argv[2])
n_seeds    = int(sys.argv[3])
out        = Path(sys.argv[4])
random.seed(pred_seed * 1_000_003 + chunk_idx)
seeds = [random.randint(0, 2**32 - 1) for _ in range(n_seeds)]
out.write_text("experiment_settings:\n  seeds: " + repr(seeds) + "\n")
PY
```

**Verified against all four chunks of the one OF3 cell we hold.** With
`PRED_SEED = 1015473677`:

| chunk | computed `random.seed(1015473677*1_000_003 + c)` → first `randint(0,2**32-1)` | directory in `received/_of3_status.json` |
|---|---|---|
| 0 | `2344327426` | `chunk_0/…/seed_2344327426/` ✔ |
| 1 | `4017696312` | `chunk_1/…/seed_4017696312/` ✔ |
| 2 | `2650761416` | `chunk_2/…/seed_2650761416/` ✔ |
| 3 | `108204258` | `chunk_3/…/seed_108204258/` ✔ |

Four of four. **The gap is closed and no question needs to be asked.**

Why the earlier attempt failed: `received/rerun_of3.d9c646af.sh` — the snapshot at commit
`d9c646af` — has **no chunking block at all**; `diff` against the bundle's copy shows the
whole `OF3_MAX_PER_CALL` / `N_CHUNKS` region as added. The formula the previous reading
implemented (`random.seed(PRED_SEED)` with no chunk term) is the **unchunked fast path**,
still present at `qsub/rerun_of3.sh:99-113`, and it is only reached when
`N_SAMPLES <= 25`.

**Two consequences that matter more than the formula.**

1. `pred_seed * 1_000_003 + chunk_idx` is **not injective over the intended domain in the
   ordinary sense, but is safe here**: with `chunk_idx < 1_000_003` the map is injective, and
   chunk indices are ≤ 3. No collision risk. It *is* however a seed derivation that produces
   a value far outside the 31-bit space the campaign seeds live in, so do not assume
   "the seed" is one number — there are two, at different levels.
2. **The receipt reports the wrong seed for every chunked run.** See §9.3. This is the
   single highest-value guard finding in this document.

### 3.6 The OF3 seed bug that made all this necessary

Context the redo needs, because it explains the whole shape. `refs/of3_seed_bug_mechanism.md:7-15`:
`openfold3/entry_points/experiment_runner.py:608-612` contains

```python
if num_model_seeds:
    start_seed = 42
    self.seeds = generate_seeds(start_seed, num_model_seeds)
```

A hardcoded `42`. Every OF3 prediction across Block A (2,375 rows) and the frozen v3.7
corpus back to 2026-08-27 ran at internal seed `2746317213`
(`refs/of3_seed_bug_mechanism.md:32`) — `random.seed(42)` first draw, which I reproduced
locally. The fix is to pass seeds via `--runner-yaml experiment_settings.seeds` and
**never pass `--num-model-seeds`** (`:46`), which is what `qsub/rerun_of3.sh:162-169` and
`:206-213` do.

There are **three** layers of defence, and it is worth copying all three:
- a vendored `raise ValueError` patched into site-packages at the offending line
  (`qsub/openfold3_vendored_patch.diff:14-18`);
- a grep guard on the generated yaml, per call and per chunk
  (`qsub/rerun_of3.sh:123-127`, `:199-204`);
- a status-JSON probe `sentinel_bug_seed_present` (`qsub/status_writer.py:142-144`).

The third one does not work on chunked runs (§9.3).

---

## 4. The environment contract — what a launcher needs

### 4.1 Mandatory in all five launchers

```
PRED_INPUT     absolute path to the backbone input file
PRED_OUT_DIR   absolute path where output should land
PRED_SEED      integer
PRED_SIDECAR   absolute path to the rerun-plan JSON
```
`qsub/rerun_boltz.sh:51-54`, `rerun_chai.sh:55-58`, `rerun_of3.sh:42-45`,
`rerun_protenix.sh:54-57`, `rerun_af2mm.sh:44-47`. All use `:?`, so a missing one aborts.

`PRED_SIDECAR` is required but **never read** — it is used only to `mkdir -p` its parent and
to be echoed into the status JSON's config block. Chai ignores it entirely and manipulates a
hardcoded `$PRED_OUT_DIR/_rerun_plan.json` instead (`qsub/rerun_chai.sh:116`).

### 4.2 Optional, with defaults

| var | default | where | notes |
|---|---|---|---|
| `PRED_SAMPLES` | `1` | all four | samples per fold call |
| `PRED_N_SEEDS` | `1` | OF3 only (`rerun_of3.sh:96`) | length of the runner-yaml seeds list |
| `OF3_MAX_PER_CALL` | `25` | `rerun_of3.sh:159` | the Triton ceiling |
| `MSA_A3M_PATH` | unset | boltz/of3/protenix only | Tier D3 depth ladder; **Chai has no branch for it** |
| `CHAI_MSA_DIRECTORY` | `/hpc/scratch/sengaad1/paper_af3/msa_cache/chai` | `rerun_chai.sh:130` | assigned with `:=`, not `:?` |
| `BOLTZ_VENV` / `BOLTZ_CACHE` | `/home/sengaad1/software/venvs/boltz`, `/hpc/scratch/sengaad1/boltz_cache` | `rerun_boltz.sh:66-67` | |
| `CHAI_VENV` | `/home/sengaad1/software/venvs/chai1` | `rerun_chai.sh:66` | |
| `OF3_VENV` / `OF3_CKPT` | `…/venvs/openfold3`, `…/openfold3/checkpoints/of3-p2-155k.pt` | `rerun_of3.sh:51-52` | **the only weights pin anywhere** |
| `PTX_VENV` | `/home/sengaad1/software/venvs/protenix` | `rerun_protenix.sh:63` | |
| `AF2_DBS` | `/db/camm/alphafoldDB` | `rerun_af2mm.sh:53` | |
| `COLABFOLD_MIN_READ` / `_MIN_CONN` | `600` / `30` | `qsub/colabfold_shim.py:59-60` | |

Path A passes exactly five of these via `qsub -v` (`scorer/rerun_dispatch.py:590-616`):
`PRED_INPUT, PRED_OUT_DIR, PRED_SEED, PRED_SAMPLES, PRED_SIDECAR`. **`MSA_A3M_PATH` and
`CHAI_MSA_DIRECTORY` are not in that list** — they are only plumbed on the Path-B queue
route (`scripts/queue_ops.py:150-157`). A depth-tier row dispatched through the supervisor
silently falls back to the live server.

### 4.3 The ColabFold shim sits between the launcher and the network

OF3 is not invoked directly; it goes through `qsub/colabfold_shim.py of3 predict`
(`qsub/rerun_of3.sh:162`, `:206`). The shim monkey-patches `requests.get`/`requests.post`
at import (`qsub/colabfold_shim.py:156-157`) and enforces a `(connect ≥ 30 s, read ≥ 600 s)`
floor on any URL containing `api.colabfold.com` (`:89-104`). It exists because of a
recurring 6.02-second `ReadTimeout` in ColabFold clients — 91 ReadTimeouts on one OF3
prediction, 748 s raw → ~200 s under the shim (`qsub/rerun_of3.sh:129-135`).

It writes a sidecar `_of3_colabfold_http_summary.json` (path from `COLABFOLD_SIDECAR`,
`:61-62`) via `atexit`, so it lands even on a crash (`:223`, `:160-176`). Fields
(`:64-74`): `backbone, policy, colabfold_calls, colabfold_retries, colabfold_http_wait_s,
cache_hit_immediate, colabfold_success_calls, colabfold_error_calls, endpoints_seen`.

**`colabfold_calls == 0` is the strongest MSA-failure signal the pipeline produces** — and
nothing acts on it.

### 4.4 Chai's MSA is a content-addressed cache, and that is the whole story

Chai has no MSA field in its input file. It reads `--msa-directory "$CHAI_MSA_DIRECTORY"`
(`qsub/rerun_chai.sh:130-136`), a flat directory of files named
`sha256(sequence.upper()).hexdigest() + ".aligned.pqt"`. **One file per protein chain, keyed
on that chain's sequence alone — there is no joint object and no pair file**
(`qsub/rerun_chai.sh:167-168`, pre-flight; `scripts/build_chai_msa_cache.py:10`, builder).

So: adding a partner adds one more independent cache file and changes nothing else. A
peptide ligand, emitted as `>protein|name=lig`, **does** require its own `.aligned.pqt`; a
small-molecule `>ligand|…` record does not (`qsub/rerun_chai.sh:164`).

The cache we hold a census of has 120 files covering every sequence Blocks A and B could
have dispatched, 1:1 with zero orphans in either direction
(`experiments/019_block_b_partner_selection/analysis/msa_depth_report.md:26-30`). Depths
range 1,996 (CNR2) to 18,146 (DRD2) for receptors and 11,904–14,986 for the five cognate Gα
(`:74-121`, `:163-167`).

Two facts from that report that a redo guard must not get wrong:
- **Depth 1 is legitimate for short peptides.** `random_helix_40mer`, `arrestin_Ctail`,
  `substanceP` (11 aa) and `DAMGO` (5 aa) all have total depth 1 — query row only, no
  homologs (`:353-356`, `:378-383`). A "depth > 1" guard would false-positive on exactly the
  peptide arms the redo cares about. Gate on depth **relative to chain length**, or exempt
  chains under ~50 aa explicitly.
- **`pairing_key` and `comment` are empty on every row of all 120 files** (`:56-68`). The
  cache format cannot answer any paired-MSA question. Do not build a paired-depth guard on it.

---

## 5. What happens when a job fails

### 5.1 How failure is detected

**Path A — three signals, in order** (`scorer/supervisor.py`):

1. **Disappearance from `qstat`.** `_reconcile_running` (`:545-551`) flips
   `submitted → running` when the job id appears, and inspects the output dir when it stops
   appearing. `qstat -u <user> -q <queue> -xml` is regex-scraped (`:150-189`); jobs in state
   `d` or `z` are dropped as on their way out (`:185-187`); only names starting `pa3_` count
   (`:429-430`).
2. **The status JSON.** `if data.get("ok"): mark done` (`:560-565`).
3. **Exit-code classification + log grep.** `classify_failure` (`:257-308`): exit codes
   `137, 139, 143` → `TRANSIENT`; any other recorded exit code → `PERMANENT`; no status file
   → grep the log for `TRANSIENT_MARKERS` (`:79-89`: `CUDA_OOM`, `cuda out of memory`,
   `unable to allocate`, `connection reset`, `connection timed out`, `cannot allocate`,
   `GPU init failed`, `temporarily unavailable`, `NCCL error`).

**There is no per-job timeout and no `qdel` anywhere in the bundle.** The only time bound is
the scheduler's own `h_rt`; the job is killed, vanishes from `qstat`, returns 137/143, and is
classified `TRANSIENT`.

**Path B — exit code only.** `scripts/block_a_worker.sh:110-126` marks `done` on
`JOB_RC == 0` and `failed` otherwise. **It never reads `_<bb>_status.json`.** A run that
exits 0 and produces zero files is `done` on Path B and not-done on Path A.

**"Stalled" is not modelled in the supervisor at all.** On Path B it is a claim-age
heuristic: `STUCK_MIN=30` minutes, 240 minutes for Protenix
(`scripts/overnight_orchestrator.sh:32`, `:114-146`), and an orphan-claim reset when
`claimed > alive` where `alive` is an unfiltered `qstat | grep -c ' r '`
(`scripts/block_a_orchestrator.sh:76`, `:107-112`).

### 5.2 Retries

**Path A: automatic, capped at 2, no backoff, per row.** `max_retries: int = 2`
(`scorer/supervisor.py:328`), counter column `retries` (`:74`). The loop (`:572-586`):
`TRANSIENT and retries < max` → `retries += 1`, state back to `pending`; else `failed`.
Backoff is only the tick period (`poll_seconds = 60.0`, `:327`) and the per-tick submit
budget (`max_submit_per_tick = 8`, `:331`).

Two leaks in the cap, both worth a guard:
- **A qsub submission failure does not increment `retries`** (`:524-533`) — an unbounded
  resubmit loop if qsub keeps rejecting.
- `classify_failure` returns `TRANSIENT` on the "nothing on disk at all" fall-through
  (`:308`), so *no evidence* and *evidence of a transient fault* are the same verdict.

**Path B: no automatic retry.** `failed` is terminal; nothing transitions `failed → pending`
automatically. Recovery is either `queue_ops.py bulk_transition --from-state failed
--to-state pending` (`scripts/queue_ops.py:248-251`) or rebuilding a fresh queue from the
failed rows (`scripts/build_h100_pool_queue.py:60-79`). There is **no attempt counter in the
queue schema at all** (`scripts/queue_ops.py:34-42`), so a repeatedly-stalling row is reset
forever.

### 5.3 **Does a retry reuse the same seed? Yes, unconditionally.**

`fresh_seed_for` (`scorer/rerun.py:749-751`) takes exactly one argument — the hex SHA-256 of
the frozen prediction file. Not the row id, not the attempt number, not the backbone, not
the clock. The retry path (`scorer/supervisor.py:579-583`) mutates only `row.retries` and
`row.state`; `retries` is read by exactly one expression, the bound at `:579`, and never
reaches seed derivation, the plan, or the qsub argv. `_plans_cache` (`:443-445`) hands back
the *identical* `ReRunPlan` object on the retry tick, so `PRED_SEED` is byte-identical.

**A retry is a bit-for-bit re-run of the same computation.** For a deterministic backbone
that is correct; for a transient CUDA OOM it is what you want. But note the consequence:

> `out_dir` embeds the seed (`scorer/rerun_dispatch.py:471-474`), so **a Path-A retry writes
> into the same directory as the failed attempt** (same calendar day). Nothing purges it —
> `_submit` only does `mkdir(parents=True, exist_ok=True)` (`scorer/supervisor.py:511`).
> Partial CIFs from attempt 1 survive and are counted by `_produced_files`, which can flip
> `ok` to true on a second attempt that itself produced nothing
> (`qsub/status_writer.py:250-257`, `:312`).

Path B does purge: `find "$PRED_OUT_DIR" -mindepth 1 -delete` before each attempt
(`scripts/block_a_worker.sh:102`, `scripts/h100_worker.sh:59`) — but with `2>/dev/null || true`,
so a failed purge is silent.

One more wrinkle: `date_stamp` defaults to `date.today()` (`scorer/rerun_dispatch.py:470`).
**Across a supervisor restart on a different calendar day the same row plans a different
`out_dir`.** The seed is stable; the destination is not.

### 5.4 What is recorded on failure

| artefact | written by | contents |
|---|---|---|
| `<out_dir>/_rerun_plan.json` | `scorer/supervisor.py:512-513`, **before** qsub | `ReRunPlan.sidecar()` (`scorer/rerun_dispatch.py:328-344`), incl. the whole `manifest_row` |
| `<out_dir>/_<backbone>_status.json` | `qsub/status_writer.py:324-325` | see §7 |
| `refs/rerun_status.csv` | `scorer/supervisor.py:128-138`, atomic `os.replace` | `prediction_sha, prediction_path, experiment_slug, backbone, receptor_effective, state, job_id, out_dir, retries, last_reason, updated_utc` (`:64-76`) |
| `<pool>/queue_state.csv` | `scripts/queue_ops.py:54-61` | `prediction_sha, backbone, state, worker, claimed_at, finished_at, last_reason` (`:34-42`) |
| `/hpc/scratch/sengaad1/paper_af3/logs/rerun_<bb>.$JOB_ID.log` | `#$ -o`, `-j y` | free text; provenance header at `qsub/rerun_boltz.sh:85-93` |

Writing the sidecar **before** qsub is a good decision and worth copying —
`scorer/supervisor.py:509-510`: *"if the qsub fails, the plan is still recoverable from disk
on the next tick."*

**Is a failure distinguishable from a job that never launched? On disk, no.** An `out_dir`
containing only `_rerun_plan.json` and no status JSON is produced identically by (i) a qsub
never accepted, (ii) a job killed before the fold finished, (iii) a dead node. All three map
to `TRANSIENT` (`scorer/supervisor.py:308`). In the CSV it is partially distinguishable:
`last_reason` is `"qsub exit=…"` / `"qsub-exception: …"` (`:526`, `:531-532`) versus
`"retry-N (TRANSIENT)"` / `"PERMANENT exhausted-retries"` (`:582`, `:586`) — but
`last_reason` is **overwritten on every `_mark`** (`:435`). There is **no append-only
per-row event log anywhere in the bundle**, so attempt-by-attempt history cannot be
reconstructed from the recorded artefacts.

Three classes of row vanish from the record entirely:
- a hydration `OSError` increments a counter and `continue`s; the row never enters
  `status.csv` (`scorer/supervisor.py:378-382`);
- `skip_unresolved=True` drops unresolved-receptor rows with no record
  (`scorer/rerun_dispatch.py:645-649`);
- `queue_ops.py pop` exit 2 ("queue.csv row missing") happens **after** the `claimed` flip
  has already been persisted (`scripts/queue_ops.py:131-138`), leaving the row permanently
  `claimed` with no owner.

### 5.5 The queue's state machine

Two CSVs side by side under `/hpc/scratch/sengaad1/paper_af3/h100_pool`
(`scripts/queue_ops.py:33`): `queue.csv` (immutable payload, propose-manifest schema) and
`queue_state.csv` (mutable). States: `pending | claimed | done | failed` (`:36`), plus an
undocumented fifth, `paused`, accepted by both `mark` (`:235`) and `bulk_transition`
(`:249-251`).

**Claiming is correct and worth copying**: an `fcntl.LOCK_EX` held over the whole
read-modify-write, then tmp-file + `os.replace` (`scripts/queue_ops.py:102-133`, `:54-61`).
Per-worker backbone filters live in `<pool>/filters/<worker_id>.txt` — line 1 comma-separated
backbones, optional line 2 `strict` (`:76-99`).

**Two documented invariants are not implemented.** `scripts/queue_ops.py:19` says "Never
overwrite a done or failed row"; `cmd_mark` matches on sha alone and overwrites whatever is
there (`:166-172`), and `bulk_transition` permits any state → any state unguarded
(`:198-211`). Likewise `scorer/supervisor.py:33-36` claims the supervisor "never resubmits a
row whose `done` marker is on disk … even if the status.csv row got wiped." I read `_submit`
(`:492-543`) in full: **there is no such check.** Delete `refs/rerun_status.csv` and every
row re-fires against completed CIFs.

---

## 6. What lands on disk

### 6.1 The pool tree

Built by the campaign builder (`scripts/build_tier_d1_manifest.py:276-281`):

```
{hpc_out_prefix}/{receptor_lower}/{ligand_role}/{arm}/{backbone}/seed_{seed_value}/
```

Real example from `received/_of3_status.json`:

```
/hpc/scratch/sengaad1/paper_af3/experiments/022_tier_d1_deep_apo/full/pool/pool/
  opsd/ apo_no_ligand/ apo/ of3/ seed_1015473677/
```

The doubled `pool/pool` is not a code defect — the builder appends
`{receptor}/…` to whatever `--hpc-out-prefix` is passed, and the invocation passed a prefix
already ending in `/pool`. It matters only because the scorer's path parser depends on it
(next paragraph).

**The scorer recovers provenance by parsing this path.** `_POOL_PATH_RE`
(`scorer/orchestrator.py:173-178`) matches
`/pool/<receptor>/<ligand_role>/<partner_arm>/<backbone>/seed_<N>` and is the **only**
source of `ligand_role` for any dispatch that did not write a sidecar
(`:161-172`). The seed is recovered by `_SEED_FROM_PATH_RE = r"/seed_(\d+)(?:/|$)"`
(`:158`), which `re.search` resolves to the **leftmost** match — the outer dispatch seed,
not the OF3 inner seed. That is the correct choice and it works by luck of ordering, not by
design; a nested `seed_` that appeared first would silently change the recorded seed.

### 6.2 Per-backbone leaf layout — they are all different

| backbone | path under `seed_<N>/` | evidence |
|---|---|---|
| Boltz | `boltz_results_<stem>/predictions/<stem>/<stem>_model_<i>.cif` | `received/rows_csv_line.txt` (real scored row, `_model_16.cif`); shape also at `scorer/orchestrator.py:319` |
| OF3, ≤25 samples | `<query_name>/seed_<inner>/<query_name>_seed_<inner>_sample_<i>_model.cif` | `qsub/rerun_of3.sh:162-169` |
| OF3, >25 samples | `chunk_<c>/<query_name>/seed_<inner_c>/<query_name>_seed_<inner_c>_sample_<i>_model.cif` | `received/_of3_status.json`, 100 files over 4 chunks |
| Chai | (see §7) | `qsub/rerun_chai.sh:197-204` |
| Protenix | (see §7) | `qsub/rerun_protenix.sh:112-118` |

Plus, in every `seed_<N>/`:

| file | written by |
|---|---|
| `_input_used.<basename-of-PRED_INPUT>` | `cp -f` at `qsub/rerun_of3.sh:77` and the equivalent in each launcher |
| `_<backbone>_status.json` | `qsub/status_writer.py:324` |
| `_rerun_plan.json` | `scorer/supervisor.py:512` (Path A); **not on every Path-B tier** |
| `_runner_seeds.yml` | OF3 only, `qsub/rerun_of3.sh:99` — and a second copy per `chunk_<c>/` at `:186` |
| `_of3_colabfold_http_summary.json` | OF3 only, `qsub/colabfold_shim.py:160-176` |

`cp -f "$PRED_INPUT" "$PRED_OUT_DIR/_input_used.$(basename "$PRED_INPUT")"` is the single
best provenance decision in the whole pipeline: **the exact bytes fed to the model are
preserved next to the output.** Copy it verbatim. It is how we hold
`received/_input_used.tier_d1_opsd_apo_boltz_seed2.yaml` at all.

### 6.3 `prediction_path` in the manifest does not point at a real file

The builder writes `prediction_path = f"{hpc_pred_out_dir}/model_0.cif"`
(`scripts/build_tier_d1_manifest.py:281`), and `propose.py` has a parallel table
`_BACKBONE_OUTPUT_LEAF` claiming `boltz → "model_0.pdb"`, `of3 → "model_0.cif"`,
`protenix → "sample_0.cif"`, `chai → "pred.model_idx_0.cif"` (`scorer/propose.py:97-103`).

**None of these is the path any backbone actually writes.** The real Boltz leaf we hold is
`…/boltz_results_<stem>/predictions/<stem>/<stem>_model_16.cif` — four directories deeper and
a different extension from the `model_0.pdb` the table predicts. The real OF3 leaf is
`…/chunk_0/<query>/seed_<inner>/<query>_seed_<inner>_sample_10_model.cif`.

The manifest's `prediction_path` is therefore a **row identity key, not a file locator**. The
scorer never opens it — `gpcr-score-batch` reads a *rescore* manifest built later by
`scripts/build_*_rescore_manifest.py` from files actually found on disk. **The redo's
delivery contract must not inherit this column's name without inheriting that distinction.**

### 6.4 Scratch that does not survive

`$TMPDIR/of3-of-sengaad1/colabfold_msas/{main,paired,template}/` is per-job scratch, purged
when the SGE job exits (`block_b_figure_data/03_msa_audit/PHASE_1D_EXTENSION.md:93`, and the
explicit `rm -rf` at `scripts/block_b_worker.sh:141`). **Raw OF3 MSAs are gone for every
landed row.** Only the hashed paths survive, inside `inference_query_set.json` (`:95-97`).
If the redo wants a column-level MSA audit on OF3, it must archive that directory before the
job exits — nothing in their pipeline does.

---

## 7. The four status JSONs, diffed

All four are `received/_<backbone>_status.json`, all OPSD × apo × Tier D1, all written by
the same `qsub/status_writer.py`. **They are not quite the same cell** — see §7.4.

### 7.1 The shape, and how `ok` is decided

Six top-level keys in all four (`qsub/status_writer.py:305-322`):
`backbone, exit_code, seed, produced_files, n_produced, ok`, plus `runtime_config`
carrying `package_version`, `received_config`, `env`, `host`, `status_write_ts_utc`,
`runtime_probe`.

```python
"ok": args.exit_code == 0 and len(produced) > 0,       # status_writer.py:312
```

Both conditions, and nothing else. `produced` is an **unbounded `rglob`** —
`*.cif` + `*.pdb` for Boltz and Chai, `*.cif` only for OF3 and Protenix
(`:250-257`). There is no maxdepth, no size check, no non-zero-byte check, and **no
comparison of `n_produced` against `received_config["n_samples"]`.** `main()` returns 0
unconditionally (`:327`) — the status writer can never fail a job.

### 7.2 Shared core, and the one block that is not comparable

22 key paths are present in all four. **`runtime_probe` has zero leaf keys in common
across the four backbones** — each probes something different:

| backbone | probe leaves | `file:line` |
|---|---|---|
| Boltz | `input_yaml`, `input_yaml_sha256`, `has_msa_field`, `has_templates_field` | `qsub/status_writer.py:189-203` |
| Chai | `msa_directory`, `msa_mode`, `protein_chains[]` (per-chain `seq_sha256`, `pqt_present`, `pqt_size`), `all_present` | `:148-186` |
| OF3 | `runner_yaml_path`, `resolved_seeds`, `sentinel_bug_seed_present` | `:122-145` |
| Protenix | `input_json`, `input_json_sha256`, `has_template_hits_file`, `has_templates_top_level`, `top_level_keys` | `:206-238` |

**For a comparison across backbones, only the six top-level keys and `received_config`'s
six shared fields are usable.** Everything interesting is in the incomparable block.

Shared values, side by side:

| key | boltz | chai | of3 | protenix |
|---|---|---|---|---|
| `exit_code` | 0 | 0 | 0 | 0 |
| `ok` | true | true | true | true |
| `seed` | **1800878580** | 1015473677 | 1015473677 | 1015473677 |
| `n_produced` = `len(produced_files)` | 100 | 100 | 100 | 100 |
| `n_samples` = `env.PRED_SAMPLES` | 100 | 100 | 100 | 100 |
| package version | boltz **2.2.1** | chai_lab **0.6.1** | openfold3 **0.4.4** | protenix **2.0.0** |
| python (from install path) | 3.11 | 3.11 | 3.13 | 3.13 |
| host | nrchbs-cph510076 | …023 | …028 | …076 |
| GPU slot | `gpu2` / `CUDA_VISIBLE_DEVICES=2` | `gpu1` / 1 | `gpu0` / 0 | `gpu3` / 3 |
| `JOB_ID` | 35918699 | 35918687 | 35918689 | 35918700 |
| launch → status-write (derived) | 4 m 05 s | 3 m 53 s | **25 m 21 s** | 3 m 12 s |

Sampler settings, by role:

| role | boltz | chai | of3 | protenix |
|---|---|---|---|---|
| recycles | `recycling_steps: 3` | `num_trunk_recycles: 3` | **not recorded** | `cycle: 3` |
| diffusion steps | `sampling_steps: 200` | `num_diffn_timesteps: 50` | **not recorded** | `step: 50` |
| MSA control | `use_msa_server: true` | `msa_mode: cache` + directory | `use_msa_server: true` | `msa_server_mode: protenix` |
| templates | `has_templates_field: false` | **not recorded** | `use_templates: false` | two flags, both false |

**A methods table saying "3 recycles, 50 diffusion steps across all four backbones"
cannot be sourced from these receipts** — OF3 records neither, and Boltz uses 200 steps,
not 50.

### 7.3 What they record, and what they do not

**Recorded by all four:** backbone, package version + install path, exit code, `ok`, seed
requested, samples requested, files produced (full path list), input file path, launch and
status-write timestamps, hostname, GPU slot index, SGE job id.

**Recorded by some:** input file sha256 (**Boltz and Protenix yes; OF3 and Chai no** —
Chai records per-chain *sequence* sha256 instead); chain count and chain labels (Chai only,
implicitly, via `protein_chains[]`); MSA file presence and size (Chai only).

**Recorded by none of the four:**

- **MSA depth.** Chai records `pqt_size` in bytes (1,622,511 B in this cell) but never a
  row count. Boltz/OF3/Protenix record only `use_msa_server: true`.
- **Model checkpoint hash.** `of3_ckpt: null`, `boltz_cache: null`,
  `use_default_params: true`. Nothing identifies the weights.
- **Wall time.** Derivable from the two timestamps, never stated.
- **GPU model name.** Only the card slot. (Protenix's `TORCH_CUDA_ARCH_LIST: "9.0"` implies
  Hopper; the other three do not carry it.)
- **Any hash or size of the output structures.** You cannot verify a CIF is unchanged.
- **Receptor / cell identity as a field.** Inferable only from paths.
- **Git commit of the pipeline.** That lives in the *scored* row (field 11 of
  `received/rows_csv_line.txt` = `d9c646af5f89861c16062bf256de96a8389d9915`), not the
  receipt.
- **CUDA / driver / torch version, stdout/stderr log path, per-sample confidence.**

**The five to add in the redo's own receipt: MSA depth, checkpoint hash, explicit wall
time, GPU model, and a hash of each output structure.** Those five turn a receipt that says
"something finished here" into one that says "this result is reproducible."

### 7.4 Output tree per backbone — four different conventions

Relative to `pred_out_dir`, with `{stem}` the job stem:

| backbone | pattern | depth | index range |
|---|---|---|---|
| boltz | `boltz_results_{stem}/predictions/{stem}/{stem}_model_{i}.cif` | 3 | `i` 0…99 |
| chai | `pred.model_idx_{i}.cif` | **0 — flat** | `i` 0…99 |
| of3 | `chunk_{c}/{stem}/seed_{s_c}/{stem}_seed_{s_c}_sample_{k}_model.cif` | 3 | `c` 0…3, `k` **1…25**, repeated per chunk |
| protenix | `{stem}/seed_{S}/predictions/{stem}_sample_{i}.cif` | 3 | `i` 0…99 |

Boltz says `model_{i}`, Chai says `model_idx_{i}`, OF3 says `sample_{k}_model`, Protenix
says `sample_{i}`. **Four regexes downstream, and no shared vocabulary.** If the redo
specifies one delivery convention, this is the cheapest thing to fix.

### 7.5 Anomalies, each stated with its numbers

**(a) The four receipts are not the same seed.** Boltz is `1800878580`; the other three are
`1015473677`. From the manifest those are `seed_index` **2** and **4**. Corroborated by the
input filenames — `…_boltz_seed2.yaml` vs `…_chai_seed4.fasta`, `…_of3_seed4.json`,
`…_protenix_seed4.json`. Verified directly against `received/tier_d1_full_manifest.csv`.
**Any "same cell, four backbones" comparison over these four files is off by one seed for
Boltz.** This is a property of what was sent to us, not of their pipeline.

**(b) OF3's `resolved_seeds` is contradicted by every path it lists.** The probe reports
`[945550830]` and `n_seeds: 1`; the string `945550830` appears in **0 of 100**
`produced_files`, which instead carry four seeds across four `chunk_*/` directories. The
cause is mechanical: `_probe_of3_runner_yaml` reads `received_config["runner_yaml_path"]`
(`qsub/status_writer.py:283-285`), which the launcher sets to
`$PRED_OUT_DIR/_runner_seeds.yml` (`qsub/rerun_of3.sh:99`, `:233`, `:238`) — the
**top-level** yaml, written on line 99 and then **never used** when the chunked branch is
taken. The per-chunk yamls at `$CHUNK_DIR/_runner_seeds.yml` (`:186`) are never probed.

Consequently `sentinel_bug_seed_present: false` was evaluated on a file the run did not
read. **The guard against the OF3 seed-collapse bug does not run on any chunked OF3 job.**
It is a passing check that never executes on the artefact it exists to police — the
project's own `[[a-silent-check-looks-like-a-passing-one]]` shape, in someone else's code.

**The fix is one line**: point the probe at the chunk yamls (glob
`$PRED_OUT_DIR/chunk_*/_runner_seeds.yml`) and report a list. The redo must do this before
spending anything on OF3.

**(c) OF3 sample indices are not unique within a run.** `sample_{k}` runs 1…25 and repeats
identically in all four chunks. `sample_7` is ambiguous unless chunk *and* inner seed travel
with it. The other three use a single 0…99 range, and start at 0 while OF3 starts at 1.

**(d) Doubled seed token in the OF3 and Protenix job stems.** The stems are
`tier_d1_opsd_apo_of3_seed4_seed4` and `tier_d1_opsd_apo_protenix_seed4_seed4`, from
inputs named with a single `seed4`. The cause is `input_name = f"{request_id}_seed{seed_index}"`
where `request_id` already ends `…_seed{seed_index}`
(`scripts/build_tier_d1_manifest.py:246-250`). Cosmetic, but it is in every output filename
for two of four backbones, so any parser must tolerate it.

**(e) `CHAI_MSA_DIRECTORY` is exported in all four environments**, including Boltz, OF3 and
Protenix whose own MSA config is `use_msa_server: true` / `msa_server_mode: protenix`. It is
inherited environment noise from the `qrsh -v` line (`qsub/dispatch_tier1.sh:83`), not
evidence those three read the Chai cache. A reader of the receipt alone could easily
conclude otherwise.

**(f) Two ISO-8601 dialects in the same object.** `launch_ts_utc` ends `Z`;
`status_write_ts_utc` ends `+00:00`. In all four files.

---

## 8. The manifest — the 34-column dispatch contract

`received/tier_d1_full_manifest.csv`: 140 data rows, 34 columns. The schema is
`PROPOSE_MANIFEST_COLUMNS` (30 columns, `scorer/schema.py:577-603`) **plus** four Block-C
extras (`scripts/build_tier_d1_manifest.py:166-169`) kept "so downstream rescore/analysis
code can consume both without a schema branch."

`scorer/schema.py:574-576` states the contract rule explicitly, and the redo should adopt
it verbatim: *"Ordering is stable so downstream consumers can rely on column positions;
adding a new column here is a schema change and requires a bump."*

### 8.1 The 34 columns

| # | column | meaning | in this file |
|---|---|---|---|
| 1 | `prediction_path` | where output **will** land + a leaf filename. **A row identity key, not a file locator** (§6.3) | 140 distinct |
| 2 | `prediction_sha` | sha256 of the fold-model *output*; empty at dispatch time by design (`scorer/propose.py:992-993`) | **empty on all 140** |
| 3 | `experiment_slug` | per-row campaign slug | 140 distinct; **≡ `request_id`** |
| 4 | `wave_group` | the dispatch wave | const `tier_d1_2026_09_06` |
| 5 | `branch` | provenance of the manifest builder | const `propose` |
| 6 | `tier` | tier label | const `tier_d1` |
| 7 | `backbone` | `boltz`\|`chai`\|`of3`\|`protenix`\|`af2mm` | 4 values, 35 rows each |
| 8 | `receptor_from_path_substring` | receptor as parsed out of a path | 7 values |
| 9 | `receptor_resolved` | receptor after `resolve_receptor` | 7 values; **≡ col 8 on all 140** |
| 10 | `disambig_conflict` | cols 8 and 9 disagree | const `false` |
| 11 | `receptor_unresolved_in_original` | the original row had no resolvable receptor | const `false` |
| 12 | `expected_control_json` | expected-control payload (rerun lineage) | empty |
| 13 | `new_seed` | **the seed passed to the model** as `PRED_SEED` | 5 values |
| 14 | `request_id` | the analyst-facing request id; feeds `input_name` | 140 distinct |
| 15 | `seed_index` | replicate index 0…N-1 within the request | 0…4 |
| 16 | `state_claim` | a `StateClaim` enum value — the *claimed* state, input to scoring | const `apo` |
| 17 | `species` | feeds the A5 species assertion | `human` ×120, `bovin` ×20 (OPSD) |
| 18 | `partner_type` | `g_alpha`\|`peptide`\|`small_molecule`\|`apo`\|`arrestin` — **selects monomer vs two-chain templater** | const `apo` |
| 19 | `partner_identity` | `partners.fasta` header id, or `""` for apo | empty |
| 20 | `partner_perturbation` | `wt`\|`truncated_Naa`\|`shuffled`\|`mutated`\|`chimeric`\|`designed` | const `wt` |
| 21 | `receptor_class` | GPCR class A/B/F | const `A` |
| 22 | `input_path` | **where the materialised input file was written** | 140 distinct |
| 23 | `input_sha` | sha256 of that file — the change-detection key | **84 distinct** (§8.3) |
| 24 | `pre_check_status` | `pass`\|`warn_A1`\|…\|`warn_multiple` from the five pre-checks | const `pass` |
| 25 | `pre_check_details_json` | per-check `(status, reason)` tuples as JSON | empty |
| 26 | `seed_used` | seed propagated end-to-end | ≡ `new_seed` on all 140 |
| 27 | `ligand_type` | `none`\|`peptide`\|`small_molecule` | empty |
| 28 | `ligand_sequence` | peptide-ligand sequence | empty |
| 29 | `ligand_smiles` | SMILES, or `CCD:<code>` | empty |
| 30 | `samples_per_seed` | → `PRED_SAMPLES`; the per-backbone samples flag | const `100` |
| 31 | `ligand_role` | `none`\|`decoy_lig`\|`neutral_antagonist`\|`inverse_agonist`\|`full_agonist`; routes the pocket-metrics reference | empty |
| 32 | `ligand_bound_pdb` | PDB the ligand pose came from | empty |
| 33 | `ligand_ccd` | CCD three-letter code | empty |
| 34 | `ligand_smiles_source` | provenance of the SMILES (CCD / PubChem / memory) | empty |

Columns 1–13 are the `rerun_manifest`-compatible core (`scorer/schema.py:578-583`); 14–21
are propose-specific; 22–25 are Layer-3 input provenance; 26–29 are the seed/ligand
context; 30 is the samples multiplier; 31–34 are the Block-C extras.

### 8.2 The grid, verified

7 receptors (ADRB2, CNR2, CXCR4, GHSR, LPAR1, NPY1R, OPSD) × 4 backbones × 5 seeds =
**140 rows**, complete and perfectly balanced: 28 distinct `(receptor, backbone)` cells,
exactly 5 rows each. 140 × `samples_per_seed` 100 = **14,000 predictions**, which matches
`n_total: 14000` in `received/rescore_parallel.provenance.json` exactly. The builder asserts
all three of these (`scripts/build_tier_d1_manifest.py:334-348`).

Seed value is a **global function of `seed_index`**, identical across every receptor and
every backbone:

| `seed_index` | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| `new_seed` | 1965127769 | 1060594406 | 1800878580 | 1330640762 | 1015473677 |

**22 of 34 columns carry zero information in this file** (13 constants plus the empty ligand
block); only 12 vary, and three of those are exact duplicates of another column
(`experiment_slug`≡`request_id`, `receptor_from_path_substring`≡`receptor_resolved`,
`new_seed`≡`seed_used`). **Nine independent varying columns.** That is what an apo-only,
ligand-free, single-tier slice looks like — the schema is sized for Block C, not for D1.

### 8.3 `input_sha` splits the backbones 2:2, and this is load-bearing

84 distinct hashes over 140 rows: **boltz 7, chai 7, of3 35, protenix 35** (verified
directly). Boltz and Chai input files do not encode the seed, so all five seed-variants of a
cell are **byte-identical**; OF3 and Protenix get one hash per receptor × seed.

Wait — Protenix's templater takes no seed either (`scorer/propose.py:614-625`). The 35
distinct Protenix hashes come from `name`, which is `input_name` and therefore carries
`seed{seed_index}` (`scripts/build_tier_d1_manifest.py:250`, `:197-201`). So Protenix's
input file varies with the seed **only through the query name**, not through any sampler
setting. OF3's varies through both the name and the real `"seeds": [N]` field.

**Consequence for reproduction:** for Boltz and Chai, `input_sha` cannot tell you which seed
was requested. Only the filename and the `PRED_SEED` env var can. **Do not key a redo row on
`input_sha` alone** — key on `(input_sha, seed)`, which is exactly what their own
`propose_row_key = sha256(input_sha + "|" + new_seed)` does
(`scorer/rerun_dispatch.py:378-382`, used at `scripts/build_block_a_campaign_queue.py:89`
with a hard duplicate guard at `:93-98`). Copy that key.

### 8.4 Two manifest-vs-reality mismatches

**`smoke` vs `full`.** All 140 manifest paths sit under
`…/022_tier_d1_deep_apo/**smoke**/pool/…`; every status JSON and the scored row sit under
`…/**full**/pool/…` (verified: 140/140 smoke in the manifest, 4/4 full in the receipts). The
`input_sha` values match across the two trees — OPSD/boltz/seed2 is `9d3090c3…` in both, and
I recomputed that hash from `received/_input_used.tier_d1_opsd_apo_boltz_seed2.yaml` and got
the same value — **so the inputs are byte-identical and only the tree prefix differs.** The
manifest we hold is the smoke-tree manifest for the same grid, not the full-run one.

**The promised scratch-path rewrite does not happen.** `scripts/build_block_a_campaign_queue.py:7-9`
promises "a worker-facing `prediction_path` column that points at scratch" and defines
`_pred_path()` at `:54-62` to do it. **`_pred_path` is defined and never called** — verified,
in both that file and `scripts/build_block_b_campaign_queue.py:52`. The queue copies the
manifest's `prediction_path` verbatim. If a manifest was materialised with a repo-local
`--output-root`, every worker would write somewhere only the login node can see, and nothing
would detect it.

### 8.5 Aligning the redo's delivery contract

Where their columns should be adopted as-is, where renamed, and where added:

| action | columns |
|---|---|
| adopt verbatim | 4–7, 13–21, 24, 26–34 — the campaign/arm/seed/ligand/pre-check descriptors |
| rename | `prediction_path` → **`cell_key`**, because it is an identity not a path (§6.3). Add a separate `output_glob` that actually resolves. |
| keep but re-scope | `input_sha` — pair it with the seed, per §8.3 |
| **add** | `msa_depth`, `checkpoint_sha`, `wall_time_s`, `gpu_model`, `output_sha` per structure (§7.3); an `attempt` counter (§9.6); a `partner_chain_count` so §9.5 is checkable |

---

## 9. What can fail silently at each stage — the guard map

This is the section the redo spends money against. Each entry: **what fails**, **why it is
silent**, **what would catch it**.

### 9.1 Chai runs single-sequence and the receipt says `ok=true` — *the one they found*

**Mechanism.** Chai-lab 0.6.1 "silently falls back to single-sequence inference when its
`--msa-directory` lacks the expected hash-named file"
(`scripts/build_chai_msa_cache.py:13-14`). In wave 1, `CHAI_MSA_DIRECTORY` did not propagate
through `qsub -v` and "chai jobs ran silently single-sequence while `_chai_status.json`
reported ok=true" (`qsub/rerun_chai.sh:36-42`). Without the cache, "the Block A chai arm
would silently duplicate `chai_singleseq` across ~4,000 predictions and we'd only discover
it at scoring" (`scripts/build_chai_msa_cache.py:14-16`).

**Their fix — three layers, all worth copying.**
1. The launcher hardcodes the default cache path with `:=`, not `:?`
   (`qsub/rerun_chai.sh:130`), and hard-exits if the directory is missing (`:131-134`).
2. A per-job pre-flight: parse the FASTA, sha256 each protein chain, require
   `<sha>.aligned.pqt` to exist, and **refuse to launch** otherwise
   (`qsub/rerun_chai.sh:162-183`) — *"Refusing to launch chai — this would silently fall
   back to single-sequence."* The exit code is explicitly rescued out of the `set +e` region
   (`:188-193`).
3. A dispatch gate (`scripts/step7_dispatch_gate.py:242-304`) that ssh's to the cluster and
   checks the cache before a campaign starts.

**What still gets through — four residual holes the redo must close.**

- **The pre-flight only counts chains whose header starts with `protein`**
  (`qsub/rerun_chai.sh:164`). A different header prefix yields `n_protein = 0`,
  `missing = []`, and the pre-flight **passes**, printing `0/0 protein chain .aligned.pqt
  files present` (`:185-186`). *Guard:* fail on `n_protein == 0`.
- **It checks existence, not content.** A 0-byte or 1-row `.aligned.pqt` passes. So does a
  file whose alignment is for a different sequence. *Guard:* open the `.pqt`, assert row 0
  equals the dispatched sequence, and assert depth — but see §4.4: exempt chains under
  ~50 aa, because depth 1 is correct for `substanceP` and `DAMGO`.
- **`verify_chai_msa_cache.sh` cannot be used as a gate.** It derives the filename, checks
  existence, prints the byte size with no threshold, then runs a **timing oracle** whose own
  verdict text says the cache is *"probably NOT being read"*
  (`scripts/verify_chai_msa_cache.sh:130-133`). It exits 0 on every outcome and never
  captures `chai-lab`'s exit code. Worse, Test 2 **moves a file out of the shared production
  cache** for up to 300 s (`:102`, `:106`) while workers may be reading it — creating
  exactly the failure it exists to detect. *Guard:* do not run this pattern against a live
  cache; and make the verifier exit non-zero.
- **Chai never honours `MSA_A3M_PATH`.** Boltz, OF3 and Protenix all branch on it
  (`qsub/rerun_boltz.sh:123`, `rerun_of3.sh:152`, `rerun_protenix.sh:105`); Chai has no such
  branch. **A Tier D3 depth-ladder run silently gives Chai the full-depth cache while the
  other three get the subsampled `.a3m`.** *Guard:* refuse to dispatch a Chai row on any
  depth-tier arm until a Chai path exists.

### 9.2 The Chai cache's decoy query rows do not carry the decoy residues

Separate from the single-sequence bug, and larger. Phase 1 §1d found **0 of 40** Block B
decoy query rows carrying the scrambled α5-CT as uppercase aligned columns in the Chai
`.aligned.pqt` — they appear as "WT-parent residues, gaps, or lowercase insertions"
(`block_b_figure_data/03_msa_audit/PHASE_1D_EXTENSION.md:145`, `:160`). Boltz, OF3 and
Protenix are all **READ** on the same query set, 6/6 each (`:58`, `:89`, `:132`).

So on one of four backbones the perturbation under study did not reach the input tensor, and
nothing anywhere detected it. The gate checks that a file with the right name exists; it
does not check what is inside.

**We cannot determine the cause from this bundle** — see §10, question 2.

*Guard for the redo:* for every arm whose whole point is a sequence edit, **assert that the
edited residues appear, uppercase, in row 0 of the MSA the model reads**, per backbone, on a
smoke cell, before the campaign. That is a cheap check and it is the only one that would
have caught this.

### 9.3 The OF3 seed guard does not run on chunked jobs

Detailed in §7.5(b). `sentinel_bug_seed_present` is computed on `_runner_seeds.yml` at the
top level, which the chunked branch writes and then never uses; the four per-chunk yamls the
run actually reads are never probed. **Every OF3 job with more than 25 samples reports a
clean seed check that was performed on the wrong file**, and reports an inner seed that
appears in none of its outputs.

*Guard:* probe `chunk_*/_runner_seeds.yml` and report a list; assert that every seed in the
list appears as a `seed_<N>/` directory in `produced_files`, and that the set of seed
directories has size `N_CHUNKS`.

### 9.4 `ok=true` proves almost nothing about sample count

`ok = exit_code == 0 and len(produced) > 0` (`qsub/status_writer.py:312`). With
`PRED_SAMPLES=100`, **one CIF still yields `ok=true`.** And `_produced_files` is an
unbounded `rglob` (`:250-257`), so on Path A — where the retry writes into the *same*
directory and nothing purges it (§5.3) — leftovers from a failed attempt count toward
`n_produced` and can flip `ok` true on an attempt that produced nothing.

*Guard:* `ok` must require `n_produced == n_samples` (exactly, not `>0`), and every produced
file must be non-zero-length and parse as a structure. One line, and it closes the largest
receipt hole.

### 9.5 Nothing ever compares the output to the input

Across `pre_check.py`, `post_run_receipts.py`, `fold_integrity.py`, `cli.py` and
`step7_dispatch_gate.py` — the five verification files — **four comparisons that a
co-folding study depends on are absent:**

| question | checked? | evidence |
|---|---|---|
| does the output sequence equal the dispatched sequence? | **no** | `fold_integrity.py` has no sequence comparison at all; `_build_seq_index` (`:142-159`) keys only on `seqid.num`. `pre_check.py` compares the *input* FASTA to GPCRdb WT (PC4 `:279-283`), never the output. |
| does the number of chains in the output equal the number requested? | **no** | `fold_integrity._pick_chain` (`:129-134`) takes one named chain and ignores the rest; other chain names surface only inside an error string (`:380`). Step 7 validates manifest *cell counts*, not output stoichiometry. |
| is the seed used equal to the seed requested? | **no** | zero `seed` hits in four of the five files. `scorer/orchestrator.py:452-459` *records* `seed_used` — from a sidecar, or by regexing the path — and never compares it. The only real defence is a propagation test grepping for one historical sentinel value. |
| is the MSA deep enough? | **no** | Step 7's `chai_aligned_pqt` (`:242-304`) checks file presence; `msa_prewarm` (`:1241-1268`) checks the string `cached` in a CSV. Nothing opens an alignment. |

**A monomer returned where a receptor + Gα dimer was requested passes every check in the
pipeline.** The nearest thing is `post_run_receipts._count_extra_protein_chain_residues`
(`:211-231`) — but it fires only in the peptide-**ligand** branch, only when the manifest
declared `ligand_type=peptide`, and is **silently skipped when `receptor_chain_name` is
unknown** (`:357-359`). A missing Gα partner chain is not a "ligand" and is not covered.

*Guard, and this is the highest-value one in the document:* a post-run receipt that opens
the output CIF and asserts **(i)** chain count == requested chain count, **(ii)** each
chain's sequence == the dispatched sequence for that chain, **(iii)** the seed directory
matches the requested seed. Three assertions, no GPU, and they close the whole class.

### 9.6 A retry is invisible in the record

Same seed (§5.3), same directory, and `last_reason` is overwritten on every `_mark`
(`scorer/supervisor.py:435`). **There is no append-only per-row event log anywhere in the
bundle**, and no `attempt` column in either state schema. A row that succeeded on attempt 3
is indistinguishable from one that succeeded on attempt 1.

*Guard:* an `attempt` integer in the row key and in the output path; an append-only
`events.jsonl` per campaign.

### 9.7 Environment variables are sticky across queue rows

`queue_ops.py pop` emits `MSA_A3M_PATH` and `CHAI_MSA_DIRECTORY` **only when the manifest
column is non-empty** (`scripts/queue_ops.py:150-157`). The worker `eval`s the output
**inside a `while` loop in the same shell**, with no `unset` anywhere
(`scripts/block_a_worker.sh:82`, `:95`; verified). So if row *N* carries an
`msa_a3m_path` and row *N+1* does not, **row *N+1* inherits row *N*'s MSA and runs with
`--use_msa_server` disabled** (`qsub/rerun_boltz.sh:123`, `rerun_of3.sh:152`,
`rerun_protenix.sh:105`). The comment at `scripts/queue_ops.py:150-151` — "Empty when the
manifest omits the column — preserves default (live-server MSA)" — is true of the emitted
string and false of the resulting process environment.

*Guard:* `unset MSA_A3M_PATH CHAI_MSA_DIRECTORY` at the top of each loop iteration, or emit
every variable unconditionally (including as the empty string). One line.

Related: `scripts/h100_worker.sh` has **no `CHAI_MSA_DIRECTORY` default line at all** —
`block_a_worker.sh:69` and `block_b_worker.sh:70` both have one, `h100_worker.sh` does not
(verified). And `qsub/dispatch_tier3.sh:20-22` states that `qrsh` does not forward exported
vars automatically. So h100_pool Chai rows relied on whatever the session happened to
inherit — the exact wave-1 shape, in a worker that never got the fix.

### 9.8 `PRED_OUT_DIR` is a string chop, and then it is recursively deleted

`out_dir = pred_path.rsplit("/", 1)[0] if pred_path else ""` (`scripts/queue_ops.py:142`).
An empty `prediction_path` gives an empty `PRED_OUT_DIR`; `pop` still returns 0; the worker
runs `mkdir -p ""` (`scripts/block_a_worker.sh:98`) with no `set -e`, then
`find "" -mindepth 1 -delete 2>/dev/null || true` (`:102`). A `prediction_path` with no
slash gives a *relative* out-dir in the worker's CWD.

`find "$PRED_OUT_DIR" -mindepth 1 -delete` is an unconditional recursive delete of a path
computed from a CSV cell, in three workers (`block_a_worker.sh:102`, `h100_worker.sh:59`,
`block_b_worker.sh:116`). **Highest blast radius in the dispatch path.**

*Guard:* validate `PRED_OUT_DIR` is absolute, non-empty, and under the campaign root before
any `mkdir` or `find -delete`.

### 9.9 The launcher pins drifted from the launchers

`refs/qsub_expected_shas.json` is the local↔HPC sync pin, checked by Step 7's
`qsub_files_hpc_matches_local` (`scripts/step7_dispatch_gate.py:762-816`) and regenerated by
`scripts/regenerate_qsub_shas.py` (plain `sha256(path.read_bytes())`, `:39-40`).

I recomputed all eight. **Five match; three differ:** `rerun_boltz.sh`, `rerun_of3.sh`,
`rerun_protenix.sh`. Those three are **exactly the three that carry an `MSA_A3M_PATH`
branch** (3, 4 and 3 occurrences respectively); `rerun_chai.sh`, which has none, matches. The
companion `refs/scorer_expected_shas.json` is clean — 8 of 8 match.

The coherent reading is that the Tier D3 MSA-path edit landed in the launchers and
`regenerate_qsub_shas.py` was not re-run, exactly as its own docstring warns:
*"Run this AFTER any change to a file in QSUB_FILES_TRACKED, and BEFORE any dispatch"*
(`:13-14`). **I cannot tell from the bundle whether the pin was stale at dispatch time or
only at bundling time** — see §10, question 1.

This is the same regression class the gate itself was built for
(`scripts/step7_dispatch_gate.py:42-48`): *"commit 0e738af rewrote all four rerun_*.sh to
invoke status_writer.py, laptop had the edits, HPC did not, and every Block A + Block B
prediction silently ran the pre-audit inline heredoc — audit-#10 / #13 countermeasures
non-operational for two campaigns without any signal."*

*Guard:* make pin regeneration a pre-commit hook on the tracked tuple, and have the launcher
itself assert its own sha at runtime.

### 9.10 Guards that are documented but not implemented

Three, each of which a reader auditing by docstring would believe exists. All verified by
reading the implementation.

| claim | where claimed | reality |
|---|---|---|
| "Never resubmits a row whose `done` marker is on disk … even if the status.csv row got wiped" | `scorer/supervisor.py:33-36` | **No such check in `_submit` (`:492-543`)** — I read it in full. Lose `refs/rerun_status.csv` and every row re-fires against completed CIFs. |
| "Never overwrite a done or failed row" | `scripts/queue_ops.py:19` | `cmd_mark` matches on sha alone with no state precondition and no worker-ownership check (`:166-177`); `bulk_transition` permits any state → any state (`:198-211`). |
| "keeps ≤10 concurrent fresh co-fold jobs" | `scorer/supervisor.py:1-7`, `:655` | actual default `max_concurrent: int = 25` (`:326`). |

The second enables the sharpest race in the system: `scripts/block_a_orchestrator.sh:107-112`
resets **all** claimed rows when `claimed > alive`, and its own comment concedes *"we can't
tell which are which … idempotent scoring means no harm even if a live one gets reset
alongside."* That is only true because `cmd_mark` has no ownership check — a second worker
can claim a row a first worker is still running, and one of the two `find -delete` calls
wipes the other's output mid-flight. Compounding it, `alive` is
`qstat -u sengaad1 | grep -c ' r '` (`:78`) — **every running job the user has
cluster-wide**, including rescores and other campaigns.

*Guard:* ownership check in `mark`; a lease timestamp instead of a global `alive` count.

### 9.11 The smaller ones, in one list

| # | silent failure | `file:line` | catch |
|---|---|---|---|
| a | `classify_failure` returns `TRANSIENT` on the "nothing on disk at all" fall-through — no evidence and evidence-of-transience are the same verdict | `scorer/supervisor.py:308` | a distinct `UNKNOWN` state |
| b | a qsub submission failure resets to `pending` **without** incrementing `retries` — unbounded resubmit loop | `scorer/supervisor.py:524-533` | increment on every path out |
| c | a `qstat` outage makes `_current_active` see an empty running set, so every live job is reclassified as ended and **resubmitted alongside the still-running original** | `scorer/supervisor.py:162-166`, `:423-428` | treat a qstat error as "do not reconcile", not "nothing is running" |
| d | `_row_n_samples` returns 1 for missing/empty/unparseable/non-positive — a typo'd `samples_per_seed` silently gives a 1-sample run | `scorer/rerun_dispatch.py:580-587` | fail on unparseable |
| e | a malformed `new_seed` silently substitutes `fresh_seed_for(input_sha)` — a **different seed than the manifest declares** — and the row proceeds | `scorer/rerun_dispatch.py:529-533` | fail |
| f | GPCRdb unreachable → PC3/PC4/PC5 all return `"pass"` | `scorer/pre_check.py:214-215`, `:269-270`, `:330-331` | return `unknown`, not `pass` |
| g | Step 7's manifest-shape check (the countermeasure to the 2,960-vs-4,080 bug) **SKIPs** when the builder omits its `.expected_grid.json` sidecar — opt-in by the builder it polices | `scripts/step7_dispatch_gate.py:1354-1360` | make the sidecar mandatory |
| h | the D-tier dispatch scripts downgrade the scorer-sync gate to a warning when `scorer_expected_shas.json` is absent; the three older scripts abort | `dispatch_tier_d1_smoke.sh:54-57` vs `dispatch_tier1.sh:52-64` | keep the abort |
| i | `tmux send-keys` discards every worker's exit code; a rejected `qrsh` still prints "spawned N workers" and the dispatch script exits 0 | `qsub/dispatch_tier1.sh:88-95` (and all five siblings) | post-spawn verification |
| j | the scavenger counts **tmux windows**, not live workers, so once at cap it never replaces a dead worker | `scripts/tier3_gpu_scavenger.sh:61`, `:72-73` | count live `qrsh` |
| k | `queue_ops.py pop` returns exit 1 for both "queue empty" and "strict filter matched nothing"; the worker logs "queue empty, exiting" while thousands of other-backbone rows remain | `scripts/queue_ops.py:129-130`, `scripts/block_a_worker.sh:86-89` | distinct exit codes |
| l | `rescore_watcher.sh`'s `\|\| log "rescore failed"` **can never fire** — `set -eu` without `pipefail` means the pipeline status is the `while` loop's, and `$?` in the RHS is the pipeline's, not `python3`'s. `RESCORE_DONE` is written unconditionally claiming `rescored=10` | `scripts/rescore_watcher.sh:62-79`, `:82` | `set -o pipefail`; check explicitly |
| m | `colabfold_shim`'s `runpy` ImportError fallback **returns 0 unconditionally**, discarding the backend CLI's real status | `qsub/colabfold_shim.py:192-195`, `:201-204` | propagate |
| n | `chai_patched_wrapper.py` rewrites the timeout only when it is **exactly** `6.02`, and its own log line says `-> 60.02` while the code sets `(30, 600)` | `qsub/chai_patched_wrapper.py:23-29`, `:35` | use the shim's floor logic |
| o | `rerun_protenix.sh:44` — `nvidia-smi … \| head -1 \|\| echo ""`: the pipe masks the exit status, so `\|\| echo ""` never fires, `CC` is empty, and `TORCH_CUDA_ARCH_LIST` silently falls through to the `8.0;9.0` default | `qsub/rerun_protenix.sh:44-49` | check `PIPESTATUS` |
| p | three workers run with `set -o pipefail` but **no `-e` and no `-u`** — every `mkdir`, `source` and `python3` can fail without stopping the loop | `block_a_worker.sh:15`, `h100_worker.sh:17`, `block_b_worker.sh:16` | `set -euo pipefail` |
| q | `block_a_orchestrator.sh:171` — `source …/activate 2>/dev/null \|\| true`: a missing venv means Phase 5 runs under system python, every later `python3` fails on imports, none is checked, and `DONE_MARKER` is written unconditionally at `:195` | `scripts/block_a_orchestrator.sh:171`, `:195` | check |
| r | the failure-rate circuit breaker needs `completed > 100` before it evaluates at all, and `pct = failed*100/completed` is integer arithmetic — 5.9% reads as 5 and does not exceed `MAX_FAIL_RATE_PCT=5` | `scripts/block_a_orchestrator.sh:88-98` | evaluate from row 1; use a float |
| s | `block_a_worker.sh:106` / `h100_worker.sh` still carry the **unscoped** `rm -rf /scratch/tmp/*/of3-of-sengaad1/…` glob across all co-located workers. `block_b_worker.sh:118-144` documents the damage this caused (*"Block C Tier 1 2026-09-04: 21 OF3 failures"*) and fixes it by `TMPDIR` scoping — **the fix was never back-ported** | `scripts/block_a_worker.sh:106` | back-port |
| t | `msa_prewarm.py --cache-dir` is declared at `:258` and **never read** — the docstring's "Optionally also cache locally" is inert; the only artefact is a CSV plus a side effect on a third-party server with an eviction policy nobody observes | `scripts/msa_prewarm.py:258` | drop the flag or implement it |

### 9.12 The prewarm asks for one MSA mode, and it is not the paired one

`spec/DECISIONS.md` F-6 flags this as a question. **The prewarm half of it is confirmed at
the code level.** `scripts/msa_prewarm.py:137` hardcodes the ColabFold request body as

```python
        "mode": "env",
```

— a single literal, with no paired variant and no second request anywhere in the file. The
paired artefacts the backbones actually produce are named for a different mode: Boltz writes
`msa/<N>_paired_tmp_**pairgreedy-env**/pair.a3m` alongside
`msa/<N>_unpaired_tmp_env/…` (`block_b_figure_data/03_msa_audit/PHASE_1D_EXTENSION.md:33`),
and OF3's paired hash is keyed on the concatenated multi-chain sequence, so it "necessarily
differs when either chain differs" (`:121`).

So the prewarm can only ever have warmed the **unpaired, single-sequence** search. A
two-chain arm's paired search was cold on first request; an apo arm has no paired search at
all. **That is an uncontrolled difference between the two arms the paper contrasts** — but
it is a difference in *latency and server-cache state*, not necessarily in *content*, and
this bundle cannot tell them apart.

*What would settle it, and it costs nothing:* the `_of3_colabfold_http_summary.json`
sidecars (§4.3). `colabfold_calls`, `colabfold_http_wait_s` and `cache_hit_immediate`
per prediction, compared between an apo row and a cognate row of the same receptor, answer
it directly. `cache_hit_immediate` is set only when the **first** call overall is a POST to
`/ticket/` returning `status == "COMPLETE"` (`qsub/colabfold_shim.py:138-146`), with the
comment *"If it's PENDING/RUNNING, the pre-warm didn't cover this sequence."* Note the
limitation: it can only ever be set on call #1 (`:140`), so a cache hit on a second chain is
never flagged — which is precisely the chain the paired question is about.

*Guard for the redo:* request every mode the backbones will use during prewarm, and record
the mode string on the row.

### 9.13 The pattern, in their own words

`scripts/step7_dispatch_gate.py:964-971`:

> audit trail #9, #10, #11, #12, #13 **all shared one failure shape — configuration correct
> at repo layer, dropped before the compute layer, all status signals green.**

Every finding in §9 is an instance of it. **The redo's guards must therefore live at the
compute layer, not the repo layer** — in the receipt the job itself writes, asserted against
the request the job itself received. A gate that runs on the login node before dispatch
cannot see this class at all.

---

## 10. Questions to ask paper_af3

Ranked by what each unblocks. Each is phrased so a one-line answer closes it.

**1. Was `refs/qsub_expected_shas.json` stale at dispatch time, or only at bundling time?**
Three of eight tracked launchers — `rerun_boltz.sh`, `rerun_of3.sh`, `rerun_protenix.sh`,
exactly the three carrying an `MSA_A3M_PATH` branch — do not match their pinned sha256; the
scorer pins are clean 8/8. *"For the Tier D1 full dispatch on 2026-09-06, what did
`scripts/step7_dispatch_gate.py --check qsub_files_hpc_matches_local` report, and when was
`regenerate_qsub_shas.py` last run before it?"* **Blocks:** whether the launchers we are
reading are the launchers that ran.

**2. What produced the Chai `.aligned.pqt` files for the 40 Block B decoy constructs, and
why is the decoy edit absent from their query rows?** `scripts/build_chai_msa_cache.py`
reads only `panel_receptor_sequences.fasta` and `partners.fasta` — **not**
`refs/constructs_block_b/*_decoy.fasta` — yet the depth report finds all 40 decoys cached
(`msa_depth_report.md:22`, `:26-30`), and Phase 1 §1d finds 0/40 decoy query rows carrying
the scrambled residues. *"Which script wrote the 40 decoy `.aligned.pqt` files, and does
row 0 of one of them equal the decoy sequence byte-for-byte?"* **Blocks:** whether the redo
can trust a content-addressed MSA cache at all, and the design of guard §9.2.

**3. Does `_probe_of3_runner_yaml` ever see a chunk yaml?** We read it as pointing only at
the unused top-level `_runner_seeds.yml`, so `sentinel_bug_seed_present` never evaluates the
file a chunked run reads. *"On a chunked OF3 job, is there any artefact that records the
per-chunk seeds other than the output directory names?"* **Blocks:** whether the OF3 seed
fix can be verified retrospectively on Tier D1, or only prospectively.

**4. `smoke` vs `full`.** Our manifest's 140 `prediction_path` values are all under
`…/022_tier_d1_deep_apo/smoke/…`; every receipt is under `…/full/…`, with identical
`input_sha`. *"Is there a second manifest for the `full` tree, and if so does it differ from
the smoke one in anything but the path prefix?"* **Blocks:** treating the manifest we hold
as the dispatch record for the receipts we hold.

**5. Can a spec name a receptor not in `KNOWN_RECEPTORS` and a partner not in
`partners.fasta` and run end to end — and has that ever been done?** Carried forward
unchanged from `CLAIM_VS_CODE.md:710-724`; nothing in this reading resolves it, and it still
decides whether the redo can dispatch through their harness at all.

**6. Which dispatch path ran each block?** We can see two (§1) and infer Path B for the
campaigns from `block_*_worker.sh`, but nothing states it. *"For Blocks A, B, C and Tier D1,
was dispatch via `scorer/supervisor.py` or via the tmux/`qrsh` worker pool?"* **Blocks:**
which retry semantics, which completion test, and whether `_rerun_plan.json` exists for any
given row.

**7. Is there an append-only per-row event log we have not been sent?** `last_reason` is
overwritten on every `_mark`, so attempt history is unreconstructable from what we hold.
*"Does anything record attempt-by-attempt history per row?"* **Blocks:** knowing how many
Block A–D rows are first-attempt results.

**8. The `_of3_colabfold_http_summary.json` sidecars, for one apo row and one cognate row of
the same receptor.** This closes `spec/DECISIONS.md` F-6's open question at zero compute
cost — see §9.12, where the prewarm half is already confirmed (`msa_prewarm.py:137` requests
`mode=env` only, while the paired artefacts are `pairgreedy-env`). *"Please send the
`_of3_colabfold_http_summary.json` from any two Block B OF3 rows on the same receptor, one
apo and one cognate."* **Blocks:** whether apo and cognate arms differed in MSA-server cache
state.

**9. `build_weekend.py`** — still outstanding from `spec/DECISIONS.md`. `propose.py:341-345`
says the templaters were adapted from it "with byte-parity where feasible"; **"where
feasible" is doing unknown work**, and this document's §2.3 is the redo's templater
specification. *"Please send `subsampling/scripts/weekend/build_weekend.py`, or confirm the
ten functions in `propose.py` are byte-identical in output to it."*

---

## 11. Checked and NOT a finding

Recorded so nobody re-opens these. Each was treated as our own error first.

**a. The OF3 inner-seed mismatch was our bug, not theirs.** `945550830` is the correct
output of the formula in the snapshot we were previously sent
(`received/rerun_of3.d9c646af.sh`), which has no chunking. The bundle's launcher added a
chunked branch with a different formula. Our arithmetic was right; our source file was old.
Resolved in §3.5 — and note this is the second time in this project that a discrepancy
turned out to be a version skew rather than a defect.

**b. `random.seed(pred_seed * 1_000_003 + chunk_idx)` is not a collision hazard.** With
`chunk_idx < 1_000_003` the map is injective, and chunk indices here are ≤ 3.

**c. The doubled `pool/pool` in the output paths is not a code bug.** The builder appends
`{receptor}/…` to whatever `--hpc-out-prefix` it is given
(`scripts/build_tier_d1_manifest.py:276-280`); the invocation passed a prefix already ending
in `/pool`. It parses correctly through `_POOL_PATH_RE` (`scorer/orchestrator.py:173-178`)
because the regex anchors on the *last* `/pool/`.

**d. `_SEED_FROM_PATH_RE` recovering the outer seed from an OF3 chunked path is correct.**
`re.search` returns the leftmost match, which is the dispatch seed. I checked this rather
than assuming it — but note it works by ordering, not by design.

**e. The `defensive` fallback in `build_chai_msa_cache.py:132-139` — copying *any*
`.aligned.pqt` found in the tempdir under the expected name — is not the cause of §9.2.**
`generate_colabfold_msas` is called with a single sequence into a **fresh** `TemporaryDirectory`
(`:47-55`), so the only file present is that sequence's. The branch is genuinely defensive.
It remains worth not copying into the redo.

**f. Depth 1 in the Chai cache is not a defect.** Four entries have total depth 1 —
`random_helix_40mer` (40 aa), `arrestin_Ctail` (41), `substanceP` (11), `DAMGO` (5). These
are short synthetic or peptide sequences with no homology hits beyond the query; expected,
not a cache failure (`msa_depth_report.md:378-383`). This is why the §9.1 depth guard must
be length-conditional.

**g. B1B1U5 (arachnid) and OPSD (bovine) are not MSA-depth outliers.** 7,810 and 8,701, both
mid-distribution; the a-priori concern does not materialise
(`msa_depth_report.md:128-133`). No receptor in the 48-panel falls below 1,000.

**h. Decoy MSAs are not systematically shallower than cognate.** All 40 within ±3.7% of
parent depth, mean +0.41% (`msa_depth_report.md:232-235`). ColabFold does not reject a
scrambled α5-CT — 11 residues out of 354 is too small a perturbation to shift retrieval.

**i. `n_produced == len(produced_files) == 100` in all four receipts, `exit_code == 0` in
all four, `seed == seed_passed` in all four, `env.PRED_SAMPLES == received_config.n_samples`
in all four.** No `ok=true, zero files` case exists in what we hold. The §9.4 hazard is
structural, not observed here.

**j. `rescore_parallel.provenance.json` is internally consistent.** The 16 per-worker counts
sum to exactly 14,000 = 140 rows × 100 samples; `throughput_rows_per_s`,
`mean_task_elapsed_ms` and `effective_parallel_efficiency` all recompute correctly from the
stated inputs; `n_failed: 0`. The 25 ms mean per row looked implausibly fast for a structure
parse, so it was checked — it is a *rescore* (metric recomputation) pass, not a fold, and the
arithmetic holds.

**k. Boltz's `input_yaml_sha256` cross-verifies.** `9d3090c363fb4604…` equals both the
recomputed sha256 of `received/_input_used.tier_d1_opsd_apo_boltz_seed2.yaml` and the
manifest's `input_sha` for that row. Independently, Chai's
`protein_chains[0].seq_sha256` equals the sha256 of the bare 348-residue sequence inside that
Boltz YAML — **so Boltz and Chai provably received the same OPSD sequence via two different
file formats.** A genuine positive; their provenance chain works where it is present.

**l. `assert CANONICAL_SEEDS == _EXPECTED_CANONICAL` cannot fire.**
`scripts/build_tier_d1_manifest.py:156-161` sets `_EXPECTED_CANONICAL = CANONICAL_SEEDS[:]`
two lines above the assertion, so the drift guard its comment describes (`:149-150`) is a
tautology. **Not counted as a finding** because the seed derivation is independently
verified against dispatched artefacts (§2.6), so the tautology cost nothing here — but the
redo should not copy the pattern, and it is a textbook `[[a-silent-check-looks-like-a-passing-one]]`.

**m. The scored row calling `active` on an apo rhodopsin sample is not a lifecycle finding.**
`received/rows_csv_line.txt` field 99 reads `active` against
`generic_inactive_fallback` with `ref=fallback:4X1H`. That is the scorer's business, it is
already covered by `spec/DECISIONS.md` F-1 and F-2, and it is outside this section's scope.
Noted so it is not mistaken for something new.

**n. `_BACKBONE_OUTPUT_LEAF` being wrong for every backbone is real but harmless in their
pipeline.** The scorer never opens `prediction_path`; a later `build_*_rescore_manifest.py`
enumerates files actually found on disk. It is recorded in §6.3 because **the redo's
delivery contract must not inherit the column name without the distinction**, not because it
broke anything for them.

