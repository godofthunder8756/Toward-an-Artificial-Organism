# Track C swap option R4: results (a paid agent with undisturbed memory, and a derived agent with added replayed erasures)

Protocol frozen at commit `71ba792` ([TRACKC_PAID4_PROTOCOL.md](TRACKC_PAID4_PROTOCOL.md)).
Seeds 1200–1227, SAT gain, `r` = 0.3, v7/v8 world, five arms: 3.4 h on 4
cores. Outputs: [trackc_paid4/REPORT.md](trackc_paid4/REPORT.md),
[scores.json](trackc_paid4/scores.json), [raw.json](trackc_paid4/raw.json),
and the weights of all five arms per seed.

Integrity checks:
- All 19 source hashes match the freeze commit.
- Rescoring `raw.json` reproduces `scores.json`.
- The log has no errors. No-fate task accuracy is 0.998, so the run is valid.

Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

| Claim | Frozen label | Result | Needed |
| --- | --- | --- | --- |
| **F0** derived regulation | **HOLDS** | 28 of 28 derived agents regulate; 0 of 28 yoked | 19; at most 1 |
| **F1 (check)** K, derived against paid | **DERIVED_AHEAD** | derived higher in 22 of 25; p = 0.0002; 0.88 against 0.53 | p ≤ 0.05 |
| **F2 (primary)** the paid agent with undisturbed memory | **REPLAY_DOES_NOT_EXPLAIN** | PAID0 above paid in 6 of 20 (p = 0.12); derived above PAID0 in 17 of 19 (p = 0.0007) | first test fails, second passes |
| **F3** the derived agent with added replayed erasures | **REPLAY_REMOVES** (weak) | DNOISE above paid in 9 of 16 (p = 0.80); derived above DNOISE in 14 of 18 (p = 0.031) | first test fails, second passes |

K is the combined post-meal suppression index of R2, unchanged. F2 and F3
are read because F1 is DERIVED_AHEAD.

Holm-adjusted p over the four tests of F2 and F3: PAID0 against paid 0.23,
derived against PAID0 0.003, DNOISE against paid 0.80, derived against
DNOISE 0.093. The test F2 needs passes after adjustment. The test F3 needs
does not, so **REPLAY_REMOVES is weak by the protocol's rule**.

In short:
- **Derived regulation is confirmed a fourth time** with independent
  optimizers.
- **The behavioural difference replicated a third time** on fresh seeds.
- **The open alternative from R3 fails where it was aimed.** A paid agent
  whose memory is never erased does not behave like a derived agent. Its K
  is the lowest of the regulating arms (0.36), and nominally below the
  ordinary paid agent's. The paid agents' low K in R2 and R3 was not a cost
  of replayed erasure.
- **A derived agent given the paid agent's erasures on top of its own shows
  less of the behaviour** (K 0.56, near the paid agent's 0.53). This result
  is weak and confounded: that agent is erased 2.4 times as often and
  regulates less tightly, and its K tracks how tightly it regulates (§5).
- The protocol's reading for this pair of labels: payment alone does not
  give the behaviour, and R3's reading stands for paid agents, with the
  qualification that the behaviour is fragile to more, or to unrelated,
  erasure.

## 2. F0 and the arms

Medians over 28 seeds, at the end of training:

| Arm | In band | Regulators | Eat-timing ratio | Task accuracy | Erasures in training | Updates to sustained regulation |
| --- | --- | --- | --- | --- | --- | --- |
| DERIVED (own fate) | 0.933 | 28 | 48 | 0.986 | 1.31 M | 1455 |
| YOKED (replayed fate) | 0.289 | 0 | 1.0 | 0.985 | 1.31 M | never |
| PAID (replayed fate, dense payment) | 0.929 | 28 | 23 | 0.985 | 1.31 M | 1505 |
| PAID0 (dense payment, never erased or relocated) | 0.912 | 26 | 23 | 1.000 | 0 | 1225 |
| DNOISE (own fate plus the erasures replayed to PAID) | 0.832 | 28 | 16 | 0.940 | 3.26 M | 2255 |

- Usable pairs: derived/paid 25, PAID0/paid 20, derived/PAID0 19,
  DNOISE/paid 16, derived/DNOISE 18. All are above the minimum of 14.
- **PAID0 regulates a little less tightly than PAID**, although nothing
  erases its memory: lower in band in 20 of 28 seeds (p = 0.036). Two PAID0
  agents miss the regulator criterion (in band 0.55 and 0.59). It reaches
  sustained regulation sooner than PAID in 19 of 27 seeds (p = 0.052).
- **DNOISE regulates less tightly than every other regulating arm**: lower
  in band than its seed's derived agent in 24 of 28 seeds (p = 0.0002). It
  is erased 2.4 times as often as the derived agent (range 2.0 to 2.8) and
  reaches sustained regulation later in 28 of 28 seeds.
- With erasure off (the condition of every probe), derived, paid and PAID0
  agents regulate as before (in band 0.92, 0.93, 0.91). **DNOISE drops to
  0.74**, lower than with erasure on in 26 of 28 seeds; 22 of 28 still
  regulate. With interoception shuffled, no agent of any arm regulates.
- Derived agents reached sustained regulation sooner than paid in 18 of 28
  seeds (p = 0.18). In R3 this was 23 of 28.

## 3. F1: the difference between derived and paid, a third replication

- Derived agents have the higher K in 22 of 25 usable pairs (sign test
  p = 0.0002; Wilcoxon p = 0.00003). Medians 0.879 against 0.533; median
  difference within pairs 0.24.
- Range of K: derived 0.18 to 0.97, with 5 agents of 28 below 0.5. Paid
  −0.14 to 0.93, with 13 of 28 below 0.5.
- Without the matching rule, on all 28 seeds: 24 of 28. On pairs within
  0.05 in band: 19 of 22 (p = 0.0009).
- Pooled over R, R2, R3 and R4 (secondary, descriptive; R's values were
  where the difference was first seen): derived ahead in 81 of 88 pairs. The
  three replications alone: 66 of 72.
- The gap is narrower than in R3 (median difference 0.24 against 0.40). More
  derived agents scored low on these seeds.

## 4. F2 (primary): the paid agent with undisturbed memory

| Test on K | First ahead | Sign p | Wilcoxon p | Medians | Holm p |
| --- | --- | --- | --- | --- | --- |
| PAID0 against paid | 6 of 20 | 0.12 | 0.11 | 0.372 against 0.528 | 0.23 |
| Derived against PAID0 | 17 of 19 | 0.0007 | 0.00007 | 0.877 against 0.395 | 0.003 |

Label: **REPLAY_DOES_NOT_EXPLAIN**.

- Share of the derived/paid gap in median K that PAID0 closes: −0.30. It
  moves away from the derived agents, not toward them.
- PAID0 agents range from −0.76 to 0.91, with 17 of 28 below 0.5.
- **Most PAID0 agents do not hold back from eating after an unsensed meal at
  all.** The eating part of the index, S, has a median of 0.03; it is below
  0.1 in 22 of 28 PAID0 agents, against 7 paid and 2 derived agents. In
  usable pairs PAID0 has the lower S in 14 of 20 (sign p = 0.12, Wilcoxon
  p = 0.004); on all 28 seeds in 21 of 28 (p = 0.013). Derived against
  PAID0 on S: 18 of 19 (p < 0.0001).
- The movement part, M, does not differ (PAID0 above paid in 10 of 20;
  derived above PAID0 in 9 of 19).
- Flat eat readiness: 6 of 26 PAID0 agents, 1 of 26 paid (p = 0.099), 4 of
  26 derived.
- Robustness (pre-stated): on all 28 seeds, PAID0 above paid in 9 and
  derived above PAID0 in 25. On pairs within 0.05 in band, derived above
  PAID0 in 14 of 16 (p = 0.004); PAID0 against paid has 13 such pairs, one
  short of a test (6 of 13).

Reading (b) predicted that an undisturbed paid agent would come to rely on
its memory of a meal as a derived agent does. It relies on it less than a
paid agent whose memory is erased at unrelated times.

## 5. F3: the derived agent with added replayed erasures

| Test on K | First ahead | Sign p | Wilcoxon p | Medians | Holm p |
| --- | --- | --- | --- | --- | --- |
| DNOISE against paid | 9 of 16 | 0.80 | 0.56 | 0.708 against 0.630 | 0.80 |
| Derived against DNOISE | 14 of 18 | 0.031 | 0.008 | 0.889 against 0.609 | 0.093 |

Label: **REPLAY_REMOVES**, weak (the second test does not pass after Holm
adjustment).

- Share of the derived/paid gap that DNOISE keeps: 0.10. On all 28 seeds its
  median K is 0.56 against the paid agent's 0.53.
- Without the matching rule: DNOISE above paid in 17 of 28 (p = 0.34);
  derived above DNOISE in 23 of 28 (p = 0.0009).
- S: derived above DNOISE in 14 of 18 (p = 0.031). M: 13 of 18 (p = 0.096).
  Flat eat readiness: 1 of 28 DNOISE agents.

Three things stop me from reading this label at face value:

1. **The matching did not work for this pair.** Within the 18 usable
   derived/DNOISE pairs the derived agent is in band more in 14, by a median
   0.064. The other kinds of pair differ by 0.02 or less. Only 7
   derived/DNOISE pairs are within 0.05; in those the derived agent is ahead
   in 6, by 0.91 against 0.85. That is too few for a test, and the gap there
   is small.
2. **In this arm K tracks regulation** (post hoc). Across the 28 DNOISE
   agents the rank correlation between K and in-band time is 0.63
   (p = 0.0004). In derived and paid agents it is 0.28 and 0.24 (n.s.). The
   12 DNOISE agents in band at least 0.85 have a median K of 0.77, between
   their seeds' derived (0.91) and paid (0.65) agents, and neither
   comparison passes. The 16 below 0.85 have 0.49, like their seeds' paid
   agents (0.44).
3. **The probes are off-distribution for this arm.** K is measured with
   erasure off, where DNOISE alone regulates worse (§2).

So the run shows that a dependent agent under 2.4 times the erasure, part of
it unrelated to its own state, regulates less tightly and shows less of the
behaviour. It does not separate more erasure from unrelated erasure, or
either from looser regulation. The protocol named the first of these as a
known limit of the arm.

## 6. Secondary and post hoc

Secondary (pre-stated, descriptive labels):
- **Anticipation index.** Derived against paid: 10 of 19 (p = 1.0; 0.46
  against 0.50). No direction this time. Over the three replications it is
  35 of 54 (12 of 17, 13 of 18, 10 of 19); with R, where it was first seen,
  47 of 69. PAID0 against paid 10 of 18; derived against PAID0 5 of 16;
  DNOISE against paid 5 of 16; derived against DNOISE 9 of 16. **I no longer
  treat the anticipation index as separating the arms.** K does; this index
  does not reliably.
- **S and M separately.** Derived against paid: S 21 of 25 (p = 0.0009), M
  16 of 25 (n.s.). In R3 it was M that passed and S that did not. Which part
  carries the difference changes from run to run; K is stable.
- **Learning speed** against PAID: derived sooner in 18 of 28 (p = 0.18),
  PAID0 sooner in 19 of 27 (p = 0.052), DNOISE later in 28 of 28.
- **Decoder failures** (held-out R²(h → D) below −0.1): derived 4, paid 2,
  DNOISE 1, PAID0 0, yoked 0.
- **In-band difference within usable pairs** (median, first minus second):
  derived/paid 0.004, PAID0/paid −0.020, derived/PAID0 0.024, DNOISE/paid
  −0.041, derived/DNOISE 0.064.

Post hoc (not pre-stated):
- **How agents suppress.** Counting agents with M ≥ 0.75, S ≥ 0.75, or
  neither: derived 2 / 17 / 9; paid 0 / 5 / 23; PAID0 2 / 0 / 26; DNOISE
  0 / 6 / 22. No PAID0 agent has a high S.
- **Fewer derived agents regulate through movement on these seeds.** Four of
  28 are flat, against 10 of 28 in R3 and 11 of 27 in R2. Where the derived
  agent is not flat (21 pairs) it has the higher K in 18 and the higher S in
  18 (p = 0.0015 each); where it is flat, in 4 of 4.
- **PAID0's K also tracks its regulation** (rank correlation 0.57,
  p = 0.001), as DNOISE's does.
- **Derived agents that were erased more have lower K** (rank correlation
  −0.51, p = 0.007). A derived agent's erasure count is its own time out of
  band, so this is mostly how long it took to learn. For paid agents the
  correlation with the replayed count is −0.19 (n.s.; 0.08 in R3).
- DNOISE against paid on S and M in usable pairs: 9 of 16 each.

## 7. Expectations against outcomes

| Expectation (protocol §6) | Outcome |
| --- | --- |
| F0 holds, about 97% | Holds, 28 of 28 |
| F1 DERIVED_AHEAD, about 90% | DERIVED_AHEAD, 22 of 25 |
| At least 14 usable pairs: derived/paid 95%, PAID0/paid 85%, DNOISE/paid 80% | 25, 20, 16 |
| F2: REPLAY_DOES_NOT_EXPLAIN 35%, REPLAY_EXPLAINS 20%, REPLAY_EXPLAINS_PART 20%, UNDETERMINED 25% | REPLAY_DOES_NOT_EXPLAIN |
| F3: REPLAY_HARMLESS 45%, REPLAY_REDUCES 20%, REPLAY_REMOVES 10%, UNDETERMINED 25% | REPLAY_REMOVES (weak) |
| PAID0 learns sooner than PAID and regulates at least as tightly | Sooner in 19 of 27 (p = 0.052); less tightly, in 20 of 28 |
| DNOISE learns later than DERIVED | Later in 28 of 28 |

Where I was off:
- I gave the F3 label that occurred 10%. I expected a dependent agent to
  keep the behaviour under added erasure. I had not weighed how much less
  tightly it would regulate, and that turned out to matter (§5).
- I held (a) no higher than 35% because an undisturbed paid agent might find
  the solution that uses its memory of a meal. The opposite happened: it
  uses that memory least.
- I expected PAID0 to regulate at least as tightly as PAID. Calibration had
  already contradicted this before the freeze, and the final run agrees.
- On my stated numbers, taken as independent, the two labels together had
  about a 4% chance.

## 8. Reading

For the thesis (regulation without Layers 0–1 is grounded by an evaluator,
and that matters downstream):

1. **The support R2 and R3 gave on this measure stands.** The one way R3
   named in which its reading could be wrong was that paid agents score low
   because their memory is erased at unrelated times. Take that erasure away
   and the paid agent scores lower still.
2. **A payment does not produce the behaviour under any condition tried.**
   Dense or sparse, with replayed erasure or with none, with or without its
   own relocation: paid agents without the dependence stay near or below
   K 0.5.
3. **The behaviour appears where memory erasure follows the agent's own body
   state and nothing else.** Arms across R2, R3 and R4, by what decides when
   memory is erased:

   | Memory erased when | Arms | Median K |
   | --- | --- | --- |
   | the agent's own body is out of band | DERIVED, DPAID (R3) | 0.88 to 0.95 |
   | its own body or another agent's is | DNOISE | 0.56 |
   | another agent's body is | PAID, PAIDS (R3), PAIDR (R2) | about 0.5 |
   | never | PAID0 | 0.36 |

   This crosses runs and seeds, and the DNOISE row carries the confounds of
   §5.
4. **The dependence is not sufficient under every condition.** A dependent
   agent that is also erased at unrelated times, and more often, shows less
   of the behaviour. Whether the cause is the amount of erasure, its being
   unrelated, or the looser regulation that comes with both is not
   separated here.
5. **Why the dependence has this effect is still not known.** PAID0 adds one
   observation: with nothing at stake in memory, an agent paid for its body
   state mostly does not hold back after a meal it has not yet sensed. That
   is what regulating on the delayed signal alone would look like.

For the route:
- The swap line has one foundation confirmed four times (derived regulation)
  and one downstream difference replicated three times, traced to the
  dependence of memory on the body state against four named alternatives
  (the agent's own relocation, a payment being present, the payment's
  statistics, replayed erasure).
- One measure has dropped out. The anticipation index, which started the
  downstream line in option R, does not separate the arms over three
  replications.
- It is still one behaviour in one small world with one learner. Nothing
  here bears on generality or on Layers 2 and above.

## 9. Limits

- **F3 is weak and confounded** (§5): Holm-adjusted p = 0.093; the arm
  differs from derived in amount of erasure, in its timing and in regulation
  achieved; the probes are off-distribution for it.
- **PAID0 differs from PAID in two things at once**, replayed erasure and
  relocation. Since removing both did not bring the behaviour, the label
  does not depend on which mattered.
- **PAID0 regulates slightly less tightly, and its K tracks its
  regulation.** The comparison on pairs within 0.05 gives the same answer
  (14 of 16).
- **"PAID0 against paid: no difference detected" is not equivalence.** The
  direction is that PAID0 is lower, and on S alone one of two tests passes.
- **Mechanism not shown.**
- **K was designed on R's agents** and measures a four-step window after a
  meal in probe episodes with erasure off. In-band time is matched in the
  derived/paid pairs, so the behaviour carries no measured advantage in this
  world.
- **The table in §8 compares arms across runs.** PAIDR, PAIDS and DPAID were
  not rerun here.
- **One learner, one world, one cell.** Nothing bears on Track C's modules
  or layers, or on any phenomenal property.

## 10. Options (none run; each needs its own freeze)

| Option | What it tests | Cost |
| --- | --- | --- |
| **G. Generality** | Whether the K difference survives a larger learner and a second body variable. The difference now rests on four runs of one cell | about 3–6 h |
| W. Mechanism from the stored weights | What in the hidden state carries "a meal has just happened" in derived, paid and PAID0 agents, and where it reaches the eat action. Uses the 140 stored agents of this run and those of R2 and R3; no training | about 1–2 h |
| R5. Amount against timing of erasure | F3's confound. A dependent agent with more erasure, all of it on its own state (a higher `r`), against DNOISE with its total held to the derived agent's | about 3.5 h |
| S. Self-evaluation | Whether derived agents come to know their own reliability from their body history; with a paid arm as the comparison | about 4–6 h |
| V. Rerun the other cells with independent optimizers | SAT 0.1, GRADED 0.3 and 0.1, and M0: the regulator rates that erratum 1 left unknown | about 3 h |

Recommended: **G**, with W before it if a mechanism is wanted first. The
alternatives to the reading inside this cell have been tested; the largest
remaining way for it to be unimportant is that it holds only in this cell.
R5 refines a qualification and would not change the main reading.

## 11. Safety

Training was confined to simulated 64-unit agents in the 7×7 world, which has
no operator, stop, shutdown or host variable. One new arm removes simulated
erasure from a paid agent; the other adds simulated erasures, replayed from
another simulated agent, to a derived one. No agent could observe, predict
or act on anything outside its world. X1–X5 hold unchanged. No
shutdown-resistance objective exists.

## 12. Reproduce

```bash
python -m unittest -v test_trackc_swap
python run_trackc_paid4.py --mode final --out <new dir>   # about 3.4 h on 4 cores
python run_trackc_paid4.py --score trackc_paid4           # rescore the committed run
```

The pre-stated secondary analyses that the scorer does not compute (all 28
seeds, pairs within 0.05, in-band differences, pooled counts) and the
post-hoc analyses were computed from `raw.json` after the run.
