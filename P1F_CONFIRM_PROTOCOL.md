# P1f protocol: confirmation of the self-monitor and the second-order test (Layer 0 → Layer 4)

- **Status:** STOPPED at calibration (2026-11-24). Three rounds failed the
  exposure criterion (§3); per the calibration rules there is no freeze, no
  stage 0 and no final run. See [P1F_CONFIRM_RESULTS.md](P1F_CONFIRM_RESULTS.md).
  The rest of this document is the draft as written before calibration,
  unchanged.
- **Follows:** [P1E_SELFMON_RESULTS.md](P1E_SELFMON_RESULTS.md) (INVALID on
  exposure; descriptive monitor, first-order). Authorized by the PI
  ("Proceed with the recommended steps", 2026-11-24).
- Astra review waived by the PI. No consciousness claim.

## 1. Questions

P1e's run failed its own exposure floor, so its monitor is descriptive. Its
post-hoc look suggested the monitor reads first-order ambiguity: in trained
nets a conflict stays visible as low-confidence content. P1f asks:

1. **Confirmation.** With exposure secured, does the agent learn to abstain
   on a conflict in its own memory, at matched perturbation, against a
   network never damaged? (P1e's P1E-1, now confirmatory.)
2. **Second order.** At **matched first-order confidence**, does a conflict
   still raise abstention? If so, the agent's state carries, and its policy
   uses, a signal about its own state that is not its confidence in the
   content. If not, the monitor is first-order: it reads how ambiguous the
   content is.
3. **The L0 arrow** (as in P1e). Does the precarious body change the
   monitor, against the same damage not tied to the body?

## 2. Design

**Training, damage, arms, evaluation and P1e's measures are P1e's,
unchanged.** They are imported from `trackc_swap/selfmon.py` and
`run_p1e_selfmon.py`, which stay hash-pinned. The one change is the damage
rate (§3).

| Arm | Damage source in training |
| --- | --- |
| PFATE | Its own body: per delay step, probability min(P_MAX_F, RATE_F × gain) |
| PYOKED | PFATE's gains replayed step by step: the same exposure, not through its own body |
| PNOFATE | None (the mechanical baseline) |

**The second-order pass** (`trackc_swap/secondorder.py`) is new. It runs on
the trained weights of every arm at every point (1800 and 3600):

- **Evaluation world:** a fresh world on its own streams (tag offset 140;
  P1e's evaluation used 120).
- **Probe:** damage off except P1e's split probe on 2/3 of the trials (half
  conflict, half same), at EARLY (delay step 1) and at LATE (step 8). No
  drain.
- **At the report step** the GRU state h is collected (P1e's collection).
  Two first-order confidences are computed per trial:
  - **own margin:** |logit(REP1) − logit(REP0)| of the agent's own policy
    head on h. This is the agent's own read of which value it holds. The
    head is linear in h.
  - **LDA margin:** P1e's linear decoder of the held value, fitted on clear,
    undamaged, unprobed trials (within-class SD units).
- **M2** = abstention(conflict) − abstention(same) at matched confidence:
  - the pooled conflict and same trials (clear, undrained) are cut into 10
    quantile bins of the confidence;
  - bins with at least 5 conflict and 5 same trials are kept;
  - the per-bin differences are averaged, weighted by the bin's conflict
    count.
- **Coverage** is the share of conflict trials in kept bins.
- Per seed and arm: **M2_own** and **M2_lda** are the means over EARLY and
  LATE of the runs that have a value.

## 3. Calibration (disclosed)

Calibrated quantity: RATE_F only. P_MAX_F stays 0.3. The rules for each
round are in `p1f_confirm_calibration/RULES.md`, each written and committed
before its round. Eight seeds per round (P1e used four, and its floor
failed). The summary is P1e's blind summary: no abstention on probed
trials, no monitoring measure, and no second-order pass.

| Round | Settings | What it showed | Decision |
| --- | --- | --- | --- |
| 1 | RATE_F 3.0 (seeds 10300–10307) | PFATE conflict share 0.019 (3/8 ≥ 0.02); in band 0.956; acc under conflict 0.509 | (c) fails → round 2 at 6.0 |
| 2 | RATE_F 6.0 (seeds 10308–10315) | 0.025 (6/8 ≥ 0.02); in band 0.947; 0.509 | (c) fails → round 3 at 12.0 |
| 3 | RATE_F 12.0 (seeds 10316–10323) | 0.029 (8/8 ≥ 0.02); in band 0.944; 0.518 | (c) fails → stop |

## 4. Measures

P1e's measures, unchanged (P1E_SELFMON_PROTOCOL.md §4): M, M_early, M_late,
Q, M_conf, acc_conflict, drain_effect, nat_M, share_conflict, in_band. New:

| Measure | Definition |
| --- | --- |
| M2_own | M at matched own margin (§2) |
| M2_lda | M at matched LDA margin |
| M2_own_early, M2_own_late | M2_own in one run |
| coverage_own, coverage_lda | Share of conflict trials in kept bins |
| raw_own | The unmatched conflict − same difference in the second-order pass |

## 5. Decision rules (exactly as in `run_p1f_confirm.py`)

**Validity** (P1e's, medians over seeds):

- (a) phase-1 clear correct ≥ 0.80;
- (b) phase-1 accuracy under the conflict probe ≤ 0.70;
- (c) PFATE natural share of clear trials with a conflict event at 3600
  ≥ 0.02.

**Primary tests at 3600.** Two-sided paired sign tests, α 0.05, Holm over
the three:

| Test | Measure | Comparison | Labels |
| --- | --- | --- | --- |
| P1F-1, monitor confirmed | M | PFATE against PNOFATE | DERIVED_AHEAD / HOST_AHEAD / NO_DIFFERENCE_DETECTED / UNDETERMINED |
| P1F-2, second order | M2_own | PFATE against PNOFATE | as P1F-1 |
| P1F-3, the L0 arrow | M | PFATE against PYOKED | DERIVED_AHEAD / YOKED_AHEAD / NO_DIFFERENCE_DETECTED / UNDETERMINED |

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | P1F-1 UNDETERMINED |
| NOT_CONFIRMED | P1F-1 not DERIVED_AHEAD |
| MONITOR_SECOND_ORDER | P1F-1 and P1F-2 DERIVED_AHEAD |
| MONITOR_FIRST_ORDER | P1F-1 DERIVED_AHEAD; P1F-2 NO_DIFFERENCE_DETECTED or HOST_AHEAD |
| MONITOR_ORDER_UNDETERMINED | P1F-1 DERIVED_AHEAD; P1F-2 UNDETERMINED |

- **Flags:**
  - **Weak:** a Holm p above 0.05 on a test the label needs.
  - **Thin overlap:** PFATE's median coverage_own at 3600 below 0.25. The
    second-order reading then rests on a minority of conflict trials.
  - **Hardened:** PFATE's accuracy under the conflict probe above 0.75.
- **L0 reading** (P1F-3; for a valid run):

  | P1F-3 label | Reading |
  | --- | --- |
  | DERIVED_AHEAD | FATE_STRENGTHENS_MONITOR |
  | YOKED_AHEAD | FATE_SUBSTITUTES_FOR_MONITOR |
  | NO_DIFFERENCE_DETECTED | EXPOSURE_SUFFICES |
  | otherwise | UNDETERMINED |

**Declared secondaries** (not Holm-corrected, not decisive):

- P1e's secondaries, unchanged, and M_early PFATE against PNOFATE;
- M2_own, PYOKED against PNOFATE;
- M2_lda, PFATE and PYOKED against PNOFATE (does the second-order reading
  hold under the decoder's confidence too?);
- M2_own, PFATE against PYOKED;
- one-sample routes for M2_own, M2_own_early, M2_own_late and M2_lda.

## 6. Stage 0 (declared; not the confirmation)

- The second-order pass runs on P1e's saved weights at 3600 (seeds
  2800–2827), after the freeze and before the final run.
- It uses the same code and rules as the final run, labelled from M2_own,
  PFATE against PNOFATE:

  | Test label | Stage 0 label |
  | --- | --- |
  | DERIVED_AHEAD | SECOND_ORDER_SIGNAL |
  | UNDETERMINED | UNDETERMINED |
  | otherwise | FIRST_ORDER_ONLY |

- Thin overlap is flagged as above.
- **Not confirmatory:** P1e's run was INVALID, and the question was
  conceived after seeing P1e's data. Stage 0 changes nothing in the final
  run.

## 7. Readings

| Outcome | Reading |
| --- | --- |
| MONITOR_SECOND_ORDER | The agent abstains on a conflict in its own memory even when its own first-order read of the value is as decisive as on an intact memory. Its state carries, and its policy uses, a signal about the state that is not confidence in the content: an operational second-order signature (Layer 4) |
| MONITOR_FIRST_ORDER | The monitor is confirmed and reads first-order ambiguity: the agent is cautious when its content is ambiguous, and a conflict matters only through that. A self-monitor of confidence, not of integrity |
| MONITOR_ORDER_UNDETERMINED | The monitor is confirmed. Too few conflict trials overlap the intact ones in confidence to decide its order |
| NOT_CONFIRMED | P1e's descriptive monitor does not replicate with exposure secured |
| EXPOSURE_SUFFICES / FATE_SUBSTITUTES / FATE_STRENGTHENS | As in P1e §6 |

## 8. Expectations (written before calibration, stage 0 and any final seed)

Probabilities are my own.

| Outcome at 3600 | Probability | Why |
| --- | --- | --- |
| Valid | 0.85 | Eight calibration seeds and a margin above the floor; regulation may still cut exposure |
| P1F-1 DERIVED_AHEAD | 0.90 | P1e: 27/28 descriptively, at lower exposure |
| P1F-2 DERIVED_AHEAD | 0.40 | P1e's M_conf_early was 0.054 (18/26) on few trials. Same-probed trials rarely have low own margin, so the matched bins are the middle of the range |
| Thin-overlap flag | 0.35 | P1e: 2.6% of PFATE's conflict states reached the decoder's median |
| Overall MONITOR_SECOND_ORDER | 0.33 | |
| Overall MONITOR_FIRST_ORDER | 0.42 | |
| Overall MONITOR_ORDER_UNDETERMINED | 0.05 | |
| Overall NOT_CONFIRMED / UNDETERMINED / INVALID | 0.05 / 0.02 / 0.13 | |
| L0 FATE_SUBSTITUTES / EXPOSURE_SUFFICES / FATE_STRENGTHENS | 0.45 / 0.45 / 0.10 | P1e: yoked ahead, 5/28 |
| M2_lda agrees with M2_own in label | 0.60 | Both are linear reads of the value |
| Drain effect, PFATE against PYOKED, DERIVED_AHEAD | 0.15 | P1e: not replicated |
| Regulation, PFATE against PYOKED, FATE_AHEAD | 0.80 | Replicated in every study of this line |
| Stage 0: SECOND_ORDER_SIGNAL / FIRST_ORDER_ONLY / UNDETERMINED | 0.40 / 0.50 / 0.10 | |

**My central expectation** is that the monitor is confirmed (0.80 with a
valid run), with a first-order reading slightly more likely than a
second-order one.

## 9. Engineering record

- **New module:** `trackc_swap/secondorder.py`:
  - own margin;
  - LDA margin (P1e's decoder, returning per-trial margins; tested to
    reproduce its threshold);
  - the matched difference;
  - the second-order pass.
- **Runner and scorer:** `run_p1f_confirm.py`.
  - Training is `selfmon.run_seed_m`, unchanged, followed by the
    second-order pass.
  - Calibration skips the pass.
  - Final mode refuses any rate but the frozen one.
- **Tests:** `test_p1f_confirm.py`. They cover:
  - matched difference: zero when abstention is first-order only; recovers
    a planted effect; None without overlap;
  - own margin;
  - the LDA margin against P1e's decoder;
  - measures and labels, and stage-0 labels;
  - no second-order pass in calibration;
  - the final-mode rate guard;
  - safety;
  - disjoint seeds against every earlier runner.
- **Compute:**
  - the second-order pass takes about 5 s per net;
  - a final seed takes about 35 minutes plus 30 s;
  - the final run is about 4 h 15 min (7 batches of 4 on 4 workers);
  - stage 0 takes a few minutes;
  - a calibration round of eight seeds takes about 70 minutes.

## 10. Limits and claim ceiling

- As in P1e: one small GRU, one world, a given drive, damage defined by the
  experimenter.
- **"Second order" is operational.** It means abstention driven by a
  conflict beyond the agent's own linear read of the value (and, as a
  secondary, beyond a linear decoder's). It does not show a representation
  about a representation, or a reportable introspective state.
- **Matching is coarse.** It uses 10 bins of one confidence at a time.
  Residual confounding within a bin is possible; the synthetic tests bound
  it for a monotone dependence.
- **Exposure is raised** to secure the floor. This tests sufficiency at one
  rate only.
- **Nothing about awareness or experience follows.** Layer 6 is not
  addressed.

## 11. Safety

- Simulated variables only (X1–X5). The body, the damage, the probes and
  the drive exist only inside the agent's world and network. No real
  process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

## 12. Admission questions

| # | How P1f answers it |
| --- | --- |
| Q-EXIST | M per arm; M2_own and M2_lda routes |
| Q-LEARN | P1F-1 and P1F-2: against a network never damaged |
| Q-CAUSE | The split probe is the intervention: a controlled conflict at matched perturbation, and in M2 at matched first-order confidence |
| Q-NECESSITY | Not tested |
