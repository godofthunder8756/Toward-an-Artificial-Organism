---
title: E3 bounded instruction implementation evidence
description: Actual engineering-fragment execution, static control bounds, and microcode tests
ms.date: 2026-09-10
status: Complete within component scope
---

## Changes

Created only these three requested files:

* [e3/machine.py](../../../../e3/machine.py)
* [test_e3_machine.py](../../../../test_e3_machine.py)
* This changes record

The prior scoped handoff, selected CONTROL v0.6, integration v0.11, and actual
State, Scratch, meter, physical and arithmetic APIs informed the implementation.
The design verifier passed all 23 frozen files before and after implementation.
No frozen source, plan, research note, package initializer or existing test was
edited. No final keys, roots, targets, experiments or external deployment were
created. The workspace is not a Git repository; Git diff evidence is unavailable.

## Implemented boundary

`Operand`, `Instruction` and `Program` are frozen, slotted values with closed
enums and strict built-in integer checks. Operands name only fixed scratch
partitions or typed <=32-bit literals. State remains its existing 276-byte
payload and Scratch its existing 32-byte payload. No machine object, extra
mutable PC, acquired execution-count slot, callback, host macro or shadow stock
was added. PC is read from Scratch for every instruction.

`validate()` checks every occupied site, including unreachable instructions,
before resource mutation. Reverse-DAG analysis verifies literal forward
occupied successors, terminating S paths, per-region CONTROL bounds <=256,
A-before-B ordering, semantic operand restrictions and the 0..65534 ROM range.
The static proof distinguishes stored sites from executed instructions: a test
has 402 stored CONTROL sites but a maximum executed A path of 202.

`step()` executes exactly one instruction and refuses programs containing
CONTROL. It never accepts a payment receipt. `execute()` supports only
`ExecutionMode.ENGINEERING_FRAGMENT`: it actually prepays 256 for each declared
CONTROL region, at most A and B, before running instructions. Both declared
regions are paid even when a branch skips B. CONTROL then has zero incremental
debit; kernels and padding cost one each, and final S costs eight.

This fragment algorithm does not pretend to be a full controller: it has no
outer M128, DECIDE gate, service admission, runtime G computation, scalar
ownership or complete local/public suffix proof. Prepayment reserves remaining
envelopes, S and the supplied public tail. Per-instruction local bounds default
to S only; caller-supplied extra bounds must be immutable ROM-indexed Cost
tuples. Public tails are immutable Cost values, never dynamic generators or
acquired callbacks. Their G provenance and sufficiency remain trusted duties.

## Instruction and payment semantics

* MOV copies or zero-extends bits; narrowing requires explicit EX. Signed EX
  promotes two's complement into a full word, never silently through MOV.
* Signed ADD/SUB/NEG/SHL use checked signed-32 results. Narrow signed values
  require prior EX. Unsigned arithmetic wraps modulo destination width;
  narrow scratch writes preserve neighboring bits.
* SHR is arithmetic for signed data and logical otherwise. Shift counts are
  unsigned 0..31, including all five-bit encodings. Boolean operations and
  SELECT preserve raw word encodings; comparisons produce canonical 0/1.
* BR charges either outcome. STAGE, JUMP and literal uint16 PC MOV use their
  declared target as the next PC, not target+1. No PC saving, dynamic PC ALU,
  backward jump or hidden call/return exists.
* READ2 uses the physical route cost and debits before reading the lane. It
  inserts a two-bit reply into an R slot; bundled D capture requires the
  designated R0 low two-bit reply. Invalid code symbol 11 remains raw data.
* WRITE2 extracts exactly the declared two-bit scratch source and debits
  energy and material at the actual owning source before memory mutation.
  Same-value writes still pay. Reservoir and reserve lanes are inaccessible.
* All instruction operand, arithmetic, address and affordability failures
  precede that instruction's writes. A failed fragment retains its completed
  paid prefix, including CONTROL envelopes; no whole-program rollback occurs.
  The observer-only `FragmentFailure.prefix` cannot fund continuation.
* S clears every scratch byte and returns HALT without any subsequent PC
  write. `execute()` stops immediately. A caller of standalone `step()` must
  honor HALT; an explicit later call is a new scheduling request.
* Immutable trace events are produced after payload and PC effects. Neither
  the step engine nor an instruction accepts trace/history/ledger feedback.

## Executed evidence

The editor-selected Python 3.13 interpreter ran with bytecode disabled:

```text
-B -m unittest -v test_e3_machine
-B -m unittest test_e3_machine test_e3_arithmetic test_e3_state test_e3_meter test_e3_physical test_e3_protocol
-B verify_e3_design.py
```

The machine suite contains 43 passing tests. The final combined run passed
172 tests in 8.115 seconds. The final verifier checked all 23 frozen files and
reported no failures. Editor diagnostics and Pylance checks are clean in both
new Python files. No third-party dependency was installed.

New executable coverage includes:

* Actual 23-ALU TD microprogram against both an independent Fraction oracle
  and `arithmetic.td_update`: 2,197 boundary-word triples, 513 remainder
  fixtures spanning all 128 remainders with positive and negative numerators,
  negative half ties -64/-192, numerator extrema, and R0 survival through
  instruction 18
* Explicit separately paid signed reward EX and terminal R2=0, with no call
  to the pure arithmetic implementation during instruction execution
* Actual 21-ALU selection across seven maximal subsets and all 96 B/T/X
  combinations, totaling 672 cases; three separate CONTROL EX handoffs and
  three explicit paid padding instructions cannot conceal other work
* Separate paid EX/EQ/BR caller fixture for T=3 rejection before selection;
  the kernel itself assumes a previously validated packet
* All scratch operand widths and partition edges, malformed enums/arity,
  strict integer and immediate bounds, signed overflow, unsigned wrap,
  narrow-field neighbor preservation, and packed W transitions 15->16/19->20
* Both branch outcomes, exact STAGE/PC MOV semantics, occupied-target checks,
  finite DAGs, 256+256 execution allowances and rejection at 257
* READ2 insertion/capture, eight Q lane reads plus signed EX, raw invalid
  symbols, address instruction separation, code/auxiliary prices, same-value
  writes, unequal source stocks and sourcewise material equality
* Paid persistent bit updates using READ2, explicit AND/OR, then WRITE2;
  no free masked persistent write
* Instrumented debit-before-read/write ordering, energy-plus-one boundaries,
  failed read/S atomicity, frozen-program revalidation, paid-prefix failure
  ledgers, immutable external tails, and no post-S PC mutation

## Remaining work and limits

This is instruction-component evidence, not a full worker, service tariff,
serial protocol, full B02 conformance, experiment or empirical E3 result.
The selection kernel requires valid signed-word/rank inputs; actual paid load
and packet-trap paths belong to later service compilation. Fragment failure is
a technical exception, not permission to omit mandatory service retirement
or reinterpret it as biological death.

Full ROM linking, service compilation, METER/G suffix computation, scalar
ownership, public-input provenance, checkpoint/replay boundaries, flow
noninterference and process sandbox enforcement remain pending. Python frozen
objects and private helpers are trusted-host conventions, not adversarial
capabilities. Generic program provenance is not proved by shape validation.
No full-service prepaid CONTROL receipt API is exposed.