---
title: E3 finite-state and exact-erasure specification review
description: Pre-code review of storage budgets, delayed queries, reset semantics, and analytic feasibility
ms.date: 2026-09-10
---

## Scope and status

Complete. Specification research only; no E3 implementation, simulation,
final-seed access, or changes to protocols or historical artifacts. This separate
research-mode tracking note is the only file created or edited by this research.

## Questions

* Can 80 two-bit code symbols, 2,048 persistent auxiliary bits, and 256
  operation-scratch bits support ordinary finite tabular RL without hidden state?
* Which acquisition, delayed-routing, reward/TD, and resource fields survive
  atomic operations?
* Can four blank ticks coexist with one query per tick and H2's 128 useful slots?
* What reset noninterference and code-only versus whole-substrate semantics are
  required for Q values and physical resources?
* Which analytic bounds most strongly challenge complete-erasure CI precision,
  H1's five-versus-three replica comparison, and physical feasibility?

## Sources

* E3_PROTOCOL_v0_1.md, sections 1-10 and pre-implementation checklist
* E3_RESEARCH_HANDOFF_v0_1.md, current decision and new scientific constraints

## Findings

### Prioritized assessment

1. P0, conceptual distinction: transient lifetime does not imply operation
   scratch. Anything surviving an atomic operation needs persistent allocation,
   or an explicitly different scratch-lifetime contract with the same total
   capacity accounting. Cue pipelines, partial teaching blocks, delayed TD
   records, and maintenance histories cannot disappear after each operation.
   The protocol distinguishes operation-cleared work from boundary-cleared delay
   state but puts both under scratch; this requires resolution, not a claim that
   an implementation already violates it.
2. P0, conditional scheduling inconsistency: four globally blank input ticks
   between cue and request cannot coexist with a new cue each tick on the same
   channel. Pipelining changes the blank condition to a per-query condition.
   Whether ecology even uses the delayed assay remains unspecified.
3. P0, freeze blocker: the all-state reset requirement is conceptually sound,
   but needs fieldwise canonical values, ownership, future-event cancellation,
   and physical fault semantics. Canonical Q without canonical resources and
   histories is not complete erasure.
4. P1, feasibility blocker: 5% H1 advantage cannot come from clean five-versus-three
   majority voting at p=0.1 alone. Ongoing wear can provide additional headroom;
   declaring the full protocol mathematically impossible would also be wrong.
5. P1, precision blocker: a 32-individual chance interval can have adequate width
   when centered exactly at chance but a low probability of lying wholly inside
   the required band. Repeated deterministic answers do not create fresh labels.

Anchors: E3_PROTOCOL_v0_1.md:60-63, 78-100, 219-229, 280-286, 310-318,
350-388, 413-431; E3_RESEARCH_HANDOFF_v0_1.md:73-92, 116-123.

### A concrete candidate capacity witness

This is a proposed layout, not a freeze or proof of resource feasibility.
All arms receive the same capacity. Unused fields are canonical and inaccessible
as an undeclared extension to code storage.

* Code bank, separate from auxiliary allowance: 160 bits; 80 two-bit symbols,
  canonical erased symbol 10
* Learned Q: 1,536 bits; 32 observation bins x three actions x signed 16 bits
* Delayed TD records: 160 bits; five 32-bit records
* Delayed cue pipeline: 25 bits; five stages of four-bit address plus valid bit
* Acquisition staging: 32 bits; four blocks of four labels plus four validity bits
* Physical resources: 48 bits; unsigned 16-bit energy and four eight-bit material
  quantities
* Upkeep history: 80 bits; twenty four-bit saturating spatial-domain lapse ages
* Controller metadata: 16 bits; five-bit cursor, eight-bit countdown, three flags
* Unused auxiliary allocation: 151 bits; canonical zero, not agent-addressable
* Auxiliary total: 2,048 bits; 1,897 used plus 151 reserve

The metadata failure flags can mean terminal death, malformed metadata, and
queue overflow. Service cursor encodings 20-31 need a fixed fail-safe rule.
These flags are not an excuse to discard an individual. Invalid-state behavior
is part of the experiment, with planned failures retained.

Suggested Q observation bins: usefulness 2 x energy 2 x material 2 x current
code-health 4 = 32. Thresholds and code-specific health mappings remain choices.
Use the offered association/block, not an address-indexed answer table. Every
read used to calculate health is charged; an externally supplied syndrome would
be an extra information/computation subsidy. Three actions remain forage,
collect material, and scrub. This is conventional tabular Q learning on possibly
aliased observations, not a claim that these bins make the full ecology Markov.

Each TD record can hold valid 1, old state 5, action 2, successor state 5,
terminal 1, signed accumulated reward 16, successor-valid 1, reward-valid 1.
Five slots require a declared maximum of five outstanding fixed-latency
transitions at one admission per tick. Store the actual successor observation,
not the observation at reward-delivery time. Use current Q values when applying
the delayed update. Longer or unbounded reward latency does not fit this layout
without another allocation. A simpler alternative is ordinary one-step learning
from resource returns received this tick; then only one pending transition is
needed. These alternatives have different temporal-credit semantics.

The four acquisition buffers support interleaving of blocks. Freeze a schedule
with one presentation of each constituent cue per teaching batch before commit.
Commit the 20-symbol codeword only when all four labels are available. A partial
buffer is persistent acquired information, with paid storage and writes, and
is cleared at isolation. Insufficient resources must not prompt unbudgeted
teaching replay or an external retained clean word. If each complete teaching
batch rewrites the full code bank, 16 presentations per cue imply 64 block
commits x 20 = 1,280 code-symbol writes, equal to 256 repetition presentations
x 5. Block staging and validity writes are additional costs, not free parity.
If unchanged symbols are not rewritten, that is a different acquisition-cost rule.

An explicit 256-bit operation-scratch witness:

* Decoder, 96 bits: 40-bit snapshot, 20-bit candidate word, four-bit best payload,
  four five-bit fields for candidate index/distance/best distance/tie count,
  two three-bit repetition counts, five-bit erasure count, one status bit
* Arithmetic, 128 bits: four 32-bit integer registers reused between decoder
  and TD stages
* Local addressing/control, 32 bits: seven-bit cell address, two-bit block
  address, two-bit action, 16-bit bounded cost, five-bit loop index

The decoder streams over codewords, retains no list of all candidates, and can
resolve ties by reservoir selection with independent indexed random inputs.
Intermediate cost overflow must be detected in the wider arithmetic registers.
No decoded payload, old Q copy, gradient residue, or work queue survives an
operation. An unfinished multistep repair would need separate persistent
allocation and would change this witness.

Twenty lapse domains assume pooled spatial upkeep, not an independent age for
every bit or cell. Eighty code-cell ages alone at four bits cost 320 bits; the
proposed 80-bit pooled history cannot be described as equivalent. Q storage,
auxiliary fields, code cells, and resource reservoirs need a fixed placement and
type-specific hazard map. The layout is not a conservation argument.

Anchors: E3_PROTOCOL_v0_1.md:70-100, 137-162, 181-204, 419-427.

### Timing and endpoint alternatives

Under a literal four-blank-tick convention, a cue at t is followed by blanks
at t+1 through t+4 and an answer request at t+5. Drain the due stage before
admitting the new cue; five pipeline stages suffice at tick boundaries. Different
within-tick ordering can temporarily require a sixth slot and must not hide it
in host state. Store only the address, not an early decoded answer.

Two compatible specifications are available, but they are different tasks:

* Keep globally blank ticks and serialize trials. A six-tick trial permits only
  42 complete queries in 256 ticks, not 256 queries or 128 useful queries.
  A balanced 256-query window would require 1,536 ticks under this convention.
* Keep the fixed H2 response count and use a multiplexed delayed-address task.
  Other cues appear during an outstanding query's delay, so the global input is
  not blank. Declare this explicitly and charge the persistent pipeline.

For H2 ecology numbered 1-512, define the scored window by response ticks
257-512. Cue admissions 252-507 then yield exactly 256 scored responses,
including 128 U responses, without extending the ecological horizon. The first
five admissions occur before the scored-write window. Do not count pending
admissions at the end as answered queries, drop them from the denominator, or
provide free post-horizon survival. The required per-cue balance applies to
responses under this alternative. If H2 instead uses immediate queries, state
that it differs from the delayed H1 assay.

H1 also needs a boundary convention. After a challenge, 256 admissions require
five warm-up ticks before all 256 delayed responses finish. Specify whether
wear, rent, paid reads, and neutral support continue during those ticks and
during the query block. The challenge-only binomial calculation below is not
the full prediction if damage continues while querying.

Writes-disabled cannot mean that no mutable agent field may ever be written:
cue routing, resource accounting, and TD bookkeeping need updates. Define
disabled corrective code writes separately from permitted, paid control/body
updates and from Q refresh. Atomic ledger bookkeeping must have a closed cost
convention rather than recursively charging for bookkeeping its own charge.

Anchors: E3_PROTOCOL_v0_1.md:60-63, 89-94, 206-225, 310-327, 364-369.

### Exact reset and physical fault domains

Use a structural reset requirement stronger than merely sampling a
target-independent marginal state. For every acquired history h and fixed
public configuration G, the reset produces the same canonical serialized state
S0(G). Given identical allowed future streams, every later state and output
must then be equal by induction on the protected transition function.

Reset code to a unique erased representation, Q to a fixed inherited default,
all queue data and valid bits to zero, partial teaching values and masks to
zero, upkeep ages and service counters to declared constants, and physical
energy/material to the same per-location reserves. Clear unused bits too.
In particular, setting an erasure flag while preserving the former low sign bit
as 10 versus 11 is not complete deletion merely because the decoder treats both
as erased. Raw reachable state must not retain the sign.

All old reward callbacks, messages, iterators, suspended computations, closures,
and external event handles must be canceled. Future external streams may remain
outside the allowance only when their keys, cursors, scheduling, and access are
target-independent. An action-count-advanced PRNG cursor or a pending correctness
reward is not such a stream. Use fixed public phase/tick/purpose/slot keys,
independent of previous target-conditioned action counts. Checkpoint/log output
is one-way; neither evaluator state nor an original object may be reachable.

The four-bit exhaustive history comparison in the protocol is a reduced test.
The production claim needs the inventory, ownership argument, and transition
induction. One-bit and cross-block counterfactual checks after real acquisition
are supporting checks, not exhaustive proof. If exact erasure cannot be
established, chance accuracy does not rescue the claim.

Keep three fault/reset cases distinct:

* Code-bank-only challenge: Q/control are not challenged but retain declared
  background wear and costs. Body laws continue; no undeclared refill occurs.
* Whole-substrate challenge: Q, queue, metadata and code share the spatial event
  with type-specific effects. Reservoir losses/support enter physical ledgers;
  corrupted metadata has deterministic bounded behavior.
* Complete erasure: every learned/history-dependent field, including frozen Q,
  becomes canonical. Per-location reserves and ages are canonical too, with
  removals/refills booked as reset interventions.

Frozen Q updates do not protect stored Q bits. Paid refresh may lower lapse
hazard, but it cannot reconstruct a corrupted learned value without surviving
redundancy that is also allocated. Copying the value currently present can
preserve an already wrong value. No clean table or learned prior may be restored
by the generic update algorithm.

Do not XOR physical reservoir quantities as if they were untrusted digital
registers unless a separate measurement-register model is intended. Flipping a
high bit of E or P can create resources. A physical damage event should specify
losses and sinks, such as E'=max(0,E-loss), with reset support separately booked.
If sensors are corruptible, their registers are additional finite state and
must not be confused with the underlying physical quantity. Merely retaining
different energy/material distributions after canonicalizing Q fails all-state
erasure because ecological correctness can have shaped those distributions.

Anchors: E3_PROTOCOL_v0_1.md:72-100, 104-124, 139-161, 219-225,
239-286, 329-337; E3_RESEARCH_HANDOFF_v0_1.md:73-90.

### Analytic H1 bounds

Assume intact correct copies immediately before a single independent p=0.1
challenge, perfect funding/response completion, majority decoding, and no
additional query-period wear. Then:

$$
A_3(p)=1-3p^2+2p^3,\qquad
A_5(p)=1-10p^3+15p^4-6p^5.
$$

At p=0.1, A3=0.972 and A5=0.99144, an advantage of 0.01944. Therefore pure
restoration from three clean copies to five cannot alone clear the 0.05 gate.
Repeated querying does not raise the expected difference. In the same ideal
model the maximum over 0<=p<=0.5 is 3/(25 sqrt(5))=0.0536656, at
p=(1-1/sqrt(5))/2=0.276393. At p=0.25 the difference is 0.052734375 and
A5=0.896484375; changing p would change the proposed protocol, not validate it.

The protocol also specifies 128 ticks of independent flip hazard h=0.001 under
fully paid upkeep. If unrepaired surviving copies undergo reversible flips
throughout recovery, their pre-challenge odd-flip probability is
q=(1-(1-2h)^128)/2=0.1130282254. After the challenge their effective error
probability is 0.1+0.8q=0.1904225803, giving A3=0.9050274574. A hypothetical
perfectly repaired five-copy endpoint would give a gain of 0.0864125426.
This is an optimistic comparison, not a prediction for a real scrub schedule:
mistaken majorities, timing, ongoing wear, exhausted budgets, Q damage, and
query-period wear can all change it. The retained p=0.1 design is thus not
analytically impossible on the information currently specified.

The additional 0.05 adaptive-over-periodic gate requires a separate headroom
check. A well-funded tuned periodic schedule might already approach the
five-copy ceiling; proving that repair helps passive storage says nothing about
whether RL can beat that schedule by another five points. Distinguish physical
recall gains from differences in powered response completion in R.

For the block code, minimum distance 10 ensures unique decoding after eight
erasures without other errors, but its remaining distance is only guaranteed
to be at least 2. The condition 2e+s<10 does not guarantee correction of even
one unknown flip when s=8. Enumerate the 16 words, 120 pairwise distances, and
all relevant puncturings for the exact layer placement before selecting costs
or claiming relative performance. Under symmetric faults, exact majority-state
recurrences or finite codeword/error enumeration can provide stronger pre-code
bounds than a proposed Monte Carlo run.

Anchors: E3_PROTOCOL_v0_1.md:193-204, 219-229, 364-388, 398-407.

### Complete-erasure CI precision

Consider the legitimate worst-repeat case where, after a canonical reset, each
cue receives one fixed answer repeated through all queries and panels. Each
individual supplies 16 independent fair target bits, not 256 fresh answers or
eight new target tables. With n=32 independent individuals:

$$
\operatorname{SD}(A_i)=0.125,\qquad
\operatorname{SE}(\bar A)=\sqrt{0.25/(32\cdot16)}=0.0220971.
$$

A normal 95% half-width is 0.0433095, or about 0.0450673 using t31 as another
rough illustration. To fit the normal interval wholly within [0.45,0.55], the
observed center must be within only 0.0066905 of 0.5. A fixed-variance normal
approximation gives approximately 24% containment probability under exact
deletion, not 95%; the analogous t-width illustration is approximately 18%.
These are design approximations, not computed properties of the proposed
10,000-resample percentile bootstrap. Its small-cluster and discrete behavior
needs separate prospective calibration.

For 16 cues, let a_c be the fraction of the actual, label-independent reset
outputs that answer one for cue c across the scored repeats/panels. Conditional
on these predictions:

$$
\operatorname{Var}(A_i\mid a)
=\frac{1}{16^2}\sum_{c=1}^{16}(a_c-1/2)^2.
$$

Repeating one answer gives the maximum variance 1/64. Fresh independent random
answers can reduce variance, so it is not correct to say repetitions never
help. But forcing balanced guesses or bypassing the actual decoder can make a
chance-accuracy gate vacuous. Exact noninterference remains the decisive
information-boundary test. Continue to average panels within individual and
resample individual vectors, never query rows as independent experimental units.

The protocol already proposes pre-drawn random tie guesses. Their granularity
therefore matters: if all complete-erasure responses use genuinely independent
fair draws across 32 individuals, eight panels, and 256 queries, an illustrative
normal half-width is 1.96/(2*sqrt(32*8*256))=0.00383. This does not apply when
one answer is reused, when panels reuse randomness, or when the process changes
the actual decoder to manufacture balanced outputs. The low-containment example
is a warning against an unspecified repeat model, not proof that the proposed
32-individual sample necessarily lacks precision.

With deterministic per-cue guesses, normal planning for a 0.05 containment band
at true chance gives n approximately ((1.96+z_(1-beta/2))*0.125/0.05)^2 for
containment probability 1-beta. Approximate requirements are 66 individuals for
80%, 82 for 90%, and 97 for 95%, before small-sample/bootstrap allowances. These
are design alternatives, not a chosen sample, seed allocation, or authorization
to increase sample size after observing outcomes.

Anchors: E3_PROTOCOL_v0_1.md:255-286, 350-375, 388;
E3_RESEARCH_HANDOFF_v0_1.md:82-92.

### Resource and numerical feasibility obligations

* Check capacity separately from physical cost. At least 16 initial repetition
  scrubs and 32 replacement-symbol writes are needed to refill two erased layers.
  This requires at least 32 material units and 128 write-energy units before
  decoder, transport, upkeep, and living charges. Baseline living alone costs
  2,048 units for recovery and another 4,096 for 256 query ticks, before delay
  warm-up. Whether erasure reclamation yields material must be declared.
* Account for allocator storage rather than treating 1,536 Q bits as free.
  The unit of auxiliary refresh/write cost, occupied storage rent, mandatory
  body upkeep, and failed attempts must be fixed. An automatic paid Q refresh
  service is one conventional choice consistent with retaining the three
  allocator actions; a protected learned table is not.
* A straightforward streaming block decoder reads 20 symbols into scratch and
  evaluates 16 candidate words of length 20. Freeze the primitive operation
  definition, candidate generation, comparisons, distance accumulation, and
  tie costs. Do not equate simulator wall-clock speed with ledger cost or
  obtain state-bin information for free.
* Show that maintaining the useful regions plus shared Q/body overhead fits
  resources while maintaining every region does not. In schematic form require
  M_useful+M_shared <= M_available < M_all+M_shared, with actual energy, transport,
  and temporal delivery constraints checked separately. Ensure continued-use and
  periodic O-write denominators can be positive; zero denominators are already
  explicitly nonevaluable in the protocol.
* A possible 16-bit Q representation has step 1/256 and range [-128,127.99609375].
  With a declared reward bound |r|<=1, gamma=15/16 gives |Q*|<=16. Alpha=1/8
  permits one exact integer numerator 16*r_int+15*Qnext_int-16*Q_int, divided
  by 128 with declared rounding, then added and clamped. All intermediate
  values fit signed 32-bit arithmetic, including the full damaged 16-bit input
  range. Terminal transitions omit the bootstrap term. These numbers are an
  illustrative conventional choice, not approved ecology reward units.
* Round-to-nearest in that example can stall updates for |TD error|<1/64.
  Small action-value differences need a precision check; exact rational
  coefficients alone do not remove quantization error. Stochastic rounding with
  independent indexed noise avoids deterministic dead bands in expectation
  without an unbudgeted residual accumulator. A 64-state x 3-action x eight-bit
  table has the same capacity but substantially less precision. Freeze reward
  units, discount, rounding, clipping, exploration, update order, and invalid
  metadata behavior before implementation.

Anchors: E3_PROTOCOL_v0_1.md:137-162, 181-204, 294-327, 390-399, 419-431.

## Alternatives and outstanding decisions

* Prefer persistent pipeline/staging/TD allocation with true operation scratch.
* Choose immediate H2 queries, multiplexed delayed queries, or a longer serial
  horizon; do not silently combine their incompatible timing assumptions.
* Choose synchronous one-step RL or a bounded delayed-feedback contract.
* Choose precise smaller Q tables versus finer bins with coarser values.
* Define code-only and whole-substrate strata rather than disguising spared
  learned control state as physical whole-state damage.
* Plan chance-control containment assurance using the actual reset output
  process, not raw repeated-answer counts.

No external literature is needed to answer the scoped questions. Remaining
questions are specification decisions: delay scope and clock ordering; reward
latency/units; upkeep domains and physical fault types; code mapping; resource
yields/rent and horizon support; sample/precision assurance. These require the
owner's choice, not discovery from the current unfrozen documents.

## Evidence and limits

Both requested documents were read in full. Closed-form arithmetic was evaluated
in a terminal without importing or executing E3, accessing final seeds, reading
result data, or writing calculation outputs. No E3 implementation validation,
Monte Carlo experiment, code-distance enumeration, bootstrap calibration, or
historical revalidation was performed. Only this required research tracking note
was created; protocol and historical artifacts were not edited.

Independent arithmetic checks give 1,897 used auxiliary bits plus 151 reserve,
96+128+32=256 scratch bits, 32 bits per delayed TD record, and 2,464 total
allocated bits including code, auxiliary, and scratch storage.

## Recommended next work not completed

* [ ] Select timing, reward-latency, and operation boundaries.
* [ ] Freeze a fieldwise storage/reset/fault/ownership inventory.
* [ ] Derive physical cost bounds including Q and routing upkeep.
* [ ] Enumerate codewords and punctured distances for the selected placement.
* [ ] Calibrate the proposed individual-level CI containment procedure.
* [ ] Establish H1 and adaptive-over-periodic headroom for the full selected
  wear/query schedule without inspecting final outcomes.
