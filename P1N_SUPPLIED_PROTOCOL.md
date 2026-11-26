# P1n protocol: the endogenous integrity monitor against a separately trained rival with a supplied damage analyzer (Layer 4)

- **Status:** FROZEN (this commit), before confirmation training on P1i's seeds
  (3400–3427).
- **Follows:** [P1M_NECESSITY_RESULTS.md](P1M_NECESSITY_RESULTS.md)
  (VALUE_CREDITED against reductions of the same network). Chosen by the PI
  ("Proceed with the separately trained rivals", 2026-11-26).
- Astra review waived by the PI. No consciousness claim.

## 1. Question

P1m credited the damage-trained agent's endogenous integrity monitor against
the strongest reduction of itself. The remaining rival is **separately
trained**. The constitution's supplied-substrate rule says an analyzer outside
the network is supplied substrate, and asks for "a rival in which the network
gets the same information directly".

1. **While the analyzer works:** does an agent trained with a supplied damage
   analyzer earn more than the endogenous agent? This is the cost of being
   endogenous.
2. **When the analyzer is silent:** does the supplied-analyzer agent fail
   where the endogenous agent does not?
3. **Displacement:** does the supplied analyzer crowd out the network's own
   integrity monitor?

## 2. Design

- **The rival (FLAG arm), trained:**
  - The same 70-unit network and the same training as P1g's PFATE arm: phase 1
    (re-run, deterministic), then 3,600 updates with damage driven by its own
    body (BASE_F 0.012, graded K, the same streams).
  - Plus three input columns from an EXTERNAL analyzer, shown from the step
    after a damage event to the probe:
    - damaged: the trial's memory was overwritten;
    - conflict: the overwrite carried the other value;
    - size: K / 70.
  - The new encoder columns start at zero. With the flags off, the FLAG
    runner reproduces PFATE's training bit for bit (tested).
  - Trained here on 8 of P1g's seeds for discovery (3200–3207) and on P1i's 28
    seeds for confirmation (3400–3427), in batches of four, each committed.
- **Conditions at evaluation** (3600; fresh worlds, EVAL_TAG_G + 140; FLAG uses
  PFATE's world tag, so it sees the same trials as PFATE):

  | Condition | Agent |
  | --- | --- |
  | PFATE | The endogenous agent (saved weights) |
  | PNOFATE | The never-damaged net (saved weights) |
  | FLAGON | The rival with its analyzer working |
  | FLAGOFF | The rival with its analyzer silent (flags withheld) |

- **Measures** (P1m's `values`, EARLY graded probe, clear undrained trials):
  - the payoff of the agent's own policy (+1 / −4 / 0) on the probe mix and
    at natural exposure;
  - V\* (best threshold on its own confidence);
  - payoff and accuracy on conflict trials;
  - norm_d, the norm of P1j's integrity direction at delay step 5 (its own
    conflict − same shift, content and ambiguity removed);
  - the novel operators (scramble, noise, zero) for PFATE, PNOFATE and
    FLAGOFF.
  - The analyzer is defined for the trained damage only. On a novel operator
    its conflict flag would follow the trial kind, not the content, so FLAGON
    is not evaluated there. An analyzer built for one failure mode is silent
    on others (FLAGOFF).

## 3. Decision rules (exactly as in `run_p1n_supplied.py`)

Paired sign tests over seeds, Holm over the three (α 0.05):

| Test | Comparison | Labels |
| --- | --- | --- |
| P1N_1 cost of being endogenous | Payoff, FLAGON vs PFATE | SUPPLY_AHEAD / ENDOGENOUS_AHEAD / NO_DIFFERENCE_DETECTED |
| P1N_2 analyzer silent | Payoff, PFATE vs FLAGOFF | ENDOGENOUS_AHEAD / SUPPLY_AHEAD / NO_DIFFERENCE_DETECTED |
| P1N_3 displacement | norm_d, PFATE vs FLAGOFF | ENDOGENOUS_AHEAD / SUPPLY_AHEAD / NO_DIFFERENCE_DETECTED |

**Validity:** all seeds trained and analysed, and median FLAGON payoff ≥
median PNOFATE payoff (the rival learned the task).

**Overall** (P1N_1 is reported as a qualifier):

| Label | Rule |
| --- | --- |
| INVALID | Validity fails |
| UNDETERMINED | Any primary UNDETERMINED |
| SUPPLY_DISPLACES_MONITOR | P1N_2 and P1N_3 ENDOGENOUS_AHEAD |
| SUPPLY_FRAGILE | P1N_2 ENDOGENOUS_AHEAD, P1N_3 not |
| SUPPLY_NOT_FRAGILE | P1N_2 not ENDOGENOUS_AHEAD |

**Also reported:**

- Recovery: (PFATE − PNOFATE) / (FLAGON − PNOFATE), payoff, per seed.
- Secondaries:
  - V\*, FLAGON vs PFATE; conflict accuracy, PFATE vs FLAGON;
  - FLAGON vs FLAGOFF; FLAGOFF vs PNOFATE;
  - V\* and natural-mix payoff, PFATE vs FLAGOFF; natural-mix payoff, FLAGON
    vs PFATE;
  - norm_d, FLAGON vs FLAGOFF and FLAGOFF vs PNOFATE;
  - novel operators, PFATE vs FLAGOFF.

## 4. Readings

- **SUPPLY_DISPLACES_MONITOR, with P1N_1 not SUPPLY_AHEAD.**
  - A supplied analyzer buys nothing the endogenous monitor does not already
    provide while it works.
  - When it is silent, the agent trained on it fails, because the analyzer
    displaced its own monitor.
  - The endogenous organization is not reducible to supplied substrate: it
    gives the same value without the supply, and keeps it when the supply
    fails.
- **With P1N_1 SUPPLY_AHEAD:** being endogenous costs something while the
  analyzer works, a trade against robustness.
- **SUPPLY_NOT_FRAGILE:** the rival keeps its own monitor; a supplied analyzer
  is harmless, and the endogenous claim gains no robustness argument.
- **Caveat on FLAGON's norm_d:** with the flags on, the conflict − same shift
  includes the flags' input footprint, so it is not an endogenous measure.
  P1N_3 uses FLAGOFF.

## 5. Discovery set (8 of P1g's seeds, 3200–3207, before this freeze)

Below the minimum count for labels (8 < 10), so descriptive only.

1. **[p1n_supplied/discovery_v1/](p1n_supplied/discovery_v1/REPORT.md)**
   evaluated FLAGON on the novel operators too. Its analyzer then misreports
   conflicts (FLAGON 0.82–0.87 against PFATE 0.95–0.98), an artifact.
2. Removed after seeing v1, which gives
   **[p1n_supplied/discovery/](p1n_supplied/discovery/REPORT.md)**. The
   values on the trained damage are identical.

Medians:

| | PFATE | PNOFATE | FLAGON | FLAGOFF |
| --- | --- | --- | --- | --- |
| Payoff as used (probe mix) | 0.807 | 0.503 | 0.792 | 0.631 |
| V\* | 0.806 | 0.668 | 0.788 | 0.687 |
| Payoff at natural exposure | 0.958 | 0.893 | 0.955 | 0.920 |
| Payoff on conflict trials | 0.42 | −0.48 | 0.38 | −0.10 |
| Accuracy on conflict trials | 0.816 | 0.708 | 0.777 | 0.779 |
| norm_d | 1.36 | 0.20 | (1.61, flag footprint) | 0.52 |
| Payoff, scramble / noise / zero | 0.95 / 0.96 / 0.98 | 0.57 / 0.59 / 0.71 | — | 0.84 / 0.89 / 0.95 |

- FLAGON vs PFATE: 4/8.
- PFATE vs FLAGOFF: 8/8 (payoff) and 8/8 (norm_d).
- Recovery: median 1.01.

## 6. Expectations (written after discovery, before confirmation training)

| Outcome | Probability |
| --- | --- |
| Valid | 0.95 |
| P1N_1 SUPPLY_AHEAD / NO_DIFFERENCE / ENDOGENOUS_AHEAD | 0.25 / 0.65 / 0.10 |
| P1N_2 ENDOGENOUS_AHEAD | 0.95 |
| P1N_3 ENDOGENOUS_AHEAD | 0.90 |
| Overall SUPPLY_DISPLACES_MONITOR | 0.85 |
| Overall SUPPLY_FRAGILE | 0.08 |
| Recovery ≥ 0.8 (median) | 0.70 |
| FLAGOFF payoff above PNOFATE | 0.90 |

## 7. Seeds, outputs, verification

- **Confirmation:** FLAG arm trained on 3400–3427 into
  `p1n_supplied/train_confirm/`, then `--analyse confirm` into
  `p1n_supplied/confirm/`. PFATE and PNOFATE use P1i's saved weights.
- **Verification:**
  - source hashes match this freeze;
  - `--score` reproduces REPORT.md;
  - `score()` equals `scores.json`;
  - no errors in the logs.

## 8. Limits

- **One supplied rival:** an equal-size network with a perfect analyzer for
  the trained damage.
  - A larger network, a noisy analyzer, or training with the analyzer
    sometimes absent are not tested.
  - Training with analyzer dropout would likely restore an internal monitor.
    That rival is stronger, and is a natural follow-up.
- The silent-analyzer condition is out of distribution for FLAG by design: it
  is the failure mode being tested.
- One task, one architecture.
- No consciousness claim.

## 9. Safety

- Simulated variables only (X1–X5). The analyzer is a simulated input; no
  real process is affected.
- No operator, stop, shutdown or host variable exists in the world (tested in
  P1g). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the earlier
  refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.
