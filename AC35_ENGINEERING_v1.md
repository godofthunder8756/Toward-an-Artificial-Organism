# AC35 engineering: the self-funded maintenance endpoint is too weak to carry a claim

2026-09-15. `ac35_survival.py`, engineering only. **No protocol was written and no final seed was run:
the prerequisite failed.** This records the failure, the numbers behind it, and a diagnosis with a
concrete recommendation for the next attempt.

## What was being attempted

AC34 rejected the binary alive/dead endpoint (horizon-unstable) and recommended graded retention in a
world where the organism funds its own maintenance from sites that produce energy. AC35 built exactly
that: production-funded renewals, endpoint = population retained at the end of the run, with the AC33
arm family and a separation-of-minima gate.

## The prerequisite, and its failure

Declared criterion (the same one AC32 used): the spread across orders must exceed the measurement noise
by a factor of at least 10. Measured under regime B over 120 orders:

| quantity | value |
| --- | ---: |
| best order | 19.33 sites retained |
| median | 18.67 |
| worst order | 18.33 |
| **spread** | **1.00 site of 24** |
| per-order noise (8 disjoint seed sets) | **sd 0.30**, values 17.16–18.14 |
| **margin / noise** | **3.39** |
| criterion | ≥ 10 → **NOT MET** |

The noise is **heterogeneous by order**, which is worth stating precisely rather than smoothing over: a
saturated order's rating is nearly deterministic (sd 0), while a near-threshold order swings across a
full site (17.16–18.14). So the cleanest formulation of the failure is that **one order's swing across
seed sets is as large as the entire spread across orders** — the endpoint cannot resolve the difference
it is supposed to measure.

A 1-site spread against 0.30 of noise cannot support an arm comparison: any difference between arms
would be indistinguishable from which seeds they were scored on. That is AC31's failure mode in
advance, and the whole point of measuring the prerequisite first is to find it here rather than after a
frozen run.

## Diagnosis: self-funding equalizes outcomes

The reason is dynamical and, in hindsight, obvious. AC30's world gave a **5.00-site spread** because the
declared income made the budget non-binding and the endpoint measured pure *ordering* quality. Here
production is proportional to the living population, so a population that falls behind **produces less,
which costs it renewals, which costs it sites** — a negative feedback that compresses outcomes. The
population saturates near carrying capacity (76–80% of 24 sites retained for every order) and the
orders converge in performance.

So making the organism pay for its own maintenance does not merely change who pays: it *shrinks the very
spread the endpoint is supposed to measure*. That is a real design constraint on viability endpoints in
this line, and it was discovered for two minutes of compute instead of a frozen run.

## What this implies for the next attempt

A maintenance endpoint needs a **binding income that is not scaled by the organism's own state**, so
that the order has to *choose* which needs to satisfy rather than being equalized by feedback:

1. keep a declared income, but make it **insufficient** — below what full maintenance demands, so every
   tick forces a choice;
2. the endpoint stays **population retained** (graded, and a maintenance measure, not a mere ordering
   measure);
3. the arms and gate shape stay as in AC33/AC35 (separation of minima over the AC33 arm family);
4. and the same prerequisite must be measured and pass — spread/noise ≥ 10 — **before** any protocol is
   written.

That is a different claim from AC33's. AC33 tested whether a released-and-re-acquired order reaches the
new regime's level; the successor would test whether an order keeps a population above a floor when
maintenance is *unaffordable in full* — the AC16/AC18 "relinquish or allocate" shape, in the
six-position world, with a graded endpoint.

## Not done, plainly

- No protocol, no final seeds, no frozen directory, no claims. `ac35_survival.py`'s `SOURCES` list is
  deliberately empty, and its `individual()` machinery is unused by any frozen run.
- Nothing about experience, understanding or life; nothing about autopoiesis. "Maintenance" here means
  sites retained under a cost, and the failed prerequisite is a statement about a measurement's
  resolving power, not about an organism.
- The negative result is not a setback dressed up: it is the second time in this line that a
  prerequisite has stopped a study before its seeds (AC31 was the first), and it cost minutes.

## Artifacts

`ac35_survival.py`, `test_ac35.py`. Related: `AC34_ENGINEERING_v1.md` (which recommended this endpoint),
`AC30_ACQUIRE_v1.md` (the 5.00 spread this endpoint loses), `AC33_RESULTS_v1.md` (the passing study this
would have complemented), `AC31_ENGINEERING_v1.md` (the first prerequisite stop).
