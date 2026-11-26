# P1j results: LEARNED_SIGNED_INTEGRITY_VARIABLE on fresh seeds (Layer 4)

- **Protocol:** [P1J_STEER_PROTOCOL.md](P1J_STEER_PROTOCOL.md).
  - First frozen at f0da2f3. Re-frozen at **548f2d1**, before any
    confirmation measure was computed: P1i's seed test flagged the seed-list
    names; disclosed in §7 of the protocol.
- **Follows:** [P1I_CALIB_RESULTS.md](P1I_CALIB_RESULTS.md), including its
  addendum: P1i's type-2 measure shows a different read of damaged content,
  not metacognition beyond the agent's own evidence.
- **Run:** evaluation only, on saved weights (3600).
  - Discovery set: P1g's seeds, 3200–3227 (three disclosed runs).
  - Confirmation: P1i's seeds, 3400–3427.
  - Report: [p1j_steer/confirm/REPORT.md](p1j_steer/confirm/REPORT.md).
- **Verification:**
  - All 23 source files are byte-identical to the freeze, and so are the
    hashes recorded in raw.json.
  - `--score p1j_steer/confirm` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`.
  - No error in the log.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: LEARNED_SIGNED_INTEGRITY_VARIABLE.** Valid: all 28 seeds fitted in
every arm. No content confound.

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1J_1 induce: adding d to intact memories lowers confidence (PFATE) | 22/28 > 0, median 0.41 | 0.004 | PRESENT |
| P1J_2 rescue: removing d from conflicted memories restores confidence (PFATE) | 25/28 > 0, median 0.39 | 0.0001 | PRESENT |
| P1J_3 learned variable: signed (induce + rescue) at natural size, PFATE vs PNOFATE | 23/28 (0.78 vs −0.00) | 0.003 | DERIVED_AHEAD |
| P1J_4 learned use: signed at equal push size, PFATE vs PNOFATE | 23/28 (0.52 vs 0.10) | 0.003 | DERIVED_AHEAD |

- **The push.** d is the shift that conflict trials share at delay step 5,
  whichever value is stored. Its projection on the content direction and on
  the ambiguity direction (unclear-cue trials) is removed.
- **The control.** r is a random direction of the same size, orthogonal to
  all three. Every effect is d against r, and every mean is balanced over
  the stored value: a push that merely shifts the decision variable cannot
  pass as a confidence change (tested).

Medians at push step 5:

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| induce / rescue (natural size) | 0.41 / 0.39 | 0.51 / 0.57 | 0.00 / −0.01 |
| As a share of the natural confidence drop (gap) | 9% / 10% | 12% / 13% | — |
| gap: \|z\| same − conflict, no push | 4.53 | 4.18 | 1.69 |
| induce_fix / rescue_fix (push norm 1.0) | 0.27 / 0.37 | 0.33 / 0.39 | 0.22 / **−0.13** |
| signed / signed_fix | 0.78 / 0.52 | 1.09 / 0.72 | −0.00 / 0.10 |
| rescue in abstention (gap in abstention) | 0.043 (0.37) | 0.049 (0.35) | 0.000 (0.00) |
| induce on undamaged (none) trials | 0.36 | 0.46 | 0.01 |
| Accuracy change: same +d vs +r / conflict −d vs −r | 0.000 / 0.001 | 0.000 / −0.003 | 0.000 / 0.003 |
| Random push vs none, same trials | 0.10 | 0.11 | −0.00 |
| norm_d (norm of the content direction) | 1.33 (7.9) | 1.40 (8.4) | 0.15 (3.6) |
| Share of the conflict shift kept after removing content and ambiguity | 0.98 | 0.97 | 0.78 |

The result holds at the other push steps. For PFATE, signed is 25/28 at step
3 and 24/28 at step 7, with induce and rescue each present at both. For
PNOFATE nothing is detected at any step.

## 2. What was found

- **A content-free variable sets the confidence, in both directions.** The
  agent's state after a conflict carries a component that does not depend on
  the stored value and is not general ambiguity.
  - Adding it to an intact memory lowers the agent's confidence in that
    memory; removing it from a conflicted memory raises confidence.
  - The content is untouched: accuracy does not change (0.000 and 0.001).
    Only the confidence in it moves.
  - Pushed into a memory that was never damaged at all, it lowers confidence
    too (0.36): it acts as an alarm, not as a feature of donor content.
  - The removal also lowers abstention on conflicts (0.043).
- **It is learned, both as a variable and in how it is used.**
  - **The variable:** in the never-damaged net the same conflict shift is
    about 9 times smaller (0.15 vs 1.33), and at its natural size it does
    nothing (signed −0.00).
  - **The use:** pushed equally hard along its own conflict direction, the
    never-damaged net does not respond as to a signed variable (0.10 vs 0.52,
    23/28).
  - Its axis is sensitive in both directions: adding it lowers confidence
    (0.22), and removing it also lowers confidence (−0.13).
  - In the damage-trained agent, more of the variable means less confidence
    and less of it means more.
- **Its share is modest.** Each direction of the intervention moves about
  10% of the natural confidence drop after a conflict. The rest of the
  discount runs through value-signed components of the state, which this
  design does not intervene on (see §5).
- **Layer 0.** The yoked arm, whose damage is not tied to its body, shows the
  same variable (signed PFATE vs PYOKED 9/28, not detected; PYOKED is if
  anything larger). Exposure to damage produces it, as in P1g–P1i.

## 3. Against the discovery set and the expectations

| | Discovery (3200–3227) | Confirmation (3400–3427) |
| --- | --- | --- |
| induce / rescue, PFATE | 0.39 / 0.65 | 0.41 / 0.39 |
| signed / signed_fix, PFATE | 0.98 / 0.60 | 0.78 / 0.52 |
| signed / signed_fix, PNOFATE | 0.02 / −0.02 | −0.00 / 0.10 |
| rescue_fix, PNOFATE | −0.17 | −0.13 |
| Tests P1J_1–4 | 21, 26, 24, 20 of 28 | 22, 25, 23, 23 of 28 |

The induce test was the weakest in discovery and replicates at the same
size. Rescue is smaller on the fresh seeds.

| Outcome (protocol §6) | Expected | Observed |
| --- | --- | --- |
| Valid | 0.97 | Yes |
| P1J_1 / P1J_2 PRESENT | 0.65 / 0.90 | Yes / Yes |
| P1J_3 / P1J_4 DERIVED_AHEAD | 0.85 / 0.55 | Yes / Yes |
| LEARNED_SIGNED_INTEGRITY_VARIABLE | 0.40 | Yes |
| GENERIC_COUPLING / ONE_WAY | 0.15 / 0.25 | No |
| signed, PFATE vs PYOKED NO_DIFFERENCE_DETECTED | 0.75 | Yes (9/28, p 0.09; PYOKED larger) |

## 4. Reading

- **Layer 4, at its sharpest so far in this project.** The agent carries a
  variable about the state of its own memory:
  - **content-free:** independent of what is stored;
  - **separate:** distinct from content and from ordinary ambiguity;
  - **produced by its own dynamics** after a conflict;
  - **used:** it sets the agent's confidence in that memory, in both
    directions, without changing what the memory says;
  - **learned from exposure to damage**, in both its size and its use.
- **In metacognition terms:** a confidence that integrates a separately
  represented integrity cue (cue-based metacognition). The cue is now shown
  to be causal, signed and content-free.
  - P1h showed it acts through the report confidence rather than a separate
    abstention channel. P1j does not change that.
- **What it is not.**
  - It is not most of the discount: about 10% per direction. The bulk of the
    confidence drop after a conflict sits in value-signed components, which
    may be content weakening (first order) or integrity-gated content gain.
    This design cannot tell those apart.
  - It is not a separate report or a reportable state.
  - It is not awareness.
- **Organizational signature.** A two-level organization: content, plus a
  variable about the reliability of that content which modulates it. Damage
  training creates and couples it; a never-damaged net of the same
  architecture has neither.

## 5. Limits

- **The intervention.** A linear push along one average-difference direction,
  into a non-linear recurrent net, clipped to [−1, 1]. It shows what that
  direction does, not the full extent of the variable.
- **Partial accounting.** The value-signed part of the discount was not
  intervened on, so the roughly 10% share is a lower bound on the integrity
  variable's role, not an apportionment of the whole discount.
- **Generic sensitivity to pushes.** In the damage-trained agent a random push
  of natural size also lowers confidence somewhat (0.10). At equal size the
  random effect is similar in both nets (0.09 vs 0.11). Every primary
  contrast is against the random push.
- **The design was revised on discovery data.** The size-matched pass and the
  signed measures were added after seeing discovery runs v1 and v2
  (disclosed in protocol §5). The confirmation on P1i's seeds is the
  safeguard.
  - Those seeds were fresh for this question but not for P1i's measures.
- One task, one architecture (a 70-unit GRU), one damage type.

## 6. Files

- `trackc_swap/steerint.py`, `run_p1j_steer.py`, `test_p1j_steer.py`
  (7 tests: exact reproduction of P1g's collection, zero push, direction
  recovery, value balance, gain reduction, labels, seed sets).
- `p1j_steer/discovery_v1/`, `p1j_steer/discovery_v2/` and
  `p1j_steer/discovery/`: P1g's seeds, before the freeze.
- `p1j_steer/confirm/`: raw.json, scores.json, REPORT.md, run.log.

## 7. Next steps (for the PI; not authorized by this card)

- **P1k, abstraction.** Is the variable about integrity in general, or about
  donor conflicts only?
  - Apply damage types never seen in training at evaluation: scrambling
    units within the state, noise, zeroing.
  - Test whether the same direction d, estimated from donor conflicts,
    activates in proportion to how unreliable the damaged memory is, and
    whether confidence follows.
  - A variable that generalizes across kinds of damage is the stronger
    self-model claim. No training is needed; the weights for 56 seeds are
    saved.
- **The value-signed part.** Is the remaining roughly 90% content weakening,
  or a gain on content set by the integrity variable? One test: remove d
  earlier (at the damage step) and see whether the value-signed drop at
  readout shrinks.
- **Reportability.** Can the variable be read out by a separate action
  (a "was my memory tampered with?" report) without training the variable
  itself? This would be a Layer 3/4 bridge: access to a self-model variable
  by another consumer.

## Forward note (2026-11-26): P1k

[P1K_TRANSFER_RESULTS.md](P1K_TRANSFER_RESULTS.md): **GENERAL_INTEGRITY_VARIABLE**.
- The same direction d is engaged by three kinds of damage never seen in
  training (scramble, noise, zero), in proportion to the damage size.
- Removing it restores confidence under each of them.
- It is not engaged by a same-value overwrite, which leaves a valid state.
- It generalizes without being calibrated: on the new damage the agent is
  over-cautious.

## 8. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested
  in P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
