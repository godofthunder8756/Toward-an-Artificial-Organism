# P1i protocol: confirmation of the calibrated integrity discount on fresh seeds (Layer 4)

- **Status:** FROZEN (this commit), before the analysis is run on any of the
  fresh seeds.
- **Follows:** [P1H_EVIDENCE_RESULTS.md](P1H_EVIDENCE_RESULTS.md): at
  matched evidence the damage-trained agent discounts its confidence on
  conflicted memories, in proportion to how unreliable they are; the
  never-damaged net does not. Found on P1g's seeds (a pre-registered secondary
  plus post-hoc characterization). Chosen by the PI ("Proceed with P1i",
  2026-11-25).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

On fresh seeds, does an agent trained with damage to its working memory:

1. **learn** to lower its confidence on a conflicted memory beyond what the
   evidence strength says (against a never-damaged net)?
2. do so **with warrant**: is a conflicted memory actually less reliable at
   the same evidence strength?
3. do so **calibrated**: does its confidence on conflicted memories separate
   its own right from wrong reports better than evidence strength alone does,
   and better than in a never-damaged net?

## 2. Design

- **Training:** P1g's frozen design exactly (`run_p1g_graded.run_jobs`,
  BASE_F 0.012, graded damage K ∈ {9, 18, 26, 35} of 70, three arms) on 28
  fresh seeds, 3400–3427, into `p1i_calib/p1g_design/`. This also yields a
  replication of P1g's declared tests (P1G_1–3), reported.
  - Disclosed ordering: training started (commit c8c9349) before the analysis
    was written. Training is P1g's frozen code and does not depend on the
    analysis. No measure from these seeds, including the P1g evaluation the
    training writes per seed, was looked at before this freeze.
- **Analysis** (`trackc_swap/calibdisc.py`, run by `run_p1i_calib.py
  --analyse`): at 3600, P1g's graded probe B re-collected exactly
  (`evidence.collect_graded`), EARLY and LATE; per seed and arm, the mean over
  the runs that have a value.
  - **Evidence:** P1h's cross-fitted MLP decoder of the stored value, trained
    on none and same trials only (it never sees a conflict); margin |logit|.
  - **Evidence-matched pairs:** each conflict trial against its nearest same
    trial in evidence margin, caliper 0.05 pooled SD, at least 20 pairs.

## 3. Measures

| Measure | Definition |
| --- | --- |
| **M2_E** | Mean exact abstention probability p_abs(conflict) − p_abs(matched same) |
| **rel_gap** | Decoder accuracy on matched same − on conflict (is a conflicted memory less reliable at the same evidence?) |
| **type2_resid** | On conflict trials: AUC of the agent's report confidence (own margin) for its report head's right vs wrong, within 10 evidence-quantile strata, after removing the linear trend on evidence inside each stratum; weighted n_right × n_wrong (strata with at least 5 of each). 0.5 = confidence knows nothing about its own errors beyond the evidence |
| own_gap | Own margin, matched same − conflict |
| type2_raw, type2_ev_raw | Unstratified type-2 AUC of own margin, and of the evidence margin |
| type2_resid_pabs | type2_resid with −p_abs as the confidence |
| trace_rho | Rank correlation on matched conflicts, evidence partialled, of a cross-fitted conflict-vs-same classifier score with own margin |
| M2_E_k, rel_k, dose_rho | Per K; dose_rho = rank correlation of M2_E_k with K |

**Controls** (`test_p1i_calib.py`, synthetic):

- **type2_resid:** gives 0.49–0.51 when confidence is a linear or non-linear
  function of evidence, and 0.66–0.68 when confidence also carries an integrity
  variable that predicts errors.
  - Without the within-stratum detrending, a purely first-order confidence
    scored 0.535. That was found by the test and fixed before the discovery
    run.
- **M2_E:** recovers a planted effect (P1h's controls).

## 4. Decision rules (exactly as in `run_p1i_calib.py`)

| Test | Comparison | Type |
| --- | --- | --- |
| P1I_1 learned | M2_E, PFATE vs PNOFATE | Paired sign test → DERIVED_AHEAD / HOST_AHEAD / NO_DIFFERENCE_DETECTED |
| P1I_2 calibrated | type2_resid, PFATE vs PNOFATE | Paired sign test |
| P1I_3 warranted | rel_gap of PFATE vs 0 | One-sample sign test → PRESENT / REVERSED / NOT_DETECTED |

Labels use Holm-adjusted p over the three tests (α 0.05); UNDETERMINED
under the minimum count.

**Validity:**

- PFATE median held-out decoder accuracy ≥ 0.95 on none and on same trials;
- P1g's validity on the fresh seeds (phase-1 memory and damage effect,
  exposure ≥ 0.02).

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | Any primary UNDETERMINED |
| NOT_CONFIRMED | P1I_1 not DERIVED_AHEAD |
| DISCOUNT_UNWARRANTED | P1I_1 DERIVED_AHEAD, P1I_3 not PRESENT |
| DISCOUNT_CONFIRMED_NOT_CALIBRATED | P1I_1 DERIVED_AHEAD, P1I_3 PRESENT, P1I_2 not DERIVED_AHEAD |
| CALIBRATED_DISCOUNT_CONFIRMED | All three |

**Secondaries** (reported, not labelled):

- M2_E PFATE vs PYOKED (the L0 arrow), and PYOKED vs PNOFATE;
- type2_resid PYOKED vs PNOFATE;
- type2_resid_pabs PFATE vs PNOFATE;
- own_gap PFATE vs PNOFATE;
- trace_rho (PFATE more negative than PNOFATE);
- one-sample routes for M2_E, rel_gap, own_gap, dose_rho, each M2_E_k, and
  type2 measures against 0.5;
- the P1g replication.

## 5. Discovery set (P1g's seeds 3200–3227, same code; run before this freeze)

[p1i_calib/discovery/REPORT.md](p1i_calib/discovery/REPORT.md):
**CALIBRATED_DISCOUNT_CONFIRMED**.

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| M2_E | 0.0995 | 0.0743 | 0.0000 |
| rel_gap | 0.0986 | 0.0747 | 0.1991 |
| type2_resid | 0.665 | 0.666 | 0.496 |
| own_gap | 2.06 | 1.75 | 0.24 |
| trace_rho | −0.66 | −0.54 | −0.13 |
| dose_rho | 1.00 | 1.00 | 0.30 |

- All three primaries are 28/28 in this set.
- The never-damaged net's conflicted memories are *less* reliable (rel_gap
  0.20), yet its confidence knows nothing about its errors beyond the
  evidence (0.496).
- This is the set the hypothesis came from. It sets the expectations below;
  it is not evidence for the confirmation.

## 6. Readings

- **CALIBRATED_DISCOUNT_CONFIRMED:** a learned, warranted and calibrated
  integrity discount.
  - The agent's confidence in a memory integrates a cue that the memory was
    tampered with, beyond the evidence, and that cue makes its confidence
    better at flagging its own errors.
  - In metacognition terms: metacognitive sensitivity beyond evidence
    strength, acquired from exposure to damage.
  - Layer 4 in the self-model sense: a variable about the agent's own memory
    process, used to weigh its own content. Not a claim of awareness.
- **DISCOUNT_CONFIRMED_NOT_CALIBRATED:** the discount is learned and
  warranted, but it does not improve the agent's error discrimination beyond
  evidence.
- **DISCOUNT_UNWARRANTED / NOT_CONFIRMED:** the P1h finding does not hold on
  fresh seeds.

## 7. Expectations (written after the discovery run, before the confirmation)

| Outcome | Probability |
| --- | --- |
| Valid | 0.95 |
| CALIBRATED_DISCOUNT_CONFIRMED | 0.85 |
| DISCOUNT_CONFIRMED_NOT_CALIBRATED | 0.05 |
| NOT_CONFIRMED / UNWARRANTED / UNDETERMINED / INVALID | 0.10 together |
| L0: M2_E PFATE vs PYOKED NO_DIFFERENCE_DETECTED | 0.65 |
| P1g replication: P1G_1 DERIVED_AHEAD | 0.95 |
| P1g replication: P1G_2 PRESENT | 0.60 |

## 8. Seeds, outputs, run plan

- Fresh seeds 3400–3427, disjoint from every earlier runner including P1h's
  reserved stage-2 seeds (tested).
- Training in batches of four, committed and pushed after each.
- `p1i_calib/p1g_design/` (P1g's outputs and weights, P1g replication
  REPORT.md); `p1i_calib/confirm/` (raw.json, scores.json, REPORT.md,
  run.log); `p1i_calib/discovery/`.
- Verification: source hashes against this freeze; `--score` reproduces
  REPORT.md; no errors in the logs.

## 9. Limits

- One task, one architecture (70-unit GRU), one damage type (overwrite by a
  donor state).
- The evidence decoder never sees conflict states and extrapolates to them
  (P1h §7). The type-2 measure does not depend on it except through the
  strata.
- "Calibrated" here means better error discrimination beyond evidence, not
  numerical calibration of probabilities.
- No consciousness claim.

## 10. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested
  in P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
