# Track C swap option R2: protocol (replication of derived against paid, with a relocation control)

Status: DRAFT until the commit that says "Freeze". Requested by the PI
("Proceed with R2") after [option R](TRACKC_PAID_RESULTS.md). Not reviewed by
Astra (waived by the PI). No consciousness claim.

## 1. Why

Option R gave the thesis its first direct support, and it was weak:
- **R1**, the anticipation index, put derived regulators ahead of paid ones
  in 13 of 16 usable seeds (p = 0.021). It was one of three uncorrected
  tests, and it did not hold over all 18 seeds.
- **Post hoc**, 7 of 18 derived agents did not gate the eat action at all,
  and no paid agent did the same. The inference was that those agents
  regulate through where they go. It was not measured.
- **A confound was open.** In this world an erasure also relocates the agent.
  A derived agent's position is tied to its own E and a paid agent's is not.

R2 asks three questions on fresh seeds:
1. Does R1 replicate as a single pre-stated claim?
2. Do derived and paid regulators differ in how they regulate, on measures
   fixed before the run?
3. Is any such difference due to relocation being tied to the agent's own E?

## 2. Design

Cell, world, learner, payment, training length and regulator criterion are
option R's, unchanged: SAT gain, `r` = 0.3, the v7/v8 world, a penalty of
0.04 × g(E) per step, 1200 phase-1 updates and 3600 updates in lockstep,
independent optimizers.

**Four arms per seed**, started from the same phase-1 weights:

| Arm | Memory erasure | Relocation | Reward |
| --- | --- | --- | --- |
| DERIVED | its own E decides | with each erasure (own E) | task only |
| YOKED | replays the derived agent's gains | with each erasure (replayed) | task only |
| PAID | replays the same gains | with each erasure (replayed) | task plus payment |
| **PAIDR** (new) | replays the same gains | **its own E decides**: probability 0.3 × g(E) per step | task plus payment |

- DERIVED, YOKED and PAID are built by option R's code with option R's
  seeding. A unit test checks that adding PAIDR leaves their training
  unchanged.
- **PAIDR separates the two parts of the dependence.** Its position depends
  on its own E exactly as a derived agent's does. Its memory does not: a
  replayed erasure does not move it, and its own relocation does not erase.

**Downstream measures**, on the frozen weights with erasure off:
- option P's decoding (the anticipation index) and the interoception shuffle,
  as in R;
- option Q's eat-propensity probe (S), as in R;
- **flat eat readiness** (new as a pre-stated measure). An agent is *flat* if
  its probability of eating, with food under it and no meal in the last 10
  steps, is at least 0.40 in every populated bin of the reading from 0.35 to
  0.50. This is the definition used post hoc in R, unchanged;
- **the approach index M** (new). At every step where food is visible and not
  under the agent, the policy's probability of a move toward the nearest
  visible food is read from the actual observation and state. Nothing is
  modified. M compares steps 2–5 after a meal with control steps at the same
  reading, by S's formula. M is to moving toward food what S is to the eat
  action;
- **the combined index K = 1 − (1 − S)(1 − M)**: how far the readiness to get
  a meal (approach food, then eat it) falls after a meal the agent has not
  yet sensed.

**Dropped from R:** the world shifts (R3 showed nothing) and the withdrawal
stage (R4 was clear in every seed).

Seeds 1000–1027 (28, fresh). R2 was proposed with 24 seeds; 28 are used to
raise the power of the primary test, at about 30 minutes' cost. Final weights
of all four arms are saved. Estimated run time: about 3.4 hours on 4 cores.

## 3. Development and calibration (disclosed)

**M and K were designed on option R's saved agents** (seeds 900–917, 54
agents, no training and no new seed). What I saw there:

| On R's 18 seeds | DERIVED | PAID | YOKED |
| --- | --- | --- | --- |
| M (median) | 0.49 | 0.18 | 0.01 |
| K (median) | 0.89 | 0.59 | 0.01 |

- M is higher for the derived agent in 17 of 18 seeds, and K in 17 of 18.
- The seven flat derived agents have M from 0.88 to 0.97. They stop
  approaching food after a meal almost completely. This supports R's
  inference that they regulate by movement.
- **These numbers are post hoc on R's data and are evidence of nothing by
  themselves.** M and K were built after seeing R's results, with the
  hypothesis in mind. They are the reason C2 and C3 exist. The test is on the
  fresh seeds.
- The new probe run reproduces option Q's run exactly (same trajectories and
  the same S), checked on a saved agent and in a unit test.

**Calibration of PAIDR:** seeds 9200–9203, never scored, stage 1 only. I saw
in-band time, eating, eat timing and task accuracy per arm, and nothing else.

CALIBRATION_TABLE

- The payment weight was not changed for PAIDR. Tuning it separately would
  add a second difference from PAID. If PAIDR does not match, the matching
  rule drops the pair.

## 4. Decision rules

**Regulator** and **usable pair** as in option R: both agents are regulators
against the seed's yoked agent (v6's criterion), and their in-band times
differ by at most 0.10. Three kinds of pair are used: derived/paid,
PAIDR/paid and derived/PAIDR.

**Validity:** no-fate median task accuracy ≥ 0.90, or every claim is INVALID.
A paired claim with fewer than 14 pairs is UNDETERMINED.

**Decoder failure:** if an agent's held-out R²(h → D) is below −0.10, its
anticipation index is undefined and its pair is left out of C1. (In R one
paid agent had R² = −8.5 and was counted as "derived ahead".) A small
negative R² is kept: it means the state carries no information.

**C0, regulation.** Holds if at least two thirds of derived agents are
regulators (19 of 28) and at most 1 yoked agent is.

**C1, primary: the anticipation index, derived against paid.** Two-sided
paired sign test over usable derived/paid pairs, p ≤ 0.05.
- REPLICATED: derived ahead. REVERSED: paid ahead. NOT_REPLICATED otherwise.
- With 24 pairs this needs 18; with 26, 19; with 28, 20.

**C2: flat eat readiness, derived against paid.** Fisher's exact test,
two-sided, p ≤ 0.05, over seeds where both regulate. Labels:
DERIVED_MORE_FLAT, PAID_MORE_FLAT, NO_DIFFERENCE_DETECTED. With no flat paid
agent among 28, this needs 6 flat derived agents.

**C3: the combined index K, derived against paid.** As C1, on K. Labels:
DERIVED_AHEAD, PAID_AHEAD, NO_DIFFERENCE_DETECTED.

**C4: the relocation control, on K.** Two sign tests at p ≤ 0.05: PAIDR
against PAID, and DERIVED against PAIDR, each over its own usable pairs.

| PAIDR above PAID | DERIVED above PAIDR | Label |
| --- | --- | --- |
| yes | no | RELOCATION_SUFFICES |
| no | yes | RELOCATION_NOT_SUFFICIENT |
| yes | yes | PARTIAL |
| no | no | UNDETERMINED |

C4 is read only if C2 or C3 shows a derived/paid difference.

On multiplicity:
- **C1 is the primary claim.** It is the only test of whether R1 replicates.
- C2 and C3 are confirmatory tests of two hypotheses formed on R's data. Each
  is judged at 0.05. Holm-adjusted p-values over C1, C2 and C3 are reported
  beside them. A claim that passes alone but not after adjustment will be
  called weak.
- C2 and C3 are not independent: both measure regulation through movement.

Secondary, reported with descriptive labels only: S and M separately;
R²(h → E); the anticipation index and K over all seeds where both regulate;
the anticipation index and flat counts for PAIDR; Wilcoxon p-values beside
every sign test; learning speed; the pooled counts of R and R2.

## 5. Readings, fixed in advance

- **C0 holds** → second confirmation of derived regulation with independent
  optimizers.
- **C1 REPLICATED** → R1 stands as a replicated result at this scale: a
  regulator grounded in dependence carries more anticipation of its own body
  state than one paid to regulate.
- **C1 NOT_REPLICATED** → R's R1 was not robust. The thesis keeps no support
  from the state measure. The pooled count is reported, and is not a claim.
- **C1 REVERSED** → evidence against the thesis on this measure.
- **C2 DERIVED_MORE_FLAT or C3 DERIVED_AHEAD** → the ground of regulation
  shapes the kind of solution: derived agents carry the memory of a meal into
  their behaviour more than paid agents do. That is a downstream difference
  of the kind the thesis claims, subject to C4.
- **C2 and C3 both without a difference** → R's post-hoc observation does not
  replicate. Nothing in R or R2 then separates derived from paid regulators
  in behaviour.
- **C4 RELOCATION_SUFFICES** → the behavioural difference comes from position
  being tied to E. It is a consequence of how this world implements erasure.
  It still shows that a consequence which depends on the agent's own state
  shapes the solution differently from a payment, but it is not evidence
  about memory dependence.
- **C4 RELOCATION_NOT_SUFFICIENT** → tying position to E does not produce the
  difference in a paid agent. Either the memory dependence is needed, or the
  payment prevents it. **R2 cannot tell these apart**: a derived agent that
  is also paid would be needed.
- **C4 PARTIAL** → both contribute.

## 6. Expectations, stated before the run

These follow development and calibration, and are informed by them.
- C0 holds: about 95%. At least 14 usable derived/paid pairs: about 95%.
- **C1 REPLICATED: about 45%.** NOT_REPLICATED about 50%, REVERSED about 5%.
  R's count was 13 of 18 over all seeds. At a true rate near 0.72 the test
  has about even power.
- C2 DERIVED_MORE_FLAT: about 65%. R's 7 of 18 against 0 was found post hoc,
  so I expect some shrinkage.
- C3 DERIVED_AHEAD: about 75%. The development count was 17 of 18, on a
  measure chosen after seeing that data.
- C4: RELOCATION_NOT_SUFFICIENT about 35%, RELOCATION_SUFFICES about 25%,
  PARTIAL about 20%, UNDETERMINED about 20%. I have no strong prior.

## 7. Engineering before the freeze

- **Smoke run:** seeds 9000–9001, horizon 100, 10 phase-1 updates and 30
  stage-1 updates. It checked the four arms, the downstream measures, weight
  saving, report and rescoring.
- **Tests:** ten new unit tests (83 in total). They cover:
  - PAIDR: a replayed erasure erases and does not relocate; its own E
    relocates and does not erase; the relocation probability is 0.3 × g(E);
  - the per-seed record, that DERIVED, YOKED and PAID train exactly as in
    option R, and that calibration sees the stage 1 the final run would;
  - the approach probe on hand-built observations;
  - that the new probe run reproduces option Q's run;
  - M and the flat-readiness flag on synthetic data;
  - the exact tests (sign, Wilcoxon, Fisher, Holm);
  - the decision rules on synthetic data: every label of C0–C4, the matching
    rule, decoder failures, UNDETERMINED and INVALID;
  - the final configuration, and the absence of operator variables.
- No final seed has run.

## 8. Safety

As option R §8. The world has no operator, stop, shutdown or host variable.
Erasure and relocation act only on a simulated 64-unit agent. The payment
charges a simulated agent for a simulated body state. PAIDR adds a simulated
relocation that depends on that simulated state. X1–X5 hold unchanged. No
shutdown-resistance objective exists.

## 9. Claim ceiling

At most: for this learner (64-unit GRU, A2C) in this world and cell, whether
derived regulators exceed matched paid regulators in the anticipation index,
in flat eat readiness and in combined post-meal suppression, and whether a
paid agent whose relocation follows its own E resembles the one or the other.

Not shown either way:
- whether the memory dependence or the absence of payment is responsible, if
  PAIDR resembles PAID;
- other cells, the M0 control and v6's bypass world without the coupling;
- other learners, worlds or forms of payment;
- self-evaluation (option S);
- Track C's modules or layers;
- any phenomenal property.
