# RESULTS A3

Exploratory W-REL named-control comparison under Addendum A3. Earlier results are unchanged. This file is additive.

Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A3.md`, sha256 `6efeef0d2ae0123e95939f63d06a803d9cde642997ce735a6b0eb28aa2ea9a2c`, recorded 2026-10-21, 2:45 PM ET. The frozen procedure is `c4_reliability_exact_check_spec_ADDENDUM_A3.md`.

Code commit at process start: `cc68e467f9cf6c9f3c4673e3609b0c4f19f910c3`.

The eligible roster is supplied explicitly at `(c_R, c_S) = (1/100, 3/50)` because that pair is not in frozen `KSEP`. The supply follows spec FINAL section 4.1 and `item8` append order. It is not a criterion change. `KSEP` is unchanged.

PM-ACT is built with `n_costs=6`. The other five descriptive costs are the frozen input alphabet. No A-SEP criterion is evaluated at those costs. Descriptive `PM_k` is not built. R-CONF-ENUM is not evaluated.

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This file is not an all-controller certificate. A T_SEP = 4 result cannot claim to distinguish R-HAC-MF.

## Smoke test

- Backward value: `4422831721/5000000000`
- Forward mixture: `4422831721/5000000000`
- Stored ITEM-2 `V_star`: `4422831721/5000000000`
- Mismatches: none
- Integrity: AGREE
- Stage wall: 0.008241238000209705 seconds
- Stage sampled peak RSS: 25505792 bytes
- Process high-water mark at stage end: 25505792 bytes

## PM-ACT closure

### T_SEP = 3

- Input domain: six descriptive costs. Study cost index `0`. A-SEP criteria were not run on the other five.
- Donor S index `10`, counts `[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]`.
- Donor E index `4`, counts `[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]`.
- States: `21622`. Controller total `12559`. Apparatus total `9063`.
- Primary blocks: 878. Queue-refiner blocks: 878.
- Partition equality: `True`.
- `well_defined.ok`: `True`. Capped bad-symbol count: 0.
- Reachable phase-1 controller beliefs by trial: `{'0': 1, '1': 11, '2': 66}`.
- `PM_k` built: `False`.

### T_SEP = 4

- Input domain: six descriptive costs. Study cost index `0`. A-SEP criteria were not run on the other five.
- Donor S index `65`, counts `[2, 0, 0, 0, 0, 0, 0, 0, 0, 0]`.
- Donor E index `4`, counts `[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]`.
- States: `114693`. Controller total `58605`. Apparatus total `56088`.
- Primary blocks: 1732. Queue-refiner blocks: 1732.
- Partition equality: `True`.
- `well_defined.ok`: `True`. Capped bad-symbol count: 0.
- Reachable phase-1 controller beliefs by trial: `{'0': 1, '1': 11, '2': 66, '3': 286}`.
- `PM_k` built: `False`.

## Settings

### T_SEP = 3

Reference conjunction: `ATTAINED`. `reference_met`: `True`.

| Criterion | Reference |
| --- | --- |
| C-REF | PASS |
| C-T2 | PASS |
| C-SEL | PASS |
| C-FO | PASS |
| rescue | PASS |

Reference integrity against stored A2: `AGREE`.

Formal label: not issued.

Label before the replay gate: `UNRESOLVED-DESIGN` (eligible control fails no evaluable core criterion while an essential comparison is unavailable: PM-ACT).

Status: `PRIMARY-ONLY`. `pm_undefined`: `False`.

| Control | Reproduction | Conjunction | Separating core criteria | Pattern keys outside ρ_REP |
| --- | --- | --- | --- | --- |
| R-HAC-MB-myopic | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_B_E |
| R-BLIND / R-CONF-S | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/20 alpha=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/20 alpha=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/20 alpha=1/5 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/10 alpha=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/10 alpha=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/10 alpha=1/5 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/5 alpha=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/5 alpha=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/5 alpha=1/5 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CG alpha=(1,1) beta=0 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, E_err_agent |
| R-CG alpha=(1,1) beta=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, E_err_agent |
| R-CG alpha=(1,1) beta=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, E_err_agent |
| R-CG alpha=(2,1) beta=0 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, E_err_agent |
| R-CG alpha=(2,1) beta=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, E_err_agent |
| R-CG alpha=(2,1) beta=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, E_err_agent |
| R-HAC-MF eps=0 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, E_err_agent |
| R-HAC-MF eps=1/10 | NO | FAILS | C-REF, C-T2, C-SEL, rescue | delta_R, delta_M, E_err_agent, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |
| PM-ACT | NO | UNRESOLVED | — | e_A_S |

Independent replay: not run.

### T_SEP = 4

Reference conjunction: `ATTAINED`. `reference_met`: `True`.

| Criterion | Reference |
| --- | --- |
| C-REF | PASS |
| C-T2 | PASS |
| C-SEL | PASS |
| C-FO | PASS |
| rescue | PASS |

Reference integrity against stored A2: `AGREE`.

Formal label: not issued.

Label before the replay gate: `UNRESOLVED-DESIGN` (eligible control fails no evaluable core criterion while an essential comparison is unavailable: PM-ACT).

Status: `PRIMARY-ONLY`. `pm_undefined`: `False`.

R-HAC-MF is not eligible at T_SEP = 4. This result cannot claim to distinguish MF.

| Control | Reproduction | Conjunction | Separating core criteria | Pattern keys outside ρ_REP |
| --- | --- | --- | --- | --- |
| R-HAC-MB-myopic | NO | FAILS | C-REF, C-T2 | delta_R, delta_M, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_B_E |
| R-BLIND / R-CONF-S | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/20 alpha=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/20 alpha=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/20 alpha=1/5 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/10 alpha=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/10 alpha=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/10 alpha=1/5 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/5 alpha=1/20 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/5 alpha=1/10 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CONF-A eta=1/5 alpha=1/5 | NO | FAILS | C-REF, C-T2 | delta_R, delta_M |
| R-CG alpha=(1,1) beta=0 | NO | FAILS | C-REF, C-T2, C-SEL, rescue | delta_R, delta_M, E_err_agent, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |
| R-CG alpha=(1,1) beta=1/20 | NO | FAILS | C-REF, C-T2, C-SEL, rescue | delta_R, delta_M, E_err_agent, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |
| R-CG alpha=(1,1) beta=1/10 | NO | FAILS | C-REF, C-T2, C-SEL, rescue | delta_R, delta_M, E_err_agent, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |
| R-CG alpha=(2,1) beta=0 | NO | FAILS | C-REF, C-T2, C-SEL, rescue | delta_R, delta_M, E_err_agent, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |
| R-CG alpha=(2,1) beta=1/20 | NO | FAILS | C-REF, C-T2, C-SEL, rescue | delta_R, delta_M, E_err_agent, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |
| R-CG alpha=(2,1) beta=1/10 | NO | FAILS | C-REF, C-T2, C-SEL, rescue | delta_R, delta_M, E_err_agent, D_e_S, D_e_E, D_q_S, D_q_E, e_A_S, e_B_S, q_A_S, q_B_S, e_A_E, e_B_E, q_A_E, q_B_E |
| PM-ACT | UNRESOLVED | UNRESOLVED | — | — |

Independent replay: not run.

## Compute

Command, from `c4_reliability_exact_check_v1`:

```text
taskset -c 0 python3 -u -m wrel.attainability_a3
```

- Cumulative wall: 10.273588445000314 seconds
- Sampled peak RSS: 144244736 bytes
- Process high-water mark: 153063424 bytes
- Limits: one CPU process, 60 cumulative minutes, 20 minutes inside each named block, 8 GB resident memory, no GPU.
- Smoke-test stage limit: 60 seconds. Invocations used: 1.

### Block `manifest`

- Wall: 0.004557453999950667 seconds
- Sampled peak RSS: 25505792 bytes
- Process high-water mark: 25505792 bytes

| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |
| --- | --- | --- | --- |

### Block `smoke`

- Wall: 0.008572525000090536 seconds
- Sampled peak RSS: 25505792 bytes
- Process high-water mark: 25505792 bytes

| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |
| --- | --- | --- | --- |
| smoke T=1 | 0.004427333999956318 | 25505792 | 25505792 |

### Block `PM construction`

- Wall: 2.9893764309999824 seconds
- Sampled peak RSS: 141180928 bytes
- Process high-water mark: 153063424 bytes

| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |
| --- | --- | --- | --- |
| PM solve T=3 cr=1/100 cs=3/50 | 0.007480142000076739 | 25505792 | 25505792 |
| PM solve T=3 cr=1/100 cs=1/10 | 0.0075158319996262435 | 25505792 | 25505792 |
| PM solve T=3 cr=1/50 cs=3/50 | 0.00783599599981244 | 25505792 | 25505792 |
| PM solve T=3 cr=1/50 cs=1/10 | 0.007514072000049055 | 25505792 | 25505792 |
| PM solve T=3 cr=1/25 cs=3/50 | 0.007156227999985276 | 25505792 | 25505792 |
| PM solve T=3 cr=1/25 cs=1/10 | 0.007279061999724945 | 25505792 | 25505792 |
| PM donors T=3 | 0.006466239000019414 | 25505792 | 25505792 |
| PM machine T=3 | 0.3104455909997341 | 43147264 | 43147264 |
| PM solve T=4 cr=1/100 cs=3/50 | 0.043843378000019584 | 45223936 | 47316992 |
| PM solve T=4 cr=1/100 cs=1/10 | 0.04251308200036874 | 45223936 | 47316992 |
| PM solve T=4 cr=1/50 cs=3/50 | 0.04236053400018136 | 45223936 | 47316992 |
| PM solve T=4 cr=1/50 cs=1/10 | 0.04199692500014862 | 45223936 | 47316992 |
| PM solve T=4 cr=1/25 cs=3/50 | 0.04165913699989687 | 45223936 | 47316992 |
| PM solve T=4 cr=1/25 cs=1/10 | 0.04116039800010185 | 45223936 | 47316992 |
| PM donors T=4 | 0.02989581099973293 | 45223936 | 47316992 |
| PM machine T=4 | 2.1001364570001897 | 141180928 | 142114816 |

### Block `T_SEP=3 evaluation`

- Wall: 2.391680105999967 seconds
- Sampled peak RSS: 144224256 bytes
- Process high-water mark: 153063424 bytes

| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |
| --- | --- | --- | --- |
| reference T=3 | 0.5006364890000441 | 143863808 | 153063424 |
| myopic solve T=3 | 0.00707527900021887 | 143872000 | 153063424 |
| myopic criteria T=3 | 0.03672544099981678 | 143872000 | 153063424 |
| blind T=3 | 0.003980176999903051 | 143872000 | 153063424 |
| R-CONF-A eta=1/20 alpha=1/20 | 0.011710357999618282 | 143872000 | 153063424 |
| R-CONF-A eta=1/20 alpha=1/10 | 0.009857969999757188 | 143872000 | 153063424 |
| R-CONF-A eta=1/20 alpha=1/5 | 0.00977635100025509 | 143872000 | 153063424 |
| R-CONF-A eta=1/10 alpha=1/20 | 0.00984053699994547 | 143872000 | 153063424 |
| R-CONF-A eta=1/10 alpha=1/10 | 0.009869692999927793 | 143872000 | 153063424 |
| R-CONF-A eta=1/10 alpha=1/5 | 0.009780859000329656 | 143872000 | 153063424 |
| R-CONF-A eta=1/5 alpha=1/20 | 0.009898356000121566 | 143872000 | 153063424 |
| R-CONF-A eta=1/5 alpha=1/10 | 0.01198768199992628 | 143872000 | 153063424 |
| R-CONF-A eta=1/5 alpha=1/5 | 0.010726304999934655 | 143872000 | 153063424 |
| R-CG alpha=(1,1) beta=0 | 0.03950253999983033 | 143872000 | 153063424 |
| R-CG alpha=(1,1) beta=1/20 | 0.03961559199979092 | 143872000 | 153063424 |
| R-CG alpha=(1,1) beta=1/10 | 0.039482981999753974 | 143872000 | 153063424 |
| R-CG alpha=(2,1) beta=0 | 0.03988708499991844 | 143872000 | 153063424 |
| R-CG alpha=(2,1) beta=1/20 | 0.03977923100001135 | 143872000 | 153063424 |
| R-CG alpha=(2,1) beta=1/10 | 0.04040385000007518 | 143872000 | 153063424 |
| R-HAC-MF eps=0 | 0.03508293700042486 | 143872000 | 153063424 |
| R-HAC-MF eps=1/10 | 1.3713443030001145 | 144211968 | 153063424 |
| PM-ACT criteria T=3 | 0.0796243479999248 | 144224256 | 153063424 |

### Block `T_SEP=4 evaluation`

- Wall: 4.254180898999948 seconds
- Sampled peak RSS: 144236544 bytes
- Process high-water mark: 153063424 bytes

| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |
| --- | --- | --- | --- |
| reference T=4 | 1.9837126170000374 | 144236544 | 153063424 |
| myopic solve T=4 | 0.036958987999696546 | 144236544 | 153063424 |
| myopic criteria T=4 | 0.0395965999996406 | 144236544 | 153063424 |
| blind T=4 | 0.00564498999983698 | 144236544 | 153063424 |
| R-CONF-A eta=1/20 alpha=1/20 | 0.013689416000033816 | 144236544 | 153063424 |
| R-CONF-A eta=1/20 alpha=1/10 | 0.013648429000113538 | 144236544 | 153063424 |
| R-CONF-A eta=1/20 alpha=1/5 | 0.013697252000383742 | 144236544 | 153063424 |
| R-CONF-A eta=1/10 alpha=1/20 | 0.013748727000347571 | 144236544 | 153063424 |
| R-CONF-A eta=1/10 alpha=1/10 | 0.01379141500001424 | 144236544 | 153063424 |
| R-CONF-A eta=1/10 alpha=1/5 | 0.01377141400007531 | 144236544 | 153063424 |
| R-CONF-A eta=1/5 alpha=1/20 | 0.014086572999985947 | 144236544 | 153063424 |
| R-CONF-A eta=1/5 alpha=1/10 | 0.013956469999811816 | 144236544 | 153063424 |
| R-CONF-A eta=1/5 alpha=1/5 | 0.016338310000264755 | 144236544 | 153063424 |
| R-CG alpha=(1,1) beta=0 | 0.24776428099994519 | 144236544 | 153063424 |
| R-CG alpha=(1,1) beta=1/20 | 0.2708166729998993 | 144236544 | 153063424 |
| R-CG alpha=(1,1) beta=1/10 | 0.2709791130000667 | 144236544 | 153063424 |
| R-CG alpha=(2,1) beta=0 | 0.2601853510000183 | 144236544 | 153063424 |
| R-CG alpha=(2,1) beta=1/20 | 0.262695777999852 | 144236544 | 153063424 |
| R-CG alpha=(2,1) beta=1/10 | 0.2622697510000762 | 144236544 | 153063424 |
| PM-ACT criteria T=4 | 0.34644784800002526 | 144236544 | 153063424 |

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

Deviation: ValueError: not enough values to unpack (expected 2, got 1)

```text
Traceback (most recent call last):
  File "/workspace/c4_reliability_exact_check_v1/wrel/attainability_a3.py", line 2596, in run
    _verify_horizon(world, horizon, held[horizon], setting, theta0, clock)
  File "/workspace/c4_reliability_exact_check_v1/wrel/attainability_a3.py", line 2310, in _verify_horizon
    bjoint = _mb_snaps_as_joint(bsnaps)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspace/c4_reliability_exact_check_v1/wrel/attainability_a3.py", line 791, in _mb_snaps_as_joint
    return [[(None, i, p) for i, p in layer] for layer in snaps]
                              ^^^^
ValueError: not enough values to unpack (expected 2, got 1)
```

## Output hashes

- `outputs/attainability_A3/smoke.json`: `271594c533cf694bac249d9b83480f131139ee30a771a9379f149ec3ea3c1cad`
- `outputs/attainability_A3/PM.json`: `cb4966dc72107c8c88b854f348a0445a0d2561fcda8a73e06106743ce6a04d39`
- `outputs/attainability_A3/TSEP-3.json`: `6fdb833c13fad16dca7cb6c53dad2a73ad0744bad0008d6f741534841a741eb0`
- `outputs/attainability_A3/TSEP-4.json`: `f8d65a4e910c2a45592526d7b70d1c9a8238286115d2b2174433f853e412f8c6`
- `outputs/attainability_A3/SUMMARY.json`: `4f66c7f286646c844a2b8ac4cac006d7d827244124be71f5612abacf4b67a000`
- `outputs/attainability_A3/HASHES.txt`: `43fa30a7a3d9595540020346688efdb5bc599fbbeed4b671c9e341b1190bef1a`

The sha256 of this file is `outputs/attainability_A3/RESULTS_A3.sha256`. It is computed after this file is written.
