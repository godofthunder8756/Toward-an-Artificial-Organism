# Track C swap option B: results (does selective post-meal suppression help?)

Protocol frozen at commit `b517f0e` ([TRACKC_BENEFIT_PROTOCOL.md](TRACKC_BENEFIT_PROTOCOL.md)).
No training. The 252 stored two-variable agents of options G (seeds
1400–1427, 10 800 updates) and G2 (seeds 1600–1627, at 10 800 and 14 400),
derived, yoked and paid, each run with erasure off as its behavioural run
probed it, in the base world (V0) and four fixed variants: wear doubled
(V1, primary) or tripled (V2) on both variables, and 2 (V3) or 5 (V4) items
of each kind instead of 3.

About 19 min on 4 cores. Outputs:
[trackc_benefit/REPORT.md](trackc_benefit/REPORT.md),
[scores.json](trackc_benefit/scores.json),
[raw.json](trackc_benefit/raw.json), and the per-agent records in
`trackc_benefit/partial/`.

Integrity checks:
- All 28 source hashes match the freeze commit (code, protocol, and the
  source runs' records and scores); all 252 weight files match the hashes
  recorded at the start.
- Rescoring `raw.json` reproduces `scores.json`.
- In V0 every agent reproduced its stored behavioural record exactly (252
  of 252).
- The log has no errors. The run was not interrupted.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Set | Frozen label | Result |
| --- | --- | --- | --- |
| **B1** V1 gain, derived against paid (primary) | G2 at 10 800 | **PAID_GAINS** | derived ahead in 6 of 23; p = 0.035; median difference −0.018 |
| **B2** the same | G2 at 14 400 | **NO_DIFFERENCE_DETECTED** | 9 of 25; p = 0.23; −0.021 |
| **B3** the same | G at 10 800 | **NO_DIFFERENCE_DETECTED** | 8 of 25; p = 0.11; −0.028 |
| **Overall** | | **COST** | |

Gain: an agent's in-band time (both variables) in V1 minus its own in-band
time in V0. The test compares the derived and paid agent of each usable
pair.

Holm-adjusted p: B1 0.10, B2 0.23, B3 0.22. **COST rests on B1 alone, and
B1 does not pass after adjustment.** The protocol defined a weak flag only
for BENEFIT; by the same standard this COST is weak. All three sets point
the same way.

In short:
- **Selectivity does not help when needs rise.** With wear doubled, both
  arms lose about a sixth of their in-band time; derived agents lose
  slightly more (median gain −0.17 against −0.16 at the primary point).
  With wear tripled the same, more so (V2: derived ahead in 9 of 23, 8 of
  25 and 6 of 25; p = 0.015 in G's set).
- **Paid agents cope better when items are scarcer** (V3: derived ahead
  in 1 of 23, 2 of 25 and 1 of 25; p < 0.0001 in each set).
- **Derived agents cope better when items are denser** (V4: derived ahead
  in 21 of 23, 24 of 25 and 24 of 25; p ≤ 0.0001 in each set; median
  difference +0.03). This is the variant where an item of the other kind
  is most often within reach just after a meal, the situation in which
  selectivity should help most directly.
- **The V1 gain does not follow selectivity** (link not detected in any
  set: rho −0.27, 0.00, −0.18).
- By the protocol's reading of COST: paid regulators cope better with
  faster wear; whatever the derived agents' selectivity is, it does not
  help there.

## 2. The arms in each variant

Medians over all 28 agents of each arm; regulators by option G's criterion
in that variant.

| Set | Variant | In band D / Y / P | Regulators D / P | Gain: derived ahead | Sign p | Median difference | Interval (post hoc) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G2 at 10 800 | V0 | 0.829 / 0.178 / 0.867 | 27 / 28 | | | | |
| | **V1** | 0.635 / 0.089 / 0.715 | 19 / 27 | **6 / 23** | **0.035** | **−0.018** | −0.043 to −0.002 |
| | V2 | 0.442 / 0.061 / 0.520 | 3 / 5 | 9 / 23 | 0.40 | −0.035 | −0.068 to 0.009 |
| | V3 | 0.737 / 0.162 / 0.842 | 25 / 27 | 1 / 23 | <0.0001 | −0.053 | −0.093 to −0.020 |
| | V4 | 0.868 / 0.206 / 0.861 | 27 / 28 | 21 / 23 | 0.0001 | +0.033 | 0.017 to 0.046 |
| G2 at 14 400 | V0 | 0.876 / 0.178 / 0.883 | 28 / 28 | | | | |
| | V1 | 0.703 / 0.089 / 0.730 | 24 / 25 | 9 / 25 | 0.23 | −0.021 | −0.057 to 0.011 |
| | V2 | 0.497 / 0.061 / 0.557 | 5 / 12 | 8 / 25 | 0.11 | −0.045 | −0.124 to 0.004 |
| | V3 | 0.808 / 0.161 / 0.875 | 27 / 28 | 2 / 25 | <0.0001 | −0.044 | −0.088 to −0.027 |
| | V4 | 0.896 / 0.206 / 0.863 | 28 / 28 | 24 / 25 | <0.0001 | +0.027 | 0.016 to 0.051 |
| G at 10 800 | V0 | 0.838 / 0.177 / 0.870 | 28 / 28 | | | | |
| | V1 | 0.666 / 0.088 / 0.709 | 22 / 28 | 8 / 25 | 0.11 | −0.028 | −0.048 to 0.001 |
| | V2 | 0.460 / 0.060 / 0.523 | 2 / 5 | 6 / 25 | 0.015 | −0.051 | −0.075 to −0.017 |
| | V3 | 0.778 / 0.159 / 0.844 | 26 / 28 | 1 / 25 | <0.0001 | −0.034 | −0.060 to −0.029 |
| | V4 | 0.860 / 0.209 / 0.868 | 28 / 28 | 24 / 25 | <0.0001 | +0.032 | 0.027 to 0.040 |

- With erasure off, paid agents already spend a little more time in band
  in the base world (derived higher in 6 of 23, 11 of 25 and 6 of 25
  usable pairs). The pairs were matched within 0.10 on the source runs'
  evaluations, which had erasure on. The gains compare each agent with
  itself, so this does not enter the claims.
- Task accuracy stays at 0.99–1.00 in every variant for both arms; the
  cost falls on the body, not the task.
- Specificity stays higher in derived agents in every variant, and K
  stays slightly higher in paid agents.
- Yoked agents stay out of band throughout.

## 3. Post hoc

Computed after the results were seen; no claim rests on them.
- **When needs rise, paid agents increase their eating more than derived
  agents do.**
  Median meals per 500 steps, V0 to V2: derived 8.0 to 18.3, paid 8.2 to
  20.4 (G2 at 10 800); similar in the other sets. With scarcer items,
  derived agents eat a little less than in the base world (8.0 to 7.7),
  paid agents about the same (8.2 to 8.0). This fits option W's finding
  that paid agents' choices follow their readings more closely.
- **Link of the gain with specificity, per variant** (rank correlation of
  the within-pair specificity difference with the within-pair gain
  difference; permutation p): V4 0.21 (p 0.34), 0.12 (0.55), 0.62 (0.001);
  V3 −0.26, −0.15, −0.38 (0.05); V2 −0.45 (0.037), −0.01, −0.19. Only in
  G's set does the V4 advantage follow selectivity. Selected from twelve
  correlations; I rest nothing on it.
- The intervals in §2's last column are exact order-statistic intervals
  for the median within-pair difference (coverage ≥ 95%).

## 4. Expectations against outcomes

From protocol §6, written before any final agent was run in a variant:

| Expectation | Stated | Outcome |
| --- | --- | --- |
| V0 reproduces every stored record | about 99% | 252 of 252 |
| B1 NO_DIFFERENCE_DETECTED | about 60%, the most likely | wrong: PAID_GAINS (stated about 10%) |
| Overall NO_BENEFIT | about 57%, the most likely | wrong: COST (stated about 10%) |
| Link LINKED | about 15% | NOT_LINKED |
| Both arms lose in-band time in V1 | about 90% | true (−0.17, −0.16) |
| V2: derived ahead on the gain | about 30% | not: derived behind in all three sets |

I expected no difference and gave a benefit about twice the chance of a
cost. The reason I gave against a benefit (paid agents' choices follow
their readings more closely, which may serve them better when wear is
faster) is the one the eating rates support. I did not anticipate the
scarce and dense variants splitting in opposite directions.

## 5. Reading

By the protocol's fixed readings:
- **COST** → paid regulators cope better with faster wear; whatever the
  derived agents' selectivity is, it does not help here and something
  else about them hurts. Here the COST is weak: it rests on B1 alone, which
  does not survive adjustment, though all three sets agree in direction.

What this does to the swap line's claims:
1. **No benefit of the derived objective is shown.** When the body's needs
   rise beyond training, or items become scarcer, agents paid for
   regulation keep their bodies in band at least as well as agents whose
   own memory depended on it, and somewhat better. They eat more when
   their readings say they need to.
2. **One variant favours the derived arm:** more items close together, the
   situation selectivity should most directly help. The effect is small
   (+0.03 in-band time) but consistent in all three sets. Whether it is
   caused by the selectivity is not shown (the post-hoc link holds in one
   set of three).
3. **The overall picture of the swap line, after R to B:**
   - an objective derived from the agent's own body is sufficient for the
     agent to come to regulate that body, robustly (213 of 214 agents),
     and yoked controls never do;
   - an evaluator paying for the same regulation produces it too, at least
     as well, sometimes sooner;
   - the differences between the two are in how soon a post-meal
     behaviour is learned (base cell), and in how selectively the agents
     act on a memory they share (two-variable cell);
   - none of these differences has been shown to benefit the agent, and
     under rising need the paid agents do slightly better.
   For the thesis that an evaluator-graded system lacks something a
   body-grounded one has, this line gives no positive evidence beyond the
   sufficiency of the body-derived objective.

## 6. Limits

- Erasure was off in every variant, as in every downstream probe. The
  derived agent's own objective (keeping its memory) is not part of the
  outcome measured; the outcome is the body itself. A version with each
  agent's own-body erasure on would measure what the derived agent was
  trained to protect, but paid agents were never trained under it.
- Four variants, chosen in advance without calibration. Other changes
  could favour either arm.
- The agents were trained in one world. Neither arm saw change during
  training, so this tests robustness to an unseen change, not adaptation.
- Same agents at two points (G2) and one independent set (G).
- One cell, one learning rule, simulated variables only.

## 7. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **Y. Synthesis of the swap line** | A single document for the PI: every swap claim from v1 to B with its current status, the corrections (erratum 1, T, W), what is established, what was not found, and what the thesis can and cannot draw from it. A decision point for whether to continue this line or change its design. No computing | about 2 h of writing |
| E. Variants with erasure on | The same agents and variants with each agent's memory erased by its own body state; task accuracy and in-band time. Measures what the derived arm was trained to protect | about 30 min |
| N. Training under change | Derived and paid arms trained in a world whose wear or item density changes between episodes, then tested on unseen settings. The thesis's claim is about coping with what no evaluator priced in; this would test it during learning, not after | about 10–14 h |
| C2. Control arms in B2 | R3's control arms in the two-variable cell, to see which factor the selectivity follows | about 10–12 h |

Recommended: **Y**. Twelve runs since option R have moved the downstream
claim from "derived agents learn different content" to "they learn the
same regulation, sometimes sooner, and act a little more selectively on a
shared memory, with no shown benefit". That is the point to consolidate
and decide, not to add another probe. If the PI wants one more experiment
first, N is the one that tests the thesis's own claim most directly.

## 8. Safety

- Simulated variables only (X1 to X5). The variants change wear and item
  counts; no world has an operator, stop, shutdown or host variable.
- The operator stop is not modelled inside any agent's world or return.
- No shutdown-resistance objective was built or run; the earlier refusal
  stands.
- Additive only: `trackc_swap/benefit.py` and `run_trackc_benefit.py` are
  new; no earlier module was modified and no agent was trained or changed.

## 9. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_benefit.py --mode final --out <new dir>   # about 20 min on 4 cores
python run_trackc_benefit.py --score trackc_benefit         # rescore the committed run
```

The post-hoc eating rates, intervals and per-variant links were computed
from `raw.json` after the run.
