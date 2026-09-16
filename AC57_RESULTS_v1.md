# AC57 results v1 — the six-region order is load-bearing AND re-acquirable: FROZEN (seventh verified claim)

2026-09-15. `ac57_order.py` (finals), `ac57_engineering.py`, `ac57_results_v1/`, `audit_ac57.py`,
`replay_ac57.py`, `test_ac57.py`. All ten gates pass.

## The claim, frozen

In the scaled body with a **concentrated head + graded tail** value structure (`VALUES_A = (100, 5, 4, 3, 2, 0.5)`),
the six-position order is **load-bearing and re-acquirable**:

1. the value-optimal order `(5, 1, 2, 4, 3, 0)` produces far more value than the value-worst order
   `(2, 4, 1, 0, 3, 5)` — median 9,057 value-units (p = 0.0020);
2. an organism that releases and re-searches after a regime A→B change produces far more value than one
   that keeps its stale order `(2, 3, 4, 0, 1, 5)` — median 9,728 value-units (p = 0.0068).

This is AC28's stated goal — acquisition and retention over the six-position order — now met, in the
value structure that permits it.

## Gates (final seeds 4836–4847)

| gate | result |
| --- | --- |
| G1 load resolvable | pass — p = 0.00195 |
| G2 load effect ≥ 6000 | pass — 9,056.75 |
| G3 re-acq resolvable | pass — p = 0.00684 |
| G4 re-acq effect ≥ 6000 | pass — 9,728.0 |
| G5 stability 0 dead | pass |
| G6 horizon-robust | pass — 2.489 |
| G7 state-blind | pass — random 63,397 < optimal 68,161 |
| G8 headroom | pass — worst 57,483 ≤ 0.9 × 68,700 |
| G9 register in the loop | pass — learner order writes and reads back |
| G10 determinism | pass — re-run exact |

## How this resolves the AC56 tension

AC56 measured that the re-acquisition benefit is negligible in the concentrated-value world, because the
deadline-scheduling balance makes the stale order already lead with the new critical region. The fix,
proposed by AC56 itself, is a **partial value spread**: the concentrated head (region 0/5 = 100) keeps
the load-bearing gap large, while the graded tail (5, 4, 3, 2, 0.5) makes the *future*-critical region
lowest under the old regime, so the stale order deprioritises it and staleness is expensive. The result
is the first world in which **both** properties hold, each resolvable on two disjoint engineering
families (re-acq 0/12 impaired on both; load 0–2/12).

## What this does and does not establish

- **Establishes**: the six-position order is load-bearing, acquirable (the learner's seeded search finds
  the optimal order), retainable (the register round-trips), and re-acquirable (re-search beats staleness
  by ~17%). The developmental-function arc's core question — is the order structure real, learnable, and
  retainable — is answered affirmatively.
- **Does not establish**: register *repair* under corruption (AC43's mechanism, not yet joined to this
  line); autopoiesis; closure; life.

## Next step

AC58 — join the maintenance line to the developmental line: put the acquired order in a register that is
*corrupted and repaired* (AC43's repair-maintained occupancy), and show the repaired register retains the
acquired function better than an unrepaired one. That is the natural bridge between the two verified
lines.

## Artifacts

`ac57_order.py`, `ac57_engineering.py`, `ac57_results_v1/`, `audit_ac57.py` (8/8 hashes, 9/9 gates
recomputed), `replay_ac57.py` (12/12 exact), `test_ac57.py` (10 tests), `AC57_PROTOCOL_v1.md`.
