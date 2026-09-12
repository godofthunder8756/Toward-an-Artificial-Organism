---
title: E3a typed interface and complete compact archive contract
description: AC-01 and AC-04 design closure with explicit authority, binary records, input ownership, and exact replay
ms.date: 2026-09-10
status: Selected design closure only - implementation validation and other acceptance closures remain
---

## Authority and acceptance boundary

Select framed binary, not JSON, for the worker interface and raw records. Select RFC 8785 canonical JSON only for external manifests. This version closes AC-01 and AC-04 as DESIGN choices, including B07's ordinary information-interface conditions; it does not assert an implemented G-INFO/G-ERASURE pass, either freeze, experimental success, or completion of AC-02/AC-03.
Retain [E3_EVALUATION_CONTRACT_v0_8.md](E3_EVALUATION_CONTRACT_v0_8.md), its product, eight-byte responses, 48-byte ticks, sparse anchors, 8,567,308,288-byte ceiling, all 32 final individuals/eight panels, and every numerical gate. Replace only its underspecified codec/capsule/context fields as specified below. No historical source or observations are changed.
Precedence is this interface/archive specification for its scope; v0.8 for evaluation/oracle scope; [E3_CONTROL_CONTRACT_v0_6.md](E3_CONTROL_CONTRACT_v0_6.md), then its CT-001..CT-010 repairs, then its incorporated controller trace; the following newly adopted ordinary expansions; otherwise inherited v0.2-v0.5 and [E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md).
Adopt the complete technical instruction, liveness, branch, quote and linking sections of both service/ROM notes below, including TICK's paid continuation, ordinary admission dispatch, final S termination and DRIVE's resource-tail correction. Exclude their historical oracle-disabled/product totals and statements of then-outstanding work. W alone is worker scratch; V/A are outbound audit counts and unrolled-PC consequences. Use the repaired packed W increment by 2^27, not by one.

| Normative evidence | Exact SHA-256 of reviewed bytes |
|--------------------|---------------------------------|
| [Control contract](E3_CONTROL_CONTRACT_v0_6.md) | 198c96c610d0fd89f9990836ad8b6d68aca13580b9ecad80b55cb5be962af060 |
| [CT repairs](.copilot-tracking/reviews/2026-09-10/e3-control-review.md) | a01d2ad9d03f064028e3ac3eec0820c8c0ee85597e332af9d7cb891f9db74e95 |
| [Controller trace, incorporated sections only](.copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md) | 8c665e4533641066cdb3aa08bed4b6f25f0e8251a9a70cf5599c609858ca2566 |
| [Ordinary service expansions](.copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md) | 9d3b53757de35077b4973b619ea61bade1dc7f7c1c10edcd03b17251610a1e1f |
| [Remaining ordinary services and ROM](.copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md) | c4cb49fb838834f21a125829615a073b58cae8a972fdeb33b548a459e94e4816 |
| [Evaluation revision](E3_EVALUATION_CONTRACT_v0_8.md) | 36580bcb074e2f7e12a1708353dc9b2cefd845d5dc6a1bdd1fbbca8d7ec876a3 |

These hashes identify evidence and remain archive-only. The ordinary demand <=26,401/capacity 27,936 and optional co-resident-controller capacity 37,536 exclude the new oracle. AC-02 owns its exact scratch/entry/trap/quote/link amendment and oracle-inclusive bound; neither old number certifies it. No unpriced METADATA, refresh, new action, acquired program selector, or hidden helper is enabled.

## Complete authority and state inventory

Use a trusted byte interpreter whose interpreted program reaches only G, the current public header, paid current primitives, 276 persistent bytes, and 32 scratch bytes. Scratch is D96/R0..R3=128/control32=PC16+address11+flags5. The 2,464-bit allocation is unchanged. Host temporaries must not become another interpreted register, suspended PC, success flag, balance, queue, cache, or acquired object.

| Persistent byte interval | Sole stored field |
|--------------------------|-------------------|
| 0..19 | Eighty raw two-bit code symbols |
| 20..211 | Ninety-six signed sixteen-bit Q words |
| 212..216 / 217..220 / 221..224 | Five raw query slots / four raw teaching blocks / one raw transition |
| 225..226 / 227..230 | Sole typed uint16 E / four uint8 P stocks |
| 231..240 / 241..242 / 243..275 | Twenty ages / cursor-counter-flags / inaccessible reserve |

Preserve all raw invalid/reserved bits. Deserialization adopts the payload as the sole state, not a mirror plus separate mutable stocks. Only authorized READ2/WRITE2 see permitted RAM lanes; typed reservoir bytes cannot be read as RAM and reserve is inaccessible. The interpreter's host implementation is trusted, but an interpreted policy cannot parse the serialization buffer directly.
The scheduler owns only independent external-purpose roots and target-independent input schedules. The teacher/evaluator separately owns labels and original due cues. Physics owns current raw state, stored ages, independent indexed faults and typed losses; it has no target. METER sees current stocks, immutable quotes and paid current gate arguments, not truth. Only an enabled RESPONSE deposit receives current ecological Y_E, never the target vector Y.
The boundary supervisor owns public permissions, fixed intervention calendars, cloning and lifecycle. Its archive sink owns truth, lineage, outputs, hashes and ledger totals. Neither supervisor nor sink can choose future worker inputs, permission, retry, time, support or stopping from correctness, except the declared teaching/ecological channels. Whole-parent/context reads never become worker capabilities.
Future deployment uses a fresh separate process for each ownership context, with a serialized allowlist, immutable G loaded before isolation, no experimental-filesystem/network reads, inherited secret handles, shared mutable memory or secret environment.
A process alone, Python encapsulation, or this paper contract does NOT guarantee host compartment isolation, adversarial sandboxing, timing security or absence of implementation leaks. Source/reachability inspection and actual access tests remain mandatory.

## Exact framed worker codec

All multibyte integers are little-endian; booleans are 0/1. A frame is kind:u8, payload_length:u16, followed by exactly that payload. Reject unknown kinds, lengths, tags, ranges, duplicate/extra frames, out-of-order delivery and nonzero reserved fields. There is no extension dictionary, opaque object, pickle, callback, asynchronous closure, replay token or arbitrary byte attachment.

| Kind | Direction | Payload and exact length |
|------|-----------|--------------------------|
| 0 BIND | Supervisor to interpreter, once | ABI=9:u16, generic_format=1:u16, public_config_id:u16, capability:u16; 8 bytes |
| 1 BEGIN | Supervisor to interpreter | Header below plus sole persistent state; 284 bytes |
| 2 SCALAR | Direction fixed by tag | tag:u8, width:u8, low_bits:u32; 6 bytes |
| 3 EXIT | Interpreter to supervisor | Actual persistent state after paid S; 276 bytes |
| 4 SHUTDOWN | Interpreter to supervisor | Actual persistent shutdown state, E=0; 276 bytes |

BIND selects one immutable G from the public candidate-constant roster, not a mutable selector later. Configuration identity includes code, policy, cuts, interval, objective, routes and generic service definitions; it is identical across individuals using that G. It is NOT a run/target/history/winner-rank ID or artifact digest.
Capability=0 is ordinary; capability=1 additionally permits engineering TEMPLATE in phase 5. Grant it prospectively to the declared oracle harness, revoke by fresh ordinary construction before reset.
Public configuration IDs are fixed before outcomes: 200*code+100*family+k, code REP/BLOCK=0/1, family H1/H2=0/1. With ascending E/P/I indices e,p,i, k=3e+p for RL; k=9+9(3e+p)+i for PERIODIC; k=90+3e+p for THRESHOLD; k=99 for DRIVE. Final selections reference those same IDs, never freshly numbered winner slots. FROZEN binds underlying RL G with learning disabled. Capability and public mode do not change these generic identities.
One operation has BEGIN, at most eight priced SCALAR occurrences including outbound ones, and one EXIT or SHUTDOWN. No nested BEGIN, saved continuation or retry is legal. A process may serve a fixed finite sequence of completed operations; planned horizons bound that sequence. Technical interruption ends the invocation with an external FAILED/PARTIAL event, not a successful worker result or fabricated SHUTDOWN.

| BEGIN offset | Field and permitted values |
|--------------|----------------------------|
| 0..1 | ABI:u16=9 |
| 2 | phase:u8, acquisition=0, development=1, recovery=2, assay=3, ecology=4, off-clock oracle=5 |
| 3..4 | planned_tick:u16, respectively 1..256/2048/128/261/512; zero only for selected entry ISOLATE or off-clock oracle |
| 5 | service:u8, TICK=0, CONTROLLER=1, RESPONSE=2, ADMIT=3, BLOCK_LESSON=4, REP_LESSON=5, COMMIT=6, TERMINAL=7, ISOLATE=8, AGE_LOW=9, AGE_HIGH=10, CONDITION=11, TEMPLATE=12 |
| 6 | argument:u8, RESPONSE/ADMIT slot 0..4, COMMIT block 0..3, CONDITION domain 0..19; otherwise zero |
| 7 | mask:u8, bit0 learning, bit1 corrective writes permitted, bit2 planned response due; bits3..7 zero |
| 8..283 | Exact 276 persistent bytes; scratch starts zero |

Only fixed public schedule combinations are legal: learning in development or ordinary learning ecology; no RESPONSE/ADMIT/controller in acquisition; no controller in assay; no ADMIT or feedback in recovery; TEMPLATE only capability 1/phase 5/tick 0/argument 0/mask 0. Phase-5 ISOLATE also uses mask 0. Ordinary entry ISOLATE has no learning/due bit. RESPONSE's due bit reveals no due cue. Slot is (t-1) mod 5. Block COMMIT dispatch is its public grouped acquisition schedule, not stored validity.
The worker may know these target-independent phase/permission facts. It does not receive CORE/SCREEN/diagnostic names, lesion/sham identity, U/O map, parent status, selected cohort, root index or protected-physics selector. ZERO-FAULT versus LIVE-WEAR is physics-side only; both query workers receive the assay shape. Public clock never substitutes for an acquired PC, action counter or reconstructed historical cue.

| Scalar tag | Width and allowed value | Owner and authorized delivery |
|------------|-------------------------|-------------------------------|
| 0; 1..4 | 16; 8, bounded E/P grants | TICK, exactly five current offers including zeros |
| 5 | 5, cue low4/usefulness bit4 | Admitted CONTROLLER offer |
| 6; 7 | 16; 8, current E/local P | Paid SENSE pair only |
| 8; 9; 10 | 1:0..1; 2:0..2; 4:0..15 | Independent B/T/X, admitted RL selection |
| 11 | 6, (action<<4) OR cue, action 0/1 | Outbound admitted forage/collect request |
| 12; 13 | 16:0..64; 8:0..8 | Matching current forage/collect raw yield |
| 14 | 1:0..1 | Readout guess on paid empty/tied RESPONSE only |
| 15 | 1:0..1 | Outbound emitted RESPONSE bit |
| 16; 17 | 16:0/64; signed16:-64/0/64 | Planned emitted ecology Y_E; b only when learning |
| 18 | 4:0..15 | ADMIT after paid successful body gate |
| 19; 20 | 4:0..15; 1:0..1 | LESSON cue and label after paid successful body gate |
| 21; 22 | 4:0..15; 4:0..15 | Privileged TEMPLATE cue/payload; REP payload 0/1, BLOCK cue in {0,4,8,12} |

Signed tag17 carries its low sixteen two's-complement bits with high sixteen zero; paid signed EX extends it. Every other unused high bit is zero. TEMPLATE tags are separate from ordinary one-bit LESSON; exactly two deliveries, one energy each at X, only after M/body admission/C. Oracle rejection receives neither. Its legal input shape is selected here; AC-02 supplies the exact corresponding ROM sites and invalid-input traps, not a free fallback.
The only scalar receive primitive is current(tag), enabled by the current immutable opcode and its counted scratch PC. It consumes that packet once into the trace's named R/D destination. It cannot query a past/future packet, arbitrary tag, due cue, schedule, RNG root or query history. The adapter does not prefetch acquired-dependent values into an uncounted worker buffer; framing temporaries are inaccessible and do not survive consumption. No queue of current-operation payloads is retained.
Before paid offer/cue discovery, quote sourcewise maxima over all legal encodings. In particular an ADMIT helper cannot deliver a free current cue, and the controller cannot inspect an offered cue to select its initial cheaper quote. TICK's PASSIVE preflight is the sole selected grant exception. SENSE includes its two encoding charges in the sixteen tariff, not two extra I_G charges. Accepted action yield is the existing METER result in a live R word, not another scalar or reusable receipt.
Caps are RL resource/scrub 8/6, fixed resource/scrub 5/3, learning RESPONSE <=4, frozen ecology <=3, isolation/assay <=2, TICK 5, ADMIT 1, LESSON/TEMPLATE 2, all other services zero. No new current U/E telemetry is allowed: usefulness is tag5's single bit, and E is the sole stock or paid sensor. Both ecology tags are absent in recovery/H1; absence is not a received zero.

## Input provenance, resets and one-way observation

Keep v0.8/v0.7's exact checked Windows CNG requests, one private 32-byte target draw per individual, sixteen low label bits, and seven independently requested purpose roots per cohort. Target draws are not roots. Keep separate public conformance and analysis keys. Independent requests that coincide are retained. Final target/root draws occur only after the second freeze; selected engineering G is held fixed before those independent final draws.
Use the exact twelve-field RFC 8785 array: [version,cohort,individual,panel,family,phase,purpose,tick,location,slot,draw_index,attempt]. Version remains E3-EVAL-0.8 for inherited input law. HMAC-SHA-256, first sixteen digest bytes little-endian uint128, accept x<floor(2^128/m)*m, return x mod m; attempts 0..1023, then technical failure. Every numeric tuple coordinate is an integer <2^53. Raw root/target bytes never enter a worker, including through a shared seed, digest or handle.
Use planned tick/location/slot indices, not consumed guesses, successful writes/actions, wall time or mutable RNG cursors. Scheduler HMAC generation runs in its private domain and only current authorized packets cross the adapter. Archive full admission/offer schedules before execution and consumed provenance through original traces.
Preserve pairing and RESET namespaces exactly; history/product/branch/outcome IDs do not select reset Z. This is a computational realization of the ideal independent-input model, not an information-theoretic theorem about a PRNG.
Reset every designated actual source history, including dead/corrupt histories: new code bytes 0xAA, all other 256 bytes zero, scratch zero; cancel all old messages, callbacks, input references, archive/scorer handles and ownership contexts. Compare actual source reset before activation and after identical E=65535/Pj=255 activation. Normal paid ISOLATE and full-source entry are not all-state reset. Parent E=0 remains absorbing; only the newly canonical child is powered.
For fixed G and the same future Z, Reset(H,G)=S0(G); target-independent transitions then give identical state, emissions, missingness, funding/rejection and stopping for every history. All reachable inputs must be jointly independent conditional on G, not merely marginally independent. Different G need not have equal trajectories.
Resolve canonical-future sharing only after each source audit and required actual paired implementation comparisons; retain every source mapping and the fixed primary H1-RL-developed subset.
Snapshot, trace and analysis hooks are external one-way sinks returning no worker value. Active-frame audit may read the declared current state/scratch for validation but is not a resumable checkpoint, extra transient queue, continuation or callback. Backpressure/acknowledgment is host orchestration, never modeled time, energy, scalar, permission or RNG index.
Only completed S boundaries have resumable scratch=0; physical minimum failure preserves actual uncleared RAM and discards terminated scratch without claiming paid S.
Probe clones export only to the archive; no state, score, timing, resource residue or acceptance status returns to their parent. Parent clock and input namespace exclude clone ticks. All artifact/target/state/result hashes, paths, sizes, offsets, timestamps and truth IDs remain archive-only. Even a digest of a sixteen-bit label table permits a 65,536-entry dictionary attack. A fixed generic format/ABI identity is safe only because it is identical independently of targets and histories.

## Archive primitives and finite keys

Raw tables are packed binary, not per-row JSON. Byte offsets below are zero-based; packed fields are listed low-bit first. Integers are exact, checked, never saturating archive arithmetic. uint64 holds counts, aggregate debits and file offsets/lengths; state stocks remain uint16/uint8, rewards int16. Counters such as cumulative energy can reach trillions and MUST NOT use reservoir widths. Technical overflow stops validation, never omits a row.
Each table's global row ordinal is its key, never reset at a shard boundary. A directory entry is table:u8, codec:u8, record_bytes:u16, first_row:u64, logical_count:u64, physical_offset:u64, physical_length:u64, SHA256:32, four zero bytes: 72 bytes. Table IDs 0..13 are tick,response,snapshot,reset-audit,summary,lesson,COMMIT,template,schedule,phase,class,trace-commitment,G,provenance. Codec 0=dense,1=dead-RLE,2=exact-alias; no other values.
File names are deterministic table/shard ordinal names of at most 32 ASCII bytes, with no acquired text. Split at one million logical records, coalescing across phases, at most 1,024 finalized shards for the selected roster and its stage partitions. Directories may contain multiple ranges in a shard; no per-phase file is required. Files/ranges are external metadata, never worker input. No dictionary keyed by a favorable score or target-bearing name is permitted.

| ID/index | Width, bound and use |
|----------|----------------------|
| Individual / panel / cohort | u16 / u8 / u8; 1..8 or 300..331 / 1..8 / engineering=0, final=1; archive-only |
| Phase / snapshot / reset-class / trunk | u32; <284592 / <3818368 / <29696 / <29696, zero-based |
| Schedule / generic configuration | u16; <20480 / <512; schedule private, configuration public only as immutable G |
| Table rows / file offsets / fault coordinates | u64; exact v0.8 roster and indexed-input products |
| Service / ROM site / variant | u8 / u16 / u16; listed services, sites 0..65534, immutable generic variants |
| Absent reference | All-ones of its width; never a valid row ID; absence flags required for scalar values |

Archive lifecycle codes are LIVE=0, DEAD_AT_ENTRY=1, MINIMUM_DEATH=2, FINAL_LEAK_DEATH=3. Technical FAILED/PARTIAL is manifest status, not a biological-death code. Service path status is UNREACHED=0, REJECTED_OR_INELIGIBLE=1, COMPLETE=2, PAID_PREFIX_STOP=3; exact rejection cause is determined by raw state and the original committed trace. No numeric value implies that an unexecuted clear or update occurred.

## Tick capsule and raw scientific outcomes

A tick row is SHA256(actual 276-byte end state), 32 bytes, followed by this 16-byte capsule. This explicitly replaces v0.8's reserved bits and per-tick C counters, not its row size. Executed C counts move to exact phase totals and replayed primitive traces; no controller charge changes. Fields not reached are zero with the relevant status/consumption flag false, never a fabricated observation.
Exception: action=3 denotes no selected action; an actual zero-return forage is action=0, not absence. Replay distinguishes a partial raw read at physical failure from an absent read; a complete raw slot is published only when all its reads completed.

| Capsule offset | Exact field sequence |
|----------------|----------------------|
| 0 | last entered outer ordinal:5, lifecycle:2, funded TICK:1; ordinal31 means none |
| 1..4 | V:5, A:5, W:5, action:2, TD:2, stored-terminal:1, DECIDE-admitted:1, eligibility:1, old-valid:1, source:2, new-store:1, offer-consumed:1, target-correct code writes:5 |
| 5..8 | raw due slot:8, decode:3, emission:2, record-finalized:1, ADMIT:2, LESSON:2, COMMIT:2, TERMINAL:2, response decoded payload:4, controller health:2, E-bin:1, P-bin:1, guessed:1, ACTION-admitted:1 |
| 9..12 | CONDITION admitted mask:20, AGE completed mask:2, target-incorrect code writes:5, offered cue:4, offer usefulness:1 |
| 13..14 | Exact signed action return a:int16, zero if no action |
| 15 | Accepted current action yield:u8, 0..64 forage or 0..8 collect; zero otherwise |

Query-phase outer ordinals are TICK0, CONTROLLER1, RESPONSE2, ADMIT3, AGE_LOW4, AGE_HIGH5, CONDITION-d=6+d, TERMINAL26. Acquisition ordinals are TICK0, LESSON1, COMMIT2, AGE_LOW3, AGE_HIGH4, CONDITION-d=5+d. Unscheduled positions stay holes, never shift later ordinals. Off-clock ISOLATE/TEMPLATE each uses ordinal0; 31 means none. TD=0 absent/drop,1 rejected,2 nonterminal update,3 terminal-shaped update. Action=0 forage,1 collect,2 scrub,3 none.
Decode=0 unentered,1 invalid,2 unaffordable,3 empty,4 tied,5 unique; 6/7 invalid. Emission=0 absent,1 bit0,2 bit1; 3 invalid. Health uses h=0 empty,1 tied,2 intact,3 degraded; it is meaningful only after admitted DECIDE. TERMINAL's two-bit status is 0 unentered,1 ineligible/drop,2 funded clear with rejected TD,3 funded clear with admitted TD; a minimum failure has lifecycle MINIMUM_DEATH and no claim of a completed clear.
V/A/W belong to CONTROLLER in query phases and the single code-writing REP LESSON or BLOCK COMMIT in acquisition; BLOCK LESSON has staging writes, not another code prefix. Preserve 0<=W<=A<=V<=20, correct_writes+incorrect_writes=W. These two truth counts are observer fields recorded from ORIGINAL writes, never worker predicates.
A paid corrective write to canonical target sign counts as reconstruction when the prior symbol differed; a corrective write to a wrong sign is a miscorrection. Report wrong-payload scrubs separately by offline replay, not by pretending all parity-cell signs differ.
Preserve masks even on truncated physical execution; an incomplete AGE is not a completed AGE bit. Deterministic replay recovers its exact reached prefix and all per-service statuses. Header/raw fields are witnesses to compare, not permission to force replay decisions. Fatal-tick outputs remain scored while activity is zero. Spurious outputs are retained here with no target score or feedback.

Every planned due response has exactly eight bytes:

| Offset | Field |
|--------|-------|
| 0 | actual cue:4; status:4, 0=unreached,1=emitted0,2=emitted1,3=invalid-slot,4=decode-rejected,5=minimum-death,6=dead-entry |
| 1 | All eight raw due-slot bits if actually read; otherwise zero |
| 2 | target:1, correct:1, U:1, O:1, due usefulness v:1, routing-match:1, endpoint:1, planned-due:1 |
| 3..4 | Received learner b:int16, zero when absent |
| 5 | Raw ecological yield:u8, 0/64, zero when absent; not accepted deposit |
| 6 | b-present, yield-present, guessed, slot-read, alive-before-RESPONSE, alive-after-RESPONSE, active-tick, record-finalized; one bit each |
| 7 | original scheduled cue:4; upper four zero |

Planned tick, admission tick=t-5, slot and phase/ledger key derive from phase/shard order. Actual cue and routing-match are meaningful only with slot-read; target is the originally scheduled label, never the corrupted cue's label. U/O mark the prespecified H2 classes even in C; v follows that branch's actual usefulness.
Endpoint counts stay 256 H1, 128 U and 128 O H2; whole H2 has 507 rows. Correct is zero on all missing/dead rows. Source labels, U/O and truth counts remain evaluator-only and are cross-checked against replay, not inferred from an aggregate success statistic.
For non-H2 rows U=O=0. H2 early rows have endpoint=0 but retain their U/O class; H1/probe planned due rows have endpoint=1. Missing rows use their actual reason, not status0 in a technically complete phase. Raw slot validity is bit0; routing-match means actual cue equals scheduled cue, independent of validity.
For MIXED, retain per-cue U/O but report shared-block correction rather than fractionally allocating parity writes. Per-cue recall and active-only recall use the raw rows with their explicit denominator counts.

## Snapshots, teaching, template and reset records

A snapshot index is 32 bytes: phase:u32, tick:u16, kind:u8, lifecycle:u8, ordinal:u16, next_service:u8, flags:u8, payload_ref:u32, context_row:u32, boundary_rule:u32, payload_offset:u64; followed by 276 raw bytes, 308 maximum. Offset is u64; length is implicitly 276. A referenced payload is byte-identical and its offset/ref resolves to finalized bytes, never a resumable live object. Flag bit0=alias, bit1=scratch-zero, remaining bits zero; next_service=254 means physical fault,255 phase end.
Boundary kinds 0..14 are canonical, activation, raw fork, full-source entry, ISOLATE, lesion, intervention/sham, tick anchor, phase end, shutdown, pre-template supply, post-template, exact-code assertion, reset canonical, reset activation. Boundary rule identifies a frozen generic rule, not an outcome-selected intervention.
Retain all v0.8 named keys, every 64th tick, phase final ticks, and actual shutdowns; coincident keys may reference identical bytes. No hidden mid-service stack/quote is serialized as a checkpoint.
LESSON is eight bytes: scheduled cue:u8, received label:u8, status:u8, packed V:5/A:5/W:5/zero:1, staging-before:u8, staging-after:u8, flags:u8. Status 0 dead-entry,1 minimum-death,2 outer-reject,3 complete,4 paid-prefix-stop. Flags bits0..5 are cue-present,label-present,staging-read,staging-written,alive-before,alive-after; upper two zero. Absent label/staging values are zero with flags false. REP staging fields are absent. Keys derive from the 256 planned lesson ticks.
COMMIT is four bytes: raw staging:u8, status:u8, packed V:5/A:5/W:5/staging-read:1. Status=0 dead-entry,1 minimum-death,2 invalid staging,3 encoding-rejected,4 complete,5 paid-prefix-stop. Its 64 planned opportunities persist even after a rejected fourth lesson. Raw stored validity/labels, not a teacher-success bitmap, determine encoding.
The trace checks exact paid retirement; reconstruct staging-after from the tick/anchor replay. Its tick status projects 0/1 to unentered,2/3 to rejected,4 to complete,5 to prefix-stop.
TEMPLATE is 64 bytes: phase:u32, ordinal:u16, status:u8, code:u8; cue:u8,payload:u8,V:u8,A:u8,W:u8,flags:u8,executed-C:u16; pre-stocks:6,post-stocks:6; scalar-presence:u16,zero:u16; paid-energy:u64; paid-P0..P3:4xu16; event-count:u64; visited-mask:u32,written-mask:u32. Stock packing is E:u16,P0..P3:u8. Flags bits0/1 are alive-before/after, others zero; scalar mask bits0/1 indicate cue/payload. Status uses LESSON codes. Per-template material fits u16; cumulative material does not use that width.
RESET-AUDIT is 64 bytes: source_phase,source_snapshot,canonical_snapshot,activation_snapshot,class_id,representative_recovery_phase (six u32); source_lifecycle:u8,checks:u8,zero:u16,ordinal:u32; source SHA256:32.
Checks bits0..6 assert raw canonical equality, activated equality, scratch, messages canceled, handles/references canceled, G/Z normalization and actual-source audit; bit7 zero. All seven are required, with implementation evidence, not unconditional constants. Each source keeps its own row even when its canonical future is shared.

## Exact 512-byte phase accounting record

Every selected phase has one fixed 512-byte record, no silent union of incompatible field widths. Header: start-stocks:6,end-stocks:6,lifecycle:u8,flags:u8,zero:u16. Flags bits0..3 mean phase-complete, technically-validated, canonical-alias, off-clock; upper four zero. Phase identity is row ordinal. Sixty-two following uint64 counters are in this exact order:

1. Slots 0..23: planned ticks, entered TICKs, active ticks, planned responses, emitted responses, correct responses, endpoint U planned, endpoint U correct, endpoint O planned, endpoint O correct, completed code writes, target-correct code writes, target-incorrect code writes, Q lane writes, AGE lane writes, CONDITION age-lane writes, other RAM lane writes, admitted conditioners,
   executed C_A instructions, executed C_B instructions, executed other-C instructions, paid C_A envelopes, paid C_B envelopes, paid other-C envelopes.
2. Slots 24..53: six five-source vectors, each E,P0,P1,P2,P3: paid debits; accepted passive grants; accepted action income; physical leakage/shutdown losses; external removed stock; external supplied stock. Never net removal against replacement or autonomous spend against subsidy.
3. Slots 54..61: ecological offered E, ecological accepted E, ecological overflow E, external dispatch energy, forage offered E, collect offered material summed across hubs, admitted scheduled TERMINAL TD updates, paid code-prefix stops.

All counters are original-execution sums, checked against expanded replay. Every envelope counter includes rejected-body funded entries; padding is 256*paid_envelopes-executed_instructions, separately for A/B/other. Final stocks come from actual raw state, including dead states, not a rounded balance.
Per-gate c/L/T/status, individual source/routing debit categories, passive/action overflow, scan/abstention counts, returns and before/after-sign subclasses are exact derived ledger views from committed primitives, NOT guessed from this summary.
The fixed count schema is sufficient together with raw records and deterministic replay, not a claim that512 bytes alone contain every ledger row. Selected tariffs and supply caps give energy totals on the order of trillions, safely within uint64; all additions are checked.
Conservation uses initial+accepted income+external supply-debits-losses-removals=final sourcewise, with ecological accepted E added only to E. Offered/overflowed amounts are not deposits. Summary start-stock is before that phase's entry interventions; charge each entry/pulse once to its receiving phase. Shared executions count once in actual expenditure, with logical attribution separately identified.
A conservative realized-debit bound uses actual reservoir caps, not the signed-32 QUOTE ceiling: no individual debit can exceed Emax=65535. Even 28*65535 sites/tick *65535 energy/site *129,338,400 ticks =15,553,642,876,899,120,000 <2^64.
Boundary work is much smaller: <=3,818,368*1120 ISOLATE energy plus260,800 template energy, with <=1020 external dispatch energy per named boundary. Their sum also fits uint64. This deliberately loose bound is not a spending forecast.
Per-event c/L/T components remain nonnegative signed-32-compatible values stored as u32; aggregate counters and offsets are checked uint64, never a reused16-bit stock. Optional quotes exceeding current stocks reject rather than becoming enormous actual debits. Conservation gives much tighter selected totals in the trillions; no wraparound, saturation or truncation is permitted in either proof or implementation.

## Original trace commitment and sufficient replay

Do not store billions of padded service rows or an opcode archive. Select one streaming ORIGINAL execution trace commitment per phase, plus every tick's full-state SHA256 and raw scientific fields. A phase commitment row is event_count:u64, scalar_count:u64, SHA256:32 (48 bytes).
Initialize SHA256 with ASCII E3TRACE9, phase_id:u32 and archive G digest:32, then append the exact event bytes below in execution order; hash the stream once without reinterpretation. No checksum/CRC/truncated digest replaces SHA256.
Each typed event is192 bytes: tick:u16,service:u8,outer_ordinal:u8,site:u16,kind:u8,status:u8,event_index:u32,lane:u16,tag:u8,width:u8; pre-stocks:6,post-stocks:6; raw-before:u32,raw-after:u32; c,L,T(each five u32); flow(five u32); aux:u32; eight zero bytes; scratch-before:32,scratch-after:32.
Nonapplicable fields are zero; absent site/lane/tag use all-ones. Source/operand selectors derive from the immutable typed site. Event index starts at zero within each tick/off-clock operation; total event_count is u64. External observers alone own these records and their streaming hash state.
Kind 0..18 is CONTROL,KERNEL,READ2,WRITE2,SCALAR_IN,SCALAR_OUT,METER,C,S,SENSE,ATTEMPT,TRANSPORT,LIVING,RENT,DUES,MINIMUM_FAIL,PASSIVE,FAULT_BOUNDARY,BOUNDARY. Status uses the path enumeration. Access raw fields contain actual two-bit symbols; scalars contain their low-bit encoding; C aux is 0=A,1=B,2=other; CONTROL aux identifies that same budget, kernels never count as CONTROL. flow records actual deposit/debit/loss in the event's declared direction, never a signed uint alias.
CONTROL/KERNEL raw-before/raw-after are the destination's declared low <=32 bits; full scratch images disambiguate operands. For non-METER sites L/T are zero, not a claim of no reservation. METER stores the exact selected local/public quote at its test, including a rejected gate; c is its actual fee.
SENSE raw-before packs E low16 and P bits16..23 after the full sensing charge, raw-after is zero. ATTEMPT raw fields are zero because income arrives later; the existing paid cap/deposit continuation records accepted yield in raw-after. c contains only actual incremental debits, so paid continuation events do not charge M twice.
METER events commit pre/post stocks, actual debit c, exact L/T and outcome; S commits zero scratch AFTER terminating, without PC increment. Other sites commit their actual charged work, not reserved maxima. An entered optional gate is recorded even when it rejects. C records its one256-energy debit, not256 fictitious instructions.
Physical/experimental BOUNDARY events additionally append exact pre/post persistent bytes(276 each). aux packs boundary kind low8 and substep bits8..15: 0=no-op,1=removal,2=supply,3=RAM lesion/reset,4=assertion,5=sham dispatch; upper16 zero. The kind/substep fixes flow direction; invalid pairs reject. Indexed fault values and consumed scalar attempts regenerate from immutable roots/coordinates, not mutable cursors.
BOUNDARY direction is fixed by rule: removals and supplies are separate events, so both gross vectors survive a replacement rather than just a net stock difference. PASSIVE flow is accepted support; scalar records retain offered grants. Deposit/TRANSPORT continuation aux distinguishes action=0 and ecological=1.
FAULT_BOUNDARY flow is typed leakage; MINIMUM_FAIL flow is the remaining E sink. Pure RAM faults have zero stock flow. No truth label, hash or aggregate audit counter returns through these observer events.
For ordinary scalar events aux is the accepted external generation-attempt index (zero for deterministic input); the full purpose tuple follows from phase/tick/tag/site and frozen index rules. FAULT_BOUNDARY appends the same pre/post persistent bytes and executes simultaneous faults using post-operation stored ages. The original physical implementation and independent replay must agree; a hash recomputed only by the replay implementation is not original evidence.
Deterministic transitions from complete anchors, immutable G, exact lifecycle/calendar and complete private indexed inputs recover every path, raw write sign/address, output, received scalar, cost and intermediate state. Compare the ORIGINAL phase trace commitment/counts, each tick SHA256/capsule, all raw response/teaching/template fields and every summary counter.
Replay verifies raw correct/incorrect writes against target encoding and raw routing/correctness against the original cue. It may not branch on archived outcome labels to force agreement.
This proves representability without claiming the small capsule uniquely identifies a path by itself. Prefixes with the same V/A/W or identical end state can differ internally; their event streams, scratch, debits and raw outcomes are committed and independently replayed. No path-ID dictionary exponential in corrupt states is needed.
Finite no-backedge ROM and bounded service/scalar counts bound each stream; AC-02 must extend that fact to TEMPLATE. Mechanical emitter/link, trace, hash and round-trip tests remain unperformed.
Nearest-anchor replay checks every subsequent raw tick/state/output locally. To certify the phase-wide primitive digest, replay that entire phase from its saved entry anchor; a suffix alone cannot reconstruct a preceding SHA256 stream. Resume accounting likewise reconstructs the exact earlier phase prefix externally, without feeding counters to the worker.
Developed/fork anchors avoid reacquisition/retraining; neither a rolling hash host object nor hidden hash state is part of the worker checkpoint.

## Bounded shared context and lossless planned rows

Keep shared context within 67,108,864 bytes, using fixed packed tables plus canonical metadata, not arbitrary per-history JSON. Allocate the following hard capacities; unused bytes are zero and not a hidden object store. Actual rows retain their checked counts. Larger debug/native source/test bundles are separate labeled implementation artifacts; their immutable hashes and availability are required, not silently charged as core observations.

| Shared component | Exact capacity in bytes |
|------------------|-------------------------|
| 20,480 schedule records x 1,312 | 26,869,760 |
| 284,592 phase descriptors x 64 | 18,213,888 |
| 29,696 canonical-class/trunk mappings x 32 | 950,272 |
| 284,592 original trace commitments x 48 | 13,660,416 |
| 512 public G configuration records x 128 | 65,536 |
| Two generic typed ROM recipes, 65,535 x 16 bytes each, plus 32-byte header | 2,097,152 |
| Packed maps, rule definitions and scalar/trace dictionaries | 1,048,576 |
| Restricted root/target provenance block | 65,536 |
| Canonical manifests, bindings, source identities and shard directory | 1,048,576 |
| Spare directory/RLE capacity, never unspecified telemetry | 3,089,152 |
| Total | 67,108,864 |

A schedule is32-byte header plus1,280 packed cue bytes(2,560 nibbles). Header: ID:u16,individual:u16,panel:u8,cohort:u8,namespace:u8,phase:u8,length:u16,admission_count:u16,U_mask:u16,O_mask:u16,hub_permutation:u8,flags:u8,fourteen zero bytes.
Store one current cue per scheduled tick, including five drain offers; acquisition/recovery/probes fit too. Unused nibbles zero. Usefulness follows U/O and the fixed branch rule, not another hidden stream. Acquisition COMMIT block derives from that acquisition schedule outside the worker.
Schedule flags bit0=current-offers-present,bit1=query-admissions-present,bit2=teaching,bit3=whole-block-UO,bit4=mixed-UO; upper three zero. U/O masks are sixteen cue bits, zero outside ecology. The historically named hub_permutation byte is the current HUB injury source 0..3,255 when absent; archive the eight-panel assignment through those eight headers, not one byte pretending to encode the entire list. Query schedule length includes drains; recovery offers number128; acquisition lessons256.
Reserve64 schedule slots per individual/panel,320 cells maximum. Slots0..3 are H1 acquisition,H1 development,H2 acquisition,H2 development;4/5=PRE/prerequisite;6..14=SCREEN,SELECTED-CONTROL,CORE each recovery/FINAL/ecology;15/16=ACUTE/POST;17..24=LL13,FLIP,HUB,RESOURCE each recovery/FINAL;25..27=G-DIAG,HS-REFERENCE,MIXED ecology;28..31=H1/H2 RESET recovery/FINAL;32/33=oracle ZERO-FAULT/LIVE-WEAR.
Slots34..63 are unused. POST A/N and paired controls share their declared purpose; different indices never imply extra independent targets. Schedule ID=64*cell+slot, cells sorted cohort/individual/panel; phase selectors use the worker phase enum, except namespace distinguishes assay types. Acquisition admission_count=0, length256; its teaching count follows the teaching flag.
A phase descriptor is64 bytes in order: phase,parent_phase,trunk(u32 each);config,schedule(u16 each);reset_class:u32;individual:u16,panel:u8,cohort:u8;code,family,policy,product,branch,stage,permission,physics(u8 each);horizon:u16,g:u8,activation:u8;first_snapshot,first_tick,first_response,first_lesson,first_commit,first_template(u32 each);namespace:u16,zero:u16.
The six first-row values locate table ranges; lengths derive from phase rules and directories. Per-phase history exists only here, outside worker reach. Off-clock restoration horizon=0; its template count16/4 derives from code. Live g and ordinary grants follow the inherited phase/branch rules, including LL13 and H2 grid values explicitly stored in g.
Products 0..12 are TRUNK,SCREEN,SELECTED-CONTROL,CORE,LL13,FLIP,HUB,RESOURCE,G-DIAG,HS-REFERENCE,MIXED,RESET,ORACLE. Branches 0..13 are NONE,I,A,N,M,S,X,D,C,FROZEN-D,FROZEN-C,RESTORE,SHAM,EXACT. Stages 0..10 are acquisition,development,recovery,FINAL,PRE,prerequisite,ACUTE,POST,ecology,ZERO-FAULT,LIVE-WEAR; oracle restoration uses stage11. Physics=0 ordinary,1 protected off-clock,2 zero-fault query. Activation=0 none,1 canonical,2 live full-entry,3 privileged diagnostic replacement.
Permission bits0/1/2 are learning/corrective/oracle; upper bits zero. Namespace equals its schedule slot0..33;65535 means no schedule. Class flags bit0=alias, others zero. Phase IDs follow a prospective lexicographic roster: cohort,individual,panel,code,family,product,policy,candidate-slot,branch,stage,local-ordinal.
Candidate-slot is public k for trunks/SCREEN, fixed policy slot for selected/CORE, default k for diagnostics; no winner/outcome sorts IDs. Bind winning trunks afterward through immutable bindings; no absent probe is assigned a phase. Snapshot IDs sort phase,planned boundary position,kind,ordinal; extra shutdown slots use the preallocated per-phase final slot. Tick/response/teaching rows sort phase then planned tick, regardless of survival.
Class mapping is class,recovery_phase,final_phase (u32); config,recovery_schedule,final_schedule,individual (u16); panel,code,family,flags (u8); trunk:u32,zero:u32. Equal classes require identical complete G and normalized Z, not merely equal configuration labels/scores. Logical roster slots that alias reference one actual representative; every source reset still has its own audit and every logical phase retains its row/count mapping.
G record: ABI:u16,code:u8,policy:u8,family:u8,Pcut:u8,Ecut:u16,I:u16,h:u8,objective:u8,ordinary_permission:u8,zero:u8,variant:u16;scalar_rules,route_rules,domain_rules,tail_rules(u32);remaining96 zero bytes. Objective=0 main,1 DRIVE; policy RL/PERIODIC/THRESHOLD/DRIVE/FROZEN=0..4, but G uses underlying RL for FROZEN.
I=0 outside PERIODIC;h=3;ordinary_permission=3 is the maximum generic permission, further restricted by phase. Four rule IDs=0 select the single normative v0.9/v0.4/v0.6 rule set, not an unbounded dictionary. Variant=code selects one of two generic typed recipes; selected code/policy/phase specializes only public constants and entries, not acquired state.
ROM record is opcode:u8,flags:u8,destination:u16,operand0:u32,operand1:u32,operand2_or_target:u16,zero:u16. Opcodes0..13 are MOV,EX,SHL,SHR,AND,OR,XOR,ADD,SUB,NEG,CMP,SELECT,BR,STAGE;14..30 are the non-CONTROL/non-KERNEL event kinds above in their listed order. Every operand field is a descriptor ID, upper sixteen bits zero in u32 fields; SELECT uses operand2, BR/STAGE instead use literal target.
Flags bits0..1 select CONTROL budget A/B/other or kernel=3;bits2..4 for CMP select EQ,NE,LT,LE,GT,GE=0..5, otherwise zero;upper bits zero. Typed non-ALU opcodes have flags0 and their primitive-specific fixed operands. No implicit ALU, new lowering, or acquired bank is added; old trace operands and sites stay authoritative.
The one-MiB dictionary assigns65,536 bytes to maps/constants,786,432 to at most65,536 twelve-byte operand descriptors,and196,608 to suffix/variant recipes. An operand descriptor is kind:u8,width:u8,signed:u8,zero:u8,bit_offset:u16,zero:u16,literal:u32;kind0 scratch,1 literal,2 public header,3 generic G.
No arbitrary mutable operand or target table is admitted. Non-CONTROL opcodes use the exact named primitive semantics, not additional hidden ALUs. Quote recipes are backward finite sums/maxima of those same sites and already-paid predicates; the finite rule expression is stored, not the astronomical expanded tail table.
Widths are1..32,signed=0/1;unused offset/literal fields are zero. Scratch offsets0..255 name counted storage; public-header selectors0..6 are phase,tick,service,argument,learning,corrective,due. G selectors0..5 are Ecut,Pcut,I,h,code,objective. Literal and G/header descriptors cannot be destinations. Reuse identical descriptors, never allocate one per target/history.
Typed primitives use the same descriptor IDs for their named fixed arguments and public routes, not extra six-byte worker inputs. Inapplicable operand fields are zero. A32-byte ROM header is magic ASCII E3ROM09 followed by zero,version:u16=9,record_width:u16=16,two u32 image counts,and twelve zero bytes.
Placement has1,104 eight-byte rows(lane:u16,hub:u8,domain:u8,read_route:u8,write_route:u8,material_route:u8,flags:u8). flags0 RAM-accessible,1 reserve,2 typed reservoir;others invalid. Twenty eight-byte domain rows are id:u8,hub:u8,low_age_lane:u16,high_age_lane:u16,two zeros. Columns are twenty u8,candidates sixteen u8.
Membership/route rules follow v0.4 exactly, with no protected true-age table. Remaining map bytes are zero. Rule IDs0..14 match boundary kinds, with the trace substep distinguishing removal/supply. Variant recipes select only public code/policy/mode, never individual targets or acquired bank IDs.
Provenance contains forty independent target requests and fourteen purpose-root requests at the complete two-cohort maximum. Each128-byte entry is role:u8,cohort:u8,individual:u16,purpose:u8,three zeros,secret:32,API_status:u32,API_flags:u32,request_ordinal:u64,UTC timestamp:32 ASCII,remaining40 zeros.
Role0 target,1 root;target purpose/root individual are zero. Root purpose0..6=schedule,fault,challenge,exploration,guess,UO,injury. Timestamp is UTC ISO8601,zero-padded;no locale format. Public analysis/conformance constants follow separately. All provenance, including API failure evidence, stays archive-only.
Engineering records do not instantiate final secrets: final requests remain absent until the second freeze, then append in a separately restricted new cohort shard. An absent slot is an index reservation, not a zero secret or overwritten early root.
Metadata allocates at most1,024*72 directory bytes,1,024*32 filename bytes,32,768 binding bytes,262,144 source/environment identity bytes and524,288 canonical start/end/statistic-schema bytes:925,696 bytes,leaving122,880 within its one-MiB allowance. Large gate vectors/expanded analysis live in separately labeled derived output, not duplicated per-history JSON.
Before each authorized phase, resolve its complete schedule and append immutable bindings in its new run stage;no winner-dependent schedule invention. Unused draws/fault slots are algorithmically indexed, not materialized as billions of records. Static table sizes and finite recipe domains establish the selected representation;future source/codec validation checks emitted bytes against it.
Exceeding a capacity requires prospective versioning, not removing observations or declaring arbitrary source objects to fit. Finite counts bound recipes: one ordinary quote rule, one fixed table of service minima, public phase/permission specializations and the separately owned AC-02 oracle extension. Store selected rule text once with its digest; no per-history quote table.
Dead suffix RLE is optional,lossless and used only when shorter than dense records. A128-byte descriptor holds phase:u32,first_tick:u16,last_tick:u16,shutdown_snapshot:u32,lifecycle:u8,three zeros;six first_row:u64/count:u64 pairs for ticks,responses,lessons,COMMITs,anchors,service slots;expanded CRC32:u32;twelve zeros.
CRC32 uses reflected polynomial0xEDB88320,initial/final XOR0xFFFFFFFF,over canonical dense bytes in table-ID then row order;derived service slots use phase:u32,tick:u16,ordinal:u8,status:u8. The finalized shard directory supplies SHA256. CRC checks expansion,never replaces authentication or per-tick SHA256.
At most one maximal dead suffix per timed phase;if descriptors exceed spare capacity,use dense records. Expand every planned key,cue/target/U/O field,exact shutdown state/hash,absence reason and zero executed work;range counts are mandatory. Death may follow an emitted response on the fatal tick,which is stored separately.
Service slots expand from fixed order and actual stop ordinal. Technical exceptions preserve absent expected keys in PARTIAL manifests,never generate a dead suffix. Canonical aliases likewise preserve complete logical keys and cannot add bootstrap votes. All referenced states and records are immutable;no dead/favorable row deletion is allowed.

## Archive ceiling, immutable stages and committed statistics

The selected dense upper envelope remains129,338,400*48 ticks +111,393,280*8 responses +3,818,368*308 snapshots +225,200*64 reset audits +284,592*512 summaries +7,602,176*8 lessons +950,272*4 COMMITs +160*64 templates +67,108,864 shared bytes =8,567,308,288 bytes,8.567308288 GB or7.9789276123046875 GiB.
This is not a strict8.5-GB limit,host-runtime forecast or measured storage result. Expanded ledger/debug views,backups,SCRIPTED H2 and implementation fixtures have separate explicit budgets. Aliasing/RLE may reduce physical bytes,not logical completeness or planned precision.
A run is exclusively created at a new destination;existing/partial destinations are refused. Immutable STARTED manifest,finalized append-only shards/bindings and a separate terminal COMPLETE/FAILED/PARTIAL manifest form the lifecycle. Never edit STARTED to COMPLETE,append a rerun into original data or overwrite roots.
Canonical JSON has sorted RFC8785 keys,UTF-8,no insignificant whitespace,duplicate keys,NaN or infinity. Store uint64 quantities and exact rational numerators/denominators as decimal strings;IDs below2^53 may be JSON integers. Undefined values are null with an explicit reason. A technically complete scientific failure is COMPLETE with failed scientific gates.
Required manifest keys are schema,stage,status,sequence,parent_manifest_sha256,source_sha256,design_sha256,config_sha256,analysis_sha256,codec_sha256,planned_counts,actual_counts,table_directory,bindings,root_provenance_sha256,validation,scientific_gates. SHA256 is full 64 lowercase hex here only. Initial scientific results are null; terminal decisions include exact estimates/intervals and pass/fail/undefined reasons. Sequence is append-only orchestration, never a worker time input.
Replay/resume loads an exact earlier completed boundary and its matching private context into a NEW process and NEW destination. Reference the immutable origin's manifest, snapshot and namespace; destination/path does not change future Z. Redo interrupted work there, never import a suspended frame, zero away interrupted scratch and pretend completion, reacquire/retrain instead of loading the saved developed state, or feed replay comparison results back to the agent.
After source exists,implement statistics with exact integer/Fraction arithmetic: per-panel planned recall C/256 or H2 C_U/128;activity active/H;coverage emitted/planned;then equal mean of eight panels and32 individuals. Powered erasure uses each panel C/M,undefined if any M=0.
H2 O spending counts completed corrective writes at ticks257..512 to the fixed O class,not merely requests or all material. Ratios are ratios of aggregate means,with zero comparators retained and aggregate zero undefined;no epsilon or complete-case filtering. Development uses its2043 planned due rows for descriptive recall,not the FINAL256 denominator.
Use the fixed analysis key 37b4e0a1c9625df80a7e413bd6982fc54e0137a965c2bd084fae1763908dc25b. Bootstrap syntax is exactly ["E3-EVAL-0.8","final",0,0,"analysis","bootstrap","individual-index",0,0,0,32*r+p,a], r=0..9999,p=0..31,a=0..1023, uniform m=32 selecting ordered IDs300..331. One index matrix serves every paired contrast. Sort 10,000 exact replicate statistics; select one-based 250 and9750 without interpolation. Do not generate this matrix or run a bootstrap during design closure.
Compute common offline task b=64v(2c-1) only for emitted planned ecology, else zero, including fixed/frozen arms without a b packet. Use capsule a and exact r=clip(a+b,-256,256), J=sum_t (15/16)^(t-1)*r/256 as an external rational; never convert absent b into worker feedback. Published decimals are derived display only. Write every v0.8 scientific gate and candidate lexicographic selection as exact comparisons before final draws; keep engineering ranking data out of final intervals.

## Scientific qualifications and later validation

POL-001: missing responses contribute zero while useful wrong emissions contribute -64;below-chance emission can have less expected task return than silence. No silence action or learned avoidance is proved. Keep all missing/rejected rows in planned denominators and apply independent recall/activity gates.
POL-002: gamma=15/16 has scale16/half-life about10.74 ticks,not a hard cutoff or a guarantee of distant retention. POL-003: engineering-selected G may encode engineering experience;hold G fixed for reset and freeze it before independent final targets.
Previous feedback can affect current TD, current selection and current scrub before the current due response. Current b cannot cause the already chosen current action, but finalizes its record and may enter scheduled TERMINAL. Ecology is answer-bearing and may relearn; primary recovery/H1 is not. Code-only injury preserves Q/body history. Equal capacities/opportunities are not equal realized costs; fixed/frozen savings, full-entry subsidies and saturated M/S/X controls remain disclosed.
Adopt the qualified B06 analysis with AN-001: conditioners protect mandatory TERMINAL clear,not its optional two-material-per-source TD. The busiest-source mandatory-tail bound32 does not guarantee full final34. Adopt AN-002's illustrative PERIODIC probabilities0.619/0.204,not0.611/0.198.
g=36 does not prove all-region fixed-REP maintenance impossible or guarantee positive O-write denominators;the clean-reference H1 adaptive bound is not a universal no-go. Retain the conditional canonical-empty assurance >=0.996306 per code(>=0.992612 jointly),not a realized experimental pass.

* [x] Select exact ordinary/privileged scalar schemas, narrow public identities, all-state/capability ownership and ordinary normative witnesses: AC-01 DESIGN closed.
* [x] Select finite raw/status/context layouts, complete planned rows, original trace commitment, exact replay and the unchanged byte envelope: AC-04 DESIGN closed.
* [ ] Finish separately owned AC-02 oracle-specific linking/traps/quotes and AC-03 SCRIPTED H2 product before unconditional first-freeze acceptance; no old ordinary-ROM bound includes the oracle.
* [ ] First freeze only the accepted design and specified tests. Create no RUN directory, target/root files, source implementation or freeze manifest as part of this document-only closure.
* [ ] After implementation authorization, verify all codec/raw-state round trips; emitted ROM links and scratch lifetimes; both C budgets; signed TD and W; every sourcewise prefix; simultaneous faults; record corruption and invalid packet traps; audit sinks and process/handle reachability.
* [ ] Execute actual acquisition/reset tests for sixteen four-bit tables, sixteen production target-bit changes and cross-block/populated/corrupt/dead histories; check entire state/output/availability, cancellation, clone independence, raw truth fields, dense/RLE counts and exact sparse replay/interruption in new destinations.
* [ ] Only after technical validation, execute authorized engineering including oracle exact-code and separate zero-fault/live-wear checks, selected controls and SCRIPTED H2. Freeze G/source/tests/analysis/archive independently before final targets/roots. Scientific failure remains valid evidence, not permission to retune or delete.

No AC-01/AC-04 design blocker or factual user clarification remains within this scope. Runtime validation, the separately owned design closures and both freezes remain distinct obligations. Conventional ECC/allocation under protected machinery and external support implies no subjective-experience, consciousness, life or organizational-closure result, positive or negative.
