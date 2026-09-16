# AC65 engineering: the permutation order is suboptimal — a reactive deadline rule achieves perfect maintenance

2026-09-15. Engineering prerequisite, but a finding that qualifies the developmental-function line.
**No protocol, no final seeds, no claim.**

## The measurement

In the AC57 scaled body (regime B, region 5 critical), compare the learned optimal permutation
`OPT_B = (5, 1, 2, 4, 3, 0)` against a value-blind reactive rule: *renew the region whose site has the
lowest remaining life* (earliest-deadline-first), no register, no learning.

| family | OPT_B (learned) | deadline-first (reactive) | OPT − deadline (median) | p |
| --- | --- | --- | --- | --- |
| ENG1 | 67,930 | 68,700 | −768 | 0.0005 |
| ENG2 | 68,398 | 68,700 | −206 | 0.0010 |

The deadline rule scores **68,700 — exactly the ceiling** (all 24 sites alive every tick). It achieves
perfect maintenance; the best permutation loses ~1% by letting a few low-value sites expire.

## Why, and why it matters

The permutation is a **fixed-priority scheduler** (renew the first urgent region in a fixed order), and
`OPT_B` over-prioritises the critical region — it keeps region 5 (value 100) alive but starves the tail.
The world is *schedulable*: one renewal per tick comfortably exceeds the stress rate (≈0.5 stress events
per tick against 1 renewal), so earliest-deadline-first misses no deadlines and keeps every site alive.
For a schedulable single-machine problem, earliest-deadline-first is optimal and any fixed priority is
not. That is the whole result.

## What this qualifies

The developmental-function line (AC20–AC28, AC55–AC60) established that the six-position order is
combinatorially rich (720 classes, 9.49 bits), load-bearing, acquirable, re-acquirable, and scaling —
**within the permutation family**. AC65 shows the family itself is dominated: in this world the right
decision rule is a value-blind reactive one, not a learned permutation. So the order's load-bearing
property (AC55) is a property of a suboptimal representation, not evidence that the acquired object is
the right one. The developmental function's claims stand as claims about *permutation orders*, and that
scope must now be stated explicitly wherever they appear.

This is not a retraction — AC55/AC57/AC60 are correct about the permutation family. It is a boundary:
the project has been treating "the acquired order" as the natural object, and in a schedulable world it is
not. Whether a permutation (rather than a deadline rule) becomes necessary in a *non-schedulable* world —
and whether such a world can be stable — is the open question this raises. (AC47/48's tension suggests the
non-schedulable region is the death regime, which would deepen the problem: the order may be necessary
only where the organism is dying.)

## Bounds

No claim. Engineering prerequisite. Not autopoiesis, closure, or life.

## Artifacts

This document (the measurement was inline). Related: `AC55_RESULTS_v1.md`, `AC57_RESULTS_v1.md`,
`AC60_RESULTS_v1.md` (the permutation claims this qualifies), `AC47_ENGINEERING_v1.md` (the schedulability
tension).
