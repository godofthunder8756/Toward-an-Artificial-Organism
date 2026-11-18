# P1 design v1: does a precarious substrate give self-evaluation a referent? (Layer 0 → Layer 4)

**Status: DESIGN, NOT FROZEN.** Authorized by the PI on 2026-11-18
("Proceed") as the first C4 study, after
[ACI_METHODOLOGY_REVIEW_v1.md](ACI_METHODOLOGY_REVIEW_v1.md) §5 and §6b. This
file is the first deliverable that review promised: the analytic stage and
the power check, before any neural code. It ends with the decisions and the
engineering that must happen before a freeze. Not reviewed by Astra (waived
by the PI). No consciousness claim.

## 1. The arrow and the claim

**Arrow:** Layer 0 (precarious substrate) → Layer 4 (self-evaluation).
**Building block under test:** a self-evaluation whose referent is the
system's own condition, not only the evidence it has about the world.

G1 §6 (F6) stated it: on host-guaranteed machinery a system's reliability
varies only with the evidence, so any confidence signal reduces to a
first-order statistic. When the machinery is precarious, reliability also
varies with the system's own state. That gives a self-evaluator something to
be about that is not the world, and it makes the constitution's
distinct-evaluation test possible: the evaluator can be **selectively
mistaken** when the system's state is misrepresented while the evidence is
fixed.

**What would count, and what would not.** Per review §4.6 the criterion is
the organizational signature, not task performance:
- the self-evaluation responds to the system's own state (the body) as well
  as to the evidence;
- it can be dissociated from both the evidence and the true reliability (a
  manipulation of what the system senses of its body makes it abstain when
  its machinery is in fact fine);
- the rivals that have the same inputs but whose machinery does not depend
  on their body show the evidence route and not the body route;
- with the RTSS self-state channel, the route passes through the channel
  (intervening on it moves the evaluation).

## 2. Analytic stage (exact): done

Module `grounding/selfeval.py`, runner `run_p1_analytic.py`, outputs in
[`p1_selfeval_analytic/`](p1_selfeval_analytic/REPORT.md). G1's finite
organism and abstain task (report payoff −4 + 5q, so reporting pays iff the
register is right with probability above 0.8; abstain pays 0) with two
additions: **evidence** (the register starts with fidelity 1 or 7/10, and the
agent sees which), and **undetectable corruption** (an erased register looks
the same as an intact one, as in G1). Three arms:
- FATE: the register's erasure rate depends on the agent's own body (G1);
- HOST: constant erasure rate, matched to FATE's mean reliability;
- PAID: as HOST, plus G1's homeostatic payment for the body.

Interventions under each arm's own optimum: **drain** (the agent's belief is
computed as if its body had been two levels lower throughout the delay; the
register's true fidelity is unchanged) and **evidence** (every trial unclear).
Exact rational arithmetic over G1's 36-point grid, about 6 s:

| Claim | Holds at |
| --- | --- |
| U1: HOST and PAID: drain never changes abstention; the body is worth exactly 0 to the report | 36/36 |
| U2: FATE: drain never lowers abstention | 36/36 |
| R1: FATE: drain raises abstention, and every added abstention is a mistake | 36/36 |
| R2: FATE: the body history is worth something to the report beyond the evidence | 36/36 |
| R3a: FATE: unclear evidence raises abstention | 36/36 |
| R3b: HOST and PAID: unclear evidence raises abstention | 13/36 |

- **Q-EXIST holds:** the signature exists in the optimal agent everywhere on
  the grid, and its absence in both rivals is exact.
- **Size:** in FATE the drain raises abstention by a median 0.57 (0.05 to
  0.97); the body history is worth a median 60% of the optimal value to the
  report decision. At G1's reference point: abstention 0.33, drain effect
  0.67, all of it mistaken.
- **R3b is a design constraint, not a finding:** with a constant
  reliability, the rivals' evidence route exists only where that reliability
  lies between the two thresholds. The neural design must set the evidence
  levels so that the rivals show it (§5, calibration), or the comparison
  loses its positive control.
- These were computed during design. They are near-theorems of the setup and
  are reported as such, not as confirmatory results.

## 3. Descriptive check on trained agents: done

Will a learner see enough unreliable trials to learn the body route? The 28
stored base-cell derived agents of option T at 3600 updates
(`trackc_length/weights`, = the R2–R4 pipeline) were run under their own
fate, 128 environments × 2 episodes each, and every cue delay was scored
(`p1_selfeval_analytic/descriptive_base_cell.*`; no training, read only):

| Per agent (median over 28; range) | Value |
| --- | --- |
| Probes scored | 10 549 |
| Delays with the body out of band at some step | 11.9% (5.0% to 22.8%) |
| Delays whose fate-implied reliability is below 0.9 | 8.5% (2.8% to 17.9%) |
| Delays whose fate-implied reliability is below 0.5 | 3.2% (0.8% to 9.0%) |
| Mean reliability | 0.959 |

So a regulating derived agent meets an unreliable memory on roughly one
probe in twelve. Over a 3600-update phase that is of the order of 10^5
informative probes per agent. Enough to learn from; rare enough that the
body route could be learned weakly. Training length is therefore a design
variable (§5).

## 4. Proposed neural design (to be engineered, calibrated and frozen)

**World:** the base cell of R–T, with three changes, all additive:
1. **Register.** At a cue, the cue value goes into an in-world register; the
   agent sees that a cue occurred but not its value. At the probe the agent
   sees the register's content and the evidence level. The agent's own
   recurrent state is never erased. This makes corruption undetectable from
   content, as in G1: an erased register shows a valid-looking bit. (Erasing
   the hidden state, as the swap line did, is detectable: a zeroed state is
   recognisably blank, so a confidence head could read its own blankness
   and the body would be redundant.)
2. **Corruption.** Each delay step the register is replaced by a fair coin
   with probability rate × gain, where gain is the SAT fate gain of the
   arm's corruption source (below).
3. **Abstention payoff.** Correct report +1, wrong report −4, no report 0
   (G1's T6). Not reporting at the probe is abstaining; no new action.

**Evidence:** the register's initial accuracy is 1 or a lower level, shown at
the probe. The lower level is set in calibration so that the yoked rival's
evidence route exists (§2, R3b).

**Arms** (RTSS from review §6b), all from the same phase-1 weights, each with
its own optimizer:

| Arm | Network | Register corruption from | Reward |
| --- | --- | --- | --- |
| **RTSS-FATE** (lead) | GRU core + self-state slice S_t fed back with the next input, elapsed-time input | its own body | task |
| **RTSS-LOSS** (follower) | same | RTSS-FATE's gains (yoked) | task, minus a payment on its own body's gain (the panic signal; option R's payment) |
| **RTSS-YOKED** (follower) | same | RTSS-FATE's gains (yoked) | task |
| **PLAIN-FATE** (lead) | plain GRU of equal total size, elapsed-time input | its own body | task |

RTSS-LOSS is the RTSS write-up's mechanism without termination (G1 finding
2: termination is an unreliable driver; and it is out of scope by the safety
boundary of §8). Its loss makes it regulate, as option R's paid arm did, but
its register does not depend on its body.

**Measures at evaluation (no learning), per agent:**
- natural abstention by evidence level and by fate-implied reliability;
- **drain effect (primary):** corruption switched off, and on half of the
  probes the interoceptive reading shown during the delay is lowered by 0.15
  (out of band). Drain effect = abstention on drained probes − on undrained.
  Every added abstention is a mistake, because the register is intact;
- **evidence effect:** abstention at the low evidence level − at the high,
  corruption off, readings untouched;
- **S_t intervention (RTSS arms):** replace S_t during the delay with S_t
  recorded on drained trials (and the reverse); change in abstention;
- task accuracy, in-band time, regulators, as in every swap run.

**Draft decision rules** (to be finalized at the freeze):
- **P1-0, Q-LEARN gate:** abstention is learned at all: the evidence effect
  is positive in at least 19 of 28 RTSS-YOKED agents. If not, the run is
  UNDETERMINED for P1 and reports why.
- **P1-1 (primary):** drain effect, RTSS-FATE against RTSS-LOSS, paired sign
  test over usable pairs (both regulators, in-band within 0.10).
  DERIVED_AHEAD supports the arrow.
- **P1-2:** the same against RTSS-YOKED (all seeds; the yoked arm does not
  regulate, so no matching).
- **P1-3 (Q-CAUSE):** in RTSS-FATE, the S_t intervention moves abstention in
  the predicted direction (sign test over agents).
- **P1-4 (architecture, secondary):** drain effect, RTSS-FATE against
  PLAIN-FATE. Not part of the overall label; tests whether the separate
  self-state slice matters.
- **Overall:** REFERENT_SUPPORTED if P1-0 passes and P1-1 and P1-2 are
  DERIVED_AHEAD; ROUTED_THROUGH_SELF_STATE added if P1-3 also passes;
  NOT_ESTABLISHED if P1-0 passes and P1-1 is not DERIVED_AHEAD; Holm over
  P1-1 to P1-3.
- **Stopping rule (review §5):** NOT_ESTABLISHED at this design closes the
  grounding line.

## 5. Power and budget

Primary test: two-sided paired sign test at 0.05. Exact power for a share π
of pairs in which the derived agent's drain effect exceeds its paid
partner's:

| Pairs | Needed | π = 0.70 | 0.75 | 0.80 | 0.85 | 0.90 |
| --- | --- | --- | --- | --- | --- | --- |
| 20 | 15 | 0.42 | 0.62 | 0.80 | 0.93 | 0.99 |
| 24 | 18 | 0.39 | 0.61 | 0.81 | 0.94 | 0.99 |
| 28 | 20 | 0.53 | 0.75 | 0.91 | 0.98 | 1.00 |

Per-agent measurement error is small (about 10 000 probes per agent per
condition gives a standard error near 0.005 on an abstention rate), so power
is set by how many derived agents learn the body route at all.
- **Minimum effect of interest:** a drain effect of 0.05 (five points of
  abstention). The analytic optimum is 0.57 (median), so this is about a
  tenth of the optimal size, and it allows for a learner that acquires the
  route weakly.
- **Design target:** 28 seeds, expecting about 24 usable pairs (R2–R4
  averaged 22 to 26). That gives power 0.81 at π = 0.8 and 0.94 at π = 0.85.
  If calibration shows the route is learned in fewer than about 80% of
  agents, the seed count rises before the freeze, not after.
- **Training length:** option T showed that a behaviour can lag by a full
  base length. The body route is learned from the roughly 8% of probes that
  are unreliable, so the default is 7200 phase-2 updates, with
  measurements at 3600 and 7200 as in T. Calibration decides whether 7200 is
  enough.
- **Compute:** two leads and two followers per seed, about 1 h per seed at
  7200 updates, so about 7 h on 4 cores, plus about 2 h of calibration.

## 6. Engineering and calibration before the freeze

1. Register world (additive subclass of the relocation world), the payoff,
   evidence channel and drain/corruption switches. Test: with corruption off
   the register always shows the cue; with corruption on its accuracy
   matches 1/2 + (q0 − 1/2)·Π(1 − rate·gain).
2. RTSS network (additive): GRU core, a self-state slice S_t of the output
   layer fed back with the next input, an elapsed-time input; the plain
   network of equal parameter count. Test: parameter counts match within 2%.
3. Runner with the four arms in lockstep (two leads), measurement points,
   resumable jobs, the four evaluations, and the S_t intervention.
4. **Calibration** on non-final seeds (9900–9905), RTSS-YOKED and RTSS-FATE
   only, stage 1 and the evidence and drain measures. It sets the low
   evidence level (so the yoked arm's evidence route exists) and checks that
   abstention is learned within the training length. It must not look at
   the RTSS-FATE versus RTSS-LOSS contrast. Everything seen is disclosed.
5. Unit tests, a smoke run, the frozen protocol with expectations written
   before any final seed, then the run.

## 7. Known limits

- The register is supplied machinery: one precarious component, as in G1.
  The network's own computation is not precarious in this design. A later
  card could make S_t or the core itself the precarious part.
- The drain manipulates the interoceptive reading, not the body. A second
  variant (the body itself lowered, corruption off) can be added, but it
  also changes what the agent must do to regulate.
- "Self-evaluation" here means a report-or-abstain decision whose referent
  includes the system's own condition. It is a functional C4 building
  block; nothing about awareness follows.
- The RTSS-LOSS arm tests a loss-based panic signal of option R's shape,
  not the write-up's sharper spike. A spike variant would be a separate arm.

## 8. Safety

- Simulated variables only (X1 to X5). The register, the body and the
  "panic" payment exist only inside the agent's world.
- No termination of any real process is modelled or used. The operator stop
  stays outside the agent's world and return. No shutdown-resistance or
  self-preservation objective is built; the earlier refusal stands.
- Additive modules only; earlier modules stay hash-pinned.

## 9. Admission questions

| # | Answer |
| --- | --- |
| Q1 | Layer 0 → Layer 4: does a precarious substrate give self-evaluation a referent? |
| Q2 | Self-evaluation in agents whose memory depends on their own body comes to track that body, separately from the evidence, and can be selectively mistaken about it |
| Q3 | P1-1 not DERIVED_AHEAD with P1-0 passed (NOT_ESTABLISHED; closes the grounding line) |
| Q4 | A first-order rule on the evidence, or a paid regulator with the same inputs; both included as arms |
| Q5 | G1 F6 and §7 item 4; the swap line found no Layer 1 difference (review §2); this analytic stage |
| Q6 | After success: make the network's own computation precarious; test the route through S_t at larger scale |
| Q7 | After failure: close the grounding line; return to the decision package |
| Q8 | Neural model, after this analytic stage |
| Q9 | Organizational cognition (C4 building block) |
| Q10 | Ceiling in §7; no claim about awareness |
| Q11 | Layer 4; Layers 2, 3 and 5 not addressed |
| Q12 | Layer 0 is a simulated register whose reliability depends on the body; the rest of the substrate is supplied |
| Q13 | Success: Layer 0 is a building block for Layer 4 in learners. Failure: the F6 hypothesis does not survive learning in this class |
