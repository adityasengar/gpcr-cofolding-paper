"""Scaffold a new experiment folder under ``experiments/<slug>/``.

Analyst supplies a biology-descriptive slug (lowercase snake_case) and a
gpcr-propose YAML spec. This script writes the initial folder structure
with a README template and an empty runs/ subdir. The subagent that
picks up the folder later runs gpcr-propose against the spec, dispatches
qsubs on HPC, and then invokes ``rescore_experiment`` to populate the
per-experiment rows.csv.

Usage:

    scripts/spawn_experiment.py \\
        --slug aa2ar_gs_bimodality_confirm \\
        --spec refs/proposals/aa2ar_gs_bimodality_confirm.yaml

    scripts/spawn_experiment.py \\
        --slug alprenolol_dose \\
        --spec-inline "$(cat <<'EOF'
    request_id: alprenolol_dose
    receptor: ADRB2
    ...
    EOF
    )"

The script is idempotent-refuse: it won't overwrite an existing
``experiments/<slug>/`` unless ``--force`` is passed. Analysts extending
an experiment do NOT run spawn again — they add new files under
``experiments/<slug>/runs/<addition_slug>/`` and edit ``spec.yaml`` in
place.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from textwrap import dedent


REPO = Path(__file__).resolve().parent.parent
EXPERIMENTS_ROOT = REPO / "experiments"


# =============================================================================
# Slug validation
# =============================================================================

# New convention (2026-08-27 evening): experiment folder names carry an
# auto-incremented 3-digit prefix, preserving the analyst-supplied
# biology-descriptive slug verbatim:
#
#     NNN_<biology_slug>
#
# The auto-incrementer walks existing `experiments/\d{3}_*` folders and
# picks max+1. Analysts can also pass a slug that already carries the
# NNN prefix directly via `--slug`.
#
# Two exceptions to the NNN prefix:
#   - `_reference_*` — reserved for reference / baseline folders
#     (v3.7 goes here if we ever fold it into the experiments/ tree)
#   - No other leading underscore permitted
_SLUG_RE = re.compile(
    r"^(?:_reference_[a-z0-9_]{1,55}|\d{3}_[a-z][a-z0-9_]{2,63})$"
)


class SlugError(ValueError):
    """The slug fails validation."""


def validate_slug(slug: str) -> str:
    """Return the normalised slug or raise SlugError with a clear message."""
    s = slug.strip()
    if not s:
        raise SlugError("slug is empty")
    if not _SLUG_RE.match(s):
        raise SlugError(
            f"slug {s!r} is invalid — must be `NNN_<biology_slug>` "
            f"(3-digit prefix + lowercase snake_case, 3-64 chars total, "
            f"[a-z0-9_], no path separators or whitespace). Reference "
            f"folders may start with `_reference_`."
        )
    if "/" in s or "\\" in s or ".." in s:
        raise SlugError(f"slug {s!r} contains a path separator or `..`")
    return s


# ---------------------------------------------------------------------------
# Auto-increment
# ---------------------------------------------------------------------------

_NNN_RE = re.compile(r"^(\d{3})_")


def next_experiment_number(experiments_root: Path) -> int:
    """Return the next 3-digit index to use for a new experiment folder.

    Walks ``experiments/\d{3}_*`` and returns ``max(existing) + 1`` (or
    1 when no numbered folders exist). Skips ``_reference_*``.
    """
    if not experiments_root.exists():
        return 1
    max_n = 0
    for child in experiments_root.iterdir():
        if not child.is_dir():
            continue
        m = _NNN_RE.match(child.name)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return max_n + 1


def compose_slug(biology_slug: str, experiments_root: Path,
                 explicit_number: int | None = None) -> str:
    """Compose ``NNN_<biology_slug>`` from a bare biology slug.

    ``biology_slug`` is what the analyst supplies (e.g.
    ``aa2ar_gs_bimodality_confirm``) — no prefix. If the biology_slug
    already carries a ``\\d{3}_`` prefix, it's returned as-is.
    """
    if _NNN_RE.match(biology_slug):
        return biology_slug
    n = explicit_number if explicit_number is not None \
        else next_experiment_number(experiments_root)
    return f"{n:03d}_{biology_slug}"


# =============================================================================
# README + fasta templates
# =============================================================================


_README_TEMPLATE = dedent("""\
# Experiment: {slug}

## Biology question

<!-- One-sentence framing: what receptor, what perturbation, what are we
     trying to learn? -->

## Hypothesis

<!-- The specific claim this experiment tests. Falsifiable. -->

## Methodology

- Receptor: **(fill from spec.yaml)**
- Partner: **(fill from spec.yaml)**
- Ligand: **(fill from spec.yaml — small_molecule / peptide / apo / none)**
- Backbones: **(fill from spec.yaml)**
- Seeds per backbone: **(fill from spec.yaml)**
- Pre-check status expected: **pass** (or list specific `warn_*` if intentional)

## Runs

Each addition to the experiment has its own subdirectory under `runs/`.
Naming: `runs/<addition_slug>/` (e.g. `runs/initial/`, `runs/more_seeds/`,
`runs/designed_peptide_variants/`).

- `runs/initial/` — the initial submission

## Status

- Spawned: {utc}
- Predictions completed: 0
- Rows scored: 0
- Findings written: no

## Related work

<!-- Link to prior findings, related v3.7 rows, or design docs -->
""")


_FASTA_STUB = "" # empty file — rescore_experiment overwrites with a real
                  # FASTA when the spec declares a peptide ligand


# =============================================================================
# Scaffolder
# =============================================================================


TEMPLATE_DIR_NAME = "000_template"


def scaffold(slug: str, spec_content: str,
             experiments_root: Path = EXPERIMENTS_ROOT,
             force: bool = False,
             utc: str | None = None) -> Path:
    """Create the ``experiments/<slug>/`` folder tree from ``000_template/``.

    Canonical shape (matches 018_block_a_switch_test after 2026-09-01 reorg):
      <slug>/
        README.md            (from template, {{SLUG}} substituted)
        spec.yaml            (from spec_content)
        manifest/            (empty)
        analysis/
          wave_verification/, per_class/, notebooks/, figures/  (empty)
        ligand_sequence.fasta  (empty; rescore fills for peptide ligands)

    If the 000_template directory is missing, falls back to the legacy
    inline scaffolding (kept for offline / installed-package callers).

    Returns the absolute path to the experiment directory.
    Raises FileExistsError when the folder already exists and force=False.
    """
    slug = validate_slug(slug)
    exp_dir = experiments_root / slug
    if exp_dir.exists():
        if not force:
            raise FileExistsError(
                f"experiment folder {exp_dir} already exists. Use --force "
                f"to overwrite (destructive), or extend the experiment by "
                f"editing spec.yaml and running rescore again."
            )
        shutil.rmtree(exp_dir)

    if utc is None:
        import datetime as _dt
        utc = _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    template_dir = experiments_root / TEMPLATE_DIR_NAME
    if template_dir.is_dir():
        # Canonical scaffold from 000_template/. Skip .gitkeep placeholders;
        # substitute {{SLUG}} in .template files and strip the extension.
        exp_dir.mkdir(parents=True)
        for src in template_dir.rglob("*"):
            rel = src.relative_to(template_dir)
            dst = exp_dir / rel
            if src.is_dir():
                dst.mkdir(parents=True, exist_ok=True)
                continue
            if src.name == ".gitkeep":
                dst.parent.mkdir(parents=True, exist_ok=True)
                continue    # skip; the dir got created above
            if src.suffix == ".template":
                text = src.read_text().replace("{{SLUG}}", slug)
                dst_final = dst.with_suffix("")   # drop .template
                dst_final.parent.mkdir(parents=True, exist_ok=True)
                dst_final.write_text(text)
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(src.read_bytes())
        # Overlay spec + ligand fasta from caller-supplied content.
        (exp_dir / "spec.yaml").write_text(spec_content)
        (exp_dir / "ligand_sequence.fasta").write_text(_FASTA_STUB)
        # README template used {{SLUG}} + <utc>; substitute both.
        readme_p = exp_dir / "README.md"
        if readme_p.exists():
            readme_p.write_text(
                readme_p.read_text()
                    .replace("{{SLUG}}", slug)
                    .replace("<utc>", utc)
            )
    else:
        # Fallback (legacy): inline scaffold.
        exp_dir.mkdir(parents=True)
        (exp_dir / "manifest").mkdir()
        (exp_dir / "analysis").mkdir()
        (exp_dir / "analysis" / "wave_verification").mkdir()
        (exp_dir / "analysis" / "per_class").mkdir()
        (exp_dir / "analysis" / "notebooks").mkdir()
        (exp_dir / "analysis" / "figures").mkdir()
        (exp_dir / "spec.yaml").write_text(spec_content)
        (exp_dir / "README.md").write_text(_README_TEMPLATE.format(slug=slug, utc=utc))
        (exp_dir / "ligand_sequence.fasta").write_text(_FASTA_STUB)

    return exp_dir


# =============================================================================
# CLI
# =============================================================================


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="gpcr-experiment",
        description="Scaffold a new experiment folder under "
                    "experiments/NNN_<biology_slug>/.",
    )
    p.add_argument("--slug", required=True,
                   help="biology-descriptive slug for the experiment. If it "
                        "already carries a `NNN_` prefix it's used verbatim; "
                        "otherwise the script auto-increments (walks "
                        "existing experiments/NNN_* and picks max+1).")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--spec", type=Path,
                     help="path to the gpcr-propose YAML spec")
    src.add_argument("--spec-inline",
                     help="the YAML spec as a literal string")
    p.add_argument("--experiments-root", type=Path, default=EXPERIMENTS_ROOT,
                   help=f"root directory for experiments (default: {EXPERIMENTS_ROOT})")
    p.add_argument("--force", action="store_true",
                   help="destructively overwrite an existing experiment folder")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.spec is not None:
        if not args.spec.exists():
            print(f"gpcr-experiment: spec file not found: {args.spec}",
                  file=sys.stderr)
            return 2
        spec_content = args.spec.read_text()
    else:
        spec_content = args.spec_inline

    # Auto-prepend NNN_ if the analyst supplied a bare biology slug.
    slug = compose_slug(args.slug, experiments_root=args.experiments_root)

    try:
        exp_dir = scaffold(slug, spec_content,
                           experiments_root=args.experiments_root,
                           force=args.force)
    except (SlugError, FileExistsError) as e:
        print(f"gpcr-experiment: {e}", file=sys.stderr)
        return 2

    print(f"scaffolded {exp_dir}")
    print()
    print("Next steps for the subagent:")
    print(f"  1. Review experiments/{slug}/spec.yaml")
    print(f"  2. Run: python3 -m scorer.propose --spec experiments/{slug}/spec.yaml \\")
    print(f"         --out experiments/{slug}/manifest/manifest.csv \\")
    print(f"         --output-root /hpc/scratch/sengaad1/paper_af3/experiments")
    print(f"  3. Dispatch via supervisor on HPC")
    print(f"  4. When done: scripts/rescore_experiment.py --slug {slug}")
    print(f"     (writes analysis/rows.csv + rows.provenance.json)")
    print(f"  5. Regenerate MASTER: scripts/build_experiments_master.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
