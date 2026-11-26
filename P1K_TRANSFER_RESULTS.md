# P1k results: GENERAL_INTEGRITY_VARIABLE on fresh seeds (Layer 4)

- **Protocol:** [P1K_TRANSFER_PROTOCOL.md](P1K_TRANSFER_PROTOCOL.md), frozen at
  810f998 before any P1k measure was computed on P1i's seeds.
- **Follows:** [P1J_STEER_RESULTS.md](P1J_STEER_RESULTS.md).
- **Run:** evaluation only, on saved weights (3600).
  - Discovery set: P1g's seeds, 3200–3227 (v1, then the final run with the
    same-overwrite secondary; disclosed).
  - Confirmation: P1i's seeds, 3400–3427.
  - Report: [p1k_transfer/confirm/REPORT.md](p1k_transfer/confirm/REPORT.md).
- **Verification:**
  - All 24 source files are byte-identical to the freeze, and so are the
    hashes recorded in raw.json.
  - `--score` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`.
  - No error in the log.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: GENERAL_INTEGRITY_VARIABLE.** All three damage types never seen in
training GENERALIZE. Valid: 28 seeds fitted in every arm, and the reference
replicates P1j (rescue on donor conflicts 26/28).

| Operator (never in training) | P1K_ACT: state moves along d | P1K_RES: removing d restores confidence | Label |
| --- | --- | --- | --- |
| scramble (the units' own values permuted) | 27/28, median 0.46 | 24/28, median 0.29 | GENERALIZES |
| noise (uniform values on [−1, 1]) | 27/28, median 0.44 | 22/28, median 0.32 | GENERALIZES |
| zero (the units set to 0) | 27/28, median 0.40 | 23/28, median 0.31 | GENERALIZES |

All Holm p ≤ 0.004. No content confound:

- the accuracy change under −d vs −r is at most 0.003;
- for scramble it is consistent in sign (23/28) but far below the 0.02
  tolerance.

## 2. Values (medians; PNOFATE in brackets)

| | donor (conflict) | same (valid overwrite) | scramble | noise | zero |
| --- | --- | --- | --- | --- | --- |
| act along d | 1.33 (0.13) | 0.00 (−0.00) | 0.46 (0.12) | 0.44 (0.11) | 0.40 (0.11) |
| Cosine of the damage shift with d | 0.98 (0.54) | 0.00 | 0.72 (0.27) | 0.67 (0.25) | 0.61 (0.25) |
| act per K (9 / 18 / 26 / 35) | 0.34 / 1.00 / 1.75 / 2.17 | ≈ 0 | 0.12 / 0.32 / 0.52 / 0.86 | 0.12 / 0.31 / 0.50 / 0.81 | 0.11 / 0.25 / 0.45 / 0.76 |
| rescue | 0.38 (0.02) | 0.06 (−0.01) | 0.29 (−0.03) | 0.32 (0.00) | 0.31 (−0.00) |
| rescue in abstention | 0.035 | 0.000 | 0.013 | 0.015 | 0.008 |
| gap: confidence drop | 4.49 (1.76) | 0.00 | 1.41 (1.36) | 1.30 (1.59) | 1.04 (1.87) |
| gap_abs: abstention rise | 0.37 (0.00) | 0.00 | 0.068 (0.00) | 0.044 (0.00) | 0.018 (0.00) |
| Agent accuracy on damaged trials | 0.81 (0.69) | 1.00 | 0.986 (0.88) | 0.994 (0.89) | 0.999 (0.93) |

- Rescue against PNOFATE: 25/28, 23/28 and 23/28 for scramble, noise and
  zero (DERIVED_AHEAD).
- Against PYOKED: no difference (11–12/28).
- The activation rises with K for every novel operator (dose_rho 1.0,
  26–27/28).

## 3. What was found

- **One variable for several kinds of damage.** The direction d was estimated
  only from donor conflicts, the one damage type the agent was trained on.
  - Three damage types it never met move the state along that same direction
    (cosine 0.61–0.72, against 0.25–0.27 in the never-damaged net), in
    proportion to the damage size.
  - Removing d restores confidence under each of them, and lowers abstention.
  - The variable is about the integrity of the agent's own memory, not about
    one damage signature.
- **It reads an anomalous state, not mere perturbation.** A same-value donor
  overwrite leaves a state that normal operation produces. d does not move
  there (0.00; below scramble in 27/28), and confidence does not drop.
  - Caveat (protocol §4): that overwrite leaves little lasting shift by step
    5 (0.12, against about 0.64). This shows that a perturbation landing on a
    valid state leaves nothing for d to read; it does not show that d ignores
    large valid shifts.
- **It is learned, and used only by the damage-trained agent.**
  - In the never-damaged net the same axis is weak and poorly aligned with
    the damage shifts.
  - Relative to its own donor activation, that axis moves almost as much for
    any damage (alpha 0.66–0.74 against 0.30–0.32 for PFATE; PNOFATE "ahead"
    on that secondary). Its conflict axis is just a direction of generic
    perturbation.
  - Removing it does nothing (rescue about 0).
  - The yoked arm matches the damage-trained agent: exposure to damage
    suffices.
- **It generalizes, but its calibration does not.**
  - Under the novel damage the damage-trained agent stays almost fully
    accurate: 0.986–0.999, and 0.96–0.997 even when half its units are hit.
  - Yet the variable fires at about a third of its donor strength, its
    confidence drops (1.0–1.4) and it abstains more (+0.02 to +0.07).
  - The never-damaged net is less accurate under the same damage (0.88–0.93)
    and does not abstain at all.
  - So the damage-trained agent is over-cautious on unfamiliar damage: it
    treats "my memory is in an abnormal state" as grounds for doubt even when
    its content survived. Its calibrated discount (P1i) holds for the damage
    it learned from.

## 4. Against the expectations (protocol §6)

| Outcome | Expected | Observed |
| --- | --- | --- |
| Valid | 0.97 | Yes |
| GENERAL_INTEGRITY_VARIABLE | 0.75 | Yes |
| PARTIAL / DONOR_SPECIFIC | 0.15 / 0.03 | No |
| act(same) not detected, and below scramble | 0.85 | Yes (0.00; 27/28 below) |
| Over-caution: accuracy ≥ 0.97 under novel damage while abstention rises | 0.85 | Yes (0.986–0.999; +0.018 to +0.068) |

Discovery and confirmation agree closely:

| | Discovery | Confirmation |
| --- | --- | --- |
| act, novel operators | 0.47–0.55 | 0.40–0.46 |
| rescue, novel operators | 0.28–0.32 | 0.29–0.32 |
| Primaries | 24–28 of 28 | 22–27 of 28 |

## 5. Reading

- **Layer 4: a general self-model variable.** The P1h–P1k line now gives a
  connected picture of one variable in the damage-trained agent:
  - **Reads:** whether its own memory state is anomalous.
  - **General:** it is engaged by kinds of corruption never met in training,
    but not by a perturbation that leaves a valid state.
  - **Graded:** it scales with the size of the damage.
  - **Separate:** it is represented apart from the content (content-free,
    P1j).
  - **Causal:** it sets the confidence in the content, in both directions
    (P1j, and here under novel damage).
  - **Learned:** it comes from exposure to damage, not from a precarious
    body; the never-damaged net has only an unused axis of generic
    perturbation.
- **Organizational signature.** A monitor of the agent's own memory that
  abstracts from the cause of damage and controls confidence. This is the
  architecture that cue-based metacognition assumes: a fluency or integrity
  cue that generalizes across sources and can mislead when the situation is
  new.
  - The over-caution is a recognizable property of such cue-based monitors:
    the cue fires on unfamiliar anomalies whether or not they harmed the
    content.
- **What it is not.**
  - It is not a calibrated reliability estimate for new kinds of damage.
  - It is not most of the confidence drop: d accounts for about 10–30%,
    depending on the operator.
  - It is not reportable by a separate channel, and it is not awareness.

## 6. Limits

- Three novel operators, each applied once to a random subset of units.
  Other kinds of corruption (slow drift, structured interference, damage to
  weights rather than state) are untested.
- The same-overwrite control is weak, as noted in §3.
- d comes from average differences, and the push is linear and clipped (as in
  P1j).
- The same-overwrite operator was added after discovery v1 (disclosed). The
  primaries were fixed before any P1k data.
- One task, one architecture (a 70-unit GRU).

## 7. Files

- `trackc_swap/transfer.py`, `run_p1k_transfer.py`, `test_p1k_transfer.py`
  (6 tests: donor reproduces P1j's runner, the operators, every probe kind
  damaged, synthetic activation, labels, streams and seed sets).
- `p1k_transfer/discovery_v1/` and `p1k_transfer/discovery/` (P1g's seeds);
  `p1k_transfer/confirm/`.

## 8. Next steps (for the PI; not authorized by this card)

- **Reportability (a Layer 3/4 bridge).** Can a separate consumer read the
  variable?
  - Freeze the agent and train only a small new readout ("was my memory
    disturbed?") on d's activation versus on the full state, then test it on
    novel damage.
  - Better: train an agent with an explicit second report action, and see
    whether the same variable is recruited.
  - Access by a second consumer is the step from a monitor to something like
    reportable self-knowledge.
- **Calibration under new damage.** Does brief exposure to a new damage type
  recalibrate the discount (accuracy-appropriate) while the variable stays
  the same? That would show the variable is fixed and its use is learned.
- **Valid large shifts.** A stronger control for "anomaly vs perturbation":
  large shifts that stay on the manifold of valid states, such as replacing
  the whole state with another agent's state holding the same value, read
  at step 1 rather than step 5.

## 8b. Safety

- Simulated variables only (X1–X5). The operators act on the simulated
  agent's own simulated state; no real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
