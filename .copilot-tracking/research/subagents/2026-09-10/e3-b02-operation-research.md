---
title: E3 B02 costed operations and event schedule research
description: Candidate finite-state operation schedule, resource tariff, and unresolved physical dependencies
ms.date: 2026-09-10
---

## Scope and status

Complete for the requested bounded research; B02 is not a design freeze.
Specification research only; no E3 implementation or protocol edit.
The selected state inventory in E3_STATE_CONTRACT_v0_2.md takes precedence over
the historical proposal in E3_PROTOCOL_v0_1.md.

## Questions

* Fit old and current TD returns into one record across cleared operation scratch.
* Order decisions, responses, failures, retirement, and five-slot query admission.
* Charge observation, decoding, preflight, cleanup, and physical accounting without
  hidden peeks, recursive charges, or additional persistent state.
* Specify live tie abstention, partial teaching, and affordable staging clearance.
* Separate physical termination from a corruptible dead flag and Q refresh from
  restoration of a lost acquired value.
* Distinguish cost-parametric B02 closures from unresolved B03 physical choices.

## Findings

Use a fused controller operation, not a second transition or a tick-local host
cache. Observe, consume the old TD record, decide, execute the selected action,
and store the current record within one atomic operation. Respond afterwards
in another operation, adding its scalar return to the current record. Reserve
mandatory retirement before either operation. This closes the principal lifetime
problem without changing a field or using the inaccessible reserve.

The commitments below are proposed B02 choices, not changes already selected in
the authoritative contract. Numerical affordability remains unestablished.

### Resource tariff and bounded placement input

Use an explicit inherited placement input G containing controller and I/O
locations, routes to every physical two-bit lane, four material sources and
their fixed routing assignment, and twenty domain memberships. Require finite
integer routes bounded by a declared Dmax, positive finite capacities, and
overflow-checked quotes. Do not supply an invented numerical Dmax, rent, hazard,
yield, or support schedule. G must be independent of acquired labels/history.
Require Emax<=65,535 and each Pmax<=255 to respect the existing physical fields.

Proposed exact primitive tariff:

* Read a persistent two-bit lane: one energy. Read a width-w field by touching
  every intersecting physical lane, not by charging one unit for a whole Q word.
* Write a persistent two-bit lane, including auxiliary storage: four energy and
  one material from its assigned source. Same-value writes cost the same. A
  single-bit update also needs a paid read and one masked-merge logic operation
  when its lane mate must survive. Intentional code erasure writes 10.
* Each at-most-32-bit ALU/register operation: one energy. Specify moves,
  signed/unsigned extraction, insertion, Boolean operations, comparisons,
  shifts, addition, subtraction, selection, and branches separately. No
  unit-cost decoder, variable-size reduction, division, popcount, or
  acquired-table lookup.
* Scratch is executor register space, not persistent material storage. Register
  access is included in each ALU instruction. Clear all eight 32-bit scratch
  words at every operation exit: eight logic/energy, no material. This explicit
  volatile-register exception does not exempt staging, TD, Q, or query writes.
* Communication costs one energy per two-bit flit per traversed link. With
  eleven-bit physical lane addresses, a read request uses six flits and its
  reply one; a write uses six address flits, one data flit, and one acknowledgement.
  For symmetric controller distance d, read transport is 7d and write transport
  is 8d. Add one energy per material-unit hop from source to destination.
  Fixed public route/address lookup costs one logic instruction per access.
* Living costs sixteen energy per live tick. Rent/service dues are explicit
  integer B03 inputs per physical domain, not free simulator occupancy counts.
  Prefer allocated-capacity dues; a content-dependent rent requires a separate
  physical rule and paid controller access if its result becomes an observation.

Thus a body trace has

$$
C_E=N_R+4N_W+N_L+H_{\mathrm{flit}}+H_{\mathrm{material}}
    +C_{\mathrm{meter}}+16I_{\mathrm{living}}+C_{\mathrm{rent}},
\qquad C_{P,j}=N_{W,j}+C_{\mathrm{service},j}.
$$

Full aligned Q-word rewrite is eight lane writes: 32 energy and eight material,
before transport. Full TD clear or store is sixteen writes: 64 energy and
sixteen material. A query-slot or teaching-block clear is four writes: sixteen
energy and four material. Material conservation includes auxiliary writes;
counting only corrective code writes would substantially understate consumption.

### Finite physical meter and affordable preflight

Declare one protected physical transaction primitive with a flat tariff of
128 energy plus its G-specified transport. It includes sensing physical E/P
for affordability, cap/overflow arithmetic, debits/deposits, and one-way ledger
emission. It returns only admission status unless a separately paid resource
read is requested. Its own resource changes do not recursively invoke it.
Shape-quote lookup, resource comparisons and admission bookkeeping are included
in this finite tariff; calculating a quote is not an extra free controller pass.
This is a proposed simulator tariff, not a claim that 128 is derived from RAM
microphysics. Typed physical E/P fields are not ordinary XOR-faultable RAM.

The meter may use bounded operation scratch and fixed generic control; it may
not retain an escrow account, cumulative cost, pending refund, event result, or
balance mirror across operations. Ledger entries leave the worker and cannot
be read back. Debit admission and work in execution order, before accepting the
yield of that work; finalization closes the transaction before scratch clears.
Apply caps at the actual deposit, not by rearranging the tick equation. For an
energy deposit x, accepted=min(x,Emax-E) and overflow=x-accepted. Physical
accounting within an admitted transaction does not recursively charge another
meter fee at every opcode. Each additional admission gate does pay a new fee.
There is no checkpoint while any transaction is open.

Before any protected operation reads acquired memory, form

$$
Q_k(G,\sigma)=(\bar C_{E,k},\bar C_{P,k,0:3},
               B_{E,\mathrm{tail}},B_{P,\mathrm{tail},0:3}).
$$

Here sigma is public operation shape: phase, substep, representation, current
input address if present, fixed maximum scan/write count, and routing bounds.
It is not a decoded value, dirty-cell count, valid flag, Q magnitude, or expected
reward. An unknown ring/TD address is bounded over all its encodings. Following
a paid read, a subtransaction may use that acquired address, but its quote still
depends on operation shape, never an uncharged reread of the contents.

Admission requires physical resources to cover the current transaction,
worst-case admitted body, local finalization, and the remaining mandatory tail,
componentwise in all four material pools. Unused reserved capacity stays in the
existing physical fields; it is not debited into hidden escrow. Recompute the
tail floor from the public substep. Resource gains never finance their own
preflight. All gates include their own fee and eventual scratch clear. Nested
write/TD gates are subtransactions inside the atomic controller, not operation
boundaries: they preserve its scratch and each reserves the controller's record
store/clear and finalization. Charge eight scratch-clear instructions once at
the atomic exit, not once per nested gate.

At tick entry reserve every minimum path: scheduled living/accounting, stale-TD
retirement where applicable, due-slot retirement, scheduled staging clearance,
required flag/age bookkeeping, and every fixed-position operation's rejection
path. Optional work cannot consume this floor. Bounds must fit checked integer
arithmetic; overflow rejects G, not a worker with wrapped negative costs.

Affordability rejection consumes its funded meter/cleanup path but does not read
the protected body or write its proposed payload. A paid failure-flag update is
part of that path. If even the minimum path is unaffordable, physically terminate
as specified below; do not offer a free observation or search for a cheaper
action. Discretionary suboperations are bounded, with no retry loop.

### Tick order and the one-record schedule

Place stochastic storage/resource faults after the paid tick operations and
mandatory cleanup. This is an explicit proposed event-window restriction on
B03, not an assumption that arbitrary intervening damage preserves reservations.
The observation and action then share a coherent atomic read snapshot.

1. Apply declared current support/deposition only to an already powered live
   worker. Check the minimum tick path, pay living, and establish its public
  tail floor. Mandatory passive grants are explicit environmental inputs, not
  self-financing forage attempts; log their cap/overflow separately and fund
  their body-side accounting in the minimum path. No answer-derived yield is
  available at this point.
2. Run the controller operation if this tick type has a maintenance offer.
   Read the offered code unit, physical resource sensors, and supplied current
   usefulness; calculate the 32-bin observation with charged logic.
3. Still inside that operation, read the old TD record. If valid and its action
   is 0-2, optionally perform the funded TD update using current Q reads. Clip
   its stored reward to [-256,256]. Honor its stored terminal bit, even if
   corrupted; terminal means m=0. Otherwise read all three successor Q values
   and take their paid maximum. Permit all three actions in this maximum;
   an affordability mask would require additional paid tests.
4. Clear the complete old record on every path before storing another. A failed
   TD-update quote drops this transition, not the whole tick or a hidden queued
   update. Corrupted valid=0 suppresses an update; false valid=1 can invent one.
   Old action=3 causes a charged drop, never a gain or a repaired action value.
5. Select the current action from freshly read current Q, after the TD update.
   A cached pre-update row can be stale if the update hit that same row. Charge
   epsilon selection, maxima, tie handling and indexed random-input access.
   Fixed policies use their own paid rule rather than a gratuitous Q pass.
  A periodic policy also skips health observation when its rule does not need
  it; a threshold policy cannot skip the scan that supplies its threshold.
6. Execute that action before any due response. Forage/collection require a
   funded attempt before accepting the current opportunity's capped yield.
   Scrub reuses the already paid observation snapshot inside this same atomic
   operation. A tied/empty decode abstains after paying its scan. For a unique
   decode, scan targets in fixed physical order; read/compare work is charged,
   and individually preflight writes of disagreeing/erased symbols. At the first
   unaffordable needed write, stop, flag partial failure, and retain the paid
   prefix. Do not retain a remaining-work mask or resume it next tick.
7. On learning-enabled ticks store the current observation, attempted action,
   its tick-local return so far, public terminal status, and valid=1. A failed
   chosen action is still the attempted action, with declared failure return;
   it is not silently replaced by forage. This store and old-record clearance
   must have been reserved before admitting controller work. Clear scratch.
   If the controller core itself cannot start, its minimum path drops/clears
   the old record, creates no new one, and makes no allocator decision.
8. Run RESPONSE for slot (t-1) modulo 5. Its base read is paid even when invalid.
   While the stored address remains in the slot, decode only that address if
   valid and funded, and emit at most one response. A valid powered query may
   use a readout-only indexed fair bit for tied/empty memory; this never becomes
   a candidate codeword for repair. An invalid slot produces no response.
9. In ecology, receive the scalar return synchronously inside RESPONSE. Apply
   its accepted physical yield and add its B04 scalar contribution to the
   current TD record, if one exists. Fund deposit/accounting and reward-field
   read/write before emission. Never retain an evaluator callback across the
   operation or credit the query-admission record from five ticks ago.
   Missing current TD means unlearned return, not a fabricated transition.
10. Clear all eight due-slot bits on success, invalidity, unaffordable decode,
    or missing planned query. This mandatory clear has its own reservation.
    The minimum RESPONSE path also finalizes/clips any current TD reward, even
    when no response is emitted. Otherwise an unaffordable response could leave
    an unclipped controller return at the tick boundary.
    Then, in a separate operation, admit the optional current cue into that
    same slot if affordable. No admission means leave the retired slot zero.
11. Finish paid periodic/cursor bookkeeping, domain upkeep, and any scheduled
    terminal TD flush; clear scratch. Apply B03 damage only after this work.
    End at the full 276-byte persistent boundary, with no suspended operation.

RESPONSE may be starved by optional action spending in this candidate: reserve
retirement, not guaranteed decoding. Making response service a higher funding
priority is another defensible choice, but requires a declared larger floor.
The action still precedes response yield in either choice.

Learning-disabled recovery uses the same fused decision/action operation but
does not store a new transition. H1 post-challenge evaluation omits that entire
controller operation: no offer, observation bins, allocator action, or Q access.
It still pays all scheduled response, routing, living, and upkeep costs for
261 ticks. Offline probes do not provide a free decode to the live worker.

Read metadata before using it. A cursor in 20-31 causes the cursor-using
operation's paid failure path, not modulo repair, out-of-range access, or a
protected replacement cursor. Increment a valid cursor or wrap the eight-bit
periodic counter only through paid operations. No failed-operation flag is
authority to discard planned rows or reconstruct missing transition history.

### Reward lifetime and terminal handling

Only the TD reward field may accumulate a return across operations. Within
the controller, the old reward is consumed first; its register can then be
reused for the current return. RESPONSE must reread/write the current reward
field rather than carry it in a host local. Its scalar feedback is consumed
before scratch clearing, not delivered to the next operation for free.

B04 must select additive integer event contributions and bound every uncorrupted
within-tick accumulator prefix to signed-16 range. Clip the final r to
[-256,256] in the last reward-bearing operation and again when TD consumes it.
Alternatively select eventwise saturation explicitly: it is a different reward
definition, not algebraically equivalent final clipping. Damage occurs after
finalization and can corrupt that bounded stored result.

The minimal reward schedule has controller and response contributions only;
later admission/upkeep costs are then physical costs, not additional rewards.
If B04 includes them, move mandatory reward finalization to the last such
operation and reserve its reward-field read/write on all failure paths.

Do not promise a reward based on total tick spending unless that total can be
formed within these lifetimes. The controller can include its own measured
local cost; later operations can add their own contributions by paid updates.
Costs incurred before a new record exists must be fixed/recomputable, fused
into the controller, or explicitly excluded from r. In particular an old-TD
update cost cannot become a protected host accumulator. Exact reward units,
prefix bounds, and treatment of non-reward cleanup costs remain B04.

At a known learning-phase end, set current terminal=1 before storing, receive
the same-tick response, then optionally update with m=0 in a terminal operation.
Reserve its record clear even if its Q update is unaffordable. Isolation entry
clears the record by a funded boundary operation or explicitly logged boundary
intervention, never by silently ignoring its price. No successor observation
or final dummy action is invented. Unexpected depletion before a payable flush
loses that transition;
there is no posthumous TD update or update on a later refill.

Physical terminality is not the corruptible dead flag. Recommended rule:
E=0 is absorbing during a phase; inability to fund a mandatory path triggers
a declared shutdown sink removing remaining E. Log shutdown energy separately
from performed work. P and memory need not be zero. Setting a digital dead flag
is attempted only if its paid write is possible; an erroneous dead=1 at E>0
does not itself stop execution, and dead=0 at E=0 cannot revive it.

After shutdown, no live events, outputs, support acceptance, or old-slot replay
occur. The external scorer retains all planned rows as failures. Terminal
status is derivable from physical E, so no additional protected alive Boolean
is needed. An explicitly named new-phase activation may power the canonical
unpowered reset state, but only after pipeline/staging/TD boundary handling.
Ordinary food/refill must not reactivate a dead historical worker with old slots.

### Five-ring and teaching edge cases

At t=1 the due position is retired before its first insertion; at t=6 that same
position is consumed for t=1. Therefore the boundary maximum is five addresses,
never six. A failed response cannot remain to reappear at t+5. If retirement
itself cannot be funded because the tick minimum fails, shut down with bytes
unchanged and no future replay; do not describe those bytes as cleared.

Use the explicit 16 passes over four blocks, four consecutive lessons per block.
Repetition attempts its five code writes per lesson in fixed order. For block
coding, each lesson performs paid validity=0, label transfer, then validity=1
updates, preserving neighboring bits through paid read/modify/write. Stop on
failure; do not resend the lesson. Each lesson is an operation, so labels survive
only in the eight-bit block staging field, not in a teacher-side pending callback.

Immediately after the fourth lesson, run the single scheduled commit opportunity:

* Reserve full eight-bit staging clearance before the opportunity's body.
* Pay to read all eight staging bits and test its four stored valid flags.
  Four ones authorize use of the four currently stored labels. No receipt
  bitmap, known-clean fourth lesson, or truth comparison strengthens this test.
* If authorized, generate code symbols from that staged payload and attempt all
  twenty writes in fixed order, including same-value writes. Prefix completion
  is the declared partial-commit rule; stop at first unaffordable write.
* Clear all eight staging bits even for invalid flags, false acceptance, partial
  transfer, or zero affordable code writes. Pay any acquisition-failed flag
  update; the flag is an imperfect diagnostic, not authenticated acquisition.

Across ticks, faults can change validity or labels, so false acceptance and
wrong encodings remain possible. Earlier lesson admission does not guarantee
later commit clearance: if subsequent physical losses make the scheduled
clearance minimum unaffordable, terminate, or use an explicitly logged boundary
intervention. There is no free ordinary clear. The next teaching pass is a new
scheduled example, not retry of a protected old payload. Full acquisition still
has 1,280 code writes per representation, plus unequal auxiliary/logic costs.

### Priced decoder kernels and scratch witness

One implementable deterministic arithmetic-kernel proposal uses unrolled fixed
ROM control, rather than charging hidden loop/control work as zero. ROM contains
generic instructions and the twenty generator columns, not learned codewords.
The columns are the fifteen nonzero four-bit columns, then 1, 2, 4, 8, 15, as
in E3_LITERATURE_REVIEW_v0_1.md. Its public physical order must be fixed in G.

For repetition, keep the five observed symbols and count zero/one votes:

* Two counter initialization instructions.
* Five instructions per symbol: scratch insertion, two equalities, two adds.
* Twelve instructions for total, empty, tie, best bit, both-signs-present,
  partial occupancy, degradation, and three health selections.
* Five separate route lookups and five persistent reads.

This gives 39 arithmetic instructions, five routing instructions, and five
reads: 49 energy plus 7 times the sum of the five read distances, before input,
meter, output, and scratch-clear costs. Empty takes priority over tie. A unique
all-agreeing five-symbol vote is health=2; a unique degraded vote is health=3.

For block decoding, always scan all twenty symbols and all sixteen candidates:

* Initialization and observation capture: 64 logic instructions, comprising
  best distance/payload/tie and observation-count initialization plus twenty
  scratch insertions, observed-symbol tests, and observation-count additions.
  Initialize best distance to 21 and the other three quantities to zero.
* Each candidate: two initializations; twenty cells at eleven instructions
  each; six minimum/tie-reduction instructions. The per-cell eleven are six
  shift/Boolean instructions for parity of payload AND column, scratch extract,
  observed test, mismatch test, observed AND mismatch, and distance add.
* Reduction computes less/equal to best, ORs equality into tie, then selects
  new tie, best payload, and best distance. Strict improvement resets tie.
* Seven health instructions: empty test, partial-occupancy test, nonzero best
  distance test, OR for degradation, then three selections. Empty overrides
  tie, which overrides the intact/degraded distinction.
* Twenty route lookups and twenty persistent reads are additional.

The block arithmetic count is 64+16(2+20x11+6)+7=3,719. Including routes/reads,
its body price is 3,759 energy plus 7 times the sum of twenty read distances.
These are prices of this deliberately fixed kernel, not lower bounds on all
possible decoders. A different optimized generic decoder needs a new priced
trace, not an unexplained implementation shortcut. Reply-bit extraction,
write-target comparison/generation, resource sensing, TD and selection remain
separately charged. Ties do not save this fixed scan cost.

At the decoder peak, 40 raw-symbol bits, four candidate bits, four best-payload
bits, five-bit distance, five-bit best distance, five-bit observation count and
one tie bit total 64 of the 96 decoder bits. Remaining decoder bits hold
one-bit intermediates. The 40-bit snapshot spans fixed scratch words; no
instruction manipulates a 40-bit integer as a single 32-bit primitive.
At the TD peak retain only the 40 symbols and four-bit best payload; use the
freed decoder bits for observation/old-address/cost temporaries.
Four 32-bit arithmetic registers support q, r, m, numerator/rounding work;
compare flags fit the remaining decoder bits. The 32 control bits cover a
16-bit micro-PC, eleven-bit lane address and five flag/control bits. Current
cue/observation need not coexist there: retain the observation in decoder
scratch and reread the current external cue with a charge when necessary.
No simultaneous saved Q row is required: stream the maximum and reread the row
for selection. Provide a micro-PC/register liveness trace
before implementation; this is a capacity witness, not a tested allocation.

The TD arithmetic kernel can also be explicit: 23 ALU instructions after
loading q, r, m, using four 32-bit registers and one scratch predicate bit:

* Clamp r with two comparisons and two selections: four instructions.
* Form 16r+15m-16q with three shifts, two subtractions, and one addition: six.
* Obtain floor quotient by arithmetic right shift seven and remainder by AND
  127: two. Determine odd quotient, equality to 64, AND, greater than 64, and OR
  for the rounding increment: five. Add increment and old q: two.
* Saturate q with two comparisons and two selections: four.

For register feasibility, start R0=q, R1=r, R2=m. After forming the numerator
in R3, reuse R1 for quotient, R3 for remainder and R2 for the increment;
one predicate bit handles equality/greater-than and saturation tests. There is
no fifth arithmetic register or fractional residue. The numerator lies in
[-1,019,888,1,019,889] even at corrupted Q extremes, within signed 32 bits.

An aligned Q read adds eight reads, eight route lookups, eight scratch
insertions and one signed-16 extraction: 25 energy before transport. That last
instruction sign-extends into the 32-bit ALU register; it is not a free cast.
Its write adds eight bit extractions, eight routes and eight writes:
48 energy and eight material before transport.
Nonterminal TD-specific work is therefore 25+3x25+4+23+48=175 energy: old Q,
three successor Q words, two compare/select maximum steps, arithmetic, and
rewrite. Terminal work is 25+1+23+48=97, including setting m=0. Add all read/write
and material transport, meter fees, old-record reads/field extraction, validity
tests and retirement. Selection afterwards rereads Q. These are kernel prices,
not an all-inclusive TD/controller operation quote.

### Policy refresh and upkeep history

A same-value Q refresh must read the current vulnerable word, then pay its
rewrite. Refreshing a corrupted q=17 as 17 does not recover an earlier q=800.
An arithmetic update that quantizes to the same q is still a paid write if
performed; skipping it is a separately declared policy. Neither operation may
read a developed checkpoint or protected learned value.

Any subsequent hazard reduction must be represented by the existing twenty
ages, with costed age updates, or an explicitly stateless physical rule.
An external last-refresh timestamp per Q word or set of domains written this
tick is forbidden acquired state. If one word's refresh resets a pooled age,
the benefit to other fields in that domain is real and must be declared.
B02 can price these updates parametrically; B03 must choose their physical
meaning and membership, and B04 their scheduling. Do not charge per-word
refresh while silently promising whole-domain protection.

### Strongest counterexamples

* Choosing this tick's action into a host local while the old TD tuple occupies
  the record creates a second persistent tuple as soon as scratch clears.
  Fusing the controller avoids this; splitting it requires paid record storage
  or recomputation and may require an actual schema change.
* Delivering a response before consuming old TD adds r_t to r_(t-1), or demands
  another accumulator. Correct delayed address handling alone does not fix TD.
* Quoting only the number of bad cells reveals memory health without paying a
  scan. A decoder implemented as a simulator helper can have the same defect.
* Funding twenty writes but not final staging/slot clearance makes the next
  pass a hidden retry or forces a free erase. Reserving only energy fails when
  local material or transport energy is exhausted.
* Sequential clipping changes reward: +300 then -300 clips to -44 instead of
  zero at bound 256. Exact final clipping requires a bounded wider intermediate
  within the existing signed-16 field, not an implicit host sum.
* A corruptible dead flag cannot provide irreversible physical death. A clean
  external alive flag, delayed retry queue, or automatic support resurrection
  violates the claimed full-state schema or no-replay semantics.
* A Q refresh that restores an earlier value is an unbudgeted acquired copy.
  A hidden per-word hazard age is extra state even if its values are not labels.
* If faults can remove reserved material between quote and clearance, the
  reservation proof fails. Either restrict event windows as proposed, make
  operations fault-atomic, or declare termination/intervention on this failure.

### What can close parametrically

The one-record lifetime, decision/response order, ring capacity, no-retry rules,
live abstention, paid scans, prefix writes, typed finite meter, physical-death
rule, and cleanup inequalities can be fully specified for any admissible G.
Exact operation prices can be computed from priced instruction traces and its
bounded route/material-source input. State remains 160+2,048+256=2,464 allocated
bits and 160+2,048=2,208 persistent bits, or 276 bytes. No escrow, reward queue,
alive bit, per-word age, or decoded cache is added.

Actual feasibility cannot close from route bounds alone. B03 still owes exact
placement, domain membership/service rules, rent, hazards, gains/caps, neutral
power/material support, resource sinks, and branch injury maps. The admissible
G predicate must also reject impossible routes and specify fault timing.
B04 owes reward-prefix bounds, thresholds, policy/refresh timing and paid rule
traces; B05 owes input schedules. Meter tariff 128, volatile-scratch treatment,
prefix repair/teaching, response funding priority, and absorbing shutdown are
explicit new candidate decisions requiring adoption, not facts implied by B01.

The proposed full-clear bookkeeping is expensive: an ordinary learning tick
with new-record store, old-record clear, reward-field write, slot clear and
admission uses 16+16+8+4+4=48 material before code writes, Q updating, or ages.
With an actual Q update this becomes 56. Even the maximum four-pool inventory
of 1,020 cannot fund nineteen such ticks without replenishment, before those
other costs. A controller without enough material to store a new TD record
cannot choose collection through an uncounted action latch. Treat this as a
feasibility constraint, not a reason to exempt bookkeeping after seeing results.

The decoder and TD arithmetic kernels are now priceable, but B02 is not frozen:
the remaining controller/record/metadata/I/O microtraces and a verified scratch
liveness allocation still require completion. Presenting this as all opcode
costs resolved would overstate the evidence.

## Evidence

* E3_STATE_CONTRACT_v0_2.md: read in full; selected 2,464-bit allocation,
  276-byte persistent schema, lifetimes, query schedule, and blocker dependencies.
* E3_PROTOCOL_v0_1.md: read in full; candidate coefficients, shared baseline
  obligations, physical resource accounting, and isolation constraints.
* E3_LITERATURE_REVIEW_v0_1.md, Mathematical baseline proposal: generic twenty
  columns for the proposed block code; consulted locally, no new source claim.
* .copilot-tracking/plans/2026-09-10/e3-specification-plan.md, Immediate next
  specification slice: B02 precedes B03-B07; specification work only.
* .copilot-tracking/research/subagents/2026-09-10/e3-finite-state-exact-erasure.md:
  earlier lifetime/capacity alternatives; not authority over selected v0.2 fields.

## Remaining research and clarifications

* [x] Reviewed schedule, resource lifetimes and arithmetic counts; no editor
  diagnostics in the research document during validation.
* [ ] Price remaining controller, record, metadata, I/O and failure microtraces.
* [ ] Resolve B03 physical placement and service/age semantics; then instantiate
  the inequalities and test bookkeeping floors against scarce material.
* [ ] Select B04 return mapping/prefix bounds and response-priority policy.
* [ ] Verify microinstruction scratch liveness and later production no-replay,
  ledger-conservation and paid-clearance tests after implementation authorization.

No clarifying question blocks this bounded research. Adopting the explicit
candidate choices requires a later versioned specification decision; no user
input or new literature lookup is needed merely to continue that design work.