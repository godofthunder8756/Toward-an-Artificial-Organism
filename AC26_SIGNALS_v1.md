# AC26: the scaled world's signal logic, and a correction to AC25's criterion

2026-09-15. `ac26_signals.py`, `test_ac26.py` (9 tests), `ac26_signals_v1.json`. Design-space.
**No reaction chemistry, no organism, no scaled acquisition, no step, no protocol, no final seeds,
nothing claimed about the organism.**

## The correction first

AC25 stated the criterion as: *every pair of the six signals must be simultaneously present in some
reachable observation, and then the full `log2(6!)` structure is real.* This step tested that by
building a world which satisfies it by construction — and **it is false as stated**.

The construction: six maintenance needs, each low for the first 2 ticks of every `PERIODS[k]` ticks,
with periods `(5,7,11,13,17,19)` pairwise coprime so the Chinese remainder theorem guarantees every
pair eventually co-occurs. Measured:

| | words | pairs co-occurring | behaviour classes | bits |
| --- | ---: | ---: | ---: | ---: |
| at 323 ticks (all 15 pairs co-occur) | 37 | **15/15** | **680** of 720 | 9.41 |
| at 1,616,615 ticks (full lcm, all 64 subsets) | 64 | 15/15 | **720** | 9.49 |

So satisfied pairwise co-occurrence yields **680 of 720 orders — not the full structure**. The
criterion AC25 gave is **necessary but not sufficient**, and the miss is 40 orders.

Why: an observation is read by *first match*, and co-occurrence inside a larger word does not
isolate a comparison — a third signal present in the same word can pre-empt it. This is the same
effect AC25 itself measured from the other side, in the triples row (all triples → 360 classes,
fewer than all pairs' 720).

**The correct criterion: for every pair `(i,j)`, the world must present an observation equal to
exactly `{i,j}`** — the pair and nothing else. AC25's "all pairs" family satisfied that by
construction (it *is* the set of exact pair words), which is why it reached 720, and that specific
satisfying instance is what I over-generalized from.

## Consequences for the design

- The cyclic independent-needs construction **does** reach the full structure, but only at the full
  conjunction period (1.6M ticks here) — because that is when exact pair words finally occur. It is
  not a design you would ship and wait for.
- Therefore the scaled world should present **isolated pairs deliberately** — schedule or drive the
  need patterns so that each exact pair occurs early — rather than relying on independent
  oscillators to drift into every combination.
- Measured discrimination among designs, and the two controls:

| design | words | pairs | classes | bits |
| --- | ---: | ---: | ---: | ---: |
| independent coprime needs, at first pair time | 37 | 15/15 | 680 | 9.41 |
| independent coprime needs, at full period | 64 | 15/15 | 720 | 9.49 |
| **control:** needs made mutually exclusive by epochs (the frozen habit) | 10 | **3/15** | **8** | **3.00** |
| **control:** the frozen world's own signals (masks 4,8,16,32; bit 5 unset; one region per run) | 3 | — | **2** | **1.00** |

The epoch control is the frozen world's habit applied to the same six needs — one group live at a
time — and it costs almost everything: 3 of 15 pairs, 3.00 bits. The frozen world's own signals
reproduce 2 classes / 1.00 bit, matching AC24 and AC25 for the third time by yet another route.

## What this means for the "broader developmental function" line

The line has now been corrected twice by measurement, and the corrections moved in the same
direction both times — the nominal number was not the real number:

1. **AC24**: the frozen controller's four positions are worth **1.00 effective bit**, not the 4.58
   of its permutation count, because two positions can never fire.
2. **AC26**: pairwise co-occurrence buys **680/720**, not 720; only *exact pair witnesses* buy the
   whole order. AC25's own triples row was the warning sign, and I read it as a curiosity instead of
   as the counterexample it was.

The design requirement is now: **six live signals, each pair presented in isolation.** That is a
property of how the world *schedules* its demands, and it is checkable by enumeration before any
chemistry exists — which remains the point of doing it here.

## Not built, plainly

- **No chemistry, no organism, no world.** This is synthetic signal logic and arithmetic over
  observation words. Nothing has been run in a new world, and no organism has been changed.
- **No protocol and no final seeds**, and no claims. The numbers are properties of synthetic
  reachability families.
- **Nothing about the organism's experience, understanding or life**, and none of this is offered as
  evidence toward them. Counting distinguishable input-output behaviours of a rule table is a
  statement about a rule table and a world's demand pattern.
- **The two endpoints the open item names** (random-fallback survival; retention of the acquired
  function) remain untouched; this is all upstream of them.

## The next step

Build the world's demand schedule so that each exact pair of the six needs is presented in
isolation early, verify 720 classes by enumeration, and only then write the reaction chemistry.
Then the scaled acquisition, then a protocol.

## Artifacts

`ac26_signals.py`, `test_ac26.py`, `ac26_signals_v1.json`. Related: `ac25_confront.py`,
`AC25_CONFRONT_v1.md`, `ac24_functional.py`, `AC24_FUNCTIONAL_v1.md`, `ac23_body.py`.
