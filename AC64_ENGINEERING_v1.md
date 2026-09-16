# AC64 engineering: the complementarity is bimodal — corruption's cost is a per-seed coin flip

2026-09-15. `ac64_engineering.py`, engineering prerequisite. **No protocol, no final seeds, no claim.**

## The attempt, and why it failed

AC63 identified the grace period (`URGENT`) as the control on corruption's cost and proposed freezing the
repair/re-acquisition complementarity (AC61) at URGENT = 4, with AC62's single-disruption design. AC64
built that study. The contrast (re-acquire vs repair-only, after a corruption event flips the register's
majority) did **not** resolve:

| URGENT | p | median | mean | impaired | optimal | repair-only | re-acquire |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4 | 0.06 / 0.25 | 0 | 7,446 | 0–1 | 62,734 | 55,288 | 62,734 |
| 3 | 0.19 | 0 | 4,872 | 1 | 52,970 | 48,098 | 52,970 |
| 2 | 0.25 | 0 | 4,158 | 0 | 40,438 | 36,280 | 40,438 |

The median difference is **0 at every grace period**, while the mean difference is positive. That is a
bimodal distribution, and it is fundamental, not a tuning problem.

## Why the effect is bimodal

Corruption produces a *random* permutation. Whether that random order harms the critical region is a
coin flip: with the critical region at a random position, it lands in a "caught" position on most seeds
(no loss) and a "missed" position on the rest (large loss). Re-acquisition only helps on the missed
seeds. So the paired differences are mostly zero with a heavy positive tail — median 0, positive mean.
The sign-flip test resolves a consistent shift, not a heavy tail at n = 12, so p stays above 0.01 no
matter how the grace period is set (shrinking it to make "missed" the majority degrades the world past
usefulness, as URGENT = 2 shows).

## What this closes

The arc AC61→AC64 is complete and negative in the right way:

- AC61: repair is preventive, re-acquisition curative — the complementarity is architecturally real.
- AC62: it is dynamically inert at the default grace period (corruption cheap).
- AC63: the grace period controls the *magnitude* of corruption's cost.
- AC64: but the cost is **bimodal** (a per-seed coin flip), so the complementarity's behavioural benefit
  cannot be frozen by the sign-flip gate at any usable grace period.

The complementarity is a genuine design principle whose behavioural consequence is real *on average* but
not resolvable as a consistent per-individual effect. A freeze would require deterministic corruption
(specific, not random damage) or an endpoint aggregated so the heavy tail dominates — both a change of
question, not a sharper measurement.

## Bounds

No claim. Engineering prerequisite. Not autopoiesis, closure, or life.

## Artifacts

`ac64_engineering.py`. Related: `AC61_ENGINEERING_v1.md`, `AC62_ENGINEERING_v1.md`,
`AC63_ENGINEERING_v1.md`.
