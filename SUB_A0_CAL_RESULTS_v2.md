# SUB-A0 calibration results v2 (probe v2: engineering depth sweep)

2026-10-05. **STOP: `NO_ADMISSIBLE_DEPTH_STOP_AND_REPORT`.** Stage 2 (v2) and
stage 3 (holdout) were **not run**, as the registered rule in
[probe v2 §2 and §4](SUB_A0_CAL_PROBE_v2.md) requires. The holdout seeds remain
untouched. No regime freeze and no candidate.

## Provenance

- [Probe v2 protocol](SUB_A0_CAL_PROBE_v2.md) and the
  [sub_a0_cal_v2/](sub_a0_cal_v2/) harness (8 tests) were frozen in
  [SUB_A0_CAL_PROBE_FREEZE_v2.json](SUB_A0_CAL_PROBE_FREEZE_v2.json) before any v2
  run. Approval basis: the user replied "A".
- The v1 freeze verified unchanged. The stage-1 selection (`s2_d1_e1`, H = 2048)
  was read with provenance checks.
- Raw outputs: [sub_a0_cal_results_v1/probe2_engineering/](sub_a0_cal_results_v1/probe2_engineering/),
  32 jobs. Wall time about 27 s per job, about 2 minutes in total.

## Result: engineering seeds 3000–3007, all 8 eligible at every (k, W)

Each cell is the median closure, EXT_BISTABLE / NO_MAINT. Admissible requires
EXT ≥ 0.75 **and** NO_MAINT ≤ 0.10.

| k \ W | 16 | 64 | 256 | 1024 |
| --- | --- | --- | --- | --- |
| −3 | 0.00 / 0.00 | 0.37 / 0.03 | 1.00 / 0.30 | 1.00 / 0.60 |
| −4 | 0.00 / 0.00 | 0.02 / 0.00 | 1.00 / 0.21 | 1.00 / 0.53 |
| −5 | 0.00 / 0.00 | 0.00 / 0.00 | 1.00 / 0.16 | 1.00 / 0.48 |
| −6 | 0.00 / 0.00 | 0.00 / 0.00 | 0.83 / **0.104** | 1.00 / 0.45 |

No cell is admissible. The nearest miss is k = −6 at W = 256, where NO_MAINT is
0.104 against the 0.10 bound. Per-seed NO_MAINT values there range from 0.055 to
0.156. That is a 0.004 miss on an 8-seed median, which I do not treat as "nearly
passing." The pattern is structural. There is a window between 64 and 256 ticks:
- by W = 64, bounded repair has not yet reversed the lesion;
- by W = 256, drift has spontaneously reversed 10–30% of the lesions in the arm
  with no repair.

Deeper lesions shrink spontaneous reversal only slowly (0.30 → 0.10 as |k| doubles)
and push repair time toward the window edge.

### Predictions, scored

| Registered prediction | Outcome |
| --- | --- |
| k = −3 fails at W = 256 (NO_MAINT ≈ 0.2) | Confirmed (0.30) |
| k = −4 most likely admissible at W = 256, marginal | **Wrong:** NO_MAINT 0.21 |
| k = −5 and −6 fail at W = 1024 by convergence | Confirmed at 1024 (0.48, 0.45). But EXT restored faster than predicted: 1.00 at W = 256 for k = −5, against a predicted ~267-tick restore |
| A STOP is a real possibility | Occurred |

My restore-time model was conservative. A likely reason, not verified: at trigger
time the bistable parent's replicas sit below m, because shrinkage acts between
writes. That shortens the restore distance. The null model under-predicted
spontaneous reversal.

## What is established

- **Engineering, bounded:**
  - In the stage-1 regime, at A0 write physics (|Δ| ≤ 0.05, B = 256), injected
    single-replica lesions show **large separation** between invulnerable bistable
    repair and no repair (≥ 0.70 closure difference at W = 256 for every depth
    tested).
  - They **do not satisfy** the registered absolute null bound (≤ 0.10) at any
    tested depth and window.
  - Under the frozen rule, the capacity probe is **UNIDENTIFIABLE**.
- **Not established:**
  - that no probe could work. The grid was {16, 64, 256, 1024} and k ∈ [−3, −6];
  - any statement about the regime's maintenance pressure. That stands on stage 1
    alone, and stage 1 has **no holdout replication**.
- **Analytic, separately** ([R-repairability check](SUB_A0_R_REPAIRABILITY_CHECK_v1.md)):
  the magnitude of real-valued performing weights cannot be recovered from live
  state under common-mode shrinkage. The A0 candidate's repair circuit can persist
  only through a sign-coded or scale-tolerant code.

## Status of the line (bluntly)

The A0 calibration was asked to supply three things:
1. pressure: **met** on calibration seeds, not replicated on the holdout;
2. external repairability: **met**;
3. an identifiable repair-capacity probe: **not met**.

The R-repairability check adds a fourth fact. In this regime, the candidate's own
machinery decays in a way that live redundancy cannot undo. A re-test of the
present candidate on this substrate is therefore predicted to end in a
competence or maintenance-use NEGATIVE, for reasons fixed by the substrate.

Per the [probe v2 consequence table](SUB_A0_CAL_PROBE_v2.md), there is **no
automatic probe v3.**

## Decision needed (human)

| Option | What it is | What it can license | What would end the line |
| --- | --- | --- | --- |
| **1. Weakened §8.5** | Drop the capacity probe. Judge the cascade only by R-interception last-quarter harm > 0.05 vs sham-interception (23/32). Run the stage-3 holdout for the **regime only**, then propose the regime freeze and the re-test. Pre-state the R-repairability prediction (row 1 or 2 NEGATIVE likely) | A Phase A license still needs all other §8 conditions plus the dependence excess X | Valid row 1–5 outcomes, as in the [re-test table](SUB_A0_RETEST_PROPOSAL_v1.md) |
| **2. Substrate revision (recommended if the question is priority, not this circuit)** | New substrate proposal: sign-coded or bistable performing weights with a physics-set magnitude, declared before results. This makes R maintainable in principle, as T is, and removes the predicted substrate-driven NEGATIVE. Recalibration is needed (control arms only, using the v1/v2 harness) | Same re-test table, with the R-unrepairability confound removed | A valid allocation or dependence-excess failure under the revised substrate ends the dependence-priority question for this lineage |
| 3. Park | Record A0-cal as: regime pressure plus repairability demonstrated; probe unidentifiable; R unrepairable in principle | Nothing | Ends here |

My recommendation is **2**, with option 1's probe-free §8.5 adopted in the revised
substrate. The probe failed through an interaction between window and drift that
is not about allocation. R-unrepairability would make option 1's re-test mostly a
test of the substrate. Option 2 is a substantive change and needs your explicit
approval. I have not started it.
