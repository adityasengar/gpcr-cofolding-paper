"""Content-hash keyed on-disk cache.

Design intent (see docs/AUDIT_TRAIL.md, artefact #6): cache keys are the
sha256 of file bytes, never derived from the directory in which the file
sits. Directory components, receptor slugs, and experiment identifiers are
banned from key construction by ci/lint_anti_patterns.sh — see
docs/TRACKING.md for the rationale.

Pattern is lifted from w56_0c_crystal_calibration.py:37-38, the only
correct on-disk cache in the frozen codebase.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Callable


CHUNK_SIZE = 1 << 20  # 1 MiB streaming reads for large PDBs / CIFs


def content_sha256(path: os.PathLike[str] | str) -> str:
    """Streaming sha256 hex-digest of file bytes.

    Never reads the file into memory in one go; safe for large mmCIFs.
    Raises FileNotFoundError if the file is absent (do not swallow: the
    caller is claiming this file backs a scored row — its absence must
    surface).
    """
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
            h.update(chunk)
    return h.hexdigest()


def _sha256_bytes(data: bytes | str) -> str:
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def cache_key(
    input_path: os.PathLike[str] | str,
    output_dir: os.PathLike[str] | str,
    bw_source_sha: str,
) -> str:
    """Canonical cache key for a scored row.

    key = sha256(
        content_sha256(input_bytes)   # exact file content — identity
        || "::"
        || sha256(absolute(output_dir))  # namespace by output root, not by
                                         # any *component* of the input path
        || "::"
        || bw_source_sha                 # GPCRdb residues/extended payload sha
    )

    Two different files sharing a filename under a shared parent produce
    different keys because content_sha256 differs. Two runs of the same
    input into different output roots produce different keys because the
    output_dir namespace differs. The parent directory of the *input* is
    never touched.

    Callers must supply an absolute output_dir; the function does not
    ``resolve()`` it (that would let a symlink swap change the key).
    """
    input_sha = content_sha256(input_path)
    out_abs = str(Path(output_dir))
    if not out_abs.startswith("/"):
        raise ValueError(
            f"output_dir must be absolute, got {out_abs!r} — see docs/AUDIT_TRAIL.md#6"
        )
    namespace_sha = _sha256_bytes(out_abs)
    composite = f"{input_sha}::{namespace_sha}::{bw_source_sha}"
    return _sha256_bytes(composite)


class JsonCache:
    """Tiny on-disk JSON cache under a caller-supplied directory.

    Keys must be hex strings from ``cache_key()`` or ``content_sha256()``
    — the ``_validate_key`` check refuses anything else so a stray call
    like ``cache.get(path.name)`` fails loudly.
    """

    _HEX = set("0123456789abcdef")

    def __init__(self, cache_dir: os.PathLike[str] | str):
        self.dir = Path(cache_dir)
        self.dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _validate_key(cls, key: str) -> None:
        if len(key) != 64 or any(c not in cls._HEX for c in key):
            raise ValueError(
                f"cache key must be a 64-char sha256 hex digest, got {key!r}"
            )

    def _path(self, key: str) -> Path:
        self._validate_key(key)
        return self.dir / (key + ".json")

    def get(self, key: str) -> Any | None:
        p = self._path(key)
        if p.exists():
            return json.loads(p.read_text())
        return None

    def put(self, key: str, value: Any) -> None:
        p = self._path(key)
        p.write_text(json.dumps(value, indent=2, sort_keys=False))

    def get_or_compute(self, key: str, factory: Callable[[], Any]) -> Any:
        cached = self.get(key)
        if cached is not None:
            return cached
        value = factory()
        self.put(key, value)
        return value


def sha256_json(payload: Any) -> str:
    """SHA256 of a canonical JSON encoding — used for `gpcrdb_residues_ext_sha256`
    on every ScorerRow."""
    return _sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")))
