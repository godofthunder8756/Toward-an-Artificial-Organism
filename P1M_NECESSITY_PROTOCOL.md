# P1m protocol (Q-NECESSITY): does the integrity variable add value for the agent against the strongest simpler rival? (Layer 4)

- **Status:** FROZEN (this commit), before any P1m measure is computed on P1i's
  seeds (3400–3427).
- **Follows:** [P1L_ACCESS_RESULTS.md](P1L_ACCESS_RESULTS.md). Chosen by the
  PI ("Proceed with Q-Necessity", 2026-11-26).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

The constitution ([ACI_RESEARCH_CONSTITUTION_v3.md](ACI_RESEARCH_CONSTITUTION_v3.md))
credits a building block only on Q-NECESSITY: *what does it add against the
strongest simpler rival with matched information, experience and substrate?*
A lesion establishes use, not necessity, and no oracle may be passed off as
the agent's own.

P1h–P1l described the damage-trained agent's integrity variable:

- content-free and causal on confidence (P1j);
- general across kinds of damage (P1k);
- shared with a second consumer (P1l).

Does it earn anything for the agent, in the agent's own currency, that a
simpler agent with the same information could not?

## 2. Design

Evaluation only, on saved weights at 3600, in fresh evaluation worlds
(EVAL_TAG_G + 120). Setting: the EARLY graded probe, clear undrained trials.

- **Currency:** the probe's payoff, the one the agents were trained on.
  - A correct report earns +1, a wrong report −4, an abstention 0.
  - Reporting pays only above 0.8 reliability.
- **Lesion (online).**
  - Pass R records the state at every step from the damage (delay step 1)
    to the readout (step 9).
  - Per step t: P1j's direction d_t (value-balanced conflict − same shift,
    with the content and ambiguity directions removed) and μ_t, the
    undamaged trials' mean coordinate on d_t.
  - In the lesion pass, at every step and for every trial, the coordinate on
    d_t is clamped to μ_t (after the update and the damage; clipped to
    [−1, 1]).
  - Weights, experience, content read and every other direction are
    unchanged (tested).
- **Values at the readout:**
  - **As used:** the mean expected payoff of the agent's own policy,
    p(report the value) − 4 · p(report the other).
  - **Thresholded, V\*:** the payoff of "report sign(z) if |z| > τ, else
    abstain". τ is chosen on one half of the trials and scored on the other
    (two-fold cross-fitted; a grid of 101 quantiles, plus never and always
    report). z is the agent's own report logit gap.
- **The strongest simpler rival:** the lesioned agent with its threshold
  re-tuned, V\*(lesion).
  - It is the same network, experience, content read and information
    channel, as cautious as pays, but without the selective integrity signal.
  - A uniformly more cautious agent is the simplest explanation of any value
    from caution.
- **The supplied oracle (EXTERNAL; a bound, never a rival):** the lesioned
  agent's |z| with a supplied damage flag and damage size K, thresholds per
  flag × K: V\*(lesion + oracle).
  - **room** = V\*(lesion + oracle) − V\*(lesion). If the oracle adds no
    detectable value, the task leaves integrity information nothing to earn,
    and necessity is not testable in it.
  - **recovery** = (V\*(intact) − V\*(lesion)) / room.
- **Mixes:**
  - **probe mix:** none, same and conflict about a third each;
  - **natural mix:** reweighted to training exposure (conflict 0.072, same
    0.072, none 0.856);
  - also a stricter payoff (wrong −9; secondary).
- **Other damage:** the novel operators (scramble, noise, zero) with the same
  lesion; secondary.

## 3. Decision rules (exactly as in `run_p1m_necessity.py`)

Holm over the three tests (α 0.05), all on the probe mix and trained damage:

| Test | Comparison | Type |
| --- | --- | --- |
| P1M_1 value against the strongest simpler rival | dV\* = V\*(intact) − V\*(lesion), PFATE | One-sample sign test → PRESENT / REVERSED / NOT_DETECTED |
| P1M_2 value as used | dV = V(intact policy) − V(lesioned policy), PFATE | One-sample sign test |
| P1M_3 learned value | dV\*, PFATE vs PNOFATE | Paired sign test → DERIVED_AHEAD / HOST_AHEAD / NO_DIFFERENCE_DETECTED |

**Validity:** at least 20 seeds fitted for PFATE and PNOFATE.

**Room:** the room test for PFATE is PRESENT (unadjusted) with a median of at
least 0.005.

**Content confound:** the lesion lowers PFATE's accuracy on conflict or
undamaged trials (intact − lesion PRESENT, median ≥ 0.02).

**Overall:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | Any primary UNDETERMINED |
| CONTENT_CONFOUNDED | P1M_1 PRESENT, and content confounded |
| VALUE_CREDITED | P1M_1 PRESENT, P1M_3 DERIVED_AHEAD, P1M_2 PRESENT |
| VALUE_CREDITED_NOT_AS_USED | As VALUE_CREDITED, but P1M_2 not PRESENT |
| VALUE_NOT_LEARNED | P1M_1 PRESENT, P1M_3 not DERIVED_AHEAD |
| NECESSITY_NOT_TESTABLE | P1M_1 not PRESENT, and no room (`_USED` added if P1M_2 PRESENT) |
| USED_NOT_NECESSARY | P1M_1 not PRESENT, room present, P1M_2 PRESENT |
| VARIABLE_COSTLY | P1M_1 REVERSED |
| NO_VALUE_DETECTED | Otherwise |

**Secondaries** (reported, not labelled):

- dV, PFATE vs PNOFATE; dV\*, PFATE vs PYOKED; V\*(intact), PFATE vs PNOFATE;
- routes per arm and damage type: dV\*, dV and room (probe mix, natural mix,
  strict payoff), recovery, per-group changes in payoff, accuracy changes.

## 4. Readings

- **VALUE_CREDITED.**
  - The agent's own integrity variable earns payoff that the strongest
    simpler rival — the same agent, as cautious as pays, without the
    variable — cannot.
  - The value is learned: in the never-damaged net, removing its
    counterpart earns less.
  - The building block passes Q-NECESSITY in this task, and can be credited
    as SUPPORTED_BOUNDED under the constitution.
- **USED_NOT_NECESSARY:** the agent relies on the variable, but a re-tuned,
  uniformly cautious agent does as well. Use without necessity.
- **NECESSITY_NOT_TESTABLE:** the task gives integrity information no room
  to earn; this design cannot settle necessity.
- **VALUE_NOT_LEARNED:** removing the never-damaged net's counterpart costs
  as much.
  - Caveat: that net's directions are mostly noise, and lesioning them
    slightly harms its content. In discovery its accuracy on damaged trials
    fell by 0.004–0.007. This inflates its dV\* and makes P1M_3
    conservative against the claim.

## 5. Discovery set (P1g's seeds 3200–3227, before this freeze)

- A one-seed smoke check (seed 3200) was seen before the room check was
  added. It showed that a supplied flag could add little in this task, which
  led to the room check and the NOT_TESTABLE and USED_NOT_NECESSARY labels.
- The code was then committed (30a5dd1) and discovery was run once; nothing
  was changed after it.
- [p1m_necessity/discovery/REPORT.md](p1m_necessity/discovery/REPORT.md):
  **VALUE_CREDITED.**

Medians, trained damage (donor), probe mix:

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| V\*(intact) / V\*(lesion) | 0.809 / 0.758 | 0.813 / 0.775 | 0.646 / 0.602 |
| dV\* (strongest-rival test) | **0.048** (27/28) | 0.040 | 0.022 |
| room (supplied oracle) / recovery | 0.077 / 0.60 | — / 0.47 | 0.113 / 0.19 |
| dV as used | **0.094** (28/28) | 0.069 | 0.006 |
| Payoff change on conflict trials, as used | 0.27 | 0.21 | 0.01 |
| Natural mix: dV\* / dV / room | 0.010 / 0.020 / 0.017 | 0.008 / 0.015 / 0.018 | 0.009 / 0.004 / 0.033 |
| Strict payoff (−9): dV\* / room | 0.127 / 0.178 | 0.110 / — | 0.011 / — |
| Accuracy change on conflicts, intact − lesion | −0.009 | −0.002 | 0.004 |

Tests: P1M_1 27/28; P1M_2 28/28; P1M_3 20/28 (weakest).

Novel damage (PFATE): the variable earns nothing against the re-tuned rival
(dV\* about 0). As used it costs (scramble −0.015, not detected; noise −0.018
and zero −0.013, REVERSED). Room is about 0: the agent stays accurate, so
there is nothing to earn. This is P1k's over-caution, priced.

## 6. Expectations (written after discovery, before the confirmation)

| Outcome | Probability |
| --- | --- |
| Valid, room present | 0.95 |
| VALUE_CREDITED | 0.60 |
| VALUE_NOT_LEARNED | 0.25 (P1M_3 weakest; PNOFATE inflated by lesion side effects) |
| USED_NOT_NECESSARY | 0.05 |
| Other | 0.10 |
| Natural-mix dV\* > 0 for PFATE | 0.85 |
| Novel damage: dV as used < 0 for PFATE (median, all three operators) | 0.80 |

## 7. Seeds, outputs, verification

- **Confirmation:** P1i's seeds 3400–3427 (P1i's weights, by design; tested).
  No P1m measure has been computed on them.
- Outputs go to `p1m_necessity/confirm/`.
- **Verification:**
  - source hashes match this freeze;
  - `--score` reproduces REPORT.md;
  - `score()` equals `scores.json`;
  - no errors in the log.

## 8. Limits

- **Matched rival, not every rival.** It is the same trained network with the
  variable clamped. A separately trained network with a different
  organization (for example, extra units, or a supplied flag in training) is
  not tested. "Strongest simpler rival" here means the strongest reduction
  available without retraining.
- **One probe payoff** (+1 / −4 / 0), the training payoff. The probe mix
  overweights damage relative to training; the natural mix is reported.
- **The lesion** uses average-difference directions per step; it may not
  remove every trace of the variable.
- One task, one architecture (a 70-unit GRU).
- No consciousness claim.

## 9. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
