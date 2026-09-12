---
title: Independent E3 interface and archive review
description: Independent AC-01 through AC-04 design review with oracle, scripted controls, archive integration, and engineering-only disposition
ms.date: 2026-09-10
status: Complete - qualified engineering-only design GO; integration and confirmatory H2 blocked
blocked: true
---

## Executive decision

GO for engineering-only pre-code design completion and a falsifiable engineering
snapshot, after IFR1 integration and IFR2's explicit claim boundary. NO-GO for
unconditional freeze of the files as currently integrated, for E3 execution now,
or for confirmatory H2/fresh final draws. Neither freeze is performed here.
Finite paper-machine acceptance needs neither runnable generators nor positive performance.

AC-01/AC-02 pass scoped static review; AC-03 passes as a bounded diagnostic, not
as an established scarcity prerequisite. AC-04's base layouts and combined byte
arithmetic pass, but its extension catalogs/count schemas remain incomplete.
The exact core-plus-SCRIPTED ceiling is 8,595,571,712 bytes, not the core-only
8,567,308,288. Engineering failure is publishable evidence, not permission to
retune, delete failures, or proceed automatically to finals.

## Scope, independence and authority

This existing review is the sole research/closure artifact for the resumed task.
Read E3_INTERFACE_CONTRACT_v0_9.md in full (290 lines),
E3_CONFORMANCE_CONTRACT_v0_10.md in full (154 dense lines), and
E3_EVALUATION_CONTRACT_v0_8.md in full (592 lines). Read B07 and B05 in full,
including B05's latest appended v0.8 acceptance and AC-01..AC-04 exit conditions.
B05 already closes EV-001/EV-002 at purpose/product level; B07's earlier
missing-v0.8 statements are historical, not current blockers.

Read v0.6, its incorporated controller trace, CT-001..CT-010, and the ordinary
ROM witness. Consulted the service witness's typed-demand/link section; v0.7's
entire input-law section; v0.3's kernels/tails; v0.4's routes/opportunities;
protocol claims/two-freeze/scarcity sections; B06 review and sourcewise analysis;
and the conformance design research. Unchanged scan/RESPONSE/upkeep internals
and B06 probability/headroom proofs are inherited reviewed evidence, NOT newly
audited instruction-by-instruction or recomputed probability results here.

Independent checks cover new paths, widths, products, information flow and stages. Selected
precedence must include v0.10's explicit exceptions, v0.9's interface/archive,
v0.8's evaluation, then v0.6/CT/trace and adopted ordinary witnesses. Exclude old
oracle-zero products and stale outstanding-service statements. No E1/E2 result,
data file, secret, E3 runtime, generator, bootstrap or experiment was inspected/run.
Only deterministic scalar arithmetic and document hashing were executed.

## Independent acceptance details

* AC-01: Accept exact state/frame/ownership design; actual access/generator tests unperformed.
* AC-02: Accept oracle scratch/prices/quotes/traps/ROM; no emitted-image or oracle pass.
* AC-03: Accept bounded learning-bookkeeping diagnostic; not a fair rival or scarcity proof.
* AC-04: Accept core codec and combined arithmetic; IFR1 integration blocks unconditional freeze.

### AC-01 information boundary and complete state

Persistent 276 bytes = 2,208 bits; scratch 32 bytes = D96/R128/control32;
total 2,464 bits. Typed stocks are the sole E/P state, not a serialization mirror
or RAM-readable balance. Preserve invalid/reserved RAM; no extra queue, host PC,
success ledger, clean age vector, acquired bank, or fifth register is permitted.
W's packed increment remains 2^27; V/A and truth counts are observer-only.

The three-byte frame header is kind:u8/length:u16. BIND/BEGIN/SCALAR/EXIT payloads
are 8/284/6/276 bytes, framed lengths 11/287/9/279. At most eight scalar
occurrences give 638 bytes per completed operation, excluding the once-only BIND.
BEGIN's eight-byte public header plus state fits exactly. Mode bits0..2 alone
encode learning/corrective/due; due exposes no cue. ABI9, capability1, phase5,
tick0/service12/argument0/mask0 identify TEMPLATE without a diagnostic-name input.
Unknown lengths/tags/high bits/order/extras reject; no arbitrary metadata extension.

Scalar direction/site/width is fixed. RL resource/scrub <=8/6; fixed and scripts
<=5/3; learning RESPONSE <=4; TICK5; LESSON/TEMPLATE2. Signed b uses low16 plus
paid sign extension. SENSE's two encodings are already priced, accepted action
yield is the existing METER result, and absent H1/recovery feedback is no packet,
not a received zero. No new unpriced E/usefulness telemetry is introduced.

Before paid cue/address discovery, quotes use sourcewise maxima; source lookup
cannot peek at the scheduler/target. TICK PASSIVE and paid admission dispatch
are the named abstractions, not general permission for free pretests. Private
CNG target requests, seven independent purpose roots per cohort and separate
public conformance/analysis roles remain distinct. The twelve-field RFC8785
HMAC tuple, little-endian uint128 rejection and 1,024-attempt abort are specified,
not implemented/validated. Planned indices, not action/guess counts, select draws.
Joint conditional input independence is required; HMAC supplies a computational realization, not an information-theoretic theorem.

Scheduler roots/schedules, evaluator labels/original cues, lineage, context keys,
hashes, filenames, offsets and truth counts stay private/external. BIND G IDs
are prospective generic configurations, never target/history/winner identities.
Target-bearing digests are not harmless worker metadata. Prior ecological b can
affect current TD/action/response; current b cannot change an already chosen
action. Only declared teaching/ecological channels carry answer information.

All-history reset makes code0xAA/other256 bytes zero, cancels old references and
messages, then identically activates a fresh child. Dead parents stay dead.
ISOLATE is not reset. Same G/Z implies equal state, predictions, availability and
stopping across histories; changed labels can change scores, not predictions.
One canonical future per equivalence class is not one global future or new n.
Actual-source audits and paired implementation checks precede reference sharing.
One-way clone/audit sinks, new-process/new-destination replay and actual S
termination forbid observation feedback or hidden suspended checkpoints.

### AC-02 oracle paths and sourcewise proof

The source is actual H1-RL-default SCREEN A post-lesion, including dead/corrupt
cases. Privileged clone replacement plus paid ISOLATE preserves Q/ages/metadata/
reserve; it does not initialize a clean bank. Two once-consumed tags21/22 enter
R0/R1 after paid admission/C; no callback or full label table enters the worker.
Width-valid REP payload>1 or BLOCK unaligned cue takes the paid BAD exit; other
malformed framing is technical failure. Neither path silently masks/retries.

Cue D0..3, payload D4..7, base D8..14 and expected D16..17 use 17 named bits,
highest bit17, within D96. Gates may clobber R0..R3, not expected/base/address.
REP base=20*(cue>>2)+(cue&3), offsets4i; BLOCK base=20*(cue>>2), offsets i.
All addresses lie in0..79; only the local source pays material. No V/A/W worker
counter or target-indexed ROM is needed. Full CONTROL=19+6n gives49/139;
reserved40+6*20=160<=256. Body reject executes M/S only; bad path <=9 CONTROL.

Stored sites=26+(g+8)n gives71/306. EXIT offsets66/301 lead to BR67/302,
normal S68/303; BAD69/304 leads to S70/305. Last-cell edges and rejection
targets remain occupied in the same segment; S clears without PC advance.
Intervals [37536,38048), [38048,38560) extend the adopted co-resident ordinary
layout. Demand<=35,877+377=36,254; highest reserved38,559<65,535<65,536.
Old capacities27,936/37,536 exclude this addition. PC16 suffices without new RAM.

Prefix price=394+gV+128A+23W, V=A, W<=A<=n. Full1154/3534, bank18464/14136;
first-write energy requirements548/2578 include remaining gates/generation/S
and residue. Each gate pays before testing; first failure retains its prefix
and releases only unvisited obligations. Before discovery use sourcewise maxima.
T=0 only in protected off-clock restoration. No intra-template supply occurs.
Each pre-template replacement is logged gross, including1020 dispatch energy;
post-input E65149 leaves64381/62001 and local P250/235 after full completion.

Immediate all80-symbol equality precedes faults/probes. ZERO-FAULT has conditional
256/256/full-activity coverage; LIVE-WEAR has no100% gate. Counts remain16 cases,
eight independent tables,32 probes,160 templates,1,280 writes,260,800 template
energy,8,352 ticks,8,192 responses,48 ISOLATEs/audits, no added oracle future.
Revoke capability before reset. These are predictions/counts, not observed passes.

### AC-03 scripts are conventional diagnostics, not efficient rivals

512 ecologies =2 codes*8 individuals*8 panels*2 scripts*2 budgets, g36/66.
Use actual H2-RL-default developed trunks, no new acquisition/development, clean
Q, oracle restoration, winning-trunk substitution or dead-parent rescue.
Immutable-G rebind changes the generic selector, not inherited acquired bytes.

The literal selector correctly reads e=D47, p=D46, h=D44..45, u=D48; priority
is low-E forage, else low-P collect, else h3 scrub with u1 for U, otherwise
forage. ALL omits only usefulness restriction. Twelve instructions plus one
STAGE replace ALL E39, not a post-selection override: BLOCK A224/B246,
REP A197/B81; resource A216/B33, stored-terminal BLOCK A193/B246.
Using conservative16 gives A227; there is no unexplained fourteenth instruction.
DECIDE rejection stays22/2 learning or4/2 disabled, with both prepaid Cs.

Remove E's Q-selection reads, rank receives/saves/check/EX handoffs and selection
kernel together. No still-live random-rank handoff remains. Literal270 kernel
MOVs pay99 intrinsic selection +24*7 routed-read energy +3 encodings, not99 alone.
They are unused diagnostic energy, not genuine Q selection or fake packets.
TD/Q writes, record retirement/store, RESPONSE and scheduled TERMINAL remain real
paid learning work. Q does not choose script actions. All32 observation states
and corrupt/drop/reject paths are later test cases, not executed tests here.

Script storage<=4,738+13+270=5,021<9,600 in [4800,14400), replacing the two
optional fixed/DRIVE regions, not adding a fourth co-resident controller.
Noncontroller/templates remain fixed; full script-image demand<=31,799 within
38,560. Four new public G IDs400..403 fit the existing512 capacity; different
script G never aliases to ordinary RL or to equal-score policies.

Energy envelopes29,275/29,395<30,000 are financial, not recall proofs. Ordinary
preconditioning material24/source plus REP<=5 gives29; mandatory final clear
raises the busiest bound to32. AN-001 forbids promising optional final TD34
after conditioning. Ordered source-local conditioner vectors, accepted deposits,
actual overrides/returns and prefix failures remain unchanged. Both Cs cost512;
no added scalar, write, ninth override or hidden helper is required.

### AC-04 raw records and independently recomputed additions

Capsule four-byte groups each sum32 bits; total128. Response8, snapshot32+276,
audit64, template64, summary16+62*8=512, trace192 and directory72 fit. Presence/
lifecycle fields distinguish absent, rejected, partial, dead and actual zero.
Original primitive commitments plus anchors/G/private indexed inputs, not the
capsule alone, recover internal paths, signs, routing, costs and truth counts.
Whole-phase replay verifies its digest; nearest-anchor suffix alone cannot.
Dense/RLE/alias expansion preserves every planned row and fatal-tick output.

With K512/R256/N512: delta L=512K+389R; F=507K+256R; U=N+2R;
B=12K+13R+2N=10,496; Bmax=B+U=11,520. Reset shares two budgets only after
512 source audits; 256 futures each have128 recovery+261 FINAL. No recursive
negatives, additional targets, primary-erasure votes or confirmatory script CI.

| Quantity                  | Core        | Script delta | Combined    |
|---------------------------|-------------|--------------|-------------|
| Planned ticks             | 129338400   | 361728       | 129700128   |
| Planned responses         | 111393280   | 325120       | 111718400   |
| Phase summaries           | 284592      | 1024         | 285616      |
| Maximum snapshots         | 3818368     | 11520        | 3829888     |
| Source reset audits       | 225200      | 512          | 225712      |
| Canonical-future roster   | 29696       | 256          | 29952       |
| Paid ISOLATE slots        | 254896      | 1024         | 255920      |
| Offered controllers       | 94633984    | 294912       | 94928896    |
| Planned outer services    | 3311370832  | 9303040      | 3320673872  |

Script record bytes: ticks17,362,944 + responses2,600,960 + snapshots3,548,160
+ audits32,768 + summaries524,288 =24,069,120. Context4,194,304 gives28,263,424.
Core8,567,308,288 + delta28,263,424 =8,595,571,712 bytes =8.595571712 GB
=8.00524997711181640625 GiB. No compression/death/winner overlap is assumed.
Core context64 MiB plus extension4 MiB is71,303,168 bytes; not per-history JSON.
Lessons7,602,176/COMMITs950,272/templates160 and trunk roster29,696 do not change.

Added ordinary fault slots1,143,060,480 give409,839,208,320 including oracle
LIVE-WEAR only. Added reset challenge20,480 gives5,918,720 primary/reset,
or5,980,160 with existing FLIP61,440. Each controller C has added funded-debit
ceiling75,497,472, both150,994,944; offers are not actual funded work.
Even the enlarged loose tick debit bound plus boundary envelope is
15,597,142,635,599,251,520<2^64. Exact checked uint64 aggregation remains required.
These are finite representation bounds, not measured disk/CPU/runtime performance.

Final n32/eight-panel weighting, H1 C/256 and H2 U/O C/128 remain unchanged.
Keep exact rational paired-individual statistics, zero comparators undefined,
missing/dead rows retained, and the fixed primary H1-RL-developed erasure subset.
No new bootstrap matrix or assurance calculation was generated here.

## Findings and exact owner fixes

### IFR1 blocking integrated AC-04 catalogs and count schemas

V0.10 explicitly leaves integration to its owner; v0.9's frozen maxima and
product0..12/policy0..4/namespace0..33 reject the new product as written.
Before unconditional first freeze, adopt a versioned extension defining product13,
policies5/6, slot/namespace34 and G400..403, including G policy validation and
generic script-rule specialization. Keep family H2; expose no SCRIPTED identity
in worker frames. Do not pretend the new G/path counts fit old class/phase limits.

Fix v0.10's integration/count-schema section or the subsequent normative
integration artifact: append phases[284592,285616), classes[29696,29952),
snapshots[3818368,3829888), and corresponding tick/response/audit ranges from
the table. Preserve old semantic keys and all aliases; trunk bound stays29696.
Schedule34 occupies reserved per-cell space within20480; four Gs fit512.
Specify unique global ordinals across extension shards, their directory bounds,
1,024 descriptor/trace/summary rows,256 class rows,64 schedules and4 G records.
The allocated extension components plus841,216 spare sum exactly4 MiB.
Append combined planned/actual count schemas, services/fault/challenge/C bounds,
byte ceiling, script gate outcomes and separately labeled actual-versus-logical
expenditure. No existing manifest, root acceptance document or contract is edited
here. Larger fixtures/debug/backups require separate budgets, not missing rows.

### IFR2 blocking stronger confirmatory H2 scarcity interpretation

Fixed/frozen REP demand28+5=33<=36 finances all-region maintenance and full
conditioning. This refutes universal forced financial sacrifice, not accurate
recall. Genuine learner overhead/padding cannot rescue that universal premise.
V0.10's ALL-fails/U-succeeds empirical criterion tests only these scripts;
even success cannot demonstrate no conventional policy can retain all regions.

Make the engineering-only authority explicit in v0.10's stage/criteria section
or its accepted integration snapshot: universal financial scarcity is already
refuted for this comparator; retain narrower H1/H2 numerical hypotheses as
falsifiable, but do not certify the stronger protocol prerequisite or current
confirmatory H2 launch. Any future confirmatory interpretation needs separately
reviewed prospective scope/design, not automatic promotion after script success.
Complete all512 cases later; invalid parents, high-support failure, low-U failure,
inactivity-only ALL failure, undefined comparator, or both low-g scripts retaining
all regions block current full-final readiness with explicit reasons. Never choose
another g, weaken ALL, relabel these as fair rivals, or erase negative evidence.

### IFR3 nonblocking at design stage but blocking later execution

Frame declarations/process plans do not prove source noninterference. HMAC/CNG
functions, ROM emission, malformed-packet traps and raw replay remain unimplemented
per the selected contracts; no source/reachability audit was performed here.
Require actual validation after authorized implementation, before engineering.
Abstract METER128/SENSE16/ATTEMPT16 and fixed-slot MOV are legitimate selected
machine primitives; native CPU lowering/performance is neither needed nor proved.
Do not reopen unchanged paper witnesses merely because executable code is absent.

## Reviewed byte identities and final status

SHA-256 values identify exact documents, not a freeze, secret listing or privacy
certificate. All six normative-evidence hashes embedded in v0.9 matched. Key
independent acceptance inputs and selected additions:

* E3_INTERFACE_CONTRACT_v0_9.md: 9198619af54add566afdf0999b356d55cdab81474962f51893878087221ba31b
* E3_CONFORMANCE_CONTRACT_v0_10.md: 31bfd25f896580d3f1ceac34f633db519a19990c6932c45456b67d0775787f33
* E3_EVALUATION_CONTRACT_v0_8.md: 36580bcb074e2f7e12a1708353dc9b2cefd845d5dc6a1bdd1fbbca8d7ec876a3
* .copilot-tracking/reviews/2026-09-10/e3-b05-review.md: 1e544368df1b07c9df83110657e6295bf873983e834f4c138bcf2be4043966d5
* .copilot-tracking/reviews/2026-09-10/e3-b06-review.md: 008b85b4deaf1a94a18cacbc2c2f8e66710a571b2f0950fcb107c434980473e9
* .copilot-tracking/reviews/2026-09-10/e3-b07-information-review.md: d31f38a22948859cbfae74ec8a41bcc0fcd8b1bff472d3434bad459c7e5bd69c

No secrets were accessed/reproduced; roots/targets stay archive-only. Full readback,
clean editor diagnostics and unchanged16-file evidence hashes are document checks, not runtime validation.

* [ ] Integrate IFR1 and explicitly adopt IFR2's engineering-only decision.
* [ ] After authorized implementation, validate sites/C budgets, sourcewise prefixes, single scalar consumption, cancellation and replay.
* [ ] Test16 reduced acquisition/reset tables,16 production bit changes, cross-block/populated/corrupt/dead histories and actual paired futures.
* [ ] Then run oracle/selected controls/all scripts; report failures without retuning. No final draws or second-freeze readiness now.

No factual user question or further original-scope research remains. Only this review changed.
Conventional ECC/allocation under protected machinery/external support establishes
no consciousness, subjective-experience, life or organizational-closure claim.