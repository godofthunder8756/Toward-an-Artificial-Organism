---
description: Operational N2 construct and bandwidth accounting for competitive shared access
---

# Competitive shared access

## Scope

The question is whether an acquired, task-conditioned limited channel has a
causal *advantage*, not whether a network can be drawn with a workspace box.
The minimum candidate has four private recurrent streams, one selector, one
finite-alphabet shared message, and three decision processes. Each stream has
a fixed *observation port* for one sensory modality but receives no ground-
truth factor or latent label. Its learned features need not align one-to-one
with any generative cause. The selector reads the four private states and
public context, not the generative factors. A consumer may use its own local
sensor input, public task context, and the shared message, but not another
stream's hidden state. The four-port partition is a design assumption, not
evidence that an unrestricted learned representation requires occupancy.

## Operational terms

* Local availability: a representation can be read within its producer or
  designated consumer, without making it readable by all consumers
* Shared availability: an encoded message is simultaneously readable by all
  three consumers at the decision tick through the same write event
* Access: an authorized read of that actual message; a head that receives the
  entire encoder state does not use the constrained channel
* Selection: a learned map from observation-derived hidden states and public
  context to one stream address and its payload, potentially changing within
  an episode
* Capacity: the log2 of the number of distinct on-wire messages, **including
  address, payload, blank/sentinel, timing, and any side channel**; a nominal
  one-slot design with a real-valued unquantized payload has no usable bound
* Competition: at a common decision time at least two acquired contents would
  improve distinct downstream decisions if made available, but their joint
  transmission exceeds the on-wire budget; occupying the channel with one
  precludes the other and changes observable losses
* Specialist: a separately timed decision process with its own observations,
  action, loss and permissible state; three identical prediction heads do not
  satisfy this definition
* Broadcast/read access: all three consumers observe the *same* on-wire bits,
  not independently computed equivalent copies
* Architectural advantage: a prespecified improvement on a consequential
  primary endpoint over the strongest eligible no-bottleneck/non-workspace
  rival, at declared parameter, information, latency and compute accounting

## Channel accounting

Use four learned private candidate streams, each sending a **one-bit**
quantized payload if selected. Exactly one stream may write per decision tick.
Its two-bit address plus payload form an alphabet of eight messages, or
three bits total. There is no extra blank symbol on a decision tick. The
choice of address itself conveys information and is counted; confidence,
selector logits, recurrent W state, and write timing are not consumer inputs.
All consumers see the same three bits. The four independent binary world
factors have 16 configurations: even granting a perfect encoder, a static
three-bit message cannot recover all four bits at once. Factor-specific
posterior confidence is also inaccessible unless encoded in those bits.

This cardinality fact is necessary but not sufficient. A neural selector
could use the address as a side-channel to encode information unrelated to
the chosen stream. Audit actual information flow, state-matched interventions,
and per-content decoding before attributing effects to occupancy. If the
candidate hides task IDs or history outside the charged three bits, the
bottleneck fails and the claim stops. Encoding one task-conditioned aggregate
bit can be an ordinary router; the fixed-routing and shared-encoder rivals
must test that reduction rather than renaming it a workspace.

## States and permitted memory

Private encoder states persist for the episode at no fee in all corresponding
arms. W is overwritten at each decision tick and does not persist. Selection
has no exogenous fee. All consumers read W simultaneously; there is no
sequential-query loophole. Specialists may retain only their specified local
history, and their histories and compute must be reported. Neither paid
persistence nor explicit integrity state is part of the primary test.

The claim ceiling is learned content-specific competitive availability with
measured rival-exclusive value in this environment, not global broadcast in
theoretical generality and not a consciousness indicator.