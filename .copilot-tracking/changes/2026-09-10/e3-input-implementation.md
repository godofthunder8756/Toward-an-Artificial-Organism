---
title: E3 indexed input implementation evidence
description: Contract research, narrow component implementation, and conformance evidence
ms.date: 2026-09-10
---

## Scope and status

Complete for the requested component scope. Added e3/inputs.py and
test_e3_inputs.py, with this requested optional evidence record. No live roots,
target draws, experimental execution, process isolation claim, or final launch.

## Research questions

* Verify the retained twelve-field HMAC tuple and bounded rejection law.
* Resolve schedule, pairing, reset, fault and SCRIPTED namespaces.
* Separate public conformance fixtures from worker capabilities and live provenance.
* Verify independent vectors, boundary tests, existing component compatibility,
  and preservation of the engineering design freeze.

## Evidence gathered

* E3_EVALUATION_CONTRACT_v0_7.md retains the HMAC-SHA-256 construction,
  first-sixteen-byte little-endian mapping, 1,024 attempts and balanced shuffles.
* E3_INTERFACE_CONTRACT_v0_9.md fixes all twelve coordinates, version
  E3-EVAL-0.8, numeric coordinates below 2^53, private ownership and slots 0..33.
  Decimal strings apply to manifest uint64 counters, not tuple coordinates.
* E3_CONFORMANCE_CONTRACT_v0_10.md and E3_INTEGRATION_DECISION_v0_11.md
  append H2-SCRIPTED slot 34, sharing codes/scripts/budgets and normalizing
  reset inputs to H2 without merging distinct G.

## Implementation and validation

e3/inputs.py implements the following external-only APIs:

* InputTuple and canonical_tuple: all twelve fields required, exact built-in
  types, ASCII strings, version E3-EVAL-0.8, nonnegative numeric coordinates
  through 9007199254740991 and attempt 0..1023
* indexed_digest and uniform: exact 32-byte keys, HMAC-SHA-256, first sixteen
  bytes little-endian, unbiased rejection, accepted-attempt provenance and
  technical failure after exactly 1024 rejected attempts
* SCHEDULE_CATALOG, phase_context and reset_context: explicit slots 0..34,
  checked individual/panel/cohort domains and unchanged schedule IDs;
  no branch, policy, code, candidate, history, result or budget key field
* generate_schedule: descending Fisher-Yates, cue-major initial multisets,
  sixteen grouped acquisition passes, recovery 16x8, assays 16x16,
  development 2043 admissions and H2 251+256 admissions with separate drains
* fault_coordinates and fault_inputs: 3160 current lane-major draws, skipping
  reservoir lanes 900..923 and including every reserve lane; compatible with
  e3/physical.py FaultFrame ordering without importing physical state
* Exact hazard thresholds, B/T/X ranges 2/3/16, planned guesses, 80-lane
  challenge inputs, whole-block/mixed U/O and balanced eight-panel HUB assignment
* bootstrap_coordinate: exact analysis tuple construction only; no matrix or
  bootstrap analysis is run

The restricted array serializer uses standard-library JSON. Its domain has no
objects, floats, nulls or booleans. ASCII escaping and integers below 2^53
match RFC 8785 without general-purpose floating-point or property-order logic.
Unicode and numeric strings are rejected rather than normalized or coerced.

Contract-selected namespace suffixes are literal H1/H2-TRUNK, SCREEN,
SELECTED-CONTROL, CORE and the diagnostic names, including H2-SCRIPTED.
RESET uses base H1/H2 with RESET-RECOVERY/RESET-FINAL. Oracle probes have
separate ZERO-FAULT/LIVE-WEAR phases. Distinct complete G remains an external
class criterion, even when normalized input coordinates agree.

The contracts do not spell every shuffle subpurpose or local scalar index.
The implementation makes these explicit in PURPOSE_ROOTS and docstrings:
swap draw_index is descending-swap ordinal starting at zero; acquisition
location is pass and slot is block; ordinary fault location is physical lane
and slot is local fault ordinal; guess slot is (tick-1)%5; preplanned shuffles
use tick zero and drains use actual planned ticks. These are source-level
conventions to bind in later provenance, not claims of previously specified
byte-exact protocol vectors for those subpurposes.

All execution in this task used public conformance constants, public analysis
single-vector checks or published RFC test fixtures. Keys are caller-owned;
the API validates shape, not provenance or independent CNG requests. No global
keys beyond the two published constants, mutable cursor, key loader, state
reader, packet adapter, root/target generator or entropy API was added.
The private digest test seam is not a public callback parameter.

Validation completed with the editor-selected Python 3.13 interpreter:

* 23/23 new deterministic tests pass, including RFC 4231 known answers,
  separate SHA256 ipad/opad construction, three hardcoded tuple payload/digest
  vectors, integer/ASCII/type boundaries, exact 1024-attempt rejection,
  endianness/window checks, independent schedule reconstruction and all slots
* Full E3 regression: 195 tests, OK with four existing skips; test_e3_design.py
  contains OS-dependent symlink fixture skips
* No editor errors in either new Python file; Pylance reports no module
  diagnostics and no test-file syntax errors
* Read-only design verification passes 23/23 entries before and after changes
* E3_DESIGN_FREEZE_v0_11.json SHA256 remains
  3678d797dc17485fcc823cb7f83696e4ba20c9a69921d709291cad50c3f878d4

The workspace is not a Git repository; no Git diff or clean-tree claim is made.

## External references

* [RFC 4231](https://www.rfc-editor.org/rfc/rfc4231), sections 4.2, 4.3 and
  4.7: independently published HMAC-SHA-256 known-answer vectors
* [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785), sections 3.2.1,
  3.2.2.2, 3.2.2.3 and 3.2.4: whitespace, string/number encoding and UTF-8

## Open questions and deferred checks

Actual process access denial, paid packet delivery, parent-state reset audits,
reference cancellation and complete replay require later integration. Pure
indexed functions cannot certify these properties.

* [ ] Bind source-level purpose/index conventions in the later private input
  provenance and validate purpose-root ownership without exposing live keys.
* [ ] Reject worker imports, IPC objects and inherited handles in actual process
  access tests; module naming and frozen dataclasses do not establish isolation.
* [ ] Audit actual populated/corrupt/dead source snapshots, cancellation and
  paired complete-G future trajectories before sharing canonical executions.
* [ ] Integrate one-way generation/consumption records with paid delivery,
  original traces and replay without exposing original due cues or attempts.

No user clarification is required for the implemented component. Final target
draws and the current full final launch remain prohibited by v0.11.