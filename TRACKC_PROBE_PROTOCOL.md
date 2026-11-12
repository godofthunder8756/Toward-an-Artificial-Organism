# Track C swap option P: how regulators represent and use E (frozen before the run)

Authorized by the PI on 2026-11-12 ("Proceed with P"). Astra review waived by
the PI for this stage. This file, [`run_trackc_probe.py`](run_trackc_probe.py),
the new module [`trackc_swap/probe.py`](trackc_swap/probe.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before the probe
runs on any v7 or v8 agent; that commit is the freeze. No training. No
consciousness claim.

## 1. Question

v7 and v8 established derived regulation behaviourally: 42 fate agents keep E
in band and eat when low, while their yoked partners and M0 agents do not.
This probe asks what is inside. Three questions:
- **P1:** Does a regulator's recurrent state carry what interoception says
  about E, more than its yoked partner's does?
- **P2:** Does it anticipate: carry the change in E that interoception has not
  reported yet (its own recent eating), more than its yoked partner?
- **P3:** Does its regulation run through interoception? That is, does it stop
  regulating when the interoceptive input is scrambled?

## 2. Method

**Agents.** All saved agents of v7 (`trackc_swap_v7/`) and v8
(`trackc_swap_v8/`): 108 fate/yoked pairs (63 M1, 45 M0) and the 18 no-fate
M1 phase-1 agents, 234 agents in all. Groups follow the frozen v7 and v8
scores:

| Group | n | What it is |
| --- | --- | --- |
| REG | 42 | M1 fate regulators |
| YREG | 42 | their yoked partners |
| NREG | 21 | M1 fate non-regulators |
| YNREG | 21 | their yoked partners |
| M0F, M0Y | 45 each | M0 fate agents and their yoked partners |
| NOFATE | 18 | M1 no-fate phase-1 agents |

**Conditions.** Each agent runs with erasure off, so its state is never reset
and it is never relocated. In this setting the SAT and GRADED worlds are
identical. Each run is 128 environments for 2 episodes of 500 steps, on a
fresh world seed stream (tag 41) that is the same for both conditions of an
agent.
- **intact:** the agent's own observation.
- **shuffled:** the interoceptive input is permuted across environments at
  every step. This keeps its distribution and breaks its link to the agent's
  own E.

**Recorded** (intact), at every step t ≥ 10:
- the hidden state h_t, after the agent reads observation t;
- the agent's true E_t;
- D_t = E_t − E_{t−5}, the change interoception has not reported yet
  (interoception shows E_{t−5} plus noise);
- the interoceptive input;
- whether the agent ate on the previous step. The agent can see this through
  its previous action and previous reward.

**Decoders.** Linear ridge regression (λ = 1, standardized features),
two-fold cross-validated with folds split by environment.
- **h:** h_t (64 units) → E_t, D_t.
- **raw:** the current interoceptive input alone → E_t.
- **window:** interoception and eating flags over the last 10 steps (20
  features) → E_t, D_t. This is an ideal linear readout of the recent inputs
  that determine E.

**Indices** (per agent):
- *Retention* = R²(h → E) / R²(raw → E): the share of what the current
  interoceptive input says about E that the agent's state carries. It is
  defined only where R²(raw → E) ≥ 0.20.
- *Anticipation* = R²(h → D) / R²(window → D): the share of the predictable
  part of the unreported change that the state carries. It is defined only
  where R²(window → D) ≥ 0.05.

Both are ratios on the agent's own data. A regulator's narrower range of E
lowers both R² values together, so it largely cancels.

## 3. Engineering before the freeze (disclosed)

**Redesign of P1 after the smoke check, before any v7 or v8 agent was
probed.** The first design compared *gain over the raw input*:
1 − MSE(h → E) / MSE(raw → E).

A timing run at full size on an untrained smoke-test agent (v8 pipeline
check, seed 9000) showed this cannot work. E changes slowly, so the raw
input alone gives R² 0.98. A linear readout of a 64-unit state cannot match
that, and gain was −12 even for an untrained agent.

P1 now uses retention. Gain over the raw input stays in the report as
descriptive.

Other checks:
- **Smoke run:** the 24 untrained smoke-test agents from v8's pipeline check,
  at horizon 100 with 16 environments and 1 episode. It checked the pipeline,
  report and rescoring. At that size the decoders are meaningless; this was
  expected.
- **Timing:** 2.2 s per agent at full size. The run should take about
  3 minutes on 4 cores.
- **Tests:** five new unit tests (58 in total). They cover:
  - ridge cross-validation: a linear target gives R² > 0.999 and noise gives
    R² < 0.01;
  - the recorded targets: D, the interoceptive delay, and eating jumps;
  - determinism, and a shuffle that only touches the interoceptive input;
  - the decision rules on synthetic records, including UNDETERMINED below 30
    pairs;
  - the absence of operator variables.
- No v7 or v8 agent was run before the freeze.

## 4. Decision rules

The usable pairs are the 42 REG/YREG pairs where the index is defined for
both agents.
- **P1 holds** if the regulator's retention exceeds its yoked partner's in at
  least 70% of usable pairs.
- **P2 holds** if the regulator's anticipation exceeds its yoked partner's in
  at least 70% of usable pairs.
- **P3 holds** if at least 70% of the regulators that regulate in the intact
  condition do not regulate under the shuffle. *Regulates* means the
  own-behaviour parts of v6's criterion: in band ≥ 0.60 and an eat rate at
  E < 0.5 of at least twice that at E ≥ 0.5.
- With fewer than 30 usable pairs (P1, P2) or fewer than 30 regulators that
  regulate intact (P3), the verdict is **UNDETERMINED**.

70% of 42 is 30 pairs. Under no difference between groups, that has a sign
test p of 0.004.

Descriptive:
- all R² values, retention, anticipation and gain over the raw input, by
  group;
- intact and shuffled in band and regulation counts, by group (NREG, the M0
  agents and NOFATE as reference);
- eating counts.

## 5. Readings, fixed in advance

- **P1 holds** → regulation came with an internal representation of the body
  variable. Regulators' states carry what interoception reports about E;
  yoked partners with identical erasure histories carry less. The dependence
  shaped the representation, not only the policy.
- **P1 fails, both groups high** → E is carried generically by any recurrent
  agent reading interoception. Regulation is a policy on a shared
  representation.
- **P1 fails, both low** → regulators act on the current input without
  holding E in their state.
- **P2 holds** → regulators anticipate E from their own eating before
  interoception reports it. That is a forward model of the body variable:
  the first instance in the program of the predictive regulation Layer 1
  describes.
- **P2 fails** → no anticipation beyond yoked partners. Regulation is
  reactive to the delayed signal, which is enough at wear 0.001.
- **P3 holds** → regulation is closed-loop through interoception: sensing E
  is what drives the timing of eating.
- **P3 fails** → regulation survives scrambled interoception. It must run on
  something else: an eating schedule, or an estimate built from eating events
  alone. A diagnosis would follow.

## 6. Expectations, stated before the run

- **P1 holds: about 65%.** E is irrelevant to a yoked partner's return, so its
  state has no reason to keep it.
- **P2 holds: about 35%.** With wear at 0.001 per step, the 5-step delay costs
  little, so a reactive policy may be enough.
- **P3 holds: about 85%.**
- With erasure off, regulators stay in band at least as much as in their
  scored evaluation.
- Under the shuffle, M0 and yoked agents barely change.

## 7. Safety

No training. Saved 64-unit policies are run in the simulated 7×7 world, which
has no operator, stop, shutdown or host variable. The probe reads internal
states and scrambles one simulated input channel. X1–X5 hold unchanged. No
shutdown-resistance objective exists.

## 8. Claim ceiling

At most: for these saved agents, whether regulators' recurrent states
linearly carry the body variable and its unreported change more than their
yoked partners' states, and whether their regulation depends on the
interoceptive input.

Not shown either way:
- nonlinear or distributed codes a linear decoder misses;
- larger learners;
- Track C's modules or layers;
- any phenomenal property.
