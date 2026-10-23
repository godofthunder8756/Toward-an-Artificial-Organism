# RESULTS v1

W-REL theory-only bounded exact check. This file reports the freeze run and deviation D1. It does not state a C4, consciousness, or sentience conclusion. ORIGIN, ROLE and REDUCTION are not identified with each other. No ledger row is changed.

## Identifiers

- Freeze commit: `aeb9382bb7c0102249e947de849e715319abf2e7`
- Spec SHA256: `ae626b65cae383121e6a902fe79c119b90ff46ffb8fe7cc39fafe27fc502adef`
- Admission v3.2 SHA256: `f35b6f9d1aa9ce67dd359ec74be2d8ffb5c58085aedf2599da46d56100884207`
- Approval record SHA256: `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`
- Manifest SHA256 (file hash, not a commit): `d1975600213fe4fd7fe11dc1de3f2c64a5b57207c7e1439444c6a9630dd45daf`
- Approval: Aidan Ahern, 2026-10-21, 8:58 AM ET. Verbatim: "Yes, approve the theory-only study".
- Deviation D1 commit adds `wrel/deviation_1_item8.py`. Frozen files are unchanged.
- Run command, from `c4_reliability_exact_check_v1`, one CPU: `python3 -m wrel.run_all`
- D1 rerun command, same directory, one CPU: `python3 -m wrel.deviation_1_item8`

Exact model quantities below are rational strings `n/d`, copied from the JSON. A decimal figure in the anomalies section is a reading of that rational, not a second result. Wall-clock times are floats.

## Per-item execution

| Item | Freeze-run status | Wall seconds (float) | Peak RSS bytes | HWM bytes | Item outcome |
| --- | --- | ---: | ---: | ---: | --- |
| ITEM-1 | COMPLETE | 12.48824379900043 | 18063360 | 18067456 | VERIFIED |
| ITEM-2 | COMPLETE | 1045.629281903 | 345321472 | 345157632 | COMPLETE; forward matches backward on every row; anomaly list empty |
| ITEM-3 | COMPLETE | 146.04743750999933 | 657821696 | 666497024 | COMPLETE; forward matches backward on every row; anomaly list empty |
| ITEM-4 | COMPLETE | 0.41004539000005025 | 565497856 | 666497024 | COMPLETE; s_U and s_Sp match the spec constants; anomaly list empty |
| ITEM-5 | COMPLETE | 13.417554485999972 | 565497856 | 666497024 | COMPLETE; values written; n_R_S stored as null (see anomalies) |
| ITEM-6 | COMPLETE | 151.49511966299997 | 565293056 | 666497024 | COMPLETE; every row tagged NOT INDEPENDENTLY REPLAYED |
| ITEM-7 | COMPLETE | 10.566568619999998 | 766574592 | 804216832 | COMPLETE; every PM-ACT and PM_k quotient well-defined |
| ITEM-8 | ENGINEERING-FAILURE | 2.0438063080000575 | 713957376 | 804216832 | ENGINEERING-FAILURE (KeyError well_defined). Corrected result is the D1 rerun. |
| ITEM-9 | COMPLETE | 26.576236177999817 | 713981952 | 804216832 | COMPLETE on the quantities still in memory; settings list empty because ITEM-8 had not stored them. Corrected result is the D1 rerun. |

D1 rerun, which does not replace the rows above:

| Item | Status | Wall seconds (float) | Peak RSS bytes | HWM bytes |
| --- | --- | ---: | ---: | ---: |
| ITEM-8 | COMPLETE | 32.39557219100061 | 706473984 | 800313344 |
| ITEM-9 | COMPLETE | 26.92538390899972 | 698114048 | 800313344 |

The frozen runner records one budget per item. It does not record a separate wall time or peak for each agent. Caps were 4 hours total, 1 hour per item, 8 GB resident, one CPU. The longest item was ITEM-2 at 1045.629 seconds. The largest HWM was 804216832 bytes on the freeze run. Neither cap was hit. No horizon or grid was shortened.

ITEM-9 D1 integrity: **AGREE**. Mismatches: none. PM partitions equal on all four machines. MB pattern keys match at T_SEP = 3 for both K_SEP costs. R-CG mixture values at T_SEP = 3 match `replay_cg_y`. Labels were not withheld.

## ITEM-1 conclusion

Outcome: **VERIFIED**.

Verbatim wording used:

> Without recheck observations, the observation history supplies no information about Z beyond its propagated prior. Recheck observations can be informative. This does not imply perfect identification of the realized regime within a finite horizon.

Checked: 16 P cells equal, 128 M cells equal, 3,006,865 histories through length 3 with equal path likelihoods, propagated prior 1/2, 10 nonempty likelihood-ratio classes with constant within-class ratios, ratios all distinct, 136 endpoint decisions coincide. eps = 23/100 in both regimes.

## A-SEP setting labels

The spec defines an A-SEP label per setting. It does not define a further label that collapses the four settings into one. The four labels are the study outcomes.

| T_SEP | c_R | c_S | Label | Note |
| ---: | --- | --- | --- | --- |
| 3 | 1/50 | 3/50 | UNRESOLVED-DESIGN | reference criterion undefined: C-SEL,rescue |
| 3 | 1/100 | 1/10 | REFERENCE CRITERIA NOT MET | the reference does not meet the required conjunction |
| 4 | 1/50 | 3/50 | UNRESOLVED-DESIGN | reference criterion undefined: C-SEL,rescue |
| 4 | 1/100 | 1/10 | REFERENCE CRITERIA NOT MET | the reference does not meet the required conjunction |

Verbatim sentences, from the spec, attached by the runner when a label is issued:

- T_SEP = 3, c_R = 1/50, c_S = 3/50: an output, intervention correspondence or criterion is undefined.
- T_SEP = 3, c_R = 1/100, c_S = 1/10: the reference does not meet the required conjunction.
- T_SEP = 4, c_R = 1/50, c_S = 3/50: an output, intervention correspondence or criterion is undefined.
- T_SEP = 4, c_R = 1/100, c_S = 1/10: the reference does not meet the required conjunction.

No setting is DISTINGUISHES NAMED CONTROLS. No setting is PATTERN REPRODUCED BY NAMED CONTROL. No setting is CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED. No setting is UNRESOLVED-COMPUTE.

Two settings, (T_SEP, c_R, c_S) = (3, 1/50, 3/50) and (4, 1/50, 3/50), are UNRESOLVED-DESIGN because the reference donors are identical (both the empty recheck-count vector). C-SEL and rescue are NOT EVALUABLE [NO INTERVENTION CONTRAST]. The donor rule was not replaced.

Two settings, (3, 1/100, 1/10) and (4, 1/100, 1/10), are REFERENCE CRITERIA NOT MET. The reference donors differ. C-REF is FAIL on the reference because Δ_M = 0/1, which is below the floor 1/100, while Δ_R is above that floor. C-T2, C-FO and rescue pass on the reference in both of these settings. C-SEL passes at T_SEP = 4 and fails at T_SEP = 3 (D_q = 0/1 on both SWAP directions).

Decision order checks the reference before reproduction. Reproduction YES on a control does not change a setting whose reference fails or whose reference criterion is undefined. That happens here: R-HAC-MB-myopic reproduces the reference pattern in all four settings, and PM-ACT reproduces it at T_SEP = 4, c_R = 1/100, c_S = 1/10.

## ITEM-8 agents and rivals

Reference and every eligible control are listed. Criterion flags, reproduction, and the I-SWAP, I-CORRUPT and I-SUSPEND statistics are the exact strings from `outputs/deviation_1/ITEM-8.json`. Intervention fields are D_e, D_q, e_now, q_now, e_intact, q_intact, eA, eB, qA, qB, LA, LB, and repair_equals_shadow. Directions S and E are the two swap directions. Wall time and peak memory for every row in this section are the ITEM-8 D1 figures: wall 32.39557219100061 seconds, sampled peak RSS 706473984 bytes, HWM 800313344 bytes.

### T_SEP = 3, c_R = 1/50, c_S = 3/50

Label: **UNRESOLVED-DESIGN**.

Note: reference criterion undefined: C-SEL,rescue

Verbatim: an output, intervention correspondence or criterion is undefined.

pm_undefined: false. λ_R = 2302211/2833600, λ_M = 432817/500000.

| Agent | C-REF | C-T2 | C-SEL | C-FO | rescue | Conjunction | Reproduction | Unavailable components | t2 note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-HAC-MB | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | reference | pattern source |  | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-HAC-MB-myopic | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | YES |  | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-BLIND / R-CONF-S | FAIL | FAIL | NOT APPLICABLE | PASS | NOT APPLICABLE | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/20 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/20 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/20 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/10 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/10 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/10 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/5 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/5 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/5 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CG alpha=(1,1) beta=0 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(1,1) beta=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(1,1) beta=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(2,1) beta=0 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(2,1) beta=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(2,1) beta=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-HAC-MF eps=0 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-HAC-MF eps=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| PM-ACT | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |

#### R-HAC-MB

Reference pattern source. donor_contrast = false. donor_S = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]. donor_E = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].

Δ_R = `0/1`. Δ_M = `0/1`. E_err_agent = `0/1`. E_err_baseline = `0/1`.

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

#### R-HAC-MB-myopic

Reproduction: YES. Disagreeing components: []. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

#### R-BLIND / R-CONF-S

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

Intervention statistics: none stored.

#### R-CONF-A eta=1/20 alpha=1/20

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/10

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/5

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/20

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/10

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/5

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/20

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/10

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/5

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CG alpha=(1,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "122199/1000000",
  "qB": "129481938201/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "0/1",
  "qB": "129481938201/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-392283/1416800",
  "q_now": "122199/1000000",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "122199/1000000",
  "qB": "1319901826551/8000000000000",
  "LA": "392283/1416800",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6917344900703/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "122199/1000000",
  "qB": "129481938201/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "0/1",
  "qB": "129481938201/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-61641/177100",
  "q_now": "122199/1000000",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "169608912627/1000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "848915329/976562500"
}
```

#### R-CG alpha=(1,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "122199/1000000",
  "qB": "129481938201/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "0/1",
  "qB": "129481938201/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-392283/1416800",
  "q_now": "122199/1000000",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "122199/1000000",
  "qB": "1319901826551/8000000000000",
  "LA": "392283/1416800",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6917344900703/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "122199/1000000",
  "qB": "129481938201/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "0/1",
  "qB": "129481938201/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-61641/177100",
  "q_now": "122199/1000000",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "169608912627/1000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "848915329/976562500"
}
```

#### R-CG alpha=(1,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-392283/1416800",
  "q_now": "122199/1000000",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6917344900703/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-61641/177100",
  "q_now": "122199/1000000",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "848915329/976562500"
}
```

#### R-CG alpha=(2,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-468449/4250400",
  "q_now": "122199/1000000",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "468449/4250400",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6917344900703/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-96373/531300",
  "q_now": "122199/1000000",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "848915329/976562500"
}
```

#### R-CG alpha=(2,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-468449/4250400",
  "q_now": "122199/1000000",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "468449/4250400",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6917344900703/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-96373/531300",
  "q_now": "122199/1000000",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "848915329/976562500"
}
```

#### R-CG alpha=(2,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-468449/4250400",
  "q_now": "122199/1000000",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "468449/4250400",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6917344900703/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-96373/531300",
  "q_now": "122199/1000000",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "848915329/976562500"
}
```

#### R-HAC-MF eps=0

Reproduction: NO. Disagreeing components: ['E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "316117/1416800",
  "q_now": "0/1",
  "e_intact": "316117/1416800",
  "q_intact": "122199/1000000",
  "eA": "316117/1416800",
  "eB": "316117/1416800",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "316117/1416800",
  "LB": "316117/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "316117/1416800",
  "q_now": "0/1",
  "e_intact": "316117/1416800",
  "q_intact": "122199/1000000",
  "eA": "316117/1416800",
  "eB": "316117/1416800",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "316117/1416800",
  "LB": "316117/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "316117/1416800",
  "q_now": "122199/1000000",
  "e_intact": "316117/1416800",
  "q_intact": "122199/1000000",
  "eA": "316117/1416800",
  "eB": "316117/1416800",
  "qA": "122199/1000000",
  "qB": "164541075699/1000000000000",
  "LA": "316117/1416800",
  "LB": "316117/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6917344900703/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "26909/177100",
  "q_now": "0/1",
  "e_intact": "26909/177100",
  "q_intact": "122199/1000000",
  "eA": "26909/177100",
  "eB": "26909/177100",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "26909/177100",
  "LB": "26909/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "26909/177100",
  "q_now": "0/1",
  "e_intact": "26909/177100",
  "q_intact": "122199/1000000",
  "eA": "26909/177100",
  "eB": "26909/177100",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "26909/177100",
  "LB": "26909/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "26909/177100",
  "q_now": "122199/1000000",
  "e_intact": "26909/177100",
  "q_intact": "122199/1000000",
  "eA": "26909/177100",
  "eB": "26909/177100",
  "qA": "122199/1000000",
  "qB": "164541075699/1000000000000",
  "LA": "26909/177100",
  "LB": "26909/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "848915329/976562500"
}
```

#### R-HAC-MF eps=1/10

Reproduction: NO. Disagreeing components: ['E_err_agent', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "316117/1416800",
  "q_now": "1/30",
  "e_intact": "316117/1416800",
  "q_intact": "10198537/75000000",
  "eA": "1011562252711/4533760000000",
  "eB": "1011562252711/4533760000000",
  "qA": "10198537/75000000",
  "qB": "795371129421761/6000000000000000",
  "LA": "101156486482397/453376000000000",
  "LB": "101156486482397/453376000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "64858713673/75000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "316117/1416800",
  "q_now": "1/30",
  "e_intact": "316117/1416800",
  "q_intact": "10198537/75000000",
  "eA": "316117/1416800",
  "eB": "1011562252711/4533760000000",
  "qA": "1/30",
  "qB": "795371129421761/6000000000000000",
  "LA": "316117/1416800",
  "LB": "101156486482397/453376000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "64858713673/75000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "316117/1416800",
  "q_now": "10198537/75000000",
  "e_intact": "316117/1416800",
  "q_intact": "10198537/75000000",
  "eA": "316117/1416800",
  "eB": "60689667268786481833/272025600000000000000",
  "qA": "10198537/75000000",
  "qB": "8175756275857/46875000000000",
  "LA": "316117/1416800",
  "LB": "2023023291401635675697/9067520000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "518382902128289/600000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "26909/177100",
  "q_now": "1/30",
  "e_intact": "26909/177100",
  "q_intact": "10198537/75000000",
  "eA": "10758306481/70840000000",
  "eB": "10758306481/70840000000",
  "qA": "10198537/75000000",
  "qB": "783016248401/5859375000000",
  "LA": "269061475973/1771000000000",
  "LB": "269061475973/1771000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "129906511721/150000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "26909/177100",
  "q_now": "1/30",
  "e_intact": "26909/177100",
  "q_intact": "10198537/75000000",
  "eA": "26909/177100",
  "eB": "10758306481/70840000000",
  "qA": "1/30",
  "qB": "783016248401/5859375000000",
  "LA": "26909/177100",
  "LB": "269061475973/1771000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "129906511721/150000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "26909/177100",
  "q_now": "10198537/75000000",
  "e_intact": "26909/177100",
  "q_intact": "10198537/75000000",
  "eA": "26909/177100",
  "eB": "5045199228418529/33206250000000000",
  "qA": "10198537/75000000",
  "qB": "8175756275857/46875000000000",
  "LA": "26909/177100",
  "LB": "42044884526030119/276718750000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "16295884891237/18750000000000"
}
```

#### PM-ACT

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

### T_SEP = 3, c_R = 1/100, c_S = 1/10

Label: **REFERENCE CRITERIA NOT MET**.

Note: the reference does not meet the required conjunction

Verbatim: the reference does not meet the required conjunction.

pm_undefined: false. λ_R = 2302211/2833600, λ_M = 432817/500000.

| Agent | C-REF | C-T2 | C-SEL | C-FO | rescue | Conjunction | Reproduction | Unavailable components | t2 note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-HAC-MB | FAIL | PASS | FAIL | PASS | PASS | reference | pattern source |  |  |
| R-HAC-MB-myopic | FAIL | PASS | FAIL | PASS | PASS | FAILS | YES |  |  |
| R-BLIND / R-CONF-S | FAIL | FAIL | NOT APPLICABLE | PASS | NOT APPLICABLE | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CONF-A eta=1/20 alpha=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/20 alpha=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/20 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CONF-A eta=1/10 alpha=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/10 alpha=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/10 alpha=1/5 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/5 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CONF-A eta=1/5 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CONF-A eta=1/5 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(1,1) beta=0 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(1,1) beta=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(1,1) beta=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(2,1) beta=0 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(2,1) beta=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(2,1) beta=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-HAC-MF eps=0 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-HAC-MF eps=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| PM-ACT | FAIL | PASS | FAIL | PASS | PASS | FAILS | NO |  |  |

#### R-HAC-MB

Reference pattern source. donor_contrast = true. donor_S = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]. donor_E = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0].

Δ_R = `195832809371055087/8192000000000000000`. Δ_M = `0/1`. E_err_agent = `0/1`. E_err_baseline = `99539673572231959713013212436330865738931788009956151441855101232551048030706615929560054034186710415904633964906186669231216521839985775444600812105304520931067355381105785919901995582343620732243470808687151801976219794446802303598973836152873417728383415646531803919650877191830571447941247891636958313/987637823497158472895435273107113552552468458608156127112047199973284493942622315499754999147939927671663300285323586783203677697611380688371764327874419748940348971687093323266283378219639549588163464164421805995037121252143554110166590951723912189720038822442084111485486053660996777663047075164160000000000`.

I-SWAP-S:

```json
{
  "D_e": "932124803307332506383683307347995070143128711730491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "1990656/28699055",
  "q_now": "1/1",
  "e_intact": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "31538590053682391559343589413116095621945995037314628521996551949515606617999049741846343157047296/467565258474955531744334125353601195671461317135878439617474305255418660184640551776469047915509375",
  "eB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "31538590053682391559343589413116095621945995037314628521996551949515606617999049741846343157047296/467565258474955531744334125353601195671461317135878439617474305255418660184640551776469047915509375",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "932124803307332506383683307347995070143128711730491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "1990656/28699055",
  "q_now": "1/1",
  "e_intact": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "1990656/28699055",
  "eB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "1990656/28699055",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_now": "1/1",
  "e_intact": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "eB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "-790806993574950226395366582012343699203134457430491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "-31061893689/490602986720",
  "q_now": "1/1",
  "e_intact": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "-1643063876258686117467509669819419313613780017162298000881727093440804401352974460131668195550688524793349/29137599864515056482495202870465904656493922623052276337525864675860072527989912734617783087855049541100000",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "228223/250000",
  "qB": "998518212217/1000000000000",
  "LA": "1643063876258686117467509669819419313613780017162298000881727093440804401352974460131668195550688524793349/29137599864515056482495202870465904656493922623052276337525864675860072527989912734617783087855049541100000",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-790806993574950226395366582012343699203134457430491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "-31061893689/490602986720",
  "q_now": "1/1",
  "e_intact": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "-31061893689/490602986720",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "998518212217/1000000000000",
  "LA": "31061893689/490602986720",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_now": "1/1",
  "e_intact": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "998518212217/1000000000000",
  "LA": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

#### R-HAC-MB-myopic

Reproduction: YES. Disagreeing components: []. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "932124803307332506383683307347995070143128711730491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "1990656/28699055",
  "q_now": "1/1",
  "e_intact": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "31538590053682391559343589413116095621945995037314628521996551949515606617999049741846343157047296/467565258474955531744334125353601195671461317135878439617474305255418660184640551776469047915509375",
  "eB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "31538590053682391559343589413116095621945995037314628521996551949515606617999049741846343157047296/467565258474955531744334125353601195671461317135878439617474305255418660184640551776469047915509375",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "932124803307332506383683307347995070143128711730491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "1990656/28699055",
  "q_now": "1/1",
  "e_intact": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "1990656/28699055",
  "eB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "1990656/28699055",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_now": "1/1",
  "e_intact": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "eB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "-790806993574950226395366582012343699203134457430491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "-31061893689/490602986720",
  "q_now": "1/1",
  "e_intact": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "-1643063876258686117467509669819419313613780017162298000881727093440804401352974460131668195550688524793349/29137599864515056482495202870465904656493922623052276337525864675860072527989912734617783087855049541100000",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "228223/250000",
  "qB": "998518212217/1000000000000",
  "LA": "1643063876258686117467509669819419313613780017162298000881727093440804401352974460131668195550688524793349/29137599864515056482495202870465904656493922623052276337525864675860072527989912734617783087855049541100000",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-790806993574950226395366582012343699203134457430491/23360581140035387934778452917186555251135626185600000",
  "D_q": "0/1",
  "e_now": "-31061893689/490602986720",
  "q_now": "1/1",
  "e_intact": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "-31061893689/490602986720",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "998518212217/1000000000000",
  "LA": "31061893689/490602986720",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_now": "1/1",
  "e_intact": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "q_intact": "1/1",
  "eA": "-688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "1/1",
  "qB": "998518212217/1000000000000",
  "LA": "688237992955411517929811892069369694306594147789509/23360581140035387934778452917186555251135626185600000",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

#### R-BLIND / R-CONF-S

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

Intervention statistics: none stored.

#### R-CONF-A eta=1/20 alpha=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/5

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/5

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/20

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/10

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/5

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CG alpha=(1,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "122199/1000000",
  "qB": "129481938201/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "0/1",
  "qB": "129481938201/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-392283/1416800",
  "q_now": "122199/1000000",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "122199/1000000",
  "qB": "1319901826551/8000000000000",
  "LA": "392283/1416800",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6922995060831/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "122199/1000000",
  "qB": "129481938201/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "0/1",
  "qB": "129481938201/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-61641/177100",
  "q_now": "122199/1000000",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "169608912627/1000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "13593680733/15625000000"
}
```

#### R-CG alpha=(1,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-392283/1416800",
  "q_now": "122199/1000000",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6922995060831/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-61641/177100",
  "q_now": "122199/1000000",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "13593680733/15625000000"
}
```

#### R-CG alpha=(1,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-392283/1416800",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "392283/1416800",
  "LB": "392283/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-392283/1416800",
  "q_now": "122199/1000000",
  "e_intact": "-392283/1416800",
  "q_intact": "122199/1000000",
  "eA": "-392283/1416800",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6922995060831/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-61641/177100",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "61641/177100",
  "LB": "61641/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-61641/177100",
  "q_now": "122199/1000000",
  "e_intact": "-61641/177100",
  "q_intact": "122199/1000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "13593680733/15625000000"
}
```

#### R-CG alpha=(2,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-468449/4250400",
  "q_now": "122199/1000000",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "468449/4250400",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6922995060831/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-96373/531300",
  "q_now": "122199/1000000",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "13593680733/15625000000"
}
```

#### R-CG alpha=(2,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-468449/4250400",
  "q_now": "122199/1000000",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "468449/4250400",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6922995060831/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-96373/531300",
  "q_now": "122199/1000000",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "13593680733/15625000000"
}
```

#### R-CG alpha=(2,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-468449/4250400",
  "q_now": "0/1",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-468449/4250400",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "468449/4250400",
  "LB": "468449/4250400",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-468449/4250400",
  "q_now": "122199/1000000",
  "e_intact": "-468449/4250400",
  "q_intact": "122199/1000000",
  "eA": "-468449/4250400",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "122199/1000000",
  "qB": "1719835691343/8000000000000",
  "LA": "468449/4250400",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6922995060831/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-96373/531300",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "96373/531300",
  "LB": "96373/531300",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-96373/531300",
  "q_now": "122199/1000000",
  "e_intact": "-96373/531300",
  "q_intact": "122199/1000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "109800322863/500000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "13593680733/15625000000"
}
```

#### R-HAC-MF eps=0

Reproduction: NO. Disagreeing components: ['delta_R', 'E_err_agent']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "316117/1416800",
  "q_now": "0/1",
  "e_intact": "316117/1416800",
  "q_intact": "122199/1000000",
  "eA": "316117/1416800",
  "eB": "316117/1416800",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "316117/1416800",
  "LB": "316117/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "316117/1416800",
  "q_now": "0/1",
  "e_intact": "316117/1416800",
  "q_intact": "122199/1000000",
  "eA": "316117/1416800",
  "eB": "316117/1416800",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "316117/1416800",
  "LB": "316117/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "316117/1416800",
  "q_now": "122199/1000000",
  "e_intact": "316117/1416800",
  "q_intact": "122199/1000000",
  "eA": "316117/1416800",
  "eB": "316117/1416800",
  "qA": "122199/1000000",
  "qB": "164541075699/1000000000000",
  "LA": "316117/1416800",
  "LB": "316117/1416800",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6922995060831/8000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "26909/177100",
  "q_now": "0/1",
  "e_intact": "26909/177100",
  "q_intact": "122199/1000000",
  "eA": "26909/177100",
  "eB": "26909/177100",
  "qA": "122199/1000000",
  "qB": "229465404399/1000000000000",
  "LA": "26909/177100",
  "LB": "26909/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-122199/1000000",
  "e_now": "26909/177100",
  "q_now": "0/1",
  "e_intact": "26909/177100",
  "q_intact": "122199/1000000",
  "eA": "26909/177100",
  "eB": "26909/177100",
  "qA": "0/1",
  "qB": "229465404399/1000000000000",
  "LA": "26909/177100",
  "LB": "26909/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "432817/500000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "26909/177100",
  "q_now": "122199/1000000",
  "e_intact": "26909/177100",
  "q_intact": "122199/1000000",
  "eA": "26909/177100",
  "eB": "26909/177100",
  "qA": "122199/1000000",
  "qB": "164541075699/1000000000000",
  "LA": "26909/177100",
  "LB": "26909/177100",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "13593680733/15625000000"
}
```

#### R-HAC-MF eps=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "316117/1416800",
  "q_now": "1/30",
  "e_intact": "316117/1416800",
  "q_intact": "10198537/75000000",
  "eA": "1011562252711/4533760000000",
  "eB": "1011562252711/4533760000000",
  "qA": "10198537/75000000",
  "qB": "795371129421761/6000000000000000",
  "LA": "101156486482397/453376000000000",
  "LB": "101156486482397/453376000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "64783713673/75000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "316117/1416800",
  "q_now": "1/30",
  "e_intact": "316117/1416800",
  "q_intact": "10198537/75000000",
  "eA": "316117/1416800",
  "eB": "1011562252711/4533760000000",
  "qA": "1/30",
  "qB": "795371129421761/6000000000000000",
  "LA": "316117/1416800",
  "LB": "101156486482397/453376000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "64783713673/75000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "316117/1416800",
  "q_now": "10198537/75000000",
  "e_intact": "316117/1416800",
  "q_intact": "10198537/75000000",
  "eA": "316117/1416800",
  "eB": "60689667268786481833/272025600000000000000",
  "qA": "10198537/75000000",
  "qB": "8175756275857/46875000000000",
  "LA": "316117/1416800",
  "LB": "2023023291401635675697/9067520000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "518138862216353/600000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "26909/177100",
  "q_now": "1/30",
  "e_intact": "26909/177100",
  "q_intact": "10198537/75000000",
  "eA": "10758306481/70840000000",
  "eB": "10758306481/70840000000",
  "qA": "10198537/75000000",
  "qB": "783016248401/5859375000000",
  "LA": "269061475973/1771000000000",
  "LB": "269061475973/1771000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "129756511721/150000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "-2566179/25000000",
  "e_now": "26909/177100",
  "q_now": "1/30",
  "e_intact": "26909/177100",
  "q_intact": "10198537/75000000",
  "eA": "26909/177100",
  "eB": "10758306481/70840000000",
  "qA": "1/30",
  "qB": "783016248401/5859375000000",
  "LA": "26909/177100",
  "LB": "269061475973/1771000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "129756511721/150000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "26909/177100",
  "q_now": "10198537/75000000",
  "e_intact": "26909/177100",
  "q_intact": "10198537/75000000",
  "eA": "26909/177100",
  "eB": "5045199228418529/33206250000000000",
  "qA": "10198537/75000000",
  "qB": "8175756275857/46875000000000",
  "LA": "26909/177100",
  "LB": "42044884526030119/276718750000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "16288258643989/18750000000000"
}
```

#### PM-ACT

Reproduction: NO. Disagreeing components: ['e_A_S', 'e_A_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "608605906909714433008436722569671532316482717777639/15254392817852079805844486658690114726114582874900000",
  "D_q": "0/1",
  "e_now": "1990656/28699055",
  "q_now": "1/1",
  "e_intact": "40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_intact": "1/1",
  "eA": "14138287323831180028216950105206286/216282585042407018054459896738353125",
  "eB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "14138287323831180028216950105206286/216282585042407018054459896738353125",
  "LB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "608605906909714433008436722569671532316482717777639/15254392817852079805844486658690114726114582874900000",
  "D_q": "0/1",
  "e_now": "1990656/28699055",
  "q_now": "1/1",
  "e_intact": "40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_intact": "1/1",
  "eA": "58892951199154176/841224294549078055",
  "eB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "58892951199154176/841224294549078055",
  "LB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_now": "1/1",
  "e_intact": "40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_intact": "1/1",
  "eA": "131779318868690539343213292414692344740954921902632093538507797996032524496069/4319035667745997668428585012064961329622156335647077795030441678551464234500000",
  "eB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "qA": "1/1",
  "qB": "3905634710386837/4096000000000000",
  "LA": "131779318868690539343213292414692344740954921902632093538507797996032524496069/4319035667745997668428585012064961329622156335647077795030441678551464234500000",
  "LB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "-258162890224114888470369810097634777145826873218507/7627196408926039902922243329345057363057291437450000",
  "D_q": "0/1",
  "e_now": "-31061893689/490602986720",
  "q_now": "1/1",
  "e_intact": "-40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_intact": "1/1",
  "eA": "-178863887105503364861327288918738504280838899839310331952194027379127346864713/3109179746438593273399680436424825983305002435335602927121156785761398261900000",
  "eB": "-20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "qA": "228223/250000",
  "qB": "998518212217/1000000000000",
  "LA": "178863887105503364861327288918738504280838899839310331952194027379127346864713/3109179746438593273399680436424825983305002435335602927121156785761398261900000",
  "LB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-258162890224114888470369810097634777145826873218507/7627196408926039902922243329345057363057291437450000",
  "D_q": "0/1",
  "e_now": "-31061893689/490602986720",
  "q_now": "1/1",
  "e_intact": "-40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_intact": "1/1",
  "eA": "-409562654375810997/6330575490129937760",
  "eB": "-20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "qA": "1/1",
  "qB": "998518212217/1000000000000",
  "LA": "409562654375810997/6330575490129937760",
  "LB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_now": "1/1",
  "e_intact": "-40862397713372206952396235755037560968608187663851/1386762983441098164167680605335464975101325715900000",
  "q_intact": "1/1",
  "eA": "-875015943923779821658601559600363405967974766890586042267734984190922970271797/30233249674221983679000095084454729307355094349529544565213091749860249641500000",
  "eB": "-20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "qA": "1/1",
  "qB": "998518212217/1000000000000",
  "LA": "875015943923779821658601559600363405967974766890586042267734984190922970271797/30233249674221983679000095084454729307355094349529544565213091749860249641500000",
  "LB": "20931702864032829003461522957736750593576415050646266461008334964504483973383997942452388890122440258597/827085571179364278953072145147273402386906571011873209834519608863645144018938446572252626005448437500000",
  "repair_equals_shadow": true
}
```

### T_SEP = 4, c_R = 1/50, c_S = 3/50

Label: **UNRESOLVED-DESIGN**.

Note: reference criterion undefined: C-SEL,rescue

Verbatim: an output, intervention correspondence or criterion is undefined.

pm_undefined: false. λ_R = 2302211/2833600, λ_M = 432817/500000.

| Agent | C-REF | C-T2 | C-SEL | C-FO | rescue | Conjunction | Reproduction | Unavailable components | t2 note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-HAC-MB | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | reference | pattern source |  | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-HAC-MB-myopic | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | YES |  | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-BLIND / R-CONF-S | FAIL | FAIL | NOT APPLICABLE | PASS | NOT APPLICABLE | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/20 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/20 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/20 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/10 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/10 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/10 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/5 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/5 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CONF-A eta=1/5 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |
| R-CG alpha=(1,1) beta=0 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(1,1) beta=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(1,1) beta=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(2,1) beta=0 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(2,1) beta=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(2,1) beta=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| PM-ACT | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | UNRESOLVED | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E | NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated. |

#### R-HAC-MB

Reference pattern source. donor_contrast = false. donor_S = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]. donor_E = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0].

Δ_R = `0/1`. Δ_M = `0/1`. E_err_agent = `0/1`. E_err_baseline = `0/1`.

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

#### R-HAC-MB-myopic

Reproduction: YES. Disagreeing components: []. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

#### R-BLIND / R-CONF-S

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

Intervention statistics: none stored.

#### R-CONF-A eta=1/20 alpha=1/20

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/10

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/5

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/20

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/10

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/5

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/20

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/10

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/5

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

#### R-CG alpha=(1,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1319901826551/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "2807629654662066927/25000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1319901826551/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "2807629654662066927/25000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3837934298548593/14168000000000000",
  "q_now": "1319901826551/8000000000000",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-3837934298548593/14168000000000000",
  "eB": "-119932539345027640279971/453376000000000000000000",
  "qA": "1319901826551/8000000000000",
  "qB": "92181091799821563/500000000000000000",
  "LA": "3837934298548593/14168000000000000",
  "LB": "119932539345027640279971/453376000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "1080725898238566278547/1250000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-169608912627/1000000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "155700240251272101/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-169608912627/1000000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "0/1",
  "qB": "155700240251272101/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-603069998182011/1771000000000000",
  "q_now": "169608912627/1000000000000",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-603069998182011/1771000000000000",
  "eB": "-2352862942637654867859/7084000000000000000000",
  "qA": "169608912627/1000000000000",
  "qB": "193315266078204501/1000000000000000000",
  "LA": "603069998182011/1771000000000000",
  "LB": "2352862942637654867859/7084000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4354375470442286206233/5000000000000000000000"
}
```

#### R-CG alpha=(1,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1319901826551/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "2807629654662066927/25000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1319901826551/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "2807629654662066927/25000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3837934298548593/14168000000000000",
  "q_now": "1319901826551/8000000000000",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-3837934298548593/14168000000000000",
  "eB": "-119932539345027640279971/453376000000000000000000",
  "qA": "1319901826551/8000000000000",
  "qB": "92181091799821563/500000000000000000",
  "LA": "3837934298548593/14168000000000000",
  "LB": "119932539345027640279971/453376000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "1080725898238566278547/1250000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-169608912627/1000000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "155700240251272101/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-169608912627/1000000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "0/1",
  "qB": "155700240251272101/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-603069998182011/1771000000000000",
  "q_now": "169608912627/1000000000000",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-603069998182011/1771000000000000",
  "eB": "-2352862942637654867859/7084000000000000000000",
  "qA": "169608912627/1000000000000",
  "qB": "193315266078204501/1000000000000000000",
  "LA": "603069998182011/1771000000000000",
  "LB": "2352862942637654867859/7084000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4354375470442286206233/5000000000000000000000"
}
```

#### R-CG alpha=(1,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3837934298548593/14168000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-3837934298548593/14168000000000000",
  "eB": "-118821150021524534516547/453376000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "2153448110025278451/8000000000000000000",
  "LA": "3837934298548593/14168000000000000",
  "LB": "118821150021524534516547/453376000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4320900816505227086063/5000000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-603069998182011/1771000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-603069998182011/1771000000000000",
  "eB": "-2331033310302690396303/7084000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "280024627353359427/1000000000000000000",
  "LA": "603069998182011/1771000000000000",
  "LB": "2331033310302690396303/7084000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4361825349601439406233/5000000000000000000000"
}
```

#### R-CG alpha=(2,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-18433822631448137/170016000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-18433822631448137/170016000000000000",
  "eB": "-179998082812391509833683/1700160000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "16844918531923181007/64000000000000000000",
  "LA": "18433822631448137/170016000000000000",
  "LB": "14530782921998825347026169/136012800000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4320900816505227086063/5000000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3792350476701949/21252000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-3792350476701949/21252000000000000",
  "eB": "-18479541531636625391453/106260000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "137789916721894899/500000000000000000",
  "LA": "3792350476701949/21252000000000000",
  "LB": "18479541531636625391453/106260000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4361825349601439406233/5000000000000000000000"
}
```

#### R-CG alpha=(2,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-18433822631448137/170016000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-18433822631448137/170016000000000000",
  "eB": "-179998082812391509833683/1700160000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "16844918531923181007/64000000000000000000",
  "LA": "18433822631448137/170016000000000000",
  "LB": "14530782921998825347026169/136012800000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4320900816505227086063/5000000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3792350476701949/21252000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-3792350476701949/21252000000000000",
  "eB": "-18479541531636625391453/106260000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "137789916721894899/500000000000000000",
  "LA": "3792350476701949/21252000000000000",
  "LB": "18479541531636625391453/106260000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4361825349601439406233/5000000000000000000000"
}
```

#### R-CG alpha=(2,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4422831721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-18433822631448137/170016000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-18433822631448137/170016000000000000",
  "eB": "-179998082812391509833683/1700160000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "16844918531923181007/64000000000000000000",
  "LA": "18433822631448137/170016000000000000",
  "LB": "14530782921998825347026169/136012800000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4320900816505227086063/5000000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "104689/125000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3792350476701949/21252000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-3792350476701949/21252000000000000",
  "eB": "-18479541531636625391453/106260000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "137789916721894899/500000000000000000",
  "LA": "3792350476701949/21252000000000000",
  "LB": "18479541531636625391453/106260000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4361825349601439406233/5000000000000000000000"
}
```

#### PM-ACT

Reproduction: UNRESOLVED. Disagreeing components: []. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "0/1",
  "e_intact": "20169/566720",
  "q_intact": "0/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "0/1",
  "e_intact": "-20169/566720",
  "q_intact": "0/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "0/1",
  "qB": "0/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true
}
```

### T_SEP = 4, c_R = 1/100, c_S = 1/10

Label: **REFERENCE CRITERIA NOT MET**.

Note: the reference does not meet the required conjunction

Verbatim: the reference does not meet the required conjunction.

pm_undefined: false. λ_R = 2302211/2833600, λ_M = 432817/500000.

| Agent | C-REF | C-T2 | C-SEL | C-FO | rescue | Conjunction | Reproduction | Unavailable components | t2 note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-HAC-MB | FAIL | PASS | PASS | PASS | PASS | reference | pattern source |  |  |
| R-HAC-MB-myopic | FAIL | PASS | PASS | PASS | PASS | FAILS | YES |  |  |
| R-BLIND / R-CONF-S | FAIL | FAIL | NOT APPLICABLE | PASS | NOT APPLICABLE | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CONF-A eta=1/20 alpha=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/20 alpha=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/20 alpha=1/5 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/10 alpha=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/10 alpha=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/10 alpha=1/5 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CONF-A eta=1/5 alpha=1/20 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CONF-A eta=1/5 alpha=1/10 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CONF-A eta=1/5 alpha=1/5 | FAIL | FAIL | NOT EVALUABLE [NO INTERVENTION CONTRAST] | PASS | NOT EVALUABLE [NO INTERVENTION CONTRAST] | FAILS | NO | D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |  |
| R-CG alpha=(1,1) beta=0 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(1,1) beta=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(1,1) beta=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(2,1) beta=0 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(2,1) beta=1/20 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| R-CG alpha=(2,1) beta=1/10 | FAIL | FAIL | FAIL | PASS | FAIL | FAILS | NO |  |  |
| PM-ACT | FAIL | PASS | PASS | PASS | PASS | FAILS | YES |  |  |

#### R-HAC-MB

Reference pattern source. donor_contrast = true. donor_S = [2, 0, 0, 0, 0, 0, 0, 0, 0, 0]. donor_E = [0, 0, 0, 0, 0, 0, 2, 0, 0, 0].

Δ_R = `23666419670118833657669697/262144000000000000000000000`. Δ_M = `0/1`. E_err_agent = `0/1`. E_err_baseline = `101282664307460238524916659792822547065333581550539832652125646805981083469363407757007285728984466969779308662088137895903858118499500540816733767134187006724125398182334413665901191525782981729816355699548952674962189625448071195756262845112476226598724304326399428266864818383576128359533212885098991694451335710721720445867185746969581752229380063400519771030671233109750620959293296392520402683932718990596050066508180465271021264303859226953580881991987125961694851002859691445611356101053366554458332660818838668266582158137872156074637881769402558719598827775771993599682469510581442044144432124121903715284891427265853114581690479731775207946746593622726704996501393906798017190984125399082160335010838315896122389488539627524182770030199451024662358823720830896195710540878112849628222718039447372751201656459947435954906427447911760405047139828087237651738425421988408808553037048329792098923649579886746068089446591100691523458249197200945173/720006327149380807173621364765181310604857175096875983929255616131711211282730691002956097039556875511437475679746229853810611624165784520470665762776282466707987460857459465439581252844145778765348918366635936407563862520952068235301547564334750951753081100310397238705642616881786265435181822277692493344627951825643996416498888440546181386132480260168608257679548942178622405197984105937116401060518943115914318641962092477073792512221533216782129205418962383696234365987245279347010433632896160739438982538841775023423518626226053119482837804818728920985391842486989091492022931917039138677336061549324401121866265965928631733111703641958788917886071974692494264865005408296628012057166238363208200314813210473430767752534727801792349221430146829442037559305029648913377334116484424316496537764204174646011310174070728794938769976741503957025930337768603673020640159088164198838607078997380443817014935240996879820088506967598774724096000000000000000000`.

I-SWAP-S:

```json
{
  "D_e": "40435083490717206570577981222122132401471599345067988722021036583359734553623310338512183485929002564911165476694879066835084538444856515671109096084506633793017219004245579419043466333951784921305676520922405915758569242410166798546812258450750564260591763173034805116185193267601456356147318921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "190365289613163/4096000000000000",
  "e_now": "43312597696512/608927557773535",
  "q_now": "1/1",
  "e_intact": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "18723026357462349441082467282551458627155601939260865993034503356764276635229673078258321076591547245455428250313788859470686435981286747144192/263442042977923374726532706698504962285594287945728906279025761495813268688480705544202580860433904247502303884162518469362556404567164672596875",
  "eB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "qA": "1/1",
  "qB": "57363643058007836360923/65536000000000000000000",
  "LA": "18723026357462349441082467282551458627155601939260865993034503356764276635229673078258321076591547245455428250313788859470686435981286747144192/263442042977923374726532706698504962285594287945728906279025761495813268688480705544202580860433904247502303884162518469362556404567164672596875",
  "LB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "40435083490717206570577981222122132401471599345067988722021036583359734553623310338512183485929002564911165476694879066835084538444856515671109096084506633793017219004245579419043466333951784921305676520922405915758569242410166798546812258450750564260591763173034805116185193267601456356147318921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "190365289613163/4096000000000000",
  "e_now": "43312597696512/608927557773535",
  "q_now": "1/1",
  "e_intact": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "43312597696512/608927557773535",
  "eB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "qA": "1/1",
  "qB": "57363643058007836360923/65536000000000000000000",
  "LA": "43312597696512/608927557773535",
  "LB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_now": "3905634710386837/4096000000000000",
  "e_intact": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "eB": "3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "qA": "3905634710386837/4096000000000000",
  "qB": "114209097767679072605819/131072000000000000000000",
  "LA": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "LB": "3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "-39535147625898236387834382012089517458607185766239080090505604875681066405637596661831211217150766805508032601640033575066017126179129138471939188178990322748294495178961627539598874893854241634877697669861086356260886465049723381078567528784786765192959540607411219019577823849207366379386509921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "-998518212217/1000000000000",
  "e_now": "-47837832294448809/682456591580714720",
  "q_now": "0/1",
  "e_intact": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-47837832294448809/682456591580714720",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "0/1",
  "qB": "998518212217/1000000000000",
  "LA": "47837832294448809/682456591580714720",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-39535147625898236387834382012089517458607185766239080090505604875681066405637596661831211217150766805508032601640033575066017126179129138471939188178990322748294495178961627539598874893854241634877697669861086356260886465049723381078567528784786765192959540607411219019577823849207366379386509921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "-998518212217/1000000000000",
  "e_now": "-47837832294448809/682456591580714720",
  "q_now": "0/1",
  "e_intact": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-47837832294448809/682456591580714720",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "0/1",
  "qB": "998518212217/1000000000000",
  "LA": "47837832294448809/682456591580714720",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_now": "998518212217/1000000000000",
  "e_intact": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "eB": "-3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "qA": "998518212217/1000000000000",
  "qB": "249068852462102353/250000000000000000",
  "LA": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "LB": "3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "repair_equals_shadow": true
}
```

#### R-HAC-MB-myopic

Reproduction: YES. Disagreeing components: []. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "40435083490717206570577981222122132401471599345067988722021036583359734553623310338512183485929002564911165476694879066835084538444856515671109096084506633793017219004245579419043466333951784921305676520922405915758569242410166798546812258450750564260591763173034805116185193267601456356147318921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "190365289613163/4096000000000000",
  "e_now": "43312597696512/608927557773535",
  "q_now": "1/1",
  "e_intact": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "18723026357462349441082467282551458627155601939260865993034503356764276635229673078258321076591547245455428250313788859470686435981286747144192/263442042977923374726532706698504962285594287945728906279025761495813268688480705544202580860433904247502303884162518469362556404567164672596875",
  "eB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "qA": "1/1",
  "qB": "57363643058007836360923/65536000000000000000000",
  "LA": "18723026357462349441082467282551458627155601939260865993034503356764276635229673078258321076591547245455428250313788859470686435981286747144192/263442042977923374726532706698504962285594287945728906279025761495813268688480705544202580860433904247502303884162518469362556404567164672596875",
  "LB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "40435083490717206570577981222122132401471599345067988722021036583359734553623310338512183485929002564911165476694879066835084538444856515671109096084506633793017219004245579419043466333951784921305676520922405915758569242410166798546812258450750564260591763173034805116185193267601456356147318921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "190365289613163/4096000000000000",
  "e_now": "43312597696512/608927557773535",
  "q_now": "1/1",
  "e_intact": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "43312597696512/608927557773535",
  "eB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "qA": "1/1",
  "qB": "57363643058007836360923/65536000000000000000000",
  "LA": "43312597696512/608927557773535",
  "LB": "81116035745135954543719863114621863324091376742968353264802800605887609776277498448653712609502070508119033691049218768719674498914807297162570096803820389831722586387748532178305958489451335503748516504075324971251027037175736604353585051814550963615538462785012650878351622714875007638145080085502933063558191394780671433786554671212289368690978173536386710059939983942873815499554505132734158365340266245064374032753241261080868805887546931310436971563633197732914497625722522907187197899590065911475144718549450851709261510378702849161160431810941944537795280379496319951208793495680708758820742980338725534357922775427623768267983478504854305920625256830904724958518294390174649685509838410084985967255359928025728704171090062086323722785853447292368023601737646788937561210496324490815120237798573466735786841949591932934520731866127145291693383965072649018679262135933433961706816225184927090173435129496187114984641105483237239671066602271260741710908038534160902869/3871034840638281938270208797064369041845661140367116596915671029813550201434154991833100617397265082960783460014266638582017704195451650289984667328770574106792889309713781968855305933318469155772716463009192504849130173339589544260324510697353051297390569663156822950734649009041208728234208819382908818169151340302935346590865649718915790917427119068223872439939065101346293294666232357278959091158486907346521024597773153359601743533821924580113035464992542906630160083649020561240785716910469210765234465646357513098013083020982617254828564238399862011960213653876642846569466608093004126506653886466732688175952561375035664769856152478707956636381566485965734265695197124294468212547936573320615193750109855168290484073916979946798858407672176853972233583205051561015279669135185357193289329079385099590876954313315676145828794135340277996256910805320451610403764000295232322116948201702434420051932676572492297213482695654765261689917429836548353540679829184000000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_now": "3905634710386837/4096000000000000",
  "e_intact": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "eB": "3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "qA": "3905634710386837/4096000000000000",
  "qB": "114209097767679072605819/131072000000000000000000",
  "LA": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "LB": "3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "-39535147625898236387834382012089517458607185766239080090505604875681066405637596661831211217150766805508032601640033575066017126179129138471939188178990322748294495178961627539598874893854241634877697669861086356260886465049723381078567528784786765192959540607411219019577823849207366379386509921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "-998518212217/1000000000000",
  "e_now": "-47837832294448809/682456591580714720",
  "q_now": "0/1",
  "e_intact": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-47837832294448809/682456591580714720",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "0/1",
  "qB": "998518212217/1000000000000",
  "LA": "47837832294448809/682456591580714720",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-39535147625898236387834382012089517458607185766239080090505604875681066405637596661831211217150766805508032601640033575066017126179129138471939188178990322748294495178961627539598874893854241634877697669861086356260886465049723381078567528784786765192959540607411219019577823849207366379386509921581331/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "D_q": "-998518212217/1000000000000",
  "e_now": "-47837832294448809/682456591580714720",
  "q_now": "0/1",
  "e_intact": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-47837832294448809/682456591580714720",
  "eB": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "qA": "0/1",
  "qB": "998518212217/1000000000000",
  "LA": "47837832294448809/682456591580714720",
  "LB": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_now": "998518212217/1000000000000",
  "e_intact": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "eB": "-3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "qA": "998518212217/1000000000000",
  "qB": "249068852462102353/250000000000000000",
  "LA": "21544375506094424121462337229643188381607005849434466894863325035485440792240014453165972905174643788645861952831559448854878285386437252911147807482841187400873213780593310787365005515277031270443372341778382113396082227149874338840465777635580943732695399070361189374346564696027234439040085878418669/871363127732529708582223384658308823186466384288675295659273715391449475881054414437248552325610466960459574644730719564514820103059165627092536285885816407520776548989883296218841207491918010294469459490067234255926313922345738733560303987616382154961920192019060657366500259088259438226149664000000000",
  "LB": "3328622434909547726376443327767686736599656027384839593121242871961171523100168284811173734137034166687723540071695147150580919621847419552490789398512815333021368800369172778168350337741397419165318617467256704086800218560668497081977020738684590917311688915102897062986809277001189928166199366452429071180312363897846399344281326635356968604559407477432509524529769929496785197996130607542208089108657666882406179451221197476771999574553759263388692772182728347605872292960936473669096583975172690178770080120861759558076717183955422975000143059638565370630600472915962857229751755092498316910291125466438616910104996272812669819217405068296367470732629246736823821536824483110268459318855270624647597112910746005168197646710472279453077774756271703970235688132740465442794932508661636099523954470465800398127188189979970692727658420419477912125035835560580850259260825608641705412846545325354736659771906016695973182867061077641150856132607113283/158809978284995413778766711243025945485613966133380678273498291954517047943148885473195779450071656971572706909881914758128046395081738892325722085592594770501302993730911972720122206037405107188150435481065591563638980122669057964096367598711610440727581764431817572766454910908779085226209993973587594699460922462954368210160857310608894468638057651964066968185247772749025622264518656906655050346846534248816505205825207438654404404340223835576238972821446742592513579454414278512098221704037302534637692012555092246484930527029673630603039817903622803365284409074805259098854578080233435090815583875045084239542072356262491118434082007419622767390879088150341938008409225079542810395161243286633655137195883874186275354790444973221420900407199946499602440205266632753691711541079462590983320194320867149123753832154928535021432536513071701419115775375980129742341932322876420198379949313016225785444076272453080846822175626323134600000000000000000",
  "repair_equals_shadow": true
}
```

#### R-BLIND / R-CONF-S

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

Intervention statistics: none stored.

#### R-CONF-A eta=1/20 alpha=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/20 alpha=1/5

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/10 alpha=1/5

Reproduction: NO. Disagreeing components: ['delta_R', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/20

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/10

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "1/1",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CONF-A eta=1/5 alpha=1/5

Reproduction: NO. Disagreeing components: ['delta_R']. Unavailable: ['D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E'].

I-SWAP-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "43920150964917487/125000000000000000",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "43920150964917487/125000000000000000",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "20169/566720",
  "q_now": "1/1",
  "e_intact": "20169/566720",
  "q_intact": "1/1",
  "eA": "20169/566720",
  "eB": "20169/566720",
  "qA": "1/1",
  "qB": "43920150964917487/125000000000000000",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "6911809/8000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "43920150964917487/125000000000000000",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "43920150964917487/125000000000000000",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-20169/566720",
  "q_now": "1/1",
  "e_intact": "-20169/566720",
  "q_intact": "1/1",
  "eA": "-20169/566720",
  "eB": "-20169/566720",
  "qA": "1/1",
  "qB": "43920150964917487/125000000000000000",
  "LA": "20169/566720",
  "LB": "20169/566720",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "901793/1000000"
}
```

#### R-CG alpha=(1,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1319901826551/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "2807629654662066927/25000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1319901826551/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "2807629654662066927/25000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3837934298548593/14168000000000000",
  "q_now": "1319901826551/8000000000000",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1319901826551/8000000000000",
  "eA": "-3837934298548593/14168000000000000",
  "eB": "-119932539345027640279971/453376000000000000000000",
  "qA": "1319901826551/8000000000000",
  "qB": "92181091799821563/500000000000000000",
  "LA": "3837934298548593/14168000000000000",
  "LB": "119932539345027640279971/453376000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4326166494701176611063/5000000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-169608912627/1000000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "155700240251272101/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-169608912627/1000000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "0/1",
  "qB": "155700240251272101/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-603069998182011/1771000000000000",
  "q_now": "169608912627/1000000000000",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "169608912627/1000000000000",
  "eA": "-603069998182011/1771000000000000",
  "eB": "-2352862942637654867859/7084000000000000000000",
  "qA": "169608912627/1000000000000",
  "qB": "193315266078204501/1000000000000000000",
  "LA": "603069998182011/1771000000000000",
  "LB": "2352862942637654867859/7084000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4358252180994924406233/5000000000000000000000"
}
```

#### R-CG alpha=(1,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3837934298548593/14168000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-3837934298548593/14168000000000000",
  "eB": "-118821150021524534516547/453376000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "2153448110025278451/8000000000000000000",
  "LA": "3837934298548593/14168000000000000",
  "LB": "118821150021524534516547/453376000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "2162810960780133151469/2500000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-603069998182011/1771000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-603069998182011/1771000000000000",
  "eB": "-2331033310302690396303/7084000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "280024627353359427/1000000000000000000",
  "LA": "603069998182011/1771000000000000",
  "LB": "2331033310302690396303/7084000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4367160263462205326233/5000000000000000000000"
}
```

#### R-CG alpha=(1,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-4143809770951/24000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-1885249/4250400",
  "q_now": "0/1",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-1885249/4250400",
  "eB": "-3837934298548593/14168000000000000",
  "qA": "0/1",
  "qB": "696525770585169777021/5000000000000000000000",
  "LA": "1885249/4250400",
  "LB": "3837934298548593/14168000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3837934298548593/14168000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-3837934298548593/14168000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-3837934298548593/14168000000000000",
  "eB": "-118821150021524534516547/453376000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "2153448110025278451/8000000000000000000",
  "LA": "3837934298548593/14168000000000000",
  "LB": "118821150021524534516547/453376000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "2162810960780133151469/2500000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-7532468559/1000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-61641/177100",
  "q_now": "0/1",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-61641/177100",
  "eB": "-603069998182011/1771000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "61641/177100",
  "LB": "603069998182011/1771000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-603069998182011/1771000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-603069998182011/1771000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-603069998182011/1771000000000000",
  "eB": "-2331033310302690396303/7084000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "280024627353359427/1000000000000000000",
  "LA": "603069998182011/1771000000000000",
  "LB": "2331033310302690396303/7084000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4367160263462205326233/5000000000000000000000"
}
```

#### R-CG alpha=(2,1) beta=0

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-18433822631448137/170016000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-18433822631448137/170016000000000000",
  "eB": "-179998082812391509833683/1700160000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "2153448110025278451/8000000000000000000",
  "LA": "18433822631448137/170016000000000000",
  "LB": "14530782921998825347026169/136012800000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "2162810960780133151469/2500000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3792350476701949/21252000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-3792350476701949/21252000000000000",
  "eB": "-18479541531636625391453/106260000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "280024627353359427/1000000000000000000",
  "LA": "3792350476701949/21252000000000000",
  "LB": "18479541531636625391453/106260000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4367160263462205326233/5000000000000000000000"
}
```

#### R-CG alpha=(2,1) beta=1/20

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-18433822631448137/170016000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-18433822631448137/170016000000000000",
  "eB": "-179998082812391509833683/1700160000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "2153448110025278451/8000000000000000000",
  "LA": "18433822631448137/170016000000000000",
  "LB": "14530782921998825347026169/136012800000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "2162810960780133151469/2500000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "0/1",
  "qB": "272855866768778601/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3792350476701949/21252000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-3792350476701949/21252000000000000",
  "eB": "-18479541531636625391453/106260000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "280024627353359427/1000000000000000000",
  "LA": "3792350476701949/21252000000000000",
  "LB": "18479541531636625391453/106260000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4367160263462205326233/5000000000000000000000"
}
```

#### R-CG alpha=(2,1) beta=1/10

Reproduction: NO. Disagreeing components: ['delta_R', 'delta_M', 'E_err_agent', 'D_e_S', 'D_e_E', 'D_q_S', 'D_q_E', 'e_A_S', 'e_B_S', 'q_A_S', 'q_B_S', 'e_A_E', 'e_B_E', 'q_A_E', 'q_B_E']. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-CORRUPT-S:

```json
{
  "D_e": "-16171731998053/96000000000000",
  "D_q": "-1719835691343/8000000000000",
  "e_now": "-392283/1416800",
  "q_now": "0/1",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-392283/1416800",
  "eB": "-18433822631448137/170016000000000000",
  "qA": "0/1",
  "qB": "1719835691343/8000000000000",
  "LA": "392283/1416800",
  "LB": "18433822631448137/170016000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4316571721/5000000000"
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-18433822631448137/170016000000000000",
  "q_now": "1719835691343/8000000000000",
  "e_intact": "-18433822631448137/170016000000000000",
  "q_intact": "1719835691343/8000000000000",
  "eA": "-18433822631448137/170016000000000000",
  "eB": "-179998082812391509833683/1700160000000000000000000",
  "qA": "1719835691343/8000000000000",
  "qB": "2317061454045550443/8000000000000000000",
  "LA": "18433822631448137/170016000000000000",
  "LB": "14530782921998825347026169/136012800000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "2162810960780133151469/2500000000000000000000"
}
```

I-SWAP-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "122199/1000000",
  "qB": "313759202773846599/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-11776684227/4000000000000",
  "D_q": "-109800322863/500000000000",
  "e_now": "-96373/531300",
  "q_now": "0/1",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-96373/531300",
  "eB": "-3792350476701949/21252000000000000",
  "qA": "0/1",
  "qB": "313759202773846599/1000000000000000000",
  "LA": "96373/531300",
  "LB": "3792350476701949/21252000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "204691/250000"
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-3792350476701949/21252000000000000",
  "q_now": "109800322863/500000000000",
  "e_intact": "-3792350476701949/21252000000000000",
  "q_intact": "109800322863/500000000000",
  "eA": "-3792350476701949/21252000000000000",
  "eB": "-18479541531636625391453/106260000000000000000000",
  "qA": "109800322863/500000000000",
  "qB": "150238147677946713/500000000000000000",
  "LA": "3792350476701949/21252000000000000",
  "LB": "18479541531636625391453/106260000000000000000000",
  "repair_equals_shadow": true,
  "reward_perturbed_trial": "4367160263462205326233/5000000000000000000000"
}
```

#### PM-ACT

Reproduction: YES. Disagreeing components: []. Unavailable: [].

I-SWAP-S:

```json
{
  "D_e": "2026132590317488558318268060771386211080574606126316450051579635551976821649243504565171659972107235299276120742311634232290507736617353261105563676714319433956056456816615678118533559967514498569815408224866690746784975176366612984667369256488017005765802189239645035203139/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "D_q": "190365289613163/4096000000000000",
  "e_now": "43312597696512/608927557773535",
  "q_now": "1/1",
  "e_intact": "1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "86854745780328465432576/1235592373844530318408055",
  "eB": "113510700540105204783910574322084688932073893530513685227366295719525331777916160073470101099445113455886699423047212631936786128453894937281767490881944259013664395529/5234571353739700405346695370993884551579892392434092490867170826677058498707558233875621118442380221136794980747694843434903357571267303823745477855544000000000000000000",
  "qA": "1/1",
  "qB": "57363643058007836360923/65536000000000000000000",
  "LA": "86854745780328465432576/1235592373844530318408055",
  "LB": "113510700540105204783910574322084688932073893530513685227366295719525331777916160073470101099445113455886699423047212631936786128453894937281767490881944259013664395529/5234571353739700405346695370993884551579892392434092490867170826677058498707558233875621118442380221136794980747694843434903357571267303823745477855544000000000000000000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-S:

```json
{
  "D_e": "2026132590317488558318268060771386211080574606126316450051579635551976821649243504565171659972107235299276120742311634232290507736617353261105563676714319433956056456816615678118533559967514498569815408224866690746784975176366612984667369256488017005765802189239645035203139/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "D_q": "190365289613163/4096000000000000",
  "e_now": "43312597696512/608927557773535",
  "q_now": "1/1",
  "e_intact": "1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "86854745780328465432576/1235592373844530318408055",
  "eB": "113510700540105204783910574322084688932073893530513685227366295719525331777916160073470101099445113455886699423047212631936786128453894937281767490881944259013664395529/5234571353739700405346695370993884551579892392434092490867170826677058498707558233875621118442380221136794980747694843434903357571267303823745477855544000000000000000000",
  "qA": "1/1",
  "qB": "57363643058007836360923/65536000000000000000000",
  "LA": "86854745780328465432576/1235592373844530318408055",
  "LB": "113510700540105204783910574322084688932073893530513685227366295719525331777916160073470101099445113455886699423047212631936786128453894937281767490881944259013664395529/5234571353739700405346695370993884551579892392434092490867170826677058498707558233875621118442380221136794980747694843434903357571267303823745477855544000000000000000000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-S:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_now": "3905634710386837/4096000000000000",
  "e_intact": "1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_intact": "3905634710386837/4096000000000000",
  "eA": "4275342525874207265365506709820652436429526336871575078316662844004045223115371803032962449052606915010822818530059174842688298309181766137292350906682514714419/163580354804365637667084230343558892236871637263565390339599088333658078084611194808613159951324381910524843148365463857340729924102103244492046182985750000000000",
  "eB": "345986881705793059910830035325908093219299322507631461809790252392006236141302832845465464006581344570204132904793605742881624429529372242906627607921664306167973/15974644023863831803426194369488173070006995826520057650351473470083796687950311993028628901496521670949691713707564829818430656650596019969926385057202148437500000",
  "qA": "3905634710386837/4096000000000000",
  "qB": "114209097767679072605819/131072000000000000000000",
  "LA": "4275342525874207265365506709820652436429526336871575078316662844004045223115371803032962449052606915010822818530059174842688298309181766137292350906682514714419/163580354804365637667084230343558892236871637263565390339599088333658078084611194808613159951324381910524843148365463857340729924102103244492046182985750000000000",
  "LB": "345986881705793059910830035325908093219299322507631461809790252392006236141302832845465464006581344570204132904793605742881624429529372242906627607921664306167973/15974644023863831803426194369488173070006995826520057650351473470083796687950311993028628901496521670949691713707564829818430656650596019969926385057202148437500000",
  "repair_equals_shadow": true
}
```

I-SWAP-E:

```json
{
  "D_e": "-1981034283548782738790401883216712373358138978587040581752377568050291367180321227293049235478742756181270265099485589901764255745225901936755012254403699841083651302610770814648193950234268351010590670785675179211311466030139603013365614879682100515441429609022500210984389/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "D_q": "-998518212217/1000000000000",
  "e_now": "-47837832294448809/682456591580714720",
  "q_now": "0/1",
  "e_intact": "-1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-406341547340120411724297/5874080463204576351873760",
  "eB": "-124745249365021524592348784002880946598394743514997391254344937455703990823612559321170815400846884531544939648248922916021994544187686447784284114637053828233/5111886087636426177096382198236215382402238664486418448112471510426814940144099837769161248478886934703901348386420745541897810128190726390376443218304687500000",
  "qA": "0/1",
  "qB": "998518212217/1000000000000",
  "LA": "406341547340120411724297/5874080463204576351873760",
  "LB": "124745249365021524592348784002880946598394743514997391254344937455703990823612559321170815400846884531544939648248922916021994544187686447784284114637053828233/5111886087636426177096382198236215382402238664486418448112471510426814940144099837769161248478886934703901348386420745541897810128190726390376443218304687500000",
  "repair_equals_shadow": true
}
```

I-CORRUPT-E:

```json
{
  "D_e": "-1981034283548782738790401883216712373358138978587040581752377568050291367180321227293049235478742756181270265099485589901764255745225901936755012254403699841083651302610770814648193950234268351010590670785675179211311466030139603013365614879682100515441429609022500210984389/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "D_q": "-998518212217/1000000000000",
  "e_now": "-47837832294448809/682456591580714720",
  "q_now": "0/1",
  "e_intact": "-1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-406341547340120411724297/5874080463204576351873760",
  "eB": "-124745249365021524592348784002880946598394743514997391254344937455703990823612559321170815400846884531544939648248922916021994544187686447784284114637053828233/5111886087636426177096382198236215382402238664486418448112471510426814940144099837769161248478886934703901348386420745541897810128190726390376443218304687500000",
  "qA": "0/1",
  "qB": "998518212217/1000000000000",
  "LA": "406341547340120411724297/5874080463204576351873760",
  "LB": "124745249365021524592348784002880946598394743514997391254344937455703990823612559321170815400846884531544939648248922916021994544187686447784284114637053828233/5111886087636426177096382198236215382402238664486418448112471510426814940144099837769161248478886934703901348386420745541897810128190726390376443218304687500000",
  "repair_equals_shadow": true
}
```

I-SUSPEND-E:

```json
{
  "D_e": "0/1",
  "D_q": "0/1",
  "e_now": "-1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_now": "998518212217/1000000000000",
  "e_intact": "-1079831694991783913360515619656855659714827916974719931805006406022250624484657396977572026985706051982880845698653467011160275334974974277429973856077718106979083911140173346324471693844267016660672369339635772872747501739666551132574499521450656702283299183544994964796861/43666446885440605327623615334839109424197223673353393787592353940633100543648843604177420296881225550997067699892517067743761457839427016316141221494010053681294630503762837063524177600686034501355907291500474069774724119166564350763677302919172808574982729748402934375000000",
  "q_intact": "998518212217/1000000000000",
  "eA": "-124745249365021524592348784002880946598394743514997391254344937455703990823612559321170815400846884531544939648248922916021994544187686447784284114637053828233/5111886087636426177096382198236215382402238664486418448112471510426814940144099837769161248478886934703901348386420745541897810128190726390376443218304687500000",
  "eB": "-345986881705793059910830035325908093219299322507631461809790252392006236141302832845465464006581344570204132904793605742881624429529372242906627607921664306167973/15974644023863831803426194369488173070006995826520057650351473470083796687950311993028628901496521670949691713707564829818430656650596019969926385057202148437500000",
  "qA": "998518212217/1000000000000",
  "qB": "249068852462102353/250000000000000000",
  "LA": "124745249365021524592348784002880946598394743514997391254344937455703990823612559321170815400846884531544939648248922916021994544187686447784284114637053828233/5111886087636426177096382198236215382402238664486418448112471510426814940144099837769161248478886934703901348386420745541897810128190726390376443218304687500000",
  "LB": "345986881705793059910830035325908093219299322507631461809790252392006236141302832845465464006581344570204132904793605742881624429529372242906627607921664306167973/15974644023863831803426194369488173070006995826520057650351473470083796687950311993028628901496521670949691713707564829818430656650596019969926385057202148437500000",
  "repair_equals_shadow": true
}
```

## Anomalies and coverage gaps

1. Freeze-run ITEM-8 raised `KeyError: 'well_defined'` after 2.044 seconds. ITEM-7 had computed the flag and stored it on the report only. Deviation D1 copies that computed flag onto the machine record and reruns ITEM-8 and ITEM-9. Original `outputs/ITEM-8.json` and `outputs/ITEM-9.json` are kept. Details are in DEVIATIONS.md.
2. At c_R = 1/50, c_S = 3/50, both T_SEP = 3 and T_SEP = 4, the S donor and the E donor are the same empty count vector. ITEM-7 reports donor_S = 0 and donor_E = 0. There is no intervention contrast. C-SEL and rescue on the reference are NOT EVALUABLE. Donors were not re-searched.
3. On every reference row, Δ_M = 0/1 exactly. C-REF therefore FAILs even where Δ_R exceeds 1/100. Decimal readings of those Δ_R values: 0 at the no-contrast settings, about 0.0239 at T_SEP = 3 with c_R = 1/100, c_S = 1/10, and about 0.0903 at T_SEP = 4 with the same costs. No agent in the four settings has C-REF = PASS. R-CG has a positive Δ_M; a decimal reading is about 0.00246 at T_SEP = 3 and about 0.00704 or 0.00886 at T_SEP = 4, all below 1/100.
4. Where the reference baseline squared error is 0/1, C-T2 is FAIL with the spec sentence "NO BASELINE ERROR TO IMPROVE; C-T2 improvement criterion not demonstrated." That is a failure of the improvement criterion, not a pass.
5. R-HAC-MB-myopic reproduction is YES in all four settings. At T_SEP = 4, c_R = 1/100, c_S = 1/10 the myopic pattern matches the reference pattern exactly on every stored component. PM-ACT reproduction is YES at that same setting and NO or UNRESOLVED elsewhere. The PM-ACT differences that remain inside the 1/1000 tolerance have decimal readings below 0.001 (the largest among the compared components is about 0.00092 on e_A_E).
6. Several controls have reproduction UNRESOLVED or NO because the intervention components are absent when there is no donor contrast. The missing names are listed in the tables. They were not imputed. R-BLIND / R-CONF-S has C-SEL and rescue NOT APPLICABLE. Its reproduction is UNRESOLVED at the no-contrast settings and NO at the contrast settings, with the same component list unavailable.
7. R-HAC-MF with eps = 1/10 is the control that has a donor contrast at T_SEP = 3, c_R = 1/50, c_S = 3/50, where the reference does not. Its C-SEL and rescue are FAIL, with a complete reproduction vector, and that vector is NO. The setting label remains UNRESOLVED-DESIGN because the reference criterion is undefined. The control's own failure is in the column, which the decision order does not reach once the reference criterion is undefined.
8. Frozen ITEM-9 replays the R-CG mixture value at T_SEP = 3. It does not replay every R-CG criterion statistic. Spec §5.4 asks for every statistic for MB and all R-CG variants at T_SEP = 3. MB pattern statistics at T_SEP = 3 were replayed and matched. R-CG criterion flags, Δ, errors and intervention statistics were not independently replayed. Switches, horizons above 4, ITEM-6, and ITEM-8 at T_SEP = 4 are tagged NOT INDEPENDENTLY REPLAYED in the value outputs or are outside the frozen replay. This coverage gap was in the freeze. It was not patched after the run.
9. ITEM-5 writes `n_R_S: null` on every row, including T = 8. `cg_forward` returns `n_R`, and the frozen writer does not store it. Bonus-disagreement counts and final state counts are stored for the T = 8, Z = S forward only. H1 rows have values and no recheck count. This is a reporting gap in the freeze, not a change made after seeing the labels.
10. ITEM-2 and ITEM-3: every `forward_value_matches_backward` entry is true. Planning advantage, adaptive-information advantage and oracle gap are nonnegative on the stored rows. Switch-aware minus certainty-equivalent gaps are nonnegative. 38 of 60 H0 switch gaps are 0/1. The switch-aware gap is descriptive. It is not a fair performance advantage.
11. ITEM-4: computed |p − 1/2| equals the spec constants s_U = 222183/468700 and s_Sp = 27/100. theta0 uses the spec constants. No anomaly was recorded.
12. ITEM-1 ratios are all distinct. The class ratios are in `outputs/ITEM-1.json`.
13. ITEM-7 reachable phase-1 belief counts are 1, 11, 66 at T_SEP = 3 and 1, 11, 66, 286 at T_SEP = 4. Primary block counts are 624, 878, 1503 and 1654 for the four PM-ACT machines. All `well_defined.ok` values are true. The second refiner agrees. State totals exceed the per-phase planning estimates (1212 and 5634) because the machine counts every phase plus the apparatus. Nothing was truncated.
14. SUSPEND on the reference, in the settings with a contrast, has D_e = 0/1 and D_q = 0/1. SWAP and CORRUPT share D_e and D_q on those rows. repair_equals_shadow is true on every stored reference intervention. Shadow equality is an integrity check. It is not rescue credit by itself.

## What this run does not say

The four setting labels are the A-SEP outcomes. They do not identify a functional role, and they do not establish acquisition. The analytic agents have supplied mechanisms. No neural network was trained. No exhaustive all-controller certificate was computed. No protected controller or register was used. No earlier study, including the work in PRs #3 through #10 and the A6 jobs, was modified or re-run.
