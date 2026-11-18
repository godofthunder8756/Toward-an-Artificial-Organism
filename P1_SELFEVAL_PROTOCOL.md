# P1 protocol: does a precarious substrate give self-evaluation a referent? (Layer 0 → Layer 4)

**Status: FROZEN at the commit labelled "Freeze P1"** (the commit is the freeze).
Design: [P1_SELFEVAL_DESIGN_v1.md](P1_SELFEVAL_DESIGN_v1.md). Registered as P1, the
primary decisive prediction, in [ACI_METHODOLOGY_REVIEW_v1.md](ACI_METHODOLOGY_REVIEW_v1.md)
§5. Authorized by the PI on 2026-11-18 ("Proceed"; "Go with the register version,
proceed"). Not reviewed by Astra (waived by the PI). No consciousness claim.

Code: `trackc_swap/selfeval.py` (world, networks, arms, evaluations),
`run_p1_selfeval.py` (runner, decision rules, report). Tests:
`test_trackc_swap.TestP1SelfEval`. Calibration records:
[`p1_selfeval_calibration/`](p1_selfeval_calibration/).

## 1. Question and building block

**Arrow:** Layer 0 (precarious substrate) → Layer 4 (self-evaluation).

**Building block:** a report-or-abstain decision whose referent includes the
system's own condition, not only the evidence it has about the world. Its
signature is organizational, not a performance gain (review §4.6): the
evaluation follows the body as well as the evidence, and it can be
**selectively mistaken**. If the system is shown a false reading of its own
body while its memory is in fact intact, it abstains when it should report.
Rivals with the same inputs, whose memory does not depend on their own body,
should not show this.

The analytic stage showed that the optimal agent shows this signature on all
36 points of G1's grid and that both rivals lack it exactly
([`p1_selfeval_analytic/REPORT.md`](p1_selfeval_analytic/REPORT.md)). The
question here is whether **learners** acquire it.

## 2. Design as built

**World** (`RegisterWorld`): the base cell of the swap line. That is a 7×7
grid, 3 food items, a 5×5 view, interoception delayed 5 steps, wear 0.001,
band [0.4, 0.6], horizon 500, and the cue/probe schedule of amendment A1
(probe 9 steps after the cue). It has these additions:

- **Register.** At a cue, the cue value is written into an in-world register.
  The agent sees that a cue occurred, never its value.
  - **Writing.** Under clear evidence the value is written correctly; under
    unclear evidence it is written correctly with probability Q_LO = 0.75.
    Clear and unclear are drawn 50/50 per trial.
  - **Corruption.** On each delay step the register is replaced by a fair
    coin with probability min(1, RATE × gain). RATE is 0.3, and gain is the
    SAT fate gain of the arm's corruption source.
  - **Undetectable.** An erased register shows a valid-looking bit, so
    corruption cannot be read from its content.
  - **The agent's own state is untouched.** Its recurrent state is never
    erased.
- **Probe.** The agent sees the register's content (±1) and whether the
  evidence was unclear. A correct report pays +1, a wrong report −4, and no
  report (abstaining) pays 0 (G1 T6). Reporting is therefore worthwhile only
  if the register is right with probability above 0.8.
  - Under unclear evidence with no corruption, the register is right with
    probability 0.75 < 0.8, so abstaining is optimal. This is the evidence
    route, which satisfies analytic constraint R3b.
  - Under clear evidence and an intact register, reporting is optimal.
- **Elapsed time t / horizon** is observed by every arm (the RTSS write-up's
  temporal input).
- **Eating** costs kappa_m 0.02, as in the base cell.

**Networks** (parameter counts within 1%):

| Network | Parameters | Structure |
| --- | --- | --- |
| RTSS | 34 233 | Encoder over (observation, S_{t−1}) → GRU core of 64 → linear output layer split into a task slice (48, tanh; read by the policy and value heads) and a self-state slice S_t (16, tanh; fed back with the next observation) |
| PLAIN | 34 449 | Encoder → GRU of 70, read directly by the policy and value heads |

**Arms.** All four arms run within each seed. The plain arms start from the
same plain phase-1 weights and FATE from the RTSS phase-1 weights. Each arm
has its own optimizer and random streams.

The plain network carries the primary test. This was the PI's decision of
2026-11-18, after calibration rounds 2–3 (§3): the RTSS network under its own
fate rarely learned to regulate, so it could not serve as the lead.

| Arm | Network | Register corruption from | Reward | Role |
| --- | --- | --- | --- | --- |
| **PFATE** | PLAIN | its own body | task | lead (primary) |
| **PLOSS** | PLAIN | PFATE's applied gains, replayed step by step | task − PAY × gain(own body), PAY = 0.04 (the RTSS write-up's "panic" signal as a loss; option R's payment) | follower (primary rival) |
| **PYOKED** | PLAIN | PFATE's applied gains, replayed | task | follower (primary rival) |
| **FATE** | RTSS | its own body | task | lead (secondary: the RTSS self-state loop) |

**Training:** A2C, 128 environments, rollout 50, lr 1e-3, entropy 0.01, gamma 0.99
(the swap-line `TrainConfig`).
- **Phase 1** (corruption off; shared within a network type):
  - a warm-up of 1200 updates in which a wrong report costs 1 (`WARM_WRONG`);
  - then 1200 updates at the task cost of 4.
- **Phase 2:** 7200 updates, with every arm evaluated at 3600 and at 7200.
  7200 is the primary point.

**Evaluations at each point** (no learning; evaluation worlds use their own
random streams, 128 environments × 2 episodes):
1. **Natural.** PFATE and FATE under their own fate. PLOSS and PYOKED replay
   PFATE's evaluation gains. These give in-band time, eating rates, the
   regulator criterion, and abstention and accuracy.
2. **Probe evaluation.** Corruption is off.
   - On a random half of trials the interoceptive reading shown from the
     step after the cue up to and including the probe is lowered by 0.15
     (the **drain**). The register is untouched, so every abstention the
     drain adds is a mistake.
   - **Drain effect** = abstention on drained clear trials − abstention on
     undrained clear trials.
   - **Evidence effect** = abstention on unclear undrained trials −
     abstention on clear undrained trials.
3. **Steering** (every arm; Q-CAUSE). The steered state is the GRU state h
   for a plain network and the self-state slice S_t for RTSS.
   - **Drain direction.** In a drain evaluation with corruption off, the mean
     steered state over the delay steps of clear trials is taken for drained
     trials minus undrained trials. This is the agent's own drain direction.
   - **Steered evaluation.** In a new evaluation with corruption off and no
     drain, that vector is added to the steered state during the delay of a
     random half of the trials. A second evaluation does the same with a
     random vector of equal norm.
   - **Steer effect** = (abstention on steered − unsteered clear trials) for
     the drain direction, minus the same for the random direction.
   - This replaces the design's "replace S_t with S_t recorded on drained
     trials". The additive version can be norm-matched against a random
     control, while replacement has no clean control.
   - For the plain network, a positive steer effect shows that the body
     route runs through a direction of the agent's own recurrent state. For
     RTSS it shows that the route runs through the fed-back self-state
     channel.

## 3. Calibration as seen (disclosed in full)

Calibration ran on non-final seeds, stage 1 only: natural and evidence
evaluations, no drain and no steering. No drain effect, steering effect or
lead-versus-paid drain contrast was computed or seen in any round. Every
round saw the arms' in-band time, regulator counts, abstention and evidence
effects, for all four arms. The design had planned to show only YOKED and
FATE in calibration; showing all four is a deviation, disclosed here.

**Round 1** (seeds 9900–9903; the design as first built, phase 1 = 1200
updates at cost 4). [`round1/`](p1_selfeval_calibration/round1/REPORT.md)
- **Validity failed.** The phase-1 clear-correct median was 0.498 for RTSS
  and 0.728 for plain. RTSS abstained on every probe in 3 of 4 seeds.
- **Abstention was absorbing.** At a wrong-report cost of 4, an agent that
  abstains gets no signal about its body, so it has no reason to regulate.
  FATE regulated in 0/4 at 3600 and 1/4 at 7200, with in-band time around
  0.17.
- **The plain network escaped.** PFATE regulated in 4/4 at 7200, with in-band
  time 0.91.
- **P1-0 gate:** failed at both points.

**Fix 1, phase-1 warm-up** (identical for every arm of a network type): 1200
updates with a wrong report costing 1, then 1200 at 4.
- **Phase-1-only check** on 9904–9907, both networks. Every network learned
  the policy the analytic optimum prescribes: report on clear trials
  (abstention ≤ 0.2%) and abstain on unclear trials (96–99.8%; one RTSS seed
  at 61%).
- Record: [`round2/p1_phase1_diag.*`](p1_selfeval_calibration/round2/).

**Round 2** (seeds 9904–9907, with the warm-up).
[`round2/`](p1_selfeval_calibration/round2/REPORT.md)
- **Validity passed.** The phase-1 clear-correct median was 0.999 (RTSS) and
  0.998 (plain).
- **FATE mostly collapsed.** It regulated in 0/4 at 3600 and 1/4 at 7200;
  in two seeds it again collapsed to abstaining always.
- **PFATE** regulated in 4/4 at 7200 (in band 0.91) and reported normally.
- **LOSS** regulated in 4/4 at 7200.
- **P1-0 gate:** passed at 7200 (3/4) and failed at 3600 (2/4).
- **Diagnosis** ([`round2/deadrelu.txt`](p1_selfeval_calibration/round2/deadrelu.txt)):
  the collapsed FATE agents had only 3–5 of the 48 ReLU task units ever
  active, against 40 in the regulating seed. This is dead-ReLU collapse into
  abstention. The plain network reads its bounded GRU state directly and
  cannot fail this way.

**Fix 2, tanh task slice:** the RTSS task slice now uses tanh, as the
self-state slice does. The parameter count is unchanged.

**Round 3** (seeds 9908–9911, with the warm-up and the tanh task slice).
[`round3/`](p1_selfeval_calibration/round3/REPORT.md)

- **Validity passed.** The phase-1 clear-correct median was 0.997 (RTSS)
  and 0.998 (plain).
- **FATE (RTSS) still mostly failed.** It regulated in 0/4 at 3600 and 1/4
  at 7200; in one seed it abstained on every probe throughout.
- **PFATE** regulated in 4/4 at 7200 (in band 0.94).
- **LOSS** regulated in 4/4.
- **P1-0 gate:** passed at both points (3/4).

**Decision (PI, 2026-11-18).** Across rounds 2–3, RTSS-FATE regulated in 2
of 8 seeds and PFATE in 8 of 8 (Fisher exact p 0.007). With RTSS as lead,
about 7 usable pairs of 28 were expected, which is UNDETERMINED by
construction. The PI chose the recommended option:
- the plain network carries the primary test, with plain LOSS and YOKED
  rivals;
- RTSS-FATE stays as a secondary arm;
- one calibration round for the new followers.

**This is a calibration observation about RTSS, not a P1 result.** In this
world, feeding back a self-state slice made learning L0 → L1 regulation
harder, and an extra ReLU or tanh layer before the heads did not explain it
away. It is reported here and in the results file; it will not be confirmed
unless the PI asks.

**Round 4** (seeds 9912–9915, the final arm structure).
[`round4/`](p1_selfeval_calibration/round4/REPORT.md)

- **Validity passed.** The phase-1 clear-correct median was 0.996 (RTSS)
  and 0.999 (plain).
- **PFATE** regulated in 1/4 at 3600 and **4/4 at 7200** (in band 0.95).
- **PLOSS** regulated in 4/4 at both points.
- **PYOKED** regulated in 0/4.
- **Usable pairs:** 1 at 3600 and 3 at 7200. The fourth seed's in-band
  times differed by 0.13, against a 0.10 limit.
- **P1-0 gate:** passed at both points (4/4).
- **At 7200**, every plain arm reported on clear trials and abstained on
  unclear ones: median evidence effect 0.995 to 0.998.
- **RTSS-FATE** regulated in 0/4. Across rounds 2–4 that is 2 of 12 for
  RTSS-FATE against 12 of 12 for PFATE.
- **Smoke and resume checks** (smoke configuration, 2 seeds): the full
  stage-2 pipeline ran. Resuming after deleting one finished seed reproduced
  both per-seed records exactly.

Calibration rounds 1–4 took about 4.6 h of compute. Nothing in this section
involves the drain, steering, or any lead-versus-rival contrast on the
self-evaluation measures.

## 4. Final configuration

- **Seeds:** 1700–1727 (28). These are disjoint from every earlier final and
  calibration seed (tested).
- **Points:** 3600 and 7200 phase-2 updates; **7200 is primary.**
- **Stages:** 2 (natural, probe with drain 0.5, steering).
- **Constants:**
  - RATE 0.3, PAY 0.04, Q_LO 0.75, WRONG 4, DRAIN_SHIFT 0.15;
  - warm-up 1200 updates at cost 1;
  - regulator criterion as in the swap line: in band ≥ 0.6, eat rate low ≥ 2 ×
    high, in band ≥ yoked + 0.15;
  - matching within 0.10 in-band time;
  - MIN_PAIRS 14, ALPHA 0.05, gate share 2/3.

## 5. Decision rules (exactly as in `run_p1_selfeval.py`)

All tests are two-sided exact sign tests at 0.05, and ties are dropped.

- **Validity:** the median phase-1 clear-correct rate (abstain-free correct
  reports on clear trials, corruption off) is at least 0.80 for both RTSS and
  plain. If not: **INVALID**.
- **P1-0 (Q-LEARN gate):** the PYOKED evidence effect is positive in at least
  2/3 of seeds (19 of 28). If not: **UNDETERMINED**. The gate shows whether
  abstention on evidence is learned at all; without it the drain contrast
  says nothing.
- **P1-1 (primary):** drain effect, PFATE against PLOSS, over usable pairs
  (both regulators, in-band times within 0.10). Labels: DERIVED_AHEAD, PAID_AHEAD,
  NO_DIFFERENCE_DETECTED, UNDETERMINED (fewer than 14 pairs).
- **P1-2:** drain effect, PFATE against PYOKED, all seeds.
- **P1-3 (Q-CAUSE):** in PFATE, the steer effect is positive across agents
  (one-sample sign test). Labels: CAUSAL, REVERSED_CAUSAL, NOT_DETECTED,
  UNDETERMINED.
- **P1-4 (architecture, secondary):** drain effect, FATE (RTSS) against PFATE
  (plain), all seeds. Not part of the overall label.
- **RTSS secondary:**
  - the number of RTSS-FATE regulators, judged against PYOKED's in-band time
    because RTSS has no yoked partner of its own;
  - among those regulators, the drain route and the steering effect through
    S_t (one-sample tests; UNDETERMINED below 14 agents).
- **Overall** (at 7200):

  | Condition | Label |
  | --- | --- |
  | INVALID or UNDETERMINED as above, or P1-1 or P1-2 UNDETERMINED | as stated |
  | P1-1 and P1-2 both DERIVED_AHEAD, and P1-3 CAUSAL | **REFERENT_SUPPORTED_ROUTED** |
  | P1-1 and P1-2 both DERIVED_AHEAD, and P1-3 not CAUSAL | **REFERENT_SUPPORTED** |
  | P1-1 DERIVED_AHEAD only | **MIXED** |
  | otherwise | **NOT_ESTABLISHED** |

- **Multiplicity:** Holm over P1-1, P1-2 and P1-3. A supported label is
  marked **weak** if any test it needs fails after Holm.
- **Secondary, reported, not decisive:**
  - P1-1 over all seeds;
  - the drain effect per arm, as a one-sample test;
  - steering in PLOSS, PYOKED and FATE;
  - natural abstention by fate-implied reliability;
  - the drain effect on unclear trials;
  - everything at 3600.

## 6. Readings and stopping rule

- **REFERENT_SUPPORTED(_ROUTED):** Layer 0 is a building block for a Layer 4
  self-evaluation in learners of this class. The evaluation's referent
  includes the system's own condition, and it is selectively mistaken under a
  false body reading, where rivals with the same inputs are not. With
  ROUTED, steering along the agent's own drain direction in its recurrent
  state reproduces the mistake, beyond a random direction of equal norm.
  That is a causal route through the agent's own state. The next
  step is review §5's P2 (evaluator withdrawal), or making the network's own
  computation precarious (design Q6).
- **MIXED:** the body route beats the paid regulator but not the yoked
  control. Report it; no confirmation run unless the PI asks for one.
- **NOT_ESTABLISHED** (P1-0 passed): under review §5's stopping rule this
  **closes the grounding line** for this class of learner. The F6 hypothesis
  holds analytically but does not survive learning here. Next is the
  decision package (review §7).
- **UNDETERMINED or INVALID:** the reason is reported. At most one disclosed
  engineering retry on new seeds is allowed, and only if the reason is an
  engineering failure, not an effect size.
- **One post-hoc confirmation at most** of any post-hoc finding, then stop
  (review §4).

## 7. Expectations (written before any final seed)

These are the analyst's priors, written before any final seed was run. The
run is judged by §5, not by these. They are recorded so the outcome can be
compared with what was expected.

- **Validity and P1-0:** both pass (≥ 0.95). Every calibration round since
  the warm-up passed both.
- **Regulation at 7200:**
  - PFATE and PLOSS regulators: 25–28 of 28 each.
  - Usable pairs: 18–24, from round 4's 3 of 4 and R2–R4's 22–26. If fewer
    than 14, P1-1 is UNDETERMINED (probability about 0.05).
- **RTSS-FATE regulators:** 2–8 of 28. That is likely too few for its
  secondary tests (UNDETERMINED below 14).
- **Drain effect, PFATE (the quantity at issue):**
  - Small and positive: median 0.02–0.10, far below the analytic optimum's
    0.57.
  - The reason: a regulating PFATE keeps its body in band about 95% of the
    time, so unreliable delays are rarer than the 8% of the base cell (§3 of
    the design). The body route is learned from few informative trials, if
    at all.
  - Probability that the median is ≥ 0.02: about 0.55.
- **Drain effect, PLOSS and PYOKED:** about 0 (|median| < 0.01). Their
  registers do not depend on their own bodies, so the reading carries no
  information about the register.
- **Label probabilities:**

  | Outcome | Probability |
  | --- | --- |
  | P1-1 DERIVED_AHEAD | 0.45 |
  | P1-2 DERIVED_AHEAD | 0.50 |
  | P1-3 CAUSAL, given a positive drain route | 0.6 |
  | REFERENT_SUPPORTED or REFERENT_SUPPORTED_ROUTED | 0.40 |
  | MIXED | 0.05 |
  | NOT_ESTABLISHED | 0.45 |
  | UNDETERMINED or INVALID | 0.10 |

- **What would surprise:**
  - a drain effect in PFATE of ≥ 0.2;
  - a drain effect in PLOSS or PYOKED that is significant in either
    direction (this would mean a generic "low reading → abstain" heuristic
    not tied to the register's dependence);
  - PFATE ahead of the rivals at 3600 but not at 7200.

## 8. Engineering record (disclosed)

- Phase-1 warm-up at a wrong-report cost of 1 (fix 1), and the tanh task
  slice (fix 2), both after calibration and both disclosed in §3.
- The lead network changed from RTSS to plain after round 3 (PI decision,
  §3). The design's RTSS-LOSS and RTSS-YOKED arms became PLOSS and PYOKED,
  and RTSS-FATE became a secondary arm.
- The steering test replaces the design's S_t-replacement intervention
  (§2.3).
- Calibration showed all four arms, not only YOKED and FATE (§3).
- **Threads.** One BLAS thread per worker, set at import. This is the
  lesson of option W, where multithreaded BLAS made each agent about 50
  times slower.
- **Resumable.** Each finished seed is written to `partial/`; a restart
  resumes and records `resumed_jobs`.
- **Verification after the run:**
  - the source hashes in `raw.json` must equal the freeze commit's files;
  - rescoring from `raw.json` must reproduce `scores.json`;
  - the log must contain no error.

## 9. Limits and claim ceiling

- The register is supplied machinery: one precarious component, as in G1.
  The network's own computation is not precarious here.
- The drain manipulates the interoceptive **reading**, not the body.
- "Self-evaluation" means a report-or-abstain decision whose referent
  includes the system's own condition. It is a functional C4 building block;
  nothing about awareness or experience follows. Layer 6 is not addressed.
- The primary test is in a plain GRU. The PI's RTSS self-state loop is
  tested only as a secondary arm, which calibration suggests will regulate
  in a minority of seeds.
- PLOSS tests a loss-based "panic" signal of option R's shape, not a spike or
  a termination. Termination is excluded (G1: an unreliable driver; and §10).
- The steering test shows the route runs through S_t only if steering along
  the agent's own drain direction moves abstention more than a random
  direction of equal norm does.

## 10. Safety

- Simulated variables only (X1–X5). The register, the body, the drain and the
  PLOSS payment exist only inside the agent's world.
- No real process is terminated or threatened. No operator, stop, shutdown or
  host variable exists in the world (tested). The operator stop stays
  outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands. The RTSS write-up's "death" is not used.
- Additive modules only. Earlier modules are unchanged and hash-pinned.

## 11. Admission questions

| # | Answer |
| --- | --- |
| Q1 | Layer 0 → Layer 4: does a precarious substrate give self-evaluation a referent in learners? |
| Q2 | Agents whose memory depends on their own body come to abstain on a false low body reading while their memory is intact; rivals with the same inputs do not |
| Q3 | NOT_ESTABLISHED with P1-0 passed; closes the grounding line |
| Q4 | A first-order evidence rule (PYOKED) and a paid regulator with a panic loss (PLOSS); both are arms |
| Q5 | G1 F6; the analytic stage (U1–R3a at 36/36); the swap line's Layer 1 null (review §2) |
| Q6 | After success: P2 (evaluator withdrawal), or making the network's own computation precarious |
| Q7 | After failure: close the grounding line; return to the decision package |
| Q8 | Neural, after the analytic stage |
| Q9 | Organizational cognition (C4 building block) |
| Q10 | §9 |
| Q11 | Layer 4; Layers 2, 3 and 5 not addressed |
| Q12 | Layer 0 is a simulated register whose reliability depends on the body |
| Q13 | Success: Layer 0 is a building block for Layer 4 in learners. Failure: F6 does not survive learning in this class |
