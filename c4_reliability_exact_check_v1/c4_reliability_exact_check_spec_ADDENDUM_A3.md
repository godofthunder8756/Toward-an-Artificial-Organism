# Addendum A3 specification: named-control comparison

Frozen before execution. This file adds no criterion, threshold, donor rule, intervention, rescue procedure, or decision-order function. It does not contain a result. The binding approval is `c4_reliability_APPROVAL_ADDENDUM_A3.md` (sha256 `6efeef0d2ae0123e95939f63d06a803d9cde642997ce735a6b0eb28aa2ea9a2c`), recorded 2026-10-21, 2:45 PM ET. Where this file and that approval differ, the approval governs.

## Implementation note: roster supply

`(c_R, c_S) = (1/100, 3/50)` is cost index 0 of the descriptive `COSTS` grid. It is not an element of frozen `KSEP`. Frozen `item8` builds the eligible-control list only inside `KSEP`, so the existing runner's list at this cost is empty. Addendum A2 stored that empty list. This addendum does not edit `KSEP`, `item8`, or any other frozen file.

The eligible roster evaluated here is the roster spec FINAL §4.1 and `item8` define, supplied explicitly at this cost pair, in `item8` append order:

- `R-HAC-MB-myopic`
- `R-BLIND / R-CONF-S` (one control)
- nine `R-CONF-A`, η ∈ {1/20, 1/10, 1/5} × α ∈ {1/20, 1/10, 1/5}, names `R-CONF-A eta=<η> alpha=<α>`
- six `R-CG`, α ∈ {(1,1), (2,1)} × β ∈ {0, 1/20, 1/10}, names `R-CG alpha=(<α_s>,<α_f>) beta=<β>`
- `PM-ACT`
- and, only at `T_SEP = 3`, `R-HAC-MF eps=0` and `R-HAC-MF eps=1/10`, inserted immediately before `PM-ACT`

That is 20 controls at `T_SEP = 3` and 18 at `T_SEP = 4`. Supplying this list is not a criterion change. R-CONF-ENUM and descriptive `PM_k` are not on it and are not evaluated.

## Scope

One process, under H0, at `(c_R, c_S) = (1/100, 3/50)`, for `T_SEP = 3` and `T_SEP = 4`. The reference is non-myopic R-HAC-MB. Every roster control is evaluated once at each horizon where it is eligible. Intervention time remains `τ = T_SEP − 2`.

The process also makes at most one smoke-test invocation: the existing T = 1 reference case at the same cost pair, limited to 60 seconds. The smoke test is not a named block and is not a `T_SEP` setting.

Named blocks, in order, each limited to 20 minutes of wall time inside that block: PM construction, `T_SEP = 3` evaluation, `T_SEP = 4` evaluation, independent verification. The whole process, including the manifest check, the smoke test, and verification, is limited to 60 cumulative minutes and 8 GB resident memory.

Excluded, and not invoked: any other cost as an A-SEP setting, any other horizon, any controller variant outside the roster, any criterion change, an all-controller certificate, neural training, Track A or Track B implementation, and any C4 or consciousness claim.

## PM-ACT input-domain closure

PM-ACT is built by the frozen procedure: donors from `_donors_for` on this cost's optimal policy, then `build_machine(..., n_costs=6)`, `refine`, `well_defined`, and the independent `refine_by_queue`. The six policies are optimal `H0Solver.solve_cost` policies, one per descriptive `COSTS` pair, solved on an `H0Solver` of horizon `T_SEP` (one solver at 3 and one at 4; no T = 10 solver). Belief indices match that solver.

Those five other costs are the frozen input alphabet of the transducer. They are not A-SEP settings. No criterion is evaluated at them. `n_costs=1` descriptive `PM_k` is not built.

A disagreement between `partition_sets(refine(...))` and `partition_sets(refine_by_queue(...))` is an integrity stop. `well_defined.ok` false, or `evaluate_pm`'s `ill_defined_extractor`, is the frozen `pm_undefined` input to `assemble_setting`. It is a specified label outcome, not by itself an integrity stop.

## Frozen criteria

Thresholds, donor rules, SWAP, CORRUPT, SUSPEND, rescue, and the decision order are the frozen functions. Each primary call is one of: `evaluate_mb_family` (reference and `R-HAC-MB-myopic`), `blind_result`, `evaluate_conf` (with `conf_theta0`), `evaluate_cg`, `evaluate_mf` (T_SEP = 3 only), `evaluate_pm`. The reference policy is the study-cost policy already solved for the machine. The myopic policy is one `solve_cost(..., myopic=True)` at the study cost only.

The formal label of a completed setting is the return of `assemble_setting` on that reference, the roster results in the order above, `incomplete` false, and `pm_undefined` as defined above. The clause is identified by which frozen note that return carries, in the order written in `decide_setting`. This addendum does not add a label. "A T = 4 result cannot claim to distinguish MF."

Reference integrity, before any control criterion is trusted: the new reference primary must match the stored Addendum A2 primary on flags, pattern, T2 note and improvement, per-action errors, split-read counts, donors, contrast, interventions, empty-belief value, policy-entry count, belief-index size, decision invariance, and the intervention/repair action-table sha256.

## Independent replay

Verification does not call `evaluate_mb_family`, `blind_result`, `evaluate_conf`, `evaluate_cg`, `evaluate_mf`, or `evaluate_pm` again.

- Reference: `Index`, `solve_reference`, `reference_case`.
- Myopic: the same Index DP with continuation omitted from the argmax only, then `reference_case`.
- Blind: an Index occupancy under a read-class table from the same strict tie, then C-REF and C-T2 recomputed with the frozen split-read helpers. C-SEL and rescue remain the frozen NOT APPLICABLE values.
- R-CG: `cg_case`.
- R-CONF-A: a second occupancy written in this addendum's module, then frozen `_finish_f0`.
- R-HAC-MF: a second occupancy written in this module. Deciding-pattern arithmetic is applied to that occupancy by a transcription of the frozen MF finish, not by a call to `evaluate_mf`.
- PM-ACT: the deciding-pattern arithmetic is run on `index_pm` of the queue-refined partition. Donor comparison uses the set of belief count vectors in the donor cell, because block labels are not required to coincide.

A configuration agrees only when those deciding statistics agree: flags, pattern, T2 note and improvement, per-action errors where both sides emit them, donors (PM: donor belief-count signatures), contrast, and interventions. Reference and myopic replays also agree on the empty-belief value, entry counts, belief-index size, invariance, and the intervention/repair action tables. An action or transition that differs from the reference is a stored comparison, not an integrity failure.

The formal label is issued only for a setting whose reference and every roster replay agree. On a disagreement the primary columns are kept, `assemble_setting` is called with `incomplete` true, that return is the recorded label, and the process stops.

## Per-state tables

Reference and myopic intervention/repair tables use the Addendum A2 key `(k, count vector, y)`. For every roster control, the positive-mass joint states of the verified occupancy are stored as `(regime, trial, belief counts, controller content, y)`, with the control action or action probabilities, the reference action at that belief, and whether the belief transition under that action equals the reference transition. A missing comparison is not imputed.

## Smoke test and integrity stops

The smoke test is one `H0Solver` at horizon 1 and `forward` under both regimes. It agrees only when the forward mixture equals the backward value and the forward record equals the stored ITEM-2 row for law H0, T = 1, and this cost (`V_star`, `n_R`, `n_R_unanimous`, `n_M`, `exploration_cost`, `first_R`, `never_R`).

The process also stops, without a replacement setting or a second attempt, if `Cpus_allowed_list` is not `0`, a manifest hash disagrees, the world identity check fails (`eps` both `23/100` and `emissions_match`), a named block or the cumulative clock or the 8 GB resident limit is hit, or a replay disagrees. Partial files already written are kept.

## Limits and command

Working directory `c4_reliability_exact_check_v1`. One CPU process. No GPU. No arguments.

```text
taskset -c 0 python3 -u -m wrel.attainability_a3
```

The runner refuses to start unless `Cpus_allowed_list` is `0` and every file listed in `ADDENDUM_A3_MANIFEST.md` still has the recorded sha256. It writes only `RESULTS_A3.md` and `outputs/attainability_A3/`. It does not modify an earlier file. A second invocation is refused when an output from this addendum already exists. Wall time and sampled peak RSS are recorded per invocation and per block.

## Claim ceiling

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This comparison is not an all-controller certificate. A `T_SEP = 4` result cannot claim to distinguish R-HAC-MF.
