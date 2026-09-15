# AC27: the deliberate pair schedule, and where the order structure comes from

2026-09-15. `ac27_schedule.py`, `test_ac27.py` (10 tests), `ac27_schedule_v1.json`. Design-space.
**No reaction chemistry, no organism, no scaled acquisition, no step, no protocol, no final seeds,
nothing claimed about the organism.**

## What this does

AC26 corrected the criterion: the controller's full order needs an **exact pair witness** for every
pair, not merely co-occurrence. The cyclic coprime-needs design of AC26 satisfies that only at its
full conjunction period — 1,616,615 ticks for six needs — which is not a design to ship. This
presents the pairs **deliberately**, as a demand schedule, and measures how quickly the structure
becomes complete.

## The minimum, and the schedule

| | presentations | classes | bits |
| --- | ---: | ---: | ---: |
| the 15 exact pairs alone | **15** | **720** | **9.49** |
| the deliberate schedule (pairs + singletons + empty, one round) | 22 | 720 | 9.49 |

Fifteen presentations suffice, and the schedule is an ordered version of the same thing. Against the
oscillator design's 1,616,615 ticks, the deliberate schedule completes the structure after 15 rounds
— **107,774× sooner**.

## The frontier, and where the numbers come from

Class count after each successive pair round:

    2, 4, 8, 16, 32, 48, 72, 108, 162, 216, 288, 384, 480, 600, 720

The count is the number of *comparison patterns realisable by a total order* — the number of
distinct first-match behaviours the accumulated pair presentations induce. That explains the shape:

- **The first five pairs all involve need 0**, so they form a *star* — a forest. Each edge is
  orientable independently of the others and every orientation is realisable by some total order, so
  the count doubles: 2, 4, 8, 16, 32. Verified directly (`test_a_forest_of_pairs_doubles_each_time`).
- **The sixth pair closes a triangle** (0–1, 0–2, 1–2), and transitivity forbids some orientations.
  Of the two star edges' four orientations, 2 + 1 + 1 + 2 = 6 extend to the third edge — so the
  count multiplies by **1.5, not 2**: 32 → 48, exactly as measured.
- From there each further pair constrains the order a little more, with the count rising to 720 once
  the comparison graph is complete.

So the frontier is not an empirical curve with no story: it is the accumulated comparison structure,
with a forest phase and then the closure of cycles.

## Robustness

| family | classes |
| --- | ---: |
| exact pairs only | 720 |
| + singletons + empty | 720 |
| + all triples | 720 |
| + every subset (2^B) | 720 |

Higher-order demands **never reduce** the count — adding triples or the full power set leaves 720
intact. That matters for the design: the world may present whatever else it likes, as long as the
exact pairs are there. It also means the AC26 measurement (triples alone → 360) was a statement about
triples *without* pairs, not a hazard for a world that has both.

## Control

One need at a time, grouped into three exclusive pairs — the frozen world's habit taken to its limit
— gives **1 class, 0.00 bits**. No comparisons, no order information at all. Together with AC26's
epoch control (3.00 bits) and the frozen world's own signals (1.00 bit), this is the fourth
independent reproduction of the same mechanism: **mutual exclusivity of demands destroys the
structure the controller is supposed to acquire.**

## What is now specified

The scaled world's requirement, complete and checkable before any chemistry:

1. Six live need signals (the AC23 body layer supplies the observation wiring; the AC22 container
   and AC21 format supply the capacity).
2. A demand pattern that presents **each exact pair in isolation** — 15 presentations suffice,
   and the order structure is fully determined once they have all occurred.
3. Verified by enumerating behaviour classes over the permutation space and requiring **720**.

The first two are properties of the *environment*, not of the organism, and that is the honest
framing: this work specifies what the world must *ask*, and says nothing yet about whether any
organism can answer it.

## Not built, plainly

- **No chemistry, no organism, no world.** The schedule is a list of observation words and the
  measurements are arithmetic over them. No reactions, no conservation accounting, no step, no
  scaled acquisition, no six-bank body in motion.
- **No protocol and no final seeds**, and no claims. Every number here is a property of a synthetic
  demand sequence.
- **Nothing about experience, understanding, or life**, and none of this is offered as evidence
  toward them. Counting distinguishable first-match behaviours of a rule table is a statement about
  a rule table and a demand pattern.
- **The two endpoints the open item names** (random-fallback survival; retention of the acquired
  function) remain untouched. This work is upstream of both.

## The next step

The reaction chemistry for the six needs: what each need costs the organism, what satisfying it
returns, and the conservation identity — with the AC22/AC23 parameters declared and the AC27 demand
pattern as the environment. Then the scaled acquisition, then a protocol that declares all of it
before any final seed.

## Artifacts

`ac27_schedule.py`, `test_ac27.py`, `ac27_schedule_v1.json`. Related: `ac26_signals.py`,
`AC26_SIGNALS_v1.md`, `ac25_confront.py`, `AC25_CONFRONT_v1.md`, `ac24_functional.py`,
`AC24_FUNCTIONAL_v1.md`.
