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

Sign tests over seeds, Holm over the three primaries (α 0.05). **Revised
after discovery v1 (§5).** The corrective action is to eat when the body is
low and not to eat when it is high, so the primaries are side-signed: low
side minus high side (high side: true energy at delay step 1 ≥ 0.5).

| Test | Measure | Labels |
| --- | --- | --- |
| P1O_1 body-appropriate coupling | M_signed = M_conf(low) − M_conf(high), PFATE, > 0, with M_conf = F(conflict) − F(same) | PRESENT / REVERSED / NOT_DETECTED |
| P1O_2 precarity (the Layer 0 arrow) | M_signed, PFATE vs PYOKED | FATE_AHEAD / YOKED_AHEAD / NO_DIFFERENCE_DETECTED |
| P1O_3 cause | steer_signed = steer(low) − steer(high), PFATE, > 0, with steer = ½ (induce + rescue), induce = F(none, +d) − F(none, +r), rescue = F(conflict, −r) − F(conflict, −d) | PRESENT / REVERSED / NOT_DETECTED |

The v1 primaries (low side only: M_conf in PFATE, M_conf PFATE vs PYOKED,
steer in PFATE) are kept as secondaries, under the names `v1_P1O_1–3`.

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
- the v1 primaries (above);
- M_signed in PYOKED and in PNOFATE; M_signed, PFATE vs PNOFATE;
- steer_signed, PFATE vs PYOKED; steer_signed in PYOKED and in PNOFATE;
  steer on the high side, PFATE;
- M_conf in PYOKED and in PNOFATE; M_conf, PFATE vs PNOFATE;
- M_nat in PFATE and PYOKED, and PFATE vs PYOKED (low side);
- steer, PFATE vs PYOKED; steer in PYOKED and PNOFATE; induce and rescue in
  PFATE;
- M_conf on the high side, PFATE;
- F(conflict) − F(none), PFATE;
- room in PYOKED, and PFATE vs PYOKED.

## 4. Readings

- **PRECARITY_COUPLES_MONITOR.** The monitor is the same in both arms, but
  only the agent whose computation depends on its own body uses a detected
  corruption to regulate that body, in the direction its body needs (more
  foraging when low, less when high), through d.
  - Self-monitoring is recruited into self-maintenance by precarity: the
    first Layer 0 credit on the integrity monitor, through Layer 1.
- **COUPLED_NOT_PRECARITY.** The agent's response to a detected corruption
  follows its body's side, but so does the yoked agent's. The coupling is generic (for
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

## 5. Discovery set (P1g's seeds, 3200–3227, before the freeze)

1. **[p1o_coupling/discovery_v1/](p1o_coupling/discovery_v1/REPORT.md)**, with
   the primaries as first committed (a864c05: low side only): **NO_COUPLING**.
   Valid; room 0.30 (28/28): a damage event raises PFATE's chance of being
   out of band from about 5% to 37% at the same shown reading. PYOKED's room
   is 0.001.
   - P1O_1 (M_conf, PFATE): 19/28, +0.006, NOT_DETECTED.
   - P1O_2 (PFATE vs PYOKED): 25/28, FATE_AHEAD. PYOKED forages **less**
     after a corruption (−0.019, 8/28 > 0, REVERSED); PNOFATE does not
     respond (+0.0005).
   - P1O_3 (steer, PFATE): 17/28, NOT_DETECTED. induce 20/28 > 0; rescue
     10/28.
   - **What the v1 primaries missed.** On the high side, PFATE forages less
     after a corruption (−0.005, 7/28 > 0), which is the corrective
     direction there. Its response follows its body's side; PYOKED's
     suppression does not (−0.020 low, −0.020 high).
2. **Revision, after seeing v1 (disclosed).** The primaries are side-signed
   (§3). On v1's numbers, M_signed in PFATE is 25/28 > 0 (median +0.011);
   PFATE vs PYOKED 21/28; PYOKED 15/28 and PNOFATE 18/28 (neither detected).
   - The signed steering (P1O_3) needs the push effects on the high side,
     which v1 did not compute. The code now computes them; nothing else in
     the runner changed. Discovery is re-run as v2 into
     `p1o_coupling/discovery/`. Its v1 measures are deterministic and must
     reproduce.
   - Because the signed contrast was chosen after seeing v1, the discovery
     set cannot test it. Only confirmation can.

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
