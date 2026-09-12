"""M2.3 fresh-rerun dispatch — recover original input, submit fresh co-fold.

For a given `refs/rerun_manifest.csv` row this module resolves:

  1. The original *input* file that produced the frozen prediction
     (Boltz `input.yaml`, OF3 / Protenix / Chai JSON, AF2-mm FASTA).
  2. The fresh seed derived from the prediction SHA
     (`fresh_seed_for(sha)`).
  3. The output directory the fresh co-fold should land in
     (`/hpc/scratch/sengaad1/paper_af3/rerun/<date>/<slug>/<sha[:12]>/<bb>/seed_<newseed>/`).
  4. For A6-conflict rows: a rewritten input where the receptor slug is
     replaced by `receptor_resolved` (never the mislabelled substring).

Nothing here submits directly — that's `scorer/supervisor.py`'s job. This
module builds *the plan* for one row so the supervisor can round-robin
submit without re-reading the manifest each tick.

Design invariants
-----------------

- Input recovery *searches* — the frozen tree does not have one canonical
  layout. Boltz jobs vary between `<experiment>/<slug>/input.yaml`,
  `<experiment>/inputs/<slug>.yaml`, and per-weekend shims. We walk
  parents up to a bounded depth and return the *closest* input file of
  the expected type.
- The rewritten input for A6-conflict rows is written to a stable
  content-hash path (SHA of the original input bytes plus the
  `receptor_resolved` slug) so re-runs are deterministic.
- Every plan carries the manifest row verbatim as `manifest_row` — the
  supervisor persists this alongside submission state so nothing has to
  be re-inferred if the pipeline restarts.
"""
from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import json
import os
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

from scorer.rerun import fresh_seed_for


# ---------------------------------------------------------------------------
# Backbone binding — one dispatcher entry per supported co-folder
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class BackboneSpec:
    name: str                       # "boltz" | "of3" | "protenix" | "chai" | "af2mm"
    qsub_template: str              # path relative to repo, e.g. "qsub/rerun_boltz.sh"
    input_exts: tuple[str, ...]     # accepted input filenames (yaml, json, fasta)
    input_candidates: tuple[str, ...]  # basenames the recovery loop looks for
    prefers_h100: bool = False      # if true, supervisor prefers H100 slots
                                     # when available; A100 is always OK.


BOLTZ = BackboneSpec(
    name="boltz",
    qsub_template="qsub/rerun_boltz.sh",
    input_exts=(".yaml", ".yml"),
    input_candidates=(
        "input.yaml",
        "input.yml",
        # some weekend arms named their inputs after the receptor slug
        # (e.g. `adrb2_human.yaml`) — supervisor picks the closest .yaml.
    ),
    # 2026-08-26 policy update: Boltz opportunistically routes to H100
    # when the site has free H100 slots. Falls back to A100 pool when
    # H100 saturates (per supervisor's h100_free_slots() live check).
    # Boltz binaries work on H100 (compute_cap 9.0) — PyTorch's
    # auto-detection handles the arch difference.
    prefers_h100=True,
)

OF3 = BackboneSpec(
    name="of3",
    qsub_template="qsub/rerun_of3.sh",
    input_exts=(".json",),
    input_candidates=("input.json", "query.json"),
    prefers_h100=True,   # memory-heavy — H100 helps
)

PROTENIX = BackboneSpec(
    name="protenix",
    qsub_template="qsub/rerun_protenix.sh",
    input_exts=(".json",),
    input_candidates=("input.json", "protenix_input.json"),
    prefers_h100=True,   # fast_layer_norm_cuda_v2 has sm_90 fast path
)

CHAI = BackboneSpec(
    name="chai",
    qsub_template="qsub/rerun_chai.sh",
    input_exts=(".fasta", ".fa"),
    input_candidates=("input.fasta", "chai_input.fasta"),
    # 2026-08-27 GPU benchmark: Chai showed the biggest H100 speedup of
    # the four backbones (1.74-1.85× inference, 2.41× wall on gp101).
    # Route to H100 whenever a free slot exists; falls back to A100
    # cleanly per supervisor.h100_free_slots() live check.
    prefers_h100=True,
)

AF2MM = BackboneSpec(
    name="af2mm",
    qsub_template="qsub/rerun_af2mm.sh",
    input_exts=(".fasta", ".fa"),
    input_candidates=("input.fasta", "af2mm_input.fasta"),
)


BACKBONES: dict[str, BackboneSpec] = {
    bb.name: bb for bb in (BOLTZ, OF3, PROTENIX, CHAI, AF2MM)
}


class UnsupportedBackboneError(ValueError):
    """Raised when a manifest row's backbone has no dispatcher entry."""


class InputRecoveryError(RuntimeError):
    """Raised when no plausible input file can be located for a row."""


# ---------------------------------------------------------------------------
# Input recovery — walk up the prediction path until an input file appears
# ---------------------------------------------------------------------------


# Directory basenames that mean "this is the frozen output, don't recurse in".
_OUTPUT_DIRS = {
    "predictions",
    "boltz_results_input",
    "boltz_results_inputs",
    "seed_0",
    "seed_1",
    "seed_2",
    "seed_3",
    "seed_4",
    "seed_5",
    "seed_42",
}


def _iter_ancestors(path: Path, max_up: int = 8) -> Iterable[Path]:
    """Yield the prediction file's parent, grandparent, ... up to ``max_up``.

    Stops at basel-hpc scratch root or filesystem root, whichever comes
    first, so a bug never walks into `/`.
    """
    p = path if path.is_dir() else path.parent
    hit_scratch_root = False
    for _ in range(max_up):
        yield p
        # Scratch has a well-defined root — one level above the
        # /hpc/scratch/<user>/subsampling*/ dir is out of scope.
        if p.name in ("subsampling", "subsampling-cap-exp", "paper_af3"):
            hit_scratch_root = True
        parent = p.parent
        if parent == p or hit_scratch_root:
            break
        p = parent


def find_original_input(prediction_path: str | os.PathLike[str],
                        backbone: BackboneSpec,
                        *,
                        max_up: int = 8) -> Path:
    """Search ancestor directories for the co-folder's input file.

    Returns the *closest* candidate to the prediction — i.e. the deepest
    ancestor that contains a file matching the backbone's accepted
    extensions or explicit basenames.

    The `pathlib.Path.parents` walk skips known-output subdirs so a
    misfiled `input.yaml` inside `boltz_results_input/` is never picked
    up as the source of truth.
    """
    p = Path(prediction_path)
    if not p.exists():
        raise InputRecoveryError(f"prediction does not exist: {p}")

    for ancestor in _iter_ancestors(p, max_up=max_up):
        # Skip ancestors that are themselves known-output containers —
        # a rogue `input.yaml` inside `boltz_results_input/` is not the
        # real input for the row and must not be silently picked up.
        if ancestor.name in _OUTPUT_DIRS:
            continue
        # First check for exact-basename matches (most reliable)
        for candidate in backbone.input_candidates:
            hit = ancestor / candidate
            if hit.is_file():
                return hit
        # Then look for any file matching the backbone's extension in
        # this directory only (not recursively — recursion would drag
        # in outputs from sibling arms).
        try:
            entries = sorted(ancestor.iterdir())
        except (OSError, PermissionError) as e:
            # Ancestor exists but we can't list it — permission denied on
            # a squashed dir, transient NFS error, etc. Skip it: the loop
            # keeps walking up, and if no ancestor is listable we still
            # raise InputRecoveryError at the end (the caller notices).
            entries = []
            _ = e
        for entry in entries:
            if entry.is_dir() and entry.name in _OUTPUT_DIRS:
                continue
            if entry.is_file() and entry.suffix.lower() in backbone.input_exts:
                # Skip obvious non-input yamls (e.g. `config.yaml` sitting
                # next to a run script — but keep `input.yaml`/`*.yaml`
                # ambiguity resolvable by preferring an explicit
                # basename above).
                if entry.name.lower().startswith(
                        ("config", "cluster", "readme", "notes")):
                    continue
                return entry

    raise InputRecoveryError(
        f"no input.{'/'.join(backbone.input_exts)} found within {max_up} "
        f"levels above {p}"
    )


# ---------------------------------------------------------------------------
# A6-conflict input rewrite — swap the mislabelled receptor slug
# ---------------------------------------------------------------------------


def _swap_receptor_in_bytes(data: bytes, wrong: str, right: str) -> bytes:
    """Replace whole-word occurrences of ``wrong`` with ``right`` in ``data``.

    Uses word-boundary regex so ADA2A never nukes AA2AR (or vice versa)
    inside a longer identifier. Case-insensitive on the *lookup*,
    case-preserving on the substitution — an input file that spells the
    slug lowercase or uppercase keeps its capitalisation for the
    non-swapped surroundings.
    """
    text = data.decode("utf-8", errors="replace")
    pat = re.compile(rf"(?<![A-Za-z0-9])({re.escape(wrong)})(?![A-Za-z0-9])",
                     re.IGNORECASE)

    def repl(m: re.Match[str]) -> str:
        # Match the case of the found token: all-upper → right upper,
        # all-lower → right lower, otherwise keep title of `right`.
        found = m.group(1)
        if found.isupper():
            return right.upper()
        if found.islower():
            return right.lower()
        return right

    return pat.sub(repl, text).encode("utf-8")


def rewrite_input_for_a6_conflict(
        original_input: Path,
        wrong_receptor: str,
        right_receptor: str,
        cache_dir: Path,
) -> Path:
    """For A6-conflict rows, write a corrected copy of the input under
    ``cache_dir/<sha_of_original>_<right_receptor>.<ext>`` and return the
    new path. The mapping is content-addressed so identical originals
    share one rewrite.
    """
    original_bytes = original_input.read_bytes()
    rewritten = _swap_receptor_in_bytes(
        original_bytes, wrong_receptor, right_receptor
    )
    if rewritten == original_bytes:
        # No occurrence to swap — return the original unchanged so the
        # supervisor doesn't burn a slot on a no-op copy. This happens
        # when the receptor slug lives in the *filename* only, not the
        # payload; the caller (`ReRunPlan.input_effective`) still logs
        # the conflict flag so the discrepancy is not silent.
        return original_input

    orig_sha = hashlib.sha256(original_bytes).hexdigest()[:16]
    ext = original_input.suffix or ".txt"
    cache_dir.mkdir(parents=True, exist_ok=True)
    out = cache_dir / f"{orig_sha}_{right_receptor.lower()}{ext}"
    if not out.exists():
        # Write atomically — a partial file left by a crashed writer
        # would silently poison downstream co-fold jobs.
        tmp = out.with_suffix(out.suffix + ".tmp")
        tmp.write_bytes(rewritten)
        os.replace(tmp, out)
    return out


# ---------------------------------------------------------------------------
# Fresh-rerun plan — one row → all info the supervisor needs to submit
# ---------------------------------------------------------------------------


@dataclass
class ReRunPlan:
    """Everything the supervisor needs to submit one fresh co-fold job."""
    # Provenance from the manifest row
    manifest_row: Mapping[str, str] = field(default_factory=dict)
    prediction_path: str = ""
    prediction_sha: str = ""
    experiment_slug: str = ""
    receptor_effective: str = ""    # receptor_resolved if set, else substring
    a6_conflict_corrected: bool = False

    # Derived
    backbone: BackboneSpec = BOLTZ
    fresh_seed: int = 0
    original_input_path: Path = Path()
    effective_input_path: Path = Path()   # == original unless A6-corrected
    out_dir: Path = Path()
    qsub_template: str = ""
    # Diversity-study add-on — samples-per-seed multiplier the qsub
    # template consumes as `PRED_SAMPLES`. Default 1 keeps every
    # historical qsub invocation byte-identical.
    n_samples: int = 1

    # Provenance envelope written next to the fresh run — lets M2.5
    # rescore recover which frozen row this came from.
    def sidecar(self) -> dict[str, Any]:
        return {
            "manifest_row": dict(self.manifest_row),
            "prediction_path_frozen": self.prediction_path,
            "prediction_sha_frozen": self.prediction_sha,
            "experiment_slug": self.experiment_slug,
            "backbone": self.backbone.name,
            "receptor_effective": self.receptor_effective,
            "a6_conflict_corrected": self.a6_conflict_corrected,
            "fresh_seed": self.fresh_seed,
            "n_samples": self.n_samples,
            "original_input_path": str(self.original_input_path),
            "effective_input_path": str(self.effective_input_path),
            "out_dir": str(self.out_dir),
            "created_utc": _dt.datetime.now(_dt.timezone.utc)
                                       .isoformat(timespec="seconds"),
        }


def _is_propose_row(row: Mapping[str, str]) -> bool:
    """True when the row was emitted by ``gpcr-propose`` — carries a
    non-empty ``input_path`` and an empty ``prediction_sha``.

    Proposal manifests describe a run that hasn't happened yet. The
    input file has been materialised on disk (input_path/input_sha are
    set) but no fold output exists (prediction_sha stays empty until
    the fold model runs).

    M2.4 rerun-manifest rows are the other case: they refer to an
    existing frozen prediction. ``prediction_sha`` is populated at
    hydration time and ``input_path`` is absent from the schema.
    """
    return bool(row.get("input_path", "").strip())


def propose_row_key(row: Mapping[str, str]) -> str:
    """Composite primary key for a propose-shape row.

    Boltz-style backbones take the seed as a runtime argument rather
    than embedding it in the input YAML, so multiple seeds on the same
    proposal share one input file and one ``input_sha``. Using
    ``input_sha`` alone as the status key would collapse them into a
    single tracked row.

    Compose ``sha256(input_sha + "|" + new_seed)`` (full 64-hex-char
    digest, the supervisor takes the first 12 chars as usual) so each
    (input, seed) pair is tracked independently. Returns "" when either
    field is missing (falls through to the M2.4 fallback in the
    supervisor).
    """
    isha = (row.get("input_sha") or "").strip()
    seed = (row.get("new_seed") or "").strip()
    if not isha or not seed:
        return ""
    return hashlib.sha256(f"{isha}|{seed}".encode("utf-8")).hexdigest()


def plan_row(
        row: Mapping[str, str],
        *,
        rerun_root: Path,
        rewrite_cache: Path,
        date_stamp: str | None = None,
) -> ReRunPlan:
    """Turn a manifest row into a fully-resolved rerun plan.

    Handles two manifest shapes:

    * **Rerun manifest** (M2.4, ``refs/rerun_manifest.csv``): the row
      references an existing frozen prediction. Uses
      ``find_original_input(prediction_path, ...)`` to walk up the
      frozen tree and locate the co-fold input file.

    * **Propose manifest** (Layer 3, ``refs/proposals/<id>.manifest.csv``):
      the row carries the input file's on-disk location in
      ``input_path`` (materialised by ``gpcr-propose``). No frozen
      prediction exists yet — ``prediction_sha`` is empty. The
      dispatcher uses ``input_sha`` as the primary key and honours the
      row's ``new_seed`` verbatim (already derived deterministically
      from the request/backbone/seed_index).

    The distinction is drawn by ``_is_propose_row(row)`` — non-empty
    ``input_path`` means propose.

    Raises
    ------
    UnsupportedBackboneError
        Manifest row has ``backbone`` = "unknown" or a name this module
        does not know how to submit.
    InputRecoveryError
        (Rerun mode) original input file cannot be located from the
        prediction path.
        (Propose mode) ``input_path`` file does not exist on disk.
    """
    bb_name = row.get("backbone", "").strip()
    if bb_name not in BACKBONES:
        raise UnsupportedBackboneError(
            f"row backbone={bb_name!r} has no dispatcher entry "
            f"(supported: {sorted(BACKBONES)})"
        )
    bb = BACKBONES[bb_name]

    if _is_propose_row(row):
        return _plan_propose_row(row, bb, rerun_root=rerun_root,
                                 date_stamp=date_stamp)

    # M2.4 rerun path — unchanged behaviour
    prediction_path = row["prediction_path"]
    prediction_sha = row.get("prediction_sha", "") or ""
    if not prediction_sha:
        # M2.1 shipped the manifest with `prediction_sha` empty. The
        # supervisor is expected to fill it via
        # `scorer.cache.content_sha256(prediction_path)` at plan time and
        # persist it — either patch the manifest or pass a filled row.
        raise InputRecoveryError(
            f"row has empty prediction_sha; the supervisor must fill "
            f"it before planning (path={prediction_path})"
        )

    fresh_seed = fresh_seed_for(prediction_sha)

    # Resolve receptor slug — prefer the corrected value, fall back to
    # substring if resolver was silent.
    receptor_effective = (row.get("receptor_resolved", "").strip()
                          or row.get("receptor_from_path_substring", "?").strip())

    original_input = find_original_input(prediction_path, bb)

    # A6 rewrite: only when the substring rule disagreed with the
    # word-boundary resolver AND the substring had a non-empty guess.
    a6_conflict = str(row.get("disambig_conflict", "")).lower() == "true"
    if a6_conflict and receptor_effective and receptor_effective != "?":
        wrong = row["receptor_from_path_substring"]
        right = receptor_effective
        effective_input = rewrite_input_for_a6_conflict(
            original_input, wrong, right, rewrite_cache
        )
        corrected = (effective_input != original_input)
    else:
        effective_input = original_input
        corrected = False

    stamp = date_stamp or _dt.date.today().strftime("%Y-%m-%d")
    out_dir = (rerun_root / stamp / row["experiment_slug"]
                            / prediction_sha[:12]
                            / bb.name
                            / f"seed_{fresh_seed}")

    return ReRunPlan(
        manifest_row=dict(row),
        prediction_path=prediction_path,
        prediction_sha=prediction_sha,
        experiment_slug=row["experiment_slug"],
        receptor_effective=receptor_effective,
        a6_conflict_corrected=corrected,
        backbone=bb,
        fresh_seed=fresh_seed,
        original_input_path=original_input,
        effective_input_path=effective_input,
        out_dir=out_dir,
        qsub_template=bb.qsub_template,
        n_samples=_row_n_samples(row),
    )


def _plan_propose_row(
        row: Mapping[str, str],
        bb: BackboneSpec,
        *,
        rerun_root: Path,
        date_stamp: str | None = None,
) -> ReRunPlan:
    """Propose-manifest branch of :func:`plan_row`.

    The propose flow already materialised the input file (Layer 3) and
    stamped its SHA in ``input_sha``. Nothing needs to be discovered —
    just wrap the row's declared paths in a ``ReRunPlan``.

    ``fresh_seed`` uses the row's ``new_seed`` field verbatim (already
    a positive int derived deterministically at propose time). Falls
    back to ``fresh_seed_for(input_sha)`` if the row somehow shipped
    without ``new_seed`` populated.

    The output directory follows the propose schema — the row's
    ``prediction_path`` is a fully-qualified file path
    (``<output_root>/<request_id>/<sha12>/<backbone>/seed_<seed>/<leaf>``)
    so ``out_dir`` is simply its parent. No date-stamp injection —
    the propose flow already namespaces by request_id.
    """
    input_path = Path(row["input_path"])
    if not input_path.exists():
        raise InputRecoveryError(
            f"propose input file does not exist: {input_path}. Was "
            f"`gpcr-propose --materialise` run before dispatching?"
        )
    input_sha = row.get("input_sha", "") or ""
    if not input_sha:
        raise InputRecoveryError(
            f"propose row missing input_sha (row={dict(row)!r})"
        )

    seed_str = row.get("new_seed", "").strip()
    try:
        fresh_seed = int(seed_str)
    except ValueError:
        fresh_seed = fresh_seed_for(input_sha)

    # Row-identity SHA — composite of (input_sha, seed) so multiple seeds
    # on the same input file (Boltz-style, seed is a runtime arg) are
    # tracked as distinct rows. See `propose_row_key`.
    row_key = propose_row_key(row) or input_sha

    receptor_effective = (row.get("receptor_resolved", "").strip()
                          or row.get("receptor_from_path_substring", "?").strip())

    prediction_path = row.get("prediction_path", "")
    if prediction_path:
        out_dir = Path(prediction_path).parent
    else:
        # No prediction_path — synthesise one from the request layout.
        request_id = row.get("request_id", row.get("experiment_slug", "propose"))
        out_dir = (rerun_root / request_id / input_sha[:12]
                   / bb.name / f"seed_{fresh_seed}")

    return ReRunPlan(
        manifest_row=dict(row),
        prediction_path=prediction_path,
        # `prediction_sha` is the row identity used by the supervisor's
        # status tracking + the qsub job-name. For propose rows this is
        # the composite (input_sha, seed) key — see propose_row_key.
        prediction_sha=row_key,
        experiment_slug=row.get("experiment_slug", row.get("request_id", "propose")),
        receptor_effective=receptor_effective,
        a6_conflict_corrected=False,   # propose rows are wt-anchor by construction
        backbone=bb,
        fresh_seed=fresh_seed,
        original_input_path=input_path,
        effective_input_path=input_path,
        out_dir=out_dir,
        qsub_template=bb.qsub_template,
        n_samples=_row_n_samples(row),
    )


def _row_n_samples(row: Mapping[str, str]) -> int:
    """Return ``samples_per_seed`` from a manifest row.

    Robust to missing / empty / malformed values: any non-positive int or
    unparseable string falls back to 1 (the historical default). Preserves
    byte-identical behaviour on every manifest that predates the
    diversity-study extension.
    """
    raw = (row.get("samples_per_seed") or "").strip()
    if not raw:
        return 1
    try:
        n = int(raw)
    except ValueError:
        return 1
    return n if n >= 1 else 1


def build_qsub_command(plan: ReRunPlan, *, repo_root: Path) -> list[str]:
    """Compose the ``qsub`` argv for a single ``ReRunPlan``.

    The qsub template consumes four env vars set on the command line:

      * ``PRED_INPUT``    — the co-folder's input file (yaml/json/fasta)
      * ``PRED_OUT_DIR``  — where the fresh prediction lands
      * ``PRED_SEED``     — the fresh integer seed
      * ``PRED_SIDECAR``  — path to the provenance JSON written by the
                            supervisor so this row can be traced back to
                            its manifest origin.

    A single ``-N`` job name embeds the SHA prefix so ``qstat`` output
    stays legible when 10 jobs are running concurrently.
    """
    template = repo_root / plan.qsub_template
    return [
        "qsub",
        "-N", f"pa3_{plan.backbone.name}_{plan.prediction_sha[:8]}",
        "-v",
        (f"PRED_INPUT={plan.effective_input_path},"
         f"PRED_OUT_DIR={plan.out_dir},"
         f"PRED_SEED={plan.fresh_seed},"
         f"PRED_SAMPLES={plan.n_samples},"
         f"PRED_SIDECAR={plan.out_dir}/_rerun_plan.json"),
        str(template),
    ]


# ---------------------------------------------------------------------------
# Manifest loader — the supervisor iterates plans through this
# ---------------------------------------------------------------------------


def iter_manifest_rows(manifest_csv: str | os.PathLike[str],
                       *,
                       backbones: Iterable[str] | None = None,
                       skip_unresolved: bool = True,
                       ) -> Iterable[dict[str, str]]:
    """Stream rows from ``refs/rerun_manifest.csv``.

    ``backbones`` filters to a subset (e.g. ``("boltz",)`` for the
    Boltz-2 pilot in M2.3 step 1).

    ``skip_unresolved`` (default true) drops rows where *both* the
    substring receptor is "?"/empty AND the word-boundary resolver
    returned nothing — these need `--extra-root` first or a manual
    receptor override before they can be re-folded.
    """
    wanted = None if backbones is None else set(backbones)
    with open(manifest_csv, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if wanted is not None and row.get("backbone", "") not in wanted:
                continue
            if skip_unresolved:
                sub = row.get("receptor_from_path_substring", "").strip()
                res = row.get("receptor_resolved", "").strip()
                if sub in ("", "?") and not res:
                    continue
            yield row


# ---------------------------------------------------------------------------
# CLI — smoke-plan a small manifest slice locally
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    import argparse
    p = argparse.ArgumentParser(
        prog="gpcr-rerun-dispatch",
        description="Smoke-plan fresh reruns for a slice of the manifest "
                    "(no submission — prints the qsub argv per row).",
    )
    p.add_argument("--manifest", default="refs/rerun_manifest.csv")
    p.add_argument("--backbone", action="append", default=None,
                   help="Restrict to one or more backbones "
                        "(boltz|of3|protenix|chai|af2mm). Repeat for multi.")
    p.add_argument("--rerun-root",
                   default="/hpc/scratch/sengaad1/paper_af3/rerun")
    p.add_argument("--rewrite-cache",
                   default="/hpc/scratch/sengaad1/paper_af3/rerun/_input_rewrites")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--limit", type=int, default=5,
                   help="Max rows to plan (default: 5 = smoke slice).")
    p.add_argument("--include-a6-only", action="store_true",
                   help="Only rows with disambig_conflict=true. Use to "
                        "verify A6-rewrite path end-to-end.")
    args = p.parse_args(argv)

    rerun_root = Path(args.rerun_root)
    rewrite_cache = Path(args.rewrite_cache)
    repo_root = Path(args.repo_root).resolve()

    n_planned = 0
    n_input_missing = 0
    n_unsupported = 0
    for row in iter_manifest_rows(args.manifest, backbones=args.backbone):
        if args.include_a6_only and str(row.get("disambig_conflict", "")).lower() != "true":
            continue
        try:
            plan = plan_row(row, rerun_root=rerun_root,
                            rewrite_cache=rewrite_cache)
        except InputRecoveryError as e:
            n_input_missing += 1
            print(f"[input-missing] {row.get('prediction_path')}  {e}")
            if n_input_missing + n_planned + n_unsupported >= args.limit:
                break
            continue
        except UnsupportedBackboneError as e:
            n_unsupported += 1
            print(f"[unsupported-bb] {row.get('prediction_path')}  {e}")
            if n_input_missing + n_planned + n_unsupported >= args.limit:
                break
            continue

        argv_qsub = build_qsub_command(plan, repo_root=repo_root)
        print(json.dumps({
            "sha12": plan.prediction_sha[:12],
            "backbone": plan.backbone.name,
            "receptor": plan.receptor_effective,
            "a6_corrected": plan.a6_conflict_corrected,
            "seed": plan.fresh_seed,
            "input": str(plan.effective_input_path),
            "out": str(plan.out_dir),
            "qsub": argv_qsub,
        }))
        n_planned += 1
        if n_planned >= args.limit:
            break

    import sys
    print(json.dumps({
        "planned": n_planned,
        "input_missing": n_input_missing,
        "unsupported": n_unsupported,
    }, indent=2), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
