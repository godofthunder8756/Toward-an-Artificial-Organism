# W-REL close-out E27 v1

Documentation and stored-artifact inspection for PR #11. No planner, solver, replay, or other computation over the model was run. Frozen files and earlier results are unchanged. This file is additive.

The two-setting check at `(c_R, c_S) = (1/100, 3/50)` was not run. It needs the PI's separate approval.

## Policy-coverage check

**(a) holds.** The independently rebuilt reference policy was the policy object used in the required reference intervention and rescue replay at `T_SEP = 3` and both `K_SEP` cost pairs.

**(b) is not established.** No stored action table covers the states that replay consults, so actions were not compared with the primary policy under the frozen tie rule.

Formal A-SEP does not stay UNRESOLVED-COMPUTE on the policy-coverage ground. The ledger wording below is included because (a) holds. Matching initial value, runtime, process isolation, and the count 624 are not the evidence for (a) and are not recorded as intervention-policy agreement.

### Extracted: the rebuilt policy is the object the replay consults

Locked source `c4_reliability_exact_check_v1/wrel/verification_a1.py`, SHA256 `f8deb34b82d7695a2a3bbf283135839c5e595d0855f1465e29eec175c95169dc`. That hash is the one locked in `VERIFICATION_A1_MANIFEST.md` before the run. Git history shows the file last changed in `db69242b03d2c305d53b58e3e945f1070b8046f0`. The result commit `0e17a05c782b294805eab317b3bafd81cff8bb7c` does not change it.

In `run`, `solve_reference` returns a new action map and that same object is passed into `reference_case`. The module does not load a stored policy. `reference_case` then uses that object at every policy lookup of the reference replay:

- forward mass, every positive-mass belief, every observation, remaining horizons 3, 2, and 1;
- split-read counts, which read the full action (P, R, or M);
- intact readout and SUSPEND readout at the perturbation horizon `k = 2`, split reads, recheck bit;
- SWAP and CORRUPT readout at the donor index, same horizon, split reads, recheck bit;
- the advance that builds the post-intervention masses, controller index (the donor, or each recipient under SUSPEND), every observation, recheck bit;
- the repair readout on both successor masses at `k = 1`, split reads, recheck bit.

`run` compares the resulting `flags`, `pattern`, donors, contrast bit, T2 note, `interventions` (including rescue components), `cref_counts`, and per-action squared errors with `outputs/deviation_1/ITEM-8.json`. It also compares the empty-belief value with ITEM-2 `V_star`.

`outputs/verification_A1/RESULT.json`, SHA256 `e9d76f3d780af4064bdb84e0ca4e9c883dd7c075a46e1ec17041bcdfe96a000e`, records that comparison. `mismatches` is empty. Each reference row has `n_mismatches` 0. Status is COMPLETE and integrity is AGREE. That mismatch count is the count of disagreements among those derived records. It is not a count of action disagreements.

### Extracted: states required, states stored

States required by the replay are the lookup sites listed above, for both stored `K_SEP` rows at `T_SEP = 3`: `(c_R, c_S) = (1/50, 3/50)` and `(1/100, 1/10)`. The visited belief indices are not written down. The primary procedure in `wrel/sep.py` consults its in-memory policy at the same sites (`_snapshots`, `_cref`, `_stats`, `_advance`). Those primary actions are not in the JSON either.

Stored coverage of those states by an action table: none. The read-only inspection below searched the original outputs, the deviation-1 outputs, and `RESULT.json`. Intervention objects store aggregate fields (`D_e`, `D_q`, `e_now`, `q_now`, `eA`, `eB`, `qA`, `qB`, `LA`, `LB`, `repair_equals_shadow`), not actions. The longest integer list in those files has length 12 and is a donor count vector. `per_action_agent` and `per_action_baseline` are squared-error totals for actions R and M. `P_action_change_split` is one rational per regime. `n_policy_entries` is an integer. `policy_source` is a sentence.

### Extracted: what 624 and the value match are

Both reference rows in `RESULT.json` store `n_policy_entries` 624 and a value equal to the ITEM-2 `V_star` already quoted in `RESULTS_v3.md` (`13268495163/5000000000` and `173582937170561189335173/65536000000000000000000`).

624 is the number of entries `solve_reference` inserts for `T = 3`: every count vector whose sum is at most `T - k`, for remaining horizons `k = 1, 2, 3`, and all 8 observations. That is `8 + 88 + 528`. It is the size of the map that was built. It is not a count of states the replay visited, and it is not a comparison with the primary policy.

`RESULT.json` field `invariant_decisions` is the world flag `Index.invariant`: `d_recheck(0, y, y')` equals `d_recheck(1, y, y')` for every observation pair. The sentence "Decision invariance held" in `RESULTS_v3.md` records that flag. It does not record an action comparison.

The frozen tie rule, in `wrel/mb.py`, keeps P unless R is strictly greater, then replaces the incumbent only when M is strictly greater. `verification_a1.py` uses that same strict update when it builds the map. Because the action tables were not stored, that rule was not applied to a stored comparison. (b) remains unestablished.

### Process wording

The committed verification record uses "in this process", "in-process", "One process", and "one CPU process". It does not contain the phrases "separate process" and "same process".

Resolved from that record:

- The verification is its own process. The locked command is `taskset -c 0 python3 -u -m wrel.verification_a1`, from `c4_reliability_exact_check_v1`. It is not `python3 -m wrel.run_all` and it is not the D1 process.
- Inside that verification process, `solve_reference` and `reference_case` run together. "In this process" and "in-process" mean the action map was built there and was not loaded from the primary run.

The resolved description is one verification process, distinct from the freeze run and from D1, with the rebuilt policy and the intervention replay inside it.

### Inspection script

`policy_coverage_inspect_v1.py`, SHA256 `09a90e4cbb0f01b7cd968a8714ebdaa7f83e8f86a847207ebe68c83b0d0ae3df`. It reads stored JSON and prints file hashes. It does not import `wrel` and does not solve or replay.

Command, from `c4_reliability_exact_check_v1`:

```text
python3 policy_coverage_inspect_v1.py
```

Wall time, including process startup, measured outside the script: 0.050447935 seconds. The script's stdout is `policy_coverage_inspect_v1_output.txt`, SHA256 `bb713b51329d617b75592fc9955fff9a462dfe17948ba5c249994dbd8c2b5863`. The clock is not inside that file. The output's last line is `stored_action_table_covering_intervention_or_repair_states: no`.

## Named edits

E27-1: "The verification addendum reports agreement for all required R-CG replay rows and reference C-FO checks. Policy verification additionally records whether the independently reconstructed policy was used in the required reference intervention replay, or whether its actions were compared with the primary policy at every state used by that replay. Matching initial value alone is not recorded as intervention-policy agreement."

E27-2: "The advisory script and output have modification timestamps of 11:00:20 and 11:00:27 AM ET. Their ordering relative to delivery of the scope-tightening instruction is unresolved from the available record. The previous assertion that the calculation preceded that instruction is withdrawn. The artifacts remain ADVISORY and provide no mandatory verification or confirmatory support."

E27-3: "Existing outputs and the stated analytic arguments exclude full reference-conjunction attainment in ten of the twelve H0 settings. They do not supply complete A-SEP classifications for previously unevaluated settings. The two remaining settings are OPEN, not predicted passes."

E27-4: "The proposed two-setting check is exploratory and informed by PR #11. It retains the frozen criteria and makes no claim of independent confirmatory selection. If neither setting attains the full reference conjunction, the frozen reference/core-criterion combination is retired as a successful A-SEP design over the declared six-cost, two-horizon grid. No additional settings are added under this approval."

E27-5: "The b=1/2 recipient subset has no upward RECHECK headroom at the identified decision point. This does not establish zero aggregate intervention effect across the full recipient population. Episode-level C-REF differences likewise do not establish C-SEL."

E27-6: "The attainability note's UNRESOLVED-COMPUTE status records the state before verification close-out. Its current status is supplied by the dated verification addendum and the documented policy-coverage check; the original note is preserved unchanged."

## Standalone errata

The attainability-from-existing-outputs note is not in this repository. These corrections are therefore standalone. No earlier file was edited. `RESULTS_v1.md`, `RESULTS_v2.md`, `RESULTS_v3.md`, `results_v1_errata/ERRATA_v1.md`, the frozen spec, and the output JSON stay as they are. That is how E27-6's preservation sentence is met: there is no note here to rewrite. Current status is `RESULTS_v3.md` together with the policy-coverage check in this file.

### Wording corrections

- Where that note said "confirmatory run", the wording is "prospectively specified exploratory attainability check, selected using PR #11 results".
- Where that note's F4 said "Both c_S=1/10 cost pairs", the wording is "All three c_S=1/10 cost pairs" (three costs times two horizons = six exclusions).

### Extracted

The frozen cost grid, spec FINAL and `wrel/run_all.py`, is `c_r ∈ {1/100, 1/50, 1/25} × c_s ∈ {3/50, 1/10}`. Three of the six pairs have `c_S = 1/10`: `(1/100, 1/10)`, `(1/50, 1/10)`, and `(1/25, 1/10)`. The A-SEP horizons in the frozen decision order are `T_SEP ∈ {3, 4}`. This inspection does not recompute attainment on that grid.

`ERRATA_v1.md` already records the advisory timestamps 11:00:20 and 11:00:27 AM ET and that "preceded" is unverified. E27-2 withdraws the earlier assertion that the calculation preceded the scope-tightening instruction. The advisory artifacts remain outside mandatory verification.

### Reasoned inferences

Donor identity and transferred C-SEL assessment effects are reasoned inferences. They are not extracted outputs and they are not results of a computation performed for this close-out. They stay in this subsection and are not used as mandatory verification or as confirmatory support.

### Newly computed

Nothing in this close-out is a new computation over the model. The inspection script only reads files that were already stored and prints their structure and hashes.

## Ledger wording

Included because the policy-coverage check establishes (a).

"W-REL PR #11: bounded exact check completed, including the approved verification addendum. Mandatory replay coverage agrees on the specified quantities; deliberately unreplayed quantities retain their coverage tags. Formal A-SEP labels are UNRESOLVED-DESIGN at (c_R,c_S)=(1/50,3/50), T_SEP=3 and 4, and REFERENCE CRITERIA NOT MET at (1/100,1/10), T_SEP=3 and 4. No tested setting demonstrates the full reference core conjunction. Reported component intervention and rescue results concern supplied analytic mechanisms. Q-LEARN and Q-NECESSITY remain untested. Reproduction is recorded separately from role identification. The theory-stage C4 candidate card status remains; there is no change to the C4 evidence or status row and no consciousness conclusion."

## Claim ceiling

This file does not change a C4 evidence row or status row. It does not state a consciousness or sentience conclusion. Q-LEARN and Q-NECESSITY remain untested. ORIGIN, ROLE, and REDUCTION stay separate. The theory-stage C4 candidate card status remains.
