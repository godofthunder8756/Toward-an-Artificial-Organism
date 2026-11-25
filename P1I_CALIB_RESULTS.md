# P1i results: CALIBRATED_DISCOUNT_CONFIRMED on fresh seeds (Layer 4)

- **Protocol:** [P1I_CALIB_PROTOCOL.md](P1I_CALIB_PROTOCOL.md), frozen at
  commit 6f0a656 before the analysis touched any fresh seed.
- **Follows:** [P1H_EVIDENCE_RESULTS.md](P1H_EVIDENCE_RESULTS.md) (§2–3: a
  learned, calibrated integrity discount, found on P1g's seeds).
- **Run:** P1g's frozen design on 28 fresh seeds (3400–3427), in seven batches
  of four, each committed and pushed; then the frozen analysis
  (`run_p1i_calib.py --analyse`). Reports:
  [p1i_calib/confirm/REPORT.md](p1i_calib/confirm/REPORT.md) (P1i) and
  [p1i_calib/p1g_design/REPORT.md](p1i_calib/p1g_design/REPORT.md) (P1g
  replication).
- **Verification:**
  - All 23 source files (`I.SOURCES`) are byte-identical to the freeze.
  - `--score p1i_calib/confirm` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json` for P1i, and P1g's `score()` equals the
    replication's `scores.json`.
  - No error in either log.
- Nothing was run post hoc for this card. Astra review waived by the PI.
  **No consciousness claim.**

## 1. Declared result

**Overall: CALIBRATED_DISCOUNT_CONFIRMED.** Valid: the evidence decoder's
held-out accuracy for PFATE is 1.000 on none and 1.000 on same trials
(needed ≥ 0.95), and P1g's validity holds on the fresh seeds.

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1I_1 learned: M2_E, PFATE vs PNOFATE | 27/28 (0.064 vs 0.000) | < 0.0001 | DERIVED_AHEAD |
| P1I_2 calibrated: type2_resid, PFATE vs PNOFATE | 28/28 (0.628 vs 0.507) | < 0.0001 | DERIVED_AHEAD |
| P1I_3 warranted: rel_gap of PFATE vs 0 | 28/28 > 0 (median 0.071) | < 0.0001 | PRESENT |

The table below gives medians at 3600, from the mean of EARLY and LATE.

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| M2_E (abstention rise at matched evidence) | **0.064** | 0.054 | 0.000 |
| rel_gap (decoder right: matched same − conflict) | 0.071 | 0.063 | 0.182 |
| own_gap (report confidence: matched same − conflict) | 1.66 | 1.69 | 0.22 |
| type2_resid (error discrimination beyond evidence) | **0.628** | 0.671 | **0.507** |
| type2_resid_pabs (the same, with abstention as confidence) | 0.623 | 0.642 | 0.504 |
| type2_raw (own confidence, unstratified) | 0.804 | 0.823 | 0.700 |
| type2_ev_raw (evidence margin, unstratified) | 0.605 | 0.549 | 0.703 |
| trace_rho (conflict trace vs own margin, evidence partialled) | −0.60 | −0.58 | −0.17 |
| Accuracy on conflicts: agent / clean decoder | 0.816 / 0.779 | 0.821 / 0.785 | 0.723 / 0.725 |
| Pair coverage | 0.47 | 0.47 | 0.63 |

**Dose by damage size K**, medians:

| K (of 70 units) | 9 | 18 | 26 | 35 |
| --- | --- | --- | --- | --- |
| PFATE, abstention rise at matched evidence | 0.006 | 0.043 | 0.124 | 0.254 |
| PFATE, decoder right on matched conflicts | 0.997 | 0.981 | 0.898 | 0.508 |
| PNOFATE, abstention rise at matched evidence | 0.000 | 0.000 | 0.000 | 0.000 |
| PNOFATE, decoder right on matched conflicts | 0.972 | 0.893 | 0.766 | 0.509 |

PFATE's dose_rho is 1.00 (27/27 > 0), and every K level is present (26–27/28).

## 2. What was confirmed

- **Learned.** At the same evidence strength, a damage-trained agent abstains
  more on a conflicted memory than on a clean overwrite. A never-damaged net
  of the same architecture does not (27/28).
- **Warranted.** At the same evidence strength, a conflicted memory really is
  wrong more often (28/28). The discount tracks reliability across damage
  sizes: it is near zero where conflicted memories stay reliable (K 9) and
  largest where they fall to chance (K 35).
- **Calibrated, in the sense of protocol §9.** On conflict trials, within
  strata of evidence, the agent's own confidence separates the reports it
  gets right from those it gets wrong (0.628). In the never-damaged net it
  does not (0.507, at chance, 28/28 pairs). The abstention probability shows
  the same (0.623 vs 0.504).
  - Unstratified, the damage-trained agent's confidence (0.80) discriminates
    its errors better than the evidence margin does (0.61).
  - The never-damaged net's confidence is no better than the evidence
    (0.70 vs 0.70): it is the evidence, and nothing more.
- **The never-damaged net is overconfident on exactly the memories that
  deserve least trust.** At matched evidence its conflicted memories are
  even less reliable (rel_gap 0.18), and its confidence barely moves
  (own_gap 0.22).
- **The integrity trace is used.** At matched evidence, the stronger the
  state's conflict trace, the lower the agent's confidence (−0.60, against
  −0.17 in the never-damaged net; 27/28).

## 3. Against the discovery set and the expectations

The discovery set (P1g's seeds, protocol §5) is where the hypothesis came
from. On fresh seeds every primary holds and has the same sign, but the
effects are smaller:

| | Discovery (3200–3227) | Confirmation (3400–3427) |
| --- | --- | --- |
| M2_E, PFATE / PNOFATE | 0.0995 / 0.000 | 0.064 / 0.000 |
| rel_gap, PFATE / PNOFATE | 0.099 / 0.199 | 0.071 / 0.182 |
| type2_resid, PFATE / PNOFATE | 0.665 / 0.496 | 0.628 / 0.507 |
| own_gap, PFATE | 2.06 | 1.66 |
| trace_rho, PFATE / PNOFATE | −0.66 / −0.13 | −0.60 / −0.17 |
| dose_rho, PFATE | 1.00 | 1.00 |

The fresh-seed M2_E is about two-thirds of the discovery value, which fits
some selection on the discovery set. The confirmation figures are the ones to
quote.

| Outcome (protocol §7) | Expected | Observed |
| --- | --- | --- |
| Valid | 0.95 | Yes |
| CALIBRATED_DISCOUNT_CONFIRMED | 0.85 | Yes |
| DISCOUNT_CONFIRMED_NOT_CALIBRATED | 0.05 | No |
| Any of the other four labels | 0.10 | No |
| L0: M2_E PFATE vs PYOKED, NO_DIFFERENCE_DETECTED | 0.65 | Yes (15/28) |
| P1g replication: P1G_1 DERIVED_AHEAD | 0.95 | Yes (26/26) |
| P1g replication: P1G_2 PRESENT | 0.60 | Yes (23/25) |

## 4. P1g replication on the fresh seeds

[p1i_calib/p1g_design/REPORT.md](p1i_calib/p1g_design/REPORT.md) gives P1g's
frozen scoring at 3600. **The overall label is MONITOR_SECOND_ORDER, and the
L0 reading is EXPOSURE_SUFFICES**, the same as P1g.

| Test | P1g (3200–3227) | Replication (3400–3427) |
| --- | --- | --- |
| P1G_1 monitor, M PFATE vs PNOFATE | 28/28 (0.578 vs 0.001) | 26/26 (0.544 vs 0.002) DERIVED_AHEAD |
| P1G_2 M2_nn_own of PFATE | 25/27 (0.005) | 23/25 (0.005) PRESENT |
| P1G_3 L0 arrow, M PFATE vs PYOKED | 15/28 | 12/26 NO_DIFFERENCE_DETECTED |
| Regulation, in band PFATE vs PYOKED | 20/28 FATE_AHEAD | 23/28 FATE_AHEAD |

- The sign tests drop seeds where either value is missing or tied, as frozen,
  hence the n below 28.
- The dose in K replicates (M 0.03 / 0.19 / 0.42 / 0.55).
- P1G_2 replicates as declared. P1h showed that this residue is explained by
  the agent's own confidence plus a non-linear read of the evidence, so it
  carries no second-order claim. The replication does not change that.
- As in P1g, M2_nn_lda is not detected for PFATE at 3600.

## 5. Reading

- **The finding is now confirmatory.** An agent trained with damage to its
  own working memory learns a confidence that integrates a cue about the
  integrity of that memory. The cue is beyond the strength of the evidence
  for the content.
  - The discount is warranted, and it scales with how unreliable tampered
    memories are.
  - It makes the agent's confidence better at flagging its own errors than
    the evidence alone would.
  - A net that never met damage carries a weaker trace of the same event. It
    neither uses the trace nor calibrates on it, and it is overconfident.
- **In metacognition terms:** metacognitive sensitivity beyond evidence
  strength (type-2 discrimination above what the first-order evidence
  supports), acquired from exposure to damage. It lives inside the content
  confidence. P1h found no separate abstention channel, and P1i does not
  test for one.
- **Layer 4 (self-model).** The agent carries a variable about the state of
  its own memory process, not about the world, and uses it to weigh its own
  content. This is the most direct confirmed instance in the project of a
  self-model variable that is functionally used. It is not a claim of
  awareness.
- **Layer 0.** The precarious body is not needed. The yoked arm, with the
  same damage not tied to its body, shows the same discount (15/28) and the
  same calibration (type2_resid 0.671). Exposure to damage is what produces
  it, as in P1g and P1h.
- **Layer 1.** Regulation recruited by precarity replicates again (23/28).

## 6. Limits, and the main alternative

- **The evidence decoder never sees a conflict state.** "Beyond evidence"
  means beyond what a decoder trained on undamaged and same-overwrite states
  reads from the state.
  - The damage-trained agent reads the value from conflicted states slightly
    better than that decoder does (0.816 vs 0.779). The never-damaged net
    does not (0.723 vs 0.725).
  - So part of type2_resid could be a **better first-order read of damaged
    content**, learned from exposure, rather than an integrity cue as such.
  - The never-damaged control rules out the decoder's extrapolation alone,
    because the same decoder gives 0.507 there. It does not rule out this
    alternative, which comes from training on damaged states.
  - trace_rho favours the integrity reading: the conflict trace predicts the
    confidence drop at matched evidence. It does not exclude a mixture.
- "Calibrated" means better error discrimination beyond evidence, not
  numerical calibration. At K 35 the abstention rise (0.25) is smaller than
  the drop in reliability (to 0.51). The optimal amount depends on the
  payoff, which this card does not model.
- One task, one architecture (a 70-unit GRU), one damage type (overwrite by
  a donor state), 28 seeds.

## 7. Files

- `trackc_swap/calibdisc.py`, `run_p1i_calib.py`, `test_p1i_calib.py`
  (6 tests).
- `p1i_calib/p1g_design/`: P1g's outputs on the fresh seeds (raw.json,
  scores.json, the replication REPORT.md, run.log, partial/, weights/).
- `p1i_calib/discovery/`: the analysis on P1g's seeds, run before the freeze.
- `p1i_calib/confirm/`: raw.json, scores.json, REPORT.md, run.log.

## 8. Next step (for the PI; not authorized by this card)

**P1j: integrity cue or better content read?** Re-run the type-2 test with
an evidence decoder that is trained on conflict states too, cross-fitted on
the stored value. That is the best first-order read of damaged content
available from the state.

- If type2_resid stays above 0.5 for PFATE, and above PNOFATE, the cue is
  about integrity, not content.
- If it falls to 0.5, the damage-trained agent has learned to read damaged
  memories better, which is first-order.

This uses the saved weights from P1g and P1i (56 seeds), needs no training,
and can be pre-registered with the P1i seeds as confirmation.

Further options:

- Ablate or project out the trace direction, and test whether the discount
  and the type-2 gain go with it (causal).
- A second damage type (noise, or decay instead of overwrite), to test
  whether the cue generalizes across kinds of damage.

## 9. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested
  in P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
