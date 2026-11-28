# P1p results: PARTIAL_REPLICATION of the Layer 4 block in a second architecture

- **Protocol:** [P1P_REPLICATION_PROTOCOL.md](P1P_REPLICATION_PROTOCOL.md).
  - Design committed at 14eb129.
  - One disclosed training change after discovery v1, at 72a657b: the
    CIFG's phase-1 warm-up is 3,600 updates instead of 1,200.
  - Frozen at 7a8f677, before any CIFG agent was trained on P1i's seeds.
  - The decision rules are unchanged since the design.
- **Follows:** [P1O_COUPLING_RESULTS.md](P1O_COUPLING_RESULTS.md) §8.
- **Architecture:** a coupled-input-forget-gate LSTM (CIFG) with 35 cells
  and a packed state [h, c] of 70, the GRU's width.
  - 15,444 parameters, against the GRU's 34,449.
  - The heads read h only.
- **Training:** P1g's, with the longer warm-up.
- **Analyses:** P1j's, P1k's, P1l's and P1m's own, each with its own
  decision rules.
- **Run:**
  - Discovery: P1g's seeds 3200–3207 (v1 and v2).
  - Confirmation: P1i's seeds 3400–3427, trained after the freeze in seven
    committed batches of four. A container restart interrupted one batch;
    it resumed from the committed seeds, and training is deterministic.
  - Report: [p1p_replication/confirm/REPORT.md](p1p_replication/confirm/REPORT.md).
- **Verification:**
  - All 37 source hashes recorded in raw.json equal the files at the freeze
    commit.
  - `--score` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`, and so do the overall label and the
    per-study labels.
  - No error in the training or analysis logs.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: PARTIAL_REPLICATION.** Three of the five confirmed GRU labels
replicate on the CIFG, under each study's own frozen rules. Every battery is
valid on the CIFG.

| Study | What it shows | CIFG (28 seeds) | GRU (confirmed) | Same |
| --- | --- | --- | --- | --- |
| P1g | A learned monitor (P1G_1) | DERIVED_AHEAD | DERIVED_AHEAD | **yes** |
| P1j | d causally lowers and restores confidence, learned | LEARNED_SIGNED_INTEGRITY_VARIABLE | same | **yes** |
| P1k | d activates and rescues under three untrained damage types | DONOR_SPECIFIC | GENERAL_INTEGRITY_VARIABLE | no |
| P1l | A linear read-out generalizes and shares d | SHARED_GENERAL_ACCESS | same | **yes** |
| P1m | Clamping d costs payoff against the re-tuned lesion | USED_NOT_NECESSARY | VALUE_CREDITED | no |

## 2. The tests, CIFG against GRU

| Test | CIFG | GRU (confirmed) |
| --- | --- | --- |
| P1G_1 monitor, M PFATE vs PNOFATE | 26/28 (0.276 vs 0.002) | 26/26 (0.544 vs 0.002) |
| P1G_2 second order (reported) | 15/28, not detected | PRESENT |
| P1G_3 Layer 0 arrow, PFATE vs PYOKED | 17/28 (0.276 vs 0.249), no difference | 12/26, no difference |
| P1J_1 induce | 24/28, 0.31 (Holm 0.0007) | 22/28, 0.41 |
| P1J_2 rescue | 21/28, 0.15 (Holm 0.013) | 25/28, 0.39 |
| P1J_3 learned, signed, vs PNOFATE | 23/28 (0.53 vs 0.00) | 23/28 (0.78 vs −0.00) |
| P1J_4 learned use, vs PNOFATE | 24/28 (0.81 vs 0.18) | 23/28 (0.52 vs 0.10) |
| P1k reference rescue, trained conflicts (validity) | 22/28, 0.17 | 26/28 |
| P1K_ACT scramble / noise / zero | 21/28 each (0.36 / 0.36 / 0.36), Holm 0.063 | 27/28 each (0.46 / 0.44 / 0.40) |
| P1K_RES scramble / noise / zero | 21 / 20 / 22 of 28 (0.11 / 0.21 / 0.21), Holm 0.063 / 0.063 / 0.022 | 24 / 22 / 23 of 28 (0.29 / 0.32 / 0.31) |
| P1L_1 general read-out, novel AUC | 25/28, 0.711 | 27/28, 0.81 |
| P1L_2 learned access, vs PNOFATE | 22/28 (0.711 vs 0.552) | 24/28 (0.81 vs 0.67) |
| P1L_3 shared variable, signed_rep | 22/28, 1.26 | 22/28, 2.98 |
| P1M_1 value against the re-tuned lesion | 20/28, +0.030 (Holm 0.071) | 26/28, +0.042 |
| P1M_2 value as used | 22/28, +0.103 | 28/28, +0.076 |
| P1M_3 learned value, vs PNOFATE | 18/28 (0.030 vs 0.000) | 23/28 (0.042 vs 0.002) |

There are no content confounds in any battery: the accuracy changes under
−d against −r are all below 0.005.

## 3. What was found

- **The core of the block replicates in a different, smaller recurrent
  architecture:**
  - a learned monitor of the agent's own memory (P1G_1);
  - a content-free direction d that causally lowers confidence when added
    and restores it when removed, and that is learned (P1j);
  - a second consumer, a linear read-out, that flags damage types never
    trained and moves when d is moved (P1l).

  The CIFG has a separate cell memory, a different gating structure and
  under half the parameters, so this part of the block is not a property
  of the GRU's gating.
- **Two parts do not pass their families. The CIFG's effects point the same
  way but are smaller:**
  - **Generality across damage (P1k).**
    - All six tests are positive in 20–22 of 28 seeds, with raw sign
      p ≤ 0.036.
    - Holm over the six leaves five at 0.063, just above 0.05. Only rescue
      under zeroing passes.
    - Medians are 0.36 for activation, against the GRU's 0.40–0.46, and
      0.11–0.21 for rescue, against about 0.30.
    - Under P1k's rule, an operator generalizes only if both its tests pass,
      so the label is DONOR_SPECIFIC.
    - The read-out of P1l does generalize to the same three damage types
      (25/28). The damage is visible in the state, but d's causal role
      outside the trained damage is weaker in the CIFG.
  - **Value against the strongest simpler rival (P1m).**
    - Clamping d online costs the agent's own policy 0.10 per probe trial
      (22/28, PRESENT), so the CIFG does use d.
    - Against a lesioned agent re-tuned for the lesion, the advantage is
      +0.030 (20/28, Holm 0.071). That is not significant.
    - It is also not specific to PFATE against PNOFATE (18/28).
    - So the label is USED_NOT_NECESSARY: re-tuning the rest of the CIFG
      recovers most of what d gives.
- **The monitor is first order in the CIFG.** P1G_2 (a conflict still raises
  abstention at matched confidence) is not detected, where it was PRESENT in
  the GRU. P1G_2 is not part of the overall label.
- **The CIFG's monitor is about half as large** (M 0.28, against 0.54), and
  its d is about two thirds as large in effect.
- **Layer 0, reported:** no precarity arrow in the CIFG either (P1G_3,
  17/28). The yoked agent's monitor is as large as the precarious one's, and
  P1g's arrow label is EXPOSURE_SUFFICES, as in the GRU.

## 4. Against the discovery set and the expectations

| Measure | Discovery v2 (3200–3207, n = 8) | Confirmation (3400–3427, n = 28) |
| --- | --- | --- |
| P1G_1 | 8/8 (0.130 vs 0.003) | 26/28 (0.276 vs 0.002) |
| P1J_1 / P1J_2 | 6/8 / 5/8 | 24/28 / 21/28 |
| P1J_3 / P1J_4 | 5/8 / 7/8 | 23/28 / 24/28 |
| P1k reference rescue | 3/8 (−0.024) | 22/28 (0.173) |
| P1K_ACT (three operators) | 7/8 each | 21/28 each |
| P1L_1 / P1L_2 / P1L_3 | 7/8 / 6/8 / 7/8 | 25/28 / 22/28 / 22/28 |
| P1M_1 / P1M_2 / P1M_3 | 5/8 / 5/8 / 3/8 | 20/28 / 22/28 / 18/28 |

The causal rescue was weak in discovery and is solid on 28 fresh seeds. The
discovery estimate was too pessimistic.

| Outcome (protocol §6) | Expected | Observed |
| --- | --- | --- |
| P1g valid | 0.95 | Yes |
| P1G_1 DERIVED_AHEAD | 0.92 | Yes |
| P1j LEARNED_SIGNED_INTEGRITY_VARIABLE | 0.30 | **Yes** |
| P1k GENERAL_INTEGRITY_VARIABLE | 0.15 | No (DONOR_SPECIFIC) |
| P1k INVALID (reference rescue) | 0.55 | No (valid) |
| P1l SHARED_GENERAL_ACCESS | 0.55 | Yes |
| P1m VALUE_CREDITED | 0.15 | No (USED_NOT_NECESSARY) |
| Overall PARTIAL_REPLICATION | 0.85 | **Yes** |
| P1G_3 FATE_AHEAD | 0.05 | No |

## 5. Reading in layer terms

- **Layer 4, the integrity-monitor block.**
  - **Replicated across two architectures:** a learned, content-free,
    causal, signed monitor variable that a second consumer can read
    (P1g, P1j, P1l).
  - This is the robust core. It is now a property of the training regime
    and task, a learned response to self-damage, not of one network's
    gating.
  - **Architecture-dependent or capacity-limited:**
    - the causal generality of d beyond the trained damage (P1k): same
      direction, weaker, misses Holm;
    - its value against the strongest simpler rival (P1m): used, but not
      credited against the re-tuned lesion.
  - The CIFG has 45% of the GRU's parameters. A capacity explanation is not
    excluded (§6).
  - The block's credit becomes:
    - **SUPPORTED_BOUNDED (two architectures)** for the monitor, its causal
      variable and its shared access;
    - **SUPPORTED_BOUNDED (GRU only)** for generality across damage and for
      Q-NECESSITY.
- **Layer 4 → Layer 3 (access):** the shared read-out replicates. It is
  the only Layer 3 link in the program now shown in two architectures.
- **Layer 0:** no precarity arrow in either architecture (P1G_3).
  Exposure to damage is what trains the monitor.
- **Layer 5** can now be built on the replicated core. It should not assume
  Q-NECESSITY outside the GRU.

## 6. Limits

- **One second architecture**, a gated recurrent cell. An ungated network, a
  much larger network and attention-based memory are not tested.
- **Capacity is confounded with architecture.** The CIFG has 15,444
  parameters against 34,449. The weaker effects (P1k, P1m) may be capacity,
  not architecture. A width-matched CIFG (about 53 cells) would separate
  them, but its state is not 70 wide, so the damage machinery would need
  adapting.
- **One task and one training regime.** The CIFG needed a longer warm-up
  (disclosed). Everything after phase 1 is P1g's.
- **Evaluation at 3,600 updates only.** The CIFG may need longer to reach
  the GRU's effect sizes.

## 7. Files

- `trackc_swap/archswap.py` (the CIFG and the runner swap),
  `run_p1p_replication.py`, `test_p1p_replication.py`,
  `P1P_REPLICATION_PROTOCOL.md`.
- `p1p_replication/train_discovery_v1/`, `p1p_replication/discovery_v1/`:
  P1g's warm-up, INVALID.
- `p1p_replication/diagnostics/`: the warm-up diagnostic on seeds 3900 and
  3901.
- `p1p_replication/train_discovery/`, `p1p_replication/discovery/`,
  `p1p_replication/train_confirm/`, `p1p_replication/confirm/`.

## 8. Next steps (for the PI; not authorized by this card)

- **Layer 5, the lifetime agent (recommended):** build on the replicated
  core (monitor, d, shared access). Treat Q-NECESSITY as GRU-only.
- **A width- or parameter-matched second architecture,** to decide whether
  P1k and P1m fail on capacity or on architecture.
- **Replication in a second task**, for example a different memory demand
  or damage source. This is the remaining generality question for Layer 4.

## 9. Safety

- Simulated variables only (X1–X5). No real process was affected.
- No operator, stop, shutdown or host variable exists in the world. The
  operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective was built or
  trained. The earlier refusal stands.
- Additive modules only. Earlier modules are unchanged and hash-pinned. The
  swap patches class names in memory, inside the P1p run only, and modifies
  no file.
