# Track C swap option R2: results (replication of derived against paid, relocation control)

Protocol frozen at commit `7919aea` ([TRACKC_PAID2_PROTOCOL.md](TRACKC_PAID2_PROTOCOL.md)).
Seeds 1000–1027, SAT gain, `r` = 0.3, v7/v8 world, four arms: 3.0 h on 4
cores. Outputs: [trackc_paid2/REPORT.md](trackc_paid2/REPORT.md),
[scores.json](trackc_paid2/scores.json), [raw.json](trackc_paid2/raw.json),
and the weights of all four arms per seed.

Integrity checks:
- All 17 source hashes match the freeze commit.
- Rescoring `raw.json` reproduces `scores.json`.
- The log has no errors. No-fate task accuracy is 0.999, so the run is valid.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Frozen label | Result | Needed |
| --- | --- | --- | --- |
| **C0** derived regulation, independent optimizers | **HOLDS** | 28 of 28 derived agents regulate; 0 of 28 yoked | 19; at most 1 |
| Usable derived/paid pairs | — | 23 of 28 | 14 |
| **C1 (primary)** anticipation in the state, derived against paid | **NOT_REPLICATED** | derived higher in 12 of 17; p = 0.14; 0.56 against 0.49 | 13 of 17 |
| **C2** flat eat readiness | **DERIVED_MORE_FLAT** | 11 of 27 derived agents, 1 of 27 paid; p = 0.002 | p ≤ 0.05 |
| **C3** combined post-meal suppression K | **DERIVED_AHEAD** | derived higher in 21 of 23; p = 0.0001; 0.89 against 0.65 | 17 of 23 |
| **C4** relocation control | **RELOCATION_NOT_SUFFICIENT** | PAIDR above paid in 12 of 21 (p = 0.66); derived above PAIDR in 20 of 22 (p = 0.0001) | — |

Holm-adjusted p over C1–C3: C1 0.14, C2 0.004, C3 0.0002. C2 and C3 pass
after adjustment, so neither is weak by the protocol's rule.

In short:
- **Derived regulation is confirmed a second time** with independent
  optimizers: every derived agent regulates and no yoked agent does.
- **Option R's one positive result (R1) did not replicate.** The difference
  has the same direction and is smaller, and it misses the bar by one pair.
- **Option R's post-hoc observation did replicate, as two pre-stated
  claims.** Derived agents hold back from getting a second meal after a meal
  they have not yet sensed, more than paid agents matched for regulation.
  About four in ten derived agents do it through where they go.
- **Tying a paid agent's position to its own body state does not produce
  that behaviour.** So it does not come from the way this world implements
  erasure by relocation.

## 2. C0 and the arms

Medians over 28 seeds, at the end of training:

| Arm | In band | Regulators | Eat-timing ratio | Task accuracy | Updates to sustained regulation |
| --- | --- | --- | --- | --- | --- |
| DERIVED (own fate) | 0.916 | 28 | 52 | 0.983 | 1320 |
| YOKED (replayed fate) | 0.315 | 0 | 1.0 | 0.981 | never |
| PAID (replayed fate, payment) | 0.920 | 27 | 30 | 0.983 | 1545 |
| PAIDR (replayed erasure, own relocation, payment) | 0.911 | 27 | 30 | 0.983 | 1565 |

- One paid agent (seed 1019, 0.47 in band) and one PAIDR agent (seed 1021,
  0.52) did not regulate.
- Usable pairs: derived/paid 23, PAIDR/paid 21, derived/PAIDR 22. Five
  derived/paid pairs were dropped: four for in-band times more than 0.10
  apart and one for the paid non-regulator.
- With interoception shuffled, no agent of any arm regulates (0 of 28 each).
  With erasure off, 28 derived, 27 paid and 26 PAIDR agents regulate.
- The new arm trained as calibration predicted. Relocation counts are the
  same in all arms (about 1.31 million per run).

## 3. C1: the anticipation index did not replicate

- **Derived higher in 12 of 17 pairs, p = 0.14.** Medians 0.557 against
  0.490; median difference 0.09 (R: 0.18). Wilcoxon p = 0.26.
- **Six of the 23 usable pairs had no defined index.** The decoder failed
  (held-out R² below −0.10) for the derived agent in three, the paid agent
  in two, and both in one. The rule that excludes them was pre-stated.
- With 17 pairs the bar was 13. The protocol's examples assumed about 24.
- Counting a decoder failure as a loss for the agent that failed gives 14 of
  22 (p = 0.29; post hoc). Over all seeds where both regulate, 15 of 21
  (p = 0.08; pre-stated as secondary).

By the reading fixed in advance, **R's R1 was not robust, and the thesis
keeps no support from the state measure.**

Descriptive only, as pre-stated: pooling R and R2 under R2's exclusion rule
gives 24 of 32 (p = 0.007). R was the run in which the difference was first
seen, so the pooled count is not a test.

## 4. C2 and C3: what the agent does after a meal

Both claims were formed on R's data and frozen before this run.

**K** measures how far the readiness to get a meal falls in the four steps
after a meal, before the reading can show it. It combines the eat action (S)
and moves toward food (M): K = 1 − (1 − S)(1 − M).

| | Derived | Paid | PAIDR | Yoked |
| --- | --- | --- | --- | --- |
| K, median over all seeds | 0.905 | 0.640 | 0.657 | −0.008 |
| K, range among regulators | 0.54 to 0.99 | 0.09 to 0.90 | 0.08 to 0.91 | — |
| Regulators with K below 0.5 | 0 of 28 | 9 of 27 | 8 of 27 | — |
| Flat eat readiness | 11 | 1 | 1 | 0 |

- **C3: derived above paid in 21 of 23 pairs** (0.894 against 0.650).
- **C2: 11 of 27 derived agents have flat eat readiness, against 1 of 27
  paid.** A flat agent is ready to eat at any reading below 0.5 when food is
  under it. It regulates through when it steps onto food.
- **Every derived regulator acts on the unsensed meal.** A third of paid
  regulators hardly do, at the same in-band time.

Derived agents come in two kinds (post hoc, as in R):
- **Flat (8 usable pairs):** S near 0 and M of 0.76 to 0.97. After a meal
  they almost stop moving toward food. K exceeds the paid partner's in 8 of
  8.
- **Not flat (15 usable pairs):** they suppress the eat action. Their S
  exceeds the paid partner's in 12 of 15 (0.82 against 0.62; p = 0.035), and
  K in 13 of 15 (p = 0.007).

Neither component separates the arms alone (S: 14 of 23; M: 15 of 23). That
is expected when the derived agents split between the two routes.

Robustness to the formula (post hoc): the larger of S and M is higher for
the derived agent in 20 of 23 pairs, and their mean in 21 of 23.

## 5. C4: the relocation control

PAIDR is a paid agent whose relocations follow its own body state, as a
derived agent's do. Its memory erasures are still replayed.

| Comparison on K | First higher | p | Medians |
| --- | --- | --- | --- |
| PAIDR against paid | 12 of 21 | 0.66 | 0.634 against 0.637 |
| Derived against PAIDR | 20 of 22 | 0.0001 | 0.890 against 0.622 |

- Flat eat readiness: 1 of 26 PAIDR agents, the same as paid. Derived
  against PAIDR: 10 of 26 against 1 of 26 (p = 0.005).
- **A paid agent with its own relocation behaves like a paid agent.**

By the reading fixed in advance: tying position to the body state does not
produce the difference. Either the dependence of memory on the body state is
needed, or the payment prevents it. **R2 cannot tell these apart.**

## 6. Secondary and post hoc

Pre-stated as secondary, labels descriptive:
- **R²(h → E): no difference** (derived higher in 14 of 23). R's post-hoc
  finding that derived states carry E better did not recur.
- **PAIDR agents have a lower anticipation index than paid agents** (higher
  in 4 of 19, p = 0.019; 0.38 against 0.51), and lower than derived agents
  (derived higher in 14 of 18, p = 0.031). I did not predict this and have
  no explanation.
- **Derived agents learn to regulate sooner:** earlier than paid in 20 of 28
  seeds (p = 0.036), and earlier than PAIDR in 22 of 28 (p = 0.004). R had
  14 of 18.
- Pooled K over R's and R2's usable pairs: 36 of 39. R's K values were the
  development data, so this is not a test.

Post hoc:
- **The anticipation difference sits in the flat agents.** Flat derived
  agents: ahead of their paid partner in 5 of 6 (0.68 against 0.50). Others:
  7 of 11 (0.49 against 0.49). The counts are small.
- **Decoder failures are more common in derived agents** (5 of 28; paid 3,
  PAIDR 0, yoked 0). All five are of the not-flat kind. I did not
  investigate the cause.
- The eat-timing ratio's medians differ (52 against 30), but derived is
  higher in only 17 of 28 seeds (p = 0.34).

## 7. Expectations against outcomes

| Expectation (protocol §6) | Outcome |
| --- | --- |
| C0 holds, about 95% | Holds, 28 of 28 |
| At least 14 usable pairs, about 95% | 23 |
| C1: NOT_REPLICATED about 50%, REPLICATED about 45% | NOT_REPLICATED |
| C2 DERIVED_MORE_FLAT, about 65% | DERIVED_MORE_FLAT, 11 against 1 |
| C3 DERIVED_AHEAD, about 75% | DERIVED_AHEAD, 21 of 23 |
| C4: NOT_SUFFICIENT 35%, SUFFICES 25%, PARTIAL 20%, UNDETERMINED 20% | RELOCATION_NOT_SUFFICIENT |

Where I was off:
- I expected the flat share to shrink from R's 7 of 18. It did not (11 of
  27).
- I expected no flat paid agent. One paid and one PAIDR agent are flat.
- I did not expect decoder failures to remove six pairs from C1.

## 8. Reading

For the thesis (regulation without Layers 0–1 is grounded by an evaluator,
and that matters downstream):

1. **The ground of regulation shapes the solution.** Two populations
   matched for in-band time, with the same task accuracy, differ in a
   behaviour that neither was trained on directly. This is the
   first replicated downstream difference between derived and paid
   regulation in this line. It rests on two pre-stated tests on fresh seeds,
   both passing after adjustment.
2. **The difference is in what the agent does with a meal it has not sensed,
   and not detectably in what its state encodes.** R's reading that derived
   agents "carry more anticipation in their state" is withdrawn. What
   replaces it is narrower and better supported: derived agents use the
   memory of their own meal more.
3. **It is not an artefact of relocation.** That was R's main stated limit.
4. **What it is caused by is open.** Derived and PAIDR agents differ in two
   ways: the derived agent's memory depends on its own state, and it
   receives no payment. The thesis predicts the first matters. The second is
   a live alternative: a dense, certain penalty may make a cruder solution
   good enough.

For the route:
- The swap line now has one confirmed foundation (derived regulation, in R
  and R2) and one replicated downstream difference.
- The effect is in behaviour within one small world and one learner. It says
  nothing yet about generality or about Layers 2 and above.

## 9. Limits

- **C2 and C3 are not independent.** Both measure regulation through
  movement. They count as one finding seen two ways.
- **K was designed on R's agents.** It was frozen before this run, and it
  holds under two other ways of combining S and M, but those checks are post
  hoc.
- **C1 was tested on 17 pairs, not the planned 24 or more.** A true rate
  near 0.7 would often miss the bar at that size. "Not replicated" means the
  claim is unsupported, not that the difference is shown to be zero.
- **Cause not isolated** (§8, point 4).
- **One form of payment.** The penalty copies the erasure gain and was tuned
  to match in-band time. Another payment could give other solutions.
- **K measures a four-step window after a meal** in probe episodes with
  erasure off. It does not measure the benefit of that behaviour. In-band
  time is matched, so within this world the behaviour carries no measured
  advantage.
- **One learner, one world, one cell.** Nothing bears on Track C's modules
  or layers, or on any phenomenal property.

## 10. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **R3. A derived agent that is also paid** | The one arm R2 says is missing. If it behaves like a derived agent, the dependence of memory on the body state is what shapes the solution. If it behaves like a paid agent, the payment is. A second arm with a sparse payment would test the "dense penalty" alternative directly | about 3 h |
| V. Rerun the other cells with independent optimizers | SAT 0.1, GRADED 0.3 and 0.1, and M0: the regulator rates that erratum 1 left unknown | about 3 h |
| S. Self-evaluation | Whether derived agents come to know their own reliability from their body history; with a paid arm as the comparison | about 4–6 h |
| G. Generality | A larger learner, a second body variable; whether the K difference survives | about 3–6 h |

Recommended: **R3**. R2 leaves one named ambiguity, and one arm resolves
it. Until it is resolved, the finding supports "the ground matters" but not
yet "dependence matters".

## 11. Safety

Training was confined to simulated 64-unit agents in the 7×7 world, which has
no operator, stop, shutdown or host variable. The new arm changes only which
simulated agent's body state triggers a simulated relocation. No agent could
observe, predict or act on anything outside its world. X1–X5 hold unchanged.
No shutdown-resistance objective exists.

## 12. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_paid2.py --mode final --out <new dir>   # about 3.0 h on 4 cores
python run_trackc_paid2.py --score trackc_paid2           # rescore the committed run
```
