# Track C swap option P: results (how regulators represent and use E)

Protocol frozen at commit `394a995` ([TRACKC_PROBE_PROTOCOL.md](TRACKC_PROBE_PROTOCOL.md)).
All 234 saved v7 and v8 agents were run once, with no training: 267 s on 4
cores. Outputs: [trackc_probe/REPORT.md](trackc_probe/REPORT.md),
[scores.json](trackc_probe/scores.json), [raw.json](trackc_probe/raw.json).

Integrity checks:
- All 9 source hashes match the freeze commit.
- All 234 weight-file hashes match the committed v7 and v8 weights.
- Rescoring reproduces `scores.json`.

Not reviewed by Astra (waived by the PI). No consciousness claim.

**[Erratum 1](TRACKC_PROBE_ERRATUM_1.md):** the agents do not receive their
previous action or reward (zeroed since v3). They can infer a meal only from
their view. No number or verdict here changes.

## 1. Outcome

| Question | Frozen verdict | Result | Threshold |
| --- | --- | --- | --- |
| **P1** regulator's state retains interoceptive E more than its yoked partner's | **HOLDS** | 39 of 42 pairs (sign p < 10⁻⁴) | ≥ 70% |
| **P2** regulator's state anticipates the unreported change more than its yoked partner's | **HOLDS** | 41 of 42 pairs (sign p < 10⁻⁴) | ≥ 70% |
| **P3** regulation lost when interoception is scrambled | **UNDETERMINED** | 29 of 29 lose it, but only 29 regulate intact | ≥ 30 regulating intact |

Readings fixed in advance (protocol §5):
- **P1 holds:** regulation came with an internal representation of the body
  variable, and yoked partners with identical erasure histories carry less.
  §2 qualifies what "more" means here.
- **P2 holds:** regulators anticipate E from their own eating before
  interoception reports it. This is a forward model of the body variable, the
  first instance in the program of the predictive regulation Layer 1
  describes.
- **P3 is UNDETERMINED,** one regulator short of the frozen minimum. Every
  regulator that could be tested lost regulation under the shuffle, and
  descriptively all 42 lose the eat timing (§4).

## 2. P1: what regulators' states carry about E

| Group (median) | R²(h → E) | R²(raw input → E) | retention | h beats raw input (gain > 0) |
| --- | --- | --- | --- | --- |
| REG (42) | 0.935 | 0.927 | **1.007** | 26 of 42 |
| YREG (42) | 0.923 | 0.959 | 0.959 | 3 of 42 |
| NREG (21) | 0.932 | 0.957 | 0.973 | — |
| M0F / M0Y (45 each) | 0.294 / 0.308 | 0.976 | 0.30 / 0.32 | — |
| NOFATE (18) | 0.486 | 0.985 | 0.495 | — |

Two findings, one of which qualifies P1:

1. **Every M1-trained agent carries E strongly, regulator or not.** Yoked
   partners, non-regulators and regulators all decode E at R² ≈ 0.92–0.94,
   and E is irrelevant to a yoked partner's return. Agents trained on M0 or
   without erasure carry far less (0.29–0.49).

   So a strong linear code for E comes with training on the memory task
   under erasure. It is not specific to regulation. This is post hoc and
   unexplained here.
2. **What separates regulators is that their estimate of E is better than
   their own input.**
   - In absolute R², regulators lead their yoked partners in only 26 of 42
     pairs.
   - The retention advantage comes mostly from the denominator: a
     regulator's raw input is a worse guide to its current E (RMSE 0.034
     against 0.030). It eats more, so more of its E change is still
     unreported.
   - Its state makes up for that: RMSE 0.031 against 0.041 for yoked
     partners.
   - Descriptively, the state beats the raw input (gain > 0) in 26 of 42
     regulators and 3 of 42 yoked partners. Within pairs the regulator's gain
     is higher in 42 of 42.

So P1's verdict is real, but its content is narrower than "regulators hold
more E". Regulators hold a better *current* estimate of E than their delayed
input gives, which is P2's mechanism.

## 3. P2: anticipation

The anticipation index is the share of the predictable part of
`E_t − E_{t−5}` (in practice, recent boluses) that the state carries:

| Group | anticipation (median) | eats per run (median) |
| --- | --- | --- |
| **REG** | **0.217** | 882 |
| NREG | 0.090 | 813 |
| YREG | 0.083 | 554 |
| YNREG | 0.054 | 588 |
| M0F / M0Y | 0.000 / 0.000 | 290 / 277 |
| NOFATE | 0.216 (unreliable, see below) | 3 |

- **Regulators lead their yoked partners in 41 of 42 pairs**, by about 2.6×.
- **Not an artefact of eating more.** Non-regulator fate agents eat almost as
  much as regulators (813 against 882 per run) but anticipate no more than
  yoked partners (0.090). The index is also normalized by what the input
  window explains.
- **NOFATE's 0.216 is not interpretable.** Those agents ate 3 times in total,
  so the window decoder explains only 0.106 of D, barely above the 0.05
  floor.
- **Partial anticipation, in absolute terms.** Regulators' states carry about
  a fifth of the predictable unreported change. That is enough to move their
  estimate of E ahead of the 5-step-delayed signal (§2), but far from a full
  forward model.

## 4. P3: regulation and interoception

With erasure off, only 29 of 42 regulators met the own-behaviour parts of the
criterion. P3 needed 30, so its frozen verdict is UNDETERMINED.
- **Why 13 fell short:** all 13 failed on in band alone, at 0.41–0.60. Their
  eat timing was intact (ratios 2.1–6.4). Eleven of the 13 are GRADED agents.
- **All 29 that did regulate lost it** under the shuffle.

Descriptively, over all 42 regulators:

| REG (42) | intact | interoception shuffled |
| --- | --- | --- |
| in band (median) | 0.638 | 0.423 (max 0.47) |
| eat timing ratio, E < 0.5 against E ≥ 0.5 (median) | 4.1 | 0.97 |
| meet the timing criterion (≥ 2) | 42 | **0** |

Yoked partners barely change (in band 0.363 → 0.347), and M0 agents do not
change at all (0.274 → 0.274). Regulation is closed-loop through
interoception: scrambling the signal abolishes the eat timing in every
regulator and leaves the others as they were. That is the reading P3 was
meant to test. This statement is descriptive, not the frozen verdict.

**The unexpected part.** With erasure off, regulators stay in band less than
in their scored evaluation (median −0.05), against my expectation (§5). One
possibility, not tested, is that erasure out of band is itself a cue: an
erased (zeroed) state may push the policy toward food. That would make
regulation partly driven by the fate event as well as by interoception.

## 5. Expectations against outcomes

| Stated before the run (protocol §6) | Outcome |
| --- | --- |
| P1 holds, about 65% | **holds**, 39/42; qualified in §2 |
| P2 holds, about 35% | **holds**, 41/42 |
| P3 holds, about 85% | **UNDETERMINED** (29 < 30); 29/29 lose it, and 42/42 lose the timing |
| With erasure off, regulators stay in band at least as much as when scored | **missed**: median −0.05; 13 of 42 fall below 0.60 |
| M0 and yoked agents barely change under the shuffle | **confirmed** |

I did not foresee two things:
- yoked partners carry E as strongly as regulators do;
- removing erasure lowers regulators' in-band time.

## 6. Reading

1. **Regulation in these agents is closed-loop and partly predictive.**
   - They read interoception: scrambling it abolishes the eat timing in every
     regulator.
   - Their states also fold in their own recent eating, so their estimate of
     E runs ahead of the delayed signal: anticipation 0.22 against 0.08 in
     their partners.

   That is the structure Layer 1 describes: regulation of a body variable
   using a model that predicts it, not only reacts to it. Here it is small
   (about a fifth of the predictable change) and linear-decoded.
2. **The representation of E itself is not what fate added.** Agents trained
   on the same task and the same erasure history, but whose E did not
   matter, encode E almost as well. What fate added is the *use* of E (the
   timing) and the *anticipation*. The dependence shaped how the body
   variable is tracked and acted on more than whether it is represented.
3. **For the Layer 0 → Layer 1 thesis:** v6–v8 showed that a dependence the
   system cannot route around produces regulation. This probe shows that the
   regulation is sensory-driven (closed-loop) and comes with a predictive
   component no evaluator asked for.

## 7. Limits

- **P3's frozen verdict is UNDETERMINED.** The closed-loop reading rests on
  descriptive counts. They are unambiguous (42/42 to 0/42), but they are not
  the pre-registered test.
- **P1's retention advantage comes mostly from regulators' weaker raw input**
  (§2). In absolute R², regulators lead in only 26 of 42 pairs. The
  comparison with the raw input (gain), which separates the groups cleanly
  (42 of 42), was declared descriptive.
- **Linear decoders only.** A nonlinear code could carry more in any group.
- **Behaviour was probed with erasure off**, not in the conditions agents
  were trained in, and regulators' in-band time dropped there. Why is not
  established.
- **The M1 agents' strong E code is unexplained**, including the yoked
  partners' eating rates.
- **One learner and one world.** Nothing bears on Track C's modules or
  layers, or on any phenomenal property.

## 8. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| Q. Causal probes on the saved weights: (a) blank the eating-event inputs (previous action and reward) and measure anticipation and behaviour; (b) run with erasure on but interoception shuffled, to rerun P3 in the trained condition; (c) test whether an erased state alone triggers food-seeking | whether anticipation is used, P3 in the trained setting, and the "erasure as cue" possibility | under 1 h, no training |
| G. Generality: the confirmed cells with a larger learner (e.g. GRU 128) or a second body variable | whether regulation, and its predictive component, survive a change of learner or variable | about 3–6 h |
| L. GRADED 0.1 with a longer phase 2 | whether the weak-incentive cell reaches majority regulation | about 2–3 h |

Recommended: **Q**. It needs no training and closes this probe's three open
points: P3 under the trained condition, whether anticipation is causal, and
the in-band drop. G after that.

## 9. Safety

No training. Saved 64-unit policies were run in the simulated 7×7 world, which
has no operator, stop, shutdown or host variable. The probe read internal
states and scrambled one simulated input channel.

The finding adds a mechanism to G1's instrumental-convergence result. Agents
paid only for a task did more than come to protect what the task depends on.
They built a predictive estimate of it and acted on that estimate. At larger
scale, a system that models what its functioning depends on is better at
protecting it.

That strengthens the case for keeping X1–X5 structural:
- The operator's stop must never be modelled inside an agent's world or
  return.
- Nothing an agent's functioning depends on should be something it is in a
  position to protect against its operators.

No shutdown-resistance objective exists.

## 10. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_probe.py --mode final --out <new dir>   # about 5 min on 4 cores
python run_trackc_probe.py --score trackc_probe           # rescore the committed run
```
