---
title: E3 machine code review
description: Read-only review of the engineering instruction fragment and its deterministic tests against selected contracts and component APIs.
ms.date: 2026-09-10
status: Complete - one P2 fragment error-reporting defect reproduced
---

## Review decision

One medium-priority defect, E3-MACH-001, is reproduced in `execute()` failure
reporting. Dynamic permission failures bypass `FragmentFailure` and lose its
completed paid-prefix record. Forbidden memory access is still prevented;
this is not a resource bypass, unauthorized read/write, or free CONTROL flow.

No other defect was established in the reviewed engineering-fragment scope.
The existing 137 targeted tests pass. Four additional expected-contract
regressions fail for this single defect, with zero test errors. No source or
test repair was made. CCI-001 and CCI-002 remain closed, without new findings
or changes to their disposition.

## Scope and authority

Read e3/machine.py and test_e3_machine.py in full, plus the relevant State,
Scratch, meter and physical implementations. Reconciled these authorities:

* E3_INTEGRATION_DECISION_v0_11.md:27-60 and E3_INTERFACE_CONTRACT_v0_9.md:9-24
  for selected authority and adoption of ordinary service/ROM notes
* E3_CONTROL_CONTRACT_v0_6.md, including CT precedence, fixed-slot ABI,
  CONTROL prepayment, TD/selection bindings, and finite ROM endpoints
* .copilot-tracking/reviews/2026-09-10/e3-control-review.md, CT-001 through CT-010
* .copilot-tracking/research/subagents/2026-09-10/e3-control-trace.md:33-237,
  interpreted with the selected CT repairs rather than stale placeholders
* .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md and
  .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md,
  especially elemental operands, bundled access insertion/extraction,
  entry/exit PC, and sourcewise quotes
* E3_OPERATION_CONTRACT_v0_3.md:56-82 for primitive costs and typed resources

The two machine files implement and test a partial instruction foundation,
not a compiled controller, complete service VM, scalar adapter, worker process,
or conformance oracle. Missing implementations explicitly excluded by
e3/machine.py:1-24 are not recast as latent security defects. This review
does not duplicate the general component or codec/input review.

## E3-MACH-001 Permission failures omit the paid-prefix record

Priority: P2. Status: Open; reproduced, not repaired.

Primary location: e3/machine.py:644-645. Triggering paths:
e3/machine.py:549-556 and e3/physical.py:181-189.
Declared failure interface: e3/machine.py:422-431.

`execute()` wraps only `ValueError` and `OverflowError`. Dynamic READ2 and
WRITE2 quote their actual scratch address through the physical API. For
reservoir lanes 900..923 and reserve lanes 972..1103 that API raises
`PermissionError`, which derives from `OSError`, not `ValueError`.

These are valid eleven-bit dynamic operand encodings, so whole-program
validation correctly accepts the instruction before the address is computed.
When the forbidden address is reached after paid work, the raw exception
escapes the execution loop. Its completed `events` and `envelopes` are not
published as the promised `FragmentFailure.prefix`. In contrast, an
out-of-range dynamic address such as 1104 receives the proper prefix because
its rejection is a `ValueError`.

The effect is an inconsistent technical-failure API and missing structured
observer evidence of work already paid. A caller handling `FragmentFailure`
cannot obtain the same prefix for these ordinary permission traps. No claim
is made that an archive writer already mishandles this exception or that a
full worker exists.

### Deterministic reproduction

Run as an in-memory Python fixture with bytecode disabled. This is the
READ2/900 member of the executed four-case expected-contract regression;
the same failure occurs for WRITE2 and reserve lane 972.

```python
import sys
sys.dont_write_bytecode = True

from e3.machine import (
    ADDRESS, R0, Charge, FragmentFailure, Instruction, Opcode,
    Operand, OperandKind, Program, execute, immediate,
)
from e3.state import Scratch, State

state, scratch = State(), Scratch()
state.energy = 1024
for hub in range(4):
    state.write_material(hub, 5)
reply = Operand(OperandKind.R0, width=2)
program = Program((
    Instruction(Opcode.MOV, ADDRESS, (immediate(900, 11),),
                charge=Charge.CONTROL_A),
    Instruction(Opcode.MOV, R0, (immediate(3),)),
    Instruction(Opcode.READ2, reply, (ADDRESS,), charge=Charge.ACCESS),
    Instruction(Opcode.S, charge=Charge.EXIT),
))
try:
    execute(program, state, scratch)
except Exception as error:
    assert state.energy == 767
    assert scratch.read_bits(224, 16) == 2
    assert isinstance(error, FragmentFailure), type(error).__name__
    assert isinstance(error.__cause__, PermissionError)
    assert len(error.prefix.envelopes) == 1
    assert [event.pc for event in error.prefix.steps] == [0, 1]
else:
    raise AssertionError("forbidden access succeeded")
```

Observed assertion: expected `FragmentFailure`, got `PermissionError`.
The 257 energy already spent consists of CONTROL_A256 and KERNEL1.
PC remains 2 and R0 remains 3; no failed-access debit, material consumption,
payload access, scratch clear, or rollback occurs. Those state effects are
correct. Only the exception/prefix handling is defective.

An additional complete sweep covered both opcodes and all 2,048 dynamic
address encodings, checking entire persistent and scratch images against
independent byte expectations:

| Outcome per opcode | Encodings | Observed reporting |
|--------------------|-----------|--------------------|
| Accessible RAM | 948 | Successful exact routed debit, access and S |
| Reservoir/reserve | 156 | Bare PermissionError; no prefix |
| Out of physical range | 944 | FragmentFailure with ValueError cause and prefix |

That is 312 affected fixtures across READ2/WRITE2. These are instances of one
bug, not separate findings. All 4,096 memory/resource outcomes match the
expected permission and payment behavior.

### Minimal repair and regression guidance

Include `PermissionError` among the runtime failures wrapped by the existing
`execute()` try/except, preserving it as `__cause__`. Do not catch every
exception, roll back the prefix, pay for the failed access, fabricate S, or
turn the failure into an admission receipt or physical shutdown. Keep static
validation errors outside that runtime wrapper and preserve `step()`'s direct
exception interface.

Existing test_e3_machine.py:469-491 checks permission rejection through
`step()`, accepting either permission/range exception. The fragment-prefix
tests at test_e3_machine.py:605-640 cover source shortage and signed overflow,
not dynamic permission failures. Add READ2/WRITE2 x reservoir/reserve fixtures
with both an envelope and a completed paid kernel prefix, asserting exception
type/cause, exact prefix, and no failing-instruction effects. Retain successful
lane 924 and wrapped out-of-range lane 1104 as neighboring controls.

## Examined behavior without another established defect

### Program validation and declared CONTROL regions

e3/machine.py:356-392 checks every occupied site, including unreachable ones,
and validates nested operand objects again. `None` holes are allowed only
when no successor enters them. BR checks both successors even for a literal
predicate. A finite forward-only graph whose non-S nodes have occupied
successors must terminate at S; there is no terminal fallthrough past ROM.

Reverse path maxima correctly bound A and B independently at 256, reject a
B-to-A path, and distinguish executed instructions from stored alternatives.
An independent enumeration of 3,465 four-site candidate DAGs agreed exactly:
412 valid, 3,053 rejected. An unreachable 257-A path is also rejected.
The existing alternate-arm test legitimately stores 402 CONTROL sites while
bounding an executed A path at 202.

`regions` includes occupied but unreachable CONTROL. Consequently `execute()`
prepays declared A/B even if the entry path skips them, and `step()` refuses
such a program. That can conservatively overcharge a fragment; it is the
declared all-regions rule, not a reachability-counting or semantic bug.
Presence of A is not a proof that every path executes A before B, but both
envelopes are actually paid in order before any instruction. No free B path
results. This validator is not a full-service control-flow permission checker.

### PC, halt, and mutation ordering

e3/machine.py:610-627 requires entry PC already equal to `Program.base`.
It never silently resets scratch or installs a free entry PC. `step()` executes
the occupied PC actually in scratch rather than a host saved result. A
nonzero-base initialized scratch fixture is permitted; full-service entry
lowering remains outside this fragment API.

MOV PC accepts only the full sixteen-bit PC from a uint16 literal, and its
target is rechecked by program validation. Address 65534 is legal; 65535 is
not a usable ROM site even though the immediate can encode it. A constructed
MOV from PC65533 to S65534 passed, ending with energy one and zero scratch;
MOV to 65535 rejected. STAGE/JUMP/MOV use the exact next address, not target+1.
PC cannot be saved, sliced as a source, or written by a dynamic ALU.

S debits eight, clears all 256 scratch bits, returns HALT, and performs no
subsequent PC write. `execute()` stops; a later explicit `step()` request is
not an implicit continuation. The tests instrument this ordering.

Whole-program/type/remainder checks occur before any payment. Runtime
arithmetic, predicate, shift, address permission and affordability checks occur
before the failing instruction's effects. Prior completed instructions and
envelopes remain paid on a later failure; no whole-program rollback is
promised. Signed overflow is therefore an atomic instruction failure, not a
reason to refund earlier work. E3-MACH-001 affects reporting, not that ordering.

### Arithmetic and literal kernel witnesses

e3/machine.py:129-147, 253-284 and 480-530 enforce strict built-in integers,
reject booleans/subclasses, and distinguish signed immediates from raw words.
Signed data operands are promoted explicitly, signed SHR is arithmetic, and
signed ADD/SUB/NEG/SHL trap outside signed32 before debit. Shift counts use raw
0..31 even for signed instructions. Unsigned operations deliberately wrap
modulo destination width; MOV/SELECT reject concealed narrowing. Narrow EX,
Boolean and arithmetic destinations preserve neighboring scratch fields.

An additional 3,360 mixed-width ADD/SUB/AND/OR/XOR fixtures covered destination
widths 1..32 against source widths 1,2,5,11,16,31,32. Exact result, energy,
PC and full scratch images matched an independent bit-mask oracle. Wider
inputs to narrow unsigned arithmetic are declared modulo arithmetic, not an
accidental signed constant or truncation bug. The packed W increment by
2^27 correctly handles W15->16 and W19->20.

`td_program()` implements the actual CT-005 23 instructions, not a call to
`arithmetic.td_update()` with invented counters. The passing machine suite
includes 2,197 boundary triples, 513 remainder fixtures spanning all 128
remainders on each numerator sign, negative half ties, numerator extrema,
old-R0 liveness, and separately paid reward EX/terminal-zero handoffs.

`selection_program()` executes 21 kernel ALUs, three CONTROL EX rank handoffs,
three paid PADs and S. Its seven maximum subsets times 96 B/T/X combinations
are 672 cases, not 675. The independent expected-action calculation and
arithmetic reference agree. T=3 is explicitly a caller's paid packet-check
prerequisite; the separate EX/EQ/BR fixture tests it before the kernel. No
fourth action, second draw, or signed-constant defect is established.

### Storage, memory access, and observer boundary

The fixed partitions match e3/state.py:83-95: D96, four R32 words, PC16,
address11, flags5. Only explicit State276/Scratch32 carry acquired execution
storage. Exact container and closed-enum checks reject callbacks and proxy
objects; revalidation catches malformed frozen values before payment.
Python private access or concurrent mutation is not an asserted sandbox.

READ2 debits its route cost before reading payload, inserts only the named
two-bit R slot, and optionally captures those same bits in D. Bundled capture
requires the designated R0 low reply slot, preserves neighboring fields,
and does not claim to zero upper R0 bits. WRITE2 extracts its two-bit source,
charges same-value writes, and debits the actual source hub. No cost pooling
or hidden RAM/stock operand was found. The complete address sweep also checks
the otherwise less-sampled query/staging/record/age/metadata ranges.

Step/fragment results duplicate values only in an observer sink after effects;
instructions never consume those traces or snapshots. The instruction enum
has no resource/snapshot/ledger operand. Resource reads inside `meter.debit()`
are the trusted accounting API, not an ALU-visible free sensor. General
service-specific RAM permissions beyond reservoir/reserve exclusion are
explicitly deferred, so their absence is not a new component security finding.

CONTROL prepayment uses the actual packed energy through `meter.debit()`.
No GateResult, boolean, callable quote, or prior result can authorize zero-cost
CONTROL. `_bounds()` checks immutable vectors, overflow and S retention;
worst-address vectors validate arithmetic without peeking at RAM. Their
conservatism is not an extra actual debit. Complete suffix sufficiency and
G provenance are explicitly trusted obligations; the default retains S only.
Outer M128/DECIDE and full-service L/T admission are not claimed implemented.

## Executed validation and integrity

The editor-selected interpreter is Python 3.13. Terminal test/verifier runs
used `-B`; in-memory checks set `sys.dont_write_bytecode = True` before project
imports. No test source, fixture file, dependency, root, target, experiment,
worker, or conformance process was created.

| Check | Result |
|-------|--------|
| unittest: machine, arithmetic, state, meter, physical | 137 passed, zero skipped/failures/errors; 10.498 seconds |
| Nine existing CCI-001/002 regressions | 9 passed; 0.025 seconds |
| Expected-contract E3-MACH-001 tests | 4 intentional assertion failures, zero errors |
| Complete dynamic-address effects sweep | 4,096 matched byte/resource expectations; 312 expose the reporting defect |
| Independent four-site DAG enumeration | 3,465 decisions/path bounds matched |
| Additional mixed-width ALU checks | 3,360 exact result/scratch/payment comparisons passed |
| Highest PC endpoint and unreachable over-budget fixtures | Passed |
| Pylance diagnostics for both reviewed files | Empty diagnostic lists |
| Initial CLI and final read-only design verification | ok=true, all 23 frozen files checked, failures=[] |

The nine CCI tests cover independently malformed capsule bytes,
constructor/marshal rejection, admitted/zero/acquisition neighbors, scalar
attempt endpoints/out-of-range/strict types, and unrelated aux preservation.
The existing admission guards and scalar-attempt limit remain present.
CCI-001/002 remain closed and are not reopened or duplicated here.

An in-memory baseline captured 88 existing source, test, verifier, contract,
and tracking-file SHA-256 values. Final comparison found 87 unchanged and
one concurrently changed file, e3/archive.py, not edited by this review.
New e3/kernels.py and test_e3_kernels.py also appeared during review; they
are excluded from this verdict. A terminal attempt returned concurrent
kernel-test interruption output rather than the requested review checks;
it is not counted as review validation. CCI regressions and final verification
were rerun successfully in a separate interpreter invocation.

The reviewed files remain byte-identical to the earlier captured CCI evidence
and the review baseline:

| File | SHA-256 |
|------|---------|
| e3/machine.py | c46a72da4f33c000222ad788c50c24581492d1bc8bb0d1e7521bb2c414abf594 |
| test_e3_machine.py | 9c778f6951ad719e935644d15b769200cf32e85de3efe1ced7895a607deee9e4 |
| E3_DESIGN_FREEZE_v0_11.json | 3678d797dc17485fcc823cb7f83696e4ba20c9a69921d709291cad50c3f878d4 |

This is captured-file evidence, not a filesystem lock or a claim that the
whole workspace was quiescent. The sole review-authored file is
.copilot-tracking/reviews/2026-09-10/e3-machine-review.md.

## Recommended next work

* [ ] Repair E3-MACH-001 and add its four focused prefix regressions when source
  changes are authorized; rerun the targeted suites and design verifier.

No further research is needed to substantiate this finding. No user
clarification is required. Full-service compilation, worker/process isolation,
and broader conformance remain separate work, not failed checks in this review.