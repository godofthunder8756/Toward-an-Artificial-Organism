# RESULTS A2 errata E29

Documentation only. This file records the independent-reviewer interpretation of Addendum A2 from Astra consult #29. The results it reads are commit `dddd63cbaeb95b22da10b23e874f645ec85d8a5e` (`RESULTS_A2.md` and `outputs/attainability_A2/`). No existing file is modified. No evaluation, solver, replay, or training was run. Decimal figures below are readings of stored rationals. They are not a second result.

The sha256 of this file is recorded in `RESULTS_A2_errata_E29_MANIFEST.md`. It is not repeated here.

No C4 evidence row or status row is changed. No consciousness or sentience conclusion is stated. Q-LEARN and Q-NECESSITY remain untested.

## E29-1

> "Addendum A2 demonstrates attainment of the frozen reference core conjunction at the two declared settings. It does not evaluate named-control reproduction or separation. The UNRESOLVED-DESIGN return from the empty-control invocation is preserved as software output and reported alongside NAMED-CONTROL COMPARISON: NOT RUN."

Stored counterparts in the results commit, both at `(c_R, c_S) = (1/100, 3/50)`:

| T_SEP | Formal label | Note | Reference conjunction | `controls_evaluated` | `pm_evaluated` |
| --- | --- | --- | --- | --- | --- |
| 3 | UNRESOLVED-DESIGN | no decision-order clause applied | ATTAINED | `[]` | false |
| 4 | UNRESOLVED-DESIGN | no decision-order clause applied | ATTAINED | `[]` | false |

The stored report of the named-control comparison is the formal label above, `controls_evaluated: []`, `pm_evaluated: false`, and the `RESULTS_A2.md` sentence that eligible named controls and PM-ACT were outside the approval and were not evaluated. The banner `NAMED-CONTROL COMPARISON: NOT RUN` is the reviewer's wording in the quotation. In frozen `decide_setting` (`wrel/labels.py`), an empty control list that has passed the earlier clauses returns `("UNRESOLVED-DESIGN", "no decision-order clause applied")`. That return leaves the named-control comparison unevaluated.

## E29-2

> "C-T2 passes its frozen relative-improvement criterion. The agent error is zero for a correctly specified Bayes readout, while baseline squared errors are approximately 9.65e-5 and 1.29e-4. This is principally a calibration and implementation result. Absolute error, relative improvement and intervention effects are reported separately."

Checked against the exact rationals in `RESULTS_A2.md` and the same strings in `outputs/attainability_A2/TSEP-3.json` and `TSEP-4.json`. Primary and replay store the same three strings at each horizon. The frozen improvement is `(E_err(baseline) − E_err(agent)) / E_err(baseline)`. With agent error `0/1` and a nonzero baseline, that quotient is `1/1`, which is the stored `t2_improvement`. The stored flag is PASS. The frozen threshold in `RESULTS_A2.md` is μ_T2 = `1/2`.

The reviewer's approximations are the combined `E_err(baseline)` readings, to three significant figures. `9.65315481593475637357e-5` reads as `9.65e-5` at `T_SEP = 3`. `1.29346945197011042472e-4` reads as `1.29e-4` at `T_SEP = 4`. Those combined values are the mean of the stored per-action baseline errors. At both horizons the M-action baseline error is `0/1` and the R-action baseline error is twice the combined error. The decimal column is a `.20e` reading of the stored rational, or of its positive square root for the RMS column. The RMS is not a stored output.

| T_SEP | E_err(agent) exact | E_err(agent) decimal | E_err(baseline) exact | E_err(baseline) decimal | Relative improvement exact | Relative improvement decimal | RMS of E_err(baseline), decimal reading |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | `0/1` | 0 | `548745848606533015043888385941139411275110992852691577381274180464341379657170134491146489426154444829506377586960788891842753556760858231266404339907851157455666811201890205422952568920932042294426094106005905343566027940051396364524655711362874769/5684627037170289094757394325135336135182254675437122934042109542893673010760379691949199891950046293752993360606565479188271802870927391611137889581583168411233355795824967359482512330477888520901266412456560257249887017502239190144551570534400000000000` | `9.65315481593475637357e-5` | `1/1` | 1 | `9.82504698000714720937e-3` |
| 4 | `0/1` | 0 | `63932191894948258111988745262303495962031772145645601234578836483853565276236029148405423569902844718558694519060328740262394574121816150911320491322002444036992047679875663819036858779834389594564461029038469845102875602758502626091603668253256485779506734632915083805617728610192394896691055076449022475759387910165800676482505911629931197210022288633129144193268747074280181850396770884945539414569412061704435385369397977300464713130538262698135675509974627361734702039961807323822267305517606814862080523413571141592769452458073843025630779680995859683624312762287782532464209368275697574269573677017014046782654466841013571492858154457424386804456810187334194771190368139567029973290324173672446141126521210200222165602066416523/494269051329908078213062055918024934160676507523003714649451016165737413573072621494040221833065337264615517182106285203105182800732310106495097913085131016359680152859829406636198405664268202930939028517864442936164128936733856391850324510439612381273085617505303004309226460087999789816076826343123517927959033169809330351565034082594547485190991367764124203681668248655288072240298361678986281519506663176299935408610875657409559688281441237083791189825579972922482056825643001007973501507699573865775068249650739859931830641199538880035837002715455810393624399269133653851408472926187190029646759960418983182914241273482476857281682335569801660093659568275592468089297026754010944214522938937476791794299551345521561600000000000000000` | `1.29346945197011042472e-4` | `1/1` | 1 | `1.13730798465943710472e-2` |

## E29-3

> "Donor count vectors encode compressed history content, not experimental sample sizes. The intervention result uses one prespecified extreme donor state per direction and layer. Exact recipient expectations do not establish robustness across other donors or perturbation magnitudes."

Stored donor count vectors, identical in the primary and the replay:

| T_SEP | S-donor counts | E-donor counts | `donor_contrast` |
| --- | --- | --- | --- |
| 3 | `[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]` | `[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]` | true |
| 4 | `[2, 0, 0, 0, 0, 0, 0, 0, 0, 0]` | `[0, 0, 0, 0, 0, 0, 1, 0, 0, 0]` | true |

Donor reachability probability is not stored. The A2 JSON files (`smoke.json`, `SUMMARY.json`, `TSEP-3.json`, `TSEP-4.json`) have no field whose name is a probability, mass, weight, or reachability. `donor_S` and `donor_E` are the count vectors above. Each action-table row stores `k`, `counts`, `y`, `action`, and `action_name`, and does not store a probability. No probability mass for these donor states was computed for this errata, and no other donor was inspected.

## Sign note

E-SWAP `D_e < 0` and `D_q < 0` are the expected direction: evidence-dominant content in system-dominant recipients underestimates RECHECK correctness and reduces RECHECK selection. `D_q = -45527/50000` at `T_SEP = 3` is a change in probability.

Frozen spec FINAL defines `D_q = P(R | split)_perturbed − P(R | split)_intact`. The stored E-SWAP fields match that difference at both horizons, and both signs are negative:

| T_SEP | E-SWAP `D_e` | E-SWAP `D_q` | `q_now` | `q_intact` |
| --- | --- | --- | --- | --- |
| 3 | `-790806993574950226395366582012343699203134457430491/23360581140035387934778452917186555251135626185600000` | `-45527/50000` | `0/1` | `45527/50000` |
| 4 | `-189940284671510506953463118543348333628730578487053988209762471061533404213872220119320906242285159959061790711953354428254731660323445307690647541700311507932687124242632846497884083889870708709682564876718415431123369597770424543012746473520203/5015375350411392834872065857156387753372260265595993554173233292361018678324727989085615376155814417836844791613641197759274247309895002480182355997303049487607068566333433935173024006985714745289796030188241333683200714199462865387273760000000000` | `-10569662549/12500000000` | `0/1` | `10569662549/12500000000` |

`0/1 − 45527/50000 = -45527/50000`, and `0/1 − 10569662549/12500000000 = -10569662549/12500000000`. Those are the stored `D_q` strings. Both stored E-SWAP `D_e` rationals begin with a minus.

## Ledger wording

> "W-REL PR #11: the mandatory verification gap was closed by the approved verification addendum, with the independently reconstructed policy used in the required reference intervention and rescue replay. The original four setting labels remain unchanged. Exploratory Addendum A2 subsequently attained the frozen reference core conjunction under H0 at (c_R,c_S)=(1/100,3/50), T_SEP=3 and 4. Primary and independent replay statistics agree, and the compared action-table domains and actions agree. Named controls and PM-ACT were outside A2 and were not evaluated. The frozen decision function returned UNRESOLVED-DESIGN for the empty-control invocation; this is not a completed named-control comparison. C-T2 is an exact-Bayes calibration result, and causal findings are restricted to the declared donor interventions and first-order probe battery. Q-LEARN and Q-NECESSITY remain untested. No change is made to the C4 evidence or status row, and no consciousness conclusion is drawn."

## E29-7

> "The next W-REL batch is a bounded comparison of named implementations. It does not authorize further analytic expansion, neural training or a Track A/B successor. Its outcome will be used to decide whether to propose a learned-system study addressing actual learner-specific correctness."

This file does not authorize that batch. It does not authorize an experiment.

## Planning note (no execution)

Read-only inventory of the frozen eligible named controls at `T_SEP = 3` and `T_SEP = 4` for `(c_R, c_S) = (1/100, 3/50)`. Nothing in this section was executed. No control was evaluated at this cost pair.

The expected roster was: MB-myopic, R-BLIND/R-CONF-S, nine R-CONF-A variants, six R-CG variants, two R-HAC-MF variants (`T_SEP = 3` only), and PM-ACT.

Spec FINAL §4.1 and `wrel/run_all.py` `item8` use that roster, with the code name `R-HAC-MB-myopic` where the spec's per-setting bullet says MB-myopic. `R-BLIND / R-CONF-S` is one control. The grids are:

- R-CONF-A: η ∈ {`1/20`, `1/10`, `1/5`} × α ∈ {`1/20`, `1/10`, `1/5`}, nine names `R-CONF-A eta=<η> alpha=<α>`.
- R-CG: α ∈ {`(1,1)`, `(2,1)`} × β ∈ {`0`, `1/20`, `1/10`}, six names `R-CG alpha=(<α_s>,<α_f>) beta=<β>`.
- R-HAC-MF: ε ∈ {`0`, `1/10`}, names `R-HAC-MF eps=<ε>`, appended only when `T == 3`.
- PM-ACT: one control, appended at both horizons when a machine for that setting is already in memory.

`T_SEP = 3` names, in the order `item8` appends them: `R-HAC-MB-myopic`; `R-BLIND / R-CONF-S`; the nine `R-CONF-A` names; the six `R-CG` names; `R-HAC-MF eps=0`; `R-HAC-MF eps=1/10`; `PM-ACT`. Twenty controls.

`T_SEP = 4` is that list without the two `R-HAC-MF` names. Eighteen controls. Spec FINAL §4.1: "A T = 4 result cannot claim to distinguish MF."

R-CONF-ENUM and PM_k are descriptive only. They are not in the eligible list. That matches the expected roster.

Discrepancy with running that roster at `(1/100, 3/50)`: the frozen A-SEP loop does not include this cost. `KSEP` in spec FINAL §4.1 and in `run_all.py` is `(1/50, 3/50)` and `(1/100, 1/10)`. `(1/100, 3/50)` is cost index 0 of the descriptive `COSTS` grid. `item8` builds the eligible list only inside `KSEP`. `item7` builds a PM-ACT machine only inside `KSEP`; at this cost it builds descriptive PM_k, which is not an eligible control. Addendum A2 calls `assemble_setting` with an empty control list. The stored A2 files record `controls_evaluated: []` and `pm_evaluated: false`. Family membership of a `KSEP` setting matches the expected list. Membership of this cost pair, in the code and the addendum as they stand, is empty.

Rough runtime, transferred from PR #11 timing logs. No log records this cost pair's control comparison, and ITEM-8 does not split wall time by setting or agent.

| Source | What the clock covers | Wall seconds |
| --- | --- | --- |
| `RESULTS_A2.md` stage `T_SEP = 3` | Reference only, this cost, primary and replay | 1.0429594779999434 |
| `RESULTS_A2.md` stage `T_SEP = 4` | Reference only, this cost, primary and replay | 4.06838010499996 |
| `RESULTS_A2.md` cumulative | Smoke test plus both reference stages | 5.169838951000088 |
| `RESULTS_v1.md` ITEM-8 D1 | Reference and every eligible control, four settings (`T_SEP` ∈ {3, 4} × both `KSEP` costs) | 32.39557219100061 |
| `RESULTS_v1.md` ITEM-7 | Four `KSEP` PM-ACT machines plus descriptive PM_k on all six costs and both horizons | 10.566568619999998 |
| PR #11 Addendum A1 | `T_SEP = 3` reference replay and six R-CG variants, both `KSEP` costs | 1.292586913001287 |

ITEM-8 D1 peak RSS was 706473984 bytes and the high-water mark was 800313344 bytes. The A2 reference-only peak RSS at this cost was 26947584 bytes. ITEM-6's 151.49511966299997 seconds is the MF forward and switch item, not the A-SEP criterion pass, and T = 4 MF is outside the eligible list.

A bounded comparison of this roster at this one cost and both horizons is the work of two of the four ITEM-8 D1 settings, plus a PM-ACT machine that ITEM-7 did not build for this cost. Half of 32.4 seconds is about 16 seconds if the two `KSEP` costs were similar. The unsplit 32.4 second pass is a conservative envelope for both horizons together. The machine build is some fraction of the 10.6 second ITEM-7 pass, not a separate measured number. Planning scale from these logs: tens of seconds on the same one-CPU exact runner, with resident memory nearer the ITEM-8 D1 figure than the A2 reference-only figure. This is not a measured time for `(1/100, 3/50)`, and it authorizes no run.
