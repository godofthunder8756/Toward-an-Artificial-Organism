# AC83 engineering v1: temporal separation resolves the material-low hijack, but the combined architecture still does not compose unconditionally

2026-09-17. `ac83.py`. **Engineering prerequisite — no final seeds, no frozen claim.**
Follow-up to AC82 (milestone 3, answered NO for the combined reconstruction + description
maintenance + route-move architecture). This card asked whether a declared design change could make
the three capabilities compose **unconditionally** (survival + recovery + both routes held, on the
planned denominator — closing AC79/AC80's survivor-conditioning). The answer is **NO — a structural
non-composition** — and this doc records it honestly rather than re-freezing the AC82 configuration
or softening the endpoint.

## The declared design: separate the two interventions in time

AC82's failure was a *simultaneous* interaction: the reconstruction's ~32-material cost and the
move's material-income cut landed on the same tick (8192), together setting observation bit 1
(material <= 64); the frozen program's rule 1 (material contact) precedes the bank-1 renewal rule,
so the material contact preempts renewal and route 0 expired unrenewed. Options (b) cheaper
reconstruction and (c) higher renewal priority require frozen-law changes (out of scope); option
(a) — separating the interventions in time — is the declared viable choice. Two schedules:

- `corrupt_then_move` (A): corruption + reconstruction at t=8192, route move at t=12288.
- `move_then_corrupt` (B): route move at t=8192, corruption + reconstruction at t=12288.

Both were declared before the runs, on the same combined runner (AC80's `build` + AC82's corrected
`AllocErase`, description stored in the damage stream, generic decode). Arms as AC82:
`internalized`, `pristine`, `unmaintained`, `no_repair`, `restore`.

## What the temporal separation fixes (and it is real)

`ac83.py` with the two ticks coincident (8192, 8192) reproduces AC82's published numbers exactly —
`internalized` perm+corrupt: survive 14/16, hold both routes 10/16 — so the runner is a correct
extension and the separation is the only change. With the separation:

| schedule | internalized (perm+corrupt, engineering seeds 0-7) | survive | fw=0 + desc=78 | hold both routes |
| --- | --- | --- | --- | --- |
| A `corrupt_then_move` | | **16/16** | **16/16** | 14/16 |
| B `move_then_corrupt` | | 14/16 | 14/16 | 12/16 |

Reconstruction and description maintenance are now **unconditional** in schedule A: every one of the
16 individuals survives and ends with `fw=0` and `desc=78/78`, where AC82's simultaneous design left
the material-low observation hijacking renewal. The specific AC82 failure mode (route 0 expiring at
~t=8205 because the material contact preempted its renewal) is gone.

## The residual failure is not the reconstruction — it is inherited from AC75's route-move accommodation

Schedule A still loses the "both routes held" endpoint on **seed 4** (both histories: survive, fw=0,
desc=78, W=3 C=2 intact, but `routes=[None,None]`, `demand=[0,0]`). Schedule B adds a late W/C
collapse (seed 4 dies t=16333) and a route-loss survivor (seed 5). The decisive isolation: this is
**not** caused by the combination.

- AC75's *frozen* erase arm, run with no corruption and no description machinery, on seed 4 under
  the permanent move: routes are held only **49.6%** of ticks and end `[None,None]`; the same arm
  with **no move** (`none`) holds routes **99.3%** of ticks and ends `[0,0]`. The route churn is
  produced by the move itself, not by reconstruction or description maintenance.
- Seed 4's acquired priority is `[3,0,2,1]`, which places the bank-1 renewal rule (mask 8, action 3)
  **last** in the rule order — after the boundary rule (mask 256, action 8), which fires 3,544 times
  and preempts renewal whenever the boundary is also aging. The renewal capacity is
  `min(32, 8·W)=24` against 42 aging replicas (both routes share region 0), so renewal is already
  marginal and the move transient tips it into expiry (the AC68/AC69 scheduling-contention family).
- The combined runner's description-triggered reconstruction actually **improves** route retention on
  seed 4 (held 85.1% of ticks vs AC75's 49.6%) — the more frequent rebuild keeps the program clean —
  but it does not make route-holding unconditional.

## The unconditional bar also fails on survival (the AC68 bimodality, AC39's lesson)

The claim demands unconditional survival on the planned denominator. Survival is seed-family
dependent: `internalized` schedule A survives 16/16 on engineering seeds 0-7 but only **10/16** on
the disjoint family 8-15 (deaths: seed 8 t=6780, seed 10 t=1404 — pre-corruption W/C collapses with
fw=8; seed 9 t=12548 — post-corruption collapse with fw=0). This is the AC68 W/C-decay bimodality,
which AC79/AC80/AC81 all reported as a bimodality-aware lower bound, not an exact count. Two further
survivors on 8-15 (seeds 13, 15) lose routes. Unconditional composition = 6/16 on this family.

## Conclusion: structural non-composition

The three capabilities do **not** compose unconditionally under the frozen laws, for two independent
reasons, neither of which the declared temporal separation can close:

1. **Route-holding under a move is seed/priority-dependent** — inherited from AC75's erase arm, not
   caused by the combination. The move transient exposes the renewal-contention limit (boundary rule
   preempts renewal; renewal capacity 24 < 42 aging replicas), and seeds whose acquired priority puts
   the renewal rule last churn and can end with both routes lapsed. Closing it needs a frozen-law
   change (renewal priority, a one-entry-per-region route layout, or a per-slot renewal budget) — all
   out of scope for this card.
2. **Survival is bimodal** (the AC68 W/C collapse), so "unconditional survival" is unsatisfiable on
   collapse-heavy seed families regardless of the intervention schedule.

What temporal separation *does* establish, and is worth carrying forward: the AC82 material-low
hijack is a genuine interaction effect — reconstruction cost plus move income cut landing together —
and separating them makes reconstruction and description maintenance unconditional (16/16 fw=0,
desc=78, 16/16 survival on the 0-7 family). That is a real, reportable improvement, but it does not
reach the card's bar, so the honest disposition is non-composition, not a re-freeze.

## Artifacts

`ac83.py` (engineering runner; never edits ac75/ac76/ac79/ac80/ac81/ac82). Scratch probes
(`ac83_diag_*.py`, `ac83_eng_sweep.py`) are throwaway instrumentation, not part of the deliverable.
Related: `AC82_ENGINEERING_v1.md` (the simultaneous-interaction failure this resolves),
`AC75_RESULTS_v1.md` (the route-move accommodation whose route-holding is seed-dependent),
`AC68_RESULTS_v1.md` / `AC71_RESULTS_v1.md` (the renewal-contention family), `AC79_RESULTS_v1.md` /
`AC80_RESULTS_v1.md` (the survivor-conditioning this card set out to close).
