# RESULTS A3 D2

Additive verification record for Addendum A3 Deviation D2. Primary files at `7e153d1` and the D1 record are unchanged.

Binding approval: `c4_reliability_APPROVAL_ADDENDUM_A3_D2.md`, sha256 `1f7158133243a2a506076bedba3a1ee5147f0004a6b772e6c92f077e6f8b82df`.

Code commit at process start: `f39baa818c2db36d9b589816a0ac6ae83815f02d`.

Gating keys are the frozen `_compare_cases` tuple plus the `_mb_replay_failures` additions, restricted to fields the stored primary emits. `cfo_detail` is not in that tuple. It is reported and does not gate. The blind joint walks each regime and stores content `None`. That nesting is not a deciding statistic.

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested. This file is not an all-controller certificate. A T_SEP = 4 result cannot claim to distinguish R-HAC-MF.

## Replay agreement

### T_SEP = 3

Formal label: `UNRESOLVED-DESIGN`.
Note: eligible control fails no evaluable core criterion while an essential comparison is unavailable: PM-ACT.
Clause: `7`.
Gating keys agreed: `True`.

| Configuration | Agreed | Gating failures |
| --- | --- | --- |
| R-HAC-MB | True | — |
Non-gating difference `cfo_detail`: Not in frozen _compare_cases or _mb_replay_failures. The stored primary is null because evaluate_mb_family does not emit cfo_detail.
| R-HAC-MB-myopic | True | — |
| R-BLIND / R-CONF-S | True | — |
| R-CONF-A eta=1/20 alpha=1/20 | True | — |
| R-CONF-A eta=1/20 alpha=1/10 | True | — |
| R-CONF-A eta=1/20 alpha=1/5 | True | — |
| R-CONF-A eta=1/10 alpha=1/20 | True | — |
| R-CONF-A eta=1/10 alpha=1/10 | True | — |
| R-CONF-A eta=1/10 alpha=1/5 | True | — |
| R-CONF-A eta=1/5 alpha=1/20 | True | — |
| R-CONF-A eta=1/5 alpha=1/10 | True | — |
| R-CONF-A eta=1/5 alpha=1/5 | True | — |
| R-CG alpha=(1,1) beta=0 | True | — |
| R-CG alpha=(1,1) beta=1/20 | True | — |
| R-CG alpha=(1,1) beta=1/10 | True | — |
| R-CG alpha=(2,1) beta=0 | True | — |
| R-CG alpha=(2,1) beta=1/20 | True | — |
| R-CG alpha=(2,1) beta=1/10 | True | — |
| R-HAC-MF eps=0 | True | — |
| R-HAC-MF eps=1/10 | True | — |
| PM-ACT | True | — |

PM-ACT donor signatures equal: `True`. Stored cells S `33`, E `35`. Replay cells S `33`, E `35`. `ill_defined_extractor`: `False`. Action mismatches: `0`. Rescue: `NOT EVALUABLE [zero-probability event]`.

### T_SEP = 4

Formal label: `UNRESOLVED-DESIGN`.
Note: eligible control fails no evaluable core criterion while an essential comparison is unavailable: PM-ACT.
Clause: `7`.
Gating keys agreed: `True`.

| Configuration | Agreed | Gating failures |
| --- | --- | --- |
| R-HAC-MB | True | — |
Non-gating difference `cfo_detail`: Not in frozen _compare_cases or _mb_replay_failures. The stored primary is null because evaluate_mb_family does not emit cfo_detail.
| R-HAC-MB-myopic | True | — |
| R-BLIND / R-CONF-S | True | — |
| R-CONF-A eta=1/20 alpha=1/20 | True | — |
| R-CONF-A eta=1/20 alpha=1/10 | True | — |
| R-CONF-A eta=1/20 alpha=1/5 | True | — |
| R-CONF-A eta=1/10 alpha=1/20 | True | — |
| R-CONF-A eta=1/10 alpha=1/10 | True | — |
| R-CONF-A eta=1/10 alpha=1/5 | True | — |
| R-CONF-A eta=1/5 alpha=1/20 | True | — |
| R-CONF-A eta=1/5 alpha=1/10 | True | — |
| R-CONF-A eta=1/5 alpha=1/5 | True | — |
| R-CG alpha=(1,1) beta=0 | True | — |
| R-CG alpha=(1,1) beta=1/20 | True | — |
| R-CG alpha=(1,1) beta=1/10 | True | — |
| R-CG alpha=(2,1) beta=0 | True | — |
| R-CG alpha=(2,1) beta=1/20 | True | — |
| R-CG alpha=(2,1) beta=1/10 | True | — |
| PM-ACT | True | — |

PM-ACT donor signatures equal: `True`. Stored cells S `321`, E `300`. Replay cells S `321`, E `300`. `ill_defined_extractor`: `False`. Action mismatches: `0`. Rescue: `NOT EVALUABLE [zero-probability event]`.

## PM reconstruction

- T_SEP = 3: matches stored PM.json `True`. Failures: —.
- T_SEP = 4: matches stored PM.json `True`. Failures: —.

## Compute

Command, from `c4_reliability_exact_check_v1`:

```text
taskset -c 0 python3 -u -m wrel.attainability_a3_d2
```

- d2_wall_seconds_float: 15.535786945999462
- prior_wall_through_d1_seconds_float: 11.234383921000244
- prior_verification_through_d1_seconds_float: 1.5758153930000844
- cumulative_a3_wall_seconds_float: 26.770170866999706
- cumulative_verification_wall_seconds_float: 17.111602338999546
- peak_rss_bytes_sampled: 180039680
- process_hwm_bytes: 239501312
- Limits: verification block 20 minutes cumulative, A3 total 60 minutes cumulative, one CPU, 8 GB, no GPU.

| Invocation | Wall seconds | Peak RSS bytes | HWM bytes |
| --- | --- | --- | --- |
| PM solve T=3 cr=1/100 cs=3/50 | 0.007973019999553799 | 28704768 | 28704768 |
| PM solve T=3 cr=1/100 cs=1/10 | 0.007745769999928598 | 28704768 | 28704768 |
| PM solve T=3 cr=1/50 cs=3/50 | 0.007597146999614779 | 28704768 | 28704768 |
| PM solve T=3 cr=1/50 cs=1/10 | 0.008337396999195335 | 28704768 | 28704768 |
| PM solve T=3 cr=1/25 cs=3/50 | 0.007416334000481584 | 28704768 | 28704768 |
| PM solve T=3 cr=1/25 cs=1/10 | 0.007605035000779026 | 28704768 | 28704768 |
| PM donors T=3 | 0.006573263000063889 | 28704768 | 28704768 |
| PM machine T=3 | 0.32209654199959914 | 46718976 | 46718976 |
| replay reference T=3 | 0.5589132599998266 | 49770496 | 50581504 |
| myopic policy reconstruct T=3 | 0.007069174999742245 | 49770496 | 50581504 |
| replay myopic T=3 | 0.043188040999666555 | 49770496 | 50581504 |
| replay blind T=3 | 0.0042221179992338875 | 49770496 | 50581504 |
| replay R-CONF-A eta=1/20 alpha=1/20 | 0.012683957999797713 | 49786880 | 50581504 |
| replay R-CONF-A eta=1/20 alpha=1/10 | 0.010590963999675296 | 49786880 | 50581504 |
| replay R-CONF-A eta=1/20 alpha=1/5 | 0.010791486000016448 | 49786880 | 50581504 |
| replay R-CONF-A eta=1/10 alpha=1/20 | 0.010673235000467685 | 49790976 | 50581504 |
| replay R-CONF-A eta=1/10 alpha=1/10 | 0.010665554999832239 | 49790976 | 50581504 |
| replay R-CONF-A eta=1/10 alpha=1/5 | 0.011142228000608156 | 49790976 | 50581504 |
| replay R-CONF-A eta=1/5 alpha=1/20 | 0.01087868000013259 | 49795072 | 50581504 |
| replay R-CONF-A eta=1/5 alpha=1/10 | 0.01067201100067905 | 49795072 | 50581504 |
| replay R-CONF-A eta=1/5 alpha=1/5 | 0.011939514000005147 | 49795072 | 50581504 |
| replay R-CG alpha=(1,1) beta=0 | 0.050978743999621656 | 49795072 | 50581504 |
| occupancy R-CG alpha=(1,1) beta=0 | 0.010087395000482502 | 49795072 | 50581504 |
| replay R-CG alpha=(1,1) beta=1/20 | 0.05102947799969115 | 50184192 | 50581504 |
| occupancy R-CG alpha=(1,1) beta=1/20 | 0.010390851000011025 | 50204672 | 50581504 |
| replay R-CG alpha=(1,1) beta=1/10 | 0.05109489099959319 | 50466816 | 50581504 |
| occupancy R-CG alpha=(1,1) beta=1/10 | 0.010839395000402874 | 50483200 | 50581504 |
| replay R-CG alpha=(2,1) beta=0 | 0.05182767599944782 | 51777536 | 51777536 |
| occupancy R-CG alpha=(2,1) beta=0 | 0.01040282399935677 | 51802112 | 51802112 |
| replay R-CG alpha=(2,1) beta=1/20 | 0.051364594000006036 | 53088256 | 53088256 |
| occupancy R-CG alpha=(2,1) beta=1/20 | 0.010346496000238403 | 53116928 | 53116928 |
| replay R-CG alpha=(2,1) beta=1/10 | 0.06806783599949995 | 54382592 | 54382592 |
| occupancy R-CG alpha=(2,1) beta=1/10 | 0.010367128999860142 | 54394880 | 54394880 |
| replay R-HAC-MF eps=0 | 0.012817335000363528 | 55615488 | 55615488 |
| finish R-HAC-MF eps=0 | 0.0251801370004614 | 55619584 | 55619584 |
| replay R-HAC-MF eps=1/10 | 0.7489874499997313 | 62697472 | 62697472 |
| finish R-HAC-MF eps=1/10 | 0.6465705059999891 | 62697472 | 62697472 |
| replay PM-ACT T=3 | 0.07416117599950667 | 105164800 | 105164800 |
| PM solve T=4 cr=1/100 cs=3/50 | 0.042959130999406625 | 67969024 | 168402944 |
| PM solve T=4 cr=1/100 cs=1/10 | 0.043760242999269394 | 67969024 | 168402944 |
| PM solve T=4 cr=1/50 cs=3/50 | 0.042673998000282154 | 67969024 | 168402944 |
| PM solve T=4 cr=1/50 cs=1/10 | 0.04249319100017601 | 67969024 | 168402944 |
| PM solve T=4 cr=1/25 cs=3/50 | 0.04247326700078702 | 67969024 | 168402944 |
| PM solve T=4 cr=1/25 cs=1/10 | 0.042164552999565785 | 67969024 | 168402944 |
| PM donors T=4 | 0.030712111999491754 | 67969024 | 168402944 |
| PM machine T=4 | 1.9366650669999217 | 131305472 | 168402944 |
| replay reference T=4 | 2.278221325999766 | 133992448 | 168402944 |
| myopic policy reconstruct T=4 | 0.03682292200028314 | 133992448 | 168402944 |
| replay myopic T=4 | 0.08773882100012997 | 133992448 | 168402944 |
| replay blind T=4 | 0.0060535980001077405 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/20 alpha=1/20 | 0.01604700400002912 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/20 alpha=1/10 | 0.015826292999918223 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/20 alpha=1/5 | 0.015694508999331447 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/10 alpha=1/20 | 0.015695918999881542 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/10 alpha=1/10 | 0.01651278499957698 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/10 alpha=1/5 | 0.07598155600044265 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/5 alpha=1/20 | 0.015896814000370796 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/5 alpha=1/10 | 0.01599209100004373 | 133992448 | 168402944 |
| replay R-CONF-A eta=1/5 alpha=1/5 | 0.019169419999343518 | 133992448 | 168402944 |
| replay R-CG alpha=(1,1) beta=0 | 0.32918791100019007 | 134037504 | 168402944 |
| occupancy R-CG alpha=(1,1) beta=0 | 0.050856562000262784 | 134049792 | 168402944 |
| replay R-CG alpha=(1,1) beta=1/20 | 0.3600389109997195 | 139374592 | 168402944 |
| occupancy R-CG alpha=(1,1) beta=1/20 | 0.0570077760003187 | 139390976 | 168402944 |
| replay R-CG alpha=(1,1) beta=1/10 | 0.3596251539993318 | 146984960 | 168402944 |
| occupancy R-CG alpha=(1,1) beta=1/10 | 0.058483728999817686 | 146989056 | 168402944 |
| replay R-CG alpha=(2,1) beta=0 | 0.34505933599939453 | 154451968 | 168402944 |
| occupancy R-CG alpha=(2,1) beta=0 | 0.05031733299983898 | 154460160 | 168402944 |
| replay R-CG alpha=(2,1) beta=1/20 | 0.347412300000542 | 162131968 | 168402944 |
| occupancy R-CG alpha=(2,1) beta=1/20 | 0.050012728000183415 | 162144256 | 168402944 |
| replay R-CG alpha=(2,1) beta=1/10 | 0.34218430199962313 | 169586688 | 169586688 |
| occupancy R-CG alpha=(2,1) beta=1/10 | 0.049949007000577694 | 169586688 | 169586688 |
| replay PM-ACT T=4 | 0.3466732630004117 | 177598464 | 177598464 |

## Stop and deviation

No approved stop fired.

No unexpected exception.

## Output hashes

- `PM-reconstruction.json`: `2d38e3263d7f5a98178d1115e112a2cd8d0b0748f86a532a465357739d16f4d7`
- `TSEP-3-replay.json`: `64726f07f286cab922b6a4b3a5e6b7c52b4dba3d498f492783119dcc83adb051`
- `TSEP-3-states.json`: `8eebd82ae9f394274c8603c2fe1be9aa9c38844abeaec9896babe746482be076`
- `TSEP-4-replay.json`: `51ce21db16b06cc8efeb79f92719420a294abadfe68ce69dd8ee34588ccad2b2`
- `TSEP-4-states.json`: `a9ebfc8b23c17f5daebaaaca4be334b502f1ecdaf0e73de8bcd8a5807113158c`
- `SUMMARY.json`: `24a10150cc6dea8c85593512c8cbda1b31833fc3d5bb5957807cbc3baf4d9154`
- `HASHES.txt`: `02047d4ebebeb4f5971106a6db3606e82d832bea98a19d2016c0cc29ed681e96`

The sha256 of this file is `outputs/attainability_A3_D2/RESULTS_A3_D2.sha256`.
