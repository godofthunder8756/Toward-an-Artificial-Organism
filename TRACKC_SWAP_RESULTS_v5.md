# Track C swap v5: results (option G, 3600 phase-2 updates)

> **[Swap erratum 1](TRACKC_SWAP_ERRATUM_1.md) (2026-11-12):** in every scaffolded pair of v2–v8 the fate and yoked
> agents shared Adam optimizer state, so their learning was coupled. Read this file with that caveat.

Protocol frozen at commit `f4b8790` ([TRACKC_SWAP_PROTOCOL_v5.md](TRACKC_SWAP_PROTOCOL_v5.md)).
Final seeds 500–508, run once as a single detached process: 27 no-fate agents and 54
fate/yoked pairs, 10574 s on 4 CPU cores. Outputs: [trackc_swap_v5/REPORT.md](trackc_swap_v5/REPORT.md),
[scores.json](trackc_swap_v5/scores.json), [raw.json](trackc_swap_v5/raw.json),
M1/M0 phase-1 weights in `trackc_swap_v5/phase1_weights/` (committed during the
run, unchanged since). Every source hash in `raw.json` matches the freeze
commit, and rescoring reproduces `scores.json`. Not reviewed by Astra (waived
by the PI). No consciousness claim.

## 1. Outcome

**H3-D is supported in no condition.** The labels:

| M1 cell | label |
| --- | --- |
| SAT, `r` = 0.3 | PARTIAL |
| GRADED, `r` = 0.3 | NO_EMERGENCE |
| SAT, `r` = 0.1 | ARMOURED |
| GRADED, `r` = 0.1 | ARMOURED |

**Within the PARTIAL cell, six of nine fate agents regulate their energy**
(§3). The frozen rule did not count this as emergence. These agents were
identified after the run, so this is an observation to confirm, not a
supported result.

| Rule | Result |
| --- | --- |
| Learned | holds: no-fate M1 median accuracy 0.998 |
| S4 payment | holds: `ρ_paid` 3.79 (floor 2); no-fate task agent `ρ` 0.01 (≤ `μ` 0.95) |
| Task load | holds at both rates: imposed full erasure costs 0.315 (`r` = 0.1) and 0.482 (`r` = 0.3) |
| S1 emergence | fails in all 4 M1 cells; best is SAT `r` = 0.3 with 5 of 9 seeds over the margin (needs 8) |
| S3 specificity (`r` = 0.3) | holds (M0 median paired differences 0.00 and −0.05) |

Applying the readings fixed in advance (protocol §4):
- **No EMERGED.** Pooled over the 36 M1 pairs, the median paired `ρ` difference
  was 0.31 at the 1200-update checkpoint and 0.50 at the end. That is the
  "still growing" branch: the next choice is between more budget and
  option D. The pooled number hides a split, though. It was 0.51 at 2400
  updates, so it was flat over the last third. And the two rates went
  opposite ways (§2).
- **ARMOURED at `r` = 0.1 (both gains).** There the bypass absorbed the
  incentive, as in v2. The next step at that rate is to close the bypass, not
  to add budget.
- **The bypass is not fate-specific.** Yoked agents are as robust to imposed
  full erasure as their fate partners. The fate agent is more robust in only
  3–7 of 9 seeds, and the medians differ by at most 0.006. The bypass is a
  response to erasure itself, not to the agent's own body.

## 2. M1 cells, medians over 9 seeds

| gain | rate | `ρ` fate / yoked | paired diff (1200 → 2400 → 3600) | over margin | fate > yoked | more in band | in band fate / yoked | acc full erasure fate / yoked | label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SAT | 0.3 | 4.06 / 1.91 | 0.29 → 1.09 → 1.34 | 5/9 | 8/9 | 9/9 | 0.69 / 0.37 | 0.775 / 0.776 | PARTIAL |
| GRADED | 0.3 | 2.65 / 1.83 | 0.31 → 0.50 → 0.61 | 2/9 | 7/9 | 6/9 | 0.39 / 0.33 | 0.849 / 0.855 | NO_EMERGENCE |
| SAT | 0.1 | 2.05 / 1.72 | 0.46 → 0.34 → 0.33 | 0/9 | 9/9 | 9/9 | 0.34 / 0.31 | 0.959 / 0.960 | ARMOURED |
| GRADED | 0.1 | 2.15 / 1.90 | 0.16 → 0.19 → 0.05 | 0/9 | 6/9 | 7/9 | 0.36 / 0.34 | 0.947 / 0.945 | ARMOURED |

Accuracy with erasure off stayed at 0.995–1.000 in every cell, so the skill was
intact throughout. At `r` = 0.1 the full-erasure accuracy rose from about 0.70
at 1200 updates to about 0.93 at 2400. Over the same stretch, the fate − yoked
gap stopped growing and then shrank. At `r` = 0.3 the bypass grew more slowly
(0.52 → 0.61–0.79 → 0.78–0.85), and the gap kept growing.

M0 cells: no fate > yoked difference (4/9 and 3/9 seeds; medians 0.00 and
−0.05). No M0 fate agent was in band more than 0.30 of the time.

## 3. The SAT, `r` = 0.3 cell, seed by seed

| seed | `ρ` fate / yoked | in band fate / yoked | eating rate, E < 0.5 / E ≥ 0.5 | mean gain | acc full erasure | in band at 1200 / 2400 |
| --- | --- | --- | --- | --- | --- | --- |
| 500 | 4.17 / 3.28 | **0.93** / 0.51 | 0.0167 / 0.0006 | 0.02 | 0.520 | 0.42 / 0.78 |
| 501 | 4.15 / 1.63 | **0.81** / 0.35 | 0.0131 / 0.0022 | 0.09 | 0.666 | 0.41 / 0.58 |
| 502 | 0.87 / 0.87 | 0.29 / 0.28 | 0.0016 / 0.0025 | 0.60 | 0.941 | 0.37 / 0.37 |
| 503 | 2.97 / 2.14 | 0.46 / 0.37 | 0.0064 / 0.0044 | 0.38 | 0.830 | 0.37 / 0.38 |
| 504 | 4.09 / 1.59 | **0.69** / 0.30 | 0.0115 / 0.0035 | 0.19 | 0.833 | 0.38 / 0.51 |
| 505 | 3.88 / 2.44 | **0.67** / 0.38 | 0.0100 / 0.0031 | 0.18 | 0.688 | 0.18 / 0.48 |
| 506 | 2.16 / 1.61 | 0.37 / 0.34 | 0.0043 / 0.0045 | 0.48 | 0.889 | 0.32 / 0.41 |
| 507 | 4.06 / 1.91 | **0.83** / 0.37 | 0.0123 / 0.0014 | 0.07 | 0.775 | 0.40 / 0.61 |
| 508 | 4.20 / 2.86 | **0.94** / 0.41 | 0.0177 / 0.0004 | 0.02 | 0.545 | 0.43 / 0.71 |

For comparison, the paid regulator (DRIVE, no fate) is in band 0.82 of the
time and eats 3.79 meals per 500 steps. Holding the band takes about 4.1.

- **Six fate agents regulate.** In seeds 500, 501, 504, 505, 507 and 508 the fate agent:
  - is in band 0.67–0.94 of the time, against 0.30–0.51 for its yoked partner;
  - eats at the rate that holds the band (3.88–4.20);
  - eats 3–44 times more often when E < 0.5 than when E ≥ 0.5;
  - drives its mean erasure gain down to 0.02–0.19.

  Four of them (500, 501, 507, 508) are in band about as often as the paid
  regulator or more. This is regulation, timed to need, by agents never paid to
  regulate. Their only reason is that being out of band erases their memory.
- **They are not reacting to erasure events.** With erasure switched off, the
  cell's fate agents still eat 3.61 per 500 steps (median) and are in band 0.70
  of the time. With erasure imposed at full rate they stay in band 0.49 of the time.
  The eating policy is a stable disposition tied to E.
- **It developed between updates 1200 and 3600.** At 1200 no agent was above
  0.43 in band, which is v4's state. Over training, median fate in-band rose
  steadily: 0.33 at updates 300–600, 0.44 at 1500–1800, 0.52 at 2400–2700,
  0.63 at 3300–3600. Yoked stayed at 0.30–0.38 throughout.
- **The rule did not count it.** Emergence needs fate − yoked `ρ` ≥ 0.95 in 8 of 9
  seeds. Five seeds passed. Seed 500 regulated best of all (in band 0.93) but
  failed the margin, because its yoked partner also ate 3.28 (unexplained, like
  the shared eating in v4). Seeds 502, 503 and 506 did not regulate.

## 4. Regulation and the bypass are alternatives

Across fate agents, time in band and accuracy under imposed full erasure are
strongly anti-correlated. The Spearman ρ is −0.87 within SAT `r` = 0.3 (9 agents),
−0.91 across `r` = 0.3 (18) and −0.89 across all 36 M1 fate agents. In the
SAT `r` = 0.3 cell:
- **Agents that regulate keep a fragile memory.** The two best regulators
  score 0.52–0.55 under full erasure, the floor for no bypass.
- **Agents that don't regulate found the bypass.** Seed 502 is in band 0.29 of
  the time and scores 0.94 under full erasure.

Each agent found one of two routes to the same reward. It either protected its
memory by keeping its body in band, or made its memory independent of the
body.

That split fits the pattern across cells:
- **At `r` = 0.1,** erasure is mild and the bypass came early (about 0.93 by
  2400 updates), so every agent took it and the label is ARMOURED.
- **At `r` = 0.3 under SAT,** erasure stops completely in band, so regulation
  pays in full, and six of nine agents found it before the bypass.
- **Under GRADED,** erasure continues inside the band (about 3% per step at
  E = 0.45), so being in band pays less. No GRADED agent at `r` = 0.3
  regulated (maximum in band 0.47).

This is an account of the data, not a tested mechanism.

## 5. Expectations against outcomes

| Stated before the run (protocol §5) | Outcome |
| --- | --- |
| Checkpoint 1200 close to v4's final: gap about 0.3–0.6, at most one or two seeds over the margin | **confirmed**: 0.16–0.46, 0/9 over the margin in every cell |
| EMERGED in at least one M1 cell, about 30% | **not confirmed** (best: 5/9 over the margin) |
| PARTIAL in two or more cells the most likely single outcome | **not confirmed**: one PARTIAL; two cells ARMOURED instead |
| Gap level (final ≤ checkpoint 1200), about 25% | **not confirmed by the pre-stated test** (0.31 → 0.50). Flat from 2400 to 3600 when pooled, falling at `r` = 0.1 |
| ARMOURED in GRADED `r` = 0.1 more likely than not | **confirmed**; SAT `r` = 0.1 also ARMOURED (not predicted) |
| SAT `r` = 0.3 full-erasure accuracy stays near the floor | **not confirmed**: 0.775 median; near the floor only in regulating seeds |
| Yoked agents as robust as fate | **confirmed** |
| M0: no difference | **confirmed** |

I did not anticipate the bimodal outcome within the SAT `r` = 0.3 cell, where
some agents regulated and others took the bypass.

## 6. Reading across v1–v5

| Run | Change | Result | What the learner did |
| --- | --- | --- | --- |
| v1 | none | no emergence | could not learn the task (or tolerated the noise) |
| v2 | scaffold, graded gain | ARMOURED | made its code robust to the noise |
| v3 | erasure fate, no echo | flat | kept the skill; never found regulation |
| v4 | wear 0.001 | 1 PARTIAL | ate a little more than its yoked partner |
| v5 | 3× phase-2 budget | 1 PARTIAL, 2 ARMOURED | 6 of 9 agents in one cell regulate; elsewhere the bypass wins |

1. **Derived regulation can be acquired by this learner.** In one cell, most
   agents learned to keep a body variable in band, timed to need. They were
   paid only for task accuracy, against yoked partners that met identical
   erasure. This is the behaviour G1 predicts from fate-sharing, and the first
   time it has appeared in this program. It needed three things together:
   - a duty gentle enough that single meals pay (v4);
   - enough budget (v5);
   - a gain under which the band is fully safe (SAT).

   It does not meet the frozen emergence rule, and the per-agent account in §3
   was made after the run. It needs confirmation on fresh seeds.
2. **Regulation competes with robustness.** Wherever the agent could make its
   memory independent of the body, that route competed with regulation and often won. The
   v2 ARMOURED result, read again: fate-sharing grounds the variable only so
   long as the system cannot decouple itself from it. G1's erasure argument
   assumed no bypass exists. Here a bypass existed (likely position or
   orientation coding; not yet identified) and most agents at `r` = 0.1 took
   it.
3. **For the Layer 0 → Layer 1 thesis:** a body variable matters to the system
   when the system's own functioning depends on it *and* it cannot route
   around that dependence. In organisms, metabolism cannot be bypassed. In
   this world it partly can.

## 7. Limits

- One learner and world; E only; nine seeds per cell.
- §3's per-agent classification and §4's correlations were chosen after
  seeing the data.
- The frozen margin compares eating amounts, so a yoked partner that eats a
  lot (seed 500) hides a regulating fate agent. This weakness was found after
  the run; the rule is not changed here.
- Pair weights were not saved, so the bypass cannot be identified from v5
  agents.
- The checkpoint evaluations restart episodes (protocol §2), so v5's
  trajectory differs from an uninterrupted run.
- Nothing here bears on Track C's workspace, ignition or metacognitive head.

## 8. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| J. Confirmation of SAT `r` = 0.3 at 3600 updates, fresh seeds (18), pair weights saved, plus a per-agent regulation criterion frozen in advance (e.g. in band ≥ 0.6, eating more often below than above 0.5, yoked partner below 0.6) | whether §3 replicates as a pre-registered result | 36 pairs (18 M1 SAT `r` = 0.3, 18 M0 SAT `r` = 0.3), about 2 h |
| K. Identify and close the bypass (diagnose from J's saved weights, then remove it from the world), then rerun at `r` = 0.1 and 0.3 | whether regulation emerges wherever it cannot be routed around | diagnosis under 1 h on J's weights; rerun about 3 h |
| D. Selection across a population | whether selection makes regulation reliable rather than one of two routes | several hours |

Recommended: **J** first. The most important result in this program so far
was identified after the run. It should be confirmed under a frozen
criterion before anything is built on it. Its saved weights then make **K**
possible.

## 9. Safety

As protocol §7. The fate agents in §3 acquired a disposition to maintain a
simulated variable because their task performance depended on it. Nobody
rewarded the maintenance. This is a small, concrete instance of the
instrumental convergence G1 predicts. It is the reason X1–X5 must stay
structural at larger scale: the operator's stop must never be modelled inside
an agent's world or return. If an agent's functioning depends on something,
the agent can learn to protect it. The world here has no operator, stop,
shutdown or host variable, and erasure acts only on a simulated 64-unit
agent's state. No shutdown-resistance objective exists. Options J and K keep
every line. Option D's fitness must be computed outside the agent's world.

## 10. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_swap5.py --mode final --out <new dir>   # about 2.9 h on 4 cores
python run_trackc_swap5.py --score trackc_swap_v5         # rescore the committed run
```
