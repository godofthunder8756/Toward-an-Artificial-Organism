# P1n results: SUPPLY_DISPLACES_MONITOR on fresh seeds (Layer 4)

- **Protocol:** [P1N_SUPPLIED_PROTOCOL.md](P1N_SUPPLIED_PROTOCOL.md), frozen
  at 51ab0dd before the rival was trained on P1i's seeds and before any P1n
  measure was computed on them.
- **Follows:** [P1M_NECESSITY_RESULTS.md](P1M_NECESSITY_RESULTS.md).
- **Run:**
  - **Rival (FLAG arm):** trained from scratch after phase 1 on P1i's 28
    seeds (3400–3427). It has the same network, damage and streams as PFATE,
    plus a supplied damage analyzer as input. 28 of 28 trained, in 7
    committed batches, with no errors.
  - **Evaluation:** at 3600 against P1i's saved PFATE and PNOFATE weights.
  - **Discovery set:** 8 of P1g's seeds (3200–3207); v1 was disclosed and
    corrected before the freeze (protocol §5).
  - **Report:** [p1n_supplied/confirm/REPORT.md](p1n_supplied/confirm/REPORT.md).
- **Verification:**
  - All 26 source files are byte-identical to the freeze, and so are the
    hashes recorded in raw.json.
  - `--score` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`.
  - No error in the training or analysis logs.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: SUPPLY_DISPLACES_MONITOR**, with P1N_1 NO_DIFFERENCE_DETECTED.
Valid: 28 seeds, and the rival learned the task (FLAGON 0.794 against
PNOFATE 0.482).

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1N_1 cost of being endogenous: payoff, FLAGON vs PFATE | FLAGON ahead on 11/28 (0.794 vs 0.805) | 0.34 | NO_DIFFERENCE_DETECTED |
| P1N_2 analyzer silent: payoff, PFATE vs FLAGOFF | 28/28 (0.805 vs 0.634) | < 0.0001 | ENDOGENOUS_AHEAD |
| P1N_3 displacement: norm_d, PFATE vs FLAGOFF | 27/28 (1.31 vs 0.38) | < 0.0001 | ENDOGENOUS_AHEAD |

- **Recovery:** the share of the supplied analyzer's gain over the
  never-damaged net that the endogenous agent gets without any supply is
  median **1.01** (n 25; 3 seeds had too small a denominator).

## 2. Values (medians; payoff per probe trial, +1 / −4 / 0)

| | PFATE (endogenous) | PNOFATE | FLAGON (analyzer working) | FLAGOFF (analyzer silent) |
| --- | --- | --- | --- | --- |
| Payoff as used (probe mix) | **0.805** | 0.482 | 0.794 | 0.634 |
| V\* (best threshold on own confidence) | 0.809 | 0.654 | 0.798 | 0.674 |
| Payoff at natural exposure | 0.957 | 0.888 | 0.955 | 0.919 |
| Payoff on conflict trials | 0.41 | −0.53 | 0.38 | −0.08 |
| Accuracy on conflict trials | 0.809 | 0.691 | 0.779 | 0.778 |
| norm_d (own integrity direction) | 1.31 | 0.16 | (1.69, includes the flags' input footprint) | 0.38 |
| Payoff, scramble / noise / zero (novel) | 0.951 / 0.963 / 0.984 | 0.590 / 0.619 / 0.758 | not evaluated | 0.850 / 0.895 / 0.963 |

Secondaries (unadjusted):

| Comparison | Result | Label |
| --- | --- | --- |
| V\*, FLAGON vs PFATE | 10/28 | NO_DIFFERENCE_DETECTED |
| Payoff at natural exposure, FLAGON vs PFATE | 13/28 | NO_DIFFERENCE_DETECTED |
| Conflict accuracy, PFATE vs FLAGON | 21/28 (p 0.013) | ENDOGENOUS_AHEAD |
| Payoff, FLAGON vs FLAGOFF | 28/28 | ON_AHEAD |
| Payoff, FLAGOFF vs PNOFATE | 25/28 | FLAGOFF_AHEAD |
| V\*, PFATE vs FLAGOFF | 26/27 | ENDOGENOUS_AHEAD |
| Payoff at natural exposure, PFATE vs FLAGOFF | 27/28 | ENDOGENOUS_AHEAD |
| norm_d, FLAGOFF vs PNOFATE | 24/28 | FLAGOFF_AHEAD |
| Novel payoff, PFATE vs FLAGOFF: scramble / noise / zero | 24/28 / 22/28 / 14/28 | ENDOGENOUS_AHEAD / ENDOGENOUS_AHEAD / NO_DIFFERENCE_DETECTED |

## 3. What was found

- **Being endogenous costs nothing measurable.**
  - An agent of the same size and training, given a perfect external
    analyzer of the trained damage, earns no more than the agent that has
    to detect the damage itself.
  - This holds as used (11/28), at the best threshold (10/28) and at natural
    exposure (13/28).
  - The endogenous agent recovers all of the analyzer's value over the
    never-damaged net (median 1.01).
- **The supplied analyzer displaces the network's own monitor.**
  - Trained with the analyzer, the network builds much less of its own
    integrity direction: 0.38 against 1.31 (27/28). That is about a quarter
    of the endogenous agent's, though still above the never-damaged net's
    (0.16, 24/28).
  - When the analyzer is silent, the rival loses most of its advantage:
    - payoff 0.634 against 0.805 (28/28);
    - on conflict trials it reports wrongly often enough to lose
      (−0.08 against +0.41);
    - it stays above the never-damaged net (25/28), using its residual
      monitor.
- **The analyzer is specific; the endogenous monitor is general.**
  - On two of three damage types neither agent was trained on (scramble,
    noise), the endogenous agent beats the rival whose analyzer does not
    cover them (24/28, 22/28).
  - On zeroing, the mildest of the three, there is no difference (14/28).
- **One unplanned observation (a secondary, unadjusted).** The endogenous
  agent reads damaged content slightly more accurately than the rival with
  its analyzer working: 0.809 against 0.779 on conflict trials (21/28).
  - The flags tell FLAGON when to abstain, but not what the memory held. Its
    conflict accuracy equals FLAGOFF's (0.779 / 0.778).
  - Learning to detect damage itself seems to come with a somewhat better
    read of what survives (compare P1i's addendum: a different read of
    damaged content).
  - This is not tested as a primary and is not credited.

## 4. Against the discovery set and the expectations

| | Discovery (3200–3207, n 8) | Confirmation (3400–3427, n 28) |
| --- | --- | --- |
| Payoff: PFATE / PNOFATE / FLAGON / FLAGOFF | 0.807 / 0.503 / 0.792 / 0.631 | 0.805 / 0.482 / 0.794 / 0.634 |
| norm_d: PFATE / FLAGOFF / PNOFATE | 1.36 / 0.52 / 0.20 | 1.31 / 0.38 / 0.16 |
| FLAGON vs PFATE | 4/8 | 11/28 |
| PFATE vs FLAGOFF: payoff / norm_d | 8/8 / 8/8 | 28/28 / 27/28 |
| Recovery (median) | 1.01 | 1.01 |
| Novel, PFATE vs FLAGOFF: scramble / noise / zero | 6/8 / 6/8 / 5/8 | 24/28 / 22/28 / 14/28 |

| Outcome (protocol §6) | Expected | Observed |
| --- | --- | --- |
| Valid | 0.95 | Yes |
| P1N_1 SUPPLY_AHEAD / NO_DIFFERENCE / ENDOGENOUS_AHEAD | 0.25 / 0.65 / 0.10 | NO_DIFFERENCE |
| P1N_2 ENDOGENOUS_AHEAD | 0.95 | Yes |
| P1N_3 ENDOGENOUS_AHEAD | 0.90 | Yes |
| Overall SUPPLY_DISPLACES_MONITOR | 0.85 | Yes |
| Recovery ≥ 0.8 (median) | 0.70 | Yes (1.01) |
| FLAGOFF payoff above PNOFATE | 0.90 | Yes (25/28) |

## 5. Reading and credit

- **The protocol's reading (§4) applies.**
  - A supplied analyzer buys nothing that the endogenous monitor does not
    already provide while it works.
  - When it is silent, the agent trained on it fails, because the analyzer
    displaced most of its own monitor.
  - So the endogenous organization is not reducible to supplied substrate,
    for this rival: it gives the same value without the supply, and keeps
    it when the supply fails or meets damage it was not built for.
- **What this adds to P1m's credit.**
  - P1m credited the variable against reductions of the same network.
  - P1n credits it against a separately trained rival with more information
    (a perfect analyzer of the trained damage).
  - It meets the constitution's supplied-substrate rule. The rival "in which
    the network gets the same information directly" does no better while the
    supply works, and worse when it does not.
  - Synthesis status of the Layer 4 building block (a learned integrity
    monitor of the agent's own memory) stays **SUPPORTED_BOUNDED**, with the
    supplied-substrate rival now passed.

  | Constitution question | Answer |
  | --- | --- |
  | Q-EXIST | Yes |
  | Q-LEARN | Yes, from exposure to damage |
  | Q-CAUSE | Yes (P1j, P1k) |
  | Q-NECESSITY / VALUE against the lesion rival | Yes (P1m) |
  | Q-NECESSITY / VALUE against a separately trained supplied-substrate rival | Equal while the supply works, ahead when it is silent or does not cover the damage (P1n) |

- **The claim ceiling (what is NOT established):**
  - **Not the strongest possible rival.** The silent analyzer is out of
    distribution for FLAG by design: it was never trained with the analyzer
    absent.
    - A rival trained with analyzer dropout would probably keep its own
      monitor and would be the stronger test.
    - So would a larger network or a noisy analyzer.
    - P1n shows that a perfect, always-present supply crowds out the
      endogenous monitor. It does not show that no supplied rival can match
      it.
  - **The robustness advantage is a property of this rival's training**,
    not proof that endogenous monitoring is necessary for robustness.
  - **One task, one payoff, one 70-unit GRU, one trained damage type.**
  - **Layer 0 → Layer 4 still not supported.** Exposure, not the precarious
    body, is the source (the yoked arm matched PFATE in P1g–P1m).
  - **Not awareness.** No phenomenal claim.

## 6. Files

- `trackc_swap/supplied.py`, `run_p1n_supplied.py`, `test_p1n_supplied.py`
  (4 tests: with the flags off, the FLAG runner reproduces PFATE training
  bit for bit; the flags report the damage; labels; seed sets).
- `p1n_supplied/train_discovery/` and `p1n_supplied/train_confirm/` (FLAG
  weights at 1800 and 3600, per-seed training records, logs).
- `p1n_supplied/discovery_v1/`, `p1n_supplied/discovery/` (P1g's seeds) and
  `p1n_supplied/confirm/`.

## 7. Next steps (for the PI; not authorized by this card)

- **The analyzer-dropout rival (recommended first).** Train FLAG with the
  analyzer present on a fraction of trials, at equal size and at larger
  size.
  - This is the strongest supplied-substrate rival: it can learn both to use
    the supply and to keep its own monitor.
  - If it matches the endogenous agent both with the analyzer and without
    it, the endogenous agent's robustness advantage is only a training
    artifact of P1n's rival.
  - If the larger network matches with fewer supplied trials, the
    advantage is one of size.
- **Replication in a second architecture or task** (LSTM or a larger GRU; a
  memory task with differently structured corruption). This is needed
  before calling the monitor a general building block rather than a result
  in this system.
- **Metacognitive learning (Layer 4):** whether a brief exposure to a new
  damage type recalibrates the use of the variable (P1k's over-caution)
  without retraining it.

## Forward note (2026-11-27): P1o

[P1O_COUPLING_RESULTS.md](P1O_COUPLING_RESULTS.md): **NO_COUPLING**.
- A detected corruption is strongly informative about the fated agent's
  body (room 0.33), but the agent does not use it to regulate.
- No difference from the yoked agent; steering along d is null.
- The precarity thesis is not supported for the integrity monitor on
  control, as on detection.

## 8. Safety

- Simulated variables only (X1–X5). The analyzer is a simulated input; no
  real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
