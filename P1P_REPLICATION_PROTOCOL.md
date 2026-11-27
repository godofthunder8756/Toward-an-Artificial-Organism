# P1p protocol: replication of the Layer 4 integrity monitor in a second architecture

- **Status:** DESIGN (code, tests and decision rules committed before any
  CIFG agent was trained on a study seed). To be frozen after discovery,
  before confirmation training.
- **Follows:** [P1O_COUPLING_RESULTS.md](P1O_COUPLING_RESULTS.md) §8 and
  [P1N_SUPPLIED_RESULTS.md](P1N_SUPPLIED_RESULTS.md) §7. Chosen by the PI
  ("Proceed with the recommended steps", 2026-11-27).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

The Layer 4 building block is SUPPORTED_BOUNDED in one system: a 70-unit GRU
on one memory task. The block is a learned, content-free monitor of the
agent's own memory that is:

- causal (P1j);
- general across damage (P1k);
- readable by a second consumer (P1l);
- valuable against the strongest reduction of itself (P1m) and against a
  separately trained supplied-analyzer rival (P1n).

Does it appear in a different recurrent architecture trained the same way?
If it does, it is a property of the training regime and task (a learned
response to self-damage), not of the GRU's gating.

## 2. Design

- **Architecture:** a coupled-input-forget-gate LSTM (CIFG; Greff et al.
  2017) with 35 cells (`trackc_swap/archswap.py`).
  - The carried state is packed as [h, c], 70 numbers, the GRU's width. So
    every damage operator, probe, direction, push and lesion of P1g–P1m acts
    on it unchanged: a damage event overwrites K of the 70 numbers, hidden
    or cell.
  - The policy and value heads read h only.
  - c is a convex combination of c and g, so the state stays within
    [−1, 1], and the clamps of P1j–P1m stay harmless (tested).
  - The forget-gate bias starts at 1. The encoder is unchanged.
  - 15,444 parameters against the GRU's 34,449. The replication is in a
    smaller network with a different gating structure and a separate cell
    memory.
- **Training:** P1g's, unchanged (`run_seed_g`). Phase 1, then three arms
  for 3,600 updates: PFATE (damage through its own body), PYOKED (PFATE's
  gains replayed) and PNOFATE (never damaged). Same world, pay, base rate,
  graded damage and streams. P1g's in-training evaluation at 1,800 and
  3,600.
  - **One disclosed change (§5):** the phase-1 warm-up is 3,600 updates
    instead of 1,200, because the CIFG learns the memory about half as fast.
    The rest of phase 1 (ramp, regulation) and the arms' training are
    unchanged.
  - The swap is installed in each worker before any runner is built. The
    runners' code, the training loop and the evaluations are the original
    ones.
- **Analyses:** P1j's, P1k's, P1l's and P1m's own `analyse_seed` and
  `score`, each with its own decision rules, on the CIFG weights at 3,600.
- **Seeds:**
  - Discovery: 8 of P1g's seeds (3200–3207), trained here.
  - Confirmation: P1i's seeds (3400–3427), trained here after the freeze,
    in batches of four, each committed.

## 3. Decision rules (exactly as in `run_p1p_replication.py`)

Each study's label on the CIFG is computed by its own frozen rules and
compared with the GRU's confirmed label:

| Study | GRU label (confirmed) | What it shows |
| --- | --- | --- |
| P1g | P1G_1 DERIVED_AHEAD | A learned monitor: abstention after a conflicting overwrite − after a same-value overwrite, PFATE vs PNOFATE |
| P1j | LEARNED_SIGNED_INTEGRITY_VARIABLE | A content-free direction d causally lowers and restores confidence, learned |
| P1k | GENERAL_INTEGRITY_VARIABLE | d activates and rescues under three damage types never trained |
| P1l | SHARED_GENERAL_ACCESS | A linear read-out of damage generalizes and shares d |
| P1m | VALUE_CREDITED | Clamping d online costs payoff against the re-tuned lesioned agent |

**Overall:**

| Label | Rule |
| --- | --- |
| INVALID | P1g's validity fails on the CIFG (phase-1 memory ≥ 0.80 clear correct; the never-damaged net loses the value under conflict; exposure ≥ 0.02) |
| UNDETERMINED | Fewer than 10 seeds, or P1G_1 UNDETERMINED |
| MONITOR_NOT_REPLICATED | P1G_1 not DERIVED_AHEAD |
| BLOCK_REPLICATED | All five labels equal the GRU's |
| PARTIAL_REPLICATION | Otherwise. The report lists which match. |

No new multiplicity correction is added: each study's own Holm family is
kept, and the overall label needs all five.

## 4. Readings

- **BLOCK_REPLICATED.** The building block is a property of the training
  regime and task, not of the GRU. This is the step from "SUPPORTED_BOUNDED
  in this system" toward a building-block principle: still one task.
- **PARTIAL_REPLICATION.** The parts that replicate are the robust core. The
  parts that do not may be GRU-specific, or may need more capacity (the
  CIFG has under half the parameters).
- **MONITOR_NOT_REPLICATED.** The monitor itself is architecture-dependent.
  The Layer 4 credit would be restricted to the GRU.
- **Layer 0 (reported, not a primary):** P1g's arrow (PFATE vs PYOKED) on
  the CIFG. In the GRU, exposure sufficed.

## 5. Discovery set

### Discovery v1 (P1g's training exactly): INVALID

- Outputs: `p1p_replication/{train_discovery_v1, discovery_v1}`.
- P1g's validity failed on memory: phase-1 clear correct 0.0006.
- **Why:** during the warm-up (wrong cost 0) the CIFG reported on almost
  every probe, but stayed at chance (correct ≈ 0.49) through all 1,200
  updates. The GRU passes 0.85 at about 900 updates on the same seed. When
  the wrong cost ramped up, the CIFG collapsed to abstaining on every probe
  (abstain 0.999). All four batteries were therefore INVALID.

### Diagnostic (non-study seeds 3900 and 3901, warm-up only)

- `p1p_replication/diagnostics/`: 3,600 warm-up updates, forget-gate bias 1
  (as designed) and 0.
- The CIFG learns the memory in every run. Correct first passes 0.8 at about
  1,800–2,120 updates and plateaus at about 0.87, the GRU's level.
- The forget-gate bias makes no difference. It is kept at 1, as designed.

### Adjustment (made before any further study-seed training)

- The CIFG's warm-up is 3,600 updates (`WARM_ITERS_P`, 3 × P1g's).
  - That is about 1.7 × the slowest learning time seen.
  - The GRU's 1,200 is about 1.3 × its own.
- **Rationale:** match the competence at the end of the warm-up, not the
  number of updates.
- Nothing else changes:
  - phase 1's wrong-cost ramp and regulation updates;
  - the arms' 3,600 updates;
  - world, pay, damage, evaluation, analyses and rules.
- Discovery is re-run on the same 8 seeds (v2), below.

### Discovery v2

(To be written after the v2 run, before the freeze.)

## 6. Expectations

(To be written after discovery, before confirmation training.)

## 7. Outputs and verification

- `p1p_replication/train_{discovery,confirm}/` (weights, per-seed P1g
  records, logs), then `p1p_replication/{discovery,confirm}/` (raw.json,
  scores.json, REPORT.md).
- **Verification:**
  - source hashes match the freeze;
  - `--score` reproduces REPORT.md;
  - no errors in the logs.

## 8. Limits

- **One second architecture:** a gated recurrent cell. An ungated network,
  a much larger network, or a transformer-style memory are not tested.
- The same task and training. Replication in a second task is a separate
  step.
- The architecture is smaller in parameters than the GRU. A failure could
  be one of capacity, not of architecture.

## 9. Safety

- Simulated variables only (X1–X5). No real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned. The
  swap patches class names in memory, inside the P1p run only, and modifies
  no file.
