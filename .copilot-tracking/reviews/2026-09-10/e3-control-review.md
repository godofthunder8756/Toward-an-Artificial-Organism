---
title: E3 controller trace adversarial review
description: Independent instruction, liveness, branch and two-page pricing review
ms.date: 2026-09-10
status: Complete - accept repaired two-envelope candidate for prospective versioning
---

## Scope and decision

Review the whole .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md
against E3_OPERATION_CONTRACT_v0_3.md and E3_POLICY_CONTRACT_v0_5.md.
Write only this review. No code, simulation, training, contract amendment or
execution authorization is part of this work.

Accept the repaired two-page candidate for prospective versioning, not as
conformance to the unchanged single-envelope contract. The existing arithmetic
495 and 250+246=496 is correct. No increase to 1,024 CONTROL energy is needed.
The repairs below can use the listed instruction slots; none requires an
additional executed CONTROL instruction on the longest path.

The acceptance is specifically for two prepaid 256-instruction execution
budgets, with finite target-independent ROM and the register assignments below.
It is not a claim that all alternative ROM instructions occupy only 256 stored
addresses per page. That stronger interpretation of "256-slot page" is false
for the stated layout and is not a requirement imposed by B02.

Disposition: ten CT findings closed at the paper-review level, zero unresolved
CT findings. The original document needs the exact clarifications below before
it can serve as the versioned witness. Existing CONTROL256 conformance remains
unproved, and implementing or freezing E3 remains blocked by the separately
identified design and service-trace gates. Closing review findings is not
claiming that those other gates passed.

## Questions under review

* Verify 495 instructions and the proposed 250/246 page bounds, including all exits.
* Separate literal instruction defects from valid priced kernel handoffs.
* Check scan relocation, old-record extraction, preservation of old q and four-register TD.
* Accept documented narrow fixed-slot MOV as the abstract primitive; reject hidden partitions.
* Check target-independent unrolling, branch/jump charges, page prepayment and tail invariants.
* Check every selected-action case, the 11-slot resource branch and DRIVE before ACTION.
* Provide exact minimal repairs and accept or reject the two-page versioning candidate.

## Findings and evidence

### CT-001 Arithmetic and the meaning of a conservative bound

Status: Closed, correct with an explicit qualification.

| Group                 | Expansion                   | CONTROL |
|-----------------------|-----------------------------|---------|
| A                     | Entry and DECIDE dispatch   | 4       |
| B                     | 4+5+39+7+9                  | 64      |
| C                     | 16+12+7+18                  | 53      |
| D                     | 8+6+40+5                    | 59      |
| E                     | 29+10                       | 39      |
| F and G               | 12+7                        | 19      |
| H                     | 20 times 11                 | 220     |
| I                     | Return and store dispatch   | 4       |
| J                     | Packing, staging, addresses | 31      |
| K                     | Exit staging and branch     | 2       |
| Unpaged total         | Sum of preceding groups     | 495     |
| Page A                | 238+11+1                    | 250     |
| Page B                | 19 times 11+4+31+2          | 246     |
| Paged total           | 250+246                     | 496     |

The all-needed-cell sum is a conservative path envelope, not a demonstrated
reachable maximum. A unique scan necessarily has some agreeing observations;
twenty erased cells instead give empty decoding and no scrub. No conclusion
that every implementation needs more than 256 follows from this worksheet.
Conversely, the worksheet cannot certify a 256-instruction implementation.

Each clean cell costs five CONTROL instructions. A failed needed write costs
ten, including its failed-gate branch. A completed needed write costs eleven.
H5 belongs before H3's gate. Generation, READ2/WRITE2 and METER are not free
CONTROL slots, and they are not counted a second time here.

Evidence: trace, complete learning block schedule and H1-H5; operation contract,
fixed control services and computational kernels.

### CT-002 Fixed-slot instructions are a legitimate abstract primitive

Status: Closed, accepted rather than subjected to a hardware lowering.

B02 prices at-most-32-bit ALU/register instructions and includes scratch access
in the instruction. The trace explicitly chooses narrow, fixed scratch slots
as register operands. Accept a one-operation MOV between those slots, including
a narrow destination preserving neighboring slots. Replacing every such MOV
with mask/shift/merge operations would review a different machine.

Exact clarification: fixed-slot source reads and writes have their declared
width; packed-record/raw extraction remains an explicit EX. Comparisons and
branches may read named fixed predicate/action slots, not an obsolete arithmetic
register that formerly contained the value. A signed sixteen-bit value promoted
to a 32-bit arithmetic operand uses the explicit signed EX in CT-004. No
40-bit snapshot operation, multi-field packing macro or address-plus-access
instruction is introduced.

The scratch inventory remains decoder 96, arithmetic 128 and control 32 bits.
STAGE writes the existing sixteen-bit micro-PC. It neither allocates a call
stack nor provides additional argument registers. Gate inputs survive in the
declared decoder/control slots, and the gate may clobber all four arithmetic
registers.

One literal correction avoids ambiguity in H4 without changing its count.
With W at decoder bits 59..63, replace an alleged *whole-word* `ADD W,W,1`
by `ADD decoder-word1,decoder-word1,134217728`, where word1 is bits 32..63.
The added constant is $2^{27}$, not one. W is at most 19 immediately before a
completed increment, so it becomes at most 20; lower fields are unchanged and
there is no overflow beyond the word. Alternatively declare W a five-bit
register operand of ADD, in which case the original notation is valid. Do not
mix those two operand meanings. Adding literal one to the packed word would
alter raw bit 32, not W; that is a concrete incorrect lowering.

The whole-word alternative is an unsigned 32-bit packed-word operation, not
signed cost arithmetic. Crossing bit 31 as W advances from 15 to 16 is not
a signed-overflow trap. The narrow-register alternative instead computes the
ordinary integer W+1 directly in its five-bit slot.

### CT-003 Scan relocation has an exact zero-additional-slot repair

Status: Closed by the following operand assignment and order.

The existing text names `best-result`, `health-result` and `cue-slot` without
binding all their source/destination offsets. The repair is to supply that
binding, not to invent new postscan copies or recompute health for free.

| Interval          | Decoder allocation                                                    |
|-------------------|-----------------------------------------------------------------------|
| Scan              | Raw 0..39, candidate 40..43, best 44..47, counters/tie 48..63            |
| Scan inputs       | Offer cue 64..67, usefulness 68, base 69..75                           |
| B3 after scan     | Best copied to 40..43; h copied to 55..56                              |
| B4 after cue copy | Cue 49..52; h 55..56; usefulness still 68                              |
| After B5          | Raw 0..39, best 40..43, s 44..48, cue 49..52; temporary h/u are dead    |

Receive the paid packed offer into R2. Bind B1's first EX to R0=cue from that
packet and its second EX to R1=usefulness from the still-intact R2. Its existing
MOVs save cue/usefulness at 64..67/68. Thus B2's promise that cue remains in R0
is true. Only then reuse R2/R3 for base calculation, with the final base retained
in R3 during raw capture. Scan candidate arithmetic starts only after all raw
reads; the base register is then dead.

At B3's end use its already counted `MOV best-result` to copy scan best
44..47 into 40..43. Use its already counted `MOV health-result` to copy the
paid kernel's two-bit h result into 55..56, after counters/tie are dead.
Do not leave best at 44..47 when s is subsequently stored there.

B4 extracts cue from 64..67 and uses its existing MOV to write 49..52 before
sensing. Derive the sensor hub from that cue and place it in the existing
control argument bits. The sensor kernel may destroy R0..R3, but cannot destroy
h, u or cue. Let its E/P results be R0/R1; the two counted GE operations put
e/p into R2/R3. B5's EX operations load h into R0 and u from bit 68 into R1.
Its shifts/ORs accumulate s in R1; its final MOV writes 44..48. Cue survives
at 49..52. Only then may C1 overwrite 64..95 with the old record.

This ordering prevents all three concrete destructive completions: packing s
over unrelocated best, placing cue over live h, and loading the old record over
usefulness before s is formed. The unqualified original operand names do not
force those mistakes, so they are not evidence that extra instructions or an
extra partition are necessary. The corrected B remains 64.

Evidence: trace, B1-B5 and decoder offsets; policy contract, exact sensor point
and s=16u+8e+4p+h; operation contract, scan and old-load lifetimes.

### CT-004 Old-record extraction and old q survive with four registers

Status: Closed by qualification and ordering, not an extra Q read.

Bind C1's full record to decoder bits 64..95. Interpret its fields relative to
that word: valid at 0, old-s at 1..5, action at 6..7, signed reward at 8..23,
terminal at 24. C2 extracts every needed field before releasing that word.

| Retained field | Decoder bits |
|----------------|--------------|
| Eligible       | 53           |
| Old s          | 54..58       |
| Old action     | 59..60       |
| Terminal       | 61           |
| Signed reward  | 64..79       |

C2's twelve instructions suffice: EX valid; EX action; NE legal; AND eligible;
MOV eligible; EX old-s; MOV old-s; MOV old-action; EX terminal; MOV terminal;
signed EX reward; MOV reward. During these operations R1 can retain old action
until its MOV, and R0 can be reused for valid, old-s, terminal and reward.
Reward extraction precedes the MOV that overwrites part of the old record.

Every C3/D1 reference to terminal, old-s or old-action must name these metadata
slots, not the released record. For example, old-s=31 and reward=0 would yield
old-s=0 if D1 reread the low old-record bits after zero reward was copied over
64..79. That incorrect completion addresses a different Q row; metadata is
the available paid remedy, not a fresh persistent read.

Replace D4's `MOV r,reward-slot` by `signed EX R1,reward-slot`, still one CONTROL
instruction. This explicitly sign-extends the retained sixteen bits. Under a
zero-extending MOV completion, q=m=0 and reward=-1 incorrectly clamp to r=256
and update q to 32 instead of zero. Neither an unsigned promotion nor a
second clipping rule is permitted.

Use this exact TD ordering:

1. Execute the reward handoff into R1 after METER, before reusing reward slots.
2. Form old base with D1 and, on the nonterminal path, successor base with D2.
	Save old base at 64..74 and successor base at 75..85. Base arithmetic uses
	R0/R2/R3 while R1 remains reward. No old q is loaded yet.
3. Stage/read old Q into R0. For the successor maximum read the first Q into
	R2, the second into R3, compare/select into R2, then read the third into
	R3 and compare/select into R2. The two predicates use one dead decoder
	predicate bit. The four maximum ALUs are the separately priced kernel.
4. R0=q, R1=r and R2=m enter the 23-step TD kernel. R0 survives until the
	kernel's final q-plus-increment, then holds q'. Rewrite from R0 using the
	retained old base. No gate intervenes between these Q loads and rewrite.

The original prose already says reward precedes bases and bases precede Q.
It is therefore incorrect to report an inevitable old-q clobber merely from
reading the D rows in numerical order as contiguous executable blocks. The
handoff ordering above makes that existing interpretation explicit.

Terminal D uses old-base 8, old-read addresses 8, rewrite addresses 8, and four
handoffs/stages: 28 CONTROL instructions. The paid terminal kernel supplies
R2=0 with its existing one ALU. It performs no successor-base formation, read
or maximum. Invalid/action=3 and rejected TD perform neither D body.

### CT-005 TD and selection kernel interfaces do not hide CONTROL work

Status: Closed for the claimed arithmetic and interfaces.

An explicit 23-step TD register witness is available without a fifth register.
Here p is one decoder predicate, not a new arithmetic word:

| Steps | Operation sequence                                                               |
|-------|----------------------------------------------------------------------------------|
| 1..4  | Compare/select lower reward clamp, then compare/select upper reward clamp in R1    |
| 5..10 | SHL R3,R1,4; SHL R1,R2,4; SUB R1,R1,R2; ADD R3,R3,R1; SHL R1,R0,4; SUB R3,R3,R1   |
| 11..12| Arithmetic SHR R1,R3,7; AND R3,R3,127                                              |
| 13..17| GT R2,R3,64; EQ p,R3,64; AND R3,R1,1; AND R3,R3,p; OR R2,R2,R3                     |
| 18..19| ADD R1,R1,R2; ADD R0,R0,R1                                                        |
| 20..23| Compare/select lower saturation, then compare/select upper saturation of R0        |

For negative N, arithmetic shift gives a floor quotient and AND gives its
nonnegative remainder. The same greater-than-half/tie-and-odd rule implements
nearest-even: -64 gives quotient -1/remainder 64 and rounds to zero; -192
gives -2/64 and stays -2. This realizes the policy contract's signed rule;
its absolute-value definition does not require a separate absolute-value
implementation. Saturation occurs after q is added, using signed 32 bits.

Selection can use its stated 21 ALUs plus three charged padding slots.
After the maximum, place the three equality flags in decoder predicate bits
55..57, so the old Q arithmetic words are dead. Use R0=count, R1=lowest,
R2=highest, R3=B. Put the B-selected candidate in R3, retaining lowest in R1
until the count-two SELECT. Highest is then dead; E2's existing EX T can load
R2. E2's EX X uses R3. The count-three and explore SELECTs use the same T.
The paid result assignment can return through R0 and E2's counted MOV stores
action at 53..54.

Save B/T/X in seven decoder bits 64..70, using E2's three counted MOVs.
Receiving each scalar uses the separately charged I/O operation and a reusable
arithmetic input register, before the selection Q words fill R0..R2. Check
T!=3 while the received T is available, before later reuse; retain no extra
random packet or host draw cursor. The three
consumption EXs are E2's existing handoffs. E1's 24 lane addresses are additional
to the Q kernels, and the selection row is reread after old-record retirement.

No omitted control instruction is assigned to TD's 23 or selection's three
padding slots. The complete block/repetition scan implementation and other
service traces remain separate obligations; this review does not certify an
arbitrary lowering of their normative priced kernels.

### CT-006 Selected actions and exact return ownership

Status: Closed, with the following explicit branch and register binding.

F's twelve instructions initialize a and W, acquire the selected action and
the health field of s, form write eligibility, stage ACTION and pay its one
METER fee before either the rejection branch or the scrub/resource dispatch.
Health/prohibition never waives that fee. Invalid old action=3 is handled in C;
it does not become a current action. Current selection returns only 0, 1 or 2
from the protected rule and valid packets, so F needs no additional action=3
repair or unpriced fallback branch.

| Selected case                   | Body and exact main return                                       |
|---------------------------------|------------------------------------------------------------------|
| ACTION rejects                  | No request/yield/cells; a=0; retain selected action for store       |
| Forage admitted                 | One attempt and yield; a=floor(accepted F/4), including truncation |
| Collect admitted                | One attempt and yield; a=2 times accepted C                       |
| Scrub h=0/1 or writes prohibited | Paid ACTION, no cells, W=0 and a=0                                |
| Unique scrub entry rejects      | No cells, W=0 and a=0                                             |
| Clean unique scrub              | Examine all n cells, pay every g, no WRITE2, a=0                  |
| Needed write rejects            | Pay that METER; stop at once; return minus prior completed W      |
| Needed writes complete          | Increment W only after each WRITE2; a=-W                          |
| DECIDE rejects                  | No selected action, no current store; learning old clear then S   |

Make the resource eleven-instruction sequence literal as follows:

| Step | Instruction or already priced substep                                       |
|------|----------------------------------------------------------------------------|
| 1    | EX R0,selected-action                                                      |
| 2    | SHL R0,R0,4                                                                |
| 3    | EX R1,cue                                                                  |
| 4    | OR R0,R0,R1, forming the six-bit request                                   |
| 5    | STAGE attempt                                                              |
| Paid | Attempt 16, request/yield I/O, and the already paid METER's cap/deposit work  |
| 6    | MOV R2,accepted-result                                                     |
| 7    | EQ predicate,selected-action,0, reading the retained fixed action slot       |
| 8    | BR predicate to forage-tail                                                |
| 9    | Collection tail: SHL R2,R2,1; forage tail: SHR R2,R2,2                      |
| 10   | Each tail has its own MOV a,R2                                             |
| 11   | Each tail has its own BR to page-B store                                   |

The two tails duplicate steps 9..11 in ROM; they do not need an uncounted join
jump. There are fourteen stored CONTROL instructions but eleven executed on
either resource branch. R2 is the accepted amount, not the raw incoming offer.
Step 7 reads the saved action, not an arithmetic value presumed to survive
METER. a occupies 64..79 and cue/action remain 49..52/53..54.

There is no new METER fee between steps 5 and 6. This is the existing ACTION
METER's admitted cap/deposit work. It may return the bounded accepted amount
in an arithmetic register under its declared interface. All attempt, I/O and
transport charges precede deposit; no additional gate or S occurs before the
return mapping consumes it. The amount then dies. This is neither a ninth
scalar nor a queue, escrow, future callback or reusable success notification.

For DRIVE, use the three counted instructions after F's action extraction and
before ACTION METER: EQ action,2; SELECT return,16,0; MOV a,return. Preserve a
through the gate and the prefix. Omit only I's EX W, NEG and MOV a, retaining
its BR to store. For resource actions a is already zero; do not substitute
the main accepted-income return. Thus selected scrub earns 16 even on gate
rejection, no unique decode, prohibition or zero completed writes, exactly as
the diagnostic specifies. Rejected DECIDE still creates no current record.

J's fifteen pre-access instructions and sixteen address MOVs total 31. Bind
its packed current word to decoder 0..31 after raw/best/cue/W are dead. It
contains valid=1, s, selected action, a masked to sixteen bits, the public
last-learning-tick bit and zero reserved bits. The previous persistent record
has already been retired. No second live transition survives the operation.

### CT-007 Branch targets and per-page executed bounds

Status: Closed by the following literal control-flow layout.

Use page A for entry, observation, old TD/clear, selection, ACTION, resource
branches, scrub setup and cell zero. Put cells 1..19, main I, J and K on page B.
The same sixteen-bit scratch micro-PC addresses both; there is no second page
index, call stack or protected acquired program counter.

* A's rejected-DECIDE branch targets a learning rejection block on page A:
	MOV zero operand, sixteen address MOV/WRITE2 pairs, then one BR to K on
	page B. It skips observation, TD, selection, ACTION and current store.
	The frozen variant branches directly to K instead.
* C3 pays TD METER before its ineligible/rejected/terminal branches. Both
	rejected-update branches target the first clearing instruction of C4.
	Each admitted D body has a charged BR to that same retirement entry.
	There is no fallthrough from terminal D into nonterminal D or a second clear.
* F's rejection branch and G's ineligible branch target I on page B in the
	main objective, or the retained I branch in DRIVE. F's successful scrub
	branch jumps over the resource alternative to G; the resource alternative
	falls through from the other F outcome and has its own BR to J.
* H0's clean branch targets the one-instruction page-B transfer stub. A
	completed H0 falls through to that stub. The stub performs the counted
	jump to H1 on page B. A rejected needed H0 gate branches straight to I;
	it does not also execute the normal transfer.
* On page B a clean-cell branch targets the next cell, or I for cell 19.
	A completed write falls through to that target. A failed needed-write
	branch targets I immediately. No next-cell increment or implicit loop
	branch is required because these are literal, unrolled instructions.
* I has its counted BR to J. In nonlearning variants J is absent and this
	branch targets K. K's STAGE and BR reach the final paid S. S clears all
	256 bits and terminates atomically; it performs no later micro-PC write.

Every cross-page BR above is itself the charged transfer. Do not add a free
transfer after it, and do not charge an additional jump unless that jump is
actually an instruction. Sequential fallthrough is already in the chosen
instruction semantics. The main H0 continuation uses the extra jump counted
in 496; early exits are not obliged to visit that continuation.

| Variant or path                          | Page A bound | Page B bound | Explanation                          |
|------------------------------------------|--------------|--------------|--------------------------------------|
| Learning RL block scrub, nonterminal TD   | 250          | 246          | Conservative longest envelope        |
| Learning block scrub, stored-terminal TD  | 219          | 246          | Replace D=59 by D=28                  |
| Learning DECIDE rejection                 | 22           | 2            | A4 + zero1 + address16 + BR1, then K  |
| Frozen DECIDE rejection                   | 4            | 2            | Rejected DECIDE BR targets K          |
| Learning resource action                  | 242          | 33           | Replace G/H/I by resource 11          |
| Learning DRIVE block scrub                | 253          | 243          | Add 3 before gate; remove 3 from I    |
| Frozen RL block scrub                     | 138          | 215          | Omit C/D and J                       |
| Fixed nonlearning block scrub             | 110          | 215          | Also replace E39 with rule <=11      |
| Learning RL repetition scrub              | 223          | 81           | B-29, G+2, four remaining cells       |
| Learning DRIVE repetition scrub           | 226          | 78           | Same DRIVE substitution              |

Drop/invalid TD and early action/cell failures only shorten these envelopes.
An earlier page-A exit cannot increase page-B beyond its complete suffix.
No page path needs more than 256 executed CONTROL instructions. DRIVE is the
tightest page A, leaving three slots; the main page B leaves ten. No spare
budget is transferred across pages, operations or ticks.

Repetition's B delta has a concrete expansion: its scan administration is
STAGE plus five literal address ADDs plus two result MOVs, eight rather than
39; add two operations for `(cue AND 3)` and addition to `20*(cue SHR 2)`.
That is -31+2=-29. Each literal cell offset is 4i, not a new runtime multiply.
G needs the same two additional base operations. Five cells instead of twenty
remove 165 CONTROL instructions, so 495-29+2-165=303, or 304 with the jump.

The fixed periodic rule's bound is EX e, EX p, EQ e,0, EQ p,0, SUB/AND/EQ
for the public period, and three priority SELECTs plus MOV action: eleven.
Threshold substitutes EX h/EQ, reducing that bound by one. Energy priority
is last in the SELECT chain and therefore wins when both resource bins are low.

### CT-008 ROM capacity is not the executed-instruction allowance

Status: Closed with a necessary naming correction and a concrete counterexample.

Replace "pair of 256-slot control pages can accommodate the stated schedule"
with "pair of prepaid 256-instruction CONTROL execution envelopes over finite
target-independent ROM; page names identify execution budgets, not ROM storage
capacities." This follows B02's at-most-256 bounded executed instructions, but
must be explicit in the new version. Immutable ROM is not acquired scratch.

If "page" instead means at most 256 physically stored CONTROL instructions,
the document's page-A claim is false, not merely uncertain. Its main path
already accounts for 250 sites. The necessary learning DECIDE-rejection clear
block has eighteen additional sites (zero MOV, sixteen address MOVs, BR K),
which are not on that main path. That alone gives 268>256. The resource branch
and duplicated terminal body make the discrepancy larger. This counterexample
invalidates the storage-page interpretation, not the executed-path bounds.

A fully literal, conservative layout of the CONTROL sites can be budgeted
without sharing any of those alternative blocks:

| Stored CONTROL sites per public program variant | Page-A region | Page-B region |
|------------------------------------------------|---------------|---------------|
| Main block learning scrub path                  | 250           | 246           |
| Separate terminal D and its BR to retirement     | 29            | 0             |
| Separate rejected-DECIDE clear and BR K          | 18            | 0             |
| Resource dispatch and duplicated mapping tails  | 14            | 0             |
| Packet-contract-error terminal trap             | 1             | 0             |
| Main variant ROM bound                          | 312           | 246           |
| DRIVE variant ROM bound                         | 315           | 243           |

Each variant has at most 558 CONTROL instruction sites. Kernel, lane, scalar,
METER and S sites remain separately typed and priced, not CONTROL padding or
unpaid worker helpers. These CONTROL labels fit the existing sixteen-bit
micro-PC without another state field. Public representation/phase/policy
selects a variant; acquired conditions select charged branches within it.
The full linked ROM must retain sixteen-bit addresses, including its already
priced primitive/kernel sites. Nothing requires encoding the sixteen generic
candidate computations as target-specific answers or a learned lookup table.

The T=3 trap is an external packet-contract violation, not a fourth action or
normal retry path. It is not included among successful-service bounds; the
listed T validity check and BR are. No malformed input is repaired through
free acquisition or another random draw.

Under an additional hard 256-stored-sites-per-page requirement, reject this
layout and mark that trace blocked; this review does not claim a repaired
storage-constrained layout. Under the stated B02 executed-instruction cap,
the concrete 250/246 and 253/243 envelopes pass. No 1,024-energy allowance
or enlarged acquired-memory budget is needed in either interpretation.

### CT-009 Fees, mandatory tails and prefix releases

Status: Closed for the prospective two-envelope payment rule.

Pay outer M, page-A C=256 and page-B C=256, in that order, before executing
entry CONTROL or DECIDE M. The minimum check and every enclosing public T
must include both C fees, the DECIDE fee, mandatory old clear when learning,
single S, other scheduled obligations and one energy of residue. Pay both
even when DECIDE rejects or only page A would otherwise be used. This changes
the single-envelope contract prospectively; it does not reinterpret prior
one-page executions as prepaid two-page operations.

Once both C fees execute, exclude them from later L as already paid. Do not
debit instructions individually on top of the fixed C prices. Debit S only
on actual exit, not on page transfer or before ACTION/TD/per-cell fees. Before
METER at a needed cell, retain the current gate fee, every unexamined cell's
generation/gate bound, store, exit, T and residue. Pay METER before testing
WRITE2 against the remaining obligations. The predicate and micro-PC identify
the current branch; METER performs the priced ROM quote selection.

The current attempted gate is no longer in L after its fee is paid. A clean
cell releases its unused gate bound through its charged branch. A failed
needed gate releases the unvisited suffix through its charged exit branch,
but still reaches return/store/S. Completed writes retain all later mandatory
obligations. These releases are reductions of bounds, not refunds or resource
deposits. No controller-visible reserve total, gate-count ledger, admitted
flag or running microcode-fuel counter is stored.

Use decoder predicate bits for eligibility/needed flags and the existing five
control flags for transient arguments/outcome; consume the admission outcome
immediately. Public ROM plus acquired scratch micro-PC provides finite local
remainders. A one-way audit may count V/A and page work externally, but those
counts are not read back. W alone is retained for the selected main return.

Bind ACTION's control flags concretely: action in flag bits 0..1, eligible
in bit 2, gate outcome in bit 3, and bit 4 temporary. F's existing two MOVs
write the action/eligible inputs. METER preserves those input bits, writes
its outcome bit and may clobber R0..R3; F consumes the outcome, and G consumes
eligibility without an omitted reload. Sensor source and TD shape reuse dead
control-flag inputs in earlier stages. A needed-cell predicate occupies decoder
bit 55 after the action dispatch; expected is 87..88 and address remains the
eleven-bit control address. No gate needs a sixth control flag or an extra
argument partition.

The old-record terminal branch is not the scheduled outer TERMINAL service.
It skips only the successor work and uses its charged 97 kernel. The later
scheduled TERMINAL retains its own existing fee, reads, optional TD, clear and
S in T. No controller branch waives it from apparent validity or past success.

### CT-010 Propagated prices and limits of closure

Status: Closed, scalar prices verified and unchanged by the repairs.

All supported controller variants pay exactly 256 more than B02's original
controller. The original 256 becomes two separately bounded 256 envelopes,
512 total, not 1,024. No extra M, S, material, packet, operation boundary or
fault window is introduced. The repairs above preserve the counts, so none
adds another tariff increment.

| Quantity                         | Block | Repetition |
|----------------------------------|-------|------------|
| Learning controller maximum      | 9573  | 3273       |
| Frozen controller maximum        | 8374  | 2074       |
| HS-DEVELOP / HS-H2-REFERENCE      | 29394 | 19174      |
| HS-RECOVER                       | 26340 | 16120      |
| HS-ACQUIRE, unchanged            | 17559 | 14467      |
| HS-H1, unchanged                 | 18339 | 14419      |

Unrouted learning/frozen mandatory bases become 872/776. The full learning
tick plus one final leakage is 29395, leaving 605 against the fixed 30000
grant. The full-start post-sensor E lower bound is
65535-441-768-1-4039-20=60266. Local P remains 255 at that point. All grid
cuts remain high. Per-source material and the support refill induction are
unchanged; neither fee is a material write. Offered ticks, not all phase
ticks regardless of controller presence, receive the increment.

These numbers are conditional financial upper bounds, not measured spending,
successful reconstruction, survival after arbitrary injuries, useful/obsolete
scarcity or a fair DRIVE advantage. They inherit the outstanding scan and
other service-trace conditions in B02/B03, including AGE/CONDITION, RESPONSE
and scheduled TERMINAL. No scientific endpoint or final sample gate changes.

## Disposition and remaining work

| Finding | Paper-review disposition                                                |
|---------|-------------------------------------------------------------------------|
| CT-001  | Closed: 495, 250/246 and 496 arithmetic correct                           |
| CT-002  | Closed: abstract fixed-slot ABI accepted; exact W operand supplied       |
| CT-003  | Closed: h/u/cue/best offsets and postscan ordering supplied              |
| CT-004  | Closed: old metadata, signed reward handoff and old-q lifetime supplied  |
| CT-005  | Closed: 23-step TD and 21+3 selection handoffs fit existing registers     |
| CT-006  | Closed: all action cases, resource eleven steps and DRIVE mapping        |
| CT-007  | Closed: explicit branches/exits fit each 256 executed-instruction cap    |
| CT-008  | Closed: finite ROM sites disclosed; hard storage-page reading rejected  |
| CT-009  | Closed: both C fees precede control; gates, releases and S remain paid    |
| CT-010  | Closed: one additional C propagates to the stated financial bounds       |

Minimal repair set for the next artifact/version:

1. Apply CT-002 through CT-005's exact operand/offset bindings, signed reward
	handoff and TD/selection order. Replace the ambiguous whole-word W increment
	by the stated single instruction. Do not add hardware-lowering ALUs.
2. Apply CT-006/CT-007's duplicated resource tails, rejection clear, terminal
	return and literal cross-page targets. Distinguish terminal D from the
	independent scheduled TERMINAL. Bind J's packed word to released raw slots.
3. Rename the two pages as executed-instruction envelopes and disclose the
	finite ROM accounting in CT-008. Keep the longest executed bounds 250/246
	for main and 253/243 for DRIVE. Static alternative code is not free executed
	control, but neither is its existence extra energy under B02's tariff.
4. Prospectively version the one-to-two-C rule and propagated prices exactly
	as CT-009/CT-010. Preserve all old contracts, experiment gates and evidence.

Net additional executed instructions on the longest path: zero. Revised
conservative totals remain 495 without the explicit page transfer and 496
with it; branch-specific alternatives have the counted costs above. Additional
ROM sites are disclosed, not hidden in scratch or kernel padding.

The candidate is accepted with these exact paper repairs for the next additive
version. The unqualified existing "256-slot pages" wording is not accepted as
a physical-ROM-capacity proof. A current-contract runnable controller is still
blocked: B02/B04 authorize only one envelope, no <=256 controller witness has
been supplied, and the independent service/implementation gates remain open.
This is a definite scope boundary, not a request to keep researching until a
passing empirical result or to seek another routine approval.

## Verification performed

Read the entire target trace and both requested contracts. Consulted the state
layout, physical routed-price/support derivations and the prior B04 review for
the specific inherited interfaces. Used only literal instruction reasoning
and read-only scalar arithmetic checks. No E3 source, simulation, training,
target enumeration, data analysis, kernel execution or scientific result was
produced. Only this review artifact was written.

## Recommended next work not completed

* [ ] Incorporate the exact repairs and two-envelope tariff into the next
  additive design version; do not edit or relabel the original contracts.
* [ ] Complete the separately outstanding scan, RESPONSE, TERMINAL and twenty-two
  upkeep traces and the B05-B07 design gates. Do not expand this controller
  review into those independent investigations.
* [ ] After the design gates, validate implementation-level instruction counts,
  scratch lifetime, paid failure prefixes, signed arithmetic and reset ownership
  before any engineering or final execution.

No further research is required to answer the controller-review questions.

## Clarifying questions

None. The exact interpretation and repair needed for versioning are supplied;
no renewed routine approval is needed to finish this bounded research handoff.

## References

* .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md
* E3_OPERATION_CONTRACT_v0_3.md
* E3_POLICY_CONTRACT_v0_5.md
* E3_STATE_CONTRACT_v0_2.md, finite live state and previous-transition layout
* E3_PHYSICAL_CONTRACT_v0_4.md, reservoirs/routes and HS-AC derivations
* .copilot-tracking/research/subagents/2026-09-10/e3-b04-policy-research.md
* .copilot-tracking/reviews/2026-09-10/e3-b04-review.md, existing operational blockers