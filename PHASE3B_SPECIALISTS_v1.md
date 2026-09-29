---
description: Three consequence-bearing decisions with distinct losses and local information in Phase III-B
---

# Phase III-B specialists

Each of the three specialists receives only the current public context,
its own current BSC(1/5) sensor, and the same three-bit channel message.
None sees earlier common evidence, another specialist's local sensor,
the selector logits, true factors, or a cached W. The common history
enters through the candidate's learned private encoder only. Context zero
uses ports 1, 2, and 3/4 below; subsequent decision ticks rotate factor
indices modulo four without changing the loss types. All three act at
each decision tick, but their actions have different effects and timing.

| Consumer | Output and action timing | Consequence and objective | Required information | Private memory |
| --- | --- | --- | --- | --- |
| S1 immediate control | binary `a` at each tick | unit loss if `a != z_1` at that tick; control reward is immediate | evidence about currently assigned factor and its own sensor | no recurrence in candidate; R3 receives its own full-history recurrent encoder |
| S2 delayed commitment | `bet 0`, `bet 1`, or `abstain` at each tick; settle one tick later | wrong bet costs 1, correct bet 0, abstain 0.18; delayed settlement cannot be revised | calibrated confidence in its assigned factor and its own sensor | one pending action only; R3 also receives its own full-history recurrent encoder |
| S3 contextual integration | binary parity action at each tick | unit loss for wrong XOR of two context-assigned factors; feedback at end of episode | relation between two factors, including one private sensor reading | no recurrence in candidate; R3 also receives its own full-history recurrent encoder |

At context zero S1 targets `z_1`, S2 `z_2`, and S3 `z_3 XOR z_4`.
All four factors can therefore matter simultaneously. Across ticks, each
specialist's target indices rotate together; its loss, sensor type, and
action alphabet do not. S3 receives a local reading of the first XOR
factor. S1 and S2 each receive a local reading of their target. An oracle
can compute each ideal response from the evaluator belief, but these
beliefs are not inputs to the learned candidate at evaluation.

These processes are not three heads predicting identical labels: one
acts for immediate 0/1 control, one trades commitment against abstention
and settles later, and one integrates a parity relation with delayed
feedback. Losses must be normalized and reported separately alongside
the joint endpoint. Feedback timing must not leak pending ground truth
into later inputs. The temporal schedule and reward ledger are also
available to all matched rivals.