# AC59 engineering: the scaling frontier — order structure grows, the rule format is the binding axis

2026-09-15. `ac59_scaling.py` (combinatorics check). **No protocol, no final seeds, no claim.**
Establishes where the developmental function can grow, and which axis binds first.

## The measurement

The order-structure criterion (AC25: every exact pair presented → B! distinguishable behaviours) scales
exactly with the number of positions:

| positions | behaviour classes | effective bits |
| --- | --- | --- |
| 6 | 720 | 9.49 |
| 7 | 5040 | 12.30 |
| 8 | 40320 | 15.30 |

Combinatorially the developmental function has room to grow: each added position adds ~3 bits of
acquired order structure, with no ceiling until the permutation count becomes intractable (not here).

## The binding axis is the rule format, not the order

AC20 measured two independent limits on the controller's format: **slot count** (9 rules) and **mask
width** (9 observation bits), each binding when C + B > 9. Scaling the order to seven positions means a
seven-region world (C = 7 constituent needs), which with even three banks needs 10 slots — already over
the 9-slot format. So the next scale step is not merely "more positions": it is the two-axis widening
AC20 specified ("widen the format AND the domain together"), and it binds at the rule format, not at the
order structure.

## What this means for the next build

The next build is a **seven-region world**: seven stress rates, seven values (a concentrated head +
graded tail of length 7), a seven-position register (13 bits), and a rule format widened to C + B = 10
slots and 10 mask bits. That is a mechanical but real extension of AC55/AC57/AC58 to a 12.30-bit order,
and the first point where the format budget AC20 measured actually binds. Whether the load-bearing and
re-acquisition properties (AC55/AC57) survive the wider domain is the question a successor study would
freeze.

## Bounds

No claim. Engineering prerequisite: a frontier specification. Not autopoiesis, closure, or life.

## Artifacts

`ac59_scaling.py`. Related: `AC25_CONFRONT_v1.md` (the criterion), `AC20_BUDGET_v1.md` (the format
limits), `AC55_RESULTS_v1.md` / `AC57_RESULTS_v1.md` (the six-position load-bearing claim this extends).
