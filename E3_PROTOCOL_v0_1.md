---
title: E3a acquired-information maintenance protocol
description: Unfrozen baseline-first protocol for material-paid memory reconstruction without answer feedback
ms.date: 2026-09-09
---

## Status and boundary

Version 0.1 is a review-ready protocol proposal, not a frozen executable protocol.
No E3 model, engineering run, final sample or result exists. Numerical commitments
below are prospective design choices, not feasibility-validated values.

This follows [NEW_AGENT_GUIDE.md](NEW_AGENT_GUIDE.md), the
[primary-literature review](E3_LITERATURE_REVIEW_v0_1.md), and
[E3_DESIGN.md](E3_DESIGN.md). E3a deliberately tests a smaller claim first:
finite acquired-information maintenance using conventional correction and
allocation. It does not yet put recall and maintenance in one developing
recurrent neural network. That architectural objective is reserved for E3b.

Two freezes are required. First freeze the completed state, transition, interface
and decision specification before implementing E3. After engineering-only tests,
freeze source, tests, analysis, configuration and gates again before fresh final
seeds. Neither freeze is an external preregistration. This document performs
neither freeze; unresolved implementation-specification items are listed below.

## Falsifiable claims and strongest rival

H1: With fixed information capacity and resource opportunity budgets, paid
scrubbing from surviving redundant traces improves useful recall after a later
damage challenge by at least five percentage points over writes-disabled
storage, without examples or answer-dependent feedback during recovery.

H2: Ordinary utility-conditioned allocation reduces corrective writes and their
material expenditure on obsolete associations while retaining useful recall
and viability, compared with its own continued-usefulness branch and a tuned
fixed scrub schedule. This is not a claim of reduced total energy expenditure.

These hypotheses test functional information maintenance and instrumental
allocation. H1 does not require immediate recall improvement: error correction
can hide damage before redundancy is repaired. H2 occurs in a separate,
feedback-enabled phase and cannot prove example-free recovery.

The strongest rival is conventional ECC plus ordinary reinforcement learning.
E3a implements that rival as its reference mechanism, rather than inventing a
new name for it. Success would go beyond E2's preserved-weight bypass but would
not demonstrate a novel adaptive algorithm or a source of subjective wanting.
Any later new mechanism must beat the conventional adaptive baseline, not merely
the writes-disabled or fixed-policy controls.

## 1. Exactly what is acquired

Use 16 public, opaque cue addresses. For each independently developed individual,
assign one independent fair binary output to each cue after inherited algorithms
and hyperparameters are fixed. Do not impose label balance, a permutation, or a
rule relating cues to answers. The ideal target distribution has 16 bits of
entropy. Record actual generator provenance; a short shared seed is not an
independent 16-bit source if the agent can read or reconstruct it.

Acquisition presents each cue-answer pair through an explicit teaching interface
and pays for all encoded writes. This is externally supplied learning, not
spontaneous invention of a memory capability. A delayed-address assay presents
the cue, then four blank ticks before the answer request. The address latch is
declared transient state; this simple delay is not a learned recurrent pathway.

Candidate fixed acquisition budget: 16 presentations per cue, 256 total.
Unequal output frequencies arise naturally and are retained. Targets, controller
initialization, opportunity schedules, damage and exploration use separate random
streams. Neither run identifiers nor target-generator state enter the agent.

## 2. All copies and their representation

The reference representation has five spatially separated binary replicas per
association: 80 code cells. Each physical cell uses a two-bit symbol alphabet
for zero, one and erased; the fourth encoding is also treated as erased. Thus
the code bank has 160 allocated bits, not 80. A write can produce zero or one;
the erasure symbol cannot retain an old sign in a hidden field.

The live association value is decoded from current symbols, never from a host
weight backup. Count all other mutable state in a common finite allocation:
candidate allowance 2,048 persistent bits and 256 scratch bits per variant,
in addition to the 160-bit code bank. This is allocated capacity, not learned
information. No uncharged float, variable-length history or Python container
may retain values across steps. Publish used and unused capacity by field.

| State                                       | Allowed treatment                                                      |
|---------------------------------------------|------------------------------------------------------------------------|
| Answer replicas or block parity symbols      | Live, finite, damageable storage; no privileged systematic copy          |
| Learned allocator values and eligibility     | Finite storage within the common allowance; costed and vulnerable        |
| Decoded answers, syndromes and work queues    | Bounded scratch; cleared after the atomic operation                     |
| Delay latch and recurrent activity           | Declared scratch; cleared at isolation and complete-erasure boundaries   |
| Material, energy and spatial resource state  | Fixed-width integer state; no hidden fractional residue                 |
| Counts, format tags, health and timestamps    | Budgeted metadata unless fixed public inputs independent of targets     |
| Replay, target networks and optimizer copies | Excluded in E3a; any later addition requires a new budget and protocol   |
| PRNG states and outstanding events           | External target-independent streams; cancel pending feedback on reset   |
| Evaluator keys, original checkpoints, logs    | Experimenter records; inaccessible to the recovery process              |

All per-individual mutable fields require a schema and reset/damage policy.
Target-dependent resource distributions or counters are acquired state even if
they are not called memory. Checkpoints must serialize the entire allowed live
state without pickle. Logging and counterfactual copies are one-way outputs.

## 3. Recovery information boundary

At the isolation boundary, clear teaching buffers, answer-bearing activations,
pending rewards, decoded caches and operation scratch. Retain only the declared
surviving code and allocator/body state. The permitted transition interface
accepts live state, target-independent opportunities and independent noise, not
the answer table, an evaluator closure, a clean checkpoint or true loss.

During the 128-tick recovery block, supply no examples, correctness feedback,
task-dependent food, gradients or task-dependent stopping conditions. Scoring
occurs offline after predictions are finalized. Neutral resource opportunities
are identical across paired variants and independent of target answers.
Current trace agreement can guide correction; true trace correctness cannot.

Resource-only feedback is allowed if its value is provably answer-independent.
Freeze allocator learning in the primary isolation assay so its behavior uses
only prior development and current permitted observations. The live controller
values remain vulnerable; frozen updates do not mean protected storage.

Run the isolated worker with an explicit allowlist of serialized inputs and no
read access to experiment checkpoints, answer files or logs. Python encapsulation
alone is not a security proof. Independently inspect reachable state and use
counterfactual noninterference tests; do not claim adversarial sandbox security.

## 4. Material, writes and generic computation

Material buys write operations and maintenance capacity; it never chooses the
answer to write. A scrub operation reads surviving local symbols, decodes a
value, and pays to replace erased or disagreeing symbols. If no value can be
decoded, it abstains; it cannot query a true answer. Ties on forced-choice probes
use pre-drawn random bits. A forced probe guess is never written back to live
storage. Live repetition scrubbing abstains on a tied vote; block decoding uses
the separately declared minimum-distance rule. Copying a wrong majority is a
recorded miscorrection.

All reads, successful and failed write attempts, control decisions, decoder
operations, communication and occupied-storage ticks have ledger entries.
Candidate integer ledger:

$$
E_{t+1}=\operatorname{clip}(E_t+F_t+R_t-C_t,0,E_{\max}),
\qquad P_{t+1}=P_t+D_t-W_t-O_t.
$$

Here $F$ is accepted ordinary food, $R$ declared external support, $D$ material
deposition, $W$ paid writes and $O$ overflow. Record energy overflow separately;
do not silently reward clipped throughput. Cost $C$ includes living, storage,
read, write, logic and distance charges. Insufficient resources prevent the
operation before it changes storage; partial operations need an explicit order.

Candidate coefficient grid for later engineering: one energy quantum per symbol
read, four per symbol write plus one material unit, one per declared primitive
logic operation and link hop, and 16 living quanta per tick. Storage rent and
resource yields must be fixed in the opcode-level specification before coding.
These are simulator quanta, not ATP, joules or actual host compute expenditure.

Error/erasure risk increases when paid maintenance lapses, rather than merely
attenuating a preserved value. Exact rent, lapse-to-hazard law and physical event
ordering remain freeze blockers. Material-only refill leaves every symbol
unchanged at that instant. Future funded writes can reconstruct partial loss
from survivors; this is expected and must not be called material restoring bits.

## 5. Conventional baselines and matching

All main arms receive the same payloads, locations, corruption streams, resource
opportunities, scalar objectives and planned experience. Compare both permitted
capacity and actual expenditure; equal opportunities do not imply equal costs.

| Arm                         | Purpose                                                         |
|-----------------------------|-----------------------------------------------------------------|
| Repetition, no writes        | Passive decoding and damage tolerance without reconstruction    |
| Repetition, periodic scrub   | Tuned fixed maintenance schedule, not wasteful always-copy       |
| Repetition, threshold scrub  | Conventional disagreement-triggered repair                      |
| Repetition, ordinary RL      | Primary utility-sensitive conventional maintenance reference    |
| Block code, ordinary RL      | Capacity-matched conventional storage-efficiency challenge       |
| Frozen allocator            | Paired trained policy with no further updates in ecology        |
| Fixed maintenance drive     | Explicitly assigned upkeep objective, diagnostic not fair reward |
| Exact-template oracle       | Privileged repair with extra answer information, positive check |

Candidate RL observation: quantized current agreement/erasure status, material
and energy status, and visible cue usefulness. Actions: forage, collect material,
or scrub the current offered association/block. Do not expose correct labels,
true damage-to-answer distance, intervention names or oracle usefulness estimates.
An ordinary finite tabular learner is sufficient; no target network or replay.
Its exact table, quantization, update rule and storage-refresh schedule must be
specified within the common bit allowance before implementation.

Tune periodic intervals and thresholds on engineering individuals only. Give
the ordinary adaptive rival at least the candidate's information and development
budget. A fixed code with adaptive scrubbing is not a fixed-policy control.

For each four-cue block, the proposed fixed $[20,4,10]$ binary code uses the same
20 two-bit physical cells as four five-copy associations. Use a generic
minimum-distance decoder over 16 possible codewords, with costs for all reads,
scratch and computation. Break equal-distance ties using independent randomness.
No true encoded word is retained. Its construction is in the
[literature review](E3_LITERATURE_REVIEW_v0_1.md).

Permit the same maximum communication range to every code, and charge measured
path lengths. Repetition is locally cheaper to decode but can be less robust to
some faults. Shared block parity couples useful and obsolete bits; charge full
physical cost and report block-level abandonment separately. Do not allocate
parity costs to individual labels by an arbitrary favorable fraction.

## 6. Partial damage and recovery schedule

Pair every intervention from the same developed individual and fixed time,
not from outcome-selected survivors. Candidate isolation sequence:

1. Offline pre-damage probe on a disposable clone; never return that clone.
2. Clear transient state and apply a prespecified damage mask to the live branch.
3. Offline acute probe on another disposable clone.
4. Run 128 recovery ticks with no answer channel, recording paid writes.
5. Probe an isolated clone after clearing inference scratch.
6. Apply an independent challenge to the recovered live storage with writes
   disabled, then measure 256 planned delayed queries.

Primary proposed channel: erase exactly two of five spatial replica layers,
with mask independent of values. During recovery, candidate independent
per-occupied-symbol flip hazard is 0.001 per tick under fully paid upkeep;
unpaid hazard is to be specified before freeze. Challenge: independent unknown
flips with probability 0.10 per surviving code symbol. Declare the same physical
damage on all acquired storage regions or explicitly label code-bank-only and
whole-substrate assays separately. Allocation state cannot silently be spared.

For pure erasures, three surviving equal replicas determine the old bit; material
can buy copies but not supply the missing answer. This channel therefore tests
restored redundancy and later resilience, not creation of information. Separate
secondary channels cover independent unknown flips and contiguous spatial loss.
Do not pool channels or substitute whichever produces a favorable outcome.

Required paired branches: intact; partial damage with correction; same damage
with writes disabled; material-only refill with writes disabled; sham material
with matched acquisition cost; and externally funded ordinary correction.
External funding pays the same decoder and writes without supplying values.
Exact-template restoration is a distinct, explicitly privileged oracle branch.

## 7. Complete-loss negative control

Completely overwrite all agent-reachable acquired state with a canonical
target-independent state, including replicas, parity, policy, body distributions,
queues, delay latch and random-state dependencies. Keep only inherited generic
laws and public cues. Refill material and energy identically across histories.
Run the same no-answer-feedback recovery boundary as in partial-damage arms.

An invertible permutation, sign inversion, biomass lesion or reset of only the
named weight array is not complete deletion. For binary targets $Y$, inherited
rules $G$, reset state $S^+$ and subsequent inputs $Z$, require:

$$
P(S^+,Z\mid Y,G)=P(S^+,Z\mid G).
$$

Under this construction expected forced-choice accuracy is one half. Test the
actual acquisition-to-erasure transition on every one of the 16 four-bit target
tables, not merely an already blank initializer. With paired subsequent streams,
canonical states, agent trajectories and predictions must be identical across
tables. Offline pooled accuracy is exactly one half for each queried address.
Also compare histories differing in one target bit, not only complements.

This four-bit enumeration is a reduced-model test, not exhaustive coverage of
the full 16-bit table or shared control state. The production-model requirement
is a complete finite-state inventory plus a compositional noninterference
argument: the reset constructs a fresh canonical agent/body and cancels every
old message or event; no old acquired object is retained or reachable; each
subsequent transition consumes only that state and target-independent inputs.
The one-way evaluator must not affect resources, outputs or scheduling.

Validate that argument against the production schema, with histories differing
at every one of the 16 cue bits, cross-block changes and deliberately populated
allocator/body/queue fields. Assert equality of every serialized allowed state
field and subsequent trajectory. Omitted fields or retained references fail
the gate. These finite tests support the structural argument, not a claim of
exhaustive proof over all histories. If the full state boundary cannot be
established, complete-loss validation remains incomplete regardless of chance
accuracy. Exhausting all 65,536 full target assignments is an optional stronger
test, not something established by the four-bit enumeration.

For 16-cue final individuals, report a seed-level 95% interval for forced-choice
accuracy and require it entirely within [0.45, 0.55], in addition to structural
noninterference. Insufficient precision is inconclusive, not proof of deletion.
Statistical deviation alone prompts investigation; reproducible target dependence
or a failed exact noninterference test invalidates the information-isolation claim.
Monitor the negative control with declared neutral power so dead slots cannot
produce artificial below-chance accuracy; report that support and all exclusions.

## 8. Relinquishment while remaining viable

Use a separate 512-tick feedback-enabled ecological phase after acquisition and
allocator development. Assignment usefulness is independent of the label. Expose
its current task yield identically to every controller. This is a visible change
in opportunity, not discovery of an unannounced inner need.

Randomly make eight cues obsolete, retaining eight useful cues with matched
presentation counts. Pair a continued-usefulness branch with the same prior
state, resources, cues and damage. Provide sufficient cue-independent food to
make selective abandonment feasible, but a fixed scarce material budget that
prevents maintaining every region without opportunity cost. Validate this
feasibility with scripted positive controls before final seeds, not by retuning
after final results.

Primary coding layout for this contrast retires whole four-cue blocks, randomly
choosing two of four. A mixed-usefulness-within-block condition is secondary;
report its shared-parity cost honestly. Measure spending on obsolete regions,
useful recall, total expenditure, active fraction and completion. Reduced
collection caused by starvation, global inactivity or forgetting everything fails.
Reduced spending is not evidence that a durable old bit was already erased.

Before branching, label the same eight retained cues U and eight devalued cues O
in every paired branch, including the continued-usefulness branch where O still
produces task returns. In the final 256 ecology ticks each of the 16 cues has
exactly 16 scheduled queries: 128 U queries and 128 O queries, in a paired
target-independent order. Define R_U as correct U responses divided by those
128 planned U queries, including zeroes after death. Compare R_U on the same U
set in both branches. This ecological endpoint is distinct from H1's 256-query
post-challenge R; it neither adds a new challenge nor uses a branch-dependent
denominator. Active fraction and completion use the whole ecological horizon.

Count O-region corrective writes in that same final window. Compare both with
the paired continued-usefulness reference and with tuned periodic scrubbing in
the devalued environment. Report total energy, reads, logic, transport, rent and
shared block charges separately. Fewer writes can coexist with more expensive
monitoring; the H2 gate supports reduced write-material expenditure only.

Correct answers may produce energy in ecology and may teach the association.
Label every ecological recovery result as potentially including relearning.
Do not combine it with the isolation endpoint to claim example-free repair.
Externally funded and sham-material ecology branches test resource responses;
all objective differences and support are reported.

## 9. Protected machinery and E3b boundary

The simulator, fixed decoder, fixed cue routing, generic update algorithm,
atomic-operation executor and experimenter clock remain protected. They are
independent of individual targets. Learned values used by the allocator are not
protected merely because the algorithm interpreting them is generic.

E3a is a finite-state memory/control benchmark. A common vulnerable storage pool
does not make it one neural organism. It has no self-produced boundary, inherited
rule reconstruction, free-form topology, life history without experimental
branches or theory-specific consciousness assessment.

E3b may replace this reference with a single quantized, materially vulnerable
neural substrate that generates both recall and maintenance decisions. It must
declare every learned input/readout/repair parameter and compare against E3a's
ordinary adaptive coding baseline. No E3b implementation is authorized by this
unfrozen specification, and no E3a success establishes the E3b claim.

## 10. Sample, endpoints and rejection rules

Candidate engineering individuals: initialization IDs 1-8, excluded from final
analysis. Candidate final sample: 32 independent individuals, IDs 300-331, each
with independently assigned labels. Eight common held-out opportunity/damage
panels per individual are repeated measures, not independent replications.
Keep initialization IDs distinct from secret target-generation streams.

Candidate allocator development: 2,048 planned ecological ticks, no replay;
all scheduled support/reset boundaries must be specified and logged before code.
Final sample size is a feasibility choice, not an effect-size power calculation.
Do not inspect final target tables or results during engineering. No seed removal
for failed acquisition, mortality or numerical difficulty.

Primary isolation retention endpoint $R$: correct responses divided by 256
planned post-challenge queries across all 16 acquired cues, all useful in H1.
Dead or missing slots count as failures. Also report
active-only recall, forced-choice accuracy where powered, completion, and physical
miscorrections. At least one offline probe must clear transient computation to
show that any benefit persists in stored information.

Average panels within independent individual. Bootstrap paired individual
vectors 10,000 times with a frozen analysis RNG. Report descriptive 95% percentile
intervals conditional on the panel, all individual vectors and paired differences.
No timestep-level inference, multiplicity-adjusted discovery claim or formal
equivalence between algorithms is implied.

| Gate                           | Prospective decision rule                                                  |
|--------------------------------|----------------------------------------------------------------------------|
| Information integrity          | All-state reset, interface isolation and resource ledgers pass exact tests  |
| Acquisition and feasibility    | Mean intact recall >= 0.90; mean active fraction >= 0.95                     |
| H1 maintenance                 | RL repetition R minus writes-disabled R >= 0.05; paired lower CI > 0        |
| H1 functional sufficiency      | RL repetition R >= 0.80; active fraction >= 0.90                            |
| Adaptive allocation increment  | RL minus tuned periodic R >= 0.05; paired lower CI > 0                      |
| H2 selective write expenditure | O writes fall >= 50% versus continued use; paired reduction lower CI > 0    |
| H2 fixed-policy comparison     | O writes fall >= 10% versus periodic in devalued ecology; lower CI > 0      |
| H2 viable useful retention     | R_U >= 0.80; ecological active >= 0.90; completion >= 0.90                   |
| H2 not blanket inactivity      | Upper paired CI for continued-use R_U minus devalued R_U <= 0.05            |
| Complete erasure               | Exact noninterference passes; powered accuracy CI within [0.45, 0.55]       |

For H2, average worlds within each individual before calculating absolute paired
O-write reductions. Calculate spending ratios from the aggregate individual
means for each comparator separately, not an average of individual ratios.
Retain individuals whose comparator writes are zero. If the aggregate reference
denominator is zero, that comparison is not evaluable and H2 cannot pass; do not
remove individuals or insert an epsilon. Predefine the endpoint window as the
final 256 ecology ticks. For H1, require at least one paid reconstruction write
and a positive post-challenge gain over no-write storage; trace agreement alone
is insufficient.

Report the block-code adaptive result regardless of which code wins. If ordinary
ECC plus RL explains performance, retain that explanation. Failure of adaptive
allocation does not negate a narrower paid-maintenance benefit that passes H1.
Failure of H1 means the proposed maintenance benefit is unsupported at this
budget/channel. Failure of acquisition is a failed prerequisite, not a reason
to select better individuals. If no-write performance is at ceiling, the frozen
advantage gate fails; redesign only in a new version with new final individuals.

Invalidate the isolation interpretation if an advantage requires answer feedback,
unbudgeted acquired state, a clean template, unequal damage information or a
reset that leaves target dependence. Stop, audit and version the experiment;
never promote such a result as regeneration of deleted information.

## Pre-implementation specification checklist

The ten conceptual questions above are answered, but the following operational
details remain deliberately unfrozen. Completing them is the next bounded task,
not permission to guess them inside an implementation.

* Specify every finite state field, capacity, quantization and canonical reset.
* Define allocator state bins, update equation, rounding, exploration and its
  own paid storage-refresh process; choose exact fixed-policy tuning grids.
* Define physical layout, transport distances, code placement, rent/hazard law,
  atomic operation ordering, decoder opcodes and partial-budget behavior.
* Fix all food/material yields, caps, initial reserves and support schedules,
  plus the exact code-only versus whole-substrate damage strata.
* Resolve H2 ecology reward units and acquisition-write ordering; ensure the
  block-code teaching buffer is paid and erased before isolation.
* Freeze the complete intervention Cartesian product, checkpoint schema,
  analysis formulas, exception policy and output row counts.
* Audit baseline algebra, all-state deletion and plausible resource feasibility;
  archive a design-only hash manifest before simulation code is written.

After implementation, use engineering seeds only. Record every result-motivated
change in a new versioned engineering log. A second freeze must hash sources,
configuration, tests, protocol and analysis before untouched final seeds run.
The runner must refuse existing result directories, record initial/final hashes
and runtime provenance, and support replay without training. Never repair an
old freeze by changing its recorded hashes.

## Required verification and interpretation

Before final execution, test copy-free input boundaries; finite precision;
known small-code distances; deterministic paired streams independent of action
counts; all-state erasure after actual acquisition; paid-write accounting;
overflow; sham/refill/oracle distinctions; frozen updates with vulnerable state;
continued wear without examples; complete planned-row retention after death;
independent evaluator clones; and full-state checkpoint replay.

Report exact replay separately from a predeclared numerical-tolerance check.
Integer state should support exact simulator-state equality; do not conflate it
with universal host-platform reproducibility. Raw result bytes and code manifests
are immutable once collected; new analyses get new destinations and labels.

A positive result establishes material-paid preservation or reconstruction of
acquired information under these controls. It does not establish information
recovery from nothing, subjective memory, intrinsic wanting, organizational
closure, life, consciousness, or originality.
