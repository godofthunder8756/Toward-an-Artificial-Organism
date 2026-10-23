# W-REL close-out E30 v1

Documentary close-out of Addendum A3 on PR #11. This file is additive. It edits no frozen file, no earlier result, and no criterion or label. It adds no setting. The formal label remains the stored D2 return.

One provenance recomputation used the frozen `build_pm_horizon` and `evaluate_pm` arithmetic already in the repository. Command, from `c4_reliability_exact_check_v1`, one CPU:

```text
taskset -c 0 python3 /tmp/pm_rescue_diag.py
```

Wall time for both horizons together was 3.5 seconds on the second run. The script wrote `/tmp/pm_rescue_diag.json` only. It wrote no file under `outputs/`. The recomputed PM-ACT pattern strings at both horizons equal the stored column strings, including the nulls. Recomputed state counts equal stored `PM.json`: 21622 states at `T_SEP = 3` and 114693 at `T_SEP = 4`. Donor cells equal the stored columns: S `33` and E `35` at `T_SEP = 3`; S `321` and E `300` at `T_SEP = 4`.

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested.

## 1. PM-ACT rescue support

Classification: **(ii) a repaired PM state with zero occupancy under the intact distribution that defines its decoder.**

The credited rescue statistic is undefined at both A3 settings for the same reason. The stored flag is `NOT EVALUABLE [zero-probability event]`. The stored nulls are `eB`, `qB`, and `LB` on I-SWAP-S and on descriptive I-CORRUPT-S. I-SWAP-E, I-CORRUPT-E, and every SUSPEND block are numerically defined. `repair_equals_shadow` is true on every block. The flag is the zero-probability string. It is not `NOT EVALUABLE [PM quotient successor not a function]`.

### Conditioning event

Rescue is scored at trial index `t = T_SEP − 1`, which is trial `τ+2` with `τ = T_SEP − 2`. The credited direction that fails is I-SWAP-S: the S-donor cell is installed into the Z = E recipient population (`z = 1`), the closed loop runs one perturbed trial, and branch B then carries the matched-history shadow cell. The decoder is applied to that shadow cell on split reads, action R.

| T_SEP | Rescue trial index | Shadow cell | Belief indices with positive perturbed weight | Split reads | Intact mass of the shadow cell |
| --- | --- | --- | --- | --- | --- |
| 3 | 2 | 844 | 18, 20 | y = 1, 2, 3, 4, 5, 6 | `0/1` |
| 4 | 3 | 1691 | 18, 20, 84, 93, 95 | y = 1, 2, 3, 4, 5, 6 | `0/1` |

Descriptive I-CORRUPT-S lands on the same shadow cell at each horizon. Credited rescue requires both I-SWAP directions. I-SWAP-E is defined, so the undefined I-SWAP-S readout is what makes the rescue flag not evaluable.

### Distribution and the zero denominator

The decoder is `E[m_F0 | trial, PM cell, read class, action]`, accumulated once from the intact forward occupancy. Its weight on a visit is `F(1, 2) * p * py[Z=S][y]`. The key that is missing is `(t = T_SEP − 1, cell as above, read class 1, action R)`. Every such key has decoder denominator `0`, because the intact occupancy of that cell at that trial is `0/1`.

The rescue average's own denominator is the shared perturbed-history weight on split reads. That denominator is `5313/10000` on branch A and on branch B, at both horizons. Total perturbed mass on each branch is `1/1`. Branch A has zero decoder misses, which is why `e_A_S` and `q_A_S` are stored numbers. Branch B's misses are the twelve `(belief, y)` pairs at `T_SEP = 3` and the thirty pairs at `T_SEP = 4` listed above. `stats_at` returns null when any of those readouts is missing, and `_flag_rescue` then returns the zero-probability string.

Every split observation has positive probability under both regimes (`py[z][y] > 0` for `y ∈ {1,2,3,4,5,6}`, `z ∈ {0,1}`). Emissions match. A positive intact visit to the shadow cell would have produced a positive decoder denominator.

### The other three classes

- (i) does not hold. The recipient-world split-read denominator is `5313/10000`.
- (iii) does not hold. The quotient successor of the perturbed trial is one cell. `repair_equals_shadow` is true. The stored flag is not the ill-defined-successor string.
- (iv) does not hold. The missing cell's intact mass is `0/1`. The implementation assigns that cell decoder weight zero because the intact distribution does not visit it. It does not assign zero weight to a cell the intact distribution does visit.

This classification is provenance for the stored label. It does not change the label, the criterion, or the decoder rule. The frozen spec already says that a perturbed controller state with zero support under the intact decoder distribution is NOT EVALUABLE, and that no extension rule was specified.

## 2. D2 verification coverage

No coverage failure. Every deciding quantity required by spec FINAL §4.4–§4.5, Addendum A3 "Independent replay", and the D1 agreement list was present in the stored primary and was compared by D2, or was explicitly recorded under the frozen rule that it is not an agreement key. D2 gating failures are empty for all 21 configurations at `T_SEP = 3` and all 19 at `T_SEP = 4`. `gating_agreed` is true at both horizons.

`cfo_detail` has no primary counterpart. That is not a scientific disagreement. The required C-FO comparison agreed.

D2 `_diff_keys` skips a named key that the stored object does not contain. For the mandatory keys below, the stored objects contain them. The skip did not remove a mandatory comparison.

| Required quantity | Frozen requirement | Primary location | Replay location | Compared / missing |
| --- | --- | --- | --- | --- |
| C-REF flag, `Δ_R`, `Δ_M` | FINAL §4.4 C-REF; A3 Independent replay (flags and pattern); D2 `REFERENCE_GATING_KEYS` and `COLUMN_KEYS` | `TSEP-*.json` `reference.flags["C-REF"]`, `reference.pattern.delta_R`, `delta_M`; the same two fields on every column | D2 `TSEP-*-replay.json` configuration `failures` (empty) after comparing those keys | Compared. Agreed at both horizons, reference and every roster row. |
| Reference split-read counts | A3 reference-integrity paragraph; D1 agreement list; D2 `REFERENCE_GATING_KEYS` includes `cref_counts` | `reference.cref_counts` | Same comparison as the reference row | Compared. Agreed. Roster columns are not required to carry raw counts; their C-REF decision is the flag and the two deltas. |
| Combined calibration error and baseline | FINAL §4.4 C-T2. The combined error decides. Pattern fields `E_err_agent`, `E_err_baseline` | `reference.pattern` and every column `pattern` | flags and pattern in the D2 comparison | Compared. Agreed. Reference `E_err_agent` is `0/1` and C-T2 is PASS. |
| Separate R and M calibration errors | FINAL §4.4 says separate R and M errors are reported and the combined error decides. A3: per-action errors where both sides emit them. D1 agreement list: roster numeric per-action errors are recorded and are not an agreement key | Reference: `per_action_agent`, `per_action_baseline`. Roster columns omit them. `controls_raw_flags` does not store them | Reference: inside `REFERENCE_GATING_KEYS`. Roster: `unstored_replay_fields.per_action_agent` and `per_action_baseline` on each D2 configuration | Reference compared and agreed. Roster values recorded, not gated, under the frozen D1 rule. Not a coverage failure: the required combined comparison was made, and the separate errors were written down rather than dropped. |
| T2 note and reference T2 improvement | A3 Independent replay; D1; D2 reference keys and `_string_note_improvement` | `reference.t2_note`, `reference.t2_improvement`; column `t2_note` | Reference keys; column `t2_note`; a stored string note forces replay improvement `None` | Compared. Agreed. |
| Directional intervention effects | FINAL §4.4 C-SEL: `D_e` and `D_q` in both SWAP directions. Pattern and intervention blocks also store the intact and perturbed levels | `pattern.D_e_S`, `D_e_E`, `D_q_S`, `D_q_E` and `interventions` SWAP/CORRUPT/SUSPEND | pattern and interventions, both gating | Compared. Agreed. PM-ACT C-SEL is PASS at both horizons, so those perturbation-trial effects are defined. |
| C-FO exact equality | FINAL §4.4 C-FO (a) and (b); §4.5 pattern equality flags `cfo_a`, `cfo_b`; flag `C-FO` | `reference.flags["C-FO"]` PASS, `pattern.cfo_a` true, `pattern.cfo_b` true; the same on every column that was compared | flags and pattern | Compared. Agreed at both horizons for the reference and every roster row, including PM-ACT (`C-FO` PASS). |
| `cfo_detail` | Not in `_compare_cases` or `_mb_replay_failures`. D2 spec: reported, not gating. `evaluate_mb_family` does not emit it | `reference.cfo_detail` is null at both horizons | D2 nongating difference. Replay object at T=3: `n_beliefs` 20, `a_equal` true, `b_equal` true. At T=4: `n_beliefs` 80, `a_equal` true, `b_equal` true | No primary counterpart. Not a scientific disagreement: the replay diagnostic's equality bits are true, and the required C-FO flags agreed. |
| Rescue, including absolute-error reduction | FINAL §4.4 rescue: `e_A`, `e_B`, `q_A`, `q_B`, and `L_A − L_B`, both SWAP directions. Flag `rescue` | pattern rescue components and `interventions.*.{eA,eB,qA,qB,LA,LB}` | pattern and interventions | Compared. Agreed, including the stored PM-ACT nulls `e_B_S`, `q_B_S`, and SWAP-S `LB`. Where `LB` is null the reduction is the undefined comparison already labeled NOT EVALUABLE. Reference SWAP-S has all six fields, and rescue is PASS. |
| Applicability statuses | FINAL §4.6. Statuses are the flag strings `NOT APPLICABLE` and `NOT EVALUABLE [reason]` | column and reference `flags` | flags | Compared. Agreed. Blind rescue remains `NOT APPLICABLE`. Contrast-absent rows remain `NOT EVALUABLE [NO INTERVENTION CONTRAST]`. PM-ACT rescue remains `NOT EVALUABLE [zero-probability event]`. |
| Reference and myopic action tables, shadow equality, donor coverage | A3 Independent replay; `_mb_replay_failures`; D2 reference and myopic blocks | `reference_action_table` and its sha256; myopic value tail and `myopic_invariant` | D2 `action_agreement` | Compared. Agreed. Reference: 432 rows at T=3 and 1552 at T=4, sha256 equal, 0 disagree, 0 missing. Myopic: 16 rows at each horizon, 0 disagree, 0 missing. `repair_equals_shadow` checked. |
| PM controller equivalence | A3 PM donor rule: belief-count signatures. D2 `PM_GATING_EXTRA`: `action_mismatches`, `ill_defined_extractor`, `decoder_entries` | `pm_extra` and column donor cells | D2 PM configuration: signatures equal, mismatches 0, `ill_defined_extractor` false | Compared. Agreed. Replay-versus-reference state tables, which the primary evaluation does not emit, are stored in D2 `state_summary`: PM-ACT 784/784 action and transition equal at T=3, and 3008/3008 at T=4. |
| Roster joint-state action and transition versus the reference | A3 per-state tables: stored by verification, as a comparison with the reference, and a difference from the reference is not an integrity failure | No primary `TSEP-*-states.json`. The primary verification stopped before writing one | D2 `TSEP-*-states.json` and `state_summary`, one block per roster name | Stored replay-versus-reference. No primary counterpart, because these tables are a verification product. Not a deciding primary-versus-replay key in the D1 agreement list. Not a coverage failure. |
| R-CONF-A value `extra.V` | Frozen `_verify_horizon` compares it; D1: compare `extra["V"]` where the stored primary has it | `controls_raw_flags` extra `V` on all nine R-CONF-A rows | D2 conf branch of `verify_horizon` | Compared. Those nine configurations have empty failure lists at both horizons. |
| CG and MF descriptive `extra.V` | Not in the frozen CG or MF deciding-diff tuples, and not in the D1 agreement list | present on those extras | not a D2 gate | Outside the frozen deciding comparison. The required CG and MF flags, pattern, donors, contrast, and interventions were compared and agreed. |

Non-PM core flags were read from the stored columns. All 19 non-PM rows at `T_SEP = 3` and all 17 at `T_SEP = 4` have C-REF FAIL and C-T2 FAIL. PM-ACT has C-REF PASS, C-T2 PASS, C-SEL PASS, C-FO PASS, and rescue NOT EVALUABLE. With the reference, the evaluated configurations are 21 and 19. R-HAC-MF is absent from the `T_SEP = 4` roster.

## 3. Hash check

`closeout_e30_hashcheck_v1.py` reads bytes and compares SHA256 digests. It does not import `wrel` and does not run a solver. Result, also stored in `closeout_e30_hashcheck_v1_output.txt`:

```text
HASH CHECK OK manifest_lines=129 ledger_lines=19 git_pins=12
```

The 129 manifest lines cover `IMPLEMENTATION_MANIFEST.md`, `ADDENDUM_A2_MANIFEST.md`, `ADDENDUM_A3_MANIFEST.md`, `ADDENDUM_A3_D1_MANIFEST.md`, `ADDENDUM_A3_D2_MANIFEST.md`, `RESULTS_A2_errata_E29_MANIFEST.md`, and the verification-module line in `VERIFICATION_A1_MANIFEST.md`. The 19 ledger lines are the `HASHES.txt` files under `outputs/attainability_A2`, `attainability_A3`, `attainability_A3_D1`, and `attainability_A3_D2`. The 12 git pins are the A3 primary files at `7e153d1`, the D1 summary and `RESULTS_A3_D1.md` at `0c5b308`, and the D2 summary and `RESULTS_A3_D2.md` at `1f2a6c9`. Each pin's committed bytes equal the worktree. Frozen files and earlier outputs are unchanged.

## 4. Reviewer text

Astra consult #30 was checked against the stored artifacts. It is review input. These claims match the artifacts:

- Formal outcome UNRESOLVED-DESIGN at both A3 settings, clause 7, note naming PM-ACT. Source: D2 `SUMMARY.json`.
- PM-ACT full-pattern reproduction is NO at `T_SEP = 3` and UNRESOLVED at `T_SEP = 4`. Source: column `reproduction`. At T=3, `reproduction_disagree` is `["e_A_S"]` and `reproduction_missing` is `["e_B_S", "q_B_S"]`. The NO label is the available `e_A_S` disagreement. At T=4, `reproduction_disagree` is empty and the same two components are missing, so the label is UNRESOLVED. The reviewer's table matches. The missing components are additional stored facts, not a contradiction of that table.
- Core conjunction UNRESOLVED at both settings. Source: column `conjunction`.
- Every eligible non-PM implementation fails C-REF and C-T2. Counted above.
- Roster 20 controls at T=3 and 18 at T=4, including PM-ACT, plus the reference, giving 21 and 19. R-HAC-MF is absent at T=4.
- Original labels in `RESULTS_v3.md`: UNRESOLVED-DESIGN at `(1/50, 3/50)`, T=3 and 4; REFERENCE CRITERIA NOT MET at `(1/100, 1/10)`, T=3 and 4.
- Addendum A2 reference conjunction attained at `(1/100, 3/50)`, T=3 and 4, as recorded in `RESULTS_A2_errata_E29.md` and the A2 outputs.
- Primary verification stopped on `ValueError: not enough values to unpack` (`RESULTS_A3.md`). D1 stopped on the `cfo_detail` comparison (`RESULTS_A3_D1.md`). D2 completed. No resource-cap stop is recorded for those processes.
- D1 and D2 approval files cite Aidan Ahern's 3:15 PM ET standing approval on 2026-10-21.

The reviewer said the supplied report did not identify which zero-probability case produced the rescue null. This close-out identifies case (ii). That was an open question in the review, and the artifacts plus the frozen arithmetic settle it. It is not a false statement in the review.

No discrepancy was found between the checked reviewer claims and the stored artifacts.
