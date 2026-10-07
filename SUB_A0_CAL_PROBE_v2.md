# SUB-A0 calibration: probe v2 successor

2026-10-05. Additive successor to the frozen
[A0-cal protocol v1](SUB_A0_CAL_PROTOCOL_v1.md). It is triggered by the stage-2
STOP in [results v1](SUB_A0_CAL_RESULTS_v1.md). The human selected **option A**:
a deeper lesion, the same criteria and the same window grid, a rerun of stage 2
on the calibration seeds, then stage 3 on the holdout.

v1 files, hashes, results and the v1 freeze are unchanged.
This document is hashed by `SUB_A0_CAL_PROBE_FREEZE_v2.json` before any v2 run.
Control arms only; no candidate.

## 1. What changes and what does not

**Changed:**
- The lesion depth k. The chosen replica is set to k × the mean of the other two.
  v1 used k = −2.5.
- How k is chosen: on disjoint engineering seeds (§2), before any calibration or
  holdout probe is rerun.

**Unchanged from v1 code and protocol:**
- Regime: stage-1 selection `s2_d1_e1`, H = 2048, read from the v1 stage-1
  summary with provenance checks.
- Probed arms: NO_MAINT, EXT_BISTABLE, EXT_MEDIAN.
- Triggers: K = 4 active-damage events after H/8.
- 64 lesions per trigger, each on an eligible coefficient.
- Fork rows sharing the fault stream.
- The closure formula.
- Seed eligibility: ≥ 3 identifiable triggers and not SEED_NO_PRESSURE, with
  ≥ 12/16 seeds eligible.
- Criteria: EXT_BISTABLE median closure ≥ 0.75 and NO_MAINT median ≤ 0.10.
- Window grid W ∈ {16, 64, 256, 1024}; the smallest admissible W is selected.
- Holdout seeds 2100–2115 and all regime criteria at stage 3.

**Mechanism:** `arms.PROBE_REVERSAL` is set inside each worker before
`simulate`. `arms.perturb` reads it at call time. A test confirms the override,
the guaranteed readout flip, recoverability, and that the v1 default is restored.

## 2. Depth selection on engineering seeds (registered rule)

- Engineering seeds 3000–3007. These are disjoint from the A0 engineering and
  confirmatory sets and from the calibration and holdout sets.
- Depths k ∈ {−3, −4, −5, −6}.
- For each k, apply the v1 probe criteria with the count scaled to 8 seeds
  (≥ 6/8 eligible). That gives the smallest admissible window W\*(k), if one exists.
- margin(k) = min(EXT median − 0.75, 0.10 − NO_MAINT median), taken at W\*(k).
- **Choose** the k with the largest margin. Ties go to the k closest to the
  human-approved −4, then to the lower value.
- If no k is admissible: **STOP and report.** Stage 2 does not rerun.

This refinement was added before any v2 data. Option A named k = −4. A sweep that
includes −4 and prefers it on ties removes the risk of a single guessed depth
failing by a hair. The cost is selecting on 8 engineering seeds; the holdout stays
untouched.

## 3. Analytic predictions (registered, rough)

For a lesion of depth |k| in a triplet with untouched replicas a and b:
- the readout mean is (a+b)(1 − |k|/2)/3;
- restoring the readout requires moving the lesioned replica a distance of
  (|k|/2 − 1)(a+b).

**EXT_BISTABLE.** Its parent sits near m, so a+b ≈ 8.9. Each of the 64 lesioned
destinations ranks first by |target − v| and is written every tick, at most 0.05
per write. Predicted restore times are about **89, 178, 267 and 356 ticks** for
k = −3, −4, −5 and −6. Therefore EXT closure ≥ 0.75 is predicted at W = 256 for
k ∈ {−3, −4}, and only at W = 1024 for k ∈ {−5, −6}.

**NO_MAINT.** Spontaneous reversal needs summed drift over the window to exceed
(|k|/2 − 1)(a+b)·s(W). Here a+b ≈ 1.2 at the trigger ticks, and s(W) is the
shrink factor over the window (≈ 0.49 at W = 256 for λ_s = 2). This window-level
model ignores the parent's own decay, which dominates at W = 1024. In v1
(|k| = 2.5), closure was 0.19 at W = 64 and 0.36 at W = 256.

**Predictions:**
1. k = −3 fails at W = 256 (NO_MAINT about 0.2).
2. k = −4 is the most likely admissible depth, at W = 256, with NO_MAINT close to
   the 0.10 bound. This is marginal.
3. k = −5 and −6 fail at W = 1024, where convergence under decay dominates the
   null arm.

A STOP with no admissible depth is a **real possibility.** It is stated here
before the data.

## 4. Consequences, fixed before data

| Outcome | Consequence |
| --- | --- |
| Engineering selects k; stage 2 (calibration) admissible; stage 3 holdout passes regime AND probe at (k, W\*) | `HOLDOUT_PASS_AWAIT_HUMAN_REGIME_FREEZE`. Propose the regime freeze `SUB_A0_CAL_REGIME_v1.json`. Before any re-test freeze, the R-repairability analytic check ([results v1](SUB_A0_CAL_RESULTS_v1.md)) must also be completed |
| No depth admissible on engineering seeds, or stage 2 fails | **Probe UNIDENTIFIABLE at A0 write physics in this regime.** Any lesion deep enough to resist drift in the unrepaired arm is too slow to repair within the window grid under a budget of 256 writes × 0.05 |
| Stage 3 fails on the holdout | STOP and report. No reselection |

**If the probe is UNIDENTIFIABLE:** design §8 condition 5 cannot be evaluated
through the probe. **There is no automatic probe v3.** The human then chooses:
- evaluate the cascade with the R-interception last-quarter criterion alone, a
  declared weakening of §8.5;
- change the write physics (a new substrate proposal); or
- park the line.

**§9 wording correction (v1).** v1 §9 treated a stage-2 failure as "the substrate
cannot host an identifiable maintenance contrast". That overreaches. A stage-2 or
probe failure establishes only that the **probe** cannot be identified. Whether
the regime has maintenance pressure is decided by stage 1 and stage 3's regime
criteria.

## 5. Compute

- Engineering: 32 jobs × 3,072 ticks.
- Stages 2 and 3: 16 jobs × 3,072 ticks each.
- CPU only, 12 workers, about 1–3 minutes per stage.
- Wall caps: 1,800 s per stage.
