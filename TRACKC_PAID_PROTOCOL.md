# Track C swap option R: derived against paid regulators (frozen before the run)

Authorized by the PI on 2026-11-12 ("Proceed with R."). Astra review waived by
the PI for this stage. This file, [`run_trackc_paid.py`](run_trackc_paid.py),
the new module [`trackc_swap/paid.py`](trackc_swap/paid.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before any final
seed runs; that commit is the freeze. No consciousness claim.

## 1. Question

The swap line has shown that a body variable a learner depends on comes to be
regulated without any evaluator paying for regulation (v6–v8). The
[route assessment](TRACKC_ROUTE_ASSESSMENT_v1.md) noted that the thesis claims
more: that regulation grounded in the system's own dependence differs from
regulation an evaluator pays for, in what is built on it.

**Does a derived regulator differ downstream from a paid regulator that
regulates equally well?**

## 2. Design

Cell: SAT gain, `r` = 0.3, in the v7/v8 world (echo-free, wear 0.001, erasure
also relocates). This was v7's primary cell (8 of 9 regulators).

**Stage 1: training.** Per seed, three agents start from the same phase-1
weights (1200 updates, no fate) and train for 3600 updates in lockstep:

| Arm | Erasure | Reward |
| --- | --- | --- |
| DERIVED | its own E decides (fate) | task only |
| YOKED | replays the derived agent's gains | task only |
| PAID | replays the same gains | task plus the homeostatic reward |

- The homeostatic reward is Track B's drive-reduction reward on eating, the
  program's standing definition of a paid regulator (the DRIVE objective's
  term, unchanged), at weight 1.
- PAID is a yoked agent with payment added. Its erasure does not depend on
  its own E, so E matters to its evaluator and not to its own memory.
- Replayed erasure is used for PAID, not zero erasure, because option P found
  that training under erasure shapes how E is encoded even in yoked agents.
  PAID and DERIVED then differ in the ground of regulation and in nothing
  else that can be equalized.
- The payment is not observable: the previous-reward input is zero in this
  world.

**Stage 2: downstream measures** on the frozen stage-1 weights, all with
erasure off so that every arm is tested in the same world:
- options P and Q's measures: E retention, the anticipation index, post-meal
  suppression S, and regulation with interoception shuffled;
- four world shifts the agents never met: bolus 0.10 (from 0.15), wear
  doubled, interoceptive delay 10 (from 5), interoceptive noise 0.05 (from
  0.02). *Robustness* is the mean in-band time over the four shifts, divided
  by the agent's own unshifted in-band time.

**Stage 3: withdrawal.** Four agents continue training for 1200 updates in
lockstep:

| Arm | Starts from | Change |
| --- | --- | --- |
| DKEEP | derived | none; its gains are replayed to the other three |
| DCUT | derived | erasure now replayed: **the dependence is removed** |
| PKEEP | paid | none |
| PCUT | paid | homeostatic reward removed: **the payment is removed** |

After the cut, DCUT and PCUT are in the same condition (replayed erasure,
task reward only). They differ only in history.

Seeds 900–917 (18, fresh). Final weights of all seven arms are saved.
Estimated run time: about 2 hours on 4 cores.

## 3. Calibration (disclosed)

CALIBRATION_PLACEHOLDER

## 4. Decision rules

**Regulator** (v6's criterion, unchanged), against the seed's yoked agent:
- in band ≥ 0.60;
- eat rate at E < 0.5 at least twice that at E ≥ 0.5;
- in band at least 0.15 above the yoked agent's.

It is applied to DERIVED and to PAID in their stage-1 evaluation: derived
under its own fate, the others replaying its gains.

**Usable seed:** both DERIVED and PAID are regulators, and their in-band
times differ by at most 0.10. This is the "regulates equally well"
condition. All claims are judged on usable seeds only.

**Validity:** no-fate median task accuracy ≥ 0.90. Otherwise every claim is
INVALID. With fewer than 10 usable seeds (or usable pairs for a measure), a
claim is UNDETERMINED.

**R1–R3, two-sided.** For each measure, a paired sign test of derived against
paid over usable seeds, at p ≤ 0.05:
- **R1:** the anticipation index (state);
- **R2:** post-meal suppression S (behaviour);
- **R3:** robustness to world shifts.

Labels: DERIVED_AHEAD, PAID_AHEAD or NO_DIFFERENCE_DETECTED.

**R4, directional.** A cut arm has *dropped* in a seed if its in-band time is
at least 0.05 below its keep arm's.
- Derived follows its dependence if DCUT dropped in at least 70% of usable
  seeds.
- Paid follows its payment if PCUT dropped in at least 70%.

Labels: BOTH_FOLLOW_THEIR_GROUND, ONLY_DERIVED_DROPS, ONLY_PAID_DROPS or
NEITHER_DROPS.

On power and multiplicity:
- With 12 usable seeds the sign test needs 10 of 12; with 14, 12; with 16, 13.
  Only consistent differences can be detected.
- Three two-sided tests are run at 0.05 with no correction. A single
  difference among the three is therefore weak evidence, and will be reported
  as such.

Descriptive: every measure by arm (including YOKED); the same comparisons
over all seeds where both regulate, ignoring the matching rule; DCUT against
PCUT; training curves; task accuracy.

## 5. Readings, fixed in advance

- **DERIVED_AHEAD on R1 or R2** → the ground of regulation shapes what is
  built on it. A system that regulates because it depends on the variable
  models its body more predictively than one paid to regulate. This would be
  the first direct support for the thesis's claim, at this scale.
- **PAID_AHEAD on R1 or R2** → an evaluator's reward buys a better model of
  the body than dependence produces. That counts against the thesis on that
  measure: here, grounding by an evaluator is no worse.
- **R3 either way** → a functional difference between the two kinds of
  regulator, in the direction found.
- **NO_DIFFERENCE_DETECTED on R1–R3** → on these measures and at this scale, a
  derived regulator and a paid one are the same kind of thing downstream.
  What differs is only what keeps the regulation in place (R4). The thesis
  gets no support from this experiment. The next step is then S
  (self-evaluation), where G1 predicts the larger effect.
- **R4 BOTH_FOLLOW_THEIR_GROUND** → each regulation lasts only while its
  ground does: dependence for one, payment for the other. This is G1's
  operational point shown in a learner. It is expected, and it does not by
  itself show a downstream difference.
- **R4 NEITHER_DROPS** → over 1200 updates regulation persists as a habit
  once learned. Withdrawal at this length says nothing about the ground.
- **R4 only one drops** → the two regulations differ in how firmly they are
  held once their ground is gone. Report the direction.

## 6. Expectations, stated before the run

- Derived regulators: at least 14 of 18, about 80%.
- Usable seeds at least 10: about 75%.
- R1: paid ahead about 40%, no difference about 40%, derived ahead about 20%.
  The paid reward depends on E at the moment of eating, which rewards a
  precise current estimate directly.
- R2: paid ahead about 35%, no difference about 45%, derived ahead about 20%.
- R3: no difference about 55%.
- R4: derived cut drops about 55%; paid cut drops about 55%; both about 35%.
  The only pressure against eating after a cut is its small cost (0.02 per
  meal), so extinction may be slow.

I expect the thesis-favourable outcome (derived ahead) to be the least likely
of the three on R1 and R2.

## 7. Engineering before the freeze

- **Smoke run:** seeds 9000–9001, horizon 100, 10 phase-1 updates, 30 stage-1
  updates and 10 withdrawal updates. It checked the three stages, weight
  saving, report and rescoring.
- **Tests:** seven new unit tests (71 in total). They cover:
  - the paid reward: it equals the task reward plus the DRIVE objective's
    drive term at every step; the observation is unchanged; pay 0 gives the
    task reward;
  - the derived and yoked arms' seeding, identical to v7's;
  - the per-seed record, and that calibration sees exactly the stage 1 the
    final run would;
  - the sign test;
  - the decision rules on synthetic data, including the matching rule,
    UNDETERMINED and INVALID;
  - the final configuration, with v6's regulator constants unchanged;
  - the absence of operator variables.
- No final seed has run.

## 8. Safety

As v8 §7. The world has no operator, stop, shutdown or host variable. Erasure
and relocation act only on a simulated 64-unit agent. The homeostatic reward
pays a simulated agent for eating simulated food.

The withdrawal stage removes a simulated dependence or a simulated payment
during continued training. It is not an operator stop, and it is not modelled
inside any agent's world or return: no agent can observe the cut, predict it
or act on it. X1–X5 hold unchanged. No shutdown-resistance objective exists.

## 9. Claim ceiling

At most: for this learner (64-unit GRU, A2C) in this world and cell, whether
derived and paid regulators that regulate equally well differ in anticipation,
post-meal suppression or robustness to four world shifts, and whether each
loses regulation when its own ground is removed.

Not shown either way:
- other measures of what is "built on" regulation, including self-evaluation;
- other learners, worlds or forms of payment;
- Track C's modules or layers;
- any phenomenal property.
