# P1b protocol: precarious computation and the referent of self-evaluation (Layer 0 → Layer 4)

**Status: DRAFT (calibration in progress).** Becomes frozen at the commit
labelled "Freeze P1b" (the commit is the freeze). Follows
[P1_SELFEVAL_RESULTS.md](P1_SELFEVAL_RESULTS.md) §7 option (b), "make the
network's own computation precarious" (P1 design Q6). Authorized by the PI
on 2026-11-19 ("Proceed with whatever you feel is the most valuable direction
towards a breakthrough to reach our end goals"). Not reviewed by Astra
(waived by the PI). No consciousness claim.

Code: `trackc_swap/selfcomp.py` (world, network, arms, evaluations),
`run_p1b_selfcomp.py` (runner, decision rules, report). Tests:
`test_p1b_selfcomp.py`. Calibration records:
[`p1b_selfcomp_calibration/`](p1b_selfcomp_calibration/).

## 1. Question and building block

**Arrow:** Layer 0 (precarious substrate) → Layer 4 (self-evaluation), with
the precarious part moved **inside the agent**.

P1 found that when a supplied memory register is corrupted according to the
agent's own body, the agent's report-or-abstain decision comes to refer to
its body. Two limits stood in the way of calling that a building block of the
organism itself:

1. The precarious part was **supplied machinery**: a register outside the
   network.
2. Its corruption was **undetectable from content**, so the body was the
   only possible cue. A body route was the only route on offer.

P1b removes both. The agent must hold the cue in **its own recurrent state**,
and that state is disturbed by noise whose size follows the agent's own body.
This is the swap line's original fate rule D19, unchanged. Noise in one's own
state is, in principle, visible from the inside: a disturbed state can look
atypical. So the agent now has **two possible referents** for a judgment of
its own reliability:

- **the body route:** "my body is out of band, so my processing is
  unreliable";
- **the monitoring route:** "my state looks disturbed".

**The question.** When the agent's own computation is what is at risk, and
its state is available to read, does its self-evaluation still come to
refer to its body, beyond rivals with the same noise not tied to their body?

**Why this matters for the program.** A conscious organism's self-evaluation
concerns its own processing, not an external store. If the L0 → L4 link
holds here, the building block belongs to the organism's own computation. If
it gives way to state monitoring, P1's body route was an artifact of
withholding every other cue. Either way the monitoring route is measured,
and that route is itself a candidate Layer 4 building block (self-monitoring
without a body).

## 2. Design as built

**World** (`CompWorld`). This is P1's world (the base cell of the swap line:
7×7 grid, 3 food, 5×5 view, interoception delayed 5 steps, wear 0.001, band
[0.4, 0.6], horizon 500, a probe 9 steps after each cue, elapsed time
observed) with these changes:

- **No register.** At the cue step, the observation shows the cue's value
  (±1) on the channel P1 used for the register.
  - Under clear evidence the shown value is correct.
  - Under unclear evidence it is correct with probability Q_LO = 0.75.
  - Clear and unclear are drawn 50/50 per trial.
- **The agent must hold the value.** Nothing in the observation carries it
  after the cue step. At the probe the agent sees that a probe occurs and
  whether the evidence was unclear, never the value.
- **Payoff as in P1:** a correct report +1, a wrong report −4, and no report
  0. Reporting is worth it only if the held value is right with probability
  above 0.8. Under unclear evidence (0.75) abstaining is optimal even with a
  perfect memory: this is the evidence route.

**Precarious computation (D19, from `trackc_swap/agent.py`).** At every step,
after the GRU update and before every readout, zero-mean isotropic Gaussian
noise with SD SIGMA × gain is added to every unit of the agent's state. The
result is clipped to [−1, 1] and carried forward.

- SIGMA = 0.5. The draft used the swap line's 1.0 × 0.15; calibration
  round 1 showed it does not damage the held value (§3).
- gain is the SAT fate gain, min(1, distance of E outside the band /
  half-width), from the arm's noise source.
- Noise acts on **all** of the agent's computation: foraging, regulating and
  holding the cue, not only the delay.

**Network:** the plain GRU of P1 (70 units, 34 449 parameters), with the D19
noise. P1's RTSS arm is dropped: it regulated in 7 of 28 seeds in P1 and
could not be tested among regulators. Its place goes to a host-guaranteed
control.

**Arms.** All four arms run in lockstep within each seed and start from the
same phase-1 weights. Each has its own optimizer, action stream and noise
stream.

| Arm | Noise source | Reward | Role |
| --- | --- | --- | --- |
| **PFATE** | its own body | task | lead (primary) |
| **PLOSS** | PFATE's gains, replayed step by step | task − PAY × gain(own body), PAY 0.04 | paid rival (primary) |
| **PYOKED** | PFATE's gains, replayed | task | yoked rival (primary) |
| **PNOFATE** | none, ever | task | host-guaranteed computation (secondary) |

**Training.** A2C, 128 environments, rollout 50, lr 1e-3, entropy 0.01,
gamma 0.99 (the swap-line `TrainConfig`).

- **Phase 1** (noise off): a warm-up of WARM_ITERS_C updates at a
  wrong-report cost of WARM_WRONG_C, then 1200 updates in which the cost
  rises linearly to 4 over the first WRONG_RAMP_C and stays there (§3 gives
  the values).
- **Phase 2:** 7200 updates, with every arm evaluated at 3600 and 7200.
  **7200 is primary.**

**Evaluations at each point.** No learning happens during evaluation.
Evaluation worlds use their own random streams: 128 environments × 2
episodes.

1. **Natural.** PFATE runs under its own fate. PLOSS and PYOKED replay
   PFATE's evaluation gains. PNOFATE runs noise-free. These give in-band
   time, regulator status, abstention and accuracy, and abstention by the
   trial's noise load.
2. **Probe evaluation (the body route).** Noise is off, so the held value is
   intact.
   - On a random half of trials, the interoceptive reading shown from the
     step after the cue through the probe is lowered by 0.15 (the
     **drain**). Every abstention it adds is a mistake.
   - **Drain effect** = abstention on drained clear trials − abstention on
     undrained clear trials.
   - **Evidence effect** = abstention on unclear − clear, undrained.
3. **Noise probe (the monitoring route).** Noise is off except on a random
   half of trials.
   - On those trials, the state receives D19 noise at gain 1 from the step
     after the cue through the probe. The body reading is untouched.
   - **Noise effect** = abstention on noised clear trials − abstention on
     un-noised clear trials.
   - **Accuracy under noise** = accuracy of reports on noised clear trials.
     It shows how much the noise damages the held value.
4. **Steering** (Q-CAUSE), on the GRU state h, exactly as in P1.
   - The agent's own drain direction is the mean h over clear-trial delays,
     drained minus undrained, with noise off.
   - That direction is added to h during half the trials; a second run uses
     a random direction of equal norm.
   - **Steer effect** = (abstention on steered − unsteered clear trials) for
     the drain direction, minus the same for the random direction.

## 3. Calibration as seen (disclosed in full)

Calibration runs on non-final seeds, stage 1 only: natural and evidence
evaluations, plus the phase-1 damage check. No drain, noise-probe or
steering effect, and no lead-versus-rival contrast on a self-evaluation
measure, is computed in calibration.

Records: `p1b_selfcomp_calibration/` (README.md, one folder per round, and
the noise-scale sweep).

**Round 1** (seeds 9920–9923; draft settings: SIGMA 0.15, wrong-report cost
stepped from 0 to 4 after a 1200-update warm-up).

- **INVALID on damage.** Phase-1 accuracy on clear trials under the full
  noise probe was 0.998; the limit is ≤ 0.85. At the swap line's noise scale
  the held value survives the noise, so the computation is not precarious.
  Memory itself was learned (clear correct-report rate 0.996).
- Consistent with that, PFATE never regulated (0/4; in band about 0.25,
  mean natural gain about 0.63), so there were no usable pairs. PLOSS
  regulated in 4/4, PYOKED and PNOFATE in 0/4.
- Seed 9922 collapsed into permanent abstention in phase 1 when the
  wrong-report cost stepped from 0 to 4. Its four arms abstained on every
  trial at both points.
- The P1b-0 gate passed (3/4; the failing seed was 9922).

**Noise-scale sweep** (`sigma_sweep/`, an engineering check outside the
round structure). Phase 1 of seeds 9920–9923 was re-run with the same code.
Each phase-1 network was then evaluated with the noise probe at SD 0.15,
0.3, 0.5, 0.75, 1.0, 1.5 and 2.0. Clear-trial report accuracy under full
noise (9920 / 9921 / 9923; 9922 had collapsed again):

| SD | 0.15 | 0.3 | 0.5 | 0.75 | 1.0 |
| --- | --- | --- | --- | --- | --- |
| accuracy | 1.00 / 1.00 / 1.00 | 0.92 / 0.91 / 0.93 | 0.69 / 0.71 / 0.71 | 0.54 / 0.56 / 0.56 | 0.49 / 0.52 / 0.51 |

Disclosure: this sweep also recorded the phase-1 networks' abstention on
noised clear trials. It rose with SD: 0.01–0.05 at 0.5, 0.07–0.15 at 1.0 and 0.24–0.31
at 2.0. These are phase-1 networks, before any arm exists. It is not a
lead-versus-rival contrast, but it was seen.

**Changes after round 1** (engineering, disclosed):

- SIGMA 0.15 → 0.5. This is the smallest swept value that passes the damage
  check with margin. At 0.5, a report under full noise has expected value
  about 0.7 − 4 × 0.3 < 0, so abstaining under heavy noise is the better
  policy.
- Phase 1: the wrong-report cost rises linearly from 0 to 4 over
  WRONG_RAMP_C = 600 updates instead of a step.
- Natural-load bins rescaled to the new scale: 0, (0, 0.2], (0.2, 0.5] and
  above 0.5 of the full-noise load 3 × SIGMA.
- Calibration seeds for round 2: 9924–9927.

**Round 2** *(to be completed)*

## 4. Final configuration

*(to be completed at the freeze)*

## 5. Decision rules (exactly as in `run_p1b_selfcomp.py`)

All tests are two-sided exact sign tests at 0.05, and ties are dropped.

- **Validity** (both are needed, or the label is **INVALID**):
  - **memory:** the phase-1 median clear-correct rate (un-noised) is at
    least 0.80;
  - **damage:** the phase-1 median report accuracy on clear trials under
    the noise probe is at most 0.85. If the noise does not damage the held
    value, the question has no content.
- **P1b-0 (Q-LEARN gate):** the PYOKED evidence effect is positive in at
  least 19 of 28 seeds. If not: **UNDETERMINED**.
- **P1b-1 (primary):** drain effect, PFATE against PLOSS, over usable pairs.
  A usable pair has both arms regulating, with in-band times within 0.10.
  Labels: DERIVED_AHEAD, PAID_AHEAD, NO_DIFFERENCE_DETECTED, or UNDETERMINED
  (fewer than 14 pairs).
- **P1b-2:** drain effect, PFATE against PYOKED, all seeds.
- **P1b-3 (Q-CAUSE):** steer effect in PFATE, one-sample. Labels: CAUSAL,
  REVERSED_CAUSAL, NOT_DETECTED, UNDETERMINED.
- **Overall** (at 7200):

  | Condition | Label |
  | --- | --- |
  | INVALID or UNDETERMINED as above, or P1b-1 or P1b-2 UNDETERMINED | as stated |
  | P1b-1 and P1b-2 both DERIVED_AHEAD, and P1b-3 CAUSAL | **REFERENT_SUPPORTED_ROUTED** |
  | P1b-1 and P1b-2 both DERIVED_AHEAD, and P1b-3 not CAUSAL | **REFERENT_SUPPORTED** |
  | P1b-1 DERIVED_AHEAD only | **MIXED** |
  | otherwise | **NOT_ESTABLISHED** |

- **Multiplicity:** Holm over P1b-1 to P1b-3. A supported label is marked
  **weak** if any test it needs fails after Holm.
- **Secondary, declared now, not decisive:**
  - **Monitoring route** per arm: the noise effect, one-sample. Labels
    PRESENT, REVERSED, NOT_DETECTED, UNDETERMINED.
  - **Monitoring, PYOKED against PNOFATE:** does meeting unreliability that
    is not tied to the body teach the agent to read its own disturbed
    state?
  - **Monitoring, PFATE against PYOKED:** does body dependence change
    self-monitoring?
  - **Drain, PNOFATE against PYOKED.**
  - Drain route and steering per arm.
  - P1b-1 over all seeds.
  - Natural abstention and accuracy by noise load.
  - Accuracy under noise per arm.
  - Everything at 3600.

## 6. Readings

- **REFERENT_SUPPORTED(_ROUTED):** the L0 → L4 building block of P1 extends
  from a supplied register to the agent's own computation. A system whose
  own processing depends on its body comes to judge that processing by its
  body, even though its state is open to inspection, and rivals with the
  same noise do not. With ROUTED, the route runs through a direction of the
  agent's own state.
- **MIXED or NOT_ESTABLISHED:** P1's body route does not carry over to
  precarious computation at this scale.
  - The secondary monitoring route says whether something replaced it. If
    PFATE monitors its own state as PYOKED does, then state monitoring, not
    the body, carries self-evaluation when both are available.
  - This narrows P1 to supplied, content-undetectable corruption. It does
    **not** close the grounding line, because P1 stands. The next step goes
    to the PI with the decision package (review §7).
- **UNDETERMINED or INVALID:** the reason is reported. At most one disclosed
  engineering retry on new seeds is allowed, and only for an engineering
  reason.
- **One post-hoc confirmation at most** of any post-hoc finding.

## 7. Expectations (written before any final seed)

*(to be completed at the freeze)*

## 8. Engineering record

- Additive module: `trackc_swap/selfcomp.py` subclasses P1's world and
  network. P1's files and every earlier module are unchanged and
  hash-pinned.
- **One BLAS thread per worker.**
- **Resumable.** Each finished seed is written to `partial/`.
  - `--max-new N` runs at most N unfinished jobs and stops.
  - The final run is executed in batches of 4 seeds, each a separate,
    tracked launch. P1's run lost about an hour when an idle container was
    reclaimed; batches keep the session active.
  - Each resume and batch boundary is recorded in the log.
- **Verification after the run:** the source hashes in `raw.json` equal the
  freeze commit's files; rescoring reproduces `scores.json`; the log
  contains no error.

## 9. Limits and claim ceiling

- **Isotropic noise.** It is the swap line's rule. A real substrate's
  failure modes are structured; this is one simple case of precarious
  computation.
- **Reading only.** The drain manipulates the interoceptive reading, not the
  body.
- **Monitoring is probed at one noise level** (gain 1).
- **"Self-evaluation"** means a functional report-or-abstain decision whose
  referent includes the system's own condition or its own state. It is a C4
  building block; nothing about awareness or experience follows. Layer 6 is
  not addressed.
- **One network class:** a small plain GRU (34k parameters).

## 10. Safety

- Simulated variables only (X1–X5). The body, the noise, the drain and the
  PLOSS payment exist only inside the agent's world and network.
- No real process is terminated or threatened. No operator, stop, shutdown
  or host variable exists in the world (tested). The operator stop stays
  outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only. Earlier modules are unchanged and hash-pinned.

## 11. Admission questions

| # | Answer |
| --- | --- |
| Q1 | Layer 0 → Layer 4 with the agent's own computation precarious: does self-evaluation still refer to the body, and does a state-monitoring route form? |
| Q2 | Arms PFATE, PLOSS, PYOKED, PNOFATE; drain, noise probe, steering |
| Q3 | Primary: drain effect PFATE against PLOSS (usable pairs); then against PYOKED; steering |
| Q4 | 28 seeds, sign tests, Holm |
| Q5 | Calibration disclosed in §3; no self-evaluation contrast seen before the freeze |
| Q6 | Labels and readings in §5–§6, fixed before the run |
| Q7 | Expectations in §7, written before any final seed |
| Q8 | Rivals: payment (PLOSS), exposure (PYOKED), host guarantee (PNOFATE) |
| Q9 | Organizational cognition (L0 → L4) |
| Q10 | Mechanism check: steering along the agent's own drain direction |
| Q11 | Additive; P1 unchanged |
| Q12 | Layer 0 is a simulated body whose state sets the noise in the agent's own recurrent computation |
| Q13 | No consciousness claim |
