# Block A: MSA-server path per backbone

Coordinator flagged before authorizing the pre-warm: *"first confirm all four backbones draw from the ColabFold MSA path — if any runs its own pipeline, the 48-sequence warm doesn't help it and the wall-time estimate is wrong for a quarter of the run."*

Findings from inspecting the four rerun templates at HEAD (2026-09-01):

| Backbone | Template | MSA server flag | Server used | Benefits from ColabFold pre-warm? |
|---|---|---|---|---|
| Boltz-2 | `qsub/rerun_boltz.sh:118` | `--use_msa_server` | ColabFold public API (`api.colabfold.com`) | **Yes** |
| OpenFold-3-preview | `qsub/rerun_of3.sh:95` | `--use-msa-server true` | ColabFold public API (`api.colabfold.com`) | **Yes** |
| Protenix v2 | `qsub/rerun_protenix.sh:103` | `--msa_server_mode protenix` | Protenix's own MSA server (separate infra) | **No** — different cache; ColabFold warm is irrelevant |
| Chai-1 | `qsub/rerun_chai.sh:108-114` | *(no MSA flag)* | None — chai-lab default is single-sequence inference | **No** — no MSA fetched at all |

## Confirmations

- Grep of `scorer/` + `qsub/` for `msa-server|use_msa_server|use-msa-server|msa_server|colabfold|mmseqs`
  hits exactly four lines: the three explicit flags above (Boltz, OF3, Protenix). Chai has
  no MSA-related invocation.
- Protenix's script comment (`rerun_protenix.sh:12`) already flags this: *"`--msa_server_mode protenix` — NOT colabfold (naming mismatch)"*.
- Chai-lab CLI default without `--use-msa-server` runs single-sequence inference (see chai-lab
  docs) — the panel currently uses that mode.

## Implication for Block A wall time

- 2 of 4 backbones (Boltz, OF3) benefit from the ColabFold pre-warm — their per-prediction
  MSA-fetch cost drops from ~4–5 min to ~1–2 min.
- 2 of 4 backbones (Protenix, Chai) are unaffected:
  - Protenix will warm its own server progressively as Block A dispatches — same "cache is a
    hidden covariate on run order" concern the pre-warm was designed to avoid, but for a
    smaller cache.
  - Chai is single-sequence — no MSA cost at all, no cache concern.
- Half the Block A prediction budget (Boltz + OF3 arms) gets the wall-time speedup; the
  Protenix + Chai halves do not.

## Recommendations

1. Proceed with the pre-warm — the Boltz + OF3 half of Block A is ~1,600 predictions × ~3-min
   savings = ~80 GPU-hours saved, easily worth ~1.5 h zero-GPU wall time.
2. When analysing Block A per-prediction wall time, stratify by backbone before comparing —
   the Protenix arm's higher mean is expected (own-server cold warm), not a bug.
3. If a symmetric pre-warm for Protenix is later desired, the same 48-sequence set could be
   POSTed to Protenix's MSA endpoint — but that's a separate script and separate authorization.
