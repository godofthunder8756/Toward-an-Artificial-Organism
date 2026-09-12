---
title: Paid ADMIT and teaching code review
description: Focused code review of E3 admission and teaching, with synthetic test evidence.
ms.date: 2026-09-10
---

## Status and scope

Complete. One reproducible P2 boundary defect remains in ADMIT (CF-001).
No additional component defect was found in the reviewed teaching paths.
This is not full E3 conformance or acceptance of a production runtime.

Review limited to e3/admission.py, e3/teaching.py, test_e3_admission.py,
test_e3_teaching.py, and the machine, meter, physical, state and contract
dependencies needed to resolve the requested boundary questions. Only this
review document was authored. No source, test, manifest or other document was
edited; no production service sequence, full phase, target draw, hypothesis
run or additional service implementation was started.

E3_INTEGRATION_DECISION_v0_11.md remains authoritative: current final launch
and confirmatory H2 are NO-GO. Component test success cannot change that decision.

## Questions

* Verify exact ROM closure for ADMIT and LESSONCOMMIT, typed microcode, paid
  per-write bounds, E0/source-P endpoints, and deferred-label rejection behavior.
* Check mixed-program PAD validation, actual GATE traces, observer matching,
  post-GATE label scratch lifetime, and retained atomic input ownership.
* Check selected-dtype meter outcomes, prepared versus executed failure traces,
  caller slot-retirement preconditions, and stored-valid COMMIT semantics.
* Reproduce sentinel resource masking and cleanup under integer-Q pressure,
  including material charges and state-P debit before clearing the current slot.
* Run focused existing and independent synthetic unit tests after freeze
  verification, without changing source, tests, or other documents.

## Findings

### CF-001 P2 ADMIT misses whole-service signed-32 quote overflow

Location: e3/admission.py, run_admit entry validation and outer gate call,
lines 99-112. Contrast e3/teaching.py, _entry, line 391.

ADMIT validates the tail itself, then calls gate with _BODY=321. The meter
separately checks 128+8+T+1 for minimum admission and 321+T+1 for the
post-fee body. Neither expression includes the entire admitted 449-energy
service plus tail and residue. Thus an invalid whole-service G quote can
pass arithmetic validation and be classified as physical shortage instead.

Reproduction, with a valid matching BEGIN, zero Scratch, E=450 and P=(1,1,1,1):

```python
from e3 import admission, meter
from test_e3_admission import fixture

state, scratch, begin = fixture(450, (1, 1, 1, 1))
tail = meter.Cost(meter.INT32_MAX - 322)
result = admission.run_admit(state, scratch, begin, None, tail)
```

Observed result:

* T.energy is 2147483325.
* The full quote is 449+T+1=2147483775, above INT32_MAX=2147483647.
* run_admit returns SHUTDOWN; E changes from 450 to 0.
* The only event has paid=Cost(0), outcome=GateResult(False, False, 450).
* P and RAM remain unchanged; no cue, C or S executes.
* Direct floor_quote(Cost(449, (1,1,1,1)), public_tail=tail) raises
  OverflowError instead of accepting that quote.

Expected: reject the overflowing whole-service configuration technically
before any state mutation. E3_OPERATION_CONTRACT_v0_3.md, Transaction admission
and mandatory tails, and the selected ROM closure, One shared instruction
address space and finite G, require invalid/overflowing G rejection before
execution rather than physical-death classification. Teaching already performs
the corresponding full-price preflight.

An independent boundary sweep confirmed exactly 128 unchecked energy values:
T.energy from INT32_MAX-449 through INT32_MAX-322 inclusive. Each silently
shuts down the E=450 fixture. At INT32_MAX-321, the current post-fee quote
finally overflows and leaves state unchanged. At INT32_MAX-450, the complete
quote equals INT32_MAX, so physical shortage is the correct result.

Recommended parent fix: before the gate, validate the complete public maximum
Cost(449, (1,1,1,1)) plus T plus residue using the same approach as teaching's
_entry. Add a regression at the first invalid whole-quote boundary and the
largest valid neighbor. Do not solve this by removing legitimate shutdown for
large but representable bounds. Existing test_bad_entry_is_atomic_before_meter
tests T=INT32_MAX, which catches the obvious overflow but misses this gap.

Impact is restricted to malformed extreme caller-supplied configuration bounds.
The selected normal service tails are far below this range, and no error in
their actual paid writes or cleanup was reproduced. This is not evidence of
wrong ordinary ADMIT execution, a teaching cost bug, or a scientific result.

## Contract and implementation checks

Read the complete selected ordinary ROM closure and both implementation/test
modules, plus the current machine/meter/physical/state dependencies. Authority:

* .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md
* E3_INTERFACE_CONTRACT_v0_9.md, authority, scalar custody and observation sections
* E3_OPERATION_CONTRACT_v0_3.md, pricing, signed bounds, retirement and residue
* E3_STATE_CONTRACT_v0_2.md, raw staging validity and operation scratch
* E3_INTEGRATION_DECISION_v0_11.md, incorporated witnesses and execution limits

### Literal typed programs and traces

| Path | Executed CONTROL | Full energy | Full material | Normal full trace events |
|------|------------------|-------------|---------------|--------------------------|
| ADMIT | 11 | 449 | (1,1,1,1) | 19 |
| BLOCK LESSON | 33 | 490 | (1,1,1,1) | 46 |
| REP LESSON | 38 | 1154 | 5 at the cue's source | 58 |
| COMMIT | 121 | 3756 | (1,1,1,1) plus 20 at the public block's source | 293 |

The current mixed representation is GateImage, not a class named _MixedProgram.
GateImage.program projects ScalarSite/GateSite to typed PAD solely for
forward-DAG validation. _run never executes these placeholders through
machine._step and never reports them as paid PAD work. Real M128 events retain
their GateSite, paid Cost and typed GateResult; scalar events are actual paid
deliveries. Every remaining executable site is a validated Instruction.

Paper offsets are rebased by two for teaching's outer M/C wrapper boundaries.
ADMIT also keeps its I/O outside the core Program: the scalar at PC1 is followed
by the actual SHL at PC1. Its 19-event trace is intentional, not a missing paid
instruction or a complete linked global-PC ABI claim.

The C256 charge is paid by this invocation before its private core is entered.
The runner does not call public machine.step or pay a second machine.execute
envelope; public machine.step itself refuses CONTROL programs.
The forward DAG prevents PC1 reentry after ADMIT deletes cue. Trace outcomes,
host V/A/W totals and prior payments are not accepted as worker inputs.

COMMIT implements EQ-valid/BR-not as NE-invalid/positive BR, preserving the
same one-comparison and branch counts. Actual failed write branches have the
prepared address and scratch f3, advance to their literal EXIT/CLEAR, and do
not execute the next cell. Branches were checked against the current scratch
predicate and the returned next_pc, not inferred only from total costs.

### Meter, source bounds and endpoints

At every ordinary debit, c+L+T+one-energy-residue is checked. E is packed uint16,
P components uint8; Cost components are nonnegative checked signed-32 integers,
not floating-point or reservoir-width arithmetic. GateResult distinguishes paid,
enough and shutdown loss; no successful-reservation flag grants later debits.

ADMIT/BLOCK LESSON reserve four complete 14-energy staging/query writes, one
at each actual source, before consuming input. REP/COMMIT optional code writes
cost 23 energy and one source unit at the paid address. Before cue discovery,
the public fixed body omits optional write commitments; REP's full-price
material bound is the sourcewise maximum (5,5,5,5), not an actual four-pool debit.

REP/COMMIT keep future generation and gate fees in L. A paid failed BR releases
only the unvisited suffix. COMMIT keeps clear/S=(64;1,1,1,1), including when the
first code-write gate rejects. Equality is allowed for material; one energy
must remain. E=0/minimum failure performs no payload reads, C or S and only
records the actual physical energy sink. No free status-flag writes occur.

Independent pressure checks covered every possible energy-limited prefix at
all four sources, with nonzero tails. Four signed-Q raw patterns (0, -1,
-32768, 32767) were combined with four sources and 0/1/19/20 affordable COMMIT
writes. All 64 fixtures preserved Q bytes and charged P before each real
staging-clear mutation. This includes the first-write-rejected case, which
still consumes exactly one cleanup unit from every source and reaches paid S.

For example, with E=5000, T=(17;2,3,4,5), P=T.material+(1,1,1,1), raw stage
255 and no extra code-write material: V/A/W=(1,1,0), spend=(750;1,1,1,1),
end E=4250, P=T.material, selected staging byte zero and Scratch zero.
No later generation/gate/write was executed or charged.

### Raw reads, input custody and scratch honesty

Sentinel tests permitted only paid two-bit reads of the selected staging
lanes, rejected all ADMIT/REP lane reads, and checked physical debit completion
before every allowed read. Code reads, Q reads, resource-as-RAM reads and
unpaid raw staging reads were not used by these service paths. Typed meter
stock access bypasses the generic RAM API by design, not by a free policy sensor.

Rejected/unfunded calls do not inspect cue/label packets. Admitted teaching
validates each scalar only at its paid site; malformed second scalars preserve
the already paid first-scalar prefix rather than manufacture S. BLOCK/REP use
Scratch after insertion, and current expected symbols reside in D[16:2] across
gates. Clobbering R0..R3 at M does not destroy payload, address or validity.

Scratch allocations remain within D96/R128/control32. ADMIT addresses D[0:8];
BLOCK uses raw D[0:8], cue D[8:4], label D[12:1], address D[16:11]; REP uses
cue D[0:4], label D[4:1], base D[8:7], expected D[16:2]; COMMIT uses raw D[0:8],
payload D[8:4], expected D[16:2]. No codeword array, acquired host label cache,
worker success bitmap, V/A/W accumulator or acquired host loop counter drives
execution. Public catalog expansion loops construct target-independent ROM.

The wrapper no longer retains its original packet tuple through service end:
run_lesson deletes packet, empties handoff with pop, then invokes _run. After
cue delivery, _run retains only (0, undelivered_label); after label delivery,
packet is None and scalar/value locals are deleted. Frame checks verified this
from the next core instruction onward, including across gates. Current input
was nevertheless supplied as an explicit host tuple before the atomic call;
unconsumed input retention is not production current(tag) custody enforcement.

Do not claim literal zero host copies: external callers may retain inputs;
observer events retain scalar/value copies; ADMIT retains its BEGIN object
(including the entry State image) for the call even though it never uses it as
payload RAM. Python evaluator temporaries and inaccessible observer history are
not established isolated worker storage. The reviewed core does not read them
back, but production process/capability tests are still required. A future
adapter consuming once is insufficient if a callback caches the delivered
label outside Scratch and uses it later without a second receive; that would
still be an extra acquired register. No such callback executes here.

### Stored validity, caller preconditions and failure observation

COMMIT uses only four paid stored-validity bits and the four paid stored label
bits. All-ones validity may be a false positive; encoding a coherent wrong
codeword from corrupt labels is permissible and is not a bug. Encoding's M128
is paid even for invalid staging; the optional 2680-energy generation/gate
budget never promises all twenty write materials. Same-value writes still cost.

ADMIT assumes preceding RESPONSE retirement and the correct scheduled slot.
It does not read the old slot, add an implicit clear, authenticate retirement
or enforce scheduling. These are explicitly documented caller preconditions,
not a demonstrated full-runtime omission in this component review. Teaching
likewise relies on grouped acquisition provenance and the caller scheduling
COMMIT even after a rejected fourth lesson; its public block is not tick-cyclic.

TeachingResult.vaw reduces completed observation events only. Normal funded
prefixes have V=A, including the final generated cell whose write gate rejects.
An injected technical stop before COMMIT PC22, after three completed parity
ALUs, produced V/A/W=(1,0,0), paid energy 555, PC22, unchanged staging and dirty
Scratch. No unexecuted M, write, S or successful cleanup was invented. An
injected post-debit read failure can leave actual energy debit absent from the
completed-event sum; the existing tests explicitly distinguish that incomplete
event from physical state. This is not a complete production failure archive.

Four constructed repeats from identical State/header/input produced identical
component traces and final states. This is deterministic component replay,
not original production trace commitment or whole-context replay validation.

### Editor diagnostics

Pylance reports no diagnostics for e3/teaching.py. e3/admission.py has four
reportPossiblyUnboundVariable diagnostics for cue at lines 132, 134, 137 and
140, message '"cue" is possibly unbound', severity Error, due to deleting it
inside the while loop. Those are real editor errors,
not suppressed or fixed here. The validated strictly forward program executes
PC1 once, so this review did not reproduce an unbound-variable runtime path
under the stated noninterleaving, immutable-ROM preconditions. They are not
counted as another semantic defect. The two focused test files have no reported
editor errors. No claim of a globally type-clean project is made.

## Test results

Read-only design verification passed before execution and again after testing:
23 of 23 entries, no failures. Python 3.13 was the editor-selected interpreter.
Existing tests used -B; in-memory synthetic suites disabled bytecode before
workspace imports and wrote no test files.

| Suite | Test methods | Passed | Failed | Fixture detail |
|-------|--------------|--------|--------|----------------|
| Existing admission and teaching unittest modules | 32 | 32 | 0 | 9 admission and 23 teaching methods, including their internal matrices |
| IndependentReview synthetic suite | 9 | 8 | 1 | 200 passing fixtures and one failing CF-001 regression |
| BoundaryFollowup synthetic suite | 2 | 2 | 0 | 130 quote-boundary characterizations and one interrupted-generation fixture |
| Total completed test methods | 43 | 42 | 1 | 332 synthetic fixture evaluations; no inflated count of existing internal loops |

The intentional assertion failure is test_07_ADMIT_whole_quote_overflow_must_not_be_shutdown.
The follow-up boundary test passes by asserting the observed defect window;
it does not show a fix. No source correction was applied. The synthetic harness
prints unittest failures explicitly; its successful Python process exit is not
being presented as all tests passing.

IndependentReview passing fixture breakdown: paid-read sentinels 4; Q-extreme
cleanup/material pressure 64; all energy prefixes/sources 108; post-capture
frame lifetime 4; no-access rejection/dead entry 12; teaching overflow 3;
largest valid ADMIT int32 quote 1; component repeatability 4.

The completed baseline ran 32 tests in 6.151 seconds with explicit marker
ADMIT_TEACH_REVIEW_BASELINE_RERUN_EXIT=0. An earlier verbose invocation was
interrupted with KeyboardInterrupt and is excluded. IndependentReview ran in
1.541 seconds; BoundaryFollowup in 0.078 seconds. Execution was confined to
synthetic component calls, not full acquisition or any scientific phase.

Before/after SHA-256 comparison confirmed all eight monitored source/test
files unchanged: e3/admission.py, e3/teaching.py, e3/machine.py, e3/meter.py,
e3/physical.py, e3/state.py, test_e3_admission.py and test_e3_teaching.py.
Final freeze marker: ADMIT_TEACH_REVIEW_FINAL_FREEZE_EXIT=0.

## Remaining questions and recommended follow-up

* [ ] Parent fixes CF-001 and promotes its invalid/valid-neighbor regression
  into the focused admission suite, then reruns it and freeze verification.
* [ ] Resolve or narrowly document the ADMIT cue liveness diagnostics without
  reintroducing a retained acquired host label or changing paid instructions.
* [ ] At a separately authorized runtime integration stage, validate linked
  global ROM PCs, scalar custody/process isolation, one-way observer access,
  scheduler retirement and production original-trace replay. None is credited
  by these reduced tests; this review does not start that work.

No clarifying question requires user input. The defect, reproduction, affected
scope, observed non-findings and remaining runtime boundaries are sufficiently
specified for the parent to act without changing the current final NO-GO.