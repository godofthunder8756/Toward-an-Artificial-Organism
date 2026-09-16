# AC55 protocol v1 — the six-region order is load-bearing (concentrated value)

Written before any final seed. Engineering (`ac55_engineering.py`) on seeds 4612–4635 (two disjoint
families), scoring on 9012–9023 — all disjoint from the final seeds 4824–4835 declared below.

## The claim

In the scaled body (six regions, repair renewal, value-weighted production, a fixed regime with one
critical region worth ~100× the rest), the six-position order is **load-bearing**: the value-optimal
order produces significantly more value than the value-worst order, at a stable equilibrium, resolvable
across two independent seed families. This is the foundation the developmental-function arc (AC20–AC28)
lacked — evidence that the 9.49-bit order structure is dynamically consequential.

## Why concentrated value

AC54 failed to freeze the same claim with graded values (0.5…5): the effect was ~7.8%, near the noise
floor, and the world occasionally hit the ceiling. AC51 measured that the effect size is bounded by
*value concentration*, not spread. So this world concentrates the value in region 5 (100 vs 1 for the
rest), which lifts the effect to ~20% — large enough to resolve — and raises the stress multiplier to 7
so the order's priority is consistently consequential. Engineering was pre-flighted on **two** disjoint
families because AC54's scoring-seed overfit was only caught at the finals.

## The world (reused, verified)

AC50's `World` mechanics, regime B (region 5 most stressed): six regions × four sites, stochastic
per-region stress (`stress_rates()` reversed × 7), one-tick life decay, value-weighted production every
4 ticks, drain 2.0/tick, renew (repair) cost 5 energy resetting the most-depleted alive site to life 64.
`VALUES = (1, 1, 1, 1, 1, 100)`. The order is a six-permutation; the first urgent position wins the
single repair. Endpoint: cumulative value-weighted production over 600 ticks.

## Declared orders (12-start climbs on scoring seeds 9012–9023, before any final seed)

- `OPT`   = `(1, 2, 0, 5, 3, 4)`  (value-optimal)
- `WORST` = `(2, 4, 1, 0, 3, 5)`  (value-worst)

## Arms

| arm | order |
| --- | --- |
| `optimal` | OPT |
| `worst` | WORST |
| `random` | a random permutation, seeded per individual (state-blind control) |

## Seeds

- Engineering: 4612–4623 (family 1), 4624–4635 (family 2).
- Scoring: 9012–9023.
- **Final: 4824–4835** (12 individuals, disjoint from all of the above).

## Gates (declared before seeds)

| gate | bar |
| --- | --- |
| G1 resolvable | sign-flip p ≤ 0.01 on paired (optimal − worst), n ≥ 8 |
| G2 median effect | median(optimal − worst) ≥ 5000 value-units |
| G3 stability | 0 dead across all arms |
| G4 horizon-robust | production@1500 / @600 in [2.4, 2.6] |
| G5 state-blind | mean(random) < mean(optimal) |
| G6 headroom | mean(worst) ≤ 0.9 × ceiling (63000) — the contrast has room |
| G7 completeness | all 12 individuals, all 3 arms |
| G8 determinism | re-run of first 2 individuals reproduces exactly |

The impaired fraction (individuals where worst > optimal) is reported descriptively, not gated, per the
AC50 precedent: the claim is statistical (the order matters on average), not a deterministic
per-individual dominance. Engineering measured it at 0/12 (family 1) and 2/12 (family 2).

## Four-check (engineering, two families)

| | family 1 (4612–4623) | family 2 (4624–4635) |
| --- | --- | --- |
| resolvability p | 0.0005 | 0.0020 |
| median difference | 12869 | 13228 |
| impaired | 0/12 | 2/12 |
| dead | 0 | 0 |
| state-blind | random 57293 < optimal 62804 | random 59914 < optimal 62802 |
| headroom (worst / ceiling) | 73.4% | 78.4% |
| horizon @1500/@600 | 2.494 | — |

SOURCES (declared): ac55_order.py ac55_engineering.py ac50_heterogeneous.py ac33_search.py ac30_acquire.py ac38_variance.py AC55_PROTOCOL_v1.md

## Bounds

Nothing here claims acquisition, retention, autopoiesis, closure, or life. The endpoint is value-weighted
production; the order is a supplied permutation; the regime is fixed. This establishes only that the order
structure is load-bearing — the precondition for AC28's acquisition/retention build.
