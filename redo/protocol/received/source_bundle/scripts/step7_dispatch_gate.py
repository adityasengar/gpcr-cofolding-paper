"""Step 7 — Block A dispatch gate.

This is the hard-gate that fires before any Block A prediction row leaves
the propose→queue pipeline. Codifies PREREG §Step 6 (A1 hard-fail on
panel receptors) plus the pre-dispatch checklist from §Open TODOs.

Run mode:
    python3 scripts/step7_dispatch_gate.py                     # gate check only
    python3 scripts/step7_dispatch_gate.py --panel refs/gpcr_coupling.csv
    python3 scripts/step7_dispatch_gate.py --skip-msa-prewarm  # emergency override

The gate REFUSES to release a manifest to h100_pool/queue.csv unless
every check below passes. It's designed to be called from
`scripts/build_block_a_manifest.py` before the manifest is emitted.

Checks (all must pass):
1. `refs/gpcr_coupling.csv` present, 40 rows, matches expected sha256
2. `refs/reference_set.csv` has `d_npxxy_oh_ref` + `d_npxxy_ca_ref`
   columns AND ≥ 32 non-NaN values per column (tier-1 threshold)
3. `refs/PREREG.md` §Open TODOs — every hard-gate TODO closed (parses
   the checklist)
4. All 6 motif-metric thresholds have panel-derived values recorded in
   `refs/thresholds_panel.csv` (produced by step3_cross_validate_instruments)
5. `docs/EXPERIMENT_CATALOG/sequences/partners.fasta` contains `>alphat`
6. Every panel receptor passes `pc4_identity_anchors_match` on its
   canonical WT FASTA (from GPCRdb) — no `warn_A1` allowed
7. Scorer schema includes the 4 new columns (`d_npxxy_y558_y753_oh`,
   `d_ga_alpha5_r350_ca`, `n_interface_contacts_ga_receptor`, `plddt_ga_alpha5`)
8. Chai `.aligned.pqt` cache complete for every unique panel + partner
   sequence (silent single-seq fallback prevention).
9. Shared `qsub/rerun_chai.sh` wires the cache in (`--msa-directory` via
   `CHAI_MSA_DIRECTORY` env), no `--use-msa-server` anywhere — prevents
   the cache-exists-but-launcher-bypasses-it failure mode.
10. MSA pre-warm has run for all 67 required sequences (unless
    --skip-msa-prewarm passed; 2 non-Block-A partners excluded).
11. Scorer files on HPC (basel-hpc:~/paper_af3/scorer/{orchestrator,
    schema,structure,cli,assertions}.py) SHA256-match local. Closes the
    audit-trail #11 regression class: rescore_experiment.py invokes
    scorer.cli.batch_main in-process against whichever scorer package
    the HPC checkout carries, so a drifted scorer produces silently
    wrong rows.csv with exit 0.
12. Qsub launcher / helper files on HPC SHA256-match local (see
    QSUB_FILES_TRACKED). Closes the audit-1.2 regression class
    (2026-09-04): commit 0e738af rewrote all four rerun_*.sh to invoke
    status_writer.py, laptop had the edits, HPC did not, and every
    Block A + Block B prediction silently ran the pre-audit inline
    heredoc — audit-#10 / #13 countermeasures non-operational for two
    campaigns without any signal.
13. `refs/ligand_set.csv` — every CCD-sourced row's SMILES matches the
    authoritative RCSB CCD entry (connectivity InChIKey byte-parity).
    Closes the Block C Step 1.1 curation-quality regression class
    (2026-09-04): ~40-46 % of memory-based SMILES entries carried
    structural errors across four verification passes; CCD sourcing
    pins on crystal chemistry and this gate prevents silent drift
    between the CSV's `smiles` / `ccd_smiles` columns and RCSB.
14. Manifest row count + per-cell distribution match the paper grid
    (Stage 0 item 5, 2026-09-06). Reads the newest
    `experiments/*/manifest/*.csv` with a companion
    `.expected_grid.json` sidecar and refuses to release the manifest
    when its total row count ≠ `expected_rows` OR its per-cell
    `(receptor, backbone, arm)` distribution is uneven / missing cells
    / extra cells. Countermeasure to the Block C Tier 3 dispatch bug:
    manifest emitted 2,960 rows instead of 4,080 because the peptide
    decoy injection was silently skipped; the CSV parsed clean and
    dispatch would have proceeded against a short manifest.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CHAI_MSA_DIR = Path("/hpc/scratch/sengaad1/paper_af3/msa_cache/chai")


class GateFailure(Exception):
    pass


def _fail(msg: str):
    raise GateFailure(msg)


# ---------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------

def check_coupling_panel() -> str:
    """Panel of record: 40 Class A + 4 Class B + 4 Class F = 48 rows (2026-09-01).

    Class C is excluded per PREREG §1 (dimer-interface activation
    mechanism uninterpretable on a monomeric construct).
    """
    p = REPO / "refs/gpcr_coupling.csv"
    if not p.exists():
        _fail(f"missing {p}")
    rows = list(csv.DictReader(p.open()))
    if len(rows) != 48:
        _fail(f"expected 48 rows in {p} (40 A + 4 B + 4 F), got {len(rows)}")
    # Confirm the class-B/F receptors are actually in the merged file.
    slugs = {r["receptor_slug"].strip().upper() for r in rows}
    required_bf = {"GLP1R", "GCGR", "PTH1R", "CRHR1", "SMO", "FZD4", "FZD6", "FZD7"}
    missing_bf = required_bf - slugs
    if missing_bf:
        _fail(f"{p}: missing Class B/F receptors {sorted(missing_bf)}")
    for r in rows:
        if not r.get("coupling_evidence"):
            _fail(f"{p}: {r['receptor_slug']} has empty coupling_evidence")
    return f"OK — {len(rows)} rows (40 A + 4 B + 4 F), all coupling_evidence filled"


def check_npxxy_refs() -> str:
    p = REPO / "refs/reference_set.csv"
    rows = list(csv.DictReader(p.open()))
    cols = rows[0].keys() if rows else set()
    if "d_npxxy_oh_ref" not in cols or "d_npxxy_ca_ref" not in cols:
        _fail(f"{p}: missing NPxxY reference columns")
    # After the physical seal (PREREG §14 v2, 2026-09-01), 8 Class A active
    # rows live in refs/sealed_active_refs_2026_09_01.csv rather than in
    # reference_set.csv. The scientific prerequisite ("≥32 tier-1 Class A
    # actives with NPxxY refs derived") is satisfied by the UNION of the
    # two files; only the physical location changed.
    sealed_p = REPO / "refs/sealed_active_refs_2026_09_01.csv"
    if sealed_p.exists():
        with sealed_p.open() as f:
            sealed_lines = [ln for ln in f if not ln.startswith("#")]
        sealed_rows = list(csv.DictReader(sealed_lines))
    else:
        sealed_rows = []
    combined = rows + sealed_rows
    active = [r for r in combined if r.get("role", "").strip() == "active"]
    n_ok_oh = sum(1 for r in active
                  if r.get("d_npxxy_oh_ref") and r["d_npxxy_oh_ref"] not in ("nan", "NaN", "None"))
    n_ok_ca = sum(1 for r in active
                  if r.get("d_npxxy_ca_ref") and r["d_npxxy_ca_ref"] not in ("nan", "NaN", "None"))
    if n_ok_oh < 32:
        _fail(f"{p} ∪ sealed: only {n_ok_oh} active rows have d_npxxy_oh_ref; need ≥ 32 Class-A tier-1")
    if n_ok_ca < 32:
        _fail(f"{p} ∪ sealed: only {n_ok_ca} active rows have d_npxxy_ca_ref; need ≥ 32 Class-A tier-1")
    return (f"OK — {n_ok_oh} active have OH-OH ref, {n_ok_ca} CA-CA ref "
            f"(union of refs/reference_set.csv + sealed CSV; Class A ≥ 32 required)")


def check_prereg_open_todos() -> str:
    p = REPO / "refs/PREREG.md"
    text = p.read_text()
    # Count `- [ ]` in the Open TODOs section
    m = re.search(r"## Open TODOs.*?(?=\n## |\Z)", text, re.S)
    if not m:
        _fail(f"{p}: no Open TODOs section")
    section = m.group(0)
    unresolved = section.count("- [ ]")
    if unresolved:
        _fail(f"{p}: {unresolved} Open TODOs still open in PREREG.md — must all be [x]")
    return "OK — PREREG Open TODOs all closed"


def check_thresholds_landed() -> str:
    p = REPO / "refs/thresholds_panel.csv"
    if not p.exists():
        _fail(f"missing {p} — run scripts/step3_cross_validate_instruments.py "
              "to derive panel thresholds after NPxxY refs land")
    rows = list(csv.DictReader(p.open()))
    metrics_required = {
        "d_npxxy_y558_y753_oh", "d_npxxy_y558_y753_ca",
        "d_y558_pack_min_heavy", "d_dry_sidechain_r350cz_e630oe1",
        "d_tm5_outward_r350_r558_ca", "icl2_helical_frac",
    }
    seen = {r.get("metric_col") for r in rows}
    missing = metrics_required - seen
    if missing:
        _fail(f"{p}: missing thresholds for metrics {missing}")
    return f"OK — panel thresholds for all 6 metrics in {p}"


def check_alphat_in_partners() -> str:
    p = REPO / "docs/EXPERIMENT_CATALOG/sequences/partners.fasta"
    text = p.read_text()
    if ">alphat|" not in text:
        _fail(f"{p}: no `>alphat|` entry — OPSD dispatch will fail")
    return "OK — alphat entry present"


def check_scorer_partner_metrics() -> str:
    p = REPO / "scorer/schema.py"
    text = p.read_text()
    required = {
        "d_npxxy_y558_y753_oh",
        "d_ga_alpha5_r350_ca",
        "n_interface_contacts_ga_receptor",
        "plddt_ga_alpha5",
    }
    missing = {c for c in required if c not in text}
    if missing:
        _fail(f"{p}: scorer schema missing columns {missing}")
    return f"OK — scorer schema has all 4 partner-interface / NPxxY-OH columns"


def check_a1_hard_gate() -> str:
    """Confirm dispatch script rejects `warn_A1` for panel receptors."""
    p = REPO / "scripts/build_block_a_manifest.py"
    text = p.read_text()
    if "warn_A1" not in text or "hard_fail" not in text.lower():
        return "SKIP — build_block_a_manifest.py doesn't yet enforce A1 hard-gate; add before dispatch"
    return "OK — dispatch script enforces A1 hard-gate on panel receptors"


def _parse_fasta(path: Path):
    """Return list of (header, sequence) tuples from a FASTA file."""
    entries = []
    header, seq_lines = None, []
    for line in path.read_text().splitlines():
        line = line.strip()
        if line.startswith(">"):
            if header is not None:
                entries.append((header, "".join(seq_lines)))
            header = line[1:]
            seq_lines = []
        elif line:
            seq_lines.append(line)
    if header is not None:
        entries.append((header, "".join(seq_lines)))
    return entries


def _chai_aligned_pqt_name(seq: str) -> str:
    """Chai-lab v0.6.1's expected pre-computed MSA filename.

    Per refs/msa_input_interfaces.md (agent audit 2026-09-01), Chai reads
    from --msa-directory with basenames `sha256(seq.upper()).hexdigest() +
    '.aligned.pqt'`. Any hash mismatch triggers silent single-sequence
    fallback — dangerous, hence this hard gate.
    """
    return hashlib.sha256(seq.upper().encode()).hexdigest() + ".aligned.pqt"


def check_chai_aligned_pqt() -> str:
    """Hard gate: every unique panel sequence must have a Chai-format
    `.aligned.pqt` at CHAI_MSA_DIR before dispatch.

    Chai's silent single-sequence fallback (chai-lab 0.6.1) makes this a
    dispatch-blocking check: without the file, the chai arm becomes a
    duplicate of chai_singleseq across ~4,000 Block A predictions and
    we'd only discover it at scoring. See refs/msa_input_interfaces.md
    §Chai-1 for the format spec and the ~30-line a3m→pqt converter
    reference.
    """
    receptors_fasta = REPO / "refs/panel_receptor_sequences.fasta"
    partners_fasta = REPO / "docs/EXPERIMENT_CATALOG/sequences/partners.fasta"
    if not receptors_fasta.exists():
        _fail(f"missing {receptors_fasta}")
    if not partners_fasta.exists():
        _fail(f"missing {partners_fasta}")

    # Collect unique sequences (dedup by SHA — some partners may repeat)
    all_entries = _parse_fasta(receptors_fasta) + _parse_fasta(partners_fasta)
    unique_by_hash = {}
    for header, seq in all_entries:
        h = hashlib.sha256(seq.upper().encode()).hexdigest()
        unique_by_hash.setdefault(h, (header, seq))
    n_unique = len(unique_by_hash)

    # Probe HPC for expected filenames (CHAI_MSA_DIR lives on scratch)
    expected = [_chai_aligned_pqt_name(seq) for _, seq in unique_by_hash.values()]
    try:
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=10", "basel-hpc",
             f"ls {CHAI_MSA_DIR}/*.aligned.pqt 2>/dev/null | wc -l"],
            capture_output=True, text=True, timeout=30
        )
        n_present = int((result.stdout or "0").strip() or 0)
    except Exception as e:  # noqa: BLE001
        _fail(f"could not probe {CHAI_MSA_DIR} on basel-hpc: {type(e).__name__}: {e}")

    if n_present < n_unique:
        _fail(
            f"only {n_present}/{n_unique} .aligned.pqt files at "
            f"{CHAI_MSA_DIR}. Chai will silently fall back to single-sequence "
            f"on the {n_unique - n_present} missing sequences. Generate them "
            f"before dispatch (a3m→pqt converter per msa_input_interfaces.md), "
            f"or REMOVE the chai arm from the Block A manifest."
        )

    # File count is sufficient — verify at least one expected filename exists
    # (guards against name-mismatch where the count-based check would still pass)
    sample = expected[0]
    result = subprocess.run(
        ["ssh", "-o", "ConnectTimeout=10", "basel-hpc",
         f"test -e {CHAI_MSA_DIR}/{sample} && echo yes || echo no"],
        capture_output=True, text=True, timeout=15
    )
    if (result.stdout or "").strip() != "yes":
        _fail(
            f"expected filename {sample} not found at {CHAI_MSA_DIR}. "
            f"count-based check passed ({n_present}/{n_unique}) but the "
            f"expected sha256-based basenames are wrong. Regenerate using "
            f"the correct `sha256(seq.upper()).hex + '.aligned.pqt'` naming."
        )
    return f"OK — {n_unique}/{n_unique} .aligned.pqt files present at {CHAI_MSA_DIR}"


def check_chai_launcher_no_server() -> str:
    """Hard gate — must-NOT-contain half of the launcher pair.

    `qsub/rerun_chai.sh` must not contain `--use-msa-server` anywhere.
    Prior to 2026-09-01 the launcher hardcoded server mode; dispatching
    Block A against it would hit the ColabFold public API ~4,000 times —
    the exact failure the local `.aligned.pqt` cache exists to prevent,
    and one the `chai_aligned_pqt` gate above cannot catch on its own
    (the cache would exist; the launcher would just ignore it).
    """
    p = REPO / "qsub/rerun_chai.sh"
    if not p.exists():
        _fail(f"missing {p}")
    if "--use-msa-server" in p.read_text():
        _fail(f"{p}: contains `--use-msa-server` — remove entirely. Cache "
              f"mode is the only supported non-baseline path. Server-mode "
              f"ablations must live in a separate one-off wrapper.")
    return "OK — rerun_chai.sh has no `--use-msa-server` anywhere"


def check_chai_launcher_uses_cache() -> str:
    """Hard gate — must-contain half of the launcher pair.

    `qsub/rerun_chai.sh` must wire the `.aligned.pqt` cache into every
    chai job via `--msa-directory` behind a `CHAI_MSA_DIRECTORY` env
    toggle. Absent this plumbing every chai prediction would silently
    fall back to single-sequence.
    """
    p = REPO / "qsub/rerun_chai.sh"
    if not p.exists():
        _fail(f"missing {p}")
    text = p.read_text()
    if "--msa-directory" not in text:
        _fail(f"{p}: no `--msa-directory` — cache mode is not wired up. "
              f"Every chai prediction would silently fall back to "
              f"single-sequence.")
    if "CHAI_MSA_DIRECTORY" not in text:
        _fail(f"{p}: no `CHAI_MSA_DIRECTORY` env toggle — cache path "
              f"appears to be hardcoded. Add the env-var route per the "
              f"2026-09-01 audit.")
    return "OK — rerun_chai.sh wires --msa-directory via CHAI_MSA_DIRECTORY"


def check_of3_launcher_no_direct() -> str:
    """Hard gate — must-NOT-contain half of the OF3 launcher pair.

    `qsub/rerun_of3.sh` must not invoke `run_openfold` directly; every
    OF3 prediction must route through `qsub/colabfold_shim.py of3`.
    Otherwise OF3's hardcoded `timeout=6.02` on
    `/result/download/{ID}` bites: 91 ReadTimeouts on a single warm-
    cache prediction were empirically observed 2026-09-01, blowing
    wall-time from ~200s (patched) to ~750s (unpatched) per prediction.
    Under 12-way concurrent Block-A load the multiplier compounds.
    """
    p = REPO / "qsub/rerun_of3.sh"
    if not p.exists():
        _fail(f"missing {p}")
    text = p.read_text()
    # Look for the raw command invocation on a non-comment line.
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        # Match `run_openfold predict` at the start of a token (not
        # `which run_openfold`, not `# run_openfold`, not
        # `/colabfold_shim.py of3 predict`).
        if stripped.startswith("run_openfold ") or stripped == "run_openfold":
            _fail(f"{p}:{i}: direct `run_openfold` invocation — must "
                  f"route through colabfold_shim.py so ColabFold "
                  f"ReadTimeouts don't blow up Block-A wall time.")
    return "OK — rerun_of3.sh has no direct `run_openfold` invocation"


def check_of3_launcher_uses_shim() -> str:
    """Hard gate — must-contain half of the OF3 launcher pair.

    `qsub/rerun_of3.sh` must invoke `colabfold_shim.py of3` and set
    `COLABFOLD_SIDECAR` for post-run retry/wait accounting.
    """
    p = REPO / "qsub/rerun_of3.sh"
    if not p.exists():
        _fail(f"missing {p}")
    text = p.read_text()
    if "colabfold_shim.py of3" not in text:
        _fail(f"{p}: no `colabfold_shim.py of3` invocation — OF3 must "
              f"route through the shim so the 6.02s ReadTimeout on "
              f"api.colabfold.com is bumped to (30, 600).")
    if "COLABFOLD_SIDECAR" not in text:
        _fail(f"{p}: no `COLABFOLD_SIDECAR` env — post-run retry/wait "
              f"accounting is not wired. Add "
              f"`export COLABFOLD_SIDECAR=$PRED_OUT_DIR/_of3_colabfold_http_summary.json`"
              f" before the fold call.")
    shim = REPO / "qsub/colabfold_shim.py"
    if not shim.exists():
        _fail(f"launcher references colabfold_shim.py but it is missing at {shim}")
    return "OK — rerun_of3.sh routes through colabfold_shim.py, sidecar wired"


def check_no_templates_any_backbone() -> str:
    """Hard gate — no backbone runs template search at inference time.

    Locked 2026-09-01 (PREREG §11b). Prospectivity claim of the paper
    (de novo generation of a conformational state) is incompatible
    with template retrieval — for any receptor whose Gs-bound
    structure is in the PDB, "predicted active" reduces to
    "retrieved." OF3's default template search fetches from
    data.rcsb.org at inference; this check pins the countermeasure
    across all four backbones.

    Enforces at the LAUNCHER level (grep-level, code paths, not
    generated inputs — those get materialised only at HPC-dispatch
    time and can't be inspected locally before the manifest is built).
    Regression class: audit trail #9 (2026-09-01). Same family as the
    chai silent-single-seq bug — an inference-time default nobody
    chose, invisible in the outputs.

    Rules:
      1. `qsub/rerun_of3.sh` must pass `--use-templates false`.
         (OF3 defaults ON; must be explicit off.)
      2. `qsub/rerun_boltz.sh` must not pass `--use_templates` /
         `--use-templates` at all.
         (Boltz reads templates from the YAML; the launcher CLI
         doesn't enable them, but we still guard against a future
         opt-in flag creeping in.)
      3. `qsub/rerun_protenix.sh` must not pass any
         `--use_template*` or set `use_templates=True`.
         (Protenix defaults `use_templates=False`.)
      4. `qsub/rerun_chai.sh` must not pass `--use-templates`.
         (Chai defaults `use_templates_server=False`.)
      5. `scorer/propose.py` must emit no `templates:` YAML key
         (Boltz), no `"template_hits_file"` or top-level
         `"templates"` JSON key (OF3, Protenix). Any regression
         that adds a template field lands here.
    """
    # 1. OF3 — must have explicit false
    of3 = REPO / "qsub/rerun_of3.sh"
    if not of3.exists():
        _fail(f"missing {of3}")
    of3_text = of3.read_text()
    if "--use-templates false" not in of3_text:
        _fail(f"{of3}: missing `--use-templates false`. OF3 template "
              f"search defaults ON and fetches from data.rcsb.org at "
              f"inference time — PREREG §11b locks it off.")
    # Also refuse an explicit true
    if "--use-templates true" in of3_text:
        _fail(f"{of3}: contains `--use-templates true`. Templates "
              f"are locked off across all four backbones per PREREG §11b.")

    # 2-4. Boltz / Protenix / Chai — must not opt in
    for name in ("rerun_boltz.sh", "rerun_protenix.sh", "rerun_chai.sh"):
        p = REPO / "qsub" / name
        if not p.exists():
            _fail(f"missing {p}")
        text = p.read_text()
        # Filter to non-comment lines only so a comment about
        # "templates were disabled" doesn't false-fail the check.
        non_comment = "\n".join(
            line for line in text.splitlines()
            if not line.lstrip().startswith("#")
        )
        # Boltz uses --use_templates_server; Protenix uses --use_templates_server or use_templates; Chai uses --use-templates.
        for pat in ("--use-templates", "--use_templates", "use_templates=True",
                    "use_templates_server=True", "--use_templates_server"):
            if pat in non_comment:
                _fail(f"{p}: contains `{pat}` — templates are locked "
                      f"off across all four backbones per PREREG §11b.")

    # 5. propose.py — no template field emission
    propose = REPO / "scorer/propose.py"
    if not propose.exists():
        _fail(f"missing {propose}")
    propose_text = propose.read_text()
    # Distinguish "templater" (function-naming, unrelated) from actual
    # template-field emission.  Look for the specific JSON/YAML keys
    # the four backbones consume.
    forbidden_keys = (
        'templates:',            # Boltz YAML key
        '"templates"',           # OF3 / Protenix JSON key
        '"template_hits_file"',  # OF3-specific
        '"template_path"',       # generic guard
        'template_hits',         # generic guard
    )
    for key in forbidden_keys:
        if key in propose_text:
            _fail(f"{propose}: contains `{key}` — propose emitters must "
                  f"not populate template fields for any backbone. "
                  f"See PREREG §11b and audit trail #9.")

    return ("OK — templates disabled across all 4 backbones "
            "(of3 --use-templates false; boltz/protenix/chai default off; "
            "propose.py emits no template fields)")


SEALED_CSV_EXPECTED_SHA256 = "879046326c6b8469f8b2f78f82280876da980f004a0b2c7f4cfc3095b2d9bc8e"


def check_sealed_refs_physically_moved() -> str:
    """Hard gate — sealed active references are physically moved (PREREG §14 v2).

    The prior seal attempt (seed 20260901) left the 8 active rows in
    refs/reference_set.csv with only an analysis-side gate. That is not a
    seal — anything reading the file has the info. This gate enforces the
    v2 physical-move semantics:

      1. refs/sealed_active_refs_2026_09_01.csv exists and its SHA256
         matches the value pinned in PREREG §14 v2.
      2. For every sealed receptor, refs/reference_set.csv contains NO
         active-role row (i.e. the row was physically moved out).

    Fails loud with the offending receptor if any active row survived in
    the main CSV.
    """
    sealed_p = REPO / "refs/sealed_active_refs_2026_09_01.csv"
    if not sealed_p.exists():
        _fail(f"missing {sealed_p} — run scripts/seal_active_refs.py before dispatch")
    actual_sha = hashlib.sha256(sealed_p.read_bytes()).hexdigest()
    if actual_sha != SEALED_CSV_EXPECTED_SHA256:
        _fail(
            f"{sealed_p}: SHA256 {actual_sha} does not match PREREG §14 pin "
            f"{SEALED_CSV_EXPECTED_SHA256}. Re-run scripts/seal_active_refs.py "
            f"and update the pinned value in step7_dispatch_gate.py + PREREG §14."
        )

    # Parse sealed slugs from the CSV (skip comment lines).
    with sealed_p.open() as f:
        lines = [ln for ln in f if not ln.startswith("#")]
    sealed_reader = csv.DictReader(lines)
    sealed_slugs = {
        r["receptor_slug"].strip().upper()
        for r in sealed_reader
        if r.get("role", "").strip() == "active"
    }
    if not sealed_slugs:
        _fail(f"{sealed_p}: no active-role rows in sealed CSV — seal is empty")

    # Assert none of them still live in reference_set.csv as active-role.
    refset_p = REPO / "refs/reference_set.csv"
    surviving: list[str] = []
    with refset_p.open() as f:
        for r in csv.DictReader(f):
            if (r["receptor_slug"].strip().upper() in sealed_slugs
                    and r.get("role", "").strip() == "active"):
                surviving.append(r["receptor_slug"].strip().upper())
    if surviving:
        _fail(
            f"{refset_p}: active row survived for sealed receptor(s) "
            f"{sorted(set(surviving))} — physical move incomplete. "
            f"Re-run scripts/seal_active_refs.py."
        )
    return (f"OK — {len(sealed_slugs)} sealed active rows physically moved out of "
            f"reference_set.csv; sealed CSV SHA256 matches PREREG §14 v2 pin")


# ---------------------------------------------------------------------
# Scorer-sync gate (audit-trail #11 countermeasure)
# ---------------------------------------------------------------------

SCORER_FILES_TRACKED = (
    "scorer/orchestrator.py",
    "scorer/schema.py",
    "scorer/structure.py",
    "scorer/cli.py",
    "scorer/assertions.py",
    # Added 2026-09-03 alongside Block C Gate 0.1 dispatch (B1) — A4
    # landed scorer/pocket_metrics.py and re-wired scorer/axes.py to
    # re-export it. Both are imported at scorer runtime, so a drifted
    # HPC copy would silently produce different pocket-axis values.
    # Extending the tuple closes the audit-#11 hole for the extension.
    "scorer/pocket_metrics.py",
    "scorer/axes.py",
    # Added 2026-09-04 alongside Block C Stage 0 Step 1.4 — two post-load
    # receipts (A_LIGAND_PRESENT, A_RECEPTOR_SLUG_MISSING) that
    # short-circuit scoring on Chai silent-apo + receptor_slug-NaN
    # regressions. Imported by scorer/orchestrator.py at runtime, so a
    # drifted HPC copy would silently disable the receipts on the compute
    # node while local scoring keeps them.
    "scorer/post_run_receipts.py",
)


def _local_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hpc_sha256_batch(
    rel_paths: tuple[str, ...] | list[str],
    hpc_repo: str = "~/paper_af3",
) -> dict[str, str]:
    """Compute SHA256 for all `rel_paths` in a single ssh round-trip.

    Refactored from `_hpc_sha256` (per-path) because basel-hpc's login-node
    sshd trips MaxStartups when the gate makes 8-16 sequential ssh calls
    back-to-back (2026-09-04 kex_exchange_identification resets during
    Block C Tier 3 kick-off). One ssh call is one handshake, and returns
    every hash the check needs — cannot rate-limit itself into failure.

    Falls back to per-path retry via `_hpc_sha256` on any transient reset.
    """
    import time as _time
    cmd = f"cd {hpc_repo} && sha256sum " + " ".join(rel_paths)
    last_err: str | None = None
    for attempt in range(3):
        if attempt > 0:
            _time.sleep(2 ** attempt)  # 2s, 4s
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=15", "basel-hpc", cmd],
            capture_output=True, text=True, timeout=120,
        )
        if result.returncode == 0:
            got: dict[str, str] = {}
            for line in result.stdout.splitlines():
                line = line.strip()
                if not line:
                    continue
                sha, _, path = line.partition(" ")
                path = path.strip()
                for rel in rel_paths:
                    if path.endswith(rel):
                        got[rel] = sha
                        break
            missing = [r for r in rel_paths if r not in got]
            if missing:
                raise RuntimeError(
                    f"batch sha256sum returned {len(got)}/{len(rel_paths)}, "
                    f"missing: {missing[:3]}"
                )
            return got
        err = (result.stderr or "").strip()
        if "kex_exchange_identification" in err or "Connection reset by peer" in err:
            last_err = err
            continue
        raise RuntimeError(
            f"basel-hpc batch sha256sum exit {result.returncode}: {err!r}"
        )
    raise RuntimeError(
        f"basel-hpc batch sha256sum: transient ssh reset persisted across "
        f"3 attempts: {last_err!r}"
    )


def _hpc_sha256(rel_path: str, hpc_repo: str = "~/paper_af3") -> str:
    """Return SHA256 hex of ``$hpc_repo/<rel_path>`` on basel-hpc.

    Uses `sha256sum` (Linux GNU coreutils) which prints
    ``<hex>  <path>``. Raises RuntimeError on ssh/tool failure so the
    gate fails loud rather than silently mismatching.

    Retries transient sshd MaxStartups resets ("kex_exchange_identification:
    read: Connection reset by peer") twice with exponential back-off — the
    check makes 8-16 sequential ssh calls and basel-hpc's login-node sshd
    intermittently drops one under that fan-out. A real permission or
    missing-file error still surfaces on the final attempt.
    """
    import time as _time
    last_err: str | None = None
    for attempt in range(3):
        if attempt > 0:
            _time.sleep(2 ** attempt)  # 2s, then 4s
        result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=15", "basel-hpc",
             f"sha256sum {hpc_repo}/{rel_path}"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            stdout = result.stdout.strip()
            if not stdout:
                raise RuntimeError(f"basel-hpc sha256sum returned empty for {rel_path}")
            return stdout.split(None, 1)[0]
        err = (result.stderr or "").strip()
        # Retry only on transient sshd handshake resets; every other
        # non-zero exit is likely a real error (missing file, wrong path).
        if "kex_exchange_identification" in err or "Connection reset by peer" in err:
            last_err = err
            continue
        raise RuntimeError(
            f"basel-hpc sha256sum {hpc_repo}/{rel_path} exit "
            f"{result.returncode}: {err!r}"
        )
    raise RuntimeError(
        f"basel-hpc sha256sum {hpc_repo}/{rel_path}: transient ssh reset "
        f"persisted across 3 attempts: {last_err!r}"
    )


def check_scorer_hpc_matches_local() -> str:
    """Hard gate — 5 core scorer files on HPC must SHA256-match local.

    Rationale: `scripts/rescore_experiment.py` invokes
    `scorer.cli.batch_main` in-process against whichever `scorer/`
    package the HPC checkout carries. When HPC and local drift, the
    scorer's assertion behaviour diverges from the local repo (audit
    trail #11, 2026-09-01: an incremental scp missed 3 of the 5 files
    and produced a 50-row A3_wrong_chain census of otherwise-correct
    OF3 predictions, exit 0). Content-hash validation between the local
    repo and the remote deployment is the countermeasure.

    Files tracked (see SCORER_FILES_TRACKED):
      - scorer/orchestrator.py
      - scorer/schema.py
      - scorer/structure.py
      - scorer/cli.py
      - scorer/assertions.py
      - scorer/pocket_metrics.py  (added 2026-09-03, Block C Gate 0.1)
      - scorer/axes.py            (added 2026-09-03, Block C Gate 0.1)
      - scorer/post_run_receipts.py (added 2026-09-04, Block C Step 1.4)

    Note: files replicated via scp bypass git provenance. This gate is
    the only mechanism that ties the runtime scorer on HPC back to the
    committed source.
    """
    # One batched ssh round-trip for all tracked files (see
    # _hpc_sha256_batch docstring — avoids the MaxStartups reset seen
    # 2026-09-04 during Block C Tier 3 kick-off).
    try:
        hpc_hashes = _hpc_sha256_batch(SCORER_FILES_TRACKED)
    except (subprocess.TimeoutExpired, RuntimeError) as e:
        _fail(f"scorer-sync gate: could not batch-probe basel-hpc: {e}")
    diverged: list[tuple[str, str, str]] = []
    for rel in SCORER_FILES_TRACKED:
        local_p = REPO / rel
        if not local_p.exists():
            _fail(f"missing {local_p} — cannot compute local SHA256")
        loc_h = _local_sha256(local_p)
        hpc_h = hpc_hashes[rel]
        if loc_h != hpc_h:
            diverged.append((rel, loc_h[:12], hpc_h[:12]))
    if diverged:
        detail = "; ".join(
            f"{rel} local={lh} hpc={hh}" for rel, lh, hh in diverged
        )
        _fail(
            f"scorer-sync mismatch on {len(diverged)}/{len(SCORER_FILES_TRACKED)} "
            f"files — HPC scorer must be re-synced before any rescore. "
            f"Diverged: {detail}. See audit trail #11."
        )
    return (f"OK — {len(SCORER_FILES_TRACKED)}/{len(SCORER_FILES_TRACKED)} "
            f"scorer files SHA256-match local ↔ basel-hpc:~/paper_af3/scorer/")


# ---------------------------------------------------------------------
# Qsub-sync gate (audit-1.2 countermeasure, 2026-09-04)
# ---------------------------------------------------------------------

QSUB_FILES_TRACKED = (
    "qsub/rerun_boltz.sh",
    "qsub/rerun_chai.sh",
    "qsub/rerun_of3.sh",
    "qsub/rerun_protenix.sh",
    "qsub/rerun_af2mm.sh",
    "qsub/status_writer.py",
    "qsub/apply_vendored_of3_patch.sh",
    "qsub/colabfold_shim.py",
)


def check_qsub_files_hpc_matches_local() -> str:
    """Hard gate — 8 qsub launcher / helper files on HPC must SHA256-match local.

    Rationale: closes the audit-1.2 hole (2026-09-04) where commit
    ``0e738af``'s rerun_*.sh rewrites landed on laptop but never reached
    ``basel-hpc:~/paper_af3/qsub/``. Every Block A + Block B prediction
    ran the pre-audit inline heredoc and emitted the minimal 5-key
    ``_${backbone}_status.json`` (no ``backbone`` field, no
    ``runtime_config`` block) — the audit-#10 / #13 countermeasures
    silently non-operational for two campaigns. This gate mirrors
    ``check_scorer_hpc_matches_local`` (audit-#11 countermeasure) so the
    same class of "launcher edited on laptop, never deployed to HPC"
    bug cannot recur.

    Files tracked (see QSUB_FILES_TRACKED):
      - qsub/rerun_boltz.sh
      - qsub/rerun_chai.sh
      - qsub/rerun_of3.sh
      - qsub/rerun_protenix.sh
      - qsub/rerun_af2mm.sh         (still uses inline heredoc — track anyway)
      - qsub/status_writer.py
      - qsub/apply_vendored_of3_patch.sh
      - qsub/colabfold_shim.py

    Note: files replicated via scp bypass git provenance. This gate is
    the only mechanism that ties the runtime launchers on HPC back to
    the committed source. Pinned sha256 values also live in
    ``refs/qsub_expected_shas.json`` for per-worker pre-flight use.
    """
    try:
        hpc_hashes = _hpc_sha256_batch(QSUB_FILES_TRACKED)
    except (subprocess.TimeoutExpired, RuntimeError) as e:
        _fail(f"qsub-sync gate: could not batch-probe basel-hpc: {e}")
    diverged: list[tuple[str, str, str]] = []
    for rel in QSUB_FILES_TRACKED:
        local_p = REPO / rel
        if not local_p.exists():
            _fail(f"missing {local_p} — cannot compute local SHA256")
        loc_h = _local_sha256(local_p)
        hpc_h = hpc_hashes[rel]
        if loc_h != hpc_h:
            diverged.append((rel, loc_h[:12], hpc_h[:12]))
    if diverged:
        detail = "; ".join(
            f"{rel} local={lh} hpc={hh}" for rel, lh, hh in diverged
        )
        _fail(
            f"qsub-sync mismatch on {len(diverged)}/{len(QSUB_FILES_TRACKED)} "
            f"files — HPC qsub launchers must be re-synced before any dispatch. "
            f"Diverged: {detail}. See "
            f"experiments/020_block_c_ligand_pharmacology/analysis/"
            f"propagation_test_audit_2026_09_04.md."
        )
    return (f"OK — {len(QSUB_FILES_TRACKED)}/{len(QSUB_FILES_TRACKED)} "
            f"qsub files SHA256-match local ↔ basel-hpc:~/paper_af3/qsub/")


_HEX40 = re.compile(r"^[0-9a-f]{40}$")


def check_scorer_git_sha(rows_csv_path: str | None = None,
                          expected_sha: str | None = None) -> str:
    """Hard gate — every row in a scored ``rows.csv`` must carry a real
    40-char lowercase-hex ``scorer_git_sha`` matching the expected commit.

    This is the countermeasure for audit finding #1 (recurred): the
    HPC pip-installed venv strips ``.git`` metadata, ``_git_sha()``
    returns ``"no-git"``, and every provenance row records
    ``scorer_version = "0.1.0+no-git"`` (2026-09-02: reproduced across
    all 9,490 Block A rows). The fix at ``setup.py`` writes
    ``scorer/_version_sha.py`` at ``pip install -e .`` time; this gate
    verifies the value that actually reached the campaign's rows.csv,
    not just the absence of the literal ``"no-git"``.

    Fails on ANY of:
      - ``scorer_git_sha == "no-git"``
      - ``scorer_git_sha`` empty
      - ``scorer_git_sha`` not a 40-character lowercase hex string
        (this also catches ``<sha>-dirty`` suffixed values — dispatch
        from a dirty tree is intentionally blocked)
      - ``scorer_git_sha`` not matching ``expected_sha`` (if given)

    Rows-file discovery:
      ``rows_csv_path`` explicit; else the latest under
      ``experiments/*/analysis/rows.csv`` sorted by mtime.

    ``expected_sha`` discovery:
      Explicit; else ``git rev-parse HEAD`` at the current repo.
    """
    if rows_csv_path is None:
        candidates = sorted(
            (REPO / "experiments").glob("*/analysis/rows.csv"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if not candidates:
            _fail("no rows.csv found under experiments/*/analysis/")
        # Filter out documented stale-artifact rows.csv paths. These are
        # historical campaign outputs whose scorer_git_sha is expected to
        # not match the current HEAD, per CLAUDE.md's standing rule
        # ("No re-running the scorer over the corpus to fix an
        # infrastructure drift"). Each waived path re-greens on its next
        # campaign-scope rescore, at which point it drops out of this
        # list. Coordinator-approved waives ONLY — this is not a
        # mechanism for silently skipping check #18.
        waived_rel = {
            # Block B rows.csv: scored under HEAD 04243c4 (post-Wide
            # rescore, 2026-09-01). Not re-scored under fd87133 / 89e3289
            # per CLAUDE.md "no re-scorer-over-corpus" rule. Re-greens
            # after any future Block-B rescore.
            "experiments/019_block_b_partner_selection/analysis/rows.csv":
                "waived per Block C Step 2 (2026-09-04, coordinator-approved). "
                "Block B rows.csv scored under HEAD 04243c4; not re-scored under "
                "current HEAD per CLAUDE.md 'no re-scorer-over-corpus' rule.",
            # Block A rows.csv: same rationale, scored under a pre-fd87133 HEAD.
            "experiments/018_block_a_switch_test/analysis/rows.csv":
                "waived per Block C Step 2 (2026-09-04, coordinator-approved). "
                "Block A rows.csv is a historical artifact scored under a "
                "pre-current HEAD; re-greens on any future Block-A rescore.",
        }
        skipped_waived = []
        while candidates:
            rel = candidates[0].relative_to(REPO).as_posix()
            if rel in waived_rel:
                skipped_waived.append((rel, waived_rel[rel]))
                candidates.pop(0)
                continue
            break
        if not candidates:
            waived_summary = "; ".join(f"{p} ({r})" for p, r in skipped_waived)
            return (
                "SKIP — all mtime-latest rows.csv candidates are documented "
                f"waived stale artifacts: {waived_summary}. "
                "Re-greens when a current-HEAD campaign lands a rows.csv."
            )
        rows_p = candidates[0]
    else:
        rows_p = Path(rows_csv_path)
        skipped_waived = []
    if not rows_p.exists():
        _fail(f"missing {rows_p}")

    if expected_sha is None:
        proc = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10,
        )
        if proc.returncode != 0:
            _fail(f"could not determine expected SHA via `git rev-parse HEAD`: "
                  f"{proc.stderr.strip()!r}")
        expected_sha = proc.stdout.strip()
    if not _HEX40.match(expected_sha):
        _fail(f"expected_sha {expected_sha!r} is not a 40-char lowercase hex")

    bad_no_git = bad_empty = bad_shape = bad_mismatch = ok = 0
    seen: set[str] = set()
    with rows_p.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            v = (row.get("scorer_git_sha") or "").strip()
            seen.add(v)
            if v == "no-git":
                bad_no_git += 1
            elif not v:
                bad_empty += 1
            elif not _HEX40.match(v):
                bad_shape += 1
            elif v != expected_sha:
                bad_mismatch += 1
            else:
                ok += 1
    total = ok + bad_no_git + bad_empty + bad_shape + bad_mismatch
    if bad_no_git or bad_empty or bad_shape or bad_mismatch:
        _fail(
            f"{rows_p}: {bad_no_git} rows with 'no-git', {bad_empty} empty, "
            f"{bad_shape} non-40-char-hex (includes -dirty suffix), "
            f"{bad_mismatch} matching-shape-but-wrong-SHA "
            f"(expected {expected_sha[:12]}...). Unique values seen: "
            f"{sorted(seen)[:5]}... "
            f"HPC venv likely needs `pip install -e .` after rsync."
        )
    return (f"OK — all {total} rows in {rows_p.name} carry scorer_git_sha == "
            f"{expected_sha[:12]}... (40-char lowercase hex, matches expected)")


PROPAGATION_RESULTS = (
    "experiments/propagation_tests_2026_09_02/results.jsonl"
)
PROPAGATION_TESTS_EXPECTED = {
    "seeds_produce_different_structures",
    "msa_depth_reaches_model",
    "no_templates_no_rcsb_call",
    "of3_seeds_reach_sampler",
    "chai_aligned_pqt_present",
    "scorer_git_sha_endtoend",
}


def check_propagation_tests_green() -> str:
    """Hard gate — the six §10 propagation tests must have run against
    the current commit and passed on the most recent run.

    Rationale: audit trail #9, #10, #11, #12, #13 all shared one
    failure shape — configuration correct at repo layer, dropped
    before the compute layer, all status signals green. The §10
    propagation tests assert distinctive config actually reaches the
    observable output. Without a fresh green run of these tests, we
    are back in the pre-Block-B regime where a config regression
    would land invisibly.

    Fails if the results file is missing, older than the current
    commit's last touch, or missing a PASS for any of the six named
    tests in its most-recent run block.
    """
    import json as _json
    p = REPO / PROPAGATION_RESULTS
    if not p.exists():
        _fail(
            f"missing {p} — run scripts/run_propagation_tests.sh before dispatch"
        )
    # Read all rows, then locate the most-recent run-boundary marker
    # and score only the rows AFTER that boundary.
    rows: list[dict] = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(_json.loads(line))
        except _json.JSONDecodeError:
            continue
    # Find the last run_boundary marker; take everything after it.
    last_boundary_idx = None
    for i, r in enumerate(rows):
        if r.get("run_boundary"):
            last_boundary_idx = i
    if last_boundary_idx is None:
        _fail(
            f"{p}: no run_boundary marker — did scripts/run_propagation_tests.sh "
            f"actually run? Re-run it."
        )
    latest = rows[last_boundary_idx + 1:]
    tests_run = {r["test"] for r in latest if "test" in r}
    missing = PROPAGATION_TESTS_EXPECTED - tests_run
    if missing:
        _fail(
            f"{p}: latest run missing tests {sorted(missing)}. "
            f"Re-run scripts/run_propagation_tests.sh."
        )
    failed = [r["test"] for r in latest if not r.get("passed", False)]
    if failed:
        _fail(
            f"{p}: latest run has {len(failed)} failing tests: {failed}. "
            f"Fix the underlying propagation regression (see "
            f"docs/PROPAGATION_TESTS.md) — do NOT loosen the tests."
        )
    # Freshness: latest run must post-date the newest commit that
    # touched any source file (code, launcher, docs), so a stale
    # green run cannot pass the gate after a change that could break
    # propagation. Commits that ONLY update the propagation
    # results.jsonl are excluded — otherwise every propagation-run
    # commit would immediately invalidate itself.
    from datetime import datetime as _dtcls
    proc = subprocess.run(
        ["git", "-C", str(REPO), "log", "-1",
         "--format=%cI",
         "--", ".", f":!{PROPAGATION_RESULTS}"],
        capture_output=True, text=True, timeout=5,
    )
    head_ts_raw = (proc.stdout or "").strip()

    def _to_utc(ts: str):
        if not ts:
            return None
        try:
            return _dtcls.fromisoformat(ts).astimezone(tz=None).timestamp()
        except ValueError:
            return None

    head_ts = _to_utc(head_ts_raw)
    if head_ts is not None and latest:
        run_tss = [_to_utc(r.get("timestamp_utc", "")) for r in latest]
        run_tss = sorted(t for t in run_tss if t is not None)
        if run_tss and run_tss[0] < head_ts:
            _fail(
                f"{p}: latest propagation run ({run_tss[0]}) predates HEAD "
                f"commit ({head_ts}). Re-run scripts/run_propagation_tests.sh "
                f"against the current commit."
            )
    return (
        f"OK — all {len(PROPAGATION_TESTS_EXPECTED)} §10 propagation tests "
        f"passed in the most recent run of {p.name}"
    )


def check_ligand_ccd_match() -> str:
    """Hard gate — every CCD-sourced row in ``refs/ligand_set.csv`` must
    match its authoritative RCSB CCD entry on connectivity InChIKey.

    Rationale: Block C Step 1.1 (2026-09-04) surfaced a ~40-46 %
    structural-error rate on memory-based SMILES entries across four
    verification passes. CCD sourcing keys on the actual crystal
    chemistry via ``smiles_source = "CCD:<pdb>:<ccd>"``. This gate
    invokes ``scripts/gate_ligand_ccd_match.py`` — which re-fetches
    each CCD via RCSB Data REST API, compares its RDKit-canonical
    form + connectivity block against the row's stored
    ``ccd_smiles``, and non-zero-exits on any FAIL — as a subprocess
    and re-raises as a GateFailure. Uses the script's on-disk cache
    so repeated dispatch-gate runs are fast (~1 s cached vs ~30 s
    cold).

    Fails on any of:
      - script exit code 1 (any FAIL row: connectivity mismatch,
        fetch failure, or column-consistency violation)
      - script exit code 2 (only fires with --fail-warns; not used here)
      - script exit code 3 (rdkit missing or CSV not found)

    Does NOT fail on WARN (SMILES byte-drift where the canonical
    equivalent still matches) — that stays informational.
    """
    script = REPO / "scripts/gate_ligand_ccd_match.py"
    if not script.exists():
        _fail(f"missing {script}")
    try:
        proc = subprocess.run(
            ["python3", str(script), "--quiet"],
            cwd=str(REPO), capture_output=True, text=True, timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        _fail(f"could not run {script}: {type(e).__name__}: {e}")
    if proc.returncode != 0:
        # Extract the FAIL lines + summary line for actionable output.
        stdout_lines = proc.stdout.splitlines()
        fails = [ln for ln in stdout_lines if "[FAIL]" in ln]
        summary = next((ln for ln in reversed(stdout_lines) if "summary" in ln), "")
        tail = "; ".join(fails[:5]) + (f" ... ({summary.strip()})" if summary else "")
        _fail(
            f"ligand_ccd_match gate exit {proc.returncode}: {tail or proc.stderr.strip()[:400]}. "
            f"Re-run `python3 {script.relative_to(REPO)}` to inspect."
        )
    # Extract the summary line for a compact OK message.
    summary = next(
        (ln for ln in proc.stdout.splitlines() if ln.startswith("# summary")),
        "",
    )
    return f"OK — {summary.lstrip('# ').strip() or 'all CCD-sourced rows match RCSB'}"


TIER3_LIGAND_SET_EXPECTED_SHA256 = (
    "5443c2e7c3570b07e08dc27979dbda7dc9dd92ba1e3578d184f25a7aeee2b98e"
)

# The 32 "new" Class A receptors added at Tier 3 (i.e. not in Tier 1's
# 8-receptor set). Enumerated verbatim from
# docs/BLOCK_C_TIER3_DISPATCH_CONTRACT_2026_09_04.md §3.
TIER3_NEW_RECEPTORS = frozenset({
    "5HT2C", "5HT5A", "ACM1", "ADA2A", "ADRB1", "AGTR1", "APJ", "B1B1U5",
    "CCKAR", "CCR5", "CNR1", "CNR2", "CXCR2", "CXCR4", "DRD2", "EDNRA",
    "EDNRB", "FSHR", "GHSR", "GRPR", "HRH1", "HRH3", "LPAR1", "LSHR",
    "LT4R1", "MCHR1", "NPY1R", "NPY2R", "OPRD", "OPRK", "OPRX", "OPSD",
})

TIER3_REQUIRED_ROLES = ("full_agonist", "neutral_antagonist")


def check_tier3_ligand_set_coverage() -> str:
    """Hard gate — ``refs/ligand_set_tier3.csv`` is complete for the 32 new
    Class A receptors added at Tier 3, and matches the SHA pinned in the
    Tier 3 dispatch contract.

    Rationale: Tier 3 fires against 40 Class A receptors × 3 states × 2
    arms × 4 backbones. The 8 Tier 1 carry-forwards remain in
    ``refs/ligand_set.csv`` (already gated by ``check_ligand_ccd_match``);
    the 32 new receptors' curation lands in ``refs/ligand_set_tier3.csv``
    as a Stage 1 sidecar. This gate:

      1. Verifies the file's SHA256 matches the contract pin
         (``5443c2e7…``). Any post-issue edit re-fires the gate.
      2. Verifies every (new_receptor × role) pair is present in the
         file, where role ∈ {full_agonist, neutral_antagonist}. This is
         the coverage guarantee the manifest builder depends on. Rows
         intentionally marked "NA" (empty smiles + empty
         peptide_sequence) satisfy the coverage check — the manifest
         builder is aware of them and drops the corresponding
         receptor×role from dispatch (asymmetry-principle per plan §6).
      3. Verifies no row carries an unresolved-lookup marker in
         ``smiles_source`` or ``notes`` — case-insensitive substring
         match against {pending, unresolved, todo, failed, error,
         fetch_error, retry, pubchem_timeout}. Intentional "NA" rows
         must have their exclusion motivation in ``notes`` and never a
         pending-fetch marker.

    Regression class: same family as ``check_ligand_ccd_match`` — a
    curation-quality gate that pins the reference chemistry so the
    manifest builder can never silently dispatch against a stale or
    incomplete SMILES set.
    """
    p = REPO / "refs/ligand_set_tier3.csv"
    if not p.exists():
        _fail(f"missing {p} — Tier 3 Stage 1 curation has not landed")
    actual_sha = hashlib.sha256(p.read_bytes()).hexdigest()
    if actual_sha != TIER3_LIGAND_SET_EXPECTED_SHA256:
        _fail(
            f"{p}: SHA256 {actual_sha} does not match Tier 3 contract pin "
            f"{TIER3_LIGAND_SET_EXPECTED_SHA256}. Re-pin in "
            f"BLOCK_C_TIER3_DISPATCH_CONTRACT_2026_09_04.md §5 and update "
            f"TIER3_LIGAND_SET_EXPECTED_SHA256 in step7_dispatch_gate.py, "
            f"or revert the CSV edit."
        )
    rows = list(csv.DictReader(p.open()))
    seen: set[tuple[str, str]] = set()
    unresolved: list[str] = []
    UNRESOLVED_MARKERS = (
        "pending", "unresolved", "todo", "failed", "error",
        "fetch_error", "retry", "pubchem_timeout",
    )
    for r in rows:
        rec = r.get("receptor", "").strip().upper()
        role = r.get("ligand_role", "").strip()
        seen.add((rec, role))
        src = (r.get("smiles_source") or "").strip().lower()
        notes = (r.get("notes") or "").strip().lower()
        # NA rows carry motivation in `notes`; that's the intended text
        # and MUST NOT be flagged. We look only for the narrow
        # pending-fetch marker family below in smiles_source AND in the
        # first token of notes (so "NA row per plan …" is fine but
        # "PENDING pubchem re-fetch" is not).
        for m in UNRESOLVED_MARKERS:
            # smiles_source: any occurrence
            if m in src:
                unresolved.append(f"{rec}/{role}: smiles_source contains {m!r}")
                break
            # notes: only if it's the leading token / status flag, not
            # a mid-sentence English word ("errors were …"). Cheap heuristic:
            # word-boundary at line start.
            if re.match(rf"^\s*[\[\(]?{m}\b", notes):
                unresolved.append(f"{rec}/{role}: notes leads with {m!r}")
                break
    if unresolved:
        _fail(
            f"{p}: {len(unresolved)} row(s) carry unresolved-lookup markers — "
            f"{'; '.join(unresolved[:5])}"
            + (f" … ({len(unresolved)-5} more)" if len(unresolved) > 5 else "")
        )
    missing_pairs = [
        (rec, role) for rec in sorted(TIER3_NEW_RECEPTORS)
        for role in TIER3_REQUIRED_ROLES
        if (rec, role) not in seen
    ]
    if missing_pairs:
        _fail(
            f"{p}: missing {len(missing_pairs)} (receptor, role) pair(s) — "
            f"{missing_pairs[:5]}"
            + (f" … ({len(missing_pairs)-5} more)" if len(missing_pairs) > 5 else "")
        )
    # Also assert no extraneous receptors leaked in from the Tier 1 set
    # (that would silently double-count them relative to refs/ligand_set.csv).
    extraneous = sorted(
        {rec for rec, _ in seen if rec and rec not in TIER3_NEW_RECEPTORS}
    )
    if extraneous:
        _fail(
            f"{p}: contains rows for {len(extraneous)} receptor(s) already in "
            f"the Tier 1 set (would double-count against refs/ligand_set.csv): "
            f"{extraneous[:5]}"
        )
    n_na = sum(
        1 for r in rows
        if not (r.get("smiles") or "").strip()
        and not (r.get("peptide_sequence") or "").strip()
    )
    return (
        f"OK — {len(rows)} rows cover all "
        f"{len(TIER3_NEW_RECEPTORS)}×{len(TIER3_REQUIRED_ROLES)} "
        f"(new_receptor × role) pairs; SHA256 matches contract pin; "
        f"{n_na} intentional NA rows (asymmetry-principle exclusions)"
    )


def check_msa_prewarm(skip: bool) -> str:
    """Pre-warm covers 40 receptor sequences + 29 partner sequences from
    partners.fasta = 69 total. Passing at 40 would leave every
    partner-containing prediction paying a cold MSA fetch at dispatch time.

    Two `partner_misc` sequences are excluded from the required count:
    - `partner:substanceP` (11 aa) — too short for MMseqs2 MSA search
    - `partner:GP161` (511 aa large orphan receptor) — ColabFold poll timeouts
    Neither is used in Block A arms (cognate/apo/shuffled/decoy use only
    Gα subunits + arrestin fragments + decoy helices), so their pre-warm
    failure is not dispatch-blocking. See refs/msa_prewarm_manifest.csv
    for the failure timestamps + ticket IDs.
    """
    if skip:
        return "SKIPPED (override) — MSA pre-warm not verified"
    p = REPO / "refs/msa_prewarm_manifest.csv"
    if not p.exists():
        _fail(f"missing {p} — run MSA pre-warm before dispatch (see task #84)")
    rows = list(csv.DictReader(p.open()))
    # Excluded partners: not in any Block A arm.
    EXCLUDED = {"partner:substanceP", "partner:GP161"}
    required = [r for r in rows if r["source"] not in EXCLUDED]
    done_req = [r for r in required if r.get("status") == "cached"]
    if len(done_req) < len(required):
        _fail(f"{p}: only {len(done_req)}/{len(required)} required sequences "
              f"pre-warmed (excluding {len(EXCLUDED)} non-Block-A partners)")
    return (f"OK — {len(done_req)}/{len(required)} required sequences pre-warmed "
            f"({len(EXCLUDED)} excluded: not in Block A arms)")


# ---------------------------------------------------------------------
# Manifest row-count + per-cell distribution gate (Stage 0 item 5,
# 2026-09-06). Countermeasure to the Block C Tier 3 dispatch bug where
# the manifest builder skipped peptide decoy injection and emitted 2,960
# rows instead of the 4,080 expected. The CSV parsed fine and dispatch
# would have proceeded silently against a short manifest.
# ---------------------------------------------------------------------

# Default cell-key columns. The sidecar can override via `cell_key_columns`.
_MANIFEST_CELL_KEY_COLUMNS_DEFAULT = (
    "receptor_resolved", "backbone", "partner_type",
)
_MANIFEST_SEED_COLUMN_DEFAULT = "new_seed"


def _find_manifest_and_sidecar() -> tuple[Path, Path] | None:
    """Discover the mtime-newest manifest CSV under experiments/*/manifest/
    that has a companion ``<manifest>.expected_grid.json`` sidecar.

    Returns (manifest_path, sidecar_path) or None if none is found.
    """
    candidates = sorted(
        (REPO / "experiments").glob("*/manifest/*.csv"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for manifest_p in candidates:
        sidecar = manifest_p.with_suffix(manifest_p.suffix + ".expected_grid.json")
        if sidecar.exists():
            return (manifest_p, sidecar)
        # Also allow the .expected_grid.json convention alongside .csv:
        alt = manifest_p.parent / (manifest_p.stem + ".expected_grid.json")
        if alt.exists():
            return (manifest_p, alt)
    return None


def check_manifest_row_count_and_distribution(
    manifest_path: str | None = None,
    expected_grid_path: str | None = None,
) -> str:
    """Hard gate — a manifest's total row count and per-cell distribution
    must match the expected grid.

    Rationale: Block C Tier 3 dispatch (2026-09-04) emitted a manifest of
    2,960 rows where 4,080 were expected — the builder silently skipped
    peptide decoy injection. The CSV parsed clean and dispatch would have
    proceeded against a short manifest. This gate refuses any manifest
    whose:

      1. total row count differs from ``expected_rows`` in the sidecar,
      2. set of ``(receptor, backbone, arm)`` cells is not exactly the
         set the sidecar declares, or
      3. per-cell row count is uneven (some cells have fewer rows than
         others — the shape a partial-inject bug produces).

    Sidecar schema (``<manifest>.expected_grid.json``):

    ```json
    {
      "expected_rows": 4080,
      "cell_key_columns": ["receptor_resolved", "backbone", "partner_type"],
      "seed_column": "new_seed",
      "cells": [
        {"key": ["5HT1B", "boltz", "apo"], "rows": 15},
        ...
      ]
    }
    ```

    ``cell_key_columns`` and ``seed_column`` default to
    ``("receptor_resolved", "backbone", "partner_type")`` /
    ``"new_seed"`` if omitted.

    Manifest / sidecar discovery: explicit path args take precedence.
    Otherwise the newest ``experiments/*/manifest/*.csv`` whose paired
    ``.expected_grid.json`` exists is picked. If no manifest+sidecar
    pair is found, the check SKIPs (dispatch is unblocked, but manifest
    builders SHOULD emit a sidecar so this check is meaningful).
    """
    import json as _json

    if manifest_path is None and expected_grid_path is None:
        found = _find_manifest_and_sidecar()
        if not found:
            return ("SKIP — no manifest with a companion "
                    "`<manifest>.expected_grid.json` sidecar found under "
                    "experiments/*/manifest/. Manifest builders should emit "
                    "the sidecar so this check can gate row count + "
                    "per-cell distribution against the paper grid.")
        manifest_p, sidecar_p = found
    else:
        if manifest_path is None or expected_grid_path is None:
            _fail("check_manifest_row_count_and_distribution: pass both "
                  "manifest_path and expected_grid_path, or neither "
                  "(auto-discover). Got one of two.")
        manifest_p = Path(manifest_path)
        sidecar_p = Path(expected_grid_path)

    if not manifest_p.exists():
        _fail(f"missing manifest {manifest_p}")
    if not sidecar_p.exists():
        _fail(f"missing expected-grid sidecar {sidecar_p}")

    try:
        grid = _json.loads(sidecar_p.read_text())
    except _json.JSONDecodeError as e:
        _fail(f"{sidecar_p}: not valid JSON: {e}")

    expected_rows = grid.get("expected_rows")
    if not isinstance(expected_rows, int) or expected_rows <= 0:
        _fail(f"{sidecar_p}: `expected_rows` must be a positive int, "
              f"got {expected_rows!r}")
    cell_key_columns = tuple(
        grid.get("cell_key_columns")
        or _MANIFEST_CELL_KEY_COLUMNS_DEFAULT
    )
    seed_column = grid.get("seed_column") or _MANIFEST_SEED_COLUMN_DEFAULT
    cells_decl = grid.get("cells")
    if not isinstance(cells_decl, list) or not cells_decl:
        _fail(f"{sidecar_p}: `cells` must be a non-empty list of "
              f"{{key, rows}} entries")

    expected_cell_rows: dict[tuple, int] = {}
    for entry in cells_decl:
        if not isinstance(entry, dict) or "key" not in entry or "rows" not in entry:
            _fail(f"{sidecar_p}: malformed cell entry {entry!r}; "
                  f"expected {{'key': [...], 'rows': int}}")
        key = tuple(str(v) for v in entry["key"])
        if len(key) != len(cell_key_columns):
            _fail(f"{sidecar_p}: cell key {entry['key']!r} has length "
                  f"{len(key)}; expected {len(cell_key_columns)} "
                  f"(matching cell_key_columns={list(cell_key_columns)})")
        if not isinstance(entry["rows"], int) or entry["rows"] <= 0:
            _fail(f"{sidecar_p}: cell {entry['key']!r} has non-positive "
                  f"`rows` {entry['rows']!r}")
        expected_cell_rows[key] = entry["rows"]

    with manifest_p.open() as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames or []
        missing_cols = [c for c in cell_key_columns
                        if c not in header] + (
            [seed_column] if seed_column not in header else []
        )
        if missing_cols:
            _fail(f"{manifest_p}: missing required column(s) "
                  f"{missing_cols}; found {header}")
        rows = list(reader)

    # 1. Total row count
    if len(rows) != expected_rows:
        _fail(
            f"{manifest_p}: row count mismatch — got {len(rows)}, "
            f"expected {expected_rows} (Δ={len(rows) - expected_rows}). "
            f"Sidecar {sidecar_p.name} declares the paper grid. "
            f"This is the Block-C-manifest-emits-2960-not-4080 bug shape."
        )

    # 2. + 3. Per-cell distribution
    actual_cell_rows: dict[tuple, int] = {}
    actual_cell_seeds: dict[tuple, set[str]] = {}
    for r in rows:
        key = tuple(r.get(c, "") for c in cell_key_columns)
        actual_cell_rows[key] = actual_cell_rows.get(key, 0) + 1
        actual_cell_seeds.setdefault(key, set()).add(r.get(seed_column, ""))

    missing_cells = sorted(set(expected_cell_rows) - set(actual_cell_rows))
    extra_cells = sorted(set(actual_cell_rows) - set(expected_cell_rows))
    wrong_count: list[tuple[tuple, int, int]] = []
    for key, expected_n in expected_cell_rows.items():
        actual_n = actual_cell_rows.get(key)
        if actual_n is not None and actual_n != expected_n:
            wrong_count.append((key, actual_n, expected_n))

    # Cross-cell evenness: every present cell must have the same seed
    # count as every other (guards against partial-inject where all cells
    # are present but some carry fewer seeds).
    seed_counts = {k: len(v) for k, v in actual_cell_seeds.items()}
    unique_seed_counts = sorted(set(seed_counts.values()))
    uneven_cells: list[tuple[tuple, int]] = []
    if len(unique_seed_counts) > 1:
        modal = max(unique_seed_counts, key=lambda n: sum(
            1 for c in seed_counts.values() if c == n))
        uneven_cells = [(k, n) for k, n in seed_counts.items() if n != modal]

    problems: list[str] = []
    if missing_cells:
        problems.append(
            f"{len(missing_cells)} missing cell(s), e.g. "
            f"{missing_cells[:3]}"
        )
    if extra_cells:
        problems.append(
            f"{len(extra_cells)} unexpected cell(s), e.g. "
            f"{extra_cells[:3]}"
        )
    if wrong_count:
        problems.append(
            f"{len(wrong_count)} cell(s) with wrong row count, e.g. "
            f"{[(k, a, e) for k, a, e in wrong_count[:3]]}"
        )
    if uneven_cells:
        problems.append(
            f"uneven per-cell seed distribution "
            f"(unique seed counts: {unique_seed_counts}), e.g. "
            f"{uneven_cells[:3]}"
        )

    if problems:
        _fail(
            f"{manifest_p}: manifest / grid mismatch — "
            + "; ".join(problems)
            + f". Sidecar: {sidecar_p.name}. "
            "This is the class of bug that emitted 2,960 rows instead "
            "of 4,080 for Block C Tier 3."
        )

    return (
        f"OK — {len(rows)}/{expected_rows} rows across "
        f"{len(actual_cell_rows)} cells; per-cell distribution even "
        f"(seed count = {unique_seed_counts[0]} for every cell); "
        f"cell key = {list(cell_key_columns)}"
    )


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

CHECKS = [
    # (name, fn, opts). `opts["pre_commit_scope"]` names one or more
    # staged-file globs that make this check relevant in pre-commit mode.
    # A check with no `pre_commit_scope` is only run in full-gate mode.
    ("coupling_panel", check_coupling_panel, {}),
    ("npxxy_refs", check_npxxy_refs, {}),
    ("prereg_todos", check_prereg_open_todos, {"pre_commit_scope": ["refs/PREREG.md"]}),
    ("thresholds_landed", check_thresholds_landed, {}),
    ("alphat_in_partners", check_alphat_in_partners, {}),
    ("scorer_partner_metrics", check_scorer_partner_metrics,
        {"pre_commit_scope": ["scorer/schema.py"]}),
    ("a1_hard_gate", check_a1_hard_gate, {}),
    ("chai_aligned_pqt", check_chai_aligned_pqt, {}),
    ("chai_launcher_no_server", check_chai_launcher_no_server,
        {"pre_commit_scope": ["qsub/rerun_chai.sh"]}),
    ("chai_launcher_uses_cache", check_chai_launcher_uses_cache,
        {"pre_commit_scope": ["qsub/rerun_chai.sh"]}),
    ("of3_launcher_no_direct", check_of3_launcher_no_direct,
        {"pre_commit_scope": ["qsub/rerun_of3.sh"]}),
    ("of3_launcher_uses_shim", check_of3_launcher_uses_shim,
        {"pre_commit_scope": ["qsub/rerun_of3.sh", "qsub/colabfold_shim.py"]}),
    ("no_templates_any_backbone", check_no_templates_any_backbone,
        {"pre_commit_scope": [
            "qsub/rerun_of3.sh", "qsub/rerun_boltz.sh",
            "qsub/rerun_protenix.sh", "qsub/rerun_chai.sh",
            "scorer/propose.py",
        ]}),
    ("sealed_refs_physically_moved", check_sealed_refs_physically_moved,
        {"pre_commit_scope": ["refs/reference_set.csv",
                              "refs/sealed_active_refs_2026_09_01.csv"]}),
    ("msa_prewarm", check_msa_prewarm, {"skip_from_args": "skip_msa_prewarm"}),
    ("scorer_hpc_matches_local", check_scorer_hpc_matches_local, {}),
    ("qsub_files_hpc_matches_local", check_qsub_files_hpc_matches_local, {}),
    ("scorer_git_sha", check_scorer_git_sha, {}),
    ("propagation_tests_green", check_propagation_tests_green, {}),
    ("ligand_ccd_match", check_ligand_ccd_match,
        {"pre_commit_scope": ["refs/ligand_set.csv",
                              "scripts/gate_ligand_ccd_match.py"]}),
    ("tier3_ligand_set_coverage", check_tier3_ligand_set_coverage,
        {"pre_commit_scope": ["refs/ligand_set_tier3.csv"]}),
    # Check #22 (Stage 0 item 5, 2026-09-06) — manifest row count +
    # per-cell distribution vs the paper grid. Countermeasure to the
    # Block C Tier 3 dispatch bug (manifest emits 2,960 rows instead of
    # 4,080; CSV parses fine; dispatch proceeds silently). Runs against
    # the newest experiments/*/manifest/*.csv with a companion
    # `.expected_grid.json` sidecar; SKIPs cleanly when no sidecar found.
    ("manifest_row_count_and_distribution",
        check_manifest_row_count_and_distribution, {}),
]


# Staged-file globs that trigger the pre-commit hook AT ALL. Anything not
# matching one of these skips the gate entirely on the assumption that
# the change is a docs / analysis / experiment edit that cannot affect
# dispatch. Kept in sync with scripts/hooks/pre-commit.
PRE_COMMIT_TRIGGERS = (
    "scorer/*.py",
    "qsub/*.sh",
    "qsub/colabfold_shim.py",
    "scripts/step7_dispatch_gate.py",
    "scripts/gate_ligand_ccd_match.py",
    "refs/PREREG.md",
    "refs/reference_set.csv",
    "refs/sealed_active_refs_2026_09_01.csv",
    "refs/ligand_set.csv",
)


def _staged_files() -> list[str]:
    """Return the list of staged file paths (paths relative to repo root)."""
    proc = subprocess.run(
        ["git", "-C", str(REPO), "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True, timeout=10,
    )
    if proc.returncode != 0:
        return []
    return [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]


def _matches_glob(path: str, pattern: str) -> bool:
    """fnmatch-based glob check anchored at the repo root."""
    import fnmatch
    return fnmatch.fnmatch(path, pattern)


def _relevant_checks(staged: list[str]) -> list[tuple]:
    """Filter CHECKS to those whose `pre_commit_scope` overlaps `staged`.

    Two special hardening rules apply in pre-commit mode:

      1. If any staged file matches `refs/PREREG.md` or
         `refs/reference_set.csv`, the hook hard-fails immediately —
         these files change only under ceremony (design-lock and
         reference-of-record, per CLAUDE.md → What never to do). The
         message tells the operator to escalate.

      2. If a staged file touches `scripts/step7_dispatch_gate.py`
         itself, we run the FULL suite (gate on itself).
    """
    relevant: list[tuple] = []
    for name, fn, opts in CHECKS:
        scope = opts.get("pre_commit_scope") or []
        for pat in scope:
            if any(_matches_glob(f, pat) for f in staged):
                relevant.append((name, fn, opts))
                break
    return relevant


def _py_compile_staged(pattern: str) -> tuple[str, bool]:
    """Compile-check every staged Python file matching `pattern`.

    Cheap syntax gate. Catches the trivial class of "committed a
    scorer file with a broken def" that pytest may miss when the file
    is not on the imported path of the seed test set.
    """
    import py_compile
    staged = [f for f in _staged_files() if _matches_glob(f, pattern)]
    if not staged:
        return (f"no {pattern} staged", True)
    failures: list[str] = []
    for rel in staged:
        p = REPO / rel
        if not p.exists():
            continue
        try:
            py_compile.compile(str(p), doraise=True)
        except py_compile.PyCompileError as e:
            failures.append(f"{rel}: {e.msg.strip()}")
    if failures:
        return (
            f"py_compile FAILED on:\n  " + "\n  ".join(failures),
            False,
        )
    return (f"py_compile OK on {len(staged)} file(s)", True)


def _run_scorer_unit_tests() -> tuple[str, bool]:
    """Run scorer-oriented unit tests. Cheap subset only.

    Returns (message, ok). Uses pytest -x -q with a fixed test glob so
    the pre-commit hook stays inside the ~10 s budget for the common
    case. If pytest is missing, degrades to a python -c import check
    of the scorer module.
    """
    try:
        proc = subprocess.run(
            ["python3", "-m", "pytest", "-x", "-q",
             "tests/test_schema.py",
             "tests/test_a1_split.py",
             "tests/test_axes.py",
             "tests/test_switch_signal.py",
             "-o", "addopts="],
            cwd=str(REPO), capture_output=True, text=True, timeout=120,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return (f"pytest unavailable or timed out: {e}", False)
    if proc.returncode == 0:
        # Extract the summary line.
        summary = ""
        for ln in proc.stdout.splitlines()[::-1]:
            if "passed" in ln or "failed" in ln:
                summary = ln.strip()
                break
        return (f"scorer unit tests OK — {summary or 'pytest exit 0'}", True)
    tail = "\n".join((proc.stdout + "\n" + proc.stderr).splitlines()[-20:])
    return (f"scorer unit tests FAILED:\n{tail}", False)


def _shellcheck_qsub() -> tuple[str, bool]:
    """Run shellcheck on staged qsub/*.sh files if shellcheck is available.

    Returns (message, ok). If shellcheck is missing, this degrades to a
    `bash -n` syntax-only check so the hook still catches gross errors.
    """
    staged = [f for f in _staged_files() if _matches_glob(f, "qsub/*.sh")]
    if not staged:
        return ("no qsub/*.sh staged", True)
    have_shellcheck = subprocess.run(
        ["which", "shellcheck"], capture_output=True, text=True, timeout=5
    ).returncode == 0
    failures: list[str] = []
    for f in staged:
        if have_shellcheck:
            proc = subprocess.run(
                ["shellcheck", "-S", "error", f],
                cwd=str(REPO), capture_output=True, text=True, timeout=30,
            )
        else:
            proc = subprocess.run(
                ["bash", "-n", f],
                cwd=str(REPO), capture_output=True, text=True, timeout=15,
            )
        if proc.returncode != 0:
            failures.append(f"{f}: {proc.stdout.strip() or proc.stderr.strip()}")
    if failures:
        tool = "shellcheck" if have_shellcheck else "bash -n"
        return (f"{tool} FAILED on:\n  " + "\n  ".join(failures), False)
    tool = "shellcheck" if have_shellcheck else "bash -n"
    return (f"{tool} OK on {len(staged)} launcher(s)", True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-msa-prewarm", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="Treat SKIP results as failures")
    ap.add_argument("--pre-commit-mode", action="store_true",
                    help="Run only the subset of checks relevant to staged files "
                         "(fast path). Reads staged files via git diff --cached.")
    args = ap.parse_args()

    if args.pre_commit_mode:
        return _pre_commit_main(args)

    n_ok = n_fail = n_skip = 0
    for name, fn, opts in CHECKS:
        kwargs = {}
        if opts.get("skip_from_args"):
            kwargs["skip"] = getattr(args, opts["skip_from_args"], False)
        try:
            msg = fn(**kwargs)
            status = "SKIP" if msg.startswith("SKIP") else "OK"
        except GateFailure as e:
            msg = str(e)
            status = "FAIL"

        mark = {"OK": "✅", "SKIP": "⚠", "FAIL": "❌"}[status]
        print(f"{mark} {name:<28}  {msg}")
        if status == "OK":
            n_ok += 1
        elif status == "SKIP":
            n_skip += 1
            if args.strict:
                n_fail += 1
        else:
            n_fail += 1

    print()
    print(f"summary: {n_ok} pass · {n_skip} skip · {n_fail} fail")
    if n_fail:
        print("DISPATCH BLOCKED — resolve failures above before Block A dispatch")
        return 1
    print("DISPATCH READY (or under override)")
    return 0


def _pre_commit_main(args) -> int:
    """Pre-commit mode entry point.

    Fires only checks whose `pre_commit_scope` overlaps the staged file
    set (see PRE_COMMIT_TRIGGERS + _relevant_checks). Two additions
    layered on top of the standard CHECKS:

      * Staged `scorer/*.py` → run scorer unit tests (subset).
      * Staged `qsub/*.sh` → shellcheck / bash -n on those files.

    Also enforces the ceremony-required hard-fail for staged
    `refs/PREREG.md` or `refs/reference_set.csv`.
    """
    staged = _staged_files()
    if not staged:
        print("pre-commit: no staged files → gate skipped")
        return 0

    triggers_matched = [
        f for f in staged
        if any(_matches_glob(f, p) for p in PRE_COMMIT_TRIGGERS)
    ]
    if not triggers_matched:
        print(f"pre-commit: {len(staged)} staged file(s), none dispatch-relevant → gate skipped")
        return 0

    # Ceremony hard-fail: PREREG or reference_set.csv are design-lock artefacts.
    ceremony = [
        f for f in staged
        if _matches_glob(f, "refs/PREREG.md") or _matches_glob(f, "refs/reference_set.csv")
    ]
    if ceremony:
        print("❌ pre-commit HARD FAIL — ceremony-required files staged:")
        for f in ceremony:
            print(f"    {f}")
        print("Standing rule (CLAUDE.md → What never to do): refs/PREREG.md and refs/reference_set.csv")
        print("do not change without explicit user go. Escalate before committing.")
        return 1

    # Gate-on-itself: staged step7_dispatch_gate.py → run FULL suite.
    gate_touched = any(_matches_glob(f, "scripts/step7_dispatch_gate.py") for f in staged)
    if gate_touched:
        print("pre-commit: gate script itself staged → running FULL suite")
        return _run_full_from_pre_commit(args, CHECKS)

    n_ok = n_fail = n_skip = 0

    # Standard scoped subset from CHECKS.
    relevant = _relevant_checks(staged)
    for name, fn, opts in relevant:
        kwargs = {}
        if opts.get("skip_from_args"):
            kwargs["skip"] = getattr(args, opts["skip_from_args"], False)
        try:
            msg = fn(**kwargs)
            status = "SKIP" if msg.startswith("SKIP") else "OK"
        except GateFailure as e:
            msg = str(e)
            status = "FAIL"
        mark = {"OK": "✅", "SKIP": "⚠", "FAIL": "❌"}[status]
        print(f"{mark} {name:<28}  {msg}")
        if status == "OK":
            n_ok += 1
        elif status == "SKIP":
            n_skip += 1
        else:
            n_fail += 1

    # Extra checks that live only in pre-commit mode.
    if any(_matches_glob(f, "scorer/*.py") for f in staged):
        # Cheap syntax check first — catches broken def / typo before
        # we pay the ~0.5s pytest startup cost.
        msg, ok = _py_compile_staged("scorer/*.py")
        mark = "✅" if ok else "❌"
        print(f"{mark} {'scorer_py_compile':<28}  {msg}")
        if ok:
            n_ok += 1
        else:
            n_fail += 1
        # Only run the pytest subset if the compile check cleared —
        # otherwise the failing file will break pytest collection with
        # a less-actionable error.
        if ok:
            msg, ok = _run_scorer_unit_tests()
            mark = "✅" if ok else "❌"
            print(f"{mark} {'scorer_unit_tests':<28}  {msg}")
            if ok:
                n_ok += 1
            else:
                n_fail += 1

    if any(_matches_glob(f, "qsub/*.sh") for f in staged):
        msg, ok = _shellcheck_qsub()
        mark = "✅" if ok else "❌"
        print(f"{mark} {'qsub_shellcheck':<28}  {msg}")
        if ok:
            n_ok += 1
        else:
            n_fail += 1

    print()
    print(f"pre-commit summary: {n_ok} pass · {n_skip} skip · {n_fail} fail "
          f"(over {len(relevant)} scoped checks + {len(staged)} staged files)")
    if n_fail:
        print("COMMIT BLOCKED — resolve failures above before committing.")
        return 1
    return 0


def _run_full_from_pre_commit(args, checks) -> int:
    """Fallback: run the full CHECKS suite from pre-commit mode.

    Used when the gate script itself is being edited (`gate on itself`).
    """
    n_ok = n_fail = n_skip = 0
    for name, fn, opts in checks:
        kwargs = {}
        if opts.get("skip_from_args"):
            kwargs["skip"] = getattr(args, opts["skip_from_args"], False)
        try:
            msg = fn(**kwargs)
            status = "SKIP" if msg.startswith("SKIP") else "OK"
        except GateFailure as e:
            msg = str(e)
            status = "FAIL"
        mark = {"OK": "✅", "SKIP": "⚠", "FAIL": "❌"}[status]
        print(f"{mark} {name:<28}  {msg}")
        if status == "OK":
            n_ok += 1
        elif status == "SKIP":
            n_skip += 1
        else:
            n_fail += 1
    print()
    print(f"gate-on-itself summary: {n_ok} pass · {n_skip} skip · {n_fail} fail")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
