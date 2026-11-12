# Track C swap option R: derived against paid regulators (frozen before the run)

Authorized by the PI on 2026-11-12 ("Proceed with R."). Astra review waived by
the PI for this stage. This file, [`run_trackc_paid.py`](run_trackc_paid.py),
the new module [`trackc_swap/paid.py`](trackc_swap/paid.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before any final
seed runs; that commit is the freeze. No consciousness claim.

## 1. Questions

**First, since [swap erratum 1](TRACKC_SWAP_ERRATUM_1.md):** in v2–v8 the
fate and yoked agents of each pair shared optimizer state. This run trains
every agent with its own optimizer. **Does derived regulation hold without
that coupling?** (R0)

**Second, the question R was designed for.** The swap line has shown that a body variable a learner depends on comes to be
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

- **Every agent has its own optimizer**, loaded from a private copy of the
  phase-1 state. This is the first run of the swap line without the coupling
  of erratum 1.
- **The homeostatic reward is a penalty of 0.04 × g(E) at every step**, where
  g is the SAT fate gain: 0 in band, rising to 1 at 0.1 outside it. This is
  the same function that sets the derived agent's erasure probability
  (0.3 × g). The evaluator charges PAID for exactly the states in which
  DERIVED would be erased. §3 explains the choice and the weight.
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
Estimated run time: about 2.6 hours on 4 cores (calibration timing: 1340 s per
seed for stage 1).

## 3. Calibration (disclosed)

Calibration used seeds 9100–9103, which are never scored. Every calibration
run was stage 1 only: it trained and evaluated the three arms, and computed
none of the measures R1–R4 judge. I saw in-band time, eating, timing ratio
and task accuracy per arm, and nothing else.

| Round | Optimizers | Payment | Derived in band | Paid in band | Outcome |
| --- | --- | --- | --- | --- | --- |
| 1 | shared (bug) | drive reduction × 1 | 0.69–0.85 (4 seeds) | 0.44–0.71 | paid under-regulates |
| 2 | shared (bug) | drive reduction × 5, × 20 | 0.64–0.83 (2 seeds) | 0.37–0.61 | **the derived result changed with the paid weight: erratum 1 found** |
| 3 | independent | drive reduction × 1, × 5 | 0.92, 0.95 | 0.59–0.86 | paid cannot match; at × 5 one agent lost the task (accuracy 0.50) |
| 4 | independent | 0.04 × g(E), 0.10 × g(E) | 0.92, 0.95 | 0.93, 0.95 at 0.04; 0.94, 0.97 at 0.10 | **matched at 0.04** |

What calibration showed, and what follows from it:
- **Rounds 1 and 2 are void.** All three agents shared optimizer state, so
  each arm's result depended on the others.
- **With independent optimizers, derived regulation was much stronger** than
  in v7: in band 0.92 and 0.95, timing ratios 18 and 69, task accuracy 0.98
  and 0.99. Yoked partners showed no eat timing (ratios 1.3 and 0.85). These
  are two calibration seeds. R0 tests the same thing on the final seeds.
- **The drive-reduction payment cannot give matched regulation.** It pays
  more for eating from a larger deficit, so its optimum lets E fall low
  before each meal. That caps in-band time near 0.67. A paid agent trained on
  it does not "regulate equally well" as a derived agent at 0.92, however it
  is weighted.
- **The gain payment is the evaluator's analogue of the dependence.** It
  charges for the same states, by the same function. The weight 0.04 is
  roughly what a derived agent loses per step at full gain: imposed full
  erasure costs about 0.48 accuracy on about 40 probes per 500 steps. It gave
  in-band times within 0.01 of the derived agents', and equal task accuracy.

The choice of payment was made on stage-1 quantities only. It was made to
satisfy the matching condition, not to produce any downstream outcome.

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
claim among R1–R4 is UNDETERMINED.

**R0, regulation without the coupling.** It holds if at least 12 of the 18
derived agents are regulators and at most 1 yoked agent is.
- Twelve of 18 is a clear majority. At v6's rate (0.39) it has probability
  about 0.02.
- R0 uses all 18 seeds. It does not depend on the paid arm.

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

- **R0 holds** → derived regulation does not depend on the optimizer
  coupling. The central result of v6–v8 stands for this cell, now with a
  yoked control that learns independently. The rates and timings of v6–v8
  still do not carry over; this run's are the ones to cite.
- **R0 fails** → without the coupling, regulation is not the majority
  outcome here. The line's central result would have to be re-established
  before anything is built on it, and R1–R4 would be moot.
- **What the leak explanation predicts** (descriptive). If the coupling had
  pushed yoked partners along the fate agent's gradient, then with
  independent optimizers yoked agents should:
  - eat less than v7's yoked partners did (median ρ 2.24 there);
  - show no eat timing;
  - encode E less well than option P found (R² about 0.92).

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

These were written after calibration and are informed by it.
- R0 holds: about 85%. Yoked agents show the three leak predictions: about
  70%.
- Usable seeds at least 10: about 85%.
- R1: no difference about 50%, paid ahead about 25%, derived ahead about 25%.
  The two agents now face the same function of E, one through erasure and one
  through a penalty, so I expect similar solutions.
- R2: no difference about 55%.
- R3: no difference about 60%.
- R4: derived cut drops about 55%; paid cut drops about 55%; both about 35%.
  The only pressure against eating after a cut is its small cost (0.02 per
  meal), so extinction may be slow.

I expect "no difference detected" to be the most likely outcome on each of
R1–R3. That is the outcome that gives the thesis no support.

## 7. Engineering before the freeze

- **Smoke run:** seeds 9000–9001, horizon 100, 10 phase-1 updates, 30 stage-1
  updates and 10 withdrawal updates. It checked the three stages, weight
  saving, report and rescoring.
- **Tests:** nine new unit tests (73 in total). They cover:
  - optimizer independence: the old loading pattern shares Adam's state, and
    this run's does not; training one agent leaves another's weights and
    optimizer untouched;
  - the gain payment: it equals 0.04 × g(E) at every step, charges nothing in
    band, and does not change the observation;
  - the drive payment, kept for the record: it equals the DRIVE objective's
    drive term;
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
derived regulation holds with independent optimizers, and whether derived and
paid regulators that regulate equally well differ in anticipation,
post-meal suppression or robustness to four world shifts, and whether each
loses regulation when its own ground is removed.

Not shown either way:
- other measures of what is "built on" regulation, including self-evaluation;
- other cells (SAT `r` = 0.1, GRADED) and the M0 control without the
  coupling;
- other learners, worlds or forms of payment;
- Track C's modules or layers;
- any phenomenal property.
