# RESULTS A3 D1

Additive verification record for Addendum A3 Deviation D1. Primary files at `7e153d1` are unchanged.

Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A3_D1.md`, sha256 `47fd381e1fdf98b40914b117e5bf24412316a7aba56240fcce273b78e872bd62`.

Code commit at process start: `8010eb5f1fa8d5f589861ba0ab25369677d59e39`.

The blind joint walks each regime and stores content `None`. `replay_blind` returns the deciding statistics before that joint is built, and `decide_setting` does not read the joint. The nesting correction is not a criterion change.

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This file is not an all-controller certificate. A T_SEP = 4 result cannot claim to distinguish R-HAC-MF.

## Replay agreement

### T_SEP = 3

Formal label: not issued.

| Configuration | Agreed | Failures |
| --- | --- | --- |
| R-HAC-MB | False | cfo_detail |

## PM reconstruction

- T_SEP = 3: matches stored PM.json `True`. Failures: —.

## Compute

Command, from `c4_reliability_exact_check_v1`:

```text
taskset -c 0 python3 -u -m wrel.attainability_a3_d1
```

- d1_wall_seconds_float: 0.9607954759999302
- prior_a3_wall_seconds_float: 10.273588445000314
- prior_verification_wall_seconds_float: 0.6150199170001542
- cumulative_a3_wall_seconds_float: 11.234383921000244
- cumulative_verification_wall_seconds_float: 1.5758153930000844
- peak_rss_bytes_sampled: 47198208
- process_hwm_bytes: 49102848
- Limits: verification block 20 minutes cumulative, A3 total 60 minutes cumulative, one CPU, 8 GB, no GPU.

| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |
| --- | --- | --- | --- |
| PM solve T=3 cr=1/100 cs=3/50 | 0.007570145000045159 | 27889664 | 27889664 |
| PM solve T=3 cr=1/100 cs=1/10 | 0.0074954100000468316 | 27889664 | 27889664 |
| PM solve T=3 cr=1/50 cs=3/50 | 0.007469586000297568 | 27889664 | 27889664 |
| PM solve T=3 cr=1/50 cs=1/10 | 0.007572128999981942 | 27889664 | 27889664 |
| PM solve T=3 cr=1/25 cs=3/50 | 0.0074906840000039665 | 27889664 | 27889664 |
| PM solve T=3 cr=1/25 cs=1/10 | 0.0074471030002314365 | 27889664 | 27889664 |
| PM donors T=3 | 0.006467857999723492 | 27889664 | 27889664 |
| PM machine T=3 | 0.30490443999997296 | 45957120 | 45957120 |
| replay reference T=3 | 0.5228222030000325 | 47198208 | 49102848 |

## Stop and deviation

Stop: integrity at T_SEP=3 reference replay disagrees.

No unexpected exception.

## Output hashes

- `PM-reconstruction.json`: `4c466013955913215c801c56229c43827871e0d8fdd824e23757c180c11a2258`
- `TSEP-3-replay.json`: `6e186ad1902a168b61b60ce9c8ba73ae4588249d262f6a4d572bcb5ce13ad84f`
- `TSEP-3-states.json`: `1d50611e181f82a241f4849986ef4fcc034548ef69404be0d23f3ac6f549fcc7`
- `SUMMARY.json`: `a920626d6b8fe59e3403a27a37659af4adb6db260c27fd76c27c9ced1a33ea8a`
- `HASHES.txt`: `ac322b69712ddf6fed35e5668b5446dfc351c435b946f706cc781485df436f33`

The sha256 of this file is `outputs/attainability_A3_D1/RESULTS_A3_D1.sha256`.
