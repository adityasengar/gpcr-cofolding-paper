"""BW numbering derivation via GPCRdb residues/extended, per-PDB, always.

Verbatim port from github.com/adityasengar/gpcr-structure-pipeline
(gpcr_pipeline.py lines 39-42, 70-125, 325-330, 337-353, 356-365).

Design intent — see docs/AUDIT_TRAIL.md and docs/BW_SOURCE.md:

- No hardcoded BW anchor tables.
- No canonical offsets (audit #1 offset-137).
- No panel-FASTA realignment shortcut (audit #5 silent-drop past 7.53).
- One and only one BW source per input.

Endpoints hit (all HTTPS, no auth):

- GPCRdb protein-by-accession          https://gpcrdb.org/services/protein/accession/<acc>/
- GPCRdb extended residues (BW ground truth) https://gpcrdb.org/services/residues/extended/<entry>/
- SIFTS UniProt segments                https://www.ebi.ac.uk/pdbe/api/mappings/uniprot_segments/<pdb>

Cache is filename-based, keyed on the natural key of the resource
(entry_name / accession / pdb_id), NOT on a caller path — the same
identity that guards ScorerRow (see scorer/cache.py).
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import requests


GPCRDB = "https://gpcrdb.org"
SIFTS_URL = "https://www.ebi.ac.uk/pdbe/api/mappings/uniprot_segments/{pdb}"


class Api:
    """requests session with retries, throttling and on-disk JSON cache.

    Ported verbatim from gpcr_pipeline.py:70-125.
    """

    def __init__(self, cache_dir: Path, delay: float = 0.15):
        self.cache = Path(cache_dir)
        self.cache.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.sess = requests.Session()
        self.sess.headers["User-Agent"] = "gpcr-state-scorer/0.1 (paper_af3)"

    def get_json(self, url: str, cache_key: str | None = None, ok404: bool = False) -> Any:
        if cache_key:
            f = self.cache / (cache_key + ".json")
            if f.exists():
                return json.loads(f.read_text())
        data = self._get(url, ok404=ok404)
        if data is None:
            parsed = None
        else:
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                parsed = None  # HTML error page etc.
        if cache_key:
            f = self.cache / (cache_key + ".json")
            f.write_text(json.dumps(parsed))
        return parsed

    def get_bytes(self, url: str, cache_key: str | None = None, ok404: bool = False) -> bytes | None:
        if cache_key:
            f = self.cache / cache_key
            if f.exists():
                return f.read_bytes()
        data = self._get(url, ok404=ok404)
        if cache_key and data is not None:
            (self.cache / cache_key).write_bytes(data)
        return data

    def _get(self, url: str, ok404: bool = False) -> bytes | None:
        for attempt in range(4):
            try:
                time.sleep(self.delay)
                r = self.sess.get(
                    url, timeout=300,
                    headers={"Accept": "application/json"},
                )
                if r.status_code == 404 or (ok404 and r.status_code >= 400):
                    return None
                r.raise_for_status()
                return r.content
            except (requests.RequestException, OSError) as e:
                if attempt == 3:
                    if ok404:
                        return None
                    raise
                wait = 2 ** attempt
                time.sleep(wait)
        return None  # unreachable but keeps type checkers quiet


def load_sifts(api: Api, pdb: str) -> dict[str, Any]:
    """SIFTS UniProt-segment mapping for `pdb` (lower-cased on request).

    Returns ``data[pdb_lower]["UniProt"]`` — a dict keyed by UniProt
    accession — or empty dict if SIFTS has no record.

    Ported verbatim from gpcr_pipeline.py:325-330.
    """
    data = api.get_json(
        SIFTS_URL.format(pdb=pdb.lower()),
        cache_key=f"sifts_{pdb.lower()}",
        ok404=True,
    )
    if not data:
        return {}
    return data.get(pdb.lower(), {}).get("UniProt", {})


def get_generic_numbers(api: Api, entry: str) -> dict[int, dict[str, str]]:
    """GPCRdb residues/extended → {uniprot_pos: {aa, segment, generic (3x50), bw (3.50)}}.

    THIS IS THE ONLY SANCTIONED BW SOURCE (see docs/BW_SOURCE.md).

    ``display_generic_number`` is a string like ``"3.50x50"``. Split on the
    ``"x"``:
       - the BW label is the prefix before the ``"x"`` (``"3.50"``)
       - the GPCRdb generic is the class-digit + ``"x"`` + suffix
         (``"3x50"``)

    Ported verbatim from gpcr_pipeline.py:337-353.
    """
    data = api.get_json(
        f"{GPCRDB}/services/residues/extended/{entry}/",
        cache_key=f"residues_ext_{entry}",
        ok404=True,
    )
    out: dict[int, dict[str, str]] = {}
    for r in data or []:
        dgn = r.get("display_generic_number") or ""
        bw = gn = ""
        if "x" in dgn:
            pre, suf = dgn.split("x", 1)
            bw = pre
            gn = pre.split(".")[0] + "x" + suf
        out[r["sequence_number"]] = {
            "aa": r.get("amino_acid"),
            "segment": r.get("protein_segment"),
            "generic": gn,
            "bw": bw,
        }
    return out


def gpcr_entry_for_accession(api: Api, acc: str) -> str | None:
    """UniProt accession → GPCRdb entry_name, or None if not a receptor.

    GPCRdb also serves G-proteins and arrestins from this endpoint; only
    receptor-family records (``family`` slug starts with a class digit)
    are accepted.

    Ported verbatim from gpcr_pipeline.py:356-365.
    """
    data = api.get_json(
        f"{GPCRDB}/services/protein/accession/{acc}/",
        cache_key=f"protein_acc_{acc}",
        ok404=True,
    )
    entry = (data or {}).get("entry_name")
    fam = str((data or {}).get("family") or "")
    return entry if entry and fam[:1].isdigit() else None


def lookup_bw(bw_map: dict[int, dict[str, str]], bw_label: str) -> tuple[int, str] | None:
    """Return ``(uniprot_pos, aa_expected)`` for a BW label like ``"3.50"``.

    Ground-truth test: for entry ``opsd_bovin``, ``lookup_bw(bw_map, "3.50")``
    returns ``(135, "R")``; for ``adrb2_human``, ``"6.50"`` returns
    ``(288, "P")``. These are the two regression fixtures from
    gpcr-structure-pipeline/run_tests.py:158-166.
    """
    for pos, info in bw_map.items():
        if info.get("bw") == bw_label:
            return int(pos), (info.get("aa") or "")
    return None
