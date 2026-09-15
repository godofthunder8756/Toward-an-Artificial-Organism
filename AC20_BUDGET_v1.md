# AC20 rule-budget analysis: the format binds at the first growth of the domain

2026-09-15. Script `ac20_budget.py`. Feasibility only — no protocol, no final seeds, nothing
claimed. This is the measurement `AC20_FEASIBILITY_v1.md` asked for ("find the scale at which
the format does bind"), done on the rule budget rather than by building a new world, because the
budget answers the structural question on its own.

## The observation that started it

The present design occupies **exactly** the format's capacity:

    five constituent rules (fuel, material, W, C, B)  +  four bank-repair rules  =  9  =  the format

That is not a coincidence to be glad about — it is a knife-edge. Measured, for a world with **C**
constituent needs and **B** banks (one rule per constituent need, then as many ordered bank rules
as slots remain), best coverage over every acquired bank order:

| C | B | C+B | slots left for banks | coverage | acquired bits |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 4 | 3 | 7 | 5 | 128/128 = **100%** | 2.58 |
| 4 | 4 | 8 | 5 | 256/256 = **100%** | 4.58 |
| 4 | 5 | 9 | 5 | 512/512 = **100%** | 6.91 |
| 4 | 6 | 10 | 5 | 1023/1024 = 99.9% | 9.49 |
| 5 | 3 | 8 | 4 | 256/256 = **100%** | 2.58 |
| **5** | **4** | **9** | 4 | 512/512 = **100%** | **4.58** |
| 5 | 5 | 10 | 4 | 1023/1024 = 99.9% | 6.91 |
| 5 | 6 | 11 | 4 | 2045/2048 = 99.9% | 9.49 |
| 6 | 3 | 9 | 3 | 512/512 = **100%** | 2.58 |
| 6 | 4 | 10 | 3 | 1023/1024 = 99.9% | 4.58 |
| 6 | 5 | 11 | 3 | 2045/2048 = 99.9% | 6.91 |
| 7 | 3 | 10 | 2 | 1023/1024 = 99.9% | 2.58 |
| 7 | 4 | 11 | 2 | 2045/2048 = 99.9% | 4.58 |

## What it says

1. **Full routing requires C + B <= 9.** Exactly at the boundary every case is covered; one
   constituent need or one bank more and it is not. The present design sits on that boundary.
2. **The shortfall just past the boundary is one observation per uncovered bank** — 1023/1024 and
   not something larger — because the uncovered bank only matters when it is the *first*
   disagreeing bank in the acquired order. So the *functional* loss at the first step of growth is
   small. It is still a structural break: the demonstrated function can no longer be reproduced
   exactly at any acquired order, so a "retained acquired function" endpoint cannot be met
   completely. One observation in 1024 is a real deficit when the endpoint is exact retention.
3. **The pressure is exactly where the open item says to push.** The acquired information grows
   with the domain (2.58 → 9.49 bits as B goes 3 → 6) while the slots available for expressing it
   fall (9-C). Broadening the developmental function therefore *squeezes* the acquired structure
   against a fixed budget.

## A second, independent limit: mask width

The rule word is 14 bits = 1 enabled + **9 mask** + 4 action. A rule conditions on at most nine
observation bits, so:

- **Slot count** (9) binds as measured above, when C + B > 9.
- **Mask width** (9 bits) binds separately, once the observation word is wider than nine bits:
  any rule that must conjoin conditions drawn from across a wider word cannot be expressed, even
  with slots to spare.

So a broader world requires a **declared format extension on both axes**, and the required scale
is now specified rather than guessed: **slots >= C + B, and mask bits >= the observation word
width.** With the present world (C = 5, B = 4, 9 observation bits) both limits happen to sit at
exactly 9 — which is why the format looked roomy in the three preference experiments: there was
no slack, but no demand beyond it either.

## Consequence for the design

The next build is a world with a larger C and B and a wider observation word, with the format
extended to match on both axes, declared in a protocol before any run. The two constructions to
avoid, both of which I nearly made:

- **Widening the format without widening the domain** — wasted work; at C = 5, B = 4 the format
  reproduces essentially every preference structure derivable (`AC20_FEASIBILITY_v1.md`).
- **Widening the domain without widening the format** — immediately binding, by the measurements
  above, with a one-observation-per-uncovered-bank deficit that blocks exact retention.

The endpoints the open item names stay separate throughout: random-fallback survival, and
retention of the acquired function.

## Artifacts

`ac20_budget.py` (the budget measurement). Related: `ac20_feasibility.py`,
`AC20_FEASIBILITY_v1.md`. No results directory, no protocol.
