# AC60 results v1 — the developmental function scales: seven-region order is load-bearing and re-acquirable: FROZEN (ninth verified claim)

2026-09-15. `ac60_order.py` (finals), `ac60_engineering.py`, `ac60_results_v1/`, `audit_ac60.py`,
`replay_ac60.py`, `test_ac60.py`. All ten gates pass.

## The claim, frozen

The six-position order (9.49 bits) that AC55/AC57 froze is not an artifact of six positions. In a
seven-region scaled body (5040 orders, 12.30 bits), the order is still **load-bearing** and
**re-acquirable**, at a stable equilibrium. This is the first scale step past six — the point AC20's
rule-format budget (9 slots) begins to bind — and the properties survive it.

## Gates (final seeds 4860–4871)

| gate | result |
| --- | --- |
| G1 load resolvable | pass — p = 0.00049 (floor) |
| G2 load effect ≥ 10000 | pass — 16,788.25 |
| G3 re-acq resolvable | pass — p = 0.00049 (floor) |
| G4 re-acq effect ≥ 10000 | pass — 19,710.0 |
| G5 stability 0 dead | pass |
| G6 horizon-robust | pass — 2.485 |
| G7 state-blind | pass — random 65,748 < optimal 71,146 |
| G8 headroom | pass — worst 53,548 ≤ 0.9 × 72,300 |
| G9 register in the loop | pass — 13-bit 7-permutation round-trips |
| G10 determinism | pass — re-run exact |

## The effect, stated plainly

- Optimal arm: mean 71,146 (98.4% of ceiling 72,300).
- Worst arm: mean 53,548 (min 36,980) — the value-worst order `(5, 4, 0, 3, 2, 1, 6)` neglects region 6.
- Stale arm (OPT_A under B): mean 49,314 (min 33,498).
- Learner arm: mean 71,034 — the seeded re-search finds the B-optimal order and reads it back through
  the register.
- Load-bearing median 16,788 and re-acquisition median 19,710, both at the exact sign-flip floor
  (p = 2/2¹²), 0 dead, 0 impaired.

Both properties survive the wider domain intact — indeed slightly *larger* than at six positions, because
the concentrated head is more dominant over the longer graded tail.

## What this does and does not establish

- **Establishes**: the developmental function's two frozen properties are not an artifact of six
  positions. A 12.30-bit order is load-bearing and re-acquirable. The order structure's information
  capacity is real across scale steps, with AC20's rule-format budget as the next binding axis.
- **Does not establish**: that the *rule format* (9 slots) can express a seven-region order — the format
  widening AC20 specified is still unbuilt; nor autopoiesis, closure, or life.

## Next step

The rule format is now the binding axis: to express a seven-region order the controller needs 10 slots +
10 mask bits (AC20). The next build widens the format to C + B = 10 on both axes and re-checks the
order's expressibility — the point where the format budget, not the order structure, is the limit.

## Artifacts

`ac60_order.py`, `ac60_engineering.py`, `ac60_results_v1/`, `audit_ac60.py` (4/4 hashes, 9/9 gates
recomputed), `replay_ac60.py` (12/12 exact), `test_ac60.py` (10 tests), `AC60_PROTOCOL_v1.md`.
