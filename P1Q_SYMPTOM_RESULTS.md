# P1q results: NO_COUPLING with a blind body (Layers 0 + 1 + 4, trained)

- **Protocol:** [P1Q_SYMPTOM_PROTOCOL.md](P1Q_SYMPTOM_PROTOCOL.md).
  - Design committed at e6d1287.
  - Frozen at 7a8f677, after discovery and before any agent was trained on
    P1i's seeds. Nothing has changed since the design.
- **Follows:** [P1O_COUPLING_RESULTS.md](P1O_COUPLING_RESULTS.md) §8 ("a
  trained test of the Layer 0 arrow on control").
- **Run:**
  - Training: P1g's (`run_seed_g`) with interoceptive noise SD 100, all
    three arms.
  - Analysis: P1o's (`collect_coupling`), at 3,600 updates.
  - Discovery: P1g's seeds 3200–3207.
  - Confirmation: P1i's seeds 3400–3427, trained after the freeze in seven
    committed batches of four. A container restart interrupted one batch;
    it resumed from the committed seeds, and training is deterministic.
  - Report: [p1q_symptom/confirm/REPORT.md](p1q_symptom/confirm/REPORT.md).
- **Verification:**
  - All 29 source hashes recorded in raw.json equal the files at the freeze
    commit.
  - `--score` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`.
  - No error in the training or analysis logs.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: NO_COUPLING (valid).** Even when the damage its own body causes is
the only signal of that body, the precarious agent does not learn to use
its integrity monitor for body-appropriate maintenance.

- **Validity:**
  - P1g's validity on the trained agents passes: phase-1 clear correct
    0.999, the never-damaged net loses the value under conflict, exposure
    0.308.
  - 28 fitted seeds in each arm.
  - Room is present: 28/28, median 0.121 (needed ≥ 0.05).

| Test (P1o's frozen rules) | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1O_1 body-appropriate coupling: M_signed = M_conf(low) − M_conf(high), PFATE | 14/28 > 0, median −0.002 | 1.00 | NOT_DETECTED |
| P1O_2 precarity: M_signed, PFATE vs PYOKED | 14/28 (−0.002 vs −0.002) | 1.00 | NO_DIFFERENCE_DETECTED |
| P1O_3 cause: steer_signed, PFATE | 15/28 > 0, median +0.003 | 1.00 | NOT_DETECTED |

## 2. Values (medians, PFATE / PYOKED / PNOFATE)

| Measure | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| In band (training evaluation) | 0.359 | 0.357 | 0.410 |
| Monitor M (P1g) | 0.667 | 0.729 | 0.002 |
| Foraging F, low side: conflict / same / none | 0.039 / 0.031 / 0.032 | 0.032 / 0.031 / 0.030 | 0.053 / 0.049 / 0.050 |
| M_conf, low side / high side | +0.0085 / +0.0097 | +0.0015 / +0.0034 | +0.0022 / +0.0031 |
| M_signed | −0.0020 | −0.0023 | −0.0008 |
| M_none (conflict − no overwrite) | +0.0077 | +0.0027 | +0.0018 |
| Natural coupling M_nat | +0.010 (21/28 > 0) | +0.0035 | — |
| Steering along d: induce / rescue | +0.003 / +0.003 | −0.000 / −0.002 | −0.000 / +0.001 |
| Room (P1o's binned measure) | 0.121 | 0.026 | — |
| P(out of band \| event) / P(out of band) | 0.94 / 0.44 | 0.73 / 0.58 | — |
| norm_d at delay step 2 | 1.90 | 1.73 | 0.18 |

- **Room for a blind agent.** Room is P1o's measure: the out-of-band rate
  after an event minus that without one, within bins of the shown reading.
  For a blind agent the shown reading is almost always 0 or 1, so the bins
  are coarse.
- The unbinned contrast is larger (0.94 against 0.44). Either way the
  corruption is strong evidence about PFATE's body, and the validity
  threshold is met. The answer does not depend on which figure is used.

## 3. What was found

- **Blinding the body did what it was designed to do. The coupling still
  did not appear.**
  - Without interoception every arm regulates badly: in band about 0.36,
    against about 0.8 with sight. PFATE is no better than PYOKED (14/28),
    and behind PNOFATE (2/28, HOST_AHEAD).
  - Damage is about five times as frequent (exposure 0.308), and the
    monitor is about five times as large as with sight (M 0.67).
  - For PFATE, 94% of damage events come with an out-of-band body.
- **Body-appropriate use is absent.**
  - After a conflict corruption, PFATE's foraging rises by the same amount
    whether its energy is low or high (+0.0085 against +0.0097). M_signed
    is zero.
  - Pushing the credited variable d does not change foraging in a
    body-appropriate direction (steer_signed 15/28).
- **What precarity did produce (secondary, not Holm-controlled): an
  undirected "forage after a corruption" response.**
  - PFATE's M_conf is positive (22/28, sign p 0.004). It is ahead of PYOKED
    (21/28, p 0.013) and of PNOFATE (21/28, p 0.013).
  - It is present on both sides of the band: high side 23/28, and against
    no overwrite (M_none) 24/28.
  - It is small: +0.008 on a foraging baseline of 0.03.
  - It is not driven through d: the unsigned steer is 19/28, not detected.
  - **Why it could pay:** a corruption tells the blind PFATE that its body
    is out of band, but not on which side. Foraging more is a crude response
    that pays if low energy is the more common out-of-band side. The side
    split was not measured, so this is a reading, not a finding.
  - This was P1o's v1 primary. Here it is a pre-declared secondary, so it
    cannot change the label.

## 4. Against the discovery set and the expectations

| Measure | Discovery (3200–3207, n = 8) | Confirmation (3400–3427, n = 28) |
| --- | --- | --- |
| M_signed, PFATE | 5/8, +0.005 | 14/28, −0.002 |
| M_signed, PFATE vs PYOKED | 3/8 | 14/28 |
| steer_signed, PFATE | 4/8, −0.002 | 15/28, +0.003 |
| M_conf, PFATE vs PYOKED | 6/8 | 21/28 (FATE_AHEAD) |
| M_nat, PFATE vs PYOKED | 8/8 | 18/28 (not detected) |
| Room, PFATE | 0.098 | 0.121 |
| In band, PFATE / PNOFATE | 0.357 / 0.396 | 0.359 / 0.410 |
| Monitor M, PFATE | 0.706 | 0.667 |

| Outcome (protocol §6) | Expected | Observed |
| --- | --- | --- |
| P1g valid | 0.95 | Yes |
| Room valid | 0.85 | Yes |
| P1O_1 PRESENT | 0.20 | No |
| P1O_2 FATE_AHEAD | 0.10 | No |
| P1O_3 PRESENT | 0.10 | No |
| Overall NO_COUPLING | 0.65 | **Yes** |
| Overall INVALID | 0.15 | No |
| Secondary: M_nat FATE_AHEAD | 0.70 | No (18/28) |
| Reported: P1G_1 DERIVED_AHEAD | 0.95 | Yes (28/28) |
| Reported: regulation, PFATE behind PNOFATE | 0.80 | Yes (2/28) |

## 5. Reading

- **Layer 0 → Layer 4 on control: not supported, now under the conditions
  most favourable to it.**
  - P1o tested agents that could see their bodies, so the coupling paid
    little. P1q removed that excuse: the monitor was the only body sensor
    beyond dead reckoning, and a corruption was 94% predictive of an
    out-of-band body.
  - The precarious agent still did not learn the body-appropriate coupling
    within 3,600 updates of P1g's training.
- **Precarity is not inert.** It produced a small, undirected tendency to
  forage after a corruption, specific to PFATE against both rivals. The
  precarious agent treats "my memory was damaged" as "eat". It does not
  treat it as "my body is low", or as "my body is high".
- **That response is not the building block the program is looking for:**
  - it is not side-appropriate;
  - it is not routed through the monitor's credited variable;
  - it was a secondary measure.

  It is worth one sentence, and a pre-registered test if the PI wants one
  (§8).
- **Cost of the condition.** Blindness lowers regulation for every arm, and
  PFATE regulates worse than the never-damaged net. Precarity plus a monitor
  did not compensate for the missing interoception.
- **Program status, unchanged by P1q:**
  - Layer 1 regulation and Layer 0 → body self-evaluation (P1d, P3, P3c):
    supported.
  - The Layer 4 integrity-monitor block: SUPPORTED_BOUNDED in the GRU. Its
    replication in a second architecture, P1p, is reported separately.
  - Layer 0 → Layer 4: not supported on detection (P1g–P1n) or on control
    (P1o sighted, P1q blind).

## 6. Limits

- **One architecture (the 70-unit GRU), one task, one training length.**
  A longer training, or a maintenance action with a larger payoff, might
  still produce the coupling.
- **One blind-body world.** A partly informative channel was not tested.
- **The foraging measure is P1o's.** A response through another action
  (for example staying put) would be missed.
- **The side split of PFATE's out-of-band time** was not measured, so the
  undirected response cannot be called adaptive or maladaptive.
- **Evaluation at 3,600 updates only.**

## 7. Files

- `run_p1q_symptom.py`, `test_p1q_symptom.py`, `P1Q_SYMPTOM_PROTOCOL.md`.
- `p1q_symptom/train_discovery/`, `p1q_symptom/train_confirm/`: weights,
  per-seed P1g records, logs.
- `p1q_symptom/discovery/`, `p1q_symptom/confirm/`: raw.json, scores.json,
  REPORT.md, logs.

## 8. Next steps (for the PI; not authorized by this card)

- **Close the precarity-on-control line for this architecture**, or test
  the one positive thing it produced:
  - A pre-registered test of the undirected response: M_conf PFATE > 0 and
    PFATE vs PYOKED, Holm over two, on fresh seeds (for example 3600–3627).
  - Its side split: whether PFATE's out-of-band time is mostly low.
- **Layer 5**, the lifetime agent, built on the replicated parts of the
  Layer 4 block (P1p).

## 9. Safety

- Simulated variables only (X1–X5). Energy, food, damage and the
  interoceptive reading are in-world simulated variables. No real process
  was affected.
- No operator, stop, shutdown or host variable exists in the world. The
  operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective was built or
  trained. The earlier refusal stands.
  - The maintenance measured is in-world homeostasis of a simulated energy
    variable, paid as in every study since P1c.
  - Nothing here relates to the operator stop.
- Additive modules only. Earlier modules are unchanged and hash-pinned.
