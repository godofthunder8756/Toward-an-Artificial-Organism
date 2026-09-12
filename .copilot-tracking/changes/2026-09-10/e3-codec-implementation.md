---
title: E3 frame codec implementation evidence
description: Scoped protocol research, implementation checks, and deferred runtime obligations
ms.date: 2026-09-10
---

## Scope and status

Complete for this component. Added only e3/protocol.py and test_e3_protocol.py,
with this optional tracking record. No frozen design, historical code, targets,
roots, runtime, archive, or simulated-state implementation changes.

## Questions under investigation

* Exact frame fields, lengths, enums, scalar encodings, and reserved-bit rules
* Immutable BIND configuration mapping and TEMPLATE/script restrictions
* Header validation supported by public facts without inventing a paid-gate FSM
* Independent golden bytes and malformed-input coverage

## Evidence collected

* E3_INTERFACE_CONTRACT_v0_9.md, first 270 lines: three-byte little-endian
  header; payload lengths 8/284/6/276/276; ABI 9; generic format 1; tags 0..22;
  signed tag 17 uses low sixteen bits with high sixteen zero; raw persistent
  bytes preserve invalid/reserved contents.
* E3_CONFORMANCE_CONTRACT_v0_10.md: TEMPLATE capability 1, phase 5, tick 0,
  argument/mask 0; script G IDs 400..403 and policy IDs 5/6. Script reset
  recovery and assay remain legal; scripts are not limited to ecology.
* E3_INTEGRATION_DECISION_v0_11.md: script namespace 34 is archive-only, not
  a worker phase/family field. Engineering implementation is authorized;
  final targets and confirmatory launch remain prohibited.
* E3_DESIGN_FREEZE_v0_11.json: 23 listed design dependencies; no editing of
  the snapshot or its dependencies is part of this task. The user supplied
  the verified-snapshot status; this task did not rerun the digest audit.
* E3_POLICY_CONTRACT_v0_5.md: cuts 24576/32768/40960 and 32/64/96;
  PERIODIC intervals 1/2/4/8/16/32/64/128/256; default DRIVE/script cuts
  32768/64. Fixed policies do not enable learner bookkeeping.
* E3_EVALUATION_CONTRACT_v0_7.md, acquisition and development section,
  retained by v0.8: acquisition block order is externally shuffled each
  pass. COMMIT block cannot be derived as a cyclic tick formula.
* E3_EVALUATION_CONTRACT_v0_8.md and E3_OPERATION_CONTRACT_v0_3.md:
  exact timed horizons, query warmup/drains, recovery without ADMIT/feedback,
  final learning TERMINAL, and acquisition-only teaching.

## Findings and implementation

* parse_frame(raw) returns the closed frozen dataclass union BindFrame,
  BeginFrame, ScalarFrame, ExitFrame, or ShutdownFrame. encode_frame(frame)
  rejects mappings, duck types, subclass extensions, and malformed fields.
* ProtocolError covers malformed wire structures and invalid contextual
  requests. Python constructors reject unknown keyword fields rather than
  accepting generic metadata. Numeric fields reject bool and coercions.
* Immutable FrameCodec stores only BIND. SCALAR context is an explicit current
  BEGIN argument, never a retained operation buffer or session cursor.
* PublicConfiguration maps IDs 0..399 to the frozen ordinary grids and
  400..403 to scripts. The 512-entry catalog is a capacity, not permission to
  accept unassigned IDs 404..511. FROZEN has no separate G ID.
* No no-maintenance policy number was invented: v0.5 mentions that optional
  comparator, but the selected v0.9-v0.11 G enumeration assigns no distinct
  wire ID to it. Future support would require an explicit selected mapping.
* Script policies are 5/6, objective 0, with no added worker family enum.
  Their ecology and reset recovery/assay headers are accepted; acquisition,
  development, and oracle script dispatch are rejected.
* Header validation checks listed service/phase membership, tick bounds,
  learning/corrective/due permissions, slot arithmetic, admission drains,
  CONDITION domain, fourth-lesson COMMIT boundary, and last learning TERMINAL.
  Actual shuffled COMMIT block selection remains an external obligation.
* All scalar widths/ranges and unused high bits are checked. Tag 17 stores
  65472 for -64, not a 32-bit sign extension. scalar_from_value and sign_extend
  provide explicit checked conversions.
* Context checks scalar/service membership, fixed/script rank-input absence,
  learning feedback permission, TEMPLATE capability, and REP/BLOCK shapes.
  Width-valid TEMPLATE semantic errors parse structurally; contextual errors
  do not implement or replace the emitter's required paid BAD path.
* Raw 276-byte state is immutable bytes with corrupt/reserved storage retained.
  SHUTDOWN additionally requires bytes 225..226 (E) to be zero. This is not a
  claim that physical shutdown or paid S has actually occurred.

## Validation

Executed python -B -m unittest test_e3_protocol once: 34 tests passed in
1.582 seconds. No other test suite or simulator was run.

Independent literal golden bytes cover every kind and every scalar tag.
Malformed fixtures cover all 327675 incorrect u16 kind/length pairs, every
truncated golden prefix, concatenated/trailing bytes, unknown tags/enums,
every wrong u8 scalar width, every unused high scalar bit, semantic ranges,
state length, and little-endian cases. Exhaustive low-16-bit sign extension
and all 400 ordinary grid IDs are checked. Template cue/payload tests and
public script/reset contexts are component checks, not target-generation tests.

Editor diagnostics report no errors in either Python file. Pylance syntax
checks passed for both. All dependencies are standard-library modules;
production state, runtime, E1/E2, and target-generator modules are not imported.

## Deferred obligations and clarifications

Paid opcode authorization, single consumption, missing/duplicate/order checks
across frames, operation scalar caps, S termination, process isolation, and
production target-access checks require the future runtime/emitter. A stateless
codec must not claim them or retain acquired-dependent session state.

Recommended next checks, not completed here:

* [ ] Enforce direction/order/count/completion at the paid immutable opcode
  and actual scratch PC; do not prefetch acquired-dependent payloads.
* [ ] Validate TEMPLATE paid semantic BAD exits and rejected-body no-input paths.
* [ ] Verify selected acquisition block against its external grouped schedule.
* [ ] Implement fresh ordinary construction and capability/reference cancellation
  at reset, then test actual production process/access boundaries.

No user clarification blocks the implemented component. None of these tests
certifies a full service flow, METER, isolation, erasure, or scientific result.