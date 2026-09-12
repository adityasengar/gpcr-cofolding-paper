"""Deterministic GPCR conformational-state scorer.

Public surface (populated across commits 2–13):

    from scorer import run_scorer, ScorerRow
    from scorer.assertions import (
        A1AminoAcidIdentity, A2FASTATrunc, A3WrongChain,
        A4ReferenceClassMismatch, A5SpeciesMismatch, A6ReceptorIdentity,
    )

The scorer git SHA is baked at import time. A dirty tree suffixes '-dirty'
onto ``__version__`` and downstream figure emission refuses to proceed.
"""
import subprocess as _sp
from pathlib import Path as _Path

__all__ = ["__version__", "run_scorer", "ScorerRow"]


def _git_sha() -> str:
    """Return the full 40-char lowercase-hex commit SHA of the scorer
    checkout, or 'no-git' if that cannot be determined. If the working
    tree is dirty, the SHA is suffixed with '-dirty' — which will fail
    the step7 dispatch-gate 40-char-hex assertion by construction.
    Dispatch from a dirty tree is intentionally blocked.
    """
    # First choice: shell out to git. Works in a dev checkout where the
    # .git directory is on disk.
    try:
        root = _Path(__file__).resolve().parent.parent
        sha = _sp.run(
            ["git", "-C", str(root), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=5,
        )
        if sha.returncode == 0:
            head = sha.stdout.strip()  # full 40-char SHA
            dirty = _sp.run(
                ["git", "-C", str(root), "status", "--porcelain"],
                capture_output=True, text=True, timeout=5,
            )
            if dirty.stdout.strip():
                return f"{head}-dirty"
            return head
    except Exception:
        pass

    # Fallback: read the SHA that setup.py stamped at build time. This
    # is the pip-installed-venv path — the HPC scorer install has no
    # .git on disk, so the subprocess above fails and every provenance
    # row records 'no-git' (audit finding #1). setup.py writes
    # scorer/_version_sha.py at build time; if that module exists,
    # trust its SHA.
    try:
        from scorer import _version_sha  # type: ignore[import-not-found]
        return getattr(_version_sha, "SHA", "no-git")
    except Exception:
        return "no-git"


__version__ = f"0.1.0+{_git_sha()}"


def __getattr__(name):
    # Lazy imports to keep import-time light and side-effect-free.
    if name == "run_scorer":
        from scorer.orchestrator import run_scorer
        return run_scorer
    if name == "ScorerRow":
        from scorer.schema import ScorerRow
        return ScorerRow
    raise AttributeError(name)
