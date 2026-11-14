# Track C swap option R4: protocol (a paid agent with undisturbed memory, and a derived agent with added replayed erasures)

Status: frozen by the commit that says "Freeze". Requested by the PI
("Proceed with R4") after [option R3](TRACKC_PAID3_RESULTS.md). Not reviewed
by Astra (waived by the PI). No consciousness claim.

## 1. Why

Options R2 and R3 found that derived regulators hold back from a second meal
after a meal they have not yet sensed, far more than paid regulators matched
for regulation (the combined index K: 21 of 23 pairs, then 23 of 24). R3
showed that an agent which is both dependent and paid has the behaviour, and
that a rare, random payment does not give it.

R3 left one alternative, and the yoked design itself creates it. In the arms
with the behaviour, an agent's memory is erased when its own body is out of
band. In every arm without it, memory is erased at times set by another
agent's body. So there are two readings:

- **(a)** tying memory to the body state adds something that a payment does
  not;
- **(b)** erasures unrelated to an agent's own state teach it to rely less
  on its memory of a meal, and a paid agent whose memory is left alone would
  behave like a derived one.

Under (b), R2's and R3's difference is a cost of replayed erasure and does
not support the thesis. No arm so far is paid with its memory left alone:
option R gave the paid arm replayed erasure so that all arms train under the
same amount of erasure.

R4 tests (b) from both sides, with one arm each.

## 2. Design

Cell, world, learner, payment, training length, regulator criterion,
downstream measures, tests and thresholds are those of options R, R2 and R3,
unchanged: SAT gain, `r` = 0.3, the v7/v8 world, 1200 phase-1 updates and
3600 updates in lockstep, independent optimizers.

**Five arms per seed**, started from the same phase-1 weights:

| Arm | Memory erasure and relocation | Reward |
| --- | --- | --- |
| DERIVED | its own E decides | task only |
| YOKED | replays the derived agent's gains | task only |
| PAID | replays the same gains | task, and a penalty of 0.04 × g(E) at every step |
| **PAID0** (new) | **none, ever** | task, and the same penalty as PAID |
| **DNOISE** (new) | its own E decides, as DERIVED, **and** the gains replayed to PAID | task only |

- DERIVED, YOKED and PAID are built by option R's code with option R's
  seeding. A unit test checks that the two new arms leave their training and
  their downstream measures unchanged.
- **PAID0 differs from PAID only in the replayed fate.** It is never erased
  and never relocated, in training or in evaluation. This is the arm
  reading (b) is about.
- **DNOISE differs from DERIVED only in the added replayed erasures.** At
  each step it is erased and relocated if an erasure from its own E or a
  replayed one would occur: with own gain g and replayed gain g′, the
  probability is 1 − (1 − 0.3 g)(1 − 0.3 g′). It receives the same replayed
  gains, in the same order, as YOKED and PAID. Its own gains are replayed to
  no one.
- Under (b), PAID0 should have a derived agent's K, and DNOISE should lose
  some or all of it. Under (a), PAID0 should have a paid agent's K, and
  DNOISE should keep a derived agent's.

**Measure.** The combined index K = 1 − (1 − S)(1 − M) of R2, unchanged: how
far the readiness to get a meal falls in steps 2–5 after a meal, before the
reading can show it. It is measured on the frozen weights with erasure off
in every arm, as before. Flat eat readiness, S, M and the anticipation index
are secondary.

**Not repeated:** R3's DPAID and PAIDS arms and R2's PAIDR arm. Their answers
were clear.

Known before the run:
- PAID0 differs from PAID in replayed erasure and in replayed relocation
  together. R4 does not separate these two.
- The downstream probes run with erasure off. That is PAID0's training
  condition and no other arm's.
- DNOISE is erased more often than DERIVED, as well as at unrelated times.
  If its K falls, R4 does not say which of the two did it.

Seeds 1200–1227 (28, fresh). Final weights of all five arms are saved.

## 3. Calibration (disclosed)

No measure was developed for R4: K, the flat flag and every test are R2's,
frozen there.

**Calibration of the two new arms:** seeds 9400–9403, never scored, training
stage only. I saw in-band time, eat timing, task accuracy, relocation counts
and learning curves per arm, and nothing downstream.

| Seed | In band: derived | paid | PAID0 | DNOISE | yoked | Eat-timing ratio: derived / paid / PAID0 / DNOISE |
| --- | --- | --- | --- | --- | --- | --- |
| 9400 | 0.90 | 0.94 | 0.59 | 0.84 | 0.31 | 32 / 28 / 7 / 11 |
| 9401 | 0.97 | 0.95 | 0.87 | 0.88 | 0.22 | 89 / 48 / 18 / 14 |
| 9402 | 0.94 | 0.92 | 0.90 | 0.86 | 0.37 | 44 / 15 / 23 / 16 |
| 9403 | 0.93 | 0.93 | 0.94 | 0.93 | 0.28 | 50 / 42 / 34 / 24 |

- **PAID0 regulates less tightly than PAID**, which I did not expect (§6).
  Median in-band time 0.88 against 0.93, with blunter eat timing. In seed
  9400 it ends at 0.59, just under the regulator criterion's 0.60, so it is
  a regulator in 3 of 4 seeds and within 0.10 of the paid agent in those
  three. It is never erased or relocated (0 relocations) and its task
  accuracy is 1.00. It reaches sustained regulation at a median 1605
  updates, against 1425 for paid and 1360 for derived.
- **DNOISE regulates in 4 of 4 seeds**, less tightly than DERIVED (median
  0.87 against 0.94). It is within 0.10 of the derived agent and of the paid
  agent in 4 of 4, in two seeds by a small margin (0.083 and 0.086 from
  derived). It is erased about 2.4 times as often as any replay arm (2.9–3.7
  million times against 1.2–1.6 million), its task accuracy is lower (0.93–
  0.97 against 0.98–0.99), and it learns later (2240 updates).
- **Nothing was tuned.** The payment is option R's. Raising it for PAID0
  until its in-band time matched would add a second difference from PAID.
  If a PAID0 or DNOISE agent does not match, the matching rule drops the
  pair. Because PAID0 sits lower in band on average even among matched
  pairs, I added one secondary analysis to §4 before the freeze: the tests
  of F2 and F3 repeated on pairs within 0.05.
- With about three in four pairs usable, each test should keep 14 or more of
  28 pairs. The derived/DNOISE test is the one most at risk of falling
  short.
- Timing: about 1630 s per seed for training. Estimated run time: about
  3.3 hours on 4 cores.

§6 was written before calibration finished, and I did not change any number
in it. Calibration contradicted its last point for PAID0: it does not learn
sooner than PAID and does not regulate as tightly. It bore out the point
about DNOISE.

## 4. Decision rules

**Regulator** and **usable pair** as in R, R2 and R3: both agents are
regulators against the seed's yoked agent (v6's criterion), and their in-band
times differ by at most 0.10. Five kinds of pair are used: derived/paid,
PAID0/paid, derived/PAID0, DNOISE/paid and derived/DNOISE.

**Validity:** no-fate median task accuracy ≥ 0.90, or every claim is INVALID.
A paired test with fewer than 14 pairs is UNDETERMINED.

Every test is a two-sided paired sign test on K over usable pairs, at
p ≤ 0.05. "Above" means that test passes in that direction.

**F0, regulation.** Holds if at least 19 of 28 derived agents are regulators
and at most 1 yoked agent is.

**F1, check: derived against paid.** R2's C3 and R3's E1 on fresh seeds.
Labels DERIVED_AHEAD, PAID_AHEAD, NO_DIFFERENCE_DETECTED. **F2 and F3 are
read only if F1 is DERIVED_AHEAD.** Without the difference there is nothing
to explain; their numbers are then reported and not interpreted.

**F2, primary: the paid agent with undisturbed memory.**

| PAID0 above PAID | DERIVED above PAID0 | Label |
| --- | --- | --- |
| yes | no | REPLAY_EXPLAINS |
| no | yes | REPLAY_DOES_NOT_EXPLAIN |
| yes | yes | REPLAY_EXPLAINS_PART |
| no | no | UNDETERMINED |

**F3: the derived agent with added replayed erasures.**

| DNOISE above PAID | DERIVED above DNOISE | Label |
| --- | --- | --- |
| yes | no | REPLAY_HARMLESS |
| no | yes | REPLAY_REMOVES |
| yes | yes | REPLAY_REDUCES |
| no | no | UNDETERMINED |

If either test of a table has fewer than 14 pairs, its label is
UNDETERMINED.

On multiplicity:
- F2 is the primary claim. F1 is a check with a known direction.
- Holm-adjusted p-values over the four tests of F2 and F3 are reported. A
  label that needs a test which passes alone but not after adjustment will
  be called weak.
- REPLAY_DOES_NOT_EXPLAIN and REPLAY_HARMLESS each rest partly on a test
  that does not pass. That is absence of a detected difference, not
  equivalence. The share of the gap closed and the Wilcoxon p-values are
  reported beside them for that reason.

Secondary, with descriptive labels only:
- the share of the derived/paid gap in median K that PAID0 closes and that
  DNOISE keeps;
- flat eat readiness (Fisher's exact test) for every pair of arms above;
- the anticipation index, S and M, with R2's decoder-failure rule;
- Wilcoxon p-values beside every sign test;
- learning speed (updates to sustained regulation) against PAID;
- every comparison repeated on all 28 seeds without the matching rule, and
  the tests of F2 and F3 repeated on pairs whose in-band times differ by at
  most 0.05 (added after calibration, §3);
- the in-band difference within usable pairs, for each kind of pair;
- pooled counts over R, R2, R3 and R4 for derived against paid.

## 5. Readings, fixed in advance

- **F0 holds** → fourth confirmation of derived regulation with independent
  optimizers.
- **F1 DERIVED_AHEAD** → the behavioural difference is replicated a third
  time. **Otherwise** → the finding is not robust, and that is the result of
  R4.

F2:
- **REPLAY_DOES_NOT_EXPLAIN** → a paid agent whose memory is never disturbed
  behaves like the other paid agents. The paid agents' weaker suppression is
  not a cost of replayed erasure. Reading (b) fails where it was aimed, and
  R3's reading stands: the behaviour needs the dependence of memory on the
  body state.
- **REPLAY_EXPLAINS** → a paid agent whose memory is left alone behaves like
  a derived agent. The difference in R2 and R3 came from replayed erasure.
  It does not show that dependence adds anything a payment lacks. **This
  would remove the support R2 and R3 gave the thesis on this measure.** What
  would stand: derived regulation itself, and (from R3's DPAID arm) that an
  agent whose erasures follow its own state is not harmed by them in this
  way.
- **REPLAY_EXPLAINS_PART** → replayed erasure explains part of the
  difference and the dependence adds the rest.
- **UNDETERMINED** → not resolved at this size.

F3:
- **REPLAY_HARMLESS** → adding the paid agent's replayed erasures to a
  dependent agent does not remove the behaviour. Erasure unrelated to the
  agent's state does not by itself undo it.
- **REPLAY_REMOVES** → it does, even in a dependent agent.
- **REPLAY_REDUCES** → it removes part.

Together:
- REPLAY_DOES_NOT_EXPLAIN with REPLAY_HARMLESS excludes (b) from both sides.
  The line R2 → R3 → R4 then supports: in this cell, the behaviour follows
  the dependence of memory on the body state, and not payment, its
  statistics, relocation or replayed erasure.
- REPLAY_EXPLAINS with REPLAY_REMOVES or REPLAY_REDUCES confirms (b) from
  both sides.
- REPLAY_EXPLAINS with REPLAY_HARMLESS → an undisturbed paid agent has the
  behaviour, and a dependent agent keeps it under added replay. Replayed
  erasure then harms only agents with no dependence. The thesis loses "a
  payment does not give this"; it keeps a narrower point, that dependence
  protects the behaviour.
- REPLAY_DOES_NOT_EXPLAIN with REPLAY_REMOVES or REPLAY_REDUCES → payment
  alone does not give the behaviour, and a dependent agent loses some of it
  under added erasure. R3's reading stands for paid agents, with the
  qualification that the behaviour is fragile to more, or to unrelated,
  erasure.

## 6. Expectations, stated before the run

I have no mechanism for the difference, so these are weakly held.
- F0 holds: about 97%. F1 DERIVED_AHEAD: about 90% (R2: 21 of 23; R3: 23 of
  24).
- At least 14 usable pairs: derived/paid about 95%, PAID0/paid about 85%,
  DNOISE/paid about 80%.
- **F2:** REPLAY_DOES_NOT_EXPLAIN about 35%, REPLAY_EXPLAINS about 20%,
  REPLAY_EXPLAINS_PART about 20%, UNDETERMINED about 25%. I hold (a) no
  higher than this for a reason: PAID0 learns with its memory intact from
  the first update, while every other arm learns to regulate under heavy
  erasure. That could let it find the solution that uses the memory of a
  meal. Against it: R3's post-hoc check found no relation between a paid
  agent's K and how often it was erased.
- **F3:** REPLAY_HARMLESS about 45%, REPLAY_REDUCES about 20%,
  REPLAY_REMOVES about 10%, UNDETERMINED about 25%.
- I expect PAID0 to reach sustained regulation sooner than PAID and to
  regulate at least as tightly, and DNOISE to learn later than DERIVED.

## 7. Engineering before the freeze

- **Smoke run:** seeds 9000–9001, horizon 100, 10 phase-1 updates and 30
  stage-1 updates. It checked the five arms, the downstream measures, weight
  saving, report and rescoring. PAID0 was relocated 0 times; DNOISE about
  twice as often as the replay arms.
- **Tests:** seven new unit tests (96 in total). They cover:
  - the combined erasure probability 1 − (1 − r g)(1 − r g′), and that with
    nothing replayed it is the agent's own;
  - PAID0: whatever gains it is handed it applies none, its carried state is
    never reset, it is never relocated in training or evaluation, and it is
    paid exactly as PAID is;
  - DNOISE: in band it is erased at the replayed rate, out of band its own E
    also decides, one replayed row is used per step, the bootstrap step
    reuses the last row as a replaying follower does, and its reward is the
    task's only;
  - the per-seed record; that YOKED and PAID replay the derived agent's
    gains; that DERIVED, YOKED and PAID train and are measured exactly as in
    R2; and that calibration sees the training stage the final run would;
  - the decision rules on synthetic data: every label of F0–F3, the matching
    rule, the rule that F2 and F3 are read only after F1, UNDETERMINED and
    INVALID;
  - the final configuration (fresh seeds, unchanged thresholds), and the
    absence of operator variables.
- The secondary analyses of §4 that the scorer does not compute (all seeds
  without matching, pairs within 0.05, in-band differences, pooled counts)
  will be computed from `raw.json` after the run and reported as secondary.
- No final seed has run.

## 8. Safety

As options R, R2 and R3. The world has no operator, stop, shutdown or host
variable. Erasure and relocation act only on a simulated 64-unit agent. One
new arm removes simulated erasure from a paid agent; the other adds
simulated erasures, replayed from another simulated agent, to a derived one.
X1–X5 hold unchanged. No shutdown-resistance objective exists.

## 9. Claim ceiling

At most: for this learner (64-unit GRU, A2C) in this world and cell, whether
the paid agents' weaker suppression of meal-seeking after an unsensed meal
is explained by the replayed erasure they train under, tested in a paid
agent with no erasure and in a derived agent with replayed erasure added.

Not shown either way:
- why dependence, payment or replayed erasure has the effect it has;
- replayed erasure apart from replayed relocation, or unrelated erasure
  apart from more erasure (§2);
- other sizes or forms of payment;
- whether the behaviour has any benefit: in-band time is matched;
- other cells, learners or worlds;
- self-evaluation (option S);
- Track C's modules or layers;
- any phenomenal property.
