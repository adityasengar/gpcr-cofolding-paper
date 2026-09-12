# MAP_MSA.md — the MSA path, per backbone

**Framing: reproduction, not audit.** The question this answers is *what would we
have to stand up to run this again, and what would we be unable to reproduce even
if we did.* Where the code is wrong, that is recorded because it changes what a
re-run must do — not as a charge.

**Written 2026-09-11** from the `paper_af3` source bundle. Every claim carries
`file:line`. Two path roots are abbreviated throughout:

| abbrev | real path |
|---|---|
| `B/` | `redo/protocol/received/source_bundle/` |
| `R/` | `redo/protocol/received/` |

**Which code this is.** `R/` holds the four launchers at two pinned scorer commits
(`04243c45` = Blocks A/B, `d9c646af` = Blocks C/D). `B/qsub/` holds them at a
later HEAD. I diffed them: `rerun_chai.sh` is **byte-identical** between
`d9c646af` and `B/qsub/`; `rerun_boltz.sh`, `rerun_of3.sh` and `rerun_protenix.sh`
differ **only** by the post-`d9c646af` `MSA_A3M_PATH` pre-fetched-MSA branch
(`B/qsub/rerun_boltz.sh:118-128`, `B/qsub/rerun_of3.sh:146-157`,
`B/qsub/rerun_protenix.sh:100-110`). That branch did not exist when any scored
block ran. **So for Blocks A–D, read the launchers without it.**

---

## 1. The answer in one paragraph

Three of the four backbones fetched their MSAs **live over HTTP at prediction
time**, and the fourth read a **local per-chain cache**. Boltz and OpenFold-3
called the ColabFold public API (`api.colabfold.com`); Protenix called Protenix's
own MSA server; Chai read `.aligned.pqt` files keyed by `sha256(sequence.upper())`
from one flat directory. Boltz, OF3 and Protenix therefore **pair** alignments
when the input carries two protein chains, and Chai **does not** — Chai's cache is
built one sequence at a time and its `pairing_key` column is empty on every row of
all 120 cache files. The consequence for our redo is the one already identified:
**apo → cognate is a different operation on Chai than on the other three.** On
Boltz/OF3/Protenix, adding a partner chain adds a *new kind of alignment* (a
complex-keyed paired search) that did not exist in the apo input. On Chai, adding
a partner chain adds a second independent single-chain MSA and nothing else. Below
that headline sit two things we did not previously know: **nothing about the MSA is
recorded in the scored rows** — not depth, not source, not pairing, not a hash
(§7) — and **the paired half of every cognate prediction was fetched cold**, because
the pre-warm only ever submitted single sequences (§6.3).

---

## 2. Boltz-2 (`boltz==2.2.1`)

### Source / server / live-or-cached
`--use_msa_server`, unconditionally, at `R/rerun_boltz.d9c646af.sh:120` (and
behind the `BOLTZ_MSA_ARGS` array at `B/qsub/rerun_boltz.sh:122,132`). That flag
sends Boltz to the ColabFold public API — confirmed by `B/refs/msa_backbone_paths.md:9`
("Boltz-2 | `qsub/rerun_boltz.sh:118` | `--use_msa_server` | ColabFold public API
(`api.colabfold.com`)"). **Live**, every prediction. The observed Tier-D1 row
confirms it on a real job: `R/_boltz_status.json` →
`runtime_config.received_config.use_msa_server: true` and
`runtime_config.runtime_probe.has_msa_field: false` — the YAML shipped no MSA, so
Boltz fetched.

### Paired?
**Yes**, and the decision is not in `paper_af3`'s code — it is inside Boltz. Their
code decides it only by emitting two `protein:` entries in the YAML
(`B/scorer/propose.py:384-397`, `_boltz_yaml_two_chain`). Boltz then issues a
paired ColabFold search. Evidence is on disk, not in code:
`B/block_b_figure_data/03_msa_audit/PHASE_1D_EXTENSION.md:33` reports each Boltz
output tree carrying **both** `msa/<N>_paired_tmp_pairgreedy-env/pair.a3m` and
`msa/<N>_unpaired_tmp_env/{uniref,bfd.mgnify30.metaeuk30.smag30}.a3m`.

`B/refs/msa_input_interfaces.md:74-76` claims Boltz "derives pairing internally by
matching taxonomy strings in the a3m headers." That is their reading of Boltz
2.2.1 source, which is **not in the bundle**; the `pairgreedy-env` directory name
suggests the pairing is done server-side by ColabFold, not by header matching
locally. Unresolved — see §10 Q4.

### Exactly what changes when a partner chain is added
`B/scorer/propose.py:706-717`:
```
if apo:   base = _boltz_yaml_monomer(receptor_seq)
else:     base = _boltz_yaml_two_chain(receptor_seq, partner_seq)
```
The YAML gains a second `- protein:` block with `id: B`
(`B/scorer/propose.py:393-396`). Nothing else in the input changes — no MSA field
is written in either case (`_row_input_content` never passes `msa_a3m_path`;
see §9.1). The launcher command line is identical. Downstream of that one block,
inside Boltz: a paired search appears that had no counterpart in the apo run, and
the receptor's own unpaired MSA is (probably) unchanged. **The apo→cognate delta
is not "one more chain" — it is "one more chain plus a whole alignment axis."**

### Subsampling / depth cap / filtering
**None in their code.** No depth cap, no subsample, no filter is applied to Boltz
in any block. `B/scripts/subsample_msa.py` exists but is Tier-D3-only and
monomer-only (§6.1), and `R/README`-level provenance in
`redo/protocol/RECEIVED_LOG.md:369` records that it did not exist at `04243c45` at
all. Whatever depth cap Boltz applies internally is an upstream default we cannot
read from the bundle (§10 Q5).

### Recorded / not recorded
Recorded per job in `_boltz_status.json`: `use_msa_server` (but see §8.2),
`input_yaml_sha256`, `has_msa_field`, `has_templates_field`
(`B/qsub/status_writer.py:189-203`). **Not** recorded: MSA depth, number of
sequences, the a3m itself, whether the paired search succeeded, HTTP retry count,
ColabFold cache-hit status. Boltz *does* write its MSA into the output tree
(`PHASE_1D_EXTENSION.md:25`), which is why the Block B column audit was possible at
all — but those trees were not shipped to us.

---

## 3. Chai-1 (`chai_lab==0.6.1`)

### Source / server / live-or-cached
`--msa-directory "$CHAI_MSA_DIRECTORY"` (`B/qsub/rerun_chai.sh:135-136`), pointing
at `/hpc/scratch/sengaad1/paper_af3/msa_cache/chai` (`:130`). **Cached, local, no
HTTP at prediction time.** The header states server mode was deliberately removed:
"Server-mode dropped to prevent live-fetch storms" (`B/qsub/rerun_chai.sh:33`), and
`B/scripts/step7_dispatch_gate.py:307-324` is a hard gate that fails if
`--use-msa-server` appears anywhere in the launcher.

The cache is built by `B/scripts/build_chai_msa_cache.py`, which hits
`https://api.colabfold.com` (`:69`) via `chai_lab`'s own
`generate_colabfold_msas` (`:107,118-124`) — so the *content* is ColabFold, fetched
once, ahead of time.

**Timeline caveat that matters for reproduction.** Chai did not always run this
way. `B/refs/msa_backbone_paths.md:12` — dated 2026-09-01 — records Chai as
"*(no MSA flag)* … None — chai-lab default is single-sequence inference." And
`B/refs/PREREG.md:368` states it plainly: "Chai-1 ran **single-sequence in all prior
work** on this project… The failure mode was silent." Cache mode was wired in on
2026-09-01, before Block A. **Any Chai output predating that is single-sequence.**

### Paired?
**No.** Three independent lines of evidence, two from code and one measured:

1. `B/scripts/build_chai_msa_cache.py:118-124` calls
   `generate_colabfold_msas(protein_seqs=[seq], …)` — a **one-element list**, once
   per unique sequence, inside a fresh tempdir. A pairing key can only be assigned
   by a search that sees both chains; this search never does.
2. The cache is **deduplicated by sequence hash across the whole project**
   (`:77-81`, `unique.setdefault(seq_sha(seq), …)`). One file per sequence, shared
   by every complex that sequence ever appears in. A file that is shared across
   complexes cannot carry complex-specific pairing.
3. Measured: `B/experiments/019_block_b_partner_selection/analysis/msa_depth_report.md:56-68`
   — a full pass over all 120 cache files found `pairing_key` and `comment`
   **empty-string on every single row of every file** (`nunique()==1`, value `''`).
   The report's own words: "There is no paired-MSA-specific subset encoded in these
   columns — contrary to what the column names suggest."

For completeness: the D3 converter writes the empty pairing key explicitly —
`B/scripts/subsample_msa_chai.py:92`, `pairing_keys.append("")`, with the docstring
at `:11` calling it "empty string for unpaired". `B/refs/msa_input_interfaces.md:317-321`
confirms Chai *supports* pairing via that column; it was simply never populated.

### Exactly what changes when a partner chain is added
`B/scorer/propose.py:732-740`: a second `>protein|name=<partner>` record is
appended to the FASTA (`_chai_fasta_two_chain`, `:656-662`). At launch, the
pre-flight loop (`B/qsub/rerun_chai.sh:143-187`) hashes **each** protein record
independently (`:167`, `sha256(seq.upper())`) and requires
`<sha>.aligned.pqt` to exist (`:168-170`), hard-exiting otherwise (`:172-183`).
Chai then loads two independent single-chain MSAs and concatenates the features.

**The receptor's MSA is byte-identical between the apo and the cognate run** — same
file, same hash, same 1,996–18,146 rows. Nothing about the receptor's alignment
knows a partner arrived. That is the cleanest statement of the asymmetry: on Chai,
apo→cognate is *purely* an extra chain; on the other three it is an extra chain
plus a paired search.

### Subsampling / depth cap / filtering
None in the Block A–D path. Observed depths are whatever ColabFold returned:
receptors 1,996 (CNR2) to 18,146 (DRD2); the five canonical Gα 11,904–14,986
(`msa_depth_report.md:74-121, 161-167`). For Tier D3 only,
`B/scripts/subsample_msa.py` + `B/scripts/subsample_msa_chai.py` produce depth
arms of **full / 512 / 128 / 32 / 8** (`B/scripts/build_tier_d3_manifest.py:60`)
— see §6.1.

### Recorded / not recorded
**Best-recorded of the four.** `B/qsub/status_writer.py:148-186` writes a
`runtime_probe` listing, per protein chain, the header, the sequence sha256,
`pqt_present`, `pqt_size`, and an `all_present` roll-up — visible in
`R/_chai_status.json`. **Not** recorded: the row count inside the pqt (size in
bytes only), the pairing state, which ColabFold databases contributed, or the date
the cache entry was fetched.

---

## 4. OpenFold-3-preview (`openfold3` 0.4.4 per `R/_of3_status.json`)

### Source / server / live-or-cached
`--use-msa-server true` (`R/rerun_of3.d9c646af.sh:133`;
`B/qsub/rerun_of3.sh:166` via `$OF3_USE_MSA_SERVER`), routed through
`B/qsub/colabfold_shim.py` (`B/qsub/rerun_of3.sh:162`). **Live**, ColabFold public
API. The shim is mandatory by gate (`B/scripts/step7_dispatch_gate.py:350-359`)
because OF3 hardcodes `timeout=6.02` on `/result/download/{ID}`; the shim raises
every `api.colabfold.com` call to a floor of `(connect=30, read=600)`
(`B/qsub/colabfold_shim.py:59-60, 89-100, 120-153`).

**OF3's raw MSAs are gone.** `PHASE_1D_EXTENSION.md:93`: OF3 writes them to
`$TMPDIR/of3-of-sengaad1/colabfold_msas/{main,paired,template}/`, "per-job scratch
that is purged when the SGE job exits." Only hashed paths survive, in OF3's own
`inference_query_set.json`.

### Paired?
**Yes, and this is the one place where a `paper_af3` line of code decides it.**
`B/scorer/propose.py:485`:
```
"use_paired_msas": is_multimer,
```
inside `_of3_query_dict` (`:475-489`). `is_multimer` is hardcoded `True` for the
two-chain emitter (`:540`) and computed for the monomer emitter at `:524-525` as
`sum(1 for c in chains if c["molecule_type"].upper() == "PROTEIN") > 1`.

Confirmed on landed data: `PHASE_1D_EXTENSION.md:123` — "`use_paired_msas: true`
and both `paired_msa_file_paths` and `main_msa_file_paths` populated on every
chain."

**The count is of PROTEIN chains, not of partner chains.** A peptide ligand is
emitted as `molecule_type: "PROTEIN"` (`B/scorer/propose.py:502-504`), so a
receptor + an 11-aa peptide *ligand*, with no partner at all, flips
`use_paired_msas` to `true`. This is a sharper statement than the one
`paper_af3` gave us (`redo/protocol/RECEIVED_LOG.md:350` says only "propose.py sets
`use_paired_msas: is_multimer`") and it bears directly on the length ladder — §8.

### Exactly what changes when a partner chain is added
`B/scorer/propose.py:718-724`: `_of3_json_monomer` → `_of3_json_two_chain`. The
query JSON gains a second chain object `{molecule_type: PROTEIN, chain_ids: ["B"],
sequence: …}` (`:534-537`) **and** the query-level flag `use_paired_msas` flips
`false → true` (`:485,540`). That flag is the single most consequential
apo→cognate difference anywhere in this pipeline: it turns on an entire alignment
mode.

### Subsampling / depth cap / filtering
None applied by `paper_af3` in Blocks A–D. Two caps live upstream and we cannot
read their values from the bundle: OF3's `max_seq_counts` registry
(`B/scorer/propose.py:439-441`, named as
`openfold3/projects/of3_all_atom/config/dataset_config_components.py`), which both
caps rows per source database *and* **filters incoming a3m files by basename** —
only basenames in the registry (`colabfold_main`, `bfd_uniref_hits`, …) are read.
See §10 Q5 and §8.5.

Separately, OF3 has a **sampling** cap that is not an MSA cap but is in the same
launcher and is easy to confuse: `OF3_MAX_PER_CALL=25`
(`B/qsub/rerun_of3.sh:159`), because the fused evoformer Triton kernel fails above
~25 diffusion samples "on typical GPCR sequences (~350 aa + 150-row MSA)"
(`:140-144`). That parenthetical is the only place in the entire bundle that names
a number of MSA rows reaching an OF3 model, and it is an offhand comment, not a
measurement.

### Recorded / not recorded
Recorded: `use_msa_server` (correctly derived at `B/qsub/rerun_of3.sh:244`),
`msa_a3m_path` (`:245`), and an HTTP summary sidecar per prediction —
`_of3_colabfold_http_summary.json` with `colabfold_calls`, `colabfold_retries`,
`colabfold_http_wait_s`, `cache_hit_immediate`, `endpoints_seen`
(`B/qsub/colabfold_shim.py:64-74`). That sidecar is the **only** per-prediction
record anywhere in the pipeline of whether an MSA was served warm or computed
fresh. It was not shipped to us.

**Not** recorded: the alignments themselves (purged), depth, or which of the two
axes (main vs paired) any retry belonged to. `runtime_probe` for OF3 carries seeds
only (`B/qsub/status_writer.py:122-147`; `R/_of3_status.json`) — no MSA field at
all.

---

## 5. Protenix v2 (`protenix==2.0.0`)

### Source / server / live-or-cached
`--msa_server_mode protenix` (`R/rerun_protenix.d9c646af.sh:103`;
`B/qsub/rerun_protenix.sh:104,116`). **Live, and not ColabFold** — Protenix's own
MSA server. The launcher header flags the naming trap explicitly:
"`--msa_server_mode protenix` — NOT colabfold (naming mismatch)"
(`B/qsub/rerun_protenix.sh:12`). `B/refs/msa_backbone_paths.md:11` draws the
consequence: Protenix gets **no** benefit from the ColabFold pre-warm, "different
cache; ColabFold warm is irrelevant."

### Paired?
**Yes.** Decided inside Protenix, from the presence of two `proteinChain` entries
(`B/scorer/propose.py:614-625`). Evidence on disk:
`PHASE_1D_EXTENSION.md:62` — per-chain `msa/{0,1}/{pairing,non_pairing}.a3m`, with
row counts of 6,603–8,126 in the paired file (`:68-79`). The interfaces note
confirms the schema supports it (`B/refs/msa_input_interfaces.md:188-215`).

One useful property fell out of the Block B audit: **Protenix's paired MSA is keyed
by partner identity, not by the complex** — ADRB1 and ADRB2 share the identical
cognate paired-MSA sha `ba439d27a1bfdced` (`PHASE_1D_EXTENSION.md:70,84`). That
differs from OF3, whose paired hash is complex-keyed and therefore differs between
ADRB1 and ADRB2 on the same Gαs (`:103,105`). Two backbones, both "paired", with
different notions of what a pairing is a function of.

### Exactly what changes when a partner chain is added
`B/scorer/propose.py:725-731`: one more `{"proteinChain": {"sequence": …,
"count": 1}}` entry (`:617-620`). No flag flips in the input — Protenix decides
internally. Downstream, `pairing.a3m` appears where the apo run had only
`non_pairing.a3m`.

### Subsampling / depth cap / filtering
None applied. One upstream knob is named but unused:
`msa_pair_as_unpair` (`B/refs/msa_input_interfaces.md:259-261`), which concatenates
paired into unpaired; "Not relevant for the us-hpc path but documented in case an
ablation asks." We do not know its default (§10 Q5).

### Recorded / not recorded
**Worst-recorded of the four.** `runtime_config.msa_server_mode` is a **hardcoded
string literal** (`B/qsub/rerun_protenix.sh:137`, `'msa_server_mode': 'protenix'`)
— see §8.2 — and the `runtime_probe` for Protenix records only template-related
keys and the input hash (`B/qsub/status_writer.py:206-238`), nothing about MSAs.
`R/_protenix_status.json` shows exactly that. Protenix *does* keep its a3m files in
the output tree, which is how the Block B audit read them
(`PHASE_1D_EXTENSION.md:26`) — again, not shipped.

---

## 6. The numbers: subsampling, depth, filtering

### 6.1 Tier D3 — the only depth ladder, and it is monomer-only
`B/scripts/build_tier_d3_manifest.py:60`: `DEPTHS = ("full", 512, 128, 32, 8)`;
grid 26 receptors × 4 backbones × 5 depths × 5 seeds × 10 samples = 26,000
predictions (`:3-5`).

`B/scripts/subsample_msa.py:104-117` keeps row 0 (query), draws `depth-1` rows
uniformly with `random.Random(seed)`, sorts them back into original a3m order, and
writes atomically (`:209-213`). Byte-identical replay is self-checked (`:129-147`).

**Every D3 row is `partner_type: "apo"`** (`B/scripts/build_tier_d3_manifest.py:237`,
`state_claim: "apo"` at `:235`), and every emitted input uses a **monomer**
templater (`:187,191-198`, importing only `_boltz_yaml_monomer`,
`_of3_json_monomer`, `_protenix_json_monomer` at `:46-50`). So **the depth ladder
never crossed with a partner chain.** There is no measurement anywhere in this
bundle of how MSA depth interacts with pairing.

A doc/code mismatch worth carrying: `:59` says `"full"` means "live-fetch or no
subsample", but `msa_a3m_path_for()` returns a concrete cached path for `full`
too (`:118-120`), which sets `MSA_A3M_PATH` and therefore *disables* the live
server. `full` is a cached full fetch, not a live one. The code is right; the
comment is loose.

### 6.2 Depth-limit behaviour that does not announce itself
`B/scripts/subsample_msa.py:106-107`: if `len(entries) <= depth`, the input is
returned unchanged. A "depth 512" arm on an a3m with 300 rows is a 300-row arm,
and the manifest still records `msa_depth: 512`
(`B/scripts/build_tier_d3_manifest.py:246`). Row counts are printed only under
`--print-stats` (`subsample_msa.py:215-224`) and are not stored anywhere.

### 6.3 The pre-warm covered the unpaired half only
`B/scripts/msa_prewarm.py:135-138` submits one ticket per sequence, body
`{"q": ">query\n<sequence>", "mode": "env"}`. Never two sequences, never a pair
mode. `B/refs/PREREG.md:362` records the result: "67/67 required sequences returned
`status=COMPLETE` immediately."

Now match that against what Boltz actually asked for. Its output directories are
named `msa/<N>_unpaired_tmp_env/` and `msa/<N>_paired_tmp_pairgreedy-env/`
(`PHASE_1D_EXTENSION.md:33`). The unpaired directory's mode string — `env` — is the
pre-warm's mode. The paired directory's is `pairgreedy-env`, a different one. And
for OF3, `PHASE_1D_EXTENSION.md:121` states the paired hash "is keyed on the
concatenated multi-chain sequence."

**Therefore: every cognate-arm prediction on Boltz/OF3/Protenix paid a cold paired
search, while its apo counterpart hit a warm cache.** That is an uncontrolled
difference in wall time, in server load, and — because a cold search on a busy
public server can time out or truncate where a warm one cannot — potentially in
alignment content, between exactly the two arms the paper contrasts. Nothing
recorded it. I have not found a direct measurement confirming it and am stating it
as a code-level inference; §10 Q1 is the question that settles it.

### 6.4 Measured depths (Chai cache, the only depth data that exists)
From `msa_depth_report.md`: 48-receptor panel spans **1,996 (CNR2) to 18,146
(DRD2)**, a ~9× range (`:74-121`); no receptor below 1,000 (`:123`). Five canonical
Gα: 11,904–14,986 (`:161-167`). Forty Block B decoy Gα: all within **−3.45% to
+3.68%** of their cognate parent, mean +0.41% (`:232-235`) — ColabFold does not
reject a scrambled 11-residue α5-CT, because 340+/354 residues dominate retrieval
(`:286-296`).

---

## 7. What is recorded about the MSA afterwards — and what is not

**The scored rows carry nothing.** I grepped all four scorer modules that touch
rows — `B/scorer/schema.py`, `B/scorer/rerun.py`, `B/scorer/pocket_metrics.py`,
`B/scorer/switch_signal.py` — for `msa|a3m|pqt`: **zero matches.** (The `paired` /
`pairing` hits in those files are atom pairing and seed pairing:
`B/scorer/schema.py:503`, `B/scorer/switch_signal.py:12,208`,
`B/scorer/pocket_metrics.py:657,703`.) The one real scored row we hold,
`R/rows_csv_line.txt`, has no MSA-named field among its ~90 columns, and
`redo/protocol/ROWS_SPEC_DERIVED.md` lists none.

So: **you cannot join MSA depth, source, or pairing state to a single scored
prediction.** Not for one row, not for 42,180.

| recorded, per job | boltz | chai | of3 | protenix |
|---|:--:|:--:|:--:|:--:|
| MSA source flag | ✔ (hardcoded, §8.2) | ✔ | ✔ (derived) | ✔ (hardcoded, §8.2) |
| input file sha256 | ✔ | — | — | ✔ |
| `has_msa_field` in input | ✔ | n/a | — | — |
| per-chain MSA file present + size | — | ✔ | — | — |
| HTTP call/retry/cache-hit counts | — | n/a | ✔ (sidecar) | — |
| **MSA depth (row count)** | — | — | — | — |
| **paired vs unpaired actually used** | — | — | — | — |
| **the alignment itself** | in output tree | in cache | **purged** | in output tree |
| **anything at all, in the scored row** | — | — | — | — |

`MSA_A3M_PATH` is not in the status writer's env allowlist
(`B/qsub/status_writer.py:61-79`), so even in D3 mode only OF3 records it, and only
because its launcher copies it into `received_config` by hand
(`B/qsub/rerun_of3.sh:245`).

---

## 8. What can fail silently here

They found one. Here are the others.

### 8.1 The known one, for the record
Chai ran single-sequence while `_chai_status.json` said `ok=true`, because
`CHAI_MSA_DIRECTORY` did not propagate through `qsub -v`
(`B/qsub/rerun_chai.sh:36-42`). Closed by the per-job pre-flight at `:143-193`,
which hard-exits on any missing `.aligned.pqt`. **The countermeasure is real and I
was able to read it working** — it checks the actual input FASTA's chains against
the actual directory.

### 8.2 Two launchers record an MSA mode they do not check — HIGH, and it fires today
`B/qsub/rerun_boltz.sh:164` writes `'use_msa_server': True` as a **Python literal**
into the status JSON, on the same code path that may have just *disabled* the
server at `:123-126`. `B/qsub/rerun_protenix.sh:137` does the same with
`'msa_server_mode': 'protenix'`. OF3 gets this right — it derives the value from
the env var it actually set (`B/qsub/rerun_of3.sh:244`).

Consequence: **in D3 depth-tier mode, Boltz's and Protenix's status JSONs assert
live-server MSA while the run used a pre-fetched depth-8 a3m.** Boltz is partly
rescued by `runtime_probe.has_msa_field` (`B/qsub/status_writer.py:201`), which
reads the YAML and would say `true`. Protenix has no such probe
(`:206-238`) — for Protenix the status JSON is simply wrong and nothing
contradicts it.

### 8.3 `ok=true` still means only "exit 0 and ≥1 file"
`B/qsub/status_writer.py:312`: `"ok": args.exit_code == 0 and len(produced) > 0`.
No MSA property enters. The Chai pre-flight now prevents an *absent* MSA from
reaching `ok=true`, but a **shallow, truncated, wrong-organism or unpaired-where-
paired-was-expected** MSA produces `ok=true` on all four backbones. For
Boltz/OF3/Protenix, a ColabFold search that returns a degraded alignment under
load is indistinguishable from a good one in every artefact we hold.

### 8.4 `_ENV_KEYS` is an allowlist, so several recorded values are `null`
`B/qsub/status_writer.py:61-79` snapshots a fixed key list. Several launcher
variables are assigned **without `export`** — `BOLTZ_VENV`/`BOLTZ_CACHE`
(`B/qsub/rerun_boltz.sh:66-67`), `CHAI_VENV` (`B/qsub/rerun_chai.sh:66`), `OF3_VENV`
/`OF3_CKPT` (`B/qsub/rerun_of3.sh:51-52`), `PTX_VENV`
(`B/qsub/rerun_protenix.sh:63`) — so the `python3 -c` subprocess sees none of them.
Visible in all four received status JSONs: `boltz_venv: null`, `chai_venv: null`,
`of3_venv: null`, `of3_ckpt: null`, `protenix_venv: null`.

The MSA-relevant instance of this is **latent, not fired**:
`B/qsub/rerun_chai.sh:130` uses `: "${CHAI_MSA_DIRECTORY:=…}"`, which assigns
without exporting. Had the launcher fallen back to its own default, the status
JSON's `msa_directory` would read `null` and
`_probe_chai_msa_cache` would return `{"msa_mode": "unknown", "error": …}` with no
`all_present` key at all (`B/qsub/status_writer.py:148-159`) — a probe that
reports nothing, next to `ok=true`. It did not fire because the workers export the
variable (`B/scripts/block_a_worker.sh:69`, `B/scripts/block_b_worker.sh:70`) and
the dispatchers forward it through `qsub -v`
(e.g. `B/qsub/dispatch_tier1.sh:83-84`). `R/_chai_status.json` confirms:
`env.CHAI_MSA_DIRECTORY` is populated. **This is a hole in the recording path, not
a defect in any shipped block** — but it would fire the moment a launcher is
invoked outside a worker, which is exactly what our redo would do.

### 8.5 D3 path: paired and unpaired are set to the same file — MEDIUM, latent
`B/scorer/propose.py:471-472`:
```
chain["main_msa_file_paths"]   = [of3_path]
chain["paired_msa_file_paths"] = [of3_path]
```
and `:599-600` for Protenix:
```
pc["unpairedMsaPath"] = path
pc["pairedMsaPath"]   = path
```
When `msa_a3m_path` is a plain string rather than a dict, **every protein chain
gets the same path, and the "paired" MSA is literally the unpaired file.** Today
this is harmless because D3 is monomer-only (§6.1). The moment anyone runs a
two-chain depth arm — which our length ladder is — a partner chain silently
inherits the receptor's alignment and the paired axis becomes a duplicate of the
unpaired one. Nothing raises. `_boltz_msa_field` has the per-chain dict form
(`:358-360`, "D3 multi-chain support, currently unused") but no caller uses it.

Compounding it: `_of3_apply_msa_paths` applies to **every** chain with
`molecule_type == PROTEIN` (`:458`) — which, per §4, includes a peptide *ligand*.

### 8.6 OF3 basename filtering drops files with no error — MEDIUM, latent
`_of3_apply_msa_paths` hands OF3 the **parent directory** of the a3m, not the file
(`B/scorer/propose.py:465-470`), relying on OF3 to scan it and accept only
basenames in its `max_seq_counts` registry (`:438-441`). A file named anything
other than a registry name is skipped. `msa_a3m_path_for()` is careful to name the
file `colabfold_main.a3m` for this reason
(`B/scripts/build_tier_d3_manifest.py:114-120`) — but nothing *verifies* that OF3
accepted it. `B/refs/msa_input_interfaces.md:171-174` names the resulting failure
mode: OF3 emits "a `warnings.warn` — not a hard error — when a protein chain has no
MSA path set and no server… The result is single-sequence featurisation for that
chain."

### 8.7 OF3's chunked path overwrites its own HTTP record — LOW
`COLABFOLD_SIDECAR` is set once, to a path under `PRED_OUT_DIR`
(`B/qsub/rerun_of3.sh:136`), then the chunk loop runs a fresh process per chunk with
its own output dir (`:183,206-213`). Each chunk's `atexit` handler
(`B/qsub/colabfold_shim.py:160-176,223`) writes the **same** file. Only the last
chunk's call/retry/wait counts survive. Also: `atexit` does not run on SIGKILL, so
an OOM- or walltime-killed job leaves no HTTP record at all — and
`cache_hit_immediate` is only ever set on the very first call
(`:138-140`), so in a multi-chain job it describes one chain.

### 8.8 The depth-propagation test is weaker than its name — LOW
`B/scripts/propagation_tests/test_msa_depth_reaches_model.py` samples `head -3`
cache files (`:48-50`) and passes if **any one** has ≥5 rows (`:100`), plus two
greps of the launcher text (`:38-41`). It does not check the chains of any actual
job, any depth target, or pairing. A test named `msa_depth_reaches_model` that
passes on "one arbitrary file in a 120-file directory is not a stub" is the
project's own `[[scope-is-asserted-where-it-is-most-read]]` pattern, in a filename.

### 8.9 `clean_a3m.py` assumes strict two-line records — LOW, never ran
`B/scripts/clean_a3m.py:16-22` iterates `range(2, len(lines), 2)` treating
`lines[i]`/`lines[i+1]` as header/sequence. A wrapped (multi-line) sequence
desynchronises the pairing and mass-skips rows; the loss surfaces only as a
`skipped` count printed to stdout (`:25`) and is never persisted. It also
index-errors on `lines[1]` for a single-record file (`:13`). Scoped correctly:
`redo/protocol/RECEIVED_LOG.md:370` records that this file first appeared
2026-09-07, after both scorer SHAs — **it did not run on any shipped block.**

### 8.10 PREREG §11c overstates the MSA lock — documentation, but load-bearing
`B/refs/PREREG.md:304` and `:359`: "all four backbones feed from a pre-computed
cache, no live server dependence" / "No live ColabFold fetch is on the critical
path." The per-backbone table three lines below is accurate — "pre-warmed ColabFold
public API" for Boltz and OF3 (`:308,310`) — and `:362` spells out that the cache
in question is ColabFold's **server-side** cache. But the summary sentence says
something materially different from what the launchers do, and it is the sentence a
methods section would inherit. `:309` is worse: Protenix's cell reads "pre-warmed
ColabFold public API (mode: `protenix`), own server," which contradicts both
`B/qsub/rerun_protenix.sh:12` and `B/refs/msa_backbone_paths.md:11` in the same
cell.

For reproduction this is the whole ballgame: three of four backbones required
**live network egress to a third-party server whose cache state was not ours, not
frozen, and not recorded**. A re-run today does not re-read those MSAs; it requests
new ones.

---

## 9. Things I expected to find and did not

### 9.1 The production path never uses a pre-fetched MSA
`_row_input_content` (`B/scorer/propose.py:687-746`) — the function every manifest
row goes through — calls the templaters **without** `msa_a3m_path` at `:708,710`
(Boltz), `:721,723` (OF3), `:728,730` (Protenix). The parameter is threaded
through every emitter but only two callers ever pass it:
`B/scripts/build_tier_d3_manifest.py:187,193,197` and
`B/qsub/d3_probe_matched_structure.sh:96-100`, both monomer-only.
`R/_input_used.tier_d1_opsd_apo_boltz_seed2.yaml` confirms at the artefact level:
five lines, one protein chain, **no `msa:` field**.

### 9.2 There is no local MSA archive for three of four backbones
Boltz and Protenix wrote their alignments into each prediction's output tree
(`PHASE_1D_EXTENSION.md:25-26`); OF3's went to `$TMPDIR` and were purged (`:93`).
The only durable, portable MSA artefact in the whole campaign is Chai's 120-file
`.aligned.pqt` cache — which is the one that is **not** paired.

---

## 10. The cross-cutting question: what happens to a short peptide partner?

**The code does not special-case short chains anywhere.** I searched the full
`scripts/`, `scorer/` and `qsub/` trees for length thresholds, minimum lengths, and
skip-on-short logic. There is no length test on any MSA path, in any of the four
backbones' input generators or launchers. A peptide partner is emitted through the
*same* code as a 394-residue Gα:

| backbone | an 11-aa partner becomes | file:line |
|---|---|---|
| Boltz | a second `- protein:` block, `id: B` | `B/scorer/propose.py:393-396` |
| Boltz (as *ligand*) | a `- protein:` block, `id: L`, **no `msa:` field ever** | `B/scorer/propose.py:416-421` |
| Chai | a second `>protein\|name=…` record; pre-flight demands its `.aligned.pqt` | `B/scorer/propose.py:660`; `B/qsub/rerun_chai.sh:164-170` |
| OF3 | `{molecule_type: PROTEIN, chain_ids: [B]}`, and `use_paired_msas → true` | `B/scorer/propose.py:536,540,485` |
| OF3 (as *ligand*) | `{molecule_type: PROTEIN, chain_ids: [L]}` — **also flips `use_paired_msas`** | `B/scorer/propose.py:502-504`, `:524-525` |
| Protenix | a second `{"proteinChain": {...}}` | `B/scorer/propose.py:617-620` |

So: **no fallback to single-sequence by length, no skip, no cutoff.** Whatever
happens to a short chain happens in MMseqs2 and in ColabFold's/Protenix's servers,
not here.

### What the code *cannot* tell us, and what the measurement already says

Alignment *quality* along the ladder is not a code question and the code cannot
answer it. But `paper_af3` has already, incidentally, measured most of a length
ladder — the Chai cache holds a `.aligned.pqt` for every partner they ever
pre-warmed. From `msa_depth_report.md:351-376`:

| length | sequence | depth (rows incl. query) |
|---:|---|---:|
| 5 | DAMGO | **1** |
| 11 | substanceP | **1** |
| 15 | arrestin_FL | 84 |
| 21 | endothelin1 | 732 |
| 33 | gcn4_leucine_zipper_33 | 224 |
| 40 | random_helix_40mer | **1** |
| 41 | arrestin_Ctail | **1** |
| 71 | Gg2 | 3,191 |
| 76 | ubiquitin | 21,576 |
| 91 | KaiB_2QKEE | 7,894 |
| 126 | Nb60 | 11,934 |
| 350–394 | the five cognate Gα | 11,904–14,986 |

Read that column carefully, because it does not say what the ladder assumes.
**Depth is not monotone in length.** A 21-mer (endothelin1, 732) retrieves more
than a 33-mer (gcn4, 224). A 40-mer retrieves **one row** — itself — while a
15-mer retrieves 84. The predictor is not length; it is **whether the sequence is a
natural one with homologs in UniRef/BFD**. `random_helix_40mer` is synthetic and
`arrestin_Ctail` is an excised fragment, and both collapse to query-only. The
report's own reading (`:378-383`) agrees: "short synthetic/peptide sequences
(5-41 residues) with no homology-search hits beyond the query itself — expected for
non-natural or very short sequences, not a cache or pipeline defect."

### What this means for our ladder, 0 → 394

**The ladder is not a smooth axis. It is at least two regimes with a cliff between
them, and the cliff is not at a length.** An α5-CT fragment excised from Gα is
exactly the `arrestin_Ctail` case — a natural sequence out of its natural context,
which retrieved **one row** at 41 residues. If that behaviour holds, then:

1. **Most of our short rungs will be single-sequence in practice**, on all four
   backbones, without any code path announcing it. On Chai the pre-flight passes
   (a 1-row `.aligned.pqt` is a present file, `B/qsub/rerun_chai.sh:168-170`);
   `all_present: true` and `ok: true` are both written; the model reads one row.
2. **On Boltz/OF3/Protenix, a depth-1 partner makes the paired MSA degenerate.**
   Pairing needs homologs on both sides. A single-sequence partner means the paired
   axis carries one row regardless of how deep the receptor is — so "paired" and
   "unpaired" converge as partner length falls. The apo/cognate *operational*
   difference we identified for three backbones therefore **shrinks toward Chai's
   as the partner shortens**, which would confound any length effect with a
   pairing-mode effect. Nothing in the campaign measured this; §6.1 shows the depth
   ladder never crossed with a partner at all.
3. **A short partner may be scored as a ligand rather than a partner**, and on OF3
   that still flips `use_paired_msas` (`B/scorer/propose.py:502-504,524-525`). Our
   0-residue rung and our 11-residue rung are not "partner absent vs partner
   present" in OF3's alignment machinery unless we control the chain's
   `molecule_type` deliberately.

**Answering plainly, as asked: the code cannot tell us whether alignment quality
varies along the ladder. Only a measurement can.** The cheapest one is free of GPU:
submit each rung's sequence to the relevant server and count rows — which is
exactly what `B/scripts/msa_prewarm.py` already does (`:126-165`), and what
`build_chai_msa_cache.py` already does end-to-end (`:107-155`). Do it **before**
committing GPU to the ladder, and do it for both the unpaired and the paired query,
because §6.3 says nobody has ever measured the paired one.

---

## 11. Checked and NOT a finding

- **"OF3's query JSON has `paired_msa_file_paths` populated, but propose.py never
  passes an MSA path."** Not a contradiction. `PHASE_1D_EXTENSION.md:95-97`
  describes `inference_query_set.json`, which is **OF3's own** post-fetch record,
  not the input JSON `propose.py` emits. The input JSON has no MSA paths; OF3
  writes the fetched ones into its artefact. Verified against
  `R/_input_used.…yaml` for Boltz (no `msa:`) and §9.1.
- **`CHAI_MSA_DIRECTORY` unexported at `rerun_chai.sh:130`.** I expected a `null`
  in the status JSON. `R/_chai_status.json` shows it populated. The workers export
  it (`B/scripts/block_a_worker.sh:69`) and the dispatchers forward it
  (`B/qsub/dispatch_tier1.sh:83-84`). Downgraded to a latent recording hole, §8.4.
- **PREREG §11c says "69/69 files", `msa_depth_report.md` says 120.** Different
  scopes and dates: 69 = Block A panel + partners at 2026-09-01
  (`B/refs/PREREG.md:361`); 120 = Block A + Block B including the 40 decoy Gα at
  2026-09-03 (`msa_depth_report.md:24,320-321`). Consistent.
- **`msa_prewarm.py` uses a 16-char sequence key (`:123`) and Chai uses the full
  64 (`build_chai_msa_cache.py:58`).** Different key spaces, but they index
  different things — a CSV manifest vs a filename — and never join. Not a defect.
- **`subsample_msa.py` did not exist at `04243c45`; `clean_a3m.py` at neither
  SHA.** Confirmed against `redo/protocol/RECEIVED_LOG.md:369-370`. Scoped as
  post-campaign D3 tooling throughout; §8.9 is flagged as never-ran.
- **Boltz/OF3/Protenix launchers "changed their MSA config between campaigns."**
  They did not. My own diff of `R/rerun_*.04243c45.sh` against
  `R/rerun_*.d9c646af.sh` shows the only MSA-relevant additions are
  status-JSON `runtime_config` entries; the backbone command lines are unchanged.
  Matches `paper_af3`'s statement at `redo/protocol/RECEIVED_LOG.md:355`.
- **Protenix "benefits from the ColabFold pre-warm" (PREREG `:309`).** I first read
  this as a second contradiction of `msa_backbone_paths.md:11`. It is one — but it
  is a documentation error in a table cell that contradicts itself, not a divergence
  between two runs. Recorded at §8.10, not counted twice.

---

## 12. Questions for `paper_af3`

Ordered by how much a redo decision depends on the answer.

- **Q1 (blocking a cost estimate).** For a two-chain prediction, was the paired
  ColabFold search ever served from cache? Concretely: across the shipped Block A/B
  OF3 runs, what is the distribution of `cache_hit_immediate` and
  `colabfold_retries` in `_of3_colabfold_http_summary.json`
  (`B/qsub/colabfold_shim.py:64-74`), split by apo vs cognate? Those sidecars exist
  per prediction and were not shipped. **Cost: free** — they are already on disk.
  This is the one file in the campaign that can settle §6.3.
- **Q2 (blocking the ladder design).** Do you still hold the Boltz and Protenix
  per-prediction MSA trees (`msa/<N>_paired_tmp_pairgreedy-env/pair.a3m`,
  `msa/{0,1}/pairing.a3m` — `PHASE_1D_EXTENSION.md:25-26`)? If so, what is the
  **row count of the paired file** for an apo row versus a cognate row on the same
  receptor? That is the direct measurement of "how much does pairing actually add,"
  and §6.1 shows nobody has made it. **Cost: free.**
- **Q3 (blocking the peptide rungs).** Did any prediction ever dispatch a partner
  chain shorter than ~120 aa? `redo/spec/DECISIONS.md` records this as still open;
  the MSA path gives a second way to check it — a partner shorter than the
  nanobody would have needed its own `.aligned.pqt`, and the 24 appendix entries in
  `msa_depth_report.md:351-376` are described as "pre-warmed for exploratory Block A
  partner-diversity work," not as dispatched. Which of those 24 were ever in a
  dispatched input file? **Cost: free** (a manifest grep).
- **Q4 (methods accuracy).** `B/refs/msa_input_interfaces.md:74-76` says Boltz
  derives pairing locally by taxonomy-string matching in a3m headers, but the
  on-disk directory is named `pairgreedy-env`, which reads like a ColabFold
  server-side pair mode. Which is it — does Boltz request a paired search from
  ColabFold, or pair a single unpaired response itself? We need this to write a
  correct methods sentence. **Cost: free** (read `boltz/main.py` in the installed
  venv).
- **Q5 (reproduction parameters).** Three upstream MSA caps we cannot read from the
  bundle: OF3's `max_seq_counts` registry values and accepted basenames
  (`B/scorer/propose.py:438-441`); Protenix's default for `msa_pair_as_unpair`
  (`B/refs/msa_input_interfaces.md:259-261`); and Boltz 2.2.1's internal max MSA
  rows. A `pip show` and three greps in the venvs. **Cost: free.**
- **Q6 (scoping a sentence).** `B/scripts/step7_dispatch_gate.py:1246-1248`
  allowlists `substanceP` (11 aa) as "too short for MMseqs2 MSA search" and
  `GP161` (511 aa) as "ColabFold poll timeouts," excluding both from the pre-warm
  gate — yet `msa_depth_report.md:355` shows substanceP *does* have a 1-row
  `.aligned.pqt`. Did the ColabFold API return an error for it, or a query-only
  MSA? The distinction decides whether our short rungs will error out or silently
  run single-sequence. `refs/msa_prewarm_manifest.csv` has the ticket IDs and
  failure text (`:1251-1252`) and was not shipped. **Cost: free.**

---

## 13. What this imposes on the redo

1. **Record the MSA per prediction, or the ladder is unreadable.** Minimum per
   row: source, mode (paired/unpaired), depth of each chain's alignment, and a
   sha256 of each alignment file. §7 shows the campaign recorded none of these, and
   §6.1 shows the one depth experiment never crossed with a partner. This is the
   single highest-value change on the MSA axis.
2. **Freeze the MSAs before the GPU runs, and hold them.** Three of four backbones
   fetched live from servers we do not control (§1, §8.10). Fetch once, store the
   `.a3m`, feed the files, and record their hashes — the pre-fetched path already
   exists in the launchers (`B/qsub/rerun_boltz.sh:118-128` and siblings) and in
   `propose.py`, and just needs the two-chain wiring that §8.5 shows is missing.
   Without this, a rerun of our own ladder in six months is a different experiment.
3. **Fix §8.5 before the first two-chain depth arm.** `paired == unpaired == the
   same file` is silent and would make the partner chain wear the receptor's
   alignment. It is a four-line fix (pass the dict form that
   `B/scorer/propose.py:358-360` already supports) and it must land before, not
   after.
4. **Measure the ladder's alignments before committing GPU** (§10). Row counts per
   rung, unpaired and paired, on the real servers. Cheap, zero-GPU, and it may
   reveal that half the ladder is single-sequence — which would change the
   experiment's design rather than its interpretation.
5. **Decide, explicitly, whether the redo wants pairing held constant or varied.**
   As inherited, "add the partner" confounds three things at once on three
   backbones: an extra chain, a paired alignment axis, and a cold-vs-warm fetch. On
   Chai it confounds only the first. Whatever we choose, it should be a decision in
   `spec/DECISIONS.md` and not an inheritance.
6. **Do not reuse the campaign's Chai numbers as "MSA-mode" without checking the
   date.** `B/refs/PREREG.md:368-370` states the prior Chai corpus ran
   single-sequence and "is not comparable to the other three backbones."
