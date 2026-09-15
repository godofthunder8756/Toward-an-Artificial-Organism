# AC25: what makes a rule order learnable — confrontability, measured

2026-09-15. `ac25_confront.py`, `test_ac25.py`, `ac25_confront_v1.json`. Design-space arithmetic.
**No chemistry, no organism, no world, no protocol, no final seeds, nothing claimed about the
organism.** This produces the design criterion the scaled world must meet, before anything is built.

## The question

AC24 measured the frozen world's developmental function at **1.00 effective bit**: two of its four
rule positions can never fire, so 24 permutations collapse to 2 behaviours. The scaled world is
supposed to carry more. What exactly must the world present for `log2(B!)` of order structure to be
real, rather than nominal?

Order information can only come from **confrontation**: a rule's position is revealed only when
another rule also matches the same observation and the earlier one wins. This module measures that,
counting distinct first-match behaviours over all permutations.

## Measured, at B = 6 (720 permutations, 9.49 nominal bits)

The ladder — how much co-occurrence buys:

| reachability | observations | behaviour classes | effective bits |
| --- | ---: | ---: | ---: |
| singletons only (each observation sets one signal) | 6 | **1** | **0.00** |
| all pairs | 15 | **720** | **9.49** |
| all triples | 20 | 360 | 8.49 |
| all subsets (2^B) | 64 | 720 | 9.49 |
| singletons + pairs (nothing higher) | 21 | 720 | 9.49 |

Two results, both worth stating as theorems because they are measured rather than argued:

1. **No co-occurrence means no order information at all.** If every reachable observation sets
   exactly one signal, each observation matches exactly one rule, the chosen action is that rule's
   action, and the order is invisible: all 720 permutations behave identically. **0.00 bits, however
   many signals are live.** The frozen world sits close to this point.
2. **Pairwise co-occurrence is sufficient for the full order.** A total order is determined by its
   pairwise comparisons, and 720 behaviour classes appear as soon as every pair of the six signals
   is simultaneously set somewhere. So the requirement is *pairwise*, not "all 64 subsets".

The triples row is the counterintuitive one and it is not a bug: **all triples buy less than all
pairs (360 vs 720)**. An observation setting three signals reveals only which of the three *wins*;
it hides the pairwise relations among the two it beat. Co-occurrence arity is therefore not
monotone in usefulness, and pairs are the sweet spot.

## What each defect costs (all pairs otherwise reachable)

| defect | classes | effective bits |
| --- | ---: | ---: |
| one position dead (5 live) | 120 | 6.91 |
| two positions dead (4 live) | 24 | 4.58 |
| two rules sharing a mask **and** an action (fused pair) | 120 | 6.91 |
| two rules sharing a mask, **different** actions | 240 | 7.91 |

- A **dead position costs immediately**: 5 live positions give 6.91 bits — the full order structure
  for five — against the 9.49 that the six-position design promises. One structurally mute position
  costs a quarter of the intended structure, not a rounding error.
- Four live positions, all pairwise confronted, give **exactly 24 classes = 4.58 bits**, the full
  nominal order structure for four. That is the clean demonstration that the frozen world's
  1.00-bit measure is **purely a deadness effect**, not a property of four-position controllers.
- **Fusing two positions** (same mask *and* same action) costs exactly what a dead position costs:
  the pair behaves as one position, so five effective positions → 120 classes. Giving the fused
  pair *different* actions restores half the loss (240 = 2 × 120): the pair's internal order becomes
  observable even though their mask is shared.

**Control:** the frozen configuration, re-measured by this independent method — masks 4, 8, 16, 32,
bit 5 never set, one region varying per individual — gives **2 classes, 1.00 bit**, reproducing AC24
exactly. Two different methods agreeing on the same number is the strongest check available here.

## The design criterion for the scaled world

> **CORRECTED BY AC26.** The criterion below is **necessary but not sufficient**, and AC26 measured
> the gap: a world satisfying it (all 15 pairs of six signals co-occurring by 323 ticks) reaches
> only **680 of 720** orders. Co-occurrence inside a larger word does not isolate a comparison,
> because a third signal present in the same word can pre-empt it — the same effect as this
> document's own triples row (360 classes), which should have been read as a counterexample rather
> than a curiosity. **The correct criterion is that for every pair `(i,j)` the world must present an
> observation equal to exactly `{i,j}` and nothing else.** The table row below labelled "all pairs"
> satisfies that stronger condition by construction — it *is* the set of exact pair words — which is
> exactly why it reaches 720, and is what I over-generalized from. See `AC26_SIGNALS_v1.md`.

Necessary but **not sufficient** as originally stated: the AC22 container (C = 6, B = 6, rules = 12,
mask_bits = 12) and the AC21 format, and the AC23 body layer. Those are about *capacity* — how much
structure could be stored. What this measurement adds is a property of the **world's dynamics**, not
the format:

> Every pair of the six signals must be simultaneously present in some reachable observation.

That is the acceptance criterion, and it is checkable before any chemistry exists: build the world's
signal logic, enumerate the reachable observations, count behaviour classes over the permutations,
and require **720**. Anything less is quantifiable drift — six positions with one dead is 120
classes, not 720, and the difference is not a rounding error but a fifth of the structure.

How to get it in a real world: six maintenance needs that vary **independently**, so that any pair
can be low at once. The frozen world does the opposite — it ties a W region to the individual's
history, making the two regions mutually exclusive, which is precisely the mechanism that produced
1.00 bit. Independence of need is the design principle, and the failure mode now has a number
attached.

## Not built, plainly

- **No world.** This is arithmetic over synthetic observation words. There is no organism, no
  chemistry, no scaled acquisition, no step. Nothing has been run in a new world.
- **No protocol, no final seeds, no claims.** The criterion above is a design requirement, not a
  result, and the numbers are properties of a synthetic reachability family.
- **Nothing about the organism.** Counting distinct input-output behaviours of a rule table says
  nothing about experience, understanding, or life, and is not offered as evidence toward any of
  them.
- **The two endpoints the open item names** (random-fallback survival; retention of the acquired
  function) remain untouched. This work is upstream of both: it says what there is to retain.

## The next step

Build the scaled world's signal logic — six independent maintenance needs with the pairwise
co-occurrence property — and verify the criterion by enumeration (720 classes) **before** writing
the reaction chemistry. Then the chemistry, then the acquisition, then a protocol.

## Artifacts

`ac25_confront.py`, `test_ac25.py`, `ac25_confront_v1.json`. Related: `ac24_functional.py`,
`AC24_FUNCTIONAL_v1.md`, `ac22_world.py`, `AC22_WORLD_v1.md`, `ac23_body.py`, `AC23_BODY_v1.md`.
