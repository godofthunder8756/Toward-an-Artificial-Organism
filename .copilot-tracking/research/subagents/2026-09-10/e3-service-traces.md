---
title: E3 static service trace closure
description: Bounded decoder, response, terminal, age and conditioning witnesses with typed ROM occupancy
ms.date: 2026-09-10
status: Complete - requested static traces pass; whole-E3 ROM coverage qualified
---

## Scope and authority

Research only. No E3 program, worker, training, target draw, contract/review edit,
or design freeze. The only output is this new research artifact.

Read E3_CONTROL_CONTRACT_v0_6.md, E3_OPERATION_CONTRACT_v0_3.md and
E3_PHYSICAL_CONTRACT_v0_4.md in full. Apply the control contract's precedence,
including CT-001 through CT-010 in
.copilot-tracking/reviews/2026-09-10/e3-control-review.md and the incorporated
.copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md.
Consult E3_STATE_CONTRACT_v0_2.md for field layouts and
E3_POLICY_CONTRACT_v0_5.md for health and signed reward semantics.

## Questions

* Expand repetition-five and block-twenty scans with exact paid instructions,
  fixed raw subwords, six-step branchless minimum/tie reduction and live slots.
* Supply complete RESPONSE and scheduled TERMINAL paths within one CONTROL256.
* Instantiate both ten-age services and all twenty fixed-domain conditioners.
* Prove positive-residue, sourcewise quotes and finite typed-ROM capacity using
  sixteen-bit micro-PC, without an unpriced loop, call, return or acquired bank.
* Distinguish static design closure from later mechanical implementation checks.

## Instruction and payment convention

Use the accepted fixed-slot ABI, not a native-machine lowering. Each EX, MOV,
comparison, Boolean operation, shift, ADD and SELECT below is one instruction;
SELECT(p,x,y) means x if p, otherwise y. Narrow named slots preserve neighbors.
Packed raw/record fields require EX. Arithmetic operands never exceed 32 bits.
R0-R3 are the only arithmetic words. Decoder D has bits 0..95; control has
micro-PC 0..15, address 16..26 and five flags f0..f4 at 27..31.

Every displayed finite repetition is literal ROM text expansion, not a runtime
loop, macro-op, call or implicit address update. STAGE is one charged MOV of a
literal forward target to micro-PC; sequential advance is intrinsic. Entry MOV
targets the following body entry, not itself. A final STAGE targets the exit BR;
that BR targets S. S clears all 256 bits and terminates without rewriting PC.
Gate results use f3; METER may destroy all R words but preserves declared live
D fields and input flags. No worker fuel, bank, return-address or quote counter.

READ2's physical reply may occupy a designated R word; its already charged
insertion then copies those two bits into the named raw destination. This is
the read/reply plus insertion already in READ2, not a second free insertion.
For scan capture, designate R0 as that reply word, raw D as insertion target,
and R3 as base. R0 remains available to the next ALU. All twenty raw symbols
are stored, including 10/11. Q/reward reads instead assemble the specified
destination, followed by the explicitly listed signed EX. WRITE2's extraction
preserves its source. Routes/flits are bundled in the access, not extra scalars.
In capture comparisons, R0 denotes its named two-bit reply subslot, not stale
upper bits of its 32-bit container. No zero-extension instruction is assumed.

Every outer service here pays M128 then C256 before its first CONTROL; the
controller alone prepays both accepted Cs. METER minimum failure is physical
shutdown, not a returning branch. Every optional test follows its paid M.
No kernel below borrows CONTROL padding; unused CONTROL is paid padding.

## Block scan with twenty stored symbols

Use candidate c=0..15 and columns
(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,1,2,4,8,15).
Both lists are generic inherited constants, never labels. Addresses are
20(cue SHR 2)+i. B2 leaves that base in R3. The following fixed slots fit the
accepted 64-bit scan footprint; controller inputs occupy 64..75 separately.

| Slot         | D bits | Meaning                         |
|--------------|--------|---------------------------------|
| raw-low      | 0..31  | Symbols 0..15                   |
| raw-high     | 32..39 | Symbols 16..19                  |
| candidate    | 40..43 | Current generic candidate       |
| best         | 44..47 | Earliest minimizing candidate   |
| observed     | 48..52 | Binary observations, 0..20      |
| distance     | 53..57 | Current distance, 0..20         |
| bestDistance | 58..62 | Minimum, initially 21           |
| tie          | 63     | Multiple minimizers predicate  |

Initialize with four kernel MOVs: observed=0, bestDistance=21, best=0, tie=0.
For i=0..19 execute one CONTROL ADD address,R3,i, then READ2 inserting R0's
reply into raw at 2i, then kernel LT R1,R0,2; ADD observed,observed,R1.
The address ADD is paid even for i=0. These forty ALUs count observations once,
not once per candidate. R3 survives every capture. After capture R3 is free.

At each candidate entry execute the existing CONTROL MOV candidate,c. Its
two kernel initializations are MOV distance,0; MOV R3,candidate. The second
is a real cached-candidate handoff, not another uncounted candidate MOV.
Each candidate's twenty cells has exactly these eleven kernel instructions:

| Step | Instruction and destination                         |
|------|-----------------------------------------------------|
| 1    | AND R0,R3,column_i                                  |
| 2    | SHR R1,R0,2                                         |
| 3    | XOR R0,R0,R1                                        |
| 4    | SHR R1,R0,1                                         |
| 5    | XOR R0,R0,R1                                        |
| 6    | AND R0,R0,1                                         |
| 7    | EX R1,raw-low[2i:2] or raw-high[2(i-16):2]           |
| 8    | LT R2,R1,2                                          |
| 9    | NE R1,R1,R0                                         |
| 10   | AND R1,R1,R2                                        |
| 11   | ADD distance,distance,R1                             |

The raw-high operand is the separate eight-bit field, not a 40-bit integer.
Steps 1..6 remain six charged ALUs even when c or column is a literal.
Observation masking excludes both 10 and 11. No cell address is set during
these comparisons: all raw data is already in D, and no persistent reread occurs.

The reduction after each candidate is branchless and exactly six instructions:

| Step | Instruction                                   |
|------|-----------------------------------------------|
| 1    | LT R0,distance,bestDistance                    |
| 2    | EQ R1,distance,bestDistance                    |
| 3    | OR R2,tie,R1                                  |
| 4    | SELECT tie,R0,0,R2                            |
| 5    | SELECT best,R0,c,best                          |
| 6    | SELECT bestDistance,R0,distance,bestDistance   |

c in step 5 is the four-bit literal for this generic candidate block, not a
ROM lookup indexed by acquired answers. Regeneration later uses the acquired
best slot as its input to the inherited generator. Strict improvement clears
tie; equality sets it; greater distance preserves it. Starting at 21 ensures
the first candidate wins even with zero observations. Later equal minima
preserve the first best, but the tie flag forbids corrective writes.

The final seven kernel instructions are EQ R0,observed,20;
EQ R1,bestDistance,0; AND R0,R0,R1; SELECT R0,R0,2,3;
SELECT R0,tie,1,R0; EQ R1,observed,0; SELECT R0,R1,0,R0.
Thus h=0 overrides h=1; h=2 requires all twenty agreeing observations and a
unique minimum; every other unique result is h=3. h returns in R0.

| Accounting class                              | Count                   |
|-----------------------------------------------|-------------------------|
| Initialization/capture as originally priced   | 4+20(1 insertion+2)=64 |
| Candidate kernels                             | 16(2+20(11)+6)=3648    |
| Health                                        | 7                       |
| Original non-read/non-route subtotal           | 64+3648+7=3719          |
| Pure ALUs, excluding READ2 insertion           | 44+3648+7=3699          |
| Whole kernel before transport                 | 3699+20(3)=3759         |
| Physical routed kernel                        | 3699+20(17)=4039        |
| CONTROL administration B3                     | 1+20+16+2=39            |

3719 is not 3719 extra ALUs plus twenty full READ2 accesses. That would double
charge twenty insertions. B3 is STAGE scan, twenty address ADDs, sixteen
candidate MOVs, MOV D40..43,best and MOV D55..56,R0. No runtime candidate or
cell increment, compare, backedge or return remains to charge. The 3520 cell
ALUs are stored inline. B3 relocation occurs only after counters die; best
is copied before observation packing overwrites D44..48.

## Repetition scan with five stored symbols

Addresses are 20(cue SHR 2)+(cue AND 3)+4i, i=0..4. Retain the accepted two
extra base ALUs. Raw occupies D0..9; best D44..47; zeros D48..52; ones
D53..57; observed D58..62; tie D63. Initialize zeros=0 and ones=0 in two
kernel MOVs. Each cell has CONTROL ADD address,R3,4i; READ2 reply R0 and
insertion into raw[2i:2]; then EQ R1,R0,0; EQ R2,R0,1;
ADD zeros,zeros,R1; ADD ones,ones,R2. R3 remains base until capture ends.

The twelve final kernel instructions, in order, are:

| Step | Instruction                       |
|------|-----------------------------------|
| 1    | ADD observed,zeros,ones            |
| 2    | EQ R0,observed,0                   |
| 3    | EQ tie,zeros,ones                  |
| 4    | GT best,ones,zeros                 |
| 5    | SELECT R1,best,ones,zeros          |
| 6    | EQ R2,observed,5                   |
| 7    | EQ R3,R1,5                        |
| 8    | AND R2,R2,R3                      |
| 9    | SELECT R2,R2,2,3                  |
| 10   | SELECT R2,tie,1,R2                |
| 11   | SELECT R2,R0,0,R2                 |
| 12   | MOV R0,R2                         |

Empty votes return h=0 despite tie=1. Nonempty equal counts, possible with
erasures even though n=5, return h=1. Five identical binary symbols give h=2;
other non-tied votes give h=3. A tied best=0 is not authorization to repair.

The original subtotal 39 is 2+5(1 insertion+4 ALUs)+12. Pure ALUs are 34;
34+5(3)=49 before transport and 34+5(17)=119 routed. Administration is
STAGE+five address ADDs+two relocations=8, not 39. The block-to-repetition
controller deltas remain B=-29, G=+2, H=-165: 303 without the transfer,
304 with it. Accepted 250/246 block and 223/81 repetition budgets are unchanged.

## RESPONSE

The public due-slot position is p=(t-1) modulo five; its four lanes are
848+4p+k, k=0..3. Those five public address tuples are
(848..851), (852..855), (856..859), (860..863), (864..867).
Public position selects literal operands, never the stored cue. Read all
eight slot bits, including reserved bits. Cue=slot bits 1..4 determines code
addressing; slot bit 0 alone enables decode. Every four-bit cue is legal.

During scan retain slot at D64..71, record-valid lane at D72..73, extracted
cue at D74..77, output bit at D78, saved record-valid predicate at D79 and
signed b at D80..95. The scan uses D0..63. Addressed allocation is exactly 96
bits; scan live occupancy is at most 95 because output is not live yet.
Output becomes live only after scan counters die. There is no decoder base
slot: compute R3 after the gate, retain it through captures and release it.
b=0 is initialized before any reject branch and survives all scan arithmetic.
Frozen variants omit record-valid/b operations, not replace them with reads.
R6's two relocations set best=D40..43 and h=D55..56; R7 reads that h slot.
For repetition append AND R0,R0,3; ADD R3,R3,R0 to R5 before its scan.

| ID | CONTROL sequence and paid work interleaved in order                                         | C bound |
|----|---------------------------------------------------------------------------------------------|---------|
| R0 | After outer M,C: MOV micro-PC,entry; MOV b,0                                                  | 2       |
| R1 | STAGE slot-read; four MOV address,848+4p+k, each followed by READ2 into D64+2k                | 5       |
| R2 | Learning only: STAGE valid-read; MOV address,884; READ2 into D72..73; EX D79,valid-lane bit 0 | 3       |
| R3 | EX f0,slot bit 0; EX R0,slot cue; MOV D74..77,R0                                             | 3       |
| R4 | STAGE decode-gate; paid M; BR not f0 to R10; BR rejected to R10                               | 3       |
| R5 | EX R0,cue; SHR R1,R0,2; SHL R2,R1,4; SHL R1,R1,2; ADD R3,R2,R1                             | 5       |
| R6 | Full block scan and its STAGE, twenty address ADDs, sixteen candidate MOVs, two relocations  | 39      |
| R7 | GE f0,h,2; BR not f0 to GUESS                                                               | 2       |
| R8 | Unique: EX R0,best; EX R1,cue; AND R1,R1,3; SHR R0,R0,R1; AND R0,R0,1; MOV D78,R0; BR EMIT | 7       |
| RG | GUESS alternative: paid one-bit input into R0; MOV D78,R0; fall through to EMIT              | 1       |
| R9 | EMIT: STAGE output; paid one-bit output from D78                                            | 1       |
| RF | BR public-no-feedback to R10; STAGE feedback; paid yield/deposit; paid b input; MOV b,R0     | 3       |
| R10| Learning: BR not D79 to R12                                                                 | 1       |
| R11| Reward read/add/clamp/rewrite sequence below                                                | 21      |
| R12| MOV R0,0; STAGE slot-clear; four literal address MOVs, each followed by WRITE2 zero          | 6       |
| R13| STAGE exit; BR S; paid S                                                                    | 2       |

R2, b initialization, R10 and R11 are absent in frozen variants. RF's learner
input/MOV is absent in frozen ecology; RF has no input/deposit at all in
isolation/H1. Its branch predicate is a public phase/planned-due flag, not a
RAM-validity, correctness or original-cue interface. Public feedback absence
may be compiled out instead. Spurious emissions bypass both feedback packets.
All references to omitted R10 target R12 in nonlearning variants. The public
flag is only the already declared planned-due schedule boundary, not an extra
scalar containing a due cue, scheduled usefulness or target.
DECODE M preserves f0 and D; the immediate branches consume f0/f3. RF's yield
cap/deposit is the already paid DECODE METER's bounded continuation, not a new
M fee or unpriced reservoir ALU. It may clobber R words before the b packet
arrives. MOV b saves the incoming sixteen-bit encoding; sign extension is later.

R11 is STAGE reward-read (1), eight MOV address,888+k/READ2 into R0 bits
2k..2k+1 (8), signed EX R0,R0 low16 (1), signed EX R1,b (1), the five
separate kernel ALUs below, AND R0,R0,65535 (1), STAGE reward-write (1),
eight MOV address,888+k/WRITE2 from R0 bits 2k..2k+1 (8): 21 CONTROL.
There is one reward read and one rewrite, never an intermediate persistent sum.

The reward kernel is ADD R0,R0,R1; LT R2,R0,-256;
SELECT R0,R2,-256,R0; GT R2,R0,256; SELECT R0,R2,256,R0.
R0 holds the signed sum in 32 bits before clamps, including corrupted reward
extremes. D79 remains live until R10; D64..71 and scan may then die. The slot
clear uses its public position, not a surviving acquired address or extra read.

The learning block unique/feedback/valid-record path uses
2+5+3+3+3+5+39+2+7+1+3+1+21+6+2=103 CONTROL.
The guessed counterpart uses 97. Both branch alternatives stored together
use 104 CONTROL sites. Repetition adds two base ALUs, substitutes 8 for 39
administration, and substitutes EX R0,best; MOV D78,R0; BR EMIT (3) for R8:
unique 70, guessed 68. Every one-envelope path is therefore below 256.

| Learning path                            | Block CONTROL | Decode/scalars                    |
|------------------------------------------|---------------|-----------------------------------|
| Invalid slot, valid record                | 45            | None; b remains zero              |
| Rejected decode, valid record             | 46            | None; b remains zero              |
| Invalid slot, invalid record              | 24            | None; still paid valid-lane read  |
| Rejected decode, invalid record           | 25            | None; still paid valid-lane read  |
| Admitted unique, feedback, invalid record | 82            | Scan, output, yield and b         |
| Admitted guess, feedback, valid record    | 97            | Scan, guess, output, yield and b  |

Retaining RF's single public absence BR even in isolated variants gives these
additional executed bounds; public constant-folding may delete that BR, not
add a runtime test or new scalar.

| Nonlearning variant | Block unique/guess | Repetition unique/guess |
|---------------------|--------------------|-------------------------|
| Frozen ecology      | 76/70              | 43/41                   |
| Isolation or H1     | 75/69              | 42/40                   |

All nonlearning invalid-slot/rejected-decode paths use 19/20 CONTROL,
respectively, and no record access. Frozen ecological spurious emissions take
the no-feedback branch, saving its STAGE and yield packet. The same emitted
bit slot is consumed once; omitted feedback never becomes an implicit zero
packet. These omission rules and explicit R10-to-R12 retargeting cover every
public RESPONSE variant without an acquired phase selector.

Invalid action/reserved/terminal bits do not suppress RESPONSE finalization:
only its paid record-valid bit matters. No code writes occur on any path.
An empty/tied guessed output never becomes decoder best or a correction input.

Routed learning base is 823 energy and three material per source; after an
invalid-record branch it is 626 energy and one per source. Nonlearning base
is 616 and one per source. Decode adds K=4039/119 plus actual scalar count:
learning unique/guess at most 3/4, frozen ecology 2/3, isolation 1/2.
Thus learning maxima remain 4866/946 and isolated maxima 4657/737.
Frozen-ecology guessed maxima are 4658/738, not the isolated 4657/737;
the extra scalar is its permitted physical feedback, not a tariff change.

## Scheduled TERMINAL

This outer operation is separate from controller terminal D. Read all record
lanes 884..899 into D0..31. Retain eligible D32, old-s D33..37, old-action
D38..39, signed reward D40..55, predicate D56 and old-base D64..74.
Full record plus extracted metadata/reward occupies at most 56 bits while
extracting; full record is dead before the gate. No stored-terminal decision
is made: this scheduled service always supplies bootstrap zero.

| ID | CONTROL sequence and interleaving                                                    | C bound |
|----|--------------------------------------------------------------------------------------|---------|
| T0 | After outer M,C: MOV micro-PC,entry                                                  | 1       |
| T1 | STAGE record-read; sixteen MOV address,884+k followed by READ2 into D2k              | 17      |
| T2 | Ten extraction/eligibility instructions below                                        | 10      |
| T3 | STAGE TD-gate; paid M; BR ineligible to T6; BR rejected to T6                         | 3       |
| T4 | Signed reward handoff, base formation, staged Q read/kernel/rewrite below             | 28      |
| T5 | BR T6                                                                               | 1       |
| T6 | MOV R0,0; STAGE record-clear; sixteen MOV address,884+k followed by WRITE2 zero       | 18      |
| T7 | STAGE exit; BR S; paid S                                                             | 2       |

T2 is EX R0,record.valid; EX R1,record.action; NE R2,R1,3;
AND R0,R0,R2; MOV eligible,R0; EX R0,record.s; MOV old-s,R0;
MOV old-action,R1; signed EX R0,record.reward; MOV reward,R0.
Every source is read before its containing record is released. All five-bit
old-s values are legal; action=3 is dropped, not masked into another action.

T4 is signed EX R1,reward (1); EX R0,old-s; SHL R2,R0,1;
ADD R2,R2,R0; EX R0,old-action; ADD R2,R2,R0; SHL R2,R2,3;
ADD R2,R2,80; MOV old-base,R2 (8); STAGE old-Q-read (1);
EX address,old-base then seven ADD address,address,1, each followed by
READ2 into R0's low sixteen bits (8); the Q kernel's signed EX R0,low16;
STAGE TD-arithmetic (1); the kernel's MOV R2,0 and 23 ALUs;
STAGE Q-rewrite (1); EX address,old-base then seven ADD address,address,1,
each followed by WRITE2 extracting R0's updated low sixteen bits (8).
No gate intervenes between reward/Q loading and rewriting. Low-field WRITE2
extraction is already paid; no implicit full-record merge occurs.

For completeness, the accepted 23-ALU sequence uses predicate p=D56:

| Steps | Exact arithmetic sequence                                                                 |
|-------|-------------------------------------------------------------------------------------------|
| 1..4  | LT p,R1,-256; SELECT R1,p,-256,R1; GT p,R1,256; SELECT R1,p,256,R1                          |
| 5..10 | SHL R3,R1,4; SHL R1,R2,4; SUB R1,R1,R2; ADD R3,R3,R1; SHL R1,R0,4; SUB R3,R3,R1           |
| 11..12| Arithmetic SHR R1,R3,7; AND R3,R3,127                                                       |
| 13..17| GT R2,R3,64; EQ p,R3,64; AND R3,R1,1; AND R3,R3,p; OR R2,R2,R3                             |
| 18..19| ADD R1,R1,R2; ADD R0,R0,R1                                                                 |
| 20..23| LT p,R0,-32768; SELECT R0,p,-32768,R0; GT p,R0,32767; SELECT R0,p,32767,R0                 |

Old q remains R0 through step 18. Negative half-ties use floor quotient and
nonnegative remainder: -64 rounds to 0, -192 to -2. No extra absolute-value,
fifth register, reward reread, successor address or Q read is hidden.

Full CONTROL is 80; valid but rejected TD is 51; ineligible/action=3 is 50.
All sixteen clear writes execute on every funded exit, including reserved
bits and same-value zeros. The independent kernel is 8R+signed EX+zero MOV+
23 ALUs+8W: 97 before routes, 217 routed, two material per source.
Mandatory base is 904 routed/four material per source; full service is
1121/six per source. Dropping TD releases only 217/two per source, never the
paid M, record reads, full retirement, S or later public obligations.

## AGE-LOW and AGE-HIGH

Choose literal expansion, with D0..3 holding two raw lane replies, D4..8 a
five-bit domain identifier, and D10..13 the four-bit result. These are the
only age values live at once. The identifier is explicitly MOVed, not a
corruptible persistent cursor; its public literal addresses are listed below.

After outer M,C execute MOV micro-PC,entry. For each of its ten literal words:
MOV D4..8,d; MOV address,low_d; READ2 into D0..1;
MOV address,high_d; READ2 into D2..3; STAGE age-kernel;
execute the eight kernel instructions; MOV address,low_d;
WRITE2 from D10..11; MOV address,high_d; WRITE2 from D12..13.
Then STAGE exit; BR S; paid S. There are six CONTROL instructions per word,
not a hidden runtime loop or twenty-slot estimate: 1+10(6)+2=63 per outer.
This is below both 232 allocated and 256 prepaid. Padding is not executed work.

The eight kernel instructions are EX R0,D0..1; EX R1,D2..3;
SHL R1,R1,2; XOR R0,R0,R1; EQ R2,R0,15; ADD R0,R0,1;
SELECT R0,R2,15,R0; AND D10..13,R0,15. The narrow fixed result destination
is an ALU slot under the accepted ABI. If a future lowering instead puts
the AND result in R0 and adds MOV D10..13,R0, count ten more CONTROL:
73 still fits, but it is not this 63-instruction witness.

Every current four-bit encoding is valid, including corrupted fifteen. The
sum uses a wide register, so fifteen cannot wrap to zero before SELECT.
Both source lanes are paid, even when age is already fifteen or later reset.
No scalar, sensor, old-age vector or discretionary gate is present. Each
operation costs 392+20(10)+80+20(14)=952 and five material per source.

## CONDITION-0 through CONDITION-19

Every service has its own public fixed-domain entry. After outer M,C execute
MOV micro-PC,entry; STAGE condition-gate; paid nested M;
BR rejected to EXIT. Admitted body: STAGE dues; pay four energy and one
material at the domain hub through the already paid METER continuation;
MOV R0,0; MOV address,low_d; WRITE2 zero;
MOV address,high_d; WRITE2 zero. EXIT is STAGE exit; BR S; paid S.
Admitted CONTROL=9; rejected CONTROL=5, both below 64 and 256.

There is no RAM read, age test, sensor, per-lane gate, old-bit preservation,
acquired domain cursor or follow-up return. Both entire dedicated age lanes
are written, including zeros already present. Gate and physical-dues executor
work are the named METER128 service, not free controller ALUs. The four-energy
medium tariff is additional, not another CONTROL/kernel or free age write.

| d  | AGE outer | Low | High | Domain hub | Lane hubs | Body material (P0,P1,P2,P3) |
|----|-----------|-----|------|------------|-----------|-----------------------------|
| 0  | LOW       | 924 | 925  | 0          | 0,1       | (2,1,0,0)                   |
| 1  | LOW       | 926 | 927  | 0          | 2,3       | (1,0,1,1)                   |
| 2  | LOW       | 928 | 929  | 0          | 0,1       | (2,1,0,0)                   |
| 3  | LOW       | 930 | 931  | 0          | 2,3       | (1,0,1,1)                   |
| 4  | LOW       | 932 | 933  | 0          | 0,1       | (2,1,0,0)                   |
| 5  | LOW       | 934 | 935  | 1          | 2,3       | (0,1,1,1)                   |
| 6  | LOW       | 936 | 937  | 1          | 0,1       | (1,2,0,0)                   |
| 7  | LOW       | 938 | 939  | 1          | 2,3       | (0,1,1,1)                   |
| 8  | LOW       | 940 | 941  | 1          | 0,1       | (1,2,0,0)                   |
| 9  | LOW       | 942 | 943  | 1          | 2,3       | (0,1,1,1)                   |
| 10 | HIGH      | 944 | 945  | 2          | 0,1       | (1,1,1,0)                   |
| 11 | HIGH      | 946 | 947  | 2          | 2,3       | (0,0,2,1)                   |
| 12 | HIGH      | 948 | 949  | 2          | 0,1       | (1,1,1,0)                   |
| 13 | HIGH      | 950 | 951  | 2          | 2,3       | (0,0,2,1)                   |
| 14 | HIGH      | 952 | 953  | 2          | 0,1       | (1,1,1,0)                   |
| 15 | HIGH      | 954 | 955  | 3          | 2,3       | (0,0,1,2)                   |
| 16 | HIGH      | 956 | 957  | 3          | 0,1       | (1,1,0,1)                   |
| 17 | HIGH      | 958 | 959  | 3          | 2,3       | (0,0,1,2)                   |
| 18 | HIGH      | 960 | 961  | 3          | 0,1       | (1,1,0,1)                   |
| 19 | HIGH      | 962 | 963  | 3          | 2,3       | (0,0,1,2)                   |

Every conditioner costs 520 on rejection, or 552 plus the displayed material
vector on admission. Across twenty, body vectors sum to (15,15,15,15).
Adding both AGE operations gives upkeep 12304+32n and material
(10,10,10,10)+sum of admitted vectors, hence 12944/(25,25,25,25) at n=20.
n is external audit notation, not a retained state variable.

Age storage remains physically cross-domain: even d's lanes belong to hubs
0/1 and odd d's to 2/3, regardless of d's domain hub. Both increments finish
before any conditioner. Fault physics uses the simultaneous post-operation
age state; no service copies an age vector for the fault or exposes it to
allocation. Rejection has no second pass, refund or unpriced old-age read.

## Exact local and future remainder witnesses

Write cost vectors in (energy; P0,P1,P2,P3), let v=(1,1,1,1), and let e_j
be a source unit vector. Auxiliary READ2=(10;0), WRITE2 at n=(14;e_(n mod 4));
code READ2=(17;0), code WRITE2=(23;e_block); one ALU=(1;0), M=(128;0),
C=(256;0), S=(8;0). Scalar routes for these RESPONSE packets terminate at X,
so each permitted occurrence is (1;0). General routes replace these scalar
and access terms with the inherited I_G/R_G/W_G expressions, once only.

At every debit c use R >= c+L+T+rho componentwise, rho=(1;0,0,0,0).
L is the sum of the unexecuted mandatory suffix of the displayed literal
path, with a componentwise maximum at an unresolved branch. This definition
is constructive: each site has a finite suffix in immutable ROM; no worker
summation, copied balance or path counter is needed. METER performs its paid
quote lookup/comparisons. Already paid M/C/accesses never remain in L.

| Service checkpoint                  | Exact local obligation after the stated checkpoint                        |
|-------------------------------------|----------------------------------------------------------------------------|
| RESPONSE before outer M             | Learning worst (823;3v); frozen (616;v), excluding optional decode           |
| RESPONSE after paid DECODE M        | Valid record (261;3v); invalid/frozen (64;v)                                |
| RESPONSE optional body quote        | (K+s_max;0), plus preceding L, T and rho                                   |
| TERMINAL before outer M             | (904;4v), excluding optional TD                                            |
| TERMINAL after paid TD M            | (232;4v); optional body quote (217;2v)                                     |
| AGE after outer M,C, before word i  | (8;0)+sum from k=i to 9 of (56;e_low(k)+e_high(k))                          |
| CONDITION before outer M            | (520;0), excluding optional body                                          |
| CONDITION after nested M            | (8;0); optional body quote (32;b(d))                                       |

RESPONSE's 261 is reward finalization 197, clear 56 and S8; 197 consists of
eight reads 80, eight writes 112 and five ALUs. Invalid record releases that
197/two per source only after its paid valid-lane read and eventual branch;
the valid read itself still costs ten. Before discovery the minimum retains
the full 823/three per source even after rejected controller/DECIDE. Slot
invalidity or rejected decode releases no valid-record finalization.
Optional decode reserves the complete K and every permitted scalar before
any scan/output/deposit. A paid unique/absence branch releases the unused guess
or absent-feedback suffix, never refunds it. b=0 and retirement remain defined.

For the block capture kernel, debit four initial ALUs, then twenty
(17+2), then sixteen (2+220+6), then seven: total 4039. Repetition is
2+five(17+4)+12=119. The already paid C covers address/candidate/branch
instructions while their micro-PC still distinguishes finite remainders.
These sums give every scan prefix, not only an end-to-end affordability test.
Decode body promotion places its full remaining scan/scalar suffix in L;
later resource deposits cannot retrospectively admit an unfunded prefix.

After admission, TERMINAL's optional 217 and eight Q writes become local
obligations; no later internal gate can drop its clear. Ineligible action=3
never forms a Q address, and no stored terminal bit narrows scheduled T.
For each AGE word replace 56 by the remaining suffix of two READ2, eight
ALUs, and two WRITE2. Both lane sources appear separately. No whole-domain
material average or implied source transfer is legal.

CONDITION promotes the full 32/b(d) before dues. After dues its remainder is
two fixed writes plus S; after the first write it retains the second and S.
No mid-operation fault can create a paid-medium/unwritten-age lapse. Rejected
body branches straight to S and releases no later service's mandatory base.

Examples of public T: after AGE-LOW it includes AGE-HIGH (952;5v), all twenty
CONDITION minima (10400;0), and scheduled TERMINAL (904;4v) when present;
after AGE-HIGH omit its own 952/5v. At CONDITION-d, T includes (19-d) later
520-energy minima plus scheduled TERMINAL's mandatory base. Optional later
conditioning/terminal bodies are not mandatory T. Earlier services include
both age services and all conditioners: upkeep mandatory (12304;10v).
Other scheduled RESPONSE/ADMIT/controller bases remain as the inherited
public schedule requires; controller bases include both Cs. No prior apparent
validity, successful conditioning or future gain reduces T.

The stated rho keeps pre-fault E positive. A sufficient post-fault-survival
bound additionally covers the one final energy leakage, separately from paid
operation spend. Material equality is allowed, including zero post-condition
stock; do not add a material survival residue or treat leakage as a writable
age/stock field. These traces preserve the 29394 pre-leakage learning bound
and its 605 margin after leakage against 30000, conditional on the other
selected service plans. They prove no arbitrary-injury funding or performance.

## Typed ROM occupancy without runtime calls

Use one target-independent image per PUBLIC representation/policy/phase
variant, as v0.6 permits. Policy/grid constants are inherited ROM operands;
they are not acquired bank IDs. Do not concatenate every policy, grid point,
phase and experimental individual into one acquired-address space. Public
service entry selects a literal entry address; inside the operation all
acquired branches use the single scratch micro-PC and counted instructions.

Each occupied address holds a typed CONTROL instruction, kernel ALU, READ2,
WRITE2, scalar I/O, sensor/attempt tariff slot, M/C/S or physical-dues opcode.
Bundled access route/insertion/extraction and METER's protected executor
internals are not separately interpreted worker helpers. If a future backend
exposes those internals as microinstructions, it must prove its own address
bound rather than silently claiming this abstract-machine witness.

Kernel tables are shared specification templates, NOT runtime subroutines.
Instantiate scan separately within controller and within each of the five
RESPONSE slot entries. Their final instruction falls through to its own
continuation. All displayed STAGE/BR targets remain explicit, priced sites.
There is no call stack, return-PC slot, acquired program selector, common
epilogue with an unpaid return, or relocation performed by a worker instruction.

| Controller stored class                 | Conservative sites |
|-----------------------------------------|--------------------|
| All repaired CONTROL alternatives       | 558                |
| Block pure scan ALUs and twenty READ2    | 3719               |
| Nonterminal TD, including accesses      | 71                 |
| Alternative terminal TD                | 41                 |
| Selection, including Q reads/padding    | 51                 |
| Twenty six-ALU regenerations            | 120                |
| Twenty possible code WRITE2            | 20                 |
| Record reads/clear/store/reject clear   | 64                 |
| Sensor's sixteen slots                 | 16                 |
| Separate resource-attempt alternatives | 32                 |
| Scalar sites, conservatively doubled   | 16                 |
| Outer/DECIDE/TD/ACTION/cell M, two C, S  | 27                 |
| Additional trap allowance              | 1                  |
| Total                                  | 4736               |

The 71 TD sites are 32 reads+4 signed EX+4 max+23 TD+8 writes;
terminal 41 is 8 reads+1 signed EX+1 zero+23 TD+8 writes; selection 51 is
24 reads+3 signed EX+24 slots. The sixteen scalar-site allowance exceeds the
one offer, three random and two resource-alternative request/yield sites;
sensor encoding is already in its sixteen slots. Duplicating branch tails
changes stored sites, not executed budgets. The extra trap allowance can
overcount the trap already included in 558; it cannot undercount it.

RESPONSE needs at most 104 CONTROL+3699 scan ALUs+45 accesses+5 reward ALUs+
4 scalars+4 envelopes+1 extra trap allowance=3862 sites per slot entry.
The 45 accesses are four slot reads, one valid read, twenty code reads,
eight reward reads, eight reward writes and four slot clears. Scheduled
TERMINAL needs 80+32 record accesses+25 TD ALUs+16 Q accesses+4 envelopes=157.
Each AGE needs 63+80+40+3=186. Each CONDITION needs 9+2 writes+4 envelopes+
1 physical-dues opcode=16. These counts include stored alternatives rather
than assuming an execution cap is also a storage cap.

For conservative linking, add two separately typed prepaid-METER continuation
sites to the controller's two resource alternatives, and one to RESPONSE's
yield deposit: controller demand <=4738, RESPONSE <=3863. These sites execute
already paid cap/deposit work, not another M fee or free CONTROL arithmetic.
CONDITION's one physical-dues site was included already. The capacities below
use these larger counts rather than depending on a fused receive/deposit opcode.

The following disjoint half-open address intervals provide a constructive
occupancy witness. Unoccupied padding addresses need not be executable;
all concrete targets must lie within their owning occupied sequence.

| Segment                    | Address interval | Capacity | Proven demand |
|----------------------------|------------------|----------|---------------|
| Controller                 | [0,4800)         | 4800     | 4738          |
| RESPONSE p=0               | [4800,8896)      | 4096     | 3863          |
| RESPONSE p=1               | [8896,12992)     | 4096     | 3863          |
| RESPONSE p=2               | [12992,17088)    | 4096     | 3863          |
| RESPONSE p=3               | [17088,21184)    | 4096     | 3863          |
| RESPONSE p=4               | [21184,25280)    | 4096     | 3863          |
| Scheduled TERMINAL         | [25280,25472)    | 192      | 157           |
| AGE-LOW                    | [25472,25664)    | 192      | 186           |
| AGE-HIGH                   | [25664,25856)    | 192      | 186           |
| CONDITION-d, d=0..19       | [25856+16d,25872+16d) | 16 each | 16 each   |
| Other selected services    | [26176,65535)    | 39359    | See scope     |

Requested traces occupy capacity 26176 < 65535, even with five duplicated
RESPONSE scans; their summed site-demand upper bound is
4738+5(3863)+157+2(186)+20(16)=24902.
Maximum assigned address is 26175, and 65535 remains unused. Literal targets
can be assigned by prefix sums of the listed expansions inside each segment;
16-bit target width is proved without producing a runnable ROM or a linker.
No numeric target need be computed at runtime. Relocation validation is a
later mechanical conformance check, not a reason to withhold this scoped
design-level capacity result.

Even retaining three separate controller program types (RL, fixed, DRIVE)
in the same representation/phase image costs capacity at most
3(4800)+5(4096)+192+2(192)+20(16)=35776, leaving 29759 addresses.
This optional placement shifts later intervals by 9600, not their instruction
counts. Constants for the periodic/cut grid require no cloned instruction text;
they are public inherited operands selected with the variant, not acquired
state. Separate fixed-rule alternatives also fit the conservative controller
capacity. This is not concatenation of all experimental policies and labels.

The whole-project statement needs a precise boundary: these intervals prove
capacity for the controller and requested services, not a linked trace for
TICK, ADMIT, LESSON, COMMIT, ISOLATE or an unspecified future METADATA service.
Their executable instructions must fit the remaining 39359 sites, or use an
explicitly public separate image permitted by v0.6; an acquired bank selector
is forbidden. A bare 256-executed-C tariff cannot prove their stored occupancy.
No full-E3-ROM pass is fabricated from that tariff. This is a concrete finite
remaining design question about five named existing service entries and any
new metadata entry, not a generic demand to implement E3 first.

## Disposition and verification boundary

| Obligation                     | Static design disposition                                      |
|--------------------------------|----------------------------------------------------------------|
| Block scan                     | Pass: 3699 pure ALUs+20 READ2; B3=39; 4039 routed                |
| Repetition scan                | Pass: 34 pure ALUs+5 READ2; administration=8; 119 routed         |
| Controller bounds              | Preserved: block 250/246; repetition 303 or 304 with transfer    |
| RESPONSE                       | Pass: block C<=103, repetition C<=70; four scalars maximum       |
| Scheduled TERMINAL             | Pass: C<=80, independent paid 97/217 TD; mandatory retirement   |
| AGE-LOW/HIGH                   | Pass: each C=63, kernel80, reads20, writes20                    |
| Twenty CONDITION instances     | Pass: each C<=9, no reads, exact sourcewise body vector         |
| Scratch and liveness           | Pass under accepted slot ABI: D<=96, four R, control32          |
| Requested typed-ROM occupancy  | Pass: demand<=24902 within capacity26176; no acquired bank      |
| Entire selected E3 image       | Not certified: five other named service traces are not expanded |
| Actual runtime conformance     | Not performed; no implementation or execution claimed          |

No requested service needs a higher tariff, extra CONTROL, scratch word,
scalar channel or persistent field. Full branch/register/link validation of
the future implementation is a later conformance test, not a prerequisite to
accepting these finite symbolic design witnesses. This research does not amend
the selected contracts or reviews, and it does not waive independent B05-B07.

The only uncovered ROM-design statement is exact and bounded: show that the
target-independent TICK, ADMIT (five public slot entries), LESSON, COMMIT and
ISOLATE instruction expansions, plus any explicitly selected further METADATA,
occupy at most the remaining 39359 sites of the one-controller layout. Their
complete CONTROL/liveness conformance is separately inherited work, not proof
supplied by unused capacity. If requiring all three controller types together,
use 29759 instead. Do not call an unexpanded tariff a stored-instruction bound.

Read-only scalar arithmetic checked kernel sums, path counts, material totals
(15,15,15,15) over all twenty conditioner rows, and address capacities.
The first document-table parser returned an erroneous zero sum; direct field
parsing corrected that validation utility, not the trace or physical vectors.
No scan was executed over sample or exhaustive data;
tie/health correctness follows the symbolic predicates and counter ranges.
Editor diagnostics reported no errors at the interim check. Only this research
file was created/updated; no worker, training, E3 program or generated ROM ran.

## Recommended next checks not performed

* [ ] Close the five named unexpanded service entries' storage bound if claiming
  whole-E3 ROM closure; the requested-service bound itself needs no linker run.
* [ ] At the separately authorized implementation stage, mechanically expand
  the traces and verify primitive typing, branch targets, all CONTROL paths,
  scratch live intervals, sourcewise prefixes and exactly one final S.
* [ ] Test empty/nonempty ties, strictly smaller-after-tie, 10/11 masking,
  four-bit candidate identity, negative TD half-ties, corrupted action=3,
  invalid-slot/valid-record finalization, age15, and conditioning equality.
* [ ] Complete the independent B05-B07 design work without claiming that funded
  services demonstrate retention, adaptive advantage or runtime noninterference.

## Clarifying questions

None. The allowed file, tariffs, state ABI and research-only boundary suffice.
Whole-project ROM coverage is a named technical remainder, not a request for
routine permission or a fabricated requirement to implement before design freeze.