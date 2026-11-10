# RWM pre-scale verification gate: results (ENGINEERING)

Protocol RWM-PSG v1. Verdict: **NO_GO**. Failed: T6_integration, T7_core_complex.

A verdict here authorizes no training. See RWM_DESIGN_v1.md sections 8 to 10.

## Gate tests on RWM-8

| Test | Pass |
| --- | --- |
| T1_single_scc | yes |
| T2_bottleneck | yes |
| T3_broadcast | yes |
| T4_monitor_higher_order | yes |
| T5_no_vestigial_declared_edges | yes |
| T6_integration | NO |
| T7_core_complex | NO |
| T8_instruments | yes |
| T9_objective_admission | yes |

## Designs and matched rivals

| Design | bits | T1 SCC | T2 bottleneck | T3 broadcast | T4 monitor | Phi_s>0 mass | core-complex mass | monitor-only complex mass | CD interv. (w) | CD closed loop (w) | mean lifetime |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RWM-8 | 8 | yes | yes | yes | yes | 0.0000 | 0.0000 | 0.7765 | 0.1473 | 0.0511 | 13.53 |
| RWM-8-v0 | 8 | yes | yes | yes | yes | 0.0000 | 0.0000 | 0.0000 | 0.1250 | 0.0055 | 7.63 |
| RV-DETACHED-MONITOR | 8 | no | yes | yes | no | 0.0000 | 0.0000 | 1.0000 | 0.1473 | 0.0214 | 5.00 |
| RV-FO-CONFIDENCE | 7 | yes | yes | yes | yes | 0.0000 | 0.0000 | 0.0000 | 0.1488 | 0.0115 | 7.63 |
| RV-SSB | 7 | yes | yes | yes | yes | 0.0000 | 0.0000 | 0.5934 | 0.1726 | 0.0688 | 15.39 |
| RV-DIRECT | 6 | yes | no | no | yes | 0.0042 | 0.0000 | 0.6492 | 0.2083 | 0.1180 | 21.96 |

## Why RWM-8 fails T6/T7

Stationary mass by Phi_s outcome and the cut side A of the minimum-information partition:

| Outcome | mass |
| --- | --- |
| zero at MIP @ ['A'] | 0.7778 |
| zero at MIP @ ['G'] | 0.0972 |
| no cause under clamped background (IIT convention) @ - | 0.0641 |
| zero at MIP @ ['I'] | 0.0610 |

Workspace/first-order edges with zero closed-loop CMI: G->K, I->G, I->K, K->I, K->X, X->K.

## Instrument validation

- copy_loop_phi: 1.0000
- copy_loop_cd: 1.0000
- dag_chain_max_phi: 0.0000
- two_islands_max_phi: 0.0000
- fooler_xor_ring_phi_state0: 0.5000
- fooler_xor_ring_cd: 0.2857
- fooler_noisy_ring_phi_state0: 0.0586
- unrolled_nodes: 24
- unrolled_io_equivalent: True
- unrolled_single_scc: False
- unrolled_phi_zero_structurally: True
- T8_instruments: True

## Objective admission (exact rationals, all 2^10 memoryless policies)

| Objective | optimal discounted cost | expected lifetime of every optimal policy |
| --- | --- | --- |
| extero_only | 0 | 5 |
| extero_plus_intero | 154049895/11230061 | 109/3 |
| intero_only | 3343923/558689 | 51 |

Dark-room lifetime 5; best lifetime over all policies 51.

## Untrained neural reference (seed 0)

- population edges equal discrete effective edges: True
- macro-skeleton structure: T1_single_scc=True, T2_bottleneck=True, T3_broadcast=True, T4_monitor_higher_order=True, T5_no_vestigial_declared_edges=False
- macro-skeleton Phi_s>0 stationary mass: 0.0000
- 5000-step rollout, no learning: steps=5000, deaths=440, mean_F_ext=0.3312, mean_F_int=1.1488, mean_L_meta=0.2400, mean_ignition=0.4030, mean_p_forage=0.5192
