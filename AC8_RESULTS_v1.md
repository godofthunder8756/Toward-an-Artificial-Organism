# AC8: reacquisition and selective route-field maintenance

2026-09-15. All48 engineering conditions retained; both declared gates pass.

When both resource mappings change at tick4096, all8 live learners reacquire
correct routes by ticks4104–4157 and complete8192 ticks. All8 learning-frozen
controllers terminate; mean activity is.527. They acquired the original mapping
before learning stopped. Random port selection completes8/8, so stored routing
remains one viable strategy, not the only one.

With mapping fixed and learning stopped after2048, ordinary repair preserves
activity and correct routes in8/8 individuals. Excluding only the eight routing
action bits from repair leaves1/8 completing; mean activity falls to.781.
The21.94-percentage-point difference passes the prespecified.2 gate. Allowing
learning to continue with the same repair exclusion gives the same aggregate
outcomes, so this learning law does not compensate for the damage observed.

| Condition | Completions | Mean activity | Correct final routes |
| --- | ---: | ---: | ---: |
| Remap, live learning | 8/8 | 1.000 | 8/8 |
| Remap, learning frozen | 0/8 | .527 | 0/8 |
| Remap, random sampling | 8/8 | 1.000 | 2/8 stored guesses |
| Static mapping, preserve routes | 8/8 | 1.000 | 8/8 |
| Static, block route repair | 1/8 | .781 | 2/8 |
| Static, block repair but keep learning | 1/8 | .781 | 2/8 |

Raw correctness in a terminated body is its frozen endpoint, not continued
functioning. One terminated repair-blocked individual has correct routes at
the endpoint; these results do not prove that every termination coincided with
a persistently wrong route. A detailed mediation chronology is not established.

## Important distinction

This experiment isolates routing action fields from the rest of the controller,
but each field includes learned port-selection bits and inherited action-type
bits. Learning switches action0 to12 or1 to13; the high two bits change, while
the low two define the inherited resource action. Blocking all eight bits does
not by itself show which subset causes the maintenance dependence.

Next partition those subsets prospectively, preserving ordinary uniform noise,
costs and the source experiment. This prevents attributing an inherited-opcode
failure to loss of newly acquired information. The unknown environment still
contains only two independent routing choices, not a newly created metabolic need.

## Verification

Three test methods verify default-step equivalence, targeted repair selectivity
and payment, and short replay. Audit verifies source snapshots, all48 unique
conditions, incremental logs, energy/fuel/material balances and six exact seed801
reruns. All earlier physical and learning laws remain supplied as documented.
Same-author engineering evidence, not independent confirmation or full autonomy.

[Protocol](AC8_PROTOCOL_v1.md), [model](ac8.py), [tests](test_ac8.py),
[data](ac8_results_v1/results.json), [audit](ac8_results_v1/audit.json),
[audit source](audit_ac8.py). Run74372 and audit73566 are complete with exit0.
