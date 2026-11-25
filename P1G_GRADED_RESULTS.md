# P1g results: MONITOR_SECOND_ORDER (declared), small in size (Layer 0 → Layer 4)

- **Protocol:** [P1G_GRADED_PROTOCOL.md](P1G_GRADED_PROTOCOL.md), frozen at
  BASE_F 0.012 (commit ad5fe94) after one calibration round
  ([p1g_graded_calibration/RULES.md](p1g_graded_calibration/RULES.md)).
- **Follows:** [P1F_CONFIRM_RESULTS.md](P1F_CONFIRM_RESULTS.md) (stopped at
  calibration; stage 0 first-order in substance).
- **Run:** 28 final seeds (3200–3227), seven batches of four, each committed
  and pushed. Report: [p1g_graded/REPORT.md](p1g_graded/REPORT.md).
- **Verification:** the 18 source files hash-identical to the freeze;
  `--score p1g_graded` reproduces REPORT.md byte for byte; `score()` equals
  `scores.json`; no error in the log.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result (primary point 3600)

**Overall: MONITOR_SECOND_ORDER.** L0 reading: EXPOSURE_SUFFICES. Valid;
not weak, not thin, not hardened.

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1G_1, monitor: M (probe A), PFATE vs PNOFATE | 28/28 (0.578 vs 0.001) | < 0.0001 | DERIVED_AHEAD |
| P1G_2, second order: M2_nn_own of PFATE vs 0 | 25/27 > 0 (median 0.005) | < 0.0001 | PRESENT |
| P1G_3, L0 arrow: M, PFATE vs PYOKED | 15/28 (0.578 vs 0.581) | 0.85 | NO_DIFFERENCE_DETECTED |

Validity: phase-1 clear correct 0.999 (≥ 0.80); phase-1 accuracy under the
conflict probe 0.507 (≤ 0.70); PFATE natural conflict share 0.072 (≥ 0.02).

Main descriptive values at 3600 (medians over seeds):

| Arm | M | M_early | M_late | M2_nn_own | coverage_nn_own | balance_own | M2_nn_lda | M_k9 / k18 / k26 / k35 | In band |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PFATE | 0.578 | 0.745 | 0.440 | 0.004 | 0.422 | −0.003 | 0.002 | 0.028 / 0.193 / 0.444 / 0.606 | 0.930 |
| PYOKED | 0.581 | 0.699 | 0.494 | 0.004 | 0.421 | −0.003 | 0.003 | 0.015 / 0.160 / 0.423 / 0.574 | 0.889 |
| PNOFATE | 0.001 | 0.000 | 0.002 | 0.000 | 0.651 | −0.001 | 0.000 | 0.000 / 0.000 / 0.001 / 0.001 | 0.888 |

- **The monitor replicates**, now confirmatory: after a conflict in its own
  memory the agent abstains about 0.58 more than after a matched overwrite
  with the same value; the never-damaged net does not (28/28). P1e had
  0.557 against 0.002, descriptively.
- **Dose:** abstention after a conflict rises smoothly with the size of the
  damage (9 → 35 of 70 units: 0.03 → 0.19 → 0.44 → 0.61), every level
  28/28 > 0 for PFATE.
- **Second order (declared):** at matched own report-logit gap, a conflict
  raises abstention by a median **0.005** (EARLY 0.003, LATE 0.005), 25 of
  27 seeds. Present at 1800 too (20/28, 0.003). Coverage is good (0.42);
  the thin flag does not apply.
- **Size:** about 1% of M. At matched confidence the same trials almost
  never abstain (0.000), and the conflict trials do so on about 0.5% of
  trials. The effect is a rare abstention on confident conflicts, not a
  broad shift.
- **L0 arrow:** PYOKED, with the same damage not tied to its body, monitors
  as much (15/28) and shows the same second-order effect (PFATE vs PYOKED
  14/28). P1e's YOKED_AHEAD (5/28) does not replicate; exposure suffices.
- **Regulation (Layer 1):** PFATE keeps its body in band more than PYOKED
  (20/28, FATE_AHEAD), as in every earlier study.
- Not detected: Q_early (route), M_conf_early (undetermined: too few
  seeds with a value), drain effect (about 0.001 in every arm).

## 2. Post-hoc robustness (disclosed; written after seeing the report)

Stage 0 had taught that a coarse match can manufacture a second-order
effect from first-order confounding. [p1g_graded/posthoc/robust.py](p1g_graded/posthoc/robust.py)
re-collects the per-trial graded-probe data at 3600 from the saved weights
and the same evaluation streams. It reproduces the declared M2_nn_own
exactly (0 mismatches over 168 seed × arm × time runs). Two passes:
pass 1 ([robust_pass1.log](p1g_graded/posthoc/robust_pass1.log)), then
pass 2 ([robust.log](p1g_graded/posthoc/robust.log)) adding looser joint
calipers and the LDA margin alone, after pass 1 showed the joint match small
with lower coverage. Values: PFATE, mean of EARLY and LATE, median over
seeds.

| Check | M2 | Seeds > 0 | Against PNOFATE |
| --- | --- | --- | --- |
| Declared: own margin, caliper 0.05 SD | 0.0040 | 25/27 (p < 0.0001) | 26/28 |
| Own margin, caliper 0.01 SD | 0.0036 | 20/26 (p 0.009) | 23/28 |
| Own margin, minus the first-order bias from residual imbalance (local linear) | 0.0040 (bias 0.0000) | 25/28 | 26/28 |
| Own margin, same damage size K | 0.0036 | 23/27 (p 0.0003) | 24/28 |
| LDA margin alone, 0.05 SD | 0.0020 | 23/26 (p 0.0001) | 24/28 |
| Own and LDA margin jointly, 0.05 SD on each | 0.0008 | 17/24 (p 0.064) | 18/25 |
| Jointly, 0.1 SD | 0.0017 | 19/25 (p 0.015) | 20/26 |
| Jointly, 0.2 SD | 0.0019 | 23/27 (p 0.0003) | 22/27 |
| PNOFATE, declared | 0.0000 | 8/16 | — |

- **Unlike stage 0, the estimate does not shrink when the own-margin match
  is tightened** (0.0040 → 0.0036 at a five times tighter caliper; the
  imbalance bias is zero because abstention is flat at 0 among confident
  same trials). Holding the damage size equal leaves it unchanged.
- **Matching on a second readout of first-order confidence removes about
  half of it.** Matched on both the agent's own report gap and the LDA
  margin (how linearly decodable the value is from the whole state), about
  0.002 remains, consistent across seeds once coverage is restored (0.2 SD:
  coverage 0.42 EARLY, 0.24 LATE; 23/27). The drop at the 0.05 joint
  caliper was mostly lost power.
- The effect sits in the lowest own-margin third of the matched conflict
  trials (EARLY 0.010, LATE 0.009; upper thirds about 0).
- PYOKED behaves like PFATE on every check except EARLY, where its residue
  disappears under the LDA or joint match.
- A caveat on the LDA checks: the never-damaged net shows a tiny LDA-matched
  residue too (12/14 > 0, median 0.000), so the LDA match is not perfectly
  clean; the PFATE − PNOFATE contrast (24/28) is the safer reading.

## 3. Reading

- **Declared:** MONITOR_SECOND_ORDER. It stands by the frozen rule.
- **In substance:** the monitor is overwhelmingly first-order — it reads
  how ambiguous the content is, at a size set by the damage. Beyond that,
  there is a **small, robust residue**: at matched confidence on both
  readouts available here, a conflict makes the agent abstain on roughly
  0.2–0.4% more trials. It survives every tightening I could make, it is
  absent in the never-damaged net, and it does not depend on the body link.
- **What the residue is, and is not.** It shows that the policy uses
  something in its state that tracks "my memory was overwritten with a
  different value" beyond the two linear measures of how sure the state is
  of the content. Half of the own-margin effect is accounted for by the
  richer (LDA) first-order measure, so the remaining half may also be
  first-order information in a non-linear form that neither margin
  captures. This design cannot exclude that. "Second order" here means only
  what protocol §9 says.
- **Layer reading:** Layer 4 in its first-order form, now confirmed under
  fixed exposure, with a dose-response to damage size. A first candidate,
  small and qualified, for a signal beyond first-order confidence. Layer 0
  does not shape it: exposure to damage, not a precarious body, produces the
  monitor (P1e's YOKED_AHEAD did not replicate; no difference here). Layer
  1: regulation recruited by precarity replicates again.

## 4. Against the expectations (protocol §7, written before calibration)

| Outcome | Expected | Observed |
| --- | --- | --- |
| Valid | 0.90 | Yes |
| P1G_1 DERIVED_AHEAD | 0.85 | Yes, 28/28 |
| P1G_2 PRESENT / NOT_DETECTED / REVERSED / UNDET | 0.30 / 0.55 / 0.05 / 0.10 | PRESENT (the less likely outcome) |
| Overall SECOND / FIRST / ORDER_UNDET | 0.25 / 0.50 / 0.05 | SECOND_ORDER; the central expectation (first-order) was wrong by the declared rule, though right about the bulk of the effect |
| Thin | 0.15 | No (0.42) |
| L0 SUBSTITUTES / SUFFICES / STRENGTHENS | 0.35 / 0.55 / 0.10 | SUFFICES |
| M2_nn_lda same label as M2_nn_own | 0.65 | Yes (PRESENT, 23/26) |
| Dose: M_k35 > M_k9 | 0.80 | Yes, monotone over the four levels |
| Regulation FATE_AHEAD | 0.80 | Yes, 20/28 |
| Freeze in round 1 | 0.60 | Yes |

## 5. Limits

- One task, one architecture (a 70-unit GRU), one damage type; 28 seeds.
- The second-order effect is about 1% of the first-order one, and half of it
  is explained by a second linear readout of confidence. A non-linear
  first-order readout could explain the rest.
- Graded damage changes the training distribution: this confirms P1e's
  monitor under a related design, not a replication of P1e's exact setup.
- §2 is post-hoc and exploratory; its p-values are not corrected and carry
  no declared weight.

## 6. Files

- `trackc_swap/gradmon.py`, `run_p1g_graded.py`, `test_p1g_graded.py` (11
  tests).
- `p1g_graded_calibration/` (RULES.md; round1/).
- `p1g_graded/`: raw.json, scores.json, REPORT.md, run.log, partial/,
  weights/ (1800 and 3600, all arms).
- `p1g_graded/posthoc/`: robust.py, robust_pass1.log, robust_pass1.json,
  robust.log, robust.json.

## 7. Possible next steps (for the PI; not authorized by this card)

- **Is the residue first-order in a non-linear form?** Match on a
  non-linear decoder's confidence (a small MLP read-out of the value from
  the state, cross-fitted). If the residue survives, it is the strongest
  candidate in this line for a signal about the agent's own state rather
  than its content. Cheap: the weights are saved.
- **Where is the residue in the state?** Ablate or project out the
  directions that predict a conflict at matched confidence, and see whether
  the abstention residue goes with them.
- **The Layer 1 finding as its own study** (from P1f): is the held exposure
  level a set point?

## Forward note (2026-11-25): P1h

[P1H_EVIDENCE_RESULTS.md](P1H_EVIDENCE_RESULTS.md):
- **The residue:** with the exact abstention probability and a joint match on
  own margin and a cross-fitted non-linear evidence decoder, it is 0.0007.
  That is within the method's leak range, so no second-order claim.
- **The LDA checks in §2** rest on a margin that leaks on conflict states;
  they are superseded.
- **What the monitor reads:** at matched evidence alone, the damage-trained
  agent discounts its confidence on conflicts (abstention +0.10). The
  discount is calibrated to how reliable such memories actually are, and the
  never-damaged net shows none.

## 8. Safety

- Simulated variables only (X1–X5). The body, the damage and the probes are
  simulated; no real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
