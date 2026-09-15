# AC42: which endpoint can carry the claim? A survey of the quantities already measured

2026-09-15. `ac42_endpoints.py`, `test_ac42.py`. Survey, not a study: **no protocol, no final seeds, no
claim.** Its output is a shortlist, and it settles two open questions from AC39 and AC41.

## Why survey rather than reason

Two consecutive prerequisite stops failed on the **endpoint**, not the world:

- **AC39**: "ticks active" saturated — 4096 for every live individual, no headroom.
- **AC41**: "register occupancy" was a structural constant — 21 for every live individual, no variance.

Both were chosen by reasoning and rejected by measurement. `ac19.run` already returns many scalar
quantities per individual, so all of them were scored at once against the four properties a claim needs:
variance, headroom, resolution of the live-vs-cut contrast (exact sign-flip test, n = 16), and an impaired
fraction away from 100%.

## The survey (15 quantities, 16 individuals per arm, corruption absent)

| quantity | live mean | live sd | cut mean | p | impaired | usable | bimodal |
| --- | ---: | ---: | ---: | ---: | ---: | :---: | :---: |
| `ledger.spent_e` | 8778.6 | 120.2 | 5257.2 | 0.0003 | 88% | **yes** | **yes** |
| `ledger.spent_m` | 5420.6 | 127.9 | 3619.4 | 0.0018 | 88% | **yes** | **yes** |
| `ledger.memory_writes` | 2529.6 | 102.5 | 1404.5 | 0.0005 | 88% | **yes** | **yes** |
| `ledger.converted` | 1104.8 | 15.0 | 651.1 | 0.0003 | 88% | **yes** | **yes** |
| `ledger.W_birth` | 369.0 | 4.5 | 199.6 | 0.0001 | 88% | **yes** | **yes** |
| `productivity_kept` | 0.6 | 0.1 | 0.9 | 0.0001 | 12% | **yes** | **yes** (inverted) |
| `ledger.deposits` | 23.0 | 2.4 | 7.4 | 0.0000 | 100% | **yes** | no |
| `ledger.active` | 4096.0 | **0.0** | 2037.1 | 0.0001 | 88% | **no** — no headroom | yes |
| `activity` | 1.0 | **0.0** | 0.5 | 0.0001 | 88% | no — no headroom | yes |
| `register_replicas_set_total` | **21.0** | **0.0** | 13.2 | 0.0000 | 100% | no — constant | no |
| `restorations` | 7.9 | 1.1 | 6.4 | 0.377 | 88% | no — unresolved | yes |
| `productivity_moved` | 0.9 | 0.0 | 0.8 | 0.024 | 75% | no | yes |
| `relinquishments` | 0.6 | 0.5 | 0.8 | 0.500 | 0% | no | no |

**Seven usable endpoints, five of them metabolic and bimodal.** The two that failed before are rejected
by the survey's own checks: `ledger.active` for having a live sd of exactly zero (every individual pinned
at the ceiling) and `register_replicas_set_total` for being a constant.

## Two open questions settled

1. **AC41's falsified prediction is resolved, not merely refuted.** The bimodality AC39 saw in "ticks
   active" and AC41 did *not* find in occupancy is present in the **metabolic family** at exactly the
   same 88% impaired / 12% unimpaired split — `spent_e`, `spent_m`, `memory_writes`, `converted`,
   `W_birth`. So the structure belongs to the metabolism of a cut organism, not to activity as such and
   not to occupancy. The prediction was wrong about *where*, right about *whether*.
2. **AC42 gives the next study a shortlist** with an explicit effect size in each endpoint's own units:
   median differences of 4218 (`spent_e`), 2353 (`spent_m`), 1390 (`memory_writes`), 543 (`converted`),
   208 (`W_birth`). No requirement needs to be copied from another ledger, which was AC41's specific
   error.

## One quantity to interpret rather than use

`productivity_kept` is the reverse signal — the *cut* arm scores higher (0.9 vs 0.6), impaired 12%. It is
flagged usable by the mechanical checks because the contrast resolves, but a reversed direction means it
must be interpreted before it is used, and no claim should rest on it without that. Recorded so it is not
mistaken for a candidate.

## What this does and does not establish

- **Establishes**: a shortlist of endpoints carrying variance, headroom and resolution; the rejection of
  the two that failed before; and where AC39's bimodality actually lives.
- **Does not establish** any claim about an organism. No protocol, no declared seeds, no results
  directory, no arm comparison beyond the survey's contrast checks. Not autopoiesis, closure, or life;
  the quantities are spending, births, conversions and writes.
- **Nothing is frozen**, and a test asserts it.

## Next

The study the survey unblocks: declare `ledger.W_birth` (or `converted`) as the endpoint, with its
median difference requirement in *its own* units, the split criterion from AC40, corruption absent so
AC14's channel is off by construction, n ≥ 8, and AC39's surviving prediction (a bimodal metabolic
response) stated in advance. The survey says the endpoint will have variance and headroom; the framework
then checks it before a protocol exists.

## Artifacts

`ac42_endpoints.py`, `test_ac42.py`, `/tmp/ac42_survey.json`. Related: `AC41_ENGINEERING_v1.md` (the stop
this answers), `AC39_ENGINEERING_v1.md` (the prediction this locates), `AC40_CRITERION_v2.md` (the checks
this applies), `AC19M_MAINTENANCE_v1.md` (the diagnosis underneath).
