# P3c protocol: confirmation and cause of the differentiated body readout (Layer 3 → Layer 4)

**Status: FROZEN.** Frozen at the commit labelled "Freeze P3c" (the commit
is the freeze), before any final seed and before stage 0 were run.

- **What it is:** the follow-up recommended in
  [P3B_DIFF_RESULTS.md](P3B_DIFF_RESULTS.md) §8.
- **Authorization:** the PI, on 2026-11-23 ("Proceed with the recommended
  path").
- Not reviewed by Astra (waived by the PI). No consciousness claim.

**Files:**

- Code: `trackc_swap/steerdiff.py` (direction estimation and steering) and
  `run_p3c_steer.py` (runner, decision rules, report). Training is P3b's
  frozen `trackc_swap/differentiate.run_seed_x`, called unchanged.
- Tests: `test_p3c_steer.py`.
- Calibration: `p3c_steer_calibration/`. Stage 0: `p3c_steer_stage0/`.
  Run: `p3c_steer/`.

## 1. What is being tested

P3b gave two decisions risks on opposite sides of one body variable:

- A (memory) is at risk when the body is low;
- C (perception) is at risk when the body is high.

Its label was UNDETERMINED, because the pre-registered perception referent
("the body looks high, so abstain on C") did not form. Descriptively, the
two decisions read the body with **opposite signs**:

- when the body looks low, A abstains more (25/27 against the yoked rival);
- C abstains *less*, a release of caution (7/27 for the yoked rival,
  p 0.019; about 85% of C's half of the differentiation index).

P3c asks two questions.

1. **Confirmation (behaviour).** On 28 new seeds, with P3b's training
   unchanged, does the opposite-sign readout replicate? The memory referent
   is the precondition; the C release, now pre-registered in the form the
   data showed, is the confirmatory test.
2. **Cause (state).** Is each readout carried by a direction of the agent's
   recurrent state that causally moves its own decision? And do the two
   decisions share **one body direction read with opposite signs**
   (content in the readout) or use **separate directions** (content in the
   state)?

The second question is the Layer 4 signature P3b could not reach: a
self-state whose content (which processing is at risk) is carried by the
agent's state and changes behaviour when that state is moved.

## 2. Design as built

**Training (unchanged from P3b):**

- `run_seed_x` from `trackc_swap/differentiate.py` at the P3b freeze
  (195bd64);
- the same world, precarities, arms (PFATE, PYOKED, PNOFATE), phase 1,
  phase 2 (3600 updates), points (1800 and 3600, primary 3600) and P3b's
  evaluation.

A test checks that the P3c job returns exactly P3b's records and weights,
plus a steering block.

**Steering (new; evaluation only).** It runs on fresh copies of the saved
weights in evaluation worlds (tag 110), with both precarities off. Each run
is 4 episodes of 128 environments, types A and C.

- **Directions.** For each probe kind there are two collection runs, with
  the look probe on a random half of the trials. In each run:
  - take the mean GRU state h over the steps of clear live trials of one
    type (cue to probe);
  - subtract the unprobed mean from the probed mean.

  The direction is the mean of the two runs, and their cosine is the
  split-half reliability.

  | Direction | Probe | Trials | Meaning |
  | --- | --- | --- | --- |
  | u_A | look_low | A | A's own risk side |
  | u_C | look_low | C | the side on which C released caution in P3b |
  | v_C | look_high | C | C's own risk side (P3b's pre-registered C referent) |
  | v_A | look_high | A | descriptive only |

- **Steering** (P1b's machinery, as in P1d and P3).
  - Mixed A/C episodes, no probe.
  - h is shifted by *scale* × direction at every step of the delay (cue to
    probe, inclusive) of a random half of the trials of both types.
  - The effect per type is the abstention on steered clear trials minus
    unsteered clear trials.
- **Directional effect.** Every direction is applied with both signs:
  Δ_t(d) = effect_t(+d) − effect_t(−d).
  - P3 found post-hoc that the fated agent abstains when its state is moved
    in **any** direction, which made P3's steer-vs-random contrast fragile.
  - That sensitivity is symmetric in the sign and cancels in Δ.
  - As a control, a random direction of the same norm as u_A, and one with
    the norm of u_C, are applied with both signs.
- **Scale:** STEER_SCALE = **SCALE_TBD** (calibration, §3).

**Stage 0 (declared; not the confirmation).**

- The frozen steering is applied, after the freeze and before the final
  seeds, to P3b's final nets (seeds 2400–2427, point 3600, P3b's usability
  rule).
- It answers the causal question early on the nets in which the pattern was
  found.
- It is reported separately and does not set the label.

## 3. Calibration (disclosed)

CALIBRATION_TBD

## 4. Measures (per usable seed, per arm, at each point)

**Behaviour (P3b's measures, P3b's code).** Each look cell is the change in
abstention on clear, probed trials against unprobed ones: A_low, A_high,
C_low and C_high. P3b's D, halves, S, G and natural discrimination are
reported as secondary.

- **C_release** = −C_low: positive when C abstains less when the body
  looks low.

**Steering.** Each measure below is a directional effect Δ, signed so that
the expected direction is positive.

| Measure | Definition | Meaning if positive |
| --- | --- | --- |
| S_A | Δ_A(u_A) | A's low-body direction makes A abstain |
| S_C | −Δ_C(u_C) | C's low-body direction releases C |
| X_AC | −Δ_C(u_A) | C reads A's direction as release (shared direction, opposite readout) |
| X_CA | Δ_A(u_C) | A reads C's direction as danger (shared direction, opposite readout) |
| V_C | Δ_C(v_C) | C's high-body direction makes C abstain |
| R_A, R_C | Δ along the random directions | control (expected about 0) |
| P_A, P_C | mean of the + and − random effects | sensitivity to any displacement (P3's post-hoc finding) |
| cos(u_A, u_C) | cosine of the two low-body directions | descriptive geometry; split-half reliabilities as its ceiling |

## 5. Decision rules (exactly as in `run_p3c_steer.py`)

Two-sided sign tests over seeds, α = 0.05. A test with fewer than 14
non-zero seeds is UNDETERMINED.

**Usability and validity:** P3b's rules, unchanged.

- **Usable:** phase 1 learned A and C.
- **Valid:** phase-1 clear correct ≥ 0.8 for A and C; overwrite-probe
  accuracy for A ≤ 0.7; PFATE exposure ≥ 0.02 for A and C.

**Gate (primary point):** P3b's gate (yoked A and C evidence positive in
≥ 2/3 of seeds; retention ≥ 0.6 in every arm).

**Primary tests at the primary point (Holm over the four):**

| Test | Measure | Pass label |
| --- | --- | --- |
| P3C-B1 | A_low, PFATE vs PYOKED (paired) — the memory referent; precondition | DERIVED_AHEAD |
| P3C-B2 | C_release, PFATE vs PYOKED (paired) — the opposite-sign readout on C | DERIVED_AHEAD |
| P3C-SA | S_A in PFATE (one-sample) | CAUSAL |
| P3C-SC | S_C in PFATE (one-sample) | CAUSAL |

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | validity fails |
| UNDETERMINED | fewer than 14 usable seeds, the gate fails, P3C-B1 is not DERIVED_AHEAD, or P3C-B2 is UNDETERMINED |
| CONFIRMED_CAUSAL | P3C-B2 DERIVED_AHEAD, and P3C-SA and P3C-SC both CAUSAL |
| CONFIRMED_BEHAVIOURAL | P3C-B2 DERIVED_AHEAD, but not both steering tests CAUSAL |
| NOT_CONFIRMED | P3C-B2 is NO_DIFFERENCE_DETECTED or YOKED_AHEAD |

- **Weak:** set when a test the label needs has Holm-adjusted p > 0.05.
  - CONFIRMED_CAUSAL needs all four.
  - CONFIRMED_BEHAVIOURAL needs B1 and B2.

**Structure reading** (pre-registered; it does not change the label).
It applies when P3C-SA and P3C-SC are both CAUSAL, and uses X_AC and X_CA
in PFATE (one-sample).

| Reading | Rule | Meaning |
| --- | --- | --- |
| **ONE_DIRECTION_TWO_READOUTS** | both CAUSAL | One body state; each decision reads it with the sign of its own risk. The content is in the readout |
| **SEPARATE_DIRECTIONS** | neither CAUSAL nor REVERSED_CAUSAL | Each decision's body warning has its own direction in the state. The content is in the state |
| **PARTLY_SHARED** | otherwise | Including a reversed cross effect (a mood-like coupling of the directions) |

Otherwise the reading is NOT_APPLICABLE.

**Secondary (reported, not decisive):**

- **Per-arm routes:** S_A, S_C, X_AC, X_CA and V_C in each arm.
- **Against the yoked rival:** S_A and S_C, PFATE vs PYOKED.
- **Against random:** S_A vs R_A and S_C vs −R_C in PFATE.
- **Controls:** R_A and R_C in PFATE (expected NOT_DETECTED).
- **Perturbation sensitivity:** P_A and P_C, PFATE vs PYOKED (a replication
  test of P3's post-hoc finding).
- **Geometry:** cos(u_A, u_C), PFATE vs PYOKED.
- **P3b's labels and measures** on the new seeds.
- **The same tests at 1800.**

**Stage 0:** SA, SC, the cross tests and the structure reading on P3b's
usable nets at 3600. It is reported as stage 0 only.

## 6. Readings

| Outcome | What it would mean |
| --- | --- |
| CONFIRMED_CAUSAL, ONE_DIRECTION_TWO_READOUTS | The body-grounded self-state is one state, but each decision reads it with the sign of its own risk, and moving the state moves both decisions in opposite directions. The content ("which processing is at risk") is in how each consumer reads a shared state: a broadcast state with consumer-specific meaning |
| CONFIRMED_CAUSAL, SEPARATE_DIRECTIONS | Each decision has its own body-warning direction in the agent's state. Content-specific self-states in the representation itself: the closer analogue of a self-model with content |
| CONFIRMED_CAUSAL, PARTLY_SHARED | Both, in part. Or a residual mood-like coupling, if a cross effect is reversed |
| CONFIRMED_BEHAVIOURAL | The opposite-sign readout replicates in behaviour, but its state direction does not move the decision (or not both). The readout may rely on something steering at this scale does not reach |
| NOT_CONFIRMED | P3b's C release does not replicate: the descriptive differentiation was seed-specific |
| UNDETERMINED / INVALID | The design did not get far enough to ask |

## 7. Expectations (written before any final seed and before stage 0)

EXPECTATIONS_TBD

## 8. Engineering record

- **Additive:**
  - `steerdiff.py` imports P3b's `DiffRunner` and `run_seed_x` and modifies
    no earlier module.
  - The state is collected by wrapping the agent's `step` for the duration
    of one evaluation run (restored afterwards; tested).
  - The masks are those of P1b's collection: clear live trials, split by
    type and probe.
- **Tested:**
  - collection counts only clear live trials of each type, and the wrapper
    is restored;
  - a zero steering vector changes no action;
  - steering acts only on live steered environments;
  - the P3c job returns P3b's training records and weights unchanged;
  - the signs of the measures;
  - the labels and the structure reading;
  - safety and seed disjointness.
- **Compute:**
  - Training as P3b (about 35 min per seed on 4 workers), plus steering.
  - The final run takes 7 batches of 4 seeds, at most 3 per invocation
    because of the 2 h background-task limit. Each batch is committed and
    pushed.
  - Stage 0 takes about STAGE0_TBD.

## 9. Limits and claim ceiling

- **As in P3b:**
  - one small GRU;
  - one world;
  - a given drive;
  - the probes change the shown reading only;
  - each decision is trained under its own risk, so differentiation is
    task-optimal.
- **Directions are mean displacements caused by a probe.** Steering along
  them tests whether the displacement is sufficient to move the decision.
  It does not show that the decision uses only that direction (sufficiency,
  not necessity). Q-NECESSITY is not tested.
- **The structure reading depends on the steering scale.** At a larger
  scale a weak cross effect might appear. The scale is fixed by a blind
  rule (§3).
- **Stage 0 is on the nets in which the behavioural pattern was found.**
  Only the steering is new there.
- **"Self-state" and "self-model"** mean functional patterns of abstention
  and of state. Nothing about awareness or experience follows. Layer 6 is
  not addressed.

## 10. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the
  perception corruption, the probes, the steering and the drive exist only
  inside the agent's world and network. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 11. Admission questions

| # | How P3c answers it |
| --- | --- |
| Q-EXIST | The memory referent and the C release in PFATE, on new seeds |
| Q-LEARN | Both against a yoked rival with the same losses |
| Q-CAUSE | Primary: steering along each decision's own low-body direction moves that decision (sign-flipped, so direction-free sensitivity cancels) |
| Q-NECESSITY | Not tested |
