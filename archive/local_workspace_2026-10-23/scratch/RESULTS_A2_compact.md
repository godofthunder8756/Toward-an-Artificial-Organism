# RESULTS A2

Exploratory W-REL reference-attainability check under Addendum A2. Earlier results are unchanged. This file is additive.

Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A2.md`, sha256 `09c336d4569ec6771c88d97bee424510fab0cd6b5403b24accee1f813fb8b835`, recorded 2026-10-21, 12:19 PM ET. The frozen procedure is `c4_reliability_exact_check_spec_ADDENDUM_A2.md`.

Code commit at process start: `8a4b3937a58ae984ec868dec7eba65a1c1aca72f`.

Only R-HAC-MB under H0 at `(c_R, c_S) = (1/100, 3/50)` is evaluated, at `T_SEP = 3` and `T_SEP = 4`. The formal label is the return value of frozen `decide_setting`, called with this reference, an empty control list, and `pm_undefined` false. Eligible named controls and PM-ACT are outside this approval and were not evaluated. This file does not add a label.

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested.

## Smoke test

One invocation: frozen `H0Solver` at T = 1, non-myopic, then `forward` under both regimes.

- Backward value: `~0.884566`
- Forward mixture: `~0.884566`
- Stored ITEM-2 `V_star`: `~0.884566`
- Mismatches: none
- Integrity: AGREE
- Stage wall: 0.007656676999999945 seconds
- Stage sampled peak RSS: 24924160 bytes
- Process high-water mark at stage end: 24928256 bytes

## Settings

### T_SEP = 3

Formal label: **UNRESOLVED-DESIGN**.

Note: no decision-order clause applied

Reference conjunction (`conjunction_of`): `ATTAINED`. `reference_met`: `True`.

| Criterion | Value |
| --- | --- |
| C-REF | PASS |
| C-T2 | PASS |
| C-SEL | PASS |
| C-FO | PASS |
| rescue | PASS |

Status: `COMPLETE`. Replay and primary agreement: `True`.

#### Deciding statistics

- Δ_R = `~0.370751`
- Δ_M = `~0.370751`
- E_err(agent) = `0/1`
- E_err(baseline) = `~9.65315e-05`
- C-T2 improvement = `1/1`
- C-T2 note = `None`
- D_e SWAP-S = `~0.0399016`; D_q SWAP-S = `~0.362736`
- D_e SWAP-E = `~-0.0338522`; D_q SWAP-E = `-45527/50000`
- C-FO (a) equal = `True`; C-FO (b) equal = `True`
- donor contrast = `True`
- S-donor counts = `[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
- E-donor counts = `[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]`
- empty-belief value = `~2.65676`

#### Intervention, suspension-control, and rescue components

| Direction | Mode | D_e | D_q | eA | eB | qA | qB | LA | LB | repair equals shadow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | SWAP | ~0.0399016 | ~0.362736 | ~0.0674528 | ~0.0247249 | 1/1 | ~0.119351 | ~0.0674528 | ~0.0247249 | True |
| S | CORRUPT | ~0.0399016 | ~0.362736 | ~0.0693631 | ~0.0247249 | 1/1 | ~0.119351 | ~0.0693631 | ~0.0247249 | True |
| S | SUSPEND | 0/1 | 0/1 | ~0.0294615 | ~0.0254421 | ~0.0934061 | ~0.114837 | ~0.0294615 | ~0.0254421 | True |
| E | SWAP | ~-0.0338522 | -45527/50000 | ~-0.0633137 | ~-0.0294615 | 0/1 | 22491/62500 | ~0.0633137 | ~0.0294615 | True |
| E | CORRUPT | ~-0.0338522 | -45527/50000 | ~-0.0633137 | ~-0.0294615 | 0/1 | 22491/62500 | ~0.0633137 | ~0.0294615 | True |
| E | SUSPEND | 0/1 | 0/1 | ~-0.0294615 | ~-0.0254421 | 22491/62500 | ~0.53938 | ~0.0294615 | ~0.0254421 | True |

#### Replay agreement

- Statistic differences: none
- Action rows compared equal: 432
- Action disagreements: 0
- Keys only in the primary table: 0
- Keys only in the replay table: 0
- Primary action-table sha256: `4f388d56e83328829818932f5699fe785469ed037f41a65cdc00ea1f697210eb`
- Replay action-table sha256: `4f388d56e83328829818932f5699fe785469ed037f41a65cdc00ea1f697210eb`
- Policy entries: 624

The per-state action tables are stored in `outputs/attainability_A2/TSEP-3.json`.

- Stage wall: 1.0429594779999434 seconds
- Stage sampled peak RSS: 24940544 bytes
- Process high-water mark at stage end: 25309184 bytes

### T_SEP = 4

Formal label: **UNRESOLVED-DESIGN**.

Note: no decision-order clause applied

Reference conjunction (`conjunction_of`): `ATTAINED`. `reference_met`: `True`.

| Criterion | Value |
| --- | --- |
| C-REF | PASS |
| C-T2 | PASS |
| C-SEL | PASS |
| C-FO | PASS |
| rescue | PASS |

Status: `COMPLETE`. Replay and primary agreement: `True`.

#### Deciding statistics

- Δ_R = `~0.65084`
- Δ_M = `~0.65084`
- E_err(agent) = `0/1`
- E_err(baseline) = `~0.000129347`
- C-T2 improvement = `1/1`
- C-T2 note = `None`
- D_e SWAP-S = `~0.0456872`; D_q SWAP-S = `~0.58691`
- D_e SWAP-E = `~-0.0378716`; D_q SWAP-E = `~-0.845573`
- C-FO (a) equal = `True`; C-FO (b) equal = `True`
- donor contrast = `True`
- S-donor counts = `[2, 0, 0, 0, 0, 0, 0, 0, 0, 0]`
- E-donor counts = `[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]`
- empty-belief value = `~3.54518`

#### Intervention, suspension-control, and rescue components

| Direction | Mode | D_e | D_q | eA | eB | qA | qB | LA | LB | repair equals shadow |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S | SWAP | ~0.0456872 | ~0.58691 | ~0.0710708 | ~0.0215587 | 1/1 | ~0.119085 | ~0.0710708 | ~0.0215587 | True |
| S | CORRUPT | ~0.0456872 | ~0.58691 | ~0.0711293 | ~0.0215587 | 1/1 | ~0.119085 | ~0.0711293 | ~0.0215587 | True |
| S | SUSPEND | 0/1 | 0/1 | ~0.0254421 | ~0.0227877 | ~0.114837 | ~0.109818 | ~0.0254421 | ~0.0227877 | True |
| E | SWAP | ~-0.0378716 | ~-0.845573 | ~-0.0633137 | ~-0.0254421 | 0/1 | ~0.53938 | ~0.0633137 | ~0.0254421 | True |
| E | CORRUPT | ~-0.0378716 | ~-0.845573 | ~-0.0633137 | ~-0.0254421 | 0/1 | ~0.53938 | ~0.0633137 | ~0.0254421 | True |
| E | SUSPEND | 0/1 | 0/1 | ~-0.0254421 | ~-0.0227877 | ~0.53938 | ~0.629055 | ~0.0254421 | ~0.0227877 | True |

#### Replay agreement

- Statistic differences: none
- Action rows compared equal: 1552
- Action disagreements: 0
- Keys only in the primary table: 0
- Keys only in the replay table: 0
- Primary action-table sha256: `d76c8c390244e3b4a04b1324613a759a32599e99ff3413f9e4a439ed4b225ba8`
- Replay action-table sha256: `d76c8c390244e3b4a04b1324613a759a32599e99ff3413f9e4a439ed4b225ba8`
- Policy entries: 2912

The per-state action tables are stored in `outputs/attainability_A2/TSEP-4.json`.

- Stage wall: 4.06838010499996 seconds
- Stage sampled peak RSS: 26947584 bytes
- Process high-water mark at stage end: 28516352 bytes

## Compute

Command, from `c4_reliability_exact_check_v1`:

```text
taskset -c 0 python3 -u -m wrel.attainability_a2
```

- Cumulative wall: 5.169838951000088 seconds
- Sampled peak RSS: 26947584 bytes
- Process high-water mark: 28516352 bytes
- Limits: one CPU process, 30 cumulative minutes, 8 GB resident memory, no GPU.
- Smoke-test stage limit: 60 seconds. Invocations used: 1.

Thresholds read from the frozen `wrel/sep.py` constants:

- μ_REF = `1/100`
- μ_T2 = `1/2`
- μ_SEL,a = `1/100`
- μ_SEL,c = `1/100`
- μ_RES,a = `1/100`
- μ_RES,c = `1/100`
- μ_RES,L = `1/100`
- ρ_REP = `1/1000`

## Stop and deviation

The batch finished inside the approved limits. No approved stop fired.

Deviation: none.

