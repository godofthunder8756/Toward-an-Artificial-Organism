# P1j protocol: does a content-free integrity variable causally set the agent's confidence? (Layer 4)

- **Status:** FROZEN (this commit), before any P1j measure is computed on P1i's
  seeds (3400–3427).
- **Follows:** [P1I_CALIB_RESULTS.md](P1I_CALIB_RESULTS.md)
  (CALIBRATED_DISCOUNT_CONFIRMED). Chosen by the PI ("Proceed with P1j",
  2026-11-26).
- Astra review waived by the PI. No consciousness claim.

## 0. Why this replaces the P1j proposed in P1i §8

P1i §8 proposed re-running the type-2 test against an evidence decoder trained
on conflict states too. On closer analysis that test cannot answer its
question, for two reasons.

- **The decoder would absorb the discount.** A decoder trained with the
  stored value as its target on conflict states learns the best posterior
  that can be read from the state. That posterior already includes any
  integrity discount. The agent's confidence would therefore fall to about
  0.5 against it under both accounts: an integrity cue, or a better read of
  the content.
- **The confidence is the agent's own decision variable.** The policy head
  is linear on the 70-unit state. The agent's confidence (own margin) is |z|,
  where z = logit(REP1) − logit(REP0), and its report is the sign of z. So
  its confidence always tells its own right from wrong reports better than
  an outside decoder can, whenever the two read the content differently.
  - P1i's type2_resid therefore shows that the damage-trained agent reads
    conflicted states differently from the clean decoder.
  - It is not metacognitive sensitivity beyond the agent's own evidence, as
    P1i §5 described it. An addendum to P1I_CALIB_RESULTS.md records this.
    P1i's declared result and label are unchanged.

The open question is causal and about organization. **Is there a component
of the agent's state that does not depend on the stored value (content-free),
that its dynamics produce after a conflict, and that turns its confidence in
the content down?** P1j tests this by intervention.

## 1. Design

Evaluation only, on saved weights at 3600, in fresh evaluation worlds
(stream tag EVAL_TAG_G + 40; P1g–P1i used EVAL_TAG_G).

- **The probe:** P1g's graded probe B, EARLY only. The overwrite comes at
  delay step 1 and the readout at step 9, so there are 8 recurrent updates
  in which the dynamics can act. K ∈ {9, 18, 26, 35}; no drain; clear
  trials.
- **Pass 1, estimation.** States are recorded at delay step S for none, same
  and conflict trials, and for none trials with unclear evidence.
  - c = mean(none | val 1) − mean(none | val 0): the content direction.
  - d_raw = the value-balanced conflict shift, the mean over val of
    [mean(conflict | val) − mean(same | val)].
  - a = the value-balanced ambiguity shift, from unclear vs clear none
    trials.
  - **d** = d_raw with its projection on span(c, a) removed. It is
    content-free and conflict-specific, not general ambiguity.
  - **r** = a random direction orthogonal to c, a and d, with the norm of d
    (the control).
- **Pass 2, intervention at natural size.** At delay step S, each targeted
  trial is assigned at random to one of three conditions: no push, the d
  push, or the r push.
  - Same and none trials get +d or +r; conflict trials get −d or −r.
  - The push is added to the state after the recurrent update, and the
    result is clipped to [−1, 1].
  - The state is carried forward and read out at step 9.
- **Pass 3, intervention at a fixed size.** As pass 2, with d and r rescaled
  to norm 1.0 (NORM_FIX). Each arm is pushed as hard along its own
  direction, so arms whose natural conflict shift is small can be compared.
- **Push steps:** S ∈ {3, 5, 7}; **S = 5 is primary.**
- **Value balance.** Every mean is the mean over val 0 and val 1 of the
  within-val means. A push that only shifts z by a constant, raising |z| for
  one value and lowering it for the other, therefore contributes nothing
  (tested).
- **Reproduction.** With no push, the P1j runner reproduces P1g's
  graded-probe collection exactly (tested). A zero push changes nothing
  (tested).

## 2. Measures (S = 5; passes 2 and 3)

| Measure | Definition | > 0 means |
| --- | --- | --- |
| **induce** | \|z\|(same, +r) − \|z\|(same, +d) | Adding d lowers confidence in an intact memory |
| **rescue** | \|z\|(conflict, −d) − \|z\|(conflict, −r) | Removing d restores confidence in a conflicted memory |
| **signed** | induce + rescue | d acts as a signed variable: more d means less confidence, less d means more |
| signed_fix, induce_fix, rescue_fix | The same at push norm 1.0 | |
| gap | \|z\|(same, none) − \|z\|(conflict, none) | The natural drop; induce_share and rescue_share are divided by it |
| induce_abs, rescue_abs | The same contrasts in exact abstention probability | |
| induce_none | Induce on undamaged (none) trials | |
| acc changes | Agent accuracy (+d) − (+r) on same trials, and (−d) − (−r) on conflict trials | Content preserved? |
| random_same, random_conflict | Effect of the random push against no push | |
| norm_d, share_d_kept, cosines | Properties of the direction | |

Why signed matters: an axis along which any displacement lowers confidence
gives induce > 0 and rescue < 0, so signed ≈ 0. Only a signed variable makes
both positive.

## 3. Decision rules (exactly as in `run_p1j_steer.py`)

| Test | Comparison | Type |
| --- | --- | --- |
| P1J_1 induce | induce of PFATE vs 0 | One-sample sign test → PRESENT / REVERSED / NOT_DETECTED |
| P1J_2 rescue | rescue of PFATE vs 0 | One-sample sign test |
| P1J_3 learned variable | signed, PFATE vs PNOFATE, natural size | Paired sign test → DERIVED_AHEAD / HOST_AHEAD / NO_DIFFERENCE_DETECTED |
| P1J_4 learned use | signed_fix, PFATE vs PNOFATE, push norm 1.0 | Paired sign test |

Labels use Holm-adjusted p over the four tests (α 0.05); UNDETERMINED
below the minimum count.

**Validity:** at least 20 seeds with a fitted primary run for PFATE and for
PNOFATE.

**Content confound:**

- **Induce:** if PFATE's accuracy on same trials under +d vs +r is REVERSED
  with a median drop of at least 0.02, induce is confounded.
- **Rescue:** if PFATE's accuracy on conflict trials under −d vs −r is
  PRESENT with a median gain of at least 0.02, rescue is confounded.

**Overall label:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | Any primary UNDETERMINED |
| CONTENT_CONFOUNDED | A PRESENT induce or rescue is confounded |
| NO_CAUSAL_SIGNAL | Neither P1J_1 nor P1J_2 PRESENT |
| ONE_WAY | Exactly one of P1J_1, P1J_2 PRESENT |
| CAUSAL_NOT_LEARNED | Both PRESENT, P1J_3 not DERIVED_AHEAD |
| LEARNED_VARIABLE_GENERIC_COUPLING | Both PRESENT, P1J_3 DERIVED_AHEAD, P1J_4 not |
| LEARNED_SIGNED_INTEGRITY_VARIABLE | All four |

**Secondaries** (reported, not labelled):

- induce, rescue, induce_fix and rescue_fix, PFATE vs PNOFATE;
- signed and induce, PFATE vs PYOKED (the L0 arrow);
- induce_abs, PFATE vs PNOFATE;
- norm_d, PFATE vs PNOFATE;
- one-sample routes per arm at S = 3, 5 and 7 for every measure in §2.

## 4. Readings

- **LEARNED_SIGNED_INTEGRITY_VARIABLE.**
  - The damage-trained agent's state carries a content-free variable,
    produced by its dynamics after a conflict, that causally sets its
    confidence in the content in both directions.
  - In a never-damaged net, an equally large push along its own conflict
    direction does not act as a signed variable.
  - Layer 4: a self-model variable (the integrity of its own memory) that is
    represented apart from the content and used for control (the confidence
    in that content). This is the strongest test in this line so far of a
    variable *about* the agent's own process rather than about the world.
    It is not a claim of awareness.
- **LEARNED_VARIABLE_GENERIC_COUPLING:** damage training creates the
  variable (its natural size), but how confidence couples to such a
  direction is generic to the architecture.
- **CAUSAL_NOT_LEARNED:** the never-damaged net shows the same causal
  pattern at natural size.
- **ONE_WAY / NO_CAUSAL_SIGNAL:** the content-free component does not set
  confidence (in one or both directions). P1i's discount would then run
  through value-signed (content) components: first-order in mechanism.

## 5. Discovery set (P1g's seeds 3200–3227, before this freeze)

Three runs, all disclosed and committed:

1. **[p1j_steer/discovery_v1/](p1j_steer/discovery_v1/REPORT.md)** used the
   first design, with natural-size pushes only and the learned test on
   induce at natural size. It showed that the never-damaged net's d is
   about 8 times smaller (0.17 vs 1.40), so its natural push is tiny.
   - I added pass 3 (fixed size) and moved the learned test onto it.
2. **[p1j_steer/discovery_v2/](p1j_steer/discovery_v2/REPORT.md)** showed:
   - at fixed size, induce does not differ between the arms (PFATE 0.23,
     PNOFATE 0.14, 16/28);
   - rescue goes the opposite way in PNOFATE (−0.17), so its d axis is
     sensitive in both directions rather than signed.
   - I then defined signed = induce + rescue, and made P1J_3 (natural size)
     and P1J_4 (fixed size) signed comparisons. **This choice was made after
     seeing v2.**
3. **[p1j_steer/discovery/](p1j_steer/discovery/REPORT.md)** is the final
   code: **LEARNED_SIGNED_INTEGRITY_VARIABLE**. Passes 1 and 2 are identical
   in all three runs; v2 and the final run add pass 3, and the scoring
   changed.

Medians at S = 5:

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| induce (gap share) | 0.39 (0.09) | 0.28 | −0.01 |
| rescue (gap share) | 0.65 (0.14) | 0.71 | 0.01 |
| signed / signed_fix | 0.98 / 0.60 | 0.94 / 0.66 | 0.02 / −0.02 |
| induce_fix / rescue_fix | 0.23 / 0.30 | 0.19 / 0.48 | 0.14 / −0.17 |
| gap (natural drop in \|z\|) | 4.30 | 4.07 | 1.72 |
| rescue_abs (gap_abs) | 0.065 (0.39) | 0.056 | 0.000 |
| norm_d (norm_c) | 1.40 (8.0) | 1.39 | 0.17 (3.4) |
| random_same | 0.17 | 0.18 | 0.01 |

Tests: P1J_1 21/28, P1J_2 26/28, P1J_3 24/28, P1J_4 20/28.

- Content is preserved: accuracy on same trials is at ceiling in every
  condition, and the conflict-trial change is 0.005, not detected.
- The pattern holds at S = 3 and S = 7: signed for PFATE is 0.80 and 0.89,
  and for PNOFATE 0.01 and 0.05.
- **Size:** d explains a modest part of the natural confidence drop (about
  9% by induce, 14% by rescue). Most of the drop runs through value-signed
  components, which this design does not intervene on.

## 6. Expectations (written after the discovery runs, before the confirmation)

| Outcome | Probability |
| --- | --- |
| Valid | 0.97 |
| P1J_1 PRESENT | 0.65 (weakest in discovery, 21/28) |
| P1J_2 PRESENT | 0.90 |
| P1J_3 DERIVED_AHEAD | 0.85 |
| P1J_4 DERIVED_AHEAD | 0.55 |
| Overall LEARNED_SIGNED_INTEGRITY_VARIABLE | 0.40 |
| Overall LEARNED_VARIABLE_GENERIC_COUPLING | 0.15 |
| Overall ONE_WAY | 0.25 |
| Overall CAUSAL_NOT_LEARNED / NO_CAUSAL_SIGNAL | 0.10 together |
| Overall CONTENT_CONFOUNDED / UNDETERMINED / INVALID | 0.10 together |
| signed, PFATE vs PYOKED: NO_DIFFERENCE_DETECTED | 0.75 |

## 7. Seeds, outputs, verification

- **Confirmation:** P1i's seeds 3400–3427 (weights in
  `p1i_calib/p1g_design/weights/`). No P1j measure has been computed on
  them.
  - They are fresh for this question, but not for P1i's measures; disclosed.
- Outputs go to `p1j_steer/confirm/` (raw.json, scores.json, REPORT.md,
  run.log).
- **Verification:**
  - source hashes match this freeze;
  - `--score p1j_steer/confirm` reproduces REPORT.md;
  - `score()` equals `scores.json`;
  - no errors in the log.

## 8. Limits

- A linear push into a non-linear recurrent net. The push is a direction
  estimated from average differences, so effects measure what that one
  direction does, not the full variable.
- Clipping to [−1, 1] makes the push slightly non-additive near saturation.
- The interventions act on content-free components only. The value-signed
  part of the discount is not intervened on, so the result bounds the
  integrity variable's share; it does not apportion the whole discount.
- One task, one architecture (a 70-unit GRU), one damage type.
- No consciousness claim.

## 9. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested
  in P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
