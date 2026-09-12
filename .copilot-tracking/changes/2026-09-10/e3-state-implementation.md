---
title: E3 state component implementation evidence
description: Scoped contract research and engineering-only state component validation.
ms.date: 2026-09-10
---

## Status

Complete for the requested state component and scoped contract research.
No VM, sandbox, empirical result, or implementation conformance claim is made.

## Questions

* What are the selected persistent layout, reset image, field and lane codecs?
* Which bytes must RAM access exclude, and how are raw physical faults preserved?
* What state-only API can the parent physics implementation use without mirrors?
* Which tests establish exact-size storage, reset independence, and bounds checks?

## Freeze evidence

Before creating any E3 implementation file, all 23 entries in
E3_DESIGN_FREEZE_v0_11.json passed byte-length and SHA-256 verification using
PowerShell Get-FileHash. The manifest kind is engineering_only_design_freeze;
final_target_draws_permitted and confirmatory_h2_permitted are both false.

## Contract findings

* E3_STATE_CONTRACT_v0_2.md selects 2,208 persistent bits, LSB-first packing, two's-complement signed fields, canonical code symbols 10, and zero auxiliary bytes. Complete reset creates a new object, not a partial mutation.
* E3_INTERFACE_CONTRACT_v0_9.md selects bytes 0..19 code, 20..211 Q, 212..216 ring, 217..220 staging, 221..224 transition, 225..226 energy, 227..230 material, 231..240 ages, 241..242 metadata, and 243..275 reserve. Invalid and reserved bits survive raw serialization unchanged.
* E3_PHYSICAL_CONTRACT_v0_4.md selects 1,104 lanes: 948 ordinary accessible RAM lanes, 24 typed reservoir lanes, and 132 reserve lanes. Stock caps are 65,535 and 255; resource faults are sinks, never bitwise RAM faults.
* E3_OPERATION_CONTRACT_v0_3.md requires a lane read, merge, and write for sub-two-bit RAM changes. Component masked-field writes are codec helpers, not a claim that this charged interpreter sequence has been implemented.
* Scratch is a separate 32-byte allocation: decoder bits 0..95, four arithmetic registers at bits 96, 128, 160, 192, and control bits 224..255. The latter contains PC16, address11, and flags5 under the selected v0.9 refinement.

## API and assumptions

The parent can import State, Scratch, and reset from e3 or e3.state. Constants
live in e3.state; all field offsets are GLOBAL BIT offsets, and all lane
indices are global two-bit indices. No FrozenG dependency is introduced.

| API | Exact behavior |
|-----|----------------|
| `State(raw: bytes \| bytearray \| None = None)` | Copy exactly 276 raw bytes, or create the canonical image |
| `State.snapshot() -> bytes` | Independent immutable raw copy; preserve every invalid and reserved bit |
| `State.read_bits(offset: int, width: int, signed: bool = False) -> int` | Checked 1..32-bit ordinary RAM field |
| `State.write_bits(offset: int, width: int, value: int, signed: bool = False) -> None` | Checked field replacement; no wrapping, saturation, or changes outside the field |
| `State.get_field` / `State.set_field` | Exact aliases of the two bit methods |
| `State.read_lane(index: int) -> int` | Raw ordinary RAM symbol 0..3, including invalid code 11 |
| `State.write_lane(index: int, symbol: int) -> None` | Checked ordinary RAM symbol replacement |
| `State.energy: int` | Read/write sole packed uint16 stock; 0..65535 |
| `State.P0` / `P1` / `P2` / `P3: int` | Read/write sole packed uint8 stocks; 0..255 |
| `State.read_material(index: int) -> int` | Typed material read, index 0..3 |
| `State.write_material(index: int, value: int) -> None` | Typed checked material assignment |
| `State._physics_read_lane(index: int) -> int` | Trusted raw RAM read, including reserve but excluding resources |
| `State._physics_write_lane(index: int, symbol: int) -> None` | Trusted raw RAM replacement, including reserve but excluding resources |
| `State.reset() -> State` / `state.reset() -> State` | New canonical object, no source argument or retained source reference |
| `Scratch(raw: bytes \| bytearray \| None = None)` | Independent exact 32-byte buffer; omitted input creates zeros |
| `Scratch.read_bits` / `write_bits` / `get_field` / `set_field` | Same checked codec signatures over 256 scratch bits |
| `Scratch.snapshot() -> bytes` | Immutable audit copy |
| `Scratch.clear() -> None` / `boundary() -> None` | Zero all 32 scratch bytes in place |
| `Scratch.is_zero() -> bool` | Current zero check, no stored mirror |

Both classes have exactly one bytearray slot and no instance dictionary.
Checks reject bool, coercible/noninteger arguments, non-bool signed flags,
oversized widths, negative or enormous indices, and out-of-range values.
Type errors raise TypeError; size/range errors raise ValueError; restricted
RAM/resource access raises PermissionError. Rejected mutations leave all bytes
unchanged. Ordinary access rejects resource lanes 900..923, reserve lanes
972..1103, and all fields that straddle these regions.

Trusted physics helpers are explicitly private-by-convention, not sandboxed.
They accept only integer lane/value arguments, not callbacks, arbitrary labels,
or fault frames. The parent physics owner must calculate simultaneous changes
from the pre-fault raw state and apply selected code-specific flip/erasure rules.
Every resource lane remains forbidden even to these helpers. Resource leakage
uses explicit checked typed sinks in the physics layer.

State access is a low-level codec, not a metered VM service. Label encoding,
decoding, read_label, FrozenG, and fault-frame application belong to other
components. Typed stock assignment rejects overflow instead of silently capping;
the future meter must compute accepted deposits and explicit overflow sinks.

## Validation evidence

* Python 3.13.3, existing editor-selected interpreter; standard library only, no installed dependencies
* Explicit focused unittest invocation with `-B`, never test discovery over E1/E2 or a conformance/history worker
* 24 tests passed twice after the import fix: 0.398 seconds verbose, then 0.268 seconds quiet
* No errors reported by the editor for all three Python files; Pylance syntax checks passed for state and test modules
* All 23 frozen files reverified after implementation, with byte lengths and SHA-256 unchanged
* No e3 bytecode directory and no state-test bytecode files created

Coverage includes 512 full-image byte fixtures (256 constant patterns and 256
position-varying patterns), all 2,208 one-hot persistent inputs, independent
per-bit codec oracles, all signed/unsigned widths 1..32 with all byte alignments,
2,000 seeded differential writes, all 948 ordinary RAM lanes, all 1,080 physical
RAM lanes, all 48 forbidden resource bits, and all 256 scratch bits. Tests check
full-image preservation on writes/rejections, canonical resets, copy independence,
single-buffer object shape, and unchanged stocks under ordinary RAM operations.

The first run found Python 3.13 eagerly evaluating the State return annotation
inside the State class. Postponed annotations fixed the import; syntax checks
alone would not have caught that runtime name lookup. A test loop variable was
also renamed to resolve a reported incompatible inferred type. Both fixes were
verified by the full focused test suite and clean editor diagnostics.

## Artifacts

Only these three implementation/test files and this permitted report were
created or edited by this task. No E1/E2 files or freeze documents were edited.

| Workspace-relative artifact | SHA-256 |
|-----------------------------|---------|
| e3/__init__.py | e3da9e14b43a5caf88600cb6ae924eeff106a98b30bc74268c519cf7c615b795 |
| e3/state.py | d23b78e26a5800857e3646c7942c35868790f12d3d801418c41cff231d92996c |
| test_e3_state.py | ac3bde60ea85e06c41d2bd02721e27650d938ab4c0d5fcfbd60199768b8b6d22 |

These are implementation evidence hashes, not a source/configuration/test freeze.

## Follow-up and clarifications

No clarifying user questions remain for this component. The following work is
intentionally not completed and requires separate scope/authorization:

* [ ] Integrate the actual paid READ2/WRITE2 interpreter, strict masked-bit instruction traces, meter, typed deposits/sinks, and phase/service permissions.
* [ ] Integrate simultaneous physical faults using the pre-fault packed ages, including reserve exposure and code erasure precedence.
* [ ] Enforce zero scratch on every actual operation/checkpoint/isolation/erasure boundary and audit cancellation of all external references, messages, and callbacks.
* [ ] Validate full history-dependent reset noninterference, immutable G/input provenance, process ownership, and interpreter reachability.

Calling State.reset does not clear an existing Scratch or cancel anything outside
the returned State. A raw snapshot does not certify a completed paid S boundary.
Python object overhead and temporary codec integers/byte slices are trusted-host
implementation machinery, not an opcode-level proof of the 256-bit scratch
budget. No code here implements a full VM or sandbox, draws final targets,
encodes/decodes labels, runs a history worker, or certifies G-INFO/G-ERASURE.