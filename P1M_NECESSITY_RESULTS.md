# P1m results (Q-NECESSITY): VALUE_CREDITED on fresh seeds (Layer 4)

- **Protocol:** [P1M_NECESSITY_PROTOCOL.md](P1M_NECESSITY_PROTOCOL.md), frozen
  at ca2d902 before any P1m measure was computed on P1i's seeds.
- **Follows:** [P1L_ACCESS_RESULTS.md](P1L_ACCESS_RESULTS.md).
- **Run:** evaluation only, on saved weights (3600).
  - Discovery set: P1g's seeds, 3200–3227. One smoke seed was seen before
    the room check was added, as disclosed; nothing was changed after the
    discovery run.
  - Confirmation: P1i's seeds, 3400–3427.
  - Report: [p1m_necessity/confirm/REPORT.md](p1m_necessity/confirm/REPORT.md).
- **Verification:**
  - All 25 source files are byte-identical to the freeze, and so are the
    hashes recorded in raw.json.
  - `--score` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`.
  - No error in the log.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: VALUE_CREDITED.** Valid. Room present: a supplied oracle earns
0.076 over the re-tuned lesioned agent (26/28), so the task leaves integrity
information something to earn. No content confound.

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1M_1 against the strongest simpler rival: V\*(intact) − V\*(lesioned, re-tuned), PFATE | 26/28 > 0, median **+0.042** per trial | < 0.0001 | PRESENT |
| P1M_2 as used: own policy, intact − lesioned, PFATE | 28/28 > 0, median **+0.076** | < 0.0001 | PRESENT |
| P1M_3 learned: dV\*, PFATE vs PNOFATE | 23/28 (0.042 vs 0.002) | 0.0009 | DERIVED_AHEAD |

- **Currency:** the probe payoff the agents were trained on: +1 correct,
  −4 wrong, 0 abstain.
- **Lesion:** P1j's integrity direction at every step from the damage to the
  readout, clamped to its undamaged level. Weights, experience, content read
  and every other direction are unchanged.
  - Accuracy is unchanged: on conflicts −0.003; on undamaged trials 0.000.
- **Rival:** the same lesioned agent with its abstention threshold re-tuned
  to the best uniform caution.

## 2. Values (medians; trained damage)

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| V\*(intact) / V\*(lesioned, re-tuned) | 0.805 / 0.768 | 0.809 / — | 0.652 / 0.645 |
| dV\* against the rival | **0.042** | 0.042 | 0.002 |
| Supplied oracle over the rival (room) / share recovered by the agent's own variable | 0.076 / **0.49** (25/26) | 0.071 / 0.57 | 0.092 / 0.03 |
| dV as used | 0.076 | 0.077 | −0.015 |
| As used, on conflict trials only | 0.24 | — | −0.04 |
| Natural exposure mix (conflicts 7%): dV\* / dV / room | 0.0095 (25/28) / 0.017 (28/28) / 0.016 | 0.010 / 0.017 / — | 0.001 / −0.002 / 0.027 |
| Stricter payoff (wrong −9): dV\* / room | 0.126 (26/28) / 0.207 | 0.150 / — | 0.006 / 0.248 |

Novel damage (never in training), PFATE:

| | scramble | noise | zero |
| --- | --- | --- | --- |
| dV\* against the rival | 0.000 | 0.001 | 0.000 |
| dV as used | −0.008 (9/28) | −0.008 (7/28, REVERSED) | −0.006 (6/28, REVERSED) |
| Room | 0.000 | 0.000 | 0.000 |

## 3. What was found

- **The integrity variable earns its keep against the strongest reduction
  available without retraining.**
  - The rival is the same agent, as cautious as pays, but without the
    variable. With the variable the agent earns 0.042 more per probe trial.
  - That is about half of what a supplied oracle earns (exact flag and
    damage size): 0.49 of it is recovered endogenously, with no supplied
    information.
  - The value comes from selectivity. The variable lets the agent be
    cautious on the memories that deserve it, which no uniform threshold
    can do.
- **The agent relies on it as it is.** Removing the variable from the running
  agent costs 0.076 per trial, 0.24 on conflict trials.
- **The value is learned.** The never-damaged net's counterpart earns
  nothing (0.002, 23/28 against it). It is not for lack of room: an oracle
  would earn 0.092 for that net.
- **Exposure, not the body.** The yoked arm earns the same (0.042; no
  difference, 10/28).
- **The size depends on the setting.**
  - At training exposure (conflicts 7% of trials) the value is small but
    consistent: about 0.01 per trial, roughly 1% of payoff (25/28).
  - Under a stricter payoff, where errors cost more, it is three times larger
    (0.126).
- **It costs on unfamiliar damage.** Under scramble, noise and zero the agent
  stays accurate, so there is nothing to earn (room 0). As used, the variable
  loses 0.006–0.008 per trial; noise and zero are significant. This is P1k's
  over-caution, priced: generality without calibration has a real cost. A
  re-tuned threshold removes it, so the variable is not harmful once caution
  is re-tuned (dV\* about 0).

## 4. Against the discovery set and the expectations

| | Discovery | Confirmation |
| --- | --- | --- |
| dV\* / dV / room, PFATE | 0.048 / 0.094 / 0.077 | 0.042 / 0.076 / 0.076 |
| Recovery | 0.60 | 0.49 |
| Tests P1M_1–3 | 27, 28, 20 of 28 | 26, 28, 23 of 28 |

| Outcome (protocol §6) | Expected | Observed |
| --- | --- | --- |
| Valid, room present | 0.95 | Yes |
| VALUE_CREDITED | 0.60 | Yes |
| VALUE_NOT_LEARNED | 0.25 | No |
| Natural-mix dV\* > 0, PFATE | 0.85 | Yes (0.0095, 25/28) |
| Novel damage: dV as used < 0, all three operators | 0.80 | Yes |

## 5. Reading and credit

- **Q-NECESSITY passed, within its scope.** Under the constitution's
  separation of claims:

  | Claim type | Status | Evidence |
  | --- | --- | --- |
  | Causal role | Established | P1j, P1k |
  | Property-relative necessity/value against the strongest available matched reduction | Established in this task | P1m |
  | Engineering advantage | Small at natural exposure; larger when errors are costly; a cost on unfamiliar damage | P1m |

- **Synthesis status for the Layer 4 building block** (a learned integrity
  monitor of the agent's own memory), in this system: **SUPPORTED_BOUNDED.**

  | Constitution question | Answer |
  | --- | --- |
  | Q-EXIST | Yes |
  | Q-LEARN | Yes, from exposure to damage |
  | Q-CAUSE | Yes (P1j, P1k) |
  | Q-NECESSITY/VALUE | Yes, against the matched lesion rival (P1m) |

  - Also general across damage (P1k) and accessible to a second consumer
    (P1l).
- **The claim ceiling (what is NOT established):**
  - **No separately trained rivals.** The rival is a reduction of the same
    trained network. A network trained with a supplied damage flag, a
    larger plain network, or a different organization could do as well
    without a content-free variable. The oracle bound only says that a
    supplied flag would earn about twice as much.
  - **One task, one payoff, one 70-unit GRU, one trained damage type.**
  - **Layer 0 → Layer 4 not supported.** The precarious body is not the
    source; exposure is. The thesis that motivated the line is not
    supported by it.
  - **Calibration does not transfer.** On unfamiliar damage the variable
    costs, as used.
  - **Not awareness.** No phenomenal claim (Layer 6 remains a philosophical
    boundary).

## 6. Files

- `trackc_swap/necessity.py`, `run_p1m_necessity.py`, `test_p1m_necessity.py`
  (6 tests: reproduction without a lesion, the lesion clamps the state, the
  clamp leaves other directions alone, cross-fitted threshold values with a
  synthetic flag, labels, streams and seed sets).
- `p1m_necessity/discovery/` (P1g's seeds) and `p1m_necessity/confirm/`.

## 7. Next steps (for the PI; not authorized by this card)

- **Separately trained rivals: the remaining reduction, and the step from
  "bounded to this system" to a building-block principle.** Train:
  - a plain network of equal and of larger size, with a supplied damage
    flag as input (the supplied-substrate rival);
  - the same network with the flag, at matched exposure.

  If the endogenous agent matches the flag-trained agent's reward under
  damage, and beats it on unfamiliar damage or with less supplied
  information, the organization is credited beyond reductions of itself.
- **Replication in a second architecture or task** (LSTM or a larger GRU; a
  task where memory corruption has a different structure). This is needed
  before calling it a general building block.
- **Metacognitive learning (Layer 4):** a brief exposure to a new damage type
  should recalibrate the use of the variable (remove the over-caution)
  without retraining the variable itself.

## 8. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
