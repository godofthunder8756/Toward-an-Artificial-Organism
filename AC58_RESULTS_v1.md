# AC58 results v1 — repair retains the acquired order, preventing corruption-induced collapse: FROZEN (eighth verified claim)

2026-09-15. `ac58_order.py` (finals), `ac58_engineering.py`, `ac58_results_v1/`, `audit_ac58.py`,
`replay_ac58.py`, `test_ac58.py`. All eight gates pass.

## The claim, frozen

In the scaled body, the acquired six-position order held in a replica-encoded register is corrupted over
the run; paying to repair the register retains the order, sustaining production and survival — while an
unrepaired register corrupts and the organism collapses. This is AC14's integrity channel, which AC43
left off (`reg_rate = 0`), now turned on and joined to the developmental line's acquired order.

## Gates (final seeds 4848–4859)

| gate | result |
| --- | --- |
| G1 resolvable | pass — p = 0.00098 |
| G2 effect ≥ 8000 | pass — 20,077.25 |
| G3 retention | pass — repaired == protected for every individual |
| G4 repaired stability | pass — 0 dead |
| G5 protected stability | pass — 0 dead |
| G6 corruption consequential | pass — unrepaired has 3 dead |
| G7 horizon-robust | pass — 2.487 |
| G8 determinism | pass — re-run exact |

## The effect, stated plainly

- Protected and repaired arms are **identical** (mean 68,402, min 67,970.5, max 68,663) — continuous
  repair restores every flipped replica, so the read-back order is always the acquired one, and the
  1-energy repair cost is invisible against the world's abundant energy.
- The unrepaired arm corrupts and collapses: mean 50,382 (min 18,115.5, max 68,679), 3/12 dead. On the
  seeds where the register corrupts badly, the critical region (value 100) is neglected, production
  crashes, and energy falls below drain.
- The difference is median 20,077 value-units (p = 0.00098) — repair retains ~40% more value than
  leaving the register to degrade, and it does so by preventing collapse, not by slowing a gradual loss.

## Why this is the integrity channel (and not a maintenance claim)

AC58 engineering established that corruption is **abrupt**: the majority-vote register flips a stored bit
when 4 of 7 replicas turn, and the positional Lehmer code maps a single flipped bit to a *different
permutation* — often one that moves the critical region to the back. Under concentrated value that is
fatal. So repair's benefit is keeping the organism on the right side of a threshold (collapse vs. no
collapse), which is AC14's integrity question answered in its honest form, rather than a gradual
maintenance effect.

## What this does and does not establish

- **Establishes**: the acquired order's register integrity is load-bearing for survival — repair retains
  it and prevents corruption-induced collapse. The maintenance line (AC43, corruption absent) and the
  developmental line (AC57, order load-bearing and re-acquirable) are now joined at the register.
- **Does not establish**: autopoiesis, closure, or life. The order, register, and repair are supplied
  mechanisms.

## Next step

The three lines now meet at one object — the acquired six-position order held in a repaired register.
The natural next question is whether the repair *payment* is self-funded from the production the order
sustains (closing the loop between the order's value and the maintenance that protects it), or whether
the order structure can be scaled beyond six positions.

## Artifacts

`ac58_order.py`, `ac58_engineering.py`, `ac58_results_v1/`, `audit_ac58.py` (7/7 hashes, 7/7 gates
recomputed), `replay_ac58.py` (12/12 exact), `test_ac58.py` (10 tests), `AC58_PROTOCOL_v1.md`.
