# P1l protocol: is the integrity variable accessible to a second consumer, and is it the same variable? (Layer 4 → Layer 3)

- **Status:** FROZEN (this commit), before any P1l measure is computed on P1i's
  seeds (3400–3427).
- **Follows:** [P1K_TRANSFER_RESULTS.md](P1K_TRANSFER_RESULTS.md)
  (GENERAL_INTEGRITY_VARIABLE). Chosen by the PI ("proceed", 2026-11-26,
  after the recommendation "reportability").
- Astra review waived by the PI. No consciousness claim.

## 1. Question

P1j and P1k found a content-free variable in the damage-trained agent's state.
Anomalous damage to its memory produces it, including damage never seen in
training, and it causally sets the agent's confidence. Its only shown
consumer is the policy's own report confidence.

A self-model variable that only one process can use is private. A variable
that other processes can read, and that is *the same* variable, is the
precondition for broadcast, the defining property of Layer 3 (the
workspace).

P1l asks:

1. **Access:** can a second consumer, trained only on the one damage type
   the agent was trained on, read "my memory is corrupted" from the state,
   and does that generalize to damage neither the agent nor the consumer has
   seen?
2. **Learned:** is the access better in the damage-trained agent than in the
   never-damaged net?
3. **Same variable:** does moving P1j's d upstream (delay step 5) move the
   second consumer downstream (step 9), as it moves the confidence?

## 2. Design

Evaluation only, on saved weights at 3600, in fresh evaluation worlds (stream
tags EVAL_TAG_G + 80 and + 100). Setting: P1j's and P1k's EARLY graded probe,
clear undrained trials.

- **Directions:** P1j's d and the random control r at delay step 5, from donor
  conflict vs same trials (`steerint.directions`).
- **The second consumer:** a logistic read-out on the standardized state at
  the readout step (step 9, the state the policy reads), L2 1e-3.
  - It is fitted on the frozen agent's states from one pass of the trained
    damage: label 1 for conflict overwrites, label 0 for undamaged trials and
    same-value overwrites.
  - Being linear, it cannot use the value-signed content, whose sign flips
    with the stored value (tested). It must read value-independent
    structure.
- **Held-out passes**, one per operator (P1k's operators):
  - donor: AUC conflict vs none, and conflict vs same;
  - same: same-value overwrite vs none;
  - scramble, noise, zero: damaged vs none.
  - AUCs are value-balanced: the mean of the within-value AUCs.
- **The steering pass** is P1j's design at natural size: same trials get +d
  or +r, conflict trials −d or −r, at step 5. The read-out's score (logit) is
  taken at step 9.
  - induce_rep = score(same, +d) − score(same, +r)
  - rescue_rep = score(conflict, −r) − score(conflict, −d)
  - **signed_rep** = induce_rep + rescue_rep
  - Also gap_rep (score conflict − same, no push), and P1j's confidence
    effects in the same pass (induce_conf, rescue_conf).
- **Alignment:** on the held-out donor pass, the within-value correlation of
  the read-out's score with the projection on d9 (P1j's direction computed at
  step 9), and with the content direction c9.
  - This is largely by construction (both separate conflicts at step 9) and
    is reported, not tested.
  - The weight-vector cosine first planned was replaced before the discovery
    run. Near-constant units make it meaningless after de-standardizing;
    found on a one-seed smoke check (seed 3200), disclosed.

## 3. Decision rules (exactly as in `run_p1l_access.py`)

Holm over the three tests (α 0.05):

| Test | Comparison | Type |
| --- | --- | --- |
| P1L_1 general | Mean AUC over scramble, noise and zero, minus 0.5, PFATE | One-sample sign test → PRESENT / REVERSED / NOT_DETECTED |
| P1L_2 learned access | Mean novel AUC, PFATE vs PNOFATE | Paired sign test → DERIVED_AHEAD / HOST_AHEAD / NO_DIFFERENCE_DETECTED |
| P1L_3 same variable | signed_rep of PFATE > 0 | One-sample sign test |

**Validity:** at least 20 seeds fitted for PFATE and PNOFATE, and PFATE's
median held-out AUC on the trained damage ≥ 0.70.

**Overall:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | Any primary UNDETERMINED |
| NOT_GENERAL | P1L_1 not PRESENT |
| SHARED_GENERAL_ACCESS | P1L_1 PRESENT, P1L_3 PRESENT, P1L_2 DERIVED_AHEAD |
| SHARED_ACCESS_NOT_LEARNED | P1L_1 PRESENT, P1L_3 PRESENT, P1L_2 not DERIVED_AHEAD |
| GENERAL_ACCESS_SEPARATE_ROUTE | P1L_1 PRESENT, P1L_3 not PRESENT, P1L_2 DERIVED_AHEAD |
| GENERAL_ACCESS_NOT_LEARNED | P1L_1 PRESENT, P1L_3 not PRESENT, P1L_2 not DERIVED_AHEAD |

**Secondaries** (reported, not labelled):

- signed_rep, PFATE vs PNOFATE; novel AUC, PFATE vs PYOKED; donor AUC,
  PFATE vs PNOFATE;
- scramble AUC vs same-overwrite AUC (PFATE);
- routes per arm for every measure.

## 4. Readings

- **SHARED_GENERAL_ACCESS.**
  - A consumer that never sees the policy, trained on one damage type, reads
    the agent's integrity variable and generalizes to new damage.
  - What it reads is causally downstream of the same direction that sets the
    agent's confidence, so one variable serves two consumers.
  - It is accessible because the damage-trained agent represents it
    explicitly. The never-damaged net offers a weaker, less general signal.
  - Layer 4 → Layer 3: the variable is in a form that could be broadcast.
- **What it is not.** The second consumer is an external, frozen-state
  read-out. P1l does not show that the agent itself reports, or that the
  variable is broadcast inside the agent. Access by a learned read-out is a
  precondition, not a workspace.
- **SEPARATE_ROUTE:** the consumer reads a correlate that d does not drive.
- **NOT_LEARNED:** the never-damaged net offers equal access.

## 5. Discovery set (P1g's seeds 3200–3227, before this freeze)

[p1l_access/discovery/REPORT.md](p1l_access/discovery/REPORT.md):
**SHARED_GENERAL_ACCESS**. The code and the primary tests were committed
(0ec3592) before the run; nothing was changed after it.

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| AUC trained damage: vs none / vs same | 0.93 / 0.93 | 0.93 / 0.93 | 0.75 / 0.73 |
| AUC same-value overwrite vs none | 0.53 | 0.54 | 0.54 |
| AUC scramble / noise / zero | 0.79 / 0.83 / 0.85 | 0.78 / 0.82 / 0.86 | 0.66 / 0.69 / 0.72 |
| induce_rep / rescue_rep (gap_rep) | 1.97 / 2.07 (8.89) | 2.25 / 1.45 (9.23) | 0.12 / 0.09 (0.97) |
| induce_conf / rescue_conf (P1j replication) | 0.34 / 0.60 | 0.28 / 0.58 | −0.00 / 0.02 |
| corr with d9 / with c9 | 0.96 / 0.01 | 0.95 / −0.01 | 0.54 / −0.05 |

Tests: P1L_1 28/28; P1L_2 26/28; P1L_3 25/28. scramble > same 28/28.

- Each push moves about 22% of the read-out's natural conflict–same
  difference (induce 1.97 and rescue 2.07, against 8.89). For the confidence
  in P1j it was about 10%.
- The never-damaged net's read-out also generalizes above chance (0.69): its
  state carries a weaker, generic perturbation signal (P1k).

## 6. Expectations (written after discovery, before the confirmation)

| Outcome | Probability |
| --- | --- |
| Valid | 0.97 |
| SHARED_GENERAL_ACCESS | 0.85 |
| SHARED_ACCESS_NOT_LEARNED | 0.05 |
| GENERAL_ACCESS_SEPARATE_ROUTE | 0.05 |
| Other | 0.05 |
| Same-overwrite AUC below 0.60 for PFATE | 0.90 |

## 7. Seeds, outputs, verification

- **Confirmation:** P1i's seeds 3400–3427 (P1i's weights, by design; tested).
  No P1l measure has been computed on them.
- Outputs go to `p1l_access/confirm/`.
- **Verification:**
  - source hashes match this freeze;
  - `--score` reproduces REPORT.md;
  - `score()` equals `scores.json`;
  - no errors in the log.

## 8. Limits

- The second consumer is an external linear read-out on a frozen agent. It
  shows what is available to a consumer, not what the agent's own processes
  consume.
- d comes from average differences, and the push is linear and clipped (as in
  P1j). The read-out is fitted with labels (supervision), which is acceptable
  for an access test but would not be for a grounding test.
- One task, one architecture (a 70-unit GRU).
- No consciousness claim.

## 9. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
