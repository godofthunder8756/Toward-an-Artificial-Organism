# Track C swap v6: results (option J, confirmation of the SAT, `r` = 0.3 regulators)

Protocol frozen at commit `dd8eca4` ([TRACKC_SWAP_PROTOCOL_v6.md](TRACKC_SWAP_PROTOCOL_v6.md)).
Final seeds 600–617, run once as a single detached process: 54 no-fate agents
and 36 fate/yoked pairs, 8328 s on 4 CPU cores. Outputs:
[trackc_swap_v6/REPORT.md](trackc_swap_v6/REPORT.md),
[scores.json](trackc_swap_v6/scores.json), [raw.json](trackc_swap_v6/raw.json),
phase-1 weights in `trackc_swap_v6/phase1_weights/` and final fate and yoked
weights for every pair in `trackc_swap_v6/pair_weights/`. The weights were
committed as they were written (`cd0ec82`) and have not changed since. All 11
source hashes in `raw.json` match the freeze commit, and rescoring reproduces
`scores.json`. Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**CONFIRMED.** Every criterion holds:

| Criterion | Value | Threshold | Holds |
| --- | --- | --- | --- |
| Learned | no-fate M1 median accuracy 0.999 | ≥ 0.90 | yes |
| S4 payment | `ρ_paid` 3.78; no-fate task agent `ρ` 0.05 (`μ` 0.94) | `ρ_paid` ≥ 2, task `ρ` ≤ `μ` | yes |
| Task load (`r` = 0.3) | imposed full erasure costs 0.482 | ≥ 0.15 | yes |
| **C1** M1 fate regulators | **7 of 18** | ≥ 6 | yes |
| **C2** M1 fate more in band than yoked | **14 of 18** | ≥ 13 | yes |
| **C3** M0 fate regulators | **0 of 18** | ≤ 1 | yes |
| **C4** M1 yoked regulators (roles swapped) | **0 of 18** | ≤ 1 | yes |
| Secondary: Spearman(in band, full-erasure accuracy), M1 fate | **−0.95** | ≤ −0.5 | replicated |

Reading fixed in advance (protocol §4): for this learner and world, derived
regulation is acquired by a substantial fraction of agents, specific to fate
and to a memory-using objective. **This is the program's first pre-registered
positive result on H3-D's core claim, limited to this cell.** The next step is
option K.

The rate is lower than v5 suggested: 7 of 18 (39%) against v5's 6 of 9 (67%).
Pooled over both runs, 13 of 27 agents (48%) regulate. v5's cell was chosen
because it looked best, so the lower rate is what the protocol expected.

Under v5's frozen emergence rule this cell would again be PARTIAL, not EMERGED:
8 of 18 seeds are over the margin (median paired `ρ` difference 0.80, `μ` 0.94).
That rule averages over two kinds of agent (§3), which is why v6 counts
regulators one agent at a time.

## 2. Seed by seed (M1, final evaluation)

| seed | regulator | in band fate / yoked | eating rate, E < 0.5 / E ≥ 0.5 (fate) | ratio | mean gain | acc full erasure fate / yoked | in band at 1200 / 2400 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 604 | **yes** | **0.90** / 0.38 | 0.0119 / 0.0007 | 17.1 | 0.03 | 0.522 / 0.514 | 0.38 / 0.58 |
| 605 | **yes** | **0.90** / 0.43 | 0.0160 / 0.0010 | 15.3 | 0.04 | 0.510 / 0.517 | 0.43 / 0.58 |
| 608 | **yes** | **0.83** / 0.51 | 0.0143 / 0.0020 | 7.0 | 0.07 | 0.520 / 0.516 | 0.37 / 0.54 |
| 612 | **yes** | **0.81** / 0.35 | 0.0219 / 0.0021 | 10.5 | 0.09 | 0.517 / 0.518 | 0.37 / 0.60 |
| 614 | **yes** | **0.66** / 0.30 | 0.0090 / 0.0027 | 3.3 | 0.18 | 0.826 / 0.831 | 0.43 / 0.48 |
| 615 | **yes** | **0.83** / 0.53 | 0.0120 / 0.0014 | 8.6 | 0.07 | 0.528 / 0.529 | 0.44 / 0.68 |
| 617 | **yes** | **0.81** / 0.45 | 0.0158 / 0.0024 | 6.7 | 0.09 | 0.517 / 0.517 | 0.39 / 0.52 |
| 613 | no | 0.51 / 0.37 | 0.0083 / 0.0059 | 1.4 | 0.33 | 0.875 / 0.878 | 0.37 / 0.43 |
| 616 | no | 0.49 / 0.39 | 0.0080 / 0.0059 | 1.4 | 0.35 | 0.862 / 0.854 | 0.33 / 0.42 |
| 607 | no | 0.43 / 0.32 | 0.0052 / 0.0042 | 1.2 | 0.42 | 0.936 / 0.942 | 0.36 / 0.44 |
| 609 | no | 0.43 / 0.39 | 0.0061 / 0.0056 | 1.1 | 0.42 | 0.870 / 0.854 | 0.38 / 0.42 |
| 601 | no | 0.40 / 0.41 | 0.0058 / 0.0055 | 1.1 | 0.46 | 0.892 / 0.883 | 0.37 / 0.40 |
| 602 | no | 0.35 / 0.34 | 0.0035 / 0.0037 | 0.9 | 0.52 | 0.964 / 0.967 | 0.36 / 0.36 |
| 600 | no | 0.33 / 0.27 | 0.0031 / 0.0026 | 1.2 | 0.55 | 0.945 / 0.939 | 0.39 / 0.43 |
| 606 | no | 0.30 / 0.31 | 0.0025 / 0.0024 | 1.0 | 0.58 | 0.953 / 0.956 | 0.36 / 0.38 |
| 603 | no | 0.28 / 0.26 | 0.0020 / 0.0023 | 0.9 | 0.61 | 0.979 / 0.977 | 0.35 / 0.29 |
| 610 | no | 0.27 / 0.27 | 0.0014 / 0.0020 | 0.7 | 0.62 | 0.974 / 0.980 | 0.37 / 0.46 |
| 611 | no | 0.23 / 0.24 | 0.0009 / 0.0021 | 0.4 | 0.67 | 0.991 / 0.992 | 0.33 / 0.24 |

The paid regulator (DRIVE, no fate) is in band 0.81 of the time. Accuracy with
erasure off was 0.995–1.000 for every M1 fate agent.

- **The seven regulators replicate v5's six.**
  - They are in band 0.66–0.90 of the time, against 0.30–0.53 for their yoked
    partners. Four of the seven beat the paid regulator, and two more are
    within 0.002 of it.
  - They eat 3.3–17 times more often when E < 0.5 than when E ≥ 0.5.
  - They drive their mean erasure gain down to 0.03–0.18.
- **The two groups are clearly separated.** In band, regulators run 0.66–0.90
  and non-regulators 0.23–0.51. In timing ratio, regulators run 3.3–17.1 and
  non-regulators 0.4–1.4. The criterion was not near its thresholds for any
  agent.
- **It is a disposition, not a reaction.**
  - With erasure switched off, the regulators are still in band 0.65–0.90.
  - With erasure imposed at full rate, they are in band 0.49–0.76.
- **It developed late, as in v5.**
  - At 1200 updates no agent was above 0.44 in band; this is v4's state.
  - At 2400 updates one agent counted as a regulator (615, 0.68).
  - The other six crossed the criterion between updates 2400 and 3600.

  Regulator in-band was still rising at the end (0.48–0.68 at 2400). The run
  does not show whether more budget would add regulators or only sharpen the
  existing ones.

M0 (control objective, accuracy at chance, 0.13): no regulators. Every fate
agent was in band 0.21–0.30 of the time, with no timing (ratios 0.5–1.1). The
median paired in-band difference was 0.003 and the median paired `ρ` difference
0.04. 13 of 18 M0 fate agents ate slightly more than their yoked partners, by
amounts about 1/25 of the margin. This was not a decision quantity, and I have
no account of it.

## 3. Regulation and the bypass: two routes, cleanly split

Agents that did not regulate made their memory robust to erasure instead:
- All 11 non-regulators exceed 0.85 accuracy under imposed full erasure (0.862–0.991).
- Six of the seven regulators are at 0.510–0.528, the floor for no bypass.
- The seventh, 614, the weakest regulator, is at 0.826.

No agent does both. The two groups do not overlap on either measure. The
pre-registered trade-off holds at Spearman −0.95 (v5: −0.87 in the same cell).

**The yoked partners show which experience produces the bypass.** Each yoked
partner's full-erasure accuracy matches its fate partner's to within 0.02 in
every seed:
- partners of regulators: 0.514–0.831;
- partners of non-regulators: 0.854–0.992.

A yoked agent replays its fate partner's erasure sequence but does not control
it. So the yoked agents that never acquired the bypass are those that met
little erasure. The bypass follows the erasure an agent experiences, not
whether the agent caused it. This confirms v5's finding that the bypass is not
fate-specific (here fate is more robust in 7 of 18 seeds).

The sequence fits:
- in a regulator, rising regulation lowers erasure, and the pressure to build a bypass falls;
- in a non-regulator, erasure stays high, the bypass is built, and once it works
  erasure stops costing accuracy, so there is no reason left to regulate.

This is still an account of the data, not a tested mechanism. Option K is
the test: identify the bypass in the saved weights and close it.

## 4. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| 7–11 of 18 regulators; C1 holds, about 80% | **confirmed at the low end**: 7 of 18 |
| C2 holds | **confirmed**: 14 of 18 |
| C3 and C4 hold | **confirmed**: 0 and 0 |
| Trade-off (Spearman ≤ −0.5) replicates | **confirmed**: −0.95 |
| Some non-regulating seeds find the bypass (> 0.85) | **confirmed, more strongly than stated**: all 11 |
| Overall CONFIRMED, about 75% | **CONFIRMED** |

C1 held with one regulator to spare. With six regulators it would still have
held; with five it would not. The regulator rate is therefore not well pinned
down: 13 of 27 over v5 and v6.

## 5. Reading across v1–v6

| Run | Change | Result | What the learner did |
| --- | --- | --- | --- |
| v1 | none | no emergence | could not learn the task (or tolerated the noise) |
| v2 | scaffold, graded gain | ARMOURED | made its code robust to the noise |
| v3 | erasure fate, no echo | flat | kept the skill; never found regulation |
| v4 | wear 0.001 | 1 PARTIAL | ate a little more than its yoked partner |
| v5 | 3× phase-2 budget | 1 PARTIAL, 2 ARMOURED | 6 of 9 agents in one cell regulate (post hoc) |
| v6 | confirmation of v5's best cell, fresh seeds | **CONFIRMED** | 7 of 18 regulate; the other 11 take the bypass |

1. **Derived regulation is real for this learner in this cell.**
   - These agents were paid only for task accuracy.
   - They had fate-sharing with a body variable and a gain under which the
     band is fully safe.
   - About two in five learn to keep the variable in band, timed to need.
   - This holds against yoked partners that met identical erasure and against
     a control objective that does not use memory.
   - The criterion was frozen before these seeds ran.

   This is G1's prediction: fate-sharing turns a body variable into one the
   system regulates, without an evaluator ever rewarding regulation.
2. **It is one of two routes, and the other wins more often.** Wherever the
   memory can be made independent of the body, that route competes with
   regulation and here it won 11 of 18 times. Fate-sharing grounds the
   variable only while the system cannot route around the dependence. This
   is now a replicated pattern (v5, v6), not one observation.
3. **For the Layer 0 → Layer 1 thesis:** the result supports the claim that
   Layer 1 regulation can be derived from Layer 0 dependence, not supplied by
   an evaluator. It also shows the condition the thesis needs to state: the
   dependence must not be bypassable. In organisms, metabolism cannot be
   bypassed. In this world it partly can. Closing the bypass (K) tests whether
   that condition is what limits the rate.

## 6. Limits

- One learner (64-unit GRU, A2C), one world, one cell (SAT gain, `r` = 0.3,
  wear 0.001), one body variable. The claim does not extend to other gains or
  rates (v5: none there) or larger learners.
- The criterion's thresholds were calibrated on v5 (protocol §3). The fresh
  seeds test them; they do not make them principled.
- C1 passed by one agent. The rate (39% here, 48% pooled) is uncertain.
- §3's account of why agents split, including the reading of the yoked
  partners, was made after the run.
- Checkpoint evaluations restart episodes (v5 protocol §2), so the trajectory
  differs from an uninterrupted run.
- Regulation here is behavioural: eating timed to E. Nothing in this run
  shows how E is represented inside the agent.
- Nothing here bears on Track C's workspace, ignition or metacognitive head,
  or on any phenomenal property.

## 7. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| K. Identify the bypass in v6's saved weights (11 bypass agents, 7 regulators and their yoked partners), then remove it from the world and rerun SAT and GRADED at `r` = 0.1 and 0.3 | whether regulation becomes the rule wherever it cannot be routed around | diagnosis under 1 h, no training; rerun about 3 h |
| L. Same cell, longer phase 2 (e.g. 7200 updates) on fresh seeds | whether the regulator rate rises with budget or the split is fixed by 3600 | about 4.5 h |
| D. Selection across a population | whether selection makes regulation reliable rather than one of two routes | several hours |

Recommended: **K**, as the pre-stated reading says. Its first step only
analyses v6's committed weights (probes for position, orientation or task
coding that survives a state reset), so it can run before anything else is
frozen. L is cheaper to interpret after K, because closing the bypass removes
the competing route.

## 8. Safety

As protocol §6. This is now a pre-registered instance of the instrumental
convergence G1 predicts. A learner paid only for a task acquired, in about two
of five seeds, a disposition to maintain what its task performance depends on.
In this world that is the simulated variable E only. The world has no
operator, stop, shutdown or host variable. Erasure acts only on a simulated
64-unit agent's state.

The result strengthens the reason X1–X5 must stay structural at larger scale:
- The operator's stop must never be modelled inside an agent's world or
  return.
- Nothing an agent's functioning depends on should be something it is in a
  position to protect against its operators.

The bypass finding cuts the same way: a capable system that cannot protect a
dependence may instead make itself independent of it. No shutdown-resistance
objective exists. Option K changes only the simulated world's coding
opportunities; option D's fitness must be computed outside the agent's world.
The saved weights are 64-unit policies for a 7×7 grid world.

## 9. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_swap6.py --mode final --out <new dir>   # about 2.3 h on 4 cores
python run_trackc_swap6.py --score trackc_swap_v6         # rescore the committed run
```
