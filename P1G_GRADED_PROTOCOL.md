# P1g protocol: self-monitoring with exposure fixed by design and graded damage (Layer 0 → Layer 4)

- **Status:** DRAFT. Calibration pending (§3). The decision rules, measures
  and expectations below are written before calibration and before any
  final seed. Only BASE_F is filled in at the freeze.
- **Follows:** [P1F_CONFIRM_RESULTS.md](P1F_CONFIRM_RESULTS.md) (stopped at
  calibration: regulation held exposure near a fixed level; stage 0 found
  P1e's monitor first-order in substance, with thin overlap). Chosen by the
  PI ("Stage 0, then P1g", 2026-11-24).
- Astra review waived by the PI. No consciousness claim.

## 1. Questions

1. **Confirmation.** With exposure fixed by design, does the agent learn to
   abstain on a conflict in its own memory, at matched perturbation,
   against a network never damaged? (P1e's P1E-1, now confirmatory.)
2. **Second order.** At **matched first-order confidence**, with conflict
   and same trials overlapping in confidence by design, does a conflict
   still raise abstention? If so, the agent's state carries, and its policy
   uses, a signal about its own state that is not its confidence in the
   content. If not, the monitor is first-order.
3. **The L0 arrow** (as in P1e). Does the precarious body change the
   monitor, against the same damage not tied to the body?

## 2. Design

Everything is P1e's (`trackc_swap/selfmon.py`, `run_p1e_selfmon.py`,
hash-pinned and unchanged: world, phase 1, arms, schedule, training,
P1e's split probe and measures) except two changes to the damage, made in
the new module `trackc_swap/gradmon.py`:

1. **A base damage rate regulation cannot reduce.** Per delay step of a
   not-yet-damaged trial the damage probability is
   min(0.3, BASE_F + 1.0 × gain): P1e's body-linked part (RATE 1.0,
   P_MAX 0.3, P1e's frozen values) plus a base.

   | Arm | Damage in training |
   | --- | --- |
   | PFATE | BASE_F + its own body's gain |
   | PYOKED | BASE_F + PFATE's gains, replayed step by step |
   | PNOFATE | None (the mechanical baseline) |

   Why: in P1e and P1f the damage taken was held near a fixed level by the
   agent's regulation, whatever the rate (P1f §3). The base sets exposure
   by design. PFATE and PYOKED keep identical damage statistics, so the L0
   arrow is unchanged in meaning.
2. **Graded damage.** Each event overwrites K units of the 70 with a
   donor's, K drawn uniformly from {9, 18, 26, 35} (about H/8 to H/2;
   P1e: always 35). A conflict with a small K leaves the agent's own
   majority holding the value, so some conflicts are still confident.

   Why: in P1e's nets only about one conflict trial in five had a same
   trial at its confidence, and the coarse matching was confounded (P1f
   §5b). Graded damage gives the matched test overlap by design.

**Evaluation** (copies in fresh worlds, tag offset 160; at 1800 and 3600):

- **Natural:** PFATE under its own fate, PYOKED replaying PFATE's gains,
  both with the base; PNOFATE undamaged. Gives exposure and in-band time.
- **Split probe A** — P1e's exactly: base off, K 35, on 2/3 of the trials
  (half conflict, half same), at EARLY (delay step 1) and LATE (step 8),
  drain on half the trials, decoder fitted. Gives P1e's measures (M,
  M_early, M_late, Q, M_conf, acc_conflict, drain_effect, …).
- **Graded probe B** — base off, K drawn per probed trial from
  {9, 18, 26, 35}, on 2/3 of the trials, at EARLY and LATE, no drain. At
  the report step the GRU state is collected, and per trial:
  - **own margin** |logit(REP1) − logit(REP0)| of the agent's policy head
    (P1f's `own_margin`);
  - **LDA margin** (P1f's `lda_margin`).

## 3. Calibration (disclosed)

Calibrated quantity: BASE_F only. Rules in
`p1g_graded_calibration/RULES.md`, each round's written and committed
before it runs. Eight seeds per round (10400–10423, rounds of 8), at most
three rounds. The summary is P1e's blind one plus the **overlap** on probe
B (caliper coverage of conflict trials by same trials on own margin, and
the median margins): computed from the margins alone, before and without
any abstention. No abstention on probed trials and no monitoring measure is
printed.

The starting value is analytic: a per-step base of 0.012 over the eight
delay steps damages about 9% of trials, about half of them with a conflict
(≈ 0.045), before the body-linked part.

| Round | Settings | What it showed | Decision |
| --- | --- | --- | --- |
| 1 | BASE_F 0.012 | pending | pending |

## 4. Measures

P1e's measures on probe A and natural running, unchanged. New, on probe B
(clear, undrained trials; per seed and arm, the mean over the EARLY and
LATE runs that have a value):

| Measure | Definition |
| --- | --- |
| M2_nn_own | Each conflict trial against its nearest same trial in own margin (with replacement), kept if within 0.05 pooled SD; mean over kept pairs of abstain(conflict) − abstain(matched same); None if fewer than 20 pairs |
| coverage_nn_own | Share of conflict trials kept |
| balance_own | Mean margin(conflict) − margin(matched same) over kept pairs |
| M2_nn_lda, coverage_nn_lda, balance_lda | The same on the LDA margin |
| M2_bins_own, M2_bins_lda | P1f's 10-bin match (secondary; known to be confounded when overlap is thin) |
| M_k9 … M_k35 | Unmatched abstention(conflict) − abstention(same) at each K (descriptive dose curve) |
| own_conflict, own_same | Median own margin of conflict and same trials |

## 5. Decision rules (exactly as in `run_p1g_graded.py`)

Primary point 3600. Holm over the three primary tests.

| Test | Comparison | Test type |
| --- | --- | --- |
| P1G_1 | M (probe A), PFATE vs PNOFATE | Paired sign test (DERIVED / HOST) |
| P1G_2 | M2_nn_own of PFATE against 0 | One-sample sign test (PRESENT / REVERSED / NOT_DETECTED; UNDETERMINED under the minimum count) |
| P1G_3 | M (probe A), PFATE vs PYOKED | Paired sign test (DERIVED / YOKED) |

**Validity** (P1e's): phase-1 clear correct ≥ 0.80; phase-1 accuracy under
the conflict probe ≤ 0.70; median PFATE natural conflict share at 3600
≥ 0.02.

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | P1G_1 UNDETERMINED |
| NOT_CONFIRMED | P1G_1 not DERIVED_AHEAD |
| MONITOR_SECOND_ORDER | P1G_1 DERIVED_AHEAD and P1G_2 PRESENT |
| MONITOR_FIRST_ORDER | P1G_1 DERIVED_AHEAD; P1G_2 NOT_DETECTED or REVERSED |
| MONITOR_ORDER_UNDETERMINED | P1G_1 DERIVED_AHEAD; P1G_2 UNDETERMINED |

**Flags:** weak (a needed test's Holm p > 0.05); thin (PFATE median
coverage_nn_own < 0.25); hardened (PFATE acc_conflict on probe A > 0.75).

**L0 arrow** from P1G_3: DERIVED_AHEAD → FATE_STRENGTHENS_MONITOR;
YOKED_AHEAD → FATE_SUBSTITUTES_FOR_MONITOR; NO_DIFFERENCE_DETECTED →
EXPOSURE_SUFFICES.

Secondaries (reported, not labelled): M_early PFATE vs PNOFATE; M PYOKED vs
PNOFATE; M2_nn_own PFATE vs PYOKED; M_conf_early; drain; regulation;
one-sample routes for M, M2_nn_own (EARLY, LATE), M2_nn_lda, M2_bins_own,
Q_early, nat_M and each M_k.

## 6. Readings

- **MONITOR_SECOND_ORDER:** at matched confidence a conflict still raises
  abstention. The agent's policy reads something about its own state that
  is not how sure it is of the content: the first candidate in this line
  for a self-model beyond first-order confidence (Layer 4). Not a claim of
  awareness. Checks: balance near 0; M2_nn_lda agreeing; EARLY and LATE.
- **MONITOR_FIRST_ORDER:** the monitor is confirmed and reads how ambiguous
  the content is. Layer 4 in its first-order form.
- **NOT_CONFIRMED:** P1e's descriptive monitor does not replicate with
  exposure fixed and graded damage.
- The L0 arrow is read as in P1e.

## 7. Expectations (written before calibration and any final seed)

Probabilities are my own.

| Outcome | Probability | Note |
| --- | --- | --- |
| Valid | 0.90 | Exposure is now set by design |
| P1G_1 DERIVED_AHEAD | 0.85 | P1e: 27/28 descriptively; graded damage could dilute it |
| P1G_2 PRESENT / NOT_DETECTED / REVERSED / UNDETERMINED | 0.30 / 0.55 / 0.05 / 0.10 | Stage 0 left a small EARLY residue (0.01) only |
| Overall SECOND_ORDER / FIRST_ORDER / ORDER_UNDET | 0.25 / 0.50 / 0.05 | |
| Overall NOT_CONFIRMED / UNDETERMINED / INVALID | 0.08 / 0.02 / 0.10 | |
| Thin | 0.15 | |
| L0 SUBSTITUTES / SUFFICES / STRENGTHENS | 0.35 / 0.55 / 0.10 | P1e: YOKED ahead 5/28 |
| M2_nn_lda has the same label as M2_nn_own | 0.65 | |
| Dose: M_k rises with K for PFATE (M_k35 > M_k9) | 0.80 | |
| Regulation, PFATE vs PYOKED, FATE_AHEAD | 0.80 | |
| Calibration freezes in round 1 | 0.60 | |

**Central expectation:** the monitor is confirmed and first-order; a
second-order signal is possible but less likely than not.

## 8. Seeds, outputs and run plan

- Final seeds 3200–3227 (28); calibration 10400–10423. Disjoint from every
  earlier runner (tested).
- Outputs `p1g_graded/`: raw.json, scores.json, REPORT.md, weights/,
  partial/, run.log. Batches of four seeds (`--max-new 4`), committed and
  pushed after each.
- Verification: source hashes against the freeze commit; `--score`
  reproduces REPORT.md; no errors in the log.

## 9. Limits and claim ceiling

- One task, one architecture (a 70-unit GRU), one damage type.
- "Second order" here means: at matched own report-logit gap (and LDA
  margin), the policy abstains more on a conflict. It does not mean a
  separate monitoring module or a representation that is about the first
  one in any richer sense.
- Graded damage changes the training distribution: the result is not a
  replication of P1e but a confirmation under a related design.
- No consciousness claim.

## 10. Safety

- Simulated variables only (X1–X5). The body, the damage and the probes are
  simulated; no real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
