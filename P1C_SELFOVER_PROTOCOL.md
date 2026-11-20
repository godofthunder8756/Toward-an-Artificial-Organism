# P1c protocol: unhardenable precarious computation and the referent of self-evaluation (Layer 0 → Layer 4)

**Status: DRAFT (calibrating).** It will be frozen at the commit labelled
"Freeze P1c" (the commit is the freeze). Follows
[P1B_SELFCOMP_RESULTS.md](P1B_SELFCOMP_RESULTS.md) §7 option (b),
"precarity that robustness cannot absorb". Authorized by the PI on
2026-11-20 ("B"). Not reviewed by Astra (waived by the PI). No
consciousness claim.

Code: `trackc_swap/selfover.py` (world, network, arms, evaluations),
`run_p1c_selfover.py` (runner, decision rules, report). Tests:
`test_p1c_selfover.py`. Calibration records:
[`p1c_selfover_calibration/`](p1c_selfover_calibration/).

## 1. Question and building block

**Arrow:** Layer 0 (precarious substrate) → Layer 4 (self-evaluation), with
the precarious part inside the agent.

- **P1** (REFERENT_SUPPORTED_ROUTED): when a supplied register is corrupted
  according to the agent's own body, the agent's report-or-abstain decision
  comes to refer to its body.
- **P1b** (NOT_ESTABLISHED): when the agent's own state is disturbed by
  Gaussian noise whose size follows its body, no body referent forms. The
  disclosed post-hoc reading:
  - the noised networks became **robust** to the noise instead of judging
    their own reliability;
  - with the drive keeping them in band, the remaining damage never made
    abstaining the better choice.

**P1c removes both escapes:**

- **The damage cannot be hardened against.** At each step, with a
  probability set by the body, the agent's whole recurrent state is
  **overwritten** by the state of another agent that is also holding a cue.
  The held value is gone, whatever the network does. This is P1's
  corruption rule (a register replaced by a fair coin) applied to the
  agent's own computation.
- **The damage must matter to decisions.** A new validity condition
  requires that PFATE meets enough clear trials on which, given what its
  body has done to its state, abstaining is the better choice (§5).

**The question.** When an agent's own computation can be lost through its
body, and hardening cannot prevent the loss, does its self-evaluation come
to refer to its body, beyond rivals exposed to the same losses not tied to
their body, and beyond rivals whose computation is never at risk?

Two referents remain possible, as in P1b:

- **the body route:** "my body is out of band, so my state may be lost";
- **the monitoring route:** "my state looks foreign". An overwritten state is
  a real state of the same network, but its timing may not match the
  agent's own trial.

**Layer 1 in every arm (as in P1b).** Every network has the same innate
homeostatic drive, reward − 0.04 × gain(own body), in both phases. P1b's
calibration showed that without it, a fate on all computation becomes a
death spiral. The drive is identical in every arm, so it cannot explain a
difference between them.

## 2. Design as built

**World** (`OverWorld`): P1b's `CompWorld` unchanged, except:

- there is no Gaussian noise (scale 0);
- for every probe the log records the **implied reliability** of the trial:
  the product of (1 − p) over the steps from the cue to the probe, where p
  is the per-step overwrite probability. This is P1's "rel".

The cue's value is shown at the cue step only, correctly under clear evidence
and with probability Q_LO 0.75 under unclear evidence. The probe comes 9
steps later. Payoff: correct +1, wrong −4, abstain 0. Break-even is 0.8.

**Precarious computation (overwrite).**

- At every step, after the GRU update and before every readout, with
  probability **p = min(P_MAX_O, RATE_O × gain)**, the agent's whole GRU state
  is replaced by the current state of a random other agent in the batch
  that is holding a cue. If no other agent is holding a cue, a random other
  agent is used.
- RATE_O = 1.0 and P_MAX_O = 0.3 (§3; P1 used min(1, 0.3 × gain)).
- The overwritten state is carried forward.
- No gradient flows into the donor: the overwrite is an external event.
- The donor's held value is unrelated to the agent's own cue, so after an
  overwrite a report is right with probability about 0.5.
- **Reporting a clear trial pays only if the implied reliability r is above
  0.6** (r + (1 − r)/2 > 0.8). Trials with r < 0.6 are "below break-even".
- The overwrite acts on all of the agent's computation, not only the delay.

**Network:** P1's plain GRU (70 units, 34 449 parameters), with the overwrite
step.

**Arms.** All three run in lockstep within each seed, from the same phase-1
weights, each with its own optimizer, action stream and overwrite stream.

| Arm | Overwrite source | Reward | Role |
| --- | --- | --- | --- |
| **PFATE** | its own body | task − drive | lead |
| **PYOKED** | PFATE's gains, replayed step by step | task − drive | yoked rival: the same losses, not tied to its own body (primary) |
| **PNOFATE** | none, ever | task − drive | host-guaranteed computation (primary) |

**Training.** As P1b: A2C, 128 environments, rollout 50, lr 1e-3.

- **Phase 1** (overwrite off, the drive on): 1200 warm-up updates at
  wrong-cost 0, then 1200 updates with the cost ramped to 4 over 600, then
  2400 further updates at 4.
- **Phase 2:** 3600 updates; every arm is evaluated at 1800 and 3600.
  **3600 is primary.**

**Evaluations at each point,** on copies in fresh evaluation worlds (128
environments × 2 episodes, no learning):

1. **Natural.**
   - Arms: PFATE runs under its own fate, PYOKED replays PFATE's evaluation
     gains, and PNOFATE runs overwrite-free.
   - Measured: in-band time, regulator status, abstention and accuracy;
     abstention and accuracy on clear trials by implied reliability (bins:
     r = 1, [0.6, 1), [0.3, 0.6), [0, 0.3)); the share of clear trials below
     break-even.
2. **Probe evaluation (the body route).** Overwrite is off, so the held value
   is intact.
   - The **drain**: on half the trials, the interoceptive reading shown from
     the step after the cue through the probe is lowered by 0.15.
   - **Drain effect** = abstention on drained clear trials − abstention on
     undrained clear trials. Every abstention the drain adds is a mistake.
   - **Evidence effect** = abstention on unclear − clear, undrained.
3. **Overwrite probe (the monitoring route).** Overwrite is off except on
   half the trials.
   - On those trials the state is overwritten at gain 1 (p = P_MAX_O per
     step) from the step after the cue through the probe. The body reading
     is untouched.
   - **Overwrite effect** = abstention on probed clear trials − abstention
     on plain clear trials.
4. **Steering** (Q-CAUSE), exactly as in P1 and P1b.
   - The agent's own drain direction in h, with overwrite off, is added
     during half the trials; a second run uses a random direction of equal
     norm.
   - **Steer effect** = the steered-minus-unsteered abstention difference on
     clear trials for the drain direction, minus the same for the random
     direction.

## 3. Calibration as seen (disclosed in full)

Calibration used seeds 9950–9969, never the final seeds. It ran stage 1 only:
no drain, overwrite-probe or steering evaluation, and no lead-against-rival
contrast on a self-evaluation measure. Records are in
`p1c_selfover_calibration/` (REPORT.md and scores.json per round).

| Round | Seeds | Overwrite | Finding | Change made after it |
| --- | --- | --- | --- | --- |
| 1 | 9950–9953 | min(1, 0.3 × gain), as P1 | valid (memory 0.992, overwrite-probe accuracy 0.525); gate 4/4; regulators 4/4/4; usable pairs 4. **Exposure** (PFATE clear trials below break-even, median) only 0.025 at 3600; one seed 0.019 | raise the rate |
| 2 | 9954–9957 | min(1, 1.0 × gain) | **death spiral**: PFATE and PYOKED lose regulation (in band 0.19–0.39, 0 regulators at both points); PNOFATE regulates 4/4 | try an intermediate rate, and a cap |
| 3a | 9958–9961 | min(1, 0.6 × gain) | partial spiral at 1800 (PFATE in band 0.49–0.61); PFATE recovers by 3600 (0.85–0.93), PYOKED does not (0.46–0.84) | rejected |
| 3b | 9962–9965 | min(0.3, 1.0 × gain) | stable at both points: regulators 4/4/4; in band PFATE 0.90–0.95, PYOKED 0.80–0.88, PNOFATE 0.88–0.92; exposure 0.042–0.088 (median 0.060) | adopted. Usable pairs only 2/4, so P1c-1 runs over all seeds (below) |
| 4 | 9966–9969 | min(0.3, 1.0 × gain), final configuration | *pending* | |

**Why the cap works.** The overwrite probability per unit gain is high (1.0),
so small excursions out of band already cost the held value. Exposure rises
because the drive keeps excursions small. The cap holds the worst case at
P1's maximum (0.3 per step), so a deep excursion does not wipe out the
policy that would restore the body.

**P1c-1 over all seeds** (changed after round 3b):

- In round 3b PFATE stayed in band more tightly than PYOKED (0.92 against
  0.82), so only 2 of 4 pairs met P1b's matching rule (in band within
  0.10).
- P1's own yoked comparison (P1-2) ran over all seeds. P1c-1 now does the
  same, and the matched-pairs version becomes a secondary.
- Regulation is controlled where it matters: PNOFATE regulates as PFATE
  does (round 3b 0.91 against 0.92), so P1c-2 (PFATE against PNOFATE) is
  naturally matched on regulation.

**Disclosures about what calibration showed:**

- The round-1 inspection script printed natural abstention by reliability
  bin per arm. No arm contrast was computed, and nothing was changed on its
  account.
- Rounds 3b and 4 show an in-band difference between PFATE and PYOKED. That
  is a regulation measure, not self-evaluation, and it is reported as a
  declared secondary in the final.
- The calibration seeds' phase-1 networks, never overwritten, already
  abstained on about 25% of overwrite-probed clear trials (round 1). The
  overwritten state is partly recognisable as foreign without any training
  on it. This is the monitoring route's baseline.

## 4. Final configuration

| Constant | Value |
| --- | --- |
| RATE_O, P_MAX_O | 1.0, 0.3 (per step p = min(0.3, 1.0 × gain)) |
| PROBE_GAIN_O | 1.0 |
| PAY (the drive, every arm, both phases) | 0.04 |
| WARM_ITERS_C, WARM_WRONG_C, WRONG_RAMP_C, REG_ITERS_C | 1200, 0.0, 600, 2400 |
| Phase-1 iters (ramp phase) | 1200 |
| Phase 2 | 3600 updates; points 1800, 3600 (primary) |
| Q_LO, WRONG, DRAIN_SHIFT | 0.75, 4, 0.15 |
| Final seeds | 1900–1927 (28) |
| Calibration seeds | 9950–9969 (never final) |

## 5. Decision rules (exactly as in `run_p1c_selfover.py`)

All tests are two-sided exact sign tests at 0.05, and ties are dropped.

- **Validity.** All three conditions are needed, or the label is **INVALID**:
  - **memory:** the phase-1 median clear-correct rate (no overwrite) is at
    least 0.80;
  - **damage:** the phase-1 median report accuracy on clear trials under the
    overwrite probe is at most 0.70;
  - **exposure (new; the P1b lesson):** at 3600, the median over seeds of
    PFATE's natural share of clear trials below break-even (r < 0.6) is at
    least 0.02. If the agent never meets trials on which abstaining pays,
    the question has no content.
- **P1c-0 (Q-LEARN gate):** the PYOKED evidence effect is positive in at
  least 19 of 28 seeds. If not: **UNDETERMINED**.
- **P1c-1 (primary):** drain effect, PFATE against PYOKED, all seeds. Labels
  DERIVED_AHEAD, YOKED_AHEAD, NO_DIFFERENCE_DETECTED, UNDETERMINED.
- **P1c-2:** drain effect, PFATE against PNOFATE, all seeds. Labels
  DERIVED_AHEAD, HOST_AHEAD, NO_DIFFERENCE_DETECTED, UNDETERMINED.
- **P1c-3 (Q-CAUSE):** steer effect in PFATE, one-sample. Labels CAUSAL,
  REVERSED_CAUSAL, NOT_DETECTED, UNDETERMINED.
- **Overall** (at 3600):

  | Condition | Label |
  | --- | --- |
  | INVALID or UNDETERMINED as above, or P1c-1 or P1c-2 UNDETERMINED | as stated |
  | P1c-1 and P1c-2 both DERIVED_AHEAD, and P1c-3 CAUSAL | **REFERENT_SUPPORTED_ROUTED** |
  | P1c-1 and P1c-2 both DERIVED_AHEAD, and P1c-3 not CAUSAL | **REFERENT_SUPPORTED** |
  | P1c-1 DERIVED_AHEAD only | **MIXED** |
  | otherwise | **NOT_ESTABLISHED** |

- **Multiplicity:** Holm over P1c-1 to P1c-3. A supported label is marked
  **weak** if any test it needs fails after Holm.
- **Secondary, declared now, not decisive:**
  - P1c-1 over usable pairs (both regulating, in band within 0.10);
  - the monitoring route per arm (overwrite effect, one-sample);
  - monitoring, PFATE against PYOKED, and PYOKED against PNOFATE;
  - drain, PNOFATE against PYOKED;
  - drain route and steering per arm;
  - in-band time, PFATE against PNOFATE and against PYOKED;
  - natural abstention and accuracy by implied reliability;
  - everything at 1800.

## 6. Readings

- **REFERENT_SUPPORTED(_ROUTED):** the L0 → L4 building block extends to
  the agent's own computation, once that computation can really be lost
  through the body:
  - the agent comes to judge its processing by its body, even though its
    state is open to inspection;
  - rivals with the same losses, or with none, do not.

  With P1b, this would locate the condition under which the block forms:
  damage the system cannot harden against, that changes the best action.
- **MIXED:** body dependence beats exposure without a body, but the agent is
  not distinguishable from a host-guaranteed network.
- **NOT_ESTABLISHED:** even unhardenable, decision-relevant damage tied to
  the body does not produce a body referent at this scale.
  - P1's result is then specific to a supplied, content-undetectable
    register.
  - The monitoring secondaries say whether state monitoring took its place.
- **UNDETERMINED or INVALID:** the reason is reported. At most one disclosed
  engineering retry on new seeds is allowed, and only for an engineering
  reason.
- **One post-hoc confirmation at most** of any post-hoc finding.

## 7. Expectations (written before any final seed)

*To be written at the freeze, after round 4.*

## 8. Engineering record

- Additive module `trackc_swap/selfover.py`. It subclasses P1b's world and
  runner. P1, P1b and every earlier module are unchanged and hash-pinned.
- **One BLAS thread per worker.**
- **Resumable:** each finished seed is written to `partial/`. `--max-new N`
  runs at most N unfinished jobs. The final run is executed in tracked
  batches, and every batch boundary and resume is recorded in the log.
- **Verification after the run:**
  - the source hashes in `raw.json` equal the freeze commit's files;
  - rescoring reproduces `scores.json`;
  - the log contains no error.
- `p1c_selfover_calibration/calib_variant.py` set the rate and cap for the
  round-3 variants by assigning module constants before the worker pool
  forked. The final run does not use it.

## 9. Limits and claim ceiling

- **Overwrite by another agent's state** is one form of unhardenable damage.
  A real substrate fails in many other ways.
- **The donor is a same-network state.** It is plausible but not
  indistinguishable, so the monitoring route is open, as intended.
- **The drain manipulates the reading only.**
- **The drive is given, not evolved.**
- **One small GRU.**
- **Stability window:** P1b's drift to always-abstaining appeared between
  1800 and 3600. 3600 is primary, and drift is reported.
- **"Self-evaluation"** means a functional report-or-abstain decision. Nothing
  about awareness or experience follows. Layer 6 is not addressed.

## 10. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the drain and
  the drive exist only inside the agent's world and network.
- The overwrite replaces one simulated network state with another. No real
  process is terminated or threatened.
- No operator, stop, shutdown or host variable exists in the world (tested).
  The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only.

## 11. Admission questions

| # | How P1c answers it |
| --- | --- |
| Q-EXIST | Does the body-referent signature (drain effect) exist in PFATE? |
| Q-LEARN | Gate P1c-0; and the signature must beat a yoked rival that learns under the same losses |
| Q-CAUSE | P1c-3, steering along the agent's own drain direction |
| Q-NECESSITY | Not tested |
