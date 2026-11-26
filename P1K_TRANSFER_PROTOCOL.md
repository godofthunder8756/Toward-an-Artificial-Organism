# P1k protocol: is the integrity variable general across damage never seen in training? (Layer 4)

- **Status:** FROZEN (this commit), before any P1k measure is computed on P1i's
  seeds (3400–3427).
- **Follows:** [P1J_STEER_RESULTS.md](P1J_STEER_RESULTS.md)
  (LEARNED_SIGNED_INTEGRITY_VARIABLE). Chosen by the PI ("Proceed with P1k",
  2026-11-26).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

P1j found a content-free direction d in the agent's state, produced by its
dynamics after a conflicting overwrite, that causally sets its confidence in
both directions. Training only ever damaged memory one way: K units
overwritten by another agent's state (a donor).

Is d a variable about the **integrity of the agent's own memory in general**,
or a detector of that one kind of damage? Concretely:

1. Under kinds of damage never met in training, does the state move along the
   same d, estimated from donor conflicts?
2. Does removing d restore confidence there?

## 2. Design

Evaluation only, on saved weights at 3600, in fresh evaluation worlds (stream
tag EVAL_TAG_G + 60). The setting is P1j's: the EARLY graded probe (damage
at delay step 1, K ∈ {9, 18, 26, 35}, readout at step 9), clear undrained
trials, value-balanced means.

- **Pass 1:** P1j's directions, recomputed in these worlds with P1j's code
  (`steerint.directions`) from donor conflict vs same trials at delay step
  5: d and a random control r of the same norm.
- **Damage operators**, applied at the probe event to the K masked units:

  | Operator | What it does | Analysed trials |
  | --- | --- | --- |
  | donor | The trained damage: the units take a donor's values | Conflict trials (reference) |
  | same | The same donor overwrite | Same-value trials (secondary control) |
  | scramble | The units' own values are permuted among themselves; no foreign content | Every damaged probe trial |
  | noise | Independent uniform draws on [−1, 1] | Every damaged probe trial |
  | zero | The units are set to 0 | Every damaged probe trial |

  scramble, noise and zero are the **novel** operators. They are never seen
  in training, and the donor's value plays no part in them.
- **Pass A (per operator):** states at delay step 5.
  - **act** = mean projection on d/|d| of the damaged trials minus that of
    the undamaged (none) trials.
  - Also act per K, the cosine of the damage shift with d, and alpha = act /
    act(donor).
- **Pass B (per operator):** at step 5 each damaged trial is assigned at
  random to no push, −d or −r (natural size, as in P1j), and read out at
  step 9.
  - **rescue** = |z|(damaged, −d) − |z|(damaged, −r).
  - gap = |z|(none) − |z|(damaged, no push).
  - The same in abstention probability, the accuracy change (−d vs −r), and
    the agent's accuracy on damaged trials, overall and per K.
- **Reproduction.** With the donor operator, the P1k runner reproduces P1j's
  runner exactly (tested). The operators touch only the masked units of
  damaged trials (tested).

## 3. Decision rules (exactly as in `run_p1k_transfer.py`)

For each novel operator X ∈ {scramble, noise, zero}, two one-sample sign tests
on PFATE, Holm over all six (α 0.05):

| Test | Measure | Labels |
| --- | --- | --- |
| P1K_ACT_X | act > 0 | PRESENT / REVERSED / NOT_DETECTED |
| P1K_RES_X | rescue > 0 | PRESENT / REVERSED / NOT_DETECTED |

**Per operator:**

| Label | Rule |
| --- | --- |
| UNDETERMINED | Either test UNDETERMINED |
| CONTENT_CONFOUNDED | Rescue PRESENT, and PFATE's accuracy rises under −d vs −r (PRESENT, median ≥ 0.02) |
| GENERALIZES | Both PRESENT |
| ACTIVATES_NOT_USED | Only act PRESENT |
| USED_NOT_ACTIVATED | Only rescue PRESENT |
| NOT_GENERAL | Neither |

**Validity:**

- at least 20 seeds fitted for PFATE and PNOFATE;
- the reference replicates P1j: rescue on donor conflicts, PFATE, PRESENT
  (unadjusted).

**Overall:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | Any operator UNDETERMINED |
| GENERAL_INTEGRITY_VARIABLE | All three GENERALIZES |
| PARTIAL_GENERALITY | One or two GENERALIZES |
| DONOR_SPECIFIC | None GENERALIZES |

**Secondaries** (reported, not labelled):

- **The same-overwrite control:** act and rescue on same-value overwrite
  trials, and act(same) vs act(scramble) for PFATE.
- alpha and rescue per operator, PFATE vs PNOFATE; rescue, PFATE vs PYOKED.
- One-sample routes per arm and operator for act, rescue, rescue_abs, gap,
  dose_rho (act against K), cos and the accuracy change.
- **Calibration transfer (descriptive):** per operator, the agent's accuracy
  on damaged trials against the abstention rise (gap_abs) and alpha.

## 4. Readings

- **GENERAL_INTEGRITY_VARIABLE.**
  - The variable learned from one kind of damage is engaged by other kinds,
    and it sets confidence there too.
  - It is about the state of the agent's own memory, not about one damage
    signature.
  - Layer 4: a general self-model variable (memory integrity) that is used.
- **PARTIAL_GENERALITY / DONOR_SPECIFIC:** the variable is tied to the
  trained damage in part or entirely.
- **The same-overwrite control, as read in discovery.**
  - A same-value donor overwrite is a perturbation of the same size, but it
    leaves a state that normal operation can produce.
  - If d does not move there while the novel operators move it, d reads
    whether the state is anomalous, not whether it was perturbed.
  - Caveat: by step 5 the same overwrite leaves only a small lasting shift
    (0.12, against about 0.7 for the novel operators). The control shows
    that a perturbation landing on a valid state leaves nothing for d to
    read; it does not show that d ignores large lasting valid shifts.
- **Calibration transfer.**
  - In discovery the damage-trained agent stays highly accurate under novel
    damage (0.98–0.998), yet d fires at about a third of donor strength and
    abstention rises.
  - So generality of the variable does not imply calibration to novel
    damage; P1k measures generality, not calibration.

## 5. Discovery set (P1g's seeds 3200–3227, before this freeze)

- **[p1k_transfer/discovery_v1/](p1k_transfer/discovery_v1/REPORT.md):**
  operators donor, scramble, noise, zero.
  **GENERAL_INTEGRITY_VARIABLE**, every primary 24–28 of 28.
- **[p1k_transfer/discovery/](p1k_transfer/discovery/REPORT.md):** the same
  run with the same-overwrite secondary added. That was decided after seeing
  v1, to separate "any perturbation" from "anomalous state"; primaries and
  rules are unchanged. Adding the operator shifts the world streams of later
  passes. **GENERAL_INTEGRITY_VARIABLE.**

Medians, PFATE (PNOFATE in brackets):

| | donor (conflict) | same | scramble | noise | zero |
| --- | --- | --- | --- | --- | --- |
| act | 1.36 (0.16) | −0.00 (0.01) | 0.55 (0.12) | 0.52 (0.13) | 0.47 (0.13) |
| cos with d | 0.97 | −0.03 | 0.74 (0.28) | 0.71 (0.30) | 0.67 (0.29) |
| dose_rho of act in K | 1.0 | −0.3 | 1.0 | 1.0 | 1.0 |
| rescue | 0.52 (−0.03) | 0.09 | 0.31 (0.04) | 0.28 (0.01) | 0.32 (0.03) |
| gap (confidence drop) | 4.33 | 0.01 | 1.39 | 1.27 | 1.00 |
| gap_abs (abstention rise) | 0.39 | 0.00 | 0.073 | 0.050 | 0.026 |
| Agent accuracy on damaged trials | 0.81 (0.69) | 1.00 | 0.98 (0.87) | 0.99 (0.88) | 0.998 (0.93) |

Tests: P1K_ACT 28, 28, 28 of 28; P1K_RES 25, 25, 24 of 28. Reference rescue
26/28. No content confound. act(same) < act(scramble) in 28/28.

## 6. Expectations (written after discovery, before the confirmation)

| Outcome | Probability |
| --- | --- |
| Valid | 0.97 |
| GENERAL_INTEGRITY_VARIABLE | 0.75 |
| PARTIAL_GENERALITY | 0.15 |
| DONOR_SPECIFIC | 0.03 |
| UNDETERMINED / CONTENT_CONFOUNDED / INVALID | 0.07 together |
| act(same) not detected for PFATE, and below act(scramble) | 0.85 |
| PFATE accuracy on novel damage ≥ 0.97 while gap_abs > 0 (over-caution) | 0.85 |

## 7. Seeds, outputs, verification

- **Confirmation:** P1i's seeds 3400–3427 (P1i's trained weights, by design;
  tested). No P1k measure has been computed on them.
- Outputs go to `p1k_transfer/confirm/` (raw.json, scores.json, REPORT.md,
  run.log).
- **Verification:**
  - source hashes match this freeze;
  - `--score p1k_transfer/confirm` reproduces REPORT.md;
  - `score()` equals `scores.json`;
  - no errors in the log.

## 8. Limits

- Three novel operators, all applied to a random subset of units at one step.
  They are not exhaustive of "damage".
- d comes from average differences, and the push is linear and clipped (as in
  P1j).
- The same-overwrite control is weak in the way described in §4.
- One task, one architecture (a 70-unit GRU).
- No consciousness claim.

## 9. Safety

- Simulated variables only (X1–X5). The operators act on the simulated agent's
  own simulated state; no real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
