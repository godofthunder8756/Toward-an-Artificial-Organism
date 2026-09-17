# AC68 results v1: repair is necessary but not sufficient — body bimodal, function open, register intact only in survivors

2026-09-16. Final seeds 2700–2703 (4 seeds × 2 histories = 8 individuals), hashed protocol
`AC68_PROTOCOL_v1.md`, 16,384 ticks (4× standard). Engineering seeds (0–2) excluded.

## Gate outcomes (prespecified)

| gate | statement | result |
| --- | --- | --- |
| G1 | body survives the horizon in all 8 | **FAIL** (4/8; seeds 2700, 2702 die at 7,813 / 7,393) |
| G2 | W_live ≥ 1 and C_live ≥ 1 at the end in all 8 | **FAIL** (4/8; the dying seeds end with W=0, C=0) |
| G3 | routes lapse (occupied == 0) in all 8 | **PASS** (8/8, routes `[None,None]`) |

The claim as written — "the body is self-sustaining while the function lapses" — is **falsified** on the
body half: the body's long-horizon survival is bimodal, not universal. Thresholds are not moved.

## The measured pattern (per individual)

| seed | outcome | register (final) | W/C | first_death |
| --- | --- | --- | --- | --- |
| 2700 | die | `[F,T,T,F]` | 0 / 0 | 7,813 |
| 2701 | survive | `[F,F,F,F]` | 2 / 2 | — |
| 2702 | die | `[F,T,F,F]` | 0 / 0 | 7,393 |
| 2703 | survive | `[F,F,F,F]` | 2 / 2 | — |

## What the data shows, precisely

**Function (routes): reliably open.** All 8 individuals lose both acquired routes (`occupied=0`,
`first_route_loss` 2,812–11,693). The routes lapse because the program's own scheduling neglects renewal
(region 1 renewed zero times in the seed-0 diagnostic; 8,792 W/C births, 2,837 B births, 4,357 idle
actions against 132 renewals). The acquired organization is not self-maintaining.

**Body: bimodal.** 4/8 reach a steady state (energy ~120, W=2, C=2, B=20) and survive the full 16,384
ticks. The other 4/8 hold the same steady state until ~7,400–7,800, then collapse: W and C die together,
energy conversion stops, energy drains 122→12, death — a W/C decay cascade.

**Register: intact only in survivors — a refinement of AC67.** The surviving seeds keep the register
`[F,F,F,F]` (the repair maintains it against damage, as AC67 showed). The dying seeds end with a degraded
register (`[F,T,T,F]` / `[F,T,F,F]`) — but this is the organism's *own* relinquishment writes (`_drop`
sets a slot to 1 on a streak of failed contacts), which the majority-directed repair cannot undo, not
damage. So the repair maintains the decision state against *damage*, but not against the organism's own
relinquishment once the routes have already lapsed and contacts are failing.

## Why this is a real result, not a tuning miss

The bimodality is the **AC47 structural limit re-entering through the long horizon**: a self-funding body
whose production is proportional to its population is either at a stable equilibrium or collapsing, and
stochastic stress decides which at ~7,500 ticks. AC67's load-bearing repair loop is **necessary** — cutting
it kills 8/8 — but **not sufficient** — even intact, half the seeds collapse, and the function lapses in
all of them. The closure boundary is now located precisely, with three independent gaps:

1. the acquired function (routes) is not self-maintaining (scheduling neglect) — 8/8 lapse;
2. the body's self-production is fragile (bimodal, W/C decay cascade) — 4/8 collapse;
3. the decision state is maintained against damage but not against the organism's own relinquishment.

## What this establishes and what it does not

Establishes: repair is necessary-but-not-sufficient; the function is reliably open; the body is bimodal;
the register is intact in survivors and degraded (via `_drop`) in the dying. The three gaps above are the
concrete remaining distance to full organismal autonomy.

Does not establish: autopoiesis, consciousness, optimality.

## Artifacts

`ac68.py`, `ac68_results_v1/`, `ac68_engineering_v1/`, `AC68_PROTOCOL_v1.md`. Next: `audit_ac68.py`,
`replay_ac68.py`, `test_ac68.py`.
