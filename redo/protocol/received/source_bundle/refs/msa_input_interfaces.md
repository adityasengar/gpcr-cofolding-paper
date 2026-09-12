# Per-backbone MSA input interface — us-hpc Cambridge path audit

Audit date: 2026-09-01. Written before authorising the switch from the ColabFold
public API to an us-hpc-local MSA fetch. The Cambridge cluster
(`us-hpc:/db/dmp/hsuchc/mmseqs2/`) has both `colabfold_envdb_202108` and
`uniref30_2302_db` — the full ColabFold-search stack — and MMseqs2/18 as a module
(verified `which mmseqs` under `module load MMseqs2/18-8cc5c-gompi-2023a`).

For each of the four Block-A backbones (Boltz-2, OpenFold-3-preview, Protenix
v2, Chai-1) this note documents:

1. The exact CLI flag or config parameter for feeding a pre-computed MSA.
2. The expected file format(s).
3. The naming / discovery convention.
4. Multi-chain (receptor + partner) handling — one MSA vs per-chain MSAs.
5. Known bugs and quirks (from prior campaigns + upstream source).

All findings verified against the installed venvs on `basel-hpc`
(`/home/sengaad1/software/venvs/{boltz,openfold3,protenix,chai1}/`) — the exact
versions the M2.4 / Round-3 pipeline is running.

Versions (as installed 2026-09-01):

| Backbone   | Package             | Version | Source root                                                                             |
|------------|---------------------|:-------:|-----------------------------------------------------------------------------------------|
| Boltz-2    | `boltz`             | 2.2.1   | `~/software/venvs/boltz/lib/python3.11/site-packages/boltz/`                            |
| OF3-preview| `openfold3`         | preview | `~/software/venvs/openfold3/lib/python3.13/site-packages/openfold3/`                    |
| Protenix   | `protenix`          | 2.0.0   | `~/software/venvs/protenix/lib/python3.13/site-packages/protenix/`                      |
| Chai-1     | `chai_lab`          | 0.6.1   | `~/software/venvs/chai1/lib/python3.11/site-packages/chai_lab/`                         |

---

## 1. Boltz-2 (`boltz==2.2.1`)

**Interface**: Boltz has NO `--msa-directory` CLI flag. Per-chain MSA paths are
specified **inline in the input YAML** (or as the third `|`-separated field of a
FASTA header when using FASTA input).

**Source of truth**:
- `boltz/data/parse/schema.py:940-1000` — YAML `sequences[*].protein.msa` field.
- `boltz/main.py:520-624` — MSA discovery: if `chain.msa_id == 0` (unset), it is
  scheduled for server fetch (requires `--use_msa_server`); if a path, Boltz
  reads it directly.
- `boltz/main.py:615-624` — accepts `.a3m` OR `.csv`, raises `RuntimeError`
  otherwise. (`.csv` is Boltz's internal format — a3m is the practical choice.)

**Format**: `.a3m` (or `.csv`). Standard a3m — the query is row 0.

**Naming**: no fixed naming — the YAML `msa:` field is the explicit path.
Any absolute filename works.

**Multi-chain**: per-chain. The YAML schema (from `schema.py:943-961`) explicitly
supports separate `msa:` per protein entity. Example (annotated from source):

```yaml
version: 1
sequences:
  - protein:
      id: A                                   # receptor
      sequence: "..."
      msa: /hpc/scratch/.../msa_cache/hash1.a3m
  - protein:
      id: B                                   # partner
      sequence: "..."
      msa: /hpc/scratch/.../msa_cache/hash2.a3m
```

If a chain has `msa:` set, Boltz uses it and does not fetch. If a chain lacks
`msa:` while another chain has one, Boltz still requires `--use_msa_server` for
the un-annotated chain (or fails). Cleanest is to fill in per-chain paths for
all protein chains (single-sequence-only chains can pass a "query-only" a3m — a
one-row file with just the query).

Boltz does NOT do explicit ColabFold-style paired-vs-unpaired columns; it takes
one a3m per chain and derives pairing internally by matching taxonomy strings
in the a3m headers.

**Known quirks**:
- If the a3m path is set but empty / missing, Boltz raises `FileNotFoundError`
  (`main.py:606-608`), not a soft fallback — verify files exist before dispatch.
- Boltz's expected a3m accepts NCBI-style headers; ColabFold's default output
  works. No prior known Boltz-side ColabFold naming mismatch.
- `--use_msa_server` and `msa:` per chain coexist fine: server-fetch only fires
  for chains with `msa_id == 0` (unset). For the us-hpc path, dispatch with
  `--use_msa_server` OMITTED and all chains carrying `msa:` — otherwise Boltz
  may still hit ColabFold for any unset chain.

**Verdict**: **pre-computed MSA supported cleanly** via per-chain `msa:` field
in YAML. Drop `--use_msa_server` from `qsub/rerun_boltz.sh` when input YAMLs
carry MSA paths.

---

## 2. OpenFold-3 preview

**Interface**: OF3 has NO `--msa-directory` CLI flag. MSA paths are specified
**per-chain in the query JSON**, as `paired_msa_file_paths` and
`main_msa_file_paths` (both accept lists).

**Source of truth**:
- `openfold3/projects/of3_all_atom/config/inference_query_format.py:60-66` —
  `Chain` pydantic model has `paired_msa_file_paths: list[FilePath|DirectoryPath] | None`
  and `main_msa_file_paths: list[FilePath|DirectoryPath] | None`.
- `openfold3/core/config/msa_pipeline_configs.py:41-47` — same fields on the
  inference-time `MsaChainDataInference` config.
- `openfold3/core/data/io/sequence/msa.py:614-618` — file extension routing:
  accepts `.a3m`, `.sto`, or `.npz` (OF3-internal serialised); directory paths
  are treated as containing multiple alignment files.
- `openfold3/core/data/tools/colabfold_msa_server.py:1000-1050` — when
  `--use-msa-server` is on, OF3 writes to
  `<out>/main/{rep_id}/colabfold_main.a3m` and
  `<out>/paired/{complex_id}/{rep_id}/colabfold_paired.a3m` — this is the
  filesystem layout OF3 expects if you skip the server and provide files
  directly.

**Format**: `.a3m`, `.sto`, or `.npz`. a3m is the practical choice for the
us-hpc path.

**Naming**: The fields are explicit lists of paths — no filename convention is
imposed. The `rep_id` above is OF3's internal SHA-derived key; when providing
paths directly, they can live anywhere.

**Multi-chain**: two separate axes:
- `main_msa_file_paths` — per-chain unpaired MSA (like Boltz's `msa:`).
- `paired_msa_file_paths` — the multi-chain paired MSA (species-aligned rows
  used only when >1 protein chain).

For a receptor + partner two-chain query, populate `main_msa_file_paths` on
each chain independently, and populate `paired_msa_file_paths` on both chains
with the same set of pairing files (one paired.a3m per chain, matched by row
index across chains).

Query JSON skeleton:

```json
{
  "queries": {
    "receptor_partner_query": {
      "chains": [
        {
          "molecule_type": "protein",
          "chain_ids": ["A"],
          "sequence": "...",
          "main_msa_file_paths": ["/.../hash1_main.a3m"],
          "paired_msa_file_paths": ["/.../pair_A.a3m"]
        },
        {
          "molecule_type": "protein",
          "chain_ids": ["B"],
          "sequence": "...",
          "main_msa_file_paths": ["/.../hash2_main.a3m"],
          "paired_msa_file_paths": ["/.../pair_B.a3m"]
        }
      ]
    }
  },
  "use_paired_msas": true,
  "use_main_msas": true
}
```

**Known quirks**:
- `--use-msa-server true` in `qsub/rerun_of3.sh:95` currently overrides any
  pre-populated `main_msa_file_paths` (see `colabfold_msa_server.py:1013-1018`
  which emits a warning and clobbers). For the us-hpc path this flag MUST be
  removed or set false.
- OF3's `rep_id` (representative id) is derived from the file's `parent.stem`
  when the file is `.a3m`/`.sto`, or the file `.stem` when `.npz`
  (`msa.py:614-620`). Two protein chains that share the same sequence should
  share the same MSA file(s); OF3 detects this via the rep_id map.
- OF3 emits a `warnings.warn` — not a hard error — when a protein chain has no
  MSA path set and no server (`msa.py:606-613`). The result is single-sequence
  featurisation for that chain. Verify the log doesn't show this warning after
  the switch.

**Verdict**: **pre-computed MSA supported cleanly** via
`main_msa_file_paths` + `paired_msa_file_paths` in the query JSON. Requires
regenerating query JSONs (or patching `scorer/propose.py::_of3_query_dict` to
plumb the paths) and dropping `--use-msa-server true` from the qsub template.

---

## 3. Protenix v2 (`protenix==2.0.0`)

**Interface**: Protenix has NO `--msa-directory` CLI flag. Pre-computed MSA is
specified **per proteinChain in the input JSON** via one of:

- `unpairedMsaPath` + `pairedMsaPath` (file paths) — **preferred, newer**.
- `unpairedMsa` + `pairedMsa` (inline a3m strings) — for programmatic input.
- `msa.precomputed_msa_dir` (directory) — **deprecated** fallback; emits a
  warning and requires filenames `pairing.a3m` + `non_pairing.a3m` inside.

**Source of truth**:
- `protenix/data/msa/msa_featurizer.py:594-635` — the exact chain object schema.
  Verbatim excerpt (line 605-635):

```python
if "proteinChain" in info:
    c = info["proteinChain"]
    seq, count, ctype, u_a3m, p_a3m = (
        c["sequence"], c["count"], PROTEIN_CHAIN,
        c.get("unpairedMsa"), c.get("pairedMsa"),
    )
    if u_a3m is None and c.get("unpairedMsaPath"):
        with open(c["unpairedMsaPath"]) as f: u_a3m = f.read()
    if p_a3m is None and c.get("pairedMsaPath"):
        with open(c["pairedMsaPath"]) as f: p_a3m = f.read()
    if u_a3m is None and (p_a3m is None):
        if c.get("msa"):
            msa_dir = c["msa"].get("precomputed_msa_dir")
            if msa_dir and opexists(msa_dir):
                logger.warning("Use the old msa json format, ...")
                if opexists(opjoin(msa_dir, "pairing.a3m")): p_a3m = read...
                if opexists(opjoin(msa_dir, "non_pairing.a3m")): u_a3m = read...
```

- `protenix/web_service/colab_request_parser.py:213-220` — same field names in
  the web request schema.

**Format**: `.a3m` for both `unpairedMsaPath` and `pairedMsaPath`. The old
`precomputed_msa_dir` fallback specifically wants `pairing.a3m` and
`non_pairing.a3m` filenames (this is the historical Protenix filename bug noted
in prior campaigns).

**Naming**: Explicit paths — no filename convention imposed. Any absolute path
resolves. Only the legacy `precomputed_msa_dir` path requires the two hardcoded
filenames.

**Multi-chain**: per-chain (per proteinChain in the input JSON). Example:

```json
[{
  "name": "receptor_partner_query",
  "sequences": [
    {"proteinChain": {
        "sequence": "RECEPTOR...",
        "count": 1,
        "unpairedMsaPath": "/.../hash1_uniref.a3m",
        "pairedMsaPath":   "/.../hash1_paired.a3m"
    }},
    {"proteinChain": {
        "sequence": "PARTNER...",
        "count": 1,
        "unpairedMsaPath": "/.../hash2_uniref.a3m",
        "pairedMsaPath":   "/.../hash2_paired.a3m"
    }}
  ]
}]
```

**Known quirks**:
- The prior "Protenix wanted a specific `bfd.mgnify30.metaeuk30.smag30.a3m`
  filename" note from `refs/msa_backbone_paths.md:19` refers specifically to
  running `--msa_server_mode colabfold` and having the fetcher return files
  named against the newer ColabFold API. That trap is **avoided entirely** by
  using `unpairedMsaPath` / `pairedMsaPath` — the input side of the featuriser
  no longer needs to guess a filename. This is the correct way to use
  pre-computed MSAs with Protenix v2.
- `msa_pair_as_unpair` (`msa_featurizer.py:606, 653`) — Protenix optionally
  concatenates paired into unpaired. Not relevant for the us-hpc path but
  documented in case an ablation asks.
- If both `unpairedMsa` inline string and `unpairedMsaPath` are set, the inline
  string wins. Don't set both.
- Per this project's `refs/msa_backbone_paths.md`, Protenix uses "receptor-only"
  MSA in prior work. That was a description of what our `scorer/propose.py`
  emits, not a Protenix constraint — Protenix itself supports per-chain MSAs
  fine. Verified in `msa_featurizer.py:585-680` (loop over `bioassembly`).

**Verdict**: **pre-computed MSA supported cleanly** via `unpairedMsaPath` +
`pairedMsaPath` per `proteinChain` in the input JSON. Requires
`scorer/propose.py::_protenix_input_json` to be extended to emit these fields,
and dropping `--msa_server_mode protenix` from the qsub template (the
`--use_msa BOOLEAN` remains default True; only the *source* changes).

---

## 4. Chai-1 (`chai_lab==0.6.1`)

**Interface**: Chai-1 v0.6.1 has an explicit `--msa-directory <path>` CLI flag
on `chai-lab fold`. **The path expected here is NOT a directory of `.a3m`
files** — it is a directory of `.aligned.pqt` files (Chai's internal parquet
format), one per unique input sequence.

**Source of truth**:
- `chai_lab/chai1.py:332-391` — `msa_directory` parameter plumbed from CLI into
  `get_msa_contexts`.
- `chai_lab/data/dataset/msas/load.py:31-85` — reads `.aligned.pqt` files by
  hash-derived basename.
- `chai_lab/data/parsing/msas/aligned_pqt.py:34-64` — schema + naming:
  - Filename: `{sha256(seq.upper()).hexdigest()}.aligned.pqt`
  - Schema (`AlignedParquetModel`, pandera): columns `sequence` (str),
    `source_database` (str, must be in RECOGNIZED_SOURCES — includes `query`,
    `uniref90`, `bfd_uniclust`, `mgnify`, `uniprot`, etc.), `pairing_key` (str,
    empty for unpaired rows), `comment` (str).
  - Row 0 MUST be the query row with `source_database == "query"`.
- `chai_lab/data/dataset/msas/colabfold.py:400-460` — the canonical
  a3m→aligned.pqt writer. This is the code path used when `--use-msa-server`
  is on; it produces exactly the format `--msa-directory` expects. This
  routine can be lifted / reused to convert a us-hpc-generated a3m to the
  `.aligned.pqt` Chai wants.

**Format**: `.aligned.pqt` (parquet, pandas DataFrame with the schema above).
NOT `.a3m` directly. Requires conversion.

**Naming**: Strict. Chai looks up `{sha256(seq.upper()).hexdigest()}.aligned.pqt`
in the directory using `expected_basename(seq)` (`aligned_pqt.py:57-60`). Any
other filename is silently ignored — Chai emits `logger.warning("No MSA found
for sequence: ...")` and falls back to single-sequence for that chain
(`load.py:51-58`).

**Multi-chain**: one `.aligned.pqt` per unique sequence in the same
`msa_directory`. Chai iterates chains, hashes each chain's sequence, looks up
the corresponding file. Two chains with the same sequence share the file. If a
chain's sequence has no matching file, Chai warns and single-sequences that
chain (silent failure, does not abort).

Pairing: unlike OF3 / Protenix, Chai pairs rows post-hoc using the
`pairing_key` column across chains. Rows in different aligned.pqt files that
share the same `pairing_key` value are paired. The ColabFold-server path
populates `pairing_key` from the paired-mmseqs2 output (see
`colabfold.py:410-440`).

**Known quirks**:
- `--use-msa-server` and `--msa-directory` are mutually exclusive
  (`chai1.py:338-345` asserts `not (use_msa_server and msa_directory)`).
- The v0.6.1 hardcoded `timeout=6.02` bug on requests to `api.colabfold.com`
  (`colabfold.py:72`) is the pain point that `qsub/chai_patched_wrapper.py`
  works around. That wrapper is only needed when using `--use-msa-server`; when
  using `--msa-directory`, no HTTP call is made and the wrapper is a no-op.
- Chai's silent single-sequence fallback for missing MSAs is dangerous — a
  hash mismatch (e.g. sequence with vs without leading Met) will look like a
  successful run but produce single-sequence quality. Post-dispatch: grep the
  Chai log for `No MSA found for sequence` before trusting the output.
- The `output_dir` empty-check bug documented in `qsub/rerun_chai.sh:81-97` is
  unchanged: `chai-lab fold` still asserts the output dir is empty. The
  existing sidecar-stash workaround still applies.

**Verdict**: **supported with quirks** — flag exists and works cleanly
(`--msa-directory`), but the a3m→aligned.pqt conversion step is bespoke.
`chai_lab.data.dataset.msas.colabfold.generate_colabfold_msas` (lines 300-460)
is the reference implementation; a small standalone converter can call the
`aligned_pqt.expected_basename` + `pandas.to_parquet` API directly against a
us-hpc a3m without going through Chai's own colabfold client. Add
`--msa-directory` to `qsub/rerun_chai.sh`; drop `--use-msa-server`.

---

## us-hpc MSA generation

Verified 2026-09-01 against a real `ssh us-hpc` login:

- **MMseqs2** available: `module load MMseqs2/18-8cc5c-gompi-2023a` → `mmseqs`
  binary at `/usr/prog/MMseqs2/18-8cc5c-gompi-2023a/bin/mmseqs` (version 18).
  Second version `MMseqs2/15-6f452-gompi-2023a` also present; module system
  default is `18` (`(D)`).
- **ColabFold DBs** on shared storage: `/db/dmp/hsuchc/mmseqs2/` — has
  `uniref30_2302_db*`, `colabfold_envdb_202108_db*`, `pdb100_230517*` (and
  their `.idx`, `.dbtype`, `_h`, `_seq` support files). Sentinel
  `COLABDB_READY` file present.
- **`colabfold_search`** NOT installed on us-hpc under `sengaad1`. Verified via
  `find /home/sengaad1 /db /usr/prog -name colabfold_search` (no hits) and
  `which colabfold_search` (not on PATH). Basel-hpc has it in the
  `pipeline-tools` venv at
  `/home/sengaad1/software/venvs/pipeline-tools/bin/colabfold_search` — a
  15-line shim over `colabfold.mmseqs.search.main`. Same package can be
  pip-installed on us-hpc.
- **Python + pip**: `/usr/bin/python3` = 3.9.25, `pip` 21.3.1 available. Both
  `/scratch` (1.6 TB) and `/hpc/scratch` (501 TB VAST) are writable.
- Host is `nrusbs-cph710302` (Cambridge, x86_64, 64 cores). Kept alive
  post-2026-08-21 (unlike the decommissioned EKS DGX). No apparent scheduler
  in front — jobs run on the login node until proven otherwise.

### One-shot install of `colabfold_search` on us-hpc

```bash
ssh us-hpc 'bash -l << "EOF"
mkdir -p /home/sengaad1/software/venvs
python3 -m venv /home/sengaad1/software/venvs/colabfold
source /home/sengaad1/software/venvs/colabfold/bin/activate
pip install --upgrade pip
# `colabfold` package brings `colabfold_search` script; alphafold extras not
# needed for MSA-only usage
pip install "colabfold[alphafold-minus-jax]==1.5.5"
which colabfold_search
EOF'
```

(Basel-hpc's pipeline-tools venv uses `colabfold-1.5.5`. Pin to the same to
avoid divergence between the two clusters.)

### Smoke-test MSA-generation command for one receptor

Under the assumption that `colabfold_search` is installed at
`/home/sengaad1/software/venvs/colabfold/bin/colabfold_search` on us-hpc:

```bash
ssh us-hpc 'bash -l << "EOF"
set -euo pipefail
module load MMseqs2/18-8cc5c-gompi-2023a
source /home/sengaad1/software/venvs/colabfold/bin/activate

WORKDIR=/hpc/scratch/sengaad1/paper_af3/msa_smoke_test
mkdir -p "$WORKDIR"
cd "$WORKDIR"

# Test with ubiquitin (76 AA, benchmark sequence from the structure-prediction skill).
cat > query.fasta << FASTA
>ubq
MQIFVKTLTGKTITLEVEPSDTIENVKAKIQDKEGIPPDQQRLIFAGKQLEDGRTLSDYNIQKESTLHLVLRLRGG
FASTA

# ColabFold_search: query fasta, DB base dir, output dir. Default flags match
# what boltz + OF3 + chai fetch from the ColabFold public API.
colabfold_search \
    query.fasta \
    /db/dmp/hsuchc/mmseqs2 \
    out_msa \
    --db1 uniref30_2302_db \
    --db3 colabfold_envdb_202108_db \
    --use-env 1 \
    --use-templates 0 \
    --pair-mode unpaired_paired \
    --threads 16 \
    --mmseqs "$(which mmseqs)"

echo "=== output ==="
ls -la out_msa/
# Expect: 0.a3m (unpaired concat) — one per query — and, if >1 query, pair.a3m.
# Single-query test: only the unpaired a3m appears.
head -5 out_msa/0.a3m
wc -l out_msa/0.a3m
EOF'
```

Expected output: `out_msa/0.a3m` — a valid a3m with the query as row 0 and
several thousand hits below (ubiquitin is very well-covered). Wall time on
64-core Cambridge login node: ~2-5 min for a single 76 AA sequence per prior
ColabFold benchmarks; probably longer for the 350-450 AA GPCR sequences
(estimate ~5-15 min/query, dominated by uniref30 search).

For a two-chain (receptor + partner) query: concatenate both sequences into
`query.fasta` and rerun. `colabfold_search` produces per-chain files
`0.a3m`, `1.a3m` (unpaired) plus a `pair.a3m` (or per-chain paired files
depending on flags) when >1 query is present.

**NOT verified end-to-end here** — this is a docs-only task, no smoke test
run. Recommend running the ubiquitin smoke test above BEFORE dispatching the
Block A pre-warm on us-hpc.

---

## Transfer + inference glue, per backbone

Assumed workflow:

```
1. On us-hpc: colabfold_search on the 48-unique-sequence set + partners →
   out_msa/{hash}_main.a3m, out_msa/{hash}_paired.a3m
2. rsync out_msa/ to basel-hpc:/hpc/scratch/sengaad1/paper_af3/msa_cache/
3. On basel-hpc: extend each backbone's input generator (scorer/propose.py) to
   plumb the cached MSA path into the input file; dispatch as usual with the
   MSA-server flag REMOVED.
4. Run inference on the 12 H100/A100 pool.
```

Per-backbone concrete plumbing:

| Backbone | Input-side edit                                                                                                                                                             | qsub-side edit                                       |
|---------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------|
| Boltz    | `scorer/propose.py::_boltz_input_yaml`: add `msa: <cached path>` to each protein entity in the YAML.                                                                        | Drop `--use_msa_server` from `qsub/rerun_boltz.sh:118`. |
| OF3      | `scorer/propose.py::_of3_query_dict`: set `main_msa_file_paths` (+ `paired_msa_file_paths` for two-chain) on each `Chain` object.                                            | Change `--use-msa-server true` → `--use-msa-server false` in `qsub/rerun_of3.sh:95` (or drop it). |
| Protenix | `scorer/propose.py::_protenix_input_json`: set `unpairedMsaPath` and `pairedMsaPath` on each `proteinChain` dict.                                                             | Drop `--msa_server_mode protenix` from `qsub/rerun_protenix.sh:103`. `--use_msa True` stays as default. |
| Chai     | Add a `scorer/msa_cache.py::a3m_to_aligned_pqt(a3m_path, out_path, seq)` helper (lift from `chai_lab.data.dataset.msas.colabfold.generate_colabfold_msas` lines 400-460), then materialise per-receptor+partner dir alongside the FASTA. | Add `--msa-directory <path>` to `qsub/rerun_chai.sh:144`, drop `--use-msa-server`, drop the `chai_patched_wrapper.py` monkey-patch route. |

### Where the workflow rubs

- **Chai's `.aligned.pqt` format** is the only non-a3m consumer. Every other
  backbone reads a3m directly. A single us-hpc a3m must be **converted twice**:
  once to `.aligned.pqt` for Chai (via a small helper) and left as `.a3m` for
  Boltz/OF3/Protenix. Both copies coexist happily in the same rsync-'d cache
  directory keyed by sequence hash.
- **OF3's paired vs main split** requires colabfold_search's `--pair-mode
  unpaired_paired` (the default). For a single-chain-only receptor prediction
  (no partner), the paired MSA is empty by definition — OF3 handles this via
  `use_paired_msas: false` at query level, or via chains with empty
  `paired_msa_file_paths`.
- **Protenix's paired MSA semantics** differ subtly from OF3/ColabFold: it
  wants the paired-mmseqs2 output (species-aligned across chains) at
  `pairedMsaPath`. `colabfold_search --pair-mode unpaired_paired` produces
  this in `pair.a3m` (or `pair_A.a3m` etc. depending on flags). The exact
  filename mapping should be verified in the smoke test — if `pair.a3m` is
  produced for the whole complex, it needs to be split per-chain before
  wiring to Protenix's per-chain `pairedMsaPath`.
- **Chai's silent single-seq fallback** is the most dangerous failure mode.
  Post-dispatch validation MUST grep the chai log for
  `No MSA found for sequence` — verify hash conversion produced the correct
  basename for every unique panel sequence. Prefer to fail-loud by wrapping
  the chai call with a pre-check that asserts every input sequence's expected
  `.aligned.pqt` file exists in the msa-directory before invoking chai.

---

## Aggregate verdict

**All four backbones accept pre-computed MSAs cleanly on the input side**:

| Backbone | Verdict |
|----------|--------|
| Boltz-2  | **pre-computed MSA supported cleanly** — per-chain `msa:` in YAML |
| OpenFold-3 | **pre-computed MSA supported cleanly** — `main_msa_file_paths` + `paired_msa_file_paths` per chain in query JSON |
| Protenix v2 | **pre-computed MSA supported cleanly** — `unpairedMsaPath` + `pairedMsaPath` per `proteinChain` in input JSON |
| Chai-1   | **supported with quirks** — `--msa-directory` flag on chai-lab fold; input must be `.aligned.pqt` (bespoke a3m→pqt conversion helper needed; silent single-seq fallback on hash mismatch) |

**Cambridge MSA-only path is viable for the full 4-backbone panel**, with two
pieces of bespoke engineering required:

1. **A small a3m → `.aligned.pqt` converter** for Chai (~30 lines, lifted
   from `chai_lab.data.dataset.msas.colabfold.generate_colabfold_msas` lines
   400-460). Not blocking — well-understood, single-file addition.
2. **`scorer/propose.py` extensions** to plumb cached MSA paths into each of
   the four input-file generators. Four small edits, one per backbone.

No backbone requires a source patch, monkey-patch wrapper, or forked upstream.
The existing `chai_patched_wrapper.py` becomes unnecessary on the us-hpc path
(no colabfold API call → the `timeout=6.02` hardcoding is irrelevant).

**Pre-flight items before committing to the plan**:

1. Install `colabfold[alphafold-minus-jax]==1.5.5` in a fresh us-hpc venv (as
   above). ~5-10 min, one-time.
2. Run the ubiquitin smoke test in `us-hpc MSA generation` above. Verify
   `out_msa/0.a3m` is non-empty and looks like a valid a3m. ~5 min.
3. Run one two-chain smoke (receptor + partner) and confirm the paired MSA
   file layout matches what each of the four backbones expects. ~15 min.
4. Then, and only then, dispatch the 48-sequence panel-wide MSA fetch.
