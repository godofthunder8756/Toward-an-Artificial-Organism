# AC24: the frozen developmental function is 1.00 effective bit, not 4.58

2026-09-15. `ac24_functional.py`, `test_ac24.py` (9 tests), `ac24_functional_v1.json`. Pure
measurement of the frozen world's controller. **No new world, no step, no protocol, no final
seeds, nothing claimed about the organism.**

## The finding

The frozen world's controller has four rule positions and 24 possible orders, which I have been
quoting as `log2(24) = 4.58 bits` of acquired structure since AC20. Measured against the
observations the world actually presents, **only two of those four positions can ever fire, and
the 24 permutations collapse to 2 distinct behaviours — `log2(2) = 1.00 bit`.**

| | history 0 | history 1 |
| --- | --- | --- |
| reachable observations (a real 2048-tick run) | 19 | 19 |
| live rule positions (of 4) | masks 4, 8 | masks 4, 16 |
| observations where the live masks co-occur | 2 | 3 |
| permutations → distinct behaviours | **2**, class sizes [12, 12] | **2**, class sizes [12, 12] |
| nominal structure | 4.58 bits | 4.58 bits |
| **effective structure** | **1.00 bit** | **1.00 bit** |

## Why, mechanically

Two independent causes, both structural rather than statistical:

1. **`activation` ties a W region to the individual's history.** In a run, `activation=[history==r
   for r in range(2)]` means an individual of history 0 never activates region 1, so no slot there
   is ever near expiry and the urgency bit for that region (observation bit 4) is never set. The
   mask that conditions on it — 16 — can never match. History 1 is the mirror image: mask 8 is the
   dead one.
2. **Observation bit 5 is never set by `ac9.observe`** (established in AC23, and re-checked here:
   0 of 19 reachable observations in either history), so mask 32 can never match either.

So per individual exactly two positions are dead: one because its region is inactive, one because
bit 5 cannot be set. What remains live is always "repair the program bank" (mask 4) plus "renew the
one active region's memory" (mask 8 or 16) — and those two *do* co-occur (2 and 3 observations
respectively), so their relative order is the one bit of real content. Class sizes of exactly
[12, 12] confirm the geometry: the two live rules' order splits the 24 permutations in half, and
the dead rules' positions absorb the rest.

## The three senses of "bank", and which one was growing

This is the terminology tangle that produced the surprise. In this project "bank" has meant:

| sense | what it is | where |
| --- | --- | --- |
| (a) site group | `life[4*bank:4*bank+4]`, a birth target | groups 0,1,2 live; group 3 never a target |
| (b) trace bank | `b.traces[bank]`, a 1024×7 replica store | only bank 0 is ever used |
| (c) rule position | a slot in the controller, mask `4<<bank` | the AC11-onward "four routing classes" |

AC20/AC21/AC22 grew sense (c) — the size of the acquired object — and sized the format for it;
AC23 then modelled sense (b) as if the added positions were trace banks. Both are coherent, but
the quantity that decides whether "broader" means anything is **how many of the positions the world
can actually confront**, and on that measure the frozen world delivers one bit.

## Scoping correction to AC20–AC23

The budget, format and body results stand on their own terms — `C + B ≤ slots`, `mask_bits ≥
observation width`, the format proven reducible to the frozen one, the body layer proven to
reproduce `ac9.observe` on 600 randomized states. What they do **not** do is size a function the
world realizes: they were sized against a 4.58-bit nominal target, and the world presents a 1-bit
question. Format capacity was never the binding constraint on the *demonstration*; it became the
subject of AC20–AC23 because I took the nominal count at face value instead of measuring the
behaviour.

This also reframes the AC11→AC13 allocation wall. That line's diagnosis was that a single-bit port
with a uniform blind fallback makes a stored route either decisive-because-fatal or negligible.
The measurement here is consistent with a deeper version of the same problem: the world gives its
controller almost nothing to be right or wrong *about* — one bit shared by two rules, with the
remaining two positions structurally mute. I record that as a hypothesis that now has a measurement
behind it, not as an established cause.

## What this makes the requirement

"Broader developmental function" is not mainly about slots or mask widths. It is about
**confrontability**: the world must present situations in which every rule position can fire and in
which the orders between them change behaviour. Stated as targets this measurement can check:

| scaled design at B = 6 | predicted effective structure |
| --- | --- |
| every position live and mutually confrontable | `log2(6!) = 9.49` bits |
| one position structurally dead | `log2(6!/6) = 6.91` bits |
| two live (the frozen situation, scaled up) | `log2(2) = 1.00` bit |

So the scaled world has an acceptance criterion that is measured, not argued: build it, enumerate
the reachable observations, count distinct behaviour classes, and require the count to approach
`B!`. The AC22 parameters (C = 6, B = 6, rules = 12, mask_bits = 12) are still the right
*container*; what they need is a world that confronts all six positions — for instance six live
urgency/need signals with genuine co-occurrence, rather than four positions of which two are mute.

## Not built, plainly

- **No scaled world, no step.** `ac24_functional.py` measures the frozen controller; there is still
  no six-bank body, no scaled acquisition, no scaled reaction chemistry. Nothing here runs an
  organism in a new world.
- **No protocol and no final seeds.** The targets above are design criteria, not results.
- **Nothing is claimed about the organism.** This is a count of distinct input-output behaviours of
  a frozen rule table. It is not evidence of experience, understanding, or life, and it does not
  bear on those questions; it is a measurement of how much structure the world's demands contain.
- **The two endpoints the open item names** (random-fallback survival; retention of the acquired
  function) are untouched. The effective-bits measure is orthogonal to both, though it now looks
  like a prerequisite for the retention endpoint: there is very little to retain.

## The next step

Design the scaled world for confrontability: choose the signals that condition the six rule
positions so that every position can fire and the pairs genuinely co-occur, then measure distinct
behaviour classes against `B!` **before** building the chemistry — the same order of work that
AC20's feasibility check used, and for the same reason: it is cheaper to discover that a design
cannot express what it claims before the bodies exist.

## Artifacts

`ac24_functional.py`, `test_ac24.py`, `ac24_functional_v1.json`. Related: `ac22_world.py`,
`AC22_WORLD_v1.md`, `ac23_body.py`, `AC23_BODY_v1.md`, `AC20_BUDGET_v1.md`, `AC21_FORMAT_v1.md`.
