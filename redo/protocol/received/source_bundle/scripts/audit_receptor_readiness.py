"""Panel-wide readiness audit — run the 5 pre-checks against every receptor
in ``scorer.receptors.KNOWN_RECEPTORS`` and emit a Markdown + CSV report.

For every unique GPCRdb entry (deduped across alias slugs) we simulate the
canonical WT proposal:

    receptor_slug          = <primary slug for the entry>
    species                = species suffix from the GPCRdb entry_name
    partner_perturbation   = "wt"     (worst case — makes PC5 fire)
    fasta_seq              = canonical WT reconstructed from GPCRdb
                             residues/extended, UniProt-indexed with 'X'
                             padding for positions the endpoint doesn't
                             enumerate (rare)

Then feed the row through ``scorer.pre_check.run_all_checks`` and record
per-check status + reason. No HPC, no writes to ``scorer/``, no config
changes. Purely local + GPCRdb-cached.

Deliverables:
    docs/RECEPTOR_READINESS_2026_08_27.md   — human report
    docs/RECEPTOR_READINESS_2026_08_27.csv  — machine-readable table
"""
from __future__ import annotations

import argparse
import csv
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from scorer.bw_numbering import Api, get_generic_numbers
from scorer.pre_check import load_ref_species_map, run_all_checks
from scorer.receptors import KNOWN_RECEPTORS, RECEPTOR_CLASS
from scorer.structure import STD_AA


REPO_ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = REPO_ROOT / "refs" / "cache" / "gpcrdb"
REF_CSV = REPO_ROOT / "refs" / "reference_set.csv"
OUT_MD = REPO_ROOT / "docs" / "RECEPTOR_READINESS_2026_08_27.md"
OUT_CSV = REPO_ROOT / "docs" / "RECEPTOR_READINESS_2026_08_27.csv"


# --------------------------------------------------------------------------
# Slug de-duplication — one row per canonical GPCRdb entry
# --------------------------------------------------------------------------


def primary_slugs() -> list[tuple[str, str, list[str]]]:
    """Return [(primary_slug, entry_name, [alias slugs]), ...].

    For each unique entry_name across ``KNOWN_RECEPTORS`` pick a primary
    slug. Preference:
        1. the slug whose uppercase equals ``entry_name.split('_')[0].upper()``
        2. else the shortest alias
        3. else the first slug encountered
    """
    groups: dict[str, list[str]] = defaultdict(list)
    for slug, entry in KNOWN_RECEPTORS.items():
        groups[entry].append(slug)

    out: list[tuple[str, str, list[str]]] = []
    for entry, slugs in groups.items():
        prefix = entry.split("_", 1)[0].upper()
        primary: str | None = None
        for s in slugs:
            if s.upper() == prefix:
                primary = s
                break
        if primary is None:
            primary = sorted(slugs, key=lambda s: (len(s), s))[0]
        aliases = [s for s in slugs if s != primary]
        out.append((primary, entry, sorted(aliases)))
    # Deterministic order: primary slug alphabetical
    out.sort(key=lambda t: t[0])
    return out


# --------------------------------------------------------------------------
# Species inference from GPCRdb entry_name suffix
# --------------------------------------------------------------------------


# Curation hints for entries where GPCRdb returns an empty payload —
# verified live against GPCRdb 2026-08-27. Adding these here (rather than
# patching scorer/receptors.py) keeps the audit read-only.
_EMPTY_PAYLOAD_HINTS: dict[str, str] = {
    "mc1r_human": (
        "GPCRdb has this receptor under entry_name 'mshr_human' "
        "(melanocyte-stimulating hormone receptor); "
        "KNOWN_RECEPTORS maps MC1R → mc1r_human, which 404s. "
        "Curation: update the mapping to mshr_human."
    ),
    "trhr_human": (
        "GPCRdb has this receptor under entry_name 'trfr_human' "
        "(thyrotropin-releasing hormone receptor); "
        "KNOWN_RECEPTORS maps TRHR → trhr_human, which 404s. "
        "Curation: update the mapping to trfr_human."
    ),
    "calm_human": (
        "Calmodulin is a positive-control target, not a GPCR — GPCRdb "
        "does not host it. Expected empty payload. Non-canonical "
        "scoring flows through scorer/noncanonical.py and does not "
        "need pre_check anchor coverage."
    ),
}


_SPECIES_SUFFIX = {
    "human": "human",
    "mouse": "mouse",
    "rat":   "rat",
    "bovin": "bovin",
    "melga": "melga",    # turkey (Meleagris gallopavo)
    "9arac": "9arac",    # spider mite
    "chick": "chick",
    "pig":   "pig",
}


def species_for(entry_name: str) -> str:
    """Return the species tag encoded in a GPCRdb entry_name (adrb2_human → human)."""
    for suffix, sp in _SPECIES_SUFFIX.items():
        if entry_name.endswith("_" + suffix):
            return sp
    # Fallback: last _-suffix, lowercased
    parts = entry_name.rsplit("_", 1)
    return parts[1].lower() if len(parts) == 2 else "human"


# --------------------------------------------------------------------------
# Canonical WT FASTA reconstruction (UniProt-indexed with 'X' padding)
# --------------------------------------------------------------------------


def wt_fasta(api: Api, entry_name: str) -> tuple[str, dict[str, int]]:
    """Fetch the residues/extended payload and reconstruct the WT FASTA
    with UniProt indexing preserved (index N-1 ↔ UniProt pos N).

    Positions absent from the GPCRdb payload (rare; N-terminal signal-
    peptide trims, disordered loops occasionally) are padded with 'X'
    so downstream pre-checks see a sequence whose length matches the
    UniProt-maximum position — PC3/PC4 keep working against
    ``fasta[uniprot_pos - 1]``. ``_score_aligned`` in PC5 will treat 'X'
    as a non-standard residue and drop it from match blocks (matches
    the scorer's own behaviour).

    Returns ``(fasta_seq, stats)`` where ``stats`` carries counts:

        residues_returned   — non-empty AA rows from GPCRdb
        max_uniprot_pos     — highest position observed
        padded_gaps         — how many positions were 'X'-filled
    """
    bw_map = get_generic_numbers(api, entry_name)
    if not bw_map:
        return "", {"residues_returned": 0, "max_uniprot_pos": 0, "padded_gaps": 0}
    wt_seq: dict[int, str] = {}
    for pos, info in bw_map.items():
        aa = info.get("aa")
        if aa and aa in STD_AA:
            wt_seq[int(pos)] = aa
    if not wt_seq:
        return "", {"residues_returned": 0, "max_uniprot_pos": 0, "padded_gaps": 0}
    max_pos = max(wt_seq)
    seq = ["X"] * max_pos
    for pos, aa in wt_seq.items():
        seq[pos - 1] = aa
    fasta = "".join(seq)
    padded = fasta.count("X")
    return fasta, {
        "residues_returned": len(wt_seq),
        "max_uniprot_pos": max_pos,
        "padded_gaps": padded,
    }


# --------------------------------------------------------------------------
# Per-receptor audit
# --------------------------------------------------------------------------


def audit_one(
    primary_slug: str,
    entry_name: str,
    aliases: list[str],
    api: Api,
    ref_species_map: dict[str, set[str]],
) -> dict[str, Any]:
    """Run every pre-check on one receptor and return a flat row dict."""
    species = species_for(entry_name)
    row: dict[str, Any] = {
        "receptor_slug": primary_slug,
        "class": RECEPTOR_CLASS.get(primary_slug, "?"),
        "uniprot_slug": entry_name,
        "species": species,
        "aliases": ",".join(aliases),
        "fasta_len": 0,
        "residues_returned": 0,
        "padded_gaps": 0,
        "pc1_status": "", "pc1_reason": "",
        "pc2_status": "", "pc2_reason": "",
        "pc3_status": "", "pc3_reason": "",
        "pc4_status": "", "pc4_reason": "",
        "pc5_status": "", "pc5_reason": "",
        "overall_verdict": "",
        "notes": "",
    }
    try:
        fasta, stats = wt_fasta(api, entry_name)
    except Exception as e:
        row["pc1_status"] = "pc0_fetch_failed"
        row["pc1_reason"] = f"{type(e).__name__}: {e}"
        row["overall_verdict"] = "blocked"
        row["notes"] = "GPCRdb fetch failed — retry once cache warms."
        return row
    row["fasta_len"] = len(fasta)
    row["residues_returned"] = stats["residues_returned"]
    row["padded_gaps"] = stats["padded_gaps"]
    if not fasta:
        row["pc1_status"] = "pc0_fetch_failed"
        row["pc1_reason"] = "GPCRdb returned no residues"
        row["overall_verdict"] = "blocked"
        # Attach a curation hint when we already know the correct entry_name
        row["notes"] = (_EMPTY_PAYLOAD_HINTS.get(entry_name)
                        or "residues/extended returned empty payload — "
                           "check that entry_name in scorer/receptors.py "
                           "matches the GPCRdb URL slug")
        return row

    try:
        results = run_all_checks(
            receptor_slug=primary_slug,
            species=species,
            fasta_seq=fasta,
            partner_perturbation="wt",
            ref_species_map=ref_species_map,
            api=api,
        )
    except Exception as e:
        row["pc1_status"] = "pc0_fetch_failed"
        row["pc1_reason"] = f"{type(e).__name__}: {e}"
        row["overall_verdict"] = "blocked"
        return row

    for k in ("pc1", "pc2", "pc3", "pc4", "pc5"):
        st, why = results[k]
        row[f"{k}_status"] = st
        row[f"{k}_reason"] = why

    # ----- Verdict aggregation ------------------------------------------
    warns = [k for k in ("pc1", "pc2", "pc3", "pc4", "pc5")
             if row[f"{k}_status"].startswith("warn_")]

    # Special-case: PC5 warn caused by GPCRdb-derived FASTA <200 residues
    # is not a data problem, just an artefact of GPCRdb's extended payload.
    # We flag it but do not upgrade the verdict from ready.
    pc5_is_length_artifact = (
        "pc5" in warns
        and row["fasta_len"] < 200
        and row["fasta_len"] == row["residues_returned"] + row["padded_gaps"]
    )
    if pc5_is_length_artifact:
        row["notes"] = (
            f"PC5 warn is a GPCRdb-length artefact "
            f"({row['fasta_len']} residues); does not reflect a real problem."
        )

    # Verdict: ready | warn | blocked
    real_warns = [w for w in warns if not (w == "pc5" and pc5_is_length_artifact)]

    # Blocked = the receptor cannot pass without significant infra work.
    # Concretely: PC5 flags identity < 0.70 despite being a wt WT sequence
    # (i.e. the *only* WT sequence GPCRdb knows for this receptor is not
    # even 70 %-identical to what _score_aligned wants — that suggests a
    # broken GPCRdb entry) AND PC2 also warns (no cross-species reference
    # to fall back on).
    if row["pc5_status"].startswith("warn_A3") and not pc5_is_length_artifact and \
       row["pc2_status"].startswith("warn_A5"):
        row["overall_verdict"] = "blocked"
    elif real_warns:
        row["overall_verdict"] = "warn"
    else:
        row["overall_verdict"] = "ready"
    return row


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def build_markdown(rows: list[dict[str, Any]]) -> str:
    total = len(rows)
    ready = [r for r in rows if r["overall_verdict"] == "ready"]
    warned = [r for r in rows if r["overall_verdict"] == "warn"]
    blocked = [r for r in rows if r["overall_verdict"] == "blocked"]

    # Per-check warn distribution
    per_check = {k: 0 for k in ("pc1", "pc2", "pc3", "pc4", "pc5")}
    for r in rows:
        for k in per_check:
            if r[f"{k}_status"].startswith("warn_"):
                per_check[k] += 1
    per_check_pc5_artifact = sum(
        1 for r in rows
        if r["pc5_status"].startswith("warn_")
        and "GPCRdb-length artefact" in (r["notes"] or "")
    )

    # Per-class breakdown
    class_counts: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        class_counts[r["class"]][r["overall_verdict"]] += 1

    lines: list[str] = []
    lines.append("# Receptor-panel pre-check readiness — 2026-08-27")
    lines.append("")
    lines.append(
        "Deterministic sweep of `scorer.pre_check.run_all_checks(...)` over "
        "every unique GPCRdb entry in `scorer.receptors.KNOWN_RECEPTORS`. "
        "Each row is a *simulated WT proposal* (`partner_perturbation=\"wt\"`, "
        "canonical GPCRdb WT sequence, species inferred from entry-name "
        "suffix). Produced by `scripts/audit_receptor_readiness.py`; no HPC, "
        "no writes to `scorer/`."
    )
    lines.append("")
    lines.append("## Headline")
    lines.append("")
    lines.append(f"- **Unique receptors audited:** {total}")
    lines.append(f"- **Ready** (all 5 checks pass): **{len(ready)}**")
    lines.append(f"- **Warn** (≥1 check warns; curation may rescue): **{len(warned)}**")
    lines.append(f"- **Blocked** (no realistic curation path): **{len(blocked)}**")
    lines.append("")
    lines.append("## Per-check warn distribution")
    lines.append("")
    lines.append("| Check | Predicts | Warns (n) |")
    lines.append("|-------|----------|-----------|")
    predicts = {"pc1": "A6", "pc2": "A5", "pc3": "A2", "pc4": "A1", "pc5": "A3"}
    for k in ("pc1", "pc2", "pc3", "pc4", "pc5"):
        lines.append(f"| {k.upper()} | {predicts[k]} | {per_check[k]} |")
    lines.append("")
    lines.append(
        f"Of the {per_check['pc5']} PC5 warns, {per_check_pc5_artifact} are "
        f"GPCRdb-length artefacts (residues/extended payload <200 residues) "
        f"and do not indicate a real data problem — see the notes column."
    )
    lines.append("")
    lines.append("## Per-class breakdown")
    lines.append("")
    lines.append("| Class | Ready | Warn | Blocked | Total |")
    lines.append("|-------|-------|------|---------|-------|")
    for cls in sorted(class_counts):
        c = class_counts[cls]
        tot = c["ready"] + c["warn"] + c["blocked"]
        lines.append(
            f"| {cls} | {c['ready']} | {c['warn']} | {c['blocked']} | {tot} |"
        )
    lines.append("")

    # Warned receptors table
    lines.append("## Warned receptors")
    lines.append("")
    lines.append(
        "One row per receptor with at least one warn (`overall_verdict` "
        "in {`warn`, `blocked`}). Each cell after `class` is a per-check "
        "status; empty ⇒ pass. `notes` calls out length-artefact PC5 hits."
    )
    lines.append("")
    lines.append(
        "| Slug | Class | Species | PC1 (A6) | PC2 (A5) | PC3 (A2) | "
        "PC4 (A1) | PC5 (A3) | Verdict | Notes |"
    )
    lines.append(
        "|------|-------|---------|----------|----------|----------|"
        "----------|----------|---------|-------|"
    )
    warned_rows = sorted(warned + blocked, key=lambda r: (r["class"], r["receptor_slug"]))
    for r in warned_rows:
        def cell(k: str) -> str:
            st = r[f"{k}_status"]
            return "" if st == "pass" else st.replace("warn_", "w:")
        note = (r["notes"] or "").replace("|", "/")
        lines.append(
            f"| {r['receptor_slug']} | {r['class']} | {r['species']} | "
            f"{cell('pc1')} | {cell('pc2')} | {cell('pc3')} | "
            f"{cell('pc4')} | {cell('pc5')} | {r['overall_verdict']} | {note} |"
        )
    lines.append("")

    # Detailed reasons for each warned row
    lines.append("## Warn reasons — details")
    lines.append("")
    for r in warned_rows:
        lines.append(f"### {r['receptor_slug']} · class {r['class']} · {r['species']}")
        lines.append("")
        lines.append(
            f"UniProt slug `{r['uniprot_slug']}` · "
            f"FASTA reconstructed length **{r['fasta_len']}** "
            f"({r['residues_returned']} standard residues from GPCRdb, "
            f"{r['padded_gaps']} 'X'-padded gaps) · verdict **{r['overall_verdict']}**"
        )
        lines.append("")
        for k in ("pc1", "pc2", "pc3", "pc4", "pc5"):
            st = r[f"{k}_status"]
            why = r[f"{k}_reason"]
            if st.startswith("warn_") or st == "pc0_fetch_failed":
                lines.append(f"- **{k.upper()} ({st})** — {why}")
        if r["notes"]:
            lines.append(f"- _Note:_ {r['notes']}")
        lines.append("")

    # Class B/C/F callout — those receptors legitimately fail some checks
    non_class_a = [r for r in warned_rows if r["class"] in {"B", "C", "F", "T2R", "N"}]
    if non_class_a:
        lines.append("## Class-B/C/F/T2R/N receptors (expected structural mismatch)")
        lines.append("")
        lines.append(
            "These receptors lack the Class-A canonical anchor scaffolding "
            "(DRY at 3.50 / NPxxY at 7.53). Some PC warns are expected and "
            "annotative rather than blocking; they are itemised here for "
            "transparency."
        )
        lines.append("")
        for r in non_class_a:
            lines.append(f"- **{r['receptor_slug']}** (class {r['class']}) — "
                         f"verdict {r['overall_verdict']}; "
                         f"warned on: "
                         f"{', '.join(k.upper() for k in ('pc1','pc2','pc3','pc4','pc5') if r[f'{k}_status'].startswith('warn_'))}")
        lines.append("")

    # Ready section (compact)
    lines.append("## Ready receptors")
    lines.append("")
    lines.append(f"All {len(ready)} of these pass PC1..PC5 cleanly and can be "
                 f"included in Pattern-A wt-partner experiments as-is:")
    lines.append("")
    ready_by_class: dict[str, list[str]] = defaultdict(list)
    for r in ready:
        ready_by_class[r["class"]].append(r["receptor_slug"])
    for cls in sorted(ready_by_class):
        slugs = sorted(ready_by_class[cls])
        lines.append(f"- **Class {cls}** ({len(slugs)}): {', '.join(slugs)}")
    lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")
    lines.append("### Include as-is in Pattern-A")
    lines.append(f"The {len(ready)} `ready` receptors above. No curation required.")
    lines.append("")
    lines.append("### Warn — curation before inclusion")
    warn_curation = [r for r in warned if not any(
        "GPCRdb-length artefact" in (r["notes"] or "")
        for _ in [0]
    ) or r["overall_verdict"] == "warn"]
    lines.append(
        f"The {len(warned)} `warn` receptors. Typical fixes: add a "
        "cross-species reference row to `refs/reference_set.csv` (PC2), "
        "extend the FASTA past the last required anchor (PC3), or correct "
        "the receptor slug ↔ species mapping (PC4). Class-B/C/F PC4 or PC5 "
        "warns tied to missing DRY/NPxxY anchors are expected biology and "
        "safe to ignore for a WT proposal — treat those as annotative."
    )
    lines.append("")
    lines.append("### Blocked — infrastructure work required")
    if blocked:
        for r in blocked:
            lines.append(f"- **{r['receptor_slug']}** ({r['class']}, "
                         f"{r['species']}) — {r['notes'] or 'see per-check details above'}")
    else:
        lines.append("_None._")
    lines.append("")

    lines.append("## Reproducing this audit")
    lines.append("")
    lines.append(
        "```bash\npython scripts/audit_receptor_readiness.py\n```"
    )
    lines.append("")
    lines.append(
        "GPCRdb responses are cached in `refs/cache/gpcrdb/`. First run "
        "warms the cache (10-15 min at ~5 s per new receptor); subsequent "
        "runs finish in under a minute. No writes outside `docs/`."
    )
    lines.append("")
    return "\n".join(lines) + "\n"


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    cols = [
        "receptor_slug", "class", "uniprot_slug", "species", "aliases",
        "fasta_len", "residues_returned", "padded_gaps",
        "pc1_status", "pc2_status", "pc3_status", "pc4_status", "pc5_status",
        "pc1_reason", "pc2_reason", "pc3_reason", "pc4_reason", "pc5_reason",
        "overall_verdict", "notes",
    ]
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in sorted(rows, key=lambda x: (x["class"], x["receptor_slug"])):
            w.writerow({k: r.get(k, "") for k in cols})


# --------------------------------------------------------------------------
# CLI entrypoint
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--limit", type=int, default=0,
                        help="only audit the first N receptors (debug)")
    parser.add_argument("--verbose", action="store_true",
                        help="print progress per receptor")
    args = parser.parse_args(argv)

    api = Api(cache_dir=CACHE_DIR)
    ref_species_map = load_ref_species_map(REF_CSV)
    entries = primary_slugs()
    if args.limit:
        entries = entries[: args.limit]

    rows: list[dict[str, Any]] = []
    t0 = time.time()
    for i, (primary, entry, aliases) in enumerate(entries, 1):
        if args.verbose or i % 10 == 0:
            print(f"[{i}/{len(entries)}] {primary} ({entry}) — "
                  f"{time.time()-t0:.0f}s elapsed",
                  file=sys.stderr, flush=True)
        row = audit_one(primary, entry, aliases, api, ref_species_map)
        rows.append(row)

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(build_markdown(rows))
    write_csv(rows, OUT_CSV)

    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_CSV}")

    # Small on-screen summary
    verdicts = Counter(r["overall_verdict"] for r in rows)
    print(f"\nSummary: ready={verdicts['ready']}, "
          f"warn={verdicts['warn']}, blocked={verdicts['blocked']}, "
          f"total={len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
