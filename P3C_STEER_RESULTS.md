# P3c results: confirmation and cause of the differentiated body readout (Layer 3 → Layer 4)

- **Protocol:** [P3C_STEER_PROTOCOL.md](P3C_STEER_PROTOCOL.md), frozen at
  commit a3bba7b before stage 0 and before any final seed was run.
- **Run:** [`p3c_steer/`](p3c_steer/) (`raw.json`, `scores.json`,
  `REPORT.md`, `run.log`, weights for every arm at 1800 and 3600), seeds
  2600–2627, run 2026-11-23 14:58–20:50 UTC.
- **Stage 0 (declared; not the confirmation):**
  [`p3c_steer_stage0/`](p3c_steer_stage0/) (`STAGE0_REPORT.md`), the frozen
  steering on P3b's nets, run 2026-11-23 14:39–14:58 UTC.
- **Post-hoc descriptives:** `p3c_steer/posthoc/` (disclosed; written after
  the scored result was known; not confirmatory).
- Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. Outcome

**Overall: CONFIRMED_CAUSAL.** The structure reading is
**ONE_DIRECTION_TWO_READOUTS**. This was not the central expectation
written at the freeze (§4).

- All 28 seeds are usable and the run is valid:
  - phase 1 clear correct: A 0.980, C 0.999;
  - overwrite-probe accuracy on A: 0.536;
  - PFATE clear trials below break-even: A 0.029, C 0.059.
- The gate passes (28/28 on both types).
- No primary test is weak: every Holm p is below 0.05.

Primary tests at 3600 (Holm over the four tests):

| Test | What it asks | Result | Holm p |
| --- | --- | --- | --- |
| P3C-B1 | Memory referent: A_low, PFATE against PYOKED | 26/28 (0.156 against −0.001), **DERIVED_AHEAD** | < 0.0001 |
| P3C-B2 | C release (−C_low), PFATE against PYOKED | 23/28 (0.266 against 0.002), **DERIVED_AHEAD** | 0.0018 |
| P3C-SA | Steering along u_A moves A (more abstention), PFATE | 25/28 (median 0.108), **CAUSAL** | < 0.0001 |
| P3C-SC | Steering along u_C releases C (less abstention), PFATE | 20/28 (median 0.286), **CAUSAL** | 0.036 |

**P3b's own rules, applied to these seeds,** give **DIFFERENTIATED**. This
is the label P3b could not reach.

| P3b measure | Result |
| --- | --- |
| Perception referent C_high against the yoked rival | 23/28 (p 0.0009) |
| D | 27/28, median 0.558 |
| S | 1.72 |
| A half | 25/28 |
| C half | 24/28 |

This is a secondary reading, not P3c's label.

- **Behaviour.** The opposite-sign readout found descriptively in P3b
  replicates on 28 new seeds with P3b's training unchanged:
  - A abstains more when the body looks low;
  - C abstains less.
  - Neither rival shows either effect.
- **Cause.** The probe-induced "body looks low" displacement moves each
  decision when it is added to the agent's state with the sign of the
  probe, rather than as an undirected disturbance. The sign-flip contrast
  cancels the part that is the same for both signs, and random directions
  of the same norm do nothing (R_A, R_C not detected).
- **Structure.** u_A and u_C are nearly the same direction (cosine 0.993).
  Each one moves both decisions, each in its own sign. In P3b I framed the
  Layer 4 signature as distinct, decision-specific directions. **That is
  not what was found.** The agent carries one body direction, and the
  differentiation lies in how each decision reads it (§3).
- **The C half is fragile** (§3.4).
  - SC passes by one seed: 20/28, where 19/28 would have failed.
  - A post-hoc contrast that avoids a leak in the unsteered baseline puts
    it at 19/28 (p 0.087).
  - The A half is robust under every check.

## 2. The steering measures

PFATE medians. The two rivals are about zero on every measure, at both
points.

| Point | S_A | S_C | X_AC | X_CA | V_C | V_CA | R_A | R_C | P_A | P_C | cos(u_A, u_C) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3600 | 0.108 | 0.286 | 0.276 | 0.100 | 0.034 | 0.017 | −0.008 | 0.009 | 0.033 | 0.021 | 0.993 |
| 1800 | 0.124 | 0.074 | 0.082 | 0.190 | 0.004 | 0.030 | −0.012 | 0.010 | 0.031 | 0.014 | 0.992 |

Secondary tests at 3600 (PFATE, sign tests over 28 seeds):

| Test | Result | Label |
| --- | --- | --- |
| X_AC: A's direction releases C | 21/28, p 0.013 | CAUSAL |
| X_CA: C's direction moves A | 24/28, p 0.0002 | CAUSAL |
| V_C: C's own look-high direction moves C | 19/28, p 0.087 | NOT_DETECTED |
| V_CA: look-high on C read by A as safety | 22/28 | CAUSAL |
| S_A against the random direction | 20/28 | DIRECTION_AHEAD |
| S_C against the random direction | 23/28 | DIRECTION_AHEAD |
| S_A, PFATE against PYOKED | 25/28 | DERIVED_AHEAD |
| S_C, PFATE against PYOKED | 22/28 | DERIVED_AHEAD |
| R_A, R_C (random controls) | 13/28, 19/28 | NOT_DETECTED |
| P_A (symmetric perturbation effect), PFATE against PYOKED | 27/28 | DERIVED_AHEAD |
| P_C (symmetric perturbation effect), PFATE against PYOKED | 28/28 | DERIVED_AHEAD |
| cos(u_A, u_C), PFATE against PYOKED | 16/28 (0.993 against 0.991) | NO_DIFFERENCE_DETECTED |

At 1800, SA and SC are also CAUSAL (27/28 and 20/28), but X_AC is not
detected (17/28). That gives the reading PARTLY_SHARED there.

## 3. What the steering shows (post-hoc descriptives, disclosed)

From `p3c_steer/posthoc/describe.log`. None of this is confirmatory.

### 3.1 One body axis, read with opposite signs

- **The geometry is not learned under the fate.**
  - u_A and u_C have cosine 0.99 in all three arms (0.993 PFATE, 0.991
    PYOKED, 0.991 PNOFATE).
  - The look-high directions are nearly opposite to them (cosine about
    −0.9).
  - The probe changes the same input channel on both trial types, so it
    displaces the state along the same axis whichever decision is pending.
- **What the fate changes is the size and the reading.**
  - The displacement is about twice as large in PFATE (norm 5.8 against
    2.9 and 3.2).
  - Only in PFATE does the state on that axis move behaviour.
- **One-sided effects, PFATE, 3600:**

  | Push | Effect on A's abstention | Effect on C's abstention |
  | --- | --- | --- |
  | +u_A (toward "low") | +0.162 | −0.026 |
  | +u_C (toward "low") | +0.136 | −0.010 |
  | −u_A (away from "low") | +0.013 | +0.212 |
  | −u_C (away from "low") | +0.008 | +0.247 |

  - Pushing the state toward "low" makes A abstain; pushing it away from
    "low" makes C abstain.
  - Each decision becomes cautious on the side of its own risk: A's
    memory is at risk when the body is low, and C's perception when it is
    high.
- **The C "release" is mostly the other half of the contrast.**
  - Baseline C abstention in these test episodes is about 0.006, so there
    is almost no room for steering to release it further.
  - The directional measure S_C therefore comes mostly from −u_C
    *raising* C's caution, not from +u_C lowering it.
  - The pre-registered measure is a difference and cannot separate the two
    halves. The reading "one axis, each decision cautious on its own side"
    covers both.
- **The real look-high direction v_C barely moves C** (V_C 0.034, not
  detected).
  - Its norm is about 3.5, so at scale 0.5 it shifts the state by about
    1.75.
  - Half of −u_C shifts it by about 2.9.
  - C's caution seems to need a larger push toward the high side than the
    look-high probe itself produces. This is a guess, not tested.

### 3.2 A abstains on the body reading, not on the state of its memory

Correct-given-report on steered A trials, PFATE, 3600 (median, with the
lowest seed after the slash):

| Steering | Correct-given-report on A |
| --- | --- |
| +u_A | 0.992 / 0.718 |
| −u_A | 0.754 |
| −u_C | 0.522 |
| Random directions | 0.51–0.64 |

- **Under +u_A,** A's held cue is intact. Yet A abstains much more
  (+0.162). The extra abstention is not a response to damaged content.
- **Under random directions,** A's content is mostly destroyed: answers
  are near chance. Yet A abstains only slightly more (+0.02 to +0.03).
- The fated agent's abstention on A tracks where the state sits on the
  body axis, that is, the predicted risk. It does not track whether the
  held content is actually intact.
- This matches P1d's finding of a referent to the body rather than a
  monitor of the memory. It is a limit on any "self-monitoring" reading:
  what the agent models is its body's condition, not its own computation.
- C's accuracy is unaffected by any steering (median ≥ 0.998).

### 3.3 Per seed, the cause tracks the behaviour

Spearman correlations over 28 seeds, PFATE, 3600:

| Pair | Correlation |
| --- | --- |
| Behavioural C release and S_C | 0.92 |
| Behavioural A_low and S_A | 0.45 |
| S_C and X_AC (same axis) | 0.99 |
| S_A and X_CA | 0.81 |
| S_A and S_C | 0.32 |

- The C release is uneven across nets.
  - S_C quartiles: −0.003, 0.286, 0.699.
  - 8 seeds have S_C < 0.
- Where a net shows the release in behaviour, steering along its axis
  produces it; where it does not, steering does nothing. The direction
  appears to carry the readout and is not an accident of the perturbation.

### 3.4 A leak on the C side, and a robustness check

- **The leak.** In PFATE, during the +u_A and +u_C runs, C's abstention on
  *unsteered* trials rises above the plain evaluation:
  - median +0.061, maximum +0.66 in one seed;
  - at 1800: +0.029, maximum 0.49.
- **Where it does not appear:**
  - in the −u runs;
  - in the random-direction runs (median ≤ 0.002);
  - in either rival (≤ 0.006);
  - on A it is small (median 0.010, maximum 0.09).
- **Comparison with calibration and stage 0.**
  - Calibration round 2 (five of P3b's nets) showed a median leak of at
    most 0.013.
  - On P3b's nets in stage 0, the same leak is median 0.006, maximum
    0.36.
  - It is larger on the final nets, in the nets whose C readout is strong.
- **What it means for the measure.** Steering toward "low" changes C's
  behaviour on later trials, through the carried state. Clamping removed
  the gross leak of round 1 but not this direction-specific carry-over.
  - Because the effect is measured as steered minus unsteered, a raised
    unsteered baseline in the +u_C run makes effect(+u_C) more negative.
    That inflates S_C.
- **The check.** A contrast between steered trials only, such as
  S_C′ = abstention on steered C trials under −u_C minus under +u_C, drops
  the unsteered baselines. It is conservative, since the leak can also
  raise steered abstention in the +u runs.

  | Contrast | 3600 | 1800 |
  | --- | --- | --- |
  | S_A′ | 25/28 (p < 0.0001), CAUSAL | 27/28, CAUSAL |
  | X_CA′ | 25/28, CAUSAL | 26/28, CAUSAL |
  | S_C′ | 19/28 (p 0.087, median 0.214), not detected | 18/28, not detected |
  | X_AC′ | 19/28, not detected | 16/28, not detected |

- **Reading.**
  - The A-side cause (u along the "low" axis moves A) is robust.
  - The C-side cause is CAUSAL by the frozen rule but not robust to the
    leak. The medians stay large and the per-seed association (0.92)
    stays, but the sign test no longer passes.
  - The label stands as frozen. The C half of "two readouts" should be
    read as probable, not established.

### 3.5 Stage 0 against the final run

PFATE medians at 3600:

| Measure | Stage 0 (P3b's nets, 27 usable) | Final run |
| --- | --- | --- |
| S_A | 0.060 | 0.108 |
| S_C | 0.030 | 0.286 |
| X_AC | 0.040 | 0.276 |
| X_CA | 0.122 | 0.100 |
| V_C | 0.006 | 0.034 |

- In stage 0, SA was CAUSAL (22/27) and SC was not detected (18/27).
- On P3b's nets the C readout was weak in behaviour too (P3b's C half was
  mostly −C_low in about 10 of 27 nets), so its steering was weak.
- The new seeds have a stronger C release (B2 median 0.266). P3b's
  perception referent C_high also passes on them.

## 4. Against the expectations (protocol §7)

| Outcome at 3600 | Expected | Observed |
| --- | --- | --- |
| Valid | 0.85 | yes |
| At least 14 usable | 0.95 | 28 |
| Gate | 0.92 | PASS |
| B1 DERIVED_AHEAD | 0.90 | yes (26/28) |
| B2 DERIVED_AHEAD | 0.55 | yes (23/28) |
| SA CAUSAL | 0.60 | yes (25/28) |
| SC CAUSAL | 0.45 | yes (20/28; fragile, §3.4) |
| CONFIRMED_CAUSAL | 0.25 | **this** |
| Structure ONE_DIRECTION_TWO_READOUTS | 0.45 | **this** |
| R_A, R_C not detected | 0.85 | yes |
| P_A PFATE ahead of PYOKED | 0.75 | yes (27/28) |
| Stage 0 SA / SC | 0.65 / 0.50 | CAUSAL / not detected |

- My central expectation (CONFIRMED_BEHAVIOURAL or NOT_CONFIRMED, 0.60
  together) was wrong.
- The C release was the weak link I expected:
  - in stage 0, on P3b's nets, it failed;
  - on the new seeds it replicated more strongly than in P3b.
- The structure outcome was the one the protocol called most likely, for
  the reason given there: the body reading enters through the same input
  channel on both trial types.

## 5. Disclosures

- **Calibration of the steering.**
  - **Round 1:** P1b's unclamped steering was broken on these saturated
    agents. It leaked into unsteered trials (abstention 0.46–0.95).
  - **Round 2:** the steering was redesigned with clamping, and a scale
    rule was written before the round. No scale met all three criteria,
    since A's accuracy on steered trials falls to chance at every scale.
    The rule picked 0.5.
  - Both rounds were blind to every directional, cross and geometry
    measure (protocol §3).
- **Leak.** The leak of §3.4 was not seen in calibration at this size. It
  is reported here and was found after the result was known.
- **Stage 0** was declared in the protocol and run on committed P3b
  weights before the final run. It does not enter the label.
- **Resumes.** The final run ran in 7 batches of 4 seeds over 4
  invocations, resuming from `partial/` (`resumed_jobs` 24 in the
  metadata). There were no restarts or errors.
- **Verification.**
  - Source hashes in `raw.json` match the files at the freeze (a3bba7b).
  - `run_p3c_steer.py --score p3c_steer` reproduces `REPORT.md`, except
    for the trailing newline from `print`, as in P3b.
  - `score()` on the raw records equals `scores.json`.
  - `run.log` contains no error.
- **Exclusions:** none.
- **Post-hoc analyses** are in `p3c_steer/posthoc/describe.py`. They were
  written after the result was known, and the steered-only contrast (§3.4)
  was chosen after the leak was seen.

## 6. Limits

- **As in P3b:**
  - one small GRU;
  - one world;
  - a given drive;
  - the probes change the shown reading only;
  - each decision is trained under its own risk, so differentiation is
    task-optimal.
- **Sufficiency, not necessity.** Steering shows that moving the state
  along the probe axis is enough to move each decision. It does not show
  that the decisions use only that axis. Q-NECESSITY is not tested.
- **The C half is fragile.** It passed by one seed and does not survive
  the leak-robust contrast (§3.4).
- **The structure reading is partly forced by the geometry.**
  - With u_A ≈ u_C (cosine 0.99 in every arm), the cross tests X_AC and
    X_CA nearly repeat SC and SA.
  - "One direction" is a fact about the probe channel, shared by the
    rivals. "Two readouts" is the learned part.
  - The test that would have shown separate directions had little room to
    do so.
- **Steering at this scale disturbs A's held content** in some directions
  (§3.2), although not along +u_A, which carries most of S_A.
- **Clamping** makes steering an approximate "set these units to their
  probed values". Magnitudes are not comparable with P1b, P1d or P3.
- **"Self-state" and "self-model"** mean functional patterns of abstention
  and of state. Nothing about awareness or experience follows. Layer 6 is
  not addressed.

## 7. What it means for the program (in layer terms)

| Layer | What is now shown | Where |
| --- | --- | --- |
| L0 | A precarious substrate (overwrite of the agent's own state when the body is low; corrupted perception when it is high) | P1c, P3b, P3c |
| L1 | Regulation recruited by that precarity: PFATE keeps the body in band better than both rivals | P1c, P1d, P3, P3b; replicated in P3c (26/28 and 25/28) |
| L3 | The body reading reaches every decision: one state axis enters every trial type | P3; in P3c the axis is shared by all arms, and only its use is learned |
| L3 → L4 | Each decision reads that axis with the sign of its own risk. Behaviour confirmed on new seeds. Cause shown for A (robust) and for C (by the frozen rule, fragile) | P3b descriptive; **P3c CONFIRMED_CAUSAL** |
| L4 | The content of the self-model is in the readouts, not in separate state directions. What is modelled is the body's condition, not the integrity of the agent's own computation (§3.2) | P3c, post-hoc |

**In plain terms.**

- The fated agent has one internal variable that stands for "how my body
  is".
  - Pushing it causes behaviour: one decision becomes cautious when it
    says "low", and another when it says "high".
  - Each decision is cautious on the side where it is the one at risk.
- In P3, the same variable acted like a global mood (L3). In P3b and P3c,
  decisions with their own risks read it in their own way. That is a
  differentiated readout of a shared body state.
- It is not two separate representations. It is closer to one interoceptive
  signal with decision-specific appraisals than to a self-model with
  separate contents.
- The agent does not model its own memory's integrity. It abstains on the
  body reading even when its memory is intact, and does not abstain when
  its memory is scrambled by a random push.

**Recommended next step (for the PI; not authorized by this card).**

**P3d, necessity and separation.**

- **(a) Q-NECESSITY:** project the body axis out of the state during the
  delay. Do both readouts vanish while accuracy holds?
- **(b) Content separation:** give A two different body-linked risks with
  different consequences, so that one decision must keep two kinds of
  body content apart. Ask whether the state develops separate directions
  when one readout can no longer carry both.

**Alternatives:**

- **Self-monitoring proper:** add a risk that damages the agent's
  computation regardless of the body, so that only a monitor of the state
  itself (not of the body) can predict it.
- **The carry-over leak (§3.4),** studied as its own effect: how steering
  toward "low" raises C's caution on later trials.
- **L5:** a lifetime change of band.

**Forward note (2026-11-24).** The PI chose the self-monitoring route.
It ran as P1e ([P1E_SELFMON_RESULTS.md](P1E_SELFMON_RESULTS.md)). The run
is INVALID: exposure fell below its frozen floor. Descriptively, the agent
learned to read a conflict in its own memory: first-order ambiguity, not a
second-order trace. It learned this from exposure, not from the body link.

## 8. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the
  perception corruption, the probes, the steering and the drive exist only
  inside the agent's world and network. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 9. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | Memory referent (A_low 26/28) and C release (23/28) in PFATE, on new seeds |
| Q-LEARN | Both are learned under the fate. PFATE beats a yoked rival with the same losses; the rivals are about 0. The shared axis exists in every arm; its use is learned |
| Q-CAUSE | Steering along the body axis moves A (25/28; robust) and C (20/28; CAUSAL by the frozen rule, fragile to a leak, §3.4), each with its own sign |
| Q-NECESSITY | Not tested |

## 10. Reproduce

```bash
python -m unittest test_p3c_steer test_p3b_diff
python run_p3c_steer.py --score p3c_steer                       # rescore the committed run
python run_p3c_steer.py --score-stage0 p3c_steer_stage0          # rescore stage 0
python run_p3c_steer.py --mode final --out <new dir>             # about 6 h on 4 workers (7 batches of about 50 min)
python p3c_steer/posthoc/describe.py                             # post-hoc descriptives (reads raw.json)
```
