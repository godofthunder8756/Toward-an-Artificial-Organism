---
title: E3 static ROM closure
description: Remaining service instructions, bounded scratch, immutable quote tables and shared micro-PC layout
ms.date: 2026-09-10
status: Complete - selected service and instruction-ROM design closed; implementation untested
---

## Scope and questions

Design only: close TICK, ADMIT, both LESSON forms, COMMIT, ISOLATE, linking, scratch and quote bounds.
Only this note is written. No E3 source, interpreter, ROM generator, checker, target draw or freeze.

## Authority and elemental convention

Read E3_CONTROL_CONTRACT_v0_6.md, E3_OPERATION_CONTRACT_v0_3.md, E3_PHYSICAL_CONTRACT_v0_4.md
and E3_POLICY_CONTRACT_v0_5.md in full, plus
.copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md,
.copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md and
.copilot-tracking/reviews/2026-09-10/e3-control-review.md.
Field evidence: E3_STATE_CONTRACT_v0_2.md; B05 scope/rows: E3_EVALUATION_CONTRACT_v0_7.md.
Use v0.6/CT precedence and the service note's scans, RESPONSE, TERMINAL and upkeep, not stale one-C wording.

Each EX, MOV, shift, Boolean operation, comparison, SELECT, ADD and BR is one CONTROL unless marked kernel.
Narrow fixed slots preserve neighbors; EX of packed fields is explicit; operands
are at most 32 bits. D[a:w] means w decoder bits starting at a; R0..R3 are the
only four arithmetic words. Control remains PC16/address11/five flags, including f3 gate outcome.
Repeats are literal text expansions, not runtime loops, macro-ops, calls or implicit address updates.

STAGE/entry MOV sets PC to the following named work site. EXIT is STAGE exit; BR S; S.
Its first two instructions are CONTROL, S is separately paid eight-energy clearing.
S zeros all 256 scratch bits, including PC, and terminates the worker invocation:
no sequential PC increment, privileged continuation, return-PC restore or callback follows it.
The next public outer service starts independently; no acquired stage survives in a host index.

Ordinary ADMIT/LESSON admission has an important distinct edge: outer METER128
itself dispatches to C on admission or the terminal S on rejection, after paying M.
This is paid admission dispatch, not a free worker BR: rejection executes exactly M,S.
All subsequent branches consume CONTROL, including failed cell gates; they cannot borrow this rule.
Mandatory-base entries pay M,C before entry MOV; the controller alone prepays two Cs.
An unfunded minimum shuts down physically, never returns to an unpaid cleanup or next service.

READ2/WRITE2 bundle route/insertion/extraction, not address instructions. Paid scalar encoding
delivers a zero-extended R0 value. METER may destroy R0..R3 but preserves live D/address/input flags.
No successful-body, reservation, spent, V/A/W or loop counter is introduced in these services.

## TICK with no CONTROL envelope

Literal typed sequence: PASSIVE prefix; M; I16(E); I8(P0); I8(P1); I8(P2);
I8(P3); H0; H1; H2; H3; LIVING16; RENT20; S. Exactly 14 stored sites, zero CONTROL.
PASSIVE is the selected preflight support exception, not an arbitrary worker macro: cap/deposit grants, retain four
accepted material amounts in D[0:8], D[8:8], D[16:8], D[24:8]. No accepted-E copy is needed.
These scratch writes belong to the named METER cap/deposit accounting; no host receipt survives.
Support precedes M's minimum check; failure sinks E and stops, externally logged without active service credit.

Each I consumes its one declared current grant scalar into R0; explicit zero offers
still cost one. It neither deposits again nor supplies a sixth accepted-amount packet.
Each Hj consumes its already retained accepted quantity and charges that many one-hop
material transport units; it is a route tariff, not a worker transport loop or ALU.
LIVING and RENT are fixed physical debits 16 and 20 through the paid METER continuation.
No branch, sensor, RAM access, balance copy or extra MOV occurs. D uses 32 bits and one I/O register.
Cost=177+sum(accepted Pj)<=177+4g, material debit zero; there is no tick-end second S.

## ADMIT and block LESSON

ADMIT has five public entries p=0..4 with slot lanes 848+4p+k, k=0..3.
After admitted M,C: MOV PC,body; I4 cue into R0; SHL R0,R0,1;
OR R0,R0,1; MOV D[0:8],R0; STAGE slot-write;
for each k: MOV address,848+4p+k; WRITE2 D[2k:2]; then EXIT.
CONTROL=1+3+1+4+2=11; stored sites=11+4W+1I+3(M,C,S)=19 per entry.
All cues are legal; reserved bits are zero. No read/second clear/history/p slot; rejection consumes no cue or write.

Block LESSON after admitted M,C: MOV PC,body; I4 cue into R0; MOV D[8:4],R0;
I1 label into R0; MOV D[12:1],R0. Base formation is exactly EX R0,D[8:4];
SHR R1,R0,2; SHL R1,R1,2; ADD R1,R1,868; MOV D[16:11],R1.
STAGE staging-read; EX address,D[16:11]; READ2 D[0:2]; then for k=1..3:
ADD address,address,1; READ2 D[2k:2]. All eight staging bits are paid, including corruption.

The thirteen CONTROL merge instructions, in order, are EX R0,D[0:8];
EX R1,D[8:4]; AND R1,R1,3; MOV R2,1; SHL R2,R2,R1;
XOR R3,R2,255; AND R0,R0,R3; EX R3,D[12:1]; SHL R3,R3,R1;
OR R0,R0,R3; SHL R2,R2,4; OR R0,R0,R2; MOV D[0:8],R0.
This clears only label r, inserts its supplied bit and sets validity 4+r;
all other currently stored label/valid bits survive unchanged, not authenticated.
STAGE staging-write; EX address,D[16:11]; WRITE2 D[0:2]; then k=1..3:
ADD address,address,1; WRITE2 D[2k:2]; then EXIT.
CONTROL=1+2+5+5+13+5+2=33; sites=33+8 accesses+2I+3=46.
No mid-body gate/fault; bases=868,872,876,880, final lane<=883. D assigns 24 bits, ending at 26.

## Repetition LESSON and block COMMIT

Repetition LESSON after admitted M,C: MOV PC,body; I4 cue into R0;
MOV D[0:4],R0; I1 label into R0; MOV D[4:1],R0.
Eight CONTROL base instructions: EX R0,D[0:4]; SHR R1,R0,2; SHL R2,R1,4;
SHL R1,R1,2; ADD R2,R2,R1; AND R0,R0,3; ADD R2,R2,R0; MOV D[8:7],R2.
For each literal i=0..4: kernel EX R0,D[4:1] (the one paid generation ALU);
MOV D[16:2],R0; EX address,D[8:7]; ADD address,address,4i; STAGE write-gate;
M; BR rejected to EXIT; WRITE2 D[16:2]. Fall through to the next literal cell or EXIT.
There are five CONTROL per visited cell; full CONTROL=1+2+8+25+2=38.
Failure at i executes 13+5(i+1) CONTROL; no later cell executes. Stored sites are
38+5 generation+5 cell M+5W+2I+3=58. No code read, compare-clean or return calculation exists.
Cue/label/base/expected occupy 14 D bits, ending at 17; all survive gates.
Addresses are 20(cue SHR 2)+(cue AND 3)+4i, always 0..79. Every visited cell needs a write.

COMMIT has four public entries j=0..3, each scheduled after its block's fourth lesson,
even when that lesson rejected. After M,C: MOV PC,body; STAGE staging-read;
for k=0..3: MOV address,868+4j+k; READ2 D[2k:2].
Extract with EX R0,D[4:4]; EQ f0,R0,15; EX R0,D[0:4]; MOV D[8:4],R0.
STAGE encoding-gate; M; BR not f0 to CLEAR; BR rejected to CLEAR.
M preserves f0/payload. It always charges the encoding gate, including false stored validity.

For each i=0..19 use columns (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,1,2,4,8,15):
EX R0,D[8:4]; kernel AND R0,R0,column_i; SHR R1,R0,2; XOR R0,R0,R1;
SHR R1,R0,1; XOR R0,R0,R1; AND R0,R0,1;
MOV D[16:2],R0; MOV address,20j+i; STAGE write-gate; M; BR rejected to CLEAR;
WRITE2 D[16:2]. Only the six marked parity instructions are generation kernel.
CLEAR is MOV R0,0; STAGE staging-clear; for k=0..3:
MOV address,868+4j+k; WRITE2 zero from R0; then EXIT.
Every funded exit retires all staging bits.

Full CONTROL=1+5+4+3+20(5)+6+2=121; invalid staging=20; rejected encoding=21;
encoding admitted with v visited cells=21+5v, including a last failed write gate.
Stored sites per j=121+8 staging accesses+120 generation+20 code W+24 envelopes=293.
The 24 are outer M,C,S, encoding M and twenty cell Ms. D[0:8] dies after extraction;
payload D[8:4] and expected D[16:2] survive each cell M. Peak D live bits=12,
maximum addressed bit=17; no retained codeword, acquired block index or fifth R word.

## ISOLATE and already-covered physical interfaces

ISOLATE after M,C: MOV PC,body; MOV R0,0; STAGE ring-clear;
for n=848..867: MOV address,n; WRITE2 zero; STAGE teaching-clear;
for n=868..883: MOV address,n; WRITE2 zero; STAGE record-clear;
for n=884..899: MOV address,n; WRITE2 zero; then EXIT.
CONTROL=1+1+3+52+2=59; sites=59+52W+3=114. No D bits, RAM reads or scalar packets.
All 52 writes are mandatory; no validity-dependent branch, masked preservation or optional reject.

SENSE is v0.3's fixed physical pair-read/encoding service, with the already MOVed two-bit
hub flag; debit 16 plus four routed flits first, then sample typed E/local P once
and deliver their 16/8-bit encodings in R0/R1. The two GE instructions are paid B4
CONTROL and form e/p afterward. No balance history, RAM sensor body, extra encoding
I/O or free health computation is used. Its declared sixteen tariff slots bound
its typed storage, not an assertion that native sensor firmware has sixteen instructions.
Similarly each resource ATTEMPT16 is an exogenous padded physical-attempt tariff,
including zero yield, not a worker algorithm hiding a search. Explicit request and
yield I/O and paid METER cap/deposit continuation follow the existing action trace.
Forage costs 16+1+1=18; collection 16+4+5=25, with hub-local material transport zero.
Opportunities are bounded by 64 E/8 P; no new body, callback or packet is inferred.

DRIVE inserts EQ f4,action,2; SELECT R3,f4,16,0; MOV a,R3 after action EX and before ACTION.
Omit I's EX W/NEG/MOV a, retaining BR store. In BOTH resource tails delete the
SHL/SHR and MOV a of the main objective; retain each BR J. The accepted-result
handoff may remain but cannot overwrite a. Thus resource return is zero, selected
scrub stays 16 through rejection/prohibition/clean/partial paths, and DECIDE rejection
still stores nothing. Stored CONTROL <=558 and executed A/B <=253/243 remain valid.

## Exact prices and sourcewise local and future tails

Let v=(1,1,1,1), e_j be one unit at source j; vectors below are (energy; material).
At every debit c require R>=c+L+T+(1;0) componentwise. Paid C leaves L; CONTROL is
not charged twice. Before an unknown cue use sourcewise maxima, never a memory peek.

| Service | Minimum including exit | Admitted/full upper price | Optional quote after outer M, besides S/T/residue |
|---------|------------------------|---------------------------|-------------------------------------------------|
| TICK | (177+sum accepted P;0) | (177+4g;0) | No optional body |
| ADMIT | (136;0) | (449;v) | (313;v)=C+I+4W |
| Block LESSON | (136;0) | (490;v) | (354;v)=C+2I+4R+4W |
| Repetition LESSON | (136;0) | (1154;5e_j) | (903;0)=C+2I+5(1+128), then per-write gates |
| COMMIT | (616;v) | (3756;v+20e_j) | After encoding M: (2680;0), retaining clear/S=(64;v) |
| ISOLATE | (1120;13v) | Same | No optional body |

For REP/COMMIT cell i, retain (n-i)(g+128)+F at entry; after generation retain
128+(n-i-1)(g+128)+F; after paying M test (23;e_j) with
L=(n-i-1)(g+128)+F. Here (n,g,F)=(5,1,(8;0)) or (20,6,(64;v)).
The paid failure BR releases only unvisited generation/gates and reaches F;
completed writes retain the later obligations. No full-write-material promise or refund occurs.
ADMIT/block LESSON promote every admitted access to L, so transfer cannot partially reject.
TICK after M retains (49+sum accepted P;0); each I/H/dues/S reduces exactly its term.
ISOLATE after C retains (736;13v), reducing one (14;e_(n mod 4)) per write, then S8.

Exact T after TICK: fourth block acquisition=136+616+12304=13056/11v; other acquisition=12440/10v.
Learning admission tick=1000+823+136+12304=14263/17v; last learning drain tick
=1000+823+12304+904=15031/21v. Controller 1000 includes both Cs and mandatory old clear.
After ADMIT retain upkeep 12304/10v plus TERMINAL 904/4v when scheduled.
Prior rejection/invalidity never narrows a future service's mandatory T. Fault leakage
one is separate from paid operation spend and from the positive pre-fault residue.

## One shared instruction address space and finite G

Keep the prior disjoint [0,26176) capacities: controller [0,4800), five RESPONSE
intervals [4800+4096p,8896+4096p), TERMINAL [25280,25472), AGE-LOW/HIGH
[25472,25664)/[25664,25856), CONDITION-d [25856+16d,25872+16d).
Prior demand bound 24902 includes the controller scan and all five separately inlined
RESPONSE scans, TD/selection, branches, physical tariff sites and paid continuations.

| Additional segment | Half-open interval | Capacity | Site demand bound |
|--------------------|--------------------|----------|-------------------|
| TICK | [26176,26240) | 64 | 14 |
| ADMIT-p | [26240+32p,26272+32p), p=0..4 | 160 total | 95 total |
| Block LESSON | [26400,26464) | 64 | 46 |
| Repetition LESSON | [26464,26528) | 64 | 58 |
| COMMIT-j | [26528+320j,26848+320j), j=0..3 | 1280 total | 1172 total |
| ISOLATE | [27808,27936) | 128 | 114 |

Additional demand=1499; capacity=1760<39359. Total demand<=26401; capacity=27936;
Remaining=37599; highest reserved address=27935<65535<65536, highest occupied<=27921.
Both teaching forms are stored conservatively; public representation enables only its prescribed form.
Assign every literal occurrence address base+its zero-based prefix ordinal, interleaving
CONTROL and typed work exactly as above. Labels denote those same addresses, not another
PC namespace. Ordinary entry M targets its own C/S; every BR/STAGE targets its named
occupied instruction, never padding. Sequential edges stay in the owning segment;
controller A/B transfers use its counted BR. Adjacent interval endpoints coincide; interiors never overlap.
Concrete offsets from each base: ADMIT M0/C1/entry2/EXIT16/BR17/S18;
block LESSON M0/C1/entry2/EXIT43/BR44/S45; REP LESSON cells start 15+8i, EXIT55/BR56/S57;
COMMIT encoding M17, reject BR18/19, cells 20+13i, CLEAR280, EXIT290/BR291/S292;
ISOLATE EXIT111/BR112/S113; TICK S13. Cell failures target their own EXIT or CLEAR.
These are the actual shared-PC addresses base+offset, not separate CONTROL and kernel numbering.
All other STAGE/entry targets are their following work instruction by the same prefix rule.

BLOCK-learning-RL, REP-learning-RL and BLOCK-learning-DRIVE each fit <=26401 sites/[0,27936); REP is smaller.
Even co-resident RL/fixed/DRIVE controllers fit: add two 4800 capacities and two 4738
demand bounds; shift every noncontroller interval by 9600. End=37536, demand<=35877,
remaining=27999. No acquired page, new C, call/return or extra state is introduced.

G DATA: 1104 placement/route rows, 20 columns, 16 generic candidates, 20 domain rows and finite policy constants.
Data is not CTRL or an executable bank; tail vectors have five signed-32 components. Future-T bound per variant:
2049 ticks/boundaries x 256 schedule masks x 28 service positions =14687232 rows.
A loose local-L table bound is 65535 PCs x 2^112 D/address/flag encodings; ignored
payload/raw/reward bits select identical rows, never free decode, dirty-count or truth tests.
Only paid predicates and declared gate arguments narrow suffixes. Backward finite suffix
sums/maxima define every row; reject overflowing/invalid G before acquisition.
Tables may be factored, not allocated here; inherited target-independent configuration ROM has no selected size cap.
The finite variant product remains finite. G contains no labels, acquired answers or reconstructible due-cue schedule.

## Disposition and remaining checks

B05 adds no worker service: probes reuse existing services; injections/refill/sham/reset and rows are external.
ORACLE is disabled, product size zero, allocation zero. No new METADATA/refresh plan is enabled.
B05 outer rows remain 1620049920 final / 10394044672 engineering, not instruction copies or worker continuations.

The selected service/ROM DESIGN blocker is closed with the exact upper bounds above.
No missing flow gets an arbitrary chunk; METER/sensor/attempt remain declared physical abstractions, not native-code proofs.
Actual instruction typing/linking, scratch-PC ownership, all-path budgets and transient-state
clear tests are implementation conformance obligations AFTER design freeze, not a demand to
write E3 code before freeze. This does not close independent B06 scientific or B07 ownership gates.

* [ ] After authorization, validate emitted instructions/targets and all scratch lifetimes against this paper expansion.
* [ ] Test rejection fees, prefix failure, corrupt staging, DRIVE resource returns and S terminating without PC restoration.
* [ ] Complete independent B06/B07 design gates; enabling an oracle/new service requires another design and bound.

Clarifying questions: none. Read-only scalar arithmetic checked sums/offsets; no runtime checker or E3 test ran.