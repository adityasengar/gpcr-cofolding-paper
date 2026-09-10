# C-B-1 — Templates-off evidence class is (b) + (c), not (a)

## Caveat

Block B's templates-off claim rests on **class (b)** launcher static
analysis + **class (c)** upstream source defaults. Evidence class (a) —
a per-row runtime echo either in `rows.csv` or as a `runtime_config`
block inside each `_<backbone>_status.json` — is NOT present on Block B
outputs.

The audit #9 post-dispatch coverage §1 line ("every launcher's
`_<backbone>_status.json` should carry `runtime_config.received_config.use_templates`")
describes the design intent, but Block B's status.json files are all in
the minimal 5-6-key form: `{exit_code, n_produced, ok, produced_files,
seed}` (Boltz) or with `backbone` added (Chai/OF3/Protenix). The design
either landed later, was reverted, or was never wired to disk on the
compute node under Block B's launcher revisions.

## Why it matters

PREREG §11b accepts class (b) + (c) as sufficient for the templates-off
lock. The full prospectivity framing depends on templates being off. A
20-file HPC stratified sample (5 files per backbone across receptors and
arms) carries no template field with any value — no populated path, no
non-zero count, no template-search invocation. Regression detector
(audit #9) is negative on this sample. But strictly weaker than a
per-row runtime echo.

## Evidence

- `docs/BLOCK_B_DOSSIER_PHASE_0_PROVENANCE.md §0d` — class (b)+(c) table per backbone.
- `docs/BLOCK_B_DOSSIER_PHASE_0_TEMPLATES_SWEEP.md` §4a–§4d — 20-file stratified sample.
- No `--use-templates true` invocation in any of the four launchers.
  OF3 carries explicit `--use-templates false` on both paths (audit #9
  countermeasure §1).
- Chai `use_templates_server = False` at `chai_lab/chai1.py:334, 492`;
  Protenix `use_templates = False` model-config default; Boltz input YAML
  never populates the `templates:` field.

## Affects

- SC-B-7 (templates were not used on any backbone).
- The prospectivity framing at manuscript level (upstream of Block B and
  onward to Block C/D).

## Manuscript sentence

> Templates were off across all four backbones on Block B. Evidence
> comprises launcher static analysis (`qsub/rerun_of3.sh` carries the
> explicit `--use-templates false` flag; no template flag in the other
> three launchers) and upstream source defaults (Chai
> `use_templates_server=False`; Protenix `use_templates=False`; Boltz
> input YAML never populates the `templates:` field). Per-row runtime
> echo is not present on Block B outputs; a 20-file stratified sample
> of `_<backbone>_status.json` carries no `runtime_config` block. The
> templates-off claim rests on the evidence class PREREG §11b accepts,
> not on a runtime-verified per-row echo.

## Related

- MANUSCRIPT_FLAGS.md Flag B-5.
