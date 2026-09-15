# AC41 engineering: prerequisite NOT MET — and the AC40 framework caught the reason before any study ran

2026-09-15. `ac41_occupancy.py`, `test_ac41.py`. Engineering only. **No protocol, no final seeds, no
claim.** Fifth prerequisite stop in this line (AC31, AC35, AC37, AC39, AC41) against two passing claims.

## What was being prepared, and what AC39 taught that was applied in advance

The claim: an organism whose register occupancy is maintained by repair keeps that occupancy higher than
one whose occupancy is not, **with corruption absent** so AC14's integrity channel is off by construction.

Three design fixes were applied *before* measuring, from AC39's stop and AC40's framework:

- **Endpoint changed** from "ticks active" (saturated at 4096 for every live individual in AC39) to
  **mean register occupancy**, precisely to give the maintained arm headroom.
- **Criterion split**: resolvability (n ≥ 8, exact sign-flip test, p ≤ 0.01, floor 2/2ⁿ stated up front),
  headroom (checked, not assumed), effect size **in endpoint units**, stability as the impaired fraction.
- **Prediction stated in advance**: AC39's cut arm was bimodal (2 of 16 unimpaired); the same structure was
  predicted for occupancy, and a failure to appear was declared to be a falsified prediction.

## Measured, 16 individuals (seeds 0–7 × two histories), corruption absent

| check | result |
| --- | --- |
| live occupancy | min 21, mean 21, **max 21** — identical for every individual |
| cut occupancy | 11 … 18, mean 13 |
| per-individual differences | 7,7,8,8,7,7,10,10,9,9,9,9,3,3,9,9 |
| **resolvability** | n 16, p ≈ 0.0000 (floor 0.00003) → **PASSES** |
| **headroom** | maintained-arm max 21, 100% at the ceiling → **SATURATED** |
| **effect size** | median 8, requirement > 1000 → **FAILS** |
| **prediction** | impaired fraction 100% → **bimodality NOT present — FALSIFIED** |

**The prerequisite is not met and the study stops.**

## Three findings, one of which is about my own instruments

1. **The occupancy endpoint is degenerate, and the AC40 headroom check caught it before any protocol
   existed.** `register_replicas_set_total` is a structural constant for the live arm — 21 for all sixteen
   individuals — so the endpoint has neither headroom nor variance. That check was added one step ago
   *because* AC39's endpoint saturated; here it immediately rejected an endpoint I had chosen for exactly
   that reason. This is the first time in this line that a framework check has blocked a bad design
   before it consumed a study, and it is the strongest argument for building the framework.
2. **My effect-size requirement was mis-scaled to the endpoint.** I declared "median difference > 1000
   occupancy units" using a number from AC19-M's *activity* ledger, not from the occupancy endpoint. The
   measured median is 8. Declaring a requirement in endpoint units is right; declaring it in units copied
   from a different endpoint is still a mistake, and it is mine.
3. **The bimodality prediction was falsified.** AC39's cut arm had two of sixteen individuals entirely
   unimpaired; occupancy shows **no** such structure (100% impaired, differences 3–10). So the bimodality
   is a property of the *activity* endpoint, not of the repair cut. That is real, if small, knowledge, and
   it is recorded as a falsified prediction rather than quietly dropped.

## What is not established

- Nothing about an organism: no protocol, no declared final seeds, no results directory, no claim.
- Not autopoiesis, closure, or life. `SOURCES` stays empty, and a test asserts every one of these.
- The contrast itself is resolvable (p ≈ 0, live 21 vs cut 11–18) — but resolvable about a constant is
  not a study, which is why headroom had to be a separate check rather than a footnote.

## Next

Two routes, both cheap because the framework now rejects bad endpoints early:

1. **Find an occupancy-family endpoint with genuine variation** — for example the *time* the register stays
   occupied (a duration, not a level), or the number of renewals the register's occupancy forced. The
   requirement must be stated in that endpoint's own units, measured before the study declares it.
2. **Or drop occupancy and take the AC39 activity endpoint with the saturation fixed** — e.g. censored
   time-to-first-drop, which has headroom by construction because it is a duration.

Either way, the AC40 framework's four checks run first, and this study's falsified prediction is the thing
to re-test.

## Artifacts

`ac41_occupancy.py`, `test_ac41.py`, `/tmp/ac41_prerequisite.json`. Related: `AC40_CRITERION_v2.md` (whose
headroom check blocked this design), `AC39_ENGINEERING_v1.md` (the stop that prompted the split),
`AC19M_MAINTENANCE_v1.md` (the diagnosis under test).
