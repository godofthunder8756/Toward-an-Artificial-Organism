# AC75 engineering v1: erase-on-relinquish makes the reconciled closure world-accommodating

2026-09-17. `ac75_engineering.py`, `ac75_addendum.py`. **Engineering prerequisite — no final seeds, no
frozen claim.** Implements goal §4's directed diagnostic on the AC74 cascade.

## The diagnosis, confirmed by intervention

AC74 traced the residual death to a stale-route persistence window: on a route move the organism
relinquishes the moved slot but does **not** erase the entry, so `read(key)` keeps returning the stale
port for the entry's full 64-tick life; the material-low observation then makes the program loop on the
failing contact, starve core W to 0, and close the deposit path (no live W parent) → death.

The §4 intervention — erase-on-relinquish — makes the drop also clear the entry immediately (booked as
memory expiry, consistent with the frozen decay law, not a new cost or write). Four variants, all in the
AC71 world (full yields, sticky damage, majority read, 16,384 ticks, move of channel 1 at t=8192):

| variant | machinery | permanent move | temporary outage | unchanged |
| --- | --- | --- | --- | --- |
| A | AC71 as-is | 0/6 re-acquire, 4/6 die | — | — |
| B | deposit open | 2/6, 4/6 die | — | — |
| C | B + restore rule | 4/6, 0/6 both-routes | 2/6 | 6/6 |
| **D** | **C + erase-on-relinquish** | **6/6, 6/6 both-routes** | **6/6** | **6/6** |

Variant D reaches **6/6 survive, 6/6 re-acquire, both routes held (`demand [42,0]`), register fully
intact (`[F,F,F,F]`)** under a permanent move, and — the sharpest test — **6/6 under a temporary outage**
(port flips at 8192, flips back at 12288: the organism relinquishes and re-acquires **twice**, mean 2.0
relinquishments), where C collapses to 2/6 on the second transition.

The unchanged-world control is clean: C and D are identical (6/6, zero relinquishments, both routes
held), so the erase introduces no spurious behaviour in the absence of change. The repair loop stays
load-bearing in every variant: `no_repair` dies 6/6 (deaths 539–1381) regardless of the erase.

## Why the mechanism is legitimate, not a rescue

- **No privileged information.** The erase is triggered only by the organism's own relinquishment
  decision (its own failure streak), not by any external signal.
- **No external rescue.** It is the organism's own write path; the drop is already paid (register write),
  and the erase books the entry as expired exactly as the frozen `age` decay does — a change in *when*
  the entry decays (on relinquishment, not after 64 ticks of non-renewal), not a new free-energy source.
  The material/energy conservation identities (`ac4.balance`) are untouched.
- **Generalizes within the declared family.** The erase applies to any slot on relinquishment, and the
  temporary-outage result shows it handles non-monotonic change, not just one move.

## The residual question to freeze

The claim shape is categorical: the erase mechanism survives and re-acquires in **all** individuals under
both permanent and temporary change, holds both routes, keeps the register intact, stays inert in the
unchanged world, and preserves the repair loop's load-bearing role — while the no-erase rival (C) fails
under change. That is exactly what the next frozen study (AC75, held-out seeds) should pre-specify.

## Bounds

Engineering prerequisite. No claim, nothing frozen. The measured quantities are survival, route holding,
register state, relinquishment/restoration counts, in the AC71 world with declared transitions.

## Artifacts

`ac75_engineering.py`, `ac75_addendum.py`. Related: `AC74_ENGINEERING_v1.md` (the cascade this fixes),
`AC71_RESULTS_v1.md` (the fixed-world closure), `AC16_RESULTS_v1.md` (the restore rule joined here).
