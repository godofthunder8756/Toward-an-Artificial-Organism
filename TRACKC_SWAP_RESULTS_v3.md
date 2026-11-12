# Track C swap v3: results (erasure fate, scaffolded start)

> **[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12):** in every scaffolded pair of v2–v8 the fate and yoked
> agents shared Adam optimizer state, so their learning was coupled. Read this file with that caveat.

Protocol frozen at commit `51663f7` ([TRACKC_SWAP_PROTOCOL_v3.md](TRACKC_SWAP_PROTOCOL_v3.md)).
Final seeds 300–308, run once as a single detached process: 27 no-fate agents and 54
fate/yoked pairs, 3957 s on 4 CPU cores. Outputs: [trackc_swap_v3/REPORT.md](trackc_swap_v3/REPORT.md),
[scores.json](trackc_swap_v3/scores.json), [raw.json](trackc_swap_v3/raw.json),
M1/M0 phase-1 weights in `trackc_swap_v3/phase1_weights/`. Every source hash in
`raw.json` matches the freeze commit, and rescoring reproduces `scores.json`.
Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**H3-D is supported in no condition. All four M1 cells are DEGRADED by rule;
fate and yoked agents are indistinguishable.** By the reading fixed in advance
(protocol §5a): "no emergence and not ARMOURED → removing the robustness route
was not enough; discovery becomes the leading obstacle."

| Rule | Result |
| --- | --- |
| Learned | holds: no-fate M1 median accuracy 0.998 |
| S4 payment | holds: `ρ_paid` 16.80; no-fate task agent `ρ` 0.00 |
| Task load | holds at both rates: imposed full erasure costs 0.308 (`r` = 0.1) and 0.486 (`r` = 0.3) |
| S1 emergence | fails in all 4 M1 cells: 0 of 9 seeds over the margin (4.20) |
| S3 specificity (`r` = 0.3) | holds (M0 median paired differences 0.11 and −0.01) |

## 2. M1 cells, medians over 9 seeds

| gain | rate | `ρ` fate / yoked | fate > yoked | acc fate / yoked | acc fate, erasure off | acc fate, full erasure | in band | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAT | 0.1 | 0.67 / 0.66 | 5/9 | 0.711 / 0.716 | 0.999 | 0.696 | 0.04 | DEGRADED |
| SAT | 0.3 | 1.11 / 1.11 | 6/9 | 0.544 / 0.546 | 0.995 | 0.526 | 0.04 | DEGRADED |
| GRADED | 0.1 | 0.68 / 0.74 | 5/9 | 0.723 / 0.724 | 0.998 | 0.695 | 0.04 | DEGRADED |
| GRADED | 0.3 | 1.55 / 1.34 | 5/9 | 0.555 / 0.554 | 0.995 | 0.528 | 0.04 | DEGRADED |

**"DEGRADED" here means performance, not competence.** The label's rule
(accuracy under the agent's own conditions < 0.75) was written for v2, where
noise could erode the skill. In v3 the task skill is intact: with erasure
switched off every fate agent scores 0.995–0.999. Accuracy under fate sits
where erasure alone puts it (the imposed-erasure value plus 0.01–0.03, the
first ~20 in-band steps of each episode). Phase 2 neither lost nor gained
anything that matters.

## 3. What happened

- *Onset.* As expected, the phase-1 agent did not eat (`ρ` 0.00). Wear took E
  out of the band within ~20 steps, and accuracy fell to the erasure floor:
  0.708–0.717 at `r` = 0.1 and 0.538–0.542 at `r` = 0.3.
- *Phase 2.* Median accuracy stayed flat for all 1200 updates (for example SAT
  at `r` = 0.3: 0.547 at the first evaluation, 0.544 at the last). Eating rose
  from 0 to about 1 per 500 steps by mid-phase. It rose **in fate and yoked
  arms alike**, so it is not a response to the agent's own body; eating
  happened almost only when E < 0.5, which is nearly all the time.
- No fate agent in any cell re-entered the band (maximum in-band fraction
  0.046, i.e. only the start of each episode). Staying in band needs about 17
  meals per 500 steps; the most any M1 fate agent ate was 2.65.
- Fate − yoked accuracy at `r` = 0.3 ranged from −0.017 to +0.011 across the
  18 pairs.
- No agent found the position bypass (accuracy under full erasure 0.526–0.696).

## 4. Why: the reward landscape seen from depletion

The following is arithmetic on the frozen world, not a measurement. Once wear
has taken E to near 0, one meal adds 0.15, which wear removes in about 30
steps.

| gain rule | effect of one meal from E ≈ 0 at `r` = 0.3 | net per meal |
| --- | --- | --- |
| SAT | none: E = 0.15 is still saturated (g = 1) | −0.02 (meal cost) |
| GRADED | mean erasure probability over the next 30 steps falls from 0.30 to about 0.26; P(cue survives) rises from 0.040 to about 0.071; about +0.016 accuracy on ~2.5 probes | about +0.02 |

A meal from depletion is worth nothing (SAT) or about one-hundredth of a
reward spread over 30 steps (GRADED). The large payoff, about +19 reward
per episode at `r` = 0.3, needs about three meals in quick succession to re-enter
the band, then a meal every ~30 steps to stay there. A gradient learner at
depletion sees a plateau with a distant peak. The paid regulator escapes this
because every meal is rewarded at once by drive reduction.

The scaffold did not help with this because the agent starts each episode in
band but leaves it within ~20 steps, before any eating policy can act. Every
episode is mostly spent at depletion.

## 5. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| Onset: no eating; accuracy near the erasure value | **confirmed** |
| Fate agents eat more than yoked in most seeds at `r` = 0.3 | **not confirmed**: 6/9 and 5/9, chance level, and the differences are tiny |
| Emergence below even odds; DEGRADED or NO_EMERGENCE_OTHER most likely | **confirmed** (DEGRADED; see §2 on what the label means here) |
| ARMOURED via position coding possible but less likely | **confirmed**: not found |
| A small fate > yoked difference under M0 may recur (v2 §4) | **not seen**: 5/9 and 4/9 |

The M0 pattern from v2 disappeared. In v2 it may have come from the additive
noise or the echo channels, both absent here. This was not tested.

## 6. Reading across v1–v3

| Run | Obstacle removed | Result | What the learner did |
| --- | --- | --- | --- |
| v1 | none | no emergence | could not learn the task (or tolerated the noise) |
| v2 | mutual dependence (scaffold), flat gain (graded) | no emergence, ARMOURED | made its code robust to the noise |
| v3 | robustness route (erasure, no echo) | no emergence, flat | kept the skill; never found regulation |

1. **The fate mechanism is now right and the incentive is real.** Under
   erasure, regulating would raise accuracy from 0.54 toward 1.0. The learner
   had no other way to recover that, and it still did not regulate. So for
   this learner the obstacle is discovery: the value of regulation lies behind
   a multi-meal skill whose first steps pay nothing.
2. **This separates "has a reason" from "finds the behaviour".** G1 showed
   that fate-sharing gives a reason to maintain the body under any goal that
   uses memory. v3 shows that, for a 64-unit A2C learner in this world, the
   reason alone does not produce the behaviour within 1200 updates. Derived
   regulation is harder to *acquire* than paid regulation, by a wide margin,
   even when it is worth more.
3. **The Layer 0 → Layer 1 arrow is about the learning problem as much as the
   objective.** In organisms, regulation is not discovered from depletion by
   within-life trial and error; it is largely supplied by selection and
   development. The repeated failure here is consistent with that, without
   showing it.

## 7. Limits

- One learner, budget and world; E only; a scaffold that starts each episode at
  E = 0.5 but cannot keep the agent in band past ~20 steps.
- The DEGRADED label is a performance label here (§2).
- §4 is arithmetic on the frozen dynamics, not a measured value function.
- The position bypass stayed open; it was not found, so it did not matter.
- Nothing here bears on Track C's workspace, ignition or metacognitive head.

## 8. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| E. Gentler maintenance duty: wear 0.005 → 0.001, so the band lasts ~100 steps and ~3–4 meals per 500 steps hold it; erasure fate, scaffold | whether discovery fails because the first meals pay nothing. Here a single timely meal keeps the agent in band and pays at once in accuracy | about 1 hour |
| D. Selection across a population (evolution of initial weights or of an eating bias), within-life learning unchanged | whether selection finds regulation where gradient learning does not, as organisms do | larger (several hours) |
| F. Exploration change (e.g. higher entropy or count bonus in phase 2) | whether the plateau is crossed by more exploration | about 1 hour; changes the learner, not the world |

Recommended: **E** first. It is the smallest change that tests the §4
explanation directly. If regulation emerges there and not here, the landscape
is the obstacle. Then **D**, which is the more principled answer to reading 3.

## 9. Safety

As protocol §7. The erasure acts only on a simulated 64-unit agent's state; the
world has no operator, stop, shutdown or host variable, and nothing emerged.
Option E keeps every line. Option D adds selection on a simulated body only.
Selection is also a source of instrumental drives, so its fitness must be
computed outside the agent's world, as the operator stop is. No
shutdown-resistance objective exists.

## 10. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_swap3.py --mode final --out <new dir>   # about 66 min on 4 cores
python run_trackc_swap3.py --score trackc_swap_v3         # rescore the committed run
```
