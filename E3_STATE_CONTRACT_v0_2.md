---
title: E3a finite-state and temporal contract
description: Pre-implementation refinement of acquired-state accounting, delayed queries, erasure, and analytical design constraints
ms.date: 2026-09-10
---

## Status and precedence

This is a versioned pre-implementation specification slice, not an executable
protocol, design freeze, implemented mechanism, or E3 result. It supplements
[E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md) without changing that historical
proposal. The selected refinements below replace its ambiguous state-lifetime
and query-timing choices for the next candidate version. Unresolved costs,
hazards, interventions, precision and production tests still prevent a freeze.

All execution state is managed through the .copilot-tracking folder files; see
the [continuation plan](.copilot-tracking/plans/2026-09-10/e3-specification-plan.md).
The [independent research note](.copilot-tracking/research/subagents/2026-09-10/e3-finite-state-exact-erasure.md)
contains alternatives, not additional selected commitments. Where its example
layout differs, the layout below is the selected candidate for this slice.

E3a remains conventional error correction plus ordinary resource allocation.
Its question is whether paid correction using surviving information improves
later retention without answer access. It does not instantiate E3b's single
developing neural substrate or establish a new source of motivation.

## Finite live state

Retain 16 independently assigned binary labels and 80 two-bit code cells. Neither
balanced labels nor a label-generation seed is available to the agent. Code
capacity is 160 bits, auxiliary persistent capacity 2,048 bits, and operation
scratch 256 bits: 2,464 allocated bits altogether. Only 2,208 bits survive an
operation boundary. Host objects are implementation vehicles, not extra storage.

The auxiliary offsets below are inclusive and relative to the start of the
auxiliary region. Fields are packed without alignment padding. Multibit integer
fields use least-significant-bit-first packing, with two's-complement signed
values. Within arrays, index zero comes first. No spare host-side values persist.

| Auxiliary offsets | Field                    | Allocation                         | Bits |
|-------------------|--------------------------|------------------------------------|------|
| 0-1535            | Q values                 | 32 observations x 3 actions x 16   | 1536 |
| 1536-1575         | Query ring               | Five eight-bit slots               | 40   |
| 1576-1607         | Teaching staging         | Four eight-bit blocks              | 32   |
| 1608-1639         | Previous transition      | One 32-bit record                  | 32   |
| 1640-1655         | Energy                   | One unsigned 16-bit quantity       | 16   |
| 1656-1687         | Material                 | Four unsigned eight-bit quantities | 32   |
| 1688-1767         | Upkeep ages              | Twenty unsigned four-bit ages      | 80   |
| 1768-1783         | Controller metadata      | Cursor, counter and three flags    | 16   |
| 1784-2047         | Inaccessible reserve     | No agent reads or writes           | 264  |

The used auxiliary allocation is 1,784 bits. The reserve is allocated capacity,
not permission to add a float, queue, visit counter, normalization statistic,
eligibility trace, or cached decoded word. Any new use requires a new version.
All competitors receive the same allowance and report unused capacity. No
replay, target network, optimizer moments, or protected learned Q copy exists.

### Code symbols and canonical values

Symbol encodings are 00 for zero, 01 for one, 10 for erased, and 11 for invalid.
Normal decoding treats invalid as erased; raw encoding remains part of the
state inventory. Every intentional erase writes exactly 10, never a validity
flag alongside a retained sign. A complete reset sets all 80 symbols to 10.
These 20 code bytes precede the 256 auxiliary bytes in boundary snapshots.

All auxiliary bits reset to zero, including invalid-slot payloads, Q, counters,
ages, resources, flags and reserve. This defines a blank, unpowered canonical
state. A subsequent target-independent support event supplies any neutral power
or material required by an assay. The amounts must be fixed under blocker B03;
they are not values copied from the developed body. A death flag of zero does
not guarantee that the next step is affordable.

Code-only lesions and complete erasure are distinct. Zeroing an unreplicated
Q word is an information-losing intervention; refreshing it merely reaffirms
the current value and may reduce subsequent hazard. Refresh cannot recover its
old value without an additional, budgeted surviving copy.

### Persistent records and lifetimes

Each query slot stores valid:1, cue:4, and reserved:3, in that order. It stores
no predicted answer, correctness bit, usefulness history, or clean codeword.
The slot remains persistent through the five-tick delay, is cleared when drained,
and is overwritten only by the next scheduled admission. Faults in valid/cue
fields can lose or misroute a query. The external scorer retains the originally
scheduled cue; it does not correct the damaged address for the agent.

Each teaching block stores four label bits followed by four validity bits.
The buffer is acquired memory even while incomplete. It is costed, vulnerable,
and cleared after that block's teaching opportunity and before every isolation
boundary. Validity means the current stored flag, not authenticated lesson
receipt or uncorrupted label content. Faults can create false acceptance or
rejection and undetectably wrong labels. No clean success bitmap is available.
No delayed host callback can resend a failed lesson.

The previous-transition record stores valid:1, observation:5, action:2,
reward:16 signed, terminal:1, and reserved:7. Reward is the return received in
that transition's tick, not an answer reward retrospectively attached to its
query-admission action. This selects ordinary one-step temporal-difference
learning, not a five-record delayed-credit scheme. No other transition survives.

Metadata stores a five-bit service cursor, eight-bit periodic counter, then
dead, acquisition-failed and operation-failed flags. Normal cursor values are
0-19; an invalid corrupted value causes the next cursor-using operation to fail,
not out-of-range access or restoration from a clean copy. Action encoding 3 is
invalid and cannot produce a resource gain. Costed failure semantics remain B02.
Upkeep ages are pooled-domain ages, not 80 independent code-cell clocks.
Their physical membership and normal update rules remain B03.

### Operation scratch

Scratch is 96 bits for decoding, 128 for integer arithmetic, and 32 for local
addressing/control. It is cleared after each atomic operation and at every
checkpoint, isolation and erasure boundary. It cannot hold a delayed query,
partial lesson, partial repair, learner transition or hidden fractional residue
across those boundaries. Atomic scratch is protected from mid-operation faults;
that is a declared generic-executor simplification shared by all arms, not
fault-tolerant hardware or organizational autonomy.

A block decoder can stream its 16 generic candidate codewords: 40 bits for the
20 observed symbols, one four-bit candidate, one four-bit best candidate, and
bounded mismatch/best-distance/tie counters fit within 96 bits. The generator
is inherited and independent of the acquired target. There is no 16-word
individual-specific decoded cache. This capacity argument is not a verified
opcode implementation or a claim that decoding is affordable.

## Observation and learner contract

Use 32 observation bins: current offered cue usefulness (two values), energy
status (two), local material status (two), and observed storage health (four).
Index the table as 16u + 8e + 4p + h. Energy/material thresholds and observation
costs remain B02/B03. The selected bins can alias distinct physical states;
they do not make the process fully observed or guarantee Q-learning convergence.

Health means empty, ambiguous decode, fully agreeing intact decode, or unique
decode with disagreement/erasure. It comes only from paid reads of the current
representation, never true distance to the target. In the primary H2, usefulness
changes for whole blocks. Mixed-usefulness blocks remain a separately reported
secondary condition, not extra information in the main controller.

Select a conservative live-write rule for both representations. Repetition
abstains on empty or tied votes. Block decoding minimizes disagreements over
currently observed binary symbols, ignoring erased/invalid symbols; it abstains
when there are no observations or more than one minimizing codeword. Only a
unique decoded value may guide corrective writes, and it can still be wrong.
This supersedes v0.1's random block-tie rule for live correction. Forced-choice
probe guessing remains readout-only and never seeds a repair. Record unique-but-
wrong decoding and resulting miscorrections offline, without truth feedback.
The cost of scanning and abstaining still belongs in B02.

Three actions are forage, collect local material, and scrub the offered memory
unit. The fixed routing maps a cue to its repetition group or four-cue block.
Full scans, decoding, decision work, scratch use, bookkeeping, Q reads/writes
and routing must be charged; no simulator-computed free health statistic exists.
Insufficient resources cannot trigger an uncharged observation/decision pass.
The exact preflight, failure, fallback and partial-operation sequence is B02.

Candidate Q values are signed 16-bit integers representing multiples of 1/256.
The discount is 15/16, learning rate 1/8, and exploration probability 1/16.
Uniform action/tie choices use external target-independent indexed inputs;
there is no persistent local PRNG or action-count-dependent shared cursor.

Let q be the stored old value, r a signed fixed-point return clipped to
[-256, 256], and m the maximum permitted successor Q value, or zero when the
stored transition is terminal. The selected quantized update is:

$$
q' = \operatorname{sat}_{16}\left(q +
\operatorname{roundEven}\left(\frac{16r+15m-16q}{128}\right)\right).
$$

Round ties to the nearest even integer, then saturate to [-32768, 32767].
Do not keep a fractional accumulator. If r is bounded as above, the ideal
unclipped discounted-return bound is 4096 stored units, inside the 16-bit range;
corruption can still place any word near saturation. Four 32-bit scratch
registers suffice for this expression's arithmetic, not for uncounted temporaries.
Quantization may stall sufficiently small updates and must be tested later.

The exact mapping from task/resource returns and costs to r is still B04.
Clip the currently stored reward when it is consumed too; a corrupted reward
word must not bypass the declared bound. Read current Q values, not old copies.
No reward is supplied for matching an experimenter-desired repair pattern.
At tick t, a charged observation may supply the successor state for the record
from tick t-1; the record is updated/cleared before another is stored. Terminal
flush, unaffordable update and failure handling require the common B02 ordering.
Any observation/action/return needed across atomic operations must live in this
one record, be recomputed with charged reads, or be consumed within one bounded
atomic operation. No second tuple persists in host locals while it is occupied.
Freeze updates throughout isolation and post-challenge testing, clearing the
transition record on entry. Frozen updates do not protect live Q from damage.

## Delayed-query semantics and planned denominators

Select pipelined queries rather than globally blank serialized trials. A cue
admitted at tick t is due at t+5, with four intervening ticks. Other cues can
arrive during that delay. The task tests a declared vulnerable address pipeline,
not a learned recurrent memory of a globally blank interval. This explicitly
narrows the original ambiguous phrase "four blank ticks."

At most five addresses are outstanding at a boundary. Tick t drains ring slot
(t-1) modulo 5 before inserting that tick's new admission in the same slot.
The generic clock and due-slot rule are protected and target-independent; the
address and valid bit are not. A response uses only the stored address. Current
time cannot be used to regenerate an old cue from an externally known schedule.
The input packet contains only the optional current admission, a separate current
maintenance offer, and declared resource/noise inputs, not the scheduled due cue.
Neither historical/future schedule lookup nor its reconstruction seed is readable.
The schedule is not a public deterministic cue cycle that bypasses the latch.

Supply one maintenance offer with advertised usefulness on every live tick in
development, H2, and isolated recovery, including drain-only ticks. On admission
ticks it equals that admission; otherwise it comes from a separate paired,
target-independent B05 schedule, never a due cue or a retained previous offer.
Offers are current external inputs, not additional persistent state. During
recovery they are addresses/usefulness only, not teaching examples or answers.
This keeps allocation available during all five final H2 spending ticks.
H1 post-challenge evaluation is response/upkeep-only: it requests no allocator
decision and supplies no maintenance offer throughout all 261 ticks. Absence is
not a seventeenth cue or new observation bin. B02 still charges responses,
upkeep and bookkeeping, and B03 fixes support for each of these tick types.

Consume/decode/emit a due response while its address remains in its slot; retire
the slot before reuse. B02 must prevent failed responses from surviving for an
unscheduled retry and must account for every intermediate value across any
interleaved operations. Five slots suffice only under this lifetime contract.

Live ecological correctness is evaluated outside the agent and returns only
the declared scalar task yield during that same response tick. This is still
an answer channel and can support relearning. Isolation supplies no such return,
including delayed rewards, resource consequences or outcome-dependent stopping.
The full tick ordering of this return relative to costs and learning is B02.

### H1 post-challenge evaluation

Admit 256 queries at ticks 1-256 and score responses at ticks 6-261. Each cue
occurs 16 times. The five warm-up ticks are real elapsed time; include their
living, rent, wear and routing costs. All 261 ticks enter active-fraction and
completion accounting. The recall denominator remains 256 planned responses.

Corrective code writes and Q updates are disabled, not every physical state
write: query routing, energy accounting and other declared bookkeeping continue
and are costed. No decoded answer is written into the live code bank. Damage
and upkeep continue during evaluation under a still-to-be-fixed B03 law. Do not
use the single-challenge algebra below as a prediction of this wearing assay.

### H2 feedback ecology

Retain the 512-tick horizon, common U/O assignments before branching, and final
256-tick spending window. The scored responses occur at ticks 257-512; their
admissions occur at ticks 252-507. Each of the 16 cues has 16 scored responses,
giving exactly 128 U and 128 O responses. The first five admissions associated
with that endpoint precede the spending window; report that asymmetry explicitly.

Admit other queries at ticks 1-251, with responses at 6-256. Their schedule is
target-independent and paired, but is not part of the final-window R_U endpoint.
There are 507 planned responses over the whole ecology. Admit none at 508-512;
drain the pipeline rather than dropping pending scored queries or extending the
survival horizon. Whole-horizon active fraction and completion use all 512 ticks.
The continued-usefulness branch uses the same U labels for its R_U denominator.

Compare the emitted bit with the target of the originally scheduled cue.
Missing/invalid responses and incorrect bits score zero. A wrong stored address
can yield the correct bit by coincidence; that bit counts as correct for binary
recall, while the routing error is reported separately. Never reduce the
denominator using surviving slots. Task yield uses the scheduled cue and its
usefulness at response time, not the current offer or corrupted address. A
spurious output without a planned due query creates neither yield nor an extra
scored row. The due cue and routing-integrity flag remain outside the worker;
only the declared scalar ecological return enters. H1 supplies no such return.
Within-cue schedules, paired noise streams and early-window counts are B05.

### Acquisition and development boundaries

Order the 256 acquisition presentations as 16 passes over four blocks, each
containing four cue lessons. Repetition has five code-write attempts per lesson;
block coding has one 20-symbol commit opportunity after its four lessons.
Successful full encoding therefore uses 1,280 code-symbol writes for either
representation, excluding staging, validity and every other charged operation.

Staging writes are additional, not free parity information. At its scheduled
opportunity the block commit tests only that all four stored validity bits are
one. It cannot detect all missing lessons or corrupted labels, and a false
acceptance may encode a wrong word. No evaluator integrity check is supplied.
Retire all eight staging bits after each scheduled opportunity, even if a commit
fails. Mandatory clearing must be paid; if unaffordable, B02 must prescribe
retirement/termination or a declared boundary intervention rather than a free
write or hidden retry. The next scheduled teaching pass is a new explicit
example opportunity. Freeze transfer and failure ordering before coding.
Acquisition need not succeed under arbitrary budgets.

For the candidate 2,048-tick development period, admit queries at 1-2043 and
drain responses at 6-2048. There are 2,043 planned responses, not 2,048 completed
delayed queries. Clear pipeline, staging, transition and scratch at the isolation
boundary. No delayed evaluator message, reward or suspended operation survives.
Checkpoint the declared developed state before constructing intervention clones.

## Erasure, physical faults and serialization

Complete erasure constructs a new canonical code/auxiliary state. It does not
mutate a small subset of an object graph and assume the rest is irrelevant.
Cancel every old event, release all references into the acquired worker state,
and restart future input indexing at a public target-independent phase boundary.
Snapshot/score/log objects never return to the recovery worker.

The reset must satisfy Reset(history, G) = S0(G) for every acquired history,
where G is the inherited generic contract. After reset, the induction step is
S(t+1) = F(G, S(t), Z(t)) with no key, target, old resource history, old cursor,
file, callback, closure or evaluator object among F's reachable inputs. Identical
future Z gives identical states and predictions. This is a design argument;
only implementation inspection and production-schema tests can establish that
the actual F obeys it.

Index future randomness by public phase, absolute tick, purpose and physical
location/slot, not number of actions taken. Pair allowed noise/opportunities
across branches. Do not derive these inputs from the target-generator seed or
expose a public run ID from which the target can be reconstructed. Unused random
inputs do not shift subsequent draws. No future schedule conditioned on past
answer-dependent resource collection is permissible after complete reset.

Physical E/P quantities can encode acquired history, so canonicalize them on
complete reset. In whole-substrate injury, use explicit resource losses/sinks,
not register XOR that creates energy or material by flipping a high bit. If a
corruptible resource sensor is later added, budget it separately from the
physical quantity. Log intervention removal/refill separately from ordinary
agent spending. Exact location-to-field mapping and hazard exposure are B03.

Boundary checkpoints contain all 276 persistent bytes, including inaccessible
reserve and invalid encodings, plus only inherited format identification outside
the worker. Scratch must be zero and no operation may be suspended. A checksum
is archival integrity metadata, not an answer-dependent sensor available to the
agent or an automatic restoration mechanism during simulation. Checkpoints and
offline clones are never repair sources.

Production tests must cover acquisition-to-reset histories differing at each
of the 16 labels, cross-block changes, populated Q/staging/transition/metadata,
resource distributions, invalid slots, reserved bits, and outstanding messages.
Assert byte equality after reset and equality of every subsequent trajectory
under common inputs. Missing fields or retained references fail the gate.
Four-bit exhaustive enumeration remains a component test, not this proof.

## Analytical constraints checked before implementation

These calculations are design checks, not experiments or E3 performance results.
They do not select final outcomes, alter old gates, or establish resource
feasibility. No E3 simulator was run.

### Retention headroom

With only one independent flip challenge at p = 0.1, three initially correct
replicas yield accuracy 0.972; five yield 0.99144. Rebuilding two missing replicas
therefore supplies 0.01944 expected gain in that idealized comparison, below
the proposed five-percentage-point H1 gate. The subsequent recovery wear is
important, not an optional detail that can be added after observing results.

For 128 ticks of independent reversible flips at h = 0.001, an unrepaired
occupied symbol has odd-flip probability:

$$
q = \frac{1-(1-2h)^{128}}2 = 0.11302822537825702.
$$

After the independent p = 0.1 challenge, its effective flip probability is
p + q - 2pq = 0.19042258030260562. Three-copy accuracy is then
0.9050274573516492. Comparing it with hypothetically perfectly restored five-copy
storage immediately before the challenge gives optimistic headroom
0.08641254264835074. A real scrubber can miscorrect and may lack resources;
query-period wear and unequal costs are absent from this calculation.

The separate five-point adaptive-over-periodic gate needs its own headroom
check. A tuned periodic baseline near ceiling may defeat that gate even when
paid maintenance strongly outperforms no-write storage. This supports keeping
the conventional explanation, not weakening a threshold after final data.

### Complete-erasure precision

With one fixed answer per cue repeated across panels, 32 independent individuals
and 16 independent labels give illustrative normal 95% half-width
1.96 sqrt(0.25 / 512) = 0.043310290347676035. Containment in [0.45, 0.55]
then requires the point estimate to be much nearer 0.5 than that half-width.
This is not high assurance of a pass, even with structurally exact deletion.

Fresh independent fair guesses at every forced response would instead give
illustrative half-width 0.003828125 across 32 x 8 x 256 responses. That assumption
is stronger than erasure alone: outputs arising from surviving/generated state
need not be independent fair guesses. Actual forced-guess indexing, support,
post-reset hazards and repetitions must be fixed before choosing sample precision.
Artificially balanced outputs can force chance without proving information loss.

Keep individual-level panel aggregation and paired bootstrap inference. The
normal approximations are sensitivity checks, not substitutes for the proposed
bootstrap or justification of the final sample. An imprecise chance interval
is inconclusive, while reproducible target dependence fails isolation. B06
requires prospective containment assurance, not outcome-dependent sample growth.

### Minimum operation and living costs

Rebuilding two lost layers of 16 replicas requires at least 32 symbol writes and
32 material units. Under the prospective coefficient of four energy units per
write, that is 128 write-energy units before reads, logic, transport or control.
At 16 living units per tick, 128 recovery plus 261 query ticks require 6,224
living units before every other charge. Equal code-bank capacity does not make
a full block decoder equally cheap, nor does lower write count imply lower
total energy use. These are lower bounds, not affordable-budget demonstrations.

## Remaining design-freeze blockers in execution order

1. B02: Specify opcode-level reads, writes, logic, transport, scratch clearing,
   storage rent and bookkeeping costs; exact tick order; affordable preflight;
   failed/partial operation, terminal update and dead-row semantics. Cost the
   streaming block decoder and the selected tied/empty abstention rules.
   Forced-choice probe guesses remain non-writing; ties cannot silently become
   learned values. Prevent recursive ledger charges with a declared finite
   bookkeeping convention, not an uncharged extra storage channel.
2. B03: Map physical locations and the 20 upkeep domains onto every field; set
   rent, lapse, flips, erasures and correlated losses; distinguish code-only
   and whole-substrate strata. Fix yields, caps, reserves, neutral support and
   query-period wear. Prove resource conservation under type-specific faults.
3. B04: Set paid observation thresholds, reward units/normalization, learning
   and policy-refresh timing, exploration stream mapping, and fixed-policy
   tuning grids. Give conventional rivals matched permitted information and
   development opportunity. Check quantized arithmetic and saturation cases.
4. B05: Freeze complete branch/arm/channel products, all schedules, panel
   pairing, seed streams, exact checkpoint/row formats and expected row counts.
   Retain fixed H2 U/O populations, 128 U responses, zero-reference individuals,
   aggregate ratio rules, and the useful-recall-loss bound.
5. B06: Justify H1/adaptive headroom, H2 viable selective spending and positive
   reference denominators, and complete-erasure precision under actual output
   dependence. Keep existing proposed gates unless a new version records a
   prospective reason for changing them before final outcomes exist.
6. B07: Complete the production noninterference and interface review, source
   access caveats relevant to adopted mechanisms, and a full operational review.
   Only then create a design-only hash manifest. No production proof/tests,
   E3 code, engineering individual or final run is supplied by this slice.

B01, the finite field/lifetime inventory and temporal interpretation, is
specified as a candidate in this version. Its implementation validation is
pending, and its physical/cost dependencies above remain blockers. A later
source/configuration/test/analysis freeze is still required after authorized
engineering and before untouched final individuals. Do not overwrite either
historical evidence or this version to make an old freeze pass.
