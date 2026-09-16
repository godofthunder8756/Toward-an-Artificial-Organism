# AC54 protocol v1 — the six-region order is load-bearing

Written before any final seed. Engineering (`ac54_engineering.py`) on seeds 4612–4623, scoring on
9012–9023 — both disjoint from the final seeds 4812–4823 declared below.

## The claim

In the scaled body (six regions, repair renewal, value-weighted production, a fixed stress/value
regime), the six-position order is **load-bearing**: the value-optimal order produces significantly
more value-weighted production than the value-worst order, at a stable equilibrium, graded and
resolvable. This is the foundation the developmental-function arc (AC20–AC28) lacked — evidence that
the 9.49-bit order structure is not merely combinatorially real but dynamically consequential.

## The world (reused, verified)

AC50's `World` mechanics, fixed to regime B (region 5 most valuable): six regions × four sites,
stochastic per-region stress (`RATES_B`, `STRESS_MULTIPLIER` = 3), one-tick life decay, value-weighted
production every `PRODUCTION_PERIOD` = 4 ticks (`VALUES_B` = (0.5, 1, 2, 3, 4, 5)), drain 2.0/tick,
renew (repair) cost 5 energy resetting the most-depleted alive site to life 64. The order is a
permutation of six positions; the first position whose region is urgent wins that tick's single repair.

Endpoint: cumulative value-weighted production over `TICKS` = 600 (horizon-robust, like AC43's ledger
totals).

## Declared orders (24-start climbs on scoring seeds 9012–9023, before any final seed)

- `OPT`   = `(4, 2, 5, 3, 1, 0)`  (value-optimal)
- `WORST` = `(2, 1, 3, 0, 5, 4)`  (value-worst)

## Arms

| arm | order |
| --- | --- |
| `optimal` | OPT |
| `worst` | WORST |
| `random` | a random permutation, seeded per individual (state-blind control) |

## Seeds

- Engineering: 4612–4623 (four-check, above).
- Scoring: 9012–9023 (finding OPT/WORST and per-individual scoring).
- **Final: 4812–4823** (12 individuals, disjoint from both).

## Gates (declared before seeds)

| gate | bar |
| --- | --- |
| G1 resolvable | sign-flip p ≤ 0.01 on paired (optimal − worst), n ≥ 8 |
| G2 median effect | median(optimal − worst) ≥ 500 value-units |
| G3 stability | 0 dead across all arms |
| G4 horizon-robust | production@1500 / @600 in [2.4, 2.6] (steady state = 2.50) |
| G5 consistency | 0% impaired (optimal ≥ worst for every individual) |
| G6 state-blind | mean(random) < mean(optimal) |
| G7 headroom | optimal arm not pinned: 0 individuals at the ceiling (9300) |
| G8 completeness + determinism | all 12 individuals, all 3 arms; re-run of first 2 reproduces exactly |

## Four-check (engineering, seeds 4612–4623)

- Resolvability: p = 0.0009766 at n = 12 (floor 2/2¹² = 0.000488) — **resolved**.
- Effect size: median difference 810.0, mean 903.2 value-units (endpoint units, not a ratio).
- Stability: impaired 0.0; per-individual differences {0.0, 67.5, 239.5, 270.0, 472.5, 810.0, 810.0,
  877.5, 1620.5, 1890.0, 1890.0, 1890.5}; 0 dead.
- Headroom: ceiling 9300 (all 24 sites alive every tick); optimal arm at 96.9% of ceiling (varies,
  not pinned), worst at 87.2%; the median difference (810) exceeds the remaining headroom (290), so
  the endpoint shows the advantage without ceiling compression.

SOURCES (declared): ac54_order.py ac54_engineering.py ac50_heterogeneous.py ac33_search.py ac30_acquire.py ac38_variance.py AC54_PROTOCOL_v1.md

## Bounds

Nothing here claims acquisition, retention, autopoiesis, closure, or life. The endpoint is value-weighted
production; the order is a supplied permutation; the regime is fixed. AC28's acquisition/retention
remains unbuilt; this establishes only that the order structure is load-bearing.
