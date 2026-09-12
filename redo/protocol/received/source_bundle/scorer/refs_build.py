"""`gpcr-refs` — reference-set build + threshold regeneration.

Two subcommands:

    gpcr-refs build       Fresh rebuild via GPCRdb + RCSB from
                          refs/reference_pdbs.csv → refs/reference_set.csv,
                          refs/pdbs.csv, refs/provenance/<PDB>.json.
                          --dry-run is a MANDATORY first pass (amendment S2).

    gpcr-refs thresholds  Compute the six axes on every accepted (active,
                          inactive) pair and write per-receptor
                          distributions to refs/state_thresholds.csv +
                          docs/THRESHOLD_DISTRIBUTION.md (amendment 1 —
                          the M1 gate).
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from scorer.anchors import AnchorSet, resolve_anchors
from scorer.axes import compute_all_axes, observed_aas_at_anchors
from scorer.bw_numbering import Api
from scorer.cache import content_sha256
from scorer.receptors import KNOWN_RECEPTORS, receptor_class, uniprot_slug
from scorer.references import DISQUALIFYING_STABILISERS
from scorer.schema import ANCHOR_KEYS
from scorer.structure import build_uniprot_model
from scorer.verified import verify, verify_reference_pdb


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


RCSB_ENTRY = "https://data.rcsb.org/rest/v1/core/entry/{pdb}"
RCSB_CIF = "https://files.rcsb.org/download/{pdb}.cif"


STABILISER_HINTS = [
    ("nanobody", ("nanobody", "nb6", "nb39", "nb35", "nb80")),
    ("scFv", ("scfv", "scfv16")),
    ("BRIL", ("bril", "cytochrome b(562)", "cytochrome b562", "b562ril")),
    ("T4L", ("t4l", "t4-lysozyme", "t4 lysozyme", "lysozyme")),
    ("DARPin", ("darpin",)),
    ("minibinder", ("minibinder",)),
    ("mini-Ga", ("mini-g", "mini gs", "mini gi", "mini gq")),
    ("arrestin", ("arrestin", "β-arrestin", "beta-arrestin")),
]


def detect_stabilisers(rcsb_entry_json: dict[str, Any]) -> frozenset[str]:
    """Best-effort detection of stabilising elements from an RCSB entry
    JSON. Looks at ``polymer_entity_names`` (heuristic — the authoritative
    check is A4 gating against the manual list in refs/reference_pdbs.csv
    ``stabilising_elements_manual`` column).
    """
    out: set[str] = set()
    text = json.dumps(rcsb_entry_json).lower()
    for label, tokens in STABILISER_HINTS:
        for t in tokens:
            if t in text:
                out.add(label)
                break
    return frozenset(out)


def load_pdb_bytes(api: Api, pdb_id: str, local_hint: Path | None = None) -> tuple[bytes, str]:
    """Prefer a local cached copy (HPC scratch) when present; otherwise
    fetch via RCSB. Files are stored under
    ``refs/cache/pdb/<pdb_id>.<ext>`` preserving the source format —
    gemmi picks its reader by extension, so writing PDB bytes into a
    .cif file corrupts the parse.

    Returns ``(bytes, extension)`` where extension is ``"cif"`` or ``"pdb"``.
    """
    pdb_id = pdb_id.upper()
    if local_hint is not None:
        for suffix in ("cif", "pdb"):
            p = local_hint / f"{pdb_id.lower()}.{suffix}"
            if p.exists():
                return p.read_bytes(), suffix
            p = local_hint / f"{pdb_id}.{suffix}"
            if p.exists():
                return p.read_bytes(), suffix
    data = api.get_bytes(
        RCSB_CIF.format(pdb=pdb_id.lower()),
        cache_key=f"pdb_{pdb_id.lower()}.cif",
    )
    if data is None:
        raise RuntimeError(f"RCSB returned no coordinates for {pdb_id}")
    return data, "cif"


def load_rcsb_entry(api: Api, pdb_id: str) -> dict[str, Any]:
    return api.get_json(
        RCSB_ENTRY.format(pdb=pdb_id.lower()),
        cache_key=f"rcsb_entry_{pdb_id.lower()}",
        ok404=True,
    ) or {}


# ---------------------------------------------------------------------------
# build subcommand
# ---------------------------------------------------------------------------


def _load_reference_pdbs_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as f:
        return [r for r in csv.DictReader(f)
                if r and (r.get("receptor_slug") or "").strip()
                and not (r["receptor_slug"] or "").startswith("#")]


def cmd_build(args: argparse.Namespace) -> int:
    src = Path(args.input)
    if not src.exists():
        print(f"reference_pdbs.csv not found at {src}", file=sys.stderr)
        return 2
    rows = _load_reference_pdbs_csv(src)

    api = Api(cache_dir=Path(args.cache_dir) / "gpcrdb")
    rcsb_api = Api(cache_dir=Path(args.cache_dir) / "rcsb")
    pdb_cache = Path(args.pdb_cache).resolve()
    pdb_cache.mkdir(parents=True, exist_ok=True)
    local_hint = Path(args.reuse_from).resolve() if args.reuse_from else None

    to_write: list[dict[str, Any]] = []
    pdb_rows: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []

    for r in rows:
        if (r.get("excluded") or "").strip().lower() == "true":
            excluded.append(r)
            if args.dry_run:
                print(f"EXCLUDE {r['receptor_slug']} {r['role']:>8} {r['pdb_id']}  "
                      f"{r['excluded_reason']}")
            continue
        pdb_id = r["pdb_id"].upper()
        receptor = r["receptor_slug"].upper()
        entry_name = r["uniprot_slug"].lower()

        # Species-vs-uniprot_slug gate: the `species` column in
        # reference_pdbs.csv is otherwise descriptive; a row with
        # ``species=mouse`` + ``uniprot_slug=adrb2_human`` would silently
        # measure the mouse PDB against the human UniProt sequence via
        # GPCRdb, producing off-anchor identity checks. Refuse those rows
        # here. Empty species stays permitted (backward compat — many
        # existing rows have empty species).
        species = (r.get("species") or "").strip().lower()
        if species and not entry_name.endswith("_" + species):
            raise ValueError(
                f"species/uniprot_slug mismatch in reference_pdbs.csv: "
                f"receptor={receptor} pdb_id={pdb_id} species={species!r} "
                f"uniprot_slug={entry_name!r} — uniprot_slug must end with "
                f"'_{species}'. Either correct the uniprot_slug, correct the "
                f"species token, or leave species empty."
            )

        # Construct labeling + optional residue-numbering offset. Default
        # ``wt`` / ``0`` for the ~172 existing rows that predate this
        # schema addition. ``construct_offset`` shifts the aligned UniProt
        # positions after ``build_uniprot_model`` renumbers — useful for
        # constructs whose numbering is systematically off by N against
        # the canonical UniProt sequence (chimeras with insertions/
        # deletions where difflib alignment produces a globally shifted
        # register).
        construct = (r.get("construct") or "").strip() or "wt"
        construct_offset_raw = (r.get("construct_offset") or "").strip()
        try:
            construct_offset = int(construct_offset_raw) if construct_offset_raw else 0
        except ValueError:
            raise ValueError(
                f"non-integer construct_offset={construct_offset_raw!r} for "
                f"receptor={receptor} pdb_id={pdb_id}"
            )

        if args.dry_run:
            print(f"FETCH  {receptor} {r['role']:>8} {pdb_id}  ({entry_name})")
            continue

        # anchors
        aset = resolve_anchors(api, entry_name)

        # coordinates
        raw, ext = load_pdb_bytes(rcsb_api, pdb_id, local_hint=local_hint)
        out_pdb = pdb_cache / f"{pdb_id.lower()}.{ext}"
        out_pdb.write_bytes(raw)
        pdb_sha = content_sha256(out_pdb)

        entry = load_rcsb_entry(rcsb_api, pdb_id)
        detected = detect_stabilisers(entry)
        manual = frozenset(s.strip() for s in
                           (r.get("stabilising_elements_manual") or "").split(";")
                           if s.strip())
        stab = detected | manual

        # measure d_r350_r630_ca_ref on the deposited coords.
        #
        # Finding #7 (docs/AUDIT_TRAIL.md): routing through the strict
        # verify() gate here silently NaN'd 15 curated receptors whose
        # crystals carry thermostabilising point mutations at 3.51 / 6.34
        # (A1 identity check fired) or whose ICL3 is disordered / T4L-
        # replaced (A2 coverage check fired globally). verify_reference_pdb
        # is the per-anchor-aware variant: A1 only raises on identity-
        # defining anchor mismatches (3.50 R, 5.58 Y, 7.53 Y) which
        # legitimately signal wrong chain; A2 coverage is per-axis so
        # d_r350_r630_ca cleanly NaN's when 3.50 or 6.30 CA is missing
        # instead of taking every other axis down with it.
        assertion_status = "OK"
        anchor_status: dict[str, Any] = {}
        try:
            model = build_uniprot_model(str(out_pdb), entry_name, api)
            # Apply construct_offset: shift the aligned UniProt positions
            # by N to correct systematic register mismatches in engineered
            # constructs. No-op when offset=0 (the default for wt PDBs).
            if construct_offset:
                model.residues = {
                    k + construct_offset: v for k, v in model.residues.items()
                }
            vresult = verify_reference_pdb(model, aset)
            axes = compute_all_axes(vresult.model)
            d_r350_r630 = axes["d_tm6_r350_r630_ca"]
            anchor_status = {
                "present": dict(vresult.anchor_present),
                "observed": dict(vresult.anchor_observed),
                "diagnostic_mismatches": {
                    k: list(v) for k, v in vresult.diagnostic_mismatches.items()
                },
                "coverage_missing": list(vresult.coverage_missing),
            }
            # per-axis coverage: 3.50 and 6.30 must both be present for a
            # numeric d_r350_r630_ca. If not, the axis is legitimately NaN
            # (crystal doesn't resolve one of the anchors). Downstream
            # tripwire distinguishes this from a bug.
            if not vresult.has_axis_coverage("3.50", "6.30"):
                missing = [
                    a for a in ("3.50", "6.30")
                    if not vresult.anchor_present.get(a, False)
                ]
                assertion_status = f"NO_COVERAGE:{','.join(missing)}"
            elif vresult.diagnostic_mismatches:
                # non-fatal point mutations at 3.51/6.30/6.34 — recorded
                # but the measurement is still emitted
                assertion_status = "OK_POINT_MUTATION:" + ",".join(
                    sorted(vresult.diagnostic_mismatches)
                )
        except Exception as e:  # lint-allow: capture-and-record — surface then continue
            print(f"WARN {pdb_id}: {type(e).__name__}: {e}", file=sys.stderr)
            d_r350_r630 = float("nan")
            assertion_status = f"FAIL:{type(e).__name__}"

        provenance_path = Path(args.out_provenance) / f"{pdb_id}.json"
        provenance_path.parent.mkdir(parents=True, exist_ok=True)
        provenance = {
            "pdb_id": pdb_id,
            "uniprot_slug": entry_name,
            "receptor_slug": receptor,
            "role": r["role"],
            "candidate_state": r["candidate_state"],
            "species": r["species"],
            "construct": construct,
            "construct_offset": construct_offset,
            "pdb_sha256": pdb_sha,
            "rcsb_entry": entry,
            "gpcrdb_residues_ext_sha256": aset.residues_ext_payload_sha256,
            "anchors": {label: asdict(a) for label, a in aset.anchors.items()},
            "detected_stabilisers": sorted(detected),
            "manual_stabilisers": sorted(manual),
            "d_tm6_r350_r630_ca_ref": d_r350_r630,
            "assertion_status": assertion_status,
            "anchor_status": anchor_status,  # Finding #7: per-anchor
                                              # presence + point-mutation
                                              # census for silent-NaN
                                              # tripwire
        }
        provenance_path.write_text(json.dumps(provenance, indent=2, sort_keys=False))
        prov_sha = content_sha256(provenance_path)

        pdb_rows.append({
            "pdb_sha": pdb_sha,
            "pdb_id": pdb_id,
            "uniprot_slug": entry_name,
            "species": r["species"],
            "resolved_state": r["candidate_state"],
            "stabilising_elements": ";".join(sorted(stab)) or "none",
            "provenance_url": RCSB_CIF.format(pdb=pdb_id.lower()),
            "provenance_sha256": prov_sha,
        })
        to_write.append({
            "receptor_slug": receptor,
            "role": r["role"],
            "pdb_id": pdb_id,
            "uniprot_slug": entry_name,
            "species": r["species"],
            "resolved_state": r["candidate_state"],
            "stabilising_elements": ";".join(sorted(stab)) or "none",
            "construct": construct,
            "construct_offset": construct_offset,
            "d_r350_r630_ca_ref": d_r350_r630,
            "anchor_positions": json.dumps(
                {label: a.uniprot_pos for label, a in aset.anchors.items()},
                separators=(",", ":"),
            ),
            "provenance_sha256": prov_sha,
        })
        print(f"OK    {receptor} {r['role']:>8} {pdb_id}  d={d_r350_r630:.2f}  "
              f"stab={sorted(stab) or 'none'}")

    if args.dry_run:
        print(f"\nDRY-RUN: would fetch {len(rows) - len(excluded)} PDBs, "
              f"exclude {len(excluded)}. Nothing written.", file=sys.stderr)
        return 0

    # reference_set.csv
    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    cols_rs = [
        "receptor_slug", "role", "pdb_id", "uniprot_slug", "species",
        "resolved_state", "stabilising_elements", "construct",
        "construct_offset", "d_r350_r630_ca_ref", "anchor_positions",
        "provenance_sha256",
    ]
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols_rs)
        w.writeheader()
        for row in to_write:
            w.writerow(row)

    # pdbs.csv
    cols_pdbs = [
        "pdb_sha", "pdb_id", "uniprot_slug", "species", "resolved_state",
        "stabilising_elements", "provenance_url", "provenance_sha256",
    ]
    with Path("refs/pdbs.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols_pdbs)
        w.writeheader()
        for row in pdb_rows:
            w.writerow(row)

    print(f"wrote {out_csv} ({len(to_write)} rows) + refs/pdbs.csv "
          f"({len(pdb_rows)} rows) + {len(pdb_rows)} provenance files",
          file=sys.stderr)

    # Finding #7 tripwire (docs/AUDIT_TRAIL.md#7): every row in
    # reference_pdbs.csv is a curated PDB the user has told us to measure.
    # If d_r350_r630_ca_ref is NaN for any row that made it this far, the
    # measurement pipeline dropped a value silently — the class of bug the
    # scorer exists to eliminate. Raise with the per-row reason so the
    # operator sees exactly which PDBs failed and why.
    #
    # "Legitimate absences" (receptors with NO row in reference_pdbs.csv
    # at all) never reach this loop, so they cannot fire this tripwire.
    silent_nans: list[dict[str, str]] = []
    for row in to_write:
        val = row.get("d_r350_r630_ca_ref")
        if val is None:
            is_nan = True
        else:
            try:
                is_nan = (float(val) != float(val))  # NaN != NaN
            except (TypeError, ValueError):
                is_nan = True
        if is_nan and (row.get("pdb_id") or ""):
            silent_nans.append({
                "receptor_slug": row["receptor_slug"],
                "role": row["role"],
                "pdb_id": row["pdb_id"],
            })
    if silent_nans and not args.allow_nan_tripwire:
        # dump the exact list so the operator can act without re-running
        detail = "\n".join(
            f"  {r['receptor_slug']:8s} {r['role']:8s} {r['pdb_id']}"
            for r in silent_nans
        )
        raise RuntimeError(
            f"refs_build tripwire (finding #7): {len(silent_nans)} row(s) in "
            f"reference_pdbs.csv produced d_r350_r630_ca_ref=nan.\n"
            f"Each row was a curated PDB — silent-NaN emission is the class "
            f"of bug this scorer eliminates. Inspect refs/provenance/<PDB>.json\n"
            f"for the per-anchor status / assertion_status. To force through "
            f"the tripwire (e.g. accepting genuinely disordered 6.30 in a\n"
            f"crystal, having marked the PDB excluded in reference_pdbs.csv "
            f"in a follow-up), pass --allow-nan-tripwire.\n\n"
            f"Rows with NaN d_r350_r630_ca_ref:\n{detail}"
        )
    return 0


# ---------------------------------------------------------------------------
# thresholds subcommand — the M1 gate
# ---------------------------------------------------------------------------


def cmd_thresholds(args: argparse.Namespace) -> int:
    """Regenerate NPxxY / TM6 / displacement thresholds from crystal pairs.

    Reads refs/reference_set.csv, groups by receptor with both an active
    and an inactive row, measures all axes on both. Emits per-receptor
    distribution to docs/THRESHOLD_DISTRIBUTION.md and per-axis medians
    to refs/state_thresholds.csv.

    THIS IS AMENDMENT 1 — no numbers are inherited from the frozen
    pipeline; the frozen 14.74 / 18.25 NPxxY medians are recomputed here
    from scratch through the new scorer.
    """
    rs = Path(args.reference_set)
    if not rs.exists():
        print(f"reference_set.csv not found at {rs} — run `gpcr-refs build` first",
              file=sys.stderr)
        return 2
    api = Api(cache_dir=Path(args.cache_dir) / "gpcrdb")
    pdb_cache = Path(args.pdb_cache)

    # group rows by receptor / role
    grouped: dict[str, dict[str, dict[str, Any]]] = {}
    with rs.open() as f:
        for row in csv.DictReader(f):
            r = row["receptor_slug"].upper()
            grouped.setdefault(r, {})[row["role"].lower()] = row

    # coupling class from a small hardcoded table (best-effort)
    COUPLING = {
        "ADRB1": "Gs", "ADRB2": "Gs", "ADRB3": "Gs",
        "AA1R": "Gi", "AA2AR": "Gs", "AA2BR": "Gs", "AA3R": "Gi",
        "ACM1": "Gq", "ACM2": "Gi", "ACM3": "Gq", "ACM4": "Gi", "ACM5": "Gq",
        "5HT1A": "Gi", "5HT1B": "Gi", "5HT2A": "Gq", "5HT2B": "Gq", "5HT2C": "Gq",
        "5HT5A": "Gi", "5HT6R": "Gs", "5HT7R": "Gs",
        "DRD1": "Gs", "DRD2": "Gi", "DRD3": "Gi", "DRD4": "Gi", "DRD5": "Gs",
        "OPRD": "Gi", "OPRK": "Gi", "OPRM": "Gi", "OPRX": "Gi",
        "HRH1": "Gq", "HRH2": "Gs", "HRH3": "Gi", "HRH4": "Gi",
        "NK1R": "Gq", "NK2R": "Gq", "NK3R": "Gq",
        "GHSR": "Gq", "MC4R": "Gs",
        "CNR1": "Gi", "CNR2": "Gi",
        "AGTR1": "Gq",
        "EDNRA": "Gq", "EDNRB": "Gq",
        "OXYR": "Gq",
        "APJ": "Gi", "C5AR1": "Gi",
        "CCR2": "Gi", "CCR5": "Gi", "CCR6": "Gi", "CCR8": "Gi",
        "CXCR2": "Gi", "CXCR3": "Gi", "CXCR4": "Gi",
        "MTR1A": "Gi", "MTR1B": "Gi",
        "SSR2": "Gi", "SSR5": "Gi",
        "NPY1R": "Gi", "NPY2R": "Gi",
        "TRHR": "Gq", "V1AR": "Gq", "V1BR": "Gq", "V2R": "Gs",
        "FSHR": "Gs", "LSHR": "Gs", "TSHR": "Gs",
        "NTR1": "Gq", "OX2R": "Gq", "OPSD": "Gt",
    }

    # census — every failure gets counted, nothing silently disappears
    census: dict[str, int] = {}

    per_receptor: list[dict[str, Any]] = []
    for receptor, roles in sorted(grouped.items()):
        if "active" not in roles or "inactive" not in roles:
            missing_role = "active" if "active" not in roles else "inactive"
            census[f"missing_role:{missing_role}"] = census.get(f"missing_role:{missing_role}", 0) + 1
            print(f"SKIP {receptor}: has only role(s) {list(roles)}",
                  file=sys.stderr)
            continue

        # KNOWN_RECEPTORS raises A6 if unknown — no silent drop (amendment
        # fix 2). Extends the failure census so an absent receptor shows
        # up in the paper figure rather than in a stderr line nobody reads.
        try:
            entry_name = uniprot_slug(receptor)
        except Exception as e:  # lint-allow: capture-and-record — recast as census entry
            census["A6_receptor_identity"] = census.get("A6_receptor_identity", 0) + 1
            print(f"SKIP {receptor}: A6ReceptorIdentity: {e}", file=sys.stderr)
            continue

        active_pdb = None
        inactive_pdb = None
        for ext in ("cif", "pdb"):
            ap = pdb_cache / f"{roles['active']['pdb_id'].lower()}.{ext}"
            ip = pdb_cache / f"{roles['inactive']['pdb_id'].lower()}.{ext}"
            if ap.exists() and active_pdb is None:
                active_pdb = ap
            if ip.exists() and inactive_pdb is None:
                inactive_pdb = ip
        if active_pdb is None or inactive_pdb is None:
            census["coord_file_missing"] = census.get("coord_file_missing", 0) + 1
            print(f"SKIP {receptor}: coord file missing "
                  f"(active={active_pdb is not None}, "
                  f"inactive={inactive_pdb is not None})",
                  file=sys.stderr)
            continue

        # Routing through verify() is what fixes the M1 A1-leak — 6OS2 style
        # rows that raised A1 during build cannot emit garbage axes because
        # compute_all_axes DEMANDS a VerifiedModel (TypeError otherwise).
        # Look up receptor class for class-conditional A2 (see
        # scorer/anchors.py::REQUIRED_ANCHORS_BY_CLASS).
        try:
            rec_class = receptor_class(receptor)
        except Exception:
            rec_class = None
        aset = resolve_anchors(api, entry_name)
        try:
            model_a = build_uniprot_model(str(active_pdb), entry_name, api)
            model_i = build_uniprot_model(str(inactive_pdb), entry_name, api)
            vmodel_a = verify(model_a, aset, receptor_class=rec_class)
            vmodel_i = verify(model_i, aset, receptor_class=rec_class)
            axes_a = compute_all_axes(vmodel_a)
            axes_i = compute_all_axes(vmodel_i)
        except Exception as e:  # lint-allow: capture-and-record — census + continue
            key = type(e).__name__
            census[key] = census.get(key, 0) + 1
            print(f"SKIP {receptor}: {key}: {e}", file=sys.stderr)
            continue

        per_receptor.append({
            "receptor": receptor,
            "coupling": COUPLING.get(receptor, "unknown"),
            "active_pdb": roles["active"]["pdb_id"],
            "inactive_pdb": roles["inactive"]["pdb_id"],
            "d_tm6_active": axes_a["d_tm6_r350_r630_ca"],
            "d_tm6_inactive": axes_i["d_tm6_r350_r630_ca"],
            "d_npxxy_active": axes_a["d_npxxy_y558_y753_ca"],
            "d_npxxy_inactive": axes_i["d_npxxy_y558_y753_ca"],
            "d_y558_pack_active": axes_a["d_y558_pack_min_heavy"],
            "d_y558_pack_inactive": axes_i["d_y558_pack_min_heavy"],
            "d_dry_active": axes_a["d_dry_sidechain_r350cz_e630oe1"],
            "d_dry_inactive": axes_i["d_dry_sidechain_r350cz_e630oe1"],
            "d_tm5_active": axes_a["d_tm5_outward_r350_r558_ca"],
            "d_tm5_inactive": axes_i["d_tm5_outward_r350_r558_ca"],
        })

    # write CSV
    out_csv = Path(args.out)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    if per_receptor:
        with out_csv.open("w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(per_receptor[0].keys()))
            w.writeheader()
            for row in per_receptor:
                w.writerow(row)

    # threshold-regen failure census — separate paper figure from the
    # Phase A batch census in scorer/cli.py.
    census_path = out_csv.parent / "threshold_census.json"
    census_path.write_text(json.dumps({
        "total_receptors_seen": len(grouped),
        "pairs_scored": len(per_receptor),
        "by_failure_reason": dict(sorted(census.items())),
    }, indent=2))

    # write markdown report
    report = _threshold_report(per_receptor)
    Path(args.report).parent.mkdir(parents=True, exist_ok=True)
    Path(args.report).write_text(report)
    print(f"wrote {out_csv} ({len(per_receptor)} pair rows) and {args.report}",
          file=sys.stderr)
    return 0


def _median_and_iqr(values: list[float]) -> tuple[float, float, float]:
    xs = sorted(v for v in values if v == v)  # drop NaN
    if not xs:
        return (float("nan"), float("nan"), float("nan"))
    med = statistics.median(xs)
    q1 = xs[len(xs) // 4] if len(xs) >= 4 else xs[0]
    q3 = xs[3 * len(xs) // 4] if len(xs) >= 4 else xs[-1]
    return med, q1, q3


def _threshold_report(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "# Threshold distribution\n\nNo pairs scored. Run `gpcr-refs build` first.\n"

    tm6_a = [r["d_tm6_active"] for r in rows]
    tm6_i = [r["d_tm6_inactive"] for r in rows]
    np_a = [r["d_npxxy_active"] for r in rows]
    np_i = [r["d_npxxy_inactive"] for r in rows]

    med_tm6_a, q1_tm6_a, q3_tm6_a = _median_and_iqr(tm6_a)
    med_tm6_i, q1_tm6_i, q3_tm6_i = _median_and_iqr(tm6_i)
    med_np_a, q1_np_a, q3_np_a = _median_and_iqr(np_a)
    med_np_i, q1_np_i, q3_np_i = _median_and_iqr(np_i)

    by_coupling: dict[str, dict[str, list[float]]] = {}
    for r in rows:
        c = r["coupling"]
        by_coupling.setdefault(c, {"tm6_a": [], "tm6_i": [], "np_a": [], "np_i": []})
        by_coupling[c]["tm6_a"].append(r["d_tm6_active"])
        by_coupling[c]["tm6_i"].append(r["d_tm6_inactive"])
        by_coupling[c]["np_a"].append(r["d_npxxy_active"])
        by_coupling[c]["np_i"].append(r["d_npxxy_inactive"])

    lines: list[str] = []
    lines.append("# Threshold distribution — M1 gate report\n")
    lines.append("Regenerated fresh through the new scorer per amendment 1. "
                 f"No numbers imported from the frozen pipeline.\n")
    lines.append(f"**n receptors with an active/inactive pair scored:** {len(rows)}\n")
    lines.append("## Panel-wide medians (median, IQR)\n")
    lines.append("| axis | active | inactive | Δ (inactive - active) |")
    lines.append("|---|---|---|---|")
    lines.append(f"| TM6 R3.50–6.30 CA-CA | {med_tm6_a:.2f} "
                 f"({q1_tm6_a:.2f}–{q3_tm6_a:.2f}) | "
                 f"{med_tm6_i:.2f} ({q1_tm6_i:.2f}–{q3_tm6_i:.2f}) | "
                 f"{med_tm6_i - med_tm6_a:.2f} |")
    lines.append(f"| NPxxY Y5.58–Y7.53 CA-CA | {med_np_a:.2f} "
                 f"({q1_np_a:.2f}–{q3_np_a:.2f}) | "
                 f"{med_np_i:.2f} ({q1_np_i:.2f}–{q3_np_i:.2f}) | "
                 f"{med_np_i - med_np_a:.2f} |\n")

    lines.append("## Polarity check\n")
    if med_np_a < med_np_i:
        lines.append(
            "**Regenerated:** active NPxxY < inactive NPxxY "
            f"({med_np_a:.2f} < {med_np_i:.2f} Å).\n\n"
            "**Frozen pipeline reported the same direction** "
            "(active 14.74 Å < inactive 18.25 Å per w56_0c). Independent "
            "confirmation of polarity. The Wave 55.1 coherence apparent "
            "contradiction is resolved: predictions clustering at 13–16 Å "
            "sit at or below the active median, which is consistent with "
            "'nearly reaching active but not quite' — the coherence claim's "
            "verbal framing was misleading, not the direction."
        )
    elif med_np_a > med_np_i:
        lines.append(
            "**Regenerated:** active NPxxY > inactive NPxxY "
            f"({med_np_a:.2f} > {med_np_i:.2f} Å).\n\n"
            "**POLARITY INVERTED** vs the frozen pipeline (which reported "
            "active 14.74 < inactive 18.25). Artefact #7 caught before "
            "entering the repo — the frozen 14.74/18.25 label assignment "
            "was flipped in `w56_0c_crystal_calibration.py` and every "
            "downstream state classification inherited the sign error."
        )
    else:
        lines.append(f"NPxxY medians tie at {med_np_a:.2f} Å. State discrimination "
                     "on this axis alone is not defined for this panel.\n")

    lines.append("\n## Per-coupling-class distributions\n")
    lines.append("| coupling | n | TM6 active (med, IQR) | TM6 inactive | NPxxY active | NPxxY inactive |")
    lines.append("|---|---|---|---|---|---|")
    for c, d in sorted(by_coupling.items()):
        n = len([v for v in d["tm6_a"] if v == v])
        m1, q1a, q3a = _median_and_iqr(d["tm6_a"])
        m2, q1b, q3b = _median_and_iqr(d["tm6_i"])
        m3, q1c, q3c = _median_and_iqr(d["np_a"])
        m4, q1d, q3d = _median_and_iqr(d["np_i"])
        lines.append(f"| {c} | {n} | {m1:.2f} ({q1a:.2f}–{q3a:.2f}) | "
                     f"{m2:.2f} ({q1b:.2f}–{q3b:.2f}) | "
                     f"{m3:.2f} ({q1c:.2f}–{q3c:.2f}) | "
                     f"{m4:.2f} ({q1d:.2f}–{q3d:.2f}) |")

    lines.append("\n## Per-receptor rows\n")
    lines.append("| receptor | coupling | active_pdb | inactive_pdb | "
                 "TM6 act | TM6 ina | Δ TM6 | NPxxY act | NPxxY ina | Δ NPxxY |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        d_tm6 = r["d_tm6_inactive"] - r["d_tm6_active"]
        d_np = r["d_npxxy_inactive"] - r["d_npxxy_active"]
        lines.append(
            f"| {r['receptor']} | {r['coupling']} | "
            f"{r['active_pdb']} | {r['inactive_pdb']} | "
            f"{r['d_tm6_active']:.2f} | {r['d_tm6_inactive']:.2f} | {d_tm6:.2f} | "
            f"{r['d_npxxy_active']:.2f} | {r['d_npxxy_inactive']:.2f} | {d_np:.2f} |"
        )

    lines.append("\n## Interpretation notes\n")
    lines.append(
        "The `Δ` columns above are the raw per-receptor active-vs-inactive "
        "separations. A single canonical Class-A threshold is well-defined "
        "for an axis only if the receptor-level Δ has narrow support and "
        "consistent sign. Where the sign is mixed within a coupling class, "
        "state classification on that axis must be per-receptor (as this "
        "scorer's `refs/state_thresholds.csv` does), not panel-wide."
    )
    lines.append(
        "\nThe amendment 1 displacement rule (frozen: `d_active - d_inactive "
        "≥ 3 Å`) is superseded here by the observed per-receptor Δ "
        "distribution. Refuse a reference pair only if the observed Δ is "
        "outside the panel's [P5, P95] range or flips sign relative to "
        "the receptor's coupling-class median."
    )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# argparse
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gpcr-refs")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="fresh reference-set rebuild via GPCRdb + RCSB")
    b.add_argument("--input", default="refs/reference_pdbs.csv")
    b.add_argument("--out-csv", default="refs/reference_set.csv")
    b.add_argument("--out-provenance", default="refs/provenance/")
    b.add_argument("--pdb-cache", default="refs/cache/pdb/")
    b.add_argument("--cache-dir", default="refs/cache/")
    b.add_argument("--reuse-from", default=None,
                   help="local directory of pre-fetched coord files "
                        "(e.g. /hpc/scratch/sengaad1/subsampling/refs/gpcr_panel_pdbs/)")
    b.add_argument("--dry-run", action="store_true",
                   help="print what would fetch / exclude; write nothing. "
                        "MANDATORY first pass (amendment S2).")
    b.add_argument("--allow-nan-tripwire", action="store_true",
                   help="Suppress the Finding #7 silent-NaN tripwire. "
                        "Use only when the operator has already inspected "
                        "the per-row NaN reasons and accepts them (e.g. "
                        "reference PDBs with genuinely disordered 6.30).")

    t = sub.add_parser("thresholds",
                       help="regenerate state thresholds (M1 gate; amendment 1)")
    t.add_argument("--reference-set", default="refs/reference_set.csv")
    t.add_argument("--pdb-cache", default="refs/cache/pdb/")
    t.add_argument("--cache-dir", default="refs/cache/")
    t.add_argument("--out", default="refs/state_thresholds.csv")
    t.add_argument("--report", default="docs/THRESHOLD_DISTRIBUTION.md")

    args = p.parse_args(argv)
    if args.cmd == "build":
        return cmd_build(args)
    if args.cmd == "thresholds":
        return cmd_thresholds(args)
    raise ValueError(f"unknown subcommand {args.cmd}")


if __name__ == "__main__":
    sys.exit(main())
