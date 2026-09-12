"""Verify the cognate arm carries the correct primary Gα per coupling table.

For every row in the Block A manifest where the request_id indicates the
cognate arm, load the materialised input file (Boltz YAML / Protenix JSON /
OpenFold-3 JSON / Chai FASTA), extract the second protein chain's sequence,
and compare against the expected primary_ga_identity for that receptor
from refs/gpcr_coupling.csv (mapped through
docs/EXPERIMENT_CATALOG/sequences/partners.fasta).

Guards against the founding W54 taxonomy failure: a blanket alphas partner
applied to all 40 receptors regardless of documented primary G-protein
coupling. Fails LOUD on any mismatch.

Usage:
    python3 scripts/verify_cognate_identity.py \\
        --manifest experiments/018_block_a_switch_test/runs/initial/manifest.csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
COUPLING_CSV = REPO / "refs" / "gpcr_coupling.csv"
PARTNERS_FASTA = REPO / "docs" / "EXPERIMENT_CATALOG" / "sequences" / "partners.fasta"


def parse_fasta(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    header: str | None = None
    chunks: list[str] = []
    for line in path.read_text().splitlines():
        if not line:
            continue
        if line.startswith(">"):
            if header:
                out[header] = "".join(chunks)
            header = line[1:].split("|", 1)[0].strip()
            chunks = []
        else:
            chunks.append(line.strip())
    if header:
        out[header] = "".join(chunks)
    return out


def extract_partner_seq(input_path: Path, backbone: str) -> str:
    """Return the second protein chain's sequence from a materialised input."""
    text = input_path.read_text()
    if backbone == "boltz":
        # boltz YAML:
        #   sequences:
        #     - protein: {id: A, sequence: <receptor>}
        #     - protein: {id: B, sequence: <partner>}
        import yaml
        data = yaml.safe_load(text)
        prots = [s["protein"] for s in data["sequences"] if "protein" in s]
        return prots[1]["sequence"].strip()
    if backbone == "of3":
        # OF3 JSON:
        #   {"queries": {"<key>": {"chains": [{sequence}, {sequence}, ...]}}}
        data = json.loads(text)
        query = next(iter(data["queries"].values()))
        chains = [c for c in query["chains"] if c.get("sequence")]
        return chains[1]["sequence"].strip()
    if backbone == "protenix":
        # Protenix JSON:
        #   [{"sequences": [{"proteinChain": {"sequence": ...}}, ...]}]
        data = json.loads(text)
        entries = data[0]["sequences"] if isinstance(data, list) else data["sequences"]
        seqs: list[str] = []
        for entry in entries:
            block = entry.get("proteinChain") or entry.get("protein")
            if isinstance(block, dict) and block.get("sequence"):
                seqs.append(block["sequence"].strip())
        return seqs[1]
    if backbone == "chai":
        # Chai FASTA — two records, second is the partner.
        headers: list[str] = []
        chunks: list[list[str]] = []
        for line in text.splitlines():
            if line.startswith(">"):
                headers.append(line[1:].strip())
                chunks.append([])
            elif chunks:
                chunks[-1].append(line.strip())
        return "".join(chunks[1])
    raise ValueError(f"Unknown backbone {backbone}")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", type=Path, required=True)
    args = p.parse_args(argv)

    coupling: dict[str, str] = {}
    with COUPLING_CSV.open() as f:
        for r in csv.DictReader(f):
            coupling[r["receptor_slug"].strip().upper()] = r["primary_ga_identity"].strip()

    partners = parse_fasta(PARTNERS_FASTA)

    rows = list(csv.DictReader(args.manifest.open()))
    cognate_rows = [r for r in rows if "_cognate_" in r["request_id"]]
    print(f"Loaded {len(rows)} manifest rows ({len(cognate_rows)} cognate).")

    # Deduplicate by (receptor, backbone) — seeds share the input file across
    # backbones that write per-seed files; we check one per (rec, bb) plus one
    # random sample from each rec across backbones would be fine, but with
    # ~160 unique (rec, bb) pairs it is cheap to check them all.
    seen: set[tuple[str, str]] = set()
    checks: list[dict] = []
    for r in cognate_rows:
        rec = r["receptor_from_path_substring"].upper()
        bb = r["backbone"]
        key = (rec, bb, r["input_path"])
        if key in seen:
            continue
        seen.add(key)
        checks.append(r)

    per_receptor_pass: dict[str, int] = {}
    per_receptor_fail: dict[str, int] = {}
    fail_examples: list[tuple[str, str, str, str]] = []

    for r in checks:
        rec = r["receptor_from_path_substring"].upper()
        bb = r["backbone"]
        exp_identity = coupling[rec]
        exp_seq = partners[exp_identity]
        got_seq = extract_partner_seq(Path(r["input_path"]), bb)
        if got_seq == exp_seq:
            per_receptor_pass[rec] = per_receptor_pass.get(rec, 0) + 1
        else:
            per_receptor_fail[rec] = per_receptor_fail.get(rec, 0) + 1
            fail_examples.append((rec, bb, exp_identity, r["input_path"]))

    print()
    print(f"Files checked: {len(checks)}")
    n_pass = sum(per_receptor_pass.values())
    n_fail = sum(per_receptor_fail.values())
    print(f"  pass: {n_pass}   fail: {n_fail}")

    all_receptors = sorted(set(per_receptor_pass) | set(per_receptor_fail))
    print()
    print("Per-receptor pass/fail (across 4 backbones):")
    for rec in all_receptors:
        n_p = per_receptor_pass.get(rec, 0)
        n_f = per_receptor_fail.get(rec, 0)
        status = "PASS" if n_f == 0 else "FAIL"
        print(f"  {rec:<10} {status}  pass={n_p} fail={n_f}  primary={coupling[rec]}")

    if fail_examples:
        print()
        print("Fail examples:")
        for rec, bb, exp, path in fail_examples[:10]:
            print(f"  {rec} {bb} expected={exp}  path={path}")
        print(f"\nFAIL: {n_fail} rows carry the wrong partner sequence.")
        return 1

    n_uniq_rec = len(all_receptors)
    print()
    print(f"{n_uniq_rec}/40 cognate rows carry correct primary Gα per coupling table.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
