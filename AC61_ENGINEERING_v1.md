# AC61 engineering: register repair is preventive, not curative — and that is why re-acquisition is necessary

2026-09-15. Engineering finding, verified empirically. **No protocol, no final seeds, no claim.**

## The finding

`ac29_register`'s repair restores non-unanimous bits to their *current* majority. So repair maintains
whatever order the register currently holds, but cannot undo a corruption once a bit's majority has
flipped — it freezes the wrong value.

Verified: with repair every tick, the order stays `(5, 1, 2, 4, 3, 0)` (preventive — holds the order).
But a register damaged unrepaired for 300 ticks reads `(5, 1, 2, 4, 0, 3)` — a valid but wrong order —
and 300 further ticks of repair leave it at `(5, 1, 2, 4, 0, 3)`. Repair did not recover the original
order; it froze the corruption. There is a point of no return: once the majority flips, no amount of
repair restores the acquired order.

## Why this matters — the two mechanisms are complementary, not redundant

The project now has two distinct responses to register corruption, and this finding shows they address
different failure modes:

- **Repair (AC58)** is *preventive*: it holds the order correct against ongoing damage. It is cheap and
  continuous, but it is inert past the point of no return — it can only ever maintain the current
  majority, right or wrong.
- **Re-acquisition (AC57)** is *curative*: it discards the corrupted order and re-searches for the
  value-optimal one. It is expensive (a full search) but it is the only mechanism that can recover after
  corruption has flipped the register.

So the two are not alternatives; they are a division of labour. Repair guards against slow degradation;
re-acquisition is the recovery path once degradation has won. A design that had only repair would be
permanently broken by any corruption that crossed the majority threshold; a design that had only
re-acquisition would pay a full search for every flipped replica. This is the first time the line has
shown *why* the organism needs both.

## What this does and does not establish

- **Establishes**: the register's repair semantics (preventive, not curative), verified; and the
  architectural complementarity of repair and re-acquisition.
- **Does not establish**: a frozen claim about an organism's behaviour (this is a property of the
  supplied register, not a measured effect); autopoiesis; closure; life.

## Bounds

No claim. Engineering prerequisite. The next natural study would freeze the complementarity: an organism
that repairs *and* re-acquires (both mechanisms) retains more value under a corruption regime that crosses
the majority threshold than one that only repairs.

## Artifacts

This document (the verification was an inline check; the property is a direct read of `ac29_register.py`).
Related: `AC58_RESULTS_v1.md` (repair prevents collapse), `AC57_RESULTS_v1.md` (re-acquisition recovers).
