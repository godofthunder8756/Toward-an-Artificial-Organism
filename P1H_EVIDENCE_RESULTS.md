# P1h results: no signal beyond the agent's own confidence; a learned, calibrated integrity discount inside it (Layer 4)

- **Protocol:** [P1H_EVIDENCE_PROTOCOL.md](P1H_EVIDENCE_PROTOCOL.md), frozen
  (commit 47d17dd) before any P1h measure was computed.
- **Follows:** [P1G_GRADED_RESULTS.md](P1G_GRADED_RESULTS.md).
- **Run:** stage 1 on P1g's saved weights (seeds 3200–3227, 3600 updates).
  Report: [p1h_evidence/stage1/REPORT.md](p1h_evidence/stage1/REPORT.md).
- **Verification:**
  - P1g's declared M2_nn_own is reproduced exactly from the re-collected data
    (0 mismatches over 168 runs).
  - Source files are identical to the freeze, and `score()` equals
    `scores.json`.
  - `--score` reproduces REPORT.md apart from its title line: the `--score`
    path prints a shorter title, and the frozen runner was left unchanged.
  - No error in the log.
- **Stage 2 did not run:** the gate (§5) requires the residue to lie outside
  the leak range.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: SECOND_ORDER_SURVIVES, within the leak range.** Valid; not thin.
Under the gate, P1h ends at stage 1.

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1H_1: M2_joint_p of PFATE vs 0 (matched on own margin and evidence) | 24/28 > 0, median **0.0007** | 0.0004 | PRESENT |
| P1H_2: M2_joint_p, PFATE vs PNOFATE | 24/28 (0.0007 vs −0.0000) | 0.0004 | DERIVED_AHEAD |

- **Size.** The residue is 0.22% of PFATE's unmatched conflict–same gap in
  abstention probability (0.309). That is below 0.5%, the largest leak of the
  joint match in the synthetic first-order-only controls (rounded up).
  - The method cannot tell this residue from its own leak, so I make no
    second-order claim from it.
- **The reading of P1g's residue.** Beyond the agent's own report confidence,
  matched together with a non-linear read of the evidence, nothing above the
  method's resolution remains.
  - P1g's M2_nn_own was 0.004 with sampled abstention. With the exact
    abstention probability, own margin alone gives 0.0019; adding the
    evidence match brings it to 0.0007.

## 2. The larger finding: matched on evidence alone (pre-registered secondary)

Medians at 3600, mean of EARLY and LATE.

| Arm | M2_E | M2_E, sampled | M2_E, alternative decoder | Trace AUC | Trace, evidence-matched pairs | p_abs conflict / same |
| --- | --- | --- | --- | --- | --- | --- |
| PFATE | **0.0995** (28/28) | 0.099 (28/28) | 0.100 (28/28) | 0.95 | 0.88 | 0.309 / 0.001 |
| PYOKED | 0.074 (28/28) | 0.079 | 0.086 | 0.96 | 0.90 | 0.297 / 0.001 |
| PNOFATE | 0.000 (15/28) | 0.000 | 0.000 | 0.78 | 0.64 | 0.001 / 0.000 |

- **The comparison.** At matched evidence strength, read non-linearly by a
  decoder that never saw a conflict, the damage-trained agent abstains about
  0.10 more on a conflict.
  - That is a third of its whole conflict–same gap.
  - The never-damaged net shows nothing.
- **Where the effect lives.** Matching on the agent's own report gap as well
  removes it (§1), so the effect runs through the agent's own confidence.
  - The agent's report confidence is lower on conflicts than the evidence
    strength warrants.
- **A trace at matched evidence.** Even at matched evidence, the state
  carries a strong trace that a conflict happened (pair AUC 0.88).
  - That trace is much weaker in the never-damaged net (0.64): damage training
    amplifies it.

## 3. Post-hoc: is the discount warranted? (disclosed; written after seeing the report)

[p1h_evidence/stage1/posthoc/calib.py](p1h_evidence/stage1/posthoc/calib.py)
re-collects the same data and reproduces M2_E exactly (0 mismatches). It uses
the evidence-matched conflict–same pairs, and the median over seeds
([calib.log](p1h_evidence/stage1/posthoc/calib.log)).

| | PFATE early | PFATE late | PNOFATE early | PNOFATE late |
| --- | --- | --- | --- | --- |
| Clean decoder correct, conflict vs matched same | 0.88 vs 1.00 (28/28) | 0.92 vs 1.00 (27/28) | 0.76 vs 1.00 (28/28) | 0.84 vs 1.00 (28/28) |
| Agent's own margin, conflict vs matched same | 9.7 vs 11.5 (27/28) | 9.1 vs 11.2 (28/28) | 9.4 vs 9.4 (20/28) | 8.4 vs 8.8 (20/28) |
| Abstention rise at matched evidence (M2_E) | 0.106 | 0.089 | 0.000 | 0.000 |
| Trace score vs own margin at matched evidence (rank correlation) | −0.60 (27/28) | −0.71 (28/28) | −0.00 | −0.19 |
| Agent vs clean decoder, accuracy on all conflicts | 0.80 vs 0.75 (25/28) | 0.83 vs 0.81 (21/27) | 0.69 vs 0.69 | 0.75 vs 0.76 |

Dose by damage size K (PFATE, EARLY | LATE):

| K (of 70 units) | 9 | 18 | 26 | 35 |
| --- | --- | --- | --- | --- |
| Clean decoder correct on matched conflicts | 0.995 \| 1.000 | 0.945 \| 0.994 | 0.821 \| 0.904 | 0.503 \| 0.508 |
| Abstention rise at matched evidence | 0.006 \| 0.009 | 0.070 \| 0.063 | 0.187 \| 0.224 | 0.294 \| 0.398 |

- **The discount is warranted.** At the same evidence strength, a conflicted
  memory is wrong more often. The never-damaged net's conflicted memories are
  even less reliable.
  - So evidence strength alone overstates how far a tampered memory can be
    trusted.
- **The damage-trained agent discounts for it, in proportion.**
  - Its confidence and its abstention fall where reliability falls, and grow
    with the damage size.
  - Its integrity trace predicts the confidence drop at matched evidence.
  - It also reads the value from conflicted states better than the clean
    decoder does.
- **The never-damaged net does not discount.** Its confidence barely moves
  and its abstention does not change: it is overconfident on exactly the
  memories that deserve least trust.
  - Damage training is what produces the calibrated discount.
- **PYOKED** behaves like PFATE, so the precarious body is not needed: the
  discount comes from exposure to damage.

## 4. Reading

- **Second order in P1h's strict sense** (beyond the agent's own
  confidence): not resolved above the method's leak. The agent has no
  separate abstention channel that reads its memory's integrity apart from
  its confidence.
- **What the agent does have** is a confidence that integrates an integrity
  cue. Its belief in the content is discounted by a learned signal that the
  memory was tampered with, and the discount is calibrated: it scales with
  how unreliable such memories actually are.
  - A net that never met damage carries a weaker version of the same trace
    but neither uses nor calibrates on it.
  - In the metacognition literature this is confidence that uses cues beyond
    the evidence for the decision (cue integration). It is not a separate
    monitor.
- **Layer 4:** a sharper and stronger result than P1g's. The self-monitor is
  first-order in where it acts, since it lives in the content confidence. In
  what it reads, it goes beyond the evidence: an integrity cue about the
  agent's own memory, learned from exposure and calibrated to how reliable
  that memory is.
  - This is post-hoc characterization of a pre-registered secondary on a
    discovery set. It needs confirmation on fresh seeds before it counts.
- **Layers 0 and 1:** as in P1g. Exposure, not the body link, produces the
  discount.

## 5. Against the expectations (protocol §7)

| Outcome | Expected | Observed |
| --- | --- | --- |
| Stage 1 valid | 0.95 | Yes |
| SURVIVES / EXPLAINED / NOT_SPECIFIC / UNDET-INVALID | 0.40 / 0.45 / 0.10 / 0.05 | SURVIVES |
| Within the leak range, given SURVIVES | 0.35 | Yes |
| Stage 2 runs | 0.25 | No |
| trace_pair_auc above 0.5 for PFATE | 0.85 | Yes (0.88, 28/28) |
| M2_E_sampled agrees in sign with M2_joint_p | 0.75 | Yes |

The central expectation ("the state carries a conflict trace; its use beyond
the evidence is at the edge of what this method can resolve") held for the
strict test. I did not anticipate how large the discount at matched evidence
alone would be (0.10).

## 6. A correction to P1g

The synthetic controls (P1h protocol §2) show that the LDA margin, fitted on
undamaged trials only, leaks badly on conflict states (0.02 in absolute
abstention). The LDA-based checks in P1G_GRADED_RESULTS.md §2 (that matching
also on LDA "removes about half" of the residue) therefore rest on a leaky
measure. P1h supersedes them: with the exact abstention probability and the
joint match on own margin and a cross-fitted non-linear decoder, the residue
is 0.0007.

## 7. Limits

- Stage 1 only: a discovery set, P1g's seeds. §2–3 have not been confirmed on
  fresh seeds.
- The evidence decoder never sees conflict states and must extrapolate to
  them. Its accuracy on conflicts (0.75–0.81) is close to the agent's, and
  the alternative decoder and the sampled-abstention version agree, but its
  exact margin on conflicts is not guaranteed.
- One task, one architecture, one damage type.

## 8. Files

- `trackc_swap/evidence.py`, `run_p1h_evidence.py`, `test_p1h_evidence.py`
  (8 tests, including the synthetic controls).
- `p1h_evidence/stage1/`: raw.json, scores.json, REPORT.md, run.log;
  `posthoc/` (calib.py, calib.log, calib.json).

## 9. Next step (for the PI; not authorized by this card)

**P1i: confirm the calibrated integrity discount on fresh seeds.** Primary
measures fixed before training:

- M2_E for PFATE vs PNOFATE;
- the reliability gap at matched evidence;
- the dose by K.

The calibration claim would be tested directly: the agent's discount should
track per-K reliability, and the never-damaged net should be overconfident.
This uses P1h's stage-2 machinery: 28 seeds, about 5 hours of training.

## 10. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world. The
  operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
