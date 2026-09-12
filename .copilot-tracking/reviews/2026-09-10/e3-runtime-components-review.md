---
title: E3 runtime components review
description: Read-only review of upkeep, services, transport, fast machine, and associated tests.
ms.date: 2026-09-10
---

## Status and scope

Complete for the inspected component scope. No confirmed runtime-component bug
was found. No critical, high, medium, or low-severity defect is being reported.
All suspected issues below were resolved against source, current callers, and
executed checks before this handoff. No production repair is recommended on
the evidence collected.

The sole review-authored workspace artifact is this report. Runtime sources,
tests, frozen contracts, experimental keys, and target draws were not modified.
The review covers e3/upkeep.py, e3/services.py, e3/transport.py,
e3/fast_machine.py and their tests, with reference-machine, meter, protocol,
kernel, physical-map, and storage dependencies. It is not a full-runtime,
process-isolation, experiment, or global repository pass.

The 23 entries in E3_DESIGN_FREEZE_v0_11.json freeze design documents, not the
implementation. Successful verification is integrity evidence only and does
not authorize final target draws or confirmatory execution.

## Research questions

* Verify compulsory upkeep sourcewise admission, public tails, paid CONTROL,
  minimum-failure shutdown, and preservation of remaining material and RAM.
* Verify TICK passive support, preflight arithmetic, actual accepted transport,
  five scalar occurrences, grant bounds, fees, shutdown, and exit state.
* Verify CONDITION's literal PC-driven witness, nested meters, paid CONTROL,
  rejection branch, and scratch lifetime without assuming caller payment tokens.
* Verify transport single-use permits, session epochs, scalar ordering, group
  caps, cost/tail admission, frame rejection, and documented trust boundaries.
* Differentially compare fast and reference execution, including traces,
  effects, paid-prefix failures, operand reads, validation, and exact-energy S.
* Run targeted read-only synthetic checks and existing suites with bytecode
  writes disabled; verify all 23 design-freeze entries afterward.

## Findings

No actionable defect established. Expected rejections, dirty scratch on
terminal failure, deliberately incomplete engineering fragments, and trusted
HOST metadata are not presented as bugs. Passing tests alone were not used to
resolve the questions: the following conclusions include source and caller
evidence and additional constructed boundary cases.

### Mandatory upkeep and sourcewise tails

e3/upkeep.py:105-142 constructs a fixed literal service and exact public body
quote. e3/upkeep.py:167-197 checks the complete mandatory body, public tail,
and one energy residue before any instruction, discovery, or material spend.
AGE costs 952 energy and (5,5,5,5); ISOLATE costs 1120 and (13,13,13,13).
M128 is paid by the wrapper and C256 by `machine.execute()`, once each.

The reference engine's default local remainder is S8, not the entire remaining
upkeep body. This is not a demonstrated funding defect in this wrapper: every
fixed instruction is admitted up front, every raw four-bit age is valid, and
there is no optional branch, interleaving, or in-call fault. Actual suffix
costs therefore remain funded throughout. test_e3_upkeep.py:196-218 checks
every debit against the exact remaining sourcewise sum. A future interleaved
runtime must not reuse this argument without its stated assumptions.

Additional checks used tail (211;7,11,13,17). Exact body-plus-tail-plus-one
funding exited with (212;7,11,13,17). Subtracting one unit from each source in
turn caused SHUTDOWN before fees or instructions; only E changed to zero,
all remaining material/RAM bytes were preserved, and scratch stayed zero.
There were 15 additional cases across the three services. Prior apparent
success or favorable age values never narrowed the supplied public tail.

The eight-op age kernel saturates 15 rather than wrapping; both reads and
writes remain paid at saturation. ISOLATE writes all 52 lanes, including
same-value zero writes, and clears no unrelated RAM. Fault hazards are handled
by the separate physical component, not implicitly scheduled inside upkeep.
Its existing synthetic tests verify post-operation age ownership and
simultaneous pre-fault state semantics; no age backup was added to upkeep.

Authority: .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md:359-386,
441-508 and .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md:155-180.
The v0.9 interface adopts these technical witness sections.

### TICK grant, admission, fees, and shutdown

e3/services.py:44-62 and 203-277 validate exact types, all five grant values,
and worst-case signed-32 quote arithmetic before PASSIVE mutates the body.
PASSIVE then precedes the resource minimum, as the selected exception requires.
An initial E=0 ignores all support. A live body can accept support and then
shut down for insufficient energy or a tail source, without rollback.

`CurrentGrant` bounds energy at 30000 and each material offer at 255. Current
phase-specific g, equal ordinary offers, and one-shot provenance remain
explicit external-scheduler duties. Reduced and unequal engineering fixtures
are allowed. The structural GRANT_E wire width of 16 bits is not itself a
phase-specific grant authorization, and transport does not claim it is.

Accepted material is held in the four D bytes after PASSIVE. `_tick_suffix()`
uses those actual current amounts; scalar registers cannot change them.
The five scalar occurrences carry the original offered values, not accepted
amounts, cost one each including zero, and write R0 only after debit.
Immutable frame preparation before PASSIVE is privileged packet validation,
not a pre-debit worker-register insertion or body-dependent output.

Total cost is 128+5+sum(accepted material)+16+20+8, with no CONTROL or material
debits. Constructed example: initial (65535;254,255,250,0), grant
(30000;9,8,7,6), zero tail. Accepted support is (0;1,0,5,6); scalar values are
30000,9,8,7,6; paid energy is 189 and final E is 65346. S clears all scratch
and there is no subsequent PC write.

Failure example: initial (1;0,0,0,0), grant (10;255,255,255,255), zero tail.
Result is SHUTDOWN with two events, zero paid fees, loss 11, final E=0,
all four P=255, and scratch PC=1. This is support then terminal shutdown,
not an active funded tick or a successful S exit. The current component emits
no archive activity flag; such a flag must not be inferred from grant receipt.

Evidence: test_e3_services.py:67-188, 348-481; adopted literal sequence and
price at .copilot-tracking/research/subagents/2026-09-10/e3-rom-closure.md:46-61.

### CONDITION literal execution and actual CONTROL payment

e3/services.py:280-382 emits the fixed domain program, validates its 9-CONTROL
maximum, pays outer M128 and C256, and drives each instruction from the current
Scratch PC. Nested M128 at PC2 supplies the rejection flag; no caller token
claims previous payment. The literal first MOV advances PC to 1; rejected
execution visits 0,1,2,9,10,11 with five CONTROL instructions. Admitted
execution visits all twelve sites, with nine CONTROL instructions, two writes,
and S. The loop is a finite interpreter over this forward program, not an
unmetered algorithmic conditioner loop.

The outer minimum retains C256+nested M128+S8. After C, local 136 means
unpaid M128+S8, not an already charged reservation. Nested admission tests the
whole optional (32;b(domain)) body. Dues debit four energy and one domain-hub
material; the two writes debit 14 each at their actual lane sources.
Rejection pays 520 energy, reads/writes no RAM, and exits through paid S;
admission pays 552 plus b(domain). No private age or presumed body-success
fact removes a later service from T.

Additional checks covered all twenty domains at initial E=520,521,552,553
with exactly b(domain) and zero tail. Results respectively: minimum shutdown
with no fees; rejected exit with E=1; rejected exit with E=32; admitted exit
with E=1. All 80 cases matched and scratch was zero at these boundaries.

Pylance references found `run_condition()` and `run_tick()` callers only in
test_e3_services.py. `run_upkeep()` callers are in test_e3_upkeep.py and its
service-sequence test. No actual CONDITION-to-fast-executor path exists.
test_e3_services.py:292-320 verifies C is paid once before private steps and
explicitly forbids double-prepaying through public execute. As an additional
test-only substitution, routing upkeep's existing execute call to the fast
executor produced identical results, traces, and bytes for all three services.
This substitution changed no source and is not a new production integration.

Authority: .copilot-tracking/research/subagents/2026-09-10/e3-service-traces.md:388-437,
491-504. Existing source-hole and interrupted-write checks also passed.

### Transport permits, scalar groups, and host lifetime

e3/transport.py:1-31 explicitly confines the session, current BEGIN snapshot,
counters, and consistency fields to trusted HOST metadata. It must not be
passed to worker policy. Pylance references found `OperationSession` users
only in test_e3_transport.py. No current worker/policy caller was identified.
Missing paid-PC attestation, body ownership, calendar enforcement, and process
isolation are declared integration obligations, not component security bugs.

`permit()` allows one pending directed named site; `_scalar()` requires the
exact pending object's identity, consumes it, and increments both-direction
count. Equal copies, other-session tokens, replay, skip, reordering, and
prefetch are rejected. `accept()` returns None. `_drop_operation()` clears
BEGIN, pending permit, count, cue, action, yield, last tag, and TEMPLATE flag
on completion/failure; only BIND survives normal operations.

Additional same-site next-BEGIN replay was rejected even with a fresh permit
outstanding. The session became FAILED and released both BEGIN and pending
references. No explicit integer epoch is required for this identity check.
Descriptor possession or direct access to underscore fields is not a worker
security boundary under this host-only contract.

TICK has exactly five inputs. Ranked controllers allow selection prefixes of
six and resource paths of eight; fixed/script controllers use three/five.
RESPONSE feedback follows phase, due, and learning bits and never fabricates
absent zero packets. LESSON/TEMPLATE input groups require two for normal exit.
Expected empty rejections remain permitted where the selected trace allows
them. Feeding all structurally allowed scalars does not prove an economically
funded core: transport has no meter and explicitly does not attest rejection
truth or paid S. Treating that limitation as a new security bug would exceed
the reviewed API contract.

EXIT requires a complete scalar path, no pending permit, and positive raw E.
An otherwise valid output with E=0 is rejected and must use SHUTDOWN.
SHUTDOWN accepts proper scalar prefixes, including pending yield/feedback,
and closes the session; it does not certify the physical cause. TEMPLATE's
semantic BAD is enforced only after both width-valid inputs, not prematurely
after an unaligned first cue. Full existing prefix, header, capability, action
cue/yield, and group-cap tests passed.

Evidence: e3/transport.py:157-369; test_e3_transport.py:106-244, 282-613,
650-686; E3_INTERFACE_CONTRACT_v0_9.md:65-92. SENSE encodings are part of its
sixteen-energy tariff, not extra transport fees; forage/collect yields retain
their 64/8 semantic maxima. No free cue, new resource sensor, or fee is
implemented by this structural validator.

### Fast/reference semantic and failure equivalence

e3/fast_machine.py:337-382 compiles and validates the supplied exact Program
afresh on every call; compiled records cannot be submitted as execution
receipts. `machine.validate()` revalidates all sites, including unreachable
instructions and their operand fields. Forged pre-call field changes are
covered by test_e3_fast_machine.py:300-330 and 384-410. Concurrent mutation
after validation or hostile rewriting of private module globals is outside
the explicitly shared trusted-host assumption; once-per-call validation is
not presented as protection against either.

Both engines validate shift counts, predicates, signed overflow, addresses,
and permissions before the current instruction's debit. Scratch operands may
be read to perform those checks. READ2 RAM payload is read only after payment;
WRITE2 uses its pre-debit operand and changes RAM only after payment. Packed
E/P reads belong to the trusted meter, not the ALU operand space. Both engines
reload PC from scratch and preserve completed paid prefixes on failure.

Existing differential comparisons use complete nested result dataclasses,
exception and cause types/messages, all 276 state bytes, and all 32 scratch
bytes. They cover every opcode, all 2048 dynamic address encodings for both
accesses, signed arithmetic, narrow slices, CONTROL A/B, source/tail equality,
holes, maximum PC, public scan programs, and malformed forged inputs.
Pylance references place current fast callers in test_e3_fast_machine.py,
including the benchmark adapter, not in service production code.

The additional differential sweep passed 296 cases: 168 combinations of
SELECT/BR/SHL/SHR, six energy thresholds, and seven operand patterns; plus
128 signed EX cases spanning every width 1..32 and four bit patterns. Inputs
were constructed with actual Instruction/Operand APIs. Error causes and full
byte images matched, including invalid-operand versus shortage precedence.

Exact-total scan energy is not enough to preserve the mandated positive
residue. The observed failure occurs before S, rather than pretending S ran:

| Fragment | Initial E | Result | Final E | Final PC | Completed steps |
|----------|-----------|--------|---------|----------|-----------------|
| REP | 383 | FragmentFailure / InsufficientResources | 9 | 51 | 51 |
| REP | 384 | S completed | 1 | 0 | 55 |
| BLOCK | 4303 | FragmentFailure / InsufficientResources | 9 | 3760 | 3760 |
| BLOCK | 4304 | S completed | 1 | 0 | 3764 |

Both implementations matched these four cases exactly. Failed fragments emit
no successful scan result and perform no implicit scratch clear. In
particular, BLOCK with 4304, not 4303, reaches S with one remaining energy.
There is no last-energy/S affordability mismatch here.

Technical interruptions are not atomic transactions. Existing injected
second-write tests deliberately retain its already paid debit even if that
write fails before a completed observer event is appended. The prefix is a
list of completed events, not a rollback ledger or receipt for unfinished
work. This documented behavior is not a fabricated normal shutdown.

## Evidence and validation

Windows, editor-selected CPython 3.13 interpreter. Existing suites ran with
`-B`; the additional in-memory Python checks set `sys.dont_write_bytecode`
before importing project code. No ad hoc source/test file was created.

| Executed check | Result |
|----------------|--------|
| test_e3_upkeep, test_e3_services, test_e3_transport, test_e3_fast_machine, test_e3_machine, test_e3_meter, test_e3_protocol | 205 tests, 32.217 seconds, OK, explicit exit marker 0 |
| test_e3_kernels, test_e3_physical, test_e3_state | 64 tests, 41.062 seconds, OK, explicit exit marker 0 |
| Additional in-memory checks detailed above | Exit 0; final E3_EXTRA_SYNTHETIC_CHECKS_OK marker |
| Final verify_e3_design.py invocation | ok=true, file_count=23, files_checked=23, failures=[], exit 0 |
| Baseline SHA-256 content audit excluding this report and Git internals | 5471 captured, 0 changed, 0 missing, 0 added |
| Report editor diagnostics | No errors reported |

Total existing tests executed here: 269, with no failures, errors, or skips
reported in these selected suites. This does not replace prior platform-skip
accounting. The earlier e3-component-review.md reports four native Windows
symlink skips in its different foundation/verifier run. test_e3_design.py:204-243
still conditions those real-link tests on OS permission. That suite was not
rerun here because it creates external temporary fixture files; its earlier
skips are not converted into passes or covered by a global-success claim.

The final content comparison is evidence for this captured tree, not a
filesystem lock or defense against malicious concurrent replacement. No E3
phase, private experimental root/key, final target draw, hypothesis evaluation,
benchmark timing run, dependency installation, or source/configuration/test
edit was performed. Synthetic physical and state fixtures are not E3 draws.

## Follow-up and clarifications

No clarifying question is required to complete this bounded review. No
unresolved suspected component defect is handed to the parent.

Recommended follow-up, not completed or claimed by this review:

* [ ] At full-runtime integration, audit current grant provenance, public G/T
  construction, and paid scalar-PC dispatch together with scheduler callers.
* [ ] Verify worker adoption of the sole body and cancellation of external
  state references, permits, and capabilities across reset/process boundaries.
* [ ] Validate archive activity, failure-prefix, and trace commitments against
  actual service execution rather than structural transport acceptance.
* [ ] Run native symlink/reparse fixture tests in an environment that supports
  their required OS privileges; retain explicit skips until they execute.

These are known integration or platform evidence gaps, not newly established
bugs and not reasons to alter the frozen design during this read-only review.