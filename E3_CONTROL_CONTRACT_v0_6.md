---
title: E3a two-budget controller contract
description: Prospective CONTROL256 execution budgets, normative repaired trace and conditional prices
ms.date: 2026-09-10
status: Selected prospective paper candidate - controller review qualified; no implementation or freeze
---

## Selection and exact precedence

Select two prepaid CONTROL256 EXECUTION BUDGETS, A and B, in the same atomic
controller. Each permits at most 256 executed nonkernel instructions and costs
256 energy, regardless of utilization. These are not 256-stored-address ROM
pages. Total CONTROL price is 512, not 1024. No budget transfers across regions,
operations or ticks; no second operation, fault window, METER, scratch clear,
scalar, persistent field, acquired page index or fuel counter is added.

This prospective version changes only the controller's one-C rule, its bound
propagation and the selected scratch/trace bindings. It adds scientific notes,
not a new objective. [E3_OPERATION_CONTRACT_v0_3.md](E3_OPERATION_CONTRACT_v0_3.md),
[E3_PHYSICAL_CONTRACT_v0_4.md](E3_PHYSICAL_CONTRACT_v0_4.md),
[E3_POLICY_CONTRACT_v0_5.md](E3_POLICY_CONTRACT_v0_5.md),
[E3_STATE_CONTRACT_v0_2.md](E3_STATE_CONTRACT_v0_2.md) and
[E3_PROTOCOL_v0_1.md](E3_PROTOCOL_v0_1.md) remain unchanged historical versions.
Legacy one-C conformance remains unproved; 495 is neither a proved lower bound
nor a demonstrated reachable maximum. The repaired schedule is accepted at paper-review
level only. No E3 executable, execution, result, design freeze or final draw is supplied.

Normatively incorporate the [trace instruction convention, complete A-K/H1-H5
schedule and gates/liveness sections](.copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md#L33-L192),
plus its [resource/fixed/repetition/DRIVE variants](.copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md#L193-L237).
Normatively incorporate every exact repair in the [review CT-001 through CT-010](.copilot-tracking/reviews/2026-09-10/e3-control-review.md#L46-L537),
including its literal TD/selection instructions and branch targets. These are
required specification content, not optional supporting examples. Precedence
for this candidate is: this contract, then those CT repairs, then the incorporated
trace, then inherited contracts for otherwise unchanged rules. CT repairs override
the trace's ambiguous operand names, whole-word W increment and storage-page wording.
No research recommendation or prior approximate worksheet overrides a selected tariff.
No incorporated text authorizes execution or retroactively changes old versions.

## Payment and mandatory remainder rules

Every funded offered controller pays outer M=128, C_A=256, C_B=256, in that
order, before entry CONTROL and DECIDE M=128. Both codes, RL, fixed, frozen,
write-prohibited and DRIVE policies pay both, including rejected DECIDE paths.
An unfunded minimum causes inherited physical shutdown, not unpaid execution.
Nonoffered ticks have no new controller charge; in particular acquisition and H1 do not.

The minimum and every enclosing public T include both Cs, DECIDE, learning old
clear, the single S=8, all other mandatory services and energy residue one.
After prepayment remove both Cs from L; do not charge their instructions again.
S executes only at final exit, clears all 256 scratch bits, and terminates
without a subsequent micro-PC write. Region transfers neither clear nor suspend.
Retain componentwise R >= c+L+T+rho, sourcewise material equality, and paid METER
before optional body testing. Earlier apparent validity never narrows public T.

At cell i entry retain (n-i)(g+128), store/exit, T and residue. After generation
retain the current possible gate and (n-i-1)(g+128). A clean charged branch releases
only its unused current gate bound. A needed gate pays 128 before testing WRITE2;
the paid current gate then leaves L. Failure branches immediately to return/store/S,
releasing the unvisited suffix. Completed writes retain later obligations.
Releases reduce bounds, never refund or deposit resources. ROM plus scratch micro-PC
selects finite remainders inside METER; no worker reserve/spent/admission ledger exists.

## Operand ABI and exact live bindings

An instruction has at most 32-bit operands. Narrow fixed-slot MOV preserves
neighboring fields for one instruction; packed raw/record fields require EX.
SHL/SHR, Boolean ALU, ADD/SUB/NEG, compare, SELECT, EX, MOV, BR and jumps are
separate instructions. BR costs one on either outcome. STAGE is one MOV of a
literal address to existing micro-PC, not a call or argument-calculation macro.
Sequential advance is intrinsic to the instruction and updates scratch micro-PC.
READ2 insertion, WRITE2 extraction and route lookup remain bundled in their
separately paid accesses; lane-address loads/increments below remain CONTROL.

Decoder offsets are relative to its existing 96 bits. R0..R3 are the four
32-bit arithmetic words. The 32-bit control partition is micro-PC 0..15,
lane address 16..26, flags 27..31. Flag indices below are relative to those five bits.

| Interval      | Exact decoder allocation                                                          |
|---------------|-----------------------------------------------------------------------------------|
| Scan          | Raw 0..39; candidate 40..43; best 44..47; counters/tie 48..63                        |
| Scan inputs   | Offer cue 64..67; usefulness 68; base 69..75                                         |
| Postscan      | Best 40..43; h 55..56; cue copied to 49..52; usefulness still 68                      |
| Observation   | Raw 0..39; best 40..43; s 44..48; cue 49..52                                         |
| Old load      | Full record 64..95; metadata 53..61 extracted before record release                  |
| TD gate       | Eligible 53; old-s 54..58; old-action 59..60; terminal 61; reward 64..79              |
| TD body       | Same metadata; old-base 64..74; successor-base 75..85 after reward enters R1          |
| Selection     | B 64; T 65..66; X 67..70; equality predicates 55..57; result action 53..54            |
| Action/scrub  | Action 53..54; predicates 55..58; W 59..63; a 64..79; base 80..86; expected 87..88    |
| Current store | Packed word 0..31 after raw/best/cue/W die; retain s/action/a for packing             |

ACTION flag bits 0..1 hold action, bit 2 eligibility, bit 3 outcome, bit 4 a
temporary. F's two MOVs set the inputs; METER preserves them, writes outcome
and may clobber all R registers. F consumes outcome immediately, G reads retained
eligibility. Sensor source and TD shape reuse dead input flags earlier. After
dispatch, needed is decoder bit 55; expected and the eleven-bit address survive gates.

Select the exact unsigned packed increment `ADD decoder-word1,decoder-word1,134217728`,
where word1 is decoder bits 32..63 and the constant is 2^27. With W<=19 before
increment, W becomes <=20 without altering lower fields or overflowing the word.
Crossing bit 31 is unsigned, not signed cost overflow. Do not add literal one
to this packed word. W alone is retained; V derives from the unrolled micro-PC,
and A/V/tariff counts are one-way external audit values, never worker inputs.

Scan uses 76 decoder bits; old-load overlap is at most 94; TD gate 78; TD body
84; selection 60; scrub/write gate 89; store 55. No 40-bit operand, fifth arithmetic
word, second transition, whole candidate table or hidden argument partition exists.
Dead-slot release is not a free clear; only final S clears scratch.

## Normative path trace and operand repairs

The incorporated literal sequences expand the following named stages. Kernel,
lane, scalar, sensor, generation, attempt and METER costs are additional, not
CONTROL padding. D and E rows group costs; execute their handoffs in the order
specified below, not mechanically by table row. Every listed BR/STAGE is counted.

| Stage | Required work and dispatch                                           | CONTROL |
|-------|---------------------------------------------------------------------|---------|
| A     | Entry PC, zero predicate, STAGE DECIDE, paid DECIDE, rejection BR     | 4       |
| B1    | Two EX and two MOV offer fields                                      | 4       |
| B2    | Block base calculation and save                                      | 5       |
| B3    | STAGE scan, 20 addresses, 16 candidate MOVs, best/h relocation         | 39      |
| B4    | Cue EX/MOV, hub/source, STAGE sensor, two bin comparisons             | 7       |
| B5    | EX h/u, shifts/ORs, MOV s=16u+8e+4p+h                                | 9       |
| C1    | Sixteen literal old-record lane addresses, each with paid READ2      | 16      |
| C2    | All old metadata/reward extraction and retention                     | 12      |
| C3    | Terminal EX/shape SELECT/MOV/STAGE; paid TD; three BRs                 | 7       |
| D1    | Old Q base from retained metadata                                    | 8       |
| D2    | Nonterminal successor base from current s                            | 6       |
| D3    | Old-read 8, successor-read 24, rewrite 8 lane-address instructions     | 40      |
| D4    | Signed reward EX and four work STAGE instructions                    | 5       |
| C4    | Body-to-retire BR, zero MOV, sixteen literal clear addresses          | 18      |
| E1    | Fresh selection base and 24 Q-lane addresses after retirement         | 29      |
| E2    | STAGE, three rank MOVs, T check/BR, three consumption EXs, action MOV | 10      |
| F     | Init/eligibility/ACTION staging, rejection and scrub dispatch        | 12      |
| G     | Eligibility BR, cue EX, scrub-base calculation/save                   | 7       |
| H     | Twenty literal cells H1-H5, at most eleven each                       | 220     |
| I     | EX W; NEG; MOV a; BR store                                           | 4       |
| J     | Fifteen pack/STAGE instructions and sixteen store-address MOVs       | 31      |
| K     | STAGE exit; BR final S                                              | 2       |

B1 receives the paid packed offer in R2: EX cue into R0, EX usefulness into R1,
save at 64..67/68. R0 still holds cue for B2; reuse R2/R3 only afterward.
Retain base in R3 until all raw reads finish, before candidate arithmetic.
B3's two existing MOVs copy best 44..47 to 40..43 and paid h to 55..56 after
counters die. B4 moves cue 64..67 to 49..52 before sensing, preserving h/u/cue.
Sensor returns E/P in R0/R1; GE produces e/p in R2/R3. B5 loads h/u into R0/R1,
accumulates s in R1 and saves 44..48. Only then may old-record reads overwrite 64..95.

The old tuple is exactly (valid bit 0, old-s 1..5, old-action 6..7, signed
reward 8..23, terminal 24, reserved 25..31), relative to loaded decoder 64..95.
C2's sequence is EX valid; EX action; NE legal; AND eligible; MOV eligible;
EX old-s; MOV old-s; MOV old-action; EX terminal; MOV terminal; signed EX reward;
MOV reward. R1 retains action until its MOV; R0 is reusable. Extract reward before
overwriting the record. C3/D1 reference metadata 53..61, never the released word.
In particular (old-s=31,reward=0) must retain row 31, not reread a zeroed row field.

After TD METER, D4 uses `signed EX R1,reward-slot`, not zero-extending MOV.
For q=m=0,r=-1 this must round to zero, not the erroneous +32 update.
Form both bases before reading Q, using R0/R2/R3 while R1 holds reward.
Read old q into R0; successor first/second into R2/R3, compare/select into R2,
then third into R3 and compare/select into R2, using one dead decoder predicate.
The four maximum ALUs are paid separately. No gate intervenes from Q load to rewrite.
The [CT-005 exact 23-step TD witness](.copilot-tracking/reviews/2026-09-10/e3-control-review.md#L223-L266)
keeps R0=q until adding the rounded increment, then rewrites q' from R0.
Its floor quotient/nonnegative remainder gives roundEven(-64/128)=0 and
roundEven(-192/128)=-2; signed-32 clamping/saturation remains mandatory.
Terminal D is 28 CONTROL, supplies m=0 through its paid 97 kernel, and never
forms/reads a successor. Invalid/action=3 or rejected TD skips D, not its paid gate/clear.

E2 receives and saves B/T/X before E1 fills arithmetic words with fresh Q reads;
check T!=3 before reuse. CT-005's 21 selection ALUs plus three paid padding slots
use decoder equality bits 55..57, then R0=count, R1=lowest, R2=highest, R3=B.
After B-selection/count-two handling, dead highest receives T in R2; X uses R3.
Both count-three and exploration use the same T. Result goes through R0 to action
53..54. No omitted CONTROL is hidden in padding or a second random draw.

Block code address is 20(cue SHR 2)+i; repetition is 20(cue SHR 2)+(cue AND 3)+4i.
Q address is 80+8(3s+action)+k, k=0..7; Q row reads use 24 contiguous lanes.
Code lanes are 0..79, Q 80..847, record exactly 884..899. Old action=3 is
excluded before Q access; s is five bits, cue four. Unknown pre-read quotes use
maxima per source over every encoding, never scorer cues or an audit address.

Each literal cell executes H1 EX best then paid g generation; H2 MOV expected,
EX raw symbol, NE needed, BR clean; H5 MOV needed before H3 EX base, ADD literal
offset, STAGE write-gate and paid M; H4 BR rejected, otherwise paid WRITE2 then
the specified W increment. Clean/failed/completed cells cost 5/10/11 CONTROL.
Block g=6 uses AND, SHR, XOR, SHR, XOR, AND parity; repetition g=1. Compare
canonical 00/01 against 10/11 or wrong binary directly. Raw extraction uses
bits 0..31 or the separate eight-bit field 32..39, never a crossing 40-bit operand.

## Actions, alternatives and explicit branch targets

F initializes a=W=0, reads selected action and health from s, and pays ACTION
before rejection/dispatch. Current action is 0/1/2; T=3 is an external packet
contract trap, not a fourth action, repair or retry. ACTION ignores write eligibility
for forage/collection. Empty/tied/prohibited or rejected-entry scrub visits no cells.
The packet trap is outside successful-service bounds; its validity test/BR remain counted.
Clean unique scrub visits all n cells and pays every g. First needed-write failure
stops immediately. Main return is a=-W, or floor(accepted F/4), or 2 accepted C;
rejected ACTION retains the selection with a=0 for learning store.

The resource branch is exactly: EX R0,action; SHL R0,4; EX R1,cue; OR R0,R0,R1;
STAGE attempt; paid attempt/request/yield/cap-deposit; MOV R2,accepted-result;
EQ predicate,saved-action,0; BR forage-tail. Collection tail is SHL R2,1;
MOV a,R2; BR J. Forage tail is SHR R2,2; MOV a,R2; BR J. These duplicate tails
use fourteen stored but eleven executed CONTROL instructions, with no join jump.
Use the retained action, not a presumed METER-surviving arithmetic value.
Accepted amount, not raw offered yield, is returned by existing ACTION METER work;
no extra M, S, packet, queue or callback intervenes. Charges precede deposit.

DRIVE inserts EQ scrub; SELECT 16-or-0; MOV a after F's action EX and before
ACTION. Preserve a through rejection/prohibition/clean or partial scrub. Delete
only I's EX/NEG/MOV, retaining BR store. Resource return stays zero. DRIVE is
not a fair objective-matched arm. J packs at decoder 0..31: valid=1, s, selected
action, a masked to sixteen bits, public last-learning-tick terminal and zero
reserved bits. Old retirement precedes current store; rejected DECIDE stores nothing.

* A rejected learning DECIDE reaches zero MOV, sixteen addressed clears, BR K;
  frozen rejection goes directly to K. No old read, observation, action or new store occurs.
* C3's ineligible/rejected branches reach C4's first clearing instruction.
  Each D body has its own charged BR there; terminal never falls into nonterminal D.
* F rejection and G ineligibility target I in B; DRIVE targets its retained BR.
  F scrub branches over resource code to G; either resource tail branches directly to J.
* H0 clean branches to the one-instruction A-to-B transfer stub; completed H0
  falls through to it. Its counted jump reaches H1; H0 failure branches straight to I.
* In B, clean branches reach next cell (I after the last); completed cells fall
  through there; needed-write failures branch to I. No runtime loop/index increment exists.
* I branches to J, or K when nonlearning omits J. K stages/branches to final S.
  Cross-region BR is the charged transfer itself, never an extra free or duplicate jump.

## Executed bounds versus finite ROM storage

Stage totals are A4+B64+C53+D59+E39+(F+G)19+H220+I4+J31+K2=495.
A's main prefix through G is 238; add H0=11 and transfer=1 for 250.
B is 19(11)+4+31+2=246. Sum 496 is conservative, not a demonstrated reachable path.

| Path or variant                | A executed | B executed |
|--------------------------------|------------|------------|
| Learning RL block nonterminal  | 250        | 246        |
| Learning block stored-terminal | 219        | 246        |
| Learning DECIDE rejection      | 22         | 2          |
| Frozen DECIDE rejection        | 4          | 2          |
| Learning resource              | 242        | 33         |
| Learning DRIVE block           | 253        | 243        |
| Frozen RL block                | 138        | 215        |
| Fixed nonlearning block        | 110        | 215        |
| Learning RL repetition         | 223        | 81         |
| Learning DRIVE repetition      | 226        | 78         |

Drop/invalid TD and early exits shorten these bounds. Repetition B replaces
39 scan administration with 8 and adds two base ALUs: delta -29; G adds two,
H removes 165, giving 303/304 without/with transfer. Fixed E replaces 39 by
at most 11: EX e/p, EQ e/p low, periodic SUB/AND/EQ, three priority SELECTs,
MOV action. Threshold uses EX h/EQ instead; energy priority is last and wins.
All selected intervals {1,2,4,8,16,32,64,128,256} use the same prepaid Cs on
every offered tick, not only due scrubs. Due is ((t-1) AND (I-1))=0, with no
paused clock, makeup, acquired counter, per-cue schedule or new service charge.

For storage, main A250 plus its separate rejected-DECIDE block18 already means
268>256. Adding terminal D/BR29, resource alternatives14 and packet trap1 yields
A312; B246 gives 558 CONTROL sites. DRIVE has A315+B243=558. These are finite
target-independent sites, not acquired data or a claim of 256 physical words.
Select a per-public-variant ROM limit of 65535 addresses, 0..65534; address
65535 is unused. The 558 CONTROL sites and all separately typed primitive/kernel
sites must share that space, with literal sequential interleaving preserving the
charged branches above; no uncounted call/return or free transfer is introduced.
One existing sixteen-bit micro-PC suffices; no acquired bank selector is permitted.
Public representation/phase/policy selects the finite variant; paid scratch branches
select acquired-dependent paths. Exact linked addresses/internal expansions remain
a static obligation, not a completed full-ROM proof or permission to hide helpers.
CT-008 closes the CONTROL storage ambiguity, not the unexpanded scan/service traces.

## Version-only ledger and physical propagation

Record contract version v0.6 and separate C_A/C_B debits in the external ledger;
report padding/executed counts separately, never feed them back. Each offered
controller adds exactly 256 energy to v0.3/v0.5 prices and zero material/scalars.
Learning/frozen unrouted mandatory bases are 872/776, with M,C,S counts 1,2,1.
All other ledger rows, primitive/kernel prices and physical flows remain unchanged.
Scalar maxima stay RL resource/scrub 8/6, fixed resource/scrub 5/3; separate
RESPONSE maxima stay learning guessed/unique 4/3, frozen guessed 3, isolated guessed 2.

| Quantity or window          | Block | Repetition | Per-source offer g |
|-----------------------------|-------|------------|--------------------|
| Learning controller maximum | 9573  | 3273       | Unchanged          |
| Frozen controller maximum   | 8374  | 2074       | Unchanged          |
| HS-DEVELOP / HS-H2-REFERENCE | 29394 | 19174      | 66                 |
| HS-RECOVER                  | 26340 | 16120      | 47                 |
| HS-ACQUIRE, unchanged        | 17559 | 14467      | 48                 |
| HS-H1, unchanged            | 18339 | 14419      | 28                 |

Learning sum is 441+9573+4866+449+1121+12944=29394; plus final leakage one
is 29395, leaving 605 under unchanged 30000 energy support. Source maximum g=66
and the refill induction remain unchanged. Apply +256 times offered-controller
count to old window bounds; 128-tick block recovery becomes 3371520 before
leakage/boundaries. H1/acquisition aggregates and LL-EVAL13 H1 are unchanged.
Full-start post-sensor E >=65535-441-768-1-4039-20=60266; local P=255.
All E/P grid cuts remain high; cut pairs alias there, although periodic intervals
can differ. No bound applies automatically after arbitrary resource/substrate injury.
These are conditional financial upper bounds, not measured spend, functional
sufficiency, scarce H2 feasibility or matched actual expenditure. Frozen/fixed arms
still omit unused learner work; no dummy writes or favorable per-policy discounts.

## Additive scientific limitations and remaining closure

Adopt [POL-001 through POL-003](.copilot-tracking/reviews/2026-09-10/e3-b04-review.md#L89-L212)
as scientific/methods qualifications without changing v0.5 coefficients or gates.
POL-001: emitted useful errors receive -64, missing responses zero. Expected task
return 64(2p-1) can favor silence over below-chance emission; fair guesses tie.
There is no silence action and no proof avoidance is feasible, learned or optimal.
Report missing/rejected rows separately, retain planned failures in recall, and
apply recall/active/completion gates independently of return. Add no missing-response
penalty packet or outcome timing, especially in no-feedback recovery/H1.

POL-002: gamma=15/16 has scale 16 ticks and half-life about 10.74, not a hard
cutoff; gamma^5 is about 0.7242 and gamma^256 about 6.678e-8. Immediate income/write
costs can outweigh distant retention. Phase-start weighting is not suppression
of later local TD updates. Recovery learning is frozen; H1 has no task feedback.
Offline selection/retention gates are separate; changing gamma requires a new design.

POL-003: engineering pairing reuses labels only across prespecified engineering
candidates; independent individuals remain independent. Selected constants may
depend on engineering outcomes, which are not confirmatory evidence. Freeze them
before independent final targets, then pair each final table across its comparisons.
Reset counterfactuals hold inherited G and future target-independent Z fixed while
varying history; never retune constants or preserve an answer-dependent namespace.

All ten CT findings are incorporated and closed only at repaired paper-candidate
level. Concrete remaining static obligations are the block/repetition scan's
full register/branch expansion, linked typed-ROM occupancy, and complete bounded
RESPONSE, scheduled TERMINAL, AGE-LOW/HIGH and twenty CONDITION traces. In particular
the 232-slot AGE and 64-slot CONDITION allocations and RESPONSE's 112-slot estimate
are not traces. Require named paid stages, valid/corrupt/rejected paths, exact offsets,
kernel separation and sourcewise c+L+T+rho quotes within their unchanged service caps.
Scheduled TERMINAL remains independent of controller terminal D and stays in T.
Other inherited service trace requirements remain; none receives a second C here.
B05 branch/scarce calendars, B06 feasibility/headroom/precision, and B07 ownership/reset
still block design freeze. No routine renewed permission is needed for safe document
research, but none of these technical gates is waived or claimed implemented.
