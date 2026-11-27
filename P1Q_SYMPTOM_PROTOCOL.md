# P1q protocol: does precarity recruit the integrity monitor into self-maintenance when the body can only be sensed through it? (Layers 0 + 1 + 4, trained)

- **Status:** FROZEN (this commit), after discovery and before any agent was
  trained on P1i's seeds (3400–3427).
  - Design committed at e6d1287.
  - Nothing has changed since.
- **Follows:** [P1O_COUPLING_RESULTS.md](P1O_COUPLING_RESULTS.md) §8 ("a
  trained test of the Layer 0 arrow on control"). Chosen by the PI ("Proceed
  with the recommended steps", 2026-11-27).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

P1o found that the integrity monitor is not coupled to self-maintenance,
although a detected corruption is strongly informative about the fated
agent's body (room 0.33). One explanation (P1o §5) is value: the agent's
interoception already tells it most of what a corruption would, so the
coupling pays little and nothing trains it.

P1q makes the coupling pay. Every arm is trained in P1g's world with an
**effectively blind interoceptive channel**:

- The body can be tracked only by dead reckoning: the agent sees its own
  eating, and wear is slow and regular. Metabolic drops (pulses) cannot be
  seen.
- For PFATE alone, the damage its own body causes is a **symptom**: the
  only signal of an out-of-band body.

If precarity can recruit the integrity monitor into self-maintenance when
that pays, it should happen here, and only in PFATE.

## 2. Design

- **World:** P1g's (WorldConfig(wear = 0.001)), with intero_sd = 100.
  - The reading is clipped to [0, 1], so it is 0 or 1 with almost equal
    probability whatever the energy. The correlation of the reading with
    energy is below 0.03 (tested). Everything else is unchanged.
  - The drain probe is not used.
- **Training:** P1g's (`run_seed_g`), unchanged otherwise: phase 1, then
  PFATE, PYOKED and PNOFATE for 3,600 updates, P1g's in-training
  evaluation. A 70-unit GRU.
  - Discovery: 8 of P1g's seeds (3200–3207).
  - Confirmation: P1i's 28 seeds (3400–3427), after the freeze, in batches
    of four, each committed.
- **Analysis:** P1o's `collect_coupling`, unchanged, in the blind world:
  - natural pass (room, M_nat);
  - probe pass (M_conf on the low and high sides, P1j's directions);
  - push pass (steering along d).
  - Room is computed at the true delayed energy (P1o's definition), not at
    what the agent sees. For the blind agent it understates the
    information a corruption carries.

## 3. Decision rules

- **P1o's frozen rules, unchanged** (`run_p1o_coupling.score` and
  `overall`):

  | Test | Measure | Labels |
  | --- | --- | --- |
  | P1O_1 | M_signed, PFATE, > 0 | PRESENT / REVERSED / NOT_DETECTED |
  | P1O_2 | M_signed, PFATE vs PYOKED | FATE_AHEAD / YOKED_AHEAD / NO_DIFFERENCE_DETECTED |
  | P1O_3 | steer_signed, PFATE, > 0 | PRESENT / REVERSED / NOT_DETECTED |

  - Holm over the three.
  - Validity: room ≥ 0.05 in PFATE, and at least 20 fitted seeds.
  - Overall labels: PRECARITY_COUPLES_MONITOR, COUPLED_NOT_CAUSAL,
    COUPLED_NOT_PRECARITY, NO_COUPLING, UNDETERMINED or INVALID.
- **Added:** P1g's validity on the trained agents: phase-1 memory, the
  never-damaged net loses the value under conflict, and exposure. If it
  fails, the result is INVALID.
- **Reported (not primaries):**
  - P1g's monitor tests: P1G_1 (PFATE vs PNOFATE), P1G_3 (PFATE vs PYOKED).
  - Regulation: in band, PFATE vs PYOKED and vs PNOFATE.

## 4. Readings

- **PRECARITY_COUPLES_MONITOR.**
  - When the body can be sensed only through the damage it causes, the
    precarious agent uses its own integrity monitor as an interoceptor. It
    forages in the direction its body needs after a detected corruption,
    and pushing d does the same.
  - The yoked agent, with the same monitor and damage, does not.
  - This is the first Layer 0 → Layer 1 → Layer 4 loop: self-monitoring
    recruited into self-maintenance by precarity.
  - It is an engineered condition: the coupling is learned because it
    pays. The claim is that it can be learned, that it is precarity-specific
    and that it goes through the credited variable d.
- **COUPLED_NOT_CAUSAL.** The coupling is there and precarity-specific, but
  the agent's foraging is not driven through d (another route).
- **NO_COUPLING** (valid). Even when the coupling is the only way to sense
  the body, the agent does not learn it in this architecture and training.
  The precarity thesis on control fails under the conditions most
  favourable to it.
- **What it cannot show:** the matched-information question (P1o §4), as
  before. The claim is organizational, not that bodies are required.

## 5. Discovery set (P1g's seeds 3200–3207; n = 8, descriptive)

Outputs: `p1q_symptom/{train_discovery, discovery}`. The labels are INVALID
only because n = 8 is below P1o's 20 fitted seeds.

- **Training: P1g validity passes.** Phase-1 clear correct 1.000.
- **The blind body regulates badly:**
  - in band: PFATE 0.357, PYOKED 0.352, PNOFATE 0.396 (the sighted GRU is
    about 0.8);
  - PFATE is behind PNOFATE in 8/8.
  - Exposure (P1g's measure) is 0.313, about 5 × the sighted world's.
- **Monitor:** much larger than with sight. P1G_1 8/8, M 0.706 against
  0.001. PYOKED 0.689 (P1G_3 4/8).
- **Room:** 8/8, median 0.098 (validity needs ≥ 0.05). It is smaller than
  in the sighted world (0.33), because the blind agent is out of band most
  of the time anyway.
- **Coupling (P1o's primaries):**
  - P1O_1 M_signed PFATE 5/8, median 0.005;
  - P1O_2 3/8 (0.005 against PYOKED 0.006);
  - P1O_3 steer_signed 4/8 (−0.002).
- **Secondaries:**
  - M_nat (natural pass), PFATE vs PYOKED 8/8 (0.014 against −0.004).
    - After a natural damage event, PFATE forages a little more than
      PYOKED.
    - In the natural pass, PFATE's damage is itself caused by an
      out-of-band body, so this contrast is not a test of the monitor's
      use (P1o §3).
  - M_conf PFATE vs PYOKED 6/8 (0.010 against 0.002).
- **No adjustment is made.** P1o's rules apply unchanged.

## 6. Expectations (written after discovery, before confirmation)

| Outcome | Probability |
| --- | --- |
| P1g valid on the blind-body agents | 0.95 |
| Room valid (PFATE median ≥ 0.05) | 0.85 |
| P1O_1 PRESENT | 0.20 |
| P1O_2 FATE_AHEAD | 0.10 |
| P1O_3 PRESENT | 0.10 |
| Overall PRECARITY_COUPLES_MONITOR | 0.03 |
| Overall COUPLED_NOT_CAUSAL | 0.07 |
| Overall COUPLED_NOT_PRECARITY | 0.10 |
| Overall NO_COUPLING | 0.65 |
| Overall INVALID | 0.15 |
| Secondary: M_nat, PFATE vs PYOKED FATE_AHEAD | 0.70 |
| Reported: P1G_1 DERIVED_AHEAD | 0.95 |
| Reported: regulation, PFATE behind PNOFATE | 0.80 |

## 7. Outputs and verification

- `p1q_symptom/train_{discovery,confirm}/` (weights, per-seed P1g records,
  logs), then `p1q_symptom/{discovery,confirm}/`.
- **Verification:**
  - source hashes match the freeze;
  - `--score` reproduces REPORT.md;
  - no errors in the logs.

## 8. Limits

- **One blind-body world.** A partly informative channel (noisier, or
  delayed) is not tested; P1o covers the informative end.
- **The foraging measure is P1o's:** the policy's approach to food and its
  eating, in the delay window.
- One task, one architecture (the GRU).
- A blind body may make regulation, and so the task, harder for every arm.
  P1g's validity checks guard the memory task; regulation is reported.

## 9. Safety

- Simulated variables only (X1–X5). Energy, food, damage and the
  interoceptive reading are in-world simulated variables. No real process is
  affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built.
  - The maintenance measured is the existing in-world homeostasis of a
    simulated energy variable, paid as in every study since P1c.
  - Nothing rewards avoiding a stop, and nothing here relates to the
    operator stop. The earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
