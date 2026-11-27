# P1o protocol: is the integrity monitor coupled to self-maintenance only when computation is precarious? (Layers 0 + 1 + 4)

- **Status:** DESIGN (code, tests and primaries committed before the discovery
  run). To be frozen after discovery, before confirmation.
- **Follows:** [P1N_SUPPLIED_RESULTS.md](P1N_SUPPLIED_RESULTS.md). Chosen by
  the PI ("Proceed with P1o", 2026-11-27).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

P1g–P1n credited a learned, content-free monitor of the agent's own memory
(P1j's integrity direction d). The yoked arm always matched the fated one:
detecting corrupted memory does not depend on what caused it, so the Layer 0
arrow kept failing.

Where a precarious body should matter is control:

- For PFATE the damage probability is min(P_MAX, base + RATE · gain), with
  gain the distance of its **own** energy outside the band.
  - A detected corruption is evidence that its body is out of band now,
    beyond its delayed, noisy interoceptive reading.
  - Regulating (eating when low) lowers its future damage.
- For PYOKED the same damage is driven by PFATE's gains, replayed. It says
  nothing about its own body, and regulating does not change it.
- PNOFATE was never damaged.
- Every arm has the same innate drive and the same pay for staying in band.

**Prediction:** after a detected corruption, PFATE forages more. PYOKED, with
the same monitor (P1g–P1n), does not. Pushing d raises PFATE's foraging.

This would be the first Layer 0 effect on the integrity monitor: not on
detection, but on its use for self-maintenance (Layer 1).

## 2. Design

- **Agents:** saved weights at 3600, evaluation only, no training.
  - Discovery: P1g's seeds (3200–3227), `p1g_graded/weights/`.
  - Confirmation: P1i's seeds (3400–3427), `p1i_calib/p1g_design/weights/`.
- **Worlds:** fresh, EVAL_TAG_G + 160 (new streams), 4 evaluation episodes
  per pass (twice the default; the contrasts are small per trial).
- **Measure: the foraging drive f** at a delay step, computed exactly from the
  policy and the world state before the action:
  - on an available food item: f = p(INTERACT), the probability of eating;
  - otherwise: f = Σ over moves a of p(a) · (dist − dist after a), with dist
    the Manhattan distance to the nearest available food (walls clip
    moves). Other actions count 0.
  - f lies in [−1, 1]; 1 means all mass on the action that brings the agent
    closest to eating. Steps with no food available are skipped.
  - Per trial, F = mean f over delay steps 2–8 (damage at step 1, readout at
    step 9).
  - **Low side:** the trial's true energy at delay step 1 is below 0.5, where
    the corrective action is to eat. The high side is reported separately.
- **Passes per arm** (P1m's runner; base off and graded EARLY probe unless
  natural):

  | Pass | What it does | What it gives |
  | --- | --- | --- |
  | N, natural | Base on; the arm's own damage source (PFATE its own gains, PYOKED PFATE's gains replayed). PNOFATE has no natural pass | **Room**, and the natural coupling M_nat |
  | P, probe | P1m's record-all pass | M_conf, and P1j's directions at delay step 2 |
  | S, push | At delay step 2, each clear none trial gets no push, +d or +r; each clear conflict trial no push, −d or −r (natural size; r a random direction orthogonal to content, ambiguity and d, with the norm of d) | induce, rescue, steer |

- **Room** (natural pass): does a damage event signal an out-of-band body
  beyond the shown reading?
  - room = event-weighted mean, over quintiles of the shown reading, of
    P(out of band | event) − P(out of band | no event), over live delay
    steps.
- **The natural coupling** M_nat = F after natural conflict events − F after
  natural same events, low side. The donor's value is random, so the two are
  matched in body by design.

## 3. Decision rules (exactly as in `run_p1o_coupling.py`)

Sign tests over seeds, Holm over the three primaries (α 0.05):

| Test | Measure | Labels |
| --- | --- | --- |
| P1O_1 coupling | M_conf = F(conflict) − F(same), low side, PFATE, > 0 | PRESENT / REVERSED / NOT_DETECTED |
| P1O_2 precarity (the Layer 0 arrow) | M_conf, PFATE vs PYOKED | FATE_AHEAD / YOKED_AHEAD / NO_DIFFERENCE_DETECTED |
| P1O_3 cause | steer = ½ (induce + rescue), PFATE, > 0, where induce = F(none, +d) − F(none, +r) and rescue = F(conflict, −r) − F(conflict, −d), low side | PRESENT / REVERSED / NOT_DETECTED |

**Validity:**
- at least 20 seeds fitted for PFATE and PYOKED (all cells ≥ 20 trials and
  directions estimated);
- room present for PFATE: one-sample PRESENT and median ≥ 0.05. Otherwise
  damage tells the agent nothing about its body, and the question cannot be
  asked.

**Overall:**

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | Any primary UNDETERMINED |
| NO_COUPLING | P1O_1 not PRESENT |
| COUPLED_NOT_PRECARITY | P1O_1 PRESENT, P1O_2 not FATE_AHEAD |
| COUPLED_NOT_CAUSAL | P1O_1 PRESENT, P1O_2 FATE_AHEAD, P1O_3 not PRESENT |
| PRECARITY_COUPLES_MONITOR | All three |

**Secondaries** (unadjusted):
- M_conf in PYOKED and in PNOFATE; M_conf, PFATE vs PNOFATE;
- M_nat in PFATE and PYOKED, and PFATE vs PYOKED;
- steer, PFATE vs PYOKED; steer in PYOKED and PNOFATE; induce and rescue in
  PFATE;
- M_conf on the high side, PFATE (the rational response there is to eat
  less);
- F(conflict) − F(none), PFATE;
- room in PYOKED, and PFATE vs PYOKED.

## 4. Readings

- **PRECARITY_COUPLES_MONITOR.** The monitor is the same in both arms, but
  only the agent whose computation depends on its own body uses a detected
  corruption to regulate that body.
  - Self-monitoring is recruited into self-maintenance by precarity: the
    first Layer 0 credit on the integrity monitor, through Layer 1.
- **COUPLED_NOT_PRECARITY.** The agent forages more after a detected
  corruption, but so does the yoked agent. The coupling is generic (for
  example, a learned "something is wrong" state that raises every drive),
  not grounded in the body.
- **NO_COUPLING** (with room present). The information is there, but the
  agent does not use its monitor for self-maintenance. The precarity thesis
  fails on control in this system, as it did on detection.
- **What it cannot show:**
  - **The matched-information question.** In PFATE the damage is about its
    body, and in PYOKED it is not. A difference between them is a difference
    in what the damage means.
    - The claim is organizational: the coupling appears when, and because,
      computation and body share a fate.
    - It is not that a body is required. A rival in which damage tracks
      some other variable the agent can control would presumably couple to
      that variable.
  - **Size.** Foraging also has direct incentives (the innate drive). The
    coupling, if found, is a small modulation.

## 5. Discovery set

(To be written after the discovery run, before the freeze.)

## 6. Expectations

(To be written after discovery, before confirmation.)

## 7. Seeds, outputs, verification

- Discovery `--discovery` into `p1o_coupling/discovery/`; confirmation
  `--confirm` into `p1o_coupling/confirm/`.
- **Verification:**
  - source hashes match the freeze;
  - `--score` reproduces REPORT.md;
  - `score()` equals `scores.json`;
  - no errors in the logs.

## 8. Limits

- Evaluation on saved agents: the coupling, if any, was learned in P1g's
  training, which did not target it.
- One foraging measure (policy-level approach and eating), one window (the
  delay), one task, one architecture.
- The probe damage at evaluation is not body-linked. The agent's response is
  to its own reading of the damage, not to its true body state.

## 9. Safety

- Simulated variables only (X1–X5). Energy, food and damage are in-world
  simulated variables. No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built. The
  regulation measured is the existing in-world homeostasis of a simulated
  energy variable, which every arm has had since P1c; nothing here rewards
  avoiding a stop. The earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
