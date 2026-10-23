# Addendum A2 specification: exploratory reference-attainability check

Frozen before execution. This file adds no criterion, threshold, donor rule, world parameter, or decision-order function. It does not contain a result. The binding approval is `c4_reliability_APPROVAL_ADDENDUM_A2.md` (sha256 `09c336d4569ec6771c88d97bee424510fab0cd6b5403b24accee1f813fb8b835`), recorded 2026-10-21, 12:19 PM ET. Where this file and that approval differ, the approval governs.

## Scope

One process evaluates only R-HAC-MB, non-myopic, under H0, at `(c_R, c_S) = (1/100, 3/50)`, for `T_SEP = 3` and then `T_SEP = 4`. Each setting gets one primary evaluation and one independent replay. Intervention time remains `τ = T_SEP − 2`.

The process also makes at most one smoke-test invocation: the existing T = 1 case at the same cost pair, limited to 60 seconds. The smoke test is not a `T_SEP` setting.

Excluded, and not invoked: additional attempts, other costs or horizons, other controllers, PM minimization, criterion changes, neural training, architecture work, and any C4 or consciousness claim.

## Frozen procedures

The primary policy is one call to `H0Solver.solve_cost` (`wrel/mb.py`) at horizon `T_SEP`, `myopic` false. The world is `study_world` (`wrel/run_all.py`). Criteria, donors, SWAP, CORRUPT, SUSPEND, and rescue come from one call to `evaluate_mb_family` (`wrel/sep.py`) with the name `R-HAC-MB`. Thresholds and flag rules are the constants and flag functions already in that module. No quantity is retuned.

The replay does not call `H0Solver` and does not load the primary policy. For that setting it makes one `Index`, one `solve_reference`, and one `reference_case` (`wrel/verification_a1.py`). A further `forward_mb` on each regime, and `_mb_advance` for SWAP, CORRUPT, and SUSPEND in both directions, only names the states whose actions are stored. Those calls do not recompute a criterion.

## Action tables

For each of the primary policy and the replay policy, store one row `(k, count vector, y, action)` for every observation `y` in `0..7` at:

- remaining horizon `k = 2`: every positive-mass belief in either regime at trial index `T_SEP − 2`, and the S-donor and E-donor when they exist;
- remaining horizon `k = 1`: every positive-mass belief in the A mass or the B mass of SWAP, CORRUPT, and SUSPEND, both directions.

Agreement is exact equality of the two stored tables, including their key sets. A missing key is not imputed.

## Smoke test

One `H0Solver` at horizon 1, one `solve_cost` at this cost pair, and `H0Solver.forward` under both regimes. The stage limit is 60 seconds. Integrity holds only when the mixture of the two forward values equals the backward value, and the forward record equals the already stored ITEM-2 row for law H0, T = 1, and this cost pair (`V_star`, `n_R`, `n_R_unanimous`, `n_M`, `exploration_cost`, `first_R`, `never_R`). Otherwise the process stops before either `T_SEP` setting.

## Integrity and the formal label

A setting is complete only when the primary and the replay agree exactly on the flags, the pattern, the T2 note and improvement, the per-action errors, the split-read counts, the donors, the contrast bit, and every stored intervention field; the empty-belief values agree; the policy-entry counts and belief-index sizes agree; the decision-invariance flags agree; the action tables agree; each donor that exists appears in both `k = 2` tables; and every replay `repair_equals_shadow` that was computed is true.

The formal label is the return value of frozen `assemble_setting` (`wrel/sep.py`), which calls frozen `decide_setting`. The control list is empty. `pm_undefined` is false, because this approval does not evaluate PM-ACT and does not assert that its quotient is ill-defined. `incomplete` is false only for a complete setting as defined above. This addendum does not add a label and does not treat the empty control list as DISTINGUISHES NAMED CONTROLS. The reference conjunction reported beside the label is frozen `conjunction_of` on the reference flags.

On an integrity failure or a cap, the process stops, writes the partial result it has, and does not start a remaining setting. A setting whose primary evaluation did not finish has no criterion flags and no formal label.

## Limits and command

Working directory `c4_reliability_exact_check_v1`. One CPU process. No GPU. No arguments. Cumulative wall-clock limit 30 minutes from process start, including manifest verification, the smoke test, and both replays. Resident memory 8 GB. No retry.

```text
taskset -c 0 python3 -u -m wrel.attainability_a2
```

The runner refuses to start unless `Cpus_allowed_list` is `0`, and unless every file listed in `ADDENDUM_A2_MANIFEST.md` still has the recorded sha256. It writes only `RESULTS_A2.md` and `outputs/attainability_A2/`. It does not modify an earlier file. A second invocation is refused when an output from this addendum already exists.

## Claim ceiling

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. Eligible named controls were not evaluated.
