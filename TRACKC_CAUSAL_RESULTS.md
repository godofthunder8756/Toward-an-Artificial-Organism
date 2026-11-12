# Track C swap option Q: results (causal probes of the regulators)

> **[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12):** in every scaffolded pair of v2–v8 the fate and yoked
> agents shared Adam optimizer state, so their learning was coupled. Read this file with that caveat.

Protocol frozen at commit `3e396b4` ([TRACKC_CAUSAL_PROTOCOL.md](TRACKC_CAUSAL_PROTOCOL.md)).
The 42 regulators, 21 fate non-regulators and 42 yoked partners of v7 and v8
were run once, with no training: 168 s on 4 cores. Outputs:
[trackc_causal/REPORT.md](trackc_causal/REPORT.md),
[scores.json](trackc_causal/scores.json), [raw.json](trackc_causal/raw.json).

Integrity checks:
- All 12 source hashes match the freeze commit.
- All 105 weight-file hashes match the committed v7 and v8 weights.
- Rescoring reproduces `scores.json`.
- Under their own fate, regulators' in-band time reproduces their scored
  value (median difference +0.002).

Not reviewed by Astra (waived by the PI). No consciousness claim. The route
check the PI asked for is in
[TRACKC_ROUTE_ASSESSMENT_v1.md](TRACKC_ROUTE_ASSESSMENT_v1.md); §6 says what
these results add to it.

## 1. Outcome

| Question | Frozen verdict | Result | Needed |
| --- | --- | --- | --- |
| **Q-a** the memory of a meal holds back eating before interoception reports it (S ≥ 0.10) | **DOES NOT HOLD** | 26 of 42 regulators; median S 0.13 | 30 |
| **Q-b** under its own fate, regulation needs interoception | **HOLDS** | 42 of 42 regulate; 42 of 42 lose it under the shuffle | 30 |
| **Q-c** erasure contingent on own E supports regulation (in band higher by > 0.02 than under scrambled erasure) | **DOES NOT HOLD** | 22 of 42; median difference 0.021 | 30 |

Two of the three claims fail their frozen bar. In both, the effect is present
in nearly every regulator, but it is small.

## 2. Q-b: regulation is closed-loop through interoception

This is the clean result. It answers the question option P left
UNDETERMINED.

| REG (42), under own fate | intact | interoception shuffled |
| --- | --- | --- |
| regulate (in band ≥ 0.60 and timing ≥ 2) | **42** | **0** |
| in band (median) | 0.701 | 0.450 (max 0.52) |
| eat timing ratio (median) | 3.9 | 0.95 |

In the condition the agents were trained in, every regulator regulates. With
its interoceptive input scrambled, none does: the eat timing disappears
entirely. Erasure and relocation still followed each agent's own E in the
shuffled condition. So erasure events alone do not carry regulation.

## 3. Q-a: the anticipation is used, but weakly

The suppression index S is the drop in readiness to eat 2–5 steps after a
meal, before interoception has reported the meal, against steps with the same
reading and no recent meal.

| Group | S (median) | S > 0 | S ≥ 0.10 |
| --- | --- | --- | --- |
| **REG** (42) | **0.132** | 42 of 42 | 26 of 42 |
| NREG (21) | 0.054 | 20 of 21 | 1 of 21 |
| YREG (42) | −0.011 | 16 of 42 | 3 of 42 |

- **The frozen claim fails:** 26 of 42 regulators reach S ≥ 0.10, and it
  needed 30.
- **The effect exists and is specific to fate.** Every regulator has S > 0,
  and every regulator exceeds its own yoked partner (42 of 42). Yoked
  partners show none (median −0.01).
- **It is small.** A typical regulator is 13% less ready to eat after a meal
  it has not yet sensed. The range is 0.005 to 0.66.
- **It is mostly a SAT effect** (post hoc):

  | Regulators trained under | n | S (median) | S ≥ 0.10 |
  | --- | --- | --- | --- |
  | SAT | 24 | 0.235 | 21 |
  | GRADED | 18 | 0.086 | 5 |

  The pooled claim failed because GRADED regulators suppress little.
- **Link to the representation** (post hoc): across regulators, S correlates
  with option P's anticipation index (Spearman 0.38).

**Habit or estimate?** The protocol named the by-reading pattern as the
check. It is mixed:

| Pre-meal reading | < 0.35 | 0.35–0.40 | 0.40–0.45 | 0.45–0.50 |
| --- | --- | --- | --- | --- |
| S, REG (median) | 0.090 | 0.180 | 0.189 | 0.100 |

- A fixed habit of not eating twice would give the same S at every reading.
  It does not: S rises from the lowest bin to the next in 41 of 42
  regulators. After a meal from very low E the agent is still low, and it
  stays readier to eat.
- An estimate of E predicts S highest in the top bin, where the meal takes
  the agent above the band. S falls there instead, in 34 of 42. Readiness to
  eat is already low at those readings (0.17 against 0.50 in the lowest bin),
  so a floor may be involved. That is not established.

So the reading-dependence is real at the low end and not as predicted at the
top.

## 4. Q-c: erasure helps at test time, mostly whether or not it tracks E

| REG (42), in band (median) | own fate | scrambled erasure | erasure off |
| --- | --- | --- | --- |
| all | 0.701 | 0.677 | 0.638 |
| SAT (24) | 0.742 | 0.705 | 0.692 |
| GRADED (18) | 0.675 | 0.662 | 0.579 |

- **The frozen claim fails:** own exceeds scrambled by more than 0.02 in 22
  of 42 regulators.
- **Both steps are consistent but small** (post hoc):
  - scrambled exceeds off in 35 of 42 (median +0.027);
  - own exceeds scrambled in 37 of 42 (median +0.021).
- **The pre-stated reading for this pattern applies in the main.** Erasure of
  any kind raises in-band time, and the link to the agent's own E adds a
  little. Roughly 60% of the gap between "off" and "own" is reproduced by
  erasures that carry no information about the body.
- **The two gains differ.**
  - Under GRADED, erasure of any kind accounts for nearly all of the gap
    (off is 0.10 lower; contingency adds 0.01).
  - Under SAT, the contingent part is larger (15 of 24 above the bar).
- **A reset state is somewhat readier to eat.** At in-band readings, the
  zeroed state's readiness exceeds the carried state's in 27 of 42 regulators
  (0.18 against 0.14). The same holds in 31 of 42 yoked partners, so it is
  not specific to regulators.

This explains option P's unexpected in-band drop with erasure off. These
agents were trained with erasure, and they forage slightly more when it
occurs. It is a minor, mostly generic effect. It does not amount to a second
interoceptive channel.

**Disclosed:** the scrambled condition did not match the total number of
erasures. Regulators received a median 8594 against 6174 under own fate.
Scrambling keeps each step's draws, but the agents then spend more time out
of band, which raises later draws.

## 5. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| Q-a holds, about 55% | **does not hold**: 26/42 (all 42 positive) |
| If so, S rises with the reading, about 50% | **partly**: rises from the lowest bin (41/42), falls at the top (34/42) |
| Q-b holds, about 90% | **holds**: 42/42 |
| Q-c holds, about 50% | **does not hold**: 22/42 (37 positive) |
| ψ₀ exceeds ψ in most regulators, about 60% | **confirmed** (27/42), but not specific to regulators |
| At least 38 of 42 regulate under own fate | **confirmed**: 42 |

## 6. Reading, and what it adds to the route assessment

1. **Regulation in these agents is a closed sensory loop.** This is now a
   frozen positive in the trained condition (Q-b). Sensing E drives the
   timing of eating; nothing else does.
2. **The predictive part is real but thin.**
   - P2 showed regulators' states anticipate their own eating.
   - Q-a shows the policy uses that, in every regulator, by about 13%. It is
     clearly there only where the band is fully safe (SAT).
   - That is evidence of predictive regulation. It is not a strong forward
     model.
3. **The dependence does not double as a sense.** Erasure events add little
   information the agents use (Q-c). The body variable matters to them
   through interoception.
4. **For the route:** the assessment's verdict stands. Q tightened the
   mechanism of the first link and found it mostly reactive.

   For experiment R (derived against paid), the anticipatory component is a
   candidate difference. It is small, though, so R should not rest on it
   alone.

## 7. Limits

- **Q-a and Q-c failed their frozen bars.** The statements about consistent
  small effects (42 of 42, 37 of 42) and the SAT/GRADED split are post hoc.
- **The 0.10 and 0.02 bars were set without pilot data.** Each sits close to
  the median effect, so the pass counts are sensitive to them.
- **The propensity probe is partly off-distribution.** It shows food under
  the agent shortly after a meal, which is uncommon in training.
- **S is a ratio.** At readings where the readiness to eat is already low, it
  is noisy and may hit a floor.
- **Scrambled erasure differs from own fate in total erasures** (§4).
- **One learner, one world.** Nothing bears on Track C's modules or layers,
  or on any phenomenal property.

## 8. Options (none run; each needs its own freeze)

From the [route assessment](TRACKC_ROUTE_ASSESSMENT_v1.md) (§4):

| Option | What it tests | Cost |
| --- | --- | --- |
| **R. Derived against paid** | Train paid regulators (task reward plus a homeostatic reward, no fate) to the same in-band level. Compare them with derived regulators on option P's and Q's measures, and on behaviour when the reward is withdrawn or the world shifts | about 3–4 h |
| S. Self-evaluation | whether fate agents come to know their own reliability from their body history (G1's largest predicted effect) | about 3–6 h; needs a new action or readout |
| G. Generality | a larger learner, a second body variable | about 3–6 h |
| L. GRADED 0.1 with a longer phase 2 | whether the weak-incentive cell reaches majority regulation | about 2–3 h |

Recommended: **R**. It is the first experiment in this line whose outcome
bears on the thesis itself.

## 9. Safety

No training. Saved 64-unit policies were run in the simulated 7×7 world,
which has no operator, stop, shutdown or host variable. The probes scrambled
one simulated input channel, permuted simulated erasure events, and read the
policy's output for a modified observation. X1–X5 hold unchanged. No
shutdown-resistance objective exists.

One point for larger systems: regulation here depended entirely on the
agent's sensing of the variable. Controlling what a system can sense about
what it depends on is therefore a lever on such behaviour. That adds to the
structural constraints X1–X5; it does not replace them.

## 10. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_causal.py --mode final --out <new dir>   # about 3 min on 4 cores
python run_trackc_causal.py --score trackc_causal          # rescore the committed run
```
