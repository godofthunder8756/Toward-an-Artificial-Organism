# AC55 results v1 — the six-region order is load-bearing: FROZEN (sixth verified claim)

2026-09-15. `ac55_order.py` (finals), `ac55_engineering.py`, `ac55_results_v1/`, `audit_ac55.py`,
`replay_ac55.py`, `test_ac55.py`. All eight gates pass.

## The claim, frozen

In the scaled body (six regions, repair renewal, value-weighted production, one critical region worth
~100× the rest, stress multiplier 7), the six-position order is **load-bearing**: the value-optimal
order `(1, 2, 0, 5, 3, 4)` produces significantly more value-weighted production than the value-worst
order `(2, 4, 1, 0, 3, 5)`, at a stable equilibrium, resolvable and large.

This is the foundation the developmental-function arc (AC20–AC28) lacked: the 9.49-bit order structure
is not merely combinatorially real — it is dynamically consequential.

## Gates (final seeds 4824–4835)

| gate | result |
| --- | --- |
| G1 resolvable | pass — p = 0.0078 (bar 0.01), n = 12 |
| G2 median effect ≥ 5000 | pass — 13,982.5 value-units |
| G3 stability 0 dead | pass |
| G4 horizon-robust | pass — 2.495 (steady state 2.50) |
| G5 state-blind | pass — random 58,214 < optimal 62,836 |
| G6 headroom | pass — worst 47,244 ≤ 0.9 × 63,000 |
| G7 completeness | pass — 12 individuals × 3 arms |
| G8 determinism | pass — re-run exact |

## The effect, honestly stated

- Optimal arm: mean 62,836 (min 62,631, max 63,000 = ceiling).
- Worst arm: mean 47,244 (min 29,300, max 63,000).
- Mean difference 15,591, median 13,982 — the optimal order retains ~33% more value than the worst.
- **Impaired 3/12** (descriptive, not a gate): one seed (4826) drew stress so lightly that all three
  arms hit the ceiling — the order was irrelevant; two seeds (4827, 4835) are near-ceiling ties where
  the worst order hit 63,000 while the optimal scored 62,861 and 62,984. The claim is statistical, not
  deterministic per-individual, and the resolvability gate (p = 0.0078) is the honest bar it clears —
  closer to it than the engineering families (0.0005, 0.0020) predicted, because the final family is
  noisier.

## Why this succeeded where AC54 failed

AC54 froze the same claim with graded values and a stress multiplier of 3; it failed (p = 0.0366, 3/12
impaired, ceiling-pinned). Two changes, both specified by AC54's own diagnosis: **concentrate the value**
(AC51's lever — one region 100× the rest lifts the effect from ~7.8% to ~33%) and **raise the stress**
(multiplier 7 so the order's priority is consistently consequential, eliminating the light-draw seeds
that made AC54's order irrelevant). And the engineering pre-flight ran on **two disjoint seed families**
so a scoring-seed overfit was caught before any protocol — the exact failure mode that took AC54 down at
its finals.

## What this does and does not establish

- **Establishes**: the six-position order is load-bearing — worth acquiring, worth retaining, worth
  re-acquiring. The precondition AC28 named is now met.
- **Does not establish**: acquisition, retention, or re-acquisition (the register/search machinery is
  unbuilt — AC28's actual next step); autopoiesis; closure; life.

## Next step

AC56 — acquisition and retention over the six-position order: a register the order is written into,
repaired when corrupted, and re-acquired after a regime change, the AC16/AC18 shape over a structure now
proven load-bearing. This is AC28's stated next step, unblocked.

## Artifacts

`ac55_order.py`, `ac55_engineering.py`, `ac55_results_v1/`, `audit_ac55.py` (7/7 hashes, gates
recomputed), `replay_ac55.py` (12/12 exact), `test_ac55.py` (10 tests), `AC55_PROTOCOL_v1.md`.
