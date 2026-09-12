---
title: E3 instruction-core implementation research
description: Verified APIs and frozen instruction requirements for the next engineering foundation
ms.date: 2026-09-10
status: Complete - research only; executable implementation not performed
---

## Scope and questions

* Identify the actual State, Scratch, meter, protocol, and physical APIs.
* Extract instruction semantics and pricing from CONTROL v0.6, CT repairs,
  exact service traces, and ROM closure's primitive ABI.
* Recommend a bounded engineering-only instruction component without inventing
  full-service gates, hidden acquired state, or unearned conformance claims.
* Identify executable witnesses and validation commands for the implementing agent.

## Verified API findings

* e3/state.py stores persistent state in one private 276-byte buffer and scratch
  in a separate private 32-byte buffer. Both classes have only one instance slot.
* Scratch partitions are decoder 0..95, R0..R3 at 96/128/160/192, PC at 224..239,
  address at 240..250, and flags at 251..255. Field widths are 1..32 bits.
* State.read_lane/write_lane reject reservoirs and reserve. Scratch.write_bits
  preserves neighbors and rejects out-of-range values rather than wrapping.
* e3/meter.py debit checks current packed stocks, mandatory remainders, and a
  positive live residue before mutation. It is not a gate or prepayment receipt.
* e3/physical.py lane_read_cost is 3+7d (17 code, 10 auxiliary); write_quote
  includes 6+8d+m energy and one material from the actual owning source.
* e3/protocol.py provides immutable public configuration and structural codecs,
  not a live transport, service executor, admission proof, or isolation boundary.

## Contract findings

### Authority and scope

E3_DESIGN_FREEZE_v0_11.json identifies an engineering-only design snapshot,
forbids final target draws and confirmatory H2, and names the following frozen
sources. Earlier statements that design freeze itself is still blocked in
historical research notes do not supersede this later snapshot. Source hashes
were not recomputed in this session.

* E3_CONTROL_CONTRACT_v0_6.md takes precedence over CT repairs, then the
  incorporated control trace, then otherwise unchanged inherited contracts.
* .copilot-tracking/reviews/2026-09-10/e3-control-review.md supplies CT-001
  through CT-010, including exact TD, selection, W, branch, and scratch repairs.
* .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md supplies
  actual scan, RESPONSE, scheduled TERMINAL, AGE, and CONDITION expansions.
* .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md supplies
  the remaining services, elemental ABI, and shared instruction address space.

### Operand and PC ABI

* Every MOV, EX, shift, Boolean operation, comparison, SELECT, ADD/SUB/NEG,
  branch, and STAGE is a separate instruction. No decoder, popcount, table
  search, fused address/access, host callable, runtime macro, call, or return.
* Fixed narrow slots are legitimate abstract operands. A destination write
  preserves neighboring scratch bits. Packed raw/record extraction is EX,
  not a host unpack or a concealed multi-field MOV.
* A signed sixteen-bit reward/Q promotion is explicitly signed EX. A MOV does
  not silently provide sign extension. Arithmetic right shift must interpret
  the current word as two's complement before shifting.
* Decoder raw capture is a 32-bit low word and separate eight-bit high field,
  never a 40-bit operand. Widths must be positive and no greater than 32.
* PC occupies scratch bits 224..239, not a saved host index. Sequential advance
  is intrinsic. STAGE and entry MOV use literal forward targets; entry targets
  the following work site, not itself. Branch targets are occupied ROM sites.
* Final S costs eight, zeros all 256 scratch bits including PC, and terminates
  the invocation. No subsequent advance, return-PC restoration, callback, or
  implicit restart at zero is allowed. Return HALT as an ephemeral scheduler
  result; do not add a persistent halted field.
* The next public service begins independently. Host iteration can enforce a
  technical execution ceiling, but cannot retain an acquired continuation,
  quote index, policy counter, or budget ledger outside State/Scratch.

CT-002 permits W as a narrow five-bit ADD destination. Its selected whole-word
alternative is ADD D[32:32],D[32:32],134217728. W is D[59:5], so this adds
2^27, not one. For W<=19, the result is <=20, preserves all lower fields,
and does not overflow unsigned 32 bits. Crossing bit 31 is not signed cost
overflow. Overflow semantics for general synthetic instructions must be named
by the new component rather than inferred from Python's unlimited integers.

### Access semantics and physical pricing

* READ2 costs 17 energy for code, 10 for auxiliary RAM. That already includes
  route lookup, reply transport, and insertion. Address MOV/ADD/EX is separate.
* WRITE2 costs 23 energy for code, 14 for auxiliary RAM, plus one material
  from the actual assigned source. Same-value writes pay the same price.
* Capture READ2 can write the designated two-bit R0 reply subslot and its
  designated D insertion slot in the bundled access. Comparisons subsequently
  read that narrow reply, not stale upper R0 bits.
* Q reads assemble eight explicit two-bit insertions in the chosen R word,
  followed by one separately executed signed EX of its low sixteen bits.
* WRITE2 extracts the declared source two-bit field without destroying its
  other bits. Signed Q values must first have a canonical low-bit encoding;
  never pass a negative full Q value to State.write_lane.
* A persistent masked-bit change is READ2, explicit Boolean merge, WRITE2.
  Scratch's neighbor-preserving narrow-write exception does not make RAM
  read/modify/write free.
* Legal ordinary RAM is lanes 0..899 and 924..971. Reservoir lanes 900..923,
  reserve 972..1103, and out-of-range lane encodings must be rejected.
* Use physical.lane_read_cost/write_quote for actual access quotes, then
  meter.debit BEFORE State.read_lane/write_lane. Never use read_bits or
  snapshots as a worker shortcut for memory-dependent operands.

### CONTROL and admission boundary

CONTROL is not an instruction-by-instruction energy tariff in a complete
service. A controller pays outer M128, C_A256, C_B256, then entry CONTROL and
DECIDE M128. Every executed CONTROL instruction consumes its region's static
allowance but is not debited again. Both Cs are paid even on rejection.
Kernels, accesses, scalars, and S are separately charged.

The controller's bounds are A250/B246 for the main block path and A253/B243
for DRIVE. These are execution allowances, not 256-address storage banks.
Main CONTROL alternatives need up to 558 stored sites. The selected shared
image has demand <=26401 and reserved capacity 27936; addresses 0..65534 are
available, 65535 unused. No acquired bank selector is justified.

meter.GateResult is explicitly not a reusable admission/prepayment receipt.
meter.debit checks present affordability but does not establish a prior
CONTROL payment, packet ownership, legal service, local suffix, or public tail.
protocol.BeginFrame and PublicConfiguration similarly prove no live gate.
Accepting any of these as proof of prepaid zero-cost CONTROL would be wrong.

For a future complete service, every debit needs c+L+T+one energy, sourcewise.
G and paid scratch/PC arguments choose finite local remainders. Before paid
address discovery, use sourcewise maxima across all allowed encodings, not a
RAM peek. A failed needed-write gate exits immediately; releases are bounds,
not refunds. No BudgetCounter or shadow reservoir may be introduced.

### Actual instruction witnesses

The 23 TD operations in CT-005 use R0=q, R1=sign-extended reward, R2=m,
R3 temporary, and one D predicate p. They must execute as instructions, not
as a call to e3/arithmetic.py followed by a fabricated 23-count trace.

| Steps | Literal operations |
|-------|--------------------|
| 1..4 | LT p,R1,-256; SELECT R1,p,-256,R1; GT p,R1,256; SELECT R1,p,256,R1 |
| 5..10 | SHL R3,R1,4; SHL R1,R2,4; SUB R1,R1,R2; ADD R3,R3,R1; SHL R1,R0,4; SUB R3,R3,R1 |
| 11..12 | Arithmetic SHR R1,R3,7; AND R3,R3,127 |
| 13..17 | GT R2,R3,64; EQ p,R3,64; AND R3,R1,1; AND R3,R3,p; OR R2,R2,R3 |
| 18..19 | ADD R1,R1,R2; ADD R0,R0,R1 |
| 20..23 | LT p,R0,-32768; SELECT R0,p,-32768,R0; GT p,R0,32767; SELECT R0,p,32767,R0 |

R0 must survive through step 18. Negative numerator -64 gives floor quotient
-1/remainder64 and rounds to zero; -192 gives -2/64 and stays -2. For valid
signed-16 inputs the numerator is in [-1019888,1019889], so signed-32
intermediates suffice. Terminal adds its separately paid R2=0 assignment.

Selection has 21 actual ALUs and three paid unused slots. After the four
maximum ALUs, store equality bits p0/p1/p2 in D55..57. The remaining sequence
can use the following bindings without a fifth register:

1. GT R3,R0,R1; SELECT R3,R3,R0,R1; GT p0,R3,R2;
   SELECT R3,p0,R3,R2 (four maximum operations).
2. EQ p0,R0,R3; EQ p1,R1,R3; EQ p2,R2,R3 (three equality operations).
3. ADD R0,p0,p1; ADD R0,R0,p2 (count).
4. SELECT R1,p1,1,2; SELECT R1,p0,0,R1 (lowest).
5. SELECT R2,p1,1,0; SELECT R2,p2,2,R2 (highest).
6. At this point execute the separately counted CONTROL EX B into R3.
   SELECT R3,R3,R2,R1; EQ p0,R0,2; SELECT R1,p0,R3,R1.
7. Separately counted CONTROL EX T into now-dead highest R2.
   EQ p0,R0,3; SELECT R1,p0,R2,R1.
8. Separately counted CONTROL EX X into R3.
   EQ p0,R3,0; SELECT R1,p0,R2,R1; MOV R0,R1.

B/T/X are saved at D64, D65..66, D67..70 before Q fill; T=3 is a packet
contract error, not a new action or retry. Padding must be explicit in the
pricing/trace model, not secretly used for handoff instructions.

Other exact kernel checks available to the implementing agent:

* Block scan: 3699 ALUs plus 20 routed READ2 =4039; B3 administration is
  39 CONTROL, including every address and candidate MOV.
* Repetition scan: 34 ALUs plus five routed READ2 =119; administration is
  eight CONTROL, excluding its two additional base-calculation ALUs.
* One AGE word: eight kernel ALUs; ADD occurs in a wide register before
  saturation at fifteen and narrow result storage.
* Scheduled terminal TD: eight Q reads, one signed EX, one zero assignment,
  23 TD ALUs, eight writes =217 routed, in addition to CONTROL and envelopes.

## Implementation recommendation

No executable implementation was performed. Active Researcher Subagent mode
requires research and a handoff, rather than editing the requested Python files.
The user's requested production/test paths remain uncreated by this session.

For the implementing agent, choose the user's explicitly allowed minimal
instruction-step foundation before a full-service compiler:

* Frozen, slotted Operand describing only a D/R/control partition, fixed
  offset, and width; strict built-in integer validation rejects bool, float,
  numeric subclasses, out-of-partition ranges, and widths outside 1..32.
* Frozen Instruction with a closed Opcode enumeration and typed fields.
  Immediates must fit a declared signed or unsigned <=32-bit interpretation.
  Do not permit callbacks, executable strings, mappings, target objects, or
  arbitrary Python operators in instruction fields.
* Immutable Program tuple, static literal branch targets, and full-program
  validation before any scratch/resource mutation. Reject writes that could
  create dynamic PC targets; reserve explicit literal PC MOV/STAGE/BR paths.
* Define unsigned arithmetic modulo its declared width separately from checked
  signed arithmetic. Explicit signed EX and arithmetic SHR must use integer
  two's-complement conversion, never float. Test chosen overflow behavior;
  do not silently wrap checked costs or hide a widened acquired register.
* An ephemeral StepResult can identify HALT and an observer effect. It must not
  be consumed as future worker input, a prepayment token, or persistent state.
  The authoritative execution PC is always read from Scratch.
* No instance runtime fields beyond immutable G and explicit State/Scratch.
  Returned traces may record executed PCs/opcodes/costs for the observer only;
  neither policy nor a later step may read trace counts or values back.

Do not expose zero-debit CONTROL by taking a caller's boolean or GateResult
asserting payment. Either keep the first core semantic/effect-only and make no
paid-service claim, or separately implement an explicitly engineering-only
fragment wrapper that actually prepays each statically verified CONTROL region.
The wrapper must state that it lacks outer METER, L/T service gates, scalar
ownership, and full B02 conformance. Arbitrary fragments charged one energy
per CONTROL are not controller tariff witnesses.

If a fragment wrapper is selected, require immutable acyclic programs and
prove max executed CONTROL<=256 per region by static path analysis, including
both outcomes and transfers. A static bound is not a new worker counter.
Charge each kernel instruction/access/S on actual execution. Include actual
CONTROL-envelope debits in the returned observer ledger. Do not invent a
METER opcode without its specified gate shape and G-derived remainder logic.

Generic program provenance remains a trusted construction obligation: a tuple
can be immutable yet contain target-specific constants. Shape validation alone
does not prove target independence or an adversarial capability boundary.

### Required implementation tests

* Immutability, opcode arity, strict integers, partition ranges, all widths,
  immediate ranges, malformed unreachable instructions, and invalid targets
* Generic ALU instructions on constructed fixtures; narrow MOV/ADD neighbor
  preservation; W=15 to16 and19 to20; unsigned wrap and signed overflow cases
* Signed EX of 0xffff to -1 versus zero-extending MOV; arithmetic versus
  logical SHR; -64/-192 ties; extreme signed-16 TD numerators
* Literal 23-step TD versus an independent Fraction reference and the pure
  arithmetic module, with actual instruction trace counts
* Selection's seven maximal subsets times 96 B/T/X combinations; 21 ALUs,
  separate rank handoffs, explicit three-slot padding, no hidden Q/rank cache
* RAM reply/insertion/extraction with invalid code symbols preserved; paid
  address instruction separation; auxiliary/code route costs and same writes
* Resource/reserve rejection; wrong material source despite abundant other
  pools; exact energy-plus-one and material-equality debit boundaries
* Debit-before-effect: insufficient resources leave PC/scratch/RAM unchanged
  for that step; invalid whole programs mutate nothing before execution
* S clears dirty D/R/PC/address/flags, returns HALT, and does not execute a
  subsequent instruction or restore/increment PC
* No extra persistent fields, caller-visible target roots, host callbacks,
  policy/history dictionaries, or trace/ledger feedback

Tests must distinguish core/fragment behavior from a full admitted service.
Synthetic failure in a core is not permission to implement partial funded
service failure or to skip required retirement and S.

## References

* e3/state.py
* e3/meter.py
* e3/physical.py
* e3/protocol.py
* E3_CONTROL_CONTRACT_v0_6.md
* E3_DESIGN_FREEZE_v0_11.json
* E3_OPERATION_CONTRACT_v0_3.md, primitive/services and transaction sections
* E3_POLICY_CONTRACT_v0_5.md, signed bounds and single-record ownership
* .copilot-tracking/reviews/2026-09-10/e3-control-review.md, CT-002/004/005/007/009
* .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md
* .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md
* .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md
* e3/arithmetic.py
* test_e3_arithmetic.py
* test_e3_meter.py

## Validation evidence

Pylance reported the selected interpreter as Python313/python.exe under the
user's local Python installation. It reported no diagnostics in
e3/arithmetic.py. No machine module exists to validate in this session.

Executed the existing baseline with the selected interpreter and bytecode
disabled: `-B -m unittest test_e3_state test_e3_meter test_e3_protocol
test_e3_physical test_e3_arithmetic`. All 129 tests passed in 2.448 seconds.
These are dependency/component tests, not evidence of an implemented machine.
The existing arithmetic tests include constructed fixed-seed local numerical
fixtures, not experimental targets or hypothesis runs.

No new executable files, target draws, experiment runs, process isolation,
service compiler, source freeze, or full-worker conformance claim.

## Follow-on questions

No unresolved contract question requires user input for the minimal instruction
core. Execution implementation requires an implementation-capable mode/agent;
this research session does not fulfill the user's IMPLEMENT request.

* [ ] Implement only the requested machine module and tests in the next session.
* [ ] Run the new machine tests with -B and check diagnostics after implementation.
* [ ] Verify full-service prepayment, literal ROM linking, all-path local/public
  remainders, permissions, scalar ownership, and boundary handling in later work.
* [ ] Keep process isolation, final targets, and hypothesis runs outside this scope.