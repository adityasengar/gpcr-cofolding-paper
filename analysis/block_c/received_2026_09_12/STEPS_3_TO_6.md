# Steps 3–6 on rows.tier3.v2.csv — cluster unit, continuous readout, seeds, opsins

**GENERATED** by `mine_steps3to6.py`. Do not hand-edit; re-run it.

Rows **40,800**; backbones {'boltz': 10200, 'protenix': 10200, 'chai': 10200, 'of3': 10200}; seeds **5**.

Every table is **per backbone**. Nothing here is pooled across backbones, because this project has twice found that pooling across disagreeing backbones produces a statement about one backbone in the clothes of a statement about a class (`DECISIONS.md` F-13(c); the Class B 9 Å split).

The unit is the **paralog cluster**. Rows collapse `row → (receptor, arm, role, backbone, seed) → receptor → cluster`, so five seeds of one receptor cannot outvote one seed of another, and a cluster with four receptors does not outweigh one with a single receptor. Intervals are **cluster bootstraps**, 2,000 resamples, paired within cluster.

## Step 4 precondition — is the continuous readout usable?

- receptors with it **complete**: **28**
- receptors with it **wholly absent**: **10** — ACM1, ADA2A, ADRB1, B1B1U5, CCKAR, DRD3, EDNRA, HRH3, OPSD, OX2R
- receptors with it **partial**: **0** — none
- receptors whose completeness **differs by ligand role**: **0**

**The missingness is receptor-wise, not role-wise or arm-wise.** That is the question that mattered: a readout missing asymmetrically across roles would have biased every ligand-class comparison, the way the opsin exclusion does. It does not. Switching to the continuous readout shrinks the PANEL and leaves the within-receptor design balanced.


## Step 6 — the opsins, handled explicitly

- `B1B1U5` and `OPSD`: **800 rows**, roles {'full_agonist': 800}.
- They carry an **empty `receptor_slug`** and an empty `receptor_class`, and `A_RECEPTOR_SLUG_MISSING` — the flag that exists to mark exactly this — is **empty on all of them**. A flag that vouches for the data and does not fire is Block A's `matches_claim_sheet` defect in another costume.
- **Every opsin row is `full_agonist`.** Dropping them for an empty class, as the first-look table did, removes agonist observations only — so any agonist-versus-antagonist comparison is then drawn on a population the other levels do not share. Both variants below are therefore reported.


## Variant: OPSINS EXCLUDED FROM EVERY ROLE (comparison-safe)

Rows retained **40,000** of 40,800.


### binary predicate — fraction active

clusters contributing: **18**, MDE = 1.218/sqrt(k) = **0.287**


| role | backbone | k | apo | cognate | shift | 95% CI (cluster boot) |
|---|---|---:|---:|---:|---:|---|
| full_agonist | boltz | 18 | 0.112 | 0.896 | **+0.785** | [+0.628, +0.911] |
| full_agonist | chai | 18 | 0.294 | 0.637 | **+0.343** | [+0.161, +0.537] |
| full_agonist | of3 | 18 | 0.168 | 0.768 | **+0.599** | [+0.472, +0.715] |
| full_agonist | protenix | 18 | 0.046 | 0.968 | **+0.922** | [+0.863, +0.977] |
| neutral_antagonist | boltz | 15 | 0.068 | 0.870 | **+0.802** | [+0.686, +0.903] |
| neutral_antagonist | chai | 15 | 0.324 | 0.642 | **+0.318** | [+0.119, +0.539] |
| neutral_antagonist | of3 | 15 | 0.120 | 0.774 | **+0.654** | [+0.503, +0.789] |
| neutral_antagonist | protenix | 15 | 0.011 | 0.989 | **+0.978** | [+0.953, +0.996] |
| decoy_lig | boltz | 18 | 0.075 | 0.834 | **+0.759** | [+0.643, +0.867] |
| decoy_lig | chai | 18 | 0.243 | 0.638 | **+0.395** | [+0.207, +0.593] |
| decoy_lig | of3 | 18 | 0.124 | 0.728 | **+0.604** | [+0.463, +0.733] |
| decoy_lig | protenix | 18 | 0.015 | 0.974 | **+0.959** | [+0.910, +1.000] |


### continuous readout — Angstrom, + = nearer active

clusters contributing: **18**, MDE = 1.218/sqrt(k) = **0.287**


| role | backbone | k | apo | cognate | shift | 95% CI (cluster boot) |
|---|---|---:|---:|---:|---:|---|
| full_agonist | boltz | 18 | -0.057 | 0.558 | **+0.615** | [+0.441, +0.792] |
| full_agonist | chai | 18 | -0.035 | 0.234 | **+0.269** | [+0.116, +0.481] |
| full_agonist | of3 | 18 | 0.045 | 0.401 | **+0.356** | [+0.256, +0.457] |
| full_agonist | protenix | 18 | -0.081 | 0.559 | **+0.640** | [+0.457, +0.848] |
| neutral_antagonist | boltz | 14 | -0.401 | 0.199 | **+0.601** | [+0.457, +0.737] |
| neutral_antagonist | chai | 14 | -0.193 | 0.114 | **+0.306** | [+0.107, +0.548] |
| neutral_antagonist | of3 | 14 | -0.217 | 0.192 | **+0.409** | [+0.261, +0.590] |
| neutral_antagonist | protenix | 14 | -0.350 | 0.381 | **+0.731** | [+0.498, +0.982] |
| decoy_lig | boltz | 18 | -0.231 | 0.366 | **+0.597** | [+0.471, +0.727] |
| decoy_lig | chai | 18 | -0.127 | 0.176 | **+0.303** | [+0.150, +0.505] |
| decoy_lig | of3 | 18 | -0.117 | 0.289 | **+0.406** | [+0.275, +0.557] |
| decoy_lig | protenix | 18 | -0.244 | 0.490 | **+0.734** | [+0.529, +0.944] |


## Variant: OPSINS INCLUDED, identity recovered from input_path

Rows retained **40,800** of 40,800.


### binary predicate — fraction active

clusters contributing: **18**, MDE = 1.218/sqrt(k) = **0.287**


| role | backbone | k | apo | cognate | shift | 95% CI (cluster boot) |
|---|---|---:|---:|---:|---:|---|
| full_agonist | boltz | 18 | 0.112 | 0.896 | **+0.785** | [+0.628, +0.911] |
| full_agonist | chai | 18 | 0.294 | 0.637 | **+0.343** | [+0.161, +0.537] |
| full_agonist | of3 | 18 | 0.168 | 0.768 | **+0.599** | [+0.472, +0.715] |
| full_agonist | protenix | 18 | 0.046 | 0.968 | **+0.922** | [+0.863, +0.977] |
| neutral_antagonist | boltz | 15 | 0.068 | 0.870 | **+0.802** | [+0.686, +0.903] |
| neutral_antagonist | chai | 15 | 0.324 | 0.642 | **+0.318** | [+0.119, +0.539] |
| neutral_antagonist | of3 | 15 | 0.120 | 0.774 | **+0.654** | [+0.503, +0.789] |
| neutral_antagonist | protenix | 15 | 0.011 | 0.989 | **+0.978** | [+0.953, +0.996] |
| decoy_lig | boltz | 18 | 0.075 | 0.834 | **+0.759** | [+0.643, +0.867] |
| decoy_lig | chai | 18 | 0.243 | 0.638 | **+0.395** | [+0.207, +0.593] |
| decoy_lig | of3 | 18 | 0.124 | 0.728 | **+0.604** | [+0.463, +0.733] |
| decoy_lig | protenix | 18 | 0.015 | 0.974 | **+0.959** | [+0.910, +1.000] |


### continuous readout — Angstrom, + = nearer active

clusters contributing: **18**, MDE = 1.218/sqrt(k) = **0.287**


| role | backbone | k | apo | cognate | shift | 95% CI (cluster boot) |
|---|---|---:|---:|---:|---:|---|
| full_agonist | boltz | 18 | -0.057 | 0.558 | **+0.615** | [+0.441, +0.792] |
| full_agonist | chai | 18 | -0.035 | 0.234 | **+0.269** | [+0.116, +0.481] |
| full_agonist | of3 | 18 | 0.045 | 0.401 | **+0.356** | [+0.256, +0.457] |
| full_agonist | protenix | 18 | -0.081 | 0.559 | **+0.640** | [+0.457, +0.848] |
| neutral_antagonist | boltz | 14 | -0.401 | 0.199 | **+0.601** | [+0.457, +0.737] |
| neutral_antagonist | chai | 14 | -0.193 | 0.114 | **+0.306** | [+0.107, +0.548] |
| neutral_antagonist | of3 | 14 | -0.217 | 0.192 | **+0.409** | [+0.261, +0.590] |
| neutral_antagonist | protenix | 14 | -0.350 | 0.381 | **+0.731** | [+0.498, +0.982] |
| decoy_lig | boltz | 18 | -0.231 | 0.366 | **+0.597** | [+0.471, +0.727] |
| decoy_lig | chai | 18 | -0.127 | 0.176 | **+0.303** | [+0.150, +0.505] |
| decoy_lig | of3 | 18 | -0.117 | 0.289 | **+0.406** | [+0.275, +0.557] |
| decoy_lig | protenix | 18 | -0.244 | 0.490 | **+0.734** | [+0.529, +0.944] |


## The ligand-class question, on a MATCHED cluster panel

The role tables above run on different cluster counts (18 / 15 / 18), so they cannot be compared with each other. These restrict to clusters where **all three roles are observed** at that (arm, backbone), and pair within cluster.


### binary predicate

| arm | backbone | k | contrast | level A | level B | difference | 95% CI |
|---|---|---:|---|---:|---:|---:|---|
| apo | boltz | 15 | agonist − antagonist | 0.068 | 0.134 | +0.066 **| [+0.002, +0.158] |
| apo | boltz | 15 | antagonist − decoy | 0.090 | 0.068 | -0.021 **| [-0.059, -0.000] |
| apo | chai | 15 | agonist − antagonist | 0.324 | 0.353 | +0.029 | [-0.045, +0.107] |
| apo | chai | 15 | antagonist − decoy | 0.291 | 0.324 | +0.033 | [+0.000, +0.088] |
| apo | of3 | 15 | agonist − antagonist | 0.120 | 0.174 | +0.054 **| [+0.007, +0.103] |
| apo | of3 | 15 | antagonist − decoy | 0.126 | 0.120 | -0.006 | [-0.032, +0.016] |
| apo | protenix | 15 | agonist − antagonist | 0.011 | 0.055 | +0.044 **| [+0.005, +0.096] |
| apo | protenix | 15 | antagonist − decoy | 0.018 | 0.011 | -0.008 | [-0.023, +0.000] |
| cognate | boltz | 15 | agonist − antagonist | 0.870 | 0.920 | +0.049 | [-0.025, +0.131] |
| cognate | boltz | 15 | antagonist − decoy | 0.840 | 0.870 | +0.031 | [-0.027, +0.093] |
| cognate | chai | 15 | agonist − antagonist | 0.642 | 0.625 | -0.017 | [-0.068, +0.020] |
| cognate | chai | 15 | antagonist − decoy | 0.628 | 0.642 | +0.014 | [-0.022, +0.067] |
| cognate | of3 | 15 | agonist − antagonist | 0.774 | 0.817 | +0.043 | [-0.040, +0.134] |
| cognate | of3 | 15 | antagonist − decoy | 0.767 | 0.774 | +0.007 | [-0.037, +0.062] |
| cognate | protenix | 15 | agonist − antagonist | 0.989 | 0.961 | -0.028 | [-0.080, +0.012] |
| cognate | protenix | 15 | antagonist − decoy | 0.969 | 0.989 | +0.020 | [-0.014, +0.073] |


### continuous readout

| arm | backbone | k | contrast | level A | level B | difference | 95% CI |
|---|---|---:|---|---:|---:|---:|---|
| apo | boltz | 14 | agonist − antagonist | -0.401 | -0.120 | +0.281 **| [+0.144, +0.419] |
| apo | boltz | 14 | antagonist − decoy | -0.289 | -0.401 | -0.112 **| [-0.182, -0.053] |
| apo | chai | 14 | agonist − antagonist | -0.193 | -0.061 | +0.132 **| [+0.055, +0.206] |
| apo | chai | 14 | antagonist − decoy | -0.145 | -0.193 | -0.047 **| [-0.089, -0.004] |
| apo | of3 | 14 | agonist − antagonist | -0.217 | 0.036 | +0.253 **| [+0.108, +0.422] |
| apo | of3 | 14 | antagonist − decoy | -0.158 | -0.217 | -0.059 **| [-0.135, -0.001] |
| apo | protenix | 14 | agonist − antagonist | -0.350 | -0.161 | +0.189 **| [+0.098, +0.290] |
| apo | protenix | 14 | antagonist − decoy | -0.301 | -0.350 | -0.049 **| [-0.094, -0.004] |
| cognate | boltz | 14 | agonist − antagonist | 0.199 | 0.534 | +0.335 **| [+0.198, +0.495] |
| cognate | boltz | 14 | antagonist − decoy | 0.310 | 0.199 | -0.111 **| [-0.192, -0.036] |
| cognate | chai | 14 | agonist − antagonist | 0.114 | 0.214 | +0.100 **| [+0.023, +0.181] |
| cognate | chai | 14 | antagonist − decoy | 0.168 | 0.114 | -0.054 **| [-0.100, -0.013] |
| cognate | of3 | 14 | agonist − antagonist | 0.192 | 0.396 | +0.204 **| [+0.068, +0.377] |
| cognate | of3 | 14 | antagonist − decoy | 0.262 | 0.192 | -0.070 **| [-0.149, -0.014] |
| cognate | protenix | 14 | agonist − antagonist | 0.381 | 0.515 | +0.135 **| [+0.007, +0.250] |
| cognate | protenix | 14 | antagonist − decoy | 0.431 | 0.381 | -0.050 | [-0.154, +0.077] |

`**` marks an interval excluding zero.


## Step 5 — seeds

- design cells (receptor × arm × role × backbone): **712**, **5 seeds** each
- cells where every seed gives the SAME cell mean: **524 (73.6%)**
- mean seed-to-seed spread within a cell: **0.083**, max **1.000**

Seeds are collapsed **inside the receptor** before the cluster mean throughout this document, so five seeds of one receptor cannot outvote one seed of another. The spread above is what that collapsing absorbs.


## The G4 off-site confound — and whether the ligand result survives it

Off-site is `distance_A > 15` Å, the G4 gate's own threshold. In the apo arm the rate is severely **role-asymmetric**:

| apo role | n | off-site |
|---|---:|---:|
| full_agonist | 7,000 | **29.30%** |
| neutral_antagonist | 5,800 | **1.62%** |
| decoy_lig | 7,200 | **12.25%** |

So the apo agonist−antagonist contrast compares a population where roughly **a third of agonist rows have no agonist in the pocket** against one where almost every antagonist row does. If C7 were an empty-pocket artefact, restricting to on-site rows should collapse it.

**It does not.** Continuous readout, apo, agonist − antagonist, cluster unit:

| filter | backbone | k | antagonist | agonist | difference | 95% CI |
|---|---|---:|---:|---:|---:|---|
| all rows | boltz | 14 | -0.401 | -0.120 | **+0.281** | [+0.146, +0.413] |
| all rows | chai | 14 | -0.193 | -0.061 | **+0.132** | [+0.053, +0.209] |
| all rows | of3 | 14 | -0.217 | 0.036 | **+0.253** | [+0.108, +0.412] |
| all rows | protenix | 14 | -0.350 | -0.161 | **+0.189** | [+0.093, +0.292] |
| on-site only | boltz | 11 | -0.359 | -0.056 | **+0.303** | [+0.175, +0.450] |
| on-site only | chai | 10 | -0.089 | 0.021 | **+0.110** | [+0.042, +0.180] |
| on-site only | of3 | 11 | -0.177 | 0.060 | **+0.237** | [+0.057, +0.443] |
| on-site only | protenix | 10 | -0.327 | -0.178 | **+0.149** | [+0.090, +0.200] |

**All four backbones still exclude zero, and the magnitudes barely move** — no systematic direction. The restriction costs clusters (14 → 10–11), because receptors that are 100% off-site leave entirely, which is why the intervals widen slightly. **The off-site confound does not explain the ligand effect.**


## The two instruments, compared unit-free

| instrument | backbone | partner Δ | ligand Δ | between-cluster SD | partner/SD | **ligand as % of partner** |
|---|---|---:|---:|---:|---:|---:|
| binary | boltz | +0.785 | +0.066 | 0.205 | 3.83 | **8.4%** |
| binary | chai | +0.343 | +0.029 | 0.421 | 0.81 | **8.4%** |
| binary | of3 | +0.599 | +0.054 | 0.194 | 3.09 | **9.0%** |
| binary | protenix | +0.922 | +0.044 | 0.073 | 12.60 | **4.8%** |
| continuous | boltz | +0.615 | +0.281 | 0.541 | 1.14 | **45.7%** |
| continuous | chai | +0.269 | +0.132 | 0.604 | 0.45 | **49.1%** |
| continuous | of3 | +0.356 | +0.253 | 0.503 | 0.71 | **71.2%** |
| continuous | protenix | +0.640 | +0.189 | 0.487 | 1.31 | **29.5%** |

**The ligand effect as a share of the partner effect changes
5.5–7.9× between the two instruments, PAIRED within
backbone** — 4.8–9.0% on the binary predicate against
29.5–71.2% on the continuous readout. The pairing matters: taking
the smallest binary share against the largest continuous one spans
3–15×, which mixes two different backbones and
**makes a strikingly consistent result look erratic**. Four independent backbones
agreeing to within 5.5–7.9× is the stronger statement. The partner effect is the
denominator of both shares, so this is unit-free; comparing the raw Δs is not,
because one is a change in fraction-active and the other is Ångström.

**And the binary predicate does something worse than compress small effects — it
inflates the apparent differences BETWEEN backbones.** Between-cluster SD in the apo
arm runs **0.073–0.421** on the binary predicate against
**0.487–0.604** on the continuous readout. Standardised by its own SD,
the partner effect spans **15.5× across backbones on the binary
instrument against 3.0× on the continuous one** — roughly a
5-fold inflation, driven by Protenix, whose denominator collapses because it is pinned near
0.01 apo and 0.99 cognate.

**It does NOT reorder them.** Ranked by standardised partner effect the order is
`protenix > boltz > of3 > chai` on **both** readouts, identically. So the defensible
claim is inflation of the spread, not scrambling of the ranking — narrower, and a
referee cannot push back on it.

**What survives the instrument change intact: sign, direction AND significance.**
All **24** partner contrasts — 3 roles × 4 backbones × 2 readouts — exclude zero.
Not one includes it. Chai is the weakest backbone on both instruments (0.81 SD binary,
0.45 SD continuous) and its intervals still exclude zero on both.


## What is NOT settled here

- **Modality stays confounded with receptor identity.** Every peptide-ligand row is a peptide-family receptor, so this file cannot separate *peptide ligand* from *peptide receptor*. That needs a within-receptor contrast, which is what `D-2026-09-12-f`'s T3 tier exists to supply.
- **The continuous readout costs panel, not balance.** 10 receptors lose it entirely: ACM1, ADA2A, ADRB1, B1B1U5, CCKAR, DRD3, EDNRA, HRH3, OPSD, OX2R.
- Nothing here calibrates the instrument. The binary predicate uses the thresholds **as carried in the file**, one of which is inherited rather than derived — that is the measurement pass, and it has not run.
