# P1e protocol: self-monitoring of the agent's own computation (Layer 0 → Layer 4)

- **Status:** frozen at the commit that adds this file's final version,
  before any final seed is run.
- **Authorized by the PI** on 2026-11-24 ("self-monitoring", chosen over
  P3d after P3c).
- Code: `trackc_swap/selfmon.py`, `run_p1e_selfmon.py`,
  `test_p1e_selfmon.py`. Calibration: `p1e_selfmon_calibration/`.
- Not reviewed by Astra (waived by the PI). No consciousness claim.

## 1. What is being tested

Every study since P1 found a self-referent to the **body**. The fated agent
abstains when its body predicts that its memory is at risk (P1, P1c, P1d),
the reading spreads to other decisions (P3) and differentiates by
decision (P3b, P3c). P3c's post-hoc analysis then showed what is missing.
The agent abstains on the body reading even when its memory is intact, and
hardly abstains when random pushes scramble its memory. It models the
conditions of its breakdown, not the breakdown.

Layer 4 in the PI's map is a metacognitive head: *internal evaluation of the
system's own state and reliability*. A monitor of one's own computation is
its core and has never been shown in this line. The overwrite probe of
P1c, P1d and P3 could not show it: every arm, including the arm never
overwritten, "detected" a whole foreign state equally (about 0.23). A whole
foreign state is a valid state; nothing in it is detectable.

P1e asks three questions:

1. **Can the agent learn to monitor its own computation**, when the damage
   leaves an internal trace? Against a network never damaged, so that any
   mechanical response is subtracted.
2. **Does the monitor survive the first-order content settling?** If the
   damage happens early and the content has time to settle into a
   confident but random value, does the agent still abstain? A monitor
   that keeps a trace of its own damage is a second-order state about the
   first-order content. A readout of first-order ambiguity is not.
3. **Does a precarious body change the monitor** (the L0 arrow), against an
   agent with the same exposure to damage that is not tied to its body?

## 2. Design as built

**Training is P1c's** (`trackc_swap/selfover.py`), with one change: the
damage.

- **Same as P1c:**
  - one held-cue task;
  - phase 1 damage-free (warm-up, wrong-cost ramp, 2400 regulation
    updates under the innate drive);
  - phase 2 of 3600 updates for three arms from the same phase-1 weights;
  - the innate homeostatic drive (0.04 × gain) in every arm.
- **Measurement points:** 1800 and 3600 (primary).
- **Seeds:** final 2800–2827; calibration 10200–10215.

**The damage: split overwrite.**

- On a damage event, a random half of the GRU units (35 of 70, drawn
  afresh) take the values of a donor's state. The donor is another agent
  in the batch that is in the delay of a clear trial and not itself
  damaged in its current trial.
- **CONFLICT event** (the donor holds the other value, about half of
  events): the state carries two incompatible halves.
  - The value is lost. The two halves are exchangeable, so no robustness
    can tell which is its own.
  - The conflict is in principle readable from the state.
- **SAME event** (the donor holds the same value): the same amount of
  perturbation, with the value intact and no conflict.
- **Timing:** at most one event per trial; it happens after the recurrent
  update and before the readout, and the mixed state is carried forward.
- No gradient flows into the donor.

**Damage in training:** at every delay step of a trial not yet damaged,
with probability min(P_MAX_M, RATE_M × gain). gain is the SAT fate gain of
the arm's damage source:

| Arm | Damage source |
| --- | --- |
| PFATE | Its own body (the lead) |
| PYOKED | PFATE's gains replayed step by step: the same exposure, not through its own body |
| PNOFATE | No damage ever: the mechanical baseline, a network never damaged |

RATE_M and P_MAX_M are calibrated (§3).

**Evaluation** is on copies in fresh worlds. Damage is off except for the
probe.

- **Natural running:**
  - PFATE under its own fate;
  - PYOKED replaying PFATE's gains;
  - PNOFATE damage-free.
  - Measures: in-band time, share of clear trials damaged and with a
    conflict (exposure), and natural monitoring (abstention on
    conflict-damaged minus same-damaged trials, where both exist).
- **The split probe,** two runs per arm:
  - **Assignment:** at the cue, each trial is assigned none, conflict or
    same (probed on 2/3 of trials, half conflict, half same).
  - **EARLY run:** the probe is applied at the first delay step. Eight
    recurrent updates follow before the readout.
  - **LATE run:** the probe is applied at the last delay step. One update
    follows before the readout.
  - **Donor:** chosen to hold the other value (conflict) or the same value
    (same).
  - **Drain:** the shown body reading is lowered by 0.15 on half the trials,
    independently.
- **Decoder:**
  - In each probe run, the GRU state at the probe step is collected.
  - A linear decoder of the held value (shrinkage LDA) is fitted on
    clear, undamaged, undrained, unprobed trials.
  - On each cell it gives the decoding accuracy and the margin (distance
    from the boundary in within-class SD units).
  - "Confident" trials are those whose margin is at least the median
    margin of the fitting trials.

## 3. Calibration (disclosed)

Calibrated quantities: RATE_M and P_MAX_M only. The rules for each round
are in `p1e_selfmon_calibration/RULES.md`, each written and committed before
its round. The summary shows only:

- validity;
- exposure;
- in-band time;
- accuracy under the conflict probe.

It shows no abstention on probed trials and no monitoring measure.

| Round | Settings | What it showed (medians over seeds 10200–10203, 3600) | Decision |
| --- | --- | --- | --- |
| 1 | RATE_M 1.0, P_MAX_M 0.3 (P1c's schedule; at most one event per trial) | (a) phase-1 clear correct 1.000; (b) phase-1 accuracy under the conflict probe 0.492 (same probe 0.999); (c) PFATE natural share of clear trials with a conflict 0.032 (per seed 0.006–0.039; damaged 0.063); (d) PFATE in band 0.907 (PYOKED 0.900, PNOFATE 0.900). Accuracy under the conflict probe at 3600: PFATE 0.524 (0.49–0.54), so not hardened | All four criteria met: **freeze with RATE_M 1.0, P_MAX_M 0.3** |

- **Exposure is modest.** About 3% of PFATE's clear trials carry a conflict
  in natural running, and one calibration seed had 0.6%. The learning
  signal for a monitor is therefore small. This is the same order as the
  exposure under which P1c's body referent formed (0.03). It is disclosed
  as the main reason a null result is plausible (§7).
- Round 1 took about 35 minutes (4 seeds on 4 workers).

## 4. Measures (per seed, per arm, at each point; clear trials, undrained unless stated)

| Measure | Definition |
| --- | --- |
| M_early, M_late | Abstention on conflict-probed minus same-probed trials, in the EARLY and LATE runs. The same perturbation, with and without an internal conflict |
| M | The mean of M_early and M_late |
| Q_early, Q_late | Abstention on same-probed minus unprobed trials: perturbation without conflict (P3's sensitivity) |
| M_conf_early, M_conf_late | M restricted to confident trials (decoder margin at least the median of undamaged trials): monitoring beyond first-order confidence |
| decode_conflict_early, margin_conflict_early | First-order content on conflict-early trials |
| acc_conflict, acc_same | Correct-given-report under the conflict and same probes (pooled early and late) |
| drain_effect | Abstention on drained minus undrained unprobed trials: the body referent |
| M_early_drained, M_late_drained | M on drained trials |
| nat_M | Natural running: abstention on conflict-damaged minus same-damaged clear trials, if at least 10 of each |
| share_conflict, share_damaged, in_band | Exposure and regulation in natural running |

## 5. Decision rules (exactly as in `run_p1e_selfmon.py`)

**Validity**, medians over seeds:

- (a) phase-1 clear correct-report rate ≥ 0.80;
- (b) phase-1 (never damaged) correct-given-report under the conflict probe,
  early and late pooled, ≤ 0.70;
- (c) PFATE natural share of clear trials with a conflict event at 3600
  ≥ 0.02.

**Primary tests at 3600.** Two-sided paired sign tests, α 0.05, Holm over
the three:

| Test | Measure | Comparison | Labels |
| --- | --- | --- | --- |
| P1E-1, monitor learned | M | PFATE against PNOFATE | DERIVED_AHEAD / HOST_AHEAD / NO_DIFFERENCE_DETECTED / UNDETERMINED |
| P1E-2, monitor after settling | M_early | PFATE against PNOFATE | as P1E-1 |
| P1E-3, the L0 arrow | M | PFATE against PYOKED | DERIVED_AHEAD / YOKED_AHEAD / NO_DIFFERENCE_DETECTED / UNDETERMINED |

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | P1E-1 UNDETERMINED |
| NOT_LEARNED | P1E-1 not DERIVED_AHEAD |
| MONITOR_LEARNED | P1E-1 DERIVED_AHEAD and P1E-2 not |
| MONITOR_LEARNED_LATCHED | P1E-1 and P1E-2 both DERIVED_AHEAD |

- **Weak flag:** a Holm p above 0.05 on a test the label needs.
- **L0 reading** (P1E-3; reported for a valid run):

  | P1E-3 label | Reading |
  | --- | --- |
  | DERIVED_AHEAD | FATE_STRENGTHENS_MONITOR |
  | YOKED_AHEAD | FATE_SUBSTITUTES_FOR_MONITOR |
  | NO_DIFFERENCE_DETECTED | EXPOSURE_SUFFICES |
  | otherwise | UNDETERMINED |

- **Hardened flag:** PFATE's correct-given-report under the conflict probe
  at 3600 is above 0.75. The trained network then recovers the value, and a
  monitor is not needed.

**Declared secondaries** (not Holm-corrected, not decisive):

- M, PYOKED against PNOFATE;
- M_late, PFATE against PNOFATE;
- M_early, PFATE against PYOKED;
- M_conf_early (PFATE and PYOKED each against PNOFATE): the second-order
  test;
- Q_early, PFATE against PNOFATE;
- drain effect, PFATE against PYOKED (the body referent);
- in-band time, PFATE against each rival;
- one-sample routes per arm for M, M_early, M_late, M_conf_early, Q_early
  and nat_M.

## 6. Readings

| Outcome | Reading |
| --- | --- |
| MONITOR_LEARNED_LATCHED, M_conf_early ahead | The agent learned to monitor its own computation and keeps a trace of its own damage after the content settles. This is the first metacognitive (second-order) signature in this line |
| MONITOR_LEARNED | It reads its own representational conflict while it is present: monitoring of the current state, possibly first-order uncertainty |
| NOT_LEARNED | Exposure to detectable damage of its own computation does not produce a monitor in this agent; the body referent remains its only self-evaluation |
| EXPOSURE_SUFFICES | Monitoring comes from exposure, not from dependence on a body. In layer terms, L0 grounds the predictive self-referent and exposure grounds the monitor |
| FATE_SUBSTITUTES_FOR_MONITOR | The body referent partly replaces monitoring: an agent that can predict its breakdown watches itself less |
| FATE_STRENGTHENS_MONITOR | The precarious body grounds monitoring as well |

## 7. Expectations (written before any final seed)

Probabilities are my own. Calibration showed no monitoring measure.

| Outcome at 3600 | Probability | Why |
| --- | --- | --- |
| Valid | 0.90 | Calibration met (a)–(c), but exposure was below 0.02 in one of four seeds |
| P1E-1 DERIVED_AHEAD | 0.45 | The damage is detectable in principle and unhardenable. But conflicts reach only about 3% of PFATE's clear trials, the body referent offers a cheaper policy, and the never-damaged net's mechanical response to a conflict state is unknown |
| P1E-2 DERIVED_AHEAD | 0.25 | Requires a trace that survives eight recurrent updates; GRU attractors tend to settle a mixture into one value |
| Overall MONITOR_LEARNED_LATCHED | 0.20 | |
| Overall MONITOR_LEARNED | 0.25 | |
| Overall NOT_LEARNED | 0.45 | |
| Overall UNDETERMINED / INVALID | 0.03 / 0.07 | |
| L0 reading EXPOSURE_SUFFICES | 0.55 | PYOKED meets the same events with the same information in the state |
| FATE_SUBSTITUTES_FOR_MONITOR | 0.25 | PFATE can abstain on its body instead (P3c) |
| FATE_STRENGTHENS_MONITOR | 0.15 | |
| Hardened flag | 0.05 | The halves are exchangeable; calibration showed about 0.52 |
| M, PYOKED against PNOFATE, DERIVED_AHEAD | 0.45 | As P1E-1 |
| M_conf_early, PFATE against PNOFATE, DERIVED_AHEAD | 0.20 | The second-order test, hardest |
| Drain effect, PFATE against PYOKED, DERIVED_AHEAD (the body referent replicates) | 0.80 | P1c, P1d |
| Regulation, PFATE against PYOKED, FATE_AHEAD | 0.70 | Replicated in P1c, P1d, P3, P3b, P3c; this calibration was mixed |

**My central expectation** is NOT_LEARNED or MONITOR_LEARNED (0.70
together), with the L0 reading EXPOSURE_SUFFICES. A latched,
beyond-first-order monitor would be the program's first second-order
signature, and I think it unlikely at this exposure.

## 8. Engineering record

- **New module:** `trackc_swap/selfmon.py` (MonWorld, MonAgent, MonRunner,
  split probe, decoder). Earlier modules are imported, never modified.
- **Runner and scorer:** `run_p1e_selfmon.py`.
- **Tests:** `test_p1e_selfmon.py`. They cover:
  - split overwrite and donor values;
  - no gradient into the donor;
  - probe timing and the donor's value relation;
  - once per trial;
  - no natural damage at zero gain;
  - summary cells;
  - the decoder on synthetic data;
  - measures and labels;
  - a blind calibration summary;
  - safety;
  - disjoint seeds.
- **Final run:** 28 seeds in batches of 4, two batches per invocation,
  resuming from `partial/`. About 36 minutes per batch on 4 workers (from
  calibration), so about 4 h 15 min in all.
- **Rate in the code:** the defaults of `--rate` and `--p-max` are the
  frozen RATE_M 1.0 and P_MAX_M 0.3. The final mode refuses any other value.

## 9. Limits and claim ceiling

- As in P1c: one small GRU, one world, a given drive, damage defined by the
  experimenter.
- **"Monitoring" means** a pattern of abstention that tracks an internal
  conflict at matched perturbation. It does not mean a reportable
  introspective state.
- **Whether early conflict states have settled** is measured by a linear
  decoder, a proxy for first-order content. The confident subset is defined
  by it.
- **The never-damaged network is the mechanical baseline.** Its response to
  a conflict state it never met may be idiosyncratic. The within-arm
  contrast (conflict against same) controls for perturbation as such.
- **Sufficiency of exposure** is tested only at the calibrated damage rate.
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed.

## 10. Safety

- Simulated variables only (X1–X5). The body, the damage, the probes and the
  drive exist only inside the agent's world and network. No real process
  is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 11. Admission questions

| # | How P1e answers it |
| --- | --- |
| Q-EXIST | M per arm (one-sample routes) and M_conf_early |
| Q-LEARN | P1E-1 and P1E-2: against a network never damaged |
| Q-CAUSE | The split probe is itself the intervention: a controlled conflict at matched perturbation, with the body reading untouched |
| Q-NECESSITY | Not tested |
