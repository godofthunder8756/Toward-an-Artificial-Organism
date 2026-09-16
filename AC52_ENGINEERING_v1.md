# AC52 engineering: the six-region order is combinatorially real but not yet acquirable

2026-09-15. `ac52_learnability.py`, engineering prerequisite. **No protocol, no final seeds, no claim.**
This measures the bounded precursor to AC28's next step (acquisition + retention): is the 720-order
structure *learnable* in the AC28 chemistry, or is the fitness landscape flat?

## The measurement

Score each order by births + final survival over 8 passes of the deliberate exact-pair schedule
(`ac27_schedule.pair_round_schedule`), with the imposed demand landed in the body so the action is
supportable, and site recycling (sites expire, births refill empty slots). Hill-climb (steepest ascent
over swaps) from 8 random starts.

## Result: the landscape is flat

- **8 starts → 8 distinct local optima**, climbs stall in 0–2 steps.
- **Score spread 2.0** (20 vs 22, of 24 possible sites) — a ~10% spread, not a graded optimum.

The order barely moves births or survival. It is not acquirable by search, because there is no gradient.

## Why, and what it means for the build

The order's only effect is *which region is renewed first* when two are urgent, and under the imposed
schedule every region's urgency is landed regardless, so the order changes only timing — not the number
of births (capped by one empty slot per region, AC28's own noted limit) and barely survival. The order
structure (720 classes / 9.49 bits, AC25/AC27/AC28) is a property of *which action fires*, not of
survival. It is real combinatorially and dynamically inert.

So the acquisition/retention build cannot proceed on the current chemistry: there is nothing to acquire.
The missing ingredient is an **emergent demand** that makes the order *load-bearing* — a stress regime
that rewards the right renewal priority (the exact mechanism AC50 demonstrated in the self-funded world:
a regime reversal that makes high-value regions high-stress, so the order's priority determines which
sites survive). That is the concrete next build: give the six-region chemistry an emergent stress regime
(the "scaled body" AC28 flagged as not built), re-measure learnability, and only then add the register
and re-acquisition.

## What this does and does not establish

- **Establishes**: the six-region order structure is not acquirable in the AC28 chemistry as it stands;
  the fitness landscape is flat. The developmental-function build is blocked on an emergent demand, not
  on a register.
- **Does not establish**: any claim about an organism. Prerequisite only. Not autopoiesis, closure, or
  life.

## Artifacts

`ac52_learnability.py`. Related: `AC28_REGIONS_v1.md` (the chemistry), `AC27_SCHEDULE_v1.md` (the
schedule), `AC25_CONFRONT_v1.md` (the 720-class criterion), `AC50_RESULTS_v1.md` (the emergent-demand
mechanism this needs).
