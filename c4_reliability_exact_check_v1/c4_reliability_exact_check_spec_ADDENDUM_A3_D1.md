# Addendum A3 Deviation D1: verification-block plumbing fix and replay

Frozen before execution. This file adds no criterion, threshold, donor rule, intervention, rescue procedure, or decision-order function. It does not contain a result. The binding approval is `c4_reliability_APPROVAL_ADDENDUM_A3_D1.md` (sha256 `47fd381e1fdf98b40914b117e5bf24412316a7aba56240fcce273b78e872bd62`), recorded 2026-10-21, 3:16 PM ET. Where this file and that approval differ, the approval governs. Addendum A3 remains binding for everything this deviation does not change.

The frozen A3 runner is `wrel/attainability_a3.py`, sha256 `12c719bebafcda83ffcaaf67cfc3ae33ea997603424fa547d255c3c6ef78ba8a`, commit `cc68e467f9cf6c9f3c4673e3609b0c4f19f910c3`. This deviation does not edit that file, `KSEP`, or any other frozen file. Primary outputs at `7e153d1648dfa5babe080b028a0c1609682c5a69` are read and are not rewritten.

## The fault

`_verify_horizon` builds blind snapshots as `bsnaps = [_snapshots(...) for z in (0, 1)]`, a length-2 list of regime horizons. It then calls `_mb_snaps_as_joint(bsnaps)`. That helper is written for one regime: `[[(None, i, p) for i, p in layer] for layer in snaps]`, and `state_table` requires `snaps[z][t] = (content, i, p)`. Passing both horizons makes `layer` a whole horizon. The first trial layer contains one belief, so the unpack of that one-element list raises `ValueError: not enough values to unpack (expected 2, got 1)` at `attainability_a3.py:2310`. The reference and myopic joints in the same function already walk each regime separately. The blind call does not.

## Plumbing fix

`wrel/attainability_a3_d1.py` is a new module. It does not call `_mb_snaps_as_joint` on the two-regime list. For the blind table it walks each regime, then each trial layer, and stores `(None, i, p)`, which is the content the frozen helper stores for one regime. No other joint changes.

This cannot change a deciding statistic. `replay_blind` returns flags, pattern, the T2 note, per-action errors, contrast, and interventions before the joint is built. The blind action distribution ignores content. `state_table` only writes the per-state comparison rows. `decide_setting` reads reference flags and each control's flags, reproduction, and conjunction. None of those are computed from the blind joint. The corrected nesting supplies the trial layers the table writer already required. It does not alter an occupancy, an action map, a threshold, a donor, an intervention, or the decision order.

## What this run does

One process. It runs only the independent-verification block. It does not call `evaluate_mb_family`, `blind_result`, `evaluate_conf`, `evaluate_cg`, `evaluate_mf`, or `evaluate_pm`. It does not rerun the smoke test and does not replace a primary file.

The replay paths are the ones Addendum A3 names: `solve_reference` and `reference_case`; the myopic Index DP then `reference_case`; `replay_blind`; `cg_case`; `replay_conf` then `_finish_f0`; `replay_mf_occupancy` then `mf_finish_on_snaps`; `pm_statistics_on_block` on the queue-refined block. PM donor comparison uses belief-count signatures from `donor_beliefs`, not block labels. The PM machine is reconstructed with the frozen `build_pm_horizon` because the primary did not serialize it. That reconstruction is accepted only when its closure record matches stored `PM.json` and the study-cost intervention/repair table matches the stored reference action-table sha256. The five non-study costs remain the input alphabet. No A-SEP criterion is evaluated at them. The myopic action table was not stored. The same `solve_cost(..., myopic=True)` policy is reconstructed and is accepted only when its empty-belief value and invariance match the stored primary fields. That reconstruction is the primary side of the action-table comparison. It is not a call to `evaluate_mb_family`.

A configuration agrees when the deciding fields present in the stored `7e153d1` primary agree with the replay. Those fields are flags, pattern, T2 note, donors (PM: belief-count signatures), contrast, and interventions, plus, for the reference, the stored value, entry count, belief-index size, invariance, split-read counts, per-action errors, T2 improvement, and action table. Where the stored T2 note is a string, the frozen pack rule makes the T2 improvement `None`, and the replay must have that `None`. Numeric T2 improvement and per-action errors for roster controls were not in the stored columns. They are recorded from the replay and are not an agreement key, because the primary side was not stored and the primary evaluators are not called again. Controller `extra["V"]` is compared where the stored primary has it and the frozen verifier compared it.

Per-state tables for the reference, the myopic control, and every roster control are written from the same occupancy objects the frozen verifier used, with the blind nesting corrected. Each positive-mass joint row stores the regime, trial, belief counts, controller content, observation, control action or action probabilities, reference action, and whether the belief transition agrees.

The formal label is the return of frozen `assemble_setting` on the stored reference and stored roster columns, with `incomplete` false and the stored `pm_undefined`. It is issued only after that return reproduces the stored `label_before_replay` and every configuration at that horizon agrees. The clause is `clause_of` of that note. On a disagreement the disagreement is stored, no formal label is issued for that horizon, and the process stops. Partial tables are kept. There is no second attempt and no replacement setting.

## Limits

The A3 cumulative wall already recorded at finalize is the SUMMARY clock, and the verification block's already-used time is that total minus the stored `T_SEP = 4` evaluation cumulative. This process adds to both. The verification block stays within 20 minutes including the time already used. The A3 total stays within 60 minutes including the time already used. One CPU (`Cpus_allowed_list` `0`), 8 GB resident memory, no GPU. An integrity failure or a cap stops the process.

```text
taskset -c 0 python3 -u -m wrel.attainability_a3_d1
```

Working directory `c4_reliability_exact_check_v1`. No arguments. The runner checks `ADDENDUM_A3_MANIFEST.md` and `ADDENDUM_A3_D1_MANIFEST.md`, then checks that the working-tree primary files still match commit `7e153d1`. It writes only `RESULTS_A3_D1.md` and `outputs/attainability_A3_D1/`. A second invocation is refused when a D1 output already exists.

## Claim ceiling

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This comparison is not an all-controller certificate. A `T_SEP = 4` result cannot claim to distinguish R-HAC-MF.
