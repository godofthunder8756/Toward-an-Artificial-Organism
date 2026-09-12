---
title: E3 oracle and scripted H2 conformance contract
description: AC-02 static template closure and AC-03 bounded learning-bookkeeping diagnostics
ms.date: 2026-09-10
status: Design selected only - independent acceptance and integration pending
---

## Authority and stage boundary

Select AC-02/AC-03's bounded designs below. Retain [E3_EVALUATION_CONTRACT_v0_8.md](E3_EVALUATION_CONTRACT_v0_8.md), [E3_INTERFACE_CONTRACT_v0_9.md](E3_INTERFACE_CONTRACT_v0_9.md), and their incorporated ordinary witnesses, except for the explicit TEMPLATE expansion, diagnostic script variants and separately budgeted additions here.
The [latest B05 acceptance review](.copilot-tracking/reviews/2026-09-10/e3-b05-review.md) closed EV-001/EV-002 at purpose/product level, not oracle implementation or SCRIPTED validation. Adopt the [B06 review](.copilot-tracking/reviews/2026-09-10/e3-b06-review.md) with AN-001/AN-002 and its sourcewise qualifications, not a universal scarcity theorem.
No ordinary policy, tariff, target law, final product, endpoint, n=32, eight-panel weighting, primary reset mapping or scientific threshold changes. Protected template physics and diagnostic padding are explicit exceptions, never ordinary repair privileges. E1/E2 and historical E3 documents remain unchanged.
First freeze may accept this falsifiable candidate and specified tests without positive empirical results. Independent static acceptance and manifest/schema integration still precede that freeze; authorized implementation and technical tests precede engineering. The additional engineering prerequisites below can forbid the current full final experiment without forbidding publication of negative engineering evidence or prospectively versioned research.
No implementation, target/root draw, test execution, run directory, freeze manifest or scientific pass is supplied.

## AC-02 product, source and exact frame

Use exactly REP/BLOCK x engineering individuals 1..8 x panel 1: 16 cases. Source each from its actual H1-RL-default SCREEN A post-lesion snapshot, including dead/ineligible cases. There are eight independent tables, not sixteen. The privileged clone lifecycle may replace diagnostic power; it never revives or changes the historical parent.
V0.8 does NOT select reset-all-canonical before templates. Start from the arbitrary source, perform its declared full entry and paid ISOLATE, and preserve damaged code/Q/metadata/ages/reserve. ISOLATE clears only ring, teaching staging and transition. Canonical all-state audits occur after restoration and separately after each probe.
Execute REP cues 0..15, one label each, or BLOCK cues 0,4,8,12, each with four labels in little-endian order. These are 16/4 atomic templates per case; every template writes all five/twenty addressed symbols, including correct cells. Each complete bank writes 80 symbols, exactly twenty at EACH P source.
Use v0.9's existing three-byte frame header and BIND payload8, BEGIN payload284, SCALAR payload6, EXIT/SHUTDOWN payload276. ABI remains9; capability1 is required. TEMPLATE is service12, phase5, tick0, argument0, mask0. Shape follows immutable code G, never a worker-supplied target/program key.
Exactly tag21 cue:4 and tag22 payload:4 arrive once each, at X, after outer M/body admission/C; each costs one energy. REP payload<=1; BLOCK cue mod4=0. The worker receives no callback, table, seed, old-clean state, alternate payload or buffered retry. Two scalar occurrences are below the per-operation cap8.
Wrong capability/header, length/tag/order, duplicate/missing/extra scalar, high/reserved bits or interruption cause external FAILED/PARTIAL, not biological death or a successful service. No subsequent operation, cleanup fiction or scalar retry is allowed. Width-valid semantic violations take the paid local bad-packet exit below. No malformed packet becomes a masked valid label.

## Literal template CONTROL and typed sites

D[a:w] names existing decoder bits. Allocate cue=D[0:4], payload=D[4:4], base=D[8:7], expected=D[16:2]; D15 is unused. Peak named D bits=17, highest=17. Use only R0..R3, PC16, address11 and flags5; f0 is validation and f3 the current gate outcome. Gates may clobber all R words, never the live D fields/address. Scratch is still32 bytes, persistent state276 bytes.
Each MOV/EX/shift/ALU/BR/STAGE is one CONTROL instruction. STAGE is a literal PC transfer, not a helper call. Scalar, generation, M, C, WRITE2 and S sites are separate paid primitives. Literal finite expansions have no runtime counter, W register, stack, bank selector, hidden source variable or host continuation.
Let b be the program base. The following offsets are shared-PC typed instruction ordinals, not CONTROL-only numbering:

| Offsets from b | Literal work |
|----------------|--------------|
| 0,1 | Outer M128; C256. Paid outer M dispatches rejected body directly to normal S, admitted body to C. |
| 2..4 | MOV PC,b+3; MOV flags,0; STAGE b+5. |
| 5..8 | Receive tag21 into R0; tag22 into R1; MOV cue,R0; MOV payload,R1. |
| 9..11 REP | LE f0,R1,1; BR not f0 to BAD; MOV R3,R3, charged padding. |
| 9..11 BLOCK | AND R2,R0,3; EQ f0,R2,0; BR not f0 to BAD. |
| 12..15 | SHR R0,R0,2; SHL R2,R0,4; SHL R3,R0,2; ADD R2,R2,R3. |
| 16..18 REP | EX R0,cue; AND R0,R0,3; ADD R2,R2,R0. |
| 16..18 BLOCK | Three literal MOV R3,R3 charged padding instructions. |
| 19,20 | MOV base,R2; STAGE b+21. |

For each literal cell i, let p_i=b+21+(g+8)i, with (n,g)=(5,1) REP or (20,6) BLOCK. Offsets are 4i for REP, i for BLOCK. Execute this exact list:

1. At p_i: EX R0,payload, one CONTROL.
2. At p_i+1..p_i+g: REP kernel AND R0,R0,1; BLOCK kernel AND R0,R0,column_i; SHR R1,R0,2; XOR R0,R0,R1; SHR R1,R0,1; XOR R0,R0,R1; AND R0,R0,1.
3. At p_i+g+1..p_i+g+4: MOV expected,R0; EX R1,base; ADD address,R1,literal_offset; STAGE p_i+g+5, four CONTROL.
4. At p_i+g+5: paid M128; at +g+6: BR rejected to EXIT, one CONTROL; at +g+7: paid WRITE2 expected. Success falls through to the next literal cell or EXIT.

BLOCK columns are 1..15,1,2,4,8,15. All generated values are canonical 00/01. Every expected/address value survives M; address is in0..79 and physical source is cue SHR2. There is no scan, clean-cell comparison, old-code read, additional copy or target-indexed ROM.
Let q=b+21+(g+8)n. EXIT at q is STAGE q+1; q+1 is BR q+2; q+2 is S8, clearing all scratch and terminating without subsequent PC increment. BAD at q+3 is STAGE q+4; q+4 is a separate S8 terminal, observed externally as technical failure, never a normal EXIT/SHUTDOWN success. No branch reaches padding or another program.
Normal administration is19 CONTROL including exit, plus6 per visited cell: full49 REP/139 BLOCK. Rejected prefixes execute19+6V; body rejection executes no CONTROL. Semantic bad packets use <=9 CONTROL. The reserved administration ceiling40 gives40+6(20)=160<=256 on every admitted path. There is one C only, not the controller's two Cs.
Stored demand is26+(g+8)n: 71 REP/306 BLOCK including the bad exit. Normal S offsets are68/303; BAD offsets69/304; bad S offsets70/305. Thus even BLOCK exceeds256 stored sites without exceeding its256 executed CONTROL budget. Physical minimum failure stops at its actual prefix with no unpaid S.

## Sourcewise quotes and complete ROM linkage

Let e_j be one material unit at source j and rho=(1;0,0,0,0). No operation borrows later support. T=0 only in the declared off-clock block; current S remains in L. At outer entry reserve M+S+rho; after paying M, body admission requires C+two encodings+n(g+128)+S+rho energy. No code-write material is prepaid: each local write has its own funded gate.
After C retain two encodings plus n(g+128)+8. At cell i entry L includes (n-i)(g+128)+8. After generation retain128+(n-i-1)(g+128)+8. After paying current M test c=(23;e_j), L=((n-i-1)(g+128)+8;0), T=0 and rho componentwise. Material equality is legal; pooled material is not. The first-write energy requirements are548 REP/2578 BLOCK.
On gate rejection, the paid BR releases only the unvisited suffix and takes EXIT; prior writes persist, with no refund or alternative cell. Invalid packets retain S funding but stop the harness technically. Quote recipes are backward finite sums/maxima over these literal sites and paid cue/address; before discovery use sourcewise maxima over legal cues, never a free source peek or acquired ledger.
Before EACH template externally replace E/P with65535/255 and record gross removed/supplied vectors and1020 dispatch energy. No supply occurs inside a template; only that declared replacement occurs between templates, with no TICK/fault/upkeep/leakage. After C/inputs E=65149; full completions leave64381/62001 and local P=250/235. Consequently every positive-case prefix is funded independently of the source's prior stocks.
Valid prefix energy is394+gV+128A+23W, V=A, W<=A<=n. Full prices1154/3534 yield full-bank18464/14136. Body rejection costs136, with no input. Record S, C, actual CONTROL, scalar presence, V/A/W, addresses, primitive traces and all five-source debits independently of replacement subsidy.
Use the ordinary co-resident layout's reserved endpoint37536 from the [adopted ROM witness](.copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md), including its9600 noncontroller offset. Add REP TEMPLATE at[37536,38048) and BLOCK at[38048,38560), capacity512 each. Public immutable code selects one entry reused for every cue; not four independently chosen source programs.
Place each occurrence at b+its literal ordinal above. All normal/reject/bad targets are occupied in its own segment; sequential edges terminate at S, never into another segment. Existing ordinary labels shift exactly as in the adopted co-resident construction. One PC16 suffices; largest reserved address38559<65535. Ordinary-plus-template demand<=35877+377=36254, reserved capacity38560; neither27936 nor37536 alone includes the oracle.
The two generic typed images contain no labels. Operand descriptions, script alternatives below and quoted suffix recipes depend only on public G and counted scratch. Mechanical emission/link/scratch checks are later tests, not an unexplained implementation prerequisite for selecting this finite construction.

## Immediate positive assertion, probes and reset

Checkpoint BEFORE any fault/query and assert every one of80 code symbols equals the external target encoding. Compare Q/metadata/ages/reserve byte-for-byte with the source; allow only declared ISOLATE/code/typed-stock changes elsewhere. A matching decode or clean initializer does not replace this assertion.
Fork independent charged261-tick no-challenge ZERO-FAULT and LIVE-WEAR probes from that checkpoint. Both receive full entry, paid ISOLATE, g=28, ordinary query/upkeep prices, and no controller/feedback. ZERO-FAULT alone suppresses RAM flips/erasures, not typed leakage/charges. It must emit256/256 correct with full activity/coverage/completion, conditional on conformance. LIVE-WEAR retains ordinary faults and has no100%-accuracy gate.
REP exact replicas and BLOCK's spanning columns1,2,4,8 establish the zero-fault decoding result; funded query entry and cleared slots establish all256 scheduled responses. No clone result/state/timing returns to its parent. Protected restoration supplies information and cannot prove ordinary example-free repair or any main hypothesis.
Retain16 restoration histories,32 probes,160 templates,1280 writes,260800 template energy,8352 ticks,8192 responses,48 ISOLATEs and48 actual source reset audits. Revoke capability before constructing each canonical reset child; reference existing H1-RL-default reset G/Z. Add no oracle future, target or final branch. Reduced sixteen-table acquisition/reset and production target-bit tests remain separate implementation fixtures.

## AC-03 bounded SCRIPTED H2 product

Select two immutable scripts, SCRIPT-U and SCRIPT-ALL, for2 codes x8 engineering individuals x8 panels x2 scripts x2 g values{36,66}=512 D ecologies. Each lasts512 ticks with507 planned responses; endpoint remains128 U/128 O. There are no script finals, extra independent individuals, candidate grid or outcome-selected scripts.
Clone each existing H2-RL-default developed trunk after its scheduled TERMINAL, not an oracle-restored/clean body or a selected winning trunk. Reuse its actual acquisition/development/intact-prerequisite records once; add no development or Q transfer between individuals/panels. Each script child inherits that complete actual body, then uses ordinary live full entry and paid ISOLATE. A dead parent yields a planned dead child, not privileged replacement power.
This is an explicit diagnostic immutable-G rebind at a completed branch boundary: generic action selection changes, acquired bytes do not. G then remains fixed through ecology and its reset audit/future. SCRIPT-U and SCRIPT-ALL use default cuts32768/64 and h=3; controller, TD, code, query and age faults stay ordinary. Both run the actual learning path, not the nonlearning fixed-policy path.
Ordinary TICK support is30000 energy and g=36 or66 per source. Keep D's whole-block U/O assignment, usefulness change and endpoint timing; no lesion/challenge, refill, forced death, fallback repair or special conditioning order. Preserve forage64/local collection8 opportunities and ordinary conditioning0..19. These source-specific budgets are not an aggregate stockpool.
Use external family namespace H2-SCRIPTED and fixed schedule slot34. Pair schedules/UO/fault/guess coordinates across codes/scripts/budgets within each individual/panel; do not key them by actions, correctness or outcomes. Reuse the same independent engineering tables, without drawing any new secret here. Workers receive only ecology phase4 and permitted current packets, never SCRIPTED/D/UO identifiers or future schedules.

## Script selector, genuine learning and diagnostic padding

Selection is a fixed rule BEFORE ACTION's normal paid gate: if e=0 forage; else if p=0 collect; else scrub when h=3 AND (u=1 for SCRIPT-U, true for SCRIPT-ALL); otherwise forage. Empty/tied storage never provides a repair sign, and rejection never chooses another action. Only paid observation s=16u+8e+4p+h supplies these predicates.
Keep v0.6 stages A/B/C/D, including all actual damaged-Q reads, signed TD kernels, Q rewrites if admitted, old retirement, F/G/H/I/J/K, learning RESPONSE finalization and scheduled TERMINAL. Retain actual stored terminal/invalid/rejected handling. Q is neither reset nor shadowed, and TD writes remain material-paid/fault-exposed, although Q estimates do not choose script actions.
Replace E's39 CONTROL instructions and its Q-selection kernel/inputs, rather than appending an override to A250. In the existing s/action slots execute these twelve CONTROL instructions, in order:

| Steps | Literal SCRIPTSEL instructions |
|-------|--------------------------------|
| 1..4 | EX R0,D[47:1]; EX R1,D[46:1]; EX R2,D[44:2]; EX R3,D[48:1]. |
| 5..8 | EQ f0,R0,0; EQ f1,R1,0; EQ f2,R2,3; AND f2,f2,R3 for U, or AND f2,f2,1 for ALL. |
| 9..12 | SELECT R0,f2,2,0; SELECT R0,f1,1,R0; SELECT R0,f0,0,R0; MOV D[53:2],R0. |

Then one CONTROL STAGE targets a literal run of270 kernel MOV R0,0 instructions; fall through to F. They are explicitly diagnostic unused-energy padding, not fake Q reads, fake packets, hidden computation or main-rival work. Action survives in D; all R values are dead. No auxiliary/persistent field or scalar is added.
The padded amount is99 intrinsic selection energy +24*7=168 routed Q-read energy +3 rank encodings=270, not99 alone. No actual selection Q read or B/T/X input occurs. Genuine TD kernels above still execute/pay normally. Quotes reserve this entire declared diagnostic run after admitted DECIDE and through TD admission; physical debits precede ACTION. Rejected DECIDE runs no padding.
This deliberately matches the removed selection tariff while doing unused work, isolating learning-bookkeeping/conditioning costs; it is NOT an efficient conventional rival or a claim that ordinary fixed policies owe these costs. Ordinary fixed/frozen policies retain their real savings and receive no dummy work. Per-realized-path equality with RL is not asserted: actions, admissions, TD shapes and stocks can differ.
E replacement uses13 CONTROL, bounded by16. BLOCK A<=250-39+13=224 (or227 with conservative16), B<=246; REP A<=197,B<=81. Resource paths are smaller; omitted TD/records in learning-disabled reset recovery shorten execution. No third C, extra operation, unpriced nine-instruction post-selection override, scratch bank or interruption is allowed.
Keep both prepaid C256 budgets,512 energy, including rejected DECIDE. Script controller scalars are at most5 resource/3 scrub (offer, paid E/P, optional request/yield); learning RESPONSE remains<=4. TD material and other genuine bookkeeping retain main prices. Return is a=floor(F/4)+2C-W; legal learning feedback b=64v(2c-1) finalizes clip(a+b,-256,256). It may reveal due labels through the permitted ecology channel, never through the selector.
Public diagnostic G IDs are400+2*code+s, code0/1, s=0 U or1 ALL. Extend policy enumeration with5/6, objective remains0, learning is the existing phase permission; variant remains the public code. BIND size/ABI and 32-byte scratch are unchanged. Specialize literals from immutable policy, not a new worker scalar or acquired variant selector.
For script G images keep ordinary RL at[0,4800), replace the two optional co-resident fixed/DRIVE controller regions with one script region[4800,14400). This is a public variant, not simultaneous four-controller occupancy. Demand<=4738+13+270=5021<9600 even without credit for deleted E sites. All noncontroller/template intervals stay fixed, final capacity38560. Script and ordinary G are distinct and never merged by identical scores.
Emit the script by the adopted controller's literal-order expansion, replacing E by SCRIPTSEL/padding, interleaving typed primitives and assigning base+prefix ordinal. Named branches resolve to those same forward labels; retain counted A/B transfers and rejection/terminal/resource exits. No unexplained helper or new opcode is introduced: diagnostic padding uses kernel MOV; original trace commitments expose every occurrence and its debit.

## Sourcewise feasibility and scarcity interpretation

Apply the [B06 sourcewise analysis](.copilot-tracking/research/subagents/2026-09-10/e3-b06-analysis.md) with AN-001. At g=36 the maximal learning BLOCK energy envelope including leakage is29275<30000; at66 it is29395<30000. Selection padding does not exceed the corresponding removed RL energy. Bounds are conditional on eligible live parents and conforming traces, not revival or recall proofs.
Before optional conditioning an ordinary admitted learning tick uses at most24 per source excluding code: old clear4+store4+Q update2+reward finalization2+slot clear1+ADMIT1+ages10. REP correction adds<=5 only at the offered source, giving29; BLOCK can reach44 and stop at its first unaffordable needed write. Every test retains local L/public T/rho, not merely an end-of-tick balance.
On the last drain remove ADMIT1 and protect mandatory TERMINAL clear4: busiest REP bound32. The full optional-terminal envelope34 is NOT guaranteed after conditioning. AN-001's remaining(4,5,4,6) example permits mandatory clear but rejects optional two-per-source TD. Do not reserve optional final TD as if mandatory or report skipped updates as successful learning.
All-conditioned no-code learner demand40 per source includes leakage; dropping TD saves2. Ordered conditioners consume b(d)=e_floor(d/5)+e_((924+2d) mod4)+e_((925+2d) mod4), not three interchangeable pooled units. Low-stock worksheets and the necessary8U+W+Lambda<=2928 exclusion apply only with their full-service premises. They exclude every-update/full-conditioning coexistence, not all legal retention paths.
Crucially, ordinary fixed/frozen REP no-record demand is28, at most33 with five correction writes. Since33<=36, full conditioning AND all-region fixed-REP correction are financially affordable. This mathematically refutes universal forced obsolete-sacrifice claims. It neither guarantees accurate code nor proves that scripts carrying genuine learner overhead retain useful information.
Conditioner lapses may damage code, Q, query or ages; the script cannot select domains or read true damage. Positive O-write denominators are not guaranteed, even under faults. Preserve zero comparators and undefined ratios. No ordinary G-DIAG/HS-REFERENCE result substitutes for these scripts.

## Prespecified engineering criteria and failure disposition

Evaluate each code separately, first equal means over eight panels per individual, then eight individuals. No response-level n or confirmatory script CI is created. Use all planned dead/missing rows. Parent prerequisite is existing intact>=0.90 and acquisition/development activity separately>=0.95; failure is retained and blocks a positive witness.
Script viability requires mean endpoint R_U>=0.80 and whole-512-tick activity/completion each>=0.90. Define all-region retention as endpoint recall>=0.80 for EACH of four fixed blocks, using64 planned responses per block and the same panel/individual averaging. Keep R_O, each block recall, full-window/end-window correction and reconstruction/miscorrection, Q updates, conditioner masks/ages, rejections and source balances.
At g=66 require U viability and ALL all-region retention plus activity/completion guards. At g=36 require U viability, at least one correct useful reconstruction, positive aggregate ALL endpoint O writes, and zero U-script O writes when the offered u=0. The latter is a structural rule check, not proof of a learned allocation effect.
For the stronger scarcity prerequisite require g=36 ALL to miss all-region retention while meeting activity/completion guards, with high-support ALL passing. Both low-budget scripts succeeding at retention means STRONG-H2-SCARCITY-NOT-ESTABLISHED, not a positive scarcity witness. Low-budget U failure, high-support failure, invalid parents, undefined comparator or ALL failure only through inactivity also fails this prerequisite with its specific reason.
This is a bounded empirical comparator condition, not proof that ALL is optimal or that no policy can retain every region. Even a passing script comparison must retain the fixed-REP financial counterexample and the learner-overhead qualification.
Complete all512 cases without favorable early stopping. A technically valid failed scientific/prerequisite gate is COMPLETE with failure, not PARTIAL or deleted data. Any failed prerequisite forbids the current full final launch/second-freeze readiness; report the negative result or propose a separately reviewed prospective design. Do not choose another g/grid point, weaken ALL, erase failures or retune prices to manufacture scarcity. Positive RL H1/H2 final effects remain falsifiable, not required before first engineering.

## Script resets, rows and separate archive allocation

Audit every one of512 terminal script ecology states, including dead states, using actual-source byte/reference cancellation checks. Canonical body is code0xAA/all256 auxiliary bytes zero, then identical activation; retain original hashes/lifecycle. Do not recursively audit negative phases or treat ISOLATE as reset.
Keep script G through reset, disable learning, normalize budgets/calendars to H2 RESET recovery128 at47 then FINAL261 at28, including challenge and two paid ISOLATEs. SCRIPTSEL and its declared padding remain on recovery offers; no ecology feedback or Q update remains. Assay has no controller. Empty code stays empty; no oracle capability is available.
One representative per(code,individual,panel,script G,H2 normalized Z) gives256 canonical futures, shared across the two source budgets only after each actual reset audit and paired implementation checks. Budget g is a phase support parameter normalized by reset, not a distinct script G. Never alias to ordinary RL/fixed G. Required paired implementation fixtures run separately; no389-tick future per512 source histories is invented.

| Added logical quantity | Ecology only | Reset futures | Total delta |
|------------------------|--------------|---------------|-------------|
| Histories/futures | 512 | 256 | Distinct products |
| Planned ticks | 262144 | 99584 | 361728 |
| Due responses | 259584 | 65536 | 325120 |
| Phase summaries | 512 | 512 | 1024 |
| Source reset audit rows | 512 | 0 | 512 |
| Scheduled snapshots, including source-reset pair | 7168 | 3328 | 10496 |
| Extra shutdown ceiling | 512 | 512 | 1024 |
| Maximum snapshot rows | 7680 | 3840 | 11520 |
| Paid ISOLATE slots | 512 | 512 | 1024 |
| Controller offers | 262144 | 32768 | 294912 |

Use v0.8 coefficients B=12K+13R+2N, Bmax=B+1024, K=512,R=256,N=512. Ecology has eight tick anchors plus four named boundaries; the two audit snapshots are separate. Add no lessons, COMMITs, templates, acquisition/development or prerequisite probes. Actual shared expenditures resolve from the manifest union, not repeated attribution.
Use v0.9 widths unchanged:48/tick,8/response,308/maximum snapshot,64/audit,512/summary bytes. Their delta is24069120 bytes. Reserve an additional4194304-byte separate SCRIPTED context allocation: up to2097152 for the two typed ROM recipes,83968 for64 schedules,65536 phase descriptors,49152 original trace commitments,8192 class mappings,512 for4 G rows, and1048576 metadata/dictionaries/directories; remaining841216 is bounded spare, not telemetry.
Thus the separate dense SCRIPTED ceiling is28263424 bytes, excluding independently budgeted implementation fixtures, expanded debug views and backups. The inherited8567308288-byte core ceiling does NOT include this addition. No compression, death, winner overlap or unproved aliasing is assumed.
Integration must append immutable planned counts, new phase/class/snapshot ranges, product SCRIPTED=13, policies5/6, namespace/schedule slot34 and G IDs400..403 before first freeze. Preserve old semantic keys; use a versioned extension shard rather than renumbering prior catalogs. Increase total phase/class/snapshot capacities or resolve checked extension ranges explicitly; old v0.9 maxima alone are insufficient. Original traces, raw truth fields and one-way sinks retain their existing codecs.
Scripts do not add targets, primary erasure maps, final n, bootstrap votes or precision. Reset clocks/inputs are held fixed under history/target counterfactuals; same predictions may score differently against changed labels. Counts/layout integration is a remaining owner deliverable, not authority to edit manifests in this task.

## Required later checks and exact status

* [x] AC-02 selected static scratch/frame/entry/cell/rejection/bad-packet/S/quote/link design; no oracle pass claimed.
* [x] AC-03 selected finite scripts, genuine learning costs, explicit padding, sourcewise limits, functional criteria, reset roster and separate archive delta.
* [ ] Independent acceptance and AC-04 integration of added enumerations/counts/capacities before unconditional design freeze.
* [ ] After implementation authorization, validate emitted sites/budgets, every sourcewise prefix, malformed packets, single consumption, S termination, no parent/probe feedback and exact byte/trace replay.
* [ ] Test arbitrary populated/corrupt/dead histories, every template cue/payload, exhausted local P with abundant remote P, first/last failed writes, target-bit/component reset cases and capability cancellation. Verify script rules on all32 paid observation states and TD invalid/terminal/rejection paths, including padding debits and zero unused rank inputs.
* [ ] Then execute mandatory oracle, selected controls and all scripts, retain failed prerequisites, and permit final draws only after applicable engineering gates and the separate source/configuration/tests/analysis/archive freeze.

No factual user clarification is required. Design specification is complete within AC-02/AC-03; independent acceptance, archive integration and all runtime evidence remain distinct outstanding obligations. No consciousness, life, subjective experience or organizational-closure conclusion follows from either outcome.