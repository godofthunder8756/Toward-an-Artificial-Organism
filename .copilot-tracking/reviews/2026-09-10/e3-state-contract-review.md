---
title: E3 state contract independent full-document review
description: Critical review of finite-state accounting, temporal semantics, erasure, and analytical qualifications
ms.date: 2026-09-10
---

## Review status and access

Complete as an independent document review. The earlier Implementation Validator
attempt lacked file tools and produced no assessment. That access limitation is
not a zero-finding review. This reviewer had filesystem access and read the full
contents of all three required files, not selected excerpts:

* E3_STATE_CONTRACT_v0_2.md, lines 1-389
* E3_PROTOCOL_v0_1.md, lines 1-457
* .copilot-tracking/plans/2026-09-10/e3-specification-plan.md, lines 1-152

Source references below use workspace-relative paths and inclusive line ranges.
The findings concern the selected finite-state and temporal slice. No E3
implementation, production noninterference test, feasibility run, or full
operational freeze was assessed. Read-only shell arithmetic checked the stated
numbers; it did not simulate agents or run training.

Only this review artifact was created or edited. Historical documents, source
files, the continuation plan, and the separate subagent research note were not
changed. The plan's historical excerpt-review closures are not transferred to
this full-document review.

## Bounded verdict

Revisions required before treating the B01 candidate as internally settled.
There is one Major finding and three Minor findings; no Critical finding was
identified in the reviewed documents. These are document findings, not claims
that an unimplemented worker already contains a leak or bug.

The selected allocation arithmetic, single-record TD capacity, five-address
pipeline capacity, endpoint counts, canonical-erasure construction, and quoted
analytical numbers are coherent at the stated design level. The main gap is
that mandatory drain-only ticks lack a defined current offer for the selected
controller interface. Other findings concern competing interpretations of live
ties, corrupted validity, and address-error scoring.

B02-B07 remain explicitly documented freeze blockers. Their unresolved costs,
hazards, schedules, precision, and tests are not findings merely because they
are unfinished. B01 lifetime feasibility remains conditional on those choices.
This verdict grants neither design-freeze approval nor code approval.

## Questions under review

* Reconcile every bit offset, record width, scratch allocation, and lifetime.
* Test five-slot drain/insert semantics against atomic scratch clearing.
* Check H1, H2, and development timing and planned-response denominators.
* Separate admission usefulness, stored-address queries, and scorer-only cues.
* Check teaching failure, corruption, bookkeeping, and complete-reset boundaries.
* Recheck algebra and uncertainty assumptions without simulating an experiment.
* Distinguish actual contradictions from the explicitly open B02-B07 blockers.

## Findings and evidence

### SC-001 Major: No current offer is defined on drain-only ticks

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 125-142, 181-186, 196-204,
209-220, and 242-245. The observation uses current offered cue usefulness and
local health/material, and scrubbing routes to that offered unit. The packet is
described as containing the current admission. H2 explicitly has no admissions
at 508-512; H1 admissions end at 256 although evaluation continues through 261;
development admissions end at 2043 although execution continues through 2048.

These are mandatory ticks, not optional schedule details. With the packet as
described, there is no cue from which to obtain the selected observation or
scrub route. The contract does not choose between suspending allocation, using
a separately supplied maintenance offer, or using some other declared route.
Reusing the last offer would retain an undeclared lifetime unless explicitly
stored. Supplying the original due cue would defeat the damaged-address rule.
Treating absence as cue zero would silently add a biased maintenance policy.

This is a partial input contract within B01, not a complaint that B05 has not
chosen a particular permutation. The distinction also matters during isolated
recovery, which needs maintenance offers without admitting teaching examples
or receiving answer feedback. In H2 it affects the last five ticks of the
spending window, not only an incidental cleanup step.

Suggested correction, as an explicit candidate input rule:

> Separate the current maintenance offer from the optional query admission.
> Whenever an allocator observation or action is requested, the packet provides
> one current maintenance cue and its advertised usefulness. On ordinary
> admission ticks the offer may equal the admission. Drain-only and recovery
> offers, if any, are supplied by a paired target-independent schedule fixed in
> B05, never by the scorer's original due cue or a retained previous offer.
> A packet with no maintenance offer requests no allocator observation or action;
> due responses, upkeep, and declared bookkeeping still follow B02. Absence is
> not a seventeenth cue or an extra observation bin. Public phase rules specify
> which of these tick types occurs. The 32 observation bins apply only to ticks
> with an offer, and all offer processing is charged.

The offer and admission are external current inputs, not new persistent state.
Their routing costs and schedules remain B02/B05. Explicitly report any policy
that forces the final five spending ticks to contain no allocation actions.

### SC-002 Minor: Live block ties lack an explicit precedence statement

Evidence: E3_PROTOCOL_v0_1.md, lines 128-135 and 193-198;
E3_STATE_CONTRACT_v0_2.md, lines 9-14, 130-135, and 358-362.
The historical proposal explicitly randomizes equal-distance block-code ties.
The new slice leaves tied/empty live rules in B02 and says ties cannot silently
become learned values, without explicitly withdrawing or limiting that inherited
random-tie sentence. Its precedence statement principally replaces lifetime
and timing choices.

An all-erased block makes every candidate equally plausible. A forced-choice
readout can randomize, but selecting one of those codewords and writing it into
live storage is a different operation. Both readings remain plausible across
the two documents. This is a wording/precedence finding, not an assertion that
B02 must already contain a finished decoder or that a leak has occurred.

Suggested correction:

> The v0.1 random minimum-distance tie rule does not select a live-write rule for
> this candidate. Live block behavior for unique, tied, and empty observations
> remains B02. Until explicitly selected, no live reconstruction guarantee is
> claimed for tied or empty blocks. Forced-choice random guesses are readout
> only and cannot be written back as correction.

If a rule is selected now, the conservative consistent choice is: minimize
distance over currently observed binary symbols; abstain from corrective writes
when there are no observations or multiple minimizers; allow a unique minimizer
to be wrong and record resulting miscorrection offline. Random tie-writing is
an alternative only if explicitly named, costed, and distinguished from recovery
of a surviving answer. No new rule has been applied by this review.

### SC-003 Minor: Stored validity must not imply authentic teaching history

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 87-90 and 229-240.
Commit eligibility requires all four valid labels, but the validity bits
themselves are acquired, vulnerable state. The text does not say whether
"valid" denotes the stored flag or authenticated receipt of an uncorrupted
lesson. The latter interpretation would require information not in the schema.

For example, a failed lesson can leave its cleared label and validity at zero.
A fault can subsequently change that validity bit to one. If the other three
lessons arrive, all four stored flags are one without all four lessons having
been received. A label bit can also flip while its validity remains one.
Neither condition is generally detectable from the eight-bit block alone.
The prohibition on replacing corrupted staging from the evaluator is correct;
it must not imply that the worker can identify every such corruption.

Suggested correction:

> Commit eligibility tests only the four currently stored validity bits, not
> historical lesson success or true label integrity. Validity faults may cause
> false acceptance or false rejection; undetectable label faults may produce an
> incorrectly encoded word. No clean success bitmap or evaluator integrity flag
> is available to the worker. B02 defines failed and partial lesson transfers.
> Clearing a teaching block means clearing all eight bits, including payloads,
> after every scheduled commit opportunity, successful or not. Any inability
> to fund mandatory clearing requires the explicit B02 retirement/boundary rule,
> not an assumed free write or hidden delayed retry.

This clarification does not create an error merely because clearing costs are
still B02. It prevents the selected field semantics from being strengthened into
an unbudgeted authentication guarantee.

### SC-004 Minor: Separate wrong-address events from wrong answer bits

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 80-85 and 222-225;
E3_PROTOCOL_v0_1.md, lines 308-318 and 362-369.
The statement that missing or wrong responses, "including loss/misrouting,"
score zero can mean either answer comparison against the scheduled cue or
automatic failure on any address error. Those are different endpoints.

If scheduled cue A and corrupted stored cue B both have label one, responding
with one is correct for the binary answer endpoint despite the routing error.
Automatic failure would add an address-integrity criterion not stated in the
original binary recall definition. This matters for chance qualifications too;
address-sensitive success is not generally a one-half forced-bit endpoint.

Suggested correction, preserving binary recall:

> For each originally planned response, compare the emitted answer bit with
> the label of the originally scheduled cue. A missing or invalid response
> scores zero. A wrong stored address can cause a wrong answer, but a matching
> answer bit still counts as correct; report address errors separately. Task
> yield uses that scheduled cue and its usefulness at the declared response
> time, not the current admission or the corrupted stored cue. A spurious
> response during a tick with no planned due query creates neither an endpoint
> row nor task yield. The scorer's cue and integrity information never return
> to the worker; only the declared ecological scalar return does.

If address-sensitive success is intended instead, explicitly version that
endpoint and its negative-control expectation rather than treating it as an
equivalent wording change. Complete-erasure forced-choice scoring also needs its
own declared missing-response handling under B06.

## Checked state accounting and lifetimes

### Exact offsets and totals

The auxiliary ranges are contiguous, inclusive, non-overlapping, and correctly
sized. There is no off-by-one or total-capacity error:

* Q: 0-1535, 1,536 bits, equal to 32 x 3 x 16
* Query ring: 1536-1575, 40 bits, equal to 5 x 8
* Teaching staging: 1576-1607, 32 bits, equal to 4 x 8
* Previous transition: 1608-1639, 32 bits
* Energy: 1640-1655, 16 bits
* Material: 1656-1687, 32 bits, equal to 4 x 8
* Upkeep ages: 1688-1767, 80 bits, equal to 20 x 4
* Metadata: 1768-1783, 16 bits
* Inaccessible reserve: 1784-2047, 264 bits

Used auxiliary capacity is 1,784 bits. Adding reserve gives 2,048, not an
additional discretionary working allocation. Code contributes 80 x 2 = 160
bits. Persistent state is 2,208 bits = 276 bytes; scratch adds 256 bits, giving
2,464 allocated bits in total. The 20 code bytes plus 256 auxiliary bytes agree
with the checkpoint size. Allocated capacity is not the target's entropy.

Subfield widths also reconcile:

* Query slot j begins at 1536 + 8j: valid at +0, cue at +1 through +4, reserved at +5 through +7, for j = 0 through 4.
* Teaching block b begins at 1576 + 8b: four labels at +0 through +3, four validity bits at +4 through +7, for b = 0 through 3.
* The transition has valid at 1608, observation at 1609-1613, action at 1614-1615, reward at 1616-1631, terminal at 1632, reserve at 1633-1639. Its widths sum to 1 + 5 + 2 + 16 + 1 + 7 = 32.
* Material quantity k occupies 1656 + 8k through 1663 + 8k. Upkeep age k occupies 1688 + 4k through 1691 + 4k, within their respective array sizes.
* Metadata is cursor at 1768-1772, counter at 1773-1780, dead at 1781, acquisition-failed at 1782, operation-failed at 1783.

Two's-complement signed Q/reward and unsigned physical resources are compatible
with the declared packing. Reserved bits are serialized raw; treating them as
a hidden policy cache is prohibited, even if the common allowance has space.

### One TD record is sufficient, but its lifetime needs B02 ordering

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 92-96 and 165-171.
The five-query delay does not require five TD records. The selected learner
receives r in the response tick and performs ordinary one-step TD, not delayed
credit reassignment to the admission action. This may be an imperfect learning
problem; it is not an arithmetic contradiction. Observation aliasing and lack
of a convergence guarantee are already disclosed.

A feasible lifetime is to consume the previous record using the current paid
successor observation, update Q and retire that record, then reuse the same
record for the current observation/action and eventually its tick return.
An in-progress current record must have explicit validity/reward/terminal
semantics before it becomes the next tick's previous record. An old record
cannot be retained while a second current tuple lives in host variables.

Observation, action selection, response returns, and resource bookkeeping can
span multiple atomic operations. Any observation or chosen action needed after
an operation boundary must be in declared state, recomputed with charged reads,
or consumed within a fused bounded atomic operation. The scratch-clear rule
forbids carrying it in local variables across separate operations. Terminal
flush and unaffordable updates are openly B02, so their absence is not a new
finding. The record-width calculation alone is not a completed lifetime proof.

### Scratch and Q arithmetic fit the claimed capacity

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 108-121 and 144-163.
For block decoding, 40 observation bits, two four-bit candidates, two five-bit
distance counters, and a five-bit tie count total 63 bits. Five bits are needed
to represent all 16 tied candidates, not four. Even reserving a 20-bit generated
candidate word brings this illustrative allocation to 83 of the 96 decode bits.
This supports capacity feasibility, not a costed opcode implementation.

The quantized TD numerator is N = 16r + 15m - 16q. With q and m signed 16-bit
words and r clipped to [-256, 256], N ranges from -1,019,888 to 1,019,889,
which fits signed 21 bits and therefore a 32-bit register. Even an unclamped
corrupted signed-16 reward gives N in [-1,540,080, 1,540,065], still within
signed 32 bits. This does not license using that reward without the specified
clipping rule.

Four 32-bit registers can hold q, r, m and N, then reuse registers for signed
division/remainder, ties-to-even rounding, and saturation. A sign, remainder,
or intermediate float cannot be retained in additional uncounted storage.
B04 must specify clipping on consumption of a damaged reward word, max over
permitted actions, and the signed rounding/saturation cases. The expression
matches learning rate 1/8 and discount 15/16. The ideal uncorrupted discounted
bound 256 / (1 - 15/16) = 4,096 stored units is correct; it is not a bound on
every corrupted Q word. No arithmetic overflow finding is warranted here.

## Checked temporal and information boundaries

### Five-slot ring and atomic operation compatibility

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 80-85, 108-114, and 175-192.
At the end of tick 5 the ring holds admissions 1-5. At tick 6, slot zero is
consumed for admission 1 before admission 6 reuses it. The rule generalizes
because t and t-5 select the same slot. There is no need for a sixth persistent
slot if consuming precedes overwriting. The expressly selected pipelining
replaces globally blank trials; it tests a vulnerable address pipeline, not a
learned recurrent ability to bridge a globally blank interval.

The safe semantic constraint is to read/decode/respond while the due address
still resides in its slot, then clear the consumed slot and scratch before
reuse. This can be one bounded response operation. Other atomic operations may
be interleaved only if they do not require an old due address or decoded answer
after its slot and scratch are cleared. Copying the due address into scratch,
inserting a new admission, clearing scratch for another operation, and later
answering the old query would not satisfy the contract.

B02 still needs an explicit consume/emit/clear/insert order, the treatment of
unaffordable responses, and the ordering of admission versus maintenance. A
failure must not preserve an overdue query for an unplanned retry or shift the
fixed five-tick latency. These are documented ordering dependencies, not proof
that five slots are insufficient. Forged valid bits during warm-up must not
create extra rewarded queries; SC-004 makes the scorer treatment explicit.

### All declared windows reconcile

* H1: 256 admissions at 1-256 produce 256 responses at 6-261. All 261 ticks, including five warm-up ticks, count for living costs and viability. Planned recall remains divided by 256, not by surviving responses or elapsed ticks.
* H2: the 256 response ticks 257-512 correspond to admissions 252-507. Sixteen responses for each of 16 cues give 128 U and 128 O. Admissions 252-256 precede the spending window, as explicitly disclosed.
* H2 early period: 251 admissions at 1-251 produce 251 responses at 6-256. Total planned responses are 251 + 256 = 507, not 512. No admissions at 508-512 leaves no pending planned response outside the survival horizon.
* Development: admissions 1-2043 produce responses 6-2048, exactly 2,043. Teaching, ring, transition and scratch retirement precede isolation.
* Acquisition: repetition attempts 256 x 5 = 1,280 code-symbol writes; block coding has 16 passes x 4 blocks x 20 = 1,280 for complete successful encoding. Staging, validity, reads and clearing are additional costs. Failed acquisition does not acquire an uncharged retry or justify dropping a seed.

H2 preserves the same U set in both branches. Its spending ratios and
useful-recall-loss bound are not replaced by a branch-dependent denominator.
SC-001 concerns the controller's input on drain ticks, not the above counts.

### Admission usefulness is not the due cue

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 125-141 and 181-192;
E3_PROTOCOL_v0_1.md, lines 288-330.
The observed usefulness describes the currently offered unit. It need not equal
the usefulness of a query admitted five ticks earlier, especially in a schedule
mixing useful and obsolete blocks. The due address comes from the vulnerable
ring. The evaluator retains the original scheduled cue only for scoring and
scalar yield; it must not repair the worker's address or supply a due-label
lookup. Receiving that scalar yield in ecology is an explicitly acknowledged
answer channel, not example-free recovery.

The ban on regenerating an old cue from the public clock is correct but needs
an interface/schedule restriction, not merely omission of a due-cue field.
A publicly known cycle or a worker-readable schedule seed can reveal c at t-5
from time alone. B05/B07 must keep scorer schedules, their reconstruction seeds,
and indexed-randomness services for other ticks out of the worker's reach.
Provide current packets, not an arbitrary historical schedule lookup service.
Target-independent schedule information can still bypass an address-memory
assay; target independence alone is insufficient for that narrower purpose.
This obligation is already implied by the explicit prohibition and is not
reported as an observed leak or an unresolved-blocker error.

### Costed bookkeeping is a constrained exception, not extra memory

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 66-75, 137-142, 199-205,
235-245, and 358-370.
Disabling corrective code writes and Q learning while allowing ring writes and
resource accounting is coherent. A writes-disabled recall assay could not run
the declared pipeline if it literally forbade every physical write. However,
"bookkeeping" cannot authorize decoded-answer storage, extra fields, Q learning,
or uncharged observation. Q refresh versus Q learning must be distinguished
explicitly; a same-value refresh can still change later hazard through upkeep.

B02 must specify a finite charging convention for charging itself, scratch
clearing, ledger updates, failure flags and mandatory staging retirement.
Unaffordable commit does not necessarily imply unaffordable clearing, but the
zero-resource case must also be defined. An external canonical boundary can
be a declared intervention; ordinary in-ecology storage mutation cannot silently
become free by using the same word "clear." No paid-observation cache, residual
reward, or operation continuation may escape the state budget. These dependencies
remain open rather than being assumed resolved by the bit inventory.

## Complete-erasure review

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 58-75, 248-290, and 379-386;
E3_PROTOCOL_v0_1.md, lines 239-286.
The selected erasure construction addresses the principal hidden-state classes:

* All code symbols become 10, not a validity flag with an old sign retained.
* All auxiliary bits, including Q, payloads behind invalid flags, transition, teaching, metadata, resources, and reserve, become zero.
* Scratch clears; no callback, suspended operation, answer-bearing closure, old object reference, pending reward, or outstanding message survives.
* Future public phase/tick/purpose/location indexing is independent of target seeds, acquired resources, and action-count-dependent stream advancement.
* Physical resource quantities are canonicalized. Later neutral support is fixed independently of the developed body. Type-specific injury cannot use register XOR to manufacture energy or material.
* Boundary serialization includes all 276 raw persistent bytes, not only nominally valid payloads. Packing supplies no alignment padding channel. Host-object storage is not permission to retain extra values.
* Archival snapshots, checksums, clones, logs and scorer state are one-way experimenter outputs, not restoration services or reachable recovery inputs.

The induction Reset(history, G) = S0(G), followed by transitions using only G,
the current state and independent Z, is a sound conditional design argument.
It is not evidence that an actual implementation meets the reachable-input
restriction. A public absolute time used after reset must be fixed independently
of old target-dependent stopping history; the declared public reset phase is
consistent with that requirement.

The production tests appropriately include each target bit, cross-block changes,
populated auxiliary state, resources, invalid flags, reserve and pending events.
Four-bit enumeration is explicitly only a component test. Chance accuracy does
not replace structural noninterference, and a zero death flag does not mean the
blank body is powered. No full-erasure contradiction was identified at the
document level; production erasure remains unassessed and B07 stays open.

## Independent analytical checks

Evidence: E3_STATE_CONTRACT_v0_2.md, lines 292-354.
All quoted numerical results reproduce using deterministic scalar arithmetic:

* At p = 0.1, majority accuracy is 0.972 for three replicas and 0.99144 for five. The ideal immediate advantage is 0.01944, below a five-point gate.
* Over 128 independent reversible-flip ticks at h = 0.001, odd-flip probability is 0.11302822537825702. Combining the independent p = 0.1 challenge gives effective error 0.19042258030260562 and three-copy accuracy 0.9050274573516492.
* Subtracting that accuracy from hypothetical perfectly restored five-copy accuracy gives 0.08641254264835074. This is optimistic comparative headroom, not a predicted paid-scrubber result or an adaptive-versus-periodic margin.
* For 512 independent label outcomes under fixed per-cue answers, the stated normal 95% half-width is 0.043310290347676035. Under that illustrative fixed width, containment requires an estimate within about 0.00668971 of one half, approximately [0.49331029, 0.50668971], not merely within [0.45, 0.55].
* For independently refreshed fair forced guesses at every response, the illustrative 32 x 8 x 256 half-width is 0.003828125. Erasure alone does not establish those output assumptions or turn panels into independent subjects.
* Thirty-two replacement symbols require at least 32 writes and 32 material units; at four energy units per write, write energy alone is 128.
* Living cost for 128 recovery plus 261 query ticks is 16 x 389 = 6,224, excluding all other charges. This is not a resource-feasibility demonstration.

The retention comparison correctly excludes real repair errors, resource limits
and query-period wear. The separate adaptive-over-periodic gate needs a separate
headroom argument. Neither comparison licenses retrospective changes to a gate.

The CI discussion correctly distinguishes repeated fixed answers from fresh
independent guesses, keeps individual-level panel aggregation and paired
bootstrap inference, and labels normal approximations as sensitivity checks.
The full protocol describes percentile intervals conditional on the panels,
not universal equivalence or multiplicity-adjusted discovery. B06 must prospectively
address containment assurance under the actual forced-response, support, missing
response and post-reset fault rules. An imprecise interval is inconclusive;
reproducible target dependence fails isolation. No sample-size approval follows
from either half-width.

## Explicit blockers not counted as review findings

* B02 remains responsible for opcode costs, common event ordering, affordable preflight, failed/partial operations, observation-to-action lifetimes, terminal TD handling, ties/empty decoding, and dead-row bookkeeping.
* B03 remains responsible for mapping all fields into the 20 upkeep domains, age saturation/wrap behavior, physical fault laws, resources/support, rent, query-period wear and type-specific conservation.
* B04 remains responsible for return units and clipping, paid observation thresholds, policy refresh, exploration mapping, tuning grids and numerical edge cases. An eight-bit counter does not silently authorize a larger one.
* B05 remains responsible for complete arm/branch/channel products, maintenance offers and query schedules, paired streams, early-window counts, checkpoint context, formats and expected rows. SC-001 requests an input-type rule before particular schedules are chosen, not a finished schedule in this review.
* B06 remains responsible for independent H1/adaptive headroom, viable selective spending, positive aggregate comparator denominators and prospective complete-erasure precision. Zero-reference individuals remain in the sample; a zero aggregate comparator is not evaluable and cannot pass H2.
* B07 remains responsible for production-schema and reachable-state requirements, interface inspection, relevant source-access caveats and operational review. There is no production proof or design-only hash freeze in this slice; actual implementation tests belong to later authorized engineering.

The continuation plan's Phase 3/4 statuses and artifact inventory predate this
review and still describe adding/reviewing the contract as pending. Authorized
follow-up should reconcile them with the candidate artifact and these open
findings. This administrative observation is not a scientific SC finding; no
plan status was edited or retroactively marked approved.

## Coverage and bounded verdict

E3_STATE_CONTRACT_v0_2.md was reviewed without omissions:

* Lines 1-26: frontmatter, status, precedence, conventional explanation
* Lines 27-57: full allocation, offsets, reserve and excluded copies
* Lines 58-77: symbol encoding, canonical values, resources and Q lesions
* Lines 78-105: every query, teaching, TD and metadata field/lifetime
* Lines 106-122: scratch widths, clearing, protected atomic executor
* Lines 123-172: all observation, action and quantized learner commitments
* Lines 173-193: pipeline ordering, due-cue boundary and ecological return
* Lines 194-206: H1 warm-up, denominators, bookkeeping and wear
* Lines 207-226: all H2 windows, U/O populations, failures and drain
* Lines 227-247: acquisition staging, failure and development retirement
* Lines 248-291: erasure, physical quantities, randomness, serialization, tests
* Lines 292-324: analytical status, retention and adaptive headroom
* Lines 325-345: complete-erasure dependence and CI qualifications
* Lines 346-355: minimum writes/material/energy and living costs
* Lines 356-389: every B02-B07 blocker, B01 status and later freeze limits

E3_PROTOCOL_v0_1.md was read through its final interpretation sentence, including
all numbered sections 1-10, hypothesis/rival framing, gates, complete-loss
qualifications, operational checklist and verification requirements. The entire
continuation plan was read, including inherited review scope, ordered workstreams
and historical preservation limits. Those historical outcomes were not rerun
or independently reverified in this bounded review.

The bounded verdict remains revisions required: resolve SC-001 and disambiguate
SC-002 through SC-004, then reconcile B01 wording with its remaining dependencies.
Conventional ECC plus ordinary allocation remains an honest interpretation.
No conclusion about an implemented E3, freeze readiness, organismal closure,
regeneration from no information, or E3b follows from this review.

## Recommended next work and clarifying questions

The following work was not completed in this review and requires a separately
authorized specification continuation, not an automatic implementation:

* [ ] Select current-offer behavior during terminal drains and isolated recovery; retain the address-only due-response boundary and state the no-offer mode.
* [ ] Resolve live block tie/empty precedence and make physical validity and binary-answer versus address-integrity scoring explicit.
* [ ] Construct a B02 event/lifetime schedule covering the single TD slot, ring, paid observations, failures, bookkeeping and mandatory buffer retirement.
* [ ] Complete B03-B05 physical, reward, schedule and stream contracts without adding unbudgeted fields or exposing old/future cue schedules.
* [ ] Complete prospective B06 headroom, feasibility and precision justification.
* [ ] Complete B07 design-level noninterference/interface and operational review before a design-only freeze. Actual production-schema tests require separately authorized later implementation and the second source/configuration/test freeze before final individuals.
* [ ] Do not translate the earlier validator access failure into a pass, a fail, or a zero-finding implementation review.

Three author choices cannot be determined from the supplied documents: whether
allocation continues on no-admission ticks; whether live block ties abstain or
explicitly write randomized guesses; and whether a wrong address with the right
answer bit is correct for the main recall endpoint. The suggested corrections
provide concrete conservative resolutions. None requires simulator execution
to settle the document wording.

## Independent re-review closure on 2026-09-10

### Current status and exact scope

Complete. The bounded slice passes document consistency only, not full protocol
approval or erasure proof. All four initial findings are resolved in the revised
text. No new Critical, Major, or Minor inconsistency was identified across the
full revised contract. No unresolved B01 document-consistency blocker was found;
implementation validation and B02-B07 remain open.

This closure supersedes the initial revisions-required verdict and its three
unanswered author choices for the revised text only. The initial findings,
evidence, line references, and historical verdict above are preserved unchanged.
Their line numbers refer to the earlier 389-line contract, not this revision.
No earlier implementation assessment or plan status is upgraded by this closure.

The re-review read all of the following, without excerpt omissions:

* E3_STATE_CONTRACT_v0_2.md, lines 1-439
* E3_PROTOCOL_v0_1.md, lines 1-457
* .copilot-tracking/reviews/2026-09-10/e3-state-contract-review.md, initial lines 1-482

The reviewed contract's SHA256 is
DD8D37356AB0990DCE6C49F5CBB87F7AEBF1A3715081B2DC49C6729BDB86BFC6.
Only this existing review receives an appended closure. No other document,
research note, source, configuration, or plan is created or edited. Read-only
scalar arithmetic checked illustrative equations; no simulations, tests,
training, empirical analysis, or feasibility runs were performed.

### Finding dispositions

#### SC-001 Major resolved

E3_STATE_CONTRACT_v0_2.md, lines 191-224, explicitly separates optional admissions
from current maintenance offers. Development, H2, and isolated recovery receive
an offer on every live tick. Admission ticks use the admitted cue; other ticks
use a separate paired, target-independent schedule, not a due-address lookup or
retained prior offer. H2 ticks 508-512 therefore remain allocation opportunities.
Recovery offers carry addresses/usefulness, not answers. All 261 H1 evaluation
ticks instead request no allocator decision and supply no maintenance offer.
This is a declared response/upkeep-only mode, not an additional cue or observation
bin. Specific schedules and affordability remain B02/B03/B05, not an unresolved
input-type choice.

#### SC-002 Minor resolved

E3_STATE_CONTRACT_v0_2.md, lines 140-149, explicitly supersedes the historical live
block-tie rule. Both representations abstain on empty or ambiguous evidence; a
block uses only observed binary symbols and requires a unique minimum-disagreement
codeword for correction. A unique result can still be wrong. Forced-choice guesses
remain readout-only; neither guessing nor offline miscorrection reports may seed
live writes. B02 must cost scanning and abstention, not choose their meaning again.

#### SC-003 Minor resolved

E3_STATE_CONTRACT_v0_2.md, lines 87-94 and 271-294, defines validity as the currently
stored flag, not authenticated teaching history. Commit tests only the four stored
flags; false acceptance, false rejection, and undetectably wrong payloads are
admitted. All eight staging bits retire after each scheduled opportunity, including
failure. Retirement is paid, with inability to clear explicitly delegated to a B02
retirement/termination or declared boundary intervention. No clean success bitmap,
evaluator integrity check, delayed lesson callback, or hidden retry is introduced.
That lifetime constraint is selected even though its costed failure sequence
remains pending.

#### SC-004 Minor resolved

E3_STATE_CONTRACT_v0_2.md, lines 260-269, compares the emitted bit against the
originally scheduled cue's target. A wrong address with a matching bit counts for
binary recall, with routing error reported separately. Missing/invalid responses
and incorrect bits remain zero; planned denominators do not shrink. Yield uses
scheduled-cue usefulness at response time, not the current offer or corrupted
address. Spurious outputs with no planned due query receive neither yield nor a
scored row. The worker receives only the declared ecological scalar return, not
scorer cues or integrity flags; H1 receives no such return. Complete-erasure
forced-response/support conventions remain a separate B03/B06 obligation.

### Full-document consistency and coverage

The scan was not restricted to the four edited passages. Coverage of the revised
E3_STATE_CONTRACT_v0_2.md is as follows:

* Lines 1-26: status, precedence, bounded conventional ECC/allocation claim
* Lines 27-57: every allocation, inclusive offset, capacity total, and reserve
* Lines 58-108: symbol encoding, canonical reset, every record and its lifetime
* Lines 109-125: scratch partitions, clearing boundaries, decoder capacity
* Lines 126-190: observation bins, live decoding, actions, quantization, TD lifetime
* Lines 191-231: ring timing, current offers, no-offer mode, retirement, feedback
* Lines 232-270: full H1/H2 windows, planned denominators, scoring, routing errors
* Lines 271-295: acquisition attempts, corrupted staging, retirement, development
* Lines 296-339: complete erasure, independent inputs, physical resources, snapshots
* Lines 340-372: analytical qualifications, retention headroom, periodic comparator
* Lines 373-403: erasure precision/dependence and minimum operation/living costs
* Lines 404-439: every remaining blocker, B01 candidate status, two-freeze limits

State totals remain 1,784 used auxiliary bits plus 264 inaccessible reserve bits,
160 code bits, and 256 operation scratch bits: 2,208 persistent bits, 276
serialized bytes, and 2,464 allocated bits. No revised clause adds an undeclared
persistent offer, decoded answer, success bitmap, reward cache, or second tuple.
The 32 observation indices still span exactly 0-31. H1's lack of allocation
removes the need for an observation on no-offer ticks; it does not remove the
costs of responses, wear, upkeep, or bookkeeping.

The strengthened cross-operation rule at lines 177-189 requires the single TD
record, charged recomputation, or a bounded fused operation for values needed
after scratch clearing. Consuming a due address while its ring slot still holds
it, then retiring before reuse, preserves the five-slot capacity argument at
lines 197-224. Neither statement is a finished B02 operation schedule, but no
second persistent tuple or sixth address is forced by the selected semantics.
Failure cannot silently extend the response delay or retain a retry.

All temporal counts remain coherent: H1 has 256 responses over 261 elapsed ticks;
H2 has 251 early plus 256 final-window responses, 507 overall, over 512 ticks;
development has 2,043 responses over 2,048 ticks. The H2 endpoint still has
128 U and 128 O responses, with admissions 252-256 preceding its spending
window. Acquisition still requires 1,280 successful code-symbol writes per
representation for all presentations, excluding staging and other costs.
Continued-usefulness comparison retains the same U set and scheduled endpoint.

Canonical reset, physical-resource reset, raw serialization, and future-input
restrictions remain mutually consistent. The new offer schedule does not grant
access to past/future admissions or their seeds. H1's no-feedback mode and
isolated recovery still prohibit outcome-dependent support. Same-value upkeep
is not restoration of a lost unreplicated Q word. The noninterference induction
remains conditional on the eventual implementation's reachable inputs; chance
accuracy and a 276-byte schema do not establish that implementation property.

### Approximate algebra recheck

Deterministic scalar recomputation agrees with the displayed design calculations
to floating-point rounding. No calculation is treated as empirical evidence:

Three- and five-copy accuracies at flip probability 0.1 are 0.972 and 0.99144,
an ideal immediate difference of 0.01944, below the proposed five-point gate.

Recovery odd-flip probability is approximately 0.113028225378257; combined
challenge error is 0.190422580302606. Worn three-copy accuracy is approximately
0.905027457351649, giving optimistic headroom of 0.086412542648351 against
perfectly restored five-copy storage. This excludes repair errors, resource
limits, evaluation wear, and any demonstrated advantage over tuned periodic
maintenance.

The illustrative fixed-answer normal half-width is 0.043310290347676.
Containment then requires an estimate near the center, approximately between
0.49331029 and 0.50668971 under that fixed-width approximation. The independent
fresh-guess half-width is 0.003828125, but erasure alone does not establish
those response-independence assumptions or approve the proposed sample.

Minimum replacement-write energy remains 128, with at least 32 writes and
material units. The 128 recovery plus 261 query ticks require 6,224 living
units at the prospective rate, before other charges. This does not demonstrate
an affordable recovery or evaluation budget.

The quantized TD equation has the stated learning rate and discount. With
consumed reward clipped to [-256, 256], its numerator spans -1,019,888 through
1,019,889 for signed-16 Q inputs and fits a signed 32-bit register. The ideal
discounted bound is 4,096 stored units, not a bound on corrupted words.
Explicit clipping on consumption now closes the damaged-reward ambiguity;
rounding/saturation implementation and full operation costs remain pending.

### Unresolved blockers and recommended follow-up

These are explicit freeze blockers, not concealed new findings or conditions
assumed already satisfied by the document-consistency pass:

* [ ] B02: Complete costed opcode and event order, preflight, finite bookkeeping, scratch/record lifetimes, partial or failed operations, paid retirement, response failure, terminal TD handling, and dead-row treatment. Include the selected abstention and all maintenance/no-maintenance tick modes.
* [ ] B03: Specify field-to-physical/upkeep-domain mapping, age rules, rent, hazards and correlated injury, resource conservation, caps, yields, and target-independent support, including H1 evaluation without allocator actions.
* [ ] B04: Fix reward units/mapping, observation thresholds, permitted-action handling, policy refresh, exploration indexing, tuning grids, and numerical edge cases. Preserve the now-selected live decoder and consumed-reward clipping.
* [ ] B05: Freeze arm/branch/channel products, maintenance and query schedules, pairing/streams, early counts, checkpoint context and row formats. Do not expose schedule lookup, due-cue repair, or past/future indexed inputs to the worker.
* [ ] B06: Establish prospective H1/adaptive headroom, viable selective spending, positive aggregate comparator denominators, and erasure containment assurance under actual forced-response, missing-response, support and dependence rules. Do not change gates after outcomes or drop zero-reference individuals.
* [ ] B07: Complete design-level interface/noninterference and operational review, including relevant source-access caveats, before a design-only freeze. Actual production-schema inspection and tests require separately authorized later implementation; a source/configuration/test/analysis freeze must precede untouched final individuals.

No clarifying author question remains for SC-001 through SC-004. The selected
revisions answer the prior offer, tie, validity, and scoring choices. B02-B07 need
separately authorized specification work rather than more interpretation of B01.
No model, implementation, design freeze, full protocol, erasure proof, resource
feasibility, or E3 performance result is approved by this closure.
