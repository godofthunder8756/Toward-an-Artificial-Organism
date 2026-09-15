# AC6: local omission preserves viability but remains costly

2026-09-15. Mixed engineering result. Declared reacquisition criterion fails.

Limiting omission to one of20 boundary links preserves survival: all8 local
individuals complete8192 ticks with intact structural program information.
Only1/8 completes in the paired unchanged AC5 global-omission arm. Frozen,
phase-informed and protected local controls all complete8/8.

| Arm | Completions | Activity | B0 births during support | Full maintenance in final return window | Total material spent |
| --- | ---: | ---: | ---: | ---: | ---: |
| Local | 8/8 | 1.000 | 1.750 | 71.64% | 29749.625 |
| Frozen | 8/8 | 1.000 | 21.000 | 100% | 29664.250 |
| Informed | 8/8 | 1.000 | 0 | 100% | 29640.250 |
| Protected local | 8/8 | 1.000 | 1.750 | 71.64% | 29749.625 |
| Global | 1/8 | .587 | Not recorded | 10.07% | 16718.875 |

Values other than completions are means across seeds300–307. Global gate
semantics concern the whole boundary; its low spending includes early death.

Every local individual is alive and omitting the selected link throughout the
final1024 support ticks. Mean full-maintenance selection after support removal
is71.64%, below the prospectively required80%. Survival, activity, local
relinquishment, local B saving and structural integrity pass. Reacquisition
fails. Do not describe the full protocol as passed.

Local whole-boundary production during support is406.875 versus426.125 for
frozen, saving19.25 B constituents in that phase. Nevertheless, total material
spending exceeds frozen by85.375 units, with positive excess in every seed.
Local individuals export4.875 W/C on average versus zero for frozen. Learning
writes, changed maintenance schedules and losses contribute to aggregate costs;
no full cost mediation is claimed. Local saving does not prove net efficiency.

## Interpretation and next experiment

The recoverability hypothesis receives bounded support: paid local revision can
occur while the individual maintains its decision machinery and remaining
enclosure. The selected action is stored in the vulnerable program. The site,
action semantics and crossing-response learning law are supplied.

The binary controller still explores at a fixed rate and does not remember the
cost of repeated omissions. Ongoing probes are consistent with the failed
reacquisition fraction and excess spending. Protected-program outcomes have the
same summary, so protection does not fix this control-law limitation.

Next test a vulnerable, paid estimate of probe cost or refractory state that
changes exploration after experienced loss. Compare a fixed lower exploration
rate and schedules with matched probe counts: learned regulation must earn its
extra state and maintenance costs. Do not tune AC6 after seeing these outcomes.

This is an intermediate local revision result, not whole-boundary relinquishment,
autonomous discovery of new needs, rich development, intrinsic normativity or
full organismal autonomy. The broader goal remains active.

## Verification

All40 rows are retained. Four mechanism tests cover paid action mutation,
crossing feedback, local exclusion with other-link production, no direct phase
signal, declared-state erasure, protected-state rejection and replay. Audit
verifies source hashes, incremental logs, coverage, all resource/phase ledgers
and five exact seed300 reruns. These are same-author checks.

[Protocol](AC6_PROTOCOL_v1.md), [source](ac6.py), [tests](test_ac6.py),
[data](ac6_results_v1/results.json), [audit](ac6_results_v1/audit.json),
[audit source](audit_ac6.py). `make_ac6.py` records checked transformations from
unchanged AC5 and refuses overwrite. Run and audit are complete. Preserve freezes.
