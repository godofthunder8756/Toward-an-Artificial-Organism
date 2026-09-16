# AC54 results v1 — the six-region order is load-bearing: FAILED to freeze (G1, G5, G7)

2026-09-15. `ac54_order.py` (finals), `ac54_engineering.py`, `ac54_results_v1/`, `audit_ac54.py`,
`replay_ac54.py`, `test_ac54.py`. A frozen study whose gates **failed** on fresh seeds. Recorded, not
retracted.

## What was attempted

The claim from `AC54_PROTOCOL_v1.md`: in the scaled body (six regions, repair renewal, value-weighted
production, a fixed regime), the value-optimal order produces significantly more value than the
value-worst order — the 9.49-bit order structure is dynamically consequential, not merely combinatorially
real.

Engineering (seeds 4612–4623) looked clean: p = 0.0009766, median difference 810, 0 dead, 0 impaired,
horizon ratio 2.489.

## What the final seeds said

Final seeds 4812–4823 (disjoint from engineering and scoring):

| gate | result |
| --- | --- |
| G1 resolvable | **FAIL** — p = 0.0366 (bar 0.01) |
| G2 median effect ≥ 500 | pass — 742.5 |
| G3 stability 0 dead | pass |
| G4 horizon-robust | pass — 2.489 |
| G5 consistency 0 impaired | **FAIL** — 3/12 impaired |
| G6 state-blind | pass |
| G7 headroom | **FAIL** — some individuals at the ceiling (9300) |
| G8 determinism | pass |

The three impaired individuals are the tell: on seeds 4813, 4816, 4822 the declared WORST order
produced *more* than the declared OPT — twice it hit the ceiling (9300, all sites alive) while OPT
scored ~8200. The OPT/WORST orders were found by climb on scoring seeds 9012–9023 and are **overfit to
that family**; on fresh seeds they sometimes reverse.

## Diagnosis — why it failed, and it is not mysterious

1. **The effect is small relative to seed noise.** Mean difference 641 value-units on a worst-arm mean
   of 8186 is ~7.8%, while seed-to-seed variation spans hundreds of units (worst arm 6870–9300). The
   signal is real but sits near the noise floor at n = 12.
2. **The world is occasionally too generous.** When a seed's stress draws lightly, the single
   repair-per-tick is enough to keep every site alive under *any* order, so the order is irrelevant and
   the arm hits the ceiling (9300). That is AC40's headroom failure in its AC39 form: saturation
   compresses the very difference the claim needs.

Both point the same way: the endpoint and the value spread are not yet demanding enough to make the
order's priority consistently load-bearing across seed families.

## What this does and does not establish

- **Establishes (negatively):** the six-region order is *not yet* robustly load-bearing in this
  configuration — the engineering four-check did not generalize, and the freeze is refused. The order
  matters on average (G2, G6 pass) but not per-individual across fresh seeds.
- **Establishes (method):** the discipline worked as designed — a clean engineering pre-flight that
  nonetheless overfits its seed family is caught by the fresh final seeds, before any claim is made.
- **Does not establish:** any claim that the order is load-bearing; not autopoiesis, closure, or life.

## The fix (next iteration)

Per AC51, the effect size is bounded by **value concentration**, not spread. The next build should (1)
concentrate the values (one critical region ~100× the rest, lifting the effect toward AC51's ~38% from
~7.8%) and (2) make the world more consistently demanding (raise stress/drain so the ceiling is rarely
reached), then re-run the AC40 four-check on *two* disjoint engineering seed families before any
protocol.

## Artifacts

`ac54_order.py`, `ac54_engineering.py`, `ac54_results_v1/`, `audit_ac54.py` (7/7 hashes, gates
recomputed), `replay_ac54.py` (12/12 exact), `test_ac54.py` (10 tests, gates pinned), `AC54_PROTOCOL_v1.md`.
