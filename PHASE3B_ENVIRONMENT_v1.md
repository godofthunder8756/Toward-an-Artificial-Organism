---
description: Proposed four-factor temporal observation world for the Phase III-B identifiability gate
---

# Phase III-B generative environment

## Generative model

At episode start draw four independent fair binary factors `z[0:4]`.
They remain fixed within the episode. Each factor has its own sensory port;
at ticks 0 through 7 the agent receives exactly one noisy binary reading
from the scheduled port. Each port is sampled twice, at ticks `j` and
`j+4`, with independent bit flip probability 1/5. Sensor schedules and
port identities are public, but latent bits, clean values, and Bayes
posteriors are evaluator-only. All agents receive the same noisy history.
An individual reading has posterior error 1/5, so no single observation
recovers a latent. Conflicting readings leave uncertainty 1/2.

At decision ticks 8 through 11 the current common observation is the same
null symbol. Public context rotates which ports affect immediate control,
delayed commitment, and contextual integration; at least three factors have
positive decision value at each tick. The task context changes mid-episode
but is never a latent truth label. A specialist additionally receives only
its own independent BSC(1/5) local observation at its decision tick. Local
signals are not visible to the shared selector. Draw fresh noisy observations
for every episode; random seed is the independent replication unit.

The fixed factor prior, sensor reliability, and schedule are public to the
evaluator and oracle arms. Neural agents are trained from observations and
loss only; they receive no clean factors, teacher beliefs, or world-model
parameters as input at evaluation. A supervised auxiliary decoder may be
used on training data only if every learned rival gets the same labels and
the primary policy is not fed its output at evaluation.

## Causal opportunities and limitations

The full evaluator belief after tick 7 is a product of four Bernoulli
posteriors, each with three attainable levels. There are 81 possible belief
vectors and only eight shared-channel messages. Multiple factors can have
nonzero simultaneous decision value, and their independent evidence can
make the preferred content change even when clock, public context, current
observation, and local signals are held equal. H3 must demonstrate that
claim for the fully specified specialist losses, not merely count bits.

Factor-specific sensor ports are an explicit inductive bias. This is a
small world designed for pretraining identifiability, not evidence that
learned codes require four human-interpretable factors. Report any simpler
finite-state, posterior-counter, arbitrary three-bit encoder, or fixed
task-clock solution. If a fixed or unrestricted rival works as well, keep
the environment and accept the negative architectural result.