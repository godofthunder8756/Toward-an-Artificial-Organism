---
title: E3 static controller trace research
description: Audit of the fused CONTROL256 controller and prospective priced alternatives
ms.date: 2026-09-10
status: Complete research - CONTROL256 unproved; prospective two-page witness
---

## Scope and questions

Resolve the static fused-controller design question, not simulator performance.
The existing CONTROL256 cap is **not proved** here. The literal-expandable control
schedule has a conservative bound of 495 instructions, or 496 with a page
transfer. This is not a lower bound on other implementations or an attainable
maximum on valid snapshots. The earlier 344/384 worksheets are not verified bounds.

A prospective pair of 256-slot control pages can accommodate the stated abstract
schedule, with page bounds 250 and 246. It requires an additive contract version:
B02 permits one envelope. No execution, source amendment, freeze or result is
authorized. The register-operand convention requires review, not silent replacement
with a more expensive instruction implementation.

## Evidence and authority

* E3_POLICY_CONTRACT_v0_5.md, read in full: objective, exact sensor instant, W-only return, policy rules, scratch witness and unverified CONTROL worksheet.
* E3_OPERATION_CONTRACT_v0_3.md, read in full: primitive/kernel tariffs, controller lifetime, mandatory tails, single envelope and finite scratch rules.
* E3_PHYSICAL_CONTRACT_v0_4.md, read in full: placement, routed costs, AGE/CONDITION trace obligations, support tables and sourcewise prefixes.
* E3_STATE_CONTRACT_v0_2.md, read in full: packed record offsets, symbol encodings, Q layout and acquired-state restrictions.
* .copilot-tracking/research/subagents/2026-09-10/e3-b04-policy-research.md: prior evidence, not a substitute for a primitive trace.

The B03 AGE split permits no implicit CONTROLLER split. Its 232-slot AGE and
64-slot CONDITION allocations still await traces. These are contract-specific costs.

## Instruction convention and literal expansion

Every semicolon-separated instruction below costs one CONTROL slot unless named
as an already priced primitive/kernel. MOV transfers at most 32 bits between
fixed scratch register slots, including narrow fixed slots; EX extracts one
packed field; SHL/SHR, AND/OR, ADD/SUB/NEG, comparison and SELECT each cost one.
No multiplication, fused compare-and-branch, address-plus-access, call/return
macro, table search, or whole-40-bit operand is assumed. BR costs one on either
outcome; a jump also costs one. Sequential instruction advance is part of the
executing instruction and advances the **scratch** micro-PC, not a host history.

STAGE is one MOV of a literal instruction address into micro-PC before the named
primitive, with no argument calculation. Named slots occupy inherited partitions,
not extra registers. Packed record/raw operands require EX. If fixed-slot MOV
lowers into mask/shift/merge ALUs, count every ALU: this witness does not certify
that lowering. This is an abstract operand convention, not native CPU energy.

Read the repetitions in the tables as **textual ROM expansion**, with no runtime
loop, call stack or free computed address. Use candidate literals 0..15, cell
literals 0..19 and columns (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,1,2,4,8,15).
Retain all six parity ALUs even when operands contain generic literals. No
individual labels, acquired Q, optimized answers or historical cues enter ROM.
Both terminal/nonterminal and resource/scrub paths are present as explicit BR
targets. Public representation/policy/phase selects the fixed program variant.

READ2/WRITE2 retain their bundled insertion/extraction and route lookup. Every
lane-address load or increment is additionally counted here, including constants.
For a contiguous q-word/row, the address sequence is EX/MOV address,base followed
by seven/23 ADD address,address,1 instructions. Constant record lanes each use
MOV address,literal. All accesses themselves remain outside CONTROL.

## Complete learning block scrub schedule

R0..R3 are the four arithmetic words; cue/s/best/W/reward/base are decoder slots,
not host locals. Listed kernel handoffs cannot absorb extra branch/address work.

| ID | Sequential nonkernel instructions or literal expansion                                                                                                                                                | Bound |
|----|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| A  | After outer M and C payment: MOV micro-PC,entry; MOV gate-predicate,0; STAGE DECIDE; paid DECIDE M; BR rejected to old-clear/exit                                                                            | 4     |
| B1 | Offer: EX cue; MOV cue-slot; EX usefulness; MOV usefulness-slot                                                                                                                                          | 4     |
| B2 | With cue still in R0: SHR j,cue,2; SHL x,j,4; SHL j,j,2; ADD base,x,j; MOV base-slot                                                                                                                      | 5     |
| B3 | STAGE scan; 20 ADD address,base-register,i before the paid reads; 16 MOV candidate,literal at candidate entry; MOV best-result; MOV health-result                                                         | 39    |
| B4 | EX cue; MOV postscan-cue-slot; SHR hub,cue,2; MOV sensor-source,hub; STAGE sense; paid sensor kernel/routes; GE e,E,Ecut; GE p,P,Pcut                                                                      | 7     |
| B5 | EX h; EX u; SHL u,4; SHL e,3; OR partial,u,e; SHL p,2; OR partial,partial,p; OR partial,partial,h; MOV s,partial                                                                                          | 9     |
| C1 | Sixteen MOV address,884+k, each followed by a paid READ2 inserting into the full old record, k=0..15                                                                                                      | 16    |
| C2 | EX valid; EX old-action; NE legal,action,3; AND eligible,valid,legal; MOV eligible; EX old-s; MOV old-s; MOV old-action; EX terminal; MOV terminal; signed EX reward; MOV reward-slot                     | 12    |
| C3 | EX terminal; SELECT TD-shape,terminal,terminal-shape,nonterminal-shape; MOV gate-shape; STAGE TD-gate; paid M; BR ineligible to retire; BR rejected to retire; BR terminal to terminal-body                 | 7     |
| D1 | Old Q base: EX old-s; SHL x,s,1; ADD x,x,s; EX old-action; ADD x,x,action; SHL x,3; ADD x,80; MOV old-base                                                                                                 | 8     |
| D2 | Nonterminal successor base: EX s; SHL x,s,1; ADD x,x,s; SHL x,3; ADD x,80; MOV successor-base                                                                                                             | 6     |
| D3 | Old-Q read: 8 address instructions; successor reads: 24; Q rewrite: 8; all paired with their already paid lane accesses                                                                                  | 40    |
| D4 | MOV r,reward-slot; STAGE old-Q-read; STAGE successor/max; STAGE TD-arithmetic; STAGE Q-rewrite, placed immediately before their respective work                                                              | 5     |
| C4 | After either TD body: BR retire; MOV zero-write-operand,0; sixteen MOV address,884+k, each followed by WRITE2 zero                                                                                        | 18    |
| E1 | Fresh selection base: EX s; SHL x,s,1; ADD x,x,s; SHL x,3; ADD x,80; then 24 address instructions for the three freshly reread Q words                                                                    | 29    |
| E2 | STAGE selection; three MOVs saving paid B/T/X inputs; NE valid-T,T,3; BR packet-error if false; three EX handoffs of ranks when used; MOV selected-action                                                  | 10    |
| F  | MOV a,0; initialize W=0; EX action; EX h from s; GE unique,h,2; AND eligible,unique,public-write-permission; MOV gate-action; MOV gate-eligible; STAGE ACTION; paid M; BR rejected to finish; EQ scrub,action,2; BR scrub | 12    |
| G  | Scrub entry: BR ineligible to finish; EX cue; SHR j,cue,2; SHL x,j,4; SHL j,j,2; ADD base,x,j; MOV base-slot                                                                                                | 7     |
| H  | Twenty cell expansions from the next table, in physical logical order                                                                                                                                   | 220   |
| I  | EX W; NEG return,W; MOV a,return; BR store                                                                                                                                                               | 4     |
| J  | Pack/store: EX s; SHL s,1; OR word,s,1; EX action; SHL action,6; OR word; EX a; AND a,65535; SHL a,8; OR word; EQ terminal,public-tick,last-learning-tick; SHL terminal,24; OR word; MOV packed-record; STAGE store; sixteen MOV address,884+k followed by WRITE2 packed-record | 31    |
| K  | STAGE exit; BR to final S opcode; paid S=8 clears scratch and terminates the operation, with no post-clear micro-PC write                                                                                 | 2     |

D moves reward to R1 before forming bases, then reads Q, computes and rewrites. E saves
ranks before consuming them and rereads Q only after C4. B captures all raw symbols
before candidate comparisons, then releases the base register. B3 copies paid h.

| Cell step | Instruction and effect                                                                                      | CONTROL |
|-----------|-------------------------------------------------------------------------------------------------------------|---------|
| H1        | EX R0,best; execute the six paid generator ALUs into R0                                                      | 1       |
| H2        | MOV expected-slot,R0; EX R1,raw-word,i-field; NE needed,R1,R0; BR not-needed to next cell                      | 4       |
| H3        | EX address,base-slot; ADD address,address,i; STAGE write-gate; pay M=128                                      | 3       |
| H4        | BR rejected to finish; otherwise WRITE2 expected-slot; ADD W,W,1 only after completed write                  | 2       |
| H5        | One MOV of the needed predicate into its retained decoder slot before the gate, on the needed branch       | 1       |

H5 is placed after H2's branch and before H3. Each examined cell uses at most
11 CONTROL instructions, plus g=6 generation, an actually attempted M, and an
actually completed WRITE2. A clean cell uses H1/H2 only (5); a failed needed
write uses 10. The raw word is bits 0..31 for i=0..15 and a separate eight-bit
field for i=16..19. No extraction crosses a 32-bit operand. Repetition uses its
ten-bit raw field, g=1, and address offset 4i instead of i.

Six-step generation is not an extra kernel: AND p,best,column; SHR x,p,2;
XOR p,p,x; SHR x,p,1; XOR p,p,x; AND p,p,1. Its integer result is already the
canonical two-bit encoding 00 or 01. NE therefore covers 10, 11 and the wrong
binary sign in one comparison; there is no additional is-erasure test.

The counted stage sums are A=4, B=64, C=53, D=59, E=39, F+G=19,
H=220, I=4, J=31, K=2: **495**. This deliberately includes all twenty needed
writes although unique decoding may make that combination unreachable. It is
not an exact attainable maximum. There is no established 256 or 375 bound.

## Gates, branches, kernels and liveness

G's METER quote is indexed by public program/substep plus paid scratch arguments.
METER's 128 covers ROM lookup, five reservoir comparisons, accounting and audit;
CONTROL pays selection/staging above. Fixed argument locations are cue/s/action,
address/expected, metadata and micro-PC; MOVs select varying shape/predicate fields
in the five control flags, not another argument buffer. ACTION ignores the scrub
eligibility flag for actions 0/1. No gate reads a host-maintained quote index.
Before offer acquisition use maxima across all encodings, separately per source.
Afterward block base=20(cue SHR 2); repetition base=20(cue SHR 2)+(cue AND 3).
Q base=80+8(3s+action). Cue/state widths and the charged action=3 check prove
addresses 0..79 and 80..847 legal; record addresses are exactly 884..899.
There is no unpriced indirect READ2 using the scorer's cue or an audit address.

At CELL i entry, reserve (n-i)(g+128) plus store/exit and T; after generation,
retain the current possible gate plus (n-i-1)(g+128). A clean BR releases only
the unused current gate bound. A needed gate pays 128 then tests WRITE2's 23
energy/one local material against the remaining obligations and residue.
A failed gate branches directly to finish; it never visits another cell.
Every micro-PC location has a finite ROM remainder entry. Selecting its vector
inside paid METER is not free worker arithmetic. No running reserve, spent total
or durable admission flag is stored. The gate branch consumes its outcome immediately.

W alone is needed for a=-W. B02 permits *at most* V/A/W slots, not three required
worker ledgers; B04's W form is retained. V is recoverable from the unrolled
scratch micro-PC while executing; A and tariff totals are one-way external trace
accounting and never read back. Clean and failed branches have their own ROM
locations. This does not replace acquired traversal state with a protected host PC.

| Path/phase | Bounded treatment or live decoder state                                                                                      |
|------------|------------------------------------------------------------------------------------------------------------------------------|
| Scan       | Kernel's 64 bits + offer 5 + saved base 7 = 76; no sixteen-candidate table                                                      |
| Old load   | Raw 40 + best 4 + s 5 + cue 4 + old record 32 = 85; extracted metadata 9 can coexist briefly: 94                               |
| TD gate    | Raw/best/s/cue 53 + metadata 9 + reward 16 = 78; reward remains until paid gate finishes                                        |
| TD body    | After reward moves to R1: 62 + old/successor bases 22 = 84; lane insertion goes directly into arithmetic Q operands              |
| Selection  | Raw/best/s/cue 53 + ranks 7 = 60; old metadata/bases are dead; three Q words use three arithmetic registers                       |
| Write gate | Raw 40 + best 4 + s 5 + cue 4 + action 2 + a 16 + W 5 + predicates 4 + base 7 + expected 2 = 89; all four arithmetic words free |
| Store      | Snapshot, best, cue, W, base and predicates die first; s/action/a plus packed record use 55 bits, not a second live transition    |
| Rejects    | DECIDE failure: A, duplicated zero operand + sixteen addressed clears, one BR to K (24 slots total); no old read/store/action. Frozen omits clear |
| Old drop   | Invalid/action=3 or unaffordable: still C's TD fee and retirement; skip D. Stored terminal: D=28 rather than 59                    |
| Abstention | Empty/tied/prohibited or rejected ACTION: W=0, no cells, I/J/K; no resource fallback                                             |

Exact decoder offsets during scrub: raw 0..39, best 40..43, s 44..48, cue 49..52,
action 53..54, predicates 55..58, W 59..63, a 64..79, base 80..86, expected 87..88.
Every extracted field fits one 32-bit word. Scan uses candidate 40..43, best
44..47, counters/tie 48..63, offer 64..68, base 69..75; B3/B4 explicitly relocate
best/cue before reuse. Old record uses 64..95; metadata 53..61; extract reward
into a register before releasing the record and storing reward at 64..79. TD bases
reuse 64..85 only after reward enters R1. W's whole-word ADD cannot carry beyond
its five bits (W<=20). Dead-slot release is not a clear; S clears all 256 bits.

TD's 23 and selection's 24 are separately charged, not 45 free CONTROL slots.
The four successor-max ALUs are additional in TD. Its 23-step witness is four
compare/select reward clamps; six shifts/adds/subtracts forming N; arithmetic
SHR N,7 and AND N,127; GT d,64, EQ d,64, AND k,1, AND tie/odd, OR with greater;
ADD rounding increment; ADD old q; four compare/select saturation steps. Floor
quotient/nonnegative remainder implements signed roundEven (-64->0, -192->-2).
R0=q survives; R1=r then quotient, R2=m then rounding predicate, R3=N then
remainder, with one decoder predicate. No fifth arithmetic register is needed.

Selection's literal 21-step sequence (three padded slots) is: two compare/SELECT
max pairs (4); three EQ maximal flags (3); two ADD tie count (2); two SELECT
lowest maximizer (2); two SELECT highest (2); SELECT by B (1); EQ count,2 and
SELECT (2); EQ count,3 and SELECT T (2); EQ X,0 and SELECT T (2); MOV result (1).
E2 separately pays EX B/T/X at their consumption points. After three equalities
the Q words are dead; count/lowest/highest use three registers, and the fourth
receives B then X; T reuses the dead highest register. Scan's inherited per-cell
eleven ALUs already include raw extraction and observation/mismatch predicates.
These are abstract tariff traces, not certification of an arbitrary host lowering.

## Prospective two-page amendment and propagated prices

If retaining this conservative schedule, add **one 256-energy CONTROL page** to
every offered controller's mandatory entry, learning/frozen, RL/fixed, both codes,
including DECIDE rejection. Pay both pages after outer M and before DECIDE; no
extra M, S, material, scalar, persistent state, fault window or operation boundary.
This explicitly changes the B02 single-envelope/entry-price rule and must be a
new additive version before freeze; B02/B04 and prior evidence remain unchanged.

Page A contains A..G and cell 0, followed by one charged jump to page B:
4+64+53+59+39+19+11+1=250. Page B contains cells 1..19 and I/J/K:
19(11)+4+31+2=246. Early exits target page B's appropriate tail directly.
No spare slots transfer between pages or ticks. Total upper bound is 496.

Resource branch instead uses: EX action; SHL request-action,4; EX cue; OR request;
STAGE attempt; paid attempt/request/yield/METER cap-deposit; MOV accepted; EQ
forage; BR forage; SHR accepted,2 or SHL accepted,1; MOV a; BR store. Its 11
CONTROL slots replace G/H/I, far below either page bound. No second yield packet.
Fixed selection uses EX e; EX p; EQ e,0; EQ p,0; trigger (periodic SUB/AND/EQ,
threshold EX h/EQ, or constant false); SELECT scrub/forage; SELECT collect;
SELECT forage; MOV action: at most 11, replacing E's 39. Nonlearning omits C/D/J.
Repetition changes B by -29, G by +2 and H by -165: 303, or 304 with page jump.
DRIVE adds EQ scrub/SELECT 16-or-0/MOV a before ACTION, omits W-to-return, and
replaces resource mapping by zero: page A<=253, page B<=243. It is not a fair arm.

| Quantity/window              | Prospective block | Prospective repetition | Change to material/support offer |
|------------------------------|-------------------|------------------------|----------------------------------|
| Learning controller maximum  | 9573              | 3273                   | None                             |
| Frozen controller maximum    | 8374              | 2074                   | None                             |
| HS-DEVELOP / HS-H2-REFERENCE  | 29394             | 19174                  | Keep g=66, energy 30000          |
| HS-RECOVER                   | 26340             | 16120                  | Keep g=47, energy 30000          |
| HS-ACQUIRE                   | 17559             | 14467                  | Unchanged; no controller         |
| HS-H1                        | 18339             | 14419                  | Unchanged; no controller         |

Learning/frozen routed controller maxima rise by exactly 256; mandatory base
subtotals before routes become 872/776. Only offered ticks incur the increment.
The full-start learning bound including leakage is 29395, below 30000 by 605
(old margin 861). The sensor lower bound becomes 60266, still above every E cut;
local P at that instant remains 255. Source material maxima and the refill
induction are unchanged. Upkeep, RESPONSE, TERMINAL, acquisition and LL-EVAL13
retain their existing conditional bounds and their outstanding trace obligations.
These are financial upper bounds, not realized expenses, functional sufficiency,
scarce-H2 feasibility or performance evidence. All comparison arms pay the same
new controller price; frozen/fixed bodies still omit genuinely unused work.

## Verification and next research

Only this file was written. Scalar checks confirmed 495, 250+246=496 and margin
605; diagnostics reported no errors. Review charged the postscan cue relocation.
No worker/training/simulation ran. CONTROL256 and other service traces remain open.

* [ ] Independently audit the fixed-slot operand ABI, kernel handoffs and literal expansion; require a different count if any transfer expands into extra ALUs.
* [ ] Either produce a genuine <=256 witness or approve/version the priced two-page alternative; do not relabel this 496-slot schedule as conforming to B02.
* [ ] Finish untouched scan/selection, RESPONSE, TERMINAL and 22 upkeep traces and B05-B07 design gates; production trace/ledger tests remain later authorized work.

No clarification is needed. Repricing requires a prospective decision, not implied consent.