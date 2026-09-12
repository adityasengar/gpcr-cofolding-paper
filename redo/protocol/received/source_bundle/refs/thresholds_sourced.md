# Motif-metric thresholds sourced from literature

**Status**: research draft — for PREREG §2b review.
**Compiled**: 2026-09-01
**Panel context**: Block A switch-test on 40 Class A GPCRs. See `refs/PREREG.md`.
**Scorer definitions**: `scorer/axes.py` (metric computations); `scorer/structure.py` (residue-model loader).

---

## Methodology and honest limitations

Literature search executed 2026-09-01 via WebFetch of primary review articles and structural databases. WebSearch was unavailable in this environment (Bedrock configuration blocks the `web_search` tool). Direct fetches of primary sources were largely blocked by publisher paywalls / IdP redirects; the two fetches that returned usable content were:

- **Zhou et al. 2019** *eLife* 8:e50279 — full PDF text extracted successfully. Paper uses **RRCS (residue-residue contact score)** methodology with the cutoff |ΔRRCS| > 0.2 for state discrimination. It does **not** publish per-pair Å thresholds distinguishing active from inactive states — that is by explicit design (§Methods: "a plateau-linear-plateau form atomic contact score" rather than distance cutoffs). Sample: 234 Class A structures.
- **Latorraca, Venkatakrishnan, Dror 2017** *Chem Rev* 117:139–155 — partial abstract-level access. One quantitative statement recovered: β2AR "TM6 rotates and swings nearly 14 Å away from the center" during activation (comparing 2RH1 vs 3SN6). This is a *displacement magnitude*, not a discriminator threshold, and is receptor-specific.

Attempts to access **Rasmussen 2011** (Nature 477:549), **Weis & Kobilka 2018** (Annu Rev Biochem 87:897), **Manglik & Kruse 2017** (Biochemistry), **Venkatakrishnan 2016** (Nature 536:484), **Trzaskowski et al. 2012** (Curr Med Chem), and **GPCRdb structure statistics** all returned either publisher-IdP redirects or unrelated PMC content (misaligned PMC IDs).

**Consequence**: the primary GPCR activation literature that IS accessible frames the active/inactive switch **qualitatively** (Y7.53 rotameric switch, ionic-lock breakage, hydrophobic-lock rearrangement) or via **contact-network metrics** (Venkatakrishnan/Dror RC scores; Zhou RRCS/ΔRRCS). Explicit numerical Å discriminators for the six scorer metrics could NOT be sourced from primary literature within this research pass.

**All six metrics therefore default to "panel-derived" calibration below.** Where a rule-of-thumb value circulates in the field (the "~7-8 Å active NPxxY OH-OH" cited in PREREG §2a as folklore), it is noted as such — but no primary paper in this fetch cited exactly that number as a discriminator.

If a fuller literature pass is possible (institutional VPN with Nature/ACS access; Google Scholar not blocked), re-running this research task will likely upgrade 1–3 metrics from "panel-derived" to "combined literature + panel."

---

## 1. NPxxY OH–OH — `d_npxxy_y558_y753_oh` (new column)

**Recommendation**: **panel-derived** threshold, target range ~7.5 Å (confidence: **LOW-MEDIUM**)
**Source**: no primary citation with a numerical Å threshold recovered in this pass. Zhou et al. 2019 (eLife 8:e50279) documents that Y7.53 loses interhelical contacts with 1.53 / 8.50 and translocates on activation but reports the change via RRCS rather than Å (verified in fetched PDF, section "Layer 3", lines 357–361). Latorraca et al. 2017 (Chem Rev 117:139) describes the rearrangement qualitatively. The "~7-8 Å" folklore threshold in PREREG §2a §2b appears to be a field rule-of-thumb without a locateable primary source in this pass.
**Justification**: The Y7.53 side-chain rotates so its OH points toward Y5.58 in the active state, forming a water-mediated H-bond network. In inactive Class A crystals Y7.53's OH is >10 Å away and points toward TM2/3. Even without a locked literature threshold, the sign and rough magnitude are consensus.
**Panel calibration plan**: compute `d_npxxy_y558_y753_oh` across the tier-1 active + tier-1 inactive references in `refs/reference_set.csv`; take the midpoint of the two distributions as the discriminator; sensitivity-sweep ±20 %.
**Panel sensitivity**: recommend testing 6.0–9.0 Å (spanning the folklore range) once panel means are known.

## 2. NPxxY CA–CA — `d_npxxy_y558_y753_ca` (existing column)

**Recommendation**: **panel-derived** threshold, ~13.5 Å (confidence: **LOW**)
**Source**: no literature threshold locateable. The scorer's own docstring in `scorer/axes.py:d_npxxy_y558_y753_ca` records that this metric was formerly the site of a critical bug — a literature OH-OH threshold (~7 Å) was misapplied to the CA-CA column (~14 Å scale), invalidating Wave 55 verdicts (`docs/AUDIT_TRAIL.md`). No literature CA-CA threshold exists to inherit.
**Justification**: CA positions of Y5.58 and Y7.53 barely move on activation relative to OH positions; the CA-CA metric captures only the rigid-body helix rearrangement, not the rotameric switch. Its discriminative power is weaker than OH-OH, which is why the OH-OH column was added as the primary channel.
**Panel calibration plan**: compute active + inactive mean/std across tier-1 crystals; midpoint threshold; ±20 % sensitivity.
**Panel sensitivity**: expect a narrow separation (Δ < 1.5 Å between state means). If separation is < 1 Å, drop this metric from the k-of-n composite and note in PREREG that CA-CA carries insufficient signal.

## 3. Y5.58 packing — `d_y558_pack_min_heavy` (existing column)

**Recommendation**: **panel-derived** threshold (confidence: **LOW**)
**Source**: no literature threshold. This metric is non-canonical — it is a scorer-defined min-heavy-atom distance from Y5.58 OH to any TM3/TM6 heavy atom within ±3 residues of anchors 3.50 and 6.30. No published review adopts this exact definition; the closest concept is the "hydrophobic lock" (I3.40–F6.44–P5.50) which Zhou 2019 refers to (eLife 8:e50279, verified fetch lines 274, 545). The hydrophobic-lock literature does not quantify a Y5.58 packing distance directly.
**Justification**: Active-state Y5.58 packs into the TM3/TM6 pocket vacated by TM6 outward rotation. The metric captures this qualitatively; its exact discriminator is empirical.
**Panel calibration plan**: compute the distribution over active + inactive tier-1 references; midpoint; ±20 % sensitivity.
**Panel sensitivity**: no prior expectation — likely 3.5–5.0 Å active vs 5.5–8.0 Å inactive based on VdW contact geometry.

## 4. DRY ionic lock — `d_dry_sidechain_r350cz_e630oe1` (existing column)

**Recommendation**: **combined** — recommended threshold **5.0 Å** (confidence: **MEDIUM**)
**Source**: no threshold from a specific primary paper was locateable in this pass, but a 5 Å cutoff is the standard structural-biology criterion for a salt-bridge / polar-contact interaction (Baker & Hubbard 1984; used throughout MD-analysis packages, GetContacts, MDTraj, PDBePISA). Rasmussen 2011 (Nature 477:549) originally described the ionic-lock breakage in the β2AR–Gs complex; Trzaskowski et al. 2012 (Curr Med Chem 19:1090) reviews DRY-motif conformational states — neither fetched successfully. Zhou 2019 (verified fetch line 363) describes "less conserved ionic lock with D(E)6.30" and its elimination on activation but does not quote an Å threshold.
**Justification**: The salt bridge R3.50 CZ–E6.30 OE1/OE2 is present (<4 Å) in inverse-agonist / apo inactive crystals of Class A receptors that preserve the DRY–E/D 6.30 pair (rhodopsin, some 5HT / dopamine receptors). It is broken (>5 Å, often >7 Å) in Gα-bound complexes. **Important caveat noted by Trzaskowski 2012 (uncorroborated in this pass) and widely reported**: some Class A receptors (β2AR, some aminergics) have a "broken lock" even in the inactive crystal state, so this metric will be a **weak** discriminator on those receptors. Panel-level performance on the 40-receptor set should confirm before dispatch.
**Panel sensitivity**: sweep 4.5–6.5 Å (the salt-bridge boundary region), ±20 %.

## 5. TM5 outward — `d_tm5_outward_r350_r558_ca` (existing column)

**Recommendation**: **panel-derived** threshold (confidence: **LOW**)
**Source**: no literature threshold locateable. The canonical TM-outward metric in the field is **R3.50 CA – R6.30 CA** (TM6 outward — Latorraca 2017 quantified as "nearly 14 Å" displacement for β2AR activation), NOT R3.50–R5.58. The scorer's `d_tm5_outward_r350_r558_ca` is a project-specific proxy for TM5 outward motion; its literature backing is thin.
**Justification**: TM5 outward is real (Zhou 2019 describes "repacking of TM5-TM6" as one of three coordinated inter-helical changes on activation, verified fetch line 387) but the specific R3.50–R5.58 CA-CA distance is not a canonical published metric. Whether this axis carries independent signal beyond TM6-outward is an empirical question.
**Panel calibration plan**: compute active/inactive distributions from tier-1 references; midpoint; ±20 %; **additionally** compute correlation with `d_tm6_r350_r630_ca` to confirm the metric is not redundant with the TM6 outward metric that is not among the five in the composite but is in the scorer output.
**Panel sensitivity**: no prior; report actual observed range.

## 6. ICL2 helicity fraction — `icl2_helical_frac` (existing column)

**Recommendation**: **panel-derived** threshold, target ~0.5 (confidence: **LOW-MEDIUM**)
**Source**: no numerical primary threshold locateable in this pass. ICL2 helicity in the ternary (agonist + receptor + Gα) complex is a well-established qualitative observation — reviewed by Weis & Kobilka 2018 Annu Rev Biochem 87:897 (fetch blocked) and Manglik & Kruse 2017 Biochemistry (fetch blocked). The PREREG §2a folklore "~0.5-0.6 typical for ternary complex" is field-consistent but not locked to a primary numeric threshold in this pass.
**Justification**: ICL2 is disordered / short in most inactive Class A crystals, becomes helical (≥ half the loop residues) on Gα engagement. The scorer computes helicity via CA(i)–CA(i+4) in a 3.8–6.4 Å envelope over a 14-residue window C-terminal to R3.50 — a project-specific approximation. The metric's numeric distribution needs to be measured on the tier-1 panel before locking a threshold.
**Panel calibration plan**: compute active + inactive distributions from tier-1 references; midpoint; ±20 %.
**Panel sensitivity**: sweep 0.35–0.65 (spanning the folklore range).

---

## Summary

**Best literature threshold available for**: **none of the six**. No primary paper with a numerical Å discriminator threshold could be sourced from the accessible fetches in this pass.

**Panel-calibration required for**: **all six metrics** — NPxxY OH-OH, NPxxY CA-CA, Y5.58 packing, DRY ionic lock, TM5 outward, ICL2 helicity.

**Weak literature backing (rule-of-thumb / folklore / standard structural criteria, cited)**:
- **DRY ionic lock**: 5 Å is the standard salt-bridge cutoff (used throughout MDAnalysis, GetContacts, PDBePISA — not attributed here to a single primary GPCR paper). MEDIUM confidence.
- **NPxxY OH-OH**: "~7-8 Å active" is field folklore consistent with the Y7.53 rotameric switch described in Rasmussen 2011 and Zhou 2019 (verified qualitatively in Zhou fetch); no numeric primary citation. LOW-MEDIUM confidence.
- **ICL2 helicity**: "~0.5" is folklore consistent with the ICL2-becomes-helical observation in Weis & Kobilka 2018 and Manglik & Kruse 2017 (unverified — fetches blocked). LOW-MEDIUM confidence.

**Contradictory reports across sources**: **DRY ionic lock** — the salt bridge is not universally present in Class A inactive crystals (β2AR, some aminergics have a "broken" lock even inactive). This means the DRY metric will discriminate cleanly for rhodopsin / 5HT / dopamine / some GPCRs but poorly for others. **Recommend reporting the DRY discriminator's per-receptor pass rate separately** in the panel-calibration output, and flagging receptors where inactive-state d_dry > 5 Å as "lock-uninformative for this receptor."

**Consequence for PREREG §2b**: mark all six threshold sources as "panel" (not "literature" or "combined"). The full ±20 % sensitivity sweep is mandatory for every metric. Consider adding a paragraph to PREREG §2a-b noting that the k-of-n composite is defined over metrics whose thresholds are panel-empirical, and pre-commit to reporting per-receptor sensitivity in the results.

**Recommend**: schedule a second literature-research pass in an environment with (a) WebSearch enabled, (b) institutional access to Nature / ACS / Annual Reviews. Highest-yield targets: Venkatakrishnan et al. 2016 Nature 536:484 (activation-pathway distance analyses), Rasmussen et al. 2011 Nature 477:549 (β2AR-Gs original), and the Manglik & Kruse 2017 Biochemistry review. Any of the three may hoist NPxxY OH-OH or DRY from panel-derived to combined.

---

## Notes for PREREG.md §2b

Copy-paste-ready markdown rows (replace the current TBD table):

```markdown
| NPxxY OH–OH | panel-midpoint (target ~7.5 Å) | active < threshold | panel (folklore ~7-8 Å; Zhou 2019 eLife 8:e50279 qualitative) | yes ±20 % (6.0–9.0 Å sweep) |
| NPxxY CA–CA | panel-midpoint (target ~13.5 Å) | active < threshold | panel (no lit threshold; see AUDIT_TRAIL.md) | yes ±20 % |
| Y5.58 pack min heavy | panel-midpoint | active < threshold | panel (no lit; scorer-defined) | yes ±20 % |
| DRY ionic lock | 5.0 Å | active > threshold | combined (5 Å salt-bridge criterion, generic; Rasmussen 2011 Nature 477:549 qualitative) | yes ±20 % (4.5–6.5 Å sweep) |
| TM5 outward | panel-midpoint | active > threshold | panel (Zhou 2019 qualitative; no R3.50-R5.58 lit threshold) | yes ±20 % |
| ICL2 helicity | panel-midpoint (target ~0.5) | active > threshold | panel (folklore ~0.5-0.6; Weis & Kobilka 2018 qualitative, unverified) | yes ±20 % (0.35–0.65 sweep) |
```

**Additional PREREG §2b language recommended**:

> All six motif-metric thresholds are panel-derived from the tier-1 active + tier-1 inactive references in `refs/reference_set.csv`. Where field-folklore ranges exist (NPxxY OH-OH ~7-8 Å; ICL2 helicity ~0.5-0.6), they informed the sensitivity-sweep range but not the lock value. The DRY ionic lock uses the standard 5.0 Å salt-bridge criterion but is flagged as receptor-specific (some Class A receptors have a broken lock in the inactive state); per-receptor DRY discrimination is reported alongside the composite in the panel-calibration section.
