# AC20 feasibility: the developmental function is narrow, but the *format* is not

2026-09-15. Feasibility only, script `ac20_feasibility.py`. No protocol, no final seeds,
nothing claimed. This is the first step on the older open item — "a broader developmental
function than the present four routing classes and two unknown bits" — and it produced a
correction to how I had been stating the problem.

## Measured starting point

`ac5_program.program(priority)` is **five fixed constituent rules plus four bank-repair rules
whose order is the entire acquisition**:

| slot | content |
| --- | --- |
| 0-4 | fixed: fuel low → take fuel; material low → take material; W low → produce W; C low → produce C; B low → produce B |
| 5-8 | acquired: the four bank rules (mask = one bank's disagreement bit, action = repair that bank), **ordered by the acquired permutation** |

So the acquired object is a permutation of 4: **24 possible programs, log2(24) = 4.58 bits**,
and the 9-rule format reproduces the present demonstration exactly (0 mismatches over all 24
permutations × 512 observations).

## Two attempts to build a demonstration the present format cannot express, both failed

1. **A resource-contingent priority** (the repair order depends on which resource is low).
   Result: **512/512** for a fixed permutation. The reason is a design error on my part — the
   fixed constituent rules fire *before* the bank rules, so whenever the repair order could
   matter, no resource is low. The contingency has to live where the bank rules actually decide.
2. **A pair exception** (when two declared banks disagree together, the later one is repaired
   first). Result: **512/512** for the present 4-slot format, best arrangement
   `((8,3),(4,2),(16,4),(32,5))`. Because rule order alone resolves subsets of four banks, a
   pairwise preference that is *acyclic* is always captured by some total order.

The widened-format comparison in that same run scored 508/512 — *worse* — because my explicit
pair rule sat after the order rules and the interpreter takes the first match. Another
construction error, recorded so it is not repeated.

## What that failure establishes

**The narrow thing is the demonstration, not the program format.** The 4.58 bits describe what
the *acquisition* conveys (a permutation); the format itself holds four free rules, each an
arbitrary (9-bit mask → 4-bit action) pair, interpreted first-match-wins in a fixed order. That
is not 24 functions; it is on the order of 8k⁴ candidate rule sets with ordered-exception
semantics. So a broader developmental function does **not** require a wider rule format — my
earlier assumption that a 13-rule storage extension was needed is wrong as stated, and the
182-bit overflow I hit only reflects 13 rules rather than the 9 the supplied law defines.

That reframes the open item accurately: **broaden what the world demonstrates and demands, not
the format** — and then measure whether the acquisition process scales to it, keeping the two
endpoints the open item names separate (random-fallback survival versus acquired-function
retention).

## The next measurement, in the form this now takes

A demonstration is inexpressible by a permutation only if its preference over the banks contains
a **cycle** — 0 before 1, 1 before 2, 2 before 0, which no single order satisfies. So that was
built and measured (`demo_cycle`, `cycle_search`):

| demonstration | best by a fixed permutation | best by the 4-slot format |
| --- | ---: | ---: |
| present (fixed priority) | 512/512 | 512/512 |
| pair exception | 512/512 | 512/512 |
| **cyclic preference** | **510/512 (99.6%)** | **511/512 (99.8%)** |

The cyclic case does fall short of perfect — by two observations out of 512, and only for the
orderings no total order reaches — but the 4-slot format closes almost all of it, because a rule
mask can require *two* banks to disagree at once. So the third attempt also fails to be a format
limit.

## Conclusion: at four banks the format is not the constraint, the domain is

Across three constructions the outcome is the same: on a four-element domain (four banks, nine
observation bits) the 9-rule format — five fixed rules plus four free rules, each an arbitrary
9-bit mask to 4-bit action pair, interpreted first-match-wins in a fixed order — reproduces
essentially every preference structure I could devise, including one that no single permutation
can satisfy. The acquired *object* in the present design is 4.58 bits, but that is a property of
the **demonstration**, not of the format's capacity.

So the open item's real content is a **domain size** question, not a coding question. "A broader
developmental function than the present four routing classes and two unknown bits" means the
world must offer **more distinguishable conditions and more actionable constituents** — more
banks, more constituent needs, a wider observation word — and only then does it become an
empirical question whether the (possibly widened) format suffices. That inverts the design step I
was about to take: I was about to widen the rule format to accommodate a richer demonstration,
and the measurements say the demonstration is the narrow part while the format has room to spare
at this scale.

The next step is therefore a **world design**, not a format change: declare a larger bank and
constituent structure (e.g. six to eight banks, with the constituent rules correspondingly
richer), keep the observation word wider than nine bits, and re-run this same feasibility
measurement to find the scale at which the format *does* bind. Only at that scale does a format
change become justified — and it would be declared before any run, per the project's protocol
discipline. The two endpoints the open item names stay separate throughout: random-fallback
survival, and retention of the acquired function.

## Artifacts

`ac20_feasibility.py` (all three constructions and their best arrangements, with the reasons for
each failure in the docstrings). No results directory, no protocol, nothing claimed.
