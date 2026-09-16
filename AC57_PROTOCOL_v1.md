# AC57 protocol v1 — the six-region order is load-bearing AND re-acquirable

Written before any final seed. Engineering (`ac57_engineering.py`) on seeds 4612–4635 (two disjoint
families), scoring on 9012–9023 — all disjoint from the final seeds 4836–4847 declared below.

## The claim

In the scaled body with a **concentrated head + graded tail** value structure, the six-position order is
**load-bearing and re-acquirable**: (1) the value-optimal order produces significantly more value than the
value-worst order; and (2) an organism that releases and re-acquires its order after a regime change
produces significantly more value than one that keeps its stale order — at a stable equilibrium.

This resolves the AC56 tension in the way AC56 itself proposed: a *partial* value spread. Concentrated
value gave load-bearing (AC55) but negligible re-acquisition; graded value (AC50) gave re-acquisition
but weak load-bearing. The concentrated head (region 0/5 = 100) keeps the load-bearing gap large, while
the graded tail (5, 4, 3, 2, 0.5) makes the *future*-critical region lowest under the old regime, so the
stale order deprioritises it and staleness is expensive.

## The world (reused, verified)

AC50's `World` mechanics: six regions × four sites, stochastic per-region stress, one-tick decay,
value-weighted production every 4 ticks, drain 2.0/tick, repair (renew) cost 5 energy resetting the
most-depleted alive site to life 64. Stress multiplier 7, reversed with the value across regimes.

- Regime A: `VALUES_A = (100, 5, 4, 3, 2, 0.5)`, `RATES_A = stress_rates() × 7` (region 0 critical).
- Regime B: `VALUES_B = reversed(VALUES_A)`, `RATES_B = reversed(RATES_A)` (region 5 critical).

Endpoint: cumulative value-weighted production over 600 ticks, under regime B.

## Declared orders (12-start climbs on scoring seeds 9012–9023)

- `OPT_A`   = `(2, 3, 4, 0, 1, 5)`  (A-optimal; stale under B)
- `OPT_B`   = `(5, 1, 2, 4, 3, 0)`  (B-optimal)
- `WORST_B` = `(2, 4, 1, 0, 3, 5)`  (B-worst)

## Arms

| arm | order |
| --- | --- |
| `optimal` | OPT_B |
| `worst` | WORST_B |
| `learner` | releases under B, re-searches (seeded climb) → held in a register and read back |
| `no_release` | OPT_A (stale under B) |
| `random` | a random permutation, seeded per individual (state-blind) |

## Seeds

- Engineering: 4612–4623 (family 1), 4624–4635 (family 2). Scoring: 9012–9023.
- **Final: 4836–4847** (12 individuals, disjoint from all of the above).

## Gates (declared before seeds)

| gate | bar |
| --- | --- |
| G1 load resolvable | sign-flip p ≤ 0.01 on (optimal − worst), n ≥ 8 |
| G2 load effect | median(optimal − worst) ≥ 6000 |
| G3 re-acq resolvable | sign-flip p ≤ 0.01 on (learner − no_release), n ≥ 8 |
| G4 re-acq effect | median(learner − no_release) ≥ 6000 |
| G5 stability | 0 dead across all arms |
| G6 horizon-robust | production@1500 / @600 in [2.4, 2.6] |
| G7 state-blind | mean(random) < mean(optimal) |
| G8 headroom | mean(worst) ≤ 0.9 × ceiling (68,700) |
| G9 register in the loop | learner's order written to a register reads back unchanged |
| G10 completeness + determinism | all 12 × 5 arms; re-run of first 2 reproduces |

Impaired fractions reported descriptively (AC50 precedent), not gated.

## Four-check (engineering, two families)

| | family 1 | family 2 |
| --- | --- | --- |
| re-acq p (OPT_B − OPT_A under B) | 0.0005 | 0.0010 |
| re-acq median | 11,958 | 13,225 |
| re-acq impaired | 0/12 | 0/12 |
| load p (OPT_B − WORST_B under B) | 0.0005 | 0.0020 |
| load median | 12,686 | 13,221 |
| dead | 0 | 0 |
| horizon @1500/@600 | 2.487 | — |
| worst / ceiling | 74.1% | — |

SOURCES (declared): ac57_order.py ac57_engineering.py ac50_heterogeneous.py ac33_search.py ac30_acquire.py ac29_register.py ac38_variance.py AC57_PROTOCOL_v1.md

## Bounds

Nothing here claims autopoiesis, closure, or life. The order is supplied (or found by a supplied search);
the register is a supplied retention mechanism. This establishes that the order structure is load-bearing
and re-acquirable — AC28's acquisition/retention goal, in the value structure that permits it.
