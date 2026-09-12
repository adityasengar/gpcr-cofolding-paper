"""Verify `active_stabilization_source` for every Class A active reference PDB.

Block B Stage-0 Gate 2 driver. Fetches PDB metadata via the RCSB REST API,
classifies each active reference PDB into one of the stabilisation classes,
compares against the current annotation in refs/reference_set.csv, and emits
refs/reference_set.stratification.csv.

Zero GPU. Pure PDB API + reasoning. Does NOT modify refs/reference_set.csv.

Also emits a small diagnostic block for the 4 NaN-OH inactive-side receptors
(EDNRB, FSHR, LSHR, GRPR) and probes GPCRdb (best-effort) for the 8 no-active
receptors (ACM1, ADA2A, ADRB1, CCKAR, DRD3, EDNRA, HRH3, OX2R).

Usage:
    python scripts/verify_active_stabilization.py

Outputs:
    refs/reference_set.stratification.csv
    experiments/019_block_b_partner_selection/analysis/reference_state_verification_report.md
      (this script emits the CSV + a JSON sidecar; the .md report is authored
       in the accompanying handoff)
    experiments/018_block_a_switch_test/analysis/reference_state_verification.json
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parent.parent
REF_CSV = REPO / "refs" / "reference_set.csv"
OUT_CSV = REPO / "refs" / "reference_set.stratification.csv"
OUT_JSON = REPO / "experiments" / "018_block_a_switch_test" / "analysis" / "reference_state_verification.json"
CACHE_DIR = REPO / "refs" / "cache" / "pdb_stabilization_verify"

RATE_LIMIT_S = 0.05  # per PDB request

# Fusion partners used for crystallography — NOT the activation partner
FUSION_KEYWORDS = [
    "lysozyme", "t4l", "bril", "cytochrome b562",
    "flavodoxin", "rubredoxin", "pgs", "glycogen synthase",
    "thermostabilized apocytochrome",
]

# Gα identifiers (broad — anything mentioning the G-alpha subunit family)
GA_ALPHA_KEYWORDS = [
    "g-alpha", "g alpha", "gα", "galpha",
    "guanine nucleotide-binding protein g",  # covers Gα, Gβ, Gγ; disambiguated below
    "guanine nucleotide binding protein g",
]

# Anything that flags a mini-Gα engineering (explicit keywords only; length rule below)
MINIG_KEYWORDS = [
    "mini-g", "minig", "mini g", "engineered mini",
    "minigs", "minigi", "minigo", "minigq",
    "mini-gs", "mini-gi", "mini-go", "mini-gq",
    "engineered domain",
]

# Dominant-negative Gα constructs (full-length with mutations) — NOT mini-G
DNG_KEYWORDS = ["dngα", "dngalpha", "dn-galpha", "dominant negative g", "dominant-negative g"]

# Full-length-Gα length cutoff. Below this, treat any Gα entity as mini-Gα.
# Full-length: Gαi/o ~354, Gαs-short ~380, Gαs-long ~394, Gαq ~359.
# Mini-Gα (Carpenter/Tate scaffold): ~225-230.
MINIG_LENGTH_MAX = 280

# Chimera markers
CHIMERA_KEYWORDS = ["chimera", "chimeric"]

# Nanobody / single-domain antibody markers
NANOBODY_KEYWORDS = [
    "nanobody", "single-domain antibody", "single domain antibody",
    "camelid", "vhh", "sybody",
]

# scFv markers
SCFV_KEYWORDS = ["scfv", "single-chain variable fragment", "single chain variable"]

# The 32 Class A receptors expected to have an active reference (from BLOCK_B_PRE_DISPATCH_DECISIONS_2026_09_02.md).
CLASS_A_ACTIVE_RECEPTORS = {
    "5HT1B", "5HT2C", "5HT5A", "AA1R", "AA2AR", "ACM2", "ACM4", "ADRB2",
    "AGTR1", "APJ", "B1B1U5", "CCR5", "CNR1", "CNR2", "CXCR2", "CXCR4",
    "DRD2", "EDNRB", "FSHR", "GHSR", "GRPR", "HRH1", "LPAR1", "LSHR",
    "LT4R1", "MCHR1", "NPY1R", "NPY2R", "OPRD", "OPRK", "OPRX", "OPSD",
}

# The 8 Class A receptors with no active reference in refs/reference_set.csv
CLASS_A_NO_ACTIVE = ["ACM1", "ADA2A", "ADRB1", "CCKAR", "DRD3", "EDNRA", "HRH3", "OX2R"]

# The 4 receptors with NaN NPxxY-OH on the inactive side (need replacement inactive PDB check)
NAN_OH_INACTIVE_RECEPTORS = ["EDNRB", "FSHR", "LSHR", "GRPR"]


def fetch_json(url: str, cache_key: str) -> dict[str, Any] | None:
    """GET JSON with a filesystem cache. Returns None on 404 or network error."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path = CACHE_DIR / f"{cache_key}.json"
    if cache_path.exists():
        try:
            return json.loads(cache_path.read_text())
        except json.JSONDecodeError:
            cache_path.unlink()
    time.sleep(RATE_LIMIT_S)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "paper-af3-verify-stabilization/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        cache_path.write_text(json.dumps(data))
        return data
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        print(f"    HTTPError {e.code} on {url}: {e.reason}", file=sys.stderr)
        return None
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"    Network error on {url}: {e}", file=sys.stderr)
        return None


def fetch_entry(pdb: str) -> dict[str, Any] | None:
    return fetch_json(f"https://data.rcsb.org/rest/v1/core/entry/{pdb}", f"entry_{pdb}")


def fetch_polymer_entity(pdb: str, entity_id: str) -> dict[str, Any] | None:
    return fetch_json(
        f"https://data.rcsb.org/rest/v1/core/polymer_entity/{pdb}/{entity_id}",
        f"poly_{pdb}_{entity_id}",
    )


def fetch_nonpolymer_entity(pdb: str, entity_id: str) -> dict[str, Any] | None:
    return fetch_json(
        f"https://data.rcsb.org/rest/v1/core/nonpolymer_entity/{pdb}/{entity_id}",
        f"nonpoly_{pdb}_{entity_id}",
    )


def _lower(s: str | None) -> str:
    return (s or "").lower()


def is_gpcr_receptor(desc: str) -> bool:
    """Heuristic: identifies the receptor entity itself."""
    d = _lower(desc)
    if "receptor" in d and "guanine nucleotide" not in d:
        return True
    if "rhodopsin" in d or "opsin" in d:
        return True
    if "adrenoceptor" in d or "adrenergic receptor" in d:
        return True
    return False


def is_fusion(desc: str) -> bool:
    d = _lower(desc)
    return any(k in d for k in FUSION_KEYWORDS)


def looks_like_alpha5_ct_peptide(desc: str, seq_len: int) -> bool:
    """A short peptide (<= 25 aa) whose description references Gα C-terminus."""
    d = _lower(desc)
    if seq_len > 25:
        return False
    ct_markers = ["c-terminal", "c terminal", "alpha 5", "alpha5", "α5"]
    ga_markers = ["g(alpha)", "galpha", "g-alpha", "g alpha", "gα",
                  "subunit alpha", "g(t)", "g(i)", "g(o)", "g(s)", "g(q)",
                  "transducin", "gustducin"]
    has_ct = any(m in d for m in ct_markers)
    has_ga = any(m in d for m in ga_markers)
    return has_ct and has_ga


def is_g_alpha(desc: str, seq_len: int) -> bool:
    """Full or near-full Gα subunit (not just the α5-CT peptide, not β/γ).

    Accepts:
      - "...subunit alpha", "...alpha subunit", "G-alpha", "G alpha", "Galpha"
      - "miniGo/Gs/Gi/Gq protein" (one-word forms)
      - "engineered domain of ... G alpha ..."
    Rejects short peptides (< ~140 aa) which are α5-CT peptide territory.
    """
    d = _lower(desc)
    is_ga = False
    if "subunit alpha" in d or "alpha subunit" in d:
        is_ga = True
    if "g-alpha" in d or "g alpha" in d or "galpha" in d:
        is_ga = True
    if re.search(r"g\(?[siotq]?\)?\s*subunit\s+alpha", d):
        is_ga = True
    if re.search(r"minig[siotq]", d):
        is_ga = True
    if "engineered domain" in d and ("g alpha" in d or "galpha" in d or "g-alpha" in d):
        is_ga = True
    if not is_ga:
        return False
    if seq_len < 140:
        return False
    return True


def is_g_beta(desc: str) -> bool:
    d = _lower(desc)
    return "subunit beta" in d and "guanine nucleotide" in d


def is_g_gamma(desc: str) -> bool:
    d = _lower(desc)
    return "subunit gamma" in d and "guanine nucleotide" in d


def has_mini_g(desc: str, seq_len: int = 999) -> bool:
    """Explicit mini-G keywords OR (Gα-like AND length below full-length cutoff).

    The length rule catches short Gα scaffolds (~225 aa) that lack the
    "mini-G" name string in their entity description (e.g. 5G53's
    "ENGINEERED DOMAIN OF HUMAN G ALPHA S LONG ISOFORM").
    """
    d = _lower(desc)
    if any(k in d for k in MINIG_KEYWORDS):
        return True
    if seq_len <= MINIG_LENGTH_MAX and is_g_alpha(d, seq_len):
        return True
    return False


def has_dng(desc: str) -> bool:
    """Dominant-negative Gα (full-length; NOT mini-G)."""
    d = _lower(desc)
    return any(k in d for k in DNG_KEYWORDS)


def has_chimera(desc: str) -> bool:
    d = _lower(desc)
    if any(k in d for k in CHIMERA_KEYWORDS):
        # Exclude the receptor chimera cases where the GPCR itself is described as a chimera
        # e.g. "Muscarinic acetylcholine receptor M2 chimera"
        if "receptor" in d and "g-alpha" not in d and "guanine" not in d:
            return False
        return True
    return False


def is_nanobody(desc: str) -> bool:
    d = _lower(desc)
    if any(k in d for k in NANOBODY_KEYWORDS):
        return True
    # heuristic: Nb followed by digits (Nb35, Nb6B9, Nb80)
    if re.search(r"\bnb\d", d):
        return True
    # Camelid antibody fragment (e.g. 4LDE)
    if "camelid antibody" in d:
        return True
    return False


def is_scfv(desc: str) -> bool:
    d = _lower(desc)
    if any(k in d for k in SCFV_KEYWORDS):
        return True
    if re.search(r"\bscfv", d):
        return True
    return False


def summarise_polymers(pdb: str, entity_ids: list[str]) -> list[dict[str, Any]]:
    out = []
    for eid in entity_ids:
        pe = fetch_polymer_entity(pdb, eid)
        if pe is None:
            out.append({"entity_id": eid, "desc": "?", "seq_len": 0, "chains": "?", "note": "fetch-failed"})
            continue
        rpe = pe.get("rcsb_polymer_entity", {})
        ep = pe.get("entity_poly", {})
        desc = rpe.get("pdbx_description", "") or ""
        seq = ep.get("pdbx_seq_one_letter_code_can", "") or ""
        chains = ep.get("pdbx_strand_id", "?") or "?"
        out.append({
            "entity_id": eid,
            "desc": desc,
            "seq_len": len(seq),
            "chains": chains,
        })
    return out


def summarise_nonpolymers(pdb: str, entity_ids: list[str]) -> list[dict[str, Any]]:
    out = []
    for eid in entity_ids:
        npe = fetch_nonpolymer_entity(pdb, eid)
        if npe is None:
            continue
        desc = (npe.get("rcsb_nonpolymer_entity", {}) or {}).get("pdbx_description", "") or ""
        comp_id = ((npe.get("nonpolymer_comp", {}) or {}).get("chem_comp", {}) or {}).get("id", "") or \
            ((npe.get("rcsb_nonpolymer_entity_container_identifiers", {}) or {}).get("nonpolymer_comp_id", "")) or ""
        out.append({"entity_id": eid, "desc": desc, "comp_id": comp_id})
    return out


def classify(pdb: str, polymers: list[dict[str, Any]], nonpolymers: list[dict[str, Any]], title: str) -> tuple[str, str]:
    """Return (verified_class, note). Multiple tags separated by '+'."""
    tags: list[str] = []
    notes: list[str] = []

    # Identify non-receptor / non-fusion polymer entities
    receptor_ents = []
    other_ents = []
    for p in polymers:
        d = p["desc"]
        if is_gpcr_receptor(d) and not any(k in _lower(d) for k in ["g-alpha", "g alpha", "galpha", "guanine nucleotide"]):
            receptor_ents.append(p)
        else:
            other_ents.append(p)

    # Check α5-CT peptide
    has_a5ct = any(looks_like_alpha5_ct_peptide(p["desc"], p["seq_len"]) for p in other_ents)

    # Full Gα subunit present?
    ga_entities = [p for p in other_ents if is_g_alpha(p["desc"], p["seq_len"])]
    has_full_ga = bool(ga_entities)

    # β and γ present?
    has_beta = any(is_g_beta(p["desc"]) for p in other_ents)
    has_gamma = any(is_g_gamma(p["desc"]) for p in other_ents)

    # miniG / chimera flags on any Gα entity or in title
    title_l = _lower(title)
    mini = any(has_mini_g(p["desc"], p["seq_len"]) for p in ga_entities) or has_mini_g(title_l)
    chim = any(has_chimera(p["desc"]) for p in ga_entities) or has_chimera(title_l)
    dng = any(has_dng(p["desc"]) for p in ga_entities) or has_dng(title_l)

    # nanobody / scFv
    nb = any(is_nanobody(p["desc"]) for p in other_ents) or is_nanobody(title_l)
    scfv = any(is_scfv(p["desc"]) for p in other_ents) or is_scfv(title_l)

    if has_full_ga:
        # "heterotrimer" only if Gα + Gβ + Gγ all present; else "Gα-only"
        if has_beta and has_gamma:
            prefix = "Gα-heterotrimer"
        else:
            prefix = "Gα-only"
        if chim and mini:
            tags.append(f"{prefix}-miniG+chimera")
        elif chim:
            tags.append(f"{prefix}-chimera")
        elif mini:
            tags.append(f"{prefix}-miniG")
        else:
            tags.append(f"{prefix}-native")
        if dng:
            notes.append("dominant-negative Gα (full-length)")
        if prefix == "Gα-only":
            missing = []
            if not has_beta:
                missing.append("no Gβ")
            if not has_gamma:
                missing.append("no Gγ")
            notes.append(",".join(missing))
    elif has_a5ct:
        tags.append("Gα-α5-CT-peptide")
    # attach auxiliary tags (nanobody/scFv) if present
    has_ga_tag = any(t.startswith("Gα-") for t in tags)
    if nb:
        if has_ga_tag:
            tags.append("aux-nanobody")
        else:
            tags.append("nanobody-stabilised")
    if scfv:
        if has_ga_tag:
            # scFv16 is a canonical Gs/Gi/Go heterotrimer stabiliser — auxiliary, not primary
            tags.append("aux-scFv")
        elif not nb:
            tags.append("scFv-stabilised")

    if not tags:
        # No G-protein of any kind, no nanobody, no scFv — likely agonist-only or something else
        # Check if there's a peptide agonist
        peptide_agonists = [p for p in other_ents if p["seq_len"] > 0 and p["seq_len"] < 25 and not is_fusion(p["desc"])]
        # Check for engineered fusion (T4L, BRIL, flavodoxin) attached to receptor entity
        fusion_only = any(is_fusion(p["desc"]) for p in polymers)
        non_fusion_others = [p for p in other_ents if not is_fusion(p["desc"])]
        if not non_fusion_others:
            tags.append("agonist-only")
            if fusion_only:
                notes.append("crystallography fusion (T4L/BRIL/etc) in receptor construct")
        elif peptide_agonists:
            tags.append("agonist-only")
            notes.append(f"peptide agonist: {'; '.join(p['desc'] for p in peptide_agonists)}")
        else:
            tags.append("other")
            notes.append(f"non-fusion partners: {[p['desc'] for p in non_fusion_others]}")

    # Non-polymer ligand summary
    if nonpolymers:
        ligs = [f"{n.get('comp_id','?')}={n['desc']}" for n in nonpolymers if n["desc"]]
        if ligs:
            notes.append("ligands: " + "; ".join(ligs[:5]))

    return "+".join(tags), " | ".join(notes) if notes else ""


def entities_summary_string(polymers: list[dict[str, Any]]) -> str:
    parts = []
    for p in polymers:
        parts.append(f"[{p['entity_id']}] chains={p['chains']} len={p['seq_len']}: {p['desc']}")
    return " ; ".join(parts)


def load_reference_set() -> list[dict[str, str]]:
    with REF_CSV.open() as f:
        return list(csv.DictReader(f))


def main() -> None:
    refs = load_reference_set()
    active_rows = [r for r in refs if r["role"] == "active" and r["receptor_slug"] in CLASS_A_ACTIVE_RECEPTORS]
    if len(active_rows) != len(CLASS_A_ACTIVE_RECEPTORS):
        got = {r["receptor_slug"] for r in active_rows}
        missing = CLASS_A_ACTIVE_RECEPTORS - got
        extra = got - CLASS_A_ACTIVE_RECEPTORS
        print(f"WARN: expected {len(CLASS_A_ACTIVE_RECEPTORS)} active rows; got {len(active_rows)}. missing={missing} extra={extra}", file=sys.stderr)

    print(f"Verifying {len(active_rows)} Class A active reference PDBs...")

    output_rows = []
    verification = {"active_verifications": [], "nan_oh_inactive_probes": {}, "no_active_gpcrdb_probes": {}}

    for row in sorted(active_rows, key=lambda r: r["receptor_slug"]):
        slug = row["receptor_slug"]
        pdb = row["pdb_id"]
        current = row.get("active_stabilization_source", "") or ""
        print(f"  {slug:8s} {pdb}: fetching...", end="", flush=True)
        entry = fetch_entry(pdb)
        if entry is None:
            print(" FAIL")
            output_rows.append({
                "receptor_slug": slug, "pdb_id": pdb,
                "current_stabilization_source": current,
                "verified_stabilization_source": "unresolved",
                "matches": "",
                "notes": "entry fetch failed",
                "entities_summary": "",
            })
            continue

        title = (entry.get("struct", {}) or {}).get("title", "") or ""
        ci = entry.get("rcsb_entry_container_identifiers", {}) or {}
        poly_ids = ci.get("polymer_entity_ids", []) or []
        nonpoly_ids = ci.get("non_polymer_entity_ids", []) or []

        polymers = summarise_polymers(pdb, poly_ids)
        nonpolymers = summarise_nonpolymers(pdb, nonpoly_ids)

        verified, cls_notes = classify(pdb, polymers, nonpolymers, title)
        entities_str = entities_summary_string(polymers)

        matches = normalize_and_compare(current, verified)
        print(f" -> {verified} (was: {current!r}) [{matches}]")

        output_rows.append({
            "receptor_slug": slug,
            "pdb_id": pdb,
            "current_stabilization_source": current,
            "verified_stabilization_source": verified,
            "matches": matches,
            "notes": (title + " || " + cls_notes) if cls_notes else title,
            "entities_summary": entities_str,
        })
        verification["active_verifications"].append({
            "receptor_slug": slug,
            "pdb_id": pdb,
            "current": current,
            "verified": verified,
            "match": matches,
            "title": title,
            "polymers": polymers,
            "nonpolymers": nonpolymers,
            "notes": cls_notes,
        })

    # NaN-OH inactive replacement candidates — probe GPCRdb for alternate inactive PDBs
    print("\nProbing NaN-OH inactive-side receptors for replacement candidates...")
    for slug in NAN_OH_INACTIVE_RECEPTORS:
        # find the inactive row in refs
        inactive_rows = [r for r in refs if r["receptor_slug"] == slug and r["role"] == "inactive"]
        if not inactive_rows:
            continue
        current_inactive = inactive_rows[0]["pdb_id"]
        uniprot_slug = inactive_rows[0].get("uniprot_slug", "")
        candidates = probe_gpcrdb_inactive(slug, uniprot_slug, exclude=current_inactive)
        verification["nan_oh_inactive_probes"][slug] = {
            "current_inactive_pdb": current_inactive,
            "candidates": candidates,
        }
        print(f"  {slug}: current={current_inactive} candidates={candidates[:5]}")

    # 8-no-active receptors — probe GPCRdb for active-state entries
    print("\nProbing no-active-ref receptors for active-state candidates in GPCRdb...")
    for slug in CLASS_A_NO_ACTIVE:
        inactive_rows = [r for r in refs if r["receptor_slug"] == slug and r["role"] == "inactive"]
        uniprot_slug = inactive_rows[0].get("uniprot_slug", "") if inactive_rows else ""
        candidates = probe_gpcrdb_active(slug, uniprot_slug)
        verification["no_active_gpcrdb_probes"][slug] = {
            "uniprot_slug": uniprot_slug,
            "active_candidates": candidates,
        }
        print(f"  {slug} ({uniprot_slug}): active candidates={candidates[:5]}")

    # Write CSV
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["receptor_slug", "pdb_id", "current_stabilization_source",
                                          "verified_stabilization_source", "matches", "notes",
                                          "entities_summary"])
        w.writeheader()
        w.writerows(output_rows)
    print(f"\nWrote {OUT_CSV}")

    # Write JSON sidecar
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(verification, indent=2))
    print(f"Wrote {OUT_JSON}")

    # Distribution summary
    dist: dict[str, int] = {}
    for r in output_rows:
        dist[r["verified_stabilization_source"]] = dist.get(r["verified_stabilization_source"], 0) + 1
    print("\nVerified-class distribution:")
    for k in sorted(dist, key=lambda x: -dist[x]):
        print(f"  {dist[k]:2d}  {k}")

    # Mismatch summary
    mism = [r for r in output_rows if r["matches"] == "mismatch"]
    print(f"\nMismatches: {len(mism)}")
    for r in mism:
        print(f"  {r['receptor_slug']:8s} {r['pdb_id']}: {r['current_stabilization_source']!r} -> {r['verified_stabilization_source']!r}")


def normalize_and_compare(current: str, verified: str) -> str:
    """Compare current label against verified. Returns 'match', 'mismatch', 'missing', or 'consistent'."""
    if not current:
        return "missing-in-refs"
    c = current.strip().lower()
    v = verified.strip().lower()
    # Map current labels to normalised buckets
    #  "native"       -> Gα-heterotrimer-native
    #  "mini_g"       -> Gα-heterotrimer-miniG  (or Gα-α5-CT-peptide when appropriate — flag)
    #  "chimera"      -> Gα-heterotrimer-chimera
    #  "nanobody"     -> nanobody-stabilised
    #  "scFv"         -> scFv-stabilised
    #  "agonist_only" -> agonist-only
    #  "DVL_DEP"      -> other (Class F, non-Gα)
    current_map = {
        "native": "gα-heterotrimer-native",
        "mini_g": "gα-heterotrimer-minig",
        "chimera": "gα-heterotrimer-chimera",
        "nanobody": "nanobody-stabilised",
        "scfv": "scfv-stabilised",
        "agonist_only": "agonist-only",
        "dvl_dep": "other",
    }
    canon = current_map.get(c, c)
    if v.replace("gα-heterotrimer-minig+chimera", "gα-heterotrimer-minig+chimera") == canon:
        return "match"
    if canon in v or v.startswith(canon):
        return "match-partial"
    return "mismatch"


_GPCRDB_INDEX_CACHE: dict[str, list[dict[str, Any]]] | None = None


def _load_gpcrdb_index() -> dict[str, list[dict[str, Any]]]:
    """Fetch GPCRdb's full structure list once, index by UniProt slug."""
    global _GPCRDB_INDEX_CACHE
    if _GPCRDB_INDEX_CACHE is not None:
        return _GPCRDB_INDEX_CACHE
    data = fetch_json("https://gpcrdb.org/services/structure/", "gpcrdb_all_structures")
    idx: dict[str, list[dict[str, Any]]] = {}
    if isinstance(data, list):
        for s in data:
            if isinstance(s, dict) and s.get("protein"):
                idx.setdefault(s["protein"], []).append(s)
    _GPCRDB_INDEX_CACHE = idx
    return idx


def _pick_fields(s: dict[str, Any]) -> dict[str, Any]:
    return {
        "pdb_code": s.get("pdb_code"),
        "resolution": s.get("resolution"),
        "method": s.get("type"),
        "publication_date": s.get("publication_date"),
        "ligand_functions": [l.get("function") for l in (s.get("ligands") or []) if isinstance(l, dict)],
    }


def probe_gpcrdb_active(slug: str, uniprot_slug: str) -> list[dict[str, Any]]:
    """Return the list of active-state (or intermediate) PDBs in GPCRdb for this receptor."""
    if not uniprot_slug:
        return []
    idx = _load_gpcrdb_index()
    hits = idx.get(uniprot_slug, [])
    out = [_pick_fields(s) for s in hits if str(s.get("state", "")).lower() in ("active", "intermediate")]
    return sorted(out, key=lambda x: (x.get("publication_date") or "", x.get("resolution") or 99), reverse=True)


def probe_gpcrdb_inactive(slug: str, uniprot_slug: str, exclude: str) -> list[dict[str, Any]]:
    """Return the list of inactive PDBs in GPCRdb for this receptor, excluding the currently-used one."""
    if not uniprot_slug:
        return []
    idx = _load_gpcrdb_index()
    hits = idx.get(uniprot_slug, [])
    ex = (exclude or "").upper()
    out = [_pick_fields(s) for s in hits if str(s.get("state", "")).lower() == "inactive"
           and (s.get("pdb_code") or "").upper() != ex]
    return sorted(out, key=lambda x: (x.get("resolution") or 99, x.get("publication_date") or ""))


if __name__ == "__main__":
    main()
