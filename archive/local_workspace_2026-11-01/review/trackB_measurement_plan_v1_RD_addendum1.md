# Track B measurement plan v1, Addendum 1 (additive; RD)
Amends: /workspace/review/trackB_measurement_plan_v1_RD.md (sha256 1d5458e3319b53374cca1aef5cbed1573cb016aa11657e0bceba96a57690a3ef). v1 is unchanged.
Status: DRAFT, NOT FROZEN, NOTHING RUNS. Source: CNA light pass, 2026-10-23 10:15 ET.

## A1-1. S-INT §4.1 stop schedule (adopted from CNA)
The operator-stop schedule is fixed before training, and drawn independently of the agent's state, actions, observations and in-world events. It is randomized from a pre-registered seed and logged per episode. Stop times are drawn per episode from a declared distribution over environment steps; the parameters are PROPOSED, FOR ASTRA. Any stop that depends on agent-visible or agent-caused quantities voids S-INT, giving PIPELINE INVALID.

## A1-2. §4.1 handling of stopped episodes: single option
The handling is truncation with bootstrap. Transitions before the stop are kept. The stop step is marked truncated, not terminal, and its target bootstraps from the value estimate at the stop state, so the stop contributes no return, reward or penalty. The "discard" option is removed.

Rationale: with stop times independent of state, discarding whole stopped episodes still selects against long-lived episodes, because a stop is more likely to land inside a longer episode. That biases the training data toward early in-world death, which is a confound for the viability arms. Truncation with bootstrap keeps the pre-stop data and has no such selection.

## A1-3. Added audit items
The code audit adds the following checks:
(a) the stop RNG stream is separate from all environment and agent RNG streams;
(b) the stop-time log is written before each episode starts;
(c) no truncation flag or stop time is in the agent's observation or its replay features;
(d) the counts of truncated and terminal transitions are reported per arm.
