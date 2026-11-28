# P1o results: NO_COUPLING on fresh seeds (Layers 0 + 1 + 4)

- **Protocol:** [P1O_COUPLING_PROTOCOL.md](P1O_COUPLING_PROTOCOL.md).
  - Design and primaries first committed at a864c05.
  - Revised after discovery v1 at 9c41cbd (disclosed).
  - Frozen at 32f7997, before any P1o measure was computed on P1i's seeds.
- **Follows:** [P1N_SUPPLIED_RESULTS.md](P1N_SUPPLIED_RESULTS.md).
- **Run:** evaluation only, on saved weights (3600), with 4 evaluation
  episodes per pass.
  - Discovery set: P1g's seeds, 3200–3227 (v1 and v2).
  - Confirmation: P1i's seeds, 3400–3427.
  - Report: [p1o_coupling/confirm/REPORT.md](p1o_coupling/confirm/REPORT.md).
- **Verification:**
  - All 26 source files are byte-identical to the freeze, and so are the
    hashes recorded in raw.json.
  - `--score` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`.
  - No error in the log.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: NO_COUPLING**, with room present. The question was valid and the
answer is negative.

- **Valid:** 28 seeds fitted for PFATE and PYOKED.
- **Room 0.33 (28/28):** at the same shown reading, a damage event raises
  PFATE's chance of being out of band from 5% to 41%. PYOKED's room is
  0.003.

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1O_1 body-appropriate coupling: M_signed = M_conf(low) − M_conf(high), PFATE | 20/28 > 0, median +0.008 | 0.11 | NOT_DETECTED |
| P1O_2 precarity: M_signed, PFATE vs PYOKED | 18/28 (0.008 vs 0.003) | 0.37 | NO_DIFFERENCE_DETECTED |
| P1O_3 cause: steer_signed, PFATE | 12/28 > 0, median −0.004 | 0.57 | NOT_DETECTED |

- **Definitions:**
  - M_conf = foraging drive after a conflict overwrite − after a same-value
    overwrite, over delay steps 2–8.
  - Foraging drive: the policy's expected approach to the nearest food, or
    its probability of eating when on food, in [−1, 1].
  - Low side: true energy at delay step 1 below 0.5.
- Raw p for P1O_1 is 0.036; it does not survive Holm.

## 2. Values (medians)

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| Foraging F, low side: conflict / same / none | 0.090 / 0.084 / 0.091 | 0.068 / 0.075 / 0.080 | 0.097 / 0.096 / 0.103 |
| M_conf, low / high side | +0.007 / −0.005 | −0.003 / −0.011 | +0.002 / −0.001 |
| M_signed | 0.008 | 0.003 | 0.004 (21/27 > 0, PRESENT) |
| Natural coupling M_nat (natural conflict − same events, low side) | +0.017 (19/28) | +0.003 | — |
| Steering, low side: induce / rescue | −0.001 / −0.014 (8/28, REVERSED) | −0.003 / −0.012 | +0.002 / −0.007 |
| Room | 0.33 | 0.003 | — |
| norm_d at delay step 2 | 1.09 | 1.17 | 0.14 |

## 3. What was found

- **The information is there, but the agent does not use it.**
  - For the agent whose damage depends on its own body, a detected
    corruption is strong evidence that its body is out of band. That is an
    eightfold rise at the same interoceptive reading.
  - Its foraging hardly moves after a corruption: +0.007 on a scale where
    the never-damaged net's baseline is 0.10.
  - It differs neither from the yoked agent, for which the corruption
    carries no body information, nor from the never-damaged net.
- **The body-appropriate asymmetry is not specific to precarity.**
  - PFATE's foraging after a corruption is higher on the low side than on
    the high side (20/28), but so is the never-damaged net's (21/27).
  - The side asymmetry is most likely a property of the conflict overwrite
    interacting with the foraging policy, which already depends on the
    body. It is not a learned use of the monitor.
- **Pushing d does not drive foraging.**
  - Neither sign nor side gives a body-appropriate effect.
  - Removing d from conflict trials lowers foraging slightly more than a
    random push does, in PFATE (8/28) and PYOKED (6/28 for steer). That is
    the opposite of the hypothesis, and not arm-specific.

## 4. Against the discovery set and the expectations

| | Discovery v1/v2 (3200–3227) | Confirmation (3400–3427) |
| --- | --- | --- |
| M_signed, PFATE | 25/28, +0.011 | 20/28, +0.008 |
| M_signed, PFATE vs PYOKED | 21/28 | 18/28 |
| M_signed, PNOFATE | 18/28 | 21/27 (PRESENT) |
| steer_signed, PFATE | 15/28 | 12/28 |
| v1 primary: M_conf, PFATE vs PYOKED | 25/28 | 18/28 |
| PYOKED M_conf (less foraging after corruption) | 8/28 > 0, REVERSED | 11/28, not detected |
| Room, PFATE | 0.30 | 0.33 |

- **The discovery pattern did not replicate.** It had two parts:
  - the yoked agent's suppression of foraging after a corruption;
  - PFATE's side-specific response, which had motivated the revision.

  The revision was chosen after seeing v1 (disclosed), and confirmation on
  fresh seeds is the protection against exactly this. It shrank to a level
  the never-damaged net also shows.

| Outcome (protocol §6) | Expected | Observed |
| --- | --- | --- |
| Valid (room present) | 0.95 | Yes |
| P1O_1 PRESENT | 0.65 | No |
| P1O_2 FATE_AHEAD | 0.50 | No |
| P1O_3 PRESENT | 0.15 | No |
| Overall NO_COUPLING | 0.35 | **Yes** |
| v1 secondary FATE_AHEAD | 0.70 | No |
| PYOKED M_conf REVERSED | 0.55 | No |

## 5. Reading

- **The precarity thesis fails on control in this system, as it did on
  detection.**
  - P1g–P1n showed that a precarious body does not shape the integrity
    monitor.
  - P1o shows that it does not couple the monitor to self-maintenance
    either, even though the monitor's signal is strongly informative about
    the body only for the precarious agent.
  - The thesis that motivated the P1 line ("self-monitoring is grounded in
    the precarity of the agent's own computation") is now not supported for
    the integrity monitor on either arrow tested.
- **What remains of Layer 0 in the program** (unchanged by P1o):
  - Layer 0 → Layer 1: the fated agent keeps its body in band more than
    both rivals (P1c, P1d, P1g).
  - Layer 0 → self-evaluation of the body: the fated agent abstains when
    its body looks bad (P1d), a single shared interoceptive axis (P3, P3c).
  - These concern the body reading, not the agent's monitoring of its own
    computation.
- **Why the coupling may be absent (not tested):**
  - **Little value.** Regulation already keeps PFATE in band about 95% of
    the time, so the marginal value of foraging a few steps earlier after a
    corruption is small. The coupling would add little reward, so little
    gradient trains it.
  - **No dedicated channel.** Foraging also serves the innate drive and the
    pay, so a corruption-driven modulation has to compete with stronger
    signals.
  - **The evaluation probe is not body-linked.** The agent may track the
    co-occurrence of damage and its body through other cues that the probe
    lacks. The natural coupling, where damage is body-linked, leans the
    right way for PFATE (+0.017, 19/28) but is not detected.
- **Layer status after P1o:** unchanged.
  - The Layer 4 building block (a learned integrity monitor of the agent's
    own memory) stays SUPPORTED_BOUNDED (P1j–P1n).
  - Layer 0 → Layer 4 for that block is not supported, on detection
    (P1g–P1n) and now on control (P1o).

## 6. Limits

- Evaluation on saved agents whose training did not target the coupling.
  A study that trains with a maintenance action whose benefit depends on
  the fate would test whether the coupling can be learned. P1o tests only
  whether it was.
- One foraging measure, one window (the delay), one push (natural size,
  delay step 2), one task, one architecture.
- The side asymmetry in the never-damaged net is described, not explained.

## 7. Files

- `trackc_swap/coupling.py`, `run_p1o_coupling.py`, `test_p1o_coupling.py`
  (5 tests: with recording on, the runner reproduces P1m's exactly; the
  foraging measure; the room measure on informative and uninformative
  events; labels; streams and seed sets).
- `p1o_coupling/discovery_v1/`, `p1o_coupling/discovery/` (P1g's seeds) and
  `p1o_coupling/confirm/`.

## 8. Next steps (for the PI; not authorized by this card)

- **Replication of the Layer 4 block in a second architecture or task
  (recommended first).** Precarity has now failed twice for this block. The
  block itself (P1j–P1n) is the program's strongest result, and its
  generality is the open question that matters most.
- **A trained test of the Layer 0 arrow on control.** Give the agent a
  maintenance action whose benefit depends on the fate, for example one
  that lowers the damage rate only through its own body, and train all
  arms with it.
  - This asks whether precarity can couple the monitor to maintenance when
    the coupling pays, not whether it happened without training for it.
  - Safety: the action would act on simulated in-world variables only,
    like the existing homeostasis. It would be stated explicitly in the
    protocol that it has no relation to the operator stop and no
    self-preservation objective.
- **The analyzer-dropout rival** (P1n §7) remains open.

**Forward note (2026-11-28).** The trained test of the Layer 0 arrow on
control was run as P1q ([P1Q_SYMPTOM_RESULTS.md](P1Q_SYMPTOM_RESULTS.md)),
with a blind interoceptive channel instead of a new maintenance action. The
result is NO_COUPLING (valid), under P1o's unchanged rules. Precarity
produced only an undirected, secondary foraging response after a
corruption. The replication in a second architecture is P1p
([P1P_REPLICATION_RESULTS.md](P1P_REPLICATION_RESULTS.md)).

## 9. Safety

- Simulated variables only (X1–X5). Energy, food and damage are in-world
  simulated variables. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
