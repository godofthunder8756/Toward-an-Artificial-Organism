---
title: E3 B07 preimplementation information and structural review
description: Contract-scoped ownership, noninterference, erasure, finite ROM, and operational review
ms.date: 2026-09-10
status: Complete - conditional information-design pass; acceptance and implementation gates remain
---

## Executive disposition

Conditional pass for the selected information and operational DESIGN, not a
production noninterference pass, unconditional first-freeze approval, or an E3
result. The 2,464-bit machine and selected paid services admit a coherent
finite-state interpretation without hidden acquired storage. Accept that
interpretation only with the worker-frame/authority closure below, explicit
adoption of the completed service/ROM witnesses, and acceptance of the pending
oracle/evaluation-scope revision. A different implementation is not covered.

The two completed research notes close the previously named static service and
instruction-ROM gaps. Do not keep describing them as unexpanded, demand an E3
implementation to establish their paper bounds, or turn a positive H1/H2 outcome
into a prerequisite for freezing a falsifiable design. Actual implementation
conformance, generator/access checks, and scripted functional controls remain
later gates before engineering/final interpretation, not tests passed here.

No simulation, E3 worker, target draw, random generation, experiment, production
replay, or source edit ran. Only this review was written. Existing archive
proof sources, contracts, traces, manifests, and results were not edited.

## Scope and authority

Baseline: E3_STATE_CONTRACT_v0_2.md, E3_OPERATION_CONTRACT_v0_3.md,
E3_PHYSICAL_CONTRACT_v0_4.md, E3_POLICY_CONTRACT_v0_5.md,
E3_CONTROL_CONTRACT_v0_6.md, and E3_EVALUATION_CONTRACT_v0_7.md, read in full.
Read E3_PROTOCOL_v0_1.md for retained purposes, claims, and two-freeze rules.

E3_CONTROL_CONTRACT_v0_6.md incorporates CT-001 through CT-010 in
.copilot-tracking/reviews/2026-09-10/e3-control-review.md and the specified
parts of .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md.
Read both in full. Apply v0.6, then CT repairs, then incorporated trace, then
otherwise unchanged inherited rules. Earlier one-C estimates, V/A host-counter
interpretations, and unexpanded 232/64/112-slot estimates are not current proofs.

Read the completed .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md
and .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md in full.
The latter supplies the remaining services that the former explicitly excluded.
They are completed supporting witnesses, not self-authorizing amendments to
historical contracts. Their exact selected contents must join the design manifest.

Consulted .copilot-tracking/reviews/2026-09-10/e3-b05-review.md and the reset,
assurance, and freeze conclusions of
.copilot-tracking/research/subagents/2026-09-10/e3-b06-analysis.md. This review
does not independently certify every B06 numerical performance calculation.

V0.8 scope: the user reports oracle/evaluation remediation in progress. No
v0.8 contract was present in the initial filename search/root inspection.
No unseen v0.8 wording, new oracle trace, revised count, or acceptance is assumed.
EV-001 and EV-002 are inherited pending-acceptance dependencies, not newly
discovered duplicate B07 defects. All numerical archive counts below explicitly
describe v0.7, not a proposed v0.8 execution plan.

## Finding register

Major means a required boundary/acceptance condition before unconditional
information-design closure. Moderate means a bounded specification qualification
or conformance obligation. A conditional pass does not assert an observed leak.

| ID | Severity | Disposition | Subject |
|----|----------|-------------|---------|
| IF001 | Major | Accept only with explicit interface/authority schema | Worker, emulator, physics, evaluator and wrapper capabilities |
| IF002 | Major | Structural rule passes; implementation later | All-history reset, resources, fixed G and fresh children |
| IF003 | Major | Provenance/access acceptance condition | Four key classes, purpose roots and independent final targets |
| IF004 | Major | Replay/interruption acceptance condition | One-way archives, probe clones, hashes and resumable boundaries |
| IF005 | Moderate | Causal qualification accepted | Previous feedback affects current TD/action before due response |
| IF006 | Moderate | Physical rule passes; enforce exactly | Planned clocks, mortality, liquidity and simultaneous faults |
| IF007 | Moderate | Completed witnesses conditionally accepted | Finite typed ROM, addresses, scratch and counters |
| IF008 | Moderate | Matching/model limitations retained | Protected machinery, code-only injury and actual expenditure |
| IF009 | Major | Existing EV-001/EV-002 pending acceptance | Oracle and evaluation/archive scope; not duplicate findings |
| IF010 | Moderate | Claim and stage boundary | Design versus runtime proof, falsifiable outcomes and subjectivity |

### IF001 Typed authority is stronger than a small argument list

Evidence: state contract, finite live state and erasure; operation contract,
state/input constraints, packet inventory and scratch obligations; evaluation
contract, randomness ownership and checkpoint/context formats; protocol section 3.

The selected logical interface is adequate only if it describes everything
reachable by the executing worker. Passing a 276-byte argument while retaining
a target in a module global, callback closure, shared array, environment value,
open handle, exception object, host PC, or archived transcript does not comply.
No hidden queue, PRNG cursor, fifth arithmetic register, balance mirror, reserve
ledger, learned decoder cache, success bitmap, true age or event receipt exists.

Use these separate authority domains in the future implementation:

| Domain | Permitted information and authority | Forbidden return path |
|--------|------------------------------------|-----------------------|
| Paid worker/emulator | Exactly live RAM/reservoir state, 256 scratch bits, immutable G, public phase/tick/service shape, admitted current scalar inputs | Target, old state, raw archive context, arbitrary filesystem/network access, decoded cache or extra mutable host fields |
| METER/sensor/physical engine | Typed current reservoirs, current paid gate arguments, immutable quotes/routes; physics additionally current RAM/ages and current indexed fault inputs | Direct Y, true loss, correctness, original due cue, root keys to policy, old clean state or resource history |
| Evaluator/teacher | Target table, original scheduled cues, usefulness, emitted output; teacher sends only authorized LESSON labels | No target-bearing packet outside teaching or enabled ecological RESPONSE; no isolated timing/resource side channel |
| Input scheduler | Private target-independent schedules/roots and public planned clock | No historical/future cue-list lookup, key or run ID supplied to worker |
| Boundary wrapper | Fixed codec, public mode/permission selection, named interventions, fresh construction and clone lifecycle | No target-conditioned permission, quote, continuation, retry, or restoration |
| Archive/analysis | Complete state/context, lineage, outcomes, accounting and hashes after export | No callback, score, checksum, clone state, acceptance result or log-read capability back to a worker |

Separate evaluator and emulator capabilities, not just class names. A host
METER must not receive Y to decide affordability. In ecology it may consume
the explicitly authorized current yield quantity Y_E; that is an acknowledged
answer-bearing channel, not access to the label vector Y. Isolation/H1 has no
such quantity or signed b packet. Ordinary physics depends on current state,
G and independent inputs, not scorer truth. It may inspect current ages without
giving their vector to allocation or persisting a protected copy.

The wrapper has real privileged authority: it selects public service variants,
enforces modes, clones, resets, validates the fixed codec and routes current
messages. That authority must be immutable with respect to individual targets
and outcomes except for explicitly selected ecology/teaching. An opaque host
function that can choose arbitrary input packets is not an independence proof.

An isolated process with a serialized allowlist and no experimental-filesystem
read capability is the required implementation direction. Trusted code/G may
be loaded before isolation or supplied as a verified immutable image. Prevent
inherited target/archive handles, environment secrets, shared memory and network
access. This is a future noninterference/access-control obligation, not a claim
that Python encapsulation, process separation alone, or this review constitutes
an adversarial sandbox or timing-security proof.

### IF002 Complete reset covers every history, not selected survivors

Evidence: state contract, canonical values and serialization; physical contract,
typed placement and FULL-SOURCE-ENTRY; evaluation contract, complete erasure.

The complete persistent inventory is exact. Byte offsets below include the
twenty leading code bytes; bit offsets elsewhere in the contracts are auxiliary.

| Persistent field | Snapshot bytes | Bits | Ordinary treatment | Complete reset |
|------------------|----------------|------|--------------------|----------------|
| 80 code symbols | 0..19 | 160 | Paid code services; occupied sign flips and erasures | Every symbol 10; all twenty bytes 0xAA |
| 96 signed Q words | 20..211 | 1536 | Paid reads/TD, ordinary RAM faults even when frozen | Zero |
| Five full query slots | 212..216 | 40 | Paid admit/read/retire; cue/valid/reserved faults | Zero, including invalid payloads |
| Four teaching blocks | 217..220 | 32 | Paid merge/commit/retire, no authenticated validity | Zero |
| Previous transition | 221..224 | 32 | One record; reward/action/terminal faults | Zero, including reserved bits |
| Typed E | 225..226 | 16 | METER/sensor and physical sinks, not RAM XOR | Zero |
| Typed P0..P3 | 227..230 | 32 | Source-local cap/debit/deposit/sinks | Zero |
| Twenty ages | 231..240 | 80 | Paid increments/resets; cross-domain RAM faults | Zero |
| Cursor/counter/three flags | 241..242 | 16 | Allocated, fault-exposed, unused by selected policies | Zero |
| Inaccessible reserve | 243..275 | 264 | Allocated and fault-exposed; no agent access | Zero |

Persistent total is 2,208 bits. Scratch adds decoder96 + arithmetic128 +
control32 = 256 bits, for 2,464 allocated bits, not 2,464 persistent bits.
Of 1,104 serialized lanes, 24 encode reservoirs, 1,080 are RAM, 132 RAM lanes
are inaccessible reserve and 948 are accessible through permitted operations.
The 276-byte serialized image is not an extra live mirror of the five stocks.

Canonical reset is unpowered: code 10, every auxiliary bit zero, all scratch
zero. It is distinct from the next named activation to E=65535/Pj=255 and from
paid ISOLATE, which subsequently spends resources and clears only its 52 lanes.
Compare snapshots at matching stages, not unpowered S0 against activated state.
The zero dead flag in S0 neither provides power nor overrides physical E.

Normal ISOLATE preserves surviving code/Q/body/age/metadata/reserve information.
FULL-SOURCE-ENTRY replaces the five current reservoirs in a live historical body,
logs removals and supplies, but preserves RAM. Neither is complete erasure.
Code-only lesions preserve acquired policy/body history intentionally. Realized
stock distributions and accepted-income returns can depend on past learning;
they are acquired history even though ordinary opportunities are target-independent.

For every history H and fixed inherited G, require Reset(H,G)=S0(G), then the
same activation and future Z. Cancel old input/event/callback references, reset
the public phase origin and namespace, and start a new worker ownership context.
No old target, stock trajectory, pending reward, hidden random cursor or prior
history identifier is reachable by its transitions. Removal totals and old
payloads may survive only in outbound experiment records.

Let S include all live state and O all worker-observable outputs/availability.
Under a target-independent transition F and jointly target-independent fresh
input process conditional on fixed G, induction gives identical (S,O) for
identical S0,G,Z, regardless of past history. The proof covers emission,
rejection, resource and stopping behavior, not only emitted bit values.
Marginally target-independent inputs alone are insufficient if they encode a
complementary share of a retained secret; the full reachable-input composition
and conditional independence must hold.

Branch eligibility is also information. Nonnegative branches are planned for
all parents, including failed acquisition and dead histories. They cannot
receive full-source entry/refill/probe rescue when already dead. Preserve actual
E=0/uncleared RAM and all planned failure rows. Every designated terminal
nonnegative history, including dead, diagnostic, fixed, frozen and DRIVE,
still has its fresh complete-erasure child. No child recursively spawns another.

Fresh negatives normalize learning off and corrective permission on, retain only
their underlying inherited policy/cuts/period, and zero Q. A frozen child uses
the underlying RL rule with canonical Q, not a retained trained table. Parent
injury/support/usefulness calendars and success do not select reset inputs.
All-history reset checks hold G and reset panel Z fixed; comparisons across
different representations or different inherited algorithms need not match.

Selected G can depend on engineering outcomes, including engineering targets:
the chosen cuts or periodic interval I are then information about that training
population. Do not claim engineering target independence after marginalizing
over a refitted G. Compare changed histories while holding G fixed. Freeze
population G before independently drawing final targets and final private roots.
No per-history retuning or answer-selected final configuration is permissible.

### IF003 Four key classes, not four interchangeable seeds

Evidence: evaluation contract, concrete algorithms/keys, pairing and every-cell
indexing; policy contract, independent ranks; v0.6 POL-003 qualification.

| Class | Concrete ownership | Worker access |
|-------|--------------------|---------------|
| Target draws | Independent private 32-byte CNG draw for each individual; first sixteen bits are labels; separate final/engineering requests | Only paid acquisition labels and explicitly enabled task feedback, never the draw/key |
| Private external-purpose roots | Separate 256-bit roots for schedules, ordinary faults, challenge, exploration, guesses, U/O and injury placement, separately by cohort | Only currently admitted indexed values, never roots or future lists |
| Public pool/conformance key | 8f6c2a19d4b730e5a1c9087f62de4b03c5a87910ef26d4b7930a1e65c8f247bd | No role generating live schedules or targets; keep out of worker input |
| Public analysis key | 37b4e0a1c9625df80a7e413bd6982fc54e0137a965c2bd084fae1763908dc25b | Analysis only; no worker or physical decision |

These are four separate roles, not a recommendation to collapse seven private
purpose roots into one seed. Distinct purpose names on a worker-exposed target
seed do not provide independence. Separate requests are a provenance requirement;
coincidentally equal target tables remain allowed, without redraw/uniqueness
filtering. The unused 240 target-draw bits do not enlarge the 16-bit label entropy.

Retain the exact twelve-field canonical tuple, fixed absent values, integer
limits, HMAC-SHA-256, uint128 interpretation, unbiased rejection threshold and
external 1024-attempt limit. Input-generation failure is technical failure, not
an alternate label draw, a worker retry or a fourth T action. This review inspected
the declared algorithm; no CNG call, test-vector execution or implementation audit
was performed. Ideal independent draws support the mathematical argument;
CNG/HMAC provides a computational implementation, not literal information-theoretic
independence among all pseudorandom outputs.

Use phase/planned tick/purpose/location/slot coordinates, never action count,
guess count, successful operation count, wall time or a mutable worker cursor.
Unused exploration/guess/fault slots do not shift future draws. Different
branches share the prescribed underlying independent noise coordinates, not
different target information. Equal draws can produce different realized faults
when branches have different stored ages; pairing is not forcing identical
state-dependent damage or accepted cap-limited income.

U/O assignments are independent of labels, memory and success, paired across
D/C/codes/policies. C keeps the same U set. The worker sees current usefulness
only, not the map or diagnostic/branch identity. Reset keys omit parent-history,
branch and candidate-outcome identifiers, retain the selected RESET namespaces,
and do not inherit diagnostic calendars. IDs and lineage are archive locations,
not entropy or capabilities supplied to the worker.

### IF004 Archive, probe and interruption ownership must stay one-way

Evidence: evaluation contract, four H1 stages, full-state archives, immutable
run lifecycle; state contract, checkpoint and reset rules; ROM note, final S.

PRE/ACUTE/POST use disposable clones at fixed declared boundaries, with their
own paid 261-tick wearing assays, entry support and ISOLATE. Their results,
final state, resource residue, timing and success status never return to the
parent. The parent's planned clock does not advance by their 783 ticks. FINAL
is the actual recovered and challenged branch. The H2 prerequisite probe has
the same one-way clone boundary. No probe is a clean repair source or a cheap
host decode substituted for a charged query assay.

Snapshot/context writers and analysis callbacks must return None at the agent
interface. Host I/O acknowledgement, hash verification and backpressure may
affect host orchestration, but cannot become a scalar, simulated energy change,
branch permission, service budget, future-input namespace or elapsed model tick.
Preselect probe/intervention times; never stop isolation according to offline
correctness. Outcome-dependent host duration is not an allowed model sensor.

Hashes are not harmless worker metadata. A digest of a 16-bit target can be
dictionary-searched over 65,536 possibilities; a digest/length/name of acquired
state can also identify history. Keep target, checkpoint, context, result and
lineage hashes, byte offsets, file paths, timestamps and content-addressed names
outside worker reach. Only an immutable generic format/ABI identity belongs in
the input codec. No frame exposes unknown extra U/E fields as a catch-all:
usefulness is one declared offer bit, E is the typed reservoir or paid sensor,
and all extra telemetry fields are rejected.

Exact replay needs both the complete boundary state and restricted external
context: G/source/schema versions, public clock and next public service,
lifecycle, permitted future schedules/roots, intervention/permission calendar
and recorded delivery provenance. The resumer may read that archive, but must
construct the same narrow worker frames and never pass its context object,
target, root handles, old process objects or evaluator directly. Its independent
archive lineage does not change the simulated input namespace. New replay and
analysis destinations preserve old raw bytes, manifests and outcomes.

Interruption rules are separate from normal physical shutdown:

* A funded outer exit executes paid S, zeroing all 256 scratch bits and terminating without a subsequent PC increment, return-PC restoration or continuation write.
* Physical minimum failure sinks E and ends execution without pretending that unpaid clears/retirement ran. Discard terminated execution scratch; export only actual persistent shutdown bytes. This is not a paid successful S or a live resumable suspended service.
* A host exception or interruption during an atomic service is FAILED/PARTIAL, not biological death and not an excuse to fabricate remaining planned rows. Preserve partial evidence separately; do not serialize a hidden mid-service stack/quote as a normal checkpoint or silently zero it and call it complete.
* Resume/replay, if authorized, starts in a fresh process from an exact earlier completed public boundary and its matching external context, in a new labeled destination. Redo required work there; do not append retries into an immutable original run or grant an agent a checkpoint-restoration action.

Require exclusively new run directories, immutable STARTED and separate terminal
manifests, append-only finalized shards, and COMPLETE only after all required
technical checks. A scientifically failed but technically complete run remains
valid evidence. Source/archive hashes identify bytes, not proof that the
implementation obeyed this interface.

### IF005 Current response is causally downstream of old feedback

Evidence: operation contract, exact tick/controller order and RESPONSE ownership;
policy contract, task contribution and one-record lifetime; v0.6 Q reread rule.

The ecological causal ordering must be reported explicitly, rather than calling
all feedback merely future influence:

1. Previous tick's ecological response contributes b_(t-1) to its current record.
2. At tick t, paid offer/scan/sensor form s_t. Admitted TD consumes that stored record and can change current Q before action selection.
3. Selection rereads Q after TD, chooses action_t and executes before RESPONSE_t. A scrub can change the very storage that the current due response will decode; resource actions/spending can also change response affordability.
4. RESPONSE_t reads only its stored ring cue, emits, and is then compared with the externally scheduled original cue. Current b_t cannot cause an already selected action_t, but it finalizes the record of that action in the same tick.
5. Later TD can use b_t; at the public last learning tick scheduled TERMINAL can update the current record immediately with bootstrap zero, without an additional action, response, successor observation or invented tick.

Thus old task feedback -> current TD -> current action -> current due prediction
is an explicit same-tick causal path. No claim that current action precedes
all answer influence is valid. Current response b is ordinary one-step return
attribution to the current action, not delayed credit to the admission five
ticks earlier. The shared scheduled target table and paired external noise do
not add a branch-specific hidden label interface.

Learning ecology sends Y_E=64vc and b=64v(2c-1) only on a planned emitted response.
Emitted bit plus useful signed feedback can reveal the binary answer. Fixed and
frozen ecology omit b/record work but still receive answer-dependent physical
yield. Energy observations and affordability can carry that history forward.
All ecology can include relearning. No-code-write is not no-information.

Recovery and H1 omit BOTH feedback packets entirely, including zero packets,
resource consequences and outcome timing. Recovery freezes learning but retains
current surviving Q; H1 has no allocator offers/actions. Forced guesses occur
only for paid empty/tied readout and never seed correction. Invalid/rejected
decode still pays finalization/retirement where required; an internal default
b=0 is not a received packet. Spurious outputs produce no score, yield or b.

The current valid-record bit, not a clean controller-success flag, governs
learning RESPONSE finalization. Corrupted action=3 drops TD, not RESPONSE's
valid-record finalization. Stored terminal governs controller TD; scheduled
TERMINAL forces zero independently. These distinctions prevent hidden histories.

### IF006 The clock and mortality source are physical and exact

Evidence: operation contract, minimum tails/status and exact live tick order;
physical contract, tick order, simultaneous faults and typed losses;
evaluation contract, phase clocks and active/completion rules.

The public phase tick counts planned time, not successful operations or host
seconds. Tick one is each declared phase origin; periodic due is
((t-1) AND (I-1))=0. The five-slot position is (t-1) modulo five. Rejected
actions do not pause either clock or earn makeup service. Public time selects
fixed ROM entry and mandatory schedule, not a hidden earlier/future cue. Queued
query content is acquired RAM, never reconstructed from its external schedule.

Exact ordinary order is TICK; CONTROLLER when offered; RESPONSE; scheduled
ADMIT; AGE-LOW; AGE-HIGH; CONDITION-0 through CONDITION-19; last-learning-tick
TERMINAL if scheduled; simultaneous final fault and boundary export.
Acquisition instead has TICK, LESSON and scheduled BLOCK COMMIT, upkeep, fault.
No mid-operation fault or additional tick-end S is selected.

| Phase | Planned ticks | Admissions or teaching | Planned due responses |
|-------|---------------|------------------------|-----------------------|
| Acquisition | 256 | 256 lessons; 64 BLOCK COMMIT opportunities | None |
| Development | 2048 | Query admissions 1..2043 | 6..2048, exactly 2043 |
| Recovery | 128 | No query admission; current offers throughout | None; RESPONSE still runs |
| H1/probe | 261 | 1..256 | 6..261, exactly 256; sixteen per cue |
| H2 | 512 | 1..507 | 6..512, exactly 507 |

H2 endpoint responses and O-write accounting use ticks 257..512; endpoint
admissions are 252..507. The 256 endpoint rows contain exactly 128 U and 128 O.
Early responses number 251. All five drain offers at 508..512 remain, without
revealing due cues. No missed/invalid/dead response changes a planned denominator.

At every debit require current sourcewise R >= c+L+T+(1,0,0,0,0). METER charges
precede optional tests, including ordinary ADMIT/LESSON admission. Their outer
M dispatch to C or S is the named paid-dispatch exception to a worker BR, not
an unpaid pretest. Passive TICK support is the named preflight exception. Prepay both controller
Cs before control. Quotes reserve maximum routes/sources before paid address
discovery. Known paid scratch can narrow local L; earlier success/invalidity
never narrows public future T. Source surplus cannot transfer to another hub.

Debit before output/deposit. No E=0 cleanup or output is authorized, and future
action yield cannot finance its own admission. Stop at the first failed needed
write, retain completed writes, and reach the funded store/retire/S tail.
Releasing an unvisited suffix is not a refund. Conditioning promotes its whole
dues/two-write body before payment, preventing a funded-medium/unwritten-age
partial state. Whole-isolation minimum failure stops, not a free clear.

E=0 is absorbing for a historical phase. Minimum failure physically sinks the
remaining E; final leakage loses min(E,1), with independent min(Pj,1) source
sinks. No resource XOR, underflow or free stock creation is permitted. Diagnostic
dead/acquisition-failed/operation-failed flags do not decide survival, permission
or row eligibility. They remain fault-exposed and receive no unscheduled writes.
Selected policies do not secretly use the counter/cursor or archive status.

An active tick requires funded TICK and E>0 after the final physical step;
completion requires the horizon's final E>0 with no historical resurrection.
A response emitted before a fatal fault is scored even though that tick is not
active and completion fails. No TERMINAL rollback or posthumous update follows.
Canonical-new-state activation is the explicit exception, not resetting the old
dead flag and refilling arbitrary stale records. Boundary E and external lifecycle
must agree; inconsistent context is technical failure, not a second alive bit.

Fault probabilities use every CURRENT stored age after all operations, then all
RAM faults are applied simultaneously. An age damaged by this fault affects a
later tick, never another lane in the same fault. Age storage location can differ
from its described domain. No protected true age or old snapshot persists.
Ordinary RAM/reserve faults remain active even for unused/frozen/invalid fields.

### IF007 Completed service closure is finite under the selected ABI

Evidence: v0.6 operand/budget rules and incorporated CT repairs; completed
service-traces and ROM-closure notes, instruction, liveness and address sections.

Accept the stated fixed-slot abstract instruction machine. Packed extraction
is explicit, each operand at most 32 bits, D96 and four R32 words share the
existing control PC16/address11/flags5. Narrow MOV preserves neighbors; a
different native lowering must price its own instructions. No 40-bit operand,
call stack, hidden return register, mutable code bank or acquired program selector
is authorized. W alone occupies its five-bit scratch slot; its packed increment
is by 2^27 at D32..63. V comes from unrolled scratch PC and A is audit-only.

| Selected service | Executed CONTROL witness | Relevant independent work/limit |
|------------------|--------------------------|---------------------------------|
| Main learning BLOCK controller | A<=250, B<=246 | Two prepaid C256; DRIVE A<=253/B<=243 |
| Main learning REP controller | A<=223, B<=81 | No extra page or persistent traversal counter |
| BLOCK/REP scan | Administration 39/8 | Routed K=4039/119; every raw symbol read |
| Learning RESPONSE | BLOCK<=103, REP<=70 | 104 stored BLOCK control alternatives; D addressed through bit95 |
| Scheduled TERMINAL | <=80 | Independent outer service; 904 base/1121 full routed |
| AGE-LOW/HIGH | 63 each | Twenty reads/writes and eighty kernel ALUs per service |
| CONDITION-d | 9 admitted/5 rejected | Twenty fixed entries; no age read or scalar |
| TICK | 0 | Fourteen typed sites; five grant scalars, rent/living/S |
| ADMIT | 11 | Five public slot entries; rejection M,S only |
| BLOCK/REP LESSON | 33/38 | Paid staging transfer or five-write prefix |
| BLOCK COMMIT | 121 | Four public block entries; mandatory staging retirement |
| ISOLATE | 59 | All 52 writes; 1120 energy/13 material per source |

The service note supplies full scans, RESPONSE including absent-feedback
variants, independent TERMINAL and all 22 upkeep services. The ROM note supplies
TICK, five ADMIT entries, both teaching forms, four COMMIT entries and ISOLATE.
Its target-independent site bound is 24,902+1,499=26,401 within reserved capacity
27,936, highest reserved address 27,935. The existing sixteen-bit PC suffices;
address 65,535 remains unused. Even co-resident RL/fixed/DRIVE controllers fit
capacity 37,536 and demand <=35,877. These are storage bounds, not 26,401
executed CONTROL instructions or a claim that each execution region stores 256 sites.

Literal expansion, prefix-ordinal address assignment and named branch/STAGE
targets supply the static linking construction. A future emitted image must
have every target on an occupied typed site, preserve interleaving, and terminate
through S. Selecting the true finite image means freezing the actual selected
expansion, public variant map, constants and immutable quote definition, not
substituting a host helper of unknown work because there is address space left.
Mechanical emission/link checking is a later code-conformance obligation; a
runnable generator is not required to accept the paper construction.

G data is distinct from instruction text and from acquired state. It includes
1,104 placement/route rows, twenty columns, sixteen generic candidate constants,
twenty domain rows, and finite policy/tail constants. The ROM note gives a finite
future-tail table bound of 14,687,232 rows per variant and a loose local-tail
bound of 65,535 times 2^112 scratch/address/flag encodings. Those large finite
bounds do not assert feasible physical table allocation. Factoring is allowed
only with the same paid METER semantics and no hidden learned table or free
dirty-count/true-loss calculation. Reject overflowing or undefined G before
acquisition; do not invent a cap on generic data ROM that was never selected.

For the v0.7 optional 65,536-events-per-service bound, interpret an event as a
declared typed primitive/site, not arbitrary host instructions or debug messages.
Selected traces are finitely unrolled with no executed loop/backedge, so even
the whole 26,401-site demand is a conservative single-service site upper bound.
Adding 512 separately represented C-padding slots, eight separately represented
scalar records and one spurious-output record gives 26,922, still below 65,536;
this intentionally overcounts already typed work. Ordinary fault slots belong
to the separate physical-boundary record, not an unbounded worker service.
Freeze this event convention or recalculate if logging emits multiple extra
rows per primitive; the bound does not certify arbitrary METER internals.

The selected METER128, sensor16, attempt16, physical conditioning and atomic
scratch protection remain declared abstraction boundaries. No native instruction
or hardware energy proof follows. None of the paper closures permits a new
METADATA/refresh service or the currently disabled oracle without a new bound.

### IF008 Matching does not erase protected machinery or subsidy

Evidence: protocol sections 4, 5 and 9; physical placement/conditioning/support;
policy objective, fixed/frozen/DRIVE rules; evaluation branch catalog.

All arms retain 2,464 allocated bits and the same permitted observations,
opportunities, routes and physical laws in their matched comparison. Fixed rules
and generic decoder/update/clock/executor are inherited and protected; learned
Q, query/teaching/record/age/metadata are vulnerable. Atomic scratch is protected
within an operation but disappears at exit. Paid age conditioning changes a
declared hazard coordinate, not symbols, Q or a clean answer copy.

Equal capacity/opportunity is not equal actual cost. Fixed/frozen paths omit
unused learner work and packets; ordinary admitted learning versus frozen can
save twelve material per source before correction. No dummy writes conceal that.
Code-write-disabled branches preserve inference/exploration/scans/resources and
all required auxiliary work; selected scrub abstains after its paid gate.
DRIVE rewards selected scrub even if it fails, a different objective, not a
fair main-rival result. Any future oracle is privileged and separately labeled.

Primary H1 injury removes only 32 code symbols. Whole-hub injury additionally
removes mapped RAM/reserve and stocks; global resource injury only sinks stocks.
Do not claim policy/body were erased by the code-only lesion. H1-M/S/X are
explicitly saturation/null diagnostics under full entry and routine support;
equal outcomes do not show material restoration or independence from subsidy.
H2 g=36 does not by itself prove a forced useful-versus-obsolete code-write
tradeoff. Optional TD/conditioning, source collection, caps and fixed savings
remain relevant, as B06 explains. Retain failed positive-denominator and recall
gates; do not turn no observed O spending into successful percentage reduction.

The generic program does not need to survive physical E loss as a living
organism. Its instructions are protected; execution is permitted only while
the modeled energy rules allow it. Protected abstract computation, rent and
external funding are assumptions, not proof of self-produced machinery.

### IF009 Existing oracle and volume decisions await acceptance

Evidence: evaluation contract, oracle status, RAWCOUNT and freeze dependencies;
.copilot-tracking/reviews/2026-09-10/e3-b05-review.md, EV-001 and EV-002.

V0.7's zero-size oracle does not satisfy the retained privileged-positive-check
purpose. That is already EV-001. The user reports a v0.8 fix in progress; mark
pending acceptance, not a duplicate newly open defect and not an accepted fix.
Review its exact teaching authority, sourcewise quotes, finite service trace,
schedule, counts and restricted inference if enabled. The current 26,401-site
ROM witness explicitly allocates zero to the disabled oracle and cannot certify
an unseen oracle addition. Alternatively an explicit prospective amendment must
justify removal/replacement of that inherited purpose.

EV-002 already requires a branch-purpose and logical-versus-physical execution/
archive plan. The v0.7 totals recompute correctly:

| V0.7 planned quantity | Final | Engineering |
|----------------------|-------|-------------|
| Erasure children | 84,992 | 547,840 |
| Due-response rows | 49,982,464 | 320,444,928 |
| Tick rows | 64,250,880 | 412,296,704 |
| Checkpoint index rows | 65,223,680 | 418,568,704 |
| Logical 276-byte payload bytes | 18,001,735,680 | 115,524,962,304 |
| Outer-service slots | 1,620,049,920 | 10,394,044,672 |
| Ordinary indexed fault slots | 203,032,780,800 | 1,302,857,584,640 |

Together the logical state payload is 133,526,697,984 bytes before metadata,
responses and services. These are not measured physical disk requirements or
independent n. Sharding/deduplication preserves logical rows; skipping executions
or changing a candidate/control/reset product needs prospective scope acceptance
and equivalence evidence, not silent omission of currently planned histories.
All-history erasure coverage need not imply storing identical futures repeatedly
under a future approved alias plan, but mapping every source history and proving
canonical/equivalent inputs remain necessary.

Host compute, disk, bandwidth and optional cloud resources need a separately
scoped execution/encoding plan. Simulated energy is not host runtime. No cloud
provider deployment, runtime estimate, infrastructure change or arbitrary global
row cap is required for this information review. Preserve 32 final individuals,
eight panels, planned-denominator endpoints and existing gates unless explicitly
changed prospectively for scientific reasons. No archive proof source is modified.

### IF010 State-limited inference is not a subjective claim

Evidence: protocol falsifiable claims, protected machinery and interpretation;
v0.6 scientific qualifications; B06 gate disposition and freeze sequencing.

Before erasure, surviving representations can preserve target information and
paid ECC can copy it into damaged locations. Without a new answer-bearing input,
the complete reachable process cannot acquire additional information about an
independent target beyond surviving state and inherited prior assumptions.
This is a conditional information-boundary statement, not a claim that every
decoded bit, accuracy metric or redundancy level must stay constant. Feedback
ecology is deliberately outside that no-new-answer condition.

After true canonical reset under fixed target-independent G and fresh independent
inputs, target dependence is absent by construction/induction if the interface
is obeyed. The empty-code invariant is stronger and specific: flips do not
populate 10, erasures retain 10, empty scrub abstains, and readout guesses never
write back. It supports B06's independent-guess law conditional on admitted
emissions, not a universal independent-output theorem for every reset design.
Missingness/availability must be included; planned recall can be below one half
without an information leak. Chance accuracy cannot excuse an omitted state field.

Format, fixed codec, the sixteen-candidate generator, parity kernel, periodic
prior and target-independent G are inherited assumptions. No result means the
agent acquires a new information rate from material or invents its kernel.
The full 2,464-bit allowance is storage capacity, not 2,464 bits of independent
acquired target entropy; the target table has sixteen fair bits.

Pre-code acceptance requires a selected finite design, interfaces/quotes,
controls/estimands, prospective analytical limitations and explicit tests. It
does not require empirical proof that RL will beat periodic by five points or
that H2 will succeed. B06's warning about limited adaptive headroom and learner-
dominated scarcity is relevant negative design evidence, not a reason to tune
until positive. Functional controls and actual conformance are required at the
appropriate authorized implementation/engineering stages before final claims.

The scoped scientific description is conventional ECC plus ordinary allocation
under protected computation and external support. Neither success nor failure
here establishes subjective experience, wanting, consciousness, life, novel
algorithms, organizational closure, or E3b's developing neural substrate. It also
does not establish a universal negative conclusion about subjectivity. Those
questions are not operationalized by these bounded measurements. Completing this
review cannot honestly mean all possible research has been exhausted.

## Proposed exact worker-frame closure

This is a concrete acceptance recommendation, not an implemented or already
adopted codec. Adopt it or an equally explicit versioned schema before treating
IF001/IF004 as unconditional design closure. No field adds acquired capacity.

### Immutable process binding

Bind one validated finite G image and ABI before acquisition. Its representation,
policy algorithm, cuts, interval, objective, routes, domains, service permissions
and constants are generic configuration. Do not send a mutable G selector, source
hash, candidate-outcome ID or arbitrary host object on later frames. Phase-specific
variants derive only from the fixed binding and approved public mode schedule.
Final G is fixed before independent final labels; test reset equality with G fixed.

### Operation-boundary input record

Use a fixed 284-byte little-endian record at a completed outer-operation boundary:

| Offset | Field | Encoding and canonical constraint |
|--------|-------|-----------------------------------|
| 0..1 | schema_version | uint16, one frozen ABI constant, for example 1 |
| 2 | phase_kind | uint8: acquisition=0, development=1, recovery=2, assay=3, ecology=4 |
| 3..4 | planned_tick | uint16; 1..256/2048/128/261/512 by phase; zero only at selected entry ISOLATE |
| 5 | service | uint8: TICK=0, CONTROLLER=1, RESPONSE=2, ADMIT=3, BLOCK_LESSON=4, REP_LESSON=5, COMMIT=6, TERMINAL=7, ISOLATE=8, AGE_LOW=9, AGE_HIGH=10, CONDITION=11 |
| 6 | public_argument | RESPONSE/ADMIT slot 0..4; COMMIT block 0..3; CONDITION domain 0..19; zero for other entries |
| 7 | mode_mask | bit0 learning enabled, bit1 corrective code writes allowed, bit2 planned due response; bits3..7 zero |
| 8..283 | state | Exactly the 276 bytes above, all raw/reserved/invalid encodings preserved |

Service/mode/argument combinations must match the fixed public schedule. Commit
block dispatch follows the declared external acquisition block schedule, not
stored validity or a target. The due flag says only whether a query was planned,
never its cue, label or routing integrity. H1 and recovery have no feedback even
if a malformed flag requests it. Reject inconsistent/unknown fields or lengths
as technical errors, not silent coercion into a valid history.

Public clock/service fields are target-independent schedule coordinates, not
extra acquired state. They cannot encode a previous decision, successful gate,
return PC or suspended loop. The operation's acquired-dependent PC/address/flags
live only in its counted control32. No scratch is imported at an ordinary
boundary; it starts zero. The typed E/P bytes are deserialized as the sole stocks,
not copied into an additional mutable policy-visible balance object. The policy
cannot directly parse reservoir bytes or inaccessible reserve to bypass services.

### Current scalar records and delivery budget

For each requested current scalar use exactly six bytes: tag:uint8,
width:uint8, low-bits:uint32 little-endian. Width and signedness are fixed by
tag; unused high bits are zero. Signed b carries its sixteen-bit two's-complement
encoding and is explicitly sign-extended only by the paid instruction. No
variable payload, arbitrary metadata dictionary or extra success packet exists.

| Tags | Widths and allowed low-bit values | Authorized service/path |
|------|----------------------------------|-------------------------|
| 0 grant_E; 1..4 grant_P0..P3 | 16; 8 each, exactly selected offers including zero | TICK, five occurrences |
| 5 offer | 5, cue in low4/usefulness bit4 | Admitted CONTROLLER |
| 6 sensed_E; 7 sensed_local_P | 16; 8, actual post-charge readings | Paid SENSE in CONTROLLER |
| 8 rank_B; 9 rank_T; 10 rank_X | 1:0..1; 2:0..2; 4:0..15 | Every admitted RL selection, three independent values |
| 11 resource_request | 6, (action shifted 4) OR cue; action 0/1 | Admitted resource action, outbound |
| 12 forage_yield; 13 collect_yield | 16:0..64; 8:0..8 | Matching admitted action, one inbound raw offer |
| 14 readout_guess | 1:0..1 | Paid empty/tied RESPONSE only |
| 15 emitted_bit | 1:0..1 | Admitted RESPONSE, outbound |
| 16 ecology_yield; 17 learner_b | 16:0/64; 16:-64/0/64 encoded | Planned emitted development/H2 feedback; b only when learning |
| 18 admitted_cue | 4:0..15 | Successful ADMIT |
| 19 lesson_cue; 20 lesson_label | 4:0..15; 1:0..1 | Successful LESSON only |

These tag numbers and wire bytes are a proposed fixed codec, not newly priced
agent ALUs or additional input scalars. Existing scalar tariffs already cover
encoding/receiving; do not silently add agent decoding work without revisiting
the ABI. Sensor/READ2/WRITE2/METER continuations remain their declared typed
interfaces, not a way to smuggle another scalar. Accepted action yield is the
existing METER result in a live R word, not a new tag.

Never prebuffer all future/current service payloads in an uncounted worker array.
Deliver each value once at its priced instruction into a named scratch slot;
consume/release according to the liveness trace. At most eight scalar occurrences
span CONTROLLER/ACTION, with six on scrub, five/three for fixed resource/scrub.
Learning RESPONSE uses at most four; frozen ecology three; isolation/H1 two.
ADMIT one, LESSON two, TICK five, all selected remaining services zero. Omitted
feedback is absence of tags16/17, not a zero value delivered in isolation.

### Boundary outputs and capability exclusions

Return exactly 276 persistent bytes on funded normal completion, with S already
zero and terminated. Emit current bit/resource request only at its priced site.
Audit records are a separate outbound sink with no agent-visible return value.
Physical shutdown exports actual persistent bytes under the external lifecycle,
not a successful funded-exit record. Technical errors use the external failure
channel, with no resumable worker exception object.

Exclude target/root/analysis keys, individual/panel/branch/history names, scorer
cue/UO map/correctness, old snapshots, probe results, hashes, file paths, wall
clock, arbitrary callbacks, hidden packet buffers, host stacks/PCs, action-count
RNG state and permissions chosen from observed success. Host scheduling and
private key/context ownership stay outside the worker frame. The future source
inspection must verify these exclusions rather than assume the wire schema
enforces them by itself.

## Future trace-validator invariants

These checks are sufficient as a concrete conformance checklist for this selected
design when combined with full capability/source inspection and the compositional
argument. They are not a claim that finite tests exhaust histories, prove an
adversarial sandbox, or close every future scientific question. None ran here.

1. Assert exact byte/bit/lane layout, integer signedness and ranges; round-trip every raw/reserved encoding without normalization. No pickle or hidden fields.
2. Check all 2,464 allocated bits, per-stage D96/R128/control32 liveness, signed EX, raw subwords, packed W increment, and every primitive's read/write set. Disallow a fifth arithmetic word, saved balance, gate counter or old tuple.
3. Emit and type the chosen finite ROM; verify every sequential/branch/STAGE target, no padding entry/backedge/call/return, public variant selection, sixteen-bit PC, W<=20 and no acquired bank/index. Verify exact quote constants.
4. Bound each service and every public policy/mode variant by its CONTROL cap; charge both controller Cs including DECIDE rejection, do not charge them again per instruction, and separate typed kernels/accesses from padding.
5. Test every mandatory/optional prefix with sourcewise c+L+T+rho, including equality and one-unit-short cases, fees before tests, maximum unknown source, failed needed writes, same-value writes, rejected conditioning and all exits.
6. Reconstruct conservation from initial stock, accepted deposits, paid debits, overflow and typed losses by source; keep experimental removal/refill separate. No yield funds its own gate or retrospective refund; no energy-zero output.
7. Assert ordinary order, acquisition COMMIT despite failed fourth lesson, complete age pass before conditioning, scheduled TERMINAL independently, simultaneous pre-fault age use, and separate final leakage.
8. Test corrupted valid/cue/action/terminal/reward/age/metadata/reserve fields; action3 drops TD, invalid slot retires, valid record finalizes even on missing decode, age15 saturates, and no diagnostic flag controls life or eligibility.
9. Check exact signed TD roundEven including +/-64 and +/-192 numerators, corruption/saturation extremes, q survival, selection-row reread and all tie counts. Check T=3 as technical packet error, not a retry/action.
10. Check main returns a=-W/floor(F/4)/2C, current b finalization once, DRIVE selected-scrub return even on rejection, and frozen absence of record work. Demonstrate old-feedback/current-action/current-response causal order.
11. Validate packet allowlist, widths, source, timing and per-operation count. Omitted tags stay absent in recovery/H1; no original due cue or routing bit arrives. Readout guesses cannot write code or shift future input indices.
12. Audit independent target/purpose provenance, four key roles, canonical tuple encoding, HMAC known-answer vectors, unbiased uniform mapping and failure limit. Check same-purpose pairing under different action/guess counts and no target-key/ID/hash reconstruction path. Do not require unique target tables.
13. Check planned phase clocks and event keys including all drains/warm-ups; five-fault ring delay, original-cue scoring and no denominator shrinkage. Validate 3160 fault slots per physical boundary without reservoir XOR.
14. Test canonical reset through actual acquisition for all sixteen four-bit component tables, every one of sixteen production target-bit perturbations, cross-block cases, populated/corrupt fields, stock histories, messages and dead/live states. Hold G/Z fixed and compare every later byte/output/availability.
15. Validate empty-code induction and output/missingness together; no teacher, feedback, callback or Q path can populate an empty code bank. Check powered guard and undefined zero-emission panels without manufactured guesses.
16. Assert nonnegative dead branches are ineligible for reactivation but retain all planned rows; each required history still maps to a fresh canonical child. Normalize negative permissions and omit history-dependent reset namespaces.
17. Inspect process/module/handle reachability and evaluator/physics separation. Test forbidden frame extras, target/archive handles, timing/hash callbacks, reused evaluator objects and output-dependent scheduler decisions.
18. Fork disposable probe states and verify parent byte/clock/input-stream equality with and without offline observation; audit result/write sinks returning no worker data. Probes never act as repair templates.
19. Compare exact replay state, emitted outputs and ledgers in fresh processes using serialized boundary/context only. Test interruption at every service boundary and inside services; refuse hidden-state resume and preserve partial runs. No scientific failure or software exception becomes fabricated death.
20. Validate all planned key products/rows, no duplicate or missing logical lineage, dead/nonexecuted service rows, undefined metrics, uint64 counts, event-schema caps, immutable shards/manifests and new replay destinations. Revise products explicitly if accepted v0.8 changes scope.
21. Validate code-only/body/resource lesions, no-write/frozen/DRIVE/oracle permissions, matched opportunities, actual bookkeeping differences and saturated-control predictions. Future oracle validation is a separate bound.
22. Keep design acceptance, actual G-INFO/G-ERASURE tests, engineering controls, source/configuration/test/analysis freeze, independent final draw and scientific gate decisions as separate recorded stages. Never relabel a research note or statistical chance interval as a passed production boundary test.

## Acceptance checklist and remaining work

* [x] Review the full six-contract baseline and normative controller repairs.
* [x] Incorporate the completed service-trace and ROM-closure evidence with its scope.
* [x] Cover all state fields, stocks, keys, clocks, causal feedback, reset, clones, archives, permissions, mortality, paid prefixes and scientific claim limits.
* [x] Specify a concrete worker-frame/capability closure and future validator invariants.
* [ ] Accept/version the exact frame or an equivalent fully enumerated boundary; freeze generic constants, selected ROM/quote definitions and no-hidden-state rule.
* [ ] Accept the pending oracle/evaluation-scope amendment against EV-001/EV-002; inspect any new service/row product without reopening completed unchanged traces.
* [ ] Resolve prospective B06 freeze/scarcity wording using falsifiable claims, not guaranteed positive H1/H2 outcomes; preserve analytical cautions and gates.
* [ ] After design-only freeze and separate authorization, implement and validate source/capability isolation, emitted traces, every-prefix ledgers and exact reset/replay.
* [ ] Perform the authorized engineering controls/catalog, then independently freeze selected G/source/tests/analysis before final targets and private roots.

No factual clarification is needed to finish this review. Acceptance of the
proposed codec and the in-progress prospective revision remains an explicit
design decision, not implied by this conditional pass. No claim that all research
is exhausted, all gates passed, or implementation/execution is authorized follows.

## Verification and evidence identity

Only read operations, document reasoning and scalar integer arithmetic were used.
Recomputed the published v0.7 negative/response/tick/checkpoint/payload/service/
fault products, 2,464-bit allocation, RAM counts and 26,401/27,936 ROM bounds.
No data analysis of historical experiments, simulation, worker code, random draw,
bootstrap, kernel execution or empirical positive control was performed.

Read-only SHA-256 identities of the reviewed baseline and completed service notes
are below. They identify reviewed bytes, not a freeze, implementation certificate,
proof of privacy, or a claim about every historical archive file.

| Evidence | SHA-256 |
|----------|---------|
| E3_STATE_CONTRACT_v0_2.md | 0040c21e3b3a46e02000f0f9a201264a621a641686ca3658a6ed7fed3ae2e1bd |
| E3_OPERATION_CONTRACT_v0_3.md | f9aeb8595cc3ab0dfa47ea3f2c3f978f91c81eeb1f51f62aae62e83b5856b019 |
| E3_PHYSICAL_CONTRACT_v0_4.md | f0f05d57b5f98c171ff2956ca4bdfd00a59edfb3579d3fbe05fb74c8001e1dc8 |
| E3_POLICY_CONTRACT_v0_5.md | fe174d0bdb8d8d22583e426cf74ebb680d8d471a8c447f906a104819ded791cf |
| E3_CONTROL_CONTRACT_v0_6.md | 198c96c610d0fd89f9990836ad8b6d68aca13580b9ecad80b55cb5be962af060 |
| E3_EVALUATION_CONTRACT_v0_7.md | ea3698bdb595b66eeebf8f50a75b6514166bdfdb7bbaaa16c6392e7ef6e0dae3 |
| E3_PROTOCOL_v0_1.md | 5a551f004024ae59e60ae25b95ca60af61f2989fb33575c97aa774b81e804bef |
| .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md | 9d3b53757de35077b4973b619ea61bade1dc7f7c1c10edcd03b17251610a1e1f |
| .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md | c4cb49fb838834f21a125829615a073b58cae8a972fdeb33b548a459e94e4816 |

Full readback completed; editor diagnostics reported no errors. A read-only
comparison of all 34 baseline files found zero changed hashes. The baseline
covered the nine identified evidence files, E1_FREEZE.json, E2_FREEZE.json,
PACKAGE_MANIFEST.json, root Python sources, and files under e1/ and e2/.
This is a bounded preservation check, not a recursive audit of result archives.

Formatting inspection found editor-inserted tabs in wrapped list continuations;
the affected lists were flattened to single-line items in this review only.
No source, archive or contract change was needed. Final format/diagnostic recheck
is separate from the unperformed production tests. No v0.8 file was found in
the final filename search; its reported remediation remains pending acceptance.
