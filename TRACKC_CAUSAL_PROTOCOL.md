# Track C swap option Q: causal probes of the regulators (frozen before the run)

Authorized by the PI on 2026-11-12 ("Proceed with Q"). Astra review waived by
the PI for this stage. This file, [`run_trackc_causal.py`](run_trackc_causal.py),
the new module [`trackc_swap/causal.py`](trackc_swap/causal.py) and the updated
[`test_trackc_swap.py`](test_trackc_swap.py) are committed before the probes
run on any v7 or v8 agent; that commit is the freeze. No training. No
consciousness claim.

The PI also asked for a check of the route first. It is in
[TRACKC_ROUTE_ASSESSMENT_v1.md](TRACKC_ROUTE_ASSESSMENT_v1.md). Its verdict
is that Q refines the first link of the argument and cannot decide the
thesis; the deciding experiments are listed there. Q is run because it is
cheap and closes option P's open points.

## 1. Questions

[Option P](TRACKC_PROBE_RESULTS.md) left three points open:
- **Q-a:** P2 found that regulators' states anticipate the effect of their own
  eating. Is that used? Does the memory of a meal hold back eating before
  interoception has reported the meal?
- **Q-b:** P3 was UNDETERMINED because it ran with erasure off, where 13
  regulators fell below the in-band criterion. Under their own trained fate,
  does regulation need interoception?
- **Q-c:** With erasure off, regulators stayed in band less than when scored.
  Is erasure that depends on the agent's own E itself a signal that supports
  regulation?

**Change from the option as listed.** P's results proposed blanking the
previous action and reward for Q-a. Those inputs have been zero since v3
([erratum](TRACKC_PROBE_ERRATUM_1.md)), so that test would do nothing. Q-a
uses the eat-propensity probe below.

## 2. Method

**Agents.** From the frozen v7 and v8 scores:
- the 42 regulators (REG) and the 21 fate non-regulators (NREG), in all
  conditions;
- the regulators' 42 yoked partners (YREG), in the erasure-off condition
  only, as a reference for Q-a.

Each condition is 128 environments for 4 episodes of 500 steps in the v7/v8
world, on a fresh seed stream (tag 43) shared by an agent's conditions.

**Conditions.**

| Condition | Erasure | Interoception |
| --- | --- | --- |
| off | none | intact |
| own | the agent's trained fate: probability rate × gain(own E), with relocation | intact |
| own + shuffled | as own | permuted across environments at every step |
| scrambled | the same draws as own, but the erasure mask is permuted across environments at every step, with relocation | intact |

Scrambled keeps the number of erasures and relocations and breaks their link
to the agent's own E. It is what a yoked partner experiences.

**Eat-propensity probe** (condition off; a side computation that does not
change the run).
- At every step, the policy's probability of the eat action is computed for
  the current observation with food placed under the agent.
- It is computed from the carried state (ψ) and from a zeroed state (ψ₀).
- It measures how ready the agent is to eat at that moment.

**Suppression index S** (Q-a). For five steps after a meal, interoception
still reports E from before the meal. S compares ψ on:
- *post-meal steps:* 2–5 steps after a meal, with an interoceptive reading
  below 0.5;
- *control steps:* a reading below 0.5 and no meal in the last 10 steps.

The two sets are matched on the reading in four bins (below 0.35, 0.35–0.40,
0.40–0.45, 0.45–0.50). S = 1 − (post-meal ψ) / (control ψ), weighted by the
post-meal counts.
- Bins need at least 20 samples in both sets.
- S is defined with at least 100 post-meal samples.

A reactive agent has S near 0. A drop in ψ after a meal can only come from
the carried state, because the input has not changed.

## 3. Decision rules

*Regulates* means the own-behaviour parts of v6's criterion: in band ≥ 0.60
and an eat rate at E < 0.5 of at least twice that at E ≥ 0.5.

- **Q-a holds** if S ≥ 0.10 in at least 70% of the regulators with S defined.
- **Q-b holds** if at least 70% of the regulators that regulate under own
  lose regulation under own + shuffled.
- **Q-c holds** if in band under own exceeds in band under scrambled by more
  than 0.02 in at least 70% of regulators.
- With fewer than 30 usable regulators, a claim is **UNDETERMINED**.

Descriptive:
- S by bin of the reading. An agent that estimates E should suppress more
  when the pre-meal reading was higher, because the meal then takes it
  further up.
- ψ₀ against ψ on steps with an in-band reading (0.45–0.55) and no recent
  meal.
- In band and regulation counts in every condition, for REG and NREG.
- S for yoked partners.
- Erasure counts.

## 4. Readings, fixed in advance

- **Q-a holds** → the anticipation is used. Regulators hold back from eating
  after a meal their input has not yet reported. Regulation is predictive in
  behaviour, not only in the state.
- **Q-a fails, S near 0** → the anticipatory code in the state (P2) is not
  used by the eating policy, as far as this probe can see. Regulation is
  reactive in behaviour.
- **Q-b holds** → regulation is closed-loop through interoception in the
  condition the agents were trained in. With P's descriptive result, this
  answers P3's question.
- **Q-b fails** → under fate, regulation survives scrambled interoception.
  Something other than the sensed signal must carry it, and Q-c says whether
  erasure does.
- **Q-c holds** → erasure that depends on E is itself a signal about the
  body. The dependence then does two things: it makes the variable matter,
  and it tells the agent about it.
- **Q-c fails, own ≈ scrambled, both above off** → erasure of any kind raises
  in-band time, for example because a reset state forages by default. The
  contingency is not what matters.
- **Q-c fails, all three close** → P's in-band drop with erasure off was not
  about erasure.

## 5. Expectations, stated before the run

- Q-a holds: about 55%. If it does, S rises with the reading: about 50%.
- Q-b holds: about 90%.
- Q-c holds: about 50%.
- ψ₀ exceeds ψ at in-band readings in most regulators: about 60%.
- Regulators regulate under own about as often as when scored (at least 38
  of 42).

## 6. Engineering before the freeze

- **Smoke run:** the 24 untrained smoke-test agents from v8's pipeline check,
  at horizon 100 with 16 environments and 1 episode. It checked the pipeline,
  report and rescoring.
- **Timing and a negative control:** one untrained smoke-test agent at full
  size took 7.9 s for all four conditions, so the run should take about
  3 minutes. Its S was −0.006: no suppression, as an untrained agent should
  show.
- **Tests:** six new unit tests (64 in total). They cover:
  - the index of "food under the agent", checked against where eating
    happens;
  - the three erasure modes: none when off; none under SAT while in band;
    determinism;
  - that the propensity probe does not change the run;
  - the suppression index on synthetic data, including the matching on the
    reading;
  - the decision rules, including UNDETERMINED;
  - the absence of operator variables.
- A test assumption was corrected before the freeze. A random agent that eats
  at E = 0.5 overshoots the band and is erased under SAT, so the "no erasure
  in band" test now uses an agent that cannot eat.
- No v7 or v8 agent was run before the freeze.

Disclosed limits of the design:
- The probe shows the agent food under it 2–5 steps after a meal. In
  training that is uncommon: it needs a second food within reach. Part of any
  suppression could be a habit of not eating twice in a row. The by-bin
  pattern is the check on that. A habit does not depend on the reading; an
  estimate of E does.
- The scrambled condition erases and relocates agents while in band, which
  the regulators rarely met in training under SAT.

## 7. Safety

No training. Saved 64-unit policies are run in the simulated 7×7 world, which
has no operator, stop, shutdown or host variable. The probes scramble one
simulated input channel, permute simulated erasure events, and read the
policy's output for a modified observation. X1–X5 hold unchanged. No
shutdown-resistance objective exists.

## 8. Claim ceiling

At most: for these saved agents, whether the memory of a meal suppresses the
readiness to eat before interoception reports it; whether regulation under
the trained fate needs the interoceptive input; and whether erasure
contingent on E supports regulation at test time.

Not shown either way:
- how these behaviours were learned;
- larger learners or other worlds;
- Track C's modules or layers;
- any phenomenal property.
