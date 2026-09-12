# CLAIM_VS_CODE.md — what the code they sent already answers

**Written 2026-09-11. Frame: REPRODUCTION, NOT AUDIT.** Nothing here is a charge. The
purpose is to establish what we can already answer from the 30 files in
`redo/protocol/received/`, so that the next message to `paper_af3` asks only what the
code cannot tell us. Every question we could have answered ourselves and asked anyway
spends credibility we need for the ones that matter.

## What this document is built on

| source | status |
|---|---|
| `redo/protocol/received/` — 30 files, `SHA256SUMS` present | authoritative |
| `redo/protocol/RECEIVED_LOG.md` | **RECOVERED from a transcript**, deduplicated, assistant commentary interleaved. Treated as a pointer to a claim, never as evidence for it. |
| `redo/protocol/BLUEPRINT_REQUEST.md` | 1,449 lines; 138 numbered asks + two artefact tables |

**Attribution rule applied throughout:** no file is said to do anything that was not read
in this session. Where a claim rests on a file we do not hold, that is stated rather than
inferred. Where a verdict rests on one SHA of a two-SHA pair, that is stated too.

**Held at both SHAs (diffable by us):** `axes.py`, `references.py`, and the four launchers.
**Held at one SHA only (identity across SHAs is their assertion, not our measurement):**
`propose.py`, `anchors.py`, `bw_numbering.py`, `queue_ops.py`, `colabfold_shim.py`
(asserted byte-identical at both); `pocket_metrics.py`, `subsample_msa.py` (d9c646af only);
`clean_a3m.py` (HEAD only).

---

# PART ONE — the five claims against the code

Verdict key: **VERIFIED IN CODE** / **CONSISTENT BUT NOT PROVABLE FROM WHAT WE HOLD** /
**NOT CHECKABLE HERE** / **CONTRADICTED**.

---

## Claim 1 — "No three-chain path exists in any backbone templater, so the heterotrimer was never run."

Their words, `RECEIVED_LOG.md` 2026-09-11T13:47:46 [2/3]:

> Q1 (heterotrimer): CONFIRMED never run for any arm in any block — VERIFIED via ls of
> scorer/propose.py, no three-chain path exists. Every cognate arm is receptor + one
> complete Gα subunit.

### Verdict: **SPLIT.**
- *"Exactly one partner chain; a Gα/Gβ/Gγ heterotrimer cannot be expressed"* → **VERIFIED IN CODE.**
- *"No three-chain path exists"* (as literally worded) → **CONTRADICTED.** A third chain exists — the ligand slot.
- *"Never run for any arm in any block"* → **NOT CHECKABLE HERE.** That is a manifest fact; no manifest was sent.

### The code

`propose.d9c646af.py:578-637`, `_row_input_content`, is the single dispatcher. Every
backbone branch is binary — `apo` (monomer) or not (two-chain) — and the two-chain call
takes exactly one `partner_seq`:

```
propose.d9c646af.py:599-603
    if backbone == "boltz":
        if apo:
            base = _boltz_yaml_monomer(receptor_seq)
        else:
            base = _boltz_yaml_two_chain(receptor_seq, partner_seq)
```

The same shape repeats for `of3` (`:610-615`), `protenix` (`:616-622`),
`chai` (`:623-631`) and `af2mm` (`:632-636`). The templater inventory at
`propose.d9c646af.py:353-563` contains `_boltz_yaml_monomer` / `_boltz_yaml_two_chain`,
`_of3_json_monomer` / `_of3_json_two_chain`, `_protenix_json_monomer` /
`_protenix_json_two_chain`, `_chai_fasta_monomer` / `_chai_fasta_two_chain`,
`_af2mm_fasta_monomer` / `_af2mm_fasta_two_chain` — **ten functions, five monomer and
five two-chain, and no `_three_chain` of any kind.** `partner_seq` is a single string
resolved once per spec at `propose.d9c646af.py:817-827`. There is no list, no loop, no
second partner slot. **A heterotrimer is not expressible in this code.** That is the
substantive claim and it holds.

### Why the literal wording does not hold

A **third chain is constructible** — as a *ligand*, on a separate chain id:

```
propose.d9c646af.py:604-609
        # Append ligand block (empty string when ligand_type in {none,
        # apo, ""} — the common case). Chain ID "L" avoids collision
        # with the receptor (A) and partner (B).
        ligand_block = _boltz_ligand_block(
            ligand_type, ligand_sequence, ligand_smiles, ligand_chain_id="L",
        )
        return base + ligand_block
```

and for `ligand_type == "peptide"` that third chain is a **protein** chain:

```
propose.d9c646af.py:388-393
    if ligand_type == "peptide":
        return (
            "  - protein:\n"
            f"      id: {ligand_chain_id}\n"
            f"      sequence: {ligand_sequence}\n"
        )
```

OF3 (`:432-434`), Protenix (`:492-493`) and Chai (`:536-537`) each have the same
peptide-as-protein-chain path. So receptor + partner + peptide ligand is
**three protein chains**, and `_of3_json_monomer:452-454` explicitly counts them:

```
propose.d9c646af.py:452-454
    is_multimer = sum(1 for c in chains
                      if c.get("molecule_type", "").upper() == "PROTEIN") > 1
```

This does not rescue a heterotrimer — the third chain is a ligand, not a second partner,
and nothing lets a Gβ and a Gγ both be named. But the sentence as written is wider than
the code supports, and we should not carry it forward unqualified.

### Two further qualifications we must not drop

1. **Their stated method — `ls` — cannot establish a code property.** `ls` lists a
   directory. Almost certainly a slip for `grep`/read, and their conclusion happens to be
   right on the substance, but the evidence class they gave is not the evidence class the
   claim needs. Worth one neutral line back.
2. **`propose.py` may not be the templater that built Blocks A–D.** Its own header says so:

```
propose.d9c646af.py:339-344
# These emit the exact input-file schema each fold model consumes, using
# the same shape as the frozen corpus's inputs. Adapted (byte-parity where
# feasible) from `subsampling/scripts/weekend/build_weekend.py` — the
# reference templater under the source branch that produced the frozen
# corpus's Boltz/OF3/Protenix inputs.
```

   `build_weekend.py` is **not in the 30 files and is not named anywhere in
   `RECEIVED_LOG.md`.** "Byte-parity where feasible" is not "byte-parity". See MUST ASK #1.

### What we did verify ourselves about the one dispatched input we hold

We re-derived the dispatched D1 Boltz apo YAML from `propose.py`'s templater and it is
byte-identical:

- `panel_receptor_sequences.fasta` record `OPSD` (348 aa) → `_boltz_yaml_monomer(rseq)`
  → 412 bytes, `sha256 9d3090c363fb46041e83f768f9e7b8177d2c84b9d35bff42e122ee51d7b39f1a`
- identical to `received/_input_used.tier_d1_opsd_apo_boltz_seed2.yaml` (412 B, same sha)
- identical to the `input_sha` column quoted from the manifest, and to
  `_boltz_status.json → runtime_config.runtime_probe.input_yaml_sha256`

So for that row: one protein chain, no MSA field, no templates field, no ligand, no
partner. **We reproduced their step 2 independently.** This is consistent with `propose.py`
being the templater of record for D1 — it is not proof of authorship, since a
byte-identical emitter would look the same.

---

## Claim 2 — "No arm ever supplied a peptide — every cognate arm is receptor + one complete Gα."

Their words, `RECEIVED_LOG.md` 2026-09-11T13:47:46 [2/3]:

> Q3 (Gα always full-length not peptide): CONFIRMED — _partner_fasta returns whole
> partners.fasta entries verbatim, alphas entry is 394 residues (Gs full-length). No arm
> ever supplied a 21-mer.

### Verdict: **SPLIT.**
- *"`_partner_fasta` returns whole entries verbatim"* → **VERIFIED IN CODE.**
- *"`alphas` is 394 residues"* → **VERIFIED IN THE FILE.**
- *"No arm ever supplied a peptide / a 21-mer"* → **NOT CHECKABLE HERE**, and the code and
  catalogue both make it *possible*, by three separate routes.

### What is verified

`_partner_fasta` performs a dict lookup and returns the value with no slicing, no
truncation, no length logic anywhere in the function:

```
propose.d9c646af.py:320-334
def _partner_fasta(identity: str) -> str:
    """Return the partner FASTA for a partner-identity slug.

    Reads docs/EXPERIMENT_CATALOG/sequences/partners.fasta. Empty
    identity ("") means apo — returns empty.
    """
    if not identity:
        return ""
    partners = _parse_fasta(PARTNERS_FASTA)
    key = identity.strip()
    # partners.fasta uses lowercase family names (alphas, alphai1, ...)
    for k in (key, key.lower(), key.upper()):
        if k in partners:
            return partners[k]
    return ""
```

And `received/partners.fasta` (28 records, read this session) gives
`alphas` = **394 aa**, `alphai1` 354, `alphaq` 359, `alpha13` 377, `alphat` 350 — exactly
the lengths the blueprint's D2 arithmetic assumes. So the *mechanism* is confirmed: what
`_partner_fasta` hands to chain B is a whole catalogue record.

### Why "no arm ever supplied a peptide" cannot be concluded from this

**(a) The catalogue itself stocks peptides.** Of the 28 records in the file *as dispatched*:

| record | length | category in header |
|---|---|---|
| `DAMGO` | **5** | partner_misc |
| `substanceP` | **11** | partner_misc |
| `arrestin_FL` | **15** | arrestin |
| `endothelin1` | **21** | partner_misc |
| `gcn4_leucine_zipper_33` | 33 | decoy |
| `random_helix_40mer` | 40 | decoy |
| `arrestin_Ctail` | 41 | arrestin |
| `Gg2` | 71 | partner_misc |

`_partner_fasta` returns any of these "verbatim" exactly as it returns `alphas`. Verbatim
is a statement about *truncation*, not about *length*. **`endothelin1` is a 21-mer sitting
in the partner catalogue.**

**(b) `peptide` is a documented partner type.** `propose.py`'s own YAML schema:

```
propose.d9c646af.py:29-32
    partner:
      type: g_alpha              # g_alpha / peptide / small_molecule / apo / arrestin
      identity: alphas           # partners.fasta header id, or "" for apo
      sequence_fasta: "MG..."    # optional inline override
```

and `materialise_inputs` rejects only *small-molecule* partner types, explicitly
permitting peptides:

```
propose.d9c646af.py:810-814
            f"partner.type {partner_type!r} (small molecule) is not "
            f"supported by Layer 3 input materialisation. Provide a "
            f"protein/peptide partner, or edit the spec to describe "
```

**(c) There is a route that bypasses `_partner_fasta` entirely.** The inline override is
tried *first*:

```
propose.d9c646af.py:817-827
    partner_seq = ""
    if not apo:
        partner_seq = (partner_block.get("sequence_fasta") or "").strip()
        if not partner_seq:
            partner_seq = _partner_fasta(partner_identity)
```

An arm specifying `partner.sequence_fasta` never touches `_partner_fasta` at all, so a
property of `_partner_fasta` says nothing about it. The schema also documents
`partner_perturbation: wt / truncated_Naa / shuffled / mutated / chimeric / designed`
(`propose.d9c646af.py:39`) — **`truncated_Naa` is a first-class, documented perturbation.**
`partner_perturbation` is carried onto every row (`:701`) and into the pre-checks (`:747`)
but is **not read by `_row_input_content`**, so whatever applies it lives upstream in code
we do not hold.

### What would settle it
One column of one manifest: `len(chain_B_sequence)` per arm, or the chain-B sha256 per arm
cross-referenced to `partners.fasta`. See MUST ASK #6.

---

## Claim 3 — "Three of four backbones pair their MSAs; Chai does not."

Their words, `RECEIVED_LOG.md` 2026-09-11T13:22:53 [1/2]:

> Boltz `--use_msa_server` … So Boltz PAIRS for two-chain inputs (inherited from the
> ColabFold response). Chai `--msa-directory` … Chai does NOT pair. OF3
> `--use-msa-server true --use-templates false`. propose.py sets use_paired_msas:
> is_multimer. OF3 PAIRS for two-chain. Protenix `--msa_server_mode protenix` … Protenix
> PAIRS for two-chain. VERDICT: three backbones pair (Boltz, OF3, Protenix), one does not
> (Chai).

### Verdict: **MIXED — two of four verified in code, two consistent but not provable.**

| backbone | claim | verdict | the evidence in the code we hold |
|---|---|---|---|
| **OF3** | pairs | **VERIFIED IN CODE** | pairing is an explicit field in the input file |
| **Chai** | does not pair | **VERIFIED IN CODE**, for the object supplied | the MSA handed in is per-chain, sha-keyed; nothing joint exists |
| **Boltz** | pairs | **CONSISTENT BUT NOT PROVABLE FROM WHAT WE HOLD** | only `--use_msa_server` is visible |
| **Protenix** | pairs | **CONSISTENT BUT NOT PROVABLE FROM WHAT WE HOLD** | only `--msa_server_mode protenix` is visible |

### OF3 — verified

The pairing switch is written into the query JSON by the templater, and the two-chain
constructor hard-codes it True:

```
propose.d9c646af.py:407-419
def _of3_query_dict(name: str, chains: list[dict[str, Any]], is_multimer: bool, seed: int) -> dict[str, Any]:
    return {
        "seeds": [seed],
        "queries": {
            name: {
                "query_name": name,
                "chains": chains,
                "use_msas": True,
                "use_paired_msas": is_multimer,
                "use_main_msas": True,
            }
        },
    }
```
```
propose.d9c646af.py:458-466
def _of3_json_two_chain(name: str, rseq: str, pseq: str, seed: int,
                        ligand_chain: dict[str, Any] | None = None) -> str:
    ...
    return json.dumps(_of3_query_dict(name, chains, is_multimer=True, seed=seed), indent=2) + "\n"
```

and the monomer path computes it from the protein-chain count (`:452-454`, quoted above),
so a receptor + small-molecule ligand stays unpaired while a receptor + peptide ligand
becomes paired. **`use_paired_msas` flips False → True the moment a second protein chain
appears.** This is the one place in the whole pipeline where the presence of a partner
visibly changes the MSA request.

### Chai — verified, with the right scope

`rerun_chai.d9c646af.sh:130-136` forces cache mode and refuses any other:

```
rerun_chai.d9c646af.sh:125-136
# MSA source — cache mode is the ONLY supported mode. Silent single-
# sequence fallback is the exact regression class audit trail #10
# exists to close ...
: "${CHAI_MSA_DIRECTORY:=/hpc/scratch/sengaad1/paper_af3/msa_cache/chai}"
...
MSA_FLAG=(--msa-directory "$CHAI_MSA_DIRECTORY")
```

and the in-launcher pre-flight shows exactly what "an MSA" is for Chai — **one file per
protein chain, keyed by the sha256 of that chain's sequence alone**:

```
rerun_chai.d9c646af.sh:162-170
    # Only protein chains need .aligned.pqt.
    if not hdr.lower().startswith("protein"):
        continue
    n_protein += 1
    sha = hashlib.sha256(seq.upper().encode()).hexdigest()
    pqt = msa_dir / f"{sha}.aligned.pqt"
    if not pqt.exists():
        missing.append((hdr, sha, str(pqt)))
```

There is no joint object, no pair file, no cross-chain key. **Adding a partner adds one
more independent per-chain cache file and changes nothing else.** That is a code-level
demonstration that no paired alignment is *supplied*. It is not a demonstration that
`chai-lab` does not pair internally — their evidence for that (`pairing_key` empty on
100 % of rows across 120 cache files) lives in `msa_depth_report.md:59-68`, which we do
not hold. Note also the exclusion above means a **peptide ligand**, emitted by
`_chai_ligand_fasta` as `>protein|name=lig` (`propose.d9c646af.py:536-537`), *does* require
its own `.aligned.pqt`, while a small-molecule `>ligand|…` does not.

### Boltz and Protenix — not provable here

All the code shows is the flag:

```
rerun_boltz.d9c646af.sh:119-124
boltz predict "$PRED_INPUT" \
    --out_dir "$PRED_OUT_DIR" \
    --use_msa_server \
    --cache "$BOLTZ_CACHE" \
    --devices 1 --accelerator gpu \
    --recycling_steps 3 --diffusion_samples "$N_SAMPLES" --sampling_steps 200 \
```
```
rerun_protenix.d9c646af.sh:104
    --msa_server_mode protenix \
```

Nothing in either names pairing, and nothing changes between the apo and two-chain
invocations — the *input file* gains a chain, the *command line* does not. Their evidence
is `PHASE_1D_EXTENSION.md:56` (Boltz paired/unpaired subdirectories) and `:60` (Protenix
`pairing.a3m` / `non_pairing.a3m`), neither of which we hold. It is a perfectly reasonable
reading of on-disk artefacts; it is simply not in the code.

### The MSA plumbing we hold does not act on any block of record

- `subsample_msa.d9c646af.py` is D3 depth-ladder tooling; its own docstring pins it to
  `refs/PREREG.md` amendment §D-3.7 and it takes `--seed` with a byte-identical replay
  self-check (`subsample_msa.d9c646af.py:1-33`, `:129` `selfcheck_deterministic`).
- `clean_a3m.HEAD.py` is 26 lines and exists only at HEAD.

Neither can have run on Blocks A/B. `subsample_msa.py` also states plainly that Chai is
outside its reach — *"Chai uses `.aligned.pqt` (converted separately by
`scripts/subsample_msa_chai.py`, TODO)"* (`:8-9`). **That converter is named as a TODO and
is not in any artefact list we sent.**

---

## Claim 4 — "The predicate axes are byte-identical between the two campaigns."

### Verdict: **VERIFIED IN CODE, for `axes.py` — and stronger than the claim as stated.** With one dependency caveat.

We diffed both files ourselves.

**`axes.04243c45.py` (20,454 B) vs `axes.d9c646af.py` (21,534 B):**
- `diff` reports **27 added lines, 0 deleted lines.** Every added line is in one block at
  the top of the module (`axes.d9c646af.py:44-70`): re-export imports from
  `scorer.pocket_metrics` and `scorer.post_run_receipts`, with a comment saying exactly
  that — *"Backward-compat re-exports — pocket metrics landed in scorer/pocket_metrics.py …
  the implementation lives in the sibling module."*
- We then compared the two files at AST level, function by function and class by class:
  **0 definitions added, 0 removed, 0 changed.** Every function body is byte-identical.
- Specifically byte-identical: `d_npxxy_y558_y753_oh`, `d_gpcrdb_tm6_tilt_246_637_ca`,
  and their entire call chain — `_anchor_pos`, `_ca_at_bw`, `_dist`, `_ca`, `_atom` — plus
  `compute_all_axes` and the module constants `AXIS_APPLICABILITY`, `_A100_PAIRS`,
  `_A100_COEFFS`, `_A100_INTERCEPT`.

So: **the files are not byte-identical; every executable definition in them is.** That is
the accurate form of the sentence and it is the form that supports the conclusion.

Neither predicate function reads the reference set. Both take only `model`:

```
axes.d9c646af.py:190-191, 203-204
def d_npxxy_y558_y753_oh(model: VerifiedModel) -> float:
    ...
    p558 = _anchor_pos(model, "5.58")
    p753 = _anchor_pos(model, "7.53")
```
```
axes.d9c646af.py:318-326
def d_gpcrdb_tm6_tilt_246_637_ca(model: VerifiedModel) -> float:
    """GPCRdb primary cross-class TM6 tilt marker: 2.46 CA -- 6.37 CA (Å).
    ...
    return _dist(_ca_at_bw(model, "2.46"), _ca_at_bw(model, "6.37"))
```

`axes.py` imports nothing from `scorer.references` at either SHA (import list is
`math`, `typing`, `gemmi`, `scorer.verified`, plus the two re-export blocks at d9c646af).
**Their statement that "neither reads the reference set" is confirmed.**

**`references.04243c45.py` (14,870 B) vs `references.d9c646af.py` (17,369 B):** we diffed
this too. The change is **purely additive**. `_role_for_state`, `check_reference_class`,
`check_species`, `compute_deltas`, `empty`, `load_uncovered_receptors`, `receptors` are
all byte-identical. `ReferenceRow` gains a `role_specific: str = ""` field;
`ReferenceLookup` gains `inactive_by_role_specific: dict[str, ReferenceRow]`;
`ReferenceSet.__init__` gains a parallel `_inactive_by_specific` index and `load_for`
populates it. `.active` and `.inactive` are unchanged. Their summary of this
(2026-09-11T13:19:12, Q_REFS_1) matches what we read.

### The caveat that must travel with this verdict

The predicate value is `_anchor_pos(model, "5.58")` etc., and those positions come from
`anchors.py` → `bw_numbering.py` → `VerifiedModel`. We hold `anchors.py` and
`bw_numbering.py` **at one SHA only**, and `verified.py`, `structure.py`, `schema.py` at
**neither**. Their assertion that `anchors.py` and `bw_numbering.py` are byte-identical
across SHAs is plausible and specific, but we did not measure it — we cannot, having been
sent one copy of each. So the correct sentence for the Methods is:

> The predicate axis *implementations* are byte-identical between campaigns (measured).
> The anchor-resolution modules they depend on are reported byte-identical (not measured
> here — one copy held).

One cheap ask retires this: the sha256 of `anchors.py` and `bw_numbering.py` at
`04243c45`. See MUST ASK #9.

### Independently confirmed against the row we hold

`received/rows_csv_line.txt` (the finished D1 OPSD × boltz × apo line) carries
`12.470604390750273` and `14.014953229750716` — matching to the last digit the values they
quoted in the trace, alongside `9.08` / `14.932` and
`thresholds_panel_csv_sha256 = 242b509f7b7af56669d72cd71906d91edd18ef43706c21d23a8be5bf1e08366b`,
`ref_set_csv_sha256 = 7a261988ff73eedc…`, `scorer_git_sha = d9c646af…`,
`cache_key = 3500b88e75b638f3…`, `seed_used = 1800878580`. Every value they quoted from
that line is in the file.

---

## Claim 5 — "ColabFold's public API is an unpinnable live dependency."

### Verdict: **VERIFIED IN CODE** that it is live, unversioned and unarchived in this pipeline. **"Unpinnable" is overstated** — the same repo pins two other network dependencies, and pins ColabFold for Chai.

### Live: verified

`colabfold_shim.d9c646af.py` monkey-patches `requests.get`/`requests.post` at module level
and treats any URL containing `api.colabfold.com` as a live call, at inference time:

```
colabfold_shim.d9c646af.py:103-104
def _is_colabfold(url: str) -> bool:
    return "api.colabfold.com" in url
```

The shim records **only** call counts, retry counts, cumulative HTTP wait, normalised
endpoints and a `cache_hit_immediate` boolean (`:70-79`, `:107-119`). It never records a
database version, a ticket id, a server build, or the returned alignment. There is no
`--write-msa`, no a3m archive path, no snapshot flag anywhere in `rerun_boltz.*.sh` or
`rerun_of3.*.sh`.

For the one row we can trace end to end, the MSA was demonstrably fetched at prediction
time, not shipped: the input YAML we reconstructed byte-identically contains no MSA block,
and `_boltz_status.json` stamps it:

```
_boltz_status.json → runtime_config.runtime_probe
    "input_yaml_sha256": "9d3090c363fb46041e83f768f9e7b8177d2c84b9d35bff42e122ee51d7b39f1a"
    "has_msa_field": false
    "has_templates_field": false
received_config.use_msa_server = true
```

So their conclusion for this row — *"this specific MSA cannot be regenerated, only
re-requested, and a re-request today would return different alignments"* — follows from
artefacts we hold. **Verified.**

### Why "unpinnable" is the wrong word, and a useful correction to carry

Three network dependencies appear in the code we hold, and they are pinned to three
different degrees:

| dependency | pinned? | evidence |
|---|---|---|
| GPCRdb `residues/extended`, `protein/accession`; EBI SIFTS | **yes** — on-disk JSON cache keyed by natural key, **and** the payload sha is stamped per row | `bw_numbering.d9c646af.py:19-21, 50-66, 100-171`; `rows_csv_line.txt` field 17 = `b3a320351982c749…` |
| ColabFold, for **Chai** | **yes** — materialised once into `.aligned.pqt`, keyed by sequence sha256, and the launcher refuses to run without it | `rerun_chai.d9c646af.sh:125-190` |
| ColabFold, for **Boltz** and **OF3** | **no** — live per prediction, nothing retained | `rerun_boltz.d9c646af.sh:120`; `rerun_of3.d9c646af.sh:141` |

The pipeline therefore already contains the mechanism that would pin it. The accurate
Methods sentence is *"the ColabFold alignments for Boltz and OF3 were fetched live and not
archived, so those two backbones' inputs cannot be reconstructed"* — which is a statement
about the campaign, not about the service, and is both defensible and cheaper to defend.

### One asymmetry worth naming, found in passing

`rerun_of3.d9c646af.sh:137` routes OF3 through the shim and writes
`_of3_colabfold_http_summary.json`. **`rerun_boltz.d9c646af.sh` does not invoke the shim
at all** — it calls `boltz predict` directly (`:119`). So for Boltz there is no record of
the ColabFold interaction whatsoever: no call count, no retry count, no cache-hit flag.
The shim's own docstring lists Boltz as a supported usage (`colabfold_shim.d9c646af.py:34`)
but the launcher does not use it. Relevant to C3 and to how we word the reproducibility
boundary per backbone.

---

## Claim-check summary

| # | claim | verdict |
|---|---|---|
| 1 | no three-chain path / heterotrimer never run | one partner chain **VERIFIED**; literal "no three-chain path" **CONTRADICTED** (ligand chain L); "never run" **NOT CHECKABLE** |
| 2 | no arm supplied a peptide; every cognate arm is one complete Gα | `_partner_fasta` verbatim + `alphas`=394 **VERIFIED**; "no peptide ever" **NOT CHECKABLE** — catalogue holds a 5-mer, an 11-mer, a 15-mer and a 21-mer, and two routes bypass `_partner_fasta` |
| 3 | 3 of 4 pair, Chai does not | OF3 pairs **VERIFIED**; Chai supplied per-chain only **VERIFIED**; Boltz & Protenix **CONSISTENT, NOT PROVABLE HERE** |
| 4 | predicate axes byte-identical across campaigns | **VERIFIED** (0 definitions changed in `axes.py`; `references.py` purely additive) — files differ by 27 import lines; anchor-module identity **not measured** (one copy held) |
| 5 | ColabFold is an unpinnable live dependency | live & unarchived for Boltz/OF3 **VERIFIED**; "unpinnable" **overstated** — pinned for Chai, and GPCRdb/SIFTS are cached and sha-stamped |

**Two of five fully verified as stated; three need their wording tightened before they enter a sentence.** None is wrong in substance.

---

# PART TWO — the blueprint, triaged

138 numbered asks. Counted by us and independently by a second pass: §1 ①–③ (3),
A (8), B (11), C (13), D (6), E (43), F (9), G (12), H (8), I (6), J (6), §12 Q (13),
plus the §13.1 / §13.2 artefact tables (18 + 11, unnumbered).

**Headline: we can now answer 34 outright and substantially narrow another 27. 77 remain
genuinely unanswerable from what we hold — but 30 of those are judgement, willingness or
history questions that were never code questions (all of J, most of H, A3, A5, G8).**

| | count |
|---|---|
| **ANSWERABLE FROM WHAT WE HOLD** | **34** |
| **PARTIALLY ANSWERABLE** | **27** |
| **MUST ASK** | **77** |

---

## ANSWERABLE FROM WHAT WE HOLD (34)

Do not re-ask any of these. The answer column is what we now hold; the file column is
where to point in our own Methods.

| id | answer | file |
|---|---|---|
| **§1 ②** | Delivered in full — 8 launchers (both SHAs) + shim + queue_ops + subsample_msa + clean_a3m. | `received/rerun_*.{04243c45,d9c646af}.sh` etc. |
| **§1 ③** | Delivered, and **independently re-verified by us**: panel FASTA → templater → 412-byte YAML → manifest `input_sha` → status-JSON probe, all one sha256. | see Claim 1 |
| **B1** | **SGE / Grid Engine.** `#$ -N/-cwd/-o/-j/-l/-pe` directives, `$SGE_HGR_gpu_card`, `$JOB_ID`, `qsub -v`. Resources per row below. **No array jobs** — no `#$ -t` in any of the eight launchers. | `rerun_*.sh:20-33`; `queue_ops.d9c646af.py:140` |
| **B6(ii)** | **A retried job gets the same seed.** `queue_ops pop` re-reads `new_seed` from the queue CSV; the seed is a property of the row, not of the attempt. | `queue_ops.d9c646af.py:145` |
| **C1** | **Yes.** One receptor sequence and one partner sequence are resolved once per spec and wrapped per backbone. The only per-backbone input difference beyond the wrapper is OF3's `use_paired_msas` and the chain-id convention. | `propose.d9c646af.py:795-827, 578-637` |
| **C2** | Confirmed verbatim: Chai `--msa-directory` (cache); Boltz `--use_msa_server`; OF3 `--use-msa-server true` via the shim; Protenix `--msa_server_mode protenix`. **Unchanged between the two SHAs** — we diffed all four pairs; the only MSA-relevant additions at d9c646af are `runtime_config` status-JSON entries. | `rerun_chai:135`, `rerun_boltz:120`, `rerun_of3:137-141`, `rerun_protenix:104` |
| **C8** | **Receptor = A, partner = B, ligand = L** for Boltz and OF3, by construction. Chai: receptor record first, partner second, ligand last. **Protenix carries no chain ids at all** — a positional `sequences` list — which is the mechanism behind the "chain-to-subdir order not stable" observation in C5. No ions, lipids or waters in any templater; tags are whatever the FASTA carries (no stripping code exists). | `propose.d9c646af.py:363-374, 458-466, 507-517, 547-554` |
| **D5** | **Confirmed: single-partner-chain throughout; a Gα+Gβ+Gγ input is a harness change, not a config change.** See Claim 1. | `propose.d9c646af.py:578-637` |
| **D6 (first half)** | `GASR` is **still mislabelled in the file as dispatched** — header reads `category=Gα`, length 396, and it is the gastrin receptor. No `Nb60` record exists in `partners.fasta` at all (nanobodies live elsewhere). | `received/partners.fasta` |
| **E2a** | **The scorer does NOT use the census script's linear-offset rule.** `anchors.py` resolves each of the six anchors by direct lookup in the GPCRdb `residues/extended` payload; `pocket_metrics.resolve_pocket_uniprot_positions` builds a reverse index of the same payload. No offset arithmetic anywhere. **E2b/E2f therefore apply to the census script only, not to the predicate axes.** | `anchors.d9c646af.py:63-85`; `pocket_metrics.d9c646af.py:238-265` |
| **E3 (part)** | Anchor positions come from GPCRdb `residues/extended`, per entry, cached on disk and sha-stamped into `AnchorSet.residues_ext_payload_sha256`. An unresolvable anchor is simply absent from the dict; `A2FASTATrunc` fires on access. | `anchors.d9c646af.py:63-88`; `bw_numbering.d9c646af.py:118-150` |
| **E4** | The twelve are canonical and confirmed verbatim: `3.32 3.33 3.36 5.42 5.43 5.46 6.48 6.51 6.52 6.55 7.39 7.42`. Predicate anchors: `5.58`/`7.53` (NPxxY OH–OH), `2.46`/`6.37` (GPCRdb tilt), `3.50`/`6.30` (Class A primary). The scorer's six resolved anchors are `3.50 3.51 5.58 6.30 6.34 7.53`. | `pocket_metrics.d9c646af.py:81-89`; `anchors.d9c646af.py:1-11` |
| **E5 (7 of 8)** | Exact atoms, from the code: `d_npxxy_y558_y753_oh` = OH(5.58)–OH(7.53); `_ca` = CA(2.46)–CA(6.37) for the tilt; `d_tm6_r350_r630_ca` = CA(3.50)–CA(6.30); `d_npxxy_y558_y753_ca` = CA–CA; `d_tm5_outward_r350_r558_ca` = CA(3.50)–CA(5.58); `d_dry_sidechain_r350cz_e630oe1` = CZ(3.50)–OE1/OD1(6.30). **`d_y558_pack_min_heavy` is a minimum over an explicit set:** all non-H, non-CA atoms of residues in `range(p350-3, p350+4) ∪ range(p630-3, p630+4)`, excluding 5.58 itself. | `axes.d9c646af.py:140-265` |
| **E8c** | **Class B and Class F get no pocket at all.** `resolve_pocket_uniprot_positions` short-circuits to `({}, POCKET_BW_LABELS)` for unsupported classes; pocket RMSDs return NaN with a deferred note. There is no second pocket definition. | `pocket_metrics.d9c646af.py:238-250, 221-236` |
| **E8d** | A BW label becomes an atom in two hops, both GPCRdb-cache lookups, no arithmetic: `get_generic_numbers` → `lookup_bw` → UniProt position → `model.residues.get(pos)` → `find_atom(name)`. | `bw_numbering.d9c646af.py:118-180`; `axes.d9c646af.py:115-137` |
| **E8e** | **Satisfied.** Both files received and hash-verified. | — |
| **E12** | `ligand_rmsd_to_ref` computes and annotates; **it gates nothing.** It returns `(NaN, note, method)` on every failure class and the row proceeds. Its docstring says explicitly *"Consumers must filter decoy_lig rows"* — the filtering is downstream, not in the scorer. | `pocket_metrics.d9c646af.py:667-740` |
| **E13 (part)** | `plddt_mean` = unweighted mean over residues of (mean `b_iso` across that residue's non-NaN atoms). `plddt_at_anchors` = the same per-residue value at each of the six anchors, NaN where the residue is absent. **Mean, not median.** | `axes.d9c646af.py:476-500` |
| **E14** | **The scorer makes no per-backbone distinction.** `_residue_plddt` reads `at.b_iso` for every structure, with the comment *"For co-folding outputs (Boltz, OF3, Protenix, AF2) this is pLDDT."* There is **no scale check and no per-backbone branch** anywhere in the extraction. That is the answer to "is the extraction verified to be on the same scale for all four" — it is assumed, not verified. | `axes.d9c646af.py:476-483` |
| **E15** | **No.** `compute_all_axes` emits 17 keys — six axes, ICL2, two pLDDT, five A100 components, the A100 index and the Class B kink. No PAE, ipTM, pTM or per-chain pLDDT is captured anywhere in the code we hold. | `axes.d9c646af.py:509-541` |
| **F4 (pocket layer)** | For the pocket columns the rule is **selection, never aggregation**: `_role_for_state_claim` maps (state_claim, ligand_role) → (role, role_specific); a `role_specific`-tagged inactive is preferred; the generic inactive is the fallback and is tagged `generic_inactive_fallback` in `pocket_ref_role_inactive`. For `apo`, role is `None` and the **active** reference is used. | `pocket_metrics.d9c646af.py:842-905, 1066-1090, 1210-1233` |
| **H5** | **Yes, at d9c646af there is an executed dispatch-time byte check** — not only a construction argument. The launcher's `runtime_probe` stamps `input_yaml_sha256` on the compute node, and for the D1 row it equals the manifest's `input_sha` and our own `shasum` of the file. Three independent points, one sha. (At `04243c45` there is no `runtime_config` block, so no such check — see B9.) | `_boltz_status.json`; `received/_input_used.*.yaml` |
| **I2 (part)** | **`input_sha` and `input_sha256` are two different objects.** The manifest's `input_sha` = sha256 of the *input file we wrote* (`content_sha256(input_path)`, `propose.d9c646af.py:844`). `rows.csv`'s `input_sha256` = sha256 of the *output CIF* (`e5ceec00c1d89192…` in the line we hold). Similar names, opposite ends of the run. Worth stating in the Methods. | `propose.d9c646af.py:844-859`; `rows_csv_line.txt` field 1 |
| **§13.1-1,2,4,5,6,7,9,10,11,12** | **Satisfied** — `pocket_metrics.py`, `bw_numbering.py`, `axes.py` (both SHAs), `anchors.py`, `references.py` (both SHAs), `propose.py`, the four launchers (both SHAs), `colabfold_shim.py`, `queue_ops.py`, `subsample_msa.py`, `clean_a3m.py` all received and hash-verified. | `received/SHA256SUMS` |
| **§13.2-3 (partial), 13.2-4, 13.2-5 (partial)** | `partners.fasta`, `gpcr_coupling.csv` and `panel_receptor_sequences.fasta` received. | `received/` |

### Per-backbone facts now readable off the launchers (covers A4 partly, A6 partly, A7 partly, B1, C6 partly)

| | Boltz | Chai | OF3 | Protenix |
|---|---|---|---|---|
| env | venv `venvs/boltz` + `--cache $BOLTZ_CACHE` | venv `venvs/chai1` | venv `venvs/openfold3` | venv `venvs/protenix` + `module load CUDA/12.1.1` |
| checkpoint pinned? | no | no | **yes** — `--inference-ckpt-path .../of3-p2-155k.pt`, existence-checked | no |
| recycles | `--recycling_steps 3` | `--num-trunk-recycles 3` | (in runner yaml) | `--cycle 3` |
| diffusion | `--sampling_steps 200` | `--num-diffn-timesteps 50` | — | `--step 50` |
| samples | `--diffusion_samples N` | `--num-diffn-samples N` | `--num-diffusion-samples N` | `--sample N` |
| seed flag | `--seed` | `--seed` | **runner yaml `experiment_settings.seeds`** (see B4) | `--seeds` (plural — singular exits non-zero) |
| templates | no flag; `has_templates_field:false` observed | not in launcher | **`--use-templates false` explicit** | not in launcher |
| SGE | `h_rt=04:00:00 m_mem_free=8G gpu_card=1 pe smp 4` | `06:00:00 8G 1 4` | `05:00:00 16G 1 4` | `05:00:00 16G 1 4` |
| runtime version capture | `boltz 2.2.1` + venv source_path, observed | `chai_venv` path only | `of3_venv` + `of3_ckpt` paths | `protenix_venv` path only |

**No launcher stamps its own git sha anywhere**, at either SHA. Config echo exists at
d9c646af; identity echo exists nowhere. (Their own summary of this, 2026-09-11T13:24:46,
matches what we read.)

---

## PARTIALLY ANSWERABLE (27) — with the single question that closes each

| id | what we can already infer | the one question that closes it |
|---|---|---|
| **§1 ①** | 8 of the module received; `pocket_metrics`/`anchors`/`bw_numbering`/`propose` at one SHA only. Missing and imported-by-what-we-hold: `verified.py`, `structure.py`, `schema.py`, `receptors.py`, `rerun.py`, `cache.py`, `pre_check.py`, `assertions.py`, `partner_metrics.py`, `post_run_receipts.py`, `fold_integrity.py`, `_version_sha.py`. | "Send `scorer/` as a tarball at each SHA — the remaining 12 modules, not one at a time." |
| **A1** | No lockfile is referenced anywhere in the eight launchers. Pinning is four venv *paths* plus `module load CUDA/12.1.1` and `proxy/GLOBAL`. A path is not a pin. | "Does a `pip freeze` / lockfile exist for each of the four venvs, and does it still exist today?" |
| **A2** | We can enumerate from code what is unpinned: ColabFold DB (Boltz, OF3), backbone package versions (3 of 4), weights for 3 of 4. Pinned: GPCRdb + SIFTS (cached, sha-stamped), Chai's MSA (sha-keyed cache), OF3 checkpoint (filename). | The three named sub-bullets (phantom SHA, `no-git` subtrees, empty generator SHAs) are repo-history questions — see MUST ASK #5. |
| **A4** | OF3 checkpoint filename in code; Boltz 2.2.1 + source_path in the status JSON. | "Package version and weights sha for Chai, Protenix and OF3 — from the venvs as they stand." |
| **A6** | `gpu_card=1` on all four, `CUDA_VISIBLE_DEVICES` from `$SGE_HGR_gpu_card`; one observed host `nrchbs-cph510076`, `gpu2`. **No precision or TF32 setting appears in any launcher** — so none was set explicitly. | "Which GPU model served each block, and was the default precision the same on all of them?" |
| **A7** | One data point: Boltz, OPSD apo, 100 samples, `18:40:06Z → 18:44:11Z` ≈ **4 min wall**. Wall limits requested: 4/6/5/5 h. | "Same number for the other three backbones, and for receptor+partner." |
| **B2** | The `propose.py → input file → qsub` leg is verified byte-exactly. | See MUST ASK #1 — which templater built the dispatched corpus. |
| **B3** | `rescore_parallel.provenance.json` names `manifest_path: /home/sengaad1/paper_af3/...` — an **HPC home path**, while the trace prose says the rescore manifest is "on laptop". | "Was the D1 full rescore run on HPC or on the MacBook? The provenance JSON's manifest path is under `/home/sengaad1/`." |
| **B4** | Row seeds are deterministic: `_derive_row_seed` = `fresh_seed_for(sha256(f"{request_id}|{backbone}|{seed_index}"))` (`propose.d9c646af.py:645-652`). OF3's inner seed has an explicit formula in the launcher: `random.seed(PRED_SEED); [randint(0, 2**32-1) for _ in range(N_SEEDS)]` → `_runner_seeds.yml` (`rerun_of3.d9c646af.sh:100-113`). **We tested it: `random.seed(1015473677)` gives `945550830`, not the observed inner seed `2344327426`.** We also tried ±8 offsets, indices to 500, and string seeds — no match. | See MUST ASK #4. |
| **B6(i,iii,iv)** | `queue_ops` gives the machinery: states `pending|claimed|done|failed`, fcntl-locked, `os.replace`. The docstring asserts *"Never overwrite a done or failed row"* (`:19`) — but `cmd_mark` sets the new state with **no check on the current state** (`:153-169`), and `cmd_bulk_transition` moves any `from_state` to any `to_state` (`:179-208`). So the invariant is not enforced in this file. A retry writes to the same `PRED_OUT_DIR` (derived from `prediction_path`), so it overwrites rather than duplicating at the path level. | "Is the done/failed guard enforced somewhere outside `queue_ops.py`, and was `bulk_transition failed→pending` ever used mid-campaign?" |
| **B8** | `propose.py` declares `_BACKBONE_OUTPUT_LEAF` = boltz `model_0.pdb`, of3 `model_0.cif`, protenix `sample_0.cif`, chai `pred.model_idx_0.cif` (`:97-103`), and `prediction_path` = `<root>/<request_id>/<sha12>/<backbone>/seed_<seed>/<leaf>` (`:857-859`). **The observed D1 Boltz output is a `.cif` at `.../boltz_results_<name>/predictions/<name>/<name>_model_16.cif`** — a different leaf and a different grammar. | "Does the dispatched corpus use `propose.py`'s `prediction_path` grammar, or a different one? The D1 path does not match." |
| **B9 (factual half)** | Answered: `runtime_config` present at d9c646af, absent at 04243c45; no launcher git-sha at either. | The willingness half is MUST ASK #14. |
| **C0** | **Four pipelines, not one alignment reformatted.** Sequence shared (C1), MSA route different per backbone (C2), pairing different per backbone (Claim 3). | "Which of the four routes could be replaced by a single pre-built a3m without changing the backbone's behaviour?" |
| **C3a** | Chai's layout is fully specified in code: `<sha256(seq.upper())>.aligned.pqt`, one per protein chain. | The other three layouts and the lossiness question — MUST ASK #3. |
| **C4** | **No depth cap is passed on any command line.** We grepped all eight launchers for `max_seqs`/`max_msa`/`max_msa_clusters`/`max_extra_msa` — zero hits. | "What is each backbone's *default* cap at the pinned version, and does any log an effective post-clustering N?" |
| **C5** | OF3 and Chai verified (Claim 3). | Boltz and Protenix — MUST ASK #3. |
| **C6** | OF3 explicit `false`; Boltz `has_templates_field:false` observed on the traced row. | "Chai and Protenix — was a template path ever active, and will you set all four explicitly in the redo?" |
| **C7** | Representation fully readable per backbone: SMILES inline, `CCD:` prefix routed to `ccd_codes` (OF3), `CCD_<code>` (Protenix), bare three-letter (Chai); peptide → protein chain everywhere. | "How is a ligand *chosen* for a receptor+role, and what happens when none exists?" |
| **C9** | **New finding:** `panel_receptor_sequences.fasta` holds **51 records but only 48 distinct ids.** Three receptors appear twice with different sequences: `ADRB1` (two 477-aa variants, one tagged `note=G389R_polymorphism`), `FSHR` (two 695-aa variants, different sha), `MCHR1` (**353 aa vs 422 aa**). `propose.py::_parse_fasta` keys on the first `\|`-token into a dict, so **last record wins silently** — though `propose.py` does not read this file (it reads GPCRdb; `RECEPTORS_FASTA` is defined at `:77` and never used). | "Which of the two `ADRB1` / `FSHR` / `MCHR1` records was dispatched, and what resolves the collision?" |
| **D2** | Confirmed from the file: Gs 394, Gi1 354, Gq 359, G13 377, Gt 350 — so the blueprint's own correction is right, `334–354` is the C-terminal 21 only for Gi1. `propose.py` already carries a from-the-C-terminus convention in its schema (`partner_perturbation: truncated_Naa`, `:39`). | "Does anything upstream of `_row_input_content` resist expressing partner length from the C terminus? `partner_perturbation` is carried onto rows but not read by the templater." |
| **E1** | Source is fully specified: GPCRdb `services/residues/extended/<entry>/`, HTTPS, no auth, on-disk JSON cache keyed by entry name, payload sha stamped per row. | "Which GPCRdb release, and on what date was the cache built?" — `docs/BW_SOURCE.md`. |
| **E1a** | Class A BW/GPCRdb verified; Class B/F gating readable from `AXIS_APPLICABILITY` and `not_applicable_axes_for`. | **"Is there a CGN convention for the partner chain, or is α5-CT indexed from the C terminus?" — no partner-side numbering exists anywhere in the code we hold.** Load-bearing for the redo; see MUST ASK #7. |
| **E4a/E4b** | The definitions did not drift: every `axes.py` function is byte-identical across campaigns (Claim 4). Geometry, pocket, RMSD and confidence groups are all readable from `axes.py` + `pocket_metrics.py`. | The **partner-engagement** group (`d_ga_alpha5_r350_ca`, `n_interface_contacts_ga_receptor`, `plddt_ga_alpha5`) is in `partner_metrics.py`, **not sent** — MUST ASK #8. The rename question needs `schema.py`. |
| **E4c** | `pocket_notes` vocabulary is enumerable from the code: `lig:<reason>`, `ref=<role|fallback>:<pdb>`, `7tm_n=<n>`, `bw_missing=…`, `ref_role_specific=…`, `ref_role_specific_fallback_to_generic_inactive`, `no_reference_available`, class-deferred notes. Our one row reads `lig:apo_no_ligand;ref=fallback:4X1H;7tm_n=227`. | "Value distribution of `pocket_notes` and `rmsd_note` over a campaign, and does any consumer parse them?" |
| **E6/E6a/E7** | The pocket layer is fully specified: 7TM Kabsch via `_superpose_transform`, `_TM_SEGMENTS = TM1..TM7` from GPCRdb `segment`, `MIN_KABSCH_CA = 20`, `MIN_POCKET_RESIDUES = 6`, computed on `common_tm_positions` and recorded as `7tm_n`. `tm_positions_from_bw_map` says it mirrors `scripts/rescore_rmsd.py`. | "Send `scripts/rescore_rmsd.py` — `rmsd_to_active_ref` / `rmsd_to_inactive_ref` / `rmsd_n_residues_used` live there, not in anything we hold." |
| **E9e** | We now hold `pocket_metrics.py` and already hold the census script, so **we can diff the two pickers ourselves.** `pocket_metrics` picks HETATM residues on the receptor chain, filtered by `_NON_LIGAND_RESNAMES`, then a two-stage `(atom_name, element)` → RDKit-MCS match. | "Were any rows scored before commit `48ddfc1`, and were they migrated?" |
| **E16/E16a** | We have the names only: `warn_A1, warn_A2, warn_A3, warn_A5, warn_A6, warn_multiple` and `run_all_checks` / `summarise` imported from `scorer.pre_check` (`propose.d9c646af.py:9-11, 63-67`). The CLI *"never refuses a proposal"* (`:8`). | "Send `scorer/pre_check.py` and `scorer/assertions.py`." |
| **I1** | `request_id` / `experiment_slug` / `wave_group` / `branch` / `tier` are manifest columns (from the header quoted in the trace). | "Is `request_id` carried into `rows.csv`, or only into the path?" |

---

## MUST ASK — ranked by what each blocks (77 items, the top 15 named)

Ranking is by **how many manuscript sentences or redo decisions sit behind the answer**,
not by cost to them.

### 1. `subsampling/scripts/weekend/build_weekend.py` — which code actually built the dispatched inputs for Blocks A–D?
**Blocks:** B2, C1, D1, D3, H5, and the standing of every claim we draw from `propose.py`.
**Why the code cannot tell us:** `propose.py`'s own header says it was *"Adapted (byte-parity
where feasible) from `subsampling/scripts/weekend/build_weekend.py` — the reference
templater under the source branch that produced the frozen corpus's Boltz/OF3/Protenix
inputs"* (`:339-344`). "Where feasible" is an admitted gap, and `build_weekend.py` is not
in the 30 files and is named nowhere in the log. Every Claim-1 and Claim-2 statement we
make about arm construction currently rests on a file that may be a *reimplementation* of
the one that ran. We verified byte-identity for one D1 apo row; one row, one backbone, one
arm. **Ask for the file, or for a one-line statement that `propose.py` is the templater of
record for all four blocks.**

### 2. `refs/reference_set.csv` **plus its generating rule** (`refs_build` / `gpcr-refs build`)
**Blocks:** the whole of Section F — F1, F1a, F1b, F2, F3, F4, F5, F6, F7 — plus E6b, and
the Methods' `[PI]` placeholder on where the state label comes from.
**Why the code cannot tell us:** `references.py` is a **loader, not a selector.** Its first
line: *"Reference-set loader — A4 / A5 gates. Loads `refs/reference_set.csv` (produced by
`gpcr-refs build` at commit 12)"* (`references.04243c45.py:1-4`). `role`, `resolved_state`,
`stabilising_elements`, `construct`, `construct_offset` and both reference distances are
**read straight out of the CSV** (`from_csv`). Nothing in the code chooses a structure or
assigns a state. One thing we *can* read and should carry: the A4 stabiliser check is
**deliberately disabled** — `DISQUALIFYING_STABILISERS` is *"kept for annotation /
provenance … but no longer used to raise A4"* (`references.*.py:24-40`), so
nanobody/scFv/BRIL-stabilised structures are admitted as active references by design.

### 3. The per-backbone MSA recipe, and **what changes when a partner chain is added**
**Blocks:** C0, C3, C3a, C3b, C4, C5, and every per-backbone comparison in the paper.
**Why the code cannot tell us:** we can now answer this for **two** of four. OF3 flips
`use_paired_msas` False→True (verified). Chai gains one more per-chain `.aligned.pqt`
(verified). For **Boltz and Protenix the command line is identical whether or not a partner
is present** — the change happens inside the backbone and at the MSA server, where we
cannot see. Also unanswerable here: which databases, which release, what search parameters,
what date. **Ask narrowly:** for one cognate cell and its matching apo cell, the on-disk MSA
directory listing plus row counts, per backbone. That is `pairing.a3m` / `non_pairing.a3m`
and the Boltz `msa/` tree — and it settles C3a, C3b, C4 and C5 together.

### 4. The OF3 chunking driver, and the seed it passes per chunk
**Blocks:** B4, B5, Q7, and whether per-seed comparisons across backbones are like-for-like.
**Why the code cannot tell us:** the formula is in `rerun_of3.d9c646af.sh:100-113` and we
implemented it: `random.seed(PRED_SEED)` then `randint(0, 2**32-1)`. It gives `945550830`
for outer `1015473677`; the observed inner seed on that D1 path is `2344327426`. We tested
±8 offsets, the first 500 draws, and string-seeded variants — no match. **So either the
chunk driver passes a different `PRED_SEED` per chunk, or `PRED_N_SEEDS`>1 with a selection
we cannot see, or that row did not go through this launcher.** Precise question: *"For
`tier_d1_lpar1_apo_of3_seed4` chunk_0, what were `PRED_SEED` and `PRED_N_SEEDS`, and which
script set them?"*

### 5. Whether their pipeline accepts an arbitrary receptor + partner set, or has the panel baked into a catalogue
**Blocks:** the entire redo experimental design, `spec/CATALOGUE.md`, and the Group 0/1 gates.
**Why the code cannot tell us:** the evidence points both ways and we cannot resolve it.
*Baked in:* `propose.py` imports `KNOWN_RECEPTORS` and `RECEPTOR_CLASS` from
`scorer.receptors` and `_wt_receptor_fasta` returns `""` for anything not in
`KNOWN_RECEPTORS` (`:301-303`); `gpcr_coupling.csv` is exactly **48 rows**, matching the 48
distinct ids in `panel_receptor_sequences.fasta` one-for-one, with only **four** distinct
`primary_ga_identity` values across all 48 (`alphai1` ×25, `alphas` ×12, `alphaq` ×10,
`alphat` ×1). *Not baked in:* `receptor_sequence_fasta` and `partner.sequence_fasta` are
documented inline overrides, and `_canonicalise_receptor` deliberately returns the
caller's form for unknown slugs *"keep the caller-provided form for A6 to catch"*
(`:252`). **Ask: "Can a spec name a receptor not in `KNOWN_RECEPTORS` and a partner not in
`partners.fasta` and run end to end — and has that ever been done?"** This is the single
question that decides whether the redo can be dispatched through their harness at all.

### 6. One dispatch manifest, whole (I3)
**Blocks:** Claim 1's "never run", Claim 2's "no peptide ever", Q1, Q4, Q6, Q6a, B4, I1, I4, E19.
**Why the code cannot tell us:** every one of those is a fact about *what was dispatched*.
We hold one manifest **header** and one **row**, quoted in prose. A manifest with
`partner_identity`, `partner_perturbation`, `ligand_type`, `input_sha` per row would close
Claim 2 outright and settle four §12 questions at zero compute cost. **Highest
value-per-byte item in the whole list after the scorer tarball.**

### 7. The Gα-side numbering convention (E1a)
**Blocks:** the redo's α5-CT length ladder — i.e. the experiment this campaign exists to run.
**Why the code cannot tell us:** there is **no partner-side numbering anywhere in the code
we hold.** `bw_numbering.py` and `anchors.py` are receptor-only (GPCRdb entry names,
receptor BW labels). `partner_metrics.py`, which would hold it, was not sent. Whether the
pipeline speaks CGN, or indexes α5 from the C terminus, or does neither, is unknown.
**Ask before we design the ladder, not after.**

### 8. `scorer/partner_metrics.py`
**Blocks:** E4a partner-engagement group, E4d, E5's eighth column, D4, and every
"engagement" sentence in the paper.
**Why the code cannot tell us:** `d_ga_alpha5_r350_ca`, `n_interface_contacts_ga_receptor`
and `plddt_ga_alpha5` are computed nowhere in the seven scorer modules we hold. The file is
named in the log (2026-09-11T11:30:47, as a candidate module present at `04243c45`) and was
never sent. It is also the module that would answer whether a retained His6 tag changes the
contact count (D4).

### 9. `sha256` of `anchors.py` and `bw_numbering.py` at `04243c45`
**Blocks:** the caveat on Claim 4.
**Why the code cannot tell us:** they sent one copy of each, labelled "byte-identical at
both". We cannot diff one file against itself. Two hashes in one line converts our
Methods sentence from *"reported identical"* to *"measured identical"*. **Cheapest
high-value ask in the document.**

### 10. `refs/state_thresholds.csv` / the thresholds panel CSV, **and the classifier module** (F3)
**Blocks:** F3, E16, and every predicate-active rate in the paper.
**Why the code cannot tell us:** `axes.py` says *"no threshold branching inside this module
— thresholds live in `refs/state_thresholds.csv` and are consulted only at classification
time in `scorer/references.py`"* (`axes.*.py:4-5`). **We hold `references.py` at both SHAs
and it contains no threshold logic at all** — `grep -i threshold` returns nothing. So
either the docstring is stale or the classifier is in a third module. Either way, **the
code that turns 12.47 and 14.01 into "inactive" using 9.08 and 14.932 is in none of the 30
files.** The row we hold pins `thresholds_panel_csv_sha256 = 242b509f7b7af566…`; the file
itself ships nowhere. Ask for the file, the module, and `scripts/derive_per_class_thresholds.py`.

### 11. `scorer/schema.py` (`StateClaim`, `LigandType`, `ANCHOR_KEYS`, `PROPOSE_MANIFEST_COLUMNS`)
**Blocks:** E18, E19, E4b's rename question, I2's canonical SHA list, and the redo's row contract.
**Why the code cannot tell us:** five of the seven modules we hold import from it. Every
`state_claim` string the reference and pocket routing branches on is defined there.

### 12. `scorer/verified.py` and `scorer/structure.py`
**Blocks:** E2c, E2e, H4(c), and the meaning of `VerifiedModel`.
**Why the code cannot tell us:** `compute_all_axes` **hard-refuses** anything that is not a
`VerifiedModel` (`axes.d9c646af.py:517-522`), and `_anchor_pos` reads
`model.anchor_set` / `model.residues`. **Everything the predicate does with residue
numbering happens inside a class we have never seen.** E2c — "is predicted residue numbering
guaranteed to equal the 1-based index into the supplied sequence?" — is decided in
`verified.py` and nowhere else.

### 13. `scripts/rescore_parallel.py` and the rescore rule (G1, G2, G3)
**Blocks:** G1, G2, G3, G5a, Q9, and whether Block B pocket columns are cross-comparable.
**Why the code cannot tell us:** we hold the *provenance* of one rescore (14,000 rows, 16
workers, 24.9 s, 0 failed) but not the driver. Whether quantities are recomputed from
coordinates or updated in place is the difference between `scorer_git_sha` meaning
something and meaning nothing.

### 14. The willingness items — B9/A4a, C6 (explicit templates), C7a, D6, G4a, Q3
These are redo-contract decisions, not reconstruction. **Batch them into one message** and
do not spend a separate ask on each. B9 + A4a together are one line of code on their side
and retire most of Sections A and B permanently, by their own assessment and ours.

### 15. All of Section J, plus H1/H1a/H1b/H3/H4, A3, A5, G8, I5, I6, J1–J6
Judgement, memory and history. **None of these was ever a code question and none should be
framed as one.** They are also, per the blueprint's own framing, the section most likely to
return value. Keep them, ask them last, and ask them as questions to a colleague rather
than as items on a checklist.

### The remaining MUST ASK items, unranked
A2(i–iii), A3, A5, B5, B6(i), B6(iv), B6a(i–iii), B6b, B7, C3, C3b, C7a, D1, D3, D4,
E1b, E2b–E2f, E4d, E6b, E8a, E8b, E9a–E9d, E9f, E17, E18, F1–F7, G2, G4, G5, G6, G6a, G7,
G9, H1–H6, I3–I6, J1–J6, Q1–Q11, §13.1-3, -8, -13 to -18, §13.2-1, -2, -6 to -11.

---

## The files they have named but not sent — which actually close something

18 `paper_af3`-side artefacts are named in the exchange and not in `received/`. They are
**not of equal value** and we should not ask for them as a block.

### Would close an open question (ask for these)

| file | closes |
|---|---|
| `refs/reference_set.csv` **+ its generating rule** | F1, F1a, F1b, F2, F4, F5, F6, F7, E6b — nine items, and the Methods `[PI]` placeholder. **The single most load-bearing file on the list.** |
| `refs/PREREG.md` | F3 (threshold derivation, §C-5), B4 (§9 seed erratum), A3 (§11a sampling A/B), D3 (§D-3.7). Quoted constantly by both sides, held by neither of us. |
| one dispatch manifest (`tier_d1_full_manifest.csv` or the Block B `manifest.csv`) | Claim 1's "never run", Claim 2's "no peptide", I3, I1, I4, Q1, Q4, Q6, Q6a, B4, E19. **Nothing else on this list closes as many.** |
| `scorer/partner_metrics.py` | E4a (partner group), E4d, E5, D4 — see MUST ASK #8 |
| `msa_depth_report.md` | C4, C5, Q3 — it holds the `pairing_key` evidence and the "raw rows ≠ effective N" statement that C4 turns on |
| `PHASE_1D_EXTENSION.md` | C3a, C5, B9 — the on-disk MSA layouts for Boltz and Protenix, which no code we hold exposes |
| `scorer/fold_integrity.py` | E8's `tm6_helicity_*`, `ramachandran_outlier_frac`, `chain_breaks`, `icl3_modelled_count`; G4a's join-key and stripped-header problem |
| the thresholds panel CSV (`sha 242b509f7b7af566…`) | F3 and every predicate rate — pinned per row, ships nowhere |

### Would merely be collected (do not spend an ask)

| file | why not |
|---|---|
| `pairing.a3m`, `non_pairing.a3m` | Two alignment files from one Protenix cell tell us that Protenix wrote two files — which `PHASE_1D_EXTENSION.md` already reports. **Ask instead for the directory listing and row counts for one cognate/apo pair across all four backbones** (MUST ASK #3). Cheaper for them, and it answers C3a, C4 and C5 together rather than one third of C5. |
| `rows.csv` (D1 full) | We hold the one line the trace is about, and we verified every value in it. A 14,000-row table answers a *different* question (Q2) and should be asked for under Q5/Block C ask 1, on its own merits, not as protocol reconstruction. |
| `rows.pocket.csv`, `rows_tidy.csv` | Both are Block B analysis tables. Their stamp story is already fully documented in the log and does not affect the redo. Wanting them is curiosity about a frozen campaign. |
| `_version_sha.py` | They already told us it is a build artefact generated by `setup.py`'s `build_py` hook and is in neither tree. Asking again re-asks a question they answered. **If we want anything here it is `setup.py`, and only if A2's `no-git` sub-bullet matters to us — which it does not for the redo.** |
| `BLOCK_C_LIGAND_BLOCK_PLAN_2026_09_03.md` | Surfaced only as a `git grep` false positive in their chronology. No open item depends on it. |
| `rescore_manifest.tier_d1_full.csv` | A worklist. `rescore_parallel.provenance.json`, which we hold, already carries everything about that rescore we need. |

### Named by neither side but required by code we hold (add to the ask)

These are hard imports or hard invocations in the 30 files, and their absence is invisible
unless someone reads the code:

`qsub/status_writer.py` (invoked by all four launchers — it writes the status JSON that is
our only runtime evidence) · `scorer/verified.py` · `scorer/structure.py` ·
`scorer/schema.py` · `scorer/receptors.py` · `scorer/rerun.py` · `scorer/cache.py` ·
`scorer/pre_check.py` · `scorer/assertions.py` · `scorer/post_run_receipts.py` ·
`scripts/rescore_rmsd.py` · `scripts/rescore_parallel.py` ·
`subsampling/scripts/weekend/build_weekend.py` · `scripts/subsample_msa_chai.py`
(named as a TODO in `subsample_msa.py:8-9`) · `qsub/verify_drd2_msa_cache.sh` ·
whatever builds the Chai `.aligned.pqt` cache — **never named by anyone, and it is the
single MSA artefact in the pipeline that is actually pinned.**

**Recommendation: ask for `scorer/` as a tarball at each SHA (§1 ①, as originally written)
rather than 12 more individual files.** The incremental-file protocol has served us well
and should stop here; the remaining modules are small and mutually dependent.

---

# Checked and NOT a finding

Every item below looked like a discrepancy on first read. Each was our error, or a
misreading, or a comparison between two different objects. Recorded so nobody re-raises
them.

1. **`ref=fallback:4X1H` in the D1 row's `pocket_notes` is not a failed lookup.** It reads
   like one. `pocket_metrics.d9c646af.py:1247` is
   `notes.append(f"ref={role or 'fallback'}:{ref.pdb_id}")`, and for an `apo` state_claim
   `_role_for_state_claim` returns `(None, "")`, so the literal string `fallback` is
   printed for *role*, not for a failure. The reference used is then
   `ref = ref_active if ref_active is not None else ref_inactive` (`:1090`) — i.e.
   **4X1H is OPSD's active reference and was correctly selected.** No finding.

2. **`pocket_ref_role_inactive = "generic_inactive_fallback"` is the designed value for an
   apo row, not a defect.** `:1231-1233`: when the primary reference is active and the row
   has no `ligand_role`, the inactive companion is the generic one and is tagged as such.
   Working as written.

3. **`rows_csv_line.txt` has 102 fields; their message says "All 92 columns present."** We
   parsed it with `csv.reader` (so the bracketed pLDDT list at field 44 is correctly one
   quoted field) and counted 102, with field 101 empty. We do **not** call this a finding:
   we hold no header, and "92 columns" may refer to `rows.csv`'s schema while the line
   carries added columns, or to a different table. **Worth one neutral question with the
   count attached** — not a contradiction. Similarly, their `rows.pocket.csv` "90 columns"
   is unverifiable here.

4. **Field 50 of the D1 row reads `borderline`, while the trace says "Non-borderline in
   both axes."** These describe different objects. Fields 45–49 are the reference-delta
   family (`receptor_d_active_ref` 14.72, `receptor_d_inactive_ref` 8.73, `receptor_midpoint`
   11.72, `delta_to_active` −5.12, `delta_to_inactive` 0.87) and field 50 is a call on
   *that* axis. Their "non-borderline" statement was about the two **predicate** axes
   (12.47 vs 9.08; 14.01 vs 14.932). Comparing a value against a statistic of a different
   kind is exactly the failure mode this project has hit three times in one day. **Not a
   finding** — though the second predicate axis sits 0.92 Å from its threshold, and if we
   ever quote that row we should say so.

5. **`axes.py` grew 27 lines, they reported 47.** Different commit pairs. Ours is
   `04243c45 → d9c646af`; theirs (2026-09-11T13:19:12) was `04243c45 → ea9efe5`. Both can
   be true. Not a discrepancy.

6. **`received/README.md` says `partners.fasta` has "29 entries"; the file has 28.** This is
   **our** error, not theirs. `grep -c "^>"` returns 28, with no duplicate first-tokens.
   The figure 29 came from `BLUEPRINT_REQUEST.md:1111` (our own reading of their
   `PHASE_1_CONSTRUCT_IDENTITY.md`), and we copied it forward into the README when the file
   landed. **`received/README.md` should be corrected to 28** — and note the arithmetic in
   §12 Q4 ("the 25 unconsumed entries") rests on 29. What we can state from the file: 28
   records; 4 distinct identities appear as `primary_ga_identity` in `gpcr_coupling.csv`
   (`alphas`, `alphai1`, `alphaq`, `alphat`); the other 24 do not appear there.

7. **`propose.py`'s `_BACKBONE_OUTPUT_LEAF` says Boltz writes `model_0.pdb`, but the D1
   output is a `.cif`.** Real mismatch, but it is a mismatch between `propose.py` and an
   observed path, not an error by anyone. Recorded as a question (B8, above), not a finding
   — it may simply mean the D-tier dispatch did not use `propose.py`'s `prediction_path`
   grammar, which is itself the thing MUST ASK #1 is about.

8. **`queue_ops.py`'s docstring invariant is not enforced in `queue_ops.py`.** We checked
   `cmd_mark` and `cmd_bulk_transition` line by line before saying so, and we are **not**
   claiming the invariant is violated in practice — only that the enforcement, if it
   exists, is somewhere else. Framed as a question (B6), not a defect.

9. **We could not reproduce the OF3 inner seed.** Before treating this as a gap in their
   pipeline we implemented the launcher's formula exactly, then tried seventeen offsets,
   500 draws and string-seeded variants. The failure to match is a statement about **what
   we hold** (no chunk driver), not about their code. Phrased that way in MUST ASK #4.

10. **`RECEPTORS_FASTA` is defined in `propose.py` and never used.** A dead constant
    (`:77`). Not a defect, and *not* evidence about which receptor file is canonical —
    `_wt_receptor_fasta` explicitly and deliberately reads GPCRdb instead (`:279-292`).
    Mentioned under C9 only for completeness.

11. **`arrestin_FL` is 15 residues.** "FL" reads as full-length; 15 is not a full arrestin.
    We have **not** called this a mislabel — we have no idea what the record is meant to be,
    and D6 already establishes that this file carries two known mislabels. If we ask about
    it, ask *what it is*, not *why it is wrong*.

---

# What we should do before the next message

1. **Correct `received/README.md`:** 28 entries, not 29.
2. **Tighten the five claims in any draft that already uses them**, per the summary table
   above — particularly Claim 2, which as written asserts something the code and catalogue
   both permit.
3. **Do not re-ask the 34 answerable items.** Several (B1, C1, C2, C8, D5, E4, E5, E8c,
   E8d, E12, E14, E15) are things we asked for and have now been answered in full by the
   code; re-asking them would be the exact failure the blueprint's §0.3 warns about.
4. **Send one message, not many.** The ranked top six, plus the willingness batch (#14),
   plus Section J. Everything else waits for the scorer tarball, which will answer a
   further ~15 items on arrival.
