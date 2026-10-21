# RESULTS v3

Addendum A1 verification completion for the W-REL bounded exact check. `RESULTS_v1.md` and `RESULTS_v2.md` are unchanged. Original outputs are unchanged. This file records `outputs/verification_A1/RESULT.json`.

No ledger file is edited. No change to the C4 evidence or status row, and no consciousness conclusion.

## Missing coverage

The missing spec §5.4 ITEM-8 replay **AGREES**.

Coverage recomputed here, at `T_SEP = 3` and both `K_SEP` cost pairs:

- the reference, including every intervention and rescue statistic and the C-FO check;
- a reference policy built in this process (`solve_reference`), with no stored policy object loaded;
- all six R-CG variants, including every intervention and rescue statistic.

Comparison is exact rational equality against `outputs/deviation_1/ITEM-8.json`, against ITEM-2 `V_star` for the reconstructed reference value, and against ITEM-5 `V_S` and `V_E` for each R-CG variant. Mismatches: 0. Integrity: **AGREE**. Status: **COMPLETE**.

Reference C-FO compared default probabilities and binary decisions across the beliefs supplied to that check. Both components were equal: 4 beliefs at costs (1/50, 3/50), and 20 beliefs at costs (1/100, 1/10). The reconstructed policy has 624 entries at each cost pair. Its value equals ITEM-2 `V_star` at both pairs (`13268495163/5000000000` and `173582937170561189335173/65536000000000000000000`). Decision invariance held.

R-CG rows: 12 (6 variants × 2 cost pairs). Each row's flags, pattern, donors, contrast bit, T2 note, and intervention record, including rescue components, matched the emitted primary. At `T_SEP = 3`, every R-CG variant has `donor_contrast` false at both cost pairs, matching the primary.

Spec §5.4 leaves ITEM-8 at `T_SEP = 4`, and ITEM-8 for R-HAC-MF, R-CONF-A, R-BLIND / R-CONF-S, MB-myopic, and PM-ACT, outside this replay. Those quantities were not recomputed.

## Formal A-SEP certification

Under the frozen gate (spec §5.1 and §6), ITEM-7 and ITEM-8 are complete and ITEM-9 now agrees on every replayed quantity in the §5.4 table, including the ITEM-8 block this completion filled. The incomplete-coverage **UNRESOLVED-COMPUTE** recorded in `RESULTS_v2.md` is lifted.

The formal certification is the per-setting label the frozen decision order already emitted:

| T | Costs | Formal A-SEP label |
| --- | --- | --- |
| 3 | (1/50, 3/50) | UNRESOLVED-DESIGN |
| 4 | (1/50, 3/50) | UNRESOLVED-DESIGN |
| 3 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET |
| 4 | (1/100, 1/10) | REFERENCE CRITERIA NOT MET |

Verbatim notes, from `outputs/deviation_1/ITEM-9.json`:

- UNRESOLVED-DESIGN: "an output, intervention correspondence or criterion is undefined." Reason recorded there: reference criterion undefined for C-SEL and rescue.
- REFERENCE CRITERIA NOT MET: "the reference does not meet the required conjunction."

At (1/50, 3/50) the reference has no donor contrast, and C-REF and C-T2 fail. At (1/100, 1/10) and T = 3, C-REF and C-SEL fail. At (1/100, 1/10) and T = 4, C-REF fails. These reasons are the ones already emitted. This completion does not change a label rule and does not reissue the decision order.

## Compute

One CPU (`taskset -c 0`). Command, from `c4_reliability_exact_check_v1`, locked in `VERIFICATION_A1_MANIFEST.md` before the run:

```text
taskset -c 0 python3 -u -m wrel.verification_a1
```

The process finished inside the Addendum A1 budget. No retry. Nothing required by the approval was left uncomputed.

| Clock | Value |
| --- | --- |
| Wall time | 1.292586913001287 seconds |
| Peak RSS sampled | 17784832 bytes |
| Process high-water mark | 17784832 bytes |

Limits were 30 cumulative minutes and 8 GB. Both clocks are the values in `outputs/verification_A1/RESULT.json`.

## Commits

| Commit | Role |
| --- | --- |
| `aeb9382bb7c0102249e947de849e715319abf2e7` | Freeze |
| `5a3d85bdeb47026e13c3b5ffbe6ee134ad377fa9` | Documentation errata |
| `3d70812e30a44d003615640942223e731c4135d5` | Addendum A1 approval |
| `99d9d0ff8a826eef8c5a39f58d41da0c391e5cf1` | Advisory-run timing correction |
| `db69242b03d2c305d53b58e3e945f1070b8046f0` | Verification code and manifest, committed before the run |

The commit that adds `outputs/verification_A1/RESULT.json` and this file is recorded on the pull request. It is not written into this file.

Locked code SHA256 of `wrel/verification_a1.py`: `f8deb34b82d7695a2a3bbf283135839c5e595d0855f1465e29eec175c95169dc`.
