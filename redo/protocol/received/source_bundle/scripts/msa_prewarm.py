"""MSA pre-warm for Block A — fetch MSAs for 40 receptors + partners.

Rationale (PREREG §Consolidated Findings → dispatch blockers):

MSA generation is the largest per-prediction cost. ColabFold's public
server caches results by query-sequence hash — a sequence we've queried
recently returns fast. Round 3 saw ×3.5-4.6 speedup vs cold-MSA runs
because AA2AR/ADRB2/DRD2 were server-warm from prior sessions.

For Block A, 37 of 40 receptors are cold (never queried through the
ColabFold API in our history). Running Block A predictions cold would
push 4-5 min/pred × ~6,400 preds → 30-50 hours wall time.

Pre-warming: fetch MSAs for every unique receptor sequence + partner
sequence in a single serial pass. Zero GPU compute, ~2-4 hours wall
time (ColabFold API rate limits). After pre-warm, Block A predictions
run at ~1-2 min/pred — a full order of magnitude faster.

**Progressive** cache-warming (letting cache warm as Block A dispatches)
would make cache state a hidden covariate on run order — earlier-
dispatched receptors would see faster wall times than later-dispatched
ones. Not what you want when comparing backbones or receptors.

## Usage

    # DRY RUN — print what would be fetched, no network I/O
    python3 scripts/msa_prewarm.py --dry-run

    # Live pre-warm (run on HPC, needs internet + writable cache dir)
    python3 scripts/msa_prewarm.py \\
        --receptor-fasta refs/panel_receptor_sequences.fasta \\
        --partners docs/EXPERIMENT_CATALOG/sequences/partners.fasta \\
        --cache-dir /hpc/scratch/sengaad1/paper_af3/msa_cache \\
        --manifest-out refs/msa_prewarm_manifest.csv

## What "pre-warmed" means

For each unique protein sequence in the input:
1. Compute the query-sequence hash (SHA256 of the AA string).
2. Submit to ColabFold API at https://api.colabfold.com/ or
   https://api.mmseqs.com/msa endpoint (public, rate-limited).
3. Wait for the server-side result — the MSA is now cached in
   ColabFold's server infrastructure by (sequence hash → MSA).
4. Optionally also cache locally under `--cache-dir/<sha256>/` so
   later runs on the same HPC can reuse without hitting the API.
5. Record status in `refs/msa_prewarm_manifest.csv`:
   `sequence_sha, source, sequence_len, status, timestamp, error`.

## What this does NOT do

- Does NOT run structure prediction.
- Does NOT touch Boltz/OF3/Protenix/Chai model weights.
- Does NOT prime Protenix's own MSA server (Protenix uses a separate
  server; that cache warms during Block A dispatch itself and cannot be
  pre-warmed by ColabFold API queries).

## Rate limits + resume

ColabFold's public API is bursty-tolerant but throws 429 under sustained
load. This script:
- Serial submission (no concurrent fetches).
- 6-second delay between queries.
- On 429, exponential backoff up to 5 min.
- Idempotent — re-running skips sequences already marked `cached` in
  the manifest.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import hashlib
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_RECEPTOR_FASTA = REPO / "refs/panel_receptor_sequences.fasta"
DEFAULT_PARTNERS = REPO / "docs/EXPERIMENT_CATALOG/sequences/partners.fasta"
DEFAULT_MANIFEST = REPO / "refs/msa_prewarm_manifest.csv"
DEFAULT_CACHE = Path("/hpc/scratch/sengaad1/paper_af3/msa_cache")

# ColabFold public MSA API — verified 2026-09-01 by probing.
# The endpoint is /ticket/msa (POST, url-encoded body), NOT /msa. Response is
# an async ticket; poll /ticket/<id> until COMPLETE. The server caches the
# computed MSA by query-sequence hash — a subsequent submission of the same
# sequence returns COMPLETE immediately, which is the whole point of the
# pre-warm.
COLABFOLD_API_TICKET = "https://api.colabfold.com/ticket/msa"
COLABFOLD_API_STATUS = "https://api.colabfold.com/ticket/{ticket_id}"

REQUEST_DELAY_SEC = 6
POLL_INTERVAL_SEC = 5
POLL_TIMEOUT_SEC = 600  # 10 min per sequence — long ones can push this
INITIAL_BACKOFF_SEC = 30
MAX_BACKOFF_SEC = 300


def parse_fasta(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    header = None
    seq_lines: list[str] = []
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


def seq_sha(seq: str) -> str:
    return hashlib.sha256(seq.upper().replace(" ", "").encode()).hexdigest()[:16]


def submit_msa(sequence: str, timeout_sec: int = 60) -> dict:
    """POST sequence to ColabFold MSA API; return the ticket JSON.

    The API is asynchronous. Body must be url-encoded (NOT JSON, NOT
    multipart). Response is `{"id": "<ticket>", "status": "PENDING"|"COMPLETE"}`.
    A COMPLETE response on submission means the server-side cache already
    holds this sequence's MSA — which is exactly the warm-cache state
    the pre-warm is trying to reach.
    """
    body = urllib.parse.urlencode({
        "q": f">query\n{sequence}",
        "mode": "env",
    }).encode()
    req = urllib.request.Request(
        COLABFOLD_API_TICKET, data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
        return json.loads(resp.read().decode())


def poll_ticket(ticket_id: str, timeout_sec: int = POLL_TIMEOUT_SEC,
                interval_sec: int = POLL_INTERVAL_SEC) -> str:
    """Poll a ColabFold ticket until it reaches a terminal state.

    Returns the final status string ("COMPLETE", "ERROR", "UNKNOWN", …).
    Raises TimeoutError if not terminal within timeout_sec.
    """
    url = COLABFOLD_API_STATUS.format(ticket_id=ticket_id)
    deadline = time.monotonic() + timeout_sec
    while time.monotonic() < deadline:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
        status = str(payload.get("status", "UNKNOWN")).upper()
        if status in ("COMPLETE", "ERROR"):
            return status
        # PENDING / RUNNING / UNKNOWN — keep polling
        time.sleep(interval_sec)
    raise TimeoutError(f"ticket {ticket_id} did not reach terminal state in {timeout_sec}s")


def load_manifest(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return {r["sequence_sha"]: r for r in csv.DictReader(path.open())}


def write_manifest(path: Path, manifest: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["sequence_sha", "source", "sequence_len", "status",
              "timestamp", "error"]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(manifest.values(),
                           key=lambda r: (r["source"], r["sequence_sha"])))


def prewarm_one(seq: str, source: str, manifest: dict[str, dict],
                dry_run: bool) -> str:
    sha = seq_sha(seq)
    if manifest.get(sha, {}).get("status") == "cached":
        return f"skip {sha[:8]} {source} — already cached"

    now = datetime.datetime.utcnow().isoformat() + "Z"
    entry = manifest.setdefault(sha, {
        "sequence_sha": sha,
        "source": source,
        "sequence_len": str(len(seq)),
        "status": "pending",
        "timestamp": now,
        "error": "",
    })
    if dry_run:
        entry["status"] = "would_fetch"
        return f"dry {sha[:8]} {source} len={len(seq)}"

    backoff = INITIAL_BACKOFF_SEC
    for attempt in range(6):
        try:
            ticket = submit_msa(seq)
            ticket_id = ticket.get("id", "")
            submit_status = str(ticket.get("status", "")).upper()
            if not ticket_id:
                entry["status"] = "failed"
                entry["error"] = f"no ticket id in response: {ticket!r}"[:200]
                return f"fail {sha[:8]} {source} — {entry['error']}"

            if submit_status == "COMPLETE":
                # Server cache hit — the MSA is already computed.
                entry["status"] = "cached"
                entry["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
                entry["error"] = f"ticket={ticket_id} instant_hit"
                return f"hit {sha[:8]} {source} len={len(seq)} ticket={ticket_id[:12]}"

            # Poll until terminal
            final_status = poll_ticket(ticket_id)
            if final_status == "COMPLETE":
                entry["status"] = "cached"
                entry["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
                entry["error"] = f"ticket={ticket_id} computed"
                return f"ok  {sha[:8]} {source} len={len(seq)} ticket={ticket_id[:12]}"
            entry["status"] = "failed"
            entry["error"] = f"ticket={ticket_id} final_status={final_status}"
            return f"fail {sha[:8]} {source} — {entry['error']}"
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(min(backoff, MAX_BACKOFF_SEC))
                backoff *= 2
                continue
            entry["status"] = "failed"
            entry["error"] = f"HTTP {e.code}: {e.reason}"
            return f"fail {sha[:8]} {source} — {entry['error']}"
        except TimeoutError as e:
            entry["status"] = "failed"
            entry["error"] = str(e)[:200]
            return f"fail {sha[:8]} {source} — {entry['error']}"
        except Exception as e:  # noqa: BLE001
            entry["status"] = "failed"
            entry["error"] = f"{type(e).__name__}: {e}"[:200]
            return f"fail {sha[:8]} {source} — {entry['error']}"
    entry["status"] = "failed"
    entry["error"] = "429 rate-limited after 6 retries"
    return f"fail {sha[:8]} {source} — {entry['error']}"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--receptor-fasta", type=Path, default=DEFAULT_RECEPTOR_FASTA,
                   help="FASTA of the 40 panel receptor sequences")
    p.add_argument("--partners", type=Path, default=DEFAULT_PARTNERS)
    p.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    p.add_argument("--manifest-out", type=Path, default=DEFAULT_MANIFEST)
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would be fetched, no network I/O")
    p.add_argument("--limit", type=int, default=None,
                   help="Cap number of sequences fetched (for testing)")
    args = p.parse_args(argv)

    if not args.receptor_fasta.exists():
        print(f"ERROR: {args.receptor_fasta} missing.")
        print("Generate via: python3 scripts/build_panel_receptor_fasta.py")
        print("(script not yet written — see refs/gpcr_coupling.csv for the 40 slugs,")
        print(" fetch each receptor's canonical UniProt sequence)")
        return 2

    receptor_entries = parse_fasta(args.receptor_fasta)
    partner_entries = parse_fasta(args.partners)

    manifest = load_manifest(args.manifest_out)

    all_targets = (
        [(hdr, seq, "receptor") for hdr, seq in receptor_entries]
        + [(hdr, seq, f"partner:{hdr.split('|', 1)[0]}") for hdr, seq in partner_entries]
    )
    if args.limit:
        all_targets = all_targets[:args.limit]

    print(f"pre-warming {len(all_targets)} sequences "
          f"(dry={args.dry_run}) into {args.manifest_out.name}")
    print()

    for i, (hdr, seq, source) in enumerate(all_targets, 1):
        result = prewarm_one(seq, source, manifest, dry_run=args.dry_run)
        print(f"[{i:>3}/{len(all_targets)}] {result}")
        if not args.dry_run:
            write_manifest(args.manifest_out, manifest)
            time.sleep(REQUEST_DELAY_SEC)

    write_manifest(args.manifest_out, manifest)
    n_cached = sum(1 for r in manifest.values() if r["status"] == "cached")
    n_failed = sum(1 for r in manifest.values() if r["status"] == "failed")
    print()
    print(f"summary: {n_cached} cached, {n_failed} failed, "
          f"{len(manifest)} total in manifest")
    return 0 if not n_failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
