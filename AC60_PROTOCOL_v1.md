# AC60 protocol v1 — the developmental function scales: a seven-region order is load-bearing and re-acquirable

Written before any final seed. Engineering (`ac60_engineering.py`) on seeds 4612–4635 (two disjoint
families), scoring on 9012–9023 — all disjoint from the final seeds 4860–4871 declared below.

## The claim

The six-position order (9.49 bits) that AC55/AC57 froze is not an artifact of six positions. In a
seven-region scaled body (5040 orders, 12.30 bits), the order is still **load-bearing** (optimal ≫ worst)
and **re-acquirable** (release + re-search ≫ keeping the stale order), at a stable equilibrium. This is
the first scale step past six — the point AC20's rule-format budget (9 slots) begins to bind — and the
properties survive it.

## The world

AC50's `World` generalized to seven regions (`ac60_engineering.World7`): seven regions × four sites,
stochastic per-region stress, one-tick decay, value-weighted production every 4 ticks, drain 2.0/tick,
repair 5 energy. Stress multiplier 7.

- Regime A: `VALUES_A = (100, 6, 5, 4, 3, 2, 0.5)`, `RATES_A` = `(0.020, 0.016, 0.012, 0.009, 0.006, 0.004, 0.003)` × 7 (region 0 critical).
- Regime B: `VALUES_B = reversed(VALUES_A)`, `RATES_B = reversed(RATES_A)` (region 6 critical).

Endpoint: cumulative value-weighted production over 600 ticks, under regime B.

## Declared orders (8-start climbs on scoring seeds 9012–9023)

- `OPT_A`   = `(2, 4, 3, 0, 1, 5, 6)`  (A-optimal; stale under B)
- `OPT_B`   = `(2, 6, 3, 4, 5, 1, 0)`  (B-optimal)
- `WORST_B` = `(5, 4, 0, 3, 2, 1, 6)`  (B-worst)

## Arms

| arm | order |
| --- | --- |
| `optimal` | OPT_B |
| `worst` | WORST_B |
| `learner` | releases under B, re-searches (seeded climb over 7-permutations) → held in a 13-bit register and read back |
| `no_release` | OPT_A (stale under B) |
| `random` | a random 7-permutation, seeded per individual |

## Seeds

Engineering 4612–4623 / 4624–4635; scoring 9012–9023. **Final: 4860–4871** (12 individuals).

## Gates

| gate | bar |
| --- | --- |
| G1 load resolvable | p(optimal − worst) ≤ 0.01, n ≥ 8 |
| G2 load effect | median(optimal − worst) ≥ 10000 |
| G3 re-acq resolvable | p(learner − no_release) ≤ 0.01, n ≥ 8 |
| G4 re-acq effect | median(learner − no_release) ≥ 10000 |
| G5 stability | 0 dead across all arms |
| G6 horizon-robust | production@1500 / @600 in [2.4, 2.6] |
| G7 state-blind | mean(random) < mean(optimal) |
| G8 headroom | mean(worst) ≤ 0.9 × 72300 |
| G9 register | learner order round-trips through the 13-bit 7-permutation register |
| G10 completeness + determinism | all 12 × 5 arms; first 2 reproduce |

## Four-check (engineering, two families)

| | family 1 | family 2 |
| --- | --- | --- |
| load p | 0.0005 | 0.0005 |
| load median | 21,296 | 21,293 |
| re-acq p | 0.0005 | 0.0005 |
| re-acq median | 21,976 | 19,642 |
| impaired (both) | 0/12 | 0/12 |
| dead | 0 | 0 |
| horizon @1500/@600 | 2.483 | — |

SOURCES (declared): ac60_order.py ac60_engineering.py ac38_variance.py AC60_PROTOCOL_v1.md

## Bounds

Nothing here claims autopoiesis, closure, or life. The order and register are supplied mechanisms. This
establishes that the developmental function's two properties survive a seven-region domain — a scale
step, not a new mechanism.
