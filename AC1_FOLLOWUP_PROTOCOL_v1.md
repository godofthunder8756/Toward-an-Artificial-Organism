# AC1 follow-up: free ablation and independent engineering seeds

Written after AC1 v1 results, before this follow-up. Exploratory validation,
not external preregistration or an independently reviewed confirmatory study.
Original model, protocol, tests, snapshot and results stay unchanged.

## Question

Does the acquired-controller maintenance effect persist when ineffective
controller writes are free, and on new seeds without changing the physics?

V1's no_policy_write charges the same cost for attempted sham writes. Its lower
activity could partly reflect futile spending. A new control refunds energy and
precursor for controller-bank sham attempts immediately within the step, before
termination is applied. Living cost remains paid. The actuator's attempt count
and partial-write cap are otherwise inherited; this refund is an explicit
favorable resource intervention, not ordinary physics or target repair.

## Fixed follow-up design

- Seeds 1000–1031, disjoint from original engineering seeds 0–7.
- All six original environments: p=0.0005/0.001/0.002, no pulse/partial pulse.
- Same 3,000 ticks, acquisition, observations, representation and costs.
- Arms: self, no_policy_write, free_policy_ablation, protected.
- All rows retained, with environment/action digests and final states.
- Primary descriptive contrast: self minus free_policy_ablation planned activity.
- Also controller and payload accuracy, survival, correct decisions per planned
  tick, ledger balances and each bank's successful writes.
- Descriptive 95% percentile intervals over paired seeds; 10,000 resamples,
  generator seed 20260914. No significance or broad-autonomy declaration.

No parameter selection or further tuning is part of this follow-up. The
favorable-control code must pass a deterministic refund/ledger test before
execution. A ledger audit and exact sampled replays follow the run.

## Additional interpretation limits recognized after v1

The learned policy family has only 24 possible bank-priority permutations
(at most log2(24), about 4.585 bits of history-specific choice). Its nominal
table uses 192 data bits plus redundancy; those are storage capacity, not
192 independent acquired policy bits. Most resource priorities are supplied
by demonstrations. Arbitrary payloads contain 192 independent binary targets.
The agent has no rule that reconstructs missing policy entries from this
known family, but a stronger future comparator could exploit that redundancy.

V1 has four environments passing its aggregate engineering criteria, including
the lowest-rate pulse case with one death. A criterion pass must not be described
as every individual surviving or complete recovery of every original bit.
The fixed protected policy is often as good or better; this construction is
explicitly ordinary error correction with a vulnerable demonstrated policy.
