# P1l results: SHARED_GENERAL_ACCESS on fresh seeds (Layer 4 → Layer 3)

- **Protocol:** [P1L_ACCESS_PROTOCOL.md](P1L_ACCESS_PROTOCOL.md), frozen at
  39b3361 before any P1l measure was computed on P1i's seeds.
- **Follows:** [P1K_TRANSFER_RESULTS.md](P1K_TRANSFER_RESULTS.md).
- **Run:** evaluation only, on saved weights (3600).
  - Discovery set: P1g's seeds, 3200–3227. The primaries were committed
    before the run, and nothing was changed after it.
  - Confirmation: P1i's seeds, 3400–3427.
  - Report: [p1l_access/confirm/REPORT.md](p1l_access/confirm/REPORT.md).
- **Verification:**
  - All 26 source files are byte-identical to the freeze, and so are the
    hashes recorded in raw.json.
  - `--score` reproduces REPORT.md byte for byte.
  - `score()` equals `scores.json`.
  - No error in the log.
- Astra review waived by the PI. **No consciousness claim.**

## 1. Declared result

**Overall: SHARED_GENERAL_ACCESS.** Valid: 28 seeds fitted per arm, and PFATE's
held-out AUC on the trained damage is 0.92 (needed ≥ 0.70).

| Test | Result | Holm p | Label |
| --- | --- | --- | --- |
| P1L_1 general: a read-out trained on one damage type flags three it never saw | 27/28 above chance, mean AUC 0.81 | < 0.0001 | PRESENT |
| P1L_2 learned access: PFATE vs PNOFATE, mean novel AUC | 24/28 (0.81 vs 0.67) | 0.0004 | DERIVED_AHEAD |
| P1L_3 same variable: moving d at step 5 moves the read-out at step 9 (signed) | 22/28 > 0, median 2.98 | 0.004 | PRESENT |

Medians:

| | PFATE | PYOKED | PNOFATE |
| --- | --- | --- | --- |
| AUC trained damage: vs none / vs same overwrite | 0.92 / 0.92 | 0.94 / 0.93 | 0.76 / 0.74 |
| AUC same-value overwrite vs none | 0.54 | 0.55 | 0.52 |
| AUC scramble / noise / zero (never trained, never seen by the read-out) | 0.78 / 0.82 / 0.84 | 0.80 / 0.83 / 0.84 | 0.64 / 0.67 / 0.70 |
| Read-out: induce / rescue (natural conflict–same difference) | 1.75 / 0.93 (8.68) | 1.79 / 1.80 (9.10) | 0.12 / 0.11 (1.09) |
| Confidence in the same pass: induce / rescue (P1j replication) | 0.41 / 0.38 | 0.45 / 0.44 | 0.01 / 0.07 |
| Read-out score: correlation with d9 / with content | 0.94 / 0.01 | 0.95 / 0.00 | 0.57 / −0.02 |

- Secondaries:
  - signed_rep, PFATE vs PNOFATE: 22/28 (DERIVED_AHEAD);
  - novel AUC, PFATE vs PYOKED: 10/28 (no difference);
  - scramble AUC above same-overwrite AUC: 27/28.
- The same-value overwrite registers very slightly (0.54, 27/28 above 0.5)
  but far below any corrupting damage.

## 2. What was found

- **The variable is accessible to a consumer other than the one that uses
  it.**
  - The read-out is a linear consumer that never sees the policy, trained
    only on the trained damage.
  - It reads "my memory is corrupted" from the damage-trained agent's state
    at 0.92 AUC, and at 0.78–0.84 under three damage types that neither the
    agent nor the read-out had met.
  - It does not flag a harmless same-value overwrite (0.54).
- **It is the same variable that sets the confidence.**
  - Pushing P1j's d at delay step 5 moves the read-out's verdict at step 9 in
    the direction the variable implies (22/28). The same pushes move the
    agent's confidence (P1j's effects replicate in the same pass).
  - The read-out's score tracks the integrity direction (0.94) and not the
    content (0.01).
  - One upstream variable, two downstream consumers.
- **Access is learned.** The never-damaged net offers a weaker and less
  general signal (0.67 on novel damage; 0.76 even on the trained damage).
  Moving its own d barely moves the read-out (0.23 against 2.98).
- **Exposure, not the body.** The yoked arm matches the damage-trained agent
  throughout.
- **Size:** each push moves about 10–20% of the read-out's natural
  conflict–same difference (induce 1.75, rescue 0.93, against 8.68). The
  rescue is smaller than in discovery (2.07).

## 3. Against the discovery set and the expectations

| | Discovery (3200–3227) | Confirmation (3400–3427) |
| --- | --- | --- |
| AUC novel, PFATE / PNOFATE | 0.83 / 0.69 | 0.81 / 0.67 |
| signed_rep, PFATE | 4.60 | 2.98 |
| Tests P1L_1–3 | 28, 26, 25 of 28 | 27, 24, 22 of 28 |

| Outcome (protocol §6) | Expected | Observed |
| --- | --- | --- |
| Valid | 0.97 | Yes |
| SHARED_GENERAL_ACCESS | 0.85 | Yes |
| Same-overwrite AUC below 0.60, PFATE | 0.90 | Yes (0.54) |

## 4. Reading

- **Layer 4 → Layer 3, the first step.** The integrity variable is explicit
  enough for any linear consumer to read.
  - It is general: what a consumer learns from one kind of damage transfers
    to others.
  - It is shared: the same upstream direction drives both the agent's own
    confidence and the new consumer.
  - These are the properties a variable needs before it can be broadcast. A
    private, entangled or damage-specific signal would fail one of them, and
    the never-damaged net's signal is weaker on all three.
- **What it is not.**
  - The second consumer is external and trained with labels on a frozen
    agent. P1l shows availability, not that the agent's own processes
    broadcast the variable or that the agent can report it.
  - Nothing here is a workspace, an ignition or awareness.
- **Where the P1 line stands (P1h–P1l).** The damage-trained agent has a
  variable about its own memory with these properties:
  - content-free (P1j);
  - produced by its dynamics and causal on its confidence in both directions
    (P1j);
  - general across kinds of damage, reading anomaly rather than perturbation
    (P1k);
  - over-cautious on unfamiliar damage (P1k);
  - readable by a second consumer, and the same variable that controls
    confidence (P1l);
  - learned from exposure to damage, not from a precarious body.

## 5. Limits

- An external linear read-out with supervision. Access is shown for a
  consumer of this class only.
- The correlation with d9 is largely by construction (protocol §2).
- d comes from average differences, and the push is linear and clipped (as in
  P1j).
- One task, one architecture (a 70-unit GRU).

## 6. Files

- `trackc_swap/access.py`, `run_p1l_access.py`, `test_p1l_access.py`
  (4 tests: content-free recovery, a linear read-out cannot use signed
  weakening, labels, streams and seed sets).
- `p1l_access/discovery/` (P1g's seeds) and `p1l_access/confirm/`.

## 7. Next steps (for the PI; not authorized by this card)

- **Q-NECESSITY (the constitution's crediting test; recommended first).**
  Does the monitor do work for the agent that the strongest simpler rival,
  with matched information, cannot?
  - Rival: the same network given an explicit, supplied damage flag (the
    analyzer as supplied substrate). The agent's own variable must match or
    beat it on reward under damage, including novel damage.
  - Ablation: project d out of the state online during the task and measure
    the loss in reward and in error avoidance.
  - Without this, the building block is described but not credited.
- **Agent-level report.** Fine-tune the agent with a second report action
  ("my memory was disturbed"), trained on donor damage only. Test whether it
  recruits d (steering moves the report), generalizes to novel damage, and
  leaves the confidence coupling intact. That is self-report by the agent,
  not by an external read-out.

## 8. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
