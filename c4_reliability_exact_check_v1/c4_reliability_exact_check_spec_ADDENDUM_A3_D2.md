# Addendum A3 Deviation D2: replay-agreement key set

Frozen before execution. This file adds no criterion, threshold, donor rule, intervention, rescue procedure, or decision-order function. It does not contain a result. The binding approval is `c4_reliability_APPROVAL_ADDENDUM_A3_D2.md` (sha256 `1f7158133243a2a506076bedba3a1ee5147f0004a6b772e6c92f077e6f8b82df`), recorded 2026-10-21, 3:29 PM ET. Where this file and that approval differ, the approval governs.

D1 stopped because the runner compared every `A2_KEYS` field. `cfo_detail` is in `A2_KEYS` and is null in the stored primary, because `evaluate_mb_family` does not emit it. `reference_case` emits the object returned by `cfo_reference`. That field is not a deciding statistic.

## Gating key set

Agreement gates only on the frozen replay-comparison keys, restricted to fields the stored `7e153d1` primary emits, as the D1 agreement list requires.

The frozen case keys are the tuple in `wrel/attainability_a3.py` `_compare_cases` (lines 505–521): `flags`, `pattern`, `t2_note`, `t2_improvement`, `per_action_agent`, `per_action_baseline`, `cref_counts`, `donor_S`, `donor_E`, `donor_contrast`, `interventions`.

`_mb_replay_failures` (lines 1022–1042) adds, for the reference and for the myopic replay, `V`, `n_policy_entries`, `n_beliefs`, `invariant_decisions`, the intervention/repair action table, `repair_equals_shadow`, and donor coverage of that table.

The per-control tuples in `_verify_horizon`, and `_pm_public` (lines 1365–1382), name the same deciding statistics. PM donors are the belief-count signatures from `donor_beliefs`, not block labels. The conf replay also gates `extra["V"]` where the stored primary has it, because the frozen verifier compared that value. PM gates `action_mismatches`, `ill_defined_extractor`, and `decoder_entries` from `_pm_public` when the stored primary has them.

Addendum A3, section “Independent replay,” defines the same statistics: flags, pattern, T2 note and improvement, per-action errors where both sides emit them, donors (PM: belief-count signatures), contrast, and interventions, plus the reference and myopic value, entry count, belief-index size, invariance, and action tables.

The D1 agreement list says a field the stored primary does not emit is not an agreement key. A stored string T2 note is the frozen encoding of `t2_improvement = None`, and the replay must have that `None`. Numeric T2 improvement and per-action errors absent from the stored roster columns are recorded and do not gate. The primary evaluators are not called again.

`cfo_detail` is not in `_compare_cases` or `_mb_replay_failures`. It is reported as a non-gating difference. The same treatment applies to diagnostic extras the frozen deciding comparison does not name, including `reachable`, `cfo_note`, and `zero_support_rule`.

## What this run does

One process. It runs only the independent-verification block, for the reference and every roster control at `T_SEP = 3` and `T_SEP = 4`, including PM-ACT and the `T_SEP = 4` machine rebuild. It does not call `evaluate_mb_family`, `blind_result`, `evaluate_conf`, `evaluate_cg`, `evaluate_mf`, or `evaluate_pm`. It does not rewrite a primary file.

The blind joint walks each regime and stores content `None`. That is the D1 plumbing correction. It does not change a deciding statistic.

The PM machine is reconstructed with frozen `build_pm_horizon` and is accepted only when the closure record matches stored `PM.json` and the study-cost action-table sha256 matches the stored reference table. The five non-study costs are the input alphabet. No A-SEP criterion is evaluated at them. The myopic action table is reconstructed with `solve_cost(..., myopic=True)` and is accepted only when the empty-belief value and invariance match the stored primary. That is not a call to `evaluate_mb_family`.

Per-state tables for the reference, the myopic control, and every roster control are written from the occupancy objects the frozen verifier used.

Formal labels are the return of frozen `assemble_setting` on the stored reference and stored roster columns. They are issued only after every configuration at both horizons agrees on the gating keys and that return reproduces the stored `label_before_replay`. The clause is `clause_of` of that note. On a gating disagreement the disagreement is stored, no formal label is issued, and the process stops. Partial tables are kept. There is no second attempt, except the one plumbing refreeze this deviation authorizes if a later error provably cannot change a deciding statistic.

## Limits

Priors are the cumulative clocks in the D1 summary at `0c5b308`. This process adds to both the 60-minute A3 total and the 20-minute verification block. One CPU (`Cpus_allowed_list` `0`), 8 GB resident memory, no GPU.

```text
taskset -c 0 python3 -u -m wrel.attainability_a3_d2
```

Working directory `c4_reliability_exact_check_v1`. No arguments. The runner checks the A3, D1, and D2 manifests, then checks that the primary files still match `7e153d1` and that the D1 summary still matches `0c5b308`. It writes only `RESULTS_A3_D2.md` and `outputs/attainability_A3_D2/`. A second invocation is refused when a D2 output already exists.

## Claim ceiling

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This comparison is not an all-controller certificate. A `T_SEP = 4` result cannot claim to distinguish R-HAC-MF.
