#!/usr/bin/env python3
"""qsub/status_writer.py — write _<backbone>_status.json with a
runtime_config block.

Motivation (Block B pre-dispatch): the three silent-config bugs this
campaign chased (Chai MSA env, OF3 start_seed=42, HPC scorer drift,
OF3 template default-on) all shared one shape — configuration correct
at the repo layer, dropped before the compute layer, all status
signals green. This writer captures what the compute node ACTUALLY
sees, not what the launcher asked for.

Contract
--------
Each launcher (qsub/rerun_{boltz,chai,of3,protenix}.sh) invokes this
script AFTER the fold call, passing:
  --backbone     boltz | chai | of3 | protenix
  --exit-code    the fold call's exit code
  --seed         the launcher's PRED_SEED
  --out-dir      PRED_OUT_DIR
  --status-json  destination path
  --config-json  a JSON string containing the launcher's view of
                 the config it passed (e.g. msa_directory, n_samples,
                 n_seeds, seeds_yaml, etc.)

The writer emits a JSON with the pre-existing minimal schema:
  {backbone, exit_code, seed, produced_files, n_produced, ok}
PLUS a `runtime_config` sub-object containing:
  package_version    imported at the compute node — the ACTUAL version
                     the process linked against, not the launcher's
                     assumption
  received_config    the launcher's --config-json passed through
                     verbatim — this is what the launcher believes it
                     asked for
  env                the set of env vars the compute node saw for
                     names that gate result-shaping
  host / timestamps  hostname, timestamps at fold-start and status-write
  runtime_probe      backbone-specific extra info — for chai, the
                     .aligned.pqt sha inventory found; for of3, the
                     runner-yaml resolved seeds; …

The pre-existing schema is preserved so existing supervisors / poll
loops don't break. Downstream code only needs to LOOK for the
`runtime_config` sub-object; its absence means the status was written
by a pre-audit launcher.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import socket
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------
# Package-version resolution
# ---------------------------------------------------------------------

_ENV_KEYS = (
    "CHAI_MSA_DIRECTORY",
    "OF3_START_SEED",
    "OF3_VENV",
    "OF3_CKPT",
    "BOLTZ_VENV",
    "BOLTZ_CACHE",
    "PTX_VENV",
    "CHAI_VENV",
    "CUDA_VISIBLE_DEVICES",
    "SGE_HGR_gpu_card",
    "PYTORCH_CUDA_ALLOC_CONF",
    "TORCH_CUDA_ARCH_LIST",
    "COLABFOLD_SIDECAR",
    "OMP_NUM_THREADS",
    "PRED_SAMPLES",
    "PRED_N_SEEDS",
    "JOB_ID",
)


def _package_version(backbone: str) -> dict:
    """Return {module, version, source_path} for the backbone's
    package as it imports on this compute node. Failure to import is
    reported as {import_error: "..."} — never raises.
    """
    if backbone == "boltz":
        module_names = ("boltz",)
    elif backbone == "chai":
        module_names = ("chai_lab", "chai")
    elif backbone == "of3":
        module_names = ("openfold3",)
    elif backbone == "protenix":
        module_names = ("protenix",)
    else:
        return {"import_error": f"unknown backbone: {backbone}"}

    for name in module_names:
        try:
            mod = __import__(name)
        except Exception as e:  # noqa: BLE001
            continue
        version = getattr(mod, "__version__", None)
        if version is None:
            try:
                from importlib.metadata import version as _v
                version = _v(name)
            except Exception:  # noqa: BLE001
                version = None
        return {
            "module": name,
            "version": version,
            "source_path": getattr(mod, "__file__", None),
        }
    return {"import_error": f"could not import any of {module_names}"}


# ---------------------------------------------------------------------
# Backbone-specific runtime probes
# ---------------------------------------------------------------------

def _probe_of3_runner_yaml(runner_yaml: str | None) -> dict:
    """For OF3: resolve the runner yaml's experiment_settings.seeds:
    field. Also record whether --num-model-seeds was passed. The seed
    bug (audit #13) manifests as seeds==[2746317213, ...] regardless
    of what the launcher wrote.
    """
    if not runner_yaml or not Path(runner_yaml).exists():
        return {"error": f"runner_yaml missing: {runner_yaml!r}"}
    text = Path(runner_yaml).read_text()
    seeds = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("seeds:"):
            try:
                seeds = json.loads(s.split(":", 1)[1].strip())
            except Exception:  # noqa: BLE001
                seeds = s.split(":", 1)[1].strip()
    return {
        "runner_yaml_path": runner_yaml,
        "resolved_seeds": seeds,
        "sentinel_bug_seed_present": (
            isinstance(seeds, list) and 2746317213 in seeds
        ),
    }


def _probe_chai_msa_cache(msa_dir: str | None, pred_input: str | None) -> dict:
    """For Chai: inventory the .aligned.pqt files that would be read
    for this prediction. Cache-mode confirmation vs single-seq silent
    fallback (audit #10).
    """
    import hashlib
    result = {
        "msa_directory": msa_dir,
        "msa_mode": "cache" if msa_dir else "unknown",
    }
    if not msa_dir or not pred_input or not Path(pred_input).exists():
        result["error"] = "pred_input or msa_dir missing"
        return result
    seqs, header, buf = [], None, []
    for line in Path(pred_input).read_text().splitlines():
        line = line.strip()
        if line.startswith(">"):
            if header is not None:
                seqs.append((header, "".join(buf)))
            header, buf = line[1:], []
        elif line:
            buf.append(line)
    if header is not None:
        seqs.append((header, "".join(buf)))
    inventory = []
    for hdr, seq in seqs:
        if not hdr.lower().startswith("protein"):
            continue
        sha = hashlib.sha256(seq.upper().encode()).hexdigest()
        pqt = Path(msa_dir) / f"{sha}.aligned.pqt"
        inventory.append({
            "chain": hdr,
            "seq_sha256": sha,
            "pqt_present": pqt.exists(),
            "pqt_size": pqt.stat().st_size if pqt.exists() else None,
        })
    result["protein_chains"] = inventory
    result["all_present"] = all(x["pqt_present"] for x in inventory)
    return result


def _probe_boltz_input(pred_input: str | None) -> dict:
    """For Boltz: extract the YAML input's msa: field(s) and any
    templates: field. Boltz's silent single-seq fallback isn't the
    same shape as Chai's, but capturing what the YAML actually
    contained is the propagation signal.
    """
    if not pred_input or not Path(pred_input).exists():
        return {"error": f"pred_input missing: {pred_input!r}"}
    text = Path(pred_input).read_text()
    return {
        "input_yaml": pred_input,
        "input_yaml_sha256": _sha256_bytes(text.encode()),
        "has_msa_field": ("msa:" in text) or ("msa_paths:" in text),
        "has_templates_field": "templates:" in text,
    }


def _probe_protenix_input(pred_input: str | None) -> dict:
    """For Protenix: hash the JSON input and record any template-related
    keys.
    """
    if not pred_input or not Path(pred_input).exists():
        return {"error": f"pred_input missing: {pred_input!r}"}
    text = Path(pred_input).read_text()
    try:
        obj = json.loads(text)
    except Exception as e:  # noqa: BLE001
        return {"error": f"pred_input not JSON: {e}"}
    # Protenix inputs are top-level LISTS of query dicts (one per fold).
    # A dict-only top-level indicates a legacy / probe-only input; both
    # shapes handled here — no more silent AttributeError inside the
    # writer, which was masquerading as a failed protenix row across the
    # Block C smoke 2026-09-04 dispatch (fold succeeded, CIFs landed,
    # status.json never written).
    top_level_keys: list = []
    has_templates_top_level = False
    if isinstance(obj, dict):
        top_level_keys = sorted(obj.keys())[:20]
        has_templates_top_level = "templates" in obj
    elif isinstance(obj, list) and obj and isinstance(obj[0], dict):
        top_level_keys = sorted(obj[0].keys())[:20]
        has_templates_top_level = any("templates" in d for d in obj
                                       if isinstance(d, dict))
    return {
        "input_json": pred_input,
        "input_json_sha256": _sha256_bytes(text.encode()),
        "has_template_hits_file": "template_hits_file" in text,
        "has_templates_top_level": has_templates_top_level,
        "top_level_keys": top_level_keys,
    }


def _sha256_bytes(b: bytes) -> str:
    import hashlib
    return hashlib.sha256(b).hexdigest()


# ---------------------------------------------------------------------
# Produced-file discovery — preserves pre-existing schema semantics
# ---------------------------------------------------------------------

def _produced_files(out_dir: Path, backbone: str) -> list[str]:
    if backbone == "boltz":
        files = list(out_dir.rglob("*.cif")) + list(out_dir.rglob("*.pdb"))
    elif backbone == "chai":
        files = list(out_dir.rglob("*.cif")) + list(out_dir.rglob("*.pdb"))
    else:
        files = list(out_dir.rglob("*.cif"))
    return sorted(str(p) for p in files)


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--backbone", required=True,
                    choices=("boltz", "chai", "of3", "protenix"))
    ap.add_argument("--exit-code", type=int, required=True)
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--status-json", type=Path, required=True)
    ap.add_argument("--config-json", type=str, default="{}",
                    help="JSON string of launcher-provided config: "
                         "msa_directory, n_samples, n_seeds, seeds_yaml, "
                         "pred_input, launch_ts_utc, etc.")
    args = ap.parse_args(argv)

    try:
        received_config = json.loads(args.config_json)
    except Exception as e:  # noqa: BLE001
        received_config = {"config_json_parse_error": str(e),
                            "raw": args.config_json}

    produced = _produced_files(args.out_dir, args.backbone)

    env = {k: os.environ.get(k) for k in _ENV_KEYS if k in os.environ}

    runtime_probe: dict
    if args.backbone == "of3":
        runtime_probe = _probe_of3_runner_yaml(
            received_config.get("runner_yaml_path"))
    elif args.backbone == "chai":
        runtime_probe = _probe_chai_msa_cache(
            received_config.get("msa_directory"),
            received_config.get("pred_input"))
    elif args.backbone == "boltz":
        runtime_probe = _probe_boltz_input(received_config.get("pred_input"))
    elif args.backbone == "protenix":
        runtime_probe = _probe_protenix_input(received_config.get("pred_input"))
    else:
        runtime_probe = {"error": f"unknown backbone {args.backbone}"}

    now_iso = _dt.datetime.now(_dt.timezone.utc).isoformat(timespec="seconds")

    status = {
        # Pre-existing minimal schema — never remove these.
        "backbone": args.backbone,
        "exit_code": args.exit_code,
        "seed": args.seed,
        "produced_files": produced,
        "n_produced": len(produced),
        "ok": args.exit_code == 0 and len(produced) > 0,
        # Runtime propagation contract (Block B pre-dispatch).
        "runtime_config": {
            "package_version": _package_version(args.backbone),
            "received_config": received_config,
            "env": env,
            "host": socket.gethostname(),
            "status_write_ts_utc": now_iso,
            "runtime_probe": runtime_probe,
        },
    }

    args.status_json.parent.mkdir(parents=True, exist_ok=True)
    args.status_json.write_text(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
